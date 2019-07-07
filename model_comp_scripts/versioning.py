#!/usr/bin/env python

#import psycopg2
#import boto3
#import sklearn
#from scipy import stats
import sqlalchemy
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
import csv
import matplotlib.pyplot as plt
import get_connected as gc

def use_gc_config():
    return gc.retrieve_config()
def use_gc():
    return gc.sqlalch_conn(use_gc_config)
def use_gc_psy():
    return gc.psycopg2_conn(use_gc_config)

conn = use_gc()
conn

def retrieve_prev_version():
    filepath_prev = 'version_previous.csv' #sys.argv[0]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    
    prev_version = []
    
    with open(filepath_prev, newline='\n', mode='r') as prev_version_input_file:
        prev_version_input_reader = csv.reader(prev_version_input_file, delimiter=',')
        for row in prev_version_input_reader:
            prev_ver_date_start = str(row[0])
            prev_ver_date_end = str(row[1])
            prev_ver_number = str(row[2])
            prev_version.append(prev_ver_date_start)
            prev_version.append(prev_ver_date_end)
            prev_version.append(prev_ver_number)
    prev_version_input_file.close()

    #print(config_dict)
    return prev_version

retrieve_prev_version()

def retrieve_version():
    filepath = 'versioning_input.csv' #sys.argv[0]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    
    version = []
    
    with open(filepath, newline='\n', mode='r') as versioning_input_file:
        versioning_input_reader = csv.reader(versioning_input_file, delimiter=',')
        for row in versioning_input_reader:
            version_date_start = str(row[0])
            version_date_end = str(row[1])
            version_number = str(row[2])
            version.append(version_date_start)
            version.append(version_date_end)
            version.append(version_number)
    versioning_input_file.close()

    #print(config_dict)
    return version

version_list = retrieve_version()

#to-do: using isnull is too subject to error, revise this
conn.execute("""UPDATE predictive_model SET version = '""" + version_list[2] + """' WHERE version isnull;""")

conn.dispose()

#write the versioned log
filepath = 'versioning_log.csv' #sys.argv[0]

if not os.path.isfile(filepath):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()
    
with open(filepath, newline='\n', mode='a') as versioning_export_file:
    versioning_output_writer = csv.writer(versioning_export_file, delimiter=',')
    versioning_output_writer = versioning_output_writer.writerow(version_list)
versioning_export_file.close()

