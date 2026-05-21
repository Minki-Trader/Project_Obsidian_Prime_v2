# Stage267 run267BD Adjacent Period Replacement MT5 Execution(인접 기간 대체 MT5 실행)

## Summary(요약)

- run_id(실행 ID): `run267BD_stage267_adjacent_period_replacement_mt5_execution_v1`
- source_run(원천 실행): `run267BC_stage267_adjacent_period_replacement_frame_materialization_v1`
- status(상태): `run267BD_adjacent_period_replacement_mt5_batch_blocked`
- attempts(시도): `1`
- strategy_reports(전략 테스터 보고서): `0/1`
- kpi_records(KPI 기록): `0`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run267BC(267BC 실행)의 feature frame(피처 프레임)을 MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)과 연결하려고 시도했지만 KPI(핵심 성과 지표)를 회수하지 못했다. 따라서 후보 선택, Adapter(어댑터) 개발, ONNX(온닉스) 검토에는 사용할 수 없다.

## KPI Snapshot(KPI 스냅샷)

- KPI(핵심 성과 지표)를 회수하지 못했다. Effect(효과): 후보 비교나 ONNX(온닉스) 검토에 사용할 수 없다.

## Blocker Evidence(차단 근거)

| attempt(시도) | tester_status(테스터 상태) | blocker(차단 사유) | runtime_status(런타임 상태) | report_status(보고서 상태) |
| --- | --- | --- | --- | --- |
| `adj_s264_aia_rep_trend_strength_adx_adjacent_2025_h1_validation_post_2024` | `blocked` | `terminal_timeout` | `blocked` | `missing` |

## Boundary(경계)

- true fallback(실제 대체): `blocked`; reason(이유): `Tier_B_and_actual_routed_total_blocked_until_true_fallback_route_manifest_exists`.
- actual routed total(실제 라우팅 전체): `not_claimed`.
- Adapter(어댑터): `not_built`; 이 실행은 인접 기간 MT5(MetaTrader 5, 메타트레이더5) 근거 수집이다.
- ONNX parity(ONNX 동등성): `not_started`; 충분한 R&D racing(연구개발 경주) 근거 전에는 진행하지 않는다.
- next_action(다음 행동): `run267BD_repair_s264_aia_adjacent_period_replacement_mt5_execution_blocker`.

## Artifact Lineage(산출물 계보)

- source materialization(원천 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267BC_adjacent_period_replacement_materialization.md`
- execution result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/execution_result.json`
- KPI records(KPI 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/kpi_records.json`
- KPI summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/kpi_summary.csv`
- forensics(포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/backtest_forensics.csv`
- attempts executed(실행된 시도): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BD/adjacent_period_replacement_mt5_execution/attempts_executed.csv`
