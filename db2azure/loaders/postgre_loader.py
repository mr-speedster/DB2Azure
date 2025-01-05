from db2azure.connectors import PostgresConnector
from db2azure.utils.loader_utils import LoaderUtils
from db2azure.helpers.response import ResponseHandler

# Define the public API of this module
__all__ = ['PostgreLoader']


class PostgreLoader:
    """
    A class for loading data from a PostgreSQL database to Azure Blob Storage in either JSON or CSV format.
    """

    @staticmethod
    def load_to_json(sql_query: str, connection_string: str, azure_config: dict) -> dict:
        """
        Load data from the PostgreSQL database to Azure Blob Storage in JSON format.

        Args:
            sql_query (str): SQL query to fetch data from the PostgreSQL database.
            connection_string (str): Connection string to connect to the PostgreSQL database.
            azure_config (dict): Configuration object containing Azure Blob Storage details.

        Returns:
            dict: Status of the operation, including success or error details.
        """
        try:
            # Use LoaderUtils to handle the JSON load operation
            return LoaderUtils.load_to_json(
                PostgresConnector,  # Connector class for Postgre
                connection_string,  # Connection string for Postgre
                sql_query,  # SQL query to execute
                azure_config  # Azure Blob Storage configuration object
            )
        except Exception as e:
            # Log and handle any errors
            return ResponseHandler.error(message=f"Error in loading to JSON: {str(e)}")

    @staticmethod
    def load_to_csv(sql_query: str, connection_string: str, azure_config: dict) -> dict:
        """
        Load data from the PostgreSQL database to Azure Blob Storage in CSV format.

        Args:
            sql_query (str): SQL query to fetch data from the PostgreSQL database.
            connection_string (str): Connection string to connect to the PostgreSQL database.
            azure_config (dict): Configuration object containing Azure Blob Storage details.

        Returns:
            dict: Status of the operation, including success or error details.
        """
        try:
            # Use LoaderUtils to handle the CSV load operation
            return LoaderUtils.load_to_csv(
                PostgresConnector,  # Connector class for Postgre
                connection_string,  # Connection string for Postgre
                sql_query,  # SQL query to execute
                azure_config  # Azure Blob Storage configuration object
            )
        except Exception as e:
            # Log and handle any errors
            return ResponseHandler.error(message=f"Error in loading to CSV: {str(e)}")