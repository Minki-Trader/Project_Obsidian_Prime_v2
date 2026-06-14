# Frontier31 Required Gate Coverage Audit(전선31 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier31_stage_open/small_review` recorded(기록)
- proxy_gate(프록시 게이트): `frontier31B_return_space_exit_shape_proxy_scout_v1` produced density/scout/seed/handoff(밀도/탐색/씨앗/인계) `85/78/62/16`
- repair_decision_gate(수리 결정 게이트): `frontier31C_return_space_exit_shape_repair_or_closeout_decision_v1` recorded mapping_queue_rows(매핑 큐 행) `16` and executable_handoff(실행 가능 인계) `0`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier31_stage_closeout/small_review` classification(분류) `accepted_preserved_clue_closeout`
- closeout_gate(마감 게이트): `preserved_clue_negative_memory(보존 단서+부정 기억)` with report(보고서) `stages/stage_frontier_31__exit_shape_pivot_for_density_preserved_source_scout_pf_lift_onnx_scout/03_reviews/frontier31D_stage_closeout_return_space_exit_shape_v1_report.md`
- runtime_probe_gate(런타임 탐침 게이트): `runtime_probe_out_of_scope_by_claim_return_space_proxy_only_executable_mapping_not_validated`
- onnx_gate(온엑스 게이트): `onnx_branch_unattempted_return_space_proxy_only_no_executable_runtime_mapping`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A(티어 A) proxy(프록시) recorded(기록), Tier B(티어 B) `missing_required` in F31B ledger(전선31B 장부), Tier A+B(티어 A+B) `out_of_scope_by_claim` in F31B ledger(전선31B 장부)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 not_claimed(주장 없음)
