from app.backend import mongodb_connector, query_builder

class ComercioService:

    def __init__(self):
        self.db = mongodb_connector.MongoConnector()
        self.query_builder = query_builder.QueryBuilder()
    
    def listar_comercios(self, filtro):
        comercios = self.db.listar("comercio",filtro)

        return comercios