# Stage267 Selection Status(267단계 선택 상태)

- stage_status(단계 상태): `run267B_historical_2024_mt5_execution_completed_review_pending`
- current_packet(현재 작업 묶음): `stage267_baseline_candidate_racing_protocol_v1`
- current_run(현재 실행): `run267B_stage267_extended_period_ablation_probe_v1`
- last_completed_run(마지막 완료 실행): `run267A_stage267_baseline_candidate_racing_protocol_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- selected_candidate(선택 후보): `none`
- candidate_pool(후보군): `s264_allow_inner_high_quarter;s264_lowrank_control;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor;s258_short_tight_control`
- source_boundary(원천 경계): `research_candidate_pool_only`
- initial_scoreboard(초기 점수판): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_initial_scoreboard.csv`
- racing_gap_report(경주 공백 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_racing_gap_report.md`
- run267B_input_readiness_report(267B 입력 준비 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267B_input_readiness_report.md`
- prior_research_utilization_audit(이전 연구 활용 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_prior_research_utilization_audit.md`
- equity_curve_shape_grading(평가금 곡선 형태 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_equity_curve_shape_grading.csv`
- equity_curve_shape_report(평가금 곡선 형태 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_equity_curve_shape_grading_report.md`
- historical_2024_manifest(2024 과거 압박 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/manifest.json`
- historical_2024_report(2024 과거 압박 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_probe_report.md`
- historical_2024_execution_result(2024 과거 압박 실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/execution_result.json`
- historical_2024_kpi_summary(2024 과거 압박 핵심 성과 지표 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/mt5_kpi_summary.csv`
- historical_2024_backtest_forensics(2024 과거 압박 백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/backtest_forensics.csv`
- historical_2024_mt5_execution_report(2024 MT5 실행 보고): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_mt5_execution_report.md`
- next_action(다음 행동): `run267B_2024_balance_equity_and_time_slice_review`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

Stage267(267단계)는 Baseline candidate pool(기준 후보군)을 racing start line(경주 출발선)으로 둘 뿐, operating baseline(운영 기준선)으로 선택하지 않는다.
Effect(효과): 후보군은 감정이나 과거 기록이 아니라 다음 연구에 실제로 도움이 되는지로 유지, 탈락, 갱신된다.

Run267B(267B 실행)는 input readiness(입력 준비), first-pass equity curve shape grading(1차 평가금 곡선 형태 판정), 2024 historical stress input materialization(2024 과거 압박 입력 산출물화), 2024 MT5 Strategy Tester execution(MT5 전략 테스터 실행)을 완료했다.
Effect(효과): 2024 stress(2024 압박) KPI(핵심 성과 지표)는 모두 positive net(양의 순수익)이지만 PF(수익 팩터) 1.02~1.05와 DD(drawdown, 손실폭) 36.68%~40.43%가 불편하므로, 선택 후보(selected candidate, 선택 후보)는 계속 없다.
