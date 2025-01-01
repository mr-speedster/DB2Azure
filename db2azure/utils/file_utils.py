import json
import csv
from io import StringIO

__all__ = ['FileUtils']

class FileUtils:
    """
    A utility class for converting data to different file formats, such as JSON and CSV.
    """

    @staticmethod
    def to_json(data):
        """
        Convert data to JSON format.

        Args:
            data (list or dict): The data to be converted to JSON format.

        Returns:
            str: The data in JSON format as a string, indented for readability.
        """
        return json.dumps(data, indent=4)

    @staticmethod
    def to_csv(data):
        """
        Convert data to CSV format.

        Args:
            data (list of dict): The data to be converted to CSV format. Each item in the list should be a dictionary.

        Returns:
            str: The data in CSV format as a string.
        """
        output = StringIO()  # Create an in-memory string buffer to hold CSV data
        if len(data) > 0:  # Check if there is any data to write
            writer = csv.DictWriter(output, fieldnames=data[0].keys())  # Create a CSV writer object
            writer.writeheader()  # Write the header row (field names)
            writer.writerows(data)  # Write the data rows
            output.seek(0)  # Rewind the output buffer to the beginning
        return output.getvalue()  # Return the CSV data as a string