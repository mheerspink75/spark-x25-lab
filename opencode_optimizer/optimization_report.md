# Optimization Report — OpenCode & Ollama Configuration

This report analyzes the current OpenCode and Ollama configuration and presents optimized recommendations to reduce startup time, improve context utilization, minimize VRAM waste, and maximize coding throughput. All changes are proposed for review and **do not apply modifications to existing project files automatically**, per task requirements.

## Current Configuration Summary

| Parameter | Current Value | Source |
| --- | --- | --- |
| Model | `ollama/SparkLLM/Spark-X2.5-4B:latest` | `opencode.json` |
| Provider | Ollama at `http://127.0.0.1:11434/v1` | `opencode.json` |
| Context Window | 65536 tokens | `opencode.json` |
| Max Prediction | 512 | `opencode.json` |
| Tools | Disabled (`false`) | `opencode.json` |
| Startup Wait | 30 seconds (max) | `run.sh` |
| Server Startup | Automatic if not running | `run.sh` |

## Recommendations

### 1. Reduce Startup Time

| Field | Detail |
| --- | --- |
| **Expected Benefit** | Drastically reduce initial server and model readiness wait times, improving overall workflow responsiveness. |
| **Tradeoffs** | Slightly increased pre-validation overhead; requires ensuring pre-checks are fast and non-blocking. |
| **Implementation Steps** | 1. In `run.sh`, replace the fixed 30-second readiness wait loop with a configurable timeout (e.g., 10 seconds) and exponential backoff polling. 2. Add a pre-validation step that checks server API availability and model presence before initiating the full launch sequence. 3. Support parallel pre-checks for server and model availability. 4. Update `run.sh` to read startup timing parameters from environment variables or the proposed config. |
| **Rollback Procedure** | Revert `run.sh` to the original 30-second wait loop; remove pre-validation checks; restore original timeout values. Re-run the launcher to restore previous behavior. |

### 2. Improve Context Utilization

| Field | Detail |
| --- | --- |
| **Expected Benefit** | Better retention of long-running session state, reducing context truncation and information loss. |
| **Tradeoffs** | May require larger memory allocation for context compression/checkpointing; slightly reduced raw token capacity. |
| **Implementation Steps** | 1. Enable context compression and checkpointing in `opencode.json` (currently both are unconfigured). 2. Set a fallback context window (e.g., 32768 tokens) for scenarios where 65536 tokens are insufficient. 3. Ensure the model's `num_ctx` and `num_predict` values are aligned with the configured window. 4. Implement periodic context state saving during long-running agent sessions. |
| **Rollback Procedure** | Disable context compression and checkpointing in `opencode.json`; revert `num_ctx` and `num_predict` to original values; remove fallback window configuration. |

### 3. Minimize VRAM Waste

| Field | Detail |
| --- | --- |
| **Expected Benefit** | Reduce memory overhead from the large 4B model, freeing VRAM for other tasks and preventing OOM errors. |
| **Tradeoffs** | Possible performance degradation from quantized inference; requires model availability in quantized format. |
| **Implementation Steps** | 1. Enable model int8 quantization in `opencode.json` memory and VRAM settings. 2. Set memory-efficient and VRAM-aware modes in the configuration. 3. Reduce unnecessary memory allocations during benchmark and server operations. 4. Verify that the quantized model is available and compatible with the Ollama server. |
| **Rollback Procedure** | Disable quantization and memory-efficient modes in `opencode.json`; revert to full-precision model settings; remove VRAM-aware allocations. |

### 4. Maximize Coding Throughput

| Field | Detail |
| --- | --- |
| **Expected Benefit** | Enable targeted tool use during coding, improving agent responsiveness, file operations, and task completion efficiency. |
| **Tradeoffs** | Tool execution may introduce additional latency for certain operations; requires careful scope management to avoid over-trusting tools. |
| **Implementation Steps** | 1. Enable tool use in `opencode.json` (`tools: true`), scoped to coding and file operations. 2. Maintain `num_predict: 512` to preserve response quality. 3. Ensure the model supports tool execution (verified via `opencode list` and Ollama model metadata). 4. Configure tool scope to minimize unnecessary tool invocations during standard coding tasks. |
| **Rollback Procedure** | Disable tools in `opencode.json`; revert tool scope to the original disabled state; ensure no tool execution is triggered during launch or health checks. |

## Overall Optimization Strategy

The proposed configuration addresses all four optimization goals simultaneously:

1. **Startup:** Pre-validation and reduced readiness timeout minimize initial wait times.
2. **Context:** Compression, checkpointing, and fallback windows protect session state from truncation.
3. **VRAM:** Quantization and memory-efficient modes reduce resource overhead.
4. **Throughput:** Tool enablement with scoped execution improves agent coding efficiency.

All changes are documented in [proposed_config.json](proposed_config.json) and this report, and **no existing project files are modified automatically** as required.

---

*Document generated as part of Prompt 3 (Refactoring Challenge) — Optimization Report. All analysis based on current project files: `opencode.json`, `run.sh`, `assistant-settings.md`, `.gitignore`, `test_prompts/*`, and `architecture_review/PROJECT_INVENTORY.md`.*
