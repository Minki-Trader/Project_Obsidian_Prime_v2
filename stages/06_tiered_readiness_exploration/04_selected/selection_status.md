# Selection Status

## Current Read

- current incumbent: `none, by policy`
- current challenger: `none, by policy`
- current read: `Stage 06 remains active because Stage 05 already froze the first downstream exploration boundary clearly enough on the combined broader_0002 + helper_0001 + broader_0003 evidence family, the first deterministic Tier B or Tier C boundary remains fixed, the first materialized Stage 06 scorecard still confirms shared-window tier counts of tier_a=56988, tier_b=88303, tier_c=116053 plus practical-window tier counts of tier_a=55457, tier_b=86192, tier_c=113352, and the first v2-native baseline seed plus Tier B offline evaluation report now materialize under tier_b_offline_eval_0001 with Tier A-only fitting, separate Tier A and Tier B reporting, and no change to the current strict Tier A runtime rule`
- scoreboard used: `scorecard_fpmarkets_v2_tiered_readiness_0001`

## Promotion Gates

- any Tier B or Tier C work must stay separate from the current strict Tier A runtime rule and from operating promotion
- every Stage 06 artifact that touches reduced-risk behavior must record `readiness_tier`, `missing_groups`, `missing_symbols`, and `reporting_lane`
- the first Tier B charter remains offline-only and does not authorize simulated execution, MT5-path expansion, or operating promotion
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

- biggest current risk: `blurring the adopted offline-only Tier B charter with the current strict Tier A line or with operating promotion`
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
- first Tier B charter adopted: `yes`
- first v2-native baseline seed materialized: `yes`
- first Tier B offline evaluation report materialized: `yes`
- first calibration read materialized: `yes`
- reduced-risk runtime family materialized: `no`
- model family choice: `first v2-native Gaussian Naive Bayes seed trained on Tier A only with separate Tier A and Tier B reporting`
- operating promotion active: `no`
- placeholder weights caveat: `allowed for offline-only charter only; not valid for promotion, simulated execution, or MT5-path expansion`

## Execution

- active_stage: `06_tiered_readiness_exploration`
- carry-forward Stage 05 evidence linked: `yes`
- stage status: `open`

## Decision

- keep_or_replace: `keep strict Tier A runtime rule, keep first Tier B work offline-only, and keep the first v2-native baseline seed on a separate exploration-only lane`
- promoted / kept / closed: `Stage 06 open`
- next required evidence: `materialize the first separate threshold read or the first calibration-fit follow-up for the v2-native baseline seed on the separate tier_b_exploration lane`

## Follow-Up Bias

- continue: `reuse the closed Stage 05 broader_0002 + helper_0001 + broader_0003 family as fixed foundation evidence and keep any Stage 06 work additive`
- do_not_reopen_without_new_hypothesis: `Stage 05, runtime-helper parity, or broader-sample parity should not be reopened by implication while Stage 06 is still defining its own boundary`
- next best question: `what is the narrowest first follow-up after the v2-native baseline seed report: a separate threshold read or a calibration fit that still avoids simulated execution and MT5-path work?`
- downstream note: `there is still no promoted operating line; Stage 06 is an exploration-only stage, the first Tier B charter is offline-only, and B-mixed-partial remains vocabulary only in the first boundary`

## Execution Contract

- next_task_id: `s06_first_v2_baseline_seed_followup`
- goal: `materialize the first separate threshold read or calibration-fit follow-up for the v2-native baseline seed on the separate tier_b_exploration lane without changing the current strict Tier A runtime rule`
- allowed_paths: `stages/06_tiered_readiness_exploration/**`, `foundation/pipelines/**`, `foundation/reports/**`, `tests/**`, and `docs/registers/artifact_registry.csv` only when a new durable artifact identity appears
- do_not_touch: `docs/contracts/**`, the current strict Tier A runtime rule, simulated execution, MT5-path expansion, and any claim that Stage 05 already closed separate runtime-helper parity or broader-sample parity
- expected_artifacts: `the first separate threshold read` or `the first separate calibration-fit follow-up report` for the v2-native baseline seed family, plus same-pass registry sync when a new durable identity is created
- verification_minimum: `the narrowest sufficient local verification for the touched Stage 06 surface`, `artifact-registry sync check when a new durable artifact appears`, and `claim-language review against the offline-only Tier B charter`
- real_env_required: `no by default; yes only if the touched change crosses into MT5 execution, tester orchestration, runtime parity flow, file import/export boundaries, or another environment-dependent path`
- publish_target: `branch_only by default; move toward main only on explicit user ask or an approved task packet that names main`
- stop_conditions: `active stage mismatch`, `scope expansion beyond the first threshold-or-calibration follow-up`, `attempt to blur Tier B exploration with operating promotion`, or `new durable artifact identity without same-pass registry sync`
- done_definition: `the first threshold-or-calibration follow-up exists in the Stage 06 home, keeps the strict Tier A runtime rule unchanged, preserves the v2-native baseline seed reporting boundary, and records any new durable identity in the registry`

## Report Refs

- `../00_spec/stage_brief.md`
- `../01_inputs/input_refs.md`
- `../03_reviews/review_index.md`
- `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
- `../../../docs/decisions/2026-04-21_stage06_first_tier_b_charter_adopted.md`
- `../01_inputs/stage06_v2_baseline_seed_local_spec.md`
- `../../../docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
- `../03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
- `../03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
- `../../../docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
- `../../../docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
- `../../05_exploration_kernel_freeze/04_selected/selection_status.md`
- `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
- `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
- `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
- `../../../docs/context/current_working_state.md`
