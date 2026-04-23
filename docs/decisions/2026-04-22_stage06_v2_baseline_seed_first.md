# Decision Memo

## Decision Summary

- `decision_id`: `2026-04-22_stage06_v2_baseline_seed_first`
- `reviewed_on`: `2026-04-22`
- `owner`: `codex + user`
- `decision`: `replace the current Stage 06 baseline-family reuse hypothesis (기준선 계열 재사용 가설) with legacy non-inheritance (레거시 비계승) plus a first v2-native baseline seed (첫 v2 고유 기준선 시드) trained on Tier A only (Tier A 전용 학습), then materialize the first Tier B offline evaluation report (Tier B 오프라인 평가 보고서) with separate Tier A and Tier B reporting without changing the current strict Tier A runtime rule (실행 규칙)`

## What Was Decided

- adopted:
  - treat legacy `model (모델)`, `bundle (번들)`, `threshold (임계값)`, and `calibration (보정)` artifacts as `prior evidence only (선행 근거 전용)` rather than reusable Stage 06 defaults
  - add `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_baseline_seed_local_spec.md` as the first Stage 06 `local spec (로컬 규격)` for label, split, and evaluation rules
  - fit the first `3-class Gaussian Naive Bayes (3분류 가우시안 나이브 베이즈)` seed on `34695` `Tier A train (Tier A 학습)` rows only
  - fix the first label thresholds to `q33=-0.00035087247936272335` and `q67=0.0004049556640609367`
  - materialize the first Stage 06 `v2-native baseline seed artifact family (v2 고유 기준선 시드 산출물 계열)` under `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/`
  - materialize the first Stage 06 `Tier B offline evaluation report (Tier B 오프라인 평가 보고서)` under `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`
  - keep `strict_tier_a (엄격 Tier A)` and `tier_b_exploration (Tier B 탐색)` separated across `validation (검증)` and `holdout (보류 평가)` reads while leaving mixed aggregates `info-only (정보용)` only
  - record the first `calibration read (보정 판독)` without fitting a separate `calibration model (보정 모델)`
- not adopted:
  - any legacy artifact reuse as the active Stage 06 baseline family
  - any `threshold sweep (임계값 스윕)` or `calibration fit (보정 적합)` in this pass
  - any `reduced-risk runtime family (축소위험 런타임 계열)`
  - any `simulated execution (가상 실행)`, `MT5 path (MT5 경로)`, or `operating promotion (운영 승격)`
  - any global `contract (계약)` change under `docs/contracts/**`

## Materialized Read

- `validation (검증)`:
  - `strict_tier_a`: `row_count=10618`, `log_loss=3.199141`, `macro_f1=0.383431`, `balanced_accuracy=0.418289`, `multiclass_brier_score=0.919930`
  - `tier_b_exploration`: `row_count=15866`, `log_loss=2.433661`, `macro_f1=0.346341`, `balanced_accuracy=0.388578`, `multiclass_brier_score=0.763493`
- `holdout (보류 평가)`:
  - `strict_tier_a`: `row_count=10144`, `log_loss=2.952236`, `macro_f1=0.381442`, `balanced_accuracy=0.416943`, `multiclass_brier_score=0.866039`
  - `tier_b_exploration`: `row_count=17978`, `log_loss=1.963620`, `macro_f1=0.336437`, `balanced_accuracy=0.369290`, `multiclass_brier_score=0.660165`
- `calibration read (보정 판독)`:
  - `validation/tier_b_exploration`: `ece=0.349659`
  - `holdout/tier_b_exploration`: `ece=0.296914`

## Why

- the repo has no materialized v2-native model family yet, so continuing to describe baseline-family reuse as current truth would blur `planning scaffold (계획 비계)` with `materialized evidence (물질화 근거)`
- `Tier B (부분 준비)` rows are absent from `features.parquet (특성 파케이)`, so the narrowest workable v2-only path is to rebuild the same parser-bound frame under the current dataset identity and pair it with the materialized readiness labels
- a first v2-native seed plus a separated report answers the next Stage 06 question more honestly than inheriting legacy artifacts that the reboot policy never promoted
- keeping this pass `offline-only (오프라인 전용)` preserves the strict Tier A boundary while still giving later threshold or calibration work a durable evidence base

## What Remains Open

- the first separate `threshold read (임계값 판독)` or `calibration fit (보정 적합)` follow-up for the v2-native baseline seed family
- whether the placeholder monthly-weight caveat still forces a real-weight rerun before any later `simulated execution (가상 실행)` or `MT5-path expansion (MT5 경로 확장)`
- whether a later Stage 06 pass should keep the same `Gaussian Naive Bayes (가우시안 나이브 베이즈)` seed family or open a different v2-native model family after the first threshold or calibration follow-up

## Evidence Used

- `stages/06_tiered_readiness_exploration/01_inputs/stage06_v2_baseline_seed_local_spec.md`
- `foundation/pipelines/materialize_fpmarkets_v2_stage06_v2_baseline_seed.py`
- `tests/test_materialize_fpmarkets_v2_stage06_v2_baseline_seed.py`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_seed_manifest_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_evaluation_summary_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/02_runs/tier_b_offline_eval_0001/baseline_calibration_read_fpmarkets_v2_tier_b_offline_eval_0001.json`
- `stages/06_tiered_readiness_exploration/03_reviews/report_fpmarkets_v2_tier_b_offline_evaluation_0001.md`

## Operational Meaning

- `active_stage changed?`: `no`
- `current strict Tier A runtime rule changed?`: `no`
- `first v2-native baseline seed materialized?`: `yes`
- `first Tier B offline evaluation report materialized?`: `yes`
- `first calibration read materialized?`: `yes`
- `threshold sweep materialized?`: `no`
- `reduced-risk runtime family materialized?`: `no`
- `operating promotion claimed?`: `no`
- `artifact_registry.csv update needed?`: `yes and completed in the same pass because five new durable Stage 06 artifact identities now exist`
- `workspace_state update needed?`: `yes and completed in the same pass so the active Stage 06 read no longer treats baseline-family reuse as the current working truth`
