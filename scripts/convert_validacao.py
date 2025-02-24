import pandas as pd

def fixDataToExplode(dataframe, column):
    return (dataframe[column].str.replace('\n', ' ').
        str.replace("'", ' ').
        str.replace("[", ' ').
        str.replace("]", ' ').
        str.replace("\r", ' '). 
        str.replace("\n", ' ').
        str.strip().
        str.split())

def getData():
    validacao_path = "data/raw/validacao.csv"

    # Carregar os arquivos de itens
    df_validacao = pd.read_csv(validacao_path)
    df_validacao['history'] = fixDataToExplode(df_validacao,'history')
    df_validacao['timestampHistory'] = fixDataToExplode(df_validacao,'timestampHistory')

    df_exploded = df_validacao.explode(['history','timestampHistory'])
    df_exploded.columns = ['userId','userType','page','timestamppage']
    print(df_exploded.head())
    return df_exploded
