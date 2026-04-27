---
name: obsidian-environment-reproducibility
description: Keep project work reproducible across clean checkout, dependencies, Python versions, CI, MT5 paths, external artifacts, and local machine assumptions.
---

# Obsidian Environment Reproducibility

Use this skill when work touches tests, README commands, dependency setup, CI, clean checkout behavior, MT5 terminal paths, local absolute paths, external artifacts, or instructions another machine must run.

## Required Output

- `execution_environment`: OS, Python, MT5, broker terminal, or CI context when relevant
- `dependency_surface`: packages, versions, tools, and missing install contract
- `entry_command`: command a clean checkout should run
- `local_assumptions`: absolute paths, terminal data roots, environment variables, or machine-only files
- `clean_checkout_status`: expected to pass, expected blocked, not tested, or not applicable
- `recovery_instruction`: install, configure, fetch artifact, regenerate, or user action
- `reproducibility_judgment`: reproducible, reproducible_with_setup, local_only, inconclusive, or blocked

## Guardrails

- Do not document a test command as default if dependencies are not declared.
- Do not rely on repository location to discover MT5 data roots without a fail-fast check or configuration path.
- Do not describe missing artifacts as reproducible unless fetch or regeneration steps exist.
