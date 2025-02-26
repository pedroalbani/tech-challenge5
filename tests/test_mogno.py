import os
import pytest
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@localhost:27017/")
DATABASE_NAME = os.getenv("MONGO_DATABASE", "tech_db")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "categories")

def get_categories_from_mongo():
    """ Obtém as categorias e palavras-chave diretamente do MongoDB. """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    categories = {}
    for category in collection.find({}, {"_id": 0, "categoria": 1, "palavras_chave": 1}):
        categories[category["categoria"]] = set(category["palavras_chave"])

    client.close()
    return categories

def test_get_categories_from_mongo():
    categories = get_categories_from_mongo()
    assert isinstance(categories, dict)
    assert len(categories) > 0
    for categoria, palavras in categories.items():
        assert isinstance(categoria, str)
        assert isinstance(palavras, set)
        assert all(isinstance(palavra, str) for palavra in palavras)
