# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AS"
RUN_ID = "run337AS_completed_day_attribution_without_db_and_forward_window_lock_v1"
PARENT_RUN_ID = "run337AR_db_source_sidecar_feasibility_or_out_of_scope_lock_v1"
NEXT_RUN_ID = "run337AT_balanced_no_lookahead_repair_protocol_without_db_v1"

STATUS = "completed_stage337AS_completed_day_non_db_attribution_forward_window_locked_no_forward_decision"
JUDGMENT = "completed_day_attribution_usable_without_db_but_cost_direction_curve_fragility_remains"
DECISION = "stage337AS_open_run337AT_balanced_no_lookahead_repair_protocol_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AS_completed_day_non_db_attribution_forward_window_lock_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AS_completed_day_attribution_without_db_and_forward_window_lock.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AS_completed_day_attribution_without_db_and_forward_window_lock.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

AD_DIR = STAGE_DIR / "02_runs" / "run337AD"
AE_DIR = STAGE_DIR / "02_runs" / "run337AE"
AO_DIR = STAGE_DIR / "02_runs" / "run337AO"
AQ_DIR = STAGE_DIR / "02_runs" / "run337AQ"
AR_DIR = STAGE_DIR / "02_runs" / "run337AR"

TRADE_RECORDS = AE_DIR / "trade_records.csv"
REGIME_ATTRIBUTION = AE_DIR / "regime_attribution_report.csv"
COST_STRESS = AE_DIR / "cost_stress_report.csv"
CURVE_POCKET = AE_DIR / "curve_pocket_report.csv"
LOT_NORMALIZED = AE_DIR / "lot_normalized_report.csv"
ASOF_JOIN = AO_DIR / "asof_trade_regime_join.csv"
PROXY_USABILITY = AD_DIR / "proxy_usability_judgment.csv"
PROXY_DIFF = AD_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
PROXY_EXPECTED = AD_DIR / "timestamp_aligned_proxy_expected_result.csv"
KPI_SUMMARY = AD_DIR / "completed_day_forward_kpi_summary.csv"
GAP_COMPLETED_DAY = AD_DIR / "tester_feature_last_gap_completed_day_slice.csv"
AQ_FINAL = AQ_DIR / "final_decision.json"
AR_FINAL = AR_DIR / "final_decision.json"

NON_DB_ATTRIBUTION = RUN_DIR / "non_db_attribution_report.csv"
FORWARD_WINDOW_LOCK = RUN_DIR / "forward_window_lock_matrix.csv"
PROXY_MT5_USABILITY = RUN_DIR / "proxy_mt5_usability_matrix.csv"
FRAGILITY_DRIVER = RUN_DIR / "fragility_driver_matrix.csv"
REPAIR_QUEUE = RUN_DIR / "repair_protocol_seed_queue.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"

COMPLETED_ATTEMPT = "u42_plain_rf_ad_completed_day_broker_slice"
FULL_CONTROL_ATTEMPT = "u42_plain_rf_ad_full_current_day_broker_control"
DEPOSIT = 500.0

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
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y.%m.%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def profit_factor(values: Sequence[float]) -> float | None:
    gross_profit = sum(value for value in values if value > 0.0)
    gross_loss = -sum(value for value in values if value < 0.0)
    if gross_loss == 0.0:
        return math.inf if gross_profit > 0.0 else None
    return gross_profit / gross_loss


def drawdown(values_by_time: Sequence[tuple[datetime | None, float]]) -> tuple[float, int, float, str, str]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    longest = 0
    current = 0
    underwater = 0
    peak_time = ""
    start = ""
    end = ""
    for ts, pnl in sorted(values_by_time, key=lambda item: item[0] or datetime.min):
        balance += pnl
        close_text = ts.strftime("%Y-%m-%d %H:%M:%S") if ts else ""
        if balance >= peak:
            peak = balance
            peak_time = close_text
            current = 0
        else:
            current += 1
            underwater += 1
            longest = max(longest, current)
        dd = peak - balance
        if dd > max_dd:
            max_dd = dd
            start = peak_time
            end = close_text
    share = underwater / len(values_by_time) if values_by_time else 0.0
    return max_dd, longest, share, start, end


def metrics(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> dict[str, Any]:
    values = [number(row.get(key)) for row in rows]
    count = len(values)
    net = sum(values)
    gross_profit = sum(value for value in values if value > 0.0)
    gross_loss = sum(value for value in values if value < 0.0)
    wins = sum(1 for value in values if value > 0.0)
    losses = sum(1 for value in values if value < 0.0)
    dd, longest, underwater_share, dd_start, dd_end = drawdown([(parse_time(row.get("close_time")), number(row.get(key))) for row in rows])
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor(values),
        "expectancy": net / count if count else None,
        "win_count": wins,
        "loss_count": losses,
        "win_rate": wins / count if count else None,
        "average_win": gross_profit / wins if wins else None,
        "average_loss": gross_loss / losses if losses else None,
        "max_closed_drawdown": dd,
        "recovery_factor": net / dd if dd else None,
        "longest_underwater_trades": longest,
        "underwater_trade_share": underwater_share,
        "drawdown_start": dd_start,
        "drawdown_end": dd_end,
    }


