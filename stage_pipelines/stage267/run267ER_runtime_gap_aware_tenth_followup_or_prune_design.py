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
    run267EQ_runtime_gap_aware_tenth_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267ER"
RUN_ID = "run267ER_stage267_runtime_gap_aware_tenth_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267ER_runtime_gap_aware_tenth_followup_or_prune_design_completed"
JUDGMENT = "runtime_gap_aware_tenth_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267ES_materialize_runtime_gap_aware_tenth_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_tenth_followup_or_prune_design"

SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_INIT_FAILURE_PATH = source_review.INIT_FAILURE_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_FOLLOWUP_QUEUE_PATH = source_review.FOLLOWUP_DECISION_QUEUE_PATH
SOURCE_ATTRIBUTION_PATH = source_review.ATTRIBUTION_SUMMARY_PATH

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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267ER_runtime_gap_aware_tenth_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267ER_runtime_gap_aware_tenth_followup_or_prune_design.py")

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

CANDIDATE_IDS = {
    "s264_aih": "s264_allow_inner_high_quarter",
    "s264_lc": "s264_lowrank_control",
    "s262_lih": "s262_lowrank_inner_half_filter",
    "s264_aia": "s264_allow_inner_all_oos_anchor",
    "s258_stc": "s258_short_tight_control",
}


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or sorted({key for row in rows for key in row.keys()}))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column, "")) for column in fieldnames})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_line_once(text: str, line: str) -> str:
    if line in text:
        return text
    return text.rstrip() + "\n" + line + "\n"


