# Selection Status

## Current Read

- current incumbent: `none, by policy`
- current challenger: `none, by policy`
- current read: `Stage 07 is now active because Stage 06 already made the first exploration-only readiness family explicit through the deterministic readiness boundary, the first scorecard family, the first v2-native baseline seed, the additive Tier B follow-up pack, and the first shared keep42 reduced-context model, so bounded alpha-search work can now move downstream without changing the current strict Tier A runtime rule`
- inherited starting point: `Tier A main lane on the full contract surface plus a separate Tier B offline-only lane on the shared keep42 reduced-context surface`

## Promotion Gates

- Stage 07 alpha search must stay separate from `operating promotion (운영 승격)`
- the current strict `Tier A` runtime rule remains unchanged until a later explicit decision says otherwise
- the separate `Tier B` lane remains `offline-only (오프라인 전용)` and does not authorize `simulated execution (가상 실행)` or `MT5 path (MT5 경로)` work
- all Stage 07 artifacts that touch Tier B must keep separate `reporting_lane`, `readiness_tier`, `missing_groups`, and `missing_symbols` fields

## Scoreboards

- structural_scout: `n/a`
- regular_risk_execution: `n/a`
- parity / special scoreboard: `Stage 07 active`

## Headline

- return_pct: `n/a`
- profit_factor: `n/a`
- trade_count: `n/a`
- max_dd_pct: `n/a`

## Risk

- biggest current risk: `blurring Stage 07 alpha-search permission with MT5 readiness, simulated execution, or operating promotion`
- state fragmentation risk: `high if Stage 07 opening is not kept aligned across workspace_state, current_working_state, and the active selection read`
- Tier B overreach risk: `high if the separate Tier B lane is treated as contract-equivalent to the strict Tier A line`
- current v2 operating risk metrics: `n/a`

## Diagnostics

- Stage 06 readiness-family closure received: `yes`
- Stage 07 alpha-search stage opened: `yes`
- strict Tier A runtime rule changed: `no`
- separate Tier B alpha-search lane opened: `yes`
- separate Tier B lane still offline-only: `yes`
- simulated execution authorized: `no`
- MT5-path expansion authorized: `no`
- operating promotion active: `no`

## Execution

- active_stage: `07_alpha_search`
- carry-forward Stage 06 evidence linked: `yes`
- stage status: `open`

## Decision

- keep_or_replace: `keep the strict Tier A runtime rule, open Stage 07 alpha search, and keep the separate Tier B lane bounded to offline-only reduced-context exploration`
- promoted / kept / closed: `Stage 07 open`
- next required evidence: `materialize the first bounded Stage 07 alpha-search pack with separate Tier A and Tier B reporting lanes`

## Follow-Up Bias

- continue: `start Stage 07 from the shared keep42 reduced-context Tier B lane rather than reopening the baseline-family or keep/drop debate from scratch`
- do_not_reopen_without_new_hypothesis: `Stage 06 readiness-boundary work, the strict Tier A runtime rule, and the offline-only Tier B separation should not be blurred or reopened by implication`
- next best question: `what is the narrowest first alpha-search pack that can test both the Tier A main lane and the separate Tier B lane without crossing into runtime meaning?`
- downstream note: `an optional macro-aware Tier B variant may still be useful later, but it is not a precondition for the current Stage 07 opening`

## Execution Contract

- next_task_id: `s07_first_alpha_search_pack`
- goal: `materialize the first bounded Stage 07 alpha-search pack across the Tier A main lane and the separate Tier B offline-only lane while keeping the current strict Tier A runtime rule unchanged`
- allowed_paths: `stages/07_alpha_search/**`, `stages/06_tiered_readiness_exploration/**`, `foundation/pipelines/**`, `foundation/reports/**`, `tests/**`, and `docs/registers/artifact_registry.csv` only when a new durable artifact identity appears`
- do_not_touch: `docs/contracts/**`, the current strict Tier A runtime rule, simulated execution, MT5-path expansion, and any operating-promotion claim
- expected_artifacts: `the first Stage 07 alpha-search local spec or packet`, `the first Stage 07 alpha-search summary/report family`, and same-pass registry sync when a new durable artifact identity appears
- verification_minimum: `the narrowest sufficient local verification for the touched alpha-search surface`, `artifact-registry sync when new durable identity appears`, and `claim-language review against the offline-only Tier B boundary`
- real_env_required: `no by default; yes only if the touched change crosses into MT5 execution, tester orchestration, runtime parity flow, file import/export boundaries, or another environment-dependent path`
- publish_target: `branch_only by default; move toward main only on explicit user ask or an approved task packet that names main`
- stop_conditions: `active stage mismatch`, `scope drift into MT5 or simulated execution`, `attempt to treat Tier B as contract-equivalent to Tier A`, or `new durable artifact identity without same-pass registry sync`
- done_definition: `the first Stage 07 alpha-search pack exists, keeps Tier A and Tier B separated, preserves the current strict Tier A runtime rule, and does not imply operating promotion`

## Report Refs

- `../00_spec/stage_brief.md`
- `../01_inputs/input_refs.md`
- `../03_reviews/review_index.md`
- `../../../docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
- `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
- `../../06_tiered_readiness_exploration/04_selected/selection_status.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
- `../../06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`
- `../../../docs/context/current_working_state.md`
