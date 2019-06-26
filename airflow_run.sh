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

#ignore comments below unless you want to know what it is doing.
#cannot do the below command unless airflow creates these files.
#$cd $AIRFLOW_HOME
# replace executor in airflow.cfg : change SequentialExecutor to LocalExecutor
# replace sql_alchemy_conn in airflow.cfg $sql_alchemy_conn=postgresql+psycopg2://<user>:<pwd>@localhost:5432/<database_name>

echo ""
echo ""
echo ""
echo "We're done with setting up Airflow!"
