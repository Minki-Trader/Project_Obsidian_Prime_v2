# run336M Live-Safe Feature Handoff Repair(336M 실시간 안전 피처 인계 수리)

- run_id(실행 ID): `run336M_materialize_live_safe_feature_handoff_repair_v1`
- status(상태): `completed_live_safe_feature_handoff_repair_probe_partial_no_forward_decision`
- decision(결정): `stage336M_repaired_feature_handoff_probe_needs_runtime_or_parity_repair_no_selection`
- latest US100 close(최신 US100 종가): `2026-05-26T18:10:00Z`
- MT5 completed(MT5 완료): `4/4`
- feature latest gaps(최신 피처 공백): `0/4`
- proxy-MT5 signal parity(프록시-MT5 신호 동등성): `0/20`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Evidence(근거)

Action(행동): macro48/u42(거시48/US100 기술42)의 feature CSV(피처 CSV)를 live-safe overnight_return(실시간 안전 야간 수익률)로 재물질화하고, 같은 ONNX/threshold/risk/lot(온엑스/임계값/위험/로트)로 MT5 Strategy Tester(전략 테스터)를 다시 실행했다.

Effect(효과): run336K의 `feature_csv_timestamp_not_found` 문제가 feature handoff(피처 인계) 문제인지, 모델/런타임 문제인지 분리한다.

| attempt(시도) | tester(테스터) | feature_rows(피처 행) | trades(거래) | net(순익) | PF(수익 팩터) | DD(낙폭) | last_skip(마지막 스킵) |
|---|---:|---:|---:|---:|---:|---:|---|
| m48_bal_rf | completed | 5553 | 282 | 49.96 | 1.07 | 143.61 | feature_csv_timestamp_not_found:2026.05.25 19:55:00 |
| m48_plain_rf | completed | 5553 | 274 | 268.51 | 1.48 | 77.96 | feature_csv_timestamp_not_found:2026.05.25 19:55:00 |
| u42_bal_rf | completed | 7805 | 333 | 4.89 | 1.01 | 163.25 | feature_csv_timestamp_not_found:2026.05.25 06:55:00 |
| u42_plain_rf | completed | 7805 | 336 | 116.14 | 1.16 | 112.86 | feature_csv_timestamp_not_found:2026.05.25 06:55:00 |

## Boundary(경계)

이 실행은 repair probe(수리 탐침)다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), Goal Achieve(목표 달성)는 주장하지 않는다.
