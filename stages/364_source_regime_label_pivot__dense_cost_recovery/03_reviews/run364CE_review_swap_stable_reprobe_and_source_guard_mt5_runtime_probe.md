# run364CE review swap-stable source guard MT5 runtime probe(364CE 스왑 안정 원천 가드 MT5 런타임 탐침 리뷰)

## Result(결과)

Action(행동): CD MT5 report(CD MT5 보고서)와 telemetry(원격 기록)를 딜 단위로 결합해 swap/gross/net/source(스왑/총손익/순수익/원천)를 리뷰했다.

Effect(효과): 이전 BX3 1008.18 net(순수익)은 current-session authority(현재 세션 권위)가 아니라 stale swap-table memory(낡은 스왑표 기억)로 낮추고, h17 overlay(17시 오버레이)는 다음 offensive seed(공격 씨앗)로 보존한다.

- status(상태): `completed_stage364CE_cd_runtime_probe_reviewed_swap_stability_closed_overlay_value_confirmed_open_cf_no_authority`
- judgment(판정): `runtime_probe_review_usable_with_boundary_same_session_swap_stability_passed_h17_overlay_value_confirmed_no_authority`
- reviewed best semantics(리뷰된 최선 의미): `cd02_ca01_clone_current_session`
- MT5 net/PF/trades/density(MT5 순수익/수익 팩터/거래수/밀도): `997.49` / `1.4` / `1008` / `3.2101910828`
- CD02-CD01 net/gross/swap(CD02-CD01 순수익/총손익/스왑): `0.0` / `0.0` / `0.0`
- CD02-CD03 net lift(CD02-CD03 순수익 우위): `41.09`

## Pair Deltas(쌍 차이)

| pair_id | common_count | left_only_count | right_only_count | net_delta_left_minus_right | gross_delta_common_left_minus_right | swap_delta_common_left_minus_right | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cd01_vs_cd02_swap_stability_control | 1008 | 0 | 0 | 0.0 | 0.0 | 0.0 | same_session_trade_path_and_cost_identical(동일 세션 거래 경로와 비용이 완전 동일) |
| cd02_vs_cd03_source_overlay_value | 995 | 13 | 7 | 41.09 | 0.0 | 0.0 | h17_synthetic_overlay_value_confirmed_vs_native_short_control(17시 합성 오버레이 가치가 기본 숏 대조 대비 확인됨) |

## Source Attribution(원천 귀속)

| variant_id | source_bucket | trade_count | net_profit | gross_profit | swap | expectancy |
| --- | --- | --- | --- | --- | --- | --- |
| cd01_bx3_clone_current_session | long_threshold | 903 | 871.13 | 874.67 | -3.54 | 0.964707 |
| cd01_bx3_clone_current_session | native_short_threshold | 66 | 57.17 | 58.77 | -1.6 | 0.866212 |
| cd01_bx3_clone_current_session | synthetic_short_overlay | 39 | 69.19 | 69.19 | 0.0 | 1.774103 |
| cd02_ca01_clone_current_session | long_threshold | 903 | 871.13 | 874.67 | -3.54 | 0.964707 |
| cd02_ca01_clone_current_session | native_short_threshold | 66 | 57.17 | 58.77 | -1.6 | 0.866212 |
| cd02_ca01_clone_current_session | synthetic_short_overlay | 39 | 69.19 | 69.19 | 0.0 | 1.774103 |
| cd03_native_short_same_calendar_current_session | long_threshold | 903 | 871.13 | 874.67 | -3.54 | 0.964707 |
| cd03_native_short_same_calendar_current_session | native_short_threshold | 99 | 85.27 | 86.87 | -1.6 | 0.861313 |

## Next Queue(다음 대기열)

| queue_id | priority | action | reason |
| --- | --- | --- | --- |
| cf01_preserve_current_session_ca01_semantics | 1 | materialize cost-stable CA01/BX3 semantics(비용 안정 CA01/BX3 의미 구체화) | CD02 and CD01 share 1008 trades with zero gross/swap/net delta(CD02와 CD01이 1008개 거래에서 총손익/스왑/순수익 차이 0) |
| cf02_preserve_h17_synthetic_overlay_value | 2 | materialize h17 overlay source guard seed(17시 오버레이 원천 가드 씨앗 구체화) | CD02 beats native short control by 41.09 net(CD02가 기본 숏 대조보다 순수익 41.09 우위) |
| cf03_gross_net_cost_layered_selection | 3 | materialize gross/net/swap layered score(총손익/순수익/스왑 층화 점수 구체화) | same-session swap delta is zero, prior cross-session swap delta was -10.69(동일 세션 스왑 차이는 0이고 이전 교차 세션 스왑 차이는 -10.69) |
| cf04_trade_shape_without_count_splitting | 4 | materialize trade-shape quality constraints(거래 형태 품질 제약 구체화) | CD02 keeps 1008 trades and density 3.21; source buckets remain auditable(CD02는 1008거래와 밀도 3.21을 유지하고 원천 버킷도 감사 가능) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/kpi_contract_audit.csv | KPI(핵심 성과 지표)를 deal table(딜 테이블)과 대조했다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/row_grain_audit.csv | closed trade(종료 거래) 행 단위를 고정했다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/source_authority_audit.csv | MT5 report(보고서)와 telemetry(기록)의 권위를 분리했다. |
| runtime_parity_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/runtime_parity_audit.csv | CD 런타임 의미와 비용 차이를 분리했다. |
| backtest_forensics_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/backtest_forensics_audit.csv | 테스터 정체성과 비용표 리뷰를 기록했다. |
| performance_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/performance_attribution_receipt.json | 수익 변화의 원인을 source/session/cost(원천/세션/비용)로 나눴다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CE/claim_boundary_receipt.json | 운영 승격과 런타임 권위를 주장하지 않는다. |

## Boundary(경계)

review only(리뷰 전용)이다. new model training(새 모델 학습), new MT5 execution(새 MT5 실행), forward pass(전진 검증), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
