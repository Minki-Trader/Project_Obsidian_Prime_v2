from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267DO_runtime_gap_aware_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267DP"
RUN_ID = "run267DP_stage267_runtime_gap_aware_fourth_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267DP_runtime_gap_aware_fourth_followup_or_prune_design_completed"
JUDGMENT = "runtime_gap_aware_fourth_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267DQ_materialize_runtime_gap_aware_fourth_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_fourth_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_CANDIDATE_RUNTIME_GAP_SUMMARY_PATH = source_review.CANDIDATE_RUNTIME_GAP_SUMMARY_PATH
SOURCE_ATTEMPT_OUTCOME_PATH = source_review.ATTEMPT_OUTCOME_REVIEW_PATH
SOURCE_ATTRIBUTION_PATH = source_review.ATTRIBUTION_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

FEATURE_BLUEPRINT_PATH = RUN_ROOT / "feature_blueprint.csv"
BRANCH_DECISION_PATH = RUN_ROOT / "branch_decision_matrix.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DP_runtime_gap_aware_fourth_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DP_runtime_gap_aware_fourth_followup_or_prune_design.py")

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_review.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_review.ARTIFACT_COLUMNS

FEATURE_BLUEPRINT_COLUMNS = (
    "feature_id",
    "candidate_aliases",
    "candidate_ids",
    "feature_family",
    "market_meaning",
    "source_evidence",
    "changed_variables",
    "held_variables",
    "aggressive_or_defensive",
    "success_read",
    "failure_read",
    "materialization_note",
    "claim_boundary",
)

BRANCH_DECISION_COLUMNS = (
    "decision_id",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_attempts",
    "runtime_completed",
    "runtime_blocked",
    "completed_profile_rows",
    "best_or_reference_net_profit",
    "best_or_reference_profit_factor",
    "max_dd_percent",
    "worst_month_net",
    "decision_label",
    "next_use",
    "why",
    "reopen_condition",
    "claim_boundary",
)

MATERIALIZATION_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "candidate_aliases",
    "candidate_ids",
    "workstream",
    "source_evidence",
    "changed_variables",
    "control_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "runtime_instruction",
    "claim_boundary",
)

PRUNE_COLUMNS = (
    "prune_id",
    "affected_candidate_aliases",
    "affected_attempts",
    "prune_label",
    "why_pruned",
    "salvage_value",
    "reopen_condition",
    "do_not_repeat",
    "claim_boundary",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "affected_scope",
    "why_failed",
    "salvage_value",
    "reopen_condition",
    "do_not_repeat",
    "claim_boundary",
)

PERFORMANCE_ATTRIBUTION_COLUMNS = (
    "candidate_alias",
    "observed_change",
    "comparison_baseline",
    "likely_drivers",
    "segment_checks",
    "trade_shape",
    "alternative_explanations",
    "attribution_confidence",
    "next_probe",
    "claim_boundary",
)

EXPERIMENT_DESIGN_COLUMNS = (
    "design_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "claim_boundary",
)

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)