def grouped(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, list[Mapping[str, Any]]]:
    output: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        bucket = str(row.get(key, "") or "missing")
        output[bucket].append(row)
    return output


def bucket_read(payload: Mapping[str, Any]) -> str:
    count = int(number(payload.get("trade_count")))
    net = number(payload.get("net_profit"))
    pf = payload.get("profit_factor")
    pf_value = number(pf, math.nan)
    if count < 20:
        return "small_sample_context_only(소표본 문맥 전용)"
    if net < 0:
        return "negative_fragility(음수 취약)"
    if math.isfinite(pf_value) and pf_value < 1.0:
        return "pf_below_one_fragility(PF 1 미만 취약)"
    if math.isfinite(pf_value) and pf_value < 1.10:
        return "thin_edge_fragility(얇은 엣지 취약)"
    if math.isfinite(pf_value) and pf_value < 1.20:
        return "cost_thin_constructive_but_fragile(수익은 있으나 비용 취약)"
    return "constructive_completed_day_only(완성일 한정 양호)"


def merge_asof(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    asof_by_index = {str(row.get("trade_index", "")): row for row in read_csv(ASOF_JOIN)}
    merged: list[dict[str, Any]] = []
    macro_fields = [
        "vix_z_regime",
        "vix_age_bucket",
        "rate_z_regime",
        "rate_age_bucket",
        "usd_z_regime",
        "usd_age_bucket",
        "no_future_source_violation",
    ]
    for row in trades:
        item = dict(row)
        asof = asof_by_index.get(str(row.get("trade_index", "")), {})
        for field in macro_fields:
            item[field] = asof.get(field, "")
        merged.append(item)
    return merged


def build_non_db_attribution(enriched_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = [
        "all",
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
    ]
    output: list[dict[str, Any]] = []
    for axis in axes:
        groups = {"all": list(enriched_rows)} if axis == "all" else grouped(enriched_rows, axis)
        for bucket, bucket_rows in sorted(groups.items(), key=lambda item: str(item[0])):
            payload = metrics(bucket_rows)
            output.append(
                {
                    "attempt_name": COMPLETED_ATTEMPT,
                    "slice_type": "completed_day_broker_slice",
                    "axis": axis,
                    "bucket": bucket,
                    **payload,
                    "bucket_read": bucket_read(payload),
                    "db_source_status": "out_of_scope_by_claim_no_timestamp_aligned_sidecar",
                    "forward_window_status": "completed_day_attribution_only_not_forward_pass_fail",
                    "effect": "D/B source(D/B 원천)를 쓰지 않고 검증 가능한 축으로만 성과를 분해한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return output


def build_forward_window_lock() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    gap_rows = read_csv(GAP_COMPLETED_DAY)
    kpi_rows = {row.get("attempt_name", ""): row for row in read_csv(KPI_SUMMARY)}
    aq_final = read_json(AQ_FINAL)
    ar_final = read_json(AR_FINAL)
    output: list[dict[str, Any]] = []
    for row in gap_rows:
        attempt = row.get("attempt_name", "")
        kpi = kpi_rows.get(attempt, {})
        gap_status = row.get("gap_status", "")
        if attempt == COMPLETED_ATTEMPT and gap_status == "tester_reached_feature_last":
            window_status = "allowed_for_completed_day_attribution_only"
            forward_use = "forbidden"
        elif attempt == FULL_CONTROL_ATTEMPT:
            window_status = "current_day_hidden_excluded_from_forward_decision"
            forward_use = "forbidden"
        else:
            window_status = "not_eligible"
            forward_use = "forbidden"
        output.append(
            {
                "attempt_name": attempt,
                "slice_type": kpi.get("slice_type", ""),
                "feature_last_timestamp": row.get("feature_last_timestamp", ""),
                "tester_last_observed_bar_time": row.get("tester_last_observed_bar_time", ""),
                "gap_status": gap_status,
                "tester_to_feature_last_gap_minutes": row.get("tester_to_feature_last_gap_minutes", ""),
                "tester_to_api_latest_gap_minutes": row.get("tester_to_api_latest_gap_minutes", ""),
                "runtime_status": row.get("runtime_status", ""),
                "report_status": row.get("report_status", ""),
                "trade_count": kpi.get("trade_count", ""),
                "net_profit": kpi.get("net_profit", ""),
                "profit_factor": kpi.get("profit_factor", ""),
                "trades_per_day": kpi.get("trades_per_day", ""),
                "window_status": window_status,
                "usable_for_attribution": "true" if attempt == COMPLETED_ATTEMPT else "context_only",
                "usable_for_forward_pass_fail": "false",
                "forward_use": forward_use,
                "db_source_status": ar_final.get("db_source_status", ""),
                "aq_current_day_gap_rows": aq_final.get("current_day_gap_rows", ""),
                "effect": "completed-day(완성일)는 귀속에는 쓰되 Forward Passed/Failed(전진 통과/실패)에는 쓰지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary = {
        "window_rows": len(output),
        "completed_day_attribution_rows": sum(1 for row in output if row["window_status"] == "allowed_for_completed_day_attribution_only"),
        "forward_usable_rows": sum(1 for row in output if row["usable_for_forward_pass_fail"] == "true"),
        "current_day_gap_rows": aq_final.get("current_day_gap_rows", 0),
    }
    return output, summary


def build_proxy_matrix() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    usability = {row.get("attempt_name", ""): row for row in read_csv(PROXY_USABILITY)}
    expected = {row.get("attempt_name", ""): row for row in read_csv(PROXY_EXPECTED)}
    diffs = read_csv(PROXY_DIFF)
    by_attempt: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in diffs:
        by_attempt[row.get("attempt_name", "")].append(row)
    output: list[dict[str, Any]] = []
    total_dimensions = 0
    matched_dimensions = 0
    for attempt, rows in sorted(by_attempt.items()):
        matched = sum(1 for row in rows if row.get("difference_status") == "matched")
        total = len(rows)
        total_dimensions += total
        matched_dimensions += matched
        u = usability.get(attempt, {})
        e = expected.get(attempt, {})
        output.append(
            {
                "attempt_name": attempt,
                "artifact_slug": e.get("artifact_slug", ""),
                "proxy_cutoff_utc": e.get("proxy_cutoff_utc", ""),
                "timestamp_aligned_feature_rows": e.get("timestamp_aligned_feature_rows", ""),
                "expected_signal_count": e.get("expected_signal_count", ""),
                "expected_long_count": e.get("expected_long_count", ""),
                "expected_short_count": e.get("expected_short_count", ""),
                "matched_dimensions": matched,
                "total_dimensions": total,
                "all_dimensions_matched": "true" if matched == total and total > 0 else "false",
                "diagnostic_usability": u.get("diagnostic_usability", ""),
                "forward_usability": u.get("forward_usability", ""),
                "gap_status": u.get("gap_status", ""),
                "runtime_signal_parity_read": "usable_for_signal_parity_only" if matched == total and total > 0 else "not_usable",
                "forward_kpi_read": "not_usable_for_forward_pass_fail",
                "effect": "proxy expected value(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)는 일치 여부만 신호 동등성에 쓴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary = {
        "proxy_attempts": len(output),
        "matched_dimensions": matched_dimensions,
        "total_dimensions": total_dimensions,
        "all_proxy_dimensions_matched": matched_dimensions == total_dimensions and total_dimensions > 0,
    }
    return output, summary


def first_row(rows: Sequence[Mapping[str, Any]], **conditions: str) -> Mapping[str, Any]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in conditions.items()):
            return row
    return {}


def build_fragility_driver(non_db_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cost_rows = read_csv(COST_STRESS)
    curve_rows = read_csv(CURVE_POCKET)
    direction_sell = first_row(non_db_rows, axis="direction", bucket="sell")
    chron_late = first_row(non_db_rows, axis="chron_segment", bucket="chron_late")
    overall = first_row(non_db_rows, axis="all", bucket="all")
    one_point = first_row(cost_rows, attempt_name=COMPLETED_ATTEMPT, extra_round_trip_points="1")
    five_point = first_row(cost_rows, attempt_name=COMPLETED_ATTEMPT, extra_round_trip_points="5")
    curve_summary = first_row(curve_rows, attempt_name=COMPLETED_ATTEMPT, pocket_type="attempt_summary")
    worst_month = first_row(curve_rows, attempt_name=COMPLETED_ATTEMPT, pocket_type="worst_month")
    drivers = [
        {
            "driver_id": "direction_short_side_fragility",
            "severity": "high",
            "evidence_value": f"net={direction_sell.get('net_profit','')};pf={direction_sell.get('profit_factor','')};trades={direction_sell.get('trade_count','')}",
            "read": "short side(sell, 매도 방향)가 completed-day(완성일)에서 음수이고 PF가 낮다.",
            "repair_seed": "direction-symmetry repair(방향 대칭 수리) with no threshold search(임계값 탐색 없음)",
            "effect": "롱 중심 수익이 숏 취약성을 가리는 일을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "driver_id": "chron_late_curve_pocket",
            "severity": "high",
            "evidence_value": f"net={chron_late.get('net_profit','')};pf={chron_late.get('profit_factor','')};trades={chron_late.get('trade_count','')}",
            "read": "late chronological pocket(후반 시간 포켓)이 음수라 curve pocket(곡선 포켓) 위험이 남는다.",
            "repair_seed": "timestamp-safe pocket guard design(시점 안전 포켓 방어 설계)",
            "effect": "후반부 손상 구간을 전체 수익으로 덮지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "driver_id": "cost_buffer_thin",
            "severity": "high",
            "evidence_value": f"one_point_pf={one_point.get('profit_factor','')};five_point_net={five_point.get('net_profit','')}",
            "read": "one-point stress(1포인트 비용 압박)도 PF가 얇고 five-point stress(5포인트 비용 압박)는 순손실이다.",
            "repair_seed": "cost-buffer first pass(비용 버퍼 우선 회차)",
            "effect": "실행 비용에 취약한 표면을 수익처럼 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "driver_id": "underwater_stretch",
            "severity": "medium",
            "evidence_value": f"underwater_share={overall.get('underwater_trade_share','')};longest={overall.get('longest_underwater_trades','')};dd={overall.get('max_closed_drawdown','')}",
            "read": "underwater stretch(수중 체류)가 길어 곡선 품질이 운영 수준이 아니다.",
            "repair_seed": "recovery-shape diagnostic(회복 형태 진단)",
            "effect": "단순 순수익보다 곡선 회복 품질을 우선 검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "driver_id": "db_source_absent",
            "severity": "scope_lock",
            "evidence_value": "direct_sidecar_ready=0",
            "read": "D/B source(D/B 원천)는 없으므로 D/B attribution(D/B 귀속)은 제외한다.",
            "repair_seed": "no D/B attribution; use direction/regime/cost/curve axes only(D/B 귀속 제외, 방향/국면/비용/곡선 축만 사용)",
            "effect": "없는 원천으로 수리 대상을 만들지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "driver_id": "forward_window_hidden",
            "severity": "scope_lock",
            "evidence_value": f"curve_read={curve_summary.get('curve_read','')};worst_month_net={worst_month.get('net_profit','')}",
            "read": "current-day intraday(현재일 장중) window(구간)는 tester cutoff(테스터 컷오프) 때문에 Forward Passed/Failed(전진 통과/실패)에 쓰지 않는다.",
            "repair_seed": "completed-day attribution-only until broker-visible latest window(브로커 가시 최신 구간 전까지 완성일 귀속 전용)",
            "effect": "가시성 없는 데이터를 전진 판정으로 끌어올리지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    summary = {
        "high_driver_count": sum(1 for row in drivers if row["severity"] == "high"),
        "scope_lock_count": sum(1 for row in drivers if row["severity"] == "scope_lock"),
        "overall_net": overall.get("net_profit", ""),
        "overall_pf": overall.get("profit_factor", ""),
        "overall_trade_count": overall.get("trade_count", ""),
    }
    return drivers, summary


def build_repair_queue(drivers: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    priority = {
        "direction_short_side_fragility": "P0",
        "cost_buffer_thin": "P0",
        "chron_late_curve_pocket": "P0",
        "underwater_stretch": "P1",
        "db_source_absent": "guardrail",
        "forward_window_hidden": "guardrail",
    }
    output: list[dict[str, Any]] = []
    for row in drivers:
        driver_id = str(row.get("driver_id", ""))
        output.append(
            {
                "queue_id": f"run337AT_seed__{driver_id}",
                "priority": priority.get(driver_id, "P2"),
                "source_driver": driver_id,
                "allowed_next_action": row.get("repair_seed", ""),
                "forbidden_action": "threshold retune, D/B rule rewrite, lot optimization, look-ahead filter(임계값 재조정/D-B 규칙 재작성/랏 최적화/미래참조 필터 금지)",
                "required_evidence": "predeclared protocol(사전 선언 프로토콜), proxy-vs-MT5 parity(프록시 대 MT5 동등성), broker-visible tester evidence(브로커 가시 테스터 근거)",
                "effect": "다음 수리 실험이 수익 구간에 맞춘 과적합으로 흐르지 않게 한다.",
                "next_run": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    paths: list[Path] = []
    paths.append(
        write_json(
            DATA_RECEIPT,
            {
                "data_source": [rel(TRADE_RECORDS), rel(ASOF_JOIN), rel(PROXY_DIFF), rel(AQ_FINAL), rel(AR_FINAL)],
                "time_axis": "MT5 Strategy Tester bar/trade timestamps(메타트레이더5 전략 테스터 봉/거래 시각); completed-day feature_last(완성일 피처 끝)은 2026-05-26T23:55:00Z이고 current-day(현재일)는 tester cutoff(테스터 컷오프) 뒤라 Forward Passed/Failed(전진 통과/실패)에 쓰지 않는다.",
                "sample_scope": f"US100 M5 completed-day broker slice(완성일 브로커 구간) {final['trade_count']} trades from {final['first_trade_time']} to {final['last_trade_time']}.",
                "missing_or_duplicate_check": "D/B source(D/B 원천)는 run337AR에서 out_of_scope_by_claim(주장 범위 밖)으로 고정; market row duplicate check(시장 행 중복 검사)는 새로 하지 않고 기존 MT5 report parse(보고서 파싱) 결과를 재사용한다.",
                "feature_label_boundary": "No model training, no relabeling, no threshold retuning, no lot optimization(모델 학습/재라벨링/임계값 재조정/랏 최적화 없음).",
                "split_boundary": "Completed-day runtime attribution only(완성일 런타임 귀속 전용); not a forward pass/fail split(전진 통과/실패 분할 아님).",
                "leakage_risk": "Using hidden current-day rows or D/B direction proxy as source(숨은 현재일 행 또는 방향 대리값을 D/B 원천으로 쓰는 위험). Both are locked out(둘 다 배제).",
                "data_hash_or_identity": {
                    "trade_records_sha256": sha256_file_lf_normalized(TRADE_RECORDS),
                    "asof_join_sha256": sha256_file_lf_normalized(ASOF_JOIN),
                    "non_db_attribution_sha256": sha256_file_lf_normalized(NON_DB_ATTRIBUTION),
                },
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "effect": "완성일 귀속은 가능하지만 전진 판정으로 승격하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "D/B attribution(D/B 귀속)을 제거하고 completed-day(완성일) 성과를 direction/regime/cost/curve(방향/국면/비용/곡선) 축으로 재분해했다.",
                "comparison_baseline": "run337AE completed-day attribution/cost stress(337AE 완성일 귀속/비용 압박) plus run337AR D/B sidecar lock(337AR D/B 보조표 고정)",
                "likely_drivers": [
                    "short-side negative expectancy(숏 방향 음수 기대값)",
                    "chron_late curve pocket(후반 곡선 포켓)",
                    "thin cost buffer(얇은 비용 버퍼)",
                    "long underwater stretch(긴 수중 체류)",
                ],
                "segment_checks": [rel(NON_DB_ATTRIBUTION), rel(FRAGILITY_DRIVER), rel(FORWARD_WINDOW_LOCK)],
                "trade_shape": {
                    "trade_count": final["trade_count"],
                    "net_profit": final["net_profit"],
                    "profit_factor": final["profit_factor"],
                    "max_closed_drawdown": final["max_closed_drawdown"],
                    "underwater_trade_share": final["underwater_trade_share"],
                },
                "alternative_explanations": [
                    "completed-day window is tester-visible but not full latest broker forward(완성일 구간은 테스터 가시지만 최신 브로커 전진 전체가 아님)",
                    "u42 technical-only feature set lacks external D/B and macro model inputs(u42 기술 피처 세트에는 외부 D/B 및 거시 모델 입력이 없음)",
                ],
                "attribution_confidence": "medium_with_forward_boundary(전진 경계 포함 중간)",
                "next_probe": NEXT_RUN_ID,
                "effect": "수익 숫자보다 취약한 성과 구조를 다음 수리 조건으로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            RUNTIME_RECEIPT,
            {
                "research_path": rel(__file__),
                "runtime_path": rel(AD_DIR / "runtime_telemetry"),
                "shared_contract": "Frozen ONNX, feature order, score threshold, risk, lot, ATR exits, runtime handoff(고정 ONNX/피처 순서/점수 임계값/위험/랏/ATR 청산/런타임 인계) unchanged(변경 없음).",
                "known_differences": "run337AS does not run a new Strategy Tester(새 전략 테스터 실행 없음); it reuses run337AD MT5 runtime probe(337AD MT5 런타임 탐침) and timestamp-aligned proxy comparison(시점 정렬 프록시 비교).",
                "parity_check": rel(PROXY_MT5_USABILITY),
                "parity_identity": {
                    "proxy_attempts": final["proxy_attempts"],
                    "matched_dimensions": final["proxy_matched_dimensions"],
                    "total_dimensions": final["proxy_total_dimensions"],
                },
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority(런타임 탐침 전용, 런타임 권위 없음)",
                "effect": "proxy expected(프록시 예상값)는 MT5 runtime(런타임) 신호 동등성에만 쓰고 KPI 권위로 쓰지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            RESULT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(NON_DB_ATTRIBUTION), rel(FORWARD_WINDOW_LOCK), rel(PROXY_MT5_USABILITY), rel(FRAGILITY_DRIVER)],
                "evidence_missing": [
                    "broker-visible latest current-day forward window(브로커 가시 최신 현재일 전진 구간)",
                    "timestamp-aligned D/B source sidecar(시점 정렬 D/B 원천 보조표)",
                    "new no-lookahead repaired candidate runtime proof(미래참조 없는 수리 후보 런타임 증명)",
                ],
                "judgment_label": "inconclusive_forward_boundary_negative_fragility_evidence(전진 경계 불충분 및 취약 근거)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "완성일 구간은 분석에 쓸 수 있지만, D/B 원천과 최신 전진 구간이 없어서 성공 판정은 아니다. 숏, 후반 포켓, 비용 버퍼가 다음 수리 대상이다.",
            },
        )
    )
    return paths


def build_gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "db_out_of_scope_lock_respected",
            "status": "passed" if final["db_source_status"] == "out_of_scope_by_claim_no_timestamp_aligned_sidecar" else "failed",
            "evidence_path": rel(AR_FINAL),
            "effect": "D/B 귀속을 만들지 않고 제외한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "completed_day_window_attribution_only",
            "status": "passed" if final["forward_usable_rows"] == 0 else "failed",
            "evidence_path": rel(FORWARD_WINDOW_LOCK),
            "effect": "완성일 구간을 전진 성공/실패 판정으로 승격하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_usability_judged",
            "status": "passed" if final["proxy_total_dimensions"] and final["proxy_matched_dimensions"] == final["proxy_total_dimensions"] else "failed",
            "evidence_path": rel(PROXY_MT5_USABILITY),
            "effect": "프록시 예상값과 MT5 런타임 탐침 차이를 활용성까지 판정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "fragility_driver_queue_materialized",
            "status": "passed" if final["repair_queue_rows"] >= 1 else "failed",
            "evidence_path": rel(REPAIR_QUEUE),
            "effect": "취약 축을 다음 수리 프로토콜로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_mutation_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_MANIFEST),
            "effect": "모델/임계값/D-B 규칙/랏/런타임 인계를 변경하지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_goal_claim_boundary",
            "status": "passed",
            "evidence_path": rel(FINAL_DECISION),
            "effect": "Forward Passed/Failed와 Goal Achieve를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_report(final: Mapping[str, Any], fragility_rows: Sequence[Mapping[str, Any]]) -> Path:
    top = [row for row in read_csv(NON_DB_ATTRIBUTION) if row.get("axis") in {"all", "direction", "chron_segment"}]
    report = f"""# Stage337AS Completed-Day Attribution Without D/B(337AS D/B 제외 완성일 귀속)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- trade_count(거래 수): `{final['trade_count']}`
- net_profit(순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- max_closed_drawdown(최대 종가 손실폭): `{final['max_closed_drawdown']}`
- underwater_trade_share(수중 체류 거래 비중): `{final['underwater_trade_share']}`
- proxy match(프록시 일치): `{final['proxy_matched_dimensions']}/{final['proxy_total_dimensions']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Window Lock(구간 고정)

completed-day broker slice(완성일 브로커 구간)는 attribution-only(귀속 전용)이다. current-day intraday(현재일 장중) 구간은 tester cutoff(테스터 컷오프) 뒤라 Forward Passed/Failed(전진 통과/실패)에 쓰지 않는다. 효과(effect, 효과)는 보이는 구간 분석과 보이지 않는 전진 판정을 섞지 않는 것이다.

## Non-D/B Attribution(D/B 제외 귀속)

| axis(축) | bucket(버킷) | trades(거래) | net(순익) | PF(수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
"""
    for row in top:
        report += (
            f"| `{row.get('axis','')}` | `{row.get('bucket','')}` | `{row.get('trade_count','')}` | "
            f"`{row.get('net_profit','')}` | `{row.get('profit_factor','')}` | `{row.get('bucket_read','')}` |\n"
        )
    report += """
## Fragility Drivers(취약 동인)

| driver(동인) | severity(강도) | evidence(근거) | repair seed(수리 씨앗) |
|---|---|---|---|
"""
    for row in fragility_rows:
        report += (
            f"| `{row.get('driver_id','')}` | `{row.get('severity','')}` | "
            f"{row.get('evidence_value','')} | {row.get('repair_seed','')} |\n"
        )
    report += """
## Boundary(경계)

D/B attribution(D/B 귀속)은 run337AR에서 out_of_scope_by_claim(주장 범위 밖)으로 고정했다. run337AS는 모델 학습(model training, 모델 학습), threshold retuning(임계값 재조정), D/B rule rewrite(D/B 규칙 재작성), lot optimization(랏 최적화)을 하지 않았다. 다음 작업은 `run337AT_balanced_no_lookahead_repair_protocol_without_db_v1`에서 direction/cost/curve(방향/비용/곡선) 수리를 사전 선언 프로토콜로 설계하는 것이다.
"""
    return write_text(REPORT_PATH, report)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# 2026-05-27 Stage337AS Completed-Day Attribution Decision(337AS 완성일 귀속 결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- trade_count(거래 수): `{final['trade_count']}`
- net_profit(순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- proxy_match(프록시 일치): `{final['proxy_matched_dimensions']}/{final['proxy_total_dimensions']}`
- db_source_status(D/B 원천 상태): `{final['db_source_status']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): completed-day(완성일) 구간은 성과 귀속에만 쓰고, D/B source(D/B 원천)와 current-day forward window(현재일 전진 구간)가 없으므로 성공/실패 판정은 하지 않는다. 숏 방향, 후반 포켓, 비용 버퍼, 수중 체류가 다음 no-lookahead repair(미래참조 없는 수리) 설계 입력이다.
"""
    return write_text(DECISION_DOC, text)


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
- completed_day_attribution_status(완성일 귀속 상태): `usable_without_db_for_attribution_only`
- db_source_status(D/B 원천 상태): `{final['db_source_status']}`
- db_source_sidecar_feasible(D/B 원천 보조표 가능): `false`
- fragility_status(취약 상태): `short_side_chron_late_cost_buffer_underwater_fragile`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_current_day_cutoff_and_db_source_out_of_scope`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AS(337AS 실행)는 D/B 없이 가능한 completed-day attribution(완성일 귀속)을 고정하고, forward window(전진 구간)는 여전히 판정 금지로 잠갔다.
"""
    artifacts.append(write_text(SELECTED_STATUS, selection))

    state, state_bom = read_text(WORKSPACE_STATE)
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage337 run337AS focus complete: run337AS(337AS 실행)은 `{STATUS}`로 D/B 없는 completed-day attribution(완성일 귀속)과 forward window lock(전진 구간 고정)을 물질화했다. "
        f"Effect(효과): trades(거래) `{final['trade_count']}`, net(순익) `{final['net_profit']}`, PF(수익 팩터) `{final['profit_factor']}`, "
        f"proxy match(프록시 일치) `{final['proxy_matched_dimensions']}/{final['proxy_total_dimensions']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    state = re.sub(r"- >-\n  Stage337 run337AS focus complete:.*?(?=\n- >-|\Z)", "", state, flags=re.S)
    state = re.sub(r"current_focus:\n\s*\n?", "current_focus:\n" + focus + "\n", state, count=1)
    artifacts.append(write_text(WORKSPACE_STATE, state, state_bom))

    old_current, current_bom = read_text(CURRENT_STATE)
    marker = "\n## Stage267 Candidate Pool"
    tail = old_current[old_current.find(marker) :] if marker in old_current else "\n"
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

## Stage337 run337AS(337AS 실행) - 2026-05-27

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): D/B source(D/B 원천) 없이 completed-day attribution(완성일 귀속)을 재분해했고, current-day forward window(현재일 전진 구간)는 tester cutoff(테스터 컷오프) 때문에 판정 금지로 유지했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    artifacts.append(write_text(CURRENT_STATE, current + tail, current_bom))

    brief, brief_bom = read_text(STAGE_BRIEF)
    brief = re.sub(r"- latest_run\(최신 실행\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", brief, count=1)
    summary = (
        f"- run337AS_summary(337AS 요약): `{STATUS}`. "
        f"Effect(효과): trades(거래) `{final['trade_count']}`, net(순익) `{final['net_profit']}`, PF(수익 팩터) `{final['profit_factor']}`, "
        f"proxy match(프록시 일치) `{final['proxy_matched_dimensions']}/{final['proxy_total_dimensions']}`, next_action(다음 행동) `{NEXT_RUN_ID}`.\n"
    )
    if "run337AS_summary(337AS 요약)" in brief:
        brief = re.sub(r"- run337AS_summary\(337AS 요약\): [^\n]*(?:\n|$)", summary, brief, count=1)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(write_text(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = read_text(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AS(337AS 실행) `{STATUS}`. "
        f"Effect(효과): D/B 없는 completed-day attribution(완성일 귀속)과 proxy-MT5 usability(프록시-MT5 활용성)를 잠갔고 Forward/Goal(전진/목표)은 주장하지 않음.\n"
    )
    pattern = rf"^- {re.escape(TODAY)}: Stage337 run337AS\(337AS 실행\).*$"
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
        "lane": "completed_day_non_db_attribution_forward_window_lock",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "performance_attribution_runtime_boundary",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__completed_day_non_db_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "completed_day_non_db_attribution",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "completed_day_attribution_without_db(완성일 D/B 제외 귀속)",
        "tier_scope": "Tier A u42 completed-day broker slice(Tier A u42 완성일 브로커 구간)",
        "kpi_scope": "attribution_only_no_forward_kpi",
        "scoreboard_lane": "performance_attribution_runtime_boundary",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trades={final['trade_count']};net={final['net_profit']};pf={final['profit_factor']};proxy={final['proxy_matched_dimensions']}/{final['proxy_total_dimensions']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "completed_from_parent_mt5_outputs(부모 MT5 출력에서 완료)",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__completed_day_non_db_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "performance_attribution_runtime_boundary",
        "evidence_scope": "run337AD proxy/MT5 runtime; run337AE trade attribution; run337AO as-of regimes; run337AR D/B lock",
        "kpi_scope": "completed_day_attribution_only_no_forward_decision",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;fragility_drivers={final['fragility_driver_rows']};repair_queue={final['repair_queue_rows']}",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__completed_day_non_db_attribution",
        "family": "completed_day_non_db_attribution_forward_window_lock",
        "question": "what non-D/B completed-day attribution remains usable and what forward window boundary prevents false pass/fail claims",
        "metric_scope": "completed_day_trade_shape_proxy_usability_fragility_no_forward_kpi",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
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
        try:
            artifact_path = rel(path)
        except ValueError:
            continue
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
    source_trades = [
        row
        for row in read_csv(TRADE_RECORDS)
        if row.get("attempt_name") == COMPLETED_ATTEMPT and row.get("slice_type") == "completed_day_broker_slice"
    ]
    enriched = merge_asof(source_trades)
    non_db_rows = build_non_db_attribution(enriched)
    window_rows, window_summary = build_forward_window_lock()
    proxy_rows, proxy_summary = build_proxy_matrix()
    fragility_rows, fragility_summary = build_fragility_driver(non_db_rows)
    repair_rows = build_repair_queue(fragility_rows)

    non_db_path = write_csv(
        NON_DB_ATTRIBUTION,
        [
            "attempt_name",
            "slice_type",
            "axis",
            "bucket",
            "trade_count",
            "net_profit",
            "gross_profit",
            "gross_loss",
            "profit_factor",
            "expectancy",
            "win_count",
            "loss_count",
            "win_rate",
            "average_win",
            "average_loss",
            "max_closed_drawdown",
            "recovery_factor",
            "longest_underwater_trades",
            "underwater_trade_share",
            "drawdown_start",
            "drawdown_end",
            "bucket_read",
            "db_source_status",
            "forward_window_status",
            "effect",
            "claim_boundary",
        ],
        non_db_rows,
    )
    window_path = write_csv(
        FORWARD_WINDOW_LOCK,
        [
            "attempt_name",
            "slice_type",
            "feature_last_timestamp",
            "tester_last_observed_bar_time",
            "gap_status",
            "tester_to_feature_last_gap_minutes",
            "tester_to_api_latest_gap_minutes",
            "runtime_status",
            "report_status",
            "trade_count",
            "net_profit",
            "profit_factor",
            "trades_per_day",
            "window_status",
            "usable_for_attribution",
            "usable_for_forward_pass_fail",
            "forward_use",
            "db_source_status",
            "aq_current_day_gap_rows",
            "effect",
            "claim_boundary",
        ],
        window_rows,
    )
    proxy_path = write_csv(
        PROXY_MT5_USABILITY,
        [
            "attempt_name",
            "artifact_slug",
            "proxy_cutoff_utc",
            "timestamp_aligned_feature_rows",
            "expected_signal_count",
            "expected_long_count",
            "expected_short_count",
            "matched_dimensions",
            "total_dimensions",
            "all_dimensions_matched",
            "diagnostic_usability",
            "forward_usability",
            "gap_status",
            "runtime_signal_parity_read",
            "forward_kpi_read",
            "effect",
            "claim_boundary",
        ],
        proxy_rows,
    )
    fragility_path = write_csv(
        FRAGILITY_DRIVER,
        ["driver_id", "severity", "evidence_value", "read", "repair_seed", "effect", "claim_boundary"],
        fragility_rows,
    )
    repair_path = write_csv(
        REPAIR_QUEUE,
        [
            "queue_id",
            "priority",
            "source_driver",
            "allowed_next_action",
            "forbidden_action",
            "required_evidence",
            "effect",
            "next_run",
            "claim_boundary",
        ],
        repair_rows,
    )

    overall = first_row(non_db_rows, axis="all", bucket="all")
    times = [parse_time(row.get("close_time")) for row in source_trades if parse_time(row.get("close_time"))]
    final = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "trade_count": int(number(overall.get("trade_count"))),
        "net_profit": number(overall.get("net_profit")),
        "profit_factor": number(overall.get("profit_factor")),
        "max_closed_drawdown": number(overall.get("max_closed_drawdown")),
        "recovery_factor": number(overall.get("recovery_factor")),
        "underwater_trade_share": number(overall.get("underwater_trade_share")),
        "first_trade_time": min(times).strftime("%Y-%m-%d %H:%M:%S") if times else "",
        "last_trade_time": max(times).strftime("%Y-%m-%d %H:%M:%S") if times else "",
        "db_source_status": "out_of_scope_by_claim_no_timestamp_aligned_sidecar",
        "forward_usable_rows": window_summary["forward_usable_rows"],
        "proxy_attempts": proxy_summary["proxy_attempts"],
        "proxy_matched_dimensions": proxy_summary["matched_dimensions"],
        "proxy_total_dimensions": proxy_summary["total_dimensions"],
        "fragility_driver_rows": len(fragility_rows),
        "high_fragility_driver_count": fragility_summary["high_driver_count"],
        "repair_queue_rows": len(repair_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "broker_tester_current_day_cutoff_and_db_source_out_of_scope",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = write_json(FINAL_DECISION, final)
    manifest_path = write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at_utc": now_utc(),
            "script": rel(__file__),
            "inputs": [rel(path) for path in [TRADE_RECORDS, ASOF_JOIN, PROXY_DIFF, PROXY_EXPECTED, PROXY_USABILITY, KPI_SUMMARY, GAP_COMPLETED_DAY, AQ_FINAL, AR_FINAL]],
            "outputs": [rel(path) for path in [non_db_path, window_path, proxy_path, fragility_path, repair_path, final_path]],
            "external_verification_status": "completed_from_parent_mt5_outputs(부모 MT5 출력에서 완료)",
            "mutation_scope": "read_only_attribution_no_candidate_mutation(읽기 전용 귀속, 후보 변경 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    receipt_paths = write_receipts(final)
    gate_path = write_csv(GATE_AUDIT, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"], build_gate_rows(final))
    report_path = write_report(final, fragility_rows)
    decision_doc_path = write_decision_doc(final)
    workspace_paths = update_workspace_docs(final)
    register_paths = update_registers(final)
    artifact_registry_path = update_artifact_registry(
        [
            non_db_path,
            window_path,
            proxy_path,
            fragility_path,
            repair_path,
            final_path,
            manifest_path,
            gate_path,
            report_path,
            decision_doc_path,
            *receipt_paths,
            *workspace_paths,
            *register_paths,
            Path(__file__),
        ],
        final,
    )
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "trade_count": final["trade_count"],
                "net_profit": final["net_profit"],
                "profit_factor": final["profit_factor"],
                "proxy_match": f"{final['proxy_matched_dimensions']}/{final['proxy_total_dimensions']}",
                "next_action": NEXT_RUN_ID,
                "artifact_registry": rel(artifact_registry_path),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
