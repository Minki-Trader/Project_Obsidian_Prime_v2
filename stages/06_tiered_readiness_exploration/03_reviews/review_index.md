# Stage 06 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
4. `../01_inputs/stage06_v2_baseline_seed_local_spec.md`
5. `../01_inputs/stage06_v2_followup_pack_local_spec.md`
6. `../03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
7. `../03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
8. `../03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
9. `../03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
10. `../03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
11. `../03_reviews/stage07_alpha_design_draft_0001.md`
12. `../03_reviews/stage06_close_stage07_open_readout_draft_0001.md`
13. `../../../docs/decisions/2026-04-21_stage06_first_tier_b_charter_adopted.md`
14. `../../../docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
15. `../../../docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
16. `../../../docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
17. `../../../docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
18. `../../../docs/policies/tiered_readiness_exploration.md`
19. `../03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
20. `../../../docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
21. `../../05_exploration_kernel_freeze/04_selected/selection_status.md`
22. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
23. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
24. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
25. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `Stage 06 is now active, Stage 05 is closed, the strict Tier A runtime rule remains the only current runtime rule, the first deterministic Tier B or Tier C boundary plus the first reporting interface are fixed, the first scorecard is materialized, the first v2-native baseline seed plus Tier B offline evaluation report exist on separate Tier A and Tier B reporting lanes, and an additive follow-up pack now materializes separate calibration fit, coarse control sensitivity, robustness, placeholder-weight verdict, and Stage 07 draft notes without reflecting an official stage transition`
- do not confuse with regular line: `Stage 06 is exploration-only work and does not imply operating promotion`

## Closed Branches

- the full foundation path through `05_exploration_kernel_freeze` is now closed
- the first downstream exploration boundary is frozen on `broader_0002 + helper_0001 + broader_0003`
- `Tier A / Tier B / Tier C` readiness already has a downstream policy boundary and now has an active stage home
- the first exact Tier B eligibility rule and the first reporting-boundary interface are now fixed for Stage 06
- the first Stage 06 row-level scorecard summary and review report are now materialized on the fixed readiness boundary
- the first Stage 06 offline-only Tier B charter remains accepted, but its baseline-family reuse hypothesis is now superseded by a first `Tier A`-trained v2-native baseline seed with separate `tier_b_exploration` reporting
- the first Stage 06 `Tier B offline evaluation report` now exists and carries separate `validation`, `holdout`, and `calibration read` summaries without claiming runtime-family or promotion meaning
- the first separate Stage 06 `Tier B calibration fit` now exists and shows that a `tier_b_exploration` temperature fit improves the Tier B holdout probabilistic read over both the raw read and the `strict_tier_a` temperature reuse candidate
- the first coarse Stage 06 `control sensitivity read` now exists and shows sparse positive Tier B proxy slices only on low-participation settings while the strict Tier A holdout slice stays non-positive on the same coarse grid
- the first Stage 06 `robustness` and `placeholder-weight verdict` reads now exist and keep the dominant Tier B holdout pattern concentrated in `g4_leader_equity|g5_breadth_extension` while the coarse weight-tilt scenarios stay narrow enough for offline screening only
- the first `Stage 07 alpha design draft` and `Stage 06 close / Stage 07 open readout draft` now exist as draft-only documents and do not change the active-stage truth by themselves
- `B-mixed-partial` now remains vocabulary only and is not an eligible first-boundary rule

## Open Questions

- should the new additive follow-up pack be reflected into the official Stage 06 read and any later `Stage 06 close / Stage 07 open` sync?
- does the placeholder monthly-weight caveat still require a real-weight rerun before any later simulated execution or MT5-path expansion even though the coarse offline tilt scenarios stayed narrow?
