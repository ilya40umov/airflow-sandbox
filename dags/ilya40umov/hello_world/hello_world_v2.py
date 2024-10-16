import random

from airflow.decorators import dag, task, task_group
from pendulum import datetime


@dag(
    schedule="@daily",
    start_date=datetime(2024, 9, 26),
    catchup=False,
    tags=["hello_world 👋"],
)
def hellow_world_v2():
    @task
    def look_up_name():
        return "Gandalf"

    @task
    def determine_confidence() -> float:
        return random.uniform(0.0, 1.0)

    # we could use the branch decorator instead of run_if/skip_if
    #
    # @task.branch
    # def choose_greeting(confidence: float) -> str:
    #     if confidence <= 0.5:
    #         return "greet_a_stranger"
    #     else:
    #         return "say_hello"

    @task.run_if(
        lambda context: context["task_instance"].xcom_pull(
            task_ids="determine_confidence", key="return_value"
        )
        > 0.5,
        skip_message="confidence is too low",
    )
    @task
    def print_hello_via_python(name: str):
        print(f"Hello ${name}")

    @task.run_if(
        lambda context: context["task_instance"].xcom_pull(
            task_ids="determine_confidence", key="return_value"
        )
        > 0.5,
        skip_message="confidence is too low",
    )
    @task.bash
    def print_hello_via_shell(name: str):
        return f'echo "Hello {name}!"'

    @task_group
    def say_hello(name: str) -> None:
        print_hello_via_python(name)
        print_hello_via_shell(name)

    @task.run_if(
        lambda context: context["task_instance"].xcom_pull(
            task_ids="determine_confidence", key="return_value"
        )
        <= 0.5,
        skip_message="confidence is too high",
    )
    @task
    def print_greeting() -> None:
        print("Greetings stranger!")

    @task_group
    def greet_a_stranger() -> None:
        print_greeting()

    looked_up_name = look_up_name()
    # noinspection PyTypeChecker,PyUnresolvedReferences
    determine_confidence() >> [say_hello(looked_up_name), greet_a_stranger()]


hellow_world_v2()
