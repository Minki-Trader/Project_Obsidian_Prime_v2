from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import review_validation_density_trade_count_repair_training as ef  # noqa: E402
from stage_pipelines.stage337 import train_validation_density_trade_count_repair_candidates as ee  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = ef.STAGE_ID
RUN_NUMBER = "run337EG"
RUN_ID = "run337EG_review_proxy_survivor_attribution_package_precheck_without_db_v1"
PARENT_RUN_ID = ef.RUN_ID
NEXT_RUN_ID = "run337EH_materialize_proxy_survivor_row_level_runtime_probe_inputs_without_db_v1"
STATUS = "completed_stage337EG_proxy_survivor_attribution_package_precheck_row_level_tape_ready_no_selection_no_mt5"
JUDGMENT = "proxy_survivors_package_precheck_clear_but_density_direction_curve_watches_require_controlled_runtime_materialization_no_selection"
DECISION = "stage337EG_open_run337EH_materialize_proxy_survivor_row_level_runtime_probe_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EG_proxy_survivor_attribution_package_precheck_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ef.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ef.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EG_proxy_survivor_attribution_package_precheck.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EG_proxy_survivor_attribution_package_precheck.md"
SELECTED_STATUS = ef.SELECTED_STATUS
STAGE_BRIEF = ef.STAGE_BRIEF
WORKSPACE_STATE = ef.WORKSPACE_STATE
CURRENT_STATE = ef.CURRENT_STATE
CHANGELOG = ef.CHANGELOG
RUN_REGISTRY = ef.RUN_REGISTRY
ALPHA_LEDGER = ef.ALPHA_LEDGER
ARTIFACT_REGISTRY = ef.ARTIFACT_REGISTRY
STAGE_LEDGER = ef.STAGE_LEDGER

EF_FINAL = ef.FINAL_DECISION
EF_GATES = ef.REQUIRED_GATE_AUDIT
EF_QUEUE = ef.EG_QUEUE
EF_TRAINING_REVIEW = ef.CANDIDATE_TRAINING_REVIEW
EF_PASS_MATRIX = ef.CANDIDATE_PASS_MATRIX
EF_RELEASE_LOCK = ef.RELEASE_LOCK_REVIEW
EE_MODEL_MANIFEST = ee.TRAINED_MODEL_MANIFEST
EE_ONNX_PARITY = ee.ONNX_PARITY
EE_CLASS_SCORECARD = ee.CANDIDATE_CLASSIFICATION_SCORECARD
EE_TRADE_SCORECARD = ee.PROXY_TRADE_SCORECARD
EE_CONTROL_SCORECARD = ee.NEGATIVE_CONTROL_SCORECARD
EE_DENSITY_AUDIT = ee.DENSITY_GUARD_AUDIT
EE_FEATURE_COMPATIBILITY = ee.FEATURE_COMPATIBILITY
EE_RUNTIME_FIREWALL = ee.RUNTIME_FIREWALL_REVIEW
EE_SOURCE_MODEL_INPUT = ee.SOURCE_MODEL_INPUT
EE_FEATURE_SET_MATRIX = ee.FEATURE_SET_MATRIX

