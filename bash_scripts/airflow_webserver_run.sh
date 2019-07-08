#!/bin/bash

source env/bin/activate
airflow webserver -p 8080
sleep 10
#run this in its own terminal, in virtualenv
#otherwise it eats up resources
