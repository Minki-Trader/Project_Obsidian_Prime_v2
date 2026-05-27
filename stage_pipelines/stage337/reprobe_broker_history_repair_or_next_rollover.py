# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import reprobe_data_history_cache_repair_or_next_rollover as aj  # noqa: E402
from stage_pipelines.stage337 import reprobe_next_rollover_or_synthetic_custom_parity_repair as ak  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AP"
RUN_ID = "run337AP_broker_tester_history_repair_or_next_rollover_v1"
PARENT_RUN_ID = "run337AO_asof_regime_and_db_source_materialization_v1"
SOURCE_RUN_ID = "run337AN_broker_rollover_reprobe_when_utc_day_boundary_available_v1"
NEXT_RUN_ID_GAP = "run337AQ_tester_visible_cutoff_policy_and_db_instrumentation_v1"
NEXT_RUN_ID_REPAIRED = "run337AQ_forward_attribution_after_broker_history_repair_and_db_instrumentation_v1"
NEXT_RUN_ID_RUNTIME = "run337AQ_broker_runtime_output_repair_v1"

CLAIM_BOUNDARY = (
    "research_development_only_stage337AP_broker_history_repair_reprobe_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STATUS_REPAIRED = "completed_stage337AP_broker_history_repair_reached_feature_last_no_forward_decision"
STATUS_GAP = "completed_stage337AP_broker_history_repair_gap_remains_no_forward_decision"
STATUS_RUNTIME = "completed_stage337AP_broker_history_repair_runtime_issue_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AP_broker_history_repair_materialized_only_no_forward_decision"
JUDGMENT_REPAIRED = "broker_history_repair_reached_feature_last_but_db_instrumentation_and_forward_review_still_required"
JUDGMENT_GAP = "broker_tester_history_gap_remains_after_api_warmup_and_reprobe"
JUDGMENT_RUNTIME = "broker_history_reprobe_runtime_output_incomplete"
JUDGMENT_MATERIALIZED = "broker_history_reprobe_inputs_materialized_execution_pending"
DECISION_REPAIRED = "stage337AP_open_run337AQ_forward_attribution_and_db_instrumentation_no_selection"
DECISION_GAP = "stage337AP_open_run337AQ_tester_visible_cutoff_and_db_instrumentation_no_selection"
DECISION_RUNTIME = "stage337AP_open_run337AQ_runtime_output_repair_no_selection"
DECISION_MATERIALIZED = "stage337AP_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SOURCE_DIR = STAGE_DIR / "02_runs" / "run337AN"
SOURCE_ATTEMPTS = SOURCE_DIR / "handoff_attempts.json"
SOURCE_FINAL = SOURCE_DIR / "final_decision.json"
PARENT_FINAL = STAGE_DIR / "02_runs" / "run337AO" / "final_decision.json"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AP_broker_tester_history_repair_or_next_rollover.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AP_broker_tester_history_repair.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = [
    "run_id",
    "stage_id",
    "lane",
    "status",
    "judgment",
    "path",
    "notes",
    "family",
    "primary_report",
]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]

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
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AP_broker_history_repair"
ORIGIN_SYMBOL = "US100"
BROKER_FROM_DATE = "2026.04.14"

