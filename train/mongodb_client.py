from dotenv import load_dotenv
from pymongo import MongoClient
import os

# Carregar variáveis do .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@localhost:27017/")
DATABASE_NAME = os.getenv("MONGO_DATABASE", "tech_db")

def save(obj_list, collection):
    return 1

def list_data(name, filter=None):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[name]

    if filter is None:
        filter = {}
    data = list(collection.find(filter))
    client.close()

    return data

def get(name, filter:None):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[name]
    if filter is None:
        filter = {}
    data = collection.find_one(filter)
    client.close()

    return data
    
