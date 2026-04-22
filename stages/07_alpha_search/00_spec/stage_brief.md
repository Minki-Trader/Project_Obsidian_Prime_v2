# Stage 07 Alpha Search

- stage: `07_alpha_search`
- stage_type: `alpha_search_stage`
- updated_on: `2026-04-22`
- owner_path: `stages/07_alpha_search/`

## Purpose

- open the first alpha-search stage after Stage 06 made the readiness family explicit enough to hand downstream work a durable boundary
- keep the current strict `Tier A` runtime rule unchanged while giving bounded alpha-search questions a separate home
- search on one `Tier A main lane (Tier A 메인 레인)` and one separate `Tier B offline-only lane (Tier B 별도 오프라인 전용 레인)` without implying runtime safety or operating promotion

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
  - bounded alpha-search work on the full-surface `Tier A main lane`
  - bounded alpha-search work on the separate keep42 `Tier B` reduced-context lane
  - lane-specific threshold, exposure, sizing, and coarse control exploration with separate reporting
  - deciding whether the separate `Tier B` lane deserves continued bounded search after the first Stage 07 pack
  - optional later comparison against one `macro-aware (매크로 인지)` Tier B variant only after the shared keep42 lane already exists as materialized evidence
- not in scope:
  - changing the current strict `Tier A` runtime rule
  - claiming `Tier B` is contract-equivalent to `Tier A`
  - `simulated execution (가상 실행)`
  - `MT5 path (MT5 경로)` expansion
  - `operating promotion (운영 승격)`
  - contract or public runtime-input changes under `docs/contracts/**`

## Success Criteria

- the first Stage 07 alpha-search read keeps `Tier A` and `Tier B` on separate reporting lanes
- the first Stage 07 pack records a clear continuation-or-prune read for the separate `Tier B` lane
- no Stage 07 artifact blurs alpha-search permission into runtime safety, MT5 readiness, or operating promotion
- any new dataset, bundle, runtime, or report identity created in Stage 07 is synchronized into `docs/registers/artifact_registry.csv` in the same pass

## Required Inputs

- `../01_inputs/input_refs.md`
- `../../../docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
- `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
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
- the first bounded Stage 07 alpha-search packet or equivalent durable decision on the opening lane layout
- same-pass registry sync when new durable artifact identity appears

## Close Bias

- close Stage 07 only after the first alpha-search family has a durable keep-or-prune read without implying operating promotion
- do not let Stage 07 absorb runtime implementation, MT5 feasibility, or operating promotion by momentum alone
