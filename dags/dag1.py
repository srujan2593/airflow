from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2023, 1, 1),
}

# Create a DAG object
dag = DAG(
    'kubernetes_executor_example',
    default_args=default_args,
    schedule_interval=None,
    tags=['example', 'kubernetes']
)

# Task 1: A simple Python task running in the default (Celery) executor
def print_hello():
    print("Hello from CeleryExecutor!")

task_1 = PythonOperator(
    task_id='celery_task',
    python_callable=print_hello,
    dag=dag,
)

# Task 2: A task running in a Kubernetes pod
task_2 = KubernetesPodOperator(
    task_id='kubernetes_task',
    namespace='default',
    image='python:3.9',
    cmds=["python", "-c"],
    arguments=["print('Hello from KubernetesExecutor!')"],
    name="kubernetes_task_pod",
    in_cluster=True,    # Assuming Airflow is running in the Kubernetes cluster
    is_delete_operator_pod=True,
    get_logs=True,
    dag=dag,
    queue='kubernetes_queue',  # This assigns the task to the Kubernetes queue
)

# Define task dependencies
task_1 >> task_2
