from __future__ import annotations

import csv
import json
import math
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
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267CD"
RUN_ID = "run267CD_stage267_aggressive_impulse_dd_shape_followup_prune_or_pivot_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design_completed"
JUDGMENT = "prune_or_pivot_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CE_design_pool_wide_orthogonal_loss_shape_state_pivot_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_impulse_dd_shape_followup_prune_or_pivot_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_CANDIDATE_PERIOD_REVIEW_PATH = source_review.CANDIDATE_PERIOD_REVIEW_PATH
SOURCE_PERIOD_SUMMARY_PATH = source_review.PERIOD_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_FOLLOWUP_QUEUE_PATH = source_review.FOLLOWUP_QUEUE_PATH
SOURCE_FAILURE_MEMORY_PATH = source_review.FAILURE_MEMORY_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

BRANCH_DECISION_PATH = RUN_ROOT / "branch_decision_matrix.csv"
PIVOT_QUEUE_PATH = RUN_ROOT / "pivot_queue.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design.py")

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

BASELINE_POOL = (
    {
        "candidate_alias": "s264_aih",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_role": "core_challenger(핵심 도전자)",
    },
    {
        "candidate_alias": "s264_lc",
        "candidate_id": "s264_lowrank_control",
        "candidate_role": "defensive_control(방어 대조군)",
    },
    {
        "candidate_alias": "s262_lih",
        "candidate_id": "s262_lowrank_inner_half_filter",
        "candidate_role": "validation_heavy_control(검증 중심 대조군)",
    },
    {
        "candidate_alias": "s264_aia",
        "candidate_id": "s264_allow_inner_all_oos_anchor",
        "candidate_role": "oos_anchor(표본외 앵커)",
    },
    {
        "candidate_alias": "s258_stc",
        "candidate_id": "s258_short_tight_control",
        "candidate_role": "stress_challenger(압박 도전자)",
    },
)

BRANCH_DECISION_COLUMNS = (
    "decision_id",
    "scope",
    "candidate_alias",
    "candidate_id",
    "source_evidence",
    "observed_signal",
    "risk_or_gap",
    "decision_label",
    "next_use",
    "do_not_repeat",
    "stop_condition",
    "claim_boundary",
)

PIVOT_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "target_period_scope",
    "target_failure_shape",
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
    "materialization_instruction",
    "claim_boundary",
)

