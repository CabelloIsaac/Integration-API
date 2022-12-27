import os

from dotenv import load_dotenv

load_dotenv()

class Config():
    CLICKUP_ACCESS_TOKEN = os.getenv('CLICKUP_ACCESS_TOKEN', "")
    CLICKUP_TEAM_ID = os.getenv('CLICKUP_TEAM_ID', "")
    CLICKUP_SPACE_ID = os.getenv('CLICKUP_CLIENTES_SPACE_ID', "")
    CLICKUP_FOLDER_ID = os.getenv('CLICKUP_CLIENTES_FOLDER_ID', "")
    CLICKUP_LIST_ID = os.getenv('CLICKUP_CLIENTES_LIST_ID', "")
    CLICK_UP_NEW_CLIENT_STATUS = os.getenv('CLICK_UP_NEW_CLIENT_STATUS', "inbox")