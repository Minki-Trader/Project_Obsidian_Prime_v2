from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import run267AQ_pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AR"
RUN_ID = "run267AR_stage267_pool_wide_state_feature_engineering_followup_or_adapter_branch_v1"
SOURCE_RUN_ID = source_review.RUN_ID
STATUS = "run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch_design_completed"
JUDGMENT = "followup_adapter_branch_design_completed_no_candidate_selection"
NEXT_ACTION = "run267AS_materialize_pool_wide_state_feature_engineering_followup_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_followup_or_adapter_branch"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_CANDIDATE_PROFILE_REVIEW_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_STATE_PROFILE_SUMMARY_PATH = source_review.STATE_PROFILE_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_TIER_DUPLICATE_REVIEW_PATH = source_review.TIER_DUPLICATE_REVIEW_PATH
SOURCE_TIME_SLICE_PATH = source_review.TIME_SLICE_KPI_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH

PROFILE_DECISION_PATH = RUN_ROOT / "profile_decision_matrix.csv"
CANDIDATE_DECISION_PATH = RUN_ROOT / "candidate_branch_decision_matrix.csv"
NEXT_EXPERIMENT_QUEUE_PATH = RUN_ROOT / "next_experiment_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
DESIGN_RECEIPT_PATH = RUN_ROOT / "design_receipt.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch.py")

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

BASELINE_CANDIDATES = {
    "s264_aih": ("s264_allow_inner_high_quarter", "challenger_core"),
    "s264_lc": ("s264_lowrank_control", "defensive_control"),
    "s262_lih": ("s262_lowrank_inner_half_filter", "validation_heavy"),
    "s264_aia": ("s264_allow_inner_all_oos_anchor", "oos_anchor"),
    "s258_stc": ("s258_short_tight_control", "stress_challenger"),
}
BASELINE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")

WORK_PACKET = {
    "primary_family": "experiment_design",
    "primary_skill": "obsidian-experiment-design",
    "support_skills": "obsidian-result-judgment;obsidian-performance-attribution;obsidian-artifact-lineage",
    "required_gates": "source_authority_audit;experiment_design_schema;failure_memory_recorded;tier_duplicate_boundary_recorded;final_claim_guard",
}

PROFILE_DECISION_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_test_id",
    "state_profile",
    "net_profit",
    "profit_factor",
    "trade_count",
    "equity_drawdown_percent",
    "worst_month",
    "worst_month_net",
    "worst_slice_axis",
    "worst_slice_bucket",
    "worst_slice_net",
    "negative_month_count",
    "positive_month_ratio",
    "headline_gate",
    "weak_slice_gate",
    "profile_decision",
    "priority",
    "next_use",
    "stop_rule",
    "reopen_condition",
    "do_not_claim",
)

CANDIDATE_DECISION_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "profile_count",
    "net_profit_mean",
    "net_profit_min",
    "net_profit_max",
    "profit_factor_mean",
    "trade_count_min",
    "equity_drawdown_percent_worst",
    "worst_month_net_min",
    "worst_slice_net_min",
    "positive_month_ratio_min",
    "deep_hole_count",
    "best_profile",
    "decision_label",
    "priority",
    "next_use",
    "prune_boundary",
    "reopen_condition",
    "do_not_claim",
)

NEXT_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "materialization_readiness",
    "workstream",
    "candidate_scope",
    "profile_scope",
    "source_evidence",
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
    "next_required_artifacts",
    "claim_boundary",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "evidence",
    "affected_scope",
    "do_not_repeat",
    "salvage_angle",
    "reopen_condition",
    "boundary",
)

