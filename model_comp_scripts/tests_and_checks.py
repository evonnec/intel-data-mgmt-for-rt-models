#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
import versioning as ver


# In[133]:


def use_ver():
    return ver.retrieve_version()
def use_gc_config():
    return gc.retrieve_config()
def use_gc():
    return gc.sqlalch_conn(use_gc_config)
def use_gc_psy():
    return gc.psycopg2_conn(use_gc_config)

version = use_ver()
version
conn = use_gc()
conn


# In[12]:


model_table_readin = 'models_table_name.csv' #to-do:sys.argv[0]
    
if not os.path.isfile(model_table_readin):
    print("File path {} does not exist. Exiting...".format(model_table_readin))
    sys.exit()

#looks up the table name of model table name
with open(model_table_readin, newline='\n', mode='r') as model_table_file:
    model_table = csv.reader(model_table_file)
    for row in model_table:
        model_table_name = str(row[0])
model_table_file.close()


# In[125]:


#take in all columns of the versioned database table data
models = pd.read_sql_query("""select * from """ + model_table_name + """ where version = '""" + version[2] + """' order by symbol asc;""", conn)


# In[127]:


#define new df for def check()
beta_models = models['beta']


# In[128]:


#simple (not-real) statistical measure evaluation flag
def check():
    
    flag = ['pass' if float(beta) < float(abs(3)) else 'fail' for beta in beta_models] 
    return flag


# In[129]:


#add a flag using the def check()
models['flag'] = check()


# In[139]:


#to-do: improve the process of tests and checks
#delete incomplete table entry for the current version
conn.execute("""DELETE from predictive_model WHERE version = '""" + version[2] + """';""")


# In[148]:


#update the dataframe and drop the numbered index
models.set_index('symbol', inplace=True)


# In[149]:


#write the dataframe to the table and append
models.to_sql(model_table_name, conn, if_exists='append')


# In[150]:


conn.dispose()

