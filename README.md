# Intelligent Data Management for Real-Time Models

Let's improve efficiency for real-time decision making by automating
the update of models as new data is piped in, specifically new data that
renders our existing model outputs obsolete.

Some examples:
- web network traffic
- weather data
- crime data
- stock data

First, an event trigger or computation trigger is activated in our scheduler,
Airflow. An Airflow DAG is initiated.

This Airflow DAG runs first task 1 which sends instructions for a python script to run.
This python script recomputes betas of models with the new dataset, saves these outputs to a versioned table.

The Airflow DAG then runs task 2, Circle CI unit tests the newly versioned dataset
and model output to make sure there are no issues.

The Airflow DAG then runs task 3, a statistical unit test will be run to make sure
that data and the model make sense (i.e. validation test et al).

Fourth, Airflow DAG task 4 will tag the datasets and model outputs that pass the
tests and checks, these get pushed in Airflow DAG task 5 to a versioned table
in the database and also become the model output that is used in production.

If the dataset and new model do not pass the tests and checks, production models
and datasets fall back or continue to use the last existing and working model
and dataset, and any failed new dataset or model outputs are pushed to a table
with a fail flag and appropriate teams are notified.

All models in production explicitly state the version of the model that is used.

If this goes as planned, we'll have monitoring and logging. We will also have
Airflow deliver latency, scale metrics, diffs of existing and new model outputs,
among other suggested features.
