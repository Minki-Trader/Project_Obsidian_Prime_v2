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
- `obsidian-answer-clarity`: 사용자 답변(user-facing answer, 사용자 답변), 계획 세우기(planning, 계획), 제안 계획(proposed plan, 제안 계획), 결과 보고(result report, 결과 보고), 완료 보고(completion report, 완료 보고), 리뷰 설명(review explanation, 리뷰 설명), 상태 보고(status report, 상태 보고)를 쉽게 풀어야 할 때 쓴다.
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

## 코드 작성 자동 서브에이전트 규칙(Code-Writing Auto Subagent Rule, 코드 작성 자동 서브에이전트 규칙)

코드 작성(code writing, 코드 작성)이나 코드 수정(code edit, 코드 수정)을 시작하기 전에 다음 lightweight subagent gate(가벼운 서브에이전트 관문)를 먼저 적용한다.

1. `obsidian-code-surface-guard(코드 표면 가드)`를 항상 먼저 호출한다.
   - 대상(target, 대상): Python(파이썬), MQL5, foundation(기반), pipeline(파이프라인), MT5 EA, stage script(단계 스크립트), test(테스트), report materializer(보고서 물질화 도구)
   - 효과(effect, 효과): owner module(소유 모듈), caller(호출자), input/output contract(입출력 계약), artifact/report effect(산출물/보고서 효과)를 코드 작성 전에 고정한다.
2. `obsidian-reference-scout(레퍼런스 탐색)`를 같은 코드 작성 패킷(packet, 묶음)에 자동으로 붙인다.
   - MQL5/MT5(MetaTrader 5, 메타트레이더5), MetaEditor(메타에디터), strategy tester(전략 테스터), file handoff(파일 인계), 외부 API, CLI, pandas/sklearn/numpy/LightGBM 같은 library behavior(라이브러리 동작)는 official docs(공식 문서) 또는 maintained source(유지보수되는 원천)를 확인한다.
   - 순수 내부 코드(pure internal code, 순수 내부 코드)이고 새 API/API 사용법이나 버전 의존 행동(version-sensitive behavior, 버전 민감 동작)이 없으면 `reference_scout: not_required(레퍼런스 탐색 불필요)`와 이유(reason, 이유)를 짧게 남긴다.
   - 효과(effect, 효과): 이전 대화 기억(project memory, 프로젝트 기억)만으로 API, MQL5 behavior(MQL5 동작), 파일 인계(file handoff, 파일 인계), 라이브러리 동작(library behavior, 라이브러리 동작)을 단정하지 않는다.
3. 두 관문(gate, 관문)의 결과는 구현 전 작업 메모(implementation precheck, 구현 전 사전확인)나 완료 보고(completion report, 완료 보고)에 짧게 남긴다.

이 규칙(rule, 규칙)은 코드 작성 전체에 적용한다. 단계(stage, 단계) 번호와 무관하다.

## 작업 자동 서브에이전트 묶음(Work Auto Subagent Bundles, 작업 자동 서브에이전트 묶음)

아래 묶음(bundle, 묶음)은 작업 종류가 보이면 자동으로 붙인다. 효과(effect, 효과)는 필요한 검토 관문(review gate, 검토 관문)을 기억에 맡기지 않고, 작업 의미와 보고 경계를 같은 회차(pass, 회차)에 고정하는 것이다.

1. 실행 생성/종료 자동 묶음(Run Evidence Auto Bundle, 실행 근거 자동 묶음)
   - 트리거(trigger, 작동 조건): run creation(실행 생성), run closeout(실행 종료), KPI report(KPI 보고), result summary(결과 요약), run registry update(실행 등록부 갱신)
   - 자동 호출(auto-call, 자동 호출): `obsidian-run-evidence-system(실행 근거 시스템)` + `obsidian-claim-discipline(주장 규율)`
   - 효과(effect, 효과): measurement(측정), identity(정체성), judgment(판정), registry boundary(등록부 경계)를 갖춘 실행만 reviewed run(검토된 실행)으로 말한다.
2. 단계 변경 자동 묶음(Stage Transition Auto Bundle, 단계 전환 자동 묶음)
   - 트리거(trigger, 작동 조건): active_stage(활성 단계) 변경, stage closeout(단계 종료), handoff(인계), selection status(선택 상태) 변경
   - 자동 호출(auto-call, 자동 호출): `obsidian-stage-transition(단계 전환)` + `obsidian-claim-discipline(주장 규율)`
   - 효과(effect, 효과): workspace_state(작업공간 상태), selection_status(선택 상태), decision memo(결정 메모), registry(등록부)가 서로 다른 상태로 갈라지지 않는다.
