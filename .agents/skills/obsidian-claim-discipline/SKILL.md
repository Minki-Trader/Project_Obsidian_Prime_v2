---
name: obsidian-claim-discipline
description: Enforce claim discipline in Project Obsidian Prime v2 by downgrading planning or pending states, separating parity levels, and preventing overstatement of closure or readiness. Use when writing docs, reviews, status notes, or user-facing summaries.
---

# Obsidian Claim Discipline

Use this skill when writing, editing, or summarizing project state.

## Trigger Tokens

If any relevant field contains one of these tokens, switch into strict claim discipline:

- `pending_*`
- `planning_*`
- `draft`
- `placeholder_*`
- `not_yet_evaluated`
- `not_applicable`

## Required Behavior

1. Do not describe pending or planning artifacts as:
   - `closed`
   - `materialized`
   - `durable`
   - `parity-closed`
   - `exploration-ready`
2. Use precise language:
   - `planning scaffold`
   - `materialized evidence`
   - `model-input parity`
   - `runtime-helper parity`
   - `bundle handoff verification`
   - `broader-sample parity`
3. If a closure claim is made, name the backing artifact, report, or decision memo.
4. If legacy evidence is referenced, mark it `prior evidence only`.
5. If local-only artifacts are relied upon, ensure their identity is represented in `docs/registers/artifact_registry.csv` before describing them as reusable.

## Project-Specific Guardrails

- `planning scaffold` is not `materialized evidence`.
- `foundation stage closure` is not `exploration-ready`.
- `handoff verification` is not `runtime parity closure`.
