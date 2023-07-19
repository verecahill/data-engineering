## Data Engineering GCP

- Folder

  - data : source data
    - retail data
  - notebook : data processing

- Google Cloud SDK

  - gcloud init
  - gsutil list

- bucket

  - gsutil ls -r gs://wjdatalake
  - gcloud auth application-default login

- datalake

  - gcp bucket
  - upload files (csv, parquet, metadata(schema))

- data warehouse

  - BigQuery
  - PostgresSQL

```
CREATE SCHEMA dw_retail;

CREATE OR REPLACE EXTERNAL TABLE dw_retail.orders (
  order_id INTEGER,
  order_date TIMESTAMP,
  order_customer_id INTEGER,
  order_status STRING
) OPTIONS (
  format='csv',
  uris=['gs://wjdatalake/data/retail_db/orders/part*']
);
```

```
CREATE OR REPLACE EXTERNAL TABLE dw_retail.order_items (
  order_item_id INTEGER,
  order_item_order_id INTEGER,
  order_item_product_id INTEGER,
  order_item_quantity INTEGER,
  order_item_subtotal DECIMAL,
  order_item_product_price DECIMAL
) OPTIONS (
  format='csv',
  uris=['gs://wjdatalake/data/retail_db/order_items/part*']
);
```

- workflow

  - Airflow (GCP composer)
  - Astro cli
    - brew install astro
    - astro dev init
    - astro dev start
    - astro dev ps
    - astro dev bash scheduler (Run a bash command in the scheduler docker container)
    - pip install apache-airflow==2.4.2

- Spark, Flink

  - dataproc
  - Databricks

- DBT

  - Fivetran

## Data Pipeline

- Retail data
- Tweet data
- Transport
  - Data : TLC(Taxi & Limousine) Trip Record Data
    - 2009 ~ 2021 year
  - batch (Airflow)
    - Data source -> Spark Job(Data preprocessing) -> Spark Job(ML Train) -> Data target
  - steam
    - Data source -> Kafka -> Flink -> Data target
