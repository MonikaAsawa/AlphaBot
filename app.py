# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:36:14 2018

@author: Monika Asawa
"""

#Python libraries that we need to import for our bot
import os
from flask import Flask, request, make_response, jsonify
from pymessenger.bot import Bot

from SuperStore_Product import recommend_selling_prodCat, suggest_selling_prodNames, check_if_product_selected, recommendProductsNames
from AppInit import setUpApp

import json

app = Flask(__name__)

#==============================================================================
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
DEVELOPER_ACCESS_TOKEN = os.environ['DIALOGFLOW_DEVELOPER_ACCESS_TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
#==============================================================================

bot = Bot(ACCESS_TOKEN)

log = app.logger

#==============================================================================
def setup_app():
    # All your initialization code
    print("Setup_app method starts")
    
    setUpApp()
    
    print("Setup_app method ends")
 
#setup_app()


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    
    print("del Just making sure this is being called")
    req = request.get_json(silent=True, force=True)
    print("del lets print req",req)
    
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    print("Going to check action value")
    print("del lets print req",req)
    
    res=''
    
    try:
        if action == 'promptProductCategory':
            print("promptProductCategory Action value matched")
            res = product_category()
            print("del did method return anything",res)
            
        elif action == 'recommendProducts':
            print("recommendProducts Action value matched")
            res = recommendProducts(req)
            print("del did method return anything",res)
            
        elif action == 'suggestTrendingProducts':
            print("recommendProducts Action value matched")
            res = suggestProducts(req)
            print("del did method return anything",res)
            
        else:
            log.error('Unexpected action.')
        
    except TypeError:
        return 'Type error'

    print('Action: ' + action)
    #print('Response: ' + res)
    
    #res =" 'fulfillmentMessages': [{'text': {'text': ['Good day1234! What can I do for you today?']}}]"

    return make_response(jsonify({'fulfillmentText': res}))
    #return make_response(jsonify({'fulfillmentMessages': res}))
    
def product_category():
    """Returns a string containing text with a response to the user
    with all the product categories we have.

    uses the template responses found in product_responses.py as templates
    """
    print("del In the function")

    response = recommend_selling_prodCat()
    print("del did product_category return anything",response)
    return response


def suggestProducts(req):
    parameters = req['queryResult']['parameters']
    
    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))
    
    selected_sub_category = parameters.get('productCategory')
    
    response = suggest_selling_prodNames(selected_sub_category)
    
    print("del did product_category return anything",response)
    return response

def recommendProducts(req):
    parameters = req['queryResult']['parameters']
    
    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))
    
    # Initialize error and params
    error = ''
    params = {}
    
    # validate request parameters, return an error if there are issues
    error, params = check_if_product_selected(parameters)
    
    if len(error) > 0:
        return error
    
    response = recommendProductsNames(params)
    
    print("del did product_category return anything",response)
    return response
    
if __name__ == "__main__":
    print("Main Method starts")
    app.run()
    print("Main Method ends")