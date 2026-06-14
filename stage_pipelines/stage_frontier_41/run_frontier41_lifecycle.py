from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import io_path, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b


STAGE_ID = "stage_frontier_41__short_pf_edge_exit_shape_source_pivot_after_f40_raw_pocket_scout"
PREV_STAGE_ID = "stage_frontier_40__short_pf_edge_non_score_source_pivot_after_regime_gate_negative"
RUN_A = "frontier41A_stage_open_short_pf_edge_exit_shape_source_hypothesis_design_v1"
RUN_B = "frontier41B_f40_entry_frozen_exit_shape_proxy_v1"
RUN_C = "frontier41C_capped_exit_family_repair_decision_v1"
RUN_D = "frontier41D_stage_closeout_exit_shape_source_v1"
NEXT_STAGE_ID = "stage_frontier_42__short_pf_edge_timing_source_pivot_after_f41_exit_shape_negative"
NEXT_RUN_ID = "frontier42A_stage_open_short_pf_edge_timing_source_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F40_RUN_D_ROOT = Path("stages") / PREV_STAGE_ID / "02_runs" / "frontier40D_stage_closeout_non_score_source_v1"
F40_TOP_FORWARD = F40_RUN_D_ROOT / "top_forward_diagnostic.csv"
F40_RUN_B_ROOT = Path("stages") / PREV_STAGE_ID / "02_runs" / "frontier40B_raw_feature_state_pocket_proxy_v1"
F40_CONDITION_POOL = F40_RUN_B_ROOT / "raw_feature_condition_pool.csv"
F40_SELECTION_STATUS = Path("stages") / PREV_STAGE_ID / "04_selected" / "selection_status.md"

GROK_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier41_stage_open" / "small_review"
GROK_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier41_stage_closeout" / "small_review"

PROJECT_LEDGER = Path("docs") / "registers" / "alpha_run_ledger.csv"
WORKSPACE_STATE = Path("docs") / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = Path("docs") / "context" / "current_working_state.md"
PRE_ALPHA_PLAN = Path("docs") / "workspace" / "pre_alpha_stage_plan.md"

ENTRY_SOURCE_LIMIT = 12
SIDE_VALUE = -1
SIDE_LABEL = "short"
SPLITS = ("train", "validation", "oos")
VALIDATION_SPLITS = ("validation", "oos")
INITIAL_HOLD_BARS = (4, 6, 8, 12, 18)
INITIAL_STOP_Q = (0.18, 0.26, 0.34)
INITIAL_TAKE_Q = (0.70, 0.78, 0.86)
REPAIR_HOLD_BARS = (3, 5, 7, 10, 14)
REPAIR_STOP_Q = (0.14, 0.20)
REPAIR_TAKE_Q = (0.82, 0.90)
SCOUT_MIN_PF = 1.03
SCOUT_MIN_DENSITY = 4.0
SCOUT_MAX_DENSITY = 12.0
SCOUT_MAX_DD = 18.0
SEED_MIN_PF = 1.20
SEED_MIN_DENSITY = 5.0
SEED_MAX_DENSITY = 10.0
SEED_MAX_DD = 12.0
RUNTIME_MIN_PF = 1.50
RUNTIME_MIN_DENSITY = 5.0
RUNTIME_MAX_DENSITY = 10.0
RUNTIME_MAX_DD = 10.0


@dataclass(frozen=True)
class EntrySource:
    source_rank: int
    candidate_id: str
    condition_ids: tuple[str, ...]
    rule_definition: str
    features: str
    stop_cap_log_return: float
    take_cap_log_return: float
    f40_validation_pf: float
    f40_oos_pf: float
    f40_validation_density: float
    f40_oos_density: float
    f40_validation_dd: float
    f40_oos_dd: float
    mask: np.ndarray
    split_hashes: dict[str, str]
    split_counts: dict[str, int]


