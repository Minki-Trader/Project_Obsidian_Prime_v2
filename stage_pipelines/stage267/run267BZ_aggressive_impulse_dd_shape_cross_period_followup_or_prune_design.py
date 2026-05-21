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
    run267BY_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267BZ"
RUN_ID = "run267BZ_stage267_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design_completed"
JUDGMENT = "followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CA_materialize_aggressive_impulse_dd_shape_followup_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_impulse_dd_shape_cross_period_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_CANDIDATE_PERIOD_REVIEW_PATH = source_review.CANDIDATE_PERIOD_REVIEW_PATH
SOURCE_PERIOD_SUMMARY_PATH = source_review.PERIOD_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_FOLLOWUP_QUEUE_PATH = source_review.FOLLOWUP_QUEUE_PATH
SOURCE_FAILURE_MEMORY_PATH = source_review.FAILURE_MEMORY_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design.py")

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

MATERIALIZATION_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "target_period",
    "target_weak_slice",
    "hypothesis",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
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


def rows_for_alias(rows: Sequence[Mapping[str, Any]], alias: str) -> list[Mapping[str, Any]]:
    return [row for row in rows if str(row.get("candidate_alias")) == alias]


def worst_negative_slice(rows: Sequence[Mapping[str, Any]], alias: str) -> Mapping[str, Any]:
    subset = rows_for_alias(rows, alias)
    return min(subset, key=lambda row: as_float(row.get("net_profit")), default={})


