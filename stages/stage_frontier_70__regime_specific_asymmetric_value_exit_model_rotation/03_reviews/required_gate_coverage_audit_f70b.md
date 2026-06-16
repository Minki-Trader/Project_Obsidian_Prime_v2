# F70B Required Gate Coverage Audit(F70B 필수 게이트 커버리지 감사)

Updated(갱신): 2026-06-16T21:28:30Z

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| experiment_design(실험 설계) | pass(통과) | `stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/02_runs/frontier70A_stage_open_regime_specific_asymmetric_value_exit_model_rotation_v1/f70a_experiment_design.json` | F70A label-first contract(라벨 우선 계약) 계승 |
| proxy_kpi(프록시 KPI) | pass(통과) | `stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/02_runs/frontier70B_label_regime_asymmetric_value_proxy_scout_v1/f70b_proxy_candidate_summary.csv` | validation/OOS KPI 기록 |
| label_regime_guard(라벨-장세 보호) | pass(통과) | `stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/02_runs/frontier70A_stage_open_regime_specific_asymmetric_value_exit_model_rotation_v1/f70a_axis_contract.csv` | F69 수리 반복 방지 |
| Tier pair(티어 쌍) | partial_with_named_gap(이름 붙인 부분 충족) | `stages/stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation/02_runs/frontier70B_label_regime_asymmetric_value_proxy_scout_v1/f70b_tier_pair_status.csv` | Tier B 누락 숨기지 않음 |
| MT5 runtime probe(MT5 런타임 탐침) | pending_after_meaningful_proxy_or_repair(의미 프록시 또는 수리 후 대기) | proxy-only boundary(프록시 전용 경계) | 런타임 주장은 없음 |

Claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
