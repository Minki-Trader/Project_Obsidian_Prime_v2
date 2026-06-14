# Frontier30 Required Gate Coverage Audit(전선30 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier30_stage_open/small_review` recorded(기록)
- proxy_gate(프록시 게이트): `frontier30B_train_density_preserving_preselector_before_loss_veto_proxy_scout_v1` produced density/scout/seed/handoff(밀도/탐색/씨앗/인계) `188/5/0/0`
- repair_decision_gate(수리 결정 게이트): `frontier30C_density_preserving_preselector_repair_or_closeout_decision_v1` recorded valid_train_density_repair_opportunity_rows(유효 학습 밀도 수리 기회 행) `0`
- stage_closeout_grok_gate(단계 마감 그록 게이트): retry packet(재시도 묶음) `docs/agent_control/grok_reviews/2026-06-14_frontier30_stage_closeout/small_review_retry` classification(분류) `accepted_retry_after_initial_format_miss`
- closeout_gate(마감 게이트): `preserved_clue_negative_memory(보존 단서+부정 기억)` with report(보고서) `stages/stage_frontier_30__train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_onnx_scout/03_reviews/frontier30D_stage_closeout_density_preserving_preselector_v1_report.md`
- runtime_probe_gate(런타임 탐침 게이트): `runtime_probe_out_of_scope_by_claim_scout_only_no_handoff`
- onnx_gate(ONNX 게이트): `onnx_branch_unattempted_no_handoff_candidate_after_f30c_repair_decision`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier B(티어 B)는 F30B에서 missing_required(필수 누락), Tier A+B(티어 A+B)는 out_of_scope_by_claim(주장 범위 밖)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
