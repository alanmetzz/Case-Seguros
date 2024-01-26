from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from .routes import racas_routes
import logging


def create_app():
    # Cria a instância do aplicativo Flask
    app = Flask(__name__)

    log = logging.getLogger('werkzeug').disabled = True
    app.logger.disabled = True

    # Registra as rotas no aplicativo
    app.register_blueprint(racas_routes)

    #Prometheus
    metrics = PrometheusMetrics(app, path='/metrics', group_by='path', port=8000)
    metrics.info('app_info', 'Application info', version='1.0.3')
    metrics.start_http_server(8000)

    return app