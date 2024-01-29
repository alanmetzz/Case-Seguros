from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from .routes import racas_routes
import logging
from flasgger import Swagger

# Variável para indicar o estado de readiness
ready = False

def create_app():
    # Cria a instância do aplicativo Flask
    app = Flask(__name__)

    log = logging.getLogger('werkzeug').disabled = True
    app.logger.disabled = True

    # Registra as rotas no aplicativo
    app.register_blueprint(racas_routes)

    # Configurar o Swagger
    Swagger(app, template_file='../docs/swagger.yaml')

    #Prometheus
    metrics = PrometheusMetrics(app, path='/metrics', group_by='path', port=8000)
    metrics.info('app_info', 'Application info', version='1.0.3')
    metrics.start_http_server(8000)

    # Endpoint de healthcheck
    @app.route('/health', methods=['GET'])
    def healthcheck():
        return jsonify({'status': 'OK'})

    # Endpoint de readiness
    @app.route('/readiness', methods=['GET'])
    def readiness():
        global ready
        if ready:
            return jsonify({'status': 'OK'})
        else:
            return jsonify({'status': 'Not Ready'}), 503

    # Endpoint de liveness
    @app.route('/liveness', methods=['GET'])
    def liveness():
        return jsonify({'status': 'OK'})

    # Função a ser chamada antes a primeira requisição
    @app.before_first_request
    def set_ready():
        global ready
        ready = True

    return app