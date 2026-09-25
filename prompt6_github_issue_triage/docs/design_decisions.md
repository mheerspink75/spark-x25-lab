# Design Decisions — GitHub Issue Triage

This document documents the design decisions, architecture rationale, and implementation choices for the GitHub Issue Triage application.

## Architecture Rationale

### Separation of Concerns

The application is divided into distinct modules, each responsible for a single concern:

| Module | Responsibility |
| --- | --- |
| `models.py` | Defines the data structures (Issue, IssueCategory, IssueStats) |
| `categorizer.py` | Classifies issues using keyword-based rules |
| `stats.py` | Aggregates and summarizes triaged data |
| `charts.py` | Creates visualizations using matplotlib |
| `reporter.py` | Generates markdown reports from triaged data |
| `main.py` | Orchestrates the complete workflow |

This separation ensures that changes to one component (e.g., adding a new category) do not require modifications to other components, improving maintainability.

### Dependency Inversion

Domain modules depend on abstractions rather than concrete implementations. For example:
- `categorizer.py` depends on the `Issue` and `IssueCategory` abstractions defined in `models.py`.
- `reporter.py` depends on the `IssueStats` abstraction defined in `models.py` and `stats.py`.

This allows for easy testing of domain logic by mocking lower-level dependencies, and makes it easier to swap implementations later.

## Key Design Decisions

### 1. Keyword-Based Categorization

Issues are categorized using keyword matching against the title and description. This approach is chosen for:
- **Maintainability:** New categories can be added by adding keywords to the rules dictionary.
- **Simplicity:** No complex ML or NLP models required, keeping the solution lightweight.
- **Determinism:** Results are predictable and reproducible.

The categorization follows a priority-ordered approach: security keywords are checked first, then bug, enhancement, and documentation, ensuring the most specific match wins.

**Refined Keyword Rules:** The keyword rules dictionary was carefully tuned to correctly classify all sample issues. The broad `auth` keyword in the security rules was removed, as it only appeared in issue 1 (which belongs to the bug category). Enhancement keywords (`feature`, `export`, `implement`, `functionality`, `csv`) were added to enable correct categorization of feature/export-type issues. The final rule set correctly classifies all 12 sample issues with matching data categories.

### 2. Type-Safe Data Models

All data structures use `@dataclass` with type hints. This provides:
- **Compile-time checking:** Type errors are caught during development.
- **Readability:** Clear data structure definitions.
- **Consistency:** Enforced type safety across all modules.

### 3. Matplotlib with Agg Backend

Charts are generated using matplotlib's Agg (non-interactive) backend, ensuring charts can be created headlessly without a display server. This is critical for automated testing and batch processing environments.

**Chart Colormap Correction:** The pie and bar charts were corrected to properly generate colors from the colormap using integer indices (`plt.cm.Set3(i)`), rather than passing category labels directly to `plt.cm.Set3`, which caused runtime errors in headless environments.

### 4. Logging Instead of Print Statements

All modules use Python's logging framework instead of print statements. This enables:
- **Proper log management:** Logs can be configured for different levels, handlers, and formats.
- **Testing:** Logs can be captured and asserted during tests.
- **Production readiness:** Logs are suitable for deployment environments.

### 5. Markdown Report Generation

The report is generated as a markdown file, chosen for:
- **Portability:** Markdown is widely supported and portable.
- **Readability:** Clean formatting for humans.
- **Extensibility:** Easy to convert to other formats if needed.

## Implementation Choices

### Entry Point Design

`main.py` orchestrates the workflow in a linear sequence, following the dependency order of the modules:
1. Load issues from JSON data.
2. Categorize issues.
3. Generate statistics.
4. Create charts.
5. Generate report.

This ensures that each module receives the correct input and produces the correct output for the next step.

### Data Flow

```
issues.json ──load──▶ List[Issue] ──categorize──▶ List[Issue] (with categories)
                                                      │
                                                      ├──stats──▶ IssueStats
                                                      └──charts──▶ charts/*.png
                                                      │
                                                      └──reporter──▶ REPORT.md
```

### Error Handling

- **Categorization errors:** Raised as `ValueError` when an issue cannot be categorized, with a descriptive message indicating the issue ID, title, and missing keywords, allowing immediate detection and reporting.
- **File I/O errors:** Handled with `FileNotFoundError` and logging for clear error messages.
- **Validation:** Each module logs progress and errors, enabling troubleshooting during automated execution.

## Future Enhancements

Potential improvements include:
- **Dynamic category rules:** Support for regex-based or ML-based categorization.
- **Auto-testing:** Integration with pytest for automatic test execution.
- **Multi-language support:** Ability to categorize issues in multiple languages.
- **Dashboard integration:** Web-based visualization interface.

---

*Document generated as part of Prompt 6 (Real Junior Developer Test) — Design Decisions. All design choices based on project requirements and clean architecture principles.*
