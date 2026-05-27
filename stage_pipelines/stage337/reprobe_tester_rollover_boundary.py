from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337U"
RUN_ID = "run337U_source_clean_cost_buffer_rebuild_or_tester_rollover_reprobe_v1"
PARENT_RUN_ID = "run337T_source_clean_u42_cost_fragility_or_tester_rollover_probe_v1"
SOURCE_RUN_ID = "run337Q_review_runtime_data_and_feature_source_repair_probe_v1"
NEXT_RUN_ID = "run337V_cost_buffer_rebuild_and_source_policy_repair_design_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337U_tester_rollover_reprobe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_REPAIRED = "completed_stage337U_tester_rollover_reprobe_reached_feature_last_no_forward_decision"
STATUS_PARTIAL = "completed_stage337U_tester_rollover_reprobe_gap_remains_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337U_tester_rollover_reprobe_materialized_only_no_forward_decision"
JUDGMENT_REPAIRED = "tester_rollover_reaches_feature_last_but_u42_cost_fragility_blocks_onnx_ready_claim"
JUDGMENT_PARTIAL = "tester_rollover_gap_remains_u42_cost_fragility_already_blocks_onnx_ready_claim"
JUDGMENT_MATERIALIZED = "tester_rollover_reprobe_inputs_materialized_execution_pending"
DECISION_REPAIRED = "stage337U_open_run337V_cost_buffer_rebuild_and_source_policy_repair_design_no_selection"
DECISION_PARTIAL = "stage337U_open_run337V_cost_buffer_rebuild_and_source_policy_repair_design_no_selection"
DECISION_MATERIALIZED = "stage337U_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Q_DIR = STAGE_DIR / "02_runs" / "run337Q"
RUN337Q_ATTEMPTS = RUN337Q_DIR / "boundary_repair_handoff_attempts.json"
RUN337Q_RUNTIME = RUN337Q_DIR / "fresh_mt5_runtime_probe_result.csv"
RUN337Q_GAP = RUN337Q_DIR / "tester_feature_last_gap_reprobe.csv"
RUN337Q_FINAL = RUN337Q_DIR / "final_tester_date_boundary_repair_review_decision.json"
RUN337T_REPORT = STAGE_DIR / "03_reviews" / "run337T_u42_source_clean_cost_fragility_review.md"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337U_tester_rollover_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337U_tester_rollover_reprobe.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DEFAULT_PORTABLE_ROOT = Path(r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
LOG_DATE = TODAY.replace("-", "")
TESTER_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "logs" / f"{LOG_DATE}.log"
TESTER_AGENT_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "Agent-127.0.0.1-3000" / "logs" / f"{LOG_DATE}.log"
TERMINAL_LOG = DEFAULT_PORTABLE_ROOT / "Logs" / f"{LOG_DATE}.log"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337U_tester_rollover_reprobe"
ATTEMPT_NAME = "u42_plain_rf"
M5_SECONDS = 300


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def disk_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) < 240:
        return resolved
    return io_path(path)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    return str(value)


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    disk_path(path.parent).mkdir(parents=True, exist_ok=True)
    target = disk_path(path)
    if path.name == "artifact_registry.csv":
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
        return path
    tmp = target.with_name(target.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, target)
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    write_csv(path, columns, rows)
    return path


