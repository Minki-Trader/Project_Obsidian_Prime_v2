# run364AK session-side PF lift density repair review(364AK 세션/방향 PF 상승 밀도 수리 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1`
- judgment(판정): `negative_for_package_positive_for_pf_pass_density_restore_offensive_seed_no_authority`
- package_decision(패키지 결정): `no_package_strict_rows_zero_and_selected_pf_below_target(패키지 없음, 엄격 행 0 및 선택 PF 목표 미달)`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `840.055` / `1.2739357721` / `1001` / `3.006006006` / `0.8392157842` / `-142.323` / `5.9024542765`
- package_candidate_rows(패키지 후보 행): `0`
- pf_pass_density_fail_rows(PF 통과 밀도 실패 행): `1`
- next_queue_rows(다음 대기열 행): `12`
- runtime_authority(런타임 권위): `not_claimed`

## Surface Review(표면 검토)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count |
| --- | --- | --- | --- | --- | --- | --- |
| selected_control_full_session(선택 대조 전체 세션) | near_pf_density_safe_seed(PF 근접 밀도 안전 씨앗) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119.0 |
| validation_pf_repair_selected_split_guard(선택 후보 검증 PF 수리 분할 가드) | near_pf_density_safe_seed(PF 근접 밀도 안전 씨앗) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119.0 |
| month_positive_pocket_observation_only(월 양수 포켓 관찰 전용) | near_pf_density_safe_seed(PF 근접 밀도 안전 씨앗) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119.0 |
| oos_locked_replay_control(표본외 잠금 재생 대조) | near_pf_density_safe_seed(PF 근접 밀도 안전 씨앗) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119.0 |
| pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원) | pf_pass_density_fail_seed(PF 통과 밀도 실패 씨앗) | 845.554 | 1.3287468527 | 2.6636636637 | -120.303 | 6.0 |
| pfpass_core_plus_premarket_long_restore(PF 통과 핵심 + 프리마켓 롱 복원) | dd_improved_density_fail_seed(낙폭 개선 밀도 실패 씨앗) | 761.975 | 1.2958707973 | 2.6576576577 | -120.303 | 6.0 |
| core_plus_late_long(핵심 세션 + 후반 롱) | dd_improved_density_fail_seed(낙폭 개선 밀도 실패 씨앗) | 725.57 | 1.2757971879 | 2.7147147147 | -103.533 | 99.0 |
| pfpass_core_restore(통과 PF 핵심 복원) | dd_improved_density_fail_seed(낙폭 개선 밀도 실패 씨앗) | 615.722 | 1.2713337758 | 2.4474474474 | -96.138 | 11.0 |
| core_session_only_dual_side(핵심 세션 양방향만) | dd_improved_density_fail_seed(낙폭 개선 밀도 실패 씨앗) | 645.703 | 1.2448583586 | 2.7087087087 | -103.533 | 99.0 |
| block_premarket_short_only(프리마켓 숏만 차단) | reject_density_floor(밀도 하한 탈락) | 805.222 | 1.2676271111 | 2.9399399399 | -133.361 | 98.0 |

## Package Gate Audit(패키지 게이트 감사)

| gate_id | status | observed | required | effect(효과) |
| --- | --- | --- | --- | --- |
| strict_package_rows(엄격 패키지 행) | failed | 0 | 1 | PF(수익 팩터), density(밀도), split(분할), short side(숏 방향)를 동시에 만족하지 못하면 package(패키지)를 막는다. |
| selected_profit_factor_target(선택 PF 목표) | failed | 1.2739357721 | 1.3 | 선택 row(행)의 PF(수익 팩터)가 목표 아래면 운영 후보로 올리지 않는다. |
| selected_density_floor(선택 밀도 하한) | passed | 3.006006006 | 3.0 | 거래 빈도가 너무 낮은 수익 착시를 막는다. |
| selected_split_profit(선택 분할 수익) | passed | validation=339.043; oos=501.012 | both_positive(둘 다 양수) | validation(검증)과 OOS(표본외)가 반대로 갈리는 후보를 막는다. |
| best_pf_density_bridge(최고 PF 밀도 연결) | failed | pf=1.3287468527; density=2.6636636637 | pf>=1.3; density>=3.0 | PF(수익 팩터)가 오른 row(행)의 density(밀도) 붕괴를 다음 탐색 제약으로 바꾼다. |
| external_runtime_evidence(외부 런타임 근거) | out_of_scope_by_claim(주장 범위 밖) | not_run(미실행) | MT5 runtime probe(MT5 런타임 탐침) | 이번 review(검토)를 MT5(메타트레이더5) 권위로 오해하지 않게 한다. |

## Policy Review(정책 검토)

| queue_id | review_status | combined_profit_factor | combined_trade_per_business_day | materialized_policy | session_policy |
| --- | --- | --- | --- | --- | --- |
| pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원) | pf_pass_density_fail_policy(PF 통과 밀도 실패 정책) | 1.3287468527 | 2.6636636637 | pf_pass_seed_block_premarket_short_restore_density(PF 통과 씨앗 프리마켓 숏 차단 밀도 복원) | all_sessions_except_premarket_short(프리마켓 숏 제외 전체) |
| pfpass_core_plus_premarket_long_restore(PF 통과 핵심 + 프리마켓 롱 복원) | watch_policy(관찰 정책) | 1.2958707973 | 2.6576576577 | pf_pass_seed_restore_core_and_premarket_long(PF 통과 씨앗 핵심 및 프리마켓 롱 복원) | us_cash_core_plus_premarket_long(핵심 + 프리마켓 롱) |
| core_plus_late_long(핵심 세션 + 후반 롱) | watch_policy(관찰 정책) | 1.2757971879 | 2.7147147147 | core_session_plus_late_long(핵심 세션 + 후반 롱) | us_cash_core_plus_post_cash_late_long(핵심 + 현금장 후반 롱) |
| selected_control_full_session(선택 대조 전체 세션) | density_safe_pf_near_policy(밀도 안전 PF 근접 정책) | 1.2739357721 | 3.006006006 | baseline_replay(기준 재생) | all_sessions(전체 세션) |
| validation_pf_repair_selected_split_guard(선택 후보 검증 PF 수리 분할 가드) | density_safe_pf_near_policy(밀도 안전 PF 근접 정책) | 1.2739357721 | 3.006006006 | validation_pf_drag_repair_without_oos_selection(표본외 선택 없는 검증 PF 끌림 수리) | all_sessions_with_validation_report(전체 세션, 검증 분리 보고) |
| month_positive_pocket_observation_only(월 양수 포켓 관찰 전용) | density_safe_pf_near_policy(밀도 안전 PF 근접 정책) | 1.2739357721 | 3.006006006 | month_pocket_observation_no_filter(월 포켓 관찰, 필터 아님) | all_sessions(전체 세션) |
| oos_locked_replay_control(표본외 잠금 재생 대조) | density_safe_pf_near_policy(밀도 안전 PF 근접 정책) | 1.2739357721 | 3.006006006 | oos_locked_control_replay(표본외 잠금 대조 재생) | all_sessions(전체 세션) |
| pfpass_core_restore(통과 PF 핵심 복원) | watch_policy(관찰 정책) | 1.2713337758 | 2.4474474474 | pf_pass_seed_restore_core_session(PF 통과 씨앗 핵심 세션 복원) | us_cash_core_restore(미국 현금장 핵심 복원) |

## Session Side Review(세션 방향 검토)

| entry_session | side | review_status | segment_net_profit | segment_profit_factor | segment_trade_count | segment_trade_per_business_day |
| --- | --- | --- | --- | --- | --- | --- |
| us_cash_core(미국 현금장 핵심) | long | positive_pf_segment(양수 PF 세그먼트) | 622.482 | 1.316715265 | 715 | 2.1471471471 |
| us_cash_core(미국 현금장 핵심) | short | positive_pf_segment(양수 PF 세그먼트) | 102.921 | 1.3122669474 | 86 | 0.2613981763 |
| post_cash_late(현금장 후반) | long | too_sparse_watch(희소 관찰) | 80.77 | inf | 5 | 0.0246305419 |
| us_premarket_cash_open(미국 프리마켓/현금장 초반) | long | positive_but_pf_below_target(PF 목표 미만 양수) | 46.197 | 1.0737177544 | 162 | 0.4864864865 |
| us_premarket_cash_open(미국 프리마켓/현금장 초반) | short | loss_or_pf_drag(손실 또는 PF 끌림) | -12.315 | 0.9150191492 | 33 | 0.1044303797 |

## Month Side Review(월 방향 검토)

| entry_month | side | review_status | segment_net_profit | segment_profit_factor | segment_trade_count |
| --- | --- | --- | --- | --- | --- |
| 2025-04 | long | positive_pf_segment(양수 PF 세그먼트) | 175.964 | 1.435582488 | 87 |
| 2025-11 | long | positive_pf_segment(양수 PF 세그먼트) | 112.066 | 1.4471728981 | 59 |
| 2025-05 | long | positive_pf_segment(양수 PF 세그먼트) | 93.222 | 1.9164929805 | 59 |
| 2026-03 | long | positive_pf_segment(양수 PF 세그먼트) | 86.985 | 1.353705398 | 78 |
| 2025-06 | long | positive_pf_segment(양수 PF 세그먼트) | 85.534 | 1.7558611182 | 60 |
| 2025-10 | long | positive_pf_segment(양수 PF 세그먼트) | 73.454 | 1.4761978853 | 62 |
| 2026-02 | short | positive_pf_segment(양수 PF 세그먼트) | 60.988 | 2.8773047681 | 11 |
| 2026-01 | long | positive_pf_segment(양수 PF 세그먼트) | 52.2 | 1.3646015227 | 67 |

## Positive Clues(긍정 단서)

| clue_id | evidence | kpi_read | effect(효과) |
| --- | --- | --- | --- |
| pf_pass_density_fail_exists(PF 통과 밀도 실패 존재) | pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원) | net=845.554; pf=1.3287468527; density=2.6636636637; dd=-120.303; shorts=6.0 | PF(수익 팩터)를 올리는 규칙은 있으나 밀도 복원 장치가 필요하다는 방향을 준다. |
| density_safe_pf_near_anchor(밀도 안전 PF 근접 기준점) | selected_control_full_session(선택 대조 전체 세션); validation_pf_repair_selected_split_guard(선택 후보 검증 PF 수리 분할 가드) | net=840.055; pf=1.2739357721; density=3.006006006; dd=-142.323 | density(밀도)를 지키는 control(대조)을 기준점으로 삼아 수익 팩터만 올리는 탐색을 연다. |
| drawdown_improvement_density_fail(낙폭 개선 밀도 실패) | pfpass_core_plus_premarket_long_restore(PF 통과 핵심 + 프리마켓 롱 복원); core_plus_late_long(핵심 세션 + 후반 롱) | dd_delta=22.02; dd=-120.303; density=2.6576576577; dd_delta=38.79; dd=-103.533; density=2.7147147147 | drawdown(낙폭) 개선 규칙은 density(밀도) 복원과 결합할 가치가 있다. |
| core_session_dual_side_positive(핵심 세션 양방향 양수) | long net=622.482; short net=102.921 | side=long; pf=1.316715265; trades=715; density=2.1471471471; side=short; pf=1.3122669474; trades=86; density=0.2613981763 | core session(핵심 세션)을 지키는 복원은 short collapse(숏 붕괴)를 줄일 수 있다. |
| month_side_positive_pockets(월 방향 양수 포켓) | 2025-04 long; 2025-11 long; 2025-05 long; 2026-03 long | net=175.964; pf=1.435582488; trades=87; net=112.066; pf=1.4471728981; trades=59; net=93.222; pf=1.9164929805; trades=59; net=86.985; pf=1.353705398; trades=78 | market behavior(시장 현상)상 월별 방향 포켓은 관찰하되 필터로 고정하지 않는다. |

## Failure Memory(실패 기억)

| failure_id | evidence | kpi_read | constraint_for_next(다음 제약) |
| --- | --- | --- | --- |
| no_strict_package_rows(엄격 패키지 행 없음) | strict_pass_rows=0 | selected_pf=1.2739357721; selected_density=3.006006006 | PF>=1.30 and density>=3/day and split positive(PF 1.30 이상, 밀도 하루 3 이상, 분할 양수)를 동시에 요구한다. |
| pf_lift_removes_too_many_trades(PF 상승이 거래를 과하게 제거) | pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원) | pf=1.3287468527; density=2.6636636637; trades=887.0 | density gap(밀도 격차) 0.34/day를 복원하되 top_n(상위 N개)과 trade splitting(거래 쪼개기)은 금지한다. |
| short_side_collapse_in_pf_pass_rows(PF 통과 행의 숏 붕괴) | pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원) | shorts=6.0 | short side(숏 방향) 복원은 별도 threshold(임계값)와 session(세션) 제약으로 시험한다. |
| premarket_short_drag(프리마켓 숏 끌림) | us_premarket_cash_open(미국 프리마켓/현금장 초반) short | net=-12.315; pf=0.9150191492; trades=33 | premarket short(프리마켓 숏)은 무조건 복원하지 말고 margin floor(마진 하한)와 함께 제한한다. |

## Next Queue(다음 대기열)

| queue_id | seed_variant_id | density_gap_to_3day | pf_anchor | density_restore_budget | forbidden(금지) |
| --- | --- | --- | --- | --- | --- |
| control_replay_density_anchor(대조 재생 밀도 기준점) | selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8 | 0.0 | 1.2739357721 | 0.0 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| pfpass_core_short_restore_budget_010(PF통과 핵심 숏 0.10 복원) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 0.3363363363 | 1.3287468527 | 0.1 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| pfpass_core_short_restore_budget_020(PF통과 핵심 숏 0.20 복원) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 0.3363363363 | 1.3287468527 | 0.2 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| pfpass_late_long_density_patch(PF통과 후반 롱 밀도 패치) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 0.3363363363 | 1.3287468527 | 0.16 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| pfpass_non_drag_session_restore(PF통과 비끌림 세션 복원) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 0.3363363363 | 1.3287468527 | 0.24 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| density_anchor_pf_floor_012(밀도 기준 PF 하한 0.12) | selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8 | 0.0 | 1.2739357721 | 0.04 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| density_anchor_hold6_pf_probe(밀도 기준 보유6 PF 탐침) | selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8 | 0.0 | 1.2739357721 | 0.0 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| dd_seed_density_restore_core_late(낙폭 씨앗 핵심후반 밀도 복원) | pfpass_core_plus_premarket_long_restore_PF_통과_핵심_프리마켓_롱_복원__ps0_5__floor0_0__hold8 | 0.3423423423 | 1.2958707973 | 0.29 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| pfpass_validation_balance_patch(PF통과 검증 균형 패치) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 0.3363363363 | 1.3287468527 | 0.18 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| pfpass_month_pocket_observation(PF통과 월 포켓 관찰) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 0.3363363363 | 1.3287468527 | 0.0 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| density_anchor_short0455_edge(밀도 기준 숏0.455 경계) | selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8 | 0.0 | 1.2739357721 | 0.0 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |
| pfpass_guardrail_no_trade_split(PF통과 거래쪼개기 금지 가드) | pfpass_block_premarket_short_restore_density_PF_통과_프리마켓_숏_차단_밀도_복원__ps0_5__floor0_0__hold8 | 0.3363363363 | 1.3287468527 | 0.0 | top_n forbidden(상위 N개 금지); trade_splitting forbidden(거래 쪼개기 금지); OOS threshold selection forbidden(표본외 임계값 선택 금지) |

## Gate Audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/final_decision.json | run364AK proxy review(run364AK 프록시 검토)를 완료했다. |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/input_manifest.csv | run364AJ 산출물과 review queue(검토 대기열)를 확인했다. |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/surface_review.csv | net/PF/density/DD/split/side(순수익/PF/밀도/낙폭/분할/방향)를 함께 검토했다. |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/surface_review.csv | 12개 surface row(표면 행)를 package(패키지) 주장 없이 분류했다. |
| package_boundary_gate(패키지 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/package_gate_audit.csv | strict package row(엄격 패키지 행) 0개라 패키지를 차단했다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/performance_attribution_receipt.json | PF 상승과 density(밀도) 붕괴 원인을 분리했다. |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/run364AL_offensive_queue.csv | run364AL offensive queue(공격 대기열)를 만들었다. |
| data_integrity_gate(데이터 무결성 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/data_integrity_receipt.json | timestamp-safe(시점 안전) review(검토) 경계를 기록했다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/artifact_lineage_receipt.json | 입력/출력 hash(해시)를 연결했다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/claim_boundary_receipt.json | runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않았다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AK/required_gate_coverage_audit.csv | 필수 gate(게이트)를 종료 기록에 연결했다. |

## Claim Boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이번 review(검토)는 package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 열지 않고, run364AL(364AL 실행) 공격 입력만 연다.
