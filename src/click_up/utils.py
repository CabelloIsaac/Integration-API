from .config import Config
from .constants import ProductsKeys
from ..constants import ClickUpCustomFields
from .service import clickup_api_service


class Utils:
    """Class for utility methods."""

    @staticmethod
    def build_client_name(cifNif: str, name: str) -> str:
        """Builds the client name from the client data. Example: "CLIENTE: 1234_NAME"

        Args:
            client (ClientBase): The client data.

        Returns:
            str: The client name in the format "CLIENTE: 1234_NAME".
        """
        return f"CLIENTE: {cifNif}_{name}".upper()

    
    @staticmethod
    def get_nif_cif_from_custom_fields(client_custom_fields: list, custom_fields: dict) -> dict:
        """Gets the CIF/NIF from the custom fields.

        Args:
            custom_fields (list): The custom fields in 'name as key and the id as value' format

        Returns:
            dict: The CIF/NIF field with the id and the value.
        """
        # custom_fields = clickup_api_service.get_list_custom_fields(Config.CLICKUP_LIST_ID, as_name_id_dict=True)

        nif_cif = {}
        nif_cif_custom_field_id = Utils.get_custom_field_id_by_name(custom_fields, ClickUpCustomFields.CIF_NIF_CLIENTE)
        for field in client_custom_fields:
            if field["id"] == nif_cif_custom_field_id:
                nif_cif = {
                    "id": field["id"],
                    "value": field["value"]
                }
                break

        return nif_cif


    @staticmethod
    def get_custom_field_id_by_name(custom_fields: list[dict], name: str) -> str:
        """Gets the custom field id by name.

        Args:
            custom_fields (list): The custom fields available in click up.
            name (str): The name of the custom field.

        Returns:
            str: The custom field id.
        """
        custom_field_id = ""
        for field in custom_fields:
            if field["name"] == name:
                custom_field_id = field["id"]
                break

        return custom_field_id


    @staticmethod
    def get_custom_field_by_id(custom_fields: list[dict], custom_field_id: str) -> str:
        """Gets the custom field by id.
        
        Args:
            custom_fields (list): The custom fields available in click up.
            custom_field_id (str): The custom field id.
        
        Returns:
            str: The custom field."""
        custom_field = {}
        for field in custom_fields:
            if field["id"] == custom_field_id:
                custom_field = field
                break

        return custom_field


    @staticmethod
    def get_custom_field_type_by_id(custom_fields: list[dict], custom_field_id: str) -> str:
        """Gets the custom field type by id.

        Args:
            custom_fields (list): The custom fields available in click up.
            custom_field_id (str): The custom field id.

        Returns:
            str: The custom field type.
        """
        custom_field_type = ""
        for field in custom_fields:
            if field["id"] == custom_field_id:
                custom_field_type = field["type"]
                break

        return custom_field_type


    @staticmethod
    def build_client_custom_fields(client_custom_fields: list[dict], custom_fields: list[dict]) -> list:
        """Builds the client custom fields from the client data and the custom fields available in click up.

        Args:
            client_custom_fields (list): The client custom fields.
            custom_fields (list): The custom fields available in click up.

        Returns:
            list: The client custom fields in a way that click up can understand.
            Example: [
                {
                    "id": "123456789",
                    "value": "1234"
                },
            ]
        """
        new_client_custom_fields = []

        for field in client_custom_fields:

            custom_field_id = Utils.get_custom_field_id_by_name(custom_fields, field["name"])
            custom_field_value = field["value"]
            custom_field = Utils.get_custom_field_by_id(custom_fields, custom_field_id)

            if "type" in custom_field:
                if custom_field["type"] == "drop_down":
                    for option in custom_field["type_config"]["options"]:
                        if option["name"] == custom_field_value:
                            custom_field_value = option["id"]
                            break

            new_client_custom_fields.append({
                "id": custom_field_id,
                "value": custom_field_value
            })

        return new_client_custom_fields
        

    @staticmethod
    def get_member_id_by_email(members: list[dict], email: str) -> str:
        """Gets the member id by email.

        Args:
            members (list): The members in the team.
            email (str): The email of the member.

        Returns:
            str: The member id.
        """
        member_id = ""
        for member in members:
            if member["email"] == email:
                member_id = member["id"]
                break

        return member_id


    @staticmethod
    def get_tipo_proyecto_name_by_key(key: str) -> str:
        """Gets the tipo proyecto id by name.

        Args:
            tipo_proyecto (str): The tipo proyecto name.

        Returns:
            str: The tipo proyecto id.
        """
        tipo_proyecto_name = ""
        if key == ProductsKeys.KD_WEB:
            tipo_proyecto_name = "KD-WEB"
        elif key == ProductsKeys.KD_SEO:
            tipo_proyecto_name = "KD-SEO"
        elif key == ProductsKeys.KD_ANLT:
            tipo_proyecto_name = "KD-ANALITICA"
        elif key == ProductsKeys.KD_RRSS:
            tipo_proyecto_name = "KD-RRSS"
        elif key == ProductsKeys.KD_ECOM:
            tipo_proyecto_name = "KD-ECOMMERCE"
        elif key == ProductsKeys.KD_CRM:
            tipo_proyecto_name = "KD-GESTIÓN_DE_CLIENTES"
        elif key == ProductsKeys.KD_PROC:
            tipo_proyecto_name = "KD-GESTIÓN_DE_PROCESOS"

        return tipo_proyecto_name


    @staticmethod
    def get_custom_field_value_by_name(custom_fields: list[dict], name: str, get_option_name: bool = False) -> str:
        """Gets the custom field value by name.

        Args:
            custom_fields (list): The custom fields in the task.
            name (str): The name of the custom field.

        Returns:
            str: The custom field value.
        """
        custom_field_value = ""
        for field in custom_fields:
            if field["name"] == name:
                if "value" in field:
                    custom_field_value = field["value"]
                break

        if get_option_name:
            if "type" in field:
                if field["type"] == "drop_down":
                    custom_field_value = field["type_config"]["options"][int(custom_field_value)]["name"]

        return custom_field_value


    def get_list_id_for_product_by_sku(lists: list[dict], sku: str) -> str:
        """Gets the corresponding list id for product by sku.

        Args:
            lists (list): The lists in the team.
            sku (str): The sku of the product.

        Returns:
            str: The list id.
        """
        list_id = ""
        for list in lists:
            # Check if the list name contains the sku
            if sku in list["name"]:
                list_id = list["id"]
                break

        return list_id


    def get_template_id_for_product_by_sku(sku: str) -> str:
        """Gets the corresponding template id for product by sku.

        Args:
            sku (str): The sku of the product.

        Returns:
            str: The template id.
        """
        return Config.PROJECT_TEMPLATES[sku]
        