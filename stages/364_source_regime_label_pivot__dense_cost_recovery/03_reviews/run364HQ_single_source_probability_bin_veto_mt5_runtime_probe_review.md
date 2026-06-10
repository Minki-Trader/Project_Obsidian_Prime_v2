# run364HQ Single-Source Probability-Bin Veto MT5 Review(단일 원천 확률 구간 거부 MT5 검토)

Updated(갱신): 2026-06-09T13:07:28Z

## Judgment(판정)

- run_id(실행 ID): `run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`
- parent_run_id(상위 실행 ID): `run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`
- judgment(판정): `valid_negative_runtime_probe_review_net_positive_but_pf_expectancy_drawdown_and_density_boundary_failed_repair_required_no_authority`
- next_run_id(다음 실행 ID): `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): HP MT5 runtime probe(HP MT5 런타임 탐침)를 scope alignment(범위 정렬), trade shape(거래 형태), guardrail(가드레일), performance attribution(성과 귀속)으로 검토했습니다.

Effect(효과): MT5 net profit(MT5 순수익) 양수 단서는 보존하지만 PF/expectancy/drawdown/density(PF/기대값/낙폭/밀도) 실패 때문에 `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`에서 trade quality density repair(거래 품질 밀도 수리)를 실행합니다.

## Scope Alignment(범위 정렬)

| comparison_id | proxy_scope | mt5_scope | expected_net | actual_mt5_net | net_diff_actual_minus_expected | expected_trade_count | actual_mt5_trade_count | trade_count_diff_actual_minus_expected | expected_trade_density | actual_mt5_trade_density | scope_alignment_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hp_recorded_oos_only_vs_mt5_total(HP 기록 OOS 전용 대 MT5 전체) | oos_only(표본외 전용) | validation_plus_oos_runtime_total(검증+표본외 런타임 전체) | 333.32 | 113.38 | -219.94 | 334.0 | 932.0 | 598.0 |  |  | scope_mismatch_reference_only(범위 불일치 참고 전용) |
| scope_aligned_validation_oos_proxy_vs_mt5_total(범위 정렬 검증+표본외 프록시 대 MT5 전체) | validation_plus_oos(검증+표본외) | validation_plus_oos_runtime_total(검증+표본외 런타임 전체) | 449.501 | 113.38 | -336.121 | 724.0 | 932.0 | 208.0 | 2.3057324841 | 2.9681528662 | scope_aligned_for_review(검토 범위 정렬) |

## Trade Shape(거래 형태)

| feature_ready_count | order_fill_count | report_trade_count | report_trade_density | runtime_order_density | long_trade_count | short_trade_count | short_share | profit_factor | expectancy | max_drawdown_percent | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17428 | 1756 | 932.0 | 2.9681528662 | 5.5923566879 | 404.0 | 528.0 | 0.5665236052 | 1.05 | 0.12 | 45.8 | borderline_below_3_by_report_trade_count(보고서 거래수 기준 3 미만 경계 실패) |

## Guardrails(가드레일)

| guardrail | value | threshold | status | effect |
| --- | --- | --- | --- | --- |
| net_profit_positive(순수익 양수) | 113.38 | > 0 | passed_as_positive_clue_only(긍정 단서로만 통과) | 순수익 양수는 보존하지만 운영 주장은 만들지 않습니다. |
| profit_factor_quality(수익 팩터 품질) | 1.05 | materially above 1 and near proxy(1 초과 및 프록시 근접) | failed_pf_compression(PF 압축 실패) | PF가 1.05라 비용/실행 압박에 매우 취약합니다. |
| expectancy_quality(기대값 품질) | 0.12 | proxy-aligned positive(프록시 정렬 양수) | failed_expectancy_collapse(기대값 붕괴 실패) | 거래 수 증가는 있지만 거래당 품질이 낮아졌습니다. |
| drawdown_recovery(낙폭/회복) | dd_pct=45.8;rf=0.4 | RF > 1 and drawdown controlled(RF 1 초과 및 낙폭 통제) | failed_drawdown_recovery(낙폭/회복 실패) | net(순수익) 대비 drawdown(낙폭)이 너무 커 운영 후보가 아닙니다. |
| report_trade_density(보고서 거래 밀도) | 2.9681528662 | >= 3/day(일 3회 이상) | failed_borderline_below_user_floor(사용자 하한 미달 경계 실패) | runtime order density(런타임 주문 밀도)는 대체 지표일 뿐 report trade density(보고서 거래 밀도)를 대체하지 않습니다. |
| side_balance(롱/숏 균형) | 0.5665236052 | short_share <= 0.60(숏 비중 0.60 이하) | passed_mild_short_tilt(약한 숏 기울기 통과) | 이전 short-heavy(숏 편중)보다 낫지만 수익 품질 실패를 가리지 못합니다. |
| scope_aligned_proxy_mt5_profit(범위 정렬 프록시/MT5 수익) | -336.121 | near zero or positive(0 근처 또는 양수) | failed_scope_aligned_profit_collapse(범위 정렬 수익 붕괴 실패) | OOS-only mismatch(OOS 전용 불일치)를 제거해도 MT5 수익이 proxy(프록시)보다 크게 낮습니다. |

## Attribution(귀속)

| observed_change | comparison_baseline | likely_drivers | attribution_confidence | next_probe |
| --- | --- | --- | --- | --- |
| MT5 kept positive net(양수 순수익 유지) but compressed PF/expectancy(수익 팩터/기대값 압축) and expanded trade count(거래수 확대). | HO combined proxy(HO 합산 프록시): net/PF/trades 449.501/1.2595656515/724 vs HP MT5 113.38/1.05/932 | reverse-on-opposite lifecycle(반대 신호 반전 생명주기), report trade accounting(보고서 거래 집계), cost accumulation(비용 누적), probability-bin veto not selective enough(확률 구간 거부 선택성 부족) | medium(중간) | run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1 |

## Next Queue(다음 대기열)

| queue_id | action | target | failure_memory |
| --- | --- | --- | --- |
| trade_quality_density_repair(거래 품질 밀도 수리) | Explore entry-transition/reversal/hold controls without top_n or trade splitting(상위 N개 자르기나 거래 쪼개기 없이 진입 전환/반전/보유 제어 탐색) | report trade density >= 3/day(보고서 거래 밀도 일 3회 이상), PF materially above 1.2(PF 1.2 의미 있게 초과), RF repair(RF 수리) | HP overtraded vs proxy(HP 프록시 대비 과잉 거래) and PF collapsed(PF 붕괴) |
| cost_pf_repair(비용 PF 수리) | Stress probability-bin veto and margin floor against MT5 cost drag(MT5 비용 끌림에 대해 확률 구간 거부와 마진 바닥 압박 시험) | gross loss compression(총손실 압축) without killing trade density(거래 밀도 훼손 없음) | HP gross profit/loss nearly neutral(HP 총수익/총손실 거의 중립) |
| session_side_cluster_review(세션/방향 군집 검토) | Segment HP telemetry/report by session, side, and drawdown clusters(HP 런타임 기록/보고서를 세션, 방향, 낙폭 군집으로 분해) | Find removable churn pockets(제거 가능한 회전매매 구간 찾기) | HQ attribution confidence is medium because segment detail is missing(HQ 귀속 신뢰도는 세부 구간 누락 때문에 중간) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HP/final_decision.json | HP/HO input lineage(입력 계보)를 확인했습니다. |
| mt5_output_review_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HP/strategy_tester_report_records.json | MT5 report/telemetry(MT5 보고서/런타임 기록)를 검토했습니다. |
| scope_alignment_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HQ/scope_alignment_review.csv | OOS-only comparison(OOS 전용 비교)과 combined comparison(합산 비교)을 분리했습니다. |
| trade_shape_guardrail_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HQ/guardrail_review.csv | density/PF/DD/side(밀도/PF/낙폭/방향)를 guardrail(가드레일)로 판정했습니다. |
| performance_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HQ/performance_attribution_review.csv | 성과 변화 원인을 medium confidence(중간 신뢰도)로 귀속했습니다. |
| next_probe_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HQ/run364HR_trade_quality_density_repair_queue.csv | HR repair queue(HR 수리 대기열)를 만들었습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HQ/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결했습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HQ/claim_boundary_receipt.json | 운영 주장(operating claim, 운영 주장)을 막았습니다. |

## Boundary(경계)

This review(이번 검토)는 runtime probe review(런타임 탐침 검토)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
