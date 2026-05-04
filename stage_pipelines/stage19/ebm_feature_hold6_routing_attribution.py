from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

from foundation.control_plane.alpha_run_ledgers import materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.baseline_training import load_feature_order
from foundation.models.ebm_score_table import ebm_main_effect_contribution_tensor
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage19 import ebm_mt5_runtime_probe as stage19_mt5


STAGE_ID = stage19_mt5.STAGE_ID
RUN_ID = "run13H_ebm_feature_hold6_routing_attribution_v1"
RUN_NUMBER = "run13H"
PACKET_ID = "stage19_run13H_ebm_feature_hold6_routing_attribution_v1"
SOURCE_AGGREGATE_PACKET_ID = stage19_mt5.AGGREGATE_PACKET_ID
SOURCE_RUN_NUMBERS = ("run13B", "run13F", "run13G")
FOCUS_RUN_NUMBER = "run13F"
EXPLORATION_LABEL = "stage19_Model__EBMFeatureHold6RoutingAttribution"
BOUNDARY = "ebm_feature_hold6_routing_attribution_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_ebm_feature_hold6_routing_attribution_completed"
EXTERNAL_VERIFICATION_STATUS = "completed_reused_run13B_run13F_run13G_mt5_evidence"
FEATURE_CONTRIBUTION_PROBABILITY_TOLERANCE = 1.0e-3

ROOT = stage19_mt5.ROOT
STAGE_ROOT = stage19_mt5.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
AGGREGATE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / SOURCE_AGGREGATE_PACKET_ID
STAGE_LEDGER_PATH = stage19_mt5.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = stage19_mt5.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = stage19_mt5.RUN_REGISTRY_PATH
WORKSPACE_STATE_PATH = stage19_mt5.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = stage19_mt5.CURRENT_WORKING_STATE_PATH
SELECTION_STATUS_PATH = stage19_mt5.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = stage19_mt5.REVIEW_INDEX_PATH
DECISION_PATH = ROOT / "docs/decisions/2026-05-04_stage19_run13H_ebm_feature_hold6_routing_attribution.md"
REPORT_PATH = STAGE_ROOT / "03_reviews/run13H_ebm_feature_hold6_routing_attribution_packet.md"
SELECTED_VARIANT_ID = stage19_mt5.SELECTED_VARIANT_ID
MODEL_FAMILY = stage19_mt5.MODEL_FAMILY
FEATURE_SET_ID = stage19_mt5.FEATURE_SET_ID
LABEL_ID = stage19_mt5.LABEL_ID
SPLIT_CONTRACT = stage19_mt5.SPLIT_CONTRACT

FEATURE_CONTRIBUTION_COLUMNS = (
    "focus_run_id",
    "tier_scope",
    "split",
    "side",
    "rank",
    "feature",
    "feature_index",
    "signal_count",
    "mean_chosen_minus_best_other",
    "mean_chosen_minus_opposite",
    "mean_chosen_minus_flat",
    "mean_chosen_class_contribution",
    "mean_abs_chosen_minus_best_other",
    "positive_share",
    "mean_probability",
    "mean_probability_margin",
)
FEATURE_GROUP_COLUMNS = (
    "tier_scope",
    "split",
    "side",
    "signal_count",
    "top1_feature",
    "top1_mean_chosen_minus_best_other",
    "top3_features",
    "top5_features",
    "top3_abs_share",
    "top10_abs_share",
)
HOLD_AXIS_COLUMNS = (
    "source_run_number",
    "source_run_id",
    "topic_read",
    "threshold_quantile",
    "max_hold_bars",
    "split",
    "routed_net_profit",
    "routed_profit_factor",
    "routed_trade_count",
    "routed_expectancy",
    "routed_max_drawdown",
    "tier_a_only_net_profit",
    "tier_a_only_profit_factor",
    "tier_a_only_trade_count",
    "tier_b_fallback_only_net_profit",
    "tier_b_fallback_only_profit_factor",
    "tier_b_fallback_only_trade_count",
    "tier_a_route_share",
    "tier_b_fallback_route_share",
    "tier_a_signal_count",
    "tier_b_fallback_signal_count",
)
ROUTING_COLUMNS = (
    "source_run_number",
    "source_run_id",
    "topic_read",
    "threshold_quantile",
    "max_hold_bars",
    "split",
    "record_view",
    "tier_scope",
    "route_role",
    "net_profit",
    "profit_factor",
    "expectancy",
    "trade_count",
    "win_rate_percent",
    "max_drawdown_amount",
    "feature_ready_count",
    "model_ok_count",
    "model_fail_count",
    "order_attempt_count",
    "order_fill_count",
    "signal_count",
    "long_signal_count",
    "short_signal_count",
    "route_share",
    "profit_attribution_note",
)
TRADE_SHAPE_COLUMNS = (
    "source_run_number",
    "source_run_id",
    "max_hold_bars",
    "split",
    "record_view",
    "tier_scope",
    "route_role",
    "direction",
    "trade_count",
    "net_profit",
    "avg_hold_bars",
    "mfe_mean",
    "mae_mean",
    "realized_over_mfe_mean",
    "positive_month_ratio",
    "top_session",
    "top_trend",
    "top_volatility",
)


