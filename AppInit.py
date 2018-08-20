# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 18:52:07 2018

@author: Monika Asawa
"""

from DialogFlow import createEntities,delete_all_existing_entities,create_productNames
from SuperStore_Product import loadProductCat
from google.api_core.exceptions import ResourceExhausted
import time

def setUpApp():
    
    print("setUpApp in AppInit starts")

    try:
        
        '1) Delete Existing Entities'
        #delete_all_existing_entities()
        #print("Existing entities deleted")
        
        #Wait for 60 seconds
        #print("Going for sleep for 45 seconds")
        #time.sleep(45)
  
        '2) Load Product Entity Type'
        #productCategories = loadProductCat()
        #createEntities(productCategories)
        
        #Wait for 60 seconds
        #print("Going for sleep for 45 seconds")
        #time.sleep(45)
        
        '3) Load Product Entity Type'
    
        productCategories = loadProductCat()
        create_productNames(productCategories)
        
        
    except ResourceExhausted:
        print("Either out of resource quota or reaching rate limiting. The client should look for google.rpc.QuotaFailure error detail for more information.")
        
    #set up entity values in bulk

    print("setUpApp in AppInit ends")

    