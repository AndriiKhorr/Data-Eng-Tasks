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

def run_spark_job():
    subprocess.run([
        "spark-submit",
        "/opt/airflow/spark_jobs/process_sales_spark.py"
    ], check=True)

with DAG(
    dag_id="process_sales",
    default_args=default_args,
    description="Run PySpark sales ETL from inside Airflow container",
    schedule_interval=None,  # ручний запуск
    start_date=datetime(2025, 6, 1),
    catchup=False,
    tags=["sales", "spark"]
) as dag:

    spark_task = PythonOperator(
        task_id="run_sales_etl_spark",
        python_callable=run_spark_job
    )
