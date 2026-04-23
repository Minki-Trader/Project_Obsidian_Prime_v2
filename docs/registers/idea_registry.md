# Idea Registry (아이디어 등록부)

This register tracks exploration ideas (탐색 아이디어) so they can be pursued, closed, archived, or reopened without inheriting legacy code or run results (레거시 코드/런 결과).

| idea_id | origin (출처) | legacy_relation (레거시 관계) | hypothesis (가설) | lane (레인) | tier_scope (티어 범위) | wfo_status (WFO 상태) | status (상태) | salvage_value (회수 가치) | reopen_condition (재개 조건) |
|---|---|---|---|---|---|---|---|---|---|
| `I-001` | v2 exploration mandate setup (v2 탐색 명령 세팅) | `concept_only` (컨셉만) | v2 should inherit the legacy exploration spirit while rejecting direct legacy code/result/promotion inheritance. | `exploration` | `tier_a/tier_b/tier_c_policy` | `policy_default_defined` | `policy_seed` | Separates exploration discipline from operating discipline. | Reopen if future stages again treat promotion-ineligible ideas as worthless. |

## Status Vocabulary (상태 어휘)

- `policy_seed` (정책 씨앗): policy or agent-setting idea, not a model/run idea.
- `active` (활성): currently being explored.
- `paused` (일시 중지): not active, but not closed.
- `archived_negative` (부정 결과 보관): closed with reusable negative evidence.
- `archived_positive` (긍정 결과 보관): useful but not currently promoted.
- `promoted_candidate` (승격 후보): moved to a promotion packet; still not operating truth by itself.

## Use Rule (사용 규칙)

- Register a non-trivial exploration idea before a stage treats it as a durable workstream.
- Keep `legacy_relation` explicit: `none`, `concept_only`, `lesson_only`, or `prior_evidence_only`.
- Do not use this register to import legacy winners, code, or promotion history.
