---
name: obsidian-run-evidence-system
description: Manage Project Obsidian Prime v2 run evidence across KPI measurement, run result identity, and lane-aware judgment. Use for run creation, run closeout, KPI reports, result summaries, stage run reviews, run registry updates, or deciding whether a run is positive, negative, inconclusive, or invalid.
---

# Obsidian Run Evidence System

Use this skill when a task creates, reviews, closes, summarizes, or registers run (`실행`) evidence.

## Must Read

- `docs/policies/kpi_measurement_standard.md`
- `docs/policies/run_result_management.md`
- `docs/policies/result_judgment_policy.md`
- `docs/registers/run_registry.csv`
- `docs/policies/exploration_mandate.md` when the run is exploration-sensitive
- `docs/policies/promotion_policy.md` when promotion is possible
- `docs/policies/tiered_readiness_exploration.md` when Tier A/B/C readiness is involved

## Required Output

- `measurement_scope`: which KPI (`key performance indicator`, 핵심 성과 지표) layers are required
- `management_state`: run folder (`실행 폴더`), manifest, KPI record, summary, and registry state
- `judgment_class`: `positive`, `negative`, `inconclusive`, or `invalid`
- `scoreboard`: `structural_scout`, `regular_risk_execution`, `wfo_oos`, `runtime_parity`, or `diagnostic_special`
- `parity_level`: `P0_unverified`, `P1_dataset_feature_aligned`, `P2_model_input_parity_closed`, `P3_runtime_shadow_parity_sampled`, or `P4_full_runtime_parity_closed`
- `wfo_status`: `not_applicable`, `planned`, `partial`, `complete`, or `exception`
- `registry_update_required`: `yes` or `no`
- `negative_memory_required`: `yes` or `no`
- `hard_gate_applicable`: `yes` only for `operating_promotion` or `runtime_authority`
- `evidence_boundary`: `scout-only`, `candidate`, `probe`, `reviewed`, `selected`, `operating_promotion`, or `runtime_authority`

## Guardrails

- Early scout runs may use partial evidence if the missing layers and evidence boundary are labeled.
- Do not close a reviewed or selected run without machine-readable KPI evidence or explicit `n/a` reasons.
- Do not confuse `negative` (`부정`) with `invalid` (`무효`).
- Do not treat `inconclusive` (`불충분`) as either success or failure.
- Do not claim `operating_promotion` (`운영 승격`) from `structural_scout` (`구조 탐색 점수판`) or `promotion_candidate` (`승격 후보`) evidence alone.
- Do not claim `runtime_authority` (`런타임 권위`) from `runtime_probe` (`런타임 탐침`) evidence.
- Do not blend Tier B/C research KPI with Tier A promotion or runtime KPI.
- Do not claim `P4_full_runtime_parity_closed` from lower-level parity evidence.
- Keep large artifacts outside Git only when their identity, path, and hash are represented in Git-tracked evidence.

## Closeout Checklist

Before marking a run as reviewed, selected, archived, invalidated, or superseded:

1. Confirm `run_manifest.json` or equivalent identity evidence exists.
2. Confirm `kpi_record.json` or equivalent KPI evidence exists.
3. Confirm `result_summary.md` or equivalent human readout exists.
4. Confirm `docs/registers/run_registry.csv` has or will receive a row.
5. Classify the result as `positive`, `negative`, `inconclusive`, or `invalid`.
6. If the result closes an exploration idea negatively, record salvage value and reopen condition.

Before claiming `operating_promotion` or `runtime_authority`, confirm the relevant hard-gate evidence exists and the claim is backed by a durable decision or closure artifact.
