# run364AF PF lift density-safe inputs(364AF PF 상승 밀도 안전 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AF_materialize_pf_lift_density_safe_expansion_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AE_review_pf_dd_near_miss_density_bridge_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AG_train_pf_lift_density_safe_expansion_scout_without_db_v1`
- judgment(판정): `pf_lift_density_safe_expansion_inputs_ready_no_operating_claim`
- profile_rows(프로필 행): `4`
- density_restore_rule_rows(밀도 복원 규칙 행): `5`
- threshold_grid_rows(임계값 격자 행): `21`
- run364AG_queue_rows(364AG 대기열 행): `12`
- runtime_authority(런타임 권위): `not_claimed`

## Profile(프로필)

| profile_id | source_variant_id | source_profit_factor | source_density_per_day | diagnosis(진단) | next_use(다음 활용) |
| --- | --- | --- | --- | --- | --- |
| run364AD_selected_density_safe_anchor | stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8 | 1.2739357721 | 3.006006006 | density passed but PF below target(밀도 통과, PF 목표 미달) | raise short quality while preserving density bridge(숏 품질을 올리되 밀도 연결 보존) |
| candidate_stress3_restore_non_hour16_margin_0_1 | stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8 | 1.2739357721 | 3.006006006 | pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전) | lift PF without breaking density(밀도를 깨지 않고 PF 상승) |
| candidate_stress3_restore_march_short_p0_475 | stress3_restore_march_short_p0_475__ps0_45__adx40_0__hold8 | 1.2721814278 | 3.0 | pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전) | lift PF without breaking density(밀도를 깨지 않고 PF 상승) |
| candidate_stress4_short050_pf_lift | stress4_short050_pf_lift__ps0_5__adx40_0__hold8 | 1.3066323163 | 2.6726726727 | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | restore density without losing PF(PF를 잃지 않고 밀도 복원) |

## Restore Rules(복원 규칙)

| rule_id | restore_policy | effect(효과) |
| --- | --- | --- |
| restore_non_hour16_margin_008 | entry_month=2025-03 restore non_hour16 abs_margin>=0.08 | restore slightly more density while keeping hour16 blocked(16시 차단을 유지하면서 밀도를 조금 더 복원) |
| restore_non_hour16_margin_010 | entry_month=2025-03 restore non_hour16 abs_margin>=0.10 | replay selected run364AD density bridge(선택된 364AD 밀도 연결 재생) |
| restore_short_p0475 | entry_month=2025-03 restore side=short p_short>=0.475 | restore density through short quality(숏 품질로 밀도 복원) |
| restore_short_p0490 | entry_month=2025-03 restore side=short p_short>=0.490 | test stricter short restore for PF defense(PF 방어용 더 엄격한 숏 복원 시험) |
| restore_long_p041_adx35 | entry_month=2025-03 restore side=long p_long>=0.41 adx_14>=35 | test limited long restore without broad March long exposure(넓은 3월 롱 노출 없이 제한 롱 복원 시험) |

## Scout Queue(정찰 대기열)

