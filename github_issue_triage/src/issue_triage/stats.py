"""
Statistics Module for Issue Triage Application.

Generates and aggregates summary statistics from categorized issues
for reporting and visualization.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from typing import List, Dict, Any

from .models import Issue, IssueStats

logger = logging.getLogger("issue_triage.stats")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def generate_stats(issues: List[Issue]) -> IssueStats:
    """Generate summary statistics from a list of categorized issues.

    Args:
        issues: List of Issue instances that have been categorized.

    Returns:
        An IssueStats instance containing the aggregated statistics.
    """
    logger.info("Generating statistics for %d issues.", len(issues))

    stats = IssueStats()
    stats.total = len(issues)

    for issue in issues:
        if issue.category is not None:
            category_value = issue.category.value
            stats.by_category[category_value] = (
                stats.by_category.get(category_value, 0) + 1
            )

    # Populate by_category_details from the finalized by_category mapping.
    _initialize_details(stats)

    logger.info("Generated statistics: %d total, %d categories.",
                 stats.total, len(stats.by_category))
    return stats


def _initialize_details(stats: IssueStats) -> None:
    """Populate by_category_details from the finalized by_category mapping.

    Args:
        stats: The IssueStats instance to populate.
    """
    for category, count in stats.by_category.items():
        stats.by_category_details.setdefault(category, []).append(count)


def get_report_snapshot(stats: IssueStats) -> Dict[str, Any]:
    """Build a report snapshot dictionary from IssueStats.

    Args:
        stats: The IssueStats instance to snapshot.

    Returns:
        A dictionary containing the key statistics for reporting.
    """
    return {
        "total_issues": stats.total,
        "category_counts": dict(stats.by_category),
        "category_details": stats.by_category_details,
        "total_categories": len(stats.by_category),
    }
