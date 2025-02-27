from app.core import mongodb_connector
from pymongo.errors import ConnectionFailure

class HealthCheckService:

    @staticmethod
    def check():
        """
        Realiza um health check geral, verificando a API e a conexão com o MongoDB.

        Retorna:
            dict: Dicionário contendo os status dos serviços.
        """
        mongo_status = HealthCheckService.check_mongo()

        return {
            "healthy": mongo_status,
            "services": {
                "mongo": mongo_status
            }
        }

    @staticmethod
    def check_mongo():
        """
        Verifica a conectividade com o banco de dados MongoDB.

        Retorna:
            bool: True se o banco estiver acessível, False caso contrário.
        """
        try:
            mongo_connector = mongodb_connector.MongoConnector(timeoutMs=1000)
            mongo_connector.db.command("ping")  # Teste de ping no MongoDB
            return True
        except ConnectionFailure:
            return False
