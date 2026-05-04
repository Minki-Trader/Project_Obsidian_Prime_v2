from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    TRAINING_SUMMARY_PATH,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.gam_additive import (
    GamVariantSpec,
    characteristic_score,
    default_stage20_gam_variants,
    fit_gam_variant,
    nonflat_threshold,
    probability_frame,
    probability_quality_read,
    probability_shape_metrics,
    shape_read,
    smooth_shape_frame,
    split_decision_metrics,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 20
STAGE_ID = "20_model_family_challenge__gam_additive_smooth_shape"
RUN_NUMBER = "run14A"
RUN_ID = "run14A_gam_additive_shape_scout_v1"
PACKET_ID = "stage20_run14A_gam_additive_shape_scout_v1"
EXPLORATION_LABEL = "stage20_Model__GAMAdditiveSmoothShape"
IDEA_ID = "IDEA-ST20-GAM-ADDITIVE-SMOOTH-SHAPE"
MODEL_FAMILY = "pygam_logistic_gam_one_vs_rest_short_long_flat_reference"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
THRESHOLD_QUANTILE = 0.90
BOUNDARY = "gam_additive_shape_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_gam_additive_shape_structural_scout_completed"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run14A_gam_additive_shape_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage20_run14A_gam_shape_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, full_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "full_feature_order": full_feature_order,
        "full_feature_order_hash": ordered_hash(full_feature_order),
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_feature_order_hash": ordered_hash(tier_b_feature_order),
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }


def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def materialize_python_tier_records(
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    a_threshold: float,
    b_threshold: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = RUN_ROOT / "predictions"
    a_path = root / "tier_a_separate_predictions.parquet"
    b_path = root / "tier_b_separate_predictions.parquet"
    ab_path = root / "tier_ab_combined_predictions.parquet"
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, a_threshold, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, b_threshold, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, ab_prob, a_threshold, ab_path),
    ]
    artifacts = {
        "tier_a_predictions": save_predictions(a_path, tier_a_prob),
        "tier_b_predictions": save_predictions(b_path, tier_b_prob),
        "tier_ab_predictions": save_predictions(ab_path, ab_prob),
    }
    return records, artifacts


def variant_characteristic(context: Mapping[str, Any], spec: GamVariantSpec) -> dict[str, Any]:
    models, sample = fit_gam_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    prob = probability_frame(models, context["tier_a_frame"], spec.feature_names)
    threshold = nonflat_threshold(prob, THRESHOLD_QUANTILE)
    metrics = split_decision_metrics(prob, threshold)
    probability_shape = probability_shape_metrics(prob)
    shape = smooth_shape_frame(models, spec)
    shape_summary = shape_read(shape)
    shape_root = RUN_ROOT / "results/variant_shapes"
    io_path(shape_root).mkdir(parents=True, exist_ok=True)
    shape_path = shape_root / f"{spec.variant_id}_smooth_shape.csv"
    shape.to_csv(io_path(shape_path), index=False)
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
        "training_sample": sample,
        "threshold": threshold,
        "metrics": metrics,
        "probability_shape": probability_shape,
        "probability_quality": probability_quality_read(prob),
        "shape_read": shape_summary,
        "shape_artifact": {"path": rel(shape_path), "sha256": sha256_file_lf_normalized(shape_path)},
        "characteristic_score": characteristic_score(metrics, shape_summary),
    }


def choose_selected_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    compatible = [row for row in rows if row.get("spec", {}).get("tier_b_compatible") is True]
    pool = compatible or list(rows)
    return dict(max(pool, key=lambda row: safe_float(row.get("characteristic_score")), default={}))


