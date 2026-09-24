"""
Issue Categorizer Module.

Categorizes GitHub issues into predefined categories based on
title and description keywords. Uses a keyword-based rule
approach for robust and maintainable classification.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from typing import List, Dict, Any

from .models import Issue, IssueCategory

# Keyword rules mapping category values to matching keywords.
# The highest-priority match wins for each issue.
_CATEGORY_RULES: Dict[IssueCategory, List[str]] = {
    IssueCategory.SECURITY: [
        "security", "vulnerab", "exploit", "credential",
        "injection", "privacy", "encrypt", "secure", "sensitive",
    ],
    IssueCategory.BUG: [
        "bug", "error", "crash", "fail", "broken", "issue",
        "regression", "defect", "broken", "glitch",
    ],
    IssueCategory.ENHANCEMENT: [
        "enhanc", "improv", "optim", "perform", "performance",
        "better", "improve", "fix", "speed", "efficiency",
        "feature", "export", "implement", "functionality", "csv",
    ],
    IssueCategory.DOCUMENTATION: [
        "document", "readme", "doc", "guide", "help", "manual",
        "tutorial", "api doc", "reference", "instructions",
    ],
}

logger = logging.getLogger("issue_triage.categorizer")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def categorize_issue(issue: Issue) -> IssueCategory:
    """Categorize a single issue into a valid category.

    The categorization uses keyword matching against the issue
    title and description. The first matching rule (highest
    priority order) determines the category.

    Args:
        issue: The Issue instance to categorize.

    Returns:
        The IssueCategory determined for the issue.

    Raises:
        ValueError: If the issue contains no matching keywords.
    """
    # Combine title and description for matching.
    text = f"{issue.title} {issue.description}".lower()

    for category in [
        IssueCategory.SECURITY,
        IssueCategory.BUG,
        IssueCategory.ENHANCEMENT,
        IssueCategory.DOCUMENTATION,
    ]:
        for keyword in _CATEGORY_RULES[category]:
            if keyword.lower() in text:
                logger.info("Categorized issue %s as %s (%s)",
                            issue.id, category.value, keyword)
                return category

    logger.warning("Issue %s could not be categorized.", issue.id)
    raise ValueError(
        f"Could not categorize issue {issue.id}: no matching keywords found. "
        f"Title: '{issue.title}', Description: '{issue.description}'"
    )


def categorize_issues(issues: List[Issue]) -> List[Issue]:
    """Categorize all issues in a list.

    Args:
        issues: List of Issue instances to categorize.

    Returns:
        The same list of issues with categories assigned.

    Raises:
        ValueError: If any issue cannot be categorized.
    """
    logger.info("Categorizing %d issues.", len(issues))

    for issue in issues:
        issue.category = categorize_issue(issue)

    logger.info("Successfully categorized all %d issues.", len(issues))
    return issues
