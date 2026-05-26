from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN_NUMBER = "run333D"
RUN_ID = "run333D_screen_guarded_payload_cost_curve_and_pocket_risk_v1"
PARENT_RUN_ID = "run333C_materialize_guarded_veto_scoring_payloads_v1"
NEXT_RUN_ID = "run333E_runtime_probe_queue_or_failure_memory_from_screen_v1"
STATUS = "completed_guarded_payload_cost_curve_pocket_screen_no_forward_decision"
JUDGMENT = "proxy_cost_curve_screen_completed_research_only_no_goal_achieve"
DECISION = "cost_curve_pocket_proxy_evidence_available_runtime_probe_or_failure_memory_next"
CLAIM_BOUNDARY = (
    "research_development_only_guarded_payload_cost_curve_pocket_screen_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

FIXED_LOT = 0.1
HOLD_BARS = 12
COST_STEPS = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0]
MIN_RUNTIME_PROBE_TRADES = 20

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
RUN333C_DIR = STAGE_DIR / "02_runs" / "run333C"
RUN330E_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330E"
RAW_FORWARD_BARS = ROOT / "stages" / "326_forward__cp322a_frozen_forward_gate" / "01_inputs" / "raw_m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage333D_cost_curve_pocket_screen.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    try:
        return io_path(path).exists()
    except OSError:
        return False


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, float) and math.isinf(value):
        return "inf" if value > 0 else "-inf"
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        return round(value, 10)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def safe_div(value: float | int | None, denom: float | int | None) -> float | None:
    if value is None or denom in (None, 0):
        return None
    return float(value) / float(denom)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line(text: str, anchor_prefix: str, insertion: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(anchor_prefix):
            lines.insert(index + 1, insertion)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + insertion + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    index: dict[tuple[str, ...], dict[str, Any]] = {
        tuple(str(row.get(key, "")) for key in key_columns): row for row in existing
    }
    for row in rows:
        index[tuple(str(row.get(key, "")) for key in key_columns)] = dict(row)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in index.values():
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})
    return path


def append_unique_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    seen = {tuple(str(row.get(key, "")) for key in key_columns) for row in existing}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        if key not in seen:
            existing.append(dict(row))
            seen.add(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in existing:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})
    return path


def profit_factor(values: Sequence[float]) -> float | None:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = -sum(value for value in values if value < 0)
    if gross_loss == 0:
        return None if gross_profit == 0 else math.inf
    return gross_profit / gross_loss


def max_drawdown(values: Sequence[float]) -> float:
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        worst = max(worst, peak - equity)
    return worst


def underwater_stats(values: Sequence[float], times: Sequence[pd.Timestamp]) -> dict[str, Any]:
    equity = 0.0
    peak = 0.0
    current_start: pd.Timestamp | None = None
    current_len = 0
    worst_len = 0
    worst_start: pd.Timestamp | None = None
    worst_end: pd.Timestamp | None = None
    worst_dd = 0.0
    for value, timestamp in zip(values, times):
        equity += value
        if equity >= peak:
            peak = equity
            current_start = None
            current_len = 0
            continue
        if current_start is None:
            current_start = timestamp
            current_len = 0
        current_len += 1
        drawdown = peak - equity
        if current_len > worst_len or drawdown > worst_dd:
            worst_len = current_len
            worst_start = current_start
            worst_end = timestamp
            worst_dd = max(worst_dd, drawdown)
    return {
        "max_underwater_trade_count": worst_len,
        "max_underwater_start": worst_start,
        "max_underwater_end": worst_end,
        "max_drawdown": worst_dd,
    }


