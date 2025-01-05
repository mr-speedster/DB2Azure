import logging
from db2azure.helpers.storage import AzureBlobHelper
from db2azure.utils.file_utils import FileUtils
from db2azure.helpers.response import ResponseHandler

__all__ = ['LoaderUtils']

# Initialize logger
logger = logging.getLogger(__name__)

class LoaderUtils:
    """
    Utility class for loading data from a database and uploading it to Azure Blob Storage.
    Provides methods to handle JSON and CSV formats.
    """

    @staticmethod
    def _fetch_data(connector_class, connection_string: str, sql_query: str):
        """
        Fetch data from a database using the provided connector.

        :param connector_class: The database connector class (e.g., MSSQLConnector, MySQLConnector).
        :param connection_string: Database connection string.
        :param sql_query: SQL query to execute.
        :return: List of rows fetched from the database.
        """
        with connector_class(connection_string) as db_connector:
            return db_connector.fetch_data(sql_query)

    @staticmethod
    def _upload_to_blob(data, azure_config: dict, row_count: int):
        """
        Upload data to Azure Blob Storage.

        :param data: Data to be uploaded (in JSON or CSV format).
        :param azure_config: Configuration for Azure Blob Storage.
        :param row_count: Number of rows being uploaded (used for metadata).
        :return: Status of the upload operation.
        """
        return AzureBlobHelper.upload_to_blob_storage(
            azure_config.get('container_name'),
            azure_config.get('folder_path'),
            azure_config.get('file_name'),
            data,
            azure_config.get('azure_blob_url'),
            azure_config.get('sas_token'),
            row_count,
        )

    @staticmethod
    def load_to_json(connector_class, connection_string: str, sql_query: str, azure_config: dict):
        """
        Fetch data from the database and upload it to Azure Blob Storage in JSON format.

        :param connector_class: The database connector class.
        :param connection_string: Database connection string.
        :param sql_query: SQL query to execute.
        :param azure_config: Configuration for Azure Blob Storage.
        :return: Status of the upload operation.
        """
        try:
            rows = LoaderUtils._fetch_data(connector_class, connection_string, sql_query)
            if not rows:
                logger.warning("No data fetched from the database.")
                return ResponseHandler.error("No data to upload.")

            json_data = FileUtils.to_json(rows)
            logger.info(f"Fetched {len(rows)} rows and converted them to JSON format.")

            status = LoaderUtils._upload_to_blob(json_data, azure_config, len(rows))
            logger.info("JSON data successfully uploaded to Azure Blob Storage.")
            return status

        except Exception as e:
            logger.error("An error occurred during JSON upload.", exc_info=True)
            return ResponseHandler.error(message=f"Error: {str(e)}")

    @staticmethod
    def load_to_csv(connector_class, connection_string: str, sql_query: str, azure_config: dict):
        """
        Fetch data from the database and upload it to Azure Blob Storage in CSV format.

        :param connector_class: The database connector class.
        :param connection_string: Database connection string.
        :param sql_query: SQL query to execute.
        :param azure_config: Configuration for Azure Blob Storage.
        :return: Status of the upload operation.
        """
        try:
            rows = LoaderUtils._fetch_data(connector_class, connection_string, sql_query)
            if not rows:
                logger.warning("No data fetched from the database.")
                return ResponseHandler.error("No data to upload.")

            csv_data = FileUtils.to_csv(rows)
            logger.info(f"Fetched {len(rows)} rows and converted them to CSV format.")

            status = LoaderUtils._upload_to_blob(csv_data, azure_config, len(rows))
            logger.info("CSV data successfully uploaded to Azure Blob Storage.")
            return status

        except Exception as e:
            logger.error("An error occurred during CSV upload.", exc_info=True)
            return ResponseHandler.error(message=f"Error: {str(e)}")