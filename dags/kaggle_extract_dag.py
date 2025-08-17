import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append('/opt/airflow')

from src.data_extraction.kaggle_extractor import download_dataset, load_to_postgres
from src.data_transformation.process_sentiments import process_and_store_sentiments

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kaggle_social_media_extract',
    default_args=DEFAULT_ARGS,
    description='End-to-end social media sentiment ETL using Kaggle, PostgreSQL, and Airflow',
    schedule_interval='@daily',
    catchup=False,
    tags=['kaggle', 'social-media', 'etl', 'sentiment']
)

download_task = PythonOperator(
    task_id='download_kaggle_dataset',
    python_callable=download_dataset,
    op_kwargs={'dataset_name': 'kazanova/sentiment140'},
    dag=dag
)

load_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag
)

process_sentiment_task = PythonOperator(
    task_id='process_sentiments',
    python_callable=process_and_store_sentiments,
    op_kwargs={'batch_size': 400},  # <--- use your desired batch size
    dag=dag
)

download_task >> load_task >> process_sentiment_task