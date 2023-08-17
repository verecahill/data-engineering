## MLflow

- Macine Learning LifeCycle Management
- Model Registry

## Optuna

- Hypterparmeter Optimization

## K-fold validation

- find best paramters and model

## Data version

- MINIO

```
docker run -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minio -e MINIO_ROOT_PASSWORD=miniostorage minio/minio server /data/minio/ --console-address :9001
```

## Docker compose

- mlflow : ML Lifecycle Management, Model Registry

- minio : Artifact Store, Data Versioning

- postgres (Backend Store)

## How to Start

```
docker compose --build
docker compose up -d
http://localhost:5001
python upload_data_minio.py
python train.py
python mlflow_load_model.py --run-id {run_id in mlflow}


# batch serving
python make_batch_data.py
python predict --run-id {your trained model run_id}
# check minio predicted bucket

# predict with docker container
docker build -t batch_predict -f batch.Dockerfile .
docker network ls
docker run --network mlflow_default batch-serving {your run-id}

# predict with downloaded model
python download_model.py --run-id {your run_id}
python image_batch_predict.py

# predict with docker container using a downloaded model
docker build -t image-batch-predict -f image_batch.Dockerfile .
docker run --network mlflow_default image-batch-predict

# api serving
cd fastapi
uvicorn app:app --reload --host 0.0.0.0

# api serving with docker
docker build -t api-serving -f api.Dockerfile .
docker run -p 8000:8000 api-serving
```
