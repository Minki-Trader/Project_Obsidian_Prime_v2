# run364AJ session/side PF lift density repair scout(364AJ 세션/방향 PF 상승 밀도 수리 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AI_materialize_session_side_pf_lift_density_repair_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_session_side_pf_lift_density_repair_ranked_mt5_probe_required_no_authority`
- scout_rows(정찰 행): `12`
- strict_pass_rows(엄격 통과 행): `0`
- selected_variant_id(선택 변형 ID): `selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `840.055` / `1.2739357721` / `1001` / `3.006006006` / `0.8392157842` / `-142.323` / `5.9024542765`
- selected long/short/balance(선택 롱/숏/균형): `882` / `119` / `0.1349206349`
- runtime_authority(런타임 권위): `not_claimed`

## Top Proxy Rows(상위 프록시 행)

| queue_id | axis_id | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | candidate_status | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| selected_control_full_session(선택 대조 전체 세션) | control(대조) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119 | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 850.82288605 |
| validation_pf_repair_selected_split_guard(선택 후보 검증 PF 수리 분할 가드) | split_guardrail(분할 가드레일) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119 | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 850.82288605 |
| month_positive_pocket_observation_only(월 양수 포켓 관찰 전용) | market_behavior_observation(시장 현상 관찰) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119 | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 850.82288605 |
| oos_locked_replay_control(표본외 잠금 재생 대조) | split_guardrail(분할 가드레일) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119 | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 850.82288605 |
| block_premarket_short_only(프리마켓 숏만 차단) | session_side_pf_lift(세션 방향 PF 상승) | 805.222 | 1.2676271111 | 2.9399399399 | -133.361 | 98 | fail_density_floor(밀도 하한 실패) | 730.37677141 |
| selected_short0455_density_edge_recheck(선택 숏 0.455 밀도 경계 재검토) | near_density_bridge(밀도 경계 연결) | 789.589 | 1.2670836468 | 2.9039039039 | -133.361 | 86 | fail_density_floor(밀도 하한 실패) | 661.62158886 |
| core_plus_premarket_long(핵심 세션 + 프리마켓 롱) | session_side_pf_lift(세션 방향 PF 상승) | 721.643 | 1.2395846959 | 2.9339339339 | -133.361 | 98 | fail_density_floor(밀도 하한 실패) | 624.36815541 |
| pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원) | pf_pass_density_bridge(PF 통과 밀도 연결) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6 | fail_density_floor(밀도 하한 실패) | 433.607842402 |
| core_plus_late_long(핵심 세션 + 후반 롱) | session_density_restore(세션 밀도 복원) | 725.57 | 1.2757971879 | 2.7147147147 | -103.533 | 99 | fail_density_floor(밀도 하한 실패) | 359.678347586 |
| pfpass_core_plus_premarket_long_restore(PF 통과 핵심 + 프리마켓 롱 복원) | pf_pass_density_bridge(PF 통과 밀도 연결) | 761.975 | 1.2958707973 | 2.6576576577 | -120.303 | 6 | fail_density_floor(밀도 하한 실패) | 303.163327494 |

## Baseline Comparison(기준 비교)

| metric_id | reference_value | selected_value | delta_selected_minus_reference |
| --- | --- | --- | --- |
| combined_net_profit | 840.055 | 840.055 | 0.0 |
| combined_profit_factor | 1.2739357721 | 1.2739357721 | 0.0 |
| combined_trade_count | 1001 | 1001 | 0.0 |
| combined_trade_per_business_day | 3.006006006 | 3.006006006 | 0.0 |
| combined_expectancy | 0.8392157842 | 0.8392157842 | 0.0 |
| combined_max_drawdown | -142.323 | -142.323 | 0.0 |
| combined_recovery_factor | 5.9024542765 | 5.9024542765 | 0.0 |
| combined_long_count | 882 | 882 | 0.0 |
| combined_short_count | 119 | 119 | 0.0 |
| combined_long_short_balance | 0.1349206349 | 0.1349206349 | 0.0 |

## Gate Audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/final_decision.json | run364AJ proxy scout(364AJ 프록시 정찰)를 닫음 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/input_manifest.csv | run364AI 대기열과 기준 산출물을 확인함 |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/data_integrity_receipt.json | 시점 안전 세션/방향 규칙과 분할 경계를 기록함 |
| queue_replay_gate(대기열 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/session_side_pf_lift_density_repair_proxy_scout_surface.csv | 12개 대기열 행을 재생함 |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/queue_replay_audit.csv | top_n 재생 없음 |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/session_side_pf_lift_density_repair_proxy_scout_surface.csv | 거래 쪼개기 없음 |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/session_side_pf_lift_density_repair_proxy_scout_surface.csv | net/PF/expectancy/DD/RF/trades/side/density를 기록함 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/performance_attribution_receipt.json | 세션/방향 정책 기여를 연결함 |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/result_judgment_receipt.json | MT5 필요 경계로 판정함 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/artifact_lineage_receipt.json | 입력/출력 해시를 연결함 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/claim_boundary_receipt.json | 런타임 권위를 주장하지 않음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AJ/required_gate_coverage_audit.csv | 필수 게이트를 종료 기록에 연결함 |

## Claim Boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 scout(정찰)는 timestamp-safe proxy(시점 안전 프록시) 후보 선별이며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다.
