# Agent Trigger Policy

이 문서는 저장소 전용 스킬(repo-scoped skills)을 언제 쓰는지 정한다.

핵심 원칙은 단순하다. 작업이 커져도, Stage 5부터 미래 Stage 50+까지 같은 방식으로 시작하고, 같은 방식으로 닫는다.

## 정책 참조(Policy References, 정책 참조)

이 정책(policy, 정책)은 다음 문서와 함께 작동한다.

- `docs/policies/architecture_invariants.md`
- `docs/policies/stage_structure.md`
- `docs/policies/exploration_mandate.md`
- `docs/policies/kpi_measurement_standard.md`
- `docs/policies/run_result_management.md`
- `docs/policies/result_judgment_policy.md`

효과(effect, 효과)는 skill routing(스킬 배치)이 architecture(구조), exploration(탐색), KPI(핵심 성과 지표), run management(실행 관리), result judgment(결과 판정) 규칙과 끊기지 않게 하는 것이다.

## 운영 커널

모든 non-trivial work packet(비사소 작업 묶음)은 다음 순서를 따른다.

1. 현재 진실(current truth)과 브랜치/작업트리 적합성을 확인한다.
2. `docs/agent_control/work_family_registry.yaml`에서 `primary_family`를 하나 고른다.
3. 그 family의 `primary_skill`을 하나만 고른다.
4. 필요한 경우에만 `support_skills`를 붙인다.
5. `required_gates`를 work packet과 closeout에 연결한다.
6. 완료/검증/검토 주장은 `required_gate_coverage_audit`와 claim guard가 통과한 뒤에만 쓴다.

이 규칙의 효과는 스킬을 줄이는 것이 아니라, 필요한 스킬이 조언 문서로 흐르지 않고 실행 계약으로 작동하게 만드는 것이다.

## 작은 작업 경계(Small-Work Boundary, 작은 작업 경계)

`trivial or information_only packet(사소 또는 정보 전용 작업 묶음)`은 파일 수정(file mutation, 파일 수정), 실행(run, 실행), publish/push(게시/원격 반영), stage closeout(단계 마감), MT5/runtime/model work(MT5/런타임/모델 작업), 상태 동기화(state sync, 상태 동기화), 또는 `completed/reviewed/verified(완료/검토/검증)` claim(주장)을 만들지 않는 좁은 상태 확인, 경로/해시/등록부 재확인, 읽기 전용 검토다.

작은 작업의 기본 라우팅(default routing, 기본 라우팅):

- `reentry_mode(재진입 모드)`: warm thread(따뜻한 스레드)에서는 delta check(변화분 점검)
- `support_skills(보조 스킬)`: 기본 0개, 사용자 보고나 주장 경계가 필요하면 최대 1개
- `skills_to_read(읽을 스킬)`: primary skill(주 스킬) 먼저, support skill(보조 스킬)은 한 줄 사유가 있을 때만
- `receipt(영수증)`: compact receipt(압축 영수증)
- `required_gates(필수 게이트)`: 실행하지 않는 gate(게이트)는 `not_applicable_with_reason(사유 있는 해당 없음)`로 남긴다.

작은 작업이 파일 수정, 정책/스킬 변경, MT5 실행, 모델 산출물, stage closeout(단계 마감), publish/push(게시/원격 반영), 또는 강한 완료/검증 주장을 만들면 즉시 non-trivial work packet(비사소 작업 묶음)으로 승격한다. 효과(effect, 효과)는 작은 질문에 전체 gate stack(게이트 묶음)이 붙는 것을 막되, 중요한 작업의 증거 요구는 유지하는 것이다.

## 운영-근거 균형(Governance/Evidence Balance, 운영-근거 균형)

Governance stays lightweight(운영은 가볍게 유지)한다. Codex(코덱스)는 claim(주장)을 보호하는 가장 작은 router/profile/skill set(라우터/프로필/스킬 묶음)을 고르고, 이 원칙만으로 새 gate/overlay/family/skill/agent call/review pass(게이트/오버레이/작업군/스킬/요원 호출/검토 회차)를 만들지 않는다.

Evidence stays heavyweight(근거는 무겁게 유지)한다. protected claim(보호 주장)을 narrow sufficient run(좁고 충분한 실행)으로 시험할 수 있으면 procedural expansion(절차 확장), advisory loop(자문 반복), deferred checkpoint(지연 점검)를 늘리기보다 active verification(능동 검증)을 먼저 시도한다. 효과(effect, 효과)는 시스템 운영 문서는 작게 두고, 토큰/시간을 실제 파일, 실행, 해시, MT5 output(MT5 출력), Task Force actual call(태스크포스 실제 호출)에 쓰게 하는 것이다.

## `/goal` 검증 프로필 라우팅(`/goal` Verification Profile Routing, `/goal` 검증 프로필 라우팅)

