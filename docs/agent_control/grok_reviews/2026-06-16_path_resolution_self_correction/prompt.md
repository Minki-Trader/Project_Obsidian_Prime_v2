# Path Resolution Self-Correction Review(경로 해석 자가 교정 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Answer only from this prompt(프롬프트). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).

## Current Issue(현재 문제)

During one Project Obsidian Prime v2 pass(작업 회차), Codex(코덱스) repeated path/name assumption mistakes(경로/이름 추정 실수):
- wrong skill path(잘못된 스킬 경로) before correcting to repo-local `.agents/skills/...`.
- Windows wildcard/glob command mistake(윈도우 와일드카드/글롭 명령 실수) before switching to `rg` search(검색).
- guessed contract filename(추정 계약 파일명) instead of listing `docs/contracts` first.
- guessed Grok packet filename `request.md`(추정 그록 패킷 파일명) where actual packet uses `prompt.md`.

User rule(사용자 규칙): repeated errors/mistakes(반복 오류/실수) should update AGENTS.md(에이전트 지침) and Skills(스킬) with Grok collaboration(그록 협업), for long-term prevention(장기 예방), not short-term hacks(단기 땜질).

## Proposed Codex Correction(Codex 제안 보정)

Add a narrow path/name resolution preflight(경로/이름 해석 사전확인) to AGENTS.md(에이전트 지침) and `.agents/skills/obsidian-workflow-drift-guard/SKILL.md`:
- Before opening a non-obvious repo file(명확하지 않은 저장소 파일), enumerate with `rg --files` or `Get-ChildItem` first.
- For known packet directories(패킷 폴더), list filenames before assuming `request.md`, `prompt.md`, or report names.
- For Windows glob(윈도우 글롭), prefer `rg pattern root -g *.ext` over shell wildcard directory assumptions(셸 와일드카드 디렉터리 추정).
- If a guessed path fails once, immediately switch to discovery(발견) and record the corrected source of truth(진실 원천); do not retry adjacent guesses.

Boundary(경계): This does not relax evidence gates(근거 게이트), thresholds(임계값), MT5 runtime requirements(MT5 런타임 요구), or stage claims(단계 주장). It is only an execution hygiene(실행 위생) rule.

## Question(질문)

Is this correction appropriately scoped(범위가 적절한가)? Name any missing guardrail(누락 보호장치) Codex(코덱스) should add before patching.
