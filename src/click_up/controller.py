import json
from time import sleep, time

from .config import Config
from ..constants import ClickUpCustomFields
from .schemas import ClientBase, TaskUpdatedElement
from .service import clickup_api_service
from .utils import Utils
from ..hubspot import controller as hubspot_controller
from src.service import LoggingService

loggin_service = LoggingService(module="click_up")

def build_nif_cif_cliente_for_checking_if_exists(nif_cif_cliente_field_id: str, nif_cif_cliente:str):
    """
    Build the custom fields to check if a client exists

    Args:
        nif_cif_cliente_field_id (str): The CIF/NIF custom field id
        nif_cif_cliente (str): The CIF/NIF value
    Returns:
        str: The custom fields to check if a client exists
    """
    nif_cif_cliente_for_checking_if_exists = {}

    if nif_cif_cliente:
        nif_cif_cliente_for_checking_if_exists = {
            "field_id": nif_cif_cliente_field_id,
            "operator": "=",
            "value": nif_cif_cliente
        }

    nif_cif_cliente_for_checking_if_exists = [nif_cif_cliente_for_checking_if_exists]
    nif_cif_cliente_for_checking_if_exists = json.dumps(nif_cif_cliente_for_checking_if_exists)

    return nif_cif_cliente_for_checking_if_exists


def set_custom_fields_to_task(task_id, custom_fields:list[dict]):
    """
    Set custom fields to a task

    Args:
        task_id (str): The task id
        custom_fields (list[dict]): The custom fields to set
    """
    for custom_field in custom_fields:
        custom_field_id = custom_field["id"]
        custom_field_value = custom_field["value"]
        clickup_api_service.set_custom_field_to_task(task_id=task_id, field_id=custom_field_id, value=custom_field_value)


def check_client_exists(custom_fields, nif_cif_cliente):
    """
    Check if a client exists

    Args:
        custom_fields (list[dict]): The custom fields
        nif_cif_cliente (str): The CIF/NIF value
    Returns:
        dict: The client if exists, None otherwise
    """
    nif_cif_cliente_field_id = Utils.get_custom_field_id_by_name(custom_fields, ClickUpCustomFields.CIF_NIF_CLIENTE)
    nif_cif_cliente_for_checking_if_exists = build_nif_cif_cliente_for_checking_if_exists(nif_cif_cliente_field_id, nif_cif_cliente)

    clients = clickup_api_service.get_tasks(
        Config.CLIENTES_LIST_ID,
        include_closed=True,
        custom_fields=nif_cif_cliente_for_checking_if_exists
    )["tasks"]

    found_client = None

    for existing_cliente in clients:
        existing_cliente_nif_cif = Utils.get_nif_cif_from_custom_fields(existing_cliente["custom_fields"], custom_fields)
        if existing_cliente_nif_cif["value"] == nif_cif_cliente:
            found_client = existing_cliente
            break

    return found_client


def create_client(client_name, cs_owner, custom_fields, client_custom_fields, nif_cif_cliente):
    """
    Create a client

    Args:
        client_name (str): The client name
        cs_owner (str): The CS owner email
        custom_fields (list[dict]): The custom fields
        client_custom_fields (list[dict]): The client custom fields
        nif_cif_cliente (str): The CIF/NIF value

    Returns:
        dict: The client if exists, None otherwise
    """
    loggin_service.info(f"Creating client {client_name}")

    # Build client name
    client_full_name = Utils.build_client_name(cifNif=nif_cif_cliente, name=client_name)

    # Get CS owner id
    members = clickup_api_service.get_list_members(Config.CLIENTES_LIST_ID)["members"]
    cs_owner_id = Utils.get_member_id_by_email(members=members, email=cs_owner)

    # Add NIF/CIF to client custom fields
    client_custom_fields.append({
        "name": ClickUpCustomFields.CIF_NIF_CLIENTE,
        "value": nif_cif_cliente
    })

    # Build client custom fields
    client_custom_fields = Utils.build_client_custom_fields(client_custom_fields, custom_fields)

    # Build client object
    client = {
        "name": client_full_name,
        "status": Config.NEW_CLIENT_STATUS,
    }

    # Create client
    client = clickup_api_service.create_task_from_template(
        list_id=Config.CLIENTES_LIST_ID,
        template_id=Config.NEW_CLIENT_TEMPLATE_ID,
        task=client
    )

    # The task could not be created
    if "id" not in client:
        loggin_service.error(f"Error creating client {client_name}")
        return {
            "status": "error",
            "error": "Error creating client",
            "nif_cif": nif_cif_cliente,
            "name": client_name,
            "error_message": client
        }

    client_id = client["id"]
    client_url = client["task"]["url"]

    loggin_service.info (f"Client {client_name} ({client_id}) created at {client_url}")

    # Apply assignees to client
    client = clickup_api_service.update_task(task_id=client_id, data={
        "assignees": {
            "add": [cs_owner_id]
        }
    })

    # Apply custom fields to client
    set_custom_fields_to_task(task_id=client_id, custom_fields=client_custom_fields)

    return client


