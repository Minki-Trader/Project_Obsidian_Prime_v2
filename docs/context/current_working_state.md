# Current Working State

- updated_on: `2026-04-18`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `01_dataset_contract_freeze`
- active_branch: `main`

## Read This First

1. `README.md`
2. `AGENTS.md`
3. `docs/workspace/workspace_state.yaml`
4. `stages/00_foundation_sprint/04_selected/selection_status.md`
5. `docs/decisions/2026-04-18_stage00_close_and_stage01_open.md`
6. `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
7. `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
8. `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
9. `docs/contracts/dataset_freeze_and_row_state_contract_fpmarkets_v2.md`
10. `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
11. `stages/01_dataset_contract_freeze/00_spec/stage_brief.md`
12. `stages/01_dataset_contract_freeze/01_inputs/input_refs.md`
13. `stages/01_dataset_contract_freeze/03_reviews/review_index.md`
14. `stages/01_dataset_contract_freeze/04_selected/selection_status.md`

## Current Read

- this workspace is a concept-preserving reboot, not a legacy continuation
- no v2 alpha incumbent has been promoted yet, by policy rather than by delay
- current v2 truth begins only after the first dataset freeze, the first parity harness, and the first artifact identity closure exist
- until those closures exist, the workspace stays in foundation mode
- `00_foundation_sprint` is now closed as planning scaffold complete, and `01_dataset_contract_freeze` is the active foundation stage
- legacy winners remain archive notes and design evidence only; they do not define current v2 truth
- the shared root skeleton now treats `docs/`, `data/`, and `foundation/` as the reusable base while `stages/` stays stage-local
- the supporting freeze/parity templates and artifact registry schema are now aligned to the Stage 00 supplemental contracts so the first reusable evidence pack can be written without ad hoc fields
- the first planning freeze card now exists for `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`, and its contract-order feature fingerprint is now fixed
- the first planning gold fixture inventory and first planning runtime parity report now exist, but those remain Stage 03 and 04 follow-up inputs rather than Stage 00 blockers

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. replace the planning-freeze placeholders with the first materialized row summary, source identities, and output hashes
2. update the Stage 01 dataset freeze evidence and artifact registry rows so the first reusable dataset-contract pack is durable
3. keep exact fixture timestamps and snapshot refs queued for `03_runtime_parity_closure`
4. keep `04_artifact_identity_closure` explicit and machine-readable across dataset, fixture, snapshot, and parity artifacts
5. keep `05_exploration_kernel_freeze` closed before opening new range stages

## Foundation Closure Path

1. `00_foundation_sprint`
2. `01_dataset_contract_freeze`
3. `02_feature_dataset_closure`
4. `03_runtime_parity_closure`
5. `04_artifact_identity_closure`
6. `05_exploration_kernel_freeze`

## Do Not Do First

- do not open a fresh alpha stage before Stage 01 to 05 foundation gates close
- do not treat legacy winners or legacy operating defaults as the starting line for v2
- do not treat Stage 00 closure as proof of materialized dataset closure or runtime parity closure
- do not treat bundle handoff verification as full parity closure
- do not treat platform built-ins as contract-equivalent just because they are convenient
- do not let durable conclusions live only in branch notes or scratch files
