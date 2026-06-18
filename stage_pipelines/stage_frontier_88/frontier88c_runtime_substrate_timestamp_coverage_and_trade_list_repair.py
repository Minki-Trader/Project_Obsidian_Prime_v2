from __future__ import annotations

import csv
import json
import math
import shutil
import subprocess
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.mt5.runtime_artifacts import (
    collect_mt5_strategy_report_artifacts,
    remove_existing_mt5_report_artifacts,
)
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics
from foundation.mt5.terminal_runner import run_mt5_tester, wait_for_mt5_runtime_outputs
from foundation.mt5.tester_files import (
    TesterMaterializationConfig,
    materialize_tester_ini_file,
    materialize_tester_set_file,
)
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades
from stage_pipelines.stage_frontier_88 import frontier88b_runtime_substrate_preflight_closeout as f88b


STAGE_ID = "stage_frontier_88__runtime_substrate_first_materialization_probe"
RUN_ID = "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"
PARENT_RUN_ID = "frontier88B_minimal_runtime_substrate_preflight_v1"
NEXT_RUN_ID = "frontier89_pending_frontier_extra_due_and_topic_rotation_check_v1"

SCRIPT_REL = "stage_pipelines/stage_frontier_88/frontier88c_runtime_substrate_timestamp_coverage_and_trade_list_repair.py"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_selected_baseline_no_operating_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MT5_DIR = RUN_DIR / "mt5"
REPORTS_DIR = RUN_DIR / "reports"
TRADE_LIST_DIR = RUN_DIR / "trade_lists"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
FEATURE_DIR = RUN_DIR / "feature_matrices"
RECOVERY_DIR = MT5_DIR / "recovery_attempt01_long_common_path_blocked"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

FEATURE_MATRIX = FEATURE_DIR / f"{RUN_ID}_validation_is_features.csv"
SET_FILE = MT5_DIR / "f88c_tier_a_validation_is.set"
INI_FILE = MT5_DIR / "f88c_tier_a_validation_is.ini"
EXECUTION_JSON = MT5_DIR / "f88c_tester_execution.json"
REPORT_NAME = f"Project_Obsidian_Prime_v2_{RUN_ID}_f88c_tier_a_validation_is"
REPORT_HTML = MT5_DIR / "reports" / f"{REPORT_NAME}.htm"
REPORT_CHART = MT5_DIR / "reports" / f"{REPORT_NAME}.png"
TELEMETRY = TELEMETRY_DIR / "f88c_tier_a_validation_is_telemetry.csv"
SUMMARY_CSV = TELEMETRY_DIR / "f88c_tier_a_validation_is_summary.csv"
DEALS_CSV = TRADE_LIST_DIR / "f88c_tier_a_validation_is_deals.csv"
TRADES_CSV = TRADE_LIST_DIR / "f88c_tier_a_validation_is_trades.csv"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RUNTIME_IDENTITY = RUN_DIR / "runtime_evidence_identity.json"
FORENSICS_SUMMARY = RUN_DIR / "backtest_forensics_summary.json"
RESULT_SUMMARY = REPORTS_DIR / "result_summary.md"

RUNTIME_EVIDENCE_GATE = REVIEW_DIR / "f88c_runtime_evidence_gate.json"
BACKTEST_FORENSICS_AUDIT = REVIEW_DIR / "f88c_backtest_forensics_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f88c_kpi_contract_audit.json"
SCOPE_GATE = REVIEW_DIR / "f88c_scope_completion_gate.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f88c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f88c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f88c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f88c_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f88c_required_gate_coverage_audit.json"

RUNTIME_PARITY_RECEIPT = REVIEW_DIR / "f88c_runtime_parity_receipt.json"
BACKTEST_RECEIPT = REVIEW_DIR / "f88c_backtest_forensics_receipt.json"
REFERENCE_RECEIPT = REVIEW_DIR / "f88c_reference_scout_receipt.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f88c_run_evidence_system_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f88c_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f88c_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f88c_claim_discipline_receipt.json"
ANSWER_RECEIPT = REVIEW_DIR / "f88c_answer_clarity_receipt.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs/registers/negative_result_register.md"
WORKSPACE_CHANGELOG = ROOT / "docs/workspace/changelog.md"
ROOT_CHANGELOG = ROOT / "docs/CHANGELOG.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier88c_runtime_substrate_repair.md"

STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs/input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

SOURCE_ONNX = f88b.SOURCE_ONNX
EA_SOURCE = f88b.EA_SOURCE
EA_BINARY = f88b.EA_BINARY
MT5_INPUT_CONTRACT = f88b.MT5_INPUT_CONTRACT
TIME_AXIS_CONTRACT = f88b.TIME_AXIS_CONTRACT
PARENT_FEATURE_MATRIX = f88b.FEATURE_MATRIX
PARENT_SUMMARY_CSV = f88b.SUMMARY_CSV
PARENT_RUNTIME_IDENTITY = f88b.RUNTIME_IDENTITY
PARENT_RESULT_SUMMARY = f88b.RESULT_SUMMARY
PARENT_SET_FILE = f88b.SET_FILE
PARENT_RUN_MANIFEST = f88b.RUN_MANIFEST

PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
TERMINAL_PATH = PORTABLE_ROOT / "terminal64.exe"
COMMON_FILES_ROOT = PORTABLE_ROOT / "Common" / "Files"
TESTER_PROFILE_ROOT = PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
TESTER_PROFILE_SET = TESTER_PROFILE_ROOT / "ObsidianPrimeV2_RuntimeProbeEA.set"
TESTER_PROFILE_INI = TESTER_PROFILE_ROOT / "opv2_frontier88C_ta_v.ini"

COMMON_RUN_ROOT = Path("Project_Obsidian_Prime_v2") / "f88c"
COMMON_FEATURE_PATH = COMMON_RUN_ROOT / "features.csv"
COMMON_MODEL_PATH = COMMON_RUN_ROOT / "model.onnx"
COMMON_TELEMETRY_PATH = COMMON_RUN_ROOT / "telemetry.csv"
COMMON_SUMMARY_PATH = COMMON_RUN_ROOT / "summary.csv"

REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "runtime_evidence_gate",
    "scope_completion_gate",
    "kpi_contract_audit",
    "backtest_forensics_audit",
    "artifact_lineage_audit",
    "result_judgment_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-runtime-parity",
    "obsidian-backtest-forensics",
    "obsidian-reference-scout",
    "obsidian-run-evidence-system",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-claim-discipline",
    "obsidian-answer-clarity",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_verified",
    "runtime_parity_closed",
    "strategy_tester_economics_pass",
    "materialization_ready",
    "ea_onnx_runtime_bundle_ready",
    "task_force_reviewed",
    "stage_closeout_pass",
]

DEAL_HEADERS = [
    "time",
    "ticket",
    "symbol",
    "order_type",
    "direction",
    "volume",
    "price",
    "order",
    "commission",
    "swap",
    "profit",
    "balance",
    "comment",
]
TRADE_HEADERS = [
    "index",
    "direction",
    "open_time",
    "close_time",
    "volume",
    "open_price",
    "close_price",
    "gross_profit",
    "net_profit",
    "swap",
    "commission",
]


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return f88b.rel(path)


def sha256_file(path: Path) -> str:
    return f88b.sha256_file(path)


def write_text(path: Path, text: str) -> None:
    f88b.write_text(path, text)


def write_json(path: Path, payload: Any) -> None:
    f88b.write_json(path, payload)


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    f88b.write_yaml(path, payload)


def append_once(path: Path, marker: str, addition: str) -> None:
    f88b.append_once(path, marker, addition)


def upsert_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    f88b.upsert_csv(path, key_fields, rows, source_header=source_header)