Active `/goal(활성 목표)`은 그 자체로 heavy verification trigger(무거운 검증 트리거)가 아니다. `/goal(목표)`가 파일 수정(file mutation, 파일 수정), 실행(run, 실행), stage open/closeout(단계 개방/마감), policy/skill change(정책/스킬 변경), runtime/model work(런타임/모델 작업), publish/push(게시/원격 반영), state sync(상태 동기화), 또는 `completed/reviewed/verified(완료/검토/검증)` claim(주장)을 만들 때만 non-trivial packet(비사소 묶음)으로 승격한다.

non-trivial `/goal` packet(비사소 목표 묶음)은 `docs/agent_control/work_family_registry.yaml`의 `verification_profiles(검증 프로필)`에서 profile id(프로필 ID) 하나를 먼저 고른다. profile(프로필)은 `claim_surface(주장 표면)`가 결정하며, 검증 행동(verification action, 검증 행동)은 다음 네 가지를 모두 기록해야 한다.

- `trigger_source(트리거 원천)`: registry gate/overlay gate/acceptance criterion/risk hard-stop/claim surface/explicit user scope(등록부 게이트/오버레이 게이트/수용 기준/위험 중단/주장 표면/명시 사용자 범위)
- `protected_claim(보호 주장)`: 그 검증이 보호하는 claim(주장)
- `required_evidence(필수 근거)`: 필요한 파일, 실행, receipt(영수증), report(보고서), hash(해시), MT5 output(MT5 출력)
- `stop_condition(중단 조건)`: 충분하면 멈출 조건과 실패 시 claim boundary(주장 경계)

효과(effect, 효과)는 `/goal(목표)`가 안정적으로 운영되면서도 “혹시 모르니 다 검증”으로 흐르지 않게 하는 것이다. trigger_source(트리거 원천)가 없는 검증은 실행하지 않는다.

Gate selection(게이트 선택)은 `family base gates(작업군 기본 게이트) + active overlay gates(활성 오버레이 게이트) + profile extra gates(프로필 추가 게이트)`를 합친 뒤 dedupe(중복 제거)한다. profile(프로필)은 필요한 gate(게이트)를 빼거나 완화하지 못한다. 실행하지 않는 gate(게이트)는 `gate/reason_code/reason/claim_effect(게이트/사유 코드/사유/주장 효과)`가 있는 `not_applicable_with_reason(사유 있는 해당 없음)`로만 남긴다.

Runtime/MT5(런타임/MT5) 검증은 runtime claim(런타임 주장), Strategy Tester output(전략 테스터 출력), EA/ONNX handoff(EA/ONNX 인계), `.mq5/.mqh/.set` behavior(`.mq5/.mqh/.set` 동작), 또는 operating promotion/runtime authority/live readiness(운영 승격/런타임 권위/실거래 준비)를 다룰 때만 켠다. Design/proxy/Python-only(설계/프록시/파이썬 전용) packet(묶음)은 MT5 Strategy Tester(전략 테스터)를 자동 요구하지 않는다.

Runtime/materialization/handoff/economics claim(런타임/물질화/인계/경제성 주장)이 있으면 `runtime_probe(런타임 탐침)`를 cost/expense(비용)를 이유로 다음 작업(next work, 다음 작업)으로 미루지 않는다. 같은 packet(묶음)에서 가장 좁은 충분한 `runtime_probe(런타임 탐침)`를 시도하거나, 복구 시도(recovery attempt, 복구 시도) 뒤 `blocked/inconclusive/out_of_scope_by_claim(차단/불충분/주장 범위 밖)`으로 낮춘다. Probe(탐침)가 없으면 `runtime verified/economics pass/materialization-ready/handoff complete(런타임 검증됨/경제성 통과/물질화 준비/인계 완료)`를 주장하지 않는다.

## Codex Task Force 트리거(Codex Task Force Trigger, 코덱스 태스크포스 트리거)

`obsidian-task-force-review(태스크포스 검토)`는 project-native Codex Task Force(프로젝트 전용 코덱스 태스크포스)를 호출하는 active trigger overlay(활성 트리거 오버레이, 추가 조건)다. 요원 명단(roster, 명단)의 진실 원천은 `docs/agent_control/codex_task_force_registry.yaml`이고, 실제 custom agent(사용자 정의 요원) 파일은 `.codex/agents/<roster_id>.toml`에 둔다. 효과(effect, 효과)는 새 대화창이나 cold start(냉시작)에서도 같은 8명 요원(agent, 요원)을 같은 이름과 임무로 불러오는 것이다.

