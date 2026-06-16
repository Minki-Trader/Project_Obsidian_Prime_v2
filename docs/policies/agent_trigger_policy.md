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

## Grok 협업 트리거(Grok Collaboration Trigger, 그록 협업 트리거)

`obsidian-grok-collaboration(그록 협업)`은 새 work family(작업군)가 아니라 trigger overlay(트리거 오버레이, 추가 조건)다. 사용자가 명시했거나 `/goal(목표)`에 들어 있을 때 현재 primary_family(주 작업군)에 Grok receipt(그록 영수증)와 external_review_packet(외부 검토 묶음) gate(게이트)를 덧붙인다.

필수 트리거(required triggers, 필수 트리거):

- Grok 호출(Grok call, 그록 호출)을 현재 요청에서 명시함
- `/goal(목표)`에 Grok 검토(Grok review, 그록 검토) 조건이 있음
- `Stage 종료 후마다 Grok 검토`
- `closeout 전에 외부 리뷰`
- `Grok에게 연구방향 점검받기`
- `Codex 혼자 판단하지 말고 Grok 2차 의견`
- `stage close(단계 마감)마다 비판 검토`
- agent/skill consulting(에이전트/스킬 상담)
- 방향성 제시(direction proposal, 방향성 제시) 뒤 Grok 2차 토론(second discussion, 2차 토론)을 요구함
- five-stage retrospective(5단계 중간 검토)가 due(도래)함

필수 순서(required order, 필수 순서)는 Codex(코덱스)가 먼저 current truth(현재 진실), direction(방향성), success criteria(성공 기준), claim boundary(주장 경계), review size(검토 크기)를 제시하고, bounded evidence(제한 근거)를 만든 뒤 Grok을 호출하고, Grok 조언을 accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)로 분리한 다음 진행하는 것이다.

기본 기록 위치(default record location, 기본 기록 위치)는 `docs/agent_control/grok_reviews/` 아래 snapshot/prompt/output/metadata(스냅샷/프롬프트/출력/메타데이터)다. 사용자가 프로젝트 폴더에 patch work material(패치 작업물)을 남기지 말라고 명시하면 새 review packet(검토 묶음)을 만들지 않고, 기존 산출물(existing artifacts, 기존 산출물)이나 프로젝트 밖 임시 경로(temp path, 임시 경로)를 쓴 뒤 final report(최종 보고)에 그 제한을 적는다.

검토 크기(review size, 검토 크기)는 다음 기본값을 따른다.

- small review(소규모 검토): 좁은 질문 하나와 compact prompt(압축 프롬프트) 하나.
- medium review(중간 검토): bounded snapshot(제한 스냅샷) 하나와 focused question(집중 질문) 하나.
- large review(대규모 검토): architecture/evidence/runtime/policy(구조/근거/런타임/정책)처럼 여러 narrow pass(좁은 회차)로 나누고, 마지막 판단은 Codex synthesis(Codex 종합)로만 닫는다.

small review(소규모 검토) receipt(영수증)는 compact receipt(압축 영수증)를 쓴다. Minimum fields(최소 필드)는 `trigger_reason(트리거 이유)`, `bounded_evidence(제한 근거)`, `advice_classification(조언 분류)`, `claim_boundary(주장 경계)`, `final_codex_direction(최종 Codex 방향)`이다. Medium/large review(중간/대규모 검토)만 full receipt(전체 영수증), full prompt/output identity(전체 프롬프트/출력 정체성), detailed local verification block(상세 로컬 검증 블록)을 기본값으로 쓴다.

가능하면 `foundation/control_plane/grok_review_wrapper.py` wrapper(래퍼)를 쓴다. wrapper(래퍼)는 prompt quoting(프롬프트 인용), timeout(시간 제한), stdout/stderr capture(표준 출력/오류 캡처), deterministic noise stripping(결정적 잡음 제거), unexpected top-level artifact detection(예상 밖 최상위 산출물 감지)을 담당한다. wrapper(래퍼)는 Grok content(Grok 내용)를 해석하거나 수용/거절하지 않는다.

