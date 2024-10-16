import time

from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime, duration

with DAG(
    dag_id="default_args_dag",
    catchup=False,
    tags=["misc 🗑️"],
    default_args={
        "owner": "airflow",
        "depends_on_past": True,
        "email": "airflow@example.com",
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 3,
        "retry_delay": duration(minutes=5),
        "retry_exponential_backoff": False,
        "max_retry_delay": duration(hours=1),
        "start_date": datetime(2024, 1, 1),
        "end_date": datetime(2024, 12, 31),
        "schedule": "@daily",
        "catchup": False,
        "sla": duration(hours=2),
        "execution_timeout": duration(minutes=30),
        "wait_for_downstream": True,
        "trigger_rule": "all_success",
    },
) as dag:
    sleep = PythonOperator(task_id="sleep", python_callable=lambda: time.sleep(1))
