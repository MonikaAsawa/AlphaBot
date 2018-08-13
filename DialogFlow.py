# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 16:04:14 2018

@author: Monika Asawa
"""

import dialogflow_v2 as dialogflow
    
def create_entity_type(project_id, display_name, kind):
    """Create an entity type with the given display name."""

    kind = 'KIND_UNSPECIFIED'
    
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)
    entity_type = dialogflow.types.EntityType(
        display_name=display_name, kind=kind)

    response = entity_types_client.create_entity_type(parent, entity_type)

    print('Entity type created: \n{}'.format(response))
    
    
def list_entity_types(project_id):
    
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)

    entity_types = entity_types_client.list_entity_types(parent)

    for entity_type in entity_types:
        print('Entity type name: {}'.format(entity_type.name))
        print('Entity type display name: {}'.format(entity_type.display_name))
        print('Number of entities: {}\n'.format(len(entity_type.entities)))