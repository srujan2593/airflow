from datetime import datetime, timedelta
import time

from airflow.models import DAG
from airflow.operators.python import PythonOperator

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def simulate_work(task_name, duration):
    print(f"Starting task: {task_name}")
    time.sleep(duration)  
    print(f"Finished task: {task_name}")

with DAG(
    'test_celery_executor_advanced',
    default_args=DEFAULT_ARGS,
    description='A DAG to test CeleryExecutor',
    schedule_interval=None,
    start_date=datetime(2024, 6, 14),
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id='task_short',
        python_callable=simulate_work,
        op_kwargs={'task_name': 'task_short', 'duration': 2}, 
    )

    task2 = PythonOperator(
        task_id='task_medium',
        python_callable=simulate_work,
        op_kwargs={'task_name': 'task_medium', 'duration': 5}, 
    )

    task3 = PythonOperator(
        task_id='task_long',
        python_callable=simulate_work,
        op_kwargs={'task_name': 'task_long', 'duration': 10}, 
    )

    task1 >> [task2, task3] 
