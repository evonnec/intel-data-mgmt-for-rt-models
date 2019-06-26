#!/usr/bin/env python
# coding: utf-8

# In[72]:


#function definition: this gathers a list of dependents
import get_connected
import sqlalchemy
import csv
import sys
import os
import psycopg2
#import pandas as pd


# In[73]:


def dep_main():
    filepath = 'dependents_table_name.csv' #sys.argv[1]
    output_file = 'dependents_list.csv' #sys.argv[2]
    
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    
    with open(filepath, newline='\n', mode='r') as dep_table_file:
        dep_table = csv.reader(dep_table_file)
        for row in dep_table:
            dep_table_name = str(row[0])
    
    dep_table_file.close()
    
    print(dep_table_name)
    
    connection_str = get_connected.conn(postgres_str)
    connector = psycopg2.connect(connection_str)
    cursor = connector.cursor()
    dependents = pd.read_sql_query('''select distinct symbol from ''' + dep_table_name + ''' order by symbol asc;''', cnx)
    
    return dependents
    
    with open (output_file, mode='w') as dep_list_file:
        output_file = csv.writer(dep_list_file)
        for dependent in dependents:
            dep_list_file.write(line)
    dep_list_file.close()
    


# In[74]:


if __name__ == '__dep_main__':
    get_connected.conn()
    dep_main()


# In[ ]:




