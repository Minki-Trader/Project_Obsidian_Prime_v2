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
    run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267CM"
RUN_ID = "run267CM_stage267_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_completed"
JUDGMENT = "followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CN_materialize_pool_wide_shared_weakness_breakout_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_loss_shape_state_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

FEATURE_BLUEPRINT_PATH = RUN_ROOT / "feature_blueprint.csv"
BRANCH_DECISION_PATH = RUN_ROOT / "branch_decisions.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.py")

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)

CANDIDATE_POOL = (
    {
        "candidate_alias": "s264_aih",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_role": "core_challenger(핵심 도전자)",
    },
    {
        "candidate_alias": "s264_lc",
        "candidate_id": "s264_lowrank_control",
        "candidate_role": "defensive_control(방어 대조)",
    },
    {
        "candidate_alias": "s262_lih",
        "candidate_id": "s262_lowrank_inner_half_filter",
        "candidate_role": "validation_heavy(검증 중심)",
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

FEATURE_BLUEPRINT_COLUMNS = (
    "feature_id",
    "feature_family",
    "market_meaning",
    "candidate_scope",
    "source_evidence",
    "changed_variables",
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
    "source_profile",
    "net_profit",
    "profit_factor",
    "equity_drawdown_percent",
    "trade_count",
    "worst_month",
    "worst_month_net",
    "weakest_weekday_net",
    "decision_label",
    "next_use",
    "why",
    "risk_boundary",
    "reopen_condition",
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


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isfinite(value):
            return round(value, 6)
        return ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return value


def as_float(value: Any, default: float | None = None) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int | None = None) -> int | None:
    try:
        return int(float(value))
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def prepend_current_focus(text: str, focus_line: str) -> str:
    if f"`{STATUS}`" in text:
        return text
    return text.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)


def feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "shared_weakness_state_interaction",
            "feature_family": "state_interaction(상태 상호작용)",
            "market_meaning": "Monday(월요일), 2024-12(2024년 12월), session_07_12(7-12 세션) 약점이 달력이 아니라 변동성/방향/손실군집 상태인지 본다.",
            "candidate_scope": "all_baseline_candidates(전체 기준 후보)",
            "source_evidence": "run267CL negative_slices(음수 구간) 11 rows; both s264_lc and s264_aia share Monday and 2024-12 weakness",
            "changed_variables": "volatility shock state(변동성 충격 상태); impulse age(임펄스 나이); loss-cluster pressure(손실군집 압박)",
            "do_not_use_as": "literal weekday/month/session filter(요일/월/세션 직접 필터)",
            "success_read": "weak slices improve without trade-count collapse(거래 수 붕괴 없이 약점 구간 완화)",
            "failure_read": "headline profit survives but weak slices remain deep(대표 수익은 남지만 약점 구간이 깊게 유지)",
            "materialization_note": "create score-table features rather than hard calendar gates(달력 게이트가 아니라 점수표 피처로 만든다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "aggressive_shock_release_reentry",
            "feature_family": "aggressive_feature_engineering(공격형 피처 엔지니어링)",
            "market_meaning": "강한 변동성 이후 눌림/재가속을 폭발형 후보가 더 넓게 잡을 수 있는지 본다.",
            "candidate_scope": "s264_aih;s264_aia;s264_lc",
            "source_evidence": "run267CL keeps profit but curve holes remain; user goal requires aggressive experiments",
            "changed_variables": "shock-release score(충격 해소 점수); reentry impulse slope(재진입 임펄스 기울기); payoff asymmetry relief(보상 비대칭 완화)",
            "do_not_use_as": "extra safety filter stack(추가 방어 필터 더미)",
            "success_read": "net and trades expand while DD and Monday/December holes do not worsen(순수익/거래 수가 늘고 손실폭과 월요일/12월 구멍은 악화하지 않음)",
            "failure_read": "more trades only deepen DD or weak months(거래만 늘고 손실폭/약한 월이 더 깊어짐)",
            "materialization_note": "force at least one explosive branch in run267CN(267CN에서 폭발형 분기를 최소 하나 강행)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "defensive_anchor_holdout_trace",
            "feature_family": "control_trace(대조 추적)",
            "market_meaning": "s264_lc와 s264_aia를 선택 후보가 아니라 다음 폭발형 실험의 방어/앵커 비교선으로 쓴다.",
            "candidate_scope": "s264_lc;s264_aia",
            "source_evidence": "s264_lc net 1207.3 PF 1.506786 DD 17.62; s264_aia net 1119.33 PF 1.548395 DD 16.03",
            "changed_variables": "none for control rows(대조 행은 변경 없음)",
            "do_not_use_as": "selected candidate(선택 후보)",
            "success_read": "new branch beats controls across curve/time-slice/trade-quality(새 분기가 곡선/시간구간/거래품질에서 대조를 이김)",
            "failure_read": "new branch only improves headline KPI(새 분기가 대표 KPI만 개선)",
            "materialization_note": "carry as holdout/control in next manifest(다음 목록에서 보류/대조로 동행)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def source_row_by_alias(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("candidate_alias")): row for row in rows}


def branch_decisions(candidate_rows: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    candidate_by_alias = source_row_by_alias(candidate_rows)
    summary_by_alias = source_row_by_alias(summary_rows)
    decisions: list[dict[str, Any]] = []
    for candidate in CANDIDATE_POOL:
        alias = str(candidate["candidate_alias"])
        row = candidate_by_alias.get(alias, {})
        summary = summary_by_alias.get(alias, {})
        if alias == "s264_lc":
            label = "hold_control_prune_same_axis_repair(대조 보류, 같은 축 수리 가지치기)"
            next_use = "defensive_control_for_shared_weakness_breakout(공유 약점 돌파 방어 대조)"
            why = "profit is strong but Monday -241.79 and 2024-12 -234.28 remain too deep after follow-up(수익은 강하지만 후속 뒤에도 월요일/2024-12 약점이 깊다)"
            risk = "do not spend a third same-axis repair stage(같은 축 수리 3단계 이상 소모 금지)"
            reopen = "reopen only if a new state-interaction feature reduces weak slices without shrinking trades(새 상태 상호작용 피처가 거래 수 축소 없이 약점 구간을 낮출 때)"
        elif alias == "s264_aia":
            label = "retain_oos_anchor_watch_no_selection(표본외 앵커 관찰 유지, 선택 아님)"
            next_use = "oos_anchor_control_for_shared_weakness_breakout(공유 약점 돌파 표본외 앵커 대조)"
            why = "PF is cleaner than s264_lc but Monday -303.41 is the worst run267CL slice(PF는 더 깨끗하지만 월요일 -303.41이 run267CL 최악 구간이다)"
            risk = "anchor role only; no selected candidate claim(앵커 역할만, 선택 후보 주장 없음)"
            reopen = "reopen after cross-candidate state attribution improves Monday and 2024-12(후보군 공통 상태 귀속이 월요일/2024-12를 완화할 때)"
        elif alias == "s264_aih":
            label = "reopen_aggressive_challenger_blast(공격형 도전자 재개)"
            next_use = "aggressive_shock_release_reentry_branch(공격형 충격 해소 재진입 분기)"
            why = "run267CL only followed s264_lc/s264_aia; the core challenger must not be lost while defensive follow-up loops(267CL은 두 후보만 봤고 방어 후속이 길어지는 동안 핵심 도전자를 잃으면 안 된다)"
            risk = "aggressive experiment may fail, but failure is valuable if recorded(공격 실험은 실패할 수 있으나 기록되면 가치가 있다)"
            reopen = "materialize if feature blueprint is structural, not another filter stack(새 피처가 필터 더미가 아니라 구조일 때 물질화)"
        elif alias == "s262_lih":
            label = "retain_validation_heavy_control(검증 중심 대조 유지)"
            next_use = "validation_damage_detector_for_new_features(새 피처 검증 손상 감지기)"
            why = "validation-heavy role is useful to detect whether aggressive features damage stability(공격형 피처가 안정성을 망치는지 보는 대조로 유용하다)"
            risk = "do not force it into an explosive role(폭발형 역할을 억지 부여하지 않음)"
            reopen = "use when new features need validation-style damage check(새 피처 검증 손상 점검이 필요할 때)"
        else:
            label = "stress_comparator_only_no_deep_repair(압박 비교 전용, 깊은 수리 없음)"
            next_use = "stress_comparator_receipt(압박 비교 영수증)"
            why = "stress challenger remains useful, but repeated repair would violate loop limit(압박 도전자는 유용하지만 반복 수리는 루프 제한에 걸린다)"
            risk = "do not chase headline OOS numbers with filters(대표 표본외 숫자를 필터로 쫓지 않음)"
            reopen = "reopen only if a broad structural feature reduces DD without trade-count collapse(넓은 구조 피처가 거래 수 붕괴 없이 손실폭을 낮출 때)"
        decisions.append(
            {
                "decision_id": f"run267cm_d_{alias}",
                "candidate_alias": alias,
                "candidate_id": candidate["candidate_id"],
                "candidate_role": candidate["candidate_role"],
                "source_profile": row.get("test_id", "not_in_run267CL_followup_scope(run267CL 후속 범위 밖)"),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", summary.get("avg_profit_factor", "")),
                "equity_drawdown_percent": row.get("report_equity_drawdown_percent", summary.get("avg_equity_drawdown_percent", "")),
                "trade_count": row.get("trade_count", summary.get("avg_trade_count", "")),
                "worst_month": row.get("worst_month", ""),
                "worst_month_net": row.get("worst_month_net", summary.get("worst_month_floor", "")),
                "weakest_weekday_net": row.get("weakest_weekday_net", ""),
                "decision_label": label,
                "next_use": next_use,
                "why": why,
                "risk_boundary": risk,
                "reopen_condition": reopen,
            }
        )
    return decisions


def materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run267cn_q01_shared_monday_december_state_interaction",
            "priority": "P0",
            "workstream": "shared_weakness_state_breakout(공유 약점 상태 돌파)",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia;s258_stc",
            "feature_blueprint_scope": "shared_weakness_state_interaction",
            "hypothesis": "The repeated Monday/December/session holes are state interactions, not calendar permissions(반복된 월요일/12월/세션 구멍은 달력 허용이 아니라 상태 상호작용이다).",
            "decision_use": "Decide whether to pivot from candidate-local repair to pool-wide state features(후보별 수리에서 후보군 전체 상태 피처로 틀지 판단).",
            "comparison_baseline": "run267CL s264_lc and s264_aia plus prior Stage267 pool-wide reviews(267CL 두 후보와 이전 후보군 전체 검토).",
            "control_variables": "US100 M5, historical 2024, MT5 tester settings, candidate source identity(US100 M5, 2024, MT5 설정, 후보 정체성).",
            "changed_variables": "state interaction feature family only(상태 상호작용 피처군만 변경).",
            "sample_scope": "Tier A and duplicate-boundary Tier A+B historical 2024; true Tier B fallback remains blocked(티어 A와 중복 경계 Tier A+B 2024; 진짜 Tier B 대체는 차단).",
            "success_criteria": "Monday and 2024-12 improve by at least 30% while trade count stays useful(월요일과 2024-12가 30% 이상 완화되고 거래 수가 유지).",
            "failure_criteria": "weak slices stay deep or trade count collapses(약점 구간 유지 또는 거래 수 붕괴).",
            "invalid_conditions": "calendar-only filter, missing source identity, parser mismatch(달력 단독 필터, 원천 정체성 누락, 파서 불일치).",
            "stop_conditions": "if all candidates still show deep common holes, stop this branch and pivot to new feature structure(모든 후보가 같은 구멍이면 중단하고 새 구조로 전환).",
            "materialization_instruction": "Build score-table/model/set/ini inputs for state-interaction features without new EA copy(새 EA 복사 없이 점수표/모델/설정/초기화 입력 생성).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cn_q02_s264_aih_aggressive_shock_release_reentry",
            "priority": "P0",
            "workstream": "aggressive_explosive_reentry(공격형 폭발 재진입)",
            "candidate_aliases": "s264_aih",
            "feature_blueprint_scope": "aggressive_shock_release_reentry",
            "hypothesis": "The core challenger can regain trade supply through shock-release structure, not more filters(핵심 도전자는 필터 추가가 아니라 충격 해소 구조로 거래 공급을 되찾을 수 있다).",
            "decision_use": "Keep the R&D race aggressive instead of only defensive(연구개발 경주가 방어만 하지 않게 함).",
            "comparison_baseline": "run267CL s264_lc net 1207.3 and s264_aia net 1119.33 controls(267CL 두 대조 수익).",
            "control_variables": "same symbol/timeframe/period/tester profile(같은 심볼/시간봉/기간/테스터 프로필).",
            "changed_variables": "shock-release score, reentry impulse slope, payoff asymmetry relief(충격 해소 점수, 재진입 임펄스 기울기, 보상 비대칭 완화).",
            "sample_scope": "historical 2024 first, then cross-period if not fragile(2024 우선, 취약하지 않으면 확장 기간).",
            "success_criteria": "net > 1200, PF >= 1.45, DD < 22%, trades > 300, Monday > -180(순수익 1200 초과, PF 1.45 이상, 손실폭 22% 미만, 거래 300 초과, 월요일 -180 초과).",
            "failure_criteria": "profit comes from deeper DD or fewer than 180 trades(더 깊은 손실폭 또는 180 미만 거래에서 수익 발생).",
            "invalid_conditions": "feature order not traceable or score table cannot be reproduced(피처 순서 추적 불가 또는 점수표 재현 불가).",
            "stop_conditions": "one materialization plus one MT5 review; no long repair loop(물질화 1회와 MT5 검토 1회, 긴 수리 루프 금지).",
            "materialization_instruction": "Force one explosive candidate branch in run267CN(267CN에서 폭발형 후보 분기 하나 강행).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cn_q03_anchor_control_holdout_trace",
            "priority": "P1",
            "workstream": "anchor_control_holdout(앵커/대조 보류 추적)",
            "candidate_aliases": "s264_lc;s264_aia",
            "feature_blueprint_scope": "defensive_anchor_holdout_trace",
            "hypothesis": "The two profitable follow-ups are useful as controls, not as selected candidates(두 양수 후속은 선택 후보가 아니라 대조로 유용하다).",
            "decision_use": "Prevent headline KPI selection while measuring new branches(대표 KPI 선택을 막고 새 분기를 측정).",
            "comparison_baseline": "run267CL candidate_profile_review and negative_slice_summary(267CL 후보 프로필 검토와 음수 구간 요약).",
            "control_variables": "keep exact run267CL decision surfaces for control rows(대조 행은 267CL 의사결정 표면 유지).",
            "changed_variables": "none for control rows(대조 행 변경 없음).",
            "sample_scope": "same historical 2024 comparison manifest(같은 2024 비교 목록).",
            "success_criteria": "new branches beat controls on weak-slice and curve metrics(새 분기가 약점 구간과 곡선 지표에서 대조를 이김).",
            "failure_criteria": "new branches only beat headline profit(새 분기가 대표 수익만 이김).",
            "invalid_conditions": "control identity drifts(대조 정체성 드리프트).",
            "stop_conditions": "close if controls remain cleaner than all aggressive branches(대조가 모든 공격 분기보다 깨끗하면 닫음).",
            "materialization_instruction": "Include as unchanged controls in run267CN manifest(267CN 목록에 변경 없는 대조로 포함).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cn_q04_validation_and_stress_guardrails",
            "priority": "P2",
            "workstream": "guardrail_receipts(가드레일 영수증)",
            "candidate_aliases": "s262_lih;s258_stc",
            "feature_blueprint_scope": "shared_weakness_state_interaction;defensive_anchor_holdout_trace",
            "hypothesis": "Validation-heavy and stress roles can catch overfit damage from new features(검증 중심/압박 역할이 새 피처 과적합 손상을 잡을 수 있다).",
            "decision_use": "Keep baseline pool role separation(기준 후보군 역할 분리 유지).",
            "comparison_baseline": "Stage267 baseline candidate pool role matrix(267단계 후보군 역할 행렬).",
            "control_variables": "candidate roles and source identities(후보 역할과 원천 정체성).",
            "changed_variables": "guardrail receipt only unless run267CN needs a minimal control row(267CN에 최소 대조 행이 필요할 때만 변경).",
            "sample_scope": "design/materialization boundary only(설계/물질화 경계).",
            "success_criteria": "new feature queue names validation/stress failure conditions(새 피처 대기열이 검증/압박 실패 조건을 이름 붙임).",
            "failure_criteria": "new feature queue ignores validation or DD risk(새 피처 대기열이 검증 또는 손실폭 위험 무시).",
            "invalid_conditions": "role drift into selected baseline claim(선택 기준 후보 주장으로 역할 드리프트).",
            "stop_conditions": "if roles add no evidence, keep as failure memory only(근거를 못 더하면 실패 기억만 유지).",
            "materialization_instruction": "Add only if needed as guardrail rows(가드레일 행이 필요할 때만 추가).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "run267cm_p01_no_same_axis_third_repair",
            "prune_label": "no_same_axis_third_repair(같은 축 3차 수리 금지)",
            "affected_scope": "s264_lc controlled impulse DD state throttle; s264_aia OOS anchor impulse pressure",
            "why_pruned": "run267CI->CJ->CK->CL already consumed a bounded follow-up loop(267CI부터 CL까지 이미 경계 후속 루프를 썼다).",
            "reopen_condition": "new state-interaction feature, not threshold polish(임계값 미세조정이 아닌 새 상태 상호작용 피처).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267cm_p02_no_literal_calendar_filter",
            "prune_label": "no_literal_calendar_filter(달력 직접 필터 금지)",
            "affected_scope": "Monday, 2024-12, session_07_12_report_time",
            "why_pruned": "calendar filter would hide the weakness rather than explain it(달력 필터는 약점을 설명하지 않고 숨긴다).",
            "reopen_condition": "calendar used only as attribution label, not permission rule(달력은 귀속 라벨로만 사용).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267cm_p03_no_headline_profit_selection",
            "prune_label": "no_headline_profit_selection(대표 수익 선택 금지)",
            "affected_scope": "run267CL profitable rows",
            "why_pruned": "positive net/PF still has deep weak slices(양수 순수익/PF에도 깊은 약점 구간이 있다).",
            "reopen_condition": "balance/equity curve and time-slice review survive next pressure(다음 압박에서 잔액/평가금 곡선과 시간구간 검토가 버팀).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "run267cm_p04_no_onnx_adapter_claim",
            "prune_label": "no_onnx_or_adapter_claim(ONNX/어댑터 주장 금지)",
            "affected_scope": "run267CM design outputs",
            "why_pruned": "design outputs are not runtime reproduction or ONNX parity evidence(설계 산출물은 런타임 재현이나 ONNX 동등성 근거가 아니다).",
            "reopen_condition": "after R&D racing survivor, Adapter package, runtime reproduction, and ONNX parity evidence(연구개발 생존자, 어댑터 패키지, 런타임 재현, ONNX 동등성 근거 이후).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    def evidence(axis: str, bucket: str) -> str:
        matched = [
            f"{row.get('candidate_alias')}:{row.get('test_id')} net={row.get('net_profit')} trades={row.get('trade_count')}"
            for row in negative_rows
            if row.get("axis") == axis and row.get("bucket") == bucket
        ]
        return " | ".join(matched) if matched else "not present in source rows(원천 행에 없음)"

    return [
        {
            "memory_id": "run267cm_m01_monday_cluster",
            "pattern": "shared_monday_loss_cluster(공유 월요일 손실 군집)",
            "affected_scope": "s264_lc;s264_aia",
            "evidence": evidence("weekday", "Monday"),
            "why_fragile": "both profitable follow-ups lose deeply on Monday(두 양수 후속 모두 월요일에 깊게 진다).",
            "do_not_repeat": "do not add Monday-off filter(월요일 제외 필터 추가 금지)",
            "salvage_angle": "attribute to volatility/impulse/loss-cluster state(변동성/임펄스/손실군집 상태로 귀속)",
            "reopen_condition": "state feature reduces Monday drawdown without killing trades(상태 피처가 거래 수를 죽이지 않고 월요일 손실폭 완화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267cm_m02_december_hole",
            "pattern": "2024_12_drawdown_hole(2024년 12월 손실 구멍)",
            "affected_scope": "s264_lc;s264_aia",
            "evidence": evidence("month", "2024-12"),
            "why_fragile": "December remains a deep month hole after follow-up(후속 뒤에도 12월 구멍이 깊다).",
            "do_not_repeat": "do not tune a December-only threshold(12월 전용 임계값 튜닝 금지)",
            "salvage_angle": "treat as regime-transition pressure(레짐 전환 압박으로 취급)",
            "reopen_condition": "cross-period state feature also helps adjacent weak months(확장 기간 상태 피처가 인접 약한 월에도 도움)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267cm_m03_session_07_12_sparse_loss",
            "pattern": "sparse_session_loss(희소 세션 손실)",
            "affected_scope": "s264_lc;s264_aia",
            "evidence": evidence("session_report", "session_07_12_report_time"),
            "why_fragile": "only three trades can still carve a sharp hole(세 거래만으로도 날카로운 구멍을 만든다).",
            "do_not_repeat": "do not overfit sparse session count(희소 세션 수에 과적합 금지)",
            "salvage_angle": "use as attribution warning, not selection rule(선택 규칙이 아니라 귀속 경고로 사용)",
            "reopen_condition": "session weakness appears with enough trades in next materialized run(다음 물질화 실행에서 충분한 거래 수로 세션 약점 재현)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267cm_m04_tier_fallback_boundary",
            "pattern": "duplicate_boundary_not_true_fallback(중복 경계, 진짜 대체 아님)",
            "affected_scope": "run267CL evidence boundary",
            "evidence": "Tier A and duplicate-boundary Tier A+B only; true Tier B fallback remains blocked",
            "why_fragile": "broad claims need true fallback or explicit lower scope(넓은 주장은 진짜 대체 또는 낮춘 범위가 필요).",
            "do_not_repeat": "do not call duplicate-boundary rows actual routed totals(중복 경계 행을 실제 라우팅 전체로 부르지 않음)",
            "salvage_angle": "carry boundary into run267CN manifest(267CN 목록에 경계를 동행)",
            "reopen_condition": "true fallback manifest exists(진짜 대체 목록 존재)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def experiment_design_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"{row['queue_id']}_design_receipt",
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
            "evidence_plan": "run267CN manifest, score tables, MT5 execution, parser checks, balance/time-slice/trade-quality review(267CN 목록, 점수표, MT5 실행, 파서 점검, 잔액/시간구간/거래품질 검토).",
        }
        for row in queue_rows
    ]


def result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
            "evidence_available": "run267CL review_result, candidate profile review, candidate summary, negative slice summary, source report",
            "evidence_missing": "run267CN materialization, MT5 execution, new trade list, Adapter package, runtime reproduction, ONNX parity",
            "judgment_label": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "수익이 있어도 약점이 깊어서 선택하지 않고, 같은 축 수리는 끊고, 후보군 전체 상태 피처와 공격형 분기로 넘긴다.",
        }
    ]


