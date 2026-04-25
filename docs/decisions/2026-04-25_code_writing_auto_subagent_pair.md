# Decision: Code-Writing Auto Subagent Pair

- date(날짜): `2026-04-25`
- scope(범위): agent settings(에이전트 설정), repo-scoped skills(저장소 전용 스킬), code-writing routing(코드 작성 라우팅)
- status(상태): `accepted`

## 결정(Decision, 결정)

코드 작성(code writing, 코드 작성)이나 코드 수정(code edit, 코드 수정)을 시작할 때 `obsidian-code-surface-guard(코드 표면 가드)`와 `obsidian-reference-scout(레퍼런스 탐색)`를 자동 선행 관문(auto precheck gate, 자동 사전확인 관문)으로 묶는다.

## 이유(Rationale, 이유)

Stage 06(6단계) 작업에서 code surface(코드 표면)는 확인했지만, MQL5/MT5(MetaTrader 5, 메타트레이더5) reference scout(레퍼런스 탐색)를 명시적으로 쓰지 않은 공백이 있었다.

효과(effect, 효과): 다음 코드 작성부터 placement(배치), owner module(소유 모듈), caller(호출자), input/output contract(입출력 계약), external API/API usage(외부 API/API 사용법), MQL5 behavior(MQL5 동작), library behavior(라이브러리 동작)을 작업 전에 분리해서 확인한다.

## 적용 규칙(Application Rule, 적용 규칙)

- Python(파이썬), MQL5, pipeline(파이프라인), stage script(단계 스크립트), test(테스트), model builder(모델 빌더), runtime helper(런타임 도구), report materializer(보고서 물질화 도구)에 모두 적용한다.
- `obsidian-code-surface-guard(코드 표면 가드)`는 항상 먼저 호출한다.
- `obsidian-reference-scout(레퍼런스 탐색)`는 같은 코드 작성 묶음(code-writing packet, 코드 작성 묶음)에 붙인다.
- 순수 내부 로직(pure internal logic, 순수 내부 로직)이고 외부 확인(external lookup, 외부 확인)이 필요 없으면 `reference_scout: not_required(레퍼런스 탐색 불필요)`와 이유(reason, 이유)를 남긴다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 agent behavior(에이전트 행동)와 skill routing(스킬 라우팅)을 바꾼다.

현재 active stage(활성 단계), model training(모델 학습), runtime authority(런타임 권위), operating promotion(운영 승격)은 바꾸지 않는다.
