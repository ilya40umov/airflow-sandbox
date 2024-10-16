import random
from typing import Any

from airflow import DAG
from airflow.models import TaskInstance
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.utils.task_group import TaskGroup
from pendulum import datetime


def _look_up_name() -> Any:
    return "Gandalf"


def _determine_confidence() -> Any:
    return random.uniform(0.0, 1.0)


def _choose_greeting(ti: TaskInstance) -> Any:
    confidence = ti.xcom_pull(task_ids="determine_confidence", key="return_value")
    if confidence <= 0.5:
        return "greet_a_stranger"
    else:
        return "say_hello"


def _print_hello(ti: TaskInstance) -> Any:
    name = ti.xcom_pull(task_ids="look_up_name", key="return_value")
    print(f"Hello ${name}")


def _print_greeting() -> Any:
    print("Greetings stranger!")


with DAG(
    dag_id="hello_world",
    start_date=datetime(2024, 9, 26),
    schedule="@daily",
    catchup=False,
    tags=["hello_world 👋"],
) as dag:
    look_up_name = PythonOperator(
        task_id="look_up_name",
        python_callable=_look_up_name,
    )

    determine_confidence = PythonOperator(
        task_id="determine_confidence",
        python_callable=_determine_confidence,
    )

    choose_greeting = BranchPythonOperator(
        task_id="choose_greeting", python_callable=_choose_greeting
    )

    with TaskGroup(group_id="say_hello") as say_hello:
        say_hello_via_shell = BashOperator(
            task_id="say_hello_via_shell",
            bash_command='echo "Hello {{ ti.xcom_pull(task_ids="look_up_name", key="return_value") }}!"',  # noqa: E501
        )

        say_hello_via_python = PythonOperator(
            task_id="say_hello_via_python",
            python_callable=_print_hello,
        )

    with TaskGroup(group_id="greet_a_stranger") as greet_a_stranger:
        greet_stranger_via_python = PythonOperator(
            task_id="greet_stranger_via_python",
            python_callable=_print_greeting,
        )

    (
        [look_up_name, determine_confidence]
        >> choose_greeting
        >> [say_hello, greet_a_stranger]
    )
