# Codex Local Verification(Codex 로컬 검증)

Created(생성): 2026-06-12

## Accepted(수용)

- Grok의 core advice(핵심 조언)는 accepted(수용)한다: future Grok usage(향후 Grok 사용)는 external reviewer mode(외부 검토자 모드), compact prompts(압축 프롬프트), packet records(묶음 기록), and Codex verification(Codex 검증)을 기본값으로 해야 한다.
- Wrapper script(래퍼 스크립트)는 필요하다. 현재 관찰된 실패는 수동 운영으로 계속 처리하기 어렵다:
  - `--prompt-file` instability(불안정)
  - MCP warning noise(MCP 경고 잡음)
  - stdout/stderr capture instability(표준 출력/오류 캡처 불안정)
  - accidental top-level `mcps/` artifact(우발적 최상위 mcps 산출물)
  - hung process cleanup(멈춘 프로세스 정리)
- Non-trivial large review(비사소 대규모 검토)는 one giant prompt(거대 단일 프롬프트)가 아니라 staged narrow reviews(단계별 좁은 검토)로 나누는 방향이 맞다.

## Rejected Or Adjusted(거절 또는 조정)

- `temp cwd` alone(임시 작업 경로만 사용)는 rejected as sufficient(충분한 해결책으로는 거절)한다. Local trial(로컬 시도) showed extra `git repo discovery failed` warnings(깃 저장소 발견 실패 경고) and no answer body(응답 본문 없음).
- `--disallowed-tools read_file,...` is not reliable as a primary control(주 제어로 신뢰 불가). Grok CLI reported `disallowedTools entry matched nothing` for those names, though the short text-only prompt still succeeded.
- Therefore the wrapper(래퍼)는 "make Grok silent(무소음화)"가 아니라 "capture, classify, and sanitize noise(잡음 캡처/분류/정리)"를 목표로 해야 한다.

## Needs Local Verification(로컬 검증 필요)

- Whether Grok CLI has a supported no-tools or no-codebase-upload mode(도구 없음/코드베이스 업로드 없음 모드) that avoids MCP initialization(MCP 초기화).
- Whether Grok config(설정) can disable or fix the noisy MCP servers(시끄러운 MCP 서버), especially `codex` and `atlassian`.
- Whether `--prompt-file` instability(프롬프트 파일 불안정)가 CLI bug(CLI 버그), prompt size(프롬프트 크기), BOM(UTF-8 BOM), or repo/MCP interaction(저장소/MCP 상호작용) 때문인지.
- Exact implementation location(정확한 구현 위치): likely `foundation/control_plane/run_grok_review.py`, with policy text(정책 문구) updated only after smoke test(스모크 테스트).

## Final Codex Direction(최종 Codex 방향)

Implement in two phases(두 단계로 구현):

1. Phase 1(1단계): add a thin wrapper(얇은 래퍼) and smoke-test it on small/medium/large synthetic prompts(소/중/대 합성 프롬프트). The wrapper records clean output(정리 출력), raw diagnostics summary(원본 진단 요약), prompt hash(프롬프트 해시), timeout status(시간 제한 상태), and artifact paths(산출물 경로).
2. Phase 2(2단계): update `obsidian-grok-collaboration` skill(그록 협업 스킬) and `docs/policies/agent_trigger_policy.md` only after wrapper behavior(래퍼 동작)가 verified(검증)된다.

Recommended default(추천 기본값):

- small review(소규모 검토): single compact `-p` prompt(단일 압축 프롬프트)
- medium review(중간 검토): one bounded snapshot(제한 스냅샷) plus one focused prompt(집중 프롬프트)
- large review(대규모 검토): multiple narrow Grok passes(여러 좁은 Grok 회차), each with a separate question(별도 질문), then one Codex synthesis(코덱스 종합)

