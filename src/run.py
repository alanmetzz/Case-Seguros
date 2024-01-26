from app import create_app
from app.database.database import inicializar_banco_dados
from app.initial_flow import iniciar_coleta_em_segundo_plano,total_racas
from app.config import configure_logging

# Configura logs
configure_logging()

# Inicializa o banco de dados
inicializar_banco_dados()

# Total de raças
total_racas()

if __name__ == "__main__":
    app = create_app()
    iniciar_coleta_em_segundo_plano()
    app.run(debug=False, host='0.0.0.0', port=5000)