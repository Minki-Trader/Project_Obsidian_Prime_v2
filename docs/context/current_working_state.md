# Current Working State

- updated_on: `2026-04-23`
- workspace: `Project_Obsidian_Prime_v2`
- project_mode: `foundation_restart`
- active_stage: `07_alpha_search`
- active_branch: `main`

## Read This First

- bootstrap entrypoint: `AGENTS.md`
- canonical re-entry order and truth precedence: `docs/policies/reentry_order.md`
- latest durable decisions to expect during that pass:
  - `docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
  - `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
  - `docs/decisions/2026-04-21_stage06_first_tier_b_charter_adopted.md`
  - `docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
  - `docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
  - `docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
  - `docs/decisions/2026-04-20_stage05_broader_0003_reinforcement_pack_materialized.md`
  - `docs/decisions/2026-04-20_stage05_helper_0001_first_focused_pack.md`
  - `docs/decisions/2026-04-20_stage05_dual_followup_order.md`
  - `docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`

## Current Read

- this workspace is a concept-preserving reboot, not a legacy continuation
- no v2 alpha incumbent has been promoted yet, by policy rather than by delay
- the foundation closure path is now explicit through `05_exploration_kernel_freeze`; `00_foundation_sprint`, `01_dataset_contract_freeze`, `02_feature_dataset_closure`, `03_runtime_parity_closure`, `04_artifact_identity_closure`, and `05_exploration_kernel_freeze` are all now closed on materialized v2 evidence
- current v2 operating truth still has no promoted operating line; the only current runtime rule remains the strict `Tier A` contract-aligned line, and Stage `07` does not change that by itself
- the first Stage 03 evaluated pack still closes model-input parity on the contract surface with `tolerance_parity=true`, `max_abs_diff=1.6846210968424202e-06`, `4 ready rows + 1 negative non-ready row`, and zero features over the agreed tolerance
- the remaining `exact_parity=false` note on Stage 03 remains bounded to floating-point serialization drift and is not treated as a contract-surface blocker
- Stage 04 remains closed because the first v2-native machine-readable identity chain stayed aligned across the request pack, MT5 snapshot rows, comparison summary, rendered report, and registry rows
- Stage 05 is now also closed, but only on its own boundary: the active `broader_0002` twenty-four-window pack reached the first broader tolerance-closed exact-open read, `helper_0001` reached the first separate helper-focused tolerance-closed exact-open read on a frozen eight-window subset, and the non-overlapping additive `broader_0003` reinforcement pack now also reproduced a native MT5 tolerance-closed exact-open read with `matched_fixtures=24`, `unexpected_record_count=0`, `tolerance_parity=true`, `exact_parity=false`, and `max_abs_diff=7.160007811535252e-06`
- that Stage 05 closure does not claim separate runtime-helper parity closure, does not claim separate broader-sample parity closure, and does not promote any operating line; it closes only the exploration-kernel freeze boundary by making the first downstream exploration family explicit enough that later work cannot drift open by implication
- `06_tiered_readiness_exploration` is now closed because the deterministic readiness boundary, reporting interface, scorecard family, first v2-native baseline seed, additive follow-up pack, and first shared keep42 reduced-context model are all materialized enough that the readiness-family question no longer needs the active-stage slot
- `07_alpha_search` is now the active stage because the next bounded question is no longer whether the separate readiness family exists, but whether the first `Tier B dual verdict packet (Tier B 이중 판정 팩)` on a validated user-weight rerun keeps the separate `Tier B` lane alive and hands it forward as an `MT5 feasibility candidate (MT5 가능성 후보)` without crossing into an opened `MT5 path (MT5 경로)` or a promoted operating-line claim (승격 운영선 주장)
- the first Stage 06 governance lock still fixes the deterministic boundary as: if `Group 1` or `Group 2` fails -> `tier_c`; else if `Group 3`, `Group 4`, and `Group 5` are all complete -> `tier_a`; else if exactly `1` or `2` of `Group 3` to `Group 5` are complete -> `tier_b`; else -> `tier_c`
- `group complete` remains fixed to exact-timestamp required-symbol and required-field presence with no forward-fill, no fabricate path, and computable required semantics
- all future Tier B work must stay separate from the current strict Tier A runtime rule and must carry the fixed `readiness_tier`, `missing_groups`, `missing_symbols`, and `reporting_lane` interface
- `B-mixed-partial` remains a vocabulary-only candidate term and is not an eligible materialized readiness rule in the first Stage 06 boundary
- the first Stage 06 scorecard family remains materialized as row-level labels under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`, a machine-readable summary under `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_scorecard_fpmarkets_v2_tiered_readiness_0001.json`, and a review report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
- that first scorecard keeps the current strict Tier A runtime rule unchanged and reads the shared window as `tier_a=56988`, `tier_b=88303`, `tier_c=116053` plus the practical window as `tier_a=55457`, `tier_b=86192`, `tier_c=113352`
- the first Stage 06 offline-only Tier B experiment charter remains accepted under `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`, but its original baseline-family reuse hypothesis is now superseded by `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
- the first Stage 06 `v2-native baseline seed (v2 고유 기준선 시드)` is now materialized under `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/`; it fits a first `3-class Gaussian Naive Bayes (3분류 가우시안 나이브 베이즈)` model on `34695` `Tier A` train rows only with `q33=-0.00035087247936272335` and `q67=0.0004049556640609367`
- the paired report under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md` separates `validation (검증)` and `holdout (보류 평가)` KPI reads for `strict_tier_a` and `tier_b_exploration` while keeping mixed aggregates `info-only (정보용)` and leaving runtime or promotion meaning closed
- the first shared `Tier B reduced-context model (Tier B 축약 문맥 모델)` is now also materialized under `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/`; it keeps the first active surface to the shared `keep=42` features, leaves subtype tags `info-only (정보용)`, and improves the current `Tier B holdout (Tier B 보류 평가)` probabilistic read to `log_loss=1.503578`
- the first Stage 07 packet is now fixed by decision as `docs/decisions/2026-04-23_stage07_tier_b_dual_verdict_packet_adopted.md`; it requires one validated user-provided `monthly-frozen weights CSV (월별 동결 가중치 CSV)` and reuses the current keep42 surface rather than opening a new model family
- that keep42 surface remains weight-neutral on direct inputs because `top3_weighted_return_1` and `us100_minus_top3_weighted_return_1` stay outside the active feature set, so the rerun primarily closes the source-boundary question for the dual verdict packet
- the placeholder weights table remains allowed only for that offline-only charter and does not justify simulated execution, MT5-path expansion, or operating promotion
- no reduced-risk runtime family is materialized yet and no operating promotion is claimed from the scorecard, baseline seed, follow-up pack, reduced-context read, or charter alone
- legacy winners remain archive notes and design evidence only; they do not define current v2 foundation truth or current v2 operating truth

