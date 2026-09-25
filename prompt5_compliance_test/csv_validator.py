"""
CSV Validator Module for Compliance Test.

Validates processed CSV data from the CSVProcessor to ensure data
consistency, type correctness, and integrity. Returns detailed
validation results for downstream reporting.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from typing import List, Dict, Any

# Configure logging for this module.
logger = logging.getLogger("prompt5_compliance_test.csv_validator")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


class CSVValidator:
    """Validates processed CSV data for consistency and integrity."""

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        """Initialize the CSV validator with processed data.

        Args:
            data: Processed dictionary list from the CSVProcessor.
        """
        self.data: List[Dict[str, Any]] = data

    def validate(self) -> List[Dict[str, Any]]:
        """Validate each record and return detailed validation results.

        Each record is checked for:
        1. Required field presence.
        2. Field type correctness.
        3. Value consistency.

        Returns:
            A list of dictionaries with validation status and details.
        """
        logger.info("Validating %d processed records.", len(self.data))

        results: List[Dict[str, Any]] = []

        if not self.data:
            logger.warning("No records to validate; returning empty results.")
            return results

        for record in self.data:
            findings: List[Dict[str, Any]] = []
            all_valid = True

            # Check required fields.
            required_fields = ("id", "category", "value")
            for field in required_fields:
                if field not in record or record[field] is None:
                    findings.append({
                        "field": field,
                        "status": "invalid",
                        "detail": "Missing required field.",
                    })
                    all_valid = False

            # Check type correctness for numeric fields.
            if "value" in record and record["value"] is not None:
                if not isinstance(record["value"], (int, float)):
                    findings.append({
                        "field": "value",
                        "status": "invalid",
                        "detail": "Value is not numeric.",
                    })
                    all_valid = False

            # Check consistency: category should be non-empty string.
            if "category" in record and record["category"] is not None:
                if not isinstance(record["category"], str) or record["category"] == "":
                    findings.append({
                        "field": "category",
                        "status": "invalid",
                        "detail": "Category must be a non-empty string.",
                    })
                    all_valid = False

            status = "valid" if all_valid else "invalid"
            findings.append({
                "field": "overall",
                "status": status,
                "detail": _findings_summary(findings),
            })

            results.append({
                "id": record.get("id"),
                "category": record.get("category"),
                "value": record.get("value"),
                "status": status,
                "findings": findings,
            })

            if not all_valid:
                logger.warning("Record %s failed validation: %s",
                               record.get("id"), _findings_summary(findings))

        logger.info("Validated %d records. %d valid, %d invalid.",
                     len(results),
                     sum(1 for r in results if r["status"] == "valid"),
                     sum(1 for r in results if r["status"] == "invalid"))
        return results


def _findings_summary(findings: List[Dict[str, Any]]) -> str:
    """Summarize validation findings into a compact string.

    Args:
        findings: List of finding dictionaries.

    Returns:
        A summary string describing the findings.
    """
    if not findings:
        return "No issues found."

    details = "; ".join(f"{f['field']}: {f['detail']}" for f in findings)
    return f"{details}"
