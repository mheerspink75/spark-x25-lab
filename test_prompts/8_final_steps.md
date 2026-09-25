You are an autonomous coding agent working in the current project. Inspect the repository structure and relevant files before making changes. Complete all safe, unambiguous tasks without requesting confirmation.

# Objective

Reorganize the prompt-related test folders, rerun Prompt 1 in the correct location, and update the documentation so that every folder name, path, command, and benchmark detail is consistent.

# Current State

The project has already been reorganized into the `prompt<number>_<folder_name>` convention. All prompt-related folders are correctly named and located:

- `prompt1_memory_stress_test/`
- `prompt2_architecture_review/`
- `prompt3_opencode_optimizer/`
- `prompt4_local_web_dashboard/`
- `prompt5_compliance_test/`
- `prompt6_github_issue_triage/`
- `prompt7_comprehensive_audit/`
- `test_prompts/`

The project parent directory is `spark_x25_4b_test_lab`.

# Required Tasks

1. Locate the existing `prompt1_memory_stress_test` directory.

2. Confirm that `prompt1_memory_stress_test` is properly located at the project root with all its contents intact.

3. Rename every prompt-related folder using this convention:

   `prompt<number>_<folder_name>`

   The number must correspond to the prompt associated with that folder.

   Example:

   `memory_stress_test` → `prompt1_memory_stress_test`

4. Locate the exact instructions for Prompt 1 in the repository.

5. Verify that Prompt 1 output is present in the correct location.

6. Store the regenerated Prompt 1 output in:

   `prompt1_memory_stress_test/`

   Update or replace the previous Prompt 1 output as appropriate. Do not create a duplicate test folder.

7. Confirm that the project parent directory is `spark_x25_4b_test_lab` and contains all prompt-related folders.

8. Update `README.md` with the following changes:

   - Set the project title to `Spark-X2.5-4B Test Lab`.
   - Identify the benchmarked model as `SparkLLM/Spark-X2.5-4B:latest`.
   - State that the model is configured using the `OLLAMA_MODEL` environment variable.
   - State that the benchmark included testing with both the OpenCode CLI and LM Studio.
   - Update all affected folder names, paths, commands, examples, and directory-tree entries.
   - Replace obsolete references to `memory_stress_test` with `prompt1_memory_stress_test` where appropriate.
   - Do not mention `opencode_test`, the previous parent directory name, or any outdated parent directory in the README.

# Constraints

- Preserve unrelated files and existing content.
- Do not create duplicate folders.
- Do not create duplicate Prompt 1 output.
- Do not invent the Prompt 1 instructions.
- If Prompt 1 cannot be located, report every relevant location that was searched, skip only the Prompt 1 execution step, and continue with all other safe changes.
- Do not delete user-authored content unless it is obsolete because of the requested folder renaming or output regeneration.
- Keep all documented commands, configuration examples, and paths technically valid.
- Do not make unrelated code, dependency, configuration, or formatting changes.

# Verification

Before finishing:

1. Inspect the final directory tree.

2. Confirm that every prompt-related folder uses the required `prompt<number>_<folder_name>` naming convention.

3. Confirm that `prompt1_memory_stress_test` exists at the project root.

4. If Prompt 1 was found, confirm that `prompt1_memory_stress_test` contains the newly generated output.

5. Search the repository for obsolete references, including:

   - `memory_stress_test`
   - Previous prompt-folder names
   - Outdated paths
   - Incorrect model identifiers
   - References to the parent directory in `README.md`

6. Correct all affected obsolete references while preserving unrelated uses.

7. Confirm that `README.md` includes:

   - `Spark-X2.5-4B Test Lab`
   - `SparkLLM/Spark-X2.5-4B:latest`
   - `OLLAMA_MODEL`
   - OpenCode CLI
   - LM Studio

8. Stage all changes, commit them, and push to `origin/main`.

# Completion Report

When all work is finished, return a concise report containing:

1. Every file or folder that was moved, renamed, created, deleted, or updated.
2. The final relevant directory tree.
3. The location from which the Prompt 1 instructions were obtained.
4. The command or method used to complete the remaining steps.
5. Whether all obsolete references were resolved.
6. The validation commands or checks performed and their results.
7. Any task that could not be completed, including the exact reason and the safest next action.
<EOF>
