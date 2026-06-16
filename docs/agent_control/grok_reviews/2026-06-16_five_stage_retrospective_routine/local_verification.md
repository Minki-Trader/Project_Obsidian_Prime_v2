# Five-Stage Retrospective Routine Local Verification(5단계 중간 검토 루틴 로컬 검증)

## Packet Identity(묶음 정체성)

- packet_id(묶음 ID): `five_stage_retrospective_routine_policy_v1`
- review root(검토 루트): `docs/agent_control/grok_reviews/2026-06-16_five_stage_retrospective_routine/`
- prompt path(프롬프트 경로): `docs/agent_control/grok_reviews/2026-06-16_five_stage_retrospective_routine/prompts/prompt.md`
- wrapper output path(래퍼 출력 경로): `docs/agent_control/grok_reviews/2026-06-16_five_stage_retrospective_routine/outputs/clean_output.md`

## Hashes(해시)

- wrapper prompt SHA256 at run time(실행 당시 래퍼 프롬프트 해시): `b7a02e3fa675dfe5b202c40bcd7395fca196aaceaf213fbab572b4e90cf8b60e`
- current prompt SHA256 after UTF-8 BOM normalization(BOM 보정 후 현재 프롬프트 해시): `cbab4a11c5f1c72e4bc47fb24516be103a9177dce8b7b61a8d1fb005d5d0bf7f`
- current clean output SHA256 after UTF-8 BOM normalization(BOM 보정 후 현재 정리 출력 해시): `30391d0e7681072806c0abcb33920493ad8622240d092915117f4b1fdde43fe5`
- metadata SHA256(메타데이터 해시): `eda9095acb273f904afa14325f66a0e534241706485016f4c2fb61f56f8a1720`
- register SHA256 after edit(수정 후 등록부 해시): `b708aead003cf4aaa70c057ca50ba57896a4e19ae5f8ec728a7087956f3fc6be`

## Grok Advice Classification(그록 조언 분류)

Accepted(수용):

- Add a source of truth register(진실 원천 등록부) instead of relying on Codex memory(코덱스 기억).
- Resolve scope(범위)를 numeric `NN-4..NN` alone(숫자만)으로 잡지 않고 actual closeout receipts(실제 마감 영수증) 최근 5개로 잡는다.
- Add next-stage open block(다음 단계 개방 차단) to stage-transition skill(단계 전환 스킬).
- Add idempotency fields(멱등 필드) such as `retrospective_packet_id(중간 검토 묶음 ID)` and `covered_stage_ids(검토 단계 ID)`.
- Add per-stage row schema(단계별 행 스키마), incomplete block rule(불완전 블록 규칙), and claim boundary header(주장 경계 머리말).

Adjusted(조정):

- Grok suggested making the retrospective a fixed large review(대규모 검토). Codex kept review size(검토 크기) governed by the existing Grok review-size policy(기존 그록 검토 크기 정책), because a compact five-stage block can be medium review(중간 검토) when evidence is bounded.

Rejected(거절):

- Grok suggested a special packet entry with `obsidian-grok-collaboration` as primary_skill(주 스킬). Codex rejected this because `docs/agent_control/work_family_registry.yaml` requires one primary family(주 작업군) by work type(작업 성격), and Grok is a trigger overlay(트리거 오버레이), not a new work family(작업군).

Needs local verification(로컬 검증 필요):

- The first due block after adoption should be verified at actual stage transition(단계 전환) time. Current register state is `not_due(아직 아님)` and points to next numeric trigger frontier(다음 숫자 트리거 전선) 70.

## Final Codex Direction(최종 Codex 방향)

The routine is adopted as a durable governance rule(지속 운영 규칙). It can change next-stage direction(다음 단계 방향) or repair priority(수리 우선순위), but cannot create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Post-Implementation Audit(구현 후 감사)

Passed(통과):

- `python -m foundation.control_plane.agent_control_contracts --root .`
- `python -m foundation.control_plane.ops_instruction_audit --root .`
- `python -m pytest tests/test_agent_control_contracts.py tests/test_ops_instruction_audit.py tests/test_skill_receipt_schema_lint.py tests/test_work_packet_schema_lint.py` -> 19 passed(19개 통과)
- scoped changed-file BOM/mojibake check(변경 파일 범위 BOM/문자 깨짐 검사) -> passed(통과)

Failed with pre-existing debt(기존 부채로 실패):

- `python .agents/skills/obsidian-architecture-guard/scripts/validate_agent_settings.py --repo-root .`
- Cause(원인): legacy Grok archive(이전 그록 보관), old decisions(이전 결정), and legacy stages(이전 단계)에 이미 있던 BOM/mojibake/repeated-BOM debt(BOM/문자 깨짐/반복 BOM 부채)를 full-repo scan(전체 저장소 검사)이 잡았다.
- Boundary(경계): this routine's changed markdown files(이번 루틴 변경 마크다운 파일)는 scoped check(범위 검사)로 clean(정상)이다. Full historical cleanup(전체 과거 정리)은 separate repair packet(별도 수리 묶음)이 필요하다.

Durable fix added(지속 수정 추가):

- Added `--encoding-scope` to `.agents/skills/obsidian-architecture-guard/scripts/validate_agent_settings.py`.
- Added `tests/test_validate_agent_settings.py` so scoped encoding validation(범위 인코딩 검증)이 BOM-present Korean docs(BOM 있는 한국어 문서)는 통과시키고 BOM-missing Korean docs(BOM 없는 한국어 문서)는 실패시킨다.
- Updated `.agents/skills/obsidian-architecture-guard/SKILL.md` to require recording both full validator(전체 검증기) and scoped validator(범위 검증기) results when historical backlog(과거 백로그)가 full scan(전체 검사)을 실패시킨다.
- Repaired existing mojibake(기존 문자 깨짐) lines in `docs/workspace/changelog.md`, because that file was touched by this packet(작업 묶음).
- Scoped validator command(범위 검증 명령): `python .agents/skills/obsidian-architecture-guard/scripts/validate_agent_settings.py --repo-root . --encoding-scope <changed-path>` passed(통과).
