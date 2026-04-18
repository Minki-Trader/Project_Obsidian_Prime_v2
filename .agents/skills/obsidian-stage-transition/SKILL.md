---
name: obsidian-stage-transition
description: Open, close, or hand off stages in Project Obsidian Prime v2 without state fragmentation. Use when active_stage changes, a stage is closed, or work is passed to the next foundation stage.
---

# Obsidian Stage Transition

Use this skill whenever a stage opens, closes, or hands work to another stage.

## Required Sync Pass

Update in the same pass:

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- current or closing stage `04_selected/selection_status.md`
- current or closing stage `03_reviews/review_index.md` when needed
- next stage `00_spec/stage_brief.md`
- next stage `01_inputs/input_refs.md`
- `docs/decisions/*.md` when the transition is durable
- `docs/workspace/changelog.md`

## Transition Rules

1. Never close a stage by implying later-stage evidence is already complete.
2. Give every remaining blocker an explicit downstream home.
3. Preserve the difference between:
   - planning closure
   - dataset-contract closure
   - runtime parity closure
   - artifact identity closure
4. Keep `active_stage` aligned everywhere after the transition.

## Project-Specific Guardrails

- `Stage 00` may close as planning scaffold complete.
- `Stage 01` owns the first materialized dataset-contract evidence.
- `Stage 03` owns evaluated runtime parity.
- `Stage 04` owns broader artifact identity closure.
