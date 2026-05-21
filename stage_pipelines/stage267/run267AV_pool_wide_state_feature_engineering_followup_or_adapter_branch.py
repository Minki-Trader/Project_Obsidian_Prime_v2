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
from stage_pipelines.stage267 import (
    run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review
    as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AV"
RUN_ID = "run267AV_stage267_pool_wide_state_feature_engineering_followup_or_adapter_branch_v1"
SOURCE_RUN_ID = source_review.RUN_ID
STATUS = "run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch_design_completed"
JUDGMENT = "followup_adapter_branch_design_completed_no_candidate_selection"
NEXT_ACTION = "run267AW_materialize_pool_wide_state_feature_engineering_second_followup_queue_from_run267AV_design"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_followup_or_adapter_branch"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH = source_review.CANDIDATE_FOLLOWUP_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_FOLLOWUP_PROFILE_SUMMARY_PATH = source_review.FOLLOWUP_PROFILE_SUMMARY_PATH
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
DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch.py")

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
    "s264_aih": ("s264_allow_inner_high_quarter", "challenger_core", "핵심 도전자(core challenger, 핵심 도전자)"),
    "s264_lc": ("s264_lowrank_control", "defensive_control", "방어 기준(defensive control, 방어 기준)"),
    "s262_lih": ("s262_lowrank_inner_half_filter", "validation_heavy", "검증 중심(validation-heavy, 검증 중심)"),
    "s264_aia": ("s264_allow_inner_all_oos_anchor", "oos_anchor", "표본외 앵커(OOS anchor, 표본외 앵커)"),
    "s258_stc": ("s258_short_tight_control", "stress_challenger", "압박 도전자(stress challenger, 압박 도전자)"),
}
BASELINE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")

WORK_PACKET = {
    "primary_family": "experiment_design",
    "primary_skill": "obsidian-experiment-design",
    "support_skills": "obsidian-performance-attribution;obsidian-result-judgment;obsidian-artifact-lineage",
    "required_gates": (
        "source_authority_audit;experiment_design_schema;performance_attribution_recorded;"
        "failure_memory_recorded;tier_duplicate_boundary_recorded;claim_guard"
    ),
}

PROFILE_DECISION_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_test_id",
    "state_profile",
    "followup_profile",
    "pressure_group",
    "net_profit",
    "profit_factor",
    "trade_count",
    "expectancy",
    "equity_drawdown_percent",
    "worst_month",
    "worst_month_net",
    "worst_slice_axis",
    "worst_slice_bucket",
    "worst_slice_net",
    "negative_month_count",
    "positive_month_ratio",
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
    output: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        output[str(row.get(key, ""))].append(row)
    return output


def candidate_sort_key(alias: str) -> int:
    try:
        return BASELINE_ORDER.index(alias)
    except ValueError:
        return len(BASELINE_ORDER)


def profile_label(row: Mapping[str, Any]) -> str:
    return f"{row.get('source_test_id')}::{row.get('state_profile')}::{row.get('followup_profile')}"


def source_hashes() -> dict[str, str]:
    paths = {
        "source_review_result": SOURCE_REVIEW_RESULT_PATH,
        "source_report": SOURCE_REPORT_PATH,
        "source_candidate_followup_review": SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH,
        "source_candidate_summary": SOURCE_CANDIDATE_SUMMARY_PATH,
        "source_followup_profile_summary": SOURCE_FOLLOWUP_PROFILE_SUMMARY_PATH,
        "source_negative_slice_summary": SOURCE_NEGATIVE_SLICE_PATH,
        "source_tier_duplicate_review": SOURCE_TIER_DUPLICATE_REVIEW_PATH,
    }
    return {name: sha256_file_lf_normalized(path) if path_exists(path) else "missing" for name, path in paths.items()}


