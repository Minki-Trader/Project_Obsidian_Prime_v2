# F84C Required Gate Coverage Audit(F84C 필수 게이트 커버리지 감사)

Status(상태): `completed_mt5_runtime_realized_winrate_materialization_observation_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `materialization_target(물질화 대상)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84c_runtime_realized_winrate_materialization_target_selection.json` | F84B 후보 중 exportable(내보내기 가능) 대상만 MT5로 보낸다. |
| `onnx_probability_parity(온엑스 확률 동등성)` | `3` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/f84c_probability_parity.csv` | Python/ONNX(파이썬/온엑스) 확률 차이를 확인한다. |
| `runtime_signal_veto_parity(런타임 신호 차단 동등성)` | `3` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/f84c_signal_parity.csv` | 선택 진입 시각이 런타임 입력으로 보존되는지 확인한다. |
| `source_reproduction(원천 재현)` | `2` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/f84c_source_reproduction.csv` | F84B proxy(프록시) 선택을 재현한다. |
| `strategy_tester_attempt(전략 테스터 시도)` | `2/2` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84C_mt5_runtime_realized_winrate_materialization_v1/run_manifest.json` | MT5 Strategy Tester(전략 테스터) 출력 여부를 기록한다. |
| `backtest_forensics_receipt(백테스트 포렌식 영수증)` | `recorded(기록됨)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84c_backtest_forensics_receipt.json` | tester identity/report gap(테스터 정체성/보고서 간극)을 분리한다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `recorded(기록됨)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84c_task_force_review_receipt.yaml` | 8명 agent(요원) 검토와 Codex local verification(코덱스 로컬 검증)을 분리한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `mt5_runtime_materialization_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | runtime authority/live readiness(런타임 권위/실거래 준비)를 만들지 않는다. |
