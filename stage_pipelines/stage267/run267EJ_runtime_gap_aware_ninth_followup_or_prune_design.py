from __future__ import annotations

import csv
import json
import re
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
    run267EI_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267EJ"
RUN_ID = "run267EJ_stage267_runtime_gap_aware_ninth_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267EJ_runtime_gap_aware_ninth_followup_or_prune_design_completed"
JUDGMENT = "runtime_gap_aware_ninth_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267EK_materialize_runtime_gap_aware_ninth_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_ninth_followup_or_prune_design"

SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_INIT_FAILURE_PATH = source_review.INIT_FAILURE_SUMMARY_PATH
SOURCE_FOLLOWUP_QUEUE_PATH = source_review.FOLLOWUP_DECISION_QUEUE_PATH

FEATURE_BLUEPRINT_PATH = RUN_ROOT / "feature_engineering_blueprint.csv"
BRANCH_DECISION_PATH = RUN_ROOT / "branch_decision_matrix.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
HANDOFF_TRIAGE_PATH = RUN_ROOT / "runtime_handoff_triage_plan.csv"
IDENTITY_AUDIT_PATH = RUN_ROOT / "identity_audit_plan.csv"
AGGRESSIVE_REENTRY_PATH = RUN_ROOT / "aggressive_reentry_plan.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
EVIDENCE_MAP_PATH = RUN_ROOT / "evidence_map.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267EJ_runtime_gap_aware_ninth_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267EJ_runtime_gap_aware_ninth_followup_or_prune_design.py")

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
    "feature_family",
    "market_meaning",
    "source_evidence",
    "changed_variables",
    "held_variables",
    "materialization_use",
    "success_read",
    "failure_read",
    "claim_boundary",
)

BRANCH_DECISION_COLUMNS = (
    "decision_id",
    "candidate_aliases",
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
    "source_queue_id",
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

TRIAGE_COLUMNS = (
    "triage_id",
    "candidate_aliases",
    "source_gap",
    "precheck",
    "success_read",
    "failure_read",
    "max_repair_span",
    "claim_boundary",
)

IDENTITY_COLUMNS = (
    "audit_id",
    "candidate_aliases",
    "identity_question",
    "required_receipts",
    "success_read",
    "failure_read",
    "claim_boundary",
)

AGGRESSIVE_COLUMNS = (
    "aggressive_id",
    "candidate_aliases",
    "entry_condition",
    "experiment_shape",
    "not_allowed",
    "success_read",
    "failure_read",
    "claim_boundary",
)

PRUNE_COLUMNS = (
    "prune_id",
    "affected_candidate_aliases",
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


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def clean(value: str) -> str:
    return value.strip().strip("`").strip()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column, "")) for column in columns})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


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


def parse_source_report() -> dict[str, Any]:
    text = read_text(SOURCE_REPORT_PATH)
    candidate_rows: list[dict[str, Any]] = []
    followup_rows: list[dict[str, str]] = []
    init_gap_rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if line.startswith("| `"):
            parts = [clean(part) for part in line.strip().strip("|").split("|")]
            if len(parts) >= 8:
                weakest = parts[6]
                weak_bucket, _, weak_net = weakest.partition("=")
                candidate_rows.append(
                    {
                        "candidate_alias": parts[0],
                        "profile_label": parts[1],
                        "net_profit": as_float(parts[2]),
                        "profit_factor": as_float(parts[3]),
                        "trade_count": int(as_float(parts[4])),
                        "dd_percent": as_float(parts[5]),
                        "weakest_bucket": weak_bucket,
                        "weakest_net": as_float(weak_net),
                        "read": parts[7],
                    }
                )
        if line.startswith("- `q"):
            match = re.match(r"- `([^`]+)` `([^`]+)` `([^`]+)`: (.+)", line)
            if match:
                followup_rows.append(
                    {
                        "queue_id": match.group(1),
                        "priority": match.group(2),
                        "candidate_aliases": match.group(3),
                        "decision_use": match.group(4),
                    }
                )
        if line.startswith("- `s") and "blocked_attempts" in line:
            match = re.match(r"- `([^`]+)` `([^`]+)` `([^`]+)`: blocked_attempts.*`(\d+)`\. (.+)", line)
            if match:
                init_gap_rows.append(
                    {
                        "candidate_alias": match.group(1),
                        "queue_id": match.group(2),
                        "attempt_role": match.group(3),
                        "blocked_attempts": match.group(4),
                        "read": match.group(5),
                    }
                )
    summary: dict[str, Any] = {
        "source_report": rel(SOURCE_REPORT_PATH),
        "candidate_rows": candidate_rows,
        "followup_rows": followup_rows,
        "init_gap_rows": init_gap_rows,
        "candidate_profile_rows": len(candidate_rows),
        "followup_queue_rows": len(followup_rows),
        "init_gap_rows_count": len(init_gap_rows),
        "negative_profile_rows": sum(1 for row in candidate_rows if row["net_profit"] < 0.0),
        "positive_low_pf_rows": sum(1 for row in candidate_rows if "positive_low_pf" in str(row["read"])),
        "parser_source": "tracked_markdown_report_fallback",
    }
    return summary


