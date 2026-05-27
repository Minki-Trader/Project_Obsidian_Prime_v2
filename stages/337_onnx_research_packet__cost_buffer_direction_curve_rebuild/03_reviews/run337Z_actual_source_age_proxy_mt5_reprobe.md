# Stage337Z Actual Source-Age Proxy MT5 Reprobe(337Z 실제 원천 나이 프록시 MT5 재탐침)

- run_id(실행 ID): `run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_v1`
- status(상태): `completed_stage337Z_actual_source_age_proxy_mt5_reprobe_gap_or_execution_issue_no_forward_decision`
- judgment(판정): `run337Z_runtime_reprobe_completed_or_attempted_but_tester_gap_or_execution_issue_blocks_forward_decision`
- decision(결정): `stage337Z_open_run337AA_tester_history_cache_or_source_session_policy_repair_no_selection`
- requested ToDate(요청 종료일): `2026.05.30`
- API latest US100 close(API 최신 US100 종가): `2026-05-27T04:20:00Z`
- MT5 completed(MT5 완료): `1/1`
- tester reached feature_last(테스터가 피처 마지막 시점 도달): `0/1`
- raw proxy parity(원시 프록시 동등성): `2/5`
- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `5/5`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Runtime Metrics(런타임 지표)

| attempt(시도) | status(상태) | net(순익) | PF(수익요인) | trades(거래수) | DD(드로다운) |
|---|---:|---:|---:|---:|---:|
| `u42_plain_rf` | `completed/completed/completed` | `99.9` | `1.13` | `344` | `112.86` |

## Boundary(경계)

run337Z(337Z 실행)는 새 후보 개발이 아니다. 효과(effect, 효과)는 run337Y(337Y 실행)가 요구한 fresh MT5 runtime execution(신규 MT5 런타임 실행), tester feature_last reach(테스터 피처 마지막 도달), proxy-vs-MT5 difference(프록시 대 MT5 차이)를 실제 근거로 닫는 것이다.

ONNX(온엑스), Adapter package(어댑터 패키지), feature order(피처 순서), D/B decision surface(D/B 결정 표면), score threshold(점수 임계값), risk/lot logic(위험/랏 로직), ATR SL/TP(ATR 손절/익절)는 바꾸지 않았다.
