import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis do .env
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

def chooseCategoryByWordIncidence(url, title, summary):
    categories = get_categories_from_mongo()

    url = url.replace("/", " ").replace("-"," ")
    fulltext = " ".join([url, title, summary])

    counts = dict.fromkeys(categories, 0)
    for word in fulltext.split(" "):
        for cat_name, cat_words in categories.items():
            counts[cat_name] += word.lower() in cat_words
    if(all(x == 0 for x in counts.values())):
        return "geral"
    else:
        return max(counts, key=lambda key: counts[key])

def getData():
    itens_path = "data/raw/news/"
    files = [f for f in os.listdir(itens_path) if f.startswith("itens-parte")]

    # Carregar os arquivos de itens
    df_itens_list = [pd.read_csv(os.path.join(itens_path, file)) for file in files]
    df_itens = pd.concat(df_itens_list, ignore_index=True)

    # Remove a coluna de body, que não será relevante para a nossa análise
    df_itens = df_itens.drop(columns=["body"])
    df_itens["category"] = np.vectorize(chooseCategoryByWordIncidence)(df_itens["url"],df_itens["title"],df_itens["caption"])
    #df_itens.to_csv('data/processed/news.csv')

    return df_itens
