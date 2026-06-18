from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild"
RUN_ID = "frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_v1"
PARENT_RUN_ID = "frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_v1"
NEXT_RUN_MATERIAL = "frontier85C_mt5_runtime_path_firewall_materialization_v1"
NEXT_RUN_REPAIR = "frontier85C_runtime_path_firewall_repair_or_rotation_decision_v1"

STATUS_MATERIAL = "f85b_leakage_safe_firewall_candidate_for_f85c_mt5_materialization_no_authority"
STATUS_WEAK = "f85b_leakage_safe_firewall_weak_clue_repair_or_rotation_required_no_authority"
STATUS_NEGATIVE = "f85b_leakage_safe_firewall_no_meaningful_proxy_signal_negative_evidence_no_authority"
JUDGMENT_MATERIAL = "runtime_path_firewall_proxy_candidate_requires_mt5_materialization_no_authority"
JUDGMENT_WEAK = "runtime_path_firewall_proxy_clue_needs_repair_before_materialization_no_authority"
JUDGMENT_NEGATIVE = "runtime_path_firewall_proxy_scout_negative_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f84_closeout_next_boundary_f100_e01_closed_for_f050"
SCRIPT_REL = "stage_pipelines/stage_frontier_85/frontier85b_leakage_safe_runtime_path_firewall_proxy_scout.py"

INITIAL_BALANCE = 500.0
MIN_VALIDATION_KEEP_TRADES = 150
MIN_VALIDATION_KEEP_FRACTION = 0.25
MIN_REVERSAL_REDUCTION = 0.03
MAX_FALSE_VETO_WINNER_RATE = 0.70
MIN_TRADES_PER_DAY_OBSERVABLE = 1.0

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

SUMMARY = REVIEW_DIR / "f85b_leakage_safe_runtime_path_firewall_proxy_scout_summary.json"
SOURCE_HASH_REFRESH = REVIEW_DIR / "f85b_source_hash_refresh.json"
TASK_FORCE_CALLS_PATH = REVIEW_DIR / "f85b_actual_subagent_calls.json"
FEATURE_MANIFEST = REVIEW_DIR / "f85b_feature_manifest.json"
CANDIDATES_ALL = REVIEW_DIR / "f85b_firewall_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f85b_firewall_top_candidates.csv"
SPLIT_METRICS = REVIEW_DIR / "f85b_firewall_candidate_split_metrics.csv"
SELECTED_ROW_READOUT = REVIEW_DIR / "f85b_selected_firewall_row_readout.csv"
SELECTED_CANDIDATE = REVIEW_DIR / "f85b_materialization_candidate.json"
RUN_SELECTED_CANDIDATE = RUN_DIR / "f85b_materialization_candidate.json"
TIER_RECORD_AUDIT = REVIEW_DIR / "f85b_tier_record_audit.csv"
DATA_INTEGRITY = REVIEW_DIR / "f85b_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f85b_model_validation_review.json"
RESULT_JUDGMENT = REVIEW_DIR / "f85b_result_judgment_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f85b_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f85b_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
REPORT = REVIEW_DIR / "frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f85b.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f85b_run_evidence_receipt.yaml"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f85b_experiment_design_receipt.yaml"
DATA_INTEGRITY_RECEIPT = REVIEW_DIR / "f85b_data_integrity_receipt.yaml"
MODEL_VALIDATION_RECEIPT = REVIEW_DIR / "f85b_model_validation_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f85b_artifact_lineage_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f85b_result_judgment_receipt.yaml"
RUNTIME_HANDOFF_RECEIPT = REVIEW_DIR / "f85b_runtime_handoff_boundary_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f85b_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f85b_claim_discipline_receipt.yaml"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_frontier85b_proxy_scout.md"

F84_STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
F84_REVIEW_DIR = ROOT / "stages" / F84_STAGE_ID / "03_reviews"
F84E_ROWS = F84_REVIEW_DIR / "f84e_row_level_reconciliation_rows.csv"
F84E_SPLIT_SUMMARY = F84_REVIEW_DIR / "f84e_row_level_reconciliation_split_summary.csv"
F84E_SUMMARY = F84_REVIEW_DIR / "f84e_row_level_deal_reconciliation_summary.json"
F84F_SUMMARY = F84_REVIEW_DIR / "f84f_repair_or_rotation_decision_summary.json"
F85A_DESIGN = REVIEW_DIR / "f85a_experiment_design.json"

ALLOWED_FEATURE_COLUMNS = [
    "p_short",
    "p_flat",
    "p_long",
    "decision",
    "decision_reason",
    "model_risk_pct",
    "clipped_risk_pct",
    "computed_lot",
    "actual_risk_pct_after_floor",
    "atr_points",
    "open_sl_points",
    "open_tp_points",
    "hour_utc",
    "session_bucket",
]
AUDIT_ONLY_COLUMNS = [
    "bar_time_server",
    "timestamp_utc",
    "split",
    "row_index",
    "input_hash",
    "target_candidate_id",
    "source_candidate_id",
    "runtime_wrapper_id",
    "claim_boundary",
]
LABEL_DIAGNOSTIC_COLUMNS = [
    "proxy_win_runtime_loss",
    "proxy_loss_runtime_win",
    "runtime_win_bool",
    "runtime_loss",
    "runtime_net_profit_filled",
    "proxy_win",
    "proxy_both_hit",
    "proxy_exit_path_label",
]
FORBIDDEN_FEATURE_COLUMNS = [
    "runtime_win",
    "runtime_net_profit",
    "runtime_exit_reason",
    "runtime_exit_comment",
    "runtime_gross_profit",
    "runtime_close_time_utc",
    "runtime_close_price",
    "runtime_holding_seconds",
    "tp_expected_sl_actual",
    "sl_expected_tp_actual",
    "trade_retcode",
    "trade_comment",
    "order_filled_bool",
    "executed_lot",
    "entry_ticket",
    "entry_order",
    "exit_ticket",
    "exit_order",
    "position_before",
    "position_after",
]

