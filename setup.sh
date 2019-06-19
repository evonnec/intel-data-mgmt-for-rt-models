#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will set up your AWS EC2 instance for development for intel-data-mgmt-for-rt-models."
echo ""
echo ""

echo "First, a few commands to set up your environment"
echo ""
echo ""
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common awscli emacs25 bash
sudo apt install build-essential
sudo apt install cmdtest #yarn
ufw allow 3000
ufw allow 5000
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
echo "Cool, now we'll check if you have Node installed"
echo ""
echo ""

export HOME=`pwd`
export NVM_DIR=`pwd`/.nvm/
sudo passwd

node_installed=`which node`
if [ $node_installed ]
then
  echo "Great! You already have Node."
else
  echo "Ah, seems like Node is missing. Let's install it now!"
  cd ~
  curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh -o install_nvm.sh
fi
bash install_nvm.sh
source ~/.profile
nvm install 10.12
nvm use 10.12
npm i -g yarn
echo "Great! Now you have `node -v` installed"

postgres_installed=`which psql`
if [ $postgres_installed ]
then
  echo "Great! You already have Postgres."
else
  echo "Ah, seems like PostgresSQL is missing. Let's install it now!"
  cd ~
  sudo apt install postgresql postgresql-contrib
  sudo apt install python3-pip
  #emacs .pgpass

echo "Now that your environment is set up, we're going to clone a GitHub repository"
echo ""
echo ""
git clone https://github.com/evonnec/intel-data-mgmt-for-rt-models.git
echo ""
echo ""
