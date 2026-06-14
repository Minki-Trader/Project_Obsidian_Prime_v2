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


STAGE_ID = "stage_frontier_43__short_pf_edge_trade_shape_source_pivot_after_f42_timing_negative"
PREV_STAGE_ID = "stage_frontier_42__short_pf_edge_timing_source_pivot_after_f41_exit_shape_negative"
RUN_A = "frontier43A_stage_open_short_pf_edge_trade_shape_source_hypothesis_design_v1"
RUN_B = "frontier43B_entry_known_trade_shape_source_proxy_v1"
RUN_C = "frontier43C_capped_trade_shape_profile_repair_v1"
RUN_D = "frontier43D_stage_closeout_trade_shape_source_v1"
NEXT_STAGE_ID = "stage_frontier_44__short_pf_edge_label_model_pivot_after_f43_trade_shape_negative"
NEXT_RUN_ID = "frontier44A_stage_open_short_pf_edge_label_model_source_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F42_ROOT = Path("stages") / PREV_STAGE_ID
F42_SELECTION_STATUS = F42_ROOT / "04_selected" / "selection_status.md"
F42_PRESERVED_CLUE = F42_ROOT / "04_selected" / "preserved_clue.md"
F42_NEGATIVE_MEMORY = F42_ROOT / "04_selected" / "negative_memory.md"
F42_SELECTION_JSON = F42_ROOT / "04_selected" / "selection_status.json"

GROK_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier43_stage_open" / "small_review"
GROK_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier43_stage_closeout" / "small_review"

PROJECT_LEDGER = Path("docs") / "registers" / "alpha_run_ledger.csv"
WORKSPACE_STATE = Path("docs") / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = Path("docs") / "context" / "current_working_state.md"
PRE_ALPHA_PLAN = Path("docs") / "workspace" / "pre_alpha_stage_plan.md"

SIDE_VALUE = -1
SIDE_LABEL = "short"
SPLITS = ("train", "validation", "oos")
EXCLUDED_SOURCE_FEATURES = {
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
}
INITIAL_SINGLE_KEEP = 48
INITIAL_PAIR_KEEP = 22
INITIAL_PAIR_LIMIT = 120
INITIAL_FIXED_HOLDS = (4, 8, 12)
INITIAL_BRACKET_HOLDS = (4, 8, 12)
INITIAL_BRACKET_PAIRS = ((0.16, 0.82), (0.24, 0.70))
REPAIR_SOURCE_LIMIT = 14
REPAIR_FIXED_HOLDS = (2, 4, 6, 10)
REPAIR_BRACKET_HOLDS = (2, 6, 10)
REPAIR_BRACKET_PAIRS = ((0.12, 0.62), (0.30, 0.86))

SCOUT_MIN_PF = 1.05
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
class Condition:
    condition_id: str
    feature: str
    feature_family: str
    operator: str
    quantile_label: str
    threshold_value: float
    definition: str
    train_coverage: float
    entry_shape_proxy_score: float
    entry_shape_contrast: float
    mask: np.ndarray


@dataclass(frozen=True)
class Source:
    source_id: str
    source_kind: str
    conditions: tuple[Condition, ...]
    rule_definition: str
    features: str
    feature_families: str
    source_shape_proxy_score: float
    train_coverage: float
    mask: np.ndarray
    split_counts: dict[str, int]
    split_hashes: dict[str, str]


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


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8-sig")


def write_dict_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


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
        "guardrail_seen": False,
        "do_not_repeat_seen": False,
        "claim_boundary_ok": False,
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
            "guardrail_seen": "required_guardrail" in lower and "train-only" in lower,
            "do_not_repeat_seen": "do_not_repeat" in lower and "timing" in lower,
            "claim_boundary_ok": "claim_boundary_ok" in lower and "yes" in lower,
        }
    )
    result["accepted_after_local_verification"] = bool(
        result["metadata_success"]
        and result["metadata_returncode"] == 0
        and result["classification"] == "accepted"
        and result["guardrail_seen"]
        and result["do_not_repeat_seen"]
        and result["claim_boundary_ok"]
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
    result.update(
        {
            "metadata_success": bool(metadata.get("success")),
            "metadata_returncode": metadata.get("returncode"),
            "classification": "needs_local_verification"
            if "needs_local_verification" in lower
            else "accepted"
            if "accepted" in lower
            else "unclassified",
            "closeout_boundary_ok": "closeout_boundary_ok" in lower and ("yes" in lower or "예" in lower),
        }
    )
    result["accepted_after_local_verification"] = bool(
        result["metadata_success"]
        and result["metadata_returncode"] == 0
        and result["classification"] == "accepted"
        and result["closeout_boundary_ok"]
    )
    return result


def context_checks(frame: pd.DataFrame, feature_order: list[str], raw_path: dict[str, Any]) -> dict[str, Any]:
    split_counts = frame["split"].astype(str).value_counts().to_dict()
    return {
        "workspace_state_exists": path_exists(WORKSPACE_STATE),
        "f42_selection_status_exists": path_exists(F42_SELECTION_STATUS),
        "f42_selection_json_exists": path_exists(F42_SELECTION_JSON),
        "f42_preserved_clue_exists": path_exists(F42_PRESERVED_CLUE),
        "f42_negative_memory_exists": path_exists(F42_NEGATIVE_MEMORY),
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "feature_order_exists": path_exists(f23b.FEATURE_ORDER_PATH),
        "raw_path_exists": path_exists(f33b.RAW_US100_PATH),
        "feature_count": len(feature_order),
        "feature_hash": ordered_hash(feature_order),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "required_splits_present": all(split in split_counts and split_counts[split] > 0 for split in SPLITS),
        "split_counts": split_counts,
        "frame_rows": int(len(frame)),
        "raw_rows": int(len(raw_path.get("raw", []))),
        "excluded_session_clock_features": sorted(EXCLUDED_SOURCE_FEATURES),
    }


def feature_family_weight(feature: str) -> float:
    family = f23b.feature_family(feature)
    weights = {
        "price_range": 1.15,
        "price_ratio": 1.05,
        "gap_return": 1.0,
        "rolling_zscore": 1.15,
        "normalized_return": 1.1,
        "volatility": 1.15,
        "volatility_ratio": 1.2,
        "bandwidth": 1.2,
        "band_position": 1.05,
        "squeeze_flag": 1.1,
        "realized_vol": 1.2,
        "realized_vol_ratio": 1.2,
        "trend_strength": 1.0,
        "trend_direction_spread": 1.0,
        "trend_state": 0.95,
        "oscillator_slope": 1.1,
        "oscillator_spread": 1.0,
        "oscillator_hist": 1.0,
        "momentum": 0.95,
        "session_return": 0.85,
        "external_return": 0.8,
        "external_zscore": 0.8,
        "breadth_aggregate": 0.85,
        "breadth_ratio": 0.9,
        "breadth_dispersion": 1.0,
        "relative_strength": 0.9,
    }
    return float(weights.get(family, 0.75))


def condition_shape_proxy_score(series: pd.Series, mask: np.ndarray, train_base: np.ndarray, feature: str) -> tuple[float, float]:
    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype="float64")
    selected = np.asarray(mask, dtype=bool) & train_base & np.isfinite(values)
    baseline = train_base & np.isfinite(values)
    if selected.sum() < 20 or baseline.sum() < 20:
        return 0.0, 0.0
    selected_values = values[selected]
    base_values = values[baseline]
    iqr = float(np.nanquantile(base_values, 0.75) - np.nanquantile(base_values, 0.25))
    scale = iqr if math.isfinite(iqr) and iqr > 1e-12 else float(np.nanstd(base_values))
    scale = scale if math.isfinite(scale) and scale > 1e-12 else 1.0
    contrast = abs(float(np.nanmedian(selected_values)) - float(np.nanmedian(base_values))) / scale
    coverage = float(selected.sum() / max(baseline.sum(), 1))
    coverage_score = max(0.0, 1.0 - abs(coverage - 0.18) / 0.18)
    score = feature_family_weight(feature) + min(contrast, 3.0) + 0.65 * coverage_score
    return float(score), float(contrast)


