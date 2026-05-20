# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage267_baseline_candidate_racing_protocol_v1`
- current_run(현재 실행): `run267J_stage267_retrained_soft_context_adapter_design_v1`
- active_stage(활성 단계): `267_adapter_research__baseline_candidate_racing_protocol`
- selected_research_baseline(선택 연구 기준선): `none`
- baseline_candidate_pool(기준 후보군): `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s262_lowrank_inner_half_filter`, `s264_allow_inner_all_oos_anchor`, `s258_short_tight_control`
- target_surface(목표 표면): `v2_native_baseline_candidate_racing_research_pool`
- adapter_under_review(검토 중 어댑터): `soft_context_retrain_source_audit_design`
- status(상태): `run267J_retrained_soft_context_adapter_design_completed`
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

## Current Next Action(현재 다음 행동)
- latest_design(최신 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267J_retrained_soft_context_adapter_design.md`.

- next_run(다음 실행): `run267K_audit_retrain_source_and_materialize_soft_context_p0`
- action(행동): run267J(267J 실행)는 run267I(267I 실행)의 점수표 확장 결과를 true retrain(진짜 재학습) 후보로 바로 부르지 않고 source audit(원천 감사), weakness target(약점 목표), stop rule(중단 규칙)로 재설계했다.
- effect(효과): Stage58 이후 이어진 model/source/score-table 연구를 다음 실행에서 확인할 수 있게 만들고, Monday(월요일), July(7월), chron_mid(중간 순서 구간), DD(drawdown, 손실폭)를 명시 게이트로 둔다.
- next_action(다음 행동): `run267K_audit_retrain_source_and_materialize_soft_context_p0`. Effect(효과): 원천 데이터, label(라벨), split(스플릿), feature order(피처 순서)가 확인될 때만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).
Run267I(267I 실행)는 P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토)를 완료했다.
Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭)가 여전히 불편해 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.

Run267J(267J 실행)는 retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계)을 완료했다.
Effect(효과): run267I(267I 실행)의 개선을 선택 후보(selected candidate, 선택 후보)로 올리지 않고, 원천 감사와 짧은 중단 규칙으로 다음 run267K(267K 실행)를 제한한다.
