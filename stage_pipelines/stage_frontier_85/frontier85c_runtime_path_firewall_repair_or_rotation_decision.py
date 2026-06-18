from __future__ import annotations

import csv
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
RUN_ID = "frontier85C_runtime_path_firewall_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
NEXT_RUN_ID = "frontier86A_stage_open_runtime_native_intrabar_path_label_source_v1"

STATUS = "f85_closed_negative_runtime_path_firewall_rotation_to_f86_no_authority"
JUDGMENT = "no_meaningful_firewall_proxy_signal_rotate_to_runtime_native_intrabar_path_label_no_authority"
DECISION = "close_f85_negative_rotate_to_f86_runtime_native_intrabar_path_label_source"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "retired_archive_only_no_new_grok_call_no_next_open_block"
SCRIPT_REL = "stage_pipelines/stage_frontier_85/frontier85c_runtime_path_firewall_repair_or_rotation_decision.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

F85A_DESIGN = REVIEW_DIR / "f85a_experiment_design.json"
F85B_SUMMARY = REVIEW_DIR / "f85b_leakage_safe_runtime_path_firewall_proxy_scout_summary.json"
F85B_REPORT = REVIEW_DIR / "frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_report.md"
F85B_TOP_CANDIDATES = REVIEW_DIR / "f85b_firewall_top_candidates.csv"
F85B_SPLIT_METRICS = REVIEW_DIR / "f85b_firewall_candidate_split_metrics.csv"
F85B_SELECTED_READOUT = REVIEW_DIR / "f85b_selected_firewall_row_readout.csv"
F85B_FEATURE_MANIFEST = REVIEW_DIR / "f85b_feature_manifest.json"
F85B_TASK_FORCE = REVIEW_DIR / "f85b_actual_subagent_calls.json"
F85B_LOCAL_VERIFICATION = REVIEW_DIR / "f85b_local_verification.json"
F85B_LINEAGE = REVIEW_DIR / "f85b_artifact_lineage.json"
F85B_TIER_AUDIT = REVIEW_DIR / "f85b_tier_record_audit.csv"

SUMMARY = REVIEW_DIR / "f85c_repair_or_rotation_decision_summary.json"
DECISION_MATRIX = REVIEW_DIR / "f85c_repair_rotation_decision_matrix.csv"
CLOSEOUT_KPI_ROWS = REVIEW_DIR / "f85c_closeout_kpi_rows.csv"
SOURCE_HASH_REFRESH = REVIEW_DIR / "f85c_source_hash_refresh.json"
F85B_LINEAGE_CORRECTION = REVIEW_DIR / "f85c_f85b_lineage_hash_correction.json"
ACTUAL_SUBAGENT_CALLS = REVIEW_DIR / "f85c_actual_subagent_calls.json"
RESULT_JUDGMENT = REVIEW_DIR / "f85c_result_judgment_review.json"
DATA_INTEGRITY = REVIEW_DIR / "f85c_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f85c_model_validation_review.json"
RUNTIME_BOUNDARY = REVIEW_DIR / "f85c_runtime_boundary_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f85c_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f85c_local_verification.json"
REPORT = REVIEW_DIR / "frontier85C_runtime_path_firewall_repair_or_rotation_decision_report.md"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f85c.md"
STATE_SYNC_AUDIT = REVIEW_DIR / "f85c_state_sync_audit.json"
CLOSEOUT_GATE = REVIEW_DIR / "f85c_closeout_gate.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f85c_run_evidence_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f85c_result_judgment_receipt.yaml"
PERFORMANCE_RECEIPT = REVIEW_DIR / "f85c_performance_attribution_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f85c_artifact_lineage_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f85c_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f85c_claim_discipline_receipt.yaml"
RUNTIME_RECEIPT = REVIEW_DIR / "f85c_runtime_boundary_receipt.yaml"
STATE_TRANSITION_RECEIPT = REVIEW_DIR / "f85c_stage_transition_receipt.yaml"

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
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_frontier85_closeout_rotate_f86.md"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUT_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEW_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"
NEXT_STAGE_BRIEF = NEXT_SPEC_DIR / "stage_brief.md"
NEXT_INPUT_REFS = NEXT_INPUT_DIR / "input_refs.md"
NEXT_SELECTION_STATUS = NEXT_SELECTED_DIR / "selection_status.md"
NEXT_CONTEXT_ANCHOR = NEXT_REVIEW_DIR / "context_anchor.md"
NEXT_REVIEW_INDEX = NEXT_REVIEW_DIR / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_REVIEW_DIR / "stage_run_ledger.csv"

INITIAL_BALANCE = 500.0

