#!/usr/bin/env python

#function definition: this gathers a list of dependents
import get_connected as gc
import sqlalchemy
import csv
import sys
import os
import psycopg2
import pandas as pd
import numpy as np

def use_gc_config():
    return gc.retrieve_config() #retrieve conn config

def use_gc():
    return gc.sqlalch_conn(use_gc_config) #call sqlalch conn

def use_gc_psy():
    return gc.psycopg2_conn(use_gc_config) #call psycopg2 conn

dep_table_readin = 'dependents_table_name.csv' #to-do:sys.argv[0]
output_file = 'dependents_list.csv' #to-do:sys.argv[1]

if not os.path.isfile(dep_table_readin):
    print("File path {} does not exist. Exiting...".format(dep_table_readin))
    sys.exit()

#looks up the table name of dependents
with open(dep_table_readin, newline='\n', mode='r') as dep_table_file:
    dep_table = csv.reader(dep_table_file)
    for row in dep_table:
        dep_table_name = str(row[0])
dep_table_file.close()

#establish connection using function
conn = use_gc()
conn

#query list of dependents
dependents = pd.read_sql_query('''select distinct symbol as dep_sym from ''' + dep_table_name + ''' order by symbol asc;''', conn)
#write df to csv. to-do: perhaps change this to csv standard library
dependents.to_csv(output_file)

#close connection (to-do: ? not certain if this is all that is needed)
conn.dispose()
