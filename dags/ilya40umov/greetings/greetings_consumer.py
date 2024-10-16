from airflow.decorators import dag, task
from ilya40umov.common import datasets
from pendulum import datetime


@dag(
    catchup=False,
    start_date=datetime(2024, 10, 15),
    schedule=datasets.GREETING_FILE,
    default_args={"do_xcom_push": False},
    tags=["greetings 🤝"],
)
def greetings_consumer():
    """
    ### Consumer Dag
    This one is processing the greetings file.
    """

    @task
    def read_greetings_file():
        """
        ### Greetings File Reader
        Here we read the greetings from the file.
        """
        with open(datasets.GREETING_FILE.uri, "r") as f:
            for line in f.readlines():
                print(line)

    read_greetings_file()


greetings_consumer()
