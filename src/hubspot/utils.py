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