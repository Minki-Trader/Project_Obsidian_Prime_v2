# Stage 06 v2 Follow-Up Pack Local Spec (Stage 06 v2 후속 팩 로컬 규격)

## Status (상태)

- this file is a `local spec (로컬 규격)` for the additive `tier_b_followup_pack_0001`
- it does not change the current active-stage decision (활성 단계 결정) or the strict `Tier A (엄격 Tier A)` runtime rule

## Inputs (입력)

- base dataset frame (기본 데이터셋 프레임): `build_feature_frame()` under the current parser identity
- readiness labels (준비도 라벨): `readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet`
- baseline seed family (기준선 시드 계열): `tier_b_offline_eval_0001`
- placeholder monthly weights (임시 월별 가중치): `foundation/config/top3_monthly_weights_fpmarkets_v2.csv`

## Included Reads (포함 판독)

1. `calibration fit (보정 적합)`
- fit method (적합 방식): `temperature scaling (온도 스케일링)` grid search on `validation (검증)` only
- candidates (후보): `identity_read_only`, `strict_tier_a_temperature_fit`, `tier_b_exploration_temperature_fit`
- objective (목표): `multiclass log loss (다중분류 로그 손실)` on the fit slice only
- evaluation slices (평가 구간): `validation` and `holdout` on separate `strict_tier_a` and `tier_b_exploration` lanes

2. `control sensitivity read (제어 민감도 판독)`
- source probabilities (입력 확률): lane-specific `temperature fit (온도 적합)` outputs
- entry threshold grid (진입 임계값 격자): `0.35, 0.40, 0.45, 0.50, 0.55`
- exposure cap grid (노출 상한 격자): `0.25, 0.50, 0.75`
- risk size grid (위험 사이징 격자): `0.50, 0.75, 1.00`
- proxy rule (프록시 규칙): use the predicted `long/short` direction only when that directional probability clears the threshold; `flat` stays no-trade
- output meaning (출력 의미): offline proxy only, not runtime PnL (런타임 손익) evidence

3. `robustness read (강건성 판독)`
- subgroup axis (하위군 축): `missing_groups` exact pattern
- time axis (시간 축): monthly slice with `row_count >= 500`
- purpose (목적): show whether the current Tier B read is broad or concentrated

4. `weight verdict read (가중치 판정 판독)`
- scenario family (시나리오 계열): placeholder equal-weight plus three coarse `60% tilt (60% 기울기)` scenarios
- mutable columns (변경 컬럼): `msft_xnas_weight`, `nvda_xnas_weight`, `aapl_xnas_weight`, `top3_weighted_return_1`, `us100_minus_top3_weighted_return_1`
- purpose (목적): determine whether the current placeholder weights are stable enough for offline screening while still requiring a later real-weight rerun for any simulated or MT5-path meaning

## Out Of Scope (범위 밖)

- `workspace_state.yaml` reflection (반영)
- `current_working_state.md` reflection (반영)
- active `selection_status.md` reflection (반영)
- any `docs/contracts/**` change
- any reduced-risk runtime family (축소위험 런타임 계열)
- any simulated execution (가상 실행), MT5-path work (MT5 경로 작업), or operating promotion (운영 승격)

## Expected Outputs (예상 산출물)

- one follow-up manifest (후속 명세) under `02_runs/tier_b_followup_pack_0001/`
- machine-readable JSON summaries for:
  - `calibration fit (보정 적합)`
  - `control sensitivity (제어 민감도)`
  - `robustness (강건성)`
  - `weight verdict (가중치 판정)`
- markdown reports (마크다운 보고서) for those four reads
- one `Stage 07 design draft (Stage 07 설계 초안)`
- one `Stage 06 close / Stage 07 open readout draft (Stage 06 종료 / Stage 07 개시 판독 초안)`

## Boundary Language (경계 언어)

- treat every result here as `additive follow-up (추가 후속)` only
- do not describe this pack as `Stage 06 closed (Stage 06 종료)` or `Stage 07 opened (Stage 07 개시)` without a later decision pass
- do not describe placeholder-weight reads as `promotion-ready (승격 준비 완료)`
