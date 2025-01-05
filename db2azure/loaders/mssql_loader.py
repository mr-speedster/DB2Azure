from db2azure.connectors import MSSQLConnector
from db2azure.utils.loader_utils import LoaderUtils
from db2azure.helpers.response import ResponseHandler

# Define the public API of this module
__all__ = ['MSSQLLoader']


class MSSQLLoader:
    """
    A class for loading data from an MSSQL database to Azure Blob Storage in either JSON or CSV format.
    """

    @staticmethod
    def load_to_json(sql_query: str, connection_string: str, azure_config: dict) -> dict:
        """
        Load data from the MSSQL database to Azure Blob Storage in JSON format.

        Args:
            sql_query (str): SQL query to fetch data from the MSSQL database.
            connection_string (str): Connection string to connect to the MSSQL database.
            azure_config (dict): Configuration object containing Azure Blob Storage details.

        Returns:
            dict: Status of the operation, including success or error details.
        """
        try:
            # Use LoaderUtils to handle the JSON load operation
            return LoaderUtils.load_to_json(
                MSSQLConnector,  # Connector class for MSSQL
                connection_string,  # Connection string for MSSQL
                sql_query,  # SQL query to execute
                azure_config  # Azure Blob Storage configuration object
            )
        except Exception as e:
            # Log and handle any errors
            return ResponseHandler.error(message=f"Error in loading to JSON: {str(e)}")

    @staticmethod
    def load_to_csv(sql_query: str, connection_string: str, azure_config: dict) -> dict:
        """
        Load data from the MSSQL database to Azure Blob Storage in CSV format.

        Args:
            sql_query (str): SQL query to fetch data from the MSSQL database.
            connection_string (str): Connection string to connect to the MSSQL database.
            azure_config (dict): Configuration object containing Azure Blob Storage details.

        Returns:
            dict: Status of the operation, including success or error details.
        """
        try:
            # Use LoaderUtils to handle the CSV load operation
            return LoaderUtils.load_to_csv(
                MSSQLConnector,  # Connector class for MSSQL
                connection_string,  # Connection string for MSSQL
                sql_query,  # SQL query to execute
                azure_config  # Azure Blob Storage configuration object
            )
        except Exception as e:
            # Log and handle any errors
            return ResponseHandler.error(message=f"Error in loading to CSV: {str(e)}")