# Long Path Skill Surface Local Verification(긴 경로 스킬 표면 로컬 검증)

- trigger(트리거): F57 coverage audit(전선57 커버리지 감사)에서 native Path/Test-Path style check(일반 경로 확인)가 F46-F49 runtime probe backfill status(런타임 탐침 소급 상태)를 missing(누락)처럼 오판했다.
- Grok advice(그록 조언): accepted(수용). Reentry/parity/judgment skill surface(재진입/동등성/판정 스킬 표면)에 `retry first, then judge(먼저 재시도, 그다음 판정)` 문구를 추가하라고 했다.
- local file check(로컬 파일 확인): target skills(대상 스킬) `obsidian-reentry-read`, `obsidian-runtime-parity`, `obsidian-result-judgment` had no conflicting long-path wording(충돌 문구 없음).
- existing guard check(기존 보호 확인): `obsidian-environment-reproducibility` and `obsidian-architecture-guard` already contain Windows long-path retry guidance(윈도우 긴 경로 재시도 지침).
- repo scan check(저장소 스캔 확인): `rg --files stages` classified frontier_count(전선 단계 수)=57, runtime_recorded(런타임 기록)=20, invalid_backfill_status(무효 소급 상태)=37, still_missing(아직 누락)=0.
- validator(검증기): `.agents/skills/obsidian-architecture-guard/scripts/validate_agent_settings.py --repo-root .` was run(실행됨) and failed(실패) because of pre-existing encoding/mojibake backlog(기존 인코딩/깨진 문자 부채) in older docs and stages, not because of the three edited skill files. This is recorded as pre-existing validation debt(기존 검증 부채), not as runtime evidence(런타임 근거).
- claim boundary(주장 경계): This policy/skill guard(정책/스킬 보호)는 gate(게이트), threshold(임계값), MT5 output requirement(MT5 출력 요구), completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성)를 만들거나 완화하지 않는다.
