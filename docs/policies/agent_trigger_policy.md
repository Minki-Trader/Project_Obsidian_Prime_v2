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
- `obsidian-work-packet-router`: 작업을 하나의 mode(모드)로 자르지 않고 설계(design, 설계), 코드(code, 코드), 실험(experiment, 실험), 검증(verification, 검증), 근거(evidence, 근거), 판정(judgment, 판정), 보고(report, 보고), 발행(publish, 발행) 단계로 라우팅할 때 쓴다.
- `obsidian-answer-clarity`: 사용자 답변(user-facing answer, 사용자 답변), 계획 세우기(planning, 계획), 제안 계획(proposed plan, 제안 계획), 결과 보고(result report, 결과 보고), 완료 보고(completion report, 완료 보고), 리뷰 설명(review explanation, 리뷰 설명), 상태 보고(status report, 상태 보고)를 쉽게 풀어야 할 때 쓴다.
- `obsidian-claim-discipline`: 문서, 검토, 상태 설명, 사용자 요약(user-facing summary, 사용자 요약)을 쓸 때 주장(claim, 주장)이 너무 강해지지 않게 할 때 쓴다.
- `obsidian-stage-transition`: `active_stage(활성 단계)`나 단계 의미(stage meaning, 단계 의미)가 바뀔 때 쓴다.
- `obsidian-lane-classifier`: 승격(promotion, 승격)이나 런타임(runtime, 런타임) 언어를 붙이기 전에 쓴다.
- `obsidian-exploration-mandate`: 알파 아이디어(alpha idea, 알파 아이디어), 티어 작업(Tier work, 티어 작업), WFO(`walk-forward optimization`, 워크포워드 최적화), 극단값 탐색(extreme sweep, 극단값 탐색), 실패 기록(negative memory, 실패 기록)에 쓴다.
- `obsidian-experiment-design`: 실험 가설(hypothesis, 가설), 비교 기준(baseline, 기준), 통제 변수(control variable, 통제 변수), 성공/실패/무효 조건을 코드나 실행 전에 정할 때 쓴다.
- `obsidian-data-integrity`: 데이터(data, 데이터), 시간축(time axis, 시간축), timezone(시간대), split(분할), feature/label boundary(피처/라벨 경계), leakage(누수)를 확인할 때 쓴다.
- `obsidian-model-validation`: 모델(model, 모델), threshold(임계값), calibration(보정), WFO, split, overfit(과적합), 모델 비교(model comparison, 모델 비교)를 판단할 때 쓴다.
- `obsidian-runtime-parity`: Python 연구 경로(Python research path, 파이썬 연구 경로), MT5 EA, runtime package(런타임 패키지), model bundle(모델 번들), tester output(테스터 출력)이 같은 의미인지 볼 때 쓴다.
- `obsidian-backtest-forensics`: MT5 Strategy Tester(전략 테스터), spread(스프레드), commission(수수료), slippage(슬리피지), trade list(거래 목록), tester setting(테스터 설정)을 검토할 때 쓴다.
- `obsidian-performance-attribution`: KPI 변화(KPI change, KPI 변화)를 시간, 티어, threshold, 모델, 거래 형태(trade shape, 거래 형태), drawdown(드로다운), market regime(시장 국면)으로 설명할 때 쓴다.
- `obsidian-environment-reproducibility`: clean checkout(깨끗한 체크아웃), dependency(의존성), CI, Python version(파이썬 버전), MT5 경로, 로컬 절대 경로(local absolute path, 로컬 절대 경로)를 검토할 때 쓴다.
- `obsidian-artifact-lineage`: 입력(input, 입력), 코드(code, 코드), 설정(config, 설정), 모델(model, 모델), report(보고서), hash(해시), manifest(목록), ledger(장부), 외부 artifact 위치를 연결할 때 쓴다.
- `obsidian-result-judgment`: 결과(result, 결과)를 positive(긍정), negative(부정), invalid(무효), inconclusive(불충분), blocked(차단), promotion_candidate(승격 후보), runtime_probe(런타임 탐침) 등으로 판정할 때 쓴다.
- `obsidian-code-surface-guard`: 코드 배치(code placement, 코드 배치)나 재사용 로직(reusable logic, 재사용 로직)을 바꿀 때 쓴다.
- `obsidian-code-quality`: 코드가 단순히 돌아가는 수준을 넘어 책임(responsibility, 책임), 흐름(flow, 흐름), 계약(contract, 계약), 검증 의도(test intent, 검증 의도)가 읽혀야 할 때 쓴다.
- `obsidian-workflow-drift-guard`: 원재료(source material, 원재료), 도구(tool, 도구), 환경(environment, 환경), 목표(goal, 목표)가 섞여 작업 방향이 새기 쉬울 때 쓴다.
- `obsidian-reference-scout`: 함수 사용법(function usage, 함수 사용법), 구문(syntax, 구문), API, MQL5, GitHub, 포럼(forum, 포럼), 외부 구현 패턴(reference pattern, 참고 패턴)을 찾아 확인할 때 쓴다.
- `obsidian-architecture-guard`: `architecture_invariants.md`, 에이전트 설정(agent settings, 에이전트 설정), 경로(path, 경로), 한국어 인코딩(Korean encoding, 한국어 인코딩), 정책 편집(policy edit, 정책 편집)에 쓴다.
- `obsidian-run-evidence-system`: 실행 근거(run evidence, 실행 근거), KPI(`key performance indicator`, 핵심 성과 지표), 결과 판정(result judgment, 결과 판정), `run_registry.csv(실행 등록부)`에 쓴다.

