# Project Obsidian Prime v2

## 핵심 의도(Core Intent, 핵심 의도)

이 작업공간은 FPMarkets `US100` `M5` 연구와 실행을 위한 깨끗한 프로젝트다.

Obsidian Prime의 개념(concept, 개념)과 브로커 심볼 계약(broker symbol contract, 브로커 심볼 계약)은 유지한다. 하지만 과거 승자(winner, 승자), 과거 승격 이력(promotion history, 승격 이력), 과거 단계 압력(stage pressure, 단계 압력)은 물려받지 않는다.

## 응답 규칙(Language Rule, 언어 규칙)

- 영어 표현(English expression, 영어 표현)을 쓸 때는 같은 문맥 안에 한국어 표기를 함께 쓴다.
- 행동(action, 행동)을 설명할 때는 그 행동의 효과(effect, 효과)도 같이 설명한다.
- 설명은 짧고 쉽게 쓴다.
- 사용자 협업 스타일(user collaboration style, 사용자 협업 스타일)은 co-pilot(공동 조종자, 협업 동반자)처럼 둔다. 실행 가능한 선택지와 근거를 짧게 말하고, 확신이 없으면 claim boundary(주장 경계)를 낮춘다.
- 효과(effect, 효과)는 사용자가 규칙 해석 부담을 떠안지 않고, Codex(코덱스)가 현재 작업에서 무엇을 할 수 있고 무엇을 아직 말하면 안 되는지 먼저 정리하게 하는 것이다.

## Codex 작업 생명주기(Codex Work Lifecycle, 코덱스 작업 생명주기)

작업(work, 작업)을 코드(code, 코드), 실험(experiment, 실험), 보고(report, 보고) 중 하나로만 고르지 않는다. 대부분의 작업은 하나의 work packet(작업 묶음) 안에서 설계(design, 설계), 코드 작성(code writing, 코드 작성), 실행(run, 실행), 근거 기록(evidence recording, 근거 기록), 결과 판정(result judgment, 결과 판정), 사용자 보고(user-facing report, 사용자 보고)를 함께 지난다.

작업 시작 시 `obsidian-session-intake(세션 인입)`는 현재 진실(current truth, 현재 진실), 브랜치/작업트리 적합성, 작업 성격(work family, 작업군) 후보만 좁게 잡는다. 그 다음 `obsidian-work-packet-router(작업 묶음 라우터)`는 `docs/agent_control/work_family_registry.yaml`에서 `primary_family(주 작업군)` 하나, `primary_skill(주 스킬)` 하나, 제한된 `support_skills(보조 스킬)`, `required_gates(필수 게이트)`를 선택한다.

효과(effect, 효과)는 스킬을 많이 붙인 것처럼 보이게 하지 않고, 실제로 선택한 스킬과 closeout(종료 기록)에 연결된 gate(게이트)만 완료 주장(completion claim, 완료 주장)의 근거로 쓰게 하는 것이다.

운영 라우팅(operating routing, 운영 라우팅)의 진실 원천(source of truth, 진실 원천)은 `docs/agent_control/work_family_registry.yaml`이다. 모든 non-trivial work packet(비사소 작업 묶음)은 `primary_family(주 작업군)` 하나와 `primary_skill(주 스킬)` 하나를 먼저 고른다. `support_skills(보조 스킬)`는 필요한 만큼만 붙이고, 완료 전에는 `required_gate_coverage_audit(필수 게이트 커버리지 감사)`로 work packet(작업 묶음)의 `required_gates(필수 게이트)`가 closeout(종료 기록)에 실제로 연결됐는지 확인한다.

효과(effect, 효과)는 Stage 5부터 미래 Stage 50+까지 작업 내용은 달라져도, 스킬 선택(skill selection, 스킬 선택), receipt(영수증), gate(게이트), claim boundary(주장 경계)가 같은 방식으로 작동하게 하는 것이다.

새 work packet(새 작업 묶음)은 `work_packet_schema_v2_1(작업 묶음 스키마 버전 2.1)`과 `packet_lifecycle=new_packet(작업 묶음 생명주기=새 묶음)`을 사용한다. 과거 v1/v2 packet(버전1/2 작업 묶음)은 archive-only(보관 전용)로만 읽고, 새 reviewed/verified/pass(검토됨/검증됨/통과) 주장 근거로 승격하지 않는다.

효과(effect, 효과)는 예전 묶음 형식을 지우지 않으면서도 새 작업이 verification_profile(검증 프로필), trigger source(트리거 원천), protected claim(보호 주장), required evidence(필수 근거), stop condition(중단 조건)을 빠뜨리지 못하게 하는 것이다.

gate(게이트)가 실패하면 `docs/agent_control/self_correction_policy.yaml`의 기본값인 `plan_only` 흐름으로 실패 원인과 repair plan(수정 계획)을 먼저 남긴다. 자동 수정은 allowlist(허용 목록) 안의 packet/closeout 배선 보정으로만 제한하며, gate 완화, threshold 완화, test skip, runtime/model logic 변경은 금지한다.

### 작은 작업 최소 모드(Small-Work Minimal Mode, 작은 작업 최소 모드)

`non-trivial work packet(비사소 작업 묶음)`은 파일 수정(file mutation, 파일 수정), 실행(run, 실행), MT5(`MetaTrader 5`, 메타트레이더5), 모델/model export(모델/모델 내보내기), 정책/스킬 변경(policy/skill change, 정책/스킬 변경), publish/push(게시/원격 반영), 상태 동기화(state sync, 상태 동기화), 또는 `completed/reviewed/verified(완료/검토/검증)` 같은 강한 claim(주장)을 만드는 작업이다.

그 밖의 좁은 status(상태), path/hash/register recount(경로/해시/등록부 재확인), read-only review(읽기 전용 검토), 짧은 질문 답변은 `trivial or information_only packet(사소 또는 정보 전용 작업 묶음)`으로 다룰 수 있다.

작은 작업의 기본값(default, 기본값)은 delta reentry(변화분 재진입), primary skill only(주 스킬만), support skills 0-1개(보조 스킬 0-1개), compact receipt(압축 영수증), gate N/A with reason(사유 있는 해당 없음)이다. 효과(effect, 효과)는 작은 작업이 전체 운영 스택(full operating stack, 전체 운영 스택)으로 커지는 것을 막는 것이다.

이 최소 모드는 gate(게이트), threshold(임계값), evidence requirement(근거 요구), MT5 runtime probe(MT5 런타임 탐침), final claim guard(최종 주장 보호)를 완화하지 않는다. 작업이 파일 수정, 실행, stage closeout(단계 마감), runtime/backtest(런타임/백테스트), model export(모델 내보내기), 또는 publish/push(게시/원격 반영)로 넘어가면 즉시 non-trivial packet(비사소 작업 묶음)으로 승격한다.

### `/goal` 검증 프로필 규칙(`/goal` Verification Profile Rule, `/goal` 검증 프로필 규칙)

`/goal(목표)` 자체는 full verification(전체 검증), all gates(모든 게이트), all agents(전체 요원), MT5 runtime(MT5 런타임)을 자동으로 켜는 trigger(트리거)가 아니다. Codex(코덱스)는 먼저 work packet(작업 묶음)에 `verification_profile(검증 프로필)` 하나를 고르고, 그 profile(프로필)은 `claim_surface(주장 표면)`가 결정한다.

허용 profile id(프로필 ID)의 진실 원천(source of truth, 진실 원천)은 `docs/agent_control/work_family_registry.yaml`의 `verification_profiles(검증 프로필)`다. 기본 효과(effect, 효과)는 `/goal(목표)` 운영이 안정적으로 돌아가되, 불안감이나 습관 때문에 무거운 검증을 덧붙이지 않게 하는 것이다.

