import mlflow
from datetime import datetime
from app.backend.mongodb_connector import MongoConnector
from operator import itemgetter
import os

class PredictionService:
    def __init__(self):
        self.MLFLOW_HOST = os.getenv("MLFLOW_HOST", "http://127.0.0.1:8080")
        self.model_name = 'KNNBaseline'
        self.version = "latest" # sempre vai pegar a última versão
        self.db = MongoConnector()

    def load_model(self):
        mlflow.set_tracking_uri(uri=self.MLFLOW_HOST)
        model_uri = f"models:/{self.model_name}/{self.model_version}"
        model = mlflow.sklearn.load_model(model_uri)

        return model

    # função que faz a predição
    # recebe o id do usuário e as notícias mais relevantes para ele
    def use_model(self, user_id, news):
        model = self.load_model() # carrega o modelo do mlflow
        predictions = []
        for new in news:
            pred = model.predict(uid=user_id,iid =new['_id']).est # faz a predição
            predictions.append({'_id':new["_id"], 'strength':pred})  # adiciona a predição na lista (noticia, força da predição)
        predictions = sorted(predictions, key=itemgetter('strength'), reverse=True)[:5] # ordena as predições e pega as 5 mais fortes

        # retorna as 5 notícias mais relevantes
        return predictions

    # ponto de entrada da api
    def suggest_news(self,user_id:str):
        user_db = self.db.buscar('data_users',{"userId": user_id})
        more_relevant_news = []

        # caso o usuário exista, vai na master data para
        # buscar as 100 noticias mais relevantes que o usuário não leu
        if(user_db is not None):
            more_relevant_news = self.db.listar_com_aggregate('master_data',[{"$match":{"userId":{"$ne":user_id}}},{"$group": {"_id": "$page", "sum_strength": {"$sum": "$strength"}}},{'$sort': {'sum_strength': -1}},{'$limit': 500}])
            # manda para o modelo para que seja feita a predição
            more_relevant_news = self.use_model(user_id, more_relevant_news)
        else: # caso o usuário não exista, pega as 10 noticias mais relevantes
            more_relevant_news =self.db.listar_com_aggregate('master_data',[{"$group": {"_id": "$page", "sum_strength": {"$sum": "$strength"}}},{'$sort': {'sum_strength': -1}},{'$limit': 10}])

        # pega as noticias mais relevantes para o usuário
        news_for_user = self.db.listar('news',{ 'page': { '$in': [new['_id'] for new in more_relevant_news ] } })
        # monta o objeto de resposta
        user_pred = {'user':user_id, 'predictions': [ {'page':new['page'], 'url': new['url']} for new in news_for_user], 'timestamp': datetime.now()}

        # salva a predição no banco
        self.db.salvar("predictions",user_pred)
        return user_pred