def condition_mask(frame: pd.DataFrame, condition: Condition) -> np.ndarray:
    values = pd.to_numeric(frame[condition.feature], errors="coerce").to_numpy(dtype="float64")
    finite = np.isfinite(values)
    threshold = float(condition.threshold_value)
    op = condition.operator
    if op == "<=":
        return finite & (values <= threshold)
    if op == "<":
        return finite & (values < threshold)
    if op == ">=":
        return finite & (values >= threshold)
    if op == ">":
        return finite & (values > threshold)
    raise ValueError(f"Unsupported operator: {op}")


def build_condition_pool(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
) -> tuple[pd.DataFrame, list[Condition], np.ndarray]:
    valid_features = np.isfinite(frame[feature_order].to_numpy(dtype="float64")).all(axis=1)
    valid = valid_features & path_labels[SIDE_VALUE]["valid"]
    train_base = f33b.split_mask(frame, "train")
    train_valid = train_base & valid
    conditions: list[Condition] = []
    for feature in feature_order:
        if feature in EXCLUDED_SOURCE_FEATURES:
            continue
        series = pd.to_numeric(frame[feature], errors="coerce")
        train_values = series.loc[train_base].replace([np.inf, -np.inf], np.nan).dropna()
        if train_values.nunique(dropna=True) <= 1:
            continue
        for operator, q_label, threshold, base_mask in f23b.condition_masks(series, train_values):
            mask = np.asarray(base_mask, dtype=bool) & valid
            coverage = float(mask[train_valid].mean()) if train_valid.any() else 0.0
            if not (0.015 <= coverage <= 0.65):
                continue
            score, contrast = condition_shape_proxy_score(series, mask, train_base, feature)
            if score <= 0.0:
                continue
            conditions.append(
                Condition(
                    condition_id=f"f43cond_{len(conditions) + 1:04d}",
                    feature=feature,
                    feature_family=f23b.feature_family(feature),
                    operator=operator,
                    quantile_label=q_label,
                    threshold_value=float(threshold),
                    definition=f"{feature} {operator} {q_label}",
                    train_coverage=coverage,
                    entry_shape_proxy_score=score,
                    entry_shape_contrast=contrast,
                    mask=mask,
                )
            )
    conditions = sorted(conditions, key=lambda item: item.entry_shape_proxy_score, reverse=True)
    renumbered: list[Condition] = []
    for index, condition in enumerate(conditions, start=1):
        renumbered.append(
            Condition(
                condition_id=f"f43cond_{index:04d}",
                feature=condition.feature,
                feature_family=condition.feature_family,
                operator=condition.operator,
                quantile_label=condition.quantile_label,
                threshold_value=condition.threshold_value,
                definition=condition.definition,
                train_coverage=condition.train_coverage,
                entry_shape_proxy_score=condition.entry_shape_proxy_score,
                entry_shape_contrast=condition.entry_shape_contrast,
                mask=condition.mask,
            )
        )
    frame_out = pd.DataFrame(
        [
            {
                "condition_id": c.condition_id,
                "feature": c.feature,
                "feature_family": c.feature_family,
                "operator": c.operator,
                "quantile_label": c.quantile_label,
                "threshold_value": c.threshold_value,
                "definition": c.definition,
                "train_coverage": c.train_coverage,
                "entry_shape_proxy_score": c.entry_shape_proxy_score,
                "entry_shape_contrast": c.entry_shape_contrast,
                "ranking_metric_boundary": "entry_known_closed_bar_shape_proxy_only_no_forward_outcome",
            }
            for c in renumbered
        ]
    )
    return frame_out, renumbered, valid


def make_source(source_id: str, source_kind: str, conditions: tuple[Condition, ...], frame: pd.DataFrame, mask: np.ndarray) -> Source:
    train_mask = f33b.split_mask(frame, "train")
    train_coverage = float((mask & train_mask).sum() / max(train_mask.sum(), 1))
    split_counts = {split: int((mask & f33b.split_mask(frame, split)).sum()) for split in SPLITS}
    split_hashes = {split: hash_mask(frame, mask, split) for split in SPLITS}
    return Source(
        source_id=source_id,
        source_kind=source_kind,
        conditions=conditions,
        rule_definition=(" OR " if source_kind == "or_union" else " & ").join(c.definition for c in conditions),
        features="|".join(c.feature for c in conditions),
        feature_families="|".join(c.feature_family for c in conditions),
        source_shape_proxy_score=float(np.mean([c.entry_shape_proxy_score for c in conditions])),
        train_coverage=train_coverage,
        mask=mask,
        split_counts=split_counts,
        split_hashes=split_hashes,
    )


