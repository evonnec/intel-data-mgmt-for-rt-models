#!/bin/bash
echo "--------------------------------------------"

#this is for after postgres is set up, pg_dump contents into a docker container
echo "Hey there! This script will run your postgres docker image for intel-data-mgmt-for-rt-models in a container."
echo ""
echo ""

#not finished
docker run -it postgres:10.8 &

echo ""
echo ""
echo ""
#psql postgres service restart
cd $HOME
pg_dumpall > backup.sql
#if not at home, copy this to home
#sudo cp backup.sql ~/.
#listen_addresses for postgres config should be adjusted to * this is done in setup.sh already

sudo systemctl enable postgresql
sudo systemctl start postgresql

#ifconfig docker0
# this is to be updated if pg_hba.conf is not listening to all
# mapping to docker container is needed

sudo systemctl restart postgresql
#running the airflow app in docker, not needed in other script
#docker run -d --add-host=database:{HOST_ADDRESS} --name docker-airflow airflow_container
#docker exec -it airflow_container ping database
#docker exec -it airflow_container ip addr show eth0

#get backup and put into container
docker run -d -v `pwd`:/backup/ --name pg_container postgres
docker exec -it pg_container bash
cd backup
psql -U postgres -f backup.sql postgres
exit

#link postgres container to airflow container
docker run -d --name airflow_container --link=pg_container:database docker-airflow

#check the containers are connected
docker exec -it airflow_container cat /etc/hosts
