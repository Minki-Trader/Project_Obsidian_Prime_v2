# Tiered Readiness Exploration

This file defines a downstream exploration framework for `Tier A / Tier B / Tier C readiness` in `Project_Obsidian_Prime_v2`.

It is a planning and design note for a future separate operating family, not a replacement for the current strict contract line.

## Boundary

- current strict line: `exact timestamp alignment` plus `all-or-skip`
- current strict line status: still active as the only contract-aligned runtime rule
- this file status: `downstream exploration only`
- this file does not override:
  - `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
  - `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
  - `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- do not use this file to claim that Stage `03` runtime parity is closed
- do not use this file to relax current Stage `03` or Stage `04` closure gates
- do not use this file to reopen alpha or range search before Stage `05` closes

## Why This Exists

- the first v2 materialized dataset showed that `invalid_rows` are dominated by `external_alignment_missing`
- that mismatch is driven mostly by off-hours equity-symbol sparsity rather than by `US100` base-frame corruption
- legacy behavior treated those rows as `ready / not ready` with no middle operating state
- the tiered framework is a way to model the gray zone honestly without pretending partial context is the same thing as full contract alignment

## Group Definitions

### Group 1. Contract Base

- `US100` closed `M5` bar exists
- no partial current-bar values
- no numeric-invalid state on required main-symbol primitives
- contract version and feature order remain aligned

If this group fails, the row is automatically `Tier C`.

### Group 2. Session Semantics

- `America/New_York` session meaning is available
- required session-derived fields are computable
- no ambiguous or missing session semantic state

If this group fails, the row is automatically `Tier C`.

### Group 3. Macro Proxy Context

- `VIX`
- `US10YR`
- `USDX`

This group represents broad macro and volatility context.

### Group 4. Leader Equity Context

- `NVDA`
- `AAPL`
- `MSFT`
- `AMZN`

This group represents the higher-priority contract equity leaders.

### Group 5. Breadth Extension Context

- `AMD`
- `GOOGL.xnas`
- `META`
- `TSLA`

This group extends equity breadth and cross-check depth beyond the leader group.

## Readiness Matrix

### Tier A Readiness

- contract base: `present`
- session semantics: `present`
- macro proxy context: `3 / 3 present`
- leader equity context: `4 / 4 present`
- breadth extension context: `4 / 4 present`
- operating meaning:
  - this is the current strict contract line
  - full contract-aligned model-input surface is available
  - full-risk eligibility may be considered by the active line
- comparison rule:
  - this is the only line that can be compared directly with the current strict legacy-compatible readiness rule

### Tier B Readiness

- contract base: `present`
- session semantics: `present`
- macro proxy context: `not fully collapsed`
- at least one external context family remains materially present
- one or more external context families are incomplete or missing at the exact timestamp
- operating meaning:
  - this is not contract-equivalent to Tier A
  - this is a candidate `risk-scaled partial-readiness line`
  - it must be treated as a separate operating family, not as a relaxed spelling of Tier A
- allowed candidate subprofiles:
  - `B-macro-strong`: macro proxy context intact while one or both equity families are incomplete
  - `B-equity-strong`: at least one equity family remains materially present while macro proxy context is partial but not collapsed
  - `B-mixed-partial`: several groups are incomplete, but base and session remain intact and the row still carries non-trivial context
- mandatory safeguards:
  - use a separate readiness label in every dataset, runtime, and report artifact
  - do not silently forward-fill or fabricate missing external context
  - do not compare Tier B performance head-to-head with Tier A without separate reporting lanes
  - do not assume a Tier A-trained model is safe on Tier B inputs without an explicit study
- starting-risk defaults for future exploration:
  - max size: `0.25x` to `0.50x` of Tier A
  - entry threshold: stricter than Tier A
  - concurrent exposure cap: lower than Tier A
  - hold-time bias: shorter than Tier A unless a separate study justifies otherwise

### Tier C Readiness

- contract base: `missing or invalid`
- or session semantics: `missing or invalid`
- or external context: `collapsed enough that the row is not honestly tradable even as a partial-context line`
- operating meaning:
  - hard skip
  - not tradable
  - not eligible for reduced-risk substitution

## Initial Practical Rule Of Thumb

Use the framework below until a later stage replaces it with a tested contract:

- if `Group 1` or `Group 2` fails: `Tier C`
- if all groups are fully present: `Tier A`
- if `Group 1` and `Group 2` pass and at least one external context family is still materially present, but exact full alignment is not available: `Tier B`
- if `Group 1` and `Group 2` pass but the remaining external context is too thin to explain risk honestly: `Tier C`

## What Tier B Is Allowed To Change

- risk sizing
- entry threshold
- exposure cap
- reporting lane
- readiness label

## What Tier B Is Not Allowed To Change

- closed-bar only semantics
- exact timestamp truth about what was missing
- contract-order feature naming and order
- artifact identity discipline
- stage closure claims for current strict parity work

## Data And Reporting Requirements

If a future stage explores tiered readiness, every affected artifact must record:

- readiness tier for each row or run
- missing-group summary
- tier-specific row counts
- tier-specific KPI summary
- whether the run used the strict line, the reduced-risk line, or both

## Stage Placement

- this framework is downstream of the current foundation path
- do not implement as the active runtime rule during Stages `03` to `05`
- the earliest natural home is a later exploration stage after:
  - `03_runtime_parity_closure`
  - `04_artifact_identity_closure`
  - `05_exploration_kernel_freeze`

## Current Claim Boundary

- current v2 runtime rule: `Tier A only`
- Tier B status: `accepted as a future exploration design, not yet implemented`
- Tier C status: `hard skip remains current policy whenever strict contract requirements fail`
