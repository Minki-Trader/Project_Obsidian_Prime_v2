# Frontier26 Required Gate Coverage Audit(전선26 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier26_stage_open/small_review` recorded(기록)
- proxy_gate(프록시 게이트): `frontier26B_joint_micro_satisfaction_before_bridge_union_proxy_scout_v1` produced pass/attempt/union/density/scout/seed/handoff(통과/시도/합집합/빈도/탐색/씨앗/인계) `3/4/0/0/0/0/0`
- repair_decision_gate(수리 결정 게이트): `frontier26C_joint_micro_satisfaction_repair_or_closeout_decision_v1` recorded repair rejection(수리 거절 기록) `repair_not_run_because_only_threshold_relaxation_could_create_unions(합집합을 만들려면 임계값 완화만 가능하므로 수리 미실행)`
- stage_closeout_grok_gate(단계 마감 그록 게이트): retry packet(재시도 묶음) `docs/agent_control/grok_reviews/2026-06-14_frontier26_stage_closeout/small_review_retry` classification(분류) `accepted_invalid_setup_closeout(수용, 무효 설정 마감)`
- closeout_gate(마감 게이트): `invalid_setup(무효 설정)` with report(보고서) `stages/stage_frontier_26__joint_micro_satisfaction_before_bridge_union_onnx_scout/03_reviews/frontier26D_stage_closeout_joint_micro_satisfaction_v1_report.md`
- runtime_probe_gate(런타임 탐침 게이트): `runtime_probe_ineligible_no_handoff_candidate_after_f26c_invalid_setup_decision(F26C 무효 설정 결정 뒤 인계 후보 없어 런타임 탐침 부적격)`
- onnx_gate(ONNX 게이트): `onnx_branch_unattempted_no_handoff_candidate_after_f26c_invalid_setup_decision(F26C 무효 설정 결정 뒤 인계 후보 없어 ONNX 미시도)`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
