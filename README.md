# Project Obsidian Prime v2

This workspace is a concept-preserving reboot for the FPMarkets `US100` `M5` pipeline.

The old project remains preserved next to this folder. This workspace inherits the concept contract of Obsidian Prime, but deliberately resets alpha lineage, operating defaults, and stage-to-stage inheritance so a new thread can re-enter quickly without carrying forward stale promotion logic, undocumented artifact identity, or partial parity assumptions.

## Read First

- bootstrap entrypoint: `AGENTS.md`
- canonical re-entry order and truth precedence: `docs/policies/reentry_order.md`
- current trigger routing for repo-scoped skills: `docs/policies/agent_trigger_policy.md`

## Current Truth

`README.md` is an orientation entrypoint, not the live state source.

- authoritative current state: `docs/workspace/workspace_state.yaml`
- narrative current status: `docs/context/current_working_state.md`
- active stage read: the active stage `stages/*/04_selected/selection_status.md`
- durable handoffs and state transitions: `docs/decisions/*.md`

If these documents disagree, use the precedence defined in `docs/policies/reentry_order.md`.

## Root Map

- `docs/`: contracts, policies, workspace state, decisions, registers, templates, archive notes
- `data/`: shared raw, processed, and snapshot roots; heavy contents stay local and only the skeleton is tracked
- `foundation/`: reusable shared code, MT5/runtime parity helpers, reports, and configuration
- `stages/`: stage-specific work history and selected reads
- `.agents/skills/`: repo-scoped Codex skills for strong re-entry, claim-discipline, and stage-transition triggers

## Shared Skeleton

- `docs/archive/`: sealed legacy lessons and carry-forward notes
- `data/raw/mt5_bars/m5/`: broker-native `M5` source bars by symbol
- `data/raw/real_ticks/us100/`: optional `US100` real-tick source exports for tester/runtime checks
- `data/processed/datasets/`: reusable dataset outputs
- `data/processed/coverage_audits/`: shared row/alignment audit artifacts
- `data/processed/runtime_snapshots/`: shared runtime parity snapshots
- `data/snapshots/`: frozen identity snapshots that are reusable across stages
- `foundation/collectors/`: source loaders and export collectors
- `foundation/features/`: contract-aligned feature helpers
- `foundation/pipelines/`: shared dataset and bundle pipelines
- `foundation/mt5/`: MT5-facing runtime helpers, templates, or wrappers
- `foundation/parity/`: Python to MT5 comparison helpers and fixtures
- `foundation/reports/`: reusable shared notes and audit writeups

## Foundation Roadmap

- `00_foundation_sprint`: align the reboot charter, read path, and durable state
- `01_dataset_contract_freeze`: materialize dataset meaning, row states, and shared input semantics on the first reusable freeze
- `02_feature_dataset_closure`: close deterministic parser output on the frozen `58`-feature contract surface
- `03_runtime_parity_closure`: close Python to MT5 parity on the contract surface
- `04_artifact_identity_closure`: close machine-readable dataset, bundle, runtime, and report identity
- `05_exploration_kernel_freeze`: freeze the exploration kernel so later stages only change search variables

## Intent

- keep the strategy concept and its contract surface
- keep the contract-first runtime philosophy while cutting legacy winner lineage and operating defaults
- close dataset, parity, and artifact identity foundations before any new alpha search
- enter exploration-only mode only after the foundation closure path is explicit and closed
- make new-thread re-entry fast, low-risk, and unambiguous
