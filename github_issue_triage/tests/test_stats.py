"""
Tests for the Statistics Generation module.

Validates that the statistics module correctly aggregates triaged
issue data into summary statistics including totals and per-category
counts.
"""

import sys
from pathlib import Path

# Ensure src. is importable when running tests directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.issue_triage.models import Issue, IssueCategory
from src.issue_triage.stats import generate_stats, get_report_snapshot


def _get_test_issues():
    """Return test issues with known categories."""
    return [
        Issue(id=1, title="Bug 1", description="", category=IssueCategory.BUG),
        Issue(id=2, title="Enh 1", description="", category=IssueCategory.ENHANCEMENT),
        Issue(id=3, title="Doc 1", description="", category=IssueCategory.DOCUMENTATION),
        Issue(id=4, title="Sec 1", description="", category=IssueCategory.SECURITY),
        Issue(id=5, title="Bug 2", description="", category=IssueCategory.BUG),
    ]


def test_total_count():
    """Test that the total count matches the number of issues."""
    stats = generate_stats(_get_test_issues())
    assert stats.total == 5


def test_category_counts():
    """Test that category counts are correct."""
    stats = generate_stats(_get_test_issues())
    assert stats.by_category["bug"] == 2
    assert stats.by_category["enhancement"] == 1
    assert stats.by_category["documentation"] == 1
    assert stats.by_category["security"] == 1


def test_category_details():
    """Test that category details list contains correct counts."""
    stats = generate_stats(_get_test_issues())
    assert stats.by_category_details["bug"] == [2]
    assert stats.by_category_details["enhancement"] == [1]


def test_get_category_count():
    """Test that get_category_count returns correct values."""
    stats = generate_stats(_get_test_issues())
    assert stats.get_category_count("bug") == 2
    assert stats.get_category_count("security") == 1
    assert stats.get_category_count("nonexistent") == 0


def test_empty_issues():
    """Test that statistics work for an empty issue list."""
    stats = generate_stats([])
    assert stats.total == 0
    assert stats.by_category == {}


def test_snapshot_content():
    """Test that the report snapshot contains correct data."""
    stats = generate_stats(_get_test_issues())
    snapshot = get_report_snapshot(stats)

    assert snapshot["total_issues"] == 5
    assert snapshot["total_categories"] == 4
    assert snapshot["category_counts"]["bug"] == 2
    assert snapshot["category_counts"]["enhancement"] == 1
    assert snapshot["category_details"]["bug"] == [2]


def test_snapshot_empty():
    """Test that snapshot works for empty stats."""
    stats = generate_stats([])
    snapshot = get_report_snapshot(stats)
    assert snapshot["total_issues"] == 0
    assert snapshot["total_categories"] == 0