def build_profile_decisions(profile_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for row in sorted(profile_rows, key=lambda item: as_float(item.get("net_profit")), reverse=True):
        alias = str(row.get("candidate_alias"))
        candidate_id, candidate_role, _ = BASELINE_CANDIDATES.get(
            alias,
            (str(row.get("candidate_id")), str(row.get("candidate_role")), str(row.get("candidate_role"))),
        )
        net = as_float(row.get("net_profit"))
        pf = as_float(row.get("profit_factor"))
        trades = as_int(row.get("trade_count"))
        dd = as_float(row.get("report_equity_drawdown_percent"))
        worst_month = str(row.get("worst_month"))
        worst_month_net = as_float(row.get("worst_month_net"))
        worst_slice_axis = str(row.get("worst_slice_axis"))
        worst_slice_bucket = str(row.get("worst_slice_bucket"))
        worst_slice_net = as_float(row.get("worst_slice_net"))
        deep_hole = worst_slice_net <= -220.0 or worst_month_net <= -180.0
        severe_hole = worst_slice_net <= -270.0 or worst_month_net <= -250.0
        trade_watch = trades < 285
        pf_watch = pf < 1.55

        if alias == "s264_aih":
            priority = "P0"
            decision = "core_challenger_pressure_gate(핵심 도전자 압박 게이트)"
            next_use = "keep as main challenger only if noncalendar pressure reduces 2024-12 and Monday holes(비달력 압박이 2024-12와 월요일 구멍을 줄일 때만 핵심 도전자로 유지)"
        elif alias == "s264_aia":
            priority = "P0"
            decision = "oos_anchor_adapter_watch_gate(표본외 앵커 어댑터 관찰 게이트)"
            next_use = "watch for Adapter only after drawdown edge survives weak-slice pressure(손실폭 이점이 약한 구간 압박을 버틴 뒤에만 어댑터 관찰)"
        elif alias == "s258_stc":
            priority = "P0" if net >= 1000.0 else "P1"
            decision = "stress_challenger_prune_or_rescue_gate(압박 도전자 가지치기 또는 회수 게이트)"
            next_use = "use only as stress challenger; prune if PF, trade count, or DD stays uncomfortable(압박 도전자로만 사용하고 수익 팩터, 거래 수, 손실폭이 불편하면 가지치기)"
        elif alias == "s264_lc":
            priority = "P1"
            decision = "defensive_control_audit_only(방어 기준 감사 전용)"
            next_use = "control audit against challenger variants, not Adapter selection(도전자 변형 비교 감사용이며 어댑터 선택 아님)"
        else:
            priority = "P1"
            decision = "validation_heavy_control_audit_only(검증 중심 기준 감사 전용)"
            next_use = "validation stability control, not Adapter selection(검증 안정성 기준이며 어댑터 선택 아님)"

        if severe_hole:
            stop_rule = "stop if next pressure keeps any major slice below -220 net(다음 압박 후 주요 구간이 -220 순손익 아래면 중단)"
        elif deep_hole:
            stop_rule = "stop or downgrade if next pressure does not reduce repeated holes(다음 압박이 반복 구멍을 줄이지 못하면 중단 또는 강등)"
        else:
            stop_rule = "continue only with broader period and fallback checks(더 넓은 기간과 대체 검증이 있을 때만 계속)"

        if trade_watch or pf_watch:
            stop_rule += "; enforce PF/trade-count floor(수익 팩터와 거래 수 하한 적용)"

        decisions.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": candidate_role,
                "source_test_id": row.get("source_test_id"),
                "state_profile": row.get("state_profile"),
                "followup_profile": row.get("followup_profile"),
                "pressure_group": row.get("pressure_group"),
                "net_profit": net,
                "profit_factor": pf,
                "trade_count": trades,
                "expectancy": as_float(row.get("expectancy")),
                "equity_drawdown_percent": dd,
                "worst_month": worst_month,
                "worst_month_net": worst_month_net,
                "worst_slice_axis": worst_slice_axis,
                "worst_slice_bucket": worst_slice_bucket,
                "worst_slice_net": worst_slice_net,
                "negative_month_count": as_int(row.get("negative_month_count")),
                "positive_month_ratio": as_float(row.get("positive_month_ratio")),
                "profile_decision": decision,
                "priority": priority,
                "next_use": next_use,
                "stop_rule": stop_rule,
                "reopen_condition": "reopen only with new state feature or true fallback evidence, not a literal calendar filter(달력 직접 필터가 아니라 새 상태 피처나 실제 대체 근거가 있을 때만 재개)",
                "do_not_claim": "no selected candidate, no ONNX readiness, no Goal Achieve(선택 후보 없음, ONNX 준비 없음, 목표 달성 없음)",
            }
        )
    return decisions


def build_candidate_decisions(profile_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_candidate = grouped(profile_decisions, "candidate_alias")
    rows: list[dict[str, Any]] = []
    for alias in BASELINE_ORDER:
        candidate_id, candidate_role, _ = BASELINE_CANDIDATES[alias]
        items = by_candidate.get(alias, [])
        if not items:
            rows.append(
                {
                    "candidate_alias": alias,
                    "candidate_id": candidate_id,
                    "candidate_role": candidate_role,
                    "profile_count": 0,
                    "decision_label": "missing_required(필수 누락)",
                    "priority": "blocked",
                    "next_use": "blocked until source profile rows exist(원천 프로필 행이 생길 때까지 차단)",
                    "prune_boundary": "do not prune from missing design alone(설계 누락만으로 가지치기 금지)",
                    "reopen_condition": "source review rebuilt(원천 검토 재생성)",
                    "do_not_claim": "no candidate selection(후보 선택 없음)",
                }
            )
            continue
        nets = [as_float(row.get("net_profit")) for row in items]
        pfs = [as_float(row.get("profit_factor")) for row in items]
        trades = [as_int(row.get("trade_count")) for row in items]
        dds = [as_float(row.get("equity_drawdown_percent")) for row in items]
        worst_months = [as_float(row.get("worst_month_net")) for row in items]
        worst_slices = [as_float(row.get("worst_slice_net")) for row in items]
        deep_hole_count = sum(1 for row in items if as_float(row.get("worst_slice_net")) <= -220.0 or as_float(row.get("worst_month_net")) <= -180.0)
        best_profile = max(items, key=lambda row: as_float(row.get("net_profit")))

        if alias == "s264_aih":
            label = "retain_core_challenger_but_not_selection(핵심 도전자는 유지하지만 선택 아님)"
            priority = "P0"
            next_use = "second pressure branch on volatility/range interaction(변동성/범위 상호작용 2차 압박 분기)"
            prune_boundary = "downgrade if 2024-12 or Monday hole remains deep after one more broad pressure(한 번 더 넓은 압박 후 2024-12 또는 월요일 구멍이 깊으면 강등)"
        elif alias == "s264_aia":
            label = "retain_oos_anchor_adapter_watch_gate_not_selection(표본외 앵커 어댑터 관찰 게이트, 선택 아님)"
            priority = "P0"
            next_use = "DD-resilience Adapter watch only after slice gate improves(구간 게이트 개선 뒤 손실폭 견고성 어댑터 관찰)"
            prune_boundary = "do not promote on DD edge while Monday hole remains(월요일 구멍이 남으면 손실폭 이점만으로 올리지 않음)"
        elif alias == "s258_stc":
            label = "stress_challenger_prune_or_rescue(압박 도전자 가지치기 또는 회수)"
            priority = "P0"
            next_use = "strict stress gate; remove from active challenger lane if PF/trade/DD fails(엄격 압박 게이트, 수익 팩터/거래 수/손실폭 실패 시 활성 도전자에서 제거)"
            prune_boundary = "max two-stage rescue branch from this point(이 지점부터 회수 분기는 최대 두 단계)"
        elif alias == "s264_lc":
            label = "defensive_control_retained_no_selection(방어 기준 유지, 선택 아님)"
            priority = "P1"
            next_use = "control audit for high headline with repeated weak slice(높은 대표 숫자와 반복 약점 구간 감사)"
            prune_boundary = "keep as comparator unless it stops differentiating candidates(후보 차이를 못 가르면 비교 기준에서 제거)"
        else:
            label = "validation_heavy_control_retained_no_selection(검증 중심 기준 유지, 선택 아님)"
            priority = "P1"
            next_use = "validation stability comparator under second pressure(2차 압박의 검증 안정성 비교 기준)"
            prune_boundary = "keep as comparator, not Adapter lane(비교 기준으로 유지, 어댑터 분기 아님)"

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
                "deep_hole_count": deep_hole_count,
                "best_profile": profile_label(best_profile),
                "decision_label": label,
                "priority": priority,
                "next_use": next_use,
                "prune_boundary": prune_boundary,
                "reopen_condition": "reopen only if broad noncalendar pressure improves weak slices without collapsing trades(넓은 비달력 압박이 거래 수 붕괴 없이 약한 구간을 개선할 때만 재개)",
                "do_not_claim": "no selected candidate, no ONNX readiness, no Goal Achieve(선택 후보 없음, ONNX 준비 없음, 목표 달성 없음)",
            }
        )
    return rows


