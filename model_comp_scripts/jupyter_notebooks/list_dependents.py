#!/usr/bin/env python
# coding: utf-8

# In[36]:


#function definition: this gathers a list of dependents
import get_connected as gc
import sqlalchemy
import csv
import sys
import os
import psycopg2
import pandas as pd
import numpy as np


# In[37]:


def use_gc_config():
    return gc.retrieve_config() #retrieve conn config


# In[38]:


def use_gc():
    return gc.sqlalch_conn(use_gc_config) #call sqlalch conn


# In[39]:


def use_gc_psy():
    return gc.psycopg2_conn(use_gc_config) #call psycopg2 conn


# In[40]:


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


# In[41]:


#to-do: delete or use - to ultimately bring in strings as connections
#with open (sql_readin, newline='\n', mode='r') as read_in_file:
#    postgres_var = csv.reader(read_in_file)
#    for row in postgres_var:
#        postgres_str = str(row[0])
#read_in_file.close()
#
#with open (psycopg2_readin, newline='\n', mode='r') as read_in_file:
#    psycopg2_var = csv.reader(read_in_file)
#    for row in psycopg2_var:
#        psycopg2_str = str(row[0])
#read_in_file.close()


# In[42]:


#establish connection using function
conn = use_gc()


# In[43]:


conn


# In[44]:


#query list of dependents
dependents = pd.read_sql_query('''select distinct symbol as dep_sym from ''' + dep_table_name + ''' order by symbol asc;''', conn)
#write df to csv. to-do: perhaps change this to csv standard library
dependents.to_csv(output_file)


# In[45]:


#close connection (to-do: ? not certain if this is all that is needed)
conn.dispose()

