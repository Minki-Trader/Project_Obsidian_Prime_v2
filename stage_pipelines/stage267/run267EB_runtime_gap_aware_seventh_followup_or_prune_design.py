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
    run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267EB"
RUN_ID = "run267EB_stage267_runtime_gap_aware_seventh_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267EB_runtime_gap_aware_seventh_followup_or_prune_design_completed"
JUDGMENT = "runtime_gap_aware_seventh_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267EC_materialize_runtime_gap_aware_seventh_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_seventh_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_ATTRIBUTION_PATH = source_review.ATTRIBUTION_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

FEATURE_BLUEPRINT_PATH = RUN_ROOT / "feature_blueprint.csv"
BRANCH_DECISION_PATH = RUN_ROOT / "branch_decision_matrix.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
EVIDENCE_MAP_PATH = RUN_ROOT / "evidence_map.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267EB_runtime_gap_aware_seventh_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267EB_runtime_gap_aware_seventh_followup_or_prune_design.py")

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
    "candidate_aliases",
    "candidate_ids",
    "branch_decision",
    "why",
    "next_use",
    "reopen_condition",
    "stop_condition",
    "claim_boundary",
)

MATERIALIZATION_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "candidate_aliases",
    "candidate_ids",
    "workstream",
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
    "runtime_instruction",
    "aggressive_or_defensive",
    "claim_boundary",
)

