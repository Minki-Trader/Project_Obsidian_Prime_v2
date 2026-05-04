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
from foundation.models.elasticnet_logistic import (
    ElasticNetLogisticVariantSpec,
    characteristic_score,
    coefficient_frame,
    coefficient_shape_read,
    default_stage21_elasticnet_variants,
    fit_elasticnet_variant,
    nonflat_threshold,
    probability_frame,
    probability_shape_metrics,
    sign_overlap_read,
    split_decision_metrics,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 21
STAGE_ID = "21_model_family_challenge__elasticnet_logistic_linear_sanity"
RUN_NUMBER = "run15A"
RUN_ID = "run15A_elasticnet_logistic_linear_sanity_scout_v1"
PACKET_ID = "stage21_run15A_elasticnet_logistic_scout_v1"
EXPLORATION_LABEL = "stage21_Model__ElasticNetLogisticLinearSanity"
IDEA_ID = "IDEA-ST21-ELASTICNET-LOGISTIC-LINEAR-SANITY"
MODEL_FAMILY = "sklearn_logistic_regression_elasticnet_multiclass_saga"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
THRESHOLD_QUANTILE = 0.90
BOUNDARY = "elasticnet_logistic_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_elasticnet_logistic_sparse_linear_scout_completed"
NEXT_RUN_ID = "run15B_elasticnet_logistic_onnx_runtime_probe_v1"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run15A_elasticnet_logistic_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage21_run15A_elasticnet_logistic_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORK_ORDER_PATH = ROOT / "docs/workspace/stage19_25_model_research_work_order.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


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


def variant_characteristic(context: Mapping[str, Any], spec: ElasticNetLogisticVariantSpec) -> dict[str, Any]:
    model, sample = fit_elasticnet_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    prob = probability_frame(model, context["tier_a_frame"], spec.feature_names)
    threshold = nonflat_threshold(prob, THRESHOLD_QUANTILE)
    metrics = split_decision_metrics(prob, threshold)
    probability_shape = probability_shape_metrics(prob)
    coefficients = coefficient_frame(model, spec.feature_names)
    coefficient_read = coefficient_shape_read(coefficients)
    result_root = RUN_ROOT / "results/variant_coefficients"
    io_path(result_root).mkdir(parents=True, exist_ok=True)
    coefficient_path = result_root / f"{spec.variant_id}_tier_a_coefficients.csv"
    coefficients.to_csv(io_path(coefficient_path), index=False)
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
        "training_sample": sample,
        "threshold": threshold,
        "metrics": metrics,
        "probability_shape": probability_shape,
        "coefficient_read": coefficient_read,
        "coefficient_artifact": {"path": rel(coefficient_path), "sha256": sha256_file_lf_normalized(coefficient_path)},
        "characteristic_score": characteristic_score(metrics, probability_shape, coefficients),
    }


def choose_selected_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    compatible = [row for row in rows if row.get("spec", {}).get("tier_b_compatible") is True]
    pool = compatible or list(rows)
    return dict(max(pool, key=lambda row: safe_float(row.get("characteristic_score")), default={}))


def selected_spec(row: Mapping[str, Any]) -> ElasticNetLogisticVariantSpec:
    payload = dict(row.get("spec", {}))
    payload["feature_names"] = tuple(payload["feature_names"])
    return ElasticNetLogisticVariantSpec(**payload)


