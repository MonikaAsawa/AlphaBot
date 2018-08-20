# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 16:04:14 2018

@author: Monika Asawa
"""

import dialogflow_v2 as dialogflow
import re
from random import randint
import google.api_core.exceptions as GError
from google.api_core.exceptions import NotFound, InvalidArgument, FailedPrecondition, ResourceExhausted
import time

from SuperStore_Product import loadProductNames

project_id="alphabotagent"

entity_types_client = dialogflow.EntityTypesClient()

#Entity name may contain only the following: A-Z, a-z, 0-9, _ (underscore), - (dash). 
#And it should start with a letter."

def entity_name_validate_n_update(entityName):
    
    print("entity_name_validate_n_update method started")
    
    if re.search(r"(\s)+",entityName):
        print("Validation failed: Contains space")
        return "entityName_" + str(randint(100, 999))
    else:
        return entityName

    print("entity_name_validate_n_update method ended")
          
# Helper to get entity_type_id from display name.
def _get_entity_type_ids(display_name):
    
    print("_get_entity_type_ids method started")
    
    parent = entity_types_client.project_agent_path(project_id)
        
    entity_types = entity_types_client.list_entity_types(parent)
    entity_type_names = [
        entity_type.name for entity_type in entity_types
        if entity_type.display_name == display_name]

    entity_type_ids = [
        entity_type_name.split('/')[-1] for entity_type_name
        in entity_type_names]
    
    print("_get_entity_type_ids method ended")

    return entity_type_ids

def delete_entity_type(entity_type_id):
    """Delete entity type with the given entity type name."""

    print("delete_entity_type method started")
    
    try:
        entity_type_path = entity_types_client.entity_type_path(
            project_id, entity_type_id)
    
        entity_types_client.delete_entity_type(entity_type_path)
    
    except (dialogflow.api_core.exceptions) as error:
        return error

    print("delete_entity_type method ended")
        
def create_entity_type(display_name, kind):
    """Create an entity type with the given display name."""

    print("create_entity_type method started")
    
    kind = 'KIND_MAP'
    
    try:
    
        parent = entity_types_client.project_agent_path(project_id)
        
        display_name = entity_name_validate_n_update(display_name)
        
        entity_type = dialogflow.types.EntityType(
            display_name=display_name, kind=kind)
    
        response = entity_types_client.create_entity_type(parent, entity_type)
        
    except GError as error:
        return error
    
    print('Entity type created: \n{}'.format(response))
    print("create_entity_type method ended")    
    
    
def createEntities(productCategories):
    
    print("createEntities method started")
    
    print("Number of productCategories to be loaded",len(productCategories))
    
    for productType in productCategories:
        
        print("Creating Entity Type:" , productType)
        
        try:
            
            create_entity_type(productType,productType)
        
        except FailedPrecondition as error:
            print("Error creating Entity Type", error)
            continue
        
    print("createEntities method started")
    
def list_entity_types():
    
    print("list_entity_types method started")
    
    try:
    
        parent = entity_types_client.project_agent_path(project_id)
    
        entity_types = entity_types_client.list_entity_types(parent)
    
        for entity_type in entity_types:
            print('Entity type name: {}'.format(entity_type.name))
            print('Entity type display name: {}'.format(entity_type.display_name))
            print('Number of entities: {}\n'.format(len(entity_type.entities)))
    
    except GError as error:
        return error
    
    print("list_entity_types method ended")
            
def get_entity_displayNames():
    
    print("get_entity_displayNames method started")
    
    try:
        
        parent = entity_types_client.project_agent_path(project_id)
    
        entity_types = entity_types_client.list_entity_types(parent)
        
        entity_displayNames=[]
    
        for entity_type in entity_types:
            entity_displayNames.append(entity_type.display_name)    
        
    except NotFound:
            print("EntityType not found")
     
    print("get_entity_displayNames method ended")
    
    return entity_displayNames

def delete_all_existing_entities():
    
    print("delete_all_existing_entities method started")
    
    try:
        
        entity_displayNames = get_entity_displayNames()
        
        for entityName in entity_displayNames:
            
            entity_type_ids = _get_entity_type_ids(entityName)
            
            for entity_type_id in entity_type_ids:
                
                try:
                    delete_entity_type(entity_type_id)
    
                except NotFound as error:
                    print(error)
                    print("EntityType not found", entityName)
                    continue
            
    except NotFound as error:
        return error
    
    print("delete_all_existing_entities method ended")


# [START dialogflow_create_entity]
def create_entity(entity_type_id, entity_value, synonyms):
    """Create an entity of the given entity type."""
    
    print("create_entity method started")

    # Note: synonyms must be exactly [entity_value] if the
    # entity_type's kind is KIND_LIST
    synonyms = [entity_value]

    entity_type_path = entity_types_client.entity_type_path(
        project_id, entity_type_id)

    entity = dialogflow.types.EntityType.Entity()
    entity.value = entity_value
    entity.synonyms.extend(synonyms)

    response = entity_types_client.batch_create_entities(
        entity_type_path, [entity])

    print('Entity created: {}'.format(response))
    
    print("create_entity method ended")
    
    
# [END dialogflow_create_entity]

def create_productNames(productCategories):
    
    print("create_productNames method started")
    
    try:
        count = 0
        
        print("Product Categories :: ",productCategories )
        
        entity_displayNames = get_entity_displayNames()
        
        for entityName in entity_displayNames:
            
            print("Entity Name :: ",entityName)
            
            if entityName in productCategories:
                
                print("Generating entities of type: ",entityName)
                
                entity_type_ids = _get_entity_type_ids(entityName)
                
                print("No of entity type ids are: ", entity_type_ids)
            
                for entity_type_id in entity_type_ids:
                    
                    productNames = loadProductNames(entityName)
                    
                    for productName in productNames:
                        
                        print("Creating Product Name: ", productName)
                        
                        count+=1
                        
                        try:
                            create_entity(entity_type_id, productName, productName)
                            
                        except InvalidArgument as error:
                            print("Error creatinf Entity", error)
                            continue
                        
                        except ResourceExhausted:
                             print("Either out of resource quota or reaching rate limiting. The client should look for google.rpc.QuotaFailure error detail for more information.")
        
                        if(count % 50 == 0):
                            try:
                                print("Going for sleep for 45 seconds")
                                #Wait for 60 seconds
                                time.sleep(45)
                                
                            except KeyboardInterrupt:
                                print('\n\nKeyboard exception received. Exiting.')
                                exit()
                        
    
    except NotFound:
        print("EntityType not found")
            
    
    print("create_productNames method ended")