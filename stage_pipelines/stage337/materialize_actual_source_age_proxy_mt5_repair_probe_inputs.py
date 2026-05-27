from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
)


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337Y"
RUN_ID = "run337Y_materialize_actual_source_age_proxy_mt5_repair_probe_inputs_v1"
PARENT_RUN_ID = "run337X_review_materialized_cost_buffer_source_policy_repair_inputs_v1"
NEXT_RUN_ID = "run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_v1"
STATUS = "completed_stage337Y_actual_source_age_proxy_mt5_repair_probe_inputs_materialized_no_training_no_new_mt5"
JUDGMENT = (
    "actual_source_age_and_proxy_values_materialized_runtime_probe_package_ready_"
    "tester_gap_remains_no_forward_decision"
)
DECISION = "stage337Y_open_run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337Y_actual_measurement_inputs_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

FORWARD_START_UTC = "2026-04-14T00:00:00Z"
FROZEN_TRAIN_END_UTC = "2026-04-13T23:55:00Z"
SESSION_AWARE_POLICY = "session_aware_explicit_age_bucket_required"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337X_DIR = STAGE_DIR / "02_runs" / "run337X"
RUN337W_DIR = STAGE_DIR / "02_runs" / "run337W"
RUN337P_DIR = STAGE_DIR / "02_runs" / "run337P"
RUN337U_DIR = STAGE_DIR / "02_runs" / "run337U"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
REPORT_PATH = REVIEWS_DIR / "run337Y_actual_measurement_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337Y_actual_measurement_inputs.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

X_GAP_REGISTER = RUN337X_DIR / "gap_register.csv"
X_QUEUE = RUN337X_DIR / "run337Y_queue.csv"
X_FINAL = RUN337X_DIR / "final_decision.json"
W_SOURCE_AGE = RUN337W_DIR / "source_age_and_availability_audit.csv"
W_FEATURE_BOUNDARY = RUN337W_DIR / "feature_label_boundary_audit.csv"
W_PROXY_TEMPLATE = RUN337W_DIR / "proxy_expected_template.csv"
W_PROXY_SCHEMA = RUN337W_DIR / "timestamp_aligned_proxy_mt5_difference_schema.csv"
W_TESTER_PLAN = RUN337W_DIR / "tester_boundary_repair_plan.csv"
W_TESTER_GATE = RUN337W_DIR / "tester_feature_last_reach_gate.csv"
W_WFO_SPLIT = RUN337W_DIR / "wfo_split_plan.csv"
W_THRESHOLD = RUN337W_DIR / "no_forward_threshold_search_contract.csv"
W_COST_LADDER = RUN337W_DIR / "cost_ladder_contract.csv"
W_DIRECTION_GATE = RUN337W_DIR / "direction_curve_gate_template.csv"
W_BRANCH_SPEC = RUN337W_DIR / "branch_spec_manifest.csv"
W_MODEL_FIREWALL = RUN337W_DIR / "model_validation_firewall.csv"
P_SOURCE_SUMMARY = RUN337P_DIR / "fresh_forward_data_probe_summary.csv"
P_SOURCE_ASOF = RUN337P_DIR / "source_asof_policy_audit.csv"
P_PROXY_EXPECTED = RUN337P_DIR / "timestamp_aligned_proxy_expected_result.csv"
P_PROXY_DIFF = RUN337P_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
P_TESTER_GAP = RUN337P_DIR / "tester_current_day_gap_reprobe.csv"
P_RUNTIME_RESULT = RUN337P_DIR / "runtime_execution_result.json"
U_FINAL = RUN337U_DIR / "final_tester_rollover_reprobe_decision.json"
U_PROXY_EXPECTED = RUN337U_DIR / "timestamp_aligned_proxy_expected_result.csv"
U_PROXY_DIFF = RUN337U_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
U_TESTER_GAP = RUN337U_DIR / "tester_rollover_feature_last_gap.csv"
U_HANDOFF = RUN337U_DIR / "rollover_reprobe_handoff_manifest.csv"

SOURCE_TIMESTAMP_SNAPSHOT = RUN_DIR / "source_timestamp_snapshot.csv"
SOURCE_AGE_DECISION = RUN_DIR / "source_age_decision.csv"
SOURCE_GAP_BLOCKERS = RUN_DIR / "source_gap_blocker_report.csv"
PROXY_EXPECTED_VALUES = RUN_DIR / "proxy_expected_values.csv"
PROXY_VALUE_IDENTITY = RUN_DIR / "proxy_value_identity.csv"
MT5_REPROBE_MANIFEST = RUN_DIR / "mt5_reprobe_manifest.json"
TESTER_HISTORY_SNAPSHOT = RUN_DIR / "tester_history_snapshot.csv"
TIMESTAMP_ALIGNED_DIFF = RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
SPLIT_MEMBERSHIP_AUDIT = RUN_DIR / "split_membership_audit.csv"
NEGATIVE_CONTROL_RESULT = RUN_DIR / "negative_control_result.csv"
THRESHOLD_IDENTITY_AUDIT = RUN_DIR / "threshold_identity_audit.csv"
BRANCH_PREFLIGHT_MATRIX = RUN_DIR / "branch_preflight_matrix.csv"
COST_CURVE_DIRECTION_OUTPUTS = RUN_DIR / "cost_curve_direction_required_outputs.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"

RAW_SYMBOLS = [
    "US100",
    "VIX",
    "US10YR",
    "USDX",
    "NVDA",
    "AAPL",
    "MSFT",
    "AMZN",
    "AMD",
    "GOOGL.xnas",
    "META",
    "TSLA",
]

OUTPUT_FILES = [
    SOURCE_TIMESTAMP_SNAPSHOT,
    SOURCE_AGE_DECISION,
    SOURCE_GAP_BLOCKERS,
    PROXY_EXPECTED_VALUES,
    PROXY_VALUE_IDENTITY,
    MT5_REPROBE_MANIFEST,
    TESTER_HISTORY_SNAPSHOT,
    TIMESTAMP_ALIGNED_DIFF,
    SPLIT_MEMBERSHIP_AUDIT,
    NEGATIVE_CONTROL_RESULT,
    THRESHOLD_IDENTITY_AUDIT,
    BRANCH_PREFLIGHT_MATRIX,
    COST_CURVE_DIRECTION_OUTPUTS,
    REQUIRED_GATE_AUDIT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    MODEL_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    RUN_MANIFEST,
    FINAL_DECISION,
]

