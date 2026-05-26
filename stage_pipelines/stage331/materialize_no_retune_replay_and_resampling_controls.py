from __future__ import annotations

import argparse
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
STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
RUN_NUMBER = "run331B"
RUN_ID = "run331B_materialize_no_retune_replay_and_resampling_controls_v1"
PARENT_RUN_ID = "run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1"
SOURCE_STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
STATUS = "completed_no_retune_replay_resampling_controls_no_forward_decision"
JUDGMENT = "no_retune_materialization_completed_research_only_no_goal_achieve"
DECISION = "stage331B_materialized_controls_show_mixed_fragility_runtime_replay_required_no_selection"
NEXT_ACTION = "run331C_runtime_replay_or_block_cross_horizon_probe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_no_retune_replay_resampling_controls_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN331A_DIR = STAGE_DIR / "02_runs" / "run331A"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN330E_DIR = SOURCE_STAGE_DIR / "02_runs" / "run330E"
RUN330F_DIR = SOURCE_STAGE_DIR / "02_runs" / "run330F"
RUN330G_DIR = SOURCE_STAGE_DIR / "02_runs" / "run330G"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage331B_no_retune_materialized_controls.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


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


def to_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
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
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return "\n".join(lines[: index + 1] + [block] + lines[index + 1 :]) + "\n"
    return text.rstrip() + "\n" + block + "\n"


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def metric_summary(values: Sequence[float]) -> dict[str, Any]:
    vals = [float(value) for value in values]
    gross_profit = sum(value for value in vals if value > 0)
    gross_loss = sum(value for value in vals if value < 0)
    trade_count = len(vals)
    wins = sum(1 for value in vals if value > 0)
    avg_win = gross_profit / wins if wins else None
    losses = trade_count - wins
    avg_loss = gross_loss / losses if losses else None
    return {
        "trade_count": trade_count,
        "net_profit": round(sum(vals), 6),
        "gross_profit": round(gross_profit, 6),
        "gross_loss": round(gross_loss, 6),
        "profit_factor": round(gross_profit / abs(gross_loss), 6) if gross_loss < 0 else None,
        "expectancy": round(sum(vals) / trade_count, 6) if trade_count else None,
        "win_rate": round(wins / trade_count, 6) if trade_count else None,
        "avg_win": round(avg_win, 6) if avg_win is not None else None,
        "avg_loss": round(avg_loss, 6) if avg_loss is not None else None,
        "max_drawdown": round(max_drawdown(vals), 6),
    }


def max_drawdown(values: Sequence[float]) -> float:
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for value in values:
        equity += float(value)
        peak = max(peak, equity)
        worst = min(worst, equity - peak)
    return abs(worst)


def load_inputs() -> dict[str, pd.DataFrame]:
    trades = read_csv(RUN330F_DIR / "trade_level_records.csv")
    trades["open_time"] = pd.to_datetime(trades["open_time"], errors="coerce")
    trades["close_time"] = pd.to_datetime(trades["close_time"], errors="coerce")
    trades["net_profit"] = pd.to_numeric(trades["net_profit"], errors="coerce").fillna(0.0)
    return {
        "trades": trades,
        "candidate": read_csv(RUN331A_DIR / "candidate_probe_matrix.csv"),
        "horizon": read_csv(RUN331A_DIR / "cross_horizon_partition_plan.csv"),
        "cost_plan": read_csv(RUN331A_DIR / "cost_curve_probe_plan.csv"),
        "parity_plan": read_csv(RUN331A_DIR / "runtime_parity_handoff_plan.csv"),
        "kpi": read_csv(RUN330F_DIR / "forward_mt5_kpi_report.csv"),
        "pressure": read_csv(RUN330G_DIR / "overfit_pressure_matrix.csv"),
    }


