# Decision: Pre-Block Recovery Hardening

- date(날짜): `2026-04-25`
- scope(범위): workflow drift guard(작업 드리프트 가드), external verification(외부 검증), MT5 runtime check(MT5 런타임 확인)
- status(상태): `accepted`

## 결정(Decision, 결정)

`blocked(차단)` 판정 전에 pre-block evidence(차단 전 근거)를 요구한다.

pre-block evidence(차단 전 근거)는 recovery attempt(복구 시도), created or patched tool(생성/수정한 도구), execution attempt(실행 시도), failure log(실패 로그), required user action(필요 사용자 행동) 중 하나 이상이어야 한다.

## 이유(Rationale, 이유)

Stage 06(6단계) runtime parity(런타임 동등성) 작업은 stale MT5 audit tool(낡은 MT5 감사 도구)을 발견하고 MetaEditor compile(메타에디터 컴파일)까지 확인했지만, MT5 snapshot(MT5 스냅샷)을 생성할 수 있는 현재 프로젝트 도구를 고치거나 만들어 실행하는 단계까지 가지 못했다.

효과(effect, 효과): 다음 MT5(`MetaTrader 5`, 메타트레이더5), external verification(외부 검증), runtime output(런타임 출력) 작업은 compile-only evidence(컴파일만의 근거)를 runtime output(런타임 출력)처럼 취급하지 않는다.

## 적용 규칙(Application Rule, 적용 규칙)

- missing tool(없는 도구), stale tool(낡은 도구), wrong-surface tool(잘못된 표면 도구)은 blocked(차단) 전에 현재 프로젝트 기준으로 만들거나 고쳐서 실행을 먼저 시도한다.
- MT5 verification(MT5 검증)에서 MetaEditor compile(메타에디터 컴파일)은 MT5 snapshot(MT5 스냅샷), terminal file output(터미널 파일 출력), strategy tester output(전략 테스터 출력)을 대체하지 않는다.
- Codex가 MT5 terminal(MT5 터미널)을 직접 조작할 수 없으면 exact terminal action(정확한 터미널 행동)과 expected output file(기대 출력 파일)을 사용자에게 요청한다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 agent behavior(에이전트 행동)와 external verification discipline(외부 검증 규율)을 강화한다.

현재 active_stage(활성 단계), Stage 06(6단계) blocked judgment(차단 판정), Stage 07(7단계) scope(범위), runtime authority(런타임 권위), operating promotion(운영 승격)은 바꾸지 않는다.
