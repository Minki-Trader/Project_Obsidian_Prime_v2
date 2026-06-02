# run364AD PF/DD density bridge scout(364AD PF/DD 밀도 연결 정찰)

## Current truth(현재 진실)

- run_id(실행 ID): `run364AD_train_pf_dd_near_miss_density_bridge_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AC_materialize_pf_dd_near_miss_density_bridge_without_db_v1`
- next_run_id(다음 실행 ID): `run364AE_review_pf_dd_near_miss_density_bridge_scout_without_db_v1`
- judgment(판정): `proxy_scout_completed_timestamp_safe_bridge_candidates_ranked_mt5_probe_required_no_authority`
- scout_rows(정찰 행): `13`
- strict_pass_rows(엄격 통과 행): `0`
- selected_variant_id(선택 변형 ID): `stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8`
- selected net/PF/trades/density/DD(선택 순수익/수익 팩터/거래수/밀도/낙폭): `840.055` / `1.2739357721` / `1001` / `3.006006006` / `-142.323`
- runtime_authority(런타임 권위): `not_claimed`

## Top proxy rows(상위 프록시 행)

| queue_id | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | candidate_status | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| stress3_restore_non_hour16_margin_0_1 | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119 | watch_pf_below_target(PF 목표 미만 관찰) | 884.172870032 |
| stress3_restore_march_short_p0_475 | 834.818 | 1.2721814278 | 3.0 | -142.323 | 117 | watch_pf_below_target(PF 목표 미만 관찰) | 876.958204586 |
| stress_zone_4_control | 808.044 | 1.2584924377 | 3.042042042 | -142.323 | 131 | watch_pf_below_target(PF 목표 미만 관찰) | 853.120714624 |
| baseline_replay_control | 771.564 | 1.2218406503 | 3.2462462462 | -155.007 | 129 | watch_pf_below_target(PF 목표 미만 관찰) | 822.459352504 |
| stress3_restore_long_p0_42_adx35_0 | 846.467 | 1.277866063 | 2.987987988 | -142.323 | 112 | fail_density_floor(밀도 하한 실패) | -112.40765103 |
| stress3_restore_non_hour16_margin_0_14 | 844.03 | 1.2768298079 | 2.993993994 | -142.323 | 115 | fail_density_floor(밀도 하한 실패) | -113.478676972 |
| adx38_stress3_month_block | 848.542 | 1.2835497807 | 2.9159159159 | -128.661 | 113 | fail_density_floor(밀도 하한 실패) | -114.645804016 |
| stress3_restore_march_short_p0_49 | 841.18 | 1.2761305224 | 2.987987988 | -142.323 | 113 | fail_density_floor(밀도 하한 실패) | -118.223578082 |
| stress_zone_3_control | 840.192 | 1.2758061959 | 2.984984985 | -142.323 | 112 | fail_density_floor(밀도 하한 실패) | -120.148395812 |
| stress3_restore_long_p0_4_adx45_0 | 840.192 | 1.2758061959 | 2.984984985 | -142.323 | 112 | fail_density_floor(밀도 하한 실패) | -120.148395812 |

## Expression safety audit(표현 안전 감사)

| source_queue_id | safety_status | effect(효과) |
| --- | --- | --- |
| baseline_replay_control | accepted_timestamp_safe(시점 안전 수용) | expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용) |
| stress_zone_3_control | accepted_timestamp_safe(시점 안전 수용) | expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용) |
| stress_zone_4_control | accepted_timestamp_safe(시점 안전 수용) | expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용) |
| stress3_restore_march_short_top5 | rewritten_top_n_not_replayed(상위 N개 표현 미재생, 고정 임계값 대체) | top_n expressions are not replayed because future month ranking is not runtime-safe(top_n 표현은 월 전체 미래 순위라 런타임 안전하지 않아 재생하지 않음) |
| stress3_restore_march_non_hour16_top8 | rewritten_top_n_not_replayed(상위 N개 표현 미재생, 고정 임계값 대체) | top_n expressions are not replayed because future month ranking is not runtime-safe(top_n 표현은 월 전체 미래 순위라 런타임 안전하지 않아 재생하지 않음) |
| stress3_restore_march_adx45_long_top8 | rewritten_top_n_not_replayed(상위 N개 표현 미재생, 고정 임계값 대체) | top_n expressions are not replayed because future month ranking is not runtime-safe(top_n 표현은 월 전체 미래 순위라 런타임 안전하지 않아 재생하지 않음) |
| stress4_short0475_pf_lift | accepted_timestamp_safe(시점 안전 수용) | expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용) |
| stress4_short050_pf_lift | accepted_timestamp_safe(시점 안전 수용) | expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용) |
| adx38_stress3_month_block | accepted_timestamp_safe(시점 안전 수용) | expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용) |
| adx38_stress4_month_long_block | accepted_timestamp_safe(시점 안전 수용) | expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용) |

## Baseline comparison(기준 비교)

| metric_id | baseline_value | selected_value | delta_selected_minus_baseline |
| --- | --- | --- | --- |
| combined_net_profit | 771.564 | 840.055 | 68.491 |
| combined_profit_factor | 1.2218406503 | 1.2739357721 | 0.0520951218 |
| combined_trade_count | 1081 | 1001 | -80.0 |
| combined_trade_per_business_day | 3.2462462462 | 3.006006006 | -0.2402402402 |
| combined_max_drawdown | -155.007 | -142.323 | 12.684 |
| combined_recovery_factor | 4.9776074629 | 5.9024542765 | 0.9248468136 |
| combined_short_count | 129 | 119 | -10.0 |

## Gate audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/final_decision.json | run364AD scope(364AD 범위)를 proxy scout(프록시 정찰)로 닫는다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/data_integrity_receipt.json | 시점 안전 고정 임계값 경계를 기록한다. |
| topn_rewrite_gate(top_n 재작성 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/bridge_expression_safety_audit.csv | top_n 표현을 직접 재생하지 않는다. |
| proxy_replay_gate(프록시 재생 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/pf_dd_density_bridge_proxy_scout_surface.csv | timestamp-safe variants(시점 안전 변형)를 재생한다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/performance_attribution_receipt.json | 기준 대비 KPI 차이를 기록한다. |
| model_boundary_gate(모델 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/model_boundary_receipt.json | 새 모델/ONNX(온엑스) 권위를 주장하지 않는다. |
| result_judgment_gate(결과 판정 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/result_judgment_receipt.json | MT5 필요 경계로 판정한다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/artifact_lineage_receipt.json | 입력/출력 hash(해시)를 연결한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/claim_boundary_receipt.json | runtime authority(런타임 권위)를 열지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AD/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Claim boundary(주장 경계)

`research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 scout(정찰)는 timestamp-safe proxy(시점 안전 프록시) 후보 선별이며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다.
