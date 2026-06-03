# run364AG PF lift density-safe scout(364AG PF 상승 밀도 안전 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AG_train_pf_lift_density_safe_expansion_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AF_materialize_pf_lift_density_safe_expansion_without_db_v1`
- next_run_id(다음 실행 ID): `run364AH_review_pf_lift_density_safe_expansion_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_pf_lift_density_safe_candidates_ranked_mt5_probe_required_no_authority`
- scout_rows(정찰 행): `12`
- strict_pass_rows(엄격 통과 행): `0`
- selected_variant_id(선택 변형 ID): `selected_density_safe_control__ps0_45__floor0_0__hold8`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `840.055` / `1.2739357721` / `1001` / `3.006006006` / `0.8392157842` / `-142.323` / `5.9024542765`
- selected long/short/balance(선택 롱/숏/균형): `882` / `119` / `0.1349206349`
- runtime_authority(런타임 권위): `not_claimed`

## Top Proxy Rows(상위 프록시 행)

| queue_id | axis_id | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | candidate_status | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| selected_density_safe_control | control(대조) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119 | watch_pf_below_target(PF 목표 미만 관찰) | 858.0676332645 |
| selected_short0455_restore_margin010 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 799.923 | 1.2639812133 | 2.963963964 | -133.361 | 105 | fail_density_floor(밀도 하한 실패) | 770.39052003 |
| selected_short0460_restore_margin010 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 774.416 | 1.2598776815 | 2.9009009009 | -133.361 | 85 | fail_density_floor(밀도 하한 실패) | 659.3669527215 |
| selected_short0465_restore_margin008 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 672.228 | 1.2262896407 | 2.8708708709 | -125.956 | 74 | fail_density_floor(밀도 하한 실패) | 507.038339414 |
| pfpass_short050_restore_short0475 | pf_pass_density_restore(PF 통과 밀도 복원) | 794.569 | 1.3021603444 | 2.6876876877 | -120.303 | 13 | fail_density_floor(밀도 하한 실패) | 431.485879878 |
| pf_pass_density_fail_control | control(대조) | 799.943 | 1.3066323163 | 2.6726726727 | -120.303 | 8 | fail_density_floor(밀도 하한 실패) | 420.948814176 |
| pfpass_short050_restore_margin008 | pf_pass_density_restore(PF 통과 밀도 복원) | 799.943 | 1.3066323163 | 2.6726726727 | -120.303 | 8 | fail_density_floor(밀도 하한 실패) | 420.948814176 |
| pfpass_short049_restore_margin010 | pf_pass_density_restore(PF 통과 밀도 복원) | 754.681 | 1.2815511632 | 2.7087087087 | -120.303 | 20 | fail_density_floor(밀도 하한 실패) | 404.506076536 |
| mixed_long041_adx35_short0475 | mixed_density_restore(혼합 밀도 복원) | 620.121 | 1.2122481628 | 2.8108108108 | -122.656 | 50 | fail_density_floor(밀도 하한 실패) | 370.016924233 |
| selected_short0475_restore_short0475 | short_quality_plus_density_restore(숏 품질 + 밀도 복원) | 628.996 | 1.216407956 | 2.7987987988 | -122.656 | 50 | fail_density_floor(밀도 하한 실패) | 365.762892532 |

## Baseline Comparison(기준 비교)

| metric_id | reference_value | selected_value | delta_selected_minus_reference |
| --- | --- | --- | --- |
| combined_net_profit | 840.055 | 840.055 | 0.0 |
| combined_profit_factor | 1.2739357721 | 1.2739357721 | 0.0 |
| combined_trade_count | 1001 | 1001 | 0.0 |
| combined_trade_per_business_day | 3.006006006 | 3.006006006 | 0.0 |
| combined_expectancy |  | 0.8392157842 | 0.8392157842 |
| combined_max_drawdown | -142.323 | -142.323 | 0.0 |
| combined_recovery_factor | 5.9024542765 | 5.9024542765 | 0.0 |
| combined_long_count | 882 | 882 | 0.0 |
| combined_short_count | 119 | 119 | 0.0 |
| combined_long_short_balance | 0.1349206349 | 0.1349206349 | 0.0 |

## Gate Audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/final_decision.json | run364AG proxy scout(364AG 프록시 정찰)를 닫음 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/input_manifest.csv | run364AF 대기열과 기준 산출물을 확인함 |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/data_integrity_receipt.json | 시점 안전 고정 임계값과 분할 경계를 기록함 |
| queue_replay_gate(대기열 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/pf_lift_density_safe_proxy_scout_surface.csv | 12개 대기열 행을 재생함 |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/queue_replay_audit.csv | top_n 재생이 없음을 확인함 |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/pf_lift_density_safe_proxy_scout_surface.csv | net/PF/expectancy/DD/RF/trades/side/density를 기록함 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/performance_attribution_receipt.json | 월/세션/방향 요약을 연결함 |
| model_boundary_gate(모델 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/model_boundary_receipt.json | 새 모델/ONNX 권위를 주장하지 않음 |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/result_judgment_receipt.json | MT5 필요 경계로 판정함 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/artifact_lineage_receipt.json | 입력/출력 해시를 연결함 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/claim_boundary_receipt.json | 런타임 권위를 주장하지 않음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AG/required_gate_coverage_audit.csv | 필수 게이트를 종료 기록에 연결함 |

## Claim Boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 scout(정찰)는 timestamp-safe proxy(시점 안전 프록시) 후보 선별이며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다.
