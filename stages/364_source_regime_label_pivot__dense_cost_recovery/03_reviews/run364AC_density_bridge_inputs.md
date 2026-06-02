# run364AC density bridge inputs(364AC 밀도 연결 입력)

## Current truth(현재 진실)

- run_id(실행 ID): `run364AC_materialize_pf_dd_near_miss_density_bridge_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AD_train_pf_dd_near_miss_density_bridge_scout_without_db_v1`
- judgment(판정): `density_bridge_scout_inputs_ready_no_operating_claim`
- near_miss_profile_rows(근접 실패 프로필 행): `2`
- density_bridge_rows(밀도 연결 행): `7`
- run364AD_queue_rows(364AD 대기열 행): `10`
- stress_zone_3_density_trade_gap(3번 압박 구간 밀도 부족 거래수): `5.0`
- runtime_authority(런타임 권위): `not_claimed`

## Near miss profile(근접 실패 프로필)

| queue_id | combined_profit_factor | combined_trade_per_business_day | density_trade_gap | pf_gap_to_target | materialization_read(구체화 판독) |
| --- | --- | --- | --- | --- | --- |
| stress_zone_3 | 1.2758061959 | 2.984984985 | 5.0 | 0.0241938041 | density_bridge_needed(밀도 연결 필요) |
| stress_zone_4 | 1.2584924377 | 3.042042042 | 0.0 | 0.0415075623 | pf_lift_needed(PF 상승 필요) |

## Bridge queue(연결 대기열)

| queue_id | seed_queue_id | bridge_expression | expected_effect(기대 효과) |
| --- | --- | --- | --- |
| stress3_restore_march_short_top5 | stress_zone_3 | entry_month=2025-03 restore side=short top_n=5 by p_short | adds about five trades to cross density floor while preserving March long block(약 5개 거래를 복원해 밀도 하한을 넘기고 3월 롱 차단은 보존) |
| stress3_restore_march_non_hour16_top8 | stress_zone_3 | entry_month=2025-03 restore non_hour16 top_n=8 by absolute_margin | tests whether hour16 risk was the March damage source(16시 위험이 3월 손상 원천인지 시험) |
| stress3_restore_march_adx45_long_top8 | stress_zone_3 | entry_month=2025-03 restore side=long adx_14>=45 top_n=8 by p_long | tries quality-gated long restoration instead of full March removal(전체 3월 제거 대신 품질 제한 롱 복원 시험) |
| stress4_short0475_pf_lift | stress_zone_4 | entry_month=2025-03 block side=long; short_threshold=0.475 | keeps density-pass March-long block and lifts short quality(밀도 통과 3월 롱 차단을 유지하고 숏 품질을 올림) |
| stress4_short050_pf_lift | stress_zone_4 | entry_month=2025-03 block side=long; short_threshold=0.50 | stronger short quality lift with density stress tracked(더 강한 숏 품질 상승과 밀도 압박 추적) |
| adx38_stress3_month_block | adx38_density_counterfactual | adx_block_min=38; entry_month=2025-03 block all | combines ADX38 density recovery with full March damage cut(ADX38 밀도 회복과 3월 손상 차단 결합) |
| adx38_stress4_month_long_block | adx38_density_counterfactual | adx_block_min=38; entry_month=2025-03 block side=long | keeps more density than full March block while cutting bad March longs(전체 3월 차단보다 밀도를 보존하며 나쁜 3월 롱을 자름) |

## Scout queue(정찰 대기열)

| queue_rank | queue_id | queue_type | bridge_expression |
| --- | --- | --- | --- |
| 1 | baseline_replay_control | control(대조) | none |
| 2 | stress_zone_3_control | control(대조) | entry_month=2025-03 block all |
| 3 | stress_zone_4_control | control(대조) | entry_month=2025-03 block side=long |
| 4 | stress3_restore_march_short_top5 | bridge_scout(연결 정찰) | entry_month=2025-03 restore side=short top_n=5 by p_short |
| 5 | stress3_restore_march_non_hour16_top8 | bridge_scout(연결 정찰) | entry_month=2025-03 restore non_hour16 top_n=8 by absolute_margin |
| 6 | stress3_restore_march_adx45_long_top8 | bridge_scout(연결 정찰) | entry_month=2025-03 restore side=long adx_14>=45 top_n=8 by p_long |
| 7 | stress4_short0475_pf_lift | bridge_scout(연결 정찰) | entry_month=2025-03 block side=long; short_threshold=0.475 |
| 8 | stress4_short050_pf_lift | bridge_scout(연결 정찰) | entry_month=2025-03 block side=long; short_threshold=0.50 |
| 9 | adx38_stress3_month_block | bridge_scout(연결 정찰) | adx_block_min=38; entry_month=2025-03 block all |
| 10 | adx38_stress4_month_long_block | bridge_scout(연결 정찰) | adx_block_min=38; entry_month=2025-03 block side=long |

## Gate audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/final_decision.json | run364AC materialization(364AC 구체화)을 닫는다. |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/input_manifest.csv | run364AB 검토 산출물을 확인한다. |
| near_miss_profile_gate(근접 실패 프로필 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/near_miss_profile.csv | stress_zone_3/4 gap(압박 구간 3/4 부족분)을 계산한다. |
| queue_materialization_gate(대기열 구체화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/run364AD_scout_queue.csv | run364AD scout queue(364AD 정찰 대기열)를 만든다. |
| experiment_boundary_gate(실험 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/experiment_design_receipt.json | 거래 쪼개기 금지를 기록한다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/artifact_lineage_receipt.json | 입력/출력 hash(해시)를 연결한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/claim_boundary_receipt.json | runtime authority(런타임 권위)를 주장하지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AC/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Claim boundary(주장 경계)

`research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 materialization(구체화)은 다음 scout(정찰) 입력만 만들며, MT5 runtime authority(MT5 런타임 권위)나 operating promotion(운영 승격)을 주장하지 않는다.
