#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will set up your airflow"
echo ""
echo ""

sudo apt install python3-pip
sudo apt install python-pip

sudo apt install virtualenv

#setting up virtualenv
mkdir airflow
export HOME=`pwd`
export AIRFLOW_HOME=`pwd`/airflow
cd $AIRFLOW_HOME
virtualenv -p `which python3` venv
source venv/bin/activate

#alternative to setting up virtual env
#$mkdir env
#$cd env
#$virtualenv airflow
#$cd $HOME
#$source ~/env/airflow/bin/activate

deactivate
cd $HOME

sudo usermod -aG sudo ubuntu
pip install apache-airflow[all]

cd $AIRFLOW_HOME
virtualenv -p `which python3` venv
source venv/bin/activate

pip install boto3

cd env/
export HOME=`pwd`
export AIRFLOW_HOME=`pwd`/airflow
cd $AIRFLOW_HOME

#must run airflow in virtualenv otherwise it won't work. can interact
#without virtualenv but not recommended. log out and log back in
#to ssh to the instance.

airflow initdb #this doesn't need to be in virtualenv

#cannot do the below command unless airflow creates these files.
#$cd $AIRFLOW_HOME
# replace executor in airflow.cfg : change SequentialExecutor to LocalExecutor
# replace sql_alchemy_conn in airflow.cfg $sql_alchemy_conn=postgresql+psycopg2://<user>:<pwd>@localhost:5432/<database_name>


airflow webserver -p 8080 #run this in its own terminal, preferably in virtualenv
#otherwise it eats up resources
# in its own terminal, run $airflow scheduler, also from a virtualenv

echo ""
echo ""
echo ""
echo "We're done with setting up Airflow!"
