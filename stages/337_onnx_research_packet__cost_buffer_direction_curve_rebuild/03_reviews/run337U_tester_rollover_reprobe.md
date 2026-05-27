# Stage337U Tester Rollover Reprobe(337U 테스터 이월 재탐침)

- run_id(실행 ID): `run337U_source_clean_cost_buffer_rebuild_or_tester_rollover_reprobe_v1`
- status(상태): `completed_stage337U_tester_rollover_reprobe_gap_remains_no_forward_decision`
- judgment(판정): `tester_rollover_gap_remains_u42_cost_fragility_already_blocks_onnx_ready_claim`
- decision(결정): `stage337U_open_run337V_cost_buffer_rebuild_and_source_policy_repair_design_no_selection`
- requested ToDate(요청 종료일): `2026.05.30`
- API latest US100 close(API 최신 US100 종가): `2026-05-27T03:05:00Z`
- MT5 completed(MT5 완료): `1/1`
- tester reached feature last(테스터 피처 끝 도달): `0/1`
- raw proxy parity(원시 프록시 동등성): `2/5`
- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `5/5`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Runtime Metrics(런타임 지표)

| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |
|---|---|---:|---:|---:|---:|
| `u42_plain_rf` | `completed/completed/completed` | `99.9` | `1.13` | `344` | `112.86` |

## Boundary(경계)

run337U(337U 실행)는 새 후보 개발이 아니라 tester rollover(테스터 이월) 재탐침이다. ONNX(온엑스), feature order(피처 순서), D/B surface(D/B 표면), threshold(임계값), risk/lot(위험/랏), ATR SL/TP(ATR 손절/익절)는 바꾸지 않았다.

효과(effect, 효과): 테스터가 feature_last(피처 마지막 시점)에 닿는지 확인하되, u42의 비용 취약성 때문에 ONNX-ready(온엑스 준비)나 Forward Passed(전진 통과)는 주장하지 않는다.
