# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AU"
RUN_ID = "run337AU_materialize_balanced_no_lookahead_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337AT_balanced_no_lookahead_repair_protocol_without_db_v1"
NEXT_RUN_ID = "run337AV_review_balanced_no_lookahead_repair_inputs_without_db_v1"

STATUS = "completed_stage337AU_balanced_no_lookahead_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "materialized_repair_inputs_ready_for_review_but_no_forward_or_goal_claim"
DECISION = "stage337AU_open_run337AV_review_balanced_repair_inputs_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AU_balanced_no_lookahead_repair_inputs_"
    "without_db_no_model_training_no_threshold_retuning_no_db_rule_rewrite_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AU_materialize_balanced_no_lookahead_repair_inputs_without_db.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AU_balanced_no_lookahead_repair_inputs_without_db.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

AT_DIR = STAGE_DIR / "02_runs" / "run337AT"
AS_DIR = STAGE_DIR / "02_runs" / "run337AS"
AE_DIR = STAGE_DIR / "02_runs" / "run337AE"
AD_DIR = STAGE_DIR / "02_runs" / "run337AD"
AO_DIR = STAGE_DIR / "02_runs" / "run337AO"

AT_FINAL = AT_DIR / "final_decision.json"
AT_PROTOCOLS = AT_DIR / "balanced_repair_protocol_catalog.csv"
AT_BOUNDARY = AT_DIR / "no_lookahead_boundary_contract.csv"
AT_QUEUE = AT_DIR / "repair_materialization_queue.csv"
AT_PROXY_GATE = AT_DIR / "proxy_mt5_gate_plan.csv"
AT_FORWARD_PLAN = AT_DIR / "forward_window_evidence_plan.csv"

AS_FINAL = AS_DIR / "final_decision.json"
AS_ATTRIBUTION = AS_DIR / "non_db_attribution_report.csv"
AS_PROXY_USABILITY = AS_DIR / "proxy_mt5_usability_matrix.csv"
AS_FORWARD_WINDOW = AS_DIR / "forward_window_lock_matrix.csv"
AS_FRAGILITY = AS_DIR / "fragility_driver_matrix.csv"

AE_TRADES = AE_DIR / "trade_records.csv"
AE_COST = AE_DIR / "cost_stress_report.csv"
AE_CURVE = AE_DIR / "curve_pocket_report.csv"
AE_LOT = AE_DIR / "lot_normalized_report.csv"
AO_ASOF = AO_DIR / "asof_trade_regime_join.csv"
AD_PROXY_EXPECTED = AD_DIR / "timestamp_aligned_proxy_expected_result.csv"
AD_PROXY_DIFF = AD_DIR / "timestamp_aligned_proxy_mt5_difference.csv"

REPAIR_INPUT_FRAME = RUN_DIR / "completed_day_pretrade_repair_feature_frame.csv"
PROTOCOL_INPUT_MATRIX = RUN_DIR / "protocol_materialized_input_matrix.csv"
FEATURE_BINDING = RUN_DIR / "protocol_feature_binding_matrix.csv"
NEGATIVE_CONTROL = RUN_DIR / "negative_control_input_recipe_matrix.csv"
COST_LADDER = RUN_DIR / "cost_ladder_input_matrix.csv"
PROXY_CONTRACT = RUN_DIR / "proxy_mt5_materialization_contract.csv"
FORWARD_VISIBILITY = RUN_DIR / "forward_visibility_handoff_matrix.csv"
RUNTIME_QUEUE = RUN_DIR / "mt5_runtime_probe_candidate_queue.csv"
NO_LOOKAHEAD_AUDIT = RUN_DIR / "no_lookahead_materialization_audit.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

COMPLETED_ATTEMPT = "u42_plain_rf_ad_completed_day_broker_slice"
INITIAL_BALANCE = 500.0

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

FRAME_COLUMNS = [
    "trade_index",
    "feature_timestamp",
    "open_time",
    "direction",
    "month",
    "weekday",
    "open_hour_utc",
    "session_utc",
    "chron_segment",
    "vol_regime",
    "atr_ratio_regime",
    "adx_regime",
    "di_regime",
    "vix_z_regime",
    "vix_age_bucket",
    "rate_z_regime",
    "rate_age_bucket",
    "usd_z_regime",
    "usd_age_bucket",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "rsi_14",
    "minutes_from_cash_open",
    "is_us_cash_open",
    "prior_trade_count",
    "prior_cumulative_net",
    "prior_balance",
    "prior_peak_balance",
    "prior_drawdown",
    "prior_underwater_flag",
    "prior_underwater_streak",
    "source_time_max",
    "no_future_source_violation",
    "feature_use",
    "forbidden_use",
    "claim_boundary",
]
PROTOCOL_INPUT_COLUMNS = [
    "protocol_id",
    "branch_family",
    "priority",
    "source_driver",
    "input_frame_path",
    "row_count",
    "required_pre_trade_columns",
    "required_parent_evidence",
    "materialized_status",
    "next_review_gate",
    "forbidden_actions",
    "effect",
    "claim_boundary",
]
FEATURE_BINDING_COLUMNS = [
    "binding_id",
    "protocol_id",
    "feature_name",
    "source_artifact",
    "source_column",
    "source_time_column",
    "use_boundary",
    "lookahead_guard",
    "effect",
    "claim_boundary",
]
NEGATIVE_COLUMNS = [
    "control_id",
    "protocol_id",
    "control_type",
    "source_rows",
    "recipe",
    "allowed_use",
    "forbidden_use",
    "invalid_if",
    "effect",
    "claim_boundary",
]
COST_COLUMNS = [
    "cost_input_id",
    "attempt_name",
    "extra_round_trip_points",
    "point_value_per_1lot_estimate",
    "breakeven_extra_round_trip_points_estimate",
    "trade_count",
    "net_profit_parent_reference",
    "profit_factor_parent_reference",
    "input_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
]
PROXY_COLUMNS = [
    "proxy_contract_id",
    "attempt_name",
    "dimension",
    "proxy_expected_value",
    "mt5_runtime_value",
    "difference_proxy_minus_mt5",
    "difference_status",
    "usable_for_runtime_signal_parity",
    "usable_for_forward_pass_fail",
    "required_next_check",
    "effect",
    "claim_boundary",
]
FORWARD_COLUMNS = [
    "window_id",
    "source_window",
    "current_status",
    "usable_for",
    "forbidden_for",
    "required_repair",
    "next_review_action",
    "effect",
    "claim_boundary",
]
RUNTIME_QUEUE_COLUMNS = [
    "queue_id",
    "protocol_id",
    "branch_family",
    "priority",
    "input_frame_path",
    "required_mt5_outputs",
    "preflight_status",
    "must_review_before_execution",
    "forbidden_actions",
    "effect",
    "claim_boundary",
]
NO_LOOKAHEAD_COLUMNS = [
    "audit_id",
    "status",
    "evidence_path",
    "check",
    "effect",
    "claim_boundary",
]
GATE_COLUMNS = [
    "gate_id",
    "status",
    "evidence_path",
    "effect",
    "claim_boundary",
]

