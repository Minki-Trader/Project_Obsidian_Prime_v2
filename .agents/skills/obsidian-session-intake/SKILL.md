---
name: obsidian-session-intake
description: Start each Project Obsidian Prime v2 turn by selecting one narrow session mode, choosing cold re-entry versus warm-thread delta check, and fixing the allowed scope before implementation drifts open.
---

# Obsidian Session Intake

Use this skill at the start of a working turn when the user asks for current status, next work, or implementation without a fixed packet.

## When To Trigger

- a new thread starts in this repo
- work resumes after a pause
- the user asks for current progress, current state, or the next task
- the user asks to proceed but no current task packet is fixed yet

## Do First

1. Choose one primary session mode:
   - `reentry_only`
   - `status_summary`
   - `next_task_planning`
   - `implementation_pass`
   - `verification_pass`
   - `stage_transition`
   - `publish_pass`
2. Decide whether the thread is cold or warm.
3. If the thread is warm and the active stage is stable, prefer a delta check instead of repeating full cold re-entry.
4. Decide whether the requested turn is architecture-sensitive: feature/model/pipeline/artifact, alpha-search framing, stage transition, repo-scoped skill, agent setting, or Korean encoding work.

## Must Read

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md` when the current read needs support
- the active stage `04_selected/selection_status.md`
- the latest durable decision memo only when it changes current meaning or the user asks why
- `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md` when the requested turn is architecture-sensitive

## Must Output

- `session_mode`
- `active_stage`
- `current_foundation_truth`
- `current_operating_truth_boundary`
- `planning_only`
- `materialized`
- `open_items`
- `forbidden_shortcuts`
- `recommended_next_task`
- `allowed_scope`
- `stop_conditions`
- `publish_default`
- `architecture_guard_required` when relevant

## Do Not

- repeat full cold re-entry inside the same stable thread when a narrower delta check is enough
- invent a new active stage or reopen a closed stage from chat momentum alone
- let orientation docs outrank `workspace_state.yaml`, stage selection status, or durable decisions
- drift from status intake straight into implementation without first fixing the scope
- ignore architecture debt when the turn touches feature/model/pipeline/artifact, alpha-search, stage-transition, skill, agent-setting, or encoding work

## Stop Conditions

- `workspace_state.yaml` and the active stage `selection_status.md` disagree on the active stage
- a durable decision memo contradicts the supposed current boundary
- the requested turn would cross from status or planning into implementation without an approved packet

## Verification

- check that the named active stage is the same across the current truth sources you used
- if a current task packet already exists, confirm it still fits the active stage and current durable decisions
- if architecture-sensitive, confirm whether the architecture guard validator is part of the verification surface

## Completion Criteria

- one session mode is selected
- one recommended next task is named
- the allowed scope and publish default are explicit enough that the next step can stay narrow
- architecture-sensitive work is routed to `obsidian-architecture-guard` regardless of active stage number
