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
    run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267CY"
RUN_ID = "run267CY_stage267_shared_weakness_breakout_second_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267CY_shared_weakness_breakout_second_followup_or_prune_design_completed"
JUDGMENT = "second_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CZ_materialize_shared_weakness_breakout_second_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_second_followup_or_prune_design"

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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CY_shared_weakness_breakout_second_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CY_shared_weakness_breakout_second_followup_or_prune_design.py")

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

CANDIDATE_POOL = {
    "s264_aih": ("s264_allow_inner_high_quarter", "challenger_core(핵심 도전자)"),
    "s264_lc": ("s264_lowrank_control", "defensive_control(방어 대조)"),
    "s262_lih": ("s262_lowrank_inner_half_filter", "validation_heavy(검증 중심)"),
    "s264_aia": ("s264_allow_inner_all_oos_anchor", "oos_anchor(표본외 앵커)"),
    "s258_stc": ("s258_short_tight_control", "stress_challenger(압박 도전자)"),
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


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, current in enumerate(lines):
        if needle in current:
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


def rows_by_alias(rows: Sequence[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("candidate_alias")), []).append(row)
    return grouped


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            as_float(row.get("net_profit")),
            as_float(row.get("profit_factor")),
            -as_float(row.get("report_equity_drawdown_percent")),
            as_int(row.get("trade_count")),
        ),
    )


def weakest_slice(candidate_alias: str, negative_rows: Sequence[Mapping[str, Any]]) -> str:
    rows = [row for row in negative_rows if row.get("candidate_alias") == candidate_alias]
    if not rows:
        return "missing_in_run267CX(267CX에 없음)"
    weakest = min(rows, key=lambda row: as_float(row.get("net_profit")))
    return f"{weakest.get('axis')}:{weakest.get('bucket')}:{weakest.get('net_profit')}"


def feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "cy_fb01_redzone_loss_shape_cross_period",
            "feature_family": "redzone loss-shape cross-period(위험 구역 손실형태 확장 기간)",
            "market_meaning": "s258_stc의 강한 2024 수익이 특정 월이나 Monday(월요일)에만 우연히 맞은 것인지 다른 기간에서 깨뜨려 본다.",
            "candidate_scope": "s258_stc",
            "source_evidence": "run267CX redzone_monday_dd_pressure net=2115.89, PF=1.4540, trades=518, DD=16.42, worst_month=2024-07:-113.17.",
            "changed_variables": "period pack(기간 묶음)과 loss-shape pressure(손실형태 압박)만 바꾸고 risk(위험), cost(비용), feature order(피처 순서)는 고정한다.",
            "similar_replacement_axis": "calendar Monday(달력 월요일) 금지가 아니라 drawdown cluster(손실폭 군집), session loss(세션 손실), volatility shock(변동성 충격)으로 의미를 대체한다.",
            "aggressive_or_defensive": "aggressive_validation(공격적 검증)",
            "do_not_use_as": "selected baseline(선택 기준 후보) 또는 ONNX readiness(ONNX 준비) 근거",
            "success_read": "2023H2, 2025H1, 2025H2 중 2개 이상에서 PF>=1.35, DD<=20%, trades>=250, worst_month_net>-180이면 생존 단서다.",
            "failure_read": "한 기간이라도 net<=0 또는 DD>=26%이면 고수익 후보가 아니라 stress-only(압박 전용)로 낮춘다.",
            "materialization_note": "run267CZ는 s258_stc redzone profile(프로필)을 확장 기간 MT5 입력으로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cy_fb02_explosive_shock_state_survival_pack",
            "feature_family": "explosive shock-state survival(폭발형 충격-상태 생존)",
            "market_meaning": "방어 필터를 더 붙이지 않고 shock(충격), state phase(상태 구간), loss shape(손실 형태)를 조합해 상단 수익을 열어 보되 DD(손실폭)로 바로 가지치기한다.",
            "candidate_scope": "s258_stc;s264_aia;s264_aih",
            "source_evidence": "run267CX explosive combo: s258_stc net=1846.96/DD=13.91, s264_aia net=1452.57/DD=14.63, s264_aih net=1550.62/DD=26.18.",
            "changed_variables": "shock persistence(충격 지속), state interaction(상태 상호작용), redzone release(위험 구역 해제)를 넓히되 calendar ban(달력 금지)은 쓰지 않는다.",
            "similar_replacement_axis": "ADX/DI 같은 trend strength(추세 강도)를 shock persistence(충격 지속)와 range expansion(범위 확장)으로 대체한다.",
            "aggressive_or_defensive": "explosive_aggressive(폭발형 공격)",
            "do_not_use_as": "repair loop(수리 반복) 또는 defensive filter stack(방어 필터 누적)",
            "success_read": "net>2200, trades>=450, PF>=1.35, DD<=22%, chron_mid_net>0이면 다음 Adapter(어댑터) 구조화 후보로 남긴다.",
            "failure_read": "DD>=28%, chron_mid_net<0, worst_month_net<-220 중 하나라도 나오면 폭발형 분기를 줄인다.",
            "materialization_note": "run267CZ는 최소 폭발형 attempt(시도)를 만들고, 실패 시 오래 끌지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cy_fb03_oos_anchor_validation_damage_probe",
            "feature_family": "OOS anchor validation damage probe(표본외 앵커 검증 손상 탐침)",
            "market_meaning": "s264_aia가 OOS anchor(표본외 앵커)로 회복하는지, 아니면 validation damage(검증 손상)를 숨기는지 확인한다.",
            "candidate_scope": "s264_aia",
            "source_evidence": "run267CX s264_aia explosive net=1452.57, PF=1.4374, trades=484, DD=14.63, negative_month_count=3.",
            "changed_variables": "validation-sensitive replacement(검증 민감 대체), OOS anchor pressure(표본외 앵커 압박), weak-month zoom(약한 월 확대).",
            "similar_replacement_axis": "state phase(상태 구간)를 volatility state(변동성 상태)와 late-segment drawdown shape(후반 손실 형태)로 대체한다.",
            "aggressive_or_defensive": "balanced_probe(균형 탐침)",
            "do_not_use_as": "OOS 숫자만으로 후보 선택",
            "success_read": "validation-like weak segment(검증 유사 약한 구간)에서 DD<=18%, PF>=1.32, worst_month_net>-160이면 살린다.",
            "failure_read": "validation-like 구간에서 DD가 커지거나 3개월 이상 음수 월이면 OOS anchor 단독 분기를 낮춘다.",
            "materialization_note": "run267CZ는 s264_aia만 좁게 validation damage probe(검증 손상 탐침)로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cy_fb04_aih_final_supply_or_prune",
            "feature_family": "AIH final supply or prune(AIH 최종 공급 수리 또는 가지치기)",
            "market_meaning": "s264_aih supply repair(공급 수리)가 높은 PF(수익 팩터)만 남기고 거래 수가 얇아지는지 마지막으로 확인한다.",
            "candidate_scope": "s264_aih",
            "source_evidence": "run267CX aih_aggressive_supply_repair net=1047.25, PF=1.7443, trades=283, Monday=-198.19, 2024-12=-155.42.",
            "changed_variables": "entry supply width(진입 공급 폭), shock release width(충격 해제 폭), thin-trade guard(얇은 거래 방지)를 한 번만 조정한다.",
            "similar_replacement_axis": "supply threshold(공급 임계값)을 liquidity pocket(유동성 포켓)과 drawdown cluster(손실폭 군집)로 대체한다.",
            "aggressive_or_defensive": "bounded_repair(제한 수리)",
            "do_not_use_as": "3단계 이상 이어지는 repair loop(수리 반복)",
            "success_read": "trades>=340, net>=1300, PF>=1.50, DD<=18, Monday net>-140이면 한 번 더 본다.",
            "failure_read": "거래 수가 늘어도 net/PF가 무너지거나 Monday가 계속 -180 아래면 가지치기한다.",
            "materialization_note": "run267CZ는 s264_aih supply repair를 최대 1개 attempt(시도)로 제한한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cy_fb05_feature_reliance_ablation_replacement",
            "feature_family": "feature reliance ablation/replacement(피처 의존 제거/대체)",
            "market_meaning": "좋아 보인 후보가 특정 피처 하나에 붙은 우연인지 확인한다.",
            "candidate_scope": "s258_stc;s264_aia",
            "source_evidence": "run267CX에서 s258_stc와 s264_aia는 건설적이지만 redzone/explosive profile(프로필) 의존 가능성이 남았다.",
            "changed_variables": "remove redzone score(위험 구역 점수 제거), replace shock-state score(충격-상태 점수 대체), keep model/risk/cost fixed(모델/위험/비용 고정).",
            "similar_replacement_axis": "ADX/DI/trend strength(추세 강도)를 volatility energy(변동성 에너지), range expansion(범위 확장), loss-shape persistence(손실 형태 지속)로 대체한다.",
            "aggressive_or_defensive": "robustness_probe(견고성 탐침)",
            "do_not_use_as": "숫자 미세 조정",
            "success_read": "피처 제거 또는 유사 대체에서 net이 35% 이상 무너지지 않고 DD가 5%p 이상 악화되지 않으면 의미 구조 단서다.",
            "failure_read": "한 피처 제거로 net이 절반 이하가 되거나 PF<1.10이면 의존 과다로 기록한다.",
            "materialization_note": "run267CZ는 생존 후보만 좁게 ablation/replacement(제거/대체) 입력으로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cy_fb06_control_rejoin_guardrail",
            "feature_family": "control rejoin guardrail(대조 후보 재합류 가드레일)",
            "market_meaning": "최근 run이 s258/s264 공격형 표면에 치우쳤으므로 s264_lc와 s262_lih를 다시 대조 축으로 붙인다.",
            "candidate_scope": "s264_lc;s262_lih",
            "source_evidence": "run267CX에는 s264_lc와 s262_lih가 직접 materialized(물질화)되지 않았다.",
            "changed_variables": "no new alpha feature(새 알파 피처 없음); same MT5 period/cost/risk(같은 MT5 기간/비용/위험)로 대조만 재확인한다.",
            "similar_replacement_axis": "defensive control(방어 대조)과 validation-heavy(검증 중심) 표면을 공격형 분기 옆에 붙인다.",
            "aggressive_or_defensive": "control_guardrail(대조 가드레일)",
            "do_not_use_as": "공격형 탐색을 막는 필터",
            "success_read": "공격형 후보가 무너질 때 대조 후보가 덜 깨지면 다음 설계에서 control lane(대조 레인)을 살린다.",
            "failure_read": "대조 후보도 같은 월/세션에서 무너지면 shared weakness(공유 약점)로 기록한다.",
            "materialization_note": "run267CZ 또는 후속 run에서 최소 대조 시도를 붙인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def branch_decisions(
    candidate_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped = rows_by_alias(candidate_rows)
    result: list[dict[str, Any]] = []
    for alias in ("s258_stc", "s264_aia", "s264_aih"):
        row = best_row(grouped.get(alias, []))
        if alias == "s258_stc":
            decision_label = "high_profit_stress_watch_no_selection(고수익 압박 관찰, 선택 아님)"
            next_use = "P0 redzone cross-period and explosive survival(위험 구역 확장 기간 및 폭발형 생존)"
            why = "두 profile(프로필)이 모두 높은 net(순수익)과 충분한 trade count(거래 수)를 보였지만 Monday/session 약점이 남았다."
            risk = "stress challenger(압박 도전자)일 뿐이며 validation/DD(검증/손실폭) 확정이 아니다."
            reopen = "확장 기간 2개 이상에서 DD<=20%, PF>=1.35이면 Adapter(어댑터) 구조 후보로 다시 본다."
        elif alias == "s264_aia":
            decision_label = "constructive_oos_anchor_followup_no_selection(건설적 표본외 앵커 후속, 선택 아님)"
            next_use = "P0/P1 explosive cross-period plus validation damage probe(폭발형 확장 기간과 검증 손상 탐침)"
            why = "DD(손실폭)는 편하지만 negative month(음수 월)가 3개라 OOS anchor(표본외 앵커) 손상 여부를 더 봐야 한다."
            risk = "OOS 숫자 회복을 validation damage(검증 손상) 위에 덮어 쓰면 안 된다."
            reopen = "검증 유사 약한 구간에서 DD<=18%, worst_month_net>-160이면 계속 살린다."
        else:
            decision_label = "curve_risk_or_thin_supply_prune_gate(곡선 위험 또는 얇은 공급 가지치기 게이트)"
            next_use = "one final bounded supply test or prune(마지막 제한 공급 시험 또는 가지치기)"
            why = "explosive profile(폭발형 프로필)은 DD 26.18%가 불편하고, supply repair(공급 수리)는 PF는 높지만 trades=283으로 얇다."
            risk = "이 분기는 이미 repair(수리) 냄새가 있으므로 길게 끌면 안 된다."
            reopen = "마지막 1회 시도에서 trades>=340, DD<=18, Monday net>-140이면 관찰만 연장한다."
        result.append(
            {
                "decision_id": f"cy_decision_{alias}",
                "candidate_alias": alias,
                "candidate_id": CANDIDATE_POOL[alias][0],
                "candidate_role": CANDIDATE_POOL[alias][1],
                "best_profile": row.get("test_id", "missing"),
                "best_net_profit": row.get("net_profit", ""),
                "best_profit_factor": row.get("profit_factor", ""),
                "best_equity_drawdown_percent": row.get("report_equity_drawdown_percent", ""),
                "best_trade_count": row.get("trade_count", ""),
                "worst_month": row.get("worst_month", ""),
                "worst_month_net": row.get("worst_month_net", ""),
                "weakest_slice": weakest_slice(alias, negative_rows),
                "decision_label": decision_label,
                "next_use": next_use,
                "why": why,
                "risk_boundary": risk,
                "reopen_condition": reopen,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for alias in ("s264_lc", "s262_lih"):
        result.append(
            {
                "decision_id": f"cy_decision_{alias}",
                "candidate_alias": alias,
                "candidate_id": CANDIDATE_POOL[alias][0],
                "candidate_role": CANDIDATE_POOL[alias][1],
                "best_profile": "not_materialized_in_run267CX(267CX에서 미물질화)",
                "best_net_profit": "",
                "best_profit_factor": "",
                "best_equity_drawdown_percent": "",
                "best_trade_count": "",
                "worst_month": "",
                "worst_month_net": "",
                "weakest_slice": "missing_in_run267CX(267CX에 없음)",
                "decision_label": "control_rejoin_required_no_selection(대조 재합류 필요, 선택 아님)",
                "next_use": "P2 control guardrail retest(대조 가드레일 재시험)",
                "why": "최근 분기가 공격형 후보 3개에 치우쳤으므로 defensive/validation control(방어/검증 대조)을 다시 붙여야 한다.",
                "risk_boundary": "대조 후보가 없으면 aggressive profile(공격형 프로필)의 성과가 과장될 수 있다.",
                "reopen_condition": "공격형 후보의 확장 기간 압박 뒤 같은 설정으로 대조 후보를 함께 비교한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return result


def materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "cy_q01_s258_redzone_cross_period_survival",
            "priority": "P0_aggressive_validation(우선순위0 공격 검증)",
            "workstream": "redzone_loss_shape_cross_period(위험 구역 손실형태 확장 기간)",
            "candidate_aliases": "s258_stc",
            "feature_blueprint_scope": "cy_fb01_redzone_loss_shape_cross_period",
            "hypothesis": "s258_stc redzone profile(위험 구역 프로필)이 2024에만 맞은 우연이 아니라면 인접 기간에서도 덜 깨진다.",
            "decision_use": "s258_stc를 stress-only(압박 전용)로 낮출지, 다음 Adapter(어댑터) 구조 후보로 유지할지 판단한다.",
            "comparison_baseline": "run267CX s258_stc redzone net=2115.89, PF=1.4540, trades=518, DD=16.42.",
            "control_variables": "symbol=US100, timeframe=M5, cost/spread/risk, feature order(피처 순서), RuntimeProbeEA(런타임 탐침 EA).",
            "changed_variables": "period pack(기간 묶음) 2023H2/2025H1/2025H2, loss-shape pressure(손실형태 압박).",
            "sample_scope": "historical_2024 plus adjacent periods(2024 과거 압박 및 인접 기간)",
            "success_criteria": "2개 이상 기간에서 PF>=1.35, DD<=20%, trades>=250, worst_month_net>-180.",
            "failure_criteria": "net<=0, DD>=26%, or Monday/session weakness(월요일/세션 약점)이 더 깊어짐.",
            "invalid_conditions": "feature order mismatch(피처 순서 불일치), missing MT5 report(MT5 보고서 누락), duplicate-boundary mistaken as true fallback(중복 경계를 실제 대체로 오해).",
            "stop_conditions": "한 기간에서 deep DD(깊은 손실폭)가 확인되면 바로 stress-only로 낮춘다.",
            "evidence_plan": "MT5 KPI, trade list(거래 목록), curve diagnostics(곡선 진단), month/weekday/session slices(월/요일/세션 구간).",
            "materialization_instruction": "Create s258_stc redzone cross-period TA/RT attempts without calendar bans.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cy_q02_explosive_combo_cross_period_prune_gate",
            "priority": "P0_explosive_aggressive(우선순위0 폭발형 공격)",
            "workstream": "explosive_shock_state_combo(폭발형 충격-상태 조합)",
            "candidate_aliases": "s258_stc;s264_aia;s264_aih",
            "feature_blueprint_scope": "cy_fb02_explosive_shock_state_survival_pack",
            "hypothesis": "방어 필터를 더 붙이지 않아도 shock-state(충격-상태) 조합이 넓은 기간에서 수익 상단을 열 수 있다.",
            "decision_use": "폭발형 분기를 살릴지, s264_aih를 DD(손실폭) 때문에 분리할지 판단한다.",
            "comparison_baseline": "run267CX explosive combo rows for s258_stc, s264_aia, s264_aih.",
            "control_variables": "same MT5 settings(같은 MT5 설정), same risk/cost(같은 위험/비용), no calendar hard ban(달력 하드 금지 없음).",
            "changed_variables": "shock persistence, state interaction, redzone release width(충격 지속/상태 상호작용/위험구역 해제 폭).",
            "sample_scope": "2024 zoom plus one adjacent period first(2024 확대와 인접 기간 1개 선실행)",
            "success_criteria": "net>2200, PF>=1.35, trades>=450, DD<=22%, chron_mid_net>0.",
            "failure_criteria": "DD>=28%, chron_mid_net<0, worst_month_net<-220.",
            "invalid_conditions": "using extra filters not listed here(명시되지 않은 추가 필터 사용), changed cost or deposit(비용/예치금 변경).",
            "stop_conditions": "2개 후보 이상에서 DD gate(손실폭 게이트)가 실패하면 폭발형 조합을 축소한다.",
            "evidence_plan": "balance/equity curve(잔액/평가금 곡선), chron segment(시간 순서 구간), weak-month zoom(약한 월 확대), trade quality(거래 품질).",
            "materialization_instruction": "Create one explosive attempt per candidate first; no fine-tune loop.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cy_q03_s264_aia_validation_damage_probe",
            "priority": "P1_balanced_probe(우선순위1 균형 탐침)",
            "workstream": "oos_anchor_validation_damage(표본외 앵커 검증 손상)",
            "candidate_aliases": "s264_aia",
            "feature_blueprint_scope": "cy_fb03_oos_anchor_validation_damage_probe",
            "hypothesis": "s264_aia의 OOS anchor(표본외 앵커) 회복은 validation damage(검증 손상)를 숨기지 않을 때만 가치가 있다.",
            "decision_use": "s264_aia를 OOS anchor 후보로 유지할지 판단한다.",
            "comparison_baseline": "run267CX s264_aia explosive net=1452.57, PF=1.4374, trades=484, DD=14.63.",
            "control_variables": "feature order, cost, risk, MT5 tester identity(피처 순서/비용/위험/테스터 정체성).",
            "changed_variables": "validation-sensitive state replacement(검증 민감 상태 대체), weak-month zoom(약한 월 확대).",
            "sample_scope": "validation-like weak segments and historical 2024(검증 유사 약한 구간 및 2024)",
            "success_criteria": "DD<=18%, PF>=1.32, worst_month_net>-160.",
            "failure_criteria": "3개 이상 negative months(음수 월) or DD>=22%.",
            "invalid_conditions": "OOS-only score read(표본외 숫자만 판독), missing validation-like slices(검증 유사 구간 누락).",
            "stop_conditions": "validation-like weakness deepens twice, lower s264_aia to observation only.",
            "evidence_plan": "month/session/chron KPIs and curve diagnostics(월/세션/시간순 KPI와 곡선 진단).",
            "materialization_instruction": "Materialize after P0 queue if budget allows; keep it narrow.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cy_q04_aih_final_supply_or_prune",
            "priority": "P1_bounded_repair(우선순위1 제한 수리)",
            "workstream": "aih_final_supply_or_prune(AIH 최종 공급 또는 가지치기)",
            "candidate_aliases": "s264_aih",
            "feature_blueprint_scope": "cy_fb04_aih_final_supply_or_prune",
            "hypothesis": "s264_aih supply repair(공급 수리)는 마지막 한 번의 공급 확대에서도 거래 수와 곡선이 같이 살아야 한다.",
            "decision_use": "s264_aih supply branch(공급 분기)를 살릴지 버릴지 결정한다.",
            "comparison_baseline": "run267CX s264_aih supply net=1047.25, PF=1.7443, trades=283, Monday=-198.19.",
            "control_variables": "source model surface(원천 모델 표면), cost/risk, no calendar ban.",
            "changed_variables": "entry supply width and shock release width(진입 공급 폭과 충격 해제 폭).",
            "sample_scope": "historical 2024 only first(2024 우선), adjacent period only if passes.",
            "success_criteria": "trades>=340, net>=1300, PF>=1.50, DD<=18, Monday net>-140.",
            "failure_criteria": "trades remain <320 or Monday net<-180 or DD>=22.",
            "invalid_conditions": "more than one additional repair attempt(추가 수리 1회 초과), hidden threshold tuning(숨은 임계값 튜닝).",
            "stop_conditions": "one failed attempt closes this repair branch.",
            "evidence_plan": "trade count, PF, Monday/session slices, curve DD(거래 수/수익 팩터/월요일/세션/곡선 손실폭).",
            "materialization_instruction": "Create at most one final supply repair attempt.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cy_q05_feature_reliance_ablation_replacement",
            "priority": "P1_robustness(우선순위1 견고성)",
            "workstream": "feature_ablation_similar_replacement(피처 제거 유사 대체)",
            "candidate_aliases": "s258_stc;s264_aia",
            "feature_blueprint_scope": "cy_fb05_feature_reliance_ablation_replacement",
            "hypothesis": "생존 후보는 redzone/explosive feature(위험 구역/폭발형 피처)를 제거하거나 유사 대체해도 완전히 무너지지 않아야 한다.",
            "decision_use": "Adapter(어댑터) 구조화 전에 피처 의존도를 낮출 수 있는지 본다.",
            "comparison_baseline": "run267CX constructive rows and run267CY P0 survivors.",
            "control_variables": "same period/cost/risk/model family(같은 기간/비용/위험/모델 계열).",
            "changed_variables": "remove one engineered feature(피처 하나 제거), replace with similar market meaning(유사 시장 의미 대체).",
            "sample_scope": "only survivors from cy_q01/cy_q02(cy_q01/cy_q02 생존 후보만).",
            "success_criteria": "net drawdown under 35%, PF>=1.20, DD worsens <=5 percentage points.",
            "failure_criteria": "net falls by more than half or PF<1.10.",
            "invalid_conditions": "running ablation before survivor set exists(생존 후보 확정 전 제거 실행).",
            "stop_conditions": "if no P0 survivor, keep this as held queue(보류 대기열).",
            "evidence_plan": "delta KPI(차이 KPI), feature order receipt(피처 순서 영수증), curve/time-slice review(곡선/시간 구간 검토).",
            "materialization_instruction": "Hold until P0 survivors are known, then materialize narrow ablation/replacement.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cy_q06_control_rejoin_guardrail",
            "priority": "P2_control_guardrail(우선순위2 대조 가드레일)",
            "workstream": "control_rejoin(대조 재합류)",
            "candidate_aliases": "s264_lc;s262_lih",
            "feature_blueprint_scope": "cy_fb06_control_rejoin_guardrail",
            "hypothesis": "공격형 후보의 의미는 defensive/validation controls(방어/검증 대조)와 같이 볼 때만 제대로 읽힌다.",
            "decision_use": "공격형 분기 성과가 후보군 전체로 확장 가능한지 확인한다.",
            "comparison_baseline": "Stage267 initial candidate pool and prior control runs(초기 후보군과 이전 대조 실행).",
            "control_variables": "no new engineered feature(새 피처 없음), same MT5 period/cost/risk.",
            "changed_variables": "only rejoin control candidates(대조 후보 재합류만).",
            "sample_scope": "historical 2024 plus same period as P0 survivor(2024와 P0 생존 후보 동일 기간).",
            "success_criteria": "control candidates are less broken in weak slices or provide clear contrast.",
            "failure_criteria": "controls break in same month/session with no explanatory value.",
            "invalid_conditions": "omitting control rows while claiming pool-wide read(후보군 전체 판독 주장 중 대조 누락).",
            "stop_conditions": "if materialization budget is tight, document as held but do not forget it.",
            "evidence_plan": "control KPI, weak-slice comparison, failure memory update(대조 KPI/약점 비교/실패 기억 갱신).",
            "materialization_instruction": "Materialize after P0 or as a compact parallel control tranche.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "cy_prune_headline_net_selection",
            "prune_label": "headline_net_selection_forbidden(대표 순수익 선택 금지)",
            "affected_scope": "all candidates(전체 후보)",
            "why_pruned": "run267CX에서 s258_stc 숫자가 강하지만 약한 세션/요일과 확장 기간 검증이 아직 없다.",
            "reopen_condition": "여러 기간, feature ablation(피처 제거), similar replacement(유사 대체), curve review(곡선 검토)를 통과해야 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cy_prune_s264_aih_explosive_selection_path",
            "prune_label": "s264_aih_explosive_selection_path_pruned(s264_aih 폭발형 선택 경로 가지치기)",
            "affected_scope": "s264_aih explosive_shock_state_combo",
            "why_pruned": "net은 양수지만 DD=26.18%와 chron_mid_net=-6.97이 불편하다.",
            "reopen_condition": "risk-limited diagnostic(제한 위험 진단)에서 DD<=20%, chron_mid_net>0이면 관찰로만 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cy_prune_calendar_only_monday_ban",
            "prune_label": "calendar_only_monday_ban_pruned(달력 월요일 금지만 가지치기)",
            "affected_scope": "Monday/session weakness repair(월요일/세션 약점 수리)",
            "why_pruned": "목표는 필터 덕지덕지가 아니므로 Monday(월요일) 자체를 막는 방식은 연구 가치를 낮춘다.",
            "reopen_condition": "market-meaning replacement(시장 의미 대체)로 손실형태/변동성 군집이 확인될 때만 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cy_prune_unbounded_aih_supply_repair",
            "prune_label": "unbounded_aih_supply_repair_pruned(무제한 AIH 공급 수리 가지치기)",
            "affected_scope": "s264_aih supply repair",
            "why_pruned": "run267CX에서 PF는 높지만 거래 수 283과 Monday=-198.19가 남아 repair loop(수리 반복) 위험이 있다.",
            "reopen_condition": "한 번의 최종 bounded repair(제한 수리)만 허용하고 실패 시 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cy_prune_duplicate_boundary_as_fallback",
            "prune_label": "duplicate_boundary_not_true_fallback(중복 경계는 실제 대체 아님)",
            "affected_scope": "Tier A+B duplicate rows(티어 A+B 중복 행)",
            "why_pruned": "run267CX는 duplicate-boundary(중복 경계)만 있고 true Tier B fallback(진짜 티어 B 대체)을 증명하지 않는다.",
            "reopen_condition": "actual routed total(실제 라우팅 전체)과 Tier B fallback component(티어 B 대체 구성)를 따로 기록할 때만 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "cy_memory_monday_session_holes",
            "pattern": "Monday/session weak slices(月요일/세션 약점 구간)",
            "affected_scope": "s258_stc;s264_aih;s264_aia",
            "evidence": "run267CX negative_slice_summary has Monday/session losses including s264_aih Monday=-198.19 and s258 session_07_12=-155.85.",
            "why_fragile": "전체 KPI가 좋아도 특정 요일/세션의 깊은 구멍이 curve(곡선)를 망칠 수 있다.",
            "do_not_repeat": "달력 금지만 붙이는 방식.",
            "salvage_angle": "loss-shape/volatility/session pressure(손실형태/변동성/세션 압박)로 시장 의미를 대체한다.",
            "reopen_condition": "유사 대체에서 약점이 줄고 전체 PF/DD가 유지될 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cy_memory_aih_dd_or_thin_supply",
            "pattern": "s264_aih DD or thin supply(s264_aih 손실폭 또는 얇은 공급)",
            "affected_scope": "s264_aih",
            "evidence": "explosive DD=26.18, supply trades=283, supply Monday=-198.19.",
            "why_fragile": "높은 PF가 거래 공급 부족과 깊은 DD를 숨길 수 있다.",
            "do_not_repeat": "s264_aih repair branch(수리 분기)를 3단계 이상 끌기.",
            "salvage_angle": "한 번의 bounded supply repair(제한 공급 수리) 후 실패 시 prune(가지치기).",
            "reopen_condition": "trades>=340 and DD<=18 and Monday net>-140.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cy_memory_controls_missing_from_latest",
            "pattern": "controls missing from latest branch(최신 분기에서 대조 후보 누락)",
            "affected_scope": "s264_lc;s262_lih",
            "evidence": "run267CX candidate rows include s258_stc, s264_aia, s264_aih only.",
            "why_fragile": "후보군 전체 판독처럼 보이지만 defensive/validation controls(방어/검증 대조)가 빠져 있다.",
            "do_not_repeat": "공격형 후보만 계속 비교하고 후보군 전체 결론처럼 말하기.",
            "salvage_angle": "compact control rejoin(작은 대조 재합류)을 다음 물질화 또는 후속 설계에 넣는다.",
            "reopen_condition": "P0 aggressive candidates finish cross-period pressure.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cy_memory_duplicate_boundary",
            "pattern": "duplicate boundary is not routed fallback(중복 경계는 라우팅 대체가 아님)",
            "affected_scope": "all run267CX TA/RT paired rows",
            "evidence": "Tier A and duplicate-boundary Tier A+B were materialized; true fallback remains outside the run.",
            "why_fragile": "Tier A+B 수익이 실제 Tier B fallback(티어 B 대체)에서 나온 것처럼 오해될 수 있다.",
            "do_not_repeat": "duplicate-boundary를 actual routed total(실제 라우팅 전체)로 부르기.",
            "salvage_angle": "future runtime reproduction(런타임 재현)에서 component rows(구성 행)를 따로 기록한다.",
            "reopen_condition": "runtime handoff(런타임 인계)와 actual routed report(실제 라우팅 보고)가 생길 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def performance_attribution(source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    observed = "; ".join(
        f"{row.get('candidate_alias')}:{row.get('test_id')}:{row.get('observed_change')}"
        for row in source_rows[:5]
    )
    return [
        {
            "attribution_id": "cy_attr_redzone_explosive_survival",
            "observed_change": observed,
            "comparison_baseline": "run267CX candidate_profile_review and run267B historical 2024 baseline(267CX 후보 프로필 검토와 267B 2024 기준)",
            "likely_drivers": "redzone loss-shape(위험 구역 손실형태), explosive shock-state(폭발형 충격-상태), bounded supply repair(제한 공급 수리)",
            "segment_checks": "month, weekday, session, hour, direction, chron segment were checked in run267CX(월/요일/세션/시간/방향/시간순 구간 확인).",
            "trade_shape": "run267CX trade_records=4470, candidate_profile_rows=5, negative_slices=27.",
            "alternative_explanations": "2024-specific fit(2024 특화 적합), duplicate-boundary artifact(중복 경계 효과), thin-trade PF inflation(얇은 거래 PF 부풀림).",
            "attribution_confidence": "medium_for_design_only(설계용 중간)",
            "next_probe": NEXT_ACTION,
        }
    ]


def experiment_design_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"cy_design_{row['queue_id']}",
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
            "receipt_id": "cy_data_integrity_design_only",
            "data_source": rel(SOURCE_REVIEW_RESULT_PATH),
            "time_axis": "inherits run267CX MT5 report close times(267CX MT5 보고서 청산 시간 상속)",
            "sample_scope": "design only; future run267CZ must recheck concrete feature frames(설계 전용, 향후 267CZ에서 실제 피처 프레임 재검사)",
            "missing_or_duplicate_check": f"source parser_errors={len(source_result.get('parser_errors', []))}",
            "feature_label_boundary": "no new label read in this design(이 설계에서 새 라벨 읽기 없음)",
            "split_boundary": "historical 2024 source plus proposed adjacent periods(2024 원천 및 제안 인접 기간)",
            "leakage_risk": "low_for_design_only; must be rechecked during materialization(설계용 낮음, 물질화 때 재검사)",
            "data_hash_or_identity": sha256_file_lf_normalized(SOURCE_REVIEW_RESULT_PATH),
            "integrity_judgment": "usable_for_design_with_boundary(경계 포함 설계 사용 가능)",
        }
    ]


def model_validation_receipts() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "cy_model_validation_design_only",
            "model_family": "stage-local score-table/feature materialization proposal(단계 로컬 점수표/피처 물질화 제안)",
            "target_and_label": "no retraining in run267CY(267CY 재학습 없음)",
            "split_method": "proposed cross-period stress plus historical 2024(제안 확장 기간 압박 및 2024)",
            "selection_metric": "not selection; survival under PF/DD/trade-count/curve gates(선택 아님, PF/DD/거래 수/곡선 생존)",
            "secondary_metrics": "weak month, weekday, session, chron segment, feature ablation response(약한 월/요일/세션/시간순/피처 제거 반응)",
            "threshold_policy": "no hidden threshold tuning(숨은 임계값 튜닝 없음)",
            "overfit_risk": "medium_high_until_cross_period_and_ablation(확장 기간/제거 전까지 중상)",
            "calibration_risk": "not evaluated in design(설계에서 미평가)",
            "comparison_baseline": "run267CX review rows and prior Stage267 controls(267CX 검토 행 및 이전 대조)",
            "validation_judgment": "design_ready_not_model_validated(설계 준비, 모델 검증 완료 아님)",
        }
    ]


