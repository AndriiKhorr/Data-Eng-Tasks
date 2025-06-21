from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "andrii",
    "start_date": datetime(2025, 6, 1),
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id="enrich_user_profiles",
    default_args=default_args,
    schedule_interval=None,  # запуск вручну
    catchup=False,
    description="Збагачення customers із user_profiles через Spark",
) as dag:

    enrich_customers = BashOperator(
        task_id="run_spark_job_enrich_user_profiles",
        bash_command="spark-submit /opt/airflow/spark_jobs/enrich_user_profiles_spark.py"
    )

    enrich_customers
