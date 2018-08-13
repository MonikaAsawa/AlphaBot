# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 18:52:07 2018

@author: Monika Asawa
"""

from DialogFlow import create_entity_type
from Product import loadProducts

def setUpApp():
    
    print("setUpApp in AppInit starts")

    ProductsEn = loadProducts()
    productCategories = ProductsEn.keys()
    
    print("Number of productCategories to be loaded",len(productCategories))
    
    #set up entity types
    for productType in productCategories:
        print(productType)
        create_entity_type("alphabotagent",productType,productType)
        
    #set up entity values in bulk

    print("setUpApp in AppInit ends")