GATE_AUDIT_COLUMNS = (
    "gate_id",
    "gate_name",
    "status",
    "evidence",
    "effect",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    output: list[str] = []
    for line in lines:
        if line.startswith(prefix):
            output.append(replacement)
            changed = True
        else:
            output.append(line)
    if not changed:
        output.append(replacement)
    return "\n".join(output) + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    output: list[str] = []
    inserted = False
    for item in lines:
        output.append(item)
        if not inserted and needle in item:
            output.append(line)
            inserted = True
    if not inserted:
        output.append(line)
    return "\n".join(output) + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    if focus_block.strip() in text:
        return text
    return text.replace("current_focus:\n", "current_focus:\n" + focus_block, 1)


def update_stage267_workspace_block(text: str) -> str:
    report_line = f"  run267DP_runtime_gap_aware_fourth_followup_or_prune_design_report_path: {rel(REPORT_PATH)}"
    if report_line not in text:
        text = append_after_contains(
            text,
            "run267DO_runtime_gap_aware_balance_timeslice_trade_quality_review_report_path",
            report_line,
        )
    output: list[str] = []
    in_block = False
    for line in text.splitlines():
        if line == "stage267_baseline_candidate_racing_protocol:":
            in_block = True
            output.append(line)
            continue
        if in_block and line and not line.startswith(" "):
            in_block = False
        if in_block:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    return "\n".join(output) + "\n"


def source_maps() -> dict[str, Any]:
    candidate_gap_rows = read_csv_rows(SOURCE_CANDIDATE_RUNTIME_GAP_SUMMARY_PATH)
    profile_rows = read_csv_rows(SOURCE_CANDIDATE_PROFILE_PATH)
    attribution_rows = read_csv_rows(SOURCE_ATTRIBUTION_PATH)
    return {
        "candidate_gap_by_alias": {row["candidate_alias"]: row for row in candidate_gap_rows},
        "profiles": profile_rows,
        "attribution_by_alias": {row["candidate_alias"]: row for row in attribution_rows},
    }


def gap(alias: str, maps: Mapping[str, Any], field: str, default: str = "") -> str:
    return str(maps["candidate_gap_by_alias"].get(alias, {}).get(field, default))


def profile(alias: str, maps: Mapping[str, Any], split_contains: str = "") -> dict[str, str]:
    rows = [row for row in maps["profiles"] if row.get("candidate_alias") == alias]
    if split_contains:
        rows = [row for row in rows if split_contains in row.get("split", "")]
    return rows[0] if rows else {}


def build_feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "bp267dp_s258_supply_shape_continuity",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "feature_family": "supply_shape_continuity(공급 형태 연속성)",
            "market_meaning": "sidefilter_open(사이드필터 개방)이 만든 거래 공급을 유지하면서 2025 구간 품질 감쇠를 분리한다.",
            "source_evidence": "run267DO completed profiles(완료 프로필) 3 rows, blocked threshold_release(차단 임계값 해제) 3 rows.",
            "changed_variables": "supply-side signal shape(공급측 신호 형태), late-period quality decay flag(후반 품질 감쇠 표식).",
            "held_variables": "threshold_release(임계값 해제)는 현 상태로 재시도하지 않는다.",
            "aggressive_or_defensive": "aggressive(공격형)",
            "success_read": "2023H2/2025H1/2025H2 모두 거래 수와 PF(profit factor, 수익 팩터)가 유지되고 DD(drawdown, 손실폭)가 덜 벌어진다.",
            "failure_read": "2025H1/H2 품질 감쇠가 그대로이거나 무거래/런타임 공백이 반복된다.",
            "materialization_note": "P0 queue(우선 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dp_s258_monday_late_session_dd_taper",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "feature_family": "risk_shape_taper(위험 형태 완화)",
            "market_meaning": "2025H2의 Monday(월요일), late session(후반 세션), weak hour(약한 시간) 손실 집중을 거래 차단이 아니라 위험 형태로 줄인다.",
            "source_evidence": "run267DO s258 profile(프로필): 2025H2 worst month(최약 월) 2025-12 -136.08, weakest weekday(최약 요일) Monday -60.47.",
            "changed_variables": "time-slice risk taper(시간 구간 위험 완화), late-session exposure cap(후반 세션 노출 제한).",
            "held_variables": "entry source(진입 원천)와 supply-side activation(공급측 활성화)은 유지한다.",
            "aggressive_or_defensive": "aggressive_risk_shaped(공격형 위험조정)",
            "success_read": "거래 수를 크게 줄이지 않으면서 2025H2 DD(손실폭)와 월별 구멍이 낮아진다.",
            "failure_read": "거래 공급이 얇아지거나 2023H2 장점까지 지워진다.",
            "materialization_note": "P0 queue(우선 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dp_s264_lc_defensive_dd_zoom",
            "candidate_aliases": "s264_lc",
            "candidate_ids": "s264_lowrank_control",
            "feature_family": "defensive_dd_zoom(방어형 손실폭 확대검토)",
            "market_meaning": "수익과 거래 수는 있지만 방어 대조 후보로도 불편한 2024-06, Monday(월요일), session_07_12(7-12 세션) 구멍을 확대해서 본다.",
            "source_evidence": "run267DO s264_lc net 1522.61, PF 1.418226, trades 473, max DD 24.39, worst month 2024-06 -163.98.",
            "changed_variables": "DD zoom audit(손실폭 확대 감사), weak-slice attribution(약한 구간 귀속).",
            "held_variables": "candidate role(후보 역할)은 defensive control(방어 대조)로 고정한다.",
            "aggressive_or_defensive": "defensive_control(방어 대조)",
            "success_read": "방어 대조로 남길 수 있는 위험 경계와 버릴 조건이 명확해진다.",
            "failure_read": "DD(손실폭)가 구조적이면 확장하지 않고 대조 기록으로만 남긴다.",
            "materialization_note": "P0 control queue(우선 대조 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dp_s264_aia_s262_lih_supply_rebuild_diagnostic",
            "candidate_aliases": "s264_aia;s262_lih",
            "candidate_ids": "s264_allow_inner_all_oos_anchor;s262_lowrank_inner_half_filter",
            "feature_family": "signal_supply_rebuild_diagnostic(신호 공급 재구축 진단)",
            "market_meaning": "무거래와 런타임 공백이 반복된 후보는 바로 MT5(MetaTrader 5, 메타트레이더5)에 다시 보내지 않고 먼저 신호 공급 증명을 요구한다.",
            "source_evidence": "run267DO s264_aia completed 0/4, s262_lih completed 0/2, retry recovered KPI 0.",
            "changed_variables": "pre-runtime supply manifest(런타임 전 공급 목록), nonzero activation proof(비영 신호 활성 증명).",
            "held_variables": "current similarity/ablation and guardrail crosscheck(현재 유사/제거 및 가드레일 교차확인)는 재시도하지 않는다.",
            "aggressive_or_defensive": "diagnostic_only(진단 전용)",
            "success_read": "MT5 실행 전에 nonzero signal count(비영 신호 수)가 증명된다.",
            "failure_read": "공급 증명 없이 재시도하려는 경우 gate(관문)에서 멈춘다.",
            "materialization_note": "P1 diagnostic queue(진단 대기열)이며 MT5 실행은 보류한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_decisions(maps: Mapping[str, Any]) -> list[dict[str, Any]]:
    s258_2023 = profile("s258_stc", maps, "2023")
    s264_lc = profile("s264_lc", maps)
    return [
        {
            "decision_id": "bd267dp_s258_advance_supply_shape_not_threshold_release",
            "candidate_alias": "s258_stc",
            "candidate_id": "s258_short_tight_control",
            "candidate_role": "stress_challenger(압박 도전자)",
            "source_attempts": gap("s258_stc", maps, "attempt_count"),
            "runtime_completed": gap("s258_stc", maps, "runtime_completed_attempts"),
            "runtime_blocked": gap("s258_stc", maps, "runtime_blocked_attempts"),
            "completed_profile_rows": gap("s258_stc", maps, "completed_profile_rows"),
            "best_or_reference_net_profit": s258_2023.get("net_profit", ""),
            "best_or_reference_profit_factor": s258_2023.get("profit_factor", ""),
            "max_dd_percent": gap("s258_stc", maps, "max_completed_dd_percent"),
            "worst_month_net": gap("s258_stc", maps, "worst_completed_month_net"),
            "decision_label": "advance_aggressive_supply_shape_but_not_threshold_release(공격형 공급 형태는 진행하되 임계값 해제는 금지)",
            "next_use": "P0 aggressive queue(우선 공격형 대기열)",
            "why": "sidefilter_open(사이드필터 개방)은 거래를 만들었지만 threshold_release(임계값 해제)는 무거래/런타임 공백을 반복했다.",
            "reopen_condition": "2025H1/H2 quality decay(품질 감쇠)를 DD(손실폭)와 거래 수를 함께 보며 줄일 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dp_s264_lc_keep_defensive_dd_zoom_only",
            "candidate_alias": "s264_lc",
            "candidate_id": "s264_lowrank_control",
            "candidate_role": "defensive_control(방어 대조)",
            "source_attempts": gap("s264_lc", maps, "attempt_count"),
            "runtime_completed": gap("s264_lc", maps, "runtime_completed_attempts"),
            "runtime_blocked": gap("s264_lc", maps, "runtime_blocked_attempts"),
            "completed_profile_rows": gap("s264_lc", maps, "completed_profile_rows"),
            "best_or_reference_net_profit": s264_lc.get("net_profit", ""),
            "best_or_reference_profit_factor": s264_lc.get("profit_factor", ""),
            "max_dd_percent": gap("s264_lc", maps, "max_completed_dd_percent"),
            "worst_month_net": gap("s264_lc", maps, "worst_completed_month_net"),
            "decision_label": "keep_defensive_control_dd_zoom_only(방어 대조 손실폭 확대검토 전용 유지)",
            "next_use": "P0 defensive control queue(우선 방어 대조 대기열)",
            "why": "수익과 거래 수는 있으나 2024-06, Monday(월요일), session_07_12(7-12 세션) DD(손실폭)가 불편하다.",
            "reopen_condition": "DD cluster(손실폭 묶음)가 구조적으로 설명되고 완화될 때만 확장한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dp_s264_aia_prune_current_runtime_gap_route",
            "candidate_alias": "s264_aia",
            "candidate_id": "s264_allow_inner_all_oos_anchor",
            "candidate_role": "oos_anchor(표본외 앵커)",
            "source_attempts": gap("s264_aia", maps, "attempt_count"),
            "runtime_completed": gap("s264_aia", maps, "runtime_completed_attempts"),
            "runtime_blocked": gap("s264_aia", maps, "runtime_blocked_attempts"),
            "completed_profile_rows": gap("s264_aia", maps, "completed_profile_rows"),
            "best_or_reference_net_profit": "",
            "best_or_reference_profit_factor": "",
            "max_dd_percent": "",
            "worst_month_net": "",
            "decision_label": "prune_current_similarity_ablation_runtime_gap(현재 유사/제거 런타임 공백 가지치기)",
            "next_use": "P1 supply rebuild diagnostic only(신호 공급 재구축 진단 전용)",
            "why": "4개 시도가 모두 무거래/차단으로 끝났고 재시도 회복 KPI(핵심 성과 지표)가 없다.",
            "reopen_condition": "pre-runtime supply manifest(런타임 전 공급 목록)가 비영 신호를 증명할 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dp_s262_lih_prune_current_guardrail_crosscheck",
            "candidate_alias": "s262_lih",
            "candidate_id": "s262_lowrank_inner_half_filter",
            "candidate_role": "validation_heavy(검증 중심)",
            "source_attempts": gap("s262_lih", maps, "attempt_count"),
            "runtime_completed": gap("s262_lih", maps, "runtime_completed_attempts"),
            "runtime_blocked": gap("s262_lih", maps, "runtime_blocked_attempts"),
            "completed_profile_rows": gap("s262_lih", maps, "completed_profile_rows"),
            "best_or_reference_net_profit": "",
            "best_or_reference_profit_factor": "",
            "max_dd_percent": "",
            "worst_month_net": "",
            "decision_label": "prune_current_guardrail_until_supply_repaired(공급 수리 전 현재 가드레일 가지치기)",
            "next_use": "P1 supply rebuild diagnostic only(신호 공급 재구축 진단 전용)",
            "why": "2개 시도 모두 무거래/차단으로 끝나 validation-heavy(검증 중심) 역할을 확인할 거래 근거가 없다.",
            "reopen_condition": "guardrail(가드레일)이 거래 공급을 먼저 만든다는 증거가 생길 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dp_s264_aih_preserve_prior_core_challenger_watch",
            "candidate_alias": "s264_aih",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_role": "core_challenger(핵심 도전자)",
            "source_attempts": "0 in run267DO",
            "runtime_completed": "0 in run267DO",
            "runtime_blocked": "0 in run267DO",
            "completed_profile_rows": "0 in run267DO",
            "best_or_reference_net_profit": "",
            "best_or_reference_profit_factor": "",
            "max_dd_percent": "",
            "worst_month_net": "",
            "decision_label": "preserve_prior_core_challenger_watch_not_materialized_here(이전 핵심 도전자 관찰 보존, 이번 물질화 제외)",
            "next_use": "watchlist only(관찰 목록 전용)",
            "why": "run267DO 직접 근거에는 없으므로 이번 queue(대기열)에 억지로 섞지 않는다.",
            "reopen_condition": "prior evidence(이전 근거)와 새 signal supply proof(신호 공급 증명)를 함께 연결할 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "q01_s258_supply_shape_continuity_cross_period",
            "priority": "P0",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "aggressive_supply_shape_continuity(공격형 공급 형태 연속성)",
            "source_evidence": "run267DO s258 sidefilter_open(사이드필터 개방) completed 3 profiles.",
            "changed_variables": "supply shape score(공급 형태 점수), quality decay flag(품질 감쇠 표식).",
            "control_variables": "same splits(동일 구간) 2023H2/2025H1/2025H2, same candidate identity(동일 후보 정체성).",
            "sample_scope": "adjacent_2023_h2_train_pre_2024;adjacent_2025_h1_validation_post_2024;adjacent_2025_h2_oos_followthrough.",
            "success_criteria": "trade count(거래 수) 유지, PF(수익 팩터) 2025 감쇠 완화, DD(손실폭) 악화 없음.",
            "failure_criteria": "zero trade(무거래), runtime gap(런타임 공백), 2025 품질 추가 붕괴.",
            "invalid_conditions": "feature/order mismatch(피처/순서 불일치), missing report(보고서 누락), parser mismatch(파서 불일치).",
            "runtime_instruction": "materialize for next MT5 queue(다음 MT5 대기열로 물질화).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_s258_monday_late_session_dd_taper_cross_period",
            "priority": "P0",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "risk_shape_taper(위험 형태 완화)",
            "source_evidence": "run267DO weak slices(약한 구간): 2025H2 Monday(월요일), session_21_23(21-23 세션), hour 19/21.",
            "changed_variables": "time-slice risk taper(시간 구간 위험 완화), exposure cap(노출 제한).",
            "control_variables": "sidefilter_open activation(사이드필터 개방 활성화), candidate model identity(후보 모델 정체성).",
            "sample_scope": "2023H2/2025H1/2025H2 cross-period(확장 기간).",
            "success_criteria": "DD(손실폭)와 worst month(최약 월)가 줄고 거래 수가 급감하지 않는다.",
            "failure_criteria": "2023H2 강점이 사라지거나 거래 수가 너무 얇아진다.",
            "invalid_conditions": "risk taper(위험 완화)가 entry signal(진입 신호)을 몰래 바꾸면 무효.",
            "runtime_instruction": "materialize for next MT5 queue(다음 MT5 대기열로 물질화).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s264_lc_defensive_dd_zoom_control",
            "priority": "P0_control",
            "candidate_aliases": "s264_lc",
            "candidate_ids": "s264_lowrank_control",
            "workstream": "defensive_control_dd_zoom(방어 대조 손실폭 확대검토)",
            "source_evidence": "run267DO s264_lc net 1522.61, PF 1.418226, trades 473, max DD 24.39.",
            "changed_variables": "DD cluster zoom(손실폭 묶음 확대검토), month/weekday/session attribution(월/요일/세션 귀속).",
            "control_variables": "defensive control role(방어 대조 역할), historical_2024 sample(2024 과거 표본).",
            "sample_scope": "historical_2024 Tier A and duplicate-boundary Tier A+B(Tier A와 중복 경계 Tier A+B).",
            "success_criteria": "방어 대조로 남길 수 있는 위험 경계가 명확해진다.",
            "failure_criteria": "DD(손실폭)가 구조적으로 불편하면 확장 중지.",
            "invalid_conditions": "duplicate-boundary row(중복 경계 행)를 true fallback(진짜 대체)으로 오해하면 무효.",
            "runtime_instruction": "materialize as control probe(대조 탐침으로 물질화).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_s264_aia_s262_lih_supply_rebuild_diagnostic_no_mt5",
            "priority": "P1_diagnostic",
            "candidate_aliases": "s264_aia;s262_lih",
            "candidate_ids": "s264_allow_inner_all_oos_anchor;s262_lowrank_inner_half_filter",
            "workstream": "pre_runtime_signal_supply_diagnostic(런타임 전 신호 공급 진단)",
            "source_evidence": "run267DO current routes(현재 경로) completed 0 and recovered KPI 0.",
            "changed_variables": "nonzero signal manifest(비영 신호 목록), supply count audit(공급 수 감사).",
            "control_variables": "no MT5 retry until nonzero supply proof(비영 공급 증명 전 MT5 재시도 금지).",
            "sample_scope": "historical_2024 diagnostic only(2024 과거 진단 전용).",
            "success_criteria": "MT5 전 단계에서 nonzero activation(비영 활성화)이 증명된다.",
            "failure_criteria": "무거래 조건이 그대로면 current route(현재 경로)는 닫는다.",
            "invalid_conditions": "supply proof(공급 증명) 없이 runtime attempt(런타임 시도)를 만들면 무효.",
            "runtime_instruction": "diagnostic only; do not schedule MT5 yet(진단 전용, 아직 MT5 배정 금지).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "pr267dp_s258_threshold_release_no_blind_retry",
            "affected_candidate_aliases": "s258_stc",
            "affected_attempts": "run267dl_03;run267dl_05;run267dl_07",
            "prune_label": "no_blind_retry(맹목 재시도 금지)",
            "why_pruned": "threshold_release(임계값 해제)는 3개 구간 모두 무거래/런타임 공백이었다.",
            "salvage_value": "sidefilter_open(사이드필터 개방)의 공급 형태 비교 재료.",
            "reopen_condition": "threshold axis(임계값 축)가 공급 수를 먼저 회복한다는 증거가 있을 때.",
            "do_not_repeat": "같은 threshold_release(임계값 해제)를 MT5에 바로 재시도하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dp_s264_aia_similarity_ablation_route",
            "affected_candidate_aliases": "s264_aia",
            "affected_attempts": "run267dl_01;run267dl_02",
            "prune_label": "prune_current_runtime_gap_route(현재 런타임 공백 경로 가지치기)",
            "why_pruned": "similar/ablation survivor(유사/제거 생존) 경로가 2024에서 4개 차단/무거래였다.",
            "salvage_value": "OOS anchor(표본외 앵커) 역할은 보존하되 현재 경로는 공급 증명 전까지 보류.",
            "reopen_condition": "feature surface rebuild(피처 표면 재구축)와 nonzero signal count(비영 신호 수)가 있을 때.",
            "do_not_repeat": "같은 유사/제거 runtime attempt(런타임 시도)를 반복하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dp_s262_lih_guardrail_crosscheck",
            "affected_candidate_aliases": "s262_lih",
            "affected_attempts": "run267dl_09",
            "prune_label": "prune_until_signal_supply_repaired(신호 공급 수리 전 가지치기)",
            "why_pruned": "validation guardrail crosscheck(검증 가드레일 교차확인)가 2024에서 거래 공급을 만들지 못했다.",
            "salvage_value": "validation-heavy(검증 중심) 역할은 이후 공급 진단에서 다시 볼 수 있다.",
            "reopen_condition": "guardrail(가드레일)이 nonzero activation(비영 활성화)을 만든다는 증거.",
            "do_not_repeat": "무거래 가드레일을 같은 형태로 재시도하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dp_repeated_runtime_retry_loop",
            "affected_candidate_aliases": "s264_aia;s262_lih;s258_stc_threshold_release",
            "affected_attempts": "run267DN retries",
            "prune_label": "stop_retry_loop(재시도 반복 중지)",
            "why_pruned": "9개 재시도에서 recovered KPI(회복 핵심 성과 지표)가 0이었다.",
            "salvage_value": "blocked condition(차단 조건)을 failure memory(실패 기억)로 보존.",
            "reopen_condition": "handoff/tooling repair(인계/도구 수리)나 signal supply proof(신호 공급 증명)가 있을 때.",
            "do_not_repeat": "같은 공백을 3 stage(3단계) 이상 끌지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "fm267dp_zero_trade_runtime_gap_not_weak_kpi",
            "pattern": "zero_trade_plus_runtime_gap(무거래와 런타임 공백)",
            "affected_scope": "s264_aia;s262_lih;s258_threshold_release",
            "why_failed": "KPI(핵심 성과 지표)가 약한 것이 아니라 거래 근거 자체가 없었다.",
            "salvage_value": "supply proof gate(공급 증명 관문)로 다음 실험을 보호한다.",
            "reopen_condition": "nonzero signal count(비영 신호 수)와 report parser match(보고서 파서 일치)가 있을 때.",
            "do_not_repeat": "무거래 보고서를 성과 비교에 넣지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dp_s258_supply_exists_quality_decays",
            "pattern": "s258_supply_exists_but_2025_quality_decays(s258 공급은 있으나 2025 품질 감쇠)",
            "affected_scope": "s258_stc sidefilter_open(사이드필터 개방)",
            "why_failed": "2023H2는 강하지만 2025H1/H2에서 PF(수익 팩터)와 DD(손실폭)가 약해졌다.",
            "salvage_value": "공급을 죽이지 않고 risk shape(위험 형태)을 조정하는 방향.",
            "reopen_condition": "2025 quality decay(품질 감쇠)가 줄고 거래 수가 유지될 때.",
            "do_not_repeat": "품질 감쇠를 더 좁은 필터만으로 누르지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dp_s264_lc_profit_but_dd_uncomfortable",
            "pattern": "profit_with_uncomfortable_dd(수익은 있으나 손실폭 불편)",
            "affected_scope": "s264_lc",
            "why_failed": "net/PF(순수익/수익 팩터)는 좋지만 2024-06, Monday(월요일), session_07_12(7-12 세션) 약점이 크다.",
            "salvage_value": "defensive control(방어 대조)로 쓰며 DD zoom(손실폭 확대검토)을 수행한다.",
            "reopen_condition": "DD cluster(손실폭 묶음)가 설명되고 낮아질 때.",
            "do_not_repeat": "수익 숫자만 보고 후보 선택을 말하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dp_s264_aih_prior_watch_not_current_evidence",
            "pattern": "prior_core_challenger_not_in_current_review(이전 핵심 도전자가 현재 검토에는 없음)",
            "affected_scope": "s264_aih",
            "why_failed": "run267DO 직접 근거가 없어서 이번 queue(대기열)에 섞으면 근거 경계가 흐려진다.",
            "salvage_value": "prior research utilization(이전 연구 활용) 관찰 목록으로 보존.",
            "reopen_condition": "이전 근거와 새 공급 증명이 같은 artifact lineage(산출물 계보)로 연결될 때.",
            "do_not_repeat": "이름값만으로 현재 설계에 끼워 넣지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_performance_attribution(maps: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for alias in ("s258_stc", "s264_lc", "s264_aia", "s262_lih"):
        source = maps["attribution_by_alias"].get(alias, {})
        rows.append(
            {
                "candidate_alias": alias,
                "observed_change": source.get("observed_change", ""),
                "comparison_baseline": source.get("comparison_baseline", "run267DO source attribution(원천 귀속)"),
                "likely_drivers": source.get("likely_drivers", ""),
                "segment_checks": source.get("segment_checks", ""),
                "trade_shape": source.get("trade_shape", ""),
                "alternative_explanations": source.get("alternative_explanations", ""),
                "attribution_confidence": source.get("attribution_confidence", "low"),
                "next_probe": source.get("next_probe", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "candidate_alias": "s264_aih",
            "observed_change": "not present in run267DO direct evidence(267DO 직접 근거 없음)",
            "comparison_baseline": "prior Stage267 failure memory and candidate role(이전 267단계 실패 기억과 후보 역할)",
            "likely_drivers": "prior core challenger(이전 핵심 도전자) 역할은 보존하되 현재 runtime gap review(런타임 공백 검토)의 직접 입력은 아니다.",
            "segment_checks": "missing in this review(이번 검토에서 없음)",
            "trade_shape": "not measured here(여기서 측정하지 않음)",
            "alternative_explanations": "excluding it avoids stale assumption(오래된 가정 방지).",
            "attribution_confidence": "low_boundary_only(낮음, 경계 전용)",
            "next_probe": "reopen only with linked prior evidence and supply proof(이전 근거와 공급 증명 연결 시 재개)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_experiment_design_receipt() -> list[dict[str, Any]]:
    return [
        {
            "design_id": "ed267dp_runtime_gap_aware_fourth_followup_or_prune",
            "hypothesis": "runtime gap(런타임 공백)을 KPI weakness(KPI 약점)와 분리하면, 다음 실험은 무거래 재시도가 아니라 살아 있는 공급 축과 방어 대조 축으로 좁혀질 수 있다.",
            "decision_use": "run267DQ materialization queue(267DQ 물질화 대기열)의 우선순위와 가지치기 범위를 정한다.",
            "comparison_baseline": "run267DO candidate_runtime_gap_summary(후보 런타임 공백 요약), candidate_profile_review(후보 프로필 검토).",
            "control_variables": "baseline candidate pool(기준 후보군), period splits(기간 구간), no selected candidate claim(선택 후보 주장 금지), no ONNX claim(ONNX 주장 금지).",
            "changed_variables": "s258 supply shape(공급 형태), s258 risk taper(위험 완화), s264_lc DD zoom(손실폭 확대검토), s264_aia/s262 supply diagnostics(공급 진단).",
            "sample_scope": "historical_2024, adjacent_2023H2, adjacent_2025H1, adjacent_2025H2.",
            "success_criteria": "next queue(다음 대기열)가 거래 공급을 유지하면서 약한 구간을 덜 악화시키고, 무거래 경로를 재시도하지 않는다.",
            "failure_criteria": "새 설계가 threshold micro-tuning(임계값 미세조정) 또는 blind runtime retry(맹목 런타임 재시도)로 변질된다.",
            "invalid_conditions": "runtime output(런타임 출력), report(보고서), parser check(파서 확인), artifact registry(산출물 등록부)가 끊기면 무효.",
            "stop_conditions": "같은 runtime gap repair(런타임 공백 수리)를 2개 stage(단계) 이상 끌지 않고 공급 증명 없으면 가지친다.",
            "evidence_plan": "feature_blueprint(피처 청사진), branch_decision(분기 판단), materialization_queue(물질화 대기열), prune_matrix(가지치기 행렬), failure_memory(실패 기억), ledger(장부), artifact registry(산출물 등록부).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "run267DO review_result(검토 결과), candidate profiles(후보 프로필), runtime gap summary(런타임 공백 요약), performance attribution(성과 귀속).",
            "evidence_missing": "run267DQ materialization(물질화), MT5 execution(MT5 실행), fresh trade list(새 거래 목록), Adapter structure(어댑터 구조), ONNX parity(ONNX 동등성).",
            "judgment_label": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run267DQ must materialize only the allowed queue(허용 대기열만 물질화) and preserve prune boundaries(가지치기 경계 보존).",
            "user_explanation_hook": "이번 작업은 후보를 고르는 것이 아니라, 고르면 안 되는 경로를 막고 다음 실험 대기열을 좁히는 것이다.",
        }
    ]


def build_gate_audit() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "g01",
            "gate_name": "source_evidence_loaded(원천 근거 적재)",
            "status": "pass",
            "evidence": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267DO 근거에서 출발해 오래된 가정 사용을 줄였다.",
        },
        {
            "gate_id": "g02",
            "gate_name": "runtime_gap_honored(런타임 공백 존중)",
            "status": "pass",
            "evidence": "retry_recovered_kpi_records=0;runtime_gap_attempts=9",
            "effect": "무거래/차단 경로를 성과 후보처럼 비교하지 않았다.",
        },
        {
            "gate_id": "g03",
            "gate_name": "repair_loop_bounded(수정 반복 제한)",
            "status": "pass",
            "evidence": "prune repeated runtime retry(반복 런타임 재시도 가지치기)",
            "effect": "같은 공백을 계속 끌지 않고 공급 증명 조건으로 바꿨다.",
        },
        {
            "gate_id": "g04",
            "gate_name": "aggressive_and_control_branches_present(공격형과 대조 분기 포함)",
            "status": "pass",
            "evidence": "s258 P0 aggressive queue(공격형 대기열), s264_lc P0 control queue(대조 대기열)",
            "effect": "방어 필터만 쌓지 않고 살아 있는 공급 축도 계속 시험한다.",
        },
        {
            "gate_id": "g05",
            "gate_name": "forbidden_claim_guard(금지 주장 방어)",
            "status": "pass",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "운영/ONNX/목표 완료 주장을 만들지 않았다.",
        },
        {
            "gate_id": "g06",
            "gate_name": "artifact_lineage_connected(산출물 계보 연결)",
            "status": "pass",
            "evidence": "run_manifest(실행 목록), lineage(계보), artifact registry(산출물 등록부)",
            "effect": "다음 run267DQ가 어떤 산출물에서 출발하는지 추적 가능하다.",
        },
    ]


def source_paths() -> dict[str, str]:
    return {
        "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
        "source_candidate_profile": rel(SOURCE_CANDIDATE_PROFILE_PATH),
        "source_candidate_runtime_gap_summary": rel(SOURCE_CANDIDATE_RUNTIME_GAP_SUMMARY_PATH),
        "source_attempt_outcome": rel(SOURCE_ATTEMPT_OUTCOME_PATH),
        "source_attribution": rel(SOURCE_ATTRIBUTION_PATH),
        "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
        "source_report": rel(SOURCE_REPORT_PATH),
    }


def output_paths() -> dict[str, str]:
    return {
        "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
        "branch_decision_matrix": rel(BRANCH_DECISION_PATH),
        "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
        "prune_matrix": rel(PRUNE_MATRIX_PATH),
        "failure_memory": rel(FAILURE_MEMORY_PATH),
        "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
        "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "result_judgment": rel(RESULT_JUDGMENT_PATH),
        "gate_audit": rel(GATE_AUDIT_PATH),
        "run_manifest": rel(RUN_MANIFEST_PATH),
        "lineage": rel(LINEAGE_PATH),
        "review_result": rel(REVIEW_RESULT_PATH),
        "report": rel(REPORT_PATH),
    }


def cell(value: Any) -> str:
    text = str(value if value is not None else "")
    return text if text else "NA(없음)"


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267DP Runtime Gap Aware Fourth Follow-Up/Prune Design(267단계 267DP 런타임 공백 반영 4차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- feature_blueprints(피처 청사진): `{len(result['feature_blueprint'])}`",
        f"- branch_decisions(분기 판단): `{len(result['branch_decisions'])}`",
        f"- materialization_queue(물질화 대기열): `{len(result['materialization_queue'])}`",
        f"- prune_rows(가지치기 행): `{len(result['prune_matrix'])}`",
        f"- failure_memory(실패 기억): `{len(result['failure_memory'])}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "baseline candidate(기준 후보)를 오래 보는 이유는 후보 이름을 고르는 일이 아니라, 잘못 고르면 안 되는 근거를 걷어내는 일이기 때문이다. run267DO(267DO 실행)에서는 completed runtime(완료 런타임) 5개와 runtime gap(런타임 공백) 9개가 섞여 있었다. 이번 run267DP(267DP 실행)는 이 둘을 분리해서, 살아 있는 공급 축은 다음 실험으로 보내고 무거래/차단 경로는 재시도하지 않게 막았다.",
        "",
        "핵심은 간단하다. `s258_stc`는 sidefilter_open(사이드필터 개방)에서 거래가 생기므로 공격형으로 더 본다. `s264_lc`는 수익은 있지만 DD(drawdown, 손실폭)가 불편하므로 방어 대조로만 본다. `s264_aia`와 `s262_lih`는 현재 경로가 무거래/런타임 공백이라 MT5(MetaTrader 5, 메타트레이더5) 재시도 전에 signal supply proof(신호 공급 증명)가 필요하다. `s264_aih`는 이전 핵심 도전자 관찰 목록으로 보존하되 run267DO 직접 근거가 없어서 이번 대기열에는 억지로 넣지 않았다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | decision(판단) | next use(다음 용도) | why(이유) |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["branch_decisions"]:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['decision_label']} | {row['next_use']} | {row['why']} |"
        )
    lines.extend(
        [
            "",
            "## Materialization Queue(물질화 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | runtime instruction(런타임 지시) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["materialization_queue"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | {row['workstream']} | {row['runtime_instruction']} |"
        )
    lines.extend(
        [
            "",
            "## Prune Matrix(가지치기 행렬)",
            "",
            "| prune(가지치기) | affected(대상) | why(이유) | reopen(재개 조건) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in result["prune_matrix"]:
        lines.append(
            f"| `{row['prune_id']}` | `{row['affected_candidate_aliases']}` | {row['why_pruned']} | {row['reopen_condition']} |"
        )
    lines.extend(
        [
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- judgment_label(판정 라벨): `exploratory_design_only(탐색 설계 전용)`",
            "- evidence_available(사용 가능 근거): run267DO review_result(검토 결과), candidate profile(후보 프로필), runtime gap summary(런타임 공백 요약), performance attribution(성과 귀속).",
            "- evidence_missing(빠진 근거): run267DQ materialization(물질화), MT5 execution(MT5 실행), fresh trade list(새 거래 목록), Adapter structure(어댑터 구조), ONNX parity(ONNX 동등성).",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- source_review_result(원천 검토 결과): `{rel(SOURCE_REVIEW_RESULT_PATH)}`",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267DP_producer", "producer_script", PRODUCER_PATH, "Builds run267DP runtime-gap-aware design."),
        ("stage267_run267DP_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267DO review result."),
        ("stage267_run267DP_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Run267DP feature blueprint."),
        ("stage267_run267DP_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Run267DP branch decisions."),
        ("stage267_run267DP_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267DP materialization queue."),
        ("stage267_run267DP_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Run267DP prune matrix."),
        ("stage267_run267DP_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267DP failure memory."),
        ("stage267_run267DP_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267DP performance attribution."),
        ("stage267_run267DP_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267DP experiment design receipt."),
        ("stage267_run267DP_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267DP result judgment."),
        ("stage267_run267DP_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267DP gate audit."),
        ("stage267_run267DP_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267DP run manifest."),
        ("stage267_run267DP_lineage", "lineage", LINEAGE_PATH, "Run267DP lineage."),
        ("stage267_run267DP_review_result", "review_result", REVIEW_RESULT_PATH, "Run267DP review result."),
        ("stage267_run267DP_report", "review_report", REPORT_PATH, "User-facing run267DP report."),
    ]
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(FEATURE_BLUEPRINT_PATH, result["feature_blueprint"], FEATURE_BLUEPRINT_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, result["branch_decisions"], BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"], MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, result["prune_matrix"], PRUNE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, result["performance_attribution"], PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], EXPERIMENT_DESIGN_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, result["gate_audit"], GATE_AUDIT_COLUMNS)
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "created_at_utc": result["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "sources": result["sources"],
            "outputs": result["outputs"],
            "next_action": NEXT_ACTION,
        },
    )
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": result["sources"],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": result["outputs"],
            "artifact_hashes": "registered_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": {
                "stage_ledger": rel(STAGE_LEDGER_PATH),
                "project_ledger": rel(PROJECT_LEDGER_PATH),
                "run_registry": rel(RUN_REGISTRY_PATH),
                "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            },
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"feature_blueprints={len(result['feature_blueprint'])};"
        f"branch_decisions={len(result['branch_decisions'])};"
        f"materialization_queue={len(result['materialization_queue'])};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"runtime_gap_honored=true;next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267DP_runtime_gap_aware_fourth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_fourth_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary evidence transformed into design; true fallback not claimed",
        "scoreboard": "experiment_design_branch_decision_materialization_queue_prune_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_runtime_gap_aware_fourth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_fourth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_fourth_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_fourth_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary design evidence; true Tier B fallback not claimed",
        "kpi_scope": "experiment_design_queue_prune_failure_memory",
        "scoreboard_lane": "runtime_gap_aware_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"materialization_queue={len(result['materialization_queue'])};prune_rows={len(result['prune_matrix'])}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "not_applicable_design_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267DP_runtime_gap_aware_fourth_followup_or_prune_design"
        f"(267DP 런타임 공백 반영 4차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267DP_summary(267DP 요약): Run267DP(267DP 실행)는 run267DO(267DO 실행)의 runtime gap(런타임 공백)을 반영해 "
        f"feature blueprint(피처 청사진) `{len(result['feature_blueprint'])}`개, branch decision(분기 판단) `{len(result['branch_decisions'])}`개, "
        f"materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, prune row(가지치기 행) `{len(result['prune_matrix'])}`개로 바꿨다. "
        "Effect(효과): 무거래/차단 경로를 맹목 재시도하지 않고 살아 있는 s258 공급 축과 s264_lc 방어 대조 축으로 다음 실행을 좁힌다."
    )
    block = "\n".join(
        [
            "Run267DP(267DP 실행)는 run267DO(267DO 실행)의 completed runtime(완료 런타임)과 runtime gap(런타임 공백)을 분리해 fourth follow-up/prune design(4차 후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개, failure memory(실패 기억) `{len(result['failure_memory'])}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(
                text,
                "- adapter_under_review(검토 중 어댑터):",
                "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_fourth_followup_or_prune_design`",
            )
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267DO_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps.md", report_line)
            text = append_after_contains(text, "## Current Next Action", summary_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267DO_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps.md", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267DO_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps.md", report_line)
        text = append_block_once(text, "Run267DP(267DP 실행)는 run267DO", block)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DP(267DP 실행) runtime-gap-aware fourth follow-up/prune design"
        f"(런타임 공백 반영 4차 후속/가지치기 설계) `{STATUS}`. "
        "Effect(효과): run267DO(267DO 실행)의 completed runtime(완료 런타임)과 runtime gap(런타임 공백)을 분리해 "
        f"materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개와 prune rows(가지치기 행) `{len(result['prune_matrix'])}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_line)
    workspace = update_stage267_workspace_block(workspace)
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    for source in (
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_CANDIDATE_PROFILE_PATH,
        SOURCE_CANDIDATE_RUNTIME_GAP_SUMMARY_PATH,
        SOURCE_ATTEMPT_OUTCOME_PATH,
        SOURCE_ATTRIBUTION_PATH,
    ):
        if not path_exists(source):
            raise FileNotFoundError(source)
    maps = source_maps()
    created_at = utc_now()
    result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "feature_blueprint": build_feature_blueprints(),
        "branch_decisions": build_branch_decisions(maps),
        "materialization_queue": build_materialization_queue(),
        "prune_matrix": build_prune_matrix(),
        "failure_memory": build_failure_memory(),
        "performance_attribution": build_performance_attribution(maps),
        "experiment_design_receipt": build_experiment_design_receipt(),
        "result_judgment": build_result_judgment(),
        "gate_audit": build_gate_audit(),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": source_paths(),
        "outputs": output_paths(),
    }
    write_outputs(result)
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> int:
    result = build_result()
    print(
        json.dumps(
            {
                "status": result["status"],
                "run_id": result["run_id"],
                "feature_blueprints": len(result["feature_blueprint"]),
                "branch_decisions": len(result["branch_decisions"]),
                "materialization_queue": len(result["materialization_queue"]),
                "prune_rows": len(result["prune_matrix"]),
                "failure_memory": len(result["failure_memory"]),
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
