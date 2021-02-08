from django.core import serializers

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse

from django.http import HttpResponse
from pydialogflow_fulfillment import DialogflowRequest, DialogflowResponse, SimpleResponse, Suggestions

from . import models

import json

# Create your views here.

@csrf_exempt
def webhook(request):
    response = ''
    if request.body:
        dialogflow_request = DialogflowRequest(request.body)

        intent_name = dialogflow_request.get_intent_displayName()
        print(intent_name)
        if 'Telephone' in intent_name:
            entity = dialogflow_request.get_parameter("Department")
            print(entity)

            result = models.Contact.objects.filter(department=entity)

            result_json = serializers.serialize('json', result)
            print(result_json)

            dialogflow_response = DialogflowResponse('telephone')
            dialogflow_response.add(SimpleResponse(result_json, result_json))

            # dialogflow_response = DialogflowResponse("This is a text response")
            # dialogflow_response.add(SimpleResponse("This is a simple text response","This is a simple text response"))

            response = dialogflow_response.get_final_response()

    else :
        response = {
            "error" : "1",
            "message" : "An error occurred."
        }
    
    # print('res : ' + json.dumps(response))
    
    return HttpResponse(response, content_type='application/json; charset=utf-8')

    # # build a request object
    # req = json.loads(request.body)
    # print('req : ' + json.dumps(req))
    # # get action from json
    # action = req.get('queryResult').get('action')
    # # return a fulfillment message
    # fulfillmentText = {'fulfillmentText': 'This is Django test response from webhook.'}
    # # return response
    # return JsonResponse(fulfillmentText, safe=False)