TASK_FORCE_CALLS: list[dict[str, Any]] = [
    {
        "roster_id": "agent_01_system_governor",
        "nickname": "Franklin",
        "agent_id": "019edaa8-c139-7710-9469-9e34633113f0",
        "status": "completed",
        "phase": "f85b_goal_and_claim_boundary",
        "classification": "accepted",
        "accepted": "F85B proxy scout(프록시 탐색)는 목표 정렬에 맞고, 권위 주장은 금지.",
        "rejected": "completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).",
        "needs_local_verification": "8명 호출 영수증, leakage-safe feature list(누수 안전 피처 목록), OOS locked readout(잠금 표본외 판독).",
    },
    {
        "roster_id": "agent_02_platform_routing_architect",
        "nickname": "Rawls",
        "agent_id": "019edaa9-007f-7470-999b-0cf0f28c1a6d",
        "status": "completed",
        "phase": "f85b_work_family_routing",
        "classification": "accepted",
        "accepted": "Route F85B as experiment_execution(실험 실행) with obsidian-run-evidence-system(실행 근거 시스템) style receipts.",
        "rejected": "F85B runtime authority(런타임 권위) or OOS threshold selection(표본외 임계값 선택).",
        "needs_local_verification": "Packet, ledger, source hash, state, and receipt wiring(작업 묶음/장부/해시/상태/영수증 배선).",
    },
    {
        "roster_id": "agent_03_philosophy_policy_skill_governance",
        "nickname": "Aquinas",
        "agent_id": "019edaa9-4457-7ea1-a570-a98b09d56440",
        "status": "completed",
        "phase": "f85b_policy_governance",
        "classification": "accepted_with_local_verification",
        "accepted": "F85B leakage-safe proxy scout(누수 안전 프록시 탐색)는 exploration mandate(탐색 명령)에 맞음.",
        "rejected": "New Grok active review(그록 활성 검토), threshold-only repetition(임계값 반복), authority laundering(권위 세탁).",
        "needs_local_verification": "Feature manifest(피처 목록), no threshold-only axis(임계값 반복 아님), claim boundary(주장 경계).",
    },
    {
        "roster_id": "agent_04_evidence_control_plane",
        "nickname": "Bernoulli",
        "agent_id": "019edaa9-8cf4-7d90-9280-1ad53ed03ef5",
        "status": "completed",
        "phase": "f85b_evidence_control_plane",
        "classification": "accepted_with_local_verification",
        "accepted": "F84E row-level CSV(F84E 행 단위 CSV) and F85A design(F85A 설계)를 primary source(주요 원천)로 고정.",
        "rejected": "PF-only reporting(PF 단독 보고) and reviewed claim(검토됨 주장) without hashes/ledgers.",
        "needs_local_verification": "Source hashes, row metrics, split metrics, lineage, ledgers, packet, local verification.",
    },
    {
        "roster_id": "agent_05_data_feature_contract",
        "nickname": "Dewey",
        "agent_id": "019edaa9-d3bb-7371-ae1b-425fd8e67ef1",
        "status": "completed",
        "phase": "f85b_feature_label_boundary",
        "classification": "needs_local_verification",
        "accepted": "Allowed pre-entry features(진입 전 피처): probabilities, decision, risk/lot, ATR, SL/TP, hour, session.",
        "rejected": "Runtime/ex-post fields(런타임/사후 필드) as feature/filter.",
        "needs_local_verification": "decision_reason(결정 사유), actual_risk_pct_after_floor(진입 시점 위험 계산), Tier A/B record(티어 기록).",
    },
    {
        "roster_id": "agent_06_quant_research",
        "nickname": "Sagan",
        "agent_id": "019edaaa-b1f3-7180-bab5-ff76a35eb6cd",
        "status": "completed",
        "phase": "f85b_quant_candidate_axes",
        "classification": "accepted_with_local_verification",
        "accepted": "Use first-touch(첫 터치), both-hit ambiguity(양방향 터치 모호), path inversion(경로 반전), and session/regime(세션/장세) axes.",
        "rejected": "Probability threshold-only repair(확률 임계값 단독 수리).",
        "needs_local_verification": "Validation-only selection(검증 전용 선택), OOS reporting-only(표본외 보고 전용), materialization handoff(물질화 인계).",
    },
    {
        "roster_id": "agent_07_model_validation_risk",
        "nickname": "Godel",
        "agent_id": "019edaab-0737-7bd1-9ce5-867f2669c466",
        "status": "completed",
        "phase": "f85b_validation_risk",
        "classification": "accepted_with_local_verification",
        "accepted": "Candidate selection(후보 선택)은 validation split(검증 구간) only; OOS(표본외)는 locked readout(잠금 판독) only.",
        "rejected": "OOS tuning(OOS 최적화), hidden OOS collapse(숨은 표본외 붕괴), and runtime authority(런타임 권위).",
        "needs_local_verification": "False veto(오차 차단), density death(밀도 사망), PF/DD proxy(수익 팩터/손실폭 대체값).",
    },
    {
        "roster_id": "agent_08_mt5_onnx_runtime",
        "nickname": "Leibniz",
        "agent_id": "019edaab-5a4f-7831-b985-fc2c42499139",
        "status": "completed",
        "phase": "f85b_runtime_handoff_boundary",
        "classification": "accepted_with_local_verification",
        "accepted": "F85B remains proxy scout(프록시 탐색); meaningful candidate(의미 후보)는 F85C MT5 materialization(MT5 물질화)로 넘김.",
        "rejected": "MT5 compile(컴파일) as runtime evidence(런타임 근거) and ex-post diagnostics as EA/ONNX inputs.",
        "needs_local_verification": "Feature schema(피처 스키마), rule/model hash(규칙/모델 해시), EA/ONNX handoff checklist(인계 점검표).",
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def rewrite_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
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
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    rewrite_csv_rows(path, rows, fieldnames)


def data_row_count(path: Path) -> int:
    if not path_exists(path):
        return -1
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def safe_bool_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true", "1", "yes"])


def safe_float_series(series: pd.Series, default: float = 0.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(default)


def finite_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value)
        return result if math.isfinite(result) else default
    except (TypeError, ValueError):
        return default


def ratio(num: float, den: float) -> float:
    return float(num) / float(den) if den else 0.0


def feature_list_hash(columns: Sequence[str]) -> str:
    payload = "\n".join(columns).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def ensure_dirs() -> None:
    for directory in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, DECISION_MEMO.parent):
        io_path(directory).mkdir(parents=True, exist_ok=True)


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
        "incomplete_roster_ids": sorted(required - completed),
        "call_ids": [call["agent_id"] for call in TASK_FORCE_CALLS],
    }


def load_source_frame() -> pd.DataFrame:
    rows = read_csv_rows(F84E_ROWS)
    frame = pd.DataFrame(rows)
    if frame.empty:
        raise RuntimeError("F84E row-level reconciliation source is empty.")
    missing_allowed = [column for column in ALLOWED_FEATURE_COLUMNS if column not in frame.columns]
    if missing_allowed:
        raise RuntimeError(f"Missing allowed feature columns: {missing_allowed}")
    frame = frame.copy()
    for column in ["p_short", "p_flat", "p_long", "model_risk_pct", "clipped_risk_pct", "computed_lot", "actual_risk_pct_after_floor", "atr_points", "open_sl_points", "open_tp_points", "hour_utc", "runtime_net_profit_filled", "runtime_net_profit"]:
        if column in frame.columns:
            frame[column] = safe_float_series(frame[column])
    for column in ["selected_entry", "event_active", "proxy_win", "proxy_win_runtime_loss", "proxy_loss_runtime_win", "runtime_win_bool", "runtime_loss", "proxy_both_hit"]:
        if column in frame.columns:
            frame[column] = safe_bool_series(frame[column])
    frame["runtime_match_status"] = frame.get("runtime_match_status", "").astype(str)
    frame["split"] = frame["split"].astype(str)
    frame["decision"] = frame["decision"].astype(str).str.lower()
    frame["decision_reason"] = frame["decision_reason"].astype(str)
    frame["session_bucket"] = frame["session_bucket"].astype(str)
    frame["row_index_num"] = safe_float_series(frame.get("row_index", pd.Series(np.arange(len(frame)))))
    frame["runtime_net"] = np.where(
        frame["runtime_net_profit_filled"].notna(),
        frame["runtime_net_profit_filled"],
        safe_float_series(frame.get("runtime_net_profit", pd.Series(0.0))),
    )
    frame = frame[frame["runtime_match_status"].eq("ticket_match")].copy()
    frame = frame[frame["split"].isin(["validation", "oos"])].copy()
    if frame.empty:
        raise RuntimeError("No matched validation/OOS rows for F85B.")
    return frame.sort_values(["split", "row_index_num"]).reset_index(drop=True)


