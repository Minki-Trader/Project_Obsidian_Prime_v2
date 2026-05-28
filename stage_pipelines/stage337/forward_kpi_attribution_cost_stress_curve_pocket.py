from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import median
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402
from stage_pipelines.stage337 import materialize_common_files_and_run_argmax_parity_probe as el  # noqa: E402
from stage_pipelines.stage337 import refresh_survivor_feature_handoff_and_surface_reprobe as eo  # noqa: E402
from stage_pipelines.stage337 import top3_weight_contract_refresh_and_runtime_probe as ep  # noqa: E402


RUN_NUMBER = "run337EQ"
RUN_ID = "run337EQ_forward_kpi_attribution_cost_stress_curve_pocket_without_db_v1"
PARENT_RUN_ID = ep.RUN_ID
NEXT_RUN_ID = "run337ER_forward_decision_review_or_failure_memory_without_db_v1"
STAGE_ID = ep.STAGE_ID
STAGE_DIR = ep.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REPORT_DIR = MT5_DIR / "reports"
FEATURE_DIR = RUN_DIR / "feature_matrices"
MODEL_DIR = RUN_DIR / "models"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"

ATTEMPT_PACKAGE = RUN_DIR / "forward_kpi_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXPECTED_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
MT5_REPORT_SUMMARY = RUN_DIR / "frozen_forward_mt5_report.csv"
TRADE_RECORDS = RUN_DIR / "trade_records.csv"
PARSER_CHECKS = RUN_DIR / "trade_report_parser_checks.csv"
PARSER_ERRORS = RUN_DIR / "trade_report_parser_errors.csv"
REGIME_ATTRIBUTION = RUN_DIR / "regime_attribution_report.csv"
DB_ATTRIBUTION = RUN_DIR / "db_attribution_report.csv"
LOT_NORMALIZED = RUN_DIR / "lot_normalized_report.csv"
COST_STRESS = RUN_DIR / "cost_stress_report.csv"
CURVE_POCKET = RUN_DIR / "curve_pocket_report.csv"
SIGNAL_ATTRIBUTION = RUN_DIR / "signal_attribution_report.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_forward_decision_report.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

CLAIM_BOUNDARY = (
    "research_development_only_stage337EQ_forward_kpi_attribution_cost_stress_curve_pocket_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_"
    "no_goal_achieve"
)
STATUS_COMPLETED = "completed_stage337EQ_forward_kpi_attribution_cost_stress_curve_pocket_no_goal"
STATUS_BLOCKED = "blocked_stage337EQ_forward_kpi_missing_or_tester_visibility_gap"
DEPOSIT = 500.0
STRESS_POINTS = (0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0)
ROLLING_WINDOWS = (20, 50, 100)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337EQ frozen forward KPI and attribution probe.")
    parser.add_argument("--terminal-path", default=str(bv.DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(bv.DEFAULT_METAEDITOR))
    parser.add_argument("--terminal-data-root", default=str(bv.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--common-files-root", default=str(bv.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(bv.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--from-date", default="2026.04.14")
    parser.add_argument("--to-date", default="2026.05.29")
    parser.add_argument("--attempt-limit", type=int, default=7)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=120)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return str(value)


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], columns: Sequence[str] | None = None) -> Path:
    rows = list(rows)
    fields = list(columns or (rows[0].keys() if rows else ["empty"]))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fields})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def safe_name(value: str, limit: int = 84) -> str:
    keep = []
    for char in value.lower():
        keep.append(char if char.isalnum() else "_")
    return "".join(keep).strip("_")[:limit]


def parse_dt(value: Any) -> pd.Timestamp | None:
    text = str(value or "").strip()
    if not text:
        return None
    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        return None
    return pd.Timestamp(parsed)


def session_bucket(ts: pd.Timestamp | None) -> str:
    if ts is None or pd.isna(ts):
        return "session_missing"
    hour = int(ts.hour)
    if 13 <= hour < 20:
        return "us_cash_core_utc"
    if 20 <= hour < 22:
        return "us_late_utc"
    if 7 <= hour < 13:
        return "europe_to_us_premarket_utc"
    return "overnight_utc"


def chronological_segment(index: int, total: int) -> str:
    if total <= 0:
        return "segment_missing"
    ratio = (index + 1) / total
    if ratio <= 0.25:
        return "q1_early"
    if ratio <= 0.50:
        return "q2"
    if ratio <= 0.75:
        return "q3"
    return "q4_late"


def numeric_bucket(value: Any, name: str, cuts: tuple[float, ...]) -> str:
    x = number(value, math.nan)
    if not math.isfinite(x):
        return f"{name}_missing"
    if x < cuts[0]:
        return f"{name}_low"
    for left, right in zip(cuts, cuts[1:]):
        if left <= x < right:
            return f"{name}_{left:g}_to_{right:g}"
    return f"{name}_high"


