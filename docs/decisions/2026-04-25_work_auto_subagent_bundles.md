# Decision: Work Auto Subagent Bundles

- date(날짜): `2026-04-25`
- scope(범위): agent settings(에이전트 설정), repo-scoped skills(저장소 전용 스킬), work routing(작업 라우팅)
- status(상태): `accepted`

## 결정(Decision, 결정)

작업 종류별 자동 서브에이전트 묶음(auto subagent bundle, 자동 서브에이전트 묶음)을 저장소 라우팅(repository routing, 저장소 라우팅)에 추가한다.

## 묶음(Bundles, 묶음)

- run evidence(실행 근거): `obsidian-run-evidence-system(실행 근거 시스템)` + `obsidian-claim-discipline(주장 규율)`
- stage transition(단계 전환): `obsidian-stage-transition(단계 전환)` + `obsidian-claim-discipline(주장 규율)`
- policy/skill/settings(정책/스킬/설정): `obsidian-architecture-guard(구조 가드)`
- user report(사용자 보고): `obsidian-answer-clarity(답변 명확성)` + `obsidian-claim-discipline(주장 규율)`
- lane/gate(레인/게이트): `obsidian-lane-classifier(레인 분류기)`
- blocker recovery(차단 복구): `obsidian-workflow-drift-guard(작업 드리프트 가드)`
- code quality(코드 품질): `obsidian-code-quality(코드 품질)` for non-trivial code edit(비사소 코드 변경)

## 이유(Rationale, 이유)

코드 작성(code writing, 코드 작성)에는 이미 code surface guard(코드 표면 가드)와 reference scout(레퍼런스 탐색)를 붙였다. 하지만 실행 생성(run creation, 실행 생성), 단계 변경(stage transition, 단계 전환), 사용자 보고(user report, 사용자 보고), 차단 복구(blocker recovery, 차단 복구)도 빠지면 claim(주장)이 강해지거나 상태(state, 상태)가 갈라질 수 있다.

효과(effect, 효과): 작업 유형이 보이는 순간 필요한 검토 관문(review gate, 검토 관문)을 자동으로 떠올리고, validator(검증기)가 각 `agents/openai.yaml` 설정의 존재와 핵심 문구를 확인한다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 agent behavior(에이전트 행동), skill routing(스킬 라우팅), metadata validation(메타데이터 검증)을 바꾼다.

현재 active_stage(활성 단계), model training(모델 학습), runtime authority(런타임 권위), operating promotion(운영 승격)은 바꾸지 않는다.
