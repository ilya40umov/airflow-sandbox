from airflow.decorators import dag, task
from ilya40umov.common import datasets
from pendulum import datetime, duration


@dag(
    catchup=False,
    start_date=datetime(2024, 10, 15),
    schedule=duration(days=1),
    default_args={"do_xcom_push": False},
    tags=["greetings 🤝"],
)
def greetings_producer():
    """
    ### Producer Dag
    This one is populating the greetings file.
    """

    @task(outlets=datasets.GREETING_FILE)
    def write_greetings_file():
        """
        ### Greetings File Writer
        Here we write the greetings to the file.
        """
        with open(datasets.GREETING_FILE.uri, "w") as f:
            f.writelines(
                [f"{text}\n" for text in ["Willkommen", "bienvenue", "welcome"]]
            )

    write_greetings_file()


greetings_producer()
