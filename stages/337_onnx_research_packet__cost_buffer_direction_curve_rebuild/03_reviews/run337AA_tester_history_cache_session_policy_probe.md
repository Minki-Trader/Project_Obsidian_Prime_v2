# Stage337AA Tester History Cache Session Policy Probe(337AA 테스터 히스토리 캐시 세션 정책 탐침)

- run_id(실행 ID): `run337AA_tester_history_cache_repair_or_actual_source_session_policy_probe_v1`
- status(상태): `completed_stage337AA_tester_current_day_boundary_diagnosed_no_forward_decision`
- judgment(판정): `strategy_tester_current_day_midnight_boundary_confirmed_custom_symbol_or_next_day_reprobe_required`
- decision(결정): `stage337AA_open_run337AB_custom_symbol_intraday_tester_visibility_probe_no_selection`
- API latest US100 close(API 최신 US100 종가): `2026-05-27T04:40:00Z`
- MT5 completed(MT5 완료): `3/3`
- tester feature_last gaps(테스터 피처 마지막 공백): `3/3`
- current-day midnight cap(현재일 자정 경계 확인): `2`
- root cause(원인): `requires_more_evidence;strategy_tester_current_day_midnight_boundary`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Boundary Micro Probes(경계 미세 탐침)

| scenario(시나리오) | requested ToDate(요청 종료일) | log test to(로그 종료) | history sync to(히스토리 동기화 종료) | gap(공백) |
|---|---:|---:|---:|---:|
| `tester_to_current_calendar_date_control` | `2026.05.27` | `2026.05.27 00:00` | `2026.05.26` | `125.0` |
| `tester_to_next_calendar_date_control` | `2026.05.28` | `2026.05.27 00:00` | `2026.05.26` | `125.0` |
| `tester_to_future_rollover_control` | `2026.05.30` | `2026.05.27 00:00` | `2026.05.26` | `125.0` |

## Meaning(의미)

terminal API(터미널 API)는 최신 US100 M5(US100 5분봉)를 볼 수 있지만, Strategy Tester(전략 테스터)는 요청 ToDate(종료일)를 2026.05.28 또는 2026.05.30으로 밀어도 실제 test end(테스트 종료)를 2026.05.27 00:00에 고정했다.

Effect(효과): run337Z(337Z 실행)의 125분 tester gap(테스터 공백)은 ONNX(온엑스) 추론이나 threshold(임계값) 문제가 아니라 Strategy Tester current-day visibility(전략 테스터 현재일 가시성) 문제로 좁혀진다.