def gate_audit(queue_rows: Sequence[Mapping[str, Any]], prune_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "work_packet_schema_lint(작업 묶음 스키마 점검)",
            "status": "completed(완료)",
            "evidence": f"queue_rows={len(queue_rows)}; experiment_design_receipt={rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}",
            "effect": "hypothesis/comparison/controls/success/failure/stop/evidence are named(가설/비교/대조/성공/실패/중단/근거가 이름 붙음).",
        },
        {
            "gate_id": "repair_loop_limit(수리 루프 제한)",
            "status": "completed(완료)",
            "evidence": "run267cm_p01_no_same_axis_third_repair",
            "effect": "s264_lc/s264_aia same-axis repair does not drag beyond this design(같은 축 수리를 더 끌지 않음).",
        },
        {
            "gate_id": "aggressive_experiment_presence(공격 실험 존재)",
            "status": "completed(완료)",
            "evidence": "run267cn_q02_s264_aih_aggressive_shock_release_reentry",
            "effect": "defensive-only research drift is interrupted(방어 전용 연구 드리프트를 끊음).",
        },
        {
            "gate_id": "no_filter_stack(필터 덧붙이기 금지)",
            "status": "completed(완료)",
            "evidence": f"prune_rows={len(prune_rows)}; feature_blueprint={rel(FEATURE_BLUEPRINT_PATH)}",
            "effect": "weakness is turned into state features, not calendar filters(약점을 달력 필터가 아니라 상태 피처로 바꿈).",
        },
        {
            "gate_id": "final_claim_guard(최종 주장 보호)",
            "status": "completed(완료)",
            "evidence": "selected_candidate=none; selected_research_baseline=none; onnx_readiness=not_claimed; goal_achieve=not_claimed",
            "effect": "design evidence cannot become ONNX or operating claim(설계 근거가 ONNX나 운영 주장으로 바뀌지 않음).",
        },
    ]


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267CM_design_script", "producer_script", PRODUCER_PATH, "Builds run267CM follow-up/prune design."),
        ("stage267_run267CM_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267CL review result."),
        ("stage267_run267CM_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Run267CM feature blueprint."),
        ("stage267_run267CM_branch_decisions", "branch_decisions", BRANCH_DECISION_PATH, "Run267CM candidate branch decisions."),
        ("stage267_run267CM_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267CM next materialization queue."),
        ("stage267_run267CM_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Run267CM prune matrix."),
        ("stage267_run267CM_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267CM failure memory."),
        ("stage267_run267CM_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267CM experiment design receipt."),
        ("stage267_run267CM_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CM result judgment."),
        ("stage267_run267CM_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CM gate audit."),
        ("stage267_run267CM_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CM run manifest."),
        ("stage267_run267CM_lineage", "lineage", LINEAGE_PATH, "Run267CM lineage."),
        ("stage267_run267CM_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CM review result."),
        ("stage267_run267CM_report", "review_report", REPORT_PATH, "User-facing run267CM report."),
    ]
    rows = []
    for artifact_id, artifact_type, path, notes in entries:
        rows.append(
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
        )
    return rows


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267CM Follow-Up/Prune Design(267단계 267CM 후속/가지치기 설계)",
        "",
        "- action(행동): run267CL(267CL 실행)의 follow-up review(후속 검토)를 branch decision(분기 판단), materialization queue(물질화 대기열), prune matrix(가지치기 행렬)로 바꿨다.",
        "- effect(효과): 수익이 있는 두 후보를 성급히 고르지 않고, 같은 축 수리 루프를 끊고, 후보군 전체 상태 피처와 공격형 분기로 다음 실험을 연다.",
        f"- status(상태): `{STATUS}`",
        f"- feature_blueprints(피처 청사진): `{result['feature_blueprint_count']}`",
        f"- branch_decisions(분기 판단): `{result['branch_decision_count']}`",
        f"- materialization_queue_rows(물질화 대기열 행): `{result['materialization_queue_count']}`",
        f"- prune_rows(가지치기 행): `{result['prune_count']}`",
        f"- failure_memory_rows(실패 기억 행): `{result['failure_memory_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267CL(267CL 실행)은 `s264_lc`와 `s264_aia`가 수익은 낼 수 있지만 Monday(월요일), 2024-12(2024년 12월), session_07_12(7-12 세션)에서 깊게 파인다는 것을 보여줬다. 그래서 이번 run267CM(267CM 실행)은 두 후보를 고르지 않는다.",
        "",
        "핵심 판단은 두 가지다. 첫째, `s264_lc`와 `s264_aia`의 같은 축 repair(수리)는 여기서 끊고 control(대조)로만 남긴다. 둘째, 후보군 전체의 shared weakness(공유 약점)를 state interaction feature(상태 상호작용 피처)로 다시 열고, `s264_aih`는 aggressive shock-release reentry(공격형 충격 해소 재진입)로 강행한다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | role(역할) | source profile(원천 프로필) | net(순수익) | DD%(손실폭) | decision(판단) | next use(다음 용도) |",
        "| --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in result["branch_decisions"]:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['candidate_role']} | `{row['source_profile']}` | {cell(row['net_profit'])} | "
            f"{cell(row['equity_drawdown_percent'])} | {row['decision_label']} | {row['next_use']} |"
        )
    lines.extend(
        [
            "",
            "## Materialization Queue(물질화 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | success(성공 기준) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["materialization_queue"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | {row['workstream']} | {row['success_criteria']} |"
        )
    lines.extend(
        [
            "",
            "## Prune Matrix(가지치기 행렬)",
            "",
            "| prune(가지치기) | label(라벨) | affected(대상) | reopen(재개 조건) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in result["prune_matrix"]:
        lines.append(f"| `{row['prune_id']}` | {row['prune_label']} | {row['affected_scope']} | {row['reopen_condition']} |")
    lines.extend(
        [
            "",
            "## Failure Memory(실패 기억)",
            "",
            "| memory(기억) | pattern(패턴) | affected(대상) | do not repeat(반복 금지) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in result["failure_memory"]:
        lines.append(f"| `{row['memory_id']}` | {row['pattern']} | {row['affected_scope']} | {row['do_not_repeat']} |")
    lines.extend(
        [
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design`.",
            "- judgment_label(판정 라벨): `exploratory_design_only(탐색 설계 전용)`.",
            "- evidence_available(사용 가능 근거): run267CL(267CL 실행) review_result(검토 결과), candidate profile review(후보 프로필 검토), negative slice summary(음수 구간 요약).",
            "- evidence_missing(누락 근거): run267CN(267CN 실행) materialization(물질화), MT5(MetaTrader 5, 메타트레이더5) execution(실행), 새 trade list(거래 목록), Adapter(어댑터), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- source_review_result(원천 검토 결과): `{rel(SOURCE_REVIEW_RESULT_PATH)}`",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decisions(분기 판단): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design(267CM 후보군 전체 직교 손실 형태/상태 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    summary_line = (
        "- run267CM_summary(267CM 요약): Run267CM(267CM 실행)은 run267CL(267CL 실행)의 양수 후보를 선택하지 않고, "
        f"feature blueprint(피처 청사진) `{result['feature_blueprint_count']}`개, branch decision(분기 판단) `{result['branch_decision_count']}`개, "
        f"materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개, prune row(가지치기 행) `{result['prune_count']}`개로 바꿨다. "
        "Effect(효과): 같은 축 수리 루프는 끊고, 공유 약점 상태 피처와 공격형 s264_aih 분기로 다음 실행을 연다."
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_loss_shape_state_followup_or_prune_design`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "Run267CM(267CM 실행)은", summary_line)
            text = append_after_contains(text, "stage267_run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design", summary_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review.md", report_line)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CM(267CM 실행) pool-wide orthogonal loss-shape/state follow-up or prune design"
        f"(후보군 전체 직교 손실 형태/상태 후속 또는 가지치기 설계) `{STATUS}`. Effect(효과): run267CL(267CL 실행)의 Monday(월요일), "
        "2024-12(2024년 12월), session(세션) 약점을 같은 축 repair(수리)로 더 끌지 않고 "
        f"feature blueprint(피처 청사진) `{result['feature_blueprint_count']}`개와 materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개로 바꿨으며, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_line)
    workspace = workspace.replace(f"  status: {source_review.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {PARENT_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {PARENT_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  next_action: {source_review.NEXT_ACTION}", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review_report_path",
        f"  run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(FEATURE_BLUEPRINT_PATH, result["feature_blueprint"], FEATURE_BLUEPRINT_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, result["branch_decisions"], BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"], MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, result["prune_matrix"], PRUNE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], FAILURE_MEMORY_COLUMNS)
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
            "artifact_hashes": "registered_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": {
                "stage_ledger": rel(STAGE_LEDGER_PATH),
                "project_ledger": rel(PROJECT_LEDGER_PATH),
                "run_registry": rel(RUN_REGISTRY_PATH),
                "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            },
            "availability": "tracked(추적됨)",
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
        f"prune_rows={result['prune_count']};"
        f"next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B run267CL review-derived design; true Tier B fallback blocked",
        "scoreboard": "feature_blueprint_branch_decision_materialization_queue_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
        "tier_scope": "Tier A run267CL design; Tier B fallback remains blocked",
        "kpi_scope": "experiment_design_feature_blueprint_queue_failure_memory",
        "scoreboard_lane": "orthogonal_loss_shape_state_followup_design",
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


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_REVIEW_PATH)
    summary_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    features = feature_blueprints()
    decisions = branch_decisions(candidate_rows, summary_rows)
    queue_rows = materialization_queue()
    prune_rows = prune_matrix()
    failure_rows = failure_memory(negative_rows)
    receipt_rows = experiment_design_receipts(queue_rows)
    judgment_rows = result_judgment()
    gates = gate_audit(queue_rows, prune_rows)
    result = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_status": source_result.get("status"),
        "source_trade_records": source_result.get("trade_record_count"),
        "source_negative_slices": len(source_result.get("negative_slices", [])),
        "feature_blueprint_count": len(features),
        "branch_decision_count": len(decisions),
        "materialization_queue_count": len(queue_rows),
        "prune_count": len(prune_rows),
        "failure_memory_count": len(failure_rows),
        "feature_blueprint": features,
        "branch_decisions": decisions,
        "materialization_queue": queue_rows,
        "prune_matrix": prune_rows,
        "failure_memory": failure_rows,
        "experiment_design_receipt": receipt_rows,
        "result_judgment": judgment_rows,
        "gate_audit": gates,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "run267CL_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267CL_candidate_review": rel(SOURCE_CANDIDATE_REVIEW_PATH),
            "run267CL_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "run267CL_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "run267CL_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": {
            "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
            "branch_decisions": rel(BRANCH_DECISION_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "prune_matrix": rel(PRUNE_MATRIX_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    return result


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
