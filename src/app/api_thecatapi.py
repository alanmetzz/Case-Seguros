import os
import requests
import logging

logger = logging.getLogger(__name__)

def consumir_api_thecatapi(url):
    api_key = os.environ.get('THECATAPI_API_KEY', None)

    if not api_key:
        logger.warning('A API Key da TheCatAPI nao esta configurada. As solicitacoes podem ser limitadas.')

    try:
        headers = {'x-api-key': api_key} if api_key else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f'Erro ao consumir a API TheCatAPI: {str(e)}')
        return response