기본 호출 방식(default call mode, 기본 호출 방식)은 `micro_consult(소형 상담)`다. agent/skill consulting(요원/스킬 상담), 라우팅 의문, 좁은 정책 해석, 증거 연결 질문은 먼저 1명만 부르고, 두 영역이 겹칠 때만 2명을 부른다. 이 receipt(영수증)는 `micro_consult_receipt(소형 상담 영수증)`와 필요 시 `micro_consult_index(소형 상담 색인)`에 남기며, claim effect(주장 효과)는 `advisory_only_no_reviewed_pass(자문 전용, 검토/통과 아님)`다.

3명 이상 호출은 `escalation_reason(확대 사유)`가 있어야 한다. 5명 이상 호출은 `why_not_smaller(왜 더 작게 못 했는지)`가 있어야 한다. 8명 전원 호출은 `escalation_reason(확대 사유)`, `why_not_smaller(왜 더 작게 못 했는지)`, `full_roster_call_reason(전원 호출 사유)`를 모두 남긴다. 효과(effect, 효과)는 과거처럼 중간중간 큰 묶음 호출로 흐르지 않고, 적재적소에 작은 상담부터 쓰게 하는 것이다.

formal Task Force review(공식 태스크포스 검토)는 stage closeout(단계 마감), policy change(정책 변경), runtime authority(런타임 권위), operating promotion(운영 승격), cross-system handoff(교차 시스템 인계), 또는 protected reviewed/verified/pass claim(보호된 검토/검증/통과 주장)에만 쓴다. 이때만 현재 primary_family(주 작업군)에 Codex Task Force receipt(코덱스 태스크포스 영수증)와 `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` gate(게이트)를 덧붙인다.

Task Force review(태스크포스 검토)가 필요하면 Codex(코덱스)는 registry(등록부) 기준으로 필요한 agent(요원)만 고르고, Task Force reviewed/reviewed/verified/pass(태스크포스 검토됨/검토됨/검증됨/통과)를 주장하기 전에 선택한 custom agent(사용자 정의 요원)를 즉시 실제 `spawn_agent(서브에이전트 생성 호출)`로 호출한다. optional `micro_consult(선택 소형 상담)`에서 현 세션 도구 metadata(메타데이터)가 아직 갱신되지 않아 이름 지정 custom agent(사용자 정의 요원)를 부를 수 없으면 compatibility fallback(호환 대체)로 명단 ID를 prompt(프롬프트)에 넣을 수 있지만, claim effect(주장 효과)는 자문 전용으로 낮춘다.

formal Task Force review(공식 태스크포스 검토)가 active goal(`/goal`, 활성 목표), work packet(작업 묶음), required gate(필수 게이트), family rule(작업군 규칙), router-selected required Task Force overlay(라우터가 선택한 필수 태스크포스 오버레이), explicit user instruction requiring review(검토를 요구하는 명시 사용자 지시), 또는 closeout claim(마감 주장)에 필요하면 `spawn_agent(서브에이전트 생성 호출)` 도구 없음이나 미호출은 `blocked_for_task_force_review(태스크포스 검토 차단)`다. `not_applicable_with_reason(사유 있는 해당 없음)`나 claim boundary lowering(주장 경계 낮춤)으로 통과시킬 수 없고, `reviewed/verified/pass/stage closeout pass/internally_reviewed/rehearsed_control_plane(검토됨/검증됨/통과/단계 마감 통과/내부 검토됨/제어면 리허설됨)`을 주장하지 않는다. dormant/stale agent(대기 중이거나 낡은 맥락의 요원)는 최신 context update(맥락 갱신) 없이 검토 근거로 쓰지 않는다.

효과(effect, 효과)는 internal adversarial review(내부 비판 검토)를 하되, Grok(그록) 외부 권위를 흉내내지 않고 self-review(자기검토)나 `micro_consult(소형 상담)`를 Task Force review(태스크포스 검토)로 포장하지 않는 것이다.

## Grok 보관 규칙(Grok Archive Rule, 그록 보관 규칙)

`obsidian-grok-collaboration(그록 협업)`은 retired/archive-only skill(퇴역/보관 전용 스킬)이다. 새 work family(작업군), trigger overlay(트리거 오버레이), required skill(필수 스킬), required gate(필수 게이트), external review packet(외부 검토 묶음)을 만들지 않는다.

사용자가 Grok call/review(그록 호출/검토)를 말해도 Grok(그록)을 호출하지 않고, 그 문구만으로 Task Force review(태스크포스 검토)도 켜지 않는다. external review(외부 리뷰), second opinion(2차 의견), no solo Codex judgment(코덱스 단독 판단 금지), stage-close adversarial review(단계 마감 비판 검토), agent/skill consulting(요원/스킬 상담)은 그 자체가 active review request(활성 검토 요청)이면 `obsidian-task-force-review(태스크포스 검토)`로 라우팅한다.