PERFORMANCE_ATTRIBUTION_COLUMNS = (
    "attribution_id",
    "observed_change",
    "comparison_baseline",
    "likely_drivers",
    "segment_checks",
    "trade_shape",
    "alternative_explanations",
    "attribution_confidence",
    "next_probe",
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

DESIGN_RECEIPT_COLUMNS = (
    "receipt_id",
    "receipt_type",
    "status",
    "evidence_path",
    "effect",
    "notes",
)

GATE_AUDIT_COLUMNS = ("gate_id", "status", "evidence_path", "effect", "notes")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def grouped(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, list[Mapping[str, Any]]]:
    result: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        result[str(row.get(key, ""))].append(row)
    return result


def candidate_sort_key(alias: str) -> int:
    try:
        return BASELINE_ORDER.index(alias)
    except ValueError:
        return len(BASELINE_ORDER)


def source_hashes() -> dict[str, str]:
    paths = {
        "source_review_result": SOURCE_REVIEW_RESULT_PATH,
        "source_report": SOURCE_REPORT_PATH,
        "source_candidate_profile_review": SOURCE_CANDIDATE_PROFILE_REVIEW_PATH,
        "source_candidate_summary": SOURCE_CANDIDATE_SUMMARY_PATH,
        "source_state_profile_summary": SOURCE_STATE_PROFILE_SUMMARY_PATH,
        "source_negative_slice_summary": SOURCE_NEGATIVE_SLICE_PATH,
        "source_tier_duplicate_review": SOURCE_TIER_DUPLICATE_REVIEW_PATH,
    }
    return {
        name: sha256_file_lf_normalized(path) if path_exists(path) else "missing"
        for name, path in paths.items()
    }


def build_profile_decisions(profile_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    ranked = sorted(profile_rows, key=lambda row: as_float(row.get("net_profit")), reverse=True)
    for row in ranked:
        alias = str(row.get("candidate_alias"))
        candidate_id, candidate_role = BASELINE_CANDIDATES.get(alias, (str(row.get("candidate_id")), str(row.get("candidate_role"))))
        net = as_float(row.get("net_profit"))
        pf = as_float(row.get("profit_factor"))
        trades = as_int(row.get("trade_count"))
        dd = as_float(row.get("report_equity_drawdown_percent"))
        worst_month_net = as_float(row.get("worst_month_net"))
        worst_slice_net = as_float(row.get("worst_slice_net"))
        positive_month_ratio = as_float(row.get("positive_month_ratio"))
        headline_ok = net >= 1000.0 and pf >= 1.50 and trades >= 290
        headline_watch = net >= 800.0 and pf >= 1.45 and trades >= 280
        deep_hole = worst_slice_net <= -250.0 or worst_month_net <= -220.0
        severe_hole = worst_slice_net <= -320.0 or worst_month_net <= -280.0
        recurring_month_hole = str(row.get("worst_month")) == "2024-12" and worst_month_net < -150.0
        if headline_ok:
            headline_gate = "pass_for_pressure_design_not_selection(압박 설계 통과, 선택 아님)"
        elif headline_watch:
            headline_gate = "watch_only_lower_headline(관찰 전용, 대표 숫자 낮음)"
        else:
            headline_gate = "low_priority_or_prune(낮은 우선순위 또는 가지치기)"
        if severe_hole:
            weak_slice_gate = "fail_severe_slice_hole(심한 구간 구멍 실패)"
        elif deep_hole or recurring_month_hole:
            weak_slice_gate = "fail_deep_slice_hole(깊은 구간 구멍 실패)"
        else:
            weak_slice_gate = "watch_slice_pressure_required(구간 압박 필요)"
        if alias == "s258_stc" and net >= 1300:
            priority = "P0"
            decision = "stress_challenger_headline_pressure_only(압박 도전자 대표숫자 압박 전용)"
            next_use = "stress_test_noncalendar_slice_pressure_before_adapter_watch(어댑터 관찰 전 비달력 구간 압박)"
        elif alias == "s264_aih" and net >= 1200:
            priority = "P0"
            decision = "core_challenger_pressure_required(핵심 도전자 압박 필요)"
            next_use = "core_challenger_noncalendar_december_monday_pressure(핵심 도전자 비달력 12월/월요일 압박)"
        elif alias == "s264_aia" and (dd <= 15.5 or str(row.get("review_read", "")).startswith("constructive")):
            priority = "P0"
            decision = "oos_anchor_adapter_watch_if_slice_pressure_survives(구간 압박 생존 시 표본외 앵커 어댑터 관찰)"
            next_use = "adapter_watch_only_after_slice_gate_improves(구간 게이트 개선 뒤 어댑터 관찰 전용)"
        elif alias in {"s264_lc", "s262_lih"} and headline_ok:
            priority = "P1"
            decision = "control_profile_audit_not_adapter_selection(통제 프로필 감사, 어댑터 선택 아님)"
            next_use = "control_audit_against_challenger_pressure(도전자 압박 대비 통제 감사)"
        elif headline_watch:
            priority = "P1"
            decision = "constructive_watch_but_no_branch_selection(건설적 관찰, 분기 선택 아님)"
            next_use = "watch_only_or_prune_if_next_pressure_fails(관찰 전용 또는 다음 압박 실패 시 가지치기)"
        else:
            priority = "P2"
            decision = "low_priority_prune_unless_role_needed(역할 필요 없으면 낮은 우선순위 가지치기)"
            next_use = "failure_memory_or_control_only(실패 기억 또는 통제 전용)"
        decisions.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": candidate_role,
                "source_test_id": row.get("source_test_id"),
                "state_profile": row.get("state_profile"),
                "net_profit": net,
                "profit_factor": pf,
                "trade_count": trades,
                "equity_drawdown_percent": dd,
                "worst_month": row.get("worst_month"),
                "worst_month_net": worst_month_net,
                "worst_slice_axis": row.get("worst_slice_axis"),
                "worst_slice_bucket": row.get("worst_slice_bucket"),
                "worst_slice_net": worst_slice_net,
                "negative_month_count": as_int(row.get("negative_month_count")),
                "positive_month_ratio": positive_month_ratio,
                "headline_gate": headline_gate,
                "weak_slice_gate": weak_slice_gate,
                "profile_decision": decision,
                "priority": priority,
                "next_use": next_use,
                "stop_rule": "stop_or_prune_if_noncalendar_pressure_keeps_Monday_or_2024_12_below_minus_200(비달력 압박 후에도 월요일/2024-12가 -200 아래면 중단 또는 가지치기)",
                "reopen_condition": "reopen_only_if_next_MT5_review_reduces_deep_slice_without_calendar_filter(다음 MT5 검토가 달력 필터 없이 깊은 구간을 줄일 때만 재개)",
                "do_not_claim": "no_selected_candidate_no_ONNX_no_goal_achieve(선택 후보/ONNX/목표 달성 주장 금지)",
            }
        )
    return decisions


def build_candidate_decisions(profile_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_candidate = grouped(profile_decisions, "candidate_alias")
    rows: list[dict[str, Any]] = []
    for alias in BASELINE_ORDER:
        items = by_candidate.get(alias, [])
        candidate_id, candidate_role = BASELINE_CANDIDATES[alias]
        if not items:
            rows.append(
                {
                    "candidate_alias": alias,
                    "candidate_id": candidate_id,
                    "candidate_role": candidate_role,
                    "profile_count": 0,
                    "decision_label": "missing_required(필수 누락)",
                    "priority": "blocked",
                    "next_use": "blocked_until_source_profile_rows_exist(원천 프로필 행 생성 전 차단)",
                    "prune_boundary": "do_not_prune_from_missing_design_alone(설계 누락만으로 가지치기 금지)",
                    "reopen_condition": "source_profile_review_rebuilt(원천 프로필 검토 재생성)",
                    "do_not_claim": "no_candidate_selection(후보 선택 금지)",
                }
            )
            continue
        nets = [as_float(row.get("net_profit")) for row in items]
        pfs = [as_float(row.get("profit_factor")) for row in items]
        trades = [as_int(row.get("trade_count")) for row in items]
        dds = [as_float(row.get("equity_drawdown_percent")) for row in items]
        worst_months = [as_float(row.get("worst_month_net")) for row in items]
        worst_slices = [as_float(row.get("worst_slice_net")) for row in items]
        positive_months = [as_float(row.get("positive_month_ratio")) for row in items]
        deep_hole_count = sum(1 for row in items if "fail_" in str(row.get("weak_slice_gate")))
        best_profile = max(items, key=lambda row: as_float(row.get("net_profit")))
        if alias == "s264_aih":
            label = "retain_core_challenger_but_require_slice_pressure(핵심 도전자는 유지하되 구간 압박 필요)"
            priority = "P0"
            next_use = "core_challenger_pressure_branch(핵심 도전자 압박 분기)"
        elif alias == "s258_stc":
            label = "retain_stress_challenger_only_under_deep_pressure(깊은 압박 조건에서만 압박 도전자 유지)"
            priority = "P0"
            next_use = "stress_challenger_prune_or_rescue_gate(압박 도전자 가지치기 또는 회수 게이트)"
        elif alias == "s264_aia":
            label = "retain_oos_anchor_adapter_watch_with_gate(게이트 포함 표본외 앵커 어댑터 관찰 유지)"
            priority = "P0"
            next_use = "adapter_watch_if_DD_edge_survives_slice_pressure(구간 압박 후 손실폭 장점 생존 시 어댑터 관찰)"
        elif alias == "s264_lc":
            label = "retain_defensive_control_no_candidate_selection(방어 통제 유지, 후보 선택 아님)"
            priority = "P1"
            next_use = "defensive_control_audit(방어 통제 감사)"
        else:
            label = "retain_validation_heavy_control_no_candidate_selection(검증 중심 통제 유지, 후보 선택 아님)"
            priority = "P1"
            next_use = "validation_heavy_control_audit(검증 중심 통제 감사)"
        rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": candidate_role,
                "profile_count": len(items),
                "net_profit_mean": mean(nets),
                "net_profit_min": min(nets),
                "net_profit_max": max(nets),
                "profit_factor_mean": mean(pfs),
                "trade_count_min": min(trades),
                "equity_drawdown_percent_worst": max(dds),
                "worst_month_net_min": min(worst_months),
                "worst_slice_net_min": min(worst_slices),
                "positive_month_ratio_min": min(positive_months),
                "deep_hole_count": deep_hole_count,
                "best_profile": f"{best_profile.get('source_test_id')}::{best_profile.get('state_profile')}",
                "decision_label": label,
                "priority": priority,
                "next_use": next_use,
                "prune_boundary": "do_not_prune_pool_role_until_next_pressure_review(다음 압박 검토 전 후보군 역할 자체는 가지치기 금지)",
                "reopen_condition": "next_MT5_review_reduces_Monday_2024_12_holes_without_calendar_filter(다음 MT5 검토가 달력 필터 없이 월요일/2024-12 구멍을 줄임)",
                "do_not_claim": "no_selected_candidate_no_ONNX_no_goal_achieve(선택 후보/ONNX/목표 달성 주장 금지)",
            }
        )
    return rows


