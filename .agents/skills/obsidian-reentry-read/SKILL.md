---
name: obsidian-reentry-read
description: Re-enter Project Obsidian Prime v2 safely by reading the current truth in order, restating the active stage and foundation status, and avoiding stale assumptions. Use when starting or resuming work in this repository.
---

# Obsidian Reentry Read

Use this skill whenever work starts or resumes inside `Project_Obsidian_Prime_v2`.

## Workflow

1. Read in this order:
   - `README.md`
   - `AGENTS.md`
   - `docs/workspace/workspace_state.yaml`
   - `docs/context/current_working_state.md`
   - latest active stage `04_selected/selection_status.md`
   - latest durable `docs/decisions/*.md` that explain the current stage handoff
   - active stage `00_spec/stage_brief.md`
   - active stage `01_inputs/input_refs.md`
2. Restate:
   - active stage
   - current foundation status
   - what is planning only
   - what is materialized
   - what remains open
3. If documents disagree, resolve in this order:
   - `docs/workspace/workspace_state.yaml`
   - active stage `04_selected/selection_status.md`
   - latest durable decision memo
   - `docs/context/current_working_state.md`
   - `AGENTS.md`
4. Do not start work from memory alone.

## Project-Specific Guardrails

- This repo is a `concept-preserving reboot`, not a legacy continuation.
- `legacy` findings are `prior evidence only` unless a v2 artifact closes the same question.
- `Stage 00` is closed as planning scaffold complete.
- The current active stage is `01_dataset_contract_freeze` until the state docs say otherwise.