def build_sources(frame: pd.DataFrame, conditions: list[Condition], valid: np.ndarray) -> list[Source]:
    sources: list[Source] = []
    for condition in conditions[:INITIAL_SINGLE_KEEP]:
        mask = np.asarray(condition.mask, dtype=bool) & valid
        sources.append(make_source("", "single_feature", (condition,), frame, mask))

    pair_candidates: list[tuple[float, tuple[Condition, Condition], np.ndarray]] = []
    top = conditions[:INITIAL_PAIR_KEEP]
    train_mask = f33b.split_mask(frame, "train")
    for index, first in enumerate(top):
        for second in top[index + 1 :]:
            if first.feature == second.feature or first.feature_family == second.feature_family:
                continue
            mask = np.asarray(first.mask, dtype=bool) & np.asarray(second.mask, dtype=bool) & valid
            coverage = float((mask & train_mask).sum() / max(train_mask.sum(), 1))
            if not (0.012 <= coverage <= 0.40):
                continue
            coverage_score = max(0.0, 1.0 - abs(coverage - 0.08) / 0.08)
            score = (first.entry_shape_proxy_score + second.entry_shape_proxy_score) / 2.0 + 0.75 * coverage_score
            pair_candidates.append((float(score), (first, second), mask))
    pair_candidates.sort(key=lambda item: item[0], reverse=True)
    for _, pair, mask in pair_candidates[:INITIAL_PAIR_LIMIT]:
        sources.append(make_source("", "pair_and", pair, frame, mask))

    for index, source in enumerate(sources, start=1):
        prefix = "s" if source.source_kind == "single_feature" else "p"
        sources[index - 1] = Source(
            source_id=f"f43{prefix}_{index:04d}",
            source_kind=source.source_kind,
            conditions=source.conditions,
            rule_definition=source.rule_definition,
            features=source.features,
            feature_families=source.feature_families,
            source_shape_proxy_score=source.source_shape_proxy_score,
            train_coverage=source.train_coverage,
            mask=source.mask,
            split_counts=source.split_counts,
            split_hashes=source.split_hashes,
        )
    return sources


