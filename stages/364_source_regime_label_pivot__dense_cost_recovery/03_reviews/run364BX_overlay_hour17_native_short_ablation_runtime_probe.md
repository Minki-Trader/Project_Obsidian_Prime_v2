# run364BX overlay hour17 native short ablation runtime probe(364BX 17시 오버레이 기본 숏 제거 비교 런타임 탐침)

## Result(결과)

Action(행동): BW queue(BW 대기열)의 3개 variant(변형)를 같은 ONNX(온엑스) model(모델), 같은 base thresholds(기본 임계값), 같은 MT5 Strategy Tester(MT5 전략 테스터) identity(정체성)로 실행했다.

Effect(효과): synthetic overlay(합성 오버레이), native short control(기본 숏 대조), late-session entry firewall(후반 세션 진입 방화벽)의 차이를 MT5 KPI(MT5 핵심 성과 지표)로 비교할 수 있다.

- status(상태): `completed_stage364BX_overlay_ablation_mt5_probe_executed_review_required_no_authority`
- judgment(판정): `runtime_ablation_completed_best_bx03_hour17_overlay_plus_weak_late_session_firewall_review_required_no_authority`
- best variant(최선 변형): `bx03_hour17_overlay_plus_weak_late_session_firewall`
- best MT5 net/PF/trades(최선 MT5 순수익/수익 팩터/거래수): `1008.18` / `1.4` / `1008`
- best density(최선 밀도): `3.2101910828`
- BV reference(BV 기준): `966.32` / `1.38` / `1018`

## Ablation Scoreboard(제거 비교 점수표)

| variant_id | net_profit | profit_factor | trade_count | trade_density_per_feature_business_day | recovery_factor | equity_drawdown_amount | long_trade_count | short_trade_count | net_diff_vs_bv | selection_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bx03_hour17_overlay_plus_weak_late_session_firewall | 1008.18 | 1.4 | 1008 | 3.2101910828 | 7.75 | 130.11 | 903 | 105 | 41.86 | passed_density_floor |
| bx01_overlay_hour17_only_keep_native_short | 987.02 | 1.39 | 1008 | 3.2101910828 | 7.59 | 130.11 | 904 | 104 | 20.7 | passed_density_floor |
| bx02_native_short_only_overlay_disabled | 945.93 | 1.37 | 1002 | 3.1910828025 | 7.27 | 130.11 | 904 | 98 | -20.39 | passed_density_floor |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| runtime_evidence_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BX/runtime_evidence_gate.json | telemetry/report(런타임 기록/보고서)가 variant(변형)별로 존재한다. |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BX/runtime_ablation_scoreboard.csv | BW queue(BW 대기열)의 제거 비교를 모두 기록한다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BX/runtime_ablation_scoreboard.csv | MT5 KPI(MT5 핵심 성과 지표)를 tester report(테스터 보고서)에서 읽는다. |
| metaeditor_compile_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BX/mt5_compile_result.json | EA(전문가 자문)가 compile(컴파일)된다. |
| portable_sync_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BX/portable_ea_sync.json | Strategy Tester(전략 테스터)가 같은 EX5를 사용한다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BX/required_gate_coverage_audit.csv | required gates(필수 게이트)를 closeout(종료 기록)에 연결한다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BX/claim_boundary_receipt.json | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않는다. |

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
