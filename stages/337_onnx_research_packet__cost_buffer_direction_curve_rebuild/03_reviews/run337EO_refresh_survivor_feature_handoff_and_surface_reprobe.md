# run337EO Refresh Survivor Feature Handoff and Surface Reprobe(생존 후보 피처 인계 갱신과 표면 재탐침)

run337EO(337EO 실행)는 survivor feature handoff(생존 후보 피처 인계)를 최신 forward raw data(전진 원천 데이터)로 다시 만들고, frozen ONNX(고정 ONNX) 7개를 새 전진 행에 재점수화했다. 효과(effect, 효과)는 후보 수정 없이 표면이 새 구간에서 살아나는지 확인하는 것이다.

## Summary(요약)

- status(상태): `completed_stage337EO_survivor_feature_handoff_refreshed_surface_reprobed_no_forward_decision`
- judgment(판정): `survivor_feature_handoff_refreshed_and_frozen_onnx_surface_reprobed_but_forward_decision_not_claimed`
- decision(결정): `stage337EO_open_run337EP_refreshed_forward_surface_runtime_probe_or_failure_memory`
- raw_source_root(원천 사용 경로): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EO/raw_refresh_probe`
- raw_refresh_status(원천 갱신 상태): `completed`
- feature_sets_materialized(물질화 피처 세트): `2`
- survivor_rows_reprobed(재탐침 생존 후보): `7`
- total_forward_feature_rows(전진 피처 행 합): `38350`
- total_nonflat_rows(비평탄 행 합): `556`
- parity_failed_rows(동등성 실패 행): `0`
- forward_passed(전진 통과): `not_claimed`
- forward_failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337EO_survivor_feature_handoff_refresh_surface_reprobe_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Feature Sets(피처 세트)

| feature_set_id | feature_count | valid_rows | first_valid_timestamp | last_valid_timestamp | status |
| --- | --- | --- | --- | --- | --- |
| macro_equity_lag_safe_rescue | 58 | 3445 | 2026-04-14T01:05:00+00:00 | 2026-04-30T23:55:00+00:00 | materialized |
| technical_session_vol_lag_safe | 42 | 8190 | 2026-04-14T01:05:00+00:00 | 2026-05-28T06:00:00+00:00 | materialized |

## Open Feature Caveat(열린 피처 주의점)

- observed(관측): `macro_equity_lag_safe_rescue` valid rows(유효 행)는 `2026-04-30T23:55:00+00:00`에서 멈췄고, `technical_session_vol_lag_safe`는 `2026-05-28T06:00:00+00:00`까지 닿았다.
- likely source(추정 원천): `top3_weighted_return_1`와 `us100_minus_top3_weighted_return_1` missing/nonfinite rows(누락/비유한 행)가 각각 `5257`개다.
- effect(효과): run337EP(337EP 실행)는 score threshold(점수 임계값)나 lot(랏)을 고치지 말고, top3 monthly proxy weight(월간 top3 대리 가중치) handoff(인계)의 no-lookahead(미래 참조 없음) 가능 여부를 먼저 분리해야 한다.

## Surface Reprobe(표면 재탐침)

| rank | feature_set_id | feature_rows | decision_short_total | decision_flat_total | decision_long_total | decision_nonflat_total | signal_density | surface_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | macro_equity_lag_safe_rescue | 3445 | 15 | 3426 | 4 | 19 | 0.0055152394775 | reprobed_nonflat |
| 2 | technical_session_vol_lag_safe | 8190 | 60 | 8064 | 66 | 126 | 0.0153846153846 | reprobed_nonflat |
| 3 | technical_session_vol_lag_safe | 8190 | 70 | 8015 | 105 | 175 | 0.0213675213675 | reprobed_nonflat |
| 4 | macro_equity_lag_safe_rescue | 3445 | 17 | 3421 | 7 | 24 | 0.00696661828737 | reprobed_nonflat |
| 5 | technical_session_vol_lag_safe | 8190 | 68 | 8021 | 101 | 169 | 0.0206349206349 | reprobed_nonflat |
| 6 | macro_equity_lag_safe_rescue | 3445 | 16 | 3424 | 5 | 21 | 0.00609579100145 | reprobed_nonflat |
| 7 | macro_equity_lag_safe_rescue | 3445 | 17 | 3423 | 5 | 22 | 0.00638606676343 | reprobed_nonflat |


## ONNX Parity(ONNX 동등성)

| rank | feature_set_id | rows_checked | max_abs_probability_diff | decision_mismatch_rows | parity_status |
| --- | --- | --- | --- | --- | --- |
| 1 | macro_equity_lag_safe_rescue | 3445 | 1.80834247632e-07 | 0 | passed |
| 2 | technical_session_vol_lag_safe | 8190 | 1.60924117198e-07 | 0 | passed |
| 3 | technical_session_vol_lag_safe | 8190 | 1.74755367732e-07 | 0 | passed |
| 4 | macro_equity_lag_safe_rescue | 3445 | 1.49459459364e-07 | 0 | passed |
| 5 | technical_session_vol_lag_safe | 8190 | 1.73815820792e-07 | 0 | passed |
| 6 | macro_equity_lag_safe_rescue | 3445 | 1.6527025265e-07 | 0 | passed |
| 7 | macro_equity_lag_safe_rescue | 3445 | 1.67450298905e-07 | 0 | passed |


## Gates(게이트)

| gate_id | status | observed |
| --- | --- | --- |
| eo_gate_parent_en_present | passed | path=stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EN/final_decision.json |
| eo_gate_raw_refresh_attempted | passed | status=completed |
| eo_gate_full_raw_or_declared_fallback | passed | completed=12;source=stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EO/raw_refresh_probe |
| eo_gate_exact_feature_sets_materialized | passed | feature_sets=2 |
| eo_gate_survivor_handoff_all_refreshed | passed | rows=7 |
| eo_gate_frozen_onnx_surface_reprobed | passed | rows=7 |
| eo_gate_joblib_onnx_parity_passed | passed | rows=7 |
| eo_gate_no_forbidden_mutation | passed | training=not_run;threshold_tuning=not_run;lot_optimization=not_run;candidate_selection=not_run |
| eo_gate_forward_decision_not_claimed | passed | forward_passed=not_claimed;forward_failed=not_claimed |


## Judgment Boundary(판정 경계)

이 실행은 feature refresh/reprobe(피처 갱신/재탐침)다. net profit/PF/DD(순이익/손익비/드로다운)와 Strategy Tester(전략 테스터) 실행이 없으므로 Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다. 다음 조건은 refreshed expected surface(갱신 예상 표면)를 MT5 argmax runtime probe(MT5 argmax 런타임 탐침)와 KPI attribution(KPI 귀속)으로 연결하는 것이다.
