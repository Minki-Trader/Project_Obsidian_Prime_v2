# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage267_baseline_candidate_racing_protocol_v1`
- current_run(현재 실행): `run267AC_stage267_noncalendar_state_guard_score_table_materialization_v1`
- active_stage(활성 단계): `267_adapter_research__baseline_candidate_racing_protocol`
- selected_research_baseline(선택 연구 기준선): `none`
- baseline_candidate_pool(기준 후보군): `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s262_lowrank_inner_half_filter`, `s264_allow_inner_all_oos_anchor`, `s258_short_tight_control`
- target_surface(목표 표면): `v2_native_baseline_candidate_racing_research_pool`
- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_score_table_materialization`
- status(상태): `run267AC_noncalendar_state_guard_score_tables_materialized_execution_pending`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

Stage266(266단계)는 실행(run, 실행) 전 계획(planning, 계획) 상태에서 사용자 지정 R&D racing goal(연구개발 경주 목표)에 의해 superseded(대체)되었다.
Effect(효과): `s264_allow_inner_high_quarter`만 좁게 late segment repair(후반 구간 수리)하지 않고, Stage267(267단계)에서 다섯 후보를 같은 연구 기준 후보군(research baseline candidate pool, 연구 기준 후보군)으로 비교한다.

## Stage267 Candidate Pool(267단계 후보군)

- `s264_allow_inner_high_quarter`: challenger(도전자) 후보. OOS(표본외) 회복이 좋지만 validation late segment(검증 후반 구간)와 약한 월을 다시 봐야 한다.
- `s264_lowrank_control`: defensive control(방어 기준) 후보. validation(검증) 안정성을 보는 비교 기준이다.
- `s262_lowrank_inner_half_filter`: validation-heavy(검증 중심) 후보. validation(검증)은 강하지만 OOS(표본외) 확장성을 확인해야 한다.
- `s264_allow_inner_all_oos_anchor`: OOS anchor(표본외 앵커) 후보. OOS(표본외)는 좋지만 validation(검증) 손상이 있다.
- `s258_short_tight_control`: stress challenger(압박 도전자) 후보. OOS(표본외) 숫자는 강하지만 validation(검증)과 DD(drawdown, 손실폭) 위험을 다시 봐야 한다.

## Required Research Direction(필수 연구 방향)

Stage267(267단계) 이후의 R&D racing(연구개발 경주)은 단순 best KPI(최고 핵심 성과 지표) 선택이 아니다.
Effect(효과): 후보가 덜 깨지는지, 넓은 기간과 구간에서 버티는지, Adapter(어댑터) 구조로 확장할 가치가 있는지 본다.

- extended period test(확장 기간 시험): 정규 IS/OOS(표본내/표본외)뿐 아니라 2024년 같은 과거 기간도 본다.
- feature/category ablation(피처/범주 제거): 후보가 특정 feature(피처)에 과의존하는지 본다.
- similar feature replacement(유사 피처 대체): ADX(ADX) 같은 의미 축을 비슷한 지표로 바꿔도 버티는지 본다.
- feature engineering(피처 엔지니어링): 새 feature(피처), 조합, 변환, 구간화를 만들되 미세 튜닝 루프는 금지한다.
- time-slice KPI(시간 구간 핵심 성과 지표): 요일, 세션, 시간, 월, 후반 구간, OOS final month(표본외 마지막 달)를 따로 본다.
- balance/equity curve(잔액/평가금 곡선): 숫자보다 먼저 그래프가 지저분한지 본다.
- trade quality(거래 품질): trade count(거래 수), net profit(순수익), PF(수익 팩터), DD(손실폭), recovery(회복), expectancy(기대값)를 같이 본다.
- failure memory(실패 기억): 실패한 실험도 버리지 않고 반복 금지 또는 재개 조건을 남긴다.

## Latest Durable Evidence(최신 지속 근거)

- Stage258(258단계) evidence(근거): `stages/258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff/03_reviews/`
- Stage262(262단계) evidence(근거): `stages/262_adapter_research__lowrank_lowedge_oos_recovery_repair/03_reviews/`
- Stage264(264단계) evidence(근거): `stages/264_adapter_research__dual_objective_lowrank_lowedge_repair/03_reviews/`
- Stage265(265단계) review(검토): `stages/265_adapter_research__stage264_dual_objective_followup_review/03_reviews/`
- Stage266(266단계) status(상태): planning_superseded_before_run(실행 전 계획 대체)
- Stage267(267단계) initial scoreboard(초기 점수판): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_initial_scoreboard.csv`
- Stage267(267단계) monthly weakness matrix(월별 약점 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_monthly_weakness_matrix.csv`
- Stage267(267단계) segment weakness matrix(구간 약점 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_segment_weakness_matrix.csv`
- Stage267(267단계) racing gap report(경주 공백 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_racing_gap_report.md`
- Stage267(267단계) run267B input readiness report(267B 입력 준비 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267B_input_readiness_report.md`
- Stage267(267단계) prior research utilization audit(이전 연구 활용 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_prior_research_utilization_audit.md`
- Stage267(267단계) equity curve shape grading(평가금 곡선 형태 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_equity_curve_shape_grading.csv`
- Stage267(267단계) equity curve shape report(평가금 곡선 형태 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_equity_curve_shape_grading_report.md`
- Stage267(267단계) historical 2024 manifest(2024 과거 압박 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/manifest.json`
- Stage267(267단계) historical 2024 feature manifest(2024 피처 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/features.csv`
- Stage267(267단계) historical 2024 report(2024 과거 압박 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_probe_report.md`
- Stage267(267단계) historical 2024 execution result(2024 과거 압박 실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/execution_result.json`
- Stage267(267단계) historical 2024 KPI summary(2024 과거 압박 핵심 성과 지표 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/mt5_kpi_summary.csv`
- Stage267(267단계) historical 2024 backtest forensics(2024 과거 압박 백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/backtest_forensics.csv`
- Stage267(267단계) historical 2024 MT5 execution report(MT5 실행 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_mt5_execution_report.md`
- Stage267(267단계) historical 2024 trade records(2024 과거 압박 거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/trade_records.csv`
- Stage267(267단계) historical 2024 time-slice KPI(2024 과거 압박 시간 구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/time_slice_kpi.csv`
- Stage267(267단계) historical 2024 balance curve diagnostics(2024 과거 압박 잔액 곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/balance_curve_diagnostics.csv`
- Stage267(267단계) historical 2024 candidate weakness summary(2024 과거 압박 후보 약점 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/candidate_weakness_summary.csv`
- Stage267(267단계) historical 2024 balance/time-slice review(2024 과거 압박 잔액/시간 구간 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_balance_time_slice_review.md`
- Stage267(267단계) historical 2024 visual ablation design(2024 시각/제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_visual_ablation_design_report.md`
- Stage267(267단계) run267C weak-slice counterfactual triage(약점 구간 반사실 선별): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_weak_slice_counterfactual_triage_report.md`
- Stage267(267단계) run267C P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_materialization_report.md`
- Stage267(267단계) run267C P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_smoke_execution_report.md`
- Stage267(267단계) run267C P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_full_batch_review.md`
- Stage267(267단계) run267C P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_materialization_report.md`
- Stage267(267단계) run267C P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md`
- Stage267(267단계) run267C P1 soft-axis follow-up review(P1 부드러운 축 후속 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_review.md`
- Stage267(267단계) run267C P1 axis selection(P1 축 선택): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_axis_selection_report.md`
- Stage267(267단계) run267D Adapter/P2 materialization(어댑터/2차 대체 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_materialization_report.md`
- Stage267(267단계) run267D Adapter/P2 MT5 execution(어댑터/2차 대체 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_mt5_execution_report.md`
- Stage267(267단계) run267D Adapter/P2 MT5 review(어댑터/2차 대체 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_mt5_review.md`
- Stage267(267단계) run267E Adapter/P2 follow-up materialization(어댑터/2차 대체 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_followup.md`
- Stage267(267단계) run267E atrcomp Monday guard MT5 execution(ATR 압축 월요일 방어 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_execution.md`
- Stage267(267단계) run267E atrcomp Monday guard MT5 review(ATR 압축 월요일 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md`
- Stage267(267단계) run267F atrcomp guard robustness materialization(ATR 압축 방어 견고성 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_materialization.md`
- Stage267(267단계) run267F non-calendar guard MT5 execution(비달력 방어 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_execution.md`
- Stage267(267단계) run267F non-calendar guard MT5 review(비달력 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md`
- Stage267(267단계) run267G ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267G_adx_followup_failure_memory.md`
- Stage267(267단계) run267H soft non-calendar Adapter design(부드러운 비달력 어댑터 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267H_soft_noncalendar_adapter_design.md`
- Stage267(267단계) run267I P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267I_soft_noncalendar_adapter_materialization.md`
- Stage267(267단계) run267I P0 soft non-calendar Adapter MT5 execution(P0 부드러운 비달력 어댑터 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267I_soft_noncalendar_adapter_mt5_execution.md`
- Stage267(267단계) run267I P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267I_soft_noncalendar_adapter_mt5_review.md`
- Stage267(267단계) run267J retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267J_retrained_soft_context_adapter_design.md`
- Stage267(267단계) run267K retrained soft-context Adapter materialization(재학습 부드러운 문맥 어댑터 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267K_retrained_soft_context_adapter_materialization.md`
- Stage267(267단계) run267K retrained soft-context Adapter MT5 execution(재학습 부드러운 문맥 어댑터 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267K_retrained_soft_context_adapter_mt5_execution.md`
- Stage267(267단계) run267K retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267K_retrained_soft_context_adapter_mt5_review.md`
- Stage267(267단계) run267L retrained soft-context follow-up/prune(재학습 부드러운 문맥 후속/가지치기): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267L_retrained_soft_context_followup_or_prune.md`
- Stage267(267단계) run267M pool-wide ablation/replacement design(후보군 전체 제거/대체 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267M_pool_wide_ablation_replacement_design.md`
- Stage267(267단계) run267N pool-wide P0 materialization(후보군 전체 P0 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267N_pool_wide_ablation_replacement_materialization.md`
- Stage267(267단계) run267N pool-wide P0 MT5 execution(후보군 전체 P0 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267N_pool_wide_ablation_replacement_mt5_execution.md`
- Stage267(267단계) run267N pool-wide P0 KPI review(후보군 전체 P0 KPI 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267N_pool_wide_ablation_replacement_kpi_review.md`
- Stage267(267단계) run267O pool-wide balance/time-slice/trade-quality review(후보군 전체 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267O_pool_wide_balance_timeslice_trade_quality_review.md`
- Stage267(267단계) run267P internal feature order confirmation and Adapter design(내부 피처 순서 확인 및 어댑터 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design.md`
- Stage267(267단계) run267Q internal feature order confirmed Adapter materialization(내부 피처 순서 확인 어댑터 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Q_internal_feature_order_confirmed_adapter_materialization.md`
- Stage267(267단계) run267Q internal feature order confirmed Adapter MT5 execution(내부 피처 순서 확인 어댑터 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_execution.md`
- Stage267(267단계) run267Q internal feature order confirmed Adapter MT5 review(내부 피처 순서 확인 어댑터 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_review.md`
- run267R_internal_adapter_stability_followup_or_prune(267R 내부 어댑터 안정성 후속/가지치기): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267R_internal_adapter_stability_followup_or_prune.md`
- run267S_pool_wide_orthogonal_stability_racing_matrix(267S 후보군 전체 직교 안정성 경주 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267S_pool_wide_orthogonal_stability_racing_matrix.md`
- run267T_pool_wide_orthogonal_stability_mt5_attempts(267T 후보군 전체 직교 안정성 MT5 시도): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267T_pool_wide_orthogonal_stability_mt5_attempts.md`
- Stage267(267단계) run267T pool-wide orthogonal stability MT5 execution(후보군 전체 직교 안정성 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267T_pool_wide_orthogonal_stability_mt5_execution.md`
- Stage267(267단계) run267T pool-wide orthogonal stability MT5 review(후보군 전체 직교 안정성 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267T_pool_wide_orthogonal_stability_mt5_review.md`
- run267U_true_internal_feature_ablation_design(267U 진짜 내부 피처 제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267U_true_internal_feature_ablation_design.md`
- run267V_reconstruct_upstream_feature_surface(267V 상류 피처 표면 재구축): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267V_reconstruct_upstream_feature_surface.md`
- Stage267(267단계) run267W true internal ablation score table materialization(진짜 내부 제거 점수표 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267W_true_internal_ablation_score_table_materialization.md`
- Stage267(267단계) run267X true internal ablation score table MT5 execution(진짜 내부 제거 점수표 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267X_true_internal_ablation_score_table_mt5_execution.md`
- Stage267(267단계) run267Y true internal ablation KPI signature review(진짜 내부 제거 KPI 서명 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Y_true_internal_ablation_kpi_signature_review.md`
- Stage267(267단계) run267Z true internal ablation balance/time-slice/trade-quality review(진짜 내부 제거 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Z_true_internal_ablation_balance_timeslice_trade_quality_review.md`
- Stage267(267단계) run267AA true internal ablation follow-up or Adapter design(진짜 내부 제거 후속 또는 어댑터 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AA_true_internal_ablation_followup_or_adapter_design.md`
- Stage267(267단계) run267AB noncalendar weak-slice resilience queue(비달력 약점 구간 견고성 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AB_noncalendar_weak_slice_resilience_queue.md`
- run267AC_noncalendar_state_guard_score_table_materialization(267AC 비달력 상태 방어 점수표 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AC_noncalendar_state_guard_score_table_materialization.md`

## Current Next Action(현재 다음 행동)
- latest_mt5_review(최신 MT5 검토): run267Z(267Z 실행) candidate-test rows(후보-시험 행) `24`, constructive curve rows(건설적 곡선 행) `5`, negative Tier A slices(음수 Tier A 구간) `120`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Z_true_internal_ablation_balance_timeslice_trade_quality_review.md`.
- latest_kpi_review(최신 KPI 검토): unique signatures(고유 서명) `24`, tier duplicate pairs(티어 중복 쌍) `24`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Y_true_internal_ablation_kpi_signature_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `48` of `48`, KPI records(핵심 성과 지표 기록) `48`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267X_true_internal_ablation_score_table_mt5_execution.md`.
- latest_mt5_review(최신 MT5 검토): unique metric signatures(고유 지표 서명) `2`, selected_candidate(선택 후보) `none`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267T_pool_wide_orthogonal_stability_mt5_review.md`.
- latest_design(최신 설계): run267U(267U 실행) true internal feature ablation design(진짜 내부 피처 제거 설계) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267U_true_internal_feature_ablation_design.md`.
- latest_materialization(최신 물질화): run267V(267V 실행) upstream feature surface reconstruction(상류 피처 표면 재구축) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267V_reconstruct_upstream_feature_surface.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `34` of `34`, KPI records(핵심 성과 지표 기록) `34`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267T_pool_wide_orthogonal_stability_mt5_execution.md`.
- latest_design(최신 설계): run267R(267R 실행) internal Adapter follow-up/prune(내부 어댑터 후속/가지치기) report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267R_internal_adapter_stability_followup_or_prune.md`.
- latest_matrix(최신 행렬): run267S(267S 실행) pool-wide orthogonal stability racing matrix(후보군 전체 직교 안정성 경주 행렬) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267S_pool_wide_orthogonal_stability_racing_matrix.md`.
- latest_materialization(최신 물질화): run267T(267T 실행) pool-wide orthogonal stability MT5 attempts(후보군 전체 직교 안정성 MT5 시도) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267T_pool_wide_orthogonal_stability_mt5_attempts.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `8` of `8`, KPI records(핵심 성과 지표 기록) `8`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Q_internal_feature_order_confirmed_adapter_mt5_execution.md`.
- latest_materialization(최신 물질화): run267Q(267Q 실행) variants(변형) `4`, attempts(시도) `8`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267Q_internal_feature_order_confirmed_adapter_materialization.md`.
- latest_design(최신 설계): run267P(267P 실행) internal feature order confirmation and Adapter design(내부 피처 순서 확인 및 어댑터 설계) audit rows(감사 행) `24`, adapter queue rows(어댑터 큐 행) `8`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267P_pool_wide_internal_feature_order_confirmation_and_adapter_design.md`.
- latest_mt5_review(최신 MT5 검토): run267O(267O 실행) candidate-test rows(후보-시험 행) `24`, negative slices(음수 구간) `80`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267O_pool_wide_balance_timeslice_trade_quality_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `48` of `48`, KPI records(핵심 성과 지표 기록) `48`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267N_pool_wide_ablation_replacement_mt5_execution.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `4`, KPI records(핵심 성과 지표 기록) `4`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267K_retrained_soft_context_adapter_mt5_execution.md`.
- latest_mt5_review(최신 MT5 검토): review rows(검토 행) `2`, negative slices(음수 구간) `18`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267K_retrained_soft_context_adapter_mt5_review.md`.
- latest_materialization(최신 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267K_retrained_soft_context_adapter_materialization.md`.
- latest_design(최신 설계): run267L(267L 실행) follow-up/prune(후속/가지치기) report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267L_retrained_soft_context_followup_or_prune.md`.
- latest_design(최신 설계): run267M(267M 실행) pool-wide ablation/replacement design(후보군 전체 제거/대체 설계) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267M_pool_wide_ablation_replacement_design.md`.
- latest_materialization(최신 물질화): run267N(267N 실행) pool-wide P0 materialization(후보군 전체 P0 물질화) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267N_pool_wide_ablation_replacement_materialization.md`.

- next_run(다음 실행): `run267AD_execute_noncalendar_state_guard_score_table_mt5_batch`
- action(행동): run267AC(267AC 실행)는 run267AB(267AB 실행)의 guard queue(방어 큐)를 score table/model/set/ini(점수표/모델/설정/초기화) 묶음으로 만들었다.
- effect(효과): calendar literal filter(달력 직접 필터)를 쓰지 않고, 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 거래/곡선/시간구간 영향을 확인한다.
- next_action(다음 행동): `run267AD_execute_noncalendar_state_guard_score_table_mt5_batch`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).

Run267I(267I 실행)는 P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토)를 완료했다.
Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭)가 여전히 불편해 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.

Run267K(267K 실행)는 retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토)를 완료했다.
Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 좋아졌지만 Monday(월요일), 2024-12 약점과 거래 수 축소가 남았다.

Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 salvage clue(회수 단서)로 가지치기했다.
Effect(효과): 한 후보 수리 루프를 끊고 후보군 전체 검증으로 되돌렸다.

Run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 설계했다.
Effect(효과): 다음 행동을 한 후보 미세 수리가 아니라 후보군 전체 P0 물질화로 전환했다.

Run267N(267N 실행)는 run267M(267M 실행)의 P0 queue(P0 큐)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.
Effect(효과): run267O(267O 실행)의 거래/곡선/시간구간 검토까지 이어졌고, 아직 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 없다.

Run267O(267O 실행)는 run267N(267N 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 단위로 다시 파싱해 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 완료했다.
Run267P(267P 실행)는 run267O(267O 실행)의 강한 단서를 run267N(267N 실행)의 feature order(피처 순서), runtime contract(런타임 계약), materialization boundary(물질화 경계)와 대조해 Adapter design queue(어댑터 설계 큐)와 failure memory(실패 기억)를 만들었다.
Run267Q(267Q 실행)는 run267P(267P 실행)의 P0 Adapter design queue(P0 어댑터 설계 큐)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.
Run267Q(267Q 실행)는 internal feature order confirmed Adapter MT5 review(내부 피처 순서 확인 어댑터 MT5 검토)를 완료했다.
Effect(효과): MT5(MetaTrader 5, 메타트레이더5)에서 run267N(267N 실행) 원천 표면을 재현했지만, 변형 차이가 후보별로 접혀 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.

Run267S(267S 실행)는 다섯 Baseline candidates(기준 후보)의 orthogonal stability racing matrix(직교 안정성 경주 행렬)를 물질화했다.
Effect(효과): Stage58(58단계) 이후 연구가 부분 활용에 그쳤다는 감사를 받아, 후보군 전체를 ablation/replacement(제거/대체), non-calendar weak-slice resilience(비달력 약점 구간 견고성), prune/restore(가지치기/복귀) 축에 다시 올렸다.

Run267T(267T 실행)는 run267S(267S 실행) 행렬에서 MT5(MetaTrader 5, 메타트레이더5) 시도를 물질화했다.
Effect(효과): `17`개 변형과 `34`개 시도를 만들었고, source variant(원천 변형)가 없는 축은 gap register(공백 등록부)에 남겼다.

Run267U(267U 실행)는 Stage58(58단계) 이후 연구 단서가 충분히 활용됐는지 재점검했다.
Effect(효과): run267M/N/O/P/S/T(267M/N/O/P/S/T 실행)가 이전 연구를 후보군 경주로 끌어온 것은 맞지만, run267T(267T 실행)의 접힘 때문에 true internal feature ablation(진짜 내부 피처 제거)까지 활용했다고는 주장하지 않는다.

Run267V(267V 실행)는 Stage56(56단계) 2024 Tier A(티어 A) source frame(원천 프레임)을 재생성해 후보 5개 raw feature surface(원시 피처 표면)를 만들었다.
Effect(효과): proxy adapter variant(대체 어댑터 변형) 반복이 아니라, 다음 run267W(267W 실행)에서 실제 feature order(피처 순서)에 맞는 score table/model(점수표/모델)을 만들 수 있다.

Run267W(267W 실행)는 run267V(267V 실행)의 raw feature surface(원시 피처 표면)를 받아 24개 supervised EBM(지도학습 EBM) score table(점수표)을 물질화했다.
Effect(효과): 다음 run267X(267X 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 진짜 내부 feature ablation/replacement(피처 제거/대체)를 검증할 수 있다.

Run267X(267X 실행)는 run267W(267W 실행)의 true internal ablation score table(진짜 내부 제거 점수표)을 MT5(MetaTrader 5, 메타트레이더5)로 실행했다.
Effect(효과): 이전 proxy adapter(대체 어댑터) 접힘 문제를 실제 feature order(피처 순서) 변화 기반 runtime evidence(런타임 근거)로 다시 볼 수 있다.

Run267Y(267Y 실행)는 run267X(267X 실행)의 KPI signature(KPI 서명)를 검토했다.
Run267Z(267Z 실행)는 run267X(267X 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)로 다시 검토했다.
Effect(효과): run267Y(267Y 실행)의 KPI signature(핵심 성과 지표 서명) 구분력을 곡선과 약한 구간까지 확장했지만, Tier A+B(Tier A+B 합산)는 fallback disabled(대체 비활성) 중복 경계라 selected candidate(선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.
Effect(효과): true internal feature ablation(진짜 내부 피처 제거)은 proxy collapse(대체 접힘)를 벗어났지만, Tier A+B(Tier A+B 합산)는 fallback(대체)이 꺼진 중복 행이라 다음 곡선/시간구간 검토에서 경계를 유지한다.

Run267AA(267AA 실행)는 run267Z(267Z 실행)의 true internal ablation(진짜 내부 제거) 결과를 후속 설계로 정리했다.
Effect(효과): constructive rows(건설적 행) `5`개는 watch(관찰)로만 남기고, selected candidate(선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.

Run267AB(267AB 실행)는 noncalendar weak-slice resilience queue(비달력 약점 구간 견고성 큐)를 물질화했다.
Effect(효과): joined trades(결합 거래) `2363/2365`, ready guard rows(준비 방어 행) `7`를 남겼고, selected candidate(선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.

Run267AC(267AC 실행)는 run267AB(267AB 실행)의 guard queue(방어 큐)를 score table/model(점수표/모델) 입력으로 물질화했다.
Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음 run267AD(267AD 실행)에서 14개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실행해 실제 거래/곡선/시간구간 영향을 확인한다.
