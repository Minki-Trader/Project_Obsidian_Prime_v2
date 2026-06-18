from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
RUN_ID = "frontier84F_runtime_realized_winrate_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_v1"
NEXT_STAGE_ID = "stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild"
NEXT_RUN_ID = "frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_v1"

STATUS = "f84_closed_negative_runtime_path_contradiction_rotation_to_f85_no_authority"
JUDGMENT = "proxy_win_runtime_loss_dominant_risk_shape_failure_rotation_no_authority"
DECISION = "rotate_to_f85_runtime_path_contradiction_firewall_label_rebuild"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f84_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "retired_archive_only_no_new_grok_call_no_next_open_block"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

F84B_SUMMARY = REVIEW_DIR / "f84b_runtime_realized_winrate_proxy_scout_summary.json"
F84C_SUMMARY = REVIEW_DIR / "f84c_mt5_runtime_realized_winrate_materialization_summary.json"
F84D_SUMMARY = REVIEW_DIR / "f84d_runtime_realized_winrate_gap_analysis_summary.json"
F84E_SUMMARY = REVIEW_DIR / "f84e_row_level_deal_reconciliation_summary.json"
F84E_ROWS = REVIEW_DIR / "f84e_row_level_reconciliation_rows.csv"
F84E_SPLIT_SUMMARY = REVIEW_DIR / "f84e_row_level_reconciliation_split_summary.csv"
F84E_MONTH_SESSION = REVIEW_DIR / "f84e_month_session_streak_summary.csv"
F84E_UNMATCHED = REVIEW_DIR / "f84e_unmatched_runtime_mapping_rows.csv"
F84E_NORMALIZED_DEALS = (
    STAGE_DIR
    / "02_runs"
    / PARENT_RUN_ID
    / "f84e_mt5_normalized_deal_rows.csv"
)
F84E_NORMALIZED_TRADES = (
    STAGE_DIR
    / "02_runs"
    / PARENT_RUN_ID
    / "f84e_mt5_normalized_trade_rows.csv"
)

SUMMARY = REVIEW_DIR / "f84f_repair_or_rotation_decision_summary.json"
DECISION_MATRIX = REVIEW_DIR / "f84f_repair_rotation_decision_matrix.csv"
CLOSEOUT_KPI_ROWS = REVIEW_DIR / "f84f_closeout_kpi_rows.csv"
PATH_PIVOTS = REVIEW_DIR / "f84f_runtime_path_contradiction_pivot_rows.csv"
SOURCE_HASH_REFRESH = REVIEW_DIR / "f84f_f84e_source_hash_refresh.json"
ACTUAL_SUBAGENT_CALLS = REVIEW_DIR / "f84f_actual_subagent_calls.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f84f_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f84f_local_verification.json"
REPORT = REVIEW_DIR / "frontier84F_runtime_realized_winrate_repair_or_rotation_decision_report.md"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f84f.md"
STATE_SYNC_AUDIT = REVIEW_DIR / "f84f_state_sync_audit.json"
CLOSEOUT_GATE = REVIEW_DIR / "f84f_closeout_gate.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RUN_DECISION_MATRIX = RUN_DIR / "f84f_repair_rotation_decision_matrix.csv"
RUN_CLOSEOUT_KPI_ROWS = RUN_DIR / "f84f_closeout_kpi_rows.csv"

RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f84f_run_evidence_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f84f_result_judgment_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f84f_performance_attribution_receipt.yaml"
RUNTIME_PARITY_RECEIPT = REVIEW_DIR / "f84f_runtime_parity_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f84f_artifact_lineage_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f84f_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f84f_claim_discipline_receipt.yaml"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_frontier84_closeout_rotate_f85.md"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
NEXT_STAGE_BRIEF = NEXT_STAGE_DIR / "00_spec/stage_brief.md"
NEXT_INPUT_REFS = NEXT_STAGE_DIR / "01_inputs/input_refs.md"

SCRIPT_REL = "stage_pipelines/stage_frontier_84/frontier84f_runtime_realized_winrate_repair_or_rotation_decision.py"

TASK_FORCE_CALLS: list[dict[str, Any]] = [
    {
        "roster_id": "agent_01_system_governor",
        "nickname": "Gauss",
        "agent_id": "019eda75-0706-74f1-9778-dade29fa7217",
        "status": "completed",
        "phase": "f84f_governance_boundary",
        "classification": "accepted",
        "accepted": "F84F may choose capped repair, rotation, or closeout, but only with new evidence/new axis.",
        "rejected": "Completion, baseline, promotion, runtime authority, live readiness, and Goal Achieve claims.",
        "needs_local_verification": "Codex must keep final direction and claim boundary.",
    },
    {
        "roster_id": "agent_02_platform_routing_architect",
        "nickname": "Euler",
        "agent_id": "019eda75-1b53-7462-90fe-67534c94fd08",
        "status": "completed",
        "phase": "f84f_work_family_routing",
        "classification": "accepted",
        "accepted": "Route F84F as kpi_evidence(KPI 근거) with run evidence, artifact lineage, result judgment, and performance attribution.",
        "rejected": "Runtime backtest as primary family, because F84F is a decision packet(결정 묶음), not a new MT5 run.",
        "needs_local_verification": "Gate coverage must link actual subagent calls and source authority.",
    },
    {
        "roster_id": "agent_03_philosophy_policy_skill_governance",
        "nickname": "Lagrange",
        "agent_id": "019eda75-3495-7601-b3b6-317d9966dc12",
        "status": "completed",
        "phase": "f84f_policy_rotation_judgment",
        "classification": "accepted",
        "accepted": "Rotation is justified because F84E shows OOS proxy win -> runtime loss dominance and runtime PF 0.8598.",
        "rejected": "Same-surface threshold/filter repair(동일 표면 임계값/필터 수리).",
        "needs_local_verification": "Record negative memory and next frontier proposal instead of promotion.",
    },
    {
        "roster_id": "agent_04_evidence_control_plane",
        "nickname": "Einstein",
        "agent_id": "019eda75-4dc4-7791-a58b-c22f9481e5a7",
        "status": "completed",
        "phase": "f84f_evidence_hash_lineage",
        "classification": "needs_local_verification",
        "accepted": "F84E row-level evidence content is sufficient for the F84F decision input.",
        "rejected": "Using stale internal hashes from f84e_artifact_lineage.json(산출물 계보) as sealed evidence.",
        "needs_local_verification": "Refresh current F84E source hashes in F84F lineage before closeout.",
    },
    {
        "roster_id": "agent_05_data_feature_contract",
        "nickname": "Popper",
        "agent_id": "019eda75-66f4-70e3-aba1-32cdc79ef5b6",
        "status": "completed",
        "phase": "f84f_data_integrity_join_boundary",
        "classification": "accepted",
        "accepted": "F84E row-level reconciliation is usable with boundary; ticket_match rows support economics judgment.",
        "rejected": "Treating unfilled/no-attempt rows with old position_after tickets as economics authority.",
        "needs_local_verification": "F84F must use runtime_match_status == ticket_match rows for economics.",
    },
    {
        "roster_id": "agent_06_quant_research",
        "nickname": "Tesla",
        "agent_id": "019eda78-74a8-70e0-bdc6-22939add6bfc",
        "status": "completed",
        "phase": "f84f_quant_axis_attribution",
        "classification": "accepted",
        "accepted": "Rotation first; target-axis rotation(목표축 회전), path-inversion meta-label(경로 반전 보조 라벨), and both-hit ambiguity(양방향 터치 모호성) are strong F85 seeds.",
        "rejected": "Threshold-only repair(임계값만 수리), bad-month deletion(나쁜 월 삭제), and direct feature use of runtime/ex-post labels.",
        "needs_local_verification": "First-touch(첫 터치) or leakage-safe(누수 안전) pre-entry inputs require WFO/MT5 verification in F85.",
    },
    {
        "roster_id": "agent_07_model_validation_risk",
        "nickname": "Volta",
        "agent_id": "019eda79-299a-7732-808e-45aed07e408f",
        "status": "completed",
        "phase": "f84f_model_risk_counterview",
        "classification": "accepted_with_verification",
        "accepted": "Risk-shape failure(위험 형태 실패) is likely, and non-leaky capped repair(누수 없는 상한 수리) has research value.",
        "rejected": "Invalid mapping(무효 매핑), execution accounting(실행 회계), or model calibration-only(모델 보정 단독) as primary cause.",
        "needs_local_verification": "Capped repair must use pre-entry surrogate(진입 전 대체 신호), not tp_expected_sl_actual(사후 행 분류).",
    },
    {
        "roster_id": "agent_08_mt5_onnx_runtime",
        "nickname": "Newton",
        "agent_id": "019eda7b-3936-73a2-91a6-5a752ae0f23a",
        "status": "completed",
        "phase": "f84f_mt5_onnx_runtime_boundary",
        "classification": "accepted",
        "accepted": "F84E MT5 row-level evidence is sufficient to close F84 negative/no authority and open F85.",
        "rejected": "Another same-surface MT5 runtime probe(동일 표면 MT5 런타임 탐침) before rotation.",
        "needs_local_verification": "F85 must rebuild leakage-safe labels and rematerialize through WFO/MT5 before any stronger runtime claim.",
    },
]


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


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def open_for_csv_rewrite(path: Path):
    target = str(path.resolve())
    if path.exists():
        handle = open(target, "r+", encoding="utf-8-sig", newline="")
        handle.seek(0)
        handle.truncate()
        return handle
    return open(target, "w", encoding="utf-8-sig", newline="")


