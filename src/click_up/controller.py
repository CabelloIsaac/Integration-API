import json

from .config import Config
from .constants import ClientCustomFields
from .schemas import ClientBase, TaskUpdatedElement
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
        Config.CLICKUP_CLIENTES_LIST_ID,
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

    custom_fields = clickup_api_service.get_list_custom_fields(Config.CLICKUP_CLIENTES_LIST_ID)["fields"]
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
        members = clickup_api_service.get_list_members(Config.CLICKUP_CLIENTES_LIST_ID)["members"]
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
        client = clickup_api_service.create_task(Config.CLICKUP_CLIENTES_LIST_ID, client)

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
            new_product = clickup_api_service.create_task(Config.CLICKUP_CLIENTES_LIST_ID, new_product)

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


def create_webhook():
    # webhook_endpoint = "https://cabelloisaac.com/clickup/webhook.php"
    webhook_endpoint = "https://hook.us1.make.com/ky7jwni8gteba46ms9mdh90eiyrtp24j"
    delete_webooks = False

    # Get all webhooks in team
    webhooks = clickup_api_service.get_webhooks(Config.CLICKUP_TEAM_ID)["webhooks"]

    # Check if webhook exists
    webhook_exists = False

    for wh in webhooks:
        if wh["endpoint"] == webhook_endpoint:
            print (f"Webhook already exists at {webhook_endpoint}")
            if delete_webooks:
                print (f"Deleting webhook {wh['id']}")
                clickup_api_service.delete_webhook(wh["id"])
            webhook_exists = True

    # If webhook doesn't exist, create it
    if not webhook_exists:
        print (f"Creating webhook at {webhook_endpoint}")
        webhook = {
            "endpoint": webhook_endpoint,
            "events": [
                "taskCreated",
                "taskUpdated",
            ],
            "space_id": Config.CLICKUP_CLIENTES_SPACE_ID,
        }
        webhook = clickup_api_service.create_webhook(Config.CLICKUP_TEAM_ID, webhook)
        if "id" not in webhook:
            print ("Error creating webhook")
            print (webhook)
            return
        else:
            print ("Webhook created")
            print (webhook)


def update_custom_fields_in_subtask(parent_custom_fields: list[dict], subtask: dict):
    fields_to_update = {}
                
    for parent_custom_field in parent_custom_fields:
        field_name = parent_custom_field["name"]
        
        if field_name in Config.FIELDS_TO_UPDATE_WHEN_UPDATE_PROJECT:
            field_value = Utils.get_custom_field_value_by_name(parent_custom_fields, field_name)    
            fields_to_update[field_name] = field_value  

    print (f"\nUpdating fields in task '{subtask['name']}':")
    for field_to_update in fields_to_update:
        field_id = Utils.get_custom_field_id_by_name(parent_custom_fields, field_to_update)
        field_name = field_to_update
        field_value = fields_to_update[field_to_update]
        field_type = Utils.get_custom_field_type_by_id(parent_custom_fields, field_id)

        if field_id != "" and field_value != "":
            print (f"\nField id: {field_id}")
            print (f"Field name: {field_name}")
            print (f"Field value: {field_value}")
            print (f"Field type: {field_type}")
            clickup_api_service.set_custom_field_to_task(subtask["id"], field_id, field_value, type=field_type)


def sync_task(request: TaskUpdatedElement):
    print (f"Syncing task {request.task_id}")
    updated_task_id = request.task_id
    updated_task = clickup_api_service.get_task(
        updated_task_id,
        include_subtasks=True,
        custom_task_ids=request.custom_task_ids,
    )

    if "id" not in updated_task:
        return "Task not found"

    subtasks_length = len(updated_task["subtasks"])

    print (f"Task name: '{updated_task['name']}'")
    print (f"Subtasks: {subtasks_length}")

    if subtasks_length == 0:
        return "No subtasks found. Nothing to do."

    updated_task_custom_fields = updated_task["custom_fields"]
    updated_subtasks = []

    for subtask in updated_task["subtasks"]:
        update_custom_fields_in_subtask(updated_task_custom_fields, subtask)
        updated_subtasks.append({
            "id": subtask["id"],
            "name": subtask["name"],
            "url": subtask["url"]
        })

    response = {
        "status": "ok",
        "updated_task": {
            "id": updated_task["id"],
            "name": updated_task["name"],
            "url": updated_task["url"]
        },
        "updated_subtasks": updated_subtasks
    }

    return response


def sync_all_tasks():

    # Set to True to update only the first subtask found. Set to False to update all subtasks found.
    ONLY_EXECUTE_ONCE = True 
    create_webhook()

    # Get lists from folder
    lists = clickup_api_service.get_lists_from_folder(Config.CLICKUP_PRODUCTOS_FOLDER_ID)["lists"]

    # Get tasks from each list
    for list in lists:
        print ("\n############################################")
        print (f"Getting tasks from list '{list['name']}'")
        list_id = list["id"]
        tasks = clickup_api_service.get_tasks(list_id, subtasks=True)["tasks"]

        parent_task = None

        for task in tasks:
            parent = task["parent"]
            if parent != "None" and parent is not None:
                print ("\n--------------------------------------------")
                print (f"Fixing task '{task['name']}' - {task['id']}")

                # Check if parent task is not the same as the last one
                if parent_task is None or parent_task["id"] != parent:
                    print (f"\nGetting parent task with id: '{parent}'")
                    parent_task = clickup_api_service.get_task(parent)

                # Get parent task custom fields
                parent_custom_fields = parent_task["custom_fields"]

                print (f"Parent task '{parent_task['name']}'")

                update_custom_fields_in_subtask(parent_custom_fields=parent_custom_fields, subtask=task)

                if ONLY_EXECUTE_ONCE:
                    return "Done"

        return "Done"
        