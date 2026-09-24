"""
CSV Processor Module for Compliance Test.

Processes type-safe CSV data from the CSVParser into transformed,
filtered, and aggregated records suitable for validation and reporting.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from typing import List, Dict, Any

# Configure logging for this module.
logger = logging.getLogger("compliance_test.csv_processor")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


class CSVProcessor:
    """Processes parsed CSV data for validation and reporting."""

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        """Initialize the CSV processor with parsed data.

        Args:
            data: Type-safe dictionary list from the CSVParser.
        """
        self.data: List[Dict[str, Any]] = data

    def process(self) -> List[Dict[str, Any]]:
        """Process parsed data with filtering and transformation.

        Performs the following steps on each record:
        1. Filters out records missing required fields.
        2. Normalizes field values while preserving type-safe values
           set by the parser (int, float, str, bool, None).
        3. Aggregates valid records for downstream validation.

        Returns:
            A list of processed, type-preserving records.
        """
        logger.info("Processing %d parsed records.", len(self.data))

        if not self.data:
            logger.warning("No parsed data to process; returning empty list.")
            return []

        required_fields = ("id", "category", "value")
        processed: List[Dict[str, Any]] = []

        for record in self.data:
            # Filter: skip records missing required fields.
            if any(record.get(field) is None for field in required_fields):
                logger.info("Skipping record missing required fields: %s",
                             _record_identifier(record))
                continue

            # Transform: preserve type-safe values from the parser.
            # Only normalize empty strings to None and ensure types are correct.
            transformed: Dict[str, Any] = {}

            for field in record.keys():
                value = record.get(field, None)

                # Preserve the type set by the parser.
                # Empty strings become None; other values remain unchanged.
                if value is None or value == "":
                    transformed[field] = None
                else:
                    # Ensure string types stay strings.
                    if not isinstance(value, (int, float, bool)):
                        transformed[field] = str(value)
                    else:
                        transformed[field] = value

            # Aggregate: mark as processed with type info.
            transformed["processed"] = True
            transformed["type_checked"] = True

            processed.append(transformed)

        logger.info("Processed %d of %d records.", len(processed), len(self.data))
        return processed


def _record_identifier(record: Dict[str, Any]) -> str:
    """Generate a short identifier string for a record.

    Args:
        record: The record dictionary to identify.

    Returns:
        A string identifier combining key fields.
    """
    identifier = f"{record.get('id')}:{record.get('category')}"
    return identifier
