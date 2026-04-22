﻿# Agent Trigger Policy

This note defines the repo-scoped `skills` layer that complements `AGENTS.md`.

Canonical re-entry order and truth precedence live in `docs/policies/reentry_order.md`. This note should not maintain a second full ordered read list or a competing precedence list.

## Purpose

- keep `AGENTS.md` focused on always-on project rules
- route repetitive agent behavior through narrow reusable skills
- reduce repeated mistakes around re-entry, claim language, and stage transitions

## Placement

- repo-scoped skills live in `.agents/skills/`
- this is a narrow allowed root exception for reusable agent workflows only
- current trigger policy lives in `docs/policies/agent_trigger_policy.md`

## Precedence

- use the truth precedence defined in `docs/policies/reentry_order.md`
- this policy may refine skill routing but does not override that precedence

## README State Hygiene

- treat `README.md` as an orientation entrypoint, not as the authoritative live-state source
- keep mutable current-state facts such as `active_stage`, stage closure status, current branch truth, and current priorities in `docs/workspace/workspace_state.yaml`, `docs/context/current_working_state.md`, the active stage `selection_status.md`, and durable decision memos
- if `README.md` still contains mutable current-state wording, the same pass that changes that meaning must either sync those lines or replace them with pointers to the authoritative current-truth docs
- prefer removing volatile status snapshots from `README.md` over maintaining a second state ledger there

## Session Mode Contract

Every working turn should first fit one primary session mode:

- `reentry_only`
- `status_summary`
- `next_task_planning`
- `implementation_pass`
- `verification_pass`
- `stage_transition`
- `publish_pass`

If the user prompt is broad, choose the narrowest mode that still completes the turn safely.

## Core Trigger Map

### `obsidian-session-intake`

Use when:

- a new thread starts in this repo
- work resumes after a pause
- the user asks for status, current progress, or the next safest task
- implementation is requested but no current task packet is fixed yet

Required effect:

- choose one primary session mode before doing substantial work
- run a full cold re-entry only when the thread is cold, the active stage is unclear, or durable meaning may have shifted
- prefer a same-thread delta check when the thread is warm and the active stage is already stable
- restate the active stage, current foundation truth, current operating-truth boundary, planning-only items, materialized items, open items, forbidden shortcuts, recommended next task, allowed scope, stop conditions, and default publish target before drifting into implementation

### `obsidian-reentry-read`

Use when:

- a new thread starts in this repo
- work resumes after a pause
- the active stage or current read is unclear

Required effect:

- read the repo in the documented re-entry order
- restate the active stage, current foundation status, and current truth boundary before making decisions
- do not begin stage work from stale assumptions
- do not repeat a full cold re-entry inside the same stable thread when a narrower delta check is sufficient

### `obsidian-claim-discipline`

Use when:

- writing or editing freeze cards, review notes, status notes, decisions, or user-facing summaries
- any field contains `pending_*`, `planning_*`, `draft`, `placeholder_*`, `not_yet_evaluated`, or `not_applicable`
- closure, materialization, readiness, or parity claims are being made

Required effect:

- downgrade claims when the evidence state is still planning or pending
- distinguish `planning scaffold`, `materialized evidence`, `runtime parity closure`, and `exploration-ready` explicitly
- mark legacy findings as `prior evidence only` unless a v2 artifact closes the same question
- if an overview document such as `README.md` contains mutable live-state wording, either sync it in the same pass or rewrite it so it points at the authoritative current-truth docs instead

### `obsidian-task-packet`

Use when:

- the user asks `계획 수립해줘`
- the user asks `작업 패킷 만들어줘`
- implementation or verification should be narrowed before files change
- the current packet is missing, stale, or too broad for a safe pass

Required effect:

- choose one primary task only
- derive that task from the active stage brief, selection status, current decision memos, and current session mode
- output a bounded packet with `task_id`, `goal`, `allowed_paths`, `do_not_touch`, `expected_artifacts`, `verification_minimum`, `real_env_required`, `publish_target`, `stop_conditions`, and `done_definition`
- keep `publish_target` at `branch_only` or `none` unless the user explicitly asks for `main` completion

