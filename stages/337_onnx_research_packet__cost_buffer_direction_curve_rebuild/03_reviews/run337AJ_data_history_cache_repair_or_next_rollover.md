# Stage337AJ Data History Cache Repair Or Next Rollover(337AJ 데이터 이력 캐시 수리 또는 다음 이월)

- run_id(실행 ID): `run337AJ_data_history_cache_repair_or_next_rollover_wait_reprobe_v1`
- parent_run_id(상위 실행 ID): `run337AI_tester_visibility_alternative_repair_or_rollover_reprobe_v1`
- status(상태): `completed_stage337AJ_history_cache_warmup_gap_remains_no_forward_decision`
- judgment(판정): `api_history_warmup_did_not_move_tester_current_day_boundary_rollover_or_synthetic_parity_repair_next`
- decision(결정): `stage337AJ_open_run337AK_next_rollover_or_synthetic_custom_parity_repair_no_selection`
- next_action(다음 행동): `run337AK_next_rollover_or_synthetic_custom_parity_repair_v1`
- Forward Passed(전방 통과): `not_claimed`
- Forward Failed(전방 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

이번 실행은 MT5 API history warmup(API 이력 예열)으로 US100 current-day(현재일) M1/M5/tick(1분/5분/틱) 구간을 먼저 읽고, 같은 frozen ONNX(고정 ONNX)를 다시 Strategy Tester(전략 테스터)에 넣었다.
Effect(효과): API-visible data(API에서 보이는 데이터)가 tester-visible data(테스터에서 보이는 데이터)로 넘어가는지 직접 본다.

## Warmup(API 예열)

| label(라벨) | type(유형) | rows(행) | last close/time(마지막 시각) |
|---|---|---:|---|
| `feature_tail_20260527_0000_0210` | `M1` | `70` | `2026-05-27T02:11:00Z` |
| `feature_tail_20260527_0000_0210` | `M5` | `15` | `2026-05-27T02:15:00Z` |
| `recent_12h` | `M1` | `659` | `2026-05-27T04:32:00Z` |
| `recent_12h` | `M5` | `132` | `2026-05-27T04:35:00Z` |
| `full_forward_tail_20260526_to_now` | `M1` | `1590` | `2026-05-27T04:32:00Z` |
| `full_forward_tail_20260526_to_now` | `M5` | `319` | `2026-05-27T04:35:00Z` |
| `feature_last_10m_ticks_0155_0205` | `ticks` | `1764` | `2026-05-27T02:04:59Z` |
| `recent_30m_ticks` | `ticks` | `14505` | `2026-05-27T04:31:52Z` |

## Tester Repair Matrix(테스터 수리 행렬)

| attempt(시도) | model(모델) | to feature gap(피처 공백) | last observed(마지막 관측) | feature last(피처 끝) | proxy(프록시) | cache read(캐시 판독) |
|---|---:|---:|---|---|---:|---|
| `u42_plain_rf_aj_api_warm_model4_real_ticks` | `4` | `125.0` | `2026-05-26T23:55:00Z` | `2026-05-27T02:00:00Z` | `5/5` | `api_warmup_did_not_move_tester_boundary` |
| `u42_plain_rf_aj_api_warm_model0_generated` | `0` | `125.0` | `2026-05-26T23:55:00Z` | `2026-05-27T02:00:00Z` | `5/5` | `api_warmup_did_not_move_tester_boundary` |
| `u42_plain_rf_aj_api_warm_model4_wide_todate` | `4` | `125.0` | `2026-05-26T23:55:00Z` | `2026-05-27T02:00:00Z` | `5/5` | `api_warmup_did_not_move_tester_boundary` |

## KPI Snapshot(KPI 스냅샷)

KPI(핵심 지표)는 cache repair diagnostic(캐시 수리 진단) 참고값이며 Forward authority(전방 권위)가 아니다.

| attempt(시도) | model(모델) | net(순익) | PF(수익 팩터) | trades(거래) | DD(손실폭) |
|---|---:|---:|---:|---:|---:|
| `u42_plain_rf_aj_api_warm_model4_real_ticks` | `4` | `99.9` | `1.13` | `344` | `112.86` |
| `u42_plain_rf_aj_api_warm_model0_generated` | `0` | `101.1` | `1.14` | `344` | `115.11` |
| `u42_plain_rf_aj_api_warm_model4_wide_todate` | `4` | `99.9` | `1.13` | `344` | `112.86` |

## Boundary(경계)

- selected_candidate(선택 후보): `none`
- model_training(모델 학습): `forbidden_not_performed`
- threshold_retuning(임계값 재조정): `forbidden_not_performed`
- lot_optimization(로트 최적화): `forbidden_not_performed`
- runtime_authority(런타임 권위): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`

Effect(효과): cache warmup(API 예열) 이후에도 tester boundary(테스터 경계)가 남으면 다음 작업은 rollover(이월) 또는 synthetic custom parity repair(합성 커스텀 동등성 수리)로 넘어간다.