| queue_rank | queue_id | axis_id | short_probability_threshold | bridge_policy | bridge_policy_value | expected_effect(효과) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | selected_density_safe_control | control(대조) | 0.45 | restore_march_non_hour16_margin | 0.10 | replay run364AD selected density-safe candidate(364AD 선택 밀도 안전 후보 재생) |
| 2 | pf_pass_density_fail_control | control(대조) | 0.5 | block_march_long |  | replay PF-pass density-fail control(PF 통과 밀도 실패 대조 재생) |
| 3 | selected_short0455_restore_margin010 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 0.455 | restore_march_non_hour16_margin | 0.10 | small PF lift while keeping selected density bridge(선택 밀도 연결을 유지하며 작은 PF 상승 시험) |
| 4 | selected_short0460_restore_margin010 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 0.46 | restore_march_non_hour16_margin | 0.10 | raise short threshold and measure density break risk(숏 임계값을 올리고 밀도 붕괴 위험 측정) |
| 5 | selected_short0465_restore_margin008 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 0.465 | restore_march_non_hour16_margin | 0.08 | counter higher short threshold with wider restore(높은 숏 임계값을 더 넓은 복원으로 상쇄) |
| 6 | selected_short0475_restore_short0475 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 0.475 | restore_march_short_p | 0.475 | let short quality carry both PF and density(숏 품질이 PF와 밀도를 함께 담당하는지 시험) |
| 7 | selected_margin_floor002_restore_margin008 | margin_band_pf_lift(마진 구간 PF 상승) | 0.45 | restore_march_non_hour16_margin | 0.08 | remove low-margin noise while preserving density restore(저마진 잡음을 줄이며 밀도 복원 보존) |
| 8 | selected_margin_floor003_restore_margin010 | margin_band_pf_lift(마진 구간 PF 상승) | 0.45 | restore_march_non_hour16_margin | 0.10 | test stricter margin floor against PF gap(더 엄격한 마진 하한으로 PF 부족분 시험) |
| 9 | pfpass_short050_restore_margin008 | pf_pass_density_restore(PF 통과 밀도 복원) | 0.5 | block_march_long_restore_non_hour16_margin | 0.08 | recover density around PF-pass control(PF 통과 대조 주변의 밀도 복원) |
| 10 | pfpass_short049_restore_margin010 | pf_pass_density_restore(PF 통과 밀도 복원) | 0.49 | block_march_long_restore_non_hour16_margin | 0.10 | slightly loosen PF-pass short gate to regain density(PF 통과 숏 문턱을 조금 낮춰 밀도 회복) |
| 11 | pfpass_short050_restore_short0475 | pf_pass_density_restore(PF 통과 밀도 복원) | 0.5 | block_march_long_restore_short_p | 0.475 | restore only high-probability shorts to defend PF(고확률 숏만 복원해 PF 방어) |
| 12 | mixed_long041_adx35_short0475 | mixed_density_restore(혼합 밀도 복원) | 0.475 | restore_march_long_p_adx_and_short_p | p_long=0.41;adx_14=35;p_short=0.475 | test narrow long restore plus short quality(좁은 롱 복원과 숏 품질 결합 시험) |

## Grid Sample(격자 표본)

| grid_id | short_probability_threshold | restore_policy | restore_policy_value |
| --- | --- | --- | --- |
| ps0_45__restore_march_non_hour16_margin__0_08 | 0.45 | restore_march_non_hour16_margin | 0.08 |
| ps0_45__restore_march_non_hour16_margin__0_10 | 0.45 | restore_march_non_hour16_margin | 0.10 |
| ps0_45__restore_march_short_p__0_475 | 0.45 | restore_march_short_p | 0.475 |
| ps0_455__restore_march_non_hour16_margin__0_08 | 0.455 | restore_march_non_hour16_margin | 0.08 |
| ps0_455__restore_march_non_hour16_margin__0_10 | 0.455 | restore_march_non_hour16_margin | 0.10 |
| ps0_455__restore_march_short_p__0_475 | 0.455 | restore_march_short_p | 0.475 |
| ps0_46__restore_march_non_hour16_margin__0_08 | 0.46 | restore_march_non_hour16_margin | 0.08 |
| ps0_46__restore_march_non_hour16_margin__0_10 | 0.46 | restore_march_non_hour16_margin | 0.10 |

## Gate Audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/final_decision.json | run364AF materialization(364AF 구체화)을 닫음 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/input_manifest.csv | run364AE 검토 산출물을 확인함 |
| experiment_design_gate(실험 설계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/experiment_design_receipt.json | 가설/대조/무효 조건을 기록함 |
| queue_materialization_gate(대기열 구체화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/run364AG_scout_queue.csv | run364AG 정찰 대기열을 만듦 |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/run364AG_scout_queue.csv | top_n 재생을 제거함 |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/data_integrity_receipt.json | 시점 안전 고정 임계값 경계를 기록함 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/performance_attribution_receipt.json | PF와 밀도 차이를 다음 검증 항목으로 분리함 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/artifact_lineage_receipt.json | 입력/출력 해시를 연결함 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/claim_boundary_receipt.json | 런타임 권위를 주장하지 않음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AF/required_gate_coverage_audit.csv | 필수 게이트를 종료 기록에 연결함 |

## Claim Boundary(주장 경계)

`research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): materialization(구체화)은 다음 proxy scout(프록시 정찰) 입력만 만들며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.