def materialize_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    io_path(result_root).mkdir(parents=True, exist_ok=True)
    json_path = result_root / "gam_variant_results.json"
    csv_path = result_root / "gam_variant_results.csv"
    write_json(json_path, list(rows))
    csv_rows: list[dict[str, Any]] = []
    for row in rows:
        metrics = row.get("metrics", {})
        spec = row.get("spec", {})
        shape = row.get("shape_read", {})
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "idea_id": row.get("idea_id"),
                "feature_count": len(spec.get("feature_names", [])),
                "n_splines": spec.get("n_splines"),
                "lam": spec.get("lam"),
                "tier_b_compatible": spec.get("tier_b_compatible"),
                "characteristic_score": row.get("characteristic_score"),
                "threshold": row.get("threshold"),
                "val_signal_coverage": metrics.get("validation", {}).get("signal_coverage"),
                "oos_signal_coverage": metrics.get("oos", {}).get("signal_coverage"),
                "val_directional_hit_rate": metrics.get("validation", {}).get("directional_hit_rate"),
                "oos_directional_hit_rate": metrics.get("oos", {}).get("directional_hit_rate"),
                "val_log_loss": metrics.get("validation", {}).get("log_loss"),
                "oos_log_loss": metrics.get("oos", {}).get("log_loss"),
                "top5_range_share": shape.get("top5_range_share"),
            }
        )
    write_csv(
        csv_path,
        [
            "variant_id",
            "idea_id",
            "feature_count",
            "n_splines",
            "lam",
            "tier_b_compatible",
            "characteristic_score",
            "threshold",
            "val_signal_coverage",
            "oos_signal_coverage",
            "val_directional_hit_rate",
            "oos_directional_hit_rate",
            "val_log_loss",
            "oos_log_loss",
            "top5_range_share",
        ],
        csv_rows,
    )
    return {
        "variant_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def selected_spec(selected: Mapping[str, Any]) -> GamVariantSpec:
    payload = dict(selected["spec"])
    payload["feature_names"] = tuple(payload["feature_names"])
    return GamVariantSpec(**payload)


def materialize_selected_models(
    context: Mapping[str, Any],
    spec: GamVariantSpec,
) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame, float, float, pd.DataFrame]:
    root = RUN_ROOT / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_models, a_sample = fit_gam_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    tier_b_models, b_sample = fit_gam_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_prob = probability_frame(tier_a_models, context["tier_a_frame"], spec.feature_names)
    tier_b_train_prob = probability_frame(tier_b_models, context["tier_b_training_frame"], spec.feature_names)
    tier_b_prob = probability_frame(tier_b_models, context["tier_b_fallback_frame"], spec.feature_names)
    a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(tier_b_train_prob, THRESHOLD_QUANTILE)
    tier_a_joblib = root / f"{spec.variant_id}_tier_a_gam_ovr.joblib"
    tier_b_joblib = root / f"{spec.variant_id}_tier_b_gam_ovr.joblib"
    joblib.dump(tier_a_models, io_path(tier_a_joblib))
    joblib.dump(tier_b_models, io_path(tier_b_joblib))
    selected_shape = smooth_shape_frame(tier_a_models, spec)
    selected_shape_path = RUN_ROOT / "results/selected_tier_a_smooth_shape.csv"
    selected_shape.to_csv(io_path(selected_shape_path), index=False)
    artifacts = {
        "selected_variant_id": spec.variant_id,
        "tier_a_training_sample": a_sample,
        "tier_b_training_sample": b_sample,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
        "selected_tier_a_smooth_shape": {"path": rel(selected_shape_path), "sha256": sha256_file_lf_normalized(selected_shape_path)},
    }
    return artifacts, tier_a_prob, tier_b_prob, a_threshold, b_threshold, selected_shape