wrapper(래퍼)를 `--output-dir`와 함께 쓸 때 `--json(JSON 출력)`은 summary JSON(요약 JSON)만 사용자/에이전트 출력으로 읽는다. raw diagnostics(원본 진단)는 `raw_diagnostics.json`에 보존하고, failure(실패), timeout(시간초과), transport issue(전송 문제), 또는 audit(감사) 필요가 있을 때만 연다. 효과(effect, 효과)는 기록 보존과 token discipline(토큰 규율)을 동시에 유지하는 것이다.

효과(effect, 효과)는 외부 2차 의견을 쓰되, 연구 방향이 산으로 가거나 stage drift(단계 드리프트)가 생기지 않게 하고, 대규모 검토에서도 같은 capture/verify/classify(캡처/검증/분류) 흐름을 유지하는 것이다.

## 5단계 중간 검토 트리거(Five-Stage Retrospective Trigger, 5단계 중간 검토 트리거)

`five_stage_retrospective(5단계 중간 검토)`는 Grok collaboration trigger overlay(그록 협업 트리거 오버레이)다. Primary work family(주 작업군)를 바꾸지 않고 `obsidian-grok-collaboration(그록 협업)`, `five_stage_retrospective_packet(5단계 중간 검토 묶음)`, `next_stage_open_block_check(다음 단계 개방 차단 점검)`를 덧붙인다.

Due check(도래 점검)는 stage closeout(단계 마감) 때 실행한다.

- closing frontier number(마감 전선 번호)가 5의 배수면 due(도래)다.
- 그렇지 않아도 `docs/registers/five_stage_retrospective_register.yaml`의 `closed_frontier_ids_since_last_retrospective`가 5개면 due(도래)다.
- due(도래)가 아니면 `not_due(아직 아님)`로 기록하고 다음 stage open(단계 개방)을 허용한다.
- due(도래)이면 최근 5개 canonical closeout stage ids(정식 마감 단계 ID)를 scope(범위)로 묶고, Grok review(그록 검토), Codex local verification(코덱스 로컬 검증), advice classification(조언 분류), compact retrospective report(압축 중간 검토 보고)를 남기기 전에는 다음 frontier stage(전선 단계)를 열지 않는다.

이 검토는 per-stage Grok receipt(단계별 그록 영수증)를 다시 읽는 repetition(반복)이 아니다. Cross-stage synthesis(단계 간 종합)만 허용하며, allowed claims(허용 주장)는 direction_delta(방향 변화)와 repair_priority_delta(수리 우선순위 변화)뿐이다.

Due check(도래 점검)는 register-first(등록부 우선)다. `not_due(아직 아님)`이면 이전 5개 stage artifacts(단계 산출물), Grok packets(그록 묶음), synthesis template(종합 템플릿)을 열지 않고 gate status(게이트 상태)만 기록한다. 효과(effect, 효과)는 5단계 루틴을 유지하면서 아직 도래하지 않은 회고 준비가 작업을 길게 늘리지 않게 하는 것이다.

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
- `obsidian-work-packet-router`: work family(작업군), primary skill(주 스킬), support skills(보조 스킬), required gates(필수 제한문)를 고른다.
- `obsidian-workflow-drift-guard`: blocker(차단 지점), missing material(빠진 재료), recovery action(복구 행동)을 정리한다.
- `obsidian-grok-collaboration`: Grok(Grok)을 외부 2차 의견(second opinion, 2차 의견)으로 호출하고, 방향성 제시(direction proposal, 방향성 제시), 2차 토론(second discussion, 2차 토론), 로컬 재검증(local verification, 로컬 검증)을 하나의 패킷(packet, 묶음)으로 관리한다.

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