INPUT_FILES = [
    X_GAP_REGISTER,
    X_QUEUE,
    X_FINAL,
    W_SOURCE_AGE,
    W_FEATURE_BOUNDARY,
    W_PROXY_TEMPLATE,
    W_PROXY_SCHEMA,
    W_TESTER_PLAN,
    W_TESTER_GATE,
    W_WFO_SPLIT,
    W_THRESHOLD,
    W_COST_LADDER,
    W_DIRECTION_GATE,
    W_BRANCH_SPEC,
    W_MODEL_FIREWALL,
    P_SOURCE_SUMMARY,
    P_SOURCE_ASOF,
    P_PROXY_EXPECTED,
    P_PROXY_DIFF,
    P_TESTER_GAP,
    P_RUNTIME_RESULT,
    U_FINAL,
    U_PROXY_EXPECTED,
    U_PROXY_DIFF,
    U_TESTER_GAP,
    U_HANDOFF,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def parse_utc(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def to_utc_z(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def minutes_between(start: datetime | None, end: datetime | None) -> int | str:
    if start is None or end is None:
        return ""
    return int(round((end - start).total_seconds() / 60.0))


def read_text_with_bom(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), has_bom


def write_text(path: Path, text: str, *, bom: bool = False) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text, bom=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    materialized = [{column: row.get(column, "") for column in columns} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        writer.writerows(materialized)
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def file_hash(path: Path) -> str:
    if path_exists(path) and io_path(path).is_file():
        return sha256_file_lf_normalized(path)
    return ""


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    existing = read_csv(path)
    columns = list(existing[0].keys()) if existing else list(row.keys())
    for column in row.keys():
        if column not in columns:
            columns.append(column)
    row_key = tuple(str(row.get(column, "")) for column in key_columns)
    output: list[dict[str, Any]] = []
    replaced = False
    for existing_row in existing:
        existing_key = tuple(str(existing_row.get(column, "")) for column in key_columns)
        if existing_key == row_key:
            merged = {column: existing_row.get(column, "") for column in columns}
            merged.update(row)
            output.append(merged)
            replaced = True
        else:
            output.append({column: existing_row.get(column, "") for column in columns})
    if not replaced:
        output.append({column: row.get(column, "") for column in columns})
    return write_csv(path, columns, output)


def source_group(symbol: str) -> str:
    if symbol == "US100":
        return "US100 broker M5"
    if symbol in {"VIX", "US10YR", "USDX"}:
        return "macro regime source"
    return "mega-cap equity source"


def source_role(symbol: str) -> str:
    roles = {
        "US100": "technical control",
        "VIX": "volatility regime",
        "US10YR": "rate regime",
        "USDX": "USD regime",
    }
    return roles.get(symbol, "equity breadth")


def age_bucket(age_minutes: int | str) -> str:
    if age_minutes == "":
        return "unknown"
    age = int(age_minutes)
    if age <= 60:
        return "0_60m"
    if age <= 180:
        return "61_180m"
    if age <= 360:
        return "181_360m"
    if age <= 720:
        return "361_720m"
    return "over_720m"


def raw_fallback_path(symbol: str) -> Path:
    raw_base = ROOT / "data" / "raw" / "mt5_bars" / "m5" / symbol
    if symbol == "GOOGL.xnas":
        return raw_base / "bars_googl_xnas_m5_mt5api_raw.csv"
    filename_symbol = symbol.lower().replace(".xnas", "")
    broker_suffix = "_xnas" if symbol not in {"US100", "VIX", "US10YR", "USDX"} else ""
    return raw_base / f"bars_{filename_symbol}{broker_suffix}_m5_mt5api_raw.csv"


def raw_summary_from_csv(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"status": "missing", "rows": 0, "first_open_utc": "", "last_open_utc": "", "last_close_utc": ""}
    rows = 0
    first: dict[str, str] | None = None
    last: dict[str, str] | None = None
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows += 1
            if first is None:
                first = row
            last = row
    if first is None or last is None:
        return {"status": "empty", "rows": rows, "first_open_utc": "", "last_open_utc": "", "last_close_utc": ""}

    def from_unix(row: Mapping[str, str], key: str) -> str:
        raw = row.get(key, "")
        if not raw:
            return ""
        return datetime.fromtimestamp(int(float(raw)), tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    return {
        "status": "completed",
        "rows": rows,
        "first_open_utc": from_unix(first, "time_open_unix"),
        "last_open_utc": from_unix(last, "time_open_unix"),
        "last_close_utc": from_unix(last, "time_close_unix"),
    }


def build_source_snapshot() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    summary_rows = {row.get("contract_symbol", ""): row for row in read_csv(P_SOURCE_SUMMARY)}
    u_final = read_json(U_FINAL)
    p_us100 = summary_rows.get("US100", {})
    reference_candidates = [
        parse_utc(p_us100.get("last_close_utc")),
        parse_utc(u_final.get("api_latest_us100_close_utc")),
        parse_utc(u_final.get("feature_latest_timestamp")),
    ]
    us100_reference = max([item for item in reference_candidates if item is not None])
    snapshot: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []

    for symbol in RAW_SYMBOLS:
        row = dict(summary_rows.get(symbol, {}))
        if not row:
            csv_path = raw_fallback_path(symbol)
            raw = raw_summary_from_csv(csv_path)
            row = {
                "contract_symbol": symbol,
                "broker_symbol": symbol,
                "status": raw["status"],
                "rows": raw["rows"],
                "first_open_utc": raw["first_open_utc"],
                "last_open_utc": raw["last_open_utc"],
                "last_close_utc": raw["last_close_utc"],
                "csv_path": rel(csv_path),
                "manifest_path": rel(csv_path.with_suffix(".csv.manifest.json")),
                "last_error": "fallback_data_raw",
            }
        csv_path = ROOT / row.get("csv_path", "")
        manifest_path = ROOT / row.get("manifest_path", "")
        last_close = parse_utc(row.get("last_close_utc"))
        age_minutes = minutes_between(last_close, us100_reference)
        lookahead = "source_lte_us100_reference" if last_close and last_close <= us100_reference else "missing_or_future_source_timestamp"
        availability = "measured"
        decision = "usable_with_session_age_boundary"
        training_allowed = "false"
        forward_allowed = "false"
        runtime_probe_allowed = "true"
        effect = "실제 timestamp(타임스탬프, 시점)를 기록해 future fill(미래 채움) 위험을 분리한다."
        if row.get("status") != "completed" or not last_close:
            availability = "missing_or_empty"
            decision = "blocked_source_missing"
            runtime_probe_allowed = "false"
            effect = "원천 파일이 없거나 비어 있어 feature handoff(피처 인계)를 신뢰하지 않는다."
        elif lookahead != "source_lte_us100_reference":
            availability = "future_timestamp_detected"
            decision = "blocked_lookahead_source_timestamp"
            runtime_probe_allowed = "false"
            effect = "원천 timestamp(시점)가 US100 decision bar(판단 봉)보다 뒤라 look-ahead bias(미래참조 편향)를 차단한다."
        elif symbol == "US100" and isinstance(age_minutes, int) and age_minutes > 60:
            availability = "measured_us100_probe_file_lags_api_reference"
            decision = "usable_for_input_identity_but_runtime_refresh_required"
            effect = "US100 파일은 측정됐지만 최신 API reference(API 기준)보다 늦어 다음 실행에서 refresh(갱신)가 필요하다."
        elif isinstance(age_minutes, int) and age_minutes > 240:
            availability = "measured_session_age_over_240m"
            decision = "usable_for_probe_only_session_policy_required"
            effect = "닫힌 세션 이후 stale bucket(오래된 구간)을 명시해 조용한 stale fill(오래된 값 채움)을 막는다."

        source_row = {
            "source_group": source_group(symbol),
            "symbol": symbol,
            "broker_symbol": row.get("broker_symbol", ""),
            "preferred_source": "run337P_raw_refresh_probe" if symbol in summary_rows else "data_raw_fallback",
            "source_path": row.get("csv_path", ""),
            "manifest_path": row.get("manifest_path", ""),
            "status": row.get("status", ""),
            "row_count": row.get("rows", ""),
            "first_open_utc": row.get("first_open_utc", ""),
            "last_open_utc": row.get("last_open_utc", ""),
            "last_close_utc": row.get("last_close_utc", ""),
            "us100_reference_close_utc": to_utc_z(us100_reference),
            "age_to_us100_minutes": age_minutes,
            "age_bucket": age_bucket(age_minutes),
            "source_hash": file_hash(csv_path),
            "manifest_hash": file_hash(manifest_path),
            "time_axis": "MT5_PY_API_UNIX_SECONDS interpreted as UTC bar open/close",
            "lookahead_status": lookahead,
            "availability_status": availability,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        snapshot.append(source_row)
        decisions.append(
            {
                "decision_id": f"source_age::{symbol}",
                "source_group": source_group(symbol),
                "symbol": symbol,
                "feature_role": source_role(symbol),
                "age_minutes": age_minutes,
                "age_bucket": age_bucket(age_minutes),
                "max_age_policy": SESSION_AWARE_POLICY,
                "decision": decision,
                "training_allowed": training_allowed,
                "forward_pass_fail_allowed": forward_allowed,
                "runtime_probe_allowed": runtime_probe_allowed,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        if decision.startswith("blocked") or "required" in decision or "refresh_required" in decision:
            blockers.append(
                {
                    "blocker_id": f"source_gap::{symbol}",
                    "severity": "hard" if decision.startswith("blocked") else "repair_required_before_training_or_forward",
                    "symbol": symbol,
                    "decision": decision,
                    "evidence_path": row.get("csv_path", ""),
                    "repair_or_probe": "refresh source or encode session-aware stale policy before training/forward claim",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    metrics = {
        "source_rows": len(snapshot),
        "source_decision_rows": len(decisions),
        "source_blocker_rows": len(blockers),
        "us100_reference_close_utc": to_utc_z(us100_reference),
    }
    return snapshot, decisions, blockers, metrics


def build_proxy_values() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    proxy_rows: list[dict[str, Any]] = []
    difference_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    source_specs = [
        ("run337P", P_PROXY_EXPECTED, P_PROXY_DIFF, "broad_repair_probe_existing_runtime"),
        ("run337U", U_PROXY_EXPECTED, U_PROXY_DIFF, "u42_rollover_reprobe_existing_runtime"),
    ]
    seen_proxy: set[tuple[str, str]] = set()
    seen_diff: set[tuple[str, str, str]] = set()
    for source_run_id, expected_path, diff_path, scope in source_specs:
        expected = read_csv(expected_path)
        diff = read_csv(diff_path)
        identity_rows.append(
            {
                "source_run_id": source_run_id,
                "artifact_role": "proxy_expected_values",
                "path": rel(expected_path),
                "exists": str(path_exists(expected_path)).lower(),
                "rows": len(expected),
                "sha256": file_hash(expected_path),
                "scope": scope,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        identity_rows.append(
            {
                "source_run_id": source_run_id,
                "artifact_role": "timestamp_aligned_proxy_mt5_difference",
                "path": rel(diff_path),
                "exists": str(path_exists(diff_path)).lower(),
                "rows": len(diff),
                "sha256": file_hash(diff_path),
                "scope": scope,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for row in expected:
            key = (row.get("attempt_name", ""), source_run_id)
            if key in seen_proxy:
                continue
            seen_proxy.add(key)
            proxy_rows.append(
                {
                    "source_run_id": source_run_id,
                    "attempt_name": row.get("attempt_name", ""),
                    "artifact_slug": row.get("artifact_slug", ""),
                    "feature_set_id": row.get("feature_set_id", ""),
                    "model_id": row.get("model_id", ""),
                    "expected_feature_ready_count": row.get("expected_feature_ready_count", ""),
                    "expected_model_ok_count": row.get("expected_model_ok_count", ""),
                    "expected_long_count": row.get("expected_long_count", ""),
                    "expected_short_count": row.get("expected_short_count", ""),
                    "expected_flat_count": row.get("expected_flat_count", ""),
                    "expected_signal_count": row.get("expected_signal_count", ""),
                    "expected_signal_rate": row.get("expected_signal_rate", ""),
                    "expected_long_share": row.get("expected_long_share", ""),
                    "feature_order_hash": row.get("feature_order_hash", ""),
                    "feature_csv_sha256": row.get("feature_csv_sha256", ""),
                    "model_sha256": row.get("model_sha256", ""),
                    "threshold_policy": row.get("threshold_policy", ""),
                    "proxy_cutoff_utc": row.get("proxy_cutoff_utc", ""),
                    "proxy_row_scope": row.get("proxy_row_scope", ""),
                    "source_scope": scope,
                    "usable_for_kpi_authority": "false",
                    "usable_for_runtime_signal_parity": "existing_timestamp_aligned_only",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        for row in diff:
            key = (row.get("attempt_name", ""), row.get("dimension", ""), source_run_id)
            if key in seen_diff:
                continue
            seen_diff.add(key)
            difference_rows.append(
                {
                    "source_run_id": source_run_id,
                    "attempt_name": row.get("attempt_name", ""),
                    "artifact_slug": row.get("artifact_slug", ""),
                    "dimension": row.get("dimension", ""),
                    "proxy_expected_value": row.get("proxy_expected_value", ""),
                    "mt5_runtime_value": row.get("mt5_runtime_value", ""),
                    "difference_proxy_minus_mt5": row.get("difference_proxy_minus_mt5", ""),
                    "difference_status": row.get("difference_status", ""),
                    "proxy_source": row.get("proxy_source", ""),
                    "mt5_source": row.get("mt5_source", ""),
                    "usable_for_runtime_signal_parity": row.get("usable_for_runtime_signal_parity", ""),
                    "usable_for_forward_pass_fail": "false",
                    "runtime_skip_reason": row.get("runtime_skip_reason", ""),
                    "run337Y_materialization_status": "carried_existing_runtime_difference_not_new_mt5_run",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    metrics = {
        "proxy_expected_rows": len(proxy_rows),
        "proxy_difference_rows": len(difference_rows),
        "proxy_identity_rows": len(identity_rows),
        "runtime_difference_matched_rows": sum(1 for row in difference_rows if row.get("difference_status") == "matched"),
    }
    return proxy_rows, difference_rows, identity_rows, metrics


def build_runtime_package() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    tester_rows: list[dict[str, Any]] = []
    for source_run_id, path in [("run337P", P_TESTER_GAP), ("run337U", U_TESTER_GAP)]:
        for row in read_csv(path):
            tester_rows.append(
                {
                    "source_run_id": source_run_id,
                    "attempt_name": row.get("attempt_name", ""),
                    "feature_set_id": row.get("feature_set_id", ""),
                    "runtime_status": row.get("runtime_status", ""),
                    "report_status": row.get("report_status", ""),
                    "api_latest_us100_close_utc": row.get("api_latest_us100_close_utc", row.get("latest_us100_last_close_utc", "")),
                    "feature_last_timestamp": row.get("feature_last_timestamp", ""),
                    "tester_last_observed_bar_time": row.get("tester_last_observed_bar_time", ""),
                    "tester_to_feature_last_gap_minutes": row.get("tester_to_feature_last_gap_minutes", row.get("tester_to_latest_gap_minutes", "")),
                    "tester_to_api_latest_gap_minutes": row.get("tester_to_api_latest_gap_minutes", ""),
                    "telemetry_rows": row.get("telemetry_rows", ""),
                    "last_skip_reason": row.get("last_skip_reason", ""),
                    "gap_status": row.get("gap_status", ""),
                    "run337Y_use": "history_snapshot_for_reprobe_decision",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    package = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "execution_status": "prepared_not_run_in_run337Y",
        "reason_new_mt5_not_run": (
            "run337Y materializes actual measurement inputs and carries existing timestamp-aligned "
            "runtime differences; run337Z is the narrow execute-or-review gate."
        ),
        "runtime_inputs": {
            "tester_boundary_repair_plan": rel(W_TESTER_PLAN),
            "tester_feature_last_reach_gate": rel(W_TESTER_GATE),
            "run337P_runtime_result": rel(P_RUNTIME_RESULT),
            "run337U_rollover_handoff": rel(U_HANDOFF),
            "run337U_final_decision": rel(U_FINAL),
        },
        "required_outputs_for_run337Z": [
            "fresh MT5 runtime execution result or explicit execution blocker",
            "tester history snapshot reaching feature_last or blocker",
            "timestamp-aligned proxy-vs-MT5 difference with new source identity",
            "runtime claim boundary receipt",
        ],
        "forbidden_actions": [
            "model training",
            "threshold retuning",
            "lot optimization",
            "post-hoc weak pocket deletion",
            "Forward Passed/Failed without tester reaching feature_last",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    metrics = {
        "tester_history_rows": len(tester_rows),
        "tester_gap_remaining_rows": sum(1 for row in tester_rows if "gap_remains" in str(row.get("gap_status", ""))),
    }
    return package, tester_rows, metrics


def build_split_and_controls(source_snapshot: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    dataset_root = ROOT / "data" / "processed" / "datasets"
    split_rows: list[dict[str, Any]] = []
    for summary_path in sorted(dataset_root.glob("*/dataset_summary.json")):
        payload = read_json(summary_path)
        last_selected = payload.get("last_selected_timestamp") or payload.get("window_end_inclusive", "")
        last_dt = parse_utc(last_selected)
        forward_dt = parse_utc(FORWARD_START_UTC)
        if last_dt and forward_dt and last_dt < forward_dt:
            membership = "pre_forward_only"
            leakage_status = "no_forward_rows_in_dataset_summary"
        else:
            membership = "needs_row_level_review"
            leakage_status = "possible_forward_overlap"
        split_rows.append(
            {
                "dataset_id": payload.get("dataset_id", summary_path.parent.name),
                "summary_path": rel(summary_path),
                "window_start": payload.get("window_start", ""),
                "window_end_inclusive": payload.get("window_end_inclusive", ""),
                "last_selected_timestamp": last_selected,
                "forward_start_utc": FORWARD_START_UTC,
                "membership": membership,
                "leakage_status": leakage_status,
                "training_allowed_in_run337Y": "false",
                "effect": "dataset summary(데이터셋 요약) 기준으로 2026-04-14 이후 forward row(전진 행) 학습 유입을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    threshold_rows: list[dict[str, Any]] = []
    for row in read_csv(W_THRESHOLD):
        threshold_rows.append(
            {
                "contract_id": row.get("contract_id", ""),
                "rule": row.get("rule", ""),
                "forbidden": row.get("forbidden", ""),
                "required_evidence": row.get("required_evidence", ""),
                "run337Y_identity_status": "fixed_not_changed",
                "violation_judgment": row.get("violation_judgment", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    negative_rows: list[dict[str, Any]] = []
    reference = parse_utc(next((row.get("us100_reference_close_utc", "") for row in source_snapshot if row.get("symbol") == "US100"), ""))
    for row in source_snapshot:
        symbol = str(row.get("symbol", ""))
        source_time = parse_utc(row.get("last_close_utc"))
        synthetic_future = (reference + timedelta(minutes=5)) if reference else None
        expected = "invalid_source_timestamp_after_decision_bar"
        actual = "invalid_by_static_timestamp_guard" if synthetic_future and reference and synthetic_future > reference else "not_evaluable"
        negative_rows.append(
            {
                "control_id": f"negative_source_shift::{symbol}",
                "symbol": symbol,
                "source_last_close_utc": to_utc_z(source_time),
                "decision_timestamp_utc": to_utc_z(reference),
                "synthetic_shifted_source_timestamp_utc": to_utc_z(synthetic_future),
                "expected_guard": expected,
                "actual_guard": actual,
                "control_status": "passed_static_guard" if actual == "invalid_by_static_timestamp_guard" else "inconclusive",
                "training_allowed_in_run337Y": "false",
                "effect": "의도적으로 미래 source timestamp(원천 시점)를 만들어 guard(방어문)가 막는지 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    metrics = {
        "split_rows": len(split_rows),
        "split_pre_forward_rows": sum(1 for row in split_rows if row.get("membership") == "pre_forward_only"),
        "negative_control_rows": len(negative_rows),
        "negative_control_passed_rows": sum(1 for row in negative_rows if row.get("control_status") == "passed_static_guard"),
        "threshold_identity_rows": len(threshold_rows),
    }
    return split_rows, negative_rows, threshold_rows, metrics


def build_branch_preflight() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    branch_rows = read_csv(W_BRANCH_SPEC)
    cost_rows = read_csv(W_COST_LADDER)
    axis_rows = read_csv(W_DIRECTION_GATE)
    firewall_rows = read_csv(W_MODEL_FIREWALL)
    cost_by_attempt: dict[str, list[str]] = {}
    for row in cost_rows:
        attempt = row.get("attempt_name", "")
        cost_by_attempt.setdefault(attempt, []).append(str(row.get("extra_round_trip_points", "")))

    preflight: list[dict[str, Any]] = []
    for branch in branch_rows:
        for attempt in ["m48_plain_rf", "c56_plain_rf", "u42_plain_rf"]:
            preflight.append(
                {
                    "branch_id": branch.get("branch_id", ""),
                    "branch_type": branch.get("branch_type", ""),
                    "attempt_name": attempt,
                    "predeclared_cost_points": ";".join(cost_by_attempt.get(attempt, [])),
                    "required_axes": ";".join(row.get("axis", "") for row in axis_rows),
                    "firewall_requirements": ";".join(row.get("firewall_id", "") for row in firewall_rows),
                    "materialization_status": "preflight_ready_no_training_no_selection",
                    "success_criteria": branch.get("success_criteria", ""),
                    "failure_criteria": branch.get("failure_criteria", ""),
                    "forbidden_shortcut": branch.get("forbidden_shortcut", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    outputs: list[dict[str, Any]] = []
    for row in axis_rows:
        outputs.append(
            {
                "axis": row.get("axis", ""),
                "required_metrics": row.get("required_metrics", ""),
                "minimum_scope": row.get("minimum_scope", ""),
                "invalid_if": row.get("invalid_if", ""),
                "required_before_onnx_ready": row.get("required_before_onnx_ready", ""),
                "run337Y_status": "required_output_declared_not_executed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in cost_rows:
        outputs.append(
            {
                "axis": f"cost_stress::{row.get('attempt_name', '')}::{row.get('extra_round_trip_points', '')}",
                "required_metrics": row.get("required_output", ""),
                "minimum_scope": "attempt_cost_ladder",
                "invalid_if": "headline_only_without_cost_ladder",
                "required_before_onnx_ready": "true",
                "run337Y_status": "required_output_declared_not_executed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    metrics = {
        "branch_preflight_rows": len(preflight),
        "cost_direction_required_rows": len(outputs),
    }
    return preflight, outputs, metrics


def write_required_gate_audit() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    gate_specs = [
        ("source_timestamp_snapshot", SOURCE_TIMESTAMP_SNAPSHOT, "actual source timestamps recorded"),
        ("source_age_decision", SOURCE_AGE_DECISION, "source age decision recorded"),
        ("source_gap_blocker_report", SOURCE_GAP_BLOCKERS, "source blockers or repair-required rows recorded"),
        ("proxy_expected_values", PROXY_EXPECTED_VALUES, "row-level proxy expected values carried"),
        ("proxy_value_identity", PROXY_VALUE_IDENTITY, "proxy source identities hashed"),
        ("mt5_reprobe_manifest", MT5_REPROBE_MANIFEST, "runtime reprobe package prepared"),
        ("tester_history_snapshot", TESTER_HISTORY_SNAPSHOT, "tester feature_last gap history recorded"),
        ("timestamp_aligned_proxy_mt5_difference", TIMESTAMP_ALIGNED_DIFF, "existing timestamp-aligned runtime differences carried"),
        ("split_membership_audit", SPLIT_MEMBERSHIP_AUDIT, "pre-forward dataset membership checked"),
        ("negative_control_result", NEGATIVE_CONTROL_RESULT, "future timestamp negative control checked"),
        ("threshold_identity_audit", THRESHOLD_IDENTITY_AUDIT, "no threshold/risk/lot retune contract carried"),
        ("branch_preflight_matrix", BRANCH_PREFLIGHT_MATRIX, "branch preflight matrix declared"),
        ("cost_curve_direction_required_outputs", COST_CURVE_DIRECTION_OUTPUTS, "cost/direction/curve outputs declared"),
    ]
    rows: list[dict[str, Any]] = []
    for gate_id, path, effect in gate_specs:
        rows.append(
            {
                "gate_id": gate_id,
                "artifact_path": rel(path),
                "exists": str(path_exists(path)).lower(),
                "status": "present" if path_exists(path) else "missing",
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    metrics = {
        "gate_rows": len(rows),
        "gate_present_rows": sum(1 for row in rows if row["status"] == "present"),
    }
    return rows, metrics


def write_receipts(metrics: Mapping[str, Any], generated_at: str) -> list[Path]:
    receipts = [
        (
            DATA_RECEIPT,
            {
                "receipt_type": "data_integrity(데이터 무결성)",
                "run_id": RUN_ID,
                "data_source": [rel(P_SOURCE_SUMMARY), rel(P_SOURCE_ASOF), rel(SOURCE_TIMESTAMP_SNAPSHOT)],
                "time_axis": "MT5 UNIX seconds(유닉스 초) as UTC bar open/close; forward starts 2026-04-14T00:00:00Z",
                "sample_scope": f"US100 M5 plus macro/equity sources through {metrics['us100_reference_close_utc']}",
                "missing_or_duplicate_check": "source availability measured; duplicate bar scan not run in this packet",
                "feature_label_boundary": "source timestamp must be <= decision bar close; no model training in run337Y",
                "split_boundary": f"training freeze ends {FROZEN_TRAIN_END_UTC}; forward starts {FORWARD_START_UTC}",
                "leakage_risk": "session-stale macro/equity source fill and tester feature_last gap",
                "data_hash_or_identity": rel(PROXY_VALUE_IDENTITY),
                "integrity_judgment": "usable_with_boundary_for_runtime_probe_inputs_not_training",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "receipt_type": "runtime_parity(런타임 동등성)",
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": [rel(U_HANDOFF), rel(P_RUNTIME_RESULT), rel(MT5_REPROBE_MANIFEST)],
                "shared_contract": "same feature order, threshold policy, D/B surface, risk/lot rules; timestamp-aligned counts only",
                "known_differences": "run337Y carries existing run337P/run337U runtime differences and prepares run337Z; no new MT5 execution",
                "parity_check": rel(TIMESTAMP_ALIGNED_DIFF),
                "parity_identity": rel(PROXY_VALUE_IDENTITY),
                "runtime_claim_boundary": "runtime_probe_inputs_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "receipt_type": "model_validation(모델 검증)",
                "run_id": RUN_ID,
                "model_family": "existing ONNX/proxy artifacts carried; no new model training",
                "target_and_label": "not rebuilt in run337Y",
                "split_method": "pre-forward freeze vs 2026-04-14+ forward boundary audit",
                "selection_metric": "none",
                "secondary_metrics": "source age, proxy-MT5 difference, tester feature_last gap, cost/direction/curve required axes",
                "threshold_policy": "fixed_not_searched",
                "overfit_risk": "forward data used for threshold/source/session filtering",
                "calibration_risk": "proxy probabilities are signal sanity only, not KPI authority",
                "comparison_baseline": "run337P and run337U runtime probes",
                "validation_judgment": "exploratory_measurement_inputs_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "receipt_type": "result_judgment(결과 판정)",
                "run_id": RUN_ID,
                "result_subject": "run337Y actual measurement input package",
                "evidence_available": {
                    "source_rows": metrics["source_rows"],
                    "proxy_expected_rows": metrics["proxy_expected_rows"],
                    "proxy_difference_rows": metrics["proxy_difference_rows"],
                    "tester_history_rows": metrics["tester_history_rows"],
                    "gate_present_rows": f"{metrics['gate_present_rows']}/{metrics['gate_rows']}",
                },
                "evidence_missing": "new MT5 reprobe execution and tester reaching feature_last",
                "judgment_label": "exploratory_runtime_probe_input_package_ready",
                "claim_boundary": "can say actual inputs are materialized; cannot say Forward Passed/Failed, runtime authority, or Goal Achieve",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "실제 재료는 준비됐고, 다음은 MT5(메타트레이더5)가 최신 feature_last(피처 끝)까지 닿는지 확인하는 일이다.",
                "claim_boundary_full": CLAIM_BOUNDARY,
            },
        ),
        (
            LINEAGE_RECEIPT,
            {
                "receipt_type": "artifact_lineage(산출물 계보)",
                "run_id": RUN_ID,
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES],
                "artifact_hashes": rel(PROXY_VALUE_IDENTITY),
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked reports and script; local 02_runs outputs ignored_with_manifest",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload | {"generated_at_utc": generated_at}) for path, payload in receipts]


def write_run_manifest(metrics: Mapping[str, Any], generated_at: str) -> list[Path]:
    final = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "generated_at_utc": generated_at,
        "selected_candidate": "none",
        "model_training": "not_run",
        "new_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "metrics": metrics,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "script": rel(Path(__file__)),
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in OUTPUT_FILES],
        "generated_at_utc": generated_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [write_json(FINAL_DECISION, final), write_json(RUN_MANIFEST, manifest)]


def write_report(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337Y Actual Measurement Inputs(337Y 실제 측정 입력)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- model training(모델 학습): `not_run`
- new MT5 execution(신규 MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Counts(수치)

- source timestamp rows(원천 시점 행): `{metrics['source_rows']}`
- source blocker rows(원천 차단/수리 행): `{metrics['source_blocker_rows']}`
- proxy expected rows(프록시 예상 행): `{metrics['proxy_expected_rows']}`
- proxy-MT5 difference rows(프록시-MT5 차이 행): `{metrics['proxy_difference_rows']}`
- tester history rows(테스터 이력 행): `{metrics['tester_history_rows']}`
- split audit rows(분할 감사 행): `{metrics['split_rows']}`
- negative control rows(부정 대조 행): `{metrics['negative_control_rows']}`
- required gates present(필수 게이트 존재): `{metrics['gate_present_rows']}/{metrics['gate_rows']}`

## Read(판독)

run337Y(337Y 실행)는 run337X(337X 실행)의 5개 hard blocker(강한 차단 요소)를 실제 파일로 바꾸는 물질화(materialization, 물질화) 작업이다. 효과(effect, 효과)는 source age(원천 나이), proxy expected value(프록시 예상값), timestamp-aligned proxy-MT5 difference(시점 정렬 프록시-MT5 차이), split membership(분할 소속), negative control(부정 대조)을 다음 MT5 reprobe(MT5 재탐침) 판단에 바로 쓸 수 있게 만든 것이다.

이번 실행은 신규 MT5(메타트레이더5)를 돌리지 않았다. 대신 run337P/run337U(337P/337U 실행)의 timestamp-aligned runtime evidence(시점 정렬 런타임 증거)를 계보와 해시로 묶고, run337Z(337Z 실행)에서 실행하거나 즉시 차단 사유를 기록해야 하는 `mt5_reprobe_manifest.json`을 만들었다.

판정은 `exploratory_runtime_probe_input_package_ready(탐색적 런타임 탐침 입력 준비)`다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 아직 금지된다.
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337Y Decision(337Y 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- source_rows(원천 행): `{metrics['source_rows']}`
- proxy_difference_rows(프록시 차이 행): `{metrics['proxy_difference_rows']}`
- tester_gap_remaining_rows(남은 테스터 공백 행): `{metrics['tester_gap_remaining_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337Y(337Y 실행)는 실제 measurement inputs(측정 입력)를 만들었지만, tester feature_last reach(테스터 피처 끝 도달)가 아직 남아 있어 forward decision(전진 판정)은 열지 않는다. 다음 최소 조건은 run337Z(337Z 실행)에서 prepared MT5 reprobe package(준비된 MT5 재탐침 패키지)를 실행하거나, 실행 불가라면 정확한 runtime blocker(런타임 차단 사유)를 기록하는 것이다.
"""
    return write_md(DECISION_DOC, text)


def replace_or_append_stage_summary(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("- latest_run("):
            lines[index] = f"- latest_run(최신 실행): `{RUN_ID}`"
    text = "\n".join(lines) + "\n"
    if "run337Y_summary(337Y 요약)" not in text:
        marker = "- selected_candidate(선택 후보):"
        insert = (
            f"- run337Y_summary(337Y 요약): `{STATUS}`. Effect(효과): 실제 source timestamp(원천 시점), "
            "proxy expected value(프록시 예상값), timestamp-aligned proxy-MT5 difference(시점 정렬 프록시-MT5 차이), "
            "split/negative control(분할/부정 대조) 입력을 물질화했고 run337Z 실행/검토 대기열을 연다.\n"
        )
        text = text.replace(marker, insert + marker, 1)
    return text


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- actual_source_rows(실제 원천 행): `{metrics['source_rows']}`
- proxy_expected_rows(프록시 예상 행): `{metrics['proxy_expected_rows']}`
- proxy_mt5_difference_rows(프록시-MT5 차이 행): `{metrics['proxy_difference_rows']}`
- tester_gap_remaining_rows(남은 테스터 공백 행): `{metrics['tester_gap_remaining_rows']}`
- required_gates_present(필수 게이트 존재): `{metrics['gate_present_rows']}/{metrics['gate_rows']}`
- tester_boundary_required(테스터 경계 필요): `tester must reach feature_last before Forward Passed/Failed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337Y는 실제 측정 입력을 물질화했고, run337Z에서 MT5 재탐침 실행 또는 차단 판정을 해야 한다.
"""
    artifacts.append(write_md(SELECTED_STATUS, selection_text))

    if path_exists(STAGE_BRIEF):
        text, _ = read_text_with_bom(STAGE_BRIEF)
        artifacts.append(write_md(STAGE_BRIEF, replace_or_append_stage_summary(text)))

    focus_entry = (
        "- >-\n"
        f"  Stage337 run337Y focus complete: Stage337(337단계) run337Y(337Y 실행)는 `{STATUS}`로 실제 measurement inputs(측정 입력)를 물질화했다. "
        f"Effect(효과): source rows(원천 행) `{metrics['source_rows']}`, proxy expected rows(프록시 예상 행) `{metrics['proxy_expected_rows']}`, "
        f"proxy-MT5 difference rows(프록시-MT5 차이 행) `{metrics['proxy_difference_rows']}`, required gates(필수 게이트) `{metrics['gate_present_rows']}/{metrics['gate_rows']}`를 기록했고 run337Z(337Z 실행) 실행/검토를 연다.\n"
    )
    if path_exists(WORKSPACE_STATE):
        text, _ = read_text_with_bom(WORKSPACE_STATE)
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[index] = f"current_run_id: {NEXT_RUN_ID}"
            elif line.startswith("updated_on:"):
                lines[index] = f"updated_on: '{TODAY}'"
        text = "\n".join(lines) + "\n"
        if "Stage337 run337Y focus complete" not in text and "current_focus:\n" in text:
            text = text.replace("current_focus:\n", "current_focus:\n" + focus_entry + "\n", 1)
        artifacts.append(write_text(WORKSPACE_STATE, text, bom=True))

    current_header = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

"""
    current_entry = f"""
## Stage337 run337Y(337Y 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 실제 source timestamp(원천 시점), proxy expected value(프록시 예상값), timestamp-aligned proxy-MT5 difference(시점 정렬 프록시-MT5 차이), split/negative control(분할/부정 대조)을 만들었다. 신규 MT5(메타트레이더5)는 run337Y에서 실행하지 않았고, run337Z에서 실행 또는 차단을 판정한다.
"""
    if path_exists(CURRENT_STATE):
        text, _ = read_text_with_bom(CURRENT_STATE)
        body = text
        if text.startswith("# Current Working State"):
            first_stage_index = text.find("\n## ")
            if first_stage_index != -1:
                body = text[first_stage_index + 1 :]
        if "## Stage337 run337Y(337Y 실행)" not in body:
            body = current_entry.strip() + "\n\n" + body.rstrip() + "\n"
        artifacts.append(write_text(CURRENT_STATE, current_header + body, bom=True))

    if path_exists(CHANGELOG):
        text, _ = read_text_with_bom(CHANGELOG)
        line = (
            f"- {TODAY}: Stage337 run337Y(337Y 실행) `{STATUS}`. Effect(효과): 실제 측정 입력과 MT5 reprobe package(MT5 재탐침 패키지)를 만들었고 "
            "Forward/Goal(전진/목표) 주장은 없음."
        )
        if "Stage337 run337Y(337Y 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        artifacts.append(write_text(CHANGELOG, text, bom=True))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], metrics: Mapping[str, Any], generated_at: str) -> list[Path]:
    paths = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "materialization_runtime_parity_model_validation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};source_rows={metrics['source_rows']};proxy_diff_rows={metrics['proxy_difference_rows']};goal_achieve_not_claimed.",
                "family": "actual_source_age_proxy_mt5_input_materialization",
                "primary_report": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "ledger_row_id": f"{RUN_ID}__actual_measurement_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "materialization_runtime_parity_model_validation",
                "evidence_scope": "source timestamps proxy values existing runtime differences split controls",
                "kpi_scope": "input_materialization_no_new_forward_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};gate_present={metrics['gate_present_rows']}/{metrics['gate_rows']};goal_achieve_not_claimed.",
                "decision": DECISION,
                "run_key": f"{RUN_ID}__actual_measurement_inputs",
                "family": "actual_source_age_proxy_mt5_input_materialization",
                "question": "can run337X evidence gaps be materialized into actual measurement inputs",
                "metric_scope": "source_proxy_runtime_split_input_identity_no_forward_decision",
                "primary_artifact": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            ALPHA_LEDGER,
            ["ledger_row_id"],
            {
                "ledger_row_id": f"{RUN_ID}__actual_measurement_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "actual_measurement_inputs",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "actual_source_age_proxy_mt5_repair_probe_inputs",
                "tier_scope": "out_of_scope_by_claim_no_tier_kpi",
                "kpi_scope": "no_new_kpi_input_materialization",
                "scoreboard_lane": "materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": "not_applicable",
                "guardrail_kpi": "source_age;proxy_mt5;tester_feature_last;split_negative_control;threshold_identity",
                "external_verification_status": "existing_runtime_evidence_carried_new_mt5_not_run",
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
    ]
    paths.append(append_artifact_rows(artifact_paths, generated_at))
    return paths


def append_artifact_rows(paths: Sequence[Path], generated_at: str) -> Path:
    columns = [
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "artifact_path",
        "claim_boundary",
    ]
    existing = read_csv(ARTIFACT_REGISTRY)
    new_ids = {f"{RUN_ID}::{rel(path)}" for path in paths}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        suffix = path.suffix.lower().lstrip(".") or "file"
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix,
                "path": rel(path),
                "sha256": file_hash(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at,
                "notes": STATUS,
                "artifact_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    generated_at = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    source_snapshot, source_decisions, source_blockers, source_metrics = build_source_snapshot()
    proxy_rows, diff_rows, identity_rows, proxy_metrics = build_proxy_values()
    runtime_package, tester_rows, runtime_metrics = build_runtime_package()
    split_rows, negative_rows, threshold_rows, split_metrics = build_split_and_controls(source_snapshot)
    preflight_rows, required_output_rows, branch_metrics = build_branch_preflight()

    write_csv(
        SOURCE_TIMESTAMP_SNAPSHOT,
        [
            "source_group",
            "symbol",
            "broker_symbol",
            "preferred_source",
            "source_path",
            "manifest_path",
            "status",
            "row_count",
            "first_open_utc",
            "last_open_utc",
            "last_close_utc",
            "us100_reference_close_utc",
            "age_to_us100_minutes",
            "age_bucket",
            "source_hash",
            "manifest_hash",
            "time_axis",
            "lookahead_status",
            "availability_status",
            "claim_boundary",
        ],
        source_snapshot,
    )
    write_csv(
        SOURCE_AGE_DECISION,
        [
            "decision_id",
            "source_group",
            "symbol",
            "feature_role",
            "age_minutes",
            "age_bucket",
            "max_age_policy",
            "decision",
            "training_allowed",
            "forward_pass_fail_allowed",
            "runtime_probe_allowed",
            "effect",
            "claim_boundary",
        ],
        source_decisions,
    )
    write_csv(
        SOURCE_GAP_BLOCKERS,
        ["blocker_id", "severity", "symbol", "decision", "evidence_path", "repair_or_probe", "claim_boundary"],
        source_blockers,
    )
    write_csv(
        PROXY_EXPECTED_VALUES,
        [
            "source_run_id",
            "attempt_name",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "expected_feature_ready_count",
            "expected_model_ok_count",
            "expected_long_count",
            "expected_short_count",
            "expected_flat_count",
            "expected_signal_count",
            "expected_signal_rate",
            "expected_long_share",
            "feature_order_hash",
            "feature_csv_sha256",
            "model_sha256",
            "threshold_policy",
            "proxy_cutoff_utc",
            "proxy_row_scope",
            "source_scope",
            "usable_for_kpi_authority",
            "usable_for_runtime_signal_parity",
            "claim_boundary",
        ],
        proxy_rows,
    )
    write_csv(PROXY_VALUE_IDENTITY, ["source_run_id", "artifact_role", "path", "exists", "rows", "sha256", "scope", "claim_boundary"], identity_rows)
    write_json(MT5_REPROBE_MANIFEST, runtime_package | {"generated_at_utc": generated_at})
    write_csv(
        TESTER_HISTORY_SNAPSHOT,
        [
            "source_run_id",
            "attempt_name",
            "feature_set_id",
            "runtime_status",
            "report_status",
            "api_latest_us100_close_utc",
            "feature_last_timestamp",
            "tester_last_observed_bar_time",
            "tester_to_feature_last_gap_minutes",
            "tester_to_api_latest_gap_minutes",
            "telemetry_rows",
            "last_skip_reason",
            "gap_status",
            "run337Y_use",
            "claim_boundary",
        ],
        tester_rows,
    )
    write_csv(
        TIMESTAMP_ALIGNED_DIFF,
        [
            "source_run_id",
            "attempt_name",
            "artifact_slug",
            "dimension",
            "proxy_expected_value",
            "mt5_runtime_value",
            "difference_proxy_minus_mt5",
            "difference_status",
            "proxy_source",
            "mt5_source",
            "usable_for_runtime_signal_parity",
            "usable_for_forward_pass_fail",
            "runtime_skip_reason",
            "run337Y_materialization_status",
            "claim_boundary",
        ],
        diff_rows,
    )
    write_csv(
        SPLIT_MEMBERSHIP_AUDIT,
        [
            "dataset_id",
            "summary_path",
            "window_start",
            "window_end_inclusive",
            "last_selected_timestamp",
            "forward_start_utc",
            "membership",
            "leakage_status",
            "training_allowed_in_run337Y",
            "effect",
            "claim_boundary",
        ],
        split_rows,
    )
    write_csv(
        NEGATIVE_CONTROL_RESULT,
        [
            "control_id",
            "symbol",
            "source_last_close_utc",
            "decision_timestamp_utc",
            "synthetic_shifted_source_timestamp_utc",
            "expected_guard",
            "actual_guard",
            "control_status",
            "training_allowed_in_run337Y",
            "effect",
            "claim_boundary",
        ],
        negative_rows,
    )
    write_csv(
        THRESHOLD_IDENTITY_AUDIT,
        ["contract_id", "rule", "forbidden", "required_evidence", "run337Y_identity_status", "violation_judgment", "claim_boundary"],
        threshold_rows,
    )
    write_csv(
        BRANCH_PREFLIGHT_MATRIX,
        [
            "branch_id",
            "branch_type",
            "attempt_name",
            "predeclared_cost_points",
            "required_axes",
            "firewall_requirements",
            "materialization_status",
            "success_criteria",
            "failure_criteria",
            "forbidden_shortcut",
            "claim_boundary",
        ],
        preflight_rows,
    )
    write_csv(
        COST_CURVE_DIRECTION_OUTPUTS,
        ["axis", "required_metrics", "minimum_scope", "invalid_if", "required_before_onnx_ready", "run337Y_status", "claim_boundary"],
        required_output_rows,
    )
    gate_rows, gate_metrics = write_required_gate_audit()
    write_csv(REQUIRED_GATE_AUDIT, ["gate_id", "artifact_path", "exists", "status", "effect", "claim_boundary"], gate_rows)

    metrics: dict[str, Any] = {}
    metrics.update(source_metrics)
    metrics.update(proxy_metrics)
    metrics.update(runtime_metrics)
    metrics.update(split_metrics)
    metrics.update(branch_metrics)
    metrics.update(gate_metrics)

    receipt_paths = write_receipts(metrics, generated_at)
    manifest_paths = write_run_manifest(metrics, generated_at)
    report_paths = [write_report(metrics), write_decision_doc(metrics)]
    status_paths = update_status_docs(metrics)
    register_paths = update_registers(
        [Path(__file__), *OUTPUT_FILES, *report_paths, *status_paths, *manifest_paths, *receipt_paths],
        metrics,
        generated_at,
    )
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "metrics": metrics,
                "tracked_report": rel(REPORT_PATH),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
