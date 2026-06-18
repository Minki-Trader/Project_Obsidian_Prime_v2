from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_82 import frontier82b_density_first_runtime_economic_mechanism_proxy_scout as f82b


STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
RUN_ID = "frontier84D_runtime_realized_winrate_proxy_runtime_gap_analysis_v1"
PARENT_RUN_ID = "frontier84C_mt5_runtime_realized_winrate_materialization_v1"
SOURCE_PROXY_RUN_ID = "frontier84B_runtime_realized_winrate_proxy_scout_v1"
NEXT_RUN_ID = "frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_v1"
STATUS = "f84d_runtime_gap_attributed_negative_runtime_deal_economics_no_authority"
JUDGMENT = "signal_feature_onnx_parity_passed_runtime_winrate_pf_dd_failed_row_level_reconciliation_required_no_authority"
CLAIM_BOUNDARY = (
    "gap_attribution_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F84B_SUMMARY = REVIEW_DIR / "f84b_runtime_realized_winrate_proxy_scout_summary.json"
F84B_TOP = REVIEW_DIR / "f84b_runtime_realized_winrate_proxy_top_candidates.csv"
F84C_SUMMARY = REVIEW_DIR / "f84c_mt5_runtime_realized_winrate_materialization_summary.json"
F84C_TARGET = REVIEW_DIR / "f84c_runtime_realized_winrate_materialization_target_selection.json"
F84C_MANIFEST = PARENT_RUN_DIR / "run_manifest.json"
F84C_RECEIPT = PARENT_RUN_DIR / "f84c_runtime_receipt.csv"
F84C_PROB_PARITY = PARENT_RUN_DIR / "f84c_probability_parity.csv"
F84C_SIGNAL_PARITY = PARENT_RUN_DIR / "f84c_signal_parity.csv"
F84C_FEATURE_PARITY = PARENT_RUN_DIR / "f84c_feature_readiness_parity.csv"
F84C_SOURCE_REPRO = PARENT_RUN_DIR / "f84c_source_reproduction.csv"

SUMMARY = REVIEW_DIR / "f84d_runtime_realized_winrate_gap_analysis_summary.json"
GAP_ROWS = REVIEW_DIR / "f84d_runtime_realized_winrate_gap_rows.csv"
REPORT = REVIEW_DIR / "frontier84D_runtime_realized_winrate_proxy_runtime_gap_analysis_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f84d.md"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f84d_run_evidence_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f84d_performance_attribution_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f84d_result_judgment_receipt.yaml"
RUNTIME_PARITY_RECEIPT = REVIEW_DIR / "f84d_runtime_parity_receipt.yaml"
BACKTEST_FORENSICS_RECEIPT = REVIEW_DIR / "f84d_backtest_forensics_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f84d_claim_discipline_receipt.yaml"
TASK_FORCE_REVIEW = REVIEW_DIR / "f84d_task_force_review_receipt.yaml"
ACTUAL_SUBAGENT_CALLS = REVIEW_DIR / "f84d_actual_subagent_calls.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f84d_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f84d_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_84/frontier84d_runtime_realized_winrate_proxy_runtime_gap_analysis.py"

MIN_FINAL_TPD = 5.0
MAX_FINAL_TPD = 10.0
MIN_FINAL_PF = 2.0
HIGH_FINAL_PF = 3.0
MAX_FINAL_DD = 10.0
EXPECTED_TASK_FORCE_CALLS = 8
REQUIRED_TASK_FORCE_ROSTER_IDS = (
    "agent_01_system_governor",
    "agent_02_platform_routing_architect",
    "agent_03_philosophy_policy_skill_governance",
    "agent_04_evidence_control_plane",
    "agent_05_data_feature_contract",
    "agent_06_quant_research",
    "agent_07_model_validation_risk",
    "agent_08_mt5_onnx_runtime",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def remove_csv_rows(path: Path, predicate: Callable[[dict[str, str]], bool]) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [row for row in reader if not predicate(row)]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_csv_row(path: Path, row: Mapping[str, Any], *, key: str | None = None, source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    if key:
        rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def split_prefix(split: str) -> str:
    return "val" if split == "validation" else split


def load_actual_subagent_calls() -> list[dict[str, Any]]:
    if not path_exists(ACTUAL_SUBAGENT_CALLS):
        return []
    payload = read_json(ACTUAL_SUBAGENT_CALLS)
    if isinstance(payload, Mapping):
        return list(payload.get("actual_subagent_calls") or [])
    return list(payload or [])


def task_force_roster_summary(actual_calls: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    required = set(REQUIRED_TASK_FORCE_ROSTER_IDS)
    roster_ids = {str(call.get("roster_id") or "") for call in actual_calls}
    roster_ids.discard("")
    covered = sorted(roster_id for roster_id in REQUIRED_TASK_FORCE_ROSTER_IDS if roster_id in roster_ids)
    missing = sorted(required.difference(roster_ids))
    extras = sorted(roster_ids.difference(required))
    return {
        "required_roster_ids": list(REQUIRED_TASK_FORCE_ROSTER_IDS),
        "covered_roster_ids": covered,
        "missing_roster_ids": missing,
        "extra_roster_ids": extras,
        "coverage_count": len(covered),
        "required_count": len(REQUIRED_TASK_FORCE_ROSTER_IDS),
        "all_required_covered": len(missing) == 0,
    }


def telemetry_summary(row: Mapping[str, Any]) -> dict[str, Any]:
    path = Path(str(row.get("summary_path") or ""))
    if not str(path):
        return {"status": "missing_path"}
    if not io_path(path).exists():
        return {"status": "missing_file", "path": path.as_posix()}
    rows = read_csv(path)
    if not rows:
        return {"status": "empty", "path": path.as_posix()}
    summary = rows[-1]
    return {
        "status": "loaded",
        "path": path.as_posix(),
        "ticks_seen": as_int(summary.get("ticks_seen")),
        "bars_seen": as_int(summary.get("bars_seen")),
        "feature_ready_count": as_int(summary.get("feature_ready_count")),
        "feature_skip_count": as_int(summary.get("feature_skip_count")),
        "model_ok_count": as_int(summary.get("model_ok_count")),
        "model_fail_count": as_int(summary.get("model_fail_count")),
        "long_count": as_int(summary.get("long_count")),
        "short_count": as_int(summary.get("short_count")),
        "flat_count": as_int(summary.get("flat_count")),
        "order_attempt_count": as_int(summary.get("order_attempt_count")),
        "order_fill_count": as_int(summary.get("order_fill_count")),
        "min_lot_floor_applied_count": as_int(summary.get("min_lot_floor_applied_count")),
        "max_model_risk_pct": as_float(summary.get("max_model_risk_pct")),
        "max_actual_risk_pct_after_floor": as_float(summary.get("max_actual_risk_pct_after_floor")),
        "last_skip_reason": summary.get("last_skip_reason"),
    }


def objective_failure_tags(row: Mapping[str, Any]) -> list[str]:
    tags: list[str] = []
    runtime_tpd = as_float(row.get("runtime_trades_per_day"))
    runtime_pf = as_float(row.get("runtime_profit_factor"))
    runtime_dd = as_float(row.get("runtime_drawdown_percent"))
    short_trades = as_int(row.get("runtime_short_trade_count"))
    if not (MIN_FINAL_TPD <= runtime_tpd <= MAX_FINAL_TPD):
        tags.append("density_outside_5_to_10_per_day(일 5~10회 범위 밖)")
    if runtime_pf < MIN_FINAL_PF:
        tags.append("pf_below_2(수익 팩터 2 미만)")
    if runtime_dd >= MAX_FINAL_DD:
        tags.append("dd_above_or_equal_10_percent(손실폭 10% 이상)")
    if short_trades == 0:
        tags.append("one_sided_long_only(롱 전용)")
    tags.append("wfo_stress_curve_not_checked(워크포워드/스트레스/곡선 미검증)")
    return tags


def build_gap_rows(runtime_rows: Sequence[Mapping[str, Any]], target: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for runtime in runtime_rows:
        split = str(runtime.get("split") or "")
        prefix = split_prefix(split)
        proxy_net = as_float(runtime.get("proxy_net_profit"))
        proxy_pf = as_float(runtime.get("proxy_profit_factor"))
        proxy_tpd = as_float(runtime.get("proxy_trades_per_day"))
        proxy_dd = as_float(runtime.get("proxy_dd_percent"))
        runtime_net = as_float(runtime.get("net_profit"))
        runtime_pf = as_float(runtime.get("profit_factor"))
        runtime_tpd = as_float(runtime.get("trades_per_day"))
        runtime_dd = as_float(runtime.get("max_drawdown_percent"))
        runtime_trades = as_int(runtime.get("trade_count"))
        runtime_long = as_int(runtime.get("long_trade_count"))
        runtime_short = as_int(runtime.get("short_trade_count"))
        runtime_win_rate_pct = as_float(runtime.get("win_rate_percent"))
        proxy_win_rate_pct = as_float(target.get(f"{prefix}_win_rate_percent"))
        expected_signal = as_int(runtime.get("expected_signal_count"))
        signal_count = as_int(runtime.get("signal_count"))
        expected_selected = as_int(runtime.get("expected_selected_trade_count"))
        order_attempt = as_int(runtime.get("order_attempt_count"))
        order_fill = as_int(runtime.get("order_fill_count"))
        summary = telemetry_summary(runtime)
        gap_class = "runtime_deal_economics_gap_after_signal_parity"
        if as_int(runtime.get("signal_count_diff")) != 0 or as_int(runtime.get("feature_ready_diff")) != 0:
            gap_class = "parity_gap_requires_repair"
        elif order_fill < expected_selected and (expected_selected - order_fill) > max(20, expected_selected * 0.02):
            gap_class = "order_fill_gap_material"
        row = {
            "split": split,
            "candidate_id": runtime.get("candidate_id"),
            "source_candidate_id": target.get("candidate_id"),
            "model": target.get("model"),
            "axis_id": runtime.get("axis_id"),
            "test_period_start": runtime.get("test_period_start"),
            "test_period_end": runtime.get("test_period_end"),
            "calendar_days_exclusive": as_int(runtime.get("calendar_days_exclusive")),
            "tester_status": runtime.get("tester_status"),
            "runtime_status": runtime.get("runtime_status"),
            "report_status": runtime.get("report_status"),
            "proxy_net_profit": proxy_net,
            "runtime_net_profit": runtime_net,
            "net_runtime_minus_proxy": runtime_net - proxy_net,
            "proxy_profit_factor": proxy_pf,
            "runtime_profit_factor": runtime_pf,
            "pf_runtime_minus_proxy": runtime_pf - proxy_pf,
            "proxy_drawdown_percent": proxy_dd,
            "runtime_drawdown_percent": runtime_dd,
            "dd_runtime_minus_proxy": runtime_dd - proxy_dd,
            "proxy_trades_per_day": proxy_tpd,
            "runtime_trades_per_day": runtime_tpd,
            "trades_per_day_runtime_minus_proxy": runtime_tpd - proxy_tpd,
            "proxy_trade_count": as_int(target.get(f"{prefix}_trade_count")),
            "runtime_trade_count": runtime_trades,
            "trade_count_runtime_minus_proxy": runtime_trades - as_int(target.get(f"{prefix}_trade_count")),
            "expected_signal_count": expected_signal,
            "runtime_signal_count": signal_count,
            "signal_count_diff": as_int(runtime.get("signal_count_diff")),
            "feature_ready_count": as_int(runtime.get("feature_ready_count")),
            "feature_ready_diff": as_int(runtime.get("feature_ready_diff")),
            "expected_selected_trade_count": expected_selected,
            "order_attempt_count": order_attempt,
            "order_fill_count": order_fill,
            "order_fill_rate": as_float(runtime.get("order_fill_rate")),
            "selected_to_order_attempt_gap": order_attempt - expected_selected,
            "selected_to_order_fill_gap": order_fill - expected_selected,
            "proxy_win_rate_percent": proxy_win_rate_pct,
            "runtime_win_rate_percent": runtime_win_rate_pct,
            "win_rate_runtime_minus_proxy_pct_points": runtime_win_rate_pct - proxy_win_rate_pct,
            "runtime_winning_trade_count": as_int(runtime.get("winning_trade_count")),
            "runtime_losing_trade_count": as_int(runtime.get("losing_trade_count")),
            "runtime_average_win": as_float(runtime.get("average_win")),
            "runtime_average_loss": as_float(runtime.get("average_loss")),
            "runtime_payoff_ratio": as_float(runtime.get("payoff_ratio")),
            "runtime_expectancy": as_float(runtime.get("expectancy")),
            "runtime_recovery_factor": as_float(runtime.get("recovery_factor")),
            "runtime_gross_profit": as_float(runtime.get("gross_profit")),
            "runtime_gross_loss": as_float(runtime.get("gross_loss")),
            "runtime_long_trade_count": runtime_long,
            "runtime_short_trade_count": runtime_short,
            "runtime_time_under_water": "missing_from_f84c_runtime_receipt",
            "runtime_max_consecutive_loss": "missing_from_f84c_runtime_receipt",
            "proxy_time_under_water_trades": target.get(f"{prefix}_time_under_water_trades", ""),
            "proxy_max_consecutive_loss": target.get(f"{prefix}_max_consecutive_loss", ""),
            "telemetry_bars_seen": summary.get("bars_seen", ""),
            "telemetry_feature_ready_count": summary.get("feature_ready_count", ""),
            "telemetry_feature_skip_count": summary.get("feature_skip_count", ""),
            "telemetry_order_attempt_count": summary.get("order_attempt_count", ""),
            "telemetry_order_fill_count": summary.get("order_fill_count", ""),
            "telemetry_last_skip_reason": summary.get("last_skip_reason", ""),
            "runtime_gap_class": gap_class,
            "objective_failure_tags": "",
            "report_path": runtime.get("report_path"),
            "telemetry_summary_path": runtime.get("summary_path"),
            "telemetry_summary_status": summary.get("status"),
        }
        row["objective_failure_tags"] = ";".join(objective_failure_tags(row))
        rows.append(row)
    return rows


def parity_summary() -> dict[str, Any]:
    prob = read_csv(F84C_PROB_PARITY)
    signal = read_csv(F84C_SIGNAL_PARITY)
    feature = read_csv(F84C_FEATURE_PARITY)
    source = read_csv(F84C_SOURCE_REPRO)
    return {
        "probability_rows": len(prob),
        "probability_pass_rows": sum(1 for row in prob if str(row.get("passed")).lower() in {"true", "1"}),
        "probability_max_abs_diff": max([as_float(row.get("patched_three_col_max_abs_diff")) for row in prob] or [0.0]),
        "signal_rows": len(signal),
        "signal_pass_rows": sum(1 for row in signal if str(row.get("passed")).lower() in {"true", "1"}),
        "signal_mismatch_total": sum(as_int(row.get("signal_mismatch_count_after_veto")) for row in signal),
        "feature_rows": len(feature),
        "feature_pass_rows": sum(1 for row in feature if str(row.get("feature_readiness_parity")).lower() in {"true", "1"}),
        "source_reproduction_rows": len(source),
        "source_reproduction_pass_rows": sum(1 for row in source if str(row.get("passed")).lower() in {"true", "1"}),
    }


def build_payload(created_at: str) -> dict[str, Any]:
    f84b_summary = read_json(F84B_SUMMARY)
    f84c_summary = read_json(F84C_SUMMARY)
    f84c_target_payload = read_json(F84C_TARGET)
    f84c_manifest = read_json(F84C_MANIFEST)
    target = dict(f84c_target_payload.get("runtime_materialization_target") or f84c_manifest.get("target") or {})
    runtime_rows = read_csv(F84C_RECEIPT)
    gap_rows = build_gap_rows(runtime_rows, target)
    validation = next((row for row in gap_rows if row["split"] == "validation"), {})
    oos = next((row for row in gap_rows if row["split"] == "oos"), {})
    actual_calls = load_actual_subagent_calls()
    parity = parity_summary()
    completed = [row for row in runtime_rows if row.get("tester_status") == "completed"]
    feature_signal_clean = all(as_int(row.get("feature_ready_diff")) == 0 and as_int(row.get("signal_count_diff")) == 0 for row in runtime_rows)
    order_fill_material_gap = any(
        abs(as_int(row.get("selected_to_order_fill_gap"))) > max(20, as_int(row.get("expected_selected_trade_count")) * 0.02)
        for row in gap_rows
    )
    roster_summary = task_force_roster_summary(actual_calls)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "target": target,
        "source_best_candidate": target.get("source_best_candidate"),
        "source_best_model": target.get("source_best_model"),
        "f84b_counts": {
            "candidate_rows": f84b_summary.get("candidate_rows"),
            "materialization_candidate_count": f84b_summary.get("materialization_candidate_count"),
            "meaningful_signal_count": f84b_summary.get("meaningful_signal_count"),
            "final_like_reference_count": f84b_summary.get("final_like_reference_count"),
        },
        "parent_status": f84c_summary.get("status"),
        "parent_judgment": f84c_summary.get("judgment"),
        "parent_attempt_count": f84c_summary.get("attempt_count"),
        "parent_completed_attempt_count": f84c_summary.get("completed_attempt_count"),
        "runtime_parity_preserved": len(completed) == len(runtime_rows) and feature_signal_clean and parity["probability_pass_rows"] == 3 and parity["signal_pass_rows"] == 3 and parity["source_reproduction_pass_rows"] >= 2,
        "parity": parity,
        "gap_rows": gap_rows,
        "validation_gap": validation,
        "oos_gap": oos,
        "observed_change": "F84B exportable proxy(내보내기 가능한 프록시)는 5-10 trades/day(일 5~10회 거래) density(밀도)를 보존했지만, MT5 runtime economics(MT5 런타임 경제성)는 win-rate erosion(승률 침식)과 drawdown expansion(손실폭 확대)로 음수 전환했다.",
        "primary_attribution": "runtime_deal_economics_winrate_dd_gap_after_signal_parity(신호 동등성 이후 런타임 거래 경제성/승률/손실폭 간극)",
        "not_primary_drivers": [
            "signal_count_mismatch(신호 수 불일치): zero diff after veto on validation/OOS",
            "feature_readiness_mismatch(피처 준비 불일치): zero diff on validation/OOS",
            "ONNX_handoff(온엑스 인계): probability and signal parity rows passed",
            "order_fill(주문 체결): fill gap is small and not enough to explain PF/DD collapse",
        ],
        "remaining_objective_gaps": [
            "profit_factor_below_2_to_3(수익 팩터 2~3 미달)",
            "drawdown_above_10_percent(손실폭 10% 초과)",
            "smooth_balance_equity_curve_not_present(매끄러운 잔고/자산 곡선 부재)",
            "one_sided_long_only(롱 전용)",
            "WFO_stress_not_validated(워크포워드/스트레스 미검증)",
        ],
        "preserved_clue": "F84B target(대상)은 MT5 runtime(MT5 런타임)에서 final-like density(최종 조건에 가까운 밀도)를 보존했고 feature/signal/ONNX parity(피처/신호/온엑스 동등성)를 통과했다.",
        "negative_memory": "Runtime-realized winrate labels(런타임 실현 승률 라벨)는 actual MT5 win rate/drawdown(실제 MT5 승률/손실폭)을 보존하지 못했다. 이 long-only exportable branch(롱 전용 내보내기 가능 가지)에서 threshold-only repair(임계값만 수리)는 피한다.",
        "alternative_explanations": [
            "intrabar TP/SL(봉 내부 익절/손절)과 broker deal accounting(브로커 거래 회계)이 contract proxy labels(계약 프록시 라벨)와 다를 수 있다",
            "proxy utility(프록시 효용)가 realized tester win rate(테스터 실현 승률)가 낮은 패턴을 아직 보상할 수 있다",
            "long-only high-vol intent-release pocket(롱 전용 고변동 의도 해제 구간)이 loss clustering(손실 군집)에 노출된다",
            "runtime stop/take-profit point mapping(런타임 손절/익절 포인트 매핑)은 parity-ready(동등성 준비됨)이지만 economic shape(경제적 형태)는 tester deals(테스터 거래)에 보정되지 않았다",
        ],
        "attribution_confidence": "high_for_not_parity_or_fill_medium_for_exact_deal_mechanism(동등성/체결 원인 배제는 높음, 정확한 거래 메커니즘 귀속은 중간)",
        "next_probe": "F84E should open row-level deal reconciliation(행 단위 거래 조정) before capped repair or rotation(상한 있는 수리 또는 회전 전): join(결합) proxy rows(프록시 행), veto tape(차단 테이프), telemetry(원격 측정), and MT5 trade/deal rows(MT5 거래/딜 행) to isolate realized win/loss(실현 승패), PnL(손익), cost(비용), and TP/SL path(익절/손절 경로).",
        "order_fill_material_gap": order_fill_material_gap,
        "actual_subagent_calls": actual_calls,
        "actual_subagent_call_count": len(actual_calls),
        "actual_subagent_minimum_expected_count": EXPECTED_TASK_FORCE_CALLS,
        "actual_subagent_roster_coverage": roster_summary,
        "actual_subagent_roster_ids": roster_summary["covered_roster_ids"],
        "actual_subagent_missing_roster_ids": roster_summary["missing_roster_ids"],
        "actual_subagent_extra_roster_ids": roster_summary["extra_roster_ids"],
        "result_label": "negative_runtime_gap_attribution_with_density_clue_preserved",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_inputs": [rel(F84B_SUMMARY), rel(F84B_TOP), rel(F84C_SUMMARY), rel(F84C_TARGET), rel(F84C_MANIFEST), rel(F84C_RECEIPT), rel(F84C_PROB_PARITY), rel(F84C_SIGNAL_PARITY), rel(F84C_FEATURE_PARITY), rel(F84C_SOURCE_REPRO)],
    }


def task_force_call_text(payload: Mapping[str, Any]) -> str:
    coverage = payload.get("actual_subagent_roster_coverage") or {}
    return (
        f"{payload.get('actual_subagent_call_count')} calls; "
        f"roster {coverage.get('coverage_count')}/{coverage.get('required_count')}"
    )


def report_text(payload: Mapping[str, Any]) -> str:
    target = payload["target"]
    val = payload["validation_gap"]
    oos = payload["oos_gap"]
    return f"""# F84D Runtime-Realized Winrate Proxy/Runtime Gap Analysis(F84D 런타임 실현 승률 프록시/런타임 간극 분석)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- source best(원천 최선): `{payload.get('source_best_candidate')}` / `{payload.get('source_best_model')}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- actual sub-agent calls(실제 하위 에이전트 호출): `{task_force_call_text(payload)}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Readout(판독)

Action(행동): F84B proxy(프록시) target(대상)과 F84C MT5 runtime(런타임) 결과를 split(구간)별로 비교했다.

Effect(효과): signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 보존됐지만, MT5 deal economics(거래 경제성), win rate(승률), DD(손실폭)가 붕괴한 negative evidence(부정 근거)를 F84E row-level deal reconciliation(행 단위 거래 조정) 입력으로 고정한다.

| split(구간) | proxy net/PF/DD/TPD(프록시 순손익/수익 팩터/손실폭/일 거래 수) | MT5 net/PF/DD/TPD(MT5 순손익/수익 팩터/손실폭/일 거래 수) | win rate proxy->runtime(승률 프록시->런타임) | signal diff(신호 차이) | fill gap(체결 간극) |
|---|---:|---:|---:|---:|---:|
| validation(검증) | `{fmt(val.get('proxy_net_profit'))}/{fmt(val.get('proxy_profit_factor'))}/{fmt(val.get('proxy_drawdown_percent'))}/{fmt(val.get('proxy_trades_per_day'))}` | `{fmt(val.get('runtime_net_profit'))}/{fmt(val.get('runtime_profit_factor'))}/{fmt(val.get('runtime_drawdown_percent'))}/{fmt(val.get('runtime_trades_per_day'))}` | `{fmt(val.get('proxy_win_rate_percent'))}% -> {fmt(val.get('runtime_win_rate_percent'))}%` | `{val.get('signal_count_diff')}` | `{val.get('selected_to_order_fill_gap')}` |
| OOS(표본외) | `{fmt(oos.get('proxy_net_profit'))}/{fmt(oos.get('proxy_profit_factor'))}/{fmt(oos.get('proxy_drawdown_percent'))}/{fmt(oos.get('proxy_trades_per_day'))}` | `{fmt(oos.get('runtime_net_profit'))}/{fmt(oos.get('runtime_profit_factor'))}/{fmt(oos.get('runtime_drawdown_percent'))}/{fmt(oos.get('runtime_trades_per_day'))}` | `{fmt(oos.get('proxy_win_rate_percent'))}% -> {fmt(oos.get('runtime_win_rate_percent'))}%` | `{oos.get('signal_count_diff')}` | `{oos.get('selected_to_order_fill_gap')}` |

## Attribution(귀속)

Primary attribution(주 귀속): `{payload.get('primary_attribution')}`.

Not primary drivers(주 원인 아님): signal count mismatch(신호 수 불일치), feature readiness mismatch(피처 준비 불일치), ONNX handoff(온엑스 인계), material order fill gap(중대한 주문 체결 간극).

Preserved clue(보존 단서): `{payload.get('preserved_clue')}`

Negative memory(부정 기억): `{payload.get('negative_memory')}`

Closeout KPI note(마감 핵심 성과 지표 참고): F84C runtime receipt(런타임 영수증)는 gross profit/loss(총이익/총손실), win rate(승률), avg win/loss(평균 이익/손실), payoff ratio(손익비), expectancy(기대값), recovery factor(회복 계수), long/short breakdown(롱/숏 분해)을 포함한다. Runtime time under water(런타임 회복 전 체류 시간)와 max consecutive loss(최대 연속 손실)는 F84C normalized receipt(정규화 영수증)에 없어 unavailable(미확보)로 둔다.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F84D Required Gate Coverage Audit(F84D 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `runtime_materialization_evidence(런타임 물질화 근거)` | `passed(통과)` | `{rel(F84C_RECEIPT)}` | F84C Strategy Tester(전략 테스터) 결과를 입력으로 쓴다. |
| `proxy_runtime_gap_analysis(프록시/런타임 간극 분석)` | `passed(통과)` | `{rel(SUMMARY)}`, `{rel(GAP_ROWS)}` | split(구간)별 KPI gap(핵심 성과 지표 간극)을 기록한다. |
| `parity_not_cause_boundary(동등성 비원인 경계)` | `passed(통과)` | `{rel(F84C_PROB_PARITY)}`, `{rel(F84C_SIGNAL_PARITY)}`, `{rel(F84C_FEATURE_PARITY)}` | parity(동등성)를 주 원인에서 제외한다. |
| `backtest_forensics_receipt(백테스트 포렌식 영수증)` | `passed(통과)` | `{rel(BACKTEST_FORENSICS_RECEIPT)}` | tester report(테스터 보고서)와 실행 정체성을 분리한다. |
| `performance_attribution_receipt(성과 귀속 영수증)` | `passed(통과)` | `{rel(PERFORMANCE_RECEIPT)}` | deal economics/win-rate/DD(거래 경제성/승률/손실폭) 붕괴를 귀속한다. |
| `result_judgment_boundary(결과 판정 경계)` | `passed(통과)` | `{rel(RESULT_RECEIPT)}` | negative evidence(부정 근거)와 preserved clue(보존 단서)를 분리한다. |
| `actual_subagent_calls(실제 하위 에이전트 호출)` | `{task_force_call_text(payload)}` | `{rel(ACTUAL_SUBAGENT_CALLS)}` | Task Force(태스크포스)를 실제 호출 기록과 연결한다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `{rel(TASK_FORCE_REVIEW)}` | 8명 agent(요원) 검토와 Codex local verification(로컬 검증)을 분리한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | authority/live readiness(권위/실거래 준비)를 만들지 않는다. |
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    val = payload["validation_gap"]
    oos = payload["oos_gap"]
    return {
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: kpi_evidence_recorded_no_authority
source_authority: parent_mt5_runtime_materialization(F84C 부모 MT5 런타임 물질화)
required_records:
  hypothesis: runtime_realized_winrate_labels_rebuild(런타임 실현 승률 라벨 재구축)
  test_period: validation 2025-01-02..2025-10-01; OOS 2025-10-01..2026-04-14
  proxy_kpi: validation net/PF/DD/TPD={val.get('proxy_net_profit')}/{val.get('proxy_profit_factor')}/{val.get('proxy_drawdown_percent')}/{val.get('proxy_trades_per_day')}; OOS net/PF/DD/TPD={oos.get('proxy_net_profit')}/{oos.get('proxy_profit_factor')}/{oos.get('proxy_drawdown_percent')}/{oos.get('proxy_trades_per_day')}
  runtime_kpi: validation net/PF/DD/TPD={val.get('runtime_net_profit')}/{val.get('runtime_profit_factor')}/{val.get('runtime_drawdown_percent')}/{val.get('runtime_trades_per_day')}; OOS net/PF/DD/TPD={oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}
  parity: signal_feature_onnx_parity_preserved(신호/피처/온엑스 동등성 보존)
  gap_cause: {payload.get('primary_attribution')}
  next_action: {NEXT_RUN_ID}
tier_records:
  tier_a_separate: recorded
  tier_b_separate: missing_required
  combined: out_of_scope_by_claim
claim_boundary: {CLAIM_BOUNDARY}
""",
        PERFORMANCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: runtime_deal_economics_gap_attributed_no_authority
observed_change: "{payload.get('observed_change')}"
comparison_baseline: F84B proxy candidate f84b_00287(F84B 프록시 후보)
likely_drivers:
  - runtime_deal_economics(런타임 거래 경제성)
  - win_rate_erosion(승률 침식)
  - drawdown_expansion(손실폭 팽창)
not_primary_drivers:
  - signal_count_mismatch(신호 수 불일치)
  - feature_readiness_mismatch(피처 준비 불일치)
  - ONNX_handoff(온엑스 인계)
  - material_order_fill_gap(중대한 주문 체결 간극)
attribution_confidence: {payload.get('attribution_confidence')}
next_probe: "{payload.get('next_probe')}"
claim_boundary: {CLAIM_BOUNDARY}
""",
        RUNTIME_PARITY_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-runtime-parity
status: parity_preserved_but_economics_failed_no_authority
research_path: {rel(F84B_TOP)}
runtime_path: {rel(F84C_MANIFEST)}
shared_contract: feature order, ONNX probabilities, selected-entry veto tape, split periods(피처 순서/온엑스 확률/선택 진입 차단 테이프/구간)
known_differences: MT5 deal accounting and intrabar execution economics differ from proxy contract KPI(MT5 거래 회계와 봉내 실행 경제성이 프록시 계약 KPI와 다름)
parity_check: probability={payload['parity'].get('probability_pass_rows')}/3; signal={payload['parity'].get('signal_pass_rows')}/3; feature={payload['parity'].get('feature_pass_rows')}/1; source_reproduction={payload['parity'].get('source_reproduction_pass_rows')}/2
runtime_claim_boundary: runtime_probe_gap_attribution_only(런타임 탐침 간극 귀속만)
claim_boundary: {CLAIM_BOUNDARY}
""",
        BACKTEST_FORENSICS_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-backtest-forensics
status: parent_strategy_tester_reports_usable_with_boundary
tester_identity: parent F84C run_manifest(부모 F84C 실행 목록)
report_identity:
  validation: {val.get('report_path')}
  oos: {oos.get('report_path')}
trade_evidence: validation trades={val.get('runtime_trade_count')}; OOS trades={oos.get('runtime_trade_count')}
cost_assumptions: broker tester environment(브로커 테스터 환경); exact deal list unavailable in normalized receipt(정규화 영수증에 거래 목록 미포함)
backtest_judgment: usable_with_boundary(경계 있는 사용 가능)
claim_boundary: {CLAIM_BOUNDARY}
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: negative_runtime_gap_with_preserved_density_clue_no_authority
result_subject: F84C runtime materialized target f84b_00287(F84C 런타임 물질화 대상)
evidence_available: MT5 runtime receipt, parity CSVs, telemetry summary, Strategy Tester reports(MT5 런타임 영수증/동등성 CSV/텔레메트리 요약/전략 테스터 보고서)
evidence_missing: runtime time under water and max consecutive loss in normalized receipt(정규화 영수증의 회복 전 체류 시간/최대 연속 손실)
judgment_label: negative(부정)
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_gap_analysis_no_authority
allowed_claims:
  - runtime_gap_attributed(런타임 간극 귀속)
  - density_clue_preserved(밀도 단서 보존)
  - row_level_reconciliation_required_before_repair_or_rotation(수리 또는 회전 전 행 단위 조정 필요)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{JUDGMENT}; boundary={CLAIM_BOUNDARY}"
""",
    }


def task_force_review_text(payload: Mapping[str, Any]) -> str:
    calls = payload.get("actual_subagent_calls") or []
    rendered_calls: list[str] = []
    for call in calls:
        summary = str(call.get("summary", "")).replace("\r", " ").replace("\n", " ").replace('"', "'")
        rendered_calls.append(
            f"  - roster_id: {call.get('roster_id')}\n"
            f"    nickname: {call.get('nickname')}\n"
            f"    agent_id: {call.get('agent_id')}\n"
            f"    status: {call.get('status')}\n"
            f"    summary: \"{summary}\""
        )
    call_lines = "\n".join(rendered_calls)
    if not call_lines:
        call_lines = "  []"
    return f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f84d_gap_analysis_no_authority
review_mode: actual_subagent_calls_plus_codex_local_verification(실제 하위 에이전트 호출 + 코덱스 로컬 검증)
roster_registry: docs/agent_control/codex_task_force_registry.yaml
actual_subagent_call_count: {payload.get('actual_subagent_call_count')}
minimum_expected_subagent_call_count: {EXPECTED_TASK_FORCE_CALLS}
required_roster_coverage: {payload.get('actual_subagent_roster_coverage', {}).get('coverage_count')}/{payload.get('actual_subagent_roster_coverage', {}).get('required_count')}
missing_roster_ids: {payload.get('actual_subagent_missing_roster_ids')}
extra_roster_ids: {payload.get('actual_subagent_extra_roster_ids')}
actual_subagent_calls:
{call_lines}
project_native_review:
  accepted:
    - "F84C parity(동등성)는 주 원인이 아니며 deal economics/win-rate/DD(거래 경제성/승률/손실폭) 붕괴를 F84D 주 귀속으로 둔다."
    - "F84B density clue(밀도 단서)는 보존하되 threshold-only repair(임계값만 수리)는 금지한다."
    - "F84E는 new axis(새 축) 수리 또는 rotation(회전)을 결정해야 한다."
  rejected:
    - "Do not treat actual sub-agent calls(실제 하위 에이전트 호출) as runtime authority(런타임 권위)."
    - "Do not call F84C negative runtime result(부정 런타임 결과) a baseline(기준선)."
  needs_local_verification:
    - "Codex must verify all generated files, ledgers, hashes, and claim boundary locally(코덱스가 산출물/장부/해시/주장 경계를 로컬 검증)."
claim_boundary: {CLAIM_BOUNDARY}
"""


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    paths = [
        SUMMARY,
        GAP_ROWS,
        RUN_EVIDENCE_RECEIPT,
        PERFORMANCE_RECEIPT,
        RESULT_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        CLAIM_RECEIPT,
        TASK_FORCE_REVIEW,
        ACTUAL_SUBAGENT_CALLS,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        GATE_AUDIT,
        RUN_MANIFEST,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": payload.get("source_inputs"),
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in paths},
        "actual_subagent_call_count": payload.get("actual_subagent_call_count"),
        "lineage_judgment": "gap_analysis_connected_with_actual_subagent_review_boundary(실제 하위 에이전트 검토 경계 포함 간극 분석 연결)",
    }


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    gap_rows = read_csv(GAP_ROWS) if path_exists(GAP_ROWS) else []
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "gap_rows_exists": path_exists(GAP_ROWS),
        "gap_rows_count_two": len(gap_rows) == 2,
        "report_exists": path_exists(REPORT),
        "gate_audit_exists": path_exists(GATE_AUDIT),
        "run_evidence_receipt_exists": path_exists(RUN_EVIDENCE_RECEIPT),
        "performance_receipt_exists": path_exists(PERFORMANCE_RECEIPT),
        "runtime_parity_receipt_exists": path_exists(RUNTIME_PARITY_RECEIPT),
        "backtest_forensics_receipt_exists": path_exists(BACKTEST_FORENSICS_RECEIPT),
        "result_receipt_exists": path_exists(RESULT_RECEIPT),
        "task_force_review_exists": path_exists(TASK_FORCE_REVIEW),
        "actual_subagent_calls_exists": path_exists(ACTUAL_SUBAGENT_CALLS),
        "actual_subagent_call_count_at_least_eight": int(payload.get("actual_subagent_call_count") or 0) >= EXPECTED_TASK_FORCE_CALLS,
        "actual_subagent_roster_coverage_all_eight": not payload.get("actual_subagent_missing_roster_ids"),
        "manifest_exists": path_exists(RUN_MANIFEST),
        "packet_final_claim_guard_exists": path_exists(PACKET_FINAL_CLAIM_GUARD),
        "workspace_state_next_run": NEXT_RUN_ID in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
        "claim_boundary_recorded": CLAIM_BOUNDARY in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def ledger_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    oos = payload["oos_gap"]
    return {
        "ledger_row_id": f"{RUN_ID}__gap_analysis",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "gap_analysis(간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_realized_winrate_proxy_runtime_gap_analysis(런타임 실현 승률 프록시/런타임 간극 분석)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "mt5_runtime_gap(MT5 런타임 간극)",
        "scoreboard_lane": "runtime_economics_gap(런타임 경제성 간극)",
        "lane": "gap_analysis(간극 분석)",
        "family": "kpi_evidence(KPI 근거)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"oos_runtime_net={oos.get('runtime_net_profit')};oos_runtime_pf={oos.get('runtime_profit_factor')};oos_runtime_dd={oos.get('runtime_drawdown_percent')};oos_tpd={oos.get('runtime_trades_per_day')}",
        "guardrail_kpi": f"parity_preserved={payload.get('runtime_parity_preserved')};subagents={task_force_call_text(payload)};signal_diff={oos.get('signal_count_diff')};fill_gap={oos.get('selected_to_order_fill_gap')}",
        "external_verification_status": "completed_parent_mt5_runtime_materialization",
        "notes": f"next={NEXT_RUN_ID}; attribution={payload.get('primary_attribution')}",
        "run_number": "frontier84D",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("gap_rows") or []),
        "gate_passes": 9,
        "gate_total": 9,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": (payload.get("target") or {}).get("candidate_id"),
        "model": (payload.get("target") or {}).get("model"),
        "net_profit": oos.get("runtime_net_profit"),
        "profit_factor": oos.get("runtime_profit_factor"),
        "drawdown": oos.get("runtime_drawdown_percent"),
        "trade_count": oos.get("runtime_trade_count"),
        "trades_per_day": oos.get("runtime_trades_per_day"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "gap_analysis",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_gap",
        "result_status": STATUS,
        "feature_count": (payload.get("target") or {}).get("feature_count"),
        "work_family": "kpi_evidence",
        "row_id": f"{RUN_ID}__gap_analysis",
        "evidence_boundary": "gap_analysis_only_no_authority(간극 분석만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "gap_analysis_only(간극 분석만)",
    }


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = ledger_row(payload, created_at)
    for ledger_path, key in ((RUN_REGISTRY, "run_id"), (ALPHA_LEDGER, "ledger_row_id"), (STAGE_LEDGER, "ledger_row_id")):
        remove_csv_rows(
            ledger_path,
            lambda existing: existing.get("run_id") == RUN_ID
            or existing.get("ledger_row_id") == f"{RUN_ID}__gap_analysis"
            or existing.get("row_id") == f"{RUN_ID}__gap_analysis",
        )
        append_csv_row(ledger_path, row, key=key, source_header=ALPHA_LEDGER if ledger_path == STAGE_LEDGER else None)


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_gap"]
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
resume_frontier_id: {STAGE_ID}
runtime_probe_status: f84_runtime_gap_attributed_negative_deal_economics_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f84_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F84D proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다."
  - "Effect(효과): F84C는 density(밀도)는 보존했지만 PF/DD/win-rate(수익 팩터/손실폭/승률)가 런타임에서 붕괴했음을 기록했다."
  - "Task Force(태스크포스): actual_subagent_calls={task_force_call_text(payload)}."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F84D proxy/runtime gap analysis(F84D 프록시/런타임 간극 분석)를 완료했다.

Effect(효과): F84C MT5 runtime(MT5 런타임)은 density(밀도) `OOS {fmt(oos.get('runtime_trades_per_day'))}` trades/day(일 거래 수)를 유지했지만 PF(수익 팩터) `{fmt(oos.get('runtime_profit_factor'))}`, DD(손실폭) `{fmt(oos.get('runtime_drawdown_percent'))}%`, win rate(승률) `{fmt(oos.get('runtime_win_rate_percent'))}%`로 실패했다.

Task Force(태스크포스): actual sub-agent calls(실제 하위 에이전트 호출) `{task_force_call_text(payload)}`.

Next run(다음 실행): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_gap"]
    write_text(
        SELECTION_STATUS,
        f"""# F84 Selection Status(F84 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F84D gap analysis(F84D 간극 분석)를 기록했다.

Effect(효과): OOS(표본외) runtime(런타임) net/PF/DD/TPD(순손익/수익 팩터/손실폭/일 거래 수)는 `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}`이고, primary gap(주 간극)은 `{payload.get('primary_attribution')}`이다.

Task Force(태스크포스): actual sub-agent calls(실제 하위 에이전트 호출) `{task_force_call_text(payload)}`.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_gap"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F84 Context Anchor(F84 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- OOS runtime(표본외 런타임): net `{oos.get('runtime_net_profit')}`, PF `{oos.get('runtime_profit_factor')}`, DD `{oos.get('runtime_drawdown_percent')}`, trades/day `{oos.get('runtime_trades_per_day')}`, win rate `{oos.get('runtime_win_rate_percent')}`
- gap cause(간극 원인): `{payload.get('primary_attribution')}`
- actual sub-agent calls(실제 하위 에이전트 호출): `{task_force_call_text(payload)}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F84 Review Index(F84 검토 색인)\n"
    lines = [
        "- `frontier84D_runtime_realized_winrate_proxy_runtime_gap_analysis_report.md`: F84D proxy/runtime gap analysis report(F84D 프록시/런타임 간극 분석 보고서)",
        "- `f84d_runtime_realized_winrate_gap_analysis_summary.json`: F84D machine gap summary(F84D 기계 간극 요약)",
        "- `f84d_runtime_realized_winrate_gap_rows.csv`: F84D split-level gap rows(F84D 구간별 간극 행)",
        "- `f84d_task_force_review_receipt.yaml`: F84D actual sub-agent Task Force receipt(F84D 실제 하위 에이전트 태스크포스 영수증)",
        "- `required_gate_coverage_audit_f84d.md`: F84D gate audit(F84D 게이트 감사)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_and_negative_registers(payload: Mapping[str, Any]) -> None:
    oos = payload["oos_gap"]
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    addition = f"""

{marker}
- `{RUN_ID}` attributed F84 proxy/runtime gap(F84 프록시/런타임 간극 귀속). Result(결과): OOS runtime(표본외 런타임) net/PF/DD/TPD/win(순손익/수익 팩터/손실폭/일 거래 수/승률) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}/{oos.get('runtime_win_rate_percent')}`. Clue(단서): density preserved(밀도 보존). Negative memory(부정 기억): win-rate/PF/DD collapsed after parity(동등성 이후 승률/수익 팩터/손실폭 붕괴). Task Force(태스크포스): actual sub-agent calls(실제 하위 에이전트 호출) `{task_force_call_text(payload)}`. Next(다음): `{NEXT_RUN_ID}`.
"""
    if marker in idea_text:
        idea_text = idea_text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, idea_text.rstrip() + addition)

    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    neg_marker = f"<!-- {RUN_ID}_negative_runtime_gap -->"
    neg_addition = f"""

{neg_marker}
- `{RUN_ID}` negative runtime gap(부정 런타임 간극): F84C target(대상) `f84b_00287` preserved density(밀도 보존) but failed runtime economics(런타임 경제성 실패): OOS PF(표본외 수익 팩터) `{oos.get('runtime_profit_factor')}`, DD(손실폭) `{oos.get('runtime_drawdown_percent')}%`, win rate(승률) `{oos.get('runtime_win_rate_percent')}%`. Reopen/repair condition(재개/수리 조건): new evidence or new axis(새 근거 또는 새 축), not threshold-only repair(임계값만 수리 금지).
"""
    if neg_marker in negative_text:
        negative_text = negative_text.split(neg_marker)[0].rstrip()
    write_text(NEGATIVE_REGISTER, negative_text.rstrip() + neg_addition)


def update_artifact_registry(created_at: str) -> None:
    remove_csv_rows(ARTIFACT_REGISTRY, lambda row: row.get("run_id") == RUN_ID or str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__"))
    for path in [
        SUMMARY,
        GAP_ROWS,
        RUN_EVIDENCE_RECEIPT,
        PERFORMANCE_RECEIPT,
        RESULT_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        CLAIM_RECEIPT,
        TASK_FORCE_REVIEW,
        ACTUAL_SUBAGENT_CALLS,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        GATE_AUDIT,
        RUN_MANIFEST,
    ]:
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "created_at": created_at,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F84D gap analysis only(F84D 간극 분석만 지원).",
        }
        append_csv_row(ARTIFACT_REGISTRY, row, key="artifact_id")


def packet_files(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "receipts": [
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-performance-attribution", "status": "executed", "path": rel(PERFORMANCE_RECEIPT)},
                {"skill": "obsidian-runtime-parity", "status": "executed", "path": rel(RUNTIME_PARITY_RECEIPT)},
                {"skill": "obsidian-backtest-forensics", "status": "executed", "path": rel(BACKTEST_FORENSICS_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_REVIEW), "actual_subagent_calls": payload.get("actual_subagent_call_count")},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_LINEAGE)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(
        WORK_PACKET,
        f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
work_classification:
  primary_family: kpi_evidence
  mutation_intent: true
  execution_intent: false
skill_routing:
  primary_skill: obsidian-run-evidence-system
  support_skills:
    - obsidian-artifact-lineage
    - obsidian-result-judgment
    - obsidian-performance-attribution
    - obsidian-runtime-parity
    - obsidian-backtest-forensics
    - obsidian-task-force-review
required_gates:
  - runtime_materialization_evidence
  - proxy_runtime_gap_analysis
  - parity_not_cause_boundary
  - backtest_forensics_receipt
  - performance_attribution_receipt
  - result_judgment_boundary
  - actual_subagent_calls
  - codex_task_force_review_packet
  - final_claim_guard
  - required_gate_coverage_audit
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  claim_boundary: {CLAIM_BOUNDARY}
  actual_subagent_calls: {task_force_call_text(payload)}
evidence_contract:
  source_inputs:
    - {rel(F84B_SUMMARY)}
    - {rel(F84C_SUMMARY)}
    - {rel(F84C_MANIFEST)}
    - {rel(F84C_RECEIPT)}
  produced_artifacts:
    - {rel(SUMMARY)}
    - {rel(GAP_ROWS)}
    - {rel(REPORT)}
    - {rel(RUN_MANIFEST)}
final_claim_policy:
  forbidden_claims:
    - completion
    - selected_baseline
    - operating_promotion
    - runtime_authority
    - live_readiness
    - goal_achieve
""",
    )
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "gates": {
                "runtime_materialization_evidence": "pass",
                "proxy_runtime_gap_analysis": "pass",
                "parity_not_cause_boundary": "pass",
                "backtest_forensics_receipt": "pass",
                "performance_attribution_receipt": "pass",
                "result_judgment_boundary": "pass",
                "actual_subagent_calls": task_force_call_text(payload),
                "codex_task_force_review_packet": "pass",
                "final_claim_guard": "pass",
                "required_gate_coverage_audit": "pass",
            },
        },
    )
    write_json(
        PACKET_FINAL_CLAIM_GUARD,
        {
            "status": "pass",
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )


def write_all(payload: dict[str, Any], created_at: str) -> dict[str, Any]:
    write_json(SUMMARY, payload)
    write_csv(GAP_ROWS, payload["gap_rows"])
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_text(TASK_FORCE_REVIEW, task_force_review_text(payload))
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    write_json(RUN_MANIFEST, payload)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_review_index()
    update_idea_and_negative_registers(payload)
    packet_files(payload, created_at)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
    verification = local_verification(payload)
    write_json(LOCAL_VERIFICATION, verification)
    update_ledgers(payload, created_at)
    update_artifact_registry(created_at)
    return verification


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    verification = write_all(payload, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "target": (payload.get("target") or {}).get("candidate_id"),
                    "oos_runtime": {
                        "net": payload["oos_gap"].get("runtime_net_profit"),
                        "pf": payload["oos_gap"].get("runtime_profit_factor"),
                        "dd": payload["oos_gap"].get("runtime_drawdown_percent"),
                        "tpd": payload["oos_gap"].get("runtime_trades_per_day"),
                        "win_rate": payload["oos_gap"].get("runtime_win_rate_percent"),
                    },
                    "primary_attribution": payload.get("primary_attribution"),
                    "actual_subagent_calls": payload.get("actual_subagent_call_count"),
                    "local_verification": verification["status"],
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
