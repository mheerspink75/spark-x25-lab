# Spark-X2.5-4B Test Lab

A local testing environment for the Spark-X2.5-4B model, configured with a local Ollama-based LLM. This project is designed for automated testing, benchmarking, and code agent evaluation tasks, using both the **OpenCode CLI** and **LM Studio** for benchmark execution.

## Overview

This directory serves as the workspace for agent-based coding (OpenCode) workflows, running against a local Ollama-based LLM. It includes sequential test prompt directories (`prompt<number>_<folder_name>`), launch scripts, configuration files, and auxiliary utilities for reproducible agent testing and evaluation.

## Directory Structure

The project organizes all prompt-related output in a `prompt<number>_<folder_name>` convention, where the number corresponds to the prompt associated with that folder.

```
prompt1_memory_stress_test/
prompt2_architecture_review/
prompt3_opencode_optimizer/
prompt4_local_web_dashboard/
prompt5_compliance_test/
prompt6_github_issue_triage/
prompt7_comprehensive_audit/
test_prompts/
run.sh
opencode.json
ollama.log
README.md
LICENSE
assistant-settings.md
.gitignore
```

## Key Files

### `run.sh`

Launcher script that:
1. Starts or connects to the Ollama server
2. Pulls the `SparkLLM/Spark-X2.5-4B:latest` model if needed
3. Verifies model availability
4. Launches OpenCode with the local model

### `opencode.json`

OpenCode configuration file that specifies:
- **Model:** `ollama/SparkLLM/Spark-X2.5-4B:latest`
- **Provider:** Ollama running locally on `http://127.0.0.1:11434/v1`
- **Options:** 65536 context window, 512 max prediction

## Running Benchmark Tasks

The prompt-related test directories contain completed benchmarks:

```bash
cd prompt1_memory_stress_test
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

- **Python** 3.14+ (for virtual environments and generated code)
- **Ollama** server with the `SparkLLM/Spark-X2.5-4B:latest` model
- **curl** and **bash** utilities
- **OpenCode CLI** and **LM Studio** for benchmark execution

See `run.sh` and `opencode.json` for the complete dependency list.

## Notes

- **Language:** All comments, documentation, and responses are in English only.
- **Language Lock:** The English-only rule takes priority over all other stylistic preferences.
- **Sensitive Files:** Virtual environments and generated artifacts are excluded from version control via `.gitignore`.
- **Reproducibility:** The launcher script ensures deterministic execution by checking model availability before proceeding.
- **Benchmark Execution:** Benchmarking is performed using both the **OpenCode CLI** and **LM Studio**, covering memory stress, architecture review, compliance, and comprehensive audits.

## License

This project is for testing and evaluation purposes. All output and benchmark results are generated locally and should be treated as reproducible testing artifacts.
