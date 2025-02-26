import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.mongo_db_tech_5 = os.getenv('mongo_db_tech_5') or "localhost"
        self.27017 = os.getenv('27017') or 27017
        self.root = os.getenv('root')
        self.pass123 = os.getenv('pass123')
        self.tech_db = os.getenv('tech_db')
        self.mongo_timeout_ms = os.getenv('MONGO_TIMEOUT_MS') or 15000

    def get_database_url(self):
        return f"mongodb://{self.root}:{self.pass123}@{self.mongo_db_tech_5}:{self.27017}/"

    def get_database_name(self):
        return self.tech_db

    def get_database_timeout_ms(self):
        return self.mongo_timeout_ms

class AppConfiguration:
    def __init__(self):
        self.url_arquivo = os.getenv('BASEURL_ARQUIVO_IMPORTACAO')
        self.url_fallback = os.getenv('BASEURL_ARQUIVO_FALLBACK')