## 프로젝트 전체 작업 패킷 규칙(Project-Wide Work Packet Rule, 프로젝트 전체 작업 패킷 규칙)

작업(work, 작업)을 코드(code, 코드), 실험(experiment, 실험), 보고(report, 보고) 중 하나로만 고르지 않는다. 이 프로젝트의 대부분의 요청은 하나의 work packet(작업 묶음) 안에서 여러 phase(단계)를 지난다.

기본 흐름(default lifecycle, 기본 생명주기)은 다음이다.

1. current truth(현재 진실) 확인
2. work packet lifecycle(작업 묶음 생명주기) 결정
3. skill routing(스킬 배치) 결정
4. 설계(design, 설계) 또는 실험 가설(experiment hypothesis, 실험 가설) 정리
5. 코드 작성/수정(code writing/edit, 코드 작성/수정)
6. 실행(run, 실행), 검증(verification, 검증), 또는 backtest(백테스트)
7. evidence(근거), artifact lineage(산출물 계보), registry(등록부) 정리
8. result judgment(결과 판정)과 claim boundary(주장 경계) 정리
9. `obsidian-answer-clarity`로 쉬운 사용자 보고(user-facing report, 사용자 보고)

모든 작업 시작 시 `obsidian-session-intake`가 current truth(현재 진실)를 잡고, `obsidian-work-packet-router`가 다음 필드를 만든다.

- `work_packet_lifecycle`
- `phase_plan`
- `skills_considered`
- `skills_selected`
- `skills_not_used`
- `skill_routing_reason`
- `phase_stop_conditions`
- `final_answer_filter`

효과(effect, 효과): 강한 트리거(trigger, 작동 조건)를 가진 스킬만 쓰이고 답변 명확성(answer clarity, 답변 명확성), 레퍼런스 확인(reference scout, 레퍼런스 확인), 데이터 무결성(data integrity, 데이터 무결성), 재현성(reproducibility, 재현성) 같은 스킬이 방치되는 일을 막는다.

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

0. 작업 묶음 라우터 자동 묶음(Work Packet Router Auto Bundle, 작업 묶음 라우터 자동 묶음)
   - 트리거(trigger, 작동 조건): 새 작업 시작, 재개, 구현 요청, 실험 요청, 보고 요청, 정책/스킬 변경, 발행 요청
   - 자동 호출(auto-call, 자동 호출): `obsidian-session-intake(세션 인입)` + `obsidian-work-packet-router(작업 묶음 라우터)`
   - 효과(effect, 효과): 단일 mode(모드)를 고르는 대신, 설계부터 최종 보고까지 필요한 phase(단계)와 스킬(skill, 스킬)을 먼저 배치한다.
