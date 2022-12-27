import json

from .config import Config
from .constants import ClientCustomFields
from .schemas import ClientBase
from .service import clickup_api_service
from .utils import Utils


def build_cif_nif_cliente_for_checking_if_exists(cif_nif_cliente_field_id: str, cif_nif_cliente:str):
    cif_nif_cliente_for_checking_if_exists = {}

    if cif_nif_cliente:
        cif_nif_cliente_for_checking_if_exists = {
            "field_id": cif_nif_cliente_field_id,
            "operator": "=",
            "value": cif_nif_cliente
        }

    cif_nif_cliente_for_checking_if_exists = [cif_nif_cliente_for_checking_if_exists]
    cif_nif_cliente_for_checking_if_exists = json.dumps(cif_nif_cliente_for_checking_if_exists)

    return cif_nif_cliente_for_checking_if_exists


def check_client_exists (custom_fields, cif_nif_cliente):
    cif_nif_cliente_field_id = Utils.get_custom_field_id_by_name(custom_fields, ClientCustomFields.CIF_NIF_CLIENTE)
    cif_nif_cliente_for_checking_if_exists = build_cif_nif_cliente_for_checking_if_exists(cif_nif_cliente_field_id, cif_nif_cliente)

    clients = clickup_api_service.get_tasks(
        Config.CLICKUP_LIST_ID,
        include_closed=True,
        custom_fields=cif_nif_cliente_for_checking_if_exists
    )["tasks"]

    found_client = None

    for existing_cliente in clients:
        existing_cliente_cif_nif = Utils.get_cif_nif_from_custom_fields(existing_cliente["custom_fields"], custom_fields)
        if existing_cliente_cif_nif["value"] == cif_nif_cliente:
            found_client = existing_cliente
            break

    return found_client


def create_client(request: ClientBase):

    custom_fields = clickup_api_service.get_list_custom_fields(Config.CLICKUP_LIST_ID)["fields"]
    client_exists = check_client_exists(custom_fields, request.cif_nif)

    if client_exists:
        print (f"Client already exists at {client_exists['url']}")
        return json.dumps({'error': 'Client already exists'})
    else:

        print (f"Creating client {request.name}")

        # Get data from request
        client_name = request.name.upper()
        cs_owner = request.cs_owner
        send_slack_notification = request.send_slack_notification
        send_email_notification = request.send_email_notification
        client_custom_fields = request.custom_fields
        products = request.products

        # Build client name
        client_full_name = Utils.build_client_name(cifNif=request.cif_nif, name=client_name)
        client_full_name = client_full_name.upper()

        # Get CS owner id
        members = clickup_api_service.get_list_members(Config.CLICKUP_LIST_ID)["members"]
        cs_owner_id = Utils.get_member_id_by_email(members=members, email=cs_owner)

        # Add CIF/NIF to client custom fields
        client_custom_fields.append({
            "name": ClientCustomFields.CIF_NIF_CLIENTE,
            "value": request.cif_nif
        })

        # Build client custom fields
        client_custom_fields = Utils.build_client_custom_fields(client_custom_fields, custom_fields)

        # Build client object
        client = {
            "name": client_full_name,
            "status": Config.CLICK_UP_NEW_CLIENT_STATUS,
            "assignees": [cs_owner_id],
            "custom_fields": client_custom_fields
        }

        # Create client
        client = clickup_api_service.create_task(Config.CLICKUP_LIST_ID, client)

        # Create products
        for product in products:
            product_name = f"{product}: {client_name}"

            product_custom_fields = [
                {
                    "name": ClientCustomFields.ESTADO_PROYECTO,
                    "value": "PREPARADOS (EN ESPERA)"
                },
                {
                    "name": ClientCustomFields.PRODUCTO,
                    "value": Utils.get_tipo_proyecto_name_by_key(product)
                },
                {
                    "name": ClientCustomFields.TIPO_ITEM_CLICKUP,
                    "value": "Proyecto"
                },

            ]
            product_custom_fields = Utils.build_client_custom_fields(product_custom_fields, custom_fields)

            new_product = {
                "name": product_name,
                "status": Config.CLICK_UP_NEW_CLIENT_STATUS,
                "assignees": [cs_owner_id],
                "custom_fields": product_custom_fields,
            }
            new_product = clickup_api_service.create_task(Config.CLICKUP_LIST_ID, new_product)

            print (f"Created product {new_product['name']}")
            
            clickup_api_service.add_task_link(client["id"], new_product["id"])

            # client_custom_fields = Utils.build_client_custom_fields([
            #         {
            #             "name": ClientCustomFields.ENLACE_A_PROYECTOS,
            #             "value": [new_product["id"]]
            #         }
            #     ], custom_fields)
            # clickup_api_service.update_task(client["id"], {
            #     "custom_fields":  client_custom_fields
            # })



        # TODO: Assign client id to hubspot project
        print (f"Assigning client id ({client['id']}) to hubspot project")

        # TODO: If send_slack_notification is true, send slack notification
        if send_slack_notification:
            print ("Sending slack notification")

        # TODO: If send_email_notification is true, send email notification
        if send_email_notification:
            print ("Sending email notification")

        return client


def fix_tasks():

    # Get lists from folder
    lists = clickup_api_service.get_lists_from_folder(Config.CLICKUP_PRODUCTOS_FOLDER_ID)["lists"]

    # Get tasks from each list
    for list in lists:
        print (f"Getting tasks from list {list['name']}")
        list_id = list["id"]
        tasks = clickup_api_service.get_tasks(list_id, subtasks=True)["tasks"]

        for task in tasks:
            parent = task["parent"]
            if parent != "None" and parent is not None:
                # print (f"Fixing task {task['name']}")
                custom_fields = task["custom_fields"]

                for custom_field in custom_fields:
                    if custom_field["name"] == ClientCustomFields.ESTADO_PROYECTO:
                       
                        value = ""

                        if "value" in custom_field:
                            print (f"Tiene ESTADO_PROYECTO: {custom_field['value']}")