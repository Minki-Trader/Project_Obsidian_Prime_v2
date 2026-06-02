# Stage364Y density side-balance MT5 review(Stage364Y 밀도 방향 균형 MT5 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `run364Y_review_density_side_balance_repair_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364Z_materialize_density_side_balance_cost_session_stress_without_db_v1`
- judgment(판정): `positive_runtime_probe_density_recovered_side_balance_added_profit_high_pf_moderate_drawdown_stress_required_no_authority`
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## KPI read(KPI 판독)

- MT5 net/PF/expectancy(순수익/수익 팩터/기대값): `989.22` / `1.3` / `0.92`
- DD/RF(낙폭/회복 계수): `221.01` / `4.48`
- trades/density(거래수/밀도): `1081` / `3.2462462462`
- long/short(롱/숏): `952` / `129`
- delta vs run364T(364T 대비 차이): net `60.33`, PF `-0.04`, trades `146`, shorts `129`

## KPI delta(KPI 차이)

| metric_id | baseline_value | current_value | delta_current_minus_baseline | improvement_status |
| --- | --- | --- | --- | --- |
| net_profit | 928.89 | 989.22 | 60.33 | improved |
| profit_factor | 1.34 | 1.3 | -0.04 | not_improved |
| trade_count | 935.0 | 1081.0 | 146.0 | improved |
| expectancy | 0.99 | 0.92 | -0.07 | not_improved |
| recovery_factor | 4.59 | 4.48 | -0.11 | not_improved |
| max_drawdown_amount | 202.3 | 221.01 | 18.71 | not_improved |
| max_drawdown_percent | 33.3 | 34.65 | 1.35 | not_improved |
| long_trade_count | 935.0 | 952.0 | 17.0 | not_improved |
| short_trade_count | 0.0 | 129.0 | 129.0 | improved |

## Density and side(밀도와 방향)

| audit_id | value | threshold | status | effect(효과) |
| --- | --- | --- | --- | --- |
| combined_trade_density(합산 거래 밀도) | 3.2462462462 | 3.0 | passed | user trade-per-day floor(사용자 일별 거래수 기준)을 거래 쪼개기 없이 확인한다. |
| long_short_presence(롱숏 존재) | 952/129 | short_count > 0 | passed | long-only failure(롱 전용 실패)가 줄었는지 확인한다. |
| proxy_trade_count_parity(프록시 거래수 동등성) | 1081/1081 | equal | passed | proxy(프록시) 거래 형태와 MT5(메타트레이더5) 실행 거래 형태가 같은지 확인한다. |

## Cost and drawdown(비용과 낙폭)

| review_id | commission | swap | max_drawdown_amount | max_drawdown_percent | worst_trade | worst_month | worst_month_net | worst_entry_hour | worst_entry_hour_net | effect(효과) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tester_cost(테스터 비용) | 0.0 | -43.39 |  |  |  |  |  |  |  | broker-native cost(브로커 네이티브 비용)가 결과에 들어갔는지 기록한다. |
| drawdown_pressure(낙폭 압박) |  |  | 221.01 | 34.65 | -40.91 |  |  |  |  | high recovery factor(높은 회복 계수)와 높은 percent DD(퍼센트 낙폭)를 함께 본다. |
| worst_month_hour(최악 월/시간) |  |  |  |  |  | 2025-03 | -68.65 | 16 | -112.31 | session/regime stress(세션/국면 압박) 다음 작업의 seed(씨앗)를 만든다. |

## Findings(소견)

| finding_id | severity | finding | effect(효과) |
| --- | --- | --- | --- |
| F01_profit_trade_count_improved | positive_clue | MT5 net/trades improved versus run364T: 989.22/1081 vs 928.89/935. | density repair(밀도 수리)가 실제 MT5 거래수 증가로 이어졌음을 보존한다. |
| F02_side_balance_added | positive_clue | short side exists: long/short 952/129; run364T short count was 0. | long-only failure(롱 전용 실패)를 완화한 공격 탐색 단서다. |
| F03_runtime_parity_clean | positive_clue | probability/decision parity(확률/판정 동등성) matched all ready rows with zero mismatch. | runtime evidence(런타임 근거)를 review(검토)에 사용할 수 있게 한다. |
| R01_pf_lower_than_run364T | stress_required | PF is 1.30, below run364T 1.34, despite higher net and density. | cost/drawdown stress(비용/낙폭 압박)를 다음 작업으로 남긴다. |
| R02_drawdown_percent_high | stress_required | max DD percent is 34.65%, still high for a deposit 500 runtime probe(예치금 500 런타임 탐침). | operating promotion(운영 승격)을 막고 recovery/drawdown(회복/낙폭) 압박 시험을 요구한다. |
| R03_tail_trade_loss | stress_required | worst trade after cost is -40.91; tail risk(꼬리 위험) remains visible. | session/regime(세션/국면)과 hold-shape(보유 형태) 수리를 다음 seed(씨앗)로 둔다. |
| B01_no_authority_yet | claim_boundary | density 3.2462462462/day and MT5 KPI are positive, but forward/runtime authority(전진/런타임 권위) is not proven. | Goal Achieve(목표 달성), live readiness(실거래 준비), operating promotion(운영 승격)을 닫지 않는다. |

## Gates(게이트)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| kpi_evidence_gate(KPI 근거 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/kpi_delta_vs_run364T.csv | MT5 KPI(MT5 핵심 성과 지표)를 baseline(기준)과 비교한다. |
| backtest_forensics_gate(백테스트 포렌식 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/closed_trade_attribution.csv | closed trade evidence(종료 거래 근거)를 파싱해 비용/낙폭을 확인한다. |
| runtime_parity_gate(런타임 동등성 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/runtime_quality_review.csv | probability parity(확률 동등성)와 report source(보고서 출처)를 고정한다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/monthly_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/entry_hour_attribution.csv; stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/side_attribution.csv | 월별/시간별/방향별 수익 구조를 분해한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/claim_boundary_receipt.json | positive runtime probe(긍정 런타임 탐침)를 운영 권위로 승격하지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Y/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)

run364Y는 positive runtime candidate(긍정 런타임 후보)로 기록하지만, cost/session stress(비용/세션 압박), forward evidence(전진 근거), operating promotion(운영 승격)은 아직 닫지 않는다.
