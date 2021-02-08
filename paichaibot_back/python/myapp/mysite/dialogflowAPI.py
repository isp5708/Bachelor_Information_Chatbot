import dialogflow_v2 as dialogflow

async def getDialogApi(message, language_code = 'ko'):
    
    DIALOGFLOW_PROJECT_ID = 'paichaibot-jxekdn'
    SESSION_ID = 'testuserid'

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.types.TextInput(text=message, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = findAnswer(session_client, session, query_input)
    # session_client.detect_intent(session=session, query_input=query_input, timeout=1)
    
    print("response :", response)
    print("Query text:", response.query_result.query_text)
    fulfillText = response.query_result.fulfillment_text
    print("Fulfillment text:", fulfillText)
    return fulfillText  

def findAnswer(session_client, session, query_input):
    return session_client.detect_intent(session=session, query_input=query_input)