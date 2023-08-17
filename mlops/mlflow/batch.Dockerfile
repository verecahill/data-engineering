FROM amd64/python:3.9-slim

WORKDIR /usr/app/

RUN pip install -U pip &&\
    pip install mlflow==2.5.0 boto3==1.28.26 minio==7.1.15

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY image_predict.py predict.py
ENTRYPOINT [ "python", "predict.py", "--run-id" ]