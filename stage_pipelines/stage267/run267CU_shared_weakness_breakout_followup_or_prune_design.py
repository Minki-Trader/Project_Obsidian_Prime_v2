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
    run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267CU"
RUN_ID = "run267CU_stage267_shared_weakness_breakout_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267CU_shared_weakness_breakout_followup_or_prune_design_completed"
JUDGMENT = "followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CV_materialize_shared_weakness_breakout_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_PROFILE_AXIS_PATH = source_review.PROFILE_AXIS_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_ATTRIBUTION_PATH = source_review.ATTRIBUTION_SUMMARY_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

FEATURE_BLUEPRINT_PATH = RUN_ROOT / "feature_blueprint.csv"
BRANCH_DECISION_PATH = RUN_ROOT / "branch_decisions.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
MODEL_VALIDATION_RECEIPT_PATH = RUN_ROOT / "model_validation_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CU_shared_weakness_breakout_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CU_shared_weakness_breakout_followup_or_prune_design.py")

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

CANDIDATE_NAME = {
    "s264_aih": "s264_allow_inner_high_quarter",
    "s264_lc": "s264_lowrank_control",
    "s262_lih": "s262_lowrank_inner_half_filter",
    "s264_aia": "s264_allow_inner_all_oos_anchor",
    "s258_stc": "s258_short_tight_control",
}

CANDIDATE_ROLE = {
    "s264_aih": "challenger_core(핵심 도전자)",
    "s264_lc": "defensive_control(방어 대조)",
    "s262_lih": "validation_heavy(검증 중심)",
    "s264_aia": "oos_anchor(표본외 앵커)",
    "s258_stc": "stress_challenger(압박 도전자)",
}

FEATURE_BLUEPRINT_COLUMNS = (
    "feature_id",
    "feature_family",
    "market_meaning",
    "candidate_scope",
    "source_evidence",
    "changed_variables",
    "similar_replacement_axis",
    "aggressive_or_defensive",
    "do_not_use_as",
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
    "best_profile",
    "best_net_profit",
    "best_profit_factor",
    "best_equity_drawdown_percent",
    "best_trade_count",
    "worst_month",
    "worst_month_net",
    "weakest_slice",
    "decision_label",
    "next_use",
    "why",
    "risk_boundary",
    "reopen_condition",
    "claim_boundary",
)

MATERIALIZATION_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_aliases",
    "feature_blueprint_scope",
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
    "prune_label",
    "affected_scope",
    "why_pruned",
    "reopen_condition",
    "claim_boundary",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "affected_scope",
    "evidence",
    "why_fragile",
    "do_not_repeat",
    "salvage_angle",
    "reopen_condition",
    "claim_boundary",
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

DATA_INTEGRITY_COLUMNS = (
    "receipt_id",
    "data_source",
    "time_axis",
    "sample_scope",
    "missing_or_duplicate_check",
    "feature_label_boundary",
    "split_boundary",
    "leakage_risk",
    "data_hash_or_identity",
    "integrity_judgment",
)

MODEL_VALIDATION_COLUMNS = (
    "receipt_id",
    "model_family",
    "target_and_label",
    "split_method",
    "selection_metric",
    "secondary_metrics",
    "threshold_policy",
    "overfit_risk",
    "calibration_risk",
    "comparison_baseline",
    "validation_judgment",
)

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "selected_candidate",
    "selected_research_baseline",
    "onnx_readiness",
    "goal_achieve",
    "next_condition",
    "claim_boundary",
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
        return list(csv.DictReader(handle))


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


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            break
    return "\n".join(lines) + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            break
    return "\n".join(lines) + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, item in enumerate(lines):
        if needle in item:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_line: str) -> str:
    if f"`{STATUS}`" in text:
        return text
    return text.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            as_float(row.get("net_profit")),
            as_float(row.get("profit_factor")),
            -as_float(row.get("report_equity_drawdown_percent")),
            as_int(row.get("trade_count")),
        ),
    )


def weak_slice_for(candidate_alias: str, negative_rows: Sequence[Mapping[str, Any]]) -> str:
    rows = [row for row in negative_rows if row.get("candidate_alias") == candidate_alias]
    if not rows:
        return "none_recorded(기록 없음)"
    weakest = min(rows, key=lambda row: as_float(row.get("net_profit")))
    return f"{weakest.get('axis')}:{weakest.get('bucket')}:{weakest.get('net_profit')}"


def feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "cu_fb01_state_phase_cross_period_reconfirmation",
            "feature_family": "state_phase_replacement_cross_period(상태 국면 대체 확장 기간)",
            "market_meaning": "2024년에서 좋아 보인 state_phase(상태 국면)가 다른 기간에서도 시장 구조를 잡는지 확인한다.",
            "candidate_scope": "s264_aih;s264_aia",
            "source_evidence": "run267CT에서 s264_aih state_phase net=1796.20 PF=1.5013 DD=12.77, s264_aia state_phase net=1686.26 PF=1.5103 DD=14.60.",
            "changed_variables": "period pack only: 2023H2, 2025H1, 2025H2; keep feature order, model bundle, risk, cost, and MT5 tester settings fixed.",
            "similar_replacement_axis": "state_phase(상태 국면)를 period-adjacent replacement(인접 기간 대체)로 먼저 압박한다.",
            "aggressive_or_defensive": "balanced_pressure(균형 압박)",
            "do_not_use_as": "selection(선택) or ONNX readiness(ONNX 준비) 근거",
            "success_read": "여러 기간에서 PF>=1.35, trades>=250, DD<=22%, worst_month_net>-180을 동시에 유지한다.",
            "failure_read": "한 기간에서 net이 음수로 무너지거나, 월별 구멍이 -220 아래로 깊어지면 후보 선택 후보군에서 낮춘다.",
            "materialization_note": "run267CV는 s264_aih/s264_aia x 3 periods x Tier A/duplicate routed boundary attempt(시도)를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cu_fb02_redzone_monday_dd_pressure",
            "feature_family": "redzone_stress_loss_shape(위험 구역 손실 형태)",
            "market_meaning": "s258_stc의 높은 net(순수익)이 Monday(월요일) 손실과 DD(손실폭)를 견디는 진짜 edge(우위)인지 확인한다.",
            "candidate_scope": "s258_stc",
            "source_evidence": "run267CT s258_stc redzone net=1900.77 PF=1.4414 DD=13.93, Monday net=-266.64.",
            "changed_variables": "redzone stress threshold, loss-shape cooldown, shock persistence; no literal weekday ban.",
            "similar_replacement_axis": "calendar(달력) 대신 loss_shape(손실 형태)와 volatility shock(변동성 충격) proxy(대리 지표)로 대체한다.",
            "aggressive_or_defensive": "aggressive_pressure(공격 압박)",
            "do_not_use_as": "single best KPI(단일 최고 지표) 선택",
            "success_read": "net>1700, PF>=1.40, DD<=18%, Monday net>-180, session_07_12 손실이 더 깊어지지 않는다.",
            "failure_read": "Monday net<-220 또는 DD>22이면 stress branch(압박 분기)를 가지치기한다.",
            "materialization_note": "run267CV는 redzone stress와 Monday/DD slice(월요일/손실폭 구간)를 직접 압박한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cu_fb03_explosive_shock_state_combo",
            "feature_family": "explosive_shock_state_combo(폭발형 충격-상태 조합)",
            "market_meaning": "방어 필터를 덧붙이지 않고 shock(충격), state phase(상태 국면), loss shape(손실 형태)를 조합해 수익 상단을 과감하게 연다.",
            "candidate_scope": "s264_aih;s264_aia;s258_stc",
            "source_evidence": "run267CT 상위 net 단서 3개와 profile_axis_summary의 state_phase/redzone constructive watch(건설적 관찰).",
            "changed_variables": "shock acceleration, state phase interaction, redzone release; no calendar ban and no narrow one-threshold tuning.",
            "similar_replacement_axis": "ADX/DI류 trend strength(추세 강도)를 shock persistence(충격 지속)와 range expansion(범위 확장)으로 대체한다.",
            "aggressive_or_defensive": "explosive_aggressive(폭발형 공격)",
            "do_not_use_as": "repair loop(수리 반복) 또는 defensive filter stack(방어 필터 누적)",
            "success_read": "net>2200, trades>=450, PF>=1.35, DD<=24%, worst_month_net>-200.",
            "failure_read": "DD가 28%를 넘거나 약점 월/요일이 더 깊어지면 폭발형 조합은 실패 기억으로 닫는다.",
            "materialization_note": "run267CV는 제한된 P0 폭발형 attempt(시도)만 만들고, 실패 시 길게 끌지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cu_fb04_aggressive_supply_repair_or_prune",
            "feature_family": "aggressive_supply_repair_or_prune(공격형 공급 수리 또는 가지치기)",
            "market_meaning": "s264_aih aggressive_shock_supply_expansion의 높은 PF가 거래 공급 부족으로 생긴 착시인지 확인한다.",
            "candidate_scope": "s264_aih",
            "source_evidence": "run267CT s264_aih aggressive supply PF=1.7811 but trades=251 and net=831.95.",
            "changed_variables": "entry supply gate, shock release width, risk handoff; keep core score surface fixed.",
            "similar_replacement_axis": "thin supply(얇은 공급)를 entry supply expansion(진입 공급 확장)으로 대체한다.",
            "aggressive_or_defensive": "bounded_repair(제한 수리)",
            "do_not_use_as": "third-stage repair loop(3단계 이상 수리 반복)",
            "success_read": "trades>=320, net>1200, PF>=1.55, DD<=16을 동시에 만족한다.",
            "failure_read": "trade count가 늘면 PF/net이 급락하거나 DD가 확대되면 이 branch(분기)는 가지치기한다.",
            "materialization_note": "run267CV는 최대 2개 attempt(시도)로 수리/폐기 판단을 끝낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_branch_decisions(
    candidate_rows: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in candidate_rows:
        grouped.setdefault(str(row.get("candidate_alias")), []).append(row)
    summary_by_alias = {str(row.get("candidate_alias")): row for row in summary_rows}
    decisions: list[dict[str, Any]] = []
    order = ("s264_aih", "s264_aia", "s258_stc", "s264_lc", "s262_lih")
    labels = {
        "s264_aih": (
            "dual_track_watch_no_selection(이중 추적 관찰, 선택 아님)",
            "P0 cross-period reconfirmation plus bounded aggressive supply repair(확장 기간 재확인 + 제한 공격 공급 수리)",
            "state_phase는 균형이 좋지만 aggressive supply는 거래 수가 얇다.",
        ),
        "s264_aia": (
            "balanced_anchor_followup_no_selection(균형 앵커 후속, 선택 아님)",
            "P0 cross-period reconfirmation with s264_aih(확장 기간 재확인)",
            "PF와 DD가 양호하지만 2024-06 약점과 validation 손상 이력이 남아 있다.",
        ),
        "s258_stc": (
            "high_profit_stress_watch_no_selection(고수익 압박 관찰, 선택 아님)",
            "P0 redzone Monday/DD pressure and explosive combo(위험 구역 월요일/DD 압박 + 폭발형 조합)",
            "순수익은 가장 크지만 Monday 손실이 깊어서 바로 고르면 위험하다.",
        ),
        "s264_lc": (
            "mixed_control_pressure_no_selection(혼합 대조 압박, 선택 아님)",
            "P1 guardrail/control retest only(가드레일/대조 재시험)",
            "거래 수는 좋지만 DD와 2024-06 손상이 불편하다.",
        ),
        "s262_lih": (
            "validation_guardrail_continue_no_selection(검증 가드레일 유지, 선택 아님)",
            "P1 guardrail retest and ablation reference(가드레일 재시험과 제거 기준)",
            "검증 안정성 역할은 유지하지만 PF와 net이 상위권보다 약하다.",
        ),
    }
    for index, alias in enumerate(order, start=1):
        rows = grouped.get(alias, [])
        if not rows:
            continue
        row = best_row(rows)
        label, next_use, why = labels[alias]
        summary = summary_by_alias.get(alias, {})
        decisions.append(
            {
                "decision_id": f"cu_d{index:02d}_{alias}",
                "candidate_alias": alias,
                "candidate_id": row.get("candidate_id") or CANDIDATE_NAME[alias],
                "candidate_role": row.get("candidate_role") or CANDIDATE_ROLE[alias],
                "best_profile": row.get("test_id"),
                "best_net_profit": as_float(row.get("net_profit")),
                "best_profit_factor": as_float(row.get("profit_factor")),
                "best_equity_drawdown_percent": as_float(row.get("report_equity_drawdown_percent")),
                "best_trade_count": as_int(row.get("trade_count")),
                "worst_month": row.get("worst_month") or summary.get("worst_month_floor"),
                "worst_month_net": as_float(row.get("worst_month_net")),
                "weakest_slice": weak_slice_for(alias, negative_rows),
                "decision_label": label,
                "next_use": next_use,
                "why": why,
                "risk_boundary": "research_only_no_selection_no_onnx(연구 전용, 선택/ONNX 아님)",
                "reopen_condition": "needs multi-period curve and feature-reliance evidence before stronger status(더 강한 상태 전 다기간 곡선과 피처 의존 근거 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return decisions


def materialization_queue() -> list[dict[str, Any]]:
    common_controls = (
        "US100 M5, FPMarkets symbol contract(브로커 심볼 계약), same EA, same cost/spread, "
        "same model bundle and feature order(같은 모델 번들/피처 순서)"
    )
    return [
        {
            "queue_id": "cu_q01_balanced_pair_cross_period_pressure",
            "priority": "P0",
            "workstream": "state_phase_cross_period_reconfirmation(상태 국면 확장 기간 재확인)",
            "candidate_aliases": "s264_aih;s264_aia",
            "feature_blueprint_scope": "cu_fb01_state_phase_cross_period_reconfirmation",
            "hypothesis": "s264_aih/s264_aia state_phase gains are not 2024-only and survive adjacent periods(인접 기간에서도 버틴다).",
            "decision_use": "keep or downgrade balanced watchlist(균형 관찰군 유지/하향)",
            "comparison_baseline": "run267CT state_phase_monday_replacement rows for s264_aih and s264_aia",
            "control_variables": common_controls,
            "changed_variables": "period window only: 2023H2, 2025H1, 2025H2",
            "sample_scope": "Tier A plus duplicate routed boundary; true Tier B fallback remains not claimed",
            "success_criteria": "PF>=1.35, trades>=250, DD<=22, worst_month_net>-180 in most adjacent periods",
            "failure_criteria": "negative net, DD>26, or worst_month_net<=-220 in any key adjacent period",
            "invalid_conditions": "missing MT5 report, parsed trade mismatch, stale tester profile, or feature order mismatch",
            "stop_conditions": "two adjacent-period failures downgrade the candidate instead of another repair loop",
            "evidence_plan": "MT5 KPI, trade list, curve diagnostics, time-slice KPI, parser checks, runtime parity receipt",
            "materialization_instruction": "Create 2 candidates x 3 periods x TA/RT attempts with unchanged state_phase profile.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cu_q02_s258_redzone_monday_dd_pressure",
            "priority": "P0_aggressive",
            "workstream": "redzone_monday_dd_pressure(위험 구역 월요일/DD 압박)",
            "candidate_aliases": "s258_stc",
            "feature_blueprint_scope": "cu_fb02_redzone_monday_dd_pressure",
            "hypothesis": "s258_stc redzone high net can retain profit while shrinking Monday/DD damage(월요일/DD 손상을 줄여도 수익 유지).",
            "decision_use": "stress challenger keep/prune(압박 도전자 유지/가지치기)",
            "comparison_baseline": "run267CT s258_stc redzone_stress_blast",
            "control_variables": common_controls,
            "changed_variables": "redzone stress, loss-shape cooldown, shock persistence; no literal Monday exclusion",
            "sample_scope": "2024 historical pressure plus optional adjacent-period smoke if materialization budget allows",
            "success_criteria": "net>1700, PF>=1.40, DD<=18, Monday net>-180, session_07_12 not worse",
            "failure_criteria": "Monday net<-220 or DD>22 while headline remains attractive",
            "invalid_conditions": "zero trade, stale runtime output, or missing report image/table",
            "stop_conditions": "one high-risk failure is enough to prune the redzone standalone selection path",
            "evidence_plan": "KPI, Monday/session slices, DD curve, trade quality, report image",
            "materialization_instruction": "Create limited redzone loss-shape pressure attempts; do not add a calendar ban.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cu_q03_control_guardrail_retest",
            "priority": "P1",
            "workstream": "control_guardrail_retest(대조/가드레일 재시험)",
            "candidate_aliases": "s264_lc;s262_lih;s258_stc",
            "feature_blueprint_scope": "cu_fb01_state_phase_cross_period_reconfirmation;cu_fb02_redzone_monday_dd_pressure",
            "hypothesis": "control and validation-heavy candidates explain whether top candidates are broad signal or isolated luck(상위 후보가 넓은 신호인지 비교).",
            "decision_use": "guardrail for racing rank, not candidate selection(경주 순위 가드레일, 선택 아님)",
            "comparison_baseline": "run267CT candidate summary and 2024 baseline rows",
            "control_variables": common_controls,
            "changed_variables": "reuse P0 surfaces without extra candidate-specific tuning",
            "sample_scope": "2024 and one adjacent-period control slice",
            "success_criteria": "controls do not outperform top candidates on both PF and DD after same pressure",
            "failure_criteria": "control candidates become clearly stronger and top candidates collapse",
            "invalid_conditions": "non-matching feature order or missing control output",
            "stop_conditions": "control dominance forces re-rank, not more filter stacking",
            "evidence_plan": "same KPI/table/curve parser as P0 queue",
            "materialization_instruction": "Materialize only the smallest guardrail subset after P0 attempts are defined.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cu_q04_aih_aggressive_supply_repair_or_prune",
            "priority": "P1",
            "workstream": "aih_aggressive_supply_repair_or_prune(s264_aih 공격 공급 수리/가지치기)",
            "candidate_aliases": "s264_aih",
            "feature_blueprint_scope": "cu_fb04_aggressive_supply_repair_or_prune",
            "hypothesis": "s264_aih aggressive high PF is useful only if trade supply expands without curve damage(공급 확대 후에도 곡선이 버틴다).",
            "decision_use": "bounded repair or prune(제한 수리 또는 가지치기)",
            "comparison_baseline": "run267CT s264_aih aggressive_shock_supply_expansion",
            "control_variables": common_controls,
            "changed_variables": "entry supply width and shock release, max two attempts",
            "sample_scope": "2024 historical pressure only until supply repair survives",
            "success_criteria": "trades>=320, net>1200, PF>=1.55, DD<=16",
            "failure_criteria": "supply increases but PF/net collapses or DD expands",
            "invalid_conditions": "trade parser mismatch or feature surface drift",
            "stop_conditions": "after two failed supply attempts, prune this branch",
            "evidence_plan": "trade count, PF, DD curve, Monday/month/session slices",
            "materialization_instruction": "Create at most two supply-expansion attempts and mark any extra tuning as out of scope.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cu_q05_explosive_shock_state_combo",
            "priority": "P0_aggressive",
            "workstream": "explosive_shock_state_combo(폭발형 충격-상태 조합)",
            "candidate_aliases": "s264_aih;s264_aia;s258_stc",
            "feature_blueprint_scope": "cu_fb03_explosive_shock_state_combo",
            "hypothesis": "A limited explosive combo can raise profit ceiling without only stacking defensive filters(방어 필터 누적 없이 수익 상단 확대).",
            "decision_use": "find or reject a high-ceiling branch(상단 높은 분기 발견/거절)",
            "comparison_baseline": "run267CT top three profile rows",
            "control_variables": common_controls,
            "changed_variables": "shock acceleration + state phase + redzone release interaction",
            "sample_scope": "2024 pressure first; adjacent period only if 2024 survives",
            "success_criteria": "net>2200, trades>=450, PF>=1.35, DD<=24, worst_month_net>-200",
            "failure_criteria": "DD>28, weak month deepens below -240, or profit comes from very thin trades",
            "invalid_conditions": "feature order drift, non-reproducible tester output, or missing chart/report",
            "stop_conditions": "one explosive failure is recorded as failure memory, not repaired for 3+ stages",
            "evidence_plan": "MT5 report, equity/balance graph, trade quality, weak-slice summary, parser checks",
            "materialization_instruction": "Create one limited explosive attempt per candidate; no calendar hard bans.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cu_q06_feature_reliance_ablation_replacement_audit",
            "priority": "P2",
            "workstream": "feature_reliance_ablation_replacement(피처 의존 제거/대체 감사)",
            "candidate_aliases": "s264_aih;s264_aia;s258_stc",
            "feature_blueprint_scope": "cu_fb01_state_phase_cross_period_reconfirmation;cu_fb03_explosive_shock_state_combo",
            "hypothesis": "Top clues should not collapse when state_phase or shock proxy is ablated/replaced(상위 단서가 단일 피처에만 붙지 않아야 한다).",
            "decision_use": "adapter worthiness gate seed(어댑터 가치 게이트 씨앗)",
            "comparison_baseline": "run267CT state_phase/redzone/aggressive rows",
            "control_variables": common_controls,
            "changed_variables": "remove or replace state_phase/shock proxy with similar market meaning",
            "sample_scope": "design seed only until P0 materialization finishes",
            "success_criteria": "ablation/replacement keeps positive net and does not destroy PF/DD shape",
            "failure_criteria": "complete collapse after one feature removal or similar replacement",
            "invalid_conditions": "feature mapping unknown or adapter feature order cannot be traced",
            "stop_conditions": "do not run this before P0 cross-period/redzone pressure evidence exists",
            "evidence_plan": "feature order receipt, score surface diff, MT5 KPI, curve/time-slice review",
            "materialization_instruction": "Hold as follow-up seed; materialize after P0/P1 pressure shows which candidate remains alive.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "cu_p01_no_literal_calendar_ban",
            "prune_label": "literal_calendar_ban_pruned(문자 그대로 달력 금지 가지치기)",
            "affected_scope": "Monday/session weak-slice repairs",
            "why_pruned": "run267CT shows Monday weakness, but calendar bans would hide the failure instead of explaining market state.",
            "reopen_condition": "Only reopen if non-calendar state features repeatedly fail and the claim is downgraded to diagnostic only.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cu_p02_no_s258_redzone_selection",
            "prune_label": "s258_redzone_selection_pruned(258 위험구역 즉시 선택 가지치기)",
            "affected_scope": "s258_stc redzone_stress_blast",
            "why_pruned": "Highest net remains paired with Monday net around -266.64 and needs DD/time-slice pressure first.",
            "reopen_condition": "Reopen if redzone Monday/DD pressure keeps net/PF while lifting weak slices.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cu_p03_no_aih_thin_supply_selection",
            "prune_label": "aih_thin_supply_selection_pruned(s264_aih 얇은 공급 즉시 선택 가지치기)",
            "affected_scope": "s264_aih aggressive_shock_supply_expansion",
            "why_pruned": "PF is high but trade_count=251 and net=831.95 are not enough for a strong package.",
            "reopen_condition": "Reopen only after bounded supply expansion reaches useful trade count without curve damage.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cu_p04_no_control_candidate_promotion_language",
            "prune_label": "control_candidate_status_pruned(대조 후보 지위 과장 가지치기)",
            "affected_scope": "s264_lc and s262_lih",
            "why_pruned": "They remain useful guardrails, but current CT evidence does not justify stronger candidate status.",
            "reopen_condition": "Reopen if guardrail retest beats top candidates on period stability, DD, and trade quality.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    monday_rows = [row for row in negative_rows if row.get("axis") == "weekday" and row.get("bucket") == "Monday"]
    month_rows = [row for row in negative_rows if row.get("axis") == "month"]
    session_rows = [row for row in negative_rows if row.get("axis") == "session_report"]
    deepest_monday = min((as_float(row.get("net_profit")) for row in monday_rows), default=0.0)
    deepest_month = min((as_float(row.get("net_profit")) for row in month_rows), default=0.0)
    deepest_session = min((as_float(row.get("net_profit")) for row in session_rows), default=0.0)
    return [
        {
            "memory_id": "cu_m01_monday_shared_weakness",
            "pattern": "Monday shared weakness(월요일 공유 약점)",
            "affected_scope": "all baseline candidates with strongest damage in s258/s264_lc/aih aggressive rows",
            "evidence": f"monday_rows={len(monday_rows)};deepest_monday_net={deepest_monday}",
            "why_fragile": "The weakness repeats across candidates, so it is probably state/regime-related instead of candidate-specific noise.",
            "do_not_repeat": "Do not add literal Monday-off filters as a shortcut.",
            "salvage_angle": "Use state phase, loss shape, and shock persistence replacements.",
            "reopen_condition": "Reopen only through non-calendar state evidence.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cu_m02_2024_06_12_month_holes",
            "pattern": "2024-06/2024-12 weak months(약한 월)",
            "affected_scope": "s264_lc, s258_stc, s264_aih, s264_aia, s262_lih",
            "evidence": f"month_negative_rows={len(month_rows)};deepest_month_net={deepest_month}",
            "why_fragile": "Headline annual net hides month-level holes.",
            "do_not_repeat": "Do not use annual KPI alone for candidate selection.",
            "salvage_angle": "Cross-period reconfirmation and monthly curve zoom.",
            "reopen_condition": "Reopen when adjacent periods show the same month pattern is not structural.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cu_m03_session_07_12_fragility",
            "pattern": "session_07_12 report-time fragility(보고 시간 기준 07-12 세션 취약)",
            "affected_scope": "s264_aih, s264_aia, s258_stc, s264_lc",
            "evidence": f"session_negative_rows={len(session_rows)};deepest_session_net={deepest_session}",
            "why_fragile": "Low trade-count session losses can distort curve quality even when headline KPI is strong.",
            "do_not_repeat": "Do not hide it behind total net.",
            "salvage_angle": "Inspect session slices after every aggressive attempt.",
            "reopen_condition": "Reopen if session loss disappears under non-calendar state replacement.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cu_m04_thin_supply_high_pf",
            "pattern": "high PF with thin supply(얇은 공급의 높은 PF)",
            "affected_scope": "s264_aih aggressive_shock_supply_expansion",
            "evidence": "trades=251;net=831.95;PF=1.7811",
            "why_fragile": "A small trade supply can look clean but fail package-level confidence.",
            "do_not_repeat": "Do not treat high PF alone as enough.",
            "salvage_angle": "Bounded supply expansion or prune after two attempts.",
            "reopen_condition": "Reopen if trade_count>=320 with PF/DD preserved.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def performance_attribution(source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(source_rows, start=1):
        alias = row.get("candidate_alias", "")
        test_id = row.get("test_id", "")
        observed = row.get("observed_change", "")
        weakest = row.get("weakest_slice", "")
        rows.append(
            {
                "attribution_id": f"cu_a{index:02d}_{alias}_{test_id}",
                "observed_change": observed,
                "comparison_baseline": "run267CT performance_attribution_summary and run267B 2024 baseline where available",
                "likely_drivers": row.get("likely_drivers")
                or "state phase, redzone stress, shock supply, or loss-shape interaction",
                "segment_checks": f"weakest_slice={weakest}; run267CT already includes month, weekday, session, hour, direction, chronology slices",
                "trade_shape": row.get("observed_change", ""),
                "alternative_explanations": "2024-specific regime fit, duplicated routed boundary, thin trade supply, or hidden month/session concentration",
                "attribution_confidence": "medium_low_until_cross_period(확장 기간 전 중하)",
                "next_probe": row.get("next_probe", "run267CV materialization and MT5 pressure"),
            }
        )
    return rows


def experiment_design_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"design_{row['queue_id']}",
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


def data_integrity_receipts(source_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "cu_data_source_run267CT",
            "data_source": rel(SOURCE_REVIEW_RESULT_PATH),
            "time_axis": "MT5 tester report time and parsed trade close time from run267CS reports",
            "sample_scope": f"trade_records={source_result.get('trade_record_count') or source_result.get('trade_records')};time_slice_rows={source_result.get('time_slice_row_count') or source_result.get('time_slice_rows')}",
            "missing_or_duplicate_check": "parser_errors=0 in run267CT; duplicate routed boundary is labeled, not claimed as true Tier B fallback",
            "feature_label_boundary": "run267CU is design only; no labels or feature values are recalculated here",
            "split_boundary": "2024 historical pressure source; adjacent periods are planned only",
            "leakage_risk": "low_for_design_only; must be rechecked during run267CV materialization",
            "data_hash_or_identity": f"source_review={rel(SOURCE_REVIEW_RESULT_PATH)}",
            "integrity_judgment": "usable_for_followup_design(후속 설계에 사용 가능)",
        }
    ]


def model_validation_receipts() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "cu_model_validation_boundary",
            "model_family": "existing Stage267 score/model surfaces; no new trained model in run267CU",
            "target_and_label": "unchanged from source candidates; design does not change labels",
            "split_method": "source evidence 2024; planned adjacent-period pressure",
            "selection_metric": "not a selection run; uses net/PF/DD/trades/worst-month for follow-up routing",
            "secondary_metrics": "balance/equity curve, time-slice KPI, trade quality, parser checks",
            "threshold_policy": "planned changed variables only; no operating threshold claimed",
            "overfit_risk": "medium until cross-period and ablation/replacement evidence exists",
            "calibration_risk": "not assessed in design; must be assessed before adapter/ONNX consideration",
            "comparison_baseline": "run267CT plus earlier Stage267 2024 baseline evidence",
            "validation_judgment": "design_only_no_candidate_selection(설계 전용, 후보 선택 아님)",
        }
    ]


def result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CU shared weakness follow-up/prune design(267CU 공유 약점 후속/가지치기 설계)",
            "evidence_available": "run267CT trade records, curve diagnostics, time-slice KPI, negative slices, attribution summary",
            "evidence_missing": "run267CV materialized attempts, MT5 execution, adjacent-period results, feature ablation/replacement outputs, adapter package",
            "judgment_label": JUDGMENT,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_condition": NEXT_ACTION,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_audit(queue_rows: Sequence[Mapping[str, Any]], prune_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_review_available",
            "status": "passed(통과)",
            "evidence": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267CU is grounded in run267CT, not memory.",
        },
        {
            "gate_id": "experiment_design_fields",
            "status": "passed(통과)",
            "evidence": f"queue_rows={len(queue_rows)}; each has hypothesis/control/changed/success/failure/evidence fields",
            "effect": "next materialization can be judged instead of just completed.",
        },
        {
            "gate_id": "aggressive_requirement",
            "status": "passed(통과)",
            "evidence": "cu_q05_explosive_shock_state_combo and cu_q02_s258_redzone_monday_dd_pressure",
            "effect": "keeps the research from becoming only defensive filter stacking.",
        },
        {
            "gate_id": "bounded_repair_loop",
            "status": "passed(통과)",
            "evidence": f"prune_rows={len(prune_rows)}; s264_aih aggressive supply capped at two attempts",
            "effect": "prevents a repair branch from dragging for 3+ stages.",
        },
        {
            "gate_id": "claim_boundary",
            "status": "passed(통과)",
            "evidence": "selected_candidate=none; selected_research_baseline=none; onnx_readiness=not_claimed; goal_achieve=not_claimed",
            "effect": "prevents headline KPI from becoming a stronger claim.",
        },
    ]


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = [
        ("stage267_run267CU_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Run267CU feature blueprint."),
        ("stage267_run267CU_branch_decisions", "branch_decisions", BRANCH_DECISION_PATH, "Run267CU branch decisions."),
        ("stage267_run267CU_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267CU materialization queue."),
        ("stage267_run267CU_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Run267CU prune matrix."),
        ("stage267_run267CU_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267CU failure memory."),
        ("stage267_run267CU_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267CU performance attribution."),
        ("stage267_run267CU_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267CU experiment design receipt."),
        ("stage267_run267CU_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267CU data integrity receipt."),
        ("stage267_run267CU_model_validation_receipt", "model_validation_receipt", MODEL_VALIDATION_RECEIPT_PATH, "Run267CU model validation receipt."),
        ("stage267_run267CU_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CU result judgment."),
        ("stage267_run267CU_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CU gate audit."),
        ("stage267_run267CU_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CU run manifest."),
        ("stage267_run267CU_lineage", "lineage", LINEAGE_PATH, "Run267CU lineage."),
        ("stage267_run267CU_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CU review result."),
        ("stage267_run267CU_report", "review_report", REPORT_PATH, "Run267CU report."),
    ]
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in artifacts
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267CU Shared Weakness Follow-up/Prune Design(267단계 267CU 공유 약점 후속/가지치기 설계)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- feature_blueprints(피처 청사진): `{result['feature_blueprint_count']}`",
        f"- branch_decisions(분기 판단): `{result['branch_decision_count']}`",
        f"- materialization_queue_rows(물질화 대기열 행): `{result['materialization_queue_count']}`",
        f"- prune_rows(가지치기 행): `{result['prune_count']}`",
        f"- failure_memory_rows(실패 기억 행): `{result['failure_memory_count']}`",
        f"- aggressive_queue_rows(공격형 대기열 행): `{result['aggressive_queue_count']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267CT(267CT 실행)는 좋은 숫자와 약점을 같이 보여줬다. run267CU(267CU 실행)는 그 결과를 바로 후보 선택으로 올리지 않고, 다음에 실제로 깨뜨려 볼 queue(대기열)로 바꾼다.",
        "",
        "핵심은 세 갈래다. 첫째, `s264_aih`와 `s264_aia`의 state_phase(상태 국면) 단서를 2023H2/2025H1/2025H2 같은 adjacent period(인접 기간)에서 다시 압박한다. 둘째, `s258_stc`의 redzone(위험 구역) 고수익이 Monday(월요일)과 DD(손실폭)를 견디는지 본다. 셋째, 방어 필터만 붙이지 않기 위해 폭발형 shock-state combo(충격-상태 조합)를 제한적으로 강행한다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | best_profile(최선 프로필) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | weakest(최약 구간) | decision(판단) |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in result["branch_decisions"]:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['best_profile']}` | {row['best_net_profit']} | "
            f"{row['best_profit_factor']} | {row['best_trade_count']} | {row['best_equity_drawdown_percent']} | "
            f"`{row['weakest_slice']}` | {row['decision_label']} |"
        )
    lines.extend(
        [
            "",
            "## Materialization Queue(물질화 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | success(성공 기준) |",
            "|---|---|---|---|---|",
        ]
    )
    for row in result["materialization_queue"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | "
            f"{row['workstream']} | {row['success_criteria']} |"
        )
    lines.extend(
        [
            "",
            "## Prune/Failure Memory(가지치기/실패 기억)",
            "",
            "| id(ID) | type(종류) | scope(범위) | read(판독) |",
            "|---|---|---|---|",
        ]
    )
    for row in result["prune_matrix"]:
        lines.append(f"| `{row['prune_id']}` | prune(가지치기) | {row['affected_scope']} | {row['why_pruned']} |")
    for row in result["failure_memory"]:
        lines.append(f"| `{row['memory_id']}` | memory(기억) | {row['affected_scope']} | {row['why_fragile']} |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run267CU(267CU 실행)는 follow-up/prune design(후속/가지치기 설계)이다. 후보 선택, 연구 기준 후보 선택, ONNX(ONNX) 준비, Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decisions(분기 판단): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(FEATURE_BLUEPRINT_PATH, result["feature_blueprint"], FEATURE_BLUEPRINT_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, result["branch_decisions"], BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"], MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, result["prune_matrix"], PRUNE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, result["performance_attribution"], PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], EXPERIMENT_DESIGN_COLUMNS)
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], DATA_INTEGRITY_COLUMNS)
    write_csv(MODEL_VALIDATION_RECEIPT_PATH, result["model_validation_receipt"], MODEL_VALIDATION_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, result["gate_audit"], GATE_AUDIT_COLUMNS)
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
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
            "registry_links": {
                "stage_ledger": rel(STAGE_LEDGER_PATH),
                "project_ledger": rel(PROJECT_LEDGER_PATH),
                "run_registry": rel(RUN_REGISTRY_PATH),
                "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            },
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"feature_blueprints={result['feature_blueprint_count']};"
        f"branch_decisions={result['branch_decision_count']};"
        f"materialization_queue={result['materialization_queue_count']};"
        f"aggressive_queue={result['aggressive_queue_count']};"
        f"next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CU_shared_weakness_breakout_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B run267CT review-derived design; true Tier B fallback not claimed",
        "scoreboard": "experiment_design_branch_decision_materialization_queue_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_shared_weakness_breakout_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_followup_or_prune_design",
        "tier_scope": "Tier A run267CT design; Tier B fallback remains outside claim",
        "kpi_scope": "experiment_design_feature_blueprint_queue_failure_memory",
        "scoreboard_lane": "shared_weakness_breakout_followup_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"feature_blueprints={result['feature_blueprint_count']};materialization_queue={result['materialization_queue_count']}",
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
        "- run267CU_shared_weakness_breakout_followup_or_prune_design"
        f"(267CU 공유 약점 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267CU_summary(267CU 요약): run267CT(267CT 실행)의 후보 선택 보류 상태를 "
        f"feature blueprint(피처 청사진) `{result['feature_blueprint_count']}`개, "
        f"materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개, "
        f"prune rows(가지치기 행) `{result['prune_count']}`개, "
        f"failure memory(실패 기억) `{result['failure_memory_count']}`개로 바꿨다. "
        "Effect(효과): state_phase(상태 국면) 확장 기간 압박, s258 redzone(위험 구역) 월요일/DD 압박, "
        "explosive shock-state combo(폭발형 충격-상태 조합)를 다음 물질화 대상으로 분리한다."
    )
    block = "\n".join(
        [
            "Run267CU(267CU 실행)는 run267CT(267CT 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): queue(대기열) `{result['materialization_queue_count']}`개 중 P0에는 balanced pair cross-period pressure(균형 쌍 확장 기간 압박), s258 redzone Monday/DD pressure(위험 구역 월요일/DD 압박), explosive shock-state combo(폭발형 충격-상태 조합)를 둔다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_followup_or_prune_design`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review", summary_line)
            text = append_block_once(text, "Run267CU(267CU 실행)는 run267CT", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review", report_line)
            text = append_block_once(text, "Run267CU(267CU 실행)는 run267CT", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review", report_line)
            text = append_block_once(text, "Run267CU(267CU 실행)는 run267CT", block)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CU(267CU 실행) shared weakness breakout follow-up/prune design"
        f"(공유 약점 돌파 후속/가지치기 설계) `{STATUS}`. Effect(효과): run267CT(267CT 실행)의 "
        f"candidate/profile(후보/프로필) 근거를 materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개와 "
        f"prune matrix(가지치기 행렬) `{result['prune_count']}`개로 바꿨고, explosive shock-state combo(폭발형 충격-상태 조합)를 포함했다. "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_line)
    workspace = workspace.replace(f"  next_action: {source_review.NEXT_ACTION}", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CT_shared_weakness_breakout_followup_balance_timeslice_trade_quality_review_report_path",
        f"  run267CU_shared_weakness_breakout_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_PROFILE_PATH)
    summary_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    profile_axis_rows = read_csv(SOURCE_PROFILE_AXIS_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    attribution_source_rows = read_csv(SOURCE_ATTRIBUTION_PATH)
    features = feature_blueprints()
    decisions = make_branch_decisions(candidate_rows, summary_rows, negative_rows)
    queue_rows = materialization_queue()
    prune_rows = prune_matrix()
    memory_rows = failure_memory(negative_rows)
    attribution_rows = performance_attribution(attribution_source_rows)
    design_rows = experiment_design_receipts(queue_rows)
    data_rows = data_integrity_receipts(source_result)
    model_rows = model_validation_receipts()
    judgment_rows = result_judgment()
    gates = gate_audit(queue_rows, prune_rows)
    outputs = {
        "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
        "branch_decisions": rel(BRANCH_DECISION_PATH),
        "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
        "prune_matrix": rel(PRUNE_MATRIX_PATH),
        "failure_memory": rel(FAILURE_MEMORY_PATH),
        "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
        "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
        "model_validation_receipt": rel(MODEL_VALIDATION_RECEIPT_PATH),
        "result_judgment": rel(RESULT_JUDGMENT_PATH),
        "gate_audit": rel(GATE_AUDIT_PATH),
        "run_manifest": rel(RUN_MANIFEST_PATH),
        "lineage": rel(LINEAGE_PATH),
        "review_result": rel(REVIEW_RESULT_PATH),
        "report": rel(REPORT_PATH),
    }
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_status": source_result.get("status"),
        "source_candidate_profile_rows": len(candidate_rows),
        "source_profile_axis_rows": len(profile_axis_rows),
        "source_negative_slices": len(negative_rows),
        "feature_blueprint_count": len(features),
        "branch_decision_count": len(decisions),
        "materialization_queue_count": len(queue_rows),
        "aggressive_queue_count": sum(1 for row in queue_rows if "aggressive" in str(row.get("priority")).lower() or "explosive" in str(row.get("workstream")).lower()),
        "prune_count": len(prune_rows),
        "failure_memory_count": len(memory_rows),
        "feature_blueprint": features,
        "branch_decisions": decisions,
        "materialization_queue": queue_rows,
        "prune_matrix": prune_rows,
        "failure_memory": memory_rows,
        "performance_attribution": attribution_rows,
        "experiment_design_receipt": design_rows,
        "data_integrity_receipt": data_rows,
        "model_validation_receipt": model_rows,
        "result_judgment": judgment_rows,
        "gate_audit": gates,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "run267CT_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267CT_candidate_profile": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "run267CT_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "run267CT_profile_axis": rel(SOURCE_PROFILE_AXIS_PATH),
            "run267CT_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "run267CT_attribution": rel(SOURCE_ATTRIBUTION_PATH),
            "run267CT_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": outputs,
    }


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers_and_artifacts(str(result["created_at_utc"]), result)
    update_current_docs(result)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "feature_blueprints": result["feature_blueprint_count"],
                "branch_decisions": result["branch_decision_count"],
                "materialization_queue": result["materialization_queue_count"],
                "aggressive_queue": result["aggressive_queue_count"],
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
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
