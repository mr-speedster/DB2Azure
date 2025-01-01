from azure.storage.blob import BlobClient, BlobServiceClient
from azure.core.exceptions import AzureError
from db2azure.helpers.response import ResponseHandler

__all__ = ['AzureBlobHelper']

class AzureBlobHelper:
    """
    A helper class to interact with Azure Blob Storage, specifically for uploading data to a blob.
    """

    @staticmethod
    def upload_to_blob_storage(container_name, folder_path, file_name, data, azure_blob_url, sas_token, rows_uploaded):
        """
        Upload data to Azure Blob Storage. If an exception occurs, return the error response from ResponseHandler.

        Args:
            container_name (str): The name of the Azure Blob Storage container.
            folder_path (str): The folder path within the container where the file will be uploaded.
            file_name (str): The name of the file to upload.
            data (str): The data to be uploaded (e.g., JSON or CSV).
            azure_blob_url (str): The URL to the Azure Blob Storage account.
            sas_token (str): The SAS token for accessing Azure Blob Storage.
            rows_uploaded (int): The number of rows that were uploaded.

        Returns:
            dict: A dictionary containing the upload status, message, and other details.
        """
        try:
            # Ensure folder path ends with '/'
            if not folder_path.endswith('/'):
                folder_path += '/'

            # Create BlobClient with SAS token
            blob_url = f"{azure_blob_url}/{container_name}/{folder_path}{file_name}"
            blob_client = BlobClient.from_blob_url(blob_url, credential=sas_token)
            
            # Upload data to Azure Blob Storage, overwriting if necessary
            blob_client.upload_blob(data, overwrite=True)

            # Use ResponseHandler to generate the success response
            return ResponseHandler.upload_success(
                status="success",
                message=f"Data successfully saved to Azure Storage at {folder_path + file_name}",
                rows_uploaded=rows_uploaded,
                file_name=file_name,
                container_name=container_name,
                folder_path=folder_path
            )
        
        except AzureError as e:
            # Handle any Azure-specific errors (e.g., network issues, permission issues)
            return ResponseHandler.error(message=f"Azure Error: {str(e)}")
        
        except Exception as e:
            # Handle any general exceptions that might occur
            return ResponseHandler.error(message=f"General Error: {str(e)}")