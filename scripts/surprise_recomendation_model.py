import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from surprise import accuracy, Dataset, SVD,Reader
from surprise.model_selection import train_test_split
import create_masterdata as master_data

df_masterdata = master_data.getMasterData()
scaler = MinMaxScaler(feature_range=(0,100))

ct = ColumnTransformer(
    [("num_preprocess", scaler, ["strength","pol_score","eco_score","cul_score","tec_score","sau_score","cri_score","ger_score"])],remainder='passthrough')

ct.set_output(transform='pandas')

df_teste = ct.fit_transform(df_masterdata)
print(df_teste.head())
print(list(df_teste.columns.values))

df_masterdata['strength'] = df_teste['num_preprocess__strength']
df_masterdata['pol_score'] = df_teste['num_preprocess__pol_score']
df_masterdata['eco_score'] = df_teste['num_preprocess__eco_score']
df_masterdata['cul_score'] = df_teste['num_preprocess__cul_score']
df_masterdata['tec_score'] = df_teste['num_preprocess__tec_score']
df_masterdata['sau_score'] = df_teste['num_preprocess__sau_score']
df_masterdata['cri_score'] = df_teste['num_preprocess__cri_score']
df_masterdata['ger_score'] = df_teste['num_preprocess__ger_score']

df_masterdata = df_masterdata.reset_index()

print(df_masterdata.head())
print(list(df_masterdata.columns.values))

reader = Reader(rating_scale=(1, 100))

#data = Dataset.load_from_df(df_masterdata[["userId", "page", "strength","pol_score","eco_score","cul_score","tec_score","sau_score","cri_score","ger_score"]], reader)
data = Dataset.load_from_df(df_masterdata[["userId", "page", "strength"]], reader)
trainset, testset = train_test_split(data, test_size=0.25)

# Train the algorithm on the trainset, and predict ratings for the testset
algo = SVD(n_factors=100, reg_all=0.05)

algo.fit(trainset)
predictions = algo.test(testset)

# Then compute RMSE
accuracy.rmse(predictions)

# sim_options = {
#     "name": "cosine",
#     "user_based": False,  # Compute  similarities between items
# }

#algo = KNNBaseline(sim_options=sim_options)

# svd = SVD(n_factors=100, reg_all=0.05)
# svd.fit(dataset)
# predict = svd.predict(uid='f98d1132f60d46883ce49583257104d15ce723b3bbda2147c1e31ac76f0bf069',iid ='3325b5a1-979a-4cb3-82b6-63905c9edbe8')
# print(predict)
# Run 5-fold cross-validation and print results.
#cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

#algo.fit(data)
# trainingSet = data.build_full_trainset()

