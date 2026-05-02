from __future__ import annotations

import json
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from pandas.errors import ParserWarning

from foundation.control_plane.ledger import io_path, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    ROOT,
    TRAINING_SUMMARY_PATH,
    attempt_payload,
    common_run_root,
    copy_to_common,
    split_dates_from_frame,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.mlp_characteristics import MlpVariantSpec
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
)
from foundation.mt5 import runtime_support as mt5


@dataclass(frozen=True)
class Stage13HandoffConfig:
    stage_number: int
    run_id: str
    exploration_label: str
    run_root: Path
    no_trade_threshold: float = 1.01
    min_margin: float = 0.0
    max_hold_bars: int = 9


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    from foundation.control_plane.ledger import json_ready

    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    tier_a_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, tier_a_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "tier_a_feature_order": tier_a_feature_order,
        "tier_a_feature_order_hash": ordered_hash(tier_a_feature_order),
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_feature_order_hash": ordered_hash(tier_b_feature_order),
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }


def materialize_models(
    *,
    config: Stage13HandoffConfig,
    spec: MlpVariantSpec,
    tier_a_model: Any,
    tier_b_model: Any,
    tier_a_frame: pd.DataFrame,
    tier_b_training_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
    artifact_prefix: str,
) -> dict[str, Any]:
    model_root = config.run_root / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_joblib = model_root / f"{artifact_prefix}_tier_a_mlp_58.joblib"
    tier_b_joblib = model_root / f"{artifact_prefix}_tier_b_mlp_core42.joblib"
    tier_a_onnx = model_root / f"{artifact_prefix}_tier_a_mlp_58.onnx"
    tier_b_onnx = model_root / f"{artifact_prefix}_tier_b_mlp_core42.onnx"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model,
        tier_a_onnx,
        feature_count=len(tier_a_feature_order),
    )
    tier_b_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model,
        tier_b_onnx,
        feature_count=len(tier_b_feature_order),
    )
    tier_a_sample = (
        tier_a_frame.loc[tier_a_frame["split"].astype(str).eq("validation"), list(tier_a_feature_order)]
        .head(128)
        .to_numpy(dtype="float64", copy=False)
    )
    tier_b_sample = (
        tier_b_training_frame.loc[
            tier_b_training_frame["split"].astype(str).eq("validation"),
            list(tier_b_feature_order),
        ]
        .head(128)
        .to_numpy(dtype="float64", copy=False)
    )
    return {
        "spec": spec.payload(),
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
        "tier_a_onnx": tier_a_export,
        "tier_b_onnx": tier_b_export,
        "onnx_parity": {
            "tier_a": check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, tier_a_sample),
            "tier_b": check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, tier_b_sample),
        },
    }