기존 `docs/agent_control/grok_reviews/`는 historical evidence(역사 근거)다. 읽을 수는 있지만, 새 prompt(프롬프트), wrapper call(래퍼 호출), Grok output(그록 출력), Grok receipt(그록 영수증), Grok gate(그록 게이트)를 만들지 않는다.

효과(effect, 효과)는 이전 Grok(그록) 운영 흔적을 보존하면서도 새 운영체계가 외부 2차 의견 경로로 역류하지 않게 하는 것이다.

## 5단계 중간 검토 트리거(Five-Stage Retrospective Trigger, 5단계 중간 검토 트리거)

`five_stage_retrospective(5단계 중간 검토)`는 retired archive rule(퇴역 보관 규칙)로만 보존한다. active trigger(활성 작동 조건), Grok call(그록 호출), next stage open block(다음 단계 개방 차단)을 만들지 않는다.

효과(effect, 효과)는 기존 register(등록부)와 report(보고서)를 보존하면서도, 새 운영체계가 Grok(그록) 회고 의무로 역류하지 않게 하는 것이다.

Archived due check(보관 도래 점검)는 과거 Grok retrospective(그록 회고) 방식의 설명으로만 보존한다. 아래 조건은 이제 Grok call(그록 호출), required gate(필수 게이트), next-open block(다음 개방 차단)을 만들지 않는다.

- closing frontier number(마감 전선 번호)가 5의 배수면 due(도래)다.
- 그렇지 않아도 `docs/registers/five_stage_retrospective_register.yaml`의 `closed_frontier_ids_since_last_retrospective`가 5개면 due(도래)다.
- due(도래)가 아니면 `not_due(아직 아님)`로 기록하고 다음 stage open(단계 개방)을 허용한다.
- due(도래)이면 역사 규칙상 최근 5개 canonical closeout stage ids(정식 마감 단계 ID)를 scope(범위)로 묶었다. 새 운영에서는 Codex Task Force replacement retrospective(코덱스 태스크포스 대체 회고)가 생길 때까지 `inactive_preserve_records(비활성, 기록 보존)`로 남긴다.

이 검토는 per-stage Grok receipt(단계별 그록 영수증)를 다시 읽는 repetition(반복)이 아니다. Cross-stage synthesis(단계 간 종합)만 허용하며, allowed claims(허용 주장)는 direction_delta(방향 변화)와 repair_priority_delta(수리 우선순위 변화)뿐이다.

Due check archive(도래 점검 보관)는 register-first(등록부 우선)다. 효과(effect, 효과)는 기존 5단계 기록을 보존하면서도 F80(전선80) 운영이 Grok packet(그록 묶음) 독해 루프로 역류하지 않게 하는 것이다.

## 전선 추가 단계 트리거(Frontier Extra Stage Trigger, 전선 추가 단계 트리거)

`frontier_extra_stage_due_check(전선 추가 단계 도래 점검)`는 active trigger overlay(활성 트리거 오버레이, 추가 조건)다. 새 frontier stage(전선 단계)를 열기 전, 또는 broad goal(넓은 목표)에서 frontier campaign(전선 캠페인)을 계속 진행할 때 먼저 실행한다.

Trigger(트리거)는 closed canonical frontier count(마감된 정식 전선 수)가 50개 단위에 도달했는지다. F50/F100/F150...(전선50/100/150...) closeout(마감)이 있고 대응 E01/E02/E03...(추가01/02/03...) closeout record(마감 기록)가 없으면 extra stage(추가 단계)를 먼저 연다.

도래하면 다음 순서를 따른다.

1. `docs/registers/frontier_extra_stage_register.yaml`를 읽어 already_closed/already_open/not_due/due_backfill(이미 마감/이미 개방/아직 아님/소급 도래)을 판정한다.
2. due(도래)이면 `stages/stage_frontier_extra_EXX__...` 아래 기존 stage structure(단계 구조)로 open packet(개방 묶음)을 만든다.
3. 해당 50개 frontier stage(전선 단계)의 closeout receipt/MT5 evidence/negative memory/preserved clue(마감 영수증/MT5 근거/부정 기억/보존 단서)를 receipt-first scan(영수증 우선 스캔)한다.
4. E02/E03...(추가02/03...)부터는 ingredient card(재료 카드), progressive depth-sampled mix queue(점증 깊이 표본 혼합 대기열), WFO-aware mix(워크포워드 인식 혼합), MT5 runtime campaign(MT5 런타임 캠페인)을 생성하고 실행한다. 기본 depth(깊이)는 2-mix -> 3-mix -> 4-mix(2개 혼합 -> 3개 혼합 -> 4개 혼합)이며, 다음 depth(깊이)는 diversity/risk/reproducibility/materialization(다양성/위험/재현성/물질화) gate(게이트)가 통과할 때만 연다.
5. closeout(마감), state sync(상태 동기화), frontier_extra_mix_depth_lint(전선 추가 혼합 깊이 점검), required gate coverage audit(필수 게이트 커버리지 감사), final claim guard(최종 주장 보호)를 남긴 뒤 resume frontier(재개 전선)를 연다.

