# OpenCode Test Project

A local testing environment for OpenCode (agent-based coding tool) configured with a local Ollama model. This project is designed for automated testing, benchmarking, and code agent evaluation tasks.

## Overview

This directory serves as the workspace for OpenCode workflows, running against a local Ollama-based LLM. It includes test prompt directories, launch scripts, configuration files, and auxiliary utilities for reproducible agent testing.

## Directory Structure

```
opencode_test/
├── .gitignore              # Git ignore rules for sensitive and generated files
├── assistant-settings.md   # Language and response policy settings
├── ollama.log              # Ollama server log file
├── opencode.json           # OpenCode configuration (model, provider, options)
├── run.sh                  # Launcher script for Ollama + OpenCode
└── test_prompts/           # Directory containing test prompt files
    ├── 1_software_engineering_agent.md
    ├── 2_long_context_research.md
    ├── 3_refactoring_challenge.md
    ├── 4_autonomous_coding.md
    ├── 5_agent_memory_test.md
    ├── 6_real_junior_developer_test.md
    ├── 7_stress_test_the_65k_context_window.md
    └── memory_stress_test/  # Memory stress test benchmark (completed)
        ├── benchmark.py
        ├── requirements.txt
        ├── REPORT.md
        └── .benchmark_results/
            ├── benchmark_summary.json
            ├── results_*.json
            └── graphs/
                ├── cpu_performance.png
                ├── memory_performance.png
                ├── file_io_performance.png
                ├── multithreaded_performance.png
                └── summary_comparison.png
    └── architecture_review/  # Architecture review (Prompt 2: completed)
        ├── PROJECT_INVENTORY.md
        ├── ARCHITECTURE_REVIEW.md
        └── RISK_ASSESSMENT.md
└── opencode_optimizer/  # Optimization artifacts (Prompt 3: completed)
    ├── proposed_config.json
    └── optimization_report.md
└── local_web_dashboard/  # Web dashboard (Prompt 4: completed)
    ├── README.md
    ├── dashboard.py
    ├── requirements.txt
    ├── TEST_RESULTS.md
    └── .venv/
        └── Scripts/
            └── python.exe
└── compliance_test/  # Compliance audit (Prompt 5: completed)
    ├── COMPLIANCE_AUDIT.md
    ├── csv_reader.py
    ├── csv_parser.py
    ├── csv_processor.py
    ├── csv_reporter.py
    ├── csv_validator.py
    ├── run_pipeline.py
    └── sample_data.csv
└── github_issue_triage/  # GitHub issue triage (Prompt 6: completed)
    ├── main.py
    ├── README.md
    ├── requirements.txt
    ├── run_tests.py
    ├── conftest.py
    ├── data/
    │   └── issues.json
    ├── src/
    │   └── issue_triage/
    │       ├── __init__.py
    │       ├── categorizer.py
    │       ├── charts.py
    │       ├── models.py
    │       ├── reporter.py
    │       └── stats.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_categorizer.py
    │   ├── test_reporter.py
    │   └── test_stats.py
    ├── docs/
    │   └── design_decisions.md
    ├── charts/
    └── REPORT.md
```

## Key Files

### `opencode.json`
OpenCode configuration file that specifies:
- **Model:** `ollama/SparkLLM/Spark-X2.5-4B:latest`
- **Provider:** Ollama running locally on `http://127.0.0.1:11434/v1`
- **Options:** 65536 context window, 512 max prediction

### `run.sh`
Launcher script that:
1. Ensures Ollama server is running
2. Verifies the model is installed
3. Runs a model health check
4. Executes OpenCode with the configured model

### `assistant-settings.md`
Sets the language policy and response rules:
- **Language Lock:** English only
- Responds in English unless explicitly instructed otherwise
- This rule has priority over other stylistic preferences

### `test_prompts/`
Directory containing benchmark and test prompt files for:
- Software engineering agent behavior
- Long context research and analysis
- Refactoring challenges
- Autonomous coding tasks
- Agent memory test compliance
- Real junior developer testing
- 65k context window stress test
- Memory stress benchmarking (memory_stress_test/)

> **Prompt 2 (Long Context Research):** Completed. The `architecture_review/` directory contains the full architecture analysis, including `PROJECT_INVENTORY.md` (file inventory), `ARCHITECTURE_REVIEW.md` (architecture with Mermaid diagram and data flow), and `RISK_ASSESSMENT.md` (top 5 risks with mitigation plans).

