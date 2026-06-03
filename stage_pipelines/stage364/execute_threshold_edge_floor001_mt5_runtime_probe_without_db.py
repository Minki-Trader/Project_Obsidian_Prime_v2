from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage364 import execute_density_side_balance_repair_mt5_runtime_probe_without_db as core  # noqa: E402
from stage_pipelines.stage364 import package_threshold_edge_floor001_runtime_probe_without_db as pkg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364AV"
RUN_ID = "run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364AW_review_threshold_edge_floor001_mt5_runtime_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage364AV_threshold_edge_floor001_mt5_runtime_probe_executed_review_required_no_authority"
STATUS_BLOCKED = "blocked_stage364AV_threshold_edge_floor001_mt5_runtime_probe_attempt_recorded_repair_required_no_authority"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_outputs_missing_or_failed_repair_required_no_authority"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "threshold_edge_floor001_mt5_probe_summary.csv"
PROBABILITY_DIFF = RUN_DIR / "probability_runtime_difference.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AV_threshold_edge_floor001_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AV_threshold_edge_floor001_mt5_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    pkg.FINAL_DECISION,
    pkg.GATE_AUDIT,
    pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    pkg.TESTER_SET_MANIFEST,
    pkg.TESTER_INI_MANIFEST,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.COMMON_FILES_SYNC,
    pkg.SOURCE_PROBABILITY_TAPE,
    pkg.SOURCE_SELECTED_TRADE_TAPE,
    pkg.SOURCE_FEATURE_MATRIX,
    pkg.SOURCE_ONNX,
    pkg.PORTABLE_EA_EX5,
]

