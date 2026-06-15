# Long Path Guard Update Review(긴 경로 보호 규칙 수정 검토)

Role(역할): external second opinion(외부 2차 의견) only. Do not claim promotion/runtime authority(승격/런타임 권위) and do not inspect files(파일 열람 금지). Answer only from bounded evidence(제한 근거) below.

Current issue(현재 문제): During Frontier50 evidence closeout(전선50 근거 마감), repeated PowerShell Get-Content/Get-ChildItem(파워셸 읽기/나열) attempts failed on deep stage paths with Windows MAX_PATH-like errors(윈도우 긴 경로 오류). The files existed and rg/Python io_path(알지/파이썬 경로 헬퍼) could read them.

Existing local helper(기존 로컬 헬퍼): foundation.control_plane.ledger.io_path is used in project tooling to handle long paths(긴 경로) and ignored 02_runs(실행 원자료) artifacts safely.

Proposed durable fix(제안 장기 수정):
1. Add AGENTS.md(에이전트 지침) rule: for deep stages/MT5 artifacts on Windows(윈도우), prefer rg --files/rg for discovery/read checks and Python io_path for long-path reads/mechanical CSV/JSON rewrites when native PowerShell path access fails; do not misclassify existing files as missing until long-path-safe check is tried.
2. Add obsidian-environment-reproducibility skill(환경 재현성 스킬) note: long-path failures require a retry with repo-relative path plus io_path/rg before declaring blocked/missing.
3. Add obsidian-architecture-guard skill(구조 가드 스킬) note: durable artifact identity should remain repo-relative; absolute/extended paths are local execution helpers only.

Question(질문): Is this narrow policy update appropriate, or should it be broader/narrower?

Return only(다음만 반환):
1. verdict: accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)
2. scope: narrow enough? yes/no(예/아니오)
3. one required local verification(필수 로컬 검증 하나)
4. one wording risk(문구 위험 하나)
