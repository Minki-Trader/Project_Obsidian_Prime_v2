# Broader-Sample Parity Charter

## Status

- `adr_id`: `0002`
- `reviewed_on`: `2026-04-19`
- `status`: `accepted`
- `scope`: `Stage 05 kernel freeze and first broader-pack materialization only; broader-sample parity is not yet evaluated or closed`

## Intent

- `broader-sample parity` is the first downstream validation lane after the closed Stage 04 artifact-identity read
- this lane is a `pre-exploration validation lane`
- it does not replace the Stage 03 `5-window` minimum pack
- it does not close `runtime-helper parity`
- it does not open `Tier B` reduced-risk work
- it does not change the current strict Tier A runtime rule

## What This Lane Proves

- whether model-input parity on the existing contract surface still holds on a wider, stratified sample than the first `5-window` minimum pack
- whether the existing artifact family can scale to a wider parity pack without changing public runtime interfaces

## What This Lane Does Not Prove

- no `runtime-helper parity` closure
- no `Tier B / Tier C` exploration readiness
- no alpha or range readiness
- no operating promotion

## Fixed Pack Shape

- pack type: `fixed stratified audit pack`
- pack size: `24 windows`
- ready rows: `16`
- negative non-ready rows: `8`

## Ready Strata

- `regular_cash_session`
  - `4 windows`
  - normal US cash-session middle segment
  - ready row only
- `cash_close_boundary`
  - `4 windows`
  - `15:55` or `16:00 America/New_York`
  - ready row only
- `dst_sensitive`
  - `4 windows`
  - must cover both `UTC-4` and `UTC-5`
  - ready row only
- `full_external_alignment`
  - `4 windows`
  - all required external symbols exact-timestamp matched
  - ready row only

## Negative Strata

- `cash_open_missing_equities`
  - `4 windows`
  - around `09:35 America/New_York`
  - equity external alignment missing
  - non-ready row only
- `off_hours_external_alignment_missing`
  - `4 windows`
  - off-hours or sparse-time external alignment missing
  - non-ready row only

## Selection Rules

- every window must use a distinct `timestamp_utc`
- include at least `6 distinct calendar months`
- include at least `3 distinct weekdays`
- include both `UTC-4` and `UTC-5`
- if a ready row matches multiple ready strata, use priority:
  - `dst_sensitive > cash_close_boundary > full_external_alignment > regular_cash_session`
- if a negative row matches multiple negative strata, use priority:
  - `cash_open_missing_equities > off_hours_external_alignment_missing`
- keep `all-or-skip` semantics unchanged
- do not reinterpret negative rows as reduced substitutes

## Reserved Identifiers

- `fixture_set_id`: `fixture_fpmarkets_v2_runtime_broader_0001`
- `bundle_id`: `bundle_fpmarkets_v2_runtime_broader_0001`
- `runtime_id`: `runtime_fpmarkets_v2_mt5_snapshot_broader_0001`
- `report_id`: `report_fpmarkets_v2_runtime_broader_parity_0001`

## Artifact Family

- reuse the existing minimum-pack family shape
- required artifacts:
  - fixture bindings
  - Python snapshot
  - MT5 request
  - comparison summary
  - rendered report

## Implementation Constraints

- do not copy-paste `materialize_fpmarkets_v2_runtime_minimum_pack.py`
- generalize to a reusable pack builder or pack-profile abstraction
- the minimum-pack profile and broader-sample profile must reuse the same compare and render chain
- do not change the current public runtime interfaces while implementing the broader-sample profile

## Boundary To Later Work

- `runtime-helper parity` stays separate and later
- `Tier B / Tier C readiness` stays downstream-only
- any later Tier B work must carry a separate readiness label, missing-group summary, and reporting lane
