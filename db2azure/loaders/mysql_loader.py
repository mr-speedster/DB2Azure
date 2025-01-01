from db2azure.connectors import MySQLConnector
from db2azure.utils.loader_utils import LoaderUtils
from db2azure.helpers.response import ResponseHandler

# Define a public module
__all__ = ['MySQLLoader']

class MySQLLoader:
    """
    A class for loading data from a MySQL database to Azure Blob Storage in either JSON or CSV format.
    """
    
    @staticmethod
    def load_to_json(sql_query, connection_string, container_name, folder_path, file_name, azure_blob_url, sas_token):
        """
        Loads data from the MySQL database to an Azure Blob Storage container in JSON format.
        
        Args:
            sql_query (str): SQL query to fetch data from the MySQL database.
            connection_string (str): Connection string to connect to the MySQL database.
            container_name (str): Azure Blob Storage container name where the file will be stored.
            folder_path (str): Folder path in Azure Blob Storage for the file.
            file_name (str): Name of the file to be created in Azure Blob Storage.
            azure_blob_url (str): The URL to the Azure Blob Storage account.
            sas_token (str): SAS token for authentication to the Azure Blob Storage.

        Returns:
            dict: The status or error message of the operation.
        """
        try:
            # Use the LoaderUtils class to load data from MySQL to JSON format
            return LoaderUtils.load_to_json(
                MySQLConnector,  # Connector class for MySQL
                connection_string,  # Connection string for MySQL connection
                sql_query,  # SQL query to execute
                container_name,  # Azure Blob container name
                folder_path,  # Folder path in the Azure Blob container
                file_name,  # File name to be uploaded
                azure_blob_url,  # Azure Blob storage account URL
                sas_token  # SAS token for authentication
            )
        except Exception as e:
            # Handle any errors during the process and return an error message
            return ResponseHandler.error(message=f"Error: {str(e)}")

    @staticmethod
    def load_to_csv(sql_query, connection_string, container_name, folder_path, file_name, azure_blob_url, sas_token):
        """
        Loads data from the MySQL database to an Azure Blob Storage container in CSV format.
        
        Args:
            sql_query (str): SQL query to fetch data from the MySQL database.
            connection_string (str): Connection string to connect to the MySQL database.
            container_name (str): Azure Blob Storage container name where the file will be stored.
            folder_path (str): Folder path in Azure Blob Storage for the file.
            file_name (str): Name of the file to be created in Azure Blob Storage.
            azure_blob_url (str): The URL to the Azure Blob Storage account.
            sas_token (str): SAS token for authentication to the Azure Blob Storage.

        Returns:
            dict: The status or error message of the operation.
        """
        try:
            # Use the LoaderUtils class to load data from MySQL to CSV format
            return LoaderUtils.load_to_csv(
                MySQLConnector,  # Connector class for MySQL
                connection_string,  # Connection string for MySQL connection
                sql_query,  # SQL query to execute
                container_name,  # Azure Blob container name
                folder_path,  # Folder path in the Azure Blob container
                file_name,  # File name to be uploaded
                azure_blob_url,  # Azure Blob storage account URL
                sas_token  # SAS token for authentication
            )
        except Exception as e:
            # Handle any errors during the process and return an error message
            return ResponseHandler.error(message=f"Error: {str(e)}")