OUTPUT_FILES = [
    ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROBABILITY_DIFF,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
    EXPECTED_KPI_SUMMARY,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return str(io_path(Path(path)))


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    return sha256_file(Path(path))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    _, rows = pkg.read_csv_rows(path)
    return rows


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def float_or_nan(value: Any) -> float:
    try:
        if value in ("", None):
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def finite(value: Any, digits: int = 10) -> float | str:
    number = float_or_nan(value)
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def configure_core() -> None:
    replacements = {
        "pkg": pkg,
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS_COMPLETED": STATUS_COMPLETED,
        "STATUS_BLOCKED": STATUS_BLOCKED,
        "JUDGMENT_COMPLETED": JUDGMENT_COMPLETED,
        "JUDGMENT_BLOCKED": JUDGMENT_BLOCKED,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "STAGE_DIR": STAGE_DIR,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "TELEMETRY_COPY_DIR": TELEMETRY_COPY_DIR,
        "REPORT_COPY_DIR": REPORT_COPY_DIR,
        "REVIEW_DIR": REVIEW_DIR,
        "SPEC_DIR": SPEC_DIR,
        "SELECTED_DIR": SELECTED_DIR,
        "ATTEMPT_PACKAGE": ATTEMPT_PACKAGE,
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "EXECUTION_SUMMARY": EXECUTION_SUMMARY,
        "PROBABILITY_DIFF": PROBABILITY_DIFF,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "TELEMETRY_SKIP_SUMMARY": TELEMETRY_SKIP_SUMMARY,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
        "EXPECTED_KPI_SUMMARY": EXPECTED_KPI_SUMMARY,
        "BACKTEST_RECEIPT": BACKTEST_RECEIPT,
        "RUNTIME_RECEIPT": RUNTIME_RECEIPT,
        "PERFORMANCE_RECEIPT": PERFORMANCE_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "CLAIM_RECEIPT": CLAIM_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "REVIEW_INDEX": REVIEW_INDEX,
        "STAGE_LEDGER": STAGE_LEDGER,
        "STAGE_BRIEF": STAGE_BRIEF,
        "SELECTION_STATUS": SELECTION_STATUS,
        "STAGE_README": STAGE_README,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_WORKING_STATE": CURRENT_WORKING_STATE,
        "WORKSPACE_CHANGELOG": WORKSPACE_CHANGELOG,
        "RUN_REGISTRY": RUN_REGISTRY,
        "PROJECT_LEDGER": PROJECT_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "IDEA_REGISTRY": IDEA_REGISTRY,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
    }
    for name, value in replacements.items():
        setattr(core, name, value)
    core.fs_path = fs_path
    core.exists = exists
    core.sha = sha
    core.expected_probability_map = expected_probability_map


def terminal_defaults() -> tuple[Path, Path, Path, Path]:
    base = pkg.basepkg.basepkg
    return (
        base.DEFAULT_TERMINAL,
        base.DEFAULT_COMMON_FILES,
        base.DEFAULT_TESTER_PROFILE_ROOT,
        base.DEFAULT_PORTABLE_ROOT,
    )


def parse_args() -> argparse.Namespace:
    terminal, common_files, tester_profile, terminal_data = terminal_defaults()
    parser = argparse.ArgumentParser(description="Stage364AV threshold-edge floor001 MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(terminal))
    parser.add_argument("--common-files-root", default=str(common_files))
    parser.add_argument("--tester-profile-root", default=str(tester_profile))
    parser.add_argument("--terminal-data-root", default=str(terminal_data))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    return parser.parse_args()


def runtime_policy() -> dict[str, Any]:
    policy = read_json(pkg.RUNTIME_POLICY_CONFIG)
    return dict(policy.get("decision_surface", {}))


def expected_policy_decision(row: Mapping[str, Any], policy: Mapping[str, Any]) -> tuple[str, str]:
    p_short = float_or_nan(row.get("p_short"))
    p_flat = float_or_nan(row.get("p_flat"))
    p_long = float_or_nan(row.get("p_long"))
    if not all(math.isfinite(value) for value in [p_short, p_flat, p_long]):
        return "flat", "probability_invalid"

    short_threshold = float(policy.get("InpShortThreshold", 0.455))
    long_threshold = float(policy.get("InpLongThreshold", 0.0))
    min_margin = float(policy.get("InpMinMargin", -0.000562137088))
    short_margin = p_short - max(p_flat, p_long)
    long_margin = p_long - max(p_flat, p_short)
    short_ok = p_short >= short_threshold and short_margin >= min_margin
    long_ok = p_long >= long_threshold and long_margin >= min_margin

    if long_ok and (not short_ok or p_long >= p_short):
        signal = "long"
        reason = "long_threshold_met"
    elif short_ok:
        signal = "short"
        reason = "short_threshold_met"
    else:
        return "flat", "threshold_or_margin_not_met"

    adx_value = float_or_nan(row.get("adx_14"))
    if (
        signal == "long"
        and str(policy.get("InpSideFilterEnabled", "")).lower() == "true"
        and str(policy.get("InpBlockLongFeatureRange", "")).lower() == "true"
        and math.isfinite(adx_value)
        and float(policy.get("InpBlockLongFeatureMin", 40.0)) <= adx_value <= float(policy.get("InpBlockLongFeatureMax", 1000000.0))
    ):
        return "flat", f"side_filter_block_long_feature_range|{reason}"

    timestamp = pd.to_datetime(row.get("bar_time_server"), errors="coerce")
    if pd.isna(timestamp):
        return signal, reason
    hour = int(timestamp.hour)
    month = int(timestamp.month)

    if str(policy.get("InpMarchNonHour16MarginFilter", "")).lower() == "true" and month == int(policy.get("InpMarchFilterMonth", 3)):
        abs_margin = max(abs(short_margin), abs(long_margin))
        blocked_hour = int(policy.get("InpMarchFilterBlockedHour", 16))
        min_abs_margin = float(policy.get("InpMarchFilterAbsMarginMin", 0.1))
        if hour == blocked_hour or abs_margin < min_abs_margin:
            return "flat", f"march_non_hour16_margin_filter|{reason}"

    entry_margin_floor = float(policy.get("InpEntryMarginFloor", 0.0))
    if entry_margin_floor > 0.0:
        side_margin = short_margin if signal == "short" else long_margin
        if side_margin < entry_margin_floor:
            return "flat", f"entry_margin_floor|{reason}"

    if (
        signal == "short"
        and str(policy.get("InpBlockPremarketShort", "")).lower() == "true"
        and int(policy.get("InpPremarketStartHour", 12)) <= hour < int(policy.get("InpPremarketEndHour", 17))
    ):
        return "flat", f"premarket_short_block|{reason}"

    return signal, reason


def expected_probability_map() -> tuple[dict[str, dict[str, Any]], int]:
    frame = pd.read_csv(io_path(pkg.SOURCE_PROBABILITY_TAPE)).fillna("")
    policy = runtime_policy()
    feature_hashes, feature_duplicates = core.feature_line_hash_map(pkg.SOURCE_FEATURE_MATRIX)
    rows: dict[str, dict[str, Any]] = {}
    duplicates = 0
    for _, source_row in frame.iterrows():
        payload = source_row.to_dict()
        key = core.norm_bar_time(payload.get("bar_time_server"))
        if key in rows:
            duplicates += 1
        signal, reason = expected_policy_decision(payload, policy)
        payload["expected_mql_input_hash"] = feature_hashes.get(key, "")
        payload["mt5_expected_signal"] = signal
        payload["mt5_expected_signal_int"] = {"short": -1, "flat": 0, "long": 1}.get(signal, 0)
        payload["mt5_decision_reason"] = reason
        payload["runtime_policy_source"] = rel(pkg.RUNTIME_POLICY_CONFIG)
        rows[key] = payload
    return rows, duplicates + feature_duplicates


def read_set_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not exists(path):
        return values
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def enrich_attempts(parent: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts = read_csv_rows(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE)
    enriched: list[dict[str, Any]] = []
    for row in attempts:
        attempt = dict(row)
        set_path = ROOT / str(attempt.get("set_path", ""))
        ini_path = ROOT / str(attempt.get("ini_path", ""))
        set_values = read_set_values(set_path)
        ini_values = read_set_values(ini_path)
        attempt["tier"] = str(attempt.get("tier") or "Tier A")
        attempt["split"] = str(attempt.get("split") or "validation_oos")
        attempt["model_id"] = str(parent.get("model_id", pkg.MODEL_ID))
        attempt["variant_id"] = str(parent.get("selected_variant_id", "threshold_edge_floor001_probe"))
        attempt["feature_set_id"] = "stage364AU_threshold_edge_floor001_features"
        attempt["ini_name"] = ini_path.name
        attempt["set_name"] = set_path.name
        attempt["common_telemetry_path"] = str(
            attempt.get("runtime_telemetry_expected", "")
            or set_values.get("InpTelemetryCsvPath", "")
        )
        attempt["common_summary_path"] = str(
            attempt.get("runtime_summary_expected", "")
            or set_values.get("InpSummaryCsvPath", "")
        )
        attempt["report_name"] = str(attempt.get("report_name", "") or ini_values.get("Report", ""))
        attempt["ini"] = {"tester": {"Report": attempt["report_name"]}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
        attempt["execution_run_id"] = RUN_ID
        attempt["parent_package_run_id"] = PARENT_RUN_ID
        attempt["effect"] = "AU package(AU 패키지)를 MT5 runtime probe(MT5 런타임 탐침) 입력으로 고정한다."
        enriched.append(attempt)
    if not enriched:
        raise RuntimeError("runtime_probe_attempt_package(런타임 탐침 시도 패키지)가 비어 있다.")
    write_csv(ATTEMPT_PACKAGE, enriched)
    return enriched


def report_usable_count(report_records: Sequence[Mapping[str, Any]]) -> int:
    return core.report_usable_count(report_records)


def build_final(
    args: argparse.Namespace,
    parent: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    diffs: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed_runtime = sum(1 for row in summaries if row.get("runtime_status") == "completed")
    usable_reports = report_usable_count(report_records)
    total_mismatches = sum(
        int(row.get("expected_missing_rows") or 0)
        + int(row.get("hash_mismatch_rows") or 0)
        + int(row.get("probability_mismatch_rows") or 0)
        + int(row.get("decision_mismatch_rows") or 0)
        for row in summaries
    )
    total_ready = sum(int(row.get("ready_model_rows") or 0) for row in summaries)
    total_matched = sum(int(row.get("matched_rows") or 0) for row in summaries)
    status = STATUS_COMPLETED if completed_runtime > 0 else STATUS_BLOCKED
    judgment = JUDGMENT_COMPLETED if completed_runtime > 0 else JUDGMENT_BLOCKED
    summary = summaries[0] if summaries else {}
    proxy = proxy_rows[0] if proxy_rows else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": f"{RUN_NUMBER}_open_{NEXT_RUN_ID}",
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_count": len(attempts),
        "runtime_completed_rows": completed_runtime,
        "usable_report_rows": usable_reports,
        "ready_model_rows": total_ready,
        "matched_rows": total_matched,
        "mismatch_rows": total_mismatches,
        "probability_diff_rows": len(diffs),
        "runtime_output_copy_rows": len(copy_rows),
        "terminal_path": str(args.terminal_path),
        "common_files_root": str(args.common_files_root),
        "tester_profile_root": str(args.tester_profile_root),
        "terminal_data_root": str(args.terminal_data_root),
        "selected_variant_id": parent.get("selected_variant_id"),
        "expected_net_profit": proxy.get("expected_net_profit", parent.get("expected_combined_net_profit")),
        "actual_mt5_net_profit": proxy.get("actual_mt5_net_profit", summary.get("net_profit", "")),
        "net_profit_diff_actual_minus_expected": proxy.get("net_profit_diff_actual_minus_expected", ""),
        "expected_trade_count": proxy.get("expected_trade_count", parent.get("expected_combined_trade_count")),
        "actual_mt5_trade_count": proxy.get("actual_mt5_trade_count", summary.get("trade_count", "")),
        "trade_count_diff_actual_minus_expected": proxy.get("trade_count_diff_actual_minus_expected", ""),
        "expected_profit_factor": proxy.get("expected_profit_factor", parent.get("expected_combined_profit_factor")),
        "actual_mt5_profit_factor": proxy.get("actual_mt5_profit_factor", summary.get("profit_factor", "")),
        "expected_long_trade_count": proxy.get("expected_long_count", parent.get("expected_combined_long_count")),
        "actual_long_trade_count": proxy.get("actual_long_count", summary.get("long_trade_count", "")),
        "expected_short_trade_count": proxy.get("expected_short_count", parent.get("expected_combined_short_count")),
        "actual_short_trade_count": proxy.get("actual_short_count", summary.get("short_trade_count", "")),
        "report_path": summary.get("report_path", ""),
        "comparison_status": summary.get("comparison_status", ""),
        "mt5_execution": "attempted",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    runtime_ok = int(final.get("runtime_completed_rows") or 0) > 0
    report_ok = int(final.get("usable_report_rows") or 0) > 0
    diff_ready = exists(PROXY_MT5_DIFF)
    gates = [
        ("tester_execution_attempt_gate(테스터 실행 시도 게이트)", True, MT5_EXECUTION_RESULT, "MT5 Strategy Tester(MT5 전략 테스터) 실행 시도를 기록한다."),
        ("runtime_evidence_gate(런타임 근거 게이트)", runtime_ok, RUNTIME_OUTPUT_COPY, "runtime telemetry/summary(런타임 기록/요약) 존재를 확인한다."),
        ("strategy_report_gate(전략 테스터 보고서 게이트)", report_ok, STRATEGY_TESTER_REPORTS, "tester KPI(테스터 핵심 성과 지표) 출처를 고정한다."),
        ("proxy_mt5_diff_gate(프록시 MT5 차이 게이트)", diff_ready, PROXY_MT5_DIFF, "proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리한다."),
        ("runtime_parity_audit(런타임 동등성 감사)", runtime_ok, PROBABILITY_DIFF, "probability/decision parity(확률/결정 동등성)를 측정한다."),
        ("kpi_contract_audit(KPI 계약 감사)", exists(EXPECTED_KPI_SUMMARY), EXPECTED_KPI_SUMMARY, "expected KPI(예상 핵심 성과 지표)를 비교 기준으로 보존한다."),
        ("final_claim_guard(최종 주장 가드)", True, CLAIM_RECEIPT, "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않는다."),
        ("required_gate_coverage_audit(필수 게이트 커버리지 감사)", runtime_ok and report_ok and diff_ready, GATE_AUDIT, "runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate(게이트)": name,
            "status": "passed" if passed else "blocked",
            "evidence(근거)": rel(path),
            "effect(효과)": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, passed, path, effect in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "ea_identity": pkg.mt5_runtime_module_hashes(),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "broker-native tester output(브로커 네이티브 테스터 출력)에서 확인한다.",
            "forensic_checks": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)" if int(final.get("usable_report_rows") or 0) else "blocked_or_inconclusive(차단 또는 불충분)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.SOURCE_SELECTED_TRADE_TAPE),
            "runtime_path": rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "MT5 tester(테스터) 비용/체결 의미는 proxy(프록시)와 다를 수 있다.",
            "parity_check": rel(PROBABILITY_DIFF),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침), not authority(권위 아님)",
        },
    )
    write_json(PERFORMANCE_RECEIPT, {**base, "expected_vs_actual": rel(PROXY_MT5_DIFF), "judgment": final["judgment"]})
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF), rel(PROBABILITY_DIFF)],
            "evidence_missing": ["review closeout(검토 종료)", "forward pass(전진 통과)", "runtime authority audit(런타임 권위 감사)"],
            "judgment_label": final["judgment"],
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "attempted",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "MT5 runtime probe(MT5 런타임 탐침)를 operating claim(운영 주장)으로 승격하지 않는다.",
        },
    )
    write_csv(
        RUNTIME_IDENTITY,
        [
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "attempt_count": final["attempt_count"],
                "terminal_path": final["terminal_path"],
                "selected_variant_id": final.get("selected_variant_id", ""),
                "source_package": rel(pkg.FINAL_DECISION),
                "runtime_module_hash_count": len(pkg.mt5_runtime_module_hashes()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def sync_stage_brief_header(final: Mapping[str, Any]) -> None:
    if not exists(STAGE_BRIEF):
        return
    text = io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig")
    replacements = {
        "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{final['status']}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        replacement = next((value for prefix, value in replacements.items() if stripped.startswith(prefix)), None)
        lines.append(replacement if replacement is not None else line)
    write_text(STAGE_BRIEF, "\n".join(lines).rstrip() + "\n", bom=True)


def write_docs(final: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364AV threshold edge floor001 MT5 runtime probe(364AV 임계값 경계 하한 0.001 MT5 런타임 탐침)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{final["status"]}`
- judgment(판정): `{final["judgment"]}`
- gates(게이트): `{final["gate_passes"]}/{final["gate_total"]}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`

## Action/Effect(행동/효과)

Action(행동): run364AU package(364AU 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry/report(런타임 기록/보고서)를 수집했다.

Effect(효과): proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)의 diff(차이)를 review(검토) 가능한 산출물로 만들었다.

## Execution summary(실행 요약)

{markdown_table(summaries, ["attempt_name", "tester_status", "runtime_status", "report_status", "net_profit", "profit_factor", "trade_count", "long_trade_count", "short_trade_count", "ready_model_rows", "matched_rows", "mismatch_rows", "comparison_status"])}

## Proxy vs MT5(프록시 대 MT5)

{markdown_table(proxy_rows, ["attempt_name", "expected_net_profit", "actual_mt5_net_profit", "net_profit_diff_actual_minus_expected", "expected_trade_count", "actual_mt5_trade_count", "trade_count_diff_actual_minus_expected", "expected_profit_factor", "actual_mt5_profit_factor", "report_status", "comparison_status"])}

## Gates(게이트)

{markdown_table(gates, ["gate(게이트)", "status", "evidence(근거)", "effect(효과)"])}

## Boundary(경계)

이 run(실행)은 runtime_probe(런타임 탐침)다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, report, bom=True)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364AV(364AV 실행)는 run364AU package(364AU 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도했다. runtime_completed_rows(런타임 완료 행)는 `{final["runtime_completed_rows"]}`, usable_report_rows(사용 가능 보고서 행)는 `{final["usable_report_rows"]}`, actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수)는 `{final["actual_mt5_net_profit"]}` / `{final["actual_mt5_profit_factor"]}` / `{final["actual_mt5_trade_count"]}`이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 proxy/MT5 diff(프록시/MT5 차이), cost stress(비용 압박), side balance(방향 균형), session/regime stability(세션/국면 안정성)를 review(검토)한다.
""",
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final["status"]}
current_judgment: {final["judgment"]}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final["created_at_utc"]}
""",
        bom=False,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): not_claimed(주장 없음)
- runtime_probe_candidate(런타임 탐침 후보): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`
- latest_mt5_probe(최근 MT5 탐침): `{RUN_ID}`
- actual_mt5_net_pf_trades(실제 MT5 순수익/수익 팩터/거래수): `{final["actual_mt5_net_profit"]}` / `{final["actual_mt5_profit_factor"]}` / `{final["actual_mt5_trade_count"]}`
- proxy_mt5_diff(프록시 MT5 차이): `{final["net_profit_diff_actual_minus_expected"]}` net(순수익), `{final["trade_count_diff_actual_minus_expected"]}` trades(거래수)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - MT5 runtime probe(MT5 런타임 탐침), authority(권위) not_claimed(주장 없음).")
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""## {RUN_ID}

Action(행동): threshold edge floor001 package(임계값 경계 하한 0.001 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도했다.

Effect(효과): proxy/MT5 diff(프록시/MT5 차이)와 runtime parity(런타임 동등성) review(검토) 입력을 만들었다. operating promotion(운영 승격)과 runtime authority(런타임 권위)는 없다.
""",
    )
    sync_stage_brief_header(final)
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364AV Threshold Edge Floor001 MT5 Runtime Probe(364AV 임계값 경계 하한 0.001 MT5 런타임 탐침)

Action(행동): run364AU package(364AU 패키지)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.

Effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 `{NEXT_RUN_ID}` review(검토)로 이어간다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} - {RUN_ID}

- action(행동): threshold edge floor001 MT5 runtime probe(임계값 경계 하한 0.001 MT5 런타임 탐침)를 실행 시도했다.
- effect(효과): runtime telemetry(런타임 기록), strategy tester report(전략 테스터 보고서), proxy/MT5 diff(프록시/MT5 차이)를 기록했다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)의 PF lift(PF 개선)를 MT5 runtime(MT5 런타임)에서 확인한다.
- evidence(근거): `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`, `{rel(PROBABILITY_DIFF)}`
- boundary(경계): runtime authority(런타임 권위)는 not_claimed(주장 없음).
""",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for row in gate_rows(final) if row["status"] == "passed")
    gate_total = len(gate_rows(final))
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "mt5_runtime_probe_attempted(MT5 런타임 탐침 시도)",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["ready_model_rows"],
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(EXECUTION_SUMMARY),
        "result_status": final["status"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "runtime_backtest(런타임 백테스트)",
        "trade_density_requirement_status": "requires_review_from_mt5_trade_count(실제 MT5 거래수 기준 검토 필요)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "attempt_rows": final["attempt_count"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "net_profit": final["actual_mt5_net_profit"],
        "profit_factor": final["actual_mt5_profit_factor"],
        "trade_count": final["actual_mt5_trade_count"],
        "long_trade_count": final["actual_long_trade_count"],
        "short_trade_count": final["actual_short_trade_count"],
        "evidence_scope": "mt5_runtime_probe_no_authority(MT5 런타임 탐침, 권위 없음)",
    }
    run_row = {**common, "subrun_id": "", "lane": "runtime_probe(MT5 런타임 탐침)"}
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=True)

    ledger_rows = []
    for suffix, view, tier, kpi_scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "mt5_runtime_probe_actual(MT5 런타임 탐침 실제)"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)"),
        ("Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "actual_routed_total_same_as_tier_a_no_tier_b_fallback(실제 라우팅 전체, Tier A와 동일)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": kpi_scope,
            }
        )
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("execution_summary", EXECUTION_SUMMARY, "MT5 runtime probe summary(MT5 런타임 탐침 요약)."),
        ("probability_diff", PROBABILITY_DIFF, "Probability runtime diff(확률 런타임 차이)."),
        ("proxy_mt5_diff", PROXY_MT5_DIFF, "Proxy-vs-MT5 diff(프록시 대 MT5 차이)."),
        ("strategy_tester_reports", STRATEGY_TESTER_REPORTS, "Strategy tester report records(전략 테스터 보고서 기록)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
    ]:
        if exists(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
                    "created_at_utc": final["created_at_utc"],
                    "notes": notes,
                    "artifact_path": rel(path),
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES if exists(path)],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    configure_core()
    args = parse_args()
    core.ensure_dirs()
    parent = core.validate_parent()
    attempts = enrich_attempts(parent)
    execution_results, report_records, copy_rows, _ = core.execute_attempts(args, attempts)
    summaries, diffs, _skips, proxy_rows = core.compare_outputs(attempts, execution_results, report_records)
    final = build_final(args, parent, attempts, execution_results, report_records, summaries, diffs, copy_rows, proxy_rows)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_receipts(final)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_docs(final, summaries, proxy_rows, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    repair_run_registry_line_endings(RUN_ID)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
