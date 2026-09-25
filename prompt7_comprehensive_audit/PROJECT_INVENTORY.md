# Project Inventory

This document provides a complete inventory of every relevant file examined during the comprehensive stress test audit for the Spark-X2.5-4B test lab. Files are grouped by purpose, each described by its likely responsibility, and relationships and dependencies between files are documented. Files that could not be examined are recorded with an explanation.

## Files by Purpose

### Top-Level Configuration & Project Files

| File | Purpose |
| --- | --- |
| `.gitignore` | Git ignore rules that exclude virtual environments, Python caches, benchmark artifacts, logs, and editor/OS files to keep the repository clean and version-controlled. |
| `assistant-settings.md` | Language lock and response policy mandating English-only responses, with the English rule given priority over all other stylistic preferences. |
| `opencode.json` | OpenCode configuration specifying the local Ollama model, provider URL, context window (65536 tokens), maximum prediction (512), and tool/tool-reasoning settings. |
| `run.sh` | Bash launcher script that checks for required binaries, starts or connects to the Ollama server, verifies the model is installed, runs a model health check, and launches OpenCode with the configured model. |
| `LICENSE` | MIT license (Copyright 2026 Matt Heerspink) governing the use, distribution, and licensing of the project. |
| `README.md` | Workspace-level documentation tracking all prompt outputs, configuration details, usage instructions, and the directory structure. |

### Test Prompts

| File | Purpose |
| --- | --- |
| `test_prompts/1_software_engineering_agent.md` | Spec for the memory stress benchmark prompt: creates a `prompt1_memory_stress_test/` directory with executable benchmark code, graphs, report, and requirements. |
| `test_prompts/2_long_context_research.md` | Spec for the long context research prompt: analyzes all project files and produces an architecture review (`prompt2_architecture_review/`). |
| `test_prompts/3_refactoring_challenge.md` | Spec for the refactoring challenge prompt: creates an `prompt3_opencode_optimizer/` directory with configuration and optimization artifacts (no auto-application). |
| `test_prompts/4_autonomous_coding.md` | Spec for the autonomous coding prompt: generates a `prompt4_local_web_dashboard/` Flask app with system resource monitoring and validation tests. |
| `test_prompts/5_agent_memory_test.md` | Spec for the agent memory test prompt: creates a `prompt5_compliance_test/` directory with five CSV-processing Python modules and a compliance audit. |
| `test_prompts/6_real_junior_developer_test.md` | Spec for the real junior developer test prompt: builds a `prompt6_github_issue_triage/` application for issue categorization, statistics, charts, and reports. |
| `test_prompts/7_stress_test_the_65k_context_window.md` | Spec for the comprehensive stress test audit prompt: performs a read-only audit and generates nine Markdown artifacts in `prompt7_comprehensive_audit/`. |
| `test_prompts/prompt1_memory_stress_test/benchmark.py` | Python benchmark application simulating resource consumption across CPU, memory, file I/O, and multithreading to validate the memory stress scenario. |
| `test_prompts/prompt1_memory_stress_test/requirements.txt` | Declares benchmark dependencies: `matplotlib>=3.7.0` and `numpy>=1.24.0`. |
| `test_prompts/prompt1_memory_stress_test/REPORT.md` | Comprehensive benchmark report covering methodology, results, bottleneck analysis, and recommendations. |

### Prompt 2 Output (Architecture Review)

| File | Purpose |
| --- | --- |
| `prompt2_architecture_review/PROJECT_INVENTORY.md` | Inventory of all project files grouped by purpose, with dependencies, relationships, and cross-references. |
| `prompt2_architecture_review/ARCHITECTURE_REVIEW.md` | Architecture analysis covering components, data flow, Mermaid diagram, coupling, boundaries, and failure points. |
| `prompt2_architecture_review/RISK_ASSESSMENT.md` | Top five risks with evidence from project files and detailed mitigation plans. |

### Prompt 5 Output (Compliance Audit)

