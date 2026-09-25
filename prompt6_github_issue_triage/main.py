"""
Issue Triage Application — Main Entry Point.

Orchestrates the complete issue triage workflow: loads issues from a
JSON file, categorizes them, generates statistics, creates charts,
and produces a markdown report.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import json
import logging
from pathlib import Path
from typing import List

from src.issue_triage.categorizer import categorize_issues
from src.issue_triage.charts import create_category_charts
from src.issue_triage.models import Issue, IssueCategory
from src.issue_triage.reporter import generate_report
from src.issue_triage.stats import generate_stats

# Configure logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Main] %(message)s",
)
logger = logging.getLogger("issue_triage.main")


def load_issues(data_path: str) -> List[Issue]:
    """Load issues from a JSON file.

    Args:
        data_path: Path to the JSON file containing issues.

    Returns:
        List of Issue instances loaded from the JSON data.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
        ValueError: If the JSON data is malformed.
    """
    logger.info("Loading issues from: %s", data_path)

    if not Path(data_path).exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    with Path(data_path).open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    issues: List[Issue] = []
    for entry in raw_data:
        issues.append(Issue(
            id=entry.get("id", 0),
            title=entry.get("title", ""),
            description=entry.get("description", ""),
            category=IssueCategory(entry.get("category", "bug")),
            metadata=entry.get("metadata", {}),
        ))

    logger.info("Loaded %d issues from JSON data.", len(issues))
    return issues


def run_triage(
    data_path: str,
    charts_output: str,
    report_output: str,
) -> None:
    """Run the complete issue triage workflow.

    Args:
        data_path: Path to the input JSON file with issues.
        charts_output: Directory for generated chart images.
        report_output: Path where the markdown report will be saved.
    """
    logger.info("Starting issue triage workflow.")

    # Step 1: Load issues.
    issues = load_issues(data_path)

    # Step 2: Categorize issues.
    issues = categorize_issues(issues)

    # Step 3: Generate statistics.
    stats = generate_stats(issues)

    # Step 4: Create charts.
    chart_paths = create_category_charts(stats, charts_output)

    # Step 5: Generate report.
    report_path = generate_report(issues, stats, report_output)

    logger.info("Issue triage workflow completed successfully.")
    logger.info("Report saved to: %s", report_path)


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    data_path = str(base_dir / "data" / "issues.json")
    charts_output = str(base_dir / "charts")
    report_output = str(base_dir / "REPORT.md")

    run_triage(data_path, charts_output, report_output)
