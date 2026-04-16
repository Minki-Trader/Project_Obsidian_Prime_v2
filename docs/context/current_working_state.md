# Current Working State

- updated_on: `2026-04-16`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `00_foundation_sprint`
- active_branch: `main`

## Read This First

1. `AGENTS.md`
2. `docs/workspace/workspace_state.yaml`
3. `stages/00_foundation_sprint/00_spec/stage_brief.md`
4. `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
5. `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
6. `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
7. `stages/00_foundation_sprint/03_reviews/review_index.md`
8. `stages/00_foundation_sprint/04_selected/selection_status.md`

## Current Read

- this workspace is a clean restart, not a continuation of the old stage tree
- no v2 alpha incumbent has been promoted yet
- the v2 priority is foundation quality, not new alpha search
- the old project remains the evidence source for legacy lessons, but not the automatic source of current v2 truth

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. keep state and durable decisions in Git-tracked docs from day one
2. define the first v2 dataset freeze and registry identities
3. define the first v2 parity harness plan before any new alpha work
4. keep the Stage 00 deliverables small, explicit, and re-entry friendly

## Do Not Do First

- do not open a fresh alpha stage before Stage 00 foundation gates close
- do not treat bundle handoff verification as full parity closure
- do not treat platform built-ins as contract-equivalent just because they are convenient
- do not let durable conclusions live only in branch notes or scratch files
