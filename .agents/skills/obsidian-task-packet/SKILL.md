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
5. Decide whether the task is exploration-sensitive: alpha search, idea variants, Tier B/C research, WFO planning, extreme sweep, negative-result closure, or user-requested extra stage.
6. Decide whether the task touches run evidence: run creation, run closeout, KPI report, result summary, result judgment, or run registry update.
7. If code will change, decide whether `obsidian-code-surface-guard` must produce a placement/effect map before implementation.

## Must Read

- `docs/workspace/workspace_state.yaml`
- the active stage `04_selected/selection_status.md`
- the active stage `00_spec/stage_brief.md`
- the active stage `01_inputs/input_refs.md`
- the latest relevant decision memo when it changes the next required evidence
- `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md` when the task is architecture-sensitive
- `docs/policies/exploration_mandate.md`, `docs/registers/idea_registry.md`, and `docs/registers/negative_result_register.md` when the task is exploration-sensitive
- `docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, `docs/policies/result_judgment_policy.md`, and `docs/registers/run_registry.csv` when the task touches run evidence
- `docs/registers/legacy_lesson_register.md` when legacy lessons are mentioned

## Must Output

- `task_id`
- `lane`
- `idea_id`
- `tier_scope`
- `goal`
- `allowed_paths`
- `do_not_touch`
- `expected_artifacts`
- `wfo_required`
- `extreme_sweep_allowed`
- `micro_search_gate`
- `negative_result_required`
- `promotion_gate_applicable`
- `code_surface_map_required`
- `run_evidence_required`
- `run_registry_update`
- `kpi_record_required`
- `result_judgment_required`
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
- treat `promotion_gate_applicable=no` as a reason to skip exploration records
- open micro search before broad sweep evidence identifies a robust region
- use a single-window optimized run as robust evidence without WFO or an explicit scout-only boundary
- close or review a run without naming the KPI record, run identity surface, registry update, and result judgment class
- confuse `negative` with `invalid`, or treat `inconclusive` as quiet success
- let a code task proceed without naming owner, caller, and effect when reusable logic or runtime behavior changes

## Stop Conditions

- current truth sources disagree on the active stage
- the needed changes would fall outside the packet's allowed paths
- the packet would require real-environment verification that cannot be run or justified in the current pass
- the packet would deepen registered architecture debt without an explicit decision memo
- the packet would close an exploration idea without salvage value and reopen condition
- the packet would use Tier C local research as a runtime or promotion lane
- the packet would mark a run reviewed without a run registry update or explicit `n/a` rationale

## Verification

- derive the narrowest sufficient verification from the touched surface
- mark `real_env_required=yes` only when MT5 execution, tester orchestration, runtime parity flow, import/export boundaries, or another environment-dependent path is touched
- keep `publish_target` at `branch_only` or `none` unless the user explicitly asks for `main` or a durable operating packet already authorizes it
- run the architecture guard validator when agent settings, repo-scoped skills, architecture policies, debt registers, or Korean docs are touched
- for exploration tasks, verify that the output can update `idea_registry.md` or `negative_result_register.md` when the result becomes durable
- for run evidence tasks, verify that `run_manifest.json`, `kpi_record.json`, `result_summary.md`, and `run_registry.csv` are either produced, updated, or explicitly marked `n/a` with a reason
- for code tasks, verify that owner module, caller, input/output, and artifact/report effect are explicit before implementation

## Completion Criteria

- one bounded primary task is fixed
- the packet is narrow enough that `진행해줘` can execute it without improvising new scope
- the packet makes the publish default and stop conditions explicit before files change
- architecture risk and encoding verification are explicit when relevant
- lane, WFO default, failure-memory rule, and code-surface rule are explicit when relevant
- run evidence measurement, management, and judgment are explicit when a run result is created, reviewed, summarized, or closed
