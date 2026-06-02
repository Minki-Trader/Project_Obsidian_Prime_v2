# Stage364AA PF/DD guardrail proxy scout(Stage364AA PF/DD 가드레일 프록시 탐색)

## Current truth(현재 진실)

- run_id(실행 ID): `run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364Z_materialize_density_side_balance_cost_session_stress_without_db_v1`
- next_run_id(다음 실행 ID): `run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_pf_dd_stress_candidates_ranked_mt5_probe_required_no_authority`
- scout_rows(탐색 행): `16`
- strict_pass_rows(엄격 통과 행): `0`
- selected_variant_id(선택 변형 ID): `maxhold6_density_control__ps0_45__adx40_0__hold6__none`
- selected net/PF/trades/density/DD(선택 순수익/수익 팩터/거래수/밀도/낙폭): `771.423` / `1.2175571938` / `1264` / `3.7957957958` / `-168.999`
- runtime_authority(런타임 권위): `not_claimed`

## Top proxy rows(상위 프록시 행)

| queue_id | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | candidate_status | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| maxhold6_density_control | 771.423 | 1.2175571938 | 3.7957957958 | -168.999 | 139 | watch_pf_not_above_target(PF 목표 미만 관찰) | 894.718495496 |
| stress_zone_3 | 840.192 | 1.2758061959 | 2.984984985 | -142.323 | 112 | fail_density_floor(밀도 하한 실패) | 882.4253864 |
| adx38_density_counterfactual | 798.689 | 1.2345298327 | 3.1741741742 | -142.197 | 130 | watch_pf_not_above_target(PF 목표 미만 관찰) | 855.167196504 |
| stress_zone_4 | 808.044 | 1.2584924377 | 3.042042042 | -142.323 | 131 | watch_pf_not_above_target(PF 목표 미만 관찰) | 854.79399189 |
| hour16_maxhold6_guardrail | 741.781 | 1.2152110968 | 3.7117117117 | -183.033 | 112 | watch_pf_not_above_target(PF 목표 미만 관찰) | 849.586405404 |
| baseline_replay_control | 771.564 | 1.2218406503 | 3.2462462462 | -155.007 | 129 | watch_pf_not_above_target(PF 목표 미만 관찰) | 826.913549544 |
| short050_hour16_soft_guardrail | 794.636 | 1.2706352591 | 2.8738738739 | -172.391 | 6 | fail_density_floor(밀도 하한 실패) | 808.0346522 |
| hour16_soft_guardrail | 744.707 | 1.2194362013 | 3.1741741742 | -192.655 | 106 | watch_pf_not_above_target(PF 목표 미만 관찰) | 786.807900904 |
| stress_zone_2 | 744.707 | 1.2194362013 | 3.1741741742 | -192.655 | 106 | watch_pf_not_above_target(PF 목표 미만 관찰) | 786.807900904 |
| short055_quality_probe | 752.15 | 1.2573454567 | 2.8558558559 | -172.391 | 0 | fail_density_floor(밀도 하한 실패) | 761.0262016 |

## Baseline comparison(기준 비교)

| metric_id | baseline_value | selected_value | delta_selected_minus_baseline |
| --- | --- | --- | --- |
| combined_net_profit | 771.564 | 771.423 | -0.141 |
| combined_profit_factor | 1.2218406503 | 1.2175571938 | -0.0042834565 |
| combined_trade_count | 1081 | 1264 | 183.0 |
| combined_trade_per_business_day | 3.2462462462 | 3.7957957958 | 0.5495495496 |
| combined_max_drawdown | -155.007 | -168.999 | -13.992 |
| combined_recovery_factor | 4.9776074629 | 4.5646601459 | -0.412947317 |
| combined_short_count | 129 | 139 | 10.0 |

## Gate audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/final_decision.json | run364AA scope(범위)를 proxy scout(프록시 탐색)로 닫는다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/data_integrity_receipt.json | 시점 안전 가드레일을 기록한다. |
| experiment_design_audit(실험 설계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/experiment_design_receipt.json | 가설/비교/중단 조건을 기록한다. |
| proxy_replay_gate(프록시 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/cost_session_guardrail_proxy_scout_surface.csv | queue(대기열)를 순서 재생했다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/performance_attribution_receipt.json | 기준 대비 KPI 차이를 남긴다. |
| model_boundary_gate(모델 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/model_boundary_receipt.json | 새 모델 학습과 ONNX 승격을 주장하지 않는다. |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/result_judgment_receipt.json | proxy scout(프록시 탐색) 경계로 판정한다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/artifact_lineage_receipt.json | 입력/출력 해시를 연결한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/claim_boundary_receipt.json | runtime authority(런타임 권위)를 닫지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AA/required_gate_coverage_audit.csv | required gate(필수 게이트)를 closeout(종료 기록)에 연결한다. |

## Claim boundary(주장 경계)

`research_development_proxy_scout_only_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 scout(탐색)는 package(패키지) 또는 repair(수리) 결정을 위한 proxy evidence(프록시 근거)다. MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.
