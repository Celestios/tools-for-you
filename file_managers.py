import csv
from pathlib import Path
from typing import List, Any, Callable, Union


class CSVTable:
    def __init__(self, filepath: str, headers: List[str]):
        self.path = Path(filepath if filepath.endswith('.csv') else f"{filepath}.csv")
        self.headers = headers
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize the file with headers if it doesn't exist
        if not self.path.exists():
            self._write_rows([], write_header=True)

        # Load the data into memory
        self.data = self._load_data()

    def _load_data(self):
        """Load data from the CSV file into memory."""
        with self.path.open('r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return list(reader)

    def _write_rows(self, rows: List[List[Any]], write_header: bool = False):
        """Write rows to the CSV file."""
        with self.path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(self.headers)
            writer.writerows(rows)

    def read_row(self, index: int) -> Union[List[Any], None]:
        """Read a single row by index."""
        if 0 <= index < len(self.data):
            return self.data[index]
        return None

    def add_row(self, row: List[Any]):
        """Write a single row to the CSV file and save changes."""
        self.data.append(row)
        self._write_rows(self.data)

    def delete_rows(self, condition: Callable[[List[Any]], bool]):
        """Delete rows based on a condition."""
        self.data = [row for row in self.data if not condition(row)]
        self._write_rows(self.data)

    def __repr__(self):
        return f"<CSVTable path={self.path!r} rows={len(self.data)}>"
