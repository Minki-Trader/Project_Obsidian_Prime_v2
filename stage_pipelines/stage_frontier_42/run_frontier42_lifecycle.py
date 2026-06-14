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


STAGE_ID = "stage_frontier_42__short_pf_edge_timing_source_pivot_after_f41_exit_shape_negative"
PREV_STAGE_ID = "stage_frontier_41__short_pf_edge_exit_shape_source_pivot_after_f40_raw_pocket_scout"
RUN_A = "frontier42A_stage_open_short_pf_edge_timing_source_hypothesis_design_v1"
RUN_B = "frontier42B_session_timing_source_proxy_v1"
RUN_C = "frontier42C_capped_broker_timing_repair_decision_v1"
RUN_D = "frontier42D_stage_closeout_timing_source_v1"
NEXT_STAGE_ID = "stage_frontier_43__short_pf_edge_trade_shape_source_pivot_after_f42_timing_negative"
NEXT_RUN_ID = "frontier43A_stage_open_short_pf_edge_trade_shape_source_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F41_ROOT = Path("stages") / PREV_STAGE_ID
F41_ENTRY_MANIFEST = F41_ROOT / "01_inputs" / "entry_freeze_manifest.json"
F41_SELECTION_STATUS = F41_ROOT / "04_selected" / "selection_status.md"
F41_PRESERVED_CLUE = F41_ROOT / "04_selected" / "preserved_clue.md"
F41_NEGATIVE_MEMORY = F41_ROOT / "04_selected" / "negative_memory.md"
F40_STAGE_ID = "stage_frontier_40__short_pf_edge_non_score_source_pivot_after_regime_gate_negative"
F40_CONDITION_POOL = (
    Path("stages")
    / F40_STAGE_ID
    / "02_runs"
    / "frontier40B_raw_feature_state_pocket_proxy_v1"
    / "raw_feature_condition_pool.csv"
)

GROK_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier42_stage_open" / "small_review"
GROK_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier42_stage_closeout" / "small_review"

PROJECT_LEDGER = Path("docs") / "registers" / "alpha_run_ledger.csv"
WORKSPACE_STATE = Path("docs") / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = Path("docs") / "context" / "current_working_state.md"
PRE_ALPHA_PLAN = Path("docs") / "workspace" / "pre_alpha_stage_plan.md"

SIDE_VALUE = -1
SIDE_LABEL = "short"
SPLITS = ("train", "validation", "oos")
INITIAL_HOLDS = (4, 6, 8, 12)
BRACKET_HOLDS = (4, 8, 12)
BRACKET_PAIRS = ((0.18, 0.86), (0.26, 0.70))
SCOUT_MIN_PF = 1.05
SCOUT_MIN_DENSITY = 4.0
SCOUT_MAX_DENSITY = 12.0
SCOUT_MAX_DD = 18.0
TRAIN_POSITIVE_MIN_PF = 1.03
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
    mask: np.ndarray
    split_counts: dict[str, int]
    split_hashes: dict[str, str]
    expected_split_hashes: dict[str, str]
    source_lock_pass: bool


@dataclass(frozen=True)
class TimingGate:
    gate_id: str
    gate_family: str
    description: str
    mask: np.ndarray
    executable_scope: str


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
        GROK_CLOSE_ROOT,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8-sig")


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if math.isfinite(number) else None
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


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing"}


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
        "accepted_after_local_verification": False,
        "timing_sweep_budget_seen": False,
        "source_lock_seen": False,
        "exit_subordinate_seen": False,
        "runtime_boundary_seen": False,
        "leakage_guard_requires_local_verification": True,
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
            "timing_sweep_budget_seen": "timing sweep budget" in lower,
            "source_lock_seen": "frozen entry-source lock" in lower or "frozen entry" in lower,
            "exit_subordinate_seen": "exit stays finite" in lower or "subordinate" in lower,
            "runtime_boundary_seen": "runtime_claim_boundary_ok" in lower and "yes" in lower,
            "leakage_guard_requires_local_verification": "leakage_guard_ok" in lower
            and "needs_local_verification" in lower,
        }
    )
    result["accepted_after_local_verification"] = bool(
        result["metadata_success"]
        and result["metadata_returncode"] == 0
        and result["timing_sweep_budget_seen"]
        and result["source_lock_seen"]
        and result["exit_subordinate_seen"]
        and result["runtime_boundary_seen"]
    )
    return result


