# run364AT threshold-edge PF gap repair review(364AT 임계값 경계 PF 간극 수리 검토)

## Current Truth(현재 진실)

- action(행동): run364AS(364AS 실행)의 strict pass(엄격 통과) 1행을 package/probe(패키지/탐침) 관점으로 검토했다.
- effect(효과): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`를 runtime probe candidate(런타임 탐침 후보)로 열고, 운영 주장은 닫았다.
- selected KPI(선택 KPI): net(순수익) `862.283`, PF(수익 팩터) `1.3105654109`, density(밀도) `3.1981981982`, DD(낙폭) `-133.571`, trades(거래수) `1065`, short(숏) `87`.
- warning(경고): month-side negative rows(월/방향 음수 행) `10`개와 runtime evidence missing(런타임 근거 없음)이 남아 있다.
- authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.

## Surface Review(표면 검토)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침) | proxy_package_candidate_runtime_probe_required(프록시 패키지 후보, 런타임 탐침 필요) | 862.283 | 1.3105654109 | 3.1981981982 | -133.571 | 87.0 | 917.263304614 |
| threshold_edge_hold6_control(임계값 경계 6봉 대조) | density_dd_safe_pf_gap_seed(밀도/DD 안전, PF 간극 씨앗) | 840.779 | 1.2804442925 | 3.3843843844 | -147.924 | 87.0 | 849.817790125 |
| late_long_hold6_control(후반 롱 6봉 대조) | density_dd_safe_pf_gap_seed(밀도/DD 안전, PF 간극 씨앗) | 706.218 | 1.2520021924 | 3.0690690691 | -147.473 | 127.0 | 707.10767506 |
| threshold_edge_late_long_blend_probe(임계값 경계 후반 롱 혼합 탐침) | density_dd_safe_pf_gap_seed(밀도/DD 안전, PF 간극 씨앗) | 606.277 | 1.2177465697 | 3.1411411411 | -143.346 | 96.0 | 580.245770305 |
| pf_pass_density_bridge_hold6_probe(PF 통과 밀도 연결 6봉 탐침) | density_safe_pf_gap_watch(밀도 안전, PF 간극 관찰) | 765.45 | 1.2781248762 | 3.1861861862 | -157.864 | 7.0 | 752.98116953 |
| threshold_edge_hold5_probe(임계값 경계 5봉 탐침) | density_safe_pf_gap_watch(밀도 안전, PF 간극 관찰) | 588.663 | 1.1840210198 | 3.7717717718 | -169.6 | 91.0 | 628.999635846 |
| threshold_edge_hold4_probe(임계값 경계 4봉 탐침) | density_safe_pf_gap_watch(밀도 안전, PF 간극 관찰) | 361.57 | 1.1131824339 | 4.2672672673 | -213.135 | 97.0 | -173.719526069 |

## Package Gate Audit(패키지 게이트 감사)

| gate_id | status | observed | required | effect |
| --- | --- | --- | --- | --- |
| strict_proxy_package_candidate(엄격 프록시 패키지 후보) | passed | 1 | 1 | PF/density/split/side/DD 조건을 동시에 만족한 후보를 런타임 탐침 대상으로 연다. |
| selected_profit_factor_target(선택 PF 목표) | passed | 1.3105654109 | 1.3 | 프록시 기준 PF 1.30 이상인지 확인한다. |
| selected_density_floor(선택 밀도 하한) | passed | 3.1981981982 | 3.0 | 거래수 쪼개기 없이 3/day 이상 밀도인지 확인한다. |
| validation_oos_pf_net(검증/표본외 PF와 순수익) | passed | validation and oos positive with PF>=1.30(검증/표본외 양수와 PF 1.30 이상) | validation/oos net>0 and PF>=1.30(검증/표본외 순수익 양수와 PF 1.30 이상) | 한쪽 split(분할)만 좋은 후보를 걸러낸다. |
| drawdown_improvement(낙폭 개선) | passed | -133.571 | >= -147.924 | threshold-edge clue(임계값 경계 단서) 대비 DD가 악화되지 않았는지 본다. |
| short_side_presence(숏 방향 존재) | passed | 87.0 | 50 | 롱만 남은 구조를 피한다. |
| session_stress(세션 압박) | passed | 0 | 0 | 세션 단위 음수 구간이 있는지 본다. |
| month_side_stress(월/방향 압박) | warning | 10 | 0 | 월/방향 손실 군집은 MT5 탐침 후 repair(수리) 후보로 남긴다. |
| cost_runtime_evidence(비용/런타임 근거) | out_of_scope_by_claim(주장 범위 밖) | not_run(미실행) | MT5 runtime probe(MT5 런타임 탐침) | 프록시 결과를 MT5 KPI로 대체하지 않는다. |
| operating_claim_boundary(운영 주장 경계) | passed | runtime_authority=not_claimed; operating_promotion=not_claimed | no operating claim(운영 주장 없음) | 좋은 프록시를 운영 가능 모델로 착각하지 않게 한다. |

## Split Stability(분할 안정성)

| split_id | net_profit | profit_factor | trade_per_business_day | max_drawdown | review_status |
| --- | --- | --- | --- | --- | --- |
| validation(검증) | 444.701 | 1.3063428042 | 2.7989690722 | -65.039 | passed(통과) |
| oos(표본외) | 417.582 | 1.3151921464 | 3.7553956835 | -133.571 | passed(통과) |
| combined(합산) | 862.283 | 1.3105654109 | 3.1981981982 | -133.571 | passed(통과) |

## Session Stress(세션 압박)

| entry_session | side | segment_trade_count | segment_net_profit | segment_profit_factor | segment_max_drawdown | review_status |
| --- | --- | --- | --- | --- | --- | --- |
| post_cash_late(현금장 후반) | long | 10.0 | 170.267 | 19.7518722467 | -7.352 | passed(통과) |
| us_cash_core(미국 현금장 핵심) | long | 805.0 | 431.765 | 1.2227979248 | -147.928 | passed(통과) |
| us_cash_core(미국 현금장 핵심) | short | 87.0 | 63.716 | 1.1944084237 | -98.358 | passed(통과) |
| us_premarket_cash_open(미국 프리마켓/현금장 초반) | long | 163.0 | 196.535 | 1.391699834 | -58.048 | passed(통과) |

## Month-Side Stress(월/방향 압박)

| entry_month | side | segment_trade_count | segment_net_profit | segment_profit_factor | segment_max_drawdown | review_status |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-04 | short | 13.0 | 0.917 | 1.0126645214 | -48.182 | month_side_positive(월/방향 양수) |
| 2025-12 | short | 4.0 | 1.175 | 1.1358381503 | -6.425 | month_side_positive(월/방향 양수) |
| 2025-01 | short | 6.0 | 5.812 | 1.2080395175 | -27.937 | month_side_positive(월/방향 양수) |
| 2025-10 | long | 70.0 | 7.199 | 1.0423368482 | -52.886 | month_side_positive(월/방향 양수) |
| 2026-04 | long | 44.0 | 11.825 | 1.1190236537 | -57.24 | month_side_positive(월/방향 양수) |
| 2025-02 | short | 11.0 | 12.946 | 1.2417012061 | -27.862 | month_side_positive(월/방향 양수) |
| 2025-10 | short | 6.0 | 20.939 | 1.7958268405 | -19.774 | month_side_positive(월/방향 양수) |
| 2026-02 | short | 10.0 | 21.9 | 1.9988597491 | -8.275 | month_side_positive(월/방향 양수) |
| 2025-02 | long | 59.0 | 25.67 | 1.1862425724 | -44.901 | month_side_positive(월/방향 양수) |
| 2025-11 | short | 9.0 | 28.687 | 1.9832733505 | -15.501 | month_side_positive(월/방향 양수) |
| 2026-01 | short | 5.0 | 32.615 | 8.9066666667 | -4.125 | month_side_positive(월/방향 양수) |
| 2026-01 | long | 74.0 | 35.72 | 1.2413350449 | -58.035 | month_side_positive(월/방향 양수) |

## Required Gates(필수 게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/final_decision.json | AT review(검토) 산출물이 완성됨 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AS/final_decision.json | AS scout(정찰) 완료와 엄격 통과 확인 |
| package_gate_audit(패키지 게이트 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/package_gate_audit.csv | 프록시 패키지 후보 조건을 감사함 |
| split_stability_gate(분할 안정성 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/split_stability_review.csv | validation/OOS(검증/표본외)를 분리 검토함 |
| session_stress_gate(세션 압박 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/session_stress_review.csv | 세션별 수익 구조를 검토함 |
| month_stress_gate(월 압박 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/month_stress_review.csv | 월/방향 음수 셀을 기록함 |
| positive_clue_gate(긍정 단서 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/positive_clues.csv | 다음 runtime probe(런타임 탐침) 후보를 기록함 |
| failure_memory_gate(실패 기억 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/failure_memory.csv | 런타임 부재와 월/방향 음수 셀을 제약으로 기록함 |
| runtime_probe_queue_gate(런타임 탐침 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/run364AU_runtime_probe_package_queue.csv | 다음 MT5 package/probe(패키지/탐침) 대기열을 작성함 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/claim_boundary_receipt.json | 운영 주장 없음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AT/work_packet.json | 작업 묶음 필수 게이트를 산출물에 연결함 |

## Claim Boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
