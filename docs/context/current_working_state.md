# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage267_baseline_candidate_racing_protocol_v1`
- current_run(현재 실행): `run267C_stage267_execute_prioritized_ablation_replacement_variants_v1`
- active_stage(활성 단계): `267_adapter_research__baseline_candidate_racing_protocol`
- selected_research_baseline(선택 연구 기준선): `none`
- baseline_candidate_pool(기준 후보군): `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s262_lowrank_inner_half_filter`, `s264_allow_inner_all_oos_anchor`, `s258_short_tight_control`
- target_surface(목표 표면): `v2_native_baseline_candidate_racing_research_pool`
- adapter_under_review(검토 중 어댑터): `none_pool_level_racing_protocol`
- status(상태): `stage267_run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending`
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

## Current Next Action(현재 다음 행동)

- next_run(다음 실행): `run267C_stage267_execute_prioritized_ablation_replacement_variants_v1`
- action(행동): run267B(267B 실행) 2024 routed trade records(라우팅 거래 기록)로 weak-slice counterfactual triage(약점 구간 반사실 선별)를 실행했다.
- effect(효과): naive filter(단순 필터)로 좋아 보이는 축과 trade count collapse(거래 수 붕괴)를 일으키는 축을 분리해, 다음 MT5 variant(MT5 변형) 물질화 우선순위를 좁혔다.
- next_action(다음 행동): `run267C_materialize_p0_mt5_variants_from_counterfactual_triage`. Effect(효과): counterfactual(반사실)로 좁힌 P0(우선순위 0) 축을 실제 MT5 rerun(MT5 재실행) 후보로 만든다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).