1. 실행 생성/종료 자동 묶음(Run Evidence Auto Bundle, 실행 근거 자동 묶음)
   - 트리거(trigger, 작동 조건): run creation(실행 생성), run closeout(실행 종료), KPI report(KPI 보고), result summary(결과 요약), run registry update(실행 등록부 갱신), Tier A primary + Tier B fallback routing(Tier A 우선 + Tier B 대체 라우팅)
   - 자동 호출(auto-call, 자동 호출): `obsidian-run-evidence-system(실행 근거 시스템)` + `obsidian-artifact-lineage(산출물 계보)` + `obsidian-result-judgment(결과 판정)` + `obsidian-claim-discipline(주장 규율)`
   - 효과(effect, 효과): measurement(측정), identity(정체성), judgment(판정), registry boundary(등록부 경계)를 갖춘 실행만 reviewed run(검토된 실행)으로 말하고, routed total(라우팅 전체)을 synthetic sum(합성 합산)과 섞지 않는다.
2. 실험 설계 자동 묶음(Experiment Design Auto Bundle, 실험 설계 자동 묶음)
   - 트리거(trigger, 작동 조건): 새 실험, 비교 실험, 패키징 실험, threshold/model/context scout(임계값/모델/문맥 탐색), ablation(제거 실험), stress test(압박 시험)
   - 자동 호출(auto-call, 자동 호출): `obsidian-experiment-design(실험 설계)` + `obsidian-data-integrity(데이터 무결성)` + 필요 시 `obsidian-reference-scout(레퍼런스 탐색)`
   - 효과(effect, 효과): 실행 전에 hypothesis(가설), baseline(기준), changed variables(변경 변수), invalid conditions(무효 조건), evidence plan(근거 계획)을 고정한다.
3. 데이터/모델 검증 자동 묶음(Data Model Validation Auto Bundle, 데이터 모델 검증 자동 묶음)
   - 트리거(trigger, 작동 조건): dataset(데이터셋), feature(피처), label(라벨), split(분할), model training(모델 학습), threshold(임계값), WFO, calibration(보정), overfit(과적합) 관련 작업
   - 자동 호출(auto-call, 자동 호출): `obsidian-data-integrity(데이터 무결성)` + `obsidian-model-validation(모델 검증)` + `obsidian-code-quality(코드 품질)`
   - 효과(effect, 효과): 시간축(time axis), feature/label boundary(피처/라벨 경계), split 의미, selection metric(선택 지표), overfit risk(과적합 위험)를 같이 본다.
4. 런타임/백테스트 자동 묶음(Runtime Backtest Auto Bundle, 런타임 백테스트 자동 묶음)
   - 트리거(trigger, 작동 조건): MT5, EA, `.mq5`, `.mqh`, `.set`, Strategy Tester, runtime package, model bundle, handoff file, tester report, live-like path
   - 자동 호출(auto-call, 자동 호출): `obsidian-runtime-parity(런타임 동등성)` + `obsidian-backtest-forensics(백테스트 포렌식)` + `obsidian-reference-scout(레퍼런스 탐색)` + `obsidian-run-evidence-system(실행 근거 시스템)`
   - 효과(effect, 효과): Python 연구 결과(Python research result, 파이썬 연구 결과)를 MT5/runtime authority(런타임 권위)로 과장하지 않고, tester identity(테스터 정체성)와 runtime parity(런타임 동등성)를 확인한다.
5. 재현성/산출물 계보 자동 묶음(Reproducibility Lineage Auto Bundle, 재현성 계보 자동 묶음)
   - 트리거(trigger, 작동 조건): README command(README 명령), test command(테스트 명령), dependency(의존성), CI, clean checkout, `.gitignore`, ignored artifact(무시된 산출물), external artifact URI(외부 산출물 URI), release bundle(릴리스 묶음), manifest(목록)
   - 자동 호출(auto-call, 자동 호출): `obsidian-environment-reproducibility(환경 재현성)` + `obsidian-artifact-lineage(산출물 계보)` + `obsidian-claim-discipline(주장 규율)`
   - 효과(effect, 효과): 새 checkout(체크아웃)에서 무엇이 바로 되는지, 무엇이 설치/다운로드/재생성되어야 하는지 분리해서 말한다.
