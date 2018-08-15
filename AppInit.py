# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 18:52:07 2018

@author: Monika Asawa
"""

from DialogFlow import create_entity_type,list_entity_types,delete_all_existing_entities
from Product import loadProducts

def setUpApp():
    
    print("setUpApp in AppInit starts")

    delete_all_existing_entities()
    print("Existing entities deleted")
    
    ProductsEn = loadProducts()
    productCategories = ProductsEn.keys()
    
    print("Number of productCategories to be loaded",len(productCategories))
    
    #set up entity types
    for productType in productCategories:
        print(productType)
        create_entity_type(productType,productType)
        
    #set up entity values in bulk

    print("setUpApp in AppInit ends")