모든 verification action(검증 행동)은 `trigger_source(트리거 원천)`, `protected_claim(보호 주장)`, `required_evidence(필수 근거)`, `stop_condition(중단 조건)`을 가져야 한다. `trigger_source(트리거 원천)`가 없으면 그 검증은 실행하지 않는다. 효과(effect, 효과)는 random verification(무작위 검증)을 막고, 필요한 검증만 packet(묶음)에 남기는 것이다.

`required_gates(필수 게이트)`는 family base gates(작업군 기본 게이트) + active overlay gates(활성 오버레이 게이트) + profile extra gates(프로필 추가 게이트)를 합친 뒤 중복 제거(dedupe, 중복 제거)한다. `verification_profile(검증 프로필)`은 protected claim(보호 주장)에 필요한 gate(게이트), threshold(임계값), evidence requirement(근거 요구), MT5 output(MT5 출력), Task Force actual call(태스크포스 실제 호출)을 제거하거나 완화할 수 없다.

gate(게이트)를 실행하지 않을 때는 `not_applicable_with_reason(사유 있는 해당 없음)`를 gate별 구조화 기록(structured record, 구조화 기록)으로 남긴다. 최소 필드는 `gate(게이트)`, `reason_code(사유 코드)`, `reason(사유)`, `claim_effect(주장 효과)`다. 효과(effect, 효과)는 “검증 안 함”이 조용히 통과되지 않고, 어떤 claim(주장)을 포기하거나 낮췄는지 보이게 하는 것이다.

Runtime/MT5(런타임/MT5) 검증은 runtime claim(런타임 주장), Strategy Tester output(전략 테스터 출력), EA/ONNX handoff(EA/ONNX 인계), `.mq5/.mqh/.set` behavior(`.mq5/.mqh/.set` 동작), 또는 operating promotion/runtime authority/live readiness(운영 승격/런타임 권위/실거래 준비) 주장에만 켠다. Design/proxy/Python-only(설계/프록시/파이썬 전용) 작업은 MT5 Strategy Tester(전략 테스터)를 자동 요구하지 않는다.

Governance stays lightweight(운영은 가볍게 유지): Codex(코덱스)는 claim(주장)을 보호하는 가장 작은 router/profile/skill set(라우터/프로필/스킬 묶음)을 고른다. Evidence stays heavyweight(근거는 무겁게 유지): 강한 claim(주장)은 그 claim(주장)에 맞는 artifact/run/hash/MT5 output/actual Task Force call(산출물/실행/해시/MT5 출력/실제 태스크포스 호출)을 요구한다. 이 규칙은 새 gate/overlay/family/skill/agent call/review pass(게이트/오버레이/작업군/스킬/요원 호출/검토 회차)를 만들지 않는다.

When a protected claim(보호 주장)을 narrow sufficient run(좁고 충분한 실행)으로 시험할 수 있으면, Codex(코덱스)는 procedural expansion(절차 확장), advisory loop(자문 반복), deferred checkpoint(지연 점검)를 늘리는 것보다 active verification(능동 검증)을 우선한다. 효과(effect, 효과)는 운영 문장은 작게 유지하고 토큰/시간을 실제 근거 생성에 쓰게 하는 것이다.

Runtime/materialization/handoff/economics claim(런타임/물질화/인계/경제성 주장)이 걸린 work packet(작업 묶음)은 runtime probe(런타임 탐침)를 cost/expense(비용)를 이유로 다음 작업(next work, 다음 작업)으로 미루지 않는다. 같은 packet(묶음)에서 가장 좁은 충분한 runtime probe(런타임 탐침)를 시도하거나, 복구 시도(recovery attempt, 복구 시도) 뒤 `blocked/inconclusive/out_of_scope_by_claim(차단/불충분/주장 범위 밖)`으로 낮춘다. Probe(탐침)가 없으면 `runtime verified/economics pass/materialization-ready/handoff complete(런타임 검증됨/경제성 통과/물질화 준비/인계 완료)`를 주장하지 않는다.

Runtime learning probe(런타임 학습 탐침)는 strong candidate(강한 후보)와 learning candidate(학습 후보)를 분리한다. Proxy bad(프록시 부진), candidate gate failed(후보 게이트 실패), not strong candidate(강한 후보 아님), low trade count expected(거래 수 부족 예상), long/short imbalanced(롱숏 비대칭), cost expensive(비용/무거움), agent recommended skip(요원 권고 생략)는 MT5 not-run reason(MT5 미실행 사유)이 아니다. Pre-gate signal row(사전 게이트 신호 행)나 deterministic decision surface(결정 가능한 판단 표면)가 있어 runtime_learning_probe_candidate(런타임 학습 탐침 후보)를 만들 수 있으면 같은 packet(묶음)에서 `runtime_learning_probe_decision_gate(런타임 학습 탐침 결정 게이트)`를 실행하고 `mt5_action(MT5 행동)`을 `run_probe(탐침 실행)` 또는 `run_after_repair(수리 후 탐침 실행)`로 둔다. No actionable runtime surface(실행 가능한 런타임 표면 없음)는 즉시 생략 사유가 아니며, 최소 한 번의 repair_attempt(수리 시도) 뒤에만 `blocked/inconclusive/out_of_scope_by_claim(차단/불충분/주장 범위 밖)`으로 낮출 수 있다. 효과(effect, 효과)는 “성공 후보는 아님”과 “런타임 학습도 시도하지 않음”을 분리하고, F97 같은 candidate=0(후보 0건) 상황에서도 조용한 MT5 생략을 막는 것이다.

### MT5 Runtime Probe Contract(MT5 런타임 탐침 계약)

MT5 runtime probe(런타임 탐침)의 기간(period, 기간), 실행 방식(execution mode, 실행 방식), 완료 주장(completion claim, 완료 주장)의 진실 원천(source of truth, 진실 원천)은 `foundation/config/mt5_runtime_probe_contract.yaml`이다. Standard runtime probe(표준 런타임 탐침)는 `validation_is(검증 내부) 2025.01.02 -> 2025.10.01`과 `oos(표본외) 2025.10.01 -> 2026.04.13` 쌍을 사용한다. `validation_is(검증 내부)`가 정상 존재하고 `oos(표본외)`가 2026년 4월 stage-native horizon(단계 고유 종료선)까지 있으면 정상 범주로 보고 2026년 6월까지 억지 확장하지 않는다. 수리/개발 여지가 남아있을 때도 같은 기간(2026년 4월 종료선) 안에서 다시 수리/개발하고 마무리한다.

실행은 `run_mt5_tester(MT5 테스터 실행)` 경로를 우선하며 `terminal64.exe /portable(터미널 포터블 모드)`를 요구한다. Tester setting(테스터 설정)은 `US100`, `M5`, `Model=4(모델 4)`, `Deposit=500(예치금 500)`, `Leverage=1:100(레버리지 1:100)`, local agent only(로컬 에이전트만), remote/cloud off(원격/클라우드 끔), `ReplaceReport=1(보고서 교체)`, `ShutdownTerminal=1(터미널 종료)`를 기본으로 둔다.

`runtime_probe_completed(런타임 탐침 완료)`는 standard probe profile(표준 탐침 프로필)에서 validation_is(검증 내부)와 oos(표본외)가 모두 있고, 각 standard attempt(표준 시도)에 completed Strategy Tester report(완료된 전략 테스터 보고서)가 있을 때만 주장한다. Strategy Tester report(전략 테스터 보고서) missing(누락)은 완료 사유가 아니라 점검/차단 사유다.

