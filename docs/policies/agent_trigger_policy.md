# Agent Trigger Policy

이 문서는 저장소 전용 스킬(repo-scoped skills)을 언제 쓰는지 정한다.

핵심 원칙은 단순하다. 작업이 커져도, Stage 5부터 미래 Stage 50+까지 같은 방식으로 시작하고, 같은 방식으로 닫는다.

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
