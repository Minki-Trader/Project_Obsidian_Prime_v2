# Agent Trigger Policy

이 문서는 저장소 전용 스킬(repo-scoped skills, 저장소 전용 스킬)을 언제 쓰는지 정한다.

## 목적(Purpose, 목적)

- `AGENTS.md`를 짧게 유지한다.
- 재진입(re-entry, 재진입)을 일정하게 만든다.
- 오래된 단계 드리프트(stage drift, 단계 드리프트)를 막는다.
- 탐색(exploration, 탐색)이 운영 게이트(operating gate, 운영 게이트)에 눌리지 않게 한다.
- 실행 근거(run evidence, 실행 근거)를 읽기 쉽게 유지한다.

## 스킬(Skills, 스킬)

- `obsidian-session-intake`: 상태(status, 상태), 계획(planning, 계획), 구현(implementation, 구현)을 시작할 때 쓴다.
- `obsidian-reentry-read`: 저장소 작업을 재개할 때 쓴다.
- `obsidian-answer-clarity`: 사용자 답변(user-facing answer, 사용자 답변), 리뷰 설명(review explanation, 리뷰 설명), 상태 보고(status report, 상태 보고)를 쉽게 풀어야 할 때 쓴다.
- `obsidian-claim-discipline`: 문서, 검토, 상태 설명, 사용자 요약(user-facing summary, 사용자 요약)을 쓸 때 주장(claim, 주장)이 너무 강해지지 않게 할 때 쓴다.
- `obsidian-stage-transition`: `active_stage(활성 단계)`나 단계 의미(stage meaning, 단계 의미)가 바뀔 때 쓴다.
- `obsidian-lane-classifier`: 승격(promotion, 승격)이나 런타임(runtime, 런타임) 언어를 붙이기 전에 쓴다.
- `obsidian-exploration-mandate`: 알파 아이디어(alpha idea, 알파 아이디어), 티어 작업(Tier work, 티어 작업), WFO(`walk-forward optimization`, 워크포워드 최적화), 극단값 탐색(extreme sweep, 극단값 탐색), 실패 기록(negative memory, 실패 기록)에 쓴다.
- `obsidian-code-surface-guard`: 코드 배치(code placement, 코드 배치)나 재사용 로직(reusable logic, 재사용 로직)을 바꿀 때 쓴다.
- `obsidian-code-quality`: 코드가 단순히 돌아가는 수준을 넘어 책임(responsibility, 책임), 흐름(flow, 흐름), 계약(contract, 계약), 검증 의도(test intent, 검증 의도)가 읽혀야 할 때 쓴다.
- `obsidian-workflow-drift-guard`: 원재료(source material, 원재료), 도구(tool, 도구), 환경(environment, 환경), 목표(goal, 목표)가 섞여 작업 방향이 새기 쉬울 때 쓴다.
- `obsidian-reference-scout`: 함수 사용법(function usage, 함수 사용법), 구문(syntax, 구문), API, MQL5, GitHub, 포럼(forum, 포럼), 외부 구현 패턴(reference pattern, 참고 패턴)을 찾아 확인할 때 쓴다.
- `obsidian-architecture-guard`: `architecture_invariants.md`, 에이전트 설정(agent settings, 에이전트 설정), 경로(path, 경로), 한국어 인코딩(Korean encoding, 한국어 인코딩), 정책 편집(policy edit, 정책 편집)에 쓴다.
- `obsidian-run-evidence-system`: 실행 근거(run evidence, 실행 근거), KPI(`key performance indicator`, 핵심 성과 지표), 결과 판정(result judgment, 결과 판정), `run_registry.csv(실행 등록부)`에 쓴다.

## 필수 정책 링크(Required Policy Links, 필수 정책 링크)

- `architecture_invariants.md`
- `exploration_mandate.md`
- `kpi_measurement_standard.md`
- `run_result_management.md`
- `result_judgment_policy.md`

## 같은 회차 동기화(Same-Pass Sync, 같은 회차 동기화)

단계 의미(stage meaning, 단계 의미)가 바뀌면 같은 작업 회차(pass, 회차)에 다음을 맞춘다.

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- 활성 단계(active stage, 활성 단계) `04_selected/selection_status.md`
- 필요하면 활성 단계(active stage, 활성 단계) `03_reviews/review_index.md`
- 변경이 지속 결정(durable decision, 지속 결정)이면 `docs/decisions/*.md`
- 산출물 정체성(artifact identity, 산출물 정체성)이 바뀌면 `docs/registers/artifact_registry.csv`
- 실행 상태(run status, 실행 상태)가 바뀌면 `docs/registers/run_registry.csv`
- `docs/workspace/changelog.md`

## 강한 게이트 규칙(Hard Gate Rule, 강한 게이트 규칙)

강한 게이트(hard gate, 강한 게이트)는 `operating_promotion(운영 승격)`과 `runtime_authority(런타임 권위)`에만 적용한다.

강한 게이트(hard gate, 강한 게이트)는 탐색 아이디어(exploration idea, 탐색 아이디어)를 시도할 수 있는지 결정하지 않는다.
