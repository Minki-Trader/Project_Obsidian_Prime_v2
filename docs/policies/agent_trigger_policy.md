# Agent Trigger Policy

This note defines the repo-scoped `skills` layer that complements `AGENTS.md`.

## Purpose

- keep `AGENTS.md` focused on always-on project rules
- route repetitive agent behavior through narrow reusable skills
- reduce repeated mistakes around re-entry, claim language, and stage transitions

## Placement

- repo-scoped skills live in `.agents/skills/`
- this is a narrow allowed root exception for reusable agent workflows only
- current trigger policy lives in `docs/policies/agent_trigger_policy.md`

## Precedence

When a skill and a project document appear to disagree, resolve in this order:

1. `docs/workspace/workspace_state.yaml`
2. active stage `04_selected/selection_status.md`
3. latest durable `docs/decisions/*.md`
4. `docs/context/current_working_state.md`
5. `AGENTS.md`
6. this trigger policy
7. stage briefs, review indexes, and templates

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
- `legacy prior evidence` is not `current v2 truth`
- `foundation stage closure` is not `exploration-ready`

## Current Active Routing

- current active stage: `01_dataset_contract_freeze`
- immediate primary skill pair:
  - `obsidian-reentry-read`
  - `obsidian-claim-discipline`
- use `obsidian-stage-transition` whenever Stage 01 changes durable project state
