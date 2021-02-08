# dialogflow
import os
import dialogflow_v2 as dialogflow
from django.core import serializers
from google.protobuf.json_format import MessageToJson
from google.api_core.exceptions import InvalidArgument

import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'chatapp/paichaibot-jxekdn-64edeccfdfdf.json'

DIALOGFLOW_PROJECT_ID = 'paichaibot-jxekdn'
DIALOGFLOW_LANGUAGE_CODE = 'ko'
SESSION_ID = 'me'

def read_dialogflow(text_to_be_analyzed):
    # dislogflow에서 응답을 받아옴
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    
    result = ''
    query_result = response.query_result

    if query_result.fulfillment_text == 'telephone' and query_result.webhook_source == 'webhook':
        result = json.loads(MessageToJson(query_result.webhook_payload))
    else:
        result = response.query_result.fulfillment_text

    return result