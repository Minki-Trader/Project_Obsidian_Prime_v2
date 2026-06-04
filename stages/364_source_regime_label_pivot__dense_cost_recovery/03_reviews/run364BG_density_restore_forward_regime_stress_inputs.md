# run364BG density restore forward/regime stress inputs(364BG 밀도 복원 전진/국면 압박 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364BF_review_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1`
- judgment(판정): `materialization_completed_forward_regime_stress_scout_inputs_no_authority`
- parent MT5 net/PF/trades/density(부모 MT5 순수익/수익 팩터/거래수/밀도): `900.36` / `1.35` / `1016` / `3.0510510511`
- parent long/short(부모 롱/숏): `917` / `99`
- claim_boundary(주장 경계): `research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Action And Effect(행동과 효과)

Action(행동): BF MT5 runtime probe review(BF MT5 런타임 탐침 검토)를 forward block(전진 블록), month regime(月 국면), session/side(세션/방향), drawdown tail(낙폭 꼬리), short restore(숏 복원) 입력으로 materialize(물질화)했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도) 긍정 단서를 BH scout(BH 스카우트)의 압박 대기열로 넘기되, forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.

## Forward Blocks(전진 유사 블록)

| block_id | trades | net | pf | density | long_share | stress |
| --- | --- | --- | --- | --- | --- | --- |
| forward_like_2025Q1 | 170 | 122.82 | 1.282202105 | 2.7419354839 | 0.8352941176 | density_stress_review_required(밀도 압박 검토 필요) |
| forward_like_2025Q2 | 264 | 311.82 | 1.413231026 | 4.0615384615 | 0.9204545455 | long_skew_stress_review_required(롱 편향 압박 검토 필요) |
| forward_like_2025Q3 | 134 | 48.18 | 1.174704475 | 2.0303030303 | 0.9626865672 | density_stress_review_required(밀도 압박 검토 필요) |
| forward_like_2025Q4 | 225 | 222.57 | 1.376000946 | 3.4615384615 | 0.8933333333 | long_skew_stress_review_required(롱 편향 압박 검토 필요) |
| forward_like_2026Q1 | 177 | 171.68 | 1.421321292 | 3.1052631579 | 0.8813559322 | long_skew_stress_review_required(롱 편향 압박 검토 필요) |
| forward_like_2026Q2 | 46 | 23.29 | 1.231972112 | 5.1111111111 | 1.0 | long_skew_stress_review_required(롱 편향 압박 검토 필요) |

## Monthly Stress(月별 압박)

| month | trades | net | pf | bucket | score |
| --- | --- | --- | --- | --- | --- |
| 2025-01 | 88 | 40.14 | 1.165457543 | normal_positive_month_regime(일반 양수 월 국면) | 1 |
| 2025-04 | 121 | 211.95 | 1.438756288 | normal_positive_month_regime(일반 양수 월 국면) | 1 |
| 2025-05 | 76 | 42.33 | 1.265575005 | normal_positive_month_regime(일반 양수 월 국면) | 1 |
| 2025-06 | 67 | 57.54 | 1.513154374 | normal_positive_month_regime(일반 양수 월 국면) | 1 |
| 2025-07 | 35 | 11.69 | 1.172266431 | normal_positive_month_regime(일반 양수 월 국면) | 1 |
| 2025-08 | 47 | -0.37 | 0.996640029 | negative_month_regime(음수 월 국면) | 4 |
| 2025-09 | 52 | 36.86 | 1.376891616 | normal_positive_month_regime(일반 양수 월 국면) | 1 |
| 2025-10 | 78 | 31.76 | 1.155709173 | normal_positive_month_regime(일반 양수 월 국면) | 1 |
| 2025-11 | 84 | 224.51 | 2.056517647 | strong_month_regime(강한 월 국면) | 1 |
| 2025-12 | 63 | -33.7 | 0.807944378 | negative_month_regime(음수 월 국면) | 4 |
| 2026-01 | 82 | 27.43 | 1.148704326 | thin_edge_month_regime(얇은 엣지 월 국면) | 1 |
| 2026-02 | 91 | 135.91 | 1.610419942 | strong_month_regime(강한 월 국면) | 1 |
| 2026-04 | 46 | 23.29 | 1.231972112 | normal_positive_month_regime(일반 양수 월 국면) | 1 |

## Session/Side Stress(세션/방향 압박)

| hour | side | trades | net | pf | bucket |
| --- | --- | --- | --- | --- | --- |
| 16 | long | 129 | 29.87 | 1.06919798 | long_thin_edge_session(long 얇은 엣지 세션) |
| 17 | short | 37 | -10.82 | 0.919583798 | short_weak_session(short 약한 세션) |
| 18 | long | 199 | -42.17 | 0.914521425 | long_weak_session(long 약한 세션) |
| 18 | short | 25 | 95.77 | 3.865649312 | short_positive_restore_candidate(숏 양수 복원 후보) |
| 19 | long | 126 | -6.87 | 0.976839834 | long_weak_session(long 약한 세션) |
| 19 | short | 17 | 13.61 | 1.215177866 | short_positive_restore_candidate(숏 양수 복원 후보) |
| 20 | short | 13 | -29.11 | 0.562453029 | short_weak_session(short 약한 세션) |

## BH Queue(BH 대기열)

| queue_rank | queue_id | idea_type | policy_family | stress_labels | success_criteria |
| --- | --- | --- | --- | --- | --- |
| 1 | bh01_forward_block_replay_current_policy | runtime_verification(런타임 검증) | no_policy_change_forward_like_replay(정책 변경 없는 전진 유사 재생) | forward_like_2025Q1;forward_like_2025Q2;forward_like_2025Q3;forward_like_2025Q4;forward_like_2026Q1;forward_like_2026Q2 | no forward-like block has net<=0 or PF<1 while combined density stays >=3/day(전진 유사 블록 순수익 양수/PF 1 이상, 합산 밀도 3/day 이상) |
| 2 | bh02_month_regime_soft_firewall_no_delete | repair_control(수리/대조) | month_regime_soft_firewall(月 국면 소프트 방화벽) | 2025-08;2025-12;2026-01 | PF improves or weak-month loss shrinks while estimated density remains >=3/day(PF 개선 또는 약한 월 손실 축소, 추정 밀도 3/day 이상) |
| 3 | bh03_hour18_19_session_side_firewall | repair_control(수리/대조) | hour_side_soft_firewall(시간/방향 소프트 방화벽) | 16;17;18;19;20 | hour 18/19 expectancy improves without cutting total density below 3/day(18/19시 기대값 개선, 전체 밀도 3/day 이상) |
| 4 | bh04_short_positive_slice_restore | offensive_exploration(공격 탐색) | short_router_restore(숏 라우터 복원) | short_2025-04_h18;short_2026-02_h17;short_2025-02_h21;short_2026-01_h17;short_2025-10_h18;short_2025-11_h18;short_2025-11_h17;short_2025-04_h20 | short net remains positive and long_share falls below 0.88 with density >=3/day(숏 순수익 양수 유지, 롱 비중 0.88 미만, 밀도 3/day 이상) |
| 5 | bh05_drawdown_tail_hold_stress_not_hard_cap | repair_control(수리/대조) | drawdown_tail_hold_stress(낙폭 꼬리 보유 압박) | dd_02_10_to_15;dd_03_ge15;hold_tail_gt_288 | drawdown tail shrinks while preserving long-hold positive contribution(낙폭 꼬리 축소와 장기 보유 양수 기여 보존) |

## Guardrails(가드레일)

| guardrail | status | evidence | effect |
| --- | --- | --- | --- |
| no_trade_splitting(거래 쪼개기 금지) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/run364BH_forward_regime_stress_scout_queue.csv | 거래수를 쪼개서 KPI(핵심 성과 지표)를 부풀리지 않는다. |
| no_top_n_or_oos_threshold_selection(top_n/OOS 임계값 선택 금지) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/run364BH_forward_regime_stress_scout_queue.csv | 사후 상위 선택이나 표본외 임계값 선택으로 과적합하지 않는다. |
| timestamp_boundary(시점 경계) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/data_integrity_receipt.json | month/hour/side(월/시간/방향)는 진입 시점 정보로, outcome labels(결과 라벨)는 학습/압박 전용으로 분리한다. |
| parent_density_floor_context(부모 밀도 하한 문맥) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BF/density_guardrail_audit.csv | BF 실제 MT5 밀도 3/day(일 3회) 이상 단서를 다음 scout(스카우트)의 하한으로 유지한다. |
| operating_claim_guard(운영 주장 가드) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/claim_boundary_receipt.json | forward pass(전진 통과)와 runtime authority(런타임 권위)를 주장하지 않는다. |

## Required Gates(필수 게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/final_decision.json | BG materialization(BG 물질화) 범위를 final decision(최종 결정)으로 닫는다. |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/run_evidence_receipt.json | BF MT5 KPI(BF MT5 핵심 성과 지표)를 원천 권위로 둔다. |
| skill_receipt_lint(스킬 영수증 점검) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/work_packet.json | primary/support skills(주/보조 스킬)와 receipt(영수증)를 연결한다. |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/data_integrity_receipt.json | 시점/라벨/분할 경계를 기록한다. |
| forward_regime_materialization_gate(전진/국면 물질화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/run364BH_forward_regime_stress_scout_queue.csv | BH scout(BH 스카우트) 입력 대기열을 생성한다. |
| guardrail_matrix_gate(가드레일 행렬 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/regime_guardrail_matrix.csv | 거래 쪼개기/top_n/표본외 임계값 선택 금지를 확인한다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/artifact_lineage_receipt.json | 입력/출력 산출물 해시를 연결한다. |
| claim_boundary_gate(주장 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/claim_boundary_receipt.json | 운영 주장과 전진 통과 주장을 열지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BG/required_gate_coverage_audit.csv | registry(등록부)의 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)

BG는 materialization only(물질화 전용)다. 새 model training(모델 학습), 새 MT5 execution(MT5 실행), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
