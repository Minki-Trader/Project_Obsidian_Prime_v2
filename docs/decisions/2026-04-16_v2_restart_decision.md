# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-16_v2_restart`
- `reviewed_on`: `2026-04-16`
- `owner`: `codex + user`
- `decision`: `start a clean v2 workspace next to the legacy project and treat Stage 00 as a foundation sprint`

## What Was Decided

- adopted:
  - preserve the legacy project untouched
  - create `Project_Obsidian_Prime_v2` as a sibling workspace
  - copy the core contract documents and placeholder weights
  - start v2 with state, registry, and parity-governance setup before new alpha search
- not adopted:
  - continuing the old stage tree in-place
  - treating legacy Stage 42 as an automatic v2 operating promotion
  - reopening broad alpha search immediately

## Why

- the legacy project already proved the strategy concept was worth keeping
- the most expensive confusion came from runtime parity, artifact identity, and late-stage governance hardening
- a clean restart keeps the good contract philosophy while dropping the stage clutter and re-entry burden

## What Remains Open

- the first v2 dataset freeze id and fingerprint
- the first v2 parity harness plan and gold fixture set
- whether the legacy `34D` contract-aligned `min_margin=0.06000` line survives as a v2 operating reference after revalidation

## Evidence Used

- legacy Stage 40 runtime parity deep audit
- legacy Stage 41 targeted feature snapshot audit and margin replay chain
- legacy Stage 42 threshold and margin recalibration read
- restart review package in the legacy workspace

## Operational Meaning

- `current_operating_reference updated?`: `no`
- `shadow updated?`: `no`
- `workspace_state update needed?`: `yes, completed on workspace creation`
- `next mandatory follow-up`: `close Stage 00 foundation gates before any new alpha stage`
