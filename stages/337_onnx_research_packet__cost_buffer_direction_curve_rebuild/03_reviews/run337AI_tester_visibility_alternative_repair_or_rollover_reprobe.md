# Stage337AI Tester Visibility Alternative Repair Or Rollover Reprobe(337AI 테스터 가시성 대체 수리 또는 이월 재탐침)

- run_id(실행 ID): `run337AI_tester_visibility_alternative_repair_or_rollover_reprobe_v1`
- parent_run_id(상위 실행 ID): `run337AH_execute_full_current_day_visibility_repair_and_no_overfit_preflight_v1`
- status(상태): `completed_stage337AI_all_tester_model_alternatives_gap_remain_no_forward_decision`
- judgment(판정): `all_tester_model_modes_gap_remain_current_day_boundary_not_resolved`
- decision(결정): `stage337AI_open_run337AJ_history_cache_repair_or_rollover_wait_reprobe_no_selection`
- next_action(다음 행동): `run337AJ_data_history_cache_repair_or_next_rollover_wait_reprobe_v1`
- Forward Passed(전방 통과): `not_claimed`
- Forward Failed(전방 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

이번 실행은 같은 frozen ONNX(고정 ONNX), feature order(피처 순서), D/B decision surface(D/B 결정 표면), threshold(임계값), risk/lot(위험/로트), ATR SL/TP(ATR 손절/익절)을 유지했다.
바꾼 것은 MT5 Strategy Tester Model(전략 테스터 모델) 값뿐이다. 효과(effect, 효과)는 full current-day(현재일 전체) 가시성 공백이 real tick history/cache(실제 틱 이력/캐시) 때문인지 좁히는 것이다.

## Model Mode Matrix(모델 방식 행렬)

| attempt(시도) | model(모델) | label(라벨) | gap(공백) | last observed(마지막 관측) | feature last(피처 끝) | proxy(프록시) | read(판독) |
|---|---:|---|---|---|---|---:|---|
| `u42_plain_rf_ai_model4_real_ticks_control` | `4` | `real_ticks` | `tester_feature_last_gap_remains` | `2026-05-26T23:55:00Z` | `2026-05-27T02:00:00Z` | `5/5` | `real_tick_visibility_gap_remains` |
| `u42_plain_rf_ai_model0_every_tick_generated` | `0` | `generated_every_tick` | `tester_feature_last_gap_remains` | `2026-05-26T23:55:00Z` | `2026-05-27T02:00:00Z` | `5/5` | `alternative_model_gap_remains` |
| `u42_plain_rf_ai_model1_m1_ohlc` | `1` | `m1_ohlc` | `tester_feature_last_gap_remains` | `2026-05-26T23:55:00Z` | `2026-05-27T02:00:00Z` | `5/5` | `alternative_model_gap_remains` |
| `u42_plain_rf_ai_model2_open_prices` | `2` | `open_prices` | `tester_feature_last_gap_remains` | `2026-05-26T23:55:00Z` | `2026-05-27T02:00:00Z` | `5/5` | `alternative_model_gap_remains` |

## KPI Snapshot(KPI 스냅샷)

KPI(핵심 지표)는 진단 참고값이며, generated model mode(생성 모델 방식) 결과는 forward authority(전방 권위)가 아니다.

| attempt(시도) | model(모델) | net(순익) | PF(수익 팩터) | trades(거래) | DD(손실폭) |
|---|---:|---:|---:|---:|---:|
| `u42_plain_rf_ai_model4_real_ticks_control` | `4` | `99.9` | `1.13` | `344` | `112.86` |
| `u42_plain_rf_ai_model0_every_tick_generated` | `0` | `101.1` | `1.14` | `344` | `115.11` |
| `u42_plain_rf_ai_model1_m1_ohlc` | `1` | `101.1` | `1.14` | `344` | `115.11` |
| `u42_plain_rf_ai_model2_open_prices` | `2` | `101.1` | `1.14` | `344` | `115.11` |

## Boundary(경계)

- selected_candidate(선택 후보): `none`
- model_training(모델 학습): `forbidden_not_performed`
- threshold_retuning(임계값 재조정): `forbidden_not_performed`
- lot_optimization(로트 최적화): `forbidden_not_performed`
- live_readiness(실거래 준비): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`

Effect(효과): 이 보고서는 다음 수리/판정 경로를 고르는 근거이며, Forward Passed/Failed(전방 통과/실패)를 닫지 않는다.