효과(effect, 효과)는 사용자가 stage 50/100(단계50/100)을 직접 말하지 않아도 Codex(코덱스)가 “extra due(추가 도래) 먼저”를 자동으로 확인하는 것이다. 이 trigger(트리거)는 Grok(그록)을 호출하지 않고, completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.

Progressive mix depth(점증 혼합 깊이)의 기본 cap(상한)은 2-mix queue 60/materialized 6/MT5 attempts 12(2개 혼합 대기열 60/물질화 6/MT5 시도 12), 3-mix queue 36/materialized 4/MT5 attempts 8(3개 혼합 대기열 36/물질화 4/MT5 시도 8), 4-mix queue 12/materialized 2/MT5 attempts 4(4개 혼합 대기열 12/물질화 2/MT5 시도 4)다. `top_forward_pf(상위 전진 수익 팩터)`는 전체 MT5 후보의 25%를 넘지 못하고, selection lane(선정 선로)은 PF/DD resilience/density-materiality/runtime materialization/negative-memory repair(수익 팩터/손실폭 회복력/밀도-물질성/런타임 물질화/부정 기억 수리)로 나눈다.

Extra stage receipt(추가 단계 영수증)는 ingredient card receipts(재료 카드 영수증), mix queue receipts(혼합 대기열 영수증), depth receipts(깊이 영수증), materialized attempt receipts(물질화 시도 영수증)를 함께 남긴다. Ingredient card(재료 카드)는 source frontier/run(원천 전선/실행), hypothesis(가설), axis tags(축 태그), artifact path/hash(산출물 경로/해시), salvage value/negative memory/do-not-repeat(회수 가치/부정 기억/반복 금지), tier scope(티어 범위), claim boundary(주장 경계), selection eligibility/lane candidates(선정 자격/선정 선로 후보)를 가진다. Mix queue(혼합 대기열)는 depth/source card ids/axis tags/selection lanes/novelty delta/near-duplicate cluster/sample method/selected-for-runtime/selection reason/risk notes/claim boundary(깊이/원천 카드 ID/축 태그/선정 선로/신규성 차이/근접 중복 군집/표본 방식/런타임 선택 여부/선정 사유/위험 기록/주장 경계)를 가진다.

Depth receipt(깊이 영수증)는 depth_id/candidate_cap/sample_method/selection_lane_counts/top_forward_pf_share/runtime_substrate_count/single_substrate_warning/materialized_count/runtime_completed_count/full_mix_materialized=false/depth_decision/claim_effect/claim_boundary(깊이 ID/후보 상한/표본 방식/선정 선로별 수/상위 전진 수익 팩터 비율/런타임 바탕 수/단일 바탕 경고/물질화 수/런타임 완료 수/전체 혼합 물질화 아님/깊이 결정/주장 효과/주장 경계)를 depth(깊이)별로 남긴다. Materialized attempt(물질화 시도)는 dataset/feature/label/split identity(데이터셋/피처/라벨/분할 정체성), parser/runtime contract version(파서/런타임 계약 버전), ONNX/EA/set/feature/tester/report/trade-list/telemetry hash(온엑스/EA/설정/피처/테스터/보고서/거래목록/텔레메트리 해시)를 남긴다. closeout(마감) 전에는 `frontier_extra_mix_depth_lint(전선 추가 혼합 깊이 점검)`로 이 receipt(영수증)를 검사한다. 효과(effect, 효과)는 `/goal(목표)`에서 “개쩌는 ONNX(온엑스)”처럼 넓은 요청이 들어와도 card/combination selection(카드/조합 선정) 생략, exhaustive search(전체 탐색), PF-only selection(PF 단독 선정), compile-only/proxy-only runtime claim(컴파일 단독/프록시 단독 런타임 주장), full mix materialization(전체 혼합 물질화)을 몰래 주장하지 못하게 하는 것이다.

## 전선 5단계 방향 종합 트리거(Five-Stage Direction Synthesis Trigger, 5단계 방향 종합 트리거)

`frontier_five_stage_direction_synthesis(전선 5단계 방향 종합)`는 Topic Rotation Guard(주제 회전 보호)와 Extra Stage(추가 단계) 사이의 light synthesis(가벼운 종합)다. 실행 순서(effect, 효과)는 `frontier_extra_stage_due_check(전선 추가 단계 도래 점검)` 뒤, canonical frontier open(정식 전선 개방)의 `frontier_topic_rotation_check(전선 주제 회전 점검)` 전에 최근 5개 방향을 짧게 정리하는 것이다.

