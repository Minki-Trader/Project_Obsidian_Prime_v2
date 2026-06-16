# Encoding Scope Long Path Validator Fix Receipt(인코딩 범위 긴 경로 검증기 수정 영수증)

- trigger_reason(트리거 이유): systemic issue(시스템성 문제) 발견. F67B deep stage report(F67B 깊은 단계 보고서)는 `io_path(입출력 경로 보조)`로 읽히고 BOM=True(BOM 있음)였지만 scoped validator(범위 검증기)는 `encoding scope path does not exist(인코딩 범위 경로 없음)`로 실패했다.
- review_size(검토 크기): small review(소규모 검토)
- direction_before_grok(그록 전 방향): `check_encoding_scope(인코딩 범위 검사)`를 `io_path(입출력 경로 보조)` 기반 existence/read(존재/읽기)로 바꾸고 regression test(회귀 테스트)를 추가한다.
- bounded_evidence(제한 근거): failing F67B report path(실패한 F67B 보고서 경로), `Path.exists(경로 존재 확인)` 실패, `io_path(입출력 경로 보조)` 읽기 성공, proposed durable fix(제안 장기 수정), risk(위험).
- prompt_identity(프롬프트 정체성): `docs/agent_control/grok_reviews/2026-06-16_encoding_scope_long_path_validator_fix/prompts/prompt.md`, hash(해시) `0c14a3d8074733c1cd57e6374e7bde46e7ddc2ad84f4c4d183b00a60ca184cd8`
- grok_output_identity(그록 출력 정체성): `docs/agent_control/grok_reviews/2026-06-16_encoding_scope_long_path_validator_fix/outputs/clean_output.md`
- advice_classification(조언 분류): accepted(수용) `io_path` file-scope existence/read(파일 범위 존재/읽기), repo-relative identity(저장소 상대 정체성), regression test(회귀 테스트), no gate relaxation(게이트 완화 없음). rejected(거절) validation skip(검증 생략), `\\?\` durable identity(긴 경로 접두사 지속 정체성), git-status waiver(깃 상태 면제). needs_local_verification(로컬 검증 필요) directory traversal(폴더 순회), validator-wide raw exists audit(검증기 전반 원시 존재 확인 감사).
- local_verification(로컬 검증): `io_path(입출력 경로 보조)` returns Path(경로) and supports long-path existence/read/traversal(긴 경로 존재/읽기/순회). Patched validator(검증기 수정) passes F67B scoped encoding validation(범위 인코딩 검증), agent control gates(에이전트 제어 게이트), and `tests/test_validate_agent_settings.py`. Full validator(전체 검증기)는 known historical encoding debt(기존 과거 인코딩 부채)에서 still fails(여전히 실패)하므로 current patch claim(현재 패치 주장)은 scoped pass(범위 통과)로 제한한다.
- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
- final_codex_direction(최종 Codex 방향): keep the fix(수정 유지), keep F67B as observation only(관찰 전용), continue to F67C runtime-native order intent economics(F67C 런타임 기반 주문 의도 경제성).