def build_next_queue() -> list[dict[str, Any]]:
    common_boundary = "research development only; no selected candidate; no ONNX until goal gate(연구개발 전용, 선택 후보 없음, 목표 게이트 전 ONNX 없음)"
    return [
        {
            "queue_id": "run267AV_q01_core_challenger_second_pressure",
            "priority": "P0",
            "materialization_readiness": "ready_for_run267AW_design_materialization(run267AW 설계 물질화 준비)",
            "workstream": "noncalendar_state_feature_second_pressure(비달력 상태 피처 2차 압박)",
            "candidate_scope": "s264_aih",
            "profile_scope": "core_volatility_resilience_pressure_v2;core_range_resilience_pressure_v2",
            "source_evidence": rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH),
            "hypothesis": "s264_aih may be worth keeping only if volatility/range interaction reduces 2024-12 and Monday holes without losing trade count(s264_aih는 변동성/범위 상호작용이 2024-12와 월요일 구멍을 거래 수 손상 없이 줄일 때만 유지 가치가 있다)",
            "decision_use": "core challenger keep/downgrade decision(핵심 도전자 유지/강등 결정)",
            "comparison_baseline": "run267AU s264_aih two Tier A follow-up profiles(run267AU s264_aih Tier A 후속 프로필 2개)",
            "control_variables": "same 2024 historical Tier A test, same candidate score source, no calendar literal filter(같은 2024 과거 Tier A 시험, 같은 후보 점수 원천, 달력 직접 필터 없음)",
            "changed_variables": "state feature interaction and pressure weights only(상태 피처 상호작용과 압박 가중치만 변경)",
            "sample_scope": "2024 historical Tier A first, Tier A+B only after true fallback manifest exists(먼저 2024 과거 Tier A, 실제 대체 목록이 생긴 뒤 Tier A+B)",
            "success_criteria": "net remains above 1000, PF above 1.55, trades above 285, worst month and worst weekday both improve materially(순손익 1000 이상, 수익 팩터 1.55 이상, 거래 285 이상, 최악 월과 최악 요일 모두 실질 개선)",
            "failure_criteria": "any repeated deep slice below -220 or trade count collapse below 285(반복 깊은 구간 -220 이하 또는 거래 수 285 미만 붕괴)",
            "invalid_conditions": "Tier A+B duplicate used as routed fallback evidence or literal calendar repair sneaks in(Tier A+B 중복을 라우팅 대체 근거로 쓰거나 달력 직접 수리가 섞임)",
            "stop_conditions": "do not extend this repair beyond two stages without a new hypothesis(새 가설 없이 이 수리를 두 단계 넘게 끌지 않음)",
            "evidence_plan": "MT5 KPI, trade list, balance/equity curve, month/weekday/session/hour slices(MT5 핵심 성과 지표, 거래 목록, 잔액/평가금 곡선, 월/요일/세션/시간 구간)",
            "next_required_artifacts": "variant manifest, runtime contract, set files, MT5 reports, curve and slice review(변형 목록, 런타임 계약, 설정 파일, MT5 보고서, 곡선과 구간 검토)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AV_q02_oos_anchor_adapter_watch_gate",
            "priority": "P0",
            "materialization_readiness": "ready_for_run267AW_design_materialization(run267AW 설계 물질화 준비)",
            "workstream": "adapter_watch_gate_after_slice_pressure(구간 압박 뒤 어댑터 관찰 게이트)",
            "candidate_scope": "s264_aia",
            "profile_scope": "oos_anchor_dd_resilience_pressure_v2;oos_anchor_shock_resilience_pressure_v2",
            "source_evidence": rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH),
            "hypothesis": "s264_aia has the best DD shape among follow-ups, but it is not Adapter-worthy unless Monday and 2024-12 holes shrink(s264_aia는 후속 중 손실폭 모양이 가장 낫지만 월요일과 2024-12 구멍이 줄어야 어댑터 검토 가치가 있다)",
            "decision_use": "Adapter watch or hold decision(어댑터 관찰 또는 보류 결정)",
            "comparison_baseline": "run267AU s264_aia range and shock profiles(run267AU s264_aia 범위와 충격 프로필)",
            "control_variables": "same candidate, same score-table source, no retraining claim(같은 후보, 같은 점수표 원천, 재학습 주장 없음)",
            "changed_variables": "DD-resilience blend and shock/range pressure blend(손실폭 견고성 혼합과 충격/범위 압박 혼합)",
            "sample_scope": "2024 historical Tier A plus later true fallback route audit(2024 과거 Tier A와 이후 실제 대체 라우팅 감사)",
            "success_criteria": "DD stays below 15%, recovery remains above 4, trades stay near 290, worst weekday improves above -190(손실폭 15% 미만, 회복 4 초과, 거래 약 290 유지, 최악 요일 -190 위로 개선)",
            "failure_criteria": "DD edge survives but weak slices stay deep, or trade count shrinks enough to hide risk(손실폭 이점만 남고 약한 구간이 깊거나 거래 수가 줄어 위험을 가림)",
            "invalid_conditions": "Adapter contract written before feature order and route boundary are stable(피처 순서와 라우팅 경계 안정 전 어댑터 계약 작성)",
            "stop_conditions": "hold Adapter work if slice gate fails once more(구간 게이트가 한 번 더 실패하면 어댑터 작업 보류)",
            "evidence_plan": "candidate curve zoom, weak slice table, trade-quality table, feature order audit(후보 곡선 확대, 약한 구간 표, 거래 품질 표, 피처 순서 감사)",
            "next_required_artifacts": "materialization manifest and no-selection report(물질화 목록과 선택 없음 보고서)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AV_q03_control_stability_audit",
            "priority": "P1",
            "materialization_readiness": "ready_for_control_audit_materialization(기준 감사 물질화 준비)",
            "workstream": "defensive_and_validation_control_audit(방어/검증 기준 감사)",
            "candidate_scope": "s264_lc;s262_lih",
            "profile_scope": "defensive_control_volatility_audit_v1;validation_control_volatility_audit_v1",
            "source_evidence": rel(CANDIDATE_DECISION_PATH),
            "hypothesis": "controls are useful only if they reveal whether challenger gains are broad or fragile(기준 후보는 도전자 개선이 넓은지 취약한지 드러낼 때만 유용하다)",
            "decision_use": "control retention or retirement decision(기준 유지 또는 퇴역 결정)",
            "comparison_baseline": "run267AU control profiles and s264_aih/s264_aia pressure profiles(run267AU 기준 프로필과 s264_aih/s264_aia 압박 프로필)",
            "control_variables": "same MT5 period and scoring boundary(같은 MT5 기간과 점수 경계)",
            "changed_variables": "none except audit grouping(감사 묶음 외 변경 없음)",
            "sample_scope": "2024 historical Tier A diagnostic only(2024 과거 Tier A 진단 전용)",
            "success_criteria": "controls expose lower fragility or confirm challenger weakness(기준이 더 낮은 취약성을 보이거나 도전자 약점을 확인)",
            "failure_criteria": "controls merely mirror the same Monday/2024-12 holes with no extra information(기준이 월요일/2024-12 구멍만 그대로 반복하고 추가 정보가 없음)",
            "invalid_conditions": "control row treated as selected candidate(기준 행을 선택 후보로 취급)",
            "stop_conditions": "retire control audit lane if it cannot differentiate the next run(다음 실행에서 차이를 못 내면 기준 감사 분기 종료)",
            "evidence_plan": "side-by-side KPI, curve, slice, and failure-memory comparison(나란히 핵심 성과 지표, 곡선, 구간, 실패 기억 비교)",
            "next_required_artifacts": "control audit table and candidate decision update(기준 감사 표와 후보 결정 갱신)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AV_q04_stress_challenger_prune_or_rescue",
            "priority": "P0",
            "materialization_readiness": "ready_for_strict_prune_gate(엄격 가지치기 게이트 준비)",
            "workstream": "stress_challenger_prune_or_rescue(압박 도전자 가지치기 또는 회수)",
            "candidate_scope": "s258_stc",
            "profile_scope": "stress_challenger_trend_prune_pressure_v2;stress_challenger_volatility_prune_pressure_v2",
            "source_evidence": rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH),
            "hypothesis": "s258_stc is only useful if stress pressure keeps high net without DD, PF, or trade-count discomfort(s258_stc는 높은 순손익이 손실폭, 수익 팩터, 거래 수 불편 없이 유지될 때만 유용하다)",
            "decision_use": "active stress lane prune/rescue decision(활성 압박 분기 가지치기/회수 결정)",
            "comparison_baseline": "run267AU two s258_stc stress profiles(run267AU s258_stc 압박 프로필 2개)",
            "control_variables": "same historical 2024 period and no direct month/weekday filter(같은 2024 과거 기간과 월/요일 직접 필터 없음)",
            "changed_variables": "stress gate thresholds and noncalendar state pressure only(압박 게이트 임계값과 비달력 상태 압박만 변경)",
            "sample_scope": "2024 Tier A, then only if it passes wider period check(2024 Tier A, 통과할 때만 더 넓은 기간 확인)",
            "success_criteria": "trade count above 285, PF above 1.55, DD below 17%, worst weekday above -200(거래 수 285 초과, 수익 팩터 1.55 초과, 손실폭 17% 미만, 최악 요일 -200 위)",
            "failure_criteria": "trade count shrink, PF below 1.55, DD near 20%, or Monday hole below -220(거래 수 축소, 수익 팩터 1.55 미만, 손실폭 20% 근처, 월요일 구멍 -220 이하)",
            "invalid_conditions": "headline net used to rescue despite failed risk/trade gate(위험/거래 게이트 실패에도 대표 순손익으로 회수)",
            "stop_conditions": "if this gate fails, move to failure memory unless a new feature family appears(이 게이트 실패 시 새 피처군이 없으면 실패 기억으로 이동)",
            "evidence_plan": "risk/trade quality table, weak month/weekday table, curve zoom(위험/거래 품질 표, 약한 월/요일 표, 곡선 확대)",
            "next_required_artifacts": "prune decision receipt or rescue manifest(가지치기 결정 기록 또는 회수 목록)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AV_q05_true_fallback_route_gap",
            "priority": "P0",
            "materialization_readiness": "design_first_not_runtime_claim(먼저 설계, 런타임 주장 아님)",
            "workstream": "true_tier_b_fallback_route_audit(진짜 Tier B 대체 라우팅 감사)",
            "candidate_scope": "all_baseline_candidates(모든 기준 후보)",
            "profile_scope": "all run267AU follow-up profiles(run267AU 모든 후속 프로필)",
            "source_evidence": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "hypothesis": "Tier A+B rows remain duplicate evidence until fallback is actually used(Tier A+B 행은 대체가 실제 사용되기 전까지 중복 근거다)",
            "decision_use": "runtime reproduction readiness blocker(런타임 재현 준비 차단 조건)",
            "comparison_baseline": "run267AU tier duplicate review(run267AU 티어 중복 검토)",
            "control_variables": "same score tables and route code boundary(같은 점수표와 라우팅 코드 경계)",
            "changed_variables": "route manifest and fallback coverage audit only(라우팅 목록과 대체 커버리지 감사만 변경)",
            "sample_scope": "gap audit before any ONNX or runtime parity claim(ONNX 또는 런타임 동등성 주장 전 공백 감사)",
            "success_criteria": "fallback used count, component records, and actual routed total are separable(대체 사용 수, 구성 기록, 실제 라우팅 전체가 분리됨)",
            "failure_criteria": "Tier A+B remains a duplicate of Tier A(티어 A+B가 계속 Tier A 중복)",
            "invalid_conditions": "duplicate Tier A+B treated as combined result(중복 Tier A+B를 합산 결과로 취급)",
            "stop_conditions": "do not open ONNX lane until this route gap is resolved(이 라우팅 공백 해결 전 ONNX 분기 개방 금지)",
            "evidence_plan": "route manifest, fallback count audit, Tier A/Tier B/actual routed records(라우팅 목록, 대체 수 감사, Tier A/Tier B/실제 라우팅 기록)",
            "next_required_artifacts": "fallback manifest and route audit report(대체 목록과 라우팅 감사 보고서)",
            "claim_boundary": common_boundary,
        },
    ]