SCENARIOS = [
    {
        "suffix": "api_warm_model4_real_ticks",
        "artifact_slug": "u42_plain_ap_api_warm_model4_real_ticks",
        "scenario_id": "api_warmup_model4_real_ticks_control",
        "model_code": "4",
        "to_date": "2026.05.30",
    },
    {
        "suffix": "api_warm_model0_generated",
        "artifact_slug": "u42_plain_ap_api_warm_model0_generated",
        "scenario_id": "api_warmup_model0_generated_control",
        "model_code": "0",
        "to_date": "2026.05.30",
    },
    {
        "suffix": "api_warm_model4_wide_todate",
        "artifact_slug": "u42_plain_ap_api_warm_model4_wide_todate",
        "scenario_id": "api_warmup_model4_real_ticks_wide_todate",
        "model_code": "4",
        "to_date": "2026.06.03",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AP broker tester history repair or next rollover reprobe.")
    parser.add_argument("--terminal", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return ak.rel(path)


def upsert_csv_fixed_columns(path: Path, key_columns: Sequence[str], row: Mapping[str, Any], columns: Sequence[str]) -> Path:
    rows = [
        {column: existing.get(column, "") for column in columns}
        for existing in ak.read_csv(path)
    ]
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [
        existing
        for existing in rows
        if tuple(str(existing.get(column, "")) for column in key_columns) != key
    ]
    rows.append({column: row.get(column, "") for column in columns})
    return ak.write_csv(path, columns, rows)


def truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "1", "yes", "matched"}


def number(value: Any) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def configure_modules() -> None:
    root = Path(__file__).resolve().parents[2]
    for module in (base, qprobe, ab, aj, ak):
        module.TODAY = TODAY
        module.STAGE_ID = STAGE_ID
        module.RUN_NUMBER = RUN_NUMBER
        module.RUN_ID = RUN_ID
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.CLAIM_BOUNDARY = CLAIM_BOUNDARY
        module.RUN_DIR = root / RUN_DIR
    base.MT5_DIR = root / MT5_DIR
    base.FEATURE_COPY_DIR = root / FEATURE_COPY_DIR
    base.MODEL_COPY_DIR = root / MODEL_COPY_DIR
    base.TELEMETRY_DIR = root / TELEMETRY_DIR
    base.COMMON_ROOT = COMMON_ROOT
    base.PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / mt5.EA_SOURCE_PATH
    base.PORTABLE_EA_EX5 = (
        DEFAULT_PORTABLE_ROOT
        / "MQL5"
        / "Experts"
        / "Project_Obsidian_Prime_v2"
        / "foundation"
        / "mt5"
        / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    )
    qprobe.MT5_DIR = root / MT5_DIR
    qprobe.FEATURE_COPY_DIR = root / FEATURE_COPY_DIR
    qprobe.MODEL_COPY_DIR = root / MODEL_COPY_DIR
    qprobe.TELEMETRY_DIR = root / TELEMETRY_DIR
    qprobe.TESTER_LOG = TESTER_LOG
    qprobe.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    qprobe.TERMINAL_LOG = TERMINAL_LOG
    ab.TESTER_LOG = TESTER_LOG
    ab.TESTER_AGENT_LOG = TESTER_AGENT_LOG
    ab.TERMINAL_LOG = TERMINAL_LOG
    aj.ORIGIN_SYMBOL = ORIGIN_SYMBOL
    ak.ARTIFACT_REGISTRY = root / ARTIFACT_REGISTRY


def load_source_attempt() -> dict[str, Any]:
    attempts = ak.read_json(SOURCE_ATTEMPTS)
    if not isinstance(attempts, list):
        raise RuntimeError(f"source attempts is not a list: {SOURCE_ATTEMPTS}")
    source = next((dict(row) for row in attempts if row.get("attempt_name") == "u42_plain_rf_an_broker_rollover_reprobe"), None)
    if source is None:
        raise RuntimeError("missing run337AN broker source attempt")
    return source


def build_prepared_attempts(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, scenario in enumerate(SCENARIOS):
        copied = dict(source)
        copied["attempt_name"] = f"u42_plain_rf_ap_{scenario['suffix']}"
        copied["artifact_slug"] = scenario["artifact_slug"]
        copied["scenario_id"] = scenario["scenario_id"]
        copied["scenario_symbol"] = ORIGIN_SYMBOL
        copied["scenario_from_date"] = BROKER_FROM_DATE
        copied["scenario_to_date"] = scenario["to_date"]
        copied["scenario_model"] = scenario["model_code"]
        copied["source_attempt_name"] = source.get("attempt_name", "")
        copied["source_run_id"] = SOURCE_RUN_ID
        copied["parent_run_id"] = PARENT_RUN_ID
        copied["model_copy"] = {"source": source.get("model_local_path") or source.get("model_copy", {}).get("source", "")}
        copied["feature_export"] = {"path": source.get("feature_local_path", "")}
        copied["feature_local_path"] = source.get("feature_local_path", "")
        copied["attempt_role"] = "stage337AP_broker_history_repair_same_frozen_u42_model_threshold_risk"
        copied["record_view_prefix"] = f"mt5_stage337AP_u42_plain_broker_history_repair_{index}"
        copied["repair_contract"] = (
            "MT5 API history warmup and tester rerun only; same ONNX(온엑스), feature order(피처 순서), "
            "threshold(임계값), risk/lot(위험/랏), and ATR SL/TP(ATR 손절/익절)."
        )
        copied["signal_policy"] = "proxy expected(프록시 예상값)는 runtime signal parity(런타임 신호 동등성)에만 사용한다."
        rows.append(copied)
    return rows


def rewrite_attempt_to_scenario(attempt: dict[str, Any]) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["Symbol"] = attempt["scenario_symbol"]
    tester["FromDate"] = attempt["scenario_from_date"]
    tester["ToDate"] = attempt["scenario_to_date"]
    tester["Model"] = attempt["scenario_model"]
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    attempt["ini"] = base.materialize_ini_file(tester, Path(str(attempt["ini"]["path"])))
    attempt["from_date"] = tester["FromDate"]
    attempt["to_date"] = tester["ToDate"]
    attempt["tester_symbol"] = tester["Symbol"]
    attempt["tester_model"] = tester["Model"]
    attempt["attempt_role"] = "stage337AP_broker_history_repair_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AP_{attempt['artifact_slug']}"
    attempt["repair_contract"] = (
        "Only API history warmup, tester Model/ToDate probe, and output identity change; model and trading logic are frozen."
    )
    return attempt


def runtime_completed(row: Mapping[str, Any]) -> bool:
    return (
        row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )


def sanitize_diff(rows: Sequence[Mapping[str, Any]], source_label: str) -> list[dict[str, Any]]:
    clean: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["proxy_source"] = source_label
        item["mt5_source"] = "stage337AP_runtime_summary(337AP 런타임 요약)"
        item["claim_boundary"] = CLAIM_BOUNDARY
        clean.append(item)
    return clean


def proxy_usability_rows(
    gap_rows: Sequence[Mapping[str, Any]],
    raw_diff: Sequence[Mapping[str, Any]],
    aligned_diff: Sequence[Mapping[str, Any]],
    parent_final: Mapping[str, Any],
) -> list[dict[str, Any]]:
    db_missing = int(number(parent_final.get("db_missing_required_columns")) or 0)
    rows: list[dict[str, Any]] = []
    for gap in gap_rows:
        attempt = str(gap.get("attempt_name", ""))
        raw = [row for row in raw_diff if row.get("attempt_name") == attempt]
        aligned = [row for row in aligned_diff if row.get("attempt_name") == attempt]
        raw_matches = sum(1 for row in raw if truthy(row.get("usable_for_runtime_signal_parity")))
        aligned_matches = sum(1 for row in aligned if truthy(row.get("usable_for_runtime_signal_parity")))
        reached = gap.get("gap_status") == "tester_reached_feature_last"
        rows.append(
            {
                "attempt_name": attempt,
                "gap_status": gap.get("gap_status", ""),
                "raw_proxy_matched": raw_matches,
                "raw_proxy_total": len(raw),
                "timestamp_aligned_proxy_matched": aligned_matches,
                "timestamp_aligned_proxy_total": len(aligned),
                "usable_for_runtime_signal_parity": aligned_matches == len(aligned) and len(aligned) > 0,
                "usable_for_forward_pass_fail": reached and db_missing == 0 and aligned_matches == len(aligned) and len(aligned) > 0,
                "db_missing_required_columns": db_missing,
                "judgment": (
                    "runtime_signal_parity_only"
                    if aligned_matches == len(aligned) and len(aligned) > 0
                    else "proxy_runtime_mismatch_requires_review"
                ),
                "effect": "proxy expected(프록시 예상값)와 MT5 runtime(런타임)을 비교해 사용 범위를 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def classify(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    aligned_diff: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, RUN_ID
    completed = sum(1 for row in runtime_rows if runtime_completed(row))
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matched = sum(1 for row in aligned_diff if truthy(row.get("usable_for_runtime_signal_parity")))
    if completed != len(runtime_rows) or not runtime_rows:
        return STATUS_RUNTIME, JUDGMENT_RUNTIME, DECISION_RUNTIME, NEXT_RUN_ID_RUNTIME
    if reached == len(gap_rows) and gap_rows and matched == len(aligned_diff) and aligned_diff:
        return STATUS_REPAIRED, JUDGMENT_REPAIRED, DECISION_REPAIRED, NEXT_RUN_ID_REPAIRED
    return STATUS_GAP, JUDGMENT_GAP, DECISION_GAP, NEXT_RUN_ID_GAP


def final_payload(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    broker_api: Mapping[str, Any],
    warmup_payload: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    raw_diff: Sequence[Mapping[str, Any]],
    aligned_diff: Sequence[Mapping[str, Any]],
    parent_final: Mapping[str, Any],
) -> dict[str, Any]:
    completed = sum(1 for row in runtime_rows if runtime_completed(row))
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff if truthy(row.get("usable_for_runtime_signal_parity")))
    aligned_matches = sum(1 for row in aligned_diff if truthy(row.get("usable_for_runtime_signal_parity")))
    first_gap = gap_rows[0] if gap_rows else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "broker_api_status": broker_api.get("status", ""),
        "api_latest_us100_close_utc": broker_api.get("m5_last_close_utc", ""),
        "api_history_warmup_status": warmup_payload.get("status", ""),
        "runtime_completed": completed,
        "runtime_total": len(runtime_rows),
        "tester_reached_feature_last": reached,
        "tester_gap_total": len(gap_rows),
        "broker_gap_status": first_gap.get("gap_status", ""),
        "feature_last_timestamp": first_gap.get("feature_last_timestamp", ""),
        "tester_last_observed_bar_time": first_gap.get("tester_last_observed_bar_time", ""),
        "tester_to_feature_last_gap_minutes": first_gap.get("tester_to_feature_last_gap_minutes", ""),
        "raw_proxy_mt5_matched": raw_matches,
        "raw_proxy_mt5_rows": len(raw_diff),
        "timestamp_aligned_proxy_mt5_matched": aligned_matches,
        "timestamp_aligned_proxy_mt5_rows": len(aligned_diff),
        "db_missing_required_columns": parent_final.get("db_missing_required_columns", ""),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows(final: Mapping[str, Any], warmup_rows: Sequence[Mapping[str, Any]], handoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "frozen_identity_lock",
            "status": "passed" if all(str(row.get("threshold_keys_unchanged", "")).lower() == "true" for row in handoff_rows) else "failed",
            "evidence_path": rel(RUN_DIR / "handoff_attempts.csv"),
            "effect": "ONNX(온엑스), feature order(피처 순서), threshold(임계값), risk/lot(위험/랏)을 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "api_history_warmup_attempted",
            "status": "passed" if warmup_rows else "failed",
            "evidence_path": rel(RUN_DIR / "api_history_warmup.csv"),
            "effect": "MT5 API history warmup(API 이력 예열)으로 현재일 브로커 이력을 강제로 읽는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "mt5_runtime_completed",
            "status": "passed" if final["runtime_completed"] == final["runtime_total"] and final["runtime_total"] else "failed",
            "evidence_path": rel(RUN_DIR / "runtime_summary.csv"),
            "effect": "Strategy Tester(전략 테스터) 출력과 runtime telemetry(런타임 기록)를 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "tester_feature_last_reach",
            "status": "passed" if final["tester_reached_feature_last"] == final["tester_gap_total"] and final["tester_gap_total"] else "failed",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_history_repair.csv"),
            "effect": "tester last observed(테스터 마지막 관측)가 feature_last(피처 끝)에 닿는지 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_usability_recorded",
            "status": "passed" if final["timestamp_aligned_proxy_mt5_rows"] else "failed",
            "evidence_path": rel(RUN_DIR / "proxy_mt5_usability_history_repair.csv"),
            "effect": "proxy expected(프록시 예상값)와 MT5 runtime(런타임)의 사용 가능 범위를 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_claim_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def receipt_payloads(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]]) -> dict[Path, Mapping[str, Any]]:
    return {
        RUN_DIR / "data_integrity_receipt.json": {
            "receipt_type": "data_integrity",
            "data_source": [rel(SOURCE_FINAL), rel(PARENT_FINAL), rel(RUN_DIR / "api_history_warmup.csv")],
            "time_axis": "US100 M5 UTC-like broker close time; feature_last compared to tester telemetry bar_time",
            "sample_scope": "post-OOS broker forward runtime probe using frozen u42 source-clean handoff",
            "feature_label_boundary": "no new training, no threshold retune, no future feature fill",
            "leakage_risk": "using tester-invisible current-day data for pass/fail would be lookahead-like authority",
            "integrity_judgment": "usable_with_boundary_for_runtime_probe_not_forward_decision",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RUN_DIR / "runtime_parity_receipt.json": {
            "receipt_type": "runtime_parity",
            "research_path": "stage_pipelines/stage337/reprobe_broker_history_repair_or_next_rollover.py",
            "runtime_path": rel(RUN_DIR / "handoff_attempts.json"),
            "shared_contract": "same ONNX, feature order, thresholds, risk, lot, ATR SL/TP, and runtime handoff",
            "known_differences": "API warmup, tester model/to-date scenario, report identity",
            "parity_check": f"timestamp-aligned proxy/MT5 {final['timestamp_aligned_proxy_mt5_matched']}/{final['timestamp_aligned_proxy_mt5_rows']}",
            "parity_identity": {"attempts": attempts, "runtime_rows": runtime_rows},
            "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
        },
        RUN_DIR / "backtest_forensics_receipt.json": {
            "receipt_type": "backtest_forensics",
            "tester_identity": "FPMarketsSC-Live US100 M5 Strategy Tester broker history repair reprobe",
            "ea_identity": rel(RUN_DIR / "handoff_attempts.json"),
            "report_identity": [row.get("report_path", "") for row in runtime_rows],
            "trade_evidence": [{key: row.get(key, "") for key in ("attempt_name", "net_profit", "profit_factor", "trade_count", "max_drawdown_amount")} for row in runtime_rows],
            "forensic_checks": ["API warmup", "tester report", "runtime telemetry", "feature_last gap"],
            "backtest_judgment": "usable_with_boundary_for_runtime_probe_not_forward_decision",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RUN_DIR / "result_judgment_receipt.json": {
            "receipt_type": "result_judgment",
            "result_subject": "run337AP broker tester history repair reprobe",
            "evidence_available": [rel(RUN_DIR / "runtime_summary.csv"), rel(RUN_DIR / "tester_feature_last_gap_history_repair.csv"), rel(RUN_DIR / "proxy_mt5_usability_history_repair.csv")],
            "evidence_missing": "D/B source telemetry remains missing; Forward Passed/Failed is not available",
            "judgment_label": "runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": final["next_action"],
        },
    }


def report_text(final: Mapping[str, Any], usability: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage337AP Broker Tester History Repair(337AP 브로커 테스터 이력 수리)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- API latest close(API 최신 종가): `{final['api_latest_us100_close_utc']}`",
        f"- runtime completed(런타임 완료): `{final['runtime_completed']}/{final['runtime_total']}`",
        f"- tester reached feature_last(테스터 피처 끝 도달): `{final['tester_reached_feature_last']}/{final['tester_gap_total']}`",
        f"- raw proxy/MT5(원시 프록시/MT5): `{final['raw_proxy_mt5_matched']}/{final['raw_proxy_mt5_rows']}`",
        f"- timestamp-aligned proxy/MT5(시점 맞춤 프록시/MT5): `{final['timestamp_aligned_proxy_mt5_matched']}/{final['timestamp_aligned_proxy_mt5_rows']}`",
        f"- D/B missing columns(D/B 누락 컬럼): `{final['db_missing_required_columns']}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Meaning(의미)",
        "",
        "run337AP(337AP 실행)는 MT5 API history warmup(API 이력 예열) 뒤 같은 frozen ONNX(고정 온엑스)를 Strategy Tester(전략 테스터)에 다시 넣었다. 효과(effect, 효과)는 broker tester gap(브로커 테스터 공백)이 데이터 캐시 문제인지, tester-visible cutoff(테스터 가시 컷오프) 문제인지 더 좁히는 것이다.",
        "",
        "## Proxy Use(프록시 사용)",
        "",
        "| attempt(시도) | gap(공백) | raw proxy(원시 프록시) | aligned proxy(정렬 프록시) | runtime usable(런타임 사용) | forward usable(전진 사용) |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in usability:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('gap_status', '')}` | "
            f"`{row.get('raw_proxy_matched', '')}/{row.get('raw_proxy_total', '')}` | "
            f"`{row.get('timestamp_aligned_proxy_matched', '')}/{row.get('timestamp_aligned_proxy_total', '')}` | "
            f"`{row.get('usable_for_runtime_signal_parity', '')}` | `{row.get('usable_for_forward_pass_fail', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "proxy expected(프록시 예상값)는 runtime signal parity(런타임 신호 동등성) 확인에는 쓸 수 있지만, broker tester(브로커 테스터)가 feature_last(피처 끝)에 닿지 않거나 D/B source(D/B 원천)가 없으면 Forward Passed/Failed(전진 통과/실패)에 쓸 수 없다.",
        ]
    )
    return "\n".join(lines)


def decision_doc_text(final: Mapping[str, Any]) -> str:
    return f"""# 2026-05-27 Stage337AP Broker History Repair Decision(337AP 브로커 이력 수리 결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): broker tester history(브로커 테스터 이력)를 API warmup(API 예열) 뒤 재탐침했고, proxy/MT5(프록시/MT5) 사용 범위를 runtime parity(런타임 동등성)와 forward decision(전진 판정)으로 분리했다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return replacement + "\n" + text


def update_status_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- broker_forward_boundary(브로커 전진 경계): `failed`
- broker_gap_status(브로커 공백 상태): `{final['broker_gap_status']}`
- tester_reached_feature_last(테스터 피처 끝 도달): `{final['tester_reached_feature_last']}/{final['tester_gap_total']}`
- timestamp_aligned_proxy_parity(시점 맞춤 프록시 동등성): `{final['timestamp_aligned_proxy_mt5_matched']}/{final['timestamp_aligned_proxy_mt5_rows']}`
- db_source_status(D/B 원천 상태): `missing_required_columns_{final['db_missing_required_columns']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_feature_last_or_db_source_not_closed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AP(337AP 실행)는 broker history repair(브로커 이력 수리)를 재탐침하고 proxy/MT5(프록시/MT5) 사용 범위를 분리했다.
"""
    artifacts.append(ak.write_md(SELECTED_STATUS, selection))

    text, had_bom = ak.read_text(WORKSPACE_STATE)
    text = replace_line(text, "current_run_id:", f"current_run_id: {final['next_action']}")
    focus = (
        "- >-\n"
        f"  Stage337 run337AP focus complete: run337AP(337AP 실행)은 `{final['status']}`로 broker tester history repair(브로커 테스터 이력 수리)를 재탐침했다. "
        f"Effect(효과): runtime(런타임) `{final['runtime_completed']}/{final['runtime_total']}`, tester reached feature_last(테스터 피처 끝 도달) "
        f"`{final['tester_reached_feature_last']}/{final['tester_gap_total']}`, timestamp-aligned proxy/MT5(시점 맞춤 프록시/MT5) "
        f"`{final['timestamp_aligned_proxy_mt5_matched']}/{final['timestamp_aligned_proxy_mt5_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    text = re.sub(r"- >-\n  Stage337 run337AP focus complete:.*?(?=\n- >-|\Z)", "", text, flags=re.S)
    text = re.sub(r"current_focus:\n", "current_focus:\n" + focus + "\n", text, count=1)
    artifacts.append(ak.write_text(WORKSPACE_STATE, text, had_bom))

    current = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{final['next_action']}`
- secondary_current_run(보조 현재 실행): `none`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Stage337 run337AP(337AP 실행) - 2026-05-27

- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): broker tester history repair(브로커 테스터 이력 수리)를 재탐침했고 proxy expected(프록시 예상값)와 MT5 runtime(런타임)의 사용 가능성을 분리했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    old_current, old_bom = ak.read_text(CURRENT_STATE)
    marker = "\n## Stage267 Candidate Pool"
    tail = old_current[old_current.find(marker) :] if marker in old_current else "\n"
    artifacts.append(ak.write_text(CURRENT_STATE, current + tail, old_bom))

    brief, brief_bom = ak.read_text(STAGE_BRIEF)
    brief = replace_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337AP_summary(337AP 요약): `{final['status']}`. "
        f"Effect(효과): broker history repair(브로커 이력 수리) 런타임 `{final['runtime_completed']}/{final['runtime_total']}`, "
        f"tester reached feature_last(테스터 피처 끝 도달) `{final['tester_reached_feature_last']}/{final['tester_gap_total']}`, "
        f"timestamp-aligned proxy/MT5(시점 맞춤 프록시/MT5) `{final['timestamp_aligned_proxy_mt5_matched']}/{final['timestamp_aligned_proxy_mt5_rows']}`.\n"
    )
    if "run337AP_summary(337AP 요약)" in brief:
        brief = re.sub(r"- run337AP_summary\(337AP 요약\): [^\n]*(?:\n|$)", summary, brief, count=1)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(ak.write_text(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = ak.read_text(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AP(337AP 실행) `{final['status']}`. "
        f"Effect(효과): broker history repair(브로커 이력 수리)를 재탐침했고 Forward/Goal(전진/목표)은 주장하지 않음.\n"
    )
    pattern = rf"^- {re.escape(TODAY)}: Stage337 run337AP\(337AP 실행\).*$"
    if re.search(pattern, changelog, flags=re.MULTILINE):
        changelog = re.sub(pattern, line.rstrip(), changelog, flags=re.MULTILINE)
    else:
        changelog = changelog.rstrip() + "\n" + line
    artifacts.append(ak.write_text(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "broker_history_repair_reprobe",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_parity_repair",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__broker_history_repair_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "broker_history_repair_reprobe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_probe_no_forward_decision(런타임 탐침, 전진 판정 없음)",
        "tier_scope": "Tier A u42 broker runtime diagnostic(Tier A u42 브로커 런타임 진단)",
        "kpi_scope": "runtime_probe_no_forward_decision",
        "scoreboard_lane": "runtime_parity_repair",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime={final['runtime_completed']}/{final['runtime_total']};gap={final['tester_reached_feature_last']}/{final['tester_gap_total']};proxy={final['timestamp_aligned_proxy_mt5_matched']}/{final['timestamp_aligned_proxy_mt5_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;no_forward_claim",
        "external_verification_status": "completed" if final["runtime_completed"] == final["runtime_total"] and final["runtime_total"] else "blocked_or_incomplete",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "run_key": f"{RUN_ID}__broker_history_repair_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_repair",
        "evidence_scope": "MT5 API warmup, Strategy Tester report, runtime telemetry, proxy/MT5 difference",
        "kpi_scope": "runtime_probe_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;broker_gap={final['broker_gap_status']};db_missing={final['db_missing_required_columns']}",
        "decision": final["decision"],
        "next_action": final["next_action"],
        "ledger_row_id": f"{RUN_ID}__broker_history_repair_reprobe",
        "family": "broker_history_repair_reprobe",
        "question": "does API history warmup or next rollover make broker tester reach feature_last without retuning",
        "metric_scope": "broker_history_repair_proxy_mt5_usability",
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(REPORT_PATH),
    }
    return [
        upsert_csv_fixed_columns(RUN_REGISTRY, ["run_id"], run_row, RUN_REGISTRY_COLUMNS),
        upsert_csv_fixed_columns(ALPHA_LEDGER, ["ledger_row_id"], alpha_row, ALPHA_LEDGER_COLUMNS),
        ak.upsert_csv(STAGE_LEDGER, ["run_key"], stage_row),
    ]


def main() -> int:
    args = parse_args()
    configure_modules()
    terminal_path = Path(args.terminal)
    metaeditor_path = Path(args.metaeditor)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    for directory in (RUN_DIR, MT5_DIR, FEATURE_COPY_DIR, MODEL_COPY_DIR, TELEMETRY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    source_final = ak.read_json(SOURCE_FINAL)
    parent_final = ak.read_json(PARENT_FINAL)
    source = load_source_attempt()
    prepared = build_prepared_attempts(source)
    parent_snapshot = {"source_final": source_final, "parent_final": parent_final, "source_attempt": source}

    pre_terminal_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    cache_before = aj.cache_snapshot_rows(terminal_data_root, "before_api_history_warmup")
    warmup_payload, warmup_rows = ({"status": "not_attempted_materialize_only"}, []) if args.materialize_only else aj.mt5_history_warmup(terminal_path)
    post_warmup_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL) if not args.materialize_only else {"status": "not_attempted_materialize_only"}
    post_broker_api_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    cache_after = aj.cache_snapshot_rows(terminal_data_root, "after_api_history_warmup")

    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, common_files_root)
    scenario_by_attempt = {str(row["attempt_name"]): row for row in prepared}
    rewritten: list[dict[str, Any]] = []
    for attempt in attempts:
        scenario = scenario_by_attempt[str(attempt["attempt_name"])]
        for key in ("scenario_id", "scenario_symbol", "scenario_from_date", "scenario_to_date", "scenario_model"):
            attempt[key] = scenario[key]
        rewritten.append(rewrite_attempt_to_scenario(dict(attempt)))
    attempts = rewritten

    before_offsets = qprobe.log_offsets([TESTER_LOG, TESTER_AGENT_LOG, TERMINAL_LOG])
    if args.materialize_only:
        execution_result: dict[str, Any] = {"compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "materialize_only": True}
    else:
        execution_result = base.execute_attempts(
            attempts,
            terminal_path=terminal_path,
            metaeditor_path=metaeditor_path,
            common_files_root=common_files_root,
            tester_profile_root=tester_profile_root,
            terminal_data_root=terminal_data_root,
            timeout_seconds=args.timeout_seconds,
            wait_timeout_seconds=args.wait_timeout_seconds,
            materialize_only=False,
        )

    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    copied_runtime_artifacts = base.copy_runtime_outputs(common_files_root, attempts)
    feature_rows = qprobe.feature_last_rows(attempts)
    boundary_rows = ab.parse_tester_boundary_rows(before_offsets, attempts)
    gap_rows = qprobe.tester_gap_rows(runtime_rows, feature_rows, common_files_root, {"last_close_utc": broker_api.get("m5_last_close_utc", "")})
    proxy_rows = base.build_proxy_signal_expected_rows(attempts)
    raw_diff = sanitize_diff(base.build_signal_difference_rows(proxy_rows, runtime_rows), "stage337AP_full_feature_python_onnx_proxy")
    cutoff_by_attempt = {str(row.get("attempt_name", "")): str(row.get("tester_last_observed_bar_time", "")) for row in gap_rows}
    aligned_proxy_rows = qprobe.build_timestamp_aligned_proxy_rows(attempts, cutoff_by_attempt)
    aligned_diff = sanitize_diff(base.build_signal_difference_rows(aligned_proxy_rows, runtime_rows), "stage337AP_timestamp_aligned_python_onnx_proxy")
    usability = proxy_usability_rows(gap_rows, raw_diff, aligned_diff, parent_final)
    status, judgment, decision, next_action = classify(runtime_rows, gap_rows, aligned_diff, bool(args.materialize_only))
    final = final_payload(status, judgment, decision, next_action, broker_api, warmup_payload, runtime_rows, gap_rows, raw_diff, aligned_diff, parent_final)
    gates = gate_rows(final, warmup_rows, handoff_rows)

    artifacts: list[Path] = [
        ak.write_json(RUN_DIR / "parent_evidence_snapshot.json", parent_snapshot),
        ak.write_json(RUN_DIR / "pre_terminal_recovery.json", pre_terminal_recovery),
        ak.write_json(RUN_DIR / "api_history_warmup.json", warmup_payload),
        ak.write_csv(RUN_DIR / "api_history_warmup.csv", ak.columns_for(warmup_rows, ["status"]), warmup_rows),
        ak.write_json(RUN_DIR / "post_warmup_terminal_recovery.json", post_warmup_recovery),
        ak.write_json(RUN_DIR / "broker_api_visibility.json", broker_api),
        ak.write_json(RUN_DIR / "post_broker_api_terminal_recovery.json", post_broker_api_recovery),
        ak.write_csv(RUN_DIR / "history_cache_snapshot_before.csv", ak.columns_for(cache_before, ["status"]), cache_before),
        ak.write_csv(RUN_DIR / "history_cache_snapshot_after.csv", ak.columns_for(cache_after, ["status"]), cache_after),
        ak.write_csv(RUN_DIR / "handoff_attempts.csv", ak.columns_for(handoff_rows, ["attempt_name"]), handoff_rows),
        ak.write_json(RUN_DIR / "handoff_attempts.json", attempts),
        ak.write_json(RUN_DIR / "execution_result.json", execution_result),
        ak.write_csv(RUN_DIR / "runtime_summary.csv", ak.columns_for(runtime_rows, ["attempt_name"]), runtime_rows),
        ak.write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", ak.columns_for(feature_rows, ["attempt_name"]), feature_rows),
        ak.write_csv(RUN_DIR / "tester_boundary_history_repair.csv", ak.columns_for(boundary_rows, ["attempt_name"]), boundary_rows),
        ak.write_csv(RUN_DIR / "tester_feature_last_gap_history_repair.csv", ak.columns_for(gap_rows, ["attempt_name"]), gap_rows),
        ak.write_csv(RUN_DIR / "proxy_expected_result.csv", ak.columns_for(proxy_rows, ["attempt_name"]), proxy_rows),
        ak.write_csv(RUN_DIR / "proxy_mt5_difference.csv", ak.columns_for(raw_diff, ["attempt_name"]), raw_diff),
        ak.write_csv(RUN_DIR / "timestamp_aligned_proxy_expected_result.csv", ak.columns_for(aligned_proxy_rows, ["attempt_name"]), aligned_proxy_rows),
        ak.write_csv(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv", ak.columns_for(aligned_diff, ["attempt_name"]), aligned_diff),
        ak.write_csv(RUN_DIR / "proxy_mt5_usability_history_repair.csv", ak.columns_for(usability, ["attempt_name"]), usability),
        ak.write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ak.columns_for(gates, ["gate_id"]), gates),
        ak.write_json(RUN_DIR / "final_decision.json", final),
        ak.write_md(REPORT_PATH, report_text(final, usability)),
        ak.write_md(DECISION_DOC, decision_doc_text(final)),
        *materialized_artifacts,
        *copied_runtime_artifacts,
    ]
    for path, payload in receipt_payloads(final, attempts, runtime_rows).items():
        artifacts.append(ak.write_json(path, payload))
    artifacts.extend(update_status_docs(final))
    artifacts.extend(update_registers(final))
    manifest = ak.write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/reprobe_broker_history_repair_or_next_rollover.py",
            "materialize_only": bool(args.materialize_only),
            "primary_family": "runtime_parity_repair",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-backtest-forensics", "obsidian-result-judgment", "obsidian-data-integrity"],
            "artifacts": [rel(path) for path in artifacts if path_exists(path)],
        },
    )
    artifacts.append(manifest)
    artifacts.append(ak.append_artifacts([*artifacts, Path(__file__)], final))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
