# run364BZ bx03 December late-session guard inputs(364BZ BX3 12월 후반 세션 가드 입력)

## Result(결과)

- status(상태): `completed_stage364BZ_bx03_guard_inputs_materialized_open_ca_no_authority`
- judgment(판정): `materialized_december_h22_calendar_semantics_and_h17_overlay_guard_inputs_no_authority`
- decision(결정): `stage364BZ_open_run364CA_bx03_guard_stack_runtime_probe`
- next(다음): `run364CA_execute_bx03_guard_stack_runtime_probe_without_db_v1`
- gate(게이트): `6/6`

## Action(행동)

Action(행동): BY attribution(BY 귀속)에서 나온 December h22 long loss block(12월 22시 롱 손실 차단), h17 overlay loss guard(17시 오버레이 손실 가드), equity DD cluster(평가손익 낙폭 클러스터)를 CA runtime probe(CA 런타임 탐침) 후보 입력으로 materialize(구체화)했다.

Effect(효과): calendar block end_hour(달력 차단 종료 시각)이 exclusive(배타)라는 runtime semantics(런타임 의미)를 명시하고, h17 threshold floors(17시 임계값 하한)는 proxy negative(프록시 부정)라 초기 MT5 grid(MT5 격자) 우선순위에서 낮췄다.

## Runtime Queue(런타임 대기열)

| candidate_id | runtime_priority | variant_role | synthetic_enabled | calendar_start_hour | calendar_end_hour | covered_hours |
| --- | --- | --- | --- | --- | --- | --- |
| ca01_bx03_semantics_control | 1 | control(대조) | True | 21 | 23 | 21\|22 |
| ca02_december_h22_only_long_block_isolation | 2 | calendar_isolation(달력 분리) | True | 22 | 23 | 22 |
| ca03_december_h21_h23_long_block_stress | 3 | calendar_stress(달력 압박) | True | 21 | 24 | 21\|22\|23 |
| ca06_native_short_same_calendar_control | 4 | source_control(원천 대조) | False | 21 | 23 | 21\|22 |

## Proxy Impact(프록시 영향)

| candidate_id | proxy_estimable | removed_trade_count | removed_net | estimated_net | estimated_density | density_floor_status |
| --- | --- | --- | --- | --- | --- | --- |
| ca01_bx03_semantics_control | yes | 0 | 0.0 | 1008.18 | 3.2101910828 | passed_proxy |
| ca02_december_h22_only_long_block_isolation | no |  |  |  |  | requires_mt5 |
| ca03_december_h21_h23_long_block_stress | yes | 0 | 0.0 | 1008.18 | 3.2101910828 | passed_proxy |
| ca04_h17_overlay_margin_q10_floor_negative_control | yes | 4 | 2.35 | 1005.83 | 3.1974522293 | passed_proxy |
| ca05_h17_overlay_pshort_q10_floor_negative_control | yes | 4 | 26.72 | 981.46 | 3.1974522293 | passed_proxy |
| ca06_native_short_same_calendar_control | no |  |  |  |  | requires_mt5 |

## H17 Scan(17시 스캔)

| scan_id | runtime_param | threshold | kept_trade_count | kept_net | removed_net | proxy_effect |
| --- | --- | --- | --- | --- | --- | --- |
| p_edge_short_vs_long_ge_q10 | InpSyntheticShortSourceMarginVsLongMin | 0.0805669784 | 35 | 66.84 | 2.35 | negative_or_weak(부정 또는 약함) |
| p_long_le_q80 | not_directly_runtime_supported | 0.3721641958 | 31 | 45.07 | 24.12 | negative_or_weak(부정 또는 약함) |
| p_short_ge_q10 | InpSyntheticShortSourcePShortMin | 0.4448249698 | 35 | 42.47 | 26.72 | negative_or_weak(부정 또는 약함) |
| p_flat_le_q80 | not_directly_runtime_supported | 0.1974754721 | 31 | 34.8 | 34.39 | negative_or_weak(부정 또는 약함) |
| p_short_ge_q40 | InpSyntheticShortSourcePShortMin | 0.453248465 | 23 | 30.75 | 38.44 | negative_or_weak(부정 또는 약함) |
| p_short_ge_q20 | InpSyntheticShortSourcePShortMin | 0.4483761609 | 31 | 29.89 | 39.3 | negative_or_weak(부정 또는 약함) |

## Equity Cluster Proxy(평가손익 클러스터 프록시)

| cluster_rank | close_time | source_bucket | net_profit | closed_balance_drawdown | proxy_boundary |
| --- | --- | --- | --- | --- | --- |
| 1 | 2025-04-07 19:50:00 | long_threshold | -1.01 | 67.67 | closed_trade_balance_proxy_not_tick_equity_path(종료 거래 잔고 프록시이며 틱 평가손익 경로 아님) |
| 2 | 2025-04-07 19:15:00 | long_threshold | -23.95 | 66.66 | closed_trade_balance_proxy_not_tick_equity_path(종료 거래 잔고 프록시이며 틱 평가손익 경로 아님) |
| 3 | 2026-01-16 19:15:00 | long_threshold | -2.76 | 65.49 | closed_trade_balance_proxy_not_tick_equity_path(종료 거래 잔고 프록시이며 틱 평가손익 경로 아님) |
| 4 | 2026-01-20 17:10:00 | long_threshold | -3.14 | 64.59 | closed_trade_balance_proxy_not_tick_equity_path(종료 거래 잔고 프록시이며 틱 평가손익 경로 아님) |
| 5 | 2025-12-11 18:35:00 | long_threshold | -5.71 | 64.51 | closed_trade_balance_proxy_not_tick_equity_path(종료 거래 잔고 프록시이며 틱 평가손익 경로 아님) |
| 6 | 2026-01-16 17:15:00 | long_threshold | -10.16 | 62.73 | closed_trade_balance_proxy_not_tick_equity_path(종료 거래 잔고 프록시이며 틱 평가손익 경로 아님) |

## Gates(게이트)

| gate | status | evidence |
| --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BZ/guard_candidate_matrix.csv |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BZ/guard_candidate_proxy_impact.csv |
| skill_receipt_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BZ/experiment_design_receipt.json |
| timestamp_safety_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BZ/guard_candidate_matrix.csv |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BZ/required_gate_coverage_audit.csv |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BZ/claim_boundary_receipt.json |

## Boundary(경계)

runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다. BZ는 materialization only(구체화 전용)이며 새 MT5 execution(MT5 실행)은 하지 않았다.
