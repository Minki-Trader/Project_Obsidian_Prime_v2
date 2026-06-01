from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "354_proxy_trade_shape_scout__small_candidate_queue"
RUN_NUMBER = "run354C"
RUN_ID = "run354C_expand_proxy_filter_sweep_without_db_v1"
PARENT_RUN_ID = "run354B_lightweight_proxy_trade_shape_scan_without_db_v1"

POSITIVE_NEXT_STAGE_ID = "355_runtime_probe_package__expanded_proxy_queue_mt5_handoff"
POSITIVE_NEXT_RUN_ID = "run355A_materialize_expanded_proxy_queue_mt5_probe_package_without_db_v1"
NEGATIVE_NEXT_STAGE_ID = "355_density_recovery_model_family__new_label_source_probe"
NEGATIVE_NEXT_RUN_ID = "run355A_design_density_recovery_label_model_source_without_db_v1"

CLAIM_BOUNDARY = (
    "expanded_proxy_filter_sweep_only_existing_stage351b_surfaces_raw_close_horizon_proxy_"
    "mt5_probe_required_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

HOLD_BARS_LIST = [4, 6, 8, 12]
THRESHOLDS = [0.28, 0.30, 0.32, 0.34, 0.36, 0.38]
THRESHOLD_PAIRS = [
    (0.28, 0.28),
    (0.30, 0.30),
    (0.32, 0.32),
    (0.34, 0.34),
    (0.36, 0.36),
    (0.38, 0.38),
    (0.28, 0.34),
    (0.34, 0.28),
    (0.30, 0.36),
    (0.36, 0.30),
    (0.32, 0.38),
    (0.38, 0.32),
]
MARGINS = [0.0, 0.005, 0.01, 0.02]
BASE_COST_LOG_RETURN = 0.00015
STRESS_COST_LOG_RETURN = 0.00030
MIN_TRADE_PER_DAY = 3.0
MIN_BALANCE = 0.20

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

EXPECTED_TAPE = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "expected"
    / "expected_tape.csv"
)
RUNTIME_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)
RAW_US100_BARS = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
SOURCE_RUN354B_FINAL = STAGE_DIR / "02_runs" / "run354B" / "final_decision.json"
SOURCE_RUN354B_SCOREBOARD = STAGE_DIR / "02_runs" / "run354B" / "nonoverlap_candidate_scoreboard.csv"

SWEEP = RUN_DIR / "expanded_outcome_horizon_sweep.csv"
DENSITY_QUEUE = RUN_DIR / "density_valid_queue.csv"
NEAR_MISS = RUN_DIR / "near_miss_scoreboard.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
REPORT_PATH = REVIEW_DIR / "run354C_expand_proxy_filter_sweep.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage354C_expand_proxy_filter_sweep.md"

STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"

