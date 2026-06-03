# run364AY density restore cost/session proxy scout(364AY 밀도 복원 비용/세션 프록시 스카우트)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AY_train_threshold_edge_density_restore_cost_session_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_density_restore_candidates_ranked_review_required_no_authority`
- scout_rows(스카우트 행): `6`
- strict_proxy_pass_rows(엄격 프록시 통과 행): `2`
- package_eligible_rows(패키지 검토 가능 행): `0`
- skipped_implementation_required_rows(구현 필요 건너뜀 행): `2`
- selected_net/PF/proxy_trades/estimated_MT5_density/DD(선택 순수익/수익 팩터/프록시 거래수/추정 MT5 밀도/낙폭): `858.662` / `1.2724135667` / `1168` / `3.1981981982` / `-168.999`
- runtime_authority(런타임 권위): `not_claimed`

## Surface(표면)

| queue_rank | queue_id | candidate_status | package_eligible_proxy | combined_net_profit | combined_profit_factor | combined_trade_count | estimated_mt5_trade_per_business_day | combined_max_drawdown | combined_short_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 | ax08_density_overstress_floor000 | watch_stress_pass_not_package(압박 통과 관찰, 패키지 아님) | False | 858.662 | 1.2724135667 | 1168 | 3.1981981982 | -168.999 | 127 | 968.584099039 |
| 3 | ax03_short_restore_ps450_floor050_stress | watch_stress_pass_not_package(압박 통과 관찰, 패키지 아님) | False | 874.129 | 1.3019773488 | 1100 | 3.012012012 | -132.758 | 103 | 906.8353805266 |
| 1 | ax01_density_buffer_floor075_controlled_expand | fail_estimated_mt5_density_floor(추정 MT5 밀도 하한 실패) | False | 869.181 | 1.3114889692 | 1073 | 2.9369369369 | -121.708 | 87 | 826.1695566043 |
| 2 | ax02_short_restore_ps452_floor075 | fail_estimated_mt5_density_floor(추정 MT5 밀도 하한 실패) | False | 833.793 | 1.2938301494 | 1083 | 2.963963964 | -143.158 | 97 | 807.4050512168 |
| 5 | ax05_sep_dec_stress_label_no_delete | watch_diagnostic_pass_not_package(진단 통과 관찰, 패키지 아님) | False | 850.315 | 1.2910832467 | 1105 | 3.024024024 | -150.182 | 118 | 761.1293752432 |
| 7 | ax07_floor001_parent_control | fail_estimated_mt5_density_floor(추정 MT5 밀도 하한 실패) | False | 862.283 | 1.3105654109 | 1065 | 2.9159159159 | -133.571 | 87 | 672.2660889091 |

## AW Comparison(AW 비교)

| metric_id | reference_value | selected_value | delta_selected_minus_reference |
| --- | --- | --- | --- |
| net_profit | 878.55 | 858.662 | -19.888 |
| profit_factor | 1.36 | 1.2724135667 | -0.0875864333 |
| proxy_trade_count | 971.0 | 1168 | 197.0 |
| estimated_mt5_density | 2.9159159159 | 3.1981981982 | 0.2822822823 |
| expectancy | 0.9 | 0.7351558219 | -0.1648441781 |
| drawdown | 17.51 | -168.999 | -186.509 |
| recovery_factor | 6.75 | 5.080870301 | -1.669129699 |
| long_count | 887.0 | 1041 | 154.0 |
| short_count | 84.0 | 127 | 43.0 |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| parent_materialization_gate(부모 물질화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/final_decision.json | AX 물질화 완료와 다음 실행 ID를 확인한다. |
| queue_replay_gate(대기열 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/density_restore_cost_session_proxy_scout_surface.csv | 실행 가능 AY 행을 proxy replay(프록시 재생)로 실행한다. |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/baseline_comparison.csv | net/PF/density/DD/side KPI(순수익/수익 팩터/밀도/낙폭/방향 지표)를 같은 표면에 둔다. |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/queue_replay_audit.csv | top_n(상위 N개) 선택을 쓰지 않는다. |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/queue_replay_audit.csv | 거래 쪼개기 없이 신호 발생 자체를 늘린다. |
| oos_threshold_lock_gate(표본외 임계값 잠금 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/run364AY_scout_queue.csv | 표본외 임계값 선택 금지를 유지한다. |
| timestamp_boundary_gate(시점 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AX/run364AY_scout_queue.csv | 닫힌 봉 기준 진입 의미를 유지한다. |
| implementation_required_visibility_gate(구현 필요 가시화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/queue_replay_audit.csv | proxy(프록시)로 표현 못 한 행 2개를 숨기지 않고 기록한다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/required_gate_coverage_audit.csv | work packet(작업 묶음)의 필수 게이트를 closeout(종료 기록)에 연결한다. |
| final_claim_guard(최종 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AY/claim_boundary_receipt.json | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않는다. |

## Claim Boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): AY는 density restore(밀도 복원) 후보를 proxy scout(프록시 스카우트)로 선별했지만, MT5 runtime probe(MT5 런타임 탐침)가 아니므로 operating promotion(운영 승격)을 주장하지 않는다.
