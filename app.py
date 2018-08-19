# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 19:36:14 2018

@author: Monika Asawa
"""

#Python libraries that we need to import for our bot
import random
import os
from flask import Flask, request, make_response, jsonify
from pymessenger.bot import Bot

from SuperStore_Product import recommend_selling_prodCat
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
    
    try:
        if action == 'promptProductCategory':
            print("Action value matched")
            res = product_category()
            print("del did method return anything",res)
        else:
            log.error('Unexpected action.')
        
    except TypeError:
        return 'Type error'

    print('Action: ' + action)
    #print('Response: ' + res)
    
    res =" 'fulfillmentMessages': [{'text': {'text': ['Good day1234! What can I do for you today?']}}]"

    #return make_response(jsonify({'fulfillmentText': res}))
    return make_response(res)

def product_category():
    """Returns a string containing text with a response to the user
    with all the product categories we have.

    uses the template responses found in product_responses.py as templates
    """
    print("del In the function")

    response = recommend_selling_prodCat()
    print("del did product_category return anything",response)
    return response
 
#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        print("ma : Token Received")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    print("ma : recipient_id", recipient_id)
					
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        print("ma : response_sent_text", response_sent_text)
                        send_message(recipient_id, response_sent_text)
                	
    					#if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"
 
 
def verify_fb_token(token_sent):
	#take token sent by facebook and verify it matches the verify token you sent
	#if they match, allow the request, else return an error
    print("ma : Token Sent", token_sent)
    print("ma : Verify Token", VERIFY_TOKEN)
    
    if token_sent == VERIFY_TOKEN:
        print("ma : Token verified")
        return request.args.get("hub.challenge")
    
    print("ma : Token didnt verify")
    return 'Invalid verification token'
 
 
#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)
 
#uses PyMessenger to send response to user
def send_message(recipient_id, response):
	#sends user the text message provided via input response parameter
	bot.send_text_message(recipient_id, response)
	print("ma : Sent Text Message")
	return "success"
 
if __name__ == "__main__":
    print("Main Method starts")
    app.run()
    print("Main Method ends")