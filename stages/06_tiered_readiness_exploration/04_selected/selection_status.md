# Selection Status

## Current Read

- current incumbent: `none, by policy`
- current challenger: `none, by policy`
- current read: `Stage 06 remains active because Stage 05 already froze the first downstream exploration boundary clearly enough on the combined broader_0002 + helper_0001 + broader_0003 evidence family, the first deterministic Tier B or Tier C boundary remains fixed, and the first materialized Stage 06 scorecard now confirms shared-window tier counts of tier_a=56988, tier_b=88303, tier_c=116053 plus practical-window tier counts of tier_a=55457, tier_b=86192, tier_c=113352 without changing the current strict Tier A runtime rule`
- scoreboard used: `scorecard_fpmarkets_v2_tiered_readiness_0001`

## Promotion Gates

- any Tier B or Tier C work must stay separate from the current strict Tier A runtime rule and from operating promotion
- every Stage 06 artifact that touches reduced-risk behavior must record `readiness_tier`, `missing_groups`, `missing_symbols`, and `reporting_lane`
- `workspace_state.yaml`, `current_working_state.md`, and the active Stage 06 read must stay aligned on the same active-stage boundary

## Scoreboards

- structural_scout: `n/a`
- regular_risk_execution: `n/a`
- parity / special scoreboard: `Stage 06 active`

## Headline

- return_pct: `n/a`
- profit_factor: `n/a`
- trade_count: `n/a`
- max_dd_pct: `n/a`

## Risk

- biggest current risk: `blurring future Tier B or Tier C exploration with the current strict Tier A line or with operating promotion`
- state fragmentation risk: `high if the active Stage 06 read drifts away from the closed Stage 05 handoff`
- reduced-risk overconfidence risk: `high if partial-context rows are treated as contract-equivalent instead of as separately labeled exploration-only inputs`
- current v2 operating risk metrics: `n/a`

## Diagnostics

- Stage 05 kernel-freeze closure received: `yes`
- strict Tier A runtime rule changed: `no`
- Tier B or Tier C exploration stage opened: `yes`
- active Stage 06 docs materialized: `yes`
- Tier B eligibility boundary materialized: `yes`
- Tier-specific reporting boundary materialized: `yes`
- first scorecard materialized: `yes`
- first scorecard reviewed: `yes`
- reduced-risk runtime family materialized: `no`
- model family choice: `open by decision, not by omission`
- operating promotion active: `no`
- placeholder weights caveat: `still open`

## Execution

- active_stage: `06_tiered_readiness_exploration`
- carry-forward Stage 05 evidence linked: `yes`
- stage status: `open`

## Decision

- keep_or_replace: `keep strict Tier A runtime rule and open separate exploration-only mode`
- promoted / kept / closed: `Stage 06 open`
- next required evidence: `either write the first Tier B reduced-risk experiment charter or record an explicit evidence decision that additional helper-lane or broader-lane support is still required before experimentation`

## Follow-Up Bias

- continue: `reuse the closed Stage 05 broader_0002 + helper_0001 + broader_0003 family as fixed foundation evidence and keep any Stage 06 work additive`
- do_not_reopen_without_new_hypothesis: `Stage 05, runtime-helper parity, or broader-sample parity should not be reopened by implication while Stage 06 is still defining its own boundary`
- next best question: `does scorecard_0001 justify a first Tier B reduced-risk charter now, or does the evidence still say to gather more helper-lane or broader-lane support first?`
- downstream note: `there is still no promoted operating line; Stage 06 is an exploration-only stage, and B-mixed-partial remains vocabulary only in the first boundary`

## Report Refs

- `../00_spec/stage_brief.md`
- `../01_inputs/input_refs.md`
- `../03_reviews/review_index.md`
- `../03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
- `../../../docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
- `../../../docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `../../05_exploration_kernel_freeze/04_selected/selection_status.md`
- `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
- `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
- `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
- `../../../docs/context/current_working_state.md`
