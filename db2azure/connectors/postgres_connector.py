import psycopg

__all__ = ['PostgresConnector']

class PostgresConnector:
    """
    A utility class to connect to a PostgreSQL database, execute queries, 
    fetch results, and manage the connection lifecycle using a context manager.
    """

    def __init__(self, connection_params):
        """
        Initialize the PostgresConnector with connection parameters.
        
        :param connection_params: A dictionary containing PostgreSQL connection parameters 
                                  such as host, database, user, password, and port.
        """
        self.connection_params = connection_params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Enter the context manager, establishing the database connection.
        
        :return: The PostgresConnector instance.
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
        Establish a connection to the PostgreSQL database and prepare the cursor.
        
        :raises psycopg.OperationalError: If the connection cannot be established.
        """
        self.connection = psycopg.connect(**self.connection_params)
        # Create a standard cursor for executing queries
        self.cursor = self.connection.cursor()

    def fetch_data(self, sql_query):
        """
        Execute a SQL query and fetch the results as a list of dictionaries.
        
        :param sql_query: The SQL query to execute.
        :return: A list of dictionaries where each dictionary represents a row,
                 with column names as keys.
        :raises psycopg.DatabaseError: If the query execution fails.
        """
        if not self.connection or not self.cursor:
            self.connect()
        self.cursor.execute(sql_query)
        # Fetch column names and row data, converting them into dictionaries
        columns = [desc[0] for desc in self.cursor.description]
        rows = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return rows

    def close(self):
        """
        Close the database connection if it is open.
        
        :raises psycopg.OperationalError: If closing the connection fails.
        """
        if self.connection:
            self.connection.close()