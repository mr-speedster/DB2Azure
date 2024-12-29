<picture align="center">
  <source media="(prefers-color-scheme: dark)" srcset="https://ik.imagekit.io/isyob5kdk4y/DB2AzureLogo_i2TWk-13b?updatedAt=1734874553185">
  <img alt="DB2Azure Logo" src="https://ik.imagekit.io/isyob5kdk4y/DB2AzureLogo_i2TWk-13b?updatedAt=1734874553185">
</picture>

# DB2Azure

DB2Azure is a Python package designed to streamline the process of loading data from SQL Server (MSSQL) and PostgreSQL databases to Azure Blob Storage in both JSON and CSV formats. This package simplifies the data extraction and upload processes with separate modules for SQL Server (`SQLLoader`) and PostgreSQL (`PostgreLoader`), enabling efficient and seamless integration with Azure Blob Storage.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
  - [Setup Reader](#setup-reader)
  - [Setup UploadManager](#setup-uploadmanager)
  - [Methods and Operation](#methods-and-operation)
- [Error Handling](#error-handling)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Description

DB2Azure helps automate the process of extracting data from SQL Server and PostgreSQL databases and uploading it directly to Azure Blob Storage in either JSON or CSV format.  
More Data Sources and Data Formats will be available in upcoming releases.

The UploadManager is the main utility of the package.  
The user needs to initialize the UploadManager with the desired configurations before pushing content.  
This involves setting up a desired Reader and Converter.  
Users would only need to call the `push_up` function of the UploadManager. In case fine-grain control is desired, the component functions could be used.  

The package consists of two sub-modules, `readers` and `converters`.  
Readers contain modules to read data from various Data Sources.  
Converters help convert the data to the desired format.
The UploadManager can be configured with a mix of any data source with any data converter to create the desired configuration.

### Key Features

- **Extendable Server Support**: The data flow is architected in a way that any Server can be configured to be read and used.
  - **SQL Server Support**: Extracts data from Microsoft SQL Server databases using `pyodbc`.
  - **PostgreSQL Support**: Extracts data from PostgreSQL databases using `psycopg`.
- **Extendable Data Type Support**: The data can be formatted into configurable types currently limitted to JSON and CSV.
- **Azure Blob Storage Upload**: Uploads data to Azure Blob Storage using the `azure-storage-blob`.
- **Flexibility**: Allows customization of folder path, file name, and blob URL.  
  Allows easy addition of other data types as well as data sources.
- **Error Handling**: Provides detailed error messages in case of failures.

## Installation

To install the `DB2Azure` package, use the following `pip` command:

```bash
pip install DB2Azure
```

Alternatively, clone the repository and install it manually:

```bash
git clone https://github.com/mr-speedster/DB2Azure.git
cd DB2Azure
pip install .
```

## Usage

### Setup Reader

Import reader from the available readers in the reader sub-module and initialize it.  
Readers are expected to have a single parameter that would contain any required configurations.  

- **SQL Server**: Use the `connection_string` parameter to configure the connection to your SQL Server.
- **PostgreSQL**: Use the `connection_params` dictionary to configure the connection to your PostgreSQL database.

```python
from db2azure.readers import SqlReader, PostgreReader

# SQL Server
sql_conn = r"Driver=<driver>;Server=<server_name>;Database=<database>;Trusted_Connection=yes;"
sql_reader = SqlReader(sql_conn)

# Postgre Server
connection_params = {
    "host": "localhost",      # e.g., "localhost" or an IP address
    "port": "5432",           # default PostgreSQL port
    "dbname": "SampleDB",     # name of the database
    "user": "*****",          # PostgreSQL username
    "password": "*****"       # PostgreSQL password
}
psg_reader = PostgreReader(connection_params)
```

### Setup UploadManager

Import the UploadManager and initialize it with the Azure configurations.  
The converters are available in the converers sub-module and need not be instantiated.

- **Azure Blob Storage**: Provide `container_name`, `folder_path`, `file_name`, `azure_blob_url`, and `sas_token` to specify where and how the data should be uploaded to Azure Blob Storage.

```python
from db2azure.converters import JsonConverter, CsvConverter
from db2azure import UploadManager

azure_configs = {
  'azure_blob_url' = 'https://your_account_name.blob.core.windows.net'
  'container_name' = 'your_container'
  'folder_path' = 'your_folder'
  'file_name' = 'your_file.json'
  'sas_token' = 'your_sas_token'
}

# setup UploadManager
uploader = UploadManager(reader, JsonConverter, azure_configs)
uploader = UploadManager(reader, CsvConverter, azuer_configs)
```

### Methods and Operation

```python
query = 'SELECT * FROM x'

# push data in one go
uploader.push_up(query)

# step by step workflow for fine-grain control
rows, columns = uploader.read(query)
data = uploader.convert(rows, columns)
result = uploader.upload(data)
```

The UploadManager consists of the following methods:

- `push_up(query: str)`  
  Perhaps the only one you'll need.  
  The push_up method requires a string parameter, `query`. It makes use of the UploadManager configurations to read data using the query provided, convert the data using the configured converter and finally push it to Azure Blob Storage.  
  The push_up method makes use of the following methods to perform the operation. A user can use these methods to assert control over the operations if required.  
- `read(query: str)`  
  The read method requires a string parameter, `query`.  
  It makes use of the Reader configurations to read data using the query provided and will return a double of rows and columns.  
- `convert(rows, columns)`  
  The convert method makes use of the values returned by the read method and converts it into the desired format.  
  It returns a data object which can be sent to Azure.
- `upload(data)`  
  The upload method initializes a blob_client from the configurations available and uses this client to push the data.  
  It finally returns a dict that contains a report with the following keys: status, message, rows_uploaded, file_name, container_name, folder_path.  

## Error Handling

If any error occurs during the data extraction or upload process, the methods will return an error response containing:

- **`status`**: Always `error`.
- **`message`**: The error message describing the issue.

Example error response:

```json
{
  "status": "error",
  "message": "Connection failed: 'Your error message here'"
}

```

## License

DB2Azure is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

We welcome contributions! Feel free to open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- **pyodbc**: A Python DB API 2.0 interface for ODBC databases, used for connecting to SQL Server.
- **psycopg**: A PostgreSQL database adapter for Python, used for connecting to PostgreSQL.
- **azure-storage-blob**: Azure SDK for Python, used for uploading files to Azure Blob Storage.
