# run364HR Single-Source Probability-Bin Veto Trade-Quality Density Repair Scout(단일 원천 확률 구간 거부 거래 품질 밀도 수리 탐색)

Updated(갱신): 2026-06-10T12:51:22Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- parent_run_id(상위 실행 ID): `run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- judgment(판정): `negative_proxy_replay_scout_no_strict_pf_density_joint_pass_but_repair_clues_review_required_no_authority`
- strict_joint_pass_count(엄격 동시 통과 수): `0`
- best variant(최선 변형): `hold4_margin_0.01`
- best net/PF/density(최선 순수익/수익 팩터/밀도): `462.0071630903` / `1.2257899553` / `2.1178343949`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): HP MT5 telemetry(HP MT5 런타임 기록)의 probabilities(확률)와 HO feature matrix(HO 피처 행렬)의 entry_open(진입 시가)을 결합해 hold/reversal/margin/pflat/session-side(보유/반전/마진/평탄 확률/세션-방향) 변형을 replay(재생)했습니다.

Effect(효과): MT5 재실행 전 trade quality(거래 품질)과 density(밀도)가 같이 고쳐지는지 넓게 확인했습니다. 결과는 strict joint pass(엄격 동시 통과) 없음이며, HS review(HS 검토)가 수리 단서와 실패 경계를 판정해야 합니다.

## Top Surface(상위 표면)

| variant_id | family | combined_net_profit | combined_profit_factor | combined_trade_density | oos_net_profit | oos_profit_factor | strict_joint_pass | repair_clue | score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hold4_margin_0.01 | hold_margin_combo(보유/마진 조합) | 462.0071630903 | 1.2257899553 | 2.1178343949 | 245.8300987125 | 1.3001656381 | False | True | 467.0478176018 |
| hold10_reverse1 | hold_reversal(보유/반전) | 422.0524678113 | 1.1667772806 | 1.9936305732 | 304.1790901288 | 1.3240144407 | False | True | 416.9065058118 |
| hold2_reverse0 | hold_reversal(보유/반전) | 364.1542660946 | 1.1690920825 | 2.7133757962 | 333.5873175967 | 1.4359445837 | False | True | 377.2797108983 |
| hold8_reverse1 | hold_reversal(보유/반전) | 372.7161630903 | 1.1461530857 | 2.1178343949 | 124.7798369099 | 1.1269461373 | False | True | 368.2003932518 |
| hold3_margin_0.03 | hold_margin_combo(보유/마진 조합) | 345.0487725323 | 1.315573871 | 1.127388535 | 76.0003776824 | 1.1825936488 | False | True | 336.1023504227 |
| margin_floor_0.025 | margin_floor(마진 바닥) | 292.2571802576 | 1.2439241763 | 1.5987261146 | 161.9535364807 | 1.3660161148 | False | True | 286.4962342822 |
| hold4_reverse1 | hold_reversal(보유/반전) | 258.245562232 | 1.1059529237 | 2.4777070064 | 209.2684206009 | 1.2229023469 | False | True | 257.9025882338 |
| hold4_margin_0 | hold_margin_combo(보유/마진 조합) | 258.245562232 | 1.1059529237 | 2.4777070064 | 209.2684206009 | 1.2229023469 | False | True | 257.9025882338 |
| hold4_reverse0 | hold_reversal(보유/반전) | 263.4925793993 | 1.1288112567 | 1.9585987261 | 151.9209785408 | 1.1827956125 | False | True | 252.9148983519 |
| hold5_reverse0 | hold_reversal(보유/반전) | 265.3833905581 | 1.1337392872 | 1.7324840764 | 148.5933133048 | 1.1961473123 | False | True | 249.7442069292 |
| hold4_margin_0.02 | hold_margin_combo(보유/마진 조합) | 253.3565536482 | 1.1556733503 | 1.6242038217 | 210.7903948498 | 1.3287670054 | False | True | 237.642451227 |
| hold3_margin_0.02 | hold_margin_combo(보유/마진 조합) | 249.7869957083 | 1.1486440613 | 1.7993630573 | 59.9845450644 | 1.0860778041 | False | True | 237.6083594945 |

## Selected Clues(선택 단서)

| selection_role | variant_id | family | combined_net_profit | combined_profit_factor | combined_trade_density | oos_net_profit | oos_profit_factor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| quality_repair_density_fail(품질 수리, 밀도 실패) | hold4_margin_0.01 | hold_margin_combo(보유/마진 조합) | 462.0071630903 | 1.2257899553 | 2.1178343949 | 245.8300987125 | 1.3001656381 |
| density_repair_quality_fail(밀도 수리, 품질 실패) | hold1_margin_0.01 | hold_margin_combo(보유/마진 조합) | 152.3237553651 | 1.0824022765 | 3.1305732484 | 41.2259914164 | 1.0540446441 |
| oos_quality_clue(표본외 품질 단서) | hold4_margin_0.01 | hold_margin_combo(보유/마진 조합) | 462.0071630903 | 1.2257899553 | 2.1178343949 | 245.8300987125 | 1.3001656381 |

## Failure Memory(실패 기억)

| hypothesis | variants_tried | strict_joint_pass_count | failed_boundary | why_failed | salvage_value |
| --- | --- | --- | --- | --- | --- |
| Lifecycle/margin/session controls(생명주기/마진/세션 제어)가 HP 과잉 거래와 PF 붕괴를 동시에 수리할 수 있다. | 56 | 0 | no variant jointly passed PF>=1.2, density>=3/day, net>HP, OOS PF>=1.2(동시 통과 변형 없음) | quality-improving variants reduce density(품질 개선 변형은 밀도 저하), density variants keep PF weak(밀도 변형은 PF 약함) | quality_repair_density_fail(품질 수리, 밀도 실패)=hold4_margin_0.01; density_repair_quality_fail(밀도 수리, 품질 실패)=hold1_margin_0.01; oos_quality_clue(표본외 품질 단서)=hold4_margin_0.01 |

## Next Queue(다음 대기열)

| queue_id | action | effect |
| --- | --- | --- |
| review_strict_failure_boundary(엄격 실패 경계 검토) | Review why no PF/density joint pass appeared(PF/밀도 동시 통과가 왜 없었는지 검토) | HS can decide whether to widen density supply or change model/source(HS가 밀도 공급 확대 또는 모델/원천 변경을 결정할 수 있습니다). |
| review_quality_repair_density_fail(품질 수리, 밀도 실패) | Review variant(변형 검토) `hold4_margin_0.01` | Preserve clue(단서 보존): net/PF/density=462.0071630903/1.2257899553/2.1178343949 |
| review_density_repair_quality_fail(밀도 수리, 품질 실패) | Review variant(변형 검토) `hold1_margin_0.01` | Preserve clue(단서 보존): net/PF/density=152.3237553651/1.0824022765/3.1305732484 |
| review_oos_quality_clue(표본외 품질 단서) | Review variant(변형 검토) `hold4_margin_0.01` | Preserve clue(단서 보존): net/PF/density=462.0071630903/1.2257899553/2.1178343949 |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HQ/final_decision.json | HQ/HP/HO input lineage(입력 계보)를 확인했습니다. |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/data_integrity_audit.csv | timestamp/split/feature-label boundary(시각/분할/피처-라벨 경계)를 기록했습니다. |
| runtime_replay_calibration_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/runtime_cost_calibration.json | HP MT5 baseline(HP MT5 기준선)에 replay cost(재생 비용)를 보정했습니다. |
| variant_surface_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/runtime_replay_variant_surface.csv | trade-quality/density variant surface(거래 품질/밀도 변형 표면)를 만들었습니다. |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/failure_memory.csv | top_n/trade splitting(상위 N개/거래 쪼개기)을 쓰지 않았음을 기록했습니다. |
| repair_clue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/selected_repair_clues.csv | strict pass(엄격 통과)가 없어도 수리 단서를 따로 보존했습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/result_judgment_receipt.json | 필수 receipt(영수증)를 덮었습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결했습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HR/claim_boundary_receipt.json | 운영 주장(operating claim, 운영 주장)을 막았습니다. |

## Boundary(경계)

This run(이번 실행)은 proxy replay scout(프록시 재생 탐색)입니다. new MT5 execution(새 MT5 실행), runtime package(런타임 패키지), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
