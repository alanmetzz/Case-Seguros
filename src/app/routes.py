from flask import Blueprint, jsonify, request, Response
from app.database.database import (
    buscar_racas_por_origem_from_database,
    listar_racas_from_database,
    buscar_info_raca_from_database,
    buscar_racas_por_temperamento_from_database,
    buscar_imagens_por_raca_from_database,
    buscar_racas_por_temperamento_e_origem_from_database
)
import logging
import os


logger = logging.getLogger(__name__)

def configurar_timeout(resposta):
    try:
        # Configurar um timeout para a resposta
        timeout = float(os.environ.get('TIMEOUT', 5.0))  # Valor padrão de 5 segundos se a variável de ambiente não estiver definida
        resposta.timeout = timeout
        return resposta
    except ValueError as e:
        logger.error(f'Erro ao configurar o timeout: {str(e)}')
        return resposta

racas_routes = Blueprint('racas_routes', __name__)
racas_routes.after_request(configurar_timeout)

@racas_routes.route('/raca/details', methods=['GET'])
def info_raca():
    raca_id = request.args.get('raca_id')
    try:
        info_raca = buscar_info_raca_from_database(raca_id)
        if info_raca:
            # Buscar imagens por raça
            imagens = buscar_imagens_por_raca_from_database(info_raca['id'])
            info_raca['images'] = imagens

            return jsonify([{'id': info_raca['id'], 'breed_id': info_raca['breed_id'], 'raca': info_raca['raca'], 'origem': info_raca['origem'], 'temperamento': info_raca['temperamento'], 'descricao': info_raca['descricao'], 'imagens': info_raca['images']}])
        else:
            return jsonify({'message': 'Raca nao encontrada'}), 404
    except Exception as e:
        logger.error(f'Erro ao obter informacoes da raca: {str(e)}')
        return jsonify({'message': 'Erro ao obter informacoes da raca'}), 500

@racas_routes.route('/racas', methods=['GET'])
def listar_racas():
    try:
        racas = listar_racas_from_database()
        return jsonify({'racas': racas})
    except Exception as e:
        logger.error(f'Erro ao buscar/listar raca: {str(e)}')
        return jsonify({'message': 'Erro ao buscar/listar raca'}), 500

@racas_routes.route('/racas_by', methods=['GET'])
def filtrar_racas():
    try:
        temperamento = request.args.get('temperamento')
        origem = request.args.get('origem')

        if temperamento and origem:
            racas = buscar_racas_por_temperamento_e_origem_from_database(temperamento, origem)
        elif temperamento:
            racas = buscar_racas_por_temperamento_from_database(temperamento)
        elif origem:
            racas = buscar_racas_por_origem_from_database(origem)

        return jsonify({'racas': racas})
    except Exception as e:
        logger.error(f'Erro ao buscar/listar racas: {str(e)}')
        return jsonify({'message': 'Erro ao buscar/listar racas por temperamento ou origem'}), 500

racas_routes