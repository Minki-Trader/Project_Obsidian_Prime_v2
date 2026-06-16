# Grok Receipt(그록 영수증): Five-Stage Retrospective Routine(5단계 중간 검토 루틴)

- packet_id(묶음 ID): `five_stage_retrospective_routine_policy_v1`
- skill(스킬): `obsidian-grok-collaboration`
- status(상태): `completed_with_local_classification(로컬 분류 포함 완료)`
- trigger_reason(트리거 이유): user requested a 5-stage Grok retrospective routine(사용자가 5단계마다 Grok 중간 검토 루틴 요청)
- review_size(검토 크기): `medium(중간)`
- direction_before_grok(그록 전 방향): add a durable five-stage retrospective rule(지속 5단계 중간 검토 규칙) with trigger(트리거), scope(범위), evidence row(근거 행), next-open block(다음 개방 차단), and forbidden claims(금지 주장)
- bounded_evidence(제한 근거): AGENTS.md Grok rule(그록 규칙), `docs/policies/frontier_governance.md`, `docs/policies/agent_trigger_policy.md`, `docs/agent_control/work_family_registry.yaml`, `docs/workspace/workspace_state.yaml`, current `/goal(목표)` intent
- prompt_identity(프롬프트 정체성): `docs/agent_control/grok_reviews/2026-06-16_five_stage_retrospective_routine/prompts/prompt.md`, wrapper runtime SHA256(래퍼 실행 해시) `b7a02e3fa675dfe5b202c40bcd7395fca196aaceaf213fbab572b4e90cf8b60e`, current BOM-normalized SHA256(현재 BOM 보정 해시) `cbab4a11c5f1c72e4bc47fb24516be103a9177dce8b7b61a8d1fb005d5d0bf7f`
- grok_output_identity(그록 출력 정체성): `docs/agent_control/grok_reviews/2026-06-16_five_stage_retrospective_routine/outputs/clean_output.md`, current BOM-normalized SHA256(현재 BOM 보정 해시) `30391d0e7681072806c0abcb33920493ad8622240d092915117f4b1fdde43fe5`
- advice_classification(조언 분류): accepted(수용) register/gate/scope/idempotency/evidence schema(등록부/게이트/범위/멱등/근거 스키마); adjusted(조정) fixed large review(고정 대규모 검토); rejected(거절) Grok as primary_skill(그록 주 스킬화)
- local_verification(로컬 검증): `docs/agent_control/grok_reviews/2026-06-16_five_stage_retrospective_routine/local_verification.md`
- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
- final_codex_direction(최종 Codex 방향): adopt five-stage retrospective(5단계 중간 검토)를 trigger overlay(트리거 오버레이), frontier governance(전선 운영), Grok skill(그록 스킬), stage transition guard(단계 전환 가드), and register(등록부)에 반영
