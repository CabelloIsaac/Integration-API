from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .config import Config


class SlackService:
    
    def __init__(self, token: str):
        self.client = WebClient(token=token)


    def test_connection(self, send_alert: bool = False):
        try:
            api_response = self.client.api_test()
            if api_response["ok"]:
                
                if send_alert:
                    self.send_alert("✅ Test connection to Slack successful")
                
                return True
            else:
                return False
        except Exception as e:
                return e.args[0]
            
    
    def send_alert(self, message: str):
        try:
            response = self.client.chat_postMessage(
                channel=Config.SLACK_ALERTS_CHANNEL_ID,
                text=message,
                
            )
            return response.data
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            if not e.response["ok"]:
                return {
                    "status": "error",
                    "message": e.response["error"]
                }


slack_client = SlackService(Config.SLACK_BOT_TOKEN)

      