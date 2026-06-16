# F64 Required Gate Coverage Audit(F64 필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_completed(프록시 완료): `frontier64B_loss_cluster_hazard_proxy_scout_v1`
- pre_mt5_grok_review(비싼 MT5 전 그록 검토): `needs_local_verification(로컬 검증 필요)`
- local_handoff_verification(로컬 인계 검증): `blocked_handoff_adapter_mismatch(차단, 인계 어댑터 불일치)`
- capped_handoff_adapter_repair(상한 있는 인계 어댑터 수리): `frontier64D_handoff_adapter_repair_or_block_v1`
- mt5_runtime_probe(MT5 런타임 탐침): `frontier64E_mt5_runtime_probe_loss_cluster_hazard_v1` / `runtime_probe_observation_no_authority`
- proxy_runtime_gap(프록시-런타임 차이): `recorded(기록됨)`
- stage_closeout_grok_review(단계 마감 그록 검토): `accepted_with_root_cause_needs_local_verification(수용, 원인 세부는 로컬 검증 필요)`
- local_verification(로컬 검증): `accepted_negative_memory_with_root_cause_boundary(부정 기억 수용, 원인 경계 낮춤)`
- final_closeout_label(최종 마감 라벨): `negative_memory(부정 기억)`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