### `architecture_review/`
The completed Prompt 2 architecture review documents:
- `PROJECT_INVENTORY.md` — File inventory grouped by purpose with dependencies.
- `ARCHITECTURE_REVIEW.md` — Architecture analysis with Mermaid diagram, data flow, coupling, and boundaries.
- `RISK_ASSESSMENT.md` — Top 5 risks with evidence and mitigation plans.

### `opencode_optimizer/`
The completed Prompt 3 optimization artifacts:
- `proposed_config.json` — Optimized configuration addressing startup, context, VRAM, and throughput.
- `optimization_report.md` — Detailed recommendations with expected benefit, tradeoffs, implementation steps, and rollback procedures.

### `local_web_dashboard/`
The completed Prompt 4 web dashboard artifacts:
- `dashboard.py` — Flask web application with real-time CPU/RAM/disk monitoring and Ollama server status. Supports validation tests via `dashboard.py --test`.
- `requirements.txt` — Dependencies: Flask and psutil.
- `TEST_RESULTS.md` — Validation test outcomes with all tests passing.
- `README.md` — Dashboard documentation and usage guide.

### `compliance_test/`
The completed Prompt 5 compliance audit artifacts:
- `csv_reader.py` — Reads CSV files into structured dictionary data.
- `csv_parser.py` — Parses data into type-safe int/float/str/bool records.
- `csv_processor.py` — Filters and transforms parsed data while preserving types.
- `csv_validator.py` — Validates records for type consistency and integrity.
- `csv_reporter.py` — Generates compliance reports and summary statistics.
- `run_pipeline.py` — Orchestrates the five modules and generates COMPLIANCE_AUDIT.md.
- `COMPLIANCE_AUDIT.md` — Compliance audit report with verification results.
- `sample_data.csv` — Sample CSV data for pipeline testing.

All five modules use type hints, logging, and English only. Pipeline validation: all 12 records passed with **compliant** status.

## Architecture Review & GitHub Issue Triage (Prompt 2)

The completed Prompt 2 analysis is available in the `architecture_review/` directory:

| Document | Description |
| --- | --- |
| `PROJECT_INVENTORY.md` | Inventory of all project files grouped by purpose, with dependencies and relationships. |
| `ARCHITECTURE_REVIEW.md` | Architecture analysis covering components, data flow, Mermaid diagram, coupling, boundaries, and failure points.
| `RISK_ASSESSMENT.md` | Top 5 risks with evidence from project files and detailed mitigation plans.

All documents use evidence from the project files (`opencode.json`, `run.sh`, `assistant-settings.md`, `.gitignore`, `test_prompts/*`, `memory_stress_test/*`, `README.md`, `LICENSE`) rather than assumptions.

## Optimization (Prompt 3)

The completed Prompt 3 refactoring optimization is available in the `opencode_optimizer/` directory:

| Document | Description |
| --- | --- |
| `proposed_config.json` | Optimized OpenCode/Ollama configuration: reduced startup, improved context, minimized VRAM, maximized throughput. |
| `optimization_report.md` | Detailed recommendations with expected benefit, tradeoffs, implementation steps, and rollback procedures. |

All recommendations are evidence-based, citing current project files (`opencode.json`, `run.sh`, `assistant-settings.md`, `.gitignore`, `test_prompts/*`, `memory_stress_test/*`, `README.md`, `LICENSE`). No existing files are modified automatically.

## Web Dashboard (Prompt 4)

The completed Prompt 4 autonomous coding web dashboard is available in the `local_web_dashboard/` directory:

| Document | Description |
| --- | --- |
| `dashboard.py` | Flask web application displaying real-time CPU, RAM, disk usage, and Ollama server status. Supports validation tests via `dashboard.py --test`. |
| `requirements.txt` | Declares dependencies: Flask >= 3.0.0 and psutil >= 6.0.0. |
| `TEST_RESULTS.md` | Validation test outcomes — all 5 tests passed with overall status all_passed. |
| `README.md` | Dashboard documentation, API endpoints, and usage guide. |

All validation tests passed, including system metrics collection, Ollama server status check, and API endpoint accessibility. The web server starts and serves the dashboard correctly on port 5000.

## Compliance Audit (Prompt 5)

The completed Prompt 5 compliance audit is available in the `compliance_test/` directory:

