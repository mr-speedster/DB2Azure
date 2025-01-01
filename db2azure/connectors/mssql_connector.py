import pyodbc

__all__ = ['MSSQLConnector']

class MSSQLConnector:
    """
    A utility class to connect to an MSSQL database, execute queries, 
    fetch results, and manage the connection lifecycle using a context manager.
    """

    def __init__(self, connection_string):
        """
        Initialize the MSSQLConnector with a connection string.
        
        :param connection_string: The connection string for the MSSQL database.
        """
        self.connection_string = connection_string
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Enter the context manager, establishing the database connection.
        
        :return: The MSSQLConnector instance.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager, closing the database connection.
        
        :param exc_type: The exception type, if any.
        :param exc_value: The exception instance, if any.
        :param traceback: The traceback object, if any exception occurred.
        """
        self.close()

    def connect(self):
        """
        Establish a connection to the MSSQL database and create a cursor.
        
        :raises pyodbc.Error: If the connection cannot be established.
        """
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def fetch_data(self, sql_query):
        """
        Execute a SQL query and fetch the results as a list of dictionaries.
        
        :param sql_query: The SQL query to execute.
        :return: A list of dictionaries where each dictionary represents a row,
                 with column names as keys.
        :raises pyodbc.Error: If the query execution fails.
        """
        if not self.connection or not self.cursor:
            self.connect()
        self.cursor.execute(sql_query)
        columns = [column[0] for column in self.cursor.description]
        rows = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return rows

    def close(self):
        """
        Close the database connection if it is open.
        
        :raises pyodbc.Error: If closing the connection fails.
        """
        if self.connection:
            self.connection.close()