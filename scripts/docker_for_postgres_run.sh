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
