# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 18:52:07 2018

@author: Monika Asawa
"""

from DialogFlow import create_entity_type,delete_all_existing_entities,create_productNames
from SuperStore_Product import loadProductCat
from google.api_core.exceptions import ResourceExhausted

def setUpApp():
    
    print("setUpApp in AppInit starts")

    try:
        
        '1) Delete Existing Entities'
        #delete_all_existing_entities()
        #print("Existing entities deleted")
        
        
        
        '2) Load Product Entity Type'
        #productCategories = loadProductCat()
        #print("Number of productCategories to be loaded",len(productCategories))
    
        #for productType in productCategories:
        #    print(productType)
        #   create_entity_type(productType,productType)
        
        '3) Load Product Entity Type'
    
        productCategories = loadProductCat()
        
        create_productNames(productCategories)
        
        
    except ResourceExhausted:
        print("Either out of resource quota or reaching rate limiting. The client should look for google.rpc.QuotaFailure error detail for more information.")
        
    #set up entity values in bulk

    print("setUpApp in AppInit ends")

    