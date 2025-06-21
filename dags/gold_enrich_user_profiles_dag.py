from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "andrii",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="gold_enrich_user_profiles",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Enrich customers_updated with data from user_profiles (birth_date, phone)",
    tags=["gold", "user_profiles", "enrichment"],
) as dag:

    run_spark_job = BashOperator(
        task_id="run_gold_enrich_user_profiles",
        bash_command="spark-submit /opt/airflow/spark_jobs/gold_enrich_user_profiles_spark.py"
    )

    run_spark_job
