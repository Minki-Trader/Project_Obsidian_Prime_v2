# run364BB density restore stress-to-candidate proxy scout(364BB 밀도 복원 압박-후보 프록시 스카우트)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_density_restore_stress_candidates_ranked_review_required_no_authority`
- scout_rows(스카우트 행): `4`
- strict_proxy_pass_rows(엄격 프록시 통과 행): `3`
- package_eligible_rows(패키지 검토 가능 행): `3`
- skipped_implementation_required_rows(구현 필요 건너뜀 행): `2`
- selected_net/PF/proxy_trades/estimated_MT5_density/DD(선택 순수익/수익 팩터/프록시 거래수/추정 MT5 밀도/낙폭): `919.75` / `1.3178004168` / `1112` / `3.045045045` / `-127.733`
- runtime_authority(런타임 권위): `not_claimed`

## Surface(표면)

| queue_rank | queue_id | bb_candidate_status | package_eligible_proxy | combined_net_profit | combined_profit_factor | combined_trade_count | estimated_mt5_trade_per_business_day | combined_max_drawdown | combined_short_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | ba02_between_ax03_ax08_floor025_ps450 | package_reviewable_proxy_candidate(패키지 검토 가능 프록시 후보) | True | 919.75 | 1.3178004168 | 1112 | 3.045045045 | -127.733 | 103 | 1023.7260238879 |
| 1 | ba01_ax03_stress_to_candidate_floor050_ps450 | package_reviewable_proxy_candidate(패키지 검토 가능 프록시 후보) | True | 874.129 | 1.3019773488 | 1100 | 3.012012012 | -132.758 | 103 | 942.0901288074 |
| 3 | ba03_short_balance_ps448_floor050 | package_reviewable_proxy_candidate(패키지 검토 가능 프록시 후보) | True | 857.741 | 1.2947886727 | 1108 | 3.033033033 | -144.033 | 111 | 932.5384195455 |
| 4 | ba04_candidate_floor075_density_rescue_ps450 | fail_estimated_mt5_density_floor(추정 MT5 밀도 하한 실패) | False | 869.182 | 1.3051213139 | 1089 | 2.981981982 | -129.758 | 103 | 789.5590247816 |

## AW Comparison(AW 비교)

| metric_id | reference_value | selected_value | delta_selected_minus_reference |
| --- | --- | --- | --- |
| net_profit | 878.55 | 919.75 | 41.2 |
| profit_factor | 1.36 | 1.3178004168 | -0.0421995832 |
| proxy_trade_count | 971.0 | 1112 | 141.0 |
| estimated_mt5_density | 2.9159159159 | 3.045045045 | 0.1291291291 |
| expectancy | 0.9 | 0.8271133094 | -0.0728866906 |
| drawdown | 17.51 | -127.733 | -145.243 |
| recovery_factor | 6.75 | 7.2005668073 | 0.4505668073 |
| long_count | 887.0 | 1009 | 122.0 |
| short_count | 84.0 | 103 | 19.0 |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/density_restore_stress_to_candidate_proxy_scout_surface.csv | BB queue(BB 대기열)의 실행 가능 후보를 proxy replay(프록시 재생)로 평가했다. |
| parent_materialization_gate(부모 물질화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/final_decision.json | BA materialization(BA 물질화)이 BB run_id(BB 실행 ID)를 열었는지 확인했다. |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/baseline_comparison.csv | net/PF/density/DD/side KPI(순수익/수익 팩터/밀도/낙폭/방향 지표)를 같은 표면에 기록했다. |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/queue_replay_audit.csv | top_n(상위 N개) 선택 없이 사전 queue(대기열)를 그대로 재생했다. |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/queue_replay_audit.csv | 거래 쪼개기 없이 신호 발생 자체만 평가했다. |
| oos_threshold_lock_gate(OOS 임계값 잠금 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/run364BB_scout_queue.csv | OOS threshold selection(OOS 임계값 선택)을 금지한 queue(대기열)를 사용했다. |
| timestamp_boundary_gate(시점 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BA/run364BB_scout_queue.csv | entry-time closed-bar(진입 시점 닫힌 봉) 경계를 유지했다. |
| implementation_required_visibility_gate(구현 필요 가시화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/queue_replay_audit.csv | 새 runtime policy(런타임 정책)가 필요한 2개 행을 숨기지 않고 skipped(건너뜀)로 기록했다. |
| skill_receipt_lint(스킬 영수증 점검) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/experiment_design_receipt.json | experiment/data/model/lineage/judgment receipt(실험/데이터/모델/계보/판정 영수증)를 썼다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/required_gate_coverage_audit.csv | work packet(작업 묶음)의 required gates(필수 게이트)를 closeout(종료 기록)에 연결했다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BB/claim_boundary_receipt.json | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않았다. |

## Claim Boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): BB candidate(BB 후보)를 proxy scout(프록시 스카우트)로 좁게 평가했지만 MT5 runtime probe(MT5 런타임 탐침)가 아니므로 operating promotion(운영 승격)은 주장하지 않는다.
