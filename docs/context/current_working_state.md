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
  - `docs/decisions/2026-04-18_stage03_bound_minimum_fixture_pack.md`
  - `docs/decisions/2026-04-18_stage03_first_v2_native_evaluated_pack_mismatch_open.md`

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
- the first bound Stage 03 minimum fixture inventory now exists under `stages/03_runtime_parity_closure/01_inputs/first_bound_runtime_minimum_fixture_inventory.md`
- the first Stage 03 Python-side snapshot artifact, matching MT5 request window spec, and v2-native MT5 audit path now exist under `stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/` and `foundation/mt5/`
- the first v2-native MT5 snapshot artifact and the first evaluated Python to MT5 parity report now exist, but the honest verdict is still `first_evaluated_pack_mismatch_open`, so Stage 03 remains active and no v2 parity closure claim is safe yet
- the first v2-native evaluated pack already reproduces the expected `4 ready rows + 1 negative non-ready row`, including the negative fixture `skip_reason=EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas`, but exact and tolerance parity both remain open because the dominant drift still concentrates in `ema50_ema200_diff` with smaller `rsi_50`, `atr_50`, `atr_14_over_atr_50`, and `ema20_ema50_diff` mismatches
- the current MT5 JSONL snapshot artifact is reusable Stage 03 evidence, but it still lacks explicit embedded identity fields such as `dataset_id`, `bundle_id`, and `runtime_id`, so this does not close Stage 04 artifact identity yet
- `Tier A / Tier B / Tier C readiness` is now accepted as a downstream exploration vocabulary for a future separate reduced-risk line, but the current runtime rule remains the strict Tier A contract line
- the detailed downstream matrix for that idea now lives in `docs/policies/tiered_readiness_exploration.md`

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. inspect and repair the localized drift on the first v2-native evaluated five-window pack, starting with `ema50_ema200_diff`
2. keep the evaluated mismatch-open read synchronized across `workspace_state.yaml`, Stage 03 selection docs, and `artifact_registry.csv`
3. keep `04_artifact_identity_closure` explicit and machine-readable across dataset, fixture, snapshot, request, comparison, and parity artifacts
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
