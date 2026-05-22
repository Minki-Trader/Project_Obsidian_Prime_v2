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
    run267DS_runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267DT"
RUN_ID = "run267DT_stage267_runtime_gap_aware_fifth_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267DT_runtime_gap_aware_fifth_followup_or_prune_design_completed"
JUDGMENT = "runtime_gap_aware_fifth_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267DU_materialize_runtime_gap_aware_fifth_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_fifth_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH = source_review.CANDIDATE_INIT_FAILURE_SUMMARY_PATH
SOURCE_ATTEMPT_OUTCOME_PATH = source_review.ATTEMPT_OUTCOME_REVIEW_PATH
SOURCE_ATTRIBUTION_PATH = source_review.ATTRIBUTION_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
INITIAL_SCOREBOARD_PATH = STAGE_ROOT / "03_reviews" / "stage267_initial_scoreboard.csv"
MONTHLY_WEAKNESS_PATH = STAGE_ROOT / "03_reviews" / "stage267_monthly_weakness_matrix.csv"
EQUITY_SHAPE_PATH = STAGE_ROOT / "03_reviews" / "stage267_equity_curve_shape_grading.csv"

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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DT_runtime_gap_aware_fifth_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DT_runtime_gap_aware_fifth_followup_or_prune_design.py")

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
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_evidence",
    "decision_label",
    "next_use",
    "why",
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
    "changed_variables",
    "control_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "runtime_instruction",
    "aggressive_or_defensive",
    "claim_boundary",
)

