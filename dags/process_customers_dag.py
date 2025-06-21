from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    "owner": "andrii",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_customers_spark():
    subprocess.run([
        "spark-submit", "/opt/airflow/spark_jobs/process_customers_spark.py"
    ], check=True)

with DAG(
    dag_id="process_customers",
    default_args=default_args,
    description="ETL pipeline for customers data",
    schedule_interval=None,
    start_date=datetime(2025, 6, 1),
    catchup=False,
    tags=["customers", "spark"],
) as dag:

    run_etl = PythonOperator(
        task_id="run_customers_etl_spark",
        python_callable=run_customers_spark,
    )