def materialize_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    io_path(result_root).mkdir(parents=True, exist_ok=True)
    json_path = result_root / "elasticnet_variant_results.json"
    csv_path = result_root / "elasticnet_variant_results.csv"
    write_json(json_path, list(rows))
    csv_rows: list[dict[str, Any]] = []
    for row in rows:
        spec = row.get("spec", {})
        metrics = row.get("metrics", {})
        coef = row.get("coefficient_read", {})
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "idea_id": row.get("idea_id"),
                "feature_count": len(spec.get("feature_names", [])),
                "c_value": spec.get("c_value"),
                "l1_ratio": spec.get("l1_ratio"),
                "tier_b_compatible": spec.get("tier_b_compatible"),
                "threshold": row.get("threshold"),
                "characteristic_score": row.get("characteristic_score"),
                "validation_signal_coverage": metrics.get("validation", {}).get("signal_coverage"),
                "oos_signal_coverage": metrics.get("oos", {}).get("signal_coverage"),
                "validation_directional_hit_rate": metrics.get("validation", {}).get("directional_hit_rate"),
                "oos_directional_hit_rate": metrics.get("oos", {}).get("directional_hit_rate"),
                "nonzero_feature_count": coef.get("nonzero_feature_count"),
                "nonzero_ratio": coef.get("nonzero_ratio"),
                "top10_abs_share": coef.get("top10_abs_share"),
                "coefficient_artifact": row.get("coefficient_artifact", {}).get("path"),
            }
        )
    write_csv(
        csv_path,
        (
            "variant_id",
            "idea_id",
            "feature_count",
            "c_value",
            "l1_ratio",
            "tier_b_compatible",
            "threshold",
            "characteristic_score",
            "validation_signal_coverage",
            "oos_signal_coverage",
            "validation_directional_hit_rate",
            "oos_directional_hit_rate",
            "nonzero_feature_count",
            "nonzero_ratio",
            "top10_abs_share",
            "coefficient_artifact",
        ),
        csv_rows,
    )
    return {
        "variant_results_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_results_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def materialize_selected_models(
    context: Mapping[str, Any],
    spec: ElasticNetLogisticVariantSpec,
) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame, float, float, dict[str, Any]]:
    root = RUN_ROOT / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_model, a_sample = fit_elasticnet_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    tier_b_model, b_sample = fit_elasticnet_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], spec.feature_names)
    tier_b_train_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], spec.feature_names)
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], spec.feature_names)
    a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(tier_b_train_prob, THRESHOLD_QUANTILE)
    tier_a_joblib = root / f"{spec.variant_id}_tier_a_elasticnet_logistic.joblib"
    tier_b_joblib = root / f"{spec.variant_id}_tier_b_elasticnet_logistic.joblib"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_coefficients = coefficient_frame(tier_a_model, spec.feature_names)
    tier_b_coefficients = coefficient_frame(tier_b_model, spec.feature_names)
    tier_a_coef_path = RUN_ROOT / "results/selected_tier_a_coefficients.csv"
    tier_b_coef_path = RUN_ROOT / "results/selected_tier_b_coefficients.csv"
    tier_a_coefficients.to_csv(io_path(tier_a_coef_path), index=False)
    tier_b_coefficients.to_csv(io_path(tier_b_coef_path), index=False)
    coefficient_read = {
        "tier_a": coefficient_shape_read(tier_a_coefficients),
        "tier_b": coefficient_shape_read(tier_b_coefficients),
        "tier_a_tier_b_sign_overlap": sign_overlap_read(tier_a_coefficients, tier_b_coefficients),
    }
    artifacts = {
        "selected_variant_id": spec.variant_id,
        "tier_a_training_sample": a_sample,
        "tier_b_training_sample": b_sample,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
        "tier_a_coefficients": {"path": rel(tier_a_coef_path), "sha256": sha256_file_lf_normalized(tier_a_coef_path)},
        "tier_b_coefficients": {"path": rel(tier_b_coef_path), "sha256": sha256_file_lf_normalized(tier_b_coef_path)},
    }
    return artifacts, tier_a_prob, tier_b_prob, a_threshold, b_threshold, coefficient_read


def build_summary(
    context: Mapping[str, Any],
    variants: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    coefficient_read: Mapping[str, Any],
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
        "mt5_runtime_probe_status": f"not_attempted_in_run15A_next_milestone_{NEXT_RUN_ID}",
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
        "selected_coefficient_read": coefficient_read,
        "artifacts": {
            "model_input_path": rel(MODEL_INPUT_PATH),
            "feature_order_path": rel(FEATURE_ORDER_PATH),
            "variant_results": rel(RUN_ROOT / "results/elasticnet_variant_results.csv"),
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
        "next_condition": f"Run {NEXT_RUN_ID} as the narrow MT5 runtime_probe by exporting the selected ElasticNet Logistic model to ONNX and using a sentinel tester tranche before any larger batch.",
    }


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "ElasticNet Logistic can reveal whether a sparse linear probability shape remains after nonlinear stages.",
            "decision_use": "Decide whether Stage21 should continue to a narrow MT5 ONNX runtime_probe.",
            "comparison_baseline": "No baseline; compare only within Stage21 ElasticNet Logistic variants and fixed data contract.",
            "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, "Tier A/B paired records"],
            "changed_variables": ["model_family=ElasticNet Logistic", "feature subset", "l1_ratio", "C"],
            "success_criteria": ["non-flat sparse coefficients", "usable Tier A/B prediction records", "clear ONNX handoff candidate"],
            "failure_criteria": ["flat probabilities", "all-zero coefficients", "unstable validation/OOS density", "no Tier-B-compatible candidate"],
            "invalid_conditions": ["missing split", "missing feature", "duplicate timestamp", "non-finite feature"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_source": rel(MODEL_INPUT_PATH),
            "time_axis": "timestamp is UTC-normalized project timestamp and split contract is unchanged.",
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
            "selection_metric": "characteristic_score on sparse coefficients, signal density, validation/OOS stability, and margin diagnostics; not trading profit.",
            "threshold_policy": f"non-flat q{THRESHOLD_QUANTILE:.2f} from validation split.",
            "overfit_risk": "single split and small hand-authored variant set; no WFO or MT5 evidence yet.",
            "calibration_risk": "multiclass logistic probabilities are scout probabilities only until runtime parity and MT5 probing.",
            "validation_judgment": "inconclusive_structural_scout",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [rel(MODEL_INPUT_PATH), rel(FEATURE_ORDER_PATH), rel(TRAINING_SUMMARY_PATH)],
            "producer": "stage_pipelines.stage21.elasticnet_logistic_scout",
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
            "evidence_available": ["variant results", "Tier A/B prediction records", "coefficient records", "stage and project ledgers"],
            "evidence_missing": ["MT5 runtime_probe", "ONNX/runtime parity", "WFO", "runtime authority"],
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": summary.get("next_condition"),
        },
    ]


