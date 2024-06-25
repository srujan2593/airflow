from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 25),
}

dag = DAG('kpo_test_dag', default_args=default_args, schedule_interval=None)

# Retrieve the image from the environment variable
kpo_image = os.environ.get('KPO_IMAGE', 'python:3.9-slim')

kpo_task = KubernetesPodOperator(
    task_id='kpo_test_task',
    name='kpo_test_task',
    namespace='default',
    image=kpo_image,
    cmds=["/bin/bash", "-c"],
    arguments=[
        "echo 'Hello from KubernetesPodOperator! Using image: " + kpo_image + "' && "
        "echo 'Waiting for 5 minutes...' && "
        "sleep 300 && "
        "echo 'Done waiting. Exiting now.'"
    ],
    dag=dag,
    get_logs=True,
)
