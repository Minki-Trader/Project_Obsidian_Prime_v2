# Project Obsidian Prime v2

## Scope

This workspace is the clean-restart FPMarkets `US100` `M5` data, feature, runtime, and stage pipeline for Project Obsidian Prime.

## Core Principles

- contract-first
- closed-bar only
- exact timestamp alignment
- contract fidelity over platform built-in convenience
- Python-led orchestration, MT5 as execution and verification engine
- one regular operating alpha line at a time
- diagnostic evidence is not the same thing as operating promotion

## Contract Hierarchy

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

Implementation notes, reviews, and selection files do not override those contracts.

## Directory Rules

- keep the root limited to `docs`, `data`, `foundation`, and `stages`
- keep source-of-truth contracts in `docs/contracts`
- keep current state in `docs/workspace`
- keep policies in `docs/policies`
- keep durable decisions in `docs/decisions` and `docs/adr`
- keep registries in `docs/registers`
- keep reusable code in `foundation`
- keep shared datasets in `data/processed`
- keep stage-local outputs under `stages/<nn_name>/`
- do not create a top-level dump folder for scratch artifacts

## Data And Time Semantics

- use `US100` `M5` as the base frame
- compute external-symbol features on each symbol's own raw `M5` series, then merge onto the `US100` frame by bar-close timestamp
- use `GOOGL.xnas` as the contract Google symbol unless explicitly changed
- treat `foundation/config/top3_monthly_weights_fpmarkets_v2.csv` as a placeholder until real monthly weights are supplied
- default shared working window: `2022-08-01` through `2026-04-13` inclusive, pending the first v2 dataset freeze
- default practical modeling start: `2022-09-01`
- no partial current-bar values are allowed in model inputs

## Runtime Fidelity Rule

- model-input feature parity is a first-class gate
- helper/runtime parity is a separate gate from model-input parity
- bundle handoff verification is a separate gate from full parity closure
- if built-in MT5 helpers disagree with the contract surface, the contract wins
- all required inputs missing means `all-or-skip`, not degrade-with-warning

## Tester Defaults

- symbol: `US100`
- timeframe: `M5`
- tester model: `Every tick based on real ticks`
- deposit: `500 USD`
- leverage: `1:100`
- signal timing: new closed `M5` bar only

## Stage Governance

- start v2 with `00_foundation_sprint` before any new alpha search
- every new stage needs a clear brief or charter before branching into runs
- diagnostic stages can close questions but cannot promote the operating line by themselves
- if execution semantics change, keep `structural_scout` and `regular_risk_execution` separate
- new telemetry cannot become a promotion gate until the incumbent/reference family is backfilled

## Document Placement

- `docs/workspace/workspace_state.yaml` is the current state source
- `stages/*/04_selected/selection_status.md` is the active stage read
- `stages/*/03_reviews/review_index.md` is the active stage reading map
- `docs/decisions/*.md` records durable operating decisions
- `docs/registers/artifact_registry.csv` records dataset, bundle, runtime, and report identity
- heavy local artifacts may stay outside Git, but their identity must stay in Git-tracked docs

## Re-entry Rule

Read in this order:

1. `AGENTS.md`
2. `docs/workspace/workspace_state.yaml`
3. `docs/context/current_working_state.md`
4. `stages/00_foundation_sprint/00_spec/stage_brief.md`
5. the three contract docs in `docs/contracts/`
6. the latest active stage `03_reviews/review_index.md`
7. the latest active stage `04_selected/selection_status.md`

## Change Discipline

- update `AGENTS.md` only when project-wide rules change
- update `docs/workspace/workspace_state.yaml` when current truth changes
- update `docs/decisions` when a durable operating decision is taken
- update registers when new durable artifact identity appears
- keep Korean `.md` and `.txt` documents in `UTF-8 with BOM` when editing them for Windows-facing workflows