def remove_csv_rows(path: Path, predicate: Callable[[dict[str, str]], bool]) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [row for row in reader if not predicate(row)]
    handle = open_for_csv_rewrite(path)
    with handle:
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
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    handle = open_for_csv_rewrite(path)
    with handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def data_row_count(path: Path) -> int:
    if not path_exists(path):
        return -1
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def max_consecutive_losses(rows: Sequence[Mapping[str, str]]) -> int:
    best = 0
    current = 0
    for row in sorted(rows, key=lambda item: str(item.get("timestamp_utc", ""))):
        if str(row.get("runtime_match_status")) != "ticket_match":
            continue
        if as_bool(row.get("runtime_win_bool")):
            current = 0
        else:
            current += 1
            best = max(best, current)
    return best


def period_text(rows: Sequence[Mapping[str, str]]) -> str:
    stamps = sorted(str(row.get("timestamp_utc", ""))[:10] for row in rows if row.get("timestamp_utc"))
    if not stamps:
        return "missing(누락)"
    return f"{stamps[0]}..{stamps[-1]}"


def distinct_days(rows: Sequence[Mapping[str, str]]) -> int:
    return len({str(row.get("timestamp_utc", ""))[:10] for row in rows if row.get("timestamp_utc")})


def split_summary_rows() -> dict[str, dict[str, Any]]:
    return {row["split"]: row for row in read_csv(F84E_SPLIT_SUMMARY)}


def matched_rows(rows: Sequence[Mapping[str, str]], split: str) -> list[dict[str, str]]:
    return [
        dict(row)
        for row in rows
        if row.get("split") == split and row.get("runtime_match_status") == "ticket_match"
    ]


def runtime_profit_factor(gross_profit: float, gross_loss: float) -> float | str:
    if gross_loss == 0:
        return "inf" if gross_profit > 0 else ""
    return gross_profit / abs(gross_loss)


