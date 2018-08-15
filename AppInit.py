# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 18:52:07 2018

@author: Monika Asawa
"""

from DialogFlow import create_entity_type,delete_all_existing_entities
from Product import loadProducts
from google.api_core.exceptions import ResourceExhausted

def setUpApp():
    
    print("setUpApp in AppInit starts")

    try:
        
        delete_all_existing_entities()
        print("Existing entities deleted")
        
        ProductsEn = loadProducts()
        productCategories = ProductsEn.keys()
        
        print("Number of productCategories to be loaded",len(productCategories))
        
        #set up entity types
        for productType in productCategories:
            print(productType)
            create_entity_type(productType,productType)
        
    except ResourceExhausted:
        print("Either out of resource quota or reaching rate limiting. The client should look for google.rpc.QuotaFailure error detail for more information.")
        
    #set up entity values in bulk

    print("setUpApp in AppInit ends")