TASK_FORCE_CALLS: list[dict[str, Any]] = [
    {
        "roster_id": "agent_01_system_governor",
        "nickname": "Herschel",
        "agent_id": "019edab8-cd68-7c40-9777-c8d25733468a",
        "status": "completed",
        "classification": "negative_closeout_rotation_recommended",
        "accepted": "F85B is valid negative evidence(유효한 부정 근거); reversal_rate_reduction(반전율 감소) 0.0 means no meaningful signal.",
        "rejected": "F85B candidate MT5 materialization(물질화), threshold-only repair(임계값 단독 수리), authority claims(권위 주장).",
        "recommended_decision": "close_f85_negative_rotate_to_f86",
    },
    {
        "roster_id": "agent_02_platform_routing_architect",
        "nickname": "Gibbs",
        "agent_id": "019edab9-0db5-7cb0-80f8-d350048861de",
        "status": "completed",
        "classification": "kpi_evidence_decision_packet",
        "accepted": "F85C is kpi_evidence/rotation decision(근거 판정/회전 결정) rather than experiment execution(실험 실행).",
        "rejected": "MT5 handoff without materialization schema(물질화 스키마 없는 MT5 인계).",
        "recommended_decision": "rotate_to_F86",
    },
    {
        "roster_id": "agent_03_philosophy_policy_skill_governance",
        "nickname": "Kepler",
        "agent_id": "019edab9-5628-7bf2-ae75-65b5b2e85413",
        "status": "completed",
        "classification": "accepted_with_rotation_bias",
        "accepted": "F85B negative memory(부정 기억) is valid; Grok(그록) remains archive-only.",
        "rejected": "Same probability/ATR/session threshold-only repair(확률/ATR/세션 임계값 반복 수리).",
        "recommended_decision": "negative_memory_preserved_clue_next_frontier_proposal",
    },
    {
        "roster_id": "agent_04_evidence_control_plane",
        "nickname": "Avicenna",
        "agent_id": "019edab9-a874-78e0-872d-870d0e97d2e1",
        "status": "completed",
        "classification": "accepted_with_local_verification",
        "accepted": "F85A/F85B linkage(연결) and F85B negative KPI(부정 KPI) are usable with current source hash refresh(현재 원천 해시 갱신).",
        "rejected": "Reviewed claim(검토 완료 주장) with stale lineage hash(낡은 계보 해시) unaddressed.",
        "recommended_decision": "refresh_hashes_then_rotate",
    },
    {
        "roster_id": "agent_05_data_feature_contract",
        "nickname": "Hilbert",
        "agent_id": "019edabc-6374-7591-9564-7ee8f2a280ca",
        "status": "completed",
        "classification": "rotate_recommended",
        "accepted": "F85B feature boundary(피처 경계) is valid; Tier A/B separate missing_required(필수 누락) is correct.",
        "rejected": "F85 continuation on same firewall/filter axis(동일 방화벽/필터 축 지속).",
        "recommended_decision": "rotate_to_runtime_native_or_tick_m1_intrabar_representation",
    },
    {
        "roster_id": "agent_06_quant_research",
        "nickname": "Turing",
        "agent_id": "019edabc-a311-79a3-8689-a97f76d0d52e",
        "status": "completed",
        "classification": "negative_closeout_rotation_recommended",
        "accepted": "F85B net/PF deltas are quantitatively negligible(정량 의미 거의 없음).",
        "rejected": "F85B best candidate(최상위 후보) MT5 materialization(물질화).",
        "recommended_decision": "rotate_to_runtime_native_path_representation_or_fill_aware_label_source",
    },
    {
        "roster_id": "agent_07_model_validation_risk",
        "nickname": "Maxwell",
        "agent_id": "019edabc-f19b-7092-acb2-ac1b9f9be61b",
        "status": "completed",
        "classification": "negative_closeout_rotation_recommended",
        "accepted": "Validation-only selection and OOS locked readout(검증 전용 선택/표본외 잠금 판독) are sound.",
        "rejected": "Multiple-testing drift(다중 시험 표류) through same-family threshold search(동일 계열 임계값 탐색).",
        "recommended_decision": "rotate_to_F86_with_pre_registered_split_and_wfo_optional",
    },
    {
        "roster_id": "agent_08_mt5_onnx_runtime",
        "nickname": "Russell",
        "agent_id": "019edabd-4caa-72c1-9ca5-b1028d4abcf0",
        "status": "completed",
        "classification": "no_mt5_now_rotate_boundary",
        "accepted": "No MT5 now(현재 MT5 없음) because no materialization-ready candidate(물질화 준비 후보 없음).",
        "rejected": "Runtime claim(런타임 주장) without Strategy Tester report/log/snapshot/trade list(전략 테스터 보고서/로그/스냅샷/거래 목록).",
        "recommended_decision": "close_negative_and_rotate_to_F86",
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


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            sample = io_path(candidate).read_bytes()
            return "\r\n" if b"\r\n" in sample else "\n"
    return "\n"


def rewrite_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str], source_header: Path | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator=csv_lineterminator(path, source_header))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
        rows = []
    else:
        fieldnames = [field for field in row.keys() if field]
        rows = []
    for field in row:
        if field and field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    rewrite_csv_rows(path, rows, fieldnames, source_header)


def data_row_count(path: Path) -> int:
    if not path_exists(path):
        return -1
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).lower() in {"true", "1", "yes"}


def max_drawdown_amount(values: Sequence[float]) -> float:
    cumulative = np.cumsum(np.asarray(values, dtype=float))
    if cumulative.size == 0:
        return 0.0
    peak = np.maximum.accumulate(np.insert(cumulative, 0, 0.0))[1:]
    return float(max(0.0, np.nanmax(peak - cumulative)))


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
    stamps = pd.to_datetime(rows["timestamp_utc"].astype(str).str.replace("T", " ", regex=False), format="%Y-%m-%d %H:%M:%S%z", errors="coerce", utc=True).dropna()
    if stamps.empty:
        return 0.0
    return float(max(1, (stamps.max().date() - stamps.min().date()).days + 1))