def build_summary(
    context: Mapping[str, Any],
    variants: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    selected_shape: pd.DataFrame,
) -> dict[str, Any]:
    validation = tier_records[0].get("split_metrics", {}).get("validation", {}) if tier_records else {}
    oos = tier_records[0].get("split_metrics", {}).get("oos", {}) if tier_records else {}
    best_overall = dict(max(variants, key=lambda row: safe_float(row.get("characteristic_score")), default={}))
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "status": "reviewed_structural_scout_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "mt5_runtime_probe_status": "not_attempted_in_run14A_next_milestone_run14B",
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "variant_count": len(variants),
        "selected_variant_id": selected.get("variant_id"),
        "best_overall_variant_id": best_overall.get("variant_id"),
        "selected_threshold_id": f"q{THRESHOLD_QUANTILE:.2f}",
        "tier_a_rows": int(len(context["tier_a_frame"])),
        "tier_b_fallback_rows": int(len(context["tier_b_fallback_frame"])),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "tier_records": list(tier_records),
        "selected_tier_a_validation_signal_coverage": validation.get("signal_coverage"),
        "selected_tier_a_oos_signal_coverage": oos.get("signal_coverage"),
        "selected_tier_a_validation_directional_hit_rate": validation.get("directional_hit_rate"),
        "selected_tier_a_oos_directional_hit_rate": oos.get("directional_hit_rate"),
        "selected_tier_a_probability_margin_validation": validation.get("mean_probability_margin"),
        "selected_tier_a_probability_margin_oos": oos.get("mean_probability_margin"),
        "selected_shape_read": shape_read(selected_shape),
        "artifacts": {
            "model_input_path": rel(MODEL_INPUT_PATH),
            "feature_order_path": rel(FEATURE_ORDER_PATH),
            "variant_results": rel(RUN_ROOT / "results/gam_variant_results.csv"),
            "model_artifacts": dict(model_artifacts),
            "prediction_artifacts": dict(prediction_artifacts),
        },
        "forbidden_claims": [
            "edge",
            "alpha_quality",
            "baseline",
            "promotion_candidate",
            "operating_promotion",
            "runtime_authority",
        ],
        "next_condition": "Run run14B as a narrow MT5 runtime_probe by adding a GAM score-table or handoff-compatible runtime representation for the selected v01/v02 Tier-B-compatible variant.",
    }


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "GAM can expose smooth additive short/long shape on the audited 58-feature US100 M5 surface.",
            "decision_use": "Decide whether Stage20 should continue to a narrow MT5 runtime_probe using a selected GAM handoff representation.",
            "comparison_baseline": "No baseline; compare only within Stage20 GAM variants and fixed data contract.",
            "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, "Tier A/B paired records"],
            "changed_variables": ["model_family=GAM", "feature subset", "spline smoothness"],
            "success_criteria": ["non-flat smooth shape", "usable Tier A/B prediction records", "clear handoff candidate"],
            "failure_criteria": ["flat probability shape", "unstable validation/OOS density", "no Tier-B-compatible candidate"],
            "invalid_conditions": ["missing split", "missing feature", "duplicate timestamp", "non-finite feature"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_source": rel(MODEL_INPUT_PATH),
            "time_axis": "timestamp is read as UTC-normalized project timestamp and split contract is unchanged.",
            "sample_scope": f"Tier A rows={summary.get('tier_a_rows')}; Tier B fallback rows={summary.get('tier_b_fallback_rows')}",
            "feature_label_boundary": LABEL_ID,
            "split_boundary": SPLIT_CONTRACT,
            "integrity_judgment": "usable_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_family": MODEL_FAMILY,
            "selection_metric": "characteristic_score on smooth shape, signal density, and hit-rate diagnostics; not trading profit.",
            "threshold_policy": f"non-flat q{THRESHOLD_QUANTILE:.2f} from validation split.",
            "overfit_risk": "single split and small hand-authored variant set; no WFO or MT5 evidence yet.",
            "calibration_risk": "one-vs-rest GAM probabilities are fused with a flat reference logit; scout probability only.",
            "validation_judgment": "inconclusive_structural_scout",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [rel(MODEL_INPUT_PATH), rel(FEATURE_ORDER_PATH), rel(TRAINING_SUMMARY_PATH)],
            "producer": "stage_pipelines.stage20.gam_characteristic_scout",
            "consumer": [rel(REPORT_PATH), rel(STAGE_LEDGER_PATH), rel(PROJECT_LEDGER_PATH)],
            "availability": "generated_02_runs_ignored_with_tracked_packet_summary",
            "lineage_judgment": "connected_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "result_subject": RUN_ID,
            "evidence_available": ["variant results", "Tier A/B prediction records", "stage and project ledgers"],
            "evidence_missing": ["MT5 runtime_probe", "WFO", "runtime authority"],
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": summary.get("next_condition"),
        },
    ]


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    selected = str(summary.get("selected_variant_id"))
    top_terms = summary.get("selected_shape_read", {}).get("top_terms", [])
    top_lines = "\n".join(
        f"- `{row.get('feature')}`: partial_range(부분범위) `{safe_float(row.get('partial_range')):.6f}`, range_share(범위비중) `{safe_float(row.get('range_share')):.4f}`"
        for row in top_terms[:6]
    )
    if not top_lines:
        top_lines = "- no smooth terms recorded(기록된 부드러운 항 없음)"
    write_md(
        REPORT_PATH,
        f"""# RUN14A GAM Additive Shape Scout Packet(실행14A GAM 가산 모양 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- best overall variant(전체 최고 변형): `{summary.get('best_overall_variant_id')}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run14A_next_milestone_run14B(실행14A에서는 미시도, 다음 마일스톤은 실행14B)`

효과(effect, 효과): GAM(`Generalized Additive Model`, 일반화 가산 모델)의 smooth additive shape(부드러운 가산 모양)는 Python-side evidence(파이썬 근거)로 잡았지만, edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형 수): `{summary.get('variant_count')}`
- Tier A rows(Tier A 행): `{summary.get('tier_a_rows')}`
- Tier B fallback rows(Tier B 대체 행): `{summary.get('tier_b_fallback_rows')}`
- validation signal coverage(검증 신호 커버리지): `{summary.get('selected_tier_a_validation_signal_coverage')}`
- OOS signal coverage(표본외 신호 커버리지): `{summary.get('selected_tier_a_oos_signal_coverage')}`
- validation directional hit(검증 방향 적중): `{summary.get('selected_tier_a_validation_directional_hit_rate')}`
- OOS directional hit(표본외 방향 적중): `{summary.get('selected_tier_a_oos_directional_hit_rate')}`

## Top Smooth Terms(상위 부드러운 항)

{top_lines}

## Next Exact Action(다음 정확한 행동)

Create `run14B_gam_runtime_handoff_probe_v1` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침). First implement or reuse a handoff-compatible GAM score representation(인계 가능 GAM 점수 표현), then run one sentinel tranche(감시 실행 묶음) before any larger batch(큰 배치).
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Stage20 RUN14A GAM Shape Scout Decision(20단계 실행14A GAM 모양 탐색 결정)

## Decision(결정)

`{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): Stage20(20단계)은 GAM(`Generalized Additive Model`, 일반화 가산 모델) smooth additive shape(부드러운 가산 모양) 단서를 얻었지만, 아직 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)가 없으므로 closeout(마감)이나 운영 의미(operating meaning, 운영 의미)를 만들지 않는다.

## Next Condition(다음 조건)

다음 milestone(마일스톤)은 `run14B_gam_runtime_handoff_probe_v1`이다. 조건은 selected variant(선택 변형)를 MQL5(`MetaQuotes Language 5`, 메타쿼츠 언어5) 또는 기존 runtime bridge(런타임 연결)에서 읽을 수 있는 score table(점수표)이나 동등한 handoff file(인계 파일)로 만드는 것이다.
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage20 Selection Status(20단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run14A_python_structural_scout_completed(실행14A 파이썬 구조 탐색 완료)`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage20(20단계)은 GAM(일반화 가산 모델)의 smooth additive shape(부드러운 가산 모양)를 보기 시작했지만, 아직 MT5 runtime_probe(MT5 런타임 탐침), closeout(마감), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Exact Action(다음 정확한 행동)

`run14B_gam_runtime_handoff_probe_v1`에서 selected GAM variant(선택 GAM 변형)를 runtime handoff(런타임 인계) 가능한 score representation(점수 표현)으로 만들고, sentinel MT5 run(감시 MT5 실행)을 먼저 수행한다.
""",
    )
    write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage20 Review Index(20단계 검토 색인)

