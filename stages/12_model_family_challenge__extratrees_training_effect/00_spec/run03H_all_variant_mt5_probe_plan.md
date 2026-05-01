# run03H All-Variant MT5 Probe Plan

## Scope

- stage: `12_model_family_challenge__extratrees_training_effect`
- package_run: `run03H_et_batch20_all_variant_tier_balance_mt5_v1`
- source structural scout: `run03G_et_variant_stability_probe_v1`
- variants: all 20 RUN03D variants
- claim boundary: `runtime_probe_only`

## Intent

Run MT5 for every structural-scout variant without shortlist reduction. The effect is that Stage 12 can read the full ExtraTrees variant surface in Tier A, Tier B fallback-only, and routed actual total views.

## Stop Conditions

- source variant file missing
- ONNX parity failure
- MT5 terminal or Strategy Tester output blocked
