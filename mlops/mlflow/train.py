import uuid
import optuna
import mlflow
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


UNIQUE_PREFIX = str(uuid.uuid4())[:8]

def objective(trial):

  trial.suggest_int("n_estimators", 100, 1000, step=100)
  trial.suggest_int("max_depth", 3, 10)
 
  run_name = f"{UNIQUE_PREFIX}-{trial.number}"
  with mlflow.start_run(run_name=run_name):

    # log parameter

    mlflow.log_params(trial.params)

    # load data

    iris = load_iris(as_frame=True)
    X, y = iris["data"], iris["target"]
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

      iris = load_iris(as_frame=True)
      X, y = iris["data"], iris["target"]

      # train model

      clf = RandomForestClassifier(
          n_estimators=params["n_estimators"], 
          max_depth=params["max_depth"], 
          random_state=2024)
      clf.fit(X, y)
      return clf


if __name__ == "__main__":

  # set mlflow
  study_name = "iris_RandomForest"
  mlflow.set_tracking_uri("http://localhost:5001")
  mlflow.set_experiment(study_name)

  # study
  sampler = optuna.samplers.RandomSampler(seed=2024)
  study = optuna.create_study(sampler=sampler, study_name=study_name, direction="maximize")

  # optimaze
  study.optimize(objective, n_trials=5)

  best_params = study.best_params
  best_clf = train_best_model(best_params)
