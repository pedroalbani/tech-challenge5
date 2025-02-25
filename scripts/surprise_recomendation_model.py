import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from surprise import accuracy, Dataset, SVD,Reader, KNNBaseline
from surprise.model_selection import train_test_split
import create_masterdata as master_data

def runModel (algo, trainset,testset):
    algo.fit(trainset)
    predictions = algo.test(testset)

    # Then compute RMSE
    accuracy.rmse(predictions)


def scaleData(dataset):
    scaler = MinMaxScaler(feature_range=(dataset["strength"].min(),dataset["strength"].max()))

    ct = ColumnTransformer(
        [("num_preprocess", scaler, ["strength"])],remainder='passthrough')

    ct.set_output(transform='pandas')

    df_scaled = ct.fit_transform(df_masterdata)

    dataset['strength'] = df_scaled['num_preprocess__strength']    
    dataset = dataset[dataset['strength'] > 0]
    return df_masterdata.reset_index()

def modelPredict(algo, user, item):
     predict = algo.predict(uid=user,iid =item)
     print(predict)

df_masterdata = master_data.getMasterData()
df_masterdata = scaleData(df_masterdata)

print(df_masterdata.head())
print(list(df_masterdata.columns.values))

reader = Reader(rating_scale=(1, 100))

data = Dataset.load_from_df(df_masterdata[["userId", "page", "strength"]], reader)
trainset, testset = train_test_split(data, test_size=0.25)

# Train the algorithm on the trainset, and predict ratings for the testset
algo = SVD(n_factors=100, reg_all=0.05)
runModel(algo,trainset,testset)
modelPredict(algo,'f98d1132f60d46883ce49583257104d15ce723b3bbda2147c1e31ac76f0bf069','3325b5a1-979a-4cb3-82b6-63905c9edbe8')

sim_options = {
    "name": "cosine",
    "user_based": True,  # Compute  similarities between items
}

algo = KNNBaseline(sim_options=sim_options)
runModel(algo,trainset,testset)
modelPredict(algo,'f98d1132f60d46883ce49583257104d15ce723b3bbda2147c1e31ac76f0bf069','3325b5a1-979a-4cb3-82b6-63905c9edbe8')

