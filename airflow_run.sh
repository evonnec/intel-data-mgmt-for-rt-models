#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will set up your airflow"
echo ""
echo ""

sudo apt install virtualenv
mkdir airflow
export AIRFLOW_HOME=`pwd`/airflow
cd airflow

sudo usermod -aG sudo ubuntu
source venv/bin/activate
pip install apache-airflow[all]
exit
source venv/bin/activate

sudo apt install python3-pip
sudo apt install python-pip

sudo usermod -aG sudo ubuntu

pip install apache-airflow[all]

#do this if you haven't set up a postgres table yet
echo "CREATE USER <user> PASSWORD '<db_pwd>'; CREATE DATABASE <db name>; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <user>;" | sudo -u postgres psql
sudo -u postgres sed -i "s|#listen_addresses = 'localhost'|listen_addresses = '*'|" /etc/postgresql/10/main/postgresql.conf
sudo -u postgres sed -i "s|127.0.0.1/32|0.0.0.0/0|" /etc/postgresql/10/main/pg_hba.conf
sudo -u postgres sed -i "s|::1/128|::/0|" /etc/postgresql/10/main/pg_hba.conf
service postgresql restart

# replace this in airflow.cfg change SequentialExecutor to LocalExecutor
# replace this in airflow.cfg $sql_alchemy_conn=postgresql+psycopg2://<user>:<pwd>@localhost:5432/<database_name>

pip install boto3

#must do these in virtualenv otherwise it won't work
airflow initdb
airflow webserver -p 8080
#airflow scheduler

echo ""
echo ""
echo ""
echo "We're done with setting up Airflow!"