`runtime_surface_contract(런타임 표면 계약)`도 완료 조건이다. `full_period_deterministic(전체 기간 결정 표면)` 또는 `full_period_sparse_decision_surface(전체 기간 희소 결정 표면)`만 `runtime_probe_completed(런타임 탐침 완료)`에 쓸 수 있다. `score_sample(점수 샘플)`, `proxy_score_sample(프록시 점수 샘플)`, `diagnostic_sample(진단 샘플)`, `preview_rows(미리보기 행)`로 만든 MT5 실행은 runtime learning observation(런타임 학습 관찰)만 만들고 완료, runtime authority(런타임 권위), economics pass(경제성 통과), materialization_ready(물질화 준비)를 만들 수 없다. 효과(effect, 효과)는 표준 기간으로 테스터를 돌렸더라도 입력 표면이 샘플이면 자동으로 claim boundary(주장 경계)를 낮추게 하는 것이다.

`materialization_smoke(물질화 스모크)`, `debug_reproduction(디버그 재현)`, `specific_period_probe(특정 기간 탐침)`, `regime_slice_probe(장세 조각 탐침)`, `source_replay(원천 재현)`는 명시 예외 profile(프로필)이다. 이 예외는 runtime learning(런타임 학습)이나 blocked reason(차단 사유)을 만들 수 있지만 `runtime_probe_completed(런타임 탐침 완료)`, runtime authority(런타임 권위), economics pass(경제성 통과)를 만들 수 없다.

기간이 이상하면 자동 수정(auto-fix, 자동 수정)으로 통과시키지 않는다. 애초에 계약에서 생성하고, 어긋나면 `mt5_runtime_probe_contract(엠티5 런타임 탐침 계약)` audit(감사)에서 blocked(차단)로 닫는다. 효과(effect, 효과)는 이상한 기간/이상한 실행 위치로 돌린 뒤 완료처럼 말하는 흐름을 막는 것이다.

## Codex Task Force 운영 규칙(Codex Task Force Operating Rule, 코덱스 태스크포스 운영 규칙)

Project Obsidian Prime v2는 Grok role succession(그록 역할 승계)이 아니라 project-native Codex Task Force operating system(프로젝트 전용 코덱스 태스크포스 운영체계)을 쓴다.

영구 roster(명단)의 진실 원천(source of truth, 진실 원천)은 `docs/agent_control/codex_task_force_registry.yaml`이다. 실제 Codex custom agent(코덱스 사용자 정의 요원) 파일은 `.codex/agents/<roster_id>.toml`에 두며, roster id(명단 ID), TOML file stem(TOML 파일명), TOML `name`(TOML 이름)은 서로 같아야 한다. 새 대화창이나 cold start(냉시작)에서도 같은 8명 agent(요원)를 같은 역할로 불러야 한다.

model policy(모델 정책)는 현재 `gpt-5.5 xhigh(5.5 매우 높음)`를 floor(하한)로 둔다. 더 높은 Codex model(코덱스 모델)이 허용되면 사용자가 명시적으로 고정하지 않는 한 `highest available xhigh(사용 가능 최상위 매우 높음)`로 자동 교체한다. 효과(effect, 효과)는 최신 상위 모델을 쓰되, model strength(모델 강도)가 gate(게이트), threshold(임계값), evidence requirement(근거 요구), claim boundary(주장 경계)를 완화하지 못하게 하는 것이다.

`obsidian-task-force-review(태스크포스 검토)`는 internal adversarial review(내부 비판 검토)와 agent routing(요원 라우팅)을 맡는다. 각 agent opinion(요원 의견)은 `accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)`로 분류하고, Codex(코덱스)가 local verification(로컬 검증)과 final direction(최종 방향)을 계속 소유한다.

Task Force(태스크포스)의 기본 호출 방식(default call mode, 기본 호출 방식)은 `micro_consult(소형 상담)`다. 보통은 1명 agent(요원)만 부르고, 두 remit(임무)가 겹칠 때만 2명 agent(요원)를 부른다. `micro_consult(소형 상담)`는 advisory(자문)로만 기록하고 `reviewed/verified/pass(검토됨/검증됨/통과)`나 Task Force reviewed(태스크포스 검토됨)의 근거가 아니다. 효과(effect, 효과)는 관련 작업마다 필요한 요원만 적재적소에 부르게 하는 것이다.

3명 이상 agent(요원)를 호출하려면 `escalation_reason(확대 사유)`를 남긴다. 5명 이상 agent(요원)를 호출하려면 `why_not_smaller(왜 더 작게 못 했는지)`를 남긴다. 8명 전원 호출은 `escalation_reason(확대 사유)`, `why_not_smaller(왜 더 작게 못 했는지)`, `full_roster_call_reason(전원 호출 사유)`를 모두 남긴다. 효과(effect, 효과)는 한 번에 여섯 명씩 부르는 습관을 막고, 큰 검토가 필요한 경우에만 큰 검토로 키우는 것이다.

formal Task Force review(공식 태스크포스 검토)는 stage closeout(단계 마감), policy change(정책 변경), runtime authority(런타임 권위), operating promotion(운영 승격), cross-system handoff(교차 시스템 인계), 또는 protected reviewed/verified/pass claim(보호된 검토/검증/통과 주장)에만 쓴다. formal review(공식 검토)가 trigger(트리거)되면 Codex(코덱스)는 먼저 work packet claim surface(작업 묶음 주장 표면), required gate(필수 게이트), roster remit(명단 임무)에 맞는 최소 관련 custom agent(사용자 정의 요원)만 registry(등록부) 기준으로 고르고, `reviewed/verified/pass(검토됨/검증됨/통과)`나 Task Force reviewed(태스크포스 검토됨)를 주장하기 전에 선택한 요원을 즉시 실제 `spawn_agent(서브에이전트 생성 호출)`로 호출한다. 효과(effect, 효과)는 self-review(자기검토)나 `micro_consult(소형 상담)`를 Task Force review(태스크포스 검토)처럼 포장하지 않고, 필요한 요원 호출 증거를 먼저 만들게 하는 것이다.

formal Task Force review(공식 태스크포스 검토)가 active goal(`/goal`, 활성 목표), work packet(작업 묶음), required gate(필수 게이트), family rule(작업군 규칙), router-selected required Task Force overlay(라우터가 선택한 필수 태스크포스 오버레이), explicit user instruction requiring review(검토를 요구하는 명시 사용자 지시), 또는 closeout claim(마감 주장)에 필요하면 `spawn_agent(서브에이전트 생성 호출)` 도구 없음이나 미호출은 `blocked_for_task_force_review(태스크포스 검토 차단)`다. `not_applicable_with_reason(사유 있는 해당 없음)`나 claim boundary lowering(주장 경계 낮춤)으로 통과시킬 수 없고, `reviewed/verified/pass/stage closeout pass/internally_reviewed/rehearsed_control_plane(검토됨/검증됨/통과/단계 마감 통과/내부 검토됨/제어면 리허설됨)`을 주장하지 않는다. optional micro_consult(선택 소형 상담)에서 current tool metadata(현재 도구 메타데이터)가 custom agent(사용자 정의 요원)를 아직 노출하지 않으면 compatibility fallback(호환 대체)을 쓸 수 있지만, claim effect(주장 효과)는 `advisory_only_no_reviewed_pass(자문 전용, 검토/통과 아님)`로 낮춘다. dormant/stale agent(대기 중이거나 낡은 맥락의 요원) 의견은 최신 context update(맥락 갱신) 없이 검토 근거로 쓰지 않는다.

