"""
CSV Reporter Module for Compliance Test.

Generates reports and summary statistics from validated CSV data
from the CSVValidator. Produces compliance audit output based on
the validation results.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from typing import List, Dict, Any

# Configure logging for this module.
logger = logging.getLogger("prompt5_compliance_test.csv_reporter")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


class CSVReporter:
    """Generates reports and summary statistics from validated data."""

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        """Initialize the CSV reporter with validation results.

        Args:
            data: Validation result list from the CSVValidator.
        """
        self.data: List[Dict[str, Any]] = data

    def report(self) -> Dict[str, Any]:
        """Generate a compliance report with summary and statistics.

        Returns:
            A dictionary containing the compliance report with
            summary statistics, counts, and overall status.
        """
        logger.info("Generating compliance report for %d records.", len(self.data))

        valid_count = sum(1 for r in self.data if r["status"] == "valid")
        invalid_count = sum(1 for r in self.data if r["status"] == "invalid")

        # Count by category.
        category_counts: Dict[str, int] = {}
        for record in self.data:
            category = record.get("category", "unknown")
            category_counts[category] = category_counts.get(category, 0) + 1

        # Compute compliance status.
        compliance_status = "compliant" if invalid_count == 0 else "non_compliant"

        report: Dict[str, Any] = {
            "total_records": len(self.data),
            "valid_records": valid_count,
            "invalid_records": invalid_count,
            "compliance_status": compliance_status,
            "category_counts": dict(sorted(category_counts.items(), key=lambda x: x[0])),
            "validation_summary": _validation_summary(self.data),
        }

        logger.info("Report generated: %d total, %d valid, %d invalid.",
                     report["total_records"], report["valid_records"],
                     report["invalid_records"])
        return report


def _validation_summary(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build a summary list from validation results.

    Args:
        data: Validation result list.

    Returns:
        A list of summary dictionaries.
    """
    summary: List[Dict[str, Any]] = []
    for record in data:
        summary.append({
            "id": record.get("id"),
            "category": record.get("category"),
            "status": record["status"],
            "value": record.get("value"),
            "findings": record.get("findings", []),
        })
    return summary
