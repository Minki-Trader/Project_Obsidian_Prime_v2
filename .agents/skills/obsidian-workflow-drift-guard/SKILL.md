---
name: obsidian-workflow-drift-guard
description: Prevent work from drifting away from the actual blocker by separating missing material, missing tools, missing environment, missing permission, and changed goals. Use when a task risks processing absent data, pretending an unavailable tool ran, or turning a tool-building task into unrelated validation.
---

# Obsidian Workflow Drift Guard

Use this skill when the work may drift from the original job into a nearby but different job.

## Simple Model

Think of making pottery:

- material: the clay or source data
- tool: the kiln, code path, library, MT5 terminal, or runner
- environment: the place where the tool can really run
- product: the artifact or answer we are trying to make

Do not process clay that does not exist. Do not pretend to fire pottery without a kiln. Do not spend the whole pass re-checking clay when the real blocker is that the kiln is missing.

## Required Check

Before changing direction, identify:

- `product`: what are we trying to produce?
- `material_state`: available, missing, partial, or unknown
- `tool_state`: available, missing, broken, or wrong environment
- `environment_state`: usable, unavailable, unverified, or not required
- `current_blocker`: material, tool, environment, permission, code, or unclear goal
- `next_action`: continue, fetch material, build tool, fix environment, lower claim, or ask user
- `drift_risk`: what nearby task could distract from the real blocker?

## Material Recovery Order

If required material is missing, do not stop at "design is still possible" when the requested product needs that material.

Use this order:

1. Check whether the material already exists inside the current repo or declared current-project data root.
2. Check whether a current repo tool can regenerate it.
3. Check whether the required source data exists inside the current project boundary.
4. If the material cannot be recovered inside the current project boundary, mark the task `blocked` or lower the claim.
5. Do not use legacy snapshots, external folders, old project outputs, forum files, or ad hoc internet artifacts unless the user explicitly asks.

External or legacy material is not a default fallback.

## Guardrails

- If source data is missing, do not create processed outputs as if the source data existed.
- If the required tool or runtime is missing, do not simulate success unless the task is explicitly to create a mock.
- If the job is to build a tool, do not turn the pass into repeated source-data auditing unless new evidence makes that necessary.
- If material is required and missing, name the shortest current-project path to restore or regenerate it.
- If verification cannot run, name whether the blocker is material, tool, environment, or permission.
- If the original goal changes, say that it changed before proceeding.
- Do not close the task with a polished report that only explains why the real work did not happen.

## Good Outcome

The user should be able to tell:

- what was supposed to be made
- what was actually available
- what was missing
- whether the work stayed on target
- what single next action removes the blocker