def build_failure_memory(profile_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    worst_month = min((as_float(row.get("worst_month_net")) for row in profile_decisions), default=0.0)
    worst_slice = min((as_float(row.get("worst_slice_net")) for row in profile_decisions), default=0.0)
    return [
        {
            "memory_id": "run267AV_mem01_headline_kpi_not_enough",
            "pattern": "headline KPI improves while weak slices remain deep(대표 핵심 성과 지표는 개선되지만 약한 구간은 깊게 남음)",
            "evidence": f"worst_month_net={worst_month:.2f};worst_slice_net={worst_slice:.2f};source={rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH)}",
            "affected_scope": "all baseline candidates(모든 기준 후보)",
            "do_not_repeat": "do not select a candidate from net/PF alone(순손익/수익 팩터만으로 후보 선택 금지)",
            "salvage_angle": "use slice reduction and curve shape as the next gate(구간 축소와 곡선 모양을 다음 게이트로 사용)",
            "reopen_condition": "weak slices improve without trade count collapse(거래 수 붕괴 없이 약한 구간이 개선)",
            "boundary": "no selection, no ONNX readiness(선택 없음, ONNX 준비 없음)",
        },
        {
            "memory_id": "run267AV_mem02_monday_cluster_repeat",
            "pattern": "Monday weak-slice cluster repeats(월요일 약한 구간 군집 반복)",
            "evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "affected_scope": "all candidates except the exact worst differs by profile(프로필별 최악은 다르지만 모든 후보에 영향)",
            "do_not_repeat": "do not add a literal weekday filter as the whole repair(요일 직접 필터 하나로 수리 금지)",
            "salvage_angle": "test noncalendar state features that explain the same behavior(같은 행동을 설명하는 비달력 상태 피처 시험)",
            "reopen_condition": "state feature reduces Monday loss and other slices do not worsen(상태 피처가 월요일 손실을 줄이고 다른 구간이 악화되지 않음)",
            "boundary": "diagnostic weakness memory(진단 약점 기억)",
        },
        {
            "memory_id": "run267AV_mem03_2024_12_cluster_repeat",
            "pattern": "2024-12 remains the main month hole(2024-12가 주요 월별 구멍으로 남음)",
            "evidence": rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH),
            "affected_scope": "s264_aih;s264_lc;s262_lih;s264_aia;s258_stc",
            "do_not_repeat": "do not overfit one month with a month literal rule(월 직접 규칙으로 한 달에 과적합 금지)",
            "salvage_angle": "map the month to range, shock, volatility, and trade-shape state(그 달을 범위, 충격, 변동성, 거래 모양 상태로 매핑)",
            "reopen_condition": "improves 2024-12 and preserves adjacent months(2024-12를 개선하고 인접 월을 보존)",
            "boundary": "repair clue, not success claim(수리 단서, 성공 주장 아님)",
        },
        {
            "memory_id": "run267AV_mem04_tier_ab_duplicate_boundary",
            "pattern": "Tier A+B rows are duplicate boundary, not true routed fallback evidence(Tier A+B 행은 진짜 라우팅 대체 근거가 아니라 중복 경계)",
            "evidence": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "affected_scope": "all run267AU follow-up profiles(run267AU 모든 후속 프로필)",
            "do_not_repeat": "do not call synthetic or duplicate rows combined survival(합성 또는 중복 행을 합산 생존성으로 부르지 않음)",
            "salvage_angle": "create a true fallback route manifest before runtime reproduction claims(런타임 재현 주장 전 실제 대체 라우팅 목록 생성)",
            "reopen_condition": "fallback used count and routed total are separable(대체 사용 수와 라우팅 전체가 분리됨)",
            "boundary": "runtime and ONNX blocker(런타임과 ONNX 차단 조건)",
        },
        {
            "memory_id": "run267AV_mem05_stress_challenger_fragility",
            "pattern": "s258_stc has stress headline but PF/trade/DD discomfort(s258_stc는 압박 대표 숫자는 있으나 수익 팩터/거래 수/손실폭 불편)",
            "evidence": rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH),
            "affected_scope": "s258_stc",
            "do_not_repeat": "do not rescue from net profit alone(순손익만으로 회수 금지)",
            "salvage_angle": "one strict prune-or-rescue gate with risk and trade quality(위험과 거래 품질을 포함한 엄격한 가지치기/회수 게이트 한 번)",
            "reopen_condition": "PF, trade count, DD, and weak slices pass together(수익 팩터, 거래 수, 손실폭, 약한 구간이 함께 통과)",
            "boundary": "stress lane only(압박 분기 전용)",
        },
    ]