def sync_client(request: ClientBase):
    """
    Create or update a client in ClickUp from a request object (ClientBase)
    Steps: 
        - Check if client exists
        - If exists, add projects to it
        - If not exists, create it and add projects to it
    
    Args:
        request (ClientBase): The request object
    """

    custom_fields = clickup_api_service.get_list_custom_fields(Config.CLIENTES_LIST_ID)["fields"]
    product_lists = clickup_api_service.get_lists_from_folder(Config.PRODUCTOS_FOLDER_ID)["lists"]

    client_exists = check_client_exists(custom_fields, request.nif_cif)

    client_name = request.name.upper()
    cs_owner = request.cs_owner

    client = {}

    if client_exists:
        # if exists, take the current it to add projects
        loggin_service.info (f"Client already exists at {client_exists['url']}")
        client = client_exists
    else:
        client = create_client(
            client_name=client_name,
            cs_owner=cs_owner,
            custom_fields=custom_fields,
            client_custom_fields=request.custom_fields,
            nif_cif_cliente=request.nif_cif
        )

    if "id" not in client:
        return client

    client_id = client["id"]
    client_url = client["url"]
    cs_owner_id = Utils.get_member_id_by_email(members=client["assignees"], email=cs_owner)
    products = request.products

    projects = [] # Projects to be returned to Hubspot

    # Create products
    for product in products:
        sku = product["sku"]
        hubspot_product_id = product["id"]
        product_name = f"{sku}: {client_name}"
        list_id = Utils.get_list_id_for_product_by_sku(lists=product_lists, sku=sku)
        template_id = Utils.get_template_id_for_product_by_sku(sku=sku)

        if template_id is None:
            loggin_service.error(f"Error creating product {product_name}: template not found")
            return {
                "status": "error",
                "error": "Error creating product",
                "nif_cif": request.nif_cif,
                "name": request.name,
                "error_message": f"Error creating product {product_name}: template not found"
            }

        loggin_service.info(f"Creating product {product_name} in list {list_id} with template {template_id}")

        if list_id is None:
            loggin_service.error(f"Error creating product {product_name}: list not found")
            return {
                "status": "error",
                "error": "Error creating product",
                "nif_cif": request.nif_cif,
                "name": request.name,
                "error_message": f"Error creating product {product_name}: list not found"
            }

        product_custom_fields = [
            {
                "name": ClickUpCustomFields.ESTADO_PROYECTO,
                "value": "DOCUMENTACIÓN"
            },
            {
                "name": ClickUpCustomFields.PRODUCTO,
                "value": Utils.get_tipo_proyecto_name_by_key(sku)
            },
            {
                "name": ClickUpCustomFields.TIPO_ITEM_CLICKUP,
                "value": "Proyecto"
            }

        ]

        product_custom_fields = Utils.build_client_custom_fields(product_custom_fields, custom_fields)

        new_product = {
            "name": product_name,
            "status": Config.NEW_PROJECT_STATUS,
        }

        new_product = clickup_api_service.create_task_from_template(
            list_id=list_id,
            template_id=template_id,
            task=new_product
        )

        if "id" not in new_product:
            loggin_service.error(f"Error creating product {product_name}")
            return {
                "status": "error",
                "error": "Error creating product",
                "nif_cif": request.nif_cif,
                "name": request.name,
                "error_message": new_product
            }

        new_product_id = new_product["id"]
        new_product_url = new_product["task"]["url"]

        loggin_service.info(f"Product {product_name} ({new_product_id}) created at {new_product_url}")
        
        # Apply assignees to product
        loggin_service.info(f"Assigning {cs_owner} as owner of product {product_name}")
        new_product = clickup_api_service.update_task(task_id=new_product_id, data={
            "assignees": {
                "add": [cs_owner_id]
            }
        })

        # Apply custom fields to product
        set_custom_fields_to_task(task_id=new_product_id, custom_fields=product_custom_fields)

        # Link product to client
        clickup_api_service.add_task_link(client_id, new_product_id)

        projects.append({
            "clickup_id": new_product_id,
            "clickup_link": new_product_url,
            "hubspot_id": hubspot_product_id,
            "sku": sku,
            "clickup_project_status": "DOCUMENTACIÓN"
        })

    return {
        "status": "ok",
        "id": client_id,
        "nif_cif": request.nif_cif,
        "name": request.name,
        "url": client_url,
        "projects": projects
    }