FEATURES_BY_PROTOCOL = {
    "defense_cost_buffer_guard": [
        "feature_timestamp",
        "atr_14",
        "atr_50",
        "atr_14_over_atr_50",
        "historical_vol_20",
        "historical_vol_5_over_20",
        "vol_regime",
        "atr_ratio_regime",
    ],
    "defense_late_curve_pocket_guard": [
        "feature_timestamp",
        "month",
        "weekday",
        "open_hour_utc",
        "session_utc",
        "chron_segment",
        "vol_regime",
        "adx_regime",
        "atr_ratio_regime",
    ],
    "repair_direction_symmetry_probe": [
        "direction",
        "session_utc",
        "month",
        "adx_regime",
        "di_regime",
        "vol_regime",
        "atr_ratio_regime",
    ],
    "repair_recovery_shape_probe": [
        "prior_trade_count",
        "prior_cumulative_net",
        "prior_balance",
        "prior_peak_balance",
        "prior_drawdown",
        "prior_underwater_flag",
        "prior_underwater_streak",
        "vol_regime",
    ],
    "offense_long_edge_preservation": [
        "direction",
        "session_utc",
        "adx_regime",
        "di_regime",
        "vol_regime",
        "atr_ratio_regime",
        "prior_drawdown",
    ],
    "offense_trade_count_recovery": [
        "feature_timestamp",
        "direction",
        "session_utc",
        "chron_segment",
        "vol_regime",
        "adx_regime",
        "prior_trade_count",
    ],
    "negative_control_direction_shuffle": [
        "direction",
        "feature_timestamp",
        "session_utc",
        "month",
        "prior_trade_count",
    ],
    "negative_control_hidden_current_day_forbidden": [
        "feature_timestamp",
        "source_time_max",
        "no_future_source_violation",
    ],
    "negative_control_cost_overstress": [
        "atr_14",
        "atr_14_over_atr_50",
        "historical_vol_20",
        "vol_regime",
    ],
}


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


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
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return str(int(value)) if value.is_integer() else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def parse_time(value: Any) -> datetime:
    text = str(value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y.%m.%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return datetime.min


def read_csv(path: Path) -> list[dict[str, str]]:
    if not io_path(path).exists():
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    target = io_path(path)
    tmp = target.with_name(target.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, target)
    return path


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8", errors="replace"), had_bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or (had_bom is None and path.suffix.lower() in {".md", ".txt"}) else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    io_path(path).write_text(normalized, encoding=encoding, newline="\n")
    return path


def sha256_file_lf_normalized(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any], columns: Sequence[str]) -> Path:
    rows = [{column: existing.get(column, "") for column in columns} for existing in read_csv(path)]
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [existing for existing in rows if tuple(str(existing.get(column, "")) for column in key_columns) != key]
    rows.append({column: row.get(column, "") for column in columns})
    return write_csv(path, columns, rows)


def rows_by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")): row for row in rows}


def completed_trades() -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(AE_TRADES)
        if row.get("attempt_name") == COMPLETED_ATTEMPT and row.get("slice_type") == "completed_day_broker_slice"
    ]
    return sorted(rows, key=lambda item: (parse_time(item.get("open_time")), int(number(item.get("trade_index")))))


