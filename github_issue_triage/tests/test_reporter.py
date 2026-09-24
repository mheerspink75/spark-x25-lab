"""
Tests for the Report Generation module.

Validates that the reporter correctly generates a markdown report
from triaged issues, statistics, and charts.
"""

import sys
from pathlib import Path

# Ensure src. is importable when running tests directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.issue_triage.models import Issue, IssueCategory
from src.issue_triage.reporter import generate_report
from src.issue_triage.stats import generate_stats


def _get_test_issues():
    """Return test issues with known categories."""
    return [
        Issue(id=1, title="High error rate", description="Login bugs", category=IssueCategory.BUG),
        Issue(id=2, title="Improve UI", description="Enhance responsiveness", category=IssueCategory.ENHANCEMENT),
        Issue(id=3, title="Update docs", description="API documentation", category=IssueCategory.DOCUMENTATION),
        Issue(id=4, title="Security check", description="Verify encryption", category=IssueCategory.SECURITY),
    ]


def _get_report_path(tmp_path):
    """Return a temporary path for the report output."""
    return str(tmp_path / "REPORT.md")


def test_report_generated():
    """Test that the report file is created."""
    issues = _get_test_issues()
    stats = generate_stats(issues)
    path = generate_report(issues, stats, _get_report_path(Path(".")))
    assert Path(path).exists()
    assert Path(path).stat().st_size > 0


def test_report_content():
    """Test that the report contains expected content."""
    issues = _get_test_issues()
    stats = generate_stats(issues)
    path = generate_report(issues, stats, _get_report_path(Path(".")))

    content = Path(path).read_text(encoding="utf-8")

    assert "# Issue Triage Report" in content
    assert "**Total Issues:** 4" in content
    assert "Category Breakdown" in content
    assert "Individual Issues" in content
    assert "bug" in content
    assert "enhancement" in content
    assert "documentation" in content
    assert "security" in content


def test_report_preserves_issue_data():
    """Test that the report includes all issue titles and descriptions."""
    issues = _get_test_issues()
    stats = generate_stats(issues)
    path = generate_report(issues, stats, _get_report_path(Path(".")))

    content = Path(path).read_text(encoding="utf-8")

    assert "High error rate" in content
    assert "Improve UI" in content
    assert "Verify encryption" in content
    assert "Login bugs" in content
    assert "API documentation" in content


def test_report_with_empty_issues():
    """Test that the report is generated for an empty issue list."""
    issues = []
    stats = generate_stats(issues)
    path = generate_report(issues, stats, _get_report_path(Path(".")))
    assert Path(path).exists()