def create_webhook():
    # webhook_endpoint = "https://cabelloisaac.com/clickup/webhook.php"
    webhook_endpoint = "https://hook.us1.make.com/ky7jwni8gteba46ms9mdh90eiyrtp24j"
    delete_webooks = False

    # Get all webhooks in team
    webhooks = clickup_api_service.get_webhooks(Config.TEAM_ID)["webhooks"]

    # Check if webhook exists
    webhook_exists = False

    for wh in webhooks:
        if wh["endpoint"] == webhook_endpoint:
            loggin_service.info(f"Webhook already exists at {webhook_endpoint}")
            if delete_webooks:
                loggin_service.info(f"Deleting webhook {wh['id']}")
                clickup_api_service.delete_webhook(wh["id"])
            webhook_exists = True

    # If webhook doesn't exist, create it
    if not webhook_exists:
        loggin_service.info(f"Creating webhook at {webhook_endpoint}")
        webhook = {
            "endpoint": webhook_endpoint,
            "events": [
                "taskCreated",
                "taskUpdated",
            ],
            "space_id": Config.CLIENTES_SPACE_ID,
        }
        webhook = clickup_api_service.create_webhook(Config.TEAM_ID, webhook)
        if "id" not in webhook:
            loggin_service.error(f"Error creating webhook: {webhook}")
            return
        else:
            loggin_service.info(f"Webhook created: {webhook}")


def apply_its_lowest_status_to_client(request: TaskUpdatedElement):
    loggin_service.info(f"Applying its lowest status to client {request.task_id}")
    client = clickup_api_service.get_task(
        task_id=request.task_id,
        include_subtasks=True,
        custom_task_ids=request.custom_task_ids,
    )
    
    if "id" not in client:
        return "Client not found"
    
    task_id = client["id"]

    client_current_status = Utils.get_custom_field_value_by_name(
        client["custom_fields"],
        ClickUpCustomFields.ESTADO_CLIENTE,
    )

    if client_current_status is None:
        loggin_service.error(f"Client { request.task_id } has no status")
        return "Client status not found"
    elif client_current_status == "":
        client_current_status = 0
    
    loggin_service.info(f"Client current status: {client_current_status}")
    
    linked_tasks = client["linked_tasks"]
    
    loggin_service.info(f"Linked tasks found: {len(linked_tasks)}")
    
    if len(linked_tasks) == 0:
        return "No linked tasks found"
    
    project_statuses = []
    
    for linked_task in linked_tasks:
        linked_task_id = linked_task["link_id"]
        linked_task_data = clickup_api_service.get_task(task_id=linked_task_id)
        linked_task_status = Utils.get_custom_field_value_by_name(linked_task_data["custom_fields"], ClickUpCustomFields.ESTADO_PROYECTO)
        project_statuses.append(linked_task_status)
        loggin_service.info(f"Linked task {linked_task_id} status: {linked_task_status}")
        
    lowest_status = min(project_statuses)
    
    if lowest_status == client_current_status:
        loggin_service.info(f"Client status is already {lowest_status}")
        return "Client status is already lowest"
    else:
        loggin_service.info(f"Client status is {client_current_status}, changing to {lowest_status}")
        clickup_custom_fields = clickup_api_service.get_list_custom_fields(Config.CLIENTES_LIST_ID)["fields"]
        estado_client_field_id = Utils.get_custom_field_id_by_name(clickup_custom_fields, ClickUpCustomFields.ESTADO_CLIENTE)
        client = clickup_api_service.set_custom_field_to_task(
            task_id=task_id,
            field_id=estado_client_field_id,
            value=lowest_status,
        )
        return f"Client status changed from {client_current_status} to {lowest_status}"
    