| Document | Description |
| --- | --- |
| `csv_reader.py` | CSV file reader with type-safe dictionary output. |
| `csv_parser.py` | Type conversion parser (int, float, str, bool) with edge case handling. |
| `csv_processor.py` | Filtering and type-preserving transformation of parsed data. |
| `csv_validator.py` | Validation of records for type consistency and integrity. |
| `csv_reporter.py` | Compliance report generation with summary statistics. |
| `run_pipeline.py` | Pipeline orchestration script generating COMPLIANCE_AUDIT.md. |
| `COMPLIANCE_AUDIT.md` | Compliance audit report — all 12 records compliant. |
| `sample_data.csv` | Sample CSV data for pipeline testing. |

All five modules use type hints, logging, and English only. The pipeline processed 12 records, all passed validation, and generated a **compliant** status report.

## GitHub Issue Triage (Prompt 6)

The completed Prompt 6 real junior developer test is available in the `github_issue_triage/` directory:

| Document | Description |
| --- | --- |
| `main.py` | Main application entry point that reads issues from the sample JSON file, categorizes them into bug, enhancement, documentation, and security categories, generates summary statistics, charts, and markdown reports. |
| `requirements.txt` | Declares dependencies for the triage application. |
| `run_tests.py` | Custom test runner that discovers and executes all `test_*` functions without requiring pytest.
| `conftest.py` | Test configuration and fixtures for the triage test suite. |
| `data/issues.json` | Sample issues dataset used for categorization and reporting. |
| `src/issue_triage/` | Clean architecture package containing `models.py` (data models), `categorizer.py` (keyword-based issue classification), `charts.py` (matplotlib chart generation), `reporter.py` (markdown report generation), and `stats.py` (statistical summaries). |
| `tests/` | Test suite with `test_categorizer.py`, `test_reporter.py`, and `test_stats.py` covering categorization, reporting, and statistics. |
| `docs/design_decisions.md` | Design decisions documentation for the triage application. |
| `charts/` | Generated category distribution and count charts (excluded from version control via `.gitignore`). |
| `REPORT.md` | Generated markdown report with categorized issues, statistics, and charts. |

All modules use type hints, logging, and English only. The custom test runner discovered and executed all 19 test functions, all passing successfully. The application correctly categorizes all sample issues into bug, enhancement, documentation, and security categories using clean architecture principles.

## Usage

### Starting the Environment

```bash
# Clone or locate this directory
cd opencode_test

# Run the launcher script (requires `bash`, `ollama`, and `curl` in PATH)
./run.sh
```

The script will:
1. Start or connect to the Ollama server
2. Pull the `SparkLLM/Spark-X2.5-4B:latest` model if needed
3. Verify model availability
4. Launch OpenCode with the local model

### Running Benchmark Tasks

The `memory_stress_test/` directory contains a completed GPU/CPU/memory stress benchmark:

```bash
cd test_prompts/memory_stress_test
.venv/bin/python benchmark.py
```

This generates graphs, saves results, and produces a comprehensive REPORT.md with methodology, results, bottleneck analysis, and recommendations.

## Configuration

### Ollama Server
- **Host:** `127.0.0.1:11434` (default)
- **Context length:** 65536 tokens
- **Model:** `SparkLLM/Spark-X2.5-4B:latest`

### Environment Variables
Set the following variables, with these defaults:

```bash
OLLAMA_HOST="127.0.0.1:11434"
OLLAMA_CONTEXT_LENGTH="65536"
OLLAMA_MODEL="SparkLLM/Spark-X2.5-4B:latest"
OPENCODE_MODEL="ollama/${OLLAMA_MODEL}"
OLLAMA_LOG="./ollama.log"
```

## Requirements

The environment requires:
- **Python** 3.14+ (for virtual environment)
- **Ollama** server with the `SparkLLM/Spark-X2.5-4B:latest` model
- **curl** and **bash** utilities

For the memory stress benchmark specifically:
- `matplotlib >= 3.7.0`
- `numpy >= 1.24.0`

See `opencode_test/test_prompts/memory_stress_test/requirements.txt` for the complete dependency list.

## Notes

- **Language:** All comments, documentation, and responses are in English only.
- **Language Lock:** The English-only rule takes priority over all other stylistic preferences.
- **Sensitive Files:** Virtual environments (`.venv/`) and generated artifacts are excluded from version control via `.gitignore`.
- **Reproducibility:** The launcher script ensures deterministic execution by checking model availability before proceeding.

## License

This project is for testing and evaluation purposes. All output and benchmark results are generated locally and should be treated as reproducible testing artifacts.
