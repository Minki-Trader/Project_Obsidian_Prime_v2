# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage267_baseline_candidate_racing_protocol_v1`
- current_run(현재 실행): `run267DI_stage267_shared_weakness_breakout_second_followup_or_prune_mt5_execution_v1`
- active_stage(활성 단계): `267_adapter_research__baseline_candidate_racing_protocol`
- selected_research_baseline(선택 연구 기준선): `none`
- baseline_candidate_pool(기준 후보군): `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s262_lowrank_inner_half_filter`, `s264_allow_inner_all_oos_anchor`, `s258_short_tight_control`
- target_surface(목표 표면): `v2_native_baseline_candidate_racing_research_pool`
- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_mt5_execution`
- status(상태): `run267DI_shared_weakness_breakout_second_followup_or_prune_mt5_batch_completed`
- run267CQ_summary(267CQ 요약): run267CP(267CP 실행)의 약한 구간을 feature blueprint(피처 청사진) `5`개, materialization queue(물질화 대기열) `6`개, prune rows(가지치기 행) `4`개로 바꿨다. Effect(효과): s264_lc/s264_aia는 확장 기간 압박, s264_aih는 공격형 공급 확장, s258_stc는 한 번의 고위험 압박으로 분리한다.
- run267CR_summary(267CR 요약): Run267CR(267CR 실행)은 run267CQ(267CQ 실행)의 공유 약점 후속 queue(대기열)를 variants(변형) `7`개와 attempts(시도) `14`개로 물질화했다. Effect(효과): 다음 run267CS(267CS 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 곡선/약점 구간/거래 품질을 검증할 수 있다.
- run267CM_summary(267CM 요약): Run267CM(267CM 실행)은 run267CL(267CL 실행)의 양수 후보를 선택하지 않고, feature blueprint(피처 청사진) `3`개, branch decision(분기 판단) `5`개, materialization queue(물질화 대기열) `4`개, prune row(가지치기 행) `4`개로 바꿨다. Effect(효과): 같은 축 수리 루프는 끊고, 공유 약점 상태 피처와 공격형 s264_aih 분기로 다음 실행을 연다.
- run267CN_summary(267CN 요약): Run267CN(267CN 실행)은 run267CM(267CM 실행)의 공유 약점 돌파 큐를 variants(변형) `6`개, attempts(시도) `12`개, control receipts(대조 영수증) `2`개, guardrail receipts(가드레일 영수증) `2`개로 물질화했다. Effect(효과): 다음 run267CO(267CO 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 곡선/약점 구간/거래 품질을 검증할 수 있다.
- next_action(다음 행동): `run267DJ_review_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality`
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
- run267AD_noncalendar_state_guard_score_table_mt5_execution(267AD 비달력 상태 방어 점수표 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AD_noncalendar_state_guard_score_table_mt5_execution.md`
- run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review(267AE 비달력 상태 방어 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review.md`
- run267AF_noncalendar_state_guard_followup_or_prune_design(267AF 비달력 상태 방어 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AF_noncalendar_state_guard_followup_or_prune_design.md`
- run267AG_noncalendar_state_guard_followup_queue_materialization(267AG 비달력 상태 방어 후속 큐 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AG_noncalendar_state_guard_followup_queue_materialization.md`
- run267AH_noncalendar_state_guard_followup_mt5_execution(267AH 비달력 상태 방어 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AH_noncalendar_state_guard_followup_mt5_execution.md`
- run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review(267AI 비달력 상태 방어 후속 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review.md`
- run267AJ_noncalendar_state_guard_followup_design(267AJ 비달력 상태 방어 후속 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AJ_noncalendar_state_guard_followup_design.md`
- run267AK_noncalendar_state_guard_repair_queue_materialization(267AK 비달력 상태 방어 수리 큐 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AK_noncalendar_state_guard_repair_queue_materialization.md`
- run267AL_noncalendar_state_guard_repair_mt5_execution(267AL 비달력 상태 방어 수리 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AL_noncalendar_state_guard_repair_mt5_execution.md`
- run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review(267AM 비달력 상태 방어 수리 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review.md`
- run267AN_noncalendar_state_guard_repair_followup_or_prune_design(267AN 비달력 상태 방어 수리 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AN_noncalendar_state_guard_repair_followup_or_prune_design.md`
- run267AO_pool_wide_state_feature_engineering_materialization(267AO 후보군 전체 상태 피처 엔지니어링 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AO_pool_wide_state_feature_engineering_materialization.md`
- Stage267(267단계) run267AP pool-wide state feature engineering MT5 execution(후보군 전체 상태 피처 엔지니어링 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AP_pool_wide_state_feature_engineering_mt5_execution.md`
- Stage267(267단계) run267AQ pool-wide state feature engineering balance/time-slice/trade-quality review(후보군 전체 상태 피처 엔지니어링 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AQ_pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review.md`
- Stage267(267단계) run267AR pool-wide state feature engineering follow-up/Adapter branch design(후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch.md`
- run267AS_pool_wide_state_feature_engineering_followup_materialization(267AS 후보군 전체 상태 피처 엔지니어링 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AS_pool_wide_state_feature_engineering_followup_materialization.md`
- run267AT_pool_wide_state_feature_engineering_followup_mt5_execution(267AT 후보군 전체 상태 피처 엔지니어링 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AT_pool_wide_state_feature_engineering_followup_mt5_execution.md`
- run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch(267AV 후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch.md`
- run267AW_pool_wide_state_feature_engineering_second_followup_materialization(267AW 후보군 전체 상태 피처 엔지니어링 2차 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AW_pool_wide_state_feature_engineering_second_followup_materialization.md`
- run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution(267AX 후보군 전체 상태 피처 엔지니어링 2차 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution.md`
- run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review(267AY 후보군 전체 상태 피처 엔지니어링 2차 후속 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review.md`
- run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch(267AZ 후보군 전체 상태 피처 엔지니어링 2차 후속/어댑터 분기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.md`
- run267BA_true_fallback_cross_period_replacement_queue_materialization(267BA 실제 대체/확장 기간/유사 대체 큐 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BA_true_fallback_cross_period_replacement_queue_materialization.md`
- run267BB_cross_period_replacement_ready_subset_review(267BB 확장 기간 대체 부분집합 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BB_cross_period_replacement_ready_subset_review.md`
- run267BC_adjacent_period_replacement_materialization(267BC 인접 기간 대체 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BC_adjacent_period_replacement_materialization.md`
- run267BG_adjacent_period_replacement_fresh_report_mt5_execution(267BG 인접 기간 대체 새 보고서 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BG_adjacent_period_replacement_fresh_report_mt5_execution.md`
- run267BH_aggressive_candidate_pressure_queue(267BH 공격형 후보 압박 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BH_aggressive_candidate_pressure_queue.md`
- run267BI_tester_profile_nobom_handoff_repair(267BI 테스터 프로필 BOM 제거 인계 수리): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BI_tester_profile_nobom_handoff_repair.md`
- run267BJ_aggressive_pressure_first_tranche_materialization(267BJ 공격형 압박 첫 묶음 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BJ_aggressive_pressure_first_tranche_materialization.md`
- run267BK_aggressive_pressure_first_tranche_mt5_execution(267BK 공격형 압박 첫 묶음 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BK_aggressive_pressure_first_tranche_mt5_execution.md`
- run267BL_aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review(267BL 공격형 압박 첫 묶음 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BL_aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review.md`
- run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design(267BM 공격형 압박 2차 묶음/확장 기간 검증 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design.md`
- run267BN_aggressive_second_tranche_cross_period_materialization(267BN 공격형 2차 묶음 확장 기간 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BN_aggressive_second_tranche_cross_period_materialization.md`
- run267BO_aggressive_second_tranche_cross_period_mt5_execution(267BO 공격형 2차 묶음 확장 기간 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BO_aggressive_second_tranche_cross_period_mt5_execution.md`
- run267BP_state_acceleration_zero_trade_gap_classification(267BP 상태 가속 거래 0개 공백 분류): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BP_state_acceleration_zero_trade_gap_classification.md`
- run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality(267BQ 과제약 제거 확장 기간 잔액/시간구간/거래품질): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality.md`
- run267BR_anti_overconstraint_cross_period_followup_or_prune_design(267BR 과제약 제거 확장 기간 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BR_anti_overconstraint_cross_period_followup_or_prune_design.md`
- run267BD_adjacent_period_replacement_mt5_execution(267BD 인접 기간 대체 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BD_adjacent_period_replacement_mt5_execution.md`
- run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review(267AU 후보군 전체 상태 피처 엔지니어링 후속 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review.md`

- latest_design(최신 설계): run267AV(267AV 실행) profile decisions(프로필 결정) `8`, candidate decisions(후보 결정) `5`, queue rows(큐 행) `5`, failure memory(실패 기억) `5`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch.md`.

- latest_design(최신 설계): run267AZ(267AZ 실행) candidate decisions(후보 결정) `5`, queue rows(큐 행) `5`, failure memory(실패 기억) `4`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.md`.

- Stage267(267단계) run267BS(267BS 실행) pool-wide directional/impulse follow-up materialization(후보군 전체 방향/임펄스 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BS_pool_wide_directional_impulse_followup_materialization.md`
- run267BT_pool_wide_directional_impulse_followup_mt5_execution(267BT 후보군 전체 방향/임펄스 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BT_pool_wide_directional_impulse_followup_mt5_execution.md`
- run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review(267BU 후보군 전체 방향/임펄스 후속 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review.md`
- run267BV_directional_impulse_followup_or_prune_design(267BV 방향/임펄스 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BV_directional_impulse_followup_or_prune_design.md`
- run267BW_aggressive_impulse_dd_shape_cross_period_materialization(267BW 공격형 임펄스 손실폭 형태 확장 기간 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BW_aggressive_impulse_dd_shape_cross_period_materialization.md`
- run267BX_aggressive_impulse_dd_shape_cross_period_mt5_execution(267BX 공격형 임펄스 손실폭 형태 확장 기간 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BX_aggressive_impulse_dd_shape_cross_period_mt5_execution.md`
- run267BY_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review(267BY 공격형 임펄스 손실폭 형태 확장 기간 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BY_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review.md`
- run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design(267BZ 공격형 임펄스 손실폭 형태 확장 기간 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design.md`
- run267CA_aggressive_impulse_dd_shape_followup_materialization(267CA 공격형 임펄스 손실폭 형태 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CA_aggressive_impulse_dd_shape_followup_materialization.md`
- run267CB_aggressive_impulse_dd_shape_followup_mt5_execution(267CB 공격형 임펄스 손실폭 형태 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CB_aggressive_impulse_dd_shape_followup_mt5_execution.md`
- run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review(267CC 공격형 임펄스 손실폭 형태 후속 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review.md`
- run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design(267CD 공격형 임펄스 손실폭 형태 후속 가지치기/방향전환 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design.md`
- run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design(267CE 후보군 전체 직교 손실 형태/상태 방향전환 큐 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design.md`
- run267CF_pool_wide_orthogonal_loss_shape_state_materialization(267CF 후보군 전체 직교 손실 형태/상태 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CF_pool_wide_orthogonal_loss_shape_state_materialization.md`
- run267CG_pool_wide_orthogonal_loss_shape_state_mt5_execution(267CG 후보군 전체 직교 손실 형태/상태 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CG_pool_wide_orthogonal_loss_shape_state_mt5_execution.md`
- run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review(267CH 후보군 전체 직교 손실 형태/상태 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review.md`
- run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design(267CI 후보군 전체 직교 손실 형태/상태 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md`
- run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization(267CJ 후보군 전체 직교 손실 형태/상태 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization.md`
- run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution(267CK 후보군 전체 직교 손실 형태/상태 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution.md`
- run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review(267CL 후보군 전체 직교 손실 형태/상태 후속 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review.md`
- run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design(267CM 후보군 전체 직교 손실 형태/상태 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md`
- run267CN_pool_wide_shared_weakness_breakout_materialization(267CN 공유 약점 돌파 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CN_pool_wide_shared_weakness_breakout_materialization.md`
- run267CO_pool_wide_shared_weakness_breakout_mt5_execution(267CO 후보군 전체 공유 약점 돌파 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CO_pool_wide_shared_weakness_breakout_mt5_execution.md`
- run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review(267CP 후보군 전체 공유 약점 돌파 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review.md`
- run267CQ_shared_weakness_breakout_followup_or_prune_design(267CQ 공유 약점 돌파 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CQ_shared_weakness_breakout_followup_or_prune_design.md`
- run267CR_shared_weakness_breakout_followup_materialization(267CR 공유 약점 돌파 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CR_shared_weakness_breakout_followup_materialization.md`
- run267CS_shared_weakness_breakout_followup_mt5_execution(267CS 공유 약점 돌파 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CS_shared_weakness_breakout_followup_mt5_execution.md`
- run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review(267CT 공유 약점 후속 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review.md`
- run267CU_summary(267CU 요약): run267CT(267CT 실행)의 후보 선택 보류 상태를 feature blueprint(피처 청사진) `4`개, materialization queue(물질화 대기열) `6`개, prune rows(가지치기 행) `4`개, failure memory(실패 기억) `4`개로 바꿨다. Effect(효과): state_phase(상태 국면) 확장 기간 압박, s258 redzone(위험 구역) 월요일/DD 압박, explosive shock-state combo(폭발형 충격-상태 조합)를 다음 물질화 대상으로 분리한다.
- run267CU_shared_weakness_breakout_followup_or_prune_design(267CU 공유 약점 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CU_shared_weakness_breakout_followup_or_prune_design.md`
- run267CV_summary(267CV 요약): run267CU(267CU 실행)의 대기열 중 실행 가능한 축을 variants(변형) `5`개와 attempts(시도) `10`개로 물질화했다. held queue(보류 대기열)는 `3`개다. Effect(효과): redzone Monday/DD pressure(위험 구역 월요일/손실폭 압박), explosive shock-state combo(폭발형 충격-상태 조합), s264_aih supply repair(s264_aih 공급 수리)를 다음 MT5 실행 입력으로 만들었다.
- run267CV_shared_weakness_breakout_followup_or_prune_materialization(267CV 공유 약점 후속/가지치기 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CV_shared_weakness_breakout_followup_or_prune_materialization.md`
- run267CW_shared_weakness_breakout_followup_or_prune_mt5_execution(267CW 공유 약점 후속/가지치기 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CW_shared_weakness_breakout_followup_or_prune_mt5_execution.md`
- run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review(267CX 공유 약점 후속/가지치기 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review.md`
- run267CY_summary(267CY 요약): run267CX(267CX 실행)의 curve/time-slice/trade-quality(곡선/시간구간/거래품질) 근거를 materialization queue(물질화 대기열) `6`개, prune rows(가지치기 행) `5`개, failure memory(실패 기억) `4`개로 바꿨다. Effect(효과): s258_stc는 확장 기간과 폭발형 압박으로 더 깨뜨려 보고, s264_aih는 마지막 제한 수리 또는 가지치기로 묶고, s264_lc/s262_lih 대조 후보를 다시 붙인다.
- run267CZ_summary(267CZ 요약): run267CY(267CY 실행)의 materialization queue(물질화 대기열)를 variants(변형) `7`개, attempts(시도) `14`개, held rows(보류 행) `2`개로 바꿨다. Effect(효과): 폭발형 2차 생존, s264_aia 검증 손상, s264_aih 최종 공급, s264_lc/s262_lih 대조 재합류를 다음 MT5 실행 입력으로 만들었다.
- run267CY_shared_weakness_breakout_second_followup_or_prune_design(267CY 공유 약점 2차 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CY_shared_weakness_breakout_second_followup_or_prune_design.md`
- run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization(267CZ 공유 약점 2차 후속/가지치기 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization.md`
- run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_execution(267DA 공유 약점 후속/가지치기 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_execution.md`
- run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review(267DB 공유 약점 후속/가지치기 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review.md`
- run267DC_shared_weakness_breakout_second_followup_or_prune_design(267DC 공유 약점 2차 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DC_shared_weakness_breakout_second_followup_or_prune_design.md`
- run267DD_shared_weakness_breakout_second_followup_or_prune_materialization(267DD 공유 약점 2차 후속/가지치기 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DD_shared_weakness_breakout_second_followup_or_prune_materialization.md`
- run267DE_shared_weakness_breakout_second_followup_or_prune_mt5_execution(267DE 공유 약점 후속/가지치기 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DE_shared_weakness_breakout_second_followup_or_prune_mt5_execution.md`
- run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review(267DF 공유 약점 후속/가지치기 잔액/시간구간/거래품질 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review.md`
- run267DG_shared_weakness_breakout_second_followup_or_prune_design(267DG 공유 약점 2차 후속/가지치기 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DG_shared_weakness_breakout_second_followup_or_prune_design.md`
- run267DH_shared_weakness_breakout_second_followup_or_prune_materialization(267DH 공유 약점 2차 후속/가지치기 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DH_shared_weakness_breakout_second_followup_or_prune_materialization.md`
- run267DI_shared_weakness_breakout_second_followup_or_prune_mt5_execution(267DI 공유 약점 후속/가지치기 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DI_shared_weakness_breakout_second_followup_or_prune_mt5_execution.md`
  Effect(효과): run267DH(267DH 실행)의 MT5(MetaTrader 5, 메타트레이더5) attempt(시도) `11/11`개를 실행해 KPI records(KPI 기록) `11`개를 만들었고, selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Current Next Action(현재 다음 행동)
- latest_mt5_execution(최신 MT5 실행): run267DI(267DI 실행) attempts(시도) `11/11`, KPI records(KPI 기록) `11`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DI_shared_weakness_breakout_second_followup_or_prune_mt5_execution.md`.
- latest_materialization(최신 물질화): run267DH(267DH 실행) variants(변형) `7`, attempts(시도) `11`, held_rows(보류 행) `2`, handoff_receipts(인계 영수증) `11`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DH_shared_weakness_breakout_second_followup_or_prune_materialization.md`.
- latest_design(최신 설계): run267DG(267DG 실행) branch_decisions(분기 판단) `5`, materialization_queue(물질화 대기열) `6`, prune_rows(가지치기 행) `6`, failure_memory(실패 기억) `6`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DG_shared_weakness_breakout_second_followup_or_prune_design.md`.
- latest_review(최신 검토): run267DF(267DF 실행) candidate_profile_rows(후보-프로필 행) `5`, negative_slices(음수 구간) `41`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review.md`.
- latest_design(최신 설계): run267DC(267DC 실행) branch_decisions(분기 판단) `5`, materialization_queue(물질화 대기열) `6`, prune_rows(가지치기 행) `5`, failure_memory(실패 기억) `5`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DC_shared_weakness_breakout_second_followup_or_prune_design.md`.
- latest_review(최신 검토): run267DB(267DB 실행) candidate_profile_rows(후보-프로필 행) `7`, negative_slices(음수 구간) `43`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review.md`.
- latest_review(최신 검토): run267CX(267CX 실행) candidate_profile_rows(후보-프로필 행) `5`, negative_slices(음수 구간) `27`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review.md`.
- latest_review(최신 검토): run267CT(267CT 실행) candidate_profile_rows(후보-프로필 행) `7`, negative_slices(음수 구간) `40`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review.md`.
- latest_review(최신 검토): run267CP(267CP 실행) candidate_profile_rows(후보-프로필 행) `6`, negative_slices(음수 구간) `34`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review.md`.
- latest_mt5_review(최신 MT5 검토): run267AY(267AY 실행) trade records(거래 기록) `2234`, candidate-second rows(후보-2차 행) `8`, watch rows(관찰 행) `0`, negative Tier A slices(음수 Tier A 구간) `35`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `8` of `8`, KPI records(KPI 기록) `8`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution.md`.
- latest_mt5_review(최신 MT5 검토): run267AU(267AU 실행) trade records(거래 기록) `4668`, candidate-followup rows(후보-후속 행) `8`, watch rows(관찰 행) `0`, negative Tier A slices(음수 Tier A 구간) `38`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `16` of `16`, KPI records(KPI 기록) `16`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AT_pool_wide_state_feature_engineering_followup_mt5_execution.md`.
- latest_design(최신 설계): run267AR(267AR 실행) profile decisions(프로필 결정) `20`, candidate decisions(후보 결정) `5`, queue rows(큐 행) `5`, failure memory(실패 기억) `8`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch.md`.
- latest_mt5_review(최신 MT5 검토): run267AQ(267AQ 실행) candidate-profile rows(후보-상태프로필 행) `20`, followup watch rows(후속 관찰 행) `0`, negative Tier A slices(음수 Tier A 구간) `99`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AQ_pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `40` of `40`, KPI records(핵심 성과 지표 기록) `40`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AP_pool_wide_state_feature_engineering_mt5_execution.md`.
- latest_design(최신 설계): run267AN(267AN 실행) repair decisions(수리 결정) `2`, queue rows(큐 행) `3`, failure memory(실패 기억) `4`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AN_noncalendar_state_guard_repair_followup_or_prune_design.md`.
- latest_repair_review(최신 수리 검토): run267AM(267AM 실행) trade records(거래 기록) `1160`, candidate-test rows(후보-시험 행) `2`, repair comparisons(수리 비교 행) `2`, negative Tier A slices(음수 Tier A 구간) `9`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `4` of `4`, KPI records(핵심 성과 지표 기록) `4`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AL_noncalendar_state_guard_repair_mt5_execution.md`.
- latest_materialization(최신 물질화): run267AK(267AK 실행) variants(변형) `2`, attempts(시도) `4`, deferred queue(보류 큐) `3`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AK_noncalendar_state_guard_repair_queue_materialization.md`.
- latest_design(최신 설계): run267AJ(267AJ 실행) candidate decisions(후보 결정) `5`, queue rows(큐 행) `4`, failure memory(실패 기억) `5`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AJ_noncalendar_state_guard_followup_design.md`.
- latest_mt5_review(최신 MT5 검토): run267AI(267AI 실행) trade records(거래 기록) `1738`, candidate-test rows(후보-시험 행) `3`, constructive curve rows(건설적 곡선 행) `2`, negative Tier A slices(음수 Tier A 구간) `16`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `6` of `6`, KPI records(KPI 기록) `6`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AH_noncalendar_state_guard_followup_mt5_execution.md`.
- latest_design(최신 설계): run267AF(267AF 실행) candidate decisions(후보 결정) `5`, queue rows(큐 행) `4`, failure memory(실패 기억) `4`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AF_noncalendar_state_guard_followup_or_prune_design.md`.
- latest_mt5_review(최신 MT5 검토): run267AE(267AE 실행) trade records(거래 기록) `4422`, candidate-test rows(후보-시험 행) `7`, constructive curve rows(건설적 곡선 행) `2`, negative Tier A slices(음수 Tier A 구간) `52`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review.md`.
- latest_mt5_execution(최신 MT5 실행): attempts(시도) `14` of `14`, KPI records(KPI 기록) `14`, report(보고서) `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267AD_noncalendar_state_guard_score_table_mt5_execution.md`.
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

- next_run(다음 실행): `run267BT_execute_pool_wide_directional_impulse_followup_mt5_batch`
- action(행동): run267AS(267AS 실행)는 run267AR(267AR 실행)의 후속 큐를 run267AT(267AT 실행) MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력으로 물질화했다.
- effect(효과): 같은 월요일/12월 수리를 직접 달력 필터로 반복하지 않고, 비달력 상태 압박(noncalendar state pressure, 비달력 상태 압박)이 실제 거래/곡선/시간구간을 개선하는지 볼 수 있다.
- next_action(다음 행동): `run267BT_execute_pool_wide_directional_impulse_followup_mt5_batch`

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

Run267AD(267AD 실행)는 run267AC(267AC 실행)의 noncalendar state guard score table(비달력 상태 방어 점수표)을 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)를 얻었지만, 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.

Run267AE(267AE 실행)는 run267AD(267AD 실행)의 noncalendar state guard score table MT5 reports(비달력 상태 방어 점수표 MT5 보고서)를 거래 단위로 다시 읽었다.
Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다음 연구 입력으로 고정한다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AF(267AF 실행)는 run267AE(267AE 실행)의 noncalendar state guard review(비달력 상태 방어 검토)를 후보별 follow-up/prune design(후속/가지치기 설계)로 바꿨다.
Effect(효과): s264_aia는 P0 후속 관찰, s264_lc는 고순익 control audit(방어 기준 감사), s264_aih는 압박 후 downgrade(강등) 경계, s262_lih와 s258_stc는 control/stress boundary(비교/압박 경계)로 분리했다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AG(267AG 실행)는 run267AF(267AF 실행)의 noncalendar state guard follow-up queue(비달력 상태 방어 후속 큐)를 물질화했다.
Effect(효과): s264_aia 2개 replacement(대체) 압박, s264_aih 1개 role pressure(역할 압박), s264_lc control audit(방어 기준 감사)을 분리했고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AH(267AH 실행)는 run267AG(267AG 실행)의 noncalendar state guard follow-up queue(비달력 상태 방어 후속 큐)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)를 얻었지만, 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.

Run267AI(267AI 실행)는 run267AH(267AH 실행)의 noncalendar state guard follow-up MT5 reports(비달력 상태 방어 후속 MT5 보고서)를 거래 단위로 다시 읽었다.
Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다음 연구 입력으로 고정한다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AJ(267AJ 실행)는 run267AI(267AI 실행)의 noncalendar state guard follow-up review(비달력 상태 방어 후속 검토)를 다음 설계로 바꿨다.
Effect(효과): s264_aia는 비달력 상태 guard(상태 방어) 물질화 관찰로 넘기고, s264_aih는 가지치기/수리 경계로 낮췄다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AK(267AK 실행)는 run267AJ(267AJ 실행)의 P0 noncalendar state guard repair queue(비달력 상태 방어 수리 큐)를 물질화했다.
Effect(효과): s264_aia 두 constructive row(건설적 행)는 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력이 되었고, s264_aih는 가지치기 gate(게이트)로 남았다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AL(267AL 실행)은 run267AK(267AK 실행)의 repair attempts(수리 시도)를 MT5(MetaTrader 5, 메타트레이더5) Strategy Tester(전략 테스터)로 실행했다.
Effect(효과): score-table repair(점수표 수리)가 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표) 근거로 이어졌지만, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 주장하지 않는다.

Run267AM(267AM 실행)은 run267AL(267AL 실행)의 repair MT5 reports(수리 MT5 보고서)를 거래 단위로 다시 읽었다.
Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 Monday(월요일), 2024-12(2024년 12월), chron segment(시간 순서 구간), session(세션)을 비교해 다음 설계/가지치기 조건을 만들었다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AN(267AN 실행)은 run267AM(267AM 실행)의 repair review(수리 검토)를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.
Effect(효과): s264_aia의 같은 bounded repair(경계 수리)는 약한 구간 gate(게이트) 미통과로 닫고, 단서는 후보군 전체 state feature engineering(상태 피처 엔지니어링)으로 넘긴다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AO(267AO 실행)는 run267AN(267AN 실행)의 pool-wide state feature engineering queue(후보군 전체 상태 피처 엔지니어링 큐)를 물질화했다.
Effect(효과): 다섯 Baseline candidates(기준 후보)에 네 개 비달력 상태 피처 축을 붙인 20개 variant(변형)와 40개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 없다.

Run267AP(267AP 실행)는 run267AO(267AO 실행)의 state feature engineering(상태 피처 엔지니어링) 입력을 MT5(MetaTrader 5, 메타트레이더5)로 실행했다.
Run267AQ(267AQ 실행)는 run267AP(267AP 실행)의 40개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)로 다시 검토했다.
Run267AR(267AR 실행)는 run267AQ(267AQ 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.
Effect(효과): 높은 headline KPI(대표 핵심 성과 지표)를 바로 선택하지 않고, Monday(월요일), 2024-12(2024년 12월), Tier A+B duplicate boundary(Tier A+B 중복 경계)를 다음 압박 조건으로 만든다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 없다.
Effect(효과): headline KPI(대표 핵심 성과 지표)가 좋아도 월별/요일별/시간대별/세션별/후반 구간에서 깊게 깨지는지 확인할 수 있다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 없다.

Run267AS(267AS 실행)는 run267AR(267AR 실행)의 next experiment queue(다음 실험 큐)를 pool-wide state feature engineering follow-up materialization(후보군 전체 상태 피처 엔지니어링 후속 물질화)으로 바꿨다.
Effect(효과): 8개 variant(변형)와 16개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267AT(267AT 실행)는 run267AS(267AS 실행)의 pool-wide state feature engineering follow-up queue(후보군 전체 상태 피처 엔지니어링 후속 큐)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)를 얻었지만, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 없다.
Next action(다음 행동): `run267AU_review_pool_wide_state_feature_engineering_followup_mt5_results`. Effect(효과): 후보별 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 판정한다.

Run267AU(267AU 실행)는 run267AT(267AT 실행)의 pool-wide state feature engineering follow-up MT5 reports(후보군 전체 상태 피처 엔지니어링 후속 MT5 보고서)를 거래 단위로 다시 읽었다.
Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다음 연구 입력으로 고정했다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267AV(267AV 실행)는 run267AU(267AU 실행)의 후속 검토를 설계 산출물로 바꿨다.
Effect(효과): Stage58(58단계) 이전 연구는 일부 활용됐지만 아직 충분하다고 닫지 않고, 후보군 전체를 2차 비달력 상태 압박(noncalendar state pressure, 비달력 상태 압박), 어댑터 관찰 게이트(Adapter watch gate, 어댑터 관찰 게이트), 실제 Tier B 대체 라우팅(true fallback routing, 실제 대체 라우팅) 공백으로 나눠 다음 실행에 넘긴다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267AW(267AW 실행)는 run267AV(267AV 실행)의 2차 후속 큐를 물질화했다.
Effect(효과): 8개 variant(변형)와 8개 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었고, Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 없어 route gap audit(라우팅 공백 감사)로 막아 두었다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267AX(267AX 실행)는 run267AW(267AW 실행)의 pool-wide state feature engineering second follow-up queue(후보군 전체 상태 피처 엔지니어링 2차 후속 큐)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)를 얻었지만 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 없다.
Next action(다음 행동): `run267AY_review_pool_wide_state_feature_engineering_second_followup_mt5_results`. Effect(효과): 후보별 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 판정한다.

Run267AY(267AY 실행)는 run267AX(267AX 실행)의 second follow-up MT5 reports(2차 후속 MT5 보고서)를 거래 단위로 다시 읽었다.
Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다음 설계 입력으로 고정했다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267AZ(267AZ 실행)는 run267AY(267AY 실행)의 2차 후속 검토를 다음 분기 설계로 바꿨다.
Effect(효과): 같은 state-pressure repair(상태 압박 수리)를 세 번째 반복하지 않고, true fallback routing(실제 대체 라우팅), cross-period check(확장 기간 확인), similar feature replacement(유사 피처 대체), Adapter hold audit(어댑터 보류 감사)로 넓혔다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BA(267BA 실행)는 run267AZ(267AZ 실행)의 다음 큐를 실제 대체/확장 기간/유사 대체 물질화로 나눴다.
Effect(효과): replacement rows(대체 행) `5`개는 다음 실행 후보로 분리했고, true fallback(실제 대체)은 manifest field(목록 필드) 누락으로 차단해 synthetic Tier A+B(합성 Tier A+B)를 routed total(라우팅 전체)로 오해하지 않게 했다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BB(267BB 실행)는 run267BA(267BA 실행)의 replacement subset(대체 부분집합)을 run267Z(267Z 실행) 거래/곡선/구간 근거와 결합했다.
Effect(효과): 5개 replacement rows(대체 행) 중 s264_aia watch pair(관찰 쌍) 2개만 다음 adjacent-period materialization(인접 기간 물질화)로 넘기고, true fallback(실제 대체)은 duplicate Tier A+B(중복 Tier A+B)라 계속 차단했다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BC(267BC 실행)는 run267BB(267BB 실행)의 `s264_aia` watch pair(관찰 쌍)를 adjacent-period(인접 기간) MT5 attempt inputs(MT5 시도 입력)로 물질화했다.
Effect(효과): feature frames(피처 프레임) `6`개와 attempts(시도) `6`개를 만들었지만, MT5 execution(MT5 실행)은 아직 하지 않았으므로 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BD(267BD 실행)은 run267BC(267BC 실행)의 `s264_aia` adjacent-period replacement(인접 기간 대체) attempt(시도) `1/6`개를 MT5(MetaTrader 5, 메타트레이더5)에서 실행 또는 실행 시도했다.
Effect(효과): KPI records(KPI 기록) `0`개를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`로 남긴다.
Next action(다음 행동): `run267BD_repair_s264_aia_adjacent_period_replacement_mt5_execution_blocker`. Effect(효과): KPI(핵심 성과 지표)와 report(보고서)가 없으므로 curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토) 전에 MT5(MetaTrader 5, 메타트레이더5) execution blocker(실행 차단 사유)를 먼저 고친다.
- run267BE_mt5_tester_start_diagnostic(267BE MT5 테스터 시작 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BE_mt5_tester_start_diagnostic.md`

Run267BE(267BE 실행)는 run267BD(267BD 실행)의 MT5 tester start blocker(MT5 테스터 시작 차단)를 별도 진단으로 고정했다.
Effect(효과): q02 feature/model(피처/모델)은 존재하지만 q02와 cached 2024 control(캐시된 2024 대조)이 모두 terminal login(터미널 로그인) 뒤 tester start(테스터 시작)로 넘어가지 않아, 후보 약점(candidate weakness, 후보 약점)이 아니라 외부 MT5 automation state(MT5 자동화 상태) 문제로 경계를 낮춘다.
Next action(다음 행동): `run267BF_repair_mt5_tester_automation_profile_start_before_adjacent_batch`. Effect(효과): adjacent-period replacement(인접 기간 대체) batch(묶음)를 다시 실행하기 전에 tester profile handoff(테스터 프로필 인계)를 먼저 복구한다.
- stage_status(단계 상태): `run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_batch_completed`
- last_completed_run(마지막 완료 실행): `run267CK_stage267_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution_v1`
- run267BF_mt5_tester_unique_report_repair(267BF MT5 테스터 고유 보고서 수리): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BF_mt5_tester_unique_report_repair.md`

Run267BF(267BF 실행)는 run267BE(267BE 실행)의 MT5 tester start blocker(MT5 테스터 시작 차단)를 fresh unique Report(새 고유 보고서) profile(프로필)로 수리 검증했다.
Effect(효과): q02 adjacent-period replacement(q02 인접 기간 대체)가 tester start(테스터 시작), runtime output(런타임 출력), strategy report(전략 보고서)까지 이어졌으므로 다음 batch(묶음)는 fresh report/profile(새 보고서/프로필) 정책으로 다시 실행한다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.

Run267BG(267BG 실행)는 run267BC(267BC 실행)의 `s264_aia` adjacent-period replacement(인접 기간 대체) attempt(시도) `1/6`개를 fresh report/profile(새 보고서/프로필) 정책으로 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): KPI records(KPI 기록) `0`개를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`로 둔다.
Next action(다음 행동): `run267BG_repair_adjacent_period_replacement_fresh_report_mt5_execution_blocker`. Effect(효과): report(보고서)와 KPI(핵심 성과 지표)가 있으면 curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토)로 넘기고, 없으면 MT5(MetaTrader 5, 메타트레이더5) execution blocker(실행 차단 사유)를 먼저 고친다.

Run267BH(267BH 실행)는 updated goal(갱신 목표)에 맞춰 aggressive/폭발형 experiment queue(공격형 실험 큐) `20`개를 물질화했다.
Effect(효과): baseline candidate(기준 후보)를 고르는 과정이 defensive filter stacking(방어 필터 덧붙이기)만 되지 않게 하고, 넓은 허용/손익 비대칭/상호작용 피처/과제약 제거 축을 다음 실행 후보로 만든다.
Next action(다음 행동): `run267BI_repair_tester_handoff_and_execute_aggressive_pressure_queue_tranche`. Effect(효과): MT5(MetaTrader 5, 메타트레이더5) tester handoff(테스터 인계)를 고친 뒤 coarse aggressive tranche(거친 공격형 묶음)를 실행한다.

Run267BI(267BI 실행)는 run267BG(267BG 실행)의 q02 tester handoff(테스터 인계) 차단을 UTF-8 no BOM(UTF-8 BOM 없음) profile(프로필)로 다시 검증했다.
Effect(효과): KPI records(KPI 기록) `1`개를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`로 둔다.
Next action(다음 행동): `run267BJ_materialize_first_aggressive_pressure_tranche_with_nobom_profiles`. Effect(효과): tester handoff(테스터 인계)가 풀리면 aggressive pressure queue(공격형 압박 큐)를 물질화/실행한다.

Run267BJ(267BJ 실행)는 run267BH(267BH 실행)의 s264_aih(핵심 도전자) 공격형 첫 묶음(tranche, 묶음)을 물질화했다.
Effect(효과): 4개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도) 입력을 만들었고, 다음 run267BK(267BK 실행)에서 no-BOM(바이트 순서 표시 없음) profile(프로필)로 실행한다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BK(267BK 실행)는 run267BJ(267BJ 실행)의 공격형 첫 묶음(tranche, 묶음)을 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `4/4`개와 KPI records(KPI 기록) `4`개를 만들었고, 다음은 curve/time-slice/trade quality(곡선/시간구간/거래품질) 검토다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BL(267BL 실행)은 run267BK(267BK 실행)의 aggressive pressure first tranche(공격형 압박 첫 묶음)를 trade list(거래 목록) 단위로 다시 읽었다.
Effect(효과): headline KPI(겉 핵심 성과 지표)만 보지 않고 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다음 연구 입력으로 고정했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BM(267BM 실행)은 run267BL(267BL 실행)의 aggressive pressure first tranche(공격형 압박 첫 묶음) 검토를 받아 2차 묶음과 cross-period validation(확장 기간 검증) 큐를 설계했다.
Effect(효과): anti_overconstraint_prune(과제약 제거)을 바로 선택하지 않고 2023H2/2025H1/2025H2 및 similar replacement(유사 대체)에서 다시 깨뜨려 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BN(267BN 실행)은 run267BM(267BM 실행)의 aggressive second tranche/cross-period queue(공격형 2차 묶음/확장 기간 큐)를 물질화했다.
Effect(효과): 4개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도) 입력을 만들어 run267BO(267BO 실행)에서 2023H2/2025H1/2025H2 기간 압박을 바로 실행할 수 있다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BO(267BO 실행)는 run267BN(267BN 실행)의 공격형 2차 확장 기간 묶음(tranche, 묶음)을 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `4/4`개 중 KPI records(KPI 기록) `3`개를 만들었고, 남은 gap(공백)은 state_acceleration_interaction(상태 가속 상호작용)의 zero-trade/no-runtime-output(거래 0개/런타임 출력 없음) 분류다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BP(267BP 실행)는 run267BO(267BO 실행)의 state_acceleration_interaction(상태 가속 상호작용) 2025H1 zero-trade/runtime gap(거래 0개/런타임 출력 공백)을 분류했다.
Effect(효과): tester report(테스터 보고서)는 완료됐고 trade count(거래 수)는 0이므로, 같은 축을 그대로 재실행하기보다 inactive surface(비활성 표면) 실패 기억으로 남긴다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BQ(267BQ 실행)는 run267BP(267BP 실행)에서 남긴 3개 anti_overconstraint_prune(과제약 제거) 완료 행을 거래 목록(trade list, 거래 목록)으로 다시 읽었다.
Effect(효과): trade records(거래 기록) `812`개, time-slice rows(시간 구간 행) `92`개, negative slices(음수 구간) `18`개를 만들었고, 확장 기간 안정성이 아직 불편함을 기록했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BR(267BR 실행)는 run267BQ(267BQ 실행)의 anti_overconstraint_prune(과제약 제거) 확장 기간 약점을 후속/가지치기 설계로 바꿨다.
Effect(효과): branch decisions(분기 판단) `4`개, followup queue rows(후속 대기열 행) `3`개, failure memory rows(실패 기억 행) `2`개를 만들고, standalone selection(독립 선택)은 낮추되 aggressive impulse branch(공격형 임펄스 분기)를 열었다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BT(267BT 실행)는 run267BS(267BS 실행)의 후보군 전체 방향/임펄스 후속 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `10/10`개 중 KPI records(KPI 기록) `10`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BU(267BU 실행)는 run267BT(267BT 실행)의 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록)로 다시 읽었다.
Effect(효과): trade records(거래 기록) `3574`개, time-slice rows(시간 구간 행) `410`개, negative slices(음수 구간) `80`개를 만들었고, directional_asymmetry(방향 비대칭)는 가지치기, aggressive_impulse_replacement(공격형 임펄스 대체)는 DD(손실폭) 압박 후속으로 넘긴다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BV(267BV 실행)는 run267BU(267BU 실행)의 방향/임펄스 검토를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.
Effect(효과): directional_asymmetry(방향 비대칭)는 독립 분기에서 가지치기하고, aggressive_impulse_replacement(공격형 임펄스 대체)는 DD-shape pressure(손실폭 형태 압박), cross-period(확장 기간), similar replacement(유사 대체)로 넘긴다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BW(267BW 실행)는 run267BV(267BV 실행)의 aggressive impulse cross-period pressure(공격형 임펄스 확장 기간 압박) 큐를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.
Effect(효과): 상위 3개 관찰 후보 x 3개 기간 = `9`개 attempt(시도)를 만들었고, 다음 run267BX(267BX 실행)에서 기간별 PF/DD(수익 팩터/손실폭), curve(곡선), time-slice(시간 구간), trade quality(거래 품질)를 확인할 수 있다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BX(267BX 실행)는 run267BW(267BW 실행)의 aggressive impulse DD-shape cross-period(공격형 임펄스 손실폭 형태 확장 기간) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `9/9`개 중 KPI records(KPI 기록) `9`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BY(267BY 실행)는 run267BX(267BX 실행)의 9개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록)로 다시 읽었다.
Effect(효과): trade records(거래 기록) `1637`개, time-slice rows(시간 구간 행) `294`개, negative slices(음수 구간) `22`개를 만들고 후보별 확장 기간 DD-shape(손실폭 형태)를 다음 설계 입력으로 고정했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267BZ(267BZ 실행)는 run267BY(267BY 실행)의 양수 총합을 바로 선택하지 않고 후속/가지치기 설계로 바꿨다.
Effect(효과): materialization queue(물질화 대기열) `3`개, prune rows(가지치기 행) `3`개, failure memory(실패 기억) `3`개를 만들고 다음 행동을 `run267CA_materialize_aggressive_impulse_dd_shape_followup_queue`으로 고정했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 없다.

Run267CA(267CA 실행)는 run267BZ(267BZ 실행)의 P0 후속 두 개를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.
Effect(효과): materialized attempts(물질화 시도) `2`개, held rows(보류 행) `1`개를 만들고 다음 행동을 `run267CB_execute_aggressive_impulse_dd_shape_followup_mt5_batch`으로 고정했다.
Boundary(경계): 아직 MT5 실행, KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), selected candidate(선택 후보), ONNX readiness(ONNX 준비)는 없다.

Run267CB(267CB 실행)는 run267CA(267CA 실행)의 aggressive impulse DD-shape follow-up(공격형 임펄스 손실폭 형태 후속) P0 attempt(우선순위 0 시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `2/2`개 중 KPI records(KPI 기록) `2`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CC(267CC 실행)는 run267CB(267CB 실행)의 2개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록)로 다시 읽었다.
Effect(효과): trade records(거래 기록) `300`개, time-slice rows(시간 구간 행) `55`개, negative slices(음수 구간) `6`개를 만들고 후보별 후속 DD-shape(손실폭 형태)를 다음 설계 입력으로 고정했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CD(267CD 실행)는 run267CC(267CC 실행)의 양수 후속 결과를 바로 선택하지 않고 prune/pivot design(가지치기/방향전환 설계)으로 바꿨다.
Effect(효과): branch decisions(분기 판단) `5`개, pivot queue(방향전환 대기열) `4`개, prune rows(가지치기 행) `4`개를 만들고 다음 행동을 `run267CE_design_pool_wide_orthogonal_loss_shape_state_pivot_queue`으로 고정했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CE(267CE 실행)는 run267CD(267CD 실행)의 prune/pivot design(가지치기/방향전환 설계)을 후보군 전체 loss-shape/state(손실 형태/상태) 설계 큐로 바꿨다.
Effect(효과): feature blueprints(피처 청사진) `8`개, candidate pivots(후보 방향전환) `5`개, materialization queue(물질화 큐) `6`개를 만들고 다음 행동을 `run267CF_materialize_pool_wide_orthogonal_loss_shape_state_tranche`으로 고정했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CF(267CF 실행)는 run267CE(267CE 실행)의 P0 materialization queue(P0 물질화 큐)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.
Effect(효과): variants(변형) `10`개와 MT5(MetaTrader 5, 메타트레이더5) attempts(시도) `20`개를 만들고 다음 행동을 `run267CG_execute_pool_wide_orthogonal_loss_shape_state_mt5_batch`으로 고정했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CG(267CG 실행)는 run267CF(267CF 실행)의 orthogonal loss-shape/state(직교 손실 형태/상태) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `20/20`개 중 KPI records(KPI 기록) `20`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.
Run267CH(267CH 실행)는 run267CG(267CG 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다. Effect(효과): selected candidate(선택 후보)는 없고, 수익 확장 축과 DD(drawdown, 손실폭) 위험 축을 run267CI(267CI 실행) 후속/가지치기로 넘긴다.
Run267CI(267CI 실행)는 run267CH(267CH 실행)의 curve/time-slice/trade-quality(곡선/시간구간/거래품질) 근거를 branch decisions(분기 판단) `5`개, materialization queue(물질화 대기열) `5`개, prune rows(가지치기 행) `5`개로 바꿨다. Effect(효과): headline net(대표 순수익)으로 후보를 고르지 않고, s264_lc 공격형 통제 후속과 s258_stc 압박 비교 전용 경계를 분리한다.
Run267CJ(267CJ 실행)는 run267CI(267CI 실행)의 materialization queue(물질화 대기열)를 variants(변형) `2`개와 attempts(시도) `4`개, held rows(보류 행) `3`개로 나눴다. Effect(효과): P0 두 후보는 다음 MT5(MetaTrader 5, 메타트레이더5) 실행 입력으로 준비했고, P1/P2는 분석 씨앗과 가지치기 영수증으로 남겨 repair loop(수리 반복)를 짧게 유지한다.

Run267CK(267CK 실행)는 run267CJ(267CJ 실행)의 follow-up(후속) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `4/4`개 중 KPI records(KPI 기록) `4`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.
Run267CL(267CL 실행)는 run267CK(267CK 실행)의 4개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다. Effect(효과): 수익 단서는 보존하되 후보 선택은 보류하고 run267CM(267CM 실행) 후속/가지치기 설계로 넘긴다.

Run267CO(267CO 실행)는 run267CN(267CN 실행)의 shared weakness breakout(공유 약점 돌파) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `12/12`개 중 KPI records(KPI 기록) `12`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CP(267CP 실행)는 run267CO(267CO 실행)의 12개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
Effect(효과): candidate_profile_rows(후보-프로필 행) `6`, negative_slices(음수 구간) `34`를 만들었고, 다음은 follow-up/prune design(후속/가지치기 설계)이다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CQ(267CQ 실행)는 run267CP(267CP 실행)의 후보 선택 보류 상태를 다음 실험 설계로 바꿨다.
Effect(효과): queue(대기열) `6`개 중 P0에는 pool-wide state phase replacement(후보군 전체 상태 국면 대체), lc/aia cross-period pressure(확장 기간 압박), aih aggressive supply expansion(공격형 공급 확장)을 둔다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CS(267CS 실행)은 run267CR(267CR 실행)의 shared weakness follow-up(공유 약점 후속) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `1/14`개 중 KPI records(KPI 기록) `1`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CT(267CT 실행)는 run267CS(267CS 실행)의 14개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
Effect(효과): candidate_profile_rows(후보-프로필 행) `7`, negative_slices(음수 구간) `40`를 만들었고, 다음은 follow-up/prune design(후속/가지치기 설계)이다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CU(267CU 실행)는 run267CT(267CT 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.
Effect(효과): queue(대기열) `6`개 중 P0에는 balanced pair cross-period pressure(균형 쌍 확장 기간 압박), s258 redzone Monday/DD pressure(위험 구역 월요일/DD 압박), explosive shock-state combo(폭발형 충격-상태 조합)를 둔다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CV(267CV 실행)는 run267CU(267CU 실행)의 follow-up/prune queue(후속/가지치기 대기열)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.
Effect(효과): variants(변형) `5`개와 attempts(시도) `10`개를 만들고, cross-period state_phase(확장 기간 상태 구간)와 feature ablation/replacement(피처 제거/대체)는 held(보류)로 기록했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CW(267CW 실행)는 run267CV(267CV 실행)의 shared weakness follow-up/prune(공유 약점 후속/가지치기) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `10/10`개 중 KPI records(KPI 기록) `10`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CX(267CX 실행)는 run267CW(267CW 실행)의 10개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
Effect(효과): candidate_profile_rows(후보-프로필 행) `5`, negative_slices(음수 구간) `27`를 만들었고, 다음은 follow-up/prune design(후속/가지치기 설계)이다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CY(267CY 실행)는 run267CX(267CX 실행)의 잔액/시간구간/거래품질 근거를 2차 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.
Effect(효과): materialization queue(물질화 대기열) `6`개와 prune matrix(가지치기 행렬) `5`개를 만들었고, 폭발형 실험과 control rejoin(대조 재합류)을 같이 열었다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267CZ(267CZ 실행)는 run267CY(267CY 실행)의 2차 follow-up/prune queue(후속/가지치기 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.
Effect(효과): variants(변형) `7`개와 attempts(시도) `14`개를 만들고, q01 cross-period(확장 기간)와 q05 ablation/replacement(제거/대체)는 held(보류)로 남겼다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DA(267DA 실행)는 run267CZ(267CZ 실행)의 shared weakness second follow-up/prune(공유 약점 후속/가지치기) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `14/14`개와 report(보고서) `14/14`개를 완료했고, KPI records(KPI 기록) `14`개를 만들었다. 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DB(267DB 실행)는 run267DA(267DA 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
Effect(효과): candidate_profile_rows(후보-프로필 행) `7`, negative_slices(음수 구간) `43`를 만들었고, 다음은 second follow-up/prune design(2차 후속/가지치기 설계)이다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DC(267DC 실행)는 run267DB(267DB 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 second follow-up/prune design(2차 후속/가지치기 설계)으로 바꿨다.
Effect(효과): branch decisions(분기 판단) `5`, materialization queue(물질화 대기열) `6`, prune matrix(가지치기 행렬) `5`, failure memory(실패 기억) `5`를 만들었다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.
- run267DD_summary(267DD 요약): run267DC(267DC 실행)의 materialization queue(물질화 대기열)를 variants(변형) `8`개, attempts(시도) `13`개, held rows(보류 행) `2`개로 바꿨다. Effect(효과): s258 인접 기간, s264_aia 대체/중립화, s264_aih 파괴 압박, control pair(대조 쌍)를 다음 MT5 실행 입력으로 만들었다.

Run267DD(267DD 실행)는 run267DC(267DC 실행)의 2차 follow-up/prune queue(후속/가지치기 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.
Effect(효과): variants(변형) `8`개와 attempts(시도) `13`개를 만들고, survivor ablation/replacement(생존 후보 제거/대체)는 run267DE/run267DF 이후로 보류했다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DE(267DE 실행)는 run267DD(267DD 실행)의 shared weakness second follow-up/prune(공유 약점 후속/가지치기) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `13/13`개 중 KPI records(KPI 기록) `13`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DF(267DF 실행)는 run267DE(267DE 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
Effect(효과): candidate_profile_rows(후보-프로필 행) `5`, negative_slices(음수 구간) `41`를 만들었고, 다음은 second follow-up/prune design(2차 후속/가지치기 설계)이다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DG(267DG 실행)는 run267DF(267DF 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 second follow-up/prune design(2차 후속/가지치기 설계)으로 바꿨다.
Effect(효과): branch decisions(분기 판단) `5`, materialization queue(물질화 대기열) `6`, prune matrix(가지치기 행렬) `6`, failure memory(실패 기억) `6`를 만들었다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DH(267DH 실행)는 run267DG(267DG 실행)의 materialization queue(물질화 대기열)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.
Effect(효과): variants(변형) `7`개, attempts(시도) `11`개, held rows(보류 행) `2`개, handoff receipts(인계 영수증) `11`개를 만들었다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.

Run267DI(267DI 실행)는 run267DH(267DH 실행)의 shared weakness second follow-up/prune(공유 약점 후속/가지치기) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.
Effect(효과): attempt(시도) `11/11`개 중 KPI records(KPI 기록) `11`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.
