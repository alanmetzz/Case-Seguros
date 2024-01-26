from pythonjsonlogger import jsonlogger
import json
import logging
import os

def configure_logging():
    root_logger = logging.getLogger()
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    root_logger.setLevel(getattr(logging, log_level))  # Configure o nível de log conforme necessário

    formatter = jsonlogger.JsonFormatter('"%(asctime)s %(name)s %(levelname)s %(funcName)s:%(lineno)d %(message)s"')

    # Adiciona um manipulador de console com o formato JSON
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