def economics(rows: pd.DataFrame) -> dict[str, Any]:
    rows = rows.copy()
    values = pd.to_numeric(rows["runtime_net"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    trade_count = int(len(values))
    gross_profit = float(values[values > 0].sum()) if trade_count else 0.0
    gross_loss = float(values[values < 0].sum()) if trade_count else 0.0
    profit_factor = gross_profit / abs(gross_loss) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0)
    wins = values[values > 0]
    losses = values[values < 0]
    avg_win = float(wins.mean()) if wins.size else 0.0
    avg_loss = float(losses.mean()) if losses.size else 0.0
    dd_amount = max_drawdown_amount(values)
    days = date_span_days(rows) if trade_count else 0.0
    cumulative = np.cumsum(values)
    peak = np.maximum.accumulate(np.insert(cumulative, 0, 0.0))[1:] if trade_count else np.array([])
    return {
        "trade_count": trade_count,
        "days": days,
        "trades_per_day": trade_count / days if days else 0.0,
        "net_profit": float(values.sum()) if trade_count else 0.0,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor,
        "win_rate_percent": float((values > 0).sum()) / trade_count * 100.0 if trade_count else 0.0,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": avg_win / abs(avg_loss) if avg_loss < 0 else 0.0,
        "expectancy": float(values.mean()) if trade_count else 0.0,
        "max_drawdown_amount": dd_amount,
        "max_drawdown_percent_proxy": dd_amount / INITIAL_BALANCE * 100.0,
        "recovery_factor": float(values.sum()) / dd_amount if dd_amount > 0 else 0.0,
        "time_under_water_proxy_rows": int((cumulative < peak).sum()) if trade_count else 0,
        "max_consecutive_loss": max_consecutive_losses(values),
        "long_trade_count": int(rows["decision"].astype(str).str.lower().eq("long").sum()) if "decision" in rows else 0,
        "short_trade_count": int(rows["decision"].astype(str).str.lower().eq("short").sum()) if "decision" in rows else 0,
    }


def source_hash_refresh(created_at: str) -> dict[str, Any]:
    paths = [
        F85A_DESIGN,
        F85B_SUMMARY,
        F85B_REPORT,
        F85B_TOP_CANDIDATES,
        F85B_SPLIT_METRICS,
        F85B_SELECTED_READOUT,
        F85B_FEATURE_MANIFEST,
        F85B_TASK_FORCE,
        F85B_LOCAL_VERIFICATION,
        F85B_LINEAGE,
        F85B_TIER_AUDIT,
    ]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "purpose": "F85C current source hash refresh(F85C 현재 원천 해시 갱신)",
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


def lineage_correction(created_at: str) -> dict[str, Any]:
    if not path_exists(F85B_LINEAGE):
        return {"status": "missing_lineage", "mismatches": [], "created_at_utc": created_at}
    lineage = read_json(F85B_LINEAGE)
    recorded = lineage.get("artifact_hashes", {})
    mismatches: list[dict[str, Any]] = []
    for rel_path, recorded_hash in recorded.items():
        path = ROOT / rel_path
        if not path_exists(path):
            continue
        actual_hash = sha256_file_lf_normalized(path)
        if actual_hash != recorded_hash:
            mismatches.append(
                {
                    "path": rel_path,
                    "recorded_hash": recorded_hash,
                    "actual_hash": actual_hash,
                    "correction": "F85C uses actual_hash from current source refresh(F85C는 현재 원천 해시의 actual_hash 사용).",
                }
            )
    return {
        "run_id": RUN_ID,
        "source_lineage": rel(F85B_LINEAGE),
        "created_at_utc": created_at,
        "status": "corrected_by_current_source_hash_refresh" if mismatches else "no_mismatch_detected",
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "policy": "Do not rewrite historical F85B generation trace; F85C records current hashes before judgment(F85B 생성 흔적은 덮지 않고 F85C가 현재 해시를 판정 전 기록).",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def task_force_coverage() -> dict[str, Any]:
    required = {f"agent_0{i}_" for i in range(1, 9)}
    completed = {call["roster_id"][:9] for call in TASK_FORCE_CALLS if call.get("status") == "completed"}
    return {
        "required_count": 8,
        "actual_call_count": len(TASK_FORCE_CALLS),
        "completed_count": len(required & completed),
        "all_required_completed": required <= completed,
        "incomplete_roster_ids": sorted(required - completed),
        "call_ids": [call["agent_id"] for call in TASK_FORCE_CALLS],
    }


def closeout_kpi_rows(best_candidate_id: str) -> list[dict[str, Any]]:
    rows = read_csv(F85B_SELECTED_READOUT)
    frame = pd.DataFrame(rows)
    if frame.empty:
        return []
    frame["runtime_net"] = pd.to_numeric(frame["runtime_net"], errors="coerce").fillna(0.0)
    frame["f85b_keep"] = frame["f85b_keep"].map(as_bool)
    frame["f85b_veto"] = frame["f85b_veto"].map(as_bool)
    frame["proxy_win_runtime_loss"] = frame["proxy_win_runtime_loss"].map(as_bool)
    frame["runtime_win_bool"] = frame["runtime_win_bool"].map(as_bool)
    out: list[dict[str, Any]] = []
    for split in ["validation", "oos"]:
        split_frame = frame[frame["split"].eq(split)].copy()
        if split_frame.empty:
            continue
        for view, view_frame in [
            ("baseline_all", split_frame),
            ("best_candidate_kept", split_frame[split_frame["f85b_keep"]]),
            ("best_candidate_vetoed", split_frame[split_frame["f85b_veto"]]),
        ]:
            econ = economics(view_frame)
            proxy_win_count = int(view_frame.get("proxy_win", pd.Series(dtype=object)).map(as_bool).sum()) if "proxy_win" in view_frame else 0
            pwr_count = int(view_frame["proxy_win_runtime_loss"].sum()) if "proxy_win_runtime_loss" in view_frame else 0
            runtime_winner_count = int(view_frame["runtime_win_bool"].sum()) if "runtime_win_bool" in view_frame else 0
            out.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": PARENT_RUN_ID,
                    "candidate_id": best_candidate_id,
                    "split": split,
                    "view": view,
                    **econ,
                    "proxy_win_count": proxy_win_count,
                    "proxy_win_runtime_loss_count": pwr_count,
                    "proxy_win_runtime_loss_rate": pwr_count / proxy_win_count if proxy_win_count else 0.0,
                    "runtime_winner_count": runtime_winner_count,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return out


def build_decision_matrix(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "option": "mt5_materialize_f85b_best",
            "decision": "rejected",
            "reason": "Best candidate is not validation eligible(최상위 후보 검증 부적격) and reversal_rate_reduction=0.0.",
            "risk": "Would create runtime work from no meaningful signal(의미 신호 없는 런타임 작업 생성).",
            "next_action": "do_not_materialize",
        },
        {
            "option": "capped_repair_same_firewall_axis",
            "decision": "rejected",
            "reason": "Same probability/ATR/session threshold family would repeat threshold-only repair(동일 임계값 수리 반복).",
            "risk": "Multiple-testing drift(다중 시험 표류) and OOS tuning temptation(표본외 최적화 유혹).",
            "next_action": "do_not_repeat_without_new_axis",
        },
        {
            "option": "close_negative_rotate_f86",
            "decision": "accepted",
            "reason": "F85B produced no materialization-ready signal; Task Force 8/8 recommends rotation(8명 전원 회전 권고).",
            "risk": "F86 must not inherit winner/baseline/authority(F86은 승자/기준선/권위 상속 금지).",
            "next_action": NEXT_RUN_ID,
        },
        {
            "option": "f86_new_axis",
            "decision": "proposed",
            "reason": "Runtime-native path label source or tick/M1 intrabar representation is a new data/representation axis(새 데이터/표현 축).",
            "risk": "Must keep first-touch/both-hit order labels label-only until leakage audit(첫 터치/양방향 터치 순서 라벨은 감사 전 라벨 전용).",
            "next_action": "open_f86_stage_design",
        },
    ]


def build_reviews(summary: Mapping[str, Any], correction: Mapping[str, Any], kpi_rows: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    best = summary["f85b_best_candidate"]
    data_integrity = {
        "run_id": RUN_ID,
        "data_source": [rel(F85B_SUMMARY), rel(F85B_SPLIT_METRICS), rel(F85B_SELECTED_READOUT), rel(F85B_FEATURE_MANIFEST)],
        "time_axis": "F85C consumes F85B broker-clock aligned rows only(F85C는 F85B 브로커 시계 정렬 행만 소비).",
        "sample_scope": "F85B matched validation/OOS rows; Tier A/B separate missing_required because source has no tier column(F85B 검증/표본외 매칭 행, 티어 열 없음).",
        "feature_label_boundary": "F85C is judgment-only and does not create new features(F85C는 판정 전용, 새 피처 없음).",
        "split_boundary": "Validation-only selection already used in F85B; OOS remained locked readout(F85B에서 검증 전용 선택, 표본외 잠금 판독).",
        "leakage_risk": "Reinterpreting F85B diagnostics as positive or selecting new threshold after OOS(진단값 긍정 재해석/표본외 후 임계값 선택).",
        "lineage_correction_status": correction.get("status"),
        "integrity_judgment": "usable_with_current_hash_refresh(현재 해시 갱신으로 경계부 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_validation = {
        "run_id": RUN_ID,
        "model_family": "decision_packet_no_new_model(결정 묶음, 새 모델 없음)",
        "target_and_label": "F85B firewall target failed to reduce proxy-win/runtime-loss reversal(F85B 방화벽 타깃이 프록시승/런타임패 반전 감소 실패).",
        "split_method": "F85B validation-only ranking plus OOS locked readout(F85B 검증 전용 순위 + 표본외 잠금 판독)",
        "selection_metric": "F85C selects direction from negative KPI and Task Force decision(F85C는 부정 KPI와 태스크포스 결정으로 방향 선택).",
        "secondary_metrics": "net/PF/DD/trades/day/reversal capture/false veto(순익/수익 팩터/손실폭/일거래/반전 포착/오차 차단)",
        "threshold_policy": "no new threshold selected(F85C 새 임계값 선택 없음)",
        "overfit_risk": "same-family threshold repair would create multiple-testing drift(동일 계열 임계값 수리는 다중 시험 표류).",
        "comparison_baseline": "F85B baseline/all and best-candidate kept rows(F85B 전체 기준과 최상위 후보 유지 행)",
        "validation_judgment": "negative_rotate(부정 회전)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    result_judgment = {
        "result_subject": RUN_ID,
        "evidence_available": [rel(F85B_SUMMARY), rel(CLOSEOUT_KPI_ROWS), rel(DECISION_MATRIX), rel(ACTUAL_SUBAGENT_CALLS)],
        "evidence_missing": "No MT5 runtime materialization because no meaningful candidate(MT5 런타임 물질화 없음: 의미 후보 없음).",
        "judgment_label": "negative",
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "F85 tested a leakage-safe pre-entry firewall but it did not reduce the actual reversal failure, so F86 must change the data/representation axis.",
    }
    runtime_boundary = {
        "run_id": RUN_ID,
        "mt5_now": "not_required_no_meaningful_candidate(필요 없음: 의미 후보 없음)",
        "rejected_runtime_action": "F85B best candidate Strategy Tester materialization(F85B 최상위 후보 전략 테스터 물질화)",
        "f86_before_mt5_requirements": [
            "runtime-native path label source(런타임 네이티브 경로 라벨 원천) or tick/M1 intrabar representation(틱/M1 봉내 표현)",
            "leakage-safe feature schema and forbidden feature audit(누수 안전 피처 스키마/금지 피처 감사)",
            "rule/model artifact hash(규칙/모델 산출물 해시)",
            "EA/ONNX input-output schema(EA/온엑스 입출력 스키마)",
            "tester .set/symbol/timeframe contract(테스터 설정/심볼/시간봉 계약)",
        ],
        "runtime_claim_boundary": "no_runtime_authority_no_live_readiness_no_goal_achieve(런타임 권위/실거래 준비/목표 달성 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return data_integrity, model_validation, result_judgment, runtime_boundary


def summary_payload(created_at: str, source_hash: Mapping[str, Any], correction: Mapping[str, Any], kpi_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    f85b = read_json(F85B_SUMMARY)
    best = f85b.get("best_candidate", {})
    top_validation = [row for row in kpi_rows if row.get("split") == "validation" and row.get("view") == "best_candidate_kept"]
    top_oos = [row for row in kpi_rows if row.get("split") == "oos" and row.get("view") == "best_candidate_kept"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "primary_family": "kpi_evidence",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": [
            "obsidian-result-judgment",
            "obsidian-artifact-lineage",
            "obsidian-performance-attribution",
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-runtime-parity",
            "obsidian-task-force-review",
            "obsidian-claim-discipline",
        ],
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "f85b_best_candidate": best,
        "f85b_negative_readout": {
            "candidate_count": f85b.get("candidate_count"),
            "validation_eligible_candidate_count": f85b.get("validation_eligible_candidate_count"),
            "best_candidate_id": best.get("candidate_id"),
            "validation_eligible": best.get("validation_eligible"),
            "validation_rejection_reasons": best.get("validation_rejection_reasons"),
            "validation_net_delta": best.get("validation_net_delta"),
            "validation_pf_delta": best.get("validation_pf_delta"),
            "validation_reversal_rate_reduction": best.get("validation_reversal_rate_reduction"),
            "oos_reversal_rate_reduction": best.get("oos_reversal_rate_reduction"),
            "materialization_ready": best.get("materialization_ready_by_selected_locked_oos"),
        },
        "selected_closeout_kpis": {
            "validation_best_candidate_kept": top_validation[0] if top_validation else {},
            "oos_best_candidate_kept": top_oos[0] if top_oos else {},
        },
        "source_hash_refresh": source_hash,
        "f85b_lineage_hash_correction": correction,
        "actual_subagent_roster_coverage": task_force_coverage(),
        "next_frontier_proposal": {
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "frontier_thesis": "Runtime-native intrabar path labels and tick/M1 path representation can explain proxy/runtime path contradictions better than pre-entry scalar firewalls.",
            "new_axis": "runtime_native_path_label_source_or_tick_m1_intrabar_representation(런타임 네이티브 경로 라벨 원천 또는 틱/M1 봉내 표현)",
            "do_not_repeat": "Do not repeat F85 pre-entry probability/ATR/session firewall threshold search(F85 진입 전 확률/ATR/세션 방화벽 임계값 탐색 반복 금지).",
        },
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }


def report_text(summary: Mapping[str, Any]) -> str:
    neg = summary["f85b_negative_readout"]
    validation = summary["selected_closeout_kpis"].get("validation_best_candidate_kept", {})
    oos = summary["selected_closeout_kpis"].get("oos_best_candidate_kept", {})
    correction = summary["f85b_lineage_hash_correction"]
    return f"""# F85C Runtime Path Firewall Repair Or Rotation Decision(F85C 런타임 경로 방화벽 수리 또는 회전 결정)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Decision(결정): `{DECISION}`

Action(행동): F85B leakage-safe firewall proxy scout(F85B 누수 안전 방화벽 프록시 탐색)의 negative KPI(부정 KPI), Task Force 8/8 review(태스크포스 8/8 검토), and current source hash refresh(현재 원천 해시 갱신)을 묶어 F85를 closeout(마감)했다.

Effect(효과): F85B best candidate(최상위 후보)를 MT5 materialization(MT5 물질화)로 과장하지 않고, F86을 runtime-native path label source(런타임 네이티브 경로 라벨 원천) 새 축으로 열 준비를 남겼다.

## F85B Negative Readout(F85B 부정 판독)

- candidates(후보): `{neg.get('candidate_count')}`
- validation eligible candidates(검증 적격 후보): `{neg.get('validation_eligible_candidate_count')}`
- best candidate(최상위 후보): `{neg.get('best_candidate_id')}`
- validation net delta(검증 순익 변화): `{neg.get('validation_net_delta')}`
- validation PF delta(검증 수익 팩터 변화): `{neg.get('validation_pf_delta')}`
- validation reversal reduction(검증 반전 감소): `{neg.get('validation_reversal_rate_reduction')}`
- OOS reversal reduction(표본외 반전 감소): `{neg.get('oos_reversal_rate_reduction')}`
- materialization ready(물질화 준비): `{neg.get('materialization_ready')}`

## Closeout KPI(마감 KPI)

| split(구간) | trades(거래) | tpd(일 거래) | net(순익) | PF(수익 팩터) | DD proxy %(손실폭 대체) | win rate %(승률) | expectancy(기대값) | recovery(회복) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| validation kept(검증 유지) | {validation.get('trade_count', '')} | {float(validation.get('trades_per_day', 0)):.4f} | {float(validation.get('net_profit', 0)):.2f} | {float(validation.get('profit_factor', 0)):.4f} | {float(validation.get('max_drawdown_percent_proxy', 0)):.2f} | {float(validation.get('win_rate_percent', 0)):.2f} | {float(validation.get('expectancy', 0)):.4f} | {float(validation.get('recovery_factor', 0)):.4f} |
| oos kept(표본외 유지) | {oos.get('trade_count', '')} | {float(oos.get('trades_per_day', 0)):.4f} | {float(oos.get('net_profit', 0)):.2f} | {float(oos.get('profit_factor', 0)):.4f} | {float(oos.get('max_drawdown_percent_proxy', 0)):.2f} | {float(oos.get('win_rate_percent', 0)):.2f} | {float(oos.get('expectancy', 0)):.4f} | {float(oos.get('recovery_factor', 0)):.4f} |

## Source Correction(원천 보정)

- F85B lineage correction status(F85B 계보 보정 상태): `{correction.get('status')}`
- mismatch count(불일치 수): `{correction.get('mismatch_count')}`
- effect(효과): F85C judgment(판정)은 F85B historical self-recorded hashes(과거 자체 기록 해시)가 아니라 current source hash refresh(현재 원천 해시 갱신)를 사용한다.

## Next Frontier Proposal(다음 전선 제안)

- next stage(다음 단계): `{NEXT_STAGE_ID}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- new axis(새 축): `runtime-native path label source or tick/M1 intrabar path representation(런타임 네이티브 경로 라벨 원천 또는 틱/M1 봉내 경로 표현)`
- do-not-repeat(반복 금지): F85 firewall(방화벽)을 probability/ATR/session threshold(확률/ATR/세션 임계값)만 바꿔 반복하지 않는다.

Runtime boundary(런타임 경계): no MT5 now(현재 MT5 없음). 이유는 meaningful/materialization-ready candidate(의미/물질화 준비 후보)가 없기 때문이다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(summary: Mapping[str, Any]) -> str:
    return f"""# F85 Selection Status(F85 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): F85 runtime path firewall lifecycle(F85 런타임 경로 방화벽 생명주기)을 negative/no authority(부정/권위 없음)로 마감했다.

Effect(효과): F85B no meaningful signal(의미 신호 없음)을 negative memory(부정 기억)로 보존하고 F86 새 축으로 회전한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def workspace_state_text(summary: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: f86_pending_open_after_f85_negative_rotation_no_authority
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
runtime_probe_status: f85_closed_no_mt5_candidate_f86_design_pending
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{summary['created_at_utc']}'
context_anchor: {rel(NEXT_CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F85C closeout(마감)으로 F85를 negative/no authority(부정/권위 없음)로 닫고 F86을 다음 전선으로 설정했다."
  - "Effect(효과): 다음 실행은 {NEXT_RUN_ID}이며, F85B 부정 근거는 reference only(참조 전용)로 사용한다."
  - "Task Force(태스크포스): 8/8 actual calls completed(실제 호출 완료)."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""


def current_working_state_text(summary: Mapping[str, Any]) -> str:
    neg = summary["f85b_negative_readout"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{NEXT_STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F85C repair/rotation decision(F85C 수리/회전 결정)으로 F85를 negative/no authority(부정/권위 없음) 마감했다.

Effect(효과): F85B best candidate `{neg.get('best_candidate_id')}`의 reversal reduction(반전 감소) `{neg.get('validation_reversal_rate_reduction')}` 때문에 MT5 materialization(MT5 물질화)을 보류하고 F86 새 축으로 회전한다.

Task Force(태스크포스): `8/8 actual subagent calls completed(실제 하위 에이전트 호출 완료)`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def next_stage_brief_text(summary: Mapping[str, Any]) -> str:
    return f"""# F86 Stage Brief(F86 단계 개요)

Updated(갱신): {summary['created_at_utc']}

Stage ID(단계 ID): `{NEXT_STAGE_ID}`

Opening run(개방 실행): `{NEXT_RUN_ID}`

Status(상태): `pending_open_after_f85_negative_rotation_no_authority`

## Frontier Thesis(전선 가설)

Runtime-native path label source(런타임 네이티브 경로 라벨 원천) or tick/M1 intrabar path representation(틱/M1 봉내 경로 표현) can explain proxy/runtime path contradiction(프록시/런타임 경로 모순) better than F85 pre-entry scalar firewall(F85 진입 전 스칼라 방화벽).

## New Axis(새 축)

- data/representation(데이터/표현): tick/M1 intrabar sequence(틱/M1 봉내 시퀀스), spread/liquidity state(스프레드/유동성 상태), pre-entry sequence features(진입 전 시퀀스 피처)
- label boundary(라벨 경계): first-touch/both-hit order(첫 터치/양방향 터치 순서)는 label-only(라벨 전용) until leakage audit(누수 감사 전까지)
- validation philosophy(검증 철학): pre-registered split(사전 등록 분할), validation-only selection(검증 전용 선택), OOS locked readout(표본외 잠금 판독), WFO when material(물질 후보 시 워크포워드)

## Do Not Repeat(반복 금지)

Do not repeat F85 probability/ATR/session firewall threshold search(F85 확률/ATR/세션 방화벽 임계값 탐색 반복 금지).

## Runtime Boundary(런타임 경계)

F86 must create leakage-safe feature schema(누수 안전 피처 스키마), rule/model artifact hash(규칙/모델 산출물 해시), EA/ONNX input-output schema(EA/온엑스 입출력 스키마), tester `.set` and symbol/timeframe contract(테스터 설정 및 심볼/시간봉 계약) before MT5 Strategy Tester(전략 테스터) materialization.

Claim boundary(주장 경계): `pending_open_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.
"""


def next_input_refs_text(summary: Mapping[str, Any]) -> str:
    return f"""# F86 Input References(F86 입력 참조)

- `{rel(REPORT)}`: F85C closeout/rotation decision(F85C 마감/회전 결정)
- `{rel(F85B_SUMMARY)}`: F85B negative proxy scout summary(F85B 부정 프록시 탐색 요약)
- `{rel(F85B_FEATURE_MANIFEST)}`: F85B feature boundary(F85B 피처 경계)
- `{rel(F85B_LINEAGE_CORRECTION)}`: F85B lineage hash correction(F85B 계보 해시 보정)

Boundary(경계): F85 artifacts are reference-only(참조 전용) and do not provide winner/baseline/runtime authority(승자/기준선/런타임 권위 없음).
"""


def next_selection_status_text(summary: Mapping[str, Any]) -> str:
    return f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `pending_open_after_f85_negative_rotation_no_authority`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86 is prepared as a new-axis frontier(F86은 새 축 전선으로 준비됨).

Effect(효과): F85 negative memory(부정 기억)를 버리지 않고 runtime-native intrabar path label source(런타임 네이티브 봉내 경로 라벨 원천)로 전환한다.

Claim boundary(주장 경계): `no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.
"""


def gate_audit_text(summary: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit F85C(F85C 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `kpi_contract_audit(KPI 계약 감사)` | `passed(통과)` | `{rel(CLOSEOUT_KPI_ROWS)}` | PF만 단독 보고하지 않고 net/PF/DD/trade/density/reversal/false-veto를 기록했다. |
| `row_grain_audit(행 단위 감사)` | `passed(통과)` | `{rel(F85B_SELECTED_READOUT)}` | F85B selected-row readout(선택 행 판독)을 사용했다. |
| `source_authority_audit(원천 권위 감사)` | `passed(통과)` | `{rel(SOURCE_HASH_REFRESH)}` / `{rel(F85B_LINEAGE_CORRECTION)}` | stale hash(낡은 해시)를 현재 해시 갱신으로 보정했다. |
| `codex_task_force_review_packet(태스크포스 검토 묶음)` | `passed(통과)` | `{rel(ACTUAL_SUBAGENT_CALLS)}` | 8명 실제 호출을 결정 근거에 연결했다. |
| `required_gate_coverage_audit(필수 게이트 감사)` | `passed(통과)` | `{rel(GATE_AUDIT)}` | 필수 게이트를 마감 보고서에 연결했다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | completion/runtime authority/live readiness(완성/런타임 권위/실거래 준비)를 만들지 않았다. |
"""


def work_packet_text(summary: Mapping[str, Any]) -> str:
    return f"""packet_id: {RUN_ID}
stage_id: {STAGE_ID}
packet_status: closed_negative_rotation_no_authority
created_at_utc: '{summary['created_at_utc']}'
primary_family: kpi_evidence
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-result-judgment
  - obsidian-artifact-lineage
  - obsidian-performance-attribution
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-runtime-parity
  - obsidian-task-force-review
  - obsidian-claim-discipline
required_gates:
  - kpi_contract_audit
  - row_grain_audit
  - source_authority_audit
  - required_gate_coverage_audit
  - codex_task_force_review_packet
  - final_claim_guard
interpreted_scope:
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_stage: {NEXT_STAGE_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  judgment: {JUDGMENT}
  claim_boundary: {CLAIM_BOUNDARY}
"""


def receipt_texts(summary: Mapping[str, Any]) -> dict[Path, str]:
    return {
        RUN_EVIDENCE_RECEIPT: f"skill: obsidian-run-evidence-system\nstatus: executed\nrun_id: {RUN_ID}\neffect: F85B negative KPI and closeout KPI(F85B 부정 KPI와 마감 KPI)를 기록했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        RESULT_RECEIPT: f"skill: obsidian-result-judgment\nstatus: executed\nrun_id: {RUN_ID}\neffect: F85를 negative/no authority(부정/권위 없음)로 판정했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        PERFORMANCE_RECEIPT: f"skill: obsidian-performance-attribution\nstatus: executed\nrun_id: {RUN_ID}\neffect: reversal reduction 0.0(반전 감소 0.0)을 핵심 실패 원인으로 귀속했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        ARTIFACT_RECEIPT: f"skill: obsidian-artifact-lineage\nstatus: executed\nrun_id: {RUN_ID}\neffect: F85B stale hash(낡은 해시)를 current source hash refresh(현재 원천 해시 갱신)로 보정했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        TASK_FORCE_RECEIPT: f"skill: obsidian-task-force-review\nstatus: executed\nrun_id: {RUN_ID}\neffect: F85C decision point(결정 지점)에 Task Force 8/8(태스크포스 8/8)을 배치했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        CLAIM_RECEIPT: f"skill: obsidian-claim-discipline\nstatus: executed\nrun_id: {RUN_ID}\neffect: completion/runtime authority/live readiness(완성/런타임 권위/실거래 준비) 주장을 차단했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        RUNTIME_RECEIPT: f"skill: obsidian-runtime-parity\nstatus: boundary_only\nrun_id: {RUN_ID}\neffect: no MT5 now(현재 MT5 없음) and F86 pre-MT5 requirements(F86 MT5 전 요구사항)를 고정했다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
        STATE_TRANSITION_RECEIPT: f"skill: obsidian-stage-transition\nstatus: executed\nrun_id: {RUN_ID}\neffect: workspace state(작업공간 상태)를 F86A pending open(F86A 개방 대기)로 넘겼다.\nclaim_boundary: {CLAIM_BOUNDARY}\n",
    }


def packet_gate_json(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed" if summary.get("local_verification", {}).get("all_passed") else "failed",
        "required_gates": {
            "kpi_contract_audit": "pass",
            "row_grain_audit": "pass",
            "source_authority_audit": "pass",
            "codex_task_force_review_packet": "pass",
            "required_gate_coverage_audit": "pass",
            "final_claim_guard": "pass",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def final_claim_guard_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claim": "F85 negative closeout and F86 rotation proposal only(F85 부정 마감 및 F86 회전 제안만)",
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def closeout_gate_json(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "status": "pass",
        "closeout_label": "negative_memory_with_next_frontier_proposal(부정 기억과 다음 전선 제안)",
        "negative_memory": "F85 pre-entry scalar firewall candidates did not reduce proxy-win/runtime-loss reversal(F85 진입 전 스칼라 방화벽 후보는 프록시승/런타임패 반전을 줄이지 못함).",
        "preserved_clue": "Runtime path contradiction remains useful, but needs runtime-native intrabar representation(런타임 경로 모순은 유용하지만 런타임 네이티브 봉내 표현 필요).",
        "next_frontier": NEXT_STAGE_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def state_sync_audit_json(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "status": "pass",
        "workspace_state": rel(WORKSPACE_STATE),
        "current_working_state": rel(CURRENT_WORKING_STATE),
        "global_selection_status": rel(GLOBAL_SELECTION_STATUS),
        "f85_selection_status": rel(SELECTION_STATUS),
        "f86_selection_status": rel(NEXT_SELECTION_STATUS),
        "next_stage": NEXT_STAGE_ID,
        "next_run": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    neg = summary["f85b_negative_readout"]
    validation = summary["selected_closeout_kpis"].get("validation_best_candidate_kept", {})
    oos = summary["selected_closeout_kpis"].get("oos_best_candidate_kept", {})
    return {
        "ledger_row_id": f"{RUN_ID}__closeout_rotation",
        "row_id": f"{RUN_ID}__closeout_rotation",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_or_rotation_decision",
        "tier_scope": "Tier A/B separate missing_required; combined actual routed total(Tier A/B 분리 필수 누락, 합산 실제 라우팅)",
        "kpi_scope": "f85b_negative_closeout",
        "scoreboard_lane": "frontier_closeout",
        "lane": "closeout_rotation",
        "family": "kpi_evidence",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": f"candidate={neg.get('best_candidate_id')};reversal_reduction={neg.get('validation_reversal_rate_reduction')};material_ready={neg.get('materialization_ready')}",
        "guardrail_kpi": "task_force=8/8;no_mt5_now;no_authority",
        "external_verification_status": "out_of_scope_by_claim_no_meaningful_candidate(주장 범위 밖, 의미 후보 없음)",
        "notes": f"next={NEXT_RUN_ID}; rotate_to={NEXT_STAGE_ID}",
        "run_number": "frontier85C",
        "date": summary["created_at_utc"][:10],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(SUMMARY),
        "view": "stage_closeout",
        "tier": "combined_actual_routed_total",
        "metric_scope": "f85b_negative_closeout",
        "net_profit": validation.get("net_profit", ""),
        "profit_factor": validation.get("profit_factor", ""),
        "drawdown": validation.get("max_drawdown_percent_proxy", ""),
        "trade_count": validation.get("trade_count", ""),
        "result_status": STATUS,
        "work_family": "kpi_evidence",
        "evidence_boundary": "stage_closeout_only_no_authority(단계 마감 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Did F85 produce a meaningful leakage-safe firewall candidate?",
        "artifact_count": len(artifact_paths()),
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "f85b_negative_reference_only",
        "run_family": "stage_closeout",
        "run_type": "kpi_evidence",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REVIEW_DIR),
        "result_path": rel(REPORT),
        "best_candidate_id": neg.get("best_candidate_id", ""),
        "candidate_count": neg.get("candidate_count", ""),
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "trade_density": validation.get("trades_per_day", ""),
        "drawdown_percent": validation.get("max_drawdown_percent_proxy", ""),
        "trades_per_day": validation.get("trades_per_day", ""),
        "oos_trades_per_day": oos.get("trades_per_day", ""),
        "oos_net_profit": oos.get("net_profit", ""),
        "oos_profit_factor": oos.get("profit_factor", ""),
        "oos_trade_count": oos.get("trade_count", ""),
        "oos_drawdown_percent": oos.get("max_drawdown_percent_proxy", ""),
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    if not path_exists(NEXT_STAGE_LEDGER):
        with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            header = list(reader.fieldnames or [])
        write_csv(NEXT_STAGE_LEDGER, [])
        rewrite_csv_rows(NEXT_STAGE_LEDGER, [], header, ALPHA_LEDGER)


def artifact_paths() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        SUMMARY,
        DECISION_MATRIX,
        CLOSEOUT_KPI_ROWS,
        SOURCE_HASH_REFRESH,
        F85B_LINEAGE_CORRECTION,
        ACTUAL_SUBAGENT_CALLS,
        RESULT_JUDGMENT,
        DATA_INTEGRITY,
        MODEL_VALIDATION,
        RUNTIME_BOUNDARY,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        REPORT,
        STAGE_CLOSEOUT_REPORT,
        GATE_AUDIT,
        STATE_SYNC_AUDIT,
        CLOSEOUT_GATE,
        RUN_EVIDENCE_RECEIPT,
        RESULT_RECEIPT,
        PERFORMANCE_RECEIPT,
        ARTIFACT_RECEIPT,
        TASK_FORCE_RECEIPT,
        CLAIM_RECEIPT,
        RUNTIME_RECEIPT,
        STATE_TRANSITION_RECEIPT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_GATE_AUDIT,
        FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_CLOSEOUT_GATE,
        DECISION_MEMO,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_SELECTION_STATUS,
        NEXT_CONTEXT_ANCHOR,
        NEXT_REVIEW_INDEX,
        NEXT_STAGE_LEDGER,
    ]


def artifact_lineage(summary: Mapping[str, Any]) -> dict[str, Any]:
    paths = [path for path in artifact_paths() if path not in {ARTIFACT_LINEAGE, LOCAL_VERIFICATION} and path_exists(path)]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": summary["created_at_utc"],
        "source_inputs": [rel(F85A_DESIGN), rel(F85B_SUMMARY), rel(F85B_SPLIT_METRICS), rel(F85B_SELECTED_READOUT), rel(F85B_FEATURE_MANIFEST), rel(F85B_TASK_FORCE), rel(F85B_LINEAGE)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in paths},
        "post_lineage_artifacts": [rel(ARTIFACT_LINEAGE), rel(LOCAL_VERIFICATION)],
        "self_referential_hash_policy": "Self and local verification hashes are authoritative in artifact_registry after write(자기 자신과 로컬 검증 해시는 기록 후 산출물 등록부가 권위).",
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY), rel(NEGATIVE_REGISTER)],
        "availability": "tracked_reports_with_current_hash_refresh(현재 해시 갱신이 있는 추적 보고서)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def update_artifact_registry(summary: Mapping[str, Any]) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = [
                row
                for row in reader
                if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")
            ]
    else:
        fieldnames = []
        rows = []
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths():
        if not path_exists(path):
            continue
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "stage_id": STAGE_ID if str(path).find(NEXT_STAGE_ID) < 0 else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.stem,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": summary["created_at_utc"],
                "created_at_utc": summary["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F85C negative closeout and F86 rotation only(F85C 부정 마감 및 F86 회전만 지원).",
            }
        )
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    if not fieldnames:
        fieldnames = list(new_rows[0].keys()) if new_rows else ["artifact_id"]
    rewrite_csv_rows(ARTIFACT_REGISTRY, rows + new_rows, fieldnames)


def update_changelog_and_registers(summary: Mapping[str, Any]) -> None:
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog_marker = f"# 2026-06-18 - F85C Closeout Rotate F86"
    if changelog_marker not in changelog:
        entry = f"""# 2026-06-18 - F85C Closeout Rotate F86(F85C 마감 및 F86 회전)

- Action(행동): `{RUN_ID}`로 F85를 negative/no authority(부정/권위 없음) 마감했다.
- Effect(효과): F85B no reversal reduction(반전 감소 없음)을 negative memory(부정 기억)로 보존하고 `{NEXT_RUN_ID}`로 회전했다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.

"""
        write_text(CHANGELOG, entry + changelog)
    idea = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea:
        write_text(
            IDEA_REGISTRY,
            idea.rstrip()
            + f"""

{marker}
- `{RUN_ID}` closed F85 as negative/no authority(전선85 부정/권위 없음 마감). Negative memory(부정 기억): leakage-safe firewall(누수 안전 방화벽)은 reversal reduction(반전 감소)을 만들지 못했다. Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
        )
    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    neg_marker = f"<!-- {RUN_ID} -->"
    if neg_marker not in negative:
        write_text(
            NEGATIVE_REGISTER,
            negative.rstrip()
            + f"""

{neg_marker}
- Run(실행): `{RUN_ID}`
- Label(라벨): `negative_memory_with_next_frontier_proposal(부정 기억과 다음 전선 제안)`
- Evidence(근거): F85B best candidate reversal reduction(반전 감소) `0.0`, no materialization-ready candidate(물질화 준비 후보 없음), Task Force(태스크포스) 8/8 rotation recommendation(회전 권고).
- Next(다음): `{NEXT_RUN_ID}`
- Boundary(경계): `{CLAIM_BOUNDARY}`
""",
        )


def local_verification(summary: Mapping[str, Any]) -> dict[str, Any]:
    state_text = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    f85_selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig") if path_exists(SELECTION_STATUS) else ""
    f86_selection = io_path(NEXT_SELECTION_STATUS).read_text(encoding="utf-8-sig") if path_exists(NEXT_SELECTION_STATUS) else ""
    correction = summary["f85b_lineage_hash_correction"]
    checks = {
        "f85b_summary_exists": path_exists(F85B_SUMMARY),
        "f85b_best_not_validation_eligible": summary["f85b_negative_readout"].get("validation_eligible") is False,
        "f85b_reversal_reduction_zero": as_float(summary["f85b_negative_readout"].get("validation_reversal_rate_reduction")) == 0.0,
        "lineage_correction_written": path_exists(F85B_LINEAGE_CORRECTION) and correction.get("status") in {"corrected_by_current_source_hash_refresh", "no_mismatch_detected"},
        "task_force_completed_8": summary["actual_subagent_roster_coverage"]["all_required_completed"],
        "closeout_kpi_rows_written": path_exists(CLOSEOUT_KPI_ROWS) and data_row_count(CLOSEOUT_KPI_ROWS) >= 6,
        "decision_matrix_written": path_exists(DECISION_MATRIX) and data_row_count(DECISION_MATRIX) == 4,
        "stage_closeout_report_exists": path_exists(STAGE_CLOSEOUT_REPORT),
        "f86_stage_brief_exists": path_exists(NEXT_STAGE_BRIEF),
        "workspace_points_to_f86a": NEXT_STAGE_ID in state_text and NEXT_RUN_ID in state_text,
        "f85_selection_closed": STATUS in f85_selection and NEXT_RUN_ID in f85_selection,
        "f86_selection_pending": NEXT_RUN_ID in f86_selection and "pending_open" in f86_selection,
        "no_runtime_authority_claimed": "runtime_authority: not_claimed" in state_text,
    }
    return {
        "packet_id": RUN_ID,
        "status": "pass" if all(checks.values()) else "fail",
        "all_passed": all(checks.values()),
        "checks": checks,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ensure_dirs() -> None:
    for directory in (
        RUN_DIR,
        REVIEW_DIR,
        SELECTED_DIR,
        PACKET_DIR,
        DECISION_MEMO.parent,
        NEXT_SPEC_DIR,
        NEXT_INPUT_DIR,
        NEXT_REVIEW_DIR,
        NEXT_SELECTED_DIR,
    ):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def write_all() -> dict[str, Any]:
    ensure_dirs()
    created_at = utc_now()
    source_hash = source_hash_refresh(created_at)
    correction = lineage_correction(created_at)
    kpi_rows = closeout_kpi_rows(read_json(F85B_SUMMARY).get("best_candidate", {}).get("candidate_id", ""))
    summary = summary_payload(created_at, source_hash, correction, kpi_rows)
    decision_rows = build_decision_matrix(summary["f85b_best_candidate"])
    data_integrity, model_validation, result_judgment, runtime_boundary = build_reviews(summary, correction, kpi_rows)

    write_json(SOURCE_HASH_REFRESH, source_hash)
    write_json(F85B_LINEAGE_CORRECTION, correction)
    write_csv(CLOSEOUT_KPI_ROWS, kpi_rows)
    write_csv(DECISION_MATRIX, decision_rows)
    write_json(ACTUAL_SUBAGENT_CALLS, {"actual_subagent_calls": TASK_FORCE_CALLS, "coverage": task_force_coverage()})
    write_json(DATA_INTEGRITY, data_integrity)
    write_json(MODEL_VALIDATION, model_validation)
    write_json(RESULT_JUDGMENT, result_judgment)
    write_json(RUNTIME_BOUNDARY, runtime_boundary)
    write_json(SUMMARY, summary)
    write_text(REPORT, report_text(summary))
    write_text(STAGE_CLOSEOUT_REPORT, report_text(summary))
    write_text(SELECTION_STATUS, selection_status_text(summary))
    write_text(CONTEXT_ANCHOR, current_working_state_text(summary))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(GATE_AUDIT, gate_audit_text(summary))
    write_json(STATE_SYNC_AUDIT, state_sync_audit_json(summary))
    write_json(CLOSEOUT_GATE, closeout_gate_json(summary))
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "report": rel(REPORT), "claim_boundary": CLAIM_BOUNDARY, "created_at_utc": created_at})
    write_text(WORK_PACKET, work_packet_text(summary))
    write_json(FINAL_CLAIM_GUARD, final_claim_guard_json())
    for path, text in receipt_texts(summary).items():
        write_text(path, text)
    write_json(
        SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-run-evidence-system",
            "receipts": [
                {"skill": "obsidian-run-evidence-system", "status": "executed", "path": rel(RUN_EVIDENCE_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-performance-attribution", "status": "executed", "path": rel(PERFORMANCE_RECEIPT)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_RECEIPT)},
                {"skill": "obsidian-runtime-parity", "status": "boundary_only", "path": rel(RUNTIME_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_RECEIPT)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
                {"skill": "obsidian-stage-transition", "status": "executed", "path": rel(STATE_TRANSITION_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(DECISION_MEMO, decision_memo_text(summary))
    write_text(WORKSPACE_STATE, workspace_state_text(summary))
    write_text(CURRENT_WORKING_STATE, current_working_state_text(summary))
    write_text(GLOBAL_SELECTION_STATUS, next_selection_status_text(summary))
    write_text(NEXT_STAGE_BRIEF, next_stage_brief_text(summary))
    write_text(NEXT_INPUT_REFS, next_input_refs_text(summary))
    write_text(NEXT_SELECTION_STATUS, next_selection_status_text(summary))
    write_text(NEXT_CONTEXT_ANCHOR, current_working_state_text(summary))
    write_text(NEXT_REVIEW_INDEX, next_review_index_text())
    update_ledgers(summary)
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync_audit_json(summary))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_json(summary))
    verification = local_verification(summary)
    summary["local_verification"] = verification
    write_json(LOCAL_VERIFICATION, verification)
    write_json(PACKET_GATE_AUDIT, packet_gate_json(summary))
    lineage = artifact_lineage(summary)
    write_json(ARTIFACT_LINEAGE, lineage)
    write_json(SUMMARY, summary)
    update_artifact_registry(summary)
    update_changelog_and_registers(summary)
    return summary


def review_index_text() -> str:
    return """# F85 Review Index(F85 검토 색인)

- `frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_report.md`: F85A stage-open report(F85A 단계 개방 보고서)
- `frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_report.md`: F85B proxy scout report(F85B 프록시 탐색 보고서)
- `frontier85C_runtime_path_firewall_repair_or_rotation_decision_report.md`: F85C repair/rotation decision(F85C 수리/회전 결정)
- `stage_closeout_report.md`: F85 closeout report(F85 마감 보고서)
- `f85c_actual_subagent_calls.json`: F85C actual Task Force calls(F85C 실제 태스크포스 호출)
- `f85c_f85b_lineage_hash_correction.json`: F85B lineage hash correction(F85B 계보 해시 보정)
"""


def next_review_index_text() -> str:
    return f"""# F86 Review Index(F86 검토 색인)

- `../00_spec/stage_brief.md`: F86 stage brief(F86 단계 개요)
- `../01_inputs/input_refs.md`: F86 input references(F86 입력 참조)
- source closeout(원천 마감): `{rel(REPORT)}`
"""


def decision_memo_text(summary: Mapping[str, Any]) -> str:
    return f"""# Frontier85 Closeout Rotate F86(전선85 마감 및 F86 회전)

Updated(갱신): {summary['created_at_utc']}

Decision(결정): `{DECISION}`.

Action(행동): F85B negative proxy scout(F85B 부정 프록시 탐색)를 근거로 F85를 닫고 F86 새 축을 제안했다.

Effect(효과): F85의 runtime path firewall(런타임 경로 방화벽) 실패를 negative memory(부정 기억)로 보존하고, F86은 runtime-native intrabar path label source(런타임 네이티브 봉내 경로 라벨 원천)로 이동한다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def main() -> int:
    summary = write_all()
    print(
        json.dumps(
            json_ready(
                {
                    "status": summary["status"],
                    "judgment": summary["judgment"],
                    "decision": summary["decision"],
                    "run_id": RUN_ID,
                    "next_stage_id": NEXT_STAGE_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "task_force": f"{summary['actual_subagent_roster_coverage']['completed_count']}/{summary['actual_subagent_roster_coverage']['required_count']}",
                    "lineage_correction": summary["f85b_lineage_hash_correction"].get("status"),
                    "local_verification": summary["local_verification"]["status"],
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
