# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 16:04:14 2018

@author: Monika Asawa
"""

import dialogflow_v2 as dialogflow
import re
from random import randint

project_id="alphabotagent"

#Entity name may contain only the following: A-Z, a-z, 0-9, _ (underscore), - (dash). 
#And it should start with a letter."

def entity_name_validate_n_update(entityName):
    
    if re.search(r"[A-Za-z]{1}[A-Za-z0-9_-]*",entityName):
        return entityName
    else:
        return entityName + randint(100, 999)
        
# Helper to get entity_type_id from display name.
def _get_entity_type_ids(display_name):
    
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)
    entity_types = entity_types_client.list_entity_types(parent)
    entity_type_names = [
        entity_type.name for entity_type in entity_types
        if entity_type.display_name == display_name]

    entity_type_ids = [
        entity_type_name.split('/')[-1] for entity_type_name
        in entity_type_names]

    return entity_type_ids

def delete_entity_type(entity_type_id):
    """Delete entity type with the given entity type name."""

    entity_types_client = dialogflow.EntityTypesClient()

    entity_type_path = entity_types_client.entity_type_path(
        project_id, entity_type_id)

    entity_types_client.delete_entity_type(entity_type_path)
        
def create_entity_type(display_name, kind):
    """Create an entity type with the given display name."""

    kind = 'KIND_MAP'
    
    try:
        entity_types_client = dialogflow.EntityTypesClient()
    
        parent = entity_types_client.project_agent_path(project_id)
        entity_type = dialogflow.types.EntityType(
            display_name=display_name, kind=kind)
    
        response = entity_types_client.create_entity_type(parent, entity_type)
    except (dialogflow.api_core.exceptions) as error:
        return error
    
    print('Entity type created: \n{}'.format(response))
    
    
def list_entity_types():
    
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)

    entity_types = entity_types_client.list_entity_types(parent)

    for entity_type in entity_types:
        print('Entity type name: {}'.format(entity_type.name))
        print('Entity type display name: {}'.format(entity_type.display_name))
        print('Number of entities: {}\n'.format(len(entity_type.entities)))
        
def get_entity_displayNames():
    
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)

    entity_types = entity_types_client.list_entity_types(parent)
    
    entity_displayNames=[]

    for entity_type in entity_types:
        entity_displayNames.append(entity_type.display_name)
    
    return entity_displayNames

def delete_all_existing_entities():
    entity_displayNames = get_entity_displayNames()
    
    for entityName in entity_displayNames:
        
        entity_type_ids = _get_entity_type_ids(entityName)
        
        for entity_type_id in entity_type_ids:
            
            delete_entity_type(entity_type_id)
            