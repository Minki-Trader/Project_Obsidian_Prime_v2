# run364EP h17 OOS108 validation floor bridge MT5 runtime probe review(17시 OOS108 검증 바닥 연결 MT5 런타임 탐침 검토)

Updated(갱신): 2026-06-06T16:42:11Z

## Judgment(판정)

- run_id(실행 ID): `run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`
- judgment(판정): `positive_runtime_probe_clue_scope_adjusted_mt5_net_density_pf_pass_short_heavy_cost_stress_repair_required_no_authority`
- next_run_id(다음 실행 ID): `run364EQ_train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): EO MT5 result(EO MT5 결과)를 OOS-only proxy(표본외 전용 프록시)와 scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시)로 나눠 다시 검토했습니다.

Effect(효과): 거래수 차이(trade count diff, 거래수 차이) `+795`는 범위 불일치(scope mismatch, 범위 불일치)가 커 보이게 만든 숫자이고, 범위 정렬 후 실제 차이는 `+75`입니다.

| mt5_net_profit | mt5_profit_factor | mt5_expectancy | mt5_trade_count | mt5_trade_density | mt5_drawdown | mt5_recovery_factor | mt5_long_trade_count | mt5_short_trade_count | mt5_short_share | scope_aligned_net_diff | scope_aligned_trade_diff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 523.58 | 1.21 | 0.4 | 1314 | 4.1847133758 | 206.2 | 2.54 | 307 | 1007 | 0.7663622527 | 119.645 | 75.0 |

## Scope Alignment(범위 정렬)

| comparison_id | proxy_scope | mt5_scope | expected_net | actual_mt5_net | net_diff_actual_minus_expected | expected_trade_count | actual_mt5_trade_count | trade_count_diff_actual_minus_expected | scope_alignment_status | usability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eo_recorded_oos_only_vs_mt5_total(EO 기록 OOS 전용 대 MT5 전체) | oos_only(표본외 전용) | validation_plus_oos(검증+표본외) | 201.155 | 523.58 | 322.425 | 519.0 | 1314.0 | 795.0 | scope_mismatch_for_total_judgment(전체 판정 범위 불일치) | usable_only_as_oos_reference(OOS 기준 참고로만 사용) |
| scope_aligned_validation_oos_proxy_vs_mt5_total(범위 정렬 검증+표본외 프록시 대 MT5 전체) | validation_plus_oos(검증+표본외) | validation_plus_oos(검증+표본외) | 403.935 | 523.58 | 119.645 | 1239.0 | 1314.0 | 75.0 | scope_aligned_for_review(검토 범위 정렬) | usable_for_next_repair_scout(다음 수리 탐색에 사용 가능) |

## Guardrails(가드레일)

| guardrail | value | threshold | status | effect |
| --- | --- | --- | --- | --- |
| density_floor(거래 밀도 하한) | 4.1847133758 | 3.0 | passed(통과) | 거래수는 3/day(일 3회) 요구를 만족하지만, 거래 쪼개기(trade splitting, 거래 쪼개기) 증거로 쓰지 않습니다. |
| profit_factor_floor(수익 팩터 바닥) | 1.21 | above validation/oos proxy PF(검증/표본외 프록시 PF 초과) | passed_with_runtime_probe_boundary(런타임 탐침 경계 포함 통과) | MT5 PF(수익 팩터)는 검증/OOS proxy PF(프록시 수익 팩터)보다 높지만 운영 권위(runtime authority, 런타임 권위)는 아닙니다. |
| short_share_caution(숏 비중 주의) | 0.7663622527 | 0.7 | caution_short_heavy(주의, 숏 편중) | 범위 정렬 후 short share(숏 비중)는 proxy(프록시)보다 조금 낮지만 여전히 70%를 넘습니다. |
| cost_stress_validation_cost06(검증 비용 0.6 압박) | -13.22 | >=0 | failed_in_proxy_guardrail(프록시 가드레일 실패) | validation cost stress(검증 비용 압박)가 약해 다음 탐색은 비용 견딤(cost resilience, 비용 회복력)을 올려야 합니다. |
| cost_stress_combined_cost09(합산 비용 0.9 압박) | -339.465 | >=0 | failed_in_proxy_guardrail(프록시 가드레일 실패) | 강한 비용 압박에서는 validation+OOS(검증+표본외) 합산도 무너져 운영 주장(operating claim, 운영 주장)을 막습니다. |
| runtime_timestamp_coverage(런타임 시각 커버리지) | 17428 | feature matrix rows 17428(피처 행렬 17428행) | passed_with_tail_skip_boundary(꼬리 스킵 경계 포함 통과) | feature_ready/model_ok(피처 준비/모델 성공)는 패키지 범위를 채웠지만 이후 tester tail(테스터 꼬리)은 CSV 밖이라 스킵되었습니다. |

## Result Boundary(결과 경계)

- positive clue(긍정 단서): MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `523.58` / `1.21` / `1314`입니다.
- corrected read(보정 판독): validation+OOS proxy(검증+표본외 프록시) 대비 MT5 net(순수익)은 `119.645` 높고 trade count(거래수)는 `75.0` 많습니다.
- unresolved guardrail(미해결 가드레일): short-heavy(숏 편중), validation cost stress(검증 비용 압박), forward/replay evidence(전진/재생 근거)가 남아 있습니다.
- no authority(권위 없음): operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 없습니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/required_gate_coverage_audit.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/oos108_validation_floor_bridge_mt5_probe_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/proxy_mt5_runtime_difference.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/strategy_tester_report_records.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/runtime_output_copy_manifest.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/runtime_identity.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/expected_kpi_summary.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/feature_matrix_audit.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/runtime_policy_config.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/runtime_parity_contract.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/tester_identity_contract.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/tester_set_manifest.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/mt5_onnx_contract_audit.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/cost_stress_review.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EM/side_balance_review.csv;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/final_decision.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/selected_el_candidate.json;stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/el_oos108_validation_floor_bridge_trade_surface.csv;stage_pipelines/stage364/review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db.py | EO/EN/EM/EL evidence(근거)를 모두 연결합니다. |
| mt5_output_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EO/oos108_validation_floor_bridge_mt5_probe_summary.csv | MT5 output(MT5 출력)이 KPI review(KPI 검토)에 충분한지 확인합니다. |
| scope_alignment_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EP/scope_aligned_proxy_mt5_review.csv | OOS-only proxy(OOS 전용 프록시)와 validation+OOS MT5(검증+표본외 MT5) 범위 차이를 분리합니다. |
| cost_stress_guardrail_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EP/oos108_mt5_guardrail_review.csv | 비용 압박(cost stress, 비용 압박)을 다음 탐색 조건으로 남깁니다. |
| side_balance_guardrail_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EP/oos108_validation_floor_bridge_mt5_review.csv | long/short balance(롱/숏 균형)를 운영 주장 전에 검토합니다. |
| runtime_parity_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EP/runtime_parity_receipt.json | runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않습니다. |
| artifact_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EP/artifact_lineage_receipt.json | 입력/출력 산출물 계보(artifact lineage, 산출물 계보)를 연결합니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EP/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결합니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EP/claim_boundary_receipt.json | Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위)를 막습니다. |

## Next(다음)

`run364EQ_train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db_v1`는 scope-aligned proxy(범위 정렬 프록시), cost resilience(비용 회복력), short-heavy quality filter(숏 편중 품질 필터)를 탐색합니다. 효과(effect, 효과)는 MT5 순수익 단서를 보존하면서 운영 주장 전에 깨지는 가드레일을 줄이는 것입니다.
