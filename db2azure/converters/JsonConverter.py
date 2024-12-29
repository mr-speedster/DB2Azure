from db2azure.converters import ConverterBase
import json

class JsonConverter(ConverterBase):
    
    @staticmethod
    def convert(rows, columns):
        rows = [dict(zip(columns, row)) for row in rows]
        json_data = json.dumps(rows, indent=4)
        return json_data