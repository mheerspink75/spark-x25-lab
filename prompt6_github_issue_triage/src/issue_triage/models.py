"""
Data Models for Issue Triage Application.

Defines the core data structures used throughout the issue triage
application: individual issues, their categories, and summary
statistics.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any


class IssueCategory(Enum):
    """Enumeration of valid issue categories."""

    BUG = "bug"
    ENHANCEMENT = "enhancement"
    DOCUMENTATION = "documentation"
    SECURITY = "security"

    @classmethod
    def from_value(cls, value: str) -> "IssueCategory":
        """Convert a string value to the corresponding IssueCategory enum.

        Args:
            value: The string value of the category.

        Returns:
            The matching IssueCategory enum member.

        Raises:
            ValueError: If the value is not a known category.
        """
        try:
            return cls(value)
        except ValueError:
            raise ValueError(
                f"Unknown issue category: '{value}'. "
                f"Valid categories are: {[c.value for c in cls]}"
            )


@dataclass
class Issue:
    """Represents a single GitHub issue."""

    id: int
    title: str
    description: str = ""
    category: IssueCategory = IssueCategory.BUG
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        """Return a readable string representation of the issue."""
        return (
            f"Issue(id={self.id}, title='{self.title}', "
            f"category={self.category.value})"
        )


@dataclass
class IssueStats:
    """Aggregates summary statistics for triaged issues."""

    total: int = 0
    by_category: Dict[str, int] = field(default_factory=dict)
    by_category_details: Dict[str, List[int]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize category counts from the by_category mapping."""
        self._initialize_counts()

    def _initialize_counts(self) -> None:
        """Populate category counts and detail lists from by_category."""
        for category, count in self.by_category.items():
            self.by_category_details.setdefault(category, []).append(count)

    def get_category_count(self, category_value: str) -> int:
        """Return the count for a given category value.

        Args:
            category_value: The string value of the category.

        Returns:
            The count for the specified category.
        """
        return self.by_category.get(category_value, 0)

    def get_total(self) -> int:
        """Return the total number of issues."""
        return self.total
