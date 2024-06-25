from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'test_kubernetes_pod_operator',
    default_args=default_args,
    description='Test Kubernetes Pod Operator with an image from an environment variable',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Retrieve the image from an environment variable
image_name = os.getenv('KPO_IMAGE', 'busybox:latest')  # Default to busybox if not specified
logger.info(f"Using image: {image_name}")

# Define the task using KubernetesPodOperator
test_kpo_task = KubernetesPodOperator(
    task_id="test_kpo_task",
    name="test_kpo_task",
    namespace="default",
    image=image_name,
    cmds=["echo", "Hello, Airflow using KPO!"],
    dag=dag,
    get_logs=True
)

# Set dependencies and task sequence
test_kpo_task
