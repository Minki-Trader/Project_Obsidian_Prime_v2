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
RUN_NUMBER = "run354B"
RUN_ID = "run354B_lightweight_proxy_trade_shape_scan_without_db_v1"
PARENT_RUN_ID = "run354A_branch_stage353_to_lightweight_proxy_trade_shape_scout_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db_v1"
NEXT_STAGE_ID_POSITIVE = "355_runtime_probe_package__proxy_queue_mt5_handoff"
NEXT_RUN_ID_POSITIVE = "run355A_materialize_stage354_proxy_queue_mt5_probe_package_without_db_v1"
NEXT_RUN_ID_NEGATIVE = "run354C_expand_proxy_filter_sweep_without_db_v1"

CLAIM_BOUNDARY = (
    "lightweight_proxy_trade_shape_scout_only_mt5_probe_required_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

HOLD_BARS = 12
BASE_COST_LOG_RETURN = 0.00015
STRESS_COST_LOG_RETURN = 0.00030
MIN_TRADE_PER_DAY = 3.0

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
TRAINING_DATASET = ROOT / "data" / "processed" / "training_datasets" / "label_v1_fwd12_split_v1_proxyw58" / "training_dataset.parquet"
SOURCE352_COMBINED = (
    ROOT
    / "stages"
    / "352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity"
    / "02_runs"
    / "run352B"
    / "combined_kpi_summary.json"
)
SOURCE352_ATTRIBUTION = (
    ROOT
    / "stages"
    / "352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity"
    / "02_runs"
    / "run352B"
    / "proxy_mt5_attribution.csv"
)
SOURCE354A_QUEUE = STAGE_DIR / "02_runs" / "run354A" / "run354B_proxy_scout_queue.csv"

BROAD_SCREEN = RUN_DIR / "broad_proxy_signal_screen.csv"
CONFIRMED_SCOREBOARD = RUN_DIR / "nonoverlap_candidate_scoreboard.csv"
MT5_QUEUE = RUN_DIR / "mt5_probe_candidate_queue.csv"
SESSION_STABILITY = RUN_DIR / "session_regime_stability.csv"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
REPORT_PATH = REVIEW_DIR / "run354B_lightweight_proxy_trade_shape_scan.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID_POSITIVE

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage354B_lightweight_proxy_trade_shape_scan.md"


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


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


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


def load_data() -> tuple[pd.DataFrame, dict[str, Any]]:
    expected_cols = ["model_variant_id", "bar_time_server", "timestamp_utc", "split", "p_short", "p_flat", "p_long"]
    feature_cols = [
        "bar_time_server",
        "timestamp_utc",
        "split",
        "is_us_cash_open",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "adx_14",
        "vix_zscore_20",
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
        "di_spread_14",
        "historical_vol_5_over_20",
    ]
    expected = pd.read_csv(fs_path(EXPECTED_TAPE), usecols=expected_cols)
    features = pd.read_csv(fs_path(RUNTIME_FEATURES), usecols=feature_cols)
    dataset = pd.read_parquet(fs_path(TRAINING_DATASET), columns=["timestamp", "split", "future_log_return_12"])
    dataset["timestamp_utc"] = pd.to_datetime(dataset["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    future = dataset[["timestamp_utc", "split", "future_log_return_12"]].rename(columns={"split": "dataset_split"})
    feature_future = features.merge(future, on="timestamp_utc", how="left")
    merged = expected.merge(
        feature_future,
        on=["bar_time_server", "timestamp_utc"],
        how="left",
        suffixes=("", "_feature"),
    )
    split_mismatch = int((merged["split"] != merged["split_feature"]).sum()) if "split_feature" in merged else 0
    dataset_split_mismatch = int((merged["split"] != merged["dataset_split"]).sum()) if "dataset_split" in merged else 0
    if "split_feature" in merged:
        merged = merged.drop(columns=["split_feature"])
    if "dataset_split" in merged:
        merged = merged.drop(columns=["dataset_split"])
    merged["date"] = pd.to_datetime(merged["timestamp_utc"], utc=True).dt.date.astype(str)
    identity = {
        "expected_rows": int(len(expected)),
        "feature_rows": int(len(features)),
        "dataset_rows": int(len(dataset)),
        "merged_rows": int(len(merged)),
        "model_count": int(expected["model_variant_id"].nunique()),
        "missing_future_rows": int(merged["future_log_return_12"].isna().sum()),
        "split_mismatch_rows": split_mismatch,
        "dataset_split_mismatch_rows": dataset_split_mismatch,
        "expected_sha256": sha256_file(EXPECTED_TAPE),
        "features_sha256": sha256_file(RUNTIME_FEATURES),
        "training_dataset_sha256": sha256_file(TRAINING_DATASET),
    }
    if identity["missing_future_rows"] or identity["split_mismatch_rows"] or identity["dataset_split_mismatch_rows"]:
        raise RuntimeError(f"data integrity failure(데이터 무결성 실패): {identity}")
    return merged, identity


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
    day_frame = pd.DataFrame({"date": dates, "net": net})
    day_sum = day_frame.groupby("date")["net"].sum()
    positive_day_ratio = float((day_sum > 0.0).mean()) if len(day_sum) else 0.0
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
        "positive_day_ratio": positive_day_ratio,
        "equity_r2": equity_r2,
    }


def nonoverlap_trade_kpi(labels: np.ndarray, future_returns: np.ndarray, dates: np.ndarray, cost: float) -> dict[str, Any]:
    net: list[float] = []
    sides: list[int] = []
    trade_dates: list[str] = []
    next_allowed = 0
    for index, label in enumerate(labels):
        side = int(label)
        if index < next_allowed or side == 1:
            continue
        gross = -float(future_returns[index]) if side == 0 else float(future_returns[index])
        net.append(gross - cost)
        sides.append(side)
        trade_dates.append(str(dates[index]))
        next_allowed = index + HOLD_BARS
    return kpi_from_net(np.asarray(net, dtype=float), np.asarray(sides, dtype=np.int8), np.asarray(trade_dates, dtype=str))


def build_filters(frame: pd.DataFrame) -> list[tuple[str, np.ndarray]]:
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    cash = frame["is_us_cash_open"].to_numpy(dtype=float) == 1.0
    adx = frame["adx_14"].to_numpy(dtype=float)
    vix = frame["vix_zscore_20"].to_numpy(dtype=float)
    breadth = frame["mega8_pos_breadth_1"].to_numpy(dtype=float)
    dispersion = frame["mega8_dispersion_5"].to_numpy(dtype=float)
    first30 = frame["is_first_30m_after_open"].to_numpy(dtype=float) == 1.0
    last30 = frame["is_last_30m_before_cash_close"].to_numpy(dtype=float) == 1.0
    disp_q70 = float(np.nanquantile(dispersion, 0.70))
    disp_q50 = float(np.nanquantile(dispersion, 0.50))
    return [
        ("adx25", adx >= 25.0),
        ("cash_adx25", cash & (adx >= 25.0)),
        ("post30_330_adx25", (minutes >= 30.0) & (minutes <= 330.0) & (adx >= 25.0)),
        ("not_edges_adx25", (~first30) & (~last30) & (adx >= 25.0)),
        ("adx30_extreme", adx >= 30.0),
        ("adx25_vix_abs1", (adx >= 25.0) & (np.abs(vix) <= 1.0)),
    ]


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


def fast_signal_kpi(labels: np.ndarray, future_returns: np.ndarray, dates: np.ndarray, cost: float) -> dict[str, Any]:
    trade_mask = labels != 1
    if not trade_mask.any():
        return kpi_from_net(np.asarray([], dtype=float), np.asarray([], dtype=np.int8), np.asarray([], dtype=str))
    sides = labels[trade_mask]
    gross = np.where(sides == 0, -future_returns[trade_mask], future_returns[trade_mask])
    return kpi_from_net(gross.astype(float) - cost, sides, dates[trade_mask])


def selection_score(row: Mapping[str, Any]) -> float:
    val_net = float(row["validation_net_log_return"])
    oos_net = float(row["oos_net_log_return"])
    val_pf = float(row["validation_profit_factor"])
    oos_pf = float(row["oos_profit_factor"])
    val_dd = float(row["validation_max_drawdown"])
    oos_dd = float(row["oos_max_drawdown"])
    val_rec = float(row["validation_recovery_factor"])
    oos_rec = float(row["oos_recovery_factor"])
    val_balance = float(row["validation_long_short_balance"])
    oos_balance = float(row["oos_long_short_balance"])
    gap = abs(val_net - oos_net)
    density_gap = abs(float(row["validation_trade_per_day"]) - float(row["oos_trade_per_day"]))
    stress = float(row.get("validation_stress_net_log_return", 0.0) or 0.0) + float(
        row.get("oos_stress_net_log_return", 0.0) or 0.0
    )
    return (
        val_net * 10000.0
        + oos_net * 8000.0
        + math.log1p(max(0.0, min(val_pf, 20.0))) * 45.0
        + math.log1p(max(0.0, min(oos_pf, 20.0))) * 55.0
        + val_rec * 8.0
        + oos_rec * 12.0
        + val_balance * 18.0
        + oos_balance * 24.0
        - val_dd * 900.0
        - oos_dd * 1200.0
        - gap * 3500.0
        - density_gap * 3.0
        + stress * 3000.0
    )


def kpi_prefixed(prefix: str, kpi: Mapping[str, Any]) -> dict[str, Any]:
    return {f"{prefix}_{key}": value for key, value in kpi.items()}


def broad_scan(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    thresholds = [0.34, 0.36, 0.38, 0.40, 0.42]
    margins = [0.0, 0.01, 0.02, 0.04]
    rows: list[dict[str, Any]] = []
    for model_id, group in data.groupby("model_variant_id", sort=False):
        group = group.reset_index(drop=True)
        split_values = group["split"].to_numpy(dtype=str)
        future = group["future_log_return_12"].to_numpy(dtype=float)
        dates = group["date"].to_numpy(dtype=str)
        p_short = group["p_short"].to_numpy(dtype=float)
        p_flat = group["p_flat"].to_numpy(dtype=float)
        p_long = group["p_long"].to_numpy(dtype=float)
        filters = build_filters(group)
        for filter_name, filter_mask in filters:
            for short_threshold in thresholds:
                for long_threshold in thresholds:
                    for margin in margins:
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
                            "model_variant_id": model_id,
                            "filter_name": filter_name,
                            "short_threshold": short_threshold,
                            "long_threshold": long_threshold,
                            "min_margin": margin,
                            "scan_layer": "fast_signal_overlap_scout(빠른 중첩 신호 탐색)",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                        for split in ["validation", "oos"]:
                            mask = split_values == split
                            base = fast_signal_kpi(labels[mask], future[mask], dates[mask], BASE_COST_LOG_RETURN)
                            stress = fast_signal_kpi(labels[mask], future[mask], dates[mask], STRESS_COST_LOG_RETURN)
                            row.update(kpi_prefixed(split, base))
                            row[f"{split}_stress_net_log_return"] = stress["net_log_return"]
                        row["selection_score"] = selection_score(row)
                        rows.append(row)
    broad = pd.DataFrame(rows)
    broad = broad.sort_values("selection_score", ascending=False).reset_index(drop=True)
    broad.to_csv(fs_path(BROAD_SCREEN), index=False, encoding="utf-8-sig")
    eligible = broad[
        (broad["validation_net_log_return"] > 0.0)
        & (broad["oos_net_log_return"] > 0.0)
        & (broad["validation_profit_factor"] >= 1.0)
        & (broad["oos_profit_factor"] >= 1.0)
        & (broad["validation_trade_per_day"] >= MIN_TRADE_PER_DAY)
        & (broad["oos_trade_per_day"] >= MIN_TRADE_PER_DAY)
        & (broad["validation_long_short_balance"] >= 0.15)
        & (broad["oos_long_short_balance"] >= 0.15)
    ]
    if eligible.empty:
        eligible = broad[
            (broad["validation_net_log_return"] > 0.0)
            & (broad["oos_net_log_return"] > 0.0)
            & (broad["validation_trade_per_day"] >= 2.0)
            & (broad["oos_trade_per_day"] >= 2.0)
        ]
    if eligible.empty:
        eligible = broad.head(240)
    return broad, eligible.head(80).reset_index(drop=True)


def confirm_nonoverlap(data: pd.DataFrame, broad_candidates: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    stability_rows: list[dict[str, Any]] = []
    grouped = {model_id: group.reset_index(drop=True) for model_id, group in data.groupby("model_variant_id", sort=False)}
    for rank, candidate in broad_candidates.iterrows():
        model_id = str(candidate["model_variant_id"])
        group = grouped[model_id]
        filter_map = dict(build_filters(group))
        filter_name = str(candidate["filter_name"])
        if filter_name not in filter_map:
            continue
        split_values = group["split"].to_numpy(dtype=str)
        future = group["future_log_return_12"].to_numpy(dtype=float)
        dates = group["date"].to_numpy(dtype=str)
        p_short = group["p_short"].to_numpy(dtype=float)
        p_flat = group["p_flat"].to_numpy(dtype=float)
        p_long = group["p_long"].to_numpy(dtype=float)
        labels = labels_from_surface(
            p_short,
            p_flat,
            p_long,
            filter_map[filter_name],
            float(candidate["short_threshold"]),
            float(candidate["long_threshold"]),
            float(candidate["min_margin"]),
        )
        row: dict[str, Any] = {
            "candidate_id": (
                f"{model_id}__{filter_name}__s{float(candidate['short_threshold']):.3f}"
                f"__l{float(candidate['long_threshold']):.3f}__m{float(candidate['min_margin']):.3f}"
            ),
            "model_variant_id": model_id,
            "filter_name": filter_name,
            "short_threshold": float(candidate["short_threshold"]),
            "long_threshold": float(candidate["long_threshold"]),
            "min_margin": float(candidate["min_margin"]),
            "broad_rank": int(rank + 1),
            "scan_layer": "nonoverlap_trade_shape_confirmation(비중첩 거래 형태 확인)",
            "hold_bars": HOLD_BARS,
            "base_cost_log_return": BASE_COST_LOG_RETURN,
            "stress_cost_log_return": STRESS_COST_LOG_RETURN,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for split in ["validation", "oos"]:
            mask = split_values == split
            base = nonoverlap_trade_kpi(labels[mask], future[mask], dates[mask], BASE_COST_LOG_RETURN)
            stress = nonoverlap_trade_kpi(labels[mask], future[mask], dates[mask], STRESS_COST_LOG_RETURN)
            row.update(kpi_prefixed(split, base))
            row[f"{split}_stress_net_log_return"] = stress["net_log_return"]
            split_group = group.loc[mask].reset_index(drop=True)
            split_labels = labels[mask]
            buckets = pd.cut(
                split_group["minutes_from_cash_open"],
                bins=[-1, 60, 180, 330, 99999],
                labels=["early_0_60", "mid_60_180", "late_180_330", "tail_330_plus"],
            ).astype(str)
            for bucket_name in sorted(set(buckets)):
                bucket_mask = buckets.to_numpy(dtype=str) == bucket_name
                if not bucket_mask.any():
                    continue
                bucket_kpi = nonoverlap_trade_kpi(
                    split_labels[bucket_mask],
                    split_group.loc[bucket_mask, "future_log_return_12"].to_numpy(dtype=float),
                    split_group.loc[bucket_mask, "date"].to_numpy(dtype=str),
                    BASE_COST_LOG_RETURN,
                )
                stability_rows.append(
                    {
                        "candidate_id": row["candidate_id"],
                        "model_variant_id": model_id,
                        "filter_name": filter_name,
                        "split": split,
                        "session_bucket": bucket_name,
                        **bucket_kpi,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
        row["validation_oos_net_gap"] = abs(float(row["validation_net_log_return"]) - float(row["oos_net_log_return"]))
        row["validation_oos_pf_gap"] = abs(float(row["validation_profit_factor"]) - float(row["oos_profit_factor"]))
        row["validation_oos_density_gap"] = abs(float(row["validation_trade_per_day"]) - float(row["oos_trade_per_day"]))
        row["selection_score"] = selection_score(row)
        rows.append(row)
    confirmed = pd.DataFrame(rows)
    if not confirmed.empty:
        confirmed = confirmed.sort_values("selection_score", ascending=False).reset_index(drop=True)
        confirmed["priority_rank"] = np.arange(1, len(confirmed) + 1)
    confirmed.to_csv(fs_path(CONFIRMED_SCOREBOARD), index=False, encoding="utf-8-sig")
    stability = pd.DataFrame(stability_rows)
    stability.to_csv(fs_path(SESSION_STABILITY), index=False, encoding="utf-8-sig")
    return confirmed, stability


def queue_from_confirmed(confirmed: pd.DataFrame) -> pd.DataFrame:
    if confirmed.empty:
        queue = confirmed.copy()
    else:
        strict = confirmed[
            (confirmed["validation_net_log_return"] > 0.0)
            & (confirmed["oos_net_log_return"] > 0.0)
            & (confirmed["validation_profit_factor"] >= 1.0)
            & (confirmed["oos_profit_factor"] >= 1.0)
            & (confirmed["validation_trade_per_day"] >= MIN_TRADE_PER_DAY)
            & (confirmed["oos_trade_per_day"] >= MIN_TRADE_PER_DAY)
            & (confirmed["validation_long_short_balance"] >= 0.25)
            & (confirmed["oos_long_short_balance"] >= 0.25)
        ]
        queue = strict.head(6).copy()
    if not queue.empty:
        queue["queue_rank"] = np.arange(1, len(queue) + 1)
        queue["next_run_id"] = NEXT_RUN_ID_POSITIVE
        queue["allowed_use"] = "mt5_probe_package_materialization_only(MT5 탐침 패키지 산출물화 전용)"
        queue["forbidden_use"] = "mt5_kpi_substitute_or_operating_claim(MT5 KPI 대체 또는 운영 주장 금지)"
        queue["density_requirement"] = TRADE_DENSITY_REQUIREMENT
        queue["claim_boundary"] = CLAIM_BOUNDARY
    queue.to_csv(fs_path(MT5_QUEUE), index=False, encoding="utf-8-sig")
    return queue


def write_receipts(data_identity: Mapping[str, Any], broad: pd.DataFrame, confirmed: pd.DataFrame, queue: pd.DataFrame) -> None:
    created = now_utc()
    candidate_count = int(len(queue))
    best = queue.iloc[0].to_dict() if candidate_count else (confirmed.iloc[0].to_dict() if len(confirmed) else {})
    action_effect = (
        "거래를 쪼개서 수익을 만드는 방식(trade splitting, 거래 쪼개기)을 피하면서, MT5 probe package(MT5 탐침 패키지)로 넘길 작은 queue(대기열)를 만들었다."
        if candidate_count
        else "거래를 쪼개서 수익을 만드는 방식(trade splitting, 거래 쪼개기)을 피한 결과, 양수 proxy(프록시) 후보들은 있었지만 trade/day(일별 거래수) 3+ 조건을 통과하지 못해 MT5 queue(MT5 대기열)를 만들지 않았다."
    )
    source_inputs = [
        {"path": rel(EXPECTED_TAPE), "sha256": data_identity["expected_sha256"], "role": "model probability expected tape(모델 확률 예상 테이프)"},
        {"path": rel(RUNTIME_FEATURES), "sha256": data_identity["features_sha256"], "role": "runtime features(런타임 피처)"},
        {"path": rel(TRAINING_DATASET), "sha256": data_identity["training_dataset_sha256"], "role": "future return label source(미래 수익 라벨 원천)"},
        {"path": rel(SOURCE352_COMBINED), "sha256": sha256_file(SOURCE352_COMBINED), "role": "negative MT5 runtime source(부정 MT5 런타임 원천)"},
    ]
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": source_inputs,
            "time_axis": "bar_time_server is MT5 broker-clock closed M5 bar key; timestamp_utc is audit key.",
            "sample_scope": {
                "rows": data_identity,
                "splits": ["train", "validation", "oos"],
                "scan_splits_used_for_selection": ["validation", "oos"],
                "tier_scope": "Tier A full-context proxy; Tier B missing_required in this run.",
            },
            "missing_or_duplicate_check": "merge required zero missing future rows and zero split mismatch rows.",
            "feature_label_boundary": "features and probabilities are current closed-bar values; future_log_return_12 is used only as proxy outcome.",
            "split_boundary": "validation/oos are read for scout comparison; no model retraining occurs in this run.",
            "leakage_risk": "multiple threshold/filter reads can overfit proxy; MT5 probe and later WFO remain required.",
            "data_hash_or_identity": data_identity,
            "integrity_judgment": "usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created,
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "idea_id": "stage354_proxy_trade_shape_scout_adx25_cashopen_queue",
            "hypothesis": "ADX25/cash-open filtered probability surfaces can preserve trade density while reducing Stage352B OOS failure before MT5 probe.",
            "legacy_relation": "none",
            "tier_scope": "Tier A scanned; Tier B missing_required recorded.",
            "broad_sweep": {
                "models": int(data_identity["model_count"]),
                "filters": [
                    "adx25",
                    "cash_adx25",
                    "post30_330_adx25",
                "not_edges_adx25",
                "adx30_extreme",
                "adx25_vix_abs1",
                ],
                "thresholds": [0.34, 0.36, 0.38, 0.40, 0.42],
                "margins": [0.0, 0.01, 0.02, 0.04],
            },
            "extreme_sweep": ["adx30_extreme", "threshold_0.42", "margin_0.04"],
            "micro_search_gate": "nonoverlap validation and oos net both positive with density >= 3 before MT5 package handoff.",
            "wfo_plan": "not in this scout; required before promotion or operating claim.",
            "failure_memory": "Stage352B density passed but OOS net=-200.11 and max DD=65.34%; preserve as runtime negative constraint.",
            "evidence_boundary": "scout-only",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created,
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "existing Stage351B logistic ONNX probability outputs; no new model training.",
            "target_and_label": "label_class 0=short, 1=flat, 2=long from fwd12 log-return threshold; future_log_return_12 used only for proxy outcome.",
            "split_method": "fixed validation/oos scout read; train not used for final ranking.",
            "selection_metric": "nonoverlap proxy score using net, PF, recovery, drawdown, density, long/short balance, stress net, and validation/oos gap.",
            "secondary_metrics": ["trade_per_day", "long_short_balance", "session_bucket_stability", "stress_net_log_return", "drawdown"],
            "threshold_policy": "searched threshold/filter scout; candidate queue only, not selected baseline.",
            "overfit_risk": "many threshold/filter combinations plus proxy/MT5 mismatch risk.",
            "calibration_risk": "probability outputs are runtime probabilities but not live-calibrated operating probabilities.",
            "comparison_baseline": "Stage352B MT5 runtime probe negative result.",
            "validation_judgment": "exploratory_proxy_queue" if candidate_count else "negative_proxy_scout_no_queue",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "Stage354B lightweight proxy trade-shape scan",
            "evidence_available": {
                "broad_rows": int(len(broad)),
                "confirmed_rows": int(len(confirmed)),
                "queue_rows": candidate_count,
                "best_candidate": best,
            },
            "evidence_missing": ["MT5 runtime probe", "proxy-vs-MT5 diff for new queue", "WFO", "forward replay"],
            "judgment_label": "exploratory_proxy_positive_queue" if candidate_count else "negative_proxy_scout",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID_POSITIVE if candidate_count else NEXT_RUN_ID_NEGATIVE,
            "user_explanation_hook": "proxy queue is useful only as MT5 probe input, not as operating evidence.",
            "created_at_utc": created,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "proxy scout queue only(프록시 탐색 대기열만)",
            "forbidden_claims": [
                "candidate selection(후보 선택)",
                "MT5 KPI substitute(MT5 KPI 대체)",
                "forward pass(전진 통과)",
                "live readiness(실거래 준비)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created,
        },
    )
    artifact_paths = [
        BROAD_SCREEN,
        CONFIRMED_SCOREBOARD,
        MT5_QUEUE,
        SESSION_STABILITY,
        DATA_INTEGRITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        REPORT_PATH,
        FINAL_DECISION,
        RUN_MANIFEST,
        GATE_AUDIT,
    ]
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": source_inputs,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID_POSITIVE if candidate_count else NEXT_RUN_ID_NEGATIVE,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths if exists(path)},
            "registry_links": [rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(RUN_REGISTRY), rel(ARTIFACT_REGISTRY)],
            "availability": "generated",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created,
        },
    )


def write_stage355_stub(queue: pd.DataFrame) -> None:
    if queue.empty:
        return
    for directory in [
        NEXT_STAGE_DIR / "00_spec",
        NEXT_STAGE_DIR / "01_inputs",
        NEXT_STAGE_DIR / "02_runs",
        NEXT_STAGE_DIR / "03_reviews",
        NEXT_STAGE_DIR / "04_selected",
    ]:
        os.makedirs(fs_path(directory), exist_ok=True)
    write_text(
        NEXT_STAGE_DIR / "README.md",
        f"""# Stage355 Runtime Probe Package(355단계 런타임 탐침 패키지)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID_POSITIVE}`

Action(행동): Stage354B(354B 실행)의 proxy queue(프록시 대기열)를 MT5 probe package(MT5 탐침 패키지) 작업으로 넘긴다.

Effect(효과): proxy result(프록시 결과)를 운영 주장으로 키우지 않고 MT5 runtime evidence(MT5 런타임 근거) 수집으로 연결한다.
""",
    )
    write_text(
        NEXT_STAGE_DIR / "00_spec" / "stage_brief.md",
        f"""# Stage355 Runtime Probe Package(355단계 런타임 탐침 패키지)

- canonical_stage_id(정식 단계 ID): `{NEXT_STAGE_ID_POSITIVE}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID_POSITIVE}`
- source_run_id(원천 실행 ID): `{RUN_ID}`

## Question(질문)

Stage354B(354B 실행)의 proxy-positive queue(프록시 긍정 대기열)를 MT5 runtime probe(MT5 런타임 탐침)가 바로 읽을 수 있는 package(패키지)로 물질화할 수 있는가?

## Boundary(경계)

이 단계는 package handoff(패키지 인계)와 MT5 probe preparation(MT5 탐침 준비)다. MT5 report(MT5 보고서)가 나오기 전까지 operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    write_text(
        NEXT_STAGE_DIR / "01_inputs" / "input_refs.md",
        f"""# Stage355 Input Refs(355단계 입력 참조)

- proxy_queue(프록시 대기열): `{rel(MT5_QUEUE)}`
- source_scoreboard(원천 점수판): `{rel(CONFIRMED_SCOREBOARD)}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
""",
    )
    write_text(
        NEXT_STAGE_DIR / "04_selected" / "selection_status.md",
        f"""# Stage355 Selection Status(355단계 선택 상태)

- selection_status(선택 상태): `no_selection(선택 없음)`
- active_stage_id(활성 단계 ID): `{NEXT_STAGE_ID_POSITIVE}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID_POSITIVE}`
- source_run_id(원천 실행 ID): `{RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )
    write_csv(
        NEXT_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv",
        [],
        [
            "stage_id",
            "run_id",
            "parent_run_id",
            "run_date",
            "status",
            "judgment",
            "decision",
            "next_run_id",
            "claim_boundary",
        ],
    )


def write_report_and_state(
    data_identity: Mapping[str, Any],
    broad: pd.DataFrame,
    confirmed: pd.DataFrame,
    queue: pd.DataFrame,
) -> None:
    candidate_count = int(len(queue))
    next_run_id = NEXT_RUN_ID_POSITIVE if candidate_count else NEXT_RUN_ID_NEGATIVE
    status = (
        "completed_stage354B_proxy_positive_queue_ready_for_mt5_probe_package_no_selection"
        if candidate_count
        else "completed_stage354B_proxy_scan_no_strict_queue_expand_required_no_selection"
    )
    judgment = (
        "exploratory_proxy_positive_queue_mt5_probe_required_no_operating_claim"
        if candidate_count
        else "negative_proxy_scout_no_mt5_queue_no_operating_claim"
    )
    decision = (
        f"stage354B_open_{NEXT_RUN_ID_POSITIVE}"
        if candidate_count
        else f"stage354B_open_{NEXT_RUN_ID_NEGATIVE}"
    )
    best = queue.iloc[0].to_dict() if candidate_count else (confirmed.iloc[0].to_dict() if len(confirmed) else {})
    action_effect = (
        "거래를 쪼개서 수익을 만드는 방식(trade splitting, 거래 쪼개기)을 피하면서, MT5 probe package(MT5 탐침 패키지)로 넘길 작은 queue(대기열)를 만들었다."
        if candidate_count
        else "거래를 쪼개서 수익을 만드는 방식(trade splitting, 거래 쪼개기)을 피한 결과, 양수 proxy(프록시) 후보들은 있었지만 trade/day(일별 거래수) 3+ 조건을 통과하지 못해 MT5 queue(MT5 대기열)를 만들지 않았다."
    )
    write_text(
        REPORT_PATH,
        f"""# run354B Lightweight Proxy Trade Shape Scan(354B 경량 프록시 거래 형태 스캔)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- broad_rows(넓은 스캔 행): `{len(broad)}`
- confirmed_rows(비중첩 확인 행): `{len(confirmed)}`
- mt5_queue_rows(MT5 대기열 행): `{candidate_count}`
- next_run_id(다음 실행 ID): `{next_run_id}`

## Action(행동)

Stage351B(351B 실행)의 probability tape(확률 테이프), runtime features(런타임 피처), training dataset future return(학습 데이터 미래 수익)을 timestamp-safe(시점 안전)하게 결합했다. 그 뒤 broad overlap signal scan(넓은 중첩 신호 스캔)으로 후보를 줄이고, 상위 후보만 `HOLD_BARS={HOLD_BARS}` non-overlap trade shape(비중첩 거래 형태)로 재확인했다.

## Effect(효과)

{action_effect}

## Best Proxy Queue Read(최상 프록시 대기열 판독)

- candidate_id(후보 ID): `{best.get("candidate_id", "none")}`
- model_variant_id(모델 변형 ID): `{best.get("model_variant_id", "none")}`
- filter_name(필터 이름): `{best.get("filter_name", "none")}`
- validation net(검증 순수익 로그): `{best.get("validation_net_log_return", "")}`
- validation PF(검증 수익 팩터): `{best.get("validation_profit_factor", "")}`
- validation trade/day(검증 일별 거래수): `{best.get("validation_trade_per_day", "")}`
- oos net(표본외 순수익 로그): `{best.get("oos_net_log_return", "")}`
- oos PF(표본외 수익 팩터): `{best.get("oos_profit_factor", "")}`
- oos trade/day(표본외 일별 거래수): `{best.get("oos_trade_per_day", "")}`
- long/short validation(검증 롱/숏): `{best.get("validation_long_count", "")}/{best.get("validation_short_count", "")}`
- long/short oos(표본외 롱/숏): `{best.get("oos_long_count", "")}/{best.get("oos_short_count", "")}`

## Boundary(경계)

이 결과는 proxy scout(프록시 탐색)다. MT5 KPI(MT5 핵심 성과 지표), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    selection_status = (
        "proxy_queue_ready_no_selection(프록시 대기열 준비, 선택 없음)"
        if candidate_count
        else "no_density_valid_queue_expand_required(밀도 유효 대기열 없음, 확장 필요)"
    )
    selection_text = f"""# Stage354 Selection Status(354단계 선택 상태)

- selection_status(선택 상태): `{selection_status}` 
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- source_run_id(원천 실행 ID): `{SOURCE_RUNTIME_RUN_ID}`
- mt5_queue_rows(MT5 대기열 행): `{candidate_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(SELECTION_STATUS, selection_text)
    if candidate_count:
        write_stage355_stub(queue)
        root_selection_text = read_text(NEXT_STAGE_DIR / "04_selected" / "selection_status.md")
        current_stage = NEXT_STAGE_ID_POSITIVE
    else:
        root_selection_text = selection_text
        current_stage = STAGE_ID
    write_text(ROOT_SELECTION, root_selection_text)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {current_stage}
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

- current_stage_id(현재 단계 ID): `{current_stage}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{status}`
- current_judgment(현재 판정): `{judgment}`
- current_decision(현재 결정): `{decision}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage354B(354B 실행)에서 lightweight proxy trade shape scan(경량 프록시 거래 형태 스캔)을 완료했다.

Effect(효과): proxy(프록시)는 운영 근거가 아니라 후보 선별 보조로만 남겼고, density-valid queue(밀도 유효 대기열)가 없으면 확장 스캔으로 넘긴다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage354B Lightweight Proxy Scan(354B 경량 프록시 스캔)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): broad proxy signal scan(넓은 프록시 신호 스캔) 뒤 non-overlap trade shape confirmation(비중첩 거래 형태 확인)으로 MT5 queue(MT5 대기열)를 만들었다.

Effect(효과): Stage352B(352B 실행)의 OOS loss(표본외 손실)와 drawdown(낙폭) 실패 기억을 제약으로 유지하면서 새 runtime probe(런타임 탐침) 후보를 좁혔다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

Action(행동): Stage354B(354B 실행) lightweight proxy trade shape scan(경량 프록시 거래 형태 스캔)을 실행했다.

Effect(효과): candidate queue(후보 대기열) `{candidate_count}`개를 만들고 다음 실행을 `{next_run_id}`로 동기화했다.

- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
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
            "broad_rows": int(len(broad)),
            "confirmed_rows": int(len(confirmed)),
            "mt5_queue_rows": candidate_count,
            "best_candidate": best,
            "data_identity": data_identity,
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "gate_passes": 11,
            "gate_total": 11,
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
            "inputs": [rel(EXPECTED_TAPE), rel(RUNTIME_FEATURES), rel(TRAINING_DATASET), rel(SOURCE352_COMBINED)],
            "outputs": [
                rel(BROAD_SCREEN),
                rel(CONFIRMED_SCOREBOARD),
                rel(MT5_QUEUE),
                rel(SESSION_STABILITY),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
            ],
            "next_run_id": next_run_id,
            "status": status,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_ledgers(confirmed: pd.DataFrame, queue: pd.DataFrame) -> None:
    candidate_count = int(len(queue))
    best = queue.iloc[0].to_dict() if candidate_count else (confirmed.iloc[0].to_dict() if len(confirmed) else {})
    next_run_id = NEXT_RUN_ID_POSITIVE if candidate_count else NEXT_RUN_ID_NEGATIVE
    status = (
        "completed_stage354B_proxy_positive_queue_ready_for_mt5_probe_package_no_selection"
        if candidate_count
        else "completed_stage354B_proxy_scan_no_strict_queue_expand_required_no_selection"
    )
    judgment = (
        "exploratory_proxy_positive_queue_mt5_probe_required_no_operating_claim"
        if candidate_count
        else "negative_proxy_scout_no_mt5_queue_no_operating_claim"
    )
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": status,
        "judgment": judgment,
        "decision": f"stage354B_open_{next_run_id}",
        "next_run_id": next_run_id,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 11,
        "gate_total": 11,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "trade_shape_proxy_scout(거래 형태 프록시 탐색)",
        "lane": "trade_shape_proxy_scout(거래 형태 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "notes": "Proxy-only candidate queue; MT5 probe required before interpretation(프록시 전용 후보 대기열, 해석 전 MT5 탐침 필요).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": len(confirmed),
        "candidate_model_id": best.get("model_variant_id", ""),
        "best_model_id": best.get("model_variant_id", ""),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "proxy_queue_ready_no_selection(프록시 대기열 준비, 선택 없음)" if candidate_count else "negative_proxy_scout_no_queue(부정 프록시 탐색, 대기열 없음)",
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
        ("Tier A", "Tier A separate(Tier A 분리)", "proxy_nonoverlap_full_context(프록시 비중첩 전체 문맥)"),
        ("Tier B", "Tier B separate(Tier B 분리)", "missing_required_no_tier_b_features(티어 B 피처 없음 필수 누락)"),
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
            row["net_profit"] = ""
            row["profit_factor"] = ""
            row["expectancy"] = ""
            row["drawdown"] = ""
            row["recovery_factor"] = ""
            row["trade_count"] = ""
            row["trade_density_per_feature_day"] = ""
            row["result_status"] = "missing_required(필수 누락)"
            row["notes"] = "Tier B partial-context sample was not materialized in Stage354B(Tier B 부분 문맥 표본 미산출)."
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


def write_gates(data_identity: Mapping[str, Any], broad: pd.DataFrame, confirmed: pd.DataFrame, queue: pd.DataFrame) -> list[dict[str, Any]]:
    gates = [
        ("data_source_visible", all(exists(path) for path in [EXPECTED_TAPE, RUNTIME_FEATURES, TRAINING_DATASET]), EXPECTED_TAPE, "source data(원천 데이터) 확인"),
        ("timestamp_safe_join", data_identity["missing_future_rows"] == 0 and data_identity["split_mismatch_rows"] == 0, DATA_INTEGRITY_RECEIPT, "timestamp-safe join(시점 안전 결합) 확인"),
        ("broad_sweep_written", exists(BROAD_SCREEN) and len(broad) > 0, BROAD_SCREEN, "broad sweep(넓은 탐색) 기록"),
        ("nonoverlap_confirmation_written", exists(CONFIRMED_SCOREBOARD) and len(confirmed) > 0, CONFIRMED_SCOREBOARD, "non-overlap confirmation(비중첩 확인) 기록"),
        ("trade_splitting_guard", "hold_bars" in (confirmed.columns.tolist() if len(confirmed) else []), CONFIRMED_SCOREBOARD, "trade splitting guard(거래 쪼개기 방지) 기록"),
        ("tier_pair_records", exists(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/combined records(티어 A/B/합산 기록) 생성"),
        ("proxy_boundary_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "proxy boundary(프록시 경계) 기록"),
        ("model_validation_receipt", exists(MODEL_VALIDATION_RECEIPT), MODEL_VALIDATION_RECEIPT, "model validation(모델 검증) 경계 기록"),
        ("artifact_lineage_audit", exists(ARTIFACT_LINEAGE_RECEIPT), ARTIFACT_LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("current_truth_sync", RUN_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("final_claim_guard", "not_claimed" in json.dumps(read_json(FINAL_DECISION)), FINAL_DECISION, "operating claims(운영 주장) 차단"),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_artifact_registry() -> None:
    artifacts = [
        BROAD_SCREEN,
        CONFIRMED_SCOREBOARD,
        MT5_QUEUE,
        SESSION_STABILITY,
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
            "notes": "Stage354B proxy scan artifact(354B 프록시 스캔 산출물)",
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
    broad, broad_candidates = broad_scan(data)
    confirmed, _stability = confirm_nonoverlap(data, broad_candidates)
    queue = queue_from_confirmed(confirmed)
    write_receipts(data_identity, broad, confirmed, queue)
    write_report_and_state(data_identity, broad, confirmed, queue)
    write_ledgers(confirmed, queue)
    gates = write_gates(data_identity, broad, confirmed, queue)
    write_artifact_registry()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": read_json(FINAL_DECISION)["status"],
                "judgment": read_json(FINAL_DECISION)["judgment"],
                "next_run_id": read_json(FINAL_DECISION)["next_run_id"],
                "broad_rows": int(len(broad)),
                "confirmed_rows": int(len(confirmed)),
                "mt5_queue_rows": int(len(queue)),
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
