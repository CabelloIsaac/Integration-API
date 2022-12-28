import os

from dotenv import load_dotenv

from .constants import ClientCustomFields

load_dotenv()

class Config():
    CLICKUP_ACCESS_TOKEN = os.getenv('CLICKUP_ACCESS_TOKEN', "")
    CLICKUP_TEAM_ID = os.getenv('CLICKUP_TEAM_ID', "")
    CLICKUP_CLIENTES_SPACE_ID = os.getenv('CLICKUP_CLIENTES_SPACE_ID', "")
    CLICKUP_CLIENTES_FOLDER_ID = os.getenv('CLICKUP_CLIENTES_FOLDER_ID', "")
    CLICKUP_CLIENTES_LIST_ID = os.getenv('CLICKUP_CLIENTES_LIST_ID', "")
    CLICK_UP_NEW_CLIENT_STATUS = os.getenv('CLICK_UP_NEW_CLIENT_STATUS', "inbox")
    
    CLICKUP_PRODUCTOS_FOLDER_ID = os.getenv('CLICKUP_PRODUCTOS_FOLDER_ID', "")

    FIELDS_TO_UPDATE_WHEN_UPDATE_PROJECT = [
        ClientCustomFields.CS_MANAGER,
        ClientCustomFields.ESTADO_PROYECTO,
        ClientCustomFields.LINK_DOCUMENTACION_PROYECTO,
        ClientCustomFields.LINK_DOCUMENTO_TEXTOS,
        ClientCustomFields.LINK_PRESENTACION_CLIENTE,
        ClientCustomFields.PRODUCTO,
        ClientCustomFields.TIPO_ITEM_CLICKUP,
        ClientCustomFields.TIPO_PROYECTO,
    ]  