| File | Purpose |
| --- | --- |
| `prompt5_compliance_test/COMPLIANCE_AUDIT.md` | Compliance audit report covering the CSV pipeline validation and compliance status. |
| `prompt5_compliance_test/csv_reader.py` | CSV file reader module converting CSV data into type-safe dictionary structures. |
| `prompt5_compliance_test/csv_parser.py` | Type conversion parser handling int, float, str, and bool values with edge case handling. |
| `prompt5_compliance_test/csv_processor.py` | Filtering and type-preserving transformation of parsed CSV data. |
| `prompt5_compliance_test/csv_validator.py` | Validation of records for type consistency and integrity. |
| `prompt5_compliance_test/csv_reporter.py` | Compliance report generation with summary statistics. |
| `prompt5_compliance_test/run_pipeline.py` | Pipeline orchestration script generating the compliance audit report. |
| `prompt5_compliance_test/sample_data.csv` | Sample CSV data (12 records) used for pipeline testing. |

### Prompt 3 Output (Optimization)

| File | Purpose |
| --- | --- |
| `prompt3_opencode_optimizer/proposed_config.json` | Optimized OpenCode + Ollama configuration addressing startup, context, VRAM, and throughput; proposed for review only. |
| `prompt3_opencode_optimizer/optimization_report.md` | Detailed optimization recommendations with expected benefit, tradeoffs, implementation steps, and rollback procedures. |

### Prompt 4 Output (Web Dashboard)

| File | Purpose |
| --- | --- |
| `prompt4_local_web_dashboard/dashboard.py` | Flask web application displaying real-time CPU, RAM, disk usage, and Ollama server status, with validation tests via `dashboard.py --test`. |
| `prompt4_local_web_dashboard/requirements.txt` | Declares dashboard dependencies: Flask and psutil. |
| `prompt4_local_web_dashboard/TEST_RESULTS.md` | Validation test outcomes documenting all passing tests and overall status. |
| `prompt4_local_web_dashboard/README.md` | Dashboard documentation, API endpoints, and usage guide. |

### Prompt 6 Output (GitHub Issue Triage)

| File | Purpose |
| --- | --- |
| `prompt6_github_issue_triage/.gitignore` | Local ignore rules for the triage project. |
| `prompt6_github_issue_triage/README.md` | Project documentation for the triage application. |
| `prompt6_github_issue_triage/REPORT.md` | Generated markdown report with categorized issues, statistics, and charts. |
| `prompt6_github_issue_triage/run_tests.py` | Custom test runner that discovers and executes all `test_*` functions without requiring pytest. |
| `prompt6_github_issue_triage/conftest.py` | Test configuration and fixtures for the triage test suite. |
| `prompt6_github_issue_triage/data/issues.json` | Sample issues dataset used for categorization and reporting. |
| `prompt6_github_issue_triage/requirements.txt` | Declares dependencies for the triage application. |
| `prompt6_github_issue_triage/docs/design_decisions.md` | Design decisions documentation for the triage application. |
| `prompt6_github_issue_triage/main.py` | Main application entry point orchestrating load, categorize, stats, charts, and report generation. |
| `prompt6_github_issue_triage/src/issue_triage/__init__.py` | Package initialization for the issue triage module. |
| `prompt6_github_issue_triage/src/issue_triage/categorizer.py` | Keyword-based issue classification module. |
| `prompt6_github_issue_triage/src/issue_triage/charts.py` | Matplotlib-based chart generation module for category visualizations. |
| `prompt6_github_issue_triage/src/issue_triage/models.py` | Data models (`Issue`, `IssueCategory`, `IssueStats`) using dataclasses and Enum. |
| `prompt6_github_issue_triage/src/issue_triage/reporter.py` | Markdown report generation module. |
| `prompt6_github_issue_triage/src/issue_triage/stats.py` | Statistical summary generation and report snapshot building. |
| `prompt6_github_issue_triage/tests/__init__.py` | Test package initialization. |
| `prompt6_github_issue_triage/tests/test_categorizer.py` | Test suite for the categorizer module. |
| `prompt6_github_issue_triage/tests/test_reporter.py` | Test suite for the reporter module. |
| `prompt6_github_issue_triage/tests/test_stats.py` | Test suite for the statistics module. |
| `prompt6_github_issue_triage/charts/category_counts.png` | Generated category count chart (generated artifact, excluded from version control). |
| `prompt6_github_issue_triage/charts/category_distribution.png` | Generated category distribution chart (generated artifact, excluded from version control). |

### Prompt 1 Output (Memory Stress Benchmark)

