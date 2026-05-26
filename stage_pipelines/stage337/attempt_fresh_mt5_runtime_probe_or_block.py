from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage336 import materialize_live_safe_feature_handoff_repair as repair  # noqa: E402
from stage_pipelines.stage336 import attempt_fresh_mt5_runtime_probe_or_block as run336k  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337N"
RUN_ID = "run337N_attempt_fresh_mt5_runtime_probe_or_block_v1"
PARENT_RUN_ID = "run337M_review_proxy_expected_fresh_mt5_probe_inputs_v1"
NEXT_RUN_ID = "run337O_review_fresh_mt5_runtime_probe_and_core56_repair_or_attribution_queue_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337N_fresh_mt5_runtime_probe_attempt_same_onnx_same_feature_order_"
    "same_threshold_same_risk_same_lot_live_safe_handoff_refresh_only_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_COMPLETED_PARTIAL = "completed_stage337N_latest_repaired_fresh_mt5_runtime_probe_partial_core56_block_no_forward_decision"
STATUS_PARTIAL = "completed_stage337N_fresh_mt5_runtime_probe_attempt_partial_or_block_no_forward_decision"
STATUS_MATERIALIZED_ONLY = "completed_stage337N_fresh_mt5_runtime_probe_inputs_materialized_execution_pending_no_forward_decision"
JUDGMENT_COMPLETED_PARTIAL = "m48_u42_latest_handoff_runtime_probe_usable_for_attribution_core56_refresh_blocked"
JUDGMENT_PARTIAL = "fresh_mt5_runtime_probe_attempt_has_runtime_or_feature_gap_requires_repair"
DECISION_COMPLETED_PARTIAL = "stage337N_m48_u42_runtime_probe_ready_for_stage337O_attribution_core56_refresh_repair_required_no_selection"
DECISION_PARTIAL = "stage337N_runtime_probe_needs_repair_before_forward_or_selection_judgment"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
REPAIRED_SOURCE_DIR = RUN_DIR / "repaired_feature_sources"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
RUN337M_DIR = STAGE_DIR / "02_runs" / "run337M"
RUN336_STAGE_DIR = ROOT / "stages" / "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN336K_ATTEMPTS = RUN336_STAGE_DIR / "02_runs" / "run336K" / "independent_handoff_attempts.json"
REPORT_PATH = REVIEWS_DIR / "run337N_fresh_mt5_runtime_probe_or_block.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337N_fresh_mt5_runtime_probe_or_block.md"
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
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337N_fresh_mt5_runtime_probe"

ATTEMPT_NAMES = ("m48_bal_rf", "m48_plain_rf", "u42_bal_rf", "u42_plain_rf")
CORE56_ATTEMPT_ID = "core56_refresh_candidate_fresh_mt5_runtime_probe_attempt"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


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
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    tmp = io_path(path).with_name(io_path(path).name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, io_path(path))
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
    io_path(path).write_text(text, encoding=encoding)
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
    columns: list[str] = []
    existing: list[dict[str, str]] = []
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
    parser = argparse.ArgumentParser(description="Stage337N fresh MT5 runtime probe attempt or blocker.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--attempt-filter", default="", help="Comma-separated subset of m48/u42 attempts.")
    parser.add_argument("--end-utc", default="", help="Optional inclusive latest data probe end in ISO UTC.")
    return parser.parse_args()


def resolve_probe_end_utc(value: str, terminal_path: Path) -> datetime:
    if value.strip():
        return run336k.parse_optional_utc(value)
    try:
        run336k.init_mt5(terminal_path)
        try:
            run336k.mt5_api.symbol_select("US100", True)
            rates = run336k.mt5_api.copy_rates_from_pos("US100", run336k.mt5_api.TIMEFRAME_M5, 0, 20)
            if rates is not None and len(rates):
                last_open = datetime.fromtimestamp(int(rates[-1]["time"]), tz=UTC)
                return last_open + timedelta(seconds=run336k.M5_SECONDS)
        finally:
            run336k.mt5_api.shutdown()
    except Exception:
        return run336k.parse_optional_utc("")
    return run336k.parse_optional_utc("")


