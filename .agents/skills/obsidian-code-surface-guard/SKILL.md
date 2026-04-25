---
name: obsidian-code-surface-guard
description: Prevent Project Obsidian Prime v2 code-surface drift and monolith growth. Use when adding, moving, or modifying code in foundation, pipelines, MT5 EA files, stage scripts, model builders, feature calculators, runtime helpers, or report materialization paths.
---

# Obsidian Code Surface Guard

Use this skill for code changes before choosing files or writing implementation.

## Automatic Code-Writing Gate

For every code-writing packet(code-writing packet, 코드 작성 묶음), including Python(파이썬), MQL5, tests(테스트), stage scripts(단계 스크립트), pipelines(파이프라인), model builders(모델 빌더), runtime helpers(런타임 도구), and report materializers(보고서 물질화 도구), run this guard before editing files.

Pair it with `obsidian-reference-scout(레퍼런스 탐색)` in the same precheck. The effect(effect, 효과) is that placement(배치) and external correctness(외부 정확성)을 분리해서 확인한다.

If no file is edited, mark `code_surface_guard: not_required(코드 표면 가드 불필요)` with a short reason(reason, 이유).

## Must Read

- `docs/policies/architecture_invariants.md`
- `docs/registers/architecture_debt_register.md`
- the touched module, caller, and nearest existing orchestration path

## Required Output

- `owner_module`: where reusable logic belongs
- `caller`: which pipeline, stage script, EA, or test calls it
- `input_contract`: input data shape, feature surface, or config boundary
- `output_contract`: output artifact, report, or runtime effect
- `artifact_or_report_relation`: what durable artifact or report is affected
- `monolith_risk`: whether the change concentrates too much logic in one file
- `placement_decision`: why the chosen location is correct
- `reference_scout_pairing`: whether `obsidian-reference-scout(레퍼런스 탐색)` was used, or why it was not required

## Placement Rules

- Put reusable feature/model/runtime logic under the correct `foundation` owner.
- Use `foundation/pipelines` for orchestration, not as the long-term owner of reusable feature logic.
- Use stage scripts for materialization and stage-local analysis, not reusable contracts.
- Use MT5 EA code for execution and verification, not as the only owner of feature or model semantics.
- Do not add another broad all-in-one EA or pipeline file when a smaller owner module can hold the logic.

## Stop Conditions

- The caller is unknown.
- The effect of the code on artifacts, reports, or runtime behavior is unknown.
- The change deepens registered architecture debt without an explicit task packet or decision memo.