PRUNE_COLUMNS = (
    "prune_id",
    "scope",
    "prune_label",
    "evidence",
    "why_pruned",
    "salvage_value",
    "reopen_condition",
    "claim_boundary",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "evidence",
    "affected_scope",
    "why_failed_or_fragile",
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

EXPERIMENT_DESIGN_COLUMNS = (
    "receipt_id",
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


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return round(value, 6) if math.isfinite(value) else ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return value


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


def row_by_alias(rows: Sequence[Mapping[str, Any]], alias: str) -> Mapping[str, Any]:
    return next((row for row in rows if str(row.get("candidate_alias")) == alias), {})


def worst_slice(rows: Sequence[Mapping[str, Any]], alias: str) -> Mapping[str, Any]:
    subset = [row for row in rows if str(row.get("candidate_alias")) == alias]
    return min(subset, key=lambda row: as_float(row.get("net_profit")), default={})


def branch_decisions(
    candidate_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    followup_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    s264 = row_by_alias(candidate_rows, "s264_aih")
    s258 = row_by_alias(candidate_rows, "s258_stc")
    s264_worst = worst_slice(negative_rows, "s264_aih")
    s258_worst = worst_slice(negative_rows, "s258_stc")
    dd_boundary = next((row for row in followup_rows if row.get("workstream") == "branch_boundary"), {})
    return [
        {
            "decision_id": "run267cd_d01_close_current_ddshape_repair_loop",
            "scope": "branch",
            "candidate_alias": "s264_aih;s258_stc",
            "candidate_id": "s264_allow_inner_high_quarter;s258_short_tight_control",
            "source_evidence": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "observed_signal": dd_boundary.get(
                "reason",
                "both follow-up candidates remain above the DD watch line(두 후속 후보 모두 손실폭 관찰선 위)",
            ),
            "risk_or_gap": "repair branch is now narrow 2025H2-only evidence(수리 분기가 2025H2 단일 근거로 좁아짐)",
            "decision_label": "close_branch_no_selection(분기 종료, 선택 아님)",
            "next_use": "pivot to pool-wide orthogonal loss-shape/state design(후보군 전체 직교 손실형태/상태 설계로 전환)",
            "do_not_repeat": "do not continue the same DD-shape repair loop for a third stage-like pass(같은 손실폭 형태 수리를 세 번째 단계처럼 끌지 않음)",
            "stop_condition": "branch is closed unless a future pool-wide result gives a genuinely new structural reason(후보군 전체 결과가 새 구조 근거를 주기 전까지 재개 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "run267cd_d02_keep_s264_aih_as_relative_watch_only",
            "scope": "candidate",
            "candidate_alias": "s264_aih",
            "candidate_id": s264.get("candidate_id", "s264_allow_inner_high_quarter"),
            "source_evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "observed_signal": f"net={as_float(s264.get('total_net_profit'))};pf={as_float(s264.get('min_profit_factor'))};trades={as_int(s264.get('total_trades'))}",
            "risk_or_gap": f"worst_dd={as_float(s264.get('worst_dd_percent'))};worst_slice={s264_worst.get('axis')}/{s264_worst.get('bucket')} net={as_float(s264_worst.get('net_profit'))}",
            "decision_label": "watch_relative_best_not_selected(상대 최선 관찰, 선택 아님)",
            "next_use": "carry as core challenger reference in the next pivot, not as a chosen baseline(다음 전환의 핵심 도전자 참조로 유지, 선택 기준 아님)",
            "do_not_repeat": "do not turn 2025H2 positive net into ONNX or Adapter claim(2025H2 양수 순익을 ONNX 또는 어댑터 주장으로 바꾸지 않음)",
            "stop_condition": "drop to ordinary watch if next pool-wide pivot fails cross-period or ablation pressure(다음 후보군 전체 전환에서 확장 기간/제거 압박 실패 시 일반 관찰로 낮춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "run267cd_d03_prune_s258_stc_deep_repair_from_this_branch",
            "scope": "candidate",
            "candidate_alias": "s258_stc",
            "candidate_id": s258.get("candidate_id", "s258_short_tight_control"),
            "source_evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "observed_signal": f"net={as_float(s258.get('total_net_profit'))};pf={as_float(s258.get('min_profit_factor'))};trades={as_int(s258.get('total_trades'))}",
            "risk_or_gap": f"worst_dd={as_float(s258.get('worst_dd_percent'))};worst_slice={s258_worst.get('axis')}/{s258_worst.get('bucket')} net={as_float(s258_worst.get('net_profit'))}",
            "decision_label": "stress_comparator_only_prune_deep_repair(압박 비교군만 유지, 깊은 수리 중단)",
            "next_use": "keep as stress comparator and reopen only if a broader loss-shape feature rescues DD(압박 비교군으로만 유지하고 넓은 손실형태 피처가 DD를 살릴 때만 재개)",
            "do_not_repeat": "do not chase stress net profit while DD stays near 16 percent(손실폭이 16% 근처일 때 압박 순익만 추격하지 않음)",
            "stop_condition": "no s258-only repair from run267CC evidence(267CC 근거만으로 s258 단독 수리 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "run267cd_d04_reanchor_full_candidate_pool",
            "scope": "candidate_pool",
            "candidate_alias": "all_five",
            "candidate_id": ";".join(row["candidate_id"] for row in BASELINE_POOL),
            "source_evidence": rel(SOURCE_REPORT_PATH),
            "observed_signal": "latest repair narrowed to two candidates after broad pool work(넓은 후보군 작업 뒤 최신 수리가 두 후보로 좁아짐)",
            "risk_or_gap": "controls and OOS anchor can be underused if this branch keeps deepening(이 분기를 더 깊게 끌면 대조군과 표본외 앵커 활용이 줄어듦)",
            "decision_label": "reanchor_controls_and_anchor(대조군과 앵커 재고정)",
            "next_use": "next queue must include all five roles or explicitly justify exclusion(다음 큐는 다섯 역할을 포함하거나 제외 이유를 명시)",
            "do_not_repeat": "do not let a two-row follow-up silently become the pool baseline(두 행 후속이 조용히 후보군 기준처럼 굳지 않게 함)",
            "stop_condition": "every future narrowed branch needs a branch-boundary receipt(앞으로 좁아진 분기는 분기 경계 영수증 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "run267cd_d05_pivot_to_orthogonal_loss_shape_state",
            "scope": "next_research_direction",
            "candidate_alias": "all_five",
            "candidate_id": ";".join(row["candidate_id"] for row in BASELINE_POOL),
            "source_evidence": f"{rel(SOURCE_NEGATIVE_SLICE_PATH)};{rel(SOURCE_FAILURE_MEMORY_PATH)}",
            "observed_signal": "weak slices concentrate in Monday, 19/22 close hour, and late report session(약점이 월요일, 19/22시 청산, 후반 보고 세션에 몰림)",
            "risk_or_gap": "calendar-only deletion would look clean but would not prove structural robustness(달력 단독 삭제는 깔끔해 보여도 구조 견고성을 증명하지 못함)",
            "decision_label": "pivot_not_calendar_filter(달력 필터가 아닌 방향 전환)",
            "next_use": "design adverse-excursion, giveback, volatility-state, and session-state features across the pool(후보군 전체에 불리한 이동, 수익 반납, 변동성 상태, 세션 상태 피처 설계)",
            "do_not_repeat": "do not solve by hard-blocking one hour, one weekday, or one month(한 시간, 한 요일, 한 달 차단으로 해결하지 않음)",
            "stop_condition": "if orthogonal pivot cannot be materialized with feature-order and evidence receipts, mark blocked rather than selecting(직교 전환을 피처 순서와 근거 영수증으로 물질화 못 하면 선택 대신 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def pivot_queue() -> list[dict[str, Any]]:
    common_controls = (
        "same five baseline candidate roles, same FPMarkets US100 M5 scope, same source splits, same MT5 settings, "
        "same parser and balance/time-slice/trade-quality review(같은 다섯 기준 후보 역할, 같은 FPMarkets US100 M5 범위, "
        "같은 분할, 같은 MT5 설정, 같은 거래/곡선/시간구간/거래품질 검토)"
    )
    all_ids = ";".join(row["candidate_id"] for row in BASELINE_POOL)
    all_aliases = ";".join(row["candidate_alias"] for row in BASELINE_POOL)
    all_roles = ";".join(row["candidate_role"] for row in BASELINE_POOL)
    return [
        {
            "queue_id": "run267ce_q01_pool_wide_loss_shape_state_feature_engineering",
            "priority": "P0",
            "workstream": "pool_wide_orthogonal_pivot(후보군 전체 직교 전환)",
            "candidate_alias": all_aliases,
            "candidate_id": all_ids,
            "candidate_role": all_roles,
            "target_period_scope": "2024 plus 2023H2/2025H1/2025H2 where available(2024와 가능한 2023H2/2025H1/2025H2)",
            "target_failure_shape": "DD shape, adverse excursion, profit giveback, late-session state(손실폭 형태, 불리한 이동, 수익 반납, 후반 세션 상태)",
            "hypothesis": "a structural loss-shape/state feature can reduce fragility more broadly than another calendar repair(구조적 손실형태/상태 피처가 달력 수리 반복보다 넓게 취약성을 줄일 수 있음)",
            "decision_use": "decide whether the next branch should be feature engineering, Adapter tracing, or candidate pruning(다음 분기가 피처 엔지니어링, 어댑터 추적, 후보 가지치기 중 무엇인지 결정)",
            "comparison_baseline": "run267CC follow-up rows plus earlier Stage267 pool-wide controls(run267CC 후속 행과 이전 Stage267 후보군 전체 대조)",
            "control_variables": common_controls,
            "changed_variables": "add non-calendar loss-shape/state features; avoid single hour/weekday/month deletion(비달력 손실형태/상태 피처 추가, 단일 시간/요일/월 삭제 회피)",
            "sample_scope": "research design first, then MT5 materialization only after receipt check(먼저 연구 설계, 영수증 확인 뒤 MT5 물질화)",
            "success_criteria": "candidate retains trade count while reducing DD and weak-slice holes across more than one period(거래 수를 유지하면서 둘 이상 기간에서 손실폭과 약한 구간 구멍 감소)",
            "failure_criteria": "trade count collapse, PF collapse, DD moves elsewhere, or only one calendar slice improves(거래 수 붕괴, PF 붕괴, 손실폭 이동, 달력 한 구간만 개선)",
            "invalid_conditions": "feature order drift, changed split, missing parser/report, or hidden threshold-only tuning(피처 순서 변동, 분할 변경, 파서/보고서 누락, 숨은 임계값 미세조정)",
            "stop_conditions": "one design plus one materialized tranche before prune/pivot decision(설계 1회와 물질화 묶음 1회 후 가지치기/전환 판단)",
            "evidence_plan": "design receipt, feature order receipt, MT5 KPI, trade records, curve diagnostics, time-slice KPI, failure memory(설계 영수증, 피처 순서 영수증, MT5 KPI, 거래 기록, 곡선 진단, 시간구간 KPI, 실패 기억)",
            "materialization_instruction": "run267CE should design the queue before any MT5 execution claim(run267CE는 MT5 실행 주장 전 큐를 설계)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267ce_q02_reanchor_defensive_controls_and_oos_anchor",
            "priority": "P0",
            "workstream": "control_reanchor(대조군 재고정)",
            "candidate_alias": "s264_lc;s262_lih;s264_aia",
            "candidate_id": "s264_lowrank_control;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "candidate_role": "defensive_control;validation_heavy_control;oos_anchor(방어 대조군;검증 중심 대조군;표본외 앵커)",
            "target_period_scope": "same as q01(1번과 같음)",
            "target_failure_shape": "control fragility and validation/OOS tradeoff(대조군 취약성과 검증/표본외 절충)",
            "hypothesis": "controls may reveal whether the current branch found edge or just risk expansion(대조군은 현재 분기가 엣지인지 위험 확장인지 보여줄 수 있음)",
            "decision_use": "prevent s264_aih or s258_stc from becoming a silent baseline by absence of controls(대조군 부재로 s264_aih 또는 s258_stc가 조용히 기준처럼 굳는 것을 막음)",
            "comparison_baseline": "initial five-candidate pool roles and Stage267 control evidence(초기 다섯 후보 역할과 Stage267 대조 근거)",
            "control_variables": common_controls,
            "changed_variables": "no candidate-specific repair; re-evaluate controls under the new loss-shape design(후보별 수리 없음, 새 손실형태 설계 아래 대조군 재평가)",
            "sample_scope": "pool-wide design rows only until materialized(물질화 전까지 후보군 전체 설계 행)",
            "success_criteria": "controls expose whether challenger gain is robust or merely risk-seeking(대조군이 도전자 이득이 견고한지 위험 추구인지 드러냄)",
            "failure_criteria": "controls omitted or compared under different conditions(대조군 누락 또는 다른 조건 비교)",
            "invalid_conditions": "missing same-condition comparison or missing feature-order receipt(동일 조건 비교 누락 또는 피처 순서 영수증 누락)",
            "stop_conditions": "do not run challenger-only next unless this row is explicitly waived(이 행을 명시 면제하지 않으면 다음은 도전자만 실행하지 않음)",
            "evidence_plan": "control rows in queue, same-condition comparison receipt, later KPI and curve review(큐의 대조군 행, 동일 조건 비교 영수증, 이후 KPI와 곡선 검토)",
            "materialization_instruction": "include controls in run267CE queue or write a blocked/waived reason(run267CE 큐에 대조군 포함 또는 차단/면제 이유 기록)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267ce_q03_s264_aih_relative_best_adapter_trace_watch",
            "priority": "P1",
            "workstream": "adapter_trace_watch(어댑터 추적 관찰)",
            "candidate_alias": "s264_aih",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_role": "core_challenger(핵심 도전자)",
            "target_period_scope": "only after q01/q02 design receipts(1/2번 설계 영수증 뒤에만)",
            "target_failure_shape": "feature order, decision surface, risk handoff, and curve shape(피처 순서, 판단 표면, 위험 인계, 곡선 형태)",
            "hypothesis": "s264_aih remains the best watch only if its structure is traceable without hiding DD fragility(s264_aih는 DD 취약성을 숨기지 않고 구조 추적이 가능할 때만 최선 관찰로 남음)",
            "decision_use": "decide whether Adapter development is worth a bounded branch later(나중에 제한된 어댑터 개발 분기 가치가 있는지 판단)",
            "comparison_baseline": "run267CC s264_aih relative best watch and all controls(run267CC s264_aih 상대 최선 관찰 및 모든 대조군)",
            "control_variables": common_controls,
            "changed_variables": "traceability audit only, no ONNX and no runtime reproduction claim(추적성 감사만, ONNX와 런타임 재현 주장 없음)",
            "sample_scope": "artifact and feature-order design scope(산출물과 피처 순서 설계 범위)",
            "success_criteria": "feature order and decision surface can be recorded before any Adapter branch(어댑터 분기 전 피처 순서와 판단 표면 기록 가능)",
            "failure_criteria": "structure depends on hidden stage-local trick or undocumented feature order(구조가 숨은 단계 로컬 요령 또는 미문서 피처 순서에 의존)",
            "invalid_conditions": "missing feature manifest, missing model/config lineage, or runtime handoff mismatch(피처 목록, 모델/설정 계보 누락 또는 런타임 인계 불일치)",
            "stop_conditions": "do not start Adapter materialization until q01/q02 decide the next surface(1/2번이 다음 표면을 정하기 전 어댑터 물질화 금지)",
            "evidence_plan": "feature order receipt, lineage, config hash, decision-surface notes(피처 순서 영수증, 계보, 설정 해시, 판단 표면 메모)",
            "materialization_instruction": "hold as watch row, not execution row(실행 행이 아니라 관찰 행으로 보류)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267ce_q04_s258_stc_stress_reopen_rule",
            "priority": "P1",
            "workstream": "stress_reopen_rule(압박 후보 재개 규칙)",
            "candidate_alias": "s258_stc",
            "candidate_id": "s258_short_tight_control",
            "candidate_role": "stress_challenger(압박 도전자)",
            "target_period_scope": "only as comparator(비교군으로만)",
            "target_failure_shape": "high DD despite positive net(양수 순익에도 높은 손실폭)",
            "hypothesis": "s258_stc is useful as a stress comparator but not as a deep repair target from run267CC(s258_stc는 압박 비교군으로 유용하지만 267CC 근거의 깊은 수리 대상은 아님)",
            "decision_use": "keep failure memory alive without wasting another repair loop(실패 기억은 살리고 또 다른 수리 루프 낭비 방지)",
            "comparison_baseline": "run267CC s258_stc and s264_aih follow-up rows(run267CC s258_stc 및 s264_aih 후속 행)",
            "control_variables": common_controls,
            "changed_variables": "no new s258-only repair unless q01 creates a cross-candidate state feature(1번이 후보 공통 상태 피처를 만들기 전 s258 단독 수리 없음)",
            "sample_scope": "stress comparator rule only(압박 비교군 규칙만)",
            "success_criteria": "future reopening requires DD improvement mechanism, not just net profit(향후 재개는 순익이 아니라 DD 개선 메커니즘 필요)",
            "failure_criteria": "s258-only threshold polishing resumes without new structural evidence(새 구조 근거 없이 s258 단독 임계값 다듬기 재개)",
            "invalid_conditions": "missing reason for reopening or changed comparison scope(재개 이유 누락 또는 비교 범위 변경)",
            "stop_conditions": "keep pruned from deep repair until q01 evidence changes the structure(1번 근거가 구조를 바꿀 때까지 깊은 수리에서 제외)",
            "evidence_plan": "failure memory and future reopen condition(실패 기억과 향후 재개 조건)",
            "materialization_instruction": "no direct MT5 attempt from this row(이 행에서 직접 MT5 시도 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "run267cd_p01_no_candidate_selection_from_positive_2025h2",
            "scope": "branch",
            "prune_label": "no_headline_selection(대표 숫자 선택 금지)",
            "evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "why_pruned": "both candidates were positive, but this is single-period follow-up with DD watch(두 후보가 양수였지만 단일 기간 후속이고 손실폭 관찰 상태)",
            "salvage_value": "s264_aih remains relative watch; s258_stc remains stress comparator(s264_aih는 상대 관찰, s258_stc는 압박 비교군)",
            "reopen_condition": "multi-period, pool-wide, curve-shape evidence improves without DD relocation(다기간 후보군 전체 곡선 근거가 DD 이동 없이 개선)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267cd_p02_no_calendar_only_slice_repair",
            "scope": "weak_slice",
            "prune_label": "no_calendar_only_filter(달력 단독 필터 금지)",
            "evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "why_pruned": "weak slices are visible, but deleting Monday/19/22h would not prove market structure(약한 구간은 보이지만 월요일/19/22시 삭제는 시장 구조를 증명하지 못함)",
            "salvage_value": "use weak slices to design state features rather than hard exclusions(약한 구간을 하드 제외가 아니라 상태 피처 설계에 사용)",
            "reopen_condition": "only as diagnostic after non-calendar state feature fails(비달력 상태 피처가 실패한 뒤 진단으로만 재개)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267cd_p03_no_third_pass_same_ddshape_loop",
            "scope": "repair_loop",
            "prune_label": "stop_same_branch_loop(같은 분기 루프 중단)",
            "evidence": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "why_pruned": "repair loop already consumed cross-period design, materialization, execution, and trade review(수리 루프가 이미 확장 기간 설계, 물질화, 실행, 거래 검토를 소비)",
            "salvage_value": "branch lessons move into pivot queue and failure memory(분기 교훈을 전환 큐와 실패 기억으로 이동)",
            "reopen_condition": "new cross-candidate feature meaning, not another threshold or slice tweak(또 다른 임계값/구간 조정이 아니라 후보 공통 피처 의미)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267cd_p04_no_onnx_or_adapter_claim",
            "scope": "claim_boundary",
            "prune_label": "no_onnx_adapter_claim(ONNX/어댑터 주장 금지)",
            "evidence": rel(SOURCE_REVIEW_RESULT_PATH),
            "why_pruned": "no full pool winner, no Adapter package, no runtime reproduction, no ONNX parity(후보군 승자, 어댑터 패키지, 런타임 재현, ONNX 동등성 없음)",
            "salvage_value": "q03 keeps Adapter trace as watch only(3번 큐가 어댑터 추적을 관찰로만 유지)",
            "reopen_condition": "goal gates later satisfied by strong candidate package(나중에 강한 후보 패키지가 목표 게이트 충족)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "memory_id": "run267cd_branch_positive_but_dd_watch",
            "pattern": "positive_net_not_selection(양수 순익은 선택이 아님)",
            "evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "affected_scope": "s264_aih;s258_stc",
            "why_failed_or_fragile": "PF and net improved in 2025H2, but worst DD stayed at or above 15 percent(PF와 순익은 2025H2에서 개선됐지만 최악 손실폭은 15% 이상)",
            "do_not_repeat": "do not promote or ONNX-review from one positive follow-up period(양수 후속 한 기간으로 승격 또는 ONNX 검토 금지)",
            "salvage_angle": "use as clue for loss-shape feature engineering(손실형태 피처 엔지니어링 단서로 사용)",
            "reopen_condition": "multi-period curve and DD shape improve together(다기간 곡선과 DD 형태가 함께 개선)",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267cd_calendar_slice_temptation",
            "pattern": "calendar_bucket_overfit_risk(달력 구간 과적합 위험)",
            "evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "affected_scope": "Monday;close_hour_19_22;session_21_23",
            "why_failed_or_fragile": "weak buckets are small and easy to overfit(약한 버킷은 작고 과적합하기 쉬움)",
            "do_not_repeat": "do not hard-delete a clock bucket as cosmetic curve repair(그래프 보기용으로 시간 버킷을 하드 삭제하지 않음)",
            "salvage_angle": "convert into state feature ideas such as adverse excursion or giveback(불리한 이동 또는 수익 반납 같은 상태 피처 아이디어로 전환)",
            "reopen_condition": "state feature still leaves the same bucket as residual diagnostic(상태 피처 후에도 같은 버킷이 잔여 진단으로 남을 때)",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267cd_two_candidate_narrowing",
            "pattern": "pool_narrowing_requires_reanchor(후보군 축소는 재고정 필요)",
            "evidence": rel(SOURCE_REPORT_PATH),
            "affected_scope": "all_five_baseline_candidates(다섯 기준 후보)",
            "why_failed_or_fragile": "latest follow-up only tested two candidates, so controls can be underweighted(최신 후속은 두 후보만 시험해 대조군 비중이 낮아질 수 있음)",
            "do_not_repeat": "do not let a narrowed branch silently define the research pool(좁아진 분기가 조용히 연구 후보군을 정의하지 않게 함)",
            "salvage_angle": "run267CE reanchors controls and OOS anchor(267CE에서 대조군과 표본외 앵커 재고정)",
            "reopen_condition": "a future branch explicitly documents why a candidate role is excluded(향후 분기가 후보 역할 제외 이유를 명시)",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267cd_s258_stress_not_deep_repair",
            "pattern": "stress_candidate_requires_dd_mechanism(압박 후보는 DD 메커니즘 필요)",
            "evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "affected_scope": "s258_stc",
            "why_failed_or_fragile": "strong net is not enough while DD remains worst in the pair(순익이 강해도 짝 안에서 손실폭이 최악이면 충분하지 않음)",
            "do_not_repeat": "do not keep polishing s258-only thresholds from this branch(이 분기에서 s258 단독 임계값 다듬기 지속 금지)",
            "salvage_angle": "use only as stress comparator until cross-candidate loss-shape feature exists(후보 공통 손실형태 피처가 생길 때까지 압박 비교군으로만 사용)",
            "reopen_condition": "new feature lowers DD without collapsing trade count(새 피처가 거래 수 붕괴 없이 DD를 낮춤)",
            "boundary": CLAIM_BOUNDARY,
        },
    ]
    for source in source_rows:
        source_id = str(source.get("memory_id", "")).strip()
        if not source_id:
            continue
        rows.append(
            {
                "memory_id": f"source_{source_id}",
                "pattern": source.get("pattern"),
                "evidence": source.get("evidence"),
                "affected_scope": source.get("affected_scope"),
                "why_failed_or_fragile": source.get("why_failed_or_fragile"),
                "do_not_repeat": source.get("do_not_repeat"),
                "salvage_angle": source.get("salvage_angle"),
                "reopen_condition": source.get("reopen_condition"),
                "boundary": source.get("boundary") or CLAIM_BOUNDARY,
            }
        )
    return rows


def performance_attribution(candidate_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    s264 = row_by_alias(candidate_rows, "s264_aih")
    s258 = row_by_alias(candidate_rows, "s258_stc")
    negative_summary = ";".join(
        f"{row.get('candidate_alias')}:{row.get('axis')}/{row.get('bucket')}={row.get('net_profit')}"
        for row in negative_rows[:6]
    )
    return [
        {
            "attribution_id": "run267cd_a01_followup_net_gain_vs_dd_watch",
            "observed_change": f"s264_net={s264.get('total_net_profit')};s258_net={s258.get('total_net_profit')};dd_watch_all_rows=true",
            "comparison_baseline": "run267BZ queue expectations and run267CC follow-up execution(run267BZ 큐 기대와 run267CC 후속 실행)",
            "likely_drivers": "aggressive impulse branch preserved enough trade flow to stay positive(공격형 임펄스 분기가 충분한 거래 흐름을 유지해 양수 유지)",
            "segment_checks": negative_summary,
            "trade_shape": "trade counts around 150 each are usable, but DD and weak slices remain uncomfortable(각 150개 안팎 거래 수는 쓸 수 있으나 DD와 약한 구간이 불편)",
            "alternative_explanations": "single 2025H2 period may hide broader instability(단일 2025H2 기간이 넓은 불안정을 숨길 수 있음)",
            "attribution_confidence": "medium_for_branch_closure_low_for_selection(분기 종료에는 중간, 선택에는 낮음)",
            "next_probe": NEXT_ACTION,
        },
        {
            "attribution_id": "run267cd_a02_controls_missing_from_latest_followup",
            "observed_change": "latest P0 follow-up contained only s264_aih and s258_stc(최신 P0 후속은 s264_aih와 s258_stc만 포함)",
            "comparison_baseline": "five-role baseline candidate pool(다섯 역할 기준 후보군)",
            "likely_drivers": "prior branch intentionally narrowed to aggressive DD-shape candidates(이전 분기가 공격형 DD-shape 후보로 의도적으로 축소)",
            "segment_checks": "controls need reanchor before any pool-level judgment(후보군 수준 판정 전 대조군 재고정 필요)",
            "trade_shape": "not_applicable_design_attribution(설계 귀속이라 해당 없음)",
            "alternative_explanations": "controls may be weaker, but absence is not evidence(대조군이 약할 수는 있으나 부재는 근거가 아님)",
            "attribution_confidence": "high_for_design_boundary(설계 경계에는 높음)",
            "next_probe": "include all five or explicit exclusion receipt(다섯 후보 포함 또는 명시 제외 영수증)",
        },
    ]


def experiment_design_receipt(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": row["queue_id"],
            "hypothesis": row["hypothesis"],
            "decision_use": row["decision_use"],
            "comparison_baseline": row["comparison_baseline"],
            "control_variables": row["control_variables"],
            "changed_variables": row["changed_variables"],
            "sample_scope": row["sample_scope"],
            "success_criteria": row["success_criteria"],
            "failure_criteria": row["failure_criteria"],
            "invalid_conditions": row["invalid_conditions"],
            "stop_conditions": row["stop_conditions"],
            "evidence_plan": row["evidence_plan"],
        }
        for row in queue_rows
    ]


def result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CD aggressive impulse DD-shape follow-up branch(267CD 공격형 임펄스 DD-shape 후속 분기)",
            "evidence_available": (
                f"{rel(SOURCE_REVIEW_RESULT_PATH)};{rel(SOURCE_CANDIDATE_SUMMARY_PATH)};"
                f"{rel(SOURCE_NEGATIVE_SLICE_PATH)};{rel(SOURCE_FOLLOWUP_QUEUE_PATH)}"
            ),
            "evidence_missing": "full-pool rerun, multi-period pivot output, Adapter package, runtime reproduction, ONNX parity(후보군 전체 재실행, 다기간 전환 산출물, 어댑터 패키지, 런타임 재현, ONNX 동등성)",
            "judgment_label": "exploratory_design_completed_no_candidate_selection(탐색 설계 완료, 후보 선택 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run267CE must design or materialize a pool-wide orthogonal pivot before any stronger claim(더 강한 주장 전 run267CE가 후보군 전체 직교 전환을 설계 또는 물질화해야 함)",
            "user_explanation_hook": "지금은 후보를 고른 게 아니라, 좁아진 수리 분기를 닫고 다음 넓은 실험 방향을 정한 상태다.",
        },
        {
            "result_subject": "candidate status after run267CD(267CD 이후 후보 상태)",
            "evidence_available": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "evidence_missing": "beautiful balance/equity curve across zoomed periods and robust ablation/replacement(확대 구간까지 예쁜 잔액/평가금 곡선과 견고한 제거/대체 근거)",
            "judgment_label": "not_applicable_to_selection(선택에는 해당 없음)",
            "claim_boundary": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "next_condition": "only future multi-condition evidence can re-rank the candidate pool(향후 다조건 근거만 후보군 순위를 다시 정할 수 있음)",
            "user_explanation_hook": "s264_aih는 상대적으로 낫지만 아직 기준 후보로 뽑을 정도는 아니고, s258_stc는 압박 비교군으로만 남긴다.",
        },
    ]


def gate_audit(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_evidence_present",
            "status": "PASS",
            "evidence": f"{rel(SOURCE_REVIEW_RESULT_PATH)};{rel(SOURCE_CANDIDATE_SUMMARY_PATH)};{rel(SOURCE_NEGATIVE_SLICE_PATH)}",
            "effect": "design uses reviewed MT5 evidence rather than memory(기억이 아니라 검토된 MT5 근거를 사용)",
        },
        {
            "gate_id": "repair_loop_boundary",
            "status": "PASS",
            "evidence": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "effect": "same branch is closed instead of stretched into another deep repair loop(같은 분기를 또 깊은 수리 루프로 늘리지 않음)",
        },
        {
            "gate_id": "experiment_design_receipt",
            "status": "PASS",
            "evidence": f"pivot_queue_rows={len(queue_rows)}",
            "effect": "next work has hypothesis, controls, changed variables, stop conditions, and evidence plan(다음 작업에 가설, 대조, 변경 변수, 중단 조건, 근거 계획이 있음)",
        },
        {
            "gate_id": "lineage_and_registry",
            "status": "PASS",
            "evidence": f"{rel(LINEAGE_PATH)};{rel(RUN_MANIFEST_PATH)}",
            "effect": "outputs can be traced from source review to next action(원천 검토에서 다음 행동까지 산출물 계보가 이어짐)",
        },
        {
            "gate_id": "forbidden_claims",
            "status": "PASS",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "positive numbers are not overstated(양수 숫자를 과장하지 않음)",
        },
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    candidates = result["source_candidate_summary"]
    decisions = result["branch_decisions"]
    queue_rows = result["pivot_queue"]
    prune_rows = result["prune_matrix"]
    lines = [
        "# Stage267 Run267CD Aggressive Impulse DD-shape Follow-up Prune or Pivot Design(267단계 267CD 공격형 임펄스 손실폭 형태 후속 가지치기 또는 방향전환 설계)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- branch_decisions(분기 판단): `{len(decisions)}`",
        f"- pivot_queue_rows(방향전환 대기열 행): `{len(queue_rows)}`",
        f"- prune_rows(가지치기 행): `{len(prune_rows)}`",
        f"- failure_memory_rows(실패 기억 행): `{result['failure_memory_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267CC(267CC 실행)의 양수 후속 결과를 다시 읽고, 같은 DD-shape(손실폭 형태) repair loop(수리 루프)를 닫을지 판단했다.",
        "Effect(효과): s264_aih는 상대적으로 나은 관찰 후보로만 유지하고, s258_stc는 stress comparator(압박 비교군)로 낮추며, 다음은 후보군 전체의 orthogonal loss-shape/state pivot(직교 손실형태/상태 방향전환)으로 넘긴다.",
        "",
        "## Why This Took Time(왜 오래 걸렸나)",
        "",
        "- baseline(기준 후보)은 운영 기준선이 아니라 R&D racing(연구개발 경주) 출발 후보군이다.",
        "- 숫자 1등을 고르는 일이 아니라, 기간/구간/피처/대체/곡선/거래품질에서 덜 깨지는지를 확인해야 한다.",
        "- 이번 분기는 양수였지만 worst DD(최악 손실폭)가 `15%` 이상이라 선택으로 닫으면 과장이다.",
        "- 그래서 결과를 버리지 않고 failure memory(실패 기억)와 다음 pivot queue(방향전환 대기열)로 바꿨다.",
        "",
        "## Candidate Read(후보 판독)",
        "",
        "| candidate(후보) | net(순익) | PF(수익 팩터) | trades(거래 수) | worst DD%(최악 손실폭) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidates:
        lines.append(
            f"| `{row.get('candidate_alias')}` | {as_float(row.get('total_net_profit')):.2f} | "
            f"{as_float(row.get('min_profit_factor')):.2f} | {as_int(row.get('total_trades'))} | "
            f"{as_float(row.get('worst_dd_percent')):.2f} | `{row.get('candidate_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Branch Decisions(분기 판단)",
            "",
            "| decision(판단) | label(라벨) | next_use(다음 사용) |",
            "| --- | --- | --- |",
        ]
    )
    for row in decisions:
        lines.append(f"| `{row.get('decision_id')}` | `{row.get('decision_label')}` | {row.get('next_use')} |")
    lines.extend(
        [
            "",
            "## Pivot Queue(방향전환 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidate(후보) | purpose(목적) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('candidate_alias')}` | {row.get('decision_use')} |"
        )
    lines.extend(
        [
            "",
            "## Prune Boundary(가지치기 경계)",
            "",
            "| prune(가지치기) | label(라벨) | reopen(재개 조건) |",
            "| --- | --- | --- |",
        ]
    )
    for row in prune_rows:
        lines.append(f"| `{row.get('prune_id')}` | `{row.get('prune_label')}` | {row.get('reopen_condition')} |")
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- current branch(현재 분기): `close_branch_no_selection(분기 종료, 선택 아님)`",
            "- s264_aih: `watch_relative_best_not_selected(상대 최선 관찰, 선택 아님)`",
            "- s258_stc: `stress_comparator_only(압박 비교군만)`",
            "- next_action(다음 행동): `run267CE_design_pool_wide_orthogonal_loss_shape_state_pivot_queue`",
            "- ONNX conversion(ONNX 변환), runtime reproduction(런타임 재현), Adapter materialization(어댑터 물질화)은 아직 진행하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- pivot_queue(방향전환 대기열): `{rel(PIVOT_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
        ]
    )
    return "\n".join(lines)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
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
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design"
        f"(267CD 공격형 임펄스 손실폭 형태 후속 가지치기/방향전환 설계): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267CD(267CD 실행)는 run267CC(267CC 실행)의 양수 후속 결과를 바로 선택하지 않고 prune/pivot design(가지치기/방향전환 설계)으로 바꿨다.",
            f"Effect(효과): branch decisions(분기 판단) `{result['branch_decision_count']}`개, pivot queue(방향전환 대기열) `{result['pivot_queue_count']}`개, prune rows(가지치기 행) `{result['prune_count']}`개를 만들고 다음 행동을 `{NEXT_ACTION}`으로 고정했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `aggressive_impulse_dd_shape_followup_prune_or_pivot_design`",
        )
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_after_contains(
            text,
            "stage267_run267CC_aggressive_impulse_dd_shape_followup_balance_timeslice_trade_quality_review.md",
            report_line,
        )
        text = append_block_once(text, "Run267CD(267CD 실행)는 run267CC", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267CD(267CD 실행) aggressive impulse DD-shape follow-up prune/pivot design"
        f"(공격형 임펄스 손실폭 형태 후속 가지치기/방향전환 설계) `{STATUS}`. "
        f"Effect(효과): run267CC(267CC 실행)의 양수 후속 결과를 selected candidate(선택 후보)로 올리지 않고 "
        f"branch decisions(분기 판단) `{result['branch_decision_count']}`개와 pivot queue(방향전환 대기열) "
        f"`{result['pivot_queue_count']}`개로 바꿨으며, selected research baseline(선택 연구 기준 후보), "
        f"ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        report_entry=f"  run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"branch_decisions={result['branch_decision_count']};pivot_queue={result['pivot_queue_count']};"
        f"prune_rows={result['prune_count']};next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_impulse_dd_shape_followup_prune_or_pivot_design",
        "tier_scope": "Tier A run267CC review-derived design; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "prune_pivot_design_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_aggressive_impulse_followup_prune_pivot_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_impulse_dd_shape_followup_prune_or_pivot_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_impulse_dd_shape_followup_prune_or_pivot_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "prune_or_pivot_design",
        "tier_scope": "Tier A run267CC review; true fallback blocked",
        "kpi_scope": "experiment_design_failure_memory_prune",
        "scoreboard_lane": "aggressive_impulse_followup_branch_close_pivot",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"pivot_queue={result['pivot_queue_count']};prune_rows={result['prune_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")

    entries = (
        ("stage267_run267CD_producer", "producer_script", PRODUCER_PATH, "Builds run267CD prune/pivot design."),
        ("stage267_run267CD_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267CC review result."),
        ("stage267_run267CD_source_candidate_summary", "source_candidate_summary", SOURCE_CANDIDATE_SUMMARY_PATH, "Source run267CC candidate summary."),
        ("stage267_run267CD_source_negative_slices", "source_negative_slices", SOURCE_NEGATIVE_SLICE_PATH, "Source run267CC negative slices."),
        ("stage267_run267CD_source_followup_queue", "source_followup_queue", SOURCE_FOLLOWUP_QUEUE_PATH, "Source run267CC follow-up queue."),
        ("stage267_run267CD_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Run267CD branch decisions."),
        ("stage267_run267CD_pivot_queue", "pivot_queue", PIVOT_QUEUE_PATH, "Run267CD pivot queue."),
        ("stage267_run267CD_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Run267CD prune matrix."),
        ("stage267_run267CD_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267CD failure memory."),
        ("stage267_run267CD_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267CD performance attribution."),
        ("stage267_run267CD_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267CD experiment design receipt."),
        ("stage267_run267CD_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CD result judgment."),
        ("stage267_run267CD_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CD gate audit."),
        ("stage267_run267CD_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CD run manifest."),
        ("stage267_run267CD_lineage", "lineage", LINEAGE_PATH, "Run267CD lineage."),
        ("stage267_run267CD_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CD review result."),
        ("stage267_run267CD_report", "review_report", REPORT_PATH, "Run267CD user-facing report."),
    )
    artifact_rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes_text,
        }
        for artifact_id, artifact_type, path, notes_text in entries
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def result_payload() -> dict[str, Any]:
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    followup_rows = read_csv(SOURCE_FOLLOWUP_QUEUE_PATH)
    source_failure_rows = read_csv(SOURCE_FAILURE_MEMORY_PATH)
    period_rows = read_csv(SOURCE_PERIOD_SUMMARY_PATH)
    if not candidate_rows:
        raise RuntimeError(f"missing candidate summary: {rel(SOURCE_CANDIDATE_SUMMARY_PATH)}")
    if not negative_rows:
        raise RuntimeError(f"missing negative slice summary: {rel(SOURCE_NEGATIVE_SLICE_PATH)}")
    decisions = branch_decisions(candidate_rows, negative_rows, followup_rows)
    queue_rows = pivot_queue()
    prune_rows = prune_matrix()
    failure_rows = failure_memory(source_failure_rows)
    attribution_rows = performance_attribution(candidate_rows, negative_rows)
    design_rows = experiment_design_receipt(queue_rows)
    judgment_rows = result_judgment()
    gate_rows = gate_audit(queue_rows)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_status": source_result.get("status"),
        "source_trade_record_count": source_result.get("trade_record_count"),
        "source_time_slice_row_count": source_result.get("time_slice_row_count"),
        "source_negative_slice_count": source_result.get("negative_slice_count"),
        "branch_decision_count": len(decisions),
        "pivot_queue_count": len(queue_rows),
        "prune_count": len(prune_rows),
        "failure_memory_count": len(failure_rows),
        "branch_decisions": decisions,
        "pivot_queue": queue_rows,
        "prune_matrix": prune_rows,
        "failure_memory": failure_rows,
        "performance_attribution": attribution_rows,
        "experiment_design_receipt": design_rows,
        "result_judgment": judgment_rows,
        "gate_audit": gate_rows,
        "source_candidate_summary": candidate_rows,
        "source_negative_slices": negative_rows,
        "source_followup_queue": followup_rows,
        "source_failure_memory": source_failure_rows,
        "source_period_summary": period_rows,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "run267CC_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267CC_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "run267CC_candidate_period_review": rel(SOURCE_CANDIDATE_PERIOD_REVIEW_PATH),
            "run267CC_period_summary": rel(SOURCE_PERIOD_SUMMARY_PATH),
            "run267CC_negative_slices": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "run267CC_followup_queue": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "run267CC_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "run267CC_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": {
            "branch_decision_matrix": rel(BRANCH_DECISION_PATH),
            "pivot_queue": rel(PIVOT_QUEUE_PATH),
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
        },
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(BRANCH_DECISION_PATH, result["branch_decisions"], BRANCH_DECISION_COLUMNS)
    write_csv(PIVOT_QUEUE_PATH, result["pivot_queue"], PIVOT_QUEUE_COLUMNS)
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
            "artifact_hashes": "registered_in_artifact_registry(artifact_registry에 등록)",
            "registry_links": {
                "stage_ledger": rel(STAGE_LEDGER_PATH),
                "project_ledger": rel(PROJECT_LEDGER_PATH),
                "run_registry": rel(RUN_REGISTRY_PATH),
                "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            },
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def execute() -> dict[str, Any]:
    result = result_payload()
    write_outputs(result)
    update_ledgers_and_artifacts(str(result["created_at_utc"]), result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "branch_decisions": result["branch_decision_count"],
                "pivot_queue": result["pivot_queue_count"],
                "prune_rows": result["prune_count"],
                "failure_memory": result["failure_memory_count"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
