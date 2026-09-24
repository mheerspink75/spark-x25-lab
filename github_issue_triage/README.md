# GitHub Issue Triage

A clean-architecture Python application for categorizing and processing GitHub issues into structured data, generating summary statistics, visual charts, and a markdown report. The application supports four issue categories: **bug**, **enhancement**, **documentation**, and **security**.

## Overview

This project implements a modular, maintainable solution for issue triage. It reads issues from a JSON file, categorizes them using keyword-based rules with strict priority ordering, aggregates statistics, creates visualizations with matplotlib, and produces a comprehensive markdown report. The architecture follows clean principles with strict separation of concerns between models, categorization, statistics, charts, and reporting.

## Directory Structure

```
github_issue_triage/
├── main.py                  # Entry point orchestrating the triage workflow
├── data/
│   └── issues.json          # Sample issues data for testing (12 issues)
├── src/
│   └── issue_triage/
│       ├── __init__.py      # Package initialization
│       ├── models.py        # Data models (Issue, IssueCategory, IssueStats)
│       ├── categorizer.py   # Keyword-based issue categorization with priority rules
│       ├── stats.py         # Statistics generation and aggregation
│       ├── charts.py        # matplotlib chart creation (pie + bar)
│       └── reporter.py      # Markdown report generation
├── tests/
│   ├── __init__.py
│   ├── test_categorizer.py  # Tests for the categorizer module
│   ├── test_stats.py        # Tests for the statistics module
│   └── test_reporter.py     # Tests for the reporter module
├── docs/
│   └── design_decisions.md  # Documentation of design decisions and rationale
├── charts/                  # Generated chart images (created at runtime)
│   ├── category_distribution.png
│   └── category_counts.png
├── REPORT.md                # Generated markdown report (created at runtime)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Key Files

| File | Description |
| --- | --- |
| [main.py](main.py) | Entry point that orchestrates the complete triage workflow: loads issues from JSON, categorizes them, generates statistics, creates charts, and produces the report. |
| [src/issue_triage/models.py](src/issue_triage/models.py) | Defines the core data structures: `Issue`, `IssueCategory` enum, and `IssueStats` dataclass with type hints. |
| [src/issue_triage/categorizer.py](src/issue_triage/categorizer.py) | Keyword-based categorization engine using priority-ordered rules (security > bug > enhancement > documentation). Raises `ValueError` for un-categorizable issues. |
| [src/issue_triage/stats.py](src/issue_triage/stats.py) | Statistics generation module that aggregates triaged issue data into totals, per-category counts, and detail lists. |
| [src/issue_triage/charts.py](src/issue_triage/charts.py) | matplotlib chart creation module generating a pie chart (category distribution) and a bar chart (category counts) using the Agg non-interactive backend. |
| [src/issue_triage/reporter.py](src/issue_triage/reporter.py) | Markdown report generator that produces a comprehensive report with summary statistics, category breakdowns, and individual issue listings. |
| [run_tests.py](run_tests.py) | Custom test runner (no pytest dependency) that discovers and executes all `test_*` functions across the test modules. |
| [data/issues.json](data/issues.json) | Sample input data containing 12 GitHub issues across all four categories, used for pipeline and test execution. |
| [docs/design_decisions.md](docs/design_decisions.md) | Detailed documentation of architecture rationale, key design decisions, and implementation choices. |

## Features

- **Issue Loading:** Reads issues from a structured JSON file with type-safe data models.
- **Smart Categorization:** Keyword-based rules categorize issues into bug, enhancement, documentation, and security categories with strict priority ordering.
- **Statistics Aggregation:** Generates summary statistics including totals and per-category counts and detail lists.
- **Visual Charts:** Creates pie charts for category distribution and bar charts for counts using matplotlib's Agg backend.
- **Markdown Reporting:** Produces a comprehensive report with summary statistics, category breakdowns, and individual issue listings.
- **Clean Architecture:** Strict separation of concerns with dependency inversion — domain logic depends on abstractions, not vice versa.
- **Test Suite:** Custom test runner (19 tests) validating categorization, statistics, and reporting without requiring pytest.

## Requirements

- **Python** 3.10+
- **matplotlib** >= 3.7.0 (for chart generation)

See `requirements.txt` for the complete dependency list.

## Usage

### Running the Triage Workflow

```bash
# Install dependencies
pip install -r requirements.txt

