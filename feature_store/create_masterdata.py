import pandas as pd
import numpy as np
import convert_history as history
import convert_news as news
import mongodb_client as mongoclient

def defineEventStrength(timeOnPage, scrolledPercent,timesVisited, numberOfClicks,relevance):
    #definiremos da seguinte forma, total scrollado da página, é o atributo mais importante, número de clicks o segundo, vezes visitados o terceiro e tempo de página o quarto
    #fator_forca = ((3*fator_recente) + (2 * percentual_scrollado/100) + n_clicks + (tempo_pagina/60k)) /4
    timeOnPage = int(timeOnPage)/1000/60 #convertido para minuto
    scrolledPercent = float(scrolledPercent) *2 /100  
    numberOfClicks = int(numberOfClicks)
    timesVisited = int(timesVisited) * 3

    return (((float(relevance)*4) + timesVisited + timeOnPage + numberOfClicks + scrolledPercent)/5)

def getMasterData():
    df_news = news.getData().set_index("page")    
    df_history = history.getData().set_index("page")

    df_master = df_history.join(df_news)
    df_master = df_master.drop(columns=['url','title','caption'])
    df_master['strength'] = np.vectorize(defineEventStrength)(df_master["timeOnPage"],df_master["scrollPercentage"],df_master["pageVisitsCount"],df_master['numberOfClicks'],df_master['relevance_score'])
    

    mongoclient.save(obj_list=df_master.to_dict("records"),name='master_data')

    return df_master