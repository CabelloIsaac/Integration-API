import json
from config.config import Config
from schemas.clickup_schemas import ClientBase


def get_custom_fields():
    custom_fields = Config.clickup.get_custom_fields(Config.CLICKUP_LIST_ID)
    return custom_fields

def create_client(request: ClientBase):
    custom_fields = get_custom_fields()["fields"]
    clean_custom_fields = {}
    for field in custom_fields:
        clean_custom_fields[field["name"]] = field["id"]

    client = {
        "name": request.name,
        "description": request.description,
        "status": request.status,
        "assignees": request.assignees,
        # "custom_fields": [
        #     {
        #         "id": clean_custom_fields[Config.ClientCustomFields.RAZON_SOCIAL],
        #         "value": "Test client"
        #     }
        # ]
    }

    client = Config.clickup.create_task(Config.CLICKUP_LIST_ID, client)

    return client