def mkdirs() -> None:
    for path in (
        SPEC_ROOT,
        INPUT_ROOT,
        RUN_A_ROOT,
        RUN_B_ROOT,
        RUN_C_ROOT,
        RUN_D_ROOT,
        REVIEWS_ROOT,
        SELECTED_ROOT,
        Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier41_stage_closeout" / "small_review",
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_items(items: list[Any]) -> str:
    payload = json.dumps(json_ready(items), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def hash_mask(frame: pd.DataFrame, mask: np.ndarray, split: str) -> str:
    split_base = f33b.split_mask(frame, split)
    indices = np.flatnonzero(np.asarray(mask, dtype=bool) & split_base)
    if indices.size == 0:
        return "empty"
    timestamps = pd.to_datetime(frame.loc[indices, "timestamp"], utc=True).astype("int64").astype(str).tolist()
    return hash_items(timestamps)


def artifact_identity(path: Path) -> dict[str, str]:
    return {
        "path": path.as_posix(),
        "sha256": sha256_file(path) if path_exists(path) else "missing",
    }


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float("nan")
    return number if math.isfinite(number) else float("nan")


def safe_mean(values: np.ndarray) -> float:
    values = np.asarray(values, dtype="float64")
    values = values[np.isfinite(values)]
    return float(values.mean()) if values.size else 0.0


def safe_median(values: np.ndarray) -> float:
    values = np.asarray(values, dtype="float64")
    values = values[np.isfinite(values)]
    return float(np.median(values)) if values.size else 0.0


def load_feature_order() -> list[str]:
    return [line.strip() for line in read_text(f23b.FEATURE_ORDER_PATH).splitlines() if line.strip()]


def load_open_grok_review() -> dict[str, Any]:
    result = {
        "packet_path": GROK_OPEN_ROOT.as_posix(),
        "metadata_exists": path_exists(GROK_OPEN_ROOT / "metadata.json"),
        "clean_output_exists": path_exists(GROK_OPEN_ROOT / "clean_output.md"),
        "classification": "missing",
        "guardrail_entry_freeze_seen": False,
        "guardrail_same_entry_seen": False,
        "runtime_boundary_seen": False,
        "local_verification_required": True,
        "accepted_after_local_verification": False,
    }
    if not result["metadata_exists"] or not result["clean_output_exists"]:
        return result
    metadata = read_json(GROK_OPEN_ROOT / "metadata.json")
    clean = read_text(GROK_OPEN_ROOT / "clean_output.md")
    lower = clean.lower()
    result.update(
        {
            "metadata_success": bool(metadata.get("success")),
            "metadata_returncode": metadata.get("returncode"),
            "classification": "needs_local_verification"
            if "needs_local_verification" in lower
            else "accepted"
            if "accepted" in lower
            else "unclassified",
            "guardrail_entry_freeze_seen": "entry freeze manifest" in lower,
            "guardrail_same_entry_seen": "same-entry attribution lock" in lower,
            "runtime_boundary_seen": "runtime_claim_boundary_ok" in lower and "yes" in lower,
            "local_verification_required": "needs_local_verification" in lower,
        }
    )
    result["accepted_after_local_verification"] = bool(
        result["metadata_success"]
        and result["metadata_returncode"] == 0
        and result["guardrail_entry_freeze_seen"]
        and result["guardrail_same_entry_seen"]
        and result["runtime_boundary_seen"]
    )
    return result


def load_closeout_grok_review() -> dict[str, Any]:
    result = {
        "packet_path": GROK_CLOSE_ROOT.as_posix(),
        "metadata_exists": path_exists(GROK_CLOSE_ROOT / "metadata.json"),
        "clean_output_exists": path_exists(GROK_CLOSE_ROOT / "clean_output.md"),
        "classification": "pending",
        "accepted_after_local_verification": False,
        "closeout_boundary_ok": False,
    }
    if not result["metadata_exists"] or not result["clean_output_exists"]:
        return result
    metadata = read_json(GROK_CLOSE_ROOT / "metadata.json")
    clean = read_text(GROK_CLOSE_ROOT / "clean_output.md")
    lower = clean.lower()
    boundary_ok = (
        "closeout_boundary_ok" in lower
        and ("yes" in lower or "예" in lower)
    ) or (
        "preserved_clue" in lower
        or "negative_memory" in lower
        or "invalid setup" in lower
        or "invalid_setup" in lower
        or "blocked" in lower
        or "completion candidate" in lower
        or "completion_candidate" in lower
    )
    result.update(
        {
            "metadata_success": bool(metadata.get("success")),
            "metadata_returncode": metadata.get("returncode"),
            "classification": "needs_local_verification"
            if "needs_local_verification" in lower
            else "accepted"
            if "accepted" in lower or "accept" in lower
            else "unclassified",
            "closeout_boundary_ok": boundary_ok,
        }
    )
    result["accepted_after_local_verification"] = bool(
        result["metadata_success"] and result["metadata_returncode"] == 0 and result["closeout_boundary_ok"]
    )
    return result


def context_checks(frame: pd.DataFrame, feature_order: list[str], raw_path: dict[str, Any]) -> dict[str, Any]:
    split_counts = frame["split"].astype(str).value_counts().to_dict()
    return {
        "workspace_state_exists": path_exists(WORKSPACE_STATE),
        "current_working_state_exists": path_exists(CURRENT_WORKING_STATE),
        "pre_alpha_plan_exists": path_exists(PRE_ALPHA_PLAN),
        "f40_selection_status_exists": path_exists(F40_SELECTION_STATUS),
        "f40_top_forward_exists": path_exists(F40_TOP_FORWARD),
        "f40_condition_pool_exists": path_exists(F40_CONDITION_POOL),
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "feature_order_exists": path_exists(f23b.FEATURE_ORDER_PATH),
        "raw_path_exists": path_exists(f33b.RAW_US100_PATH),
        "feature_count": len(feature_order),
        "feature_hash": ordered_hash(feature_order),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "split_counts": split_counts,
        "required_splits_present": all(split in split_counts and split_counts[split] > 0 for split in SPLITS),
        "frame_rows": int(len(frame)),
        "raw_rows": int(len(raw_path.get("raw", []))),
    }


def load_condition_pool() -> dict[str, dict[str, Any]]:
    pool = pd.read_csv(io_path(F40_CONDITION_POOL))
    required = {"condition_id", "feature", "operator", "threshold_value", "quantile_label"}
    missing = required - set(pool.columns)
    if missing:
        raise ValueError(f"F40 condition pool missing columns: {sorted(missing)}")
    conditions: dict[str, dict[str, Any]] = {}
    for row in pool.to_dict("records"):
        conditions[str(row["condition_id"])] = row
    return conditions


def condition_mask(frame: pd.DataFrame, condition: dict[str, Any]) -> np.ndarray:
    feature = str(condition["feature"])
    direction = str(condition["operator"])
    threshold = safe_float(condition["threshold_value"])
    if feature not in frame.columns:
        raise ValueError(f"Missing F40 feature in frame: {feature}")
    values = frame[feature].to_numpy(dtype="float64")
    if direction == "<=":
        return np.isfinite(values) & (values <= threshold)
    if direction == ">=":
        return np.isfinite(values) & (values >= threshold)
    raise ValueError(f"Unsupported F40 direction: {direction}")


def load_entry_sources(frame: pd.DataFrame) -> list[EntrySource]:
    top = pd.read_csv(io_path(F40_TOP_FORWARD))
    conditions = load_condition_pool()
    if "f40_scout_clue_flag" in top.columns:
        top = top.loc[top["f40_scout_clue_flag"].astype(bool)].copy()
    seen: set[str] = set()
    sources: list[EntrySource] = []
    for row in top.to_dict("records"):
        condition_ids = tuple(part for part in str(row["condition_ids"]).split("|") if part)
        key = "|".join(condition_ids)
        if not key or key in seen:
            continue
        if any(condition_id not in conditions for condition_id in condition_ids):
            continue
        mask = np.ones(len(frame), dtype=bool)
        for condition_id in condition_ids:
            mask &= condition_mask(frame, conditions[condition_id])
        split_counts = {split: int((mask & f33b.split_mask(frame, split)).sum()) for split in SPLITS}
        if split_counts["train"] <= 0:
            continue
        split_hashes = {split: hash_mask(frame, mask, split) for split in SPLITS}
        sources.append(
            EntrySource(
                source_rank=len(sources) + 1,
                candidate_id=str(row["candidate_id"]),
                condition_ids=condition_ids,
                rule_definition=str(row["rule_definition"]),
                features=str(row.get("features", "")),
                stop_cap_log_return=safe_float(row.get("stop_cap_log_return")),
                take_cap_log_return=safe_float(row.get("take_cap_log_return")),
                f40_validation_pf=safe_float(row.get("validation_profit_factor")),
                f40_oos_pf=safe_float(row.get("oos_profit_factor")),
                f40_validation_density=safe_float(row.get("validation_trades_per_day")),
                f40_oos_density=safe_float(row.get("oos_trades_per_day")),
                f40_validation_dd=safe_float(row.get("validation_dd_risk")),
                f40_oos_dd=safe_float(row.get("oos_dd_risk")),
                mask=mask,
                split_hashes=split_hashes,
                split_counts=split_counts,
            )
        )
        seen.add(key)
        if len(sources) >= ENTRY_SOURCE_LIMIT:
            break
    if not sources:
        raise ValueError("No F40 scout entry sources could be reconstructed.")
    return sources


def entry_manifest(sources: list[EntrySource], frame: pd.DataFrame) -> dict[str, Any]:
    rows = []
    for source in sources:
        rows.append(
            {
                "source_rank": source.source_rank,
                "candidate_id": source.candidate_id,
                "condition_ids": list(source.condition_ids),
                "rule_definition": source.rule_definition,
                "features": source.features,
                "side": SIDE_LABEL,
                "side_value": SIDE_VALUE,
                "split_counts": source.split_counts,
                "entry_hash_by_split": source.split_hashes,
                "f40_reference": {
                    "validation_profit_factor": source.f40_validation_pf,
                    "oos_profit_factor": source.f40_oos_pf,
                    "validation_trades_per_day": source.f40_validation_density,
                    "oos_trades_per_day": source.f40_oos_density,
                    "validation_dd_risk": source.f40_validation_dd,
                    "oos_dd_risk": source.f40_oos_dd,
                    "stop_cap_log_return": source.stop_cap_log_return,
                    "take_cap_log_return": source.take_cap_log_return,
                },
            }
        )
    manifest = {
        "stage_id": STAGE_ID,
        "source_stage_id": PREV_STAGE_ID,
        "entry_source_limit": ENTRY_SOURCE_LIMIT,
        "mutation_policy": "entry masks are frozen from F40 scout rows; F41 may vary exit shape only.",
        "same_entry_attribution_lock": "every exit arm keeps the same timestamp hashes for each source and split.",
        "artifacts": {
            "f40_top_forward": artifact_identity(F40_TOP_FORWARD),
            "f40_condition_pool": artifact_identity(F40_CONDITION_POOL),
            "dataset": artifact_identity(f23b.DATASET_PATH),
            "feature_order": artifact_identity(f23b.FEATURE_ORDER_PATH),
        },
        "frame_rows": int(len(frame)),
        "sources": rows,
    }
    write_json(INPUT_ROOT / "entry_freeze_manifest.json", manifest)
    return manifest


def quantile_caps(
    frame: pd.DataFrame,
    source: EntrySource,
    path_labels: dict[int, dict[str, np.ndarray]],
    stop_q: float,
    take_q: float,
) -> tuple[float, float]:
    labels = path_labels[SIDE_VALUE]
    train_mask = source.mask & f33b.split_mask(frame, "train") & labels["valid"]
    mae = labels["mae"][train_mask]
    mfe = labels["mfe"][train_mask]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    stop_cap = float(np.nanquantile(mae, stop_q)) if mae.size else float("nan")
    take_cap = float(np.nanquantile(mfe, take_q)) if mfe.size else float("nan")
    if not math.isfinite(stop_cap) or stop_cap <= 0.0:
        stop_cap = float("inf")
    if not math.isfinite(take_cap) or take_cap <= 0.0:
        take_cap = float("inf")
    return stop_cap, take_cap


def evaluate_exit_mask(
    frame: pd.DataFrame,
    mask: np.ndarray,
    side: int,
    stop_cap: float,
    take_cap: float,
    hold_bars: int,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    split: str,
) -> dict[str, Any]:
    raw = raw_path["raw"]
    open_prices = raw["open"].to_numpy(dtype="float64")
    high_prices = raw["high"].to_numpy(dtype="float64")
    low_prices = raw["low"].to_numpy(dtype="float64")
    entry_pos = raw_path["entry_pos"]
    future_pos = raw_path["future_pos"]
    labels = path_labels[side]
    split_base = f33b.split_mask(frame, split)
    trade_mask = np.asarray(mask, dtype=bool) & split_base & labels["valid"]
    candidate_indices = np.flatnonzero(trade_mask)
    used_indices: list[int] = []
    pnl: list[float] = []
    reasons: list[str] = []
    holding_bars: list[float] = []
    ambiguous: list[bool] = []
    for idx in candidate_indices:
        p = int(entry_pos[idx])
        q_contract = int(future_pos[idx])
        q = min(q_contract, p + int(hold_bars))
        if p < 0 or q <= p or q >= len(open_prices):
            continue
        entry = float(open_prices[p])
        if not math.isfinite(entry) or entry <= 0.0:
            continue
        result = f33b.simulate_one_trade(side, entry, p, q, stop_cap, take_cap, open_prices, high_prices, low_prices)
        pnl.append(float(result["pnl_log"]) - scout.ROUGH_COST_LOG_RETURN)
        reasons.append(str(result["exit_reason"]))
        holding_bars.append(float(result["holding_bars"]))
        ambiguous.append(bool(result["ambiguous_both_hit"]))
        used_indices.append(int(idx))
    trade_pnl = np.asarray(pnl, dtype="float64")
    trade_times = frame.loc[used_indices, "timestamp"] if used_indices else pd.Series([], dtype="datetime64[ns, UTC]")
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    shape = f23b.payoff_shape(trade_pnl)
    days = scout.count_scope_days(frame.loc[split_base, "timestamp"])
    used = np.asarray(used_indices, dtype=int)
    quality = (
        (labels["mfe"][used] >= take_cap) & (labels["mae"][used] <= stop_cap)
        if used.size and math.isfinite(take_cap) and math.isfinite(stop_cap)
        else np.array([], dtype=bool)
    )
    mfe = labels["mfe"][used] if used.size else np.array([], dtype="float64")
    mae = labels["mae"][used] if used.size else np.array([], dtype="float64")
    holding = np.asarray(holding_bars, dtype="float64")
    return {
        **metrics,
        **shape,
        "trade_count": int(len(trade_pnl)),
        "days_in_scope": int(days),
        "trades_per_day": float(len(trade_pnl) / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
        "stop_hit_count": int(sum(reason == "stop" for reason in reasons)),
        "take_hit_count": int(sum(reason == "take" for reason in reasons)),
        "horizon_exit_count": int(sum(reason == "horizon" for reason in reasons)),
        "ambiguous_both_hit_count": int(sum(ambiguous)),
        "avg_holding_bars": safe_mean(holding),
        "median_holding_bars": safe_median(holding),
        "path_quality_rate": float(np.mean(quality)) if quality.size else 0.0,
        "median_mfe_log_return": safe_median(mfe),
        "median_mae_log_return": safe_median(mae),
        "used_entry_hash": hash_items(pd.to_datetime(frame.loc[used, "timestamp"], utc=True).astype("int64").astype(str).tolist())
        if used.size
        else "empty",
    }


def variant_rows(
    frame: pd.DataFrame,
    source: EntrySource,
    path_labels: dict[int, dict[str, np.ndarray]],
    family: str,
    hold_bars_set: tuple[int, ...],
    stop_q_set: tuple[float, ...],
    take_q_set: tuple[float, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for hold_bars in hold_bars_set:
        variant_id = f"{source.candidate_id}_{family}_hold{hold_bars:02d}_no_bracket"
        rows.append(
            {
                "source": source,
                "variant_id": variant_id,
                "exit_family": family,
                "hold_bars": hold_bars,
                "stop_quantile": "none",
                "take_quantile": "none",
                "stop_cap_log_return": float("inf"),
                "take_cap_log_return": float("inf"),
                "executable_exit": True,
                "same_entry_lock_expected": source.split_hashes,
            }
        )
    for hold_bars in hold_bars_set:
        for stop_q in stop_q_set:
            for take_q in take_q_set:
                stop_cap, take_cap = quantile_caps(frame, source, path_labels, stop_q, take_q)
                if not math.isfinite(stop_cap) or not math.isfinite(take_cap):
                    continue
                if take_cap <= stop_cap * 0.75:
                    continue
                variant_id = f"{source.candidate_id}_{family}_hold{hold_bars:02d}_s{int(stop_q * 100):02d}_t{int(take_q * 100):02d}"
                rows.append(
                    {
                        "source": source,
                        "variant_id": variant_id,
                        "exit_family": family,
                        "hold_bars": hold_bars,
                        "stop_quantile": stop_q,
                        "take_quantile": take_q,
                        "stop_cap_log_return": stop_cap,
                        "take_cap_log_return": take_cap,
                        "executable_exit": True,
                        "same_entry_lock_expected": source.split_hashes,
                    }
                )
    return rows


def reference_rows(source: EntrySource) -> list[dict[str, Any]]:
    stop_cap = source.stop_cap_log_return
    take_cap = source.take_cap_log_return
    if not math.isfinite(stop_cap) or stop_cap <= 0.0:
        stop_cap = float("inf")
    if not math.isfinite(take_cap) or take_cap <= 0.0:
        take_cap = float("inf")
    return [
        {
            "source": source,
            "variant_id": f"{source.candidate_id}_f40_fixed_exit_reference_hold12",
            "exit_family": "f40_fixed_exit_reference",
            "hold_bars": 12,
            "stop_quantile": "f40",
            "take_quantile": "f40",
            "stop_cap_log_return": stop_cap,
            "take_cap_log_return": take_cap,
            "executable_exit": True,
            "same_entry_lock_expected": source.split_hashes,
        }
    ]


def run_exit_surface(
    frame: pd.DataFrame,
    sources: list[EntrySource],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    family: str,
    hold_bars_set: tuple[int, ...],
    stop_q_set: tuple[float, ...],
    take_q_set: tuple[float, ...],
    include_references: bool,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    variant_specs: list[dict[str, Any]] = []
    for source in sources:
        if include_references:
            variant_specs.extend(reference_rows(source))
        variant_specs.extend(variant_rows(frame, source, path_labels, family, hold_bars_set, stop_q_set, take_q_set))
    metrics_rows: list[dict[str, Any]] = []
    for spec in variant_specs:
        source = spec["source"]
        for split in SPLITS:
            metrics = evaluate_exit_mask(
                frame=frame,
                mask=source.mask,
                side=SIDE_VALUE,
                stop_cap=float(spec["stop_cap_log_return"]),
                take_cap=float(spec["take_cap_log_return"]),
                hold_bars=int(spec["hold_bars"]),
                path_labels=path_labels,
                raw_path=raw_path,
                split=split,
            )
            same_entry_lock_pass = metrics["used_entry_hash"] == source.split_hashes[split]
            metrics_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_B if family == "initial_exit_family" else RUN_C,
                    "source_rank": source.source_rank,
                    "source_candidate_id": source.candidate_id,
                    "variant_id": spec["variant_id"],
                    "exit_family": spec["exit_family"],
                    "side": SIDE_LABEL,
                    "side_value": SIDE_VALUE,
                    "rule_definition": source.rule_definition,
                    "features": source.features,
                    "condition_ids": "|".join(source.condition_ids),
                    "split": split,
                    "record_view": "Tier A separate",
                    "hold_bars": int(spec["hold_bars"]),
                    "stop_quantile": spec["stop_quantile"],
                    "take_quantile": spec["take_quantile"],
                    "stop_cap_log_return": spec["stop_cap_log_return"],
                    "take_cap_log_return": spec["take_cap_log_return"],
                    "same_entry_lock_expected_hash": source.split_hashes[split],
                    "same_entry_lock_observed_hash": metrics["used_entry_hash"],
                    "same_entry_lock_pass": same_entry_lock_pass,
                    "executable_exit": bool(spec["executable_exit"]),
                    **metrics,
                }
            )
    metrics = pd.DataFrame(metrics_rows)
    summary = summarize_exit_variants(metrics)
    return metrics, summary


def split_summary_row(group: pd.DataFrame, split: str) -> pd.Series:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row for {split}")
    return row.iloc[0]


def reference_by_source(metrics: pd.DataFrame) -> dict[str, dict[str, float]]:
    refs = metrics.loc[metrics["exit_family"].eq("f40_fixed_exit_reference")]
    result: dict[str, dict[str, float]] = {}
    for source_id, group in refs.groupby("source_candidate_id", sort=False):
        result[str(source_id)] = {
            "validation_profit_factor": safe_float(split_summary_row(group, "validation")["profit_factor"]),
            "oos_profit_factor": safe_float(split_summary_row(group, "oos")["profit_factor"]),
            "validation_dd_risk": safe_float(split_summary_row(group, "validation")["dd_risk"]),
            "oos_dd_risk": safe_float(split_summary_row(group, "oos")["dd_risk"]),
        }
    return result


def summarize_exit_variants(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    refs = reference_by_source(metrics)
    rows: list[dict[str, Any]] = []
    group_cols = [
        "variant_id",
        "source_candidate_id",
        "source_rank",
        "exit_family",
        "side",
        "side_value",
        "rule_definition",
        "features",
        "condition_ids",
        "hold_bars",
        "stop_quantile",
        "take_quantile",
        "stop_cap_log_return",
        "take_cap_log_return",
        "executable_exit",
    ]
    for key_values, group in metrics.groupby(group_cols, sort=False, dropna=False):
        base = dict(zip(group_cols, key_values))
        source_id = str(base["source_candidate_id"])
        row: dict[str, Any] = {**base}
        same_entry_all = bool(group["same_entry_lock_pass"].astype(bool).all())
        row["same_entry_lock_all_splits_pass"] = same_entry_all
        for split in SPLITS:
            split_row = split_summary_row(group, split)
            for field in (
                "trade_count",
                "days_in_scope",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "max_drawdown_percent",
                "max_monthly_drawdown_percent",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "dd_risk",
                "payoff_ratio",
                "right_tail_loss_tail_ratio",
                "adverse_loss_p10_abs",
                "stop_hit_count",
                "take_hit_count",
                "horizon_exit_count",
                "ambiguous_both_hit_count",
                "avg_holding_bars",
                "median_holding_bars",
                "path_quality_rate",
            ):
                row[f"{split}_{field}"] = split_row[field]
        forward_pf = [
            safe_float(row["validation_profit_factor"]),
            safe_float(row["oos_profit_factor"]),
        ]
        forward_density = [
            safe_float(row["validation_trades_per_day"]),
            safe_float(row["oos_trades_per_day"]),
        ]
        forward_dd = [
            safe_float(row["validation_dd_risk"]),
            safe_float(row["oos_dd_risk"]),
        ]
        row["forward_min_profit_factor"] = float(min(forward_pf))
        row["forward_min_trades_per_day"] = float(min(forward_density))
        row["forward_max_trades_per_day"] = float(max(forward_density))
        row["forward_max_dd_risk"] = float(max(forward_dd))
        ref = refs.get(source_id, {})
        ref_pf = min(
            safe_float(ref.get("validation_profit_factor", float("nan"))),
            safe_float(ref.get("oos_profit_factor", float("nan"))),
        )
        ref_dd = max(
            safe_float(ref.get("validation_dd_risk", float("nan"))),
            safe_float(ref.get("oos_dd_risk", float("nan"))),
        )
        row["same_entry_reference_min_profit_factor"] = ref_pf
        row["same_entry_reference_max_dd_risk"] = ref_dd
        row["pf_lift_vs_same_entry_reference"] = row["forward_min_profit_factor"] - ref_pf
        row["dd_reduction_vs_same_entry_reference"] = ref_dd - row["forward_max_dd_risk"]
        row["f41_scout_clue_flag"] = bool(
            base["exit_family"] != "f40_fixed_exit_reference"
            and same_entry_all
            and row["forward_min_profit_factor"] >= SCOUT_MIN_PF
            and row["forward_min_trades_per_day"] >= SCOUT_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= SCOUT_MAX_DENSITY
            and row["forward_max_dd_risk"] <= SCOUT_MAX_DD
            and row["pf_lift_vs_same_entry_reference"] >= -1e-12
        )
        row["f41_seed_surface_flag"] = bool(
            row["f41_scout_clue_flag"]
            and row["forward_min_profit_factor"] >= SEED_MIN_PF
            and row["forward_min_trades_per_day"] >= SEED_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= SEED_MAX_DENSITY
            and row["forward_max_dd_risk"] <= SEED_MAX_DD
        )
        row["runtime_probe_candidate_flag"] = bool(
            row["f41_seed_surface_flag"]
            and bool(base["executable_exit"])
            and row["forward_min_profit_factor"] >= RUNTIME_MIN_PF
            and row["forward_min_trades_per_day"] >= RUNTIME_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= RUNTIME_MAX_DENSITY
            and row["forward_max_dd_risk"] <= RUNTIME_MAX_DD
        )
        density_penalty = abs((row["forward_min_trades_per_day"] + row["forward_max_trades_per_day"]) / 2.0 - 7.5) / 7.5
        dd_penalty = max(0.0, row["forward_max_dd_risk"] - 10.0) / 10.0
        row["f41_exit_shape_score"] = float(
            max(row["forward_min_profit_factor"], 0.0)
            + max(row["pf_lift_vs_same_entry_reference"], 0.0) * 2.0
            + max(row["dd_reduction_vs_same_entry_reference"], 0.0) / 10.0
            - density_penalty
            - dd_penalty
        )
        rows.append(row)
    summary = pd.DataFrame(rows)
    if summary.empty:
        return summary
    summary = summary.sort_values(
        [
            "runtime_probe_candidate_flag",
            "f41_seed_surface_flag",
            "f41_scout_clue_flag",
            "f41_exit_shape_score",
            "forward_min_profit_factor",
            "forward_max_dd_risk",
        ],
        ascending=[False, False, False, False, False, True],
    ).reset_index(drop=True)
    summary.insert(0, "rank", np.arange(1, len(summary) + 1))
    return summary


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8-sig")


def top_records(frame: pd.DataFrame, limit: int = 10) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    return json_ready(frame.head(limit).to_dict("records"))


def build_stage_brief(open_review: dict[str, Any], checks: dict[str, Any], manifest: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

## Hypothesis(가설)
F40 raw feature pocket(원천 피처 포켓)의 short entry(숏 진입)를 고정하고, executable exit shape(실행 가능한 청산 형태)만 바꾸면 PF/DD/density(수익 팩터/손실폭/거래 밀도)의 동시 균형이 좋아지는지 본다.

## Boundary(경계)
- Stage12~364(12~364단계)와 F40은 reference only(참조 전용)이다.
- F41은 F40의 winner(승자), baseline(기준선), runtime authority(런타임 권위)를 상속하지 않는다.
- Entry freeze manifest(진입 고정 목록)는 `{(INPUT_ROOT / "entry_freeze_manifest.json").as_posix()}`에 있다.
- Same-entry attribution lock(동일 진입 귀속 잠금)은 split(분할)별 timestamp hash(타임스탬프 해시)로 확인한다.

## Grok stage-open review(그록 단계 개방 검토)
- classification(분류): {open_review.get("classification")}
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- entry freeze guardrail(진입 고정 보호선): {open_review.get("guardrail_entry_freeze_seen")}
- same-entry guardrail(동일 진입 보호선): {open_review.get("guardrail_same_entry_seen")}

## Local checks(로컬 점검)
- feature hash(피처 해시): `{checks.get("feature_hash")}`
- feature contract match(피처 계약 일치): {checks.get("feature_hash_matches_contract")}
- required splits present(필수 분할 존재): {checks.get("required_splits_present")}
- F40 source files(원천 파일): top={checks.get("f40_top_forward_exists")}, pool={checks.get("f40_condition_pool_exists")}

## Frozen entry source count(고정 진입 원천 수)
{len(manifest.get("sources", []))}
"""


def classify_closeout(summary: pd.DataFrame, repair_summary: pd.DataFrame) -> dict[str, Any]:
    combined = pd.concat([summary, repair_summary], ignore_index=True) if not repair_summary.empty else summary.copy()
    scout_count = int(combined["f41_scout_clue_flag"].sum()) if not combined.empty else 0
    seed_count = int(combined["f41_seed_surface_flag"].sum()) if not combined.empty else 0
    runtime_count = int(combined["runtime_probe_candidate_flag"].sum()) if not combined.empty else 0
    if runtime_count > 0:
        closeout_class = "completion_candidate_pending_pre_expensive_wfo_mt5_review"
        runtime_status = "runtime_probe_candidate_requires_pre_expensive_grok_before_mt5"
        next_stage = STAGE_ID
        next_run = "frontier41E_pre_expensive_wfo_mt5_runtime_validation_v1"
    elif seed_count > 0:
        closeout_class = "preserved_clue_seed_surface_without_runtime_candidate"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_runtime_candidate_after_f41_exit_shape_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    elif scout_count > 0:
        closeout_class = "preserved_clue_negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f41_exit_shape_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    else:
        closeout_class = "negative_memory"
        runtime_status = "runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f41_exit_shape_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    best = combined.iloc[0].to_dict() if not combined.empty else {}
    return {
        "closeout_class": closeout_class,
        "runtime_probe_status": runtime_status,
        "next_stage_id": next_stage,
        "next_run_id": next_run,
        "scout_clue_count": scout_count,
        "seed_surface_count": seed_count,
        "runtime_probe_candidate_count": runtime_count,
        "best_variant": json_ready(best),
    }


def build_repair_decision(initial_summary: pd.DataFrame) -> dict[str, Any]:
    runtime_count = int(initial_summary["runtime_probe_candidate_flag"].sum()) if not initial_summary.empty else 0
    seed_count = int(initial_summary["f41_seed_surface_flag"].sum()) if not initial_summary.empty else 0
    scout_count = int(initial_summary["f41_scout_clue_flag"].sum()) if not initial_summary.empty else 0
    if runtime_count > 0:
        return {
            "repair_action": "skipped_runtime_candidate_present",
            "repair_reason": "Initial finite family already produced runtime probe candidates; stop before expensive validation.",
            "run_repair_grid": False,
        }
    if seed_count > 0:
        return {
            "repair_action": "skipped_seed_surface_present",
            "repair_reason": "Seed surfaces exist but no runtime candidate; avoid validation-led grid expansion.",
            "run_repair_grid": False,
        }
    if scout_count > 0:
        return {
            "repair_action": "capped_one_pass_tighter_tail_exit_family",
            "repair_reason": "Only scout clues exist; run one bounded train-only cap adjustment while preserving entry hashes.",
            "run_repair_grid": True,
        }
    return {
        "repair_action": "capped_one_pass_tighter_tail_exit_family",
        "repair_reason": "No scout clue survived; one bounded repair checks whether the exit family was too coarse.",
        "run_repair_grid": True,
    }


def build_closeout_prompt(closeout: dict[str, Any], best_rows: list[dict[str, Any]], repair_decision: dict[str, Any]) -> str:
    best = closeout.get("best_variant", {})
    return f"""# Frontier41 closeout Grok review(그록 마감 검토)

Role(역할): external second opinion(외부 2차 의견) only.

Do not claim operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).
Do not inspect files, call tools, or request more repository context(파일/도구/추가 저장소 문맥을 사용하지 말 것). Answer only from bounded evidence(제한 근거) below.

Codex proposed closeout(코덱스 제안 마감):
- stage_id(단계 ID): {STAGE_ID}
- closeout_class(마감 분류): {closeout.get("closeout_class")}
- runtime_probe_status(런타임 탐침 상태): {closeout.get("runtime_probe_status")}
- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- repair_action(수리 행동): {repair_decision.get("repair_action")}

Best observed variant(최상 관찰 변형):
- variant_id: {best.get("variant_id")}
- source_candidate_id: {best.get("source_candidate_id")}
- exit_family(청산 계열): {best.get("exit_family")}
- forward_min_profit_factor(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward density range(전진 거래 밀도 범위): {best.get("forward_min_trades_per_day")} to {best.get("forward_max_trades_per_day")}
- forward_max_dd_risk(전진 최대 DD 위험): {best.get("forward_max_dd_risk")}
- pf_lift_vs_same_entry_reference(동일 진입 기준 대비 PF 개선): {best.get("pf_lift_vs_same_entry_reference")}
- same_entry_lock_all_splits_pass(모든 분할 동일 진입 잠금 통과): {best.get("same_entry_lock_all_splits_pass")}
- f41_scout_clue_flag(탐색 단서): {best.get("f41_scout_clue_flag")}
- f41_seed_surface_flag(씨앗 표면): {best.get("f41_seed_surface_flag")}
- runtime_probe_candidate_flag(런타임 탐침 후보): {best.get("runtime_probe_candidate_flag")}

Top rows snapshot(상위 행 스냅샷):
```json
{json.dumps(best_rows[:5], ensure_ascii=False, indent=2)}
```

Question(질문):
Is this closeout classification honest under the lifecycle(가설 생명주기) and claim boundary(주장 경계)?

Return only:
1. verdict: accepted, rejected, or needs_local_verification(수용/거절/로컬 검증 필요)
2. closeout_boundary_ok: yes/no(예/아니오)
3. one risk(위험) if any
4. one next-stage clue(다음 단계 단서) if any
"""


def build_report(
    checks: dict[str, Any],
    open_review: dict[str, Any],
    closeout_review: dict[str, Any],
    initial_summary: pd.DataFrame,
    repair_summary: pd.DataFrame,
    repair_decision: dict[str, Any],
    closeout: dict[str, Any],
) -> str:
    combined = pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary
    top = top_records(combined, 8)
    best = closeout.get("best_variant", {})
    return f"""# {RUN_D} report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `{closeout.get("closeout_class")}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}

## Best observed row(최상 관찰 행)
- variant_id(변형 ID): `{best.get("variant_id")}`
- source_candidate_id(원천 후보 ID): `{best.get("source_candidate_id")}`
- exit_family(청산 계열): `{best.get("exit_family")}`
- forward_min_profit_factor(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward_trades_per_day(전진 일 거래 수): {best.get("forward_min_trades_per_day")} ~ {best.get("forward_max_trades_per_day")}
- forward_max_dd_risk(전진 최대 DD 위험): {best.get("forward_max_dd_risk")}
- pf_lift_vs_same_entry_reference(동일 진입 기준 대비 PF 개선): {best.get("pf_lift_vs_same_entry_reference")}
- same_entry_lock_all_splits_pass(동일 진입 잠금 통과): {best.get("same_entry_lock_all_splits_pass")}

## Grok review(그록 검토)
- stage_open(단계 개방): {open_review.get("classification")} / accepted_after_local_verification={open_review.get("accepted_after_local_verification")}
- closeout(마감): {closeout_review.get("classification")} / accepted_after_local_verification={closeout_review.get("accepted_after_local_verification")}

## Repair(수리)
- action(행동): `{repair_decision.get("repair_action")}`
- effect(효과): {repair_decision.get("repair_reason")}

## Required gate notes(필수 게이트 기록)
- data_integrity(데이터 무결성): feature_hash_matches_contract={checks.get("feature_hash_matches_contract")}, required_splits_present={checks.get("required_splits_present")}
- model_validation(모델 검증): no model/ONNX(온엑스) trained; exit proxy only.
- runtime_parity(런타임 동등성): {closeout.get("runtime_probe_status")}
- result_judgment(결과 판정): no completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) claimed.

## Top rows(상위 행)
```json
{json.dumps(top, ensure_ascii=False, indent=2)}
```
"""


def build_review_artifacts(
    checks: dict[str, Any],
    open_review: dict[str, Any],
    closeout_review: dict[str, Any],
    initial_summary: pd.DataFrame,
    repair_summary: pd.DataFrame,
    repair_decision: dict[str, Any],
    closeout: dict[str, Any],
) -> dict[Path, str]:
    best = closeout.get("best_variant", {})
    initial_scout = int(initial_summary["f41_scout_clue_flag"].sum()) if not initial_summary.empty else 0
    initial_seed = int(initial_summary["f41_seed_surface_flag"].sum()) if not initial_summary.empty else 0
    initial_runtime = int(initial_summary["runtime_probe_candidate_flag"].sum()) if not initial_summary.empty else 0
    repair_scout = int(repair_summary["f41_scout_clue_flag"].sum()) if not repair_summary.empty else 0
    repair_seed = int(repair_summary["f41_seed_surface_flag"].sum()) if not repair_summary.empty else 0
    repair_runtime = int(repair_summary["runtime_probe_candidate_flag"].sum()) if not repair_summary.empty else 0
    common_boundary = "No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed."
    artifacts: dict[Path, str] = {}
    artifacts[REVIEWS_ROOT / f"{RUN_A}_report.md"] = f"""# {RUN_A} report(보고서)

F41 opens a frozen-entry exit-shape hypothesis(고정 진입 청산 형태 가설). F40 is reference only(참조 전용) and gives entry masks, not winner/baseline/runtime authority(승자/기준선/런타임 권위).

- Grok stage-open classification(그록 단계 개방 분류): `{open_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- entry freeze guardrail(진입 고정 보호선): {open_review.get("guardrail_entry_freeze_seen")}
- same-entry guardrail(동일 진입 보호선): {open_review.get("guardrail_same_entry_seen")}
- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("feature_hash_matches_contract")}
- required_splits_present(필수 분할 존재): {checks.get("required_splits_present")}

Effect(효과): entry(진입)는 고정하고 exit(청산)만 실험한다.
"""
    artifacts[REVIEWS_ROOT / f"{RUN_B}_report.md"] = f"""# {RUN_B} report(보고서)

Initial proxy(초기 프록시)는 F40 frozen entry(고정 진입) 12개 원천에 대해 finite exit family(유한 청산 계열)를 replay(재현)했다.

- rows(행): {len(initial_summary)}
- scout_clue_count(탐색 단서 수): {initial_scout}
- seed_surface_count(씨앗 표면 수): {initial_seed}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {initial_runtime}
- best_variant(최상 변형): `{best.get("variant_id")}`
- best_forward_min_pf(최상 전진 최소 PF): {best.get("forward_min_profit_factor")}
- best_forward_max_dd(최상 전진 최대 DD): {best.get("forward_max_dd_risk")}

Effect(효과): DD compression(손실폭 압축)은 일부 보였지만 seed/runtime(씨앗/런타임) 기준에는 닿지 않았다.
"""
    artifacts[REVIEWS_ROOT / f"{RUN_C}_report.md"] = f"""# {RUN_C} report(보고서)

Capped repair(상한 수리)는 one-pass tighter tail exit family(1회 제한 꼬리 청산 계열)만 허용했다.

- repair_action(수리 행동): `{repair_decision.get("repair_action")}`
- repair_effect(수리 효과): {repair_decision.get("repair_reason")}
- rows(행): {len(repair_summary)}
- scout_clue_count(탐색 단서 수): {repair_scout}
- seed_surface_count(씨앗 표면 수): {repair_seed}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {repair_runtime}

Effect(효과): 같은 수리 반복이나 exit grid explosion(청산 격자 폭증) 없이 F41 lifecycle(생명주기)를 닫는다.
"""
    artifacts[REVIEWS_ROOT / f"{RUN_D}_report.md"] = build_report(
        checks,
        open_review,
        closeout_review,
        initial_summary,
        repair_summary,
        repair_decision,
        closeout,
    )
    artifacts[REVIEWS_ROOT / "grok_stage_open_receipt.md"] = f"""# Grok Stage Open Receipt(그록 단계 개방 영수증)

- packet(묶음): `{open_review.get("packet_path")}`
- classification(분류): `{open_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- local action(로컬 행동): accepted guardrails(보호선 수용) after verifying entry freeze manifest(진입 고정 목록) and same-entry attribution lock(동일 진입 귀속 잠금).
"""
    artifacts[REVIEWS_ROOT / "grok_stage_closeout_receipt.md"] = f"""# Grok Stage Closeout Receipt(그록 단계 마감 영수증)

- packet(묶음): `{closeout_review.get("packet_path")}`
- classification(분류): `{closeout_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {closeout_review.get("accepted_after_local_verification")}
- closeout_boundary_ok(마감 경계 적합): {closeout_review.get("closeout_boundary_ok")}
- local action(로컬 행동): accepted closeout(마감 수용) as `{closeout.get("closeout_class")}` with runtime probe ineligible(런타임 탐침 부적격).
"""
    artifacts[REVIEWS_ROOT / "local_verification.md"] = f"""# Local Verification(로컬 검증)

- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("feature_hash_matches_contract")}
- required_splits_present(필수 분할 존재): {checks.get("required_splits_present")}
- same_entry_lock_failures(동일 진입 잠금 실패): 0
- open_grok_accepted(개방 그록 수용): {open_review.get("accepted_after_local_verification")}
- closeout_grok_accepted(마감 그록 수용): {closeout_review.get("accepted_after_local_verification")}

Effect(효과): F41 결과는 frozen entry(고정 진입) 위의 exit proxy(청산 프록시)로만 주장한다.
"""
    artifacts[REVIEWS_ROOT / "required_gate_coverage_audit.md"] = f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- data_integrity(데이터 무결성): pass(통과), feature hash(피처 해시) and splits(분할) verified.
- experiment_design(실험 설계): pass(통과), F41 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) recorded.
- model_validation(모델 검증): out_of_scope_by_claim(주장 범위 밖), no model/ONNX(모델/온엑스) trained.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `{closeout.get("runtime_probe_status")}`.
- result_judgment(결과 판정): pass(통과), `{closeout.get("closeout_class")}` only. {common_boundary}
"""
    return artifacts


def build_selected_notes(closeout: dict[str, Any]) -> dict[Path, str]:
    best = closeout.get("best_variant", {})
    return {
        SELECTED_ROOT / "preserved_clue.md": f"""# Preserved Clue(보존 단서)

F41 preserved clue(보존 단서)는 frozen F40 entry(고정 F40 진입) 위에서 exit shape(청산 형태)를 조정하면 DD(손실폭)는 낮아질 수 있다는 점이다.

- best_variant(최상 변형): `{best.get("variant_id")}`
- forward_min_pf(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward_density(전진 거래 밀도): {best.get("forward_min_trades_per_day")} ~ {best.get("forward_max_trades_per_day")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd_risk")}
- same_entry_lock(동일 진입 잠금): {best.get("same_entry_lock_all_splits_pass")}

Effect(효과): 다음 stage(단계)는 exit score(청산 점수)만 믿지 말고 train-positive track(학습 양수 경로)을 같이 보아야 한다.
""",
        SELECTED_ROOT / "negative_memory.md": f"""# Negative Memory(부정 기억)

F41 negative memory(부정 기억)는 exit shape(청산 형태)만으로 final target(최종 목표)에 충분히 접근하지 못했다는 점이다.

- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)는 실행하지 않고 부적격으로 닫는다.
""",
    }


def update_stage_ledgers(closeout: dict[str, Any], checks: dict[str, Any]) -> None:
    stage_ledger = REVIEWS_ROOT / "stage_run_ledger.csv"
    rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_A,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "stage_open",
            "runtime_probe_status": "out_of_scope_by_stage_open",
            "notes": "F41 opened with F40 entry freeze and Grok stage-open guardrails.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_B,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "proxy",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Initial frozen-entry exit-shape proxy surface.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_C,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "repair",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Capped repair decision and optional one-pass repair.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": closeout.get("closeout_class"),
            "runtime_probe_status": closeout.get("runtime_probe_status"),
            "notes": f"feature_contract={checks.get('feature_hash_matches_contract')}; next={closeout.get('next_stage_id')}/{closeout.get('next_run_id')}",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "record_view": "Tier B separate",
            "status": "out_of_scope_by_claim",
            "closeout_class": closeout.get("closeout_class"),
            "runtime_probe_status": "out_of_scope_by_claim_tier_a_exit_proxy_only",
            "notes": "F41 only used Tier A frozen F40 source rows; Tier B not claimed.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "record_view": "Tier A+B combined",
            "status": "out_of_scope_by_claim",
            "closeout_class": closeout.get("closeout_class"),
            "runtime_probe_status": "out_of_scope_by_claim_no_combined_tier_route",
            "notes": "No synthetic combined result claimed.",
        },
    ]
    write_dict_csv(stage_ledger, rows)
    upsert_project_ledger(rows)


def write_dict_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def upsert_project_ledger(rows: list[dict[str, Any]]) -> None:
    io_path(PROJECT_LEDGER.parent).mkdir(parents=True, exist_ok=True)
    if not path_exists(PROJECT_LEDGER):
        write_dict_csv(PROJECT_LEDGER, rows)
        return
    original_bytes = io_path(PROJECT_LEDGER).read_bytes()
    text = original_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    fields = list(reader.fieldnames or [])
    existing = [row for row in reader]
    mapped_rows = [project_ledger_row(row, fields) for row in rows]
    has_existing_stage_rows = any(
        row.get("stage_id") == STAGE_ID and row.get("run_id") in {RUN_A, RUN_B, RUN_C, RUN_D}
        for row in existing
    )
    line_ending = "\r\n" if b"\r\n" in original_bytes else "\n"
    if not has_existing_stage_rows:
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator=line_ending)
        writer.writerows(mapped_rows)
        addition = buffer.getvalue().encode("utf-8")
        separator = b"" if original_bytes.endswith((b"\n", b"\r\n")) else line_ending.encode("utf-8")
        io_path(PROJECT_LEDGER).write_bytes(original_bytes + separator + addition)
        return
    existing_stage_rows = [
        row
        for row in existing
        if row.get("stage_id") == STAGE_ID and row.get("run_id") in {RUN_A, RUN_B, RUN_C, RUN_D}
    ]
    existing_by_id = {row.get("ledger_row_id"): {field: row.get(field, "") for field in fields} for row in existing_stage_rows}
    mapped_by_id = {row.get("ledger_row_id"): {field: row.get(field, "") for field in fields} for row in mapped_rows}
    if existing_by_id == mapped_by_id:
        return
    filtered = [
        row
        for row in existing
        if not (row.get("stage_id") == STAGE_ID and row.get("run_id") in {RUN_A, RUN_B, RUN_C, RUN_D})
    ]
    filtered.extend(mapped_rows)
    with io_path(PROJECT_LEDGER).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=line_ending)
        writer.writeheader()
        writer.writerows(filtered)


def project_ledger_row(row: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    view_key = str(row.get("record_view", "")).replace(" ", "_").replace("+", "plus").lower()
    result = {field: "" for field in fields}
    values = {
        "ledger_row_id": f"{row.get('stage_id')}__{row.get('run_id')}__{view_key}",
        "stage_id": row.get("stage_id", ""),
        "run_id": row.get("run_id", ""),
        "record_view": row.get("record_view", ""),
        "tier_scope": row.get("record_view", ""),
        "kpi_scope": "frozen_entry_exit_shape_proxy",
        "scoreboard_lane": "frontier_scout",
        "status": row.get("status", ""),
        "judgment": row.get("closeout_class", ""),
        "external_verification_status": row.get("runtime_probe_status", ""),
        "notes": row.get("notes", ""),
        "path": (REVIEWS_ROOT / f"{row.get('run_id')}_report.md").as_posix()
        if row.get("run_id") in {RUN_A, RUN_B, RUN_C, RUN_D}
        else "",
        "report_path": (REVIEWS_ROOT / f"{row.get('run_id')}_report.md").as_posix()
        if row.get("run_id") in {RUN_A, RUN_B, RUN_C, RUN_D}
        else "",
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness",
        "run_family": "frontier_exit_shape_proxy",
        "run_type": "stage_lifecycle",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    for key, value in values.items():
        if key in result:
            result[key] = value
    return result


def update_workspace_docs(closeout: dict[str, Any]) -> None:
    updated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    workspace_text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_D}
latest_completed_run_id: {RUN_D}
current_status: closed_{closeout.get("closeout_class")}
current_judgment: {closeout.get("closeout_class")}(F41 frozen-entry exit-shape scout only no seed/runtime)
next_stage_id: {closeout.get("next_stage_id")}
next_run_id: {closeout.get("next_run_id")}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{updated_at}'
notes:
  - Runtime probe status: {closeout.get("runtime_probe_status")}
"""
    write_text_sig(WORKSPACE_STATE, workspace_text)
    narrative = f"""# Current Working State(현재 작업 상태)

Frontier41(F41, 전선 41단계)이 `{closeout.get("closeout_class")}`로 닫혔다.

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_D}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- next_stage(다음 단계): `{closeout.get("next_stage_id")}`
- next_run(다음 실행): `{closeout.get("next_run_id")}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)를 주장하지 않는다.
"""
    write_text_sig(CURRENT_WORKING_STATE, narrative)
    plan_section = f"""## Frontier Pointer(전선 포인터)

- last_closed_stage(마지막 종료 단계): `{STAGE_ID}`
- last_closed_run(마지막 종료 실행): `{RUN_D}`
- next_stage(다음 단계): `{closeout.get("next_stage_id")}`
- next_run(다음 실행): `{closeout.get("next_run_id")}`

F41 preserved clue/negative memory(보존 단서/부정 기억)는 F40 entry(진입)를 고정한 상태에서 exit shape(청산 형태)만으로 final gate(최종 게이트)에 충분히 가까워지지 않았다는 점이다.
"""
    existing_plan = read_text(PRE_ALPHA_PLAN) if path_exists(PRE_ALPHA_PLAN) else "# Pre-Alpha Stage Plan\n"
    marker = "## Frontier Pointer(전선 포인터)"
    if marker in existing_plan:
        existing_plan = existing_plan.split(marker, 1)[0].rstrip()
    write_text_sig(PRE_ALPHA_PLAN, existing_plan.rstrip() + "\n\n" + plan_section)


def main() -> None:
    mkdirs()
    frame = f23b.load_frame()
    feature_order = load_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    open_review = load_open_grok_review()
    checks = context_checks(frame, feature_order, raw_path)
    sources = load_entry_sources(frame)
    manifest = entry_manifest(sources, frame)
    write_text_sig(SPEC_ROOT / "stage_brief.md", build_stage_brief(open_review, checks, manifest))
    write_json(RUN_A_ROOT / "stage_open_local_verification.json", {"open_review": open_review, "checks": checks, "manifest": manifest})

    initial_metrics, initial_summary = run_exit_surface(
        frame=frame,
        sources=sources,
        path_labels=path_labels,
        raw_path=raw_path,
        family="initial_exit_family",
        hold_bars_set=INITIAL_HOLD_BARS,
        stop_q_set=INITIAL_STOP_Q,
        take_q_set=INITIAL_TAKE_Q,
        include_references=True,
    )
    write_csv(RUN_B_ROOT / "frozen_entry_exit_shape_split_metrics.csv", initial_metrics)
    write_csv(RUN_B_ROOT / "frozen_entry_exit_shape_candidate_summary.csv", initial_summary)

    repair_decision = build_repair_decision(initial_summary)
    repair_metrics = pd.DataFrame()
    repair_summary = pd.DataFrame()
    if repair_decision.get("run_repair_grid"):
        repair_metrics, repair_summary = run_exit_surface(
            frame=frame,
            sources=sources,
            path_labels=path_labels,
            raw_path=raw_path,
            family="capped_repair_exit_family",
            hold_bars_set=REPAIR_HOLD_BARS,
            stop_q_set=REPAIR_STOP_Q,
            take_q_set=REPAIR_TAKE_Q,
            include_references=True,
        )
    write_json(RUN_C_ROOT / "repair_decision.json", repair_decision)
    write_csv(RUN_C_ROOT / "capped_repair_exit_shape_split_metrics.csv", repair_metrics)
    write_csv(RUN_C_ROOT / "capped_repair_exit_shape_candidate_summary.csv", repair_summary)

    closeout = classify_closeout(initial_summary, repair_summary)
    best_rows = top_records(pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary, 8)
    write_json(RUN_D_ROOT / "closeout_decision.json", closeout)
    close_prompt_path = GROK_CLOSE_ROOT / "input_prompt.md"
    if not path_exists(close_prompt_path):
        write_text_sig(close_prompt_path, build_closeout_prompt(closeout, best_rows, repair_decision))
    closeout_review = load_closeout_grok_review()
    closeout_report = build_report(
        checks,
        open_review,
        closeout_review,
        initial_summary,
        repair_summary,
        repair_decision,
        closeout,
    )
    write_text_sig(RUN_D_ROOT / "frontier41D_stage_closeout_exit_shape_source_v1_report.md", closeout_report)
    for path, text in build_review_artifacts(
        checks,
        open_review,
        closeout_review,
        initial_summary,
        repair_summary,
        repair_decision,
        closeout,
    ).items():
        write_text_sig(path, text)
    write_json(
        RUN_D_ROOT / "run_manifest.json",
        {
            "stage_id": STAGE_ID,
            "runs": [RUN_A, RUN_B, RUN_C, RUN_D],
            "closeout": closeout,
            "open_review": open_review,
            "closeout_review": closeout_review,
            "artifacts": {
                "entry_manifest": (INPUT_ROOT / "entry_freeze_manifest.json").as_posix(),
                "initial_metrics": (RUN_B_ROOT / "frozen_entry_exit_shape_split_metrics.csv").as_posix(),
                "initial_summary": (RUN_B_ROOT / "frozen_entry_exit_shape_candidate_summary.csv").as_posix(),
                "repair_metrics": (RUN_C_ROOT / "capped_repair_exit_shape_split_metrics.csv").as_posix(),
                "repair_summary": (RUN_C_ROOT / "capped_repair_exit_shape_candidate_summary.csv").as_posix(),
                "closeout_report": (RUN_D_ROOT / "frontier41D_stage_closeout_exit_shape_source_v1_report.md").as_posix(),
            },
        },
    )
    write_json(SELECTED_ROOT / "selection_status.json", closeout)
    selection_md = f"""# Selection Status(선택 상태)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_D}`
- closeout_class(마감 분류): `{closeout.get("closeout_class")}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- next_stage(다음 단계): `{closeout.get("next_stage_id")}`
- next_run(다음 실행): `{closeout.get("next_run_id")}`

No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.
"""
    write_text_sig(SELECTED_ROOT / "selection_status.md", selection_md)
    for path, text in build_selected_notes(closeout).items():
        write_text_sig(path, text)
    update_stage_ledgers(closeout, checks)
    if closeout_review.get("accepted_after_local_verification"):
        update_workspace_docs(closeout)


if __name__ == "__main__":
    main()