이 trigger(트리거)는 retrospective(회고), Grok call(그록 호출), heavy Task Force review(무거운 태스크포스 검토), runtime authority(런타임 권위)를 만들지 않는다. Required record(필수 기록)는 covered_frontier_ids/dominant_direction/repeated_mechanism/overused_axis_warning/next_axis_options/allowed_reexperiment_conditions/adjacent_same_axis_block/claim_boundary(검토 전선 ID/지배 방향/반복 메커니즘/과사용 축 경고/다음 축 후보/재실험 허용 조건/인접 동일 축 차단/주장 경계)다.

중요한 경계(boundary, 경계)는 topic ban(주제 금지)이 아니다. 같은 topic(주제)은 나중에 new axis or new evidence(새 축 또는 새 근거)가 있으면 다시 실험할 수 있다. 이 trigger(트리거)가 막는 것은 adjacent same-axis continuation(인접 동일 축 연속), renamed repair(이름만 바꾼 수리), 그리고 최근 5개 흐름과 같은 question class(질문 계열)를 계속 미는 것이다.

Allowed claims(허용 주장)는 direction_delta/axis_rotation_hint/adjacent_repeat_warning(방향 변화/축 회전 힌트/인접 반복 경고)뿐이다. completion/selected baseline/operating promotion/runtime authority/live readiness/Goal Achieve(완성/선택 기준선/운영 승격/런타임 권위/실거래 준비/목표 달성)는 금지한다.

## 전선 주제 회전 트리거(Frontier Topic Rotation Trigger, 전선 주제 회전 트리거)

`frontier_topic_rotation_check(전선 주제 회전 점검)`는 active trigger overlay(활성 트리거 오버레이, 추가 조건)다. canonical frontier stage(정식 전선 단계)를 새로 열기 전 실행한다. 50개 boundary(경계)에서는 `frontier_extra_stage_due_check(전선 추가 단계 도래 점검)`를 먼저 처리하고, `frontier_five_stage_direction_synthesis(전선 5단계 방향 종합)`로 최근 5개 방향을 가볍게 정리한 뒤, resume frontier open(전선 재개 개방)에 이 점검을 적용한다.

Trigger(트리거)는 다음 중 하나다.

1. frontier closeout(전선 마감) 뒤 다음 canonical frontier stage(정식 전선 단계)를 열려 한다.
2. 최근 5개 closed canonical frontier stages(마감된 정식 전선 단계)를 넘는 새 block(블록)을 시작한다.
3. 직전 stage(단계)와 같은 broad topic(넓은 주제) 또는 같은 artifact surface(산출물 표면)를 다시 열려 한다.

점검 순서는 다음과 같다.

1. 직전 frontier closeout(전선 마감)과 최근 5개 closeout(마감)을 receipt-first(영수증 우선)로 읽는다.
2. closing/current stage(마감 또는 현재 단계)의 repair disposition(수리 처분)이 같은 stage(단계) 안에서 닫혔는지 확인한다.
3. 새 stage question(단계 질문)이 continuation repair/near-duplicate hypothesis/threshold-filter-session-routing-parameter-only tweak/renamed repair(연속 수리/근접 중복 가설/임계값-필터-세션-라우팅-파라미터만 미세조정/이름만 바꾼 수리)가 아닌지 기록한다.
4. 같은 broad topic(넓은 주제)이면 source/data representation/label/runtime representation/validation philosophy/model family/objective/trade shape/risk logic/regime split(원천/데이터 표현/라벨/런타임 표현/검증 철학/모델 계열/목적함수/거래 형태/위험 로직/장세 분할) 중 material novelty delta(실질 신규성 차이)를 적는다.
5. 실패하면 새 frontier open(전선 개방)을 만들지 않고 같은 stage repair packet(동일 단계 수리 묶음)으로 남기거나, materially distinct question(실질적으로 다른 질문)으로 다시 제안한다.

효과(effect, 효과)는 같은 주제(topic, 주제)를 영구 금지하지 않으면서도, 인접한 frontier stage(전선 단계)가 같은 수리나 비슷한 가설을 계속 밀고 나가는 것을 막는 것이다. 실패한 check(점검)는 현재 proposed next-open shape(제안된 다음 개방 형태)만 막고, broad topic(넓은 주제)의 future reuse(미래 재사용)를 막지 않는다. 이 trigger(트리거)는 retrospective(회고), Grok call(그록 호출), external review(외부 검토), completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.

## 라우팅 소스

라우팅의 진실 원천(source of truth)은 `docs/agent_control/work_family_registry.yaml`이다.

각 family는 반드시 다음을 가진다.

- `primary_skill`: 작업을 대표하는 스킬 1개
- `support_skills`: primary를 보조하는 제한된 스킬 목록
- `required_skills`: receipt가 필요한 전체 스킬 목록
- `required_gates`: closeout 전에 실행되거나 명시적으로 N/A 처리되어야 하는 gate 목록

