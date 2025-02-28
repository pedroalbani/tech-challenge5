import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from surprise import accuracy, Dataset, SVD,Reader, KNNBaseline
from surprise.model_selection import train_test_split
import create_masterdata as master_data
import mlflow
from mlflow.models import infer_signature
import os

# Converte o trainset para um DataFrame
def trainset_to_dataframe(trainset):
    data = []
    for user_id, item_id, rating in trainset.all_ratings():
        data.append([trainset.to_raw_uid(user_id), trainset.to_raw_iid(item_id), rating])

    return pd.DataFrame(data, columns=["userId", "page", "strength"])

MLFLOW_HOST = os.getenv("MLFLOW_HOST", "http://127.0.0.1:8080")
#realiza treinamento do modelo e loga no mlflow
# quando roda a api, o mlflow é iniciado e o treinamento é feito
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

        trainset_df = trainset_to_dataframe(train_set)
        testset_df = pd.DataFrame(test_set, columns=["userId", "page", "strength"])

        # Infer the model signature
        signature = infer_signature(trainset_df, testset_df)

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
    mlflow.set_tracking_uri(uri=MLFLOW_HOST) ## url do mlflow
    df_masterdata = master_data.getMasterData() ## pega os dados do masterdata
    max_strength = df_masterdata["strength"].max()
    min_strength = df_masterdata["strength"].min()
    df_masterdata = scaleData(df_masterdata) ## normaliza os dados,
    input_sample = df_masterdata.head(50) ## pega uma amostra dos dados para serem usados como exemplo no mlflow

    print(df_masterdata.head())
    print(list(df_masterdata.columns.values))

    reader = Reader(rating_scale=(min_strength, max_strength)) ## define o range de valores para o rating baseado no minimo e maximo do dataset

    data = Dataset.load_from_df(df_masterdata[["userId", "page", "strength"]], reader) # transforma o dataset em um dataset do surprise
    trainset, testset = train_test_split(data, test_size=0.25)

    # Train the algorithm on the trainset, and predict ratings for the testset
    svd_options = {
        'n_factors':100,
        'reg_all' :0.05
    }

    algo = SVD(n_factors=svd_options["n_factors"], reg_all = svd_options["reg_all"])
    # o SVD não foi o melhor pq ele ficou como o RSME muito alto, o que indica que ele não está conseguindo prever bem os valores

    runModel(algo,trainset,testset,'SVD Experimentation',svd_options,"SVD","Experiment with Scikit Surprise SVD model",input_sample)

    # treinamodelo com o KNNBaseline
    knn_options = {
        "name": "cosine",
        "user_based": True,  # Compute  similarities between items
    }

    algo = KNNBaseline(sim_options=knn_options)
    runModel(algo,trainset,testset,'KNN Experimentation',knn_options,"KNNBaseline","Experiment with Scikit Surprise KNN Baseline model",input_sample)
