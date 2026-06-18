# F84D Required Gate Coverage Audit(F84D 필수 게이트 커버리지 감사)

Status(상태): `f84d_runtime_gap_attributed_negative_runtime_deal_economics_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `runtime_materialization_evidence(런타임 물질화 근거)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/f84c_runtime_receipt.csv` | F84C Strategy Tester(전략 테스터) 결과를 입력으로 쓴다. |
| `proxy_runtime_gap_analysis(프록시/런타임 간극 분석)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84d_runtime_realized_winrate_gap_analysis_summary.json`, `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84d_runtime_realized_winrate_gap_rows.csv` | split(구간)별 KPI gap(핵심 성과 지표 간극)을 기록한다. |
| `parity_not_cause_boundary(동등성 비원인 경계)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/f84c_probability_parity.csv`, `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/f84c_signal_parity.csv`, `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/f84c_feature_readiness_parity.csv` | parity(동등성)를 주 원인에서 제외한다. |
| `backtest_forensics_receipt(백테스트 포렌식 영수증)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84d_backtest_forensics_receipt.yaml` | tester report(테스터 보고서)와 실행 정체성을 분리한다. |
| `performance_attribution_receipt(성과 귀속 영수증)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84d_performance_attribution_receipt.yaml` | deal economics/win-rate/DD(거래 경제성/승률/손실폭) 붕괴를 귀속한다. |
| `result_judgment_boundary(결과 판정 경계)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84d_result_judgment_receipt.yaml` | negative evidence(부정 근거)와 preserved clue(보존 단서)를 분리한다. |
| `actual_subagent_calls(실제 하위 에이전트 호출)` | `9 calls; roster 8/8` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84d_actual_subagent_calls.json` | Task Force(태스크포스)를 실제 호출 기록과 연결한다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84d_task_force_review_receipt.yaml` | 8명 agent(요원) 검토와 Codex local verification(로컬 검증)을 분리한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `gap_attribution_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | authority/live readiness(권위/실거래 준비)를 만들지 않는다. |
