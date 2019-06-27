from airflow import DAG
from airflow.operators import DummyOperator, PythonOperator

default_args = {
    'owner': 'ubuntu',
    'start_date': datetime.utcnow(),
    'retry_delay': timedelta(minutes=5)
}
# Using the context manager allows you not to duplicate the dag parameter in each operator
with DAG('S3_dag_test', default_args=default_args, schedule_interval='@once') as dag:

    start_task = DummyOperator(
            task_id='dummy_start'
    )

    upload_to_S3_task = PythonOperator(
            task_id='upload_file_to_S3',
            python_callable=lambda _ : print("Uploading file to S3")
    )

    # Use arrows to set dependencies between tasks
start_task >> upload_to_S3_task