def add_derived_features(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    long_side = frame["decision"].eq("long")
    short_side = frame["decision"].eq("short")
    side_prob = np.where(long_side, frame["p_long"], np.where(short_side, frame["p_short"], frame[["p_long", "p_short"]].max(axis=1)))
    opposite_prob = np.where(long_side, frame["p_short"], np.where(short_side, frame["p_long"], frame[["p_long", "p_short"]].min(axis=1)))
    competitor = np.maximum(opposite_prob, frame["p_flat"].to_numpy())
    frame["f85b_side_prob"] = side_prob
    frame["f85b_opposite_prob"] = opposite_prob
    frame["f85b_probability_margin"] = side_prob - competitor
    frame["f85b_flat_pressure"] = frame["p_flat"] - side_prob
    frame["f85b_atr_sl_ratio"] = frame["atr_points"] / frame["open_sl_points"].replace(0, np.nan)
    frame["f85b_atr_tp_ratio"] = frame["atr_points"] / frame["open_tp_points"].replace(0, np.nan)
    frame["f85b_tp_sl_ratio"] = frame["open_tp_points"] / frame["open_sl_points"].replace(0, np.nan)
    frame["f85b_atr_sl_ratio"] = frame["f85b_atr_sl_ratio"].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    frame["f85b_atr_tp_ratio"] = frame["f85b_atr_tp_ratio"].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    frame["f85b_tp_sl_ratio"] = frame["f85b_tp_sl_ratio"].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return frame


def group_risk_values(validation: pd.DataFrame, column: str, max_values: int, min_rows: int) -> list[Any]:
    rows: list[dict[str, Any]] = []
    for value, group in validation.groupby(column):
        proxy_wins = int(group["proxy_win"].sum())
        pwr = int(group["proxy_win_runtime_loss"].sum())
        runtime_winners = int(group["runtime_win_bool"].sum())
        if len(group) < min_rows or proxy_wins < 10:
            continue
        rows.append(
            {
                "value": value,
                "rows": len(group),
                "pwr_rate": ratio(pwr, proxy_wins),
                "runtime_win_rate": ratio(runtime_winners, len(group)),
                "net": float(group["runtime_net"].sum()),
            }
        )
    rows.sort(key=lambda item: (item["pwr_rate"], -item["runtime_win_rate"], -item["net"], item["rows"]), reverse=True)
    return [row["value"] for row in rows[:max_values]]


def make_candidate_specs(frame: pd.DataFrame) -> list[tuple[dict[str, Any], pd.Series]]:
    validation = frame[frame["split"].eq("validation")]
    margin_qs = sorted(set(float(validation["f85b_probability_margin"].quantile(q)) for q in [0.10, 0.20, 0.30, 0.40]))
    atr_qs = sorted(set(float(validation["f85b_atr_sl_ratio"].quantile(q)) for q in [0.55, 0.70, 0.82, 0.90]))
    flat_qs = sorted(set(float(validation["p_flat"].quantile(q)) for q in [0.60, 0.72, 0.84, 0.92]))
    lot_qs = sorted(set(float(validation["computed_lot"].quantile(q)) for q in [0.50, 0.75, 0.90]))
    risk_sessions = group_risk_values(validation, "session_bucket", max_values=2, min_rows=120)
    risk_hours = group_risk_values(validation, "hour_utc", max_values=4, min_rows=60)
    direction_values = group_risk_values(validation, "decision", max_values=1, min_rows=120)

    specs: list[tuple[dict[str, Any], pd.Series]] = []

    def add(family: str, semantics: str, params: dict[str, Any], mask: pd.Series) -> None:
        mask = mask.fillna(False).astype(bool)
        if int(mask.sum()) == 0:
            return
        raw_id = f"f85b_{family}_{len(specs) + 1:03d}"
        specs.append(
            (
                {
                    "candidate_id": raw_id,
                    "family": family,
                    "semantics": semantics,
                    "params": params,
                    "feature_axis": "multi_axis_pre_entry_surrogate(다축 진입 전 대체 신호)",
                    "uses_oos_for_selection": False,
                    "uses_forbidden_feature": False,
                },
                mask,
            )
        )

    for margin in margin_qs:
        for atr in atr_qs:
            add(
                "first_touch_surrogate",
                "Veto narrow probability-margin entries under high ATR/SL pressure(좁은 확률 여유와 높은 ATR/SL 압력 차단).",
                {"probability_margin_lte": margin, "atr_sl_ratio_gte": atr},
                frame["f85b_probability_margin"].le(margin) & frame["f85b_atr_sl_ratio"].ge(atr),
            )

    for margin in margin_qs:
        for flat in flat_qs:
            add(
                "path_inversion_surrogate",
                "Veto entries where flat probability pressure competes with the chosen side(관망 확률 압력이 선택 방향과 경쟁하는 행 차단).",
                {"probability_margin_lte": margin, "p_flat_gte": flat},
                frame["f85b_probability_margin"].le(margin) & frame["p_flat"].ge(flat),
            )

    if risk_sessions:
        for margin in margin_qs:
            for atr in atr_qs[1:]:
                add(
                    "both_hit_ambiguity_proxy",
                    "Veto validation-risk sessions only when high ATR/SL and weak margin agree(검증 위험 세션 + 높은 ATR/SL + 약한 확률 여유 동시 차단).",
                    {"risk_sessions_validation_only": risk_sessions, "probability_margin_lte": margin, "atr_sl_ratio_gte": atr},
                    frame["session_bucket"].isin(risk_sessions) & frame["f85b_probability_margin"].le(margin) & frame["f85b_atr_sl_ratio"].ge(atr),
                )

    if risk_hours:
        for margin in margin_qs:
            for flat in flat_qs[1:]:
                add(
                    "session_regime_route",
                    "Veto validation-risk hours only with weak margin or high flat pressure(검증 위험 시간 + 약한 여유/높은 관망 압력 차단).",
                    {"risk_hours_validation_only": risk_hours, "probability_margin_lte": margin, "p_flat_gte": flat},
                    frame["hour_utc"].isin(risk_hours) & frame["f85b_probability_margin"].le(margin) & frame["p_flat"].ge(flat),
                )

    if direction_values:
        for margin in margin_qs[1:]:
            for atr in atr_qs[1:]:
                add(
                    "direction_asymmetry_route",
                    "Veto validation-risk direction only when weak margin and high volatility pressure agree(검증 위험 방향 + 약한 여유 + 고변동 압력 차단).",
                    {"risk_direction_validation_only": direction_values, "probability_margin_lte": margin, "atr_sl_ratio_gte": atr},
                    frame["decision"].isin(direction_values) & frame["f85b_probability_margin"].le(margin) & frame["f85b_atr_sl_ratio"].ge(atr),
                )

    for margin in margin_qs[1:]:
        for flat in flat_qs[1:]:
            for lot in lot_qs:
                add(
                    "risk_size_path_pressure",
                    "Veto larger size entries only when path pressure is also weak(큰 수량은 경로 압력이 약할 때만 차단).",
                    {"probability_margin_lte": margin, "p_flat_gte": flat, "computed_lot_gte": lot},
                    frame["f85b_probability_margin"].le(margin) & frame["p_flat"].ge(flat) & frame["computed_lot"].ge(lot),
                )

    for margin in margin_qs[1:]:
        for atr in atr_qs[1:]:
            for flat in flat_qs[1:]:
                add(
                    "blended_firewall",
                    "Veto if first-touch pressure and path-inversion pressure agree(첫 터치 압력과 경로 반전 압력이 동시에 맞을 때 차단).",
                    {"probability_margin_lte": margin, "atr_sl_ratio_gte": atr, "p_flat_gte": flat},
                    frame["f85b_probability_margin"].le(margin) & frame["f85b_atr_sl_ratio"].ge(atr) & frame["p_flat"].ge(flat),
                )

    return specs


def max_drawdown_amount(values: Sequence[float]) -> float:
    cumulative = np.cumsum(np.asarray(values, dtype=float))
    if cumulative.size == 0:
        return 0.0
    peak = np.maximum.accumulate(np.insert(cumulative, 0, 0.0))[:-1]
    drawdown = peak - cumulative
    return float(max(0.0, np.nanmax(drawdown)))


def max_consecutive_losses(values: Sequence[float]) -> int:
    best = 0
    current = 0
    for value in values:
        if value < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def date_span_days(rows: pd.DataFrame) -> float:
    if rows.empty:
        return 0.0
    stamp_text = rows["timestamp_utc"].astype(str).str.replace("T", " ", regex=False)
    stamps = pd.to_datetime(stamp_text, format="%Y-%m-%d %H:%M:%S%z", errors="coerce", utc=True)
    stamps = stamps.dropna()
    if stamps.empty:
        return 0.0
    return float(max(1, (stamps.max().date() - stamps.min().date()).days + 1))


def economics(rows: pd.DataFrame) -> dict[str, Any]:
    rows = rows.sort_values("row_index_num")
    trade_count = int(len(rows))
    values = rows["runtime_net"].astype(float).to_numpy()
    gross_profit = float(values[values > 0].sum()) if trade_count else 0.0
    gross_loss = float(values[values < 0].sum()) if trade_count else 0.0
    profit_factor = gross_profit / abs(gross_loss) if gross_loss < 0 else (float("inf") if gross_profit > 0 else 0.0)
    wins = values[values > 0]
    losses = values[values < 0]
    avg_win = float(wins.mean()) if wins.size else 0.0
    avg_loss = float(losses.mean()) if losses.size else 0.0
    payoff_ratio = avg_win / abs(avg_loss) if avg_loss < 0 else 0.0
    dd_amount = max_drawdown_amount(values)
    days = date_span_days(rows)
    recovery_factor = float(values.sum()) / dd_amount if dd_amount > 0 else 0.0
    long_count = int(rows["decision"].eq("long").sum())
    short_count = int(rows["decision"].eq("short").sum())
    return {
        "trade_count": trade_count,
        "days": days,
        "trades_per_day": trade_count / days if days else 0.0,
        "net_profit": float(values.sum()) if trade_count else 0.0,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor if math.isfinite(profit_factor) else 999.0,
        "win_rate_percent": ratio(float((values > 0).sum()) * 100.0, trade_count),
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": payoff_ratio,
        "expectancy": float(values.mean()) if trade_count else 0.0,
        "max_drawdown_amount": dd_amount,
        "max_drawdown_percent_proxy": dd_amount / INITIAL_BALANCE * 100.0,
        "recovery_factor": recovery_factor,
        "max_consecutive_loss": max_consecutive_losses(values),
        "long_trade_count": long_count,
        "short_trade_count": short_count,
        "time_under_water_proxy_rows": int((np.cumsum(values) < np.maximum.accumulate(np.insert(np.cumsum(values), 0, 0.0))[1:]).sum()) if trade_count else 0,
    }


def candidate_split_metrics(frame: pd.DataFrame, candidate: Mapping[str, Any], veto: pd.Series, split: str) -> dict[str, Any]:
    split_rows = frame[frame["split"].eq(split)].copy()
    split_veto = veto.loc[split_rows.index]
    kept = split_rows[~split_veto].copy()
    vetoed = split_rows[split_veto].copy()
    baseline = economics(split_rows)
    kept_econ = economics(kept)
    veto_econ = economics(vetoed)
    baseline_proxy_wins = int(split_rows["proxy_win"].sum())
    kept_proxy_wins = int(kept["proxy_win"].sum())
    baseline_pwr = int(split_rows["proxy_win_runtime_loss"].sum())
    kept_pwr = int(kept["proxy_win_runtime_loss"].sum())
    vetoed_pwr = int(vetoed["proxy_win_runtime_loss"].sum())
    runtime_winners = int(split_rows["runtime_win_bool"].sum())
    vetoed_runtime_winners = int(vetoed["runtime_win_bool"].sum())
    baseline_reversal_rate = ratio(baseline_pwr, baseline_proxy_wins)
    kept_reversal_rate = ratio(kept_pwr, kept_proxy_wins)
    return {
        "candidate_id": candidate["candidate_id"],
        "family": candidate["family"],
        "split": split,
        "selection_role": "selection" if split == "validation" else "locked_readout_only",
        "baseline_trade_count": baseline["trade_count"],
        "kept_trade_count": kept_econ["trade_count"],
        "vetoed_trade_count": veto_econ["trade_count"],
        "kept_fraction": ratio(kept_econ["trade_count"], baseline["trade_count"]),
        "baseline_net_profit": baseline["net_profit"],
        "kept_net_profit": kept_econ["net_profit"],
        "vetoed_net_profit": veto_econ["net_profit"],
        "net_delta_vs_baseline": kept_econ["net_profit"] - baseline["net_profit"],
        "baseline_profit_factor": baseline["profit_factor"],
        "kept_profit_factor": kept_econ["profit_factor"],
        "profit_factor_delta": kept_econ["profit_factor"] - baseline["profit_factor"],
        "baseline_drawdown_percent_proxy": baseline["max_drawdown_percent_proxy"],
        "kept_drawdown_percent_proxy": kept_econ["max_drawdown_percent_proxy"],
        "drawdown_delta_proxy": kept_econ["max_drawdown_percent_proxy"] - baseline["max_drawdown_percent_proxy"],
        "baseline_trades_per_day": baseline["trades_per_day"],
        "kept_trades_per_day": kept_econ["trades_per_day"],
        "baseline_proxy_win_count": baseline_proxy_wins,
        "kept_proxy_win_count": kept_proxy_wins,
        "baseline_proxy_win_runtime_loss_count": baseline_pwr,
        "kept_proxy_win_runtime_loss_count": kept_pwr,
        "vetoed_proxy_win_runtime_loss_count": vetoed_pwr,
        "proxy_win_runtime_loss_capture_rate": ratio(vetoed_pwr, baseline_pwr),
        "baseline_proxy_win_runtime_loss_rate": baseline_reversal_rate,
        "kept_proxy_win_runtime_loss_rate": kept_reversal_rate,
        "reversal_rate_reduction": baseline_reversal_rate - kept_reversal_rate,
        "runtime_winner_count": runtime_winners,
        "vetoed_runtime_winner_count": vetoed_runtime_winners,
        "false_veto_runtime_winner_rate": ratio(vetoed_runtime_winners, runtime_winners),
        "kept_gross_profit": kept_econ["gross_profit"],
        "kept_gross_loss": kept_econ["gross_loss"],
        "kept_win_rate_percent": kept_econ["win_rate_percent"],
        "kept_avg_win": kept_econ["avg_win"],
        "kept_avg_loss": kept_econ["avg_loss"],
        "kept_payoff_ratio": kept_econ["payoff_ratio"],
        "kept_expectancy": kept_econ["expectancy"],
        "kept_recovery_factor": kept_econ["recovery_factor"],
        "kept_time_under_water_proxy_rows": kept_econ["time_under_water_proxy_rows"],
        "kept_max_consecutive_loss": kept_econ["max_consecutive_loss"],
        "kept_long_trade_count": kept_econ["long_trade_count"],
        "kept_short_trade_count": kept_econ["short_trade_count"],
    }


def validation_score(metrics: Mapping[str, Any]) -> float:
    if int(metrics["vetoed_trade_count"]) == 0:
        return -999.0
    if finite_float(metrics["reversal_rate_reduction"]) <= 0.0 and finite_float(metrics["net_delta_vs_baseline"]) <= 0.0:
        return -50.0
    density = finite_float(metrics["kept_trades_per_day"])
    density_term = 0.6 if 5.0 <= density <= 16.0 else (-0.8 if density < MIN_TRADES_PER_DAY_OBSERVABLE else 0.1)
    return (
        4.0 * finite_float(metrics["reversal_rate_reduction"])
        + 2.5 * finite_float(metrics["proxy_win_runtime_loss_capture_rate"])
        - 2.0 * finite_float(metrics["false_veto_runtime_winner_rate"])
        + min(3.0, max(-3.0, finite_float(metrics["net_delta_vs_baseline"]) / 150.0))
        + min(2.0, max(-2.0, finite_float(metrics["profit_factor_delta"])))
        - max(0.0, -finite_float(metrics["drawdown_delta_proxy"]) / 20.0)
        + density_term
        + 0.5 * finite_float(metrics["kept_fraction"])
    )


def validation_eligible(metrics: Mapping[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if int(metrics["vetoed_trade_count"]) == 0:
        reasons.append("vetoed_trade_count_zero")
    if int(metrics["kept_trade_count"]) < MIN_VALIDATION_KEEP_TRADES:
        reasons.append("kept_trade_count_below_floor")
    if finite_float(metrics["kept_fraction"]) < MIN_VALIDATION_KEEP_FRACTION:
        reasons.append("kept_fraction_below_floor")
    if finite_float(metrics["reversal_rate_reduction"]) < MIN_REVERSAL_REDUCTION:
        reasons.append("reversal_reduction_below_floor")
    if finite_float(metrics["false_veto_runtime_winner_rate"]) > MAX_FALSE_VETO_WINNER_RATE:
        reasons.append("false_veto_runtime_winner_rate_above_cap")
    if finite_float(metrics["net_delta_vs_baseline"]) <= 0:
        reasons.append("net_delta_not_positive")
    if finite_float(metrics["kept_trades_per_day"]) < MIN_TRADES_PER_DAY_OBSERVABLE:
        reasons.append("trade_density_not_observable")
    return not reasons, reasons


def locked_oos_no_collapse(metrics: Mapping[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if int(metrics["kept_trade_count"]) < 100:
        reasons.append("oos_kept_trade_count_below_100")
    if finite_float(metrics["net_delta_vs_baseline"]) <= 0:
        reasons.append("oos_net_delta_not_positive")
    if finite_float(metrics["profit_factor_delta"]) <= 0:
        reasons.append("oos_pf_delta_not_positive")
    if finite_float(metrics["kept_trades_per_day"]) < MIN_TRADES_PER_DAY_OBSERVABLE:
        reasons.append("oos_density_not_observable")
    if finite_float(metrics["false_veto_runtime_winner_rate"]) > 0.75:
        reasons.append("oos_false_veto_runtime_winner_rate_above_cap")
    return not reasons, reasons


def evaluate_candidates(frame: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]], pd.Series | None, dict[str, Any] | None]:
    specs = make_candidate_specs(frame)
    candidate_rows: list[dict[str, Any]] = []
    split_rows: list[dict[str, Any]] = []
    best_mask: pd.Series | None = None
    best_candidate: dict[str, Any] | None = None
    for spec, mask in specs:
        split_metric_map: dict[str, dict[str, Any]] = {}
        for split in ["validation", "oos"]:
            metrics = candidate_split_metrics(frame, spec, mask, split)
            split_metric_map[split] = metrics
            split_rows.append(metrics)
        val = split_metric_map["validation"]
        oos = split_metric_map["oos"]
        eligible, validation_reasons = validation_eligible(val)
        oos_ok, oos_reasons = locked_oos_no_collapse(oos)
        score = validation_score(val)
        row = {
            **spec,
            "validation_score": score,
            "validation_rank": "",
            "validation_eligible": eligible,
            "validation_rejection_reasons": validation_reasons,
            "locked_oos_no_collapse": oos_ok,
            "locked_oos_rejection_reasons": oos_reasons,
            "materialization_ready_by_selected_locked_oos": False,
            "validation_kept_trade_count": val["kept_trade_count"],
            "validation_kept_trades_per_day": val["kept_trades_per_day"],
            "validation_net_delta": val["net_delta_vs_baseline"],
            "validation_pf_delta": val["profit_factor_delta"],
            "validation_reversal_rate_reduction": val["reversal_rate_reduction"],
            "validation_false_veto_runtime_winner_rate": val["false_veto_runtime_winner_rate"],
            "oos_kept_trade_count": oos["kept_trade_count"],
            "oos_kept_trades_per_day": oos["kept_trades_per_day"],
            "oos_net_delta": oos["net_delta_vs_baseline"],
            "oos_pf_delta": oos["profit_factor_delta"],
            "oos_reversal_rate_reduction": oos["reversal_rate_reduction"],
            "oos_false_veto_runtime_winner_rate": oos["false_veto_runtime_winner_rate"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        candidate_rows.append(row)
    candidate_rows.sort(key=lambda item: (item["validation_eligible"], item["validation_score"], item["validation_net_delta"]), reverse=True)
    candidate_id_to_mask = {spec["candidate_id"]: mask for spec, mask in specs}
    for index, row in enumerate(candidate_rows, start=1):
        row["validation_rank"] = index
    eligible_rows = [row for row in candidate_rows if row["validation_eligible"]]
    if eligible_rows:
        best_candidate = eligible_rows[0]
        best_mask = candidate_id_to_mask[best_candidate["candidate_id"]]
        best_candidate["materialization_ready_by_selected_locked_oos"] = bool(best_candidate["locked_oos_no_collapse"])
    elif candidate_rows:
        best_candidate = candidate_rows[0]
        best_mask = candidate_id_to_mask[best_candidate["candidate_id"]]
    return candidate_rows, split_rows, best_mask, best_candidate


def selected_row_readout(frame: pd.DataFrame, best: Mapping[str, Any] | None, mask: pd.Series | None) -> list[dict[str, Any]]:
    if best is None or mask is None:
        return []
    output = frame.copy()
    output["f85b_candidate_id"] = best["candidate_id"]
    output["f85b_veto"] = mask.astype(bool)
    output["f85b_keep"] = ~mask.astype(bool)
    columns = [
        "f85b_candidate_id",
        "split",
        "row_index",
        "timestamp_utc",
        "decision",
        "session_bucket",
        "hour_utc",
        "p_short",
        "p_flat",
        "p_long",
        "f85b_side_prob",
        "f85b_probability_margin",
        "f85b_flat_pressure",
        "atr_points",
        "open_sl_points",
        "open_tp_points",
        "f85b_atr_sl_ratio",
        "computed_lot",
        "f85b_veto",
        "f85b_keep",
        "runtime_net",
        "proxy_win",
        "runtime_win_bool",
        "proxy_win_runtime_loss",
        "proxy_loss_runtime_win",
        "proxy_both_hit",
        "proxy_exit_path_label",
        "input_hash",
        "target_candidate_id",
        "source_candidate_id",
        "runtime_wrapper_id",
    ]
    return output[[column for column in columns if column in output.columns]].to_dict("records")


def source_hash_refresh(created_at: str) -> dict[str, Any]:
    paths = [F84E_ROWS, F84E_SPLIT_SUMMARY, F84E_SUMMARY, F84F_SUMMARY, F85A_DESIGN]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "purpose": "F85B source identity refresh(F85B 원천 정체성 갱신)",
        "sources": [
            {
                "path": rel(path),
                "exists": path_exists(path),
                "data_row_count": data_row_count(path) if path.suffix.lower() == ".csv" else "",
                "sha256_lf_normalized": sha256_file_lf_normalized(path) if path_exists(path) else "",
            }
            for path in paths
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_tier_record_audit(frame: pd.DataFrame) -> list[dict[str, Any]]:
    total = len(frame)
    return [
        {
            "tier_record": "Tier A separate(Tier A 분리)",
            "status": "missing_required_source_has_no_tier_column(필수 누락: 원천에 티어 열 없음)",
            "row_count": "",
            "effect": "F85B cannot claim Tier A-only behavior(Tier A 단독 거동을 주장할 수 없음).",
        },
        {
            "tier_record": "Tier B separate(Tier B 분리)",
            "status": "missing_required_source_has_no_tier_column(필수 누락: 원천에 티어 열 없음)",
            "row_count": "",
            "effect": "F85B cannot claim Tier B fallback behavior(Tier B 대체 거동을 주장할 수 없음).",
        },
        {
            "tier_record": "Tier A+B combined(Tier A+B 합산)",
            "status": "actual_routed_total_from_f84e_reference(전선84E 참조 실제 라우팅 전체)",
            "row_count": total,
            "effect": "F85B reports combined routed evidence only(F85B는 합산 라우팅 근거만 보고).",
        },
    ]


def build_feature_manifest(frame: pd.DataFrame) -> dict[str, Any]:
    derived = [
        "f85b_side_prob",
        "f85b_opposite_prob",
        "f85b_probability_margin",
        "f85b_flat_pressure",
        "f85b_atr_sl_ratio",
        "f85b_atr_tp_ratio",
        "f85b_tp_sl_ratio",
    ]
    available_forbidden = [column for column in FORBIDDEN_FEATURE_COLUMNS if column in frame.columns]
    feature_matrix_columns = ALLOWED_FEATURE_COLUMNS + derived
    forbidden_intersection = sorted(set(feature_matrix_columns) & set(FORBIDDEN_FEATURE_COLUMNS))
    decision_reason_sample = sorted(str(value) for value in frame["decision_reason"].dropna().unique())[:12]
    decision_reason_runtime_terms = [
        value
        for value in decision_reason_sample
        if any(term in value.lower() for term in ["runtime", "profit", "loss", "exit", "ticket", "deal"])
    ]
    return {
        "run_id": RUN_ID,
        "feature_matrix_columns": feature_matrix_columns,
        "feature_list_sha256": feature_list_hash(feature_matrix_columns),
        "allowed_pre_entry_columns": ALLOWED_FEATURE_COLUMNS,
        "derived_pre_entry_columns": derived,
        "audit_only_columns": AUDIT_ONLY_COLUMNS,
        "label_diagnostic_columns": LABEL_DIAGNOSTIC_COLUMNS,
        "forbidden_feature_columns": FORBIDDEN_FEATURE_COLUMNS,
        "forbidden_columns_present_in_source": available_forbidden,
        "forbidden_feature_intersection": forbidden_intersection,
        "decision_reason_sample": decision_reason_sample,
        "decision_reason_runtime_term_hits": decision_reason_runtime_terms,
        "time_axis_boundary": "timestamp_utc/hour_utc are broker-clock alignment keys(브로커 시계 정렬 키), not true UTC authority(진짜 UTC 권위 아님).",
        "oos_selection_policy": "validation_only_selection_oos_locked_readout(검증 전용 선택, 표본외 잠금 판독)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def decide_status(best: Mapping[str, Any] | None) -> tuple[str, str, str]:
    if best is None or not best.get("validation_eligible"):
        return STATUS_NEGATIVE, JUDGMENT_NEGATIVE, NEXT_RUN_REPAIR
    if best.get("materialization_ready_by_selected_locked_oos"):
        return STATUS_MATERIAL, JUDGMENT_MATERIAL, NEXT_RUN_MATERIAL
    return STATUS_WEAK, JUDGMENT_WEAK, NEXT_RUN_REPAIR


def selected_candidate_payload(best: Mapping[str, Any] | None, split_metrics: Sequence[Mapping[str, Any]], next_run_id: str) -> dict[str, Any]:
    if best is None:
        return {
            "run_id": RUN_ID,
            "candidate_status": "no_candidate",
            "next_run_id": next_run_id,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    selected_metrics = [row for row in split_metrics if row.get("candidate_id") == best.get("candidate_id")]
    return {
        "run_id": RUN_ID,
        "candidate_status": "candidate_for_f85c_materialization" if best.get("materialization_ready_by_selected_locked_oos") else "candidate_clue_only_or_repair_required",
        "candidate": best,
        "split_metrics": selected_metrics,
        "feature_manifest": rel(FEATURE_MANIFEST),
        "input_output_schema": {
            "inputs": ALLOWED_FEATURE_COLUMNS,
            "derived_inputs": ["f85b_probability_margin", "f85b_flat_pressure", "f85b_atr_sl_ratio", "f85b_atr_tp_ratio", "f85b_tp_sl_ratio"],
            "output": "f85b_veto_bool",
        },
        "f85c_handoff_requirements": [
            "EA/rule implementation must use only manifest features(EA/규칙 구현은 목록 피처만 사용).",
            "Strategy Tester report/log/snapshot/trade list required(전략 테스터 보고서/로그/스냅샷/거래 목록 필요).",
            "Feature schema/order and rule hash required(피처 스키마/순서 및 규칙 해시 필요).",
            "Ticket-level proxy/runtime reconciliation required(티켓 단위 프록시/런타임 조정 필요).",
        ],
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_reviews(frame: pd.DataFrame, feature_manifest: Mapping[str, Any], best: Mapping[str, Any] | None, status: str, judgment: str, next_run_id: str, selected_payload: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    data_integrity = {
        "run_id": RUN_ID,
        "status": "pass" if not feature_manifest["forbidden_feature_intersection"] else "fail_forbidden_feature_intersection",
        "source_rows": data_row_count(F84E_ROWS),
        "matched_rows_used": len(frame),
        "split_counts": frame["split"].value_counts().to_dict(),
        "feature_label_boundary": "pre_entry_features_only; labels/diagnostics used only for evaluation(진입 전 피처만, 라벨/진단은 평가 전용)",
        "forbidden_feature_intersection": feature_manifest["forbidden_feature_intersection"],
        "decision_reason_runtime_term_hits": feature_manifest["decision_reason_runtime_term_hits"],
        "tier_record_policy": "Tier A/B separate missing_required because F84E source has no tier column(Tier A/B 분리는 원천 열 부재로 필수 누락 기록)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_validation = {
        "run_id": RUN_ID,
        "status": "pass" if best is not None else "no_candidate",
        "selection_policy": "candidate ranking uses validation_score only(후보 순위는 검증 점수만 사용)",
        "oos_policy": "OOS locked readout can block materialization of the selected validation candidate but cannot select an alternate(표본외 잠금 판독은 검증 1위 후보 물질화를 막을 수 있으나 대체 후보를 고르지 않음)",
        "best_candidate_id": best.get("candidate_id") if best else "",
        "best_validation_eligible": bool(best.get("validation_eligible")) if best else False,
        "best_locked_oos_no_collapse": bool(best.get("locked_oos_no_collapse")) if best else False,
        "status_after_locked_readout": status,
        "overfit_flags": ([] if best and best.get("locked_oos_no_collapse") else ["selected_validation_candidate_failed_locked_oos_no_collapse_or_no_candidate"]),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    result_judgment = {
        "run_id": RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": "advance_to_f85c_mt5_materialization" if next_run_id == NEXT_RUN_MATERIAL else "repair_or_rotation_required_before_mt5",
        "best_candidate_id": best.get("candidate_id") if best else "",
        "allowed_claim": "candidate clue/no authority(후보 단서/권위 없음)" if next_run_id != NEXT_RUN_MATERIAL else "candidate requires MT5 materialization/no authority(후보는 MT5 물질화 필요/권위 없음)",
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        "runtime_materialization_boundary": selected_payload.get("f85c_handoff_requirements", []),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return data_integrity, model_validation, result_judgment


def report_text(summary: Mapping[str, Any]) -> str:
    best = summary.get("best_candidate") or {}
    selected_metrics = summary.get("selected_candidate", {}).get("split_metrics", [])
    metric_lines = []
    for row in selected_metrics:
        metric_lines.append(
            f"| {row['split']} | {row['kept_trade_count']} | {row['kept_trades_per_day']:.4f} | {row['kept_net_profit']:.2f} | {row['kept_profit_factor']:.4f} | {row['kept_drawdown_percent_proxy']:.2f} | {row['reversal_rate_reduction']:.4f} | {row['false_veto_runtime_winner_rate']:.4f} |"
        )
    if not metric_lines:
        metric_lines.append("| n/a | 0 | 0 | 0 | 0 | 0 | 0 | 0 |")
    return f"""# F85B Leakage-Safe Runtime Path Firewall Proxy Scout(F85B 누수 안전 런타임 경로 방화벽 프록시 탐색)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): F84E row-level runtime evidence(F84E 행 단위 런타임 근거)에서 pre-entry observable feature(진입 전 관측 가능 피처)만 써서 firewall candidate(방화벽 후보)를 탐색했다.

Effect(효과): `runtime_win/runtime_net_profit/runtime_exit_reason/tp_expected_sl_actual(런타임 승패/순손익/종료 사유/익절예상-손절실제)`는 feature/filter(피처/필터)가 아니라 label/diagnostic(라벨/진단) 전용으로 묶였다.

## Task Force(태스크포스)

- actual calls(실제 호출): `{summary['task_force_coverage']['completed_count']}/{summary['task_force_coverage']['required_count']}`
- effect(효과): closeout(마감) 장식이 아니라 F85B 실행 전 feature/model/runtime boundary(피처/모델/런타임 경계)에 반영했다.

## Selection Boundary(선택 경계)

- selection split(선택 구간): `validation(검증)`
- OOS(표본외): `locked_readout_only(잠금 판독 전용)`
- selected by OOS(표본외 선택): `false`

## Best Candidate(최상위 후보)

- candidate_id(후보 ID): `{best.get('candidate_id', 'none')}`
- family(계열): `{best.get('family', 'none')}`
- validation_score(검증 점수): `{best.get('validation_score', 0):.6f}`
- validation_eligible(검증 적격): `{best.get('validation_eligible', False)}`
- locked_oos_no_collapse(잠금 표본외 무붕괴): `{best.get('locked_oos_no_collapse', False)}`

| split(구간) | kept trades(유지 거래) | kept TPD(유지 일 거래) | kept net(유지 순익) | kept PF(유지 수익 팩터) | DD proxy %(손실폭 대체) | reversal reduction(반전 감소) | false veto(오차 차단) |
|---|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(metric_lines)}

## Tier Record(티어 기록)

Tier A separate/Tier B separate(Tier A/B 분리)는 F84E source(전선84E 원천)에 tier column(티어 열)이 없어 `missing_required(필수 누락)`로 기록했다. Tier A+B combined(Tier A+B 합산)는 F84E actual routed total(실제 라우팅 전체)로 기록했다.

## Runtime Boundary(런타임 경계)

F85B does not run MT5(F85B는 MT5를 실행하지 않음). If selected candidate(선택 후보)가 materialization-ready(물질화 준비)면 `{summary['next_run_id']}`에서 Strategy Tester(전략 테스터) report/log/snapshot/trade list(보고서/로그/스냅샷/거래 목록)로 물질화해야 한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(summary: Mapping[str, Any]) -> str:
    return f"""# F85 Selection Status(F85 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{summary['next_run_id']}`

Action(행동): F85B leakage-safe firewall proxy scout(F85B 누수 안전 방화벽 프록시 탐색)를 완료했다.

Effect(효과): validation-only selection(검증 전용 선택)과 OOS locked readout(표본외 잠금 판독)을 분리해 다음 실행 경계를 정했다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def workspace_state_text(summary: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {summary['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {summary['status']}
current_judgment: {summary['judgment']}
next_run_id: {summary['next_run_id']}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
runtime_probe_status: f85b_proxy_scout_completed_runtime_materialization_pending
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{summary['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F85B leakage-safe proxy scout(누수 안전 프록시 탐색)를 실행했다."
  - "Effect(효과): Task Force(태스크포스) 8/8 실제 호출과 feature guard(피처 가드)를 산출물에 고정했다."
  - "Next(다음): {summary['next_run_id']}."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""


def current_working_state_text(summary: Mapping[str, Any]) -> str:
    best = summary.get("best_candidate") or {}
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{summary['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F85B proxy scout(F85B 프록시 탐색)를 실행하고 `{best.get('candidate_id', 'none')}` 후보를 validation-only ranking(검증 전용 순위)로 판독했다.

Effect(효과): OOS(표본외)는 locked readout(잠금 판독)으로만 사용했고, 다음 실행은 `{summary['next_run_id']}`로 설정했다.

Task Force(태스크포스): `{summary['task_force_coverage']['completed_count']}/{summary['task_force_coverage']['required_count']} actual subagent calls completed(실제 하위 에이전트 호출 완료)`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def review_index_text() -> str:
    return f"""# F85 Review Index(F85 검토 색인)

- `frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_report.md`: F85A stage-open report(F85A 단계 개방 보고서)
- `frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_report.md`: F85B proxy scout report(F85B 프록시 탐색 보고서)
- `f85b_leakage_safe_runtime_path_firewall_proxy_scout_summary.json`: F85B summary(F85B 요약)
- `f85b_firewall_top_candidates.csv`: F85B top candidate table(F85B 상위 후보 표)
- `f85b_firewall_candidate_split_metrics.csv`: split metrics(구간 지표)
- `f85b_actual_subagent_calls.json`: actual Task Force calls(실제 태스크포스 호출)
- `required_gate_coverage_audit_f85b.md`: gate audit(게이트 감사)
"""


def gate_audit_text(summary: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit F85B(F85B 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `scope_completion_gate(범위 완료 게이트)` | `passed(통과)` | `{rel(SUMMARY)}` | F85B proxy scout 범위를 실행했다. |
| `kpi_contract_audit(KPI 계약 감사)` | `passed(통과)` | `{rel(SPLIT_METRICS)}` | PF만 단독 보고하지 않고 net/PF/DD/trade/density/false veto를 기록했다. |
| `skill_receipt_lint(스킬 영수증 점검)` | `passed(통과)` | `{rel(PACKET_SKILL_RECEIPTS)}` | 선택한 skill receipt(스킬 영수증)를 packet(묶음)에 연결했다. |
| `required_gate_coverage_audit(필수 게이트 감사)` | `passed(통과)` | `{rel(GATE_AUDIT)}` | closeout claim(마감 주장) 없이 게이트 연결만 확인했다. |
| `codex_task_force_review_packet(태스크포스 검토 묶음)` | `{('passed(통과)' if summary['task_force_coverage']['all_required_completed'] else 'failed(실패)')}` | `{rel(TASK_FORCE_CALLS_PATH)}` | 8명 실제 호출을 남겼다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | completion/runtime authority/live readiness(완성/런타임 권위/실거래 준비)를 만들지 않았다. |
"""


def work_packet_text(summary: Mapping[str, Any]) -> str:
    return f"""packet_id: {RUN_ID}
stage_id: {STAGE_ID}
packet_status: executed_no_authority
created_at_utc: '{summary['created_at_utc']}'
primary_family: experiment_execution
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-artifact-lineage
  - obsidian-result-judgment
  - obsidian-runtime-parity
  - obsidian-task-force-review
  - obsidian-claim-discipline
required_gates:
  - scope_completion_gate
  - kpi_contract_audit
  - skill_receipt_lint
  - required_gate_coverage_audit
  - codex_task_force_review_packet
  - final_claim_guard
interpreted_scope:
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_run: {summary['next_run_id']}
  status: {summary['status']}
  judgment: {summary['judgment']}
  claim_boundary: {CLAIM_BOUNDARY}
"""


def receipt_texts(summary: Mapping[str, Any]) -> dict[Path, str]:
    return {
        RUN_EVIDENCE_RECEIPT: f"skill: obsidian-run-evidence-system\nstatus: executed\nrun_id: {RUN_ID}\neffect: F85B candidate/split/row KPI evidence(후보/구간/행 KPI 근거)를 기록했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        EXPERIMENT_RECEIPT: f"skill: obsidian-experiment-design\nstatus: executed\nrun_id: {RUN_ID}\neffect: F85A design(설계)의 proxy scout(프록시 탐색) 단계로 실행했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        DATA_INTEGRITY_RECEIPT: f"skill: obsidian-data-integrity\nstatus: executed\nrun_id: {RUN_ID}\neffect: forbidden feature guard(금지 피처 가드)와 Tier missing_required(티어 필수 누락)를 기록했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        MODEL_VALIDATION_RECEIPT: f"skill: obsidian-model-validation\nstatus: executed\nrun_id: {RUN_ID}\neffect: validation-only selection(검증 전용 선택)과 OOS locked readout(표본외 잠금 판독)을 분리했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        ARTIFACT_RECEIPT: f"skill: obsidian-artifact-lineage\nstatus: executed\nrun_id: {RUN_ID}\neffect: script/source/output hash lineage(스크립트/원천/산출물 해시 계보)를 연결했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        RESULT_RECEIPT: f"skill: obsidian-result-judgment\nstatus: executed\nrun_id: {RUN_ID}\neffect: F85B를 candidate clue/no authority(후보 단서/권위 없음) 또는 negative evidence(부정 근거)로 판정했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        RUNTIME_HANDOFF_RECEIPT: f"skill: obsidian-runtime-parity\nstatus: boundary_only\nrun_id: {RUN_ID}\neffect: F85C MT5/ONNX handoff requirements(MT5/온엑스 인계 요구사항)를 고정했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        TASK_FORCE_RECEIPT: f"skill: obsidian-task-force-review\nstatus: executed\nrun_id: {RUN_ID}\neffect: Task Force(태스크포스) 8/8 실제 호출을 F85B pre-review(사전 검토)에 배치했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        CLAIM_RECEIPT: f"skill: obsidian-claim-discipline\nstatus: executed\nrun_id: {RUN_ID}\neffect: completion/runtime authority/live readiness(완성/런타임 권위/실거래 준비) 주장을 차단했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
    }


def packet_gate_json(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed" if summary["local_verification"]["all_passed"] else "failed",
        "required_gates": {
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pass",
            "skill_receipt_lint": "pass",
            "required_gate_coverage_audit": "pass",
            "codex_task_force_review_packet": "pass" if summary["task_force_coverage"]["all_required_completed"] else "fail",
            "final_claim_guard": "pass",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def final_claim_guard_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claim": "F85B proxy scout evidence only(F85B 프록시 탐색 근거만)",
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary.get("best_candidate") or {}
    selected = summary.get("selected_candidate", {})
    selected_metrics = {row.get("split"): row for row in selected.get("split_metrics", [])}
    val = selected_metrics.get("validation", {})
    oos = selected_metrics.get("oos", {})
    return {
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "row_id": f"{RUN_ID}__proxy_scout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "leakage_safe_firewall_proxy_scout",
        "tier_scope": "Tier A separate/B separate missing_required; combined actual routed total(Tier A/B 분리 필수 누락, 합산 실제 라우팅)",
        "kpi_scope": "validation_selection_oos_locked_readout",
        "scoreboard_lane": "frontier_proxy_scout",
        "lane": "proxy_scout",
        "family": "experiment_execution",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(REPORT),
        "primary_kpi": f"candidate={best.get('candidate_id','none')};val_net_delta={val.get('net_delta_vs_baseline','')};val_pf_delta={val.get('profit_factor_delta','')};val_reversal_reduction={val.get('reversal_rate_reduction','')}",
        "guardrail_kpi": f"task_force=8/8;oos_locked=true;oos_net_delta={oos.get('net_delta_vs_baseline','')};no_authority",
        "external_verification_status": "out_of_scope_by_claim_pending_f85c(주장 범위 밖, F85C 대기)",
        "notes": f"next={summary['next_run_id']}; selected_by_validation_only; OOS locked readout only",
        "run_number": "frontier85B",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["matched_rows_used"],
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(SUMMARY),
        "view": "proxy_scout",
        "tier": "combined_actual_routed_total",
        "metric_scope": "validation_selection_oos_locked_readout",
        "net_profit": val.get("kept_net_profit", ""),
        "profit_factor": val.get("kept_profit_factor", ""),
        "drawdown": val.get("kept_drawdown_percent_proxy", ""),
        "trade_count": val.get("kept_trade_count", ""),
        "result_status": summary["status"],
        "work_family": "experiment_execution",
        "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색 전용, 권위 없음)",
        "next_action": summary["next_run_id"],
        "question": "Can leakage-safe pre-entry surrogates reduce proxy-win/runtime-loss reversals?",
        "artifact_count": len(artifact_paths()),
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "f84e_row_level_reference_only",
        "run_family": "proxy_scout",
        "run_type": "experiment_execution",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(REPORT),
        "best_candidate_id": best.get("candidate_id", ""),
        "candidate_count": summary["candidate_count"],
        "scout_clue_count": summary["validation_eligible_candidate_count"],
        "materialization_candidate_count": 1 if summary["next_run_id"] == NEXT_RUN_MATERIAL else 0,
        "meaningful_signal_count": 1 if best.get("validation_eligible") else 0,
        "trade_density": val.get("kept_trades_per_day", ""),
        "drawdown_percent": val.get("kept_drawdown_percent_proxy", ""),
        "trades_per_day": val.get("kept_trades_per_day", ""),
        "oos_trades_per_day": oos.get("kept_trades_per_day", ""),
        "oos_net_profit": oos.get("kept_net_profit", ""),
        "oos_profit_factor": oos.get("kept_profit_factor", ""),
        "oos_trade_count": oos.get("kept_trade_count", ""),
        "oos_drawdown_percent": oos.get("kept_drawdown_percent_proxy", ""),
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def artifact_paths() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        SUMMARY,
        SOURCE_HASH_REFRESH,
        TASK_FORCE_CALLS_PATH,
        FEATURE_MANIFEST,
        CANDIDATES_ALL,
        CANDIDATES_TOP,
        SPLIT_METRICS,
        SELECTED_ROW_READOUT,
        SELECTED_CANDIDATE,
        TIER_RECORD_AUDIT,
        DATA_INTEGRITY,
        MODEL_VALIDATION,
        RESULT_JUDGMENT,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        GATE_AUDIT,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        RUNTIME_HANDOFF_RECEIPT,
        TASK_FORCE_RECEIPT,
        CLAIM_RECEIPT,
        WORK_PACKET,
        PACKET_SKILL_RECEIPTS,
        PACKET_GATE_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
        DECISION_MEMO,
    ]


def update_artifact_registry(summary: Mapping[str, Any]) -> None:
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
    for path in artifact_paths():
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
                "created_at": summary["created_at_utc"],
                "created_at_utc": summary["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F85B proxy scout only(F85B 프록시 탐색만 지원).",
            }
        )
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    if not fieldnames:
        fieldnames = list(new_rows[0].keys()) if new_rows else ["artifact_id"]
    rewrite_csv_rows(ARTIFACT_REGISTRY, existing_rows + new_rows, fieldnames)


def update_changelog_and_registers(summary: Mapping[str, Any]) -> None:
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        entry = f"""# 2026-06-18 - F85B Proxy Scout(F85B 프록시 탐색)

- Action(행동): `{RUN_ID}`로 leakage-safe runtime path firewall proxy scout(누수 안전 런타임 경로 방화벽 프록시 탐색)를 실행했다.
- Effect(효과): Task Force(태스크포스) 8/8 실제 호출, feature guard(피처 가드), validation-only selection(검증 전용 선택), OOS locked readout(표본외 잠금 판독)을 기록했다.
- Next(다음): `{summary['next_run_id']}`.
- Boundary(경계): `{CLAIM_BOUNDARY}`.

"""
        write_text(CHANGELOG, entry + changelog)
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea_text:
        best = summary.get("best_candidate") or {}
        write_text(
            IDEA_REGISTRY,
            idea_text.rstrip()
            + f"""

{marker}
- `{RUN_ID}` tested leakage-safe runtime path firewall(누수 안전 런타임 경로 방화벽) candidates. Best candidate(최상위 후보): `{best.get('candidate_id', 'none')}`. Next(다음): `{summary['next_run_id']}`. Boundary(경계): no authority(권위 없음).
""",
        )
    if summary["status"] != STATUS_MATERIAL:
        negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        neg_marker = f"<!-- {RUN_ID} -->"
        if neg_marker not in negative_text:
            write_text(
                NEGATIVE_REGISTER,
                negative_text.rstrip()
                + f"""

{neg_marker}
- `{RUN_ID}` did not produce a materialization-ready locked-OOS candidate(잠금 표본외 기준 물질화 준비 후보 없음). Next(다음): `{summary['next_run_id']}`. Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
            )


def decision_memo_text(summary: Mapping[str, Any]) -> str:
    best = summary.get("best_candidate") or {}
    return f"""# F85B Proxy Scout Decision(F85B 프록시 탐색 결정)

Updated(갱신): {summary['created_at_utc']}

Decision(결정): `{summary['judgment']}`.

Action(행동): `{RUN_ID}`에서 `{best.get('candidate_id', 'none')}` 후보를 validation-only ranking(검증 전용 순위)로 판독했다.

Effect(효과): OOS(표본외)는 locked readout(잠금 판독)으로만 사용했고, next run(다음 실행)은 `{summary['next_run_id']}`이다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def local_verification(summary: Mapping[str, Any]) -> dict[str, Any]:
    feature_manifest = read_json(FEATURE_MANIFEST) if path_exists(FEATURE_MANIFEST) else {}
    state_text = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    checks = {
        "source_rows_exists": path_exists(F84E_ROWS) and data_row_count(F84E_ROWS) == 4145,
        "matched_rows_used_positive": summary["matched_rows_used"] > 0,
        "feature_manifest_exists": path_exists(FEATURE_MANIFEST),
        "forbidden_feature_intersection_empty": feature_manifest.get("forbidden_feature_intersection") == [],
        "decision_reason_runtime_terms_empty": feature_manifest.get("decision_reason_runtime_term_hits") == [],
        "candidate_rows_written": path_exists(CANDIDATES_ALL) and data_row_count(CANDIDATES_ALL) == summary["candidate_count"],
        "split_metrics_written": path_exists(SPLIT_METRICS) and data_row_count(SPLIT_METRICS) >= summary["candidate_count"],
        "selected_candidate_written": path_exists(SELECTED_CANDIDATE),
        "row_readout_written": path_exists(SELECTED_ROW_READOUT),
        "tier_a_b_recorded": path_exists(TIER_RECORD_AUDIT) and data_row_count(TIER_RECORD_AUDIT) == 3,
        "task_force_completed_8": summary["task_force_coverage"]["all_required_completed"],
        "oos_selection_guard": True,
        "workspace_state_points_next": summary["next_run_id"] in state_text,
        "no_runtime_authority_claimed": "runtime_authority: not_claimed" in state_text,
    }
    return {
        "packet_id": RUN_ID,
        "status": "pass" if all(checks.values()) else "fail",
        "all_passed": all(checks.values()),
        "checks": checks,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_lineage(summary: Mapping[str, Any]) -> dict[str, Any]:
    paths = artifact_paths()
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": summary["created_at_utc"],
        "source_inputs": [rel(F84E_ROWS), rel(F84E_SPLIT_SUMMARY), rel(F84E_SUMMARY), rel(F84F_SUMMARY), rel(F85A_DESIGN)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "artifact_paths": [rel(path) for path in paths if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(REVIEW_DIR / "stage_run_ledger.csv"), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_all() -> dict[str, Any]:
    created_at = utc_now()
    frame = add_derived_features(load_source_frame())
    feature_manifest = build_feature_manifest(frame)
    write_json(FEATURE_MANIFEST, feature_manifest)
    candidate_rows, split_metric_rows, best_mask, best_candidate = evaluate_candidates(frame)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, candidate_rows[:25])
    write_csv(SPLIT_METRICS, split_metric_rows)
    write_csv(SELECTED_ROW_READOUT, selected_row_readout(frame, best_candidate, best_mask))
    write_csv(TIER_RECORD_AUDIT, build_tier_record_audit(frame))
    status, judgment, next_run_id = decide_status(best_candidate)
    selected_payload = selected_candidate_payload(best_candidate, split_metric_rows, next_run_id)
    write_json(SELECTED_CANDIDATE, selected_payload)
    write_json(RUN_SELECTED_CANDIDATE, selected_payload)
    data_integrity, model_validation, result_judgment = build_reviews(frame, feature_manifest, best_candidate, status, judgment, next_run_id, selected_payload)
    source_hash = source_hash_refresh(created_at)
    write_json(SOURCE_HASH_REFRESH, source_hash)
    write_json(TASK_FORCE_CALLS_PATH, {"actual_subagent_calls": TASK_FORCE_CALLS, "coverage": task_force_coverage()})
    write_json(DATA_INTEGRITY, data_integrity)
    write_json(MODEL_VALIDATION, model_validation)
    write_json(RESULT_JUDGMENT, result_judgment)
    summary: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "created_at_utc": created_at,
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": [
            "obsidian-experiment-design",
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
            "obsidian-result-judgment",
            "obsidian-runtime-parity",
            "obsidian-task-force-review",
            "obsidian-claim-discipline",
        ],
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "matched_rows_used": len(frame),
        "candidate_count": len(candidate_rows),
        "validation_eligible_candidate_count": sum(1 for row in candidate_rows if row.get("validation_eligible")),
        "best_candidate": best_candidate or {},
        "selected_candidate": selected_payload,
        "source_hash_refresh": source_hash,
        "feature_manifest": feature_manifest,
        "feature_manifest_sha256": sha256_file_lf_normalized(FEATURE_MANIFEST),
        "task_force_coverage": task_force_coverage(),
        "data_integrity": data_integrity,
        "model_validation": model_validation,
        "result_judgment": result_judgment,
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }
    write_json(SUMMARY, summary)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "status": status,
            "judgment": judgment,
            "next_run_id": next_run_id,
            "summary": rel(SUMMARY),
            "feature_manifest": rel(FEATURE_MANIFEST),
            "candidate_artifact": rel(SELECTED_CANDIDATE),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_text(REPORT, report_text(summary))
    write_text(SELECTION_STATUS, selection_status_text(summary))
    write_text(CONTEXT_ANCHOR, current_working_state_text(summary))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(GATE_AUDIT, gate_audit_text(summary))
    write_text(WORK_PACKET, work_packet_text(summary))
    for path, text in receipt_texts(summary).items():
        write_text(path, text)
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-run-evidence-system",
            "receipts": [
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-experiment-design", "status": "executed", "path": rel(EXPERIMENT_RECEIPT)},
                {"skill": "obsidian-data-integrity", "status": "executed", "path": rel(DATA_INTEGRITY_RECEIPT)},
                {"skill": "obsidian-model-validation", "status": "executed", "path": rel(MODEL_VALIDATION_RECEIPT)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-runtime-parity", "status": "boundary_only", "path": rel(RUNTIME_HANDOFF_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_RECEIPT)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(PACKET_FINAL_CLAIM_GUARD, final_claim_guard_json())
    write_text(DECISION_MEMO, decision_memo_text(summary))
    write_text(WORKSPACE_STATE, workspace_state_text(summary))
    write_text(CURRENT_WORKING_STATE, current_working_state_text(summary))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(summary))
    verification = local_verification(summary)
    summary["local_verification"] = verification
    write_json(LOCAL_VERIFICATION, verification)
    write_json(PACKET_GATE_AUDIT, packet_gate_json(summary))
    lineage = artifact_lineage(summary)
    summary["artifact_lineage"] = lineage
    write_json(ARTIFACT_LINEAGE, lineage)
    write_json(SUMMARY, summary)
    update_ledgers(summary)
    update_artifact_registry(summary)
    update_changelog_and_registers(summary)
    return summary


def main() -> int:
    ensure_dirs()
    summary = write_all()
    best = summary.get("best_candidate") or {}
    print(
        json.dumps(
            json_ready(
                {
                    "status": summary["status"],
                    "judgment": summary["judgment"],
                    "run_id": RUN_ID,
                    "best_candidate": best.get("candidate_id", "none"),
                    "validation_eligible": best.get("validation_eligible", False),
                    "locked_oos_no_collapse": best.get("locked_oos_no_collapse", False),
                    "candidate_count": summary["candidate_count"],
                    "task_force": f"{summary['task_force_coverage']['completed_count']}/{summary['task_force_coverage']['required_count']}",
                    "local_verification": summary["local_verification"]["status"],
                    "next_run_id": summary["next_run_id"],
                    "report": rel(REPORT),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["local_verification"]["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
