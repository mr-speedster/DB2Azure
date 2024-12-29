from db2azure.converters import ConverterBase
import csv
from io import StringIO

class CsvConverter(ConverterBase):
    
    @staticmethod
    def convert(rows, columns):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(rows)
        output.seek(0)
        csv_data = output.getvalue()
        return csv_data