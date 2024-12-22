import json
import csv
from io import StringIO
from azure.storage.blob import BlobClient
import psycopg

class PostgreLoader:
    @staticmethod
    def load_to_json(sql_query, connection_params, container_name, folder_path, file_name, azure_blob_url, sas_token):
        try:
            # Connect to PostgreSQL and execute the query
            with psycopg.connect(**connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_query)
                    columns = [desc[0] for desc in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Convert rows to JSON
            json_data = json.dumps(rows, indent=4)

            # Ensure folder path ends with '/'
            if not folder_path.endswith('/'):
                folder_path += '/'

            # Create BlobClient with SAS token
            blob_url = f"{azure_blob_url}/{container_name}/{folder_path}{file_name}"
            blob_client = BlobClient.from_blob_url(blob_url, credential=sas_token)
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
            # Connect to PostgreSQL and execute the query
            with psycopg.connect(**connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_query)
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()

            # Create CSV content
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(columns)
            writer.writerows(rows)
            output.seek(0)

            # Ensure folder path ends with '/'
            if not folder_path.endswith('/'):
                folder_path += '/'

            # Construct the Blob URL
            blob_url = f"{azure_blob_url}/{container_name}/{folder_path}{file_name}"
            
            # Create BlobClient with SAS token
            blob_client = BlobClient.from_blob_url(blob_url, credential=sas_token)
            
            # Upload CSV content to Azure Blob Storage
            blob_client.upload_blob(output.getvalue(), overwrite=True)
            
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