def configure_repair_modules() -> None:
    for name, value in {
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "STATUS_COMPLETED": STATUS_COMPLETED_PARTIAL,
        "STATUS_PARTIAL": STATUS_PARTIAL,
        "STATUS_MATERIALIZED_ONLY": STATUS_MATERIALIZED_ONLY,
        "JUDGMENT_COMPLETED": JUDGMENT_COMPLETED_PARTIAL,
        "JUDGMENT_PARTIAL": JUDGMENT_PARTIAL,
        "DECISION_COMPLETED": DECISION_COMPLETED_PARTIAL,
        "DECISION_PARTIAL": DECISION_PARTIAL,
        "STAGE_DIR": STAGE_DIR,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "FEATURE_COPY_DIR": FEATURE_COPY_DIR,
        "MODEL_COPY_DIR": MODEL_COPY_DIR,
        "REPAIRED_SOURCE_DIR": REPAIRED_SOURCE_DIR,
        "TELEMETRY_DIR": TELEMETRY_DIR,
        "RAW_REFRESH_DIR": RAW_REFRESH_DIR,
        "REVIEWS_DIR": REVIEWS_DIR,
        "SELECTED_STATUS": SELECTED_STATUS,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "STAGE_LEDGER": STAGE_LEDGER,
        "RUN_REGISTRY": RUN_REGISTRY,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_STATE": CURRENT_STATE,
        "CHANGELOG": CHANGELOG,
        "DEFAULT_PORTABLE_ROOT": DEFAULT_PORTABLE_ROOT,
        "DEFAULT_TERMINAL": DEFAULT_TERMINAL,
        "DEFAULT_METAEDITOR": DEFAULT_METAEDITOR,
        "DEFAULT_COMMON_FILES": DEFAULT_COMMON_FILES,
        "DEFAULT_TESTER_PROFILE_ROOT": DEFAULT_TESTER_PROFILE_ROOT,
        "DEFAULT_TERMINAL_DATA_ROOT": DEFAULT_TERMINAL_DATA_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
    }.items():
        setattr(repair, name, value)
    repair.patch_modules()


def selected_attempt_names(attempt_filter: str) -> set[str]:
    allowed = set(ATTEMPT_NAMES)
    if not attempt_filter.strip():
        return allowed
    requested = {item.strip() for item in attempt_filter.split(",") if item.strip()}
    unknown = sorted(requested - allowed)
    if unknown:
        raise ValueError(f"Unsupported attempt names for run337N: {unknown}")
    return requested


def load_repairable_source_attempts(attempt_filter: str) -> list[dict[str, Any]]:
    keep = selected_attempt_names(attempt_filter)
    attempts = read_json(RUN336K_ATTEMPTS)
    prepared: list[dict[str, Any]] = []
    for row in attempts:
        if row.get("attempt_name") not in keep:
            continue
        copied = dict(row)
        copied["model_copy"] = {"source": row.get("model_local_path", "")}
        copied["feature_export"] = {"path": ""}
        copied["source_run_id"] = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
        prepared.append(copied)
    if not prepared:
        raise RuntimeError("No repairable m48/u42 source attempts were selected for run337N.")
    return prepared


