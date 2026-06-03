# run364AQ hold6 PF/DD repair review(364AQ 6봉 PF/DD 수리 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AQ_review_hold6_pf_dd_repair_offensive_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AP_train_hold6_pf_dd_repair_offensive_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AR_materialize_threshold_edge_pf_gap_repair_inputs_without_db_v1`
- judgment(판정): `negative_for_package_positive_for_threshold_edge_pf_dd_seed_no_authority`
- package_candidate_rows(패키지 후보 행): `0`
- pf_dd_lift_density_safe_rows(PF/DD 개선, 밀도 안전 행): `2`
- pf_pass_density_fail_rows(PF 통과, 밀도 실패 행): `2`
- runtime_authority(런타임 권위): `not_claimed`

## Reviewed Surface(검토 표면)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count |
| --- | --- | --- | --- | --- | --- | --- |
| late_long_hold6_pf_patch(후반 롱 6봉 PF 패치) | pf_dd_lift_density_safe_seed(PF/DD 개선, 밀도 안전 씨앗) | 785.813 | 1.2871701599 | 3.1531531532 | -157.864 | 7.0 |
| threshold_edge_hold6_density_repair(임계값 경계 6봉 밀도 수리) | pf_dd_lift_density_safe_seed(PF/DD 개선, 밀도 안전 씨앗) | 840.779 | 1.2804442925 | 3.3843843844 | -147.924 | 87.0 |
| soft_margin_floor_0_003(소프트 마진 하한 0.003) | dd_lift_density_safe_seed(DD 개선, 밀도 안전 씨앗) | 706.218 | 1.2520021924 | 3.0690690691 | -147.473 | 127.0 |
| hold6_density_anchor_control(6봉 밀도 기준 대조) | density_safe_pf_fail(밀도 안전, PF 실패) | 858.662 | 1.2724135667 | 3.5075075075 | -168.999 | 127.0 |
| sparse_pf_pass_anchor_control(희소 PF 통과 대조) | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6.0 |
| pf_pass_density_bridge_no_split_guard(PF 통과 밀도 연결 무분할 가드) | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6.0 |
| soft_margin_floor_0_006(소프트 마진 하한 0.006) | reject_or_watch(거절 또는 관찰) | 438.326 | 1.1668598594 | 2.7417417417 | -156.985 | 128.0 |

## Positive Clues(긍정 단서)

| clue_id | evidence | kpi_read | salvage_value |
| --- | --- | --- | --- |
| threshold_edge_pf_dd_lift(임계값 경계 PF/DD 개선) | threshold_edge_hold6_density_repair(임계값 경계 6봉 밀도 수리) | net=840.779; pf=1.2804442925; density=3.3843843844; dd=-147.924 | PF and DD improved while density stayed above 3/day(PF와 DD가 개선되고 밀도 3/day 이상 유지) |
| late_long_pf_lift_density_safe(후반 롱 PF 개선, 밀도 안전) | soft_margin_floor_0_003(소프트 마진 하한 0.003) | net=706.218; pf=1.2520021924; density=3.0690690691; dd=-147.473 | PF lift is stronger but short side thins(PF 개선은 강하지만 숏이 얇아짐) |
| sparse_pf_anchor_density_gap(희소 PF 기준 밀도 간극) | sparse_pf_pass_anchor_control(희소 PF 통과 대조) | net=845.554; pf=1.3287468527; density=2.6636636637; dd=-120.303 | PF>=1.30 exists but density below 3/day(PF 1.30 이상은 있으나 밀도 3/day 미만) |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/final_decision.json | run364AQ review(364AQ 검토)를 완료했다. |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/input_manifest.csv | run364AP 산출물을 확인했다. |
| package_gate_audit(패키지 게이트 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/package_gate_audit.csv | strict package(엄격 패키지)가 없음을 기록했다. |
| failure_memory_gate(실패 기억 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/failure_memory.csv | 실패를 다음 제약으로 전환했다. |
| positive_clue_gate(긍정 단서 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/positive_clues.csv | threshold edge(임계값 경계) 단서를 보존했다. |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/run364AR_materialization_queue.csv | run364AR 대기열을 만들었다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/data_integrity_receipt.json | timestamp-safe(시점 안전) 경계를 기록했다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/performance_attribution_receipt.json | PF/DD 개선과 밀도 실패 원인을 분리했다. |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/result_judgment_receipt.json | 패키지 부정, 씨앗 긍정으로 판정했다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/artifact_lineage_receipt.json | 입력/출력 hash(해시)를 연결했다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/claim_boundary_receipt.json | 운영 승격을 주장하지 않았다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AQ/required_gate_coverage_audit.csv | 필수 gate(게이트)를 종료 기록에 연결했다. |

## Claim Boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): run364AQ(364AQ 실행)는 package(패키지)를 만들지 않고, threshold edge(임계값 경계) 단서를 run364AR(364AR 실행) 입력으로 넘긴다.
