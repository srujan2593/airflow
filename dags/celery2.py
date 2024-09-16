import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

def heavy_computation():
    """Simulate a heavy computation by sleeping for 5 seconds."""
    time.sleep(5)
    return "Heavy computation complete."

def fetch_data():
    """Simulate data fetching by sleeping for 3 seconds."""
    time.sleep(3)
    return "Data fetching complete."

def process_data():
    """Simulate data processing by sleeping for 4 seconds."""
    time.sleep(4)
    return "Data processing complete."

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'complex_task_workflow_new',
    default_args=default_args,
    description='A DAG with multiple complex tasks to test CeleryExecutor.',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    heavy_computation_task = PythonOperator(
        task_id='heavy_computation',
        python_callable=heavy_computation
    )

    fetch_data_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data
    )

    process_data_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data
    )

    end = DummyOperator(
        task_id='end'
    )

    start >> [heavy_computation_task, fetch_data_task] >> process_data_task >> end
