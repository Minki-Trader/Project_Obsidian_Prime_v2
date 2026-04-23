---
name: obsidian-stage-transition
description: Open, close, or hand off stages in Project Obsidian Prime v2 without state fragmentation. Use when active_stage changes, a stage is closed, or work is passed to the next foundation stage.
---

# Obsidian Stage Transition

Use this skill whenever a stage opens, closes, or hands work to another stage.

## Required Sync Pass

Use the canonical same-pass sync norm from `docs/policies/agent_trigger_policy.md`.

Update in the same pass:

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- current or closing stage `04_selected/selection_status.md`
- current or closing stage `03_reviews/review_index.md` when needed
- next stage `00_spec/stage_brief.md`
- next stage `01_inputs/input_refs.md`
- `docs/decisions/*.md` when the transition is durable
- `docs/registers/artifact_registry.csv` when dataset, bundle, runtime, or report identity rows are added or superseded
- `docs/workspace/changelog.md`
- `README.md` when it still contains mutable stage, closure, or current-mode wording that this transition would otherwise leave stale
- `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md` when the transition changes feature/model/pipeline/artifact ownership, alpha-search framing, or encoding-sensitive agent behavior
- `docs/policies/exploration_mandate.md`, `docs/registers/idea_registry.md`, and `docs/registers/negative_result_register.md` when the transition opens, closes, archives, or hands off exploration work

## Transition Rules

1. Never close a stage by implying later-stage evidence is already complete.
2. Give every remaining blocker an explicit downstream home.
3. Preserve the difference between:
   - planning closure
   - dataset-contract closure
   - runtime parity closure
   - artifact identity closure
4. Keep `active_stage` aligned everywhere after the transition.
5. Derive current and next stage names from `docs/workspace/workspace_state.yaml`, decision memos, and stage docs; do not hard-code the active stage name in this skill.
6. Prefer replacing volatile `README.md` status snapshots with pointers to the authoritative current-truth docs instead of maintaining a second live-state ledger there.
7. Do not let a new stage inherit registered architecture debt as if it were normal project style.
8. If the transition opens alpha search, separate source cleanup or validation debt closure from the actual alpha-search question.
9. If the transition opens a user-requested extra stage, require charter, lane, question, allowed evidence, exit condition, and no-promotion boundary unless a promotion packet is explicitly opened.
10. If the transition closes exploration, require negative-result memory or a positive archive record before treating the idea as durable knowledge.

## Validation

- after the sync pass, verify that `docs/workspace/workspace_state.yaml`, `docs/context/current_working_state.md`, and the active stage `selection_status.md` all name the same active stage
- if the transition changes durable meaning, make sure a `docs/decisions/*.md` memo exists in the same pass
- if architecture-sensitive docs or skills changed, run the architecture guard validator
- if exploration-sensitive docs or skills changed, verify that lane routing, WFO default, and failure-memory references are still linked from the trigger policy

## Project-Specific Guardrails

- `Stage 00` may close as planning scaffold complete.
- `Stage 01` owns the first materialized dataset-contract evidence.
- `Stage 03` owns evaluated runtime parity.
- `Stage 04` owns broader artifact identity closure.
