# Stage337Q Tester Date Boundary Repair Review(337Q 테스터 종료일 경계 수리 리뷰)

- run_id(실행 ID): `run337Q_review_runtime_data_and_feature_source_repair_probe_v1`
- status(상태): `completed_stage337Q_tester_date_boundary_probe_partial_no_forward_decision`
- judgment(판정): `tester_date_boundary_gap_or_runtime_partial_requires_repair`
- decision(결정): `stage337Q_open_run337R_tester_boundary_or_source_policy_repair_no_selection`
- api_latest_us100_close(API 최신 US100 종가): `2026-05-27T02:25:00Z`
- MT5 completed(MT5 완료): `5/5`
- tester reached feature last(테스터 피처 끝 도달): `0/5`
- raw proxy parity(전체 프록시 동등성): `10/25`
- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `25/25`
- asof policy rows needing forward caution(전진 주의 필요 정책 행): `14`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Runtime Metrics(런타임 지표)

| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |
|---|---:|---:|---:|---:|---:|
| `c56_bal_rf` | `completed/completed/completed` | `-49.0` | `0.87` | `80` | `126.68` |
| `c56_plain_rf` | `completed/completed/completed` | `146.56` | `1.67` | `84` | `63.32` |
| `m48_bal_rf` | `completed/completed/completed` | `-17.63` | `0.98` | `351` | `113.73` |
| `m48_plain_rf` | `completed/completed/completed` | `267.39` | `1.4` | `344` | `91.32` |
| `u42_plain_rf` | `completed/completed/completed` | `99.9` | `1.13` | `344` | `112.86` |

## Boundary(경계)

run337Q(337Q 실행)는 tester ToDate boundary(테스터 종료일 경계) 수리 탐침이다. ONNX(온엑스), feature order(피처 순서), threshold(임계값), risk/lot(위험/랏)은 그대로 유지했다. 이 결과는 runtime probe(런타임 탐침)일 뿐이며 Forward Passed/Failed(전진 통과/실패)나 runtime authority(런타임 권위)가 아니다.
