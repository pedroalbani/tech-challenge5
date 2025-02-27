import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.mongo_host = os.getenv('MONGO_DB_TECH_5', 'localhost')
        self.mongo_port = int(os.getenv('MONGO_PORT', 27017))
        self.mongo_user = os.getenv('MONGO_USER', 'root')
        self.mongo_password = os.getenv('MONGO_PASSWORD', 'pass123')
        self.mongo_db_name = os.getenv('MONGO_DB_NAME', 'tech_db')
        self.mongo_timeout_ms = int(os.getenv('MONGO_TIMEOUT_MS', 15000))

    def get_database_url(self):
        """Gera a URL de conexão com o MongoDB."""
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"

    def get_database_name(self):
        """Retorna o nome do banco de dados."""
        return self.mongo_db_name

    def get_database_timeout_ms(self):
        """Retorna o timeout da conexão em milissegundos."""
        return self.mongo_timeout_ms

# Instância global para acesso às configurações
db_config = DatabaseConfig()
