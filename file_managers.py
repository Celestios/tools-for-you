import csv
from typing import List, Callable, Any, Optional


class CSVTable:
    def __init__(self, filepath: str, fieldnames: Optional[List[str]] = None, dialect: str = 'excel'):
        """
        :param filepath: Path to the CSV file.
        :param fieldnames: Optional list of column headers. If provided,
                           writing operations will use these headers.
        :param dialect:    CSV dialect to use (default: 'excel').
        """
        self.filepath = filepath
        self.fieldnames = fieldnames
        self.dialect = dialect

    def read_all(self) -> List[List[str]]:
        """Read and return all rows (including header, if any)."""
        with open(self.filepath, mode='r', newline='') as f:
            reader = csv.reader(f, dialect=self.dialect)
            rows = [row for row in reader]
        return rows

    def write_all(self, rows: List[List[Any]]) -> None:
        """
        Overwrite the CSV file with the provided rows.
        :param rows: List of rows, where each row is a list of values.
        """
        with open(self.filepath, mode='w', newline='') as f:
            writer = csv.writer(f, dialect=self.dialect)
            writer.writerows(rows)

    def append_row(self, row: List[Any]) -> None:
        """
        Append a single row to the CSV file.
        :param row: List of values for the new row.
        """
        with open(self.filepath, mode='a', newline='') as f:
            writer = csv.writer(f, dialect=self.dialect)
            writer.writerow(row)

    def delete_where(self, predicate: Callable[[List[str]], bool]) -> None:
        """
        Delete rows for which predicate(row) is True.
        :param predicate: A function that takes a row and returns True if
                          that row should be removed.
        """
        # Read current data
        rows = self.read_all()
        # Filter out rows matching the predicate
        filtered = [row for row in rows if not predicate(row)]
        # Rewrite file with filtered data
        self.write_all(filtered)
