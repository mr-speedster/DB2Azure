from db2azure.helpers.storage import AzureBlobHelper
from db2azure.utils.file_utils import FileUtils
from db2azure.helpers.response import ResponseHandler

__all__ = ['LoaderUtils']

class LoaderUtils:
    @staticmethod
    def load_to_json(connector_class, connection_params, sql_query, container_name, folder_path, file_name, azure_blob_url, sas_token):
        """
        Fetch data from the database using a generic connector and upload it to Azure Blob Storage in JSON format.
        
        :param connector_class: The database connector class (e.g., MSSQLConnector, MySQLConnector).
        :param connection_params: Parameters required to establish a connection.
        :param sql_query: The SQL query to execute.
        :param container_name: The name of the Azure Blob container.
        :param folder_path: The folder path in the container.
        :param file_name: The name of the file to upload.
        :param azure_blob_url: The URL of the Azure Blob Storage account.
        :param sas_token: The SAS token for authentication.
        :return: Status of the upload operation.
        """
        try:
            # Use the database connector as a context manager
            with connector_class(connection_params) as db_connector:
                # Execute the query and fetch the rows
                rows = db_connector.fetch_data(sql_query)

            # Convert rows to JSON format
            json_data = FileUtils.to_json(rows)

            # Upload the data to Azure Blob Storage
            status = AzureBlobHelper.upload_to_blob_storage(
                container_name, folder_path, file_name, json_data, azure_blob_url, sas_token, len(rows)
            )

            return status

        except Exception as e:
            return ResponseHandler.error(message=f"Error: {str(e)}")

    @staticmethod
    def load_to_csv(connector_class, connection_params, sql_query, container_name, folder_path, file_name, azure_blob_url, sas_token):
        """
        Fetch data from the database using a generic connector and upload it to Azure Blob Storage in CSV format.
        
        :param connector_class: The database connector class (e.g., MSSQLConnector, MySQLConnector).
        :param connection_params: Parameters required to establish a connection.
        :param sql_query: The SQL query to execute.
        :param container_name: The name of the Azure Blob container.
        :param folder_path: The folder path in the container.
        :param file_name: The name of the file to upload.
        :param azure_blob_url: The URL of the Azure Blob Storage account.
        :param sas_token: The SAS token for authentication.
        :return: Status of the upload operation.
        """
        try:
            # Use the database connector as a context manager
            with connector_class(connection_params) as db_connector:
                # Execute the query and fetch the rows
                rows = db_connector.fetch_data(sql_query)

            # Convert rows to CSV format
            csv_data = FileUtils.to_csv(rows)

            # Upload the data to Azure Blob Storage
            status = AzureBlobHelper.upload_to_blob_storage(
                container_name, folder_path, file_name, csv_data, azure_blob_url, sas_token, len(rows)
            )

            return status

        except Exception as e:
            return ResponseHandler.error(message=f"Error: {str(e)}")