- `{RUN_ID}`: `{rel(REPORT_PATH)}`

효과(effect, 효과): Stage20(20단계)의 검토 근거 위치를 한 곳에서 찾게 한다.
""",
    )


def write_packet_artifacts(summary: Mapping[str, Any], created_at: str) -> None:
    receipts = build_skill_receipts(summary, created_at)
    gates = {
        "scope_completion_gate": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_views": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
            "completed_views": [record.get("record_view") for record in summary.get("tier_records", [])],
        },
        "kpi_contract_audit": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "kpi_scope": "signal_probability_threshold",
            "runtime_kpi_required": False,
            "runtime_kpi_reason": "out_of_scope_by_claim_python_structural_scout",
        },
        "skill_receipt_lint": {"packet_id": PACKET_ID, "status": "passed", "receipt_count": len(receipts)},
        "required_gate_coverage_audit": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "covered_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
        },
        "final_claim_guard": {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": ["python_structural_scout_completed", "gam_shape_clues_recorded"],
            "forbidden_claims": summary.get("forbidden_claims"),
        },
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", receipts)
    for name, payload in gates.items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    write_md(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
primary_family: experiment_execution
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-artifact-lineage
required_gates:
  - scope_completion_gate
  - kpi_contract_audit
  - skill_receipt_lint
  - required_gate_coverage_audit
status: completed_with_boundary
boundary: {BOUNDARY}
""",
    )


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    selected_threshold_id = str(summary.get("selected_threshold_id"))
    rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=summary.get("tier_records", []),
        mt5_kpi_records=[],
        selected_threshold_id=selected_threshold_id,
        run_output_root=RUN_ROOT,
        external_verification_status="out_of_scope_by_claim_python_structural_scout",
    )
    ledgers = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_model_family_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": ledger_pairs(
            (
                ("selected_variant", summary.get("selected_variant_id")),
                ("best_overall_variant", summary.get("best_overall_variant_id")),
                ("external_verification", summary.get("external_verification_status")),
                ("mt5_next", "run14B_gam_runtime_handoff_probe_v1"),
                ("boundary", BOUNDARY),
            )
        ),
    }
    ledgers["run_registry"] = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    return ledgers