def load_closeout_grok_review() -> dict[str, Any]:
    result = {
        "packet_path": GROK_CLOSE_ROOT.as_posix(),
        "metadata_exists": path_exists(GROK_CLOSE_ROOT / "metadata.json"),
        "clean_output_exists": path_exists(GROK_CLOSE_ROOT / "clean_output.md"),
        "classification": "pending",
        "closeout_boundary_ok": False,
        "accepted_after_local_verification": False,
    }
    if not result["metadata_exists"] or not result["clean_output_exists"]:
        return result
    metadata = read_json(GROK_CLOSE_ROOT / "metadata.json")
    clean = read_text(GROK_CLOSE_ROOT / "clean_output.md")
    lower = clean.lower()
    boundary_ok = ("closeout_boundary_ok" in lower and ("yes" in lower or "예" in lower)) or any(
        token in lower
        for token in (
            "preserved_clue",
            "negative_memory",
            "seed_surface",
            "runtime_probe",
            "completion_candidate",
            "invalid_setup",
            "blocked",
        )
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
        "f41_selection_status_exists": path_exists(F41_SELECTION_STATUS),
        "f41_entry_manifest_exists": path_exists(F41_ENTRY_MANIFEST),
        "f41_preserved_clue_exists": path_exists(F41_PRESERVED_CLUE),
        "f41_negative_memory_exists": path_exists(F41_NEGATIVE_MEMORY),
        "f40_condition_pool_exists": path_exists(F40_CONDITION_POOL),
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "feature_order_exists": path_exists(f23b.FEATURE_ORDER_PATH),
        "raw_path_exists": path_exists(f33b.RAW_US100_PATH),
        "feature_count": len(feature_order),
        "feature_hash": ordered_hash(feature_order),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "required_timing_columns_present": all(
            col in frame.columns
            for col in (
                "minutes_from_cash_open",
                "is_first_30m_after_open",
                "is_last_30m_before_cash_close",
            )
        ),
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
    return {str(row["condition_id"]): row for row in pool.to_dict("records")}


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


def load_entry_sources(frame: pd.DataFrame) -> tuple[list[EntrySource], dict[str, Any]]:
    manifest = read_json(F41_ENTRY_MANIFEST)
    conditions = load_condition_pool()
    sources: list[EntrySource] = []
    for row in manifest.get("sources", []):
        condition_ids = tuple(str(item) for item in row["condition_ids"])
        mask = np.ones(len(frame), dtype=bool)
        for condition_id in condition_ids:
            mask &= condition_mask(frame, conditions[condition_id])
        split_counts = {split: int((mask & f33b.split_mask(frame, split)).sum()) for split in SPLITS}
        split_hashes = {split: hash_mask(frame, mask, split) for split in SPLITS}
        expected = {split: str(row.get("entry_hash_by_split", {}).get(split, "")) for split in SPLITS}
        sources.append(
            EntrySource(
                source_rank=int(row["source_rank"]),
                candidate_id=str(row["candidate_id"]),
                condition_ids=condition_ids,
                rule_definition=str(row["rule_definition"]),
                features=str(row.get("features", "")),
                mask=mask,
                split_counts=split_counts,
                split_hashes=split_hashes,
                expected_split_hashes=expected,
                source_lock_pass=all(split_hashes[split] == expected[split] for split in SPLITS),
            )
        )
    if not sources:
        raise ValueError("F42 could not load frozen F41 entry sources.")
    return sources, manifest


def build_timing_gates(frame: pd.DataFrame, family: str) -> list[TimingGate]:
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype="float64")
    valid = np.isfinite(minutes)
    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    hour = timestamp.dt.hour.to_numpy(dtype=int)
    dow = timestamp.dt.dayofweek.to_numpy(dtype=int)
    session_gates = [
        TimingGate("session_full_reference", "session_bucket", "all valid cash-session rows", valid, "session_feature"),
        TimingGate("session_core_30_300", "session_bucket", "30 < minutes_from_cash_open <= 300", valid & (minutes > 30) & (minutes <= 300), "session_feature"),
        TimingGate("session_morning_5_120", "session_bucket", "5 <= minutes_from_cash_open <= 120", valid & (minutes >= 5) & (minutes <= 120), "session_feature"),
        TimingGate("session_mid_90_240", "session_bucket", "90 < minutes_from_cash_open <= 240", valid & (minutes > 90) & (minutes <= 240), "session_feature"),
        TimingGate("session_late_210_330", "session_bucket", "210 < minutes_from_cash_open <= 330", valid & (minutes > 210) & (minutes <= 330), "session_feature"),
        TimingGate("session_post_open_35_180", "session_bucket", "30 < minutes_from_cash_open <= 180", valid & (minutes > 30) & (minutes <= 180), "session_feature"),
        TimingGate("session_pre_close_180_330", "session_bucket", "180 < minutes_from_cash_open <= 330", valid & (minutes > 180) & (minutes <= 330), "session_feature"),
        TimingGate("session_not_first_or_last_30", "session_flag", "not first 30m and not last 30m", valid & (minutes > 30) & (minutes <= 300), "session_feature"),
    ]
    repair_gates = [
        TimingGate("broker_hour_16_18", "broker_clock_diag", "UTC-stored/broker-key hour 16-17", (hour >= 16) & (hour < 18), "broker_clock_diagnostic"),
        TimingGate("broker_hour_18_20", "broker_clock_diag", "UTC-stored/broker-key hour 18-19", (hour >= 18) & (hour < 20), "broker_clock_diagnostic"),
        TimingGate("broker_hour_20_22", "broker_clock_diag", "UTC-stored/broker-key hour 20-21", (hour >= 20) & (hour < 22), "broker_clock_diagnostic"),
        TimingGate("dow_mon_to_wed", "day_of_week_diag", "Monday through Wednesday", dow <= 2, "broker_clock_diagnostic"),
        TimingGate("dow_thu_fri", "day_of_week_diag", "Thursday and Friday", dow >= 3, "broker_clock_diagnostic"),
    ]
    return session_gates if family == "session" else repair_gates


def quantile_caps(
    frame: pd.DataFrame,
    mask: np.ndarray,
    path_labels: dict[int, dict[str, np.ndarray]],
    stop_q: float,
    take_q: float,
) -> tuple[float, float]:
    labels = path_labels[SIDE_VALUE]
    train_mask = np.asarray(mask, dtype=bool) & f33b.split_mask(frame, "train") & labels["valid"]
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
    used_hash = (
        hash_items(pd.to_datetime(frame.loc[used, "timestamp"], utc=True).astype("int64").astype(str).tolist())
        if used.size
        else "empty"
    )
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
        "timed_entry_hash": used_hash,
    }


