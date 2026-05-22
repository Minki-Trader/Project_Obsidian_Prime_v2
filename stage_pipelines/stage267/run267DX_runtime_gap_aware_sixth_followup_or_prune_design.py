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
    run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267DX"
RUN_ID = "run267DX_stage267_runtime_gap_aware_sixth_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267DX_runtime_gap_aware_sixth_followup_or_prune_design_completed"
JUDGMENT = "runtime_gap_aware_sixth_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267DY_materialize_runtime_gap_aware_sixth_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_sixth_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH = source_review.CANDIDATE_INIT_FAILURE_SUMMARY_PATH
SOURCE_ATTEMPT_OUTCOME_PATH = source_review.ATTEMPT_OUTCOME_REVIEW_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
BRANCH_DECISION_PATH = RUN_ROOT / "branch_decision_matrix.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
EVIDENCE_MAP_PATH = RUN_ROOT / "evidence_map.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DX_runtime_gap_aware_sixth_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DX_runtime_gap_aware_sixth_followup_or_prune_design.py")

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

QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "candidate_aliases",
    "candidate_ids",
    "candidate_role",
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
    "materialization_boundary",
    "aggressive_or_defensive",
    "claim_boundary",
)

BRANCH_COLUMNS = (
    "decision_id",
    "candidate_alias",
    "candidate_id",
    "branch_decision",
    "why",
    "next_use",
    "reopen_condition",
    "stop_condition",
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


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def source_counts() -> dict[str, int]:
    return {
        "candidate_profile_rows": len(read_csv_rows(SOURCE_CANDIDATE_PROFILE_PATH)),
        "candidate_summary_rows": len(read_csv_rows(SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH)),
        "attempt_rows": len(read_csv_rows(SOURCE_ATTEMPT_OUTCOME_PATH)),
        "negative_slice_rows": len(read_csv_rows(SOURCE_NEGATIVE_SLICE_PATH)),
        "curve_rows": len(read_csv_rows(SOURCE_CURVE_DIAGNOSTICS_PATH)),
    }


def build_materialization_queue() -> list[dict[str, Any]]:
    fixed_controls = (
        "symbol=FPMarkets US100; timeframe=M5; source_run=run267DW; "
        "same cost/spread assumptions; selected_candidate=none"
    )
    return [
        {
            "queue_id": "q01_s258_stc_structural_dd_shape_split",
            "priority": "P0",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "candidate_role": "stress challenger(압박 도전자)",
            "workstream": "structural_dd_shape_split(구조적 손실폭 형태 분리)",
            "source_evidence": "run267DW: avg net 658.825, avg PF 1.356823, max DD 26.32, worst completed month -136.08",
            "hypothesis": "s258_stc(258 STC 후보)의 수익은 살아 있지만 DD(drawdown, 손실폭)가 구조 문제인지, 단순 약한 시간대 문제인지 분리한다.",
            "decision_use": "Adapter(어댑터)로 확장할 가치가 있는 stress challenger(압박 도전자)인지 판단한다.",
            "comparison_baseline": "run267DW s258_stc table handoff repair(테이블 인계 수리)와 noncalendar impulse(비달력 충격) 완료 프로필",
            "control_variables": fixed_controls,
            "changed_variables": "risk shape(위험 형태), adverse excursion(불리한 진행), impulse/route split(충격/경로 분리)",
            "sample_scope": "2023H2, 2025H1, 2025H2 Tier A(티어 A) adjacent pressure slices(인접 압박 구간)",
            "success_criteria": "net profit(순수익)과 trade count(거래 수)를 보존하면서 2025H1/H2 DD와 recovery(회복)가 개선된다.",
            "failure_criteria": "수익이 약해지거나 DD가 24%대 이상으로 남거나 약한 월이 단순 이동만 한다.",
            "invalid_conditions": "MT5(MetaTrader 5, 메타트레이더5) runtime output(런타임 출력) 누락, zero trade(무거래), feature order(피처 순서) 불명",
            "stop_conditions": "한 번의 물질화/검토 뒤 구조 개선이 없으면 s258_stc는 stress-only(압박 전용) 보류로 낮춘다.",
            "evidence_plan": "MT5 report(보고서), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), month/weekday/hour/session KPI(월/요일/시간/세션 지표)",
            "runtime_instruction": "materialize structural variants(구조 변형 물질화); avoid hour-only exclusion(시간만 제외 금지)",
            "materialization_boundary": "materialize in run267DY; no candidate selection(후보 선택 없음)",
            "aggressive_or_defensive": "aggressive_structural(공격형 구조)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_s258_stc_adverse_slice_falsification",
            "priority": "P0",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "candidate_role": "stress challenger(압박 도전자)",
            "workstream": "adverse_slice_falsification(불리 구간 반증)",
            "source_evidence": "run267DW weak slices: hour16 -699.43, Monday -184.02, 2025-12 -136.08",
            "hypothesis": "약한 구간이 달력 필터 문제가 아니라 impulse quality(충격 품질) 또는 route state(경로 상태) 문제인지 반증한다.",
            "decision_use": "s258_stc를 계속 살릴지, 약점이 너무 국소적이고 위험한 후보인지 가른다.",
            "comparison_baseline": "run267DW weakest slice watch(약한 구간 관찰) 상위 음수 구간",
            "control_variables": fixed_controls,
            "changed_variables": "noncalendar state features(비달력 상태 피처), impulse quality(충격 품질), route state(경로 상태)",
            "sample_scope": "hour16, Monday, 2025-12, adjacent 2025H1/H2, 2023H2",
            "success_criteria": "약한 구간 손실이 줄고 전체 거래 수가 과하게 줄지 않는다.",
            "failure_criteria": "약한 bucket(구간)을 제외할 때만 좋아지거나 다른 bucket(구간)으로 손실이 이동한다.",
            "invalid_conditions": "calendar-only ban(달력 전용 금지)으로만 성과가 개선된 경우",
            "stop_conditions": "단순 제외형 개선만 나오면 해당 repair(수리) 축은 prune(가지치기)한다.",
            "evidence_plan": "negative slice summary(음수 구간 요약), trade quality(거래 품질), curve diagnostics(곡선 진단)",
            "runtime_instruction": "materialize falsification variants(반증 변형 물질화) with structural state features(구조 상태 피처)",
            "materialization_boundary": "materialize in run267DY; no filter-stack-only variant(필터 누적 전용 변형 금지)",
            "aggressive_or_defensive": "aggressive_falsification(공격형 반증)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s264_aih_validation_anchor_one_repair",
            "priority": "P0",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "candidate_role": "core challenger(핵심 도전자)",
            "workstream": "validation_anchor_one_repair(검증 앵커 1회 수리)",
            "source_evidence": "run267DW: validation anchor init failure 1, ebm_table_open_failure 1, final month net -33.16",
            "hypothesis": "s264_aih(264 AIH 후보)의 validation anchor(검증 앵커)는 성능 실패 이전에 table handoff(테이블 인계)가 막혔을 수 있다.",
            "decision_use": "core challenger(핵심 도전자)를 한 번 더 시험할 수 있는지, 아니면 가지치기할지 결정한다.",
            "comparison_baseline": "run267DW s264_aih explosive shock probe(폭발형 충격 탐침)와 blocked validation anchor(차단된 검증 앵커)",
            "control_variables": fixed_controls,
            "changed_variables": "table path(테이블 경로), preflight open check(사전 열기 점검), validation anchor handoff(검증 앵커 인계)",
            "sample_scope": "validation anchor(검증 앵커) plus 2026.04 final OOS month(마지막 표본외 월)",
            "success_criteria": "init failure(초기화 실패)가 사라지고 2026.04가 음수 붕괴를 반복하지 않는다.",
            "failure_criteria": "init failure가 반복되거나 2026.04 final month(마지막 달)가 계속 음수다.",
            "invalid_conditions": "runtime telemetry(런타임 텔레메트리) 없이 zero trade(무거래)만 생긴 경우",
            "stop_conditions": "이번 repair(수리) 뒤에도 실패하면 s264_aih validation repair branch(검증 수리 분기)는 종료한다.",
            "evidence_plan": "preflight receipt(사전 점검 영수증), MT5 report(보고서), telemetry(텔레메트리), candidate profile(후보 프로필)",
            "runtime_instruction": "one repair only(1회 수리만); then prune if failure persists(실패 지속 시 가지치기)",
            "materialization_boundary": "materialize once in run267DY",
            "aggressive_or_defensive": "repair_gate(수리 게이트)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_s264_aih_counter_shock_final_month_probe",
            "priority": "P0",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "candidate_role": "core challenger(핵심 도전자)",
            "workstream": "counter_shock_final_month_probe(반대 충격 마지막 달 탐침)",
            "source_evidence": "run267DW: s264_aih 2026.04 explosive shock net -33.16, PF 0.553581, trades 17",
            "hypothesis": "final month(마지막 달) 음수가 shock-state(충격 상태) 정의 실패인지 반대 방향 탐침으로 확인한다.",
            "decision_use": "s264_aih의 공격형 clue(단서)를 유지할지, 2026.04 취약성으로 가지치기할지 판단한다.",
            "comparison_baseline": "run267DW s264_aih 202604 explosive shock probe(2026.04 폭발형 충격 탐침)",
            "control_variables": fixed_controls,
            "changed_variables": "counter shock gate(반대 충격 관문), threshold/risk shape(임계값/위험 형태), final-month state(마지막 달 상태)",
            "sample_scope": "2026.04 final OOS month(마지막 표본외 월) with validation anchor pairing(검증 앵커 쌍)",
            "success_criteria": "final month 음수가 구조적으로 줄고 validation anchor(검증 앵커)와 모순이 줄어든다.",
            "failure_criteria": "trade count(거래 수)가 너무 적거나 PF(수익 팩터)가 1 미만으로 남는다.",
            "invalid_conditions": "validation anchor repair(검증 앵커 수리) 없이 단독 성공처럼 보이는 경우",
            "stop_conditions": "counter shock(반대 충격)도 깨지면 s264_aih 공격형 충격 축은 failure memory(실패 기억)로 낮춘다.",
            "evidence_plan": "paired MT5 attempts(쌍 실행), profile review(프로필 검토), weak month read(약한 월 판독)",
            "runtime_instruction": "materialize as falsification probe(반증 탐침으로 물질화), not selection(선택 아님)",
            "materialization_boundary": "materialize in run267DY with q03 pair(q03 쌍)",
            "aggressive_or_defensive": "explosive_aggressive(폭발형 공격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q05_s264_lc_same_month_control_hold",
            "priority": "P1",
            "candidate_aliases": "s264_lc",
            "candidate_ids": "s264_lowrank_control",
            "candidate_role": "defensive control(방어 대조)",
            "workstream": "same_month_control_hold(같은 월 대조 보류)",
            "source_evidence": "run267DW: s264_lc 2026.04 net -39.29, PF 0.403975, trades 17",
            "hypothesis": "s264_lc(264 LC 후보)는 같은 월 방어 대조로만 의미가 있고 도전자 repair(수리) 대상은 아니다.",
            "decision_use": "q03/q04의 2026.04 결과가 시장 공통 약점인지 후보 고유 약점인지 비교한다.",
            "comparison_baseline": "run267DW s264_lc 202604 defensive control(방어 대조)",
            "control_variables": fixed_controls,
            "changed_variables": "none unless q03/q04 require paired control(쌍 대조가 필요할 때만)",
            "sample_scope": "2026.04 final OOS month(마지막 표본외 월)",
            "success_criteria": "q03/q04 해석에 필요한 same-month control(같은 월 대조)을 제공한다.",
            "failure_criteria": "standalone challenger(단독 도전자)처럼 쓰이기 시작한다.",
            "invalid_conditions": "control-only(대조 전용) 경계가 사라진 경우",
            "stop_conditions": "q03/q04가 실행되지 않으면 새 MT5(MetaTrader 5, 메타트레이더5) 시도는 생략한다.",
            "evidence_plan": "control comparison receipt(대조 비교 영수증)",
            "runtime_instruction": "hold unless paired control is needed(쌍 대조 필요 시에만 보류 해제)",
            "materialization_boundary": "conditional hold(조건부 보류)",
            "aggressive_or_defensive": "defensive_control(방어 대조)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q06_prune_micro_filter_stack",
            "priority": "P0_guardrail",
            "candidate_aliases": "s258_stc;s264_aih;s264_lc",
            "candidate_ids": "s258_short_tight_control;s264_allow_inner_high_quarter;s264_lowrank_control",
            "candidate_role": "guardrail(가드레일)",
            "workstream": "anti_micro_filter_stack(미세 필터 누적 방지)",
            "source_evidence": "run267DW weak slices are hour/weekday/month clustered, but goal forbids bottleneck micro-tuning(병목 미세 조정 금지)",
            "hypothesis": "hour-only(시간만), Monday-only(월요일만), month-only(월만) 제외는 후보 체질 개선이 아니다.",
            "decision_use": "run267DY materialization(물질화)에서 단순 제외형 변형을 막는다.",
            "comparison_baseline": "run267DW weak slice watch(약한 구간 관찰)",
            "control_variables": "goal guardrails(목표 가드레일); no candidate selection(후보 선택 없음)",
            "changed_variables": "none; prune rule(가지치기 규칙)",
            "sample_scope": "all queued branches(모든 대기 분기)",
            "success_criteria": "next queue(다음 대기열)가 structural feature/route change(구조 피처/경로 변화)를 포함한다.",
            "failure_criteria": "단순 시간/요일/월 제외가 주 실험이 된다.",
            "invalid_conditions": "filter-only(필터 전용) 성공을 robustness(견고성)로 해석한 경우",
            "stop_conditions": "filter-only branch(필터 전용 분기)는 물질화하지 않는다.",
            "evidence_plan": "materialization manifest audit(물질화 목록 감사)",
            "runtime_instruction": "do not materialize standalone(단독 물질화 금지)",
            "materialization_boundary": "guardrail only(가드레일 전용)",
            "aggressive_or_defensive": "prune_guardrail(가지치기 가드레일)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_decisions() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "bd267dx_s258_keep_only_as_structural_stress_challenger",
            "candidate_alias": "s258_stc",
            "candidate_id": "s258_short_tight_control",
            "branch_decision": "continue_but_no_selection(계속하되 선택 아님)",
            "why": "수익과 거래 수는 살아 있으나 2025H1/H2 DD(drawdown, 손실폭)와 약한 구간이 불편하다.",
            "next_use": "q01/q02에서 구조적 DD와 약한 구간 반증으로만 사용한다.",
            "reopen_condition": "DD가 낮아지고 weak slice(약한 구간)가 구조적으로 줄며 trade count(거래 수)가 보존된다.",
            "stop_condition": "단순 제외형 필터로만 좋아지면 stress-only(압박 전용) 보류로 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dx_s264_aih_one_repair_then_prune",
            "candidate_alias": "s264_aih",
            "candidate_id": "s264_allow_inner_high_quarter",
            "branch_decision": "one_repair_plus_counter_probe(1회 수리와 반대 탐침)",
            "why": "core challenger(핵심 도전자)이지만 validation anchor(검증 앵커) init failure(초기화 실패)와 2026.04 음수가 같이 있다.",
            "next_use": "q03 repair gate(수리 게이트)와 q04 counter shock(반대 충격)으로만 사용한다.",
            "reopen_condition": "validation anchor가 실행되고 final month(마지막 달) 음수가 반복되지 않는다.",
            "stop_condition": "init failure 또는 final-month negative(마지막 달 음수)가 반복되면 해당 branch(분기)를 종료한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dx_s264_lc_control_only",
            "candidate_alias": "s264_lc",
            "candidate_id": "s264_lowrank_control",
            "branch_decision": "same_month_control_only(같은 월 대조 전용)",
            "why": "2026.04 방어 대조도 음수라 도전자 수리 가치가 낮다.",
            "next_use": "q03/q04가 실행될 때 시장 공통 약점 판별용으로만 쓴다.",
            "reopen_condition": "후속 후보가 2026.04에서 개선될 때 대조 해석이 필요해지는 경우",
            "stop_condition": "독립 도전자 repair(수리)로 확장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dx_filter_stack_pruned",
            "candidate_alias": "pool_guardrail",
            "candidate_id": "pool_guardrail",
            "branch_decision": "prune_micro_filter_stack(미세 필터 누적 가지치기)",
            "why": "hour16, Monday, 2025-12만 자르면 숫자는 좋아질 수 있지만 후보 체질 증거가 아니다.",
            "next_use": "run267DY materialization audit(물질화 감사)에 적용한다.",
            "reopen_condition": "필터가 구조 피처 또는 경로 변화의 일부이고, 다른 기간에서도 살아남는 경우",
            "stop_condition": "filter-only(필터 전용) 변형은 실행하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "pr267dx_hour_weekday_month_only_filters",
            "affected_candidate_aliases": "s258_stc",
            "affected_scope": "hour16;Monday;2025-12 weak slices(약한 구간)",
            "prune_label": "filter_only_pruned(필터 전용 가지치기)",
            "why_pruned": "단순 제외는 balance/equity curve(잔액/평가금 곡선) 체질 개선을 증명하지 못한다.",
            "salvage_value": "비달력 상태 피처 또는 route state(경로 상태) 반증으로만 살린다.",
            "reopen_condition": "다른 기간과 구간에서도 같은 시장 의미가 유지될 때",
            "do_not_repeat": "hour-only, weekday-only, month-only 제외 실험 반복 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dx_s264_aih_deep_repair_loop_cap",
            "affected_candidate_aliases": "s264_aih",
            "affected_scope": "validation anchor init failure(검증 앵커 초기화 실패)",
            "prune_label": "repair_loop_capped(수리 루프 제한)",
            "why_pruned": "한 후보의 table handoff(테이블 인계) 수리를 3 stage(단계) 이상 끌면 목표의 repair cap(수리 제한)을 어긴다.",
            "salvage_value": "이번 1회 수리에서만 후보 고유 성능을 다시 볼 수 있다.",
            "reopen_condition": "preflight(사전 점검)와 MT5 telemetry(런타임 텔레메트리)가 모두 정상일 때",
            "do_not_repeat": "init failure 반복 branch(분기)를 계속 끌지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dx_s264_lc_challenger_expansion",
            "affected_candidate_aliases": "s264_lc",
            "affected_scope": "2026.04 defensive control(방어 대조)",
            "prune_label": "control_only_no_challenger(대조 전용, 도전자 아님)",
            "why_pruned": "final month(마지막 달) net -39.29와 PF 0.403975라 새 도전자 축으로 확장할 근거가 없다.",
            "salvage_value": "same-month control(같은 월 대조)로만 해석 가치가 있다.",
            "reopen_condition": "다른 후보의 2026.04 탐침과 비교할 대조가 필요할 때",
            "do_not_repeat": "독립 repair(수리) 분기로 열지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "fm267dx_s258_profit_with_dd_fragility",
            "pattern": "profit_survives_but_dd_fragile(수익은 살아남지만 손실폭 취약)",
            "affected_scope": "s258_stc 2025H1/2025H2",
            "why_failed": "net profit(순수익)은 양수지만 DD(drawdown, 손실폭) 24-26%대와 약한 월/시간 손실이 불편하다.",
            "salvage_value": "구조적 risk shape(위험 형태)와 impulse quality(충격 품질)로만 살릴 수 있다.",
            "reopen_condition": "DD, recovery(회복), weak slices(약한 구간)가 동시에 나아질 때",
            "do_not_repeat": "수익만 보고 선택하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dx_s258_adverse_slice_concentration",
            "pattern": "adverse_slice_concentration(불리 구간 집중)",
            "affected_scope": "hour16;Monday;2025-12",
            "why_failed": "최악 구간이 특정 시간/요일/월에 몰려 curve(곡선)를 더럽힌다.",
            "salvage_value": "달력 제외가 아니라 상태 피처 반증으로 다시 볼 수 있다.",
            "reopen_condition": "비달력 feature(피처)로 같은 약점이 완화될 때",
            "do_not_repeat": "특정 bucket(구간)만 제거하는 미세 조정 반복 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dx_s264_aih_anchor_and_final_month_break",
            "pattern": "anchor_init_failure_plus_final_month_negative(앵커 초기화 실패와 마지막 달 음수)",
            "affected_scope": "s264_aih validation anchor and 2026.04",
            "why_failed": "검증 앵커는 init failure(초기화 실패), final month(마지막 달)는 net -33.16이다.",
            "salvage_value": "한 번의 handoff repair(인계 수리)와 counter shock(반대 충격)으로만 확인한다.",
            "reopen_condition": "앵커가 실행되고 2026.04 음수가 사라질 때",
            "do_not_repeat": "깊은 repair loop(수리 루프) 반복 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dx_s264_lc_control_negative",
            "pattern": "control_final_month_negative(대조 마지막 달 음수)",
            "affected_scope": "s264_lc 2026.04",
            "why_failed": "defensive control(방어 대조)도 PF 0.403975로 깨져 후보 확장 가치가 낮다.",
            "salvage_value": "시장 공통 약점 비교 대조로만 가치가 있다.",
            "reopen_condition": "paired control(쌍 대조)이 필요한 후속 실행에서만",
            "do_not_repeat": "도전자처럼 수리하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_experiment_design_receipt(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        rows.append(
            {
                "design_id": row["queue_id"],
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
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_evidence_map(counts: Mapping[str, int]) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "ev267dx_source_review",
            "source_path": rel(SOURCE_REPORT_PATH),
            "source_field": "next_action",
            "observed_value": "run267DX_design_runtime_gap_aware_sixth_followup_or_prune_from_run267DW_review",
            "used_for": "defines this design run(설계 실행) entry point",
            "effect": "prevents stale re-entry(낡은 재진입) from older stage rows",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267dx_candidate_profiles",
            "source_path": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_field": "candidate_profile_rows",
            "observed_value": counts["candidate_profile_rows"],
            "used_for": "s258/s264 profile comparison(후보 프로필 비교)",
            "effect": "keeps queue tied to completed MT5 trade evidence(완료 거래 근거)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267dx_init_failure_summary",
            "source_path": rel(SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH),
            "source_field": "s264_aih init_failure_attempts",
            "observed_value": "1 init failure and 1 ebm_table_open_failure",
            "used_for": "s264_aih one repair cap(1회 수리 제한)",
            "effect": "separates blocked evidence(차단 근거) from bad KPI(나쁜 지표)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267dx_negative_slices",
            "source_path": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_field": "negative_slice_rows",
            "observed_value": counts["negative_slice_rows"],
            "used_for": "anti filter-stack rule(필터 누적 방지 규칙)",
            "effect": "weak buckets(약한 구간)을 structural tests(구조 시험)로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267dx_curve_diagnostics",
            "source_path": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            "source_field": "curve_rows",
            "observed_value": counts["curve_rows"],
            "used_for": "balance/equity curve boundary(잔액/평가금 곡선 경계)",
            "effect": "숫자만 좋은 후보 선택을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "run267DW review, profile rows, weak slices, init failure summary",
            "evidence_missing": "run267DY materialized variants and MT5(MetaTrader 5, 메타트레이더5) outputs",
            "judgment_label": "design_completed_no_candidate_selection(설계 완료, 후보 선택 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "baseline(기준 후보) 선택이 느린 이유는 수익 숫자보다 덜 깨지는 구조를 확인하기 때문이다.",
        },
        {
            "result_subject": "candidate_selection",
            "evidence_available": "design queue only(설계 대기열만 있음)",
            "evidence_missing": "fresh MT5 execution(새 MT5 실행), curve review(곡선 검토), adapter evidence(어댑터 근거)",
            "judgment_label": "not_selected(선택 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run267DY then execution/review",
            "user_explanation_hook": "아직 ONNX(온엑스)나 최종 후보로 넘길 단계가 아니다.",
        },
    ]


def build_gate_audit(queue_rows: Sequence[Mapping[str, Any]], prune_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materializable = [row for row in queue_rows if "do not materialize" not in str(row.get("runtime_instruction", ""))]
    aggressive = [
        row
        for row in queue_rows
        if "aggressive" in str(row.get("aggressive_or_defensive", "")) or "explosive" in str(row.get("aggressive_or_defensive", ""))
    ]
    return [
        {
            "gate_id": "gate267dx_input_evidence",
            "gate_name": "input evidence present(입력 근거 존재)",
            "status": "pass",
            "evidence": f"{rel(SOURCE_CANDIDATE_PROFILE_PATH)};{rel(SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH)};{rel(SOURCE_NEGATIVE_SLICE_PATH)}",
            "effect": "design starts from run267DW evidence(267DW 근거에서 시작)",
        },
        {
            "gate_id": "gate267dx_aggressive_branch",
            "gate_name": "aggressive branch included(공격 분기 포함)",
            "status": "pass",
            "evidence": f"aggressive_or_explosive_queue_rows={len(aggressive)}",
            "effect": "avoids too-defensive-only loop(방어만 도는 루프 방지)",
        },
        {
            "gate_id": "gate267dx_repair_cap",
            "gate_name": "repair cap enforced(수리 제한 적용)",
            "status": "pass",
            "evidence": "q03_s264_aih_validation_anchor_one_repair",
            "effect": "prevents dragging one repair branch(한 수리 분기 장기화 방지)",
        },
        {
            "gate_id": "gate267dx_anti_filter_stack",
            "gate_name": "anti filter stack enforced(필터 누적 방지 적용)",
            "status": "pass",
            "evidence": f"prune_rows={len(prune_rows)}; q06_prune_micro_filter_stack",
            "effect": "weak slices become structural tests(약한 구간을 구조 시험으로 전환)",
        },
        {
            "gate_id": "gate267dx_materialization_ready",
            "gate_name": "materialization ready(물질화 준비)",
            "status": "pass",
            "evidence": f"queue_rows={len(queue_rows)}; materializable_rows={len(materializable)}",
            "effect": "run267DY can create variants/attempts(변형/시도 생성 가능)",
        },
        {
            "gate_id": "gate267dx_claim_guard",
            "gate_name": "claim guard(주장 가드)",
            "status": "pass",
            "evidence": "selected_candidate=none; selected_research_baseline=none; onnx_readiness=not_claimed; goal_achieve=not_claimed",
            "effect": "keeps this as R&D racing design(연구개발 경주 설계) only",
        },
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    queue_rows = result["materialization_queue"]
    branch_rows = result["branch_decisions"]
    prune_rows = result["prune_matrix"]
    failure_rows = result["failure_memory"]
    gate_rows = result["gate_audit"]
    lines = [
        "# Stage267 Run267DX Runtime Gap Aware Sixth Follow-Up/Prune Design(267단계 267DX 런타임 공백 반영 6차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- queue_rows(대기열 행): `{len(queue_rows)}`",
        f"- aggressive_or_explosive_rows(공격/폭발 행): `{result['aggressive_queue_count']}`",
        f"- prune_rows(가지치기 행): `{len(prune_rows)}`",
        f"- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DX(267DX 실행)는 run267DW(267DW 실행)의 review(검토)를 다음 materialization queue(물질화 대기열)로 바꾼 설계다.",
        "효과: s258_stc(258 STC 후보)는 수익은 살아 있지만 DD(drawdown, 손실폭)와 약한 시간/월 구간이 불편해서 구조적 반증으로만 계속 본다.",
        "효과: s264_aih(264 AIH 후보)는 validation anchor(검증 앵커) init failure(초기화 실패)와 2026.04 음수가 겹쳐, 한 번만 수리하고 실패하면 가지치기한다.",
        "효과: s264_lc(264 LC 후보)는 같은 달 control(대조)로만 남기고 도전자 수리는 하지 않는다.",
        "",
        "baseline(기준 후보)을 정하는 데 오래 걸리는 이유는 여기서 baseline(기준 후보)이 운영 기준선이 아니기 때문이다. 지금은 R&D racing(연구개발 경주)용 후보군이므로, 숫자 몇 개보다 balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), 약한 월/요일/시간, Adapter(어댑터) 확장 가능성을 같이 본다.",
        "",
        "## Queue(대기열)",
        "",
        "| queue_id(대기열 ID) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | instruction(지시) |",
        "|---|---|---|---|---|",
    ]
    for row in queue_rows:
        lines.append(
            "| "
            f"`{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | "
            f"{row['workstream']} | {row['runtime_instruction']} |"
        )
    lines.extend(
        [
            "",
            "## Branch Decisions(분기 판단)",
            "",
            "| decision(판단) | candidate(후보) | next_use(다음 용도) | stop_condition(중단 조건) |",
            "|---|---|---|---|",
        ]
    )
    for row in branch_rows:
        lines.append(
            "| "
            f"`{row['decision_id']}` | `{row['candidate_alias']}` | "
            f"{row['next_use']} | {row['stop_condition']} |"
        )
    lines.extend(
        [
            "",
            "## Prune Matrix(가지치기 행렬)",
            "",
            "| prune_id(가지치기 ID) | affected(대상) | why(이유) | do_not_repeat(반복 금지) |",
            "|---|---|---|---|",
        ]
    )
    for row in prune_rows:
        lines.append(
            "| "
            f"`{row['prune_id']}` | `{row['affected_candidate_aliases']}` | "
            f"{row['why_pruned']} | {row['do_not_repeat']} |"
        )
    lines.extend(
        [
            "",
            "## Failure Memory(실패 기억)",
            "",
            "| memory(기억) | affected_scope(대상 범위) | do_not_repeat(반복 금지) |",
            "|---|---|---|",
        ]
    )
    for row in failure_rows:
        lines.append(
            "| "
            f"`{row['memory_id']}` | {row['affected_scope']} | {row['do_not_repeat']} |"
        )
    lines.extend(
        [
            "",
            "## Gate Audit(게이트 감사)",
            "",
            "| gate(게이트) | status(상태) | effect(효과) |",
            "|---|---|---|",
        ]
    )
    for row in gate_rows:
        lines.append(f"| `{row['gate_id']}` | `{row['status']}` | {row['effect']} |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run267DX(267DX 실행)는 design(설계)이다. 새 MT5(MetaTrader 5, 메타트레이더5) 결과, Adapter(어댑터) 패키지, ONNX parity(ONNX 동등성) 근거는 아직 없다.",
            "따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DX_producer", "producer_script", PRODUCER_PATH, "Builds run267DX sixth follow-up/prune design."),
        ("stage267_run267DX_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267DW review result."),
        ("stage267_run267DX_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Sixth follow-up/prune queue."),
        ("stage267_run267DX_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decisions."),
        ("stage267_run267DX_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune matrix."),
        ("stage267_run267DX_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267DX_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DX_evidence_map", "evidence_map", EVIDENCE_MAP_PATH, "Evidence map."),
        ("stage267_run267DX_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DX_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DX_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DX_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DX_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267DX_report", "review_report", REPORT_PATH, "User-facing report."),
    )
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


def stage267_report_entry() -> str:
    return f"  run267DX_runtime_gap_aware_sixth_followup_or_prune_design_report_path: {rel(REPORT_PATH)}"


def update_stage267_workspace_block(text: str) -> str:
    report_entry = stage267_report_entry()
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    report_seen = report_entry in text
    for line in lines:
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" "):
            if not report_seen:
                output.append(report_entry)
                report_seen = True
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
                if not report_seen:
                    output.append(report_entry)
                    report_seen = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not report_seen:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"queue_rows={len(result['materialization_queue'])};"
        f"aggressive_rows={result['aggressive_queue_count']};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267DX_runtime_gap_aware_sixth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_sixth_followup_or_prune_design",
        "tier_scope": "design only from run267DW completed and blocked evidence",
        "scoreboard": "queue_prune_failure_memory_experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_sixth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_sixth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_sixth_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_sixth_followup_or_prune_design",
        "tier_scope": "design only; MT5 evidence must be created in run267DY+",
        "kpi_scope": "queue_prune_failure_memory_experiment_design",
        "scoreboard_lane": "runtime_gap_aware_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={len(result['materialization_queue'])};aggressive_rows={result['aggressive_queue_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}. Design enforces repair cap and anti filter-stack guard.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267DX_runtime_gap_aware_sixth_followup_or_prune_design"
        f"(267DX 런타임 공백 반영 6차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_design(최신 설계): run267DX(267DX 실행) queue_rows(대기열 행) "
        f"`{len(result['materialization_queue'])}`, aggressive_rows(공격 행) `{result['aggressive_queue_count']}`, "
        f"prune_rows(가지치기 행) `{len(result['prune_matrix'])}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DX(267DX 실행)는 run267DW(267DW 실행)의 후보 프로필/초기화 실패/약한 구간 근거를 6차 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, aggressive/explosive branch(공격/폭발 분기) `{result['aggressive_queue_count']}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_sixth_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "stage267_run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures.md", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267DX(267DX 실행)는 run267DW", block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "stage267_run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality", report_line)
    selection = append_block_once(selection, "Run267DX(267DX 실행)는 run267DW", block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "stage267_run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures.md", report_line)
    review_index = append_block_once(review_index, "Run267DX(267DX 실행)는 run267DW", block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = update_stage267_workspace_block(workspace)
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DX(267DX 실행) runtime gap aware sixth follow-up/prune design"
        f"(런타임 공백 반영 6차 후속/가지치기 설계) `{STATUS}`. "
        f"Effect(효과): run267DW(267DW 실행)의 DD(drawdown, 손실폭), weak slice(약한 구간), init failure(초기화 실패) 근거를 "
        f"materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개와 prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_design() -> dict[str, Any]:
    created_at = utc_now()
    counts = source_counts()
    queue_rows = build_materialization_queue()
    branch_rows = build_branch_decisions()
    prune_rows = build_prune_matrix()
    failure_rows = build_failure_memory()
    experiment_rows = build_experiment_design_receipt(queue_rows)
    evidence_rows = build_evidence_map(counts)
    result_judgment = build_result_judgment()
    gate_rows = build_gate_audit(queue_rows, prune_rows)
    aggressive_count = sum(
        1
        for row in queue_rows
        if "aggressive" in str(row.get("aggressive_or_defensive", "")) or "explosive" in str(row.get("aggressive_or_defensive", ""))
    )
    result: dict[str, Any] = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_counts": counts,
        "materialization_queue": queue_rows,
        "branch_decisions": branch_rows,
        "prune_matrix": prune_rows,
        "failure_memory": failure_rows,
        "experiment_design_receipt": experiment_rows,
        "evidence_map": evidence_rows,
        "result_judgment": result_judgment,
        "gate_audit": gate_rows,
        "aggressive_queue_count": aggressive_count,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "branch_decision_matrix": rel(BRANCH_DECISION_PATH),
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
    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "queue_rows": len(queue_rows),
        "aggressive_queue_count": aggressive_count,
        "prune_rows": len(prune_rows),
        "next_action": NEXT_ACTION,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "sources": {
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_candidate_profile": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_candidate_init_failure_summary": rel(SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH),
            "source_attempt_outcome": rel(SOURCE_ATTEMPT_OUTCOME_PATH),
            "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": result["outputs"],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(MATERIALIZATION_QUEUE_PATH, queue_rows, QUEUE_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, branch_rows, BRANCH_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, prune_rows, PRUNE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_rows, FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, experiment_rows, EXPERIMENT_DESIGN_COLUMNS)
    write_csv(EVIDENCE_MAP_PATH, evidence_rows, EVIDENCE_MAP_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result_judgment, RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, gate_rows, GATE_AUDIT_COLUMNS)
    write_json(RUN_MANIFEST_PATH, run_manifest)
    write_json(LINEAGE_PATH, lineage)
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> int:
    result = build_design()
    print(
        json.dumps(
            {
                "status": result["status"],
                "queue_rows": len(result["materialization_queue"]),
                "aggressive_queue_count": result["aggressive_queue_count"],
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