def insert_line_after_once(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if existing == anchor:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return append_line_once(text, line)


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def as_float(value: Any) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    return int(round(as_float(value)))


def source_summary(
    candidate_rows: Sequence[Mapping[str, str]],
    init_rows: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
    queue_rows: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    positive_low_pf = [row for row in candidate_rows if "positive_low_pf" in row.get("profile_read", "")]
    broken = [row for row in candidate_rows if as_float(row.get("net_profit")) < 0.0]
    return {
        "source_run_id": source_review.RUN_ID,
        "candidate_profile_rows": len(candidate_rows),
        "init_failure_groups": len(init_rows),
        "negative_slices": len(negative_rows),
        "followup_queue_rows": len(queue_rows),
        "positive_low_pf_rows": len(positive_low_pf),
        "negative_profile_rows": len(broken),
        "max_trade_count": max((as_int(row.get("trade_count")) for row in candidate_rows), default=0),
        "max_dd_percent": max((as_float(row.get("report_equity_drawdown_percent")) for row in candidate_rows), default=0.0),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def candidate_ids_for(aliases: str) -> str:
    return ";".join(CANDIDATE_IDS.get(alias, alias) for alias in aliases.split(";") if alias)


def build_feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "fb01_runtime_handoff_integrity_precheck",
            "candidate_aliases": "s258_stc;s264_aih",
            "feature_family": "runtime_handoff_integrity(런타임 인계 무결성)",
            "market_meaning": "시장 신호가 아니라 파일 인계, 초기화, 출력 공백이 성능 판독을 막는지 먼저 분리한다.",
            "source_evidence": "run267EQ init/runtime gap(초기화/런타임 공백) 4개",
            "changed_variables": "handoff file presence(인계 파일 존재), set/ini path validity(설정/초기화 경로 유효성), timeout/deinit reason capture(시간초과/종료 사유 기록)",
            "held_variables": "candidate identity(후보 정체성), feature order(피처 순서), model bundle(모델 묶음), MT5 tester harness(MetaTrader 5 테스터 장치)",
            "materialization_use": "run267ES에서 성능 실험 전 precheck receipt(사전검사 영수증)를 만든다.",
            "success_read": "막힌 4개 시도가 runtime output(런타임 출력)까지 가거나, 실패 이유가 구체 경로로 좁혀진다.",
            "failure_read": "같은 init_failed(초기화 실패)가 반복되면 해당 공격/압박 분기는 최대 2단계 repair loop(수리 루프) 안에서 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb02_202604_shared_adverse_state",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "feature_family": "shared_adverse_state_feature_engineering(공유 불리 상태 피처 엔지니어링)",
            "market_meaning": "2026.04 손상이 후보 하나의 문제가 아니라 공통 시장 상태인지 본다.",
            "source_evidence": "run267EQ에서 네 후보가 2026.04 measured slice(측정 구간)에서 모두 음수",
            "changed_variables": "sell-pressure state(매도 압력 상태), impulse exhaustion(충격 소진), ATR regime transition(ATR 체제 전환), no calendar-only filter(달력 단독 필터 금지)",
            "held_variables": "date scope(기간 범위), risk/ATR handoff(위험/ATR 인계), candidate surfaces(후보 표면)",
            "materialization_use": "같은 월 필터를 더 붙이지 않고 구조 피처 축으로 물질화한다.",
            "success_read": "거래 수를 과도하게 줄이지 않으면서 2026.04 sell weakness(매도 약점)가 완화된다.",
            "failure_read": "개선이 달력/시간 억제에서만 나오거나 네 후보가 계속 같이 깨지면 구조 축은 실패 기억으로 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb03_duplicate_signature_identity_receipt",
            "candidate_aliases": "s262_lih;s264_aia",
            "feature_family": "identity_and_feature_order_audit(정체성 및 피처 순서 감사)",
            "market_meaning": "두 후보가 다른 시장 의미를 잡은 것인지, 같은 표면이 이름만 다른 것인지 확인한다.",
            "source_evidence": "run267EQ validation identity receipt(검증 정체성 영수증)에서 두 후보의 net/PF/trades/DD가 동일",
            "changed_variables": "feature order hash(피처 순서 해시), model hash(모델 해시), route label(경로 라벨), decision surface signature(결정 표면 서명)",
            "held_variables": "validation scope(검증 범위), 2026.04 pressure scope(2026.04 압박 범위), no selection(선택 없음)",
            "materialization_use": "독립 후보로 세기 전에 identity receipt(정체성 영수증)를 만든다.",
            "success_read": "두 후보의 표면 차이가 해시/서명으로 분리된다.",
            "failure_read": "계속 동일하면 둘 중 하나는 independent evidence(독립 근거)가 아니라 duplicate control(중복 대조)로 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "fb04_aggressive_non_filter_reentry",
            "candidate_aliases": "s258_stc;s264_aih",
            "feature_family": "aggressive_non_filter_experiment(공격형 비필터 실험)",
            "market_meaning": "방어 필터만 쌓는 흐름을 끊고, 인계가 살아난 뒤 한 번은 넓게 밀어본다.",
            "source_evidence": "run267EQ q05 aggressive experiment after handoff fix(인계 수리 뒤 공격형 실험) 대기열",
            "changed_variables": "entry impulse intensity(진입 충격 강도), adverse-state confirmation(불리 상태 확인), no calendar-only suppression(달력 단독 억제 없음)",
            "held_variables": "precheck pass(사전검사 통과), feature order(피처 순서), bounded risk guard(제한된 위험 가드)",
            "materialization_use": "handoff triage(인계 진단)가 통과한 뒤 공격형 non-filter branch(비필터 분기)를 하나 물질화한다.",
            "success_read": "거래 수와 곡선 모양이 살아나면서 DD(drawdown, 손실폭)가 지나치게 악화되지 않는다.",
            "failure_read": "DD가 커지거나 약한 구간이 확대되면 공격형 분기는 실패 기억으로 보존하고 반복하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "q01_runtime_handoff_gap_bounded_triage",
            "priority": "P0",
            "candidate_aliases": "s258_stc;s264_aih",
            "candidate_ids": candidate_ids_for("s258_stc;s264_aih"),
            "workstream": "runtime_handoff_triage(런타임 인계 진단)",
            "source_queue_id": "q01_runtime_handoff_gap_bounded_triage",
            "action_type": "materialize_precheck_attempts(사전검사 시도 물질화)",
            "hypothesis": "blocked rows(차단 행)는 시장 성능 실패가 아니라 인계/초기화 문제일 수 있다.",
            "decision_use": "성능 판단 전에 repair(수리) 또는 prune(가지치기) 경계를 정한다.",
            "comparison_baseline": "run267EQ init/runtime gap(초기화/런타임 공백) 4개",
            "control_variables": "candidate/model/feature order/risk handoff(후보/모델/피처 순서/위험 인계) 유지",
            "changed_variables": "handoff diagnostics(인계 진단), timeout capture(시간초과 기록), path receipt(경로 영수증)",
            "sample_scope": "s258_stc 2025H1/2025H2, s264_aih validation/202604 blocked profiles",
            "success_criteria": "각 blocked profile(차단 프로필)이 runtime output(런타임 출력) 또는 정확한 blocker(차단 사유)를 남긴다.",
            "failure_criteria": "같은 init_failed(초기화 실패)가 재발하고 새 근거가 없으면 해당 분기는 닫는다.",
            "invalid_conditions": "set/ini/profile path(설정/초기화/프로필 경로)가 누락되면 성능 판독 금지",
            "stop_conditions": "repair branch(수리 분기)는 최대 2개 stage(단계) 안에서 종료",
            "evidence_plan": "preflight receipt(사전검사 영수증), runtime parity receipt(런타임 동등성 영수증), MT5 report(MetaTrader 5 보고서)",
            "runtime_instruction": "run267ES는 먼저 precheck를 물질화하고 run267ET에서 MT5 runtime probe(런타임 탐침)로 확인한다.",
            "aggressive_or_defensive": "diagnostic(진단)",
            "active_state": "active",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_202604_shared_sell_fragility_pivot",
            "priority": "P0",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "candidate_ids": candidate_ids_for("s264_aih;s264_lc;s262_lih;s264_aia"),
            "workstream": "shared_state_feature_engineering(공유 상태 피처 엔지니어링)",
            "source_queue_id": "q02_202604_shared_sell_fragility_pivot",
            "action_type": "materialize_structural_feature_pivot(구조 피처 전환 물질화)",
            "hypothesis": "2026.04 sell fragility(매도 취약성)는 후보 공통의 불리 상태일 수 있다.",
            "decision_use": "같은 월 필터 반복 대신 시장 상태 피처가 유효한지 판단한다.",
            "comparison_baseline": "run267EQ 2026.04 shared state rows(공유 상태 행)",
            "control_variables": "candidate surface/date window/risk profile(후보 표면/기간/위험 프로필) 유지",
            "changed_variables": "sell pressure state, impulse exhaustion, ATR transition without naked calendar filter",
            "sample_scope": "2026.04 OOS final slice(표본외 마지막 구간)",
            "success_criteria": "net/PF/DD/trade count(순손익/수익 팩터/손실폭/거래 수)가 함께 개선되고 거래 수가 과도하게 줄지 않는다.",
            "failure_criteria": "개선이 거래 억제나 달력 필터 효과뿐이면 실패",
            "invalid_conditions": "feature order(피처 순서) 또는 model identity(모델 정체성)가 바뀌면 무효",
            "stop_conditions": "동일 월 필터 추가 금지, 구조 피처 한 번 압박 후 판단",
            "evidence_plan": "candidate profile(후보 프로필), negative slice(음수 구간), curve diagnostics(곡선 진단)",
            "runtime_instruction": "four-candidate shared-state MT5 attempts(4후보 공유 상태 MT5 시도)를 만든다.",
            "aggressive_or_defensive": "structural_pivot(구조 전환)",
            "active_state": "active",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s262_s264_aia_signature_collapse_audit",
            "priority": "P1",
            "candidate_aliases": "s262_lih;s264_aia",
            "candidate_ids": candidate_ids_for("s262_lih;s264_aia"),
            "workstream": "identity_audit(정체성 감사)",
            "source_queue_id": "q03_s262_s264_aia_signature_collapse_audit",
            "action_type": "materialize_identity_receipts(정체성 영수증 물질화)",
            "hypothesis": "s262_lih와 s264_aia는 실질적으로 같은 표면일 수 있다.",
            "decision_use": "두 후보를 독립 후보로 셀지, 중복 대조로 낮출지 판단한다.",
            "comparison_baseline": "run267EQ validation identity rows(검증 정체성 행)",
            "control_variables": "validation window(검증 기간), model bundle(모델 묶음), feature order(피처 순서)",
            "changed_variables": "hash/route/signature receipts(해시/경로/서명 영수증)",
            "sample_scope": "validation IS(검증 표본내) plus 2026.04 pressure reference(압박 참고)",
            "success_criteria": "두 후보의 입력/모델/결정 표면 차이가 명확히 기록된다.",
            "failure_criteria": "동일 signature(서명)가 유지되면 독립 후보 주장을 중단한다.",
            "invalid_conditions": "hash source(해시 원천)가 누락되면 identity conclusion(정체성 결론) 금지",
            "stop_conditions": "중복 후보를 성과 개선으로 중복 계산하지 않는다.",
            "evidence_plan": "feature hash(피처 해시), model hash(모델 해시), decision surface signature(결정 표면 서명)",
            "runtime_instruction": "runtime artifact identity(런타임 산출물 정체성)를 receipt로 남긴다.",
            "aggressive_or_defensive": "audit(감사)",
            "active_state": "active",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_validation_positive_low_pf_watch",
            "priority": "P1",
            "candidate_aliases": "s264_aih;s262_lih;s264_aia",
            "candidate_ids": candidate_ids_for("s264_aih;s262_lih;s264_aia"),
            "workstream": "validation_watch_hold(검증 관찰 보류)",
            "source_queue_id": "q04_validation_positive_low_pf_watch",
            "action_type": "hold_not_materialize(보류, 단독 물질화 안 함)",
            "hypothesis": "validation positive(검증 양수)는 watch(관찰) 근거지만 선택 근거는 아니다.",
            "decision_use": "양수 숫자만 보고 ONNX(온엑스) 방향으로 건너뛰지 않게 한다.",
            "comparison_baseline": "run267EQ positive low-PF rows(낮은 PF 양수 행)",
            "control_variables": "none, this is a hold row(보류 행)",
            "changed_variables": "none",
            "sample_scope": "validation rows only(검증 행만)",
            "success_criteria": "다른 active queue(활성 대기열)의 곡선/구간 검증 뒤 다시 판단",
            "failure_criteria": "PF 약 1.21과 약한 월이 유지되면 watch로만 둔다.",
            "invalid_conditions": "단독 선택 근거로 사용하면 무효",
            "stop_conditions": "no selected candidate(선택 후보 없음), no ONNX(온엑스 없음)",
            "evidence_plan": "watch note(관찰 메모) only",
            "runtime_instruction": "run267ES에서 단독 시도는 만들지 않는다.",
            "aggressive_or_defensive": "held_watch(보류 관찰)",
            "active_state": "held",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q05_aggressive_experiment_after_handoff_fix",
            "priority": "P2_aggressive",
            "candidate_aliases": "s258_stc;s264_aih",
            "candidate_ids": candidate_ids_for("s258_stc;s264_aih"),
            "workstream": "aggressive_non_filter_reentry(공격형 비필터 재진입)",
            "source_queue_id": "q05_aggressive_experiment_after_handoff_fix",
            "action_type": "conditional_aggressive_materialization(조건부 공격형 물질화)",
            "hypothesis": "인계 공백이 해결되면 방어 필터가 아닌 공격형 구조도 한 번은 확인할 가치가 있다.",
            "decision_use": "연구가 방어 필터 누적에 갇히는지 막는다.",
            "comparison_baseline": "run267EQ aggressive rows(공격 행): s258 positive high DD, s264_aih negative",
            "control_variables": "handoff precheck pass(인계 사전검사 통과), bounded risk(제한 위험)",
            "changed_variables": "entry impulse intensity(진입 충격 강도), no calendar-only suppression(달력 단독 억제 없음)",
            "sample_scope": "s258 2025H1 and s264_aih 202604 only after precheck",
            "success_criteria": "trade count(거래 수), net profit(순수익), DD(손실폭), curve shape(곡선 형태)가 함께 개선",
            "failure_criteria": "DD 확대 또는 약한 구간 심화",
            "invalid_conditions": "precheck failed(사전검사 실패) 상태에서 공격형 성능 판독",
            "stop_conditions": "one aggressive tranche(공격 묶음 1회) 뒤 반복 금지 판단",
            "evidence_plan": "trade quality(거래 품질), curve diagnostics(곡선 진단), time-slice KPI(시간구간 핵심 성과 지표)",
            "runtime_instruction": "precheck pass(사전검사 통과) 뒤에만 materialize(물질화)",
            "aggressive_or_defensive": "aggressive(공격형)",
            "active_state": "conditional_active",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_handoff_triage(init_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(init_rows, start=1):
        alias = row.get("candidate_alias", "")
        attempt_role = row.get("attempt_role", "")
        rows.append(
            {
                "triage_id": f"ht{index:02d}_{alias}_{attempt_role}",
                "candidate_alias": alias,
                "candidate_id": CANDIDATE_IDS.get(alias, alias),
                "source_queue_id": row.get("queue_id", ""),
                "source_attempt_names": row.get("attempt_names", ""),
                "source_gap": row.get("read", ""),
                "precheck": "verify set/ini/profile/handoff file paths and capture init/deinit reason(설정/초기화/프로필/인계 경로와 초기화/종료 사유 확인)",
                "success_read": "runtime output(런타임 출력) exists or blocker(차단 사유) is precise",
                "failure_read": "same init_failed(초기화 실패) repeats without new evidence",
                "max_repair_span": "2 stages(2단계)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_identity_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ia01_s262_s264_aia_validation_signature",
            "candidate_aliases": "s262_lih;s264_aia",
            "identity_question": "두 validation identity receipt(검증 정체성 영수증)가 같은 후보 표면인지 확인한다.",
            "required_receipts": "feature order hash(피처 순서 해시);model hash(모델 해시);decision signature(결정 서명);runtime contract path(런타임 계약 경로)",
            "success_read": "서명이 분리되면 별도 후보 역할을 다시 검토",
            "failure_read": "서명이 같으면 duplicate control(중복 대조)로 낮춤",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_aggressive_reentry() -> list[dict[str, Any]]:
    return [
        {
            "aggressive_id": "ag01_s258_stc_after_handoff",
            "candidate_aliases": "s258_stc",
            "entry_condition": "q01 handoff precheck(인계 사전검사) 통과",
            "experiment_shape": "2025H1 stress branch(압박 분기), no calendar-only filter(달력 단독 필터 없음), bounded risk(제한 위험)",
            "not_allowed": "DD(drawdown, 손실폭)를 숨기거나 trade count(거래 수)를 과도하게 줄이는 미세 튜닝",
            "success_read": "profit(수익), PF(수익 팩터), DD(손실폭), curve(곡선)가 같이 좋아짐",
            "failure_read": "DD 20%대가 유지되거나 약한 시간/월이 더 깊어짐",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "aggressive_id": "ag02_s264_aih_final_month_after_handoff",
            "candidate_aliases": "s264_aih",
            "entry_condition": "q01 handoff precheck(인계 사전검사) 통과",
            "experiment_shape": "2026.04 final-month branch(마지막 월 분기), structural state(구조 상태), no same-month filter stack(같은 월 필터 누적 없음)",
            "not_allowed": "2026.04 손실만 가리는 달력/시간 필터 반복",
            "success_read": "17-trade collapse(17거래 붕괴)가 완화되고 sell slice(매도 구간)가 덜 깨짐",
            "failure_read": "매도 구간이 계속 음수면 s264_aih 공격형 분기는 닫음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_decisions() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "bd01_handoff_before_performance",
            "candidate_aliases": "s258_stc;s264_aih",
            "branch_decision": "repair_or_prune_runtime_gap_before_performance_claim(성능 주장 전 런타임 공백 수리 또는 가지치기)",
            "why": "run267EQ의 4개 blocked row(차단 행)는 시장 실패가 아니라 init/runtime gap(초기화/런타임 공백)이다.",
            "next_use": "run267ES에서 precheck materialization(사전검사 물질화) 우선",
            "reopen_condition": "runtime output(런타임 출력)과 trade list(거래 목록)가 생성될 때",
            "stop_condition": "동일 blocker(차단 사유)가 반복되면 최대 2단계 안에서 닫음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd02_shared_202604_structure_not_filter",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "branch_decision": "pivot_to_structural_feature_engineering(구조 피처 엔지니어링으로 전환)",
            "why": "2026.04에서 네 후보가 같이 음수라 후보 개별 수리보다 공유 상태 질문이 먼저다.",
            "next_use": "sell-pressure/adverse-state feature(매도 압력/불리 상태 피처) 물질화",
            "reopen_condition": "공통 약점이 줄고 validation(검증) 손상이 크지 않을 때",
            "stop_condition": "calendar-only filter(달력 단독 필터) 방향은 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd03_duplicate_signature_first",
            "candidate_aliases": "s262_lih;s264_aia",
            "branch_decision": "identity_audit_before_distinct_candidate_claim(독립 후보 주장 전 정체성 감사)",
            "why": "validation identity rows(검증 정체성 행)가 같은 KPI signature(핵심 성과 지표 서명)를 보였다.",
            "next_use": "feature/model/decision hash receipt(피처/모델/결정 해시 영수증)",
            "reopen_condition": "서명이 분리되면 validation-heavy(검증 중심)와 OOS anchor(표본외 앵커)를 다시 분리",
            "stop_condition": "서명이 같으면 독립 근거로 중복 계산 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd04_validation_watch_not_selection",
            "candidate_aliases": "s264_aih;s262_lih;s264_aia",
            "branch_decision": "watch_only_no_baseline_selection(관찰만, 기준 후보 선택 없음)",
            "why": "검증 양수 행은 PF 약 1.21이고 약한 월/구간이 남아 있다.",
            "next_use": "active queue(활성 대기열) 결과 후 재평가",
            "reopen_condition": "곡선/구간/거래 품질이 동시에 개선될 때",
            "stop_condition": "양수 숫자만으로 ONNX(온엑스) 검토 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd05_aggressive_lane_preserved",
            "candidate_aliases": "s258_stc;s264_aih",
            "branch_decision": "preserve_one_aggressive_non_filter_branch(공격형 비필터 분기 1회 보존)",
            "why": "방어 필터만 누적하면 목표의 넓은 탐색과 어긋난다.",
            "next_use": "handoff pass(인계 통과) 뒤 조건부 공격형 실험",
            "reopen_condition": "precheck 통과 후 bounded risk(제한 위험)로 실행 가능",
            "stop_condition": "DD 확대 또는 같은 약점 반복 시 실패 기억으로 닫음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "pr01_no_baseline_from_run267EQ",
            "affected_candidate_aliases": "pool",
            "prune_label": "no_candidate_selection(후보 선택 없음)",
            "why_pruned": "run267EQ는 8개 KPI와 4개 init/runtime gap을 분리했지만 최종 후보 근거가 아니다.",
            "salvage_value": "weakness map(약점 지도)와 next queue(다음 대기열)",
            "reopen_condition": "여러 기간/구간/곡선/거래 품질이 함께 개선될 때",
            "do_not_repeat": "숫자 몇 개 개선만으로 선택하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr02_no_same_month_filter_stack",
            "affected_candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "prune_label": "no_calendar_only_filter_stack(달력 단독 필터 누적 금지)",
            "why_pruned": "2026.04 손실만 가리는 필터는 구조를 배우지 못한다.",
            "salvage_value": "shared adverse-state feature(공유 불리 상태 피처)",
            "reopen_condition": "시장 의미가 있는 상태 피처가 설계될 때",
            "do_not_repeat": "월/요일/시간 필터만 더 붙이지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr03_no_duplicate_independent_counting",
            "affected_candidate_aliases": "s262_lih;s264_aia",
            "prune_label": "duplicate_signature_guard(중복 서명 가드)",
            "why_pruned": "동일 KPI signature(핵심 성과 지표 서명)를 독립 후보 근거로 세면 과장된다.",
            "salvage_value": "identity audit(정체성 감사)",
            "reopen_condition": "해시/서명이 분리될 때",
            "do_not_repeat": "같은 표면을 두 후보처럼 계산하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr04_no_raw_aggressive_without_precheck",
            "affected_candidate_aliases": "s258_stc;s264_aih",
            "prune_label": "precheck_before_aggressive(공격 전 사전검사)",
            "why_pruned": "init/runtime gap이 남은 상태에서 공격형 성능을 읽으면 무효다.",
            "salvage_value": "bounded aggressive branch(제한된 공격형 분기)",
            "reopen_condition": "handoff precheck(인계 사전검사) 통과",
            "do_not_repeat": "차단 행을 성능 실패나 성공으로 해석하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr05_no_onnx_from_review",
            "affected_candidate_aliases": "pool",
            "prune_label": "no_onnx_readiness(온엑스 준비 없음)",
            "why_pruned": "Adapter(어댑터), 안정성, 기간별/구간별 검증, runtime reproduction(런타임 재현), ONNX parity(온엑스 동등성) 근거가 아직 부족하다.",
            "salvage_value": "R&D racing queue(연구개발 경주 대기열)",
            "reopen_condition": "강한 후보가 여러 검증에서 덜 깨질 때",
            "do_not_repeat": "MT5 한 묶음 숫자로 ONNX를 논하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "fm01_runtime_gap_not_performance",
            "pattern": "init/runtime gap(초기화/런타임 공백)",
            "affected_scope": "s258_stc;s264_aih aggressive/precheck rows",
            "why_failed": "MT5 output(런타임 출력)이 없어서 성능 판독이 막힘",
            "salvage_value": "handoff triage(인계 진단)",
            "reopen_condition": "precheck receipt(사전검사 영수증) 생성",
            "do_not_repeat": "output 없는 행을 성능 행으로 비교하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm02_202604_shared_sell_fragility",
            "pattern": "shared final-month sell weakness(공유 마지막 월 매도 약점)",
            "affected_scope": "s264_aih;s264_lc;s262_lih;s264_aia",
            "why_failed": "2026.04에서 네 후보가 비슷하게 음수",
            "salvage_value": "structural adverse-state feature(구조적 불리 상태 피처)",
            "reopen_condition": "구조 피처가 거래 수를 유지하며 약점을 줄일 때",
            "do_not_repeat": "같은 월 필터만 추가하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm03_low_pf_positive_watch",
            "pattern": "positive but low PF(양수지만 낮은 수익 팩터)",
            "affected_scope": "s262_lih;s264_aia;s258_stc",
            "why_failed": "양수 행도 PF 약 1.21과 DD/약한 구간 위험이 있음",
            "salvage_value": "watch clue(관찰 단서)",
            "reopen_condition": "곡선과 약한 구간이 같이 좋아질 때",
            "do_not_repeat": "양수 net profit(순수익)만으로 후보 선택 금지",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm04_duplicate_signature_risk",
            "pattern": "duplicate signature(중복 서명)",
            "affected_scope": "s262_lih;s264_aia",
            "why_failed": "동일 KPI signature가 독립 후보성을 흐림",
            "salvage_value": "identity audit receipt(정체성 감사 영수증)",
            "reopen_condition": "feature/model/decision signature가 분리될 때",
            "do_not_repeat": "중복 표면을 후보군 다양성으로 과장하지 않음",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm05_aggressive_dd_risk",
            "pattern": "aggressive DD risk(공격형 손실폭 위험)",
            "affected_scope": "s258_stc;s264_aih",
            "why_failed": "s258_stc는 수익은 있으나 DD 21.19%, s264_aih는 final month 음수",
            "salvage_value": "one bounded aggressive branch(제한된 공격형 분기 1회)",
            "reopen_condition": "handoff pass + bounded risk guard",
            "do_not_repeat": "고위험 분기를 여러 단계 끌지 않음",
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


def build_evidence_map(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "ev01_source_review",
            "source_path": rel(SOURCE_REPORT_PATH),
            "source_field": "run267EQ report(보고서)",
            "observed_value": f"candidate_profile_rows={summary['candidate_profile_rows']};init_failure_groups={summary['init_failure_groups']};negative_slices={summary['negative_slices']}",
            "used_for": "design scope(설계 범위)",
            "effect": "run267ER는 새 성능 주장이 아니라 다음 물질화 설계를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev02_followup_queue",
            "source_path": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "source_field": "followup_decision_queue(후속 판단 대기열)",
            "observed_value": f"rows={summary['followup_queue_rows']}",
            "used_for": "materialization queue(물질화 대기열)",
            "effect": "다음 run267ES의 active/held queue(활성/보류 대기열)를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev03_candidate_profiles",
            "source_path": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_field": "candidate_profile_review(후보 프로필 검토)",
            "observed_value": f"negative_profile_rows={summary['negative_profile_rows']};positive_low_pf_rows={summary['positive_low_pf_rows']};max_dd_percent={summary['max_dd_percent']:.2f}",
            "used_for": "prune guard(가지치기 가드) and failure memory(실패 기억)",
            "effect": "선택 후보 없음과 ONNX readiness(온엑스 준비) 없음 경계를 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "run267EQ reviewed evidence(검토 근거), followup queue(후속 대기열), design artifacts(설계 산출물), ledgers(장부)",
            "evidence_missing": "new MT5 output(새 MT5 출력), Adapter parity(어댑터 동등성), runtime reproduction(런타임 재현), ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run267ES materialization(물질화) then MT5 runtime probe(런타임 탐침)",
            "user_explanation_hook": "이번 작업은 후보를 뽑은 것이 아니라 다음 실행을 덜 헷갈리게 나눈 설계다.",
        }
    ]


def build_gate_audit(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "g01_source_evidence_loaded",
            "gate_name": "source evidence gate(원천 근거 게이트)",
            "status": "passed",
            "evidence": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267EQ 검토 결과를 원천으로 사용했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "g02_experiment_design_receipt",
            "gate_name": "experiment design receipt(실험 설계 영수증)",
            "status": "passed",
            "evidence": f"design_rows={len(result['experiment_design_receipt'])}",
            "effect": "가설/비교 기준/성공·실패 조건을 남겼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "g03_anti_filter_stack_guard",
            "gate_name": "anti filter stack guard(필터 누적 방지 가드)",
            "status": "passed",
            "evidence": "q02 uses structural feature pivot, not naked calendar filter",
            "effect": "같은 월 필터 반복을 금지했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "g04_aggressive_lane_preserved",
            "gate_name": "aggressive lane preserved(공격형 레인 보존)",
            "status": "passed",
            "evidence": "q05_aggressive_experiment_after_handoff_fix",
            "effect": "방어 필터만 쌓는 흐름을 피한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "g05_claim_boundary",
            "gate_name": "claim boundary guard(주장 경계 가드)",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "운영·ONNX·목표 달성 주장을 하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs = [
        ("stage267_run267ER_producer", "producer_script", PRODUCER_PATH, "Builds run267ER follow-up/prune design."),
        ("stage267_run267ER_source_review", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267EQ review result."),
        ("stage267_run267ER_feature_blueprint", "feature_engineering_blueprint", FEATURE_BLUEPRINT_PATH, "Feature engineering blueprint."),
        ("stage267_run267ER_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decision matrix."),
        ("stage267_run267ER_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Materialization queue."),
        ("stage267_run267ER_handoff_triage", "runtime_handoff_triage_plan", HANDOFF_TRIAGE_PATH, "Runtime handoff triage plan."),
        ("stage267_run267ER_identity_audit", "identity_audit_plan", IDENTITY_AUDIT_PATH, "Identity audit plan."),
        ("stage267_run267ER_aggressive_reentry", "aggressive_reentry_plan", AGGRESSIVE_REENTRY_PATH, "Aggressive reentry plan."),
        ("stage267_run267ER_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune matrix."),
        ("stage267_run267ER_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267ER_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267ER_evidence_map", "evidence_map", EVIDENCE_MAP_PATH, "Evidence map."),
        ("stage267_run267ER_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267ER_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267ER_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267ER_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267ER_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267ER_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in specs:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "next_action": NEXT_ACTION,
        "source_paths": {
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
            "candidate_profile_review": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "init_failure_summary": rel(SOURCE_INIT_FAILURE_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "followup_decision_queue": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
        },
        "outputs": result["outputs"],
        "counts": result["counts"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source": rel(SOURCE_REVIEW_RESULT_PATH),
        "derived_outputs": result["outputs"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267ER Tenth Follow-Up/Prune Design(267단계 267ER 10차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- source_report(원천 보고서): `{rel(SOURCE_REPORT_PATH)}`",
        f"- candidate_profile_rows(후보-프로필 행): `{counts['candidate_profile_rows']}`",
        f"- init_failure_groups(초기화 실패 묶음): `{counts['init_failure_groups']}`",
        f"- negative_slices(음수 구간): `{counts['negative_slices']}`",
        f"- materialization_queue(물질화 대기열): `{counts['materialization_queue_rows']}`",
        f"- active_queue_rows(활성 대기열 행): `{counts['active_queue_rows']}`",
        f"- aggressive_rows(공격형 행): `{counts['aggressive_rows']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267EQ(267EQ 실행)는 후보를 뽑은 결과가 아니다. 8개 KPI(핵심 성과 지표)를 읽었지만 4개 init/runtime gap(초기화/런타임 공백), 69개 negative slice(음수 구간), 낮은 PF(profit factor, 수익 팩터) 양수 행이 같이 남았다.",
        "따라서 run267ER(267ER 실행)는 다음 실행을 세 갈래로 나눈다. 첫째, 런타임 인계가 막힌 행은 성능 실패가 아니라 handoff triage(인계 진단)로 본다. 둘째, 2026.04 공통 손상은 달력 필터가 아니라 shared adverse-state feature(공유 불리 상태 피처)로 본다. 셋째, 방어 필터만 쌓지 않도록 precheck(사전검사) 뒤 aggressive non-filter experiment(공격형 비필터 실험)를 한 번 보존한다.",
        "",
        "## Queue(대기열)",
        "",
    ]
    for row in result["materialization_queue"]:
        lines.append(
            f"- `{row['queue_id']}` `{row['priority']}` `{row['candidate_aliases']}` `{row['active_state']}`: {row['decision_use']}"
        )
    lines.extend(["", "## Prune Guard(가지치기 가드)", ""])
    for row in result["prune_matrix"]:
        lines.append(f"- `{row['prune_id']}` `{row['prune_label']}`: {row['why_pruned']}")
    lines.extend(["", "## Boundary(경계)", ""])
    lines.append("- 이 설계는 exploratory design(탐색 설계)이다. 후보 선택, 연구 기준 후보 선택, ONNX(온엑스) 준비, Goal Achieve(목표 달성)를 주장하지 않는다.")
    lines.append("- run267ES(267ES 실행)는 물질화 단계이며, 새 MT5(MetaTrader 5, 메타트레이더5) 성능 근거는 이후 runtime probe(런타임 탐침)에서만 생긴다.")
    lines.extend(["", "## Artifacts(산출물)", ""])
    for label, path in result["outputs"].items():
        lines.append(f"- {label}: `{path}`")
    return "\n".join(lines)


def build_result() -> dict[str, Any]:
    required = [
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_REPORT_PATH,
        SOURCE_CANDIDATE_PROFILE_PATH,
        SOURCE_INIT_FAILURE_PATH,
        SOURCE_NEGATIVE_SLICE_PATH,
        SOURCE_FOLLOWUP_QUEUE_PATH,
        SOURCE_ATTRIBUTION_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    candidate_rows = read_csv(SOURCE_CANDIDATE_PROFILE_PATH)
    init_rows = read_csv(SOURCE_INIT_FAILURE_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    source_queue_rows = read_csv(SOURCE_FOLLOWUP_QUEUE_PATH)
    attribution_rows = read_csv(SOURCE_ATTRIBUTION_PATH)
    queue_rows = build_materialization_queue()
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": utc_now(),
        "next_action": NEXT_ACTION,
        "source_summary": source_summary(candidate_rows, init_rows, negative_rows, source_queue_rows),
        "source_attribution_rows": len(attribution_rows),
        "feature_blueprint": build_feature_blueprints(),
        "branch_decision_matrix": build_branch_decisions(),
        "materialization_queue": queue_rows,
        "runtime_handoff_triage_plan": build_handoff_triage(init_rows),
        "identity_audit_plan": build_identity_audit(),
        "aggressive_reentry_plan": build_aggressive_reentry(),
        "prune_matrix": build_prune_matrix(),
        "failure_memory": build_failure_memory(),
        "experiment_design_receipt": build_experiment_design_receipt(queue_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    result["evidence_map"] = build_evidence_map(result["source_summary"])
    result["result_judgment"] = build_result_judgment()
    result["gate_audit"] = build_gate_audit(result)
    result["counts"] = {
        **result["source_summary"],
        "feature_blueprint_rows": len(result["feature_blueprint"]),
        "branch_decision_rows": len(result["branch_decision_matrix"]),
        "materialization_queue_rows": len(result["materialization_queue"]),
        "active_queue_rows": sum(1 for row in result["materialization_queue"] if row["active_state"] != "held"),
        "aggressive_rows": sum(1 for row in result["materialization_queue"] if "aggressive" in row["aggressive_or_defensive"]),
        "prune_rows": len(result["prune_matrix"]),
        "failure_memory_rows": len(result["failure_memory"]),
    }
    result["outputs"] = {
        "feature_engineering_blueprint(피처 엔지니어링 청사진)": rel(FEATURE_BLUEPRINT_PATH),
        "branch_decision_matrix(분기 판단 행렬)": rel(BRANCH_DECISION_PATH),
        "materialization_queue(물질화 대기열)": rel(MATERIALIZATION_QUEUE_PATH),
        "runtime_handoff_triage_plan(런타임 인계 진단 계획)": rel(HANDOFF_TRIAGE_PATH),
        "identity_audit_plan(정체성 감사 계획)": rel(IDENTITY_AUDIT_PATH),
        "aggressive_reentry_plan(공격형 재진입 계획)": rel(AGGRESSIVE_REENTRY_PATH),
        "prune_matrix(가지치기 행렬)": rel(PRUNE_MATRIX_PATH),
        "failure_memory(실패 기억)": rel(FAILURE_MEMORY_PATH),
        "experiment_design_receipt(실험 설계 영수증)": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "evidence_map(근거 지도)": rel(EVIDENCE_MAP_PATH),
        "result_judgment(결과 판정)": rel(RESULT_JUDGMENT_PATH),
        "gate_audit(게이트 감사)": rel(GATE_AUDIT_PATH),
        "run_manifest(실행 목록)": rel(RUN_MANIFEST_PATH),
        "lineage(계보)": rel(LINEAGE_PATH),
        "review_result(검토 결과)": rel(REVIEW_RESULT_PATH),
        "report(보고서)": rel(REPORT_PATH),
    }
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(FEATURE_BLUEPRINT_PATH, result["feature_blueprint"])
    write_csv(BRANCH_DECISION_PATH, result["branch_decision_matrix"])
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"])
    write_csv(HANDOFF_TRIAGE_PATH, result["runtime_handoff_triage_plan"])
    write_csv(IDENTITY_AUDIT_PATH, result["identity_audit_plan"])
    write_csv(AGGRESSIVE_REENTRY_PATH, result["aggressive_reentry_plan"])
    write_csv(PRUNE_MATRIX_PATH, result["prune_matrix"])
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(EVIDENCE_MAP_PATH, result["evidence_map"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, run_manifest(result))
    write_json(LINEAGE_PATH, lineage(result))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def update_ledgers(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    notes = (
        f"queue_rows={counts['materialization_queue_rows']};"
        f"active_rows={counts['active_queue_rows']};"
        f"aggressive_rows={counts['aggressive_rows']};"
        f"prune_rows={counts['prune_rows']};"
        f"source=run267EQ_review;next_action={NEXT_ACTION}."
    )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_tenth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267ER_runtime_gap_aware_tenth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_tenth_followup_or_prune_design",
        "tier_scope": "design only from run267EQ reviewed rows",
        "scoreboard": "handoff_shared_state_identity_aggressive_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_tenth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_tenth_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_tenth_followup_or_prune_design",
        "tier_scope": "design only; next run materializes Tier A attempts",
        "kpi_scope": "experiment_design_queue_prune_failure_memory",
        "scoreboard_lane": "runtime_gap_aware_tenth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={counts['materialization_queue_rows']};aggressive_rows={counts['aggressive_rows']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "Design converts run267EQ review into runtime handoff triage, shared-state pivot, identity audit, validation watch, and aggressive non-filter queue.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(str(result["created_at_utc"]), result), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267ER_runtime_gap_aware_tenth_followup_or_prune_design"
        f"(267ER 런타임 공백 반영 10차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_block = "\n".join(
        [
            "Run267ER(267ER 실행)는 run267EQ(267EQ 실행)의 reviewed evidence(검토 근거)를 원천으로 runtime handoff gap(런타임 인계 공백), 2026.04 shared fragility(공유 취약성), duplicate signature(중복 서명), validation low-PF watch(검증 낮은 PF 관찰), aggressive non-filter branch(공격형 비필터 분기)를 분리했다.",
            f"Effect(효과): materialization queue(물질화 대기열) `{counts['materialization_queue_rows']}`개, active rows(활성 행) `{counts['active_queue_rows']}`개, aggressive rows(공격형 행) `{counts['aggressive_rows']}`개, prune matrix(가지치기 행렬) `{counts['prune_rows']}`개, failure memory(실패 기억) `{counts['failure_memory_rows']}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_tenth_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_line_once(current, report_line)
    current = append_block_once(current, "Run267ER(267ER 실행)는 run267EQ", summary_block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_line_once(selection, report_line)
    selection = append_block_once(selection, "Run267ER(267ER 실행)는 run267EQ", summary_block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = append_line_once(review_index, report_line)
    review_index = append_block_once(review_index, "Run267ER(267ER 실행)는 run267EQ", summary_block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267ER(267ER 실행) runtime gap aware tenth follow-up/prune design(런타임 공백 반영 10차 후속/가지치기 설계) `{STATUS}`. "
        f"Effect(효과): materialization queue(물질화 대기열) `{counts['materialization_queue_rows']}`개, aggressive rows(공격형 행) `{counts['aggressive_rows']}`개, prune matrix(가지치기 행렬) `{counts['prune_rows']}`개를 만들었고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage267(267단계) run267ER(267ER 실행)" not in workspace:
        workspace = workspace.replace("current_focus:\n", focus, 1)
    workspace = workspace.replace(
        "next_action: run267ER_design_runtime_gap_aware_tenth_followup_or_prune_from_run267EQ_review",
        f"next_action: {NEXT_ACTION}",
        1,
    )
    workspace_report_line = f"  run267ER_runtime_gap_aware_tenth_followup_or_prune_design_report_path: {rel(REPORT_PATH)}"
    workspace_report_anchor = (
        "  run267EQ_runtime_gap_aware_tenth_followup_or_prune_balance_timeslice_trade_quality_review_report_path: "
        f"{rel(SOURCE_REPORT_PATH)}"
    )
    workspace = insert_line_after_once(workspace, workspace_report_anchor, workspace_report_line)
    write_md(WORKSPACE_STATE_PATH, workspace)


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_current_docs(result)
    return result


def main() -> int:
    result = execute()
    counts = result["counts"]
    print(
        json.dumps(
            {
                "status": result["status"],
                "source_run": PARENT_RUN_ID,
                "candidate_profile_rows": counts["candidate_profile_rows"],
                "init_failure_groups": counts["init_failure_groups"],
                "negative_slices": counts["negative_slices"],
                "materialization_queue": counts["materialization_queue_rows"],
                "active_queue_rows": counts["active_queue_rows"],
                "aggressive_rows": counts["aggressive_rows"],
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
