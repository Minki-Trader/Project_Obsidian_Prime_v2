# Current Working State

- updated_on: `2026-04-18`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `00_foundation_sprint`
- active_branch: `main`

## Read This First

1. `README.md`
2. `AGENTS.md`
3. `docs/workspace/workspace_state.yaml`
4. `stages/00_foundation_sprint/00_spec/stage_brief.md`
5. `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
6. `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
7. `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
8. `docs/contracts/dataset_freeze_and_row_state_contract_fpmarkets_v2.md`
9. `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
10. `stages/00_foundation_sprint/03_reviews/review_index.md`
11. `stages/00_foundation_sprint/04_selected/selection_status.md`

## Current Read

- this workspace is a concept-preserving reboot, not a legacy continuation
- no v2 alpha incumbent has been promoted yet, by policy rather than by delay
- current v2 truth begins only after the first dataset freeze, the first parity harness, and the first artifact identity closure exist
- until those closures exist, the workspace stays in foundation mode
- legacy winners remain archive notes and design evidence only; they do not define current v2 truth
- the shared root skeleton now treats `docs/`, `data/`, and `foundation/` as the reusable base while `stages/` stays stage-local
- the supporting freeze/parity templates and artifact registry schema are now aligned to the Stage 00 supplemental contracts so the first reusable evidence pack can be written without ad hoc fields

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. use the aligned dataset freeze card, runtime parity report, gold fixture inventory template, and artifact registry schema to write the first reusable Stage 00 evidence pack
2. write the first `01_dataset_contract_freeze` evidence pack and its row-state closure before opening alpha work
3. define `02_feature_dataset_closure` and the first dataset freeze identity
4. write the first gold fixture inventory and then close `03_runtime_parity_closure` and `04_artifact_identity_closure`
5. keep `05_exploration_kernel_freeze` closed before opening new range stages

## Foundation Closure Path

1. `00_foundation_sprint`
2. `01_dataset_contract_freeze`
3. `02_feature_dataset_closure`
4. `03_runtime_parity_closure`
5. `04_artifact_identity_closure`
6. `05_exploration_kernel_freeze`

## Do Not Do First

- do not open a fresh alpha stage before Stage 00 foundation gates close
- do not treat legacy winners or legacy operating defaults as the starting line for v2
- do not treat bundle handoff verification as full parity closure
- do not treat platform built-ins as contract-equivalent just because they are convenient
- do not let durable conclusions live only in branch notes or scratch files
