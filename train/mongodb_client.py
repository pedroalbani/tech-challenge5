from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis do .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@localhost:27017/")
DATABASE_NAME = os.getenv("MONGO_DATABASE", "tech_db")

def save(obj_list, collection):
    return 1

def list(collection, filter):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[collection]

    if filter is None:
        filter = {}
    data = list(collection.find(filter))

    return 1

def get(collection, filter:None):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[collection]
    if filter is None:
        filter = {}
    data = collection.find_one(filter)

    return data