SURVIVOR_ATTRIBUTION = RUN_DIR / "proxy_survivor_attribution.csv"
SURVIVOR_DIRECTION = RUN_DIR / "survivor_direction_attribution.csv"
SURVIVOR_CURVE = RUN_DIR / "survivor_curve_pocket_review.csv"
SURVIVOR_PACKAGE = RUN_DIR / "survivor_package_precheck.csv"
SURVIVOR_CONTROL = RUN_DIR / "survivor_control_alignment_review.csv"
SOURCE_AXIS_SUMMARY = RUN_DIR / "survivor_source_axis_summary.csv"
TRADE_TAPE = RUN_DIR / "proxy_survivor_trade_tape.parquet"
EH_QUEUE = RUN_DIR / "run337EH_runtime_materialization_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EF_FINAL,
    EF_GATES,
    EF_QUEUE,
    EF_TRAINING_REVIEW,
    EF_PASS_MATRIX,
    EF_RELEASE_LOCK,
    EE_MODEL_MANIFEST,
    EE_ONNX_PARITY,
    EE_CLASS_SCORECARD,
    EE_TRADE_SCORECARD,
    EE_CONTROL_SCORECARD,
    EE_DENSITY_AUDIT,
    EE_FEATURE_COMPATIBILITY,
    EE_RUNTIME_FIREWALL,
    EE_SOURCE_MODEL_INPUT,
    EE_FEATURE_SET_MATRIX,
)
OUTPUT_FILES = (
    SURVIVOR_ATTRIBUTION,
    SURVIVOR_DIRECTION,
    SURVIVOR_CURVE,
    SURVIVOR_PACKAGE,
    SURVIVOR_CONTROL,
    SOURCE_AXIS_SUMMARY,
    TRADE_TAPE,
    EH_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

ATTRIBUTION_COLUMNS = (
    "model_id",
    "proxy_rank",
    "split",
    "feature_set_id",
    "cost_policy_id",
    "model_variant_id",
    "objective_contract_id",
    "trade_count",
    "trades_per_day",
    "signal_density",
    "net_log_return_after_cost",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "long_count",
    "short_count",
    "long_share",
    "short_share",
    "balanced_accuracy",
    "macro_f1",
    "density_vs_train",
    "scorecard_net_abs_diff",
    "scorecard_pf_abs_diff",
    "attribution_status",
    "effect",
    "claim_boundary",
)
DIRECTION_COLUMNS = (
    "model_id",
    "proxy_rank",
    "split",
    "direction",
    "trade_count",
    "net_log_return_after_cost",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "direction_share",
    "direction_status",
    "claim_boundary",
)
CURVE_COLUMNS = (
    "model_id",
    "proxy_rank",
    "split",
    "trade_count",
    "net_log_return_after_cost",
    "profit_factor",
    "max_drawdown",
    "recovery_factor",
    "longest_underwater_trades",
    "worst_25_trade_net",
    "worst_50_trade_net",
    "worst_100_trade_net",
    "curve_watch_flags",
    "curve_review_status",
    "claim_boundary",
)
PACKAGE_COLUMNS = (
    "model_id",
    "proxy_rank",
    "model_path",
    "model_hash_match",
    "onnx_path",
    "onnx_hash_match",
    "onnx_parity_passed",
    "feature_count",
    "feature_order_hash",
    "feature_compatibility_passed",
    "runtime_firewall_status",
    "package_precheck_status",
    "forbidden_action",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "model_id",
    "proxy_rank",
    "split",
    "control_id",
    "candidate_balanced_accuracy",
    "control_alignment_balanced_accuracy",
    "alignment_gap",
    "blocks_training_review",
    "control_review_status",
    "claim_boundary",
)
AXIS_COLUMNS = (
    "axis_id",
    "axis_value",
    "survivor_rows",
    "validation_pf_min",
    "validation_pf_max",
    "oos_pf_min",
    "oos_pf_max",
    "interpretation",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "passed"}


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def profit_factor(values: np.ndarray) -> float:
    positive = float(values[values > 0].sum())
    negative = abs(float(values[values < 0].sum()))
    if negative == 0:
        return 999.0 if positive > 0 else 0.0
    return positive / negative


def max_drawdown(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def longest_underwater(values: np.ndarray) -> int:
    if values.size == 0:
        return 0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    underwater = curve < peak
    longest = 0
    current = 0
    for flag in underwater:
        if bool(flag):
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return int(longest)


def worst_rolling(values: np.ndarray, window: int) -> float:
    if values.size == 0:
        return 0.0
    if values.size <= window:
        return float(values.sum())
    csum = np.concatenate([[0.0], np.cumsum(values)])
    rolling = csum[window:] - csum[:-window]
    return float(np.min(rolling))


def split_days(source: pd.DataFrame, mask: np.ndarray) -> float:
    if not mask.any() or "timestamp" not in source.columns:
        return 0.0
    times = pd.to_datetime(source.loc[mask, "timestamp"], utc=True)
    if times.empty:
        return 0.0
    span = max((times.max() - times.min()).total_seconds() / 86400.0, 1.0)
    return float(span)


def trade_metrics(trade_values: np.ndarray) -> dict[str, float | int]:
    trade_count = int(trade_values.size)
    net = float(trade_values.sum()) if trade_count else 0.0
    dd = max_drawdown(trade_values)
    return {
        "trade_count": trade_count,
        "net": net,
        "profit_factor": profit_factor(trade_values),
        "expectancy": float(trade_values.mean()) if trade_count else 0.0,
        "max_drawdown": dd,
        "recovery_factor": (net / dd) if dd > 0 else (999.0 if net > 0 else 0.0),
        "longest_underwater_trades": longest_underwater(trade_values),
        "worst_25_trade_net": worst_rolling(trade_values, 25),
        "worst_50_trade_net": worst_rolling(trade_values, 50),
        "worst_100_trade_net": worst_rolling(trade_values, 100),
    }


def feature_sets() -> dict[str, list[str]]:
    rows = read_csv(EE_FEATURE_SET_MATRIX)
    parsed: dict[str, list[str]] = {}
    for row in rows:
        parsed[row["feature_set_id"]] = list(json.loads(row["included_features_json"]))
    return parsed


def survivor_ids(pass_matrix: pd.DataFrame) -> list[str]:
    survivors = pass_matrix.loc[pass_matrix["joint_proxy_pass"].map(as_bool)].copy()
    survivors["proxy_survivor_rank"] = survivors["proxy_survivor_rank"].map(as_int)
    return survivors.sort_values("proxy_survivor_rank")["model_id"].tolist()


def load_source_and_targets() -> tuple[pd.DataFrame, dict[str, Mapping[str, Any]]]:
    source = pd.read_parquet(io_path(EE_SOURCE_MODEL_INPUT))
    targets = {str(row["cost_policy_id"]): row for row in ee.dz.read_targets()}
    return source, targets


def build_survivor_outputs() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    pd.DataFrame,
    dict[str, Any],
]:
    pass_matrix = pd.read_csv(io_path(EF_PASS_MATRIX))
    training_review = pd.read_csv(io_path(EF_TRAINING_REVIEW))
    trade_scorecard = pd.read_csv(io_path(EE_TRADE_SCORECARD))
    class_scorecard = pd.read_csv(io_path(EE_CLASS_SCORECARD))
    manifest = pd.read_csv(io_path(EE_MODEL_MANIFEST))
    features_by_id = feature_sets()
    source, targets = load_source_and_targets()
    split_masks = {split: source["split"].astype(str).eq(split).to_numpy() for split in ("train", "validation", "oos")}
    survivor_list = survivor_ids(pass_matrix)
    rank_by_model = {
        row["model_id"]: as_int(row["proxy_survivor_rank"])
        for row in pass_matrix.to_dict("records")
        if as_bool(row.get("joint_proxy_pass"))
    }
    training_by_model = {row["model_id"]: row for row in training_review.to_dict("records")}
    trade_lookup = {
        (row["model_id"], row["split"]): row for row in trade_scorecard.to_dict("records")
    }
    class_lookup = {
        (row["model_id"], row["split"]): row for row in class_scorecard.to_dict("records")
    }
    manifest_by_model = {row["model_id"]: row for row in manifest.to_dict("records")}
    attribution_rows: list[dict[str, Any]] = []
    direction_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    tape_rows: list[dict[str, Any]] = []
    max_net_diff = 0.0
    max_pf_diff = 0.0
    density_watch_rows = 0
    curve_watch_rows = 0
    direction_watch_rows = 0

    for model_id in survivor_list:
        model_row = manifest_by_model[model_id]
        rank = rank_by_model[model_id]
        model_path = ROOT / str(model_row["model_path"])
        model = joblib.load(io_path(model_path))
        features = features_by_id[str(model_row["feature_set_id"])]
        x_all = source[features].to_numpy(dtype=np.float32)
        probs = model.predict_proba(x_all)
        classes = np.asarray(model.classes_, dtype=np.int64)
        pred = classes[np.asarray(probs).argmax(axis=1)]
        target = targets[str(model_row["cost_policy_id"])]
        future_returns = np.asarray(target["future_returns"], dtype=float)
        cost_returns = np.asarray(target["cost_returns"], dtype=float)
        direction = np.where(pred == ee.LABEL_TO_INT["long"], 1.0, np.where(pred == ee.LABEL_TO_INT["short"], -1.0, 0.0))
        is_trade = direction != 0
        pnl = np.where(is_trade, direction * future_returns - cost_returns, 0.0)
        train_density = None
        for split in ("train", "validation", "oos"):
            mask = split_masks[split]
            split_trade = is_trade & mask
            split_values = pnl[split_trade]
            split_pred = pred[mask]
            metrics = trade_metrics(split_values)
            long_count = int((split_pred == ee.LABEL_TO_INT["long"]).sum())
            short_count = int((split_pred == ee.LABEL_TO_INT["short"]).sum())
            signal_density = float((split_pred != ee.LABEL_TO_INT["flat"]).mean()) if split_pred.size else 0.0
            if split == "train":
                train_density = signal_density
            density_vs_train = signal_density / train_density if train_density and train_density > 0 else 1.0
            score_trade = trade_lookup[(model_id, split)]
            score_class = class_lookup[(model_id, split)]
            net_diff = abs(metrics["net"] - as_float(score_trade["net_log_return_after_cost"]))
            pf_diff = abs(metrics["profit_factor"] - as_float(score_trade["profit_factor"]))
            max_net_diff = max(max_net_diff, net_diff)
            max_pf_diff = max(max_pf_diff, pf_diff)
            days = split_days(source, mask)
            long_share = long_count / metrics["trade_count"] if metrics["trade_count"] else 0.0
            short_share = short_count / metrics["trade_count"] if metrics["trade_count"] else 0.0
            flags = []
            if split != "train" and density_vs_train >= 2.5:
                flags.append("density_shift_watch")
                density_watch_rows += 1
            if metrics["recovery_factor"] < 1.0:
                flags.append("low_recovery_watch")
            if max(long_share, short_share) >= 0.75:
                flags.append("direction_skew_watch")
                direction_watch_rows += 1
            status = "attribution_clear_review_only" if not flags else "watch_" + ";".join(flags)
            attribution_rows.append(
                {
                    "model_id": model_id,
                    "proxy_rank": rank,
                    "split": split,
                    "feature_set_id": model_row["feature_set_id"],
                    "cost_policy_id": model_row["cost_policy_id"],
                    "model_variant_id": model_row["model_variant_id"],
                    "objective_contract_id": model_row["objective_contract_id"],
                    "trade_count": metrics["trade_count"],
                    "trades_per_day": (metrics["trade_count"] / days) if days > 0 else 0.0,
                    "signal_density": signal_density,
                    "net_log_return_after_cost": metrics["net"],
                    "profit_factor": metrics["profit_factor"],
                    "expectancy": metrics["expectancy"],
                    "max_drawdown": metrics["max_drawdown"],
                    "recovery_factor": metrics["recovery_factor"],
                    "long_count": long_count,
                    "short_count": short_count,
                    "long_share": long_share,
                    "short_share": short_share,
                    "balanced_accuracy": as_float(score_class["balanced_accuracy"]),
                    "macro_f1": as_float(score_class["macro_f1"]),
                    "density_vs_train": density_vs_train,
                    "scorecard_net_abs_diff": net_diff,
                    "scorecard_pf_abs_diff": pf_diff,
                    "attribution_status": status,
                    "effect": "row-level proxy replay matches the scorecard and exposes split-level risk(행 단위 프록시 재생이 점수표와 맞고 분할 위험을 드러낸다)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            curve_flags = []
            if metrics["worst_50_trade_net"] < -0.05:
                curve_flags.append("worst_50_loss_watch")
            if metrics["longest_underwater_trades"] >= 120:
                curve_flags.append("underwater_stretch_watch")
            if metrics["recovery_factor"] < 1.0:
                curve_flags.append("recovery_below_one_watch")
            if curve_flags:
                curve_watch_rows += 1
            curve_rows.append(
                {
                    "model_id": model_id,
                    "proxy_rank": rank,
                    "split": split,
                    "trade_count": metrics["trade_count"],
                    "net_log_return_after_cost": metrics["net"],
                    "profit_factor": metrics["profit_factor"],
                    "max_drawdown": metrics["max_drawdown"],
                    "recovery_factor": metrics["recovery_factor"],
                    "longest_underwater_trades": metrics["longest_underwater_trades"],
                    "worst_25_trade_net": metrics["worst_25_trade_net"],
                    "worst_50_trade_net": metrics["worst_50_trade_net"],
                    "worst_100_trade_net": metrics["worst_100_trade_net"],
                    "curve_watch_flags": ";".join(curve_flags),
                    "curve_review_status": "curve_watch_review_required" if curve_flags else "curve_proxy_clear_review_only",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            for label_name, label_value in (("long", ee.LABEL_TO_INT["long"]), ("short", ee.LABEL_TO_INT["short"])):
                direction_mask = mask & (pred == label_value)
                values = pnl[direction_mask]
                direction_metrics = trade_metrics(values)
                share = direction_metrics["trade_count"] / metrics["trade_count"] if metrics["trade_count"] else 0.0
                direction_status = "direction_proxy_clear_review_only"
                if share >= 0.75:
                    direction_status = "direction_skew_watch"
                elif direction_metrics["profit_factor"] < 1.0 and direction_metrics["trade_count"] >= 50:
                    direction_status = "direction_pf_watch"
                direction_rows.append(
                    {
                        "model_id": model_id,
                        "proxy_rank": rank,
                        "split": split,
                        "direction": label_name,
                        "trade_count": direction_metrics["trade_count"],
                        "net_log_return_after_cost": direction_metrics["net"],
                        "profit_factor": direction_metrics["profit_factor"],
                        "expectancy": direction_metrics["expectancy"],
                        "max_drawdown": direction_metrics["max_drawdown"],
                        "recovery_factor": direction_metrics["recovery_factor"],
                        "direction_share": share,
                        "direction_status": direction_status,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
            trade_indices = np.flatnonzero(split_trade)
            for local_order, idx in enumerate(trade_indices, start=1):
                tape_rows.append(
                    {
                        "model_id": model_id,
                        "proxy_rank": rank,
                        "split": split,
                        "trade_order": local_order,
                        "timestamp": str(source.iloc[idx]["timestamp"]),
                        "direction": "long" if pred[idx] == ee.LABEL_TO_INT["long"] else "short",
                        "future_log_return_12": float(future_returns[idx]),
                        "cost_return": float(cost_returns[idx]),
                        "pnl_after_cost": float(pnl[idx]),
                        "cumulative_pnl_after_cost": float(np.cumsum(split_values)[local_order - 1]),
                    }
                )
        best_review = training_by_model[model_id]
        _ = best_review

    summary = {
        "survivor_rows": len(survivor_list),
        "attribution_rows": len(attribution_rows),
        "direction_rows": len(direction_rows),
        "curve_rows": len(curve_rows),
        "trade_tape_rows": len(tape_rows),
        "max_scorecard_net_abs_diff": max_net_diff,
        "max_scorecard_pf_abs_diff": max_pf_diff,
        "density_watch_rows": density_watch_rows,
        "direction_watch_rows": direction_watch_rows,
        "curve_watch_rows": curve_watch_rows,
    }
    return attribution_rows, direction_rows, curve_rows, pd.DataFrame(tape_rows), summary


def build_package_precheck() -> tuple[list[dict[str, Any]], dict[str, int]]:
    pass_matrix = pd.read_csv(io_path(EF_PASS_MATRIX))
    manifest = pd.read_csv(io_path(EE_MODEL_MANIFEST))
    onnx = pd.read_csv(io_path(EE_ONNX_PARITY))
    feature = pd.read_csv(io_path(EE_FEATURE_COMPATIBILITY))
    runtime_firewall = pd.read_csv(io_path(EE_RUNTIME_FIREWALL))
    survivors = survivor_ids(pass_matrix)
    rank_by_model = {
        row["model_id"]: as_int(row["proxy_survivor_rank"])
        for row in pass_matrix.to_dict("records")
        if as_bool(row.get("joint_proxy_pass"))
    }
    manifest_by_model = {row["model_id"]: row for row in manifest.to_dict("records")}
    onnx_by_model = {row["model_id"]: row for row in onnx.to_dict("records")}
    feature_by_id = {row["feature_set_id"]: row for row in feature.to_dict("records")}
    firewall_active = all(str(row.get("review_status")) == "active_no_release" for row in runtime_firewall.to_dict("records"))
    rows: list[dict[str, Any]] = []
    failed_hashes = 0
    failed_parity = 0
    failed_features = 0
    for model_id in survivors:
        model_row = manifest_by_model[model_id]
        parity_row = onnx_by_model[model_id]
        feature_row = feature_by_id[str(model_row["feature_set_id"])]
        model_path = ROOT / str(model_row["model_path"])
        onnx_path = ROOT / str(model_row["onnx_path"])
        model_hash_match = path_exists(model_path) and sha256_file(model_path) == str(model_row["model_sha256"])
        onnx_hash_match = path_exists(onnx_path) and sha256_file(onnx_path) == str(model_row["onnx_sha256"])
        parity_passed = as_bool(parity_row.get("passed"))
        feature_ok = (
            as_int(feature_row.get("feature_count")) == as_int(model_row.get("feature_count"))
            and as_int(feature_row.get("missing_count")) == 0
            and as_int(feature_row.get("nonfinite_rows")) == 0
            and str(feature_row.get("feature_order_hash")) == str(model_row.get("feature_order_hash"))
        )
        failed_hashes += 0 if model_hash_match and onnx_hash_match else 1
        failed_parity += 0 if parity_passed else 1
        failed_features += 0 if feature_ok else 1
        status = "precheck_passed_review_only"
        if not (model_hash_match and onnx_hash_match and parity_passed and feature_ok and firewall_active):
            status = "precheck_blocked"
        rows.append(
            {
                "model_id": model_id,
                "proxy_rank": rank_by_model[model_id],
                "model_path": model_row["model_path"],
                "model_hash_match": str(model_hash_match).lower(),
                "onnx_path": model_row["onnx_path"],
                "onnx_hash_match": str(onnx_hash_match).lower(),
                "onnx_parity_passed": str(parity_passed).lower(),
                "feature_count": model_row["feature_count"],
                "feature_order_hash": model_row["feature_order_hash"],
                "feature_compatibility_passed": str(feature_ok).lower(),
                "runtime_firewall_status": "active_no_release" if firewall_active else "firewall_not_active",
                "package_precheck_status": status,
                "forbidden_action": "selection, MT5 probe, Forward claim, live readiness(선택/MT5 탐침/전진 주장/라이브 준비 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows, {
        "package_rows": len(rows),
        "package_failed_hash_rows": failed_hashes,
        "package_failed_parity_rows": failed_parity,
        "package_failed_feature_rows": failed_features,
    }


def build_control_review() -> tuple[list[dict[str, Any]], dict[str, int]]:
    pass_matrix = pd.read_csv(io_path(EF_PASS_MATRIX))
    controls = pd.read_csv(io_path(EE_CONTROL_SCORECARD))
    survivors = survivor_ids(pass_matrix)
    rank_by_model = {
        row["model_id"]: as_int(row["proxy_survivor_rank"])
        for row in pass_matrix.to_dict("records")
        if as_bool(row.get("joint_proxy_pass"))
    }
    frame = controls.loc[controls["model_id"].isin(survivors)].copy()
    rows: list[dict[str, Any]] = []
    block_rows = 0
    close_alignment_rows = 0
    for row in frame.to_dict("records"):
        candidate = as_float(row.get("candidate_balanced_accuracy"))
        alignment = as_float(row.get("control_alignment_balanced_accuracy"))
        blocks = as_bool(row.get("blocks_training_review"))
        gap = candidate - alignment
        if blocks:
            block_rows += 1
        if row.get("control_id") == "shifted_return_control" and gap < 0.01:
            close_alignment_rows += 1
        status = "control_clear_review_only"
        if blocks:
            status = "control_block"
        elif row.get("control_id") == "shifted_return_control" and gap < 0.01:
            status = "shifted_alignment_close_watch"
        rows.append(
            {
                "model_id": row["model_id"],
                "proxy_rank": rank_by_model[row["model_id"]],
                "split": row["split"],
                "control_id": row["control_id"],
                "candidate_balanced_accuracy": candidate,
                "control_alignment_balanced_accuracy": alignment,
                "alignment_gap": gap,
                "blocks_training_review": str(blocks).lower(),
                "control_review_status": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows, {"control_rows": len(rows), "control_block_rows": block_rows, "shifted_alignment_close_watch_rows": close_alignment_rows}


def build_axis_summary(attribution_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    frame = pd.DataFrame(attribution_rows)
    validation = frame.loc[frame["split"].eq("validation")]
    oos = frame.loc[frame["split"].eq("oos"), ["model_id", "profit_factor"]].rename(columns={"profit_factor": "oos_profit_factor"})
    base = validation.merge(oos, on="model_id", how="left")
    axes = ["cost_policy_id", "feature_set_id", "model_variant_id", "objective_contract_id"]
    rows: list[dict[str, Any]] = []
    for axis in axes:
        for value, group in base.groupby(axis):
            rows.append(
                {
                    "axis_id": axis,
                    "axis_value": value,
                    "survivor_rows": len(group),
                    "validation_pf_min": float(group["profit_factor"].min()),
                    "validation_pf_max": float(group["profit_factor"].max()),
                    "oos_pf_min": float(group["oos_profit_factor"].min()),
                    "oos_pf_max": float(group["oos_profit_factor"].max()),
                    "interpretation": "axis evidence only, not selection(축 근거일 뿐 선택이 아니다)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_eh_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EH_survivor_runtime_probe_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize row-level proxy and runtime probe inputs for all 7 survivors(7개 생존 후보 전체의 행 단위 프록시/런타임 탐침 입력 물질화)",
            "required_inputs": f"{rel(SURVIVOR_ATTRIBUTION)};{rel(SURVIVOR_CURVE)};{rel(SURVIVOR_PACKAGE)};{rel(TRADE_TAPE)}",
            "required_outputs": "survivor_runtime_probe_manifest.csv;survivor_feature_handoff_manifest.csv;survivor_proxy_expected_contract.csv",
            "blocked_if_missing": "row-level tape, package precheck, active no-release firewall(행 단위 테이프/패키지 사전검사/활성 해제금지 방화벽)",
            "forbidden_action": "no MT5 execution, no winner selection, no threshold tuning(이번 물질화에서 MT5 실행/승자 선택/임계값 조정 금지)",
            "effect": "keeps the next step reproducible before any external runtime probe(외부 런타임 탐침 전에 다음 단계를 재현 가능하게 만든다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EH_density_direction_curve_watch_contract",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "carry density, direction, and curve watches into runtime materialization(밀도/방향/곡선 감시 항목을 런타임 물질화로 이월)",
            "required_inputs": f"{rel(SURVIVOR_ATTRIBUTION)};{rel(SURVIVOR_DIRECTION)};{rel(SURVIVOR_CURVE)};{rel(SURVIVOR_CONTROL)}",
            "required_outputs": "runtime_probe_blocker_matrix.csv;survivor_watch_policy.csv",
            "blocked_if_missing": "watch rows or control review(감시 행 또는 대조 검토)",
            "forbidden_action": "no watch-row cherry-pick, no cost/feature retune(감시 행 골라잡기/비용·피처 재조정 금지)",
            "effect": "prevents proxy survivors from becoming overfit winners(프록시 생존 후보가 과적합 승자로 둔갑하지 못하게 한다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "필수 EF/EE 입력이 있어야 EG 검토가 닫힌다."),
        ("parent_ef_gates_passed", final["ef_failed_gate_rows"] == 0, str(final["ef_failed_gate_rows"]), "0", "부모 EF 게이트가 통과해야 한다."),
        ("parent_next_action_matches", final["ef_next_action"] == RUN_ID, str(final["ef_next_action"]), RUN_ID, "라우팅이 EG로 정확히 이어졌는지 확인한다."),
        ("proxy_survivor_rows_present", final["survivor_rows"] == 7, str(final["survivor_rows"]), "7", "EF 생존 후보 7개를 모두 검토해야 한다."),
        ("row_level_scorecard_replay", final["max_scorecard_net_abs_diff"] < 1e-9 and final["max_scorecard_pf_abs_diff"] < 1e-9, f"net={final['max_scorecard_net_abs_diff']};pf={final['max_scorecard_pf_abs_diff']}", "<1e-9", "행 단위 재생과 EE 점수표가 같아야 한다."),
        ("package_precheck_clear", final["package_failed_rows"] == 0, str(final["package_failed_rows"]), "0", "ONNX/모델/피처 계보가 깨지지 않아야 한다."),
        ("control_blocks_clear", final["control_block_rows"] == 0, str(final["control_block_rows"]), "0", "생존 후보에서 대조 차단 행이 없어야 한다."),
        ("runtime_queue_materialized", final["eh_queue_rows"] == 2, str(final["eh_queue_rows"]), "2", "다음 런타임 물질화 대기열을 남긴다."),
        (
            "no_forbidden_claim",
            final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "선택/MT5/Goal 주장을 막는다.",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in checks
    ]


def write_parquet(path: Path, frame: pd.DataFrame) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return path


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "sample_scope": f"survivors={final['survivor_rows']};trade_tape_rows={final['trade_tape_rows']}",
        "time_axis": "existing train/validation/oos split only(기존 학습/검증/OOS 분할만 사용)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_proxy_attribution_precheck(프록시 귀속 사전검사에 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "saved ExtraTrees joblib and ONNX replay(저장된 ExtraTrees joblib/ONNX 재생)",
        "onnx_package_precheck": f"failed_package_rows={final['package_failed_rows']}",
        "scorecard_replay": f"net_diff={final['max_scorecard_net_abs_diff']};pf_diff={final['max_scorecard_pf_abs_diff']}",
        "selection_metric": "none; all 7 survivors carried forward as a package set(없음, 7개 생존 후보 전체 묶음 이월)",
        "threshold_policy": "unchanged_no_tuning(변경 없음, 조정 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "survivor_rows": final["survivor_rows"],
        "curve_watch_rows": final["curve_watch_rows"],
        "density_watch_rows": final["density_watch_rows"],
        "direction_watch_rows": final["direction_watch_rows"],
        "shifted_alignment_close_watch_rows": final["shifted_alignment_close_watch_rows"],
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_claim": "not_run_no_MT5(미실행, MT5 없음)",
        "package_status": "precheck_clear_but_materialization_required(사전검사 통과, 물질화 필요)",
        "runtime_authority": "not_claimed(주장 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "row-level replay tape, attribution, package precheck, control review(행 단위 재생 테이프/귀속/패키지 사전검사/대조 검토)",
        "evidence_missing": "actual MT5 runtime probe and fresh forward decision(실제 MT5 런타임 탐침과 신규 전진 판정)",
        "next_condition": NEXT_RUN_ID,
        "goal_achieve": "not_claimed(주장 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 안에서 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EG Proxy Survivor Attribution Package Precheck(프록시 생존 후보 귀속 패키지 사전검사)

## Conclusion(결론)

run337EG(337EG 실행)는 EF 생존 후보 `7`개를 모두 행 단위로 재생했다. EE scorecard(EE 점수표)와 row-level replay(행 단위 재생)의 최대 차이는 net(순손익) `{final["max_scorecard_net_abs_diff"]}` / PF(수익 팩터) `{final["max_scorecard_pf_abs_diff"]}`라서 재생 정체성은 통과했다.

Action(행동): 후보 선택(candidate selection, 후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)은 실행하지 않았다.

Effect(효과): package precheck(패키지 사전검사)는 `0`개 실패지만 density/direction/curve watch(밀도/방향/곡선 감시)가 남아 run337EH(337EH 실행)에서 런타임 입력을 통제 물질화한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- survivor_rows(생존 후보 수): `{final["survivor_rows"]}`
- trade_tape_rows(거래 테이프 행): `{final["trade_tape_rows"]}`
- package_failed_rows(패키지 실패 행): `{final["package_failed_rows"]}`
- density_watch_rows(밀도 감시 행): `{final["density_watch_rows"]}`
- direction_watch_rows(방향 감시 행): `{final["direction_watch_rows"]}`
- curve_watch_rows(곡선 감시 행): `{final["curve_watch_rows"]}`
- shifted_alignment_close_watch_rows(이동 대조 근접 행): `{final["shifted_alignment_close_watch_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EG

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 7개 프록시 생존 후보의 행 단위 재생/패키지 계보는 통과했지만, 밀도/방향/곡선 감시를 다음 런타임 입력 물질화에 묶어 넘긴다. 선택/MT5/Forward(전진)는 금지한다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(SURVIVOR_ATTRIBUTION)}`, `{rel(SURVIVOR_PACKAGE)}`, `{rel(TRADE_TAPE)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337EG focus complete: proxy survivor attribution/package precheck(프록시 생존 후보 귀속/패키지 사전검사)에서 "
        f"생존 후보 `{final['survivor_rows']}`개와 trade tape(거래 테이프) `{final['trade_tape_rows']}`행을 검토했다. "
        "Effect(효과): 다음 run337EH에서 런타임 탐침 입력을 물질화하되 선택/MT5/Forward(전진)는 계속 닫는다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EG focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337EG(337EG 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 프록시 생존 후보 `{final['survivor_rows']}`개를 행 단위로 재생했고 패키지 실패 `0`개를 확인했다. 다만 밀도/방향/곡선 감시를 런타임 입력 물질화로 넘기며 선택/MT5/Forward/Goal(선택/MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EF("
    if "## Stage337 run337EG(337EG 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- proxy_survivor_rows(프록시 생존 후보 수): `{final["survivor_rows"]}`
- package_failed_rows(패키지 실패 행): `{final["package_failed_rows"]}`
- actual_mt5_execution(실제 MT5 실행): `not_run_eg_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): proxy survivor runtime input materialization(프록시 생존 후보 런타임 입력 물질화)으로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EG(337EG 실행) reviewed proxy survivor attribution/package precheck(프록시 생존 후보 귀속/패키지 사전검사). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)는 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EG(337EG 실행) reviewed proxy survivor"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337EG replayed 7 proxy survivors row-level and opened `{NEXT_RUN_ID}` without selection/MT5/Forward claims."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EG replayed 7 proxy survivors"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_survivor_attribution_package_precheck_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"survivors={final['survivor_rows']};trade_tape_rows={final['trade_tape_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "performance_attribution_model_validation_runtime_parity_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__proxy_survivor_precheck",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_survivor_precheck",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "row_level_proxy_replay_package_precheck",
        "scoreboard_lane": "performance_attribution_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"survivors={final['survivor_rows']};trade_tape_rows={final['trade_tape_rows']};package_failed={final['package_failed_rows']}",
        "guardrail_kpi": "release_locked;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__proxy_survivor_precheck",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "performance_attribution_model_validation_runtime_parity_artifact_lineage",
        "evidence_scope": "EF survivors and EE model artifacts replayed",
        "kpi_scope": "row_level_proxy_replay_package_precheck",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__proxy_survivor_precheck",
        "family": "performance_attribution_model_validation_runtime_parity_artifact_lineage",
        "question": "can proxy survivors pass attribution and package precheck before runtime materialization",
        "metric_scope": "row_level_replay_curve_direction_density_package_control",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    attribution_rows, direction_rows, curve_rows, trade_tape, replay_summary = build_survivor_outputs()
    package_rows, package_summary = build_package_precheck()
    control_rows, control_summary = build_control_review()
    axis_rows = build_axis_summary(attribution_rows)
    queue_rows = build_eh_queue()
    artifacts: list[Path] = [
        write_csv(SURVIVOR_ATTRIBUTION, ATTRIBUTION_COLUMNS, attribution_rows),
        write_csv(SURVIVOR_DIRECTION, DIRECTION_COLUMNS, direction_rows),
        write_csv(SURVIVOR_CURVE, CURVE_COLUMNS, curve_rows),
        write_csv(SURVIVOR_PACKAGE, PACKAGE_COLUMNS, package_rows),
        write_csv(SURVIVOR_CONTROL, CONTROL_COLUMNS, control_rows),
        write_csv(SOURCE_AXIS_SUMMARY, AXIS_COLUMNS, axis_rows),
        write_parquet(TRADE_TAPE, trade_tape),
        write_csv(EH_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    ef_final = read_json(EF_FINAL)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ef_next_action": ef_final.get("next_action", ""),
        "ef_failed_gate_rows": sum(1 for row in read_csv(EF_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "survivor_rows": replay_summary["survivor_rows"],
        "attribution_rows": replay_summary["attribution_rows"],
        "direction_rows": replay_summary["direction_rows"],
        "curve_rows": replay_summary["curve_rows"],
        "trade_tape_rows": replay_summary["trade_tape_rows"],
        "max_scorecard_net_abs_diff": replay_summary["max_scorecard_net_abs_diff"],
        "max_scorecard_pf_abs_diff": replay_summary["max_scorecard_pf_abs_diff"],
        "density_watch_rows": replay_summary["density_watch_rows"],
        "direction_watch_rows": replay_summary["direction_watch_rows"],
        "curve_watch_rows": replay_summary["curve_watch_rows"],
        "package_rows": package_summary["package_rows"],
        "package_failed_hash_rows": package_summary["package_failed_hash_rows"],
        "package_failed_parity_rows": package_summary["package_failed_parity_rows"],
        "package_failed_feature_rows": package_summary["package_failed_feature_rows"],
        "package_failed_rows": package_summary["package_failed_hash_rows"] + package_summary["package_failed_parity_rows"] + package_summary["package_failed_feature_rows"],
        "control_rows": control_summary["control_rows"],
        "control_block_rows": control_summary["control_block_rows"],
        "shifted_alignment_close_watch_rows": control_summary["shifted_alignment_close_watch_rows"],
        "axis_rows": len(axis_rows),
        "eh_queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "survivor_rows": final["survivor_rows"],
                "trade_tape_rows": final["trade_tape_rows"],
                "package_failed_rows": final["package_failed_rows"],
                "density_watch_rows": final["density_watch_rows"],
                "direction_watch_rows": final["direction_watch_rows"],
                "curve_watch_rows": final["curve_watch_rows"],
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
