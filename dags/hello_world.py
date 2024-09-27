from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_world",
    start_date=datetime(2024, 9, 26),
    schedule="@daily",
    catchup=False,
) as dag:
    say_hello_via_shell = BashOperator(
        task_id="say_hello_via_shell",
        bash_command="echo 'hello world!'",
    )
