# Stage337AP Broker Tester History Repair(337AP 브로커 테스터 이력 수리)

- run_id(실행 ID): `run337AP_broker_tester_history_repair_or_next_rollover_v1`
- status(상태): `completed_stage337AP_broker_history_repair_gap_remains_no_forward_decision`
- judgment(판정): `broker_tester_history_gap_remains_after_api_warmup_and_reprobe`
- decision(결정): `stage337AP_open_run337AQ_tester_visible_cutoff_and_db_instrumentation_no_selection`
- next_action(다음 행동): `run337AQ_tester_visible_cutoff_policy_and_db_instrumentation_v1`
- API latest close(API 최신 종가): `2026-05-27T09:30:00Z`
- runtime completed(런타임 완료): `3/3`
- tester reached feature_last(테스터 피처 끝 도달): `0/3`
- raw proxy/MT5(원시 프록시/MT5): `6/15`
- timestamp-aligned proxy/MT5(시점 맞춤 프록시/MT5): `15/15`
- D/B missing columns(D/B 누락 컬럼): `7`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

run337AP(337AP 실행)는 MT5 API history warmup(API 이력 예열) 뒤 같은 frozen ONNX(고정 온엑스)를 Strategy Tester(전략 테스터)에 다시 넣었다. 효과(effect, 효과)는 broker tester gap(브로커 테스터 공백)이 데이터 캐시 문제인지, tester-visible cutoff(테스터 가시 컷오프) 문제인지 더 좁히는 것이다.

## Proxy Use(프록시 사용)

| attempt(시도) | gap(공백) | raw proxy(원시 프록시) | aligned proxy(정렬 프록시) | runtime usable(런타임 사용) | forward usable(전진 사용) |
|---|---:|---:|---:|---|---|
| `u42_plain_rf_ap_api_warm_model4_real_ticks` | `tester_feature_last_gap_remains` | `2/5` | `5/5` | `True` | `False` |
| `u42_plain_rf_ap_api_warm_model0_generated` | `tester_feature_last_gap_remains` | `2/5` | `5/5` | `True` | `False` |
| `u42_plain_rf_ap_api_warm_model4_wide_todate` | `tester_feature_last_gap_remains` | `2/5` | `5/5` | `True` | `False` |

## Boundary(경계)

proxy expected(프록시 예상값)는 runtime signal parity(런타임 신호 동등성) 확인에는 쓸 수 있지만, broker tester(브로커 테스터)가 feature_last(피처 끝)에 닿지 않거나 D/B source(D/B 원천)가 없으면 Forward Passed/Failed(전진 통과/실패)에 쓸 수 없다.
