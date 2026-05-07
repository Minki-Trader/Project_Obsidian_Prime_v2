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
