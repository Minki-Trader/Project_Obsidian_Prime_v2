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

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import review_validation_pocket_cost_shape_repair_inputs as di  # noqa: E402
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
STAGE_ID = di.STAGE_ID
RUN_NUMBER = "run337DJ"
RUN_ID = "run337DJ_materialize_pair_prediction_tape_and_surface_attribution_without_db_v1"
PARENT_RUN_ID = di.RUN_ID
NEXT_RUN_ID = "run337DK_review_pair_prediction_tape_surface_attribution_without_db_v1"
STATUS = "completed_stage337DJ_pair_prediction_tape_surface_attribution_materialized_no_training_no_selection"
JUDGMENT = "frozen_prediction_replay_materialized_surface_isolation_review_required"
DECISION = "stage337DJ_open_run337DK_review_pair_prediction_tape_surface_attribution"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DJ_pair_prediction_tape_surface_attribution_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = di.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = di.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DJ_pair_prediction_tape_surface_attribution.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DJ_pair_prediction_tape_surface_attribution.md"
SELECTED_STATUS = di.SELECTED_STATUS
STAGE_BRIEF = di.STAGE_BRIEF
WORKSPACE_STATE = di.WORKSPACE_STATE
CURRENT_STATE = di.CURRENT_STATE
CHANGELOG = di.CHANGELOG
RUN_REGISTRY = di.RUN_REGISTRY
ALPHA_LEDGER = di.ALPHA_LEDGER
ARTIFACT_REGISTRY = di.ARTIFACT_REGISTRY
STAGE_LEDGER = di.STAGE_LEDGER

DI_FINAL = di.FINAL_DECISION
DI_GATES = di.REQUIRED_GATE_AUDIT
DI_QUEUE = di.DJ_QUEUE
MODEL_INPUT = STAGE_DIR.parents[1] / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
CZ_FEATURE_SET = STAGE_DIR / "02_runs" / "run337CZ" / "feature_set_matrix.csv"
DE_MANIFEST = STAGE_DIR / "02_runs" / "run337DE" / "trained_model_manifest.csv"
DE_PAIR = STAGE_DIR / "02_runs" / "run337DE" / "two_stage_pair_scorecard.csv"
DH_FLOOR_FRAME = STAGE_DIR / "02_runs" / "run337DH" / "validation_pf_floor_input_frame.parquet"
DH_SLICE_FRAME = STAGE_DIR / "02_runs" / "run337DH" / "slice_stability_frame.csv"
DH_PAIR_SURFACE = STAGE_DIR / "02_runs" / "run337DH" / "pair_surface_smoothness_matrix.csv"
DH_ISOLATED_FLAGS = STAGE_DIR / "02_runs" / "run337DH" / "isolated_pocket_flags.csv"
DH_FORBIDDEN = STAGE_DIR / "02_runs" / "run337DH" / "forbidden_selection_audit.csv"
DH_QUARANTINE = STAGE_DIR / "02_runs" / "run337DH" / "oos_quarantine_audit.csv"

PAIR_TAPE = RUN_DIR / "pair_prediction_tape.parquet"
PAIR_SCORECARD = RUN_DIR / "prediction_tape_pair_scorecard.csv"
REPLAY_PARITY = RUN_DIR / "prediction_tape_replay_parity.csv"
SLICE_ATTRIBUTION = RUN_DIR / "prediction_slice_attribution.csv"
CURVE_POCKET_REVIEW = RUN_DIR / "curve_pocket_review.csv"
SURFACE_AUDIT = RUN_DIR / "surface_deconcentration_audit.csv"
RELEASE_BLOCKERS = RUN_DIR / "release_blocker_update.csv"
FIREWALL_AUDIT = RUN_DIR / "prediction_replay_firewall_audit.csv"
DK_QUEUE = RUN_DIR / "run337DK_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
TAPE_MANIFEST = RUN_DIR / "prediction_tape_manifest.json"

