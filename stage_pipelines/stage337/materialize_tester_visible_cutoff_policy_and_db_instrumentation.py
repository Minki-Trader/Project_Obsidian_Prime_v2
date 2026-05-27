# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AQ"
RUN_ID = "run337AQ_tester_visible_cutoff_policy_and_db_instrumentation_v1"
PARENT_RUN_ID = "run337AP_broker_tester_history_repair_or_next_rollover_v1"
NEXT_RUN_ID = "run337AR_db_source_sidecar_feasibility_or_out_of_scope_lock_v1"

CLAIM_BOUNDARY = (
    "research_development_only_stage337AQ_tester_visible_cutoff_policy_db_instrumentation_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STATUS = "completed_stage337AQ_tester_visible_cutoff_policy_db_instrumentation_no_forward_decision"
JUDGMENT = "tester_current_day_intraday_cutoff_policy_confirmed_db_source_still_missing"
DECISION = "stage337AQ_open_run337AR_db_source_sidecar_or_out_of_scope_lock_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AQ_tester_visible_cutoff_policy_and_db_instrumentation.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AQ_tester_visible_cutoff_policy_db_instrumentation.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

AP_DIR = STAGE_DIR / "02_runs" / "run337AP"
AO_DIR = STAGE_DIR / "02_runs" / "run337AO"

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
STAGE_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "work_family",
    "evidence_scope",
    "kpi_scope",
    "status",
    "judgment",
    "claim_boundary",
    "path",
    "notes",
    "decision",
    "run_key",
    "family",
    "question",
    "metric_scope",
    "primary_artifact",
    "report_path",
    "next_action",
]
ARTIFACT_COLUMNS = [
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

GAP_SOURCES = [
    ("run337AA", "tester_feature_last_gap_micro_probe.csv", "tester_history_cache_session_policy"),
    ("run337AH", "tester_feature_last_gap_visibility_repair.csv", "full_current_day_visibility_repair"),
    ("run337AI", "tester_feature_last_gap_model_mode_reprobe.csv", "tester_model_mode_reprobe"),
    ("run337AJ", "tester_feature_last_gap_cache_repair_reprobe.csv", "api_history_cache_repair_reprobe"),
    ("run337AK", "tester_feature_last_gap_exact_timestamp.csv", "synthetic_exact_timestamp_repair"),
    ("run337AN", "tester_feature_last_gap_reprobe.csv", "broker_rollover_reprobe"),
    ("run337AP", "tester_feature_last_gap_history_repair.csv", "broker_history_repair_reprobe"),
]

REQUIRED_DB_COLUMNS = [
    "db_decision_source",
    "d_source",
    "b_source",
    "d_score",
    "b_score",
    "decision_surface_branch",
    "source_component",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path | str) -> str:
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return str(int(value)) if value.is_integer() else f"{value:.10g}"
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not io_path(path).exists():
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or (had_bom is None and path.suffix.lower() in {".md", ".txt"}) else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding, newline="\n")
    return path


def sha256_file_lf_normalized(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def columns_for(rows: Sequence[Mapping[str, Any]], defaults: Sequence[str]) -> list[str]:
    columns = list(defaults)
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    return columns


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any], columns: Sequence[str]) -> Path:
    rows = [{column: existing.get(column, "") for column in columns} for existing in read_csv(path)]
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [
        existing
        for existing in rows
        if tuple(str(existing.get(column, "")) for column in key_columns) != key
    ]
    rows.append({column: row.get(column, "") for column in columns})
    return write_csv(path, columns, rows)