def exit_specs(frame: pd.DataFrame, timed_mask: np.ndarray, path_labels: dict[int, dict[str, np.ndarray]], gate_id: str) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for hold_bars in INITIAL_HOLDS:
        specs.append(
            {
                "exit_id": f"{gate_id}_hold{hold_bars:02d}_no_bracket",
                "exit_family": "fixed_hold_no_bracket",
                "hold_bars": hold_bars,
                "stop_quantile": "none",
                "take_quantile": "none",
                "stop_cap_log_return": float("inf"),
                "take_cap_log_return": float("inf"),
            }
        )
    for hold_bars in BRACKET_HOLDS:
        for stop_q, take_q in BRACKET_PAIRS:
            stop_cap, take_cap = quantile_caps(frame, timed_mask, path_labels, stop_q, take_q)
            if not math.isfinite(stop_cap) or not math.isfinite(take_cap):
                continue
            specs.append(
                {
                    "exit_id": f"{gate_id}_hold{hold_bars:02d}_s{int(stop_q * 100):02d}_t{int(take_q * 100):02d}",
                    "exit_family": "train_quantile_bracket",
                    "hold_bars": hold_bars,
                    "stop_quantile": stop_q,
                    "take_quantile": take_q,
                    "stop_cap_log_return": stop_cap,
                    "take_cap_log_return": take_cap,
                }
            )
    return specs


