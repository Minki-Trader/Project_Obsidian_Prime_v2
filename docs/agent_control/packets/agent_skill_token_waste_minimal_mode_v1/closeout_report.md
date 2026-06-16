# Agent/Skill Token Waste Minimal Mode Closeout

## Summary(요약)

This packet(작업 묶음) applies the accepted Grok-reviewed(그록 검토 수용) guidance for reducing unnecessary token/work expansion(토큰/작업 과확장) in AGENTS.md(에이전트 지침), repo-scoped skills(저장소 전용 스킬), routing policy(라우팅 정책), and the Grok wrapper(그록 래퍼).

## What Changed(변경 내용)

- Added small-work minimal mode(작은 작업 최소 모드) and trivial/non-trivial boundary(사소/비사소 경계).
- Added warm-thread delta reentry(따뜻한 스레드 변화분 재진입) guidance.
- Added compact Grok small-review receipt(소규모 그록 검토 압축 영수증).
- Added five-stage retrospective register-first due check(5단계 중간 검토 등록부 우선 도래 점검).
- Added router lite mode(라우터 경량 모드) and `skills_to_read(읽을 스킬)` cap.
- Changed Grok wrapper `--json(JSON 출력)` to summary output(요약 출력), leaving full raw channels(전체 원본 채널) to `--full-json(전체 JSON)` or `raw_diagnostics.json(원본 진단 파일)`.
- Added compact Grok receipt schema/linter support(압축 그록 영수증 스키마/검사 지원) for `review_size=small(소규모 검토)`.

## Claim Boundary(주장 경계)

Allowed(허용): agent policy update applied(에이전트 정책 변경 반영), governance validation passed(거버넌스 검증 통과), pushed to main only after git push succeeds(깃 원격 반영 성공 시 메인 반영).

Forbidden(금지): completion(완성), selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

## Grok Evidence(그록 근거)

- receipt(영수증): `docs/agent_control/grok_reviews/2026-06-16_agent_skill_token_waste_review/receipt.md`
- clean output(정리 출력): `docs/agent_control/grok_reviews/2026-06-16_agent_skill_token_waste_review/clean_output.md`

## Gate Results(게이트 결과)

Gate outputs(게이트 출력)는 이 폴더의 JSON files(JSON 파일)에 기록한다.

- `agent_control_contracts(에이전트 제어 계약)`: pass(통과)
- `ops_instruction_audit(운영 지침 감사)`: pass(통과)
- `work_packet_schema_lint(작업 묶음 스키마 검사)`: pass(통과)
- `skill_receipt_schema_lint(스킬 영수증 스키마 검사)`: pass(통과)
- `pytest(파이테스트)`: 30 passed(30개 통과)
- `py_compile(파이썬 컴파일 검사)`: pass(통과)
- `git diff --check(깃 차이 공백 검사)`: pass(통과)
- scoped Korean encoding validation(범위 한국어 인코딩 검증): pass(통과)

Full `validate_agent_settings(에이전트 설정 검증)`는 historical encoding/mojibake debt(기존 인코딩/문자 깨짐 부채)에서 실패했다. Current patch scope(현재 패치 범위)는 scoped validation(범위 검증)으로 통과했다.
