import os
import uuid
import optuna
import mlflow
import dill
import textwrap
import pandas as pd
# from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from minio import Minio

UNIQUE_PREFIX = str(uuid.uuid4())[:8]
BUCKET_NAME = "mlflow"
OBJECT_NAME = "iris"

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://0.0.0.0:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://0.0.0.0:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"


class CustomModel:
  def __init__(self, clf):
    self.clf = clf

  def predict(self, X):
    import pandas as pd
    X_pred = self.clf.predict(X)
    X_pred_df = pd.Series(X_pred).map({0: "virginica", 1: "setosa", 2:"versicolor"})
    return X_pred_df

def download_data():
  # minio client
  url = "0.0.0.0:9000"
  access_key = "minio"
  secret_key = "miniostorage"
  client = Minio(url, access_key=access_key, secret_key=secret_key, secure=False)


  # data download
  object_stat = client.stat_object(BUCKET_NAME, OBJECT_NAME)
  data_version_id = object_stat.version_id
  client.fget_object(BUCKET_NAME, OBJECT_NAME, file_path="data/download_iris_data.csv")
  return data_version_id

def load_data():
  data_version_id = download_data()
  df = pd.read_csv("data/download_iris_data.csv")
  X, y = df.drop(columns=["target"]), df["target"]
  data_dict = {"data": X, "target":y, "version_id": data_version_id}
  return data_dict

def objective(trial):

  trial.suggest_int("n_estimators", 100, 1000, step=100)
  trial.suggest_int("max_depth", 3, 10)
 
  run_name = f"{UNIQUE_PREFIX}-{trial.number}"
  with mlflow.start_run(run_name=run_name):

    # log parameter

    mlflow.log_params(trial.params)

    # load data

    data_dict = load_data()
    mlflow.log_param("bucket_name", BUCKET_NAME)
    mlflow.log_param("object_name", OBJECT_NAME)
    mlflow.log_param("version_id", data_dict["version_id"])
    X, y = data_dict["data"], data_dict["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2024)

    # train model

    clf = RandomForestClassifier(
        n_estimators=trial.params["n_estimators"], 
        max_depth=trial.params["max_depth"], 
        random_state=2024)
    clf.fit(X_train, y_train)

    # evaluate train model

    y_pred = clf.predict(X_test)
    acc_score = accuracy_score(y_test, y_pred)

    # log metrics

    mlflow.log_metric("accuracy", acc_score)
  return acc_score

def train_best_model(params):
    run_name = f"{UNIQUE_PREFIX}-best-model"
    with mlflow.start_run(run_name=run_name):

      # log parameter

      mlflow.log_params(params)
      
      # load data

      data_dict = load_data()
      mlflow.log_param("bucket_name", BUCKET_NAME)
      mlflow.log_param("object_name", OBJECT_NAME)
      mlflow.log_param("version_id", data_dict["version_id"])
      X, y = data_dict["data"], data_dict["target"]

      # train model

      clf = RandomForestClassifier(
          n_estimators=params["n_estimators"], 
          max_depth=params["max_depth"], 
          random_state=2024)
      clf.fit(X, y)

      my_model = CustomModel(clf)

      # mlflow.sklearn.log_model(sk_model=clf, artifact_path="best_model")
      with open("model.dill", "wb") as f:
        dill.dump(my_model, f)
        

      with open("loader.py", "w") as f:
        f.write(
          textwrap.dedent(
"""
import os
import dill

def _load_pyfunc(path):
  if os.path.isdir(path):
    path = os.path.join(path, "model.dill")
  with open(path, "rb") as f:
    return dill.load(f)
"""
          )
        )

      mlflow.pyfunc.log_model(
        artifact_path="best_model",
        data_path="model.dill",
        loader_module="loader",
        code_path=["loader.py"],
      )
      return clf


if __name__ == "__main__":

  # set mlflow
  study_name = "iris_RandomForest"
  mlflow.set_experiment(study_name)

  # study
  sampler = optuna.samplers.RandomSampler(seed=2024)
  study = optuna.create_study(sampler=sampler, study_name=study_name, direction="maximize")

  # optimaze
  study.optimize(objective, n_trials=5)

  best_params = study.best_params
  best_clf = train_best_model(best_params)