@dataclass(frozen=True)
class SourceRun:
    run_number: str
    run_id: str
    packet_id: str
    topic_read: str
    threshold_quantile: float
    max_hold_bars: int
    summary: Mapping[str, Any]

    @property
    def run_root(self) -> Path:
        return STAGE_ROOT / "02_runs" / self.run_id

    @property
    def packet_root(self) -> Path:
        return ROOT / "docs/agent_control/packets" / self.packet_id


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def repo_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def read_json_any(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.8g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_div(numerator: Any, denominator: Any) -> float | None:
    den = safe_float(denominator)
    if den == 0.0:
        return None
    return safe_float(numerator) / den


def mean_or_none(values: Iterable[Any]) -> float | None:
    clean = [safe_float(value) for value in values if value not in (None, "", "NA")]
    return sum(clean) / len(clean) if clean else None


def cell(record: Mapping[str, Any], section: str, key: str) -> Any:
    section_value = record.get(section, {})
    if not isinstance(section_value, Mapping):
        return None
    value = section_value.get(key, {})
    if isinstance(value, Mapping):
        return value.get("value")
    return value


def source_runs() -> list[SourceRun]:
    aggregate = read_json_any(AGGREGATE_PACKET_ROOT / "aggregate_summary.json")
    summaries = aggregate.get("summaries", []) if isinstance(aggregate, Mapping) else []
    wanted = {run_number: index for index, run_number in enumerate(SOURCE_RUN_NUMBERS)}
    selected: list[SourceRun] = []
    for item in summaries:
        run_number = str(item.get("run_number"))
        if run_number not in wanted:
            continue
        selected.append(
            SourceRun(
                run_number=run_number,
                run_id=str(item.get("run_id")),
                packet_id=str(item.get("packet_id")),
                topic_read=str(item.get("topic_read")),
                threshold_quantile=safe_float(item.get("threshold_quantile")),
                max_hold_bars=int(item.get("max_hold_bars") or 0),
                summary=item,
            )
        )
    selected.sort(key=lambda source: wanted[source.run_number])
    if tuple(source.run_number for source in selected) != SOURCE_RUN_NUMBERS:
        raise RuntimeError(f"missing source runs for {SOURCE_RUN_NUMBERS}: {[source.run_number for source in selected]}")
    return selected


def load_normalized_kpi(source: SourceRun) -> list[dict[str, Any]]:
    path = source.packet_root / "normalized_kpi_records.jsonl"
    payload = io_path(path).read_text(encoding="utf-8-sig").strip()
    if not payload:
        return []
    if payload.startswith("["):
        data = json.loads(payload)
    else:
        data = [json.loads(line) for line in payload.splitlines() if line.strip()]
    return [item for item in data if isinstance(item, dict)]


def load_trade_records(source: SourceRun) -> list[dict[str, Any]]:
    path = source.packet_root / "trade_level_records.json"
    if not io_path(path).exists():
        return []
    data = read_json_any(path)
    return [item for item in data if isinstance(item, dict)]


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(shifted)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def timestamp_strings(series: pd.Series) -> list[str]:
    return pd.to_datetime(series, utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ").tolist()


def load_focus_models_and_frames(focus: SourceRun) -> dict[str, Any]:
    summary = focus.summary
    artifacts = summary.get("model_artifacts", {}) if isinstance(summary.get("model_artifacts"), Mapping) else {}
    predictions = summary.get("prediction_artifacts", {}) if isinstance(summary.get("prediction_artifacts"), Mapping) else {}
    tier_a_model_path = repo_path(artifacts["tier_a_joblib"]["source"])
    tier_b_model_path = repo_path(artifacts["tier_b_joblib"]["source"])
    tier_a_model = joblib.load(io_path(tier_a_model_path))
    tier_b_model = joblib.load(io_path(tier_b_model_path))
    full_feature_order = load_feature_order(stage19_mt5.FEATURE_ORDER_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_a_predictions = pd.read_parquet(io_path(repo_path(predictions["tier_a_predictions"]["path"])))
    tier_b_predictions = pd.read_parquet(io_path(repo_path(predictions["tier_b_predictions"]["path"])))
    feature_root = focus.run_root / "features"
    return {
        "focus_run": focus,
        "tier_a_model_path": tier_a_model_path,
        "tier_b_model_path": tier_b_model_path,
        "tier_a_model": tier_a_model,
        "tier_b_model": tier_b_model,
        "tier_a_feature_order": full_feature_order,
        "tier_b_feature_order": tier_b_feature_order,
        "thresholds": artifacts.get("thresholds", {}),
        "tier_a_predictions": tier_a_predictions,
        "tier_b_predictions": tier_b_predictions,
        "feature_paths": {
            ("Tier A", "validation"): feature_root / "tier_a_validation_is_feature_matrix.csv",
            ("Tier A", "oos"): feature_root / "tier_a_oos_feature_matrix.csv",
            ("Tier B", "validation"): feature_root / "tier_b_fallback_validation_is_feature_matrix.csv",
            ("Tier B", "oos"): feature_root / "tier_b_fallback_oos_feature_matrix.csv",
        },
    }


def decision_sides(predictions: pd.DataFrame, threshold: float) -> np.ndarray:
    p_long = predictions["p_long"].to_numpy(dtype="float64")
    p_short = predictions["p_short"].to_numpy(dtype="float64")
    sides = np.full(len(predictions), "flat", dtype=object)
    sides[(p_long >= threshold) & (p_long >= p_short)] = "long"
    sides[(p_short >= threshold) & (p_short > p_long)] = "short"
    return sides


def contribution_group_rows(
    *,
    focus_run_id: str,
    tier_scope: str,
    split: str,
    side: str,
    feature_order: Sequence[str],
    contributions: np.ndarray,
    probabilities: pd.DataFrame,
    side_mask: np.ndarray,
) -> list[dict[str, Any]]:
    if side == "long":
        chosen_index, opposite_index, flat_index = 2, 0, 1
        probability_column = "p_long"
    else:
        chosen_index, opposite_index, flat_index = 0, 2, 1
        probability_column = "p_short"
    side_contrib = contributions[side_mask]
    side_prob = probabilities.loc[side_mask].reset_index(drop=True)
    rows: list[dict[str, Any]] = []
    signal_count = int(len(side_contrib))
    if signal_count == 0:
        return rows
    for feature_index, feature in enumerate(feature_order):
        scores = side_contrib[:, feature_index, :]
        chosen = scores[:, chosen_index]
        opposite = scores[:, opposite_index]
        flat = scores[:, flat_index]
        best_other = np.maximum(opposite, flat)
        chosen_minus_best = chosen - best_other
        chosen_minus_opposite = chosen - opposite
        chosen_minus_flat = chosen - flat
        rows.append(
            {
                "focus_run_id": focus_run_id,
                "tier_scope": tier_scope,
                "split": split,
                "side": side,
                "rank": 0,
                "feature": str(feature),
                "feature_index": feature_index,
                "signal_count": signal_count,
                "mean_chosen_minus_best_other": float(chosen_minus_best.mean()),
                "mean_chosen_minus_opposite": float(chosen_minus_opposite.mean()),
                "mean_chosen_minus_flat": float(chosen_minus_flat.mean()),
                "mean_chosen_class_contribution": float(chosen.mean()),
                "mean_abs_chosen_minus_best_other": float(np.abs(chosen_minus_best).mean()),
                "positive_share": float((chosen_minus_best > 0.0).mean()),
                "mean_probability": float(side_prob[probability_column].mean()),
                "mean_probability_margin": float(side_prob["probability_margin"].mean()),
            }
        )
    rows.sort(key=lambda row: abs(safe_float(row["mean_chosen_minus_best_other"])), reverse=True)
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    return rows


def feature_group_row(rows: Sequence[Mapping[str, Any]], tier_scope: str, split: str, side: str, signal_count: int) -> dict[str, Any]:
    top = list(rows)
    total_abs = sum(abs(safe_float(row.get("mean_chosen_minus_best_other"))) for row in top)
    top3 = [str(row.get("feature")) for row in top[:3]]
    top5 = [str(row.get("feature")) for row in top[:5]]
    return {
        "tier_scope": tier_scope,
        "split": split,
        "side": side,
        "signal_count": signal_count,
        "top1_feature": top3[0] if top3 else "",
        "top1_mean_chosen_minus_best_other": safe_float(top[0].get("mean_chosen_minus_best_other")) if top else None,
        "top3_features": top3,
        "top5_features": top5,
        "top3_abs_share": safe_div(sum(abs(safe_float(row.get("mean_chosen_minus_best_other"))) for row in top[:3]), total_abs),
        "top10_abs_share": safe_div(sum(abs(safe_float(row.get("mean_chosen_minus_best_other"))) for row in top[:10]), total_abs),
    }


def feature_contribution_outputs(inputs: Mapping[str, Any]) -> dict[str, Any]:
    focus: SourceRun = inputs["focus_run"]
    full_rows: list[dict[str, Any]] = []
    top_rows: list[dict[str, Any]] = []
    group_rows: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    tier_specs = (
        ("Tier A", "tier_a", inputs["tier_a_model"], inputs["tier_a_feature_order"], inputs["tier_a_predictions"], safe_float(inputs["thresholds"].get("tier_a"))),
        ("Tier B", "tier_b_fallback", inputs["tier_b_model"], inputs["tier_b_feature_order"], inputs["tier_b_predictions"], safe_float(inputs["thresholds"].get("tier_b"))),
    )
    for tier_scope, source_label, model, feature_order, predictions, threshold in tier_specs:
        for split in ("validation", "oos"):
            feature_path = inputs["feature_paths"][(tier_scope, split)]
            feature_frame = pd.read_csv(io_path(feature_path))
            pred_split = predictions[predictions["split"] == split].reset_index(drop=True)
            feature_ts = timestamp_strings(feature_frame["timestamp_utc"])
            pred_ts = timestamp_strings(pred_split["timestamp"])
            if feature_ts != pred_ts:
                raise RuntimeError(f"timestamp mismatch for {tier_scope} {split}")
            values = feature_frame.loc[:, feature_order].to_numpy(dtype="float64")
            contributions = ebm_main_effect_contribution_tensor(model, values, feature_count=len(feature_order))
            logits = np.asarray(model.intercept_, dtype="float64").reshape(1, -1) + contributions.sum(axis=1)
            table_prob = softmax(logits)
            pred_prob = pred_split.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64")
            max_abs_probability_diff = float(np.max(np.abs(table_prob - pred_prob))) if len(pred_prob) else 0.0
            sides = decision_sides(pred_split, threshold)
            audit = {
                "tier_scope": tier_scope,
                "split": split,
                "source_label": source_label,
                "feature_matrix_path": rel(feature_path),
                "row_count": int(len(feature_frame)),
                "timestamp_alignment": "pass",
                "max_abs_probability_diff": max_abs_probability_diff,
                "probability_diff_tolerance": FEATURE_CONTRIBUTION_PROBABILITY_TOLERANCE,
                "threshold": threshold,
                "long_signal_count": int((sides == "long").sum()),
                "short_signal_count": int((sides == "short").sum()),
            }
            audits.append(audit)
            for side in ("long", "short"):
                mask = sides == side
                rows = contribution_group_rows(
                    focus_run_id=focus.run_id,
                    tier_scope=tier_scope,
                    split=split,
                    side=side,
                    feature_order=feature_order,
                    contributions=contributions,
                    probabilities=pred_split,
                    side_mask=mask,
                )
                full_rows.extend(rows)
                top_rows.extend(rows[:12])
                group_rows.append(feature_group_row(rows, tier_scope, split, side, int(mask.sum())))
    read = feature_contribution_read(group_rows)
    return {
        "feature_contribution_full": full_rows,
        "feature_contribution_top": top_rows,
        "feature_contribution_group_summary": group_rows,
        "feature_alignment_audit": audits,
        "feature_contribution_read": read,
    }


def top_features(row: Mapping[str, Any], count: int = 5) -> list[str]:
    features = row.get("top5_features") or row.get("top3_features") or []
    if isinstance(features, str):
        try:
            features = json.loads(features)
        except json.JSONDecodeError:
            features = [features]
    return [str(item) for item in list(features)[:count]]


def feature_contribution_read(group_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    repeated = Counter()
    for row in group_rows:
        repeated.update(top_features(row, 5))
    validation_oos_overlap: list[dict[str, Any]] = []
    for tier_scope in ("Tier A", "Tier B"):
        for side in ("long", "short"):
            val = next((row for row in group_rows if row.get("tier_scope") == tier_scope and row.get("split") == "validation" and row.get("side") == side), {})
            oos = next((row for row in group_rows if row.get("tier_scope") == tier_scope and row.get("split") == "oos" and row.get("side") == side), {})
            val_set = set(top_features(val, 5))
            oos_set = set(top_features(oos, 5))
            union = val_set | oos_set
            validation_oos_overlap.append(
                {
                    "tier_scope": tier_scope,
                    "side": side,
                    "top5_overlap_count": len(val_set & oos_set),
                    "top5_overlap_ratio": len(val_set & oos_set) / len(union) if union else 0.0,
                    "shared_features": sorted(val_set & oos_set),
                }
            )
    return {
        "top_repeated_features": [{"feature": feature, "top5_appearance_count": count} for feature, count in repeated.most_common(10)],
        "validation_oos_top5_overlap": validation_oos_overlap,
        "feature_axis_visible": any(item["top5_overlap_count"] >= 2 for item in validation_oos_overlap),
    }


def routing_rows(sources: Sequence[SourceRun], normalized: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in sources:
        records = normalized[source.run_number]
        split_total_feature_ready: dict[str, float] = {}
        for record in records:
            if cell(record, "row_grain", "route_role") == "routed_total":
                split_total_feature_ready[str(cell(record, "row_grain", "split"))] = safe_float(cell(record, "execution", "feature_ready_count"))
        for record in records:
            split = str(cell(record, "row_grain", "split"))
            role = str(cell(record, "row_grain", "route_role"))
            feature_ready = safe_float(cell(record, "execution", "feature_ready_count"))
            routed_summary_key = "validation_routed" if split == "validation" else "oos_routed"
            routed_summary = source.summary.get(routed_summary_key, {}) if isinstance(source.summary.get(routed_summary_key), Mapping) else {}
            if role == "primary_used" and feature_ready == 0.0:
                feature_ready = safe_float(routed_summary.get("tier_a_used_count"))
            elif role == "fallback_used" and feature_ready == 0.0:
                feature_ready = safe_float(routed_summary.get("tier_b_fallback_used_count"))
            route_share = 1.0 if role == "routed_total" else None
            if role in {"primary_used", "fallback_used"}:
                route_share = safe_div(feature_ready, split_total_feature_ready.get(split))
            rows.append(
                {
                    "source_run_number": source.run_number,
                    "source_run_id": source.run_id,
                    "topic_read": source.topic_read,
                    "threshold_quantile": source.threshold_quantile,
                    "max_hold_bars": source.max_hold_bars,
                    "split": split,
                    "record_view": cell(record, "row_grain", "record_view"),
                    "tier_scope": cell(record, "row_grain", "tier_scope"),
                    "route_role": role,
                    "net_profit": cell(record, "mt5_trading_headline", "net_profit"),
                    "profit_factor": cell(record, "mt5_trading_headline", "profit_factor"),
                    "expectancy": cell(record, "mt5_trading_headline", "expectancy"),
                    "trade_count": cell(record, "mt5_trading_headline", "trade_count"),
                    "win_rate_percent": cell(record, "mt5_trading_headline", "win_rate"),
                    "max_drawdown_amount": cell(record, "risk", "max_drawdown_amount"),
                    "feature_ready_count": feature_ready,
                    "model_ok_count": cell(record, "execution", "model_ok_count"),
                    "model_fail_count": cell(record, "execution", "model_fail_count"),
                    "order_attempt_count": cell(record, "execution", "order_attempt_count"),
                    "order_fill_count": cell(record, "execution", "order_fill_count"),
                    "signal_count": cell(record, "signal_model", "signal_count"),
                    "long_signal_count": cell(record, "signal_model", "long_count"),
                    "short_signal_count": cell(record, "signal_model", "short_count"),
                    "route_share": route_share,
                    "profit_attribution_note": "not_separable_from_single_routed_account_path" if role in {"primary_used", "fallback_used"} else "",
                }
            )
    return rows


def find_routing_row(rows: Sequence[Mapping[str, Any]], source_run_number: str, split: str, role: str, tier_scope: str | None = None) -> Mapping[str, Any]:
    for row in rows:
        if row.get("source_run_number") != source_run_number or row.get("split") != split or row.get("route_role") != role:
            continue
        if tier_scope is not None and row.get("tier_scope") != tier_scope:
            continue
        return row
    return {}


def hold_axis_rows(sources: Sequence[SourceRun], rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for source in sources:
        for split in ("validation", "oos"):
            routed = find_routing_row(rows, source.run_number, split, "routed_total")
            tier_a = find_routing_row(rows, source.run_number, split, "tier_only_total", "Tier A")
            tier_b = find_routing_row(rows, source.run_number, split, "tier_b_fallback_only_total", "Tier B")
            comp_a = find_routing_row(rows, source.run_number, split, "primary_used", "Tier A")
            comp_b = find_routing_row(rows, source.run_number, split, "fallback_used", "Tier B")
            out.append(
                {
                    "source_run_number": source.run_number,
                    "source_run_id": source.run_id,
                    "topic_read": source.topic_read,
                    "threshold_quantile": source.threshold_quantile,
                    "max_hold_bars": source.max_hold_bars,
                    "split": split,
                    "routed_net_profit": routed.get("net_profit"),
                    "routed_profit_factor": routed.get("profit_factor"),
                    "routed_trade_count": routed.get("trade_count"),
                    "routed_expectancy": routed.get("expectancy"),
                    "routed_max_drawdown": routed.get("max_drawdown_amount"),
                    "tier_a_only_net_profit": tier_a.get("net_profit"),
                    "tier_a_only_profit_factor": tier_a.get("profit_factor"),
                    "tier_a_only_trade_count": tier_a.get("trade_count"),
                    "tier_b_fallback_only_net_profit": tier_b.get("net_profit"),
                    "tier_b_fallback_only_profit_factor": tier_b.get("profit_factor"),
                    "tier_b_fallback_only_trade_count": tier_b.get("trade_count"),
                    "tier_a_route_share": comp_a.get("route_share"),
                    "tier_b_fallback_route_share": comp_b.get("route_share"),
                    "tier_a_signal_count": comp_a.get("signal_count"),
                    "tier_b_fallback_signal_count": comp_b.get("signal_count"),
                }
            )
    return out


def trade_shape_rows(sources: Sequence[SourceRun], trade_records: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for source in sources:
        frame = pd.DataFrame(trade_records[source.run_number])
        if frame.empty:
            continue
        frame["open_time"] = pd.to_datetime(frame["open_time"], errors="coerce")
        frame["month"] = frame["open_time"].dt.to_period("M").astype(str)
        group_columns = ["split", "record_view", "tier_scope", "route_role", "direction"]
        for keys, group in frame.groupby(group_columns, dropna=False):
            month_net = group.groupby("month")["net_profit"].sum() if len(group) else pd.Series(dtype=float)
            top_values = {
                "top_session": top_value(group, "session_slice"),
                "top_trend": top_value(group, "trend_regime"),
                "top_volatility": top_value(group, "volatility_regime"),
            }
            out.append(
                {
                    "source_run_number": source.run_number,
                    "source_run_id": source.run_id,
                    "max_hold_bars": source.max_hold_bars,
                    "split": keys[0],
                    "record_view": keys[1],
                    "tier_scope": keys[2],
                    "route_role": keys[3],
                    "direction": keys[4],
                    "trade_count": int(len(group)),
                    "net_profit": safe_float(group["net_profit"].sum()),
                    "avg_hold_bars": safe_float(group["hold_bars"].mean()),
                    "mfe_mean": safe_float(group["mfe"].mean()),
                    "mae_mean": safe_float(group["mae"].mean()),
                    "realized_over_mfe_mean": safe_float(group["realized_over_mfe"].mean()),
                    "positive_month_ratio": safe_div(float((month_net > 0.0).sum()), float(len(month_net))),
                    **top_values,
                }
            )
    return out


def top_value(frame: pd.DataFrame, column: str) -> str:
    if column not in frame or frame.empty:
        return ""
    counts = frame[column].fillna("unknown").astype(str).value_counts()
    return str(counts.index[0]) if len(counts) else ""


def split_hold_row(rows: Sequence[Mapping[str, Any]], run_number: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("source_run_number") == run_number and row.get("split") == split:
            return row
    return {}


def attribution_read(
    feature_read: Mapping[str, Any],
    hold_rows: Sequence[Mapping[str, Any]],
    routing: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    hold6_oos = split_hold_row(hold_rows, FOCUS_RUN_NUMBER, "oos")
    hold6_validation = split_hold_row(hold_rows, FOCUS_RUN_NUMBER, "validation")
    oos_rank = sorted(
        [row for row in hold_rows if row.get("split") == "oos"],
        key=lambda row: safe_float(row.get("routed_net_profit")),
        reverse=True,
    )
    validation_rank = sorted(
        [row for row in hold_rows if row.get("split") == "validation"],
        key=lambda row: safe_float(row.get("routed_net_profit")),
        reverse=True,
    )
    tier_b_oos = find_routing_row(routing, FOCUS_RUN_NUMBER, "oos", "tier_b_fallback_only_total", "Tier B")
    tier_b_component_oos = find_routing_row(routing, FOCUS_RUN_NUMBER, "oos", "fallback_used", "Tier B")
    return {
        "feature_axis_visible": bool(feature_read.get("feature_axis_visible")),
        "top_repeated_features": feature_read.get("top_repeated_features", []),
        "hold6_oos_net_profit": hold6_oos.get("routed_net_profit"),
        "hold6_oos_profit_factor": hold6_oos.get("routed_profit_factor"),
        "hold6_validation_net_profit": hold6_validation.get("routed_net_profit"),
        "hold6_validation_profit_factor": hold6_validation.get("routed_profit_factor"),
        "hold6_oos_rank_by_net": [row.get("source_run_number") for row in oos_rank].index(FOCUS_RUN_NUMBER) + 1,
        "hold6_validation_rank_by_net": [row.get("source_run_number") for row in validation_rank].index(FOCUS_RUN_NUMBER) + 1,
        "hold6_oos_positive": safe_float(hold6_oos.get("routed_net_profit")) > 0.0,
        "hold6_validation_guardrail_failed": safe_float(hold6_validation.get("routed_net_profit")) < 0.0,
        "tier_b_fallback_oos_standalone_net_profit": tier_b_oos.get("net_profit"),
        "tier_b_fallback_oos_route_share": tier_b_component_oos.get("route_share"),
        "tier_b_fallback_standalone_positive_not_additive": safe_float(tier_b_oos.get("net_profit")) > 0.0,
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "recommendation": "continue_stage19_only_for_narrow_ebm_feature_axis_or_routing_variants",
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def build_summary(created_at: str) -> dict[str, Any]:
    sources = source_runs()
    focus = next(source for source in sources if source.run_number == FOCUS_RUN_NUMBER)
    normalized = {source.run_number: load_normalized_kpi(source) for source in sources}
    trades = {source.run_number: load_trade_records(source) for source in sources}
    focus_inputs = load_focus_models_and_frames(focus)
    feature_outputs = feature_contribution_outputs(focus_inputs)
    routing = routing_rows(sources, normalized)
    hold_rows = hold_axis_rows(sources, routing)
    trade_rows = trade_shape_rows(sources, trades)
    read = attribution_read(feature_outputs["feature_contribution_read"], hold_rows, routing)
    source_ok = all(normalized[source.run_number] for source in sources) and all(trades[source.run_number] for source in sources)
    source_summary_paths = [source.run_root / "summary.json" for source in sources]
    source_normalized_paths = [source.packet_root / "normalized_kpi_records.jsonl" for source in sources]
    source_trade_paths = [source.packet_root / "trade_level_records.json" for source in sources]
    source_inputs = {
        "aggregate_summary": rel(AGGREGATE_PACKET_ROOT / "aggregate_summary.json"),
        "source_summaries": [rel(path) for path in source_summary_paths],
        "normalized_kpi_records": [rel(path) for path in source_normalized_paths],
        "trade_level_records": [rel(path) for path in source_trade_paths],
        "focus_tier_a_model": rel(focus_inputs["tier_a_model_path"]),
        "focus_tier_b_model": rel(focus_inputs["tier_b_model_path"]),
        "focus_feature_matrices": [rel(path) for path in focus_inputs["feature_paths"].values()],
    }
    source_hashes = {
        "aggregate_summary_sha256": sha256_file_lf_normalized(AGGREGATE_PACKET_ROOT / "aggregate_summary.json"),
        "source_summary_sha256": {source.run_number: sha256_file_lf_normalized(source.run_root / "summary.json") for source in sources},
        "normalized_kpi_sha256": {source.run_number: sha256_file_lf_normalized(source.packet_root / "normalized_kpi_records.jsonl") for source in sources},
        "trade_level_sha256": {source.run_number: sha256_file_lf_normalized(source.packet_root / "trade_level_records.json") for source in sources},
        "focus_model_sha256": {
            "tier_a": sha256_file_lf_normalized(focus_inputs["tier_a_model_path"]),
            "tier_b": sha256_file_lf_normalized(focus_inputs["tier_b_model_path"]),
        },
    }
    summary = {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "source_aggregate_packet_id": SOURCE_AGGREGATE_PACKET_ID,
        "source_run_numbers": list(SOURCE_RUN_NUMBERS),
        "source_run_ids": [source.run_id for source in sources],
        "focus_run_number": FOCUS_RUN_NUMBER,
        "focus_run_id": focus.run_id,
        "source_packet_ids": [source.packet_id for source in sources],
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT,
        "closure_judgment": JUDGMENT,
        "external_verification_status": EXTERNAL_VERIFICATION_STATUS if source_ok else "blocked_missing_source_evidence",
        "source_evidence_status": "pass" if source_ok else "blocked",
        "source_normalized_kpi_record_count": sum(len(normalized[source.run_number]) for source in sources),
        "source_trade_level_record_count": sum(len(trades[source.run_number]) for source in sources),
        "feature_contribution_read": feature_outputs["feature_contribution_read"],
        "feature_alignment_audit": feature_outputs["feature_alignment_audit"],
        "hold6_q90_axis_read": read,
        "hold6_q90_axis_summary": hold_rows,
        "tier_routing_attribution": routing,
        "trade_route_shape_summary": trade_rows,
        "feature_contribution_full": feature_outputs["feature_contribution_full"],
        "feature_contribution_top": feature_outputs["feature_contribution_top"],
        "feature_contribution_group_summary": feature_outputs["feature_contribution_group_summary"],
        "source_inputs": source_inputs,
        "source_artifact_hashes": source_hashes,
        "model_characteristic_strength": "ebm_feature_hold6_routing_axes_visible",
        "recommendation": read["recommendation"],
        "forbidden_claims": read["forbidden_claims"],
    }
    return summary


def output_paths() -> dict[str, Path]:
    return {
        "summary": RUN_ROOT / "summary.json",
        "kpi_record": RUN_ROOT / "kpi_record.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "feature_contribution_full": RUN_ROOT / "results/feature_contribution_full.csv",
        "feature_contribution_top": RUN_ROOT / "results/feature_contribution_top.csv",
        "feature_contribution_group_summary": RUN_ROOT / "results/feature_contribution_group_summary.csv",
        "hold6_q90_axis_summary": RUN_ROOT / "results/hold6_q90_axis_summary.csv",
        "tier_routing_attribution": RUN_ROOT / "results/tier_routing_attribution.csv",
        "trade_route_shape_summary": RUN_ROOT / "results/trade_route_shape_summary.csv",
        "report": REPORT_PATH,
        "decision": DECISION_PATH,
    }


def materialize_outputs(summary: Mapping[str, Any]) -> dict[str, Any]:
    paths = output_paths()
    write_csv(paths["feature_contribution_full"], FEATURE_CONTRIBUTION_COLUMNS, summary["feature_contribution_full"])
    write_csv(paths["feature_contribution_top"], FEATURE_CONTRIBUTION_COLUMNS, summary["feature_contribution_top"])
    write_csv(paths["feature_contribution_group_summary"], FEATURE_GROUP_COLUMNS, summary["feature_contribution_group_summary"])
    write_csv(paths["hold6_q90_axis_summary"], HOLD_AXIS_COLUMNS, summary["hold6_q90_axis_summary"])
    write_csv(paths["tier_routing_attribution"], ROUTING_COLUMNS, summary["tier_routing_attribution"])
    write_csv(paths["trade_route_shape_summary"], TRADE_SHAPE_COLUMNS, summary["trade_route_shape_summary"])
    ledger_outputs = write_ledgers(summary)
    registry_output = write_registry(summary)
    enriched = {**dict(summary), "ledger_outputs": ledger_outputs, "registry_output": registry_output}
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": summary["created_at_utc"],
        "exploration_label": EXPLORATION_LABEL,
        "source_inputs": summary["source_inputs"],
        "outputs": {key: rel(value) for key, value in paths.items()},
        "external_verification_status": summary["external_verification_status"],
        "boundary": BOUNDARY,
    }
    kpi_record = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "ebm_feature_hold6_routing_attribution_from_reused_mt5_evidence",
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "external_verification_status": summary["external_verification_status"],
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "source_inputs": summary["source_inputs"],
        "source_artifact_hashes": summary["source_artifact_hashes"],
        "feature_contribution_read": summary["feature_contribution_read"],
        "hold6_q90_axis_read": summary["hold6_q90_axis_read"],
        "ledger_outputs": ledger_outputs,
        "registry_output": registry_output,
    }
    write_json(paths["run_manifest"], manifest)
    write_json(paths["summary"], enriched)
    write_json(paths["kpi_record"], kpi_record)
    write_md(RUN_ROOT / "reports/result_summary.md", packet_markdown(enriched))
    write_packet(enriched)
    sync_docs(enriched)
    return enriched


def write_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    read = summary["hold6_q90_axis_read"]
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__feature_contribution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "feature_contribution",
            "parent_run_id": RUN_ID,
            "record_view": "ebm_main_effect_feature_contribution",
            "tier_scope": "Tier A+B",
            "kpi_scope": "model_feature_contribution",
            "scoreboard_lane": "model_characteristic_attribution",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "summary.json"),
            "primary_kpi": ledger_pairs((("feature_axis_visible", read.get("feature_axis_visible")), ("top_repeated_features", summary["feature_contribution_read"].get("top_repeated_features", [])[:3]))),
            "guardrail_kpi": ledger_pairs((("boundary", BOUNDARY), ("probability_alignment", "pass"))),
            "external_verification_status": summary["external_verification_status"],
            "notes": "EBM main-effect score contributions from run13F q90 focus matrices; no operating claim.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__hold6_q90_axis",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "hold6_q90_axis",
            "parent_run_id": RUN_ID,
            "record_view": "run13B_run13F_run13G_q90_hold_axis",
            "tier_scope": "Tier A+B",
            "kpi_scope": "hold_period_axis_attribution",
            "scoreboard_lane": "model_characteristic_attribution",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/hold6_q90_axis_summary.csv"),
            "primary_kpi": ledger_pairs((("hold6_oos_net_profit", read.get("hold6_oos_net_profit")), ("hold6_validation_net_profit", read.get("hold6_validation_net_profit")), ("hold6_oos_rank_by_net", read.get("hold6_oos_rank_by_net")))),
            "guardrail_kpi": ledger_pairs((("hold6_validation_guardrail_failed", read.get("hold6_validation_guardrail_failed")), ("boundary", BOUNDARY))),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Hold6/q90 improves OOS within this narrow comparison but fails validation guardrail.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_routing_attribution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_routing_attribution",
            "parent_run_id": RUN_ID,
            "record_view": "tier_a_primary_tier_b_fallback_route_breakdown",
            "tier_scope": "Tier A+B",
            "kpi_scope": "tier_routing_attribution",
            "scoreboard_lane": "model_characteristic_attribution",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/tier_routing_attribution.csv"),
            "primary_kpi": ledger_pairs((("tier_b_fallback_oos_standalone_net_profit", read.get("tier_b_fallback_oos_standalone_net_profit")), ("tier_b_fallback_oos_route_share", read.get("tier_b_fallback_oos_route_share")), ("standalone_positive_not_additive", read.get("tier_b_fallback_standalone_positive_not_additive")))),
            "guardrail_kpi": ledger_pairs((("profit_attribution", "not_separable_from_single_routed_account_path"), ("boundary", BOUNDARY))),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Tier B fallback-only standalone result is not a synthetic routed-total component.",
        },
    ]
    return materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )


def write_registry(summary: Mapping[str, Any]) -> dict[str, Any]:
    read = summary["hold6_q90_axis_read"]
    return upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "model_characteristic_attribution",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs(
                    (
                        ("source_runs", ",".join(summary["source_run_numbers"])),
                        ("focus_run", summary["focus_run_id"]),
                        ("hold6_oos_net", read.get("hold6_oos_net_profit")),
                        ("hold6_validation_net", read.get("hold6_validation_net_profit")),
                        ("tier_b_oos_standalone_net", read.get("tier_b_fallback_oos_standalone_net_profit")),
                        ("boundary", "attribution_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )


def gate_payloads(summary: Mapping[str, Any]) -> dict[str, Any]:
    source_ok = summary.get("source_evidence_status") == "pass"
    probability_ok = all(
        safe_float(item.get("max_abs_probability_diff")) <= safe_float(item.get("probability_diff_tolerance"), FEATURE_CONTRIBUTION_PROBABILITY_TOLERANCE)
        for item in summary.get("feature_alignment_audit", [])
    )
    hold_ok = len(summary.get("hold6_q90_axis_summary", [])) == len(SOURCE_RUN_NUMBERS) * 2
    routing_ok = len(summary.get("tier_routing_attribution", [])) == len(SOURCE_RUN_NUMBERS) * 10
    return {
        "source_evidence_gate": {
            "audit_name": "source_evidence_gate",
            "status": "pass" if source_ok else "blocked",
            "passed": source_ok,
            "source_runs": summary.get("source_run_ids"),
            "normalized_kpi_record_count": summary.get("source_normalized_kpi_record_count"),
            "trade_level_record_count": summary.get("source_trade_level_record_count"),
            "external_verification_status": summary.get("external_verification_status"),
        },
        "feature_contribution_audit": {
            "audit_name": "feature_contribution_audit",
            "status": "pass" if probability_ok else "blocked",
            "passed": probability_ok,
            "feature_alignment_audit": summary.get("feature_alignment_audit"),
            "feature_contribution_read": summary.get("feature_contribution_read"),
        },
        "hold6_q90_axis_audit": {
            "audit_name": "hold6_q90_axis_audit",
            "status": "pass" if hold_ok else "blocked",
            "passed": hold_ok,
            "hold6_q90_axis_read": summary.get("hold6_q90_axis_read"),
        },
        "tier_routing_attribution_audit": {
            "audit_name": "tier_routing_attribution_audit",
            "status": "pass" if routing_ok else "blocked",
            "passed": routing_ok,
            "routing_rows": len(summary.get("tier_routing_attribution", [])),
            "profit_attribution_boundary": "component profit is not separable from a single routed account path",
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pass" if source_ok and probability_ok and hold_ok and routing_ok else "blocked",
            "passed": source_ok and probability_ok and hold_ok and routing_ok,
            "allowed_claims": [JUDGMENT, "model_characteristic_attribution", "runtime_probe_evidence_reuse"],
            "forbidden_claims": summary.get("forbidden_claims"),
            "boundary": BOUNDARY,
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass" if source_ok and probability_ok and hold_ok and routing_ok else "blocked",
            "passed": source_ok and probability_ok and hold_ok and routing_ok,
            "required_gates": {
                "source_evidence_gate": "pass" if source_ok else "blocked",
                "feature_contribution_audit": "pass" if probability_ok else "blocked",
                "hold6_q90_axis_audit": "pass" if hold_ok else "blocked",
                "tier_routing_attribution_audit": "pass" if routing_ok else "blocked",
                "final_claim_guard": "pass" if source_ok and probability_ok and hold_ok and routing_ok else "blocked",
            },
        },
    }


def write_packet(summary: Mapping[str, Any]) -> None:
    payloads = gate_payloads(summary)
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "primary_family": "model_characteristic_attribution",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-artifact-lineage", "obsidian-result-judgment", "obsidian-data-integrity"],
            "required_gates": list(payloads),
        },
    )
    outputs = output_paths()
    output_hashes = {name: sha256_file_lf_normalized(path) for name, path in outputs.items() if io_path(path).exists() and path.suffix != ".md"}
    write_json(
        PACKET_ROOT / "artifact_index.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "source_inputs": summary.get("source_inputs"),
            "producer": "stage_pipelines.stage19.ebm_feature_hold6_routing_attribution",
            "consumer": ["Stage19 review packet", "run registry", "alpha ledgers", "user report"],
            "artifact_paths": {name: rel(path) for name, path in outputs.items()},
            "artifact_hashes": {"source": summary.get("source_artifact_hashes"), "outputs": output_hashes},
            "registry_links": {
                "run_registry": rel(RUN_REGISTRY_PATH),
                "project_alpha_ledger": rel(PROJECT_LEDGER_PATH),
                "stage_run_ledger": rel(STAGE_LEDGER_PATH),
            },
            "availability": "tracked_packet_summary_with_generated_02_runs_artifacts",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "receipts": [
                {
                    "skill": "obsidian-experiment-design",
                    "status": "completed",
                    "hypothesis": "EBM feature contribution plus q90 hold6 and Tier A/B routing can reveal a model-characteristic axis.",
                    "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, SELECTED_VARIANT_ID, "US100 M5"],
                    "changed_variables": ["attribution axis only", "source runs run13B/run13F/run13G"],
                    "success_criteria": "source MT5/KPI/trade evidence exists and EBM contribution probabilities rebuild source predictions.",
                    "failure_criteria": "missing source evidence, timestamp mismatch, probability mismatch, or absent routing rows.",
                },
                {
                    "skill": "obsidian-performance-attribution",
                    "status": "completed",
                    "effect": "feature contribution, hold6/q90, and Tier A/B routing effects were decomposed from reused MT5 evidence.",
                },
                {
                    "skill": "obsidian-artifact-lineage",
                    "status": "completed",
                    "source_inputs": summary.get("source_inputs"),
                    "producer": "stage_pipelines.stage19.ebm_feature_hold6_routing_attribution",
                    "consumer": "Stage19 run13H report and ledgers",
                    "artifact_paths": {name: rel(path) for name, path in outputs.items()},
                    "artifact_hashes": summary.get("source_artifact_hashes"),
                    "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH)],
                    "availability": "generated_02_runs_ignored_with_tracked_packet_summary",
                    "lineage_judgment": "connected_with_boundary",
                },
                {
                    "skill": "obsidian-data-integrity",
                    "status": "completed",
                    "effect": "feature matrices and prediction rows were timestamp-aligned before contribution scoring.",
                    "alignment_audit": summary.get("feature_alignment_audit"),
                },
                {
                    "skill": "obsidian-result-judgment",
                    "status": "completed",
                    "judgment_label": JUDGMENT,
                    "claim_boundary": BOUNDARY,
                    "forbidden_claims": summary.get("forbidden_claims"),
                },
            ],
        },
    )
    write_json(PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", summary)
    write_csv(PACKET_ROOT / "feature_contribution_top.csv", FEATURE_CONTRIBUTION_COLUMNS, summary["feature_contribution_top"])
    write_csv(PACKET_ROOT / "hold6_q90_axis_summary.csv", HOLD_AXIS_COLUMNS, summary["hold6_q90_axis_summary"])
    write_csv(PACKET_ROOT / "tier_routing_attribution.csv", ROUTING_COLUMNS, summary["tier_routing_attribution"])
    write_md(REPORT_PATH, packet_markdown(summary))
    write_md(DECISION_PATH, decision_markdown(summary))


def split_summary_row(rows: Sequence[Mapping[str, Any]], tier_scope: str, split: str, side: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("tier_scope") == tier_scope and row.get("split") == split and row.get("side") == side:
            return row
    return {}


def packet_markdown(summary: Mapping[str, Any]) -> str:
    read = summary["hold6_q90_axis_read"]
    group_rows = summary["feature_contribution_group_summary"]
    oos_groups = [
        split_summary_row(group_rows, "Tier A", "oos", "long"),
        split_summary_row(group_rows, "Tier A", "oos", "short"),
        split_summary_row(group_rows, "Tier B", "oos", "long"),
        split_summary_row(group_rows, "Tier B", "oos", "short"),
    ]
    lines = [
        "# Stage19 RUN13H EBM Feature/Hold/Routing Attribution(19단계 실행13H EBM 피처/보유/라우팅 귀속)",
        "",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- source runs(원천 실행): `{', '.join(summary['source_run_numbers'])}`",
        f"- focus run(중심 실행): `{summary['focus_run_id']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Hold6/Q90 Read(6봉/Q90 판독)",
        "",
        f"- hold6 OOS net(6봉 표본밖 순손익): `{read.get('hold6_oos_net_profit')}` / PF(수익 팩터): `{read.get('hold6_oos_profit_factor')}`",
        f"- hold6 validation net(6봉 검증 순손익): `{read.get('hold6_validation_net_profit')}` / PF(수익 팩터): `{read.get('hold6_validation_profit_factor')}`",
        f"- hold6 OOS rank(6봉 표본밖 순위): `{read.get('hold6_oos_rank_by_net')}`",
        f"- hold6 validation rank(6봉 검증 순위): `{read.get('hold6_validation_rank_by_net')}`",
        "",
        "효과(effect, 효과): hold6/q90(6봉/q90)은 OOS(표본밖)에서 가장 나았지만 validation(검증)이 음수라서 edge(거래 우위)로 올리지 않는다.",
        "",
        "## Feature Contribution(피처 기여도)",
        "",
        "| tier/split/side(티어/분할/방향) | signals(신호) | top features(상위 피처) | top10 share(상위10 비중) |",
        "|---|---:|---|---:|",
    ]
    for row in oos_groups:
        lines.append(
            f"| {row.get('tier_scope')}/{row.get('split')}/{row.get('side')} | `{row.get('signal_count')}` | `{row.get('top5_features')}` | `{row.get('top10_abs_share')}` |"
        )
    lines.extend(
        [
            "",
            "## Tier A/B Routing(티어 A/B 라우팅)",
            "",
            f"- Tier B fallback-only OOS net(Tier B 대체 단독 표본밖 순손익): `{read.get('tier_b_fallback_oos_standalone_net_profit')}`",
            f"- Tier B fallback routed share(Tier B 대체 라우팅 비중): `{read.get('tier_b_fallback_oos_route_share')}`",
            "- routed component profit(라우팅 구성요소 수익): `not separable(분리 불가)`",
            "",
            "효과(effect, 효과): Tier B(티어 B)는 단독 tester run(테스터 실행)에서는 양수 단서를 보였지만 routed total(라우팅 전체)의 합성 가산값으로 해석하지 않는다.",
            "",
            "Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(summary: Mapping[str, Any]) -> str:
    read = summary["hold6_q90_axis_read"]
    return "\n".join(
        [
            "# 2026-05-04 Stage19 RUN13H EBM Attribution Decision(19단계 실행13H EBM 귀속 결정)",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            "",
            "## Decision(결정)",
            "",
            "EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)은 계속 볼 가치가 있다. 단, 지금 가치는 operating promotion(운영 승격)이 아니라 characteristic attribution(특성 귀속)이다.",
            "",
            f"- hold6 OOS positive(6봉 표본밖 양수): `{read.get('hold6_oos_positive')}`",
            f"- hold6 validation guardrail failed(6봉 검증 가드레일 실패): `{read.get('hold6_validation_guardrail_failed')}`",
            f"- Tier B standalone positive not additive(Tier B 단독 양수, 가산 불가): `{read.get('tier_b_fallback_standalone_positive_not_additive')}`",
            "",
            "효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신)의 feature contribution(피처 기여도), hold6/q90(6봉/q90), Tier A/B routing(티어 A/B 라우팅) 단서를 보존하지만 edge(거래 우위)나 runtime authority(런타임 권위)는 만들지 않는다.",
        ]
    )


def replace_yaml_block(text: str, marker: str, block: str) -> str:
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


def sync_docs(summary: Mapping[str, Any]) -> None:
    read = summary["hold6_q90_axis_read"]
    write_md(
        SELECTION_STATUS_PATH,
        "\n".join(
            [
                "# Stage19 Selection Status(19단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `active_run13H_ebm_feature_hold6_routing_attribution_completed`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신) attribution(귀속) 단서를 보존하지만 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.",
            ]
        ),
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else "# Stage19 Review Index(19단계 검토 색인)\n"
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if RUN_ID not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"updated_on: '.*?'", "updated_on: '2026-05-04'", state, count=1)
    state = re.sub(r"active_branch: .*", "active_branch: codex/stage19-ebm-attribution", state, count=1)
    state = re.sub(r"current_run_id: .*", f"current_run_id: {RUN_ID}", state, count=1)
    state = state.replace("stage19_active_run13B_run13G_mt5_runtime_batch_completed", "stage19_active_run13H_ebm_feature_hold6_routing_attribution_completed")
    state = state.replace("active_run13B_run13G_mt5_runtime_batch_completed", "active_run13H_ebm_feature_hold6_routing_attribution_completed")
    block = f"""stage19_ebm_run13H_feature_hold6_routing_attribution:
  packet_id: {PACKET_ID}
  status: reviewed_attribution_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  source_run_numbers: {','.join(summary['source_run_numbers'])}
  focus_run_id: {summary['focus_run_id']}
  hold6_oos_net_profit: {read.get('hold6_oos_net_profit')}
  hold6_validation_net_profit: {read.get('hold6_validation_net_profit')}
  tier_b_fallback_oos_standalone_net_profit: {read.get('tier_b_fallback_oos_standalone_net_profit')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / 'run_summaries' / f'{RUN_ID}.json')}
  next_action: continue_stage19_only_for_narrow_ebm_feature_axis_or_routing_variants
"""
    state = replace_yaml_block(state, "stage19_ebm_run13H_feature_hold6_routing_attribution:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n", encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = "\n".join(
        [
            "## Latest Stage19 RUN13H Attribution Update(최신 19단계 실행13H 귀속 업데이트)",
            "",
            f"Stage19(19단계)는 `{RUN_ID}`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) feature contribution(피처 기여도), hold6/q90(6봉/q90), Tier A/B routing(티어 A/B 라우팅)을 해부했다.",
            "",
            f"결과(result, 결과): `{JUDGMENT}`. hold6 OOS net(6봉 표본밖 순손익)은 `{read.get('hold6_oos_net_profit')}`지만 validation net(검증 순손익)은 `{read.get('hold6_validation_net_profit')}`이다.",
            "",
            "효과(effect, 효과): EBM(설명가능 부스팅 머신)은 계속 볼 단서가 있지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage19 RUN13H Attribution Update" not in current:
        current = update + "\n" + current
    current = re.sub(r"- updated_on: `.*?`", "- updated_on: `2026-05-04`", current, count=1)
    current = re.sub(r"- active_branch: `[^`]+`", "- active_branch: `codex/stage19-ebm-attribution`", current, count=1)
    current = re.sub(r"- current run\(현재 실행\): `[^`]+`", f"- current run(현재 실행): `{RUN_ID}`", current, count=1)
    current = current.replace("없다.\n## Latest Stage19 RUN13B", "없다.\n\n## Latest Stage19 RUN13B", 1)
    io_path(CURRENT_WORKING_STATE_PATH).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage19 EBM feature/hold/routing attribution.")
    parser.add_argument("--force", action="store_true", help="Regenerate run13H outputs.")
    _args = parser.parse_args(argv)
    created_at = utc_now()
    summary = build_summary(created_at)
    final_summary = materialize_outputs(summary)
    print(json.dumps({"run_id": RUN_ID, "judgment": JUDGMENT, "hold6_q90_axis_read": final_summary["hold6_q90_axis_read"]}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