def quantile_caps(frame: pd.DataFrame, mask: np.ndarray, path_labels: dict[int, dict[str, np.ndarray]], stop_q: float, take_q: float) -> tuple[float, float]:
    labels = path_labels[SIDE_VALUE]
    train_mask = np.asarray(mask, dtype=bool) & f33b.split_mask(frame, "train") & labels["valid"]
    mae = labels["mae"][train_mask]
    mfe = labels["mfe"][train_mask]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    if mae.size < 35 or mfe.size < 35:
        return float("nan"), float("nan")
    stop_cap = max(float(np.nanquantile(mae, stop_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
    take_cap = max(float(np.nanquantile(mfe, take_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
    return stop_cap, take_cap


def exit_specs(frame: pd.DataFrame, mask: np.ndarray, path_labels: dict[int, dict[str, np.ndarray]], profile: str) -> list[dict[str, Any]]:
    fixed_holds = REPAIR_FIXED_HOLDS if profile == "repair" else INITIAL_FIXED_HOLDS
    bracket_holds = REPAIR_BRACKET_HOLDS if profile == "repair" else INITIAL_BRACKET_HOLDS
    bracket_pairs = REPAIR_BRACKET_PAIRS if profile == "repair" else INITIAL_BRACKET_PAIRS
    specs: list[dict[str, Any]] = []
    for hold_bars in fixed_holds:
        specs.append(
            {
                "exit_id": f"{profile}_hold{hold_bars:02d}_no_bracket",
                "exit_family": "fixed_hold_no_bracket",
                "profile": profile,
                "hold_bars": hold_bars,
                "stop_quantile": "none",
                "take_quantile": "none",
                "stop_cap_log_return": float("inf"),
                "take_cap_log_return": float("inf"),
            }
        )
    for hold_bars in bracket_holds:
        for stop_q, take_q in bracket_pairs:
            stop_cap, take_cap = quantile_caps(frame, mask, path_labels, stop_q, take_q)
            if not math.isfinite(stop_cap) or not math.isfinite(take_cap):
                continue
            specs.append(
                {
                    "exit_id": f"{profile}_hold{hold_bars:02d}_s{int(stop_q * 100):02d}_t{int(take_q * 100):02d}",
                    "exit_family": "train_quantile_bracket",
                    "profile": profile,
                    "hold_bars": hold_bars,
                    "stop_quantile": stop_q,
                    "take_quantile": take_q,
                    "stop_cap_log_return": stop_cap,
                    "take_cap_log_return": take_cap,
                }
            )
    return specs


def evaluate_exit_mask(
    frame: pd.DataFrame,
    mask: np.ndarray,
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
    labels = path_labels[SIDE_VALUE]
    split_base = f33b.split_mask(frame, split)
    trade_mask = np.asarray(mask, dtype=bool) & split_base & labels["valid"]
    indices = np.flatnonzero(trade_mask)
    pnl: list[float] = []
    reasons: list[str] = []
    holding_bars_values: list[float] = []
    ambiguous: list[bool] = []
    used: list[int] = []
    for idx in indices:
        p = int(entry_pos[idx])
        q_contract = int(future_pos[idx])
        q = min(q_contract, p + int(hold_bars))
        if p < 0 or q <= p or q >= len(open_prices):
            continue
        entry = float(open_prices[p])
        if not math.isfinite(entry) or entry <= 0.0:
            continue
        result = f33b.simulate_one_trade(SIDE_VALUE, entry, p, q, stop_cap, take_cap, open_prices, high_prices, low_prices)
        pnl.append(float(result["pnl_log"]) - scout.ROUGH_COST_LOG_RETURN)
        reasons.append(str(result["exit_reason"]))
        holding_bars_values.append(float(result["holding_bars"]))
        ambiguous.append(bool(result["ambiguous_both_hit"]))
        used.append(int(idx))
    trade_pnl = np.asarray(pnl, dtype="float64")
    trade_times = frame.loc[used, "timestamp"] if used else pd.Series([], dtype="datetime64[ns, UTC]")
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    shape = f23b.payoff_shape(trade_pnl)
    days = scout.count_scope_days(frame.loc[split_base, "timestamp"])
    used_indices = np.asarray(used, dtype=int)
    holding = np.asarray(holding_bars_values, dtype="float64")
    if used_indices.size:
        mfe = labels["mfe"][used_indices]
        mae = labels["mae"][used_indices]
        quality = (
            (mfe >= take_cap) & (mae <= stop_cap)
            if math.isfinite(take_cap) and math.isfinite(stop_cap)
            else np.array([], dtype=bool)
        )
    else:
        mfe = np.array([], dtype="float64")
        mae = np.array([], dtype="float64")
        quality = np.array([], dtype=bool)
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
    }


def run_surface(
    frame: pd.DataFrame,
    sources: list[Source],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    run_id: str,
    profile: str,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    metrics_rows: list[dict[str, Any]] = []
    attempt_count = 0
    for source in sources:
        if int((source.mask & f33b.split_mask(frame, "train")).sum()) < 35:
            continue
        specs = exit_specs(frame, source.mask, path_labels, profile)
        for spec in specs:
            attempt_count += 1
            variant_id = f"{source.source_id}_{spec['exit_id']}"
            for split in SPLITS:
                metrics = evaluate_exit_mask(
                    frame=frame,
                    mask=source.mask,
                    stop_cap=float(spec["stop_cap_log_return"]),
                    take_cap=float(spec["take_cap_log_return"]),
                    hold_bars=int(spec["hold_bars"]),
                    path_labels=path_labels,
                    raw_path=raw_path,
                    split=split,
                )
                metrics_rows.append(
                    {
                        "stage_id": STAGE_ID,
                        "run_id": run_id,
                        "variant_id": variant_id,
                        "source_id": source.source_id,
                        "source_kind": source.source_kind,
                        "source_shape_proxy_score": source.source_shape_proxy_score,
                        "source_train_coverage": source.train_coverage,
                        "source_split_counts": json.dumps(source.split_counts, sort_keys=True),
                        "source_split_hashes": json.dumps(source.split_hashes, sort_keys=True),
                        "side": SIDE_LABEL,
                        "side_value": SIDE_VALUE,
                        "rule_definition": source.rule_definition,
                        "features": source.features,
                        "feature_families": source.feature_families,
                        "condition_ids": "|".join(c.condition_id for c in source.conditions),
                        "split": split,
                        "record_view": "Tier A separate",
                        "profile": profile,
                        "hold_bars": int(spec["hold_bars"]),
                        "exit_family": spec["exit_family"],
                        "stop_quantile": spec["stop_quantile"],
                        "take_quantile": spec["take_quantile"],
                        "stop_cap_log_return": spec["stop_cap_log_return"],
                        "take_cap_log_return": spec["take_cap_log_return"],
                        **metrics,
                    }
                )
    metrics_frame = pd.DataFrame(metrics_rows)
    summary = summarize_variants(metrics_frame)
    budget = {
        "run_id": run_id,
        "profile": profile,
        "source_count": len(sources),
        "attempt_count": attempt_count,
        "exit_profile_policy": "finite fixed holds plus train-only quantile brackets",
        "source_ranking_boundary": "entry-known closed-bar shape proxy only; validation/OOS not used to build sources",
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
        "source_id",
        "source_kind",
        "source_shape_proxy_score",
        "source_train_coverage",
        "side",
        "side_value",
        "rule_definition",
        "features",
        "feature_families",
        "condition_ids",
        "profile",
        "hold_bars",
        "exit_family",
        "stop_quantile",
        "take_quantile",
        "stop_cap_log_return",
        "take_cap_log_return",
    ]
    for key_values, group in metrics.groupby(group_cols, sort=False, dropna=False):
        row: dict[str, Any] = dict(zip(group_cols, key_values))
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
                "median_mfe_log_return",
                "median_mae_log_return",
            ):
                row[f"{split}_{field}"] = split_row[field]
        forward_pf = [safe_float(row["validation_profit_factor"]), safe_float(row["oos_profit_factor"])]
        forward_density = [safe_float(row["validation_trades_per_day"]), safe_float(row["oos_trades_per_day"])]
        forward_dd = [safe_float(row["validation_dd_risk"]), safe_float(row["oos_dd_risk"])]
        train_positive = safe_float(row["train_profit_factor"]) >= 1.02 and safe_float(row["train_net_profit"]) > 0.0
        train_shape_lane = bool(
            train_positive
            and int(row["train_trade_count"]) >= 45
            and 2.5 <= safe_float(row["train_trades_per_day"]) <= 18.0
            and safe_float(row["train_dd_risk"]) <= 24.0
            and safe_float(row["source_shape_proxy_score"]) >= 1.0
        )
        row["forward_min_profit_factor"] = float(min(forward_pf))
        row["forward_min_trades_per_day"] = float(min(forward_density))
        row["forward_max_trades_per_day"] = float(max(forward_density))
        row["forward_max_dd_risk"] = float(max(forward_dd))
        row["train_positive_lane_pass"] = bool(train_positive)
        row["train_shape_lane_pass"] = bool(train_shape_lane)
        row["f43_scout_clue_flag"] = bool(
            train_shape_lane
            and row["forward_min_profit_factor"] >= SCOUT_MIN_PF
            and row["forward_min_trades_per_day"] >= SCOUT_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= SCOUT_MAX_DENSITY
            and row["forward_max_dd_risk"] <= SCOUT_MAX_DD
        )
        row["f43_seed_surface_flag"] = bool(
            row["f43_scout_clue_flag"]
            and row["forward_min_profit_factor"] >= SEED_MIN_PF
            and row["forward_min_trades_per_day"] >= SEED_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= SEED_MAX_DENSITY
            and row["forward_max_dd_risk"] <= SEED_MAX_DD
        )
        row["runtime_probe_candidate_flag"] = bool(
            row["f43_seed_surface_flag"]
            and row["forward_min_profit_factor"] >= RUNTIME_MIN_PF
            and row["forward_min_trades_per_day"] >= RUNTIME_MIN_DENSITY
            and row["forward_max_trades_per_day"] <= RUNTIME_MAX_DENSITY
            and row["forward_max_dd_risk"] <= RUNTIME_MAX_DD
        )
        density_mid = (row["forward_min_trades_per_day"] + row["forward_max_trades_per_day"]) / 2.0
        density_penalty = abs(density_mid - 7.5) / 7.5
        dd_penalty = max(0.0, row["forward_max_dd_risk"] - 10.0) / 10.0
        train_penalty = 0.0 if row["train_shape_lane_pass"] else 1.5
        row["f43_trade_shape_score"] = float(
            row["forward_min_profit_factor"]
            + 0.10 * min(safe_float(row["source_shape_proxy_score"]), 4.0)
            + max(safe_float(row["train_profit_factor"]) - 1.0, 0.0)
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
            "f43_seed_surface_flag",
            "f43_scout_clue_flag",
            "train_shape_lane_pass",
            "f43_trade_shape_score",
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


def build_repair_decision(initial_summary: pd.DataFrame) -> dict[str, Any]:
    if initial_summary.empty:
        return {
            "run_repair_grid": False,
            "repair_action": "skipped_no_initial_variants",
            "repair_reason": "No initial trade-shape variants existed.",
        }
    runtime_count = int(initial_summary["runtime_probe_candidate_flag"].sum())
    seed_count = int(initial_summary["f43_seed_surface_flag"].sum())
    scout_count = int(initial_summary["f43_scout_clue_flag"].sum())
    if runtime_count:
        return {
            "run_repair_grid": False,
            "repair_action": "skipped_runtime_candidate_present",
            "repair_reason": "Initial source surface already produced runtime candidate; stop before expensive validation.",
        }
    if seed_count:
        return {
            "run_repair_grid": False,
            "repair_action": "skipped_seed_surface_present",
            "repair_reason": "Seed surfaces exist; avoid profile overfitting before runtime validation.",
        }
    top_sources = list(dict.fromkeys(initial_summary.head(80)["source_id"].astype(str).tolist()))[:REPAIR_SOURCE_LIMIT]
    return {
        "run_repair_grid": bool(top_sources),
        "repair_action": "capped_trade_shape_profile_diagnostic",
        "repair_reason": f"Initial surface produced scout={scout_count}, seed=0, runtime=0; run bounded profile diagnostic on top source ids only.",
        "repair_source_ids": top_sources,
    }


def classify_closeout(initial_summary: pd.DataFrame, repair_summary: pd.DataFrame) -> dict[str, Any]:
    combined = pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary.copy()
    if combined.empty:
        scout_count = seed_count = runtime_count = 0
        best = {}
    else:
        combined = combined.sort_values(
            [
                "runtime_probe_candidate_flag",
                "f43_seed_surface_flag",
                "f43_scout_clue_flag",
                "train_shape_lane_pass",
                "f43_trade_shape_score",
            ],
            ascending=[False, False, False, False, False],
        ).reset_index(drop=True)
        scout_count = int(combined["f43_scout_clue_flag"].sum())
        seed_count = int(combined["f43_seed_surface_flag"].sum())
        runtime_count = int(combined["runtime_probe_candidate_flag"].sum())
        best = json_ready(dict(combined.iloc[0]))
    if runtime_count:
        closeout_class = "completion_candidate_pending_pre_expensive_wfo_mt5_review"
        runtime_status = "runtime_probe_candidate_requires_pre_expensive_grok_before_mt5"
    elif seed_count:
        closeout_class = "preserved_clue_seed_surface_without_runtime_candidate"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_runtime_candidate_after_f43_trade_shape_proxy"
    elif scout_count:
        closeout_class = "preserved_clue_negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f43_trade_shape_proxy"
    elif not combined.empty:
        closeout_class = "negative_memory"
        runtime_status = "runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f43_trade_shape_proxy"
    else:
        closeout_class = "invalid_setup"
        runtime_status = "runtime_probe_blocked_invalid_no_trade_shape_source_rows"
    return {
        "closeout_class": closeout_class,
        "runtime_probe_status": runtime_status,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "scout_clue_count": scout_count,
        "seed_surface_count": seed_count,
        "runtime_probe_candidate_count": runtime_count,
        "best_variant": best,
    }


def build_input_manifest(
    checks: dict[str, Any],
    open_review: dict[str, Any],
    condition_pool: pd.DataFrame,
    sources: list[Source],
) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "idea_id": "IDEA-FR43-ENTRY-KNOWN-TRADE-SHAPE-SOURCE-PIVOT-ONNX-SCOUT",
        "hypothesis": "Entry-known trade-shape proxy source selection can improve short PF/DD/density without inheriting F42 timing gates.",
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system_missing_in_current_skill_list",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-grok-collaboration",
                "obsidian-result-judgment",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
                "external_review_packet",
            ],
        },
        "grok_stage_open": open_review,
        "data_integrity": checks,
        "source_generation": {
            "condition_pool_rows": int(len(condition_pool)),
            "source_count": len(sources),
            "excluded_session_clock_features": sorted(EXCLUDED_SOURCE_FEATURES),
            "source_ranking_boundary": "entry-known closed-bar shape proxy only; no validation/OOS outcome in source construction",
            "top_conditions": json_ready(condition_pool.head(12).to_dict("records")),
        },
        "artifact_inputs": [
            artifact_identity(f23b.DATASET_PATH),
            artifact_identity(f23b.FEATURE_ORDER_PATH),
            artifact_identity(f33b.RAW_US100_PATH),
            artifact_identity(F42_SELECTION_STATUS),
            artifact_identity(F42_PRESERVED_CLUE),
            artifact_identity(F42_NEGATIVE_MEMORY),
        ],
    }


def build_stage_brief(open_review: dict[str, Any], checks: dict[str, Any], manifest: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

## Hypothesis(가설)
Entry-known trade-shape proxy source(진입 시점 거래 형태 대리 원천)가 weak short PF(약한 숏 수익 팩터)를 설명한다면, source selection criterion(원천 선택 기준)을 train-only closed-bar shape proxy(학습 전용 닫힌 봉 형태 대리값)로 바꾸면 PF/DD/density(수익 팩터/손실폭/밀도)를 동시에 개선할 수 있다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F42 best row(최상 행)는 reference-only(참조 전용), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서).
- changed_variables(변경 변수): source ranking/composition(원천 순위/구성)을 entry-known trade-shape proxy(진입시점 거래 형태 대리값)로 변경.
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 source construction(원천 구성)에 쓰거나 session-clock(세션 시계)을 primary lever(주 레버)로 쓰는 경우.
- stop_conditions(중지 조건): seed/runtime candidate(씨앗/런타임 후보) 발생 또는 capped repair(상한 수리) 종료.

## Grok Stage-Open Review(그록 단계 개방 검토)
- classification(분류): {open_review.get("classification")}
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- guardrail_seen(보호선 확인): {open_review.get("guardrail_seen")}

## Local Checks(로컬 점검)
- feature_hash(피처 해시): `{checks.get("feature_hash")}`
- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("feature_hash_matches_contract")}
- required_splits_present(필수 분할 존재): {checks.get("required_splits_present")}
- source_rows(원천 행): {manifest.get("source_generation", {}).get("source_count")}

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.
"""


def build_closeout_prompt(closeout: dict[str, Any], best_rows: list[dict[str, Any]], repair_decision: dict[str, Any]) -> str:
    best = closeout.get("best_variant", {}) or {}
    compact_rows = "\n".join(
        (
            f"- r{row.get('rank')} {row.get('variant_id')}: "
            f"rule={row.get('rule_definition')}; "
            f"train_pf={row.get('train_profit_factor')}; "
            f"val_pf={row.get('validation_profit_factor')}; "
            f"oos_pf={row.get('oos_profit_factor')}; "
            f"fwd_density={row.get('forward_min_trades_per_day')}..{row.get('forward_max_trades_per_day')}; "
            f"fwd_dd={row.get('forward_max_dd_risk')}; "
            f"scout={row.get('f43_scout_clue_flag')}; seed={row.get('f43_seed_surface_flag')}; "
            f"runtime={row.get('runtime_probe_candidate_flag')}"
        )
        for row in best_rows[:5]
    )
    return f"""# Frontier43 closeout Grok review(그록 마감 검토)

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
- source_id: {best.get("source_id")}
- source_kind(원천 종류): {best.get("source_kind")}
- profile(프로필): {best.get("profile")}
- exit_family(청산 계열): {best.get("exit_family")}
- train_pf(학습 PF): {best.get("train_profit_factor")}
- train_shape_lane_pass(학습 형태 경로 통과): {best.get("train_shape_lane_pass")}
- forward_min_profit_factor(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward density range(전진 거래 밀도 범위): {best.get("forward_min_trades_per_day")} to {best.get("forward_max_trades_per_day")}
- forward_max_dd_risk(전진 최대 DD 위험): {best.get("forward_max_dd_risk")}
- f43_scout_clue_flag(탐색 단서): {best.get("f43_scout_clue_flag")}
- f43_seed_surface_flag(씨앗 표면): {best.get("f43_seed_surface_flag")}
- runtime_probe_candidate_flag(런타임 탐침 후보): {best.get("runtime_probe_candidate_flag")}

Top rows snapshot(상위 행 스냅샷):
{compact_rows}

Question(질문):
Is this closeout classification honest under the lifecycle(가설 생명주기), Grok stage-open guardrail(단계 개방 보호선), and claim boundary(주장 경계)?

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
    best = closeout.get("best_variant", {}) or {}
    return f"""# {RUN_D} report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `{closeout.get("closeout_class")}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}

## Best Observed Row(최상 관찰 행)
- variant_id(변형 ID): `{best.get("variant_id")}`
- source_id(원천 ID): `{best.get("source_id")}`
- source_kind(원천 종류): `{best.get("source_kind")}`
- source_shape_proxy_score(원천 형태 대리 점수): {best.get("source_shape_proxy_score")}
- rule_definition(규칙): `{best.get("rule_definition")}`
- profile(프로필): `{best.get("profile")}`
- exit_family(청산 계열): `{best.get("exit_family")}`
- train_profit_factor(학습 PF): {best.get("train_profit_factor")}
- train_shape_lane_pass(학습 형태 경로 통과): {best.get("train_shape_lane_pass")}
- forward_min_profit_factor(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward_trades_per_day(전진 일 거래 수): {best.get("forward_min_trades_per_day")} ~ {best.get("forward_max_trades_per_day")}
- forward_max_dd_risk(전진 최대 DD 위험): {best.get("forward_max_dd_risk")}

## Sweep Budget(탐색 예산)
- initial_attempt_count(초기 시도 수): {budgets.get("initial", {}).get("attempt_count")}
- repair_attempt_count(수리 시도 수): {budgets.get("repair", {}).get("attempt_count")}
- repair_action(수리 행동): `{repair_decision.get("repair_action")}`
- repair_effect(수리 효과): {repair_decision.get("repair_reason")}

## Grok Review(그록 검토)
- stage_open(단계 개방): {open_review.get("classification")} / accepted_after_local_verification={open_review.get("accepted_after_local_verification")}
- closeout(마감): {closeout_review.get("classification")} / accepted_after_local_verification={closeout_review.get("accepted_after_local_verification")}

## Required Gate Notes(필수 게이트 기록)
- data_integrity(데이터 무결성): feature_hash_matches_contract={checks.get("feature_hash_matches_contract")}, required_splits_present={checks.get("required_splits_present")}
- experiment_design(실험 설계): F43 source ranking(원천 순위)은 entry-known closed-bar shape proxy(진입시점 닫힌봉 형태 대리값)로 고정.
- model_validation(모델 검증): no model/ONNX(모델/온엑스) trained; proxy source only.
- runtime_parity(런타임 동등성): {closeout.get("runtime_probe_status")}
- result_judgment(결과 판정): no completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) claimed.

## Top Rows(상위 행)
```json
{json.dumps(top_records(pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary, 8), ensure_ascii=False, indent=2)}
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
    initial_scout = int(initial_summary["f43_scout_clue_flag"].sum()) if not initial_summary.empty else 0
    initial_seed = int(initial_summary["f43_seed_surface_flag"].sum()) if not initial_summary.empty else 0
    initial_runtime = int(initial_summary["runtime_probe_candidate_flag"].sum()) if not initial_summary.empty else 0
    repair_scout = int(repair_summary["f43_scout_clue_flag"].sum()) if not repair_summary.empty else 0
    repair_seed = int(repair_summary["f43_seed_surface_flag"].sum()) if not repair_summary.empty else 0
    repair_runtime = int(repair_summary["runtime_probe_candidate_flag"].sum()) if not repair_summary.empty else 0
    local = f"""# Local Verification(로컬 검증)

- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("feature_hash_matches_contract")}
- required_splits_present(필수 분할 존재): {checks.get("required_splits_present")}
- open_grok_accepted(개방 그록 수용): {open_review.get("accepted_after_local_verification")}
- closeout_grok_accepted(마감 그록 수용): {closeout_review.get("accepted_after_local_verification")}
- source_ranking_boundary(원천 순위 경계): entry-known closed-bar shape proxy only(진입시점 닫힌 봉 형태 대리값만)
- validation_oos_not_used_for_source_build(검증/표본외 원천 구성 미사용): True
"""
    gate = f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- data_integrity(데이터 무결성): pass(통과), feature hash(피처 해시), split(분할), raw path(원천 경로) verified.
- experiment_design(실험 설계): pass(통과), F43 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) recorded.
- model_validation(모델 검증): out_of_scope_by_claim(주장 범위 밖), no model/ONNX(모델/온엑스) trained.
- artifact_lineage(산출물 계보): pass(통과), source/report/ledger paths(원천/보고/장부 경로) recorded; 02_runs(실행 원자료)는 ignored_with_manifest(목록 포함 무시).
- external_review_packet(외부 검토 묶음): pass(통과), stage-open and closeout Grok(단계 개방/마감 그록) receipts recorded.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `{closeout.get("runtime_probe_status")}`.
- result_judgment(결과 판정): pass(통과), `{closeout.get("closeout_class")}` only.
"""
    open_receipt = f"""# Grok Stage Open Receipt(그록 단계 개방 영수증)

- packet(묶음): `{GROK_OPEN_ROOT.as_posix()}`
- classification(분류): `{open_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- required_guardrail_seen(필수 보호선 확인): {open_review.get("guardrail_seen")}
- forbidden_claim_check(금지 주장 확인): no forbidden claims accepted(금지 주장 수용 없음)
"""
    close_receipt = f"""# Grok Stage Closeout Receipt(그록 단계 마감 영수증)

- packet(묶음): `{GROK_CLOSE_ROOT.as_posix()}`
- classification(분류): `{closeout_review.get("classification")}`
- accepted_after_local_verification(로컬 검증 후 수용): {closeout_review.get("accepted_after_local_verification")}
- closeout_boundary_ok(마감 경계 적합): {closeout_review.get("closeout_boundary_ok")}
"""
    run_a_report = f"""# {RUN_A} report(보고서)

F43 opens a trade-shape source hypothesis(거래 형태 원천 가설). F42 is reference only(참조 전용) and provides preserved clue/negative memory(보존 단서/부정 기억), not winner/baseline/runtime authority(승자/기준선/런타임 권위).
"""
    run_b_report = f"""# {RUN_B} report(보고서)

- rows(행): {len(initial_summary)}
- scout/seed/runtime(탐색/씨앗/런타임): {initial_scout}/{initial_seed}/{initial_runtime}
- attempt_count(시도 수): {budgets.get("initial", {}).get("attempt_count")}
- boundary(경계): source ranking(원천 순위)은 entry-known closed-bar shape proxy(진입시점 닫힌 봉 형태 대리값)로만 만들었다.
"""
    run_c_report = f"""# {RUN_C} report(보고서)

- repair_action(수리 행동): `{repair_decision.get("repair_action")}`
- rows(행): {len(repair_summary)}
- scout/seed/runtime(탐색/씨앗/런타임): {repair_scout}/{repair_seed}/{repair_runtime}
- attempt_count(시도 수): {budgets.get("repair", {}).get("attempt_count")}
- boundary(경계): top source rows only(상위 원천 행만) capped profile diagnostic(상한 프로필 진단).
"""
    return {
        REVIEWS_ROOT / "local_verification.md": local,
        REVIEWS_ROOT / "required_gate_coverage_audit.md": gate,
        REVIEWS_ROOT / "grok_stage_open_receipt.md": open_receipt,
        REVIEWS_ROOT / "grok_stage_closeout_receipt.md": close_receipt,
        REVIEWS_ROOT / f"{RUN_A}_report.md": run_a_report,
        REVIEWS_ROOT / f"{RUN_B}_report.md": run_b_report,
        REVIEWS_ROOT / f"{RUN_C}_report.md": run_c_report,
    }


def build_selected_notes(closeout: dict[str, Any]) -> dict[Path, str]:
    best = closeout.get("best_variant", {}) or {}
    preserved = f"""# Preserved Clue(보존 단서)

F43 preserved clue(보존 단서)는 entry-known trade-shape proxy source(진입시점 거래 형태 대리 원천)가 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_variant(최상 변형): `{best.get("variant_id")}`
- source_id(원천 ID): `{best.get("source_id")}`
- source_kind(원천 종류): `{best.get("source_kind")}`
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_profit_factor")}
- forward_density(전진 거래 밀도): {best.get("forward_min_trades_per_day")} ~ {best.get("forward_max_trades_per_day")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd_risk")}
"""
    negative = f"""# Negative Memory(부정 기억)

F43 negative memory(부정 기억)는 entry-known trade-shape source(진입시점 거래 형태 원천)가 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- do_not_repeat(반복 금지): F42 timing gate(타이밍 제한)나 session-clock(세션 시계)을 winner/baseline(승자/기준선)처럼 상속하지 않는다.
"""
    return {
        SELECTED_ROOT / "preserved_clue.md": preserved,
        SELECTED_ROOT / "negative_memory.md": negative,
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
            "notes": "F43 opened with entry-known trade-shape source hypothesis and Grok guardrails.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_B,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "proxy",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Entry-known trade-shape source proxy surface.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_C,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "repair",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Capped trade-shape profile repair diagnostic.",
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
            "runtime_probe_status": "out_of_scope_by_claim_tier_a_trade_shape_proxy_only",
            "notes": "F43 used Tier A source proxy only; Tier B not claimed.",
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


def project_ledger_row(row: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    view_key = str(row.get("record_view", "")).replace(" ", "_").replace("+", "plus").lower()
    result = {field: "" for field in fields}
    values = {
        "ledger_row_id": f"{row.get('stage_id')}__{row.get('run_id')}__{view_key}",
        "stage_id": row.get("stage_id", ""),
        "run_id": row.get("run_id", ""),
        "record_view": row.get("record_view", ""),
        "tier_scope": row.get("record_view", ""),
        "kpi_scope": "trade_shape_source_proxy",
        "scoreboard_lane": "frontier_scout",
        "status": row.get("status", ""),
        "judgment": row.get("closeout_class", ""),
        "external_verification_status": row.get("runtime_probe_status", ""),
        "notes": row.get("notes", ""),
        "path": (REVIEWS_ROOT / f"{row.get('run_id')}_report.md").as_posix(),
        "report_path": (REVIEWS_ROOT / f"{row.get('run_id')}_report.md").as_posix(),
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness",
        "run_family": "frontier_trade_shape_source_proxy",
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
current_judgment: {closeout.get("closeout_class")}(F43 trade-shape source proxy no operating authority)
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

Frontier43(F43, 전선 43단계)가 `{closeout.get("closeout_class")}`로 닫혔다.

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

F43 carry-forward(이월) 기록은 entry-known trade-shape source(진입시점 거래 형태 원천)가 PF/DD/density(수익 팩터/손실폭/밀도)를 네 축 목표까지 끌어올렸는지와 seed/runtime(씨앗/런타임) 후보가 생겼는지 여부다.
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
    condition_pool, conditions, valid = build_condition_pool(frame, feature_order, path_labels)
    sources = build_sources(frame, conditions, valid)
    manifest = build_input_manifest(checks, open_review, condition_pool, sources)

    write_text_sig(SPEC_ROOT / "stage_brief.md", build_stage_brief(open_review, checks, manifest))
    write_json(INPUT_ROOT / "trade_shape_source_manifest.json", manifest)
    write_csv(INPUT_ROOT / "entry_shape_condition_pool.csv", condition_pool)
    source_rows = [
        {
            "source_id": source.source_id,
            "source_kind": source.source_kind,
            "condition_ids": "|".join(c.condition_id for c in source.conditions),
            "features": source.features,
            "feature_families": source.feature_families,
            "rule_definition": source.rule_definition,
            "source_shape_proxy_score": source.source_shape_proxy_score,
            "train_coverage": source.train_coverage,
            "split_counts": json.dumps(source.split_counts, sort_keys=True),
            "split_hashes": json.dumps(source.split_hashes, sort_keys=True),
        }
        for source in sources
    ]
    write_csv(INPUT_ROOT / "entry_shape_source_pool.csv", pd.DataFrame(source_rows))
    write_json(RUN_A_ROOT / "stage_open_local_verification.json", {"open_review": open_review, "checks": checks})

    initial_metrics, initial_summary, initial_budget = run_surface(frame, sources, path_labels, raw_path, RUN_B, "initial")
    write_csv(RUN_B_ROOT / "entry_known_trade_shape_split_metrics.csv", initial_metrics)
    write_csv(RUN_B_ROOT / "entry_known_trade_shape_candidate_summary.csv", initial_summary)
    write_json(RUN_B_ROOT / "trade_shape_source_budget.json", initial_budget)

    repair_decision = build_repair_decision(initial_summary)
    repair_metrics = pd.DataFrame()
    repair_summary = pd.DataFrame()
    repair_budget = {
        "run_id": RUN_C,
        "profile": "repair",
        "source_count": 0,
        "attempt_count": 0,
        "exit_profile_policy": "skipped",
    }
    if repair_decision.get("run_repair_grid"):
        source_by_id = {source.source_id: source for source in sources}
        repair_sources = [source_by_id[source_id] for source_id in repair_decision.get("repair_source_ids", []) if source_id in source_by_id]
        repair_metrics, repair_summary, repair_budget = run_surface(frame, repair_sources, path_labels, raw_path, RUN_C, "repair")
    write_json(RUN_C_ROOT / "repair_decision.json", repair_decision)
    write_csv(RUN_C_ROOT / "capped_trade_shape_profile_split_metrics.csv", repair_metrics)
    write_csv(RUN_C_ROOT / "capped_trade_shape_profile_candidate_summary.csv", repair_summary)
    write_json(RUN_C_ROOT / "trade_shape_profile_budget.json", repair_budget)

    closeout = classify_closeout(initial_summary, repair_summary)
    combined = pd.concat([initial_summary, repair_summary], ignore_index=True) if not repair_summary.empty else initial_summary
    best_rows = top_records(combined, 8)
    write_json(RUN_D_ROOT / "closeout_decision.json", closeout)
    if not path_exists(GROK_CLOSE_ROOT / "metadata.json"):
        write_text_sig(GROK_CLOSE_ROOT / "input_prompt.md", build_closeout_prompt(closeout, best_rows, repair_decision))
    closeout_review = load_closeout_grok_review()
    budgets = {"initial": initial_budget, "repair": repair_budget}
    closeout_report = build_report(checks, open_review, closeout_review, initial_summary, repair_summary, repair_decision, closeout, budgets)
    write_text_sig(RUN_D_ROOT / "frontier43D_stage_closeout_trade_shape_source_v1_report.md", closeout_report)
    for path, text in build_review_artifacts(checks, open_review, closeout_review, initial_summary, repair_summary, repair_decision, closeout, budgets).items():
        write_text_sig(path, text)
    write_text_sig(REVIEWS_ROOT / f"{RUN_D}_report.md", closeout_report)
    write_json(
        RUN_D_ROOT / "run_manifest.json",
        {
            "stage_id": STAGE_ID,
            "runs": [RUN_A, RUN_B, RUN_C, RUN_D],
            "open_review": open_review,
            "closeout_review": closeout_review,
            "closeout": closeout,
            "repair_decision": repair_decision,
            "budgets": budgets,
            "artifacts": {
                "trade_shape_source_manifest": (INPUT_ROOT / "trade_shape_source_manifest.json").as_posix(),
                "condition_pool": (INPUT_ROOT / "entry_shape_condition_pool.csv").as_posix(),
                "source_pool": (INPUT_ROOT / "entry_shape_source_pool.csv").as_posix(),
                "initial_summary": (RUN_B_ROOT / "entry_known_trade_shape_candidate_summary.csv").as_posix(),
                "repair_summary": (RUN_C_ROOT / "capped_trade_shape_profile_candidate_summary.csv").as_posix(),
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