3. 정책/스킬/설정 자동 묶음(Policy Skill Settings Auto Bundle, 정책/스킬/설정 자동 묶음)
   - 트리거(trigger, 작동 조건): agent settings(에이전트 설정), repo-scoped skills(저장소 전용 스킬), policy edit(정책 편집), architecture invariant(구조 불변 규칙), Korean encoding(한국어 인코딩), durable path reference(지속 경로 참조) 변경
   - 자동 호출(auto-call, 자동 호출): `obsidian-architecture-guard(구조 가드)`
   - 효과(effect, 효과): 파일 배치(file placement, 파일 배치), 경로(path, 경로), UTF-8 BOM(UTF-8 BOM 포함), agent metadata(에이전트 메타데이터)를 검증 대상으로 만든다.
4. 사용자 보고 자동 묶음(User Report Auto Bundle, 사용자 보고 자동 묶음)
   - 트리거(trigger, 작동 조건): status summary(상태 요약), result report(결과 보고), completion report(완료 보고), plan(계획), review explanation(검토 설명)
   - 자동 호출(auto-call, 자동 호출): `obsidian-answer-clarity(답변 명확성)` + `obsidian-claim-discipline(주장 규율)`
   - 효과(effect, 효과): 사용자에게 현재 사실(current truth, 현재 진실), 아직 아닌 것(not-yet-true, 아직 사실 아님), 다음 행동(next action, 다음 행동)을 짧고 정확하게 말한다.
5. 레인/게이트 자동 묶음(Lane Gate Auto Bundle, 레인/게이트 자동 묶음)
   - 트리거(trigger, 작동 조건): exploration(탐색), evidence(근거), promotion(승격), runtime(런타임), hard gate(강한 게이트), Tier A/B/C(티어 A/B/C)가 섞일 수 있는 작업
   - 자동 호출(auto-call, 자동 호출): `obsidian-lane-classifier(레인 분류기)`
   - 효과(effect, 효과): hard gate(강한 게이트)를 exploration permission(탐색 허가)으로 잘못 쓰지 않는다.
6. 차단/드리프트 복구 자동 묶음(Blocker Recovery Auto Bundle, 차단 복구 자동 묶음)
   - 트리거(trigger, 작동 조건): source material(원재료), tool(도구), environment(환경), permission(권한), MT5 output(MT5 출력), external verification(외부 검증)이 없거나 틀린 작업
   - 자동 호출(auto-call, 자동 호출): `obsidian-workflow-drift-guard(작업 드리프트 가드)`
   - 효과(effect, 효과): 진짜 blocker(차단 사유)를 복구하거나, 복구가 안 되면 claim(주장)을 낮춰 blocked(차단)로 남긴다.
7. 확대 코드 품질 자동 묶음(Code Quality Auto Bundle, 코드 품질 자동 묶음)
   - 트리거(trigger, 작동 조건): 모델 학습(model training, 모델 학습), feature(피처), label(라벨), split(분할), parity(동등성), report materializer(보고서 물질화 도구), test(테스트)처럼 결과 해석을 바꿀 수 있는 비사소 코드 변경(non-trivial code edit, 비사소 코드 변경)
   - 자동 호출(auto-call, 자동 호출): `obsidian-code-quality(코드 품질)`를 코드 표면 가드(code-surface guard, 코드 표면 가드) 뒤에 붙인다.
   - 효과(effect, 효과): responsibility(책임), flow(흐름), contract(계약), test intent(검증 의도)가 코드 안에서 읽히게 한다.

## 필수 정책 링크(Required Policy Links, 필수 정책 링크)

- `architecture_invariants.md`
- `exploration_mandate.md`
- `kpi_measurement_standard.md`
- `run_result_management.md`
- `result_judgment_policy.md`

## 답변 명확성 강제 트리거(Answer Clarity Hard Trigger, 답변 명확성 강제 트리거)

다음 user-facing output(사용자용 출력)은 `obsidian-answer-clarity`를 마지막에 적용한다.

- 계획 세우기(plan, 계획), 제안 계획(proposed plan, 제안 계획), 다음 작업 계획(next-task plan, 다음 작업 계획)
- 결과 보고(result report, 결과 보고), 완료 보고(completion report, 완료 보고), 상태 요약(status summary, 상태 요약)
- 단계 종료(stage closeout, 단계 종료), 인계(handoff, 인계), 실행 결과(run result, 실행 결과), 검토 결과(review result, 검토 결과)

효과(effect, 효과): 답변은 파일 목록(file inventory, 파일 목록)이나 명령 로그(command log, 명령 기록)로 시작하지 않고, 결론(conclusion, 결론), 현재 의미(current meaning, 현재 의미), 아직 아닌 것(not-yet-true, 아직 사실 아님), 다음 행동(next action, 다음 행동)을 먼저 말한다.

다른 스킬(skill, 작업 지침)이 기술 판단(technical judgment, 기술 판단)을 만들었더라도, 사용자에게 답할 때는 이 트리거(trigger, 작동 조건)를 마지막 필터(final filter, 최종 필터)로 적용한다.

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
