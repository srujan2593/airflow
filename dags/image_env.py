from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import os
from datetime import datetime

# Define the DAG
with DAG(
    dag_id="kpo_os_env_example",
    start_date=datetime(2024, 6, 25), 
    schedule_interval=None, 
    catchup=False
) as dag:
    # Fetch the image name from OS environment variable
    image_name = os.getenv("KPO_IMAGEE", "python:3.9-slim")
    
    # Define the KubernetesPodOperator task
    kpo_task = KubernetesPodOperator(
        task_id="my_kpo_task",
        name="my-pod",
        namespace="airflow-cluster",  
        image=image_name, 
        cmds=["sleep", "10"],
    )
