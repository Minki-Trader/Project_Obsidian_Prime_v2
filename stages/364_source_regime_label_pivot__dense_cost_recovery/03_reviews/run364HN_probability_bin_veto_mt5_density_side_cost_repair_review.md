# run364HN Probability-Bin Veto Density/Side/Cost Repair Review(확률 구간 거부 밀도/방향/비용 수리 검토)

Updated(갱신): 2026-06-09T12:10:08Z

## Judgment(판정)

- run_id(실행 ID): `run364HN_review_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`
- parent_run_id(상위 실행 ID): `run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`
- judgment(판정): `positive_package_readiness_clue_scaled_density_seed_single_source_mt5_package_required_no_authority`
- decision(결정): `stage364HN_open_run364HO_single_source_probability_bin_veto_runtime_package`
- next_run_id(다음 실행 ID): `run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): HM selected seed(HM 선택 씨앗)인 `fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160`를 single-source runtime package(단일 원천 런타임 패키지) 후보로 검토했습니다.

Effect(효과): OOS net/PF/density(표본외 순수익/수익 팩터/밀도) `333.32` / `1.4709758917` / `2.5496183206`와 scaled density estimate(스케일 밀도 추정) `3.055518353`는 긍정 단서입니다. 다만 direct density proof(직접 밀도 증명)는 없고 validation cost(검증 비용)가 취약해 운영 권위는 없습니다.

## Package Readiness(패키지 준비성)

| review_item | status | evidence | feature_count | feature_order_hash | max_abs_diff | effect |
| --- | --- | --- | --- | --- | --- | --- |
| onnx_joblib_lineage(ONNX/잡립 계보) | passed(통과) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/onnx/fj_sym_h2_m1p75_fj_behavior_density_cost_et8_l18_n160.onnx \| stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/models/fj_sym_h2_m1p75_fj_behavior_density_cost_et8_l18_n160.joblib |  |  |  | HO package(HO 패키지)가 같은 모델 산출물을 사용할 수 있습니다. |
| onnx_smoke(ONNX 스모크) | passed(통과) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/onnx_smoke_report.csv |  |  | 1.56324e-07 | Python model(Python 모델)과 ONNX(온엑스) 출력 차이가 작은지 확인합니다. |
| feature_order_contract(피처 순서 계약) | passed_reconstructable(통과, 재현 가능) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/hn_fj_single_source_feature_order_contract.json | 60 | 204d912740d40322db76967362166c363a86afeb559cbeca8538cc9b9ab0d654 |  | HO에서 feature CSV(피처 CSV)와 MT5 set(설정 파일)의 입력 수를 고정할 수 있습니다. |
| single_source_route(단일 원천 라우트) | package_ready_clue(패키지 준비 단서) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/hm_route_parity_decision.csv |  |  |  | GZ+HB dual-source fallback(GZ+HB 이중 원천 대체)의 partial parity(부분 동등성)를 재사용하지 않고 단일 FJ 모델로 좁힙니다. |

## Guardrails(가드레일)

| guardrail | value | threshold | status | effect |
| --- | --- | --- | --- | --- |
| direct_proxy_density(직접 프록시 밀도) | 2.5496183206 | 3.0 | failed_recorded(실패 기록) | 직접 3/day(일 3회) 증명은 없으므로 MT5 proof(MT5 증명)로 부르지 않습니다. |
| scaled_density_estimate(스케일 밀도 추정) | 3.055518353 | 3.0 | passed_as_clue_only(통과, 단서 전용) | HL ratio(HL 비율)를 사용한 추정이라 HO/MT5 확인 전까지 권위가 없습니다. |
| side_balance(방향 균형) | 0.5483425414 | 0.65 | passed(통과) | short-heavy(숏 과중) 실패 기억을 완화했는지 봅니다. |
| validation_cost06(검증 비용0.6) | -0.819 | > 0 | fragile_recorded(취약 기록) | validation(검증) 비용 압박이 약해 운영 주장을 막습니다. |
| combined_cost09(합산 비용0.9) | 15.101 | > 0 | thin_pass_recorded(얇은 통과 기록) | 비용 0.9에서 간신히 버티므로 HO에서 MT5 cost/fill(비용/체결) 차이를 봐야 합니다. |
| no_trade_splitting(거래 쪼개기 금지) | true | single_position_jump_to_exit_plus_one | passed(통과) | 거래수를 쪼개 수익을 나누는 방식을 배제합니다. |

## Cost/Side Stability(비용/방향 안정성)

| item | validation_cost06_net | validation_cost09_net | oos_cost06_net | combined_cost09_net | row_count | status | effect |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cost_stress_summary(비용 압박 요약) | -0.819 | -117.819 | 233.12 | 15.101 |  | oos_strong_validation_fragile(표본외 강함, 검증 취약) | 다음 HO/MT5 package(HO/MT5 패키지)에서 비용 차이를 우선 확인하게 합니다. |
| side_session_rows(방향/세션 행) |  |  |  |  | 19 | recorded(기록됨) | 특정 hour(시간) 또는 side(방향)에 수익이 몰리는지 HO 검토 입력으로 넘깁니다. |
| month_rows(월별 행) |  |  |  |  | 16 | recorded(기록됨) | equity curve quality(수익곡선 품질)와 월별 안정성을 다음 MT5 probe(MT5 탐침)에서 비교할 수 있습니다. |

## Next Queue(다음 대기열)

| queue_id | next_run_id | model_id | feature_order_contract | target | avoid | effect |
| --- | --- | --- | --- | --- | --- | --- |
| ho01_materialize_single_source_probability_bin_veto_package | run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1 | fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160 | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/hn_fj_single_source_feature_order_contract.json | materialize MT5 runtime package(MT5 런타임 패키지 물질화) | do not call scaled density MT5 proof(스케일 밀도를 MT5 증명으로 부르지 않음) | proxy clue(프록시 단서)를 MT5 runtime probe(MT5 런타임 탐침)로 검증할 수 있게 합니다. |

## Boundary(경계)

This run(이 실행)은 package readiness review(패키지 준비성 검토)입니다. MT5 runtime probe(MT5 런타임 탐침), runtime package(런타임 패키지), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| parent_hm_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/final_decision.json | HM 입력 계보를 확인했습니다. |
| hm_required_gate_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/required_gate_coverage_audit.csv | HM 필수 gate(게이트)가 모두 통과했습니다. |
| selected_seed_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/hn_package_readiness_review.csv | ONNX/joblib(온엑스/잡립) 계보를 확인했습니다. |
| onnx_smoke_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/onnx_smoke_report.csv | ONNX smoke(온엑스 스모크)를 확인했습니다. |
| feature_order_reconstruct_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/hn_fj_single_source_feature_order_contract.json | FJ feature order(FJ 피처 순서)를 재현했습니다. |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/selected_hm_seed_trade_tape.csv | 거래 쪼개기 금지를 확인했습니다. |
| scaled_density_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/hn_guardrail_review.csv | 스케일 밀도는 단서 전용임을 기록했습니다. |
| cost_fragility_recorded_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/hn_cost_side_stability_review.csv | validation cost(검증 비용) 취약성을 숨기지 않았습니다. |
| single_source_route_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/hm_route_parity_decision.csv | 단일 원천 route(라우트)로 복잡도를 줄이는 경계를 기록했습니다. |
| package_next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/run364HO_single_source_probability_bin_veto_package_queue.csv | HO runtime package(HO 런타임 패키지) 대기열을 만들었습니다. |
| paired_tier_record_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv | Tier A/Tier B/Tier A+B 기록 경계를 남겼습니다. |
| artifact_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HN/artifact_lineage_receipt.json | 산출물 계보를 연결했습니다. |
