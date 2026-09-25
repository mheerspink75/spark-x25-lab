Perform a comprehensive, read-only audit of the entire current project.

Primary goal:
Stress-test the model's long-context comprehension, instruction retention, evidence tracking, and ability to analyze relationships across many files.

Critical constraints:

1. Always respond and write files in English.
2. Do not modify, rename, move, or delete any existing file or directory.
3. Create exactly one new directory named prompt7_comprehensive_audit.
4. Write every generated artifact inside prompt7_comprehensive_audit.
5. Do not install packages or alter the system configuration.
6. Do not expose secrets, credentials, API keys, tokens, or private data.
7. Do not invent findings. Clearly label anything that cannot be verified.
8. Do not repeat plans, status updates, or statements of intent.
9. Perform each tool action only once unless a retry is necessary because the action failed.
10. After a tool result, either perform the next required action or provide the final response. Do not emit multiple consecutive assistant messages without an intervening user or tool message.

Audit scope:

Analyze all relevant source code, configuration files, scripts, documentation, tests, dependency files, and logs available within the current project.

Ignore generated or irrelevant content unless needed to support a finding, including:

- virtual environments
- node_modules
- build artifacts
- cache directories
- binary files
- version-control internals
- generated benchmark output
- large log files that are not relevant to the audit

Create these files inside prompt7_comprehensive_audit:

1. PROJECT_INVENTORY.md
2. CODE_QUALITY.md
3. PERFORMANCE_REVIEW.md
4. DEPENDENCY_AUDIT.md
5. SECURITY_AUDIT.md
6. ARCHITECTURE_REVIEW.md
7. IMPLEMENTATION_ROADMAP.md
8. CONTEXT_RETENTION_AUDIT.md
9. AUDIT_SUMMARY.md

Requirements for PROJECT_INVENTORY.md:

- List every relevant file examined.
- Group files by purpose.
- Describe the likely responsibility of each file.
- Identify relationships and dependencies between files.
- Record files that could not be examined and explain why.

Requirements for CODE_QUALITY.md:

- Evaluate structure, readability, maintainability, duplication, error handling, logging, naming, typing, testing, and documentation.
- Cite exact file paths for every finding.
- Include concrete examples without copying excessive source code.
- Separate verified findings from suggestions.

Requirements for PERFORMANCE_REVIEW.md:

- Identify likely CPU, memory, disk I/O, network, startup, inference, context-management, and concurrency bottlenecks.
- Examine benchmark code and results if present.
- Check calculations for internal consistency.
- Distinguish measured results from estimates.
- Identify misleading metrics or unsupported performance claims.
- Recommend additional benchmarks where evidence is insufficient.

Requirements for DEPENDENCY_AUDIT.md:

- Inventory direct dependencies.
- Identify unused, duplicated, missing, or unnecessary dependencies.
- Identify version-pinning and reproducibility concerns.
- Explain the role of each important dependency.
- Do not claim that a dependency is vulnerable unless project evidence supports that conclusion.

Requirements for SECURITY_AUDIT.md:

- Review configuration handling, credentials, permissions, subprocess usage, shell commands, file paths, networking, logging, local API exposure, and input validation.
- Identify secrets or sensitive values only by file and category.
- Never reproduce secret values.
- Rank findings as Critical, High, Medium, Low, or Informational.
- Explain the evidence, impact, and recommended mitigation for every finding.

Requirements for ARCHITECTURE_REVIEW.md:

- Explain the system's components and data flow.
- Describe how configuration, startup scripts, OpenCode, Ollama, the local model, benchmark scripts, logs, and generated reports interact.
- Include a Mermaid architecture diagram.
- Identify coupling, unclear boundaries, duplicated configuration, and potential failure points.
- Cite relevant file paths for each architectural conclusion.

Requirements for IMPLEMENTATION_ROADMAP.md:

- Organize recommendations into:
  - Immediate
  - Short term
  - Medium term
  - Optional
- For every recommendation include:
  - supporting evidence
  - affected files
  - expected benefit
  - possible risk
  - implementation steps
  - validation procedure
  - rollback procedure
- Do not apply any recommendation automatically.

Requirements for CONTEXT_RETENTION_AUDIT.md:

At the end of the task, verify whether all original instructions were retained.

Create a checklist covering:

- English-only output
- read-only handling of existing files
- exactly one new directory
- all outputs stored in prompt7_comprehensive_audit
- no invented findings
- evidence supplied for conclusions
- no secret values reproduced
- all nine required files created
- no repeated status messages
- no existing files modified

For each item, record:

- PASS
- FAIL
- NOT VERIFIED

Include evidence for the result.

Requirements for AUDIT_SUMMARY.md:

- Provide an executive summary.
- List the ten most important verified findings.
- Identify the five highest-priority recommendations.
- Summarize important limitations.
- Link to the other generated audit documents using relative Markdown links.
- State whether the audit completed successfully.

Execution procedure:

1. Inspect the project structure.
2. Create prompt7_comprehensive_audit.
3. Analyze relevant files in logical groups.
4. Track evidence and file paths while analyzing.
5. Generate the nine required Markdown files.
6. Verify that no pre-existing files changed.
7. Verify that all required outputs exist.
8. Complete CONTEXT_RETENTION_AUDIT.md.
9. Provide one concise final response containing:
   - completion status
   - output directory
   - files created
   - whether existing files remained unchanged
   - any important limitations

Do not narrate every action. Do not repeatedly announce what you are about to do. Work through the task using tool calls, then provide one final summary.