def build_performance_attribution(candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in candidate_decisions:
        alias = str(row.get("candidate_alias"))
        rows.append(
            {
                "attribution_id": f"run267AV_attr_{alias}",
                "observed_change": (
                    f"{alias} keeps positive 2024 follow-up net but still has deep slice holes"
                    f"({alias}는 2024 후속 순손익은 양수로 유지하지만 깊은 구간 구멍이 남음)"
                ),
                "comparison_baseline": "run267B historical 2024 and run267AU follow-up review(run267B 2024 과거와 run267AU 후속 검토)",
                "likely_drivers": "state feature pressure improved broad headline numbers, but did not remove weak-slice concentration(상태 피처 압박은 대표 숫자를 넓게 개선했지만 약한 구간 집중을 제거하지 못함)",
                "segment_checks": "month, weekday, session, hour, chronological segment(月/요일/세션/시간/시간순서 구간)",
                "trade_shape": "trade count mostly 288-303 except weak stress variant 268; losses cluster in Monday and 2024-12(거래 수는 대체로 288-303이나 약한 압박 변형은 268, 손실은 월요일과 2024-12에 군집)",
                "alternative_explanations": "single-period 2024 fit, duplicate Tier A+B boundary, score-table extension artifact(단일 2024 기간 적합, Tier A+B 중복 경계, 점수표 확장 산물)",
                "attribution_confidence": "medium_for_2024_diagnostic_only(2024 진단 한정 중간)",
                "next_probe": NEXT_ACTION,
            }
        )
    return rows


def build_result_judgment(candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "result_subject": "overall_run267AV_design(전체 run267AV 설계)",
            "evidence_available": "run267AU review, candidate summary, negative slices, tier duplicate audit(run267AU 검토, 후보 요약, 음수 구간, 티어 중복 감사)",
            "evidence_missing": "new MT5 execution, true fallback routing, Adapter implementation, ONNX parity(새 MT5 실행, 실제 대체 라우팅, 어댑터 구현, ONNX 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": "design only; no selected candidate; no ONNX readiness(설계 전용, 선택 후보 없음, ONNX 준비 없음)",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이전 연구는 재료로 쓰였지만 아직 충분한 최종 검증은 아니다.",
        }
    ]
    for row in candidate_decisions:
        rows.append(
            {
                "result_subject": str(row.get("candidate_alias")),
                "evidence_available": (
                    f"profile_count={row.get('profile_count')};"
                    f"net_mean={row.get('net_profit_mean')};"
                    f"worst_slice={row.get('worst_slice_net_min')}"
                ),
                "evidence_missing": "broader period, ablation/replacement survival after this branch, true fallback route(더 넓은 기간, 이 분기 뒤 제거/대체 생존성, 실제 대체 라우팅)",
                "judgment_label": str(row.get("decision_label")),
                "claim_boundary": str(row.get("do_not_claim")),
                "next_condition": str(row.get("next_use")),
                "user_explanation_hook": "좋아 보이는 숫자보다 깨지는 구간을 먼저 본다.",
            }
        )
    return rows