INPUT_FILES = (
    DI_FINAL,
    DI_GATES,
    DI_QUEUE,
    MODEL_INPUT,
    CZ_FEATURE_SET,
    DE_MANIFEST,
    DE_PAIR,
    DH_FLOOR_FRAME,
    DH_SLICE_FRAME,
    DH_PAIR_SURFACE,
    DH_ISOLATED_FLAGS,
    DH_FORBIDDEN,
    DH_QUARANTINE,
)
OUTPUT_FILES = (
    PAIR_TAPE,
    PAIR_SCORECARD,
    REPLAY_PARITY,
    SLICE_ATTRIBUTION,
    CURVE_POCKET_REVIEW,
    SURFACE_AUDIT,
    RELEASE_BLOCKERS,
    FIREWALL_AUDIT,
    DK_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    TAPE_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

SCORE_COLUMNS = (
    "pair_id",
    "stage1_model_id",
    "stage2_model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "split",
    "trade_count",
    "signal_density",
    "net_log_return_after_cost",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "pair_status",
    "blocks_runtime_probe",
    "claim_boundary",
)
PARITY_COLUMNS = (
    "pair_id",
    "split",
    "trade_count_diff",
    "net_abs_diff",
    "pf_abs_diff",
    "status",
    "effect",
    "claim_boundary",
)
SLICE_COLUMNS = (
    "pair_id",
    "split",
    "slice_axis",
    "slice_value",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "trade_count",
    "net_after_cost",
    "profit_factor",
    "expectancy",
    "win_rate",
    "concentration_share",
    "effect",
    "claim_boundary",
)
CURVE_COLUMNS = (
    "pair_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "validation_net",
    "validation_trades",
    "oos_pf",
    "oos_net",
    "oos_trades",
    "review_status",
    "effect",
    "claim_boundary",
)
SURFACE_COLUMNS = (
    "feature_set_id",
    "model_config_id",
    "validation_pf_extra0",
    "validation_pf_extra2",
    "validation_pf_extra5",
    "oos_pf_extra0",
    "oos_pf_extra2",
    "oos_pf_extra5",
    "validation_pf_max",
    "oos_pf_max",
    "oos_minus_validation_gap_max",
    "surface_status",
    "effect",
    "claim_boundary",
)
BLOCKER_COLUMNS = ("release_blocker", "rows", "effect", "claim_boundary")
FIREWALL_COLUMNS = ("audit_id", "observed", "expected", "status", "effect", "claim_boundary")
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "review_task",
    "required_inputs",
    "pass_condition",
    "fail_condition",
    "invalid_condition",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


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


def reverse_label_map(class_label_json: str) -> dict[str, int]:
    labels = json.loads(class_label_json)
    return {str(label): int(key) for key, label in labels.items()}


def int_label_map(class_label_json: str) -> dict[int, str]:
    labels = json.loads(class_label_json)
    return {int(key): str(label) for key, label in labels.items()}


def read_feature_sets() -> dict[str, list[str]]:
    rows = read_csv(CZ_FEATURE_SET)
    return {row["feature_set_id"]: [str(item) for item in json.loads(row["included_features_json"])] for row in rows}


def read_source() -> pd.DataFrame:
    source = pd.read_parquet(io_path(MODEL_INPUT)).copy()
    source["timestamp"] = pd.to_datetime(source["timestamp"], utc=True)
    source = source.sort_values("timestamp").reset_index(drop=True)
    source["source_row_id"] = np.arange(len(source), dtype=np.int64)
    return source


def ordered_probabilities(model: Any, matrix: np.ndarray, class_order: Sequence[int]) -> np.ndarray:
    raw = model.predict_proba(matrix)
    classes = list(getattr(model, "classes_", class_order))
    ordered = np.zeros((raw.shape[0], len(class_order)), dtype=np.float64)
    for output_index, class_value in enumerate(class_order):
        if class_value in classes:
            ordered[:, output_index] = raw[:, classes.index(class_value)]
    return ordered


def predict_manifest_model(row: Mapping[str, str], source: pd.DataFrame, feature_sets: Mapping[str, list[str]]) -> dict[str, Any]:
    features = feature_sets[row["feature_set_id"]]
    model = joblib.load(io_path(ROOT / row["model_path"]))
    matrix = source.loc[:, features].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float64)
    class_order = [int(item) for item in json.loads(row["class_order_json"])]
    probs = ordered_probabilities(model, matrix, class_order)
    pred = np.asarray(class_order, dtype=np.int64)[probs.argmax(axis=1)]
    label_to_int = reverse_label_map(row["class_label_json"])
    int_to_label = int_label_map(row["class_label_json"])
    return {
        "model_id": row["model_id"],
        "pred": pred,
        "probs": probs,
        "class_order": class_order,
        "label_to_int": label_to_int,
        "int_to_label": int_to_label,
    }


def max_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def stats_from_values(values: np.ndarray, trade_mask: np.ndarray) -> tuple[int, float, float, float, float, float, float]:
    trade_values = values[trade_mask]
    gross_profit = float(trade_values[trade_values > 0].sum()) if len(trade_values) else 0.0
    gross_loss = float(-trade_values[trade_values < 0].sum()) if len(trade_values) else 0.0
    pf = gross_profit / gross_loss if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)
    total = float(values.sum())
    expectancy = float(trade_values.mean()) if len(trade_values) else 0.0
    dd = max_drawdown(values)
    recovery = total / dd if dd > 0 else 0.0
    return int(trade_mask.sum()), float(trade_mask.mean()) if len(trade_mask) else 0.0, total, pf, expectancy, dd, recovery


