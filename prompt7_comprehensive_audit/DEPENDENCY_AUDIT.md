# Dependency Audit

This document inventories the direct dependencies of the project, analyzes them for unused, duplicated, missing, or unnecessary dependencies, identifies version-pinning and reproducibility concerns, and explains the role of each important dependency. No claim is made that a dependency is vulnerable unless project evidence supports it.

## Overall Assessment

The project's dependency footprint is **clean and minimal**, with dependencies that are all directly used in their respective modules. No unused or unnecessary dependencies were identified. However, version-pinning and reproducibility concerns exist, as requirements files use minimum-version constraints rather than exact pinning, and no lock files are maintained.

## Direct Dependency Inventory

### Python Dependencies

| Dependency | Version Constraint | Used In | Role |
| --- | --- | --- | --- |
| `numpy` | `>=1.24.0` | `test_prompts/prompt1_memory_stress_test/benchmark.py`, `prompt6_github_issue_triage/src/issue_triage/charts.py` | Numerical analysis and chart data processing in benchmark and chart modules. |
| `matplotlib` | `>=3.7.0` | `test_prompts/prompt1_memory_stress_test/benchmark.py`, `prompt6_github_issue_triage/src/issue_triage/charts.py` | Chart generation (PNG output) in both the benchmark and the triage chart modules. |
| `flask` | `>=3.0.0` | `prompt4_local_web_dashboard/dashboard.py` | Web application framework serving the dashboard and REST API endpoints. |
| `psutil` | `>=6.0.0` | `prompt4_local_web_dashboard/dashboard.py` | System resource monitoring (CPU, RAM, disk) for the dashboard. |

**Requirement files:**
- `test_prompts/prompt1_memory_stress_test/requirements.txt` — lists `matplotlib>=3.7.0`, `numpy>=1.24.0`.
- `prompt4_local_web_dashboard/requirements.txt` — lists `flask>=3.0.0`, `psutil>=6.0.0`.
- `prompt6_github_issue_triage/requirements.txt` — lists `matplotlib>=3.7.0`.

### External Tools & Services

| Dependency | Role | Source |
| --- | --- | --- |
| Ollama server | Local model runtime serving the `SparkLLM/Spark-X2.5-4B:latest` model at `http://127.0.0.1:11434`. | `opencode.json`, `run.sh` |
| opencode CLI | Agent-based coding tool launched by `run.sh` with the configured model. | `run.sh` |
| `@ai-sdk/openai-compatible` (npm) | OpenCode provider adapter converting the Ollama-compatible API to the OpenCode SDK format. | `opencode.json` |

### Python Standard Library

All Python modules use the Python standard library where possible, including modules such as `csv`, `json`, `pathlib`, `typing`, `logging`, `dataclasses`, `enum`, `concurrent.futures`, `os`, `sys`, `datetime`, and `urllib`. No third-party packages are required for these modules.

## Unused, Duplicated, Missing, or Unnecessary Dependencies

### Verified Findings

- **No unused dependencies.** Each listed dependency is directly used in at least one module:
  - `matplotlib` is used for chart generation in both `benchmark.py` and `charts.py`.
  - `numpy` is used for numerical analysis in `benchmark.py` and chart data processing in `charts.py`.
  - `flask` serves the web dashboard in `dashboard.py`.
  - `psutil` provides system resource metrics in `dashboard.py`.
- **No duplicated dependencies.** Dependencies are not duplicated across modules. Each project's `requirements.txt` lists only the packages it needs.
- **No missing dependencies.** All modules that require external packages have corresponding entries in their `requirements.txt` files.

### Potential Concerns

- **Generated artifact dependency coupling:** The triage project's `charts.py` imports `matplotlib` and generates PNG charts referenced by `REPORT.md` and `charts/` directories. While the dependency is valid, the generated chart artifacts are excluded from version control via `.gitignore`, meaning the dependency is only needed during runtime generation, not for static distribution.

## Version-Pinning and Reproducibility Concerns

### Verified Findings

