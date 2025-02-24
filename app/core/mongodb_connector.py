from pymongo import MongoClient
from app.config import base_settings

class MongoConnector:
    def __init__(self, timeoutMs=None):
        db_settings = base_settings.DatabaseConfig()
        timeoutMs = timeoutMs if timeoutMs is not None else db_settings.get_database_timeout_ms()

        self.db = MongoClient(db_settings.get_database_url(), serverSelectionTimeoutMS=timeoutMs)[db_settings.get_database_name()]

    def salvar(self, collection, dados):
        return self.db[collection].insert_many(dados)
    def apagar(self, collection, filtro):
        return self.db[collection].delete_many(filtro)
    def buscar(self, collection, criterio_busca):
        return self.db[collection].find_one(criterio_busca)
    def listar(self, collection,filtro={}):
        return self.db[collection].find(filtro)