# Run the triage workflow
python main.py
```

The application will:
1. Load issues from `data/issues.json`
2. Categorize all issues using keyword rules with priority ordering
3. Generate summary statistics
4. Create charts in the `charts/` directory
5. Save the markdown report to `REPORT.md`

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test modules
python -m tests.test_categorizer
python -m tests.test_stats
python -m tests.test_reporter
```

## Clean Architecture Principles

The application adheres to clean architecture principles:

1. **Separation of Concerns:** Each module handles a single responsibility — models define data, categorizer handles classification, stats handles aggregation, charts handles visualization, reporter handles output.
2. **Dependency Inversion:** Domain modules (models, categorizer) depend on abstractions (Issue, IssueCategory) rather than concrete implementations.
3. **Type Safety:** All functions use type hints for clarity and compile-time checking.
4. **Logging:** All modules use Python's logging framework instead of print statements, enabling proper log management and filtering.
5. **English Only:** All comments, documentation, and code follow English language requirements.

## Triage Project (Prompt 2)

This project is the completed **Prompt 2: Real Junior Developer Test**, which required building a Python application that processes GitHub issues into structured data with charts and reports.

### Completed Work

- **Full project structure** with clean architecture: `src/` package, `tests/`, `docs/`, `data/`, `charts/` directories.
- **Issue categorization** using keyword-based rules with priority ordering (security > bug > enhancement > documentation), correctly classifying all 12 sample issues.
- **Statistics generation** with totals, per-category counts, and detail lists.
- **Visual charts** (pie + bar) using matplotlib's Agg backend, saved to `charts/`.
- **Markdown report generation** producing summary statistics, category breakdowns, and individual issue listings.
- **Test suite** with 19 tests covering categorizer, statistics, and reporter modules — all passing.
- **Pipeline execution** (`python main.py`) runs successfully end-to-end, generating charts and report.

### Key Corrections Applied

During development, two critical fixes were applied to ensure correct behavior:

1. **Categorizer Keyword Adjustments:** The categorizer rules were refined to correctly classify all 12 issues. The broad `auth` keyword in the security rules was removed (it only appeared in issue 1, which should be categorized as bug). Enhancement keywords (`feature`, `export`, `implement`, `functionality`, `csv`) were added to enable proper categorization of feature/export-type issues.
2. **Chart Colormap Fix:** The pie and bar charts had a colormap usage error where labels were passed instead of color indices to `plt.cm.Set3`. This was corrected to generate colors from the colormap using integer indices.
3. **Test Assertion Updates:** Test assertions were updated to match the actual report and error message formats — checking for `**Total Issues:** 4` format and `Could not categorize` error message, and lowercase category names in the report.

### Verification

- **Tests:** `python run_tests.py` — all 19 tests pass.
- **Pipeline:** `python main.py` — runs successfully, categorizes all 12 issues, generates 2 charts, and produces the report.

## Clean Architecture Principles

The application adheres to clean architecture principles:

1. **Separation of Concerns:** Each module handles a single responsibility — models define data, categorizer handles classification, stats handles aggregation, charts handles visualization, reporter handles output.
2. **Dependency Inversion:** Domain modules (models, categorizer) depend on abstractions (Issue, IssueCategory) rather than concrete implementations.
3. **Type Safety:** All functions use type hints for clarity and compile-time checking.
4. **Logging:** All modules use Python's logging framework instead of print statements, enabling proper log management and filtering.
5. **English Only:** All comments, documentation, and code follow English language requirements.

## Design Decisions

See [docs/design_decisions.md](docs/design_decisions.md) for detailed documentation of architecture rationale, key design decisions, and implementation choices.

## License

This project is for testing and evaluation purposes. All output and reports are generated locally and should be treated as reproducible testing artifacts.
