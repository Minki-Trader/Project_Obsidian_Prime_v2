# Stage267 Run267AN Noncalendar State Guard Repair Follow-Up/Prune Design(267단계 267AN 비달력 상태 방어 수리 후속/가지치기 설계)

- action(행동): run267AM(267AM 실행)의 repair review(수리 검토)를 repair branch decision(수리 분기 결정), failure memory(실패 기억), next queue(다음 큐)로 바꿨다.
- effect(효과): 같은 Monday(월요일)/2024-12(2024년 12월) repair(수리)를 반복하지 않고, 넓은 pool-wide state feature engineering(후보군 전체 상태 피처 엔지니어링)으로 전환한다.
- status(상태): `run267AN_noncalendar_state_guard_repair_followup_or_prune_design_completed`
- judgment(판정): `negative_repair_watch_gate_failed_design_completed_no_candidate_selection`
- repair_branch_rows(수리 분기 행): `2`
- candidate_decisions(후보 결정): `5`
- next_queue_rows(다음 큐 행): `3`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AL/run267AM(267AL/267AM 실행)의 수리는 완전 실패는 아니다. DD(drawdown, 손실폭)와 2024-12(2024년 12월)는 조금 나아졌다.
하지만 goal(목표)이 요구하는 기준은 “조금 나아짐”이 아니다. Monday(월요일) 손실과 2024-12 손실이 아직 gate(게이트)를 못 넘었다.
Effect(효과): run267AN(267AN 실행)은 이 repair branch(수리 분기)를 더 끌지 않고, 그 단서를 후보군 전체 feature engineering(피처 엔지니어링)으로 넘긴다.

## Repair Branch Decision(수리 분기 결정)

| source_test_id | repair_net_profit | repair_profit_factor | repair_trade_count | repair_monday_net | repair_december_net | headline_gate | named_weak_slice_gate | repair_branch_decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rep_volatility_atr | 1018.38 | 1.658251 | 290 | -220.0 | -126.58 | pass | fail | close_bounded_repair_branch_salvage_state_guard_clue |
| rep_trend_strength_adx | 1017.11 | 1.594895 | 290 | -263.83 | -135.39 | pass | fail | close_bounded_repair_branch_salvage_state_guard_clue |

## Candidate Decisions(후보 결정)

| candidate_alias | source_coverage | run267AN_decision_label | next_use | prune_boundary |
| --- | --- | --- | --- | --- |
| s264_aih | not_touched_in_run267AM_repair | keep_downgraded_core_role_pressure_boundary | comparison_only_if_pool_wide_feature_engineering_targets_all_candidates | do_not_rescue_by_old_core_challenger_preference |
| s264_lc | not_touched_in_run267AM_repair | preserve_defensive_control_for_pool_wide_queue | defensive_control_in_next_pool_wide_state_feature_engineering_queue | do_not_select_by_high_net_rank_alone |
| s262_lih | not_touched_in_run267AM_repair | preserve_validation_heavy_control_for_pool_wide_queue | validation_heavy_comparison_in_next_pool_wide_queue | do_not_drop_without_same_axis_pool_wide_evidence |
| s264_aia | run267AM_repair_touched | bounded_repair_branch_closed_salvage_only | use_as_state_feature_engineering_clue_against_all_candidates | do_not_run_same_aia_dual_replacement_state_guard_repair_v4 |
| s258_stc | not_touched_in_run267AM_repair | preserve_stress_challenger_boundary_for_pool_wide_queue | stress_boundary_in_next_pool_wide_state_feature_engineering_queue | do_not_treat_OOS_headline_strength_as_ONNX_readiness |

## Next Queue(다음 큐)

| queue_id | priority | materialization_readiness | workstream | candidate_scope | stop_conditions |
| --- | --- | --- | --- | --- | --- |
| run267AO_q01_pool_wide_noncalendar_state_feature_engineering_matrix | P0 | ready_for_design_to_materialization | pool_wide_state_feature_engineering | s264_aih;s264_lc;s262_lih;s264_aia;s258_stc | if_state_feature_engineering_still_fails_named_weak_slices_close_branch_and_pivot_to_new_model_family_or_period_design |
| run267AO_q02_real_tier_b_fallback_probe_after_feature_queue | P1 | deferred_until_q01_has_surviving_rows | real_fallback_routing_gap | surviving_rows_from_q01 | do_not_make_runtime_or_ONNX_claim_before_nonduplicate_routing |
| run267AO_q03_broader_period_pressure_after_state_feature_survival | P1 | deferred_until_q01_survives_2024 | broader_period_pressure | surviving_rows_from_q01 | do_not_advance_to_ONNX_review_before_broader_period_pressure |