internal adversarial review(내부 비판 검토)는 기본 2회차(pass, 회차)로 제한한다. 1차는 critique(비판), 2차는 owner response plus local verification(소유자 응답 + 로컬 검증)이다. 3차는 new evidence(새 근거)가 있을 때만 허용한다. 효과(effect, 효과)는 검토가 과한 loop(반복)가 되지 않으면서도 rubber stamp(형식 승인)가 되지 않게 하는 것이다.

active five-stage Grok retrospective(활성 5단계 그록 회고)는 retired/archive-only(퇴역/보관 전용)로 비활성화한다. 기존 Grok review(그록 검토), register(등록부), report(보고서)는 historical evidence(역사 근거)로 보존한다.

효과(effect, 효과)는 Grok(그록)을 의식해 역할을 승계하지 않고, 프로젝트 철학과 근거 규율에 맞는 자체 운영 체계를 유지하는 것이다.

## Grok 보관 규칙(Grok Archive Rule, 그록 보관 규칙)

Grok(Grok, 그록)은 더 이상 active review path(활성 검토 경로), external review path(외부 검토 경로), second opinion path(2차 의견 경로), stage closeout gate(단계 마감 게이트), agent/skill consulting path(요원/스킬 상담 경로)로 쓰지 않는다.

사용자가 Grok 호출(call, 호출)이나 Grok 검토(review, 검토)를 말해도 새 Grok 호출을 만들지 않고, 그 문구만으로 Task Force review(태스크포스 검토)도 켜지 않는다. 외부 리뷰(external review, 외부 리뷰), 2차 의견(second opinion, 2차 의견), Codex 단독 판단 금지(no solo Codex judgment, 코덱스 단독 판단 금지), 또는 stage close 비판 검토(stage-close adversarial review, 단계 마감 비판 검토)가 active review request(활성 검토 요청)이면 `obsidian-task-force-review(태스크포스 검토)`의 internal adversarial review(내부 비판 검토)와 agent roster(요원 명단)로 라우팅한다.

`obsidian-grok-collaboration(그록 협업)`은 retired/archive-only skill(퇴역/보관 전용 스킬)이다. 새 prompt(프롬프트), wrapper call(래퍼 호출), Grok output(그록 출력), Grok receipt(그록 영수증), Grok gate(그록 게이트)를 만들지 않는다. 기존 `docs/agent_control/grok_reviews/`와 과거 stage artifact(단계 산출물)는 historical evidence(역사 근거)로만 읽는다.

효과(effect, 효과)는 새 대화창이나 cold start(냉시작)에서도 Grok(그록) 잔재가 운영 의사결정으로 역류하지 않고, 모든 비판 검토와 요원 상담이 Project-native Codex Task Force(프로젝트 전용 코덱스 태스크포스)에서 처리되게 하는 것이다.

### 5단계 Grok 중간 검토 보관(Five-Stage Grok Retrospective Archive, 5단계 그록 중간 검토 보관)

Five-stage Grok retrospective(5단계 그록 중간 검토)는 retired operating memory(퇴역 운영 기억)다. `docs/registers/five_stage_retrospective_register.yaml`와 기존 report(보고서)는 삭제하지 않고 historical archive(역사 보관소)로 보존한다.

이 보관 기록은 다음 frontier stage open(다음 전선 단계 개방)을 차단하지 않고, Grok call(그록 호출), Grok packet(그록 묶음), next-open block(다음 개방 차단), Goal Achieve(목표 달성), runtime authority(런타임 권위)를 만들 수 없다.

향후 5단계 단위 회고가 필요하면 Grok(그록)이 아니라 Codex Task Force replacement retrospective(코덱스 태스크포스 대체 회고)로 별도 policy(정책)를 만든다.

## 가장 중요한 원칙(Non-Negotiable Principle, 양보 불가 원칙)

탐색(exploration, 탐색)에는 게이트(gate, 제한문)가 없다.

`Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 데이터 완전성(data completeness, 데이터 완전성)이나 문맥 상태(context quality, 문맥 품질)를 설명하는 라벨(label, 라벨)일 뿐이다.

제한(restriction, 제한)은 운영 의미(operational meaning, 운영 의미)를 주장할 때만 붙는다. 예를 들면 실거래(live use, 실거래), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)이다.

## 티어 쌍 작업(Paired Tier Work, 티어 쌍 작업)

Stage 10(10단계) 이후 알파 탐색(alpha exploration, 알파 탐색)은 `Tier A(티어 A)`와 `Tier B(티어 B)`를 항상 같은 작업 묶음(work packet, 작업 묶음)에서 함께 다룬다.

필수 기록(required records, 필수 기록)은 세 가지다.

- `Tier A separate(Tier A 분리)`
- `Tier B separate(Tier B 분리)`
- `Tier A+B combined(Tier A+B 합산)`

효과(effect, 효과)는 `Tier A(티어 A)`만 본 결과를 전체 알파 판독(alpha read, 알파 판독)처럼 과장하지 않고, `Tier B(티어 B)`의 부분 문맥 표본(partial-context sample, 부분 문맥 표본)이 같은 아이디어에서 무엇을 바꾸는지 함께 보게 하는 것이다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서 사용자가 `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)`을 의도하면, 위 세 기록은 각각 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 해석한다.

효과(effect, 효과)는 Tier A(티어 A)의 빈 구간을 Tier B(티어 B)가 실제로 메웠는지 기록하고, separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)을 combined result(합산 결과)로 오해하지 않게 하는 것이다.

`Tier B(티어 B)`나 합산 기록(combined record, 합산 기록)을 만들 수 없으면 생략하지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 적는다.

## 점진적 경화(Progressive Hardening, 점진적 경화)

- 초기 탐색(early exploration, 초기 탐색)은 빠진 근거를 이름 붙이면 시작할 수 있다.
- `promotion_candidate(승격 후보)`는 비교할 가치가 있다는 뜻이지, 운영선을 교체한다는 뜻이 아니다.
- `runtime_probe(런타임 탐침)`는 런타임을 관찰한다는 뜻이지, 런타임 권위가 닫혔다는 뜻이 아니다.
- `operating_promotion(운영 승격)`과 `runtime_authority(런타임 권위)`는 강한 근거가 필요하다.
- `promotion-ineligible(승격 부적격)`은 아이디어 사망(idea-dead, 아이디어 사망)이 아니다.

## 단계 규칙(Stage Rule, 단계 규칙)

프로젝트는 단계(stage, 단계)로 관리한다.

각 단계는 번호(number, 번호)와 짧은 부제(subtitle, 부제)를 함께 쓴다.

`NN_area__specific_question`

부제(subtitle, 부제)는 이번 단계의 질문(question, 질문)을 설명한다. 미래의 모든 알파(alpha, 알파)를 한 단계 안에 가두면 안 된다.

모델 학습(model training, 모델 학습)과 검증(validation, 검증)이 실제로 가능해지는 순간부터 알파 탐색(alpha research, 알파 탐색)을 시작할 수 있다. 고정된 단계 번호에 묶지 않는다.

## 전선 단계 규칙(Frontier Stage Rule, 전선 단계 규칙)

Stage364(364단계) 이후 새 큰 연구 단위(research unit, 연구 단위)는 `stage_frontier_NN__specific_question(전선 단계 번호와 구체 질문)` 형식을 쓸 수 있다.

`stage_frontier_NN(전선 단계 번호)`은 Stage365(365단계) continuation(연속)이 아니다. independent frontier campaign(독립 전선 캠페인)이다.

핵심 규칙(core rule, 핵심 규칙)은 `reference, not inheritance(참조이지 상속 아님)`이다. Stage12~364(12~364단계)는 prior-stage archive(이전 단계 보관소)로 읽고, preserved clue(보존 단서), negative memory(부정 기억), reusable artifact(재사용 산출물), do-not-repeat note(반복 금지 메모)만 가져온다.

winner(승자), selected baseline(선택 기준선), promotion history(승격 이력), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 prior stage(이전 단계)에서 가져오지 않는다.

Frontier stage(전선 단계)는 새 최상위 `frontiers/` folder(폴더)를 만들지 않고 기존 `stages/*` 아래에 둔다. 세부 운영 규칙(source of truth, 진실 원천)은 `docs/policies/frontier_governance.md`다.

Frontier open(전선 개방)은 `frontier_topic_rotation_check(전선 주제 회전 점검)`를 거친다. 최근 5개 정식 frontier closeout(전선 마감)과 직전 단계(stage, 단계)를 기준으로, 다음 단계가 continuation repair(연속 수리), near-duplicate hypothesis(근접 중복 가설), threshold/filter/session/routing/parameter-only tweak(임계값/필터/세션/라우팅/파라미터만 미세조정), 또는 repair disguised as a new hypothesis(새 가설로 위장한 수리)가 아닌지 기록한다.

수리는 같은 frontier stage(전선 단계) 안에서 repair disposition(수리 처분)을 닫는다. repaired/negative/invalid/blocked/out_of_scope(수리됨/부정/무효/차단/주장 범위 밖) 중 무엇이든 같은 단계(stage, 단계) 안에서 근거와 함께 결론을 남긴 뒤에만 transition(전환)할 수 있다. blocked(차단)는 다음 단계가 같은 수리를 이어받아도 된다는 뜻이 아니다.

같은 broad topic(넓은 주제)은 나중에 다시 등장할 수 있다. 금지되는 것은 topic(주제) 자체가 아니라 인접한 frontier open(전선 개방)을 같은 surface repair(동일 표면 수리)나 이름만 바꾼 가설로 계속 미는 것이다. 다시 등장하려면 source/data representation/label/runtime representation/validation philosophy/model family/objective/trade shape/risk logic/regime split(원천/데이터 표현/라벨/런타임 표현/검증 철학/모델 계열/목적함수/거래 형태/위험 로직/장세 분할) 중 material novelty delta(실질 신규성 차이)를 적는다.

`frontier_topic_rotation_check(전선 주제 회전 점검)` 실패는 현재 proposed next-open shape(제안된 다음 개방 형태)만 막는다. 같은 topic(주제) 자체를 future stage(미래 단계)에서 금지하지 않는다.

`frontier_five_stage_direction_synthesis(전선 5단계 방향 종합)`는 Topic Rotation Guard(주제 회전 보호)와 Extra Stage(추가 단계) 사이의 가벼운 방향 기록이다. 최근 5개 정식 frontier closeout(전선 마감)의 dominant direction/repeated mechanism/overused axis warning/next-axis options(지배 방향/반복 메커니즘/과사용 축 경고/다음 축 후보)을 요약하지만, retrospective(회고), heavy review(무거운 검토), topic abandonment(주제 폐기), permanent topic ban(영구 주제 금지)을 만들지 않는다. 같은 topic(주제)은 나중에 새 axis/evidence(새 축/근거)로 다시 실험할 수 있고, 이 기록이 막는 것은 adjacent same-axis continuation(인접 동일 축 연속)뿐이다.

## 전선 추가 단계 규칙(Frontier Extra Stage Rule, 전선 추가 단계 규칙)

Frontier Extra Stage(전선 추가 단계)는 `stage_frontier_extra_EXX__specific_question(전선 추가 단계 번호와 구체 질문)` 형식으로 둔다. 새 최상위 `frontiers/` 또는 `extra_stages/` folder(폴더)는 만들지 않는다.

Trigger(트리거)는 closed canonical frontier stage(마감된 정식 전선 단계) 50개마다 발동한다. F50/F100/F150...(전선50/100/150...) closeout(마감) 뒤 다음 frontier open(다음 전선 개방) 전에 `frontier_extra_due_check(전선 추가 도래 점검)`를 먼저 한다. broad goal(넓은 목표), 예를 들어 “개쩌는 ONNX(온엑스) 만들어줘”가 들어와도 같은 due check(도래 점검)를 실행한다.

Due(도래)이면 E01/E02/E03...(추가01/02/03...)을 먼저 open -> operate -> closeout(개방 -> 운영 -> 마감)한다. 그 뒤 resume frontier(재개 전선)로 돌아간다. E01(추가01)은 F01-F50(전선01-50)을 재료로 쓰고, E02(추가02)는 F51-F100(전선51-100)을 재료로 쓴다. backfill execution(소급 실행)이 필요한 경우에도 같은 numbering(번호)을 유지한다.

Extra stage(추가 단계)는 retrospective(회고)가 아니다. 50개 frontier closeout(전선 마감)을 ingredient card(재료 카드)로 만들고, feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 공격적으로 섞어 실제 MT5 runtime learning campaign(MT5 런타임 학습 캠페인)까지 밀어본다.

E02(추가02)부터 모든 Frontier Extra Stage(전선 추가 단계)는 progressive mix depth(점증 혼합 깊이) 계약을 쓴다. 50!(팩토리얼) 전체 조합이나 exhaustive mix(전체 혼합 탐색)는 금지한다. 기본 순서는 2-mix -> 3-mix -> 4-mix(2개 혼합 -> 3개 혼합 -> 4개 혼합)이고, 다음 depth(깊이)는 이전 depth(깊이)의 diversity/risk/reproducibility/materialization(다양성/위험/재현성/물질화) gate(게이트)가 통과할 때만 연다.

기본 cap(상한)은 2-mix queue 60/materialized 6/MT5 attempts 12(2개 혼합 대기열 60/물질화 6/MT5 시도 12), 3-mix queue 36/materialized 4/MT5 attempts 8(3개 혼합 대기열 36/물질화 4/MT5 시도 8), 4-mix queue 12/materialized 2/MT5 attempts 4(4개 혼합 대기열 12/물질화 2/MT5 시도 4)다. invalid/block recovery(무효/차단 복구)를 포함해 전체 hard cap(절대 상한)은 30 MT5 attempts(MT5 시도 30회)다.

selection lane(선정 선로)은 PF(수익 팩터), DD resilience(손실폭 회복력), density/materiality(밀도/물질성), runtime materialization(런타임 물질화), negative-memory repair(부정 기억 수리)로 나눈다. `top_forward_pf(상위 전진 수익 팩터)`는 전체 MT5 후보의 25%를 넘을 수 없다. 효과(effect, 효과)는 “개쩌는 ONNX(온엑스) 만들어줘” 같은 broad goal(넓은 목표)이 들어와도 조합 폭발이나 PF-only selection(PF 단독 선정)으로 흐르지 않고, 깊이별 runtime learning record(런타임 학습 기록)를 남기게 하는 것이다.

Ingredient card receipt(재료 카드 영수증)는 source frontier/run(원천 전선/실행), hypothesis(가설), axis tags(축 태그), artifact path/hash(산출물 경로/해시), salvage value/negative memory/do-not-repeat(회수 가치/부정 기억/반복 금지), tier scope(티어 범위), claim boundary(주장 경계), selection eligibility/lane candidates(선정 자격/선정 선로 후보)를 남긴다. Mix queue receipt(혼합 대기열 영수증)는 mix id/depth/source card ids(혼합 ID/깊이/원천 카드 ID), axis tags(축 태그), selection lanes(선정 선로), novelty delta(신규성 차이), near-duplicate cluster(근접 중복 군집), sample method(표본 방식), selected-for-runtime flag(런타임 선택 여부), selection reason/risk notes(선정 사유/위험 기록), claim boundary(주장 경계)를 남긴다.

Depth receipt(깊이 영수증)는 selection lane counts/top_forward_pf share/runtime substrate count/single_substrate_warning/full_mix_materialized=false/claim_effect(선정 선로별 수/상위 전진 수익 팩터 비율/런타임 바탕 수/단일 바탕 경고/전체 혼합 물질화 아님/주장 효과)를 남긴다. Materialized attempt(물질화 시도)는 dataset/feature/label/split identity(데이터셋/피처/라벨/분할 정체성), parser/runtime contract version(파서/런타임 계약 버전), ONNX/EA/set/feature/tester/report/trade-list/telemetry hash(온엑스/EA/설정/피처/테스터/보고서/거래목록/텔레메트리 해시)를 남긴다. compile-only(컴파일 단독)와 proxy-only(프록시 단독)는 runtime evidence(런타임 근거)가 아니다.

Extra stage closeout(추가 단계 마감) 전에는 `frontier_extra_mix_depth_lint(전선 추가 혼합 깊이 점검)`를 실행한다. cap 초과, PF-only selection(PF 단독 선정), compile-only runtime evidence(컴파일 단독 런타임 근거), single substrate warning missing(단일 바탕 경고 누락)은 blocked(차단) 또는 lowered claim boundary(낮춘 주장 경계)로 닫는다.

MT5 failure(MT5 실패), zero-trade(무거래), mismatch(불일치), crash/block(충돌/차단), PF/DD collapse(수익 팩터/손실폭 붕괴), density death(밀도 사망)는 waste(낭비)가 아니라 negative evidence(부정 근거)다. compile(컴파일)만으로 runtime evidence(런타임 근거)를 대체하지 않는다.

Extra stage closeout(추가 단계 마감)은 preserved clue/negative memory/seed surface/reference surface/invalid setup/blocked retry condition/next frontier proposal(보존 단서/부정 기억/씨앗 표면/참고 표면/무효 설정/차단 재시도 조건/다음 전선 제안) 중 하나 이상으로 닫는다.

금지 claim(주장)은 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), git push as validation(깃 원격 반영을 검증으로 간주)이다.

## 알파 탐색 단계 규칙(Alpha Exploration Stage Rule, 알파 탐색 단계 규칙)

Stage 10(10단계)부터 알파 탐색(alpha exploration, 알파 탐색)이 닫히는 단계(stage, 단계)까지는 탐색 라벨(exploration label, 탐색 라벨)과 실행 번호(run number, 실행 번호) 규칙을 쓴다.

- 정식 단계 이름(canonical stage id, 정식 단계 ID)은 `NN_area__specific_question`을 유지한다.
- 탐색 라벨(exploration label, 탐색 라벨)은 `stageN_exploration_group__specific_detail`을 쓴다. 예: `stage10_Model__LGBM`.
- 실행 번호(run number, 실행 번호)는 `run01A`, `run01B`, `run01C`처럼 단계 로컬 순서 번호(stage-local sequence number, 단계 로컬 순서 번호)다.
- 실행 번호(run number, 실행 번호)는 탐색 상한(limit, 한계)이나 역할 고정(role lock, 역할 고정)이 아니다.
- 해당 단계(stage, 단계)는 핵심 주제(core topic, 핵심 주제)를 끝까지 학습(training, 학습), 최적화(optimization, 최적화), 압박 시험(stress test, 압박 시험)한 뒤 다음 단계(next stage, 다음 단계)로 간다.
- 알파 탐색 단계 전환(alpha exploration stage transition, 알파 탐색 단계 전환)은 기준선 선택(baseline selection, 기준선 선택)이 아니라 주제 전환(topic pivot, 주제 전환)이다. 명시적 승격/운영 작업 묶음(explicit promotion/operating packet, 명시적 승격/운영 작업 묶음)이 없으면 마감 단계(closeout stage, 마감 단계)에서 기준선(baseline, 기준선)을 만들지 않는다.

효과(effect, 효과)는 모든 새 작업 회차(pass, 회차)가 알파 탐색(alpha exploration, 알파 탐색)을 좁게 닫지 않고, 같은 단계(stage, 단계) 안에서 끝까지 밀어붙이게 하는 것이다.

## 티어 규칙(Tier Rule, 티어 규칙)

- `Tier A(티어 A)`: 전체 문맥 표본(full-context sample, 전체 문맥 표본)
- `Tier B(티어 B)`: 부분 문맥 표본(partial-context sample, 부분 문맥 표본)
- `Tier C(티어 C)`: 약한 표본(weak sample, 약한 표본) 또는 명시적으로 허용된 로컬 연구(local research, 로컬 연구)

모든 티어(tier, 티어)는 탐색할 수 있다. 보고서(report, 보고서)는 무엇을 탐색했는지만 정직하게 라벨링(labeling, 라벨링)하면 된다.

## 구조 불변 규칙(Architecture Invariants, 구조 불변 규칙)

`docs/policies/architecture_invariants.md`가 코드 배치(code placement, 코드 배치)와 경로 규칙(path rule, 경로 규칙)을 담당한다.

- 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)은 `foundation/features`에 둔다.
- 재사용 모델 로직(reusable model logic, 재사용 모델 로직)이 생기면 별도 소유 모듈(owner module, 소유 모듈)에 둔다.
- `foundation/pipelines`는 조율(orchestration, 조율)을 담당한다. 숨은 진실 원천(source of truth, 진실 원천)이 되면 안 된다.
- MT5 EA(`Expert Advisor`, 전문가 자문)는 얇은 진입점(thin entrypoint, 얇은 진입점)과 `foundation/mt5/include/ObsidianPrime/` 모듈(module, 모듈)로 나눈다.
- EA run variant(EA 실행 변형)는 새 `.mq5` 복제(copy, 복사)로 관리하지 않는다. 파라미터만 다르면 `.set` 파일과 `run_manifest.json(실행 목록)`으로 관리하고, 로직(logic, 로직)이 다르면 `.mqh` 모듈 버전(module version, 모듈 버전)을 올린다.
- `stages/*`는 단계 로컬 산출물(stage-local artifact, 단계 로컬 산출물), 보고서(report, 보고서), 실행 근거(run evidence, 실행 근거)를 담는다.

효과(effect, 효과)는 run별 차이(run-specific difference, 실행별 차이)가 코드 파일 이름만 늘리는 방식으로 숨지 않고, 설정(set, 설정), 모듈 해시(module hash, 모듈 해시), 모델/번들 해시(model/bundle hash, 모델/번들 해시), 테스터 출력(tester output, 테스터 출력)으로 추적되게 하는 것이다.

## 윈도우 긴 경로 규칙(Windows Long Path Rule, 윈도우 긴 경로 규칙)

깊은 stage(단계) 산출물, MT5(`MetaTrader 5`, 메타트레이더5) 산출물, `docs/agent_control/packets` 같은 long/deep artifact tree(긴/깊은 산출물 트리)를 다룰 가능성이 있으면 첫 filesystem command(파일시스템 명령)는 `rg --files <repo-relative scope>` 또는 targeted `rg`여야 한다. 넓은 `Get-ChildItem -Recurse`, `Test-Path`, `Resolve-Path`, `Import-Csv`, `Measure-Object`를 첫 명령으로 쓰지 않는다. 효과(effect, 효과)는 실패 후 재시도(retry, 재시도)가 아니라 처음부터 Windows MAX_PATH(윈도우 최대 경로 길이) 함정을 피하는 것이다.

repo-relative discovery(저장소 상대 발견)로 파일 identity(정체성)를 확인한 뒤에도 deep artifact tree(깊은 산출물 트리)의 첫 content read(내용 읽기)나 existence check(존재 확인)는 일반 `Path.read_text`, `Path.read_bytes`, `Path.open`, `Path.exists`, PowerShell(파워셸) `Get-Content`, `Import-Csv`, 또는 pandas direct path(판다스 직접 경로)로 시작하지 않는다. 처음부터 `foundation.control_plane.ledger.io_path`, `path_exists`, 또는 그 helper(보조 함수)를 쓰고, 보고서에는 repo-relative path(저장소 상대 경로)를 남긴다. 효과(effect, 효과)는 `rg`로 발견한 파일을 직접 path API(경로 API)로 다시 못 읽어 missing(누락)처럼 보이는 실패를 시작 단계에서 막는 것이다.

깊은 stage(단계) 산출물이나 MT5(`MetaTrader 5`, 메타트레이더5) 실행 산출물을 다룰 때 PowerShell(파워셸) `Get-Content`, `Get-ChildItem`, 또는 일반 `Path.exists`가 실패하면 곧바로 missing(누락)이나 blocked(차단)로 판정하지 않는다.

필수 첫 읽기/재시도(required first-read/retry, 필수 첫 읽기/재시도)는 repo-relative path(저장소 상대 경로) 기준으로 `rg --files` 또는 `rg`를 먼저 쓰고, 파일 내용이나 CSV/JSON(표/제이슨) 기계 수정이 필요하면 처음부터 `foundation.control_plane.ledger.io_path`를 거쳐 Python(파이썬)에서 연다.

PowerShell(파워셸) `Import-Csv`, `Measure-Object`, 재귀 `Get-ChildItem`이 깊은 frontier stage(전선 단계) 경로에서 `Could not find a part of the path(경로 일부를 찾을 수 없음)`를 내면 같은 cmdlet(명령 도구)을 반복하지 않는다. `cmd /c dir /x`로 확인한 8.3 short path(짧은 경로)나 `io_path` 기반 Python(파이썬) 읽기로 한 번에 전환한다.

효과(effect, 효과)는 Windows MAX_PATH(윈도우 최대 경로 길이) 한계 때문에 존재하는 파일을 없는 파일로 오판하지 않고, durable artifact identity(지속 산출물 정체성)는 계속 repo-relative path(저장소 상대 경로)와 hash(해시)로 남기는 것이다. `\\?\` 같은 extended path prefix(확장 경로 접두사)는 local execution helper(로컬 실행 보조)로만 쓰고 문서 정체성으로 남기지 않는다.

## 경로/이름 해석 사전확인(Path/Name Resolution Preflight, 경로/이름 해석 사전확인)

명확하지 않은 파일(non-obvious file, 명확하지 않은 파일)은 이름을 추정해서 바로 열지 않는다. 다음 중 하나라도 맞으면 preflight(사전확인)를 먼저 한다.

- convention(관례), memory(기억), 다른 repo habit(다른 저장소 습관)에서 추론한 path(경로)다.
- 사용자 문구(user text, 사용자 문구)에 repo-relative confirmation(저장소 상대 경로 확인)이 없다.
- 첫 open/read(열기/읽기)가 한 번 실패했다.
- `docs/contracts/*`, `docs/agent_control/grok_reviews/*/`, stage packet folder(단계 패킷 폴더)처럼 이름 변형(naming variance, 이름 변형)이 있는 산출물군이다.

발견 순서(discovery order, 발견 순서)는 `rg --files` 또는 targeted `rg -g(대상 rg)`를 먼저 쓰고, 그 다음 smallest sufficient directory listing(최소 충분 디렉터리 목록화), 그 다음 필요한 경우 `Get-ChildItem`, 마지막으로 이미 repo-relative identity(저장소 상대 정체성)가 확인된 파일에만 `foundation.control_plane.ledger.io_path` 또는 extended path helper(확장 경로 보조)를 쓴다.

한 번 실패한 뒤에는 adjacent guess(인접 추정)를 반복하지 않는다. 같은 parent directory(상위 폴더)에서 basename(파일명)만 바꾸거나, 같은 artifact role(산출물 역할)의 확장자/접미사만 바꾸는 시도는 adjacent guess(인접 추정)다. 이때는 해당 폴더를 먼저 목록화한다.

discovery(발견)로 바로잡은 경우 wrong assumption(잘못된 가정), repo-relative canonical path(저장소 상대 정식 경로), discovery method(발견 방법)를 작업 기록이나 사용자 업데이트에 짧게 남긴다. 목록화 후에도 없으면 `missing_material(자료 누락)`로 분기하고 가까운 파일을 대체물처럼 쓰지 않는다.

Repo-scoped skill(저장소 전용 스킬)은 기본적으로 `.agents/skills/<skill-name>/SKILL.md`에서 확인한다. 외부 skill path(외부 스킬 경로)는 사용자가 명시했거나 현재 세션의 skill roots(스킬 루트)가 명시할 때만 쓴다.

효과(effect, 효과)는 경로 추정 실수(path assumption mistake, 경로 추정 실수)를 반복하지 않고, Windows long path rule(윈도우 긴 경로 규칙)과 architecture path identity(구조 경로 정체성)를 해치지 않는 것이다. 이 사전확인은 hash(해시), ledger(장부), MT5 evidence identity(MT5 근거 정체성), gate(게이트), threshold(임계값), runtime requirement(런타임 요구)를 대체하지 않는다.

## 탐색 명령(Exploration Mandate, 탐색 명령)

`docs/policies/exploration_mandate.md`가 탐색 규율(exploration discipline, 탐색 규율)을 담당한다.

탐색은 아이디어를 자유롭게 만들고, 정직하게 시험하고, 실패를 기록하며, 운영 조심성(operating caution, 운영 조심성)이 아이디어 필터(idea filter, 아이디어 필터)가 되지 않게 하는 일이다.

## 실행 근거 시스템(Run Evidence System, 실행 근거 시스템)

`docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, `docs/policies/result_judgment_policy.md`가 실행 근거(run evidence, 실행 근거)를 담당한다.

