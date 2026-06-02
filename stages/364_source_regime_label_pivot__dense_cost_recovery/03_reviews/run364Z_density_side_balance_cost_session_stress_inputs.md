# Stage364Z cost/session stress inputs(Stage364Z 비용/세션 압박 입력)

## Current truth(현재 진실)

- run_id(실행 ID): `run364Z_materialize_density_side_balance_cost_session_stress_without_db_v1`
- parent_run_id(부모 실행 ID): `run364Y_review_density_side_balance_repair_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1`
- judgment(판정): `stress_inputs_ready_pf_drawdown_session_repair_scout_no_operating_claim`
- source_trade_rows(원천 거래 행): `1081`
- parent MT5 net/PF/trades(부모 MT5 순수익/수익 팩터/거래수): `989.22` / `1.3` / `1081`
- density(밀도): `3.2462462462`
- runtime_authority(런타임 권위): `not_claimed`

## Stress candidates(압박 후보)

| candidate_rank | group_columns | group_value | trade_count | net_profit_after_cost | profit_factor_after_cost | stress_reasons | candidate_use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | entry_hour | entry_hour=16 | 177 | -112.31 | 0.845687748 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수);tail_loss(꼬리 손실) | session_filter_or_soft_size_probe(세션 필터 또는 소프트 사이징 탐침) |
| 2 | entry_hour+side | entry_hour=16\|side=short | 32 | -81.47 | 0.563981804 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수) | session_filter_or_soft_size_probe(세션 필터 또는 소프트 사이징 탐침) |
| 3 | entry_month | entry_month=2025-03 | 87 | -88.94 | 0.801561803 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수);tail_loss(꼬리 손실) | diagnostic_guardrail_probe(진단 가드레일 탐침) |
| 4 | entry_month+side | entry_month=2025-03\|side=long | 70 | -57.99 | 0.848467428 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수);tail_loss(꼬리 손실) | side_quality_guardrail_probe(방향 품질 가드레일 탐침) |
| 5 | entry_month+entry_hour | entry_month=2026-03\|entry_hour=18 | 23 | -36.47 | 0.567532314 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수) | session_filter_or_soft_size_probe(세션 필터 또는 소프트 사이징 탐침) |
| 6 | entry_month+entry_hour | entry_month=2025-04\|entry_hour=17 | 20 | -34.8 | 0.626368907 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수) | session_filter_or_soft_size_probe(세션 필터 또는 소프트 사이징 탐침) |
| 7 | entry_month+entry_hour | entry_month=2025-12\|entry_hour=17 | 21 | -32.77 | 0.586237374 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수) | session_filter_or_soft_size_probe(세션 필터 또는 소프트 사이징 탐침) |
| 8 | entry_month+entry_hour | entry_month=2025-03\|entry_hour=17 | 22 | -29.16 | 0.6758199 | negative_net(순손익 음수);pf_below_1_0(PF 1.0 미만);negative_expectancy(기대값 음수) | session_filter_or_soft_size_probe(세션 필터 또는 소프트 사이징 탐침) |

## Simple filter proxy(단순 필터 프록시)

| candidate_rank | filter_expression | removed_trade_count | projected_net_if_removed | projected_trade_per_business_day_if_removed | density_floor_status |
| --- | --- | --- | --- | --- | --- |
| 1 | entry_hour=16 | 177 | 1101.53 | 2.7147147147 | fail_density_floor(밀도 하한 실패) |
| 2 | entry_hour=16\|side=short | 32 | 1070.69 | 3.1501501501 | pass(통과) |
| 3 | entry_month=2025-03 | 87 | 1078.16 | 2.9849849849 | fail_density_floor(밀도 하한 실패) |
| 4 | entry_month=2025-03\|side=long | 70 | 1047.21 | 3.036036036 | pass(통과) |
| 5 | entry_month=2026-03\|entry_hour=18 | 23 | 1025.69 | 3.1771771771 | pass(통과) |
| 6 | entry_month=2025-04\|entry_hour=17 | 20 | 1024.02 | 3.1861861861 | pass(통과) |
| 7 | entry_month=2025-12\|entry_hour=17 | 21 | 1021.99 | 3.1831831831 | pass(통과) |
| 8 | entry_month=2025-03\|entry_hour=17 | 22 | 1018.38 | 3.1801801801 | pass(통과) |

## Parameter queue(파라미터 대기열)

| queue_rank | queue_id | short_threshold | adx_block_min | max_hold_m5 | guardrail_expression | queue_type |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | baseline_replay_control | 0.45 | 40.0 | 8 | none(없음) | control(대조) |
| 2 | maxhold6_density_control | 0.45 | 40.0 | 6 | none(없음) | repair_probe(수리 탐침) |
| 3 | adx42_pf_control | 0.45 | 42.0 | 8 | none(없음) | repair_probe(수리 탐침) |
| 4 | adx38_density_counterfactual | 0.45 | 38.0 | 8 | none(없음) | counterfactual(대조 반사실) |
| 5 | short050_quality_probe | 0.5 | 40.0 | 8 | short_only_threshold(숏 전용 임계값) | repair_probe(수리 탐침) |
| 6 | short055_quality_probe | 0.55 | 40.0 | 8 | short_only_threshold(숏 전용 임계값) | stress_probe(압박 탐침) |
| 7 | hour16_soft_guardrail | 0.45 | 40.0 | 8 | soft_guard_entry_hour_16(16시 소프트 가드) | session_probe(세션 탐침) |
| 8 | hour16_maxhold6_guardrail | 0.45 | 40.0 | 6 | soft_guard_entry_hour_16(16시 소프트 가드) | session_probe(세션 탐침) |

## Gate audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/final_decision.json | run364Z scope(범위)를 input materialization(입력 구체화)로 닫는다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/data_integrity_receipt.json | entry-known/control boundary(진입 시점/대조 경계)를 기록한다. |
| experiment_design_audit(실험 설계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/experiment_design_receipt.json | hypothesis/comparison/stop condition(가설/비교/중단 조건)을 남긴다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/performance_attribution_receipt.json | 세션/방향/계좌상태 구간을 분해한다. |
| model_boundary_gate(모델 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/model_boundary_receipt.json | model training(모델 학습)과 selection(선택)을 주장하지 않는다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/artifact_lineage_receipt.json | source/output hash(원천/출력 해시)를 연결한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/claim_boundary_receipt.json | runtime authority(런타임 권위)를 닫지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Z/required_gate_coverage_audit.csv | required gate(필수 게이트)를 closeout(종료 기록)에 연결한다. |

## Claim boundary(주장 경계)

`research_development_input_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 report(보고서)는 다음 `run364AA` scout(탐색)의 입력을 만든다. MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.
