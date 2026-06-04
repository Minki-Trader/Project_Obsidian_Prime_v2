# run364BV synthetic short source runtime repair(364BV 합성 숏 원천 런타임 수리)

## Result(결과)

Action(행동): BS proxy(BS 프록시)의 synthetic short source(합성 숏 원천)를 EA(`Expert Advisor`, 전문가 자문) input(입력)으로 물질화했다.

Effect(효과): `hour 17|19|20`, `p_short >= 0.4375`, `p_short - p_long >= 0.075`, max hold 6 bars(최대 6봉 보유), December h21 long block(12월 21시 롱 차단)을 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)에서 같은 run(실행)으로 탐침할 수 있게 했다.

- status(상태): `completed_stage364BV_synthetic_short_source_runtime_probe_executed_review_required_no_authority`
- judgment(판정): `runtime_probe_executed_with_mt5_kpi_available_review_required_no_authority`
- selected proxy(선택 프록시): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`
- proxy net/PF/trades(프록시 순수익/수익 팩터/거래수): `1063.14` / `1.4220035161` / `1023`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `966.32` / `1.38` / `1018`
- BK MT5 reference(BK MT5 기준): `959.64` / `1.38` / `1006`

## Proxy MT5 Diff(프록시 MT5 차이)

| comparison_id | proxy_net_profit | mt5_net_profit | net_diff_proxy_minus_mt5 | net_diff_bv_minus_bk | mt5_short_trade_count | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bs_proxy_vs_bv_mt5_runtime_probe | 1063.14 | 966.32 | 96.82 | 6.68 | 114 | usable_runtime_probe_diff |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| runtime_source_support_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/runtime_source_support_audit.csv | 합성 숏 원천 입력이 EA/계약에 존재한다. |
| metaeditor_compile_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/mt5_compile_result.json | EA 변경이 컴파일된다. |
| portable_sync_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/portable_ea_sync.json | Strategy Tester가 같은 EX5를 사용한다. |
| tester_identity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/tester_identity_contract.csv | US100 M5 real tick, deposit 500, leverage 1:100을 고정한다. |
| runtime_execution_attempt_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/mt5_execution_result.json | MT5 실행 시도 또는 스킵 기록을 남긴다. |
| runtime_evidence_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/runtime_output_validation.json | telemetry/summary가 완성된다. |
| strategy_report_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/strategy_tester_report_records.json | MT5 KPI 보고서가 수집된다. |
| proxy_mt5_diff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/proxy_mt5_runtime_difference.csv | proxy expected value와 MT5 KPI 차이를 기록한다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/claim_boundary_receipt.json | runtime authority/operating promotion/goal을 주장하지 않는다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BV/required_gate_coverage_audit.csv | 필수 gate를 종료 기록에 연결한다. |

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
