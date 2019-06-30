"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ubuntu',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['evo@intelligent-data-modeling.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'sched', default_args=default_args, schedule_interval=timedelta(days=1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='init_connection',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/get_connected.py ', #psql copy data from new data to data versioned
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5', #run python script to calculate model
    retries=3,
    dag=dag)

#templated_command = """
#    {% for i in range(5) %}
#        echo "{{ ds }}"
#        echo "{{ macros.ds_add(ds, 7)}}"
#        echo "{{ params.my_param }}"
#    {% endfor %}
#"""

#t3 = BashOperator(
#    task_id='templated',
#    bash_command=templated_command, #very interesting! run results against unit tests and give flag passing or failure
#    params={'my_param': 'Parameter I passed in'},
#    dag=dag)

t3 = BashOperator(
    task_id='retrieve_dependents_from_table_name_takes_in_version',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/list_dependents.py ', #psql copy data from new data to data versioned
    dag=dag)

#choose a model based on fitting new data on a few existing models here in t3.5.
# i.e. linear regression multi factor, logistic regression, etc.

t4 = BashOperator(
    task_id='retrains_model',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/linear_reg_model.py ', #compile successful models for production, send emails with logging metrics
    dag=dag)

t5 = BashOperator(
    task_id='tests_model_output_and_passes_pass_or_fail_flags_to_output_table_column',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/test_model.py ', #compile successful models for production, send emails with logging metrics
    dag=dag)

t6 = BashOperator(
    task_id='prod_table_is_generated_and_new_version_is_updated_next_model_is_specified',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/prod_model_versioning.py ', #compile successful models for production, send emails with logging metrics
    dag=dag)

t7 = BashOperator(
    task_id='push_output_and_logs_to_s3_takes_in_s3_bucket_name',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/upload_logs_to_s3.py ', #compile successful models for production, send emails with logging metrics
    dag=dag)

#t2.set_upstream(t1)
#t3.set_upstream(t1)

###

#t1.set_downstream(t2)

# This means that t2 will depend on t1
# running successfully to run.
# It is equivalent to:
#t2.set_upstream(t1)

# The bit shift operator can also be
# used to chain operations:
#t1 >> t2

# And the upstream dependency with the
# bit shift operator:
#t2 << t1

# Chaining multiple dependencies becomes
# concise with the bit shift operator:
t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7

# A list of tasks can also be set as
# dependencies. These operations
# all have the same effect:
#t1.set_downstream([t2, t3])
#t1 >> [t2, t3]
#[t2, t3] << t1
