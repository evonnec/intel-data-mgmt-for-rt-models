#!/usr/bin/env python
# coding: utf-8

# In[1]:


#function definition: this calls the sql connection
import csv
import sys
import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# In[3]:


#retrieves postgres config
def retrieve_config():
    filepath = 'postgres_config.csv' #sys.argv[0]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    
    config_dict = {}
    
    with open(filepath, newline='\n', mode='r') as postgres_config_file:
        config_reader = csv.reader(postgres_config_file, delimiter=',')
        for row in config_reader:
            var_name = str(row[0])
            var_value = str(row[1])
            if var_name not in config_dict:
                config_dict.update({var_name: var_value})
    postgres_config_file.close()

    #print(config_dict)
    return config_dict


# In[4]:


#connects to sql alchemy with engine
def sqlalch_conn(dict_config):
    filepath = 'postgres_config.csv' #to-do:sys.argv[0]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    
    config_dict = {} #make the contents of the config file a dictionary
    
    #load the dict with the config stored in csv
    with open(filepath, newline='\n', mode='r') as postgres_config_file:
        config_reader = csv.reader(postgres_config_file, delimiter=',')
        for row in config_reader:
            var_name = str(row[0])
            var_value = str(row[1])
            if var_name not in config_dict:
                config_dict.update({var_name: var_value})
    postgres_config_file.close()
    
    sqlalch_output = 'sqlalch_output.csv' #to-do:sys.argv[1]
    
    retrieve_config()
    
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'
                .format(username=config_dict.get('POSTGRES_USERNAME'),
                        password=config_dict.get('POSTGRES_PASSWORD'),
                        ipaddress=config_dict.get('POSTGRES_ADDRESS'),
                        port=config_dict.get('POSTGRES_PORT'),
                        dbname=config_dict.get('POSTGRES_DBNAME')))
    #print(postgres_str)
    
    #to check what the output was
    with open (sqlalch_output, mode='w') as sqlalch_conn_file:
        sqlalch_output = csv.writer(sqlalch_conn_file)
        sqlalch_conn_file.write(postgres_str)
    sqlalch_conn_file.close()

    #create connection to db
    cnx = create_engine(postgres_str)
    return cnx


# In[6]:


#sqlalch_conn(retrieve_config)


# In[7]:


#same notes as sqlalch_ def above. to-do:delete repeat config dict and configure it as its own def
def psycopg2_conn(dict_config):
    filepath = 'postgres_config.csv' #to-do:sys.argv[0]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    
    config_dict = {}
    
    with open(filepath, newline='\n', mode='r') as postgres_config_file:
        config_reader = csv.reader(postgres_config_file, delimiter=',')
        for row in config_reader:
            var_name = str(row[0])
            var_value = str(row[1])
            if var_name not in config_dict:
                config_dict.update({var_name: var_value})
    postgres_config_file.close()
    psycopg2_output = 'psycopg2_output.csv' #to-do:sys.argv[1]
    
    psycopg2_str = ("dbname='{dbname}' user='{username}' host='{ipaddress}' password='{password}'"
                .format(username=config_dict.get('POSTGRES_USERNAME'),
                        password=config_dict.get('POSTGRES_PASSWORD'),
                        ipaddress=config_dict.get('POSTGRES_ADDRESS'),
                        port=config_dict.get('POSTGRES_PORT'),
                        dbname=config_dict.get('POSTGRES_DBNAME')))
    #print(psycopg2_str)
        
    with open (psycopg2_output, mode='w') as psycopg2_conn_file:
        psycopg2_output = csv.writer(psycopg2_conn_file)
        psycopg2_conn_file.write(psycopg2_str)
    psycopg2_conn_file.close()
    
    conn = psycopg2.connect(psycopg2_str)
    
    return conn


# In[8]:


#psycopg2_conn(retrieve_config)


# In[2]:


#to-do CR: use env_file 
#user = os.environ['POSTGRES_USERNAME']
#pwd = os.environ['POSTGRES_PASSWORD']
#db = os.environ['POSTGRES_DBNAME']
#host = os.environ['POSTGRES_ADDRESS']
#port = os.environ['POSTGRES_PORT']
#engine = create_engine('postgresql://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))

