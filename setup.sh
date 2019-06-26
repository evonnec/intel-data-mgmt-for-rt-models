#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will set up your AWS EC2 instance for development for intel-data-mgmt-for-rt-models."
echo ""
echo ""

echo "First, a few commands to set up your environment"
echo ""
echo ""
sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common awscli emacs25 bash
sudo apt install build-essential
sudo apt install cmdtest #yarn
sudo ufw allow 3000
sudo ufw allow 5000
sudo ufw allow 8080
sudo ufw allow 5432

echo ""
echo ""

echo "Now, let's make sure you have Docker installed"
echo ""
echo ""

docker_installed=`which docker`

if [ $docker_installed ]
then
  echo "Great! You already have Docker. If it is old, run this $sudo apt-get remove docker docker-engine docker.io containerd runc "
else
  echo "Ah, seems like Docker is missing. Let's install it now!"
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
  #sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  sudo apt update
  sudo apt upgrade
  apt-cache policy docker-ce
  sudo apt install docker-ce docker-ce-cli containerd.io
fi

sudo systemctl status docker #check out the system status of docker
sudo docker run hello-world #makes sure docker is working as expected
sudo docker info #some information for you
#docker image pull postgres:latest #get the latest postgres image
docker pull postgres:10.8
docker pull apache/airflow:latest-3.5-ci #get the latest airflow image
docker pull python:3.6.8-slim #get the latest python image
docker pull vault:latest #get the latest vault image
docker pull bash:latest #get the latest bash image

apt install docker-compose


echo ""
echo ""
echo ""
echo ""

sudo passwd

postgres_installed=`which psql`
if [ $postgres_installed ]
then
  echo "Great! You already have Postgres."
else
  echo "Ah, seems like PostgresSQL is missing. Let's install it now!"
  cd ~
  sudo apt install postgresql postgresql-contrib
  sudo apt install python3-pip

  echo "CREATE USER <user> PASSWORD '<db_pwd>'; CREATE DATABASE <db name>; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <user>;" | sudo -u postgres psql
  #.pgpass set up is host:port:database_name:user:password
  sed -i 's//*:5432:<database_name>:<user>:<pwd>/g' .pgpass
  chmod 600 .pgpass
  #change the config files
  sudo -u postgres sed -i "s|#listen_addresses = 'localhost'|listen_addresses = '*'|" /etc/postgresql/10/main/postgresql.conf
  sudo -u postgres sed -i "s|127.0.0.1/32|0.0.0.0/0|" /etc/postgresql/10/main/pg_hba.conf
  sudo -u postgres sed -i "s|::1/128|::/0|" /etc/postgresql/10/main/pg_hba.conf
  sudo -u postgres sed -i "s|    peer|    md5|g" /etc/postgresql/10/main/pg_hba.conf
  #restart postgresql
  service postgresql restart
  sudo -u postgres psql
  #in postgres now
  #postgres=#
  \du
  \password postgres
  \q
  sudo service postgresql reload
  sudo -u postgres psql
  \q


echo "Now that your environment is set up, we're going to clone a GitHub repository"
echo ""
echo ""
git clone https://github.com/evonnec/intel-data-mgmt-for-rt-models.git
echo ""
echo ""