def action_returns(action_label: np.ndarray, exact_returns: np.ndarray, cost_return: np.ndarray) -> np.ndarray:
    raw = np.where(action_label == "long", exact_returns, np.where(action_label == "short", -exact_returns, 0.0))
    trade_mask = np.isin(action_label, ["long", "short"])
    return raw - np.where(trade_mask, cost_return, 0.0)


def write_tape(frame: pd.DataFrame) -> Path:
    io_path(PAIR_TAPE.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(PAIR_TAPE), index=False)
    return PAIR_TAPE


def materialize_prediction_tape() -> tuple[pd.DataFrame, list[dict[str, Any]], list[dict[str, Any]]]:
    source = read_source()
    feature_sets = read_feature_sets()
    manifest_rows = read_csv(DE_MANIFEST)
    manifest = {row["model_id"]: row for row in manifest_rows}
    pairs = pd.DataFrame(read_csv(DE_PAIR)).drop_duplicates("pair_id").sort_values("pair_id")
    floor = pd.read_parquet(io_path(DH_FLOOR_FRAME)).sort_values(["cost_policy_id", "source_row_id"]).reset_index(drop=True)
    model_cache: dict[str, dict[str, Any]] = {}
    tape_frames: list[pd.DataFrame] = []
    score_rows: list[dict[str, Any]] = []
    for _, pair in pairs.iterrows():
        stage1_id = str(pair["stage1_model_id"])
        stage2_id = str(pair["stage2_model_id"])
        if stage1_id not in model_cache:
            model_cache[stage1_id] = predict_manifest_model(manifest[stage1_id], source, feature_sets)
        if stage2_id not in model_cache:
            model_cache[stage2_id] = predict_manifest_model(manifest[stage2_id], source, feature_sets)
        stage1 = model_cache[stage1_id]
        stage2 = model_cache[stage2_id]
        cost_policy = str(pair["cost_policy_id"])
        policy_frame = floor.loc[floor["cost_policy_id"].astype(str).eq(cost_policy)].sort_values("source_row_id").reset_index(drop=True)
        if len(policy_frame) != len(source):
            raise ValueError(f"Policy frame row mismatch for {cost_policy}: {len(policy_frame)} != {len(source)}")
        tradeable_int = stage1["label_to_int"].get("tradeable", 1)
        flat_int = stage2["label_to_int"].get("flat", 1)
        stage1_pred = stage1["pred"]
        stage2_pred = stage2["pred"]
        final_action_int = np.where(stage1_pred == tradeable_int, stage2_pred, flat_int)
        stage1_labels = np.asarray([stage1["int_to_label"].get(int(value), str(value)) for value in stage1_pred])
        final_labels = np.asarray([stage2["int_to_label"].get(int(value), str(value)) for value in final_action_int])
        cost_return = pd.to_numeric(policy_frame["round_trip_spread_return"], errors="coerce").fillna(0.0).to_numpy()
        cost_return += pd.to_numeric(policy_frame["extra_cost_return"], errors="coerce").fillna(0.0).to_numpy()
        exact = pd.to_numeric(policy_frame["exact_future_log_return_12"], errors="coerce").fillna(0.0).to_numpy()
        values = action_returns(final_labels, exact, cost_return)
        trade_mask = np.isin(final_labels, ["long", "short"])
        stage1_tradeable_col = stage1["class_order"].index(tradeable_int) if tradeable_int in stage1["class_order"] else 0
        stage2_scores = {label: np.zeros(len(source), dtype=np.float64) for label in ("short", "flat", "long")}
        for label, value in stage2["label_to_int"].items():
            if label in stage2_scores and value in stage2["class_order"]:
                stage2_scores[label] = stage2["probs"][:, stage2["class_order"].index(value)]
        tape = pd.DataFrame(
            {
                "pair_id": pair["pair_id"],
                "source_row_id": policy_frame["source_row_id"].to_numpy(),
                "timestamp": policy_frame["timestamp"].to_numpy(),
                "split": policy_frame["split"].astype(str).to_numpy(),
                "cost_policy_id": cost_policy,
                "feature_set_id": pair["feature_set_id"],
                "model_config_id": pair["model_config_id"],
                "stage1_model_id": stage1_id,
                "stage2_model_id": stage2_id,
                "stage1_pred": stage1_pred,
                "stage1_pred_label": stage1_labels,
                "stage1_tradeable_score": stage1["probs"][:, stage1_tradeable_col],
                "stage2_pred": stage2_pred,
                "final_action_int": final_action_int,
                "final_action_label": final_labels,
                "stage2_short_score": stage2_scores["short"],
                "stage2_flat_score": stage2_scores["flat"],
                "stage2_long_score": stage2_scores["long"],
                "exact_future_log_return_12": exact,
                "cost_return": cost_return,
                "action_net_after_cost": values,
                "is_trade": trade_mask,
                "session_bucket": policy_frame["session_bucket"].astype(str).to_numpy(),
                "hour_utc": policy_frame["hour_utc"].to_numpy(),
                "month": policy_frame["month"].astype(str).to_numpy(),
                "volatility_bucket": policy_frame["volatility_bucket"].astype(str).to_numpy(),
                "adx_bucket": policy_frame["adx_bucket"].astype(str).to_numpy(),
                "vix_regime": policy_frame["vix_regime"].astype(str).to_numpy(),
                "usd_regime": policy_frame["usd_regime"].astype(str).to_numpy(),
                "rate_regime": policy_frame["rate_regime"].astype(str).to_numpy(),
            }
        )
        tape_frames.append(tape)
        for split, split_frame in tape.groupby("split", sort=False):
            split_values = split_frame["action_net_after_cost"].to_numpy(dtype=np.float64)
            split_trade = split_frame["is_trade"].to_numpy(dtype=bool)
            trade_count, density, total, pf, expectancy, dd, recovery = stats_from_values(split_values, split_trade)
            status = "passed_pair_cost_shape" if trade_count >= 50 and total > 0 and pf >= 1.05 else "block_pair_cost_shape"
            score_rows.append(
                {
                    "pair_id": pair["pair_id"],
                    "stage1_model_id": stage1_id,
                    "stage2_model_id": stage2_id,
                    "cost_policy_id": cost_policy,
                    "feature_set_id": pair["feature_set_id"],
                    "model_config_id": pair["model_config_id"],
                    "split": split,
                    "trade_count": trade_count,
                    "signal_density": density,
                    "net_log_return_after_cost": total,
                    "profit_factor": pf,
                    "expectancy": expectancy,
                    "max_drawdown": dd,
                    "recovery_factor": recovery,
                    "pair_status": status,
                    "blocks_runtime_probe": str(status != "passed_pair_cost_shape").lower(),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    full_tape = pd.concat(tape_frames, ignore_index=True)
    replay_rows = build_replay_parity(score_rows)
    return full_tape, score_rows, replay_rows


def build_replay_parity(score_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    de_rows = {(row["pair_id"], row["split"]): row for row in read_csv(DE_PAIR)}
    rows: list[dict[str, Any]] = []
    for row in score_rows:
        key = (row["pair_id"], row["split"])
        original = de_rows.get(key, {})
        trade_diff = int(row["trade_count"]) - as_int(original.get("trade_count"))
        net_diff = abs(as_float(row["net_log_return_after_cost"]) - as_float(original.get("net_log_return_after_cost")))
        pf_diff = abs(as_float(row["profit_factor"]) - as_float(original.get("profit_factor")))
        status = "passed_replay_parity" if trade_diff == 0 and net_diff <= 1e-9 and pf_diff <= 1e-9 else "review_replay_drift"
        rows.append(
            {
                "pair_id": row["pair_id"],
                "split": row["split"],
                "trade_count_diff": trade_diff,
                "net_abs_diff": net_diff,
                "pf_abs_diff": pf_diff,
                "status": status,
                "effect": "checks frozen replay matches DE pair scorecard(고정 리플레이가 DE 쌍 점수표와 맞는지 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_slice_attribution(tape: pd.DataFrame) -> list[dict[str, Any]]:
    axes = ["session_bucket", "hour_utc", "month", "volatility_bucket", "adx_bucket", "vix_regime", "usd_regime", "rate_regime"]
    rows: list[dict[str, Any]] = []
    totals = {
        (pair_id, split): int(group["is_trade"].astype(bool).sum())
        for (pair_id, split), group in tape.groupby(["pair_id", "split"], sort=False)
    }
    for axis in axes:
        for key, group in tape.groupby(["pair_id", "split", axis], sort=False):
            pair_id, split, value = key
            trades = group[group["is_trade"].astype(bool)]
            values = trades["action_net_after_cost"].to_numpy(dtype=np.float64)
            trade_count = len(trades)
            total = float(values.sum()) if trade_count else 0.0
            pf = stats_from_values(values, np.ones(trade_count, dtype=bool))[3] if trade_count else 0.0
            wins = int((values > 0).sum()) if trade_count else 0
            first = group.iloc[0]
            rows.append(
                {
                    "pair_id": pair_id,
                    "split": split,
                    "slice_axis": axis,
                    "slice_value": str(value),
                    "cost_policy_id": first["cost_policy_id"],
                    "feature_set_id": first["feature_set_id"],
                    "model_config_id": first["model_config_id"],
                    "trade_count": trade_count,
                    "net_after_cost": total,
                    "profit_factor": pf,
                    "expectancy": total / trade_count if trade_count else 0.0,
                    "win_rate": wins / trade_count if trade_count else 0.0,
                    "concentration_share": trade_count / totals.get((pair_id, split), 1) if totals.get((pair_id, split), 0) else 0.0,
                    "effect": "non-oracle slice attribution from frozen predictions(고정 예측의 비오라클 슬라이스 귀속)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_curve_review(score_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_pair: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in score_rows:
        by_pair.setdefault(str(row["pair_id"]), {})[str(row["split"])] = row
    rows: list[dict[str, Any]] = []
    for pair_id, splits in sorted(by_pair.items()):
        validation = splits.get("validation", {})
        oos = splits.get("oos", {})
        val_pf = as_float(validation.get("profit_factor"))
        oos_pf = as_float(oos.get("profit_factor"))
        val_net = as_float(validation.get("net_log_return_after_cost"))
        oos_net = as_float(oos.get("net_log_return_after_cost"))
        if val_pf >= 1.05 and val_net > 0:
            status = "validation_floor_pass_review_required"
        elif oos_pf >= 1.10 and val_pf < 1.05:
            status = "oos_positive_validation_thin_block"
        else:
            status = "blocked_pair_cost_shape"
        first = validation or oos
        rows.append(
            {
                "pair_id": pair_id,
                "cost_policy_id": first.get("cost_policy_id", ""),
                "feature_set_id": first.get("feature_set_id", ""),
                "model_config_id": first.get("model_config_id", ""),
                "validation_pf": val_pf,
                "validation_net": val_net,
                "validation_trades": as_int(validation.get("trade_count")),
                "oos_pf": oos_pf,
                "oos_net": oos_net,
                "oos_trades": as_int(oos.get("trade_count")),
                "review_status": status,
                "effect": "separates validation survival from OOS pocket(검증 생존과 OOS 포켓 분리)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def cost_order(policy: str) -> int:
    if "extra0" in policy:
        return 0
    if "extra2" in policy:
        return 2
    if "extra5" in policy:
        return 5
    return 999


def build_surface_audit(curve_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    frame = pd.DataFrame(curve_rows)
    rows: list[dict[str, Any]] = []
    for (feature_set, model_config), group in frame.groupby(["feature_set_id", "model_config_id"], dropna=False):
        by_cost = {cost_order(str(row["cost_policy_id"])): row for _, row in group.iterrows()}
        val_pfs = [as_float(row.get("validation_pf")) for row in by_cost.values()]
        oos_pfs = [as_float(row.get("oos_pf")) for row in by_cost.values()]
        val_max = max(val_pfs) if val_pfs else 0.0
        oos_max = max(oos_pfs) if oos_pfs else 0.0
        gap_max = max((as_float(row.get("oos_pf")) - as_float(row.get("validation_pf")) for row in by_cost.values()), default=0.0)
        status = "isolated_oos_surface_watch" if oos_max >= 1.10 and val_max < 1.05 else "surface_no_release"
        rows.append(
            {
                "feature_set_id": feature_set,
                "model_config_id": model_config,
                "validation_pf_extra0": as_float(by_cost.get(0, {}).get("validation_pf", 0.0)) if 0 in by_cost else 0.0,
                "validation_pf_extra2": as_float(by_cost.get(2, {}).get("validation_pf", 0.0)) if 2 in by_cost else 0.0,
                "validation_pf_extra5": as_float(by_cost.get(5, {}).get("validation_pf", 0.0)) if 5 in by_cost else 0.0,
                "oos_pf_extra0": as_float(by_cost.get(0, {}).get("oos_pf", 0.0)) if 0 in by_cost else 0.0,
                "oos_pf_extra2": as_float(by_cost.get(2, {}).get("oos_pf", 0.0)) if 2 in by_cost else 0.0,
                "oos_pf_extra5": as_float(by_cost.get(5, {}).get("oos_pf", 0.0)) if 5 in by_cost else 0.0,
                "validation_pf_max": val_max,
                "oos_pf_max": oos_max,
                "oos_minus_validation_gap_max": gap_max,
                "surface_status": status,
                "effect": "checks replay surface concentration(리플레이 표면 집중 점검)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_blockers(curve_rows: Sequence[Mapping[str, Any]], surface_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    validation_blocks = sum(1 for row in curve_rows if as_float(row.get("validation_pf")) < 1.05)
    oos_thin = sum(1 for row in curve_rows if row.get("review_status") == "oos_positive_validation_thin_block")
    surface_watch = sum(1 for row in surface_rows if row.get("surface_status") == "isolated_oos_surface_watch")
    return [
        {
            "release_blocker": "validation_prediction_pf_below_1p05",
            "rows": validation_blocks,
            "effect": "keeps runtime release blocked until prediction validation improves(예측 검증 개선 전 런타임 해제 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "release_blocker": "oos_positive_validation_thin_prediction_watch",
            "rows": oos_thin,
            "effect": "keeps attractive OOS pocket quarantined(매력적인 OOS 포켓 격리 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "release_blocker": "surface_isolation_watch",
            "rows": surface_watch,
            "effect": "keeps surface-mined pockets from selection(표면 채굴 포켓 선택 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "release_blocker": "auto_release_blocked",
            "rows": len(curve_rows),
            "effect": "DJ is materialization only(DJ는 물질화 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_firewall() -> list[dict[str, str]]:
    checks = [
        ("no_new_training", "not_run", "not_run"),
        ("no_threshold_tuning", "not_run", "not_run"),
        ("no_candidate_selection", "not_run", "not_run"),
        ("no_mt5_probe", "not_run", "not_run"),
        ("no_forward_goal_claim", "not_claimed", "not_claimed"),
    ]
    return [
        {
            "audit_id": audit_id,
            "observed": observed,
            "expected": expected,
            "status": "passed" if observed == expected else "failed",
            "effect": "keeps prediction replay inside research boundary(예측 리플레이를 연구 경계 안에 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for audit_id, observed, expected in checks
    ]


def build_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DK_review_replay_parity",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "review_task": "review prediction tape parity against DE scorecard(DE 점수표 대비 예측 테이프 동등성 검토)",
            "required_inputs": f"{rel(REPLAY_PARITY)};{rel(PAIR_SCORECARD)}",
            "pass_condition": "all pair/split rows match DE replay(모든 쌍/분할 행이 DE 리플레이와 일치)",
            "fail_condition": "any replay drift changes pair status(리플레이 차이가 쌍 상태를 바꿈)",
            "invalid_condition": "model artifact hash mismatch(모델 산출물 해시 불일치)",
            "effect": "checks replay identity before interpretation(해석 전 리플레이 정체성 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DK_review_prediction_slices",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "review_task": "review non-oracle slice attribution(비오라클 슬라이스 귀속 검토)",
            "required_inputs": rel(SLICE_ATTRIBUTION),
            "pass_condition": "OOS pocket is not concentrated in thin slices(OOS 포켓이 얇은 슬라이스에 집중되지 않음)",
            "fail_condition": "validation weakness remains broad or OOS pocket concentrated(검증 약점이 넓거나 OOS 포켓이 집중)",
            "invalid_condition": "slice attribution uses label oracle(슬라이스 귀속이 라벨 오라클 사용)",
            "effect": "tests actual prediction pocket anatomy(실제 예측 포켓 해부)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DK_review_release_blockers",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "review_task": "review release blocker update(해제 차단 갱신 검토)",
            "required_inputs": f"{rel(CURVE_POCKET_REVIEW)};{rel(RELEASE_BLOCKERS)};{rel(SURFACE_AUDIT)}",
            "pass_condition": "blockers are explained without selection(차단 요소가 선택 없이 설명됨)",
            "fail_condition": "release would rely on OOS-positive validation-thin pocket(해제가 OOS 양호/검증 얇음 포켓에 의존)",
            "invalid_condition": "candidate selected in materialization(물질화에서 후보 선택)",
            "effect": "decides whether to design another repair or review training eligibility(다음 수리 설계 또는 학습 적격 검토 결정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required inputs exist(필수 입력 존재)"),
        ("parent_di_gates_passed", final["di_failed_gate_rows"] == 0, str(final["di_failed_gate_rows"]), "0", "DI review usable(DI 검토 사용 가능)"),
        ("parent_next_action_matches", final["di_next_action"] == RUN_ID, str(final["di_next_action"]), RUN_ID, "continues DI queue(DI 대기열을 이어감)"),
        ("prediction_tape_rows", final["prediction_tape_rows"] == final["expected_tape_rows"], str(final["prediction_tape_rows"]), str(final["expected_tape_rows"]), "row-level tape complete(행 단위 테이프 완성)"),
        ("pair_count", final["pair_count"] == 18, str(final["pair_count"]), "18", "all DE pairs replayed(모든 DE 쌍 리플레이)"),
        ("replay_parity_passed", final["replay_parity_failed_rows"] == 0, str(final["replay_parity_failed_rows"]), "0", "replay matches DE scorecard(리플레이가 DE 점수표와 일치)"),
        ("release_rows_zero", final["release_candidate_rows"] == 0, str(final["release_candidate_rows"]), "0", "no auto release(자동 해제 없음)"),
        ("blockers_named", final["release_blocker_rows"] >= 4, str(final["release_blocker_rows"]), ">=4", "release blockers named(해제 차단 요소 명명)"),
        ("dk_queue_materialized", final["queue_rows"] >= 3, str(final["queue_rows"]), ">=3", "DK review queue exists(DK 검토 대기열 존재)"),
        (
            "no_forbidden_execution",
            final["model_training"] == "not_run"
            and final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"training={final['model_training']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary preserved(주장 경계 보존)",
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


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "closed M5 UTC inherited from model input and DH floor frame(모델 입력과 DH 하한 프레임의 닫힌 M5 UTC 상속)",
        "sample_scope": f"prediction_tape_rows={final['prediction_tape_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};replay_parity_failed={final['replay_parity_failed_rows']}",
        "feature_label_boundary": "features current-bar only; realized returns used only for replay scoring(피처는 현재 봉 전용, 실현 수익은 리플레이 채점에만 사용)",
        "split_boundary": "inherited train/validation/OOS(상속 학습/검증/OOS)",
        "leakage_risk": "using replay result to tune threshold(리플레이 결과로 임계값 튜닝)",
        "data_hash_or_identity": {"pair_tape": sha256_file(PAIR_TAPE), "de_pair": sha256_file(DE_PAIR)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "frozen DE joblib models(고정 DE joblib 모델)",
        "target_and_label": "stage1 cost gate plus stage2 final action replay(1단계 비용 게이트 + 2단계 최종 행동 리플레이)",
        "split_method": "inherited chronological train/validation/OOS(상속 시간순 학습/검증/OOS)",
        "selection_metric": "none; replay only(없음, 리플레이 전용)",
        "secondary_metrics": "pair scorecard, slice attribution, surface blockers(쌍 점수표/슬라이스 귀속/표면 차단)",
        "threshold_policy": "unchanged model argmax; no tuning(변경 없는 모델 argmax, 튜닝 없음)",
        "overfit_risk": "choosing OOS-positive validation-thin replay pocket(OOS 양호/검증 얇음 리플레이 포켓 선택)",
        "calibration_risk": "probabilities are model scores, not calibrated trading probabilities(확률은 모델 점수이며 보정된 거래 확률 아님)",
        "comparison_baseline": rel(DE_PAIR),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"release_candidate_rows={final['release_candidate_rows']};oos_positive_validation_thin_rows={final['oos_positive_validation_thin_rows']}",
        "comparison_baseline": rel(DE_PAIR),
        "likely_drivers": "frozen model prediction surface, cost policy, feature context(고정 모델 예측 표면/비용 정책/피처 문맥)",
        "segment_checks": f"slice_rows={final['slice_rows']};surface_watch_rows={final['surface_watch_rows']}",
        "trade_shape": f"prediction_trade_rows={final['prediction_trade_rows']}",
        "alternative_explanations": "regime concentration and model-family surface mining(국면 집중과 모델 계열 표면 채굴)",
        "attribution_confidence": "high_for_replay_identity_medium_for_surface_block(리플레이 정체성은 높음, 표면 차단은 중간)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "prediction tape, replay parity, slice attribution, blockers(예측 테이프/리플레이 동등성/슬라이스 귀속/차단 요소)",
        "evidence_missing": "DK review and any later repair/training decision(DK 검토 및 이후 수리/학습 결정)",
        "judgment_label": "materialized_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "라벨이 아니라 고정 모델 예측으로 다시 재생했고, 아직 해제 후보는 없습니다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_prediction_outputs_with_tracked_report(무시된 예측 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DJ Pair Prediction Tape Surface Attribution(쌍 예측 테이프 표면 귀속)

## Conclusion(결론)

run337DJ(337DJ 실행)는 frozen DE models(고정 DE 모델)로 row-level prediction tape(행 단위 예측 테이프)를 물질화했다. 이 작업은 training(학습)이 아니라 replay(리플레이)다.

Replay parity(리플레이 동등성)는 failed rows(실패 행) `{final["replay_parity_failed_rows"]}`로 DE pair scorecard(DE 쌍 점수표)와 일치한다. 다만 release candidate(해제 후보)는 `{final["release_candidate_rows"]}`개이며, OOS-positive/validation-thin(표본외 양호/검증 얇음) 행은 `{final["oos_positive_validation_thin_rows"]}`개다.

Effect(효과): label oracle(라벨 오라클)을 제거하고 실제 고정 예측 기준으로 표면과 슬라이스를 볼 수 있게 됐다. 그러나 MT5 probe(MT5 탐침), candidate selection(후보 선택), Forward/Goal(전진/목표)은 계속 차단한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- prediction_tape_rows(예측 테이프 행): `{final["prediction_tape_rows"]}`
- pair_count(쌍 수): `{final["pair_count"]}`
- replay_parity_failed_rows(리플레이 동등성 실패 행): `{final["replay_parity_failed_rows"]}`
- release_candidate_rows(해제 후보 행): `{final["release_candidate_rows"]}`
- oos_positive_validation_thin_rows(OOS 양호/검증 얇음 행): `{final["oos_positive_validation_thin_rows"]}`
- surface_watch_rows(표면 감시 행): `{final["surface_watch_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DJ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 고정 모델 예측 테이프와 표면 귀속을 물질화했고, 다음은 DK 검토다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(REPLAY_PARITY)}`
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
        f"  Stage337 run337DJ focus complete: frozen pair prediction tape/surface attribution(고정 쌍 예측 테이프/표면 귀속)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337DK(337DK 실행)에서 replay parity/slice/surface blockers(리플레이 동등성/슬라이스/표면 차단)를 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DJ focus complete")
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
## Stage337 run337DJ(337DJ 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 고정 모델 예측 테이프를 만들었고 replay parity(리플레이 동등성)는 통과했지만 release(해제)는 없다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DI(337DI"
    if "## Stage337 run337DJ(337DJ 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_dj_prediction_replay_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 pair prediction tape surface attribution review(쌍 예측 테이프 표면 귀속 검토)다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DJ(337DJ 실행) materialized frozen pair prediction tape and surface attribution(고정 쌍 예측 테이프와 표면 귀속). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DJ(337DJ 실행) materialized frozen pair prediction"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DJ materialized frozen pair prediction tape and surface attribution(고정 쌍 예측 테이프와 표면 귀속) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DJ materialized frozen pair prediction"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "pair_prediction_tape_surface_attribution_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"tape_rows={final['prediction_tape_rows']};release_rows={final['release_candidate_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__prediction_tape",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "prediction_tape",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "prediction_replay_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "frozen_prediction_pair_slice_surface",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"release_rows={final['release_candidate_rows']};oos_thin={final['oos_positive_validation_thin_rows']}",
        "guardrail_kpi": "replay_parity;no_training;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__prediction_tape",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "frozen DE prediction tape materialized",
        "kpi_scope": "pair_replay_slice_surface_blockers",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__prediction_tape",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "do frozen prediction rows reproduce DE pair scorecard and explain surface isolation",
        "metric_scope": "replay_parity_prediction_slices_release_blockers",
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
    di_final = read_json(DI_FINAL)
    di_gates = read_csv(DI_GATES)
    tape, score_rows, parity_rows = materialize_prediction_tape()
    tape_path = write_tape(tape)
    slice_rows = build_slice_attribution(tape)
    curve_rows = build_curve_review(score_rows)
    surface_rows = build_surface_audit(curve_rows)
    blocker_rows = build_blockers(curve_rows, surface_rows)
    firewall_rows = build_firewall()
    queue_rows = build_queue()
    release_rows = sum(1 for row in curve_rows if row["review_status"] == "validation_floor_pass_review_required")
    oos_thin = sum(1 for row in curve_rows if row["review_status"] == "oos_positive_validation_thin_block")
    artifacts: list[Path] = [
        tape_path,
        write_csv(PAIR_SCORECARD, SCORE_COLUMNS, score_rows),
        write_csv(REPLAY_PARITY, PARITY_COLUMNS, parity_rows),
        write_csv(SLICE_ATTRIBUTION, SLICE_COLUMNS, slice_rows),
        write_csv(CURVE_POCKET_REVIEW, CURVE_COLUMNS, curve_rows),
        write_csv(SURFACE_AUDIT, SURFACE_COLUMNS, surface_rows),
        write_csv(RELEASE_BLOCKERS, BLOCKER_COLUMNS, blocker_rows),
        write_csv(FIREWALL_AUDIT, FIREWALL_COLUMNS, firewall_rows),
        write_csv(DK_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "di_next_action": di_final.get("next_action", ""),
        "di_failed_gate_rows": sum(1 for row in di_gates if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "prediction_tape_rows": int(len(tape)),
        "expected_tape_rows": int(tape["pair_id"].nunique() * tape["source_row_id"].nunique()),
        "pair_count": int(tape["pair_id"].nunique()),
        "source_rows": int(tape["source_row_id"].nunique()),
        "prediction_trade_rows": int(tape["is_trade"].astype(bool).sum()),
        "score_rows": len(score_rows),
        "slice_rows": len(slice_rows),
        "curve_review_rows": len(curve_rows),
        "replay_parity_failed_rows": sum(1 for row in parity_rows if row["status"] != "passed_replay_parity"),
        "max_replay_net_abs_diff": max((as_float(row["net_abs_diff"]) for row in parity_rows), default=0.0),
        "max_replay_pf_abs_diff": max((as_float(row["pf_abs_diff"]) for row in parity_rows), default=0.0),
        "release_candidate_rows": release_rows,
        "oos_positive_validation_thin_rows": oos_thin,
        "surface_watch_rows": sum(1 for row in surface_rows if row["surface_status"] == "isolated_oos_surface_watch"),
        "release_blocker_rows": len(blocker_rows),
        "firewall_failed_rows": sum(1 for row in firewall_rows if row["status"] != "passed"),
        "queue_rows": len(queue_rows),
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
            write_json(
                TAPE_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "pair_prediction_tape": rel(PAIR_TAPE),
                    "prediction_tape_rows": final["prediction_tape_rows"],
                    "pair_count": final["pair_count"],
                    "source_rows": final["source_rows"],
                    "model_manifest": rel(DE_MANIFEST),
                    "de_pair_scorecard": rel(DE_PAIR),
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
