# Risk Assessment

This document identifies the top five risks in the OpenCode Test Project workspace, with detailed evidence from project files and actionable mitigation plans. All findings are based on direct evidence from the project's configuration, scripts, prompts, and benchmark files.

## Risk Summary

| # | Risk | Severity | Evidence |
| --- | --- | --- | --- |
| 1 | Ollama Server Dependency & Startup Variability | High | `run.sh` starts Ollama server with 30-second readiness wait, depends on external service |
| 2 | Shell Command Injection / Security in `run.sh` | Critical | `run.sh` uses `$(...)` substitution for JSON payload construction in `curl` commands |
| 3 | Context Window Exhaustion in OpenCode Sessions | High | `num_ctx` = 65536, `num_predict` = 512 — no monitoring or checkpointing |
| 4 | Test Prompt Auto-Execution & File Modification Risk | High | Test prompts are designed for OpenCode execution but lack auto-validation of file changes |
| 5 | Resource Contention & Performance Degradation | Medium | `run.sh` and `benchmark.py` run concurrently, consuming CPU/memory without isolation |

---

## Risk 1: Ollama Server Dependency & Startup Variability

### Description

The `run.sh` launcher script depends on an external **Ollama server** that must be running before OpenCode can execute. If Ollama is not running or the target model (`SparkLLM/Spark-X2.5-4B:latest`) is unavailable, the script initiates a 30-second readiness wait loop and exits on failure. This creates a non-deterministic startup path dependent on external infrastructure.

### Evidence

- **`run.sh`:** The script checks `curl -fsS "http://${OLLAMA_HOST}/api/tags"` to detect server availability. If the server is not ready after 30 iterations (`seq 1 30`), it exits with an error and tails `ollama.log` for diagnostics.
- **`opencode.json`:** Specifies `baseURL: http://127.0.0.1:11434/v1` and model `SparkLLM/Spark-X2.5-4B:latest`.
- **`assistant-settings.md`:** Confirms the environment depends on Ollama for model execution.
- **`README.md`:** States Ollama server with `SparkLLM/Spark-X2.5-4B:latest` model is required.

### Impact

- **High:** Startup failures are non-deterministic and depend on external service availability. The 30-second wait is a poor fallback for slow or unresponsive servers.
- **Low-to-Medium:** If Ollama is pre-configured, the risk is reduced, but any network or service issue causes the entire workflow to halt.

### Mitigation Plan

1. **Pre-Validation:** Add an explicit pre-check for Ollama server availability and model presence before initiating the launcher, failing fast with clear error messages.
2. **Improved Readiness Logic:** Reduce or remove the fixed 30-second wait; instead, poll the server API with exponential backoff and a configurable timeout.
3. **Model Pre-Pull:** Optionally pre-pull the model during setup to reduce startup variability.
4. **Enhanced Logging:** Improve `ollama.log` capture and provide clearer error messages with log excerpts on failure.

---

## Risk 2: Shell Command Injection / Security in `run.sh`

### Description

`run.sh` constructs JSON payloads for `curl` API calls using `$(...)` command substitution:

```bash
response="$(curl -fsS "http://${OLLAMA_HOST}/api/generate" \
    -H "Content-Type: application/json" \
    -d "$(printf '{"model":"%s","prompt":"Reply with OK.","stream":false,"options":{"num_ctx":%s}}' \
        "${OLLAMA_MODEL}" "${OLLAMA_CONTEXT_LENGTH}")"
```

This approach interpolates variable values directly into shell command strings. If `OLLAMA_MODEL` or `OLLAMA_CONTEXT_LENGTH` contains unexpected or malicious content, the constructed command string could be malformed, leading to command injection or unexpected API responses.

### Evidence

- **`run.sh`:** The `curl` command uses `-d "$(printf ... "${OLLAMA_MODEL}" "${OLLUTO_CONTEXT_LENGTH}")"` pattern, interpolating model name and context length directly into shell commands.
- **`opencode.json`:** Model name contains spaces (`SparkLLM/Spark-X2.5-4B:latest`), which is safe when properly quoted but increases the surface for injection if quoting is not maintained.
- **`set -euo pipefail`:** The script enforces strict mode, which improves safety but does not prevent injection in command construction.

### Impact

- **Critical:** Potential command injection vulnerability in the health check and model test steps. This could lead to unauthorized command execution or unauthorized API calls.
- **Medium:** Malformed JSON payloads could cause the health check to fail or return unexpected responses, disrupting workflow.

### Mitigation Plan

1. **Avoid Shell Interpolation:** Replace `$(...)` substitution with parameterized API calls or JSON construction that avoids shell command string assembly.
2. **Input Validation:** Validate `OLLAMA_MODEL`, `OLLAMA_CONTEXT_LENGTH`, and all environment variables against expected patterns (e.g., regex for model names) before use.
3. **Quoted Variable Handling:** Ensure all variable interpolations are properly quoted to prevent unintentional shell interpretation.
4. **Defense in Depth:** Add pre-validation of constructed commands against a whitelist of safe patterns before execution.

---

## Risk 3: Context Window Exhaustion in OpenCode Sessions

### Description

The project configures a 65536 token context window with a 512-token maximum prediction (`num_ctx: 65536`, `num_predict: 512`) in `opencode.json`. For long-running OpenCode sessions that accumulate significant context, this window can be exhausted, potentially losing earlier instructions, context, or state.

### Evidence