PRUNE_COLUMNS = (
    "prune_id",
    "affected_candidate_aliases",
    "affected_scope",
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

EVIDENCE_MAP_COLUMNS = (
    "evidence_id",
    "source_path",
    "source_field",
    "observed_value",
    "used_for",
    "effect",
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

GATE_AUDIT_COLUMNS = ("gate_id", "gate_name", "status", "evidence", "effect")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
        lines.insert(0, replacement)
    return "\n".join(lines) + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, current in enumerate(lines):
        if needle in current:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    lines.append(line)
    return "\n".join(lines) + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_stage267_field(text: str, field: str, replacement: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("stage267_baseline_candidate_racing_protocol:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            end = index
            break
    prefix = f"  {field}:"
    for index in range(start + 1, end):
        if lines[index].startswith(prefix):
            lines[index] = f"  {field}: {replacement}"
            return "\n".join(lines) + "\n"
    lines.insert(end, f"  {field}: {replacement}")
    return "\n".join(lines) + "\n"


def insert_stage267_report_path(text: str) -> str:
    line = f"  run267EB_runtime_gap_aware_seventh_followup_or_prune_design_report_path: {rel(REPORT_PATH)}"
    if line in text:
        return text
    lines = text.splitlines()
    try:
        start = lines.index("stage267_baseline_candidate_racing_protocol:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            end = index
            break
    for index in range(start + 1, end):
        if lines[index].startswith("  next_action:"):
            lines.insert(index, line)
            return "\n".join(lines) + "\n"
    lines.insert(end, line)
    return "\n".join(lines) + "\n"


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def profile_by_label(rows: Sequence[Mapping[str, str]], label: str) -> Mapping[str, str]:
    for row in rows:
        if row.get("profile_label") == label:
            return row
    return {}


def source_summary(profile_rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    s258_rows = [row for row in profile_rows if row.get("candidate_alias") == "s258_stc"]
    s264_aih_rows = [row for row in profile_rows if row.get("candidate_alias") == "s264_aih"]
    s264_lc_rows = [row for row in profile_rows if row.get("candidate_alias") == "s264_lc"]
    return {
        "profile_rows": len(profile_rows),
        "s258_rows": len(s258_rows),
        "s258_worst_dd": max((as_float(row.get("report_equity_drawdown_percent")) for row in s258_rows), default=0.0),
        "s258_2025h2_state_net": as_float(profile_by_label(profile_rows, "s258_stc_adverse_slice_state_2025h2").get("net_profit")),
        "s264_aih_final_month_net": as_float(profile_by_label(profile_rows, "s264_aih_202604_counter_shock_probe").get("net_profit")),
        "s264_lc_final_month_net": as_float(profile_by_label(profile_rows, "s264_lc_202604_same_month_control").get("net_profit")),
        "s264_aih_rows": len(s264_aih_rows),
        "s264_lc_rows": len(s264_lc_rows),
    }


def build_feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "eb_fb01_s258_period_survival_state_mix",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "feature_family": "period_survival_state_mix(기간 생존 상태 조합)",
            "market_meaning": "2023H2 강세가 2025H1/H2로 넘어갈 때 DD(손실폭)와 불리 상태가 같이 커지는지 본다.",
            "source_evidence": "run267EA: s258 2023H2 strong, 2025H1/H2 PF/DD uncomfortable.",
            "changed_variables": "period state score(기간 상태 점수), DD pressure rank(손실폭 압박 순위), adverse slice flag(불리 구간 표시)",
            "held_variables": "symbol=US100; timeframe=M5; MT5 tester contract; no calendar-only exclusion.",
            "aggressive_or_defensive": "diagnostic_defensive(진단형 방어)",
            "success_read": "2025H1/H2에서 PF/DD가 같이 덜 깨지고 거래 수가 얇아지지 않는다.",
            "failure_read": "2023H2만 예쁘고 2025H2 월/시간 구멍이 계속 깊으면 stress challenger(압박 도전자)만 유지한다.",
            "materialization_note": "run267EC에서 기간별 별도 attempt(시도)로 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "eb_fb02_s264_aih_final_month_market_state_rebuild",
            "candidate_aliases": "s264_aih;s264_lc",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control",
            "feature_family": "final_month_market_state_rebuild(마지막 달 시장 상태 재구축)",
            "market_meaning": "2026.04가 후보 단독 약점인지 시장 구간 약점인지 s264_lc control(대조)와 같이 분리한다.",
            "source_evidence": "run267EA: s264_aih 2026.04 net=-33.79; s264_lc 2026.04 net=-39.29.",
            "changed_variables": "counter-shock state bucket(역충격 상태 구간), direction shock balance(방향 충격 균형), final-month state handoff(마지막 달 상태 인계)",
            "held_variables": "same month scope(같은 달 범위), same cost assumptions(같은 비용 가정), no single-month rescue selection.",
            "aggressive_or_defensive": "repair_diagnostic(수리 진단)",
            "success_read": "s264_aih가 validation(검증)을 크게 손상하지 않고 2026.04 음수를 완화한다.",
            "failure_read": "s264_lc와 같이 깨지면 시장 구간 약점으로 기록하고 깊은 repair(수리)를 멈춘다.",
            "materialization_note": "repair cap(수리 제한) 안에서 1회 rebuild(재구축)만 허용한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "eb_fb03_pool_explosive_impulse_breakout",
            "candidate_aliases": "s258_stc;s264_aih",
            "candidate_ids": "s258_short_tight_control;s264_allow_inner_high_quarter",
            "feature_family": "explosive_impulse_breakout(폭발형 임펄스 돌파)",
            "market_meaning": "필터를 더 붙이지 않고 강한 방향/변동성 압축 해제 구간에서 수익 공급이 늘어나는지 본다.",
            "source_evidence": "user goal requires aggressive(공격적) experiment when defensive-only loop appears.",
            "changed_variables": "impulse expansion gate(임펄스 확장 게이트), ATR expansion rank(ATR 확장 순위), direction imbalance(방향 불균형)",
            "held_variables": "no hour/month hard ban(시간/월 하드 금지 없음), no ONNX(ONNX 없음), research-only boundary(연구 전용 경계).",
            "aggressive_or_defensive": "aggressive_explosive(공격형 폭발)",
            "success_read": "거래 수가 유지되면서 PF(수익 팩터)와 recovery(회복)가 같이 개선된다.",
            "failure_read": "DD(손실폭)가 더 깊어지거나 한두 거래로만 좋아 보이면 실패 기억으로 닫는다.",
            "materialization_note": "run267EC에서 적어도 2개 aggressive rows(공격형 행)를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "eb_fb04_pool_coverage_rejoin",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": "s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "feature_family": "pool_coverage_rejoin(후보군 커버리지 재합류)",
            "market_meaning": "run267DZ/EA에서 빠진 후보군 축을 다음 경주에서 다시 대조해 후보군 전체 균형을 맞춘다.",
            "source_evidence": "run267EA only reviewed s258_stc, s264_aih, s264_lc profiles.",
            "changed_variables": "none yet; materialization coverage restoration(물질화 커버리지 복원)",
            "held_variables": "same tester contract(같은 테스터 계약), no selection claim(선택 주장 없음).",
            "aggressive_or_defensive": "coverage_control(커버리지 대조)",
            "success_read": "누락 후보가 같은 약점 구간에서 더 덜 깨지는지 비교 가능해진다.",
            "failure_read": "자료/인계가 막히면 blocked(차단)로 기록하고 후보 선택 근거로 쓰지 않는다.",
            "materialization_note": "run267EC queue(대기열)에 s262_lih/s264_aia rejoin row(재합류 행)를 포함한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "eb_fb05_filter_stack_prune_guard",
            "candidate_aliases": "pool",
            "candidate_ids": "all_baseline_candidates",
            "feature_family": "filter_stack_prune_guard(필터 누적 가지치기 가드)",
            "market_meaning": "월/요일/시간 제외만 덕지덕지 붙이는 접근을 이번 설계에서 명시적으로 막는다.",
            "source_evidence": "run267EA boundary asks q06 filter-stack prune(필터 누적 가지치기)을 분리.",
            "changed_variables": "none; prune guard(가지치기 가드)",
            "held_variables": "all current candidate assumptions(현재 후보 가정 전체)",
            "aggressive_or_defensive": "prune_guard(가지치기 가드)",
            "success_read": "다음 물질화가 구조/상태/공급 실험으로 남고 단순 제외 필터로 퇴화하지 않는다.",
            "failure_read": "새 큐가 calendar-only filter(달력 전용 필터)만 늘리면 설계 실패다.",
            "materialization_note": "guard row(가드 행)로만 남기고 MT5 attempt(시도)는 만들지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_decisions(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "bd267eb_s258_period_survival_before_combine",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "branch_decision": "keep_as_stress_challenger_with_period_survival_gate(기간 생존 게이트 조건부 압박 도전자 유지)",
            "why": f"run267EA s258 worst DD={summary['s258_worst_dd']} and 2025H2 adverse net={summary['s258_2025h2_state_net']}; headline 2023H2 profit is not enough.",
            "next_use": "run267EC materializes 2025H1/H2 survival attempts before any combine.",
            "reopen_condition": "PF/DD and month/session holes improve across 2025H1/H2 without thin trade count.",
            "stop_condition": "If 2025H2 remains DD-heavy, keep only as stress memory(압박 기억).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267eb_s264_aih_one_rebuild_then_stop",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "branch_decision": "one_final_month_rebuild_then_prune_if_failed(마지막 달 1회 재구축 후 실패 시 가지치기)",
            "why": f"validation repair net exists, but final month net={summary['s264_aih_final_month_net']} remains negative.",
            "next_use": "run267EC materializes one counter-shock rebuild and compares with s264_lc control.",
            "reopen_condition": "2026.04 improves while validation anchor(검증 앵커) stays usable.",
            "stop_condition": "If same month still breaks, stop deep repair loop.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267eb_s264_lc_interpretation_control_only",
            "candidate_aliases": "s264_lc",
            "candidate_ids": "s264_lowrank_control",
            "branch_decision": "interpretation_control_only(해석 대조 전용)",
            "why": f"same-month control net={summary['s264_lc_final_month_net']} confirms 2026.04 may be a market slice issue.",
            "next_use": "Use as paired control(쌍 대조), not candidate selection.",
            "reopen_condition": "Only if paired final-month pressure shows stable defensive behavior across broader periods.",
            "stop_condition": "Do not promote control from one same-month slice.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267eb_missing_pool_axes_rejoin",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": "s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "branch_decision": "rejoin_as_pool_coverage_controls(후보군 커버리지 대조로 재합류)",
            "why": "run267EA profile rows do not cover s262_lih or s264_aia, so the baseline pool(기준 후보군) comparison would narrow unintentionally.",
            "next_use": "run267EC restores at least one coverage row for each missing axis.",
            "reopen_condition": "They show less breakage in weak slices than current s258/s264 probes.",
            "stop_condition": "If handoff or data supply is missing, mark blocked(차단) rather than infer weakness.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267eb_force_explosive_not_filter_loop",
            "candidate_aliases": "s258_stc;s264_aih",
            "candidate_ids": "s258_short_tight_control;s264_allow_inner_high_quarter",
            "branch_decision": "force_aggressive_impulse_probe(공격형 임펄스 탐침 강행)",
            "why": "The goal forbids only defensive filtering; at least one high-energy supply experiment must be tested.",
            "next_use": "run267EC includes aggressive/explosive(공격/폭발) rows without hour/month hard bans.",
            "reopen_condition": "If curve improves with enough trades and no hidden DD hole.",
            "stop_condition": "If DD or thin lucky trades dominate, record failure and do not micro-tune.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267eb_filter_stack_pruned",
            "candidate_aliases": "pool",
            "candidate_ids": "all_baseline_candidates",
            "branch_decision": "prune_calendar_hour_filter_stack(달력/시간 필터 누적 가지치기)",
            "why": "run267EA has many weak slices, but hiding them with exclusions would not prove structure.",
            "next_use": "Keep as guardrail row only.",
            "reopen_condition": "Only if tied to a market state feature, not a naked exclusion.",
            "stop_condition": "Any run267EC row that only bans month/day/hour should be held.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_materialization_queue() -> list[dict[str, Any]]:
    common_controls = "symbol=US100; timeframe=M5; spread/cost/tester contract fixed; no candidate selection claim."
    return [
        {
            "queue_id": "q01_s258_2025h1_period_survival_gate",
            "priority": "P0_survival_gate(P0 생존 게이트)",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "s258_period_survival",
            "source_evidence": "run267EA s258 2025H1 PF about 1.15-1.17 with DD up to 23.71.",
            "hypothesis": "A state-based survival gate(상태 기반 생존 게이트) can reduce DD without killing trade count.",
            "decision_use": "Decide whether s258 remains a stress challenger(압박 도전자) worth further Adapter(어댑터) work.",
            "comparison_baseline": "run267EA s258 2025H1 dd_shape/state rows.",
            "control_variables": common_controls,
            "changed_variables": "period survival score(기간 생존 점수), adverse-state rank(불리 상태 순위)",
            "sample_scope": "Tier A; 2025H1 validation post-2024.",
            "success_criteria": "PF improves, DD drops, trade count remains substantial, weak month/session not hidden.",
            "failure_criteria": "DD remains high or trade count becomes too thin.",
            "invalid_conditions": "Missing MT5 report, parser error, changed cost assumptions, or hidden calendar-only exclusion.",
            "stop_conditions": "If 2025H1 fails after this gate, stop s258 H1 repair loop.",
            "evidence_plan": "run_manifest, MT5 report, KPI summary, trade list, curve diagnostics, time-slice KPI.",
            "runtime_instruction": "Materialize as a distinct attempt(시도), not merged with 2025H2.",
            "aggressive_or_defensive": "diagnostic_defensive(진단형 방어)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_s258_2025h2_period_survival_gate",
            "priority": "P0_survival_gate(P0 생존 게이트)",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "s258_period_survival",
            "source_evidence": "run267EA s258 2025H2 month 2025-12 and Monday slices are negative.",
            "hypothesis": "The same survival state can reduce 2025H2 month/hour DD without overfiltering.",
            "decision_use": "Decide whether s258 can survive OOS followthrough(표본외 후속) pressure.",
            "comparison_baseline": "run267EA s258 2025H2 dd_shape/state rows.",
            "control_variables": common_controls,
            "changed_variables": "late-period survival score(후반 기간 생존 점수), DD pressure state(손실폭 압박 상태)",
            "sample_scope": "Tier A; 2025H2 OOS followthrough.",
            "success_criteria": "2025-12 and Monday damage shrink without suppressing normal trade supply.",
            "failure_criteria": "Month/hour hole persists or improvement is only thin supply.",
            "invalid_conditions": "Missing final report, malformed trade list, or hard-banned weak month.",
            "stop_conditions": "If 2025H2 fails, do not continue s258 DD-shape repair in this branch.",
            "evidence_plan": "MT5 report, candidate profile review, negative slice summary, failure memory update.",
            "runtime_instruction": "Run separately from q01 to avoid hiding period-specific weakness.",
            "aggressive_or_defensive": "diagnostic_defensive(진단형 방어)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s258_explosive_impulse_supply_probe",
            "priority": "P0_aggressive_explosive(P0 공격형 폭발)",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "explosive_supply",
            "source_evidence": "s258 has strong 2023H2 supply but weak later-period risk; defensive-only repair is not enough.",
            "hypothesis": "An impulse expansion feature(임펄스 확장 피처) can add strong trades rather than merely filtering weak ones.",
            "decision_use": "Check whether s258 has expansion value beyond tight control(타이트 대조).",
            "comparison_baseline": "run267EA s258 2023H2 strong rows and 2025H1/H2 weak rows.",
            "control_variables": common_controls,
            "changed_variables": "ATR expansion rank(ATR 확장 순위), direction impulse imbalance(방향 임펄스 불균형), no hour/month hard bans.",
            "sample_scope": "Tier A; 2023H2, 2025H1, 2025H2 split attempts if materialized.",
            "success_criteria": "More robust expectancy(기대값) and PF with enough trades; DD not worse than source rows.",
            "failure_criteria": "Explosive branch increases DD or wins only from a tiny trade count.",
            "invalid_conditions": "If the row silently adds calendar-only exclusions.",
            "stop_conditions": "One aggressive attempt set; no micro-threshold loop.",
            "evidence_plan": "run_manifest, feature receipt, MT5 KPI, curve diagnostics, time-slice KPI.",
            "runtime_instruction": "Aggressive row must remain visibly separate from defensive gates.",
            "aggressive_or_defensive": "aggressive_explosive(공격형 폭발)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_s264_aih_validation_anchor_integrity_check",
            "priority": "P1_validation_integrity(P1 검증 무결성)",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "workstream": "s264_aih_validation_anchor",
            "source_evidence": "run267EA validation anchor repair net=574.25 PF=1.23 trades=467 but weak slices remain.",
            "hypothesis": "Validation anchor(검증 앵커) can be preserved while final-month rebuild is tested separately.",
            "decision_use": "Prevent final-month repair from damaging validation surface.",
            "comparison_baseline": "run267EA s264_aih_validation_anchor_repair.",
            "control_variables": common_controls,
            "changed_variables": "validation anchor integrity receipt(검증 앵커 무결성 영수증)",
            "sample_scope": "Tier A; validation_is.",
            "success_criteria": "Validation remains positive with acceptable DD and no new weak slice concentration.",
            "failure_criteria": "Validation drops or weak session/hour damage deepens.",
            "invalid_conditions": "Feature order drift or missing validation report.",
            "stop_conditions": "If validation breaks, stop final-month repair branch.",
            "evidence_plan": "feature order receipt, MT5 validation report, curve/time-slice review.",
            "runtime_instruction": "Pair with q05 but keep separate report.",
            "aggressive_or_defensive": "defensive_integrity(방어형 무결성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q05_s264_aih_202604_counter_shock_rebuild",
            "priority": "P0_repair_cap(P0 수리 제한)",
            "candidate_aliases": "s264_aih;s264_lc",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control",
            "workstream": "s264_aih_final_month_rebuild",
            "source_evidence": "run267EA s264_aih 2026.04 net=-33.79 and s264_lc same month net=-39.29.",
            "hypothesis": "A market-state rebuild(시장 상태 재구축) can separate candidate weakness from month-slice weakness.",
            "decision_use": "Decide whether s264_aih final-month hole is salvageable within repair cap.",
            "comparison_baseline": "run267EA s264_aih and s264_lc 2026.04 rows.",
            "control_variables": common_controls,
            "changed_variables": "counter-shock state(역충격 상태), sell-side damage control(매도 손상 제어), no one-month selection.",
            "sample_scope": "Tier A; 2026-04 final month plus paired validation check.",
            "success_criteria": "Final month loss improves and s264_lc control explains whether this is market-wide.",
            "failure_criteria": "Both s264_aih and control remain negative or validation breaks.",
            "invalid_conditions": "Same-month report missing, control omitted, or hidden spread/cost drift.",
            "stop_conditions": "After this one rebuild, prune branch if final-month remains broken.",
            "evidence_plan": "paired MT5 reports, control receipt, negative slice summary, failure memory.",
            "runtime_instruction": "One rebuild only; do not extend to a third repair stage.",
            "aggressive_or_defensive": "bounded_repair(제한 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q06_s264_aih_explosive_counter_impulse_probe",
            "priority": "P1_aggressive_explosive(P1 공격형 폭발)",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "workstream": "explosive_supply",
            "source_evidence": "s264_aih validation anchor is alive but final-month shock is negative.",
            "hypothesis": "A counter-impulse branch(역임펄스 분기) may add supply in shock state instead of filtering it away.",
            "decision_use": "Check whether s264_aih has aggressive expansion value or should be constrained to control role.",
            "comparison_baseline": "run267EA s264_aih validation and 2026.04 shock rows.",
            "control_variables": common_controls,
            "changed_variables": "counter-impulse expansion(역임펄스 확장), direction stress bucket(방향 압박 구간)",
            "sample_scope": "Tier A; validation_is and 2026-04 paired read.",
            "success_criteria": "Adds trades and improves expectancy without deepening final-month DD.",
            "failure_criteria": "Higher DD or final-month hole gets worse.",
            "invalid_conditions": "Aggressive row is actually a hidden exclusion filter.",
            "stop_conditions": "One aggressive pass; if weak, record and stop.",
            "evidence_plan": "MT5 report, trade count, equity curve, final-month slice, validation anchor check.",
            "runtime_instruction": "Must be labeled aggressive(공격형) in manifest.",
            "aggressive_or_defensive": "aggressive_explosive(공격형 폭발)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q07_s262_s264_aia_pool_coverage_rejoin",
            "priority": "P1_pool_coverage(P1 후보군 커버리지)",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": "s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "workstream": "pool_coverage_rejoin",
            "source_evidence": "run267EA did not profile s262_lih or s264_aia after run267DZ sixth follow-up.",
            "hypothesis": "Missing pool axes may be less fragile in weak slices and must rejoin before narrowing candidates.",
            "decision_use": "Restore candidate-pool comparison breadth.",
            "comparison_baseline": "Initial Stage267 pool roles and earlier Stage267 coverage rows.",
            "control_variables": common_controls,
            "changed_variables": "coverage restoration(커버리지 복원), no new tuning.",
            "sample_scope": "Tier A; same weak-slice windows used in run267EA where possible.",
            "success_criteria": "Produces comparable KPI and slice evidence for missing candidates.",
            "failure_criteria": "Supply or handoff is missing; then mark blocked not weak.",
            "invalid_conditions": "Different cost/model contract or missing feature order receipt.",
            "stop_conditions": "If coverage cannot be materialized, write blocked receipt before next repair.",
            "evidence_plan": "materialization receipts, run_manifest, MT5 KPI or blocked reason.",
            "runtime_instruction": "Coverage row is not a selection shortcut.",
            "aggressive_or_defensive": "coverage_control(커버리지 대조)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q08_filter_stack_prune_guard_hold",
            "priority": "P0_prune_guard(P0 가지치기 가드)",
            "candidate_aliases": "pool",
            "candidate_ids": "all_baseline_candidates",
            "workstream": "filter_stack_prune_guard",
            "source_evidence": "run267EA found 71 negative slices; filter-only response is explicitly disallowed.",
            "hypothesis": "No MT5 attempt should be created for naked month/day/hour exclusion.",
            "decision_use": "Hold filter-stack rows and keep next run structural.",
            "comparison_baseline": "run267EA negative_slice_summary.",
            "control_variables": common_controls,
            "changed_variables": "none; held prune row(보류 가지치기 행)",
            "sample_scope": "not_applicable_by_claim(주장 범위상 해당 없음)",
            "success_criteria": "Next materialization excludes naked filter-stack attempt.",
            "failure_criteria": "A calendar/hour-only row appears as materialized attempt.",
            "invalid_conditions": "Guard row is ignored by materialization.",
            "stop_conditions": "Always held until a market-state explanation exists.",
            "evidence_plan": "prune matrix and run267EC materialization audit.",
            "runtime_instruction": "Do not materialize as tester attempt.",
            "aggressive_or_defensive": "prune_guard(가지치기 가드)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "pr267eb_filter_only_calendar_hour_stack",
            "affected_candidate_aliases": "pool",
            "affected_scope": "month/day/hour hard exclusions",
            "prune_label": "filter_only_stack_pruned(필터 전용 누적 가지치기)",
            "why_pruned": "Weak slices must be explained by state/structure, not hidden by exclusions.",
            "salvage_value": "Can reappear only as a market-state feature(시장 상태 피처).",
            "reopen_condition": "State feature proves why the slice is structurally different.",
            "do_not_repeat": "Do not create naked month/day/hour bans.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267eb_s258_2023h2_headline_selection",
            "affected_candidate_aliases": "s258_stc",
            "affected_scope": "2023H2 strong rows",
            "prune_label": "headline_profit_selection_pruned(대표 수익 선택 가지치기)",
            "why_pruned": "2023H2 strength does not cover 2025H1/H2 PF/DD weakness.",
            "salvage_value": "Use as supply clue(공급 단서), not selected candidate.",
            "reopen_condition": "2025H1/H2 survival improves too.",
            "do_not_repeat": "Do not choose s258 from 2023H2 alone.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267eb_s264_one_month_rescue_selection",
            "affected_candidate_aliases": "s264_aih;s264_lc",
            "affected_scope": "2026.04 final month",
            "prune_label": "one_month_rescue_selection_pruned(한 달 구제 선택 가지치기)",
            "why_pruned": "A single final-month repair cannot justify candidate selection or ONNX review.",
            "salvage_value": "Use to classify market-slice weakness.",
            "reopen_condition": "Broad validation and OOS periods remain stable after rebuild.",
            "do_not_repeat": "Do not turn one-month improvement into selection.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267eb_deep_repair_loop_cap",
            "affected_candidate_aliases": "s264_aih;s258_stc",
            "affected_scope": "repeated repair branches",
            "prune_label": "repair_loop_cap_enforced(수리 루프 제한 적용)",
            "why_pruned": "The goal forbids dragging one repair branch beyond a short bounded loop.",
            "salvage_value": "Failure memory can guide a later rebuild from a different angle.",
            "reopen_condition": "New feature structure, not micro-threshold tuning.",
            "do_not_repeat": "No third-stage repair on the same threshold/filter axis.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267eb_onnx_before_adapter_runtime_evidence",
            "affected_candidate_aliases": "pool",
            "affected_scope": "ONNX parity(ONNX 동등성) and runtime reproduction(런타임 재현)",
            "prune_label": "onnx_before_evidence_pruned(근거 전 ONNX 가지치기)",
            "why_pruned": "No candidate has survived Adapter(어댑터), runtime reproduction(런타임 재현), and broader stability checks.",
            "salvage_value": "Keep parity requirements as later evidence gate.",
            "reopen_condition": "A candidate survives racing, Adapter, and runtime package checks.",
            "do_not_repeat": "Do not discuss ONNX conversion from a few good KPIs.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "mem267eb_s258_2025h2_dd_month_hole",
            "pattern": "s258 2025H2 DD/month hole(s258 2025H2 손실폭/월별 구멍)",
            "affected_scope": "s258_stc 2025H2",
            "why_failed": "PF is only around 1.10-1.15 while DD approaches or exceeds 22 percent and December is negative.",
            "salvage_value": "May still teach aggressive supply or stress challenger behavior.",
            "reopen_condition": "Period survival gate reduces DD without thin trades.",
            "do_not_repeat": "Do not combine 2023H2 profit with 2025H2 as if stable.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "mem267eb_s258_2025h1_adverse_state_dd",
            "pattern": "s258 2025H1 adverse state DD(s258 2025H1 불리 상태 손실폭)",
            "affected_scope": "s258_stc 2025H1",
            "why_failed": "Adverse-state row has uncomfortable DD and weak May/Tuesday/session slices.",
            "salvage_value": "Useful as state-feature design input.",
            "reopen_condition": "State mix improves May/session without calendar-only exclusion.",
            "do_not_repeat": "No more May-only hard ban.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "mem267eb_s264_aih_final_month_break",
            "pattern": "s264_aih final-month break(s264_aih 마지막 달 붕괴)",
            "affected_scope": "s264_aih 2026.04",
            "why_failed": f"run267EA final month net={summary['s264_aih_final_month_net']} with thin 17 trades.",
            "salvage_value": "May identify market shock state if paired with s264_lc.",
            "reopen_condition": "Counter-shock rebuild improves final month and keeps validation anchor.",
            "do_not_repeat": "Do not run more than one rebuild before prune.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "mem267eb_s264_lc_same_month_negative_control",
            "pattern": "s264_lc same-month negative control(s264_lc 같은 달 음수 대조)",
            "affected_scope": "s264_lc 2026.04",
            "why_failed": f"control net={summary['s264_lc_final_month_net']} in the same month.",
            "salvage_value": "Interprets whether 2026.04 is market-wide weak slice.",
            "reopen_condition": "Broader control periods show defensive stability.",
            "do_not_repeat": "Do not use same-month control as safe candidate.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "mem267eb_missing_pool_axes",
            "pattern": "missing candidate pool axes(누락 후보군 축)",
            "affected_scope": "s262_lih;s264_aia",
            "why_failed": "run267EA did not include these pool roles, so narrowing would be premature.",
            "salvage_value": "Rejoin as coverage controls.",
            "reopen_condition": "run267EC materializes comparable rows or records blocked reason.",
            "do_not_repeat": "Do not silently drop baseline pool members.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "mem267eb_filter_stack_guard",
            "pattern": "filter stack temptation(필터 누적 유혹)",
            "affected_scope": "pool",
            "why_failed": "71 negative slices could tempt naked filters, but that would not prove structure.",
            "salvage_value": "Use slices to build state features.",
            "reopen_condition": "Only with market-state explanation.",
            "do_not_repeat": "No filter-only repair branch.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_experiment_designs() -> list[dict[str, Any]]:
    return [
        {
            "design_id": "ed267eb_runtime_gap_aware_seventh_followup_or_prune",
            "hypothesis": "The next useful step is not candidate selection, but separating period survival, final-month market state, aggressive supply, missing pool coverage, and filter-stack pruning.",
            "decision_use": "Decide what run267EC should materialize and what should be held/pruned.",
            "comparison_baseline": "run267EA candidate_profile_review, negative_slice_summary, and attribution summary.",
            "control_variables": "US100 M5, same tester/cost contract, same candidate pool boundary, no ONNX claim.",
            "changed_variables": "period survival states, counter-shock rebuild, explosive impulse supply, pool coverage restoration.",
            "sample_scope": "Design-only from MT5 reviewed Tier A rows; next run must create materialized attempts.",
            "success_criteria": "Queue contains bounded repair, aggressive rows, pool coverage, and explicit prune guards.",
            "failure_criteria": "Queue collapses into filter-only micro tuning or silently drops pool members.",
            "invalid_conditions": "Source run267EA artifacts missing or parser errors not accounted for.",
            "stop_conditions": "One bounded repair pass for s264_aih final month; one aggressive pass before failure memory.",
            "evidence_plan": "feature_blueprint, branch_decision_matrix, materialization_queue, prune_matrix, failure_memory, gate_audit, lineage.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_evidence_map(
    profile_rows: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
    attribution_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = [
        {
            "evidence_id": "ev267eb_source_profile_rows",
            "source_path": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_field": "row_count",
            "observed_value": len(profile_rows),
            "used_for": "confirm run267EA reviewed 9 candidate profiles.",
            "effect": "Prevents selecting from partial headline metrics.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267eb_source_negative_slices",
            "source_path": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_field": "row_count",
            "observed_value": len(negative_rows),
            "used_for": "drive failure memory and anti-filter-stack guard.",
            "effect": "Weak slices become design evidence, not hidden exclusions.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267eb_source_attribution",
            "source_path": rel(SOURCE_ATTRIBUTION_PATH),
            "source_field": "row_count",
            "observed_value": len(attribution_rows),
            "used_for": "separate s258, s264_aih, and s264_lc next probes.",
            "effect": "Keeps repair branches separate instead of merging them.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for label in (
        "s258_stc_adverse_slice_state_2025h2",
        "s264_aih_202604_counter_shock_probe",
        "s264_lc_202604_same_month_control",
    ):
        row = profile_by_label(profile_rows, label)
        if row:
            evidence.append(
                {
                    "evidence_id": f"ev267eb_{label}",
                    "source_path": rel(SOURCE_CANDIDATE_PROFILE_PATH),
                    "source_field": "net_profit;profit_factor;drawdown;trade_count",
                    "observed_value": f"net={row.get('net_profit')};PF={row.get('profit_factor')};DD={row.get('report_equity_drawdown_percent')};trades={row.get('trade_count')}",
                    "used_for": "branch decision and failure memory.",
                    "effect": "Turns a profile row into explicit next-run design logic.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return evidence


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267EB runtime gap aware seventh follow-up/prune design(267EB 런타임 공백 반영 7차 후속/가지치기 설계)",
            "evidence_available": "run267EA reviewed MT5 outputs, candidate profile, negative slices, attribution; run267EB design artifacts.",
            "evidence_missing": "No run267EC materialization yet, no new MT5 KPI, no Adapter runtime package, no ONNX parity.",
            "judgment_label": "exploratory_design_completed(탐색 설계 완료)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run267EC must materialize queue rows and preserve prune guards before MT5 execution.",
            "user_explanation_hook": "이번 단계는 후보 선택이 아니라, 약한 후보를 계속 붙잡을지 버릴지 가르는 다음 실험 설계다.",
        }
    ]


def build_gate_audit(
    queue_rows: Sequence[Mapping[str, Any]],
    prune_rows: Sequence[Mapping[str, Any]],
    memory_rows: Sequence[Mapping[str, Any]],
    profile_rows: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    aggressive_count = sum("aggressive" in str(row.get("aggressive_or_defensive", "")) for row in queue_rows)
    coverage_ok = any("s262_lih" in str(row.get("candidate_aliases", "")) and "s264_aia" in str(row.get("candidate_aliases", "")) for row in queue_rows)
    filter_pruned = any("filter" in str(row.get("prune_id", "")) for row in prune_rows)
    return [
        {
            "gate_id": "gate267eb_source_artifacts",
            "gate_name": "source artifacts available(원천 산출물 사용 가능)",
            "status": "passed" if profile_rows and negative_rows else "failed",
            "evidence": f"profile_rows={len(profile_rows)};negative_slices={len(negative_rows)}",
            "effect": "Design is tied to reviewed evidence.",
        },
        {
            "gate_id": "gate267eb_aggressive_required",
            "gate_name": "aggressive rows present(공격형 행 존재)",
            "status": "passed" if aggressive_count >= 2 else "failed",
            "evidence": f"aggressive_rows={aggressive_count}",
            "effect": "Prevents defensive-only filter loop.",
        },
        {
            "gate_id": "gate267eb_pool_coverage",
            "gate_name": "missing pool axes rejoin(누락 후보군 축 재합류)",
            "status": "passed" if coverage_ok else "failed",
            "evidence": "s262_lih and s264_aia rejoin row present." if coverage_ok else "missing",
            "effect": "Keeps baseline candidate pool broad.",
        },
        {
            "gate_id": "gate267eb_filter_stack_prune",
            "gate_name": "filter stack pruned(필터 누적 가지치기)",
            "status": "passed" if filter_pruned else "failed",
            "evidence": f"prune_rows={len(prune_rows)}",
            "effect": "Weak slices are not hidden by naked exclusions.",
        },
        {
            "gate_id": "gate267eb_failure_memory",
            "gate_name": "failure memory recorded(실패 기억 기록)",
            "status": "passed" if len(memory_rows) >= 5 else "failed",
            "evidence": f"failure_memory={len(memory_rows)}",
            "effect": "Repeated weak directions have explicit stop/reopen conditions.",
        },
    ]


def build_run_manifest(created_at: str, queue_rows: Sequence[Mapping[str, Any]], prune_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "status": STATUS,
        "created_at_utc": created_at,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "candidate_profile_review": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "attribution_summary": rel(SOURCE_ATTRIBUTION_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
        },
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "queue_rows": len(queue_rows),
        "aggressive_rows": sum("aggressive" in str(row.get("aggressive_or_defensive", "")) for row in queue_rows),
        "prune_rows": len(prune_rows),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
    }


def build_lineage(created_at: str) -> dict[str, Any]:
    return {
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "created_at_utc": created_at,
        "source_inputs": [
            rel(SOURCE_REVIEW_RESULT_PATH),
            rel(SOURCE_CANDIDATE_PROFILE_PATH),
            rel(SOURCE_NEGATIVE_SLICE_PATH),
            rel(SOURCE_ATTRIBUTION_PATH),
            rel(SOURCE_REPORT_PATH),
        ],
        "producer": rel(PRODUCER_PATH),
        "outputs": [
            rel(FEATURE_BLUEPRINT_PATH),
            rel(BRANCH_DECISION_PATH),
            rel(MATERIALIZATION_QUEUE_PATH),
            rel(PRUNE_MATRIX_PATH),
            rel(FAILURE_MEMORY_PATH),
            rel(REPORT_PATH),
        ],
        "consumer": NEXT_ACTION,
        "availability": "tracked_after_commit(커밋 후 추적)",
        "boundary": "Design only; no new MT5 KPI or candidate selection.",
    }


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    profile_rows = read_csv_rows(SOURCE_CANDIDATE_PROFILE_PATH)
    negative_rows = read_csv_rows(SOURCE_NEGATIVE_SLICE_PATH)
    attribution_rows = read_csv_rows(SOURCE_ATTRIBUTION_PATH)
    summary = source_summary(profile_rows)
    feature_rows = build_feature_blueprints()
    branch_rows = build_branch_decisions(summary)
    queue_rows = build_materialization_queue()
    prune_rows = build_prune_matrix()
    memory_rows = build_failure_memory(summary)
    experiment_rows = build_experiment_designs()
    evidence_rows = build_evidence_map(profile_rows, negative_rows, attribution_rows)
    judgment_rows = build_result_judgment()
    gate_rows = build_gate_audit(queue_rows, prune_rows, memory_rows, profile_rows, negative_rows)
    aggressive_count = sum("aggressive" in str(row.get("aggressive_or_defensive", "")) for row in queue_rows)
    return {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "source_summary": summary,
        "feature_blueprint": feature_rows,
        "branch_decisions": branch_rows,
        "materialization_queue": queue_rows,
        "prune_matrix": prune_rows,
        "failure_memory": memory_rows,
        "experiment_design_receipt": experiment_rows,
        "evidence_map": evidence_rows,
        "result_judgment": judgment_rows,
        "gate_audit": gate_rows,
        "aggressive_queue_count": aggressive_count,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
            "branch_decisions": rel(BRANCH_DECISION_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "prune_matrix": rel(PRUNE_MATRIX_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "evidence_map": rel(EVIDENCE_MAP_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    queue_rows = list(result["materialization_queue"])
    branch_rows = list(result["branch_decisions"])
    prune_rows = list(result["prune_matrix"])
    memory_rows = list(result["failure_memory"])
    lines = [
        "# Stage267 Run267EB Seventh Follow-Up/Prune Design(267단계 267EB 7차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- feature_blueprints(피처 청사진): `{len(result['feature_blueprint'])}`",
        f"- branch_decisions(분기 판단): `{len(branch_rows)}`",
        f"- materialization_queue(물질화 대기열): `{len(queue_rows)}`",
        f"- aggressive_rows(공격형 행): `{result['aggressive_queue_count']}`",
        f"- prune_rows(가지치기 행): `{len(prune_rows)}`",
        f"- failure_memory(실패 기억): `{len(memory_rows)}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        f"- selected_candidate(선택 후보): `{result['selected_candidate']}`",
        f"- selected_research_baseline(선택 연구 기준 후보): `{result['selected_research_baseline']}`",
        f"- ONNX readiness(ONNX 준비): `{result['onnx_readiness']}`",
        f"- Goal Achieve(목표 달성): `{result['goal_achieve']}`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267EB(267EB 실행)는 후보를 고른 단계가 아니다. run267EA(267EA 실행)에서 보인 약점을 다음 materialization(물질화) 큐로 바꾼 설계 단계다.",
        "s258_stc는 2023H2 수익만 보고 밀지 않고 2025H1/H2 생존 조건을 먼저 본다. s264_aih는 2026.04 마지막 달 구멍을 한 번만 더 구조적으로 재검토하고, s264_lc는 해석 대조로만 둔다.",
        "또 s262_lih와 s264_aia는 이번 6차 실행 리뷰에 없었기 때문에 후보군 커버리지 차원에서 다시 불러온다. 필터를 더 붙이는 행은 prune guard(가지치기 가드)로 막고, aggressive/explosive(공격/폭발) 실험도 별도 행으로 강행한다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| decision(판단) | candidates(후보) | next(다음) |",
        "|---|---|---|",
    ]
    for row in branch_rows:
        lines.append(f"| `{row['decision_id']}` | `{row['candidate_aliases']}` | {row['next_use']} |")
    lines.extend(
        [
            "",
            "## Materialization Queue(물질화 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidates(후보) | mode(모드) |",
            "|---|---|---|---|",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | `{row['aggressive_or_defensive']}` |"
        )
    lines.extend(
        [
            "",
            "## Prune/Failure Boundary(가지치기/실패 경계)",
            "",
            "- headline profit selection(대표 수익 선택)은 금지한다.",
            "- one-month rescue selection(한 달 구제 선택)은 금지한다.",
            "- naked calendar/hour filter stack(달력/시간 필터 누적)은 가지치기한다.",
            "- one bounded repair(제한 수리 1회) 뒤에도 깨지면 실패 기억으로 닫는다.",
            "",
            "## Boundary(경계)",
            "",
            "- 이 설계는 exploratory design(탐색 설계)이며 후보 선택, 연구 기준 후보 선택, ONNX(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            "- 다음 run267EC(267EC 실행)는 materialization_queue(물질화 대기열)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿔야 한다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    items = [
        ("stage267_run267EB_producer", "producer_script", PRODUCER_PATH, "Builds run267EB seventh follow-up/prune design."),
        ("stage267_run267EB_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267EA review result."),
        ("stage267_run267EB_source_profile", "source_candidate_profile", SOURCE_CANDIDATE_PROFILE_PATH, "Source candidate profile review."),
        ("stage267_run267EB_source_negative_slices", "source_negative_slices", SOURCE_NEGATIVE_SLICE_PATH, "Source negative slice summary."),
        ("stage267_run267EB_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Feature blueprint for next materialization."),
        ("stage267_run267EB_branch_decisions", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decisions."),
        ("stage267_run267EB_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Next materialization queue."),
        ("stage267_run267EB_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune and stop-loop matrix."),
        ("stage267_run267EB_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267EB_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267EB_evidence_map", "evidence_map", EVIDENCE_MAP_PATH, "Evidence map."),
        ("stage267_run267EB_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267EB_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267EB_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267EB_lineage", "lineage", LINEAGE_PATH, "Artifact lineage."),
        ("stage267_run267EB_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267EB_report", "review_report", REPORT_PATH, "User-facing design report."),
    ]
    rows = []
    for artifact_id, artifact_type, path, notes in items:
        if path_exists(Path(path)):
            digest = sha256_file_lf_normalized(Path(path))
        else:
            digest = "missing"
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": digest,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    notes = (
        f"queue_rows={len(result['materialization_queue'])};"
        f"aggressive_rows={result['aggressive_queue_count']};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"next_action={NEXT_ACTION}."
    )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_seventh_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267EB_runtime_gap_aware_seventh_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_seventh_followup_or_prune_design",
        "tier_scope": "design only from run267EA Tier A reviewed rows",
        "scoreboard": "experiment_design_queue_prune_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_seventh_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_seventh_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_seventh_followup_or_prune_design",
        "tier_scope": "design only; next run materializes Tier A attempts",
        "kpi_scope": "experiment_design_queue_prune_failure_memory",
        "scoreboard_lane": "runtime_gap_aware_seventh_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={len(result['materialization_queue'])};aggressive_rows={result['aggressive_queue_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}. Design enforces pool coverage, aggressive rows, and filter-stack prune guard.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(str(result["created_at_utc"])), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267EB_runtime_gap_aware_seventh_followup_or_prune_design"
        f"(267EB 런타임 공백 반영 7차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_block = (
        "Run267EB(267EB 실행)는 run267EA(267EA 실행)의 후보 프로필/음수 구간/성과 귀속 근거를 7차 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.\n"
        f"Effect(효과): materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, aggressive/explosive rows(공격/폭발 행) `{result['aggressive_queue_count']}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개, failure memory(실패 기억) `{len(result['failure_memory'])}`개를 만들었다.\n"
        "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다."
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_seventh_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "stage267_run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review.md", report_line)
    current = append_block_once(current, "Run267EB(267EB 실행)는 run267EA", summary_block)
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review", report_line)
    selection = append_block_once(selection, "Run267EB(267EB 실행)는 run267EA", summary_block)
    write_text(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = append_after_contains(review_index, "Run267EA(267EA 실행)는", summary_block)
    write_text(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus_entry = (
        "current_focus:\n"
        "- >-\n"
        "  Stage267(267단계) run267EB(267EB 실행) runtime gap aware seventh follow-up/prune design(런타임 공백 반영 7차 후속/가지치기 설계) "
        f"`{STATUS}`. Effect(효과): run267EA(267EA 실행)의 약점 근거를 materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, "
        f"aggressive/explosive rows(공격/폭발 행) `{result['aggressive_queue_count']}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage267(267단계) run267EB(267EB 실행)" not in workspace:
        workspace = workspace.replace("current_focus:\n", focus_entry, 1)
    workspace = replace_stage267_field(workspace, "status", STATUS)
    workspace = replace_stage267_field(workspace, "current_run_id", RUN_ID)
    workspace = replace_stage267_field(workspace, "last_completed_run_id", RUN_ID)
    workspace = insert_stage267_report_path(workspace)
    workspace = replace_stage267_field(workspace, "next_action", NEXT_ACTION)
    write_text(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(FEATURE_BLUEPRINT_PATH, result["feature_blueprint"], FEATURE_BLUEPRINT_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, result["branch_decisions"], BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"], MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, result["prune_matrix"], PRUNE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], EXPERIMENT_DESIGN_COLUMNS)
    write_csv(EVIDENCE_MAP_PATH, result["evidence_map"], EVIDENCE_MAP_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, result["gate_audit"], GATE_AUDIT_COLUMNS)
    write_json(RUN_MANIFEST_PATH, build_run_manifest(str(result["created_at_utc"]), result["materialization_queue"], result["prune_matrix"]))
    write_json(LINEAGE_PATH, build_lineage(str(result["created_at_utc"])))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_current_docs(result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "feature_blueprints": len(result["feature_blueprint"]),
                "branch_decisions": len(result["branch_decisions"]),
                "materialization_queue": len(result["materialization_queue"]),
                "aggressive_rows": result["aggressive_queue_count"],
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
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