def sync_task(request: TaskUpdatedElement):
    """Syncs a task with its subtasks"""

    start_time = time()

    loggin_service.info(f"Syncing task {request.task_id}")
    updated_task_id = request.task_id
    updated_task = clickup_api_service.get_task(
        updated_task_id,
        include_subtasks=True,
        custom_task_ids=request.custom_task_ids,
    )

    if "id" not in updated_task:
        return "Task not found"

    # Send task status to Hubspot
    updated_task_original_id = updated_task["id"]
    status = Utils.get_custom_field_value_by_name(updated_task["custom_fields"], ClickUpCustomFields.ESTADO_PROYECTO, get_option_name=True)
    hubspot_controller.set_click_up_status_in_project(click_up_status=status, click_up_id=updated_task_original_id)

    if "subtasks" not in updated_task:
        return "No subtasks found. Nothing to do."

    subtasks_length = len(updated_task["subtasks"])

    loggin_service.info(f"Task name: '{updated_task['name']}'")
    loggin_service.info(f"Subtasks: {subtasks_length}")

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

    end_time = time()
    loggin_service.info(f"Syncing task {request.task_id} took {end_time - start_time} seconds")

    return response


def update_custom_fields_in_subtask(parent_custom_fields: list[dict], subtask: dict):
    fields_to_update = {}
    
    start_time = time()
                
    for parent_custom_field in parent_custom_fields:
        field_name = parent_custom_field["name"]
        
        if field_name in Config.FIELDS_TO_UPDATE_WHEN_UPDATE_PROJECT:
            field_value = Utils.get_custom_field_value_by_name(parent_custom_fields, field_name)    
            fields_to_update[field_name] = field_value

    loggin_service.info(f"\nUpdating fields in task '{subtask['name']}':")
    for field_to_update in fields_to_update:
        field_id = Utils.get_custom_field_id_by_name(parent_custom_fields, field_to_update)
        field_name = field_to_update
        field_value = fields_to_update[field_to_update]
        field_type = Utils.get_custom_field_type_by_id(parent_custom_fields, field_id)

        if field_id != "" and field_value != "":
            clickup_api_service.set_custom_field_to_task(subtask["id"], field_id, field_value, type=field_type)

    loggin_service.info(f"Finished updating fields in task '{subtask['name']}' in {time() - start_time} seconds")


def sync_all_tasks():

    start_time = time()
    tasks_processed = 0

    # Set to True to update only the first subtask found. Set to False to update all subtasks found.
    ONLY_EXECUTE_ONCE = False 
    create_webhook()

    # Get lists from folder
    lists = clickup_api_service.get_lists_from_folder(Config.PRODUCTOS_FOLDER_ID)["lists"]

    # Get tasks from each list
    for list in lists:
        loggin_service.info("\n############################################")
        loggin_service.info(f"Getting tasks from list '{list['name']}'")
        list_id = list["id"]
        tasks = []
        current_page = 0
        is_last_page = False

        # Get tasks from list (paginated)
        while not is_last_page:
            tasks_response = clickup_api_service.get_tasks(list_id, subtasks=True, page=current_page)

            if "tasks" not in tasks_response:
                loggin_service.info("Error getting tasks")
                return tasks_response

            current_page += 1

            tasks += tasks_response["tasks"]
            is_last_page = tasks_response["tasks"] == []

        loggin_service.info(f"Tasks found: {len(tasks)}")

        parent_task = None

        for task in tasks:
            parent = task["parent"]
            if parent != "None" and parent is not None:
                loggin_service.info("\n--------------------------------------------")
                loggin_service.info(f"Fixing task '{task['name']}' - {task['id']}")

                # Check if parent task is not the same as the last one
                if parent_task is None or parent_task["id"] != parent:
                    loggin_service.info(f"\nGetting parent task with id: '{parent}'")
                    parent_task = clickup_api_service.get_task(parent)

                # Get parent task custom fields
                parent_custom_fields = parent_task["custom_fields"]

                loggin_service.info(f"Parent task '{parent_task['name']}'")

                update_custom_fields_in_subtask(parent_custom_fields=parent_custom_fields, subtask=task)
                tasks_processed += 1

                if ONLY_EXECUTE_ONCE:
                    return "Done"

        loggin_service.info("Waiting 5 seconds before getting next list...")
        sleep(5)

    end_time = time()
    loggin_service.info(f"Syncing {tasks_processed} tasks took {end_time - start_time} seconds")

    return "Done"
    