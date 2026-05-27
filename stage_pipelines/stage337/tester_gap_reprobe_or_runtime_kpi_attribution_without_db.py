from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402


aw = bv.aw
bg = bv.bg
bu = bv.bu

TODAY = "2026-05-28"
STAGE_ID = bv.STAGE_ID
RUN_NUMBER = "run337BX"
RUN_ID = "run337BX_tester_gap_reprobe_or_runtime_kpi_attribution_without_db_v1"
PARENT_RUN_ID = "run337BW_review_model_scout_runtime_probe_without_db_v1"
NEXT_RUN_ID_GAP_CLOSED = "run337BY_runtime_kpi_attribution_and_no_overfit_research_matrix_without_db_v1"
NEXT_RUN_ID_GAP_REMAINS = "run337BY_completed_day_lock_or_tester_visibility_repair_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BX_tester_gap_reprobe_runtime_kpi_attribution_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_COPY_DIR = RUN_DIR / "models"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEWS_DIR = bv.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BX_tester_gap_reprobe_runtime_kpi_attribution.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337BX_tester_gap_reprobe_runtime_kpi_attribution.md"
SELECTED_STATUS = bv.SELECTED_STATUS
STAGE_BRIEF = bv.STAGE_BRIEF
WORKSPACE_STATE = bv.WORKSPACE_STATE
CURRENT_STATE = bv.CURRENT_STATE
CHANGELOG = bv.CHANGELOG
RUN_REGISTRY = bv.RUN_REGISTRY
ALPHA_LEDGER = bv.ALPHA_LEDGER
ARTIFACT_REGISTRY = bv.ARTIFACT_REGISTRY
STAGE_LEDGER = bv.STAGE_LEDGER

BW_FINAL = STAGE_DIR / "02_runs" / "run337BW" / "final_decision.json"
BW_GAP_REVIEW = STAGE_DIR / "02_runs" / "run337BW" / "tester_gap_review.csv"
BV_SUMMARY = STAGE_DIR / "02_runs" / "run337BV" / "model_scout_mt5_runtime_probe_summary.csv"
BU_SCORECARD = bu.DECISION_SCORECARD
BU_PROXY_EXPECTED = bu.PROXY_EXPECTED_FORWARD
BU_PACKAGE = bu.MT5_RUNTIME_PROBE_PACKAGE

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage337/{RUN_NUMBER}_tester_gap_reprobe_runtime_kpi"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXECUTION_SUMMARY = RUN_DIR / "tester_gap_reprobe_runtime_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "tester_gap_reprobe_proxy_mt5_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
GAP_REPROBE_REVIEW = RUN_DIR / "tester_gap_reprobe_review.csv"
KPI_ATTRIBUTION = RUN_DIR / "runtime_kpi_attribution.csv"
SIGNAL_HOUR_ATTRIBUTION = RUN_DIR / "signal_hour_attribution.csv"
TRADE_FLOW_ATTRIBUTION = RUN_DIR / "trade_flow_attribution.csv"
PROXY_USABILITY = RUN_DIR / "proxy_usability_judgment.csv"
NEXT_RESEARCH_MATRIX = RUN_DIR / "next_research_matrix.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
TESTER_SETTINGS_IDENTITY = RUN_DIR / "tester_settings_identity.json"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (BW_FINAL, BW_GAP_REVIEW, BV_SUMMARY, BU_SCORECARD, BU_PROXY_EXPECTED, BU_PACKAGE)
OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    COMMON_SYNC,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    GAP_REPROBE_REVIEW,
    KPI_ATTRIBUTION,
    SIGNAL_HOUR_ATTRIBUTION,
    TRADE_FLOW_ATTRIBUTION,
    PROXY_USABILITY,
    NEXT_RESEARCH_MATRIX,
    RUNTIME_IDENTITY,
    TESTER_SETTINGS_IDENTITY,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    FORENSICS_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