6. 성과 귀인 자동 묶음(Performance Attribution Auto Bundle, 성과 귀인 자동 묶음)
   - 트리거(trigger, 작동 조건): KPI가 좋아짐/나빠짐/이상함, 모델/threshold/feature 선택, drawdown(드로다운), trade shape(거래 형태), regime(국면) 설명
   - 자동 호출(auto-call, 자동 호출): `obsidian-performance-attribution(성과 귀인)` + `obsidian-result-judgment(결과 판정)` + `obsidian-answer-clarity(답변 명확성)`
   - 효과(effect, 효과): headline KPI(대표 KPI)만 보고 좋아졌다고 말하지 않고, 무엇 때문에 변했는지와 아직 모르는 것을 같이 설명한다.
7. 단계 변경 자동 묶음(Stage Transition Auto Bundle, 단계 전환 자동 묶음)
   - 트리거(trigger, 작동 조건): active_stage(활성 단계) 변경, stage closeout(단계 종료), handoff(인계), selection status(선택 상태) 변경
   - 자동 호출(auto-call, 자동 호출): `obsidian-stage-transition(단계 전환)` + `obsidian-claim-discipline(주장 규율)`
   - 효과(effect, 효과): workspace_state(작업공간 상태), selection_status(선택 상태), decision memo(결정 메모), registry(등록부)가 서로 다른 상태로 갈라지지 않는다.
8. 정책/스킬/설정 자동 묶음(Policy Skill Settings Auto Bundle, 정책/스킬/설정 자동 묶음)
   - 트리거(trigger, 작동 조건): agent settings(에이전트 설정), repo-scoped skills(저장소 전용 스킬), policy edit(정책 편집), architecture invariant(구조 불변 규칙), Korean encoding(한국어 인코딩), durable path reference(지속 경로 참조) 변경
   - 자동 호출(auto-call, 자동 호출): `obsidian-architecture-guard(구조 가드)`
   - 효과(effect, 효과): 파일 배치(file placement, 파일 배치), 경로(path, 경로), UTF-8 BOM(UTF-8 BOM 포함), agent metadata(에이전트 메타데이터)를 검증 대상으로 만든다.
9. 사용자 보고 자동 묶음(User Report Auto Bundle, 사용자 보고 자동 묶음)
   - 트리거(trigger, 작동 조건): status summary(상태 요약), result report(결과 보고), completion report(완료 보고), plan(계획), review explanation(검토 설명)
   - 자동 호출(auto-call, 자동 호출): `obsidian-answer-clarity(답변 명확성)` + `obsidian-claim-discipline(주장 규율)`
   - 효과(effect, 효과): 사용자가 "그래서 무슨 뜻이야?"라고 다시 묻지 않도록 결론(conclusion, 결론), 쉬운 의미(plain meaning, 쉬운 의미), 확정된 것(confirmed, 확정), 아직 아닌 것(not yet confirmed, 아직 미확정), 근거(evidence, 근거), 다음 행동(next action, 다음 행동)을 먼저 말한다.
10. 레인/게이트 자동 묶음(Lane Gate Auto Bundle, 레인/게이트 자동 묶음)
   - 트리거(trigger, 작동 조건): exploration(탐색), evidence(근거), promotion(승격), runtime(런타임), hard gate(강한 게이트), Tier A/B/C(티어 A/B/C)가 섞일 수 있는 작업
   - 자동 호출(auto-call, 자동 호출): `obsidian-lane-classifier(레인 분류기)`
   - 효과(effect, 효과): hard gate(강한 게이트)를 exploration permission(탐색 허가)으로 잘못 쓰지 않는다.
