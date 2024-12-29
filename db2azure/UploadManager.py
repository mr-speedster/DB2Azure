from db2azure.converters import ConverterBase
from db2azure.readers import ReaderBase
from azure.storage.blob import BlobClient
from os import sep

class UploadManager:

    def __init__(self, reader: ReaderBase, converter: ConverterBase, azure_configs: dict):
        self.reader = reader
        self.converter = converter
        self.azure_blob_url = azure_configs['azure_blob_url']
        self.container_name = azure_configs['container_name']
        self.folder_path = azure_configs['folder_path']
        self.file_name = azure_configs['file_name']
        self.sas_token = azure_configs['sas_token']

        # validations
        if not path.endswith(sep):
            path += sep

    def read(self, sql_query):
        return self.reader.read(sql_query)
    
    def convert(self, rows, columns):
        return self.converter.convert(rows, columns)

    def upload(self, data):
        blob_url = f'{self.azure_blob_url}/{self.container_name}/{self.folder_path}{self.file_name}'
        blob_client = BlobClient.from_blob_url(blob_url, credential=self.sas_token)
        blob_client.upload_blob(data, overwrite=True)
    
    def push_up(self, sql_query):
        try:
            rows, columns = self.read(sql_query)
            data = self.convert(rows, columns)
            self.upload(data)
            return {
                "status": "success",
                "message": f"Data successfully saved to Azure Storage at {self.folder_path + self.file_name}",
                "rows_uploaded": len(rows),
                "file_name": self.file_name,
                "container_name": self.container_name,
                "folder_path": self.folder_path,
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
