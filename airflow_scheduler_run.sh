#!/bin/bash

source env/bin/activate
airflow scheduler
sleep 10
# in its own terminal, run scheduler also from a virtualenv
