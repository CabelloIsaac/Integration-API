from slack_sdk import WebClient
from .config import Config

class SlackService:

    def __init__(self, token: str):
        self.client = WebClient(token="token")


    def test_connection(self):
        try:
            api_response = self.client.api_test()
            if api_response["ok"]:
                return True
            else:
                return False
        except Exception as e:
                return e.args[0]


slack_client = SlackService(Config.SLACK_BOT_TOKEN)

      