def append_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]]) -> Path:
    if not rows:
        return path
    existing: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            existing = [dict(item) for item in reader]
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    existing.extend({column: csv_value(row.get(column, "")) for column in columns} for row in rows)
    write_csv(path, columns, existing)
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337U tester rollover reprobe for frozen source-clean u42.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def configure_probe_modules() -> None:
    qprobe.TODAY = TODAY
    qprobe.STAGE_ID = STAGE_ID
    qprobe.RUN_NUMBER = RUN_NUMBER
    qprobe.RUN_ID = RUN_ID
    qprobe.PARENT_RUN_ID = PARENT_RUN_ID
    qprobe.NEXT_RUN_ID = NEXT_RUN_ID
    qprobe.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    qprobe.STAGE_DIR = STAGE_DIR
    qprobe.RUN_DIR = RUN_DIR
    qprobe.MT5_DIR = MT5_DIR
    qprobe.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    qprobe.MODEL_COPY_DIR = MODEL_COPY_DIR
    qprobe.TELEMETRY_DIR = TELEMETRY_DIR
    qprobe.REVIEWS_DIR = REVIEWS_DIR
    qprobe.REPORT_PATH = REPORT_PATH
    qprobe.DECISION_DOC = DECISION_DOC
    qprobe.SELECTED_STATUS = SELECTED_STATUS
    qprobe.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
    qprobe.DEFAULT_TERMINAL = DEFAULT_TERMINAL
    qprobe.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
    qprobe.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
    qprobe.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
    qprobe.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
    qprobe.TESTER_LOG = TESTER_LOG
    qprobe.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    qprobe.TERMINAL_LOG = TERMINAL_LOG
    qprobe.COMMON_ROOT = COMMON_ROOT
    qprobe.ATTEMPT_NAMES = (ATTEMPT_NAME,)
    qprobe.configure_base()


def source_attempts() -> list[dict[str, Any]]:
    rows = read_json(RUN337Q_ATTEMPTS)
    selected: list[dict[str, Any]] = []
    for row in rows:
        if row.get("attempt_name") != ATTEMPT_NAME:
            continue
        copied = dict(row)
        copied["model_copy"] = {"source": row.get("model_local_path", "")}
        copied["feature_export"] = {"path": row.get("feature_local_path", "")}
        copied["source_run_id"] = SOURCE_RUN_ID
        copied["attempt_role"] = "stage337U_tester_rollover_reprobe_same_frozen_u42_model_feature_threshold_risk"
        selected.append(copied)
    if len(selected) != 1:
        raise RuntimeError(f"expected one {ATTEMPT_NAME} source attempt from {RUN337Q_ATTEMPTS}, got {len(selected)}")
    return selected


def target_tester_to_date(feature_latest: pd.Timestamp) -> str:
    return (feature_latest.date() + timedelta(days=3)).strftime("%Y.%m.%d")


def rewrite_attempt_to_rollover(attempt: dict[str, Any], tester_to_date: str) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["ToDate"] = tester_to_date
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = base.materialize_ini_file(tester, ini_path)
    attempt["to_date"] = tester_to_date
    attempt["attempt_role"] = "stage337U_tester_rollover_reprobe_same_frozen_u42_model_feature_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337U_{attempt['artifact_slug']}"
    attempt["source_run_id"] = SOURCE_RUN_ID
    attempt["repair_contract"] = "tester ToDate rollover reprobe only; same ONNX, feature order, threshold, risk, lot, and feature CSV"
    attempt["signal_policy"] = "same frozen ONNX and runtime settings; ToDate rollover reprobe only"
    return attempt


