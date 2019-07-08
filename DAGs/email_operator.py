import airflow
from airflow import DAG
from datetime import datetime, timedelta
#from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
#from airflow.operators.bash_operator import BashOperator
#from airflow.models import Variable
#import json
from airflow.operators.email_operator import EmailOperator
#import snakebite.client
#from google.protobuf import descriptor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 6, 6),
    'email': ['evo@intelligent-data-modeling.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('EmailOperator-Test', default_args=default_args, catchup=False)

send_email = EmailOperator(
    task_id='send_email',
    to='evo@intelligent-data-modeling.com',
    subject='stakeholders test email',
    html_content="BODY OF EMAIL: model failures/successes",
    dag=dag
) #send emails with logging metrics
