# Required Gate Coverage Audit F78C(F78C 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F78B proxy evidence(F78B 프록시 근거) | `passed(통과)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78b_contract_proxy_summary.json` |
| pre-MT5 Grok review(사전 MT5 Grok 검토) | `passed(통과)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/grok_pre_mt5_execution_calibrated_negative_control_runtime_probe_receipt.md` |
| bounded evidence(제한 근거) | `passed(통과)` | summary/top100/integrity/validation(요약/상위100/무결성/검증) |
| local export check(로컬 내보내기 확인) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78c_pre_mt5_local_verification.json` |
| materialization target selection(물질화 대상 선택) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78c_runtime_materialization_target_selection.json` |
| advice classification(조언 분류) | `accepted_with_conditions(조건부 수용)` | `docs/agent_control/grok_reviews/2026-06-17_f78c_pre_mt5_execution_calibrated_negative_control_runtime_probe/clean_output.md` |
| runtime probe next(다음 런타임 탐침) | `required(필수)` | `frontier78D_mt5_execution_calibrated_negative_control_runtime_probe_v1` |
| claim guard(주장 보호) | `passed(통과)` | `pre_mt5_review_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` |
