import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from surprise import accuracy, Dataset, SVD,Reader, KNNBaseline
from surprise.model_selection import train_test_split
import create_masterdata as master_data
import mlflow
from mlflow.models import infer_signature
import os

MLFLOW_HOST = os.getenv("MLFLOW_HOST", "http://127.0.0.1:8080")

def runModel (algo, train_set,test_set,experiment_name,hyper_params, model_name, description, input_sample):
    mlflow.set_experiment(experiment_name=experiment_name)
    algo.fit(train_set)
    predictions = algo.test(test_set)
    # Then compute RMSE
    rmse = accuracy.rmse(predictions)

    with mlflow.start_run():
        # Log the hyperparameters
        mlflow.log_params(hyper_params)

        # Log the loss metric
        mlflow.log_metric("rmse", rmse)

        # Set a tag that we can use to remind ourselves what this run was for
        mlflow.set_tag("Training Info", description)

        # Infer the model signature
        signature = infer_signature(train_set, algo.test(test_set))

        # Log the model
        model_info = mlflow.sklearn.log_model(
            sk_model=algo,
            artifact_path="news_prediction",
            signature=signature,
            input_example=input_sample,
            registered_model_name=model_name,
        )

def scaleData(dataset):
    scaler = MinMaxScaler(feature_range=(dataset["strength"].min(),dataset["strength"].max()))

    ct = ColumnTransformer(
        [("num_preprocess", scaler, ["strength"])],remainder='passthrough')

    ct.set_output(transform='pandas')

    df_scaled = ct.fit_transform(dataset)

    dataset['strength'] = df_scaled['num_preprocess__strength']    
    dataset = dataset[dataset['strength'] > 0]
    return dataset.reset_index()

def train_model():
    mlflow.set_tracking_uri(uri=MLFLOW_HOST)
    df_masterdata = master_data.getMasterData()
    df_masterdata = scaleData(df_masterdata)
    input_sample = df_masterdata.head(50)

    print(df_masterdata.head())
    print(list(df_masterdata.columns.values))

    reader = Reader(rating_scale=(1, 100))

    data = Dataset.load_from_df(df_masterdata[["userId", "page", "strength"]], reader)
    trainset, testset = train_test_split(data, test_size=0.25)

    # Train the algorithm on the trainset, and predict ratings for the testset
    svd_options = {
        'n_factors':100,
        'reg_all' :0.05
    }

    algo = SVD(n_factors=svd_options["n_factors"], reg_all = svd_options["reg_all"])
    runModel(algo,trainset,testset,'SVD Experimentation',svd_options,"SVD","Experiment with Scikit Surprise SVD model",input_sample)

    knn_options = {
        "name": "cosine",
        "user_based": True,  # Compute  similarities between items
    }

    algo = KNNBaseline(sim_options=knn_options)
    runModel(algo,trainset,testset,'KNN Experimentation',knn_options,"KNNBaseline","Experiment with Scikit Surprise KNN Baseline model",input_sample)


