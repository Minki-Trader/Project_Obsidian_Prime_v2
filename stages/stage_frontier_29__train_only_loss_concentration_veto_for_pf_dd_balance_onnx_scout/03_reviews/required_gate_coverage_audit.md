# Frontier29 Required Gate Coverage Audit(전선29 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier29_stage_open/small_review` recorded(기록)
- proxy_gate(프록시 게이트): `frontier29B_train_only_loss_concentration_veto_proxy_scout_v1` produced selected/density/scout/seed/handoff(선택/밀도/탐색/씨앗/인계) `1438/287/0/0/0`
- repair_decision_gate(수리 결정 게이트): `frontier29C_loss_concentration_veto_repair_or_closeout_decision_v1` recorded valid_train_loss_repair_opportunity_rows(유효 학습 손실 수리 기회 행) `0`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `docs/agent_control/grok_reviews/2026-06-14_frontier29_stage_closeout/small_review` classification(분류) `accepted_with_local_count_reconciliation`
- local_reconciliation_gate(로컬 정합 게이트): stale prompt counts(낡은 프롬프트 수치) `168/177` reconciled to local counts(로컬 수치) `7/11`
- runtime_probe_gate(런타임 탐침 게이트): `runtime_probe_ineligible_no_handoff_candidate_after_f29c_repair_decision`
- onnx_gate(ONNX 게이트): `onnx_branch_unattempted_no_handoff_candidate_after_f29c_repair_decision`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B(티어 A/B/A+B) rows(행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