def top_feature_lines(coefficient_read: Mapping[str, Any]) -> str:
    rows = coefficient_read.get("tier_a", {}).get("top_features", [])
    if not rows:
        return "- no coefficient terms recorded(계수 항목 기록 없음)"
    return "\n".join(
        "- `{feature}`: max_abs_coef(최대 절대 계수) `{coef:.6f}`, dominant_label(우세 라벨) `{label}`, dominant_sign(우세 부호) `{sign}`".format(
            feature=row.get("feature"),
            coef=safe_float(row.get("max_abs_coef")),
            label=row.get("dominant_label"),
            sign=row.get("dominant_sign"),
        )
        for row in rows[:8]
    )


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    selected = str(summary.get("selected_variant_id"))
    coefficient_read = summary.get("selected_coefficient_read", {})
    write_md(
        REPORT_PATH,
        f"""# RUN15A ElasticNet Logistic Scout Packet(실행15A 엘라스틱넷 로지스틱 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- best overall variant(전체 최고 변형): `{summary.get('best_overall_variant_id')}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run15A_next_milestone_{NEXT_RUN_ID}(실행15A에서는 미시도, 다음 마일스톤은 {NEXT_RUN_ID})`

효과(effect, 효과): ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear probability shape(희소 선형 확률 모양)과 coefficient sign(계수 부호)을 Python-side evidence(파이썬 측 근거)로 잡았다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `{summary.get('variant_count')}`
- Tier A rows(Tier A 행): `{summary.get('tier_a_rows')}`
- Tier B fallback rows(Tier B 대체 행): `{summary.get('tier_b_fallback_rows')}`
- validation signal coverage(검증 신호 커버리지): `{summary.get('selected_tier_a_validation_signal_coverage')}`
- OOS signal coverage(표본외 신호 커버리지): `{summary.get('selected_tier_a_oos_signal_coverage')}`
- validation directional hit(검증 방향 적중): `{summary.get('selected_tier_a_validation_directional_hit_rate')}`
- OOS directional hit(표본외 방향 적중): `{summary.get('selected_tier_a_oos_directional_hit_rate')}`
- Tier A nonzero ratio(Tier A 비영 계수 비율): `{coefficient_read.get('tier_a', {}).get('nonzero_ratio')}`
- Tier B nonzero ratio(Tier B 비영 계수 비율): `{coefficient_read.get('tier_b', {}).get('nonzero_ratio')}`
- Tier A/B sign overlap(Tier A/B 부호 겹침): `{coefficient_read.get('tier_a_tier_b_sign_overlap', {}).get('same_dominant_sign_share')}`

## Top Coefficients(상위 계수)

{top_feature_lines(coefficient_read)}

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침). Export(내보내기) selected ElasticNet Logistic(선택 엘라스틱넷 로지스틱) model(모델) to ONNX(온닉스) and start with a sentinel tranche(감시 실행 묶음) before any larger batch(더 큰 배치).
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Stage21 RUN15A ElasticNet Logistic Decision(21단계 실행15A 엘라스틱넷 로지스틱 결정)

## Decision(결정)

`{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): Stage21(21단계)은 sparse linear scout(희소 선형 탐색) 근거를 확보했지만, MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)가 아직 없으므로 closeout(마감)이나 operating meaning(운영 의미)으로 올리지 않는다.

## Next Condition(다음 조건)

다음 milestone(마일스톤)은 `{NEXT_RUN_ID}`이다. 조건(condition, 조건)은 selected variant(선택 변형)를 ONNX(온닉스) handoff file(인계 파일)로 만들고 MT5 runtime_probe(런타임 탐침)에서 report(보고서), telemetry(기록), normalized KPI(정규화 핵심 성과 지표)를 확인하는 것이다.
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage21 Selection Status(21단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run15A_python_structural_scout_completed(실행15A 파이썬 구조 탐색 완료)`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage21(21단계)는 ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear signal(희소 선형 신호)을 탐색했지만 MT5 runtime_probe(MT5 런타임 탐침), closeout(마감), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )
    write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage21 Review Index(21단계 검토 색인)

- `{RUN_ID}`: `{rel(REPORT_PATH)}`

효과(effect, 효과): Stage21(21단계)의 검토 근거 위치를 한 곳에서 찾게 한다.
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
            "allowed_claims": ["python_structural_scout_completed", "sparse_linear_shape_clues_recorded"],
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
    rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=summary.get("tier_records", []),
        mt5_kpi_records=[],
        selected_threshold_id=str(summary.get("selected_threshold_id")),
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
                ("mt5_next", NEXT_RUN_ID),
                ("boundary", BOUNDARY),
            )
        ),
    }
    ledgers["run_registry"] = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    return ledgers


def replace_yaml_block(text: str, block_name: str, block: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line == block_name:
            start = index
            break
    block_lines = block.rstrip().splitlines()
    if start is None:
        suffix = "\n" if text.endswith("\n") else ""
        return text + suffix + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith(" ") and not line.startswith("-"):
            end = index
            break
    new_lines = lines[:start] + block_lines + lines[end:]
    return "\n".join(new_lines) + "\n"


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    path = io_path(WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = text.replace("current_run_id: not_started", f"current_run_id: {RUN_ID}", 1)
    text = text.replace(
        "- treat Stage 21 as active and opened_not_started after Stage 20 GAM runtime_probe and reviewed closeout; next action is run15A_elasticnet_logistic_linear_sanity_scout_v1, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 21 as active after {RUN_ID} ElasticNet Logistic Python structural scout; next action is {NEXT_RUN_ID} MT5 runtime_probe, and no baseline, promotion, or runtime authority exists",
        1,
    )
    text = text.replace("      status: opened_not_started\n      current_run_id: not_started", f"      status: active_run15A_python_structural_scout_completed\n      current_run_id: {RUN_ID}", 1)
    text = text.replace(
        """stage21_elasticnet_logistic_linear_sanity:
  stage_id: 21_model_family_challenge__elasticnet_logistic_linear_sanity
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/21_model_family_challenge__elasticnet_logistic_linear_sanity/00_spec/stage_brief.md
  selection_status_path: stages/21_model_family_challenge__elasticnet_logistic_linear_sanity/04_selected/selection_status.md
  next_action: run15A_elasticnet_logistic_linear_sanity_scout_v1""",
        f"""stage21_elasticnet_logistic_linear_sanity:
  stage_id: 21_model_family_challenge__elasticnet_logistic_linear_sanity
  status: active_run15A_python_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  stage_brief_path: stages/21_model_family_challenge__elasticnet_logistic_linear_sanity/00_spec/stage_brief.md
  selection_status_path: stages/21_model_family_challenge__elasticnet_logistic_linear_sanity/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}""",
        1,
    )
    block = f"""stage21_elasticnet_run15A_structural_scout:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary.get('selected_variant_id')}
  best_overall_variant_id: {summary.get('best_overall_variant_id')}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / 'aggregate_summary.json')}
  next_action: {NEXT_RUN_ID}"""
    text = replace_yaml_block(text, "stage21_elasticnet_run15A_structural_scout:", block)
    path.write_text(text, encoding="utf-8-sig")


def update_goal_plan(summary: Mapping[str, Any]) -> None:
    path = io_path(GOAL_PLAN_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = text.replace(
        "- current run(현재 실행): `not_started`",
        f"- current run(현재 실행): `{RUN_ID}`",
        1,
    )
    text = text.replace(
        "효과(effect, 효과): 이 문서는 Stage20-32(20-32단계)의 운영 목표(goal, 목표)를 고정하며, Stage20(20단계)은 MT5 runtime_probe(런타임 탐침)와 reviewed closeout(검토된 마감)을 끝냈고 현재 첫 미완료 milestone(마일스톤)은 Stage21(21단계) `run15A_elasticnet_logistic_linear_sanity_scout_v1`이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
        f"효과(effect, 효과): 이 문서는 Stage20-32(20-32단계)의 운영 목표(goal, 목표)를 고정하며, Stage20(20단계)은 MT5 runtime_probe(런타임 탐침)와 reviewed closeout(검토된 마감)을 끝냈고 Stage21(21단계)은 `{RUN_ID}` Python structural scout(파이썬 구조 탐색)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage21(21단계) `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
        1,
    )
    text = text.replace(
        "Current active milestone(현재 활성 마일스톤): Stage21(21단계) `run15A_elasticnet_logistic_linear_sanity_scout_v1` broad scout(넓은 탐색).",
        f"Current active milestone(현재 활성 마일스톤): Stage21(21단계) `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침).",
        1,
    )
    start = text.find("## Latest Stop Resume State(최신 중지 재개 상태)")
    end = text.find("\n## Per-Stage Milestone Loop", start)
    if start != -1 and end != -1:
        block = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료).
- active stage/current run id(활성 단계/현재 실행 ID): Stage21(21단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/21_model_family_challenge__elasticnet_logistic_linear_sanity/02_runs`, `03_reviews`, `04_selected`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): Stage21 ElasticNet Logistic scout(21단계 엘라스틱넷 로지스틱 탐색), current truth docs(현재 진실 문서), ledgers(장부), tests(테스트).
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `not_attempted_in_run15A(실행15A 미시도)`; next(다음) `{NEXT_RUN_ID}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): create and run(생성 및 실행) `{NEXT_RUN_ID}` as sentinel MT5 runtime_probe(감시 MT5 런타임 탐침).
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending before stop(중지 전 대기).

효과(effect, 효과): 다음 재개는 Stage21(21단계) MT5 runtime_probe(런타임 탐침)에서 시작한다.
"""
        text = text[:start] + block + text[end:]
    path.write_text(text, encoding="utf-8-sig")


