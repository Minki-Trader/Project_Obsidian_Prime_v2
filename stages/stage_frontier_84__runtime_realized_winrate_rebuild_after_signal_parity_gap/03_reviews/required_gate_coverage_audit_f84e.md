# F84E Required Gate Coverage Audit(F84E 필수 게이트 커버리지 감사)

Status(상태): `f84e_row_level_deal_reconciliation_completed_proxy_win_runtime_loss_dominant_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `row_level_reconciliation(행 단위 조정)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84e_row_level_reconciliation_rows.csv` | selected entry(선택 진입)마다 proxy/runtime(프록시/런타임)을 붙였다. |
| `normalized_deal_trade_rows(정규화 딜/거래 행)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_v1/f84e_mt5_normalized_deal_rows.csv`, `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/02_runs/frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_v1/f84e_mt5_normalized_trade_rows.csv` | MT5 HTML report(MT5 보고서)를 row evidence(행 근거)로 바꿨다. |
| `ticket_join_policy(티켓 결합 정책)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84e_row_level_reconciliation_split_summary.csv` | time-only join(시간만 결합)보다 ticket(티켓)을 우선했다. |
| `proxy_runtime_confusion(프록시/런타임 혼동표)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84e_row_level_reconciliation_split_summary.csv` | proxy win -> runtime loss(프록시 승리 -> 런타임 손실) 전환을 기록했다. |
| `month_session_streak(월/세션/연패)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84e_month_session_streak_summary.csv` | 붕괴가 어느 시간 묶음에 몰리는지 볼 수 있게 했다. |
| `runtime_parity_boundary(런타임 동등성 경계)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84e_runtime_parity_receipt.yaml` | parity(동등성)를 authority(권위)로 승격하지 않았다. |
| `task_force_actual_calls(태스크포스 실제 호출)` | `passed(통과)` | `stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/f84e_actual_subagent_calls.json` | 8명 agent(요원) 호출을 기록했다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `row_level_reconciliation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | completion/runtime authority/live readiness(완성/런타임 권위/실거래 준비)를 만들지 않았다. |
