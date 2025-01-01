class ResponseHandler:
    """
    A utility class to handle responses for file upload operations.
    It includes methods for successful uploads and error handling.
    """

    @staticmethod
    def upload_success(status, message, rows_uploaded, file_name, container_name, folder_path):
        """
        Handle successful upload response with the required details.

        Args:
            status (str): The status of the upload, typically "success".
            message (str): A message providing details about the successful upload.
            rows_uploaded (int): The number of rows successfully uploaded.
            file_name (str): The name of the uploaded file.
            container_name (str): The Azure Blob Storage container where the file was uploaded.
            folder_path (str): The folder path within the container where the file is stored.

        Returns:
            dict: A dictionary containing the status, message, and additional details of the upload.
        """
        return {
            "status": status,  # The status of the upload (e.g., "success").
            "message": message,  # A message providing details about the upload.
            "rows_uploaded": rows_uploaded,  # The number of rows uploaded.
            "file_name": file_name,  # The name of the uploaded file.
            "container_name": container_name,  # The Azure Blob container name.
            "folder_path": folder_path,  # The folder path within the container.
        }

    @staticmethod
    def error(message):
        """
        Handle error response when an issue occurs during the upload process.

        Args:
            message (str): A message explaining the error that occurred.

        Returns:
            dict: A dictionary containing the status "error" and the error message.
        """
        return {
            "status": "error",  # The status indicating an error occurred.
            "message": message,  # The error message explaining the issue.
        }