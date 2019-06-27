#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will set up your airflow"
echo ""
echo ""

sudo apt install python3-pip

sudo apt install virtualenv

python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate

#alternative:
#pip3 install virtualenv
#sudo virtualenv -p python3 $HOME or sudo virtualenv -m python3 $HOME
#source $HOME/bin/activate

#setting up virtualenv
mkdir airflow
export HOME=`pwd`
export AIRFLOW_HOME=`pwd`/airflow
cd $AIRFLOW_HOME
#virtualenv -p `which python3` venv
#source venv/bin/activate

#alternative to setting up virtual env
#$mkdir env
#$cd env
#$virtualenv airflow
#$cd $HOME
#$source ~/env/airflow/bin/activate

deactivate
cd $HOME

sudo usermod -aG sudo ubuntu
pip install apache-airflow[postgres,async,statsd,s3,kubernetes,ssh,python3]
#don't use [all] as it doesn't work
#alternative is pipenv install apache-airflow[list_of_packages]

cd $AIRFLOW_HOME
#virtualenv -p `which python3` venv
#source venv/bin/activate
python3 -m venv env
source env/bin/activate

sudo apt-get install python3-venv
python3 -m venv ~/airflow

sudo apt-get install libpq-dev postgresql-client postgresql-client-common

pip3 install boto3
pip3 install psycopg2

cd env/
export HOME=`pwd`
export AIRFLOW_HOME=`pwd`/airflow
cd $AIRFLOW_HOME

#must run airflow in virtualenv otherwise it won't work long term. can interact
#without virtualenv but not recommended. log out and log back in.
#to ssh to the instance.

airflow initdb #this doesn't need to be in virtualenv

#now your airflow.cfg is created
cd $AIRFLOW_HOME
sed -i 's/executor = SequentialExecutor/executor = LocalExecutor/g' airflow.cfg
#replace
sed -i 's|sql_alchemy_conn = sqlite:////home/ubuntu/airflow/airflow.db|sql_alchemy_conn = postgresql+psycopg2://<user>:<password>@localhost:5432/<database_table>|g' airflow.cfg
sed -i 's/load_examples = True/load_examples = False/g' airflow.cfg
#ignore comments below unless you want to know what it is doing.
#cannot do the below command unless airflow creates these files.
#$cd $AIRFLOW_HOME
# replace executor in airflow.cfg : change SequentialExecutor to LocalExecutor
# replace sql_alchemy_conn in airflow.cfg $sql_alchemy_conn=postgresql+psycopg2://<user>:<pwd>@localhost:5432/<database_name>


mkdir ~/airflow/dags/
cp -R intel-data-mgmt-for-rt-models/DAGs/ airflow/dags/

#logging
sed -i 's/remote_logging = False/remote_logging = True/g' airflow.cfg
sed -i 's/remote_log_conn_id =/remote_log_conn_id=something/g' airflow.cfg
sed -i 's|remote_base_log_folder =|remote_base_log_folder = s3://logs-of-intel-data-model-airflow|g' airflow.cfg
sed -i 's|encrypt_s3_logs = False|encrypt_s3_logs = True|g' airflow.cfg
#time zone
sed -i 's|default_timezone = utc|default_timezone = American/New_York|g' airflow.cfg
#how powerful
sed -i 's|max_threads = 2|max_threads = 4|g' airflow.cfg
echo ""
echo ""
echo ""
echo "We're done with setting up Airflow!"