- **Minimum-version constraints:** All Python `requirements.txt` files use `>=` (minimum version) constraints rather than `==` (exact version) pinning. This provides flexibility for newer package versions but reduces reproducibility.
- **No version lock files:** No `requirements.lock`, `poetry.lock`, or equivalent lock files are present in the workspace.
- **External tool version transparency:** The OpenCode provider configuration (`opencode.json`) references `@ai-sdk/openai-compatible` without specifying a version, and `run.sh` does not verify or pin the installed versions of `ollama` and `opencode` tools.

### Concerns

1. **Reproducibility gap.** Without pinned versions, the exact package versions may differ across environments, potentially causing subtle behavioral differences in chart generation, web serving, or system monitoring.
2. **Environmental variability.** The `run.sh` script does not automatically install or verify dependency versions; users must set up environments separately, increasing the risk of version mismatches.
3. **External tool dependency.** The reliance on `ollama` and `opencode` as external tools without version verification means the launcher script depends on these tools being present and compatible with the configured model.

## Role of Each Important Dependency

### `matplotlib>=3.7.0`
**Role:** Chart generation and data visualization. Used in `benchmark.py` to generate performance charts (PNG) from benchmark metrics, and in `prompt6_github_issue_triage/src/issue_triage/charts.py` to create category distribution and count charts for the triage report.
**Evidence:** `benchmark.py` imports `matplotlib.pyplot as plt` and configures `matplotlib.use("Agg")` for non-interactive chart generation. `charts.py` uses matplotlib for category distribution and count visualizations.

### `numpy>=1.24.0`
**Role:** Numerical analysis and data processing. Used in `benchmark.py` for numerical operations within the memory stress and multithreading benchmarks, and in `charts.py` for chart data processing.
**Evidence:** `benchmark.py` imports `numpy as np` for numerical computations in the benchmark metrics.

### `flask>=3.0.0`
**Role:** Web application framework. Serves the `prompt4_local_web_dashboard/dashboard.py` Flask application, providing REST API endpoints (`/`, `/api/metrics`, `/health`) for system resource monitoring and health checks.
**Evidence:** `dashboard.py` imports `from flask import Flask, render_template_string, jsonify` and uses `app = Flask(__name__)` for the web application.

### `psutil>=6.0.0`
**Role:** System resource monitoring. Provides access to CPU, memory, and disk usage metrics, used in `dashboard.py` to collect real-time system metrics for display and validation.
**Evidence:** `dashboard.py` imports `psutil` and calls `psutil.cpu_percent()`, `psutil.virtual_memory()`, and disk-related functions for metric collection.

### Ollama Server
**Role:** Local model runtime. Serves the `SparkLLM/Spark-X2.5-4B:latest` model at `http://127.0.0.1:11434`, providing the inference API consumed by `run.sh` and `dashboard.py`.
**Evidence:** `opencode.json` configures the Ollama provider with the model and API base URL; `run.sh` connects to the server for model health checks.

### `@ai-sdk/openai-compatible` (npm)
**Role:** OpenCode provider adapter. Converts the Ollama-compatible API endpoint to the OpenCode SDK format, enabling OpenCode to interact with the local model via `opencode.json`.
**Evidence:** `opencode.json` specifies the provider using `@ai-sdk/openai-compatible` with a base URL pointing to the Ollama server.

## Version-Pinning Recommendations

1. **Pin exact versions.** Convert `>=` constraints to `==` exact versions in `requirements.txt` files to ensure reproducible environments.
2. **Add lock files.** Include `requirements.lock` or `poetry.lock` for all Python projects to pin exact dependency versions.
3. **Pin npm packages.** Specify exact version constraints for `@ai-sdk/openai-compatible` in the OpenCode configuration.

## Reproducibility Recommendations

1. **Dependency verification in run.sh.** Add dependency installation and version verification steps to `run.sh` to ensure compatible versions before launching.
2. **Environment documentation.** Document the exact Python and npm versions required in the README for reproducibility.
3. **Dependency inventory audit.** Continue the dependency audit to identify any missing or unnecessary dependencies, and update `requirements.txt` accordingly.

**Overall conclusion:** The project's dependency footprint is clean, with all dependencies directly used and none duplicated or unused. However, version-pinning and reproducibility concerns exist due to minimum-version constraints, lack of lock files, and unspecified external tool versions. Recommendations have been provided to address these concerns.