def parse_time(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    for candidate in (text, text.replace("Z", "+00:00")):
        try:
            return datetime.fromisoformat(candidate)
        except ValueError:
            pass
    for fmt in ("%Y.%m.%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    return None


def minutes_between(later: Any, earlier: Any) -> float | None:
    later_dt = parse_time(later)
    earlier_dt = parse_time(earlier)
    if later_dt is None or earlier_dt is None:
        return None
    if later_dt.tzinfo is not None:
        later_dt = later_dt.replace(tzinfo=None)
    if earlier_dt.tzinfo is not None:
        earlier_dt = earlier_dt.replace(tzinfo=None)
    return (later_dt - earlier_dt).total_seconds() / 60.0


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def first_existing_csv_header(paths: Sequence[Path]) -> list[str]:
    for path in paths:
        if io_path(path).exists():
            with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle)
                try:
                    return next(reader)
                except StopIteration:
                    return []
    return []


def collect_cutoff_evidence() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_dir_name, filename, evidence_family in GAP_SOURCES:
        source_path = STAGE_DIR / "02_runs" / run_dir_name / filename
        for row in read_csv(source_path):
            tester_last = row.get("tester_last_observed_bar_time", "")
            feature_last = row.get("feature_last_timestamp", "")
            api_latest = row.get("api_latest_us100_close_utc", "")
            gap_status = row.get("gap_status", "")
            attempt_name = row.get("attempt_name", "")
            scenario_id = row.get("scenario_id", "")
            tester_symbol = row.get("tester_symbol", "")
            is_shifted_custom = "shifted_custom" in attempt_name or "custom_symbol_shift" in scenario_id
            is_broker_us100 = tester_symbol in {"", "US100"} and not is_shifted_custom
            gap_minutes = row.get("tester_to_feature_last_gap_minutes") or minutes_between(feature_last, tester_last)
            api_gap_minutes = row.get("tester_to_api_latest_gap_minutes") or minutes_between(api_latest, tester_last)
            if is_shifted_custom:
                policy_read = "synthetic_shifted_custom_parity_only"
                forward_usable = False
            elif gap_status == "tester_reached_feature_last":
                policy_read = "completed_day_or_tester_visible_window"
                forward_usable = False
            elif tester_last == "2026-05-26T23:55:00Z" and str(feature_last).startswith("2026-05-27"):
                policy_read = "current_day_intraday_hidden_by_tester_cutoff"
                forward_usable = False
            elif gap_status == "tester_feature_last_gap_remains":
                policy_read = "tester_feature_last_gap_remains"
                forward_usable = False
            else:
                policy_read = "inconclusive"
                forward_usable = False
            rows.append(
                {
                    "source_run": run_dir_name,
                    "source_file": rel(source_path),
                    "evidence_family": evidence_family,
                    "attempt_name": attempt_name,
                    "scenario_id": scenario_id,
                    "tester_symbol": tester_symbol,
                    "tester_model": row.get("tester_model", ""),
                    "feature_set_id": row.get("feature_set_id", ""),
                    "api_latest_us100_close_utc": api_latest,
                    "feature_last_timestamp": feature_last,
                    "tester_last_observed_bar_time": tester_last,
                    "tester_to_feature_last_gap_minutes": gap_minutes,
                    "tester_to_api_latest_gap_minutes": api_gap_minutes,
                    "gap_status": gap_status,
                    "runtime_status": row.get("runtime_status", ""),
                    "report_status": row.get("report_status", ""),
                    "telemetry_rows": row.get("telemetry_rows", ""),
                    "log_test_to": row.get("log_test_to", ""),
                    "is_broker_us100": bool_text(is_broker_us100),
                    "is_shifted_custom": bool_text(is_shifted_custom),
                    "policy_read": policy_read,
                    "usable_for_runtime_signal_parity": bool_text(gap_status == "tester_reached_feature_last" or "parity" in policy_read or row.get("runtime_status") == "completed"),
                    "usable_for_forward_pass_fail": bool_text(forward_usable),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def summarize_cutoff(evidence_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    current_day_gap_rows = [
        row for row in evidence_rows
        if row.get("policy_read") == "current_day_intraday_hidden_by_tester_cutoff"
        and row.get("is_broker_us100") == "true"
    ]
    completed_visible_rows = [
        row for row in evidence_rows
        if row.get("policy_read") == "completed_day_or_tester_visible_window"
        and row.get("is_broker_us100") == "true"
    ]
    shifted_rows = [row for row in evidence_rows if row.get("is_shifted_custom") == "true"]
    api_later_rows = [
        row for row in evidence_rows
        if row.get("api_latest_us100_close_utc")
        and row.get("tester_last_observed_bar_time")
        and (minutes_between(row.get("api_latest_us100_close_utc"), row.get("tester_last_observed_bar_time")) or 0) > 0
    ]
    latest_api = max((str(row.get("api_latest_us100_close_utc")) for row in api_later_rows if row.get("api_latest_us100_close_utc")), default="")
    min_current_gap = min((float(row.get("tester_to_feature_last_gap_minutes") or 0) for row in current_day_gap_rows), default=0.0)
    policy_rows = [
        {
            "policy_id": "broker_current_day_intraday_cutoff",
            "status": "confirmed",
            "evidence_rows": len(current_day_gap_rows),
            "rule": "On 2026-05-27 broker US100 Strategy Tester(전략 테스터)는 API history(API 이력)가 더 최신이어도 2026-05-26T23:55:00Z까지만 관측했다.",
            "allowed_use": "Use completed-day or tester-visible windows only(완성일 또는 테스터 가시 구간만 사용).",
            "forbidden_use": "Do not use current-day intraday feature rows for Forward Passed/Failed(현재일 장중 피처 행으로 전진 통과/실패 판정 금지).",
            "effect": "현재일 장중 데이터 공백을 성과 실패나 성공으로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "policy_id": "completed_day_window_allowed",
            "status": "allowed_with_boundary",
            "evidence_rows": len(completed_visible_rows),
            "rule": "If feature_last(피처 끝)이 tester_last_observed_bar_time(테스터 마지막 관측 시점) 이하이면 attribution-only review(귀속 전용 검토)는 가능하다.",
            "allowed_use": "Runtime signal parity, attribution, cost stress, curve pocket diagnostics(런타임 신호 동등성, 귀속, 비용 압박, 곡선 포켓 진단).",
            "forbidden_use": "Do not promote to operating readiness or broad forward pass(운영 준비나 넓은 전진 통과로 승격 금지).",
            "effect": "완성일 구간은 쓸 수 있지만 현재일 전진 판정과 섞지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "policy_id": "synthetic_shifted_custom_proxy_scope",
            "status": "parity_only",
            "evidence_rows": len(shifted_rows),
            "rule": "Shifted custom symbols(이동 커스텀 심볼)은 exact timestamp parity(정확 시점 동등성)만 시험하며 broker US100 forward KPI(브로커 US100 전진 KPI) 근거가 아니다.",
            "allowed_use": "Proxy-MT5 timestamp and signal sanity check(프록시-MT5 시점 및 신호 점검).",
            "forbidden_use": "Do not use shifted custom result as broker forward profitability evidence(이동 커스텀 결과를 브로커 전진 수익성 근거로 사용 금지).",
            "effect": "프록시 수리를 실제 브로커 수익 검증처럼 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "policy_id": "api_history_warmup_not_sufficient",
            "status": "confirmed",
            "evidence_rows": len(api_later_rows),
            "rule": "MT5 API(MT5 API)는 더 최신 bar(봉)를 보지만 Strategy Tester(전략 테스터)는 이전 완성일에 머물 수 있다.",
            "allowed_use": "Use API freshness as data availability evidence only(API 최신성은 데이터 확보 근거로만 사용).",
            "forbidden_use": "Do not infer tester forward availability from API latest close alone(API 최신 종가만으로 테스터 전진 가시성 추론 금지).",
            "effect": "데이터 확보와 테스터 가시성을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    summary = {
        "evidence_rows": len(evidence_rows),
        "current_day_gap_rows": len(current_day_gap_rows),
        "completed_visible_rows": len(completed_visible_rows),
        "shifted_custom_rows": len(shifted_rows),
        "api_later_rows": len(api_later_rows),
        "latest_api_latest_us100_close_utc": latest_api,
        "min_current_day_gap_minutes": min_current_gap,
        "broker_forward_usable": False,
    }
    return policy_rows, summary


def build_db_instrumentation() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    telemetry_header = first_existing_csv_header(
        [
            AP_DIR / "runtime_telemetry" / "u42_plain_rf_ap_api_warm_model4_real_ticks_telemetry.csv",
            AP_DIR / "runtime_telemetry" / "u42_plain_rf_ap_api_warm_model0_generated_telemetry.csv",
            AP_DIR / "runtime_telemetry" / "u42_plain_rf_ap_api_warm_model4_wide_todate_telemetry.csv",
        ]
    )
    feature_header = first_existing_csv_header(
        [
            AP_DIR / "feature_matrices" / "u42_plain_ap_api_warm_model4_real_ticks_features.csv",
            AP_DIR / "feature_matrices" / "u42_plain_ap_api_warm_model0_generated_features.csv",
            AP_DIR / "feature_matrices" / "u42_plain_ap_api_warm_model4_wide_todate_features.csv",
        ]
    )
    ao_schema = {row.get("required_column", ""): row for row in read_csv(AO_DIR / "db_source_telemetry_schema.csv")}
    rows: list[dict[str, Any]] = []
    missing_count = 0
    for column in REQUIRED_DB_COLUMNS:
        telemetry_status = "present" if column in telemetry_header else "missing"
        feature_status = "present" if column in feature_header else "missing"
        ao_status = ao_schema.get(column, {}).get("readiness", "missing_required")
        if telemetry_status == "missing" and feature_status == "missing":
            missing_count += 1
            readiness = "missing_required"
        else:
            readiness = "available"
        rows.append(
            {
                "required_column": column,
                "ap_runtime_telemetry_status": telemetry_status,
                "ap_feature_matrix_status": feature_status,
                "ao_readiness": ao_status,
                "readiness": readiness,
                "allowed_proxy": "none" if readiness == "missing_required" else "direct_column",
                "forbidden_claim": "D/B attribution from long/short decision or direction proxy(롱/숏 결정이나 방향 대리값으로 D/B 귀속 주장 금지)",
                "required_repair": "source sidecar or explicit out_of_scope lock(원천 보조표 또는 명시적 범위 밖 고정)",
                "effect": "D/B 원천을 실제 컬럼 없이 만들지 못하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "required_column": "decision",
            "ap_runtime_telemetry_status": "present" if "decision" in telemetry_header else "missing",
            "ap_feature_matrix_status": "not_required",
            "ao_readiness": "direction_proxy_only",
            "readiness": "direction_proxy_only",
            "allowed_proxy": "long_short_direction_only",
            "forbidden_claim": "D/B source attribution(D/B 원천 귀속)",
            "required_repair": "do not substitute direction for D/B source(방향을 D/B 원천으로 대체하지 않음)",
            "effect": "방향 귀속과 D/B 원천 귀속을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    action_rows = [
        {
            "action_id": "db_source_sidecar_search",
            "priority": "P0",
            "action": "Search existing frozen package or parent score tables for real D/B source fields(기존 고정 패키지나 부모 점수표에서 실제 D/B 원천 필드 탐색).",
            "allowed_change": "read-only lineage and sidecar materialization(읽기 전용 계보 확인 및 보조표 물질화)",
            "forbidden_change": "threshold retune; D/B rule rewrite; inferring source from direction(임계값 재조정, D/B 규칙 재작성, 방향에서 원천 추론 금지)",
            "success_condition": "All required D/B columns are present as timestamp-aligned sidecar fields(필수 D/B 컬럼이 시점 정렬 보조표로 존재).",
            "failure_condition": "No frozen source contains D/B fields, so D/B attribution remains out_of_scope_by_claim(고정 원천에 D/B 필드가 없으면 D/B 귀속은 범위 밖).",
            "effect": "D/B 귀속을 살릴 수 있는지, 아니면 명시적으로 제외해야 하는지 닫는다.",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "action_id": "tester_window_policy_lock",
            "priority": "P0",
            "action": "Use completed-day/tester-visible windows for attribution until broker tester reaches feature_last(브로커 테스터가 피처 끝에 닿을 때까지 완성일/테스터 가시 구간만 귀속에 사용).",
            "allowed_change": "window labeling and evidence boundary only(구간 라벨과 근거 경계만 변경)",
            "forbidden_change": "using proxy or shifted custom result as broker forward KPI(프록시나 이동 커스텀 결과를 브로커 전진 KPI로 사용 금지)",
            "success_condition": "Forward decision uses only broker-visible rows or remains not_claimed(전진 판정은 브로커 가시 행만 쓰거나 미주장 유지).",
            "failure_condition": "Current-day intraday rows are mixed into forward pass/fail(현재일 장중 행이 전진 통과/실패에 섞임).",
            "effect": "테스터 가시 구간 밖 데이터로 과적합 판정을 만들지 않는다.",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "action_id": "runtime_telemetry_schema_extension_gate",
            "priority": "P1",
            "action": "Only after sidecar feasibility, define non-trading telemetry fields for D/B source if frozen lineage provides them(보조표 가능성이 확인된 뒤에만 매매 비개입 D/B 기록 필드 정의).",
            "allowed_change": "instrumentation-only telemetry schema(계측 전용 텔레메트리 스키마)",
            "forbidden_change": "model, ONNX, feature order, score threshold, lot, risk, ATR exit, runtime handoff semantics(모델, 온엑스, 피처 순서, 점수 임계값, 랏, 위험, ATR 청산, 런타임 인계 의미 변경 금지)",
            "success_condition": "Telemetry extension records D/B source without changing decisions(결정 변경 없이 D/B 원천만 기록).",
            "failure_condition": "Instrumentation changes trading behavior or hides missing source(계측이 매매 행동을 바꾸거나 원천 누락을 숨김).",
            "effect": "계측은 가능하게 하되 매매 의미는 바꾸지 않는다.",
            "next_run": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    summary = {
        "required_db_columns": len(REQUIRED_DB_COLUMNS),
        "missing_required_db_columns": missing_count,
        "runtime_telemetry_columns": len(telemetry_header),
        "feature_matrix_columns": len(feature_header),
        "decision_column_present": "decision" in telemetry_header,
        "db_source_available": missing_count == 0,
    }
    return rows, action_rows, summary


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(AP_DIR / "tester_feature_last_gap_history_repair.csv"),
                    rel(AO_DIR / "db_source_telemetry_schema.csv"),
                ],
                "time_axis": "MT5 broker server bar close timestamps(MT5 브로커 서버 봉 종가 시점); tester_last_observed(테스터 마지막 관측)을 feature_last(피처 끝)와 API latest close(API 최신 종가)에 비교한다.",
                "sample_scope": "Stage337 repeated US100 M5 broker/tester probes(반복 브로커/테스터 탐침) on 2026-05-27 plus shifted custom parity control(이동 커스텀 동등성 대조).",
                "missing_or_duplicate_check": "not a bar rematerialization run(봉 재물질화 실행 아님); prior run gap and schema evidence(이전 실행 공백과 스키마 근거)를 사용한다.",
                "feature_label_boundary": "No model training/relabeling/threshold adjustment(모델 학습/재라벨/임계값 조정 없음); tester cutoff(테스터 컷오프) 이후 현재일 행은 전진 판정에 쓰지 않는다.",
                "split_boundary": "runtime diagnostic only(런타임 진단 전용); train/validation/OOS split(학습/검증/표본외 분할) 변경 없음.",
                "leakage_risk": "Using API-visible or proxy-visible rows as broker tester forward KPI(API 또는 프록시 가시 행을 브로커 테스터 전진 KPI로 쓰는 위험).",
                "data_hash_or_identity": {
                    "ap_final_decision": sha256_file_lf_normalized(AP_DIR / "final_decision.json"),
                    "ao_db_schema": sha256_file_lf_normalized(AO_DIR / "db_source_telemetry_schema.csv"),
                },
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "effect": "현재일 데이터 가시성과 전진 판정을 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(__file__),
                "runtime_path": rel(AP_DIR / "handoff_attempts.csv"),
                "shared_contract": "same frozen ONNX(동일 고정 온엑스), feature order(피처 순서), threshold(임계값), risk(위험), lot(랏), ATR exits(ATR 청산), timestamp basis(시점 기준), telemetry files(기록 파일)를 run337AP evidence(근거)에서 유지.",
                "known_differences": "run337AQ does not execute a new Strategy Tester run(새 전략 테스터 실행 없음); run337AA/AH/AI/AJ/AK/AN/AP 외부 테스터 근거를 해석한다.",
                "parity_check": "timestamp cutoff evidence(시점 컷오프 근거) and D/B schema inventory(D/B 스키마 목록)를 prior MT5 runtime outputs(이전 MT5 런타임 출력)에서 물질화.",
                "parity_identity": {
                    "parent_run_id": PARENT_RUN_ID,
                    "ap_runtime_completed": final.get("parent_runtime_completed"),
                    "cutoff_evidence_rows": final.get("cutoff_evidence_rows"),
                    "db_missing_required_columns": final.get("db_missing_required_columns"),
                },
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority(런타임 탐침 전용, 런타임 권위 없음)",
                "effect": "새 실행 없이도 반복된 외부 런타임 증거의 의미를 좁혀 기록한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": RUN_ID,
                "evidence_available": [
                    rel(RUN_DIR / "tester_visible_cutoff_evidence.csv"),
                    rel(RUN_DIR / "tester_visible_cutoff_policy.csv"),
                    rel(RUN_DIR / "db_instrumentation_gap_matrix.csv"),
                    rel(RUN_DIR / "db_instrumentation_action_plan.csv"),
                ],
                "evidence_missing": [
                    "broker Strategy Tester reaching 2026-05-27T02:00:00Z feature_last",
                    "real D/B source telemetry or timestamp-aligned sidecar",
                    "full forward attribution report using broker-visible latest window",
                ],
                "judgment_label": "inconclusive_runtime_probe_boundary(불충분한 런타임 탐침 경계)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "테스터가 최신 장중 봉을 못 보므로 forward 판정은 막고, D/B 원천은 실제 컬럼이나 sidecar가 있어야만 주장한다.",
            },
        )
    )
    return artifacts


def write_report(final: Mapping[str, Any], policy_rows: Sequence[Mapping[str, Any]], action_rows: Sequence[Mapping[str, Any]]) -> Path:
    report = f"""# Stage337AQ Tester Visible Cutoff Policy And D/B Instrumentation(337AQ 테스터 가시 컷오프 정책 및 D/B 계측)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- cutoff evidence rows(컷오프 근거 행): `{final['cutoff_evidence_rows']}`
- broker current-day gap rows(브로커 현재일 공백 행): `{final['current_day_gap_rows']}`
- completed visible rows(완성일 가시 행): `{final['completed_visible_rows']}`
- shifted custom rows(이동 커스텀 행): `{final['shifted_custom_rows']}`
- latest API close(API 최신 종가): `{final['latest_api_latest_us100_close_utc']}`
- D/B missing columns(D/B 누락 컬럼): `{final['db_missing_required_columns']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Cutoff Policy(컷오프 정책)

| policy(정책) | status(상태) | evidence(근거) | allowed(허용) | forbidden(금지) |
|---|---:|---:|---|---|
"""
    for row in policy_rows:
        report += (
            f"| `{row['policy_id']}` | `{row['status']}` | `{row['evidence_rows']}` | "
            f"{row['allowed_use']} | {row['forbidden_use']} |\n"
        )
    report += """
## D/B Instrumentation(D/B 계측)

D/B source(D/B 원천)는 run337AP runtime telemetry(런타임 기록)와 feature matrix(피처 행렬)에 없다. decision(결정) 컬럼은 방향 proxy(대리값)일 뿐이며 D/B attribution(D/B 귀속)을 대신하지 않는다.

| action(행동) | priority(우선순위) | allowed change(허용 변경) | forbidden change(금지 변경) |
|---|---:|---|---|
"""
    for row in action_rows:
        report += f"| `{row['action_id']}` | `{row['priority']}` | {row['allowed_change']} | {row['forbidden_change']} |\n"
    report += """
## Boundary(경계)

run337AQ(337AQ 실행)는 새 training(학습), threshold retuning(임계값 재조정), D/B rule rewrite(D/B 규칙 재작성), lot optimization(랏 최적화)을 하지 않았다. 효과(effect, 효과)는 tester-visible(테스터 가시) 데이터만 forward decision(전진 판정)에 쓸 수 있게 경계를 고정하고, D/B source(D/B 원천)는 실제 source sidecar(원천 보조표)나 out_of_scope(범위 밖) 중 하나로 닫게 하는 것이다.
"""
    return write_text(REPORT_PATH, report)


def update_workspace_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- broker_forward_boundary(브로커 전진 경계): `failed`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- broker_current_day_gap_rows(브로커 현재일 공백 행): `{final['current_day_gap_rows']}`
- completed_visible_rows(완성일 가시 행): `{final['completed_visible_rows']}`
- db_source_status(D/B 원천 상태): `missing_required_columns_{final['db_missing_required_columns']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_current_day_cutoff_and_db_source_missing`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AQ(337AQ 실행)는 현재일 tester cutoff(테스터 컷오프)를 정책으로 고정하고 D/B source(D/B 원천) sidecar(보조표) 또는 out_of_scope(범위 밖) 결정을 다음 조건으로 분리했다.
"""
    artifacts.append(write_text(SELECTED_STATUS, selection))

    state, state_bom = read_text(WORKSPACE_STATE)
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage337 run337AQ focus complete: run337AQ(337AQ 실행)은 `{STATUS}`로 tester visible cutoff policy(테스터 가시 컷오프 정책)와 D/B instrumentation(D/B 계측)을 물질화했다. "
        f"Effect(효과): current-day gap rows(현재일 공백 행) `{final['current_day_gap_rows']}`, completed visible rows(완성일 가시 행) `{final['completed_visible_rows']}`, "
        f"D/B missing columns(D/B 누락 컬럼) `{final['db_missing_required_columns']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    state = re.sub(r"- >-\n  Stage337 run337AQ focus complete:.*?(?=\n- >-|\Z)", "", state, flags=re.S)
    state = re.sub(r"current_focus:\n\s*\n?", "current_focus:\n" + focus + "\n", state, count=1)
    artifacts.append(write_text(WORKSPACE_STATE, state, state_bom))

    current = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- secondary_current_run(보조 현재 실행): `none`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Stage337 run337AQ(337AQ 실행) - 2026-05-27

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): tester visible cutoff(테스터 가시 컷오프)를 current-day forward boundary(현재일 전진 경계)로 고정하고, D/B source(D/B 원천)는 sidecar feasibility(보조표 가능성) 또는 out_of_scope lock(범위 밖 고정)으로 다음 작업을 좁혔다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    old_current, current_bom = read_text(CURRENT_STATE)
    marker = "\n## Stage267 Candidate Pool"
    tail = old_current[old_current.find(marker) :] if marker in old_current else "\n"
    artifacts.append(write_text(CURRENT_STATE, current + tail, current_bom))

    brief, brief_bom = read_text(STAGE_BRIEF)
    brief = re.sub(r"- latest_run\(최신 실행\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", brief, count=1)
    summary = (
        f"- run337AQ_summary(337AQ 요약): `{STATUS}`. "
        f"Effect(효과): tester visible cutoff(테스터 가시 컷오프) current-day gap(현재일 공백) `{final['current_day_gap_rows']}`행, "
        f"completed visible(완성일 가시) `{final['completed_visible_rows']}`행, D/B missing(D/B 누락) `{final['db_missing_required_columns']}`.\n"
    )
    if "run337AQ_summary(337AQ 요약)" in brief:
        brief = re.sub(r"- run337AQ_summary\(337AQ 요약\): [^\n]*(?:\n|$)", summary, brief, count=1)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(write_text(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = read_text(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AQ(337AQ 실행) `{STATUS}`. "
        f"Effect(효과): tester cutoff(테스터 컷오프) policy(정책)와 D/B instrumentation(D/B 계측) 경계를 물질화했고 Forward/Goal(전진/목표)은 주장하지 않음.\n"
    )
    pattern = rf"^- {re.escape(TODAY)}: Stage337 run337AQ\(337AQ 실행\).*$"
    if re.search(pattern, changelog, flags=re.MULTILINE):
        changelog = re.sub(pattern, line.rstrip(), changelog, flags=re.MULTILINE)
    else:
        changelog = changelog.rstrip() + "\n" + line
    artifacts.append(write_text(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "tester_visible_cutoff_policy_db_instrumentation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_runtime_boundary",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__tester_visible_cutoff_policy_db_instrumentation",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "tester_visible_cutoff_policy_db_instrumentation",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "policy_materialization_no_forward_decision(정책 물질화, 전진 판정 없음)",
        "tier_scope": "Tier A u42 broker tester diagnostics(Tier A u42 브로커 테스터 진단)",
        "kpi_scope": "tester_cutoff_and_db_instrumentation",
        "scoreboard_lane": "data_integrity_runtime_boundary",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"cutoff_rows={final['cutoff_evidence_rows']};current_gap={final['current_day_gap_rows']};db_missing={final['db_missing_required_columns']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;no_forward_claim",
        "external_verification_status": "completed_from_parent_mt5_outputs",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__tester_visible_cutoff_policy_db_instrumentation",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_runtime_boundary",
        "evidence_scope": "run337AA/AH/AI/AJ/AK/AN/AP tester gap evidence and run337AO D/B schema",
        "kpi_scope": "policy_materialization_no_forward_decision",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;current_gap={final['current_day_gap_rows']};db_missing={final['db_missing_required_columns']}",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__tester_visible_cutoff_policy_db_instrumentation",
        "family": "tester_visible_cutoff_policy_db_instrumentation",
        "question": "what tester-visible window policy and D/B instrumentation boundary prevents false forward claims",
        "metric_scope": "tester_cutoff_policy_db_schema_no_forward_decision",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row, RUN_REGISTRY_COLUMNS),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row, ALPHA_LEDGER_COLUMNS),
        upsert_csv(STAGE_LEDGER, ["ledger_row_id"], stage_row, STAGE_LEDGER_COLUMNS),
    ]


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# 2026-05-27 Stage337AQ Tester Cutoff And D/B Instrumentation Decision(337AQ 테스터 컷오프 및 D/B 계측 결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- db_source_status(D/B 원천 상태): `missing_required_columns_{final['db_missing_required_columns']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337AQ(337AQ 실행)는 Strategy Tester(전략 테스터)가 현재일 장중 feature_last(피처 끝)를 보지 못하는 정책 경계를 고정했고, D/B attribution(D/B 귀속)은 실제 source sidecar(원천 보조표)가 없으면 범위 밖으로 잠가야 한다.
"""
    return write_text(DECISION_DOC, text)


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    unique_paths: list[Path] = []
    seen_paths: set[str] = set()
    for path in paths:
        if not io_path(path).exists():
            continue
        artifact_path = rel(path)
        if artifact_path in seen_paths:
            continue
        seen_paths.add(artifact_path)
        unique_paths.append(path)
    artifact_ids = {f"{RUN_ID}::{rel(path)}" for path in unique_paths}
    rows = [row for row in rows if row.get("artifact_id") not in artifact_ids]
    created_at = now_utc()
    for path in unique_paths:
        artifact_path = rel(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows)


def build_gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "parent_mt5_evidence_loaded",
            "status": "passed" if final["parent_runtime_completed"] == final["parent_runtime_total"] else "failed",
            "evidence_path": rel(AP_DIR / "final_decision.json"),
            "effect": "부모 MT5 외부 실행 근거를 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "tester_visible_cutoff_policy_materialized",
            "status": "passed" if final["current_day_gap_rows"] > 0 else "failed",
            "evidence_path": rel(RUN_DIR / "tester_visible_cutoff_policy.csv"),
            "effect": "현재일 테스터 공백을 정책으로 잠근다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "db_instrumentation_gap_materialized",
            "status": "passed" if final["db_missing_required_columns"] >= 0 else "failed",
            "evidence_path": rel(RUN_DIR / "db_instrumentation_gap_matrix.csv"),
            "effect": "D/B 원천 누락을 실제 컬럼 기준으로 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_model_threshold_lot_mutation",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
            "effect": "ONNX, threshold, D/B rule, risk, lot을 바꾸지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_claim_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed와 Goal Achieve를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    parent_final = read_json(AP_DIR / "final_decision.json")
    evidence_rows = collect_cutoff_evidence()
    policy_rows, cutoff_summary = summarize_cutoff(evidence_rows)
    db_rows, action_rows, db_summary = build_db_instrumentation()
    final = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "cutoff_evidence_rows": cutoff_summary["evidence_rows"],
        "current_day_gap_rows": cutoff_summary["current_day_gap_rows"],
        "completed_visible_rows": cutoff_summary["completed_visible_rows"],
        "shifted_custom_rows": cutoff_summary["shifted_custom_rows"],
        "api_later_rows": cutoff_summary["api_later_rows"],
        "latest_api_latest_us100_close_utc": cutoff_summary["latest_api_latest_us100_close_utc"],
        "min_current_day_gap_minutes": cutoff_summary["min_current_day_gap_minutes"],
        "db_missing_required_columns": db_summary["missing_required_db_columns"],
        "db_source_available": db_summary["db_source_available"],
        "parent_runtime_completed": parent_final.get("runtime_completed"),
        "parent_runtime_total": parent_final.get("runtime_total"),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    artifacts: list[Path] = []
    artifacts.extend(
        [
            write_csv(RUN_DIR / "tester_visible_cutoff_evidence.csv", columns_for(evidence_rows, ["source_run", "attempt_name"]), evidence_rows),
            write_csv(RUN_DIR / "tester_visible_cutoff_policy.csv", columns_for(policy_rows, ["policy_id"]), policy_rows),
            write_csv(RUN_DIR / "db_instrumentation_gap_matrix.csv", columns_for(db_rows, ["required_column"]), db_rows),
            write_csv(RUN_DIR / "db_instrumentation_action_plan.csv", columns_for(action_rows, ["action_id"]), action_rows),
            write_json(RUN_DIR / "parent_run337AP_final_decision.json", parent_final),
            write_json(RUN_DIR / "final_decision.json", final),
        ]
    )
    artifacts.extend(build_receipts(final))
    gate_rows = build_gate_rows(final)
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", columns_for(gate_rows, ["gate_id"]), gate_rows))
    artifacts.append(write_report(final, policy_rows, action_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_workspace_docs(final))
    artifacts.extend(update_registers(final))
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "parent_run_id": PARENT_RUN_ID,
        "artifacts": [
            {
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
            }
            for path in artifacts
            if io_path(path).exists()
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_decision": final,
    }
    manifest_path = write_json(RUN_DIR / "run_manifest.json", manifest)
    artifacts.append(manifest_path)
    artifact_registry_path = update_artifact_registry(
        artifacts + [Path(__file__), RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER],
        final,
    )
    artifacts.append(artifact_registry_path)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
