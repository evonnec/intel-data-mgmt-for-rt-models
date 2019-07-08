#!/bin/bash

##if you choose not to do airflow set up script then bring up the docker version here
echo ""
echo ""
echo "let's retrieve docker for airflow by puckel on hub.docker.com and github"
echo ""
echo ""

cd $HOME
git clone https://www.github.com/puckel/docker-airflow.git

cd $HOME
cp -R intel-data-mgmt-for-rt-models/dags/ docker-airflow/

cd docker-airflow/

docker build --rm --build-arg AIRFLOW_DEPS="s3,postgres,ssh,python3,async,statsd" -t puckel/docker-airflow .
docker-compose -f docker-compose-LocalExecutor.yml up -d
docker run -d -p 8080:8080 -e LOAD_EX=n puckel/docker-airflow

echo "we're all done with retrieving docker for airflow by puckel"