def result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CY second follow-up/prune design(267CY 2차 후속/가지치기 설계)",
            "evidence_available": "run267CX review_result, candidate_profile_review, negative_slice_summary, performance_attribution(267CX 검토 결과/후보 프로필/음수 구간/성과 귀속)",
            "evidence_missing": "new MT5 execution(새 MT5 실행), cross-period results(확장 기간 결과), ablation/replacement results(제거/대체 결과), Adapter package(어댑터 패키지)",
            "judgment_label": JUDGMENT,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_condition": NEXT_ACTION,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_audit(
    decisions: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    prune_rows: Sequence[Mapping[str, Any]],
    memory_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    aliases = {row["candidate_alias"] for row in decisions}
    checks = (
        ("source_review_available", path_exists(SOURCE_REVIEW_RESULT_PATH), rel(SOURCE_REVIEW_RESULT_PATH), "uses real run267CX evidence(실제 267CX 근거 사용)"),
        ("candidate_pool_covered", set(CANDIDATE_POOL) <= aliases, ";".join(sorted(aliases)), "all baseline candidates have a branch decision(모든 기준 후보 분기 판단 포함)"),
        ("aggressive_queue_present", any("explosive" in row["queue_id"] for row in queue_rows), "explosive queue present", "prevents overly defensive-only progress(방어 전용 진행 방지)"),
        ("ablation_replacement_present", any("ablation" in row["queue_id"] for row in queue_rows), "ablation queue present", "keeps feature reliance check alive(피처 의존 점검 유지)"),
        ("control_rejoin_present", any("control" in row["queue_id"] for row in queue_rows), "control queue present", "keeps s264_lc/s262_lih in pool(대조 후보 유지)"),
        ("prune_matrix_blocks_headline_selection", any("headline" in row["prune_id"] for row in prune_rows), "headline prune present", "prevents number-only selection(숫자만 선택 방지)"),
        ("failure_memory_records_weakness", len(memory_rows) >= 4, f"failure_memory={len(memory_rows)}", "records recurring weak points(반복 약점 기록)"),
        ("no_selection_claim", True, "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed", "keeps claim boundary(주장 경계 유지)"),
    )
    return [
        {
            "gate_id": name,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "effect": effect,
        }
        for name, passed, evidence, effect in checks
    ]


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "sources": result["sources"],
        "outputs": result["outputs"],
        "counts": result["counts"],
    }


def lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
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
        "availability": "tracked_after_commit(커밋 후 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267CY Second Follow-up/Prune Design(267단계 267CY 2차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- branch_decisions(분기 판단): `{len(result['branch_decisions'])}`",
        f"- materialization_queue(물질화 대기열): `{len(result['materialization_queue'])}`",
        f"- prune_rows(가지치기 행): `{len(result['prune_matrix'])}`",
        f"- failure_memory(실패 기억): `{len(result['failure_memory'])}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "run267CX(267CX 실행)는 s258_stc가 강한 숫자를 냈지만 약한 세션/요일/확장 기간 근거가 아직 부족하다고 봤다.",
        "Effect(효과): run267CY(267CY 실행)는 s258_stc를 바로 고르지 않고 cross-period pressure(확장 기간 압박)와 explosive combo(폭발형 조합)로 더 깨뜨려 보도록 대기열을 만들었다.",
        "",
        "s264_aih는 수익 단서가 있지만 DD(손실폭)와 thin supply(얇은 공급)가 불편하다.",
        "Effect(효과): 한 번의 bounded repair(제한 수리)만 허용하고 실패하면 가지치기하도록 기록했다.",
        "",
        "s264_lc와 s262_lih는 이번 run267CX(267CX 실행)에 없었다.",
        "Effect(효과): 후보군 전체 판독이 공격형 후보 3개로만 좁아지지 않도록 control rejoin(대조 재합류)을 대기열에 넣었다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | decision(판단) | next_use(다음 사용) | weakest_slice(약점 구간) |",
        "|---|---|---|---|",
    ]
    for row in result["branch_decisions"]:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['decision_label']}` | `{row['next_use']}` | `{row['weakest_slice']}` |"
        )
    lines.extend(
        [
            "",
            "## Materialization Queue(물질화 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) |",
            "|---|---|---|---|",
        ]
    )
    for row in result["materialization_queue"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | `{row['workstream']}` |"
        )
    lines.extend(
        [
            "",
            "## Prune Boundary(가지치기 경계)",
            "",
            "| prune(가지치기) | affected(영향 범위) | why(이유) |",
            "|---|---|---|",
        ]
    )
    for row in result["prune_matrix"]:
        lines.append(f"| `{row['prune_id']}` | `{row['affected_scope']}` | {row['why_pruned']} |")
    lines.extend(
        [
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decisions(분기 판단): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Boundary(경계)",
            "",
            "run267CY(267CY 실행)는 design(설계)이다. MT5(MetaTrader 5, 메타트레이더5) 실행 결과, Adapter(어댑터) 완성, ONNX(오닉스) 검토 준비를 주장하지 않는다.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267CY_producer", "producer_script", PRODUCER_PATH, "Builds run267CY second follow-up/prune design."),
        ("stage267_run267CY_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Feature blueprints."),
        ("stage267_run267CY_branch_decisions", "branch_decisions", BRANCH_DECISION_PATH, "Branch decisions."),
        ("stage267_run267CY_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Materialization queue."),
        ("stage267_run267CY_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune matrix."),
        ("stage267_run267CY_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267CY_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Performance attribution."),
        ("stage267_run267CY_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267CY_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267CY_model_validation", "model_validation_receipt", MODEL_VALIDATION_RECEIPT_PATH, "Model validation receipt."),
        ("stage267_run267CY_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267CY_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267CY_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267CY_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267CY_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267CY_report", "review_report", REPORT_PATH, "User-facing report."),
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
    write_json(RUN_MANIFEST_PATH, run_manifest(result))
    write_json(LINEAGE_PATH, lineage(result))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"branch_decisions={len(result['branch_decisions'])};"
        f"materialization_queue={len(result['materialization_queue'])};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"failure_memory={len(result['failure_memory'])};next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267CY_shared_weakness_breakout_second_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_second_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary run267CX review-derived design; true fallback not claimed",
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
        "lane": "baseline_candidate_racing_shared_weakness_breakout_second_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_second_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_second_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_second_followup_or_prune_design",
        "tier_scope": "Tier A run267CX design; Tier B fallback remains outside claim",
        "kpi_scope": "experiment_design_feature_blueprint_queue_failure_memory",
        "scoreboard_lane": "shared_weakness_breakout_second_followup_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"materialization_queue={len(result['materialization_queue'])};prune_rows={len(result['prune_matrix'])}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "not_applicable",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267CY_shared_weakness_breakout_second_followup_or_prune_design"
        f"(267CY 공유 약점 2차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267CY_summary(267CY 요약): run267CX(267CX 실행)의 curve/time-slice/trade-quality"
        f"(곡선/시간구간/거래품질) 근거를 materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, "
        f"prune rows(가지치기 행) `{len(result['prune_matrix'])}`개, failure memory(실패 기억) `{len(result['failure_memory'])}`개로 바꿨다. "
        "Effect(효과): s258_stc는 확장 기간과 폭발형 압박으로 더 깨뜨려 보고, s264_aih는 마지막 제한 수리 또는 가지치기로 묶고, s264_lc/s262_lih 대조 후보를 다시 붙인다."
    )
    block = "\n".join(
        [
            "Run267CY(267CY 실행)는 run267CX(267CX 실행)의 잔액/시간구간/거래품질 근거를 2차 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개와 prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개를 만들었고, 폭발형 실험과 control rejoin(대조 재합류)을 같이 열었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_design`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review", summary_line)
            text = append_block_once(text, "Run267CY(267CY 실행)는 run267CX", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review", report_line)
            text = append_block_once(text, "Run267CY(267CY 실행)는 run267CX", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review", report_line)
            text = append_block_once(text, "Run267CY(267CY 실행)는 run267CX", block)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CY(267CY 실행) shared weakness breakout second follow-up/prune design"
        f"(공유 약점 돌파 2차 후속/가지치기 설계) `{STATUS}`. Effect(효과): run267CX(267CX 실행)의 "
        f"balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, "
        f"prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개, failure memory(실패 기억) `{len(result['failure_memory'])}`개로 바꿨고, "
        "폭발형 실험과 대조 후보 재합류를 같이 열었다. selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_line)
    workspace = workspace.replace(f"  next_action: {source_review.NEXT_ACTION}", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CX_shared_weakness_breakout_followup_or_prune_balance_timeslice_trade_quality_review_report_path",
        f"  run267CY_shared_weakness_breakout_second_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_PROFILE_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    source_attribution = read_csv(SOURCE_ATTRIBUTION_PATH)
    features = feature_blueprints()
    decisions = branch_decisions(candidate_rows, negative_rows)
    queue_rows = materialization_queue()
    prune_rows = prune_matrix()
    memory_rows = failure_memory(negative_rows)
    attribution_rows = performance_attribution(source_attribution)
    experiment_rows = experiment_design_receipts(queue_rows)
    data_rows = data_integrity_receipts(source_result)
    model_rows = model_validation_receipts()
    judgment_rows = result_judgment()
    gates = gate_audit(decisions, queue_rows, prune_rows, memory_rows)
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
    result = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_status": source_result.get("status"),
        "counts": {
            "source_candidate_profile_rows": len(candidate_rows),
            "source_negative_slices": len(negative_rows),
            "feature_blueprints": len(features),
            "branch_decisions": len(decisions),
            "materialization_queue": len(queue_rows),
            "prune_rows": len(prune_rows),
            "failure_memory": len(memory_rows),
            "gate_rows": len(gates),
        },
        "feature_blueprint": features,
        "branch_decisions": decisions,
        "materialization_queue": queue_rows,
        "prune_matrix": prune_rows,
        "failure_memory": memory_rows,
        "performance_attribution": attribution_rows,
        "experiment_design_receipt": experiment_rows,
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
            "run267CX_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267CX_candidate_profile": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "run267CX_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "run267CX_profile_axis": rel(SOURCE_PROFILE_AXIS_PATH),
            "run267CX_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "run267CX_attribution": rel(SOURCE_ATTRIBUTION_PATH),
            "run267CX_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": outputs,
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
                "branch_decisions": len(result["branch_decisions"]),
                "materialization_queue": len(result["materialization_queue"]),
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
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