def build_feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "fb01_runtime_handoff_integrity_precheck",
            "candidate_aliases": "s258_stc;s264_aih",
            "feature_family": "runtime_handoff_integrity",
            "market_meaning": "시장 신호가 아니라 파일 인계, 초기화, 출력 공백이 성능 판독을 막는지 먼저 분리한다.",
            "source_evidence": "run267EI init/runtime gap(초기화/런타임 공백) 6개.",
            "changed_variables": "handoff file presence, set/ini path validity, timeout/deinit reason capture, one representative smoke after precheck.",
            "held_variables": "candidate identity(후보 정체성), feature order(피처 순서), risk/ATR handoff(위험/ATR 인계), MT5 tester harness(MetaTrader 5 테스터 장치).",
            "materialization_use": "run267EK(267EK 실행)에서 전체 재실행 전 precheck receipt(사전검사 영수증)를 만들게 한다.",
            "success_read": "blocked gap(차단 공백)이 원인별로 분류되고 최소 하나의 대표 시도가 runtime output(런타임 출력)까지 간다.",
            "failure_read": "같은 init failure(초기화 실패)가 반복되면 해당 공격 분기는 failure memory(실패 기억)로 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb02_202604_shared_adverse_state",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "feature_family": "shared_adverse_state_feature_engineering",
            "market_meaning": "2026.04가 후보별 임계값 문제가 아니라 공유 불리 상태인지 본다.",
            "source_evidence": "run267EI에서 네 후보/대조 표면이 2026.04 measured slice(측정 구간)에서 모두 음수.",
            "changed_variables": "sell-pressure state(매도 압박 상태), counter-impulse exhaustion(역임펄스 소진), ATR regime transition(ATR 체제 전환), no naked month filter(날것 월 필터 없음).",
            "held_variables": "date scope(기간 범위), candidate surfaces(후보 표면), execution harness(실행 장치).",
            "materialization_use": "same-month filter(같은 월 필터)가 아니라 구조 피처 피벗으로 물질화한다.",
            "success_read": "거래 수를 숨기지 않고 2026.04 손실이 완화되며 validation(검증) 양수 표면을 망치지 않는다.",
            "failure_read": "개선이 달력/시간 금지로만 나오거나 모든 후보가 계속 비슷하게 음수면 구조 피벗을 더 크게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb03_duplicate_signature_identity_receipt",
            "candidate_aliases": "s262_lih;s264_aia",
            "feature_family": "identity_and_feature_order_audit",
            "market_meaning": "두 후보가 서로 다른 시장 의미를 잡은 것인지, 같은 표면을 다른 이름으로 본 것인지 확인한다.",
            "source_evidence": "run267EI validation identity audit(검증 정체성 감사)에서 두 후보가 net/PF/trades/DD와 worst month가 동일.",
            "changed_variables": "feature order hash(피처 순서 해시), model/bundle hash(모델/번들 해시), route label(라우팅 라벨), decision surface signature(결정 표면 서명).",
            "held_variables": "validation and 2026.04 scopes(검증 및 2026.04 범위), no candidate selection(후보 선택 없음).",
            "materialization_use": "독립 후보 주장 전 정체성 영수증을 만들게 한다.",
            "success_read": "분리 가능한 hash/signature(해시/서명) 차이가 기록된다.",
            "failure_read": "같은 표면이면 한쪽을 duplicate control(중복 대조)로 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb04_aggressive_non_filter_reentry",
            "candidate_aliases": "s258_stc;s264_aih",
            "feature_family": "aggressive_non_filter_experiment",
            "market_meaning": "방어 필터 누적으로만 연구가 굳지 않도록, 인계 수리 뒤 공격형 비필터 실험을 한 번 연다.",
            "source_evidence": "run267EI q05 aggressive experiment after handoff fix(인계 수리 뒤 공격형 실험) 대기열.",
            "changed_variables": "entry impulse intensity(진입 임펄스 강도), adverse-state confirmation(불리 상태 확인), no calendar-only suppression(달력만 억제 없음).",
            "held_variables": "precheck pass(사전검사 통과), feature order(피처 순서), risk guard(위험 가드).",
            "materialization_use": "runtime handoff(런타임 인계)가 회복된 경우에만 대표 공격 실험 1회를 물질화한다.",
            "success_read": "얇은 필터가 아니라 거래 품질과 곡선 형태가 함께 개선된다.",
            "failure_read": "거래 수가 지나치게 줄거나 DD(손실폭)가 튀면 공격 분기는 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_decisions() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "bd01_s258_runtime_gap_before_stress_judgment",
            "candidate_aliases": "s258_stc",
            "branch_decision": "keep_as_stress_challenger_only_after_handoff_triage",
            "why": "run267EI에서 s258_stc는 전부 runtime output(런타임 출력) 전에 막혀 성능 실패인지 판정할 수 없다.",
            "next_use": "P0 handoff triage(인계 진단) 후 aggressive branch(공격 분기)를 한 번만 재개한다.",
            "reopen_condition": "대표 시도가 trade list(거래 목록)와 curve diagnostics(곡선 진단)를 만든다.",
            "stop_condition": "동일 init/runtime gap(초기화/런타임 공백)이 반복되면 한 repair loop(수리 루프) 안에서 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd02_s264_aih_watch_not_core_selection",
            "candidate_aliases": "s264_aih;s264_lc",
            "branch_decision": "watch_core_challenger_but_no_baseline_selection",
            "why": "validation(검증)은 양수지만 PF(수익 팩터)가 낮고 2026.04 measured slice(측정 구간)에서 깨졌다.",
            "next_use": "s264_lc를 defensive control(방어 대조)로 두고 공유 2026.04 상태와 aggressive handoff(공격형 인계)를 분리한다.",
            "reopen_condition": "validation 손상 없이 2026.04와 약한 구간이 동시에 완화된다.",
            "stop_condition": "같은 마지막 월 수리가 반복되면 feature structure(피처 구조) 피벗으로 전환한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd03_s262_s264_aia_identity_first",
            "candidate_aliases": "s262_lih;s264_aia",
            "branch_decision": "hold_independent_role_until_signature_audit",
            "why": "두 후보의 validation identity audit(검증 정체성 감사) 행이 동일한 KPI(핵심 성과 지표) 서명을 보였다.",
            "next_use": "feature order/model hash/route label(피처 순서/모델 해시/라우팅 라벨)을 확인한다.",
            "reopen_condition": "결정 표면 차이가 증명되면 validation-heavy(검증 중심)와 OOS anchor(표본외 앵커) 역할을 다시 분리한다.",
            "stop_condition": "동일 표면이면 독립 후보 주장 금지.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd04_pool_no_filter_stack",
            "candidate_aliases": "pool",
            "branch_decision": "pivot_from_same_month_filtering_to_structure",
            "why": "run267EI follow-up queue(후속 대기열)가 같은 월 필터 반복이 아니라 구조/피처 엔지니어링을 요구한다.",
            "next_use": "2026.04 공유 취약성은 feature engineering(피처 엔지니어링) 질문으로 물질화한다.",
            "reopen_condition": "시장 의미가 있는 피처가 ablation/replacement(제거/대체)에서 버틸 때.",
            "stop_condition": "달력/시간 필터만 추가하는 설계는 가지치기한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "q01_runtime_handoff_gap_bounded_precheck",
            "priority": "P0",
            "candidate_aliases": "s258_stc;s264_aih",
            "candidate_ids": "s258_short_tight_control;s264_allow_inner_high_quarter",
            "workstream": "runtime_handoff_gap_triage",
            "source_queue_id": "run267EI:q01_runtime_handoff_gap_bounded_triage",
            "hypothesis": "The blocked rows are handoff/runtime failures, not proven market failures.",
            "decision_use": "Decide whether s258_stc and s264_aih aggressive branches can be tested, or should be pruned as unrecoverable handoff gaps.",
            "comparison_baseline": "run267EI six init/runtime gap rows.",
            "control_variables": "candidate identity;feature order;risk/ATR handoff;MT5 tester harness;no parameter drift.",
            "changed_variables": "handoff precheck;path validity;init log capture;single representative smoke after precheck.",
            "sample_scope": "s258_stc 2025H1/2025H2 survival and explosive roles; s264_aih validation/final-month explosive roles.",
            "success_criteria": "All gaps are classified and at least one representative blocked branch reaches runtime output.",
            "failure_criteria": "The same init_failed/runtime output gap repeats or root cause is still unknown.",
            "invalid_conditions": "Feature order drift, silent set/ini change, zero-trade report treated as success, or missing log.",
            "stop_conditions": "Maximum one bounded repair pass before prune/hold decision.",
            "evidence_plan": "handoff receipt, setup diff, init log, execution_result, optional MT5 report, artifact lineage.",
            "runtime_instruction": "Run precheck first; do not full-rerun blocked attempts until precheck passes.",
            "aggressive_or_defensive": "diagnostic_precheck",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_202604_shared_state_feature_pivot",
            "priority": "P0",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "candidate_ids": "s264_allow_inner_high_quarter;s264_lowrank_control;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "workstream": "shared_adverse_state_feature_engineering",
            "source_queue_id": "run267EI:q02_202604_shared_sell_fragility_pivot",
            "hypothesis": "2026.04 weakness is a shared adverse state that needs structural feature treatment, not another same-month filter.",
            "decision_use": "Decide whether to pivot into shared-state feature engineering or prune repeated final-month repair loops.",
            "comparison_baseline": "run267EI 2026.04 measured-slice rows across four candidates/controls.",
            "control_variables": "same date scope;candidate surfaces;MT5 harness;no naked calendar exclusion.",
            "changed_variables": "sell-pressure state;counter-impulse exhaustion;ATR regime transition;directional adverse-state grouping.",
            "sample_scope": "2026-04 final OOS segment plus validation rows for damage check.",
            "success_criteria": "Losses shrink without hiding trades and validation rows remain structurally intact.",
            "failure_criteria": "All candidates remain negative, or improvement comes only from trade removal/calendar filtering.",
            "invalid_conditions": "Changed date scope, missing controls, duplicate surfaces not disclosed, or parser mismatch.",
            "stop_conditions": "If this fails, stop same-month repair and move to broader feature-structure branch.",
            "evidence_plan": "paired MT5 reports, curve diagnostics, time-slice KPI, trade quality, negative-slice summary.",
            "runtime_instruction": "Materialize as pool-wide pressure, not candidate selection.",
            "aggressive_or_defensive": "structural_pivot",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s262_s264_aia_signature_identity_audit",
            "priority": "P1",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": "s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "workstream": "identity_surface_audit",
            "source_queue_id": "run267EI:q03_s262_s264_aia_signature_collapse_audit",
            "hypothesis": "The two candidates may be the same decision surface or handoff path under different labels.",
            "decision_use": "Decide whether both remain role-separated candidates or one becomes duplicate control.",
            "comparison_baseline": "run267EI identical validation identity audit rows.",
            "control_variables": "same validation and 2026.04 scopes;same feature contract;no selection claim.",
            "changed_variables": "feature order hash;model/bundle hash;route label;decision surface signature.",
            "sample_scope": "s262_lih and s264_aia validation and final-month evidence.",
            "success_criteria": "Meaningful feature/model/route difference is documented.",
            "failure_criteria": "Hashes and signatures collapse to the same surface.",
            "invalid_conditions": "Missing hash receipts or unverifiable route labels.",
            "stop_conditions": "Do not count the pair as independent evidence until audit passes.",
            "evidence_plan": "feature order receipt, model/bundle hashes, route labels, lineage map.",
            "runtime_instruction": "Diagnostic only; MT5 rerun only if hash receipts require reproduction.",
            "aggressive_or_defensive": "diagnostic",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_validation_low_pf_wide_period_watch",
            "priority": "P1",
            "candidate_aliases": "s264_aih;s262_lih;s264_aia",
            "candidate_ids": "s264_allow_inner_high_quarter;s262_lowrank_inner_half_filter;s264_allow_inner_all_oos_anchor",
            "workstream": "validation_positive_low_pf_watch",
            "source_queue_id": "run267EI:q04_validation_positive_low_pf_watch",
            "hypothesis": "Positive validation rows are useful anchors but not strong enough for baseline selection without broader period stability.",
            "decision_use": "Keep these rows as watch anchors for comparison, not as selected research baseline.",
            "comparison_baseline": "run267EI positive validation rows with PF about 1.21.",
            "control_variables": "candidate identity;validation scope;no ONNX;no selected baseline.",
            "changed_variables": "add 2024/weak-month adjacency lens and balance/equity shape gate before any Adapter escalation.",
            "sample_scope": "validation rows plus prior weak months and final OOS segment references.",
            "success_criteria": "Positive rows remain positive while weak months and final OOS do not show deep holes.",
            "failure_criteria": "PF stays thin, weak months deepen, or trade quality concentrates.",
            "invalid_conditions": "Only headline net/PF is used or visual curve inspection is missing.",
            "stop_conditions": "No Adapter escalation from these rows until curve and period evidence improves.",
            "evidence_plan": "curve diagnostics, weak-month table, trade quality, 2024/adjacent-period comparison.",
            "runtime_instruction": "Design as watch/anchor evidence; no standalone selection run.",
            "aggressive_or_defensive": "watch_guardrail",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q05_aggressive_non_filter_reentry_after_precheck",
            "priority": "P2_aggressive",
            "candidate_aliases": "s258_stc;s264_aih",
            "candidate_ids": "s258_short_tight_control;s264_allow_inner_high_quarter",
            "workstream": "aggressive_non_filter_reentry",
            "source_queue_id": "run267EI:q05_aggressive_experiment_after_handoff_fix",
            "hypothesis": "A bounded aggressive, non-filter experiment is needed after handoff recovery to avoid defensive-only research.",
            "decision_use": "Decide whether an aggressive impulse branch can improve trade quality without calendar/filter stacking.",
            "comparison_baseline": "run267EI blocked aggressive rows and previous defensive repairs.",
            "control_variables": "handoff precheck must pass;feature order;risk guard;no calendar-only suppression.",
            "changed_variables": "entry impulse intensity;adverse-state confirmation;trade-quality gate.",
            "sample_scope": "one representative recovered aggressive branch, then validation/final-month comparison if usable.",
            "success_criteria": "Trade count remains meaningful, DD is not worse, and curve shape improves without thin filtering.",
            "failure_criteria": "DD spikes, trade count collapses, or result depends on narrow filter removal.",
            "invalid_conditions": "Precheck failed, missing runtime output, or risk settings drift.",
            "stop_conditions": "Only one aggressive branch after precheck; prune if it repeats the same failure.",
            "evidence_plan": "precheck receipt, MT5 report, trade_records, curve diagnostics, trade-quality review.",
            "runtime_instruction": "Materialize only after q01 passes.",
            "aggressive_or_defensive": "aggressive_non_filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_handoff_triage() -> list[dict[str, Any]]:
    return [
        {
            "triage_id": "ht01_s258_gap_classification",
            "candidate_aliases": "s258_stc",
            "source_gap": "survival_quality_recheck and explosive_handoff rows blocked before runtime output.",
            "precheck": "Verify set/ini path, feature bundle presence, tester profile, output directory, init/deinit reason.",
            "success_read": "One representative s258 attempt produces a tester report and runtime output.",
            "failure_read": "Same init/runtime gap repeats and branch is held/pruned.",
            "max_repair_span": "one design plus one materialized precheck pass",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "triage_id": "ht02_s264_aih_explosive_gap_classification",
            "candidate_aliases": "s264_aih",
            "source_gap": "validation and final-month explosive handoff triage rows blocked.",
            "precheck": "Verify aggressive branch handoff file, feature order, model route label, terminal output path.",
            "success_read": "One representative s264_aih aggressive attempt reaches runtime output.",
            "failure_read": "Aggressive branch closes as failure memory, not market performance evidence.",
            "max_repair_span": "one design plus one materialized precheck pass",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_identity_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ia01_s262_s264_aia_feature_order_model_hash",
            "candidate_aliases": "s262_lih;s264_aia",
            "identity_question": "Are these two candidates genuinely different surfaces or duplicate handoff/model routes?",
            "required_receipts": "feature_order_hash;model_bundle_hash;candidate_config_hash;route_label;decision_surface_signature",
            "success_read": "Receipts show a meaningful surface difference and explain identical KPI.",
            "failure_read": "Receipts collapse to the same surface, so independent candidate claim is blocked.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_aggressive_reentry() -> list[dict[str, Any]]:
    return [
        {
            "aggressive_id": "ag01_s258_or_s264_one_representative_non_filter",
            "candidate_aliases": "s258_stc;s264_aih",
            "entry_condition": "q01_runtime_handoff_gap_bounded_precheck passes for at least one aggressive branch.",
            "experiment_shape": "one representative recovered branch; no naked month/hour/session filter; compare curve/trade quality.",
            "not_allowed": "full rerun of all blocked attempts; defensive filter stacking; headline-profit selection.",
            "success_read": "Meaningful trade count, improved curve quality, no DD spike, no thin filtering.",
            "failure_read": "DD/trade collapse or handoff gap repeats, then branch is pruned.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "pr01_no_baseline_selection_from_low_pf_validation",
            "affected_candidate_aliases": "s264_aih;s262_lih;s264_aia",
            "prune_label": "low_pf_validation_selection_pruned",
            "why_pruned": "Positive validation rows have PF(수익 팩터) around 1.21 and weak-month/final-month questions remain.",
            "salvage_value": "Keep as watch anchors for comparison.",
            "reopen_condition": "Broader periods, curve shape, and trade quality improve together.",
            "do_not_repeat": "Do not select by positive validation net alone.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr02_no_same_month_filter_stack",
            "affected_candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "prune_label": "same_month_filter_stack_pruned",
            "why_pruned": "2026.04 weakness is shared and should become structural feature work, not a naked April filter.",
            "salvage_value": "Use 2026.04 as adverse-state pressure evidence.",
            "reopen_condition": "A market-meaning feature survives validation and adjacent-period checks.",
            "do_not_repeat": "Do not keep adding calendar/hour filters.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr03_no_duplicate_independent_counting",
            "affected_candidate_aliases": "s262_lih;s264_aia",
            "prune_label": "duplicate_signature_independence_pruned",
            "why_pruned": "Identical KPI signatures are not independent evidence until identity audit passes.",
            "salvage_value": "One can remain a control if duplicate surface is confirmed.",
            "reopen_condition": "Feature/model/route receipts show distinct surfaces.",
            "do_not_repeat": "Do not double-count identical surfaces.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr04_no_raw_aggressive_rerun_without_precheck",
            "affected_candidate_aliases": "s258_stc;s264_aih",
            "prune_label": "raw_aggressive_rerun_pruned",
            "why_pruned": "Blocked aggressive rows need handoff classification before performance judgment.",
            "salvage_value": "A single non-filter aggressive attempt is allowed after precheck.",
            "reopen_condition": "Handoff receipt passes and runtime output is recoverable.",
            "do_not_repeat": "Do not rerun all blocked attempts blindly.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "fm01_run267EI_s258_all_runtime_outputs_blocked",
            "pattern": "s258_stc runtime output gap before performance evidence",
            "affected_scope": "q01 and q02 blocked roles",
            "why_failed": "No usable trade evidence reached runtime output.",
            "salvage_value": "Handoff triage may recover one representative aggressive branch.",
            "reopen_condition": "precheck receipt and runtime output are produced.",
            "do_not_repeat": "Do not treat as market-negative until runtime gap is classified.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm02_run267EI_202604_shared_negative",
            "pattern": "2026.04 measured-slice negative across pool surfaces",
            "affected_scope": "s264_aih;s264_lc;s262_lih;s264_aia",
            "why_failed": "All measured final-month rows are negative or fragile.",
            "salvage_value": "Useful as shared adverse-state feature engineering target.",
            "reopen_condition": "Structural feature reduces loss without hiding trades.",
            "do_not_repeat": "Do not solve only with month filtering.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm03_run267EI_s262_s264_aia_duplicate_validation",
            "pattern": "s262_lih and s264_aia identical validation signature",
            "affected_scope": "validation identity audit rows",
            "why_failed": "Independent role is unproven.",
            "salvage_value": "Identity audit can keep role distinction if receipts differ.",
            "reopen_condition": "feature/model/route receipts differ.",
            "do_not_repeat": "Do not count both as independent candidates before audit.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm04_run267EI_low_pf_positive_watch",
            "pattern": "positive validation rows with low PF and weak-month holes",
            "affected_scope": "s264_aih;s262_lih;s264_aia",
            "why_failed": "Positive but not robust enough for baseline selection.",
            "salvage_value": "Use as watch anchors for future pressure tests.",
            "reopen_condition": "balance/equity curve and wider periods become cleaner.",
            "do_not_repeat": "Do not jump from positive validation to ONNX(온엑스).",
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


def build_evidence_map(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "ev01_tracked_source_report",
            "source_path": rel(SOURCE_REPORT_PATH),
            "source_field": "report body",
            "observed_value": "tracked markdown report parsed",
            "used_for": "Clean-checkout recoverability.",
            "effect": "run267EJ does not require ignored 02_runs CSV to design next queue.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev02_candidate_profile_table",
            "source_path": rel(SOURCE_REPORT_PATH),
            "source_field": "Candidate Profile",
            "observed_value": f"rows={summary['candidate_profile_rows']};negative_rows={summary['negative_profile_rows']};positive_low_pf_rows={summary['positive_low_pf_rows']}",
            "used_for": "Branch decisions and prune guard.",
            "effect": "Positive rows remain watch anchors; negative rows steer structural pressure.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev03_init_runtime_gaps",
            "source_path": rel(SOURCE_REPORT_PATH),
            "source_field": "Init/Runtime Gaps",
            "observed_value": f"gap_rows={summary['init_gap_rows_count']}",
            "used_for": "Handoff triage plan.",
            "effect": "Blocked rows are not treated as market performance failures.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev04_followup_queue",
            "source_path": rel(SOURCE_REPORT_PATH),
            "source_field": "Follow-Up Queue",
            "observed_value": f"queue_rows={summary['followup_queue_rows']}",
            "used_for": "Materialization queue design.",
            "effect": "The next pass includes handoff, shared-state, identity, watch, and aggressive branches.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267EJ ninth follow-up/prune design(267EJ 9차 후속/가지치기 설계)",
            "evidence_available": "tracked run267EI report, candidate profile table, init/runtime gap list, follow-up queue, branch/prune/experiment-design outputs",
            "evidence_missing": "run267EK materialization, MT5 execution, visual curve inspection, Adapter package, ONNX parity",
            "judgment_label": "exploratory_design_completed_no_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 설계는 후보를 고르는 일이 아니라, 런타임 공백과 구조 약점을 분리해 다음 실행 대기열로 바꾸는 일이다.",
        }
    ]


def build_gate_audit(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "gate01_source_report_available",
            "gate_name": "source report available(원천 보고서 존재)",
            "status": "passed" if path_exists(SOURCE_REPORT_PATH) else "failed",
            "evidence": rel(SOURCE_REPORT_PATH),
            "effect": "Design can be regenerated from tracked evidence.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate02_candidate_pool_coverage",
            "gate_name": "candidate pool coverage(후보군 커버리지)",
            "status": "passed",
            "evidence": "s258_stc;s264_aih;s264_lc;s262_lih;s264_aia",
            "effect": "All five baseline candidate roles are represented through direct or control branches.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate03_runtime_gap_not_market_failure",
            "gate_name": "runtime gap separation(런타임 공백 분리)",
            "status": "passed",
            "evidence": "q01_runtime_handoff_gap_bounded_precheck",
            "effect": "Blocked attempts are triaged before performance judgment.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate04_aggressive_branch_present",
            "gate_name": "aggressive branch present(공격 분기 포함)",
            "status": "passed",
            "evidence": "q05_aggressive_non_filter_reentry_after_precheck",
            "effect": "Research does not become defensive filter-only work.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate05_no_filter_stack_guard",
            "gate_name": "no filter stack guard(필터 누적 방지)",
            "status": "passed",
            "evidence": f"prune_rows={len(result['prune_matrix'])}",
            "effect": "Same-month and headline-profit shortcuts are blocked.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate06_claim_boundary",
            "gate_name": "claim boundary(주장 경계)",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "No ONNX(온엑스), runtime authority(런타임 권위), or operating claim(운영 주장) is made.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_run_manifest(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "created_at_utc": created_at,
        "source_run_id": PARENT_RUN_ID,
        "source_report": rel(SOURCE_REPORT_PATH),
        "next_action": NEXT_ACTION,
        "queue_ids": [row["queue_id"] for row in result["materialization_queue"]],
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
        HANDOFF_TRIAGE_PATH,
        IDENTITY_AUDIT_PATH,
        AGGRESSIVE_REENTRY_PATH,
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
        SOURCE_REPORT_PATH,
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_CANDIDATE_PROFILE_PATH,
        SOURCE_INIT_FAILURE_PATH,
        SOURCE_FOLLOWUP_QUEUE_PATH,
    ]
    return {
        "source_inputs": {rel(path): hash_or_missing(path) for path in source_paths},
        "producer": rel(PRODUCER_PATH),
        "producer_sha256": hash_or_missing(REPO_ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in artifact_paths],
        "artifact_hashes": {rel(path): hash_or_missing(path) for path in artifact_paths if path != LINEAGE_PATH},
        "lineage_judgment": "connected_from_tracked_report_with_ignored_artifact_fallback",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    items = [
        ("stage267_run267EJ_producer", "producer_script", PRODUCER_PATH, "Builds run267EJ ninth follow-up/prune design."),
        ("stage267_run267EJ_source_report", "source_report", SOURCE_REPORT_PATH, "Tracked run267EI source report."),
        ("stage267_run267EJ_feature_blueprint", "feature_engineering_blueprint", FEATURE_BLUEPRINT_PATH, "Feature engineering blueprint."),
        ("stage267_run267EJ_branch_decisions", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decisions."),
        ("stage267_run267EJ_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Next materialization queue."),
        ("stage267_run267EJ_handoff_triage", "runtime_handoff_triage_plan", HANDOFF_TRIAGE_PATH, "Runtime handoff triage plan."),
        ("stage267_run267EJ_identity_audit", "identity_audit_plan", IDENTITY_AUDIT_PATH, "Identity audit plan."),
        ("stage267_run267EJ_aggressive_reentry", "aggressive_reentry_plan", AGGRESSIVE_REENTRY_PATH, "Aggressive reentry plan."),
        ("stage267_run267EJ_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune matrix."),
        ("stage267_run267EJ_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267EJ_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267EJ_evidence_map", "evidence_map", EVIDENCE_MAP_PATH, "Evidence map."),
        ("stage267_run267EJ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267EJ_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267EJ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267EJ_lineage", "lineage", LINEAGE_PATH, "Artifact lineage."),
        ("stage267_run267EJ_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267EJ_report", "review_report", REPORT_PATH, "User-facing design report."),
    ]
    return [
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
        for artifact_id, artifact_type, path, notes in items
    ]


def build_result() -> dict[str, Any]:
    summary = parse_source_report()
    queue = build_materialization_queue()
    result: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "created_at_utc": utc_now(),
        "source_summary": summary,
        "feature_blueprint": build_feature_blueprints(),
        "branch_decisions": build_branch_decisions(),
        "materialization_queue": queue,
        "handoff_triage_plan": build_handoff_triage(),
        "identity_audit_plan": build_identity_audit(),
        "aggressive_reentry_plan": build_aggressive_reentry(),
        "prune_matrix": build_prune_matrix(),
        "failure_memory": build_failure_memory(),
        "experiment_design_receipt": build_experiment_designs(queue),
        "evidence_map": build_evidence_map(summary),
        "result_judgment": build_result_judgment(),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    result["gate_audit"] = build_gate_audit(result)
    result["aggressive_queue_count"] = sum(1 for row in queue if "aggressive" in row["aggressive_or_defensive"])
    result["outputs"] = {
        "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
        "branch_decision_matrix": rel(BRANCH_DECISION_PATH),
        "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
        "handoff_triage_plan": rel(HANDOFF_TRIAGE_PATH),
        "identity_audit_plan": rel(IDENTITY_AUDIT_PATH),
        "aggressive_reentry_plan": rel(AGGRESSIVE_REENTRY_PATH),
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
    }
    return result


def report_markdown(result: Mapping[str, Any]) -> str:
    summary = result["source_summary"]

    queue_reads = {
        "q01_runtime_handoff_gap_bounded_precheck": "handoff gap(인계 공백)이 고칠 수 있는 실행 문제인지 먼저 분류하고, 고칠 수 없으면 가지치기한다.",
        "q02_202604_shared_state_feature_pivot": "2026.04 shared state(공유 상태)를 같은 월 필터가 아니라 structural feature engineering(구조적 피처 엔지니어링) 질문으로 바꾼다.",
        "q03_s262_s264_aia_signature_identity_audit": "duplicate signature(중복 서명)가 실제 동일 표면인지 audit(감사)한 뒤 후보 역할을 다시 나눈다.",
        "q04_validation_low_pf_wide_period_watch": "positive validation(양수 검증) 행은 watch anchor(관찰 기준점)로만 두고 selected baseline(선택 기준 후보)으로 쓰지 않는다.",
        "q05_aggressive_non_filter_reentry_after_precheck": "precheck(사전검사)가 통과한 뒤에만 aggressive non-filter experiment(공격형 비필터 실험)를 한 번 연다.",
    }
    prune_reads = {
        "pr01_no_baseline_selection_from_low_pf_validation": "low PF validation(낮은 수익 팩터 검증)만으로 baseline selection(기준 후보 선택)을 하지 않는다.",
        "pr02_no_same_month_filter_stack": "same-month filter stack(같은 월 필터 누적)을 막고 shared-state feature(공유 상태 피처)로 전환한다.",
        "pr03_no_duplicate_independent_counting": "duplicate signature(중복 서명)를 independent evidence(독립 근거)로 두 번 세지 않는다.",
        "pr04_no_raw_aggressive_rerun_without_precheck": "precheck(사전검사) 없이 raw aggressive rerun(원시 공격형 재실행)을 반복하지 않는다.",
    }
    lines = [
        "# Stage267 Run267EJ Ninth Follow-Up/Prune Design(267단계 267EJ 9차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{result['source_run_id']}`",
        f"- source_report(원천 보고서): `{rel(SOURCE_REPORT_PATH)}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        f"- parsed_candidate_profile_rows(파싱 후보 프로필 행): `{summary['candidate_profile_rows']}`",
        f"- parsed_init_runtime_gap_rows(파싱 초기화/런타임 공백 행): `{summary['init_gap_rows_count']}`",
        f"- source_followup_queue_rows(원천 후속 대기열 행): `{summary['followup_queue_rows']}`",
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
        "run267EI(267EI 실행)는 숫자 1등을 고르라는 결과가 아니었다. 9개 KPI(핵심 성과 지표) 행 중 양수 행은 PF(수익 팩터)가 낮고, 2026.04 measured slice(측정 구간)는 여러 후보가 같이 음수였다.",
        "따라서 run267EJ(267EJ 실행)는 같은 필터를 더 붙이지 않고, handoff gap(인계 공백), 2026.04 shared state(공유 상태), duplicate signature(중복 서명), aggressive non-filter experiment(공격형 비필터 실험)를 분리한다.",
        "",
        "## Queue(대기열)",
        "",
    ]
    for row in result["materialization_queue"]:
        lines.append(
            f"- `{row['queue_id']}` `{row['priority']}` `{row['candidate_aliases']}`: "
            f"{queue_reads.get(str(row['queue_id']), row['decision_use'])}"
        )
    lines.extend(["", "## Feature Blueprint(피처 청사진)", ""])
    for row in result["feature_blueprint"]:
        lines.append(f"- `{row['feature_id']}` `{row['candidate_aliases']}`: {row['market_meaning']}")
    lines.extend(["", "## Prune Guard(가지치기 가드)", ""])
    for row in result["prune_matrix"]:
        lines.append(
            f"- `{row['prune_id']}` `{row['prune_label']}`: "
            f"{prune_reads.get(str(row['prune_id']), row['why_pruned'])}"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 설계는 exploratory design(탐색 설계)이며 후보 선택, 연구 기준 후보 선택, ONNX(온엑스) 준비, Goal Achieve(목표 달성)를 주장하지 않는다.",
            "- 다음 run267EK(267EK 실행)는 먼저 handoff precheck(인계 사전검사)를 물질화하고, 통과한 경우에만 공격형 비필터 실험을 연다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_engineering_blueprint(피처 엔지니어링 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- runtime_handoff_triage_plan(런타임 인계 진단 계획): `{rel(HANDOFF_TRIAGE_PATH)}`",
            f"- identity_audit_plan(정체성 감사 계획): `{rel(IDENTITY_AUDIT_PATH)}`",
            f"- aggressive_reentry_plan(공격 재진입 계획): `{rel(AGGRESSIVE_REENTRY_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- evidence_map(근거 지도): `{rel(EVIDENCE_MAP_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
        ]
    )
    return "\n".join(lines)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(FEATURE_BLUEPRINT_PATH, result["feature_blueprint"], FEATURE_BLUEPRINT_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, result["branch_decisions"], BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"], MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(HANDOFF_TRIAGE_PATH, result["handoff_triage_plan"], TRIAGE_COLUMNS)
    write_csv(IDENTITY_AUDIT_PATH, result["identity_audit_plan"], IDENTITY_COLUMNS)
    write_csv(AGGRESSIVE_REENTRY_PATH, result["aggressive_reentry_plan"], AGGRESSIVE_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, result["prune_matrix"], PRUNE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], EXPERIMENT_DESIGN_COLUMNS)
    write_csv(EVIDENCE_MAP_PATH, result["evidence_map"], EVIDENCE_MAP_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, result["gate_audit"], GATE_AUDIT_COLUMNS)
    write_json(RUN_MANIFEST_PATH, build_run_manifest(str(result["created_at_utc"]), result))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    write_json(LINEAGE_PATH, build_lineage(str(result["created_at_utc"])))


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    notes = (
        f"queue_rows={len(result['materialization_queue'])};"
        f"aggressive_rows={result['aggressive_queue_count']};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"source=tracked_run267EI_report;next_action={NEXT_ACTION}."
    )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_ninth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267EJ_runtime_gap_aware_ninth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_ninth_followup_or_prune_design",
        "tier_scope": "design only from tracked run267EI report",
        "scoreboard": "handoff_shared_state_identity_aggressive_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_ninth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_ninth_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_ninth_followup_or_prune_design",
        "tier_scope": "design only; next run materializes Tier A attempts",
        "kpi_scope": "experiment_design_queue_prune_failure_memory",
        "scoreboard_lane": "runtime_gap_aware_ninth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={len(result['materialization_queue'])};aggressive_rows={result['aggressive_queue_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "Design converts run267EI tracked report into handoff, shared-state, identity, validation-watch, and aggressive non-filter queue.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267EJ_runtime_gap_aware_ninth_followup_or_prune_design"
        f"(267EJ 런타임 공백 반영 9차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_block = "\n".join(
        [
            "Run267EJ(267EJ 실행)는 run267EI(267EI 실행)의 tracked report(추적 보고서)를 원천으로 handoff gap(인계 공백), 2026.04 shared state(공유 상태), duplicate signature(중복 서명), validation low-PF watch(검증 낮은 PF 관찰), aggressive non-filter reentry(공격형 비필터 재진입)를 9차 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, aggressive rows(공격 행) `{result['aggressive_queue_count']}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개, failure memory(실패 기억) `{len(result['failure_memory'])}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_ninth_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_line_once(current, report_line)
    current = append_block_once(current, "Run267EJ(267EJ 실행)는 run267EI", summary_block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_line_once(selection, report_line)
    selection = append_block_once(selection, "Run267EJ(267EJ 실행)는 run267EI", summary_block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    review_index = append_line_once(review_index, report_line)
    review_index = append_block_once(review_index, "Run267EJ(267EJ 실행)는 run267EI", summary_block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267EJ(267EJ 실행) runtime gap aware ninth follow-up/prune design(런타임 공백 반영 9차 후속/가지치기 설계) `{STATUS}`. "
        f"Effect(효과): run267EI(267EI 실행)의 tracked report(추적 보고서)를 materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, "
        f"aggressive rows(공격 행) `{result['aggressive_queue_count']}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage267(267단계) run267EJ(267EJ 실행)" not in workspace:
        workspace = workspace.replace("current_focus:\n", focus, 1)
    workspace = workspace.replace(
        "  status: run267EI_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review_completed_with_init_failures",
        f"  status: {STATUS}",
    )
    workspace = workspace.replace(
        "  current_run_id: run267EI_stage267_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review_v1",
        f"  current_run_id: {RUN_ID}",
    )
    workspace = workspace.replace(
        "  last_completed_run_id: run267EI_stage267_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review_v1",
        f"  last_completed_run_id: {RUN_ID}",
    )
    workspace = workspace.replace(
        "  run267EI_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review_report_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267EI_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review.md\n  next_action: run267EJ_design_runtime_gap_aware_ninth_followup_or_prune_from_run267EI_review",
        "  run267EI_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review_report_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267EI_runtime_gap_aware_eighth_followup_or_prune_balance_timeslice_trade_quality_review.md\n"
        f"  run267EJ_runtime_gap_aware_ninth_followup_or_prune_design_report_path: {rel(REPORT_PATH)}\n"
        f"  next_action: {NEXT_ACTION}",
    )
    workspace = append_block_once(workspace, "Run267EJ(267EJ 실행)는 run267EI", summary_block)
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_current_docs(result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "source_report": rel(SOURCE_REPORT_PATH),
                "candidate_profile_rows": result["source_summary"]["candidate_profile_rows"],
                "init_gap_rows": result["source_summary"]["init_gap_rows_count"],
                "materialization_queue": len(result["materialization_queue"]),
                "aggressive_rows": result["aggressive_queue_count"],
                "prune_rows": len(result["prune_matrix"]),
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
