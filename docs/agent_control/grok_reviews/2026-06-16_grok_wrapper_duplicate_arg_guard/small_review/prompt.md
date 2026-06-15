# Grok Wrapper Duplicate Argument Guard Review(그록 래퍼 중복 인자 보호 검토)

Current truth(현재 진실):
- Project(프로젝트): Project Obsidian Prime v2.
- User goal(사용자 목표) requires Grok review(그록 검토) at stage open(단계 개방), before expensive WFO/MT5(비싼 WFO/MT5 전), and stage closeout(단계 마감).
- Rule2(추가규칙2): when repeated errors or mistakes appear, update AGENTS.md(에이전트 문서) and Skills(스킬) with Grok cooperation(그록 협조) so the operation improves long-term(장기 운영 개선).

Observed local transport error(로컬 전송 오류 관찰):
- Codex first called wrapper(래퍼) with `--extra-arg --no-plan`, which failed because `--extra-arg` expects one value.
- Codex then called wrapper(래퍼) with `--extra-arg=--no-plan --extra-arg=--no-subagents --extra-arg=--disable-web-search`, which failed because wrapper defaults already pass those flags.
- Calling wrapper(래퍼) without duplicated default flags succeeded.

Proposed Codex change(제안 변경):
- Add to AGENTS.md(에이전트 문서) and `obsidian-grok-collaboration` Skill(그록 협업 스킬):
  "Wrapper defaults(래퍼 기본값) already include `--rules`, `--no-plan`, `--no-subagents`, and `--disable-web-search`; do not pass them again through `--extra-arg` unless wrapper output proves they are absent. If an extra argument begins with `--`, use the `--extra-arg=--flag` form."

Claim boundary(주장 경계):
- This is policy/skill governance(정책/스킬 운영 보정) only.
- It does not relax any gate(게이트), threshold(임계값), MT5 evidence requirement(MT5 근거 요구), or claim boundary(주장 경계).

Question(질문):
Is this proposed guard accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) as a durable prevention for the repeated Grok wrapper duplicate-argument mistake? Answer only from this snapshot(스냅샷) and list concrete risks only.