def make_branch_decisions(
    candidate_rows: Sequence[Mapping[str, Any]],
    period_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    s264_aih = row_by_alias(candidate_rows, "s264_aih")
    s258_stc = row_by_alias(candidate_rows, "s258_stc")
    s264_aia = row_by_alias(candidate_rows, "s264_aia")
    p2025h2 = next((row for row in period_rows if row.get("target_period") == "2025H2"), {})
    aih_slice = worst_negative_slice(negative_rows, "s264_aih")
    stc_slice = worst_negative_slice(negative_rows, "s258_stc")
    aia_slice = worst_negative_slice(negative_rows, "s264_aia")
    return [
        {
            "decision_id": "run267bz_d01_s264_aih_primary_aggressive_followup",
            "scope": "candidate",
            "candidate_alias": "s264_aih",
            "candidate_id": s264_aih.get("candidate_id", "s264_allow_inner_high_quarter"),
            "source_evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "observed_signal": f"total_net={as_float(s264_aih.get('total_net_profit'))};worst_dd={as_float(s264_aih.get('worst_dd_percent'))};min_pf={as_float(s264_aih.get('min_profit_factor'))}",
            "risk_or_gap": f"worst_slice={aih_slice.get('target_period')}/{aih_slice.get('axis')}={aih_slice.get('bucket')};net={as_float(aih_slice.get('net_profit'))}",
            "decision_label": "continue_as_primary_aggressive_challenger_no_selection(주 공격형 도전자로 계속, 선택 아님)",
            "next_use": "materialize one DD-shape/late-session guard and compare against unchanged aggressive impulse profile(손실폭 형태/후반 세션 방어 1개를 물질화해 원형과 비교)",
            "do_not_repeat": "do not claim research baseline from this branch; do not tune only one hour bucket(이 분기만으로 연구 기준 후보를 주장하지 말고 한 시간 구간만 조정하지 않음)",
            "stop_condition": "drop branch if net or PF collapses, or if 2025H2 late session damage moves elsewhere(순수익 또는 수익 팩터가 접히거나 2025H2 후반 세션 손상이 다른 곳으로 이동하면 중단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "run267bz_d02_s258_stc_stress_challenger_dd_cap",
            "scope": "candidate",
            "candidate_alias": "s258_stc",
            "candidate_id": s258_stc.get("candidate_id", "s258_short_tight_control"),
            "source_evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "observed_signal": f"total_net={as_float(s258_stc.get('total_net_profit'))};trades={as_int(s258_stc.get('total_trades'))}",
            "risk_or_gap": f"worst_dd={as_float(s258_stc.get('worst_dd_percent'))};worst_slice={stc_slice.get('target_period')}/{stc_slice.get('axis')}={stc_slice.get('bucket')};net={as_float(stc_slice.get('net_profit'))}",
            "decision_label": "stress_challenger_only_until_dd_shape_improves(손실폭 형태가 좋아질 때까지만 압박 도전자)",
            "next_use": "run one capped-risk stress variant; use as stress comparator, not as chosen candidate(위험 상한 압박 변형 1개만 실행해 압박 비교군으로 사용)",
            "do_not_repeat": "do not chase highest net while worst DD stays near 16 percent(최고 순수익만 보고 최악 손실폭 16% 근처를 따라가지 않음)",
            "stop_condition": "demote if capped variant keeps DD above 15 percent or keeps 22h/session_21_23 hole(상한 변형도 손실폭 15% 이상 또는 22시/21-23세션 구멍을 유지하면 격하)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "run267bz_d03_s264_aia_anchor_control_hold",
            "scope": "candidate",
            "candidate_alias": "s264_aia",
            "candidate_id": s264_aia.get("candidate_id", "s264_allow_inner_all_oos_anchor"),
            "source_evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "observed_signal": f"total_net={as_float(s264_aia.get('total_net_profit'))};min_pf={as_float(s264_aia.get('min_profit_factor'))}",
            "risk_or_gap": f"worst_dd={as_float(s264_aia.get('worst_dd_percent'))};worst_slice={aia_slice.get('target_period')}/{aia_slice.get('axis')}={aia_slice.get('bucket')}",
            "decision_label": "hold_as_oos_anchor_control_not_standalone(표본외 앵커 대조로 보류, 독립 후보 아님)",
            "next_use": "keep as comparison row only unless s264_aih or s258_stc follow-up fails(다른 후속이 실패할 때만 비교 행으로 재개)",
            "do_not_repeat": "do not reopen anchor just because headline total is positive(대표 총합이 양수라는 이유만으로 앵커를 재개하지 않음)",
            "stop_condition": "no new materialization in run267CA unless explicit control comparison is needed(명시 대조가 필요하지 않으면 다음 물질화 제외)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "run267bz_d04_2025h2_late_session_pressure",
            "scope": "period_slice",
            "candidate_alias": "pool_subset",
            "candidate_id": "s264_aih;s258_stc",
            "source_evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "observed_signal": f"2025H2_total_net={as_float(p2025h2.get('total_net_profit'))};worst_dd={as_float(p2025h2.get('worst_dd_percent'))}",
            "risk_or_gap": "close_hour_report=22 and session_21_23_report_time concentrate the deepest negative slices(22시와 21-23세션에 가장 깊은 음수 구간 집중)",
            "decision_label": "pressure_late_session_without_calendar_only_filter(달력 전용 필터 없이 후반 세션 압박)",
            "next_use": "probe state-shaped guard that can be explained by trade risk shape, not by one clock bucket(단일 시각이 아니라 거래 위험 형태로 설명되는 방어를 시험)",
            "do_not_repeat": "do not hard-delete 22h as a cosmetic repair(겉보기 수리로 22시를 단순 삭제하지 않음)",
            "stop_condition": "stop if guard reduces trades too much or shifts loss into Monday/month buckets(방어가 거래 수를 과하게 줄이거나 손실을 월요일/월 구간으로 옮기면 중단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_materialization_queue() -> list[dict[str, Any]]:
    common_controls = (
        "same source run267BW aggressive impulse profile, same 2023H2/2025H1/2025H2 splits, same MT5 settings, "
        "same trade parser and curve/time-slice review(동일 공격형 임펄스 원형, 동일 기간 분할, 동일 MT5 설정, 동일 거래/곡선/시간구간 검토)"
    )
    return [
        {
            "queue_id": "run267bz_q01_s264_aih_2025h2_late_session_dd_shape_guard",
            "priority": "P0",
            "workstream": "aggressive_impulse_dd_shape_followup(공격형 임펄스 손실폭 형태 후속)",
            "candidate_alias": "s264_aih",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_role": "challenger_core(핵심 도전자)",
            "target_period": "2025H2",
            "target_weak_slice": "close_hour_report=22;session_21_23_report_time",
            "hypothesis": "s264_aih can keep cross-period positivity while reducing late-session adverse-excursion damage(s264_aih가 확장 기간 양수를 유지하며 후반 세션 불리한 이동 손상을 줄일 수 있음)",
            "comparison_baseline": "run267BY unchanged s264_aih aggressive impulse profile(run267BY 원형 s264_aih 공격형 임펄스)",
            "control_variables": common_controls,
            "changed_variables": "add DD-shape guard using late-session adverse excursion and profit-giveback state(후반 세션 불리한 이동/수익 반납 상태 기반 손실폭 형태 방어 추가)",
            "success_criteria": "2025H2 late-session negative net improves without total trades collapsing below 120 and without PF below 1.55(2025H2 후반 세션 음수 개선, 거래 120 미만 붕괴 없음, 수익 팩터 1.55 아래 아님)",
            "failure_criteria": "net/PF collapse, DD moves to another period, or 22h repair becomes a calendar-only deletion(순수익/수익 팩터 붕괴, 손실폭 이동, 22시 달력 삭제화)",
            "invalid_conditions": "missing MT5 report, parser mismatch, feature order drift, or changed split(보고서 누락, 파서 불일치, 피처 순서 드리프트, 분할 변경)",
            "stop_conditions": "after one materialization plus MT5 review, either deepen once or prune; no long repair loop(물질화+MT5 검토 1회 뒤 한 번만 심화하거나 가지치기, 장기 수리 금지)",
            "evidence_plan": "MT5 report, trade_records, curve_diagnostics, time_slice_kpi, parser_checks, failure_memory(MT5 보고서, 거래 기록, 곡선 진단, 시간구간 핵심 성과 지표, 파서 확인, 실패 기억)",
            "materialization_instruction": "build next run267CA input variant with explicit changed-variable receipt and no candidate selection claim(변경 변수 영수증을 붙여 다음 실행 입력 변형 생성, 후보 선택 주장 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267bz_q02_s258_stc_2025h2_stress_dd_cap",
            "priority": "P0",
            "workstream": "stress_challenger_dd_cap(압박 도전자 손실폭 상한)",
            "candidate_alias": "s258_stc",
            "candidate_id": "s258_short_tight_control",
            "candidate_role": "stress_challenger(압박 도전자)",
            "target_period": "2025H2",
            "target_weak_slice": "close_hour_report=22;session_21_23_report_time;worst_dd_percent_near_16",
            "hypothesis": "s258_stc is useful only if net strength survives a real DD cap(s258_stc는 실제 손실폭 상한에서도 순수익 강도가 살아야 쓸모 있음)",
            "comparison_baseline": "run267BY unchanged s258_stc aggressive impulse profile(run267BY 원형 s258_stc 공격형 임펄스)",
            "control_variables": common_controls,
            "changed_variables": "cap high-risk late-session entries and require stronger risk/reward state(고위험 후반 세션 진입 상한 및 더 강한 위험/보상 상태 요구)",
            "success_criteria": "worst DD below 14.5 percent with total net still competitive against s264_aih(최악 손실폭 14.5% 미만, 총 순수익은 s264_aih와 경쟁 가능)",
            "failure_criteria": "trade count collapses, PF drops below 1.45, or DD remains at/above 15 percent(거래 수 붕괴, 수익 팩터 1.45 미만, 손실폭 15% 이상 유지)",
            "invalid_conditions": "same as q01 plus any hidden threshold-only drift(q01과 동일, 숨은 임계값 미세 변경 포함)",
            "stop_conditions": "if fails once, keep only as stress memory and do not keep polishing(한 번 실패하면 압박 기억으로만 보존하고 계속 다듬지 않음)",
            "evidence_plan": "same as q01 with candidate-level stress comparison(q01과 동일하며 후보 수준 압박 비교 포함)",
            "materialization_instruction": "build one capped-risk stress variant only; no second similar cap unless evidence is clearly new(위험 상한 압박 변형 1개만 생성, 새 근거 없으면 2차 유사 상한 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267bz_q03_s264_aih_2023h2_curve_zoom_sanity",
            "priority": "P1",
            "workstream": "curve_zoom_sanity(곡선 확대 정상성)",
            "candidate_alias": "s264_aih",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_role": "challenger_core(핵심 도전자)",
            "target_period": "2023H2",
            "target_weak_slice": "weakest candidate in 2023H2 period summary(2023H2 기간 요약에서 가장 약한 후보)",
            "hypothesis": "s264_aih should not only look best by DD; it must survive curve zoom in earlier adjacent period(s264_aih는 손실폭만 좋아 보이면 안 되고 이전 인접 기간 곡선 확대도 버텨야 함)",
            "comparison_baseline": "run267BY s264_aih 2023H2 candidate-period review(run267BY s264_aih 2023H2 후보 기간 검토)",
            "control_variables": common_controls,
            "changed_variables": "no model change; add review zoom and optional materialization only if curve hole is localized(모델 변경 없음, 곡선 확대 검토만 추가하고 구멍이 국소적일 때만 물질화)",
            "success_criteria": "no hidden deep drawdown after curve zoom and no month-level fragility stronger than source review(곡선 확대 뒤 깊은 숨은 손실폭 없음, 원천 검토보다 강한 월 취약성 없음)",
            "failure_criteria": "curve zoom exposes deep hole that was masked by aggregate KPI(곡선 확대가 집계 핵심 성과 지표에 가려진 깊은 구멍을 드러냄)",
            "invalid_conditions": "missing curve diagnostics or inconsistent trade ordering(곡선 진단 누락 또는 거래 순서 불일치)",
            "stop_conditions": "if curve zoom fails, do not materialize extra guards; demote branch to clue only(곡선 확대가 실패하면 추가 방어 물질화 없이 단서로 격하)",
            "evidence_plan": "curve_diagnostics, candidate_period_review, negative_slice_summary(곡선 진단, 후보 기간 검토, 음수 구간 요약)",
            "materialization_instruction": "design-review row first; materialize only after q01/q02 result or explicit curve-hole evidence(먼저 설계 검토 행, q01/q02 결과 또는 명시 곡선 구멍 근거 뒤 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "run267bz_p01_no_headline_positive_selection",
            "scope": "selection_claim(선택 주장)",
            "prune_label": "prune_now(현재 가지치기)",
            "evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "why_pruned": "all three candidates are positive, but Tier B, routed total, Adapter structure, and curve zoom are still missing(세 후보가 모두 양수지만 티어 B, 실제 라우팅 전체, 어댑터 구조, 곡선 확대가 아직 없음)",
            "salvage_value": "use headline positives only as follow-up priority(대표 양수는 후속 우선순위로만 사용)",
            "reopen_condition": "reopen selection only after materialized follow-up survives MT5 and trade-quality review(물질화 후속이 MT5와 거래 품질 검토를 버틴 뒤에만 선택 재개)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267bz_p02_no_calendar_only_22h_filter",
            "scope": "repair_method(수리 방식)",
            "prune_label": "blocked_as_overfit_risk(과적합 위험으로 차단)",
            "evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "why_pruned": "22h is a visible weak bucket, but deleting one clock bucket would hide whether risk shape is real(22시는 보이는 약점이지만 한 시각 삭제는 위험 형태가 실제인지 숨김)",
            "salvage_value": "convert to state-shaped DD guard evidence(상태 기반 손실폭 방어 근거로 변환)",
            "reopen_condition": "only if multiple periods prove the same clock bucket is structurally invalid(여러 기간에서 같은 시각 구간이 구조적으로 무효임이 증명될 때만 재개)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267bz_p03_s264_aia_no_standalone_materialization",
            "scope": "s264_aia",
            "prune_label": "hold_as_control(대조군 보류)",
            "evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "why_pruned": "OOS anchor has positive net but DD watch remains and it is not the most stable aggressive branch(표본외 앵커는 양수지만 손실폭 관찰이 남고 공격형 분기에서 가장 안정적이지 않음)",
            "salvage_value": "control row for s264_aih/s258_stc follow-up comparison(s264_aih/s258_stc 후속 비교 대조 행)",
            "reopen_condition": "reopen only if primary/stress follow-ups fail or control contrast is required(주/압박 후속 실패 또는 대조 필요 때만 재개)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_failure_memory(source_failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    inherited = ";".join(str(row.get("memory_id")) for row in source_failure_rows)
    return [
        {
            "memory_id": "run267bz_headline_positive_still_not_selection",
            "pattern": "headline_positive_but_evidence_incomplete(대표 양수지만 근거 미완성)",
            "evidence": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "affected_scope": "s258_stc;s264_aih;s264_aia",
            "why_failed_or_fragile": "positive cross-period totals do not prove curve smoothness, routed total, or Adapter durability(확장 기간 총합 양수는 곡선 매끈함, 실제 라우팅 전체, 어댑터 내구성을 증명하지 않음)",
            "do_not_repeat": "do not select candidate or start ONNX review from run267BY headline KPI(run267BY 대표 핵심 성과 지표만으로 후보 선택 또는 ONNX 검토 시작 금지)",
            "salvage_angle": "use as prioritization for q01/q02 follow-up(q01/q02 후속 우선순위로 사용)",
            "reopen_condition": "after run267CA/CB MT5 execution and balance/time-slice review(다음 물질화/MT5/잔액 시간구간 검토 뒤)",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267bz_2025h2_late_session_concentration",
            "pattern": "late_session_weak_slice_concentration(후반 세션 약점 집중)",
            "evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "affected_scope": "2025H2 close_hour_report=22;session_21_23_report_time",
            "why_failed_or_fragile": "deepest negative slices cluster in late session and can distort an otherwise positive period(가장 깊은 음수 구간이 후반 세션에 모여 양수 기간을 왜곡할 수 있음)",
            "do_not_repeat": "do not make a pure clock deletion repair(순수 시각 삭제 수리 금지)",
            "salvage_angle": "test DD-shape or adverse-excursion guard(손실폭 형태 또는 불리한 이동 방어 시험)",
            "reopen_condition": "if next guard improves slice without shifting loss elsewhere(다음 방어가 손실 이동 없이 구간을 개선할 때)",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267bz_inherited_run267by_failure_memory",
            "pattern": "inherited_failure_memory(상속 실패 기억)",
            "evidence": rel(SOURCE_FAILURE_MEMORY_PATH),
            "affected_scope": inherited or "none",
            "why_failed_or_fragile": "run267BZ consumes run267BY failure memory instead of resetting branch context(run267BZ는 분기 문맥을 초기화하지 않고 run267BY 실패 기억을 소비)",
            "do_not_repeat": "do not loop this repair beyond one materialization plus one review without prune decision(가지치기 판단 없이 물질화 1회와 검토 1회를 넘겨 반복 금지)",
            "salvage_angle": "keep only evidence-backed q01/q02/q03 work(q01/q02/q03 근거 기반 작업만 유지)",
            "reopen_condition": "new period or feature-replacement evidence, not same threshold polish(같은 임계값 다듬기가 아닌 새 기간 또는 피처 대체 근거)",
            "boundary": CLAIM_BOUNDARY,
        },
    ]


def make_performance_attribution(candidate_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    s264_aih = row_by_alias(candidate_rows, "s264_aih")
    s258_stc = row_by_alias(candidate_rows, "s258_stc")
    return [
        {
            "attribution_id": "run267bz_attr01_s264_aih_stability_vs_net",
            "observed_change": f"s264_aih lower worst DD than s258_stc while total net is lower(s264_aih는 s258_stc보다 최악 손실폭은 낮고 총 순수익은 낮음): {as_float(s264_aih.get('worst_dd_percent'))} vs {as_float(s258_stc.get('worst_dd_percent'))}",
            "comparison_baseline": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "likely_drivers": "risk shape and late-session exposure, not broad period failure(넓은 기간 실패가 아니라 위험 형태와 후반 세션 노출)",
            "segment_checks": "2025H2, close_hour_report=22, session_21_23_report_time",
            "trade_shape": "all candidates still have enough trades; next probe should not collapse count(모든 후보 거래 수는 충분, 다음 시험은 거래 수를 붕괴시키면 안 됨)",
            "alternative_explanations": "positive totals may reflect aggressive profile exposure rather than durable decision surface(양수 총합은 내구성 있는 결정 표면보다 공격형 노출 때문일 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "s264_aih late-session DD-shape guard(s264_aih 후반 세션 손실폭 형태 방어)",
        },
        {
            "attribution_id": "run267bz_attr02_negative_slice_concentration",
            "observed_change": f"negative_slice_rows={len(negative_rows)} with largest losses in 2025H2 late session(음수 구간 {len(negative_rows)}개, 최대 손실은 2025H2 후반 세션)",
            "comparison_baseline": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "likely_drivers": "time-local risk exposure and adverse excursion(시간 국소 위험 노출과 불리한 이동)",
            "segment_checks": "hour/session/month/weekday cross-check required(시간/세션/월/요일 교차 확인 필요)",
            "trade_shape": "late-session slices have small trade count but large loss impact(후반 세션 구간은 거래 수는 작고 손실 영향은 큼)",
            "alternative_explanations": "MT5 report path or parser issue checked in run267BY; parser matched source counts(MT5 보고서/파서 문제는 run267BY에서 원천 수량 일치 확인)",
            "attribution_confidence": "medium_high(중상)",
            "next_probe": "state-shaped guard, not calendar-only cut(달력 전용 절단이 아닌 상태 기반 방어)",
        },
    ]


def make_design_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": row["queue_id"],
            "hypothesis": row["hypothesis"],
            "decision_use": row["workstream"],
            "comparison_baseline": row["comparison_baseline"],
            "control_variables": row["control_variables"],
            "changed_variables": row["changed_variables"],
            "sample_scope": row["target_period"],
            "success_criteria": row["success_criteria"],
            "failure_criteria": row["failure_criteria"],
            "invalid_conditions": row["invalid_conditions"],
            "stop_conditions": row["stop_conditions"],
            "evidence_plan": row["evidence_plan"],
        }
        for row in queue_rows
    ]


def make_result_judgment(queue_rows: Sequence[Mapping[str, Any]], prune_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"run267BY review result, candidate summary, period summary, negative slices, follow-up queue({rel(SOURCE_REVIEW_RESULT_PATH)};{rel(SOURCE_CANDIDATE_SUMMARY_PATH)};{rel(SOURCE_NEGATIVE_SLICE_PATH)})",
            "evidence_missing": "new MT5 execution, Adapter materialization, Tier B routed evidence, actual routed total, ONNX parity(새 MT5 실행, 어댑터 물질화, 티어 B 라우팅 근거, 실제 라우팅 전체, ONNX 동등성)",
            "judgment_label": "exploratory_design_completed(탐색 설계 완료)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": f"materialize {len(queue_rows)} queue rows and execute/review before any stronger claim({len(queue_rows)}개 대기열 물질화와 실행/검토 전까지 강한 주장 금지)",
            "user_explanation_hook": "이번 실행은 후보를 고른 게 아니라, 어떤 후속은 살리고 어떤 방식은 버릴지 정한 설계다.",
        },
        {
            "result_subject": "prune_boundary(가지치기 경계)",
            "evidence_available": f"prune_rows={len(prune_rows)}; failure memory connected(가지치기 행 {len(prune_rows)}개, 실패 기억 연결)",
            "evidence_missing": "post-prune execution evidence(가지치기 뒤 실행 근거)",
            "judgment_label": "not_applicable_selection(선택 판정 해당 없음)",
            "claim_boundary": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "next_condition": "run267CA materialization then MT5 execution/review(run267CA 물질화 뒤 MT5 실행/검토)",
            "user_explanation_hook": "오래 걸리는 이유는 숫자 1등을 고르는 게 아니라, 깨지는 방식을 제거하면서 남길 후보를 찾기 때문이다.",
        },
    ]


def make_gate_audit(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_review_available(원천 검토 존재)",
            "status": "passed(통과)",
            "evidence": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267BZ is grounded in run267BY trade-level review(run267BZ가 run267BY 거래 단위 검토에 근거)",
        },
        {
            "gate_id": "no_selection_claim(선택 주장 없음)",
            "status": "passed(통과)",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "design cannot be mistaken for candidate selection(설계를 후보 선택으로 오해하지 않게 함)",
        },
        {
            "gate_id": "bounded_repair_loop(제한된 수리 루프)",
            "status": "passed_with_watch(관찰 포함 통과)",
            "evidence": f"queue_rows={len(queue_rows)}",
            "effect": "next work is one materialization plus review before deepen/prune decision(다음은 물질화 1회와 검토 뒤 심화/가지치기 판단)",
        },
        {
            "gate_id": "artifact_lineage_connected(산출물 계보 연결)",
            "status": "passed(통과)",
            "evidence": rel(LINEAGE_PATH),
            "effect": "source and outputs are traceable(원천과 출력 추적 가능)",
        },
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = result["source_candidate_summary"]
    queue_rows = result["materialization_queue"]
    prune_rows = result["prune_matrix"]
    negative_rows = result["source_negative_slices"][:8]
    lines = [
        "# Stage267 Run267BZ Aggressive Impulse Follow-up/Prune Design(267단계 267BZ 공격형 임펄스 후속/가지치기 설계)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- branch_decisions(분기 판단): `{len(result['branch_decisions'])}`",
        f"- materialization_queue(물질화 대기열): `{len(queue_rows)}`",
        f"- prune_rows(가지치기 행): `{len(prune_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BY(267BY 실행)의 양수 총합, 손실폭, 후반 세션 약점을 후속 대기열과 가지치기 판단으로 바꿨다.",
        "Effect(효과): 최고 숫자 후보를 바로 고르지 않고, 어떤 후보는 더 압박하고 어떤 수리 방식은 반복하지 않을지 고정했다.",
        "",
        "## Candidate Read(후보 판독)",
        "",
        "| candidate(후보) | total net(총 순수익) | min PF(최저 수익 팩터) | worst DD%(최악 손실폭 %) | trades(거래 수) | decision(판단) |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidate_rows:
        alias = row.get("candidate_alias")
        decision = {
            "s264_aih": "P0 continue(우선 계속)",
            "s258_stc": "P0 stress with DD cap(손실폭 상한 압박)",
            "s264_aia": "control hold(대조 보류)",
        }.get(str(alias), "watch(관찰)")
        lines.append(
            f"| `{alias}` | {as_float(row.get('total_net_profit'))} | {as_float(row.get('min_profit_factor'))} | "
            f"{as_float(row.get('worst_dd_percent'))} | {as_int(row.get('total_trades'))} | {decision} |"
        )
    lines.extend(
        [
            "",
            "## Next Queue(다음 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidate(후보) | target(목표) | purpose(목적) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('candidate_alias')}` | "
            f"`{row.get('target_period')}` / `{row.get('target_weak_slice')}` | {row.get('workstream')} |"
        )
    lines.extend(
        [
            "",
            "## Prune Matrix(가지치기 행렬)",
            "",
            "| prune(가지치기) | scope(범위) | reason(이유) | reopen(재개 조건) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in prune_rows:
        lines.append(
            f"| `{row.get('prune_id')}` | {row.get('scope')} | {row.get('why_pruned')} | {row.get('reopen_condition')} |"
        )
    lines.extend(
        [
            "",
            "## Worst Negative Slices(최악 음수 구간)",
            "",
            "| candidate(후보) | period(기간) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | DD%(손실폭 %) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negative_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('target_period')}` | `{row.get('axis')}` | "
            f"`{row.get('bucket')}` | {as_int(row.get('trade_count'))} | {as_float(row.get('net_profit'))} | "
            f"{as_float(row.get('closed_balance_max_drawdown_percent'))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- run267BZ(267BZ 실행)는 design-only(설계 전용) 증거다.",
            "- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 없다.",
            "- 다음은 run267CA(267CA 실행) 물질화이며, 그 뒤 MT5(MetaTrader 5, 메타트레이더5) 실행과 거래 품질 검토가 필요하다.",
            "- 같은 약점만 계속 깎는 수리 루프는 금지하며, 한 번 더 실행 후 살릴지 버릴지 판단한다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
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


def update_stage267_workspace_block(text: str, *, status: str, next_action: str, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    report_seen = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not report_seen:
                output.append(report_entry)
                report_seen = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not report_seen:
                    output.append(report_entry)
                    report_seen = True
                output.append(f"  next_action: {next_action}")
                continue
        output.append(line)
    if in_stage267 and not report_seen:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design(267BZ 공격형 임펄스 손실폭 형태 확장 기간 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BZ(267BZ 실행)는 run267BY(267BY 실행)의 양수 총합을 바로 선택하지 않고 후속/가지치기 설계로 바꿨다.",
            f"Effect(효과): materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개, prune rows(가지치기 행) `{result['prune_count']}`개, failure memory(실패 기억) `{result['failure_memory_count']}`개를 만들고 다음 행동을 `{next_action}`으로 고정했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 없다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `aggressive_impulse_dd_shape_cross_period_followup_or_prune_design`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        text = append_after_contains(text, "stage267_run267BY_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality_review.md", report_line)
        text = append_block_once(text, "Run267BZ(267BZ 실행)는", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BZ(267BZ 실행) aggressive impulse DD-shape cross-period follow-up/prune design(공격형 임펄스 손실폭 형태 확장 기간 후속/가지치기 설계) `{status}`. "
        f"Effect(효과): run267BY(267BY 실행)의 양수 총합을 즉시 선택하지 않고 materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개와 prune matrix(가지치기 행렬) `{result['prune_count']}`개로 바꿨으며 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        status=status,
        next_action=next_action,
        report_entry=f"  run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    notes = (
        f"branch_decisions={result['branch_decision_count']};materialization_queue={result['materialization_queue_count']};"
        f"prune_rows={result['prune_count']};next_action={next_action};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_impulse_dd_shape_cross_period_followup_or_prune_design",
        "tier_scope": "Tier A source review design; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "followup_prune_design_failure_memory",
        "status": status,
        "judgment": judgment,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_aggressive_impulse_followup_prune_design",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_impulse_dd_shape_cross_period_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_impulse_dd_shape_cross_period_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_or_prune_design",
        "tier_scope": "Tier A run267BY review; true fallback blocked",
        "kpi_scope": "experiment_design_failure_memory_prune",
        "scoreboard_lane": "aggressive_impulse_cross_period_followup_design",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"materialization_queue={result['materialization_queue_count']};prune_rows={result['prune_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {next_action}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")

    entries = (
        ("stage267_run267BZ_producer", "producer_script", PRODUCER_PATH, "Builds run267BZ follow-up/prune design."),
        ("stage267_run267BZ_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267BY review result."),
        ("stage267_run267BZ_source_candidate_summary", "source_candidate_summary", SOURCE_CANDIDATE_SUMMARY_PATH, "Source run267BY candidate summary."),
        ("stage267_run267BZ_source_negative_slices", "source_negative_slices", SOURCE_NEGATIVE_SLICE_PATH, "Source run267BY negative slices."),
        ("stage267_run267BZ_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Run267BZ branch decisions."),
        ("stage267_run267BZ_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267BZ materialization queue."),
        ("stage267_run267BZ_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Run267BZ prune matrix."),
        ("stage267_run267BZ_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267BZ failure memory."),
        ("stage267_run267BZ_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267BZ performance attribution."),
        ("stage267_run267BZ_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BZ experiment design receipt."),
        ("stage267_run267BZ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BZ result judgment."),
        ("stage267_run267BZ_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BZ gate audit."),
        ("stage267_run267BZ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BZ run manifest."),
        ("stage267_run267BZ_lineage", "lineage", LINEAGE_PATH, "Run267BZ lineage."),
        ("stage267_run267BZ_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BZ review result."),
        ("stage267_run267BZ_report", "review_report", REPORT_PATH, "Run267BZ user-facing report."),
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
            "notes": notes_text,
        }
        for artifact_id, artifact_type, path, notes_text in entries
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def result_payload() -> dict[str, Any]:
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    candidate_period_rows = read_csv(SOURCE_CANDIDATE_PERIOD_REVIEW_PATH)
    period_rows = read_csv(SOURCE_PERIOD_SUMMARY_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    source_queue_rows = read_csv(SOURCE_FOLLOWUP_QUEUE_PATH)
    source_failure_rows = read_csv(SOURCE_FAILURE_MEMORY_PATH)
    branch_decisions = make_branch_decisions(candidate_rows, period_rows, negative_rows)
    materialization_queue = make_materialization_queue()
    prune_matrix = make_prune_matrix()
    failure_memory = make_failure_memory(source_failure_rows)
    performance_attribution = make_performance_attribution(candidate_rows, negative_rows)
    experiment_design = make_design_receipts(materialization_queue)
    result_judgment = make_result_judgment(materialization_queue, prune_matrix)
    gate_audit = make_gate_audit(materialization_queue)
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
        "branch_decision_count": len(branch_decisions),
        "materialization_queue_count": len(materialization_queue),
        "prune_count": len(prune_matrix),
        "failure_memory_count": len(failure_memory),
        "branch_decisions": branch_decisions,
        "materialization_queue": materialization_queue,
        "prune_matrix": prune_matrix,
        "failure_memory": failure_memory,
        "performance_attribution": performance_attribution,
        "experiment_design_receipt": experiment_design,
        "result_judgment": result_judgment,
        "gate_audit": gate_audit,
        "source_candidate_summary": candidate_rows,
        "source_candidate_period_review": candidate_period_rows,
        "source_period_summary": period_rows,
        "source_negative_slices": negative_rows,
        "source_followup_queue": source_queue_rows,
        "source_failure_memory": source_failure_rows,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "run267BY_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267BY_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "run267BY_candidate_period_review": rel(SOURCE_CANDIDATE_PERIOD_REVIEW_PATH),
            "run267BY_period_summary": rel(SOURCE_PERIOD_SUMMARY_PATH),
            "run267BY_negative_slices": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "run267BY_followup_queue": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "run267BY_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "run267BY_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": {
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
        },
    }


def write_outputs(result: Mapping[str, Any]) -> None:
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
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
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
                "materialization_queue": result["materialization_queue_count"],
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