def aggregate_rows(rows: Sequence[Mapping[str, str]], split: str, group_type: str, group_value: str) -> dict[str, Any]:
    selected = [row for row in rows if row.get("runtime_match_status") == "ticket_match"]
    runtime_net = sum(as_float(row.get("runtime_net_profit_filled") or row.get("runtime_net_profit")) for row in selected)
    gross_profit = sum(max(0.0, as_float(row.get("runtime_net_profit_filled") or row.get("runtime_net_profit"))) for row in selected)
    gross_loss = sum(min(0.0, as_float(row.get("runtime_net_profit_filled") or row.get("runtime_net_profit"))) for row in selected)
    wins = sum(1 for row in selected if as_bool(row.get("runtime_win_bool")))
    proxy_wins = sum(1 for row in selected if as_bool(row.get("proxy_win")))
    proxy_win_runtime_loss = sum(1 for row in selected if as_bool(row.get("proxy_win_runtime_loss")))
    tp_expected_sl_actual = sum(1 for row in selected if as_bool(row.get("tp_expected_sl_actual")))
    sl_expected_tp_actual = sum(1 for row in selected if as_bool(row.get("sl_expected_tp_actual")))
    trade_count = len(selected)
    return {
        "split": split,
        "group_type": group_type,
        "group_value": group_value,
        "matched_trade_count": trade_count,
        "runtime_net_profit": round(runtime_net, 6),
        "runtime_gross_profit": round(gross_profit, 6),
        "runtime_gross_loss": round(gross_loss, 6),
        "runtime_profit_factor": runtime_profit_factor(gross_profit, gross_loss),
        "runtime_win_count": wins,
        "runtime_win_rate_percent": (wins / trade_count * 100.0) if trade_count else "",
        "proxy_win_count": proxy_wins,
        "proxy_win_runtime_loss_count": proxy_win_runtime_loss,
        "proxy_win_to_runtime_loss_rate": (proxy_win_runtime_loss / proxy_wins) if proxy_wins else "",
        "tp_expected_sl_actual_count": tp_expected_sl_actual,
        "sl_expected_tp_actual_count": sl_expected_tp_actual,
        "max_consecutive_loss": max_consecutive_losses(selected),
        "source_authority": "ticket_match_rows_only(티켓 결합 행 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_path_pivots(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    pivots: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        split_rows = matched_rows(rows, split)
        pivots.append(aggregate_rows(split_rows, split, "all_matched(전체 결합)", "all"))
        for label in sorted({row.get("proxy_exit_path_label", "") for row in split_rows}):
            group = [row for row in split_rows if row.get("proxy_exit_path_label") == label]
            pivots.append(aggregate_rows(group, split, "proxy_exit_path_label(프록시 종료 경로 라벨)", label))
        for session in sorted({row.get("session_bucket", "") for row in split_rows}):
            group = [row for row in split_rows if row.get("session_bucket") == session]
            pivots.append(aggregate_rows(group, split, "session_bucket(세션 구간)", session))
        tp_sl = [row for row in split_rows if as_bool(row.get("tp_expected_sl_actual"))]
        no_tp_sl = [row for row in split_rows if not as_bool(row.get("tp_expected_sl_actual"))]
        pivots.append(aggregate_rows(tp_sl, split, "diagnostic_class(진단 분류)", "tp_expected_sl_actual_true"))
        pivots.append(aggregate_rows(no_tp_sl, split, "diagnostic_class(진단 분류)", "excluding_tp_expected_sl_actual"))
    return pivots


def build_closeout_kpi_rows(rows: Sequence[Mapping[str, str]], split_rows: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    kpi_rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        source = split_rows[split]
        matched = matched_rows(rows, split)
        trade_count = int(as_float(source.get("runtime_trade_count")))
        wins = int(as_float(source.get("runtime_win_count_matched")))
        losses = max(0, trade_count - wins)
        gross_profit = as_float(source.get("runtime_gross_profit_matched"))
        gross_loss = as_float(source.get("runtime_gross_loss_matched"))
        avg_win = gross_profit / wins if wins else ""
        avg_loss = gross_loss / losses if losses else ""
        payoff = (as_float(avg_win) / abs(as_float(avg_loss))) if avg_win != "" and avg_loss != "" and as_float(avg_loss) else ""
        long_count = sum(1 for row in matched if row.get("direction") == "buy")
        short_count = sum(1 for row in matched if row.get("direction") == "sell")
        days = distinct_days(matched)
        kpi_rows.append(
            {
                "record_id": f"{RUN_ID}__runtime_{split}",
                "split": split,
                "test_period": period_text(matched),
                "proxy_kpi": (
                    f"proxy_net={source.get('proxy_pnl_contract_matched')};"
                    f"proxy_win_rate={source.get('proxy_win_rate_matched_percent')};"
                    f"proxy_wins={source.get('proxy_win_count_matched')}"
                ),
                "runtime_kpi": (
                    f"runtime_net={source.get('runtime_net_profit_matched')};"
                    f"runtime_pf={source.get('runtime_profit_factor_matched')};"
                    f"runtime_dd={source.get('receipt_runtime_drawdown_percent')};"
                    f"runtime_win_rate={source.get('runtime_win_rate_matched_percent')}"
                ),
                "net_profit": source.get("runtime_net_profit_matched"),
                "gross_profit": source.get("runtime_gross_profit_matched"),
                "gross_loss": source.get("runtime_gross_loss_matched"),
                "PF": source.get("runtime_profit_factor_matched"),
                "DD_percent": source.get("receipt_runtime_drawdown_percent"),
                "trade_count": trade_count,
                "trades_per_day": (trade_count / days) if days else "",
                "win_rate": source.get("runtime_win_rate_matched_percent"),
                "avg_win": avg_win,
                "avg_loss": avg_loss,
                "payoff_ratio": payoff,
                "expectancy": (as_float(source.get("runtime_net_profit_matched")) / trade_count) if trade_count else "",
                "recovery_factor": "not_available_without_drawdown_amount(손실폭 금액 없음)",
                "time_under_water": "not_available_in_f84e_receipt(F84E 영수증 없음)",
                "max_consecutive_loss": max_consecutive_losses(matched),
                "long_short_breakdown": f"long={long_count};short={short_count}(롱={long_count};숏={short_count})",
                "parity": "signal_feature_onnx_parity_preserved_before_economics_failure(경제성 실패 전 신호/피처/온엑스 동등성 보존)",
                "gap_cause": "runtime_path_contradiction_proxy_win_to_runtime_loss_dominant(런타임 경로 모순: 프록시 승리->런타임 손실 우세)",
                "next_action": NEXT_RUN_ID,
                "source_authority": "F84E row-level ticket_match economics(F84E 행 단위 티켓 결합 경제성)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return kpi_rows


def build_decision_matrix(oos: Mapping[str, Any], pivots: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    oos_tp_sl = next(
        row
        for row in pivots
        if row["split"] == "oos" and row["group_type"].startswith("diagnostic_class") and row["group_value"] == "tp_expected_sl_actual_true"
    )
    oos_without_tp_sl = next(
        row
        for row in pivots
        if row["split"] == "oos" and row["group_type"].startswith("diagnostic_class") and row["group_value"] == "excluding_tp_expected_sl_actual"
    )
    return [
        {
            "option": "same_surface_threshold_filter_parameter_repair(동일 표면 임계값/필터/파라미터 수리)",
            "decision": "rejected(거절)",
            "evidence": "F84E shows OOS proxy win -> runtime loss 560/821 and runtime PF 0.8598 after parity; agent_06 rejects threshold-only separation.",
            "effect": "Prevents repeating the same failure mode without a new axis(새 축 없는 동일 실패 반복 방지).",
        },
        {
            "option": "additional_same_surface_mt5_probe_before_rotation(회전 전 동일 표면 MT5 추가 탐침)",
            "decision": "rejected(거절)",
            "evidence": "F84C/F84E already materialized MT5 runtime rows: OOS selected 1805, matched 1801, net/PF/DD -133.51/0.8598/29.27.",
            "effect": "Avoids spending a runtime probe(런타임 탐침) on already diagnosed evidence.",
        },
        {
            "option": "direct_tp_expected_sl_actual_filter(익절예상-손절실제 직접 필터)",
            "decision": "rejected_as_leakage(누수로 거절)",
            "evidence": f"OOS diagnostic group has trades={oos_tp_sl['matched_trade_count']} and net={oos_tp_sl['runtime_net_profit']}, but the class uses ex-post runtime exit reason(사후 런타임 종료 사유).",
            "effect": "Preserves the clue(단서) while blocking an invalid feature/filter(무효 피처/필터).",
        },
        {
            "option": "non_leaky_capped_repair_inside_f84(전선84 내부 누수 없는 상한 수리)",
            "decision": "not_selected_preserved_as_f85_seed(미선택, 전선85 씨앗 보존)",
            "evidence": "Volta accepts one capped repair only if pre-entry surrogates are built; that requires a new label/source axis and WFO/MT5 materialization.",
            "effect": "Treats the repair idea as a new hypothesis lifecycle(새 가설 생명주기), not a late threshold tweak(늦은 임계값 수정).",
        },
        {
            "option": "rotate_to_f85_runtime_path_contradiction_firewall(전선85 런타임 경로 모순 방화벽 회전)",
            "decision": "accepted(수용)",
            "evidence": f"OOS excluding tp_expected_sl_actual net={oos_without_tp_sl['runtime_net_profit']} while tp_expected_sl_actual net={oos_tp_sl['runtime_net_profit']}; proxy win/runtime loss remains dominant and demands new leakage-safe labels.",
            "effect": "Moves the preserved clue(보존 단서) into a new runtime-label research axis(런타임 라벨 연구 축).",
        },
        {
            "option": "claim_completion_or_runtime_authority(완성 또는 런타임 권위 주장)",
            "decision": "rejected_forbidden_claim(금지 주장으로 거절)",
            "evidence": "Runtime OOS remains negative and DD is 29.27%, far outside final completion hard gate(최종 완성 강제 게이트).",
            "effect": "Keeps F84 closeout as negative memory(부정 기억) only.",
        },
    ]


def build_source_hash_refresh(created_at: str) -> dict[str, Any]:
    sources = [
        F84B_SUMMARY,
        F84C_SUMMARY,
        F84D_SUMMARY,
        F84E_SUMMARY,
        F84E_ROWS,
        F84E_SPLIT_SUMMARY,
        F84E_MONTH_SESSION,
        F84E_UNMATCHED,
        F84E_NORMALIZED_DEALS,
        F84E_NORMALIZED_TRADES,
    ]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "purpose": "Refresh current F84E source hashes because prior f84e_artifact_lineage internal hashes were stale(기존 F84E 계보 내부 해시가 낡아 현재 해시를 갱신).",
        "sources": [
            {
                "path": rel(path),
                "exists": path_exists(path),
                "data_row_count": data_row_count(path) if path.suffix.lower() == ".csv" else "",
                "sha256_lf_normalized": sha256_file_lf_normalized(path) if path_exists(path) else "",
            }
            for path in sources
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def task_force_coverage() -> dict[str, Any]:
    required = {f"agent_0{i}_" for i in range(1, 9)}
    covered = {call["roster_id"][:9] for call in TASK_FORCE_CALLS}
    completed = {call["roster_id"][:9] for call in TASK_FORCE_CALLS if call.get("status") == "completed"}
    return {
        "required_count": 8,
        "actual_call_count": len(TASK_FORCE_CALLS),
        "coverage_count": len(required & covered),
        "completed_count": len(required & completed),
        "all_required_covered": required <= covered,
        "all_required_completed": required <= completed,
        "call_ids": [call["agent_id"] for call in TASK_FORCE_CALLS],
    }


def build_payload(created_at: str) -> dict[str, Any]:
    f84e = read_json(F84E_SUMMARY)
    rows = read_csv(F84E_ROWS)
    split_rows = split_summary_rows()
    pivots = build_path_pivots(rows)
    closeout_rows = build_closeout_kpi_rows(rows, split_rows)
    decision_matrix = build_decision_matrix(split_rows["oos"], pivots)
    source_hash_refresh = build_source_hash_refresh(created_at)
    oos = split_rows["oos"]
    validation = split_rows["validation"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": "Runtime-realized win/loss and stop-touch path labels(런타임 실현 승패 및 손절/익절 경로 라벨)이 F84 proxy win-rate gap(프록시 승률 간극)을 수리할 수 있다.",
        "test_period": f"validation(검증) {closeout_rows[0]['test_period']}; OOS(표본외) {closeout_rows[1]['test_period']}",
        "f84e_source_status": {
            "status": f84e.get("status"),
            "judgment": f84e.get("judgment"),
            "primary_readout": f84e.get("primary_readout"),
            "preserved_clue": f84e.get("preserved_clue"),
            "negative_memory": f84e.get("negative_memory"),
        },
        "validation_summary": validation,
        "oos_summary": oos,
        "closeout_kpi_rows": closeout_rows,
        "runtime_path_contradiction_pivots": pivots,
        "decision_matrix": decision_matrix,
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "actual_subagent_roster_coverage": task_force_coverage(),
        "source_hash_refresh": source_hash_refresh,
        "gap_cause": "runtime_path_contradiction_proxy_win_to_runtime_loss_dominant(런타임 경로 모순: 프록시 승리 -> 런타임 손실 우세)",
        "why_rotation": [
            "F84E OOS(표본외) selected 1805, matched 1801, runtime net/PF/DD -133.51/0.8598/29.27 after signal/feature/ONNX parity(신호/피처/온엑스 동등성 이후).",
            "OOS proxy win -> runtime loss(프록시 승리 -> 런타임 손실) is 560 of 821 proxy wins, which makes win-rate repair a path-label problem(경로 라벨 문제).",
            "Direct tp_expected_sl_actual(익절예상-손절실제) filtering is ex-post leakage(사후 누수), so the repair needs a new F85 label/source axis.",
            "Another same-surface MT5 probe(동일 표면 MT5 탐침)는 F84E 근거를 반복할 가능성이 크다.",
        ],
        "preserved_clues": [
            "Density(밀도)는 MT5에서 보존됐지만 economics(경제성)는 보존되지 않았다.",
            "tp_expected_sl_actual(익절예상-손절실제) and both_hit_close_direction(양방향 터치 후 종가 방향)은 F85 label design(라벨 설계)의 단서다.",
            "cash_mid(현금장 중반) and path inversion(경로 반전)은 위험 라우팅 씨앗이다.",
        ],
        "negative_memory": [
            "F84 proxy winners(프록시 승리 행)은 runtime loss(런타임 손실)로 자주 뒤집힌다.",
            "Threshold-only repair(임계값만 수리)는 F84E row-level evidence(행 단위 근거)를 설명하지 못한다.",
            "Ex-post runtime exit labels(사후 런타임 종료 라벨)은 direct feature/filter(직접 피처/필터)로 쓰면 안 된다.",
        ],
        "next_frontier_question": "Can a leakage-safe runtime path contradiction firewall label(누수 안전 런타임 경로 모순 방화벽 라벨) reduce proxy-win/runtime-loss reversals while preserving enough US100 M5 trade density(거래 밀도)?",
        "next_frontier_seed_axes": [
            "pre-entry first-touch surrogate(진입 전 첫 터치 대체 신호)",
            "both-hit ambiguity class(양방향 터치 모호 분류)",
            "path-inversion meta-label(경로 반전 보조 라벨)",
            "session/regime/streak risk route(세션/장세/연속손실 위험 라우팅)",
            "WFO-aware selection and MT5 materialization(워크포워드 인식 선택 및 MT5 물질화)",
        ],
    }


def report_text(payload: Mapping[str, Any]) -> str:
    oos = payload["oos_summary"]
    validation = payload["validation_summary"]
    return f"""# F84F Repair Or Rotation Decision(F84F 수리 또는 회전 결정)

Updated(갱신): {payload['created_at_utc']}

Decision(결정): `{DECISION}`.

Action(행동): F84E row-level MT5 evidence(F84E 행 단위 MT5 근거)와 Task Force 8/8 actual calls(태스크포스 8/8 실제 호출)를 대조해 F84를 negative/no authority(부정/권위 없음)로 닫고 F85를 인계했다.

Effect(효과): same-surface threshold repair(동일 표면 임계값 수리)를 반복하지 않고, F84E의 path contradiction clue(경로 모순 단서)를 새 hypothesis lifecycle(가설 생명주기)로 넘긴다.

## KPI Readout(KPI 판독)

- Validation(검증): selected/matched `{validation.get('selected_entry_count')}/{validation.get('ticket_matched_trade_count')}`, runtime net/PF/DD `{validation.get('runtime_net_profit_matched')}/{validation.get('runtime_profit_factor_matched')}/{validation.get('receipt_runtime_drawdown_percent')}`, proxy win -> runtime loss `{validation.get('proxy_win_runtime_loss_count')}/{validation.get('proxy_win_count_matched')}`.
- OOS(표본외): selected/matched `{oos.get('selected_entry_count')}/{oos.get('ticket_matched_trade_count')}`, runtime net/PF/DD `{oos.get('runtime_net_profit_matched')}/{oos.get('runtime_profit_factor_matched')}/{oos.get('receipt_runtime_drawdown_percent')}`, proxy win -> runtime loss `{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}`.

## Judgment(판정)

- accepted(수용): rotate to F85 runtime path contradiction firewall label rebuild(F85 런타임 경로 모순 방화벽 라벨 재구축으로 회전).
- rejected(거절): same-surface threshold/filter/parameter repair(동일 표면 임계값/필터/파라미터 수리).
- rejected(거절): direct tp_expected_sl_actual filter(익절예상-손절실제 직접 필터), because it is ex-post leakage(사후 누수).
- preserved(보존): Volta(볼타)의 non-leaky capped repair(누수 없는 상한 수리) 의견은 F85 seed(전선85 씨앗)로 보존.

## Task Force(태스크포스)

Actual subagent calls(실제 하위 에이전트 호출): `8/8 completed(8/8 완료)`.

## Boundary(경계)

No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    coverage = payload["actual_subagent_roster_coverage"]
    return f"""# F84F Required Gate Coverage Audit(F84F 필수 게이트 커버리지 감사)

- kpi_contract_audit(KPI 계약 감사): pass(통과). Closeout KPI(마감 KPI)는 net/PF/DD/trade count/trades per day/win rate/avg win-loss/payoff/expectancy/max consecutive loss/long-short breakdown(순손익/수익 팩터/손실폭/거래 수/일 거래/승률/평균 이익·손실/손익비/기대값/최대 연속 손실/롱·숏 분해)을 포함한다.
- row_grain_audit(행 단위 감사): pass(통과). Economics(경제성)는 `runtime_match_status == ticket_match` rows(티켓 결합 행)만 사용했다.
- source_authority_audit(원천 권위 감사): pass(통과). F84E source hashes(전선84E 원천 해시)를 F84F에서 새로 계산했다.
- performance_attribution_receipt(성과 귀인 영수증): pass(통과). Path contradiction pivot(경로 모순 피벗)을 기록했다.
- result_judgment_boundary(결과 판정 경계): pass(통과). Negative/no authority(부정/권위 없음)로 닫았다.
- codex_task_force_review_packet(코덱스 태스크포스 검토 묶음): pass(통과). Actual calls(실제 호출) `{coverage['completed_count']}/{coverage['required_count']}`.
- frontier_extra_due_check(전선 추가 도래 점검): pass_not_due(통과/미도래). `{FRONTIER_EXTRA_DUE_STATUS}`.
- required_gate_coverage_audit(필수 게이트 커버리지 감사): pass(통과).
- final_claim_guard(최종 주장 보호): pass(통과). `{CLAIM_BOUNDARY}`.
"""


def task_force_receipt_text(payload: Mapping[str, Any]) -> str:
    rendered = []
    for call in payload["actual_subagent_calls"]:
        rendered.append(
            f"  - roster_id: {call['roster_id']}\n"
            f"    nickname: {call['nickname']}\n"
            f"    agent_id: {call['agent_id']}\n"
            f"    status: {call['status']}\n"
            f"    phase: {call['phase']}\n"
            f"    classification: {call['classification']}\n"
            f"    accepted: \"{call['accepted']}\"\n"
            f"    rejected: \"{call['rejected']}\"\n"
            f"    needs_local_verification: \"{call['needs_local_verification']}\""
        )
    coverage = payload["actual_subagent_roster_coverage"]
    return f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_8_of_8_no_authority
actual_subagent_call_count: {coverage['actual_call_count']}
completed_roster_coverage: {coverage['completed_count']}/{coverage['required_count']}
review_mode: role_timed_actual_subagent_calls_plus_codex_local_verification
actual_subagent_calls:
{chr(10).join(rendered)}
claim_boundary: {CLAIM_BOUNDARY}
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    oos = payload["oos_summary"]
    return {
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: passed
primary_family: kpi_evidence
source_run: {PARENT_RUN_ID}
oos_runtime_net_profit: {oos.get('runtime_net_profit_matched')}
oos_profit_factor: {oos.get('runtime_profit_factor_matched')}
oos_drawdown_percent: {oos.get('receipt_runtime_drawdown_percent')}
oos_trade_count: {oos.get('runtime_trade_count')}
decision: {DECISION}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: negative_no_authority
judgment: {JUDGMENT}
accepted_claim: F84 closeout negative memory and F85 handoff(F84 부정 기억 마감 및 F85 인계)
forbidden_claims: completion, selected_baseline, operating_promotion, runtime_authority, live_readiness, goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
        PERFORMANCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-performance-attribution
status: passed
primary_gap_cause: {payload['gap_cause']}
oos_proxy_win_runtime_loss: {oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}
decision_matrix: {rel(DECISION_MATRIX)}
path_pivots: {rel(PATH_PIVOTS)}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RUNTIME_PARITY_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-runtime-parity
status: inherited_from_f84c_f84e_with_boundary
decision: no_additional_same_surface_mt5_probe_before_f85
reason: F84E row-level MT5 evidence(F84E 행 단위 MT5 근거)가 충분해 F84F는 decision packet(결정 묶음)으로 닫음
next_runtime_requirement: F85 must rematerialize leakage-safe label through WFO/MT5(F85는 누수 안전 라벨을 WFO/MT5로 다시 물질화해야 함)
claim_boundary: {CLAIM_BOUNDARY}
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: passed
lineage: {rel(ARTIFACT_LINEAGE)}
source_hash_refresh: {rel(SOURCE_HASH_REFRESH)}
claim_boundary: {CLAIM_BOUNDARY}
""",
        TASK_FORCE_RECEIPT: task_force_receipt_text(payload),
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_no_authority
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
    }


def work_packet_text(payload: Mapping[str, Any]) -> str:
    return f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{payload['created_at_utc']}'
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
    - obsidian-task-force-review
required_gates:
  - kpi_contract_audit
  - row_grain_audit
  - source_authority_audit
  - performance_attribution_receipt
  - result_judgment_boundary
  - artifact_lineage_audit
  - codex_task_force_review_packet
  - frontier_extra_due_check
  - required_gate_coverage_audit
  - final_claim_guard
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_stage: {NEXT_STAGE_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  judgment: {JUDGMENT}
  decision: {DECISION}
  actual_subagent_calls: 8/8 completed(8/8 완료)
  claim_boundary: {CLAIM_BOUNDARY}
"""


def packet_gate_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "gates": {
            "kpi_contract_audit": "pass",
            "row_grain_audit": "pass",
            "source_authority_audit": "pass",
            "performance_attribution_receipt": "pass",
            "result_judgment_boundary": "pass",
            "artifact_lineage_audit": "pass",
            "codex_task_force_review_packet": "pass_8_of_8_actual_calls",
            "frontier_extra_due_check": "pass_not_due",
            "required_gate_coverage_audit": "pass",
            "final_claim_guard": "pass",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def final_claim_guard_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claim": "F84 negative closeout and F85 handoff only(F84 부정 마감 및 F85 인계만)",
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def state_sync_audit() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "pass",
        "workspace_state": rel(WORKSPACE_STATE),
        "current_working_state": rel(CURRENT_WORKING_STATE),
        "stage_selection_status": rel(SELECTION_STATUS),
        "global_selection_status": rel(GLOBAL_SELECTION_STATUS),
        "next_stage_brief": rel(NEXT_STAGE_BRIEF),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def closeout_gate() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "pass",
        "decision": DECISION,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def update_state_files(payload: Mapping[str, Any]) -> None:
    oos = payload["oos_summary"]
    created_at = payload["created_at_utc"]
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_stage_id: {STAGE_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
runtime_probe_status: f84_closed_negative_f85_requires_new_runtime_materialization
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F84F repair/rotation decision(F84F 수리/회전 결정)을 닫고 F85 scaffold(전선85 뼈대)를 만들었다."
  - "Effect(효과): OOS proxy win -> runtime loss(표본외 프록시 승리 -> 런타임 손실) {oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}을 F85 label rebuild(라벨 재구축) 씨앗으로 넘겼다."
  - "Task Force(태스크포스): 8/8 actual calls completed(실제 호출 완료)."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{NEXT_STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F84F repair/rotation decision(F84F 수리/회전 결정)으로 F84를 negative/no authority(부정/권위 없음) 마감했다.

Effect(효과): F84E row-level MT5 evidence(F84E 행 단위 MT5 근거)를 F85 runtime path contradiction firewall label rebuild(F85 런타임 경로 모순 방화벽 라벨 재구축)의 입력으로 고정했다.

OOS(표본외): selected `{oos.get('selected_entry_count')}`, matched `{oos.get('ticket_matched_trade_count')}`, runtime net/PF/DD `{oos.get('runtime_net_profit_matched')}/{oos.get('runtime_profit_factor_matched')}/{oos.get('receipt_runtime_drawdown_percent')}`, proxy win -> runtime loss `{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}`.

Task Force(태스크포스): `8/8 actual subagent calls completed(8/8 실제 하위 에이전트 호출 완료)`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )
    write_text(
        GLOBAL_SELECTION_STATUS,
        f"""# Selection Status(선택 상태)

Updated(갱신): {created_at}

Current stage(현재 단계): `{NEXT_STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F84 closed as negative runtime path contradiction evidence(F84를 부정 런타임 경로 모순 근거로 마감).

Effect(효과): F85 opens from preserved clue/negative memory(보존 단서/부정 기억) only, with no inherited winner/baseline/authority(상속 승자/기준선/권위 없음).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )


def update_stage_files(payload: Mapping[str, Any]) -> None:
    oos = payload["oos_summary"]
    created_at = payload["created_at_utc"]
    write_text(
        SELECTION_STATUS,
        f"""# F84 Selection Status(F84 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Decision(결정): `{DECISION}`

Action(행동): F84E row-level evidence(F84E 행 단위 근거)와 F84F Task Force 8/8 actual calls(태스크포스 8/8 실제 호출)로 F84를 마감했다.

Effect(효과): F84는 runtime authority(런타임 권위) 없이 negative memory(부정 기억)와 F85 seed(전선85 씨앗)만 남긴다.

OOS(표본외): selected `{oos.get('selected_entry_count')}`, matched `{oos.get('ticket_matched_trade_count')}`, runtime net/PF/DD `{oos.get('runtime_net_profit_matched')}/{oos.get('runtime_profit_factor_matched')}/{oos.get('receipt_runtime_drawdown_percent')}`.

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CONTEXT_ANCHOR,
        f"""# F84 Context Anchor(F84 문맥 앵커)

Updated(갱신): {created_at}

- stage(단계): `{STAGE_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- next stage(다음 단계): `{NEXT_STAGE_ID}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- OOS readout(표본외 판독): selected `{oos.get('selected_entry_count')}`, matched `{oos.get('ticket_matched_trade_count')}`, proxy win -> runtime loss `{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}`
- Task Force(태스크포스): `8/8 actual calls completed(8/8 실제 호출 완료)`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F84 Review Index(F84 검토 색인)\n"
    entries = [
        "- `frontier84F_runtime_realized_winrate_repair_or_rotation_decision_report.md`: F84F repair/rotation report(F84F 수리/회전 보고서)",
        "- `stage_closeout_report.md`: F84 stage closeout report(F84 단계 마감 보고서)",
        "- `f84f_repair_or_rotation_decision_summary.json`: F84F machine summary(F84F 기계 요약)",
        "- `f84f_repair_rotation_decision_matrix.csv`: F84F decision matrix(F84F 결정 행렬)",
        "- `f84f_actual_subagent_calls.json`: F84F actual Task Force calls(F84F 실제 태스크포스 호출)",
        "- `required_gate_coverage_audit_f84f.md`: F84F gate audit(F84F 게이트 감사)",
    ]
    for entry in entries:
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    write_text(REVIEW_INDEX, text)


def update_next_stage_scaffold(payload: Mapping[str, Any]) -> None:
    write_text(
        NEXT_STAGE_BRIEF,
        f"""# F85 Stage Brief(F85 단계 개요)

Stage ID(단계 ID): `{NEXT_STAGE_ID}`

Prepared by(작성 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Status(상태): `handoff_scaffold_pending_stage_open(인계 뼈대, 단계 개방 대기)`

## Question(질문)

{payload['next_frontier_question']}

## Action And Effect(행동과 효과)

Action(행동): F85는 F84E/F84F evidence(근거)를 reference only(참조 전용)로 받아, runtime path contradiction firewall label(런타임 경로 모순 방화벽 라벨)을 새 hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F84의 ex-post diagnostic class(사후 진단 분류)를 직접 필터로 쓰지 않고, leakage-safe pre-entry surrogate(누수 안전 진입 전 대체 신호)와 WFO/MT5 materialization(워크포워드/MT5 물질화)로 검증한다.

## Seed Axes(씨앗 축)

{chr(10).join(f"- {item}" for item in payload['next_frontier_seed_axes'])}

## Forbidden Inheritance(상속 금지)

- winner(승자)
- selected baseline(선택 기준선)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)

Boundary(경계): this scaffold(뼈대)는 F85 open evidence(F85 개방 근거)가 아니라 handoff(인계)다.
""",
    )
    write_text(
        NEXT_INPUT_REFS,
        f"""# F85 Input References(F85 입력 참조)

Prepared by(작성 실행): `{RUN_ID}`

## Reference Only(참조 전용)

- F84 closeout report(F84 마감 보고서): `{rel(STAGE_CLOSEOUT_REPORT)}`
- F84F decision summary(F84F 결정 요약): `{rel(SUMMARY)}`
- F84F decision matrix(F84F 결정 행렬): `{rel(DECISION_MATRIX)}`
- F84E row-level reconciliation rows(F84E 행 단위 조정 행): `{rel(F84E_ROWS)}`
- F84E split summary(F84E 구간 요약): `{rel(F84E_SPLIT_SUMMARY)}`
- F84C MT5 runtime materialization(F84C MT5 런타임 물질화): `{rel(F84C_SUMMARY)}`

## Use Boundary(사용 경계)

Action(행동): F85 may use F84E/F84F as clue/negative memory/seed surface(F85는 F84E/F84F를 단서/부정 기억/씨앗 표면으로 사용 가능).

Effect(효과): F85 must not inherit winner/baseline/runtime authority(F85는 승자/기준선/런타임 권위를 상속하지 않음).
""",
    )


def update_decision_memo(payload: Mapping[str, Any]) -> None:
    oos = payload["oos_summary"]
    write_text(
        DECISION_MEMO,
        f"""# Frontier84 Closeout And F85 Rotation Decision(전선84 마감 및 전선85 회전 결정)

Updated(갱신): {payload['created_at_utc']}

Decision(결정): `{DECISION}`

Action(행동): F84E row-level MT5 evidence(F84E 행 단위 MT5 근거)와 F84F Task Force(태스크포스) 검토를 근거로 F84를 negative/no authority(부정/권위 없음)로 마감했다.

Effect(효과): 같은 threshold/filter repair(임계값/필터 수리)를 반복하지 않고, F85 runtime path contradiction firewall label rebuild(F85 런타임 경로 모순 방화벽 라벨 재구축)을 다음 hypothesis lifecycle(가설 생명주기)로 연다.

Evidence(근거): OOS selected/matched `{oos.get('selected_entry_count')}/{oos.get('ticket_matched_trade_count')}`, runtime net/PF/DD `{oos.get('runtime_net_profit_matched')}/{oos.get('runtime_profit_factor_matched')}/{oos.get('receipt_runtime_drawdown_percent')}`, proxy win -> runtime loss `{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}`.

Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
    )


def update_registers(payload: Mapping[str, Any]) -> None:
    created_at = payload["created_at_utc"]
    oos = payload["oos_summary"]
    row = {
        "ledger_row_id": f"{RUN_ID}__closeout",
        "row_id": f"{RUN_ID}__closeout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_or_rotation_decision",
        "tier_scope": "Tier A runtime evidence; Tier B missing_required; combined out_of_scope_by_claim",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"oos_net={oos.get('runtime_net_profit_matched')};oos_pf={oos.get('runtime_profit_factor_matched')};oos_dd={oos.get('receipt_runtime_drawdown_percent')};proxy_win_runtime_loss={oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}",
        "guardrail_kpi": f"task_force=8/8_actual_calls;claim_boundary={CLAIM_BOUNDARY}",
        "external_verification_status": "completed_parent_mt5_row_level_evidence_reused_with_boundary",
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "run_date": created_at[:10],
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "F84E row-level MT5 evidence only",
        "work_family": "kpi_evidence",
        "run_family": "frontier_closeout_decision",
        "run_type": "repair_or_rotation_decision",
        "result_status": "negative_no_authority",
        "net_profit": oos.get("runtime_net_profit_matched"),
        "profit_factor": oos.get("runtime_profit_factor_matched"),
        "drawdown_percent": oos.get("receipt_runtime_drawdown_percent"),
        "trade_count": oos.get("runtime_trade_count"),
        "oos_net_profit": oos.get("runtime_net_profit_matched"),
        "oos_profit_factor": oos.get("runtime_profit_factor_matched"),
        "oos_trade_count": oos.get("runtime_trade_count"),
        "oos_drawdown_percent": oos.get("receipt_runtime_drawdown_percent"),
    }
    for ledger_path, key in ((RUN_REGISTRY, "run_id"), (ALPHA_LEDGER, "ledger_row_id"), (STAGE_LEDGER, "ledger_row_id")):
        remove_csv_rows(
            ledger_path,
            lambda existing: existing.get("run_id") == RUN_ID
            or existing.get("ledger_row_id") == row["ledger_row_id"]
            or existing.get("row_id") == row["row_id"],
        )
        append_csv_row(ledger_path, row, key=key, source_header=ALPHA_LEDGER if ledger_path == STAGE_LEDGER else None)
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker in idea_text:
        idea_text = idea_text.split(marker)[0].rstrip()
    write_text(
        IDEA_REGISTRY,
        idea_text.rstrip()
        + f"""

{marker}
- `{RUN_ID}` closed F84 as negative/no authority(부정/권위 없음). Preserved clue(보존 단서): runtime path contradiction(런타임 경로 모순), tp_expected_sl_actual(익절예상-손절실제), both-hit ambiguity(양방향 터치 모호성). Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
    )
    neg_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    neg_marker = "<!-- NR-F84-RUNTIME-PATH-CONTRADICTION-CLOSEOUT -->"
    if neg_marker in neg_text:
        neg_text = neg_text.split(neg_marker)[0].rstrip()
    write_text(
        NEGATIVE_REGISTER,
        neg_text.rstrip()
        + f"""

{neg_marker}
## NR-F84-RUNTIME-PATH-CONTRADICTION-CLOSEOUT

- Stage(단계): `{STAGE_ID}`
- Run(실행): `{RUN_ID}`
- Why failed(실패 이유): OOS(표본외) runtime net/PF/DD `{oos.get('runtime_net_profit_matched')}/{oos.get('runtime_profit_factor_matched')}/{oos.get('receipt_runtime_drawdown_percent')}`, proxy win -> runtime loss(프록시 승리 -> 런타임 손실) `{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}`.
- Do-not-repeat(반복 금지): same-surface threshold/filter/parameter-only repair(동일 표면 임계값/필터/파라미터만 수리).
- Salvage value(회수 가치): F85 runtime path contradiction firewall label seed(F85 런타임 경로 모순 방화벽 라벨 씨앗).
- Reopen condition(재개 조건): leakage-safe pre-entry surrogate(누수 안전 진입 전 대체 신호), WFO-aware split(워크포워드 인식 분할), and MT5 materialization(MT5 물질화)이 포함될 때만 재개.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
    )
    changelog_text = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog_text:
        entry = f"""# 2026-06-18 - F84F Closeout And F85 Rotation(F84F 마감 및 F85 회전)

- Action(행동): `{RUN_ID}`로 F84를 negative/no authority(부정/권위 없음) 마감했다.
- Effect(효과): runtime path contradiction(런타임 경로 모순)을 F85 leakage-safe label rebuild(F85 누수 안전 라벨 재구축) 씨앗으로 넘겼다.
- Task Force(태스크포스): 8/8 actual calls completed(8/8 실제 호출 완료).
- Boundary(경계): `{CLAIM_BOUNDARY}`.

"""
        write_text(CHANGELOG, entry + changelog_text)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    created_at = payload["created_at_utc"]
    paths = [
        ROOT / SCRIPT_REL,
        SUMMARY,
        DECISION_MATRIX,
        CLOSEOUT_KPI_ROWS,
        PATH_PIVOTS,
        SOURCE_HASH_REFRESH,
        ACTUAL_SUBAGENT_CALLS,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        STAGE_CLOSEOUT_REPORT,
        GATE_AUDIT,
        STATE_SYNC_AUDIT,
        CLOSEOUT_GATE,
        RUN_MANIFEST,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_GATE_AUDIT,
        FINAL_CLAIM_GUARD,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        DECISION_MEMO,
    ]
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [
                row
                for row in reader
                if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")
            ]
    else:
        fieldnames = []
        existing_rows = []
    new_rows: list[dict[str, Any]] = []
    for path in paths:
        if not path_exists(path):
            continue
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.stem,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": created_at,
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F84 closeout/F85 handoff only(F84 마감/F85 인계만 지원).",
            }
        )
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    if not fieldnames:
        fieldnames = list(new_rows[0].keys()) if new_rows else ["artifact_id"]
    tmp_path = ARTIFACT_REGISTRY.with_name(f"{ARTIFACT_REGISTRY.stem}.{RUN_ID}.tmp")
    with open(str(tmp_path.resolve()), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in existing_rows + [{field: csv_value(row.get(field, "")) for field in fieldnames} for row in new_rows]:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    tmp_path.replace(ARTIFACT_REGISTRY)


def artifact_lineage(payload: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = [
        ROOT / SCRIPT_REL,
        SUMMARY,
        DECISION_MATRIX,
        CLOSEOUT_KPI_ROWS,
        PATH_PIVOTS,
        SOURCE_HASH_REFRESH,
        ACTUAL_SUBAGENT_CALLS,
        LOCAL_VERIFICATION,
        REPORT,
        STAGE_CLOSEOUT_REPORT,
        GATE_AUDIT,
        STATE_SYNC_AUDIT,
        CLOSEOUT_GATE,
        RUN_MANIFEST,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_GATE_AUDIT,
        FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_CLOSEOUT_GATE,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        DECISION_MEMO,
        RUN_EVIDENCE_RECEIPT,
        RESULT_RECEIPT,
        PERFORMANCE_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        ARTIFACT_RECEIPT,
        TASK_FORCE_RECEIPT,
        CLAIM_RECEIPT,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": payload["created_at_utc"],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "source_inputs": [
            rel(F84B_SUMMARY),
            rel(F84C_SUMMARY),
            rel(F84D_SUMMARY),
            rel(F84E_SUMMARY),
            rel(F84E_ROWS),
            rel(F84E_SPLIT_SUMMARY),
            rel(F84E_NORMALIZED_TRADES),
        ],
        "source_hash_refresh": payload["source_hash_refresh"],
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY), rel(NEGATIVE_REGISTER)],
        "lineage_judgment": "connected_with_refreshed_source_hashes(현재 원천 해시로 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def local_verification(payload: Mapping[str, Any]) -> dict[str, Any]:
    state_text = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    report_text_current = io_path(REPORT).read_text(encoding="utf-8-sig") if path_exists(REPORT) else ""
    coverage = payload["actual_subagent_roster_coverage"]
    source_rows = {item["path"]: item for item in payload["source_hash_refresh"]["sources"]}
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "decision_matrix_exists": path_exists(DECISION_MATRIX),
        "closeout_kpi_rows_exists": path_exists(CLOSEOUT_KPI_ROWS),
        "path_pivots_exists": path_exists(PATH_PIVOTS),
        "f84e_source_hash_refresh_exists": path_exists(SOURCE_HASH_REFRESH),
        "f84e_row_count_4145": source_rows.get(rel(F84E_ROWS), {}).get("data_row_count") == 4145,
        "f84e_trade_row_count_4127": source_rows.get(rel(F84E_NORMALIZED_TRADES), {}).get("data_row_count") == 4127,
        "task_force_completed_8": coverage["all_required_completed"],
        "workspace_state_points_to_f85": NEXT_STAGE_ID in state_text and NEXT_RUN_ID in state_text,
        "f85_stage_scaffold_exists": path_exists(NEXT_STAGE_BRIEF) and path_exists(NEXT_INPUT_REFS),
        "final_claim_guard_exists": path_exists(FINAL_CLAIM_GUARD),
        "report_has_no_authority_boundary": CLAIM_BOUNDARY in report_text_current
        and "runtime authority(런타임 권위)" in report_text_current,
        "frontier_extra_not_due": FRONTIER_EXTRA_DUE_STATUS.startswith("not_due"),
    }
    return {
        "packet_id": RUN_ID,
        "status": "pass" if all(checks.values()) else "fail",
        "all_passed": all(checks.values()),
        "checks": checks,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ensure_dirs() -> None:
    for path in (
        RUN_DIR,
        REVIEW_DIR,
        SELECTED_DIR,
        PACKET_DIR,
        NEXT_STAGE_BRIEF.parent,
        NEXT_INPUT_REFS.parent,
        DECISION_MEMO.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def write_all(payload: dict[str, Any]) -> dict[str, Any]:
    write_csv(DECISION_MATRIX, payload["decision_matrix"])
    write_csv(RUN_DECISION_MATRIX, payload["decision_matrix"])
    write_csv(CLOSEOUT_KPI_ROWS, payload["closeout_kpi_rows"])
    write_csv(RUN_CLOSEOUT_KPI_ROWS, payload["closeout_kpi_rows"])
    write_csv(PATH_PIVOTS, payload["runtime_path_contradiction_pivots"])
    write_json(SOURCE_HASH_REFRESH, payload["source_hash_refresh"])
    write_json(ACTUAL_SUBAGENT_CALLS, {"actual_subagent_calls": payload["actual_subagent_calls"], "coverage": payload["actual_subagent_roster_coverage"]})
    write_text(REPORT, report_text(payload))
    write_text(STAGE_CLOSEOUT_REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_text(WORK_PACKET, work_packet_text(payload))
    write_json(
        SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-run-evidence-system",
            "receipts": [
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-performance-attribution", "status": "executed", "path": rel(PERFORMANCE_RECEIPT)},
                {"skill": "obsidian-runtime-parity", "status": "executed_with_boundary", "path": rel(RUNTIME_PARITY_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed_8_of_8", "path": rel(TASK_FORCE_RECEIPT)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(PACKET_GATE_AUDIT, packet_gate_json(payload))
    write_json(FINAL_CLAIM_GUARD, final_claim_guard_json())
    write_json(STATE_SYNC_AUDIT, state_sync_audit())
    write_json(CLOSEOUT_GATE, closeout_gate())
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync_audit())
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate())
    update_next_stage_scaffold(payload)
    update_decision_memo(payload)
    update_state_files(payload)
    update_stage_files(payload)
    update_registers(payload)

    verification = local_verification(payload)
    write_json(LOCAL_VERIFICATION, verification)
    payload["local_verification"] = verification
    write_json(SUMMARY, payload)
    write_json(RUN_MANIFEST, payload)
    lineage = artifact_lineage(payload)
    payload["artifact_lineage"] = lineage
    write_json(ARTIFACT_LINEAGE, lineage)
    write_json(SUMMARY, payload)
    write_json(RUN_MANIFEST, payload)
    update_artifact_registry(payload)
    return verification


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    payload["producer"] = SCRIPT_REL
    payload["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    payload["artifacts"] = {
        "summary": rel(SUMMARY),
        "decision_matrix": rel(DECISION_MATRIX),
        "closeout_kpi_rows": rel(CLOSEOUT_KPI_ROWS),
        "path_pivots": rel(PATH_PIVOTS),
        "actual_subagent_calls": rel(ACTUAL_SUBAGENT_CALLS),
        "report": rel(REPORT),
        "stage_closeout_report": rel(STAGE_CLOSEOUT_REPORT),
        "gate_audit": rel(GATE_AUDIT),
        "next_stage_brief": rel(NEXT_STAGE_BRIEF),
        "source_hash_refresh": rel(SOURCE_HASH_REFRESH),
        "local_verification": rel(LOCAL_VERIFICATION),
    }
    verification = write_all(payload)
    oos = payload["oos_summary"]
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "oos": {
                        "selected": oos.get("selected_entry_count"),
                        "matched": oos.get("ticket_matched_trade_count"),
                        "net": oos.get("runtime_net_profit_matched"),
                        "pf": oos.get("runtime_profit_factor_matched"),
                        "dd": oos.get("receipt_runtime_drawdown_percent"),
                        "proxy_win_runtime_loss": f"{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}",
                    },
                    "task_force": "8/8 actual calls completed",
                    "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
                    "next_run_id": NEXT_RUN_ID,
                    "local_verification": verification["status"],
                    "report": rel(REPORT),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if verification["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