11. 차단/드리프트 복구 자동 묶음(Blocker Recovery Auto Bundle, 차단 복구 자동 묶음)
   - 트리거(trigger, 작동 조건): source material(원재료), tool(도구), environment(환경), permission(권한), MT5 output(MT5 출력), external verification(외부 검증)이 없거나 틀린 작업
   - 자동 호출(auto-call, 자동 호출): `obsidian-workflow-drift-guard(작업 드리프트 가드)`
   - 효과(effect, 효과): 진짜 blocker(차단 사유)를 복구하거나, 복구가 안 되면 claim(주장)을 낮춰 blocked(차단)로 남긴다.
   - blocked(차단) 전 필수 증거(required evidence, 필수 증거): recovery attempt(복구 시도), created or patched tool(생성/수정한 도구), execution attempt(실행 시도), failure log(실패 로그), required user action(필요 사용자 행동) 중 하나를 남긴다.
   - MT5 주의(MT5 caution, MT5 주의): MetaEditor compile(메타에디터 컴파일)은 MT5 snapshot(MT5 스냅샷), terminal file output(터미널 파일 출력), strategy tester output(전략 테스터 출력)을 대체하지 않는다.
12. 확대 코드 품질 자동 묶음(Code Quality Auto Bundle, 코드 품질 자동 묶음)
   - 트리거(trigger, 작동 조건): 모델 학습(model training, 모델 학습), feature(피처), label(라벨), split(분할), parity(동등성), report materializer(보고서 물질화 도구), test(테스트)처럼 결과 해석을 바꿀 수 있는 비사소 코드 변경(non-trivial code edit, 비사소 코드 변경)
   - 자동 호출(auto-call, 자동 호출): `obsidian-code-quality(코드 품질)`를 코드 표면 가드(code-surface guard, 코드 표면 가드) 뒤에 붙인다.
   - 효과(effect, 효과): responsibility(책임), flow(흐름), contract(계약), test intent(검증 의도)가 코드 안에서 읽히게 한다.
13. EA 실행 변형 강제 묶음(EA Run Variant Hard Bundle, EA 실행 변형 강제 묶음)
   - 트리거(trigger, 작동 조건): MT5 EA(`Expert Advisor`, 전문가 자문), `.mq5`, `.mqh`, `.set`, Strategy Tester(전략 테스터), optimization pass(최적화 회차), tester property(테스터 속성), runtime package(런타임 패키지), model bundle(모델 번들), EA run config(EA 실행 설정), Tier A primary + Tier B fallback routing(Tier A 우선 + Tier B 대체 라우팅), module hash(모듈 해시)를 만들거나 바꾸는 작업
   - 자동 호출(auto-call, 자동 호출): `obsidian-code-surface-guard(코드 표면 가드)` + `obsidian-reference-scout(레퍼런스 탐색)` + `obsidian-run-evidence-system(실행 근거 시스템)` + `obsidian-claim-discipline(주장 규율)`
   - 사전 판정(required precheck, 필수 사전 판정): run별 차이(run-specific difference, 실행별 차이)가 parameter-only(파라미터만), module-change(모듈 변경), entrypoint-change(진입점 변경), new-runner-required(새 실행기 필요) 중 무엇인지 먼저 적는다.
   - 금지(default no, 기본 금지): run마다 새 `.mq5` 파일을 복제(copy, 복사)해서 관리하지 않는다.
   - 필수 정체성(required identity, 필수 정체성): `ea_entrypoint`, `.set` path(설정 파일 경로), input params hash(입력 파라미터 해시), module hashes(모듈 해시), model/bundle hash(모델/번들 해시), tester model/deposit/leverage(테스터 모델/예치금/레버리지), output path(출력 경로)를 실행 근거(run evidence, 실행 근거)에 남긴다.
   - 효과(effect, 효과): EA run(실행) 결과가 어느 코드(code, 코드), 어느 설정(set, 설정), 어느 모델/번들(model/bundle, 모델/번들), 어느 테스터 조건(tester condition, 테스터 조건)에서 나온 것인지 끊기지 않는다.

## 필수 정책 링크(Required Policy Links, 필수 정책 링크)

- `architecture_invariants.md`
- `exploration_mandate.md`
- `kpi_measurement_standard.md`
- `run_result_management.md`
- `result_judgment_policy.md`
- `mt5_ea_input_order_contract_fpmarkets_v2.md`

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
