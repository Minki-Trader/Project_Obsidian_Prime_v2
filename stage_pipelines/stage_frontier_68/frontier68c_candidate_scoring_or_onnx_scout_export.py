from __future__ import annotations

import json
import math
import re
import sys
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone

warnings.filterwarnings(
    "ignore",
    message="X does not have valid feature names, but SimpleImputer was fitted with feature names",
    category=UserWarning,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_sklearn_to_onnx_zipmap_disabled
from stage_pipelines.stage_frontier_68 import frontier68b_runtime_lifecycle_proxy_broad_sweep as f68b
from stage_pipelines.stage_frontier_68.frontier68a_bridge_feasibility_and_label_design import (
    STAGE_ID,
    ordered_hash,
    rel,
    sha256_file,
    upsert_ledger,
    write_csv,
    write_json,
    write_md,
)


RUN_ID = "frontier68C_candidate_scoring_or_onnx_scout_export_v1"
PARENT_RUN_ID = f68b.RUN_ID
NEXT_RUN_ID = "frontier68D_mt5_runtime_probe_candidate_axis_materialization_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"

F68B_TOP_CANDIDATES = REVIEWS_ROOT / "f68b_top_candidates_review.json"
F68B_REPORT = REVIEWS_ROOT / "frontier68B_proxy_broad_sweep_report.md"
GROK_RECEIPT = (
    ROOT
    / "docs/agent_control/grok_reviews/2026-06-17_f68c_pre_onnx_candidate_axis_review/f68c_pre_onnx_candidate_axis_receipt.md"
)
GROK_CLEAN_OUTPUT = (
    ROOT
    / "docs/agent_control/grok_reviews/2026-06-17_f68c_pre_onnx_candidate_axis_review/outputs/clean_output.md"
)

CLAIM_BOUNDARY = (
    "onnx_scout_export_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


@dataclass(frozen=True)
class CandidateAxis:
    axis_id: str
    candidate_id: str
    role: str
    target_prefix: str
    feature_prefix: str
    model_prefix: str
    threshold_quantile: float
    cooldown_bars: int
    side_prefix: str
    exit_prefix: str
    priority: int


CANDIDATE_AXES: tuple[CandidateAxis, ...] = (
    CandidateAxis(
        axis_id="density_axis",
        candidate_id="f68b_23f4d4607a78",
        role="density_axis_trade_count_ok_pf_weak",
        target_prefix="h2_ddp03_min1p5",
        feature_prefix="full58",
        model_prefix="extra_trees_shallow",
        threshold_quantile=0.30,
        cooldown_bars=1,
        side_prefix="both",
        exit_prefix="close_horizon",
        priority=1,
    ),
    CandidateAxis(
        axis_id="pf_axis",
        candidate_id="f68b_3481a04983ee",
        role="pf_axis_strong_pf_density_gap",
        target_prefix="h6_ddp04_min3",
        feature_prefix="no_mega_top3",
        model_prefix="extra_trees_shallow",
        threshold_quantile=0.975,
        cooldown_bars=0,
        side_prefix="long_only",
        exit_prefix="atr_sltp_conservative",
        priority=2,
    ),
    CandidateAxis(
        axis_id="low_dd_density_axis",
        candidate_id="f68b_547ac8b4ead1",
        role="low_dd_density_axis_hgb_converter_conditional",
        target_prefix="h2_ddp03_min1p5",
        feature_prefix="no_mega_top3",
        model_prefix="hgb_small",
        threshold_quantile=0.70,
        cooldown_bars=1,
        side_prefix="both",
        exit_prefix="atr_sltp_conservative",
        priority=3,
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def fmt(value: Any, digits: int = 6) -> str:
    number = safe_float(value, default=float("nan"))
    if not math.isfinite(number):
        return ""
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def slug(text: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return value or "item"


def match_prefix(items: Sequence[Any], attr: str, prefix: str) -> Any:
    matches = [item for item in items if str(getattr(item, attr)).startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"prefix match failed for {attr}={prefix}: {len(matches)} matches")
    return matches[0]


def unique_by_prefix(values: Sequence[str], prefix: str) -> str:
    matches = sorted({str(value) for value in values if str(value).startswith(prefix)})
    if len(matches) != 1:
        raise RuntimeError(f"prefix match failed for value={prefix}: {len(matches)} matches")
    return matches[0]


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def artifact_identity(path: Path, rows: int | None = None) -> dict[str, Any]:
    stat = io_path(path).stat()
    return {
        "path": rel(path),
        "sha256": sha256_file(path),
        "bytes": int(stat.st_size),
        "rows": rows,
    }


def compact_error(exc: Exception, limit: int = 420) -> str:
    text = f"{type(exc).__name__}: {exc}"
    text = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    if "Unable to create node 'TreeEnsembleClassifier'" in text:
        return (
            "ValueError: skl2onnx TreeEnsembleClassifier conversion failed for this HGB pipeline; "
            "preserved clue only(HGB 파이프라인 변환 실패, 보존 단서 전용)."
        )
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "...[truncated]"


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, REVIEWS_ROOT, STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def f68b_reference_by_candidate() -> dict[str, Mapping[str, Any]]:
    payload = read_json(F68B_TOP_CANDIDATES)
    rows = list(payload.get("top_candidates", []))
    stats = dict(payload.get("candidate_group_stats", {}))
    for key in ("best_density_clue", "best_pf_clue", "best_low_dd_density_clue"):
        value = stats.get(key)
        if value:
            rows.append(value)
    return {str(row.get("candidate_id")): row for row in rows if row.get("candidate_id")}


def build_candidate_context(
    axis: CandidateAxis,
    model_input: pd.DataFrame,
    raw: pd.DataFrame,
    raw_positions: np.ndarray,
    reference: Mapping[str, Any],
) -> dict[str, Any]:
    target = match_prefix(f68b.target_specs(), "target_id", axis.target_prefix)
    feature_set = match_prefix(f68b.feature_sets(model_input), "feature_set_id", axis.feature_prefix)
    model_spec = match_prefix(f68b.model_specs(), "model_id", axis.model_prefix)
    side_policy = unique_by_prefix([spec.side_policy for spec in f68b.eval_specs()], axis.side_prefix)
    exit_mode = unique_by_prefix([spec.exit_mode for spec in f68b.eval_specs()], axis.exit_prefix)
    candidate_id_check = "f68b_" + f68b.stable_id(
        [
            target.target_id,
            feature_set.feature_set_id,
            model_spec.model_id,
            axis.threshold_quantile,
            axis.cooldown_bars,
            side_policy,
            exit_mode,
        ]
    )
    frame = f68b.future_path_payload(model_input, raw, raw_positions, target)
    estimator = clone(model_spec.estimator)
    train_mask = frame["split"].eq("train")
    feature_columns = list(feature_set.columns)
    estimator.fit(frame.loc[train_mask, feature_columns], frame.loc[train_mask, "target_class"])
    classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
    _, train_edge = f68b.side_and_edge(estimator.predict_proba(frame.loc[train_mask, feature_columns]), classes)
    train_edges = train_edge[train_edge > -100.0]
    if len(train_edges) == 0:
        train_edges = np.array([999.0])
    edge_threshold = float(np.quantile(train_edges, axis.threshold_quantile))
    kpi_rows = [
        split_metrics(
            axis=axis,
            frame=frame,
            estimator=estimator,
            classes=classes,
            split_name=split_name,
            feature_columns=feature_columns,
            side_policy=side_policy,
            exit_mode=exit_mode,
            edge_threshold=edge_threshold,
            horizon_bars=int(target.horizon_bars),
        )
        for split_name in ("train", "validation", "oos")
    ]
    reference_diff = reference_metric_diff(kpi_rows, reference)
    return {
        "axis": axis,
        "target": target,
        "feature_set": feature_set,
        "model_spec": model_spec,
        "side_policy": side_policy,
        "exit_mode": exit_mode,
        "candidate_id_check": candidate_id_check,
        "candidate_id_match": bool(candidate_id_check == axis.candidate_id),
        "frame": frame,
        "estimator": estimator,
        "classes": classes,
        "feature_columns": feature_columns,
        "feature_order_hash": ordered_hash(feature_columns),
        "edge_threshold_from_train": edge_threshold,
        "kpi_rows": kpi_rows,
        "reference_diff": reference_diff,
    }


def split_metrics(
    *,
    axis: CandidateAxis,
    frame: pd.DataFrame,
    estimator: Any,
    classes: Sequence[int],
    split_name: str,
    feature_columns: Sequence[str],
    side_policy: str,
    exit_mode: str,
    edge_threshold: float,
    horizon_bars: int,
) -> dict[str, Any]:
    split_frame = frame.loc[frame["split"].eq(split_name)].copy().reset_index(drop=True)
    proba = estimator.predict_proba(split_frame.loc[:, list(feature_columns)])
    side, edge = f68b.side_and_edge(proba, classes)
    side = f68b.apply_side_policy(side, side_policy)
    signal = (side != 1) & (edge >= edge_threshold)
    profit = f68b.profit_for_side(split_frame, side, exit_mode)
    chosen = f68b.non_overlap_indices(signal, horizon_bars, axis.cooldown_bars)
    metrics = f68b.proxy_kpi(profit[chosen], split_frame.loc[chosen, "timestamp"] if chosen else split_frame["timestamp"].iloc[:0])
    long_count = int((side[chosen] == 2).sum()) if chosen else 0
    short_count = int((side[chosen] == 0).sum()) if chosen else 0
    return {
        "candidate_id": axis.candidate_id,
        "axis_id": axis.axis_id,
        "split": split_name,
        "signal_count": int(signal.sum()),
        "trade_count": metrics["trade_count"],
        "trades_per_day": metrics["trades_per_day"],
        "net_profit_proxy_points": metrics["net_profit"],
        "gross_profit_proxy_points": metrics["gross_profit"],
        "gross_loss_proxy_points": metrics["gross_loss"],
        "profit_factor": metrics["profit_factor"],
        "expectancy_proxy_points": metrics["expectancy"],
        "win_rate_percent": metrics["win_rate_percent"],
        "average_win_proxy_points": metrics["average_win"],
        "average_loss_proxy_points": metrics["average_loss"],
        "payoff_ratio": metrics["payoff_ratio"],
        "max_drawdown_proxy_points": metrics["max_drawdown"],
        "proxy_dd_percent_on_10000_points": metrics["proxy_dd_percent_on_10000"],
        "recovery_factor": metrics["recovery_factor"],
        "max_consecutive_loss": metrics["max_consecutive_loss"],
        "long_trade_count": long_count,
        "short_trade_count": short_count,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def reference_metric_diff(kpi_rows: Sequence[Mapping[str, Any]], reference: Mapping[str, Any]) -> dict[str, Any]:
    rows_by_split = {str(row["split"]): row for row in kpi_rows}
    fields = {
        "validation_net": ("validation", "net_profit_proxy_points"),
        "validation_pf": ("validation", "profit_factor"),
        "validation_tpd": ("validation", "trades_per_day"),
        "validation_dd_pct_proxy": ("validation", "proxy_dd_percent_on_10000_points"),
        "oos_net": ("oos", "net_profit_proxy_points"),
        "oos_pf": ("oos", "profit_factor"),
        "oos_tpd": ("oos", "trades_per_day"),
        "oos_dd_pct_proxy": ("oos", "proxy_dd_percent_on_10000_points"),
    }
    diffs: dict[str, Any] = {}
    for ref_key, (split, local_key) in fields.items():
        expected = safe_float(reference.get(ref_key), default=float("nan"))
        actual = safe_float(rows_by_split.get(split, {}).get(local_key), default=float("nan"))
        diffs[ref_key + "_abs_diff"] = abs(actual - expected) if math.isfinite(expected) and math.isfinite(actual) else None
    diffs["max_abs_diff"] = max([value for value in diffs.values() if value is not None], default=None)
    diffs["passed"] = bool(safe_float(diffs.get("max_abs_diff"), default=999.0) <= 1e-6)
    return diffs


def export_candidate(context: Mapping[str, Any]) -> dict[str, Any]:
    axis: CandidateAxis = context["axis"]
    candidate_id = axis.candidate_id
    feature_columns = list(context["feature_columns"])
    estimator = context["estimator"]
    model_path = MODEL_ROOT / f"{candidate_id}.joblib"
    onnx_path = MODEL_ROOT / f"{candidate_id}.onnx"
    feature_order_path = MODEL_ROOT / f"{candidate_id}_feature_order.txt"
    io_path(feature_order_path).write_text("\n".join(feature_columns) + "\n", encoding="utf-8")
    joblib.dump(estimator, io_path(model_path))
    try:
        export_meta = export_sklearn_to_onnx_zipmap_disabled(
            estimator,
            onnx_path,
            feature_count=len(feature_columns),
            target_opset=12,
            drop_label_output=True,
        )
        probability_parity = probability_parity_rows(context, onnx_path)
        signal_parity = signal_parity_rows(context, onnx_path)
        export_status = "exported_onnx_parity_passed" if all(row.get("passed") for row in probability_parity) else "exported_onnx_parity_failed"
        return {
            "candidate_id": candidate_id,
            "axis_id": axis.axis_id,
            "export_status": export_status,
            "export_error": "",
            "model_path": rel(model_path),
            "model_sha256": sha256_file(model_path),
            "onnx_path": rel(onnx_path),
            "onnx_sha256": sha256_file(onnx_path),
            "feature_order_path": rel(feature_order_path),
            "feature_order_sha256": sha256_file(feature_order_path),
            "onnx_export": export_meta,
            "probability_parity": probability_parity,
            "signal_parity": signal_parity,
        }
    except Exception as exc:  # noqa: BLE001 - export failure is recorded as evidence.
        return {
            "candidate_id": candidate_id,
            "axis_id": axis.axis_id,
            "export_status": "export_failed_preserved_clue",
            "export_error": compact_error(exc),
            "model_path": rel(model_path),
            "model_sha256": sha256_file(model_path),
            "onnx_path": rel(onnx_path),
            "onnx_sha256": sha256_file(onnx_path),
            "feature_order_path": rel(feature_order_path),
            "feature_order_sha256": sha256_file(feature_order_path),
            "onnx_export": {},
            "probability_parity": [],
            "signal_parity": [],
        }


def probability_parity_rows(context: Mapping[str, Any], onnx_path: Path) -> list[dict[str, Any]]:
    frame: pd.DataFrame = context["frame"]
    feature_columns = list(context["feature_columns"])
    estimator = context["estimator"]
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].eq(split), feature_columns].head(2048)
        values = split_frame.to_numpy(dtype="float64")
        parity = check_onnxruntime_probability_parity(estimator, onnx_path, values, tolerance=1e-5)
        rows.append({"candidate_id": context["axis"].candidate_id, "split": split, **parity})
    return rows


def onnx_probabilities(onnx_path: Path, values: np.ndarray) -> np.ndarray:
    import onnxruntime as ort

    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: np.asarray(values, dtype="float32")})
    candidates = [output for output in outputs if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == 3]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one probability output, got {[getattr(output, 'shape', None) for output in outputs]}")
    return np.asarray(candidates[0], dtype="float64")


def signal_parity_rows(context: Mapping[str, Any], onnx_path: Path) -> list[dict[str, Any]]:
    frame: pd.DataFrame = context["frame"]
    feature_columns = list(context["feature_columns"])
    estimator = context["estimator"]
    classes = list(context["classes"])
    axis: CandidateAxis = context["axis"]
    side_policy = str(context["side_policy"])
    threshold = float(context["edge_threshold_from_train"])
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        split_frame = frame.loc[frame["split"].eq(split)].copy().reset_index(drop=True)
        values = split_frame.loc[:, feature_columns].to_numpy(dtype="float64")
        sklearn_proba = np.asarray(estimator.predict_proba(split_frame.loc[:, feature_columns]), dtype="float64")
        onnx_proba = onnx_probabilities(onnx_path, values)
        sklearn_side, sklearn_edge = f68b.side_and_edge(sklearn_proba, classes)
        onnx_side, onnx_edge = f68b.side_and_edge(onnx_proba, classes)
        sklearn_side = f68b.apply_side_policy(sklearn_side, side_policy)
        onnx_side = f68b.apply_side_policy(onnx_side, side_policy)
        sklearn_signal = (sklearn_side != 1) & (sklearn_edge >= threshold)
        onnx_signal = (onnx_side != 1) & (onnx_edge >= threshold)
        signal_mismatch = sklearn_signal != onnx_signal
        side_mismatch_on_signal = (sklearn_side != onnx_side) & (sklearn_signal | onnx_signal)
        edge_diff = np.abs(onnx_edge - sklearn_edge)
        rows.append(
            {
                "candidate_id": axis.candidate_id,
                "split": split,
                "rows": int(len(split_frame)),
                "sklearn_signal_count": int(sklearn_signal.sum()),
                "onnx_signal_count": int(onnx_signal.sum()),
                "signal_count_diff": int(onnx_signal.sum() - sklearn_signal.sum()),
                "signal_mismatch_count": int(signal_mismatch.sum()),
                "side_mismatch_on_signal_count": int(side_mismatch_on_signal.sum()),
                "max_edge_abs_diff": float(edge_diff.max()) if len(edge_diff) else 0.0,
                "passed": bool(int(signal_mismatch.sum()) == 0 and int(side_mismatch_on_signal.sum()) == 0),
            }
        )
    return rows


def write_feature_csvs(contexts: Sequence[Mapping[str, Any]], model_input: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for context in contexts:
        feature_set = context["feature_set"]
        feature_columns = list(context["feature_columns"])
        key = (feature_set.feature_set_id, context["feature_order_hash"])
        if key in seen:
            continue
        seen.add(key)
        path = FEATURE_ROOT / f"f68c_{slug(feature_set.feature_set_id)}_{context['feature_order_hash'][:10]}_features.csv"
        frame = model_input.loc[:, ["timestamp", *feature_columns]].copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
        io_path(path.parent).mkdir(parents=True, exist_ok=True)
        frame.to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")
        rows.append(
            {
                "feature_set_id": feature_set.feature_set_id,
                "feature_count": len(feature_columns),
                "feature_order_hash": context["feature_order_hash"],
                "feature_csv_path": rel(path),
                "feature_csv_sha256": sha256_file(path),
                "rows": int(len(frame)),
            }
        )
    return rows


def axis_summary_row(context: Mapping[str, Any], export: Mapping[str, Any], reference: Mapping[str, Any]) -> dict[str, Any]:
    axis: CandidateAxis = context["axis"]
    rows = {row["split"]: row for row in context["kpi_rows"]}
    val = rows["validation"]
    oos = rows["oos"]
    prob_pass = all(row.get("passed") for row in export.get("probability_parity", [])) if export.get("probability_parity") else False
    signal_pass = all(row.get("passed") for row in export.get("signal_parity", [])) if export.get("signal_parity") else False
    return {
        "candidate_id": axis.candidate_id,
        "axis_id": axis.axis_id,
        "role": axis.role,
        "priority": axis.priority,
        "candidate_id_match": context["candidate_id_match"],
        "target_id": context["target"].target_id,
        "feature_set_id": context["feature_set"].feature_set_id,
        "feature_count": len(context["feature_columns"]),
        "feature_order_hash": context["feature_order_hash"],
        "model_id": context["model_spec"].model_id,
        "model_family": context["model_spec"].family,
        "threshold_quantile": axis.threshold_quantile,
        "edge_threshold_from_train": context["edge_threshold_from_train"],
        "cooldown_bars": axis.cooldown_bars,
        "side_policy": context["side_policy"],
        "exit_mode": context["exit_mode"],
        "validation_net": val["net_profit_proxy_points"],
        "validation_pf": val["profit_factor"],
        "validation_tpd": val["trades_per_day"],
        "validation_dd_pct_proxy": val["proxy_dd_percent_on_10000_points"],
        "oos_net": oos["net_profit_proxy_points"],
        "oos_pf": oos["profit_factor"],
        "oos_tpd": oos["trades_per_day"],
        "oos_dd_pct_proxy": oos["proxy_dd_percent_on_10000_points"],
        "reference_reconstruction_passed": context["reference_diff"]["passed"],
        "reference_max_abs_diff": context["reference_diff"]["max_abs_diff"],
        "export_status": export["export_status"],
        "probability_parity_passed": prob_pass,
        "signal_parity_passed": signal_pass,
        "onnx_path": export.get("onnx_path", ""),
        "onnx_sha256": export.get("onnx_sha256", ""),
        "export_error": export.get("export_error", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def handoff_intent_row(context: Mapping[str, Any], export: Mapping[str, Any], feature_csv_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    axis: CandidateAxis = context["axis"]
    feature_csv = next(row for row in feature_csv_rows if row["feature_order_hash"] == context["feature_order_hash"])
    edge_threshold = float(context["edge_threshold_from_train"])
    short_threshold = 2.0 if str(context["side_policy"]).startswith("long_only") else 0.0
    long_threshold = 2.0 if str(context["side_policy"]).startswith("short_only") else 0.0
    atr_enabled = str(context["exit_mode"]).startswith("atr_sltp")
    probe_eligible = bool(
        str(export.get("export_status", "")).startswith("exported")
        and export.get("onnx_sha256")
    )
    return {
        "candidate_id": axis.candidate_id,
        "axis_id": axis.axis_id,
        "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
        "probe_eligible": probe_eligible,
        "model_backend": "onnx" if probe_eligible else "not_exported_preserved_clue",
        "model_path_repo": export.get("onnx_path", "") if probe_eligible else "",
        "model_sha256": export.get("onnx_sha256", "") if probe_eligible else "",
        "ineligible_reason": "" if probe_eligible else export.get("export_error", "export_failed"),
        "feature_csv_repo": feature_csv["feature_csv_path"],
        "feature_count": len(context["feature_columns"]),
        "feature_order_hash": context["feature_order_hash"],
        "decision_mode": "threshold_margin",
        "short_threshold": short_threshold,
        "long_threshold": long_threshold,
        "min_margin": edge_threshold,
        "side_policy_note": context["side_policy"],
        "max_hold_bars": int(context["target"].horizon_bars),
        "same_direction_reentry_cooldown_bars": int(axis.cooldown_bars),
        "atr_sltp_enabled": atr_enabled,
        "atr_stop_multiplier": float(context["target"].atr_stop_multiplier) if atr_enabled else 0.0,
        "atr_take_profit_multiplier": float(context["target"].atr_take_profit_multiplier) if atr_enabled else 0.0,
        "proxy_runtime_mapping_boundary": (
            "handoff_intent_only_requires_mt5_runtime_probe"
            "(인계 의도 전용, MT5 런타임 탐침 필요)"
        ),
    }


def build_result(created_at: str) -> dict[str, Any]:
    ensure_dirs()
    reference = f68b_reference_by_candidate()
    missing = [axis.candidate_id for axis in CANDIDATE_AXES if axis.candidate_id not in reference]
    if missing:
        raise RuntimeError(f"F68B reference candidates missing: {missing}")
    model_input_raw, raw, raw_positions = f68b.load_frames()
    model_input = f68b.model_input_with_spread(model_input_raw, raw)
    contexts = [build_candidate_context(axis, model_input, raw, raw_positions, reference[axis.candidate_id]) for axis in CANDIDATE_AXES]
    exports = [export_candidate(context) for context in contexts]
    feature_csv_rows = write_feature_csvs(contexts, model_input)
    summary_rows = [axis_summary_row(context, export, reference[context["axis"].candidate_id]) for context, export in zip(contexts, exports)]
    kpi_rows = [row for context in contexts for row in context["kpi_rows"]]
    probability_rows = [row for export in exports for row in export.get("probability_parity", [])]
    signal_rows = [row for export in exports for row in export.get("signal_parity", [])]
    handoff_rows = [handoff_intent_row(context, export, feature_csv_rows) for context, export in zip(contexts, exports)]
    exported_count = sum(1 for row in summary_rows if str(row["export_status"]).startswith("exported"))
    parity_pass_count = sum(1 for row in summary_rows if row["probability_parity_passed"] and row["signal_parity_passed"])
    status = (
        "completed_onnx_scout_export_no_authority(ONNX 탐색 내보내기 완료, 권위 없음)"
        if exported_count
        else "blocked_no_onnx_exported_preserved_clues_only(ONNX 내보내기 없음, 보존 단서만)"
    )
    judgment = (
        "onnx_scout_axes_materialized_mt5_probe_pending_no_authority(ONNX 탐색 축 물질화, MT5 탐침 대기, 권위 없음)"
        if parity_pass_count >= 2
        else "partial_onnx_scout_axes_materialized_mt5_probe_pending_no_authority(부분 ONNX 탐색 축 물질화, MT5 탐침 대기, 권위 없음)"
    )
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_axis_count": len(CANDIDATE_AXES),
        "exported_count": exported_count,
        "parity_pass_count": parity_pass_count,
        "summary_rows": summary_rows,
        "kpi_rows": kpi_rows,
        "probability_parity_rows": probability_rows,
        "signal_parity_rows": signal_rows,
        "feature_csv_rows": feature_csv_rows,
        "handoff_intent_rows": handoff_rows,
        "exports": exports,
        "grok_receipt": rel(GROK_RECEIPT),
        "grok_clean_output": rel(GROK_CLEAN_OUTPUT),
    }


def write_outputs(result: Mapping[str, Any]) -> dict[str, Path]:
    artifacts = {
        "final": RUN_ROOT / "f68c_candidate_axis_onnx_scout_export.json",
        "manifest": RUN_ROOT / "run_manifest.json",
        "summary": RUN_ROOT / "f68c_candidate_axis_summary.csv",
        "kpi": RUN_ROOT / "f68c_candidate_axis_kpi_by_split.csv",
        "probability_parity": RUN_ROOT / "f68c_onnx_probability_parity.csv",
        "signal_parity": RUN_ROOT / "f68c_onnx_signal_parity.csv",
        "features": RUN_ROOT / "f68c_feature_csv_manifest.csv",
        "handoff": RUN_ROOT / "f68c_handoff_intent.json",
        "review_report": REVIEWS_ROOT / "frontier68C_onnx_scout_export_report.md",
        "review_summary": REVIEWS_ROOT / "f68c_candidate_axis_summary_review.csv",
        "review_handoff": REVIEWS_ROOT / "f68c_handoff_intent_review.json",
        "gate_audit": REVIEWS_ROOT / "f68c_gate_audit.md",
    }
    write_json(artifacts["final"], result)
    write_csv(artifacts["summary"], result["summary_rows"])
    write_csv(artifacts["kpi"], result["kpi_rows"])
    write_csv(artifacts["probability_parity"], result["probability_parity_rows"])
    write_csv(artifacts["signal_parity"], result["signal_parity_rows"])
    write_csv(artifacts["features"], result["feature_csv_rows"])
    write_json(artifacts["handoff"], {"run_id": RUN_ID, "handoff_intent": result["handoff_intent_rows"], "claim_boundary": CLAIM_BOUNDARY})
    write_csv(artifacts["review_summary"], result["summary_rows"])
    write_json(artifacts["review_handoff"], {"run_id": RUN_ID, "handoff_intent": result["handoff_intent_rows"], "claim_boundary": CLAIM_BOUNDARY})
    write_md(artifacts["review_report"], report_lines(result, artifacts))
    write_md(artifacts["gate_audit"], gate_audit_lines(result, artifacts))
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "status": result["status"],
        "judgment": result["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_68/frontier68c_candidate_scoring_or_onnx_scout_export.py",
        "source_inputs": [rel(F68B_TOP_CANDIDATES), rel(F68B_REPORT), rel(GROK_RECEIPT), rel(f68b.MODEL_INPUT), rel(f68b.RAW_US100)],
        "artifacts": {key: rel(path) for key, path in artifacts.items()},
        "model_artifacts": [export for export in result["exports"]],
        "feature_artifacts": result["feature_csv_rows"],
        "artifact_identities": {
            key: artifact_identity(path, rows=None)
            for key, path in artifacts.items()
            if io_path(path).exists()
        },
        "next_run_id": NEXT_RUN_ID,
    }
    write_json(artifacts["manifest"], manifest)
    return artifacts


def report_lines(result: Mapping[str, Any], artifacts: Mapping[str, Path]) -> list[str]:
    lines = [
        "# F68C ONNX Scout Export(F68C ONNX 탐색 내보내기)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68B의 density axis(밀도 축), PF axis(수익 팩터 축), low-DD density axis(저손실폭 밀도 축)을 F68B logic(로직)으로 재학습하고 ONNX scout export(ONNX 탐색 내보내기)를 시도했다.",
        "",
        "Effect(효과): 한 후보를 winner(승자)처럼 고르지 않고, MT5 Runtime Probe(MT5 런타임 탐침)로 물질화할 후보 축과 인계 계약(handoff contract, 인계 계약)을 분리 기록했다.",
        "",
        "## Grok Review(그록 검토)",
        "",
        f"- receipt(영수증): `{result['grok_receipt']}`.",
        f"- clean_output(정리 출력): `{result['grok_clean_output']}`.",
        "- classification(분류): dual-axis preservation(이중 축 보존) accepted(수용), single leaderboard(단일 순위표) rejected_or_risky(거절 또는 위험), converter/parity(변환기/동등성)는 local verification(로컬 검증 필요).",
        "",
        "## Candidate Axis Results(후보 축 결과)",
        "",
    ]
    for row in result["summary_rows"]:
        lines.extend(
            [
                f"### {row['axis_id']} - `{row['candidate_id']}`",
                "",
                f"- feature/model(피처/모델): `{row['feature_set_id']}` / `{row['model_id']}`.",
                f"- feature_count/hash(피처 수/해시): `{row['feature_count']}` / `{row['feature_order_hash']}`.",
                f"- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `{fmt(row['edge_threshold_from_train'])}/{row['cooldown_bars']}/{row['side_policy']}/{row['exit_mode']}`.",
                f"- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭): `{fmt(row['validation_net'])}/{fmt(row['validation_pf'])}/{fmt(row['validation_tpd'])}/{fmt(row['validation_dd_pct_proxy'])}`.",
                f"- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭): `{fmt(row['oos_net'])}/{fmt(row['oos_pf'])}/{fmt(row['oos_tpd'])}/{fmt(row['oos_dd_pct_proxy'])}`.",
                f"- reconstruction/parity(재구성/동등성): `{row['reference_reconstruction_passed']}` / probability `{row['probability_parity_passed']}` / signal `{row['signal_parity_passed']}`.",
                f"- export_status(내보내기 상태): `{row['export_status']}`.",
                "",
            ]
        )
    lines.extend(
        [
            "## Runtime Parity Boundary(런타임 동등성 경계)",
            "",
            "- research_path(연구 경로): `stage_pipelines/stage_frontier_68/frontier68c_candidate_scoring_or_onnx_scout_export.py`.",
            "- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`.",
            "- shared_contract(공유 계약): feature order hash(피처 순서 해시), ONNX probability output(ONNX 확률 출력), threshold_margin decision mode(임계값/마진 의사결정), max hold/cooldown/ATR SLTP(최대 보유/대기봉/ATR 손익절).",
            "- known_differences(알려진 차이): proxy DD%(프록시 손실폭 %)는 account DD(계좌 손실폭)가 아니며, proxy exit mapping(프록시 청산 매핑)은 MT5 Strategy Tester(전략 테스터)에서 검증해야 한다.",
            "- parity_check(동등성 점검): ONNX probability parity(ONNX 확률 동등성)와 threshold signal parity(임계값 신호 동등성)를 로컬에서 실행했다. MT5 Runtime Probe(MT5 런타임 탐침)는 아직 대기다.",
            f"- handoff_intent(인계 의도): `{rel(artifacts['review_handoff'])}`.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"- `{NEXT_RUN_ID}`: exported axes(내보낸 축)를 MT5 Runtime Probe(MT5 런타임 탐침)로 물질화하고 proxy/runtime KPI gap(프록시/런타임 핵심 성과 지표 간극)을 기록한다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(result: Mapping[str, Any], artifacts: Mapping[str, Path]) -> list[str]:
    return [
        "# F68C Required Gate Coverage Audit(F68C 필수 게이트 커버리지 감사)",
        "",
        f"- pre_export_grok_review(내보내기 전 그록 검토): `{result['grok_receipt']}`.",
        f"- f68b_source_evidence(F68B 원천 근거): `{rel(F68B_REPORT)}`.",
        f"- candidate_axis_count(후보 축 수): `{result['candidate_axis_count']}`.",
        f"- exported_count(내보낸 수): `{result['exported_count']}`.",
        f"- parity_pass_count(동등성 통과 수): `{result['parity_pass_count']}`.",
        f"- handoff_intent(인계 의도): `{rel(artifacts['review_handoff'])}`.",
        "- MT5 Runtime Probe(MT5 런타임 탐침): `pending_next_run(다음 실행 대기)`.",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`.",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`.",
    ]


def update_state_and_ledgers(result: Mapping[str, Any], artifacts: Mapping[str, Path]) -> None:
    best_density = next(row for row in result["summary_rows"] if row["axis_id"] == "density_axis")
    best_pf = next(row for row in result["summary_rows"] if row["axis_id"] == "pf_axis")
    row = {
        "ledger_row_id": f"{RUN_ID}__onnx_scout_export",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "onnx_scout_export(ONNX 탐색 내보내기)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "candidate_axis_materialization(후보 축 물질화)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "onnx_export_proxy_reconstruction_parity(ONNX 내보내기/프록시 재구성/동등성)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "status": result["status"],
        "judgment": result["judgment"],
        "path": rel(artifacts["review_report"]),
        "primary_kpi": (
            f"exported={result['exported_count']};parity_pass={result['parity_pass_count']};"
            f"density_axis={best_density['candidate_id']};pf_axis={best_pf['candidate_id']}"
        ),
        "guardrail_kpi": "mt5_runtime_probe_pending;proxy_dd_not_account_authority(MT5 런타임 탐침 대기, 프록시 손실폭은 계좌 권위 아님)",
        "external_verification_status": "out_of_scope_by_claim_pre_mt5_export_only(주장 범위상 MT5 전 내보내기 전용)",
        "notes": "F68C preserved density/PF/low-DD axes and exported ONNX scout artifacts where converter/parity passed; no runtime authority claimed.",
        "run_number": "frontier68C",
        "date": result["created_at_utc"][:10],
        "decision": "proceed_to_f68d_mt5_runtime_probe_candidate_axis_materialization",
        "next_run_id": NEXT_RUN_ID,
        "rows": len(result["summary_rows"]),
        "gate_passes": result["parity_pass_count"],
        "gate_total": len(result["summary_rows"]),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(artifacts["review_report"]),
        "trained_models": len(result["summary_rows"]),
        "onnx_parity": result["parity_pass_count"],
        "best_proxy": best_density["candidate_id"],
        "candidate_rows": len(result["summary_rows"]),
        "positive_proxy_rows": "",
        "best_model_id": best_density["model_id"],
        "best_proxy_net": fmt(best_density["oos_net"]),
        "run_date": result["created_at_utc"][:10],
        "primary_artifact": rel(artifacts["final"]),
        "view": "onnx_scout_export(ONNX 탐색 내보내기)",
        "tier": "Tier A+B planned(티어 A+B 계획)",
        "metric_scope": "proxy_reconstruction_and_onnx_parity(프록시 재구성 및 ONNX 동등성)",
        "net_profit": fmt(best_density["oos_net"]),
        "profit_factor": fmt(best_density["oos_pf"]),
        "drawdown": fmt(best_density["oos_dd_pct_proxy"]),
        "trade_count": "",
        "result_status": result["status"],
        "feature_count": best_density["feature_count"],
        "lane": "onnx_scout_export(ONNX 탐색 내보내기)",
        "family": "model_export(모델 내보내기)",
        "primary_report": rel(artifacts["review_report"]),
        "sample_rows": "",
        "attempt_count": len(result["summary_rows"]),
        "source_package_run_id": PARENT_RUN_ID,
        "row_id": f"{RUN_ID}__onnx_scout_export",
        "scoreboard": "structural_scout(구조 탐색)",
        "evidence_boundary": "onnx_scout_only_no_runtime_authority(ONNX 탐색 전용, 런타임 권위 없음)",
        "work_family": "model_export(모델 내보내기)",
        "evidence_scope": "candidate_axis_materialization(후보 축 물질화)",
        "run_key": RUN_ID,
        "question": "Can F68B proxy poles be materialized as ONNX scout artifacts before MT5?(F68B 프록시 극을 MT5 전 ONNX 탐색 산출물로 물질화할 수 있는가)",
        "next_action": NEXT_RUN_ID,
        "result_judgment": result["judgment"],
        "final_decision_path": rel(artifacts["review_report"]),
        "created_at": result["created_at_utc"],
        "gate_audit_path": rel(artifacts["gate_audit"]),
        "artifact_count": len(artifacts),
        "created_at_utc": result["created_at_utc"],
        "required_gate_audit": rel(artifacts["gate_audit"]),
        "kpi_summary": (
            f"exported_count={result['exported_count']};parity_pass_count={result['parity_pass_count']};"
            f"density_oos_pf={fmt(best_density['oos_pf'])};pf_axis_oos_pf={fmt(best_pf['oos_pf'])}"
        ),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "trade_density": fmt(best_density["oos_tpd"]),
        "source_authority": "proxy_onnx_scout_no_runtime(프록시 ONNX 탐색, 런타임 없음)",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_onnx_scout_export(전선 ONNX 탐색 내보내기)",
        "run_type": "candidate_axis_materialization(후보 축 물질화)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(artifacts["final"]),
        "result_path": rel(artifacts["review_report"]),
        "selected_net_profit": fmt(best_density["oos_net"]),
        "selected_profit_factor": fmt(best_density["oos_pf"]),
        "selected_trade_density": fmt(best_density["oos_tpd"]),
        "max_drawdown_percent": fmt(best_density["oos_dd_pct_proxy"]),
        "strict_joint_pass_count": 0,
    }
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    write_review_index()
    write_current_state(result)
    write_selection_status(result, artifacts)


def write_review_index() -> None:
    lines = [
        "# F68 Review Index(F68 검토 색인)",
        "",
        "- `../00_spec/stage_brief.md`: F68 stage brief(F68 단계 개요)",
        "- `runA_report.md`: F68A stage open report(F68A 단계 개방 보고서)",
        "- `grok_stage_open_receipt.md`: F68 Grok stage-open receipt(F68 그록 단계 개방 영수증)",
        "- `stage_run_ledger.csv`: F68 stage-local run ledger(F68 단계 내부 실행 장부)",
        "- `frontier68A_bridge_feasibility_and_label_design_report.md`: F68A bridge feasibility and label design report(F68A 연결 가능성 및 라벨 설계 보고서)",
        "- `frontier68B_proxy_broad_sweep_report.md`: F68B proxy broad sweep report(F68B 프록시 넓은 탐색 보고서)",
        "- `frontier68C_onnx_scout_export_report.md`: F68C ONNX scout export report(F68C ONNX 탐색 내보내기 보고서)",
        "- `f68c_candidate_axis_summary_review.csv`: F68C candidate axis summary(F68C 후보 축 요약)",
        "- `f68c_handoff_intent_review.json`: F68C handoff intent(F68C 인계 의도)",
        "- `f68c_gate_audit.md`: F68C required gate coverage audit(F68C 필수 게이트 커버리지 감사)",
        "",
        f"Current status(현재 상태): `{RUN_ID}` completed as ONNX scout export(ONNX 탐색 내보내기 완료, 권위 없음)",
        f"Next action(다음 행동): `{NEXT_RUN_ID}`",
    ]
    write_md(REVIEWS_ROOT / "review_index.md", lines)


def write_current_state(result: Mapping[str, Any]) -> None:
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {result['status']}",
        f"current_judgment: {result['judgment']}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68_mandatory_runtime_probe_pending_after_onnx_scout_export(F68 ONNX 탐색 내보내기 후 필수 런타임 탐침 대기)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{result['created_at_utc']}'",
        "notes:",
        f'  - "F68C completed(완료): candidate axes(후보 축) `{result["candidate_axis_count"]}`개, ONNX exported(ONNX 내보내기) `{result["exported_count"]}`개, parity pass(동등성 통과) `{result["parity_pass_count"]}`개를 기록했다."',
        '  - "Boundary(경계): F68C is ONNX scout export only(ONNX 탐색 내보내기 전용) and does not claim MT5 runtime authority(MT5 런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성)."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Runtime Probe(MT5 런타임 탐침)를 실행하고 proxy/runtime gap(프록시/런타임 간극)을 기록한다."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    cws = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        "",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        "",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F68C ONNX scout export(F68C ONNX 탐색 내보내기)를 실행했다.",
        "",
        "Effect(효과): F68B의 density/PF/low-DD axes(밀도/수익 팩터/저손실폭 축)를 하나의 winner(승자)로 합치지 않고, MT5 Runtime Probe(MT5 런타임 탐침)로 물질화할 인계 산출물(handoff artifacts, 인계 산출물)로 분리했다.",
        "",
        f"- F68C status(F68C 상태): `{result['status']}`.",
        f"- exported_count(내보낸 수): `{result['exported_count']}`.",
        f"- parity_pass_count(동등성 통과 수): `{result['parity_pass_count']}`.",
        "- mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침): still pending(아직 대기).",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- F68C report(F68C 보고서): `stages/{STAGE_ID}/03_reviews/frontier68C_onnx_scout_export_report.md`",
        f"- F68C handoff intent(F68C 인계 의도): `stages/{STAGE_ID}/03_reviews/f68c_handoff_intent_review.json`",
        f"- F68C summary(F68C 요약): `stages/{STAGE_ID}/03_reviews/f68c_candidate_axis_summary_review.csv`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", cws)


def write_selection_status(result: Mapping[str, Any], artifacts: Mapping[str, Path]) -> None:
    lines = [
        "# F68 Selection Status(F68 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- completed_action(완료 행동): F68C ONNX scout export(F68C ONNX 탐색 내보내기)로 후보 축 `{result['candidate_axis_count']}`개를 물질화했다.",
        f"- exported_count(내보낸 수): `{result['exported_count']}`.",
        f"- parity_pass_count(동등성 통과 수): `{result['parity_pass_count']}`.",
        f"- report(보고서): `{rel(artifacts['review_report'])}`",
        f"- handoff_intent(인계 의도): `{rel(artifacts['review_handoff'])}`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}` MT5 Runtime Probe(MT5 런타임 탐침).",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", lines)


def main() -> int:
    created_at = utc_now()
    result = build_result(created_at)
    artifacts = write_outputs(result)
    update_state_and_ledgers(result, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": result["status"],
                    "judgment": result["judgment"],
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "candidate_axis_count": result["candidate_axis_count"],
                    "exported_count": result["exported_count"],
                    "parity_pass_count": result["parity_pass_count"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if result["exported_count"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
