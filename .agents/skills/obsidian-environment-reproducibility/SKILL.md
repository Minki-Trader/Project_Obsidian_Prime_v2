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
- On Windows(윈도우) deep stage path(깊은 단계 경로) or MT5 artifact path(MT5 산출물 경로), do not classify(분류) a file as missing(누락) or blocked(차단) after a single native PowerShell path failure(파워셸 경로 실패)만으로 판정하지 않는다. Retry(재시도)는 repo-relative path(저장소 상대 경로) `rg --files`/`rg`로 먼저 하고, long-path-safe read(긴 경로 안전 읽기) 또는 mechanical CSV/JSON rewrite(기계적 표/제이슨 수정)는 `foundation.control_plane.ledger.io_path`를 거쳐 수행한 뒤 missing(누락)을 기록한다.

Effect(효과): reproducibility notes(재현성 기록)가 real missing artifact(실제 누락 산출물)와 Windows long-path access failure(윈도우 긴 경로 접근 실패)를 구분하고, 다음 agent(에이전트)에 stable retry recipe(안정 재시도 절차)를 준다.
