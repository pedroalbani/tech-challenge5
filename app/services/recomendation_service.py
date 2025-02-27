from app.backend import mongodb_connector, query_builder
from bson import json_util
import json

class RecommendationService:
    def __init__(self):
        self.db = mongodb_connector.MongoConnector()
        self.query_builder = query_builder.QueryBuilder()

    def get_all_categories(self, filtro):
        """ Obtém todas as categorias armazenadas no MongoDB e converte para JSON serializável. """

        print(f"Aplicando filtro: {filtro}")  # Log do filtro aplicado

        categories = list(self.db.listar("categories"))  # Obtém os registros
        print(f"Registros encontrados: {categories}")  # Log dos dados retornados

        if not categories:
            print("Nenhuma categoria encontrada no banco de dados.")
            return {"message": "Nenhuma categoria encontrada"}

        return json.loads(json_util.dumps(categories))  # Retorna JSON serializável
