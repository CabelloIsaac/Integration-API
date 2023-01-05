from .click_up import controller as click_up_controller
from .click_up.schemas import ClientBase
from .hubspot import controller as hubspot_controller


def sync_clients():
    """
    Syncs clients and projects between Hubspot and ClickUp

    Returns:
        list: Synced clients from Hubspot to ClickUp
    """
    click_up_clients = hubspot_controller.process_deals()
    processed_click_up_clients = []

    for click_up_client in click_up_clients:
        processed_click_up_client = click_up_controller.create_client(ClientBase(**click_up_client))
        processed_click_up_clients.append(processed_click_up_client)

    for processed_click_up_client in processed_click_up_clients:
        if processed_click_up_client["status"] == "ok":
            projects = processed_click_up_client["projects"]
            for project in projects:
                hubspot_controller.update_project(project=project)

    for click_up_client in click_up_clients:
        hubspot_controller.set_deal_as_added_to_clickup(deal_id=click_up_client["hubspot_deal_id"])

    return processed_click_up_clients