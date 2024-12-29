from db2azure.readers import ReaderBase
import psycopg

class PostgreReader(ReaderBase):

    def __init__(self, connection_params):
        '''requires a dictionary of psycopg connection params.'''
        self.connection_params = connection_params
    
    def read(self, query):
        with psycopg.connect(**self.connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
        return rows, columns