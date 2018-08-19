# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 00:41:42 2018

@author: Monika Asawa
"""

import pandas as pd
import numpy as np

TOP_HOW_MANY = 3

#----------------------------
'Grab the data from last quarter only'
def provide_recent_quarter_data():
    
    ordersDf = pd.read_csv('SuperStoreData.csv', index_col = ['Order Date'], parse_dates = True)

    ordersDf = ordersDf.loc[ordersDf['Category'] == 'Furniture']

    ordersDf = ordersDf.sort_index()
    
    last_date = ordersDf.last_valid_index()
    
    from datetime import timedelta
    date_120_days_ago  = last_date - timedelta(days=120)
    
    recent_quarter_data = ordersDf.loc[date_120_days_ago : last_date]
    
    print("No of records in recent quarter", np.shape(recent_quarter_data))
    
    return recent_quarter_data

#----------------------------

'I want to find top 3 sub categories in Furniture Category'
def recommend_selling_prodCat():
    
    recent_quarter_data = provide_recent_quarter_data()
    
    sub_cat_freq = pd.DataFrame(recent_quarter_data.groupby('Sub-Category')['Quantity'].sum())
    
    sub_cat_freq = sub_cat_freq.sort_values(by="Quantity", ascending =False)
    
    top_3_sub_cat = sub_cat_freq[:TOP_HOW_MANY]
    
    response = ''
    for i in top_3_sub_cat.index.tolist():
        response += ", "+ i 
    response = response[1:]
    print(response)
    
    return response
#----------------------------
