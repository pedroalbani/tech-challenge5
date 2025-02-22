import pandas as pd
import os

def fixDataToExplode(dataframe, column):
    return (dataframe[column].str.replace('\n', ' ').
        str.replace("'", ' ').
        str.replace("[", ' ').
        str.replace("]", ' ').
        str.strip().
        str.split(", "))
def fetch():
    data_path = "data/raw/history/"
    arquivos = [f for f in os.listdir(data_path) if f.startswith("treino_parte")]
    # Carregar os arquivos de treino
    df_list = [pd.read_csv(os.path.join(data_path, file)) for file in arquivos]
    df_completo = pd.concat(df_list, ignore_index=True)

    return df_completo

def explodeDataframe(df_completo):
    df_completo['history'] = fixDataToExplode(df_completo,'history')
    df_completo['timestampHistory'] = fixDataToExplode(df_completo,'timestampHistory')
    df_completo['numberOfClicksHistory'] = fixDataToExplode(df_completo,'numberOfClicksHistory')
    df_completo['timeOnPageHistory'] = fixDataToExplode(df_completo,'timeOnPageHistory')
    df_completo['scrollPercentageHistory'] = fixDataToExplode(df_completo,'scrollPercentageHistory')
    df_completo['pageVisitsCountHistory'] = fixDataToExplode(df_completo,'pageVisitsCountHistory')
    df_completo['timestampHistory_new'] = fixDataToExplode(df_completo,'timestampHistory_new')

    df_exploded = df_completo.explode(['history','timestampHistory','numberOfClicksHistory','timeOnPageHistory','scrollPercentageHistory','pageVisitsCountHistory','timestampHistory_new']).reset_index(drop=True)
    df_exploded.columns = ['userId','userType','historySize','page','timestampPage','numberOfClicks','timeOnPage','scrollPercentage','pageVisitsCount','timestamp_new']
    
    return df_exploded

def getData():
    dataframe = fetch()
    return explodeDataframe(dataframe)