## Legacy Lessons Carried Forward

- Stage 40 proved that the old runtime mismatch was real and not a simple one-bar offset
- Stage 41 localized the dominant drift to the MT5 ATR and Stochastic feature path, then closed the audited windows to float-noise parity after replacing the built-in path with contract-matching logic
- Stage 41 also showed that the remaining latest-window weakness on the contract-aligned lane was mostly a fixed `min_margin` tax rather than a fresh contextual-rule mystery
- Stage 42 removed the remaining MT5 built-in ATR and Stochastic helper usage from the runtime helper path and rechecked that the best tested legacy contract-aligned gate still centered on `min_margin=0.06000`

Use those findings as prior evidence and design guidance. Do not treat them as a substitute for v2 dataset identity, v2 parity fixtures, or v2 operating promotion.

## Immediate Priorities

1. materialize the first `Stage 07 Tier B dual verdict packet (Stage 07 Tier B 이중 판정 팩)` on a validated user-provided `monthly-frozen weights CSV (월별 동결 가중치 CSV)`
2. decide from that packet whether the separate `Tier B` lane survives as `keep` or closes as `prune`
3. decide from that packet whether the rerun is strong enough for `MT5 feasibility candidate (MT5 가능성 후보)` handoff only
4. keep the current strict Tier A runtime rule unchanged until a later explicit exploration read says otherwise

## Foundation Closure Path

1. `00_foundation_sprint`
2. `01_dataset_contract_freeze`
3. `02_feature_dataset_closure`
4. `03_runtime_parity_closure`
5. `04_artifact_identity_closure`
6. `05_exploration_kernel_freeze`

All six foundation stages are now explicitly closed.

## Active Exploration Stage

1. `07_alpha_search`

## Do Not Do First

- do not reopen `05_exploration_kernel_freeze` unless a new contradiction breaks the frozen `broader_0002 + helper_0001 + broader_0003` read
- do not treat Stage 06 closure or the Stage 07 dual-verdict packet as runtime-helper parity closure, broader-sample parity closure, an opened `MT5 path (MT5 경로)`, or a promoted operating-line claim (승격 운영선 주장)
- do not let any Stage 07 artifact imply that Tier B is contract-equivalent to the current strict Tier A line
- do not treat the shared keep42 reduced-context read as a materialized runtime family or as permission to open simulated execution or MT5-path work
- do not treat `B-mixed-partial` or any other non-binding vocabulary as an eligible first-boundary rule
- do not compare future Tier B outputs head-to-head with Tier A without separate reporting lanes
- do not let durable conclusions live only in branch notes or scratch files
