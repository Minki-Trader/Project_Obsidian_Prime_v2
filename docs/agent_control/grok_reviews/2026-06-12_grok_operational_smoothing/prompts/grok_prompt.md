# Grok Operational Consultation(Grok 운영 상담)

You are reviewing how Codex should operate Grok as a stable external reviewer(안정적인 외부 검토자) inside Project Obsidian Prime v2.

Use the facts below. Do not assume runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), selected baseline(선택 기준선), or goal achieve(목표 달성).

## Observed Issues(관찰 이슈)

- `--prompt-file` calls(프롬프트 파일 호출) produced empty response body(빈 응답 본문) or `max turns reached`.
- `grok.exe -p` single prompt(단일 프롬프트) worked for sanity check(정상 확인) and compact review(압축 검토).
- Running from repo cwd(저장소 작업 경로) produced many MCP warning logs(MCP 경고 로그), including `codex` handshake failure(핸드셰이크 실패) and `atlassian` OAuth required(OAuth 필요).
- stdout/stderr(표준 출력/표준 오류) behavior was noisy and inconsistent(시끄럽고 불일치).
- Long prompts(긴 프롬프트) were less reliable; short compact prompts(짧은 압축 프롬프트) worked better.
- A top-level `mcps/` folder(최상위 mcps 폴더) was created during Grok execution and had to be deleted because top-level scratch folders(최상위 임시 폴더) are not allowed.
- User wants smooth future feedback/discussion(원활한 향후 피드백/토론) for both large and small reviews(대규모/소규모 검토).

## Codex Draft Plan(Codex 초안 계획)

- Treat Grok as isolated external reviewer(격리 외부 검토자), not repo-local coding agent(저장소 내부 코딩 에이전트).
- Default to `grok.exe -p` single prompt(단일 프롬프트).
- Run from isolated temp cwd(격리 임시 작업 경로), not repo root(저장소 루트).
- Use compact prompt tiers(압축 프롬프트 단계): small 1-2KB, medium 2-5KB, large staged digest(단계별 요약), not whole repo dump(전체 저장소 투척).
- Add wrapper script(래퍼 스크립트) to preflight, run, timeout, capture, strip logs, write clean output, and prevent repo-root scratch artifacts(저장소 루트 임시 산출물).
- Update skill/policy(스킬/정책) after wrapper behavior(래퍼 동작) is verified.

## Required Answer(필수 답변)

Please answer in these sections:

- accepted(수용)
- rejected_or_risky(거절 또는 위험)
- recommended_protocol(추천 절차)
- wrapper_requirements(래퍼 요구사항)
- skill_policy_updates(스킬/정책 업데이트)
- open_questions(열린 질문)

Keep it concise and operational(간결하고 운영 가능하게).

