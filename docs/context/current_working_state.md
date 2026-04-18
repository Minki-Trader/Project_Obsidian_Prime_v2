# Current Working State

- updated_on: `2026-04-19`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `04_artifact_identity_closure`
- active_branch: `codex/stage03-v2-native-parity-sync`

## Read This First

- bootstrap entrypoint: `AGENTS.md`
- canonical re-entry order and truth precedence: `docs/policies/reentry_order.md`
- latest durable decisions to expect during that pass:
  - `docs/decisions/2026-04-19_stage03_close_and_stage04_open.md`
  - `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
  - `docs/decisions/2026-04-18_stage03_bound_minimum_fixture_pack.md`

## Current Read

- this workspace is a concept-preserving reboot, not a legacy continuation
- no v2 alpha incumbent has been promoted yet, by policy rather than by delay
- current v2 foundation truth already exists and is anchored in `workspace_state.yaml`, the active stage `selection_status.md`, and durable decision memos
- current v2 operating truth still begins only after the first artifact-identity closure and the later exploration-kernel freeze exist; the dataset-contract closure, deterministic feature-dataset closure, and first model-input parity closure now exist, but they still do not by themselves promote an operating line
- `00_foundation_sprint` is closed as planning scaffold complete, `01_dataset_contract_freeze` is closed as the first materialized dataset-contract evidence pack, `02_feature_dataset_closure` is closed after a deterministic rerun match, and `03_runtime_parity_closure` is now closed after the first v2-native five-window pack matched within the agreed tolerance
- the first Stage 03 evaluated pack now closes model-input parity on the contract surface with `tolerance_parity=true`, `max_abs_diff=1.6846210968424202e-06`, `4 ready rows + 1 negative non-ready row`, and zero features over the agreed tolerance
- the remaining `exact_parity=false` note is bounded to floating-point serialization drift and is not treated as a contract-surface blocker for Stage 03
- the first v2-native MT5 snapshot rows now carry explicit machine-readable identity fields including `dataset_id`, `fixture_set_id`, `bundle_id`, `report_id`, `runtime_id`, `parser_version`, `feature_contract_version`, `runtime_contract_version`, and `feature_order_hash`
- the first parity comparison summary now proves that the request and MT5 snapshot agree on those identity values and on the tracked comparison-side artifact hashes for the first pack; the rendered report and artifact registry still carry linked evidence for the same pack through `required_artifact_hashes_checked` and registry rows rather than through direct comparison-summary proof
- `04_artifact_identity_closure` is now the active stage because the first identity chain is materialized, but the explicit Stage 04 closure read and any remaining runtime self-check proof still need to be written without conflating that work with runtime-helper parity
- legacy winners remain archive notes and design evidence only; they do not define current v2 foundation truth or current v2 operating truth
- `Tier A / Tier B / Tier C readiness` remains a downstream exploration vocabulary only; it does not relax the current strict-line foundation read

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. keep the Stage 03 closure read synchronized across `workspace_state.yaml`, the closing Stage 03 docs, and the artifact registry
2. write the explicit Stage 04 artifact-identity closure read from the now machine-readable first-pack identity chain
3. verify that the recorded request, snapshot, comparison, report, and registry hashes stay internally consistent through the Stage 04 pass
4. keep runtime-helper parity and broader-sample parity explicit as separate downstream questions
5. keep placeholder weights caveat explicit until a real monthly-weight source replaces the equal-weight table
6. keep branch truth aligned to `codex/stage03-v2-native-parity-sync` until the handoff is merged

## Foundation Closure Path

1. `00_foundation_sprint`
2. `01_dataset_contract_freeze`
3. `02_feature_dataset_closure`
4. `03_runtime_parity_closure`
5. `04_artifact_identity_closure`
6. `05_exploration_kernel_freeze`

## Do Not Do First

- do not reopen `03_runtime_parity_closure` unless a new hypothesis breaks the first tolerance-closed pack or the agreed tolerance itself changes
- do not treat Stage 03 closure as runtime-helper parity closure
- do not treat the first machine-readable identity chain as automatic operating promotion
- do not open a fresh alpha or range stage before Stages `04` to `05` close
- do not let durable conclusions live only in branch notes or scratch files