## Required Design Fields(필수 설계 필드)

- hypothesis(가설): 새 noncalendar state features(비달력 상태 피처)가 특정 요일/월 필터 없이 반복 약점을 줄일 수 있는지 본다.
- decision_use(결정 용도): 어떤 후보가 Adapter extension watch(어댑터 확장 관찰)로 남을 가치가 있는지 판단한다.
- comparison_baseline(비교 기준): run267O(267O 실행) 후보군 전체 검토와 run267AM(267AM 실행) s264_aia 수리 검토다.
- control_variables(고정 변수): US100 M5, 2024 historical stress(2024 과거 압박), MT5 cost boundary(MT5 비용 경계), 후보군, 금지 주장 경계를 고정한다.
- changed_variables(변경 변수): return shock(수익률 충격), volatility regime(변동성 체제), range expansion(범위 확장), trend-strength disagreement(추세 강도 불일치) 상태 피처다.
- success_criteria(성공 기준): 여러 후보에서 거래 수, PF(수익 팩터), DD(손실폭), Monday/December 약점이 함께 버텨야 한다.
- failure_criteria(실패 기준): 같은 구멍이 남거나 거래 수가 무너지거나 한 후보만 threshold tweak(임계값 미세 조정)으로 살아남으면 실패다.
- invalid_conditions(무효 조건): literal calendar filter(문자 그대로의 달력 필터), feature order(피처 순서) 미추적, Tier A+B 중복을 real routing(실제 라우팅)으로 오해하는 경우다.
- stop_conditions(중단 조건): 이 축도 약한 구간을 못 줄이면 같은 수리 대신 새 model family(모델 계열)나 기간 설계로 전환한다.
- evidence_plan(근거 계획): feature manifest(피처 목록), score table manifest(점수표 목록), attempt manifest(시도 목록), MT5 KPI, balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토), failure memory(실패 기억)를 남긴다.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AN_stage267_noncalendar_state_guard_repair_followup_or_prune_design_v1`.
- evidence_available(사용 근거): run267AM(267AM 실행) comparison rows(비교 행) 2개, candidate-test rows(후보-시험 행) 2개, negative slices(음수 구간) 9개.
- evidence_missing(부족 근거): 새 feature engineering matrix(피처 엔지니어링 행렬), 후보군 전체 MT5 실행, real Tier B fallback(실제 Tier B 대체), broader period pressure(넓은 기간 압박), Adapter extension(어댑터 확장), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `negative_repair_watch_gate_failed_design_completed_no_candidate_selection`.
- claim_boundary(주장 경계): 수리 분기 종료와 다음 설계만 주장한다. 선택 후보, ONNX 준비, 목표 달성은 주장하지 않는다.
- next_condition(다음 조건): `run267AO_materialize_pool_wide_state_feature_engineering_queue`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/review_result.json`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/run267AI_baseline_comparison.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/negative_slice_summary.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AM/noncalendar_state_guard_repair_balance_timeslice_trade_quality_review/tier_duplicate_review.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AN_noncalendar_state_guard_repair_followup_or_prune_design.py`.
- outputs(출력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AN/noncalendar_state_guard_repair_followup_or_prune_design/repair_branch_decision.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AN/noncalendar_state_guard_repair_followup_or_prune_design/candidate_followup_prune_decision.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AN/noncalendar_state_guard_repair_followup_or_prune_design/next_experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AN/noncalendar_state_guard_repair_followup_or_prune_design/failure_memory.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AN/noncalendar_state_guard_repair_followup_or_prune_design/review_result.json`.
- consumer(소비자): `run267AO_materialize_pool_wide_state_feature_engineering_queue`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Boundary(경계)

- positive_claim(긍정 주장): `none`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).