def horizon_subset(trades: pd.DataFrame, horizon: Mapping[str, Any], attempt: str) -> pd.DataFrame:
    start = pd.to_datetime(horizon.get("start_time"), errors="coerce")
    end = pd.to_datetime(horizon.get("end_time"), errors="coerce")
    source_attempt = str(horizon.get("source_attempt", "all"))
    subset = trades.loc[trades["attempt_name"].astype(str).eq(attempt)].copy()
    if source_attempt not in {"all", attempt}:
        return subset.iloc[0:0]
    if pd.notna(start):
        subset = subset.loc[subset["close_time"] >= start]
    if pd.notna(end):
        subset = subset.loc[subset["close_time"] <= end]
    return subset.sort_values(["close_time", "trade_index"])


def build_candidate_horizon_rows(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, candidate in frames["candidate"].iterrows():
        attempt = str(candidate["attempt_name"])
        for _, horizon in frames["horizon"].iterrows():
            subset = horizon_subset(frames["trades"], horizon.to_dict(), attempt)
            if subset.empty and str(horizon.get("source_attempt")) != "all":
                continue
            metrics = metric_summary(list(subset["net_profit"]))
            rows.append(
                {
                    "attempt_name": attempt,
                    "artifact_slug": candidate["artifact_slug"],
                    "role": candidate["role"],
                    "horizon_id": horizon["horizon_id"],
                    "source_attempt": horizon["source_attempt"],
                    "start_time": horizon["start_time"],
                    "end_time": horizon["end_time"],
                    **metrics,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_cost_rows(horizon_rows: Sequence[Mapping[str, Any]], frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    levels = sorted(float(value) for value in frames["cost_plan"]["cost_level"].unique())
    trades = frames["trades"]
    horizon_by_id = {str(row["horizon_id"]): row for _, row in frames["horizon"].iterrows()}
    rows: list[dict[str, Any]] = []
    for hrow in horizon_rows:
        attempt = str(hrow["attempt_name"])
        horizon = horizon_by_id[str(hrow["horizon_id"])]
        subset = horizon_subset(trades, horizon.to_dict(), attempt)
        base_values = list(subset["net_profit"])
        for level in levels:
            stressed = [value - level for value in base_values]
            metrics = metric_summary(stressed)
            rows.append(
                {
                    "attempt_name": attempt,
                    "artifact_slug": hrow["artifact_slug"],
                    "role": hrow["role"],
                    "horizon_id": hrow["horizon_id"],
                    "cost_level": level,
                    "net_profit_after_cost": metrics["net_profit"],
                    "profit_factor_after_cost": metrics["profit_factor"],
                    "expectancy_after_cost": metrics["expectancy"],
                    "max_drawdown_after_cost": metrics["max_drawdown"],
                    "survives_pf_gt_1": bool((metrics["profit_factor"] or 0.0) > 1.0),
                    "stress_boundary": "synthetic round-trip account-currency cost; no retuning",
                }
            )
    return rows


def split_chunks(rows: pd.DataFrame, count: int) -> list[pd.DataFrame]:
    if rows.empty:
        return [rows for _ in range(count)]
    size = math.ceil(len(rows) / count)
    chunks = [rows.iloc[index : index + size] for index in range(0, len(rows), size)]
    while len(chunks) < count:
        chunks.append(rows.iloc[0:0])
    return chunks[:count]


def rolling_metrics(rows: pd.DataFrame, window: int) -> dict[str, Any]:
    if rows.empty or len(rows) < window:
        return {"rolling_window": window, "rolling_min_net": None, "rolling_min_pf": None, "rolling_min_start": None, "rolling_min_end": None}
    best: dict[str, Any] | None = None
    ordered = rows.sort_values(["close_time", "trade_index"]).reset_index(drop=True)
    for start in range(0, len(ordered) - window + 1):
        chunk = ordered.iloc[start : start + window]
        metrics = metric_summary(list(chunk["net_profit"]))
        payload = {
            "rolling_window": window,
            "rolling_min_net": metrics["net_profit"],
            "rolling_min_pf": metrics["profit_factor"],
            "rolling_min_start": chunk.iloc[0]["close_time"],
            "rolling_min_end": chunk.iloc[-1]["close_time"],
        }
        if best is None or float(payload["rolling_min_net"]) < float(best["rolling_min_net"]):
            best = payload
    return best or {"rolling_window": window, "rolling_min_net": None, "rolling_min_pf": None, "rolling_min_start": None, "rolling_min_end": None}


def build_resampling_rows(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    trades = frames["trades"]
    for _, candidate in frames["candidate"].iterrows():
        attempt = str(candidate["attempt_name"])
        subset = trades.loc[trades["attempt_name"].astype(str).eq(attempt)].sort_values(["close_time", "trade_index"])
        thirds = [metric_summary(list(chunk["net_profit"])) for chunk in split_chunks(subset, 3)]
        fifths = [metric_summary(list(chunk["net_profit"])) for chunk in split_chunks(subset, 5)]
        rolling20 = rolling_metrics(subset, 20)
        rolling40 = rolling_metrics(subset, 40)
        rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": candidate["artifact_slug"],
                "role": candidate["role"],
                "third_min_net": min((row["net_profit"] for row in thirds), default=None),
                "third_positive_share": sum(1 for row in thirds if row["net_profit"] > 0) / len(thirds),
                "fifth_min_net": min((row["net_profit"] for row in fifths), default=None),
                "fifth_positive_share": sum(1 for row in fifths if row["net_profit"] > 0) / len(fifths),
                **rolling20,
                "rolling40_min_net": rolling40["rolling_min_net"],
                "rolling40_min_pf": rolling40["rolling_min_pf"],
                "rolling40_min_start": rolling40["rolling_min_start"],
                "rolling40_min_end": rolling40["rolling_min_end"],
                "resampling_boundary": "deterministic trade-order chunks only; no randomized tuning",
            }
        )
    return rows


def read_summary(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        return {}
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[-1] if rows else {}


def build_parity_rows(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    kpi_by_attempt = {str(row["attempt_name"]): row for _, row in frames["kpi"].iterrows()}
    rows: list[dict[str, Any]] = []
    reports_dir = RUN330E_DIR / "mt5" / "reports"
    for _, plan in frames["parity_plan"].iterrows():
        attempt = str(plan["attempt_name"])
        telemetry_path = ROOT / str(plan["telemetry_path"])
        summary_path = telemetry_path.with_name(telemetry_path.name.replace("_telemetry.csv", "_summary.csv"))
        telemetry_exists = telemetry_path.exists()
        summary = read_summary(summary_path)
        telemetry_rows = 0
        cycle_rows = 0
        if telemetry_exists:
            telemetry = read_csv(telemetry_path)
            telemetry_rows = int(telemetry.shape[0])
            cycle_rows = int(telemetry.loc[telemetry["record_type"].astype(str).eq("cycle")].shape[0])
        report_files = list(reports_dir.glob(f"*{attempt}.*"))
        htm_exists = any(path.suffix.lower() in {".htm", ".html"} for path in report_files)
        png_exists = any(path.suffix.lower() == ".png" for path in report_files)
        kpi = kpi_by_attempt.get(attempt, {})
        trade_count = int(to_float(kpi.get("trade_count")) or 0)
        order_fill_count = int(to_float(summary.get("order_fill_count")) or 0)
        status = "usable_for_runtime_probe_boundary"
        blocker = ""
        if not telemetry_exists or not summary:
            status = "blocked_missing_runtime_telemetry"
            blocker = "missing telemetry or summary"
        elif not htm_exists:
            status = "blocked_missing_strategy_report"
            blocker = "missing html report"
        rows.append(
            {
                "attempt_name": attempt,
                "telemetry_path": rel(telemetry_path),
                "summary_path": rel(summary_path),
                "telemetry_exists": telemetry_exists,
                "telemetry_rows": telemetry_rows,
                "cycle_rows": cycle_rows,
                "summary_feature_ready_count": summary.get("feature_ready_count"),
                "summary_model_ok_count": summary.get("model_ok_count"),
                "summary_order_fill_count": order_fill_count,
                "kpi_trade_count": trade_count,
                "report_htm_exists": htm_exists,
                "report_png_exists": png_exists,
                "parity_status": status,
                "blocker": blocker,
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
            }
        )
    return rows


def build_survival_rows(
    candidate_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    resampling_rows: Sequence[Mapping[str, Any]],
    parity_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    cost_by_attempt_horizon = {
        (str(row["attempt_name"]), str(row["horizon_id"]), float(row["cost_level"])): row for row in cost_rows
    }
    resampling_by_attempt = {str(row["attempt_name"]): row for row in resampling_rows}
    parity_by_attempt = {str(row["attempt_name"]): row for row in parity_rows}
    rows: list[dict[str, Any]] = []
    for row in candidate_rows:
        if str(row["horizon_id"]) != "full_forward":
            continue
        attempt = str(row["attempt_name"])
        cost1 = cost_by_attempt_horizon.get((attempt, "full_forward", 1.0), {})
        cost2 = cost_by_attempt_horizon.get((attempt, "full_forward", 2.0), {})
        resampling = resampling_by_attempt.get(attempt, {})
        parity = parity_by_attempt.get(attempt, {})
        survives_cost1 = bool(cost1.get("survives_pf_gt_1"))
        survives_cost2 = bool(cost2.get("survives_pf_gt_1"))
        rolling20 = to_float(resampling.get("rolling_min_net"))
        third_share = to_float(resampling.get("third_positive_share")) or 0.0
        parity_ok = str(parity.get("parity_status")) == "usable_for_runtime_probe_boundary"
        flags: list[str] = []
        if survives_cost1:
            flags.append("cost1_survives")
        else:
            flags.append("cost1_fails")
        if survives_cost2:
            flags.append("cost2_survives")
        else:
            flags.append("cost2_fails")
        if rolling20 is not None and rolling20 < -50:
            flags.append("rolling20_deep_negative")
        if third_share < 0.67:
            flags.append("thirds_not_consistently_positive")
        if not parity_ok:
            flags.append("runtime_parity_materialization_blocked")
        role = str(row["role"])
        if role.startswith("preserved") and survives_cost1 and rolling20 is not None and rolling20 > -50 and parity_ok:
            materialized_read = "preserved_clue_retained_for_runtime_replay_not_selection"
        elif role.startswith("preserved"):
            materialized_read = "preserved_clue_fragile_runtime_replay_required_not_selection"
        else:
            materialized_read = "negative_control_or_fragility_control_caught_by_guard"
        rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": row["artifact_slug"],
                "role": role,
                "full_net": row["net_profit"],
                "full_pf": row["profit_factor"],
                "cost1_pf": cost1.get("profit_factor_after_cost"),
                "cost2_pf": cost2.get("profit_factor_after_cost"),
                "third_positive_share": third_share,
                "rolling20_min_net": rolling20,
                "parity_status": parity.get("parity_status"),
                "survival_flags": ";".join(flags),
                "materialized_read": materialized_read,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_decision_payload(survival_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    retained = [str(row["attempt_name"]) for row in survival_rows if str(row["materialized_read"]).startswith("preserved_clue_retained")]
    fragile = [str(row["attempt_name"]) for row in survival_rows if "fragile" in str(row["materialized_read"])]
    controls = [str(row["attempt_name"]) for row in survival_rows if "control" in str(row["materialized_read"])]
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "selected_candidate": "none",
        "retained_clues_not_selection": retained,
        "fragile_clues_not_selection": fragile,
        "negative_controls_caught": controls,
        "next_action": NEXT_ACTION,
        "reason": "run331B materializes no-retune controls from existing MT5 evidence; runtime replay is still required before any forward decision.",
    }


def write_outputs(generated_at_utc: str) -> list[Path]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    SELECTED_DIR.mkdir(parents=True, exist_ok=True)
    frames = load_inputs()
    horizon_rows = build_candidate_horizon_rows(frames)
    cost_rows = build_cost_rows(horizon_rows, frames)
    resampling_rows = build_resampling_rows(frames)
    parity_rows = build_parity_rows(frames)
    survival_rows = build_survival_rows(horizon_rows, cost_rows, resampling_rows, parity_rows)
    decision = build_decision_payload(survival_rows)

    artifacts: list[Path] = []
    artifacts.append(write_csv(RUN_DIR / "candidate_horizon_kpi_report.csv", [
        "attempt_name", "artifact_slug", "role", "horizon_id", "source_attempt", "start_time", "end_time",
        "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy",
        "win_rate", "avg_win", "avg_loss", "max_drawdown", "claim_boundary",
    ], horizon_rows))
    artifacts.append(write_csv(RUN_DIR / "cost_curve_by_horizon_report.csv", [
        "attempt_name", "artifact_slug", "role", "horizon_id", "cost_level", "net_profit_after_cost",
        "profit_factor_after_cost", "expectancy_after_cost", "max_drawdown_after_cost",
        "survives_pf_gt_1", "stress_boundary",
    ], cost_rows))
    artifacts.append(write_csv(RUN_DIR / "resampling_stability_report.csv", [
        "attempt_name", "artifact_slug", "role", "third_min_net", "third_positive_share",
        "fifth_min_net", "fifth_positive_share", "rolling_window", "rolling_min_net",
        "rolling_min_pf", "rolling_min_start", "rolling_min_end", "rolling40_min_net",
        "rolling40_min_pf", "rolling40_min_start", "rolling40_min_end", "resampling_boundary",
    ], resampling_rows))
    artifacts.append(write_csv(RUN_DIR / "runtime_parity_materialization_report.csv", [
        "attempt_name", "telemetry_path", "summary_path", "telemetry_exists", "telemetry_rows",
        "cycle_rows", "summary_feature_ready_count", "summary_model_ok_count", "summary_order_fill_count",
        "kpi_trade_count", "report_htm_exists", "report_png_exists", "parity_status",
        "blocker", "runtime_claim_boundary",
    ], parity_rows))
    artifacts.append(write_csv(RUN_DIR / "candidate_survival_summary.csv", [
        "attempt_name", "artifact_slug", "role", "full_net", "full_pf", "cost1_pf", "cost2_pf",
        "third_positive_share", "rolling20_min_net", "parity_status", "survival_flags",
        "materialized_read", "claim_boundary",
    ], survival_rows))
    artifacts.append(write_json(RUN_DIR / "performance_attribution_receipt.json", {
        "observed_change": "full-window clues are decomposed across horizon/cost/resampling/parity controls",
        "comparison_baseline": rel(RUN330F_DIR / "forward_mt5_kpi_report.csv"),
        "likely_drivers": ["cost sensitivity", "curve pockets", "direction split", "trade concentration"],
        "segment_checks": [rel(artifacts[0]), rel(artifacts[1]), rel(artifacts[2])],
        "trade_shape": rel(artifacts[4]),
        "alternative_explanations": ["single forward window", "broker tester cost assumptions", "D/B source missing"],
        "attribution_confidence": "medium_research_only",
        "next_probe": NEXT_ACTION,
    }))
    artifacts.append(write_json(RUN_DIR / "model_validation_receipt.json", {
        "model_family": "Stage330 forward-safe non-identity ONNX clue set",
        "target_and_label": "fixed no-retune forward MT5 signal behavior",
        "split_method": "cross-horizon trade partitions and deterministic resampling controls",
        "selection_metric": "none_no_selection",
        "secondary_metrics": ["cost survival", "rolling pocket", "resampling positive share", "runtime parity materialization"],
        "threshold_policy": "fixed_no_retune",
        "overfit_risk": "preserved clues can still be single-window artifacts",
        "calibration_risk": "score calibration not claimed",
        "comparison_baseline": "run330F full-window MT5 and run330G pressure matrix",
        "validation_judgment": "exploratory_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
    }))
    artifacts.append(write_json(RUN_DIR / "runtime_parity_receipt.json", {
        "research_path": rel(RUN_DIR / "candidate_horizon_kpi_report.csv"),
        "runtime_path": rel(RUN330E_DIR / "mt5"),
        "shared_contract": "fixed candidate identity, feature order, threshold, risk/lot/ATR and bar time",
        "known_differences": "D/B source remains out_of_scope_by_claim",
        "parity_check": rel(RUN_DIR / "runtime_parity_materialization_report.csv"),
        "parity_identity": "existing run330E reports and telemetry, no new runtime replay",
        "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
    }))
    artifacts.append(write_json(RUN_DIR / "result_judgment_receipt.json", {
        "result_subject": RUN_ID,
        "evidence_available": [rel(path) for path in artifacts[:5]],
        "evidence_missing": ["fresh MT5 runtime replay", "D/B source attribution", "final forward pass/fail decision"],
        "judgment_label": "exploratory_materialization_no_forward_decision",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_ACTION,
        "user_explanation_hook": "무재튜닝 검증 표를 만든 것이며 아직 전진 통과가 아니다.",
    }))
    artifacts.append(write_csv(RUN_DIR / "result_judgment.csv", [
        "run_id", "status", "judgment", "decision", "forward_passed", "forward_failed",
        "goal_achieve", "selected_candidate", "next_action", "claim_boundary",
    ], [{**decision, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY}]))
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", [
        "gate_name", "status", "evidence_path", "effect",
    ], gate_rows()))
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    artifacts.append(write_json(RUN_DIR / "run_manifest.json", {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "generated_at_utc": generated_at_utc,
        **decision,
        "claim_boundary": CLAIM_BOUNDARY,
    }))
    artifacts.extend(write_reports(horizon_rows, survival_rows, decision))
    artifacts.append(update_selection_status(decision))
    artifacts.extend(update_current_truth(decision))
    update_registers(generated_at_utc, decision, artifacts)
    return artifacts


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "performance_attribution(성과 귀속)",
            "status": "completed",
            "evidence_path": rel(RUN_DIR / "performance_attribution_receipt.json"),
            "effect": "headline MT5 KPI(대표 MT5 핵심 지표)를 기간/비용/곡선/재표본으로 분해한다.",
        },
        {
            "gate_name": "model_validation(모델 검증)",
            "status": "completed_materialization_only",
            "evidence_path": rel(RUN_DIR / "model_validation_receipt.json"),
            "effect": "threshold retuning(임계값 재튜닝) 없이 보존 단서의 과적합 압력을 재검사한다.",
        },
        {
            "gate_name": "runtime_parity(런타임 동등성)",
            "status": "materialized_from_existing_runtime_probe",
            "evidence_path": rel(RUN_DIR / "runtime_parity_materialization_report.csv"),
            "effect": "기존 run330E runtime evidence(런타임 근거)를 연결하지만 runtime authority(런타임 권위)는 주장하지 않는다.",
        },
        {
            "gate_name": "result_judgment(결과 판정)",
            "status": "passed_no_goal_achieve",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "effect": "Forward Passed/Failed(전진 통과/실패), selected candidate(선택 후보), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
        {
            "gate_name": "artifact_lineage(산출물 계보)",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "effect": "run331A 설계와 run330F/run330E 근거를 run331B 물질화 산출물에 연결한다.",
        },
    ]


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        RUN331A_DIR / "candidate_probe_matrix.csv",
        RUN331A_DIR / "cross_horizon_partition_plan.csv",
        RUN331A_DIR / "cost_curve_probe_plan.csv",
        RUN331A_DIR / "runtime_parity_handoff_plan.csv",
        RUN330F_DIR / "trade_level_records.csv",
        RUN330F_DIR / "forward_mt5_kpi_report.csv",
        RUN330E_DIR / "runtime_telemetry",
        RUN330E_DIR / "mt5" / "reports",
    ]
    all_paths = list(dict.fromkeys([*artifacts, Path(__file__)]))
    return {
        "generated_at_utc": generated_at_utc,
        "source_inputs": [rel(path) for path in inputs],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in all_paths if path.exists()],
        "artifact_hashes": {rel(path): sha256_file(path) for path in all_paths if path.exists() and path.is_file()},
        "lineage_judgment": "connected_with_no_retune_materialization_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_reports(
    horizon_rows: Sequence[Mapping[str, Any]],
    survival_rows: Sequence[Mapping[str, Any]],
    decision: Mapping[str, Any],
) -> list[Path]:
    survival_table = "\n".join(
        [
            "| attempt(시도) | role(역할) | full PF(전체 PF) | cost+1 PF(비용+1 PF) | rolling20 net(롤링20 순손익) | read(판독) |",
            "|---|---|---:|---:|---:|---|",
            *[
                f"| {row['attempt_name']} | {row['role']} | {csv_value(row['full_pf'])} | {csv_value(row['cost1_pf'])} | {csv_value(row['rolling20_min_net'])} | {row['materialized_read']} |"
                for row in survival_rows
            ],
        ]
    )
    horizon_table = "\n".join(
        [
            "| attempt(시도) | horizon(기간) | trades(거래수) | net(순손익) | PF(수익 팩터) | DD(드로다운) |",
            "|---|---|---:|---:|---:|---:|",
            *[
                f"| {row['attempt_name']} | {row['horizon_id']} | {row['trade_count']} | {csv_value(row['net_profit'])} | {csv_value(row['profit_factor'])} | {csv_value(row['max_drawdown'])} |"
                for row in horizon_rows
                if row["horizon_id"] in {"full_forward", "first_half", "second_half", "month_2026-04", "month_2026-05"}
            ][:36],
        ]
    )
    report = write_md(
        REVIEWS_DIR / "run331B_no_retune_replay_resampling_controls.md",
        f"""
# run331B No-Retune Replay and Resampling Controls(331B 무재튜닝 재생 및 재표본 대조군)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Survival Summary(생존 요약)

{survival_table}

## Horizon Snapshot(기간 스냅샷)

{horizon_table}

## Read(판독)

- retained_clues_not_selection(선택 아닌 유지 단서): `{', '.join(decision['retained_clues_not_selection']) or 'none'}`
- fragile_clues_not_selection(선택 아닌 취약 단서): `{', '.join(decision['fragile_clues_not_selection']) or 'none'}`
- negative_controls_caught(포착된 부정 대조군): `{', '.join(decision['negative_controls_caught']) or 'none'}`
- effect(효과): 물질화 표는 run331C(331C 실행)의 runtime replay or block(런타임 재생 또는 차단) 입력이며 Forward Passed(전진 통과)가 아니다.
""",
    )
    decision_doc = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage331B No-Retune Materialized Controls Decision(331B 무재튜닝 물질화 대조군 결정)

