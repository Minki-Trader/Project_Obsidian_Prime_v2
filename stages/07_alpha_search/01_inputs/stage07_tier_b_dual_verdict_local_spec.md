# Stage 07 Tier B Dual Verdict Local Spec (Stage 07 Tier B 이중 판정 로컬 규격)

## Scope (범위)

- this `local spec (로컬 규격)` defines the first bounded `Stage 07 Tier B dual verdict packet (Stage 07 Tier B 이중 판정 팩)`
- the packet answers only two questions:
  - should `Tier B (Tier B)` stay open as a `separate lane (별도 레인)`?
  - may the packet move forward as an `MT5 feasibility candidate (MT5 가능성 후보)`?
- the packet does not change any global `contract (계약)` under `docs/contracts/**`

## Inputs (입력)

- `data/raw/mt5_bars/m5/**` rebuilt through the current `build_feature_frame() (특성 프레임 재구성)` parser identity with a validated user-weight source
- `stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_reduced_context_0001/reduced_context_evaluation_summary_fpmarkets_v2_tier_b_reduced_context_0001.json`
- carry-forward policy and decision refs:
  - `docs/policies/tiered_readiness_exploration.md`
  - `docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
  - `docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
  - `docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
  - `docs/decisions/2026-04-23_stage07_tier_b_dual_verdict_packet_adopted.md`

## User Weight Source Rule (사용자 가중치 소스 규칙)

- the packet requires one validated `monthly-frozen weights CSV (월별 동결 가중치 CSV)`
- allowed columns (허용 컬럼): `month`, `msft_xnas_weight`, `nvda_xnas_weight`, `aapl_xnas_weight`
- allowed month coverage (허용 월 범위): every month from `2022-08` through `2026-04` exactly once
- validation rules (검증 규칙):
  - no duplicate month rows
  - no missing or extra months
  - all weight columns must be numeric
  - each month's weight sum must equal `1.0` within tolerance
- if validation fails, the packet is `blocked (차단)` before any verdict is written

## Model And Surface Rule (모델 및 표면 규칙)

- reuse the current shared `keep42 reduced-context model (keep42 축약 문맥 모델)` only
- keep the same `train / validation / holdout (학습 / 검증 / 보류 평가)` windows as the Stage 06 reduced-context pass
- keep `Tier A train only (Tier A 학습 전용)` fitting
- keep `Tier A (Tier A)` and `Tier B (Tier B)` on separate `reporting lanes (보고 레인)`
- keep the active-surface note explicit:
  - the shared keep42 active surface is weight-neutral on direct inputs because `top3_weighted_return_1` and `us100_minus_top3_weighted_return_1` remain outside the active feature set

## Decision Rule (판정 규칙)

- `separate_lane_verdict (별도 레인 판정)`:
  - `keep` if the rerun `Tier B holdout log_loss (Tier B 보류 평가 로그 손실)` stays below the Stage 06 full-baseline floor `1.963620` and the holdout coarse `control grid (제어 격자)` still has at least one positive `proxy config (프록시 구성)`
  - `prune` otherwise
- `mt5_candidate_verdict (MT5 후보 판정)`:
  - `yes` only if `separate_lane_verdict=keep` and the packet used a validated user-weight source
  - `no` if the rerun completes but the packet should not move forward as an `MT5 feasibility candidate (MT5 가능성 후보)`
  - `blocked` only when the user-weight source itself fails validation and the packet cannot be evaluated

## Required Outputs (필수 산출물)

- `stages/07_alpha_search/02_runs/tier_b_dual_verdict_0001/tier_b_dual_verdict_manifest_fpmarkets_v2_0001.json`
- `stages/07_alpha_search/02_runs/tier_b_dual_verdict_0001/tier_b_dual_verdict_evaluation_summary_fpmarkets_v2_0001.json`
- `stages/07_alpha_search/02_runs/tier_b_dual_verdict_0001/tier_b_dual_verdict_control_summary_fpmarkets_v2_0001.json`
- `stages/07_alpha_search/02_runs/tier_b_dual_verdict_0001/tier_b_dual_verdict_summary_fpmarkets_v2_0001.json`
- `stages/07_alpha_search/03_reviews/report_fpmarkets_v2_tier_b_dual_verdict_0001.md`
- `stages/07_alpha_search/03_reviews/decision_fpmarkets_v2_tier_b_dual_verdict_0001.md`

## Not Opened Here (이번 패스에서 열지 않는 것)

- no new `model family (모델 계열)`
- no optional `macro-aware variant (매크로 인지 변형)`
- no opened `MT5 path (MT5 경로)`
- no changed `Tier A runtime rule (Tier A 런타임 규칙)`
- no promoted operating-line claim (승격 운영선 주장)