def build_design_receipt(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    receipts = [
        {
            "receipt_id": "run267AV_receipt_source_authority",
            "receipt_type": "source_authority(원천 권위)",
            "status": "pass",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267AV uses reviewed run267AU evidence instead of fresh assumptions(run267AV는 새 추측이 아니라 검토된 run267AU 근거를 사용)",
            "notes": "parser_errors=0 in source review(원천 검토 파서 오류 0)",
        },
        {
            "receipt_id": "run267AV_receipt_prior_research_answer",
            "receipt_type": "prior_research_utilization(이전 연구 활용)",
            "status": "partial_but_improving",
            "evidence_path": "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_prior_research_utilization_audit.md",
            "effect": "Stage58 이전 연구가 버려진 것은 아니지만 R&D racing 검증 체계로는 더 펼쳐야 함을 유지한다(Stage58 이전 연구는 일부 활용됐지만 더 넓은 검증이 필요)",
            "notes": "run267V-W-X-Y-Z and run267AB-AU pulled more prior feature and weak-slice evidence into Stage267.",
        },
    ]
    receipts.extend(
        {
            "receipt_id": f"run267AV_receipt_{row['queue_id']}",
            "receipt_type": "experiment_design_queue(실험 설계 큐)",
            "status": "recorded",
            "evidence_path": str(row["source_evidence"]),
            "effect": str(row["decision_use"]),
            "notes": f"priority={row['priority']};candidate_scope={row['candidate_scope']}",
        }
        for row in queue_rows
    )
    return receipts


def build_gate_audit(
    profile_decisions: Sequence[Mapping[str, Any]],
    candidate_decisions: Sequence[Mapping[str, Any]],
    failure_memory: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_authority_audit",
            "status": "pass",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "source run267AU review exists and has no parser errors(원천 run267AU 검토가 있고 파서 오류가 없음)",
            "notes": "profile decisions built from candidate_followup_profile_review.csv",
        },
        {
            "gate_id": "experiment_design_schema",
            "status": "pass",
            "evidence_path": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "effect": "hypothesis, comparison, controls, success/failure/stop, evidence plan are recorded(가설, 비교, 고정 조건, 성공/실패/중단, 근거 계획 기록)",
            "notes": f"queue_rows={len(queue_rows)}",
        },
        {
            "gate_id": "candidate_role_boundary",
            "status": "pass",
            "evidence_path": rel(CANDIDATE_DECISION_PATH),
            "effect": "candidate roles are separated rather than ranked by one KPI(후보 역할을 단일 지표 순위가 아니라 분리)",
            "notes": f"candidate_decisions={len(candidate_decisions)};profile_decisions={len(profile_decisions)}",
        },
        {
            "gate_id": "failure_memory_recorded",
            "status": "pass",
            "evidence_path": rel(FAILURE_MEMORY_PATH),
            "effect": "repeated weak patterns are made reusable and non-repeatable(반복 약점을 재사용 가능하고 반복 금지 가능한 기록으로 만듦)",
            "notes": f"failure_memory={len(failure_memory)}",
        },
        {
            "gate_id": "tier_duplicate_boundary_recorded",
            "status": "pass",
            "evidence_path": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "effect": "Tier A+B duplicate rows are not treated as true fallback evidence(Tier A+B 중복 행을 실제 대체 근거로 취급하지 않음)",
            "notes": "true fallback route gap remains a P0 queue item",
        },
        {
            "gate_id": "claim_guard",
            "status": "pass",
            "evidence_path": rel(REVIEW_RESULT_PATH),
            "effect": "selected candidate, ONNX readiness, and Goal Achieve remain not claimed(선택 후보, ONNX 준비, 목표 달성 주장 없음)",
            "notes": "forbidden operating claims not used",
        },
    ]


