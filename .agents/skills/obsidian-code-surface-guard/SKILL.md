---
name: obsidian-code-surface-guard
description: Prevent Project Obsidian Prime v2 code-surface drift and monolith growth. Use when adding, moving, or modifying code in foundation, pipelines, MT5 EA files, stage scripts, model builders, feature calculators, runtime helpers, or report materialization paths.
---

# Obsidian Code Surface Guard

Use this skill for code changes before choosing files or writing implementation.

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