실행(run, 실행)은 측정(measurement, 측정), 정체성(identity, 정체성), 판정(judgment, 판정)이 있어야 검토된 실행(reviewed run, 검토된 실행)이 된다.

프로젝트 장부(project ledger, 프로젝트 장부)는 `docs/registers/alpha_run_ledger.csv`이고, 단계 장부(stage ledger, 단계 장부)는 `stages/<stage_id>/03_reviews/stage_run_ledger.csv`다.

효과(effect, 효과)는 run/subrun/view(실행/하위 실행/보기)를 한 줄씩 모아, Tier A 분리(Tier A separate, Tier A 분리), Tier B 분리(Tier B separate, Tier B 분리), Tier A+B 합산(Tier A+B combined, Tier A+B 합산), Tier A 우선 + Tier B 대체 라우팅(Tier A primary + Tier B fallback routing, Tier A 우선 + Tier B 대체 라우팅), MT5 런타임 탐침(MT5 runtime probe, MT5 런타임 탐침)을 같이 추적하게 하는 것이다.

## 외부 검증 지연 방지(External Verification Anti-Deferral, 외부 검증 지연 방지)

외부 검증(external verification, 외부 검증)이 필요한 주장(claim, 주장)은 다음 작업(next work, 다음 작업)으로 반복해서 밀 수 없다.