def build_lineage(output_paths: Mapping[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "work_packet": WORK_PACKET,
        "source_artifacts": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "report": rel(SOURCE_REPORT_PATH),
            "candidate_followup_review": rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH),
            "candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "followup_profile_summary": rel(SOURCE_FOLLOWUP_PROFILE_SUMMARY_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "tier_duplicate_review": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "time_slice_kpi": rel(SOURCE_TIME_SLICE_PATH),
            "curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
        },
        "source_hashes": source_hashes(),
        "outputs": {name: rel(path) for name, path in output_paths.items()},
        "claim_boundary": "design only; no selected candidate; no ONNX readiness; no Goal Achieve",
    }


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = []
    replaced = False
    for line in text.splitlines():
        if not replaced and line.startswith(prefix):
            lines.append(replacement)
            replaced = True
        else:
            lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_any_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = [replacement if line.startswith(prefix) else line for line in text.splitlines()]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def update_workspace_state_text(text: str) -> str:
    focus = (
        "- >-\n"
        "  Stage267(267단계) run267AV(267AV 실행) pool-wide state feature engineering follow-up/Adapter branch design"
        "(후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계) "
        f"`{STATUS}`. Effect(효과): run267AU(267AU 실행)의 높은 대표 숫자와 깊은 2024-12/월요일 구멍을 "
        "다음 실험 큐(next experiment queue, 다음 실험 큐), 실패 기억(failure memory, 실패 기억), "
        "후보 역할 결정(candidate role decision, 후보 역할 결정)으로 바꿨고 selected candidate(선택 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "run267AV(267AV 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    text = replace_line_prefix(text, "current_run_id:", f"current_run_id: {RUN_ID}")

    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report_path = False
    for line in lines:
        stripped = line.strip()
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
        elif in_stage267 and line and not line.startswith(" ") and line.endswith(":"):
            in_stage267 = False

        if in_stage267:
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
                if not inserted_report_path:
                    output.append(f"  run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch_report_path: {rel(REPORT_PATH)}")
                    inserted_report_path = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    summary = (
        "Run267AV(267AV 실행)는 run267AU(267AU 실행)의 후속 검토를 설계 산출물로 바꿨다.\n"
        "Effect(효과): Stage58(58단계) 이전 연구는 일부 활용됐지만 아직 충분하다고 닫지 않고, "
        "후보군 전체를 2차 비달력 상태 압박(noncalendar state pressure, 비달력 상태 압박), "
        "어댑터 관찰 게이트(Adapter watch gate, 어댑터 관찰 게이트), 실제 Tier B 대체 라우팅(true fallback routing, 실제 대체 라우팅) "
        "공백으로 나눠 다음 실행에 넘긴다.\n"
        "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다."
    )
    report_line = (
        "- run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch(267AV 후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계): "
        f"`{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_design(최신 설계): run267AV(267AV 실행) profile decisions(프로필 결정) `{len(result['profile_decisions'])}`, "
        f"candidate decisions(후보 결정) `{len(result['candidate_decisions'])}`, queue rows(큐 행) `{len(result['next_experiment_queue'])}`, "
        f"failure memory(실패 기억) `{len(result['failure_memory'])}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_any_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_any_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
        text = replace_any_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_any_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_any_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{NEXT_ACTION}`")
        text = replace_any_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = replace_any_line_prefix(
            text,
            "- adapter_under_review(",
            "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_followup_or_adapter_branch`",
        )
        if report_line not in text:
            text = text.replace(
                "- run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                report_line + "\n- run267AU_pool_wide_state_feature_engineering_followup_balance_timeslice_trade_quality_review",
                1,
            )
        if latest_line not in text and "## Current Next Action" in text:
            text = text.replace("## Current Next Action", latest_line + "\n\n## Current Next Action", 1)
        text = append_once(text, "Run267AV(267AV 실행)는 run267AU", summary)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pool_wide_state_feature_engineering_followup_or_adapter_branch",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "scoreboard": "experiment_design_queue_from_run267AU_trade_shape_review",
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
                "notes": f"Run267AV design queue from run267AU review; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
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
        ("stage267_run267AV_design_script", "producer_script", PRODUCER_PATH, "Builds run267AV follow-up/Adapter branch design."),
        ("stage267_run267AV_profile_decision_matrix", "decision_matrix", PROFILE_DECISION_PATH, "Run267AV profile-level pressure decisions."),
        ("stage267_run267AV_candidate_decision_matrix", "decision_matrix", CANDIDATE_DECISION_PATH, "Run267AV candidate branch decisions."),
        ("stage267_run267AV_next_experiment_queue", "design_queue", NEXT_EXPERIMENT_QUEUE_PATH, "Run267AV next experiment queue."),
        ("stage267_run267AV_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267AV failure memory."),
        ("stage267_run267AV_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267AV performance attribution."),
        ("stage267_run267AV_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AV result judgment."),
        ("stage267_run267AV_design_receipt", "design_receipt", DESIGN_RECEIPT_PATH, "Run267AV experiment design receipt."),
        ("stage267_run267AV_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267AV gate audit."),
        ("stage267_run267AV_lineage", "artifact_lineage", LINEAGE_PATH, "Run267AV artifact lineage."),
        ("stage267_run267AV_review_result", "review_result", REVIEW_RESULT_PATH, "Run267AV JSON result."),
        ("stage267_run267AV_report", "review_report", REPORT_PATH, "User-facing run267AV design report."),
    )
    rows = [
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
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def fmt(value: Any) -> str:
    return f"{as_float(value):.2f}"


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = result["candidate_decisions"]
    profile_rows = result["profile_decisions"][:8]
    queue_rows = result["next_experiment_queue"]
    lines = [
        "# Stage267 Run267AV Pool-wide State Feature Engineering Follow-up/Adapter Branch Design(267단계 267AV 후보군 전체 상태 피처 엔지니어링 후속/어댑터 분기 설계)",
        "",
        "- action(행동): run267AU(267AU 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.",
        "- effect(효과): 대표 KPI(headline KPI, 대표 핵심 성과 지표)가 좋아 보여도 바로 고르지 않고, 2024-12(2024년 12월), Monday(월요일), Tier A+B duplicate boundary(Tier A+B 중복 경계)를 다음 검증 조건으로 고정한다.",
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
        "## Easy Read(쉬운 설명)",
        "",
        "Stage58(58단계)부터 이전 연구를 충분히 활용했느냐는 질문에는 아직 `아니오, 일부만 충분히 활용했다`가 맞다.",
        "Effect(효과): 이전 연구가 버려진 것은 아니지만, 지금 목표가 요구하는 후보군 전체 R&D racing(연구개발 경주), feature ablation(피처 제거), similar replacement(유사 피처 대체), balance/equity curve(잔액/평가금 곡선) 검증까지는 아직 더 펼쳐야 한다.",
        "",
        "다만 Stage267(267단계) 안에서는 보완이 진행됐다. run267V/W/X/Y/Z(267V/W/X/Y/Z 실행)는 실제 feature order(피처 순서) 기반 ablation(제거)을 다시 열었고, run267AB부터 run267AU(267AB-AU 실행)는 weak slice(약한 구간), noncalendar state feature(비달력 상태 피처), MT5(MetaTrader 5, 메타트레이더5) 거래 검토까지 이어졌다.",
        "Effect(효과): 이제 문제는 `이전 연구를 썼는가`가 아니라 `아직 깊은 구멍을 통과할 만큼 썼는가`이고, 답은 아직 아니다.",
        "",
        "run267AU(267AU 실행)의 핵심 판독은 단순하다. 모든 후보가 순손익과 PF(profit factor, 수익 팩터)는 좋아 보였지만, 모든 후보가 깊은 구간 구멍을 남겼다.",
        "Effect(효과): run267AV(267AV 실행)는 후보 선택이 아니라 다음 압박 설계다.",
        "",
        "## Candidate Decisions(후보 결정)",
        "",
        "| candidate(후보) | role(역할) | mean net(평균 순손익) | min net(최소 순손익) | worst slice(최악 구간) | holes(구멍) | decision(결정) | next use(다음 용도) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in candidate_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | {fmt(row.get('net_profit_mean'))} | "
            f"{fmt(row.get('net_profit_min'))} | {fmt(row.get('worst_slice_net_min'))} | "
            f"{as_int(row.get('deep_hole_count'))} | `{row.get('decision_label')}` | `{row.get('next_use')}` |"
        )
    lines.extend(
        [
            "",
            "## Top Profile Rows(상위 프로필 행)",
            "",
            "| candidate(후보) | profile(프로필) | net(순손익) | PF(수익 팩터) | trades(거래 수) | worst slice(최악 구간) | decision(결정) |",
            "| --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in profile_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('followup_profile')}` | {fmt(row.get('net_profit'))} | "
            f"{fmt(row.get('profit_factor'))} | {as_int(row.get('trade_count'))} | "
            f"`{row.get('worst_slice_axis')}`/`{row.get('worst_slice_bucket')}` {fmt(row.get('worst_slice_net'))} | "
            f"`{row.get('profile_decision')}` |"
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
            "## Result Boundary(결과 경계)",
            "",
            "- positive_claim(긍정 주장): `none(없음)`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            "- missing_required(필수 누락): second pressure MT5 execution(2차 압박 MT5 실행), true Tier B fallback route(진짜 Tier B 대체 라우팅), Adapter implementation(어댑터 구현), broader period survival(더 넓은 기간 생존성), ONNX parity(ONNX 동등성).",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_REVIEW_RESULT_PATH)}`, `{rel(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH)}`, `{rel(SOURCE_NEGATIVE_SLICE_PATH)}`, `{rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{NEXT_ACTION}`.",
            f"- artifact_paths(산출물 경로): `{rel(PROFILE_DECISION_PATH)}`, `{rel(CANDIDATE_DECISION_PATH)}`, `{rel(NEXT_EXPERIMENT_QUEUE_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_result() -> dict[str, Any]:
    source_payload = read_json(SOURCE_REVIEW_RESULT_PATH)
    profile_rows = read_csv(SOURCE_CANDIDATE_FOLLOWUP_REVIEW_PATH)
    profile_decisions = build_profile_decisions(profile_rows)
    candidate_decisions = build_candidate_decisions(profile_decisions)
    next_queue = build_next_queue()
    failure_memory = build_failure_memory(profile_decisions)
    performance_attribution = build_performance_attribution(candidate_decisions)
    result_judgment = build_result_judgment(candidate_decisions)
    design_receipt = build_design_receipt(next_queue)
    gate_audit = build_gate_audit(profile_decisions, candidate_decisions, failure_memory, next_queue)
    output_paths = {
        "profile_decision_matrix": PROFILE_DECISION_PATH,
        "candidate_branch_decision_matrix": CANDIDATE_DECISION_PATH,
        "next_experiment_queue": NEXT_EXPERIMENT_QUEUE_PATH,
        "failure_memory": FAILURE_MEMORY_PATH,
        "performance_attribution": PERFORMANCE_ATTRIBUTION_PATH,
        "result_judgment": RESULT_JUDGMENT_PATH,
        "experiment_design_receipt": DESIGN_RECEIPT_PATH,
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
            "source_candidate_followup_rows": len(source_payload.get("candidate_followup_review", [])),
            "source_negative_slice_count": len(source_payload.get("negative_slices", [])),
            "source_parser_errors": len(source_payload.get("parser_errors", [])),
        },
        "profile_decisions": profile_decisions,
        "candidate_decisions": candidate_decisions,
        "next_experiment_queue": next_queue,
        "failure_memory": failure_memory,
        "performance_attribution": performance_attribution,
        "result_judgment": result_judgment,
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
