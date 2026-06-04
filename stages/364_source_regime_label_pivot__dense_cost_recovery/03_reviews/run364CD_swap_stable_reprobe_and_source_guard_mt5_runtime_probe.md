# run364CD swap-stable source guard MT5 runtime probe(364CD 스왑 안정 원천 가드 MT5 런타임 탐침)

## Result(결과)

Action(행동): CC queue(CC 대기열)의 ready candidates(준비 후보) 3개를 같은 ONNX(온엑스), feature order(피처 순서), MT5 Strategy Tester(MT5 전략 테스터) 조건으로 실행했다.

Effect(효과): BX3 clone(BX3 복제), CA01 clone(CA01 복제), native short same-calendar control(기본 숏 동일 달력 대조)을 같은 CD 실행 묶음에서 비교할 수 있게 했다.

- status(상태): `completed_stage364CD_swap_stable_source_guard_mt5_probe_executed_review_required_no_authority`
- judgment(판정): `runtime_probe_completed_best_cd01_bx3_clone_current_session_same_session_review_required_no_authority`
- best variant(최선 변형): `cd01_bx3_clone_current_session`
- best MT5 net/PF/trades(최선 MT5 순수익/수익 팩터/거래수): `997.49` / `1.4` / `1008`
- best density/recovery/equity DD(최선 밀도/회복 계수/수익곡선 낙폭): `3.2101910828` / `7.67` / `130.11`
- CD02 minus CD01 net(CD02-CD01 순수익): `0.0`
- CD02 minus CD03 net(CD02-CD03 순수익): `41.09`

## Scoreboard(점수판)

| variant_id | source_variant_id | net_profit | profit_factor | trade_count | trade_density_per_feature_business_day | recovery_factor | equity_drawdown_amount | net_diff_vs_expected_anchor | selection_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cd01_bx3_clone_current_session | bx03_hour17_overlay_plus_weak_late_session_firewall | 997.49 | 1.4 | 1008 | 3.2101910828 | 7.67 | 130.11 | -10.69 | passed_density_floor |
| cd02_ca01_clone_current_session | ca01_bx03_semantics_control | 997.49 | 1.4 | 1008 | 3.2101910828 | 7.67 | 130.11 | 0.0 | passed_density_floor |
| cd03_native_short_same_calendar_current_session | ca06_native_short_same_calendar_control | 956.4 | 1.38 | 1002 | 3.1910828025 | 7.35 | 130.11 | 0.0 | passed_density_floor |

## Pair Metric Screen(쌍 지표 1차 화면)

| pair_id | left_candidate_id | right_candidate_id | net_delta_left_minus_right | trade_count_delta_left_minus_right | report_metric_screen |
| --- | --- | --- | --- | --- | --- |
| cd01_vs_cd02_swap_stability_control | cd02_ca01_clone_current_session | cd01_bx3_clone_current_session | 0.0 | 0.0 | passes_report_metric_swap_stability_screen_review_required |
| cd02_vs_cd03_source_overlay_value | cd02_ca01_clone_current_session | cd03_native_short_same_calendar_current_session | 41.09 | 6.0 | passes_report_metric_overlay_lift_screen_review_required |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| runtime_evidence_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/runtime_evidence_gate.json | telemetry/report(런타임 기록/보고서)이 CD 후보별로 존재한다. |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/runtime_probe_scoreboard.csv | CD 기본 ready 후보만 좁게 실행 범위로 닫았다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/runtime_probe_scoreboard.csv | MT5 report(MT5 보고서)에서 net/PF/trades/drawdown KPI를 읽었다. |
| same_session_batch_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/same_session_pair_metric_summary.csv | BX3/CA01/source control을 같은 CD 실행 묶음에서 비교할 수 있다. |
| metaeditor_compile_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/mt5_compile_result.json | EA(전문가 자문)를 compile(컴파일)했다. |
| portable_sync_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/portable_ea_sync.json | Strategy Tester(전략 테스터)가 같은 EX5를 사용하게 했다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/required_gate_coverage_audit.csv | required gates(필수 게이트)를 closeout(종료 기록)에 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CD/claim_boundary_receipt.json | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않는다. |

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. report-level metric(보고서 지표) 화면은 deal-level trade path(딜 레벨 거래 경로), gross/net/swap(총손익/순수익/스왑) 리뷰를 대체하지 않는다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
