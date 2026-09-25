"""
Tests for the Issue Categorizer module.

Validates that the categorizer correctly classifies issues into
the four predefined categories (bug, enhancement, documentation,
security) based on keyword matching.
"""

import sys
from pathlib import Path

# Ensure src. is importable when running tests directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.issue_triage.categorizer import categorize_issues, categorize_issue
from src.issue_triage.models import Issue, IssueCategory


def _get_test_issues():
    """Return a list of test issues with known categories."""
    return [
        Issue(id=1, title="High error rate", description="Login bugs", category=IssueCategory.BUG),
        Issue(id=2, title="Improve UI", description="Enhance responsiveness", category=IssueCategory.ENHANCEMENT),
        Issue(id=3, title="Update docs", description="API documentation", category=IssueCategory.DOCUMENTATION),
        Issue(id=4, title="Security check", description="Verify encryption", category=IssueCategory.SECURITY),
    ]


def test_categorize_bug_issue():
    """Test that a bug issue is categorized as bug."""
    issues = _get_test_issues()
    result = categorize_issue(issues[0])
    assert result == IssueCategory.BUG


def test_categorize_enhancement_issue():
    """Test that an enhancement issue is categorized as enhancement."""
    issues = _get_test_issues()
    result = categorize_issue(issues[1])
    assert result == IssueCategory.ENHANCEMENT


def test_categorize_documentation_issue():
    """Test that a documentation issue is categorized as documentation."""
    issues = _get_test_issues()
    result = categorize_issue(issues[2])
    assert result == IssueCategory.DOCUMENTATION


def test_categorize_security_issue():
    """Test that a security issue is categorized as security."""
    issues = _get_test_issues()
    result = categorize_issue(issues[3])
    assert result == IssueCategory.SECURITY


def test_categorize_all_issues():
    """Test that all issues are categorized correctly."""
    issues = _get_test_issues()
    result = categorize_issues(issues)
    assert len(result) == len(issues)
    assert result[0].category == IssueCategory.BUG
    assert result[1].category == IssueCategory.ENHANCEMENT
    assert result[2].category == IssueCategory.DOCUMENTATION
    assert result[3].category == IssueCategory.SECURITY


def test_categorize_preserves_order():
    """Test that the order of issues is preserved."""
    issues = _get_test_issues()
    result = categorize_issues(issues)
    assert [issue.id for issue in result] == [1, 2, 3, 4]


def test_unknown_category_raises_error():
    """Test that an invalid category raises a ValueError."""
    issue = Issue(id=1, title="Unknown category", description="test")
    try:
        categorize_issue(issue)
        assert False, "Expected ValueError to be raised"
    except ValueError as exc:
        assert "Could not categorize" in str(exc)


def test_empty_description():
    """Test that an issue with empty description is still categorized."""
    issue = Issue(id=1, title="Security issue", description="", category=IssueCategory.BUG)
    result = categorize_issue(issue)
    assert result == IssueCategory.SECURITY
