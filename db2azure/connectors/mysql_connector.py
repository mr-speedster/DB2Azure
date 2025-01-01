import pymysql

__all__ = ['MySQLConnector']

class MySQLConnector:
    """
    A utility class to connect to a MySQL database, execute queries, 
    fetch results, and manage the connection lifecycle using a context manager.
    """

    def __init__(self, connection_config):
        """
        Initialize the MySQLConnector with connection configuration.
        
        :param connection_config: A dictionary containing MySQL connection parameters 
                                  such as host, user, password, database, and port.
        """
        self.connection_config = connection_config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Enter the context manager, establishing the database connection.
        
        :return: The MySQLConnector instance.
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
        Establish a connection to the MySQL database and prepare the cursor.
        
        :raises pymysql.MySQLError: If the connection cannot be established.
        """
        self.connection = pymysql.connect(**self.connection_config)
        # Use a dictionary cursor to fetch rows as dictionaries
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def fetch_data(self, sql_query):
        """
        Execute a SQL query and fetch the results as a list of dictionaries.
        
        :param sql_query: The SQL query to execute.
        :return: A list of dictionaries where each dictionary represents a row,
                 with column names as keys.
        :raises pymysql.MySQLError: If the query execution fails.
        """
        if not self.connection or not self.cursor:
            self.connect()
        self.cursor.execute(sql_query)
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        """
        Close the database connection if it is open.
        
        :raises pymysql.MySQLError: If closing the connection fails.
        """
        if self.connection:
            self.connection.close()