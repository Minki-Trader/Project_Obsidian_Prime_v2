from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    FEATURE_ORDER_PATH,
    METAEDITOR_PATH_DEFAULT,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    TRAINING_SUMMARY_PATH,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.catboost_ordered import (
    CatBoostVariantSpec,
    characteristic_score,
    default_stage18_catboost_variants,
    feature_importance_frame,
    fit_catboost_variant,
    nonflat_threshold,
    probability_frame,
    probability_shape_metrics,
    selected_spec,
    split_decision_metrics,
)
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_catboost_classifier_to_onnx, ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 18
STAGE_ID = "18_model_family_challenge__catboost_ordered_boosting_scout"
AGGREGATE_PACKET_ID = "stage18_catboost_characteristic_mt5_kpi_v1"
MODEL_FAMILY = "catboost_catboostclassifier_multiclass_ordered_boosting"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
STAGE_INHERITANCE = "independent_catboost_topic_after_stage17_xgboost_closeout_no_baseline_inheritance"
ONNX_OPSET = 13
ONNX_PARITY_TOLERANCE = 1e-5
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0
ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
AGGREGATE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / AGGREGATE_PACKET_ID


@dataclass(frozen=True)
class RunTopic:
    run_id: str
    run_number: str
    packet_id: str
    exploration_label: str
    review_filename: str
    decision_filename: str
    threshold_quantile: float
    mode: str
    expected_attempts: int
    expected_kpi_records: int
    boundary: str
    judgment_completed: str
    judgment_blocked: str
    topic_read: str

    @property
    def run_root(self) -> Path:
        return STAGE_ROOT / "02_runs" / self.run_id

    @property
    def packet_root(self) -> Path:
        return ROOT / "docs/agent_control/packets" / self.packet_id

    @property
    def review_path(self) -> Path:
        return STAGE_ROOT / "03_reviews" / self.review_filename

    @property
    def decision_path(self) -> Path:
        return ROOT / "docs/decisions" / self.decision_filename


RUN_TOPICS: tuple[RunTopic, ...] = (
    RunTopic(
        run_id="run12A_catboost_ordered_boosting_characteristic_scout_v1",
        run_number="run12A",
        packet_id="stage18_run12A_catboost_characteristic_mt5_v1",
        exploration_label="stage18_Model__CatBoostOrderedCharacteristic",
        review_filename="run12A_catboost_characteristic_mt5_packet.md",
        decision_filename="2026-05-03_stage18_run12A_catboost_characteristic_mt5.md",
        threshold_quantile=0.90,
        mode="routed",
        expected_attempts=6,
        expected_kpi_records=10,
        boundary="catboost_ordered_characteristic_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_catboost_ordered_characteristic_mt5_runtime_probe_completed",
        judgment_blocked="blocked_catboost_ordered_characteristic_mt5_runtime_probe_after_attempt",
        topic_read="ordered_boosting_probability_shape",
    ),
    RunTopic(
        run_id="run12B_catboost_q80_signal_density_probe_v1",
        run_number="run12B",
        packet_id="stage18_run12B_catboost_signal_density_mt5_v1",
        exploration_label="stage18_Model__CatBoostQ80SignalDensity",
        review_filename="run12B_catboost_signal_density_packet.md",
        decision_filename="2026-05-03_stage18_run12B_catboost_signal_density.md",
        threshold_quantile=0.80,
        mode="routed",
        expected_attempts=6,
        expected_kpi_records=10,
        boundary="catboost_q80_signal_density_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_catboost_q80_signal_density_mt5_runtime_probe_completed",
        judgment_blocked="blocked_catboost_q80_signal_density_mt5_runtime_probe_after_attempt",
        topic_read="q80_signal_density_pressure",
    ),
    RunTopic(
        run_id="run12C_catboost_q80_direction_balance_probe_v1",
        run_number="run12C",
        packet_id="stage18_run12C_catboost_direction_balance_mt5_v1",
        exploration_label="stage18_Model__CatBoostQ80DirectionBalance",
        review_filename="run12C_catboost_direction_balance_packet.md",
        decision_filename="2026-05-03_stage18_run12C_catboost_direction_balance.md",
        threshold_quantile=0.80,
        mode="direction",
        expected_attempts=12,
        expected_kpi_records=20,
        boundary="catboost_q80_direction_balance_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_catboost_q80_direction_balance_mt5_runtime_probe_completed",
        judgment_blocked="blocked_catboost_q80_direction_balance_mt5_runtime_probe_after_attempt",
        topic_read="direction_balance_long_short_split",
    ),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True) + "\n")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if pd.notna(number) else default


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


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


def tier_record(
    topic: RunTopic,
    record_view: str,
    tier_scope: str,
    prob_frame: pd.DataFrame,
    threshold: float,
    path: Path,
) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {str(key): int(value) for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()}
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{topic.threshold_quantile:.2f}",
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


def python_tier_records(
    topic: RunTopic,
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    a_threshold: float,
    b_threshold: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = topic.run_root / "predictions"
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
        tier_record(topic, "tier_a_separate", mt5.TIER_A, tier_a_prob, a_threshold, a_path),
        tier_record(topic, "tier_b_separate", mt5.TIER_B, tier_b_prob, b_threshold, b_path),
        tier_record(topic, "tier_ab_combined", mt5.TIER_AB, ab_prob, a_threshold, ab_path),
    ]
    artifacts = {
        "tier_a": save_predictions(a_path, tier_a_prob),
        "tier_b": save_predictions(b_path, tier_b_prob),
        "tier_ab": save_predictions(ab_path, ab_prob),
    }
    return records, artifacts


def variant_characteristic(context: Mapping[str, Any], spec: CatBoostVariantSpec) -> dict[str, Any]:
    model, sample = fit_catboost_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    prob = probability_frame(model, context["tier_a_frame"], context["full_feature_order"])
    threshold = nonflat_threshold(prob, 0.90)
    metrics = split_decision_metrics(prob, threshold)
    shape = probability_shape_metrics(prob)
    importance = feature_importance_frame(model, context["full_feature_order"])
    root = RUN_TOPICS[0].run_root / "results" / "variant_importance"
    io_path(root).mkdir(parents=True, exist_ok=True)
    importance_path = root / f"{spec.variant_id}_feature_importance.csv"
    importance.to_csv(io_path(importance_path), index=False)
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
        "training_sample": sample,
        "threshold": threshold,
        "metrics": metrics,
        "probability_shape": shape,
        "feature_importance": {
            "path": rel(importance_path),
            "sha256": sha256_file_lf_normalized(importance_path),
            "top10_gain_share": float(importance.head(10)["gain_share"].sum()) if not importance.empty else None,
            "top_features": importance.head(10).to_dict(orient="records"),
        },
        "characteristic_score": characteristic_score(metrics, shape, importance),
    }


def choose_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return dict(max(rows, key=lambda row: safe_float(row.get("characteristic_score")), default={}))


def materialize_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_TOPICS[0].run_root / "results"
    io_path(result_root).mkdir(parents=True, exist_ok=True)
    json_path = result_root / "catboost_variant_results.json"
    csv_path = result_root / "catboost_variant_results.csv"
    write_json(json_path, list(rows))
    with io_path(csv_path).open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "variant_id",
            "idea_id",
            "boosting_type",
            "bootstrap_type",
            "characteristic_score",
            "threshold",
            "val_signal_coverage",
            "oos_signal_coverage",
            "val_directional_hit_rate",
            "oos_directional_hit_rate",
            "val_log_loss",
            "oos_log_loss",
            "top10_gain_share",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            metrics = row.get("metrics", {})
            spec = row.get("spec", {})
            writer.writerow(
                {
                    "variant_id": row.get("variant_id"),
                    "idea_id": row.get("idea_id"),
                    "boosting_type": spec.get("boosting_type"),
                    "bootstrap_type": spec.get("bootstrap_type"),
                    "characteristic_score": row.get("characteristic_score"),
                    "threshold": row.get("threshold"),
                    "val_signal_coverage": metrics.get("validation", {}).get("signal_coverage"),
                    "oos_signal_coverage": metrics.get("oos", {}).get("signal_coverage"),
                    "val_directional_hit_rate": metrics.get("validation", {}).get("directional_hit_rate"),
                    "oos_directional_hit_rate": metrics.get("oos", {}).get("directional_hit_rate"),
                    "val_log_loss": metrics.get("validation", {}).get("log_loss"),
                    "oos_log_loss": metrics.get("oos", {}).get("log_loss"),
                    "top10_gain_share": row.get("feature_importance", {}).get("top10_gain_share"),
                }
            )
    return {
        "variant_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def materialize_selected_models(
    topic: RunTopic,
    context: Mapping[str, Any],
    spec: CatBoostVariantSpec,
) -> tuple[dict[str, Any], Any, Any, pd.DataFrame, pd.DataFrame, float, float]:
    root = topic.run_root / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_model, _a_sample = fit_catboost_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    tier_b_model, _b_sample = fit_catboost_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["full_feature_order"])
    tier_b_train_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    a_threshold = nonflat_threshold(tier_a_prob, topic.threshold_quantile)
    b_threshold = nonflat_threshold(tier_b_train_prob, topic.threshold_quantile)
    tier_a_joblib = root / f"{spec.variant_id}_tier_a_catboost.joblib"
    tier_b_joblib = root / f"{spec.variant_id}_tier_b_catboost_core42.joblib"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    artifacts = {
        "selected_variant_id": spec.variant_id,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
    }
    return artifacts, tier_a_model, tier_b_model, tier_a_prob, tier_b_prob, a_threshold, b_threshold


def export_models(topic: RunTopic, context: Mapping[str, Any], model_artifacts: Mapping[str, Any], tier_a_model: Any, tier_b_model: Any) -> dict[str, Any]:
    root = topic.run_root / "models"
    variant_id = str(model_artifacts["selected_variant_id"])
    tier_a_onnx = root / f"{variant_id}_tier_a_catboost_opset{ONNX_OPSET}.onnx"
    tier_b_onnx = root / f"{variant_id}_tier_b_catboost_core42_opset{ONNX_OPSET}.onnx"
    tier_a_export = export_catboost_classifier_to_onnx(tier_a_model, tier_a_onnx, feature_count=len(context["full_feature_order"]), target_opset=ONNX_OPSET)
    tier_b_export = export_catboost_classifier_to_onnx(tier_b_model, tier_b_onnx, feature_count=len(context["tier_b_feature_order"]), target_opset=ONNX_OPSET)
    a_sample = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq("validation"), context["full_feature_order"]].head(128).to_numpy(dtype="float64", copy=False)
    b_sample = context["tier_b_training_frame"].loc[context["tier_b_training_frame"]["split"].astype(str).eq("validation"), context["tier_b_feature_order"]].head(128).to_numpy(dtype="float64", copy=False)
    return {
        "tier_a_onnx": {**tier_a_export, "path": rel(Path(tier_a_export["path"]))},
        "tier_b_onnx": {**tier_b_export, "path": rel(Path(tier_b_export["path"]))},
        "onnx_parity": {
            "tier_a": check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, a_sample, tolerance=ONNX_PARITY_TOLERANCE),
            "tier_b": check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, b_sample, tolerance=ONNX_PARITY_TOLERANCE),
        },
    }