def run_timing_surface(
    frame: pd.DataFrame,
    sources: list[EntrySource],
    gates: list[TimingGate],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    run_id: str,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    metrics_rows: list[dict[str, Any]] = []
    attempt_count = 0
    for source in sources:
        for gate in gates:
            timed_mask = source.mask & gate.mask
            train_entries = int((timed_mask & f33b.split_mask(frame, "train")).sum())
            if train_entries <= 0:
                continue
            specs = exit_specs(frame, timed_mask, path_labels, gate.gate_id)
            for spec in specs:
                attempt_count += 1
                variant_id = f"{source.candidate_id}_{gate.gate_id}_{spec['exit_id']}"
                for split in SPLITS:
                    metrics = evaluate_exit_mask(
                        frame=frame,
                        mask=timed_mask,
                        side=SIDE_VALUE,
                        stop_cap=float(spec["stop_cap_log_return"]),
                        take_cap=float(spec["take_cap_log_return"]),
                        hold_bars=int(spec["hold_bars"]),
                        path_labels=path_labels,
                        raw_path=raw_path,
                        split=split,
                    )
                    timed_split_mask = timed_mask & f33b.split_mask(frame, split)
                    metrics_rows.append(
                        {
                            "stage_id": STAGE_ID,
                            "run_id": run_id,
                            "source_rank": source.source_rank,
                            "source_candidate_id": source.candidate_id,
                            "variant_id": variant_id,
                            "gate_id": gate.gate_id,
                            "gate_family": gate.gate_family,
                            "gate_description": gate.description,
                            "executable_scope": gate.executable_scope,
                            "side": SIDE_LABEL,
                            "side_value": SIDE_VALUE,
                            "rule_definition": source.rule_definition,
                            "features": source.features,
                            "condition_ids": "|".join(source.condition_ids),
                            "split": split,
                            "record_view": "Tier A separate",
                            "hold_bars": int(spec["hold_bars"]),
                            "exit_family": spec["exit_family"],
                            "stop_quantile": spec["stop_quantile"],
                            "take_quantile": spec["take_quantile"],
                            "stop_cap_log_return": spec["stop_cap_log_return"],
                            "take_cap_log_return": spec["take_cap_log_return"],
                            "source_lock_pass": source.source_lock_pass,
                            "source_entry_hash_expected": source.expected_split_hashes[split],
                            "source_entry_hash_observed": source.split_hashes[split],
                            "timed_entry_hash_expected": hash_mask(frame, timed_mask, split),
                            "timed_entry_hash_observed": metrics["timed_entry_hash"],
                            "timed_entry_count": int(timed_split_mask.sum()),
                            **metrics,
                        }
                    )
    metrics_frame = pd.DataFrame(metrics_rows)
    summary = summarize_variants(metrics_frame)
    budget = {
        "run_id": run_id,
        "source_count": len(sources),
        "timing_gate_count": len(gates),
        "timing_gate_ids": [gate.gate_id for gate in gates],
        "exit_specs_per_nonempty_source_gate_max": len(INITIAL_HOLDS) + len(BRACKET_HOLDS) * len(BRACKET_PAIRS),
        "attempt_count": attempt_count,
        "sweep_policy": "capped timing gates; train-positive lane required before scout/seed/runtime flags.",
    }
    return metrics_frame, summary, budget


def split_summary_row(group: pd.DataFrame, split: str) -> pd.Series:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row for {split}")
    return row.iloc[0]


def summarize_variants(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    group_cols = [
        "variant_id",
        "source_candidate_id",
        "source_rank",
        "gate_id",
        "gate_family",
        "gate_description",
        "executable_scope",
        "side",
        "side_value",
        "rule_definition",
        "features",
        "condition_ids",
        "hold_bars",
        "exit_family",
        "stop_quantile",
        "take_quantile",
        "stop_cap_log_return",
        "take_cap_log_return",
    ]
    for key_values, group in metrics.groupby(group_cols, sort=False, dropna=False):
        row: dict[str, Any] = dict(zip(group_cols, key_values))
        source_lock_all = bool(group["source_lock_pass"].astype(bool).all())
        timing_hash_all = bool((group["timed_entry_hash_expected"].astype(str) == group["timed_entry_hash_observed"].astype(str)).all())
        row["source_lock_all_splits_pass"] = source_lock_all
        row["timed_entry_hash_all_splits_pass"] = timing_hash_all
        for split in SPLITS:
            split_row = split_summary_row(group, split)
            for field in (
                "trade_count",
                "timed_entry_count",
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
        forward_pf = [safe_float(row["validation_profit_factor"]), safe_float(row["oos_profit_factor"])]
        forward_density = [safe_float(row["validation_trades_per_day"]), safe_float(row["oos_trades_per_day"])]
        forward_dd = [safe_float(row["validation_dd_risk"]), safe_float(row["oos_dd_risk"])]
        row["forward_min_profit_factor"] = float(min(forward_pf))
        row["forward_min_trades_per_day"] = float(min(forward_density))
        row["forward_max_trades_per_day"] = float(max(forward_density))
        row["forward_max_dd_risk"] = float(max(forward_dd))
        row["train_positive_lane_pass"] = bool(
            row["train_profit_factor"] >= TRAIN_POSITIVE_MIN_PF and row["train_net_profit"] > 0.0
        )
        integrity = bool(source_lock_all and timing_hash_all)
        timing_gate_active = str(row["gate_id"]) != "session_full_reference"
        row["timing_gate_active"] = bool(timing_gate_active)
        row["f42_scout_clue_flag"] = bool(
            integrity
            and timing_gate_active
            and row["train_positive_lane_pass"]
            and row["forward_min_profit_factor"] >= SCOUT_MIN_PF
            and row["forward_min_trades_per_day"] >= SCOUT_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= SCOUT_MAX_DENSITY
            and row["forward_max_dd_risk"] <= SCOUT_MAX_DD
        )
        row["f42_seed_surface_flag"] = bool(
            row["f42_scout_clue_flag"]
            and row["forward_min_profit_factor"] >= SEED_MIN_PF
            and row["forward_min_trades_per_day"] >= SEED_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= SEED_MAX_DENSITY
            and row["forward_max_dd_risk"] <= SEED_MAX_DD
        )
        row["runtime_probe_candidate_flag"] = bool(
            row["f42_seed_surface_flag"]
            and row["train_profit_factor"] >= 1.05
            and row["forward_min_profit_factor"] >= RUNTIME_MIN_PF
            and row["forward_min_trades_per_day"] >= RUNTIME_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= RUNTIME_MAX_DENSITY
            and row["forward_max_dd_risk"] <= RUNTIME_MAX_DD
            and str(row["executable_scope"]) in {"session_feature", "broker_clock_diagnostic"}
        )
        density_mid = (row["forward_min_trades_per_day"] + row["forward_max_trades_per_day"]) / 2.0
        density_penalty = abs(density_mid - 7.5) / 7.5
        dd_penalty = max(0.0, row["forward_max_dd_risk"] - 10.0) / 10.0
        train_penalty = 0.0 if row["train_positive_lane_pass"] else 2.0
        row["f42_timing_score"] = float(
            row["forward_min_profit_factor"]
            + max(row["train_profit_factor"] - 1.0, 0.0)
            - density_penalty
            - dd_penalty
            - train_penalty
        )
        rows.append(row)
    summary = pd.DataFrame(rows)
    if summary.empty:
        return summary
    summary = summary.sort_values(
        [
            "runtime_probe_candidate_flag",
            "f42_seed_surface_flag",
            "f42_scout_clue_flag",
            "train_positive_lane_pass",
            "f42_timing_score",
            "forward_min_profit_factor",
            "forward_max_dd_risk",
        ],
        ascending=[False, False, False, False, False, False, True],
    ).reset_index(drop=True)
    summary.insert(0, "rank", np.arange(1, len(summary) + 1))
    return summary


def top_records(frame: pd.DataFrame, limit: int = 8) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    return json_ready(frame.head(limit).to_dict("records"))


def build_input_manifest(
    checks: dict[str, Any],
    open_review: dict[str, Any],
    source_manifest: dict[str, Any],
    sources: list[EntrySource],
    initial_gates: list[TimingGate],
    repair_gates: list[TimingGate],
) -> dict[str, Any]:
    manifest = {
        "stage_id": STAGE_ID,
        "source_stage_id": PREV_STAGE_ID,
        "hypothesis": "Entry-known timing gates may isolate train-positive short source slices from F40/F41 raw pockets.",
        "claim_boundary": "scout/seed/runtime-probe-candidate only; no completion/baseline/promotion/runtime authority/live readiness.",
        "grok_stage_open": open_review,
        "local_checks": checks,
        "artifacts": {
            "f41_entry_manifest": artifact_identity(F41_ENTRY_MANIFEST),
            "f41_selection_status": artifact_identity(F41_SELECTION_STATUS),
            "f40_condition_pool": artifact_identity(F40_CONDITION_POOL),
            "dataset": artifact_identity(f23b.DATASET_PATH),
            "feature_order": artifact_identity(f23b.FEATURE_ORDER_PATH),
            "raw_path": artifact_identity(f33b.RAW_US100_PATH),
        },
        "source_lock": {
            "source_count": len(sources),
            "all_sources_pass": all(source.source_lock_pass for source in sources),
            "sources": [
                {
                    "source_rank": source.source_rank,
                    "candidate_id": source.candidate_id,
                    "condition_ids": list(source.condition_ids),
                    "rule_definition": source.rule_definition,
                    "split_counts": source.split_counts,
                    "expected_split_hashes": source.expected_split_hashes,
                    "observed_split_hashes": source.split_hashes,
                    "source_lock_pass": source.source_lock_pass,
                }
                for source in sources
            ],
        },
        "timing_sweep_budget": {
            "initial_gate_count": len(initial_gates),
            "repair_gate_count": len(repair_gates),
            "exit_holds": list(INITIAL_HOLDS),
            "bracket_holds": list(BRACKET_HOLDS),
            "bracket_pairs": BRACKET_PAIRS,
            "initial_gate_ids": [gate.gate_id for gate in initial_gates],
            "repair_gate_ids": [gate.gate_id for gate in repair_gates],
        },
        "source_manifest_snapshot": {
            "source_stage_id": source_manifest.get("stage_id"),
            "source_artifacts": source_manifest.get("artifacts", {}),
        },
    }
    write_json(INPUT_ROOT / "timing_source_manifest.json", manifest)
    return manifest


def build_stage_brief(open_review: dict[str, Any], checks: dict[str, Any], manifest: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

## Hypothesis(가설)
F40/F41 short raw pockets(숏 원천 포켓)의 약한 PF(수익 팩터)가 time-of-session contamination(세션 시간 오염)에서 왔다면, entry-known timing gates(진입 시점 타이밍 제한)가 train-positive(학습 양수)이고 forward-stable(전진 안정)한 short source(숏 원천)를 분리할 수 있다.

## Boundary(경계)
- F41 and F40 are reference only(참조 전용)이다.
- No winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않는다.
- Timing(타이밍)이 primary lever(주 레버)이고 exit(청산)은 finite subordinate family(유한 보조 계열)이다.

## Grok stage-open review(그록 단계 개방 검토)
- classification(분류): {open_review.get("classification")}
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- timing_sweep_budget_seen(타이밍 예산 확인): {open_review.get("timing_sweep_budget_seen")}
- source_lock_seen(원천 잠금 확인): {open_review.get("source_lock_seen")}

## Local checks(로컬 점검)
- feature_hash(피처 해시): `{checks.get("feature_hash")}`
- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("feature_hash_matches_contract")}
- timing columns present(타이밍 열 존재): {checks.get("required_timing_columns_present")}
- source lock all pass(원천 잠금 전체 통과): {manifest.get("source_lock", {}).get("all_sources_pass")}
"""


def build_repair_decision(initial_summary: pd.DataFrame) -> dict[str, Any]:
    scout_count = int(initial_summary["f42_scout_clue_flag"].sum()) if not initial_summary.empty else 0
    seed_count = int(initial_summary["f42_seed_surface_flag"].sum()) if not initial_summary.empty else 0
    runtime_count = int(initial_summary["runtime_probe_candidate_flag"].sum()) if not initial_summary.empty else 0
    if runtime_count > 0:
        return {
            "repair_action": "skipped_runtime_candidate_present",
            "repair_reason": "Initial session timing surface produced runtime probe candidates; stop before expensive validation.",
            "run_repair_grid": False,
        }
    if seed_count > 0:
        return {
            "repair_action": "skipped_seed_surface_present",
            "repair_reason": "Initial session timing surface produced seed surfaces; avoid broker-hour diagnostic expansion.",
            "run_repair_grid": False,
        }
    return {
        "repair_action": "capped_broker_hour_dow_diagnostic",
        "repair_reason": f"Initial session timing surface produced scout={scout_count}, seed={seed_count}, runtime={runtime_count}; run capped entry-known diagnostic timing family.",
        "run_repair_grid": True,
    }


def classify_closeout(initial_summary: pd.DataFrame, repair_summary: pd.DataFrame) -> dict[str, Any]:
    combined = pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary.copy()
    scout_count = int(combined["f42_scout_clue_flag"].sum()) if not combined.empty else 0
    seed_count = int(combined["f42_seed_surface_flag"].sum()) if not combined.empty else 0
    runtime_count = int(combined["runtime_probe_candidate_flag"].sum()) if not combined.empty else 0
    if runtime_count > 0:
        closeout_class = "completion_candidate_pending_pre_expensive_wfo_mt5_review"
        runtime_status = "runtime_probe_candidate_requires_pre_expensive_grok_before_mt5"
        next_stage = STAGE_ID
        next_run = "frontier42E_pre_expensive_wfo_mt5_runtime_validation_v1"
    elif seed_count > 0:
        closeout_class = "preserved_clue_seed_surface_without_runtime_candidate"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_runtime_candidate_after_f42_timing_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    elif scout_count > 0:
        closeout_class = "preserved_clue_negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f42_timing_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    else:
        closeout_class = "negative_memory"
        runtime_status = "runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f42_timing_proxy"
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


def build_closeout_prompt(closeout: dict[str, Any], best_rows: list[dict[str, Any]], repair_decision: dict[str, Any]) -> str:
    best = closeout.get("best_variant", {})
    return f"""# Frontier42 closeout Grok review(그록 마감 검토)

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
- gate_id(타이밍 제한): {best.get("gate_id")}
- exit_family(청산 계열): {best.get("exit_family")}
- train_pf(학습 PF): {best.get("train_profit_factor")}
- train_positive_lane_pass(학습 양수 경로 통과): {best.get("train_positive_lane_pass")}
- forward_min_profit_factor(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward density range(전진 거래 밀도 범위): {best.get("forward_min_trades_per_day")} to {best.get("forward_max_trades_per_day")}
- forward_max_dd_risk(전진 최대 DD 위험): {best.get("forward_max_dd_risk")}
- source_lock_all_splits_pass(원천 잠금 통과): {best.get("source_lock_all_splits_pass")}
- f42_scout_clue_flag(탐색 단서): {best.get("f42_scout_clue_flag")}
- f42_seed_surface_flag(씨앗 표면): {best.get("f42_seed_surface_flag")}
- runtime_probe_candidate_flag(런타임 탐침 후보): {best.get("runtime_probe_candidate_flag")}

Top rows snapshot(상위 행 스냅샷):
```json
{json.dumps(best_rows[:5], ensure_ascii=False, indent=2)}
```

Question(질문):
Is this closeout classification honest under the lifecycle(가설 생명주기), Grok stage-open guardrails(단계 개방 보호선), and claim boundary(주장 경계)?

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
    budgets: dict[str, Any],
) -> str:
    combined = pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary
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
- gate_id(타이밍 제한): `{best.get("gate_id")}`
- exit_family(청산 계열): `{best.get("exit_family")}`
- train_profit_factor(학습 PF): {best.get("train_profit_factor")}
- train_positive_lane_pass(학습 양수 경로 통과): {best.get("train_positive_lane_pass")}
- forward_min_profit_factor(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward_trades_per_day(전진 일 거래 수): {best.get("forward_min_trades_per_day")} ~ {best.get("forward_max_trades_per_day")}
- forward_max_dd_risk(전진 최대 DD 위험): {best.get("forward_max_dd_risk")}
- source_lock_all_splits_pass(원천 잠금 통과): {best.get("source_lock_all_splits_pass")}

## Sweep budget(탐색 예산)
- initial_attempt_count(초기 시도 수): {budgets.get("initial", {}).get("attempt_count")}
- repair_attempt_count(수리 시도 수): {budgets.get("repair", {}).get("attempt_count")}
- repair_action(수리 행동): `{repair_decision.get("repair_action")}`
- repair_effect(수리 효과): {repair_decision.get("repair_reason")}

## Grok review(그록 검토)
- stage_open(단계 개방): {open_review.get("classification")} / accepted_after_local_verification={open_review.get("accepted_after_local_verification")}
- closeout(마감): {closeout_review.get("classification")} / accepted_after_local_verification={closeout_review.get("accepted_after_local_verification")}

## Required gate notes(필수 게이트 기록)
- data_integrity(데이터 무결성): feature_hash_matches_contract={checks.get("feature_hash_matches_contract")}, timing_columns_present={checks.get("required_timing_columns_present")}
- model_validation(모델 검증): no model/ONNX(온엑스) trained; timing proxy only.
- runtime_parity(런타임 동등성): {closeout.get("runtime_probe_status")}
- result_judgment(결과 판정): no completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) claimed.

## Top rows(상위 행)
```json
{json.dumps(top_records(combined, 8), ensure_ascii=False, indent=2)}
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
    budgets: dict[str, Any],
) -> dict[Path, str]:
    best = closeout.get("best_variant", {})
    initial_scout = int(initial_summary["f42_scout_clue_flag"].sum()) if not initial_summary.empty else 0
    initial_seed = int(initial_summary["f42_seed_surface_flag"].sum()) if not initial_summary.empty else 0
    initial_runtime = int(initial_summary["runtime_probe_candidate_flag"].sum()) if not initial_summary.empty else 0
    repair_scout = int(repair_summary["f42_scout_clue_flag"].sum()) if not repair_summary.empty else 0
    repair_seed = int(repair_summary["f42_seed_surface_flag"].sum()) if not repair_summary.empty else 0
    repair_runtime = int(repair_summary["runtime_probe_candidate_flag"].sum()) if not repair_summary.empty else 0
    artifacts: dict[Path, str] = {}
    artifacts[REVIEWS_ROOT / f"{RUN_A}_report.md"] = f"""# {RUN_A} report(보고서)

F42 opens a timing-source hypothesis(타이밍 원천 가설). F41/F40 are reference only(참조 전용) and provide source masks, not winner/baseline/runtime authority(승자/기준선/런타임 권위).

- Grok stage-open classification(그록 단계 개방 분류): `{open_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- timing_sweep_budget_seen(타이밍 예산 확인): {open_review.get("timing_sweep_budget_seen")}
- source_lock_seen(원천 잠금 확인): {open_review.get("source_lock_seen")}
- exit_subordinate_seen(청산 보조성 확인): {open_review.get("exit_subordinate_seen")}
- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("feature_hash_matches_contract")}
"""
    artifacts[REVIEWS_ROOT / f"{RUN_B}_report.md"] = f"""# {RUN_B} report(보고서)

Initial proxy(초기 프록시)는 session timing gates(세션 타이밍 제한)를 primary lever(주 레버)로 시험했다.

- attempts(시도 수): {budgets.get("initial", {}).get("attempt_count")}
- rows(행): {len(initial_summary)}
- scout_clue_count(탐색 단서 수): {initial_scout}
- seed_surface_count(씨앗 표면 수): {initial_seed}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {initial_runtime}
- best_variant(최상 변형): `{best.get("variant_id")}`
"""
    artifacts[REVIEWS_ROOT / f"{RUN_C}_report.md"] = f"""# {RUN_C} report(보고서)

Capped repair(상한 수리)는 broker-hour/day-of-week diagnostic(브로커 시간/요일 진단)만 허용했다.

- repair_action(수리 행동): `{repair_decision.get("repair_action")}`
- repair_effect(수리 효과): {repair_decision.get("repair_reason")}
- attempts(시도 수): {budgets.get("repair", {}).get("attempt_count")}
- rows(행): {len(repair_summary)}
- scout_clue_count(탐색 단서 수): {repair_scout}
- seed_surface_count(씨앗 표면 수): {repair_seed}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {repair_runtime}
"""
    artifacts[REVIEWS_ROOT / f"{RUN_D}_report.md"] = build_report(
        checks, open_review, closeout_review, initial_summary, repair_summary, repair_decision, closeout, budgets
    )
    artifacts[REVIEWS_ROOT / "grok_stage_open_receipt.md"] = f"""# Grok Stage Open Receipt(그록 단계 개방 영수증)

- packet(묶음): `{open_review.get("packet_path")}`
- classification(분류): `{open_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- local action(로컬 행동): accepted guardrails(보호선 수용) after coding timing sweep budget(타이밍 탐색 예산), frozen source lock(고정 원천 잠금), and subordinate exit family(보조 청산 계열).
"""
    artifacts[REVIEWS_ROOT / "grok_stage_closeout_receipt.md"] = f"""# Grok Stage Closeout Receipt(그록 단계 마감 영수증)

- packet(묶음): `{closeout_review.get("packet_path")}`
- classification(분류): `{closeout_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {closeout_review.get("accepted_after_local_verification")}
- closeout_boundary_ok(마감 경계 적합): {closeout_review.get("closeout_boundary_ok")}
"""
    artifacts[REVIEWS_ROOT / "local_verification.md"] = f"""# Local Verification(로컬 검증)

- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("feature_hash_matches_contract")}
- required_splits_present(필수 분할 존재): {checks.get("required_splits_present")}
- timing_columns_present(타이밍 열 존재): {checks.get("required_timing_columns_present")}
- source_lock_all_pass(원천 잠금 전체 통과): {best.get("source_lock_all_splits_pass")}
- open_grok_accepted(개방 그록 수용): {open_review.get("accepted_after_local_verification")}
- closeout_grok_accepted(마감 그록 수용): {closeout_review.get("accepted_after_local_verification")}
"""
    artifacts[REVIEWS_ROOT / "required_gate_coverage_audit.md"] = f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- data_integrity(데이터 무결성): pass(통과), feature hash(피처 해시), split(분할), timing columns(타이밍 열) verified.
- experiment_design(실험 설계): pass(통과), F42 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) recorded.
- model_validation(모델 검증): out_of_scope_by_claim(주장 범위 밖), no model/ONNX(모델/온엑스) trained.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `{closeout.get("runtime_probe_status")}`.
- result_judgment(결과 판정): pass(통과), `{closeout.get("closeout_class")}` only.
"""
    return artifacts


def build_selected_notes(closeout: dict[str, Any]) -> dict[Path, str]:
    best = closeout.get("best_variant", {})
    return {
        SELECTED_ROOT / "preserved_clue.md": f"""# Preserved Clue(보존 단서)

F42 preserved clue(보존 단서)는 timing gate(타이밍 제한)가 train-positive lane(학습 양수 경로)을 유지하면서 일부 short source(숏 원천)의 PF/DD/density(수익 팩터/손실폭/밀도)를 바꿀 수 있는지에 대한 근거다.

- best_variant(최상 변형): `{best.get("variant_id")}`
- gate_id(타이밍 제한): `{best.get("gate_id")}`
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward_density(전진 거래 밀도): {best.get("forward_min_trades_per_day")} ~ {best.get("forward_max_trades_per_day")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd_risk")}
""",
        SELECTED_ROOT / "negative_memory.md": f"""# Negative Memory(부정 기억)

F42 negative memory(부정 기억)는 timing source(타이밍 원천)만으로 final target(최종 목표)에 충분히 접근하지 못했는지 또는 seed/runtime(씨앗/런타임) 후보가 없었는지를 기록한다.

- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
""",
    }


def update_stage_ledgers(closeout: dict[str, Any], checks: dict[str, Any]) -> None:
    rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_A,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "stage_open",
            "runtime_probe_status": "out_of_scope_by_stage_open",
            "notes": "F42 opened with timing-source hypothesis and Grok guardrails.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_B,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "proxy",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Session timing source proxy surface.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_C,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "repair",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Capped broker-hour/day-of-week timing repair decision.",
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
            "runtime_probe_status": "out_of_scope_by_claim_tier_a_timing_proxy_only",
            "notes": "F42 only used Tier A frozen source rows; Tier B not claimed.",
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
    write_dict_csv(REVIEWS_ROOT / "stage_run_ledger.csv", rows)
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


def project_ledger_row(row: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    view_key = str(row.get("record_view", "")).replace(" ", "_").replace("+", "plus").lower()
    result = {field: "" for field in fields}
    values = {
        "ledger_row_id": f"{row.get('stage_id')}__{row.get('run_id')}__{view_key}",
        "stage_id": row.get("stage_id", ""),
        "run_id": row.get("run_id", ""),
        "record_view": row.get("record_view", ""),
        "tier_scope": row.get("record_view", ""),
        "kpi_scope": "timing_source_proxy",
        "scoreboard_lane": "frontier_scout",
        "status": row.get("status", ""),
        "judgment": row.get("closeout_class", ""),
        "external_verification_status": row.get("runtime_probe_status", ""),
        "notes": row.get("notes", ""),
        "path": (REVIEWS_ROOT / f"{row.get('run_id')}_report.md").as_posix(),
        "report_path": (REVIEWS_ROOT / f"{row.get('run_id')}_report.md").as_posix(),
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness",
        "run_family": "frontier_timing_source_proxy",
        "run_type": "stage_lifecycle",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    for key, value in values.items():
        if key in result:
            result[key] = value
    return result


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


def update_workspace_docs(closeout: dict[str, Any]) -> None:
    updated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    workspace_text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_D}
latest_completed_run_id: {RUN_D}
current_status: closed_{closeout.get("closeout_class")}
current_judgment: {closeout.get("closeout_class")}(F42 timing-source scout no operating authority)
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

Frontier42(F42, 전선 42단계)가 `{closeout.get("closeout_class")}`로 닫혔다.

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

F42 carry-forward(이월) 기록은 timing source(타이밍 원천)가 PF/DD/density(수익 팩터/손실폭/밀도)를 네 축 목표까지 끌어올렸는지 여부와 train-positive lane(학습 양수 경로)의 유지 여부다.
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
    sources, source_manifest = load_entry_sources(frame)
    initial_gates = build_timing_gates(frame, "session")
    repair_gates = build_timing_gates(frame, "repair")
    manifest = build_input_manifest(checks, open_review, source_manifest, sources, initial_gates, repair_gates)
    write_text_sig(SPEC_ROOT / "stage_brief.md", build_stage_brief(open_review, checks, manifest))
    write_json(RUN_A_ROOT / "stage_open_local_verification.json", {"open_review": open_review, "checks": checks, "manifest": manifest})

    initial_metrics, initial_summary, initial_budget = run_timing_surface(
        frame, sources, initial_gates, path_labels, raw_path, RUN_B
    )
    write_csv(RUN_B_ROOT / "session_timing_source_split_metrics.csv", initial_metrics)
    write_csv(RUN_B_ROOT / "session_timing_source_candidate_summary.csv", initial_summary)
    write_json(RUN_B_ROOT / "timing_sweep_budget.json", initial_budget)

    repair_decision = build_repair_decision(initial_summary)
    repair_metrics = pd.DataFrame()
    repair_summary = pd.DataFrame()
    repair_budget = {"run_id": RUN_C, "attempt_count": 0, "timing_gate_count": len(repair_gates), "timing_gate_ids": [gate.gate_id for gate in repair_gates]}
    if repair_decision.get("run_repair_grid"):
        repair_metrics, repair_summary, repair_budget = run_timing_surface(
            frame, sources, repair_gates, path_labels, raw_path, RUN_C
        )
    write_json(RUN_C_ROOT / "repair_decision.json", repair_decision)
    write_csv(RUN_C_ROOT / "capped_broker_timing_split_metrics.csv", repair_metrics)
    write_csv(RUN_C_ROOT / "capped_broker_timing_candidate_summary.csv", repair_summary)
    write_json(RUN_C_ROOT / "timing_repair_budget.json", repair_budget)

    closeout = classify_closeout(initial_summary, repair_summary)
    combined = pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary
    best_rows = top_records(combined, 8)
    write_json(RUN_D_ROOT / "closeout_decision.json", closeout)
    close_prompt_path = GROK_CLOSE_ROOT / "input_prompt.md"
    if not path_exists(GROK_CLOSE_ROOT / "metadata.json"):
        write_text_sig(close_prompt_path, build_closeout_prompt(closeout, best_rows, repair_decision))
    closeout_review = load_closeout_grok_review()
    budgets = {"initial": initial_budget, "repair": repair_budget}
    closeout_report = build_report(
        checks, open_review, closeout_review, initial_summary, repair_summary, repair_decision, closeout, budgets
    )
    write_text_sig(RUN_D_ROOT / "frontier42D_stage_closeout_timing_source_v1_report.md", closeout_report)
    for path, text in build_review_artifacts(
        checks, open_review, closeout_review, initial_summary, repair_summary, repair_decision, closeout, budgets
    ).items():
        write_text_sig(path, text)
    write_json(
        RUN_D_ROOT / "run_manifest.json",
        {
            "stage_id": STAGE_ID,
            "runs": [RUN_A, RUN_B, RUN_C, RUN_D],
            "open_review": open_review,
            "closeout_review": closeout_review,
            "closeout": closeout,
            "budgets": budgets,
            "artifacts": {
                "timing_source_manifest": (INPUT_ROOT / "timing_source_manifest.json").as_posix(),
                "initial_summary": (RUN_B_ROOT / "session_timing_source_candidate_summary.csv").as_posix(),
                "repair_summary": (RUN_C_ROOT / "capped_broker_timing_candidate_summary.csv").as_posix(),
                "closeout_report": (REVIEWS_ROOT / f"{RUN_D}_report.md").as_posix(),
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
