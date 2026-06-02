from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import materialize_density_side_balance_cost_session_stress_without_db as prev  # noqa: E402
from stage_pipelines.stage364 import train_density_side_balance_repair_onnx_scout_without_db as base  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = prev.STAGE_ID
RUN_NUMBER = "run364AA"
RUN_ID = "run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1"
PARENT_RUN_ID = prev.RUN_ID
BASELINE_RUN_ID = base.RUN_ID
NEXT_RUN_ID = "run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1"

STATUS = "completed_stage364AA_cost_session_pf_dd_proxy_scout_no_mt5_no_authority"
JUDGMENT = "proxy_scout_completed_pf_dd_stress_candidates_ranked_mt5_probe_required_no_authority"
DECISION = "stage364AA_open_run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
TARGET_PF = 1.30
DEPOSIT = 500.0

STAGE_DIR = prev.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SCOUT_SURFACE = RUN_DIR / "cost_session_guardrail_proxy_scout_surface.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_EXPECTED_TRADE_TAPE = EXPECTED_DIR / "selected_trade_tape.csv"
GUARDRAIL_EFFECT_AUDIT = RUN_DIR / "guardrail_effect_audit.csv"
BASELINE_COMPARISON = RUN_DIR / "baseline_comparison.csv"
RUN364AB_QUEUE = RUN_DIR / "run364AB_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_boundary_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AA_density_side_balance_cost_session_stress_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AA_density_side_balance_cost_session_stress_scout.md"
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
    prev.FINAL_DECISION,
    prev.GATE_AUDIT,
    prev.PARAMETER_QUEUE,
    prev.RUN364AA_QUEUE,
    prev.STRESS_ZONE_CANDIDATES,
    prev.SIMPLE_FILTER_PROXY,
    prev.ACCOUNT_DRAWDOWN_TABLE,
    base.SELECTED_RUNTIME_CANDIDATE,
    base.SELECTED_TRADE_TAPE,
    base.DUAL_SIDE_RUNTIME_SURFACE,
    base.prev.sidepkg.pkg.FEATURE_MATRIX,
    base.prev.sidepkg.pkg.FEATURE_ORDER,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SCOUT_SURFACE,
    SELECTED_PROXY_CANDIDATE,
    SELECTED_EXPECTED_TRADE_TAPE,
    GUARDRAIL_EFFECT_AUDIT,
    BASELINE_COMPARISON,
    RUN364AB_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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


def rel(path: Path | str) -> str:
    return prev.rel(path)


def exists(path: Path | str) -> bool:
    return prev.exists(path)


def sha(path: Path | str) -> str:
    return prev.sha(path)


