# Intelligent Data Management for Real-Time Models

Let's improve efficiency for real-time decision making by automating
the update of models as new data is piped in, specifically new data that
renders our existing model outputs obsolete.

Some examples:
- web network traffic
- weather data
- crime data
- stock data

This takes into account that the system running is ubuntu 18.04. This won't work for systems not ubuntu 18.04.

1. Edit file env_vars.sh with your variables
2. Run setup.sh to set up your environment
3. Run postgres_config.sh to set up your Postgres
4. At this point you can choose to continue as is, or to dump your Postgres contents in a .sql file and pull it into a Docker container. This choice will determine what you will choose with Airflow in step 5.
5. Choose whether you want to run Airflow natively or if you want to
set it up in a Docker container.
    - if you'd like to use a Docker container, run docker_for_airflow_by_puckel.sh
    - if you'd like to set up airflow natively, run airflow_run.sh
6. Please leave feedback after usage!
