"""
Charts Module for Issue Triage Application.

Creates visualizations from triaged issue statistics using matplotlib.
Generates pie charts for category distribution and bar charts for
category counts, saving them as image files.

Requirements:
- English only
- Type hints in all functions
- Uses logging instead of print statements
"""

import logging
from pathlib import Path
from typing import Dict, Any, List

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend.
import matplotlib.pyplot as plt

logger = logging.getLogger("issue_triage.charts")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def create_category_charts(
    stats: Any,
    output_dir: str,
) -> List[Path]:
    """Create charts visualizing issue statistics.

    Generates two charts:
    1. A pie chart showing the category distribution.
    2. A bar chart showing category counts.

    Args:
        stats: The IssueStats instance to visualize.
        output_dir: Directory where chart images will be saved.

    Returns:
        List of Path objects pointing to the generated chart files.
    """
    logger.info("Creating charts for %d issues.", stats.total)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    chart_paths: List[Path] = []

    # --- Pie Chart: Category Distribution ---
    pie_chart = _create_pie_chart(stats, output_path, "category_distribution.png")
    chart_paths.append(pie_chart)

    # --- Bar Chart: Category Counts ---
    bar_chart = _create_bar_chart(stats, output_path, "category_counts.png")
    chart_paths.append(bar_chart)

    logger.info("Generated %d charts in %s.", len(chart_paths), output_path)
    return chart_paths


def _create_pie_chart(
    stats: Any,
    output_path: Path,
    filename: str,
) -> Path:
    """Create a pie chart for category distribution.

    Args:
        stats: The IssueStats instance to visualize.
        output_path: Output directory for the chart.
        filename: File name for the chart.

    Returns:
        Path to the generated pie chart file.
    """
    categories = list(stats.by_category.items())
    labels = [category for category, _ in categories]
    sizes = [count for _, count in categories]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct * sum(sizes) / 100))} issues)",
        startangle=90,
        colors=[plt.cm.Set3(i) for i in range(len(labels))],
        textprops={"fontsize": 11},
    )
    ax.set_title("Issue Category Distribution", fontsize=14, fontweight="bold")

    fig.tight_layout()
    chart_path = output_path / filename
    fig.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    logger.info("Saved pie chart: %s", chart_path)
    return chart_path


def _create_bar_chart(
    stats: Any,
    output_path: Path,
    filename: str,
) -> Path:
    """Create a bar chart for category counts.

    Args:
        stats: The IssueStats instance to visualize.
        output_path: Output directory for the chart.
        filename: File name for the chart.

    Returns:
        Path to the generated bar chart file.
    """
    categories = list(stats.by_category.items())
    labels = [category for category, _ in categories]
    sizes = [count for _, count in categories]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(labels, sizes, color=[plt.cm.Set3(i) for i in range(len(labels))])
    ax.set_title("Issue Category Counts", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Issues")
    ax.set_xlabel("Category")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    chart_path = output_path / filename
    fig.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    logger.info("Saved bar chart: %s", chart_path)
    return chart_path
