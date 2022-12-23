import json
import requests

class ClickUp:

    api_prefix = "https://api.clickup.com/api/v2"

    def __init__(self, token):
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }

    def get_custom_fields(self, list_id):
        url = f"{self.api_prefix}/list/{list_id}/field"
        response = requests.get( url, headers=self.headers)
        return response.json()

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
        

      