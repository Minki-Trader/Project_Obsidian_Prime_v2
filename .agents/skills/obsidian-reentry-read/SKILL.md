---
name: obsidian-reentry-read
description: Re-enter Project Obsidian Prime v2 safely by reading the current truth in order, restating the active stage and foundation status, and avoiding stale assumptions. Use when starting or resuming work in this repository.
---

# Obsidian Reentry Read

Use this skill whenever work starts or resumes inside `Project_Obsidian_Prime_v2`.

## Workflow

1. Open `AGENTS.md`, then open `docs/policies/reentry_order.md`.
2. Follow the canonical ordered pass and truth precedence defined there.
3. If the task touches feature/model/pipeline/artifact architecture, alpha-search framing, repo-scoped skills, agent settings, or Korean encoding, also read `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md`.
4. Validate before acting:
   - `docs/workspace/workspace_state.yaml` names one active stage
   - the active stage `selection_status.md` agrees with that stage
   - the latest durable stage-handoff decision matches the same transition
   - if any of those disagree, stop and surface state fragmentation before continuing
5. Restate:
   - active stage
   - current foundation truth
   - current operating-truth boundary
   - what is planning only
   - what is materialized
   - what remains open
   - architecture debt interaction when relevant
6. Do not start work from memory alone.

## Project-Specific Guardrails

- This repo is a `concept-preserving reboot`, not a legacy continuation.
- `legacy` findings are `prior evidence only` unless a v2 artifact closes the same question.
- `Stage 00` is closed as planning scaffold complete.
- derive the current active stage from `docs/workspace/workspace_state.yaml` and active stage docs; do not hard-code the stage name in this skill
- registered architecture debt is not a normal pattern to copy into later stages
