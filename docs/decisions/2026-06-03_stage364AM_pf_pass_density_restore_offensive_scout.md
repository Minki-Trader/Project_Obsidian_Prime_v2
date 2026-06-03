# run364AM PF-pass density restore offensive scout(364AM PF 통과 밀도 복원 공격 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AM_train_pf_pass_density_restore_offensive_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_pf_pass_density_restore_ranked_mt5_probe_required_no_authority`
- scout_rows(정찰 행): `12`
- strict_pass_rows(엄격 통과 행): `0`
- package_path(패키지 경로): `no_package_proxy_review_required(패키지 없음, 프록시 검토 필요)`
- selected_variant_id(선택 변형 ID): `density_anchor_hold6_pf_probe_밀도_기준_보유6_PF_탐침__seed_selected_control_full_session_선택_대조_전체_세션_ps0_45_floor0_0_hold8__ps0_45__floor0_00__hold6`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `858.662` / `1.2724135667` / `1168` / `3.5075075075` / `0.7351558219` / `-168.999` / `5.080870301`
- selected long/short/balance(선택 롱/숏/균형): `1041` / `127` / `0.1219980788`
- runtime_authority(런타임 권위): `not_claimed`

## Top Proxy Rows(상위 프록시 행)

| queue_id | axis_id | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | candidate_status | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| density_anchor_hold6_pf_probe(밀도 기준 보유6 PF 탐침) | hold_shape(보유 형태) | 858.662 | 1.2724135667 | 3.5075075075 | -168.999 | 127 | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 992.841178715 |
| control_replay_density_anchor(대조 재생 밀도 기준점) | control_anchor(대조 기준) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119 | watch_density_safe_pf_below_reference(밀도 안전이나 PF 기준 미달 관찰) | 852.863251865 |
| density_anchor_short0455_edge(밀도 기준 숏0.455 경계) | threshold_edge(임계값 경계) | 789.589 | 1.2670836468 | 2.9039039039 | -133.361 | 86 | fail_density_floor(밀도 하한 실패) | 652.27072627 |
| pfpass_core_short_restore_budget_010(PF통과 핵심 숏 0.10 복원) | short_restore(숏 복원) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6 | fail_density_floor(밀도 하한 실패) | 410.418022536 |
| pfpass_guardrail_no_trade_split(PF통과 거래쪼개기 금지 가드) | guardrail(가드레일) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6 | fail_density_floor(밀도 하한 실패) | 410.418022536 |
| dd_seed_density_restore_core_late(낙폭 씨앗 핵심후반 밀도 복원) | dd_restore(낙폭 복원) | 688.499 | 1.2534558955 | 2.7807807808 | -128.108 | 109 | fail_density_floor(밀도 하한 실패) | 367.327753275 |
| pfpass_late_long_density_patch(PF통과 후반 롱 밀도 패치) | late_long_restore(후반 롱 복원) | 810.666 | 1.310783255 | 2.6696696697 | -120.303 | 6 | fail_density_floor(밀도 하한 실패) | 358.312178894 |
| pfpass_month_pocket_observation(PF통과 월 포켓 관찰) | market_behavior(시장 현상) | 799.943 | 1.3066323163 | 2.6726726727 | -120.303 | 8 | fail_density_floor(밀도 하한 실패) | 96.533312892 |
| pfpass_validation_balance_patch(PF통과 검증 균형 패치) | split_balance(분할 균형) | 390.702 | 1.2128851815 | 1.7087087087 | -164.69 | 8 | fail_density_floor(밀도 하한 실패) | -1600.859568975 |
| pfpass_non_drag_session_restore(PF통과 비끌림 세션 복원) | session_restore(세션 복원) | 343.724 | 1.1795958461 | 1.7537537538 | -164.69 | 6 | fail_density_floor(밀도 하한 실패) | -1602.408069335 |

## Baseline Comparison(기준 비교)

| metric_id | reference_value | selected_value | delta_selected_minus_reference |
| --- | --- | --- | --- |
| combined_net_profit | 840.055 | 858.662 | 18.607 |
| combined_profit_factor | 1.2739357721 | 1.2724135667 | -0.0015222054 |
| combined_trade_count | 1001 | 1168 | 167.0 |
| combined_trade_per_business_day | 3.006006006 | 3.5075075075 | 0.5015015015 |
| combined_expectancy | 0.8392157842 | 0.7351558219 | -0.1040599623 |
| combined_max_drawdown | -142.323 | -168.999 | -26.676 |
| combined_recovery_factor | 5.9024542765 | 5.080870301 | -0.8215839755 |
| combined_long_count | 882 | 1041 | 159.0 |
| combined_short_count | 119 | 127 | 8.0 |
| combined_long_short_balance | 0.1349206349 | 0.1219980788 | -0.0129225561 |

## Gate Audit(게이트 감사)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/final_decision.json | run364AM proxy scout(364AM 프록시 정찰)를 닫음 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/input_manifest.csv | run364AL 대기열과 부모 산출물을 확인함 |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/data_integrity_receipt.json | 시점 안전 프록시 재생 경계를 기록함 |
| queue_replay_gate(대기열 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/pf_pass_density_restore_proxy_scout_surface.csv | 12개 대기열 행을 재생함 |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/queue_replay_audit.csv | top_n 재생 없음 |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/pf_pass_density_restore_proxy_scout_surface.csv | 거래 쪼개기 없음 |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/pf_pass_density_restore_proxy_scout_surface.csv | net/PF/expectancy/DD/RF/trades/side/density 기록 |
| model_boundary_audit(모델 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/model_boundary_receipt.json | 새 모델 학습 없음과 threshold(임계값) 경계를 기록 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/performance_attribution_receipt.json | 복원 정책별 성과 귀속 연결 |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/result_judgment_receipt.json | MT5 필요 경계로 판정 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/artifact_lineage_receipt.json | 입력/출력 해시 연결 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/claim_boundary_receipt.json | 런타임 권위 주장 없음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AM/required_gate_coverage_audit.csv | 필수 게이트를 종료 기록에 연결 |

## Claim Boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 scout(정찰)는 timestamp-safe proxy(시점 안전 프록시) 후보 선별이며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다.
