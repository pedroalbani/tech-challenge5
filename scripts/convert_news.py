import os
import pandas as pd
import numpy as np

def chooseCategoryByWordIncidence(url, title, summary):
    categories = {'politica' : {'vota','politica','voto','stf','candidato','presidente','eleicoes','eleição','ministro','congresso','vereador','prefeito','vereadora','prefeita'},
    'cultura' : {'atriz','filme','cultura','cinema','teatro','ator','série','show','música','arte','pop','artista','cantor','cantora','album'},
    'tecnologia' : {'tecnologia','celular','game','console','smartphone','computador','notebook','tablet','streaming','elétrica','elétrico','aparelho','dispositivo'},
    'saude' : {'doença','saúde','saude','bem-estar','epidemia','sintoma','remédio','medicina','médico','tratamento','vacina'},
    'economia' : {'economia','imposto','renda','taxa','salário','tributação','dolar','real','euro','libra','R$','$', 'importar','importação','importacao'},
    'criminal' : {'polícia','prisão','crime','assassinato','sequestro','morte','inocente','culpado','bandido','criminoso','delegado','morto','mandado','morre','morta','facada','arma','tiro'}}
    
    
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
    

itens_path = "data/raw/news/"
files = [f for f in os.listdir(itens_path) if f.startswith("itens-parte")]

# Carregar os arquivos de itens
df_itens_list = [pd.read_csv(os.path.join(itens_path, file)) for file in files]
df_itens = pd.concat(df_itens_list, ignore_index=True)

# Remove a coluna de body, que não será relevante para a nossa análise
df_itens = df_itens.drop(columns=["body"])
df_itens["category"] = np.vectorize(chooseCategoryByWordIncidence)(df_itens["url"],df_itens["title"],df_itens["caption"])

df_itens.to_csv("data/processed/news.csv")