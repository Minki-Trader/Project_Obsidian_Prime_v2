# run337ER shifted custom failure memory(시프트 커스텀 실패 기억)

## 판정

- decision(판정): `Forward Blocked`
- diagnostic decision(진단 판정): `failure_memory_strengthened_synthetic_shifted_custom_no_forward_failed_authority`
- status(상태): `completed_stage337ER_shifted_custom_failure_memory_no_forward_decision`
- goal achieve(목표 달성): `not_claimed(주장 안 함)`

## 실행 효과

run337EQ의 broker Strategy Tester(브로커 전략 테스터)는 최신 feature(피처) `2026-05-28 06:00 UTC`까지 닿지 못해 Forward Blocked(전진 차단)으로 남았다. run337ER는 같은 frozen ONNX(고정 ONNX), feature order(피처 순서), argmax decision surface(argmax 결정 표면), threshold(임계값), fixed lot(고정 랏), risk logic(위험 로직)을 유지하고, timestamp shift(타임스탬프 이동) custom symbol(커스텀 심볼) `US100.OPV337ERD`만 써서 tester visibility(테스터 가시성)를 진단했다.

효과(effect, 효과)는 broker forward authority(브로커 전진 권한)를 우회하지 않고, 최신 구간이 보일 때 KPI(핵심 지표)와 curve pocket(곡선 포켓)이 어떤 실패 기억을 만드는지만 분리한 것이다.

## 핵심 수치

- seed status(seed 상태): `completed`
- shifted feature last(이동 피처 마지막): `2026-05-27 06:00:00+00:00`
- runtime last(런타임 마지막): `2026-05-27 07:57:59+00:00`
- latest lag minutes(최신 지연 분): `-117.98333333333333`
- attempt rows(시도 행): `7`
- trade rows(거래 행): `267`
- rank1 net/PF/DD(rank1 순손익/손익비/낙폭): `-33.75` / `0.82` / `66.81`
- failure counts(실패 개수): `{"attempts_with_cost_1pt_break_or_thin": 6, "attempts_with_negative_net": 5, "attempts_with_nonconstructive_curve": 7, "attempts_with_pf_below_1": 5, "attempts_with_short_net_negative": 7}`

## 경계

- Forward Passed(전진 통과): `not_claimed(주장 안 함)`
- Forward Failed(전진 실패): `not_claimed_synthetic_route(합성 경로라 주장 안 함)`
- Forward Blocked(전진 차단): `claimed_by_broker_visibility_gap_reference(브로커 가시성 공백 근거로 주장)`
- live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위): 모두 `not_claimed(주장 안 함)`

## 근거 파일

- shifted MT5 report(이동 MT5 보고): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/shifted_custom_mt5_report.csv`
- regime attribution(국면 귀속): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/shifted_custom_regime_attribution_report.csv`
- D/B attribution(D/B 귀속): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/shifted_custom_db_attribution_report.csv`
- lot normalized(랏 정규화): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/shifted_custom_lot_normalized_report.csv`
- cost stress(비용 스트레스): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/shifted_custom_cost_stress_report.csv`
- curve pocket(곡선 포켓): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/shifted_custom_curve_pocket_report.csv`
- failure memory matrix(실패 기억 행렬): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/failure_memory_matrix.csv`
- gate audit(게이트 감사): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/shifted_custom_required_gate_coverage_audit.csv`
- final decision(최종 판정): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ER/final_forward_decision_report.json`

## 다음 작업

`run337ES_no_overfit_repair_or_broker_rollover_reprobe_without_db_v1`는 broker rollover(브로커 롤오버) 재확인 또는 failure memory(실패 기억) 기반 no-overfit repair(비과적합 수리) 설계로 이어진다. 이 수리는 새 데이터에 threshold(임계값)를 맞추는 방식이 아니라, 실패 원인을 고립해서 후보군 설계를 다시 세우는 방식이어야 한다.