`primary_skill`은 항상 `required_skills`의 첫 번째 항목이어야 한다.

## Work Family 선택

작업군은 stage 번호가 아니라 작업 성격으로 고른다.

| work family | primary_skill | 쓰는 때 |
| --- | --- | --- |
| `information_only` | `obsidian-answer-clarity` | 읽기, 설명, 상태 요약 |
| `state_sync` | `obsidian-stage-transition` | 현재 진실, active stage, current run, 브랜치/상태 동기화 |
| `policy_skill_governance` | `obsidian-work-packet-router` | `AGENTS.md`, policy, skill, control-plane 계약 변경 |
| `code_edit` | `obsidian-code-surface-guard` | 일반 코드 수정 |
| `code_refactor` | `obsidian-code-surface-guard` | 모듈 분리, 비대증 방지, owner module 이동 |
| `experiment_design` | `obsidian-experiment-design` | 실험 가설, baseline, 변수, 무효 조건 설계 |
| `experiment_execution` | `obsidian-run-evidence-system` | Python/model/variant 실행과 결과 근거 기록 |
| `runtime_backtest` | `obsidian-runtime-parity` | MT5, EA, `.mq5`, `.mqh`, `.set`, Strategy Tester, runtime handoff |
| `kpi_evidence` | `obsidian-run-evidence-system` | KPI, ledger, row grain, source authority, 결과 판정 |
| `artifact_lineage` | `obsidian-artifact-lineage` | artifact, hash, manifest, report 연결 |
| `cleanup_archive` | `obsidian-artifact-lineage` | 정리, 보관, 삭제, 이동 |
| `publish_handoff` | `obsidian-stage-transition` | PR, branch, handoff, stage closeout |

한 요청이 여러 성격을 가져도 `primary_family`는 하나만 고른다. 나머지는 support 또는 phase로 기록한다.

## Support Skill 규칙

Support skill은 작업을 보조한다. 작업을 다시 분류하지 않는다.

- 기본 support 한도는 `work_family_registry.yaml`의 `support_skill_limit_default`를 따른다.
- `trivial or information_only packet(사소 또는 정보 전용 작업 묶음)`은 support skill(보조 스킬) 기본값이 0개이며, 붙이면 `skills_to_read(읽을 스킬)`와 한 줄 justification(사유)을 남긴다.
- runtime이나 experiment처럼 진짜 복합 작업일 때만 family별 `support_skill_limit`을 쓴다.
- support로 선택한 스킬도 `required_skills`에 들어가야 하며, 완료 전에 receipt가 있어야 한다.
- 순수 내부 리팩터처럼 외부 API나 MT5 동작이 바뀌지 않는 경우 `obsidian-reference-scout`는 `not_required` 사유를 남길 수 있다.

## 스킬