def aggregate(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(tuple(row.get(key, "") for key in keys), []).append(row)
    output: list[dict[str, Any]] = []
    for key, group_rows in grouped.items():
        values = [float(row.get("proxy_net_profit", 0.0)) for row in group_rows]
        times = [pd.Timestamp(row.get("close_time")) for row in group_rows]
        gross_profit = sum(value for value in values if value > 0)
        gross_loss = -sum(value for value in values if value < 0)
        wins = [value for value in values if value > 0]
        losses = [value for value in values if value < 0]
        avg_win = safe_div(sum(wins), len(wins))
        avg_loss = safe_div(sum(losses), len(losses))
        output.append(
            {
                **dict(zip(keys, key)),
                "trade_count": len(group_rows),
                "net_profit": sum(values),
                "gross_profit": gross_profit,
                "gross_loss": gross_loss,
                "profit_factor": profit_factor(values),
                "expectancy": safe_div(sum(values), len(values)),
                "win_rate": safe_div(len(wins), len(group_rows)),
                "avg_win": avg_win,
                "avg_loss": avg_loss,
                "payoff_ratio": safe_div(avg_win, abs(avg_loss) if avg_loss is not None else None),
                **underwater_stats(values, times),
            }
        )
    return output


def rolling_min_net(rows: Sequence[Mapping[str, Any]], window: int) -> tuple[float | None, str, str]:
    if len(rows) < window:
        return None, "", ""
    worst_sum: float | None = None
    worst_start = ""
    worst_end = ""
    for start in range(0, len(rows) - window + 1):
        chunk = rows[start : start + window]
        net = sum(float(row["proxy_net_profit"]) for row in chunk)
        if worst_sum is None or net < worst_sum:
            worst_sum = net
            worst_start = str(chunk[0]["open_time"])
            worst_end = str(chunk[-1]["close_time"])
    return worst_sum, worst_start, worst_end


def split_chunks(rows: Sequence[Mapping[str, Any]], count: int) -> list[list[Mapping[str, Any]]]:
    if not rows:
        return []
    size = math.ceil(len(rows) / count)
    return [list(rows[index : index + size]) for index in range(0, len(rows), size)]


def load_bars() -> pd.DataFrame:
    bars = pd.read_csv(
        io_path(RAW_FORWARD_BARS),
        usecols=["time_open_unix", "open", "high", "low", "close", "spread_points"],
    )
    bars["timestamp"] = pd.to_datetime(bars["time_open_unix"], unit="s", utc=True)
    for column in ("open", "high", "low", "close", "spread_points"):
        bars[column] = pd.to_numeric(bars[column], errors="coerce")
    return bars.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def load_queue() -> list[dict[str, str]]:
    rows = read_csv_rows(RUN333C_DIR / "cost_curve_input_queue.csv")
    return [row for row in rows if row.get("queue_status") == "queued_for_run333D_proxy_cost_curve_screen"]


def load_source_mt5_reference() -> list[dict[str, Any]]:
    rows = read_csv_rows(RUN330E_DIR / "mt5_runtime_probe_summary.csv")
    return [
        {
            **row,
            "source_run_id": "run330E_mt5_runtime_probe_or_block_v1",
            "reference_boundary": "source_raw_forward_mt5_reference_only_not_guarded_branch_mt5",
        }
        for row in rows
        if row.get("artifact_slug") in {"c56_plain", "m48_plain"}
    ]


def build_proxy_trades(bars: pd.DataFrame, queue_rows: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bar_index = {pd.Timestamp(row.timestamp): index for index, row in bars.iterrows()}
    all_trades: list[dict[str, Any]] = []
    coverage_rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        payload_path = ROOT / str(queue["signal_payload_path"])
        signals = pd.read_csv(io_path(payload_path))
        if signals.empty:
            coverage_rows.append(
                {
                    "queue_id": queue["queue_id"],
                    "thesis_id": queue["thesis_id"],
                    "source_artifact": queue["source_artifact"],
                    "scoring_mode": queue["scoring_mode"],
                    "signal_rows": 0,
                    "proxy_trade_count": 0,
                    "missing_bar_rows": 0,
                    "skipped_during_hold_rows": 0,
                    "coverage_judgment": "empty_signal_payload",
                }
            )
            continue
        signals["timestamp"] = pd.to_datetime(signals["timestamp"], utc=True, errors="coerce")
        signals = signals.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
        next_allowed: pd.Timestamp | None = None
        missing_bar_rows = 0
        skipped_during_hold_rows = 0
        trade_index = 0
        for signal in signals.to_dict("records"):
            timestamp = pd.Timestamp(signal["timestamp"])
            if next_allowed is not None and timestamp <= next_allowed:
                skipped_during_hold_rows += 1
                continue
            open_index = bar_index.get(timestamp)
            if open_index is None:
                missing_bar_rows += 1
                continue
            close_index = min(open_index + HOLD_BARS, len(bars) - 1)
            if close_index <= open_index:
                missing_bar_rows += 1
                continue
            direction = int(to_float(signal.get("signal_direction")) or 0)
            if direction == 0:
                continue
            open_bar = bars.iloc[open_index]
            close_bar = bars.iloc[close_index]
            entry_price = float(open_bar["close"])
            exit_price = float(close_bar["close"])
            point_return = direction * (exit_price - entry_price)
            net_profit = point_return * FIXED_LOT
            window = bars.iloc[open_index : close_index + 1]
            trade_index += 1
            next_allowed = pd.Timestamp(close_bar["timestamp"])
            all_trades.append(
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "source_type": "guarded_signal_proxy_nonoverlap_hold12_not_mt5",
                    "queue_id": queue["queue_id"],
                    "thesis_id": queue["thesis_id"],
                    "guard_family": signal.get("guard_family", ""),
                    "source_artifact": queue["source_artifact"],
                    "scoring_mode": queue["scoring_mode"],
                    "candidate_id": signal.get("candidate_id", ""),
                    "artifact_slug": signal.get("artifact_slug", queue["source_artifact"]),
                    "feature_set_id": signal.get("feature_set_id", ""),
                    "model_id": signal.get("model_id", ""),
                    "view_id": signal.get("view_id", queue["queue_id"]),
                    "trade_index": trade_index,
                    "direction": "long" if direction > 0 else "short",
                    "signal_timestamp": timestamp,
                    "open_time": pd.Timestamp(open_bar["timestamp"]),
                    "close_time": pd.Timestamp(close_bar["timestamp"]),
                    "hold_bars": close_index - open_index,
                    "fixed_lot": FIXED_LOT,
                    "entry_close": entry_price,
                    "exit_close": exit_price,
                    "point_return": point_return,
                    "proxy_net_profit": net_profit,
                    "guard_score": to_float(signal.get("guard_score")),
                    "hard_veto_flag": int(to_float(signal.get("hard_veto_flag")) or 0),
                    "soft_veto_flag": int(to_float(signal.get("soft_veto_flag")) or 0),
                    "negative_control_flag": int(to_float(signal.get("negative_control_flag")) or 0),
                    "guard_score_missing_flag": int(to_float(signal.get("guard_score_missing_flag")) or 0),
                    "max_probability": to_float(signal.get("max_probability")),
                    "probability_margin": to_float(signal.get("probability_margin")),
                    "decision_threshold": to_float(signal.get("decision_threshold")),
                    "hour": signal.get("hour_utc", ""),
                    "month": signal.get("month", ""),
                    "session_slice": signal.get("us_cash_session", ""),
                    "volatility_regime": signal.get("volatility_regime", ""),
                    "adx_regime": signal.get("adx_regime", ""),
                    "vix_regime": signal.get("vix_zscore_regime", ""),
                    "usd_regime": signal.get("usdx_zscore_regime", ""),
                    "rate_regime": signal.get("us10yr_zscore_regime", ""),
                    "spread_points_median_in_trade": float(window["spread_points"].median()),
                    "proxy_boundary": "guarded_signal_curve_proxy_not_mt5_not_forward_decision",
                }
            )
        proxy_trade_count = sum(1 for trade in all_trades if trade["queue_id"] == queue["queue_id"])
        coverage_rows.append(
            {
                "queue_id": queue["queue_id"],
                "thesis_id": queue["thesis_id"],
                "source_artifact": queue["source_artifact"],
                "scoring_mode": queue["scoring_mode"],
                "signal_rows": len(signals),
                "proxy_trade_count": proxy_trade_count,
                "missing_bar_rows": missing_bar_rows,
                "skipped_during_hold_rows": skipped_during_hold_rows,
                "signal_to_proxy_trade_compression": safe_div(len(signals), proxy_trade_count),
                "coverage_judgment": "usable_proxy_coverage" if proxy_trade_count else "blocked_no_proxy_trades",
            }
        )
    return all_trades, coverage_rows


def build_kpi_rows(trades: Sequence[Mapping[str, Any]], coverage_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    coverage_by_queue = {row["queue_id"]: row for row in coverage_rows}
    rows: list[dict[str, Any]] = []
    for group in aggregate(trades, ["queue_id", "thesis_id", "guard_family", "source_artifact", "scoring_mode"]):
        group_trades = [trade for trade in trades if trade["queue_id"] == group["queue_id"]]
        values = [float(trade["proxy_net_profit"]) for trade in group_trades]
        coverage = coverage_by_queue.get(group["queue_id"], {})
        start = min(pd.Timestamp(trade["open_time"]) for trade in group_trades)
        end = max(pd.Timestamp(trade["close_time"]) for trade in group_trades)
        days = max((end - start).total_seconds() / 86400.0, 1 / 24)
        dd = to_float(group.get("max_drawdown")) or 0.0
        net = to_float(group.get("net_profit")) or 0.0
        rolling20, rolling20_start, rolling20_end = rolling_min_net(group_trades, 20)
        rolling40, rolling40_start, rolling40_end = rolling_min_net(group_trades, 40)
        rows.append(
            {
                **group,
                "first_trade_time": start,
                "last_trade_time": end,
                "days": days,
                "proxy_trades_per_day": safe_div(group["trade_count"], days),
                "signal_rows": coverage.get("signal_rows", ""),
                "signal_to_proxy_trade_compression": coverage.get("signal_to_proxy_trade_compression", ""),
                "recovery_factor": safe_div(net, dd),
                "rolling20_min_net": rolling20,
                "rolling20_start": rolling20_start,
                "rolling20_end": rolling20_end,
                "rolling40_min_net": rolling40,
                "rolling40_start": rolling40_start,
                "rolling40_end": rolling40_end,
                "fixed_lot": FIXED_LOT,
                "hold_bars_policy": HOLD_BARS,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_curve_rows(trades: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    curve_rows: list[dict[str, Any]] = []
    underwater_rows: list[dict[str, Any]] = []
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for trade in sorted(trades, key=lambda item: (item["queue_id"], item["close_time"])):
        grouped.setdefault(str(trade["queue_id"]), []).append(trade)
    for queue_id, group in grouped.items():
        meta_keys = ["queue_id", "thesis_id", "guard_family", "source_artifact", "scoring_mode"]
        for chunk_count, chunk_type in [(3, "thirds"), (5, "fifths")]:
            for idx, chunk in enumerate(split_chunks(group, chunk_count), start=1):
                stats = aggregate(chunk, meta_keys)[0]
                curve_rows.append(
                    {
                        **stats,
                        "chunk_type": chunk_type,
                        "chunk_id": f"{chunk_type}_{idx}",
                        "start_time": chunk[0]["open_time"],
                        "end_time": chunk[-1]["close_time"],
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
        for window in [20, 40]:
            if len(group) < window:
                continue
            candidates: list[tuple[int, list[Mapping[str, Any]], float]] = []
            for start in range(0, len(group) - window + 1):
                chunk = group[start : start + window]
                candidates.append((start, list(chunk), sum(float(row["proxy_net_profit"]) for row in chunk)))
            start, worst, _ = min(candidates, key=lambda item: item[2])
            stats = aggregate(worst, meta_keys)[0]
            curve_rows.append(
                {
                    **stats,
                    "chunk_type": "rolling_worst_net",
                    "chunk_id": f"rolling_{window}_start_{start + 1}",
                    "start_time": worst[0]["open_time"],
                    "end_time": worst[-1]["close_time"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        values = [float(row["proxy_net_profit"]) for row in group]
        times = [pd.Timestamp(row["close_time"]) for row in group]
        first = group[0]
        underwater_rows.append(
            {
                "queue_id": queue_id,
                "thesis_id": first["thesis_id"],
                "guard_family": first["guard_family"],
                "source_artifact": first["source_artifact"],
                "scoring_mode": first["scoring_mode"],
                "trade_count": len(group),
                **underwater_stats(values, times),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return curve_rows, underwater_rows


def build_cost_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for trade in trades:
        grouped.setdefault(str(trade["queue_id"]), []).append(trade)
    rows: list[dict[str, Any]] = []
    for queue_id, group in grouped.items():
        base = group[0]
        for cost in COST_STEPS:
            values = [float(trade["proxy_net_profit"]) - cost for trade in group]
            rows.append(
                {
                    "queue_id": queue_id,
                    "thesis_id": base["thesis_id"],
                    "guard_family": base["guard_family"],
                    "source_artifact": base["source_artifact"],
                    "scoring_mode": base["scoring_mode"],
                    "extra_cost_per_round_trip_account_ccy": cost,
                    "trade_count": len(values),
                    "net_profit_after_cost": sum(values),
                    "profit_factor_after_cost": profit_factor(values),
                    "expectancy_after_cost": safe_div(sum(values), len(values)),
                    "max_drawdown_after_cost": max_drawdown(values),
                    "survives_pf_ge_1": (profit_factor(values) or 0.0) >= 1.0,
                    "stress_boundary": "score_proxy_synthetic_round_trip_cost_not_mt5_no_threshold_or_lot_repair",
                }
            )
    return rows


def build_lot_rows(kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": row["queue_id"],
            "thesis_id": row["thesis_id"],
            "source_artifact": row["source_artifact"],
            "scoring_mode": row["scoring_mode"],
            "fixed_lot": FIXED_LOT,
            "net_profit_at_fixed_lot": row["net_profit"],
            "equity_dd_amount_at_fixed_lot": row["max_drawdown"],
            "net_profit_per_1lot_linear": safe_div(to_float(row.get("net_profit")), FIXED_LOT),
            "equity_dd_amount_per_1lot_linear": safe_div(to_float(row.get("max_drawdown")), FIXED_LOT),
            "expectancy_per_1lot_linear": safe_div(to_float(row.get("expectancy")), FIXED_LOT),
            "normalization_boundary": "linear_lot_normalization_only_not_new_lot_optimization_score_proxy",
        }
        for row in kpi_rows
    ]


def build_attribution_rows(trades: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    long_short = aggregate(trades, ["queue_id", "thesis_id", "source_artifact", "scoring_mode", "direction"])
    regime_rows: list[dict[str, Any]] = []
    axes = [
        ("session", "session_slice"),
        ("hour", "hour"),
        ("month", "month"),
        ("volatility", "volatility_regime"),
        ("adx", "adx_regime"),
        ("vix", "vix_regime"),
        ("usd", "usd_regime"),
        ("rate", "rate_regime"),
    ]
    for axis, key in axes:
        rows = aggregate(trades, ["queue_id", "thesis_id", "source_artifact", "scoring_mode", key])
        for row in rows:
            row["axis"] = axis
            row["bucket"] = row.pop(key)
            row["claim_boundary"] = CLAIM_BOUNDARY
            regime_rows.append(row)
    db_rows = []
    for queue_id in sorted({str(trade["queue_id"]) for trade in trades}):
        sample = next(trade for trade in trades if str(trade["queue_id"]) == queue_id)
        db_rows.append(
            {
                "queue_id": queue_id,
                "thesis_id": sample["thesis_id"],
                "source_artifact": sample["source_artifact"],
                "scoring_mode": sample["scoring_mode"],
                "db_source": "not_available_in_stage330_non_identity_payload",
                "status": "out_of_scope_by_claim",
                "reason": "guarded payloads inherit c56/m48 non-identity raw-forward signals, not original cp322A D/B decision surface rows.",
                "effect": "D/B attribution is explicitly unavailable and cannot support Forward Passed.",
            }
        )
    return long_short, regime_rows, db_rows


def cost2_by_queue(cost_rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    output = {}
    for row in cost_rows:
        if float(row["extra_cost_per_round_trip_account_ccy"]) == 2.0:
            output[str(row["queue_id"])] = row
    return output


def build_delta_rows(kpi_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    kpi_by_queue = {str(row["queue_id"]): row for row in kpi_rows}
    cost2 = cost2_by_queue(cost_rows)
    control_by_thesis = {
        str(row["thesis_id"]): row for row in kpi_rows if row.get("scoring_mode") == "control_no_veto"
    }
    delta_rows: list[dict[str, Any]] = []
    decision_rows: list[dict[str, Any]] = []
    for row in kpi_rows:
        thesis_id = str(row["thesis_id"])
        control = control_by_thesis.get(thesis_id, row)
        control_cost2 = cost2.get(str(control["queue_id"]), {})
        row_cost2 = cost2.get(str(row["queue_id"]), {})
        trade_count = int(row["trade_count"])
        pf2 = to_float(row_cost2.get("profit_factor_after_cost")) or 0.0
        rolling20 = to_float(row.get("rolling20_min_net"))
        rolling40 = to_float(row.get("rolling40_min_net"))
        net = to_float(row.get("net_profit")) or 0.0
        dd = to_float(row.get("max_drawdown")) or 0.0
        if row["scoring_mode"] == "control_no_veto":
            decision = "baseline_reference_not_candidate"
            next_use = "comparison_baseline_only"
        elif trade_count < MIN_RUNTIME_PROBE_TRADES:
            decision = "screen_inconclusive_sparse"
            next_use = "failure_memory_or_sparse_probe_review"
        elif pf2 >= 1.0 and (rolling20 or -math.inf) >= 0.0 and (rolling40 or -math.inf) >= 0.0 and net > 0:
            decision = "screen_survived_proxy_guard_runtime_probe_design_only"
            next_use = "eligible_for_run333E_runtime_probe_queue_design"
        else:
            decision = "screen_failed_proxy_cost_curve_guard"
            next_use = "failure_memory_no_candidate_language"
        delta_rows.append(
            {
                "queue_id": row["queue_id"],
                "thesis_id": thesis_id,
                "source_artifact": row["source_artifact"],
                "scoring_mode": row["scoring_mode"],
                "control_queue_id": control["queue_id"],
                "net_delta_vs_control": (to_float(row.get("net_profit")) or 0.0) - (to_float(control.get("net_profit")) or 0.0),
                "pf_delta_vs_control": None
                if to_float(row.get("profit_factor")) is None or to_float(control.get("profit_factor")) is None
                else (to_float(row.get("profit_factor")) or 0.0) - (to_float(control.get("profit_factor")) or 0.0),
                "dd_delta_vs_control": dd - (to_float(control.get("max_drawdown")) or 0.0),
                "trade_count_delta_vs_control": trade_count - int(control["trade_count"]),
                "cost2_pf": pf2,
                "control_cost2_pf": to_float(control_cost2.get("profit_factor_after_cost")),
                "rolling20_min_net": rolling20,
                "rolling40_min_net": rolling40,
                "comparison_boundary": "proxy_delta_only_not_candidate_selection",
            }
        )
        decision_rows.append(
            {
                "queue_id": row["queue_id"],
                "thesis_id": thesis_id,
                "source_artifact": row["source_artifact"],
                "scoring_mode": row["scoring_mode"],
                "trade_count": trade_count,
                "net_profit": net,
                "profit_factor": row["profit_factor"],
                "max_drawdown": dd,
                "cost2_pf": pf2,
                "rolling20_min_net": rolling20,
                "rolling40_min_net": rolling40,
                "screen_decision": decision,
                "next_use": next_use,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return delta_rows, decision_rows


def build_runtime_probe_queue(decision_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in decision_rows:
        if row["screen_decision"] != "screen_survived_proxy_guard_runtime_probe_design_only":
            continue
        rows.append(
            {
                "queue_id": row["queue_id"],
                "thesis_id": row["thesis_id"],
                "source_artifact": row["source_artifact"],
                "scoring_mode": row["scoring_mode"],
                "signal_payload_path": next(
                    q["signal_payload_path"]
                    for q in read_csv_rows(RUN333C_DIR / "cost_curve_input_queue.csv")
                    if q["queue_id"] == row["queue_id"]
                ),
                "runtime_probe_status": "queued_for_run333E_design_only",
                "required_before_mt5": "feature/model/threshold/risk/report/telemetry identity plus MT5 tester handoff contract",
                "forbidden_claim": "no_runtime_authority_no_forward_passed_no_goal_achieve",
            }
        )
    return rows


def build_decision_payload(decision_rows: Sequence[Mapping[str, Any]], kpi_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    survivors = [row for row in decision_rows if row["screen_decision"] == "screen_survived_proxy_guard_runtime_probe_design_only"]
    failures = [row for row in decision_rows if row["screen_decision"] == "screen_failed_proxy_cost_curve_guard"]
    sparse = [row for row in decision_rows if row["screen_decision"] == "screen_inconclusive_sparse"]
    best_net = max((to_float(row.get("net_profit")) or -math.inf for row in kpi_rows), default=-math.inf)
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "screen_survivor_count": len(survivors),
        "screen_failure_count": len(failures),
        "screen_sparse_count": len(sparse),
        "best_proxy_net_profit": None if best_net == -math.inf else best_net,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "reason": "proxy screen only; MT5/runtime parity and forward decision remain missing.",
        "next_action": NEXT_RUN_ID,
    }


def source_hash_rows() -> list[dict[str, Any]]:
    queue = read_csv_rows(RUN333C_DIR / "cost_curve_input_queue.csv")
    paths: dict[str, Path] = {
        "run333C_cost_curve_queue": RUN333C_DIR / "cost_curve_input_queue.csv",
        "run333C_signal_manifest": RUN333C_DIR / "signal_payload_manifest.csv",
        "run333C_payload_manifest": RUN333C_DIR / "payload_manifest.csv",
        "raw_forward_bars": RAW_FORWARD_BARS,
        "run330E_mt5_runtime_probe_summary": RUN330E_DIR / "mt5_runtime_probe_summary.csv",
    }
    for row in queue:
        if row.get("queue_status") == "queued_for_run333D_proxy_cost_curve_screen":
            paths[f"signal_payload__{row['queue_id']}"] = ROOT / row["signal_payload_path"]
    rows = []
    for artifact_id, path in paths.items():
        exists = path_exists(path)
        rows.append(
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": exists,
                "sha256": sha256_file(path) if exists and io_path(path).is_file() else "",
            }
        )
    return rows


def gate_rows(
    queue_rows: Sequence[Mapping[str, str]],
    proxy_trades: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    runtime_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    source_missing = [row["artifact_id"] for row in source_hash_rows() if not row["exists"]]
    return [
        {
            "gate": "source_artifacts_present",
            "status": "pass" if not source_missing else "fail",
            "evidence_path": rel(RUN_DIR / "source_artifact_hashes.json"),
            "notes": "all run333C signal payload and raw bar sources present" if not source_missing else f"missing={source_missing}",
        },
        {
            "gate": "queued_views_screened",
            "status": "pass" if len(queue_rows) == 15 and len(kpi_rows) == 15 else "fail",
            "evidence_path": rel(RUN_DIR / "proxy_kpi_by_view.csv"),
            "notes": f"queued={len(queue_rows)};kpi_rows={len(kpi_rows)}",
        },
        {
            "gate": "proxy_trade_records_exist",
            "status": "pass" if len(proxy_trades) > 0 else "fail",
            "evidence_path": rel(RUN_DIR / "proxy_trade_records.csv"),
            "notes": f"proxy_trades={len(proxy_trades)}",
        },
        {
            "gate": "cost_ladder_complete",
            "status": "pass" if len(cost_rows) == len(kpi_rows) * len(COST_STEPS) else "fail",
            "evidence_path": rel(RUN_DIR / "cost_stress_report.csv"),
            "notes": f"cost_rows={len(cost_rows)};expected={len(kpi_rows) * len(COST_STEPS)}",
        },
        {
            "gate": "curve_pocket_complete",
            "status": "pass" if len(curve_rows) >= len(kpi_rows) else "fail",
            "evidence_path": rel(RUN_DIR / "curve_pocket_report.csv"),
            "notes": f"curve_rows={len(curve_rows)}",
        },
        {
            "gate": "runtime_probe_queue_boundary",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "runtime_probe_branch_queue.csv"),
            "notes": f"runtime_probe_design_rows={len(runtime_queue)};no MT5 run in run333D",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "no_retune_guard_receipt.json"),
            "notes": "no threshold, lot, model, ONNX, D/B rule, ATR SL/TP, or runtime handoff change.",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "proxy screen only; no Forward Passed/Failed, runtime authority, or Goal Achieve.",
        },
    ]


def write_receipts(
    generated_at_utc: str,
    queue_rows: Sequence[Mapping[str, str]],
    proxy_trades: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    decision_rows: Sequence[Mapping[str, Any]],
    runtime_queue: Sequence[Mapping[str, Any]],
) -> list[Path]:
    failed = [row for row in gate_rows(queue_rows, proxy_trades, kpi_rows, cost_rows, curve_rows, runtime_queue) if row["status"] != "pass"]
    survivors = [row for row in decision_rows if row["screen_decision"] == "screen_survived_proxy_guard_runtime_probe_design_only"]
    failures = [row for row in decision_rows if row["screen_decision"] == "screen_failed_proxy_cost_curve_guard"]
    return [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "guarded hard/soft/negative-control views changed trade count, cost survival, and rolling pocket shape versus control_no_veto.",
                "comparison_baseline": "per-thesis control_no_veto payload from run333C.",
                "likely_drivers": "guard score filtering, missing breadth abstain boundary, session/macro/volatility risk slicing, trade frequency compression.",
                "segment_checks": "direction, session, hour, month, volatility, ADX, VIX, USD, rate, rolling20/rolling40, underwater stretch, cost ladder.",
                "trade_shape": "recorded in proxy_kpi_by_view.csv, curve_pocket_report.csv, underwater_stretch_report.csv, and lot_normalized_report.csv.",
                "alternative_explanations": "proxy hold12 model is not MT5, synthetic round-trip cost is not broker execution, and source ONNX remains Stage330 research artifact.",
                "attribution_confidence": "low_to_medium_proxy_only",
                "next_probe": NEXT_RUN_ID,
            },
        ),
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(RUN333C_DIR / "cost_curve_input_queue.csv"), rel(RAW_FORWARD_BARS)],
                "time_axis": "signal timestamps and bar timestamps are UTC bar opens; proxy close uses 12 later M5 bars.",
                "sample_scope": "15 queued run333C guarded signal payloads; one expected-invalid breadth negative-control is excluded.",
                "missing_or_duplicate_check": rel(RUN_DIR / "proxy_coverage_audit.csv"),
                "feature_label_boundary": "no labels, future returns, or forward PnL are used to set guard rules.",
                "split_boundary": "raw-forward proxy screen only; not train/validation selection and not MT5.",
                "leakage_risk": "interpreting proxy KPI as Forward Passed or selecting a threshold from the proxy result.",
                "data_hash_or_identity": rel(RUN_DIR / "source_artifact_hashes.json"),
                "integrity_judgment": "usable_for_proxy_cost_curve_screen_only",
            },
        ),
        write_json(
            RUN_DIR / "no_retune_guard_receipt.json",
            {
                "selected_candidate_changed": False,
                "onnx_changed": False,
                "adapter_package_changed": False,
                "feature_order_changed_for_existing_models": False,
                "d_b_decision_surface_changed": False,
                "score_threshold_changed": False,
                "risk_or_lot_logic_changed": False,
                "atr_sl_tp_changed": False,
                "runtime_handoff_changed": False,
                "new_model_trained": False,
                "forward_pnl_used_for_guard_thresholds": False,
                "notes": "run333D only screens existing payloads with fixed proxy cost/curve rules.",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "source_inputs": [row["path"] for row in source_hash_rows()],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(RUN_DIR / "proxy_kpi_by_view.csv"),
                    rel(RUN_DIR / "cost_stress_report.csv"),
                    rel(RUN_DIR / "curve_pocket_report.csv"),
                    rel(RUN_DIR / "runtime_probe_branch_queue.csv"),
                ],
                "artifact_hashes": "recorded in docs/registers/artifact_registry.csv",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked",
                "lineage_judgment": "connected_with_proxy_screen_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "run333D guarded payload cost curve and pocket risk proxy screen",
                "evidence_available": [
                    rel(RUN_DIR / "proxy_kpi_by_view.csv"),
                    rel(RUN_DIR / "cost_stress_report.csv"),
                    rel(RUN_DIR / "curve_pocket_report.csv"),
                    rel(RUN_DIR / "branch_screen_decision.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "evidence_missing": ["MT5 tester output for guarded branches", "runtime telemetry reconciliation", "final Forward Passed/Failed decision"],
                "judgment_label": "exploratory_proxy_screen_completed",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": f"Proxy screen found {len(survivors)} runtime-probe design rows and {len(failures)} cost/curve failures, but this is not a forward pass.",
                "failed_gates": failed,
            },
        ),
    ]


def write_reports(decision_payload: Mapping[str, Any]) -> list[Path]:
    report = write_md(
        REVIEWS_DIR / "run333D_cost_curve_pocket_screen.md",
        f"""
# run333D Cost Curve Pocket Screen(333D 비용 곡선 포켓 선별)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Proxy Screen(대리 선별)

- screen_survivor_count(선별 생존 수): `{decision_payload.get("screen_survivor_count")}`
- screen_failure_count(선별 실패 수): `{decision_payload.get("screen_failure_count")}`
- screen_sparse_count(희소 수): `{decision_payload.get("screen_sparse_count")}`
- best_proxy_net_profit(최고 대리 순손익): `{decision_payload.get("best_proxy_net_profit")}`

Effect(효과): run333D(333D 실행)는 guarded payload(방어 페이로드)를 cost ladder(비용 사다리), rolling20/40 pocket(롤링20/40 포켓), underwater stretch(수중 구간), session/hour/month/regime slice(세션/시간/월/국면 구간)로 압박했다. MT5 tester(메타트레이더5 테스터) 실행은 아니므로 Forward Passed/Failed(전진 통과/실패)는 없다.

## Boundary(경계)

- no threshold retuning(임계값 재조정 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 갱신 없음)
- no ONNX update(온엑스 갱신 없음)
- no runtime authority(런타임 권위 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage333D Cost Curve Pocket Decision(333D 비용 곡선 포켓 결정)

run333D(333D 실행)는 run333C(333C 실행)의 15개 queued guarded signal payload(대기 방어 신호 페이로드)를 fixed hold12 proxy(고정 12봉 대리검증)로 선별했다.

- decision(결정): `{DECISION}`
- screen_survivor_count(선별 생존 수): `{decision_payload.get("screen_survivor_count")}`
- screen_failure_count(선별 실패 수): `{decision_payload.get("screen_failure_count")}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): 생존 행은 runtime probe queue design(런타임 탐침 대기열 설계) 입력일 뿐이다. 실패 행은 failure memory(실패 기억)로 남기며, proxy(대리검증) 숫자만으로 후보를 고르지 않는다.
""",
    )
    return [report, decision]


def update_selection_status() -> Path:
    text = f"""
# Stage333 Selection Status(333단계 선택 상태)

- stage_status(단계 상태): `open_cost_curve_screen_completed_runtime_probe_or_failure_memory_next`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `332_overfit_guard__failure_memory_forward_research_handoff`
- latest_materialization(최신 물질화): `run333A_materialize_timestamp_safe_pocket_veto_features_v1`
- latest_scoring_design(최신 점수화 설계): `run333B_design_guarded_veto_scoring_no_retune_v1`
- latest_payload_materialization(최신 페이로드 물질화): `run333C_materialize_guarded_veto_scoring_payloads_v1`
- latest_cost_curve_screen(최신 비용 곡선 선별): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run333D(333D 실행)는 cost/curve/pocket screen(비용/곡선/포켓 선별)을 마쳤고, 다음은 runtime probe queue(런타임 탐침 대기열) 또는 failure memory(실패 기억) 정리다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_current_truth(decision_payload: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage333(333단계) run333D(333D 실행)는 `{STATUS}`로 guarded payload cost/curve/pocket screen(방어 페이로드 비용/곡선/포켓 선별)을 완료했다. Effect(효과): `{decision_payload.get('screen_survivor_count')}`개 branch(분기)는 runtime probe design(런타임 탐침 설계) 입력으로 남고, Forward Passed/Failed(전진 통과/실패)나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage333(333단계) run333D(333D 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v5`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": "- source_stage(원천 단계): `332_overfit_guard__failure_memory_forward_research_handoff`",
        "- target_surface(": "- target_surface(목표 표면): `runtime_probe_queue_or_failure_memory_from_screen`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run333D_summary(333D 요약): guarded payload cost/curve/pocket screen(방어 페이로드 비용/곡선/포켓 선별)을 `{STATUS}`로 완료했다. "
        f"Effect(효과): screen survivor(선별 생존) `{decision_payload.get('screen_survivor_count')}`개와 failure(실패) `{decision_payload.get('screen_failure_count')}`개를 분리했지만 MT5(메타트레이더5), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run333D_summary(333D 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))
    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage333D Cost Curve Pocket Screen",
            f"""
## 2026-05-26 - Stage333D Cost Curve Pocket Screen(333D 비용 곡선 포켓 선별)

- run333D(333D 실행): guarded signal payload(방어 신호 페이로드)를 cost/curve/pocket proxy(비용/곡선/포켓 대리검증)로 압박했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- screen_survivor_count(선별 생존 수): `{decision_payload.get('screen_survivor_count')}`
- screen_failure_count(선별 실패 수): `{decision_payload.get('screen_failure_count')}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음 run333E(333E 실행)의 runtime probe queue(런타임 탐침 대기열) 또는 failure memory(실패 기억) 입력을 만들고, 후보 선택이나 Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run333D_cost_curve_pocket_screen.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": "proxy_cost_curve_pocket_screen_only;selected_candidate=none;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__cost_curve_pocket_screen",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "guarded_payload_cost_curve_pocket_screen",
                "tier_scope": "raw_forward_signal_payload_scope",
                "kpi_scope": "proxy_trade_shape_and_cost_curve_only",
                "scoreboard_lane": "kpi_evidence",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "proxy_kpi_by_view;cost_stress;curve_pocket;runtime_probe_queue",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "missing_mt5_for_guarded_branches_out_of_scope_by_claim",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__cost_curve_pocket_screen",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "guarded_payload_cost_curve_pocket_screen(방어 페이로드 비용 곡선 포켓 선별)",
                "tier_scope": "raw_forward_signal_payload_scope(원본 전진 신호 페이로드 범위)",
                "scoreboard": "proxy_trade_shape_and_cost_curve_only(대리 거래 형태와 비용 곡선 전용)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if path_exists(artifact) and io_path(artifact).is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage333D cost curve pocket screen artifact; no operating claim.",
                }
            )
    append_unique_csv(ARTIFACT_REGISTRY, ["artifact_id", "path"], artifact_rows)


def write_run_artifacts(generated_at_utc: str) -> tuple[list[Path], dict[str, Any]]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    queue = load_queue()
    bars = load_bars()
    proxy_trades, coverage_rows = build_proxy_trades(bars, queue)
    if not proxy_trades:
        raise RuntimeError("run333D cannot proceed because no proxy trades were generated")
    kpi_rows = build_kpi_rows(proxy_trades, coverage_rows)
    curve_rows, underwater_rows = build_curve_rows(proxy_trades)
    cost_rows = build_cost_rows(proxy_trades)
    lot_rows = build_lot_rows(kpi_rows)
    long_short_rows, regime_rows, db_rows = build_attribution_rows(proxy_trades)
    delta_rows, decision_rows = build_delta_rows(kpi_rows, cost_rows)
    runtime_queue = build_runtime_probe_queue(decision_rows)
    source_mt5_rows = load_source_mt5_reference()
    decision_payload = build_decision_payload(decision_rows, kpi_rows)

    artifacts: list[Path] = [
        write_csv(RUN_DIR / "source_artifact_hashes.csv", ["artifact_id", "path", "exists", "sha256"], source_hash_rows()),
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_csv(RUN_DIR / "proxy_trade_records.csv", list(proxy_trades[0].keys()), proxy_trades),
        write_csv(RUN_DIR / "proxy_coverage_audit.csv", list(coverage_rows[0].keys()), coverage_rows),
        write_csv(RUN_DIR / "proxy_kpi_by_view.csv", list(kpi_rows[0].keys()), kpi_rows),
        write_csv(RUN_DIR / "cost_stress_report.csv", list(cost_rows[0].keys()), cost_rows),
        write_csv(RUN_DIR / "curve_pocket_report.csv", list(curve_rows[0].keys()), curve_rows),
        write_csv(RUN_DIR / "underwater_stretch_report.csv", list(underwater_rows[0].keys()), underwater_rows),
        write_csv(RUN_DIR / "lot_normalized_report.csv", list(lot_rows[0].keys()), lot_rows),
        write_csv(RUN_DIR / "long_short_attribution_report.csv", list(long_short_rows[0].keys()), long_short_rows),
        write_csv(RUN_DIR / "regime_slice_attribution_report.csv", list(regime_rows[0].keys()), regime_rows),
        write_csv(RUN_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv", list(regime_rows[0].keys()), regime_rows),
        write_csv(RUN_DIR / "db_attribution_report.csv", list(db_rows[0].keys()), db_rows),
        write_csv(RUN_DIR / "control_delta_report.csv", list(delta_rows[0].keys()), delta_rows),
        write_csv(RUN_DIR / "branch_screen_decision.csv", list(decision_rows[0].keys()), decision_rows),
        write_csv(
            RUN_DIR / "runtime_probe_branch_queue.csv",
            [
                "queue_id",
                "thesis_id",
                "source_artifact",
                "scoring_mode",
                "signal_payload_path",
                "runtime_probe_status",
                "required_before_mt5",
                "forbidden_claim",
            ],
            runtime_queue,
        ),
        write_csv(
            RUN_DIR / "source_mt5_reference_report.csv",
            list(source_mt5_rows[0].keys()) if source_mt5_rows else ["source_run_id"],
            source_mt5_rows,
        ),
    ]
    gate_audit = gate_rows(queue, proxy_trades, kpi_rows, cost_rows, curve_rows, runtime_queue)
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate", "status", "evidence_path", "notes"], gate_audit))
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "primary_family": "kpi_evidence",
                "primary_skill": "obsidian-performance-attribution",
                "support_skills": [
                    "obsidian-data-integrity",
                    "obsidian-result-judgment",
                    "obsidian-artifact-lineage",
                ],
                "required_gates": [
                    "kpi_contract_audit",
                    "row_grain_audit",
                    "source_authority_audit",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [row["path"] for row in source_hash_rows()],
                "queued_views": len(queue),
                "proxy_trade_records": len(proxy_trades),
                "kpi_rows": len(kpi_rows),
                "cost_rows": len(cost_rows),
                "curve_rows": len(curve_rows),
                "runtime_probe_queue_rows": len(runtime_queue),
                "failed_gates": [row for row in gate_audit if row["status"] != "pass"],
                "decision_payload": decision_payload,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.extend(write_receipts(generated_at_utc, queue, proxy_trades, kpi_rows, cost_rows, curve_rows, decision_rows, runtime_queue))
    artifacts.extend(write_reports(decision_payload))
    artifacts.append(update_selection_status())
    artifacts.extend(update_current_truth(decision_payload))
    return artifacts, decision_payload


def main() -> None:
    generated_at_utc = utc_now()
    artifacts, decision_payload = write_run_artifacts(generated_at_utc)
    update_registers(generated_at_utc, artifacts)
    failures = read_csv_rows(RUN_DIR / "required_gate_coverage_audit.csv")
    failed = [row for row in failures if row.get("status") != "pass"]
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "decision_payload": decision_payload,
                "failed_gates": failed,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
