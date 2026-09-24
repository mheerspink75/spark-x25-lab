"""
CSV Parser Module for Compliance Test.

Parses raw CSV data from the CSVReader into structured, type-safe
dictionaries with validated and type-converted values. Handles
missing values, type conversion, and edge cases consistently.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from typing import List, Dict, Any, Tuple

# Configure logging for this module.
logger = logging.getLogger("compliance_test.csv_parser")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


class CSVParser:
    """Parses raw CSV data into structured, type-safe records."""

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        """Initialize the CSV parser with raw data.

        Args:
            data: Raw dictionary list from the CSVReader.
        """
        self.data: List[Dict[str, Any]] = data

    def parse(self) -> List[Dict[str, Any]]:
        """Parse raw data into type-safe structured records.

        Each record has all values converted to their appropriate type:
        numeric strings converted to int/float where possible,
        boolean strings converted to bool, and missing values set to None.

        Returns:
            A list of dictionaries with type-converted values.
        """
        logger.info("Parsing %d records with %d columns", len(self.data),
                     len(self.data[0]) if self.data else 0)

        if not self.data:
            logger.warning("No data to parse; returning empty list.")
            return []

        headers: List[str] = list(self.data[0].keys())
        parsed: List[Dict[str, Any]] = []

        for record in self.data:
            parsed_record: Dict[str, Any] = {}
            for header in headers:
                raw_value = record.get(header, "")

                # Skip missing values.
                if raw_value is None or raw_value == "":
                    parsed_record[header] = None
                    continue

                # Convert numeric strings to int or float.
                if raw_value.isdigit():
                    parsed_record[header] = int(raw_value)
                elif _is_float(raw_value):
                    parsed_record[header] = float(raw_value)
                # Convert boolean strings.
                elif raw_value.lower() in ("true", "1", "yes", "y", "on"):
                    parsed_record[header] = True
                elif raw_value.lower() in ("false", "0", "no", "n", "off"):
                    parsed_record[header] = False
                else:
                    parsed_record[header] = str(raw_value)

            parsed.append(parsed_record)

        logger.info("Parsed %d records into type-safe structures.", len(parsed))
        return parsed


def _is_float(value: str) -> bool:
    """Check if a string represents a valid float number.

    Args:
        value: The string to check.

    Returns:
        True if the string represents a float, False otherwise.
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
