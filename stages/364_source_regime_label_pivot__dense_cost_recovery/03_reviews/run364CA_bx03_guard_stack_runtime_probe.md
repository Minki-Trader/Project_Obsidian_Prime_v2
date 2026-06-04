# run364CA bx03 guard stack runtime probe(364CA BX3 가드 묶음 런타임 탐침)

## Result(결과)

Action(행동): BZ queue(BZ 대기열)의 ready candidates(준비 후보) 4개를 같은 ONNX(온엑스), 같은 feature order(피처 순서), 같은 MT5 Strategy Tester(MT5 전략 테스터) 조건으로 실행했다.

Effect(효과): h22-only isolation(h22 단독 분리), h21-h23 stress(h21-h23 압박), native-short same-calendar control(같은 달력 기본 숏 대조)이 BX3/BV 대비 실제 수익 구조를 바꾸는지 MT5 KPI(MT5 핵심 성과 지표)로 확인했다.

- status(상태): `completed_stage364CA_bx03_guard_stack_mt5_probe_executed_review_required_no_authority`
- judgment(판정): `runtime_probe_completed_best_ca01_bx03_semantics_control_review_required_no_authority`
- best variant(최선 변형): `ca01_bx03_semantics_control`
- best MT5 net/PF/trades(최선 MT5 순수익/수익 팩터/거래수): `997.49` / `1.4` / `1008`
- best density/recovery/equity DD(최선 밀도/회복/평가손익 낙폭): `3.2101910828` / `7.67` / `130.11`
- diff vs BX3/BV(BX3/BV 대비 차이): `-10.69` / `31.17`

## Scoreboard(점수표)

| variant_id | net_profit | profit_factor | trade_count | trade_density_per_feature_business_day | recovery_factor | equity_drawdown_amount | long_trade_count | short_trade_count | net_diff_vs_bx3 | net_diff_vs_bv | selection_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ca01_bx03_semantics_control | 997.49 | 1.4 | 1008 | 3.2101910828 | 7.67 | 130.11 | 903 | 105 | -10.69 | 31.17 | passed_density_floor |
| ca03_december_h21_h23_long_block_stress | 997.49 | 1.4 | 1008 | 3.2101910828 | 7.67 | 130.11 | 903 | 105 | -10.69 | 31.17 | passed_density_floor |
| ca02_december_h22_only_long_block_isolation | 989.62 | 1.39 | 1012 | 3.2229299363 | 7.61 | 130.11 | 907 | 105 | -18.56 | 23.3 | passed_density_floor |
| ca06_native_short_same_calendar_control | 956.4 | 1.38 | 1002 | 3.1910828025 | 7.35 | 130.11 | 903 | 99 | -51.78 | -9.92 | passed_density_floor |

## Gates(게이트)

| gate | status | evidence |
| --- | --- | --- |
| runtime_evidence_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CA/runtime_evidence_gate.json |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CA/runtime_probe_scoreboard.csv |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CA/runtime_probe_scoreboard.csv |
| metaeditor_compile_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CA/mt5_compile_result.json |
| portable_sync_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CA/portable_ea_sync.json |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CA/required_gate_coverage_audit.csv |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CA/claim_boundary_receipt.json |

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