def grouped(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[str, ...], list[Mapping[str, Any]]]:
    out: dict[tuple[str, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        out[tuple(str(row.get(key, "")) for key in keys)].append(row)
    return out


def profit_factor(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> float | None:
    gross_profit = sum(number(row.get(key)) for row in rows if number(row.get(key)) > 0.0)
    gross_loss = -sum(number(row.get(key)) for row in rows if number(row.get(key)) < 0.0)
    if gross_loss == 0.0:
        return math.inf if gross_profit > 0.0 else None
    return gross_profit / gross_loss


def max_closed_drawdown(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> tuple[float, int, str, str]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    underwater = 0
    longest = 0
    dd_start = ""
    dd_end = ""
    peak_time = ""
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += number(row.get(key))
        close_time = str(row.get("close_time", ""))
        if balance >= peak:
            peak = balance
            peak_time = close_time
            underwater = 0
        else:
            underwater += 1
            longest = max(longest, underwater)
            dd = peak - balance
            if dd > max_dd:
                max_dd = dd
                dd_start = peak_time
                dd_end = close_time
    return max_dd, longest, dd_start, dd_end


def metrics(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> dict[str, Any]:
    trades = len(rows)
    net = sum(number(row.get(key)) for row in rows)
    winners = [row for row in rows if number(row.get(key)) > 0.0]
    losers = [row for row in rows if number(row.get(key)) < 0.0]
    avg_win = sum(number(row.get(key)) for row in winners) / len(winners) if winners else 0.0
    avg_loss = sum(number(row.get(key)) for row in losers) / len(losers) if losers else 0.0
    max_dd, longest, dd_start, dd_end = max_closed_drawdown(rows, key)
    pf = profit_factor(rows, key)
    return {
        "trade_count": trades,
        "net_profit": net,
        "gross_profit": sum(number(row.get(key)) for row in winners),
        "gross_loss": sum(number(row.get(key)) for row in losers),
        "profit_factor": pf,
        "win_rate": len(winners) / trades if trades else None,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": abs(avg_win / avg_loss) if avg_loss else None,
        "expectancy": net / trades if trades else None,
        "max_closed_drawdown": max_dd,
        "recovery_factor": net / max_dd if max_dd else (math.inf if net > 0 else None),
        "longest_underwater_trade_count": longest,
        "drawdown_start": dd_start,
        "drawdown_end": dd_end,
    }


def point_value_estimate(rows: Sequence[Mapping[str, Any]]) -> float:
    estimates = []
    for row in rows:
        volume = number(row.get("volume"))
        distance = abs(number(row.get("close_price")) - number(row.get("open_price")))
        gross = abs(number(row.get("gross_profit")))
        if volume > 0 and distance > 0 and gross > 0:
            estimates.append(gross / (distance * volume))
    return median(estimates) if estimates else 1.0


def materialize_attempts(args: argparse.Namespace) -> list[dict[str, Any]]:
    common_files = Path(args.common_files_root)
    common_root = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_forward_kpi"
    attempts: list[dict[str, Any]] = []
    sync_rows: list[dict[str, Any]] = []
    expected_rows: list[dict[str, Any]] = []
    for directory in [MT5_DIR, SET_DIR, INI_DIR, REPORT_DIR, FEATURE_DIR, MODEL_DIR, EXPECTED_DIR, TELEMETRY_DIR]:
        io_path(directory).mkdir(parents=True, exist_ok=True)
    for base in el.selected_attempts(args.attempt_limit):
        attempt_name = str(base["attempt_name"])
        feature_order = eo.load_feature_order(str(base["feature_set_id"]))
        frame = pd.read_parquet(io_path(ep.FEATURE_FRAME_DIR / f"{base['feature_set_id']}.parquet"))
        frame = el.date_filter(frame, args.from_date, args.to_date)
        local_features = FEATURE_DIR / f"{attempt_name}_features.csv"
        local_model = MODEL_DIR / f"{attempt_name}.onnx"
        expected_tape = EXPECTED_DIR / f"{attempt_name}_expected_probability_tape.csv"
        mt5.export_mt5_feature_matrix_csv(frame, feature_order, local_features, timestamp_column="timestamp", metadata_columns=("split",))
        shutil.copy2(io_path(Path(base["onnx_path"])), io_path(local_model))
        expected_rows.append(el.write_expected_probability_tape(base, frame, feature_order, expected_tape))
        common_feature_path = f"{common_root}/features/{local_features.name}"
        common_model_path = f"{common_root}/models/{local_model.name}"
        common_telemetry_path = f"{common_root}/telemetry/{attempt_name}_telemetry.csv"
        common_summary_path = f"{common_root}/telemetry/{attempt_name}_summary.csv"
        for old_path in [common_telemetry_path, common_summary_path]:
            target = common_files / Path(old_path)
            if path_exists(target):
                io_path(target).unlink()
        sync_rows.append({"sync_id": f"{attempt_name}::features", **mt5.copy_to_common_files(common_files, local_features, common_feature_path)})
        sync_rows.append({"sync_id": f"{attempt_name}::model", **mt5.copy_to_common_files(common_files, local_model, common_model_path)})
        set_name = f"opv2_{RUN_NUMBER}_{base['probe_id']}.set"
        ini_name = f"opv2_{RUN_NUMBER}_{base['probe_id']}.ini"
        set_path = SET_DIR / f"{attempt_name}.set"
        ini_path = INI_DIR / f"{attempt_name}.ini"
        report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{safe_name(attempt_name, 64)}"
        params = {
            "InpRunId": f"{RUN_ID}_{attempt_name}",
            "InpExplorationLabel": "stage337_ForwardKpiAttribution",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "forward_after_2026_04_14_top3_refreshed",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": int(base["feature_count"]),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": common_model_path,
            "InpModelId": base["model_id"],
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": base["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpShortThreshold": 0.55,
            "InpLongThreshold": 0.55,
            "InpMinMargin": 0.05,
            "InpDecisionMode": "argmax_probe",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": False,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": 3371400 + int(base["proxy_rank"]),
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry_path,
            "InpSummaryCsvPath": common_summary_path,
        }
        mt5.materialize_tester_set_file(params, set_path, generated_by="stage337EQ_forward_kpi")
        tester_config = mt5.TesterMaterializationConfig(
            expert=mt5.EA_EXPERT_PATH,
            symbol="US100",
            period="M5",
            model=4,
            deposit=DEPOSIT,
            leverage="1:100",
            shutdown_terminal=1,
            from_date=args.from_date,
            to_date=args.to_date,
            report=report_name,
        )
        mt5.materialize_tester_ini_file(tester_config, ini_path, set_file_path=Path(set_name))
        attempts.append(
            {
                **base,
                "tier": "Tier A",
                "split": "forward_after_2026_04_14_top3_refreshed",
                "feature_rows": len(frame),
                "feature_first_timestamp": str(pd.to_datetime(frame["timestamp"], utc=True).min()) if len(frame) else "",
                "feature_last_timestamp": str(pd.to_datetime(frame["timestamp"], utc=True).max()) if len(frame) else "",
                "common_telemetry_path": common_telemetry_path,
                "common_summary_path": common_summary_path,
                "common_feature_path": common_feature_path,
                "common_model_path": common_model_path,
                "local_feature_path": rel(local_features),
                "local_model_path": rel(local_model),
                "expected_probability_tape_path": rel(expected_tape),
                "set_name": set_name,
                "ini_name": ini_name,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "ini": {"path": rel(ini_path), "tester": {"Report": report_name}},
                "set": {"path": rel(set_path)},
                "from_date": args.from_date,
                "to_date": args.to_date,
                "allow_trading": True,
                "fixed_lot": 0.10,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ATTEMPT_PACKAGE, attempts)
    write_csv(COMMON_SYNC, sync_rows)
    write_csv(EXPECTED_INDEX, expected_rows)
    return attempts


def run_mt5(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    common_files = Path(args.common_files_root)
    tester_profile = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    compile_result, ea_sync = bv.compile_and_sync_ea(Path(args.metaeditor_path), terminal_data_root)
    terminal_probe = bv.terminal_processes()
    execution: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if args.materialize_only:
        return {
            "compile": compile_result,
            "ea_sync": ea_sync,
            "terminal_process_probe": terminal_probe,
            "execution_results": [{"attempt_name": row["attempt_name"], "status": "not_run_materialize_only"} for row in attempts],
            "strategy_tester_reports": [],
        }
    can_run = compile_result.get("status") == "completed" or path_exists(bv.PORTABLE_EA_EX5)
    if not can_run:
        execution = [{"attempt_name": row["attempt_name"], "status": "blocked", "blocker": "compile_blocked_and_no_portable_ex5"} for row in attempts]
    elif terminal_probe.get("status") != "no_terminal64_process":
        execution = [{"attempt_name": row["attempt_name"], "status": "blocked", "blocker": "terminal64_already_running"} for row in attempts]
    else:
        for attempt in attempts:
            for key in ("common_telemetry_path", "common_summary_path"):
                target = common_files / Path(str(attempt.get(key, "")))
                if path_exists(target):
                    io_path(target).unlink()
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            try:
                tester = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini_path"]),
                    set_path=ROOT / str(attempt["set_path"]),
                    tester_profile_set_path=tester_profile / str(attempt["set_name"]),
                    tester_profile_ini_path=tester_profile / str(attempt["ini_name"]),
                    timeout_seconds=args.timeout_seconds,
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                tester = {
                    "status": "blocked",
                    "returncode": None,
                    "blocker": "terminal_timeout",
                    "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                    "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
                }
            runtime_wait = mt5.wait_for_mt5_runtime_outputs(common_files, attempt, timeout_seconds=args.wait_timeout_seconds, poll_seconds=2.0)
            for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
                src = common_files / Path(str(attempt.get(key, "")))
                if path_exists(src):
                    shutil.copy2(io_path(src), io_path(TELEMETRY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"))
            execution.append(
                {
                    **tester,
                    "runtime_outputs": runtime_wait,
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
                    "feature_set_id": attempt["feature_set_id"],
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
        report_records = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution, report_records)
    payload = {
        "compile": compile_result,
        "ea_sync": ea_sync,
        "terminal_process_probe": terminal_probe,
        "terminal_extra_args": ["/portable"],
        "execution_results": execution,
        "strategy_tester_reports": report_records,
    }
    write_json(MT5_EXECUTION_RESULT, payload)
    return payload


def feature_frame(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(io_path(path))
    frame["_feature_ts"] = pd.to_datetime(frame["bar_time_server"], errors="coerce")
    return frame.sort_values("_feature_ts").reset_index(drop=True)


def feature_at(frame: pd.DataFrame, ts: pd.Timestamp | None) -> Mapping[str, Any]:
    if ts is None or frame.empty:
        return {}
    eligible = frame[frame["_feature_ts"] <= ts]
    if eligible.empty:
        return {}
    return eligible.iloc[-1].to_dict()


def build_mt5_summary(execution: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempt_by_name = {row["attempt_name"]: row for row in attempts}
    rows = []
    for item in execution.get("execution_results", []):
        attempt = attempt_by_name.get(item.get("attempt_name"), {})
        report = item.get("strategy_tester_report", {})
        metrics_payload = report.get("metrics", {})
        summary = item.get("runtime_outputs", {}).get("last_summary", {})
        rows.append(
            {
                "attempt_name": item.get("attempt_name", ""),
                "proxy_rank": attempt.get("proxy_rank", ""),
                "model_id": item.get("model_id", ""),
                "feature_set_id": item.get("feature_set_id", ""),
                "tester_status": item.get("status", ""),
                "report_status": report.get("status", "missing"),
                "feature_rows": attempt.get("feature_rows", ""),
                "feature_last_timestamp": attempt.get("feature_last_timestamp", ""),
                "last_ready_bar_time": summary.get("written_at", ""),
                "feature_ready_count": summary.get("feature_ready_count", ""),
                "long_count": summary.get("long_count", ""),
                "short_count": summary.get("short_count", ""),
                "flat_count": summary.get("flat_count", ""),
                "order_attempt_count": summary.get("order_attempt_count", ""),
                "order_fill_count": summary.get("order_fill_count", ""),
                "net_profit": metrics_payload.get("net_profit", ""),
                "profit_factor": metrics_payload.get("profit_factor", ""),
                "trade_count": metrics_payload.get("trade_count", ""),
                "max_drawdown_amount": metrics_payload.get("max_drawdown_amount", ""),
                "max_drawdown_percent": metrics_payload.get("max_drawdown_percent", ""),
                "recovery_factor": metrics_payload.get("recovery_factor", ""),
                "expectancy": metrics_payload.get("expectancy", ""),
                "short_trade_count": metrics_payload.get("short_trade_count", ""),
                "long_trade_count": metrics_payload.get("long_trade_count", ""),
                "html_report": report.get("html_report", {}).get("path", ""),
                "chart": report.get("chart", {}).get("path", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(MT5_REPORT_SUMMARY, rows)
    return rows


def build_trade_records(execution: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempt_by_name = {row["attempt_name"]: row for row in attempts}
    feature_cache: dict[str, pd.DataFrame] = {}
    rows: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for item in execution.get("execution_results", []):
        attempt_name = str(item.get("attempt_name", ""))
        report = item.get("strategy_tester_report", {})
        report_path = report.get("html_report", {}).get("path", "")
        attempt = attempt_by_name.get(attempt_name, {})
        if not report_path:
            errors.append({"attempt_name": attempt_name, "error": "missing_html_report", "claim_boundary": CLAIM_BOUNDARY})
            continue
        try:
            parsed = parse_mt5_trade_report(Path(report_path))
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:
            errors.append({"attempt_name": attempt_name, "report_path": report_path, "error": str(exc), "claim_boundary": CLAIM_BOUNDARY})
            continue
        expected_count = int(number(report.get("metrics", {}).get("trade_count")))
        checks.append(
            {
                "attempt_name": attempt_name,
                "report_path": report_path,
                "expected_trade_count": expected_count,
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected_count,
                "parser_status": "matched" if len(trades) == expected_count else "count_mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        feature_path = ROOT / str(attempt.get("local_feature_path", ""))
        if feature_path.as_posix() not in feature_cache:
            feature_cache[feature_path.as_posix()] = feature_frame(feature_path)
        features = feature_cache[feature_path.as_posix()]
        point_value = point_value_estimate(
            [
                {
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": trade.gross_profit,
                }
                for trade in trades
            ]
        )
        ordered = sorted(trades, key=lambda trade: trade.close_time)
        for index, trade in enumerate(ordered):
            open_time = parse_dt(trade.open_time)
            close_time = parse_dt(trade.close_time)
            feat = feature_at(features, open_time)
            rows.append(
                {
                    "run_id": RUN_ID,
                    "attempt_name": attempt_name,
                    "proxy_rank": attempt.get("proxy_rank", ""),
                    "model_id": attempt.get("model_id", ""),
                    "feature_set_id": attempt.get("feature_set_id", ""),
                    "db_source_status": "not_available_in_argmax_probe_artifacts",
                    "db_source": "not_available",
                    "decision_surface_mapping": "argmax_short_flat_long_no_D_B_source_columns",
                    "trade_index": trade.index,
                    "direction": trade.direction,
                    "open_time": open_time.strftime("%Y-%m-%d %H:%M:%S") if open_time is not None else "",
                    "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S") if close_time is not None else "",
                    "holding_minutes": (close_time - open_time).total_seconds() / 60.0 if open_time is not None and close_time is not None else "",
                    "holding_bars_m5": (close_time - open_time).total_seconds() / 300.0 if open_time is not None and close_time is not None else "",
                    "month": close_time.strftime("%Y-%m") if close_time is not None else "",
                    "weekday": close_time.strftime("%A") if close_time is not None else "",
                    "open_hour_utc": open_time.strftime("%H") if open_time is not None else "",
                    "close_hour_utc": close_time.strftime("%H") if close_time is not None else "",
                    "session_utc": session_bucket(open_time),
                    "chron_segment": chronological_segment(index, len(ordered)),
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": trade.gross_profit,
                    "net_profit": trade.net_profit,
                    "swap": trade.swap,
                    "commission": trade.commission,
                    "lot_normalized_net_per_1lot": trade.net_profit / trade.volume if trade.volume else None,
                    "point_value_per_lot_estimate": point_value,
                    "feature_timestamp": feat.get("bar_time_server", ""),
                    "atr_14": feat.get("atr_14", ""),
                    "atr_50": feat.get("atr_50", ""),
                    "atr_14_over_atr_50": feat.get("atr_14_over_atr_50", ""),
                    "historical_vol_20": feat.get("historical_vol_20", ""),
                    "historical_vol_5_over_20": feat.get("historical_vol_5_over_20", ""),
                    "adx_14": feat.get("adx_14", ""),
                    "di_spread_14": feat.get("di_spread_14", ""),
                    "rsi_14": feat.get("rsi_14", ""),
                    "minutes_from_cash_open": feat.get("minutes_from_cash_open", ""),
                    "is_us_cash_open": feat.get("is_us_cash_open", ""),
                    "vix_zscore_20": feat.get("vix_zscore_20", ""),
                    "us10yr_zscore_20": feat.get("us10yr_zscore_20", ""),
                    "usdx_zscore_20": feat.get("usdx_zscore_20", ""),
                    "vol_regime": numeric_bucket(feat.get("historical_vol_20"), "vol", (0.08, 0.14, 0.22)),
                    "atr_ratio_regime": numeric_bucket(feat.get("atr_14_over_atr_50"), "atr_ratio", (0.8, 1.0, 1.2)),
                    "adx_regime": numeric_bucket(feat.get("adx_14"), "adx", (20.0, 25.0, 40.0)),
                    "vix_regime": numeric_bucket(feat.get("vix_zscore_20"), "vix_z", (-1.0, 0.0, 1.0)),
                    "rate_regime": numeric_bucket(feat.get("us10yr_zscore_20"), "us10yr_z", (-1.0, 0.0, 1.0)),
                    "usd_regime": numeric_bucket(feat.get("usdx_zscore_20"), "usdx_z", (-1.0, 0.0, 1.0)),
                    "source_report_path": report_path,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(TRADE_RECORDS, rows)
    write_csv(PARSER_CHECKS, checks)
    write_csv(PARSER_ERRORS, errors)
    return rows, checks, errors


def slice_read(item: Mapping[str, Any]) -> str:
    trades = int(number(item.get("trade_count")))
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    recovery = number(item.get("recovery_factor"), math.nan)
    if trades < 5:
        return "too_thin_to_read"
    if net <= 0.0:
        return "negative_slice"
    if math.isfinite(pf) and pf < 1.1:
        return "pf_thin_slice"
    if math.isfinite(recovery) and recovery < 1.0:
        return "recovery_below_one_slice"
    return "constructive_slice"


def build_regime_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = (
        "direction",
        "month",
        "weekday",
        "open_hour_utc",
        "session_utc",
        "chron_segment",
        "vol_regime",
        "atr_ratio_regime",
        "adx_regime",
        "vix_regime",
        "rate_regime",
        "usd_regime",
        "is_us_cash_open",
    )
    rows: list[dict[str, Any]] = []
    for axis in axes:
        for key, items in grouped(trades, ("attempt_name", "proxy_rank", "feature_set_id", axis)).items():
            attempt, proxy_rank, feature_set, bucket = key
            item = metrics(items)
            rows.append(
                {
                    "attempt_name": attempt,
                    "proxy_rank": proxy_rank,
                    "feature_set_id": feature_set,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(REGIME_ATTRIBUTION, rows)
    return rows


def build_db_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, items in grouped(trades, ("attempt_name", "proxy_rank", "feature_set_id", "db_source_status", "db_source", "decision_surface_mapping")).items():
        attempt, proxy_rank, feature_set, status, source, mapping = key
        rows.append(
            {
                "attempt_name": attempt,
                "proxy_rank": proxy_rank,
                "feature_set_id": feature_set,
                "db_source_status": status,
                "db_source": source,
                "decision_surface_mapping": mapping,
                **metrics(items),
                "interpretation": "D/B source columns are not present; direction attribution is provided separately and must not be read as D/B source authority.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for key, items in grouped(trades, ("attempt_name", "proxy_rank", "feature_set_id", "direction")).items():
        attempt, proxy_rank, feature_set, direction = key
        rows.append(
            {
                "attempt_name": attempt,
                "proxy_rank": proxy_rank,
                "feature_set_id": feature_set,
                "db_source_status": "direction_proxy_only",
                "db_source": f"direction_{direction}",
                "decision_surface_mapping": "long_short_attribution_not_D_B_source",
                **metrics(items),
                "interpretation": "Direction attribution exists, but D/B source attribution remains unavailable.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(DB_ATTRIBUTION, rows)
    return rows


def build_lot_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for key, items in grouped(trades, ("attempt_name", "proxy_rank", "feature_set_id")).items():
        attempt, proxy_rank, feature_set = key
        item = metrics(items)
        total_lots = sum(number(row.get("volume")) for row in items)
        lot_values = [number(row.get("volume")) for row in items if number(row.get("volume")) > 0.0]
        rows.append(
            {
                "attempt_name": attempt,
                "proxy_rank": proxy_rank,
                "feature_set_id": feature_set,
                **item,
                "total_lots": total_lots,
                "median_lot": median(lot_values) if lot_values else None,
                "net_per_1lot": item["net_profit"] / total_lots if total_lots else None,
                "lot_policy_read": "fixed_0_10_lot_observed_no_lot_optimization",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(LOT_NORMALIZED, rows)
    return rows


def stress_read(item: Mapping[str, Any]) -> str:
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    if net <= 0.0:
        return "cost_breaks_net"
    if not math.isfinite(pf) or pf < 1.0:
        return "cost_breaks_pf"
    if pf < 1.1:
        return "cost_leaves_pf_below_1_1"
    if pf < 1.2:
        return "cost_thin_pf_1_1_to_1_2"
    return "cost_survives_this_scenario"


def build_cost_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for key, items in grouped(trades, ("attempt_name", "proxy_rank", "feature_set_id")).items():
        attempt, proxy_rank, feature_set = key
        point_value = point_value_estimate(items)
        lots = [number(row.get("volume")) for row in items if number(row.get("volume")) > 0.0]
        med_lot = median(lots) if lots else 0.0
        base = metrics(items)
        breakeven = base["net_profit"] / (len(items) * med_lot * point_value) if items and med_lot and point_value else None
        for stress in STRESS_POINTS:
            stressed = []
            for row in items:
                copy = dict(row)
                copy["stressed_net_profit"] = number(row.get("net_profit")) - stress * number(row.get("volume")) * point_value
                stressed.append(copy)
            item = metrics(stressed, "stressed_net_profit")
            rows.append(
                {
                    "attempt_name": attempt,
                    "proxy_rank": proxy_rank,
                    "feature_set_id": feature_set,
                    "extra_round_trip_points": stress,
                    "point_value_per_1lot_estimate": point_value,
                    "breakeven_extra_round_trip_points_estimate": breakeven,
                    **item,
                    "stress_read": stress_read(item),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(COST_STRESS, rows)
    return rows


def rolling_pocket(items: Sequence[Mapping[str, Any]], window: int) -> dict[str, Any]:
    ordered = sorted(items, key=lambda row: str(row.get("close_time")))
    if len(ordered) < window:
        return {"window_trades": window, "pocket_status": "not_enough_trades", "net_profit": None, "pocket_start": "", "pocket_end": ""}
    worst = {"net_profit": math.inf, "pocket_start": "", "pocket_end": ""}
    for start in range(0, len(ordered) - window + 1):
        chunk = ordered[start : start + window]
        net = sum(number(row.get("net_profit")) for row in chunk)
        if net < number(worst.get("net_profit"), math.inf):
            worst = {"net_profit": net, "pocket_start": chunk[0].get("close_time", ""), "pocket_end": chunk[-1].get("close_time", "")}
    worst["window_trades"] = window
    worst["pocket_status"] = "computed"
    return worst


def curve_read(item: Mapping[str, Any], worst: Mapping[str, Any], one_point: Mapping[str, Any], five_point: Mapping[str, Any]) -> str:
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    recovery = number(item.get("recovery_factor"), math.nan)
    worst_net = number(worst.get("net_profit"))
    one_pf = number(one_point.get("profit_factor"), math.nan)
    five_net = number(five_point.get("net_profit"), math.nan)
    if net <= 0.0 or not math.isfinite(pf) or pf <= 1.0:
        return "negative_or_unprofitable_forward"
    if math.isfinite(one_pf) and one_pf < 1.1:
        return "cost_fragile_forward"
    if math.isfinite(five_net) and five_net <= 0.0:
        return "wide_cost_stress_breaks_net"
    if math.isfinite(recovery) and recovery < 1.0:
        return "recovery_below_one_forward"
    if worst_net < 0.0:
        return "has_negative_curve_pocket"
    return "constructive_forward_shape"


def build_curve_rows(trades: Sequence[Mapping[str, Any]], regime_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    cost_by_attempt = {(row.get("attempt_name"), number(row.get("extra_round_trip_points"))): row for row in cost_rows}
    for key, items in grouped(trades, ("attempt_name", "proxy_rank", "feature_set_id")).items():
        attempt, proxy_rank, feature_set = key
        item = metrics(items)
        relevant = [row for row in regime_rows if row.get("attempt_name") == attempt]
        month_slices = [row for row in relevant if row.get("axis") == "month" and int(number(row.get("trade_count"))) >= 3]
        chron_slices = [row for row in relevant if row.get("axis") == "chron_segment"]
        worst = min(month_slices + chron_slices, key=lambda row: number(row.get("net_profit")), default={})
        negative_months = [row for row in month_slices if number(row.get("net_profit")) < 0.0]
        one_point = cost_by_attempt.get((attempt, 1.0), {})
        five_point = cost_by_attempt.get((attempt, 5.0), {})
        rows.append(
            {
                "attempt_name": attempt,
                "proxy_rank": proxy_rank,
                "feature_set_id": feature_set,
                "pocket_type": "attempt_summary",
                **item,
                "positive_month_ratio": (len(month_slices) - len(negative_months)) / len(month_slices) if month_slices else None,
                "negative_month_count": len(negative_months),
                "worst_slice_axis": worst.get("axis", ""),
                "worst_slice_bucket": worst.get("bucket", ""),
                "worst_slice_net_profit": worst.get("net_profit", ""),
                "one_point_pf": one_point.get("profit_factor", ""),
                "five_point_net_profit": five_point.get("net_profit", ""),
                "curve_read": curve_read(item, worst, one_point, five_point),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for pocket_type, slices in (("worst_month", month_slices), ("worst_chron_segment", chron_slices)):
            pocket = min(slices, key=lambda row: number(row.get("net_profit")), default={})
            if pocket:
                rows.append(
                    {
                        "attempt_name": attempt,
                        "proxy_rank": proxy_rank,
                        "feature_set_id": feature_set,
                        "pocket_type": pocket_type,
                        "axis": pocket.get("axis", ""),
                        "bucket": pocket.get("bucket", ""),
                        "trade_count": pocket.get("trade_count", ""),
                        "net_profit": pocket.get("net_profit", ""),
                        "profit_factor": pocket.get("profit_factor", ""),
                        "max_closed_drawdown": pocket.get("max_closed_drawdown", ""),
                        "recovery_factor": pocket.get("recovery_factor", ""),
                        "curve_read": pocket.get("slice_read", ""),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
        for window in ROLLING_WINDOWS:
            pocket = rolling_pocket(items, window)
            rows.append(
                {
                    "attempt_name": attempt,
                    "proxy_rank": proxy_rank,
                    "feature_set_id": feature_set,
                    "pocket_type": f"worst_rolling_{window}_trades",
                    "trade_count": window,
                    "net_profit": pocket.get("net_profit"),
                    "pocket_start": pocket.get("pocket_start", ""),
                    "pocket_end": pocket.get("pocket_end", ""),
                    "curve_read": "negative_rolling_pocket" if number(pocket.get("net_profit"), math.inf) < 0.0 else pocket.get("pocket_status", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(CURVE_POCKET, rows)
    return rows


def build_signal_rows() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(TELEMETRY_DIR.glob("*_telemetry.csv")):
        attempt_name = path.name.removesuffix("_telemetry.csv")
        cycles = [row for row in read_csv(path) if row.get("record_type") == "cycle"]
        enriched = []
        for row in cycles:
            ts = parse_dt(row.get("bar_time"))
            item = dict(row)
            item["attempt_name"] = attempt_name
            item["hour_utc"] = ts.strftime("%H") if ts is not None else ""
            item["session_utc"] = session_bucket(ts)
            item["order_filled_bool"] = str(row.get("order_filled", "")).lower() == "true"
            enriched.append(item)
        for key, items in grouped(enriched, ("attempt_name", "decision", "hour_utc", "session_utc")).items():
            attempt, decision, hour, session = key
            rows.append(
                {
                    "attempt_name": attempt,
                    "decision": decision,
                    "hour_utc": hour,
                    "session_utc": session,
                    "cycle_count": len(items),
                    "order_fill_count": sum(1 for row in items if row.get("order_filled_bool")),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(SIGNAL_ATTRIBUTION, rows)
    return rows


def latest_feature_timestamp(attempts: Sequence[Mapping[str, Any]]) -> pd.Timestamp | None:
    values = [pd.to_datetime(row.get("feature_last_timestamp"), utc=True, errors="coerce") for row in attempts]
    values = [pd.Timestamp(v) for v in values if not pd.isna(v)]
    return max(values) if values else None


def latest_runtime_timestamp(summary_rows: Sequence[Mapping[str, Any]]) -> pd.Timestamp | None:
    values = []
    for row in summary_rows:
        parsed = pd.to_datetime(row.get("last_ready_bar_time"), utc=True, errors="coerce")
        if not pd.isna(parsed):
            values.append(pd.Timestamp(parsed))
    return max(values) if values else None


def build_gate_rows(
    summary_rows: Sequence[Mapping[str, Any]],
    trades: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
    regime_rows: Sequence[Mapping[str, Any]],
    db_rows: Sequence[Mapping[str, Any]],
    lot_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    latest_feature = latest_feature_timestamp(attempts)
    latest_runtime = latest_runtime_timestamp(summary_rows)
    lag_minutes = (latest_feature - latest_runtime).total_seconds() / 60.0 if latest_feature is not None and latest_runtime is not None else None
    rows = [
        ("frozen_identity", "covered", rel(ATTEMPT_PACKAGE), "ONNX, feature order, decision mode, risk and lot parameters are fixed from the probe package."),
        ("mt5_report", "covered" if summary_rows else "blocked", rel(MT5_REPORT_SUMMARY), f"strategy_tester_report_rows={len(summary_rows)}"),
        ("trade_list_parse", "covered" if trades and not parser_errors else "blocked", rel(TRADE_RECORDS), f"trade_rows={len(trades)};parser_errors={len(parser_errors)}"),
        ("latest_visibility", "covered" if lag_minutes is not None and lag_minutes <= 10 else "blocked", rel(MT5_REPORT_SUMMARY), f"feature_last={latest_feature};runtime_last={latest_runtime};lag_minutes={lag_minutes}"),
        ("regime_attribution", "covered" if regime_rows else "blocked", rel(REGIME_ATTRIBUTION), "time/session/volatility/ADX/VIX/USD/rate slices generated where features exist."),
        ("db_attribution", "covered_boundary" if db_rows else "blocked", rel(DB_ATTRIBUTION), "D/B source unavailable; direction proxy boundary recorded."),
        ("lot_normalized", "covered" if lot_rows else "blocked", rel(LOT_NORMALIZED), "Fixed-lot and per-lot results generated without lot optimization."),
        ("cost_stress", "covered" if cost_rows else "blocked", rel(COST_STRESS), "Spread/slippage point stress generated after the fact."),
        ("curve_pocket", "covered" if curve_rows else "blocked", rel(CURVE_POCKET), "Worst month, chronology and rolling pockets generated."),
        ("no_goal_achieve", "covered", rel(FINAL_DECISION), "Goal Achieve is not claimed in this run."),
    ]
    payload = [{"gate_name": name, "status": status, "evidence_path": path, "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for name, status, path, effect in rows]
    write_csv(GATE_AUDIT, payload)
    return payload


def decide(summary_rows: Sequence[Mapping[str, Any]], curve_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rank1 = next((row for row in summary_rows if str(row.get("proxy_rank")) == "1"), {})
    curve_rank1 = next((row for row in curve_rows if str(row.get("proxy_rank")) == "1" and row.get("pocket_type") == "attempt_summary"), {})
    blocked_gates = [row for row in gate_rows if row.get("status") == "blocked"]
    if blocked_gates:
        decision = "Forward Blocked"
        judgment = "blocked_forward_data_or_tester_visibility_gap"
        forward_failed = "not_claimed"
    else:
        rank1_pf = number(rank1.get("profit_factor"), math.nan)
        rank1_net = number(rank1.get("net_profit"))
        rank1_dd = number(rank1.get("max_drawdown_amount"))
        rank1_curve = str(curve_rank1.get("curve_read", ""))
        if rank1_net > 0.0 and math.isfinite(rank1_pf) and rank1_pf >= 1.10 and rank1_dd <= max(250.0, abs(rank1_net) * 3.0) and rank1_curve == "constructive_forward_shape":
            decision = "Forward Passed"
            judgment = "rank1_forward_kpi_and_curve_shape_constructive_research_handoff_only"
            forward_failed = "not_claimed"
        else:
            decision = "Forward Failed"
            judgment = "rank1_lost_core_forward_kpi_or_curve_pocket_condition"
            forward_failed = "claimed_research_artifact_only"
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS_BLOCKED if blocked_gates else STATUS_COMPLETED,
        "judgment": judgment,
        "decision": decision,
        "next_action": NEXT_RUN_ID,
        "latest_feature_timestamp": str(latest_feature_timestamp(attempts)),
        "latest_runtime_timestamp": str(latest_runtime_timestamp(summary_rows)),
        "attempt_rows": len(summary_rows),
        "trade_rows": len(read_csv(TRADE_RECORDS)),
        "rank1_mt5_summary": rank1,
        "rank1_curve_summary": curve_rank1,
        "blocked_gates": blocked_gates,
        "forward_passed": "claimed_research_handoff_only" if decision == "Forward Passed" else "not_claimed",
        "forward_failed": forward_failed,
        "forward_blocked": "claimed" if decision == "Forward Blocked" else "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "deployment": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> int:
    args = parse_args()
    attempts = materialize_attempts(args)
    execution = run_mt5(args, attempts)
    summary_rows = build_mt5_summary(execution, attempts)
    trades, _checks, parser_errors = build_trade_records(execution, attempts)
    regime_rows = build_regime_rows(trades)
    db_rows = build_db_rows(trades)
    lot_rows = build_lot_rows(trades)
    cost_rows = build_cost_rows(trades)
    curve_rows = build_curve_rows(trades, regime_rows, cost_rows)
    signal_rows = build_signal_rows()
    gate_rows = build_gate_rows(summary_rows, trades, parser_errors, regime_rows, db_rows, lot_rows, cost_rows, curve_rows, attempts)
    final = decide(summary_rows, curve_rows, gate_rows, attempts)
    final["signal_attribution_rows"] = len(signal_rows)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "inputs": [rel(ep.FINAL_DECISION), rel(ep.FEATURE_SET_SUMMARY), rel(ep.SURFACE_REPROBE), rel(ep.ONNX_PARITY_CHECK)],
            "outputs": [
                rel(ATTEMPT_PACKAGE),
                rel(COMMON_SYNC),
                rel(EXPECTED_INDEX),
                rel(MT5_EXECUTION_RESULT),
                rel(MT5_REPORT_SUMMARY),
                rel(TRADE_RECORDS),
                rel(REGIME_ATTRIBUTION),
                rel(DB_ATTRIBUTION),
                rel(LOT_NORMALIZED),
                rel(COST_STRESS),
                rel(CURVE_POCKET),
                rel(SIGNAL_ATTRIBUTION),
                rel(GATE_AUDIT),
                rel(FINAL_DECISION),
                rel(RUN_MANIFEST),
            ],
            "from_date": args.from_date,
            "to_date": args.to_date,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "script_sha256": sha256_file(Path(__file__)),
        },
    )
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