| File | Purpose |
| --- | --- |
| `test_prompts/prompt1_memory_stress_test/benchmark.py` | Python benchmark application simulating CPU, memory, file I/O, and multithreaded resource consumption. |
| `test_prompts/prompt1_memory_stress_test/REPORT.md` | Comprehensive benchmark report with methodology, results, and bottleneck analysis. |
| `test_prompts/prompt1_memory_stress_test/requirements.txt` | Benchmark dependencies: `matplotlib>=3.7.0`, `numpy>=1.24.0`. |

### Prompt 7 Output (Comprehensive Audit)

| File | Purpose |
| --- | --- |
| `prompt7_comprehensive_audit/PROJECT_INVENTORY.md` | Inventory of examined files grouped by purpose with responsibilities, dependencies, and unverifiable items. |
| `prompt7_comprehensive_audit/CODE_QUALITY.md` | Evaluation of structure, readability, maintainability, duplication, error handling, logging, naming, typing, testing, and documentation. |
| `prompt7_comprehensive_audit/PERFORMANCE_REVIEW.md` | Review of CPU, memory, disk I/O, network, startup, inference, context-management, and concurrency bottlenecks. |
| `prompt7_comprehensive_audit/DEPENDENCY_AUDIT.md` | Inventory of direct dependencies with analysis of unused, duplicated, missing, and unnecessary dependencies. |
| `prompt7_comprehensive_audit/SECURITY_AUDIT.md` | Review of configuration handling, credentials, permissions, subprocess, shell, file paths, networking, logging, API exposure, and input validation. |
| `prompt7_comprehensive_audit/ARCHITECTURE_REVIEW.md` | Architecture analysis with Mermaid diagram, data flow, coupling, boundaries, failure points, and file citations. |
| `prompt7_comprehensive_audit/IMPLEMENTATION_ROADMAP.md` | Recommendations organized by timeframe (Immediate, Short-term, Medium-term, Optional) with evidence, affected files, benefit, risk, steps, validation, and rollback. |
| `prompt7_comprehensive_audit/CONTEXT_RETENTION_AUDIT.md` | Verification of original instruction retention with PASS/FAIL/NOT VERIFIED checklist and evidence. |
| `prompt7_comprehensive_audit/AUDIT_SUMMARY.md` | Executive summary with ten key findings, five high-priority recommendations, limitations, and links to all audit documents. |

### Files That Could Not Be Examined

No files could not be examined. All relevant files within the project workspace were available and analyzed. Generated artifacts that are explicitly excluded from audit scope — virtual environments, Python caches, binary files, version-control internals, generated benchmark output, and large non-relevant log files — were not examined, consistent with the audit's read-only and scope-limited requirements.

### Relationships and Dependencies

- **Top-level orchestration:** `run.sh` depends on `opencode.json` (model configuration), `assistant-settings.md` (response policy), and `.gitignore` (version control constraints). It also requires `ollama` and `curl` binaries in the PATH.
- **Test prompt coherence:** All test prompts in `test_prompts/` are executed sequentially by OpenCode and operate on the same project workspace. Prompt 2's analysis leverages all other files (code, config, benchmark results, and generated reports) for its architecture review.
- **Benchmark dependency:** `benchmark.py` depends on `numpy` and `matplotlib` (declared in `requirements.txt`) and writes results to `.benchmark_results/`, which feeds the `REPORT.md` for documentation.
- **Module dependency:** The triage project (`prompt6_github_issue_triage/`) uses a clean package structure where `main.py` imports modules from `src/issue_triage/` (models, categorizer, charts, reporter, stats), and tests import from the package as well.
- **Cross-project consistency:** All prompt outputs (prompt2_architecture_review, prompt5_compliance_test, prompt3_opencode_optimizer, prompt4_local_web_dashboard, prompt6_github_issue_triage) reference the same project files (`opencode.json`, `run.sh`, `assistant-settings.md`, `.gitignore`, `test_prompts/*`, `prompt1_memory_stress_test/*`, `README.md`, `LICENSE`) to ensure evidence-based consistency across the audit scope.
- **Audit scope constraint:** The prompt7_comprehensive_audit directory contains read-only analysis documents that do not modify, rename, move, or delete any existing files, in accordance with the prompt's critical constraints.
