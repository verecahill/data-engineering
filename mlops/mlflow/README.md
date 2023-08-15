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

```
docker compose up -d --build
http://localhost:5001
```

- mlflow : ML Lifecycle Management, Model Registry

- minio : Artifact Store, Data Versioning

- postgres (Backend Store)
