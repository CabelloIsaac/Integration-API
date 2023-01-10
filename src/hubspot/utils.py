class Utils:
    """Class for utility methods."""

    @staticmethod
    def build_project_name(sku: str, deal_name: str) -> str:
        """Builds the project name from the sku and deal name.

        Args:
            sku (str): The sku.
            deal_name (str): The deal name.

        Returns:
            str: The project name.
        """
        return f"{sku} - {deal_name}"


    @staticmethod
    def build_single_line_products_list(line_items_data):
        """Builds a single line products list from the line items data.

        Args:
            line_items_data (list): The line items data.

        Returns:
            list: The single line products list.
        """
        products = ""
        for line_item in line_items_data:
            products += f"{line_item['name']}, "

        return products[:-2]