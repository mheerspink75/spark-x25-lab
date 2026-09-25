# Project Inventory

This document inventory-lists every relevant file in the project, grouped by purpose, with its intended responsibility and relationships/dependencies between files.

## Files by Purpose

### Configuration & Launch

| File | Purpose |
| --- | --- |
| `opencode.json` | OpenCode configuration specifying the Ollama-based model, provider URL, context length, and prediction limits. |
| `run.sh` | Bash launcher script that starts or connects to the Ollama server, checks model availability, verifies model health, and launches OpenCode with the configured model. |
| `assistant-settings.md` | Language lock and response policy: mandates English-only responses with priority over all other stylistic preferences. |
| `.gitignore` | Ignores virtual environments, Python caches, benchmark artifacts, logs, and editor/OS files to keep the repository clean. |

### Test Prompts

| File | Purpose |
| --- | --- |
| `test_prompts/1_software_engineering_agent.md` | Specifies creating and completing a `prompt1_memory_stress_test` directory with executable code, graphs, report, and requirements. |
| `test_prompts/2_long_context_research.md` | This analysis prompt: analyzes all project files (markdown, JSON, shell, config) and produces an architecture review. |
| `test_prompts/3_refactoring_challenge.md` | Requires creating a `prompt3_opencode_optimizer` directory with config and optimization artifacts (no auto-application). |
| `test_prompts/4_autonomous_coding.md` | Generates a `prompt4_local_web_dashboard` Flask app with CPU/RAM/disk/Ollama status display and validation tests. |
| `test_prompts/5_agent_memory_test.md` | Creates a `prompt5_compliance_test` directory with five CSV-processing Python modules and compliance audits. |
| `test_prompts/6_real_junior_developer_test.md` | Builds a `prompt6_github_issue_triage` app for issue categorization, stats, charts, and markdown reporting. |
| `test_prompts/7_stress_test_the_65k_context_window.md` | Read-only project audit stress-testing model's long-context comprehension and evidence tracking. |

### Benchmark (prompt1_memory_stress_test)

| File | Purpose |
| --- | --- |
| `prompt1_memory_stress_test/benchmark.py` | Python benchmark application that measures CPU, memory, file I/O, and multithreaded performance under controlled stress. |
| `prompt1_memory_stress_test/requirements.txt` | Lists dependencies: `matplotlib` and `numpy` with minimum version constraints. |
| `prompt1_memory_stress_test/REPORT.md` | Comprehensive benchmark report covering methodology, results, graphs, bottleneck analysis, recommendations, and executive summary. |
| `prompt1_memory_stress_test/.benchmark_results/` | Generated benchmark output including summary JSON, per-metric result JSONs, and 5 PNG graphs. |

## Relationships and Dependencies

- **Top-level orchestration:** `run.sh` depends on `opencode.json` (model configuration) and `assistant-settings.md` (response policy). It also requires `ollama` and `curl` binaries in the PATH.
- **Test prompt coherence:** All test prompts in `test_prompts/` are executed sequentially by OpenCode and operate on the same project workspace. The `2_long_context_research.md` prompt leverages all other files (code, config, benchmark results) for its analysis.
- **Benchmark dependency:** `benchmark.py` depends on `numpy` and `matplotlib` (declared in `requirements.txt`). It writes results to `.benchmark_results/` which feeds the `REPORT.md` for documentation.
- **Infrastructure dependency:** The `.gitignore` constrains what is tracked by git, ensuring that generated benchmark artifacts and virtual environments do not pollute the repository history.

## Files Not Examined

No files could not be examined. All relevant files in the project were available and analyzed.
