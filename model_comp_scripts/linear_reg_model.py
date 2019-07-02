#!/usr/bin/env python
# coding: utf-8

# In[144]:


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


# In[166]:


dep_table_readin = 'dependents_list.csv' #sys.argv[0]

if not os.path.isfile(dep_table_readin):
    print("File path {} does not exist. Exiting...".format(filepath))
    sys.exit()
    
with open(dep_table_readin, newline='\n', mode='r') as dep_table_file:
    dep_table = csv.reader(dep_table_file, delimiter=',')
    dep_table_list = []
    for row in dep_table:
        dep_table_list_item = str(row[1])
        if dep_table_list_item not in dep_table_list:
            dep_table_list.append(dep_table_list_item)
dep_table_file.close()


# In[167]:


#omit the index and use only the list of symbols
dep_table_list = dep_table_list[1:]


# In[159]:


def use_gc_config():
    return gc.retrieve_config()
def use_gc():
    return gc.sqlalch_conn(use_gc_config)
def use_gc_psy():
    return gc.psycopg2_conn(use_gc_config)
def use_ver():
    return ver.retrieve_version()


# In[160]:


conn = use_gc()
conn
version = use_ver()
version


# In[161]:


#version_start_datetime = datetime.strptime(version[0], "%Y-%m-%d %H:%M:%S")
#version_end_datetime = datetime.strptime(version[1], "%Y-%m-%d %H:%M:%S")


# In[164]:


for item in dep_table_list:
    #for each depdendent
    
    dep_item = item
    if dep_item in dep_table_list:
    #if dependent in list    
        
        predictor = pd.read_sql_query("""select distinct predictor from raw_all_trades_dependents where symbol =  '""" + dep_item + """';""", conn)
        pred = predictor['predictor'].iloc[0]
        index_with_curr = pd.read_sql_query("""select symbol from raw_future_curr_mapping where symbol <> 'ESM9 Index';""", conn)
        #to determine if predictor needs a currency or not
        
        if pred in index_with_curr:
            #if predictor needs a currency
            data = pd.read_sql_query("""select * from (select date_time as dep_date_time, trade_price_open as dep_trade_price_open, trade_price_close as dep_trade_price_close, volume as dep_volume, symbol as dep_sym, predictor as dep_pred, industry from raw_all_trades_dependents) a LEFT JOIN (select pred_date_time, pred_trade_price_open, pred_trade_price_close, pred_sym,currency, curr_pred_trade_price_open, curr_pred_trade_price_close from vw_all_predictors_with_currencies) b ON a.dep_pred = b.pred_sym and a.dep_date_time = b.pred_date_time where a.dep_sym = '""" + dep_item + """' and not b.pred_sym isnull and a.dep_date_time between '""" + version[0] +"""'::timestamp and '""" + version[1] + """'::timestamp order by a.dep_sym, a.dep_date_time asc;""", conn)
            #use this df
            
            if data['currency'][0] == 'EURUSD Curncy' or data['currency'][0] == 'GBPUSD Curncy' or data['currency'][0] == 'AUDUSD Curncy':
                x = np.multiply(data['pred_trade_price_close'], data['curr_pred_trade_price_close']) #data[:][data.dep_sym == key]
                y = data['dep_trade_price_close']
            else:
                x = np.divide(data['pred_trade_price_close'], data['curr_pred_trade_price_close']) #data[:][data.dep_sym == key]
                y = data['dep_trade_price_close']
            #account for differences in how to calculate for currencies and assign matrices x and y
            
        else:
            data = pd.read_sql_query("""select * from (select date_time as dep_date_time, trade_price_open as dep_trade_price_open, trade_price_close as dep_trade_price_close, volume as dep_volume, symbol as dep_sym, predictor as dep_pred, industry from raw_all_trades_dependents) a LEFT JOIN (select date_time as pred_date_time, trade_price_open as pred_trade_price_open, trade_price_close as pred_trade_price_close, volume as pred_volume, symbol as pred_sym from raw_all_trades_predictors) b ON a.dep_pred = b.pred_sym and a.dep_date_time = b.pred_date_time where a.dep_sym = '""" + dep_item + """' and not b.pred_sym isnull and a.dep_date_time between '""" + version[0] + """' and '""" + version[1] + """' order by a.dep_sym, a.dep_date_time asc;""", conn)
            #if predictor does not need a currency
            x = data['pred_trade_price_close']
            y = data['dep_trade_price_close']
        
        xmean = np.mean(x)
        ymean = np.mean(y)
        
        # Calculate the terms needed for the numator and denominator of beta
        xycov = np.multiply((x - xmean), (y - ymean))
        xvar = np.power((x - xmean), 2)
        beta = xycov.sum() / xvar.sum()
        alpha = ymean - (beta * xmean)

        #isolate one predictor from the table
        pred = data['pred_sym'][0]
        
        #make beta a string
        beta_str = str(beta)
        
        #insert model output without version or flag
        conn.execute("""INSERT INTO predictive_model (symbol, predictor, beta) VALUES ('""" + dep_item + """', '""" + pred + """',  """ + beta_str + """)""")


# In[165]:


conn.dispose()


# In[ ]:


#lr = LinearRegression() # Initialize the model


# In[ ]:


#lr.fit(x,y) # Fit the model


# In[ ]:


#new_x = np.array([7,8,9]).reshape(-1,1)
#predicted_y = lr.predict(new_x) # Predict for new data
#print(predicted_y)

