from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import design_validation_pocket_cost_shape_repair as dg  # noqa: E402
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
STAGE_ID = dg.STAGE_ID
RUN_NUMBER = "run337DH"
RUN_ID = "run337DH_materialize_validation_pocket_cost_shape_repair_inputs_without_db_v1"
PARENT_RUN_ID = dg.RUN_ID
NEXT_RUN_ID = "run337DI_review_validation_pocket_cost_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337DH_validation_pocket_cost_shape_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "repair_inputs_materialized_for_validation_floor_slice_oos_quarantine_review"
DECISION = "stage337DH_open_run337DI_review_validation_pocket_cost_shape_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DH_validation_pocket_cost_shape_repair_inputs_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dg.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DH_validation_pocket_cost_shape_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DH_validation_pocket_cost_shape_repair_inputs.md"
SELECTED_STATUS = dg.SELECTED_STATUS
STAGE_BRIEF = dg.STAGE_BRIEF
WORKSPACE_STATE = dg.WORKSPACE_STATE
CURRENT_STATE = dg.CURRENT_STATE
CHANGELOG = dg.CHANGELOG
RUN_REGISTRY = dg.RUN_REGISTRY
ALPHA_LEDGER = dg.ALPHA_LEDGER
ARTIFACT_REGISTRY = dg.ARTIFACT_REGISTRY
STAGE_LEDGER = dg.STAGE_LEDGER

MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
DG_FINAL = dg.FINAL_DECISION
DG_GATES = dg.REQUIRED_GATE_AUDIT
DG_FAILURE_MEMORY = dg.FAILURE_MEMORY
DG_REPAIR_CONTRACT = dg.REPAIR_CONTRACT
DG_SLICE_CONTRACT = dg.SLICE_CONTRACT
DG_PAIR_SMOOTHNESS = dg.PAIR_SMOOTHNESS
DG_FIREWALL = dg.FIREWALL
DG_DH_QUEUE = dg.DH_QUEUE
DF_PAIR_SUMMARY = dg.DF_PAIR_SUMMARY
DF_DIVERGENCE = dg.DF_DIVERGENCE
DE_PAIR = dg.DE_PAIR
DD_STAGE1 = dg.DD_STAGE1
DD_STAGE2 = dg.DD_STAGE2
DD_POINT = dg.DD_POINT
DD_MANIFEST = dg.DD_MANIFEST

