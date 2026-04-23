# Stage 06 Review Index

## Reading Order

1. `../00_spec/stage_brief.md`
2. `../01_inputs/input_refs.md`
3. `../../../docs/decisions/2026-04-22_stage06_close_and_stage07_open.md`
4. `../../../docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md`
5. `../01_inputs/stage06_v2_baseline_seed_local_spec.md`
6. `../01_inputs/stage06_v2_followup_pack_local_spec.md`
7. `../01_inputs/stage06_tier_b_safe_feature_schema_draft_0001.md`
8. `../01_inputs/stage06_tier_b_reduced_context_local_spec.md`
9. `../03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
10. `../03_reviews/report_fpmarkets_v2_tier_b_reduced_context_0001.md`
11. `../03_reviews/report_fpmarkets_v2_tier_b_calibration_fit_0001.md`
12. `../03_reviews/report_fpmarkets_v2_tier_b_control_sensitivity_0001.md`
13. `../03_reviews/report_fpmarkets_v2_tier_b_robustness_0001.md`
14. `../03_reviews/report_fpmarkets_v2_tier_b_weight_verdict_0001.md`
15. `../03_reviews/stage07_alpha_design_draft_0001.md`
16. `../03_reviews/stage06_close_stage07_open_readout_draft_0001.md`
17. `../03_reviews/note_fpmarkets_v2_tier_b_reduced_context_model_anchor_0001.md`
18. `../../../docs/decisions/2026-04-21_stage06_first_tier_b_charter_adopted.md`
19. `../../../docs/adr/0003_tier_b_reduced_risk_experiment_charter.md`
20. `../../../docs/decisions/2026-04-21_stage06_first_scorecard_materialized.md`
21. `../../../docs/decisions/2026-04-20_stage06_first_readiness_boundary.md`
22. `../../../docs/decisions/2026-04-20_stage05_close_and_stage06_open.md`
23. `../../../docs/policies/tiered_readiness_exploration.md`
24. `../03_reviews/report_fpmarkets_v2_tiered_readiness_0001.md`
25. `../../../docs/decisions/2026-04-18_tiered_readiness_exploration_boundary.md`
26. `../../05_exploration_kernel_freeze/04_selected/selection_status.md`
27. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0002.md`
28. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_helper_parity_0001.md`
29. `../../05_exploration_kernel_freeze/03_reviews/report_fpmarkets_v2_runtime_broader_parity_0003.md`
30. `../04_selected/selection_status.md`

## Latest Regular Read

- current decision: `no regular alpha line in v2 yet`
- current incumbent: `none`
- current challenger: `none`

## Latest Structural / Diagnostic Read

- structural read: `Stage 06 is now closed, Stage 07 is now active, the strict Tier A runtime rule remains the only current runtime rule, the first deterministic Tier B or Tier C boundary plus the first reporting interface stayed fixed, the first scorecard is materialized, the first v2-native baseline seed plus Tier B offline evaluation report exist on separate Tier A and Tier B reporting lanes, the additive follow-up pack materializes separate calibration fit, coarse control sensitivity, robustness, placeholder-weight verdict, and Stage 07 draft notes, and the first shared Tier B reduced-context model materializes on the keep42 feature surface with separate lane reporting and info-only subtype tags`
- draft anchor read: `a draft-only Stage 06 anchor note now records the current preference for one shared Tier B reduced-context model plus subtype tags, without opening Stage 07 or changing official state by itself`
- draft schema read: `a draft-only Tier B-safe feature schema now fixes the first shared reduced-context active set to keep=42, conditional=6, and drop=10 and now serves as the planning scaffold that backed the first materialized reduced-context model pass`
- reduced-context read: `the first shared reduced-context model improves Tier B holdout log_loss to 1.503578 from the prior full-baseline 1.963620 while keeping all meaning offline-only`
- do not confuse with regular line: `Stage 06 closure hands off to Stage 07 alpha search only and still does not imply operating promotion`

## Closed Branches

- the full foundation path through `05_exploration_kernel_freeze` is now closed
- the first downstream exploration boundary is frozen on `broader_0002 + helper_0001 + broader_0003`
- `Tier A / Tier B / Tier C` readiness already has a downstream policy boundary and now has a closed stage home
- the first exact Tier B eligibility rule and the first reporting-boundary interface are now fixed for Stage 06
- the first Stage 06 row-level scorecard summary and review report are now materialized on the fixed readiness boundary
- the first Stage 06 offline-only Tier B charter remains accepted, but its baseline-family reuse hypothesis is now superseded by a first `Tier A`-trained v2-native baseline seed with separate `tier_b_exploration` reporting
- the first Stage 06 `Tier B offline evaluation report` now exists and carries separate `validation`, `holdout`, and `calibration read` summaries without claiming runtime-family or promotion meaning
- the first separate Stage 06 `Tier B calibration fit` now exists and shows that a `tier_b_exploration` temperature fit improves the Tier B holdout probabilistic read over both the raw read and the `strict_tier_a` temperature reuse candidate
- the first coarse Stage 06 `control sensitivity read` now exists and shows sparse positive Tier B proxy slices only on low-participation settings while the strict Tier A holdout slice stays non-positive on the same coarse grid
- the first Stage 06 `robustness` and `placeholder-weight verdict` reads now exist and keep the dominant Tier B holdout pattern concentrated in `g4_leader_equity|g5_breadth_extension` while the coarse weight-tilt scenarios stay narrow enough for offline screening only
- the first `Stage 07 alpha design draft` and `Stage 06 close / Stage 07 open readout draft` now exist as draft-only documents and do not change official stage truth by themselves
- a draft-only `Tier B reduced-context modeling anchor` now exists so later sessions can resume from one shared `Tier B` reduced-context model plus subtype tags instead of reopening the same planning debate from scratch
- a draft-only `Tier B-safe feature schema` now exists so the first shared reduced-context model can start from one fixed keep/drop surface instead of re-litigating feature eligibility from chat memory
- the first shared `Tier B reduced-context model` now exists and beats the current full-feature baseline on both Tier A and Tier B validation and holdout probabilistic reads
- the official decision reflection now closes Stage 06 and opens Stage 07 without changing the current strict Tier A runtime rule or authorizing any MT5-path work
- `B-mixed-partial` now remains vocabulary only and is not an eligible first-boundary rule

## Downstream Handoff Questions

- the new additive follow-up pack and reduced-context model are now reflected into the official Stage 06 close and Stage 07 open sync
- does the placeholder monthly-weight caveat still require a real-weight rerun before any later simulated execution or MT5-path expansion even though the coarse offline tilt scenarios stayed narrow?
- the current shared reduced-context baseline is now enough for an official separate Stage 07 Tier B exploration target, while an optional `macro-aware` variant remains a later question rather than an opening requirement
- should a later stage keep one shared `Tier B reduced-context model` with `b_eq_dark / b_macro_late / b_residual_sparse` tags before considering any two-way or three-way Tier B model split?
