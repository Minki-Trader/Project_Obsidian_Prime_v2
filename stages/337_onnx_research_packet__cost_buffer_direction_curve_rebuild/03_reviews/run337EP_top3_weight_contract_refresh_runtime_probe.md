# run337EP Top3 Weight Contract Refresh Runtime Probe(상위3 가중치 계약 갱신 런타임 탐침)

## Summary(요약)

run337EP(337EP 실행)는 run337EO(337EO 실행) 뒤에 남은 2026-05 top3 monthly proxy weight(월간 상위3 대리 가중치) 공백을 no-lookahead(미래 참조 없음) 방식으로 보강하고, frozen ONNX(고정 ONNX) 7개 survivor(생존 후보)를 다시 score/reprobe(점수화/재탐침)했다. 그 다음 MT5 argmax runtime parity(MT5 최대확률 런타임 동등성)를 trading disabled(거래 비활성) 상태로 확인했다.

- status(상태): `completed_stage337EP_top3_weight_contract_repaired_runtime_probe_executed_no_forward_decision`
- judgment(판정): `top3_2026_05_weight_contract_resolved_feature_gap_and_mt5_argmax_runtime_parity_passed_but_forward_kpi_not_claimed`
- decision(결정): `stage337EP_open_run337EQ_forward_kpi_attribution_cost_stress_curve_pocket`
- next_action(다음 행동): `run337EQ_forward_kpi_attribution_cost_stress_curve_pocket_without_db_v1`
- parent_run(부모 실행): `run337EO_refresh_survivor_feature_handoff_and_surface_reprobe_without_db_v1`
- claim_boundary(주장 경계): `research_development_only_stage337EP_top3_weight_contract_refresh_surface_runtime_probe_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Top3 Contract(상위3 계약)

- month(월): `2026-05`
- source_timestamp(원천 시각): `2026-04-30T23:00:00+00:00`
- source_rule(원천 규칙): `last_common_closed_bar_before_month_start`
- bootstrap_month(부트스트랩 월): `false`
- weight_sum(가중치 합): `1`
- no_lookahead_passed(미래 참조 없음 통과): `true`
- contract_sha256(계약 해시): `8cd4662f119b77ca074795715c11e7c24280cb98143d18b9d6cc227f61fc1f49`

Effect(효과): macro-equity 58 feature set(매크로-주식 58 피처 세트)이 2026-04-30에서 멈추던 공백을 2026-05-28T06:00:00Z까지 확장했다. 이 보강은 새 학습(new training, 새 학습), threshold tuning(임계값 조정), lot optimization(랏 최적화), candidate selection(후보 선택)을 하지 않았다.

## Feature Handoff(피처 인계)

- `macro_equity_lag_safe_rescue`: feature_count(피처 수) `58`, valid_rows(유효 행) `8075`, first_valid(첫 유효 시각) `2026-04-14T01:05:00+00:00`, last_valid(마지막 유효 시각) `2026-05-28T06:00:00+00:00`, status(상태) `materialized`.
- `technical_session_vol_lag_safe`: feature_count(피처 수) `42`, valid_rows(유효 행) `8190`, first_valid(첫 유효 시각) `2026-04-14T01:05:00+00:00`, last_valid(마지막 유효 시각) `2026-05-28T06:00:00+00:00`, status(상태) `materialized`.

- valid_feature_set_rows_total(유효 피처 세트 행 합): `16265`
- survivor_feature_rows_total(생존 후보 피처 행 합): `56870`

## Frozen Surface Reprobe(고정 표면 재탐침)

- rank(순위) `1` `macro_equity_lag_safe_rescue`: rows(행) `8075`, short/flat/long(매도/평탄/매수) `52/7999/24`, nonflat(비평탄) `76`, last_nonflat(마지막 비평탄) `2026-05-27 17:35:00+00:00`.
- rank(순위) `2` `technical_session_vol_lag_safe`: rows(행) `8190`, short/flat/long(매도/평탄/매수) `60/8064/66`, nonflat(비평탄) `126`, last_nonflat(마지막 비평탄) `2026-05-27 17:35:00+00:00`.
- rank(순위) `3` `technical_session_vol_lag_safe`: rows(행) `8190`, short/flat/long(매도/평탄/매수) `70/8015/105`, nonflat(비평탄) `175`, last_nonflat(마지막 비평탄) `2026-05-27 18:05:00+00:00`.
- rank(순위) `4` `macro_equity_lag_safe_rescue`: rows(행) `8075`, short/flat/long(매도/평탄/매수) `75/7977/23`, nonflat(비평탄) `98`, last_nonflat(마지막 비평탄) `2026-05-27 18:00:00+00:00`.
- rank(순위) `5` `technical_session_vol_lag_safe`: rows(행) `8190`, short/flat/long(매도/평탄/매수) `68/8021/101`, nonflat(비평탄) `169`, last_nonflat(마지막 비평탄) `2026-05-27 18:00:00+00:00`.
- rank(순위) `6` `macro_equity_lag_safe_rescue`: rows(행) `8075`, short/flat/long(매도/평탄/매수) `62/7989/24`, nonflat(비평탄) `86`, last_nonflat(마지막 비평탄) `2026-05-27 17:35:00+00:00`.
- rank(순위) `7` `macro_equity_lag_safe_rescue`: rows(행) `8075`, short/flat/long(매도/평탄/매수) `67/7991/17`, nonflat(비평탄) `84`, last_nonflat(마지막 비평탄) `2026-05-27 17:35:00+00:00`.

- surface_rows(표면 행): `7`
- surface_nonflat_rows(표면 비평탄 행): `814`
- surface_short_long_total(표면 매도/매수 합): `454/360`
- onnx_parity_failed_rows(ONNX 동등성 실패 행): `0`

## MT5 Runtime Probe(MT5 런타임 탐침)

- `eh_rank01`: runtime_status(런타임 상태) `completed`, matched_rows(일치 행) `276`, probability_mismatch_rows(확률 불일치 행) `0`, decision_mismatch_rows(결정 불일치 행) `0`, max_abs_probability_diff(최대 절대 확률 차이) `2.59364e-07`.
- `eh_rank02`: runtime_status(런타임 상태) `completed`, matched_rows(일치 행) `276`, probability_mismatch_rows(확률 불일치 행) `0`, decision_mismatch_rows(결정 불일치 행) `0`, max_abs_probability_diff(최대 절대 확률 차이) `2.0344e-07`.
- `eh_rank03`: runtime_status(런타임 상태) `completed`, matched_rows(일치 행) `276`, probability_mismatch_rows(확률 불일치 행) `0`, decision_mismatch_rows(결정 불일치 행) `0`, max_abs_probability_diff(최대 절대 확률 차이) `2.16765e-07`.
- `eh_rank04`: runtime_status(런타임 상태) `completed`, matched_rows(일치 행) `276`, probability_mismatch_rows(확률 불일치 행) `0`, decision_mismatch_rows(결정 불일치 행) `0`, max_abs_probability_diff(최대 절대 확률 차이) `2.88822e-07`.
- `eh_rank05`: runtime_status(런타임 상태) `completed`, matched_rows(일치 행) `276`, probability_mismatch_rows(확률 불일치 행) `0`, decision_mismatch_rows(결정 불일치 행) `0`, max_abs_probability_diff(최대 절대 확률 차이) `1.67355e-07`.
- `eh_rank06`: runtime_status(런타임 상태) `completed`, matched_rows(일치 행) `276`, probability_mismatch_rows(확률 불일치 행) `0`, decision_mismatch_rows(결정 불일치 행) `0`, max_abs_probability_diff(최대 절대 확률 차이) `2.25905e-07`.
- `eh_rank07`: runtime_status(런타임 상태) `completed`, matched_rows(일치 행) `276`, probability_mismatch_rows(확률 불일치 행) `0`, decision_mismatch_rows(결정 불일치 행) `0`, max_abs_probability_diff(최대 절대 확률 차이) `1.91568e-07`.

- attempt_rows(시도 행): `7`
- matched_rows(일치 행): `1932`
- probability_mismatch_rows(확률 불일치 행): `0`
- decision_mismatch_rows(결정 불일치 행): `0`
- max_abs_probability_diff(최대 절대 확률 차이): `2.88822e-07`
- runtime_long_short_flat_total(런타임 매수/매도/평탄 합): `4/46/1882`
- order_attempt_count/order_fill_count(주문 시도/체결 수): `0/0`

Effect(효과): Python/joblib/ONNX(파이썬/joblib/ONNX) score surface(점수 표면)와 MT5 runtime(메타트레이더5 런타임)의 probability/decision(확률/결정) 해석은 이번 probe window(탐침 구간)에서 일치했다. 거래가 비활성이라 profit/PF/DD(손익/수익 팩터/낙폭)는 측정하지 않았다.

## Judgment Boundary(판정 경계)

Forward Passed(전진 통과), Forward Failed(전진 실패), Goal Achieve(목표 달성)는 모두 `not_claimed`다. 이유는 run337EP(337EP 실행)가 parity/data handoff(동등성/데이터 인계)를 확인했을 뿐, frozen forward MT5 KPI(고정 전진 MT5 성과), D/B attribution(D/B 귀속), lot-normalized result(랏 정규화 결과), cost stress(비용 스트레스), curve pocket(곡선 포켓)을 아직 닫지 않았기 때문이다.

Next(다음)는 `run337EQ_forward_kpi_attribution_cost_stress_curve_pocket_without_db_v1`이며, 효과는 수익성보다 overfit/parity/forward robustness(과적합/동등성/전진 강건성) 판단에 필요한 KPI(성과 지표)와 regime attribution(국면 귀속)을 분리해서 닫는 것이다.
