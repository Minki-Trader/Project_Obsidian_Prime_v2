# Current Working State

- updated_on: `2026-04-20`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `05_exploration_kernel_freeze`
- active_branch: `codex/stage05-broader-rebind`

## Read This First

- bootstrap entrypoint: `AGENTS.md`
- canonical re-entry order and truth precedence: `docs/policies/reentry_order.md`
- latest durable decisions to expect during that pass:
  - `docs/decisions/2026-04-19_stage05_broader_0002_contract_aligned_rebind.md`
  - `docs/decisions/2026-04-19_stage05_broader_sample_first_lane.md`
  - `docs/decisions/2026-04-19_stage04_close_and_stage05_open.md`
  - `docs/decisions/2026-04-19_stage03_close_and_stage04_open.md`
  - `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
  - `docs/decisions/2026-04-18_stage03_bound_minimum_fixture_pack.md`

## Current Read

- this workspace is a concept-preserving reboot, not a legacy continuation
- no v2 alpha incumbent has been promoted yet, by policy rather than by delay
- current v2 foundation truth already exists and is anchored in `workspace_state.yaml`, the active stage `selection_status.md`, and durable decision memos
- current v2 operating truth still begins only after the later exploration-kernel freeze exists; the dataset-contract closure, deterministic feature-dataset closure, first model-input parity closure, and first artifact-identity closure now exist, but they still do not by themselves promote an operating line
- `00_foundation_sprint` is closed as planning scaffold complete, `01_dataset_contract_freeze` is closed as the first materialized dataset-contract evidence pack, `02_feature_dataset_closure` is closed after a deterministic rerun match, and `03_runtime_parity_closure` is now closed after the first v2-native five-window pack matched within the agreed tolerance
- the first Stage 03 evaluated pack now closes model-input parity on the contract surface with `tolerance_parity=true`, `max_abs_diff=1.6846210968424202e-06`, `4 ready rows + 1 negative non-ready row`, and zero features over the agreed tolerance
- the remaining `exact_parity=false` note is bounded to floating-point serialization drift and is not treated as a contract-surface blocker for Stage 03
- the first v2-native MT5 snapshot rows now carry explicit machine-readable identity fields including `dataset_id`, `fixture_set_id`, `bundle_id`, `report_id`, `runtime_id`, `parser_version`, `feature_contract_version`, `runtime_contract_version`, and `feature_order_hash`
- the first parity comparison summary now proves that the request and MT5 snapshot agree on those identity values and on the tracked comparison-side artifact hashes for the first pack; the rendered report and artifact registry still carry linked evidence for the same pack through `required_artifact_hashes_checked` and registry rows rather than through direct comparison-summary proof
- `04_artifact_identity_closure` is now closed because the explicit Stage 04 read names one aligned machine-readable identity chain across the request pack, MT5 snapshot rows, comparison summary, rendered report, and registry rows, and the recorded hashes remain internally consistent on the materialized first pack
- the Stage 04 runtime self-check meaning is satisfied on the first pack because the MT5 audit path loaded the declared identity inputs, echoed them into every snapshot row, and the comparison summary verified those exported values and derived feature-order hashes against the declared request pack
- `05_exploration_kernel_freeze` remains the active stage, and the first downstream lane is now frozen to `broader-sample parity` rather than `runtime-helper parity` or a separate exploration charter
- the new broader-sample charter treats that lane as a `pre-exploration validation lane` only; it extends the existing minimum-pack artifact family into a fixed `24-window` stratified audit pack and does not change the current strict Tier A runtime rule
- the first broader evaluated pack `broader_0001` is retained as pre-alignment mismatch-open evidence rather than active Stage 05 truth; it remains useful diagnostic evidence, but it no longer carries the active broader request-pack identity after the localized contract-alignment fixes landed
- those localized fixes are now materialized in the active code path: Python external proxy features are computed `raw-series-first`, the MT5 broader audit loader uses the full declared contract window through each audited close instead of the earlier short trailing slice, and the MT5 `supertrend_10_3` seed rule now follows the current Python contract surface
- the active charter-aligned broader-sample inventory, machine-readable selection manifest, Python snapshot, MT5 request, MT5 input `.set`, tester `.ini`, imported MT5 snapshot, broader comparison summary, and rendered broader parity report now exist under the `broader_0002` identity family in `stages/05_exploration_kernel_freeze/`
- the active broader evaluated pack `broader_0002` now reaches the first broader tolerance-closed read rather than mismatch-open evidence: all `24` frozen fixtures matched by id and timestamp with zero unexpected MT5 rows, all `16` ready rows match within tolerance, all `8` negative rows match on the strict non-ready comparison rule, `exact_parity=false`, `tolerance_parity=true`, `max_abs_diff=3.9019953135266405e-06`, and zero features remain over the agreed tolerance
- the localized Stage 05 blocker on the active pack is now resolved on materialized evidence: the MT5 audit path skips a tester-synthesized single-bar decimal-scale artifact in early-history `NVDA` history, and the pre-open negative rows now resolve to the same external-alignment-missing skip-reason family that the Python side expects
- that first broader tolerance-closed read does not by itself close runtime-helper parity, does not by itself close broader-sample parity as a separate stage read, and does not promote any operating line; the remaining `exact_parity=false` note stays bounded to floating-point serialization drift
- legacy winners remain archive notes and design evidence only; they do not define current v2 foundation truth or current v2 operating truth
- `Tier A / Tier B / Tier C readiness` remains a downstream exploration vocabulary only; it does not relax the current strict-line foundation read

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. carry the first broader tolerance-closed pack forward without conflating it with runtime-helper parity closure, broader-sample parity closure, or operating promotion
2. decide whether the next Stage 05 evidence is additional broader-sample coverage or a separate runtime-helper parity lane
3. keep the active broader `exact_parity=false` note bounded to floating-point serialization drift rather than a contract blocker
4. keep the Stage 04 closure bounded to artifact identity rather than runtime-helper parity or operating promotion
5. keep placeholder weights caveat explicit until a real monthly-weight source replaces the equal-weight table
6. keep branch truth aligned to `codex/stage05-broader-rebind` until the handoff is merged

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
- do not open a fresh alpha or range stage before Stage `05` closes
- do not let durable conclusions live only in branch notes or scratch files