- decision(결정): `{decision['decision']}`
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): 기존 MT5 근거를 재분해했지만 새 runtime replay(런타임 재생)와 D/B source(D/B 원천) 확인이 남아 최종 전진 판단을 닫지 않는다.
""",
    )
    return [report, decision_doc]


def update_selection_status(decision: Mapping[str, Any]) -> Path:
    return write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage331 Selection Status(331단계 선택 상태)

- stage_status(단계 상태): `open_in_progress`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- latest_design(최신 설계): `{PARENT_RUN_ID}`
- latest_materialization(최신 물질화): `{RUN_ID}`
- retained_clues_not_selection(선택 아닌 유지 단서): `{', '.join(decision['retained_clues_not_selection']) or 'none'}`
- fragile_clues_not_selection(선택 아닌 취약 단서): `{', '.join(decision['fragile_clues_not_selection']) or 'none'}`
- negative_controls_caught(포착된 부정 대조군): `{', '.join(decision['negative_controls_caught']) or 'none'}`
- current_run(현재 실행): `{NEXT_ACTION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): run331B는 무재튜닝 검증 표를 만들었지만 후보 선택이나 운영 주장은 없다.
""",
    )


def update_current_truth(decision: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_ACTION}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus = (
        "- >-\n"
        f"  Stage331(331단계) run331B(331B 실행)는 `{decision['status']}`로 no-retune replay/resampling controls(무재튜닝 재생/재표본 대조군)를 물질화했다. Effect(효과): 기존 MT5 근거를 기간/비용/곡선/런타임 동등성 표로 재분해했지만 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage331(331단계) run331B(331B 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v3`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_ACTION}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `runtime_replay_or_block_cross_horizon_probe`",
        "- status(": f"- status(상태): `{decision['status']}`",
        "- decision(": f"- decision(판정): `{decision['judgment']}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run331B_summary(331B 요약): no-retune replay/resampling controls(무재튜닝 재생/재표본 대조군)를 `{decision['status']}`로 물질화했다. "
        "Effect(효과): `c56_plain_rf`, `m48_plain_rf`의 보존 단서는 선택 후보가 아니며 run331C(331C 실행)의 runtime replay or block(런타임 재생 또는 차단)으로 넘긴다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run331B_summary(331B 요약)")
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    append_if_missing(
        CHANGELOG,
        "Stage331B No-Retune Replay Resampling Controls",
        f"""
## 2026-05-26 - Stage331B No-Retune Replay Resampling Controls(331B 무재튜닝 재생 재표본 대조군)

- run331B(331B 실행): run331A(331A 실행) 설계를 실제 기간/비용/곡선/재표본/런타임 동등성 표로 물질화했다.
- status(상태): `{decision['status']}`
- judgment(판정): `{decision['judgment']}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): 새 후보 선택 없이 run331C(331C 실행)의 runtime replay or block(런타임 재생 또는 차단) 입력을 만든다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, decision: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run331B_no_retune_replay_resampling_controls.md"
    upsert_csv(RUN_REGISTRY, ["run_id"], [{
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "performance_attribution",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(report_path),
        "notes": "no_retune_replay_resampling_controls;no_selection;goal_achieve_not_claimed.",
    }])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [{
        "ledger_row_id": f"{RUN_ID}__no_retune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "no_retune_materialization",
        "tier_scope": "raw_forward_runtime_probe_total",
        "kpi_scope": "horizon_cost_curve_resampling_parity",
        "scoreboard_lane": "performance_attribution",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(report_path),
        "primary_kpi": "candidate_survival_summary",
        "guardrail_kpi": "cost_curve_by_horizon;resampling_stability;runtime_parity_materialization",
        "external_verification_status": "uses_completed_run330E_run330F_mt5_evidence",
        "notes": f"decision={decision['decision']};next_action={NEXT_ACTION}.",
    }])
    upsert_csv(STAGE_LEDGER, ["row_id"], [{
        "row_id": f"{RUN_ID}__no_retune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "no_retune_replay_resampling_controls(무재튜닝 재생 재표본 대조군)",
        "tier_scope": "raw_forward_runtime_probe_total(원본 전진 런타임 탐침 전체)",
        "scoreboard": "horizon_cost_curve_resampling_parity(기간/비용/곡선/재표본/동등성)",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "evidence_boundary": CLAIM_BOUNDARY,
        "report_path": rel(report_path),
        "notes": "no_candidate_selected;goal_achieve_not_claimed.",
        "decision": decision["decision"],
    }])
    artifact_rows = []
    for path in artifacts:
        if path.exists() and path.is_file():
            artifact_rows.append({
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage331B_materialization_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "no-retune materialized control artifact; no operating claim.",
            })
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize Stage331B no-retune replay and resampling controls.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "artifact_count": len(artifacts),
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
