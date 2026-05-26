# run336N Timestamp-Aligned Parity Review(336N 타임스탬프 정렬 동등성 검토)

- run_id(실행 ID): `run336N_repair_gap_or_parity_review_v1`
- status(상태): `completed_timestamp_aligned_proxy_mt5_parity_review_no_forward_decision`
- judgment(판정): `feature_handoff_gap_repaired_proxy_mismatch_explained_by_tester_feature_timestamp_basis`
- decision(결정): `stage336N_timestamp_aligned_parity_passed_queue_forward_attribution_no_selection`
- timestamp-aligned proxy-MT5 parity(타임스탬프 정렬 프록시-MT5 동등성): `20/20`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Finding(발견)

Action(행동): run336M(336M 실행)의 feature CSV(피처 CSV) 전체가 아니라 MT5 telemetry(메타트레이더5 기록)의 `feature_ready=true` cycle bar_time(사이클 봉 시간)과 교집합을 잡아 ONNX inference(온엑스 추론)를 다시 계산했다.

Effect(효과): 기존 run336M proxy mismatch(프록시 불일치)는 모델/ONNX 불일치가 아니라 timestamp basis(타임스탬프 기준) 차이로 설명된다. 정렬 후 4개 attempt(시도)의 `feature_ready/model_ok/long/short/flat`이 모두 일치했다.

| attempt(시도) | feature_csv_rows(피처 행) | mt5_cycle_rows(MT5 사이클 행) | feature_ready_rows(피처 준비 행) | feature_rows_not_seen(미처리 피처 행) |
|---|---:|---:|---:|---:|
| m48_bal_rf | 5640 | 5553 | 5553 | 87 |
| m48_plain_rf | 5640 | 5553 | 5553 | 87 |
| u42_bal_rf | 8012 | 7805 | 7805 | 207 |
| u42_plain_rf | 8012 | 7805 | 7805 | 207 |

## Boundary(경계)

run336N은 runtime parity review(런타임 동등성 검토)다. Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
