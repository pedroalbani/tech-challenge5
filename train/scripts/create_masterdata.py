import pandas as pd
import convert_history as history
import convert_news as news


df_news = news.getData().set_index("page")
print(df_news.shape)

df_history = history.getData().set_index("page")
print(df_history.shape)


df_master = df_history.join(df_news)
df_master = df_master.drop(columns=['url','title','caption'])
print(df_master.head())
df_master.to_csv('data/processed/master_data.csv')