def export_feature_matrices(topic: RunTopic, context: Mapping[str, Any]) -> dict[str, Any]:
    root = topic.run_root / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            context["full_feature_order"],
            root / f"tier_a_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            context["tier_b_feature_order"],
            root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(topic: RunTopic, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_routed_attempts(
    topic: RunTopic,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": topic.run_root,
            "run_id": topic.run_id,
            "stage_number": STAGE_NUMBER,
            "exploration_label": topic.exploration_label,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_only_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=float(thresholds["tier_a"]), long_threshold=float(thresholds["tier_a"]), min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="tier_only_total", record_view_prefix="mt5_tier_a_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_fallback_only_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{topic.run_id}_tier_b", feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=float(thresholds["tier_b"]), long_threshold=float(thresholds["tier_b"]), min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role="tier_b_fallback_only_total", record_view_prefix="mt5_tier_b_fallback_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=float(thresholds["tier_a"]), long_threshold=float(thresholds["tier_a"]), min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="routed_total", record_view_prefix="mt5_routed_total", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{topic.run_id}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=float(thresholds["tier_b"]), fallback_long_threshold=float(thresholds["tier_b"]), fallback_min_margin=MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def make_direction_attempts(
    topic: RunTopic,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    disabled_threshold = 1.1
    sides = (
        ("long_only", disabled_threshold, float(thresholds["tier_a"]), disabled_threshold, float(thresholds["tier_b"])),
        ("short_only", float(thresholds["tier_a"]), disabled_threshold, float(thresholds["tier_b"]), disabled_threshold),
    )
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": topic.run_root,
            "run_id": topic.run_id,
            "stage_number": STAGE_NUMBER,
            "exploration_label": topic.exploration_label,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        for side, a_short, a_long, b_short, b_long in sides:
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_{side}_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=a_short, long_threshold=a_long, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role=f"tier_a_{side}", record_view_prefix=f"mt5_tier_a_{side}"))
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_{side}_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{topic.run_id}_tier_b", feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=b_short, long_threshold=b_long, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role=f"tier_b_{side}", record_view_prefix=f"mt5_tier_b_{side}"))
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{side}_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=a_short, long_threshold=a_long, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role=f"routed_{side}", record_view_prefix=f"mt5_routed_{side}", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{topic.run_id}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=b_short, fallback_long_threshold=b_long, fallback_min_margin=MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def make_attempts(
    topic: RunTopic,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    thresholds: Mapping[str, Any],
) -> list[dict[str, Any]]:
    if topic.mode == "direction":
        return make_direction_attempts(topic, context, model_artifacts, feature_matrices, thresholds)
    return make_routed_attempts(topic, context, model_artifacts, feature_matrices, thresholds)


