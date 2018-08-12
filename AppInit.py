# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 18:52:07 2018

@author: Monika Asawa
"""

from DialogFlow import create_entity_type
from Product import loadProductCategories

def setUpApp():

    productCategories = loadProductCategories()
    
    #set up entity types
    for productType in productCategories:
        create_entity_type("alphabotagent",productType,productType)
        
    #set up entity values in bulk