#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


def use_gc_config():
    return gc.retrieve_config()
def use_gc():
    return gc.sqlalch_conn(use_gc_config)
def use_gc_psy():
    return gc.psycopg2_conn(use_gc_config)


# In[3]:


conn = use_gc()
conn


# In[35]:


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


# In[36]:


version_list = retrieve_version()


# In[38]:


#to-do: using isnull is too subject to error, revise this
conn.execute("""UPDATE predictive_model SET version = '""" + version_list[2] + """' WHERE version isnull;""")
       


# In[39]:


conn.dispose()


# In[43]:


#write the versioned log
filepath = 'versioning_log.csv' #sys.argv[0]

if not os.path.isfile(filepath):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()
    
with open(filepath, newline='\n', mode='a') as versioning_export_file:
    versioning_output_writer = csv.writer(versioning_export_file, delimiter=',')
    versioning_output_writer = versioning_output_writer.writerow(version_list)
versioning_export_file.close()

