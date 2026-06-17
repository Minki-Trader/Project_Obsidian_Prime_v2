# Required Gate Coverage Audit F78F(F78F 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F78E repair input(F78E 수리 입력) | `passed(통과)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78e_proxy_runtime_gap_analysis.json` |
| entry timing repair(진입 시각 수리) | `applied(적용됨)` | `same_bar_open_runtime_aligned(동일 봉 시가 런타임 정렬)` |
| DD denominator repair(손실폭 분모 수리) | `applied(적용됨)` | `dd_pct_uses_tester_deposit_500(손실폭 퍼센트는 테스터 예치금 500 기준)` |
| proxy KPI contract(프록시 KPI 계약) | `passed(통과)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78f_entry_timing_deposit_repair_proxy_summary.json` |
| data integrity(데이터 무결성) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78f_data_integrity_review.json` |
| model validation(모델 검증) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78f_model_validation_review.json` |
| runtime probe rule(런타임 탐침 규칙) | `required_next(다음 필수)` | `frontier78G_zero_signal_or_negative_repair_closeout_decision_v1` |
| claim guard(주장 보호) | `passed(통과)` | `proxy_repair_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` |

Open status(현재 상태): `entry_timing_deposit_repair_proxy_zero_signal_decision_required_no_authority`

Summary(요약): candidates(후보) `2592`, scout(탐색) `0`, meaningful(의미) `0`.
