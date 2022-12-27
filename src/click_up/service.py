import json

import requests

from .config import Config

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
        subtasks: bool = False
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
                "include_closed": include_closed,
                "custom_fields": custom_fields,
                "subtasks": subtasks,
            }
        )
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


    def set_custom_field_to_task(self, task_id, field_id, value):
        """Set a custom field to a task
        Args:
            task_id (str): The task id
            field_id (str): The field id
            value (str): The value to set
        Returns:
            dict: The task updated"""
        url = f"{self.api_prefix}/task/{task_id}/field/{field_id}"
        data = json.dumps({"value": value})
        response = requests.put( url, headers=self.headers, data=data)
        return response.json()
        

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


clickup_api_service = ClickUpApiService(Config.CLICKUP_ACCESS_TOKEN)

      