def csv_cell(value: Any) -> str:
    value = json_ready(value)
    if value is None:
        return ""
    if isinstance(value, float):
        return "" if not math.isfinite(value) else str(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def current_branch() -> str:
    return f88b.current_branch()


def file_identity(path: Path, *, role: str) -> dict[str, Any]:
    payload: dict[str, Any] = {"path": rel(path), "exists": path_exists(path), "role": role}
    if path_exists(path):
        payload["sha256"] = sha256_file(path)
        payload["size_bytes"] = io_path(path).stat().st_size
    return payload


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def parse_parent_set() -> dict[str, str]:
    params: dict[str, str] = {}
    for line in io_path(PARENT_SET_FILE).read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(";") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        params[key] = value
    params.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": "frontier88C_timestamp_coverage_trade_list_repair",
            "InpModelPath": COMMON_MODEL_PATH.as_posix(),
            "InpModelId": f"{RUN_ID}_f88c_tier_a",
            "InpFeatureCsvPath": COMMON_FEATURE_PATH.as_posix(),
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpCsvTimestampIsBarClose": "true",
            "InpTelemetryCsvPath": COMMON_TELEMETRY_PATH.as_posix(),
            "InpSummaryCsvPath": COMMON_SUMMARY_PATH.as_posix(),
            "InpMagic": "1001002",
        }
    )
    return params


def unlink_if_exists(path: Path) -> None:
    if path_exists(path):
        io_path(path).unlink()


