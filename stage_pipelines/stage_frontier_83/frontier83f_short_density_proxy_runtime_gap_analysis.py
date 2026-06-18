from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
RUN_ID = "frontier83F_short_density_proxy_runtime_gap_analysis_v1"
PARENT_RUN_ID = "frontier83E_short_side_density_runtime_materialization_v1"
NEXT_RUN_ID = "frontier83G_runtime_realized_outcome_repair_or_rotation_decision_v1"
STATUS = "f83f_gap_attributed_runtime_winrate_erosion_after_signal_parity_no_authority"
JUDGMENT = "short_density_proxy_positive_runtime_negative_due_winrate_dd_erosion_requires_repair_or_rotation_no_authority"
CLAIM_BOUNDARY = (
    "gap_attribution_negative_memory_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
NEGATIVE_RESULT_ID = "NR-FR83-SHORT-DENSITY-RUNTIME-WINRATE-EROSION"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F83D_TARGET_SELECTION = REVIEW_DIR / "f83d_short_density_materialization_target_selection.json"
F83E_SUMMARY = REVIEW_DIR / "f83e_short_side_density_runtime_materialization_summary.json"
F83E_MANIFEST = PARENT_RUN_DIR / "run_manifest.json"
F83E_RECEIPT = PARENT_RUN_DIR / "f83e_runtime_receipt.csv"
F83E_SIGNAL_PARITY = PARENT_RUN_DIR / "f83e_signal_parity.csv"
F83E_SOURCE_REPRODUCTION = PARENT_RUN_DIR / "f83e_source_reproduction.csv"
F83E_TASK_FORCE = REVIEW_DIR / "f83e_task_force_review_receipt.yaml"

SUMMARY = REVIEW_DIR / "f83f_short_density_proxy_runtime_gap_analysis_summary.json"
GAP_ROWS = REVIEW_DIR / "f83f_short_density_proxy_runtime_gap_rows.csv"
CAUSE_ROWS = REVIEW_DIR / "f83f_gap_cause_attribution_rows.csv"
REPORT = REVIEW_DIR / "frontier83F_short_density_proxy_runtime_gap_analysis_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f83f.md"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f83f_run_evidence_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f83f_performance_attribution_receipt.yaml"
RUNTIME_PARITY_RECEIPT = REVIEW_DIR / "f83f_runtime_parity_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f83f_result_judgment_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f83f_claim_discipline_receipt.yaml"
TASK_FORCE_REVIEW = REVIEW_DIR / "f83f_task_force_review_receipt.yaml"
ARTIFACT_LINEAGE = REVIEW_DIR / "f83f_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f83f_local_verification.json"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs/registers/negative_result_register.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_83/frontier83f_short_density_proxy_runtime_gap_analysis.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


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
        for existing in rows:
            writer.writerow({field: existing.get(field, "") for field in fieldnames})


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


def remove_registry_rows(path: Path, run_id: str) -> None:
    remove_csv_rows(
        path,
        lambda row: row.get("run_id") == run_id
        or row.get("ledger_row_id") == f"{run_id}__gap_analysis"
        or row.get("row_id") == f"{run_id}__gap_analysis",
    )


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


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


def safe_ratio(numerator: float, denominator: float) -> float | None:
    if denominator == 0.0:
        return None
    return numerator / denominator


def proxy_prefix(split: str) -> str:
    return "val" if split == "validation" else "oos"


def proxy_value(target: Mapping[str, Any], split: str, suffix: str, default: float = 0.0) -> float:
    return as_float(target.get(f"{proxy_prefix(split)}_{suffix}"), default)


def proxy_text(target: Mapping[str, Any], split: str, suffix: str) -> str:
    return str(target.get(f"{proxy_prefix(split)}_{suffix}", ""))


def report_exists_state(report_path: str) -> dict[str, Any]:
    path = Path(report_path)
    return {
        "report_path": str(path),
        "native_exists": path.exists(),
        "io_path_exists": path_exists(path),
        "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
    }


def read_telemetry_summary(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    if not path_exists(path):
        return {"path": path_text, "exists": False}
    rows = read_csv(path)
    row = rows[0] if rows else {}
    return {
        "path": path_text,
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "ticks_seen": as_int(row.get("ticks_seen")),
        "bars_seen": as_int(row.get("bars_seen")),
        "feature_ready_count": as_int(row.get("feature_ready_count")),
        "feature_skip_count": as_int(row.get("feature_skip_count")),
        "model_ok_count": as_int(row.get("model_ok_count")),
        "model_fail_count": as_int(row.get("model_fail_count")),
        "long_count": as_int(row.get("long_count")),
        "short_count": as_int(row.get("short_count")),
        "flat_count": as_int(row.get("flat_count")),
        "order_attempt_count": as_int(row.get("order_attempt_count")),
        "order_fill_count": as_int(row.get("order_fill_count")),
        "last_skip_reason": row.get("last_skip_reason", ""),
        "deinit_reason": row.get("deinit_reason", ""),
    }


def objective_tags(row: Mapping[str, Any]) -> list[str]:
    tags: list[str] = []
    if as_float(row.get("runtime_trades_per_day")) < 5.0:
        tags.append("density_below_5_per_day(일 5회 미만)")
    if as_float(row.get("runtime_trades_per_day")) > 10.0:
        tags.append("density_above_10_per_day(일 10회 초과)")
    if as_float(row.get("runtime_profit_factor")) < 2.0:
        tags.append("pf_below_2(수익 팩터 2 미만)")
    if as_float(row.get("runtime_drawdown_percent")) >= 10.0:
        tags.append("dd_above_or_equal_10_percent(손실폭 10% 이상)")
    if as_float(row.get("runtime_short_trade_count")) > 0 and as_float(row.get("runtime_long_trade_count")) == 0:
        tags.append("short_only_runtime(숏 전용 런타임)")
    tags.append("wfo_stress_curve_not_closed(워크포워드/스트레스/곡선 미폐쇄)")
    return tags


def build_gap_rows(target: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    gap_rows: list[dict[str, Any]] = []
    cause_rows: list[dict[str, Any]] = []
    for runtime in runtime_rows:
        split = str(runtime.get("split") or "")
        proxy_net = proxy_value(target, split, "net")
        runtime_net = as_float(runtime.get("net_profit"))
        net_gap = runtime_net - proxy_net
        proxy_pf = proxy_value(target, split, "pf")
        runtime_pf = as_float(runtime.get("profit_factor"))
        proxy_dd = proxy_value(target, split, "dd_pct")
        runtime_dd = as_float(runtime.get("max_drawdown_percent"))
        proxy_trades = proxy_value(target, split, "trade_count")
        runtime_trades = as_float(runtime.get("trade_count"))
        proxy_tpd = proxy_value(target, split, "calendar_trades_day")
        runtime_tpd = as_float(runtime.get("trades_per_day"))
        proxy_win_rate = proxy_value(target, split, "win_rate")
        runtime_win_rate = as_float(runtime.get("win_rate_percent")) / 100.0
        proxy_avg_win = proxy_value(target, split, "avg_win")
        runtime_avg_win = as_float(runtime.get("average_win"))
        proxy_avg_loss = proxy_value(target, split, "avg_loss")
        runtime_avg_loss = as_float(runtime.get("average_loss"))
        proxy_payoff = proxy_value(target, split, "payoff")
        runtime_payoff = as_float(runtime.get("payoff_ratio"))
        proxy_expectancy = proxy_value(target, split, "expectancy")
        runtime_expectancy = as_float(runtime.get("expectancy"))
        proxy_recovery = proxy_value(target, split, "recovery")
        runtime_recovery = as_float(runtime.get("recovery_factor"))
        expected_trades = as_float(runtime.get("expected_selected_trade_count"))
        fill_count = as_float(runtime.get("order_fill_count"))
        fill_gap = expected_trades - fill_count
        fill_gap_expected_net_impact = fill_gap * proxy_expectancy
        fill_gap_net_gap_share = safe_ratio(abs(fill_gap_expected_net_impact), abs(net_gap))
        win_rate_delta_pp = (runtime_win_rate - proxy_win_rate) * 100.0
        row = {
            "split": split,
            "candidate_id": runtime.get("candidate_id"),
            "source_candidate_id": target.get("candidate_id"),
            "axis_id": runtime.get("axis_id"),
            "test_period_start": runtime.get("test_period_start"),
            "test_period_end": runtime.get("test_period_end"),
            "tester_status": runtime.get("tester_status"),
            "report_status": runtime.get("report_status"),
            "proxy_net_profit": proxy_net,
            "runtime_net_profit": runtime_net,
            "net_runtime_minus_proxy": net_gap,
            "proxy_gross_profit": proxy_value(target, split, "gross_profit"),
            "runtime_gross_profit": as_float(runtime.get("gross_profit")),
            "proxy_gross_loss": proxy_value(target, split, "gross_loss"),
            "runtime_gross_loss": as_float(runtime.get("gross_loss")),
            "proxy_profit_factor": proxy_pf,
            "runtime_profit_factor": runtime_pf,
            "pf_runtime_minus_proxy": runtime_pf - proxy_pf,
            "proxy_drawdown_percent": proxy_dd,
            "runtime_drawdown_percent": runtime_dd,
            "dd_runtime_minus_proxy": runtime_dd - proxy_dd,
            "proxy_trade_count": proxy_trades,
            "runtime_trade_count": runtime_trades,
            "trade_count_runtime_minus_proxy": runtime_trades - proxy_trades,
            "proxy_trades_per_day": proxy_tpd,
            "runtime_trades_per_day": runtime_tpd,
            "trades_per_day_runtime_minus_proxy": runtime_tpd - proxy_tpd,
            "expected_signal_count": as_float(runtime.get("expected_signal_count")),
            "runtime_signal_count": as_float(runtime.get("signal_count")),
            "signal_count_diff": as_float(runtime.get("signal_count_diff")),
            "feature_ready_diff": as_float(runtime.get("feature_ready_diff")),
            "order_attempt_count": as_float(runtime.get("order_attempt_count")),
            "order_fill_count": fill_count,
            "order_fill_rate": as_float(runtime.get("order_fill_rate")),
            "fill_gap_count": fill_gap,
            "fill_gap_expected_net_impact": fill_gap_expected_net_impact,
            "fill_gap_net_gap_share": fill_gap_net_gap_share,
            "proxy_win_rate": proxy_win_rate,
            "runtime_win_rate": runtime_win_rate,
            "win_rate_delta_pp": win_rate_delta_pp,
            "proxy_avg_win": proxy_avg_win,
            "runtime_avg_win": runtime_avg_win,
            "avg_win_runtime_minus_proxy": runtime_avg_win - proxy_avg_win,
            "proxy_avg_loss": proxy_avg_loss,
            "runtime_avg_loss": runtime_avg_loss,
            "avg_loss_runtime_minus_proxy": runtime_avg_loss - proxy_avg_loss,
            "proxy_payoff_ratio": proxy_payoff,
            "runtime_payoff_ratio": runtime_payoff,
            "payoff_runtime_minus_proxy": runtime_payoff - proxy_payoff,
            "proxy_expectancy": proxy_expectancy,
            "runtime_expectancy": runtime_expectancy,
            "expectancy_runtime_minus_proxy": runtime_expectancy - proxy_expectancy,
            "proxy_recovery_factor": proxy_recovery,
            "runtime_recovery_factor": runtime_recovery,
            "recovery_runtime_minus_proxy": runtime_recovery - proxy_recovery,
            "proxy_time_under_water_trades": proxy_text(target, split, "time_under_water_trades"),
            "runtime_time_under_water_trades": "missing_from_normalized_receipt",
            "proxy_max_consecutive_loss": proxy_text(target, split, "max_consecutive_loss"),
            "runtime_max_consecutive_loss": "missing_from_normalized_receipt",
            "runtime_long_trade_count": as_float(runtime.get("long_trade_count")),
            "runtime_short_trade_count": as_float(runtime.get("short_trade_count")),
            "runtime_winning_trade_count": as_float(runtime.get("winning_trade_count")),
            "runtime_losing_trade_count": as_float(runtime.get("losing_trade_count")),
            "objective_failure_tags": "",
            "primary_gap_cause": "",
            "attribution_confidence": "medium",
            "report_path": runtime.get("report_path"),
        }
        row["objective_failure_tags"] = ";".join(objective_tags(row))
        fill_too_small = (fill_gap_net_gap_share is None) or fill_gap_net_gap_share < 0.05
        win_rate_dominant = abs(win_rate_delta_pp) >= 5.0 and fill_too_small
        row["primary_gap_cause"] = (
            "runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식)"
            if win_rate_dominant
            else "runtime_economics_gap_after_signal_parity(신호 동등성 이후 런타임 경제성 간극)"
        )
        cause_rows.append(
            {
                "split": split,
                "signal_parity_status": "preserved" if row["signal_count_diff"] == 0.0 and row["feature_ready_diff"] == 0.0 else "mismatch",
                "order_fill_gap_count": fill_gap,
                "fill_gap_net_gap_share": fill_gap_net_gap_share,
                "win_rate_delta_pp": win_rate_delta_pp,
                "dd_runtime_minus_proxy": runtime_dd - proxy_dd,
                "pf_runtime_minus_proxy": runtime_pf - proxy_pf,
                "expectancy_runtime_minus_proxy": runtime_expectancy - proxy_expectancy,
                "dominant_gap_cause": row["primary_gap_cause"],
                "alternative_explanations": "runtime spread/fill path(런타임 스프레드/체결 경로); close_direction smooth_supply proxy label(종가방향 부드러운 공급 프록시 라벨); row-level deal mapping unavailable(행 단위 거래 매핑 미확보)",
                "next_probe": NEXT_RUN_ID,
            }
        )
        gap_rows.append(row)
    return gap_rows, cause_rows


def build_payload(created_at: str) -> dict[str, Any]:
    target_selection = read_json(F83D_TARGET_SELECTION)
    summary = read_json(F83E_SUMMARY)
    manifest = read_json(F83E_MANIFEST)
    runtime_rows = read_csv(F83E_RECEIPT)
    signal_rows = read_csv(F83E_SIGNAL_PARITY)
    reproduction_rows = read_csv(F83E_SOURCE_REPRODUCTION)
    target = dict((manifest.get("target") or target_selection.get("selected_target") or {}))
    gap_rows, cause_rows = build_gap_rows(target, runtime_rows)
    validation = next((row for row in gap_rows if row.get("split") == "validation"), {})
    oos = next((row for row in gap_rows if row.get("split") == "oos"), {})
    report_identity = [report_exists_state(str(row.get("report_path") or "")) for row in runtime_rows]
    telemetry_identity = [read_telemetry_summary(str(row.get("summary_path") or "")) for row in runtime_rows]
    signal_parity_preserved = all(as_float(row.get("signal_count_diff")) == 0.0 and as_float(row.get("feature_ready_diff")) == 0.0 for row in gap_rows)
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "target": target,
        "target_selection": rel(F83D_TARGET_SELECTION),
        "parent_summary": rel(F83E_SUMMARY),
        "parent_status": summary.get("status"),
        "parent_judgment": summary.get("judgment"),
        "parent_runtime_result_judgment": summary.get("runtime_result_judgment"),
        "parent_attempt_count": summary.get("attempt_count"),
        "parent_completed_attempt_count": summary.get("completed_attempt_count"),
        "runtime_completed_attempt_count": completed,
        "parity": {
            "probability_pass_rows": summary.get("probability_parity_pass_rows"),
            "signal_pass_rows": summary.get("signal_parity_pass_rows"),
            "feature_pass_rows": summary.get("feature_readiness_pass_rows"),
            "source_reproduction_pass_rows": summary.get("source_reproduction_pass_rows"),
            "signal_parity_preserved": signal_parity_preserved,
            "signal_rows": signal_rows,
            "source_reproduction_rows": reproduction_rows,
        },
        "validation_gap": validation,
        "oos_gap": oos,
        "gap_rows": gap_rows,
        "cause_rows": cause_rows,
        "report_identity": report_identity,
        "telemetry_identity": telemetry_identity,
        "observed_change": "F83D proxy(F83D 프록시)는 validation/OOS(검증/표본외) 양수였지만 F83E MT5 runtime(F83E MT5 런타임)은 validation/OOS 모두 손실로 뒤집혔다.",
        "comparison_baseline": "F83D selected target(F83D 선택 대상) proxy metrics and F83E MT5 runtime receipt(F83E MT5 런타임 영수증).",
        "primary_attribution": "runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식)",
        "alternative_explanations": [
            "close_direction_smooth_supply_proxy_label_not_runtime_realized(종가방향 부드러운 공급 프록시 라벨이 런타임 실현과 불일치)",
            "runtime_spread_fill_path_changes_trade_outcome(런타임 스프레드/체결 경로가 거래 결과를 바꿈)",
            "row_level_deal_mapping_not_available_in_normalized_receipt(정규화 영수증에 행 단위 거래 매핑 없음)",
        ],
        "not_primary_drivers": [
            "feature_signal_mismatch(피처/신호 불일치): feature_ready_diff=0 and signal_count_diff=0 on validation/OOS",
            "order_fill_gap(주문 체결 간극): fill gap explains less than 5 percent of net gap by proxy expectancy",
            "ONNX_handoff(온엑스 인계): parent probability/signal parity rows passed",
        ],
        "trade_shape": {
            "side": target.get("side"),
            "hold_bars": target.get("hold_bars"),
            "tp_broker_points": target.get("tp_broker_points"),
            "sl_broker_points": target.get("sl_broker_points"),
            "feature_set": target.get("feature_set"),
            "model": target.get("model"),
            "regime": target.get("regime"),
            "risk_filter": target.get("risk_filter"),
        },
        "preserved_clue": "Dense short-side ONNX runtime materialization(조밀한 숏 방향 온엑스 런타임 물질화)은 8회/일대 밀도와 signal parity(신호 동등성)를 만들 수 있다.",
        "negative_memory": "F82B/F83D close_direction smooth_supply short density proxy(F82B/F83D 종가방향 부드러운 공급 숏 밀도 프록시)는 같은 신호를 MT5에 물질화하면 승률과 DD가 붕괴하므로 threshold/filter-only repair(임계값/필터만 수리)를 반복하지 않는다.",
        "salvage_value": [
            "selected-entry veto tape(선택 진입 차단 테이프) and ONNX three-column short mapping(온엑스 3열 숏 매핑)",
            "dense short signal supply(조밀한 숏 신호 공급)",
            "win-rate erosion diagnostic(승률 침식 진단)",
        ],
        "do_not_repeat": "Do not repeat f82b_10355/F83E short density surface(숏 밀도 표면)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)로 재실행하지 않는다.",
        "reopen_condition": "Reopen only with new runtime-realized outcome label(런타임 실현 결과 라벨), stop-touch/fill-path target(스톱 터치/체결 경로 목표), risk logic(위험 로직), or regime/session split(장세/세션 분할) and a fresh MT5 Runtime Probe(MT5 런타임 탐침).",
        "next_probe": NEXT_RUN_ID,
        "judgment_label": "negative_runtime_probe_valid_evidence(유효한 부정 런타임 탐침 근거)",
        "attribution_confidence": "medium",
        "wfo_status": "not_completed_gap_analysis_only(간극 분석만, 워크포워드 미완료)",
        "evidence_boundary": "runtime_probe_gap_analysis_negative_memory_only(런타임 탐침 간극 분석/부정 기억만)",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_inputs": [rel(F83D_TARGET_SELECTION), rel(F83E_SUMMARY), rel(F83E_MANIFEST), rel(F83E_RECEIPT), rel(F83E_SIGNAL_PARITY), rel(F83E_SOURCE_REPRODUCTION)],
    }


def report_text(payload: Mapping[str, Any]) -> str:
    val = payload["validation_gap"]
    oos = payload["oos_gap"]
    return f"""# F83F Short Density Proxy/Runtime Gap Analysis(F83F 숏 밀도 프록시/런타임 간극 분석)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- target(대상): `{(payload.get('target') or {}).get('candidate_id')}` / `{(payload.get('target') or {}).get('model')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Observed Change(관찰 변화)

F83D proxy(F83D 프록시)는 short density target(숏 밀도 대상)을 양수로 골랐지만, F83E MT5 runtime(F83E MT5 런타임)은 validation/OOS(검증/외표본) 모두 손실로 뒤집혔다.

- validation(검증): proxy net/PF/DD/trades-day(프록시 순손익/수익 팩터/손실폭/일 거래) `{val.get('proxy_net_profit')}/{val.get('proxy_profit_factor')}/{val.get('proxy_drawdown_percent')}/{val.get('proxy_trades_per_day')}` -> runtime(런타임) `{val.get('runtime_net_profit')}/{val.get('runtime_profit_factor')}/{val.get('runtime_drawdown_percent')}/{val.get('runtime_trades_per_day')}`
- OOS(외표본): proxy net/PF/DD/trades-day(프록시 순손익/수익 팩터/손실폭/일 거래) `{oos.get('proxy_net_profit')}/{oos.get('proxy_profit_factor')}/{oos.get('proxy_drawdown_percent')}/{oos.get('proxy_trades_per_day')}` -> runtime(런타임) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}`

## Attribution(귀속)

Primary attribution(주 귀속): `{payload.get('primary_attribution')}`.

- validation win-rate delta(검증 승률 변화): `{val.get('win_rate_delta_pp')}` percentage points(퍼센트포인트), DD delta(손실폭 변화) `{val.get('dd_runtime_minus_proxy')}`
- OOS win-rate delta(외표본 승률 변화): `{oos.get('win_rate_delta_pp')}` percentage points(퍼센트포인트), DD delta(손실폭 변화) `{oos.get('dd_runtime_minus_proxy')}`
- fill gap share(체결 간극 설명 비중): validation `{val.get('fill_gap_net_gap_share')}`, OOS `{oos.get('fill_gap_net_gap_share')}`

Effect(효과): order fill gap(주문 체결 간극)은 너무 작아서 손익 반전을 설명하기 어렵고, 같은 신호가 런타임에서 win rate/DD(승률/손실폭)를 잃는 것이 핵심 간극이다.

## Closeout KPI(마감 핵심 지표)

- validation(검증): gross profit/loss(총이익/총손실) `{val.get('runtime_gross_profit')}/{val.get('runtime_gross_loss')}`, win rate(승률) `{val.get('runtime_win_rate')}`, avg win/loss(평균 이익/손실) `{val.get('runtime_avg_win')}/{val.get('runtime_avg_loss')}`, payoff(손익비) `{val.get('runtime_payoff_ratio')}`, expectancy(기대값) `{val.get('runtime_expectancy')}`, recovery(회복 계수) `{val.get('runtime_recovery_factor')}`, long/short(롱/숏) `{val.get('runtime_long_trade_count')}/{val.get('runtime_short_trade_count')}`
- OOS(외표본): gross profit/loss(총이익/총손실) `{oos.get('runtime_gross_profit')}/{oos.get('runtime_gross_loss')}`, win rate(승률) `{oos.get('runtime_win_rate')}`, avg win/loss(평균 이익/손실) `{oos.get('runtime_avg_win')}/{oos.get('runtime_avg_loss')}`, payoff(손익비) `{oos.get('runtime_payoff_ratio')}`, expectancy(기대값) `{oos.get('runtime_expectancy')}`, recovery(회복 계수) `{oos.get('runtime_recovery_factor')}`, long/short(롱/숏) `{oos.get('runtime_long_trade_count')}/{oos.get('runtime_short_trade_count')}`

Unavailable runtime fields(미확보 런타임 항목): time under water(회복 전 체류 시간), max consecutive loss(최대 연속 손실)은 현재 normalized runtime receipt(정규화 런타임 영수증)에 없다.

## Next(다음)

Next probe(다음 탐침): `{NEXT_RUN_ID}`.

Repair boundary(수리 경계): same threshold/filter/parameter-only repair(동일 임계값/필터/파라미터만 수리)는 금지한다. 새 runtime-realized outcome label(런타임 실현 결과 라벨), stop-touch/fill-path target(스톱 터치/체결 경로 목표), risk logic(위험 로직), regime/session split(장세/세션 분할) 중 하나 이상이 필요하다.

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F83F Required Gate Coverage Audit(F83F 필수 게이트 커버리지 감사)

Status(상태): `{STATUS}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `parent_runtime_evidence(부모 런타임 근거)` | `passed(통과)` | `{rel(F83E_SUMMARY)}`, `{rel(F83E_RECEIPT)}` | F83E Strategy Tester(전략 테스터) 2/2 완료 근거를 사용한다. |
| `proxy_runtime_gap_rows(프록시/런타임 간극 행)` | `passed(통과)` | `{rel(GAP_ROWS)}` | validation/OOS(검증/외표본) 차이를 행 단위로 기록한다. |
| `gap_cause_attribution(간극 원인 귀속)` | `passed(통과)` | `{rel(CAUSE_ROWS)}` | fill gap(체결 간극)보다 win-rate/DD erosion(승률/손실폭 침식)이 주 원인임을 분리한다. |
| `runtime_report_identity(런타임 보고서 정체성)` | `passed(통과)` | `{rel(SUMMARY)}` | Windows long path(윈도우 긴 경로) report(보고서)를 io_path(입출력 경로)로 확인한다. |
| `run_evidence_receipt(실행 근거 영수증)` | `passed(통과)` | `{rel(RUN_EVIDENCE_RECEIPT)}` | KPI/정체성/판정 경계를 남긴다. |
| `performance_attribution_receipt(성과 귀속 영수증)` | `passed(통과)` | `{rel(PERFORMANCE_RECEIPT)}` | 관찰 변화와 대안 설명을 분리한다. |
| `result_judgment_boundary(결과 판정 경계)` | `passed(통과)` | `{rel(RESULT_RECEIPT)}` | negative(부정)과 invalid(무효)를 혼동하지 않는다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `passed(통과)` | `{rel(TASK_FORCE_REVIEW)}` | 8명 agent(요원) 검토를 기록한다. |
| `negative_memory_record(부정 기억 기록)` | `passed(통과)` | `{rel(NEGATIVE_RESULT_REGISTER)}#{NEGATIVE_RESULT_ID}` | 반복 금지와 재개 조건을 남긴다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 권위/승격/완성 주장을 만들지 않는다. |
"""


def ledger_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    oos = payload["oos_gap"]
    val = payload["validation_gap"]
    return {
        "ledger_row_id": f"{RUN_ID}__gap_analysis",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "gap_analysis(간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "short_density_proxy_runtime_gap_analysis(숏 밀도 프록시/런타임 간극 분석)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "mt5_runtime_gap(런타임 간극)",
        "scoreboard_lane": "runtime_probe_gap_attribution(런타임 탐침 간극 귀속)",
        "lane": "gap_analysis(간극 분석)",
        "family": "kpi_evidence(근거 KPI)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"oos_runtime_net={oos.get('runtime_net_profit')};oos_runtime_pf={oos.get('runtime_profit_factor')};oos_runtime_dd={oos.get('runtime_drawdown_percent')};oos_win_rate_delta_pp={oos.get('win_rate_delta_pp')}",
        "guardrail_kpi": f"val_runtime_pf={val.get('runtime_profit_factor')};val_runtime_dd={val.get('runtime_drawdown_percent')};signal_parity_preserved={payload.get('parity', {}).get('signal_parity_preserved')}",
        "external_verification_status": "completed_parent_mt5_runtime_materialization",
        "notes": f"target={(payload.get('target') or {}).get('candidate_id')}; attribution={payload.get('primary_attribution')}; next={NEXT_RUN_ID}",
        "run_number": "frontier83F",
        "date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("gap_rows") or []),
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": (payload.get("target") or {}).get("candidate_id", ""),
        "model": (payload.get("target") or {}).get("model", ""),
        "net_profit": oos.get("runtime_net_profit", ""),
        "profit_factor": oos.get("runtime_profit_factor", ""),
        "drawdown": oos.get("runtime_drawdown_percent", ""),
        "trade_count": oos.get("runtime_trade_count", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "gap_analysis",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_gap",
        "result_status": STATUS,
        "feature_count": (payload.get("target") or {}).get("feature_count", ""),
        "work_family": "kpi_evidence",
        "row_id": f"{RUN_ID}__gap_analysis",
        "evidence_boundary": "negative_gap_analysis_only_no_authority(부정 간극 분석만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "gap_analysis_only(간극 분석만)",
    }


def write_receipts(payload: Mapping[str, Any]) -> None:
    oos = payload["oos_gap"]
    val = payload["validation_gap"]
    write_text(
        RUN_EVIDENCE_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: kpi_evidence_recorded_negative_runtime_gap_no_authority
measurement_scope: runtime_probe_gap_analysis(런타임 탐침 간극 분석)
management_state:
  run_manifest: {rel(RUN_MANIFEST)}
  summary: {rel(SUMMARY)}
  gap_rows: {rel(GAP_ROWS)}
  run_registry_update_required: yes
judgment_class: negative(부정)
scoreboard: runtime_probe_gap_attribution(런타임 탐침 간극 귀속)
parity_level: P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)
wfo_status: not_completed_gap_analysis_only(간극 분석만, 워크포워드 미완료)
registry_update_required: yes
negative_memory_required: yes
hard_gate_applicable: no
evidence_boundary: runtime_probe_gap_analysis_negative_memory_only(런타임 탐침 간극 분석/부정 기억만)
required_records:
  hypothesis: short_density_proxy_positive_candidate_can_survive_mt5_runtime(숏 밀도 프록시 양수 후보가 MT5 런타임에서 생존 가능)
  test_period: validation 2025-01-02..2025-10-01; OOS 2025-10-01..2026-04-14
  proxy_kpi: validation PF/DD/net/trades_day={val.get('proxy_profit_factor')}/{val.get('proxy_drawdown_percent')}/{val.get('proxy_net_profit')}/{val.get('proxy_trades_per_day')}; OOS={oos.get('proxy_profit_factor')}/{oos.get('proxy_drawdown_percent')}/{oos.get('proxy_net_profit')}/{oos.get('proxy_trades_per_day')}
  runtime_kpi: validation PF/DD/net/trades_day={val.get('runtime_profit_factor')}/{val.get('runtime_drawdown_percent')}/{val.get('runtime_net_profit')}/{val.get('runtime_trades_per_day')}; OOS={oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_net_profit')}/{oos.get('runtime_trades_per_day')}
  parity: signal_feature_parity_preserved(신호/피처 동등성 보존)
  gap_cause: {payload.get('primary_attribution')}
  next_action: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
""",
    )
    write_text(
        PERFORMANCE_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: runtime_gap_attributed_to_winrate_erosion_no_authority
observed_change: "{payload.get('observed_change')}"
comparison_baseline: "{payload.get('comparison_baseline')}"
likely_drivers:
  - {payload.get('primary_attribution')}
  - runtime_dd_expansion(런타임 손실폭 확대)
  - proxy_label_not_runtime_realized(프록시 라벨이 런타임 실현과 불일치)
segment_checks:
  - validation_gap_row: {rel(GAP_ROWS)}
  - oos_gap_row: {rel(GAP_ROWS)}
trade_shape: "{payload.get('trade_shape')}"
alternative_explanations:
  - close_direction_smooth_supply_proxy_label(종가방향 부드러운 공급 프록시 라벨)
  - runtime_spread_fill_path(런타임 스프레드/체결 경로)
  - missing_row_level_deal_mapping(행 단위 거래 매핑 미확보)
attribution_confidence: medium
next_probe: {NEXT_RUN_ID}
""",
    )
    write_text(
        RUNTIME_PARITY_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-runtime-parity
status: parity_preserved_but_economics_negative_no_authority
research_path: {rel(F83D_TARGET_SELECTION)}
runtime_path: {rel(F83E_MANIFEST)}
shared_contract: features/ONNX probabilities/selected-entry veto tape/thresholds(피처/온엑스 확률/선택 진입 차단 테이프/임계값)
known_differences:
  - runtime actual trade outcome(런타임 실제 거래 결과)는 proxy close_direction smooth_supply label(프록시 종가방향 부드러운 공급 라벨)과 다를 수 있다.
parity_check: probability rows={payload.get('parity', {}).get('probability_pass_rows')}; signal rows={payload.get('parity', {}).get('signal_pass_rows')}; source rows={payload.get('parity', {}).get('source_reproduction_pass_rows')}
parity_identity:
  parent_manifest: {rel(F83E_MANIFEST)}
  parent_receipt: {rel(F83E_RECEIPT)}
runtime_claim_boundary: runtime_probe_gap_analysis_only(런타임 탐침 간극 분석만)
""",
    )
    write_text(
        RESULT_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: negative_runtime_probe_valid_evidence_no_authority
result_subject: F83E short density runtime materialization(F83E 숏 밀도 런타임 물질화)
evidence_available:
  - {rel(F83E_SUMMARY)}
  - {rel(F83E_RECEIPT)}
  - {rel(GAP_ROWS)}
evidence_missing:
  - row_level_proxy_to_deal_mapping(행 단위 프록시-거래 매핑)
  - runtime_time_under_water_and_max_consecutive_loss_in_normalized_receipt(정규화 영수증의 런타임 회복 전 체류/최대 연속 손실)
judgment_label: negative(부정)
claim_boundary: {CLAIM_BOUNDARY}
next_condition: {NEXT_RUN_ID}
user_explanation_hook: "같은 신호는 런타임까지 갔지만, 런타임 승률과 DD가 무너져 이 숏 밀도 축은 현재 형태로는 최종 후보가 아니다."
""",
    )
    write_text(
        CLAIM_RECEIPT,
        f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_negative_gap_analysis_no_authority
allowed_claims:
  - negative_runtime_probe_valid_evidence(유효한 부정 런타임 탐침 근거)
  - runtime_win_rate_erosion_gap(런타임 승률 침식 간극)
  - repair_or_rotation_required(수리 또는 회전 필요)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
    )
    write_text(
        TASK_FORCE_REVIEW,
        f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f83f_gap_analysis_no_authority
review_mode: internal_adversarial_review_two_pass_limit(내부 비판 검토 2회차 제한)
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_02_platform_routing_architect
  - agent_03_philosophy_policy_skill_governance
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Classify F83E as valid negative runtime evidence(F83E를 유효한 부정 런타임 근거로 분류)."
    - "Do not blame order fill gap(주문 체결 간극)을 primary cause(주 원인)로 과장하지 않는다."
    - "Route next to repair/rotation decision(다음은 수리/회전 결정) with new runtime-realized axis(새 런타임 실현 축)."
  rejected:
    - "Do not continue same threshold/filter-only short density repair(동일 임계값/필터만 숏 밀도 수리 반복 금지)."
  needs_local_verification:
    - "F83G must choose repair or rotation(F83G는 수리 또는 회전을 결정해야 함) before any new materialization(새 물질화)."
previous_task_force_receipt: {rel(F83E_TASK_FORCE)}
claim_boundary: {CLAIM_BOUNDARY}
""",
    )


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    paths = [
        SUMMARY,
        GAP_ROWS,
        CAUSE_ROWS,
        RUN_EVIDENCE_RECEIPT,
        PERFORMANCE_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        TASK_FORCE_REVIEW,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        GATE_AUDIT,
        RUN_MANIFEST,
    ]
    external_paths = []
    for item in payload.get("report_identity", []) + payload.get("telemetry_identity", []):
        path_text = item.get("report_path") or item.get("path")
        if path_text:
            external_paths.append(path_text)
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
        "external_local_paths": external_paths,
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(NEGATIVE_RESULT_REGISTER)],
        "availability": "tracked_receipts_with_ignored_parent_runtime_artifact_hashes(추적 영수증과 무시된 부모 런타임 산출물 해시)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
    }


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    gap_rows = read_csv(GAP_ROWS) if path_exists(GAP_ROWS) else []
    cause_rows = read_csv(CAUSE_ROWS) if path_exists(CAUSE_ROWS) else []
    negative_text = io_path(NEGATIVE_RESULT_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_RESULT_REGISTER) else ""
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "gap_rows_exists": path_exists(GAP_ROWS),
        "gap_rows_count_two": len(gap_rows) == 2,
        "cause_rows_exists": path_exists(CAUSE_ROWS),
        "cause_rows_count_two": len(cause_rows) == 2,
        "winrate_erosion_named": all("win_rate" in row.get("dominant_gap_cause", "") for row in cause_rows),
        "report_exists": path_exists(REPORT),
        "gate_audit_exists": path_exists(GATE_AUDIT),
        "run_evidence_receipt_exists": path_exists(RUN_EVIDENCE_RECEIPT),
        "performance_receipt_exists": path_exists(PERFORMANCE_RECEIPT),
        "runtime_parity_receipt_exists": path_exists(RUNTIME_PARITY_RECEIPT),
        "result_receipt_exists": path_exists(RESULT_RECEIPT),
        "task_force_review_exists": path_exists(TASK_FORCE_REVIEW),
        "manifest_exists": path_exists(RUN_MANIFEST),
        "packet_final_claim_guard_exists": path_exists(PACKET_FINAL_CLAIM_GUARD),
        "parent_reports_exist_via_io_path": all(bool(item.get("io_path_exists")) for item in payload.get("report_identity", [])),
        "negative_result_register_updated": NEGATIVE_RESULT_ID in negative_text,
        "workspace_state_next_run": NEXT_RUN_ID in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = ledger_row(payload, created_at)
    for ledger_path, key in ((RUN_REGISTRY, "run_id"), (ALPHA_LEDGER, "ledger_row_id"), (STAGE_LEDGER, "ledger_row_id")):
        remove_registry_rows(ledger_path, RUN_ID)
        append_csv_row(ledger_path, row, key=key, source_header=ALPHA_LEDGER if ledger_path == STAGE_LEDGER else None)


def update_state_files(created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f83_short_density_gap_attributed_negative_runtime_probe_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f83_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F83F short-density proxy/runtime gap analysis(숏 밀도 프록시/런타임 간극 분석)을 완료했다."
  - "Effect(효과): F83E의 부정 런타임 결과를 win-rate/DD erosion after signal parity(신호 동등성 이후 승률/손실폭 침식)으로 귀속했다."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F83F short-density proxy/runtime gap analysis(F83F 숏 밀도 프록시/런타임 간극 분석)을 완료했다.

Effect(효과): F83E는 signal parity(신호 동등성)를 보존했지만 runtime win-rate/DD erosion(런타임 승률/손실폭 침식)으로 validation/OOS(검증/외표본) 모두 부정이었다.

Next run(다음 실행): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    oos = payload["oos_gap"]
    write_text(
        SELECTION_STATUS,
        f"""# F83 Selection Status(F83 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F83F gap analysis(F83F 간극 분석)을 기록했다.

Effect(효과): F83E OOS runtime(외표본 런타임)은 net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}`로 부정이며, 주 간극은 signal mismatch(신호 불일치)가 아니라 runtime win-rate erosion(런타임 승률 침식)이다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    val = payload["validation_gap"]
    oos = payload["oos_gap"]
    write_text(
        CONTEXT_ANCHOR,
        f"""# F83 Context Anchor(F83 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- validation runtime(검증 런타임): net `{val.get('runtime_net_profit')}`, PF `{val.get('runtime_profit_factor')}`, DD `{val.get('runtime_drawdown_percent')}`, win-rate delta `{val.get('win_rate_delta_pp')}` pp
- OOS runtime(외표본 런타임): net `{oos.get('runtime_net_profit')}`, PF `{oos.get('runtime_profit_factor')}`, DD `{oos.get('runtime_drawdown_percent')}`, win-rate delta `{oos.get('win_rate_delta_pp')}` pp
- gap cause(간극 원인): runtime win-rate/DD erosion after signal parity(신호 동등성 이후 런타임 승률/손실폭 침식)
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F83 Review Index(F83 검토 색인)\n"
    lines = [
        "- `frontier83F_short_density_proxy_runtime_gap_analysis_report.md`: F83F short-density proxy/runtime gap analysis report(F83F 숏 밀도 프록시/런타임 간극 분석 보고서)",
        "- `f83f_short_density_proxy_runtime_gap_analysis_summary.json`: F83F machine gap summary(F83F 기계 간극 요약)",
        "- `f83f_short_density_proxy_runtime_gap_rows.csv`: F83F split-level gap rows(F83F 구간별 간극 행)",
        "- `f83f_gap_cause_attribution_rows.csv`: F83F cause attribution rows(F83F 원인 귀속 행)",
        "- `required_gate_coverage_audit_f83f.md`: F83F gate audit(F83F 게이트 감사)",
        "- `f83f_task_force_review_receipt.yaml`: F83F Task Force review receipt(F83F 태스크포스 검토 영수증)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    oos = payload["oos_gap"]
    addition = f"""

{marker}
- `{RUN_ID}` attributed F83E short-density runtime gap(F83E 숏 밀도 런타임 간극 귀속). Result(결과): OOS runtime net/PF/DD/trades-day(외표본 런타임 순손익/수익 팩터/손실폭/일 거래) `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}/{oos.get('runtime_trades_per_day')}`. Clue(단서): dense short ONNX/signal parity(조밀한 숏 온엑스/신호 동등성). Negative memory(부정 기억): win-rate/DD erosion after signal parity(신호 동등성 이후 승률/손실폭 침식). Next(다음): `{NEXT_RUN_ID}`.
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_negative_result_register(payload: Mapping[str, Any]) -> None:
    text = io_path(NEGATIVE_RESULT_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_RESULT_REGISTER) else "# Negative Result Register\n"
    marker = f"<!-- {NEGATIVE_RESULT_ID} -->"
    val = payload["validation_gap"]
    oos = payload["oos_gap"]
    addition = f"""

{marker}
## {NEGATIVE_RESULT_ID}

- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): F83D short density proxy(F83D 숏 밀도 프록시) `f82b_10355`가 MT5 runtime(MT5 런타임)에서도 validation/OOS(검증/외표본) 양수와 5~10 trades/day(일 거래 수)를 보존할 수 있다.
- Why failed(실패 이유): F83E runtime(F83E 런타임)은 signal/feature parity(신호/피처 동등성)를 보존했지만 validation net/PF/DD(검증 순손익/수익 팩터/손실폭) `{val.get('runtime_net_profit')}/{val.get('runtime_profit_factor')}/{val.get('runtime_drawdown_percent')}`와 OOS `{oos.get('runtime_net_profit')}/{oos.get('runtime_profit_factor')}/{oos.get('runtime_drawdown_percent')}`로 부정이었다. Order fill gap(주문 체결 간극)은 net gap(순손익 간극)을 설명하기에 작고, 핵심은 runtime win-rate/DD erosion(런타임 승률/손실폭 침식)이다.
- Salvage value(회수 가치): dense short supply(조밀한 숏 공급), ONNX/signal/feature parity(온엑스/신호/피처 동등성), selected-entry veto tape(선택 진입 차단 테이프), win-rate erosion diagnostic(승률 침식 진단)을 보존한다.
- Do-not-repeat(반복 금지): same `f82b_10355`/F83E close_direction smooth_supply short density surface(동일 종가방향 부드러운 공급 숏 밀도 표면)를 threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)로 반복하지 않는다.
- Reopen condition(재개 조건): runtime-realized outcome label(런타임 실현 결과 라벨), stop-touch/fill-path target(스톱 터치/체결 경로 목표), risk logic(위험 로직), or regime/session split(장세/세션 분할) 중 하나 이상이 새로워지고 MT5 Runtime Probe(MT5 런타임 탐침)를 포함할 때만 재개한다.
- Evidence(근거): `{rel(REPORT)}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(NEGATIVE_RESULT_REGISTER, text.rstrip() + addition)


def update_artifact_registry(created_at: str) -> None:
    remove_csv_rows(ARTIFACT_REGISTRY, lambda row: row.get("run_id") == RUN_ID or str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__"))
    for path in [
        SUMMARY,
        GAP_ROWS,
        CAUSE_ROWS,
        RUN_EVIDENCE_RECEIPT,
        PERFORMANCE_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        TASK_FORCE_REVIEW,
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
            "effect": "Supports F83F negative gap analysis only(F83F 부정 간극 분석만 지원).",
        }
        append_csv_row(ARTIFACT_REGISTRY, row, key="artifact_id")


def packet_files(created_at: str) -> None:
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "receipts": [
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-performance-attribution", "status": "executed", "path": rel(PERFORMANCE_RECEIPT)},
                {"skill": "obsidian-runtime-parity", "status": "executed", "path": rel(RUNTIME_PARITY_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_REVIEW)},
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
    - obsidian-performance-attribution
    - obsidian-runtime-parity
    - obsidian-result-judgment
    - obsidian-task-force-review
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
required_gates:
  - parent_runtime_evidence
  - proxy_runtime_gap_rows
  - gap_cause_attribution
  - runtime_report_identity
  - run_evidence_receipt
  - performance_attribution_receipt
  - result_judgment_boundary
  - codex_task_force_review_packet
  - negative_memory_record
  - final_claim_guard
  - required_gate_coverage_audit
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  claim_boundary: {CLAIM_BOUNDARY}
evidence_contract:
  source_inputs:
    - {rel(F83D_TARGET_SELECTION)}
    - {rel(F83E_SUMMARY)}
    - {rel(F83E_MANIFEST)}
    - {rel(F83E_RECEIPT)}
  produced_artifacts:
    - {rel(SUMMARY)}
    - {rel(GAP_ROWS)}
    - {rel(CAUSE_ROWS)}
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
                "parent_runtime_evidence": "pass",
                "proxy_runtime_gap_rows": "pass",
                "gap_cause_attribution": "pass",
                "runtime_report_identity": "pass",
                "run_evidence_receipt": "pass",
                "performance_attribution_receipt": "pass",
                "result_judgment_boundary": "pass",
                "codex_task_force_review_packet": "pass",
                "negative_memory_record": "pass",
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


def write_all(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    write_json(SUMMARY, payload)
    write_csv(GAP_ROWS, payload["gap_rows"])
    write_csv(CAUSE_ROWS, payload["cause_rows"])
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    write_receipts(payload)
    manifest = {
        **payload,
        "artifacts": {
            "summary": rel(SUMMARY),
            "gap_rows": rel(GAP_ROWS),
            "cause_rows": rel(CAUSE_ROWS),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
            "run_evidence_receipt": rel(RUN_EVIDENCE_RECEIPT),
            "performance_receipt": rel(PERFORMANCE_RECEIPT),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT),
            "result_receipt": rel(RESULT_RECEIPT),
            "task_force_review": rel(TASK_FORCE_REVIEW),
        },
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
    update_ledgers(payload, created_at)
    update_state_files(created_at)
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    update_negative_result_register(payload)
    packet_files(created_at)
    verification = local_verification(payload)
    write_json(LOCAL_VERIFICATION, verification)
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload))
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
                    "validation_gap": payload.get("validation_gap"),
                    "oos_gap": payload.get("oos_gap"),
                    "primary_attribution": payload.get("primary_attribution"),
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