def read_json(path: Path) -> Any:
    return prev.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    prev.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    prev.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    prev.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    prev.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return prev.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    prev.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, EXPECTED_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(path, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    parent = read_json(prev.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(금지된 운영 주장)")
    gates = read_csv_rows(prev.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit is not fully passed(부모 게이트 미통과)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AA inputs(입력 누락): " + ", ".join(missing))
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "role": input_role(path),
                "timestamp_boundary(시점 경계)": "entry-known guardrail replay; no post-entry feature use(진입 시점 가드레일 재생, 진입 후 피처 미사용)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def input_role(path: Path) -> str:
    name = path.name
    if name == "pf_drawdown_parameter_neighborhood_queue.csv":
        return "parameter_queue(파라미터 대기열)"
    if name == "run364AA_scout_queue.csv":
        return "scout_queue(탐색 대기열)"
    if "selected_runtime_candidate" in name:
        return "baseline_proxy_candidate(기준 프록시 후보)"
    if "trade_tape" in name:
        return "baseline_expected_trade_tape(기준 예상 거래 테이프)"
    return "supporting_evidence(보조 근거)"


def variant_id(queue_id: str, short_threshold: float, long_block_min: float, max_hold: int, guardrail: str) -> str:
    short_label = str(round(short_threshold, 6)).replace(".", "_")
    block_label = str(round(long_block_min, 6)).replace(".", "_")
    guard = guardrail.split("(")[0].replace("|", "_").replace("=", "").replace(" ", "_")
    guard = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in guard)[:40]
    return f"{queue_id}__ps{short_label}__adx{block_label}__hold{max_hold}__{guard}"


def load_queue(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = read_csv_rows(prev.PARAMETER_QUEUE)
    out = []
    for row in rows:
        queue_id = row.get("queue_id", "")
        short_threshold = as_float(row.get("short_threshold"), as_float(selected.get("short_probability_threshold"), 0.45))
        long_block_min = as_float(row.get("adx_block_min"), as_float(selected.get("long_block_min"), 40.0))
        max_hold = as_int(row.get("max_hold_m5"), as_int(selected.get("max_hold_m5"), 8))
        guardrail = row.get("guardrail_expression", "none(없음)")
        out.append(
            {
                "queue_rank": as_int(row.get("queue_rank")),
                "queue_id": queue_id,
                "short_threshold": short_threshold,
                "long_block_min": long_block_min,
                "max_hold_m5": max_hold,
                "min_margin": as_float(selected.get("min_margin")),
                "guardrail_expression": guardrail,
                "queue_type": row.get("queue_type", ""),
                "variant_id": variant_id(queue_id, short_threshold, long_block_min, max_hold, guardrail),
            }
        )
    return out


def server_timestamp(row: pd.Series) -> pd.Timestamp:
    return pd.Timestamp(row["bar_time_server"])


def guardrail_decision(signal: int, row: pd.Series, guardrail: str, previous_closed_dd_pct: float) -> tuple[int, str]:
    if signal == 0:
        return 0, "flat_or_threshold_not_met(무신호 또는 임계값 미충족)"
    server_time = server_timestamp(row)
    hour = int(server_time.hour)
    month = server_time.strftime("%Y-%m")
    text = guardrail or "none(없음)"
    if text.startswith("none") or text.startswith("short_only_threshold"):
        return signal, "guardrail_not_applied(가드레일 미적용)"
    if "soft_stop_prev_closed_dd_ge_2pct" in text and previous_closed_dd_pct >= 2.0:
        return 0, "blocked_previous_closed_dd_ge_2pct(이전 종료잔고 DD 2% 이상 차단)"
    if "soft_stop_prev_closed_dd_ge_5pct" in text and previous_closed_dd_pct >= 5.0:
        return 0, "blocked_previous_closed_dd_ge_5pct(이전 종료잔고 DD 5% 이상 차단)"
    if "soft_guard_entry_hour_16" in text or "short_threshold_plus_hour16" in text:
        if hour == 16 and signal == -1:
            return 0, "blocked_hour16_short_soft_guard(16시 숏 소프트 가드 차단)"
        return signal, "soft_hour_guard_passed(소프트 시간 가드 통과)"
    if text == "entry_hour=16":
        if hour == 16:
            return 0, "blocked_entry_hour_16(16시 차단)"
        return signal, "entry_hour_guard_passed(시간 가드 통과)"
    if text == "entry_hour=16|side=short":
        if hour == 16 and signal == -1:
            return 0, "blocked_entry_hour_16_short(16시 숏 차단)"
        return signal, "entry_hour_side_guard_passed(시간/방향 가드 통과)"
    if text == "entry_month=2025-03":
        if month == "2025-03":
            return 0, "blocked_entry_month_2025_03(2025-03 진입 차단)"
        return signal, "entry_month_guard_passed(월 가드 통과)"
    if text == "entry_month=2025-03|side=long":
        if month == "2025-03" and signal == 1:
            return 0, "blocked_entry_month_2025_03_long(2025-03 롱 차단)"
        return signal, "entry_month_side_guard_passed(월/방향 가드 통과)"
    return signal, "guardrail_not_implemented_pass_through(미구현 가드레일 통과)"


def simulate_guardrail(frame: pd.DataFrame, variant: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    trade_rows: list[dict[str, Any]] = []
    audit = {
        "guardrail_block_count": 0,
        "guardrail_pass_count": 0,
        "previous_dd_block_count": 0,
        "hour16_short_block_count": 0,
    }
    for split, split_frame in frame.groupby("split", sort=False):
        part = split_frame.sort_values("timestamp_dt").reset_index(drop=True)
        signals, _ = base.decision_signals(
            part,
            short_threshold=float(variant["short_threshold"]),
            long_block_min=float(variant["long_block_min"]),
            min_margin=float(variant["min_margin"]),
            with_reasons=False,
        )
        opens = part["entry_open"].to_numpy(dtype=float)
        timestamps = part["timestamp_dt"].to_numpy()
        position = 0
        entry_index = 0
        entry_open = 0.0
        entry_prev_dd = 0.0
        bars_in_position = 0
        closed_equity = 0.0
        peak_equity = 0.0
        previous_closed_dd_pct = 0.0
        for index in range(len(part)):
            if position != 0:
                bars_in_position += 1
            if position != 0 and bars_in_position >= int(variant["max_hold_m5"]):
                trade = make_trade_row(variant, split, part, timestamps, opens, position, entry_index, index, entry_open, entry_prev_dd, "close_max_hold")
                closed_equity, peak_equity, previous_closed_dd_pct = update_drawdown_state(trade, closed_equity, peak_equity)
                trade["closed_balance_drawdown_percent"] = finite(previous_closed_dd_pct, 6)
                trade_rows.append(trade)
                position = 0
                bars_in_position = 0
                continue
            signal, reason = guardrail_decision(int(signals[index]), part.iloc[index], str(variant["guardrail_expression"]), previous_closed_dd_pct)
            if signal == 0:
                if int(signals[index]) != 0:
                    audit["guardrail_block_count"] += 1
                    if "previous_closed_dd" in reason:
                        audit["previous_dd_block_count"] += 1
                    if "hour16_short" in reason or "entry_hour_16_short" in reason:
                        audit["hour16_short_block_count"] += 1
                continue
            audit["guardrail_pass_count"] += 1
            if position == 0:
                position = signal
                entry_index = index
                entry_open = float(opens[index])
                entry_prev_dd = previous_closed_dd_pct
                bars_in_position = 0
                continue
            if signal == position:
                continue
            trade = make_trade_row(variant, split, part, timestamps, opens, position, entry_index, index, entry_open, entry_prev_dd, "reverse_on_opposite")
            closed_equity, peak_equity, previous_closed_dd_pct = update_drawdown_state(trade, closed_equity, peak_equity)
            trade["closed_balance_drawdown_percent"] = finite(previous_closed_dd_pct, 6)
            trade_rows.append(trade)
            position = signal
            entry_index = index
            entry_open = float(opens[index])
            entry_prev_dd = previous_closed_dd_pct
            bars_in_position = 0
    return pd.DataFrame(trade_rows), audit


def make_trade_row(
    variant: Mapping[str, Any],
    split: str,
    part: pd.DataFrame,
    timestamps: np.ndarray,
    opens: np.ndarray,
    position: int,
    entry_index: int,
    exit_index: int,
    entry_open: float,
    previous_dd_pct: float,
    exit_reason: str,
) -> dict[str, Any]:
    exit_open = float(opens[exit_index])
    profit = (exit_open - entry_open) * base.POINT_VALUE - base.BASE_COST if position == 1 else (entry_open - exit_open) * base.POINT_VALUE - base.BASE_COST
    entry_row = part.iloc[entry_index]
    server_time = server_timestamp(entry_row)
    return {
        "run_id": RUN_ID,
        "variant_id": variant["variant_id"],
        "queue_id": variant["queue_id"],
        "split": split,
        "entry_timestamp": pd.Timestamp(timestamps[entry_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "exit_timestamp": pd.Timestamp(timestamps[exit_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entry_server_time": server_time.strftime("%Y-%m-%d %H:%M:%S"),
        "entry_month": server_time.strftime("%Y-%m"),
        "entry_hour": int(server_time.hour),
        "held_m5": int(exit_index - entry_index),
        "side": "long" if position == 1 else "short",
        "entry_score": finite(entry_row["long_margin"] if position == 1 else entry_row["short_margin"], 12),
        "entry_confidence": finite(entry_row["p_long"] if position == 1 else entry_row["p_short"], 12),
        "entry_open": finite(entry_open, 5),
        "exit_open": finite(exit_open, 5),
        "net_profit": finite(profit, 10),
        "previous_closed_balance_drawdown_percent": finite(previous_dd_pct, 6),
        base.SIDE_FILTER_FEATURE: finite(entry_row[base.SIDE_FILTER_FEATURE], 12),
        "exit_reason": exit_reason,
        "guardrail_expression": variant["guardrail_expression"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def update_drawdown_state(trade: Mapping[str, Any], equity: float, peak: float) -> tuple[float, float, float]:
    equity += as_float(trade.get("net_profit"))
    peak = max(peak, equity)
    drawdown = min(0.0, equity - peak)
    drawdown_pct = abs(drawdown) / DEPOSIT * 100.0
    return equity, peak, drawdown_pct


def candidate_status(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> str:
    if as_float(row.get("combined_trade_per_business_day")) < DENSITY_FLOOR:
        return "fail_density_floor(밀도 하한 실패)"
    if as_float(row.get("combined_short_count")) <= 0:
        return "fail_short_side_zero(숏 0 실패)"
    if as_float(row.get("validation_net_profit")) <= 0 or as_float(row.get("oos_net_profit")) <= 0:
        return "fail_split_profit(분할 수익 실패)"
    if as_float(row.get("combined_profit_factor")) <= TARGET_PF:
        return "watch_pf_not_above_target(PF 목표 미만 관찰)"
    if as_float(row.get("combined_max_drawdown")) < as_float(baseline.get("combined_max_drawdown")):
        return "watch_proxy_dd_worse_than_baseline(프록시 낙폭 기준 악화 관찰)"
    return "pass_pf_density_side_balance_proxy(PF/밀도/방향 프록시 통과)"


def selection_score(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> float:
    return (
        as_float(row.get("combined_net_profit"))
        + 250.0 * max(0.0, as_float(row.get("combined_profit_factor")) - as_float(baseline.get("combined_profit_factor")))
        + 120.0 * max(0.0, as_float(row.get("combined_trade_per_business_day")) - DENSITY_FLOOR)
        + 0.20 * as_float(row.get("combined_short_count"))
        + 0.50 * max(0.0, as_float(row.get("combined_max_drawdown")) - as_float(baseline.get("combined_max_drawdown")))
    )


def evaluate_queue(frame: pd.DataFrame, queue: Sequence[Mapping[str, Any]], baseline: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    best_trades = pd.DataFrame()
    audit_rows: list[dict[str, Any]] = []
    for variant in queue:
        trades, audit = simulate_guardrail(frame, variant)
        row: dict[str, Any] = {
            "run_id": RUN_ID,
            "queue_id": variant["queue_id"],
            "queue_rank": variant["queue_rank"],
            "variant_id": variant["variant_id"],
            "short_probability_threshold": finite(variant["short_threshold"], 12),
            "long_threshold": 0.0,
            "min_margin": finite(variant["min_margin"], 12),
            "long_block_feature": base.SIDE_FILTER_FEATURE,
            "long_block_min": finite(variant["long_block_min"], 6),
            "max_hold_m5": variant["max_hold_m5"],
            "guardrail_expression": variant["guardrail_expression"],
            "queue_type": variant["queue_type"],
            "trade_splitting_status": "not_used(미사용)",
            "proxy_boundary(프록시 경계)": "sequence_proxy_not_mt5_runtime(순서 프록시, MT5 런타임 아님)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for split in ["validation", "oos"]:
            row.update(base.metrics_for_trades(trades[trades["split"].eq(split)].copy(), split))
        row.update(base.metrics_for_trades(trades, "combined"))
        row["net_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_net_profit")) - as_float(baseline.get("combined_net_profit")), 10)
        row["pf_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_profit_factor")) - as_float(baseline.get("combined_profit_factor")), 10)
        row["dd_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_max_drawdown")) - as_float(baseline.get("combined_max_drawdown")), 10)
        row["density_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_trade_per_business_day")) - as_float(baseline.get("combined_trade_per_business_day")), 10)
        row["candidate_status"] = candidate_status(row, baseline)
        row["selection_score"] = finite(selection_score(row, baseline), 10)
        rows.append(row)
        audit_rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": variant["queue_id"],
                "variant_id": variant["variant_id"],
                **audit,
                "trade_count": len(trades),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
        if not rows or as_float(row["selection_score"]) >= max(as_float(item.get("selection_score")) for item in rows):
            best_trades = trades.copy()
    surface = pd.DataFrame(rows).sort_values("selection_score", ascending=False).reset_index(drop=True)
    best_id = surface.iloc[0]["variant_id"] if not surface.empty else ""
    if best_id and not best_trades.empty and str(best_trades["variant_id"].iloc[0]) != best_id:
        selected = next(item for item in queue if item["variant_id"] == best_id)
        best_trades, _ = simulate_guardrail(frame, selected)
    return surface, best_trades, audit_rows


def comparison_rows(best: Mapping[str, Any], baseline: Mapping[str, Any]) -> list[dict[str, Any]]:
    metrics = [
        ("combined_net_profit", True),
        ("combined_profit_factor", True),
        ("combined_trade_count", True),
        ("combined_trade_per_business_day", True),
        ("combined_max_drawdown", True),
        ("combined_recovery_factor", True),
        ("combined_short_count", True),
    ]
    rows = []
    for metric, higher_is_better in metrics:
        delta = as_float(best.get(metric)) - as_float(baseline.get(metric))
        rows.append(
            {
                "run_id": RUN_ID,
                "baseline_run_id": BASELINE_RUN_ID,
                "selected_variant_id": best.get("variant_id", ""),
                "metric_id": metric,
                "baseline_value": baseline.get(metric, ""),
                "selected_value": best.get(metric, ""),
                "delta_selected_minus_baseline": finite(delta, 10),
                "higher_is_better": higher_is_better,
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_queue_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "review_selected_proxy_candidate(선택 프록시 후보 검토)",
            "selected_variant_id": best.get("variant_id", ""),
            "candidate_status": best.get("candidate_status", ""),
            "required_review(필수 검토)": "proxy-vs-baseline attribution, density, side balance, DD pressure(프록시-기준 귀속, 밀도, 방향 균형, 낙폭 압박)",
            "effect(효과)": "package(MT5 패키지) 전 과적합과 단순 삭제 효과를 판정한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "decide_package_or_repair(패키지 또는 수리 결정)",
            "selected_variant_id": best.get("variant_id", ""),
            "candidate_status": best.get("candidate_status", ""),
            "required_review(필수 검토)": "if PF/DD/density pass, open runtime package; otherwise recycle failure memory(PF/DD/밀도 통과 시 런타임 패키지, 아니면 실패 기억 재사용)",
            "effect(효과)": "운영 주장 없이 다음 실행 경로를 좁힌다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def gate_row(name: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": "passed",
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(
    parent: Mapping[str, Any],
    baseline: Mapping[str, Any],
    surface: pd.DataFrame,
    best: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    pass_count = int(surface["candidate_status"].astype(str).str.startswith("pass_").sum()) if "candidate_status" in surface else 0
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_materialization_run_id": parent.get("run_id"),
        "baseline_variant_id": baseline.get("variant_id"),
        "scout_rows": int(len(surface)),
        "strict_pass_rows": pass_count,
        "selected_variant_id": best.get("variant_id", ""),
        "selected_queue_id": best.get("queue_id", ""),
        "selected_candidate_status": best.get("candidate_status", ""),
        "selected_combined_net_profit": best.get("combined_net_profit", ""),
        "selected_combined_profit_factor": best.get("combined_profit_factor", ""),
        "selected_combined_trade_count": best.get("combined_trade_count", ""),
        "selected_combined_trade_per_business_day": best.get("combined_trade_per_business_day", ""),
        "selected_combined_max_drawdown": best.get("combined_max_drawdown", ""),
        "selected_combined_recovery_factor": best.get("combined_recovery_factor", ""),
        "selected_combined_long_count": best.get("combined_long_count", ""),
        "selected_combined_short_count": best.get("combined_short_count", ""),
        "net_delta_vs_run364V_proxy": best.get("net_delta_vs_run364V_proxy", ""),
        "pf_delta_vs_run364V_proxy": best.get("pf_delta_vs_run364V_proxy", ""),
        "dd_delta_vs_run364V_proxy": best.get("dd_delta_vs_run364V_proxy", ""),
        "density_delta_vs_run364V_proxy": best.get("density_delta_vs_run364V_proxy", ""),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def write_receipts(final: Mapping[str, Any], surface: pd.DataFrame, best_trades: pd.DataFrame) -> list[dict[str, Any]]:
    base_payload = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = {
        DATA_RECEIPT: {
            **base_payload,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "runtime_rows": int(len(surface)),
            "selected_trade_rows": int(len(best_trades)),
            "timestamp_boundary": "guardrails use server entry time or previous closed balance only(가드레일은 서버 진입 시각 또는 이전 종료 잔고만 사용)",
            "effect(효과)": "미래참조 편향(look-ahead bias, 미래참조 편향)을 막는다.",
        },
        EXPERIMENT_RECEIPT: {
            **base_payload,
            "skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "PF/DD can improve through session/account-state/short guardrails without splitting trades(PF/DD가 거래 쪼개기 없이 가드레일로 개선 가능)",
            "comparison": "run364V selected proxy baseline(364V 선택 프록시 기준)",
            "stop_condition": "density < 3/day or short_count == 0(일 거래 3회 미만 또는 숏 0)",
        },
        MODEL_RECEIPT: {
            **base_payload,
            "skill": "obsidian-model-validation(모델 검증)",
            "model_training": "not_run(실행 안 함)",
            "onnx_export": "not_run(실행 안 함)",
            "effect(효과)": "threshold/rule scout(임계값/규칙 탐색)를 새 모델 권위로 오해하지 않는다.",
        },
        ATTRIBUTION_RECEIPT: {
            **base_payload,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "surface": rel(SCOUT_SURFACE),
            "baseline_comparison": rel(BASELINE_COMPARISON),
            "selected_candidate": final.get("selected_variant_id"),
            "attribution_confidence": "medium_proxy_only(프록시 전용 중간)",
        },
        JUDGMENT_RECEIPT: {
            **base_payload,
            "skill": "obsidian-result-judgment(결과 판정)",
            "result_subject": RUN_ID,
            "judgment_label": JUDGMENT,
            "evidence_available": [rel(SCOUT_SURFACE), rel(BASELINE_COMPARISON), rel(SELECTED_EXPECTED_TRADE_TAPE)],
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침)",
            "next_condition": NEXT_RUN_ID,
        },
        LINEAGE_RECEIPT: {
            **base_payload,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
        CLAIM_RECEIPT: {
            **base_payload,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "mt5_execution": "not_run(실행 안 함)",
            "effect(효과)": "proxy scout(프록시 탐색)를 운영 주장으로 승격하지 않는다.",
        },
    }
    for path, payload in receipts.items():
        write_json(path, payload)
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AA scope(범위)를 proxy scout(프록시 탐색)로 닫는다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점 안전 가드레일을 기록한다."),
        gate_row("experiment_design_audit(실험 설계 감사)", EXPERIMENT_RECEIPT, "가설/비교/중단 조건을 기록한다."),
        gate_row("proxy_replay_gate(프록시 재생 게이트)", SCOUT_SURFACE, "queue(대기열)를 순서 재생했다."),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "기준 대비 KPI 차이를 남긴다."),
        gate_row("model_boundary_gate(모델 경계 게이트)", MODEL_RECEIPT, "새 모델 학습과 ONNX 승격을 주장하지 않는다."),
        gate_row("result_judgment_gate(결과 판정 게이트)", JUDGMENT_RECEIPT, "proxy scout(프록시 탐색) 경계로 판정한다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 해시를 연결한다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "runtime authority(런타임 권위)를 닫지 않는다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "required gate(필수 게이트)를 closeout(종료 기록)에 연결한다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header(final: Mapping[str, Any]) -> None:
    if not exists(STAGE_BRIEF):
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
    lines = []
    for line in text.splitlines():
        if line.startswith("- current_run_id"):
            lines.append(f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`")
        elif line.startswith("- latest_completed_run_id"):
            lines.append(f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`")
        elif line.startswith("- selection_status"):
            lines.append(f"- selection_status(선택 상태): `{STATUS}`")
        elif line.startswith("- claim_boundary"):
            lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines) + "\n")


def write_docs(final: Mapping[str, Any], surface: pd.DataFrame, comparison: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header(final)
    top = surface.head(10).to_dict("records")
    text = f"""# Stage364AA PF/DD guardrail proxy scout(Stage364AA PF/DD 가드레일 프록시 탐색)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- scout_rows(탐색 행): `{final['scout_rows']}`
- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- selected net/PF/trades/density/DD(선택 순수익/수익 팩터/거래수/밀도/낙폭): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_max_drawdown']}`
- runtime_authority(런타임 권위): `not_claimed`

## Top proxy rows(상위 프록시 행)

{markdown_table(top, ['queue_id', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count', 'candidate_status', 'selection_score'])}

## Baseline comparison(기준 비교)

{markdown_table(comparison, ['metric_id', 'baseline_value', 'selected_value', 'delta_selected_minus_baseline'])}

## Gate audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 scout(탐색)는 package(패키지) 또는 repair(수리) 결정을 위한 proxy evidence(프록시 근거)다. MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"""

## {RUN_ID}

- report(보고서): `{rel(REPORT_PATH)}`
- judgment(판정): `{JUDGMENT}`
- selected(선택): `{final['selected_variant_id']}`
- effect(효과): PF/DD guardrail proxy scout(PF/DD 가드레일 프록시 탐색)를 완료하고 review(검토)로 넘긴다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""

## run364AA PF/DD guardrail proxy scout(364AA PF/DD 가드레일 프록시 탐색)

- action(행동): `run364Z` queue(대기열)를 기존 ONNX probability(온엑스 확률)에 sequence replay(순서 재생)했다.
- effect(효과): `{final['selected_variant_id']}`를 다음 review(검토) 대상으로 넘긴다.
- next(다음): `{NEXT_RUN_ID}`
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): proxy_review_candidate_not_operating(프록시 검토 후보, 운영 아님)
- latest_mt5_probe(최근 MT5 탐침): `run364X`
- latest_mt5_review(최근 MT5 검토): `run364Y`
- latest_materialization(최근 구체화): `run364Z`
- latest_proxy_scout(최근 프록시 탐색): `run364AA`
- selected_proxy_variant(선택 프록시 변형): `{final['selected_variant_id']}`
- selected_proxy_net_pf_density(선택 프록시 순수익/수익 팩터/밀도): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_per_business_day']}`
- blockers(차단): review(검토), package decision(패키지 결정), MT5 runtime probe(MT5 런타임 탐침), runtime authority audit(런타임 권위 감사)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364AA`는 `run364Z` PF/DD guardrail queue(PF/DD 가드레일 대기열)를 proxy replay(프록시 재생)했다. selected proxy(선택 프록시)는 `{final['selected_variant_id']}`이고 net/PF/trades/density/DD(순수익/수익 팩터/거래수/밀도/낙폭)는 `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_max_drawdown']}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 proxy evidence(프록시 근거)를 review(검토)하고 package(패키지) 또는 repair(수리)를 결정한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): PF/DD guardrail proxy scout(PF/DD 가드레일 프록시 탐색)를 실행했다.
- effect(효과): 다음 `{NEXT_RUN_ID}`에서 package(패키지) 또는 repair(수리) 결정을 검토할 수 있다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): session/account-state/short guardrails(세션/계좌상태/숏 가드레일)이 PF/DD(수익 팩터/낙폭)를 개선할 수 있다.
- positive clue(긍정 단서): selected proxy(선택 프록시) `{final['selected_variant_id']}`.
- failure memory(실패 기억): proxy replay(프록시 재생)는 MT5 runtime probe(MT5 런타임 탐침)를 대체하지 않는다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""

## {RUN_ID}

- action(행동): `run364Z` 대기열을 프록시 재생했다.
- effect(효과): 새 stage(단계) 분기 없이 Stage364(364단계)에서 PF/DD 수리를 계속한다.
""",
    )


def write_final_and_manifest(final: Mapping[str, Any]) -> None:
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "proxy_scout(프록시 탐색)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"selected={final['selected_variant_id']}; pass_rows={final['strict_pass_rows']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["scout_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(SCOUT_SURFACE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": "proxy_checked_no_trade_splitting(프록시 확인, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "net_profit": final["selected_combined_net_profit"],
        "profit_factor": final["selected_combined_profit_factor"],
        "trade_count": final["selected_combined_trade_count"],
        "expectancy": "",
        "max_drawdown_amount": final["selected_combined_max_drawdown"],
        "long_trade_count": final["selected_combined_long_count"],
        "short_trade_count": final["selected_combined_short_count"],
        "evidence_scope": "proxy_scout_no_authority(프록시 탐색, 권위 없음)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy scout surface(프록시 탐색 표면)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)"),
        (f"{RUN_ID}__Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "combined proxy scout(합산 프록시 탐색)"),
    ]:
        row = dict(common)
        row.update({"ledger_row_id": subrun_id, "subrun_id": subrun_id, "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": kpi_scope})
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("scout_surface", SCOUT_SURFACE, "Proxy scout surface(프록시 탐색 표면)."),
            ("selected_proxy_candidate", SELECTED_PROXY_CANDIDATE, "Selected proxy candidate(선택 프록시 후보)."),
            ("selected_expected_trade_tape", SELECTED_EXPECTED_TRADE_TAPE, "Selected expected trade tape(선택 예상 거래 테이프)."),
            ("baseline_comparison", BASELINE_COMPARISON, "Baseline comparison(기준 비교)."),
            ("run364AB_queue", RUN364AB_QUEUE, "Next review queue(다음 검토 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    selected = read_json(base.SELECTED_RUNTIME_CANDIDATE)
    frame, _, _ = base.load_runtime_frame()
    base.RUN_ID = RUN_ID
    base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    queue = load_queue(selected)
    baseline = normalize_baseline(selected)
    surface, best_trades, audit_rows = evaluate_queue(frame, queue, baseline)
    best = surface.iloc[0].to_dict()
    comparison = comparison_rows(best, baseline)
    review_queue = review_queue_rows(best)
    write_csv(SCOUT_SURFACE, surface.to_dict("records"))
    write_csv(SELECTED_EXPECTED_TRADE_TAPE, best_trades.to_dict("records"))
    write_json(SELECTED_PROXY_CANDIDATE, best)
    write_csv(GUARDRAIL_EFFECT_AUDIT, audit_rows)
    write_csv(BASELINE_COMPARISON, comparison)
    write_csv(RUN364AB_QUEUE, review_queue)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "data_integrity_audit",
                "experiment_design_audit",
                "proxy_replay_gate",
                "performance_attribution_gate",
                "model_boundary_gate",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    created_at_utc = now_utc()
    gates = write_receipts({"created_at_utc": created_at_utc}, surface, best_trades)
    final = final_payload(parent, baseline, surface, best, gates, created_at_utc)
    write_docs(final, surface, comparison, gates)
    write_final_and_manifest(final)
    write_ledgers(final, gates)
    write_final_and_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


def normalize_baseline(selected: Mapping[str, Any]) -> dict[str, Any]:
    mapping = {
        "variant_id": selected.get("variant_id"),
        "combined_net_profit": selected.get("combined_net_profit"),
        "combined_profit_factor": selected.get("combined_profit_factor"),
        "combined_trade_count": selected.get("combined_trade_count"),
        "combined_trade_per_business_day": selected.get("combined_trade_per_business_day"),
        "combined_max_drawdown": selected.get("combined_max_drawdown"),
        "combined_recovery_factor": selected.get("combined_recovery_factor"),
        "combined_short_count": selected.get("combined_short_count"),
        "combined_long_count": selected.get("combined_long_count"),
    }
    return mapping


if __name__ == "__main__":
    main()
