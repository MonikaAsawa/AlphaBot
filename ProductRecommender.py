# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:32:43 2018

@author: Monika Asawa
"""

import pandas as pd
import numpy as np

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

TOP_HOW_MANY = 3

def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

def generateRules():
    
    ordersDf = pd.read_csv('SuperStoreData.csv')
    
    'Focussing on Furniture Category only'
    ordersDf = ordersDf.loc[ordersDf['Category'] == 'Furniture']
    
    orders =  pd.DataFrame(ordersDf, columns=['Order ID','Product Name'])
    
    print("Shape of orders data : ", np.shape(orders))
    
    'Removing the records which doesnt have OrderID'
    orders.dropna(axis=0, subset=['Order ID'], inplace=True)
    
    basket = pd.crosstab(orders['Order ID'],orders['Product Name'])
    
    basket_sb = basket.applymap(encode_units)
    
    print("Shape of basket_sb data : ", np.shape(basket_sb))
    
    #----------------------------------------------------------------------
    
    'Generating frequent item sets that have a support of at least 0.1%'

    frequent_itemsets = apriori(basket_sb, min_support=0.00001, use_colnames=True)

    'Determining length of each itemset'
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    
    print("Shape of frequent_itemsets data : ", np.shape(frequent_itemsets))
    
    #----------------------------------------------------------------------

    'Generating the rules with their corresponding support, confidence and lift'
    
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    print("Shape of rules data : ", np.shape(rules))
    print("Printing top 5 rules generated", rules.head())
    
    'Creating new column to store value of consequents from frozen set format'
    rules['conse'] = [list(x) for x in rules.consequents]
    
    
    #----------------------------------------------------------------------
    'Lift should be minimum 6 and confidence should be 80%'
    rules = rules[ (rules['lift'] >= 6) & (rules['confidence'] >= 0.8)]
    
    'Converting lift(float) to lift(int)'
    rules['lift'] = rules['lift'].apply(lambda x: int(x))
    
    return rules

#----------------------------
rules = generateRules()
#----------------------------


def recommendProducts(selectedProducts):
    
    orderedProducts = frozenset((selectedProducts))
    
    'extracting rules which has selected products as antecedents'
    prodRules = rules[ rules['antecedents'] == orderedProducts ]
    
    print("Shape of prodRules data : ", np.shape(prodRules))
    print("Printing top 5 prodRules generated", prodRules.head())
    
    'sorting out product rules by lift, confidence and support'
    result = prodRules.sort_values(by=['lift', 'confidence','support'],axis=0, ascending=[0, 0, 0])
    
    print("Shape of result data : ", np.shape(result))
    print("Printing top 5 result generated", result.head())
    
    'Determing best 3 rules for the selected products'
    top_3_result = result[:TOP_HOW_MANY]
    
    conse = set()
    
    for i in top_3_result['conse']:
    
        print(i)
        
        for j in i:
            print(j)
            conse.add(j)
            
            if(len(conse)>=3):
                break
        
        if(len(conse)>=3):
            break
    
    return conse

