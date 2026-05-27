# Stage337AB Custom Symbol Intraday Tester Visibility Probe(337AB 커스텀 심볼 장중 테스터 가시성 탐침)

- run_id(실행 ID): `run337AB_custom_symbol_intraday_tester_visibility_probe_v1`
- status(상태): `completed_stage337AB_custom_symbol_tester_visibility_inconclusive_no_forward_decision`
- judgment(판정): `custom_symbol_intraday_tester_visibility_not_confirmed_requires_repair_or_next_day_reprobe`
- decision(결정): `stage337AB_open_run337AC_next_day_broker_or_custom_symbol_seed_repair_no_selection`
- next_action(다음 행동): `run337AC_next_day_broker_rollover_or_custom_symbol_seed_repair_v1`
- custom symbol(커스텀 심볼): `US100.OPV337AB`
- custom seed status(커스텀 심볼 심기 상태): `completed`
- custom API latest M5 close(커스텀 API 최신 5분봉 종가): `2026-05-27T05:15:00Z`
- MT5 runtime completed(MT5 런타임 완료): `2/2`
- broker control gap(브로커 대조 공백): `tester_feature_last_gap_remains`
- custom tester gap(커스텀 테스터 공백): `tester_feature_last_gap_remains`
- custom tester last observed(커스텀 테스터 마지막 관측): `2026-05-26T23:55:00Z`
- feature_last(피처 마지막 시점): `2026-05-27T02:00:00Z`
- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `6/10`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

run337AB(337AB 실행)는 API(응용 프로그램 인터페이스)에서 보이는 US100(US100) M1/M5 봉을 MQL5 custom symbol(커스텀 심볼)에 심고, 같은 frozen u42 ONNX(고정 u42 온엑스)와 같은 threshold/risk/lot(임계값/위험/로트)로 Strategy Tester(전략 테스터)를 다시 실행했다. custom symbol(커스텀 심볼)은 real ticks(실제 틱)가 없으므로 generated ticks(생성 틱) 모델을 visibility-only(가시성 전용)로 썼다.

Effect(효과): 이 결과는 tester visibility repair evidence(테스터 가시성 수리 근거)이지, Forward Passed(전진 통과), operating promotion(운영 승격), runtime authority(런타임 권위)가 아니다.

## Tester Boundary(테스터 경계)

| attempt(시도) | symbol(심볼) | log test to(로그 종료) | last observed(마지막 관측) | gap status(공백 상태) |
|---|---:|---:|---:|---:|
| `u42_plain_rf_ab_broker_control` | `US100` | `2026.05.27 00:00` | `2026-05-26T23:55:00Z` | `tester_feature_last_gap_remains` |
| `u42_plain_rf_ab_custom_symbol` | `US100.OPV337AB` | `2026.05.27 00:00` | `2026-05-26T23:55:00Z` | `tester_feature_last_gap_remains` |

## Proxy vs MT5(프록시 대 MT5)

proxy expected(프록시 예상값)는 timestamp-aligned(시점 맞춤) 범위에서만 runtime signal parity(런타임 신호 동등성) 판단에 쓰며, KPI authority(KPI 권한)나 Forward decision(전진 판정)으로 쓰지 않는다.