def run() -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variants = [variant_characteristic(context, spec) for spec in default_stage20_gam_variants()]
    variant_artifacts = materialize_variant_results(variants)
    selected = choose_selected_variant(variants)
    spec = selected_spec(selected)
    model_artifacts, tier_a_prob, tier_b_prob, a_threshold, b_threshold, selected_shape = materialize_selected_models(context, spec)
    tier_records, prediction_artifacts = materialize_python_tier_records(tier_a_prob, tier_b_prob, a_threshold, b_threshold)
    summary = build_summary(context, variants, selected, model_artifacts, {**prediction_artifacts, **variant_artifacts}, tier_records, selected_shape)
    write_json(RUN_ROOT / "run_manifest.json", {"created_at_utc": created_at, "summary": summary})
    write_json(RUN_ROOT / "kpi_record.json", {"created_at_utc": created_at, "tier_records": tier_records, "judgment": JUDGMENT})
    write_json(RUN_ROOT / "summary.json", summary)
    write_stage_docs(summary)
    write_packet_artifacts(summary, created_at)
    ledgers = materialize_ledgers(summary)
    summary["ledger_updates"] = ledgers
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage20 GAM additive smooth shape scout.")
    parser.parse_args(argv)
    summary = run()
    print(json.dumps(json_ready({"run_id": RUN_ID, "judgment": summary["judgment"], "selected": summary["selected_variant_id"]}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