- `obsidian-answer-clarity`: user-facing status(사용자 보고 상태), result report(결과 보고), completion report(완료 보고)를 쉽게 설명한다.
- `obsidian-architecture-guard`: architecture debt(구조 부채), code placement(코드 배치), Korean encoding(한국어 인코딩)을 지킨다.
- `obsidian-artifact-lineage`: artifact(산출물), manifest(목록), report(보고서), hash(해시), registry(등록부) 연결을 확인한다.
- `obsidian-backtest-forensics`: MT5 Strategy Tester(전략 테스터) report/settings/trade list(보고서/설정/거래 목록)를 검사한다.
- `obsidian-claim-discipline`: claim boundary(주장 경계)를 낮출 곳은 낮추고 promotion/runtime(승격/런타임) 과장을 막는다.
- `obsidian-code-quality`: 코드 책임(code responsibility, 코드 책임), 흐름(flow, 흐름), 테스트 의도(test intent, 테스트 의도)를 확인한다.
- `obsidian-code-surface-guard`: owner module(소유 모듈), caller(호출자), input/output contract(입출력 계약), monolith risk(일체형 위험)를 점검한다.
- `obsidian-data-integrity`: data source(데이터 원천), time axis(시간축), split(분할), leakage(누수)를 점검한다.
- `obsidian-environment-reproducibility`: dependency/runtime(의존성/런타임), clean checkout(깨끗한 체크아웃), local machine assumption(로컬 가정)을 확인한다.
- `obsidian-experiment-design`: hypothesis(가설), baseline(기준선), variables(변수), invalid conditions(무효 조건)을 설계한다.
- `obsidian-exploration-mandate`: exploration lane(탐색 레인), idea boundary(아이디어 경계), failure memory(실패 기억)를 지킨다.
- `obsidian-lane-classifier`: exploration/runtime/promotion lane(탐색/런타임/승격 레인)을 구분한다.
- `obsidian-model-validation`: model/threshold surface(모델/임계값 표면), split(분할), overfit(과적합), selection metric(선택 지표)을 점검한다.
- `obsidian-performance-attribution`: KPI change(KPI 변화)를 time/sample/tier/model/trade shape(시간/표본/티어/모델/거래 형태)로 분해한다.
- `obsidian-reentry-read`: current truth(현재 진실)와 active stage(활성 단계)를 재진입 순서대로 확인한다.
- `obsidian-reference-scout`: version-sensitive external reference(버전 민감 외부 참고자료)가 필요한지 확인한다.
- `obsidian-result-judgment`: positive/negative/inconclusive/invalid(긍정/부정/불충분/무효) 판정을 경계와 함께 정리한다.
- `obsidian-run-evidence-system`: run identity(실행 정체성), KPI(핵심 성과 지표), ledger row(장부 행), missing evidence(빠진 근거)를 관리한다.
- `obsidian-runtime-parity`: Python/MT5/runtime handoff(파이썬/MT5/런타임 인계) 동등성과 외부 검증을 다룬다.
- `obsidian-session-intake`: 작업 시작 때 current truth(현재 진실), branch/worktree fit(브랜치/작업트리 적합성), work family candidate(작업군 후보)를 좁힌다.
- `obsidian-stage-transition`: active stage(활성 단계), handoff(인계), closeout(마감), current run(현재 실행)을 같은 회차에 동기화한다.
- `obsidian-task-force-review`: Codex Task Force(코덱스 태스크포스) roster(명단), model policy(모델 정책), internal adversarial review(내부 비판 검토), explicit active review request(명시적 활성 검토 요청), Frontier80 rehearsal(F80 리허설)를 관리한다.
- `obsidian-work-packet-router`: work family(작업군), primary skill(주 스킬), support skills(보조 스킬), required gates(필수 제한문)를 고른다.
- `obsidian-workflow-drift-guard`: blocker(차단 지점), missing material(빠진 재료), recovery action(복구 행동)을 정리한다.
- `obsidian-grok-collaboration`: retired/archive-only(퇴역/보관 전용) 스킬이다. 기존 Grok record(그록 기록)를 읽을 때만 쓰고, 새 호출/검토/게이트는 만들지 않는다.

## Receipt 규칙

스킬을 선택했다는 말은 receipt가 있다는 뜻이다.

`docs/agent_control/skill_receipt_schema.yaml`는 각 스킬별 필수 receipt 필드를 정한다.

완료 보고 전에는 다음이 맞아야 한다.

- work packet의 `skill_routing.primary_family`
- work packet의 `skill_routing.primary_skill`
- work packet의 `skill_routing.support_skills`
- work packet의 `skill_routing.required_skill_receipts`
- closeout의 실행 audit 목록
- `required_gate_coverage_audit` 결과

이 중 하나가 비면 `completed`, `reviewed`, `verified`, `runtime_authority`, `operating_promotion` 같은 주장은 금지한다.

## Skill Layer

스킬은 네 층으로 본다.

- Intake/router: `obsidian-session-intake`, `obsidian-work-packet-router`
- Domain skills: code, experiment, model, runtime, KPI, artifact, state sync
- Guard skills: claim discipline, workflow drift, environment reproducibility, reference scout
- Final report filter: `obsidian-answer-clarity`, `obsidian-claim-discipline`

모든 스킬을 매번 읽는 것이 목표가 아니다. 현재 family가 요구하는 스킬을 정확히 읽고, receipt로 증명하는 것이 목표다.

## Same-Pass Sync

단계 의미(stage meaning), active stage, current run, branch, artifact identity, run status가 바뀌면 같은 작업 회차(pass)에 관련 문서를 맞춘다.

주요 current truth 문서는 다음이다.

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- 활성 단계 `04_selected/selection_status.md`
- `docs/registers/run_registry.csv`
- 단계별 `03_reviews/stage_run_ledger.csv`

`workspace_state.active_branch`와 실제 git branch가 다르면 state sync는 완료될 수 없다.

## Hard Gate Rule

강한 게이트(hard gate)는 운영 의미에만 적용한다.

탐색(exploration)은 할 수 있다. 하지만 다음 주장은 gate 없이 닫지 않는다.

- 검증 완료
- 리뷰 완료
- 런타임 권위
- 운영 승격
- MT5 검증 완료
- full verification

탐색 아이디어가 promotion-ineligible이어도 아이디어가 죽었다는 뜻은 아니다.

## Policy Skill Settings

`AGENTS.md`, policy, skill, control-plane 파일을 바꾸는 작업은 `policy_skill_governance` family다.

필수 gate는 다음이다.

- `agent_control_contracts`
- `ops_instruction_audit`
- `work_packet_schema_lint`
- `skill_receipt_schema_lint`

이 효과는 스킬/정책을 더 추가하기 전에 운영 라우터 자체가 안정적인지 먼저 막는 것이다.
