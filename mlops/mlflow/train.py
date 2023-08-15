import mlflow
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

mlflow.set_tracking_uri("http://localhost:5001")
mlflow.set_experiment("iris_RandomForest")

with mlflow.start_run():

  # log parameter

  params = {"n_estimator": 100, "max_depth": 5}
  mlflow.log_params(params)

  # load data

  iris = load_iris(as_frame=True)
  X, y = iris["data"], iris["target"]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2024)

  # train model

  clf = RandomForestClassifier(n_estimators=params["n_estimator"], max_depth=params["max_depth"], random_state=2024)
  clf.fit(X_train, y_train)

  # evaluate train model

  y_pred = clf.predict(X_test)
  acc_score = accuracy_score(y_test, y_pred)

  print("Accuracry score is {:.4f}".format(acc_score))

  # log metrics
  
  mlflow.log_metric("accuracy", acc_score)

