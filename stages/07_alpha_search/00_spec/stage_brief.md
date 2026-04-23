# Stage 07 Alpha Search

- stage: `07_alpha_search`
- stage_type: `alpha_search_stage`
- updated_on: `2026-04-23`
- owner_path: `stages/07_alpha_search/`

## Purpose

- open the first alpha-search stage after Stage 06 made the readiness family explicit enough to hand downstream work a durable boundary
- keep the current strict `Tier A` runtime rule unchanged while giving bounded alpha-search questions a separate home
- start Stage 07 with the first `Tier B dual verdict packet (Tier B 이중 판정 팩)` so the repo can decide whether the separate `Tier B` lane survives and whether it may move forward as an `MT5 feasibility candidate (MT5 가능성 후보)` without implying runtime safety or promoted operating-line meaning

## Inherited Context

- `00_foundation_sprint` through `05_exploration_kernel_freeze` are closed
- `06_tiered_readiness_exploration` is now closed after materializing:
  - the first deterministic readiness boundary
  - the first row-label scorecard family
  - the first v2-native baseline seed and offline evaluation read
  - the additive calibration, control, robustness, and weight-verdict follow-up pack
  - the first shared keep42 `Tier B reduced-context model (Tier B 축약 문맥 모델)`
- current operating truth still has no promoted v2 operating line

## Scope

- in scope:
  - the first `Tier B dual verdict packet (Tier B 이중 판정 팩)` on a validated user-provided `monthly-frozen weights CSV (월별 동결 가중치 CSV)`
  - bounded rerun work on the separate keep42 `Tier B` reduced-context lane with the current strict `Tier A` lane still reported separately
  - coarse control exploration with separate reporting so the packet can test the Stage 07 keep-or-prune boundary honestly
  - deciding whether the separate `Tier B` lane deserves continued bounded search after the dual-verdict packet
  - deciding whether the dual-verdict packet may move forward as an `MT5 feasibility candidate (MT5 가능성 후보)` only
- not in scope:
  - changing the current strict `Tier A` runtime rule
  - claiming `Tier B` is contract-equivalent to `Tier A`
  - an opened `MT5 path (MT5 경로)`
  - any promoted operating-line claim (승격 운영선 주장)
  - contract or public runtime-input changes under `docs/contracts/**`
  - any optional `macro-aware (매크로 인지)` Tier B variant before the dual-verdict packet exists

## Success Criteria

- the first Stage 07 packet uses a validated user-provided `monthly-frozen weights CSV (월별 동결 가중치 CSV)`
- the first Stage 07 packet keeps `Tier A` and `Tier B` on separate reporting lanes
- the first Stage 07 packet records both `separate_lane_verdict (별도 레인 판정)` and `mt5_candidate_verdict (MT5 후보 판정)`
- no Stage 07 artifact blurs the packet into an opened `MT5 path (MT5 경로)` or a promoted operating-line claim (승격 운영선 주장)
- any new dataset, bundle, runtime, or report identity created in Stage 07 is synchronized into `docs/registers/artifact_registry.csv` in the same pass

## Required Inputs

- `../01_inputs/input_refs.md`
- `../../../docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
- `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
- `../../../docs/decisions/2026-04-23_stage07_tier_b_dual_verdict_packet_adopted.md`
- `../../../docs/policies/tiered_readiness_exploration.md`
- `../../06_tiered_readiness_exploration/04_selected/selection_status.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`
- `../../../docs/context/current_working_state.md`

## Required Outputs

- updated `03_reviews/review_index.md`
- updated `04_selected/selection_status.md`
- `01_inputs/stage07_tier_b_dual_verdict_local_spec.md`
- the first Stage 07 `Tier B dual verdict packet (Tier B 이중 판정 팩)` summary and review family
- same-pass registry sync when new durable artifact identity appears

## Close Bias

- close Stage 07 only after the first dual-verdict question has a durable `keep|prune` plus `yes|no` answer on a validated user-weight rerun
- do not let Stage 07 absorb an opened `MT5 path (MT5 경로)` or a promoted operating-line claim by momentum alone
