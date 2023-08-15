import mlflow
mlflow.set_tracking_uri("http://localhost:5001")
mlflow.set_experiment("test01")
# mlflow.log_param("my_param", 1)
# params = {"my_second_param": 2, "my_third_param": 3}
# mlflow.log_params(params)

# mlflow.log_metric("my_metric", 0.1)
# metrics = {"my_second_metric": 0.2, "my_thrid_metric": 0.3}
# mlflow.log_metrics(metrics)

# mlflow.log_metric("history", 0.1, step=1)
for i in range(3):
    with mlflow.start_run():
      mlflow.log_param("trial", i)
      mlflow.log_metric("metric", i+1)