# Current Working State

- updated_on: `2026-04-18`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `03_runtime_parity_closure`
- active_branch: `main`

## Read This First

- bootstrap entrypoint: `AGENTS.md`
- canonical re-entry order and truth precedence: `docs/policies/reentry_order.md`
- latest durable decisions to expect during that pass:
  - `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
  - `docs/decisions/2026-04-18_stage02_close_and_stage03_open.md`

## Current Read

- this workspace is a concept-preserving reboot, not a legacy continuation
- no v2 alpha incumbent has been promoted yet, by policy rather than by delay
- current v2 foundation truth already exists and is anchored in `workspace_state.yaml`, the active stage `selection_status.md`, and durable decision memos
- current v2 operating truth begins only after the first evaluated runtime-parity closure and the first artifact-identity closure exist; the first dataset-contract closure and the first deterministic feature-dataset closure now exist but do not by themselves promote an operating line
- until those closures exist, the workspace stays in foundation mode
- `00_foundation_sprint` is closed as planning scaffold complete, `01_dataset_contract_freeze` is closed as the first materialized dataset-contract evidence pack, `02_feature_dataset_closure` is closed after a deterministic rerun match, and `03_runtime_parity_closure` is now the active foundation stage
- legacy winners remain archive notes and design evidence only; they do not define current v2 foundation truth or current v2 operating truth
- the shared root skeleton now treats `docs/`, `data/`, and `foundation/` as the reusable base while `stages/` stays stage-local
- repo-scoped skills now exist under `.agents/skills/` to reinforce re-entry reads, claim discipline, and stage-transition sync
- the supporting freeze/parity templates and artifact registry schema are now aligned to the Stage 00 supplemental contracts so the first reusable evidence pack can be written without ad hoc fields
- the first planning freeze card now exists for `dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01`, and its contract-order feature fingerprint is now fixed
- the first raw `M5` source exports and manifests for all `12` required symbols now exist under `data/raw/mt5_bars/m5/`, and their tracked identity note now lives in `stages/01_dataset_contract_freeze/01_inputs/first_raw_source_inventory.md`
- the first materialized processed dataset outputs now exist under `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01/`, with `raw_rows=261344`, `valid_rows=24280`, `invalid_rows=237064`, and tracked hashes for the first reusable freeze
- a second rerun of the first materialized freeze reproduced the same row summary, invalid-reason breakdown, and tracked output hashes, so deterministic feature-dataset closure now exists
- the first planning gold fixture inventory and first planning runtime parity report now exist, but those remain Stage 03 and 04 follow-up inputs rather than Stage 00 blockers
- `Tier A / Tier B / Tier C readiness` is now accepted as a downstream exploration vocabulary for a future separate reduced-risk line, but the current runtime rule remains the strict Tier A contract line
- the detailed downstream matrix for that idea now lives in `docs/policies/tiered_readiness_exploration.md`

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. bind the first fixture timestamps and snapshot refs for the minimum runtime parity pack
2. evaluate the first Python to MT5 parity report on the frozen `58`-feature contract surface
3. keep `04_artifact_identity_closure` explicit and machine-readable across dataset, fixture, snapshot, and parity artifacts
4. keep `05_exploration_kernel_freeze` closed before opening new range stages
5. keep placeholder weights caveat explicit until a real monthly-weight source replaces the equal-weight table
6. keep tiered-readiness exploration explicitly downstream of Stages `03` to `05` so it does not get mistaken for a current Stage 03 runtime rule

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
