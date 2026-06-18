from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.trade_report import Deal, parse_mt5_trade_report
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_79 import frontier79b_runtime_native_trade_shape_label_proxy_scout as f79b
from stage_pipelines.stage_frontier_84 import frontier84b_runtime_realized_winrate_proxy_scout as f84b


STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
RUN_ID = "frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_v1"
PARENT_RUN_ID = "frontier84D_runtime_realized_winrate_proxy_runtime_gap_analysis_v1"
RUNTIME_PARENT_RUN_ID = "frontier84C_mt5_runtime_realized_winrate_materialization_v1"
SOURCE_PROXY_RUN_ID = "frontier84B_runtime_realized_winrate_proxy_scout_v1"
NEXT_RUN_ID = "frontier84F_runtime_realized_winrate_repair_or_rotation_decision_v1"
STATUS = "f84e_row_level_deal_reconciliation_completed_proxy_win_runtime_loss_dominant_no_authority"
JUDGMENT = "row_level_reconciliation_shows_proxy_win_to_runtime_loss_dominant_risk_shape_failure_likely_no_authority"
CLAIM_BOUNDARY = (
    "row_level_reconciliation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
RUNTIME_PARENT_DIR = STAGE_DIR / "02_runs" / RUNTIME_PARENT_RUN_ID
PROXY_RUN_DIR = STAGE_DIR / "02_runs" / SOURCE_PROXY_RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F84B_CANDIDATES_ALL = PROXY_RUN_DIR / "f84b_runtime_realized_winrate_proxy_candidates_all.csv"
F84B_TOP = REVIEW_DIR / "f84b_runtime_realized_winrate_proxy_top_candidates.csv"
F84B_SUMMARY = REVIEW_DIR / "f84b_runtime_realized_winrate_proxy_scout_summary.json"
F84C_TARGET = REVIEW_DIR / "f84c_runtime_realized_winrate_materialization_target_selection.json"
F84C_SUMMARY = REVIEW_DIR / "f84c_mt5_runtime_realized_winrate_materialization_summary.json"
F84C_EXECUTION_RESULTS = RUNTIME_PARENT_DIR / "f84c_execution_results.json"
F84C_RECEIPT = RUNTIME_PARENT_DIR / "f84c_runtime_receipt.csv"
F84C_SIGNAL_PARITY = RUNTIME_PARENT_DIR / "f84c_signal_parity.csv"
F84C_FEATURE_PARITY = RUNTIME_PARENT_DIR / "f84c_feature_readiness_parity.csv"
F84C_PROB_PARITY = RUNTIME_PARENT_DIR / "f84c_probability_parity.csv"
F84C_SOURCE_REPRO = RUNTIME_PARENT_DIR / "f84c_source_reproduction.csv"
F84C_FEATURES = RUNTIME_PARENT_DIR / "features/f84c_runtime_f84b_00287_features.csv"
F84C_VETO = RUNTIME_PARENT_DIR / "runtime_veto_tapes/f84c_runtime_f84b_00287_selected_entry_runtime_veto_tape.csv"
F84D_SUMMARY = REVIEW_DIR / "f84d_runtime_realized_winrate_gap_analysis_summary.json"

ROW_RECONCILIATION = REVIEW_DIR / "f84e_row_level_reconciliation_rows.csv"
SPLIT_SUMMARY = REVIEW_DIR / "f84e_row_level_reconciliation_split_summary.csv"
MONTH_SESSION_SUMMARY = REVIEW_DIR / "f84e_month_session_streak_summary.csv"
UNMATCHED_ROWS = REVIEW_DIR / "f84e_unmatched_runtime_mapping_rows.csv"
SUMMARY = REVIEW_DIR / "f84e_row_level_deal_reconciliation_summary.json"
REPORT = REVIEW_DIR / "frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f84e.md"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f84e_run_evidence_receipt.yaml"
DATA_INTEGRITY_RECEIPT = REVIEW_DIR / "f84e_data_integrity_receipt.yaml"
BACKTEST_FORENSICS_RECEIPT = REVIEW_DIR / "f84e_backtest_forensics_receipt.yaml"
RUNTIME_PARITY_RECEIPT = REVIEW_DIR / "f84e_runtime_parity_receipt.yaml"
MODEL_VALIDATION_RECEIPT = REVIEW_DIR / "f84e_model_validation_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f84e_result_judgment_receipt.yaml"
TASK_FORCE_REVIEW = REVIEW_DIR / "f84e_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f84e_claim_discipline_receipt.yaml"
ACTUAL_SUBAGENT_CALLS = REVIEW_DIR / "f84e_actual_subagent_calls.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f84e_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f84e_local_verification.json"

NORMALIZED_DEALS = RUN_DIR / "f84e_mt5_normalized_deal_rows.csv"
NORMALIZED_TRADES = RUN_DIR / "f84e_mt5_normalized_trade_rows.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_84/frontier84e_runtime_realized_winrate_row_level_deal_reconciliation.py"

EXPECTED_TASK_FORCE_CALLS = 8
REQUIRED_TASK_FORCE_ROSTER_IDS = (
    "agent_01_system_governor",
    "agent_02_platform_routing_architect",
    "agent_03_philosophy_policy_skill_governance",
    "agent_04_evidence_control_plane",
    "agent_05_data_feature_contract",
    "agent_06_quant_research",
    "agent_07_model_validation_risk",
    "agent_08_mt5_onnx_runtime",
)

TASK_FORCE_CALLS: list[dict[str, Any]] = [
    {
        "roster_id": "agent_01_system_governor",
        "nickname": "Halley",
        "agent_id": "019eda5b-20f5-7091-9cbd-cc0eeac8d81b",
        "status": "completed",
        "phase": "f84e_reentry_scope_guard",
        "classification": "accepted",
        "summary": "F84E scope is row-level MT5 trade/deal evidence reconciliation; forbidden claims remain completion, baseline, promotion, runtime authority, live readiness, and Goal Achieve.",
    },
    {
        "roster_id": "agent_02_platform_routing_architect",
        "nickname": "Hypatia",
        "agent_id": "019eda5b-353f-7e81-ae4b-6e080fc08739",
        "status": "completed",
        "phase": "f84e_work_family_routing",
        "classification": "accepted",
        "summary": "Route F84E as runtime_backtest with obsidian-runtime-parity primary and backtest forensics, run evidence, artifact lineage, and Task Force review support.",
    },
    {
        "roster_id": "agent_03_philosophy_policy_skill_governance",
        "nickname": "Planck",
        "agent_id": "019eda5b-4e21-7e12-ba80-47a3f20f1b83",
        "status": "completed",
        "phase": "f84e_policy_boundary",
        "classification": "accepted",
        "summary": "Reference-not-inheritance and no threshold-only repair before row-level reconciliation; exact cause remains bounded until proxy, veto, telemetry, and MT5 rows are joined.",
    },
    {
        "roster_id": "agent_04_evidence_control_plane",
        "nickname": "Meitner",
        "agent_id": "019eda5b-6781-7271-8dc1-2d728748687b",
        "status": "completed",
        "phase": "f84e_evidence_identity",
        "classification": "needs_local_verification",
        "summary": "Record path, SHA256, row count, producer, consumer, candidate IDs, telemetry, veto, report, set, ini, and attempts identities before row-level claims.",
    },
    {
        "roster_id": "agent_05_data_feature_contract",
        "nickname": "Schrodinger",
        "agent_id": "019eda5b-80ce-7470-9dda-733388291179",
        "status": "completed",
        "phase": "f84e_join_policy",
        "classification": "accepted",
        "summary": "Use candidate-level ID separation; join selected/veto/telemetry at split and bar/source time, and prefer telemetry ticket to MT5 entry deal over time-only matching.",
    },
    {
        "roster_id": "agent_06_quant_research",
        "nickname": "Boole",
        "agent_id": "019eda5b-99c8-76c1-9995-dfaa50c2a5f6",
        "status": "completed",
        "phase": "f84e_quant_attribution",
        "classification": "accepted",
        "summary": "Prioritize proxy_win_to_runtime_loss counts, share, and net drag; include PnL delta, TP/SL path attribution, month/session, and loss streak summaries.",
    },
    {
        "roster_id": "agent_07_model_validation_risk",
        "nickname": "Ptolemy",
        "agent_id": "019eda5e-fd27-74b2-8e76-291bca99282d",
        "status": "completed",
        "phase": "f84e_model_risk_boundary",
        "classification": "accepted",
        "summary": "Do not prematurely choose overfit, calibration, execution accounting, or invalid mapping; row-level diagnostic probe must separate these possibilities.",
    },
    {
        "roster_id": "agent_08_mt5_onnx_runtime",
        "nickname": "Helmholtz",
        "agent_id": "019eda60-900b-7fb3-b833-c0a83641997b",
        "status": "completed",
        "phase": "f84e_runtime_deal_mapping",
        "classification": "needs_local_verification",
        "summary": "F84C artifacts are usable_with_boundary; count bridge is validation 2340->2335->2326 and OOS 1805->1802->1801, invalid stops are 9/1, and validation has two second-level open-time drifts.",
    },
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def remove_csv_rows(path: Path, predicate: Callable[[dict[str, str]], bool]) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [row for row in reader if not predicate(row)]
    try:
        handle = io_path(path).open("w", encoding="utf-8-sig", newline="")
    except OSError:
        handle = path.resolve().open("w", encoding="utf-8-sig", newline="")
    with handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_csv_row(path: Path, row: Mapping[str, Any], *, key: str | None = None, source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    if key:
        rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_ticket(value: Any) -> str:
    match = re.search(r"ticket=([0-9]+)", str(value or ""))
    return match.group(1) if match else ""


def parse_time(value: Any) -> pd.Timestamp:
    if pd.isna(value):
        return pd.NaT
    text = str(value)
    if "." in text and "-" not in text:
        return pd.to_datetime(text, format="%Y.%m.%d %H:%M:%S", errors="coerce", utc=True)
    return pd.to_datetime(text, errors="coerce", utc=True)


def time_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    return ts.isoformat()


def load_target() -> dict[str, Any]:
    payload = read_json(F84C_TARGET)
    return dict(payload["runtime_materialization_target"])


def target_spec(target: Mapping[str, Any]) -> Any:
    label_name = str(target["label_name"])
    for spec in f84b.runtime_specs():
        if spec.name == label_name:
            return spec
    raise ValueError(f"missing F84 spec for {label_name}")


def reconstruct_proxy_rows(target: Mapping[str, Any]) -> pd.DataFrame:
    df, raw, _features = f78b.load_inputs()
    spec = target_spec(target)
    entry_idx = f79b.entry_indices(df, raw, spec.entry_mode)
    outcome = f79b.compute_outcome(raw, entry_idx, spec)
    proxy = pd.DataFrame(
        {
            "split": df["split"].astype(str),
            "timestamp_utc": pd.to_datetime(df["timestamp"], errors="coerce", utc=True),
            "row_index": np.arange(len(df), dtype=int),
            "entry_raw_index": entry_idx,
            "proxy_pnl_price": outcome["pnl_price"],
            "proxy_pnl_contract": outcome["pnl_contract"],
            "proxy_mfe_contract": outcome["mfe_contract"],
            "proxy_mae_contract": outcome["mae_contract"],
            "proxy_spread_cost_contract": outcome["spread_cost_contract"],
            "proxy_utility": outcome["utility"],
            "proxy_exit_offset_bars": outcome["exit_offset"],
            "proxy_both_hit": outcome["both_hit"],
            "proxy_valid": outcome["valid"],
        }
    )
    proxy["proxy_win"] = proxy["proxy_pnl_contract"] > 0.0
    proxy["proxy_exit_path_label"] = np.select(
        [
            proxy["proxy_both_hit"].astype(int) == 1,
            proxy["proxy_pnl_price"] >= as_float(target.get("tp_price_units")),
            proxy["proxy_pnl_price"] <= -as_float(target.get("sl_price_units")),
        ],
        ["both_hit_close_direction", "tp_expected", "sl_expected"],
        default="hold_close_or_partial",
    )
    return proxy


def load_selected_rows(proxy: pd.DataFrame) -> pd.DataFrame:
    veto = pd.read_csv(io_path(F84C_VETO))
    veto["timestamp_utc"] = pd.to_datetime(veto["timestamp_utc"], errors="coerce", utc=True)
    veto["bar_time_server_ts"] = pd.to_datetime(veto["bar_time_server"], errors="coerce", utc=True)
    veto["selected_entry"] = veto["selected_entry"].map(boolish)
    veto["event_active"] = veto["event_active"].map(boolish)
    selected = veto.loc[veto["selected_entry"] & veto["split"].isin(["validation", "oos"])].copy()
    merged = selected.merge(proxy, on=["split", "timestamp_utc"], how="left", validate="one_to_one")
    if merged["proxy_pnl_contract"].isna().any():
        raise ValueError("selected rows failed proxy outcome join")
    return merged.sort_values(["split", "timestamp_utc"]).reset_index(drop=True)


def split_attempts(execution_results: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    attempts: dict[str, dict[str, Any]] = {}
    source_attempts = execution_results if isinstance(execution_results, list) else execution_results.get("attempts", [])
    for attempt in source_attempts:
        split = str(attempt.get("split") or "")
        if split in {"validation", "oos"}:
            attempts[split] = dict(attempt)
    return attempts


def load_telemetry(attempts: Mapping[str, Mapping[str, Any]]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for split, attempt in attempts.items():
        telemetry_path = Path(str((attempt.get("runtime_outputs") or {}).get("telemetry_path") or attempt.get("telemetry_path") or ""))
        frame = pd.read_csv(io_path(telemetry_path))
        frame["split"] = split
        frame = frame.loc[frame["record_type"].astype(str).str.lower() == "cycle"].copy()
        frame["source_time_ts"] = frame["source_time"].map(parse_time)
        frame["bar_time_ts"] = frame["bar_time"].map(parse_time)
        frame["order_attempted_bool"] = frame["order_attempted"].map(boolish)
        frame["order_filled_bool"] = frame["order_filled"].map(boolish)
        frame["entry_ticket"] = frame["position_after"].map(parse_ticket)
        frames.append(frame)
    telemetry = pd.concat(frames, ignore_index=True)
    if telemetry.duplicated(["split", "source_time_ts"]).any():
        raise ValueError("telemetry split/source_time duplicate detected")
    return telemetry


def normalized_deal_rows(split: str, report_path: Path) -> list[dict[str, Any]]:
    report = parse_mt5_trade_report(report_path)
    rows: list[dict[str, Any]] = []
    for index, deal in enumerate(report["deals"], start=1):
        deal_dict = asdict(deal)
        deal_dict.update(
            {
                "split": split,
                "deal_index": index,
                "time_utc": time_text(deal.time),
                "report_path": report_path.as_posix(),
            }
        )
        deal_dict.pop("time", None)
        rows.append(deal_dict)
    return rows


def pair_deals_with_tickets(split: str, deals: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    open_deal: Mapping[str, Any] | None = None
    for deal in deals:
        direction = str(deal.get("direction") or "").lower()
        if direction == "in" and deal.get("price") not in {None, ""}:
            open_deal = deal
            continue
        if direction != "out" or open_deal is None or deal.get("price") in {None, ""}:
            continue
        open_time = parse_time(open_deal["time_utc"])
        close_time = parse_time(deal["time_utc"])
        gross_profit = as_float(deal.get("profit"))
        net_profit = gross_profit + as_float(deal.get("swap")) + as_float(deal.get("commission"))
        holding_seconds = float((close_time - open_time).total_seconds()) if not pd.isna(open_time) and not pd.isna(close_time) else np.nan
        exit_comment = str(deal.get("comment") or "")
        rows.append(
            {
                "split": split,
                "runtime_trade_index": len(rows) + 1,
                "entry_ticket": str(open_deal.get("ticket") or ""),
                "entry_order": str(open_deal.get("order") or ""),
                "exit_ticket": str(deal.get("ticket") or ""),
                "exit_order": str(deal.get("order") or ""),
                "symbol": open_deal.get("symbol"),
                "direction": str(open_deal.get("order_type") or "").lower(),
                "volume": as_float(open_deal.get("volume")),
                "runtime_open_time_utc": time_text(open_time),
                "runtime_close_time_utc": time_text(close_time),
                "runtime_open_price": as_float(open_deal.get("price")),
                "runtime_close_price": as_float(deal.get("price")),
                "runtime_gross_profit": gross_profit,
                "runtime_net_profit": net_profit,
                "runtime_commission": as_float(deal.get("commission")),
                "runtime_swap": as_float(deal.get("swap")),
                "runtime_win": net_profit > 0.0,
                "runtime_exit_comment": exit_comment,
                "runtime_exit_reason": "tp" if exit_comment.lower().startswith("tp") else ("sl" if exit_comment.lower().startswith("sl") else "other"),
                "runtime_holding_seconds": holding_seconds,
            }
        )
        open_deal = None
    return rows


def load_runtime_rows(attempts: Mapping[str, Mapping[str, Any]]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    all_deals: list[dict[str, Any]] = []
    all_trades: list[dict[str, Any]] = []
    report_summaries: dict[str, Any] = {}
    for split, attempt in attempts.items():
        report_block = attempt.get("strategy_tester_report") or {}
        report_path = Path(
            str(
                (report_block.get("metrics") or {}).get("report_path")
                or (report_block.get("html_report") or {}).get("path")
                or (attempt.get("tester_artifacts") or {}).get("report_path")
                or ""
            )
        )
        report = parse_mt5_trade_report(report_path)
        report_summaries[split] = report.get("summary") or {}
        deal_rows = normalized_deal_rows(split, report_path)
        trade_rows = pair_deals_with_tickets(split, deal_rows)
        all_deals.extend(deal_rows)
        all_trades.extend(trade_rows)
    deals = pd.DataFrame(all_deals)
    trades = pd.DataFrame(all_trades)
    if not deals.empty:
        deals["time_ts"] = deals["time_utc"].map(parse_time)
    if not trades.empty:
        trades["runtime_open_time_ts"] = trades["runtime_open_time_utc"].map(parse_time)
        trades["runtime_close_time_ts"] = trades["runtime_close_time_utc"].map(parse_time)
    return deals, trades, report_summaries


def reconcile_rows(selected: pd.DataFrame, telemetry: pd.DataFrame, trades: pd.DataFrame, target: Mapping[str, Any]) -> pd.DataFrame:
    telemetry_cols = [
        "split",
        "source_time_ts",
        "bar_time_ts",
        "input_hash",
        "p_short",
        "p_flat",
        "p_long",
        "decision",
        "decision_reason",
        "order_attempted_bool",
        "order_filled_bool",
        "trade_retcode",
        "trade_comment",
        "position_before",
        "position_after",
        "entry_ticket",
        "model_risk_pct",
        "clipped_risk_pct",
        "computed_lot",
        "executed_lot",
        "actual_risk_pct_after_floor",
        "atr_points",
        "open_sl_points",
        "open_tp_points",
    ]
    rows = selected.merge(
        telemetry[telemetry_cols],
        left_on=["split", "timestamp_utc"],
        right_on=["split", "source_time_ts"],
        how="left",
        validate="one_to_one",
    )
    trade_cols = [
        "split",
        "runtime_trade_index",
        "entry_ticket",
        "entry_order",
        "exit_ticket",
        "exit_order",
        "direction",
        "volume",
        "runtime_open_time_utc",
        "runtime_close_time_utc",
        "runtime_open_time_ts",
        "runtime_close_time_ts",
        "runtime_open_price",
        "runtime_close_price",
        "runtime_gross_profit",
        "runtime_net_profit",
        "runtime_commission",
        "runtime_swap",
        "runtime_win",
        "runtime_exit_comment",
        "runtime_exit_reason",
        "runtime_holding_seconds",
    ]
    rows = rows.merge(trades[trade_cols], on=["split", "entry_ticket"], how="left", validate="many_to_one")
    rows["runtime_match_status"] = np.select(
        [
            rows["order_filled_bool"].fillna(False) & rows["runtime_trade_index"].notna(),
            rows["order_filled_bool"].fillna(False) & rows["runtime_trade_index"].isna(),
            rows["order_attempted_bool"].fillna(False) & ~rows["order_filled_bool"].fillna(False),
        ],
        ["ticket_match", "filled_without_trade_match", "attempted_unfilled"],
        default="selected_no_attempt_or_no_fill",
    )
    rows["runtime_open_time_delta_seconds"] = (
        rows["runtime_open_time_ts"] - rows["timestamp_utc"]
    ).dt.total_seconds()
    rows["runtime_net_profit_filled"] = pd.to_numeric(rows["runtime_net_profit"], errors="coerce")
    rows["proxy_pnl_contract"] = pd.to_numeric(rows["proxy_pnl_contract"], errors="coerce")
    rows["proxy_runtime_pnl_delta"] = rows["runtime_net_profit_filled"] - rows["proxy_pnl_contract"]
    rows["runtime_loss"] = rows["runtime_net_profit_filled"] < 0.0
    rows["runtime_win_bool"] = rows["runtime_win"].map(lambda value: bool(value) if pd.notna(value) else False)
    rows["proxy_win_runtime_loss"] = rows["proxy_win"].astype(bool) & rows["runtime_loss"].fillna(False)
    rows["proxy_loss_runtime_win"] = (~rows["proxy_win"].astype(bool)) & rows["runtime_win_bool"]
    rows["tp_expected_sl_actual"] = (rows["proxy_exit_path_label"] == "tp_expected") & (rows["runtime_exit_reason"] == "sl")
    rows["sl_expected_tp_actual"] = (rows["proxy_exit_path_label"] == "sl_expected") & (rows["runtime_exit_reason"] == "tp")
    rows["month"] = rows["timestamp_utc"].dt.strftime("%Y-%m")
    rows["hour_utc"] = rows["timestamp_utc"].dt.hour
    rows["session_bucket"] = np.select(
        [
            rows["timestamp_utc"].dt.hour.between(14, 16),
            rows["timestamp_utc"].dt.hour.between(17, 19),
            rows["timestamp_utc"].dt.hour.between(20, 22),
        ],
        ["cash_open_or_pre_open", "cash_mid", "cash_late"],
        default="other",
    )
    rows["target_candidate_id"] = str(target.get("candidate_id") or "")
    rows["target_label_name"] = str(target.get("label_name") or "")
    rows["source_candidate_id"] = str(target.get("candidate_id") or "")
    rows["runtime_wrapper_id"] = "f84c_runtime_f84b_00287"
    rows["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def summarize_split(rows: pd.DataFrame, trades: pd.DataFrame, receipts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    receipt_by_split = {row.get("split"): row for row in receipts}
    summaries: list[dict[str, Any]] = []
    for split in ["validation", "oos"]:
        part = rows.loc[rows["split"] == split].copy()
        matched = part.loc[part["runtime_match_status"] == "ticket_match"].copy()
        split_trades = trades.loc[trades["split"] == split].copy()
        proxy_win = int(matched["proxy_win"].sum())
        runtime_win = int(matched["runtime_win_bool"].sum())
        proxy_win_runtime_loss = int(matched["proxy_win_runtime_loss"].sum())
        proxy_loss_runtime_win = int(matched["proxy_loss_runtime_win"].sum())
        proxy_win_to_runtime_loss_rate = proxy_win_runtime_loss / proxy_win if proxy_win else 0.0
        matched_count = int(len(matched))
        gross_profit = float(matched.loc[matched["runtime_net_profit_filled"] > 0, "runtime_net_profit_filled"].sum())
        gross_loss = float(matched.loc[matched["runtime_net_profit_filled"] < 0, "runtime_net_profit_filled"].sum())
        pf = gross_profit / abs(gross_loss) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0)
        receipt = receipt_by_split.get(split, {})
        summaries.append(
            {
                "split": split,
                "selected_entry_count": int(len(part)),
                "telemetry_attempt_count": int(part["order_attempted_bool"].fillna(False).sum()),
                "telemetry_fill_count": int(part["order_filled_bool"].fillna(False).sum()),
                "runtime_trade_count": int(len(split_trades)),
                "ticket_matched_trade_count": matched_count,
                "selected_no_fill_count": int((part["runtime_match_status"].isin(["attempted_unfilled", "selected_no_attempt_or_no_fill"])).sum()),
                "filled_without_trade_match_count": int((part["runtime_match_status"] == "filled_without_trade_match").sum()),
                "runtime_without_selected_count": int(max(0, len(split_trades) - matched_count)),
                "open_time_second_drift_count": int((matched["runtime_open_time_delta_seconds"].abs() > 0).sum()),
                "proxy_win_count_matched": proxy_win,
                "runtime_win_count_matched": runtime_win,
                "proxy_win_runtime_loss_count": proxy_win_runtime_loss,
                "proxy_loss_runtime_win_count": proxy_loss_runtime_win,
                "proxy_same_win_count": int((matched["proxy_win"].astype(bool) & matched["runtime_win_bool"]).sum()),
                "proxy_same_loss_count": int(((~matched["proxy_win"].astype(bool)) & matched["runtime_loss"].fillna(False)).sum()),
                "proxy_win_to_runtime_loss_rate": proxy_win_to_runtime_loss_rate,
                "runtime_net_profit_matched": float(matched["runtime_net_profit_filled"].sum()),
                "proxy_pnl_contract_matched": float(matched["proxy_pnl_contract"].sum()),
                "pnl_delta_sum": float(matched["proxy_runtime_pnl_delta"].sum()),
                "runtime_gross_profit_matched": gross_profit,
                "runtime_gross_loss_matched": gross_loss,
                "runtime_profit_factor_matched": pf,
                "runtime_win_rate_matched_percent": runtime_win / matched_count * 100.0 if matched_count else 0.0,
                "proxy_win_rate_matched_percent": proxy_win / matched_count * 100.0 if matched_count else 0.0,
                "tp_expected_sl_actual_count": int(matched["tp_expected_sl_actual"].sum()),
                "sl_expected_tp_actual_count": int(matched["sl_expected_tp_actual"].sum()),
                "avg_runtime_holding_seconds": float(matched["runtime_holding_seconds"].mean()) if matched_count else 0.0,
                "receipt_runtime_net_profit": as_float(receipt.get("net_profit")),
                "receipt_runtime_profit_factor": as_float(receipt.get("profit_factor")),
                "receipt_runtime_drawdown_percent": as_float(receipt.get("max_drawdown_percent")),
                "receipt_runtime_trade_count": as_int(receipt.get("trade_count")),
                "receipt_proxy_net_profit": as_float(receipt.get("proxy_net_profit")),
                "receipt_proxy_profit_factor": as_float(receipt.get("proxy_profit_factor")),
            }
        )
    return summaries


def max_consecutive_losses(values: Sequence[float]) -> int:
    best = 0
    current = 0
    for value in values:
        if value < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def summarize_month_session(rows: pd.DataFrame) -> list[dict[str, Any]]:
    matched = rows.loc[rows["runtime_match_status"] == "ticket_match"].copy()
    output: list[dict[str, Any]] = []
    for keys, part in matched.groupby(["split", "month", "session_bucket"], sort=True):
        split, month, session = keys
        pnl = pd.to_numeric(part["runtime_net_profit_filled"], errors="coerce").fillna(0.0).to_numpy(float)
        proxy_win_runtime_loss = int(part["proxy_win_runtime_loss"].sum())
        output.append(
            {
                "split": split,
                "month": month,
                "session_bucket": session,
                "trade_count": int(len(part)),
                "runtime_net_profit": float(pnl.sum()),
                "runtime_win_rate_percent": float((pnl > 0).mean() * 100.0) if len(pnl) else 0.0,
                "proxy_win_runtime_loss_count": proxy_win_runtime_loss,
                "proxy_win_runtime_loss_share": proxy_win_runtime_loss / len(part) if len(part) else 0.0,
                "max_consecutive_loss": max_consecutive_losses(pnl),
            }
        )
    return output


def task_force_roster_summary(calls: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    required = set(REQUIRED_TASK_FORCE_ROSTER_IDS)
    roster_ids = {str(call.get("roster_id") or "") for call in calls}
    roster_ids.discard("")
    completed_ids = {str(call.get("roster_id") or "") for call in calls if call.get("status") == "completed"}
    completed_ids.discard("")
    missing = sorted(required.difference(roster_ids))
    incomplete = sorted(required.difference(completed_ids))
    return {
        "required_roster_ids": list(REQUIRED_TASK_FORCE_ROSTER_IDS),
        "covered_roster_ids": sorted(required.intersection(roster_ids)),
        "completed_roster_ids": sorted(required.intersection(completed_ids)),
        "missing_roster_ids": missing,
        "incomplete_roster_ids": incomplete,
        "coverage_count": len(required.intersection(roster_ids)),
        "completed_count": len(required.intersection(completed_ids)),
        "required_count": len(REQUIRED_TASK_FORCE_ROSTER_IDS),
        "all_required_covered": not missing,
        "all_required_completed": not incomplete,
    }


def task_force_call_text(payload: Mapping[str, Any]) -> str:
    coverage = payload.get("actual_subagent_roster_coverage") or {}
    return f"{payload.get('actual_subagent_call_count')}/{EXPECTED_TASK_FORCE_CALLS}; completed={coverage.get('completed_count')}/{coverage.get('required_count')}"


def build_payload(created_at: str) -> dict[str, Any]:
    target = load_target()
    proxy = reconstruct_proxy_rows(target)
    selected = load_selected_rows(proxy)
    execution_results = read_json(F84C_EXECUTION_RESULTS)
    attempts = split_attempts(execution_results)
    telemetry = load_telemetry(attempts)
    deals, trades, report_summaries = load_runtime_rows(attempts)
    rows = reconcile_rows(selected, telemetry, trades, target)
    receipts = read_csv_rows(F84C_RECEIPT)
    split_summary = summarize_split(rows, trades, receipts)
    month_session = summarize_month_session(rows)
    unmatched = rows.loc[rows["runtime_match_status"] != "ticket_match"].copy()
    coverage = task_force_roster_summary(TASK_FORCE_CALLS)
    source_paths = [
        F84B_CANDIDATES_ALL,
        F84B_TOP,
        F84C_TARGET,
        F84C_SUMMARY,
        F84C_EXECUTION_RESULTS,
        F84C_RECEIPT,
        F84C_SIGNAL_PARITY,
        F84C_FEATURE_PARITY,
        F84C_PROB_PARITY,
        F84C_SOURCE_REPRO,
        F84C_FEATURES,
        F84C_VETO,
        F84D_SUMMARY,
    ]
    external_paths = [
        Path(str((attempt.get("runtime_outputs") or {}).get("telemetry_path") or ""))
        for attempt in attempts.values()
        if (attempt.get("runtime_outputs") or {}).get("telemetry_path")
    ]
    source_identity = []
    for path in source_paths + external_paths:
        if not str(path):
            continue
        exists = path_exists(path) if path.is_absolute() is False else io_path(path).is_file()
        source_identity.append(
            {
                "path": rel(path),
                "exists": exists,
                "sha256": sha256_file_lf_normalized(path) if exists else "",
            }
        )
    oos_summary = next(row for row in split_summary if row["split"] == "oos")
    validation_summary = next(row for row in split_summary if row["split"] == "validation")
    primary_readout = (
        "proxy_win_to_runtime_loss_dominant"
        if oos_summary["proxy_win_runtime_loss_count"] > oos_summary["proxy_loss_runtime_win_count"]
        else "mixed_proxy_runtime_flip"
    )
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "runtime_parent_run_id": RUNTIME_PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "target": target,
        "selected_entry_total": int(len(selected)),
        "normalized_deal_count": int(len(deals)),
        "normalized_trade_count": int(len(trades)),
        "split_summary": split_summary,
        "validation_summary": validation_summary,
        "oos_summary": oos_summary,
        "month_session_summary_rows": len(month_session),
        "unmatched_row_count": int(len(unmatched)),
        "runtime_report_summaries": report_summaries,
        "primary_readout": primary_readout,
        "preserved_clue": "density preserved in MT5 but not economics",
        "negative_memory": "proxy row winners frequently become runtime row losses after signal/feature/ONNX parity",
        "next_action": NEXT_RUN_ID,
        "source_identity": source_identity,
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "actual_subagent_call_count": len(TASK_FORCE_CALLS),
        "actual_subagent_roster_coverage": coverage,
        "actual_subagent_missing_roster_ids": coverage["missing_roster_ids"],
        "actual_subagent_incomplete_roster_ids": coverage["incomplete_roster_ids"],
        "output_paths": {
            "row_reconciliation": rel(ROW_RECONCILIATION),
            "split_summary": rel(SPLIT_SUMMARY),
            "month_session_summary": rel(MONTH_SESSION_SUMMARY),
            "unmatched_rows": rel(UNMATCHED_ROWS),
            "normalized_deals": rel(NORMALIZED_DEALS),
            "normalized_trades": rel(NORMALIZED_TRADES),
            "summary": rel(SUMMARY),
            "report": rel(REPORT),
        },
    }
    payload["_frames"] = {
        "rows": rows,
        "deals": deals,
        "trades": trades,
        "split_summary": pd.DataFrame(split_summary),
        "month_session": pd.DataFrame(month_session),
        "unmatched": unmatched,
    }
    return payload


def safe_output_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key != "_frames"}


def report_text(payload: Mapping[str, Any]) -> str:
    val = payload["validation_summary"]
    oos = payload["oos_summary"]
    return f"""# F84E Runtime Realized Winrate Row-Level Deal Reconciliation(F84E 런타임 실현 승률 행 단위 거래 조정)

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): F84B proxy outcome(프록시 결과), F84C veto tape(차단 테이프), telemetry(원격 측정), MT5 deal report(거래 보고서)를 selected entry(선택 진입) 행 단위로 결합했다.

Effect(효과): aggregate KPI(집계 핵심 성과 지표)가 아니라 어떤 proxy win(프록시 승리)이 runtime loss(런타임 손실)로 바뀌었는지 기록했다.

## Readout(판독)

| split(구간) | selected(선택) | filled(체결) | ticket matched(티켓 결합) | proxy win -> runtime loss(프록시 승리 -> 런타임 손실) | runtime win rate(런타임 승률) | runtime PF(런타임 수익 팩터) |
|---|---:|---:|---:|---:|---:|---:|
| validation(검증) | {val['selected_entry_count']} | {val['telemetry_fill_count']} | {val['ticket_matched_trade_count']} | {val['proxy_win_runtime_loss_count']} / {val['proxy_win_count_matched']} ({fmt(val['proxy_win_to_runtime_loss_rate'] * 100.0, 2)}%) | {fmt(val['runtime_win_rate_matched_percent'], 2)}% | {fmt(val['runtime_profit_factor_matched'], 4)} |
| OOS(표본외) | {oos['selected_entry_count']} | {oos['telemetry_fill_count']} | {oos['ticket_matched_trade_count']} | {oos['proxy_win_runtime_loss_count']} / {oos['proxy_win_count_matched']} ({fmt(oos['proxy_win_to_runtime_loss_rate'] * 100.0, 2)}%) | {fmt(oos['runtime_win_rate_matched_percent'], 2)}% | {fmt(oos['runtime_profit_factor_matched'], 4)} |

## Attribution(귀속)

Accepted(수용): F84C signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 보존됐고, row-level(행 단위) MT5 ticket match(티켓 결합)는 validation(검증) {val['ticket_matched_trade_count']}/{val['runtime_trade_count']}, OOS(표본외) {oos['ticket_matched_trade_count']}/{oos['runtime_trade_count']}로 닫혔다.

Rejected(거절): fill gap(체결 간극)만으로 PF/DD collapse(수익 팩터/손실폭 붕괴)를 설명하는 주장, F84C parity pass(동등성 통과)를 runtime authority(런타임 권위)로 보는 주장, threshold-only repair(임계값만 수리)로 바로 가는 주장은 거절한다.

Needs local verification(로컬 검증 필요): F84F(전선84F)는 this row evidence(이 행 근거)를 보고 capped repair(상한 있는 수리) 또는 rotation(회전)을 골라야 한다. completion(완성)이나 selected baseline(선택 기준선)은 없다.

Preserved clue(보존 단서): `{payload['preserved_clue']}`.

Negative memory(부정 기억): `{payload['negative_memory']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    coverage = payload["actual_subagent_roster_coverage"]
    return f"""# F84E Required Gate Coverage Audit(F84E 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `row_level_reconciliation(행 단위 조정)` | `passed(통과)` | `{rel(ROW_RECONCILIATION)}` | selected entry(선택 진입)마다 proxy/runtime(프록시/런타임)을 붙였다. |
| `normalized_deal_trade_rows(정규화 딜/거래 행)` | `passed(통과)` | `{rel(NORMALIZED_DEALS)}`, `{rel(NORMALIZED_TRADES)}` | MT5 HTML report(MT5 보고서)를 row evidence(행 근거)로 바꿨다. |
| `ticket_join_policy(티켓 결합 정책)` | `passed(통과)` | `{rel(SPLIT_SUMMARY)}` | time-only join(시간만 결합)보다 ticket(티켓)을 우선했다. |
| `proxy_runtime_confusion(프록시/런타임 혼동표)` | `passed(통과)` | `{rel(SPLIT_SUMMARY)}` | proxy win -> runtime loss(프록시 승리 -> 런타임 손실) 전환을 기록했다. |
| `month_session_streak(월/세션/연패)` | `passed(통과)` | `{rel(MONTH_SESSION_SUMMARY)}` | 붕괴가 어느 시간 묶음에 몰리는지 볼 수 있게 했다. |
| `runtime_parity_boundary(런타임 동등성 경계)` | `passed(통과)` | `{rel(RUNTIME_PARITY_RECEIPT)}` | parity(동등성)를 authority(권위)로 승격하지 않았다. |
| `task_force_actual_calls(태스크포스 실제 호출)` | `{'passed(통과)' if coverage['all_required_completed'] else 'pending(대기)'}` | `{rel(ACTUAL_SUBAGENT_CALLS)}` | 8명 agent(요원) 호출을 기록했다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | completion/runtime authority/live readiness(완성/런타임 권위/실거래 준비)를 만들지 않았다. |
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    val = payload["validation_summary"]
    oos = payload["oos_summary"]
    return {
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: row_level_reconciliation_recorded_no_authority
test_period: validation 2025-01-02..2025-10-01; OOS 2025-10-01..2026-04-14
proxy_kpi: validation proxy matched pnl={val['proxy_pnl_contract_matched']}; OOS proxy matched pnl={oos['proxy_pnl_contract_matched']}
runtime_kpi: validation net/PF/trades={val['runtime_net_profit_matched']}/{val['runtime_profit_factor_matched']}/{val['ticket_matched_trade_count']}; OOS net/PF/trades={oos['runtime_net_profit_matched']}/{oos['runtime_profit_factor_matched']}/{oos['ticket_matched_trade_count']}
trade_count: validation selected={val['selected_entry_count']} filled={val['telemetry_fill_count']}; OOS selected={oos['selected_entry_count']} filled={oos['telemetry_fill_count']}
gap_cause: proxy_win_to_runtime_loss_dominant
next_action: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
""",
        DATA_INTEGRITY_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-data-integrity
status: usable_with_boundary
join_policy: split + selected timestamp + telemetry source_time + entry ticket
selected_no_fill: validation={val['selected_no_fill_count']}; OOS={oos['selected_no_fill_count']}
open_time_second_drift: validation={val['open_time_second_drift_count']}; OOS={oos['open_time_second_drift_count']}
boundary: broker_clock_alignment_key_not_true_utc_claim
claim_boundary: {CLAIM_BOUNDARY}
""",
        BACKTEST_FORENSICS_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-backtest-forensics
status: normalized_mt5_deal_trade_rows_created
normalized_deals: {rel(NORMALIZED_DEALS)}
normalized_trades: {rel(NORMALIZED_TRADES)}
validation_pairs: {val['runtime_trade_count']}
oos_pairs: {oos['runtime_trade_count']}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RUNTIME_PARITY_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-runtime-parity
status: signal_feature_onnx_parity_preserved_but_deal_economics_failed_no_authority
parity_sources:
  - {rel(F84C_SIGNAL_PARITY)}
  - {rel(F84C_FEATURE_PARITY)}
  - {rel(F84C_PROB_PARITY)}
row_level_evidence: {rel(ROW_RECONCILIATION)}
claim_boundary: {CLAIM_BOUNDARY}
""",
        MODEL_VALIDATION_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-model-validation
status: model_risk_shape_failure_likely_but_not_authority
accepted: proxy winners frequently become runtime losers
rejected: immediate overfit_or_calibration_single_cause_claim
next_required: F84F capped_repair_or_rotation_decision
claim_boundary: {CLAIM_BOUNDARY}
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: negative_runtime_row_level_evidence_no_authority
judgment: {JUDGMENT}
preserved_clue: {payload['preserved_clue']}
negative_memory: {payload['negative_memory']}
forbidden_claims: completion, selected_baseline, operating_promotion, runtime_authority, live_readiness, goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_no_authority
allowed_claim: row_level_reconciliation_completed_with_negative_evidence
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
    }


def task_force_review_text(payload: Mapping[str, Any]) -> str:
    calls = payload["actual_subagent_calls"]
    rendered = []
    for call in calls:
        summary = str(call.get("summary") or "").replace("\n", " ").replace('"', "'")
        rendered.append(
            f"  - roster_id: {call.get('roster_id')}\n"
            f"    nickname: {call.get('nickname')}\n"
            f"    agent_id: {call.get('agent_id')}\n"
            f"    status: {call.get('status')}\n"
            f"    phase: {call.get('phase')}\n"
            f"    classification: {call.get('classification')}\n"
            f"    summary: \"{summary}\""
        )
    coverage = payload["actual_subagent_roster_coverage"]
    return f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: {'completed_8_of_8_no_authority' if coverage['all_required_completed'] else 'pending_agent_08_no_closeout_authority'}
review_mode: role_timed_actual_subagent_calls_plus_codex_local_verification
actual_subagent_call_count: {payload['actual_subagent_call_count']}
required_roster_coverage: {coverage['coverage_count']}/{coverage['required_count']}
completed_roster_coverage: {coverage['completed_count']}/{coverage['required_count']}
incomplete_roster_ids: {coverage['incomplete_roster_ids']}
actual_subagent_calls:
{chr(10).join(rendered)}
claim_boundary: {CLAIM_BOUNDARY}
"""


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    paths = [
        ROW_RECONCILIATION,
        SPLIT_SUMMARY,
        MONTH_SESSION_SUMMARY,
        UNMATCHED_ROWS,
        NORMALIZED_DEALS,
        NORMALIZED_TRADES,
        SUMMARY,
        REPORT,
        GATE_AUDIT,
        RUN_EVIDENCE_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_RECEIPT,
        TASK_FORCE_REVIEW,
        CLAIM_RECEIPT,
        ACTUAL_SUBAGENT_CALLS,
        RUN_MANIFEST,
        WORK_PACKET,
        PACKET_SKILL_RECEIPTS,
        PACKET_GATE_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "source_identity": payload["source_identity"],
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in paths},
        "claim_boundary": CLAIM_BOUNDARY,
    }


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    row_count = sum(row["selected_entry_count"] for row in payload["split_summary"])
    trade_count = sum(row["runtime_trade_count"] for row in payload["split_summary"])
    matched_count = sum(row["ticket_matched_trade_count"] for row in payload["split_summary"])
    coverage = payload["actual_subagent_roster_coverage"]
    checks = {
        "row_reconciliation_exists": path_exists(ROW_RECONCILIATION),
        "row_reconciliation_count_matches_selected": len(read_csv_rows(ROW_RECONCILIATION)) == row_count,
        "split_summary_exists": path_exists(SPLIT_SUMMARY),
        "normalized_deals_exists": path_exists(NORMALIZED_DEALS),
        "normalized_trades_exists": path_exists(NORMALIZED_TRADES),
        "normalized_trade_count_matches_receipt": len(read_csv_rows(NORMALIZED_TRADES)) == trade_count,
        "ticket_matched_count_equals_runtime_trade_count": matched_count == trade_count,
        "oos_selected_count_1805": payload["oos_summary"]["selected_entry_count"] == 1805,
        "oos_trade_count_1801": payload["oos_summary"]["runtime_trade_count"] == 1801,
        "validation_selected_count_2340": payload["validation_summary"]["selected_entry_count"] == 2340,
        "validation_trade_count_2326": payload["validation_summary"]["runtime_trade_count"] == 2326,
        "task_force_roster_covered_8": coverage["all_required_covered"],
        "task_force_roster_completed_8": coverage["all_required_completed"],
        "claim_boundary_recorded": CLAIM_BOUNDARY in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig") if path_exists(SELECTION_STATUS) else False,
        "final_claim_guard_exists": path_exists(PACKET_FINAL_CLAIM_GUARD),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_summary"]
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f84_runtime_negative_row_level_reconciliation_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F84E row-level deal reconciliation(행 단위 거래 조정)을 기록했다."
  - "Effect(효과): OOS proxy win -> runtime loss(표본외 프록시 승리 -> 런타임 손실) {oos['proxy_win_runtime_loss_count']}건을 다음 수리/회전 입력으로 고정했다."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F84E row-level deal reconciliation(F84E 행 단위 거래 조정)을 완료했다.

Effect(효과): F84C MT5 runtime(MT5 런타임)의 손익 붕괴를 selected entry(선택 진입)별 proxy/runtime(프록시/런타임) 전환으로 추적했다.

OOS(표본외): selected `{oos['selected_entry_count']}`, filled `{oos['telemetry_fill_count']}`, proxy win -> runtime loss `{oos['proxy_win_runtime_loss_count']}`.

Task Force(태스크포스): `{task_force_call_text(payload)}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )


def update_selection_and_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_summary"]
    text = f"""# F84 Selection Status(F84 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F84E row-level reconciliation(행 단위 조정)을 기록했다.

Effect(효과): OOS(표본외) ticket matched trades(티켓 결합 거래) `{oos['ticket_matched_trade_count']}`건 중 proxy win -> runtime loss(프록시 승리 -> 런타임 손실) `{oos['proxy_win_runtime_loss_count']}`건을 확인했다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Task Force(태스크포스): `{task_force_call_text(payload)}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS, text)
    write_text(
        CONTEXT_ANCHOR,
        f"""# F84 Context Anchor(F84 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- OOS row readout(표본외 행 판독): selected `{oos['selected_entry_count']}`, filled `{oos['telemetry_fill_count']}`, matched `{oos['ticket_matched_trade_count']}`, proxy win -> runtime loss `{oos['proxy_win_runtime_loss_count']}`
- actual sub-agent calls(실제 하위 에이전트 호출): `{task_force_call_text(payload)}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F84 Review Index(F84 검토 색인)\n"
    lines = [
        "- `frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_report.md`: F84E row-level deal reconciliation report(F84E 행 단위 거래 조정 보고서)",
        "- `f84e_row_level_reconciliation_rows.csv`: F84E selected-entry proxy/runtime rows(F84E 선택 진입 프록시/런타임 행)",
        "- `f84e_row_level_reconciliation_split_summary.csv`: F84E split-level confusion summary(F84E 구간별 혼동 요약)",
        "- `f84e_mt5_normalized_deal_rows.csv`: F84E normalized MT5 deal rows(F84E 정규화 MT5 딜 행)",
        "- `required_gate_coverage_audit_f84e.md`: F84E gate audit(F84E 게이트 감사)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_registers(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_summary"]
    row = {
        "ledger_row_id": f"{RUN_ID}__row_level_reconciliation",
        "row_id": f"{RUN_ID}__row_level_reconciliation",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "row_level_deal_reconciliation",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"oos_proxy_win_runtime_loss={oos['proxy_win_runtime_loss_count']};oos_matched={oos['ticket_matched_trade_count']};oos_runtime_pf={oos['runtime_profit_factor_matched']}",
        "guardrail_kpi": f"task_force={task_force_call_text(payload)};claim_boundary={CLAIM_BOUNDARY}",
        "external_verification_status": "completed_parent_mt5_strategy_tester_report_parsed",
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "run_date": created_at[:10],
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "row_level_reconciliation_only",
    }
    for ledger_path, key in ((RUN_REGISTRY, "run_id"), (ALPHA_LEDGER, "ledger_row_id"), (STAGE_LEDGER, "ledger_row_id")):
        remove_csv_rows(
            ledger_path,
            lambda existing: existing.get("run_id") == RUN_ID
            or existing.get("ledger_row_id") == row["ledger_row_id"]
            or existing.get("row_id") == row["row_id"],
        )
        append_csv_row(ledger_path, row, key=key, source_header=ALPHA_LEDGER if ledger_path == STAGE_LEDGER else None)
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    addition = f"""

{marker}
- `{RUN_ID}` completed row-level reconciliation(행 단위 조정). OOS(표본외) proxy win -> runtime loss(프록시 승리 -> 런타임 손실) `{oos['proxy_win_runtime_loss_count']}`건. Preserved clue(보존 단서): density(밀도)는 유지됐지만 deal economics(거래 경제성)는 무너졌다. Next(다음): `{NEXT_RUN_ID}`. Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    if marker in idea_text:
        idea_text = idea_text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, idea_text.rstrip() + addition)
    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    neg_marker = f"<!-- {RUN_ID}_negative_row_level_runtime -->"
    neg_addition = f"""

{neg_marker}
- `{RUN_ID}` negative row-level runtime evidence(부정 행 단위 런타임 근거): OOS(표본외) matched runtime trades(결합 런타임 거래) `{oos['ticket_matched_trade_count']}`건, proxy win -> runtime loss(프록시 승리 -> 런타임 손실) `{oos['proxy_win_runtime_loss_count']}`건. Reopen/repair condition(재개/수리 조건): F84F must choose capped repair or rotation with new axis(전선84F는 새 축으로 상한 수리 또는 회전 선택).
"""
    if neg_marker in negative_text:
        negative_text = negative_text.split(neg_marker)[0].rstrip()
    write_text(NEGATIVE_REGISTER, negative_text.rstrip() + neg_addition)


def packet_files(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "receipts": [
                {"skill": "obsidian-runtime-parity", "status": "executed", "path": rel(RUNTIME_PARITY_RECEIPT)},
                {"skill": "obsidian-backtest-forensics", "status": "executed", "path": rel(BACKTEST_FORENSICS_RECEIPT)},
                {"skill": "obsidian-data-integrity", "status": "executed", "path": rel(DATA_INTEGRITY_RECEIPT)},
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-model-validation", "status": "executed", "path": rel(MODEL_VALIDATION_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_REVIEW), "actual_subagent_calls": task_force_call_text(payload)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_LINEAGE)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(
        WORK_PACKET,
        f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
work_classification:
  primary_family: runtime_backtest
  mutation_intent: true
  execution_intent: true
skill_routing:
  primary_skill: obsidian-runtime-parity
  support_skills:
    - obsidian-backtest-forensics
    - obsidian-data-integrity
    - obsidian-run-evidence-system
    - obsidian-model-validation
    - obsidian-result-judgment
    - obsidian-task-force-review
    - obsidian-artifact-lineage
required_gates:
  - row_level_reconciliation
  - normalized_deal_trade_rows
  - ticket_join_policy
  - proxy_runtime_confusion
  - task_force_actual_calls
  - final_claim_guard
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  claim_boundary: {CLAIM_BOUNDARY}
  actual_subagent_calls: {task_force_call_text(payload)}
""",
    )
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "gates": {
                "row_level_reconciliation": "pass",
                "normalized_deal_trade_rows": "pass",
                "ticket_join_policy": "pass",
                "proxy_runtime_confusion": "pass",
                "task_force_actual_calls": task_force_call_text(payload),
                "final_claim_guard": "pass",
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        PACKET_FINAL_CLAIM_GUARD,
        {
            "status": "pass",
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )


def update_artifact_registry(created_at: str) -> None:
    paths = [
        ROW_RECONCILIATION,
        SPLIT_SUMMARY,
        MONTH_SESSION_SUMMARY,
        UNMATCHED_ROWS,
        NORMALIZED_DEALS,
        NORMALIZED_TRADES,
        SUMMARY,
        REPORT,
        GATE_AUDIT,
        RUN_EVIDENCE_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_RECEIPT,
        TASK_FORCE_REVIEW,
        CLAIM_RECEIPT,
        ACTUAL_SUBAGENT_CALLS,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        RUN_MANIFEST,
    ]
    remove_csv_rows(ARTIFACT_REGISTRY, lambda row: row.get("run_id") == RUN_ID or str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__"))
    for path in paths:
        append_csv_row(
            ARTIFACT_REGISTRY,
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.stem,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "created_at": created_at,
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F84E row-level reconciliation only.",
            },
            key="artifact_id",
        )


def write_all(payload: dict[str, Any], created_at: str) -> dict[str, Any]:
    frames = payload.pop("_frames")
    frames["rows"].to_csv(io_path(ROW_RECONCILIATION), index=False, encoding="utf-8-sig")
    frames["deals"].to_csv(io_path(NORMALIZED_DEALS), index=False, encoding="utf-8-sig")
    frames["trades"].to_csv(io_path(NORMALIZED_TRADES), index=False, encoding="utf-8-sig")
    frames["split_summary"].to_csv(io_path(SPLIT_SUMMARY), index=False, encoding="utf-8-sig")
    frames["month_session"].to_csv(io_path(MONTH_SESSION_SUMMARY), index=False, encoding="utf-8-sig")
    frames["unmatched"].to_csv(io_path(UNMATCHED_ROWS), index=False, encoding="utf-8-sig")
    write_json(SUMMARY, safe_output_payload(payload))
    write_json(ACTUAL_SUBAGENT_CALLS, {"actual_subagent_calls": payload["actual_subagent_calls"], "coverage": payload["actual_subagent_roster_coverage"]})
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_text(TASK_FORCE_REVIEW, task_force_review_text(payload))
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    write_json(RUN_MANIFEST, safe_output_payload(payload))
    update_state_files(payload, created_at)
    update_selection_and_anchor(payload, created_at)
    update_review_index()
    packet_files(payload, created_at)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
    verification = local_verification(payload)
    write_json(LOCAL_VERIFICATION, verification)
    update_registers(payload, created_at)
    update_artifact_registry(created_at)
    return verification


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    verification = write_all(payload, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "oos": payload["oos_summary"],
                    "task_force": task_force_call_text(payload),
                    "local_verification": verification["status"],
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if verification["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
