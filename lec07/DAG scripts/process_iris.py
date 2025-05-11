from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from python_scripts.train_model import process_iris_data
from python_scripts.send_email import send_notification_email

default_args = {
    'start_date': datetime(2025, 4, 22),
    'end_date': datetime(2025, 4, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='process_iris',
    default_args=default_args,
    schedule_interval='0 22 * * *',
    catchup=True,
    tags=['iris', 'ml'],
    description='ETL + ML pipeline for Iris dataset with accuracy and feature importance email',
) as dag:

    dbt_transform = BashOperator(
        task_id='dbt_transform',
        bash_command="""
            set -e
            cd /opt/airflow/dags/dbt/homework &&
            dbt run --profiles-dir /opt/airflow/dags/dbt \
            --select iris_processed \
            --vars '{"execution_date": "{{ ds }}"}' \
            --debug
        """
    )

    train_model = PythonOperator(
        task_id='train_model',
        python_callable=process_iris_data,
        op_kwargs={'ds': '{{ ds }}'},
        provide_context=True
    )

    send_email = PythonOperator(
        task_id='send_email_notification',
        python_callable=send_notification_email,
        provide_context=True
    )

    dbt_transform >> train_model >> send_email