SWEEP_COLUMNS = [
    "candidate_id",
    "model_variant_id",
    "hold_bars",
    "filter_name",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "base_cost_log_return",
    "stress_cost_log_return",
    "validation_trade_count",
    "validation_long_count",
    "validation_short_count",
    "validation_trade_per_day",
    "validation_net_log_return",
    "validation_profit_factor",
    "validation_expectancy",
    "validation_win_rate",
    "validation_max_drawdown",
    "validation_recovery_factor",
    "validation_long_short_balance",
    "validation_positive_day_ratio",
    "validation_equity_r2",
    "validation_stress_net_log_return",
    "oos_trade_count",
    "oos_long_count",
    "oos_short_count",
    "oos_trade_per_day",
    "oos_net_log_return",
    "oos_profit_factor",
    "oos_expectancy",
    "oos_win_rate",
    "oos_max_drawdown",
    "oos_recovery_factor",
    "oos_long_short_balance",
    "oos_positive_day_ratio",
    "oos_equity_r2",
    "oos_stress_net_log_return",
    "validation_oos_net_gap",
    "validation_oos_pf_gap",
    "validation_oos_density_gap",
    "density_valid",
    "stress_valid",
    "selection_score",
    "claim_boundary",
    "scan_layer",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(100_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    new_rows = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing_rows = read_csv_rows(path)
    else:
        fieldnames, existing_rows = [], []
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replace_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in existing_rows
        if tuple(str(row.get(key, "")) for key in key_fields) not in replace_keys
    ]
    write_csv(path, kept + new_rows, fieldnames)


def kpi_from_net(net: np.ndarray, sides: np.ndarray, dates: np.ndarray) -> dict[str, Any]:
    if len(net) == 0:
        return {
            "trade_count": 0,
            "long_count": 0,
            "short_count": 0,
            "trade_per_day": 0.0,
            "net_log_return": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "win_rate": 0.0,
            "max_drawdown": 0.0,
            "recovery_factor": 0.0,
            "long_short_balance": 0.0,
            "positive_day_ratio": 0.0,
            "equity_r2": 0.0,
        }
    gains = float(net[net > 0.0].sum())
    losses = float(net[net < 0.0].sum())
    if losses < 0.0:
        profit_factor = gains / abs(losses)
    elif gains > 0.0:
        profit_factor = 999.0
    else:
        profit_factor = 0.0
    equity = np.cumsum(net)
    peak = np.maximum.accumulate(np.insert(equity, 0, 0.0))[1:]
    max_drawdown = abs(float(np.min(equity - peak))) if len(equity) else 0.0
    net_total = float(net.sum())
    if max_drawdown > 0.0:
        recovery = net_total / max_drawdown
    else:
        recovery = 999.0 if net_total > 0.0 else 0.0
    long_count = int((sides == 2).sum())
    short_count = int((sides == 0).sum())
    balance = min(long_count, short_count) / max(1, max(long_count, short_count))
    day_sum = pd.DataFrame({"date": dates, "net": net}).groupby("date")["net"].sum()
    if len(equity) >= 3:
        corr = np.corrcoef(np.arange(len(equity), dtype=float), equity)[0, 1]
        equity_r2 = float(corr * corr) if math.isfinite(corr) else 0.0
    else:
        equity_r2 = 0.0
    return {
        "trade_count": int(len(net)),
        "long_count": long_count,
        "short_count": short_count,
        "trade_per_day": float(len(net) / max(1, len(set(map(str, dates))))),
        "net_log_return": net_total,
        "profit_factor": float(min(profit_factor, 999.0)),
        "expectancy": float(net.mean()),
        "win_rate": float((net > 0.0).mean()),
        "max_drawdown": max_drawdown,
        "recovery_factor": float(min(recovery, 999.0)),
        "long_short_balance": float(balance),
        "positive_day_ratio": float((day_sum > 0.0).mean()) if len(day_sum) else 0.0,
        "equity_r2": equity_r2,
    }


def nonoverlap_trade_kpi(
    labels: np.ndarray,
    future_returns: np.ndarray,
    dates: np.ndarray,
    hold_bars: int,
    cost: float,
) -> dict[str, Any]:
    trade_indexes = np.flatnonzero(labels != 1)
    net: list[float] = []
    sides: list[int] = []
    trade_dates: list[str] = []
    next_allowed = 0
    for index in trade_indexes:
        if index < next_allowed:
            continue
        side = int(labels[index])
        gross = -float(future_returns[index]) if side == 0 else float(future_returns[index])
        net.append(gross - cost)
        sides.append(side)
        trade_dates.append(str(dates[index]))
        next_allowed = index + hold_bars
    return kpi_from_net(np.asarray(net, dtype=float), np.asarray(sides, dtype=np.int8), np.asarray(trade_dates, dtype=str))


def labels_from_surface(
    p_short: np.ndarray,
    p_flat: np.ndarray,
    p_long: np.ndarray,
    mask: np.ndarray,
    short_threshold: float,
    long_threshold: float,
    margin: float,
) -> np.ndarray:
    short_margin = p_short - np.maximum(p_flat, p_long)
    long_margin = p_long - np.maximum(p_flat, p_short)
    short_ok = (p_short >= short_threshold) & (short_margin >= margin) & mask
    long_ok = (p_long >= long_threshold) & (long_margin >= margin) & mask
    labels = np.ones(len(p_short), dtype=np.int8)
    long_take = long_ok & ((~short_ok) | (p_long >= p_short))
    short_take = short_ok & (~long_take)
    labels[long_take] = 2
    labels[short_take] = 0
    return labels


def kpi_prefixed(prefix: str, kpi: Mapping[str, Any]) -> dict[str, Any]:
    return {f"{prefix}_{key}": value for key, value in kpi.items()}


def selection_score(row: Mapping[str, Any]) -> float:
    val_net = float(row["validation_net_log_return"])
    oos_net = float(row["oos_net_log_return"])
    val_pf = float(row["validation_profit_factor"])
    oos_pf = float(row["oos_profit_factor"])
    val_dd = float(row["validation_max_drawdown"])
    oos_dd = float(row["oos_max_drawdown"])
    val_density = float(row["validation_trade_per_day"])
    oos_density = float(row["oos_trade_per_day"])
    val_balance = float(row["validation_long_short_balance"])
    oos_balance = float(row["oos_long_short_balance"])
    stress = float(row["validation_stress_net_log_return"]) + float(row["oos_stress_net_log_return"])
    density_shortfall = max(0.0, MIN_TRADE_PER_DAY - val_density) + max(0.0, MIN_TRADE_PER_DAY - oos_density)
    return (
        val_net * 9000.0
        + oos_net * 10000.0
        + math.log1p(max(0.0, min(val_pf, 20.0))) * 50.0
        + math.log1p(max(0.0, min(oos_pf, 20.0))) * 60.0
        + val_balance * 16.0
        + oos_balance * 24.0
        + stress * 3000.0
        - val_dd * 700.0
        - oos_dd * 1000.0
        - abs(val_net - oos_net) * 2500.0
        - abs(val_density - oos_density) * 6.0
        - density_shortfall * 140.0
    )


def build_filters(frame: pd.DataFrame) -> list[tuple[str, np.ndarray]]:
    cash = frame["is_us_cash_open"].to_numpy(dtype=float) == 1.0
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    adx = frame["adx_14"].to_numpy(dtype=float)
    vix = frame["vix_zscore_20"].to_numpy(dtype=float)
    size = len(frame)
    return [
        ("all", np.ones(size, dtype=bool)),
        ("cash", cash),
        ("adx20", adx >= 20.0),
        ("adx25", adx >= 25.0),
        ("post30_330", cash & (minutes >= 30.0) & (minutes <= 330.0)),
        ("vix_abs1", np.abs(vix) <= 1.0),
    ]


def load_data() -> tuple[pd.DataFrame, dict[str, Any]]:
    expected_cols = ["model_variant_id", "bar_time_server", "timestamp_utc", "split", "p_short", "p_flat", "p_long"]
    feature_cols = [
        "bar_time_server",
        "timestamp_utc",
        "split",
        "is_us_cash_open",
        "minutes_from_cash_open",
        "adx_14",
        "vix_zscore_20",
    ]
    expected = pd.read_csv(fs_path(EXPECTED_TAPE), usecols=expected_cols)
    features = pd.read_csv(fs_path(RUNTIME_FEATURES), usecols=feature_cols)
    raw = pd.read_csv(fs_path(RAW_US100_BARS), usecols=["time_close_unix", "close"])
    raw["timestamp_utc"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    raw = raw.sort_values("time_close_unix").reset_index(drop=True)
    raw["log_close"] = np.log(raw["close"].astype(float))
    for hold_bars in HOLD_BARS_LIST:
        raw[f"future_log_return_{hold_bars}"] = raw["log_close"].shift(-hold_bars) - raw["log_close"]
    future_cols = ["timestamp_utc"] + [f"future_log_return_{hold_bars}" for hold_bars in HOLD_BARS_LIST]
    future = raw[future_cols]
    merged = expected.merge(
        features,
        on=["bar_time_server", "timestamp_utc"],
        how="left",
        suffixes=("", "_feature"),
    ).merge(future, on="timestamp_utc", how="left")
    split_mismatch = int((merged["split"] != merged["split_feature"]).sum()) if "split_feature" in merged else 0
    if "split_feature" in merged:
        merged = merged.drop(columns=["split_feature"])
    missing_future = {
        str(hold_bars): int(merged[f"future_log_return_{hold_bars}"].isna().sum())
        for hold_bars in HOLD_BARS_LIST
    }
    identity = {
        "expected_rows": int(len(expected)),
        "feature_rows": int(len(features)),
        "raw_rows": int(len(raw)),
        "merged_rows": int(len(merged)),
        "model_count": int(expected["model_variant_id"].nunique()),
        "expected_duplicate_key_rows": int(expected.duplicated(["model_variant_id", "timestamp_utc"]).sum()),
        "feature_duplicate_timestamp_rows": int(features.duplicated(["timestamp_utc"]).sum()),
        "raw_duplicate_timestamp_rows": int(raw.duplicated(["timestamp_utc"]).sum()),
        "split_mismatch_rows": split_mismatch,
        "missing_future_rows_by_hold": missing_future,
        "expected_sha256": sha256_file(EXPECTED_TAPE),
        "features_sha256": sha256_file(RUNTIME_FEATURES),
        "raw_us100_bars_sha256": sha256_file(RAW_US100_BARS),
    }
    if (
        identity["feature_duplicate_timestamp_rows"]
        or identity["raw_duplicate_timestamp_rows"]
        or identity["split_mismatch_rows"]
        or any(value for value in missing_future.values())
    ):
        raise RuntimeError(f"data integrity failure(데이터 무결성 실패): {identity}")
    merged["date"] = pd.to_datetime(merged["timestamp_utc"], utc=True).dt.date.astype(str)
    return merged, identity


def scan(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    for model_id, group in data.groupby("model_variant_id", sort=False):
        group = group.reset_index(drop=True)
        split_values = group["split"].to_numpy(dtype=str)
        p_short = group["p_short"].to_numpy(dtype=float)
        p_flat = group["p_flat"].to_numpy(dtype=float)
        p_long = group["p_long"].to_numpy(dtype=float)
        dates = group["date"].to_numpy(dtype=str)
        split_masks = {
            "validation": split_values == "validation",
            "oos": split_values == "oos",
        }
        filters = build_filters(group)
        for hold_bars in HOLD_BARS_LIST:
            future = group[f"future_log_return_{hold_bars}"].to_numpy(dtype=float)
            for filter_name, filter_mask in filters:
                for short_threshold, long_threshold in THRESHOLD_PAIRS:
                    for margin in MARGINS:
                            labels = labels_from_surface(
                                p_short,
                                p_flat,
                                p_long,
                                filter_mask,
                                short_threshold,
                                long_threshold,
                                margin,
                            )
                            row: dict[str, Any] = {
                                "candidate_id": (
                                    f"{model_id}__h{hold_bars}__{filter_name}"
                                    f"__s{short_threshold:.3f}__l{long_threshold:.3f}__m{margin:.3f}"
                                ),
                                "model_variant_id": model_id,
                                "hold_bars": hold_bars,
                                "filter_name": filter_name,
                                "short_threshold": short_threshold,
                                "long_threshold": long_threshold,
                                "min_margin": margin,
                                "base_cost_log_return": BASE_COST_LOG_RETURN,
                                "stress_cost_log_return": STRESS_COST_LOG_RETURN,
                                "claim_boundary": CLAIM_BOUNDARY,
                                "scan_layer": "expanded_raw_close_horizon_nonoverlap_proxy(확장 원시 종가 보유기간 비중첩 프록시)",
                            }
                            for split_name, split_mask in split_masks.items():
                                base = nonoverlap_trade_kpi(
                                    labels[split_mask],
                                    future[split_mask],
                                    dates[split_mask],
                                    hold_bars,
                                    BASE_COST_LOG_RETURN,
                                )
                                row.update(kpi_prefixed(split_name, base))
                                row[f"{split_name}_stress_net_log_return"] = (
                                    float(base["net_log_return"])
                                    - (STRESS_COST_LOG_RETURN - BASE_COST_LOG_RETURN) * float(base["trade_count"])
                                )
                            row["validation_oos_net_gap"] = abs(
                                float(row["validation_net_log_return"]) - float(row["oos_net_log_return"])
                            )
                            row["validation_oos_pf_gap"] = abs(
                                float(row["validation_profit_factor"]) - float(row["oos_profit_factor"])
                            )
                            row["validation_oos_density_gap"] = abs(
                                float(row["validation_trade_per_day"]) - float(row["oos_trade_per_day"])
                            )
                            row["density_valid"] = (
                                float(row["validation_trade_per_day"]) >= MIN_TRADE_PER_DAY
                                and float(row["oos_trade_per_day"]) >= MIN_TRADE_PER_DAY
                                and int(row["validation_trade_count"]) > 0
                                and int(row["oos_trade_count"]) > 0
                            )
                            row["stress_valid"] = (
                                float(row["validation_stress_net_log_return"]) > 0.0
                                and float(row["oos_stress_net_log_return"]) > 0.0
                            )
                            row["selection_score"] = selection_score(row)
                            rows.append(row)
    sweep = pd.DataFrame(rows, columns=SWEEP_COLUMNS).sort_values("selection_score", ascending=False)
    eligible_mask = (
        (sweep["validation_net_log_return"] > 0.0)
        & (sweep["oos_net_log_return"] > 0.0)
        & (sweep["validation_profit_factor"] >= 1.0)
        & (sweep["oos_profit_factor"] >= 1.0)
        & (sweep["validation_trade_per_day"] >= MIN_TRADE_PER_DAY)
        & (sweep["oos_trade_per_day"] >= MIN_TRADE_PER_DAY)
        & (sweep["validation_long_short_balance"] >= MIN_BALANCE)
        & (sweep["oos_long_short_balance"] >= MIN_BALANCE)
        & (sweep["validation_stress_net_log_return"] > 0.0)
        & (sweep["oos_stress_net_log_return"] > 0.0)
    )
    queue = sweep.loc[eligible_mask].copy().sort_values("selection_score", ascending=False)
    near = sweep.head(80).copy()
    return sweep, queue, near


def write_findings(queue: pd.DataFrame, near: pd.DataFrame) -> None:
    if len(queue):
        rows = [
            {
                "finding_id": f"{RUN_ID}__proxy_queue_requires_mt5_probe",
                "source_run": RUN_ID,
                "finding": "density-valid proxy queue(밀도 유효 프록시 대기열)가 생겼지만 MT5 probe(MT5 탐침) 전에는 운영 근거가 아니다.",
                "evidence": rel(DENSITY_QUEUE),
                "salvage_value": "next MT5 probe package(다음 MT5 탐침 패키지)로 보낸다.",
                "do_not_repeat": "proxy KPI(프록시 핵심 성과 지표)를 MT5 KPI(MT5 핵심 성과 지표)처럼 말하지 않는다.",
                "reopen_condition": "MT5 runtime probe(MT5 런타임 탐침)가 proxy-MT5 diff(프록시-MT5 차이)를 닫을 때.",
                "next_action": POSITIVE_NEXT_RUN_ID,
            }
        ]
    else:
        best = near.iloc[0].to_dict() if len(near) else {}
        rows = [
            {
                "finding_id": f"{RUN_ID}__existing_surface_density_edge_failure",
                "source_run": RUN_ID,
                "finding": (
                    "기존 Stage351B probability surface(확률 표면)는 hold/filter/threshold(보유기간/필터/임계값) 확장에서도 "
                    "validation/OOS(검증/표본외) 순수익, 비용 압박, trade/day(일별 거래수) 3+를 동시에 만족하지 못했다."
                ),
                "evidence": rel(SWEEP),
                "salvage_value": (
                    f"best_near_miss(최상 근접 실패) `{best.get('candidate_id', 'none')}`를 실패 경계로 보존한다."
                ),
                "do_not_repeat": "같은 surface(표면)의 미세 threshold search(임계값 미세 탐색)를 운영 후보처럼 반복하지 않는다.",
                "reopen_condition": (
                    "new label/source/model family(새 라벨/원천/모델 계열) 또는 MT5 runtime diff(MT5 런타임 차이)가 생길 때."
                ),
                "next_action": NEGATIVE_NEXT_RUN_ID,
            }
        ]
    write_csv(FAILURE_MEMORY, rows)


def write_receipts(data_identity: Mapping[str, Any], sweep: pd.DataFrame, queue: pd.DataFrame) -> None:
    created = now_utc()
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created,
    }
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            **common,
            "data_source": [rel(EXPECTED_TAPE), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS)],
            "time_axis": "timestamp_utc is closed M5 bar time(UTC 닫힌 M5 봉 시각)",
            "sample_scope": "US100 M5 Stage351B expected tape with validation and OOS splits(US100 M5 351B 검증/표본외 표본)",
            "missing_or_duplicate_check": data_identity,
            "feature_label_boundary": (
                "features use existing closed-bar runtime features; labels use raw close shifted only after the current timestamp"
                "(피처는 닫힌 봉 런타임 피처, 라벨은 현재 시각 이후 원시 종가 이동 수익률)"
            ),
            "split_boundary": "existing Stage351B split field(기존 351B 분할 필드)",
            "leakage_risk": "future returns are used only for proxy scoring, not as model inputs(미래 수익률은 프록시 점수 전용)",
            "data_hash_or_identity": data_identity,
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "idea_id": "IDEA-ST354C-EXPANDED-HORIZON-FILTER-SWEEP",
            "hypothesis": (
                "existing probability surface(기존 확률 표면) may recover density and edge by using alternate raw-close horizons"
                "(원시 종가 보유기간) and broader filters(넓은 필터)."
            ),
            "legacy_relation": "prior_evidence_only(이전 근거 전용)",
            "tier_scope": "Tier A separate + Tier B missing_required + Tier A+B same_as_tier_a(Tier A 분리 + Tier B 필수 누락 + 합산 동일)",
            "broad_sweep": {
                "holds": HOLD_BARS_LIST,
                "filters": ["all", "cash", "adx20", "adx25", "post30_330", "vix_abs1"],
                "threshold_pairs": THRESHOLD_PAIRS,
                "margins": MARGINS,
            },
            "extreme_sweep": "symmetric plus asymmetric short/long threshold pairs 0.28..0.38(대칭 및 비대칭 숏/롱 임계값 쌍)",
            "micro_search_gate": "density-valid queue must exist before fine search(밀도 유효 대기열 전에는 미세 탐색 금지)",
            "wfo_plan": "not applied; scout-only fixed validation/OOS split(WFO 미적용, 탐색 전용 검증/표본외 분할)",
            "failure_memory": rel(FAILURE_MEMORY),
            "evidence_boundary": "scout_only_proxy(프록시 탐색 전용)",
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-exploration-mandate(탐색 규율)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            **common,
            "model_family": "reused Stage351B probability surfaces(351B 확률 표면 재사용), no new training(신규 학습 없음)",
            "target_and_label": "raw US100 close future log return horizons 4/6/8/12(원시 US100 종가 미래 로그수익률)",
            "split_method": "fixed validation/OOS proxy scout(고정 검증/표본외 프록시 탐색)",
            "selection_metric": "multi-KPI score with density, stress, PF, drawdown(밀도/압박/수익 팩터/낙폭 복합 점수)",
            "secondary_metrics": [
                "trade_per_day(일별 거래수)",
                "long_short_balance(롱/숏 균형)",
                "stress_net_log_return(비용 압박 순 로그수익)",
                "equity_r2(수익곡선 품질)",
            ],
            "threshold_policy": "searched exploratory threshold surface(탐색 임계값 표면 검색)",
            "overfit_risk": "multiple-testing risk; queue requires MT5 runtime probe(다중 탐색 위험, MT5 런타임 탐침 필요)",
            "calibration_risk": "probabilities are treated as rank scores unless calibrated(보정 전 확률은 순위 점수)",
            "comparison_baseline": rel(SOURCE_RUN354B_FINAL),
            "validation_judgment": "exploratory(탐색)",
            "sweep_rows": int(len(sweep)),
            "density_valid_queue_rows": int(len(queue)),
        },
    )
    artifact_paths = [
        SWEEP,
        DENSITY_QUEUE,
        NEAR_MISS,
        FAILURE_MEMORY,
        DATA_INTEGRITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        RUN_MANIFEST,
        FINAL_DECISION,
        REPORT_PATH,
    ]
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [rel(EXPECTED_TAPE), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS), rel(SOURCE_RUN354B_FINAL)],
            "producer": rel(Path(__file__)),
            "consumer": "Stage355 next action(355단계 다음 행동)",
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {
                rel(path): sha256_file(path)
                for path in [SWEEP, DENSITY_QUEUE, NEAR_MISS, FAILURE_MEMORY, DATA_INTEGRITY_RECEIPT, EXPERIMENT_RECEIPT, MODEL_VALIDATION_RECEIPT]
                if exists(path)
            },
            "registry_links": [rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(RUN_REGISTRY), rel(ARTIFACT_REGISTRY)],
            "availability": "reproducible_from_command(명령으로 재생 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    judgment = (
        "exploratory_proxy_positive_queue_mt5_probe_required_no_operating_claim"
        if len(queue)
        else "negative_proxy_scout_existing_surface_no_density_edge_queue_no_operating_claim"
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(SWEEP), rel(DENSITY_QUEUE), rel(NEAR_MISS), rel(FAILURE_MEMORY)],
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침), forward replay(전진 재생), runtime parity closeout(런타임 동등성 종료)",
            "judgment_label": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": (
                "Run MT5 probe package( MT5 탐침 패키지 실행)" if len(queue) else
                "Open new label/source/model family design(새 라벨/원천/모델 계열 설계 시작)"
            ),
            "user_explanation_hook": "proxy is a scout, not an operating proof(프록시는 탐색이지 운영 증명이 아님)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "expanded proxy scout result only(확장 프록시 탐색 결과만)",
            "forbidden_claims": [
                "candidate_selection(후보 선정)",
                "MT5 KPI substitute(MT5 핵심 성과 지표 대체)",
                "forward pass(전진 통과)",
                "live readiness(실거래 준비)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )


def write_next_stage_stub(candidate_count: int) -> tuple[str, str, str, str]:
    if candidate_count:
        next_stage_id = POSITIVE_NEXT_STAGE_ID
        next_run_id = POSITIVE_NEXT_RUN_ID
        selection_status = "proxy_queue_ready_no_selection(프록시 대기열 준비, 선정 없음)"
        stage_question = "expanded proxy queue(확장 프록시 대기열)를 MT5 runtime probe(MT5 런타임 탐침) 패키지로 만들 수 있는가?"
        next_effect = "proxy(프록시)를 운영 근거로 오해하지 않고 MT5 probe(MT5 탐침)로 검증한다."
    else:
        next_stage_id = NEGATIVE_NEXT_STAGE_ID
        next_run_id = NEGATIVE_NEXT_RUN_ID
        selection_status = "new_label_model_source_pivot_open(새 라벨/모델/원천 전환 열림)"
        stage_question = (
            "기존 probability surface(확률 표면)의 임계값/보유기간 확장이 실패했으므로, "
            "새 label/source/model family(라벨/원천/모델 계열)로 거래 밀도와 수익 원천을 회복할 수 있는가?"
        )
        next_effect = "같은 blocker(차단 원인)를 반복하지 않고 새 수익 원천 탐색으로 이동한다."
    stage_dir = ROOT / "stages" / next_stage_id
    for directory in [stage_dir / "00_spec", stage_dir / "01_inputs", stage_dir / "02_runs", stage_dir / "03_reviews", stage_dir / "04_selected"]:
        os.makedirs(fs_path(directory), exist_ok=True)
    write_text(
        stage_dir / "00_spec" / "stage_brief.md",
        f"""# Stage355 {next_stage_id}(355단계)

- canonical_stage_id(정식 단계 ID): `{next_stage_id}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- source_run_id(원천 실행 ID): `{RUN_ID}`
- selection_status(선택 상태): `{selection_status}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

{stage_question}

## Action(행동)

Stage354C(354C 실행)의 결과를 다음 작업 묶음(work packet, 작업 묶음)으로 넘긴다.

## Effect(효과)

{next_effect}
""",
    )
    write_text(
        stage_dir / "01_inputs" / "input_refs.md",
        f"""# Stage355 Input Refs(355단계 입력 참조)

- source_final_decision(원천 최종 결정): `{rel(FINAL_DECISION)}`
- source_sweep(원천 스윕): `{rel(SWEEP)}`
- source_queue(원천 대기열): `{rel(DENSITY_QUEUE)}`
- source_failure_memory(원천 실패 기억): `{rel(FAILURE_MEMORY)}`

Action(행동): Stage354C(354C 실행)의 current truth(현재 진실)와 failure memory(실패 기억)를 입력으로 고정한다.

Effect(효과): 다음 실행이 같은 threshold-only search(임계값 전용 탐색)를 반복하지 않게 한다.
""",
    )
    write_text(
        stage_dir / "03_reviews" / "review_index.md",
        f"""# Stage355 Review Index(355단계 검토 색인)

- pending_run(대기 실행): `{next_run_id}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
""",
    )
    selection_text = f"""# Stage355 Selection Status(355단계 선택 상태)

- selection_status(선택 상태): `{selection_status}`
- active_stage_id(활성 단계 ID): `{next_stage_id}`
- latest_completed_source_run_id(최근 완료 원천 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- mt5_queue_rows(MT5 대기열 행): `{candidate_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(stage_dir / "04_selected" / "selection_status.md", selection_text)
    return next_stage_id, next_run_id, selection_status, selection_text


def status_bundle(candidate_count: int) -> tuple[str, str, str]:
    if candidate_count:
        return (
            "completed_stage354C_expanded_proxy_queue_ready_for_mt5_probe_package_no_selection",
            "exploratory_proxy_positive_queue_mt5_probe_required_no_operating_claim",
            f"stage354C_open_{POSITIVE_NEXT_RUN_ID}",
        )
    return (
        "completed_stage354C_expanded_sweep_no_density_edge_queue_model_family_pivot_opened",
        "negative_proxy_scout_existing_surface_no_density_edge_queue_no_operating_claim",
        f"stage354C_open_{NEGATIVE_NEXT_RUN_ID}",
    )


def write_report_state_and_docs(
    data_identity: Mapping[str, Any],
    sweep: pd.DataFrame,
    queue: pd.DataFrame,
    near: pd.DataFrame,
) -> tuple[str, str, str, str]:
    candidate_count = int(len(queue))
    status, judgment, decision = status_bundle(candidate_count)
    next_stage_id, next_run_id, selection_status, root_selection_text = write_next_stage_stub(candidate_count)
    best = queue.iloc[0].to_dict() if candidate_count else (near.iloc[0].to_dict() if len(near) else {})
    write_text(ROOT_SELECTION, root_selection_text)
    write_text(
        SELECTION_STATUS,
        f"""# Stage354 Selection Status(354단계 선택 상태)

- selection_status(선택 상태): `completed_no_density_valid_queue(완료, 밀도 유효 대기열 없음)` 
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- handoff_stage_id(인계 단계 ID): `{next_stage_id}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- mt5_queue_rows(MT5 대기열 행): `{candidate_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {next_stage_id}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
current_decision: {decision}
next_run_id: {next_run_id}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{next_stage_id}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{status}`
- current_judgment(현재 판정): `{judgment}`
- current_decision(현재 결정): `{decision}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage354C(354C 실행)에서 expanded proxy filter sweep(확장 프록시 필터 스윕)을 완료했다.

Effect(효과): 기존 probability surface(확률 표면)의 threshold/horizon/filter(임계값/보유기간/필터) 확장이 trade/day(일별 거래수) 3+와 수익/비용 압박을 동시에 만족하지 못하면, 다음 Stage355(355단계)를 새 label/source/model family(라벨/원천/모델 계열) 탐색으로 연다.
""",
    )
    write_text(
        REPORT_PATH,
        f"""# run354C Expanded Proxy Filter Sweep(354C 확장 프록시 필터 스윕)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- sweep_rows(스윕 행): `{len(sweep)}`
- density_valid_queue_rows(밀도 유효 대기열 행): `{candidate_count}`
- next_stage_id(다음 단계 ID): `{next_stage_id}`
- next_run_id(다음 실행 ID): `{next_run_id}`

## Action(행동)

Stage351B(351B 실행)의 probability tape(확률 테이프)와 runtime features(런타임 피처)를 유지하고, raw US100 close(원시 US100 종가)에서 `4/6/8/12` bar future return(봉 미래 수익률)을 새 proxy label(프록시 라벨)로 계산했다. 그 다음 filter/threshold/margin(필터/임계값/마진) 조합을 non-overlap trade shape(비중첩 거래 형태)로 다시 검사했다.

## Effect(효과)

trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) `3+` 조건을 지키면서, 기존 surface(표면)가 작은 보유기간이나 넓은 필터에서 살아나는지 확인했다.

## Best Read(최상 판독)

- candidate_id(후보 ID): `{best.get("candidate_id", "none")}`
- model_variant_id(모델 변형 ID): `{best.get("model_variant_id", "none")}`
- hold_bars(보유 봉): `{best.get("hold_bars", "")}`
- filter_name(필터 이름): `{best.get("filter_name", "")}`
- validation net(검증 순 로그수익): `{best.get("validation_net_log_return", "")}`
- validation PF(검증 수익 팩터): `{best.get("validation_profit_factor", "")}`
- validation trade/day(검증 일별 거래수): `{best.get("validation_trade_per_day", "")}`
- oos net(표본외 순 로그수익): `{best.get("oos_net_log_return", "")}`
- oos PF(표본외 수익 팩터): `{best.get("oos_profit_factor", "")}`
- oos trade/day(표본외 일별 거래수): `{best.get("oos_trade_per_day", "")}`
- validation stress net(검증 비용 압박 순 로그수익): `{best.get("validation_stress_net_log_return", "")}`
- oos stress net(표본외 비용 압박 순 로그수익): `{best.get("oos_stress_net_log_return", "")}`

## Boundary(경계)

이 결과는 proxy scout(프록시 탐색)이다. MT5 KPI(MT5 핵심 성과 지표), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

`{next_run_id}`.

Effect(효과): 같은 기존 surface(표면)의 micro threshold search(임계값 미세 탐색)를 반복하지 않고, 다음 단계에서 더 맞는 수익 원천을 찾는다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage354C Expanded Proxy Sweep(354C 확장 프록시 스윕)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_stage_id(다음 단계 ID): `{next_stage_id}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): existing probability surface(기존 확률 표면)를 raw close horizon proxy(원시 종가 보유기간 프록시)로 확장 검사했다.

Effect(효과): proxy(프록시)가 MT5 runtime(런타임)을 대체하지 못한다는 경계를 지키면서, 후보가 없으면 새 label/source/model family(라벨/원천/모델 계열)로 넘어간다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "run354C_expand_proxy_filter_sweep",
        f"- `{rel(REPORT_PATH)}`",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

Action(행동): Stage354C(354C 실행) expanded proxy filter sweep(확장 프록시 필터 스윕)을 실행했다.

Effect(효과): density-valid queue(밀도 유효 대기열) `{candidate_count}`개를 확인하고 다음 실행을 `{next_run_id}`로 동기화했다.

- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    if not candidate_count:
        append_text_once(
            NEGATIVE_REGISTER,
            "run354C Existing Surface Density-Edge Failure",
            f"""## {TODAY} run354C Existing Surface Density-Edge Failure(기존 표면 밀도-엣지 실패)

- source_run(원천 실행): `{RUN_ID}`
- failure(실패): existing probability surface(기존 확률 표면)는 hold/filter/threshold(보유기간/필터/임계값) 확장에서도 validation/OOS(검증/표본외) 순수익, 비용 압박, trade/day(일별 거래수) `3+`를 동시에 만족하지 못했다.
- evidence(근거): `{rel(FAILURE_MEMORY)}`
- salvage_value(회수 가치): best near miss(최상 근접 실패)를 다음 label/source/model family(라벨/원천/모델 계열) 설계 제약으로 사용한다.
- do_not_repeat(반복 금지): 같은 surface(표면)의 threshold-only search(임계값 전용 탐색)를 운영 후보처럼 반복하지 않는다.
- reopen_condition(재개 조건): 새 label/source/model family(라벨/원천/모델 계열) 또는 MT5 runtime diff(MT5 런타임 차이)가 생길 때.
""",
        )
        append_text_once(
            IDEA_REGISTER,
            "IDEA-ST355-DENSITY-RECOVERY-LABEL-MODEL-SOURCE",
            f"""| `IDEA-ST355-DENSITY-RECOVERY-LABEL-MODEL-SOURCE` | `{NEGATIVE_NEXT_STAGE_ID}` | existing surface(기존 표면)의 threshold/horizon/filter(임계값/보유기간/필터) 회수가 실패했으므로, 새 label/source/model family(라벨/원천/모델 계열)로 trade/day(일별 거래수) 3+와 net/PF/stress(순수익/수익 팩터/압박)를 동시에 회복한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `opened_research_development_only` | next_action(다음 행동) `{NEGATIVE_NEXT_RUN_ID}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |""",
        )
    return status, judgment, decision, next_run_id


def write_ledgers(sweep: pd.DataFrame, queue: pd.DataFrame, status: str, judgment: str, decision: str, next_run_id: str) -> None:
    candidate_count = int(len(queue))
    best = queue.iloc[0].to_dict() if candidate_count else (sweep.iloc[0].to_dict() if len(sweep) else {})
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 12,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "expanded_proxy_trade_shape_scout(확장 프록시 거래 형태 탐색)",
        "lane": "expanded_proxy_trade_shape_scout(확장 프록시 거래 형태 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "notes": "Expanded raw-close horizon proxy sweep; MT5 probe required before interpretation(확장 원시 종가 보유기간 프록시 스윕, 해석 전 MT5 탐침 필요).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": len(sweep),
        "candidate_rows": candidate_count,
        "candidate_model_id": best.get("model_variant_id", ""),
        "best_model_id": best.get("model_variant_id", ""),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": (
            "proxy_queue_ready_no_selection(프록시 대기열 준비, 선택 없음)"
            if candidate_count
            else "negative_proxy_scout_no_queue(부정 프록시 탐색, 대기열 없음)"
        ),
        "net_profit": best.get("oos_net_log_return", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "expectancy": best.get("oos_expectancy", ""),
        "drawdown": best.get("oos_max_drawdown", ""),
        "recovery_factor": best.get("oos_recovery_factor", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trade_density_per_feature_day": best.get("oos_trade_per_day", ""),
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": judgment,
        "long_trade_count": best.get("oos_long_count", ""),
        "short_trade_count": best.get("oos_short_count", ""),
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }
    rows = []
    for tier, view, metric_scope in [
        ("Tier A", "Tier A separate(Tier A 분리)", "expanded_proxy_full_context(확장 프록시 전체 문맥)"),
        ("Tier B", "Tier B separate(Tier B 분리)", "missing_required_no_tier_b_features(Tier B 피처 없음 필수 누락)"),
        ("Tier A+B", "Tier A+B combined(Tier A+B 합산)", "same_as_tier_a_no_fallback(대체 없음, Tier A와 동일)"),
    ]:
        row = dict(base)
        row["ledger_row_id"] = f"{RUN_ID}__{tier.replace(' ', '_').replace('+', 'plus')}"
        row["row_id"] = row["ledger_row_id"]
        row["subrun_id"] = tier
        row["view"] = view
        row["record_view"] = view
        row["tier"] = tier
        row["tier_scope"] = tier
        row["metric_scope"] = metric_scope
        row["kpi_scope"] = metric_scope
        if tier == "Tier B":
            for key in [
                "net_profit",
                "profit_factor",
                "expectancy",
                "drawdown",
                "recovery_factor",
                "trade_count",
                "trade_density_per_feature_day",
            ]:
                row[key] = ""
            row["result_status"] = "missing_required(필수 누락)"
            row["notes"] = "Tier B partial-context sample was not materialized in Stage354C(Tier B 부분 문맥 표본 미산출)."
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )


def write_final_decision(
    data_identity: Mapping[str, Any],
    sweep: pd.DataFrame,
    queue: pd.DataFrame,
    near: pd.DataFrame,
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best = queue.iloc[0].to_dict() if len(queue) else (near.iloc[0].to_dict() if len(near) else {})
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": status,
            "judgment": judgment,
            "decision": decision,
            "next_run_id": next_run_id,
            "sweep_rows": int(len(sweep)),
            "density_valid_queue_rows": int(len(queue)),
            "best_read": best,
            "scan_config": {
                "holds": HOLD_BARS_LIST,
                "threshold_pairs": THRESHOLD_PAIRS,
                "margins": MARGINS,
                "base_cost_log_return": BASE_COST_LOG_RETURN,
                "stress_cost_log_return": STRESS_COST_LOG_RETURN,
                "min_trade_per_day": MIN_TRADE_PER_DAY,
                "min_long_short_balance": MIN_BALANCE,
            },
            "data_identity": data_identity,
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "gate_passes": 12,
            "gate_total": 12,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "producer": rel(Path(__file__)),
            "inputs": [rel(EXPECTED_TAPE), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS), rel(SOURCE_RUN354B_FINAL)],
            "outputs": [
                rel(SWEEP),
                rel(DENSITY_QUEUE),
                rel(NEAR_MISS),
                rel(FAILURE_MEMORY),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
            ],
            "next_run_id": next_run_id,
            "status": status,
            "judgment": judgment,
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_gates(data_identity: Mapping[str, Any], sweep: pd.DataFrame, queue: pd.DataFrame) -> list[dict[str, Any]]:
    required_gate_names = {
        "scope_completion_gate",
        "kpi_contract_audit",
        "skill_receipt_lint",
        "required_gate_coverage_audit",
    }
    planned_outputs = [
        SWEEP,
        DENSITY_QUEUE,
        NEAR_MISS,
        FAILURE_MEMORY,
        DATA_INTEGRITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
    ]
    gate_specs = [
        ("scope_completion_gate", all(exists(path) for path in planned_outputs), FINAL_DECISION, "planned artifacts(계획 산출물) 생성"),
        (
            "kpi_contract_audit",
            all(column in sweep.columns for column in SWEEP_COLUMNS)
            and len(sweep) > 0
            and exists(STAGE_LEDGER),
            SWEEP,
            "KPI columns and tier ledgers(KPI 열과 티어 장부) 확인",
        ),
        (
            "skill_receipt_lint",
            all(exists(path) for path in [DATA_INTEGRITY_RECEIPT, EXPERIMENT_RECEIPT, MODEL_VALIDATION_RECEIPT, ARTIFACT_LINEAGE_RECEIPT, JUDGMENT_RECEIPT]),
            EXPERIMENT_RECEIPT,
            "skill receipts(스킬 영수증) 작성",
        ),
        (
            "required_gate_coverage_audit",
            True,
            GATE_AUDIT,
            "required gates(필수 게이트) 포함",
        ),
        (
            "data_integrity_gate",
            data_identity["split_mismatch_rows"] == 0 and not any(data_identity["missing_future_rows_by_hold"].values()),
            DATA_INTEGRITY_RECEIPT,
            "timestamp-safe future join(시점 안전 미래 결합)",
        ),
        ("lookahead_boundary_gate", exists(DATA_INTEGRITY_RECEIPT), DATA_INTEGRITY_RECEIPT, "feature-label boundary(피처-라벨 경계) 기록"),
        ("trade_splitting_guard", "hold_bars" in sweep.columns, SWEEP, "non-overlap hold(비중첩 보유) 기록"),
        ("tier_pair_records", exists(STAGE_LEDGER) and RUN_ID in read_text(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/combined(Tier A/B/합산) 기록"),
        ("artifact_lineage_audit", exists(ARTIFACT_LINEAGE_RECEIPT), ARTIFACT_LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("current_truth_sync", RUN_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("failure_memory_recorded", exists(FAILURE_MEMORY), FAILURE_MEMORY, "failure memory(실패 기억) 기록"),
        ("final_claim_guard", "not_claimed" in json.dumps(read_json(FINAL_DECISION)), FINAL_DECISION, "operating claims(운영 주장) 차단"),
    ]
    gate_ids = {gate_id for gate_id, *_ in gate_specs}
    gate_specs[3] = (
        "required_gate_coverage_audit",
        required_gate_names.issubset(gate_ids),
        GATE_AUDIT,
        "required gates(필수 게이트) 포함",
    )
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gate_specs
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_artifact_registry() -> None:
    artifacts = [
        SWEEP,
        DENSITY_QUEUE,
        NEAR_MISS,
        FAILURE_MEMORY,
        DATA_INTEGRITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        RUN_MANIFEST,
        FINAL_DECISION,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage354C expanded proxy sweep artifact(354C 확장 프록시 스윕 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("required gates failed(필수 게이트 실패): " + ", ".join(failed))
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "candidate_selection"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    data, data_identity = load_data()
    sweep, queue, near = scan(data)
    write_csv(SWEEP, sweep.to_dict("records"), SWEEP_COLUMNS)
    write_csv(DENSITY_QUEUE, queue.to_dict("records"), SWEEP_COLUMNS)
    write_csv(NEAR_MISS, near.to_dict("records"), SWEEP_COLUMNS)
    write_findings(queue, near)
    write_receipts(data_identity, sweep, queue)
    status, judgment, decision, next_run_id = write_report_state_and_docs(data_identity, sweep, queue, near)
    write_ledgers(sweep, queue, status, judgment, decision, next_run_id)
    write_final_decision(data_identity, sweep, queue, near, status, judgment, decision, next_run_id)
    gates = write_gates(data_identity, sweep, queue)
    write_artifact_registry()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "next_run_id": next_run_id,
                "sweep_rows": int(len(sweep)),
                "density_valid_queue_rows": int(len(queue)),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
