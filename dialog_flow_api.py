import dialogflow_v2 as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\Google_Account\small-talk-sioi-a15d9112b273.json"


class DialogFlowApiManager:
    def __init__(self):
        pass

    @staticmethod
    def GetMessageFromDialogFlowApi(message):
        sessionClient = dialogflow.SessionsClient()
        session = sessionClient.session_path("small-talk-sioi", "19881988")
        text_input = dialogflow.types.TextInput(
            text=message, language_code='ru')

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = sessionClient.detect_intent(session=session, query_input=query_input)
        resultMessage = response.query_result.fulfillment_text
        return resultMessage