FLOOR_FRAME = RUN_DIR / "validation_pf_floor_input_frame.parquet"
FLOOR_AUDIT = RUN_DIR / "validation_pf_floor_audit.csv"
SLICE_FRAME = RUN_DIR / "slice_stability_frame.csv"
SLICE_POCKET_AUDIT = RUN_DIR / "slice_pocket_audit.csv"
OOS_QUARANTINE = RUN_DIR / "oos_quarantine_audit.csv"
FORBIDDEN_SELECTION = RUN_DIR / "forbidden_selection_audit.csv"
PAIR_SURFACE = RUN_DIR / "pair_surface_smoothness_matrix.csv"
ISOLATED_FLAGS = RUN_DIR / "isolated_pocket_flags.csv"
DI_QUEUE = RUN_DIR / "run337DI_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DG_FINAL,
    DG_GATES,
    DG_FAILURE_MEMORY,
    DG_REPAIR_CONTRACT,
    DG_SLICE_CONTRACT,
    DG_PAIR_SMOOTHNESS,
    DG_FIREWALL,
    DG_DH_QUEUE,
    DF_PAIR_SUMMARY,
    DF_DIVERGENCE,
    DE_PAIR,
    DD_STAGE1,
    DD_STAGE2,
    DD_POINT,
    DD_MANIFEST,
    MODEL_INPUT,
)
OUTPUT_FILES = (
    FLOOR_FRAME,
    FLOOR_AUDIT,
    SLICE_FRAME,
    SLICE_POCKET_AUDIT,
    OOS_QUARANTINE,
    FORBIDDEN_SELECTION,
    PAIR_SURFACE,
    ISOLATED_FLAGS,
    DI_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
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

FLOOR_AUDIT_COLUMNS = (
    "split",
    "cost_policy_id",
    "rows",
    "stage1_pass_rows",
    "stage1_pass_rate",
    "trade_count",
    "long_count",
    "short_count",
    "flat_count",
    "net_after_cost",
    "profit_factor",
    "expectancy",
    "avg_edge_after_cost_identity",
    "median_stage1_score",
    "floor_status",
    "effect",
    "claim_boundary",
)
SLICE_COLUMNS = (
    "slice_axis",
    "slice_value",
    "split",
    "cost_policy_id",
    "rows",
    "trade_count",
    "net_after_cost",
    "profit_factor",
    "expectancy",
    "win_rate",
    "concentration_share",
    "effect",
    "claim_boundary",
)
SLICE_AUDIT_COLUMNS = (
    "slice_axis",
    "slice_value",
    "cost_policy_id",
    "validation_trades",
    "validation_net",
    "validation_pf",
    "oos_trades",
    "oos_net",
    "oos_pf",
    "pocket_status",
    "effect",
    "claim_boundary",
)
QUARANTINE_COLUMNS = (
    "pair_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "oos_pf",
    "pf_gap_oos_minus_validation",
    "quarantine_status",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
FORBIDDEN_COLUMNS = (
    "audit_id",
    "blocked_action",
    "observed",
    "expected",
    "status",
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
FLAG_COLUMNS = (
    "flag_id",
    "pair_id",
    "flag_type",
    "validation_pf",
    "oos_pf",
    "pf_gap_oos_minus_validation",
    "effect",
    "claim_boundary",
)
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


def safe_ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def profit_factor(values: pd.Series) -> float:
    positives = float(values[values > 0].sum())
    negatives = float(-values[values < 0].sum())
    if negatives == 0:
        return 999.0 if positives > 0 else 0.0
    return positives / negatives


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def read_parquet(path: Path, columns: Sequence[str] | None = None) -> pd.DataFrame:
    return pd.read_parquet(io_path(path), columns=list(columns) if columns else None)


def bucket_zscore(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    return pd.Series(
        np.select(
            [values <= -1.0, values >= 1.0],
            ["low_z", "high_z"],
            default="mid_z",
        ),
        index=series.index,
    )


def build_floor_frame() -> pd.DataFrame:
    stage1 = read_parquet(DD_STAGE1)
    stage2_cols = [
        "source_row_id",
        "timestamp",
        "split",
        "cost_policy_id",
        "stage1_score",
        "stage2_payoff_score",
        "stage2_rank_bucket",
        "stage2_rank_label",
        "stage2_direction_hint",
        "final_action_label",
        "skip_reason",
    ]
    stage2 = read_parquet(DD_STAGE2, stage2_cols)
    feature_cols = [
        "timestamp",
        "atr_14",
        "historical_vol_20",
        "adx_14",
        "is_us_cash_open",
        "minutes_from_cash_open",
        "vix_zscore_20",
        "usdx_zscore_20",
        "us10yr_zscore_20",
    ]
    features = read_parquet(MODEL_INPUT, feature_cols)
    for frame in (stage1, stage2, features):
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    merged = stage1.merge(
        stage2,
        on=["source_row_id", "timestamp", "split", "cost_policy_id"],
        how="inner",
        suffixes=("", "_stage2"),
    )
    merged = merged.merge(features, on="timestamp", how="left")
    timestamp = pd.to_datetime(merged["timestamp"], utc=True)
    merged["hour_utc"] = timestamp.dt.hour
    merged["month"] = timestamp.dt.strftime("%Y-%m")
    cash_open = merged["is_us_cash_open"].astype(str).str.lower().isin(["true", "1", "1.0"])
    minutes = pd.to_numeric(merged["minutes_from_cash_open"], errors="coerce").fillna(-9999)
    merged["session_bucket"] = np.select(
        [
            cash_open & (minutes < 60),
            cash_open & (minutes >= 60) & (minutes <= 300),
            cash_open & (minutes > 300),
        ],
        ["cash_open_first_hour", "cash_open_midday", "cash_open_late"],
        default="outside_us_cash",
    )
    hist_vol = pd.to_numeric(merged["historical_vol_20"], errors="coerce")
    train_vol = hist_vol[merged["split"].astype(str) == "train"].dropna()
    q33 = float(train_vol.quantile(0.33)) if not train_vol.empty else float(hist_vol.quantile(0.33))
    q66 = float(train_vol.quantile(0.66)) if not train_vol.empty else float(hist_vol.quantile(0.66))
    merged["volatility_bucket"] = np.select(
        [hist_vol <= q33, hist_vol >= q66],
        ["low_vol", "high_vol"],
        default="mid_vol",
    )
    adx = pd.to_numeric(merged["adx_14"], errors="coerce")
    merged["adx_bucket"] = np.select([adx < 20.0, adx >= 25.0], ["low_adx", "strong_adx"], default="mid_adx")
    merged["vix_regime"] = bucket_zscore(merged["vix_zscore_20"])
    merged["usd_regime"] = bucket_zscore(merged["usdx_zscore_20"])
    merged["rate_regime"] = bucket_zscore(merged["us10yr_zscore_20"])
    costs = pd.to_numeric(merged["round_trip_spread_return"], errors="coerce").fillna(0) + pd.to_numeric(
        merged["extra_cost_return"], errors="coerce"
    ).fillna(0)
    future = pd.to_numeric(merged["exact_future_log_return_12"], errors="coerce").fillna(0)
    action = merged["final_action_label"].astype(str)
    merged["is_trade"] = action.isin(["long", "short"]) & merged["stage1_pass"].astype(bool)
    merged["action_net_after_cost"] = np.select(
        [action.eq("long") & merged["is_trade"], action.eq("short") & merged["is_trade"]],
        [future - costs, -future - costs],
        default=0.0,
    )
    merged["floor_candidate_status"] = np.select(
        [
            merged["split"].eq("train") & merged["stage1_pass"].astype(bool),
            merged["split"].eq("validation") & merged["stage1_pass"].astype(bool),
            merged["split"].eq("oos") & merged["stage1_pass"].astype(bool),
        ],
        ["train_floor_anchor", "validation_readonly_candidate", "oos_quarantine_candidate"],
        default="not_tradeable",
    )
    keep_cols = [
        "source_row_id",
        "timestamp",
        "future_timestamp",
        "split",
        "cost_policy_id",
        "stage1_pass",
        "stage1_label",
        "stage1_score",
        "stage2_payoff_score",
        "stage2_rank_bucket",
        "stage2_rank_label",
        "stage2_direction_hint",
        "final_action_label",
        "skip_reason",
        "current_close",
        "exact_future_log_return_12",
        "round_trip_spread_return",
        "extra_cost_return",
        "train_only_noise_buffer",
        "edge_after_cost_identity",
        "action_net_after_cost",
        "is_trade",
        "hour_utc",
        "month",
        "session_bucket",
        "volatility_bucket",
        "adx_bucket",
        "vix_regime",
        "usd_regime",
        "rate_regime",
        "floor_candidate_status",
    ]
    return merged[keep_cols]


def write_floor_frame(frame: pd.DataFrame) -> Path:
    io_path(FLOOR_FRAME.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(FLOOR_FRAME), index=False)
    return FLOOR_FRAME


def summarize_floor(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (split, cost_policy), group in frame.groupby(["split", "cost_policy_id"], dropna=False):
        trades = group[group["is_trade"].astype(bool)]
        net = float(trades["action_net_after_cost"].sum()) if not trades.empty else 0.0
        pf = profit_factor(trades["action_net_after_cost"]) if not trades.empty else 0.0
        rows.append(
            {
                "split": split,
                "cost_policy_id": cost_policy,
                "rows": len(group),
                "stage1_pass_rows": int(group["stage1_pass"].astype(bool).sum()),
                "stage1_pass_rate": safe_ratio(float(group["stage1_pass"].astype(bool).sum()), float(len(group))),
                "trade_count": len(trades),
                "long_count": int((trades["final_action_label"] == "long").sum()),
                "short_count": int((trades["final_action_label"] == "short").sum()),
                "flat_count": int((~group["final_action_label"].isin(["long", "short"])).sum()),
                "net_after_cost": net,
                "profit_factor": pf,
                "expectancy": safe_ratio(net, float(len(trades))),
                "avg_edge_after_cost_identity": float(pd.to_numeric(group["edge_after_cost_identity"], errors="coerce").mean()),
                "median_stage1_score": float(pd.to_numeric(group["stage1_score"], errors="coerce").median()),
                "floor_status": f"{split}_read_only" if split != "train" else "train_anchor",
                "effect": "summarizes floor input without selecting thresholds(임계값 선택 없이 하한 입력 요약)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summarize_group(axis: str, value: Any, split: Any, cost_policy: Any, group: pd.DataFrame, total_trades: int) -> dict[str, Any]:
    trades = group[group["is_trade"].astype(bool)]
    net = float(trades["action_net_after_cost"].sum()) if not trades.empty else 0.0
    pf = profit_factor(trades["action_net_after_cost"]) if not trades.empty else 0.0
    wins = int((trades["action_net_after_cost"] > 0).sum()) if not trades.empty else 0
    return {
        "slice_axis": axis,
        "slice_value": str(value),
        "split": split,
        "cost_policy_id": cost_policy,
        "rows": len(group),
        "trade_count": len(trades),
        "net_after_cost": net,
        "profit_factor": pf,
        "expectancy": safe_ratio(net, float(len(trades))),
        "win_rate": safe_ratio(float(wins), float(len(trades))),
        "concentration_share": safe_ratio(float(len(trades)), float(total_trades)),
        "effect": "materializes slice-level pocket evidence(슬라이스 단위 포켓 근거 물질화)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_slice_frame(frame: pd.DataFrame) -> list[dict[str, Any]]:
    axes = [
        "session_bucket",
        "hour_utc",
        "month",
        "volatility_bucket",
        "adx_bucket",
        "vix_regime",
        "usd_regime",
        "rate_regime",
        "cost_policy_id",
    ]
    rows: list[dict[str, Any]] = []
    totals = {
        (split, cost): int(group["is_trade"].astype(bool).sum())
        for (split, cost), group in frame.groupby(["split", "cost_policy_id"], dropna=False)
    }
    for axis in axes:
        group_cols = ["split", "cost_policy_id"] if axis == "cost_policy_id" else ["split", "cost_policy_id", axis]
        for key, group in frame.groupby(group_cols, dropna=False):
            if axis == "cost_policy_id":
                split, cost_policy = key
                value = cost_policy
            else:
                split, cost_policy, value = key
            rows.append(summarize_group(axis, value, split, cost_policy, group, totals.get((split, cost_policy), 0)))
    return rows


def build_slice_pocket_audit(slice_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str, str], dict[str, Mapping[str, Any]]] = {}
    for row in slice_rows:
        key = (str(row["slice_axis"]), str(row["slice_value"]), str(row["cost_policy_id"]))
        by_key.setdefault(key, {})[str(row["split"])] = row
    audits: list[dict[str, Any]] = []
    for (axis, value, cost_policy), splits in sorted(by_key.items()):
        validation = splits.get("validation", {})
        oos = splits.get("oos", {})
        val_trades = int(as_float(validation.get("trade_count", 0)))
        oos_trades = int(as_float(oos.get("trade_count", 0)))
        val_net = as_float(validation.get("net_after_cost", 0))
        oos_net = as_float(oos.get("net_after_cost", 0))
        val_pf = as_float(validation.get("profit_factor", 0))
        oos_pf = as_float(oos.get("profit_factor", 0))
        if val_trades < 50 or oos_trades < 50:
            status = "thin_slice_review_required"
        elif val_pf < 1.0 and oos_pf >= 1.10 and oos_net > 0:
            status = "oos_positive_validation_weak_slice"
        elif val_net <= 0 and oos_net > 0:
            status = "validation_negative_oos_positive_slice"
        else:
            status = "no_oos_only_flag"
        audits.append(
            {
                "slice_axis": axis,
                "slice_value": value,
                "cost_policy_id": cost_policy,
                "validation_trades": val_trades,
                "validation_net": val_net,
                "validation_pf": val_pf,
                "oos_trades": oos_trades,
                "oos_net": oos_net,
                "oos_pf": oos_pf,
                "pocket_status": status,
                "effect": "flags OOS-only or thin slice pockets(OOS 전용 또는 얇은 슬라이스 포켓 표시)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return audits


def build_oos_quarantine() -> list[dict[str, Any]]:
    divergence = read_csv(DF_DIVERGENCE)
    rows: list[dict[str, Any]] = []
    for row in divergence:
        validation_pf = as_float(row.get("validation_pf"))
        oos_pf = as_float(row.get("oos_pf"))
        gap = as_float(row.get("pf_gap_oos_minus_validation"))
        status = (
            "quarantined_oos_positive_validation_thin"
            if oos_pf >= 1.10 and validation_pf < 1.05
            else "read_only_not_quarantined"
        )
        rows.append(
            {
                "pair_id": row.get("pair_id", ""),
                "cost_policy_id": row.get("cost_policy_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "model_config_id": row.get("model_config_id", ""),
                "validation_pf": validation_pf,
                "oos_pf": oos_pf,
                "pf_gap_oos_minus_validation": gap,
                "quarantine_status": status,
                "forbidden_use": "no OOS winner selection(OOS 승자 선택 금지)",
                "effect": "turns OOS pocket into falsification evidence(OOS 포켓을 반증 근거로 전환)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_forbidden_selection(quarantine_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    quarantined = sum(1 for row in quarantine_rows if row.get("quarantine_status") == "quarantined_oos_positive_validation_thin")
    checks = [
        ("no_candidate_selected", "candidate selection(후보 선택)", "not_run", "not_run"),
        ("no_threshold_tuned", "threshold tuning(임계값 튜닝)", "not_run", "not_run"),
        ("no_lot_optimized", "lot optimization(로트 최적화)", "not_run", "not_run"),
        ("no_mt5_probe", "MT5 probe(MT5 탐침)", "not_run", "not_run"),
        ("oos_quarantine_present", "OOS quarantine(OOS 격리)", str(quarantined), ">0"),
    ]
    return [
        {
            "audit_id": audit_id,
            "blocked_action": action,
            "observed": observed,
            "expected": expected,
            "status": "passed" if (observed == expected or (expected == ">0" and int(observed) > 0)) else "failed",
            "effect": "keeps materialization from becoming selection(물질화가 선택으로 바뀌지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for audit_id, action, observed, expected in checks
    ]


def cost_order(policy: str) -> int:
    if "extra0" in policy:
        return 0
    if "extra2" in policy:
        return 2
    if "extra5" in policy:
        return 5
    return 999


def build_pair_surface() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pairs = pd.DataFrame(read_csv(DF_PAIR_SUMMARY))
    pairs["validation_pf"] = pd.to_numeric(pairs["validation_pf"], errors="coerce").fillna(0.0)
    pairs["oos_pf"] = pd.to_numeric(pairs["oos_pf"], errors="coerce").fillna(0.0)
    rows: list[dict[str, Any]] = []
    flags: list[dict[str, Any]] = []
    for (feature_set, model_config), group in pairs.groupby(["feature_set_id", "model_config_id"], dropna=False):
        by_cost = {cost_order(str(row["cost_policy_id"])): row for _, row in group.iterrows()}
        val_pfs = [float(row["validation_pf"]) for row in by_cost.values()]
        oos_pfs = [float(row["oos_pf"]) for row in by_cost.values()]
        val_max = max(val_pfs) if val_pfs else 0.0
        oos_max = max(oos_pfs) if oos_pfs else 0.0
        gap_max = max((float(row["oos_pf"]) - float(row["validation_pf"]) for row in by_cost.values()), default=0.0)
        status = "isolated_oos_surface_watch" if oos_max >= 1.10 and val_max < 1.05 else "surface_no_release"
        rows.append(
            {
                "feature_set_id": feature_set,
                "model_config_id": model_config,
                "validation_pf_extra0": float(by_cost.get(0, {}).get("validation_pf", 0.0)) if 0 in by_cost else 0.0,
                "validation_pf_extra2": float(by_cost.get(2, {}).get("validation_pf", 0.0)) if 2 in by_cost else 0.0,
                "validation_pf_extra5": float(by_cost.get(5, {}).get("validation_pf", 0.0)) if 5 in by_cost else 0.0,
                "oos_pf_extra0": float(by_cost.get(0, {}).get("oos_pf", 0.0)) if 0 in by_cost else 0.0,
                "oos_pf_extra2": float(by_cost.get(2, {}).get("oos_pf", 0.0)) if 2 in by_cost else 0.0,
                "oos_pf_extra5": float(by_cost.get(5, {}).get("oos_pf", 0.0)) if 5 in by_cost else 0.0,
                "validation_pf_max": val_max,
                "oos_pf_max": oos_max,
                "oos_minus_validation_gap_max": gap_max,
                "surface_status": status,
                "effect": "checks whether edge is smooth across cost policies(비용 정책 사이 우위가 매끄러운지 점검)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for _, row in group.iterrows():
            gap = float(row["oos_pf"]) - float(row["validation_pf"])
            if float(row["oos_pf"]) >= 1.10 and float(row["validation_pf"]) < 1.05:
                flags.append(
                    {
                        "flag_id": f"{row['pair_id']}__oos_validation_gap",
                        "pair_id": row["pair_id"],
                        "flag_type": "oos_positive_validation_thin",
                        "validation_pf": float(row["validation_pf"]),
                        "oos_pf": float(row["oos_pf"]),
                        "pf_gap_oos_minus_validation": gap,
                        "effect": "marks isolated OOS pocket before review(검토 전 고립 OOS 포켓 표시)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows, flags


def build_review_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DI_review_floor_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "review_task": "review validation PF floor frame and audit(검증 PF 하한 프레임과 감사 검토)",
            "required_inputs": f"{rel(FLOOR_FRAME)};{rel(FLOOR_AUDIT)}",
            "pass_condition": "floor inputs are complete and train-only thresholds remain fixed(하한 입력 완성 및 학습 전용 임계값 고정)",
            "fail_condition": "validation/OOS threshold fitting detected(검증/OOS 임계값 맞춤 발견)",
            "invalid_condition": "missing source rows or timestamp mismatch(원천 행 누락 또는 시각 불일치)",
            "effect": "decides whether inputs can feed a later repair training(이후 수리 학습 입력 가능 여부 판단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DI_review_slice_pockets",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "review_task": "review slice OOS-only pockets(슬라이스 OOS 전용 포켓 검토)",
            "required_inputs": f"{rel(SLICE_FRAME)};{rel(SLICE_POCKET_AUDIT)}",
            "pass_condition": "no dominant OOS-only slice concentration(지배적인 OOS 전용 슬라이스 집중 없음)",
            "fail_condition": "edge depends on thin OOS slice(우위가 얇은 OOS 슬라이스에 의존)",
            "invalid_condition": "slice labels use future outcome(슬라이스 라벨이 미래 결과 사용)",
            "effect": "tests whether pocket is robust or concentrated(포켓이 강건한지 집중인지 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DI_review_quarantine_and_surface",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "review_task": "review OOS quarantine and pair surface smoothness(OOS 격리와 쌍 표면 매끄러움 검토)",
            "required_inputs": f"{rel(OOS_QUARANTINE)};{rel(PAIR_SURFACE)};{rel(ISOLATED_FLAGS)}",
            "pass_condition": "OOS positive rows remain quarantined and surface is not isolated(OOS 양호 행 격리 유지 및 표면 비고립)",
            "fail_condition": "apparent edge is isolated to one pair/cost/model(겉보기 우위가 한 쌍/비용/모델에 고립)",
            "invalid_condition": "any selected candidate appears(선택 후보가 나타남)",
            "effect": "keeps overfit check ahead of any training(학습 전에 과적합 점검을 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "all required inputs exist(필수 입력 존재)"),
        ("parent_dg_gates_passed", final["dg_failed_gate_rows"] == 0, str(final["dg_failed_gate_rows"]), "0", "DG design is usable(DG 설계 사용 가능)"),
        ("parent_next_action_matches", final["dg_next_action"] == RUN_ID, str(final["dg_next_action"]), RUN_ID, "continues declared DG queue(DG 선언 대기열을 이어감)"),
        ("floor_frame_materialized", final["floor_frame_rows"] > 0, str(final["floor_frame_rows"]), ">0", "floor input frame exists(하한 입력 프레임 존재)"),
        ("floor_audit_materialized", final["floor_audit_rows"] >= 9, str(final["floor_audit_rows"]), ">=9", "split/cost audit exists(분할/비용 감사 존재)"),
        ("slice_frame_materialized", final["slice_frame_rows"] > 0, str(final["slice_frame_rows"]), ">0", "slice frame exists(슬라이스 프레임 존재)"),
        ("oos_quarantine_materialized", final["quarantined_pairs"] == final["parent_oos_positive_thin_rows"], str(final["quarantined_pairs"]), str(final["parent_oos_positive_thin_rows"]), "all OOS-positive thin pairs quarantined(OOS 양호/얇음 쌍 격리)"),
        ("pair_surface_materialized", final["pair_surface_rows"] > 0, str(final["pair_surface_rows"]), ">0", "pair surface controls exist(쌍 표면 대조 존재)"),
        ("review_queue_materialized", final["review_queue_rows"] >= 3, str(final["review_queue_rows"]), ">=3", "DI review queue exists(DI 검토 대기열 존재)"),
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
        "time_axis": "closed M5 UTC bar close inherited from DD/model input(DD/모델 입력의 닫힌 M5 UTC 봉마감 상속)",
        "sample_scope": f"floor_frame_rows={final['floor_frame_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};duplicate_keys={final['duplicate_floor_keys']}",
        "feature_label_boundary": "features are timestamp-joined at current bar; outcomes stay in DD label columns(피처는 현재 봉 시각 결합, 결과는 DD 라벨 열에 유지)",
        "split_boundary": "train thresholds inherited; validation/OOS read-only(학습 임계값 상속, 검증/OOS 읽기 전용)",
        "leakage_risk": "using OOS quarantine as selector(OOS 격리를 선택자로 사용)",
        "data_hash_or_identity": {
            "floor_frame": sha256_file(FLOOR_FRAME),
            "slice_frame": sha256_file(SLICE_FRAME),
            "model_input": sha256_file(MODEL_INPUT),
        },
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "none; materialization only(없음, 물질화 전용)",
        "target_and_label": "inherited DD stage1/stage2 labels(DD 1/2단계 라벨 상속)",
        "split_method": "inherited chronological train/validation/OOS(상속 시간순 학습/검증/OOS)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "floor audit, slice pockets, surface smoothness(하한 감사/슬라이스 포켓/표면 매끄러움)",
        "threshold_policy": "unchanged train-only thresholds(변경 없는 학습 전용 임계값)",
        "overfit_risk": "OOS pocket selection(OOS 포켓 선택)",
        "calibration_risk": "scores remain diagnostic(점수는 진단 전용)",
        "comparison_baseline": rel(DF_PAIR_SUMMARY),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "materialized row/slice evidence from DG design(DG 설계에서 행/슬라이스 근거 물질화)",
        "comparison_baseline": rel(DF_DIVERGENCE),
        "likely_drivers": "session, hour, month, volatility, ADX, VIX, USD, rate, cost policy(세션/시/월/변동성/ADX/VIX/USD/금리/비용 정책)",
        "segment_checks": f"slice_rows={final['slice_frame_rows']};oos_only_slice_flags={final['oos_only_slice_flags']}",
        "trade_shape": f"floor_trade_rows={final['floor_trade_rows']}",
        "alternative_explanations": "regime concentration or surface mining(국면 집중 또는 표면 채굴)",
        "attribution_confidence": "medium_for_materialization_low_for_final_cause(물질화는 중간, 최종 원인은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "floor frame, slice frame, OOS quarantine, surface controls(하한 프레임/슬라이스 프레임/OOS 격리/표면 대조)",
        "evidence_missing": "DI review and any later training/rerun(DI 검토와 이후 학습/재실행)",
        "judgment_label": "input_materialization",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이제 좋은 OOS가 어디서 나온 것인지 슬라이스와 비용 표면으로 검토할 수 있습니다.",
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
        "availability": "ignored_materialized_outputs_with_tracked_report(무시된 물질화 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DH Validation Pocket Cost-Shape Repair Inputs(검증 포켓 비용 곡선 수리 입력)

## Conclusion(결론)

run337DH(337DH 실행)는 DG 설계(design, 설계)를 실제 materialized inputs(물질화 입력)로 바꿨다.

floor frame(하한 프레임)은 `{final["floor_frame_rows"]}`행이고, slice stability frame(슬라이스 안정성 프레임)은 `{final["slice_frame_rows"]}`행이다. OOS quarantine(OOS 격리)은 부모 DF/DG가 표시한 `{final["parent_oos_positive_thin_rows"]}`개를 모두 격리했다.

Effect(효과): run337DI(337DI 실행)에서 검증 PF 하한, OOS 전용 슬라이스, 비용/피처/모델 표면 매끄러움을 검토할 수 있다. 아직 model training(모델 학습), candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)은 하지 않았다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- floor_frame_rows(하한 프레임 행): `{final["floor_frame_rows"]}`
- floor_audit_rows(하한 감사 행): `{final["floor_audit_rows"]}`
- slice_frame_rows(슬라이스 프레임 행): `{final["slice_frame_rows"]}`
- oos_only_slice_flags(OOS 전용 슬라이스 표시): `{final["oos_only_slice_flags"]}`
- quarantined_pairs(격리 쌍): `{final["quarantined_pairs"]}`
- pair_surface_rows(쌍 표면 행): `{final["pair_surface_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DH

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 검증 하한/슬라이스/OOS 격리/쌍 표면 대조 입력을 물질화했고, 다음은 review(검토)다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FLOOR_AUDIT)}`, `{rel(SLICE_POCKET_AUDIT)}`
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
        f"  Stage337 run337DH focus complete: validation pocket cost-shape repair inputs(검증 포켓 비용 곡선 수리 입력)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337DI(337DI 실행)에서 floor/slice/quarantine/surface(하한/슬라이스/격리/표면)를 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DH focus complete")
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
## Stage337 run337DH(337DH 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): validation PF floor/slice/OOS quarantine/pair surface(검증 PF 하한/슬라이스/OOS 격리/쌍 표면) 입력을 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DG(337DG"
    if "## Stage337 run337DH(337DH 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_dh_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 validation pocket cost-shape repair input review(검증 포켓 비용 곡선 수리 입력 검토)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DH(337DH 실행) materialized validation pocket cost-shape repair inputs(검증 포켓 비용 곡선 수리 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DH(337DH 실행) materialized validation pocket"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DH materialized validation pocket cost-shape repair inputs(검증 포켓 비용 곡선 수리 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DH materialized validation pocket"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_pocket_cost_shape_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"floor_rows={final['floor_frame_rows']};slice_rows={final['slice_frame_rows']};quarantine={final['quarantined_pairs']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "input_materialization_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "floor_slice_quarantine_surface_inputs",
        "scoreboard_lane": "data_integrity_model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"floor_rows={final['floor_frame_rows']};slice_rows={final['slice_frame_rows']}",
        "guardrail_kpi": "no_selection;no_threshold_tuning;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "DG design materialized into repair input artifacts",
        "kpi_scope": "validation_floor_slice_quarantine_surface",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_inputs",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "can validation pocket repair inputs be materialized without OOS selection",
        "metric_scope": "floor_frame_slice_pockets_oos_quarantine_surface",
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

    dg_final = read_json(DG_FINAL)
    dg_gates = read_csv(DG_GATES)
    frame = build_floor_frame()
    duplicate_keys = int(frame.duplicated(["source_row_id", "split", "cost_policy_id"]).sum())
    floor_path = write_floor_frame(frame)
    floor_rows = summarize_floor(frame)
    slice_rows = build_slice_frame(frame)
    slice_audit_rows = build_slice_pocket_audit(slice_rows)
    quarantine_rows = build_oos_quarantine()
    forbidden_rows = build_forbidden_selection(quarantine_rows)
    surface_rows, flag_rows = build_pair_surface()
    queue_rows = build_review_queue()
    artifacts: list[Path] = [
        floor_path,
        write_csv(FLOOR_AUDIT, FLOOR_AUDIT_COLUMNS, floor_rows),
        write_csv(SLICE_FRAME, SLICE_COLUMNS, slice_rows),
        write_csv(SLICE_POCKET_AUDIT, SLICE_AUDIT_COLUMNS, slice_audit_rows),
        write_csv(OOS_QUARANTINE, QUARANTINE_COLUMNS, quarantine_rows),
        write_csv(FORBIDDEN_SELECTION, FORBIDDEN_COLUMNS, forbidden_rows),
        write_csv(PAIR_SURFACE, SURFACE_COLUMNS, surface_rows),
        write_csv(ISOLATED_FLAGS, FLAG_COLUMNS, flag_rows),
        write_csv(DI_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    quarantined = sum(1 for row in quarantine_rows if row["quarantine_status"] == "quarantined_oos_positive_validation_thin")
    oos_only_slice_flags = sum(
        1
        for row in slice_audit_rows
        if row["pocket_status"] in {"oos_positive_validation_weak_slice", "validation_negative_oos_positive_slice"}
    )
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dg_next_action": dg_final.get("next_action", ""),
        "dg_failed_gate_rows": sum(1 for row in dg_gates if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "duplicate_floor_keys": duplicate_keys,
        "floor_frame_rows": int(len(frame)),
        "floor_trade_rows": int(frame["is_trade"].astype(bool).sum()),
        "floor_audit_rows": len(floor_rows),
        "slice_frame_rows": len(slice_rows),
        "slice_pocket_audit_rows": len(slice_audit_rows),
        "oos_only_slice_flags": oos_only_slice_flags,
        "quarantined_pairs": quarantined,
        "parent_oos_positive_thin_rows": int(dg_final.get("oos_positive_thin_rows", 0)),
        "pair_surface_rows": len(surface_rows),
        "isolated_pocket_flags": len(flag_rows),
        "forbidden_audit_rows": len(forbidden_rows),
        "review_queue_rows": len(queue_rows),
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
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