- **`opencode.json`:** `"num_ctx": 65536` and `"num_predict": 512` for the `SparkLLM/Spark-X2.5-4B:latest` model.
- **`run.sh`:** Runs OpenCode with `${OPENCODE_MODEL}` which resolves to the configured model; no context monitoring or checkpointing is implemented.
- **`README.md`:** States context length of 65536 tokens and model `SparkLLM/Spark-X2.5-4B:latest`.

### Impact

- **High:** Long-running agent sessions may exceed the 65536 token limit, causing context truncation, loss of earlier instructions, and potential workflow failures.
- **Medium:** Exhausted context could degrade response quality or cause the agent to operate on incomplete state.

### Mitigation Plan

1. **Context Monitoring:** Add monitoring for context usage during OpenCode execution, alerting when context approaches the limit.
2. **Checkpointing:** Implement session checkpointing or context compression to preserve earlier instructions and state within the window.
3. **Configurable Limits:** Allow adjustable context window and prediction limits via environment variables with validation.
4. **Session Truncation Strategy:** Define a policy for context truncation (e.g., sliding window) to minimize information loss.

---

## Risk 4: Test Prompt Auto-Execution & File Modification Risk

### Description

The test prompts in `test_prompts/` are designed for sequential OpenCode execution but do not automatically validate that existing project files remain unmodified. Prompts like prompt 3 and 4 explicitly state "Do not modify existing files" / "Do not modify files outside this directory," but the automated execution process lacks verification mechanisms to confirm no unintended modifications occur.

### Evidence

- **`test_prompts/3_refactoring_challenge.md`:** States "Do not modify existing project files" and requires creating new directories only.
- **`test_prompts/4_autonomous_coding.md`:** States "Do not modify files outside this directory."
- **`test_prompts/7_stress_test_the_65k_context_window.md`:** Enforces "Do not modify, rename, move, or delete any existing file or directory" and "Verify that no pre-existing files changed."
- **`architecture_review/PROJECT_INVENTORY.md`:** Notes test prompt coherence with sequential execution on the same workspace.

### Impact

- **High:** Automated test execution could inadvertently modify or alter project files, compromising the integrity of the test environment and potentially corrupting artifacts.
- **Medium:** Unintended file changes could make test results invalid or misleading, reducing the reliability of benchmark evaluations.

### Mitigation Plan

1. **Pre-Execution Checks:** Before running test prompts, verify the project's file integrity (checksums or file lists) and pass as a pre-condition.
2. **Post-Execution Validation:** After each test prompt execution, compare the current file state against the pre-execution baseline to detect any modifications.
3. **Explicit Constraints:** Reiterate read-only constraints in test prompt design and verify them at execution time.
4. **Automated Rollback:** Implement rollback mechanisms that restore project files to their original state if unintended modifications are detected.

---

## Risk 5: Resource Contention & Performance Degradation

### Description

The system runs two resource-intensive components concurrently: the `run.sh` launcher (which starts and monitors the Ollama server) and the `benchmark.py` application (which performs multithreaded CPU/memory/file I/O benchmarks). Both consume CPU and memory simultaneously without explicit resource isolation or monitoring.

### Evidence

- **`run.sh`:** Starts `ollama serve` in the background, polls the server, and uses CPU-intensive model health checks.
- **`test_prompts/memory_stress_test/benchmark.py`:** Uses `THREAD_COUNT = 4` and `CPU_CORES = 4`, performing multithreaded memory stress and CPU benchmarks.
- **`opencode.json`:** Configures 65536 context window and 512 prediction, which also consume resources during execution.
- **`requirements.txt`:** Declares `numpy` and `matplotlib` as dependencies, which have memory overhead.

### Impact

- **Medium:** Concurrent execution can lead to CPU/memory contention, causing performance degradation, slower responses, or even system instability if resources are limited.
- **Low-to-Medium:** Resource exhaustion could cause the benchmark or server to fail or timeout, affecting test reproducibility.

### Mitigation Plan

1. **Resource Monitoring:** Add CPU/memory usage monitoring during concurrent execution and alert when thresholds are approached.
2. **Resource Isolation:** Run the benchmark and Ollama server in separate processes or containers with resource limits (e.g., cgroups or process isolation).
3. **Sequential Execution:** Consider executing benchmark and server operations sequentially when not in active parallel need.
4. **Configurable Limits:** Allow tuning of `CPU_CORES`, `THREAD_COUNT`, and memory allocation in `benchmark.py` and `run.sh` with validation.

---

## Risk Priority Matrix

| Risk | Severity | Likelihood | Priority |
| --- | --- | --- | --- |
| 2. Shell Command Injection (`run.sh`) | Critical | Medium | **P0** |
| 3. Context Window Exhaustion | High | Medium | **P0** |
| 1. Ollama Server Dependency & Startup | High | Medium | **P1** |
| 4. Test Prompt Modification Risk | High | Low | **P1** |
| 5. Resource Contention | Medium | Medium | **P2** |

## Summary

The top risk is **Shell Command Injection in `run.sh`** (Critical), due to unsafe `$(...)` substitution in curl command construction. **Context Window Exhaustion** (High) is the second highest risk, stemming from the 65536 token limit with no monitoring. Both are addressed by input validation, command construction safeguards, and context management. The Ollama server dependency and test prompt modification risks are also High severity, mitigated by pre-validation, post-validation, and resource isolation. All mitigation plans are evidence-based, citing specific files and code patterns from the project.

---

*Document generated as part of Prompt 2 (Long Context Research) — Risk Assessment. Evidence cited from: `run.sh`, `opencode.json`, `assistant-settings.md`, `test_prompts/*.md`, `test_prompts/memory_stress_test/benchmark.py`, `requirements.txt`, `README.md`, `architecture_review/PROJECT_INVENTORY.md`.*
