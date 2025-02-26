import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configurações do MongoDB a partir do .env
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

# Testando a função e imprimindo as categorias
if __name__ == "__main__":
    categories = get_categories_from_mongo()
    print("\nCategorias carregadas do MongoDB:")
    for categoria, palavras in categories.items():
        print(f"{categoria}: {', '.join(palavras)}")
