import os

from dotenv import load_dotenv

from ..constants import ClickUpCustomFields

load_dotenv()

class Config():

    ACCESS_TOKEN = os.getenv('CLICKUP_ACCESS_TOKEN', "")
    TEAM_ID = "4708019"
    CLIENTES_SPACE_ID = "55696518"
    CLIENTES_FOLDER_ID = "127517171"
    CLIENTES_LIST_ID = "223523696"
    NEW_CLIENT_STATUS = "inbox"
    NEW_PROJECT_STATUS = "to do"
    PRODUCTOS_FOLDER_ID = "127517051"

    # TEMPLATES
    NEW_CLIENT_TEMPLATE_ID = "t-865bcmheb"
    PROJECT_TEMPLATES = {
        "KD-ANLT": "t-865bezne9",
        "KD-ECOM": "t-865beznb5",
        "KD-RRSS": "t-865bezmtv",
        "KD-SEO": "t-865bezmkb",
        "KD-WEB": "t-865bezmqp",
    }

    FIELDS_TO_UPDATE_WHEN_UPDATE_PROJECT = [
        ClickUpCustomFields.CS_MANAGER,
        ClickUpCustomFields.ESTADO_PROYECTO,
        ClickUpCustomFields.LINK_DOCUMENTACION_PROYECTO,
        ClickUpCustomFields.LINK_DOCUMENTO_TEXTOS,
        ClickUpCustomFields.LINK_PRESENTACION_CLIENTE,
        ClickUpCustomFields.PRODUCTO,
        ClickUpCustomFields.TIPO_ITEM_CLICKUP,
        ClickUpCustomFields.TIPO_PROYECTO,
    ]  
