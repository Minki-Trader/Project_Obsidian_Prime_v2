# Long Path Skill Surface Review(긴 경로 스킬 표면 검토)

Role(역할): external second opinion(외부 2차 의견) only. Answer only from this bounded evidence(제한 근거). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim runtime authority(런타임 권위).

## Current Truth(현재 진실)

- AGENTS.md already contains Windows Long Path Rule(윈도우 긴 경로 규칙): if PowerShell Get-Content/Get-ChildItem or normal Path.exists(일반 경로 존재 확인)가 deep stage/MT5 artifact(깊은 단계/MT5 산출물)에서 실패하면, missing/blocked(누락/차단)로 바로 판정하지 않고 repo-relative `rg --files`/`rg` and `foundation.control_plane.ledger.io_path`로 재시도한다.
- Existing repo skills(기존 저장소 스킬) already containing related guidance: `obsidian-environment-reproducibility`, `obsidian-architecture-guard`.
- New observed repeat(새 반복 관찰): after F57 closeout(전선57 마감), Codex initially counted F46-F49 as missing runtime probe(런타임 탐침 누락) because native Path/Test-Path style checks failed on long paths. `rg --files` then proved runtime_probe_backfill_status(런타임 탐침 소급 상태) files existed, so still_missing(아직 누락)은 0이었다.

## Proposed Patch(제안 수정)

Add narrow guard text(좁은 보호 문구) to these repo skills:

1. `obsidian-reentry-read`: during current-truth validation(현재 진실 검증), use repo-relative `rg --files`/`rg` before declaring active stage docs or deep frontier evidence missing(누락).
2. `obsidian-runtime-parity`: when checking MT5/runtime artifacts(MT5/런타임 산출물), a native PowerShell/Python path failure is not parity failure(동등성 실패) until `rg --files`/`io_path` retry is tried.
3. `obsidian-result-judgment`: do not label missing/invalid/blocked(누락/무효/차단) from one native path failure on deep stage artifacts; require long-path-safe retry first.

## Claim Boundary(주장 경계)

This is policy/skill governance(정책/스킬 운영) only. It does not relax gates(게이트), thresholds(임계값), MT5 evidence requirements(MT5 근거 요구), or final completion hard gates(최종 완성 강제 게이트).

## Question(질문)

Is this skill-surface patch appropriate and narrow enough? Return accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요), one wording risk(문구 위험), and one required local verification(필수 로컬 검증).