def sanitize_proxy_rows(rows: Sequence[Mapping[str, Any]], *, source_label: str) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["proxy_source"] = source_label
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_diff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["mt5_source"] = "stage337U_tester_rollover_reprobe_tier_a_telemetry_summary"
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def classify(runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    if completed == len(runtime_rows) and reached == len(gap_rows) and matches == len(aligned_diff_rows) and aligned_diff_rows:
        return STATUS_REPAIRED, JUDGMENT_REPAIRED, DECISION_REPAIRED
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL


def gate_rows(runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], raw_diff_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]], boundary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        {
            "gate_name": "run337Q_u42_source_loaded",
            "status": "covered",
            "evidence_path": rel(RUN337Q_ATTEMPTS),
            "effect": "run337Q(337Q 실행)의 u42 frozen handoff(고정 인계)를 그대로 읽어 새 run337U(337U 실행) 폴더로 복사했다.",
        },
        {
            "gate_name": "no_retune_guard",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "rollover_reprobe_handoff_manifest.csv"),
            "effect": "ONNX(온엑스), feature order(피처 순서), threshold(임계값), risk/lot(위험/랏)은 유지하고 tester ToDate(테스터 종료일)만 바꿨다.",
        },
        {
            "gate_name": "mt5_tester_rollover_reprobe",
            "status": "covered" if completed == len(runtime_rows) else "covered_partial",
            "evidence_path": rel(RUN_DIR / "frozen_forward_mt5_result.csv"),
            "effect": f"MT5(메타트레이더5) Strategy Tester(전략 테스터)를 단일 u42 경로로 실행했다; completed={completed}/{len(runtime_rows)}.",
        },
        {
            "gate_name": "tester_reached_feature_last",
            "status": "covered_repaired" if reached == len(gap_rows) else "covered_blocker",
            "evidence_path": rel(RUN_DIR / "tester_rollover_feature_last_gap.csv"),
            "effect": f"테스터 관측 마지막 봉이 feature_last(피처 마지막 시점)에 닿았는지 확인했다; reached={reached}/{len(gap_rows)}.",
        },
        {
            "gate_name": "proxy_mt5_difference_recorded",
            "status": "covered" if aligned_matches == len(aligned_diff_rows) and aligned_diff_rows else "covered_partial",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": f"proxy expected(프록시 예상값)와 MT5 observed(관측값)를 비교했다; raw={raw_matches}/{len(raw_diff_rows)}, aligned={aligned_matches}/{len(aligned_diff_rows)}.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "final_tester_rollover_reprobe_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않았다.",
        },
    ]