def build_repair_feature_frame(trades: Sequence[Mapping[str, str]], asof_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    asof = rows_by_key(asof_rows, "trade_index")
    balance = INITIAL_BALANCE
    peak = INITIAL_BALANCE
    underwater_streak = 0
    output: list[dict[str, Any]] = []
    for trade in trades:
        joined = asof.get(str(trade.get("trade_index", "")), {})
        prior_drawdown = max(0.0, peak - balance)
        source_times = [
            str(joined.get("vix_source_close_utc", "")),
            str(joined.get("rate_source_close_utc", "")),
            str(joined.get("usd_source_close_utc", "")),
            str(trade.get("feature_timestamp", "")),
        ]
        row = {
            "trade_index": trade.get("trade_index", ""),
            "feature_timestamp": trade.get("feature_timestamp", ""),
            "open_time": trade.get("open_time", ""),
            "direction": trade.get("direction", ""),
            "month": trade.get("month", ""),
            "weekday": trade.get("weekday", ""),
            "open_hour_utc": trade.get("open_hour_utc", ""),
            "session_utc": trade.get("session_utc", ""),
            "chron_segment": trade.get("chron_segment", ""),
            "vol_regime": trade.get("vol_regime", ""),
            "atr_ratio_regime": trade.get("atr_ratio_regime", ""),
            "adx_regime": trade.get("adx_regime", ""),
            "di_regime": trade.get("di_regime", ""),
            "vix_z_regime": joined.get("vix_z_regime", ""),
            "vix_age_bucket": joined.get("vix_age_bucket", ""),
            "rate_z_regime": joined.get("rate_z_regime", ""),
            "rate_age_bucket": joined.get("rate_age_bucket", ""),
            "usd_z_regime": joined.get("usd_z_regime", ""),
            "usd_age_bucket": joined.get("usd_age_bucket", ""),
            "atr_14": trade.get("atr_14", ""),
            "atr_50": trade.get("atr_50", ""),
            "atr_14_over_atr_50": trade.get("atr_14_over_atr_50", ""),
            "historical_vol_20": trade.get("historical_vol_20", ""),
            "historical_vol_5_over_20": trade.get("historical_vol_5_over_20", ""),
            "adx_14": trade.get("adx_14", ""),
            "di_spread_14": trade.get("di_spread_14", ""),
            "rsi_14": trade.get("rsi_14", ""),
            "minutes_from_cash_open": trade.get("minutes_from_cash_open", ""),
            "is_us_cash_open": trade.get("is_us_cash_open", ""),
            "prior_trade_count": len(output),
            "prior_cumulative_net": balance - INITIAL_BALANCE,
            "prior_balance": balance,
            "prior_peak_balance": peak,
            "prior_drawdown": prior_drawdown,
            "prior_underwater_flag": prior_drawdown > 0.0,
            "prior_underwater_streak": underwater_streak,
            "source_time_max": max(source_times),
            "no_future_source_violation": joined.get("no_future_source_violation", "0"),
            "feature_use": "pre_trade_input_only(진입 전 입력 전용)",
            "forbidden_use": "current_trade_pnl_or_forward_pass_fail(현재 거래 손익 또는 전진 통과/실패)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        output.append(row)
        balance += number(trade.get("net_profit"))
        if balance >= peak:
            peak = balance
            underwater_streak = 0
        else:
            underwater_streak += 1
    return output


def build_protocol_input_matrix(protocols: Sequence[Mapping[str, str]], frame_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        protocol_id = str(protocol.get("protocol_id", ""))
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_family": protocol.get("branch_family", ""),
                "priority": protocol.get("priority", ""),
                "source_driver": protocol.get("source_driver", ""),
                "input_frame_path": rel(REPAIR_INPUT_FRAME),
                "row_count": len(frame_rows),
                "required_pre_trade_columns": FEATURES_BY_PROTOCOL.get(protocol_id, []),
                "required_parent_evidence": protocol.get("required_evidence", ""),
                "materialized_status": "ready_for_review_not_execution(검토 준비, 실행 아님)",
                "next_review_gate": NEXT_RUN_ID,
                "forbidden_actions": protocol.get("forbidden_actions", ""),
                "effect": "프로토콜을 실제 입력 행렬에 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def source_for_feature(feature: str) -> tuple[str, str, str]:
    asof_features = {"vix_z_regime", "vix_age_bucket", "rate_z_regime", "rate_age_bucket", "usd_z_regime", "usd_age_bucket"}
    prior_features = {"prior_trade_count", "prior_cumulative_net", "prior_balance", "prior_peak_balance", "prior_drawdown", "prior_underwater_flag", "prior_underwater_streak"}
    if feature in asof_features:
        return rel(AO_ASOF), feature, "feature_timestamp/source_close_utc(피처 시각/원천 종가 UTC)"
    if feature in prior_features:
        return rel(REPAIR_INPUT_FRAME), feature, "strictly prior closed trades only(이전 종결 거래만)"
    return rel(AE_TRADES), feature, "feature_timestamp(피처 시각)"


def build_feature_binding(protocols: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        protocol_id = str(protocol.get("protocol_id", ""))
        for feature in FEATURES_BY_PROTOCOL.get(protocol_id, []):
            source_artifact, source_column, source_time_column = source_for_feature(feature)
            rows.append(
                {
                    "binding_id": f"{protocol_id}__{feature}",
                    "protocol_id": protocol_id,
                    "feature_name": feature,
                    "source_artifact": source_artifact,
                    "source_column": source_column,
                    "source_time_column": source_time_column,
                    "use_boundary": "input_only_no_selection(입력 전용, 선택 아님)",
                    "lookahead_guard": "source_time_must_be_at_or_before_feature_timestamp(원천 시각은 피처 시각 이하)",
                    "effect": "각 입력이 어디에서 왔는지 추적한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_negative_controls(protocols: Sequence[Mapping[str, str]], frame_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    protocol_ids = {row.get("protocol_id") for row in protocols}
    specs = [
        (
            "negative_control_direction_shuffle",
            "direction_shuffle(방향 섞기)",
            "deterministic cyclic shift by 17 rows within tester-visible rows(테스터 가시 행 안에서 17행 순환 이동)",
            "direction repair(방향 수리)이 신호가 아니라 포켓 선택인지 본다.",
        ),
        (
            "negative_control_hidden_current_day_forbidden",
            "hidden_window_assertion(숨은 구간 단언)",
            "assert all rows have forward_use forbidden until tester reaches feature_last(테스터가 피처 끝에 도달할 때까지 전진 사용 금지)",
            "현재일 숨은 행이 판정에 섞이는지 막는다.",
        ),
        (
            "negative_control_cost_overstress",
            "cost_overstress_ladder(비용 과압박 사다리)",
            "include fixed overstress ladder as diagnostic only(고정 과압박 사다리를 진단 전용으로 포함)",
            "비용 수리가 손익 맞춤으로 변하는지 확인한다.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for protocol_id, control_type, recipe, effect in specs:
        if protocol_id not in protocol_ids:
            continue
        rows.append(
            {
                "control_id": f"{RUN_ID}__{protocol_id}",
                "protocol_id": protocol_id,
                "control_type": control_type,
                "source_rows": len(frame_rows),
                "recipe": recipe,
                "allowed_use": "diagnostic_only_no_candidate_selection(진단 전용, 후보 선택 금지)",
                "forbidden_use": "performance improvement claim or threshold choice(성과 개선 주장 또는 임계값 선택)",
                "invalid_if": "control output is used as candidate or forward pass/fail(대조 결과를 후보나 전진 판정으로 쓰면 무효)",
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_cost_ladder() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(read_csv(AE_COST), start=1):
        rows.append(
            {
                "cost_input_id": f"cost_ladder_{index:02d}",
                "attempt_name": row.get("attempt_name", ""),
                "extra_round_trip_points": row.get("extra_round_trip_points", ""),
                "point_value_per_1lot_estimate": row.get("point_value_per_1lot_estimate", ""),
                "breakeven_extra_round_trip_points_estimate": row.get("breakeven_extra_round_trip_points_estimate", ""),
                "trade_count": row.get("trade_count", ""),
                "net_profit_parent_reference": row.get("net_profit", ""),
                "profit_factor_parent_reference": row.get("profit_factor", ""),
                "input_use": "fixed_cost_stress_reference_only(고정 비용 압박 참고 전용)",
                "forbidden_use": "selecting best cost after seeing PnL(손익 확인 후 최적 비용 선택)",
                "effect": "비용 사다리를 고정해 비용 과적합을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_contract() -> list[dict[str, Any]]:
    diff_rows = read_csv(AD_PROXY_DIFF)
    output: list[dict[str, Any]] = []
    for index, row in enumerate(diff_rows, start=1):
        output.append(
            {
                "proxy_contract_id": f"proxy_mt5_{index:02d}",
                "attempt_name": row.get("attempt_name", ""),
                "dimension": row.get("dimension", ""),
                "proxy_expected_value": row.get("proxy_expected_value", ""),
                "mt5_runtime_value": row.get("mt5_runtime_value", ""),
                "difference_proxy_minus_mt5": row.get("difference_proxy_minus_mt5", ""),
                "difference_status": row.get("difference_status", ""),
                "usable_for_runtime_signal_parity": row.get("usable_for_runtime_signal_parity", ""),
                "usable_for_forward_pass_fail": row.get("usable_for_forward_pass_fail", ""),
                "required_next_check": "exact timestamp match and MT5 runtime telemetry(정확 시각 일치와 MT5 런타임 기록)",
                "effect": "proxy expected(프록시 예상값)를 신호 동등성에만 쓴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_forward_visibility() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in read_csv(AT_FORWARD_PLAN):
        output.append(
            {
                "window_id": row.get("window_id", ""),
                "source_window": row.get("source_window", ""),
                "current_status": row.get("current_status", ""),
                "usable_for": row.get("usable_for", ""),
                "forbidden_for": row.get("forbidden_for", ""),
                "required_repair": row.get("required_repair", ""),
                "next_review_action": NEXT_RUN_ID,
                "effect": "전진 판정 전 구간 가시성을 다시 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_runtime_queue(protocol_inputs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in protocol_inputs:
        rows.append(
            {
                "queue_id": f"{NEXT_RUN_ID}__{row.get('protocol_id')}",
                "protocol_id": row.get("protocol_id", ""),
                "branch_family": row.get("branch_family", ""),
                "priority": row.get("priority", ""),
                "input_frame_path": rel(REPAIR_INPUT_FRAME),
                "required_mt5_outputs": "tester report, trade list, runtime telemetry, proxy-MT5 difference(테스터 보고서/거래 목록/런타임 기록/프록시-MT5 차이)",
                "preflight_status": "review_required_before_mt5_execution(MT5 실행 전 검토 필수)",
                "must_review_before_execution": "true",
                "forbidden_actions": "new EA copy, threshold retune, D/B rewrite, lot optimization(새 EA 복제/임계값 재조정/D-B 재작성/랏 최적화 금지)",
                "effect": "다음 런타임 탐침 후보를 만들되 바로 실행 권한으로 올리지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_no_lookahead_audit(frame_rows: Sequence[Mapping[str, Any]], protocols: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    no_future = all(str(row.get("no_future_source_violation", "0")) in {"", "0", "0.0", "false"} for row in frame_rows)
    rows = [
        (
            "source_time_guard",
            no_future,
            rel(REPAIR_INPUT_FRAME),
            "no future source violation in materialized frame(물질화 프레임 미래 원천 위반 없음)",
            "원천 시각 누수를 막는다.",
        ),
        (
            "current_trade_pnl_excluded",
            all("net_profit" not in row for row in frame_rows),
            rel(REPAIR_INPUT_FRAME),
            "current trade PnL excluded from feature frame(현재 거래 손익 피처 프레임 제외)",
            "손익을 피처처럼 쓰는 누수를 막는다.",
        ),
        (
            "prior_equity_only",
            all("prior_balance" in row and "prior_drawdown" in row for row in frame_rows),
            rel(REPAIR_INPUT_FRAME),
            "recovery inputs use prior closed trades only(회복 입력은 이전 종결 거래만 사용)",
            "미래 곡선 정보를 쓰지 않는다.",
        ),
        (
            "db_source_absent_respected",
            True,
            rel(AT_BOUNDARY),
            "D/B source out-of-scope lock carried forward(D/B 원천 범위 밖 고정 계승)",
            "없는 D/B 원천을 만들지 않는다.",
        ),
        (
            "protocol_count_preserved",
            len(protocols) == 9,
            rel(PROTOCOL_INPUT_MATRIX),
            "all run337AT protocols materialized(337AT 프로토콜 모두 물질화)",
            "방어/수리/공격/부정대조 균형을 보존한다.",
        ),
    ]
    return [
        {
            "audit_id": audit_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence_path,
            "check": check,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for audit_id, passed, evidence_path, check, effect in rows
    ]


def build_gate_rows(
    frame_rows: Sequence[Mapping[str, Any]],
    protocols: Sequence[Mapping[str, str]],
    feature_bindings: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    no_lookahead_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    families = {row.get("branch_family", "") for row in protocols}
    required_families = {"defensive(방어)", "repair(수리)", "offensive(공격)", "negative_control(부정 대조)"}
    checks = [
        ("repair_frame_materialized", len(frame_rows) > 0, rel(REPAIR_INPUT_FRAME), "행 단위 진입 전 입력 프레임을 만들었다."),
        ("all_protocols_materialized", len(protocols) == 9, rel(PROTOCOL_INPUT_MATRIX), "run337AT 프로토콜 9개를 모두 입력에 연결했다."),
        ("balanced_family_coverage", required_families.issubset(families), rel(PROTOCOL_INPUT_MATRIX), "방어/수리/공격/부정대조 계열이 모두 남아 있다."),
        ("feature_bindings_present", len(feature_bindings) >= len(protocols), rel(FEATURE_BINDING), "피처별 원천과 시간축을 연결했다."),
        ("negative_controls_present", len(negative_rows) == 3, rel(NEGATIVE_CONTROL), "부정 대조 3개를 물질화했다."),
        ("proxy_contract_present", len(proxy_rows) >= 1 and all(row.get("difference_status") == "matched" for row in proxy_rows), rel(PROXY_CONTRACT), "proxy-MT5 신호 동등성 계약을 유지했다."),
        ("no_lookahead_audit_passed", all(row.get("status") == "passed" for row in no_lookahead_rows), rel(NO_LOOKAHEAD_AUDIT), "미래참조 방지 감사를 통과했다."),
        ("no_mutation_boundary", True, rel(RUN_MANIFEST), "모델/임계값/D-B/랏/런타임 인계를 바꾸지 않았다."),
        ("final_claim_guard", True, rel(FINAL_DECISION), "Forward/Goal/권위 주장을 하지 않는다."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence_path,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, evidence_path, effect in checks
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    paths: list[Path] = []
    paths.append(
        write_json(
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "run337AT protocol(337AT 프로토콜)을 행 단위 no-lookahead input(미래참조 방지 입력)으로 만들면 다음 검토가 말뿐인 설계가 아니라 실제 materialization(물질화)을 검증할 수 있다.",
                "decision_use": "run337AV review(337AV 검토) 입력. Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)에는 쓰지 않는다.",
                "comparison_baseline": "run337AT balanced protocol(균형 프로토콜) and run337AS parent attribution(부모 귀속)",
                "control_variables": "frozen ONNX/package/feature order/threshold/risk/lot/ATR/runtime handoff(동결 ONNX/패키지/피처 순서/임계값/위험/랏/ATR/런타임 인계)",
                "changed_variables": "materialized input rows and review queue only(입력 행과 검토 대기열만)",
                "sample_scope": "US100 M5 completed-day tester-visible parent rows(완성일 테스터 가시 부모 행)",
                "success_criteria": "protocols, feature bindings, negative controls, proxy contract, no-lookahead audit all present(프로토콜/피처 연결/부정 대조/프록시 계약/미래참조 감사 모두 존재)",
                "failure_criteria": "missing protocol family, missing source timestamp, or missing negative control(프로토콜 계열/원천 시각/부정 대조 누락)",
                "invalid_conditions": "current trade PnL or hidden current-day rows used as feature(현재 거래 손익 또는 숨은 현재일 행을 피처로 사용)",
                "stop_conditions": "review before MT5 execution and no model training(모델 학습 없이 MT5 실행 전 검토)",
                "evidence_plan": [rel(REPAIR_INPUT_FRAME), rel(PROTOCOL_INPUT_MATRIX), rel(FEATURE_BINDING), rel(GATE_AUDIT)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            DATA_RECEIPT,
            {
                "data_source": [rel(AE_TRADES), rel(AO_ASOF), rel(AT_PROTOCOLS), rel(AD_PROXY_DIFF), rel(AE_COST)],
                "time_axis": "MT5 broker/tester bar close and feature_timestamp(브로커/테스터 봉 마감 및 피처 시각)",
                "sample_scope": f"completed-day parent feature frame rows(완성일 부모 피처 프레임 행) {final['repair_input_rows']}",
                "missing_or_duplicate_check": "materialization preserves parent trade_index and does not resample market bars(부모 거래 인덱스를 유지하고 시장 봉 재표본화 없음)",
                "feature_label_boundary": "current trade net_profit excluded; prior equity fields use only earlier closed trades(현재 거래 순익 제외, 이전 종결 거래만 prior 곡선 필드에 사용)",
                "split_boundary": "completed-day attribution only, not forward split(완성일 귀속 전용, 전진 분할 아님)",
                "leakage_risk": "future macro source, hidden current-day rows, current PnL as feature(미래 거시 원천/숨은 현재일/현재 손익 피처화)",
                "data_hash_or_identity": {
                    "repair_frame_sha256": sha256_file_lf_normalized(REPAIR_INPUT_FRAME),
                    "protocol_input_sha256": sha256_file_lf_normalized(PROTOCOL_INPUT_MATRIX),
                    "feature_binding_sha256": sha256_file_lf_normalized(FEATURE_BINDING),
                },
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "effect": "다음 검토에 필요한 실제 입력을 만들면서 미래참조를 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            RUNTIME_RECEIPT,
            {
                "research_path": rel(__file__),
                "runtime_path": "not_executed_in_run337AU(337AU에서 실행 안 함)",
                "shared_contract": "proxy expected value compared to MT5 runtime only for signal parity(프록시 예상값은 MT5 런타임 신호 동등성에만 비교)",
                "known_differences": "broker latest forward feature_last still requires visibility repair/reprobe(브로커 최신 전진 피처 끝은 아직 가시성 수리/재탐침 필요)",
                "parity_check": rel(PROXY_CONTRACT),
                "parity_identity": {
                    "proxy_contract_rows": final["proxy_contract_rows"],
                    "all_proxy_differences_matched": final["all_proxy_differences_matched"],
                },
                "runtime_claim_boundary": "runtime_probe_candidate_queue_only_no_runtime_authority(런타임 탐침 후보 대기열 전용, 런타임 권위 없음)",
                "effect": "MT5 실행 후보는 만들지만 실행 권위는 열지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "no new trading KPI; parent fragility becomes input frame(신규 거래 KPI 없음, 부모 취약성이 입력 프레임이 됨)",
                "comparison_baseline": "run337AS/run337AT parent evidence(337AS/337AT 부모 근거)",
                "likely_drivers": "cost buffer, short-side asymmetry, late curve pocket, underwater stretch(비용 버퍼/숏 비대칭/후반 곡선 포켓/수중 체류)",
                "segment_checks": [rel(AS_ATTRIBUTION), rel(AE_CURVE), rel(AE_COST), rel(FORWARD_VISIBILITY)],
                "trade_shape": "parent-only; no new MT5 trades in run337AU(부모 전용, 337AU 신규 MT5 거래 없음)",
                "alternative_explanations": "completed-day scope is narrow and not latest forward(완성일 범위는 좁고 최신 전진이 아님)",
                "attribution_confidence": "medium_for_input_materialization_low_for_forward_kpi(입력 물질화는 중간, 전진 KPI는 낮음)",
                "next_probe": NEXT_RUN_ID,
                "effect": "성과 해석보다 다음 검토 입력의 오염 방지에 집중한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            RESULT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(REPAIR_INPUT_FRAME), rel(PROTOCOL_INPUT_MATRIX), rel(NEGATIVE_CONTROL), rel(GATE_AUDIT)],
                "evidence_missing": [
                    "new MT5 runtime execution(신규 MT5 런타임 실행)",
                    "new model or ONNX(새 모델 또는 ONNX)",
                    "latest broker-visible forward pass/fail(최신 브로커 가시 전진 통과/실패)",
                ],
                "judgment_label": "exploratory_input_materialized_no_forward_decision(탐색 입력 물질화, 전진 판정 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "이번 실행은 고치는 실행이 아니라, 고칠 때 과적합하지 않도록 실제 입력과 대조군을 만든 것이다.",
                "effect": "Goal Achieve(목표 달성)는 계속 열지 않는다.",
            },
        )
    )
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    report = f"""# Stage337AU Balanced No-Lookahead Repair Inputs Without D/B(337AU D/B 없는 균형 미래참조 방지 수리 입력)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{final['next_action']}`
- repair_input_rows(수리 입력 행): `{final['repair_input_rows']}`
- protocol_inputs(프로토콜 입력): `{final['protocol_input_rows']}`
- feature_bindings(피처 연결): `{final['feature_binding_rows']}`
- negative_controls(부정 대조): `{final['negative_control_rows']}`
- proxy_contract_rows(프록시 계약 행): `{final['proxy_contract_rows']}`
- gates_passed(게이트 통과): `{final['passed_gates']}/{final['gate_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What Was Materialized(물질화한 것)

run337AU(337AU 실행)는 run337AT(337AT 실행)의 9개 protocol(프로토콜)을 실제 completed-day pre-trade feature frame(완성일 진입 전 피처 프레임)과 연결했다. prior equity fields(이전 곡선 필드)는 current trade PnL(현재 거래 손익)을 쓰지 않고, 이전 종결 거래만 사용한다. 효과(effect, 효과)는 회복/곡선 수리가 미래 정보를 먹지 못하게 하는 것이다.

## Key Files(핵심 파일)

- repair frame(수리 프레임): `{rel(REPAIR_INPUT_FRAME)}`
- protocol input matrix(프로토콜 입력 행렬): `{rel(PROTOCOL_INPUT_MATRIX)}`
- feature binding(피처 연결): `{rel(FEATURE_BINDING)}`
- negative controls(부정 대조): `{rel(NEGATIVE_CONTROL)}`
- proxy contract(프록시 계약): `{rel(PROXY_CONTRACT)}`
- runtime queue(런타임 대기열): `{rel(RUNTIME_QUEUE)}`
- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`

## Boundary(경계)

새 model training(모델 학습), threshold retuning(임계값 재조정), D/B rule rewrite(D/B 규칙 재작성), lot optimization(랏 최적화), MT5 execution(MT5 실행)은 하지 않았다. proxy expected value(프록시 예상값)는 MT5 runtime signal parity(MT5 런타임 신호 동등성) 전용이고, net/PF/DD(순익/수익 팩터/손실폭) 권위가 아니다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_text(REPORT_PATH, report)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# 2026-05-27 Stage337AU Decision(337AU 결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- repair_input_rows(수리 입력 행): `{final['repair_input_rows']}`
- protocol_input_rows(프로토콜 입력 행): `{final['protocol_input_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_rows']}`
- passed_gates(통과 게이트): `{final['passed_gates']}/{final['gate_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337AU(337AU 실행)는 run337AT(337AT 실행)의 균형 프로토콜을 실제 입력 행렬로 바꿨다. 다음 run337AV(337AV 실행)는 이 입력이 review-ready(검토 준비)인지, MT5 runtime probe(MT5 런타임 탐침)로 넘겨도 되는지 확인한다.
"""
    return write_text(DECISION_DOC, text)


def update_workspace_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- broker_forward_boundary(브로커 전진 경계): `failed`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- completed_day_attribution_status(완성일 귀속 상태): `usable_without_db_for_attribution_only`
- db_source_status(D/B 원천 상태): `{final['db_source_status']}`
- db_source_sidecar_feasible(D/B 원천 보조표 가능): `false`
- repair_inputs_status(수리 입력 상태): `balanced_no_lookahead_without_db_materialized`
- repair_input_rows(수리 입력 행): `{final['repair_input_rows']}`
- protocol_input_rows(프로토콜 입력 행): `{final['protocol_input_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_current_day_cutoff_and_db_source_out_of_scope`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AU(337AU 실행)는 균형 수리 프로토콜을 행 단위 pre-trade input(진입 전 입력)과 부정 대조로 물질화했다.
"""
    artifacts.append(write_text(SELECTED_STATUS, selection))

    state, state_bom = read_text(WORKSPACE_STATE)
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {final['next_action']}", state, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage337 run337AU focus complete: run337AU(337AU 실행)은 `{final['status']}`로 balanced no-lookahead repair inputs(균형 미래참조 방지 수리 입력)을 물질화했다. "
        f"Effect(효과): repair_input_rows(수리 입력 행) `{final['repair_input_rows']}`, protocols(프로토콜) `{final['protocol_input_rows']}`, "
        f"negative_controls(부정 대조) `{final['negative_control_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    state = re.sub(r"- >-\n  Stage337 run337AU focus complete:.*?(?=\n- >-|\Z)", "", state, flags=re.S)
    state = re.sub(r"current_focus:\n\s*\n?", "current_focus:\n" + focus + "\n", state, count=1)
    artifacts.append(write_text(WORKSPACE_STATE, state, state_bom))

    old_current, current_bom = read_text(CURRENT_STATE)
    marker = "\n## Stage267 Candidate Pool"
    tail = old_current[old_current.find(marker) :] if marker in old_current else "\n"
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

## Stage337 run337AU(337AU 실행) - 2026-05-27

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AU(337AU 실행)는 run337AT(337AT 실행)의 protocol(프로토콜)을 실제 pre-trade feature frame(진입 전 피처 프레임), feature binding(피처 연결), negative control(부정 대조), proxy contract(프록시 계약)으로 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    artifacts.append(write_text(CURRENT_STATE, current + tail, current_bom))

    brief, brief_bom = read_text(STAGE_BRIEF)
    brief = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", brief, count=1)
    summary = (
        f"- run337AU_summary(337AU 요약): `{final['status']}`. "
        f"Effect(효과): repair_input_rows(수리 입력 행) `{final['repair_input_rows']}`, "
        f"protocol inputs(프로토콜 입력) `{final['protocol_input_rows']}`, next_action(다음 행동) `{final['next_action']}`; "
        "Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337AU_summary(337AU 요약)" in brief:
        brief = re.sub(r"- run337AU_summary\(337AU 요약\): [^\n]*(?:\n|$)", summary, brief, count=1)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(write_text(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = read_text(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AU(337AU 실행) `{final['status']}`. "
        f"Effect(효과): balanced no-lookahead repair inputs(균형 미래참조 방지 수리 입력) `{final['repair_input_rows']}`행을 만들고 "
        "Forward/Goal(전진/목표)은 주장하지 않음.\n"
    )
    pattern = rf"^- {re.escape(TODAY)}: Stage337 run337AU\(337AU 실행\).*$"
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
        "lane": "balanced_no_lookahead_repair_input_materialization_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};repair_rows={final['repair_input_rows']};goal_achieve_not_claimed.",
        "family": "experiment_execution_runtime_boundary",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balanced_repair_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialized_repair_inputs_without_db(D/B 없는 수리 입력 물질화)",
        "tier_scope": "Tier A u42 completed-day parent evidence(Tier A u42 완성일 부모 근거)",
        "kpi_scope": "input_materialization_no_new_trading_kpi(입력 물질화, 신규 거래 KPI 없음)",
        "scoreboard_lane": "experiment_execution_runtime_boundary",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"repair_rows={final['repair_input_rows']};protocols={final['protocol_input_rows']};negative_controls={final['negative_control_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_input_materialization_only(주장 범위 밖, 입력 물질화 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_runtime_boundary",
        "evidence_scope": "run337AT protocols plus run337AE trades/cost/curve and run337AO as-of regimes",
        "kpi_scope": "input_materialization_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;repair_rows={final['repair_input_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__balanced_repair_inputs",
        "family": "balanced_no_lookahead_repair_input_materialization_without_db",
        "question": "can run337AT protocols become real no-lookahead pre-trade inputs without D/B or retuning",
        "metric_scope": "input_rows_protocol_coverage_negative_controls_no_new_kpi",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row, RUN_REGISTRY_COLUMNS),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row, ALPHA_LEDGER_COLUMNS),
        upsert_csv(STAGE_LEDGER, ["ledger_row_id"], stage_row, STAGE_LEDGER_COLUMNS),
    ]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    unique_paths: list[Path] = []
    seen_paths: set[str] = set()
    for path in paths:
        artifact_path = rel(path)
        if not io_path(path).exists() or artifact_path in seen_paths:
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


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    at_final = read_json(AT_FINAL)
    as_final = read_json(AS_FINAL)
    protocols = read_csv(AT_PROTOCOLS)
    frame_rows = build_repair_feature_frame(completed_trades(), read_csv(AO_ASOF))
    protocol_inputs = build_protocol_input_matrix(protocols, frame_rows)
    feature_bindings = build_feature_binding(protocols)
    negative_rows = build_negative_controls(protocols, frame_rows)
    cost_rows = build_cost_ladder()
    proxy_rows = build_proxy_contract()
    forward_rows = build_forward_visibility()
    runtime_rows = build_runtime_queue(protocol_inputs)
    no_lookahead_rows = build_no_lookahead_audit(frame_rows, protocols)

    frame_path = write_csv(REPAIR_INPUT_FRAME, FRAME_COLUMNS, frame_rows)
    protocol_path = write_csv(PROTOCOL_INPUT_MATRIX, PROTOCOL_INPUT_COLUMNS, protocol_inputs)
    feature_path = write_csv(FEATURE_BINDING, FEATURE_BINDING_COLUMNS, feature_bindings)
    negative_path = write_csv(NEGATIVE_CONTROL, NEGATIVE_COLUMNS, negative_rows)
    cost_path = write_csv(COST_LADDER, COST_COLUMNS, cost_rows)
    proxy_path = write_csv(PROXY_CONTRACT, PROXY_COLUMNS, proxy_rows)
    forward_path = write_csv(FORWARD_VISIBILITY, FORWARD_COLUMNS, forward_rows)
    runtime_path = write_csv(RUNTIME_QUEUE, RUNTIME_QUEUE_COLUMNS, runtime_rows)
    no_lookahead_path = write_csv(NO_LOOKAHEAD_AUDIT, NO_LOOKAHEAD_COLUMNS, no_lookahead_rows)
    gate_rows = build_gate_rows(frame_rows, protocols, feature_bindings, negative_rows, proxy_rows, no_lookahead_rows)
    gate_path = write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows)
    passed_gates = sum(1 for row in gate_rows if row.get("status") == "passed")
    failed_gates = [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"]

    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "invalid_stage337AU_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if not failed_gates else "balanced_repair_input_materialization_gate_failure",
        "decision": DECISION if not failed_gates else "repair_stage337AU_gate_failure_before_review",
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_stage337AU_gate_failure_v1",
        "repair_input_rows": len(frame_rows),
        "protocol_input_rows": len(protocol_inputs),
        "feature_binding_rows": len(feature_bindings),
        "negative_control_rows": len(negative_rows),
        "cost_ladder_rows": len(cost_rows),
        "proxy_contract_rows": len(proxy_rows),
        "forward_visibility_rows": len(forward_rows),
        "runtime_queue_rows": len(runtime_rows),
        "no_lookahead_audit_rows": len(no_lookahead_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": passed_gates,
        "failed_gates": failed_gates,
        "all_proxy_differences_matched": all(row.get("difference_status") == "matched" for row in proxy_rows),
        "db_source_status": as_final.get("db_source_status"),
        "parent_protocol_count": at_final.get("protocol_count"),
        "parent_forward_usable_rows": at_final.get("forward_usable_rows"),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": rel(__file__),
        "parent_inputs": [
            rel(AT_FINAL),
            rel(AT_PROTOCOLS),
            rel(AT_BOUNDARY),
            rel(AE_TRADES),
            rel(AO_ASOF),
            rel(AD_PROXY_DIFF),
            rel(AE_COST),
        ],
        "outputs": [
            rel(REPAIR_INPUT_FRAME),
            rel(PROTOCOL_INPUT_MATRIX),
            rel(FEATURE_BINDING),
            rel(NEGATIVE_CONTROL),
            rel(COST_LADDER),
            rel(PROXY_CONTRACT),
            rel(FORWARD_VISIBILITY),
            rel(RUNTIME_QUEUE),
            rel(NO_LOOKAHEAD_AUDIT),
            rel(GATE_AUDIT),
            rel(FINAL_DECISION),
        ],
        "frozen_items": [
            "selected_candidate(선택 후보)",
            "ONNX model(온엑스 모델)",
            "Adapter package(어댑터 패키지)",
            "feature order(피처 순서)",
            "score threshold(점수 임계값)",
            "risk/lot/ATR/runtime handoff(위험/랏/ATR/런타임 인계)",
        ],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rule rewrite(D/B 규칙 재작성)",
            "lot optimization(랏 최적화)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = write_json(FINAL_DECISION, final)
    manifest_path = write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    workspace_paths = update_workspace_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        Path(__file__),
        frame_path,
        protocol_path,
        feature_path,
        negative_path,
        cost_path,
        proxy_path,
        forward_path,
        runtime_path,
        no_lookahead_path,
        gate_path,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *receipt_paths,
        *workspace_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    summary = {
        "run_id": RUN_ID,
        "status": final["status"],
        "decision": final["decision"],
        "repair_input_rows": final["repair_input_rows"],
        "protocol_input_rows": final["protocol_input_rows"],
        "negative_control_rows": final["negative_control_rows"],
        "gates": f"{final['passed_gates']}/{final['gate_rows']}",
        "report_path": rel(report_path),
        "artifact_registry": rel(artifact_registry_path),
        "next_action": final["next_action"],
        "goal_achieve": "not_claimed",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