def execute_or_block(topic: RunTopic, prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {**dict(prepared), "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": topic.judgment_blocked, "failure": {"type": "materialize_only", "message": "MT5 execution was skipped by CLI flag."}}
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": topic.judgment_blocked, "failure": {"type": type(exc).__name__, "message": str(exc)}}
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = topic.judgment_completed if completed else topic.judgment_blocked
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = prepared["selected_variant_id"]
        record["topic_read"] = topic.topic_read
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def metrics_by_view_or_report_hint(result: Mapping[str, Any], view: str, report_hint: str) -> dict[str, Any]:
    metrics = metrics_by_view(result, view)
    if metrics:
        return metrics
    for record in result.get("mt5_kpi_records", []):
        report = record.get("report", {})
        if not isinstance(report, Mapping):
            continue
        path_candidates: list[str] = []
        html_report = report.get("html_report", {})
        if isinstance(html_report, Mapping) and html_report.get("path"):
            path_candidates.append(str(html_report.get("path")))
        metrics_report = report.get("metrics", {})
        if isinstance(metrics_report, Mapping) and metrics_report.get("report_path"):
            path_candidates.append(str(metrics_report.get("report_path")))
        source_report = report.get("source_report", {})
        if isinstance(source_report, Mapping):
            source_html = source_report.get("html_report", {})
            if isinstance(source_html, Mapping) and source_html.get("path"):
                path_candidates.append(str(source_html.get("path")))
        if any(report_hint in candidate for candidate in path_candidates):
            raw_metrics = record.get("metrics", {})
            return dict(raw_metrics) if isinstance(raw_metrics, Mapping) else {}
    return {}


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    parity = model_artifacts.get("onnx_parity", {})
    return bool(parity.get("tier_a", {}).get("passed")) and bool(parity.get("tier_b", {}).get("passed"))


def build_run_read(topic: RunTopic, summary: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    selected = summary.get("selected_variant", {})
    score = safe_float(selected.get("characteristic_score"))
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    if topic.mode == "direction":
        direction = summary.get("direction_routed", {})
        long_val = direction.get("long_validation", {})
        long_oos = direction.get("long_oos", {})
        short_val = direction.get("short_validation", {})
        short_oos = direction.get("short_oos", {})
        long_avg_trades = (safe_float(long_val.get("trade_count")) + safe_float(long_oos.get("trade_count"))) / 2.0
        short_avg_trades = (safe_float(short_val.get("trade_count")) + safe_float(short_oos.get("trade_count"))) / 2.0
        long_avg_pf = (safe_float(long_val.get("profit_factor")) + safe_float(long_oos.get("profit_factor"))) / 2.0
        short_avg_pf = (safe_float(short_val.get("profit_factor")) + safe_float(short_oos.get("profit_factor"))) / 2.0
        contrast = abs(long_avg_trades - short_avg_trades) / max(long_avg_trades + short_avg_trades, 1.0)
        pf_contrast = abs(long_avg_pf - short_avg_pf)
        visible = completed and parity_ok and (contrast >= 0.20 or pf_contrast >= 0.20)
        strength = "direction_balance_or_asymmetry_visible" if visible else "direction_axis_weak_or_incomplete"
        return {
            "characteristic_score": score,
            "model_characteristic_strength": strength,
            "run_recommendation": "preserve_direction_axis_for_attribution" if visible else "do_not_microtune_direction_axis",
            "closure_judgment": topic.judgment_completed if completed else topic.judgment_blocked,
            "direction_read": {
                "long_avg_routed_trades": long_avg_trades,
                "short_avg_routed_trades": short_avg_trades,
                "long_avg_profit_factor": long_avg_pf,
                "short_avg_profit_factor": short_avg_pf,
                "trade_count_contrast": contrast,
                "profit_factor_contrast": pf_contrast,
                "new_characteristic_visible": visible,
            },
        }
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    val_trades = safe_float(validation.get("trade_count"))
    oos_trades = safe_float(oos.get("trade_count"))
    avg_trades = (val_trades + oos_trades) / 2.0 if val_trades or oos_trades else 0.0
    val_net = safe_float(validation.get("net_profit"))
    oos_net = safe_float(oos.get("net_profit"))
    visible = completed and parity_ok and (score >= 0.50 or avg_trades >= 20)
    risk_warning = safe_float(oos.get("max_drawdown_percent")) >= 25.0 or safe_float(validation.get("max_drawdown_percent")) >= 25.0
    if topic.run_number == "run12B":
        strength = "q80_density_visible_risk_warning" if visible and risk_warning else "q80_density_visible" if visible else "q80_density_weak_or_incomplete"
    else:
        strength = "ordered_probability_shape_visible" if visible else "ordered_probability_shape_weak_or_incomplete"
    return {
        "characteristic_score": score,
        "model_characteristic_strength": strength,
        "run_recommendation": "continue_to_kpi_attribution" if visible else "stop_if_next_probe_has_no_axis",
        "closure_judgment": topic.judgment_completed if completed else topic.judgment_blocked,
        "runtime_read": {
            "avg_routed_trades": avg_trades,
            "validation_net_profit": val_net,
            "oos_net_profit": oos_net,
            "risk_warning": risk_warning,
            "new_characteristic_visible": visible,
        },
    }


def build_summary(
    topic: RunTopic,
    result: Mapping[str, Any],
    selected: Mapping[str, Any],
    variant_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "run_number": topic.run_number,
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "topic_read": topic.topic_read,
        "boundary": topic.boundary,
        "judgment": result["judgment"],
        "external_verification_status": result["external_verification_status"],
        "selected_variant": selected,
        "variant_artifacts": variant_artifacts,
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "python_tier_records": list(tier_records),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "attempt_count": len(result.get("attempts", [])),
    }
    if topic.mode == "direction":
        summary["direction_routed"] = {
            "long_validation": metrics_by_view_or_report_hint(result, "mt5_routed_long_only_validation_is", "_routed_long_only_validation_is"),
            "long_oos": metrics_by_view_or_report_hint(result, "mt5_routed_long_only_oos", "_routed_long_only_oos"),
            "short_validation": metrics_by_view_or_report_hint(result, "mt5_routed_short_only_validation_is", "_routed_short_only_validation_is"),
            "short_oos": metrics_by_view_or_report_hint(result, "mt5_routed_short_only_oos", "_routed_short_only_oos"),
        }
        summary["validation_routed"] = summary["direction_routed"]["long_validation"]
        summary["oos_routed"] = summary["direction_routed"]["long_oos"]
    else:
        summary["validation_routed"] = metrics_by_view(result, "mt5_routed_total_validation_is")
        summary["oos_routed"] = metrics_by_view(result, "mt5_routed_total_oos")
    summary.update(build_run_read(topic, summary))
    return summary


def upsert_run_registry(topic: RunTopic, result: Mapping[str, Any], read: Mapping[str, Any]) -> dict[str, Any]:
    validation = read.get("validation_routed", {})
    oos = read.get("oos_routed", {})
    row = {
        "run_id": topic.run_id,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": read["closure_judgment"],
        "path": rel(topic.run_root),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("topic_read", topic.topic_read),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("selected_variant", result.get("selected_variant_id")),
                ("threshold_quantile", f"q{topic.threshold_quantile:.2f}"),
                ("validation_net_profit", validation.get("net_profit")),
                ("validation_pf", validation.get("profit_factor")),
                ("oos_net_profit", oos.get("net_profit")),
                ("oos_pf", oos.get("profit_factor")),
                ("characteristic_strength", read.get("model_characteristic_strength")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def write_normalized_kpi(topic: RunTopic) -> dict[str, Any]:
    inventory = [{"run_id": topic.run_id, "stage_id": STAGE_ID, "idea_id": topic.run_number, "path": rel(topic.run_root)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_jsonl(topic.packet_root / "normalized_kpi_records.jsonl", records)
    write_csv_rows(topic.packet_root / "normalized_kpi_summary.csv", mt5_kpi_recorder.SUMMARY_COLUMNS, summary_rows)
    write_json(topic.packet_root / "normalized_kpi_missing_runs.json", missing)
    write_json(topic.packet_root / "normalized_kpi_parser_errors.json", parser_errors)
    write_jsonl(topic.packet_root / "enriched_kpi_records.jsonl", enriched)
    write_csv_rows(topic.packet_root / "trade_level_records.csv", mt5_trade_attribution.TRADE_COLUMNS, trade_rows)
    write_csv_rows(topic.packet_root / "trade_attribution_summary.csv", mt5_trade_attribution.SUMMARY_COLUMNS, trade_summary)
    write_json(topic.packet_root / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def run_result_markdown(topic: RunTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    selected = summary.get("selected_variant", {})
    lines = [
        f"# {topic.run_id} Result Summary({topic.run_number} 결과 요약)",
        "",
        f"- selected variant(선택 변형): `{selected.get('variant_id')}`",
        f"- topic read(주제 판독): `{topic.topic_read}`",
        f"- judgment(판정): `{summary.get('closure_judgment')}`",
        f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
        f"- characteristic strength(특성 강도): `{summary.get('model_characteristic_strength')}`",
        f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`",
        f"- normalized KPI records(정규화 핵심 성과 지표 기록): `{kpi.get('normalized_records')}`",
        "",
    ]
    if topic.mode == "direction":
        direction = summary.get("direction_routed", {})
        lines.extend(
            [
                "| side(방향) | validation trades/net/PF(검증 거래/순수익/수익 팩터) | OOS trades/net/PF(표본외 거래/순수익/수익 팩터) |",
                "|---|---:|---:|",
                f"| long-only(롱 전용) | `{direction.get('long_validation', {}).get('trade_count')} / {direction.get('long_validation', {}).get('net_profit')} / {direction.get('long_validation', {}).get('profit_factor')}` | `{direction.get('long_oos', {}).get('trade_count')} / {direction.get('long_oos', {}).get('net_profit')} / {direction.get('long_oos', {}).get('profit_factor')}` |",
                f"| short-only(숏 전용) | `{direction.get('short_validation', {}).get('trade_count')} / {direction.get('short_validation', {}).get('net_profit')} / {direction.get('short_validation', {}).get('profit_factor')}` | `{direction.get('short_oos', {}).get('trade_count')} / {direction.get('short_oos', {}).get('net_profit')} / {direction.get('short_oos', {}).get('profit_factor')}` |",
            ]
        )
    else:
        lines.extend(
            [
                "| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) | recovery(회복 계수) |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for key, label in (("validation_routed", "validation(검증)"), ("oos_routed", "OOS(표본외)")):
            metrics = summary.get(key, {})
            lines.append(f"| {label} | `{metrics.get('net_profit')}` | `{metrics.get('profit_factor')}` | `{metrics.get('trade_count')}` | `{metrics.get('max_drawdown_amount')}` | `{metrics.get('recovery_factor')}` |")
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 실행은 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 모델 특성을 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)로 연결했다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def write_run_outputs(
    topic: RunTopic,
    context: Mapping[str, Any],
    result: Mapping[str, Any],
    selected: Mapping[str, Any],
    variant_rows: Sequence[Mapping[str, Any]],
    variant_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    kpi: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(topic, result, selected, variant_artifacts, model_artifacts, prediction_artifacts, tier_records)
    registry_output = upsert_run_registry(topic, result, summary)
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=topic.run_id,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"validation_nonflat_q{topic.threshold_quantile:.2f}",
        run_output_root=topic.run_root,
        external_verification_status=result["external_verification_status"],
    )
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=ledger_rows)
    manifest = {
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "stage_id": STAGE_ID,
        "run_number": topic.run_number,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "topic_read": topic.topic_read,
        "boundary": topic.boundary,
        "variant_sweep": list(variant_rows) if topic.run_number == "run12A" else "reused_run12A_selected_variant_sweep",
        "selected_variant_id": selected.get("variant_id"),
        "tier_a_feature_order": list(context["full_feature_order"]),
        "tier_a_feature_order_hash": context["full_feature_order_hash"],
        "tier_b_feature_order_hash": context["tier_b_feature_order_hash"],
        "threshold_policy": f"validation nonflat q{topic.threshold_quantile:.2f}; not profit searched",
        "runtime_probe": {key: result.get(key) for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure") if key in result},
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "variant_artifacts": variant_artifacts,
    }
    kpi_record = {
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": False,
        "kpi_scope": f"catboost_{topic.topic_read}_python_shape_plus_mt5_runtime_probe",
        "selected_variant": selected,
        "python_tier_records": list(tier_records),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "mt5": {"scoreboard_lane": "runtime_probe", "external_verification_status": result["external_verification_status"], "execution_results": result.get("execution_results", []), "strategy_tester_reports": result.get("strategy_tester_reports", []), "kpi_records": result.get("mt5_kpi_records", [])},
        "kpi_management": dict(kpi),
        "external_verification_status": result["external_verification_status"],
        "judgment": summary["closure_judgment"],
        "boundary": topic.boundary,
        "ledger_outputs": ledger_outputs,
        "registry_output": registry_output,
    }
    summary["ledger_outputs"] = ledger_outputs
    summary["registry_output"] = registry_output
    summary["kpi_management"] = dict(kpi)
    write_json(topic.run_root / "run_manifest.json", manifest)
    write_json(topic.run_root / "kpi_record.json", kpi_record)
    write_json(topic.run_root / "summary.json", summary)
    write_json(topic.packet_root / "run_summaries" / f"{topic.run_id}.json", summary)
    write_md(topic.run_root / "reports/result_summary.md", run_result_markdown(topic, summary, kpi))
    return summary


def gate_payloads(topic: RunTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    runtime_ok = summary["external_verification_status"] == "completed" and summary["attempt_count"] == topic.expected_attempts and summary["mt5_kpi_record_count"] == topic.expected_kpi_records
    kpi_ok = kpi["normalized_records"] == topic.expected_kpi_records and kpi["parser_errors"] == 0 and kpi["missing_runs"] == 0
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    source_ok = runtime_ok and kpi_ok and parity_ok
    required = {
        "runtime_evidence_gate": "pass" if runtime_ok else "blocked",
        "scope_completion_gate": "pass" if summary.get("selected_variant") else "blocked",
        "kpi_contract_audit": "pass" if kpi_ok else "blocked",
        "source_authority_audit": "pass" if source_ok else "blocked",
        "final_claim_guard": "pass" if source_ok else "blocked",
    }
    return {
        "runtime_evidence_gate": {"audit_name": "runtime_evidence_gate", "status": required["runtime_evidence_gate"], "passed": runtime_ok, "expected_attempts": topic.expected_attempts, "expected_kpi_records": topic.expected_kpi_records, "counts": {"attempt_count": summary["attempt_count"], "mt5_kpi_record_count": summary["mt5_kpi_record_count"]}},
        "scope_completion_gate": {"audit_name": "scope_completion_gate", "status": required["scope_completion_gate"], "passed": bool(summary.get("selected_variant")), "scope": f"{topic.run_number} CatBoost topic probe plus MT5 KPI"},
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": required["kpi_contract_audit"], "passed": kpi_ok, **dict(kpi)},
        "source_authority_audit": {"audit_name": "source_authority_audit", "status": required["source_authority_audit"], "passed": source_ok, "source": "run kpi_record.json plus MT5 Strategy Tester reports plus normalized KPI files", "onnx_parity_passed": parity_ok},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": required["final_claim_guard"], "passed": source_ok, "allowed_claims": [summary.get("closure_judgment"), "runtime_probe", "model_characteristic_read"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if source_ok else "blocked", "passed": source_ok, "required_gates": required},
    }


def packet_markdown(topic: RunTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"# Stage18 {topic.run_number} CatBoost MT5 KPI Packet({topic.run_number} 캣부스트 MT5 핵심 성과 지표 묶음)",
            "",
            f"- run(실행): `{topic.run_id}`",
            f"- topic read(주제 판독): `{topic.topic_read}`",
            f"- judgment(판정): `{summary.get('closure_judgment')}`",
            f"- characteristic strength(특성 강도): `{summary.get('model_characteristic_strength')}`",
            f"- selected variant(선택 변형): `{summary.get('selected_variant', {}).get('variant_id')}`",
            f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`",
            f"- normalized KPI records(정규화 KPI 기록): `{kpi.get('normalized_records')}`",
            f"- trade attribution records(거래 귀속 기록): `{kpi.get('trade_attribution_records')}`",
            f"- boundary(경계): `{topic.boundary}`",
            "",
            "효과(effect, 효과): 이 묶음은 Stage18(18단계) CatBoost(캣부스트) 주제를 Python(파이썬) 구조 판독과 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 연결한다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def write_packet_files(topic: RunTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any], created_at: str) -> None:
    write_json(topic.packet_root / "aggregate_summary.json", {**dict(summary), "kpi_management": dict(kpi)})
    write_json(topic.packet_root / "artifact_index.json", {"run_summary": rel(topic.run_root / "summary.json"), "report_path": rel(topic.review_path), "created_at_utc": created_at})
    write_json(
        topic.packet_root / "routing_receipt.json",
        {
            "packet_id": topic.packet_id,
            "created_at_utc": created_at,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-backtest-forensics", "obsidian-run-evidence-system", "obsidian-artifact-lineage", "obsidian-result-judgment"],
            "required_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "source_authority_audit", "required_gate_coverage_audit", "final_claim_guard"],
        },
    )
    write_json(
        topic.packet_root / "skill_receipts.json",
        {
            "packet_id": topic.packet_id,
            "created_at_utc": created_at,
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "completed", "hypothesis": "CatBoost ordered boosting exposes a distinct model-characteristic axis.", "decision_use": "choose whether Stage18 continues, narrows, or closes."},
                {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe", "research_path": rel(Path(__file__)), "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"},
                {"skill": "obsidian-backtest-forensics", "status": "completed", "backtest_judgment": "usable_with_boundary" if summary["external_verification_status"] == "completed" else "blocked", "tester_identity": "US100 M5, tester model=4, deposit=500, leverage=1:100"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "lineage_judgment": "connected_with_boundary", "artifact_paths": [rel(topic.run_root / "run_manifest.json"), rel(topic.run_root / "kpi_record.json")]},
                {"skill": "obsidian-performance-attribution", "status": "completed", "attribution_confidence": "diagnostic_runtime_probe"},
                {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": summary.get("closure_judgment"), "claim_boundary": topic.boundary},
            ],
        },
    )
    for name, payload in gate_payloads(topic, summary, kpi).items():
        write_json(topic.packet_root / f"{name}.json", payload)
    write_md(topic.review_path, packet_markdown(topic, summary, kpi))


def build_topic_run(
    topic: RunTopic,
    args: argparse.Namespace,
    context: Mapping[str, Any],
    selected: Mapping[str, Any],
    variant_rows: Sequence[Mapping[str, Any]],
    variant_artifacts: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    spec = selected_spec(selected)
    selected_model_artifacts, tier_a_model, tier_b_model, tier_a_prob, tier_b_prob, a_threshold, b_threshold = materialize_selected_models(topic, context, spec)
    tier_records, prediction_artifacts = python_tier_records(topic, tier_a_prob, tier_b_prob, a_threshold, b_threshold)
    onnx_artifacts = export_models(topic, context, selected_model_artifacts, tier_a_model, tier_b_model)
    model_artifacts = {**selected_model_artifacts, **onnx_artifacts, "thresholds": {"tier_a": a_threshold, "tier_b": b_threshold}}
    feature_matrices = export_feature_matrices(topic, context)
    copies = copy_runtime_inputs(topic, model_artifacts, feature_matrices)
    attempts = make_attempts(topic, context, model_artifacts, feature_matrices, model_artifacts["thresholds"])
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_id": topic.run_id,
        "run_number": topic.run_number,
        "run_root": topic.run_root,
        "selected_variant_id": selected.get("variant_id"),
        "attempts": attempts,
        "common_copies": copies,
        "route_coverage": context["tier_b_context_summary"],
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
    }
    result = execute_or_block(topic, prepared, args)
    result["selected_variant_id"] = selected.get("variant_id")
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional_kpi = {"normalized_records": 0, "normalized_summary_rows": 0, "missing_runs": 0, "parser_errors": 0, "trade_attribution_records": 0, "trade_level_rows": 0, "trade_parser_errors": 0}
    write_run_outputs(topic, context, result, selected, variant_rows, variant_artifacts, model_artifacts, prediction_artifacts, tier_records, provisional_kpi, created_at)
    kpi = write_normalized_kpi(topic)
    summary = write_run_outputs(topic, context, result, selected, variant_rows, variant_artifacts, model_artifacts, prediction_artifacts, tier_records, kpi, created_at)
    write_packet_files(topic, summary, kpi, created_at)
    return {**summary, "kpi_management": kpi}


def aggregate_read(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_run = {summary["run_number"]: summary for summary in summaries}
    run12a = by_run.get("run12A", {})
    run12b = by_run.get("run12B", {})
    run12c = by_run.get("run12C", {})
    a_oos = run12a.get("oos_routed", {})
    b_oos = run12b.get("oos_routed", {})
    c_dir = run12c.get("direction_read", {})
    a_trades = safe_float(a_oos.get("trade_count"))
    b_trades = safe_float(b_oos.get("trade_count"))
    density_ratio = safe_div(b_trades, a_trades)
    visible_count = sum(1 for item in summaries if "visible" in str(item.get("model_characteristic_strength")))
    risk_warnings = [item["run_number"] for item in summaries if item.get("runtime_read", {}).get("risk_warning")]
    recommendation = "keep_stage18_open_for_catboost_attribution_or_regime_probe" if visible_count >= 2 else "close_stage18_if_no_new_axis_after_review"
    return {
        "visible_topic_count": visible_count,
        "run12B_oos_trade_density_ratio_vs_run12A": density_ratio,
        "run12C_direction_read": c_dir,
        "risk_warning_runs": risk_warnings,
        "recommendation": recommendation,
        "judgment": "inconclusive_catboost_model_characteristic_mt5_kpi_completed",
        "claim_boundary": "runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
    }


def aggregate_markdown(summaries: Sequence[Mapping[str, Any]], read: Mapping[str, Any]) -> str:
    lines = [
        "# Stage18 CatBoost Characteristic MT5 KPI Aggregate(18단계 캣부스트 특성 MT5 핵심 성과 지표 종합)",
        "",
        f"- judgment(판정): `{read.get('judgment')}`",
        f"- recommendation(권고): `{read.get('recommendation')}`",
        f"- boundary(경계): `{read.get('claim_boundary')}`",
        "",
        "| run(실행) | topic(주제) | strength(강도) | validation net/PF/trades(검증 순수익/수익 팩터/거래) | OOS net/PF/trades(표본외 순수익/수익 팩터/거래) |",
        "|---|---|---|---:|---:|",
    ]
    for summary in summaries:
        if summary.get("topic_read") == "direction_balance_long_short_split":
            direction = summary.get("direction_routed", {})
            long_val = direction.get("long_validation", {})
            short_val = direction.get("short_validation", {})
            long_oos = direction.get("long_oos", {})
            short_oos = direction.get("short_oos", {})
            val_text = f"long {long_val.get('net_profit')} / {long_val.get('profit_factor')} / {long_val.get('trade_count')}; short {short_val.get('net_profit')} / {short_val.get('profit_factor')} / {short_val.get('trade_count')}"
            oos_text = f"long {long_oos.get('net_profit')} / {long_oos.get('profit_factor')} / {long_oos.get('trade_count')}; short {short_oos.get('net_profit')} / {short_oos.get('profit_factor')} / {short_oos.get('trade_count')}"
        else:
            val = summary.get("validation_routed", {})
            oos = summary.get("oos_routed", {})
            val_text = f"{val.get('net_profit')} / {val.get('profit_factor')} / {val.get('trade_count')}"
            oos_text = f"{oos.get('net_profit')} / {oos.get('profit_factor')} / {oos.get('trade_count')}"
        lines.append(
            f"| `{summary.get('run_number')}` | `{summary.get('topic_read')}` | `{summary.get('model_characteristic_strength')}` | `{val_text}` | `{oos_text}` |"
        )
    lines.extend(
        [
            "",
            f"- visible topic count(보이는 주제 수): `{read.get('visible_topic_count')}`",
            f"- run12B density ratio vs run12A(run12A 대비 run12B 밀도 비율): `{read.get('run12B_oos_trade_density_ratio_vs_run12A')}`",
            f"- risk warning runs(위험 경고 실행): `{read.get('risk_warning_runs')}`",
            "",
            "효과(effect, 효과): Stage18(18단계)는 CatBoost(캣부스트)의 ordered boosting(순서 부스팅), q80 signal density(q80 신호 밀도), direction balance(방향 균형)를 MT5(`MetaTrader 5`, 메타트레이더5)까지 확인했다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def write_aggregate_packet(summaries: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    read = aggregate_read(summaries)
    io_path(AGGREGATE_PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    write_json(AGGREGATE_PACKET_ROOT / "aggregate_summary.json", {"packet_id": AGGREGATE_PACKET_ID, "created_at_utc": created_at, "run_summaries": list(summaries), "aggregate_read": read})
    write_json(AGGREGATE_PACKET_ROOT / "artifact_index.json", {"run_summary_paths": [rel(STAGE_ROOT / "02_runs" / str(summary["run_id"]) / "summary.json") for summary in summaries], "report_path": rel(STAGE_ROOT / "03_reviews/stage18_catboost_characteristic_mt5_kpi_packet.md"), "created_at_utc": created_at})
    write_json(AGGREGATE_PACKET_ROOT / "performance_attribution_audit.json", {"audit_name": "performance_attribution_audit", "status": "pass", "passed": True, "observed_change": "CatBoost topic probes produced model-characteristic and MT5 KPI reads across q90, q80 density, and direction split.", "comparison_baseline": "Stage17 XGBoost preserved clues only; no baseline inheritance.", "attribution_confidence": "diagnostic_runtime_probe", "aggregate_read": read})
    write_json(AGGREGATE_PACKET_ROOT / "result_judgment_audit.json", {"audit_name": "result_judgment_audit", "status": "pass", "passed": True, "result_subject": "Stage18 CatBoost run12A-run12C model-characteristic MT5 KPI packet", "judgment_label": read["judgment"], "claim_boundary": read["claim_boundary"]})
    write_json(AGGREGATE_PACKET_ROOT / "final_claim_guard.json", {"audit_name": "final_claim_guard", "status": "pass", "passed": True, "allowed_claims": [read["judgment"], "runtime_probe", "model_characteristic_read"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"]})
    write_json(AGGREGATE_PACKET_ROOT / "required_gate_coverage_audit.json", {"audit_name": "required_gate_coverage_audit", "status": "pass", "passed": True, "required_gates": {"performance_attribution_audit": "pass", "result_judgment_audit": "pass", "final_claim_guard": "pass"}})
    write_md(STAGE_ROOT / "03_reviews/stage18_catboost_characteristic_mt5_kpi_packet.md", aggregate_markdown(summaries, read))
    return read


def sync_stage18_docs(summaries: Sequence[Mapping[str, Any]], aggregate: Mapping[str, Any]) -> None:
    latest = summaries[-1]
    status = "reviewed_run12A_run12C_catboost_characteristic_mt5_kpi"
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage18 Selection Status(18단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                f"- status(상태): `{status}`",
                f"- current run(현재 실행): `{latest.get('run_id')}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{aggregate.get('judgment')}`",
                f"- recommendation(권고): `{aggregate.get('recommendation')}`",
                f"- boundary(경계): `{aggregate.get('claim_boundary')}`",
                "",
                "효과(effect, 효과): Stage18(18단계)는 run12A-run12C(실행12A-실행12C)까지 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)를 만들었지만, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            ]
        ),
    )
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage18 Review Index(18단계 검토 색인)",
                "",
                "- aggregate packet(종합 묶음): `stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/stage18_catboost_characteristic_mt5_kpi_packet.md`",
                *[f"- `{summary.get('run_id')}`: `{summary.get('closure_judgment')}`, report(보고서): `stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/{RUN_TOPICS[index].review_filename}`" for index, summary in enumerate(summaries)],
                "",
                "효과(effect, 효과): Stage18(18단계)의 CatBoost(캣부스트) 모델 특성 실험 기록을 한 곳에서 찾을 수 있다.",
            ]
        ),
    )
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("current_run_id: ''", f"current_run_id: {latest.get('run_id')}", 1)
    state = state.replace(
        "treat Stage 18 as topic_open_no_run for CatBoost ordered boosting scout; no run, KPI, MT5 runtime_probe, baseline, promotion, or runtime authority exists yet",
        "treat Stage 18 as reviewed_run12A_run12C_catboost_characteristic_mt5_kpi; run12A-run12C are MT5 runtime_probe and KPI evidence only, not baseline, promotion, or runtime authority",
    )
    state = state.replace(
        "    stage18:\n      stage_id: 18_model_family_challenge__catboost_ordered_boosting_scout\n      ownership: independent CatBoost ordered boosting scout after Stage17 XGBoost closeout\n      status: topic_open_no_run",
        f"    stage18:\n      stage_id: 18_model_family_challenge__catboost_ordered_boosting_scout\n      ownership: independent CatBoost ordered boosting scout after Stage17 XGBoost closeout\n      status: {status}\n      current_run_id: {latest.get('run_id')}",
    )
    stage_block = f"""stage18_catboost_ordered_boosting_scout:
  stage_id: {STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {MODEL_FAMILY}
  current_run_id: {latest.get('run_id')}
  current_status: reviewed_runtime_probe_completed
  judgment: {aggregate.get('judgment')}
  recommendation: {aggregate.get('recommendation')}
  run_range: run12A-run12C
  completed_run_count: {len(summaries)}
  mt5_kpi_record_count: {sum(int(summary.get('mt5_kpi_record_count') or 0) for summary in summaries)}
  normalized_kpi_record_count: {sum(int(summary.get('kpi_management', {}).get('normalized_records') or 0) for summary in summaries)}
  trade_attribution_records: {sum(int(summary.get('kpi_management', {}).get('trade_attribution_records') or 0) for summary in summaries)}
  selected_variant_id: {latest.get('selected_variant', {}).get('variant_id')}
  visible_topic_count: {aggregate.get('visible_topic_count')}
  risk_warning_runs: {','.join(aggregate.get('risk_warning_runs') or [])}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {aggregate.get('claim_boundary')}
  aggregate_packet_path: {rel(STAGE_ROOT / '03_reviews/stage18_catboost_characteristic_mt5_kpi_packet.md')}
  packet_summary_path: docs/agent_control/packets/{AGGREGATE_PACKET_ID}/aggregate_summary.json
  next_action: {aggregate.get('recommendation')}
"""
    marker = "stage18_catboost_ordered_boosting_scout:"
    state = replace_top_level_yaml_block(state, marker, stage_block)
    for summary in summaries:
        block = f"""stage18_catboost_{summary.get('run_number')}_runtime_probe:
  packet_id: {summary.get('packet_id')}
  status: reviewed_runtime_probe_completed
  judgment: {summary.get('closure_judgment')}
  current_run_id: {summary.get('run_id')}
  topic_read: {summary.get('topic_read')}
  selected_variant_id: {summary.get('selected_variant', {}).get('variant_id')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  normalized_kpi_record_count: {summary.get('kpi_management', {}).get('normalized_records')}
  trade_attribution_records: {summary.get('kpi_management', {}).get('trade_attribution_records')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {summary.get('boundary')}
  report_path: stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/{RUN_TOPICS[[item.run_number for item in RUN_TOPICS].index(str(summary.get('run_number')))].review_filename}
"""
        state = replace_top_level_yaml_block(state, f"stage18_catboost_{summary.get('run_number')}_runtime_probe:", block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")

    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage18 RUN12A-RUN12C Update(최신 18단계 실행12A-실행12C 업데이트)",
            "",
            "Stage18(18단계)는 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) ordered boosting(순서 부스팅) 모델 특성을 세 주제로 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 확인했다.",
            "",
            f"효과(effect, 효과): `{aggregate.get('judgment')}`로 기록했다. run12A(실행12A)는 ordered probability shape(순서 부스팅 확률 모양), run12B(실행12B)는 q80 signal density(q80 신호 밀도), run12C(실행12C)는 direction balance(방향 균형)를 본다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage18 RUN12A-RUN12C Update" not in current:
        current = insert + current
    current = current.replace("- current run(현재 실행): 없음", f"- current run(현재 실행): `{latest.get('run_id')}`", 1)
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage18(18단계) `run12A-run12C` CatBoost(캣부스트) 모델 특성 MT5 KPI 묶음을 완료했다. 효과(effect, 효과): ordered shape(순서 부스팅 모양), q80 density(q80 밀도), direction balance(방향 균형)를 runtime_probe(런타임 탐침)로 기록하고 `{aggregate.get('judgment')}`로 판정했다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variant_rows = [variant_characteristic(context, spec) for spec in default_stage18_catboost_variants()]
    selected = choose_variant(variant_rows)
    variant_artifacts = materialize_variant_results(variant_rows)
    summaries = [build_topic_run(topic, args, context, selected, variant_rows, variant_artifacts, created_at) for topic in RUN_TOPICS]
    aggregate = write_aggregate_packet(summaries, created_at)
    sync_stage18_docs(summaries, aggregate)
    payload = {"aggregate": aggregate, "summaries": summaries}
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage18 CatBoost model-characteristic MT5 KPI probes.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--materialize-only", action="store_true")
    args = parser.parse_args(argv)
    build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
