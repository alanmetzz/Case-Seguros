import sqlite3
import logging
import os

logger = logging.getLogger(__name__)
DB_FILE = os.path.join(os.path.dirname(__file__), 'files/gatos.db')

def obter_conexao():
    return sqlite3.connect(DB_FILE)

def tabela_existe(nome_tabela):
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (nome_tabela,))
        result = cursor.fetchone()
        return result[0] == 1
    except Exception as e:
        logger.error(f'Erro ao verificar se a tabela existe: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def criar_tabela_gatos():
    try:
        conn = obter_conexao()
        cursor = conn.cursor()

        if not tabela_existe('gatos'):
            cursor.execute('''
                CREATE TABLE gatos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    breed_id TEXT NOT NULL,
                    raca TEXT NOT NULL,
                    origem TEXT,
                    temperamento TEXT,
                    descricao TEXT,
                    imagem TEXT
                )
            ''')
            logger.info('Tabela gatos criada no banco de dados.')
        else:
            logger.info('Tabela gatos já existe no banco de dados.')

        conn.commit()
    except Exception as e:
        logger.error(f'Erro ao criar tabela gatos: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def criar_tabela_imagens():
    try:
        conn = obter_conexao()
        cursor = conn.cursor()

        if not tabela_existe('imagens'):
            cursor.execute('''
                CREATE TABLE imagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    raca_id INTEGER,
                    url TEXT NOT NULL,
                    FOREIGN KEY(raca_id) REFERENCES gatos(id)
                )
            ''')
            logger.info('Tabela imagens criada no banco de dados.')
        else:
            logger.info('Tabela imagens já existe no banco de dados.')

        conn.commit()
    except Exception as e:
        logger.error(f'Erro ao criar tabela imagens: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def inicializar_banco_dados():
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()

        # Chamar a função para criar a tabela
        criar_tabela_gatos()
        criar_tabela_imagens()

        logger.info('Banco de dados inicializado com sucesso.')
    except Exception as e:
        logger.error(f'Erro ao inicializar o banco de dados: {str(e)}')
    finally:
        if conn:
            conn.close()


def verificar_existencia_raca(breed_id):
    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute('SELECT breed_id FROM gatos WHERE breed_id = ?', (breed_id,))
    resultado = cursor.fetchone()

    conn.close()

    return resultado is not None

def inserir_info_basica_no_banco(info_gato):
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()

        # Converter todas as informações para minúsculas
        info_gato_lower = {key: value.lower() if isinstance(value, str) else value for key, value in info_gato.items()}

        # Verificar se a raça já existe no banco
        cursor.execute('SELECT breed_id FROM gatos WHERE breed_id = ?', (info_gato_lower['breed_id'],))
        resultado = cursor.fetchone()

        if resultado is None:
            # Inserir informações básicas do gato
            cursor.execute('''
                INSERT INTO gatos (breed_id, raca, origem, temperamento, descricao)
                VALUES (?, ?, ?, ?, ?)
            ''', (info_gato_lower['breed_id'], info_gato_lower['name'], info_gato_lower.get('origin', ''), info_gato_lower.get('temperament', ''), info_gato_lower.get('description', '')))

            conn.commit()
            logger.info(f'Informações básicas do gato {info_gato_lower["name"]} inseridas no banco.')
        else:
            logger.warning(f'A raça {info_gato_lower["name"]} já existe no banco. As informações não foram inseridas novamente.')

    except Exception as e:
        logger.error(f'Erro ao inserir informações básicas no banco: {str(e)}')
    finally:
        if conn:
            conn.close()

def inserir_imagens_no_banco(info_gato,tipo):
    try:
        conn = obter_conexao()
        cursor = conn.cursor()

        if tipo == "normal":
            # Obter o ID da raça no banco de dados
            cursor.execute('SELECT id FROM gatos WHERE breed_id = ?', (info_gato['breed_id'],))
            raca_id = cursor.fetchone()
        else:
            raca_id[0] = 0

        if raca_id:
            raca_id = raca_id[0]
            # Inserir imagens no banco de dados
            for url in info_gato['image']['url']:
                cursor.execute('INSERT INTO imagens (raca_id, url) VALUES (?, ?)', (raca_id, url))

            logger.info(f'Imagens da raça {info_gato["name"]} salvas no banco de dados.')
        else:
            logger.warning(f'Ração {info_gato["name"]} não encontrada no banco de dados.')

        conn.commit()
    except Exception as e:
        logger.error(f'Erro ao inserir imagens no banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

# Alteração na função listar_racas_from_database
def listar_racas_from_database():
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()

        cursor.execute('SELECT id, breed_id, raca FROM gatos GROUP BY raca')
        racas = [{'id': r[0], 'breed_id': r[1],'raca': r[2]} for r in cursor.fetchall()]

        logger.info('Lista de raças recuperada do banco de dados.')
        return racas
    except Exception as e:
        logger.error(f'Erro ao listar raças do banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def obter_raca_id(raca_id):
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()
        if raca_id.isdigit():
            cursor.execute('SELECT id FROM gatos WHERE id = ? LIMIT 1', (raca_id,))
            raca_id_normalizado = cursor.fetchone()
        else:
            cursor.execute('SELECT id FROM gatos WHERE breed_id = ? LIMIT 1', (raca_id,))
            raca_id_normalizado = cursor.fetchone()

        if raca_id_normalizado:
            return raca_id_normalizado[0]
        else:
            return raca_id
    except Exception as e:
        logger.error(f'Erro ao buscar informações da raça do banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def buscar_info_raca_from_database(raca_id):
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()
        raca_id_normalizado = obter_raca_id(raca_id)

        cursor.execute('SELECT id, breed_id, raca, origem, temperamento, descricao FROM gatos WHERE id = ? LIMIT 1', (raca_id_normalizado,))
        info_raca = cursor.fetchone()

        if info_raca:
            return {'id': info_raca[0], 'breed_id': info_raca[1], 'raca': info_raca[2], 'origem': info_raca[3], 'temperamento': info_raca[4], 'descricao': info_raca[5]}
        else:
            return None
    except Exception as e:
        logger.error(f'Erro ao buscar informações da raça do banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()


def buscar_imagens_por_raca_from_database(raca_id):
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()

        # Buscar imagens por raça
        cursor.execute('SELECT url FROM imagens WHERE raca_id = ?', (raca_id,))
        imagens = [{'url': imagem[0]} for imagem in cursor.fetchall()]

        logger.info(f'Imagens para a raça {raca_id} recuperadas do banco de dados.')
        return imagens
    except Exception as e:
        logger.error(f'Erro ao buscar imagens por raça do banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def buscar_racas_por_temperamento_from_database(temperamento):
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()

        cursor.execute('SELECT id, breed_id, raca FROM gatos WHERE temperamento LIKE ? GROUP BY raca', (f'%{temperamento}%',))
        racas = [{'id': r[0], 'breed_id': r[1], 'raca': r[2]} for r in cursor.fetchall()]

        logger.info(f'Raças com temperamento {temperamento} recuperadas do banco de dados.')
        return racas
    except Exception as e:
        logger.error(f'Erro ao buscar raças por temperamento do banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def buscar_racas_por_origem_from_database(origem):
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()

        cursor.execute('SELECT id, breed_id, raca FROM gatos WHERE origem = ? GROUP BY raca', (origem,))
        racas = [{'id': r[0], 'breed_id': r[1], 'raca': r[2]} for r in cursor.fetchall()]

        logger.info(f'Raças com origem {origem} recuperadas do banco de dados.')
        return racas
    except Exception as e:
        logger.error(f'Erro ao buscar raças por origem do banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()

def buscar_racas_por_temperamento_e_origem_from_database(temperamento, origem):
    try:
        # Obter conexão ao banco de dados SQLite
        conn = obter_conexao()
        cursor = conn.cursor()

        cursor.execute('SELECT id, breed_id, raca FROM gatos WHERE temperamento LIKE ? AND origem = ? GROUP BY raca', (f'%{temperamento}%',origem,))
        racas = [{'id': r[0], 'breed_id': r[1], 'raca': r[2]} for r in cursor.fetchall()]

        logger.info(f'Raças com origem {origem} e temperamento {temperamento} recuperadas do banco de dados.')
        return racas
    except Exception as e:
        logger.error(f'Erro ao buscar raças por origem e temperamento do banco de dados: {str(e)}')
        raise
    finally:
        if conn:
            conn.close()