def build_next_queue(candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    p0_candidates = ";".join(
        str(row.get("candidate_alias")) for row in candidate_decisions if str(row.get("priority")) == "P0"
    )
    p1_candidates = ";".join(
        str(row.get("candidate_alias")) for row in candidate_decisions if str(row.get("priority")) == "P1"
    )
    return [
        {
            "queue_id": "run267AS_q01_noncalendar_slice_pressure_matrix",
            "priority": "P0",
            "materialization_readiness": "ready_for_score_table_materialization(점수표 물질화 준비됨)",
            "workstream": "noncalendar_slice_resilience_pressure(비달력 구간 견고성 압박)",
            "candidate_scope": p0_candidates,
            "profile_scope": "high_headline_or_constructive_profiles_with_Monday_and_2024_12_holes(대표 숫자 높거나 건설적이나 월요일/2024-12 구멍 보유 프로필)",
            "source_evidence": rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH),
            "hypothesis": "noncalendar_state_interactions_can_reduce_recurring_Monday_and_2024_12_holes_without_direct_calendar_filter(비달력 상태 상호작용이 직접 달력 필터 없이 반복 월요일/2024-12 구멍을 줄일 수 있다)",
            "decision_use": "decide_whether_any_P0_candidate_deserves_adapter_watch_after_pressure(압박 뒤 P0 후보가 어댑터 관찰 가치가 있는지 판단)",
            "comparison_baseline": "run267AQ_profile_decision_matrix_and_run267B_2024_base(267AQ 프로필 결정과 267B 2024 기준)",
            "control_variables": "FPMarkets_US100_M5;2024_historical_window;existing_model_bundle_identity;no_retraining_unless_explicit(심볼/시간프레임/기간/모델 정체성 고정, 명시 전 재학습 없음)",
            "changed_variables": "state_score_table_terms_for_volatility_trend_risk_interactions_not_calendar_labels(달력 라벨이 아닌 변동성/추세/위험 상호작용 상태 점수표 항)",
            "sample_scope": "Tier A primary plus Tier A+B duplicate-boundary reports until real_fallback_probe_is_designed(Tier A 우선 및 실제 대체 설계 전 Tier A+B 중복 경계)",
            "success_criteria": "net_profit_and_PF_remain_strong;Monday_and_2024_12_above_minus_200;DD_not_worse;trade_count_not_thin(순수익/PF 유지, 월요일/2024-12 -200 위, 손실폭 악화 없음, 거래 수 얇지 않음)",
            "failure_criteria": "headline_only_improves_but_deep_slice_remains_or_trade_count_thins(대표 숫자만 개선되고 깊은 구간 또는 얇은 거래 수 유지)",
            "invalid_conditions": "calendar_filter_leakage;feature_order_break;missing_MT5_report;Tier_A_B_synthetic_sum_claim(달력 필터 누수/피처 순서 파손/MT5 보고서 누락/합성 합산 주장)",
            "stop_conditions": "one_materialized_pressure_pass_then_prune_or_redirect_if_holes_persist(물질화 압박 1회 후 구멍 지속 시 가지치기 또는 방향 전환)",
            "evidence_plan": "score_table_manifest;runtime_contract;attempt_manifest;MT5_KPI;trade_records;curve_time_slice_review;failure_memory(점수표/런타임 계약/시도 목록/MT5 KPI/거래/곡선 구간 검토/실패 기억)",
            "next_required_artifacts": "state_pressure_design.csv;score_table_manifest.csv;attempts.csv;run267AT_review(상태 압박 설계/점수표/시도/후속 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267AS_q02_candidate_role_pressure_and_prune_gate",
            "priority": "P0",
            "materialization_readiness": "ready_for_design_matrix(설계 행렬 준비됨)",
            "workstream": "candidate_role_pressure_gate(후보 역할 압박 게이트)",
            "candidate_scope": p0_candidates,
            "profile_scope": "candidate_role_specific_best_and_worst_profiles(후보 역할별 최선/최악 프로필)",
            "source_evidence": rel(CANDIDATE_DECISION_PATH),
            "hypothesis": "P0_roles_have_different_failure_shapes_and_should_not_share_one_repair(우선 후보 역할마다 실패 모양이 달라 하나의 수리를 공유하면 안 된다)",
            "decision_use": "split_keep_watch_or_prune_for_core_challenger_oos_anchor_stress_challenger(핵심 도전자/표본외 앵커/압박 도전자의 유지/관찰/가지치기 분리)",
            "comparison_baseline": "run267AQ_candidate_decision_matrix(267AQ 후보 결정 행렬)",
            "control_variables": "same_risk_ATR_surface_and_report_parser(동일 위험/ATR 표면과 보고서 파서)",
            "changed_variables": "candidate_role_specific_stop_rules_and_materialization_priority(후보 역할별 중단 규칙과 물질화 우선순위)",
            "sample_scope": "candidate_pool_all_five_with_P0_focus(다섯 후보 전체, P0 집중)",
            "success_criteria": "each_candidate_has_explicit_keep_prune_reopen_condition(각 후보가 유지/가지치기/재개 조건을 가짐)",
            "failure_criteria": "queue_collapses_back_to_single_candidate_micro_tuning(큐가 단일 후보 미세조정으로 되돌아감)",
            "invalid_conditions": "candidate_role_missing_or_source_profile_rows_missing(후보 역할 또는 원천 프로필 행 누락)",
            "stop_conditions": "if_P0_pressure_fails_do_not_extend_same_repair_more_than_one_more_stage(P0 압박 실패 시 같은 수리를 한 단계 이상 늘리지 않음)",
            "evidence_plan": "candidate_decision_matrix;failure_memory;next_materialization_result(후보 결정/실패 기억/다음 물질화 결과)",
            "next_required_artifacts": "candidate_role_pressure_matrix.csv;failure_memory.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267AS_q03_defensive_validation_control_audit",
            "priority": "P1",
            "materialization_readiness": "ready_if_P0_queue_materializes(우선 큐 물질화 시 준비)",
            "workstream": "control_audit(통제 감사)",
            "candidate_scope": p1_candidates,
            "profile_scope": "defensive_and_validation_heavy_profiles(방어 및 검증 중심 프로필)",
            "source_evidence": rel(CANDIDATE_DECISION_PATH),
            "hypothesis": "controls_can_show_whether_P0_improvement_is_candidate_specific_or_score_table_general(통제가 P0 개선이 후보 특이인지 점수표 일반 효과인지 보여줄 수 있다)",
            "decision_use": "keep_or_prune_controls_after_P0_pressure(우선 압박 뒤 통제 유지/가지치기 결정)",
            "comparison_baseline": "s264_lc_defensive_control_and_s262_lih_validation_heavy_control(방어 통제와 검증 중심 통제)",
            "control_variables": "same_2024_window_same_parser_same_score_table_family(같은 2024 기간/파서/점수표 계열)",
            "changed_variables": "control_audit_only_no_adapter_branch(통제 감사 전용, 어댑터 분기 없음)",
            "sample_scope": "Tier A primary with duplicate-boundary audit(Tier A 우선 및 중복 경계 감사)",
            "success_criteria": "controls_explain_general_vs_candidate_specific_effect(통제가 일반 효과와 후보 특이 효과를 분리)",
            "failure_criteria": "controls_move_identically_to_challengers_and_do_not_distinguish_roles(통제가 도전자와 동일하게 움직여 역할을 구분하지 못함)",
            "invalid_conditions": "control_rows_missing_or_candidate_alias_mismatch(통제 행 누락 또는 후보 별칭 불일치)",
            "stop_conditions": "keep_as_control_only_or_archive_if_no_longer_informative(정보 가치 없으면 통제 전용 유지 또는 보관)",
            "evidence_plan": "control_kpi;curve_review;role_delta_matrix(통제 KPI/곡선 검토/역할 차이 행렬)",
            "next_required_artifacts": "control_audit_matrix.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267AS_q04_real_tier_b_fallback_probe_design",
            "priority": "P1_deferred",
            "materialization_readiness": "deferred_until_noncalendar_pressure_survives(비달력 압박 생존 전 보류)",
            "workstream": "real_fallback_boundary_design(실제 대체 경계 설계)",
            "candidate_scope": "survivors_only_after_run267AS_run267AT(267AS/267AT 이후 생존 후보만)",
            "profile_scope": "not_applicable_until_survivor_exists(생존 후보 전 해당 없음)",
            "source_evidence": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "hypothesis": "Tier_A_B_duplicate_boundary_must_be_replaced_by_real_fallback_evidence_before_runtime_reproduction(런타임 재현 전 Tier A+B 중복 경계는 실제 대체 근거로 바뀌어야 한다)",
            "decision_use": "prevent_duplicate_combined_result_from_becoming_robustness_claim(중복 합산 결과가 견고성 주장으로 바뀌는 것을 방지)",
            "comparison_baseline": "run267AQ_tier_duplicate_review(267AQ 티어 중복 검토)",
            "control_variables": "no_synthetic_sum_as_actual_routed_total(합성 합산을 실제 라우팅 전체로 말하지 않음)",
            "changed_variables": "design_only_real_fallback_manifest_required(설계 전용, 실제 대체 목록 필요)",
            "sample_scope": "blocked_or_deferred_until_real_Tier_B_fallback_manifest_exists(실제 Tier B 대체 목록 전 차단 또는 보류)",
            "success_criteria": "fallback_manifest_names_primary_used_fallback_used_actual_routed_total(대체 목록이 우선 사용/대체 사용/실제 라우팅 전체를 명명)",
            "failure_criteria": "duplicate_boundary_persists_without_route_counts(경로 수 없이 중복 경계 지속)",
            "invalid_conditions": "synthetic_sum_reported_as_routed_total(합성 합산을 라우팅 전체로 보고)",
            "stop_conditions": "do_not_start_runtime_reproduction_until_real_fallback_boundary_exists(실제 대체 경계 전 런타임 재현 시작 금지)",
            "evidence_plan": "fallback_manifest;route_count_KPI;component_boundary_report(대체 목록/경로 수 KPI/구성 경계 보고)",
            "next_required_artifacts": "fallback_probe_design.md;fallback_manifest.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267AS_q05_no_single_calendar_repair_guard",
            "priority": "P2_guardrail",
            "materialization_readiness": "guardrail_only(가드레일 전용)",
            "workstream": "anti_bottleneck_guard(병목 방지 가드)",
            "candidate_scope": "all_candidates(전체 후보)",
            "profile_scope": "all_profiles_with_Monday_or_2024_12_weakness(월요일 또는 2024-12 약점 전체 프로필)",
            "source_evidence": rel(FAILURE_MEMORY_PATH),
            "hypothesis": "direct_calendar_repair_would_overfit_the_current_weak_slice(직접 달력 수리는 현재 약한 구간에 과적합될 가능성이 높다)",
            "decision_use": "block_single_month_or_single_weekday_micro_tuning(단일 월/요일 미세조정 차단)",
            "comparison_baseline": "run267AQ_negative_slice_summary(267AQ 음수 구간 요약)",
            "control_variables": "weak_slices_are_evaluation_gates_not_entry_filters(약한 구간은 평가 게이트이지 진입 필터가 아님)",
            "changed_variables": "none_guardrail_only(변경 없음, 가드레일 전용)",
            "sample_scope": "design_guardrail_for_next_queue(다음 큐 설계 가드레일)",
            "success_criteria": "next_queue_materializes_structural_state_features_not_calendar_filters(다음 큐가 달력 필터가 아닌 구조 상태 피처를 물질화)",
            "failure_criteria": "next_queue_targets_only_Monday_or_December_thresholds(다음 큐가 월요일 또는 12월 임계값만 겨냥)",
            "invalid_conditions": "guardrail_removed_without_documented_reason(문서화된 이유 없이 가드 제거)",
            "stop_conditions": "stop_repair_loop_if_same_slice_target_repeats_after_one_more_pass(한 번 더 수행 후 같은 구간 목표가 반복되면 수리 루프 중단)",
            "evidence_plan": "gate_audit;failure_memory;materialization_review(게이트 감사/실패 기억/물질화 검토)",
            "next_required_artifacts": "gate_audit.csv;failure_memory.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory(profile_decisions: Sequence[Mapping[str, Any]], candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    worst_profile = min(profile_decisions, key=lambda row: as_float(row.get("worst_slice_net"))) if profile_decisions else {}
    memories = [
        {
            "memory_id": "run267AR_m01_recurring_monday_and_december_holes",
            "pattern": "headline_good_but_Monday_or_2024_12_holes(대표 숫자는 좋지만 월요일 또는 2024-12 구멍)",
            "evidence": f"negative Tier A slices(음수 Tier A 구간)=99;worst={worst_profile.get('candidate_alias')}::{worst_profile.get('state_profile')} {worst_profile.get('worst_slice_net')}",
            "affected_scope": "all_candidates(전체 후보)",
            "do_not_repeat": "do_not_add_direct_Monday_or_December_entry_filter_as_first_response(첫 대응으로 직접 월요일/12월 진입 필터 추가 금지)",
            "salvage_angle": "use_noncalendar_volatility_trend_risk_state_pressure(비달력 변동성/추세/위험 상태 압박 사용)",
            "reopen_condition": "deep_slice_improves_without_calendar_filter(달력 필터 없이 깊은 구간 개선)",
            "boundary": "failure_memory_not_candidate_selection(실패 기억, 후보 선택 아님)",
        },
        {
            "memory_id": "run267AR_m02_tier_ab_duplicate_boundary",
            "pattern": "Tier_A_B_duplicate_boundary_not_real_fallback(Tier A+B 중복 경계, 실제 대체 아님)",
            "evidence": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "affected_scope": "runtime_reproduction_and_fallback_claims(런타임 재현 및 대체 주장)",
            "do_not_repeat": "do_not_call_duplicate_Tier_A_B_robustness_or_actual_routed_total(중복 Tier A+B를 견고성 또는 실제 라우팅 전체로 부르지 않음)",
            "salvage_angle": "design_real_fallback_manifest_after_survivor_exists(생존 후보 뒤 실제 대체 목록 설계)",
            "reopen_condition": "primary_used_fallback_used_actual_routed_total_are_measured(우선 사용/대체 사용/실제 라우팅 전체가 측정됨)",
            "boundary": "deferred_design_guardrail(보류 설계 가드레일)",
        },
        {
            "memory_id": "run267AR_m03_high_headline_not_adapter_selection",
            "pattern": "high_net_profit_does_not_override_curve_holes(높은 순수익이 곡선 구멍을 덮지 않음)",
            "evidence": rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH),
            "affected_scope": "s258_stc;s264_aih;s264_aia",
            "do_not_repeat": "do_not_start_ONNX_or_adapter_handoff_from_headline_KPI_only(대표 KPI만으로 ONNX 또는 어댑터 인계 시작 금지)",
            "salvage_angle": "pressure_high_headline_profiles_against_named_weak_slices(대표 숫자 높은 프로필을 명명 약한 구간으로 압박)",
            "reopen_condition": "candidate_reduces_deep_slice_and_keeps_trade_count_profit_DD_bundle(후보가 깊은 구간을 줄이고 거래수/수익/손실폭 묶음을 유지)",
            "boundary": "research_development_only(연구개발 전용)",
        },
    ]
    for row in candidate_decisions:
        if as_int(row.get("deep_hole_count")) <= 0:
            continue
        alias = str(row.get("candidate_alias"))
        memories.append(
            {
                "memory_id": f"run267AR_m_candidate_{alias}",
                "pattern": f"{alias}_deep_slice_hole_count={row.get('deep_hole_count')}",
                "evidence": f"net_min={row.get('net_profit_min')};worst_slice={row.get('worst_slice_net_min')};worst_month={row.get('worst_month_net_min')}",
                "affected_scope": alias,
                "do_not_repeat": "do_not_treat_role_label_as_survival_evidence(역할 라벨을 생존 근거처럼 쓰지 않음)",
                "salvage_angle": str(row.get("next_use")),
                "reopen_condition": str(row.get("reopen_condition")),
                "boundary": "candidate_role_memory_no_selection(후보 역할 기억, 선택 아님)",
            }
        )
    return memories


def build_performance_attribution(profile_decisions: Sequence[Mapping[str, Any]], candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    top = max(profile_decisions, key=lambda row: as_float(row.get("net_profit"))) if profile_decisions else {}
    deepest = min(profile_decisions, key=lambda row: as_float(row.get("worst_slice_net"))) if profile_decisions else {}
    return [
        {
            "attribution_id": "run267AR_a01_headline_improvement_with_slice_holes",
            "observed_change": f"top profile(최상위 프로필)={top.get('candidate_alias')}::{top.get('state_profile')} net={top.get('net_profit')} PF={top.get('profit_factor')}",
            "comparison_baseline": "run267B_2024_base_and_run267AQ_review(267B 2024 기준 및 267AQ 검토)",
            "likely_drivers": "state_feature_score_table_extension_not_retraining(상태 피처 점수표 확장, 재학습 아님)",
            "segment_checks": f"deepest slice(최심 구간)={deepest.get('candidate_alias')}::{deepest.get('worst_slice_axis')}/{deepest.get('worst_slice_bucket')} {deepest.get('worst_slice_net')}",
            "trade_shape": "trade_count_remains_roughly_280_to_321_but_slice_quality_is_uneven(거래 수는 대략 280~321이나 구간 품질이 고르지 않음)",
            "alternative_explanations": "single_2024_period_fit_or_score_table_accident_remains_possible(단일 2024 기간 적합 또는 점수표 우연 가능성 잔존)",
            "attribution_confidence": "medium_for_design_only(설계 한정 중간)",
            "next_probe": "run267AS_noncalendar_pressure_materialization(267AS 비달력 압박 물질화)",
        },
        {
            "attribution_id": "run267AR_a02_candidate_roles_are_not_equivalent",
            "observed_change": ";".join(
                f"{row.get('candidate_alias')}:mean={as_float(row.get('net_profit_mean')):.2f},min={as_float(row.get('net_profit_min')):.2f},hole={row.get('deep_hole_count')}"
                for row in candidate_decisions
            ),
            "comparison_baseline": "five_candidate_pool_roles(다섯 후보군 역할)",
            "likely_drivers": "candidate_source_surfaces_and_state_profiles_interact_differently(후보 원천 표면과 상태 프로필 상호작용 차이)",
            "segment_checks": "all_candidates_have_deep_hole_count_gt_0(모든 후보가 깊은 구멍 수 0 초과)",
            "trade_shape": "trade_count_not_thin_but_weak_slice_loss_concentrates(거래 수는 얇지 않지만 약한 구간 손실 집중)",
            "alternative_explanations": "candidate_role_may_reflect_same_underlying_score_table_behavior(후보 역할이 같은 기본 점수표 행동일 수도 있음)",
            "attribution_confidence": "medium_low_until_next_pressure(다음 압박 전 중하)",
            "next_probe": "candidate_role_pressure_and_control_audit(후보 역할 압박과 통제 감사)",
        },
    ]


def build_result_judgment(profile_decisions: Sequence[Mapping[str, Any]], candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"profile_decisions={len(profile_decisions)};candidate_decisions={len(candidate_decisions)};source={rel(SOURCE_REVIEW_RESULT_PATH)}",
            "evidence_missing": "new_MT5_execution;multi_period_pressure;real_Tier_B_fallback;ONNX_parity;runtime_reproduction(새 MT5 실행/다기간 압박/실제 Tier B 대체/ONNX 동등성/런타임 재현)",
            "judgment_label": "exploratory_design_completed_no_candidate_selection(탐색 설계 완료, 후보 선택 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "좋은 숫자는 보였지만 깊은 구간 구멍이 남아 다음은 구조 압박 설계다.",
        },
        {
            "result_subject": "baseline_candidate_pool(기준 후보군)",
            "evidence_available": f"all five candidates reviewed(다섯 후보 검토);deep_hole_candidates={sum(1 for row in candidate_decisions if as_int(row.get('deep_hole_count')) > 0)}",
            "evidence_missing": "candidate_that_survives_slice_pressure_without_calendar_filter(달력 필터 없이 구간 압박을 생존한 후보)",
            "judgment_label": "retain_pool_for_pressure_not_selection(압박용 후보군 유지, 선택 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run267AS/run267AT must show reduced holes before adapter watch(267AS/267AT가 구멍 축소를 보여야 어댑터 관찰 가능)",
            "user_explanation_hook": "후보군은 아직 살아 있지만, 바로 고를 후보는 없다.",
        },
    ]


def build_design_receipt(next_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    required = (
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
    )
    missing = [
        f"{row.get('queue_id')}:{field}"
        for row in next_queue
        for field in required
        if not str(row.get(field, "")).strip()
    ]
    return [
        {
            "receipt_id": "run267AR_experiment_design_schema",
            "receipt_type": "experiment_design(실험 설계)",
            "status": "completed" if not missing else "missing_required",
            "evidence_path": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "effect": "each_queue_row_names_hypothesis_decision_controls_changed_variables_success_failure_invalid_stop_and_evidence_plan(각 큐 행이 가설/결정/고정/변경/성공/실패/무효/중단/근거 계획을 명명)",
            "notes": ";".join(missing) if missing else f"queue_rows={len(next_queue)}",
        },
        {
            "receipt_id": "run267AR_claim_boundary",
            "receipt_type": "final_claim_guard(최종 주장 가드)",
            "status": "completed",
            "evidence_path": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected_candidate_ONNX_goal_achieve_not_claimed(선택 후보/ONNX/목표 달성 미주장)",
            "notes": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(
    profile_decisions: Sequence[Mapping[str, Any]],
    candidate_decisions: Sequence[Mapping[str, Any]],
    failure_memory: Sequence[Mapping[str, Any]],
    next_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_authority_audit",
            "status": "completed",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267AR_uses_run267AQ_review_not_memory(267AR는 기억이 아니라 267AQ 검토를 사용)",
            "notes": f"profile_decisions={len(profile_decisions)};candidate_decisions={len(candidate_decisions)}",
        },
        {
            "gate_id": "experiment_design_schema",
            "status": "completed",
            "evidence_path": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "effect": "next_queue_has_required_experiment_design_fields(다음 큐가 필수 실험 설계 필드를 가짐)",
            "notes": f"queue_rows={len(next_queue)}",
        },
        {
            "gate_id": "failure_memory_recorded",
            "status": "completed",
            "evidence_path": rel(FAILURE_MEMORY_PATH),
            "effect": "failed_patterns_become_do_not_repeat_and_reopen_conditions(실패 패턴이 반복 금지와 재개 조건으로 남음)",
            "notes": f"failure_memory_rows={len(failure_memory)}",
        },
        {
            "gate_id": "tier_duplicate_boundary_recorded",
            "status": "completed",
            "evidence_path": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "effect": "Tier_A_B_duplicate_is_not_used_as_fallback_robustness(Tier A+B 중복을 대체 견고성으로 쓰지 않음)",
            "notes": "real_fallback_probe_deferred_until_survivor_exists",
        },
        {
            "gate_id": "final_claim_guard",
            "status": "completed",
            "evidence_path": rel(RESULT_JUDGMENT_PATH),
            "effect": "no_selected_candidate_no_ONNX_no_goal_achieve(선택 후보/ONNX/목표 달성 없음)",
            "notes": CLAIM_BOUNDARY,
        },
    ]


def build_lineage(output_paths: Mapping[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_inputs": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "report": rel(SOURCE_REPORT_PATH),
            "candidate_profile_review": rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH),
            "candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "state_profile_summary": rel(SOURCE_STATE_PROFILE_SUMMARY_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "tier_duplicate_review": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
        },
        "source_hashes": source_hashes(),
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": {name: rel(path) for name, path in output_paths.items()},
        "artifact_hashes": "registered_after_write_in_docs/registers/artifact_registry.csv(작성 후 산출물 등록부에 기록)",
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY_PATH),
            "alpha_run_ledger": rel(PROJECT_LEDGER_PATH),
            "stage_run_ledger": rel(STAGE_LEDGER_PATH),
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
        },
        "availability": "tracked_after_commit(커밋 후 추적)",
        "lineage_judgment": "connected_with_boundary(경계부 연결)",
        "boundary": "design_only_no_new_MT5_no_candidate_selection_no_ONNX(설계 전용, 새 MT5 없음, 후보 선택 없음, ONNX 없음)",
    }


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def remove_line_prefix(text: str, prefix: str) -> str:
    lines = [line for line in text.splitlines() if not line.startswith(prefix)]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def update_workspace_state_text(text: str, result: Mapping[str, Any]) -> str:
    focus_marker = "run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch_report_path"
    focus_line = (
        "  Stage267(267단계) run267AR(267AR 실행) pool-wide state feature engineering follow-up/Adapter branch design"
        f"(후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계) `{STATUS}`. Effect(효과): run267AQ(267AQ 실행)의 "
        "깊은 Monday(월요일)/2024-12(2024년 12월) 구멍을 next experiment queue(다음 실험 큐), failure memory(실패 기억), "
        "candidate role decision(후보 역할 결정)으로 바꿨고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_focus = focus_marker in text
    inserted_stage_path = focus_marker in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not inserted_focus:
            output.append(line)
            output.append("- >-")
            output.append(focus_line)
            output.append(f"  {focus_marker}: {rel(REPORT_PATH)}")
            inserted_focus = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
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
            if stripped.startswith("decision_path:") and not inserted_stage_path:
                output.append(f"  {focus_marker}: {rel(REPORT_PATH)}")
                inserted_stage_path = True
        output.append(line)
    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- Stage267(267단계) run267AR pool-wide state feature engineering follow-up/Adapter branch design"
        f"(후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        "- latest_design(최신 설계): run267AR(267AR 실행) "
        f"profile decisions(프로필 결정) `{len(result['profile_decisions'])}`, "
        f"candidate decisions(후보 결정) `{len(result['candidate_decisions'])}`, "
        f"queue rows(큐 행) `{len(result['next_experiment_queue'])}`, "
        f"failure memory(실패 기억) `{len(result['failure_memory'])}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    summary = (
        "Run267AR(267AR 실행)는 run267AQ(267AQ 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 "
        "candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.\n"
        "Effect(효과): 높은 headline KPI(대표 핵심 성과 지표)를 바로 선택하지 않고, Monday(월요일), 2024-12(2024년 12월), "
        "Tier A+B duplicate boundary(Tier A+B 중복 경계)를 다음 압박 조건으로 만든다.\n"
        "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 없다."
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
        else:
            text = remove_line_prefix(text, "- stage_status(")
        text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
        if path == CURRENT_WORKING_STATE_PATH:
            text = remove_line_prefix(text, "- last_completed_run(")
            text = replace_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_followup_or_adapter_branch`")
            text = append_after_contains(text, "stage267_run267AQ_pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
            text = append_after_contains(text, "Run267AQ(267AQ 실행)", summary)
        else:
            text = replace_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267AQ_pool_wide_state_feature_engineering_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "Run267AQ(267AQ 실행)", summary)
        text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace, result))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "scoreboard": "experiment_design_queue_from_trade_shape_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"profile_decisions={len(result['profile_decisions'])};"
                    f"candidate_decisions={len(result['candidate_decisions'])};"
                    f"queue_rows={len(result['next_experiment_queue'])};"
                    f"failure_memory={len(result['failure_memory'])};next_action={NEXT_ACTION}."
                ),
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"Run267AR design queue from run267AQ review; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "kpi_scope": "experiment_design_queue_failure_memory_result_judgment",
                "scoreboard_lane": "followup_adapter_branch_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": (
                    f"profile_decisions={len(result['profile_decisions'])};"
                    f"candidate_decisions={len(result['candidate_decisions'])};"
                    f"queue_rows={len(result['next_experiment_queue'])}"
                ),
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_design_only_no_new_MT5",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    entries = (
        ("stage267_run267AR_design_script", "producer_script", PRODUCER_PATH, "Builds run267AR follow-up/Adapter branch design."),
        ("stage267_run267AR_profile_decision_matrix", "decision_matrix", PROFILE_DECISION_PATH, "Run267AR profile-level pressure decisions."),
        ("stage267_run267AR_candidate_decision_matrix", "decision_matrix", CANDIDATE_DECISION_PATH, "Run267AR candidate branch decisions."),
        ("stage267_run267AR_next_experiment_queue", "design_queue", NEXT_EXPERIMENT_QUEUE_PATH, "Run267AR next experiment queue."),
        ("stage267_run267AR_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267AR failure memory."),
        ("stage267_run267AR_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267AR performance attribution."),
        ("stage267_run267AR_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AR result judgment."),
        ("stage267_run267AR_design_receipt", "design_receipt", DESIGN_RECEIPT_PATH, "Run267AR experiment design receipt."),
        ("stage267_run267AR_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267AR gate audit."),
        ("stage267_run267AR_lineage", "artifact_lineage", LINEAGE_PATH, "Run267AR artifact lineage."),
        ("stage267_run267AR_review_result", "review_result", REVIEW_RESULT_PATH, "Run267AR JSON result."),
        ("stage267_run267AR_report", "review_report", REPORT_PATH, "User-facing run267AR design report."),
    )
    registry_rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
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
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = result["candidate_decisions"]
    queue_rows = result["next_experiment_queue"]
    profile_rows = result["profile_decisions"][:12]
    lines = [
        "# Stage267 Run267AR Pool-wide State Feature Engineering Follow-up/Adapter Branch Design(267단계 267AR 후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계)",
        "",
        "- action(행동): run267AQ(267AQ 실행)의 profile review(프로필 검토)를 candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.",
        "- effect(효과): 높은 headline KPI(대표 핵심 성과 지표)를 바로 고르지 않고, Monday(월요일), 2024-12(2024년 12월), Tier A+B duplicate boundary(Tier A+B 중복 경계)를 다음 압박 조건으로 쓴다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- profile_decisions(프로필 결정): `{len(result['profile_decisions'])}`",
        f"- candidate_decisions(후보 결정): `{len(candidate_rows)}`",
        f"- next_queue_rows(다음 큐 행): `{len(queue_rows)}`",
        f"- failure_memory(실패 기억): `{len(result['failure_memory'])}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267AQ(267AQ 실행)는 숫자가 좋아진 후보를 많이 만들었다. 하지만 모든 후보에 깊은 구간 구멍이 남았다.",
        "Effect(효과): run267AR(267AR 실행)는 후보를 고르는 단계가 아니라, 누가 다음 압박을 받을지와 무엇을 반복하지 않을지를 정한다.",
        "",
        "가장 중요한 경계는 Tier A+B(Tier A+B 합산)다. 이번 Tier A+B는 duplicate boundary(중복 경계)라서 real fallback(실제 대체) 근거가 아니다.",
        "Effect(효과): runtime reproduction(런타임 재현)이나 ONNX parity(ONNX 동등성) 쪽으로 가기 전에 실제 fallback manifest(대체 목록)가 따로 필요하다.",
        "",
        "## Candidate Decisions(후보 결정)",
        "",
        "| candidate(후보) | role(역할) | mean net(평균 순수익) | min net(최소 순수익) | worst slice(최악 구간) | holes(구멍) | decision(결정) | next use(다음 용도) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in candidate_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | {as_float(row.get('net_profit_mean')):.2f} | "
            f"{as_float(row.get('net_profit_min')):.2f} | {as_float(row.get('worst_slice_net_min')):.2f} | "
            f"{as_int(row.get('deep_hole_count'))} | `{row.get('decision_label')}` | `{row.get('next_use')}` |"
        )
    lines.extend(
        [
            "",
            "## Top Profile Pressure Rows(상위 프로필 압박 행)",
            "",
            "| candidate(후보) | source(원천) | profile(프로필) | net(순수익) | PF(수익 팩터) | worst slice(최악 구간) | gate(게이트) | next use(다음 용도) |",
            "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in profile_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('source_test_id')}` | `{row.get('state_profile')}` | "
            f"{as_float(row.get('net_profit')):.2f} | {as_float(row.get('profit_factor')):.2f} | "
            f"`{row.get('worst_slice_axis')}`/`{row.get('worst_slice_bucket')}` {as_float(row.get('worst_slice_net')):.2f} | "
            f"`{row.get('weak_slice_gate')}` | `{row.get('next_use')}` |"
        )
    lines.extend(
        [
            "",
            "## Next Experiment Queue(다음 실험 큐)",
            "",
            "| priority(우선순위) | queue(큐) | workstream(작업 흐름) | candidate scope(후보 범위) | decision use(결정 용도) | stop(중단) |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row.get('priority')}` | `{row.get('queue_id')}` | `{row.get('workstream')}` | "
            f"`{row.get('candidate_scope')}` | `{row.get('decision_use')}` | `{row.get('stop_conditions')}` |"
        )
    lines.extend(
        [
            "",
            "## Experiment Design Receipt(실험 설계 기록)",
            "",
            "- hypothesis/decision_use/comparison/control/changed/sample/success/failure/invalid/stop/evidence fields(가설/결정/비교/고정/변경/표본/성공/실패/무효/중단/근거 필드)는 `next_experiment_queue.csv`에 기록했다.",
            "- failure memory(실패 기억)는 single Monday/December repair(단일 월요일/12월 수리), Tier A+B duplicate boundary(Tier A+B 중복 경계), headline-only selection(대표 숫자만 보고 선택)을 반복 금지로 남긴다.",
            "- claim boundary(주장 경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_REVIEW_RESULT_PATH)}`, `{rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH)}`, `{rel(SOURCE_NEGATIVE_SLICE_PATH)}`, `{rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{NEXT_ACTION}`.",
            f"- artifact_paths(산출물 경로): `{rel(PROFILE_DECISION_PATH)}`, `{rel(CANDIDATE_DECISION_PATH)}`, `{rel(NEXT_EXPERIMENT_QUEUE_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_result() -> dict[str, Any]:
    source_payload = read_json(SOURCE_REVIEW_RESULT_PATH)
    profile_rows = read_csv(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH)
    profile_decisions = build_profile_decisions(profile_rows)
    candidate_decisions = build_candidate_decisions(profile_decisions)
    next_queue = build_next_queue(candidate_decisions)
    failure_memory = build_failure_memory(profile_decisions, candidate_decisions)
    performance = build_performance_attribution(profile_decisions, candidate_decisions)
    judgment = build_result_judgment(profile_decisions, candidate_decisions)
    design_receipt = build_design_receipt(next_queue)
    gate_audit = build_gate_audit(profile_decisions, candidate_decisions, failure_memory, next_queue)
    output_paths = {
        "profile_decision_matrix": PROFILE_DECISION_PATH,
        "candidate_branch_decision_matrix": CANDIDATE_DECISION_PATH,
        "next_experiment_queue": NEXT_EXPERIMENT_QUEUE_PATH,
        "failure_memory": FAILURE_MEMORY_PATH,
        "performance_attribution": PERFORMANCE_ATTRIBUTION_PATH,
        "result_judgment": RESULT_JUDGMENT_PATH,
        "design_receipt": DESIGN_RECEIPT_PATH,
        "gate_audit": GATE_AUDIT_PATH,
        "lineage": LINEAGE_PATH,
        "review_result": REVIEW_RESULT_PATH,
        "report": REPORT_PATH,
    }
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_summary": {
            "source_status": source_payload.get("status"),
            "source_trade_record_count": source_payload.get("trade_record_count"),
            "source_negative_slice_count": len(source_payload.get("negative_slices", [])),
            "source_parser_errors": len(source_payload.get("parser_errors", [])),
        },
        "profile_decisions": profile_decisions,
        "candidate_decisions": candidate_decisions,
        "next_experiment_queue": next_queue,
        "failure_memory": failure_memory,
        "performance_attribution": performance,
        "result_judgment": judgment,
        "design_receipt": design_receipt,
        "gate_audit": gate_audit,
        "lineage": build_lineage(output_paths),
        "artifacts": {name: rel(path) for name, path in output_paths.items()},
    }


def main() -> int:
    created_at = utc_now()
    result = build_result()
    write_csv(PROFILE_DECISION_PATH, result["profile_decisions"], PROFILE_DECISION_COLUMNS)
    write_csv(CANDIDATE_DECISION_PATH, result["candidate_decisions"], CANDIDATE_DECISION_COLUMNS)
    write_csv(NEXT_EXPERIMENT_QUEUE_PATH, result["next_experiment_queue"], NEXT_QUEUE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, result["performance_attribution"], PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_csv(DESIGN_RECEIPT_PATH, result["design_receipt"], DESIGN_RECEIPT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, result["gate_audit"], GATE_AUDIT_COLUMNS)
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_truth_docs(result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "profile_decisions": len(result["profile_decisions"]),
                "candidate_decisions": len(result["candidate_decisions"]),
                "queue_rows": len(result["next_experiment_queue"]),
                "failure_memory": len(result["failure_memory"]),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
