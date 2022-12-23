import os
from dotenv import load_dotenv
from utils.clickup import ClickUp

load_dotenv()


class Config():
    CLICKUP_ACCESS_TOKEN = os.getenv('CLICKUP_ACCESS_TOKEN', "")
    clickup = ClickUp(CLICKUP_ACCESS_TOKEN)

    CLICKUP_TEAM_ID = os.getenv('CLICKUP_TEAM_ID', "")
    CLICKUP_SPACE_ID = os.getenv('CLICKUP_CLIENTES_SPACE_ID', "")
    CLICKUP_FOLDER_ID = os.getenv('CLICKUP_CLIENTES_FOLDER_ID', "")
    CLICKUP_LIST_ID = os.getenv('CLICKUP_CLIENTES_LIST_ID', "")
    # Enum with custom fields
    class ClientCustomFields():
        RAZON_SOCIAL: str = "RAZÓN SOCIAL"
        EMAIL_LLAVE_CLIENTE_PASSWORD: str = "EMAIL LLAVE CLIENTE PASSWORD"
        EMAIL_LLAVE_CLIENTE_EMAIL: str = "EMAIL LLAVE CLIENTE EMAIL"
        ID_CLIENTE_HUBSPOT: str = "ID CLIENTE HUBSPOT"
        SATISFACCION_CLIENTE: str = "Satisfacción Cliente"
        EQUIPO: str = "EQUIPO"
        CÓDIGO_PROYECTO: str = "CÓDIGO PROYECTO"
        LINK_DOCUMENTACIÓN_PROYECTO: str = "LINK DOCUMENTACIÓN PROYECTO"
        SUBVENCIÓN_APROBADA: str = "¿SUBVENCIÓN APROBADA?"
        ENLACE_HUBSPOT: str = "ENLACE HUBSPOT"
        ESTADO_PROYECTO: str = "ESTADO PROYECTO"
        ENLACE_A_PROYECTOS: str = "ENLACE A PROYECTOS"
        STATUS: str = "STATUS"
        TIPO_ITEM_CLICKUP: str = "TIPO ITEM CLICKUP"
        CODIGO_CLIENTE: str = "CÓDIGO CLIENTE"
        PRODUCTO: str = "PRODUCTO"
        CIF_NIF_CLIENTE: str = "CIF/NIF CLIENTE"