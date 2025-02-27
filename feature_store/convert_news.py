import os
import pandas as pd
import numpy as np
import mongodb_client as mongoclient
import text_preprocessor as tp
from datetime import datetime

categories = None

def get_categories_from_mongo():
    collection = 'categories'
    categories = mongoclient.list_data(name=collection)
    return categories

def chooseCategoryByWordIncidence(url, title, summary):
    
    url = url.replace("/", " ").replace("-"," ")
    fulltext = " ".join([url, title, summary])
    fulltext = tp.pre_proccess(fulltext)

    counts =  {category["categoria"]: 0 for category in categories}
    for word in fulltext.split(" "):
        for category in categories:
            cat_name = category["categoria"]
            cat_words= set(category["palavras_chave"])

            counts[cat_name] += word.lower() in cat_words
    if(all(x == 0 for x in counts.values())):
        return "geral"
    else:
        return max(counts, key=lambda key: counts[key])

def chooseCategoryScore(cat, target):
    if cat == target:
        return 100
    else:
        return 0
def getDateRelevance(creationDate, updateDate):
    creationDate = creationDate.split('+')[0]
    updateDate = updateDate.split('+')[0]

    #para esse experimento, a data de atualização está sempre preenchida então por mais que recebamos os dois parametros aqui, apenas o updateDate precisa ser considerado
    convertedCreationDate = datetime.strptime(creationDate, '%Y-%m-%d %H:%M:%S')
    convertedUpdateDate = datetime.strptime(updateDate, '%Y-%m-%d %H:%M:%S')

    cutDate = datetime(2022, 12, 1)
    daysBetweenMoreRecentAndCurrent = abs((cutDate - convertedUpdateDate).days)

    #o coeficiente de relevância vai estar diretamente ligado ao quão recente a noticia é, baseando se pela data de corte da noticia mais recente encontrada nos dados
    if daysBetweenMoreRecentAndCurrent <= 7:
        return 100
    elif daysBetweenMoreRecentAndCurrent > 7 and daysBetweenMoreRecentAndCurrent <=14:
        return 50
    elif daysBetweenMoreRecentAndCurrent > 14 and daysBetweenMoreRecentAndCurrent <=28:
        return 25
    else:
        return 12.25

    
def getData():
    itens_path = "feature_store/data/raw/news/"
    files = [f for f in os.listdir(itens_path) if f.startswith("itens-parte")]

    # Carregar os arquivos de itens
    df_itens_list = [pd.read_csv(os.path.join(itens_path, file)) for file in files]
    df_itens = pd.concat(df_itens_list, ignore_index=True)

    # Remove a coluna de body, que não será relevante para a nossa análise
    df_itens = df_itens.drop(columns=["body"])
    global categories
    categories = get_categories_from_mongo()

    df_itens["category"] = np.vectorize(chooseCategoryByWordIncidence)(df_itens["url"],df_itens["title"],df_itens["caption"])
    df_itens["relevance_score"] = np.vectorize(getDateRelevance)(df_itens["issued"],df_itens["modified"])

    data = df_itens.to_dict('records')

    mongoclient.save(obj_list=data,name='news')
    return df_itens
