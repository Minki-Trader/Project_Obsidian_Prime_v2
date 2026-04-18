# Agent Trigger Policy

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

## Core Trigger Map

### `obsidian-reentry-read`

Use when:

- a new thread starts in this repo
- work resumes after a pause
- the active stage or current read is unclear

Required effect:

- read the repo in the documented re-entry order
- restate the active stage, current foundation status, and current truth boundary before making decisions
- do not begin stage work from stale assumptions

### `obsidian-claim-discipline`

Use when:

- writing or editing freeze cards, review notes, status notes, decisions, or user-facing summaries
- any field contains `pending_*`, `planning_*`, `draft`, `placeholder_*`, `not_yet_evaluated`, or `not_applicable`
- closure, materialization, readiness, or parity claims are being made

Required effect:

- downgrade claims when the evidence state is still planning or pending
- distinguish `planning scaffold`, `materialized evidence`, `runtime parity closure`, and `exploration-ready` explicitly
- mark legacy findings as `prior evidence only` unless a v2 artifact closes the same question

### `obsidian-stage-transition`

Use when:

- a stage opens, closes, or hands off work to the next stage
- `active_stage` changes
- a selection note changes operational meaning

Required effect:

- update in the same pass:
  - `docs/workspace/workspace_state.yaml`
  - `docs/context/current_working_state.md`
  - the active stage `04_selected/selection_status.md`
  - the active stage `03_reviews/review_index.md` when needed
  - `docs/decisions/*.md` when the change is durable
- never close a stage by implying later-stage evidence is already complete

## Always-On Claim Guardrails

- `planning scaffold` is not `materialized evidence`
- `handoff verification` is not `runtime parity closure`
- `legacy prior evidence` is not `current v2 foundation truth` or `current v2 operating truth`
- `foundation stage closure` is not `exploration-ready`

## Dynamic Active Routing

- derive the current active stage from `docs/workspace/workspace_state.yaml` and the active stage `selection_status.md`
- use `obsidian-reentry-read` and `obsidian-claim-discipline` as the default primary pair for any new or resumed thread
- use `obsidian-stage-transition` whenever `active_stage` or stage-level operational meaning changes durably