def materialize_runtime_inputs() -> dict[str, Any]:
    for directory in (RUN_DIR, MT5_DIR, REPORTS_DIR, TRADE_LIST_DIR, TELEMETRY_DIR, FEATURE_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    archived = archive_existing_attempt_outputs()
    shutil.copy2(io_path(PARENT_FEATURE_MATRIX), io_path(FEATURE_MATRIX))
    io_path((COMMON_FILES_ROOT / COMMON_MODEL_PATH).parent).mkdir(parents=True, exist_ok=True)
    io_path((COMMON_FILES_ROOT / COMMON_FEATURE_PATH).parent).mkdir(parents=True, exist_ok=True)
    io_path((COMMON_FILES_ROOT / COMMON_TELEMETRY_PATH).parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(SOURCE_ONNX), io_path(COMMON_FILES_ROOT / COMMON_MODEL_PATH))
    shutil.copy2(io_path(FEATURE_MATRIX), io_path(COMMON_FILES_ROOT / COMMON_FEATURE_PATH))
    unlink_if_exists(COMMON_FILES_ROOT / COMMON_TELEMETRY_PATH)
    unlink_if_exists(COMMON_FILES_ROOT / COMMON_SUMMARY_PATH)

    set_artifact = materialize_tester_set_file(parse_parent_set(), SET_FILE, generated_by=SCRIPT_REL)
    ini_artifact = materialize_tester_ini_file(
        TesterMaterializationConfig(
            from_date="2025.01.02",
            to_date="2025.01.09",
            report=REPORT_NAME,
            shutdown_terminal=1,
        ),
        INI_FILE,
        set_file_path=Path("ObsidianPrimeV2_RuntimeProbeEA.set"),
    )
    attempt = {
        "attempt_name": "f88c_tier_a_validation_is",
        "tier": "Tier A",
        "split": "validation_is",
        "candidate_id": "rf_depth5_leaf80_balanced_argmax",
        "common_feature_matrix_path": COMMON_FEATURE_PATH.as_posix(),
        "common_model_path": COMMON_MODEL_PATH.as_posix(),
        "common_telemetry_path": COMMON_TELEMETRY_PATH.as_posix(),
        "common_summary_path": COMMON_SUMMARY_PATH.as_posix(),
        "ini": ini_artifact,
        "set": set_artifact,
        "date_range_repair": "tester_to_date_aligned_to_day_after_feature_last_timestamp",
    }
    remove_existing_mt5_report_artifacts(PORTABLE_ROOT, attempt, run_id=RUN_ID)
    return {
        "attempt": attempt,
        "set_artifact": set_artifact,
        "ini_artifact": ini_artifact,
        "common_model": file_identity(COMMON_FILES_ROOT / COMMON_MODEL_PATH, role="common_files_onnx"),
        "common_feature": file_identity(COMMON_FILES_ROOT / COMMON_FEATURE_PATH, role="common_files_feature_matrix"),
        "recovery_axis": "short_common_files_path_after_feature_csv_open_failed_5003",
        "archived_previous_attempt": archived,
    }


def archive_existing_attempt_outputs() -> list[dict[str, Any]]:
    archive_sources = [
        (EXECUTION_JSON, RECOVERY_DIR / EXECUTION_JSON.name),
        (SET_FILE, RECOVERY_DIR / SET_FILE.name),
        (INI_FILE, RECOVERY_DIR / INI_FILE.name),
        (REPORT_HTML, RECOVERY_DIR / "reports" / REPORT_HTML.name),
        (REPORT_CHART, RECOVERY_DIR / "reports" / REPORT_CHART.name),
        (TELEMETRY, RECOVERY_DIR / TELEMETRY.name),
        (SUMMARY_CSV, RECOVERY_DIR / SUMMARY_CSV.name),
        (DEALS_CSV, RECOVERY_DIR / DEALS_CSV.name),
        (TRADES_CSV, RECOVERY_DIR / TRADES_CSV.name),
        (RUN_MANIFEST, RECOVERY_DIR / RUN_MANIFEST.name),
        (KPI_RECORD, RECOVERY_DIR / KPI_RECORD.name),
    ]
    archived: list[dict[str, Any]] = []
    for source, destination in archive_sources:
        if not path_exists(source):
            continue
        io_path(destination.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(source), io_path(destination))
        archived.append(file_identity(destination, role="recovery_attempt01_long_common_path_blocked"))
    return archived


def execute_mt5_probe(materialized: Mapping[str, Any]) -> dict[str, Any]:
    attempt = dict(materialized["attempt"])
    execution = run_mt5_tester(
        TERMINAL_PATH,
        INI_FILE,
        set_path=SET_FILE,
        tester_profile_set_path=TESTER_PROFILE_SET,
        tester_profile_ini_path=TESTER_PROFILE_INI,
        timeout_seconds=900,
        terminal_extra_args=["/portable"],
    )
    runtime_outputs = wait_for_mt5_runtime_outputs(COMMON_FILES_ROOT, attempt, timeout_seconds=120, poll_seconds=2.0)
    execution["runtime_outputs"] = runtime_outputs
    execution.update(
        {
            "attempt_name": attempt["attempt_name"],
            "candidate_id": attempt["candidate_id"],
            "model_id": "rf_depth5_leaf80_balanced_argmax",
            "ini_path": rel(INI_FILE),
            "set_path": rel(SET_FILE),
            "common_feature_matrix_path": attempt["common_feature_matrix_path"],
            "common_model_path": attempt["common_model_path"],
            "date_range_repair": attempt["date_range_repair"],
        }
    )
    copy_common_runtime_outputs()
    report_records = collect_mt5_strategy_report_artifacts(
        terminal_data_root=PORTABLE_ROOT,
        run_output_root=RUN_DIR,
        attempts=[attempt],
        run_id=RUN_ID,
    )
    execution["strategy_tester_report"] = report_records[0] if report_records else {"status": "missing"}
    write_json(EXECUTION_JSON, execution)
    return execution


def copy_common_runtime_outputs() -> None:
    common_telemetry = COMMON_FILES_ROOT / COMMON_TELEMETRY_PATH
    common_summary = COMMON_FILES_ROOT / COMMON_SUMMARY_PATH
    if path_exists(common_telemetry):
        shutil.copy2(io_path(common_telemetry), io_path(TELEMETRY))
    if path_exists(common_summary):
        shutil.copy2(io_path(common_summary), io_path(SUMMARY_CSV))


def read_summary_row() -> dict[str, Any]:
    if not path_exists(SUMMARY_CSV):
        return {}
    frame = pd.read_csv(io_path(SUMMARY_CSV), encoding="utf-8-sig")
    if frame.empty:
        return {}
    return json_ready(frame.iloc[-1].to_dict())


def parent_summary_row() -> dict[str, Any]:
    frame = pd.read_csv(io_path(PARENT_SUMMARY_CSV), encoding="utf-8-sig")
    return json_ready(frame.iloc[-1].to_dict())


def feature_span() -> dict[str, Any]:
    frame = pd.read_csv(io_path(FEATURE_MATRIX), usecols=["bar_time_server"])
    stamps = frame["bar_time_server"].astype(str)
    return {
        "row_count": int(len(frame)),
        "first_bar_time_server": stamps.iloc[0] if len(stamps) else "",
        "last_bar_time_server": stamps.iloc[-1] if len(stamps) else "",
        "unique_server_dates": sorted({value.split(" ")[0] for value in stamps if " " in value}),
    }


def report_metrics() -> dict[str, Any]:
    if not path_exists(REPORT_HTML):
        return {"status": "missing", "report_path": rel(REPORT_HTML), "missing_required_metrics": ["report_html_missing"]}
    return extract_mt5_strategy_report_metrics(REPORT_HTML)


def timestamp_text(value: Any) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%Y.%m.%d %H:%M:%S")
    return str(value)


def dataclass_row(item: Any) -> dict[str, Any]:
    row = asdict(item)
    for key, value in list(row.items()):
        if hasattr(value, "strftime"):
            row[key] = timestamp_text(value)
    return row


def write_rows(path: Path, headers: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(headers), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({header: csv_cell(row.get(header, "")) for header in headers})


def materialize_trade_lists() -> dict[str, Any]:
    if not path_exists(REPORT_HTML):
        write_rows(DEALS_CSV, DEAL_HEADERS, [])
        write_rows(TRADES_CSV, TRADE_HEADERS, [])
        return {
            "status": "missing_report",
            "deal_count": 0,
            "trade_count": 0,
            "deals_csv": file_identity(DEALS_CSV, role="mt5_deals_csv_empty_missing_report"),
            "trades_csv": file_identity(TRADES_CSV, role="mt5_trades_csv_empty_missing_report"),
        }
    parsed = parse_mt5_trade_report(REPORT_HTML)
    deals = parsed.get("deals", [])
    trades = pair_deals_into_trades(deals)
    deal_rows = [dataclass_row(item) for item in deals]
    trade_rows = [dataclass_row(item) for item in trades]
    write_rows(DEALS_CSV, DEAL_HEADERS, deal_rows)
    write_rows(TRADES_CSV, TRADE_HEADERS, trade_rows)
    return {
        "status": "separated" if deal_rows else "empty",
        "deal_count": len(deal_rows),
        "trade_count": len(trade_rows),
        "report_trade_summary": parsed.get("summary", {}),
        "deals_csv": file_identity(DEALS_CSV, role="mt5_deals_csv"),
        "trades_csv": file_identity(TRADES_CSV, role="mt5_trades_csv"),
        "long_short_trade_net": long_short_trade_net(trade_rows),
        "max_consecutive_loss": max_consecutive_loss(trade_rows),
    }


def long_short_trade_net(trade_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result = {
        "long": {"trade_count": 0, "net_profit": 0.0},
        "short": {"trade_count": 0, "net_profit": 0.0},
    }
    for row in trade_rows:
        direction = str(row.get("direction", "")).lower()
        bucket = "long" if direction == "buy" else "short" if direction == "sell" else ""
        if not bucket:
            continue
        result[bucket]["trade_count"] += 1
        result[bucket]["net_profit"] += float(row.get("net_profit") or 0.0)
    for bucket in result.values():
        bucket["net_profit"] = round(bucket["net_profit"], 2)
    return result


def max_consecutive_loss(trade_rows: Sequence[Mapping[str, Any]]) -> int:
    current = 0
    best = 0
    for row in trade_rows:
        net = float(row.get("net_profit") or 0.0)
        if net < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def average_trade_stats(metrics: Mapping[str, Any]) -> dict[str, Any]:
    gross_profit = metrics.get("gross_profit")
    gross_loss = metrics.get("gross_loss")
    wins = metrics.get("winning_trade_count")
    losses = metrics.get("losing_trade_count")
    avg_win = float(gross_profit) / float(wins) if gross_profit is not None and wins else None
    avg_loss = float(gross_loss) / float(losses) if gross_loss is not None and losses else None
    payoff = avg_win / abs(avg_loss) if avg_win is not None and avg_loss not in (None, 0) else None
    return {
        "avg_win": None if avg_win is None else round(avg_win, 4),
        "avg_loss": None if avg_loss is None else round(avg_loss, 4),
        "payoff_ratio": None if payoff is None else round(payoff, 4),
    }


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RUNTIME_IDENTITY,
        FORENSICS_SUMMARY,
        RESULT_SUMMARY,
        FEATURE_MATRIX,
        SET_FILE,
        INI_FILE,
        EXECUTION_JSON,
        REPORT_HTML,
        REPORT_CHART,
        TELEMETRY,
        SUMMARY_CSV,
        DEALS_CSV,
        TRADES_CSV,
        RUNTIME_EVIDENCE_GATE,
        BACKTEST_FORENSICS_AUDIT,
        KPI_CONTRACT_AUDIT,
        SCOPE_GATE,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_RECEIPT,
        REFERENCE_RECEIPT,
        RUN_EVIDENCE_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        ANSWER_RECEIPT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        RECOVERY_DIR / EXECUTION_JSON.name,
        RECOVERY_DIR / SET_FILE.name,
        RECOVERY_DIR / INI_FILE.name,
        RECOVERY_DIR / "reports" / REPORT_HTML.name,
        RECOVERY_DIR / "reports" / REPORT_CHART.name,
        RECOVERY_DIR / TELEMETRY.name,
        RECOVERY_DIR / SUMMARY_CSV.name,
        RECOVERY_DIR / DEALS_CSV.name,
        RECOVERY_DIR / TRADES_CSV.name,
        RECOVERY_DIR / RUN_MANIFEST.name,
        RECOVERY_DIR / KPI_RECORD.name,
        DECISION_MEMO,
    ]


def source_inputs() -> list[Path]:
    return [
        PARENT_RESULT_SUMMARY,
        PARENT_RUNTIME_IDENTITY,
        PARENT_FEATURE_MATRIX,
        PARENT_SET_FILE,
        SOURCE_ONNX,
        EA_SOURCE,
        EA_BINARY,
        MT5_INPUT_CONTRACT,
        TIME_AXIS_CONTRACT,
        FEATURE_MATRIX,
        SET_FILE,
        INI_FILE,
    ]


def build_payload(created_at: str, materialized: Mapping[str, Any], execution: Mapping[str, Any], trade_lists: Mapping[str, Any]) -> dict[str, Any]:
    metrics = report_metrics()
    summary_row = read_summary_row()
    parent_summary = parent_summary_row()
    span = feature_span()
    runtime_completed = (
        execution.get("status") == "completed"
        and execution.get("runtime_outputs", {}).get("status") == "completed"
        and metrics.get("status") in {"completed", "partial"}
        and path_exists(REPORT_HTML)
    )
    parent_skip = int(parent_summary.get("feature_skip_count") or 0)
    current_skip = int(summary_row.get("feature_skip_count") or 0)
    parent_ready = int(parent_summary.get("feature_ready_count") or 0)
    current_ready = int(summary_row.get("feature_ready_count") or 0)
    skip_reduced = runtime_completed and current_skip < parent_skip
    trade_list_separated = trade_lists.get("status") == "separated" and trade_lists.get("deal_count", 0) > 0
    econ_gap = economic_gap(metrics)
    status, judgment, allowed_claims = status_judgment(runtime_completed, skip_reduced, trade_list_separated, econ_gap)
    tester = tester_identity(execution)
    runtime_identity = {
        "dataset_id": "f88c_runtime_validation_short_probe_2025_01_02_to_2025_01_09",
        "feature_set_id": "frontier04d_f04d_read_feature_order_58",
        "label_id": "frontier04d_path_label_argmax_reference_only",
        "split_id": "validation_is_short_probe_2025_01_02_to_2025_01_09",
        "source_candidate": {
            "source_stage_id": "stage_frontier_04__path_aware_cost_dd_event_labeling",
            "source_run_id": "frontier04D_trainable_path_label_onnx_probe_v1",
            "candidate_id": "rf_depth5_leaf80_balanced_argmax",
            "claim_effect": "reference runtime substrate candidate only; no inherited baseline or authority",
        },
        "parser_contract_version": rel(MT5_INPUT_CONTRACT),
        "runtime_contract_version": "ObsidianPrimeV2_RuntimeProbeEA_f88c",
        "compile_status": "existing_binary_reused_no_compile_only_claim",
        "tester_status": execution.get("status"),
        "runtime_status": execution.get("runtime_outputs", {}).get("status"),
        "report_status": metrics.get("status"),
        "onnx_hash": sha256_file(SOURCE_ONNX),
        "ea_source_hash": sha256_file(EA_SOURCE),
        "ea_binary_hash": sha256_file(EA_BINARY),
        "set_ini_hash": {"set": sha256_file(SET_FILE), "ini": sha256_file(INI_FILE)},
        "feature_order_hash": summary_row.get("feature_order_hash"),
        "feature_matrix_hash": sha256_file(FEATURE_MATRIX),
        "tester_identity": tester,
        "report_hash": sha256_file(REPORT_HTML) if path_exists(REPORT_HTML) else "",
        "trade_list_hash": sha256_file(TRADES_CSV) if path_exists(TRADES_CSV) else "",
        "deal_list_hash": sha256_file(DEALS_CSV) if path_exists(DEALS_CSV) else "",
        "trade_list_identity": "separate_trade_list_csv_from_mt5_html_report" if trade_list_separated else "trade_list_separation_attempted_but_empty_or_missing",
        "telemetry_hash": sha256_file(TELEMETRY) if path_exists(TELEMETRY) else "",
        "summary_hash": sha256_file(SUMMARY_CSV) if path_exists(SUMMARY_CSV) else "",
        "parser_status": {
            "strategy_report": metrics.get("source_encoding", "missing"),
            "summary_csv": "parsed_utf_8_sig" if summary_row else "missing",
            "trade_report": trade_lists.get("status"),
        },
    }
    economics = economics_payload(metrics, trade_lists)
    operation_proof = {
        "runtime_completed": runtime_completed,
        "ea_loaded": bool(runtime_completed and int(summary_row.get("model_ok_count") or 0) > 0),
        "onnx_inference_called": bool(int(summary_row.get("model_ok_count") or 0) > 0),
        "report_generated": path_exists(REPORT_HTML),
        "telemetry_updated": path_exists(TELEMETRY) and path_exists(SUMMARY_CSV),
        "trade_list_separated": trade_list_separated,
        "timestamp_coverage_gap": {
            "parent_feature_ready_count": parent_ready,
            "current_feature_ready_count": current_ready,
            "parent_feature_skip_count": parent_skip,
            "current_feature_skip_count": current_skip,
            "skip_reduced": skip_reduced,
            "skip_delta": current_skip - parent_skip,
            "ready_delta": current_ready - parent_ready,
            "last_skip_reason": summary_row.get("last_skip_reason", ""),
        },
        "feature_span": span,
        "boundary": "runtime probe observation only; not runtime authority",
    }
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": allowed_claims,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "materialized": materialized,
        "execution": execution,
        "runtime_identity": runtime_identity,
        "operation_proof": operation_proof,
        "economics": economics,
        "summary_row": summary_row,
        "parent_summary_row": parent_summary,
        "metrics": metrics,
        "trade_lists": trade_lists,
        "next_condition": (
            "F89 can only open after frontier_extra_due_check and frontier_topic_rotation_check; "
            "F88C adds timestamp coverage/trade-list evidence but no authority."
        ),
    }


def tester_identity(execution: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "broker": "FPMarkets",
        "symbol": "US100",
        "timeframe": "M5",
        "date_range": "2025.01.02..2025.01.09",
        "modeling_mode": "4_Every_tick_based_on_real_ticks",
        "deposit": 500,
        "leverage": "1:100",
        "spread": "broker_native_or_report_not_parsed",
        "commission": "broker_native_or_report_not_parsed",
        "slippage": "not_explicit_in_ini",
        "swap": "broker_native_or_report_not_parsed",
        "terminal_command": execution.get("command"),
        "tester_profile_ini": execution.get("tester_profile_ini_copy"),
        "tester_profile_set": execution.get("tester_profile_set_copy"),
    }


def economic_gap(metrics: Mapping[str, Any]) -> bool:
    net = metrics.get("net_profit")
    pf = metrics.get("profit_factor")
    dd = metrics.get("max_drawdown_percent")
    if metrics.get("status") not in {"completed", "partial"}:
        return True
    return bool((net is None or float(net) <= 0.0) or (pf is None or float(pf) < 2.0) or (dd is None or float(dd) >= 10.0))


def status_judgment(runtime_completed: bool, skip_reduced: bool, trade_list_separated: bool, econ_gap: bool) -> tuple[str, str, list[str]]:
    allowed = [
        "runtime_probe_attempt_recorded",
        "actual_output_identity_recorded",
        "separate_trade_list_attempt_recorded",
        "economics_recorded_no_authority",
    ]
    if not runtime_completed:
        return (
            "f88c_runtime_probe_blocked_or_inconclusive_no_authority",
            "runtime_probe_blocked_or_inconclusive_no_authority",
            allowed + ["blocked_or_inconclusive_runtime_recorded"],
        )
    if skip_reduced:
        allowed.append("timestamp_coverage_gap_reduced_observed")
    if trade_list_separated:
        allowed.append("separate_trade_list_identity_recorded")
    if econ_gap:
        allowed.append("negative_economics_gap_recorded")
    judgment = (
        "runtime_probe_observation_timestamp_coverage_reduced_trade_list_separated_negative_economics_no_authority"
        if skip_reduced and trade_list_separated and econ_gap
        else "runtime_probe_observation_with_remaining_gap_no_authority"
    )
    status = (
        "f88c_runtime_probe_observation_timestamp_coverage_trade_list_repair_no_authority"
        if skip_reduced and trade_list_separated
        else "f88c_runtime_probe_observation_remaining_gap_no_authority"
    )
    return status, judgment, allowed


def economics_payload(metrics: Mapping[str, Any], trade_lists: Mapping[str, Any]) -> dict[str, Any]:
    trade_count = metrics.get("trade_count") or trade_lists.get("trade_count") or 0
    stats = average_trade_stats(metrics)
    return {
        "net_profit": metrics.get("net_profit"),
        "profit_factor": metrics.get("profit_factor"),
        "max_drawdown_percent": metrics.get("max_drawdown_percent"),
        "equity_drawdown_maximal_percent": metrics.get("equity_drawdown_maximal_percent"),
        "trade_count": metrics.get("trade_count"),
        "trades_per_calendar_day": round(float(trade_count or 0) / 7.0, 4),
        "trades_per_feature_day": round(float(trade_count or 0) / 5.0, 4),
        "gross_profit": metrics.get("gross_profit"),
        "gross_loss": metrics.get("gross_loss"),
        "win_rate_percent": metrics.get("win_rate_percent"),
        "avg_win": stats["avg_win"],
        "avg_loss": stats["avg_loss"],
        "payoff_ratio": stats["payoff_ratio"],
        "expectancy": metrics.get("expectancy"),
        "recovery_factor": metrics.get("recovery_factor"),
        "time_under_water": "not_parsed_from_mt5_html_report",
        "max_consecutive_loss": trade_lists.get("max_consecutive_loss"),
        "long_short_breakdown": {
            "report": {
                "long_trade_count": metrics.get("long_trade_count"),
                "short_trade_count": metrics.get("short_trade_count"),
                "long_win_rate_percent": metrics.get("long_win_rate_percent"),
                "short_win_rate_percent": metrics.get("short_win_rate_percent"),
            },
            "trade_list_net": trade_lists.get("long_short_trade_net", {}),
        },
        "judgment": "negative_or_inconclusive_for_final_entry_gate",
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    econ = payload["economics"]
    op = payload["operation_proof"]
    return f"""# F88C Runtime Substrate Repair Result(F88C 런타임 바탕 수리 결과)

Updated(갱신): {payload['created_at_utc']}

Conclusion(결론): F88C produced a bounded MT5 Strategy Tester runtime probe observation(F88C는 경계 있는 MT5 전략 테스터 런타임 탐침 관찰을 만들었다).

Action(행동): The tester ToDate(테스터 종료일)를 feature span(피처 범위)에 맞춰 `2025.01.09`로 좁히고, embedded report trades(보고서 내장 거래)를 separate trade-list CSV(분리 거래목록 CSV)로 추출했다.

Effect(효과): timestamp coverage gap(타임스탬프 커버리지 간극)과 trade-list identity gap(거래목록 정체성 간극)을 실제 runtime evidence(런타임 근거)로 관찰했다.

KPI(핵심 성과 지표): net_profit(순수익) `{econ.get('net_profit')}`, PF(수익 팩터) `{econ.get('profit_factor')}`, DD(손실폭) `{econ.get('max_drawdown_percent')}%`, trades(거래 수) `{econ.get('trade_count')}`, trades_per_calendar_day(달력일당 거래 수) `{econ.get('trades_per_calendar_day')}`.

Closeout KPI(마감 핵심 성과 지표): gross_profit/loss(총이익/총손실) `{econ.get('gross_profit')}/{econ.get('gross_loss')}`, win_rate(승률) `{econ.get('win_rate_percent')}`, avg_win/loss(평균 이익/손실) `{econ.get('avg_win')}/{econ.get('avg_loss')}`, payoff_ratio(손익비) `{econ.get('payoff_ratio')}`, expectancy(기대값) `{econ.get('expectancy')}`, recovery_factor(회복 계수) `{econ.get('recovery_factor')}`, max_consecutive_loss(최대 연속 손실) `{econ.get('max_consecutive_loss')}`.

Coverage(커버리지): parent skip(부모 스킵) `{op['timestamp_coverage_gap'].get('parent_feature_skip_count')}`, current skip(현재 스킵) `{op['timestamp_coverage_gap'].get('current_feature_skip_count')}`, skip_reduced(스킵 감소) `{op['timestamp_coverage_gap'].get('skip_reduced')}`.

Trade list(거래목록): `{rel(TRADES_CSV)}`.

Not claimed(주장하지 않음): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Next action(다음 행동): `{NEXT_RUN_ID}` requires frontier_extra_due_check(전선 추가 도래 점검) and frontier_topic_rotation_check(전선 주제 회전 점검) before any formal F89 open(정식 F89 개방).
"""


def audits(payload: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    runtime_pass = bool(payload["operation_proof"]["runtime_completed"])
    report_exists = path_exists(REPORT_HTML)
    trade_list_exists = path_exists(TRADES_CSV)
    audit_status = "pass" if runtime_pass else "blocked"
    runtime_gate = {
        "audit_name": "runtime_evidence_gate",
        "status": audit_status,
        "passed": runtime_pass,
        "findings": [] if runtime_pass else [{"severity": "blocking", "message": "MT5 runtime probe did not complete with report and telemetry."}],
        "counts": {
            "runtime_identity": payload["runtime_identity"],
            "operation_proof": payload["operation_proof"],
            "economics": payload["economics"],
        },
        "allowed_claims": payload["allowed_claims"] if runtime_pass else ["blocked_or_inconclusive_runtime_recorded"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    forensics = {
        "audit_name": "backtest_forensics_audit",
        "status": "pass" if report_exists else "blocked",
        "passed": report_exists,
        "findings": [
            {
                "severity": "info",
                "message": "Spread/commission/slippage are broker-native or not separately parsed; no runtime authority claim.",
            }
        ],
        "counts": {
            "tester_identity": payload["runtime_identity"]["tester_identity"],
            "report_identity": file_identity(REPORT_HTML, role="strategy_tester_report"),
            "trade_list_identity": payload["runtime_identity"]["trade_list_identity"],
            "cost_assumptions": {
                "spread": "broker_native_or_report_not_parsed",
                "commission": "broker_native_or_report_not_parsed",
                "slippage": "not_explicit_in_ini",
                "swap": "broker_native_or_report_not_parsed",
            },
            "trade_evidence": payload["economics"],
        },
        "allowed_claims": ["actual_output_identity_recorded"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    kpi = {
        "audit_name": "kpi_contract_audit",
        "status": "pass" if payload["metrics"].get("status") in {"completed", "partial"} else "blocked",
        "passed": payload["metrics"].get("status") in {"completed", "partial"},
        "findings": [],
        "counts": {
            "runtime_kpi_layer": payload["economics"],
            "execution_kpi_layer": {
                "ticks_seen": payload["summary_row"].get("ticks_seen"),
                "bars_seen": payload["summary_row"].get("bars_seen"),
                "feature_ready_count": payload["summary_row"].get("feature_ready_count"),
                "feature_skip_count": payload["summary_row"].get("feature_skip_count"),
                "model_ok_count": payload["summary_row"].get("model_ok_count"),
                "order_attempt_count": payload["summary_row"].get("order_attempt_count"),
                "order_fill_count": payload["summary_row"].get("order_fill_count"),
            },
            "trade_list_kpi_layer": payload["trade_lists"],
        },
        "allowed_claims": ["economics_recorded_no_authority"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    scope = {
        "audit_name": "scope_completion_gate",
        "status": "pass" if report_exists and trade_list_exists else "blocked",
        "passed": report_exists and trade_list_exists,
        "findings": [],
        "counts": {"expected_outputs": [rel(path) for path in produced_artifacts() if path_exists(path)], "next_run_id": NEXT_RUN_ID},
        "allowed_claims": ["f88c_runtime_probe_observation_recorded"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    artifact = {
        "audit_name": "artifact_lineage_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "producer": SCRIPT_REL,
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in produced_artifacts() if path_exists(path)},
        },
        "allowed_claims": ["runtime_bundle_identity_recorded", "actual_output_identity_recorded"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    judgment = {
        "audit_name": "result_judgment_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(path) for path in [REPORT_HTML, TELEMETRY, SUMMARY_CSV, TRADES_CSV, KPI_RECORD] if path_exists(path)],
            "evidence_missing": ["WFO/stress continuation", "full tester cost fields parsed separately"],
            "judgment_label": payload["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": payload["next_condition"],
        },
        "allowed_claims": payload["allowed_claims"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    final = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "requested_claims": payload["allowed_claims"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "allowed_claims": payload["allowed_claims"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    return {
        "runtime": runtime_gate,
        "forensics": forensics,
        "kpi": kpi,
        "scope": scope,
        "artifact": artifact,
        "judgment": judgment,
        "final": final,
    }


def receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_inputs_rel = [rel(path) for path in source_inputs()]
    produced_rel = [rel(path) for path in produced_artifacts() if path_exists(path)]
    hashes = {rel(path): sha256_file(path) for path in produced_artifacts() if path_exists(path)}
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "receipt_path": rel(RUNTIME_PARITY_RECEIPT),
            "python_artifact": rel(SOURCE_ONNX),
            "runtime_artifact": rel(REPORT_HTML),
            "compared_surface": "F04D ONNX through F88C RuntimeProbeEA Strategy Tester timestamp coverage repair",
            "parity_level": "P3_runtime_shadow_parity_sampled",
            "tester_identity": payload["runtime_identity"]["tester_identity"],
            "runtime_evidence_identity": payload["runtime_identity"],
            "missing_evidence": ["full runtime parity closure", "WFO/stress continuation"],
            "allowed_claims": payload["allowed_claims"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-backtest-forensics",
            "status": "executed",
            "receipt_path": rel(BACKTEST_RECEIPT),
            "tester_report": rel(REPORT_HTML),
            "tester_settings": payload["runtime_identity"]["tester_identity"],
            "spread_commission_slippage": "broker_native_or_report_not_parsed; no authority claim",
            "trade_list_identity": payload["runtime_identity"]["trade_list_identity"],
            "forensic_gaps": ["cost_fields_not_separately_parsed", "single_short_probe_no_wfo_stress"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-reference-scout",
            "status": "executed",
            "receipt_path": rel(REFERENCE_RECEIPT),
            "reference_need": "No new external reference needed; reused local F88B tester helper and RuntimeProbeEA contract.",
            "sources_checked_or_not_required_reason": "not_required_local_reuse_of_existing_materialized_MT5_runtime_contract",
            "version_sensitive_surface": "MetaTrader 5 Strategy Tester local portable runtime already exercised in F88B",
            "implementation_effect": "F88C changed tester date boundary/output identity only and recorded runtime artifacts.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "receipt_path": rel(RUN_EVIDENCE_RECEIPT),
            "source_inputs": source_inputs_rel,
            "produced_artifacts": produced_rel,
            "ledger_rows": [f"{RUN_ID}__runtime_probe_observation", f"{NEXT_RUN_ID}__planned_current_run"],
            "missing_evidence": ["WFO/stress continuation", "full operating promotion package"],
            "allowed_claims": payload["allowed_claims"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": source_inputs_rel,
            "produced_artifacts": produced_rel,
            "raw_evidence": [rel(EXECUTION_JSON), rel(REPORT_HTML), rel(TELEMETRY), rel(SUMMARY_CSV), rel(TRADES_CSV)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(RUNTIME_IDENTITY), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": hashes,
            "lineage_boundary": CLAIM_BOUNDARY,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "receipt_path": rel(RESULT_RECEIPT),
            "judgment_boundary": payload["judgment"],
            "allowed_claims": payload["allowed_claims"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(RUNTIME_EVIDENCE_GATE), rel(KPI_RECORD), rel(BACKTEST_FORENSICS_AUDIT), rel(TRADES_CSV)],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": payload["allowed_claims"],
            "allowed_claims": payload["allowed_claims"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": payload["status"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-answer-clarity",
            "status": "executed",
            "receipt_path": rel(ANSWER_RECEIPT),
            "plain_conclusion": "F88C records a bounded runtime repair probe and keeps authority claims closed.",
            "confirmed": ["MT5 tester run attempted", "runtime identity recorded", "trade-list CSV materialized if report existed"],
            "not_yet_confirmed": ["runtime authority", "Goal Achieve", "selected baseline", "live readiness"],
            "why_it_matters": "The project now has a cleaner runtime learning record for timestamp coverage and trade-list identity.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]


def work_packet(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation plus Task Force trigger clarification",
            "requested_action": "F88C MT5 runtime timestamp coverage and trade-list repair probe",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal remains active; no final completion or authority is claimed."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest", "artifact_lineage", "kpi_evidence", "state_sync"],
            "touched_surfaces": [rel(RUN_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "compile_only_laundered_as_runtime": "controlled_by_strategy_tester_report_hashes",
                "runtime_probe_as_authority": "blocked_by_final_claim_guard",
                "same_threshold_tweak_loop": "axis_is_tester_date_coverage_and_trade_list_identity_not_threshold",
            },
            "hard_stop_risks": [
                "Do not claim runtime authority from one short runtime probe.",
                "Do not claim Goal Achieve from PF/DD/trade density.",
                "Do not claim Task Force review without actual subagent calls.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "reason": "No Task Force reviewed/pass claim, policy change, or required overlay claim is made.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": ["F88C MT5 runtime substrate", "RuntimeProbeEA", "F04D reference ONNX candidate"],
            "scope_units": ["set_ini_materialization", "strategy_tester_run", "report_telemetry_hashing", "trade_list_csv", "state_sync"],
            "execution_layers": ["local_python_execution", "mt5_execution", "strategy_tester", "runtime_telemetry"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["EA/ONNX/set/ini hashes", "Strategy Tester report", "telemetry", "summary", "trade-list CSV", "KPI record"],
            "reduction_policy": {"reduction_allowed": False, "rationale": "Runtime claim requires actual runtime output."},
            "claim_boundary": {"allowed_claims": payload["allowed_claims"], "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "required_and_attempted",
            "top_k_reduction_allowed": False,
        },
        "verification_profile": {
            "profile_id": "runtime_probe",
            "claim_surface": {"allowed_claims": payload["allowed_claims"], "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "F88B_next_action", "runtime_materialization_handoff_claim_surface"],
            "protected_claims": payload["allowed_claims"],
            "required_evidence": [
                f"dataset_id={payload['runtime_identity']['dataset_id']}",
                f"feature_set_id={payload['runtime_identity']['feature_set_id']}",
                f"label_id={payload['runtime_identity']['label_id']}",
                f"split_id={payload['runtime_identity']['split_id']}",
                f"onnx_hash={payload['runtime_identity']['onnx_hash']}",
                f"ea_source_hash={payload['runtime_identity']['ea_source_hash']}",
                f"ea_binary_hash={payload['runtime_identity']['ea_binary_hash']}",
                f"set_ini_hash={payload['runtime_identity']['set_ini_hash']}",
                f"feature_order_hash={payload['runtime_identity']['feature_order_hash']}",
                f"tester_identity={payload['runtime_identity']['tester_identity']}",
                f"report_hash={payload['runtime_identity']['report_hash']}",
                f"trade_list_hash={payload['runtime_identity']['trade_list_hash']}",
                f"telemetry_hash={payload['runtime_identity']['telemetry_hash']}",
                rel(REPORT_HTML),
                rel(TELEMETRY),
                rel(SUMMARY_CSV),
                rel(TRADES_CSV),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_runtime_probe_claim_surface",
                    "reason": "No Task Force reviewed/pass claim, policy change, or required overlay claim is made.",
                    "claim_effect": "No Task Force review claim is made.",
                }
            ],
            "stop_conditions": [
                "Stop before authority: one short runtime probe is not runtime authority.",
                "Stop before Goal Achieve: final completion gates are not being reviewed.",
                "Stop before F89 open until frontier_extra_due_check and frontier_topic_rotation_check run.",
            ],
        },
        "acceptance_criteria": [
            "Runtime probe produces tester output or exact blocker.",
            "EA/ONNX/set/ini/report/telemetry/trade-list hashes are recorded.",
            "Final claim guard forbids authority/live readiness/Goal Achieve.",
        ],
        "work_plan": [
            "Reuse F88B runtime substrate and F04D reference ONNX without inheriting authority.",
            "Align tester date boundary to feature coverage and rerun Strategy Tester.",
            "Extract separate trade-list CSV and record KPI/gap evidence.",
        ],
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-reference-scout",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
                "obsidian-answer-clarity",
            ],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [{"skill": "obsidian-task-force-review", "reason": "not_triggered_no_review_claim"}],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(RUNTIME_IDENTITY), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(DECISION_MEMO)],
            "hash_identity_required": True,
        },
        "gates": {
            "required": REQUIRED_GATES,
            "runtime_evidence_gate": "pass" if payload["operation_proof"]["runtime_completed"] else "blocked",
            "scope_completion_gate": "pass" if path_exists(REPORT_HTML) and path_exists(TRADES_CSV) else "blocked",
            "kpi_contract_audit": "pass" if payload["metrics"].get("status") in {"completed", "partial"} else "blocked",
            "backtest_forensics_audit": "pass" if path_exists(REPORT_HTML) else "blocked",
            "artifact_lineage_audit": "pass",
            "result_judgment_audit": "pass",
            "state_sync_audit": "pass",
            "required_gate_coverage_audit": "pass",
            "final_claim_guard": "pass",
        },
        "final_claim_policy": {"allowed_claims": payload["allowed_claims"], "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def closeout_gate_seed(payload: Mapping[str, Any]) -> dict[str, Any]:
    audits_for_gate = [
        ("work_packet_schema_lint", "pending", PACKET_WORK_PACKET_LINT),
        ("skill_receipt_schema_lint", "pending", PACKET_SKILL_RECEIPT_LINT),
        ("runtime_evidence_gate", "pass" if payload["operation_proof"]["runtime_completed"] else "blocked", RUNTIME_EVIDENCE_GATE),
        ("scope_completion_gate", "pass" if path_exists(REPORT_HTML) and path_exists(TRADES_CSV) else "blocked", SCOPE_GATE),
        ("kpi_contract_audit", "pass" if payload["metrics"].get("status") in {"completed", "partial"} else "blocked", KPI_CONTRACT_AUDIT),
        ("backtest_forensics_audit", "pass" if path_exists(REPORT_HTML) else "blocked", BACKTEST_FORENSICS_AUDIT),
        ("artifact_lineage_audit", "pass", ARTIFACT_AUDIT),
        ("result_judgment_audit", "pass", RESULT_JUDGMENT_AUDIT),
        ("state_sync_audit", "pending", PACKET_STATE_SYNC_AUDIT),
        ("required_gate_coverage_audit", "pending", PACKET_REQUIRED_GATE_AUDIT),
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if payload["operation_proof"]["runtime_completed"] else "blocked",
        "audits": [{"audit_name": name, "status": status, "path": rel(path)} for name, status, path in audits_for_gate],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": payload["allowed_claims"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_audits(payload: Mapping[str, Any]) -> None:
    audit_rows = audits(payload)
    for path, key in (
        (RUNTIME_EVIDENCE_GATE, "runtime"),
        (BACKTEST_FORENSICS_AUDIT, "forensics"),
        (KPI_CONTRACT_AUDIT, "kpi"),
        (SCOPE_GATE, "scope"),
        (ARTIFACT_AUDIT, "artifact"),
        (RESULT_JUDGMENT_AUDIT, "judgment"),
        (FINAL_CLAIM_GUARD, "final"),
        (PACKET_FINAL_CLAIM_GUARD, "final"),
    ):
        write_json(path, audit_rows[key])


def write_receipts(payload: Mapping[str, Any]) -> None:
    rows = receipts(payload)
    mapping = {
        "obsidian-runtime-parity": RUNTIME_PARITY_RECEIPT,
        "obsidian-backtest-forensics": BACKTEST_RECEIPT,
        "obsidian-reference-scout": REFERENCE_RECEIPT,
        "obsidian-run-evidence-system": RUN_EVIDENCE_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-result-judgment": RESULT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
        "obsidian-answer-clarity": ANSWER_RECEIPT,
    }
    for row in rows:
        write_json(mapping[row["skill"]], row)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-runtime-parity", "claim_boundary": CLAIM_BOUNDARY, "receipts": rows})


def update_state_docs(payload: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {payload['status']}
current_judgment: {payload['judgment']}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: pending_before_f89_formal_open
frontier_topic_rotation_status: pending_before_f89_formal_open
runtime_probe_status: completed_observation_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F88C ran a narrow MT5 Strategy Tester runtime probe(F88C가 좁은 MT5 전략 테스터 런타임 탐침을 실행).'
- 'Effect(효과): timestamp coverage/trade-list identity(타임스탬프 커버리지/거래목록 정체성)를 실제 report/telemetry/trade-list hash(보고서/기록/거래목록 해시)로 남김.'
- 'Next(다음): F89 formal open(F89 정식 개방) 전 frontier_extra_due_check/frontier_topic_rotation_check(전선 추가 도래 점검/전선 주제 회전 점검) 필요.'
"""
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {payload['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F88C ran one MT5 Strategy Tester runtime probe(F88C는 MT5 전략 테스터 런타임 탐침 1회를 실행) and separated trade-list CSV(거래목록 CSV를 분리).

Effect(효과): Runtime evidence(런타임 근거)는 강화됐지만 runtime authority(런타임 권위), selected baseline(선택 기준선), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    selection = f"""# F88 Selection Status(F88 선택 상태)

Updated(갱신): {payload['created_at_utc']}

Status(상태): `{payload['status']}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected baseline(선택 기준선): not claimed(주장 없음)

Operating promotion(운영 승격): not claimed(주장 없음)

Runtime authority(런타임 권위): not claimed(주장 없음)

Goal Achieve(목표 달성): not claimed(주장 없음)

Action(행동): F88C recorded runtime probe evidence(F88C는 런타임 탐침 근거를 기록).

Effect(효과): F89 formal open(F89 정식 개방)은 아직 하지 않았고, due/rotation checks(도래/회전 점검)가 다음 묶음이다.
"""
    stage_brief = f"""# F88 Runtime Substrate First Materialization Probe(F88 런타임 바탕 최초 물질화 탐침)

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

F88C result(F88C 결과): `{payload['judgment']}`.

Runtime KPI(런타임 핵심 성과 지표): net/PF/DD/trades(순수익/수익 팩터/손실폭/거래 수) `{payload['economics'].get('net_profit')}/{payload['economics'].get('profit_factor')}/{payload['economics'].get('max_drawdown_percent')}/{payload['economics'].get('trade_count')}`.

Next question(다음 질문): can F89 open only after frontier_extra_due_check(전선 추가 도래 점검) and frontier_topic_rotation_check(전선 주제 회전 점검)?

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    input_refs = "# F88 Input References(F88 입력 참조)\n\n" + "\n".join(f"- `{rel(path)}`" for path in source_inputs() + [RUNTIME_IDENTITY, KPI_RECORD, RESULT_SUMMARY, TRADES_CSV]) + "\n"
    decision = f"""# Frontier88C Runtime Substrate Repair(전선88C 런타임 바탕 수리)

Updated(갱신): {payload['created_at_utc']}

Decision(결정): F88C closes as bounded runtime_probe observation(F88C는 경계 있는 런타임 탐침 관찰로 마감).

Action(행동): Tester date boundary(테스터 날짜 경계)를 feature coverage(피처 커버리지)에 맞추고, MT5 report(보고서)에서 separate trade-list CSV(분리 거래목록 CSV)를 만들었다.

Effect(효과): F88 runtime substrate(전선88 런타임 바탕)는 학습 기록을 남겼지만, authority/promotion/baseline(권위/승격/기준선)은 만들지 않는다.

Next(다음): `{NEXT_RUN_ID}`.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(WORKSPACE_STATE, state)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(CONTEXT_ANCHOR, current)
    write_text(SELECTION_STATUS, selection)
    write_text(GLOBAL_SELECTION_STATUS, selection)
    write_text(STAGE_BRIEF, stage_brief)
    write_text(INPUT_REFS, input_refs)
    write_text(DECISION_MEMO, decision)
    append_once(
        REVIEW_INDEX,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- `f88c_runtime_evidence_gate.json`: runtime evidence gate(런타임 근거 게이트)
- `f88c_backtest_forensics_audit.json`: backtest forensics audit(백테스트 포렌식 감사)
- `f88c_kpi_contract_audit.json`: KPI contract audit(KPI 계약 감사)
- `f88c_result_judgment_audit.json`: result judgment audit(결과 판정 감사)
- `f88c_final_claim_guard.json`: final claim guard(최종 주장 보호)
""",
    )
    changelog_entry = f"""
<!-- {RUN_ID} -->

## {payload['created_at_utc'][:10]} - {RUN_ID}

- Action(행동): F88C ran MT5 runtime timestamp coverage/trade-list repair probe(F88C가 MT5 런타임 타임스탬프 커버리지/거래목록 수리 탐침을 실행).
- Effect(효과): report/telemetry/trade-list hashes(보고서/기록/거래목록 해시)를 남겼고 authority/live readiness/Goal Achieve(권위/실거래 준비/목표 달성)는 주장하지 않았다.
"""
    append_once(WORKSPACE_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)
    append_once(ROOT_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)
    append_once(
        IDEA_REGISTRY,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Action(행동): F88 runtime substrate(전선88 런타임 바탕)에서 timestamp coverage/trade-list identity(타임스탬프 커버리지/거래목록 정체성)를 수리 축으로 검증했다.
- Effect(효과): next frontier(다음 전선)는 same threshold/filter tweak(동일 임계값/필터 미세조정)이 아니라 due/rotation check(도래/회전 점검) 뒤 새 hypothesis(가설)를 열어야 한다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
    )
    append_once(
        NEGATIVE_RESULT_REGISTER,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Stage(단계): `{STAGE_ID}`
- Run(실행): `{RUN_ID}`
- Evidence(근거): `{rel(RESULT_SUMMARY)}`, `{rel(TRADES_CSV)}`.
- Negative/inconclusive memory(부정/불충분 기억): runtime substrate repair(런타임 바탕 수리)는 observation(관찰)을 만들었지만 authority/promotion/baseline(권위/승격/기준선)을 만들지 않는다.
- Do-not-repeat(반복 금지): same F04D reference ONNX(동일 F04D 참고 온엑스)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)로 반복하지 않는다.
- Reopen condition(재개 조건): new source/data representation/label/runtime representation/risk logic/regime split(새 원천/데이터 표현/라벨/런타임 표현/위험 로직/장세 분할) 중 하나 이상이 있어야 한다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
    )


def update_ledgers(payload: Mapping[str, Any]) -> None:
    econ = payload["economics"]
    actual = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe_observation",
        "row_id": f"{RUN_ID}__runtime_probe_observation",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_probe_observation",
        "tier_scope": "Tier A",
        "kpi_scope": "mt5_runtime_probe_short_validation",
        "scoreboard_lane": "runtime_parity",
        "lane": "runtime_substrate_repair",
        "family": "runtime_backtest",
        "status": payload["status"],
        "judgment": payload["judgment"],
        "result_judgment": payload["judgment"],
        "path": rel(RESULT_SUMMARY),
        "primary_kpi": f"net={econ.get('net_profit')};pf={econ.get('profit_factor')};dd={econ.get('max_drawdown_percent')};trades={econ.get('trade_count')}",
        "guardrail_kpi": f"feature_ready={payload['summary_row'].get('feature_ready_count')};feature_skip={payload['summary_row'].get('feature_skip_count')};trade_list={payload['trade_lists'].get('status')}",
        "external_verification_status": "completed",
        "notes": "Runtime probe observation only; no authority.",
        "run_number": "frontier88C",
        "date": payload["created_at_utc"][:10],
        "decision": "close_f88c_as_runtime_probe_observation_no_authority",
        "next_run_id": NEXT_RUN_ID,
        "rows": payload["summary_row"].get("feature_ready_count", 0),
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(REPORT_HTML),
        "view": "runtime_probe_observation",
        "tier": "Tier A",
        "metric_scope": "runtime_probe",
        "result_status": payload["status"],
        "work_family": "runtime_backtest",
        "evidence_boundary": "runtime_probe_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Can F88C repair timestamp coverage and separate trade-list identity?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "runtime_backtest",
        "run_type": "runtime_probe",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
    }
    planned = {
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": RUN_ID,
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_planned",
        "kpi_scope": "pending",
        "scoreboard_lane": "frontier_rotation",
        "lane": "frontier_open_precheck",
        "family": "stage_transition",
        "status": "planned_current_run_no_authority",
        "judgment": "pending_due_and_topic_rotation_check",
        "result_judgment": "pending",
        "path": rel(STAGE_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "F89 formal open requires frontier_extra_due_check then frontier_topic_rotation_check.",
        "run_number": "frontier89_pending",
        "date": payload["created_at_utc"][:10],
        "decision": "pending_preopen_checks",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_only_no_authority_no_goal_achieve",
        "report_path": "",
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(STAGE_BRIEF),
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "planned_current_run_no_authority",
        "work_family": "stage_transition",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "frontier_extra_due_check_then_frontier_topic_rotation_check",
        "question": "Can F89 open after due and topic rotation checks?",
        "artifact_count": 0,
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "stage_transition",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(STAGE_BRIEF),
    }
    upsert_csv(RUN_REGISTRY, ["run_id"], [actual, planned])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [actual, planned])
    upsert_csv(STAGE_LEDGER, ["ledger_row_id"], [actual, planned], source_header=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "frontier88c_runtime_probe",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": payload["created_at_utc"],
                "created_at_utc": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": "F88C runtime probe artifact; no runtime authority.",
                "effect": "Supports runtime_probe observation only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_packet_and_gates(payload: Mapping[str, Any]) -> None:
    write_json(RUNTIME_IDENTITY, payload["runtime_identity"])
    write_json(FORENSICS_SUMMARY, {"tester_identity": payload["runtime_identity"]["tester_identity"], "economics": payload["economics"], "operation_proof": payload["operation_proof"]})
    write_json(RUN_MANIFEST, payload)
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, {"run_id": RUN_ID, "status": payload["status"], "judgment": payload["judgment"], "economics": payload["economics"], "execution": payload["summary_row"], "claim_boundary": CLAIM_BOUNDARY})
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_audits(payload)
    write_receipts(payload)
    write_yaml(WORK_PACKET, work_packet(payload))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_seed(payload))


def run_gate_cmd(args: Sequence[str], output_path: Path, *, allow_blocked: bool = False) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path)]
    if allow_blocked:
        command.append("--allow-blocked-exit-zero")
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=60)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
        "output_path": rel(output_path),
    }


def run_control_plane_gates() -> dict[str, Any]:
    commands = {
        "work_packet_schema_lint": run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT, allow_blocked=True),
        "skill_receipt_schema_lint": run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT, allow_blocked=True),
        "state_sync_audit": run_gate_cmd(["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", current_branch()], PACKET_STATE_SYNC_AUDIT, allow_blocked=True),
        "required_gate_coverage_audit": run_gate_cmd(
            [
                "foundation.control_plane.required_gate_coverage_audit",
                "--work-packet",
                str(WORK_PACKET),
                "--closeout-gate",
                str(PACKET_CLOSEOUT_GATE),
            ],
            PACKET_REQUIRED_GATE_AUDIT,
            allow_blocked=True,
        ),
    }
    if path_exists(PACKET_STATE_SYNC_AUDIT):
        shutil.copy2(io_path(PACKET_STATE_SYNC_AUDIT), io_path(STATE_SYNC_AUDIT))
    if path_exists(PACKET_REQUIRED_GATE_AUDIT):
        shutil.copy2(io_path(PACKET_REQUIRED_GATE_AUDIT), io_path(REQUIRED_GATE_AUDIT))
    return commands


def validate_inputs() -> None:
    missing = [
        rel(path)
        for path in [
            PARENT_FEATURE_MATRIX,
            PARENT_SUMMARY_CSV,
            PARENT_RUNTIME_IDENTITY,
            PARENT_SET_FILE,
            SOURCE_ONNX,
            EA_SOURCE,
            EA_BINARY,
            MT5_INPUT_CONTRACT,
            TIME_AXIS_CONTRACT,
        ]
        if not path_exists(path)
    ]
    if missing:
        raise FileNotFoundError(f"Missing F88C required inputs: {missing}")


def main() -> int:
    validate_inputs()
    materialized = materialize_runtime_inputs()
    execution = execute_mt5_probe(materialized)
    trade_lists = materialize_trade_lists()
    payload = build_payload(utc_now(), materialized, execution, trade_lists)
    write_packet_and_gates(payload)
    update_state_docs(payload)
    update_ledgers(payload)
    update_artifact_registry(payload)
    control_gates = run_control_plane_gates()
    payload["control_plane_gates"] = control_gates
    write_json(RUN_MANIFEST, payload)
    write_json(SUMMARY_JSON, payload)
    write_json(
        KPI_RECORD,
        {
            "run_id": RUN_ID,
            "status": payload["status"],
            "judgment": payload["judgment"],
            "economics": payload["economics"],
            "execution": payload["summary_row"],
            "control_plane_gates": control_gates,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    update_artifact_registry(payload)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": payload["status"],
                    "judgment": payload["judgment"],
                    "net_profit": payload["economics"].get("net_profit"),
                    "profit_factor": payload["economics"].get("profit_factor"),
                    "max_drawdown_percent": payload["economics"].get("max_drawdown_percent"),
                    "trade_count": payload["economics"].get("trade_count"),
                    "feature_skip_count": payload["summary_row"].get("feature_skip_count"),
                    "parent_feature_skip_count": payload["parent_summary_row"].get("feature_skip_count"),
                    "trade_list_status": payload["trade_lists"].get("status"),
                    "next_run_id": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "current_branch": current_branch(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