- MT5(`MetaTrader 5`, 메타트레이더5), 브로커 터미널(broker terminal, 브로커 터미널), 전략 테스터(strategy tester, 전략 테스터), 파일 인계(file handoff, 파일 인계), 런타임 동등성(runtime parity, 런타임 동등성)에 기대는 주장은 같은 작업 회차(pass, 회차)에서 가장 좁은 충분한 외부 검증(narrow sufficient external check, 좁은 충분 외부 검증)을 먼저 시도한다.
- 도구(tool, 도구), 스크립트(script, 스크립트), 설정(configuration, 설정), 실행 인계 파일(handoff file, 인계 파일)이 낡았거나 없으면 blocked(차단)로 닫기 전에 현재 프로젝트 기준으로 만들거나 고쳐서 실행을 먼저 시도한다.
- MT5 검증(MT5 verification, MT5 검증)에서 MetaEditor compile(메타에디터 컴파일)은 좁은 외부 검증(narrow external check, 좁은 외부 검증)의 일부일 수 있지만, MT5 snapshot(MT5 스냅샷), strategy tester output(전략 테스터 출력), terminal file output(터미널 파일 출력)을 대체하지 않는다.
- 외부 검증이 없으면 그 주장은 검토 완료(reviewed, 검토됨)나 긍정 판정(positive judgment, 긍정 판정)으로 닫지 않는다. 대신 범위를 낮춰 말하거나, 불충분(inconclusive, 불충분), 무효(invalid, 무효), 또는 차단(blocked, 차단)으로 적는다.
- runtime probe(런타임 탐침)는 비싼 선택 점검(expensive optional checkpoint, 비싼 선택 점검)이 아니다. runtime/materialization/handoff/economics claim(런타임/물질화/인계/경제성 주장)을 같은 작업 묶음(work packet, 작업 묶음)에서 좁게 시험할 수 있으면 먼저 시도하고, 못 하면 비용(cost, 비용)이 아니라 도구/환경/산출물 조건(tool/environment/artifact condition, 도구/환경/산출물 조건)과 낮춘 claim boundary(주장 경계)를 남긴다.
- 같은 빠진 외부 검증(missing external verification, 빠진 외부 검증)을 두 번 연속 next work(다음 작업)로만 남기지 않는다. 실행하거나, 현재 도구를 생성/수정해서 실행을 시도하거나, 사용자 행동(user action, 사용자 행동)이 필요한 정확한 terminal action(터미널 행동)을 요청하거나, 주장을 낮추거나, 차단 사유(blocker, 차단 사유)를 기록한다.
- blocked(차단) 판정은 복구 시도(recovery attempt, 복구 시도), 실행 명령(execution command, 실행 명령), 실패 로그(failure log, 실패 로그), 또는 필요한 사용자 행동(user action, 사용자 행동)을 남긴 뒤에만 쓴다.