GAP_COLUMNS = (
    "model_id",
    "feature_set_id",
    "previous_last_ready_bar_time",
    "new_last_ready_bar_time",
    "latest_expected_bar_time",
    "previous_gap_minutes",
    "new_gap_minutes",
    "gap_delta_minutes",
    "feature_last_reached",
    "gap_status",
    "interpretation",
    "claim_boundary",
)
KPI_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "proxy_signal_count",
    "proxy_net_log_return_cost1",
    "proxy_profit_factor_cost1",
    "proxy_max_drawdown_log_return_cost1",
    "previous_mt5_net_profit",
    "new_mt5_net_profit",
    "mt5_net_delta",
    "previous_trade_count",
    "new_trade_count",
    "trade_count_delta",
    "new_profit_factor",
    "new_max_drawdown_amount",
    "new_short_trade_count",
    "new_long_trade_count",
    "likely_drivers",
    "attribution_confidence",
    "claim_boundary",
)
FLOW_COLUMNS = (
    "model_id",
    "feature_set_id",
    "ready_model_rows",
    "runtime_signal_count",
    "runtime_signal_rate",
    "order_attempt_count",
    "order_fill_count",
    "trade_count",
    "orders_per_signal",
    "fills_per_order",
    "trades_per_ready_row",
    "flow_interpretation",
    "claim_boundary",
)
HOUR_COLUMNS = (
    "model_id",
    "feature_set_id",
    "hour_utc",
    "cycle_rows",
    "ready_model_rows",
    "short_count",
    "long_count",
    "flat_count",
    "signal_rate",
    "claim_boundary",
)
USABILITY_COLUMNS = (
    "model_id",
    "feature_set_id",
    "proxy_mt5_mismatch_rows",
    "feature_last_reached",
    "tester_gap_minutes",
    "runtime_completed",
    "strategy_report_completed",
    "proxy_usability",
    "not_usable_for",
    "effect",
    "claim_boundary",
)
NEXT_COLUMNS = ("next_action_id", "lane", "priority", "reason", "required_evidence", "stop_condition", "effect", "claim_boundary")
GATE_COLUMNS = bv.GATE_COLUMNS


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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
    return raw.decode("utf-8-sig"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337BX tester gap reprobe and runtime KPI attribution.")
    parser.add_argument("--terminal-path", default=str(bv.DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(bv.DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(bv.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(bv.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(bv.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--attempt-filter", default="")
    return parser.parse_args()


def patch_bv_module() -> None:
    bv.RUN_NUMBER = RUN_NUMBER
    bv.RUN_ID = RUN_ID
    bv.PARENT_RUN_ID = PARENT_RUN_ID
    bv.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    bv.RUN_DIR = RUN_DIR
    bv.MT5_DIR = MT5_DIR
    bv.SET_DIR = SET_DIR
    bv.INI_DIR = INI_DIR
    bv.MODEL_COPY_DIR = MODEL_COPY_DIR
    bv.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    bv.TELEMETRY_COPY_DIR = TELEMETRY_COPY_DIR
    bv.REPORT_COPY_DIR = REPORT_COPY_DIR
    bv.COMMON_ROOT = COMMON_ROOT
    bv.COMMON_MODEL_DIR = COMMON_MODEL_DIR
    bv.COMMON_FEATURE_DIR = COMMON_FEATURE_DIR
    bv.COMMON_TELEMETRY_DIR = COMMON_TELEMETRY_DIR


def as_float(value: Any) -> float:
    try:
        number = float(value)
        return number if math.isfinite(number) else math.nan
    except Exception:
        return math.nan


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def time_gap_minutes(start: Any, end: Any) -> float:
    try:
        a = pd.Timestamp(str(start)).tz_localize("UTC") if pd.Timestamp(str(start)).tzinfo is None else pd.Timestamp(str(start)).tz_convert("UTC")
        b = pd.Timestamp(str(end)).tz_localize("UTC") if pd.Timestamp(str(end)).tzinfo is None else pd.Timestamp(str(end)).tz_convert("UTC")
        return (b - a).total_seconds() / 60.0
    except Exception:
        return math.nan


def load_parent() -> tuple[dict[str, Any], list[dict[str, str]], pd.DataFrame, list[dict[str, str]], list[dict[str, str]], pd.DataFrame]:
    parent = read_json(BW_FINAL)
    if parent.get("next_action") != RUN_ID:
        raise RuntimeError(f"parent next_action mismatch: {parent.get('next_action')} != {RUN_ID}")
    package_rows = read_csv(BU_PACKAGE)
    proxy = pd.read_csv(io_path(BU_PROXY_EXPECTED))
    bw_gap = read_csv(BW_GAP_REVIEW)
    bv_summary = read_csv(BV_SUMMARY)
    scorecard = pd.read_csv(io_path(BU_SCORECARD))
    return parent, package_rows, proxy, bw_gap, bv_summary, scorecard


def build_gap_review(summary: Sequence[Mapping[str, Any]], prior_gap: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    previous = {str(row.get("model_id", "")): row for row in prior_gap}
    rows: list[dict[str, Any]] = []
    for row in summary:
        model_id = str(row.get("model_id", ""))
        prior = previous.get(model_id, {})
        new_gap = time_gap_minutes(row.get("last_ready_bar_time"), row.get("latest_expected_bar_time"))
        previous_gap = as_float(prior.get("tester_to_feature_last_gap_minutes"))
        reached = str(row.get("feature_last_reached", "")).lower() == "true"
        status = "tester_reached_feature_last" if reached else "tester_feature_last_gap_remains"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "previous_last_ready_bar_time": prior.get("last_ready_bar_time", ""),
                "new_last_ready_bar_time": row.get("last_ready_bar_time", ""),
                "latest_expected_bar_time": row.get("latest_expected_bar_time", ""),
                "previous_gap_minutes": previous_gap,
                "new_gap_minutes": new_gap,
                "gap_delta_minutes": new_gap - previous_gap if math.isfinite(new_gap) and math.isfinite(previous_gap) else "",
                "feature_last_reached": reached,
                "gap_status": status,
                "interpretation": "tester visibility repaired(테스터 가시성 수리됨)" if reached else "tester visibility still limits latest pocket(테스터 가시성이 최신 구간을 아직 제한)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def primary_proxy_scorecard(scorecard: pd.DataFrame) -> dict[str, Mapping[str, Any]]:
    frame = scorecard[
        (scorecard["split"].astype(str) == "forward_after_2026_04_14_diagnostic")
        & (scorecard["threshold_id"].astype(str) == "fixed_short040_long040_margin002")
        & (scorecard["cost_bps_per_trade"].astype(float) == 1.0)
    ].copy()
    return {str(row["model_id"]): row.to_dict() for _, row in frame.iterrows()}


def build_kpi_attribution(summary: Sequence[Mapping[str, Any]], bv_summary: Sequence[Mapping[str, str]], scorecard: pd.DataFrame) -> list[dict[str, Any]]:
    previous = {str(row.get("model_id", "")): row for row in bv_summary}
    proxy_by_model = primary_proxy_scorecard(scorecard)
    rows: list[dict[str, Any]] = []
    for row in summary:
        model_id = str(row.get("model_id", ""))
        prev = previous.get(model_id, {})
        proxy = proxy_by_model.get(model_id, {})
        prev_net = as_float(prev.get("net_profit"))
        new_net = as_float(row.get("net_profit"))
        prev_trades = as_int(prev.get("trade_count"))
        new_trades = as_int(row.get("trade_count"))
        likely = [
            "proxy log-return vs MT5 account-currency unit mismatch(단위 차이)",
            "execution lifecycle: one position, reverse, max-hold(실행 생애주기)",
            "broker real-tick spread/slippage and order timing(브로커 실제 틱 비용/시점)",
        ]
        if str(row.get("feature_last_reached", "")).lower() != "true":
            likely.append("tester latest-pocket visibility gap(테스터 최신 구간 가시성 공백)")
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "model_family": proxy.get("model_family", ""),
                "proxy_signal_count": proxy.get("signal_count", ""),
                "proxy_net_log_return_cost1": proxy.get("net_log_return_sum", ""),
                "proxy_profit_factor_cost1": proxy.get("profit_factor", ""),
                "proxy_max_drawdown_log_return_cost1": proxy.get("max_drawdown_log_return", ""),
                "previous_mt5_net_profit": prev_net,
                "new_mt5_net_profit": new_net,
                "mt5_net_delta": new_net - prev_net if math.isfinite(new_net) and math.isfinite(prev_net) else "",
                "previous_trade_count": prev_trades,
                "new_trade_count": new_trades,
                "trade_count_delta": new_trades - prev_trades,
                "new_profit_factor": row.get("profit_factor", ""),
                "new_max_drawdown_amount": row.get("max_drawdown_amount", ""),
                "new_short_trade_count": row.get("short_trade_count", ""),
                "new_long_trade_count": row.get("long_trade_count", ""),
                "likely_drivers": "; ".join(likely),
                "attribution_confidence": "medium" if str(row.get("runtime_status")) == "completed" else "low",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_trade_flow(summary: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary:
        ready = as_int(row.get("ready_model_rows"))
        signal = as_int(row.get("long_count")) + as_int(row.get("short_count"))
        orders = as_int(row.get("order_attempt_count"))
        fills = as_int(row.get("order_fill_count"))
        trades = as_int(row.get("trade_count"))
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "ready_model_rows": ready,
                "runtime_signal_count": signal,
                "runtime_signal_rate": signal / ready if ready else "",
                "order_attempt_count": orders,
                "order_fill_count": fills,
                "trade_count": trades,
                "orders_per_signal": orders / signal if signal else "",
                "fills_per_order": fills / orders if orders else "",
                "trades_per_ready_row": trades / ready if ready else "",
                "flow_interpretation": "signal-to-trade compression is expected from max-hold, one-position, reverse/close rules(최대보유/단일포지션/반전-청산 때문에 신호가 거래로 압축됨)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def read_telemetry_for_attempt(attempt_name: str) -> pd.DataFrame:
    path = TELEMETRY_COPY_DIR / f"{attempt_name}_telemetry.csv"
    if not path_exists(path):
        return pd.DataFrame()
    return pd.read_csv(io_path(path)).fillna("")


def build_signal_hour_attribution(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        frame = read_telemetry_for_attempt(str(attempt["attempt_name"]))
        if frame.empty or "record_type" not in frame.columns:
            continue
        cycles = frame[frame["record_type"].astype(str).str.lower() == "cycle"].copy()
        if cycles.empty:
            continue
        cycles["hour_utc"] = pd.to_datetime(cycles["source_time"], errors="coerce").dt.hour
        for hour, part in cycles.groupby("hour_utc", dropna=True):
            ready = part[(part["feature_ready"].astype(str).str.lower() == "true") & (part["model_ok"].astype(str).str.lower() == "true")]
            decisions = ready["decision"].astype(str).str.lower()
            short_count = int((decisions == "short").sum())
            long_count = int((decisions == "long").sum())
            flat_count = int((decisions == "flat").sum())
            signal = short_count + long_count
            rows.append(
                {
                    "model_id": attempt.get("model_id", ""),
                    "feature_set_id": attempt.get("feature_set_id", ""),
                    "hour_utc": int(hour),
                    "cycle_rows": int(len(part)),
                    "ready_model_rows": int(len(ready)),
                    "short_count": short_count,
                    "long_count": long_count,
                    "flat_count": flat_count,
                    "signal_rate": signal / len(ready) if len(ready) else "",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_proxy_usability(summary: Sequence[Mapping[str, Any]], mismatch_rows: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary:
        reached = str(row.get("feature_last_reached", "")).lower() == "true"
        runtime_ok = str(row.get("runtime_status")) == "completed"
        report_ok = str(row.get("report_status")) == "completed"
        gap = time_gap_minutes(row.get("last_ready_bar_time"), row.get("latest_expected_bar_time"))
        if mismatch_rows == 0 and reached and runtime_ok:
            usability = "usable_for_runtime_inference_parity_and_completed_window_probe(런타임 추론 동등성/완성 구간 탐침에 사용 가능)"
            not_usable = "not usable alone for operating promotion or final forward pass/fail(단독 운영 승격/최종 전진 판정 불가)"
        elif mismatch_rows == 0 and runtime_ok:
            usability = "usable_for_overlap_runtime_parity_only(겹친 구간 런타임 동등성에만 사용 가능)"
            not_usable = "not usable for latest forward pocket or operating claim(최신 전진 구간/운영 주장 불가)"
        else:
            usability = "not usable_until_runtime_mismatch_repaired(런타임 불일치 수리 전 사용 불가)"
            not_usable = "all forward and runtime claims(모든 전진/런타임 주장)"
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "proxy_mt5_mismatch_rows": mismatch_rows,
                "feature_last_reached": reached,
                "tester_gap_minutes": gap,
                "runtime_completed": runtime_ok,
                "strategy_report_completed": report_ok,
                "proxy_usability": usability,
                "not_usable_for": not_usable,
                "effect": "proxy(프록시)를 어디까지 믿을 수 있는지 명시해 과대 주장 방지",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_matrix(gap_closed: bool, kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best_net = max((as_float(row.get("new_mt5_net_profit")) for row in kpi_rows), default=math.nan)
    weak_models = [row.get("model_id", "") for row in kpi_rows if as_float(row.get("new_mt5_net_profit")) < 0]
    if gap_closed:
        primary_next = NEXT_RUN_ID_GAP_CLOSED
        primary_reason = "tester feature_last reached; runtime KPI drift is now the main bottleneck"
        required = "lifecycle, hour/session, direction, cost, drawdown pocket attribution without tuning"
        stop = "identify non-overfit repair/offense/defense experiment matrix"
    else:
        primary_next = NEXT_RUN_ID_GAP_REMAINS
        primary_reason = "tester feature_last gap remains after reprobe"
        required = "completed-day lock or tester visibility repair with exact feature_last proof"
        stop = "tester reaches feature_last or completed-day boundary is locked"
    return [
        {
            "next_action_id": primary_next,
            "lane": "repair",
            "priority": "P0",
            "reason": primary_reason,
            "required_evidence": required,
            "stop_condition": stop,
            "effect": "다음 병목을 수리/귀속 대상으로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_action_id": "defensive_runtime_lifecycle_repair_matrix",
            "lane": "defense",
            "priority": "P0",
            "reason": f"negative MT5 net models={len(weak_models)}; best_net={best_net}",
            "required_evidence": "drawdown, hold, signal compression, session/hour, direction balance",
            "stop_condition": "repair idea must improve robustness without using forward retuning",
            "effect": "손실/드로우다운을 낮추는 방어형 실험 후보를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_action_id": "offensive_signal_quality_frontier_matrix",
            "lane": "offense",
            "priority": "P1",
            "reason": "some proxy signals survive parity but MT5 profit shape is weak",
            "required_evidence": "no-lookahead feature family, calibration, trade frequency, cross-split proof",
            "stop_condition": "new ONNX candidates must pass parity and no-overfit gates before selection",
            "effect": "폭발력 있는 ONNX 후보를 탐색하되 과적합 루프를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(
    parent: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    def gate(gate_id: str, ok: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    mismatch_rows = sum(1 for row in diff_rows if row.get("comparison_status") != "matched")
    runtime_completed = sum(1 for row in summary_rows if str(row.get("runtime_status")) == "completed")
    feature_reached = sum(1 for row in gap_rows if str(row.get("gap_status")) == "tester_reached_feature_last")
    return [
        gate("bx_gate_parent_bw_loaded", parent.get("next_action") == RUN_ID, str(parent.get("next_action")), RUN_ID, "BW가 BX를 열었는지 확인한다."),
        gate("bx_gate_attempts_materialized", len(attempts) == 6, f"attempts={len(attempts)}", "6 attempts", "6개 모델을 같은 조건으로 재탐침한다."),
        gate("bx_gate_runtime_completed", runtime_completed == len(summary_rows) and runtime_completed > 0, f"completed={runtime_completed}/{len(summary_rows)}", "all runtime completed", "MT5 runtime telemetry(런타임 기록)를 다시 확보한다."),
        gate("bx_gate_proxy_mt5_mismatch_zero", mismatch_rows == 0 and bool(diff_rows), f"mismatch_rows={mismatch_rows};diff_rows={len(diff_rows)}", "zero mismatches", "프록시와 MT5 추론/결정 값이 같은지 확인한다."),
        gate("bx_gate_gap_reprobe_recorded", len(gap_rows) == len(summary_rows) and len(gap_rows) > 0, f"feature_reached={feature_reached}/{len(gap_rows)}", "gap review rows recorded", "tester gap(테스터 공백) 수리 여부를 기록한다."),
        gate("bx_gate_no_forward_or_goal_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim", "Forward/Goal(전진/목표)을 주장하지 않는다."),
    ]


def classify(gates: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337BX_gap_reprobe_or_runtime_kpi_attribution_gate_failure",
            "gap_reprobe_runtime_kpi_attribution_gate_failure_requires_repair",
            "stage337BX_open_reprobe_repair",
            NEXT_RUN_ID_GAP_REMAINS,
        )
    gap_closed = all(str(row.get("gap_status")) == "tester_reached_feature_last" for row in gap_rows)
    if gap_closed:
        return (
            "completed_stage337BX_tester_gap_reprobe_feature_last_reached_runtime_kpi_attribution_ready_no_forward_decision",
            "tester_gap_repaired_proxy_mt5_parity_holds_runtime_kpi_drift_requires_research_matrix",
            "stage337BX_open_run337BY_runtime_kpi_attribution_and_no_overfit_research_matrix",
            NEXT_RUN_ID_GAP_CLOSED,
        )
    return (
        "completed_stage337BX_tester_gap_reprobe_gap_remains_runtime_kpi_attribution_partial_no_forward_decision",
        "tester_gap_remains_after_reprobe_proxy_mt5_overlap_parity_still_holds",
        "stage337BX_open_run337BY_completed_day_lock_or_visibility_repair",
        NEXT_RUN_ID_GAP_REMAINS,
    )


def write_report(
    final: Mapping[str, Any],
    gap_rows: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
) -> Path:
    lines = [
        "# Stage337 run337BX Tester Gap Reprobe and Runtime KPI Attribution(테스터 공백 재탐침 및 런타임 성과 귀속)",
        "",
        "## Conclusion(결론)",
        "",
        "run337BX(337BX 실행)는 run337BV/BW(337BV/BW 실행)의 tester gap(테스터 공백)을 같은 ONNX/feature/threshold/lot(온엑스/피처/임계값/로트) 조건으로 다시 탐침하고, MT5 KPI drift(성과 지표 차이)를 귀속했다.",
        "",
        f"Effect(효과): status(상태)는 `{final['status']}`이다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.",
        "",
        "## Result(결과)",
        "",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`",
        f"- proxy_mt5_mismatch_rows(프록시-MT5 불일치 행): `{final['mismatch_rows']}`",
        f"- feature_last_reached_rows(피처 끝 도달 행): `{final['feature_last_reached_rows']}`",
        "",
        "## Gap Reprobe(공백 재탐침)",
        "",
        "| model(모델) | previous gap(이전 공백) | new gap(새 공백) | reached(도달) |",
        "|---|---:|---:|---|",
    ]
    for row in gap_rows:
        lines.append(f"| `{row['model_id']}` | {row['previous_gap_minutes']} | {row['new_gap_minutes']} | `{row['feature_last_reached']}` |")
    lines.extend(["", "## KPI Attribution(KPI 귀속)", "", "| model(모델) | proxy net log(프록시 로그 순익) | new MT5 net(새 MT5 순익) | PF(수익 팩터) | trades(거래) |", "|---|---:|---:|---:|---:|"])
    for row in kpi_rows:
        lines.append(f"| `{row['model_id']}` | {row['proxy_net_log_return_cost1']} | {row['new_mt5_net_profit']} | {row['new_profit_factor']} | {row['new_trade_count']} |")
    lines.extend(["", "## Proxy Usability(프록시 사용성)", "", "| model(모델) | usability(사용성) | not usable for(불가 범위) |", "|---|---|---|"])
    for row in usability_rows:
        lines.append(f"| `{row['model_id']}` | `{row['proxy_usability']}` | `{row['not_usable_for']}` |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- model_training(모델 학습): `not_run`",
            "- threshold_tuning(임계값 조정): `not_run`",
            "- lot_optimization(로트 최적화): `not_run`",
            "- candidate_selection(후보 선택): `not_run`",
            "- Forward Passed/Failed(전진 통과/실패): `not_claimed`",
            "- runtime_authority(런타임 권위): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337BX Tester Gap Reprobe and Runtime KPI Attribution(결정: 테스터 공백 재탐침 및 런타임 성과 귀속)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): tester gap(테스터 공백) 재탐침과 runtime KPI attribution(런타임 성과 귀속)을 수행했지만, 이 결과는 연구/수리 입력이다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (EXPERIMENT_RECEIPT, {"run_id": RUN_ID, "hypothesis": "tester rollover may expose feature_last without changing model or thresholds.", "controls": "same BU ONNX, features, thresholds, lot, EA", "claim_boundary": CLAIM_BOUNDARY}),
        (DATA_RECEIPT, {"data_scope": "BU feature CSV/proxy expected and BX MT5 telemetry", "integrity_judgment": "usable_with_boundary", "claim_boundary": CLAIM_BOUNDARY}),
        (MODEL_RECEIPT, {"model_subject": "BU scout ONNX unchanged", "training": "not_run", "threshold_policy": "unchanged fixed_short040_long040_margin002", "claim_boundary": CLAIM_BOUNDARY}),
        (RUNTIME_RECEIPT, {"parity_check": rel(PROXY_MT5_DIFF), "runtime_claim_boundary": "runtime_probe_only_no_authority", "claim_boundary": CLAIM_BOUNDARY}),
        (PERFORMANCE_RECEIPT, {"observed_change": "MT5 KPI differs from proxy log-return diagnostics", "comparison_baseline": rel(BV_SUMMARY), "likely_drivers": "unit mismatch, execution lifecycle, broker costs, tester visibility", "attribution_confidence": "medium", "next_probe": final["next_action"], "claim_boundary": CLAIM_BOUNDARY}),
        (FORENSICS_RECEIPT, {"tester_identity": "portable MT5 Strategy Tester; US100; M5; model 4; deposit 500; leverage 1:100", "backtest_judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY}),
        (ARTIFACT_RECEIPT, {"source_inputs": [rel(path) for path in INPUT_FILES], "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)], "claim_boundary": CLAIM_BOUNDARY}),
        (JUDGMENT_RECEIPT, {"result_subject": RUN_ID, "judgment_label": final["judgment"], "next_condition": final["next_action"], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", final["next_action"])
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337BX focus complete: tester gap reprobe/runtime KPI attribution(테스터 공백 재탐침/런타임 성과 귀속)을 `{final['status']}`로 닫았다. "
        "Effect(효과): proxy-MT5 parity(프록시-MT5 동등성) 사용 범위와 다음 방어/공격/수리 연구 대기열을 분리한다.\n"
    )
    if "Stage337 run337BX focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current = current_text
    replacements = {
        "- current_run(현재 실행): ": f"`{final['next_action']}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{final['next_action']}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BX(337BX 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 같은 ONNX/피처/임계값/로트로 tester gap(테스터 공백)을 재탐침하고 runtime KPI drift(런타임 성과 차이)를 귀속했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BX(337BX 실행)" not in current:
        marker = "## Stage337 run337BW(337BW"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `attempted_strategy_tester_reprobe`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): 다음은 runtime KPI attribution(런타임 성과 귀속)을 기반으로 한 방어/공격/수리 연구 행렬이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BX(337BX 실행) reprobed tester gap(테스터 공백) and attributed runtime KPI drift(런타임 성과 차이). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BX reprobed tester gap(테스터 공백) and opened `{final['next_action']}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "tester_gap_reprobe_runtime_kpi_attribution_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};mismatch_rows={final['mismatch_rows']};feature_last_reached={final['feature_last_reached_rows']};goal_achieve_not_claimed.",
        "family": "runtime_parity_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__tester_gap_reprobe_runtime_kpi_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "tester_gap_reprobe_runtime_kpi_attribution",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_reprobe_and_kpi_attribution",
        "tier_scope": "Tier A runtime probe; no operating claim",
        "kpi_scope": "runtime_parity_kpi_attribution_no_forward_decision",
        "scoreboard_lane": "runtime_reprobe_attribution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"mismatch_rows={final['mismatch_rows']}",
        "guardrail_kpi": "no training; no threshold tuning; no goal claim",
        "external_verification_status": "attempted_strategy_tester_reprobe",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__tester_gap_reprobe_runtime_kpi_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_performance_attribution",
        "evidence_scope": "MT5 telemetry, strategy tester report, proxy-vs-MT5 diff, KPI attribution",
        "kpi_scope": "runtime_reprobe_and_attribution",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"feature_last_reached={final['feature_last_reached_rows']};mismatch_rows={final['mismatch_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__tester_gap_reprobe_runtime_kpi_attribution",
        "family": "runtime_parity_performance_attribution",
        "question": "does tester rollover repair the latest-pocket gap and what explains MT5 KPI drift",
        "metric_scope": "runtime_parity_gap_kpi_attribution",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    artifact_columns = artifact_columns or ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    generated = now_utc()
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    args = parse_args()
    patch_bv_module()
    for directory in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_COPY_DIR, FEATURE_COPY_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    parent, package_rows, proxy, prior_gap, bv_summary, scorecard = load_parent()
    pre_process = bv.terminal_processes()
    compile_result, ea_sync = bv.compile_and_sync_ea(Path(args.metaeditor_path), Path(args.terminal_data_root))
    attempts, sync_rows, attempt_artifacts = bv.materialize_attempts(package_rows, args)
    sync_rows = list(ea_sync) + sync_rows
    execution = bv.execute_attempts(attempts, args, compile_result)
    copied_runtime = bv.copy_runtime_outputs(Path(args.common_files_root), attempts)
    summary_rows, diff_rows, skip_rows = bv.compare_all(attempts, execution, proxy)
    gap_rows = build_gap_review(summary_rows, prior_gap)
    kpi_rows = build_kpi_attribution(summary_rows, bv_summary, scorecard)
    flow_rows = build_trade_flow(summary_rows)
    hour_rows = build_signal_hour_attribution(attempts)
    mismatch_rows = sum(1 for row in diff_rows if row.get("comparison_status") != "matched")
    usability_rows = build_proxy_usability(summary_rows, mismatch_rows)
    gap_closed = all(str(row.get("gap_status")) == "tester_reached_feature_last" for row in gap_rows)
    next_rows = build_next_matrix(gap_closed, kpi_rows)
    gates = build_gates(parent, attempts, summary_rows, diff_rows, gap_rows)
    status, judgment, decision, next_action = classify(gates, gap_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "attempt_rows": len(attempts),
        "summary_rows": len(summary_rows),
        "diff_rows": len(diff_rows),
        "mismatch_rows": mismatch_rows,
        "runtime_completed_rows": sum(1 for row in summary_rows if str(row.get("runtime_status")) == "completed"),
        "feature_last_reached_rows": sum(1 for row in gap_rows if str(row.get("gap_status")) == "tester_reached_feature_last"),
        "kpi_attribution_rows": len(kpi_rows),
        "signal_hour_rows": len(hour_rows),
        "actual_mt5_execution": "attempted_strategy_tester_reprobe" if not args.materialize_only else "not_run_materialize_only",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }
    attempt_rows = [{column: attempt.get(column, "") for column in bv.ATTEMPT_COLUMNS} for attempt in attempts]
    artifacts: list[Path] = [
        write_csv(ATTEMPT_PACKAGE, bv.ATTEMPT_COLUMNS, attempt_rows),
        write_csv(COMMON_SYNC, bv.SYNC_COLUMNS, sync_rows),
        write_csv(EXECUTION_SUMMARY, bv.SUMMARY_COLUMNS, summary_rows),
        write_csv(PROXY_MT5_DIFF, bv.DIFF_COLUMNS, diff_rows),
        write_csv(TELEMETRY_SKIP_SUMMARY, ["attempt_name", "model_id", "skip_reason", "rows", "effect", "claim_boundary"], skip_rows),
        write_csv(GAP_REPROBE_REVIEW, GAP_COLUMNS, gap_rows),
        write_csv(KPI_ATTRIBUTION, KPI_COLUMNS, kpi_rows),
        write_csv(SIGNAL_HOUR_ATTRIBUTION, HOUR_COLUMNS, hour_rows),
        write_csv(TRADE_FLOW_ATTRIBUTION, FLOW_COLUMNS, flow_rows),
        write_csv(PROXY_USABILITY, USABILITY_COLUMNS, usability_rows),
        write_csv(NEXT_RESEARCH_MATRIX, NEXT_COLUMNS, next_rows),
        write_csv(RUNTIME_IDENTITY, bv.IDENTITY_COLUMNS, bv.build_identity_rows(attempts, sync_rows)),
        write_json(TESTER_SETTINGS_IDENTITY, {
            "terminal_path": str(args.terminal_path),
            "terminal_data_root": str(args.terminal_data_root),
            "common_files_root": str(args.common_files_root),
            "tester_profile_root": str(args.tester_profile_root),
            "from_date": "2026.04.14",
            "to_date": attempts[0].get("to_date", "") if attempts else "",
            "claim_boundary": CLAIM_BOUNDARY,
        }),
        write_json(TERMINAL_PROCESS_AUDIT, {"pre_run": pre_process, "post_run": bv.terminal_processes(), "claim_boundary": CLAIM_BOUNDARY}),
        write_json(MT5_EXECUTION_RESULT, execution),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(attempt_artifacts)
    artifacts.extend(copied_runtime)
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final, gap_rows, kpi_rows, usability_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