PRUNE_COLUMNS = (
    "prune_id",
    "affected_candidate_aliases",
    "affected_attempts",
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
            insert_at = index + 1
            while insert_at < len(lines) and lines[insert_at].startswith("  "):
                insert_at += 1
            lines.insert(insert_at, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def stage267_report_entry() -> str:
    return f"  run267DT_runtime_gap_aware_fifth_followup_or_prune_design_report_path: {rel(REPORT_PATH)}"


def source_maps() -> dict[str, Any]:
    init_summary = {row.get("candidate_alias", ""): row for row in read_csv_rows(SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH)}
    profiles = read_csv_rows(SOURCE_CANDIDATE_PROFILE_PATH)
    attempts = read_csv_rows(SOURCE_ATTEMPT_OUTCOME_PATH)
    attribution = {row.get("candidate_alias", ""): row for row in read_csv_rows(SOURCE_ATTRIBUTION_PATH)}
    scoreboard = {row.get("candidate_id", ""): row for row in read_csv_rows(INITIAL_SCOREBOARD_PATH)}
    return {
        "init_summary": init_summary,
        "profiles": profiles,
        "attempts": attempts,
        "attribution": attribution,
        "scoreboard": scoreboard,
        "monthly_weakness": read_csv_rows(MONTHLY_WEAKNESS_PATH),
        "equity_shape": read_csv_rows(EQUITY_SHAPE_PATH),
    }


def build_feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "bp267dt_s258_ebm_table_handoff_repair",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "feature_family": "runtime_handoff_repair(런타임 인계 수리)",
            "market_meaning": "s258_stc(258 STC 후보)의 supply continuity(공급 연속성)가 시장 의미 전에 EBM table open failure(EBM 테이블 열기 실패)로 막혔는지 확인한다.",
            "source_evidence": "run267DS(267DS 실행) init_failure_attempts(초기화 실패 시도) 3, ebm_table_open_failed:5003 3.",
            "changed_variables": "model/table export path(모델/테이블 출력 경로), Common Files handoff(공통 파일 인계), preflight open check(사전 열기 점검).",
            "held_variables": "candidate identity(후보 정체성), split(구간), threshold release 금지(임계값 해제 금지).",
            "aggressive_or_defensive": "repair_gate(수리 게이트)",
            "success_read": "세 구간 모두 init failure(초기화 실패)가 사라지고 nonzero feature/model ready(비영 피처/모델 준비)가 확인된다.",
            "failure_read": "테이블 인계 수리 뒤에도 0 trade(무거래) 또는 init failure(초기화 실패)가 반복되면 이 공급 연속성 경로는 닫는다.",
            "materialization_note": "run267DU(267DU 실행)에서 P0 preflight와 좁은 MT5 재시도까지 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dt_s258_noncalendar_impulse_reentry",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "feature_family": "noncalendar_impulse_reentry(비달력 충격 재진입)",
            "market_meaning": "월요일/후반 시간 필터를 더 두껍게 붙이지 않고, 충격/추세/변동성 상태에서 살아나는 거래만 다시 열어본다.",
            "source_evidence": "run267DS(267DS 실행) taper rows: 2023H2 net 190.76, 2025H1 net -3.69, 2025H2 net 33.93.",
            "changed_variables": "impulse strength(충격 강도), volatility compression break(변동성 압축 돌파), late-session risk shape(후반 세션 위험 형태).",
            "held_variables": "기존 calendar ban(달력 금지) 추가 금지, 기존 split(구간) 유지.",
            "aggressive_or_defensive": "aggressive(공격형)",
            "success_read": "2025H1 검증 붕괴를 줄이면서 거래 수를 과도하게 줄이지 않는다.",
            "failure_read": "2025H1/2025H2 품질이 계속 약하거나 거래 수가 얇아지면 s258_stc 공격 축을 낮춘다.",
            "materialization_note": "P0 aggressive queue(공격형 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dt_s264_aih_explosive_shock_state",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "feature_family": "explosive_shock_state(폭발형 충격 상태)",
            "market_meaning": "현재 가장 밀어볼 만한 core challenger(핵심 도전자)를 다시 전면에 놓고 OOS final month(표본외 마지막 달) 손실이 우연인지 확인한다.",
            "source_evidence": "initial scoreboard(초기 점수판): OOS net 857.67, PF 1.74, final OOS month 2026.04 -41.14.",
            "changed_variables": "shock-state gate(충격 상태 관문), trend-strength replacement(추세 강도 대체), late-OOS drawdown guard(후반 표본외 손실 방어).",
            "held_variables": "s264_aih identity(s264 AIH 정체성), no operating claim(운영 주장 없음).",
            "aggressive_or_defensive": "explosive_aggressive(폭발형 공격)",
            "success_read": "OOS 회복은 유지하면서 2026.04 손실과 validation weak PF(검증 약한 PF)를 덜 깨뜨린다.",
            "failure_read": "OOS 회복이 사라지거나 validation(검증)이 더 깨지면 공격형 shock-state는 실패 기억으로 닫는다.",
            "materialization_note": "run267DU(267DU 실행)의 P0 aggressive challenger queue(공격형 도전자 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dt_s264_lc_dd_cluster_control",
            "candidate_aliases": "s264_lc",
            "candidate_ids": "s264_lowrank_control",
            "feature_family": "dd_cluster_control(손실폭 군집 대조)",
            "market_meaning": "수익은 좋지만 24.39% DD(drawdown, 손실폭), Monday(월요일), 2024-06/12 구멍이 있어 방어 대조로만 둔다.",
            "source_evidence": "run267DS(267DS 실행): net 1522.61, PF 1.42, trades 473, DD 24.39, Monday -235.05.",
            "changed_variables": "drawdown cluster tagging(손실폭 군집 태깅), weak month attribution(약한 월 귀속).",
            "held_variables": "defensive control role(방어 대조 역할), no candidate selection(후보 선택 없음).",
            "aggressive_or_defensive": "defensive_control(방어 대조)",
            "success_read": "방어 대조의 허용 불가 손실 조건을 명확히 해 다음 경주 비교 기준을 만든다.",
            "failure_read": "DD 구조가 설명되지 않으면 대조 후보도 확장하지 않는다.",
            "materialization_note": "P0 control queue(대조 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dt_aia_lih_supply_manifest_diagnostic",
            "candidate_aliases": "s264_aia;s262_lih",
            "candidate_ids": "s264_allow_inner_all_oos_anchor;s262_lowrank_inner_half_filter",
            "feature_family": "pre_runtime_supply_manifest(런타임 전 공급 목록)",
            "market_meaning": "무거래/공백 경로를 MT5(MetaTrader 5, 메타트레이더5)에 다시 던지기 전에 신호 공급 자체가 있는지 검증한다.",
            "source_evidence": "이전 runtime gap(런타임 공백) 계열에서 s264_aia/s262_lih는 completed runtime(완료 런타임)이 약했다.",
            "changed_variables": "nonzero activation manifest(비영 활성 목록), feature-row supply count(피처 행 공급 수).",
            "held_variables": "MT5 blind retry(눈먼 MT5 재시도) 금지.",
            "aggressive_or_defensive": "diagnostic_only(진단 전용)",
            "success_read": "신호 공급이 증명되면 다음 공격/대조 실행에 재합류시킨다.",
            "failure_read": "공급 증명이 없으면 이번 루프에서는 보류한다.",
            "materialization_note": "P1 diagnostic queue(진단 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "bp267dt_similar_feature_replacement_pack",
            "candidate_aliases": "s264_aih;s258_stc",
            "candidate_ids": "s264_allow_inner_high_quarter;s258_short_tight_control",
            "feature_family": "similar_feature_replacement(유사 피처 대체)",
            "market_meaning": "ADX(추세 강도) 하나에 우연히 붙은 것이 아니라, 유사한 추세/변동성 의미에서도 살아남는지 본다.",
            "source_evidence": "goal requirement(목표 요구): similar replacement(유사 대체)를 baseline 후보군 기준으로 다시 수행해야 한다.",
            "changed_variables": "ADX-like trend strength(ADX 유사 추세 강도), ATR-z impulse(ATR 표준화 충격), range expansion(범위 확장).",
            "held_variables": "same candidate pool(동일 후보군), same split scope(동일 구간 범위), no ONNX claim(ONNX 주장 없음).",
            "aggressive_or_defensive": "aggressive_validation(공격형 검증)",
            "success_read": "대체 피처에서도 후보가 완전히 무너지지 않으면 Adapter(어댑터) 개발 가치가 올라간다.",
            "failure_read": "대체 피처에서 완전히 붕괴하면 feature dependency(피처 의존성) 실패로 기록한다.",
            "materialization_note": "P0/P1 사이의 replacement queue(대체 대기열)로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_decisions() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "bd267dt_s258_supply_continuity_repair_once",
            "candidate_alias": "s258_stc",
            "candidate_id": "s258_short_tight_control",
            "candidate_role": "stress_challenger(압박 도전자)",
            "source_evidence": "run267DS(267DS 실행) supply continuity 3/3 init_failed, ebm_table_open_failed:5003.",
            "decision_label": "repair_once_then_drop_if_still_failed(한 번 수리 후 실패 반복 시 종료)",
            "next_use": "P0 handoff repair plus narrow MT5 retry(P0 인계 수리와 좁은 MT5 재시도)",
            "why": "실패 원인이 성능이 아니라 table handoff(테이블 인계)라서 후보 자체를 성급히 버리지는 않는다.",
            "reopen_condition": "preflight open check(사전 열기 점검)가 통과하고 runtime output(런타임 출력)이 생성될 때.",
            "stop_condition": "수리 뒤에도 init_failed(초기화 실패)가 반복되면 이 branch(분기)는 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dt_s258_taper_not_enough_use_aggressive_noncalendar",
            "candidate_alias": "s258_stc",
            "candidate_id": "s258_short_tight_control",
            "candidate_role": "stress_challenger(압박 도전자)",
            "source_evidence": "2025H1 net -3.69, 2025H2 net 33.93, avg PF 1.10837.",
            "decision_label": "do_not_add_more_calendar_filters_try_noncalendar_impulse(달력 필터 추가 대신 비달력 충격 실험)",
            "next_use": "P0 aggressive noncalendar reentry(P0 공격형 비달력 재진입)",
            "why": "필터를 덕지덕지 붙이는 방향을 피하고, 시장 상태 의미가 있는 충격/변동성 축으로 바꾼다.",
            "reopen_condition": "2025H1 validation(2025 상반기 검증)이 회복되고 거래 수가 유지될 때.",
            "stop_condition": "거래 수가 얇아지거나 2025H1/H2 품질이 계속 약하면 s258 공격 축을 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dt_s264_aih_reenter_as_explosive_core_challenger",
            "candidate_alias": "s264_aih",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_role": "core_challenger(핵심 도전자)",
            "source_evidence": "initial scoreboard(초기 점수판) OOS net 857.67, PF 1.74, final OOS month 2026.04 -41.14.",
            "decision_label": "reenter_aggressive_challenger_queue(공격형 도전자 대기열 재진입)",
            "next_use": "P0 explosive shock-state probe(P0 폭발형 충격 상태 탐침)",
            "why": "DS 이후 흐름이 s258/s264_lc로 좁아졌으므로 핵심 도전자를 다시 전면 테스트한다.",
            "reopen_condition": "OOS final month(표본외 마지막 달) 손실을 줄이며 validation(검증)을 크게 훼손하지 않을 때.",
            "stop_condition": "OOS 회복이 무너지면 shock-state 방향은 실패 기억으로 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dt_s264_lc_keep_control_only",
            "candidate_alias": "s264_lc",
            "candidate_id": "s264_lowrank_control",
            "candidate_role": "defensive_control(방어 대조)",
            "source_evidence": "run267DS(267DS 실행) net 1522.61 but DD 24.39, Monday -235.05.",
            "decision_label": "control_only_no_selection(대조 전용, 선택 아님)",
            "next_use": "P0 defensive control DD cluster(P0 방어 대조 손실폭 군집)",
            "why": "수익은 좋지만 DD(drawdown, 손실폭)와 월/요일 구멍이 불편하다.",
            "reopen_condition": "DD cluster(손실폭 군집)가 설명되고 대조 기준으로만 쓰일 때.",
            "stop_condition": "DD를 줄이려는 수리가 2단계 이상 반복되면 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bd267dt_aia_lih_no_blind_retry",
            "candidate_alias": "s264_aia;s262_lih",
            "candidate_id": "s264_allow_inner_all_oos_anchor;s262_lowrank_inner_half_filter",
            "candidate_role": "oos_anchor_and_validation_heavy(표본외 앵커와 검증 중심)",
            "source_evidence": "prior runtime gap(이전 런타임 공백) and no current DS completed profile(현재 DS 완료 프로필 없음).",
            "decision_label": "diagnostic_before_runtime_retry(런타임 재시도 전 진단)",
            "next_use": "P1 supply manifest diagnostic(P1 공급 목록 진단)",
            "why": "무거래/공백을 반복 실행하면 병목이 되므로 신호 공급 증명부터 만든다.",
            "reopen_condition": "nonzero activation(비영 활성)이 증명될 때.",
            "stop_condition": "공급 증명이 없으면 이번 루프에서 실행하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "q01_s258_supply_continuity_table_handoff_repair",
            "priority": "P0_repair",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "runtime_handoff_repair(런타임 인계 수리)",
            "source_evidence": "run267DS init failure(초기화 실패) attempts run267dq_01/02/03.",
            "changed_variables": "EBM table path(EBM 테이블 경로), Common Files copy(공통 파일 복사), preflight open receipt(사전 열기 영수증).",
            "control_variables": "same 2023H2/2025H1/2025H2 splits(동일 구간), same supply continuity profile(동일 공급 연속성 프로필).",
            "sample_scope": "adjacent_2023_h2_train_pre_2024;adjacent_2025_h1_validation_post_2024;adjacent_2025_h2_oos_followthrough.",
            "success_criteria": "init_failed(초기화 실패) 0 and runtime output(런타임 출력) exists.",
            "failure_criteria": "ebm_table_open_failed:5003 repeats(반복) or zero-trade report remains after repair(수리 후 무거래 지속).",
            "invalid_conditions": "model/table hash(모델/테이블 해시) missing, feature order mismatch(피처 순서 불일치), report parser mismatch(보고서 파서 불일치).",
            "runtime_instruction": "materialize preflight receipts, then narrow MT5 retry(사전 영수증 생성 후 좁은 MT5 재시도).",
            "aggressive_or_defensive": "repair_gate(수리 게이트)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_s258_noncalendar_impulse_reentry_cross_period",
            "priority": "P0_aggressive",
            "candidate_aliases": "s258_stc",
            "candidate_ids": "s258_short_tight_control",
            "workstream": "aggressive_noncalendar_impulse(공격형 비달력 충격)",
            "source_evidence": "run267DS taper completed 3 rows but validation/OOS weak.",
            "changed_variables": "impulse strength(충격 강도), ATR-z shock(ATR 표준화 충격), late-session risk size(후반 세션 위험 크기).",
            "control_variables": "no additional weekday/month ban(요일/월 금지 추가 없음), same splits(동일 구간).",
            "sample_scope": "2023H2, 2025H1 validation, 2025H2 OOS followthrough.",
            "success_criteria": "2025H1 net_profit(순수익) turns positive and PF(수익 팩터) > 1.08 without severe trade-count loss(거래 수 급감 없음).",
            "failure_criteria": "validation remains negative(검증 음수 유지) or OOS trade quality decays(표본외 거래 품질 저하).",
            "invalid_conditions": "hidden calendar filter(숨은 달력 필터) or changed candidate identity(후보 정체성 변경).",
            "runtime_instruction": "materialize aggressive variant pack(공격형 변형 묶음 물질화).",
            "aggressive_or_defensive": "aggressive(공격형)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s264_aih_explosive_shock_state_oos_final_month",
            "priority": "P0_explosive",
            "candidate_aliases": "s264_aih",
            "candidate_ids": "s264_allow_inner_high_quarter",
            "workstream": "explosive_core_challenger_reentry(폭발형 핵심 도전자 재진입)",
            "source_evidence": "initial scoreboard OOS net 857.67 and OOS final month 2026.04 -41.14.",
            "changed_variables": "shock-state gate(충격 상태 관문), trend-strength replacement(추세 강도 대체), late-OOS risk shape(후반 표본외 위험 형태).",
            "control_variables": "same core challenger identity(동일 핵심 도전자 정체성), no ONNX claim(ONNX 주장 없음).",
            "sample_scope": "validation_is and OOS including 2026.04 final month(검증 및 2026.04 마지막 표본외).",
            "success_criteria": "OOS final month loss(마지막 표본외 월 손실) improves while OOS PF(표본외 수익 팩터) remains strong.",
            "failure_criteria": "OOS recovery disappears(표본외 회복 소실) or validation damage grows(검증 손상 확대).",
            "invalid_conditions": "feature order drift(피처 순서 드리프트), leakage(누수), or missing Tier boundary(티어 경계 누락).",
            "runtime_instruction": "materialize explosive challenger attempts(폭발형 도전자 시도 물질화).",
            "aggressive_or_defensive": "explosive_aggressive(폭발형 공격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_s264_lc_defensive_dd_cluster_control",
            "priority": "P0_control",
            "candidate_aliases": "s264_lc",
            "candidate_ids": "s264_lowrank_control",
            "workstream": "defensive_dd_cluster_control(방어 손실폭 군집 대조)",
            "source_evidence": "run267DS DD 24.39, Monday -235.05, 2024-06 -163.98, 2024-12 -129.63.",
            "changed_variables": "DD cluster labels(손실폭 군집 라벨), weak-month audit(약한 월 감사).",
            "control_variables": "historical_2024 scope(2024 과거 범위), defensive role(방어 역할).",
            "sample_scope": "historical_2024 Tier A; duplicate-boundary Tier A+B marked as not true fallback(실제 대체 아님 표시).",
            "success_criteria": "control risk boundary(대조 위험 경계)가 명확히 기록된다.",
            "failure_criteria": "DD repair loop(손실폭 수리 반복)가 생기면 중단한다.",
            "invalid_conditions": "duplicate-boundary treated as actual fallback(중복 경계를 실제 대체로 취급).",
            "runtime_instruction": "materialize only if needed as control receipt(필요 시 대조 영수증으로만 물질화).",
            "aggressive_or_defensive": "defensive_control(방어 대조)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q05_s264_aia_s262_lih_supply_manifest_diagnostic",
            "priority": "P1_diagnostic",
            "candidate_aliases": "s264_aia;s262_lih",
            "candidate_ids": "s264_allow_inner_all_oos_anchor;s262_lowrank_inner_half_filter",
            "workstream": "pre_runtime_supply_diagnostic(런타임 전 공급 진단)",
            "source_evidence": "current DS has no completed rows for these candidates; prior gap memory remains.",
            "changed_variables": "signal supply manifest(신호 공급 목록), feature activation count(피처 활성 수).",
            "control_variables": "no blind MT5 retry(눈먼 MT5 재시도 없음).",
            "sample_scope": "historical_2024 and prior weak slices as diagnostic only(2024 과거와 이전 약점 구간 진단 전용).",
            "success_criteria": "nonzero activation proof(비영 활성 증명)가 생성된다.",
            "failure_criteria": "activation proof missing(활성 증명 누락) or all-skip state(전체 스킵 상태).",
            "invalid_conditions": "diagnostic without source hashes(원천 해시 없는 진단).",
            "runtime_instruction": "do not schedule MT5 until diagnostic passes(진단 통과 전 MT5 배정 금지).",
            "aggressive_or_defensive": "diagnostic_only(진단 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q06_s264_aih_s258_similar_feature_replacement",
            "priority": "P1_replacement",
            "candidate_aliases": "s264_aih;s258_stc",
            "candidate_ids": "s264_allow_inner_high_quarter;s258_short_tight_control",
            "workstream": "similar_feature_replacement(유사 피처 대체)",
            "source_evidence": "goal requires feature/category ablation and similar replacement(유사 피처 대체).",
            "changed_variables": "ADX-like trend strength(ADX 유사 추세 강도), ATR-z impulse(ATR 표준화 충격), range expansion(범위 확장).",
            "control_variables": "same split windows(동일 구간), same candidate identities(동일 후보 정체성).",
            "sample_scope": "validation/OOS plus weak month zoom(검증/표본외 및 약한 월 확대).",
            "success_criteria": "candidate does not collapse under similar feature replacement(유사 피처 대체에서 완전 붕괴하지 않음).",
            "failure_criteria": "one-feature dependency(단일 피처 의존성) appears.",
            "invalid_conditions": "replacement changes label timing(대체가 라벨 시점을 바꿈) or feature leakage(피처 누수).",
            "runtime_instruction": "materialize after q03/q02 shape is available(q03/q02 형태 확보 후 물질화).",
            "aggressive_or_defensive": "aggressive_validation(공격형 검증)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "pr267dt_no_third_stage_supply_repair_loop",
            "affected_candidate_aliases": "s258_stc",
            "affected_attempts": "run267dq_01;run267dq_02;run267dq_03",
            "prune_label": "repair_once_only(수리 한 번만)",
            "why_pruned": "EBM table open failure(EBM 테이블 열기 실패)는 수리 대상이지만, 같은 분기를 3단계 이상 끌지 않는다.",
            "salvage_value": "수리 성공 시 supply continuity(공급 연속성) 성능을 처음으로 유효하게 볼 수 있다.",
            "reopen_condition": "preflight open check(사전 열기 점검)와 runtime output(런타임 출력)이 모두 성공할 때.",
            "do_not_repeat": "같은 table open failure(테이블 열기 실패)를 성능 실험처럼 반복하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dt_no_more_calendar_filter_stack",
            "affected_candidate_aliases": "s258_stc;s264_lc",
            "affected_attempts": "time-slice weak rows",
            "prune_label": "no_filter_stack(필터 덕지덕지 금지)",
            "why_pruned": "요일/월/시간 약점을 단순 배제 필터로 계속 덮으면 목표와 어긋난다.",
            "salvage_value": "시장 상태 의미가 있는 impulse/shock/replacement(충격/상태/대체) 축으로 전환한다.",
            "reopen_condition": "필터가 아니라 구조적 상태 피처로 설명될 때.",
            "do_not_repeat": "약한 월 하나를 줄이려고 비슷한 repair(수리)를 반복하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dt_duplicate_boundary_not_fallback",
            "affected_candidate_aliases": "s264_lc",
            "affected_attempts": "run267dq_07_rt_2024",
            "prune_label": "not_true_fallback(실제 대체 아님)",
            "why_pruned": "Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계)라 실제 routed total(라우팅 전체)이 아니다.",
            "salvage_value": "대조 해석의 경계로는 유용하다.",
            "reopen_condition": "actual routed total(실제 라우팅 전체) 텔레메트리가 생길 때.",
            "do_not_repeat": "중복 경계 숫자를 fallback(대체) 성과로 말하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "pr267dt_aia_lih_no_blind_runtime_retry",
            "affected_candidate_aliases": "s264_aia;s262_lih",
            "affected_attempts": "prior runtime gap routes",
            "prune_label": "diagnostic_before_retry(재시도 전 진단)",
            "why_pruned": "공급 증명 없이 MT5(MetaTrader 5, 메타트레이더5)를 반복하면 병목이 된다.",
            "salvage_value": "신호 공급만 증명되면 다시 후보군 경주에 올릴 수 있다.",
            "reopen_condition": "nonzero activation manifest(비영 활성 목록)가 생성될 때.",
            "do_not_repeat": "무거래/공백 경로를 같은 설정으로 재시도하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "fm267dt_ebm_table_open_failed_5003",
            "pattern": "init_failure_ebm_table_open_failed(초기화 실패 EBM 테이블 열기 실패)",
            "affected_scope": "s258_stc supply continuity run267dq_01/02/03",
            "why_failed": "runtime telemetry(런타임 텔레메트리)가 ebm_table_open_failed:5003을 남겼다.",
            "salvage_value": "table handoff repair(테이블 인계 수리) 후 처음으로 성능을 볼 수 있다.",
            "reopen_condition": "preflight open receipt(사전 열기 영수증)가 통과할 때.",
            "do_not_repeat": "init failure(초기화 실패)를 zero-trade success(무거래 성공)로 해석하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dt_s258_validation_oos_quality_decay",
            "pattern": "validation_oos_quality_decay(검증/표본외 품질 약화)",
            "affected_scope": "s258_stc monday late DD taper",
            "why_failed": "2025H1 net -3.69, 2025H2 net 33.93, PF near 1.0.",
            "salvage_value": "calendar filter(달력 필터)가 아니라 noncalendar impulse(비달력 충격)로 다시 볼 가치가 있다.",
            "reopen_condition": "2025H1 validation(검증)이 양수로 회복될 때.",
            "do_not_repeat": "시간대 필터만 더 붙이지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dt_s264_lc_dd_cluster",
            "pattern": "profit_with_uncomfortable_dd_cluster(수익 있지만 손실폭 군집 불편)",
            "affected_scope": "s264_lc historical_2024",
            "why_failed": "DD 24.39, Monday -235.05, 2024-06 -163.98.",
            "salvage_value": "defensive control(방어 대조) 경계로 유용하다.",
            "reopen_condition": "DD cluster(손실폭 군집)가 설명되고 대조 용도에 한정될 때.",
            "do_not_repeat": "수익이 크다는 이유로 선택 후보로 말하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267dt_s264_aih_oos_final_month_loss",
            "pattern": "oos_final_month_loss(표본외 마지막 달 손실)",
            "affected_scope": "s264_aih 2026.04",
            "why_failed": "initial scoreboard(초기 점수판)에서 OOS final month(표본외 마지막 달) 2026.04가 -41.14다.",
            "salvage_value": "explosive shock-state(폭발형 충격 상태) 실험의 표적 약점으로 쓸 수 있다.",
            "reopen_condition": "OOS PF(표본외 수익 팩터)를 유지하면서 2026.04 손실을 줄일 때.",
            "do_not_repeat": "OOS 전체 숫자만 보고 약한 마지막 달을 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_experiment_design_receipt() -> list[dict[str, Any]]:
    return [
        {
            "design_id": "ed267dt_runtime_gap_aware_fifth_followup_or_prune",
            "hypothesis": "DS 근거를 보면 s258_stc는 테이블 인계 실패와 성능 약화를 분리해야 하고, s264_aih는 다시 공격형 도전자로 압박해야 한다.",
            "decision_use": "run267DU(267DU 실행) 물질화 대상과 보류/가지치기 대상을 정한다.",
            "comparison_baseline": "run267DS(267DS 실행) candidate profile, init failure, negative slice evidence(후보 프로필/초기화 실패/음수 구간 근거).",
            "control_variables": "US100 M5, Stage267 후보군, split scope(구간 범위), no operating claim(운영 주장 없음).",
            "changed_variables": "EBM table handoff(EBM 테이블 인계), noncalendar impulse(비달력 충격), explosive shock-state(폭발형 충격 상태), similar replacement(유사 대체).",
            "sample_scope": "2023H2, historical_2024, validation_is, OOS, 2025H1/H2, 2026.04 weak final month.",
            "success_criteria": "수리 분기는 init failure(초기화 실패) 제거, 공격 분기는 거래 수/수익/PF/DD가 함께 개선, 대체 분기는 붕괴하지 않음.",
            "failure_criteria": "같은 초기화 실패 반복, 2025H1/H2 품질 재붕괴, s264_aih OOS 회복 소실, 단일 피처 의존성 확인.",
            "invalid_conditions": "feature order mismatch(피처 순서 불일치), data leakage(데이터 누수), missing report(보고서 누락), duplicate-boundary misread(중복 경계 오독).",
            "stop_conditions": "repair loop(수리 루프)는 최대 1개 후속 수리만 허용하고, 같은 약점 축 미세조정 반복은 중단한다.",
            "evidence_plan": "feature_blueprint, materialization_queue, failure_memory, run_manifest, gate_audit, DS source hashes, next DU materialization receipts.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_evidence_map() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "ev267dt_ds_summary_s258",
            "source_path": rel(SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH),
            "source_field": "s258_stc row",
            "observed_value": "attempt_count=6;completed=3;init_failure=3;avg_net=73.666667;max_dd=17.93",
            "used_for": "s258 repair and aggressive reentry design(수리와 공격 재진입 설계)",
            "effect": "성능 약화와 런타임 인계 실패를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267dt_ds_summary_s264_lc",
            "source_path": rel(SOURCE_CANDIDATE_INIT_FAILURE_SUMMARY_PATH),
            "source_field": "s264_lc row",
            "observed_value": "avg_net=1522.61;PF=1.418226;max_dd=24.39;worst_month=-163.98",
            "used_for": "defensive control DD cluster design(방어 대조 손실폭 군집 설계)",
            "effect": "수익이 커도 선택하지 않고 위험 경계로만 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267dt_s264_aih_scoreboard",
            "source_path": rel(INITIAL_SCOREBOARD_PATH),
            "source_field": "s264_allow_inner_high_quarter",
            "observed_value": "OOS net 857.67;OOS PF 1.74;final OOS month 2026.04 -41.14",
            "used_for": "explosive core challenger reentry(폭발형 핵심 도전자 재진입)",
            "effect": "방어 대조만 보던 흐름을 공격형 탐색으로 넓힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "ev267dt_goal_similar_replacement",
            "source_path": "user_goal_context(사용자 목표 문맥)",
            "source_field": "similar replacement requirement(유사 대체 요구)",
            "observed_value": "feature ablation/replacement must be revisited from baseline pool(기준 후보군 기준 재검토 필요)",
            "used_for": "q06 similar feature replacement queue(q06 유사 피처 대체 대기열)",
            "effect": "단일 피처 우연 적합인지 검증하는 다음 실험을 준비한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DT runtime gap aware fifth follow-up/prune design(267DT 런타임 공백 반영 5차 후속/가지치기 설계)",
            "evidence_available": "run267DS profile/init failure/negative slice evidence(프로필/초기화 실패/음수 구간 근거), initial scoreboard(초기 점수판), monthly weakness matrix(월별 약점 행렬)",
            "evidence_missing": "run267DU materialized artifacts(267DU 물질화 산출물), MT5 execution(메타트레이더5 실행), Adapter package(어댑터 패키지), ONNX parity(ONNX 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 작업은 다음 큐를 정한 설계이며, 후보 선택이나 ONNX 준비가 아니다.",
        }
    ]


def build_gate_audit(
    feature_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    prune_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "gate267dt_reentry_truth",
            "gate_name": "current truth agrees(현재 진실 일치)",
            "status": "passed",
            "evidence": "workspace_state and selection_status point to run267DS and next run267DT",
            "effect": "stale stage(낡은 단계)에서 시작하지 않았다.",
        },
        {
            "gate_id": "gate267dt_experiment_design",
            "gate_name": "experiment design fields present(실험 설계 필드 존재)",
            "status": "passed",
            "evidence": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "effect": "가설/비교/성공/실패/무효 조건을 먼저 고정했다.",
        },
        {
            "gate_id": "gate267dt_aggressive_included",
            "gate_name": "aggressive branch included(공격형 분기 포함)",
            "status": "passed" if any("aggressive" in str(row.get("aggressive_or_defensive")) or "explosive" in str(row.get("aggressive_or_defensive")) for row in queue_rows) else "failed",
            "evidence": f"queue_rows={len(queue_rows)};feature_rows={len(feature_rows)}",
            "effect": "방어 대조만 진행하지 않고 s258/s264_aih 공격형 실험을 포함했다.",
        },
        {
            "gate_id": "gate267dt_repair_loop_cap",
            "gate_name": "repair loop cap(수리 루프 제한)",
            "status": "passed",
            "evidence": f"prune_rows={len(prune_rows)}",
            "effect": "같은 초기화 실패 수리를 길게 끌지 않도록 stop condition(중단 조건)을 둔다.",
        },
        {
            "gate_id": "gate267dt_claim_boundary",
            "gate_name": "claim boundary held(주장 경계 유지)",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed",
            "effect": "운영/ONNX/목표 달성 주장을 만들지 않았다.",
        },
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    queue_rows = list(result["materialization_queue"])
    branch_rows = list(result["branch_decisions"])
    failure_rows = list(result["failure_memory"])
    lines = [
        "# Stage267 Run267DT Runtime Gap Aware Fifth Follow-Up/Prune Design(267단계 267DT 런타임 공백 반영 5차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- parent_run(부모 실행): `{PARENT_RUN_ID}`",
        f"- feature_blueprints(피처 청사진): `{len(result['feature_blueprints'])}`",
        f"- materialization_queue(물질화 대기열): `{len(queue_rows)}`",
        f"- prune_rows(가지치기 행): `{len(result['prune_matrix'])}`",
        f"- failure_memory(실패 기억): `{len(failure_rows)}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DT(267DT 실행)는 run267DS(267DS 실행)의 결과를 다음 실험 대기열(queue, 대기열)로 바꿨다.",
        "효과: s258_stc(258 STC 후보)는 테이블 인계 실패와 성능 약화를 분리하고, s264_lc(264 LC 후보)는 방어 대조로만 남기며, s264_aih(264 AIH 후보)는 폭발형 공격 실험으로 다시 전면에 올린다.",
        "즉, 수리(repair, 수리)만 하지 않고 공격형(explosive/aggressive, 폭발형/공격형) 탐색도 같이 밀어붙인다.",
        "",
        "## Queue(대기열)",
        "",
        "| queue_id(대기열 ID) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | intent(의도) |",
        "|---|---|---|---|---|",
    ]
    for row in queue_rows:
        lines.append(
            "| "
            f"`{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('candidate_aliases')}` | "
            f"`{row.get('workstream')}` | {row.get('runtime_instruction')} |"
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
            f"`{row.get('decision_id')}` | `{row.get('candidate_alias')}` | "
            f"{row.get('next_use')} | {row.get('stop_condition')} |"
        )
    lines.extend(
        [
            "",
            "## Failure Memory(실패 기억)",
            "",
            "| memory(기억) | affected_scope(영향 범위) | do_not_repeat(반복 금지) |",
            "|---|---|---|",
        ]
    )
    for row in failure_rows:
        lines.append(
            "| "
            f"`{row.get('memory_id')}` | {row.get('affected_scope')} | {row.get('do_not_repeat')} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run267DT(267DT 실행)는 design(설계)이다. MT5(MetaTrader 5, 메타트레이더5) 실행 결과, Adapter(어댑터) 패키지, ONNX parity(ONNX 동등성)는 아직 없다.",
            "따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DT_producer", "producer_script", PRODUCER_PATH, "Builds run267DT fifth follow-up/prune design."),
        ("stage267_run267DT_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267DS review result."),
        ("stage267_run267DT_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Feature blueprints for next queue."),
        ("stage267_run267DT_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decisions."),
        ("stage267_run267DT_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Next materialization queue."),
        ("stage267_run267DT_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune and stop-loop matrix."),
        ("stage267_run267DT_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267DT_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DT_evidence_map", "evidence_map", EVIDENCE_MAP_PATH, "Evidence map."),
        ("stage267_run267DT_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DT_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DT_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DT_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DT_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267DT_report", "review_report", REPORT_PATH, "User-facing report."),
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


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"queue_rows={len(result['materialization_queue'])};"
        f"aggressive_rows={result['aggressive_queue_count']};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267DT_runtime_gap_aware_fifth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_fifth_followup_or_prune_design",
        "tier_scope": "design_only_from_run267DS_and_initial_scoreboard; no MT5 result",
        "scoreboard": "experiment_design_queue_prune_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_fifth_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_fifth_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_fifth_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_fifth_followup_or_prune_design",
        "tier_scope": "design only; Tier rows must be materialized and tested in run267DU+",
        "kpi_scope": "experiment_design_queue_prune_failure_memory",
        "scoreboard_lane": "runtime_gap_aware_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={len(result['materialization_queue'])};aggressive_rows={result['aggressive_queue_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}. Design includes repair cap and aggressive branches.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


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


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267DT_runtime_gap_aware_fifth_followup_or_prune_design"
        f"(267DT 런타임 공백 반영 5차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_design(최신 설계): run267DT(267DT 실행) queue_rows(대기열 행) "
        f"`{len(result['materialization_queue'])}`, aggressive_rows(공격형 행) `{result['aggressive_queue_count']}`, "
        f"prune_rows(가지치기 행) `{len(result['prune_matrix'])}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DT(267DT 실행)는 run267DS(267DS 실행)의 초기화 실패/약점 구간을 다음 materialization queue(물질화 대기열)로 바꿨다.",
            f"Effect(효과): repair gate(수리 게이트) `1`, aggressive/explosive branch(공격/폭발 분기) `{result['aggressive_queue_count']}`, defensive control(방어 대조) `1`, diagnostic(진단) `1`을 나눴다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_fifth_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "stage267_run267DS_runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures.md", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267DT(267DT 실행)는 run267DS", block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "stage267_run267DS_runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality", report_line)
    selection = append_block_once(selection, "Run267DT(267DT 실행)는 run267DS", block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "stage267_run267DS_runtime_gap_aware_fourth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures.md", report_line)
    review_index = append_block_once(review_index, "Run267DT(267DT 실행)는 run267DS", block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = update_stage267_workspace_block(workspace)
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DT(267DT 실행) runtime gap aware fifth follow-up/prune design"
        f"(런타임 공백 반영 5차 후속/가지치기 설계) `{STATUS}`. "
        f"Effect(효과): run267DS(267DS 실행)의 init failure(초기화 실패), weak slices(약한 구간), s264_aih prior clue(이전 단서)를 "
        f"materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개와 aggressive/explosive branch(공격/폭발 분기) `{result['aggressive_queue_count']}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_design() -> dict[str, Any]:
    created_at = utc_now()
    _ = source_maps()
    feature_rows = build_feature_blueprints()
    branch_rows = build_branch_decisions()
    queue_rows = build_materialization_queue()
    prune_rows = build_prune_matrix()
    failure_rows = build_failure_memory()
    experiment_rows = build_experiment_design_receipt()
    evidence_rows = build_evidence_map()
    result_judgment = build_result_judgment()
    gate_rows = build_gate_audit(feature_rows, queue_rows, prune_rows)
    aggressive_count = sum(
        1
        for row in queue_rows
        if "aggressive" in str(row.get("aggressive_or_defensive")) or "explosive" in str(row.get("aggressive_or_defensive"))
    )
    result: dict[str, Any] = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "feature_blueprints": feature_rows,
        "branch_decisions": branch_rows,
        "materialization_queue": queue_rows,
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
    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "queue_count": len(queue_rows),
        "aggressive_queue_count": aggressive_count,
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
            "source_attribution": rel(SOURCE_ATTRIBUTION_PATH),
            "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
            "initial_scoreboard": rel(INITIAL_SCOREBOARD_PATH),
            "monthly_weakness": rel(MONTHLY_WEAKNESS_PATH),
            "equity_shape": rel(EQUITY_SHAPE_PATH),
        },
        "outputs": result["outputs"],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(FEATURE_BLUEPRINT_PATH, feature_rows, FEATURE_BLUEPRINT_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, branch_rows, BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, queue_rows, MATERIALIZATION_QUEUE_COLUMNS)
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
