# Project Obsidian Prime v2

This workspace is a clean restart for the FPMarkets `US100` `M5` pipeline.

The old project remains preserved next to this folder. This workspace starts from the same contract philosophy, but resets the operating surface so a new thread can re-enter quickly without inheriting stage clutter, stale runtime assumptions, or undocumented artifact identity.

## Read First

1. `AGENTS.md`
2. `docs/workspace/workspace_state.yaml`
3. `docs/context/current_working_state.md`
4. `stages/00_foundation_sprint/00_spec/stage_brief.md`
5. `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
6. `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
7. `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

## Current Mode

- `project_mode`: `foundation_restart`
- `active_stage`: `00_foundation_sprint`
- `active_branch`: `main`
- `v2_alpha_status`: `no_promoted_v2_incumbent_yet`

## Root Map

- `docs/`: contracts, policies, workspace state, decisions, registers, templates
- `data/`: raw and processed artifacts only
- `foundation/`: reusable shared code and configuration
- `stages/`: stage-specific work history and selected reads

## Intent

- keep the strategy concept
- keep the contract-first runtime philosophy
- rebuild state, artifact identity, and parity discipline before new alpha search
- make new-thread re-entry fast and low-risk
