#!/usr/bin/env python
# coding: utf-8

# In[73]:


#function definition: this gathers a list of dependents
import get_connected as gc
import sqlalchemy
import csv
import sys
import os
import psycopg2
import pandas as pd
import numpy as np


# In[74]:


def use_gc_config():
    return gc.retrieve_config()


# In[75]:


def use_gc():
    return gc.sqlalch_conn(use_gc_config)


# In[76]:


def use_gc_psy():
    return gc.psycopg2_conn(use_gc_config)


# In[77]:


dep_table_readin = 'dependents_table_name.csv' #sys.argv[1]
output_file = 'dependents_list.csv' #sys.argv[2]
sql_readin = 'sqlalch_output.csv' #use_gc
psycopg2_readin = 'psycopg2_output.csv' #use_gc_psy
    
if not os.path.isfile(dep_table_readin):
    print("File path {} does not exist. Exiting...".format(dep_table_readin))
    sys.exit()
elif not os.path.isfile(sql_readin):
    print("File path {} does not exist. Exiting...".format(sql_readin))
    sys.exit()
elif not os.path.isfile(psycopg2_readin):
    print("File path {} does not exist. Exiting...".format(psycopg2_readin))
    sys.exit()
    
with open(dep_table_readin, newline='\n', mode='r') as dep_table_file:
    dep_table = csv.reader(dep_table_file)
    for row in dep_table:
        dep_table_name = str(row[0])   
dep_table_file.close()
    
print(dep_table_name)


# In[78]:


with open (sql_readin, newline='\n', mode='r') as read_in_file:
    postgres_var = csv.reader(read_in_file)
    for row in postgres_var:
        postgres_str = str(row[0])
read_in_file.close()

with open (psycopg2_readin, newline='\n', mode='r') as read_in_file:
    psycopg2_var = csv.reader(read_in_file)
    for row in psycopg2_var:
        psycopg2_str = str(row[0])
read_in_file.close()
    
    #return dep_table_name


# In[79]:


if __name__ == '__dep_main__':
    #get_connected.conn()
    dep_main()


# In[80]:


dep_main


# In[82]:


cnx = sqlalchemy.create_engine('postgresql://postgres:postgres@127.0.0.1:5432/postgres')

dependents = pd.read_sql_query('''select distinct symbol as dep_sym from ''' + dep_table_name + ''' order by symbol asc;''', cnx)
dependents.to_csv(output_file)

#print(dependents)


# In[83]:


#print(str(use_gc))
#cnx = create_engine(use_gc)
#cnx = create_engine(postgres_str)

    #connection_str = psycopg2_str
    #connector = psycopg2.connect(psycopg2_str)
    #cursor = connector.cursor()

    #cursor.execute('''select distinct symbol as dep_sym from ''' + dep_table_name + ''' order by symbol asc;''')
    #connector.commit()
    #cursor.close()
    #connector.close()

#dependents = pd.read_sql_query('''select distinct symbol as dep_sym from ''' + dep_table_name + ''' order by symbol asc;''', use_gc)
    #dependents.drop(dependents.columns[0], axis=1).to_csv(output_file)
#cnx.close
#dependents.to_csv(output_file)

    #with open (output_file, mode='w') as dep_list_file:
    #    output_file = csv.writer(dep_list_file)
    #    for dependent in dependents:
    #        line = ",".join([str(e) for e in dependent]) + "\n"
    #        dep_list_file.write(line)
    #dep_list_file.close()
    
#return dependents


# In[ ]:




