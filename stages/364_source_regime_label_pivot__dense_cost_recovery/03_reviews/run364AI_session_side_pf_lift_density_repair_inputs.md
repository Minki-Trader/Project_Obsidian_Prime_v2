# run364AI session/side PF lift density repair inputs(364AI 세션/방향 PF 상승 밀도 수리 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AI_materialize_session_side_pf_lift_density_repair_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AH_review_pf_lift_density_safe_expansion_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1`
- judgment(판정): `session_side_pf_lift_density_repair_inputs_ready_no_operating_claim`
- parent_selected_variant(부모 선택 변형): `selected_density_safe_control__ps0_45__floor0_0__hold8`
- parent net/PF/density(부모 순수익/수익 팩터/밀도): `840.055` / `1.2739357721` / `3.006006006`
- queue_rows(대기열 행): `12`
- control_rows(대조 행): `2`
- candidate_rows(후보 행): `10`
- top_n_rows(top_n 행): `0`
- trade_splitting_rows(거래 쪼개기 행): `0`
- runtime_authority(런타임 권위): `not_claimed`

## Repair Profile(수리 프로필)

| profile_id | source | net_profit | profit_factor | density | effect(효과) |
| --- | --- | --- | --- | --- | --- |
| selected_density_safe_near_pf(선택 밀도 안전 PF 근접) | selected_density_safe_control__ps0_45__floor0_0__hold8 | 840.055 | 1.2739357721 | 3.006006006 | 밀도는 지키되 PF 목표 미달을 수리 대상으로 고정한다. |
| package_blockers(패키지 차단 원인) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/package_gate_audit.csv |  | density_floor(밀도 하한)=passed; profit_factor_target(PF 목표)=failed; strict_package_rows(엄격 패키지 행)=failed; external_runtime_evidence(외부 런타임 근거)=out_of_scope_by_claim(주장 범위 밖) |  | PF 목표와 엄격 패키지 행 실패를 다음 제약으로 쓴다. |
| core_session_positive(핵심 세션 양수) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/session_side_review.csv | long=622.482; short=102.921 | long=1.316715265; short=1.3122669474 | long=2.1471471471; short=0.2613981763 | 핵심 세션 롱/숏 양수 포켓을 공격 탐색 씨앗으로 쓴다. |
| premarket_short_drag(프리마켓 숏 끌림) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/session_side_review.csv | -12.315 | 0.9150191492 | 0.1044303797 | 프리마켓 숏 차단을 손실 압박 대조로 만든다. |

## Materialized Queue(구체화 대기열)

| queue_rank | queue_id | axis_id | seed_variant_id | materialized_policy | session_policy | side_policy | restore_policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | selected_control_full_session(선택 대조 전체 세션) | control(대조) | selected_density_safe_control__ps0_45__floor0_0__hold8 | baseline_replay(기준 재생) | all_sessions(전체 세션) | all_sides(전체 방향) | none(없음) |
| 2 | block_premarket_short_only(프리마켓 숏만 차단) | session_side_pf_lift(세션 방향 PF 상승) | selected_density_safe_control__ps0_45__floor0_0__hold8 | block_premarket_short(프리마켓 숏 차단) | all_sessions_except_premarket_short(프리마켓 숏 제외 전체) | long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외) | none(없음) |
| 3 | core_plus_premarket_long(핵심 세션 + 프리마켓 롱) | session_side_pf_lift(세션 방향 PF 상승) | selected_density_safe_control__ps0_45__floor0_0__hold8 | core_session_keep_premarket_long(핵심 세션 보존 + 프리마켓 롱) | us_cash_core_plus_premarket_long(미국 현금장 핵심 + 프리마켓 롱) | core_both_sides_premarket_long_only(핵심 양방향 + 프리마켓 롱만) | none(없음) |
| 4 | core_session_only_dual_side(핵심 세션 양방향만) | session_side_pf_lift(세션 방향 PF 상승) | selected_density_safe_control__ps0_45__floor0_0__hold8 | core_session_only(핵심 세션만) | us_cash_core_only(미국 현금장 핵심만) | core_long_and_short(핵심 롱/숏) | none(없음) |
| 5 | core_plus_late_long(핵심 세션 + 후반 롱) | session_density_restore(세션 밀도 복원) | selected_density_safe_control__ps0_45__floor0_0__hold8 | core_session_plus_late_long(핵심 세션 + 후반 롱) | us_cash_core_plus_post_cash_late_long(핵심 + 현금장 후반 롱) | core_both_sides_late_long(핵심 양방향 + 후반 롱) | restore_sparse_late_long_watch(희소 후반 롱 관찰 복원) |
| 6 | pfpass_core_restore(통과 PF 핵심 복원) | pf_pass_density_bridge(PF 통과 밀도 연결) | pfpass_short050_restore_short0475__ps0_5__floor0_0__hold8 | pf_pass_seed_restore_core_session(PF 통과 씨앗 핵심 세션 복원) | us_cash_core_restore(미국 현금장 핵심 복원) | core_both_sides_restore(핵심 양방향 복원) | restore_core_from_selected_density_safe(선택 밀도 안전 후보에서 핵심 세션 복원) |
| 7 | pfpass_core_plus_premarket_long_restore(PF 통과 핵심 + 프리마켓 롱 복원) | pf_pass_density_bridge(PF 통과 밀도 연결) | pf_pass_density_fail_control__ps0_5__floor0_0__hold8 | pf_pass_seed_restore_core_and_premarket_long(PF 통과 씨앗 핵심 및 프리마켓 롱 복원) | us_cash_core_plus_premarket_long(핵심 + 프리마켓 롱) | core_both_sides_premarket_long_only(핵심 양방향 + 프리마켓 롱만) | restore_core_and_premarket_long_from_selected(선택 후보에서 핵심/프리마켓 롱 복원) |
| 8 | pfpass_block_premarket_short_restore_density(PF 통과 프리마켓 숏 차단 밀도 복원) | pf_pass_density_bridge(PF 통과 밀도 연결) | pfpass_short050_restore_margin008__ps0_5__floor0_0__hold8 | pf_pass_seed_block_premarket_short_restore_density(PF 통과 씨앗 프리마켓 숏 차단 밀도 복원) | all_sessions_except_premarket_short(프리마켓 숏 제외 전체) | long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외) | restore_non_drag_sessions_from_selected(선택 후보에서 손실 끌림 외 세션 복원) |
| 9 | selected_short0455_density_edge_recheck(선택 숏 0.455 밀도 경계 재검토) | near_density_bridge(밀도 경계 연결) | selected_short0455_restore_margin010__ps0_455__floor0_0__hold8 | near_density_repair_with_session_guard(밀도 근접 수리 + 세션 가드) | all_sessions_except_premarket_short(프리마켓 숏 제외 전체) | long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외) | recover_density_gap_0_04(밀도 격차 0.04 복원) |
| 10 | validation_pf_repair_selected_split_guard(선택 후보 검증 PF 수리 분할 가드) | split_guardrail(분할 가드레일) | selected_density_safe_control__ps0_45__floor0_0__hold8 | validation_pf_drag_repair_without_oos_selection(표본외 선택 없는 검증 PF 끌림 수리) | all_sessions_with_validation_report(전체 세션, 검증 분리 보고) | all_sides(전체 방향) | validation_loss_segments_as_report_only(검증 손실 세그먼트는 보고 전용) |
| 11 | oos_locked_replay_control(표본외 잠금 재생 대조) | split_guardrail(분할 가드레일) | selected_density_safe_control__ps0_45__floor0_0__hold8 | oos_locked_control_replay(표본외 잠금 대조 재생) | all_sessions(전체 세션) | all_sides(전체 방향) | no_oos_threshold_selection(표본외 임계값 선택 없음) |
| 12 | month_positive_pocket_observation_only(월 양수 포켓 관찰 전용) | market_behavior_observation(시장 현상 관찰) | selected_density_safe_control__ps0_45__floor0_0__hold8 | month_pocket_observation_no_filter(월 포켓 관찰, 필터 아님) | all_sessions(전체 세션) | all_sides(전체 방향) | month_pockets_report_only_not_filter(월 포켓은 보고 전용, 필터 아님) |

## Gate Audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/final_decision.json | run364AI 구체화를 닫음 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/input_manifest.csv | run364AH 검토 산출물을 확인함 |
| queue_materialization_gate(대기열 구체화 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/run364AJ_scout_queue.csv | run364AJ 정찰 대기열을 만듦 |
| topn_absence_gate(top_n 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/run364AJ_scout_queue.csv | top_n 사용 금지를 기록함 |
| trade_splitting_absence_gate(거래 쪼개기 부재 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/run364AJ_scout_queue.csv | 거래 쪼개기 없음 상태를 기록함 |
| data_integrity_audit(데이터 무결성 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/data_integrity_receipt.json | 시점 안전 경계를 기록함 |
| experiment_design_gate(실험 설계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/experiment_design_receipt.json | 다음 프록시 정찰 설계를 기록함 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/performance_attribution_receipt.json | 세션/방향 단서를 연결함 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/artifact_lineage_receipt.json | 입력/출력 해시를 연결함 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/claim_boundary_receipt.json | 운영 승격을 주장하지 않음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AI/required_gate_coverage_audit.csv | 필수 게이트를 종료 기록에 연결함 |

## Claim Boundary(주장 경계)

`research_development_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 materialization(구체화)은 run364AJ(실행364AJ) 프록시 정찰 입력만 만들며, package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