def copy_reports_to_required_names(runtime_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    copied: list[Path] = []
    first_report = next((row.get("report_path") for row in runtime_rows if row.get("report_path")), "")
    if first_report:
        source = Path(str(first_report))
        if path_exists(source):
            for name in ("mt5_strategy_tester_report.html", "frozen_forward_mt5_report.html"):
                target = RUN_DIR / name
                shutil.copy2(io_path(source), io_path(target))
                copied.append(target)
    first_telemetry = next((TELEMETRY_DIR / f"{row.get('attempt_name')}_telemetry.csv" for row in runtime_rows if path_exists(TELEMETRY_DIR / f"{row.get('attempt_name')}_telemetry.csv")), None)
    if first_telemetry:
        target = RUN_DIR / "mt5_terminal_telemetry.csv"
        shutil.copy2(io_path(first_telemetry), io_path(target))
        copied.append(target)
    return copied


def build_receipts(status: str, judgment: str, decision: str, runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]], tester_to_date: str, feature_latest: pd.Timestamp) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "run337Q u42 feature CSV and fresh run337U MT5 tester output",
                "time_axis": "MT5 bar_time and feature bar_time_server use UTC-like server timestamp strings; tester ToDate rollover separately audited",
                "sample_scope": "US100 M5 forward runtime probe after prior OOS end, u42 source-clean no-external feature set only",
                "feature_label_boundary": "no model training, no threshold retune, no future feature fill; ToDate rollover probes tester inclusion only",
                "leakage_risk": "post-hoc selecting only u42 is avoided by treating it as source-clean control and not candidate selection",
                "integrity_judgment": "usable_for_runtime_probe_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "research_path": "stage_pipelines/stage337/reprobe_tester_rollover_boundary.py",
                "runtime_path": rel(RUN_DIR / "rollover_reprobe_handoff_attempts.json"),
                "shared_contract": "same ONNX, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, and runtime handoff; only tester ToDate widened",
                "runtime_completed": f"{completed}/{len(runtime_rows)}",
                "tester_reached_feature_last": f"{reached}/{len(gap_rows)}",
                "timestamp_aligned_signal_parity": f"{matches}/{len(aligned_diff_rows)}",
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": "FPMarketsSC-Live US100 M5 real-tick Strategy Tester tester-rollover reprobe",
                "requested_tester_to_date": tester_to_date,
                "feature_latest_timestamp": feature_latest.isoformat().replace("+00:00", "Z"),
                "report_identity": [row.get("report_path", "") for row in runtime_rows],
                "trade_evidence": [{key: row.get(key, "") for key in ("attempt_name", "net_profit", "profit_factor", "trade_count", "max_drawdown_amount")} for row in runtime_rows],
                "cost_assumptions": "frozen source set values inherited from run337Q u42 handoff; no spread, slippage, lot, or risk optimization",
                "backtest_judgment": "usable_with_boundary_for_runtime_probe_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "result_subject": "source-clean u42 tester rollover reprobe",
                "evidence_available": [rel(RUN_DIR / "frozen_forward_mt5_result.csv"), rel(RUN_DIR / "tester_rollover_feature_last_gap.csv"), rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv")],
                "evidence_missing": "forward pass/fail still blocked by tester gap if unrepaired and by u42 cost fragility even if repaired",
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_condition": "cost-buffer rebuild and source-policy repair must produce a robust ONNX without lookahead or proxy-only authority",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "source_inputs": [rel(RUN337Q_ATTEMPTS), rel(RUN337T_REPORT)],
                "lineage_judgment": "connected_with_boundary",
                "availability": "tracked",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def write_report(status: str, judgment: str, decision: str, latest_probe: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], raw_diff_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]], tester_to_date: str) -> Path:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    lines = [
        "# Stage337U Tester Rollover Reprobe(337U 테스터 이월 재탐침)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- requested ToDate(요청 종료일): `{tester_to_date}`",
        f"- API latest US100 close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`",
        f"- MT5 completed(MT5 완료): `{completed}/{len(runtime_rows)}`",
        f"- tester reached feature last(테스터 피처 끝 도달): `{reached}/{len(gap_rows)}`",
        f"- raw proxy parity(원시 프록시 동등성): `{raw_matches}/{len(raw_diff_rows)}`",
        f"- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `{aligned_matches}/{len(aligned_diff_rows)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Runtime Metrics(런타임 지표)",
        "",
        "| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        status_label = f"{row.get('tester_status', '')}/{row.get('runtime_status', '')}/{row.get('report_status', '')}"
        lines.append(f"| `{row.get('attempt_name', '')}` | `{status_label}` | `{row.get('net_profit', '')}` | `{row.get('profit_factor', '')}` | `{row.get('trade_count', '')}` | `{row.get('max_drawdown_amount', '')}` |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run337U(337U 실행)는 새 후보 개발이 아니라 tester rollover(테스터 이월) 재탐침이다. ONNX(온엑스), feature order(피처 순서), D/B surface(D/B 표면), threshold(임계값), risk/lot(위험/랏), ATR SL/TP(ATR 손절/익절)는 바꾸지 않았다.",
            "",
            "효과(effect, 효과): 테스터가 feature_last(피처 마지막 시점)에 닿는지 확인하되, u42의 비용 취약성 때문에 ONNX-ready(온엑스 준비)나 Forward Passed(전진 통과)는 주장하지 않는다.",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(status: str, judgment: str, decision: str, latest_probe: Mapping[str, Any], tester_to_date: str, reached: int, total: int) -> Path:
    text = f"""# Stage337U Decision(337U 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- requested ToDate(요청 종료일): `{tester_to_date}`
- API latest US100 close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`
- tester reached feature last(테스터 피처 끝 도달): `{reached}/{total}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337U(337U 실행)는 u42 source-clean control(원천 깨끗한 대조군)의 tester rollover(테스터 이월)만 재확인한다. 결과는 다음 cost-buffer rebuild(비용 버퍼 재구성)와 source-policy repair(원천 정책 수리)의 입력이며 선택이나 운영 주장이 아니다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(status: str, decision: str, runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], aligned_diff_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    aligned = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- u42_source_clean_control(원천 깨끗한 대조군): `kept_as_failure_memory_control_not_onnx_ready`
- source_policy_repair_required(원천 정책 수리 필요): `m48_plain_rf;c56_plain_rf`
- tester_rollover_probe_runtime(테스터 이월 탐침 런타임): `{completed}/{len(runtime_rows)} completed(완료)`
- tester_reached_feature_last(테스터 피처 끝 도달): `{reached}/{len(gap_rows)}`
- timestamp_aligned_proxy_parity(시점 맞춤 프록시 동등성): `{aligned}/{len(aligned_diff_rows)}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): u42는 tester rollover(테스터 이월)를 재탐침했지만 비용 취약성 때문에 ONNX-ready(온엑스 준비)가 아니며, 다음은 cost-buffer rebuild(비용 버퍼 재구성)와 source-policy repair(원천 정책 수리)를 설계한다.
"""
    write_md(SELECTED_STATUS, selection_text)

    focus_line = (
        "- >-\n"
        f"  Stage337 run337U focus complete: Stage337(337단계) run337U(337U 실행)는 `{status}`로 tester rollover reprobe(테스터 이월 재탐침)를 완료했다. "
        f"Effect(효과): u42 source-clean control(원천 깨끗한 대조군)을 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행하고 tester reached feature last(테스터 피처 끝 도달) `{reached}/{len(gap_rows)}`, timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{aligned}/{len(aligned_diff_rows)}`를 기록했으며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[idx] = f"current_run_id: {NEXT_RUN_ID}"
                break
        text = "\n".join(lines) + "\n"
        if "Stage337 run337U focus complete" in text:
            text = re.sub(r"- >-\n  Stage337 run337U focus complete:.*?(?=\n- >-|\Z)", focus_line.rstrip(), text, count=1, flags=re.S)
        else:
            lines = text.splitlines()
            try:
                idx = lines.index("current_focus:")
                lines.insert(idx + 1, focus_line.rstrip())
            except ValueError:
                lines.extend(["current_focus:", focus_line.rstrip()])
            text = "\n".join(lines) + "\n"
        write_text_preserving(WORKSPACE_STATE, text, had_bom)

    current_entry = f"""
## Stage337 run337U(337U 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): tester rollover reprobe(테스터 이월 재탐침)를 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행했고, tester reached feature last(테스터 피처 끝 도달) `{reached}/{len(gap_rows)}`, timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{aligned}/{len(aligned_diff_rows)}`를 기록했다.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337U(337U 실행)" in text:
            text = re.sub(r"## Stage337 run337U\(337U 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=re.S)
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n\n" + current_entry.strip() + "\n", had_bom)

    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        line = f"\n- {TODAY}: Stage337 run337U(337U 실행) `{status}`. Effect(효과): tester rollover reprobe(테스터 이월 재탐침)를 MT5(메타트레이더5) `{completed}/{len(runtime_rows)}`로 실행했고 Forward/Goal(전진/목표) 주장은 없음.\n"
        if "Stage337 run337U(337U 실행)" in text:
            text = re.sub(r"\n- [^\n]*Stage337 run337U\(337U 실행\)[^\n]*", line.rstrip(), text, count=1)
            write_text_preserving(CHANGELOG, text.rstrip() + "\n", had_bom)
        else:
            write_text_preserving(CHANGELOG, text.rstrip() + line, had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "tester_rollover_reprobe",
                "lane": "runtime_parity_repair",
                "status": status,
                "judgment": judgment,
                "primary_report": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"decision={decision};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "run_key": f"{RUN_ID}__tester_rollover_reprobe",
                "ledger_row_id": f"{RUN_ID}__tester_rollover_reprobe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "tester_rollover_reprobe",
                "work_family": "runtime_parity_repair",
                "question": "can a stronger ToDate rollover make source-clean u42 tester reach feature_last without retuning",
                "metric_scope": "runtime_boundary_reprobe_no_forward_decision",
                "evidence_scope": "MT5 tester logs telemetry proxy parity and u42 cost failure memory",
                "kpi_scope": "diagnostic_runtime_probe_not_forward_kpi",
                "status": status,
                "judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
                "primary_artifact": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": decision,
            },
        ),
    ]
    generated = now_utc()
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in artifact_paths:
        path_key = str(path)
        if path_key in seen:
            continue
        seen.add(path_key)
        if not path_exists(path) or not io_path(path).is_file():
            continue
        suffix = path.suffix.lower()
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".ini", ".set", ".py"} else sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    artifacts.append(append_csv_rows(ARTIFACT_REGISTRY, rows))
    return artifacts


def metric_summary(runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        trades = float(row.get("trade_count") or 0.0)
        net = float(row.get("net_profit") or 0.0)
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "runtime_status": row.get("runtime_status", ""),
                "report_status": row.get("report_status", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "expectancy": row.get("expectancy", ""),
                "recovery_factor": row.get("recovery_factor", ""),
                "max_drawdown_amount": row.get("max_drawdown_amount", ""),
                "long_trade_count": row.get("long_trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "lot_normalized_net_per_trade": (net / trades) if trades else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def main() -> int:
    args = parse_args()
    configure_probe_modules()
    generated_at_utc = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)
    FEATURE_COPY_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_COPY_DIR.mkdir(parents=True, exist_ok=True)
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

    parent_runtime_rows = read_csv(RUN337Q_RUNTIME) if path_exists(RUN337Q_RUNTIME) else []
    parent_gap_rows = read_csv(RUN337Q_GAP) if path_exists(RUN337Q_GAP) else []
    latest_probe = qprobe.latest_us100_close(Path(args.terminal_path))
    prepared = source_attempts()
    feature_rows = qprobe.feature_last_rows(prepared)
    feature_latest = max((pd.to_datetime(row["feature_last_timestamp"], utc=True) for row in feature_rows if row.get("feature_last_timestamp")), default=pd.Timestamp("1970-01-01", tz=UTC))
    tester_to_date = target_tester_to_date(feature_latest)

    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, Path(args.common_files_root))
    attempts = [rewrite_attempt_to_rollover(dict(attempt), tester_to_date) for attempt in attempts]
    proxy_rows = sanitize_proxy_rows(base.build_proxy_signal_expected_rows(attempts), source_label="stage337U_python_onnx_inference_from_run337Q_u42_features")
    terminal_recovery = {"status": "skipped_materialize_only"} if args.materialize_only else qprobe.stop_target_terminal_if_running(Path(args.terminal_path))
    before_offsets = qprobe.log_offsets([TESTER_LOG, TESTER_AGENT_LOG, TERMINAL_LOG])

    if args.materialize_only:
        execution_result: dict[str, Any] = {
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "terminal_extra_args": ["/portable"],
        }
    else:
        execution_result = base.execute_attempts(
            attempts,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            terminal_data_root=Path(args.terminal_data_root),
            timeout_seconds=args.timeout_seconds,
            wait_timeout_seconds=args.wait_timeout_seconds,
            materialize_only=False,
        )

    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    boundary_rows = qprobe.tester_boundary_rows(before_offsets, attempts, tester_to_date)
    base.copy_runtime_outputs(Path(args.common_files_root), attempts)
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, Path(args.common_files_root), latest_probe)
    raw_diff_rows = sanitize_diff_rows(base.build_signal_difference_rows(proxy_rows, runtime_rows))
    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in gap_rows}
    aligned_proxy_rows = sanitize_proxy_rows(qprobe.build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt), source_label="stage337U_timestamp_aligned_python_onnx_inference")
    aligned_diff_rows = sanitize_diff_rows(base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows))
    metrics = metric_summary(runtime_rows)
    status, judgment, decision = classify(runtime_rows, gap_rows, aligned_diff_rows, bool(args.materialize_only))
    gates = gate_rows(runtime_rows, gap_rows, raw_diff_rows, aligned_diff_rows, boundary_rows)

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "parent_run337Q_final_decision_snapshot.json", read_json(RUN337Q_FINAL) if path_exists(RUN337Q_FINAL) else {"status": "missing"}),
        write_csv(RUN_DIR / "parent_run337Q_gap_snapshot.csv", list(parent_gap_rows[0].keys()) if parent_gap_rows else ["status"], parent_gap_rows or [{"status": "missing"}]),
        write_csv(RUN_DIR / "parent_run337Q_runtime_snapshot.csv", list(parent_runtime_rows[0].keys()) if parent_runtime_rows else ["status"], parent_runtime_rows or [{"status": "missing"}]),
        write_json(RUN_DIR / "fresh_us100_api_probe.json", latest_probe),
        write_json(RUN_DIR / "terminal_process_recovery.json", terminal_recovery),
        write_csv(
            RUN_DIR / "feature_last_timestamp_audit.csv",
            ["attempt_name", "feature_set_id", "feature_rows", "feature_first_timestamp", "feature_last_timestamp", "feature_csv_path", "feature_csv_sha256", "claim_boundary"],
            feature_rows,
        ),
        write_csv(
            RUN_DIR / "tester_rollover_log_audit.csv",
            ["attempt_name", "requested_to_date", "log_test_from", "log_test_to", "history_sync_from", "history_sync_to", "tick_sync_from", "tick_sync_to", "generated_ticks", "generated_bars", "source", "effect", "claim_boundary"],
            boundary_rows,
        ),
        write_json(RUN_DIR / "rollover_reprobe_handoff_attempts.json", attempts),
        write_csv(
            RUN_DIR / "rollover_reprobe_handoff_manifest.csv",
            [
                "attempt_name",
                "artifact_slug",
                "source_set_path",
                "source_ini_path",
                "new_set_path",
                "new_ini_path",
                "source_model_path",
                "new_model_path",
                "source_feature_path",
                "new_feature_path",
                "model_common_path",
                "feature_common_path",
                "telemetry_common_path",
                "summary_common_path",
                "threshold_keys_unchanged",
                "risk_lot_keys_unchanged",
                "allowed_identity_keys_changed",
                "source_set_sha256",
                "new_set_sha256",
                "source_ini_sha256",
                "new_ini_sha256",
                "model_sha256",
                "feature_sha256",
                "materialization_status",
                "claim_boundary",
            ],
            handoff_rows,
        ),
        write_json(RUN_DIR / "runtime_execution_result.json", execution_result),
        write_csv(
            RUN_DIR / "frozen_forward_mt5_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "tester_status",
                "runtime_status",
                "report_status",
                "returncode",
                "blocker",
                "feature_ready_count",
                "model_ok_count",
                "tier_a_long_count",
                "tier_a_short_count",
                "tier_a_flat_count",
                "long_count",
                "short_count",
                "flat_count",
                "no_tier_count",
                "last_skip_reason",
                "order_attempt_count",
                "order_fill_count",
                "net_profit",
                "profit_factor",
                "trade_count",
                "expectancy",
                "recovery_factor",
                "max_drawdown_amount",
                "short_trade_count",
                "long_trade_count",
                "common_summary_path",
                "common_telemetry_path",
                "report_name",
                "report_path",
                "claim_boundary",
            ],
            runtime_rows,
        ),
        write_csv(
            RUN_DIR / "tester_rollover_feature_last_gap.csv",
            ["attempt_name", "feature_set_id", "runtime_status", "report_status", "api_latest_us100_close_utc", "feature_last_timestamp", "tester_last_observed_bar_time", "tester_to_feature_last_gap_minutes", "tester_to_api_latest_gap_minutes", "telemetry_rows", "last_skip_reason", "gap_status", "claim_boundary"],
            gap_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_expected_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "expected_feature_ready_count",
                "expected_model_ok_count",
                "expected_short_count",
                "expected_long_count",
                "expected_flat_count",
                "expected_signal_count",
                "expected_signal_rate",
                "expected_long_share",
                "mean_p_short",
                "mean_p_flat",
                "mean_p_long",
                "mean_probability_margin",
                "max_probability_row_sum_abs_error",
                "feature_order_hash",
                "feature_csv_sha256",
                "model_sha256",
                "threshold_policy",
                "proxy_source",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_aligned_proxy_expected_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "expected_feature_ready_count",
                "expected_model_ok_count",
                "expected_short_count",
                "expected_long_count",
                "expected_flat_count",
                "expected_signal_count",
                "expected_signal_rate",
                "expected_long_share",
                "mean_p_short",
                "mean_p_flat",
                "mean_p_long",
                "mean_probability_margin",
                "max_probability_row_sum_abs_error",
                "feature_order_hash",
                "feature_csv_sha256",
                "model_sha256",
                "threshold_policy",
                "proxy_source",
                "proxy_cutoff_utc",
                "proxy_row_scope",
                "full_feature_rows",
                "timestamp_aligned_feature_rows",
                "claim_boundary",
            ],
            aligned_proxy_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            raw_diff_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            aligned_diff_rows,
        ),
        write_csv(
            RUN_DIR / "lot_normalized_report.csv",
            ["attempt_name", "feature_set_id", "runtime_status", "report_status", "net_profit", "profit_factor", "trade_count", "expectancy", "recovery_factor", "max_drawdown_amount", "long_trade_count", "short_trade_count", "lot_normalized_net_per_trade", "claim_boundary"],
            metrics,
        ),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(
            RUN_DIR / "tester_settings_identity.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "requested_tester_to_date": tester_to_date,
                "feature_latest_timestamp": feature_latest.isoformat().replace("+00:00", "Z"),
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "queued_attempts": [attempt["attempt_name"] for attempt in attempts],
                "model_training": "forbidden_not_performed",
                "threshold_retuning": "forbidden_not_performed",
                "lot_optimization": "forbidden_not_performed",
                "only_change": "tester_to_date_rollover_reprobe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifact_paths.extend(materialized_artifacts)
    artifact_paths.extend(base.copy_runtime_outputs(Path(args.common_files_root), attempts))
    artifact_paths.extend(copy_reports_to_required_names(runtime_rows))
    artifact_paths.extend(build_receipts(status, judgment, decision, runtime_rows, gap_rows, aligned_diff_rows, tester_to_date, feature_latest))
    artifact_paths.append(write_report(status, judgment, decision, latest_probe, runtime_rows, gap_rows, raw_diff_rows, aligned_diff_rows, tester_to_date))

    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    artifact_paths.append(write_decision_doc(status, judgment, decision, latest_probe, tester_to_date, reached, len(gap_rows)))
    artifact_paths.extend(update_status_docs(status, decision, runtime_rows, gap_rows, aligned_diff_rows))

    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "api_latest_us100_close_utc": latest_probe.get("last_close_utc", ""),
        "feature_latest_timestamp": feature_latest.isoformat().replace("+00:00", "Z"),
        "requested_tester_to_date": tester_to_date,
        "runtime_completed": completed,
        "runtime_total": len(runtime_rows),
        "tester_reached_feature_last": reached,
        "tester_gap_total": len(gap_rows),
        "signal_parity_matched_rows": raw_matches,
        "signal_parity_total_rows": len(raw_diff_rows),
        "timestamp_aligned_signal_parity_matched_rows": aligned_matches,
        "timestamp_aligned_signal_parity_total_rows": len(aligned_diff_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_tester_rollover_reprobe_decision.json", final_decision))
    artifact_paths.extend(update_registers(status, judgment, decision, [*artifact_paths, Path(__file__)]))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "command": "python stage_pipelines/stage337/reprobe_tester_rollover_boundary.py",
                "materialize_only": bool(args.materialize_only),
                "artifacts": [rel(path) for path in artifact_paths if path_exists(path)],
            },
        )
    )
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
