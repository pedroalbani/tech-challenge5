import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.mongo_host = os.getenv('MONGO_HOST') or "localhost"
        self.mongo_port = os.getenv('MONGO_PORT') or 27017
        self.mongo_username = os.getenv('MONGO_USERNAME')
        self.mongo_password = os.getenv('MONGO_PASSWORD')
        self.mongo_database = os.getenv('MONGO_DATABASE')
        self.mongo_timeout_ms = os.getenv('MONGO_TIMEOUT_MS') or 15000

    def get_database_url(self):
        return f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"

    def get_database_name(self):
        return self.mongo_database

    def get_database_timeout_ms(self):
        return self.mongo_timeout_ms

class AppConfiguration:
    def __init__(self):
        self.url_arquivo = os.getenv('BASEURL_ARQUIVO_IMPORTACAO')
        self.url_fallback = os.getenv('BASEURL_ARQUIVO_FALLBACK')