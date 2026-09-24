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

## Architecture Review (Prompt 2)

The completed Prompt 2 analysis is available in the `architecture_review/` directory:

| Document | Description |
| --- | --- |
| `PROJECT_INVENTORY.md` | Inventory of all project files grouped by purpose, with dependencies and relationships. |
| `ARCHITECTURE_REVIEW.md` | Architecture analysis covering components, data flow, Mermaid diagram, coupling, boundaries, and failure points.
| `RISK_ASSESSMENT.md` | Top 5 risks with evidence from project files and detailed mitigation plans.

All documents use evidence from the project files (`opencode.json`, `run.sh`, `assistant-settings.md`, `.gitignore`, `test_prompts/*`, `memory_stress_test/*`, `README.md`, `LICENSE`) rather than assumptions.

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