### `obsidian-stage-transition`

Use when:

- a stage opens, closes, or hands off work to the next stage
- `active_stage` changes
- a selection note changes operational meaning

Required effect:

- follow the canonical same-pass sync list defined in this policy
- never close a stage by implying later-stage evidence is already complete
- if `README.md` carries mutable stage or closure wording, sync or neutralize it in the same pass so it does not become a competing stale state source

### `obsidian-publish-merge`

Use when:

- the user explicitly asks for `브랜치랑 메인머지까지`
- the user explicitly asks to `메인까지 올려줘`
- the user explicitly asks for push plus branch-to-`main` completion in one pass
- an approved current task packet explicitly names `publish_target=main`

Required effect:

- finish the requested work before starting the publish flow
- stage and commit only the intended scope
- push the working branch first
- update against the latest remote `main` before merging
- merge into local `main` only when the branch is ready and the working tree is clean
- push `origin/main` in the same pass when no blocker remains
- stop and surface the blocker explicitly if remote `main`, branch history, or working-tree state makes a clean merge unsafe
- do not infer `main` publish from implementation completion alone

## Canonical Same-Pass Sync Norm

The canonical same-pass sync norm lives in this file and applies whenever stage-level operational meaning changes durably.

Required same-pass files:

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- the active or closing stage `04_selected/selection_status.md`
- the active or closing stage `03_reviews/review_index.md` when needed
- `docs/decisions/*.md` when the change is durable
- `docs/registers/artifact_registry.csv` when dataset, bundle, runtime, or report identity rows are added or superseded
- `docs/workspace/changelog.md`
- `README.md` when it still contains mutable current-state language that the same pass would otherwise leave stale

## Always-On Claim Guardrails

- `planning scaffold` is not `materialized evidence`
- `handoff verification` is not `runtime parity closure`
- `legacy prior evidence` is not `current v2 foundation truth` or `current v2 operating truth`
- `foundation stage closure` is not `exploration-ready`

## Verification Escalation (`검증 상향 규칙`)

- start with the smallest sufficient local verification
- if a change touches MT5 execution, tester orchestration, runtime parity flow, file import/export boundaries, or another environment-dependent path, add the narrowest real-environment check (`실환경 검증`) before reporting the work as verified
- prefer the active stage pack plus the native MT5 runner when that is the closest contract-surface check
- docs-only, wording-only, registry-only, or isolated pure-Python changes may stop at local verification when they do not alter an environment-dependent path
- when real-environment verification is skipped, state why it was unnecessary or infeasible

## Prompt Routing Hints

- `현재 진행사항 파악해줘`, `지금 어디까지 왔어`, `상태 요약해줘`: start with `obsidian-session-intake`
- `바로 다음 작업은?`, `다음 작업 골라줘`: start with `obsidian-session-intake` and return one recommended next task
- `계획 수립해줘`, `작업 패킷 만들어줘`: use `obsidian-task-packet`
- `진행해줘`: execute the current approved task packet; if none exists, create or reconstruct one before implementation
- `브랜치랑 메인머지까지`, `메인까지 올려줘`: use `obsidian-publish-merge`

## Dynamic Active Routing

- derive the current active stage from `docs/workspace/workspace_state.yaml` and the active stage `selection_status.md`
- use `obsidian-session-intake` and `obsidian-claim-discipline` as the default primary pair for any new or resumed thread
- let `obsidian-session-intake` decide whether the thread needs full cold re-entry or only a same-thread delta check
- use `obsidian-task-packet` before implementation or verification whenever the current packet is missing or ambiguous
- use `obsidian-stage-transition` whenever `active_stage` or stage-level operational meaning changes durably
- use `obsidian-publish-merge` only when the user explicitly asks for branch push plus `main` merge completion in the same pass or an approved task packet explicitly names `publish_target=main`
- do not auto-trigger `obsidian-publish-merge` only because a verified implementation pass finished
