"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

#CR to-do: abstract away default args
default_args = {
    'owner': 'ubuntu',
    'depends_on_past': False,
    'start_date': datetime(2019, 6, 6),
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

#CR to-do: abstract away
dag = DAG(
    'run_schedule', default_args=default_args, schedule_interval=timedelta(days=0))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='init_connection',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/model_comp_scripts/get_connected.py ', #psql copy data from new data to data versioned
    dag=dag)

t2 = BashOperator(
    task_id='retrieve_dependents_from_table_name_takes_in_version',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/model_comp_scripts/list_dependents.py ', #psql copy data from new data to data versioned
    dag=dag)

#choose a model based on fitting new data on a few existing models here in t3.5.
# i.e. linear regression multi factor, logistic regression, etc.

t3 = BashOperator(
    task_id='retrains_model_on_new_data_date_range_pushes_to_db_table',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/model_comp_scripts/linear_reg_model.py ', #re-run model
    dag=dag)

t4 = BashOperator(
    task_id='take_the_model_output_and_version_it_in_appropriate_tables_taking_in_configs_and_pushing_logs',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/model_comp_scripts/versioning.py ', #version
    dag=dag)

t5 = BashOperator(
    task_id='tests_model_output_and_passes_pass_or_fail_flags_to_output_table_column',
    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/model_comp_scripts/tests_and_checks.py ', #tests and checks
    dag=dag)

#t6 = BashOperator(
#    task_id='prod_table_is_generated_and_new_version_is_updated_next_model_is_specified',
#    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/model_comp_scripts/compile_model_prod.py ', #compile successful models for production
#    dag=dag)

#t7 = BashOperator(
#    task_id='push_output_and_logs_to_s3_takes_in_s3_bucket_name',
#    bash_command='python3 /home/ubuntu/intel-data-mgmt-for-rt-models/model_comp_scripts/upload_logs_to_s3.py ', #uploads to s3
#    dag=dag)

# Chaining multiple dependencies becomes
# concise with the bit shift operator:
t1 >> t2 >> t3 >> t4 >> t5 #>> t6 >> t7
