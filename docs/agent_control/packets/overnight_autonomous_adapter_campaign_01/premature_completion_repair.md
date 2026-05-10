# Premature Completion Repair(조기 완료 수정)

- campaign_id(캠페인 ID): `OVERNIGHT-AUTONOMOUS-ADAPTER-CAMPAIGN-01`
- repair_status(수정 상태): `campaign_reopened_after_premature_self_completion`
- active_campaign_judgment(활성 캠페인 판정): `campaign_in_progress_user_review_required_candidate_observed`
- active_mode(활성 모드): `autonomous_candidate_discovery_until_budget_or_blocker`
- active_boundary(활성 경계): `candidate_discovery_only_until_explicit_user_approval`

## Historical Mistake(과거 오판)

이 repair note(수정 노트)는 과거 텍스트를 감사(audit, 감사) 목적으로만 보존한다. 이전 run(실행)은 `campaign_completed_adapter_review_ready`, `reviewed_completed_adapter_review_ready_runtime_probe_only`, `adapter_completed_review_ready`, `completed_adapter_id`, `adapter_completion_packet_path`, `adapter_completion_review_stage53_spf03_block_early_or_trend_buy_v1` 같은 표현을 active state(활성 상태)에 남겼다.

## Corrected Classification(수정된 분류)

Stage53(53단계) `spf03_block_early_or_trend_buy`는 completed adapter(완료 어댑터)가 아니다. 새 상태는 `adapter_candidate_observed_user_review_required`이다. 효과(effect, 효과)는 MT5 evidence(MT5 근거), KPI(KPI), trade density(거래 밀도), concentration(집중도), cost sensitivity(비용 민감도)를 보존하되, campaign stop(캠페인 중단)이나 adapter acceptance(어댑터 수락)로 해석하지 않게 하는 것이다.

## Corrected Rule(수정 규칙)

Codex는 candidate(후보)를 발견, 보존, 순위화, 검토 묶음 작성까지 할 수 있다. Codex는 user approval(사용자 승인) 없이 campaign completion(캠페인 완료), adapter acceptance(어댑터 수락), promotion(승격), baseline(기준선), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)를 선언할 수 없다.

## Repair Commit Recording(수정 커밋 기록)

- repair_commit_sha(수정 커밋 SHA): `pending_repair_commit`
- pushed_main_sha(푸시된 메인 SHA): `pending_repair_push`
- next_stage_after_repair(수정 후 다음 단계): `54`