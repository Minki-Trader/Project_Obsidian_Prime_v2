# run364AP hold6 PF/DD repair scout(364AP 6봉 PF/DD 수리 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AP_train_hold6_pf_dd_repair_offensive_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364AQ_review_hold6_pf_dd_repair_offensive_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_hold6_pf_dd_repair_ranked_mt5_probe_required_no_authority`
- scout_rows(정찰 행): `7`
- skipped_new_policy_rows(새 정책 건너뜀 행): `1`
- strict_pass_rows(엄격 통과 행): `0`
- selected_net/PF/density/DD(선택 순수익/PF/밀도/낙폭): `858.662` / `1.2724135667` / `3.5075075075` / `-168.999`
- runtime_authority(런타임 권위): `not_claimed`

## Surface(표면)

| queue_rank | queue_id | candidate_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | hold6_density_anchor_control(6봉 밀도 기준 대조) | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 858.662 | 1.2724135667 | 3.5075075075 | -168.999 | 127 | 872.480818355 |
| 3 | threshold_edge_hold6_density_repair(임계값 경계 6봉 밀도 수리) | watch_pf_lift_below_target(PF 상승이나 목표 미달 관찰) | 840.779 | 1.2804442925 | 3.3843843844 | -147.924 | 87 | 868.515101413 |
| 4 | late_long_hold6_pf_patch(후반 롱 6봉 PF 패치) | watch_pf_lift_below_target(PF 상승이나 목표 미달 관찰) | 785.813 | 1.2871701599 | 3.1531531532 | -157.864 | 7 | 792.887227487 |
| 5 | soft_margin_floor_0_003(소프트 마진 하한 0.003) | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 706.218 | 1.2520021924 | 3.0690690691 | -147.473 | 127 | 722.91392506 |
| 2 | sparse_pf_pass_anchor_control(희소 PF 통과 대조) | fail_density_floor(밀도 하한 실패) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6 | 430.97301648 |
| 8 | pf_pass_density_bridge_no_split_guard(PF 통과 밀도 연결 무분할 가드) | fail_density_floor(밀도 하한 실패) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6 | 430.97301648 |
| 6 | soft_margin_floor_0_006(소프트 마진 하한 0.006) | fail_density_floor(밀도 하한 실패) | 438.326 | 1.1668598594 | 2.7417417417 | -156.985 | 128 | 5.40802116 |

## Hold6 Comparison(6봉 비교)

| metric_id | reference_value | selected_value | delta_selected_minus_reference |
| --- | --- | --- | --- |
| combined_net_profit | 858.662 | 858.662 | 0.0 |
| combined_profit_factor | 1.2724135667 | 1.2724135667 | 0.0 |
| combined_trade_count |  | 1168 | 1168.0 |
| combined_trade_per_business_day | 3.5075075075 | 3.5075075075 | 0.0 |
| combined_expectancy |  | 0.7351558219 | 0.7351558219 |
| combined_max_drawdown | -168.999 | -168.999 | 0.0 |
| combined_recovery_factor |  | 5.080870301 | 5.080870301 |
| combined_long_count |  | 1041 | 1041.0 |
| combined_short_count |  | 127 | 127.0 |
| combined_long_short_balance |  | 0.1219980788 | 0.1219980788 |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/final_decision.json | run364AP proxy scout(364AP 프록시 정찰)를 닫음 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/input_manifest.csv | run364AO 대기열과 부모 산출물을 확인함 |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/data_integrity_receipt.json | 시점 안전 프록시 재생 경계를 기록함 |
| queue_replay_gate(대기열 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/hold6_pf_dd_repair_proxy_scout_surface.csv | 실행 가능 queue(대기열) 행을 재생함 |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/queue_replay_audit.csv | top_n 사용 없음 |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/queue_replay_audit.csv | 거래 쪼개기 없음 |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/hold6_pf_dd_repair_proxy_scout_surface.csv | net/PF/expectancy/DD/RF/trades/side/density 기록 |
| model_boundary_audit(모델 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/model_boundary_receipt.json | 새 모델 학습 없음과 threshold(임계값) 경계를 기록 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/performance_attribution_receipt.json | 수리 축별 성과 귀속을 연결 |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/result_judgment_receipt.json | MT5 필요 경계로 판정 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/artifact_lineage_receipt.json | 입력/출력 hash(해시) 연결 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/claim_boundary_receipt.json | 런타임 권위 주장 없음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AP/required_gate_coverage_audit.csv | 필수 gate(게이트)를 종료 기록에 연결 |

## Claim Boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): run364AP(364AP 실행)는 proxy scout(프록시 정찰)이며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.
