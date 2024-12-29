from db2azure.readers import ReaderBase
import pyodbc

class SqlReader(ReaderBase):

    def __init__(self, connection_string, *args, **kwargs):
        '''requires connection_string parameter.'''
        self.connection_string = connection_string
    
    def read(self, query):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return rows, columns