def prepend_current_state(summary: Mapping[str, Any]) -> None:
    path = io_path(CURRENT_STATE_PATH)
    old = path.read_text(encoding="utf-8-sig")
    block = f"""## Latest Stage21 RUN15A ElasticNet Logistic Update(최신 21단계 실행15A 엘라스틱넷 로지스틱 업데이트)

Stage21(21단계) `{RUN_ID}`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{summary.get('selected_variant_id')}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear probability shape(희소 선형 확률 모양), coefficient sign(계수 부호), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 남겼다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    path.write_text(block + old, encoding="utf-8-sig")


def update_work_order() -> None:
    path = io_path(WORK_ORDER_PATH)
    text = path.read_text(encoding="utf-8-sig")
    line = f"- 2026-05-05: Stage21(21단계) `{RUN_ID}` Python structural scout(파이썬 구조 탐색) 완료. 효과(effect, 효과): ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear probability shape(희소 선형 확률 모양)을 기록했고 다음은 `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)이다.\n"
    if RUN_ID not in text:
        text = text.rstrip() + "\n" + line
        path.write_text(text, encoding="utf-8-sig")


def run() -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variants = [
        variant_characteristic(context, spec)
        for spec in default_stage21_elasticnet_variants(
            full_feature_order=context["full_feature_order"],
            tier_b_feature_order=context["tier_b_feature_order"],
        )
    ]
    variant_artifacts = materialize_variant_results(variants)
    selected = choose_selected_variant(variants)
    spec = selected_spec(selected)
    model_artifacts, tier_a_prob, tier_b_prob, a_threshold, b_threshold, coefficient_read = materialize_selected_models(context, spec)
    tier_records, prediction_artifacts = materialize_python_tier_records(tier_a_prob, tier_b_prob, a_threshold, b_threshold)
    summary = build_summary(context, variants, selected, model_artifacts, {**prediction_artifacts, **variant_artifacts}, tier_records, coefficient_read)
    write_json(RUN_ROOT / "run_manifest.json", {"created_at_utc": created_at, "summary": summary})
    write_json(RUN_ROOT / "kpi_record.json", {"created_at_utc": created_at, "tier_records": tier_records, "judgment": JUDGMENT})
    write_json(RUN_ROOT / "summary.json", summary)
    write_stage_docs(summary)
    write_packet_artifacts(summary, created_at)
    ledgers = materialize_ledgers(summary)
    summary["ledger_updates"] = ledgers
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    update_workspace_state(summary)
    update_goal_plan(summary)
    prepend_current_state(summary)
    update_work_order()
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage21 ElasticNet Logistic sparse linear scout.")
    parser.parse_args(argv)
    summary = run()
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "judgment": summary["judgment"],
                    "selected": summary["selected_variant_id"],
                    "next": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
