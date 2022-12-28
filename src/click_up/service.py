import json

import requests

from .config import Config
from .constants import CustomFieldTypes


class ClickUpApiService:

    api_prefix = "https://api.clickup.com/api/v2"

    def __init__(self, token):
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }

    def get_list_custom_fields(self, list_id, as_name_id_dict: bool = False):
        """Get all custom fields for a list
        Args:
            list_id (str): The list id
            as_name_id_dict (bool, optional): If True, returns a dict with the name as key and the id as value. Defaults to False.
        Returns:
            dict: The custom fields"""
        url = f"{self.api_prefix}/list/{list_id}/field"
        response = requests.get( url, headers=self.headers)

        if as_name_id_dict:
            json = response.json()
            fields = {}
            for field in json["fields"]:
                fields[field["name"]] = field["id"]
            return fields
        else:
            return response.json()


    # Tasks
    
    def create_task(self, list_id, task):
        """Create a task in a list
        Args:
            list_id (str): The list id
            task (dict): The task to create
        Returns:
            dict: The task created"""
        url = f"{self.api_prefix}/list/{list_id}/task"
        data = json.dumps(task)
        response = requests.post( url, headers=self.headers, data=data)
        return response.json()


    def create_task_from_template(self, list_id, template_id, task):
        """Create a task in a list from a template
        Args:
            list_id (str): The list id
            template_id (str): The template id
            task (dict): The task to create
        Returns:
            dict: The task created"""
        url = f"{self.api_prefix}/list/{list_id}/taskTemplate/{template_id}"
        data = json.dumps(task)
        response = requests.post( url, headers=self.headers, data=data, params={"template_id": template_id})
        return response.json()
        

    def get_tasks(
        self,
        list_id,
        include_closed: bool = False,
        custom_fields: str = None,
        subtasks: bool = False,
        page: int = 0,
    ):
        """Get all tasks in a list
        Args:
            list_id (str): The list id
        Returns:
            dict: The tasks"""
        url = f"{self.api_prefix}/list/{list_id}/task"
        response = requests.get(
            url,
            headers=self.headers,
            params={
                "include_closed": str(include_closed).lower(),
                "custom_fields": custom_fields,
                "subtasks": str(subtasks).lower(),
                "page": page,
            }
        )
        return response.json()


    def get_task(self, task_id, include_subtasks: bool = False, custom_task_ids: bool = False):
        """Get a task
        Args:
            task_id (str): The task id
        Returns:
            dict: The task"""
        url = f"{self.api_prefix}/task/{task_id}"

        query = {
            "include_subtasks": str(include_subtasks).lower(),
            "custom_task_ids": str(custom_task_ids).lower(),
            "team_id": Config.CLICKUP_TEAM_ID,
        }

        response = requests.get( url, headers=self.headers, params=query)
        return response.json()


    def update_task(self, task_id, task):
        """Update a task
        Args:
            task_id (str): The task id
            task (dict): The task to update
        Returns:
            dict: The task updated"""
        url = f"{self.api_prefix}/task/{task_id}"
        data = json.dumps(task)
        response = requests.put( url, headers=self.headers, data=data)
        return response.json()


    # Folders

    def get_lists_from_folder(self, folder_id):
        """Get all lists in a folder
        Args:
            folder_id (str): The folder id
        Returns:
            dict: The lists"""
        url = f"{self.api_prefix}/folder/{folder_id}/list"
        response = requests.get( url, headers=self.headers)
        return response.json()


    def set_custom_field_to_task(self, task_id, field_id, value, type: str = None):
        """Set a custom field to a task
        Args:
            task_id (str): The task id
            field_id (str): The field id
            value (str): The value to set
        Returns:
            dict: The task updated"""
        url = f"{self.api_prefix}/task/{task_id}/field/{field_id}"

        formatted_value = {"value": value}

        if type == CustomFieldTypes.USERS:
            users_id_list = [user["id"] for user in value]
            formatted_value = {"value":{"add": users_id_list}}

        data = json.dumps(formatted_value)
        requests.post( url, headers=self.headers, data=data)
        

    def get_list_members(self, list_id):
        """Get all members in a list
        Args:
            list_id (str): The list id
        Returns:
            dict: The members"""
        url = f"{self.api_prefix}/list/{list_id}/member"
        response = requests.get( url, headers=self.headers)
        return response.json()


    def add_task_link(self, task_id, links_to):
        """Add a link to a task
        Args:
            task_id (str): The task id
            links_to (str): The task id to link to
        Returns:
            dict: The link created"""
        url = f"{self.api_prefix}/task/{task_id}/link/{links_to}"
        response = requests.post( url, headers=self.headers)
        return response.json()


    def create_webhook(self, team_id, webhook):
        """Create a webhook
        Args:
            team_id (str): The team id
            webhook (dict): The webhook to create
        Returns:
            dict: The webhook created"""
        url = f"{self.api_prefix}/team/{team_id}/webhook"
        data = json.dumps(webhook)
        response = requests.post( url, headers=self.headers, data=data)
        return response.json()


    def get_webhooks(self, team_id):
        """Get all webhooks
        Args:
            team_id (str): The team id
        Returns:
            dict: The webhooks"""
        url = f"{self.api_prefix}/team/{team_id}/webhook"
        response = requests.get( url, headers=self.headers)
        return response.json()


    def delete_webhook(self, webhook_id):
        """Delete a webhook
        Args:
            webhook_id (str): The webhook id
        Returns:
            dict: The webhook deleted"""
        url = f"{self.api_prefix}/webhook/{webhook_id}"
        response = requests.delete( url, headers=self.headers)
        return response.json()



clickup_api_service = ClickUpApiService(Config.CLICKUP_ACCESS_TOKEN)

      