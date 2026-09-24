"""
CSV Reader Module for Compliance Test.

Reads CSV files from the project workspace and converts them into
structured, type-safe data structures suitable for downstream processing.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure logging for this module.
logger = logging.getLogger("compliance_test.csv_reader")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


class CSVReader:
    """Reads CSV files and converts them into structured data dictionaries."""

    def __init__(self, filepath: str) -> None:
        """Initialize the CSV reader with a file path.

        Args:
            filepath: Path to the CSV file to read.
        """
        self.filepath: str = filepath
        self.path: Path = Path(filepath)

    def read(self) -> List[Dict[str, Any]]:
        """Read the CSV file and return each row as a dictionary.

        Returns:
            A list of dictionaries, where each dictionary represents one
            row from the CSV file with keys matching column headers.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
            ValueError: If the CSV file is empty or malformed.
        """
        logger.info("Reading CSV file: %s", self.filepath)

        if not self.path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.filepath}")

        with self.path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            rows: List[Dict[str, Any]] = []

            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no headers.")

            for row in reader:
                rows.append(row)

        logger.info("Successfully read %d rows from %s", len(rows), self.filepath)
        return rows
