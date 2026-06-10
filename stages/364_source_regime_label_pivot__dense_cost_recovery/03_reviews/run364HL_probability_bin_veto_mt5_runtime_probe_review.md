# run364HL Probability-Bin Veto MT5 Runtime Probe Review(확률 구간 거부 MT5 런타임 탐침 검토)

Updated(갱신): 2026-06-08T13:06:21Z

## Judgment(판정)

- run_id(실행 ID): `run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`
- parent_run_id(상위 실행 ID): `run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`
- judgment(판정): `positive_runtime_probe_clue_mt5_net_pf_pass_trade_density_below_goal_short_heavy_cost_stress_and_route_parity_repair_required_no_authority`
- next_run_id(다음 실행 ID): `run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): HK MT5 result(HK MT5 결과)를 OOS-only proxy(OOS 전용 프록시)와 scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시)로 나눠 검토했습니다.

Effect(효과): MT5 net/PF/trades(순수익/수익 팩터/거래수) `369.03 / 1.39 / 542`는 긍정 단서지만, 실제 trade density(거래 밀도) `1.7261146497`는 3/day(일 3회) 미만이라 운영 후보가 아닙니다.

| mt5_net_profit | mt5_profit_factor | mt5_expectancy | mt5_trade_count | mt5_trade_density | mt5_drawdown | mt5_recovery_factor | mt5_long_trade_count | mt5_short_trade_count | mt5_short_share | scope_aligned_net_diff | scope_aligned_trade_diff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 369.03 | 1.39 | 0.68 | 542 | 1.7261146497 | 94.78 | 3.89 | 118 | 424 | 0.7822878229 | 145.082 | 133.0 |

## Scope Alignment(범위 정렬)

| comparison_id | proxy_scope | mt5_scope | expected_net | actual_mt5_net | net_diff_actual_minus_expected | expected_trade_count | actual_mt5_trade_count | trade_count_diff_actual_minus_expected | scope_alignment_status | usability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hk_recorded_oos_only_vs_mt5_total(HK 기록 OOS 전용 대 MT5 전체) | oos_only(표본외 전용) | validation_plus_oos_runtime_total(검증+표본외 런타임 전체) | 78.188 | 369.03 | 290.842 | 180.0 | 542.0 | 362.0 | scope_mismatch_for_total_judgment(전체 판정 범위 불일치) | usable_only_as_oos_reference(OOS 기준 참고로만 사용) |
| scope_aligned_validation_oos_proxy_vs_mt5_total(범위 정렬 검증+표본외 프록시 대 MT5 전체) | validation_plus_oos(검증+표본외) | validation_plus_oos_runtime_total(검증+표본외 런타임 전체) | 223.948 | 369.03 | 145.082 | 409.0 | 542.0 | 133.0 | scope_aligned_for_review(검토 범위 정렬) | usable_for_next_density_side_cost_repair_scout(다음 밀도/방향/비용 수리 탐색에 사용 가능) |

## Route Mix(라우트 혼합)

| route_item | tier_a_used_count | tier_b_fallback_used_count | tier_a_order_attempt_count | tier_b_fallback_order_attempt_count | order_attempt_count | short_signal_share | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| feature_route_mix(피처 라우트 혼합) | 1477.0 | 15951.0 |  |  |  |  | fallback_materially_used(대체 라우트 실질 사용) |
| order_route_mix(주문 라우트 혼합) |  |  | 931.0 | 151.0 | 1082.0 |  | fallback_order_contribution_present(대체 주문 기여 있음) |
| signal_direction_mix(신호 방향 혼합) |  |  |  |  |  | 0.8057228916 | short_heavy_signal_surface(숏 편중 신호 표면) |

## Guardrails(가드레일)

| guardrail | value | threshold | status | effect |
| --- | --- | --- | --- | --- |
| mt5_net_pf_positive_runtime_clue(MT5 순수익/PF 긍정 런타임 단서) | 369.03 / 1.39 | net>0 and PF>1.25(순수익>0 그리고 PF>1.25) | passed_as_positive_clue_only(긍정 단서로만 통과) | MT5 real-tick tester(MT5 실틱 테스터)에서 수익 단서가 실제로 관찰됐지만 운영 권위는 만들지 않습니다. |
| trade_density_goal(거래 밀도 목표) | 1.7261146497 | 3.0 | failed_user_goal_below_3_per_day(사용자 목표 실패, 일 3회 미만) | order_attempt_count(주문 시도 수)가 아니라 MT5 report trade_count(MT5 보고서 거래수) 기준으로 밀도를 재서 거래 쪼개기 착시를 막습니다. |
| side_balance_short_share(방향 균형 숏 비중) | 0.7822878229 | 0.7 | failed_short_heavy(실패, 숏 편중) | 숏 수익 구조가 강하지만 한쪽 방향에 과도하게 기대는 위험을 다음 탐색 제약으로 바꿉니다. |
| proxy_cost_stress(프록시 비용 압박) | oos_cost06=24.188; combined_cost09=-21.452 | combined_cost09>=0(합산 비용0.9 >= 0) | failed_in_proxy_guardrail(프록시 가드레일 실패) | MT5 수익이 좋아도 강한 비용 압박에서는 약한 원인을 다음 탐색에서 줄입니다. |
| route_parity_boundary(라우트 동등성 경계) | probability_bin_veto represented; dual_source_route partial(확률 구간 거부 표현됨; 이중 원천 라우트 부분 표현) | full route parity required before authority(권위 전 전체 라우트 동등성 필요) | partial_represented_no_authority(부분 표현, 권위 없음) | EA fallback-after-flat(EA flat 이후 대체)이 Python score switch(Python 점수 전환)를 완전히 대체한다고 말하지 않습니다. |
| forward_replay_evidence(전진/재생 근거) | missing(없음) | required for operating claim(운영 주장에 필요) | missing_required_for_authority(권위에는 필수 누락) | 단일 Strategy Tester(전략 테스터) 탐침을 live readiness(실거래 준비)로 오해하지 않습니다. |

## Next Queue(다음 대기열)

| queue_item | seed | target | avoid | effect |
| --- | --- | --- | --- | --- |
| density_lift_without_trade_splitting(거래 쪼개기 없는 밀도 상승) | MT5 net/PF positive but trade_count density below 3/day(MT5 순수익/PF 긍정이나 거래수 밀도 일 3회 미만) | trade_density>=3/day, PF>=1.25, net>0(거래 밀도 일 3회 이상, PF 1.25 이상, 순수익 양수) | do not count entry/exit order attempts as trades(진입/청산 주문 시도를 거래수로 세지 않음) | 사용자 거래수 목표를 실제 MT5 report trade_count(MT5 보고서 거래수) 기준으로 맞춥니다. |
| short_heavy_quality_filter(숏 편중 품질 필터) | short_share=0.7822878229 | short_share<=0.70 first, <=0.65 target(숏 비중 0.70 이하 우선, 0.65 이하 목표) | do not destroy short edge while forcing symmetry(균형 강제로 숏 엣지를 파괴하지 않음) | 강한 숏 수익 구조를 살리면서 방향 붕괴 위험을 줄입니다. |
| cost_resilience_repair(비용 회복력 수리) | HF combined_cost09 below zero(HF 합산 비용0.9 음수) | combined_cost09>=0 and OOS cost06 stays positive(합산 비용0.9 양수, OOS 비용0.6 양수 유지) | do not select only on MT5 headline net(MT5 표면 순수익만으로 선택하지 않음) | 실틱 MT5 수익 단서를 비용 압박에서도 버티는 구조로 다듬습니다. |
| route_parity_decision(라우트 동등성 결정) | HJ dual-source route partial(HJ 이중 원천 라우트 부분 표현) | decide whether to implement score-switch parity or keep fallback-after-flat as separate runtime idea(점수 전환 동등성 구현 여부 결정) | do not call partial route runtime authority(부분 라우트를 런타임 권위로 부르지 않음) | Python proxy(Python 프록시)와 EA behavior(EA 행동)의 차이를 다음 탐색 변수로 격리합니다. |

## Boundary(경계)

이 run(실행)은 positive runtime clue(긍정 런타임 단서) 검토입니다. operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/work_packet.json | 입력 산출물(input artifacts, 입력 산출물)을 확인했습니다. |
| mt5_output_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/probability_bin_veto_mt5_review.csv | MT5 output(MT5 출력)을 review(검토)했습니다. |
| scope_alignment_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/scope_aligned_proxy_mt5_review.csv | OOS-only proxy(OOS 전용 프록시)와 validation+OOS(검증+표본외) 범위를 분리했습니다. |
| route_mix_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/runtime_route_mix_review.csv | Tier A/Tier B route usage(Tier A/Tier B 라우트 사용)를 기록했습니다. |
| density_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/probability_bin_veto_mt5_guardrail_review.csv | 3/day(일 3회) 밀도 목표 미달을 명시했습니다. |
| side_balance_guardrail_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/probability_bin_veto_mt5_guardrail_review.csv | short-heavy(숏 편중) 경계를 기록했습니다. |
| cost_stress_guardrail_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/probability_bin_veto_mt5_guardrail_review.csv | 비용 압박(cost stress, 비용 압박) 경계를 기록했습니다. |
| runtime_parity_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/runtime_parity_receipt.json | 부분 라우트(partial route, 부분 라우트)를 권위(authority, 권위)로 승격하지 않았습니다. |
| artifact_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/artifact_lineage_receipt.json | 산출물 계보(artifact lineage, 산출물 계보)를 연결했습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결했습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/claim_boundary_receipt.json | Goal Achieve(목표 달성), runtime authority(런타임 권위), operating promotion(운영 승격)을 막았습니다. |
