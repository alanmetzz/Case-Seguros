from app.api_thecatapi import consumir_api_thecatapi
from app.database.database import (
    inserir_info_basica_no_banco,
    inserir_imagens_no_banco,
    verificar_existencia_raca
)
import time
import logging
import threading
import os


logger = logging.getLogger(__name__)

# Função para iniciar a coleta em segundo plano
def iniciar_coleta_em_segundo_plano():
    initial_flow_cats = os.environ.get('INITIAL_FLOW_CATS', 'FALSE').upper()
    initial_flow_hats_cats = os.environ.get('INITIAL_FLOW_HATS_CATS', 'FALSE').upper()

    logger.info(f"A variavel de carga inicial esta definida como: {initial_flow_cats}")
    logger.info(f"A variavel de carga inicial esta definida como: {initial_flow_hats_cats}")

    if initial_flow_cats == "TRUE":
        thread_info_gatos  = threading.Thread(target=coletar_info_gatos)
        thread_info_gatos .start()

    if initial_flow_hats_cats == "TRUE":
        thread_salvar_imagens = threading.Thread(target=coletar_e_salvar_imagens)
        thread_salvar_imagens.start()

def total_racas():
    racas_api = consumir_api_thecatapi('https://api.thecatapi.com/v1/breeds')

    if racas_api:
        racas = racas_api.json()
        number_of_breeds = len(racas)
        logger.info(f"O numero de racas de gatos na API: {number_of_breeds}")

    else:
        logger.info(f"Erro ao acessar a API. Codigo de status: {racas_api.status_code}")

def coletar_info_gatos():
    try:
        logger.info(f'Iniciando a carga base.')
        # Coletar informações sobre todas as raças disponíveis
        racas_api = consumir_api_thecatapi('https://api.thecatapi.com/v1/breeds')
        if racas_api:
            racas = [raca['id'] for raca in racas_api.json()]

            for raca_id in racas:
                time.sleep(0.5)
                # Coletar informações da API TheCatAPI para cada raça
                info_gato_api = consumir_api_thecatapi(f'https://api.thecatapi.com/v1/breeds/{raca_id}')
                # Aguarde 1 segundo entre as solicitações
                if info_gato_api and isinstance(info_gato_api.json(), dict):  # Verificar se a resposta é um dicionário
                    nome_raca = info_gato_api.json().get('name', '')

                    # Verificar se a raça já existe no banco de dados
                    if verificar_existencia_raca(nome_raca):
                        logger.warning(f'A raça {nome_raca} já existe no banco. As informações não foram inseridas novamente.')
                        continue  # Pular para a próxima iteração
                    if not info_gato_api or not info_gato_api.ok:
                        logger.warning(f'Não foi possível obter informações da raça com ID {raca_id} da API TheCatAPI.')
                        continue
                    try:
                        info_gato_api_json = info_gato_api.json()
                    except ValueError:
                        logger.warning(f'Resposta da API TheCatAPI não contém JSON válido para a raça {raca_id}.')
                        continue
                    info_gato = {
                        'name': info_gato_api_json.get('name', ''),
                        'origin': info_gato_api_json.get('origin', ''),
                        'temperament': info_gato_api_json.get('temperament', ''),
                        'description': info_gato_api_json.get('description', ''),
                        'image': {'url': []}  # Inicializar a lista de URLs de imagens
                    }

                    # Coletar informações adicionais com imagens aleatórias
                    time.sleep(0.5)
                    imagens_aleatorias = consumir_api_thecatapi(f'https://api.thecatapi.com/v1/images/search?breed_id={raca_id}&limit=3')
                    if imagens_aleatorias and imagens_aleatorias.ok:
                        try:
                            imagens_aleatorias_json = imagens_aleatorias.json()
                        except ValueError as e:
                            logger.warning(f'Resposta da API TheCatAPI (imagens aleatórias) não contém JSON válido para a raça {raca_id}. Erro: {str(e)}')
                            imagens_aleatorias_json = []
                    else:
                        logger.warning(f'Não foi possível obter imagens aleatórias para a raça com ID {raca_id}. Status code: {imagens_aleatorias.status_code}')
                        imagens_aleatorias_json = []

                    # Combinar URLs de imagens aleatórias
                    info_gato['image']['url'].extend([img['url'] for img in imagens_aleatorias_json])

                    # Limitar a 3 imagens por raça
                    info_gato['image']['url'] = info_gato['image']['url'][:3]

                    # Inserir informações no banco de dados
                    inserir_info_basica_no_banco(info_gato)
                    inserir_imagens_no_banco(info_gato)

                    logger.info(f'Informações da raça {info_gato["name"]} coletadas e salvas no banco.')
                else:
                    logger.warning(f'Não foi possível obter informações da raça com ID {raca_id} da API TheCatAPI.')
        else:
            logger.warning('Não foi possível obter a lista de raças da API TheCatAPI.')
        logger.info(f'Finalizado a carga base.')
    except Exception as e:
        logger.error(f'Erro ao coletar informações dos gatos: {str(e)}')

def coletar_e_salvar_imagens():
    imagens_com_chapeu = consumir_api_thecatapi(f'https://api.thecatapi.com/v1/images/search?category_ids=1&limit=3')
    imagens_com_oculos = consumir_api_thecatapi(f'https://api.thecatapi.com/v1/images/search?category_ids=4&limit=3')

    urls_chapeu = [img['url'] for img in imagens_com_chapeu.json()] if imagens_com_chapeu and imagens_com_chapeu.ok else []
    urls_oculos = [img['url'] for img in imagens_com_oculos.json()] if imagens_com_oculos and imagens_com_oculos.ok else []

    for url in urls_chapeu:
        info_imagem = obter_info_imagem(url)
        if info_imagem:
            info_gato = {
                'name': info_imagem.get('breeds')[0]['name'] if 'breeds' in info_imagem else 'Desconhecida',
                'image': {'url': [url]}
            }
            inserir_info_basica_no_banco(info_gato)
            inserir_imagens_no_banco(info_gato)

    for url in urls_oculos:
        info_imagem = obter_info_imagem(url)
        if info_imagem:
            info_gato = {
                'name': info_imagem.get('breeds')[0]['name'] if 'breeds' in info_imagem else 'Desconhecida',
                'image': {'url': [url]}
            }
            inserir_info_basica_no_banco(info_gato)
            inserir_imagens_no_banco(info_gato)

# Função para obter informações detalhadas de uma imagem
def obter_info_imagem(url):
    try:
        response = consumir_api_thecatapi(f'https://api.thecatapi.com/v1/images?&url={url}')
        return response.json()[0] if response and response.ok else None
    except Exception as e:
        logger.warning(f'Erro ao obter informações da imagem: {str(e)}')
        return None