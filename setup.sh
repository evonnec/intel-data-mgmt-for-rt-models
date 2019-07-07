#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will set up your AWS EC2 Ubuntu 18.04 instance for development for intel-data-mgmt-for-rt-models."
echo ""
echo ""

echo "First, a few commands to set up your environment"
echo ""
echo ""
sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common awscli emacs25 bash
sudo apt install build-essential
sudo apt install cmdtest #yarn
sudo ufw allow 5000
sudo ufw allow 8080
sudo ufw allow 5432
echo ""
echo ""
echo "--------------------------------------------"
echo ""
echo ""
echo "Run the file to export your environment variables"
env_vars.sh
echo ""
echo ""

echo "--------------------------------------------"
echo ""
echo ""

echo "Now, let's make sure you have Docker installed"
echo ""
echo ""

docker_installed=`which docker`

if [ $docker_installed ]
then
  echo "Great! You already have Docker. But! If it is old, run this and try again: $sudo apt-get remove docker docker-engine docker.io containerd runc "
  echo ""
else
  echo "Ah, seems like Docker is missing. Let's install it now!"
  echo ""
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
  #run this line instead when 18.04 bionic becomes outdated - $sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  sudo apt update
  sudo apt upgrade
  apt-cache policy docker-ce
  sudo apt install docker-ce docker-ce-cli containerd.io

  sudo systemctl status docker #check out the system status of docker
  sudo docker run hello-world #makes sure docker is working as expected
  sudo docker info #some information for you

  docker pull postgres:10.8 #get the postgres image you'll be using
  docker pull puckel/docker-airflow #this is if you decide to run the docker for airflow instead
  docker pull python:3.6.8-slim #get the python image compatible with airflow
  docker pull vault:latest #get the latest vault image
  docker pull bash:latest #get the latest bash image

  apt install docker-compose
fi

echo ""
echo ""
echo "--------------------------------------------"
echo ""
echo ""

#make a password for your current user if you haven't already
sudo passwd

echo ""
echo ""
echo "--------------------------------------------"
echo ""
echo ""

echo "Before your environment is set up, we're going to clone a GitHub repository"
echo ""
echo ""
git clone https://github.com/evonnec/intel-data-mgmt-for-rt-models.git
echo ""
echo ""

echo "--------------------------------------------"
echo ""
echo ""
echo "Now let's set up Postgres for the current user if it's not already set up"

postgres_installed=`which psql`
if [ $postgres_installed ]
then
  echo "Great! You already have Postgres."
else
  echo "Ah, seems like PostgresSQL is missing. Let's install it now!"
  cd ~
  sudo apt install postgresql postgresql-contrib
  sudo apt install python3-pip

  #create some users, permissions and the database
  echo "CREATE USER ${POSTGRES_USER} PASSWORD '${POSTGRES_PWD}'; CREATE DATABASE ${DB_NAME}; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${POSTGRES_USER};" | sudo -u postgres psql
  echo "CREATE USER airflow PASSWORD 'airflow'; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;" | sudo -u postgres psql

  #.pgpass set up is host:port:database_name:user:password
  sed -i 's//*:5432:${DB_NAME}:${POSTGRES_USER}:${POSTGRES_PWD}/g' .pgpass
  chmod 600 .pgpass #give permissions

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

  echo ""
  echo ""
  echo "--------------------------------------------"

  echo "let's run boto3_setup.sh"
  boto3_setup.sh

  echo ""
  echo ""
  echo "--------------------------------------------"
  echo ""
  echo ""
  echo "We're done with setup. Move next to postgres_config.sh to set up tables and schemas"
  echo ""
  echo ""
