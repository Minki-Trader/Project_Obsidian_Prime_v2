---
name: obsidian-task-packet
description: Convert the current Project Obsidian Prime v2 truth state into one bounded task packet so implementation, verification, and publish behavior stay narrow and explicit.
---

# Obsidian Task Packet

Use this skill when the user asks for a plan, asks to create a task packet, or asks to proceed without a narrow current packet.

## When To Trigger

- the user asks `계획 수립해줘`
- the user asks `작업 패킷 만들어줘`
- implementation or verification is about to begin without a fixed scope
- an older packet no longer matches the active stage or current durable decisions

## Do First

1. Confirm the active stage from `docs/workspace/workspace_state.yaml` and the active stage `selection_status.md`.
2. Read the active stage `00_spec/stage_brief.md` and `01_inputs/input_refs.md` only as far as needed to choose one primary task.
3. If a same-thread session-intake summary already exists, reuse it instead of rebuilding the whole read.
4. Decide whether the task is architecture-sensitive: feature/model/pipeline/artifact, alpha-search framing, stage transition, repo-scoped skill, agent setting, or Korean encoding work.

## Must Read

- `docs/workspace/workspace_state.yaml`
- the active stage `04_selected/selection_status.md`
- the active stage `00_spec/stage_brief.md`
- the active stage `01_inputs/input_refs.md`
- the latest relevant decision memo when it changes the next required evidence
- `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md` when the task is architecture-sensitive

## Must Output

- `task_id`
- `goal`
- `allowed_paths`
- `do_not_touch`
- `expected_artifacts`
- `verification_minimum`
- `real_env_required`
- `publish_target`
- `stop_conditions`
- `done_definition`
- `architecture_guard_required`
- `debt_register_update`
- `encoding_verification`

## Do Not

- put more than one primary task in the packet
- widen the packet into stage transition or operating promotion unless the user explicitly asked for that
- treat `publish_target=main` as the default
- leave verification, stop conditions, or expected artifacts implicit
- normalize registered architecture debt as acceptable project style

## Stop Conditions

- current truth sources disagree on the active stage
- the needed changes would fall outside the packet's allowed paths
- the packet would require real-environment verification that cannot be run or justified in the current pass
- the packet would deepen registered architecture debt without an explicit decision memo

## Verification

- derive the narrowest sufficient verification from the touched surface
- mark `real_env_required=yes` only when MT5 execution, tester orchestration, runtime parity flow, import/export boundaries, or another environment-dependent path is touched
- keep `publish_target` at `branch_only` or `none` unless the user explicitly asks for `main` or a durable operating packet already authorizes it
- run the architecture guard validator when agent settings, repo-scoped skills, architecture policies, debt registers, or Korean docs are touched

## Completion Criteria

- one bounded primary task is fixed
- the packet is narrow enough that `진행해줘` can execute it without improvising new scope
- the packet makes the publish default and stop conditions explicit before files change
- architecture risk and encoding verification are explicit when relevant
