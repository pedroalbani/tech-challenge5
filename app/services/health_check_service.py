from urllib import request
from app.backend import mongodb_connector
from app.config.base_settings import AppConfiguration
from pymongo.errors import ConnectionFailure
from http import HTTPStatus

class HealthCheck():

    def __init__(self):
        self.app_settings = AppConfiguration()

    def check(self):
        mongo = self.check_mongo()
        embrapa = self.check_embrapa()

        is_healthy = mongo and embrapa

        return {
            "healthy": is_healthy,
            "services": {
                "mongo": mongo,
                "embrapa": embrapa
            }
        }
    
    def check_mongo(self):
        try:
            mongo_connector = mongodb_connector.MongoConnector(timeoutMs=1000)
            mongo_connector.db.command("ping")
            return True
        except ConnectionFailure:
            return False
        
    def check_embrapa(self):
        try:
            status_code = request.urlopen(self.app_settings.url_arquivo).getcode()
            return status_code == HTTPStatus.OK
        except:
            return False
