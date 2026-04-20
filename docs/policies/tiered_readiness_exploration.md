# Tiered Readiness Exploration

This file defines a downstream exploration framework for `Tier A / Tier B / Tier C readiness` in `Project_Obsidian_Prime_v2`.

It now also fixes the first Stage 06 deterministic boundary (`deterministic boundary`, 결정형 경계) as a docs-only governance lock (`docs-only governance lock`, 문서 전용 거버넌스 잠금). It is not a replacement for the current strict contract line.

## Boundary

- current strict line: `exact timestamp alignment` plus `all-or-skip`
- current strict line status: still active as the only contract-aligned runtime rule
- this file status: `downstream exploration only with the first deterministic Stage 06 boundary now fixed at the governance layer`
- this file does not override:
  - `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
  - `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
  - `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- do not use this file to claim that Stage `03` runtime parity is closed
- do not use this file to relax current Stage `03` or Stage `04` closure gates
- do not use this file to reopen alpha or range search before Stage `05` closes
- this first Stage 06 boundary is a docs-only governance lock; it does not materialize a scorecard, a report, a runtime family, or new registry rows by itself

## Why This Exists

- the first v2 materialized dataset showed that `invalid_rows` are dominated by `external_alignment_missing`
- that mismatch is driven mostly by off-hours equity-symbol sparsity rather than by `US100` base-frame corruption
- legacy behavior treated those rows as `ready / not ready` with no middle operating state
- the tiered framework is a way to model the gray zone honestly without pretending partial context is the same thing as full contract alignment

## Group Complete Definition

A group is `complete` only when all of the following are true at the exact timestamp:

- the group's required symbols and required fields exist
- no `forward-fill` or `fabricate` path is used
- the group's required semantics are computable

## Group Definitions

### Group 1. Contract Base

- `US100` closed `M5` bar exists
- no partial current-bar values
- no numeric-invalid state on required main-symbol primitives
- contract version and feature order remain aligned

If this group fails, the row is automatically `tier_c`.

### Group 2. Session Semantics

- `America/New_York` session meaning is available
- required session-derived fields are computable
- no ambiguous or missing session semantic state

If this group fails, the row is automatically `tier_c`.

### Group 3. Macro Proxy Context

- `VIX`
- `US10YR`
- `USDX`

This group represents broad macro and volatility context and is complete only when all three symbols satisfy the group-complete definition.

### Group 4. Leader Equity Context

- `NVDA`
- `AAPL`
- `MSFT`
- `AMZN`

This group represents the higher-priority contract equity leaders and is complete only when all four symbols satisfy the group-complete definition.

### Group 5. Breadth Extension Context

- `AMD`
- `GOOGL.xnas`
- `META`
- `TSLA`

This group extends equity breadth and cross-check depth beyond the leader group and is complete only when all four symbols satisfy the group-complete definition.

## Canonical Readiness Rule

Apply the rule below exactly until a later explicit Stage 06 decision replaces it:

- if `Group 1` or `Group 2` fails -> `tier_c`
- else if `Group 3`, `Group 4`, and `Group 5` are all complete -> `tier_a`
- else if exactly `1` or `2` of `Group 3` to `Group 5` are complete -> `tier_b`
- else -> `tier_c`

`B-mixed-partial` remains a vocabulary-only candidate term and is not an eligible materialized readiness rule in the first Stage 06 boundary.

## Readiness Meaning

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
- external complete-group count: `exactly 1 or 2 of Group 3 to Group 5`
- operating meaning:
  - this is not contract-equivalent to Tier A
  - this is a candidate `risk-scaled partial-readiness line`
  - it must be treated as a separate operating family, not as a relaxed spelling of Tier A
- mandatory safeguards:
  - use a separate readiness label in every dataset, runtime, and report artifact
  - do not silently forward-fill or fabricate missing external context
  - do not compare Tier B performance head-to-head with Tier A without separate reporting lanes
  - do not assume a Tier A-trained model is safe on Tier B inputs without an explicit study

### Tier C Readiness

- contract base: `missing or invalid`
- or session semantics: `missing or invalid`
- or external complete-group count: `0`
- operating meaning:
  - hard skip
  - not tradable
  - not eligible for reduced-risk substitution

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

## Document Interface

Future Stage 06 artifacts that touch tiered readiness must use the interface below:

- `readiness_tier`: `tier_a | tier_b | tier_c`
- `missing_groups`: `g1_contract_base | g2_session_semantics | g3_macro_proxy | g4_leader_equity | g5_breadth_extension`
- `missing_symbols`: the symbol list that explains why a group was not complete at the exact timestamp
- `reporting_lane`: `strict_tier_a | tier_b_exploration`

`tier_c` is a skip classification, not a reporting lane.

## Data And Reporting Requirements

If a future stage explores tiered readiness, every affected artifact must record:

- readiness tier for each row or run using `readiness_tier`
- missing-group summary using `missing_groups`
- symbol-level missing explanation using `missing_symbols`
- tier-specific row counts
- tier-specific KPI summary
- whether the run used `strict_tier_a`, `tier_b_exploration`, or both
- any first materialized dataset, runtime, or report identity artifact that adopts this interface must add the corresponding `artifact_registry.csv` rows in the same pass

## Non-Binding Future Exploration Notes

The notes below are not part of the canonical readiness rule and must not override it:

- heuristic phrases such as `materially present` and `not fully collapsed` remain historical planning language only
- candidate Tier B vocabulary such as `B-macro-strong` and `B-equity-strong` may still be useful for later analysis notes, but not as eligibility rules
- `B-mixed-partial` remains vocabulary only and is not eligible in the first materialized Stage 06 boundary
- starting-risk defaults for a later reduced-risk study may still be explored, but only after a later explicit Stage 06 decision and not from this rule alone

## Stage Placement

- this framework is downstream of the current foundation path
- do not implement as the active runtime rule during Stages `03` to `05`
- the earliest natural home is a later exploration stage after:
  - `03_runtime_parity_closure`
  - `04_artifact_identity_closure`
  - `05_exploration_kernel_freeze`

## Current Claim Boundary

- current v2 runtime rule: `Tier A only`
- Tier B status: `accepted as a future exploration design with the first deterministic boundary fixed and the first materialized Stage 06 row-label scorecard plus review report now written on that boundary; no reduced-risk runtime family or operating promotion is materialized yet`
- Tier C status: `hard skip remains current policy whenever strict contract requirements fail`
