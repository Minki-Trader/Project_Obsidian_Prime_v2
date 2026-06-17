# F72B Required Gate Coverage Audit(F72B 필수 게이트 커버리지 감사)

Updated(갱신): 2026-06-17T00:25:32Z

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| stage_open_anchor(단계 개방 고정점) | pass(통과) | `stages/stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling/02_runs/frontier72A_stage_open_new_upstream_axis_after_f71_economics_negative_memory_v1/f72a_label_exit_risk_spec.json` | F72A label/exit/risk spec(라벨/청산/위험 명세)에 연결 |
| proxy_scout_execution(프록시 탐색 실행) | pass(통과) | `stages/stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling/02_runs/frontier72B_trade_shape_exit_distribution_proxy_scout_v1/f72b_candidate_summary.csv` | 후보 KPI 생성 |
| feature_ablation_breadth(피처 묶음 폭) | pass(통과) | `stages/stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling/02_runs/frontier72B_trade_shape_exit_distribution_proxy_scout_v1/f72b_feature_bundle_summary.csv` | 빼기/재조합 반영 |
| tier_pair_record(티어 쌍 기록) | partial_with_missing_required(필수 누락 포함 부분 통과) | `stages/stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling/02_runs/frontier72B_trade_shape_exit_distribution_proxy_scout_v1/f72b_tier_record_status.csv` | Tier B 누락을 숨기지 않음 |
| mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침) | pending_after_proxy(프록시 후 대기) | next action(다음 행동) | proxy-only 주장을 넘지 않음 |
| final_claim_guard(최종 주장 보호) | pass(통과) | `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` | 금지 주장 없음 |
