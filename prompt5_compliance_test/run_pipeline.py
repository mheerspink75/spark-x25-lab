"""
Pipeline Orchestration Script for Compliance Test.

Runs the five CSV processing modules (reader, parser, processor,
validator, reporter) in sequence to process a CSV file and generate
a compliance audit report.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from pathlib import Path
from typing import Dict, Any

# Import the five compliance modules.
from csv_reader import CSVReader
from csv_parser import CSVParser
from csv_processor import CSVProcessor
from csv_validator import CSVValidator
from csv_reporter import CSVReporter

# Configure logging for the pipeline.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Pipeline] %(message)s",
)


def run_pipeline(csv_path: str) -> Dict[str, Any]:
    """Run the complete CSV compliance pipeline.

    Args:
        csv_path: Path to the input CSV file.

    Returns:
        The final compliance report dictionary from the reporter.
    """
    logger = logging.getLogger("prompt5_compliance_test.pipeline")

    # Step 1: Read the CSV file.
    logger.info("=== Step 1: Reading CSV file ===")
    reader = CSVReader(csv_path)
    raw_data = reader.read()

    # Step 2: Parse the raw data.
    logger.info("=== Step 2: Parsing CSV data ===")
    parser = CSVParser(raw_data)
    parsed_data = parser.parse()

    # Step 3: Process the parsed data.
    logger.info("=== Step 3: Processing CSV data ===")
    processor = CSVProcessor(parsed_data)
    processed_data = processor.process()

    # Step 4: Validate the processed data.
    logger.info("=== Step 4: Validating CSV data ===")
    validator = CSVValidator(processed_data)
    validation_results = validator.validate()

    # Step 5: Generate the report.
    logger.info("=== Step 5: Generating compliance report ===")
    reporter = CSVReporter(validation_results)
    report = reporter.report()

    return report


def main() -> None:
    """Run the pipeline with the sample CSV file and generate the audit."""
    csv_path = str(Path(__file__).parent / "sample_data.csv")

    logger = logging.getLogger("prompt5_compliance_test.pipeline")
    logger.info("Starting compliance test pipeline.")

    report = run_pipeline(csv_path)

    # Generate the compliance audit document.
    _generate_audit(report, csv_path)

    logger.info("Compliance pipeline completed successfully.")


def _generate_audit(report: Dict[str, Any], csv_path: str) -> None:
    """Generate the compliance audit markdown document.

    Args:
        report: The compliance report dictionary.
        csv_path: Path to the input CSV file.
    """
    import os

    audit_path = str(Path(__file__).parent / "COMPLIANCE_AUDIT.md")

    lines: list[str] = []
    lines.append("# Compliance Audit Report")
    lines.append("")
    lines.append(f"**Input CSV:** `{csv_path}`")
    lines.append("")
    lines.append("## Overall Status")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"| --- | --- |")
    lines.append(f"| Total Records | {report['total_records']} |")
    lines.append(f"| Valid Records | {report['valid_records']} |")
    lines.append(f"| Invalid Records | {report['invalid_records']} |")
    lines.append(f"| Compliance Status | **{report['compliance_status']}** |")
    lines.append("")
    lines.append("## Category Breakdown")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("| --- | --- |")
    for category, count in report.get("category_counts", {}).items():
        lines.append(f"| {category} | {count} |")
    lines.append("")
    lines.append("## Validation Summary")
    lines.append("")
    lines.append("| ID | Category | Status | Value | Findings |")
    lines.append("| --- | --- | --- | --- | --- |")
    for item in report.get("validation_summary", []):
        findings = item.get("findings", [])
        findings_text = "; ".join(
            f"{f['field']}: {f['detail']}" for f in findings
        ) if findings else "—"
        lines.append(
            f"| {item.get('id')} | {item.get('category')} | "
            f"{item['status']} | {item.get('value')} | {findings_text} |"
        )
    lines.append("")
    lines.append("## Conclusion")
    lines.append("")
    if report["compliance_status"] == "compliant":
        lines.append(
            f"The compliance test completed successfully. All {report['total_records']} "
            f"records passed validation with a status of **compliant**."
        )
    else:
        lines.append(
            f"The compliance test detected {report['invalid_records']} invalid "
            f"records out of {report['total_records']} total. The status is "
            f"**non_compliant**."
        )
    lines.append("")
    lines.append("---")
    lines.append(
        "*Document generated as part of Prompt 5 (Agent Memory Test) — Compliance Audit. "
        "All modules use type hints, logging, and English only."
    )

    with open(audit_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()