## 현재 진실(Current Truth, 현재 진실)

- 현재 상태(current state, 현재 상태): `docs/workspace/workspace_state.yaml`
- 현재 설명(current narrative, 현재 설명): `docs/context/current_working_state.md`
- 재진입 순서(re-entry order, 재진입 순서): `docs/policies/reentry_order.md`
- 에이전트 라우팅(agent routing, 에이전트 라우팅): `docs/policies/agent_trigger_policy.md`

## 폴더 규칙(Folder Rules, 폴더 규칙)

- `docs/`: 계약(contract, 계약), 정책(policy, 정책), 현재 상태(current state, 현재 상태), 결정(decision, 결정), 등록부(register, 등록부), 템플릿(template, 템플릿)
- `data/`: 원천 데이터(raw data, 원천 데이터)와 처리 데이터(processed data, 처리 데이터)
- `foundation/`: 재사용 코드(reusable code, 재사용 코드)와 공유 도구(shared tools, 공유 도구)
- `stage_pipelines/`: 단계별 실행 어댑터(stage-specific execution adapter, 단계 전용 실행 어댑터). `foundation/pipelines`의 legacy shim(호환 진입점) 뒤 실제 stage-local orchestration(단계 로컬 실행 지휘)을 둔다. 재사용 모델/피처/런타임 로직(reusable model/feature/runtime logic, 재사용 로직)의 장기 소유자가 되면 안 된다.
- `stages/`: 번호가 붙은 단계 작업(numbered stage work, 번호 단계 작업)
- `tests/`: 재사용 코드 테스트(test, 테스트)
- `.agents/skills/`: 저장소 전용 에이전트 스킬(repo-scoped agent skills, 저장소 전용 에이전트 스킬)

최상위 임시 폴더(scratch folder, 임시 폴더)는 만들지 않는다.

## 인코딩 규칙(Encoding Rule, 인코딩 규칙)

한국어 `.md`와 `.txt` 문서는 UTF-8 with BOM(UTF-8 BOM 포함)을 유지한다.

한국어 `.md/.txt`, repo-scoped skill(저장소 전용 스킬), policy/control-plane markdown(정책/제어면 마크다운)을 만들거나 고칠 가능성이 있으면 첫 write action(쓰기 행동) 전에 encoding surface(인코딩 표면)를 먼저 정한다. 대상 파일 목록, 기존 BOM 상태, 기존 mojibake(문자 깨짐) 또는 repeated BOM(반복 BOM) 여부를 scoped validation(범위 검증)이나 동등한 바이트 검사로 확인한 뒤 작업한다. 효과(effect, 효과)는 인코딩 문제를 “작업 끝 검증”이 아니라 “쓰기 전 차단”으로 옮기는 것이다.

새 한국어 `.md/.txt`는 처음 생성할 때부터 UTF-8 with BOM(UTF-8 BOM 포함)으로 만든다. 기존 대상 파일에 인코딩 부채(encoding debt, 인코딩 부채)가 있으면 조용히 덮어쓰지 않는다. 같은 작업의 touched surface(수정 표면)라면 BOM/mojibake/repeated BOM(바이트 순서 표시/문자 깨짐/반복 BOM) 수리 여부를 명시하고, 범위 밖이면 historical debt(역사 부채)로 분리한다. 효과(effect, 효과)는 새 부채와 기존 부채를 섞지 않는 것이다.

PowerShell(파워셸)에서 BOM 없는 UTF-8(유티에프8) 문서를 BOM 포함으로 바꿀 때는 반드시 읽기에도 `Get-Content -Encoding UTF8 -Raw`를 명시한 뒤 `Set-Content -Encoding UTF8`로 쓴다. 기본 `Get-Content` 읽기는 금지한다. 효과(effect, 효과)는 한국어 문서가 mojibake(문자 깨짐)로 다시 저장되는 일을 막는 것이다.

Git(깃)의 LF/CRLF line-ending warning(줄 끝 경고)은 encoding failure(인코딩 실패)로 판정하지 않는다. 넓은 기계적 문서 수정(broad mechanical rewrite, 넓은 기계적 재작성) 전에는 대상 파일의 줄 끝 표면(line-ending surface, 줄 끝 표면)을 확인하고, 명시 수리 작업이 아니면 기존 줄 끝 관례를 유지한다. 한 파일 안에 LF/CRLF/CR(줄 끝 형식)이 섞인 경우만 mixed line endings(혼합 줄 끝) 경고 또는 범위 수리 대상으로 남긴다. 효과(effect, 효과)는 줄 끝 변동(line-ending churn, 줄 끝 변동)이 인코딩 수리(encoding repair, 인코딩 수리)나 근거 diff(evidence diff, 근거 차이)를 숨기지 못하게 하는 것이다.

`stages/*/02_runs/`처럼 path length(경로 길이)가 긴 산출물은 일반 PowerShell(파워셸) 경로 확인이 실패할 수 있다. 이 경우 `foundation.control_plane.ledger.io_path(입출력 경로)` 또는 `\\?\` long-path prefix(긴 경로 접두사)를 사용한다. 효과(effect, 효과)는 실제 산출물이 존재하는데 missing(누락)으로 오판하는 일을 막는 것이다.