def export_feature_matrices(config: Stage13HandoffConfig, context: Mapping[str, Any]) -> dict[str, Any]:
    feature_root = config.run_root / "features"
    io_path(feature_root).mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[
            context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)
        ].copy()
        tier_a_path = feature_root / f"tier_a_{runtime_split}_feature_matrix.csv"
        tier_b_path = feature_root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv"
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            context["tier_a_feature_order"],
            tier_a_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            context["tier_b_feature_order"],
            tier_b_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(
    *,
    config: Stage13HandoffConfig,
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
) -> list[dict[str, Any]]:
    common = common_run_root(config.stage_number, config.run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        source = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(source, f"{common}/models/{source.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        source = ROOT / matrix["path"]
        copies.append(copy_to_common(source, f"{common}/features/{source.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_no_trade_attempts(
    *,
    config: Stage13HandoffConfig,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    model_id_suffix: str,
    record_prefix_suffix: str,
) -> list[dict[str, Any]]:
    return make_threshold_attempts(
        config=config,
        context=context,
        model_artifacts=model_artifacts,
        feature_matrices=feature_matrices,
        model_id_suffix=model_id_suffix,
        record_prefix_suffix=record_prefix_suffix,
        tier_a_threshold=float(config.no_trade_threshold),
        tier_b_threshold=float(config.no_trade_threshold),
    )


def make_threshold_attempts(
    *,
    config: Stage13HandoffConfig,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    model_id_suffix: str,
    record_prefix_suffix: str,
    tier_a_threshold: float,
    tier_b_threshold: float,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(config.stage_number, config.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": config.run_root,
            "run_id": config.run_id,
            "stage_number": config.stage_number,
            "exploration_label": config.exploration_label,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": config.max_hold_bars,
            "common_root": common,
        }
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_a_{record_prefix_suffix}_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{config.run_id}_tier_a_{model_id_suffix}",
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(context["tier_a_feature_order"]),
                feature_order_hash=context["tier_a_feature_order_hash"],
                short_threshold=tier_a_threshold,
                long_threshold=tier_a_threshold,
                min_margin=config.min_margin,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix=f"mt5_tier_a_{record_prefix_suffix}",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_{record_prefix_suffix}_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{config.run_id}_tier_b_{model_id_suffix}",
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=len(context["tier_b_feature_order"]),
                feature_order_hash=context["tier_b_feature_order_hash"],
                short_threshold=tier_b_threshold,
                long_threshold=tier_b_threshold,
                min_margin=config.min_margin,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix=f"mt5_tier_b_fallback_{record_prefix_suffix}",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{record_prefix_suffix}_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{config.run_id}_tier_a_{model_id_suffix}",
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(context["tier_a_feature_order"]),
                feature_order_hash=context["tier_a_feature_order_hash"],
                short_threshold=tier_a_threshold,
                long_threshold=tier_a_threshold,
                min_margin=config.min_margin,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix=f"mt5_routed_{record_prefix_suffix}",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{config.run_id}_tier_b_{model_id_suffix}",
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=len(context["tier_b_feature_order"]),
                fallback_feature_order_hash=context["tier_b_feature_order_hash"],
                fallback_short_threshold=tier_b_threshold,
                fallback_long_threshold=tier_b_threshold,
                fallback_min_margin=config.min_margin,
                fallback_invert_signal=False,
            )
        )
    return attempts


def runtime_probability_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for execution in result.get("execution_results", []):
        runtime = execution.get("runtime_outputs", {})
        telemetry_path = runtime.get("telemetry_path")
        if not telemetry_path or not Path(str(telemetry_path)).exists():
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ParserWarning)
            frame = pd.read_csv(io_path(Path(str(telemetry_path))), index_col=False)
        cycle = frame.loc[frame["record_type"].astype(str).eq("cycle")].copy()
        if "feature_ready" in cycle:
            cycle = cycle.loc[_truthy_series(cycle["feature_ready"])]
        if "model_ok" in cycle:
            cycle = cycle.loc[_truthy_series(cycle["model_ok"])]
        probs = cycle.loc[:, ["p_short", "p_flat", "p_long"]].apply(pd.to_numeric, errors="coerce").dropna()
        if probs.empty:
            continue
        values = probs.to_numpy(dtype="float64", copy=False)
        clipped = np.clip(values, 1e-12, 1.0)
        entropy = -(clipped * np.log(clipped)).sum(axis=1)
        rows.append(
            {
                "attempt_name": execution.get("attempt_name"),
                "split": execution.get("split"),
                "tier": execution.get("tier"),
                "route_role": execution.get("attempt_role"),
                "rows": int(len(probs)),
                "mean_p_short": float(probs["p_short"].mean()),
                "mean_p_flat": float(probs["p_flat"].mean()),
                "mean_p_long": float(probs["p_long"].mean()),
                "mean_entropy": float(entropy.mean()),
                "mean_max_probability": float(values.max(axis=1).mean()),
                "row_sum_max_abs_error": float(np.abs(values.sum(axis=1) - 1.0).max()),
                "telemetry_path": str(telemetry_path),
            }
        )
    return rows


def write_runtime_probability_artifacts(
    *,
    result: Mapping[str, Any],
    output_root: Path,
    boundary: str,
) -> dict[str, Any]:
    rows = runtime_probability_rows(result)
    io_path(output_root).mkdir(parents=True, exist_ok=True)
    csv_path = output_root / "runtime_probability_summary.csv"
    json_path = output_root / "runtime_probability_summary.json"
    pd.DataFrame(rows).to_csv(io_path(csv_path), index=False, encoding="utf-8")
    payload = {"rows": rows, "boundary": boundary}
    write_json(json_path, payload)
    return {
        "runtime_probability_summary_csv": {"path": rel(csv_path), "rows": len(rows), "sha256": sha256_file_lf_normalized(csv_path)},
        "runtime_probability_summary_json": {"path": rel(json_path), "rows": len(rows), "sha256": sha256_file_lf_normalized(json_path)},
        "payload": payload,
    }


def _truthy_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin({"true", "1", "yes"})
