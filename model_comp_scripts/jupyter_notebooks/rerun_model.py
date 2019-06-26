#!/usr/bin/env python
# coding: utf-8

# In[150]:


#import psycopg2
#import boto3
import sqlalchemy
import pandas as pd
import numpy as np
#import sklearn
from datetime import datetime
#from scipy import stats
import sys
import os
import csv
import matplotlib.pyplot as plt
import get_connected as gc


# In[151]:


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


# In[165]:


dep_table_list = dep_table_list[1:]


# In[166]:


dep_table_list


# In[154]:


cnx = sqlalchemy.create_engine('postgresql://postgres:postgres@127.0.0.1:5432/postgres')


# In[175]:


for item in dep_table_list:
    
    dep_item = item
    if dep_item in dep_table_list:
        print(item)


# In[176]:


#conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='postgres'")
#cursor = conn.cursor()


# In[184]:


for item in dep_table_list:
    dep_item = item
    if dep_item in dep_table_list:
        data = pd.read_sql_query("""select * from (select date_time as dep_date_time, trade_price_open as dep_trade_price_open, trade_price_close as dep_trade_price_close, volume as dep_volume, symbol as dep_sym, predictor as dep_pred, industry from raw_all_trades_dependents) a LEFT JOIN (select date_time as pred_date_time, trade_price_open as pred_trade_price_open, trade_price_close as pred_trade_price_close, volume as pred_volume, symbol as pred_sym from raw_all_trades_predictors) b ON a.dep_pred = b.pred_sym and a.dep_date_time = b.pred_date_time where a.dep_sym = '""" + dep_item + """' and not b.pred_sym isnull order by a.dep_sym, a.dep_date_time asc;""", cnx)
        print(item)
        x = data['pred_trade_price_close'] #data[:][data.dep_sym == key]
        y = data['dep_trade_price_close']
        xmean = np.mean(x)
        ymean = np.mean(y)
        x = np.array(x).reshape(-1,1)
        y = np.array(y).reshape(-1,1)
        # plt.scatter(x,y); visual went here
        # Calculate the terms needed for the numator and denominator of beta
        xycov = (x - xmean) * (y - ymean)
        xvar = (x - xmean)**2
        beta = xycov.sum() / xvar.sum()
        alpha = ymean - (beta * xmean)
        ## Calculate beta and alpha
        #print(f'alpha = {alpha}')
        #print(f'beta = {beta}')
        #isolate one predictor from the table
        pred = data['pred_sym'][0]
        #make beta a string
        beta_str = str(float(beta))
        cnx.execute("""INSERT INTO predictive_model (symbol, predictor, beta) VALUES ('""" + dep_item + """', '""" + pred + """',  """ + beta_str + """)""")


# In[145]:


#cnx.execute("""INSERT INTO predictive_model (symbol, predictor, beta) VALUES ('""" + dep_item + """', '""" + pred + """',  """ + beta_str + """)""")
#    statement = predictive_model.insert().values(symbol=dep_item, predictor=pred, beta=beta)  
#    cnx.execute(statement) 


# In[ ]:


#sym_dict = {elem: data for elem in dependents}
#dependents = data.dep_sym.unique()
#
#for key in sym_dict.keys():
#    sym_dict[key] = data[:][data.dep_sym == key]


# In[71]:


#from sklearn.linear_model import LinearRegression #import the regression called "LinearRegression"


# In[ ]:


#lr = LinearRegression() # Initialize the model


# In[ ]:


#lr.fit(x,y) # "Fit" the model, which means "I want you to learn from my data!"


# In[ ]:


#new_x = np.array([7,8,9]).reshape(-1,1)
#predicted_y = lr.predict(new_x) # Predict for new data!
#print(predicted_y)

