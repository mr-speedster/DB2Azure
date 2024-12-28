import json
import csv
from io import StringIO
from azure.storage.blob import BlobClient
import psycopg
from os import sep

class PostgreLoader:

    @staticmethod
    def connect_and_query(connection_params, sql_query):
        with psycopg.connect(**connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
        return rows, columns

    @staticmethod
    def format_path(path):
        if not path.endswith(sep):
            path += sep
        return path

    @staticmethod
    def create_blob_client(azure_blob_url, container_name, folder_path, file_name, sas_token):
        blob_url = f'{azure_blob_url}/{container_name}/{folder_path}{file_name}'
        blob_client = BlobClient.from_blob_url(blob_url, credential=sas_token)

    @staticmethod
    def load_to_json(sql_query, connection_params, container_name, folder_path, file_name, azure_blob_url, sas_token):
        try:
            rows, columns = PostgreLoader.connect_and_query(connection_params, sql_query)
            rows = [dict(zip(columns, row)) for row in rows]

            # Convert rows to JSON
            json_data = json.dumps(rows, indent=4)

            folder_path = PostgreLoader.format_path(folder_path)

            # Upload to Azure Blob Storage
            blob_client = PostgreLoader.create_blob_client(azure_blob_url, container_name, folder_path, file_name, sas_token)
            blob_client.upload_blob(json_data, overwrite=True)

            # Return status
            return {
                "status": "success",
                "message": f"Data successfully saved to Azure Storage at {folder_path + file_name}",
                "rows_uploaded": len(rows),
                "file_name": file_name,
                "container_name": container_name,
                "folder_path": folder_path,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    def load_to_csv(sql_query, connection_params, container_name, folder_path, file_name, azure_blob_url, sas_token):
        try:
            rows, columns = PostgreLoader.connect_and_query(connection_params, sql_query)

            # Create CSV content
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(columns)
            writer.writerows(rows)
            output.seek(0)
            csv_data = output.getvalue()

            folder_path = PostgreLoader.format_path(folder_path)

            # Upload to Azure Blob Storage
            blob_client = PostgreLoader.create_blob_client(azure_blob_url, container_name, folder_path, file_name, sas_token)
            blob_client.upload_blob(csv_data, overwrite=True)
            
            # Return status
            return {
                "status": "success",
                "message": f"Data successfully saved to Azure Storage at {folder_path + file_name}",
                "rows_uploaded": len(rows),
                "file_name": file_name,
                "container_name": container_name,
                "folder_path": folder_path,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }