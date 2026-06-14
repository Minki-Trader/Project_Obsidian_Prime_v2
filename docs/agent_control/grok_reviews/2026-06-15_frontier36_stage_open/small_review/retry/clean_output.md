verdict: accepted
novelty_ok: yes
main_leakage_or_overfit_risk: Train-only multi-metric utility ranking can overfit source choice to in-sample PF/DD/density unless candidate count, scoring weights, and tie-break rules stay fixed and bounded before any read-only validation/OOS read.
must_not_repeat: Do not add single-feature or sequential filter layers onto the F34/F35 scaffold as the primary way to pass DD and density together.
runtime_claim_boundary_ok: yes