def core56_blocker_rows(latest: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": CORE56_ATTEMPT_ID,
            "subject": "core56_refresh_candidate",
            "runtime_status": "blocked_before_mt5_execution",
            "blocker": "core56_refresh_requires_equity_breadth_or_top3_feature_source_repair_before_latest_handoff",
            "latest_us100_last_close_utc": latest.get("us100_last_close_utc", ""),
            "safe_action": "open_run337O_core56_feature_source_repair_or_drop_decision",
            "effect": "core56은 최신 피처 인계가 없어 MT5(메타트레이더5) 결과를 만들지 않고, m48/u42와 섞어 성공처럼 보이지 않게 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def run337o_queue_rows(runtime_rows: Sequence[Mapping[str, Any]], core56_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        completed = (
            row.get("tester_status") == "completed"
            and row.get("runtime_status") == "completed"
            and row.get("report_status") == "completed"
        )
        rows.append(
            {
                "queue_id": f"{row.get('attempt_name')}_stage337O_runtime_attribution",
                "subject": row.get("attempt_name", ""),
                "source_status": "runtime_completed" if completed else "runtime_incomplete",
                "next_work": "cost_direction_curve_runtime_attribution" if completed else "runtime_repair_review",
                "required_outputs": "cost stress;spread/slippage stress;lot-normalized;D/B attribution;long/short;session/hour/regime;curve pockets",
                "blocked_if_missing": "trade ledger or timestamp-aligned proxy-MT5 difference",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in core56_rows:
        rows.append(
            {
                "queue_id": "core56_stage337O_feature_source_repair_or_drop_decision",
                "subject": row.get("subject", ""),
                "source_status": row.get("runtime_status", ""),
                "next_work": "core56_feature_source_refresh_or_research_drop_decision",
                "required_outputs": "as-of equity breadth/top3 source audit;feature handoff repair feasibility;no-lookahead check",
                "blocked_if_missing": "as-of safe source or explicit drop decision",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def gate_rows(
    runtime_rows: Sequence[Mapping[str, Any]],
    freshness_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    core56_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    feature_gaps = sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "covers_latest_broker_close")
    signal_matches = sum(1 for row in signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    compile_status = (execution_result.get("compile") or {}).get("status", "")
    return [
        {
            "gate_name": "latest_broker_data_probe",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "fresh_forward_data_probe_latest.json"),
            "effect": "최신 US100 M5 봉 기준을 고정해 낡은 피처 인계를 숨기지 않는다.",
        },
        {
            "gate_name": "live_safe_feature_handoff_refresh",
            "status": "covered" if feature_gaps == 0 else "covered_with_gap",
            "evidence_path": rel(RUN_DIR / "feature_freshness_gap_audit.csv"),
            "effect": f"m48/u42 피처가 최신 브로커 close(종가)를 덮는지 확인한다; gap attempts={feature_gaps}.",
        },
        {
            "gate_name": "mt5_compile_and_runtime_attempt",
            "status": "covered" if completed == len(runtime_rows) and compile_status in {"completed", "not_attempted_materialize_only"} else "covered_partial",
            "evidence_path": rel(RUN_DIR / "runtime_execution_result.json"),
            "effect": f"MetaEditor(메타에디터) 컴파일과 MT5(메타트레이더5) 실행 증거를 묶는다; completed={completed}/{len(runtime_rows)}.",
        },
        {
            "gate_name": "proxy_expected_and_mt5_difference",
            "status": "covered" if signal_diff_rows else "covered_missing_difference_rows",
            "evidence_path": rel(RUN_DIR / "proxy_mt5_difference.csv"),
            "effect": f"proxy expected(프록시 예상값)와 MT5 observed(관측값) 차이를 남긴다; matched={signal_matches}/{len(signal_diff_rows)}.",
        },
        {
            "gate_name": "core56_refresh_blocker_documented",
            "status": "covered_blocked_subject",
            "evidence_path": rel(RUN_DIR / "core56_refresh_blocker.csv"),
            "effect": f"core56 차단 행 {len(core56_rows)}개를 별도로 남겨 m48/u42 결과와 섞지 않는다.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "final_fresh_mt5_runtime_probe_or_block_decision.json"),
            "effect": "Forward Passed(전진 통과), Forward Failed(전진 실패), Goal Achieve(목표 달성)를 모두 닫아둔다.",
        },
    ]


def classify(
    runtime_rows: Sequence[Mapping[str, Any]],
    freshness_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED_ONLY, JUDGMENT_PARTIAL, DECISION_PARTIAL
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    feature_gaps = sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "covers_latest_broker_close")
    if completed == len(runtime_rows) and feature_gaps == 0:
        return STATUS_COMPLETED_PARTIAL, JUDGMENT_COMPLETED_PARTIAL, DECISION_COMPLETED_PARTIAL
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL


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


def build_receipts(
    latest: Mapping[str, Any],
    feature_summaries: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    core56_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
) -> list[Path]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    signal_matches = sum(1 for row in signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    receipts = {
        "data_integrity_receipt": {
            "run_id": RUN_ID,
            "latest_us100_last_close_utc": latest.get("us100_last_close_utc"),
            "feature_sources": [row.get("feature_csv_path", "") for row in feature_summaries],
            "integrity_judgment": "usable_for_m48_u42_runtime_probe_core56_blocked",
            "effect": "최신 봉까지 피처 인계를 다시 만들고, core56은 source(원천) 문제로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "runtime_parity_receipt": {
            "run_id": RUN_ID,
            "runtime_completed": f"{completed}/{len(runtime_rows)}",
            "signal_parity": f"{signal_matches}/{len(signal_diff_rows)}",
            "parity_judgment": "diagnostic_runtime_parity_available_no_forward_decision",
            "effect": "MT5(메타트레이더5) 관측값과 proxy(프록시) 예상값의 차이를 다음 귀속 단계 입력으로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "backtest_forensics_receipt": {
            "run_id": RUN_ID,
            "tester_identity": "portable MT5 terminal, US100 M5, same .set/.ini contract, same risk and lot settings",
            "runtime_reports": [row.get("report_path", "") for row in runtime_rows],
            "forensics_judgment": "usable_with_boundary" if completed == len(runtime_rows) else "partial_requires_repair",
            "effect": "Strategy Tester(전략 테스터) report(보고서), telemetry(원격측정), settings identity(설정 정체성)를 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "artifact_lineage_receipt": {
            "run_id": RUN_ID,
            "source_attempts": rel(RUN336K_ATTEMPTS),
            "parent_queue": rel(RUN337M_DIR / "run337N_fresh_mt5_runtime_probe_attempt_queue.csv"),
            "core56_blocker": core56_rows,
            "lineage_judgment": "connected_with_partial_blocker",
            "effect": "어떤 산출물이 m48/u42 실행에서 왔고 어떤 항목이 core56 차단인지 추적한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "result_judgment_receipt": {
            "run_id": RUN_ID,
            "status": status,
            "judgment": judgment,
            "decision": decision,
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "effect": "이번 결과는 전진 통과가 아니라 다음 attribution(귀속)과 core56 repair(수리) 입력이다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }
    return [write_json(RUN_DIR / f"{name}.json", payload) for name, payload in receipts.items()]


def write_report(
    status: str,
    judgment: str,
    decision: str,
    latest: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    freshness_rows: Sequence[Mapping[str, Any]],
    core56_rows: Sequence[Mapping[str, Any]],
) -> Path:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    feature_gaps = sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "covers_latest_broker_close")
    lines = [
        "# Stage337N Fresh MT5 Runtime Probe Or Block(337N 신규 MT5 런타임 탐침 또는 차단)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- latest US100 close(최신 US100 종가): `{latest.get('us100_last_close_utc', '')}`",
        f"- MT5 completed(MT5 완료): `{completed}/{len(runtime_rows)}`",
        f"- feature handoff gap(피처 인계 공백): `{feature_gaps}/{len(freshness_rows)}`",
        f"- core56 blocker(core56 차단): `{len(core56_rows)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Effect(효과)",
        "",
        "run337N은 최신 브로커 봉까지 m48/u42 feature handoff(피처 인계)를 다시 만들고 MT5(메타트레이더5) 런타임으로 확인한다. core56은 최신 source(원천) 문제가 아직 있어 별도 blocker(차단 사유)로 남긴다.",
        "",
        "## Runtime Rows(런타임 행)",
        "",
        "| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        status_label = f"{row.get('tester_status', '')}/{row.get('runtime_status', '')}/{row.get('report_status', '')}"
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{status_label}` | `{row.get('net_profit', '')}` | `{row.get('profit_factor', '')}` | `{row.get('trade_count', '')}` | `{row.get('max_drawdown_amount', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "이 실행은 forward decision(전진 판정)이 아니라 attribution/reair input(귀속/수리 입력)이다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(랏 최적화)은 수행하지 않았다.",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(status: str, judgment: str, decision: str, latest: Mapping[str, Any]) -> Path:
    text = f"""# Stage337N Decision(337N 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- latest US100 close(최신 US100 종가): `{latest.get('us100_last_close_utc', '')}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): m48/u42는 최신 피처 인계와 MT5(메타트레이더5) 런타임 확인으로 다음 attribution(귀속) 단계에 보낼 수 있다. core56은 source refresh(원천 갱신) 없이는 실행하지 않는다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(status: str, decision: str, latest: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild`
- opened_by(개방 실행): `run336P_forward_decision_or_failure_memory_handoff_v1`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest US100 close(최신 US100 종가): `{latest.get('us100_last_close_utc', '')}`
- fresh MT5 runtime probe(신규 MT5 런타임 탐침): `{completed}/{len(runtime_rows)} completed(완료)`
- core56 refresh(core56 갱신): `blocked_until_source_repair_or_drop_decision`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337N(337N 실행)는 m48/u42 최신 피처 인계와 MT5(메타트레이더5) 런타임 탐침을 시도하고, core56은 차단 사유를 분리했다. 아직 선택 후보는 없다.
"""
    write_md(SELECTED_STATUS, selection_text)

    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[idx] = f"current_run_id: {NEXT_RUN_ID}"
                break
        focus_line = (
            "- >-\n"
            f"  Stage337 run337N focus complete: Stage337(337단계) run337N(337N 실행)는 `{status}`로 fresh MT5 runtime probe attempt-or-block(신규 MT5 런타임 탐침 시도 또는 차단)을 처리했다. "
            "Effect(효과): m48/u42는 최신 피처 인계와 MT5(메타트레이더5) 런타임 증거를 만들고 core56은 source repair(원천 수리) 전까지 분리했으며, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
        )
        try:
            current_focus_idx = lines.index("current_focus:")
            if "Stage337 run337N focus complete" not in text:
                lines.insert(current_focus_idx + 1, focus_line.rstrip())
        except ValueError:
            lines.append("current_focus:")
            lines.append(focus_line.rstrip())
        write_text_preserving(WORKSPACE_STATE, "\n".join(lines) + "\n", had_bom)

    current_entry = f"""
## Stage337 run337N(337N 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- latest US100 close(최신 US100 종가): `{latest.get('us100_last_close_utc', '')}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 최신 MT5(메타트레이더5) 봉 기준으로 m48/u42 피처 인계를 다시 만들고 runtime probe(런타임 탐침)를 실행했다. core56은 source repair(원천 수리) 전까지 차단한다.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337N(337N 실행)" not in text:
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n\n" + current_entry.strip() + "\n", had_bom)

    changelog_entry = (
        f"\n- {TODAY}: Stage337 run337N(337N 실행) `{status}`. "
        "Effect(효과): fresh MT5 runtime probe(신규 MT5 런타임 탐침)를 최신 피처 인계 기준으로 처리하고 core56 blocker(차단 사유)를 분리했다. "
        "Forward/Goal(전진/목표) 주장은 없음.\n"
    )
    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        if "Stage337 run337N(337N 실행)" not in text:
            write_text_preserving(CHANGELOG, text.rstrip() + changelog_entry, had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "runtime_parity_feature_handoff_repair",
                "lane": "runtime_parity",
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
                "run_key": f"{RUN_ID}__fresh_mt5_runtime_probe_or_block",
                "ledger_row_id": f"{RUN_ID}__fresh_mt5_runtime_probe_or_block",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "runtime_parity_feature_handoff_repair",
                "work_family": "runtime_parity_feature_handoff_repair",
                "question": "can latest m48/u42 feature handoff survive fresh MT5 runtime while core56 remains blocked",
                "metric_scope": "fresh_mt5_runtime_probe_no_forward_decision",
                "evidence_scope": "latest_feature_handoff_repair_runtime_probe_core56_blocker",
                "kpi_scope": "runtime_diagnostic_no_forward_kpi_decision",
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
    artifact_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        suffix = path.suffix.lower()
        artifact_rows.append(
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
    artifacts.append(append_csv_rows(ARTIFACT_REGISTRY, artifact_rows))
    return artifacts


def main() -> int:
    args = parse_args()
    configure_repair_modules()
    generated_at_utc = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)

    end_utc = resolve_probe_end_utc(args.end_utc, Path(args.terminal_path))
    raw_rows, latest = run336k.probe_latest_raw_data(Path(args.terminal_path), end_utc)
    latest_close = pd.to_datetime(latest["us100_last_close_utc"], utc=True)
    terminal_recovery = (
        {"status": "skipped_materialize_only"}
        if args.materialize_only
        else run336k.stop_target_terminal_if_running(Path(args.terminal_path))
    )

    source_attempts = load_repairable_source_attempts(args.attempt_filter)
    context, repaired_frame, foundation_counts, overnight_rows = repair.build_repaired_foundation_frame(latest_close)
    feature_summaries, missing_rows, feature_source_paths, feature_source_artifacts = repair.materialize_repaired_feature_sources(
        context,
        repaired_frame,
        latest_close,
        source_attempts,
    )
    prepared_sources = repair.attach_repaired_feature_exports(source_attempts, feature_source_paths)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared_sources, Path(args.common_files_root))
    attempts = [repair.rewrite_attempt_to_latest(dict(attempt), str(latest["tester_to_date"])) for attempt in attempts]
    for attempt in attempts:
        attempt["attempt_role"] = "stage337N_latest_live_safe_feature_handoff_same_frozen_model_feature_threshold_risk"
        attempt["record_view_prefix"] = f"mt5_stage337N_{attempt['artifact_slug']}"
        attempt["source_run_id"] = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
        attempt["repair_source_run_id"] = PARENT_RUN_ID

    proxy_rows = repair.sanitize_proxy_rows(base.build_proxy_signal_expected_rows(attempts))
    freshness_rows = repair.build_feature_freshness_rows(attempts, latest)
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
    signal_diff_rows = repair.sanitize_signal_diff_rows(base.build_signal_difference_rows(proxy_rows, runtime_rows))
    core56_rows = core56_blocker_rows(latest)
    status, judgment, decision = classify(runtime_rows, freshness_rows, bool(args.materialize_only))
    queue_rows = run337o_queue_rows(runtime_rows, core56_rows)
    gates = gate_rows(runtime_rows, freshness_rows, signal_diff_rows, core56_rows, execution_result)
    metrics = metric_summary(runtime_rows)

    artifact_paths: list[Path] = [
        write_csv(
            RUN_DIR / "fresh_forward_data_probe_summary.csv",
            ["contract_symbol", "broker_symbol", "status", "rows", "first_open_utc", "last_open_utc", "last_close_utc", "csv_path", "manifest_path", "last_error"],
            raw_rows,
        ),
        write_json(RUN_DIR / "fresh_forward_data_probe_latest.json", latest),
        write_json(RUN_DIR / "terminal_process_recovery.json", terminal_recovery),
        write_json(RUN_DIR / "foundation_feature_counts.json", foundation_counts),
        write_csv(
            RUN_DIR / "live_safe_overnight_overlap_audit.csv",
            ["check_id", "old_non_null_rows", "repaired_non_null_rows", "overlap_rows", "newly_available_rows", "max_abs_diff_on_overlap", "changed_overlap_rows", "judgment", "claim_boundary"],
            overnight_rows,
        ),
        write_csv(
            RUN_DIR / "repaired_feature_set_summary.csv",
            [
                "feature_set_id",
                "feature_count",
                "feature_order_sha256",
                "required_symbols",
                "scope_rows",
                "valid_rows",
                "invalid_rows",
                "alignment_missing_rows",
                "finite_missing_rows",
                "first_valid_timestamp",
                "last_valid_timestamp",
                "latest_us100_close",
                "feature_csv_path",
                "feature_csv_sha256",
                "mt5_export_rows",
                "repair_contract",
                "claim_boundary",
            ],
            feature_summaries,
        ),
        write_csv(
            RUN_DIR / "repaired_feature_missing_counts.csv",
            ["feature_set_id", "feature", "missing_or_nonfinite_rows"],
            missing_rows or [{"feature_set_id": "", "feature": "", "missing_or_nonfinite_rows": 0}],
        ),
        write_json(RUN_DIR / "independent_handoff_attempts.json", attempts),
        write_csv(
            RUN_DIR / "branch_attempt_binding.csv",
            ["attempt_name", "artifact_slug", "feature_set_id", "model_id", "binding_status", "branch_use", "selection_use", "forward_decision_use", "claim_boundary"],
            repair.build_branch_rows(attempts),
        ),
        write_csv(
            RUN_DIR / "independent_handoff_attempt_manifest.csv",
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
                "source_set_sha256",
                "new_set_sha256",
                "model_sha256",
                "feature_sha256",
                "materialization_status",
                "claim_boundary",
            ],
            handoff_rows,
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
            RUN_DIR / "feature_freshness_gap_audit.csv",
            ["attempt_name", "artifact_slug", "feature_set_id", "feature_rows", "feature_first_timestamp", "feature_last_timestamp", "latest_us100_last_close_utc", "feature_to_latest_gap_minutes", "fresh_latest_handoff_status", "effect", "claim_boundary"],
            freshness_rows,
        ),
        write_json(RUN_DIR / "runtime_execution_result.json", execution_result),
        write_csv(
            RUN_DIR / "fresh_mt5_runtime_probe_result.csv",
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
            RUN_DIR / "proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            signal_diff_rows,
        ),
        write_csv(
            RUN_DIR / "runtime_metric_summary.csv",
            [
                "attempt_name",
                "feature_set_id",
                "runtime_status",
                "report_status",
                "net_profit",
                "profit_factor",
                "trade_count",
                "expectancy",
                "recovery_factor",
                "max_drawdown_amount",
                "long_trade_count",
                "short_trade_count",
                "lot_normalized_net_per_trade",
                "claim_boundary",
            ],
            metrics,
        ),
        write_csv(
            RUN_DIR / "core56_refresh_blocker.csv",
            ["attempt_id", "subject", "runtime_status", "blocker", "latest_us100_last_close_utc", "safe_action", "effect", "claim_boundary"],
            core56_rows,
        ),
        write_csv(
            RUN_DIR / "run337O_runtime_attribution_or_repair_queue.csv",
            ["queue_id", "subject", "source_status", "next_work", "required_outputs", "blocked_if_missing", "claim_boundary"],
            queue_rows,
        ),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(
            RUN_DIR / "tester_settings_identity.json",
            {
                "run_id": RUN_ID,
                "tester_to_date": latest.get("tester_to_date"),
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "queued_attempts": [attempt["attempt_name"] for attempt in attempts],
                "core56_status": "blocked_before_mt5_execution",
                "model_training": "forbidden_not_performed",
                "threshold_retuning": "forbidden_not_performed",
                "lot_optimization": "forbidden_not_performed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifact_paths.extend(feature_source_artifacts)
    artifact_paths.extend(materialized_artifacts)
    artifact_paths.extend(base.copy_runtime_outputs(Path(args.common_files_root), attempts))
    artifact_paths.extend(repair.copy_reports_to_required_names(runtime_rows))
    artifact_paths.extend(build_receipts(latest, feature_summaries, runtime_rows, signal_diff_rows, core56_rows, status, judgment, decision))
    artifact_paths.append(write_report(status, judgment, decision, latest, runtime_rows, freshness_rows, core56_rows))
    artifact_paths.append(write_decision_doc(status, judgment, decision, latest))
    artifact_paths.extend(update_status_docs(status, decision, latest, runtime_rows))

    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    signal_matches = sum(1 for row in signal_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "latest_us100_last_close_utc": latest.get("us100_last_close_utc"),
        "fresh_runtime_completed": completed,
        "fresh_runtime_total": len(runtime_rows),
        "feature_latest_gap_attempts": sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "covers_latest_broker_close"),
        "signal_parity_matched_rows": signal_matches,
        "signal_parity_total_rows": len(signal_diff_rows),
        "core56_blocked_rows": len(core56_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_fresh_mt5_runtime_probe_or_block_decision.json", final_decision))
    artifact_paths.extend(update_registers(status, judgment, decision, [*artifact_paths, Path(__file__)]))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "parent_run_id": PARENT_RUN_ID,
                "command": "python stage_pipelines/stage337/attempt_fresh_mt5_runtime_probe_or_block.py",
                "materialize_only": bool(args.materialize_only),
                "attempt_filter": args.attempt_filter,
                "artifacts": [rel(path) for path in artifact_paths if path_exists(path)],
            },
        )
    )
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
