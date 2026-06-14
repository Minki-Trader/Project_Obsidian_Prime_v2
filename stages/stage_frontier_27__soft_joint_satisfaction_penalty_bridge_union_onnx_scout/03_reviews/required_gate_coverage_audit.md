# Frontier27 Required Gate Coverage Audit(전선27 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier27_stage_open/small_review` recorded(기록)
- proxy_gate(프록시 게이트): `frontier27B_soft_joint_satisfaction_penalty_bridge_union_proxy_scout_v1` produced micro/union/scout/seed/handoff(미세/합집합/탐색/씨앗/인계) `80/234/19/0/0`
- repair_decision_gate(수리 결정 게이트): `frontier27C_soft_joint_satisfaction_penalty_repair_or_closeout_decision_v1` recorded repair rejection(수리 거절 기록) `repair_not_run_because_allowed_train_only_filters_found_no_seed_and_heavier_coverage_probe_timed_out(허용된 학습 전용 필터는 씨앗을 찾지 못했고 더 무거운 구성 범위 탐침은 시간 초과되어 수리 미실행)`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier27_stage_closeout/small_review` classification(분류) `accepted_preserved_clue_negative_memory_closeout(수용, 보존 단서+부정 기억 마감)`
- closeout_gate(마감 게이트): `preserved_clue_negative_memory(보존 단서+부정 기억)` with report(보고서) `stages/stage_frontier_27__soft_joint_satisfaction_penalty_bridge_union_onnx_scout/03_reviews/frontier27D_stage_closeout_soft_joint_satisfaction_penalty_v1_report.md`
- runtime_probe_gate(런타임 탐침 게이트): `runtime_probe_ineligible_no_handoff_candidate_after_f27c_repair_decision(F27C 수리 결정 뒤 인계 후보 없어 런타임 탐침 부적격)`
- onnx_gate(ONNX 게이트): `onnx_branch_unattempted_no_handoff_candidate_after_f27c_repair_decision(F27C 수리 결정 뒤 인계 후보 없어 ONNX 미시도)`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
