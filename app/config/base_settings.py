import socket
from pymongo import MongoClient

class DatabaseConfig:
    def __init__(self):
        self.mongo_host = "localhost"
        self.mongo_port = 27017
        self.mongo_user = "root"
        self.mongo_password = "pass123"
        self.mongo_db_name = "tech_db"
        self.mongo_timeout_ms = 15000

    def get_database_url(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"

    def get_database_name(self):
        return self.mongo_db_name

    def get_database_timeout_ms(self):
        return self.mongo_timeout_ms

    def test_connection(self):
        mongo_uri = self.get_database_url()
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=self.mongo_timeout_ms)
            client.admin.command("ping")
            print(f"✅ Conexão bem-sucedida com MongoDB em {self.mongo_host}:{self.mongo_port}")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar ao MongoDB: {e}")
            return False

db_config = DatabaseConfig()

print("🔍 Configuração do MongoDB :")
print(f"🔹 MONGO_HOST: {db_config.mongo_host}")
print(f"🔹 MONGO_PORT: {db_config.mongo_port}")
print(f"🔹 MONGO_USERNAME: {db_config.mongo_user}")
print(f"🔹 MONGO_DATABASE: {db_config.mongo_db_name}")
