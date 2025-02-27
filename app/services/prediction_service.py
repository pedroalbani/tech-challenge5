import mlflow
from datetime import datetime
from app.backend.mongodb_connector import MongoConnector
from operator import itemgetter
import os

class PredictionService:
    def __init__(self):
        self.MLFLOW_HOST = os.getenv("MLFLOW_HOST", "http://127.0.0.1:8080")
        self.model_name = 'KNNBaseline'
        self.version = "latest"
        self.db = MongoConnector()

    def load_model(self):
        mlflow.set_tracking_uri(uri=self.MLFLOW_HOST)
        model_uri = f"models:/{self.model_name}/{self.model_version}"
        model = mlflow.sklearn.load_model(model_uri)

        return model
    
    def use_model(self, user_id, news):
        model = self.load_model()
        predictions = []
        for new in news:
            pred = model.predict(uid=user_id,iid =new['_id']).est
            predictions.append({'_id':new["_id"], 'strength':pred})
        predictions = sorted(predictions, key=itemgetter('strength'), reverse=True)[:5]

        return predictions
    
    def suggest_news(self,user_id:str):        
        user_db = self.db.buscar('data_users',{"userId": user_id})
        more_relevant_news = []

        if(user_db is not None):
            more_relevant_news = self.db.listar_com_aggregate('master_data',[{"$match":{"userId":{"$ne":user_id}}},{"$group": {"_id": "$page", "sum_strength": {"$sum": "$strength"}}},{'$sort': {'sum_strength': -1}},{'$limit': 500}])
            more_relevant_news = self.use_model(user_id,more_relevant_news) 
        else:
            more_relevant_news =self.db.listar_com_aggregate('master_data',[{"$group": {"_id": "$page", "sum_strength": {"$sum": "$strength"}}},{'$sort': {'sum_strength': -1}},{'$limit': 10}])

        news_for_user = self.db.listar('news',{ 'page': { '$in': [new['_id'] for new in more_relevant_news ] } })
        user_pred = {'user':user_id, 'predictions': [ {'page':new['page'], 'url': new['url']} for new in news_for_user], 'timestamp': datetime.now()}

        self.db.salvar("predictions",user_pred)
        return user_pred

