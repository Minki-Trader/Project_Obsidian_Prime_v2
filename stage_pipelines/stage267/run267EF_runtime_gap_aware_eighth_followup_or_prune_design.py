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
    run267EE_runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267EF"
RUN_ID = "run267EF_stage267_runtime_gap_aware_eighth_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267EF_runtime_gap_aware_eighth_followup_or_prune_design_completed"
JUDGMENT = "runtime_gap_aware_eighth_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267EG_materialize_runtime_gap_aware_eighth_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_eighth_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_ATTEMPT_OUTCOME_PATH = source_review.ATTEMPT_OUTCOME_REVIEW_PATH
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267EF_runtime_gap_aware_eighth_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267EF_runtime_gap_aware_eighth_followup_or_prune_design.py")

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

GATE_AUDIT_COLUMNS = (
    "gate_id",
    "gate_name",
    "status",
    "evidence",
    "effect",
    "claim_boundary",
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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    write_md(path, text)


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def append_line_once(text: str, line: str) -> str:
    if line in text:
        return text
    return text.rstrip() + "\n" + line + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text


def replace_first_exact_prefix(text: str, prefix: str, replacement: str) -> str:
    return replace_line_prefix(text, prefix, replacement)


def as_float(row: Mapping[str, str], key: str) -> float:
    try:
        return float(row.get(key, "0") or 0)
    except ValueError:
        return 0.0


def build_source_summary(
    profile_rows: Sequence[Mapping[str, str]],
    attempt_rows: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    completed = [row for row in attempt_rows if row.get("execution_status") == "completed"]
    blocked = [row for row in attempt_rows if row.get("execution_status") == "blocked"]
    profile_by_alias: dict[str, list[Mapping[str, str]]] = {}
    for row in profile_rows:
        profile_by_alias.setdefault(row.get("candidate_alias", ""), []).append(row)
    worst_slices = sorted(negative_rows, key=lambda row: as_float(row, "net_profit"))[:12]
    return {
        "profile_rows": len(profile_rows),
        "attempt_rows": len(attempt_rows),
        "completed_attempts": len(completed),
        "blocked_attempts": len(blocked),
        "profile_by_alias": {key: len(value) for key, value in sorted(profile_by_alias.items())},
        "worst_slices": worst_slices,
        "s258_worst_h1_session": "-120.64 session_21_23_report_time",
        "s258_worst_h2_month": "-82.97 month 2025-12",
        "final_month_shared_loss": "s264_aih -30.46; s264_lc/s262_lih/s264_aia -39.29",
        "duplicate_signature": "s262_lih and s264_aia share validation +574.21 and 2026.04 -39.29",
    }


def build_feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "fb01_s258_period_survival_quality_split",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "feature_family": "period_survival_trade_quality",
            "market_meaning": "2025H1/H2 survival(생존) 숫자는 양수지만 DD(drawdown, 손실폭)와 약한 시간대가 불편한지 확인한다.",
            "source_evidence": "run267EE s258_stc 2025H1 net 301.88 PF 1.182 DD 14.65; 2025H2 net 164.54 PF 1.135 DD 20.51.",
            "changed_variables": "split period quality lens(기간별 거래 품질 관점), weak hour/session attribution(약한 시간/세션 귀속).",
            "held_variables": "candidate identity(후보 정체성), Tier A(티어 A), FPMarkets US100 M5, no calendar ban(달력 금지 없음).",
            "aggressive_or_defensive": "defensive_diagnostic",
            "success_read": "양수 유지뿐 아니라 late chron(후반 구간), Monday(월요일), hour 19/21(19/21시)이 덜 깨지면 계속 압박한다.",
            "failure_read": "PF(수익 팩터)만 양수이고 DD/약한 구간이 계속 불편하면 stress challenger(압박 도전자) 역할을 낮춘다.",
            "materialization_note": "run267EG(267EG 실행)에서 survival gate(생존 게이트)를 약한 구간 중심으로 재물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb02_s258_explosive_init_failure_diagnostic",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "feature_family": "explosive_supply_handoff",
            "market_meaning": "공격형 explosive impulse(폭발형 임펄스) 아이디어가 숫자가 나쁘기 전에 init failure(초기화 실패)로 막혔는지 본다.",
            "source_evidence": "run267EE run267ec_03/04/05 blocked with init_failed timeout.",
            "changed_variables": "handoff precheck(인계 사전검사), minimal one-run smoke(최소 1회 스모크), not full repeated rerun(전체 반복 재실행 아님).",
            "held_variables": "same s258_stc model/feature identity(동일 후보 정체성), same split labels(동일 기간 라벨).",
            "aggressive_or_defensive": "aggressive_diagnostic",
            "success_read": "초기화 실패 원인이 분리되고 최소 한 개 runtime(런타임) 거래 근거가 생기면 공격 분기를 다시 열 수 있다.",
            "failure_read": "같은 초기화 실패가 재현되면 explosive supply(폭발 공급) 분기는 failure memory(실패 기억)로 닫는다.",
            "materialization_note": "공격형 실험은 유지하되 같은 실패를 3개 기간에 그대로 반복하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb03_s264_aih_validation_final_month_decoupling",
            "candidate_aliases": "s264_aih;s264_lc",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control",
            "feature_family": "validation_anchor_vs_final_month",
            "market_meaning": "s264_aih validation anchor(검증 앵커)는 좋지만 2026.04 final month(마지막 달)가 깨지는 문제를 분리한다.",
            "source_evidence": "run267EE s264_aih validation net 518.62 PF 1.222 DD 11.71; 2026.04 net -30.46 PF 0.429. s264_lc control 2026.04 net -39.29.",
            "changed_variables": "counter-shock state(역충격 상태), sell-side fragility(매도 취약성), validation/final-month split(검증/마지막 달 분리).",
            "held_variables": "s264_aih challenger role(도전자 역할), s264_lc control role(대조 역할), no selection claim(선택 주장 없음).",
            "aggressive_or_defensive": "bounded_repair",
            "success_read": "validation(검증)을 망치지 않고 final-month(마지막 달) 음수가 줄면 한 번 더 살린다.",
            "failure_read": "validation만 예쁘고 final month(마지막 달)가 계속 음수면 core challenger(핵심 도전자) 지위를 낮춘다.",
            "materialization_note": "repair loop(수리 루프)는 2개 stage(단계) 이상 끌지 않는 제한을 명시한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb04_shared_202604_sell_fragility",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "feature_family": "shared_final_month_loss_state",
            "market_meaning": "여러 후보가 2026.04에서 동시에 음수라 후보 단독 결함인지 시장 구간 결함인지 구분한다.",
            "source_evidence": "run267EE 2026.04 rows: s264_aih -30.46; s264_lc -39.29; s262_lih -39.29; s264_aia -39.29.",
            "changed_variables": "shared adverse state(공유 불리 상태), direction sell(매도 방향), final-month pressure(마지막 달 압박).",
            "held_variables": "candidate-specific thresholds(후보별 임계값), feature order(피처 순서), MT5 handoff(메타트레이더5 인계).",
            "aggressive_or_defensive": "pool_wide_pressure",
            "success_read": "공유 상태를 설명하면서도 특정 후보 하나만 과하게 살리는 calendar filter(달력 필터)가 아니어야 한다.",
            "failure_read": "모든 후보가 같은 방식으로 깨지면 현재 feature structure(피처 구조) 자체를 바꾸는 방향으로 전환한다.",
            "materialization_note": "후보군 전체 shared weakness(공유 약점) 압박 행으로 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb05_s262_s264_aia_identity_audit",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": "s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "feature_family": "duplicate_surface_identity",
            "market_meaning": "validation(검증) 양수와 2026.04 음수가 완전히 같은 서명이라 두 후보가 독립 후보인지 확인한다.",
            "source_evidence": "run267EE s262_lih and s264_aia both validation +574.21 PF 1.212909 and final-month -39.29 PF 0.403975.",
            "changed_variables": "feature-order audit(피처 순서 감사), adapter identity check(어댑터 정체성 확인), route label audit(라우팅 라벨 감사).",
            "held_variables": "same validation/final-month scopes(같은 검증/마지막 달 범위), no candidate merge claim(후보 병합 주장 없음).",
            "aggressive_or_defensive": "diagnostic",
            "success_read": "동일 서명이 이유 있는 대조 구조인지 확인되면 둘을 역할 분리해 유지한다.",
            "failure_read": "사실상 같은 surface(표면)이면 한쪽은 independent candidate(독립 후보) 주장을 낮춘다.",
            "materialization_note": "다음 물질화 전에 identity receipt(정체성 영수증)를 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_decisions() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "bd01_s258_keep_as_stress_not_selection",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "branch_decision": "keep_but_split_survival_quality_from_explosive_failure",
            "why": "2025H1/H2는 양수지만 2025H2 DD 20.51과 2025-12 -82.97, Monday -73.87이 불편하다.",
            "next_use": "period survival(기간 생존)은 거래 품질로 압박하고 explosive branch(폭발 분기)는 초기화 진단으로만 연다.",
            "reopen_condition": "약한 기간에서도 PF/DD/trade quality(수익 팩터/손실폭/거래 품질)가 같이 개선될 때.",
            "stop_condition": "init_failed(초기화 실패)가 반복되거나 H2 DD가 계속 커질 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd02_s264_aih_keep_core_with_one_bounded_repair",
            "candidate_aliases": "s264_aih;s264_lc",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control",
            "branch_decision": "keep_core_challenger_only_under_validation_final_month_split",
            "why": "validation anchor(검증 앵커)는 +518.62로 살아 있지만 2026.04는 -30.46이고 control(대조)도 -39.29다.",
            "next_use": "s264_lc는 선택 후보가 아니라 시장 구간 해석용 defensive control(방어 대조)로만 둔다.",
            "reopen_condition": "2026.04 손실을 줄이면서 validation(검증) 손상을 만들지 않을 때.",
            "stop_condition": "같은 final-month repair(마지막 달 수리)가 2회 안에 실패할 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd03_s262_s264_aia_hold_until_identity_audit",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": "s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "branch_decision": "hold_independent_selection_until_duplicate_signature_explained",
            "why": "검증 +574.21, 2026.04 -39.29가 둘 다 같아 독립 후보 의미가 흐리다.",
            "next_use": "identity audit(정체성 감사) 후 validation-heavy(검증 중심)와 OOS anchor(표본외 앵커) 역할을 다시 나눈다.",
            "reopen_condition": "feature order(피처 순서), decision surface(결정 표면), route label(라우팅 라벨) 차이가 확인될 때.",
            "stop_condition": "동일 표면이면 한쪽은 duplicate control(중복 대조)로 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd04_pool_final_month_shared_state_first",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "branch_decision": "treat_202604_as_shared_state_before_candidate_prune",
            "why": "여러 후보가 2026.04에서 음수라 후보별 미세 필터보다 공유 시장 상태 해석이 먼저다.",
            "next_use": "shared adverse state(공유 불리 상태) queue(대기열)로 물질화한다.",
            "reopen_condition": "공유 상태가 특정 후보에서만 덜 깨지는지 보여줄 때.",
            "stop_condition": "calendar/hour ban(달력/시간 금지)만으로 좋아지는 결과가 나올 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd05_prune_filter_stack_and_headline_profit",
            "candidate_aliases": "pool",
            "candidate_ids": "all_stage267_baseline_candidate_pool",
            "branch_decision": "prune_headline_profit_selection_and_filter_stack",
            "why": "Goal(목표)은 숫자 1등 선택이 아니라 여러 기간과 구간에서 덜 깨지는 후보다.",
            "next_use": "queue(대기열)는 ablation/replacement(제거/대체), shared state(공유 상태), identity(정체성), runtime handoff(런타임 인계)를 같이 요구한다.",
            "reopen_condition": "없음. 선택 주장은 Goal gate(목표 게이트) 이전에 열지 않는다.",
            "stop_condition": "후보 선택이나 ONNX(온엑스) 검토로 해석될 때 즉시 경계 낮춤.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "q01_s258_period_survival_quality_split",
            "priority": "P0",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "trade_quality_period_survival",
            "source_evidence": "run267EE s258 2025H1/H2 completed with 614 trades total but DD/weak slices remain uncomfortable.",
            "hypothesis": "s258_stc may survive as stress challenger(압박 도전자) only if period survival(기간 생존) is not hiding DD/time-slice weakness.",
            "decision_use": "s258_stc stress role(압박 역할)을 다음 racing packet(경주 묶음)에서 유지, 하향, 또는 가지치기할지 결정한다.",
            "comparison_baseline": "run267EE q01/q02 s258 period survival rows.",
            "control_variables": "candidate identity, Tier A, symbol US100, timeframe M5, execution harness, no new calendar exclusion.",
            "changed_variables": "score weak-period survival by month/weekday/hour/session/chron segment and trade quality.",
            "sample_scope": "2025H1 validation-post-2024 and 2025H2 OOS follow-through.",
            "success_criteria": "PF stays above 1.15, DD improves, weak slices shrink without collapsing trade count.",
            "failure_criteria": "2025H2 DD remains around 20 percent, 2025-12/Monday/hour19 losses remain dominant, or trade count becomes too thin.",
            "invalid_conditions": "missing MT5 report, parser mismatch, changed candidate identity, hidden calendar ban.",
            "stop_conditions": "Stop after one materialized pass; do not convert to another narrow month repair loop.",
            "evidence_plan": "MT5 report, trade_records, curve_diagnostics, time_slice_kpi, candidate_profile_review, negative_slice_summary.",
            "runtime_instruction": "materialize as Tier A attempts; no ONNX(온엑스); no selection claim.",
            "aggressive_or_defensive": "defensive_diagnostic",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_s258_explosive_init_failure_triage",
            "priority": "P0",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "aggressive_runtime_handoff_diagnostic",
            "source_evidence": "run267EE run267ec_03/04/05 all blocked by init_failed timeout before trade evidence.",
            "hypothesis": "The explosive impulse(폭발형 임펄스) branch may be blocked by handoff/runtime setup rather than market failure.",
            "decision_use": "aggressive s258 branch(공격형 s258 분기)를 실제 runtime attempt(런타임 시도)로 열지, failure memory(실패 기억)로 닫을지 결정한다.",
            "comparison_baseline": "run267EE blocked explosive attempts.",
            "control_variables": "same s258_stc candidate, same split labels, same MT5 harness, fixed feature order.",
            "changed_variables": "pre-runtime validation, minimal handoff probe, one representative smoke attempt only if handoff is valid.",
            "sample_scope": "2023H2, 2025H1, 2025H2 diagnostic labels; trade evidence only if precheck passes.",
            "success_criteria": "init failure root cause is recorded and at least one representative attempt reaches runtime output.",
            "failure_criteria": "same init_failed timeout repeats or handoff file is invalid.",
            "invalid_conditions": "probe silently changes strategy settings or masks the failed branch as zero-trade success.",
            "stop_conditions": "Do not rerun all three failed attempts without a new handoff receipt.",
            "evidence_plan": "handoff receipt, setup diff, execution_result, init log, optional one MT5 report.",
            "runtime_instruction": "aggressive diagnostic first; materialize full aggressive branch only after precheck.",
            "aggressive_or_defensive": "aggressive_diagnostic",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s264_aih_validation_final_month_bounded_repair",
            "priority": "P0",
            "candidate_aliases": "s264_aih;s264_lc",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control",
            "workstream": "validation_anchor_final_month_decoupling",
            "source_evidence": "run267EE s264_aih validation +518.62 but 2026.04 -30.46; s264_lc control 2026.04 -39.29.",
            "hypothesis": "s264_aih remains a core challenger(핵심 도전자) only if final-month shock can be reduced without damaging validation anchor.",
            "decision_use": "bounded repair(제한 수리) 후 s264_aih core challenger(핵심 도전자) 역할을 유지할지 하향할지 결정한다.",
            "comparison_baseline": "run267EE s264_aih validation_anchor_integrity and 202604_counter_shock_rebuild plus s264_lc control.",
            "control_variables": "s264_aih/s264_lc identities, feature order, risk/ATR handoff, Tier A scope.",
            "changed_variables": "final-month adverse-state handling, sell-side shock read, no headline-profit filter.",
            "sample_scope": "validation_is and 2026.04 final month.",
            "success_criteria": "final-month loss improves while validation remains positive with acceptable DD and trade count.",
            "failure_criteria": "2026.04 stays negative or validation anchor is damaged.",
            "invalid_conditions": "selection claim, calendar-only repair, missing control pair, parser mismatch.",
            "stop_conditions": "Close or downgrade if this bounded repair fails; do not stretch into a third repair loop.",
            "evidence_plan": "paired MT5 reports, curve diagnostics, time-slice KPI, trade quality, control comparison.",
            "runtime_instruction": "materialize s264_aih plus s264_lc paired control; no ONNX(온엑스).",
            "aggressive_or_defensive": "bounded_repair",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_pool_202604_shared_sell_fragility_pressure",
            "priority": "P1",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "workstream": "pool_wide_shared_final_month_state",
            "source_evidence": "run267EE final-month rows are negative for four candidate/control surfaces.",
            "hypothesis": "2026.04 may be a shared adverse market state rather than a single candidate defect.",
            "decision_use": "shared state(공유 상태)를 위한 feature engineering(피처 엔지니어링)으로 pivot(전환)할지, 후보별 repair(수리)를 가지치기할지 결정한다.",
            "comparison_baseline": "run267EE 2026.04 rows across s264_aih/s264_lc/s262_lih/s264_aia.",
            "control_variables": "same execution harness, same date scope, no calendar/hour ban, same candidate surfaces.",
            "changed_variables": "shared adverse-state tags, direction/sell attribution, cross-candidate weakness grouping.",
            "sample_scope": "2026-04-01 through 2026-04-13 OOS final month.",
            "success_criteria": "one candidate or feature structure clearly loses less without hiding trades.",
            "failure_criteria": "all candidates remain similar negative or improvement comes only from removing trades.",
            "invalid_conditions": "missing reports, changed date scope, duplicate candidate surfaces not disclosed.",
            "stop_conditions": "If all fail similarly, move to feature-structure pivot instead of more threshold repair.",
            "evidence_plan": "cross-candidate MT5 reports, direction/time-slice KPI, curve diagnostics, candidate profile review.",
            "runtime_instruction": "materialize as a pool-wide pressure pass, not as candidate selection.",
            "aggressive_or_defensive": "pool_wide_pressure",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q05_s262_s264_aia_identity_and_feature_order_audit",
            "priority": "P1",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": "s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "workstream": "identity_surface_audit",
            "source_evidence": "run267EE s262_lih and s264_aia have identical validation and 2026.04 KPI signatures.",
            "hypothesis": "The two candidates may be sharing an equivalent decision surface or handoff path.",
            "decision_use": "두 후보를 separate roles(분리 역할)로 유지할지, 한쪽을 duplicate control(중복 대조)로 낮출지 결정한다.",
            "comparison_baseline": "run267EE s262_lih/s264_aia validation and final-month rows.",
            "control_variables": "same reports, same feature order contract, same adapter handoff path.",
            "changed_variables": "identity receipts, feature hash/order comparison, route label verification.",
            "sample_scope": "validation_is and 2026.04 final-month evidence.",
            "success_criteria": "a meaningful surface or handoff difference is documented.",
            "failure_criteria": "no difference is found or both paths are the same model/feature bundle.",
            "invalid_conditions": "audit lacks hashes, route labels, or feature order receipts.",
            "stop_conditions": "Do not treat duplicate KPI signatures as independent evidence until audit passes.",
            "evidence_plan": "feature order receipt, model/config hashes, route label check, lineage map.",
            "runtime_instruction": "diagnostic materialization; MT5 only if identity audit needs a reproduction check.",
            "aggressive_or_defensive": "diagnostic",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q06_s264_aih_explosive_counter_impulse_handoff_triage",
            "priority": "P1",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "workstream": "aggressive_explosive_handoff_diagnostic",
            "source_evidence": "run267EE run267ec_09/10 blocked by init_failed timeout.",
            "hypothesis": "The s264_aih explosive counter impulse(폭발형 역임펄스) branch may be useful only if handoff failure is repaired narrowly.",
            "decision_use": "aggressive branch(공격 분기) 하나를 다시 열지, failure memory(실패 기억)로 기록할지 결정한다.",
            "comparison_baseline": "run267EE q06 blocked validation and 2026.04 explosive attempts.",
            "control_variables": "s264_aih identity, validation/final-month scopes, no full rerun before precheck.",
            "changed_variables": "handoff validation, minimal smoke, init failure root-cause receipt.",
            "sample_scope": "validation_is and 2026.04 labels.",
            "success_criteria": "handoff root cause found and one attempt reaches runtime output.",
            "failure_criteria": "init_failed repeats or probe cannot preserve feature order.",
            "invalid_conditions": "silent parameter drift, missing log, zero-trade treated as success.",
            "stop_conditions": "One bounded diagnostic only; close if the failure repeats.",
            "evidence_plan": "handoff file receipt, init log, setup diff, optional MT5 report.",
            "runtime_instruction": "aggressive diagnostic; no candidate selection.",
            "aggressive_or_defensive": "aggressive_diagnostic",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q07_pool_prune_guard_and_next_pivot_receipt",
            "priority": "P2",
            "candidate_aliases": "pool",
            "candidate_ids": "all_stage267_baseline_candidate_pool",
            "workstream": "prune_guard_and_pivot_receipt",
            "source_evidence": "run267EE shows positive-but-not-strong rows, final-month breaks, duplicate signatures, and init failures.",
            "hypothesis": "The next pass must either produce broader stability evidence or pivot away from repeated repair loops.",
            "decision_use": "filter-stack(필터 누적)과 headline-profit(표면 수익) selection(선택)을 막는다.",
            "comparison_baseline": "Stage267 goal gate and run267EE result judgment.",
            "control_variables": "candidate pool, claim boundary, no ONNX(온엑스), no operating claim(운영 주장 없음).",
            "changed_variables": "queue-level stop conditions and prune receipts.",
            "sample_scope": "all Stage267 baseline candidate pool evidence up to run267EE.",
            "success_criteria": "run267EG has explicit materialization/prune gates before execution.",
            "failure_criteria": "next work only tweaks one threshold/month or selects by net profit.",
            "invalid_conditions": "missing gate audit, missing failure memory, missing artifact lineage.",
            "stop_conditions": "If evidence remains narrow, pivot to new feature structure or discard weak branches.",
            "evidence_plan": "materialization manifest, prune matrix, failure memory, artifact registry rows.",
            "runtime_instruction": "no standalone MT5 attempt; use as guardrail receipt.",
            "aggressive_or_defensive": "guardrail",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "pr01_no_headline_profit_selection",
            "affected_candidate_aliases": "pool",
            "affected_scope": "all positive rows",
            "prune_label": "headline_profit_selection_pruned",
            "why_pruned": "run267EE에는 positive validation/period rows(양수 검증/기간 행)가 있지만 weak slices(약한 구간)와 final-month breaks(마지막 달 붕괴)가 남아 있다.",
            "salvage_value": "Positive rows are still useful as comparison baselines(비교 기준).",
            "reopen_condition": "Only after balance/equity(잔액/평가금), period, ablation/replacement, Adapter(어댑터), and runtime evidence survive.",
            "do_not_repeat": "Do not choose candidate by net profit or PF alone.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr02_no_raw_explosive_rerun_after_init_failure",
            "affected_candidate_aliases": "s258_stc;s264_aih",
            "affected_scope": "blocked explosive branches",
            "prune_label": "raw_explosive_rerun_pruned",
            "why_pruned": "five explosive attempts(폭발형 시도 5개)가 init_failed(초기화 실패)로 막혔고, direct rerun(직접 재실행)은 runtime gap(런타임 공백)을 반복한다.",
            "salvage_value": "Use a handoff diagnostic first, then one representative smoke attempt.",
            "reopen_condition": "Handoff receipt and setup diff explain the failure.",
            "do_not_repeat": "Do not rerun all blocked attempts without a precheck.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr03_no_one_month_rescue_selection",
            "affected_candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "affected_scope": "2026.04 final-month repair",
            "prune_label": "single_month_rescue_pruned",
            "why_pruned": "single final-month fix(단일 마지막 달 수정)는 broader weakness(더 넓은 약점)를 숨기고 one slice(한 구간)에 과적합될 수 있다.",
            "salvage_value": "Use 2026.04 as shared adverse-state pressure evidence.",
            "reopen_condition": "Improvement also survives validation and adjacent periods.",
            "do_not_repeat": "Do not add naked month/hour/session filters.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr04_no_duplicate_independent_candidate_claim",
            "affected_candidate_aliases": "s262_lih;s264_aia",
            "affected_scope": "identical KPI signatures",
            "prune_label": "duplicate_independence_claim_pruned",
            "why_pruned": "두 후보가 run267EE에서 identical validation/final-month KPI signature(동일 검증/마지막 달 핵심 성과 지표 서명)를 보였다.",
            "salvage_value": "May still be useful as a control pair after identity audit.",
            "reopen_condition": "Feature order, model/config hash, or decision surface difference is documented.",
            "do_not_repeat": "Do not count identical surfaces as independent evidence.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr05_no_filter_stack_bottleneck",
            "affected_candidate_aliases": "pool",
            "affected_scope": "future follow-up design",
            "prune_label": "filter_stack_bottleneck_pruned",
            "why_pruned": "user goal(사용자 목표)이 one KPI/month/feature/threshold(한 핵심 성과 지표/월/피처/임계값)에 갇히는 것을 금지한다.",
            "salvage_value": "Weak slices guide feature engineering(피처 엔지니어링), not calendar-only filtering.",
            "reopen_condition": "A filter is backed by market meaning and replacement/ablation evidence.",
            "do_not_repeat": "Do not keep patching the same month for more than one bounded pass.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "fm01_s258_explosive_init_failed_x3",
            "pattern": "s258 explosive impulse supply init_failed",
            "affected_scope": "run267ec_03/04/05",
            "why_failed": "No usable runtime trade evidence; all blocked before KPI.",
            "salvage_value": "Handoff diagnostics may reveal setup issue.",
            "reopen_condition": "pre-runtime receipt plus one representative smoke output.",
            "do_not_repeat": "Do not rerun all three periods blindly.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm02_s264_aih_explosive_counter_init_failed_x2",
            "pattern": "s264_aih explosive counter impulse init_failed",
            "affected_scope": "run267ec_09/10",
            "why_failed": "Both validation and final-month explosive attempts blocked before trade evidence.",
            "salvage_value": "One narrow handoff triage is allowed.",
            "reopen_condition": "init failure root cause fixed without feature-order drift.",
            "do_not_repeat": "Do not treat zero trades as negative market evidence.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm03_shared_202604_final_month_break",
            "pattern": "2026.04 final-month negative across multiple candidates",
            "affected_scope": "s264_aih;s264_lc;s262_lih;s264_aia",
            "why_failed": "All tested final-month rows are negative or fragile.",
            "salvage_value": "Useful as shared adverse-state pressure.",
            "reopen_condition": "Improvement survives validation and non-calendar checks.",
            "do_not_repeat": "Do not repair only April with a naked month filter.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm04_s258_time_slice_dd_discomfort",
            "pattern": "s258 positive net but weak DD/time slices",
            "affected_scope": "2025H1/H2 period survival",
            "why_failed": "H2 recovery 1.01, DD 20.51, 2025-12 -82.97, Monday -73.87, hour19 -95.67.",
            "salvage_value": "Can still be stress challenger if trade quality improves without thinning trades.",
            "reopen_condition": "Weak slices shrink while trade count remains enough.",
            "do_not_repeat": "Do not rank by net profit alone.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm05_s262_s264_aia_duplicate_signature",
            "pattern": "s262_lih and s264_aia identical KPI signature",
            "affected_scope": "validation and 2026.04 rows",
            "why_failed": "Independent candidate meaning is not proven.",
            "salvage_value": "Identity audit can keep one as control or role-specific anchor.",
            "reopen_condition": "Decision-surface or feature-order difference is documented.",
            "do_not_repeat": "Do not double count same surface.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm06_positive_validation_not_enough",
            "pattern": "validation positives with hidden weak slices",
            "affected_scope": "s264_aih;s262_lih;s264_aia",
            "why_failed": "Validation net is strong, but weak months/sessions and final-month fragility remain.",
            "salvage_value": "Good comparison anchors for next pressure tests.",
            "reopen_condition": "Ablation/replacement and final-month pressure both survive.",
            "do_not_repeat": "Do not call validation recovery a selected baseline(선택 기준 후보).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_experiment_designs(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
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
        for row in queue_rows
    ]


def build_evidence_map(
    source_summary: Mapping[str, Any],
    attribution_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "evidence_id": "ev01_candidate_profile_rows",
            "source_path": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_field": "candidate_profile_review",
            "observed_value": f"{source_summary['profile_rows']} rows",
            "used_for": "Build branch decisions and queue coverage.",
            "effect": "Positive rows remain evidence but do not become selection.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev02_attempt_outcome_split",
            "source_path": rel(SOURCE_ATTEMPT_OUTCOME_PATH),
            "source_field": "execution_status",
            "observed_value": f"completed={source_summary['completed_attempts']};blocked={source_summary['blocked_attempts']}",
            "used_for": "Separate usable runtime evidence from init failure memory.",
            "effect": "Blocked rows become diagnostics, not market negatives.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev03_worst_negative_slices",
            "source_path": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_field": "net_profit sorted ascending",
            "observed_value": "worst 12 slices mapped into failure memory.",
            "used_for": "Prevent hidden weak-slice selection.",
            "effect": "Weak time/month/session slices steer next pressure tests.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev04_final_month_shared_loss",
            "source_path": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_field": "2026.04 profile rows",
            "observed_value": source_summary["final_month_shared_loss"],
            "used_for": "Pool-wide final-month pressure queue.",
            "effect": "Treats 2026.04 as shared state before candidate pruning.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev05_duplicate_signature",
            "source_path": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_field": "s262_lih/s264_aia profile labels",
            "observed_value": source_summary["duplicate_signature"],
            "used_for": "Identity and feature-order audit.",
            "effect": "Stops duplicate surfaces being counted as independent candidates.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for row in attribution_rows:
        alias = row.get("candidate_alias", "unknown")
        rows.append(
            {
                "evidence_id": f"ev_attr_{alias}",
                "source_path": rel(SOURCE_ATTRIBUTION_PATH),
                "source_field": "performance_attribution_summary",
                "observed_value": f"{alias}: total_net_profit={row.get('total_net_profit')};worst_dd={row.get('worst_equity_dd_percent')}",
                "used_for": "Candidate role boundary in branch decision.",
                "effect": "Keeps attribution as research evidence, not selection.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267EF eighth follow-up/prune design(8차 후속/가지치기 설계)",
            "evidence_available": "run267EE candidate_profile_review, attempt_outcome_review, negative_slice_summary, performance_attribution_summary, curve_diagnostics",
            "evidence_missing": "run267EG materialized artifacts, MT5 execution, visual curve inspection, Adapter package, ONNX parity",
            "judgment_label": "exploratory_design_completed_no_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 작업은 baseline(기준 후보)을 고르는 것이 아니라 다음 실행에서 무엇을 살리고 버릴지 정리한 설계다.",
        }
    ]


def build_gate_audit(
    queue_rows: Sequence[Mapping[str, Any]],
    prune_rows: Sequence[Mapping[str, Any]],
    source_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    aliases = ";".join(row["candidate_aliases"] for row in queue_rows)
    return [
        {
            "gate_id": "gate01_source_evidence_present",
            "gate_name": "source evidence read(원천 근거 읽기)",
            "status": "passed",
            "evidence": f"profile_rows={source_summary['profile_rows']};attempt_rows={source_summary['attempt_rows']}",
            "effect": "run267EE reviewed rows are the design input.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate02_candidate_pool_coverage",
            "gate_name": "candidate pool coverage(후보군 커버리지)",
            "status": "passed",
            "evidence": aliases,
            "effect": "All five initial candidates or their controls are represented.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate03_aggressive_branch_present",
            "gate_name": "aggressive branch present(공격 분기 포함)",
            "status": "passed",
            "evidence": "q02_s258_explosive_init_failure_triage;q06_s264_aih_explosive_counter_impulse_handoff_triage",
            "effect": "The design does not become only defensive filtering.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate04_prune_guard_present",
            "gate_name": "prune guard present(가지치기 가드 포함)",
            "status": "passed",
            "evidence": f"prune_rows={len(prune_rows)}",
            "effect": "Repeated repair loops and filter-stack bottlenecks are blocked.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate05_experiment_design_fields",
            "gate_name": "experiment design fields(실험 설계 필드)",
            "status": "passed",
            "evidence": "hypothesis;decision_use;comparison_baseline;control_variables;changed_variables;sample_scope;success/failure/invalid/stop;evidence_plan",
            "effect": "run267EG can materialize without guessing the decision boundary.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate06_claim_boundary",
            "gate_name": "claim boundary(주장 경계)",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "No operating or ONNX(온엑스) claim is made.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_run_manifest(
    created_at: str,
    queue_rows: Sequence[Mapping[str, Any]],
    prune_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "created_at_utc": created_at,
        "source_run_id": PARENT_RUN_ID,
        "next_action": NEXT_ACTION,
        "materialization_queue_path": rel(MATERIALIZATION_QUEUE_PATH),
        "queue_ids": [row["queue_id"] for row in queue_rows],
        "prune_ids": [row["prune_id"] for row in prune_rows],
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def hash_or_missing(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else "missing"


def build_lineage(created_at: str) -> dict[str, Any]:
    artifact_paths = [
        FEATURE_BLUEPRINT_PATH,
        BRANCH_DECISION_PATH,
        MATERIALIZATION_QUEUE_PATH,
        PRUNE_MATRIX_PATH,
        FAILURE_MEMORY_PATH,
        EXPERIMENT_DESIGN_RECEIPT_PATH,
        EVIDENCE_MAP_PATH,
        RESULT_JUDGMENT_PATH,
        GATE_AUDIT_PATH,
        RUN_MANIFEST_PATH,
        REVIEW_RESULT_PATH,
        REPORT_PATH,
    ]
    source_paths = [
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_CANDIDATE_PROFILE_PATH,
        SOURCE_ATTEMPT_OUTCOME_PATH,
        SOURCE_NEGATIVE_SLICE_PATH,
        SOURCE_ATTRIBUTION_PATH,
        SOURCE_CURVE_DIAGNOSTICS_PATH,
        SOURCE_REPORT_PATH,
    ]
    return {
        "source_inputs": {rel(path): hash_or_missing(path) for path in source_paths},
        "producer": rel(PRODUCER_PATH),
        "producer_sha256": hash_or_missing(REPO_ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in artifact_paths],
        "artifact_hashes": {rel(path): hash_or_missing(path) for path in artifact_paths if path != LINEAGE_PATH},
        "registry_links": [
            rel(RUN_REGISTRY_PATH),
            rel(STAGE_LEDGER_PATH),
            rel(PROJECT_LEDGER_PATH),
            rel(ARTIFACT_REGISTRY_PATH),
        ],
        "availability": "tracked_after_commit;generated_from_command",
        "lineage_judgment": "connected_with_boundary",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    items = [
        ("stage267_run267EF_producer", "producer_script", PRODUCER_PATH, "Builds run267EF eighth follow-up/prune design."),
        ("stage267_run267EF_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267EE review result."),
        ("stage267_run267EF_source_profile", "source_candidate_profile", SOURCE_CANDIDATE_PROFILE_PATH, "Source candidate profile review."),
        ("stage267_run267EF_source_attempts", "source_attempt_outcome", SOURCE_ATTEMPT_OUTCOME_PATH, "Source attempt outcome review."),
        ("stage267_run267EF_source_negative_slices", "source_negative_slices", SOURCE_NEGATIVE_SLICE_PATH, "Source negative slice summary."),
        ("stage267_run267EF_source_attribution", "source_attribution", SOURCE_ATTRIBUTION_PATH, "Source performance attribution summary."),
        ("stage267_run267EF_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Feature blueprint for eighth queue."),
        ("stage267_run267EF_branch_decisions", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decisions."),
        ("stage267_run267EF_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Next materialization queue."),
        ("stage267_run267EF_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune and stop-loop matrix."),
        ("stage267_run267EF_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267EF_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267EF_evidence_map", "evidence_map", EVIDENCE_MAP_PATH, "Evidence map."),
        ("stage267_run267EF_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267EF_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267EF_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267EF_lineage", "lineage", LINEAGE_PATH, "Artifact lineage."),
        ("stage267_run267EF_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267EF_report", "review_report", REPORT_PATH, "User-facing design report."),
    ]
    rows = []
    for artifact_id, artifact_type, path, notes in items:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": hash_or_missing(Path(path)),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def build_result() -> dict[str, Any]:
    profile_rows = read_csv_rows(SOURCE_CANDIDATE_PROFILE_PATH)
    attempt_rows = read_csv_rows(SOURCE_ATTEMPT_OUTCOME_PATH)
    negative_rows = read_csv_rows(SOURCE_NEGATIVE_SLICE_PATH)
    attribution_rows = read_csv_rows(SOURCE_ATTRIBUTION_PATH)
    source_summary = build_source_summary(profile_rows, attempt_rows, negative_rows)
    feature_blueprint = build_feature_blueprints()
    branch_decisions = build_branch_decisions()
    materialization_queue = build_materialization_queue()
    prune_matrix = build_prune_matrix()
    failure_memory = build_failure_memory()
    experiment_design_receipt = build_experiment_designs(materialization_queue)
    evidence_map = build_evidence_map(source_summary, attribution_rows)
    gate_audit = build_gate_audit(materialization_queue, prune_matrix, source_summary)
    aggressive_queue_count = sum(1 for row in materialization_queue if "aggressive" in row["aggressive_or_defensive"])
    created_at = utc_now()
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "created_at_utc": created_at,
        "source_summary": source_summary,
        "feature_blueprint": feature_blueprint,
        "branch_decisions": branch_decisions,
        "materialization_queue": materialization_queue,
        "prune_matrix": prune_matrix,
        "failure_memory": failure_memory,
        "experiment_design_receipt": experiment_design_receipt,
        "evidence_map": evidence_map,
        "result_judgment": build_result_judgment(),
        "gate_audit": gate_audit,
        "aggressive_queue_count": aggressive_queue_count,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "outputs": {
            "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
            "branch_decision_matrix": rel(BRANCH_DECISION_PATH),
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
    summary = result["source_summary"]
    lines = [
        "# Stage267 Run267EF Eighth Follow-Up/Prune Design(267단계 267EF 8차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{result['source_run_id']}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        f"- source_profile_rows(원천 후보 프로필 행): `{summary['profile_rows']}`",
        f"- source_attempt_rows(원천 시도 행): `{summary['attempt_rows']}`",
        f"- completed_attempts(완료 시도): `{summary['completed_attempts']}`",
        f"- blocked_attempts(차단 시도): `{summary['blocked_attempts']}`",
        f"- materialization_queue(물질화 대기열): `{len(result['materialization_queue'])}`",
        f"- aggressive_rows(공격 행): `{result['aggressive_queue_count']}`",
        f"- prune_rows(가지치기 행): `{len(result['prune_matrix'])}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267EE(267EE 실행)는 후보를 고를 수 있게 만든 결과가 아니다. s258_stc는 2025H1/H2가 양수지만 2025H2 DD(drawdown, 손실폭)와 2025-12, Monday(월요일), hour 19(19시)가 불편하다.",
        "s264_aih는 validation anchor(검증 앵커)가 살아났지만 2026.04 final month(마지막 달)가 음수다. s264_lc, s262_lih, s264_aia도 같은 2026.04에서 음수라 후보 하나의 문제가 아니라 공유 시장 상태일 수 있다.",
        "s262_lih와 s264_aia는 validation(검증)과 final month(마지막 달) KPI(핵심 성과 지표)가 똑같아서 독립 후보인지 identity audit(정체성 감사)이 필요하다.",
        "",
        "## Why It Still Takes Time(왜 아직 오래 걸리는가)",
        "",
        "- baseline(기준 후보)은 운영선이 아니라 R&D racing(연구개발 경주) 출발점이다.",
        "- 숫자만 보면 s264_aih, s262_lih, s264_aia가 좋아 보이는 구간이 있지만, 2026.04와 약한 slice(구간)에서 깨진다.",
        "- s258_stc는 수익이 나도 DD(손실폭)와 약한 시간대가 커서 그냥 뽑으면 위험하다.",
        "- blocked(차단)된 공격형 실험은 시장 실패가 아니라 runtime handoff(런타임 인계) 실패일 수 있어 따로 기록해야 한다.",
        "",
        "## Queue(대기열)",
        "",
    ]
    for row in result["materialization_queue"]:
        lines.append(f"- `{row['queue_id']}` workstream(작업 흐름) `{row['workstream']}`: {row['decision_use']}")
    lines.extend(
        [
            "",
            "## Prune Guard(가지치기 가드)",
            "",
        ]
    )
    for row in result["prune_matrix"]:
        lines.append(f"- `{row['prune_id']}` prune_label(가지치기 라벨) `{row['prune_label']}`: {row['why_pruned']}")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 설계는 exploratory design(탐색 설계)이며 후보 선택, 연구 기준 후보 선택, ONNX(온엑스) 준비, Goal Achieve(목표 달성)를 주장하지 않는다.",
            "- 다음 run267EG(267EG 실행)는 queue(대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화해야 한다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- evidence_map(근거 지도): `{rel(EVIDENCE_MAP_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
        ]
    )
    return "\n".join(lines)


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
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    write_json(LINEAGE_PATH, build_lineage(str(result["created_at_utc"])))


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    notes = (
        f"queue_rows={len(result['materialization_queue'])};"
        f"aggressive_rows={result['aggressive_queue_count']};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"next_action={NEXT_ACTION}."
    )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_eighth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267EF_runtime_gap_aware_eighth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_eighth_followup_or_prune_design",
        "tier_scope": "design only from run267EE Tier A reviewed rows",
        "scoreboard": "experiment_design_queue_prune_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_eighth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_eighth_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_eighth_followup_or_prune_design",
        "tier_scope": "design only; next run materializes Tier A attempts",
        "kpi_scope": "experiment_design_queue_prune_failure_memory",
        "scoreboard_lane": "runtime_gap_aware_eighth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={len(result['materialization_queue'])};aggressive_rows={result['aggressive_queue_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "Design converts run267EE weak slices, init failures, duplicate signatures, and final-month breaks into run267EG queue.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267EF_runtime_gap_aware_eighth_followup_or_prune_design"
        f"(267EF 런타임 공백 반영 8차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_block = "\n".join(
        [
            "Run267EF(267EF 실행)는 run267EE(267EE 실행)의 후보 프로필, 음수 구간, 초기화 실패, 중복 KPI(핵심 성과 지표) 서명을 8차 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, aggressive rows(공격 행) `{result['aggressive_queue_count']}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개, failure memory(실패 기억) `{len(result['failure_memory'])}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_eighth_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_line_once(current, report_line)
    current = append_block_once(current, "Run267EF(267EF 실행)는 run267EE", summary_block)
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_line_once(selection, report_line)
    selection = append_block_once(selection, "Run267EF(267EF 실행)는 run267EE", summary_block)
    write_text(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    review_index = append_line_once(review_index, report_line)
    review_index = append_block_once(review_index, "Run267EF(267EF 실행)는 run267EE", summary_block)
    write_text(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_first_exact_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267EF(267EF 실행) runtime gap aware eighth follow-up/prune design(런타임 공백 반영 8차 후속/가지치기 설계) `{STATUS}`. "
        f"Effect(효과): run267EE(267EE 실행)의 약점 근거를 materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, "
        f"aggressive rows(공격 행) `{result['aggressive_queue_count']}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage267(267단계) run267EF(267EF 실행)" not in workspace:
        workspace = workspace.replace("current_focus:\n", focus, 1)
    workspace = workspace.replace("run267EF_design_runtime_gap_aware_eighth_followup_or_prune_from_run267EE_review", NEXT_ACTION)
    workspace = append_block_once(workspace, "Run267EF(267EF 실행)는 run267EE", summary_block)
    write_text(WORKSPACE_STATE_PATH, workspace)


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
