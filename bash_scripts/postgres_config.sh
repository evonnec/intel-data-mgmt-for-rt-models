#!/bin/bash

#setup.sh sets up most of your postgres. now to load the tables with data
#set up Postgres tables and config files for intel-data-mgmt-for-rt-Models

#this is poor security practice, use hashicorp vault
aws configure
echo ""
echo ""
#take a look at s3 buckets and bring data from S3 to local
echo "--------------------------------------------"
echo ""
echo ""
echo "bring over data to local from S3 bucket"
aws s3 ls
aws s3 sync s3://{IMPORT_BUCKET_NAME} .

echo ""
echo ""
echo "--------------------------------------------"
echo ""
echo ""
echo "Load schemas of tables"
#load schemas of tables
psql -f schemas/schema_pred_template.sql -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${DB_NAME}
psql -f schemas/schema_dependents_template.sql -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${DB_NAME}
psql -f schemas/schema_curr_mapping.sql -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${DB_NAME}
psql -f schemas/schema_model_template.sql -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${DB_NAME}
psql -f schemas/schema_versioning_template.sql -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${DB_NAME}
psql -f schemas/schema_raw_data_template.sql -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${DB_NAME}

echo ""
echo ""
echo "--------------------------------------------"
echo ""
echo ""
echo "import data from S3 as csv into tables just created"
#import data as csv into tables just created
psql -p ${POSTGRES_PORT} -d ${DB_NAME} -U ${POSTGRES_USER} -c 'COPY public.raw_all_trades_dependents FROM STDIN with (format csv, header true, delimiter ",");' < dependents/data_formatted_master.csv
psql -p ${POSTGRES_PORT} -d ${DB_NAME} -U ${POSTGRES_USER} -c 'COPY public.raw_all_trades_predictors FROM STDIN with (format csv, header true, delimiter ",");' < predictors/predictors_master.csv

echo ""
echo ""
echo "--------------------------------------------"
echo ""
echo ""
echo "insert some pertinent predictor mapping into tables"
#insert some pertinent predictor mapping information into TABLES
psql -f schemas/predictor_insertions.sql -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${DB_NAME}
psql -U postgres
INSERT into raw_future_curr_mapping (symbol, currency) VALUES ('ESM9 Index', 'USD'), ('Z M9 Index', 'GBPUSD Curncy'), ('GXM9 Index', 'EURUSD Curncy'), ('VGM9 Index', 'EURUSD Curncy'), ('NHM9 Index', 'USDJPY Curncy'), ('SMM9 Index', 'USDCHF Curncy');
exit
echo ""
echo ""
echo "--------------------------------------------"
echo ""
echo ""
echo "now it's time to choose your airflow as local or in a docker container"
