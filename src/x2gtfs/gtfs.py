# feed_writer.py
from dataclasses import fields, is_dataclass
from typing import Type, List, Any
import csv
from io import StringIO
from zipfile import ZipFile
import os

class Feed:
    """
    Generic GTFS Feed writer for dataclass objects.
    
    Usage:
        feed = Feed()
        feed.add_data("stops.txt", list_of_stop_dataclasses)
        feed.add_data("routes.txt", list_of_route_dataclasses)
        feed.write("gtfs_feed.zip")
    """
    def __init__(self):
        # Dictionary mapping filename -> list of dataclass objects
        self._data_files: dict[str, List[Any]] = {}

    def add_data(self, filename: str, data_list: List[Any]) -> None:
        """
        Add a list of dataclass objects to be written to a CSV file.

        Args:
            filename: Name of the CSV file (e.g., "stops.txt")
            data_list: List of dataclass instances
        """
        if not data_list:
            raise ValueError(f"No data provided for file {filename}.")
        if not is_dataclass(data_list[0]):
            raise TypeError(f"Objects in list for {filename} must be dataclass instances.")

        # Store the list keyed by filename
        self._data_files[filename] = data_list

    def write(self, zip_filename: str) -> None:
        """
        Write all added data to CSV files and package them into a ZIP file.

        Args:
            zip_filename: Name of the output ZIP file
        """
        with ZipFile(zip_filename, "w") as zipf:
            for filename, data_list in self._data_files.items():
                if not data_list:
                    continue  # skip empty lists

                # Create CSV in memory
                output = StringIO()
                writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

                # Extract headers from dataclass fields
                headers = [f.name for f in fields(data_list[0])]
                writer.writerow(headers)

                # Write rows
                for obj in data_list:
                    row = [getattr(obj, f) for f in headers]
                    writer.writerow(row)

                # Write CSV into the ZIP
                zipf.writestr(filename, output.getvalue())
                output.close()
