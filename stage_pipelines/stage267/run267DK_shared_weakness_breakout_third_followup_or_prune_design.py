from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
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
    run267DJ_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267DK"
RUN_ID = "run267DK_stage267_shared_weakness_breakout_third_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267DK_shared_weakness_breakout_third_followup_or_prune_design_completed"
JUDGMENT = "third_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267DL_materialize_shared_weakness_breakout_third_followup_or_prune_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_third_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_PROFILE_AXIS_PATH = source_review.PROFILE_AXIS_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_ATTRIBUTION_PATH = source_review.ATTRIBUTION_SUMMARY_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

FEATURE_BLUEPRINT_PATH = RUN_ROOT / "feature_blueprint.csv"
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DK_shared_weakness_breakout_third_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DK_shared_weakness_breakout_third_followup_or_prune_design.py")

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
    "s264_aia": ("s264_allow_inner_all_oos_anchor", "oos_anchor(표본외 앵커)"),
    "s262_lih": ("s262_lowrank_inner_half_filter", "validation_heavy(검증 중심)"),
    "s258_stc": ("s258_short_tight_control", "stress_challenger(압박 도전자)"),
    "s264_lc": ("s264_lowrank_control", "defensive_control(방어 대조)"),
    "s264_aih": ("s264_allow_inner_high_quarter", "challenger_core(핵심 도전자)"),
}

FEATURE_BLUEPRINT_COLUMNS = (
    "feature_id",
    "feature_family",
    "candidate_scope",
    "market_meaning",
    "source_evidence",
    "changed_variables",
    "similar_replacement_axis",
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


def grouped_by_alias(rows: Sequence[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("candidate_alias")), []).append(row)
    return grouped


def best_profile_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            as_float(row.get("net_profit")),
            as_float(row.get("profit_factor")),
            as_int(row.get("trade_count")),
            -as_float(row.get("report_equity_drawdown_percent")),
        ),
    )


def weakest_slice(alias: str, negative_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    rows = [row for row in negative_rows if row.get("candidate_alias") == alias]
    if not rows:
        return {}
    return min(rows, key=lambda row: as_float(row.get("net_profit")))


def slice_text(row: Mapping[str, Any]) -> str:
    if not row:
        return "missing(누락)"
    return f"{row.get('axis')}:{row.get('bucket')}:{round(as_float(row.get('net_profit')), 2)}"


def s258_summary(curve_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = [row for row in curve_rows if row.get("candidate_alias") == "s258_stc"]
    if not rows:
        return {}
    return {
        "candidate_alias": "s258_stc",
        "candidate_id": "s258_short_tight_control",
        "candidate_role": "stress_challenger",
        "best_profile": "s258_stc_thin_supply_impulse_stress",
        "best_net_profit": sum(as_float(row.get("net_profit")) for row in rows),
        "best_profit_factor": mean(as_float(row.get("profit_factor")) for row in rows),
        "best_equity_drawdown_percent": max(as_float(row.get("report_equity_drawdown_percent")) for row in rows),
        "best_trade_count": sum(as_int(row.get("trade_count")) for row in rows),
        "worst_month": min(rows, key=lambda row: as_float(row.get("worst_month_net"))).get("worst_month"),
        "worst_month_net": min(as_float(row.get("worst_month_net")) for row in rows),
        "weakest_slice": "thin_supply_periods(얇은 공급 기간):trades_167_178_226",
    }


def evidence_summary(decisions: Sequence[Mapping[str, Any]], alias: str) -> Mapping[str, Any]:
    for row in decisions:
        if row.get("candidate_alias") == alias:
            return row
    return {}


def branch_decisions(
    candidate_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped = grouped_by_alias(candidate_rows)
    output: list[dict[str, Any]] = []
    for alias in ("s264_aia", "s262_lih", "s258_stc", "s264_lc", "s264_aih"):
        candidate_id, candidate_role = CANDIDATE_POOL[alias]
        if alias == "s258_stc":
            row = s258_summary(curve_rows)
            weak = {}
        else:
            row = dict(best_profile_row(grouped.get(alias, [])))
            weak = weakest_slice(alias, negative_rows)
        if alias == "s264_aia":
            label = "survivor_adapter_watch_no_selection(생존 어댑터 관찰, 선택 아님)"
            next_use = "P0 dual ablation/replacement survivor gate(P0 이중 제거/대체 생존 관문)"
            why = "ablation(제거)과 similar replacement(유사 대체)가 모두 500개 안팎 거래, PF(수익 팩터) 1.37 이상, DD(손실폭) 16% 미만으로 살아남았다."
            risk = "session_07_12(보고 시간 07-12 세션)과 2024-12(2024년 12월) 구멍이 남아 선택 후보는 아니다."
            reopen = "약한 세션과 2024-12가 동시에 완화되고 feature reliance(피처 의존)가 낮게 유지되면 Adapter watch(어댑터 관찰)를 강화한다."
        elif alias == "s262_lih":
            label = "validation_guardrail_no_selection(검증 가드레일, 선택 아님)"
            next_use = "P0 defensive guardrail crosscheck(P0 방어 가드레일 교차 확인)"
            why = "DD(손실폭) 13.95%와 462 trades(거래 수)는 대조 후보로 쓸 수 있지만 Monday(월요일), 2024-12, chron_mid(중간 순서 구간)이 약하다."
            risk = "validation-heavy(검증 중심) 안정성을 최종 후보로 오해하면 안 된다."
            reopen = "s264_aia/s258_stc 후속 압박 옆에서 덜 깨지는 기준선으로 계속 비교한다."
        elif alias == "s258_stc":
            label = "aggressive_thin_supply_stress_no_selection(공격적 얇은 공급 압박, 선택 아님)"
            next_use = "P0 explosive supply expansion stress(P0 폭발형 공급 확장 압박)"
            why = "세 인접 기간 모두 net(순수익)과 PF(수익 팩터)는 좋지만 각 기간 trade count(거래 수)가 167~226으로 얇다."
            risk = "거래 공급이 얇은 상태에서 좋아 보이는 PF(수익 팩터)는 운 좋게 보일 수 있다."
            reopen = "공급 확장에서 trades(거래 수) 300 이상 구간이 두 개 이상 나오고 DD(손실폭)가 20% 아래면 stress challenger(압박 도전자)를 유지한다."
        elif alias == "s264_lc":
            label = "defensive_control_demote_or_one_stage_audit(방어 대조 강등 또는 한 단계 감사)"
            next_use = "P1 one-stage weekday/DD audit(P1 한 단계 요일/손실폭 감사)"
            why = "net(순수익)은 좋지만 DD(손실폭) 24.39%와 Monday(월요일) -235.05가 방어 대조 역할에 불편하다."
            risk = "defensive control(방어 대조)라는 이름 때문에 DD(손실폭)를 덮으면 안 된다."
            reopen = "한 번의 bounded audit(제한 감사)에서 Monday/DD가 뚜렷하게 낮아지지 않으면 control role(대조 역할)을 강등한다."
        else:
            label = "held_rebuild_only_no_repair_loop(보류 재구축 전용, 수리 반복 금지)"
            next_use = "held until new supply structure exists(새 공급 구조 전까지 보류)"
            why = "run267DJ에는 s264_aih 생존 프로필이 없고, 이전 파괴형 가지치기 경로는 실패 기억으로 남아 있다."
            risk = "같은 repair loop(수리 반복)를 계속하면 필터만 붙이는 연구가 된다."
            reopen = "기존 threshold(임계값) 미세 조정이 아닌 새 supply/impulse structure(공급/충격 구조)가 있을 때만 재개한다."
            row = {
                "best_profile": "not_materialized_in_run267DI(267DI에서 물질화 안 됨)",
                "best_net_profit": "",
                "best_profit_factor": "",
                "best_equity_drawdown_percent": "",
                "best_trade_count": "",
                "worst_month": "prior_failure_memory(이전 실패 기억)",
                "worst_month_net": "",
                "weakest_slice": "held_no_current_survivor(현재 생존 행 없음)",
            }
            weak = {}
        output.append(
            {
                "decision_id": f"dk_decision_{alias}",
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": candidate_role,
                "best_profile": row.get("test_id") or row.get("best_profile") or "",
                "best_net_profit": row.get("net_profit") or row.get("best_net_profit") or "",
                "best_profit_factor": row.get("profit_factor") or row.get("best_profit_factor") or "",
                "best_equity_drawdown_percent": row.get("report_equity_drawdown_percent") or row.get("best_equity_drawdown_percent") or "",
                "best_trade_count": row.get("trade_count") or row.get("best_trade_count") or "",
                "worst_month": row.get("worst_month") or "",
                "worst_month_net": row.get("worst_month_net") or "",
                "weakest_slice": slice_text(weak) if weak else row.get("weakest_slice", "missing(누락)"),
                "decision_label": label,
                "next_use": next_use,
                "why": why,
                "risk_boundary": risk,
                "reopen_condition": reopen,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def feature_blueprints(decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    aia = evidence_summary(decisions, "s264_aia")
    s258 = evidence_summary(decisions, "s258_stc")
    lc = evidence_summary(decisions, "s264_lc")
    return [
        {
            "feature_id": "dk_fb01_s264_aia_dual_survivor_gate",
            "feature_family": "dual ablation/replacement survivor gate(이중 제거/대체 생존 관문)",
            "candidate_scope": "s264_aia",
            "market_meaning": "OOS anchor(표본외 앵커)가 특정 feature(피처)에 우연히 붙은 것인지, 유사 시장 의미에서도 살아남는지 본다.",
            "source_evidence": f"best_net={aia.get('best_net_profit')};PF={aia.get('best_profit_factor')};DD={aia.get('best_equity_drawdown_percent')};weak={aia.get('weakest_slice')}",
            "changed_variables": "session loss-shape(세션 손실 형태), 2024-12 month stress(2024년 12월 압박), similar replacement(유사 대체), feature ablation(피처 제거).",
            "similar_replacement_axis": "trend strength(추세 강도), volatility energy(변동성 에너지), range expansion(범위 확장)을 서로 바꿔 본다.",
            "aggressive_or_defensive": "balanced_survivor_gate(균형 생존 관문)",
            "success_read": "두 profile(프로필) 모두 PF>=1.30, DD<=18%, trades>=450, weak session loss>-110이면 Adapter watch(어댑터 관찰)를 강화한다.",
            "failure_read": "하나라도 PF<1.15 또는 net retention(순수익 유지율)<55%이면 feature over-reliance(피처 과의존)로 기록한다.",
            "materialization_note": "run267DL에서 s264_aia를 P0 생존 관문으로 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dk_fb02_s258_explosive_supply_expansion",
            "feature_family": "explosive supply expansion stress(폭발형 공급 확장 압박)",
            "candidate_scope": "s258_stc",
            "market_meaning": "얇은 거래 공급이 우연인지, 더 넓은 충격/공급 조건에서 거래 수와 수익이 같이 늘어나는지 본다.",
            "source_evidence": f"aggregate_net={s258.get('best_net_profit')};avg_PF={s258.get('best_profit_factor')};max_DD={s258.get('best_equity_drawdown_percent')};trades={s258.get('best_trade_count')}",
            "changed_variables": "short impulse(짧은 충격), supply widening(공급 확장), adjacent period pack(인접 기간 묶음).",
            "similar_replacement_axis": "tight short gate(타이트 숏 관문)를 impulse persistence(충격 지속성)와 volatility burst(변동성 폭발)로 대체한다.",
            "aggressive_or_defensive": "aggressive_explosive(공격적 폭발형)",
            "success_read": "적어도 두 기간에서 trades>=300, PF>=1.35, DD<=20%이면 stress challenger(압박 도전자)를 유지한다.",
            "failure_read": "거래 수가 계속 250 미만이면 high PF(높은 수익 팩터)를 신뢰하지 않고 stress-only(압박 전용)로 둔다.",
            "materialization_note": "방어 필터를 덧붙이지 않고 공급을 넓혀 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dk_fb03_s262_guardrail_and_s264_lc_demote_audit",
            "feature_family": "control guardrail and demotion audit(대조 가드레일과 강등 감사)",
            "candidate_scope": "s262_lih;s264_lc",
            "market_meaning": "validation-heavy(검증 중심) 후보와 defensive control(방어 대조) 후보가 실제로 덜 깨지는지 비교한다.",
            "source_evidence": f"s264_lc_DD={lc.get('best_equity_drawdown_percent')};s264_lc_weak={lc.get('weakest_slice')};s262_lih_Monday=-135.08",
            "changed_variables": "weekday/DD attribution(요일/손실폭 귀속), no new alpha filter(새 알파 필터 없음), control comparison(대조 비교).",
            "similar_replacement_axis": "calendar(달력) 금지가 아니라 session liquidity(세션 유동성)와 loss persistence(손실 지속성)로 설명한다.",
            "aggressive_or_defensive": "defensive_guardrail(방어 가드레일)",
            "success_read": "s262_lih가 더 낮은 DD(손실폭)를 유지하고 s264_lc의 Monday/DD가 뚜렷하게 낮아지면 대조 역할을 유지한다.",
            "failure_read": "s264_lc가 DD/Monday를 줄이지 못하면 defensive control(방어 대조) 지위를 강등한다.",
            "materialization_note": "한 단계 이상 같은 DD repair(손실폭 수리)를 끌지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dk_fb04_adapter_handoff_readiness_gap",
            "feature_family": "adapter handoff readiness gap(어댑터 인계 준비 공백)",
            "candidate_scope": "s264_aia;s262_lih;s258_stc",
            "market_meaning": "선택은 아니지만 후속 생존 후보가 Adapter(어댑터) 구조로 정리될 수 있는지 미리 기록한다.",
            "source_evidence": "run267DJ has MT5 report(보고서), curve diagnostics(곡선 진단), time slices(시간구간) but no Adapter package(어댑터 패키지).",
            "changed_variables": "feature order receipt(피처 순서 영수증), decision surface note(의사결정 표면 기록), risk/ATR handoff(위험/ATR 인계).",
            "similar_replacement_axis": "not a signal replacement(신호 대체 아님), handoff evidence(인계 근거) 전용.",
            "aggressive_or_defensive": "infrastructure_guardrail(기반 가드레일)",
            "success_read": "후속 실행이 살아남으면 Adapter package(어댑터 패키지) 설계에 필요한 누락 목록이 명확해야 한다.",
            "failure_read": "feature order(피처 순서)나 runtime handoff(런타임 인계)가 불명확하면 ONNX 검토 금지를 유지한다.",
            "materialization_note": "runtime authority(런타임 권위)는 주장하지 않고 receipt(영수증)만 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dk_fb05_s264_aih_rebuild_only_hold",
            "feature_family": "rebuild-only hold(재구축 전용 보류)",
            "candidate_scope": "s264_aih",
            "market_meaning": "핵심 도전자였지만 현재 경로는 수리 반복으로 끌지 않고 새 구조가 있을 때만 재개한다.",
            "source_evidence": "run267DJ has no current survivor row(현재 생존 행 없음); prior destructive prune path(이전 파괴형 가지치기 경로)는 실패 기억이다.",
            "changed_variables": "none in immediate materialization(즉시 물질화 없음).",
            "similar_replacement_axis": "new supply/impulse structure only(새 공급/충격 구조만).",
            "aggressive_or_defensive": "held_prune(보류 가지치기)",
            "success_read": "새 구조 가설이 생길 때만 reopen(재개)한다.",
            "failure_read": "threshold micro-tuning(임계값 미세 조정)만 있으면 계속 보류한다.",
            "materialization_note": "run267DL active queue(활성 대기열)에 넣지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def materialization_queue(decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    aia = evidence_summary(decisions, "s264_aia")
    s258 = evidence_summary(decisions, "s258_stc")
    s262 = evidence_summary(decisions, "s262_lih")
    lc = evidence_summary(decisions, "s264_lc")
    return [
        {
            "queue_id": "dk_q01_s264_aia_dual_survivor_ablation_replacement",
            "priority": "P0_survivor_gate(P0 생존 관문)",
            "workstream": "s264_aia_dual_survivor_gate",
            "candidate_aliases": "s264_aia",
            "feature_blueprint_scope": "dk_fb01_s264_aia_dual_survivor_gate",
            "hypothesis": "s264_aia가 진짜 구조라면 ablation(제거)과 similar replacement(유사 대체)를 동시에 압박해도 session/month(세션/월) 구멍이 제한된다.",
            "decision_use": "Adapter watch(어댑터 관찰)를 강화할지, feature reliance(피처 의존)로 낮출지 판단한다.",
            "comparison_baseline": f"run267DJ s264_aia best_net={aia.get('best_net_profit')}, PF={aia.get('best_profit_factor')}, DD={aia.get('best_equity_drawdown_percent')}, weak={aia.get('weakest_slice')}.",
            "control_variables": "US100 M5, risk/cost/spread(위험/비용/스프레드), MT5 tester profile(테스터 프로필), duplicate-boundary note(중복 경계 메모).",
            "changed_variables": "session loss-shape replacement(세션 손실 형태 대체), 2024-12 stress(2024년 12월 압박), paired ablation/replacement(쌍 제거/대체).",
            "sample_scope": "2024 historical plus adjacent survivor windows(2024 과거 구간과 인접 생존 구간).",
            "success_criteria": "PF>=1.30, DD<=18%, trades>=450, worst_session_net>-110, worst_month_net>-100.",
            "failure_criteria": "PF<1.15, DD>=22%, trades<350, or one replacement collapses below 55% net retention.",
            "invalid_conditions": "hidden calendar ban(숨은 달력 금지), feature order mismatch(피처 순서 불일치), missing MT5 report(MT5 보고서 누락).",
            "stop_conditions": "두 변형 중 하나가 크게 깨지면 s264_aia를 Adapter watch(어댑터 관찰)에서 feature reliance watch(피처 의존 관찰)로 낮춘다.",
            "evidence_plan": "MT5 KPI, trade records(거래 기록), curve diagnostics(곡선 진단), month/weekday/session/hour slices(월/요일/세션/시간 구간).",
            "materialization_instruction": "Materialize compact TA/RT attempts that pair ablation and similar replacement without new calendar-only filters.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dk_q02_s258_explosive_supply_expansion_stress",
            "priority": "P0_aggressive_explosive(P0 공격적 폭발형)",
            "workstream": "s258_explosive_supply_expansion",
            "candidate_aliases": "s258_stc",
            "feature_blueprint_scope": "dk_fb02_s258_explosive_supply_expansion",
            "hypothesis": "s258_stc가 얇은 표본 운이 아니라면 공급 확장 후에도 수익, PF(수익 팩터), DD(손실폭)가 같이 버틴다.",
            "decision_use": "stress challenger(압박 도전자)를 계속 유지할지 stress-only failure memory(압박 전용 실패 기억)로 낮출지 판단한다.",
            "comparison_baseline": f"run267DJ adjacent-period aggregate_net={s258.get('best_net_profit')}, avg_PF={s258.get('best_profit_factor')}, max_DD={s258.get('best_equity_drawdown_percent')}, trades={s258.get('best_trade_count')}.",
            "control_variables": "same risk/cost/spread(동일 위험/비용/스프레드), no defensive calendar patch(방어 달력 패치 없음).",
            "changed_variables": "impulse persistence(충격 지속성), volatility burst(변동성 폭발), supply expansion(공급 확장).",
            "sample_scope": "2023H2, 2025H1, 2025H2 adjacent periods plus current 2024 pressure.",
            "success_criteria": "at least two periods with trades>=300, PF>=1.35, DD<=20%.",
            "failure_criteria": "trades remain below 250 in most periods, or DD>=24% after supply expansion.",
            "invalid_conditions": "supply increase caused only by duplicate rows(중복 행), hidden filter loosening(숨은 필터 완화), report parse gap(보고서 파싱 공백).",
            "stop_conditions": "If supply stays thin, stop repairing and keep s258_stc as stress memory only.",
            "evidence_plan": "period KPI(기간 핵심 성과 지표), trade count distribution(거래 수 분포), DD cluster(손실폭 군집), session slices(세션 구간).",
            "materialization_instruction": "Materialize aggressive supply-widening attempts; do not solve it by adding safety filters first.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dk_q03_s262_lih_validation_guardrail_crosscheck",
            "priority": "P0_control_guardrail(P0 대조 가드레일)",
            "workstream": "s262_lih_validation_guardrail",
            "candidate_aliases": "s262_lih",
            "feature_blueprint_scope": "dk_fb03_s262_guardrail_and_s264_lc_demote_audit",
            "hypothesis": "s262_lih가 validation-heavy(검증 중심) control(대조)이라면 s264_aia/s258_stc 압박 옆에서도 덜 깨지는 참조 역할을 한다.",
            "decision_use": "후속 공격 실험의 guardrail(가드레일)로 유지할지 판단한다.",
            "comparison_baseline": f"run267DJ s262_lih net={s262.get('best_net_profit')}, PF={s262.get('best_profit_factor')}, DD={s262.get('best_equity_drawdown_percent')}, weak={s262.get('weakest_slice')}.",
            "control_variables": "same feature order(동일 피처 순서), no extra alpha filter(추가 알파 필터 없음), same 2024 pressure.",
            "changed_variables": "weekday/session/month attribution only(요일/세션/월 귀속만).",
            "sample_scope": "2024 historical and the same windows used by s264_aia/s258_stc.",
            "success_criteria": "DD stays <=16%, PF>=1.30, Monday and session loss do not deepen below run267DJ.",
            "failure_criteria": "chron_mid(중간 순서 구간) or Monday weakness deepens while challengers improve.",
            "invalid_conditions": "different data window(다른 데이터 구간), missing duplicate-boundary label(중복 경계 라벨 누락).",
            "stop_conditions": "If it no longer guards anything, keep as failure memory instead of promoting.",
            "evidence_plan": "paired candidate KPI(쌍 후보 핵심 성과 지표), curve diagnostics(곡선 진단), weak slice matrix(약점 구간 행렬).",
            "materialization_instruction": "Materialize as a guardrail row beside P0 challenger attempts.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dk_q04_s264_lc_one_stage_dd_demote_audit",
            "priority": "P1_bounded_demote_audit(P1 제한 강등 감사)",
            "workstream": "s264_lc_weekday_dd_demote",
            "candidate_aliases": "s264_lc",
            "feature_blueprint_scope": "dk_fb03_s262_guardrail_and_s264_lc_demote_audit",
            "hypothesis": "s264_lc의 수익이 방어 대조 가치라면 Monday/DD(월요일/손실폭) 약점이 한 단계 감사에서 설명되거나 줄어야 한다.",
            "decision_use": "s264_lc를 defensive control(방어 대조)에서 강등할지 결정한다.",
            "comparison_baseline": f"run267DJ s264_lc net={lc.get('best_net_profit')}, PF={lc.get('best_profit_factor')}, DD={lc.get('best_equity_drawdown_percent')}, weak={lc.get('weakest_slice')}.",
            "control_variables": "no calendar-only ban(달력 금지만 금지), same risk/cost(동일 위험/비용), same candidate surface(동일 후보 표면).",
            "changed_variables": "weekday loss persistence(요일 손실 지속성) and session liquidity proxy(세션 유동성 대리 변수).",
            "sample_scope": "2024 historical control audit only.",
            "success_criteria": "DD<20%, Monday loss>-170, 2024-06 loss>-120 without killing trade count.",
            "failure_criteria": "DD remains >=22% or Monday stays below -200.",
            "invalid_conditions": "calendar-only exclusion(달력만 제외), trade count collapse(거래 수 붕괴).",
            "stop_conditions": "If it fails, demote and do not open a third control repair loop.",
            "evidence_plan": "weekday/month/session KPI(요일/월/세션 핵심 성과 지표), DD curve zoom(손실폭 곡선 확대).",
            "materialization_instruction": "Materialize one bounded audit attempt only; do not extend repair more than one next stage.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dk_q05_adapter_handoff_gap_receipts",
            "priority": "P2_handoff_receipt(P2 인계 영수증)",
            "workstream": "adapter_handoff_gap",
            "candidate_aliases": "s264_aia;s262_lih;s258_stc",
            "feature_blueprint_scope": "dk_fb04_adapter_handoff_readiness_gap",
            "hypothesis": "후속 생존 후보가 나오더라도 Adapter(어댑터) 구조, feature order(피처 순서), decision surface(의사결정 표면), risk/ATR handoff(위험/ATR 인계)가 추적 가능해야 한다.",
            "decision_use": "Adapter package(어댑터 패키지)로 넘어갈 수 있는 근거 공백을 미리 줄인다.",
            "comparison_baseline": "run267DJ has MT5 reports but no Adapter package(어댑터 패키지) or runtime reproduction(런타임 재현).",
            "control_variables": "no ONNX export(ONNX 내보내기 없음), no runtime authority(런타임 권위 없음).",
            "changed_variables": "receipt coverage(영수증 커버리지) only.",
            "sample_scope": "survivor/stress/control rows that pass run267DL.",
            "success_criteria": "Every survivor has feature order, model/config hash, decision-surface note, and handoff gap list.",
            "failure_criteria": "Any survivor lacks a reproducible handoff receipt.",
            "invalid_conditions": "claiming ONNX readiness(ONNX 준비) from receipts alone.",
            "stop_conditions": "Do not proceed to ONNX parity(ONNX 동등성) until R&D gates are stronger.",
            "evidence_plan": "artifact registry(산출물 등록부), run manifest(실행 목록), lineage(계보), receipt CSV(영수증 CSV).",
            "materialization_instruction": "Create receipt placeholders only after run267DL materializes actual attempts.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "dk_prune_headline_profit_selection",
            "prune_label": "headline_profit_selection_forbidden(대표 수익 선택 금지)",
            "affected_scope": "all candidates(전체 후보)",
            "why_pruned": "run267DJ에서 수익과 PF(수익 팩터)가 좋아도 session/month/DD/trade supply(세션/월/손실폭/거래 공급) 약점이 남아 있다.",
            "reopen_condition": "여러 기간, 제거/대체, 곡선 확대, 거래 품질을 통과할 때만 선택 검토를 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dk_prune_s264_aih_repair_loop",
            "prune_label": "s264_aih_repair_loop_pruned(s264_aih 수리 반복 가지치기)",
            "affected_scope": "s264_aih current path(s264_aih 현재 경로)",
            "why_pruned": "run267DJ에 현재 생존 행이 없고, 기존 경로를 계속 수리하면 필터 덧붙이기 연구가 된다.",
            "reopen_condition": "새 supply/impulse structure(공급/충격 구조)가 있을 때만 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dk_prune_s264_lc_as_safe_control",
            "prune_label": "s264_lc_safe_control_claim_pruned(s264_lc 안전 대조 주장 가지치기)",
            "affected_scope": "s264_lc defensive control label(s264_lc 방어 대조 라벨)",
            "why_pruned": "DD(손실폭) 24.39%와 Monday(월요일) -235.05는 안전 대조라고 부르기 불편하다.",
            "reopen_condition": "한 단계 감사에서 DD/Monday가 명확히 낮아질 때만 대조 지위를 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dk_prune_s258_high_pf_before_supply",
            "prune_label": "s258_high_pf_before_supply_forbidden(s258 공급 전 높은 PF 선택 금지)",
            "affected_scope": "s258_stc stress challenger(s258_stc 압박 도전자)",
            "why_pruned": "세 기간 PF(수익 팩터)는 좋지만 각 기간 거래 수가 167~226으로 얇다.",
            "reopen_condition": "공급 확장 후에도 trades>=300 구간이 두 개 이상이면 재검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dk_prune_calendar_only_repair",
            "prune_label": "calendar_only_repair_pruned(달력 전용 수리 가지치기)",
            "affected_scope": "month/weekday/session weak slice repair(월/요일/세션 약점 수리)",
            "why_pruned": "특정 월/요일만 막는 방식은 시장 의미를 설명하지 않고 과적합을 키운다.",
            "reopen_condition": "volatility/session/loss-shape(변동성/세션/손실 형태) 설명이 붙을 때만 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dk_prune_onnx_before_adapter_runtime_reproduction",
            "prune_label": "onnx_before_adapter_runtime_reproduction_forbidden(어댑터/런타임 재현 전 ONNX 금지)",
            "affected_scope": "all survivors(모든 생존 후보)",
            "why_pruned": "Adapter package(어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)가 아직 없다.",
            "reopen_condition": "R&D racing(연구개발 경주) 생존, 여러 기간 안정, Adapter 구조, 런타임 재현 근거가 모두 쌓일 때만 재검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "dk_memory_s264_aia_survives_but_session_month_watch",
            "pattern": "s264_aia survives but weak session/month remains(s264_aia 생존하나 세션/월 약점 잔존)",
            "affected_scope": "s264_aia",
            "evidence": "run267DJ ablation net=1646 PF=1.448 DD=15.45, similar net=1292.34 PF=1.377 DD=14.12, weak session around -129/-115.",
            "why_fragile": "survival(생존)은 보이지만 session_07_12(세션 07-12)와 2024-12 약점이 남았다.",
            "do_not_repeat": "selecting from net/PF only(순수익/PF만 보고 선택).",
            "salvage_angle": "dual ablation/replacement survivor gate(이중 제거/대체 생존 관문).",
            "reopen_condition": "weak session and month improve without hidden calendar ban.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dk_memory_s262_lih_guardrail_not_final",
            "pattern": "s262_lih guardrail not final candidate(s262_lih 가드레일이지 최종 후보 아님)",
            "affected_scope": "s262_lih",
            "evidence": "run267DJ DD=13.95 but Monday=-135.08, session_07_12=-124.22, 2024-12=-118.64.",
            "why_fragile": "validation-heavy(검증 중심) 안정이 Adapter value(어댑터 가치)를 보장하지 않는다.",
            "do_not_repeat": "calling guardrail a selected baseline(가드레일을 선택 기준 후보로 부르기).",
            "salvage_angle": "use as control beside aggressive and survivor branches.",
            "reopen_condition": "keeps breaking less than challengers under the same pressure.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dk_memory_s258_thin_supply_high_pf",
            "pattern": "s258 high PF with thin supply(s258 높은 PF와 얇은 거래 공급)",
            "affected_scope": "s258_stc",
            "evidence": "run267DJ 2023H2 trades=178, 2025H1 trades=226, 2025H2 trades=167.",
            "why_fragile": "high PF(높은 수익 팩터)가 sparse trades(희소 거래)에 기대는지 아직 모른다.",
            "do_not_repeat": "promoting before supply proof(공급 증명 전 밀어 올리기).",
            "salvage_angle": "explosive supply expansion stress(폭발형 공급 확장 압박).",
            "reopen_condition": "trade supply and DD stay acceptable together.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dk_memory_s264_lc_profit_dd_monday_uncomfortable",
            "pattern": "s264_lc profit with DD/Monday discomfort(s264_lc 수익은 있으나 손실폭/월요일 불편)",
            "affected_scope": "s264_lc",
            "evidence": "run267DJ net=1522.61 PF=1.418 DD=24.39 Monday=-235.05.",
            "why_fragile": "defensive control(방어 대조)라면 먼저 덜 깨져야 한다.",
            "do_not_repeat": "using profit to ignore drawdown(수익으로 손실폭 덮기).",
            "salvage_angle": "one-stage DD/Monday demote audit(한 단계 손실폭/월요일 강등 감사).",
            "reopen_condition": "DD and Monday improve without trade collapse.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dk_memory_s264_aih_hold_rebuild_only",
            "pattern": "s264_aih held for rebuild only(s264_aih 재구축 전용 보류)",
            "affected_scope": "s264_aih",
            "evidence": "run267DJ has no current survivor profile; prior destructive path remains failure memory.",
            "why_fragile": "same-axis repair loop(같은 축 수리 반복)가 과제약으로 흐른다.",
            "do_not_repeat": "third repair stage with threshold tweaks(임계값 조정 3차 수리).",
            "salvage_angle": "new supply/impulse structure only(새 공급/충격 구조만).",
            "reopen_condition": "materially different feature structure exists.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dk_memory_duplicate_boundary_not_true_fallback",
            "pattern": "duplicate boundary is not true fallback(중복 경계는 실제 대체 아님)",
            "affected_scope": "all run267DJ rows",
            "evidence": "run267DJ keeps Tier A and duplicate-boundary Tier A+B only where source attempts exist.",
            "why_fragile": "true Tier B fallback(진짜 티어 B 대체)과 actual routed total(실제 라우팅 전체)은 아직 증명되지 않았다.",
            "do_not_repeat": "runtime authority(런타임 권위) or ONNX readiness(ONNX 준비) claim.",
            "salvage_angle": "handoff receipt audit(인계 영수증 감사).",
            "reopen_condition": "true fallback route evidence appears.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def performance_attribution(decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "attribution_id": "dk_attr_run267dj_survivor_control_stress_split",
            "observed_change": "; ".join(
                f"{row['candidate_alias']}:{row['decision_label']}:{row['best_net_profit']}" for row in decisions
            ),
            "comparison_baseline": "run267DJ candidate profile, curve diagnostics, negative slice summary.",
            "likely_drivers": "s264_aia dual survivor gate, s262_lih validation guardrail, s258 thin-supply high PF, s264_lc DD/Monday discomfort, s264_aih held failure memory.",
            "segment_checks": "month, weekday, session_report, hour_report, chron_segment, adjacent-period trade supply.",
            "trade_shape": "s264_aia 507/527 trades; s262_lih 462; s264_lc 473; s258_stc 167/178/226 per adjacent period; s264_aih absent.",
            "alternative_explanations": "2024-specific fit, duplicate-boundary repetition, sparse adjacent-period supply, calendar slice overfit.",
            "attribution_confidence": "medium(중간): MT5 trade/curve evidence exists, but run267DK is design-only.",
            "next_probe": "run267DL should materialize survivor, aggressive supply, guardrail, bounded demote, and handoff receipt queues.",
        }
    ]


def experiment_design_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"dk_receipt_{row['queue_id']}",
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


def result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DK shared weakness third follow-up/prune design(267DK 공유 약점 3차 후속/가지치기 설계)",
            "evidence_available": "run267DJ MT5 trade records(거래 기록), curve diagnostics(곡선 진단), time-slice KPI(시간구간 핵심 성과 지표), negative slices(음수 구간).",
            "evidence_missing": "run267DL materialization(물질화), MT5 execution(MT5 실행), Adapter package(어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).",
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
    checks = [
        (
            "all_five_candidates_decided",
            len({row["candidate_alias"] for row in decisions}) == 5,
            f"decision_aliases={';'.join(row['candidate_alias'] for row in decisions)}",
            "keeps the whole Baseline candidate pool(기준 후보군 전체)을 다룬다.",
        ),
        (
            "aggressive_explosive_queue_present",
            any("aggressive" in row["priority"] or "explosive" in row["priority"] for row in queue_rows),
            "s258 aggressive explosive queue present",
            "prevents overly defensive-only progress(방어 전용 진행 방지).",
        ),
        (
            "ablation_replacement_queue_present",
            any("ablation" in row["queue_id"] or "replacement" in row["queue_id"] for row in queue_rows),
            "s264_aia ablation/replacement queue present",
            "keeps feature reliance check alive(피처 의존 점검 유지).",
        ),
        (
            "control_guardrail_present",
            any("guardrail" in row["queue_id"] or "control" in row["priority"] for row in queue_rows),
            "s262/s264_lc control guardrail rows present",
            "keeps defensive/validation controls(방어/검증 대조)을 비교에 붙인다.",
        ),
        (
            "prune_blocks_headline_and_onnx",
            any("headline" in row["prune_id"] for row in prune_rows) and any("onnx" in row["prune_id"] for row in prune_rows),
            "headline and ONNX prune rows present",
            "prevents number-only selection and premature ONNX(숫자 선택 및 조기 ONNX 방지).",
        ),
        (
            "failure_memory_present",
            len(memory_rows) >= 5,
            f"failure_memory={len(memory_rows)}",
            "records failures as next research material(실패를 다음 연구 재료로 남긴다).",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "pass" if ok else "fail",
            "evidence": evidence,
            "effect": effect,
        }
        for gate_id, ok, evidence, effect in checks
    ]


def run_manifest(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "parent_run_id": PARENT_RUN_ID,
        "purpose": "Convert run267DJ balance/time-slice/trade-quality review into third follow-up/prune materialization design.",
        "candidate_pool": CANDIDATE_POOL,
        "inputs": {
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_candidate_profile": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "source_profile_axis": rel(SOURCE_PROFILE_AXIS_PATH),
            "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            "source_attribution": rel(SOURCE_ATTRIBUTION_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": result["outputs"],
        "branch_decisions": len(result["branch_decisions"]),
        "materialization_queue": len(result["materialization_queue"]),
        "prune_rows": len(result["prune_matrix"]),
        "failure_memory": len(result["failure_memory"]),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(created_at: str) -> dict[str, Any]:
    return {
        "lineage_id": "stage267_run267DK_lineage",
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "parent_run": PARENT_RUN_ID,
        "source_inputs": [
            rel(SOURCE_REVIEW_RESULT_PATH),
            rel(SOURCE_CANDIDATE_PROFILE_PATH),
            rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            rel(SOURCE_PROFILE_AXIS_PATH),
            rel(SOURCE_NEGATIVE_SLICE_PATH),
            rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            rel(SOURCE_ATTRIBUTION_PATH),
            rel(SOURCE_REPORT_PATH),
        ],
        "output_artifacts": [
            rel(FEATURE_BLUEPRINT_PATH),
            rel(BRANCH_DECISION_PATH),
            rel(MATERIALIZATION_QUEUE_PATH),
            rel(PRUNE_MATRIX_PATH),
            rel(FAILURE_MEMORY_PATH),
            rel(PERFORMANCE_ATTRIBUTION_PATH),
            rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            rel(RESULT_JUDGMENT_PATH),
            rel(GATE_AUDIT_PATH),
            rel(RUN_MANIFEST_PATH),
            rel(REVIEW_RESULT_PATH),
            rel(REPORT_PATH),
        ],
        "availability": "tracked_after_commit(커밋 후 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267DK Shared Weakness Third Follow-up/Prune Design(267단계 267DK 공유 약점 3차 후속/가지치기 설계)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
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
        "## Easy Read(쉬운 설명)",
        "",
        "run267DJ(267DJ 실행)는 s264_aia와 s262_lih가 살아남는 단서를 보여줬지만, 아직 선택할 단계는 아니다. s258_stc는 숫자는 강하지만 거래 수가 얇아서 공격적인 supply expansion(공급 확장)으로 더 세게 흔들어 본다. s264_lc는 수익은 있으나 DD(drawdown, 손실폭)와 Monday(월요일)가 불편해 한 단계 감사 후 강등 여부를 정한다. s264_aih는 같은 수리 반복을 끊고 새 구조가 생길 때만 재개한다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | label(판정) | next_use(다음 사용) | weakest_slice(가장 약한 구간) |",
        "|---|---|---|---|",
    ]
    for row in result["branch_decisions"]:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['decision_label']}` | {row['next_use']} | `{row['weakest_slice']}` |"
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
            "## Prune Matrix(가지치기 행렬)",
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
            "## Boundary(경계)",
            "",
            "이 설계는 R&D racing(연구개발 경주)의 다음 물질화 입력을 만드는 단계다. selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- gate_audit(관문 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DK_producer", "producer_script", PRODUCER_PATH, "Builds run267DK third follow-up/prune design."),
        ("stage267_run267DK_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Feature blueprint."),
        ("stage267_run267DK_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decision matrix."),
        ("stage267_run267DK_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Materialization queue."),
        ("stage267_run267DK_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune matrix."),
        ("stage267_run267DK_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267DK_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Performance attribution."),
        ("stage267_run267DK_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DK_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DK_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DK_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DK_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267DK_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DK_report", "review_report", REPORT_PATH, "User-facing report."),
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
        f"branch_decisions={len(result['branch_decisions'])};"
        f"materialization_queue={len(result['materialization_queue'])};"
        f"prune_rows={len(result['prune_matrix'])};"
        f"failure_memory={len(result['failure_memory'])};next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267DK_shared_weakness_breakout_third_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_third_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary evidence transformed into design; true fallback not claimed",
        "scoreboard": "experiment_design_branch_decision_materialization_queue_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_mt5_execution_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_shared_weakness_third_followup_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_third_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_third_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_third_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary design evidence",
        "kpi_scope": "experiment_design_queue_failure_memory",
        "scoreboard_lane": "shared_weakness_third_followup_design",
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
        "- run267DK_shared_weakness_breakout_third_followup_or_prune_design"
        f"(267DK 공유 약점 3차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        f"- latest_design(최신 설계): run267DK(267DK 실행) branch_decisions(분기 판단) `{len(result['branch_decisions'])}`, "
        f"materialization_queue(물질화 대기열) `{len(result['materialization_queue'])}`, "
        f"prune_rows(가지치기 행) `{len(result['prune_matrix'])}`, failure_memory(실패 기억) `{len(result['failure_memory'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DK(267DK 실행)는 run267DJ(267DJ 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 third follow-up/prune design(3차 후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): branch decisions(분기 판단) `{len(result['branch_decisions'])}`, materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`, failure memory(실패 기억) `{len(result['failure_memory'])}`를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_third_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "Effect(효과): run267DI(267DI 실행)의 MT5 report", report_line)
    current = append_after_contains(current, "## Current Next Action", summary_line)
    current = append_block_once(current, "Run267DK(267DK 실행)는 run267DJ", block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "run267DJ_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review", report_line)
    selection = append_block_once(selection, "Run267DK(267DK 실행)는 run267DJ", block)
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{STATUS}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after_contains(review, "run267DJ_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review", report_line)
    review = append_block_once(review, "Run267DK(267DK 실행)는 run267DJ", block)
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_review.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {PARENT_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {PARENT_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  next_action: {source_review.NEXT_ACTION}", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267DJ_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_report_path",
        f"  run267DK_shared_weakness_breakout_third_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DK(267DK 실행) shared weakness breakout third follow-up/prune design"
        f"(공유 약점 돌파 3차 후속/가지치기 설계) `{STATUS}`. "
        f"Effect(효과): run267DJ(267DJ 실행)의 곡선/시간구간/거래품질 근거를 materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, "
        f"prune rows(가지치기 행) `{len(result['prune_matrix'])}`개, failure memory(실패 기억) `{len(result['failure_memory'])}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus_line)
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_payload = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_PROFILE_PATH)
    summary_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    profile_rows = read_csv(SOURCE_PROFILE_AXIS_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    curve_rows = read_csv(SOURCE_CURVE_DIAGNOSTICS_PATH)
    source_attr_rows = read_csv(SOURCE_ATTRIBUTION_PATH)

    decisions = branch_decisions(candidate_rows, curve_rows, negative_rows)
    feature_rows = feature_blueprints(decisions)
    queue_rows = materialization_queue(decisions)
    prune_rows = prune_matrix()
    memory_rows = failure_memory(decisions)
    attribution_rows = performance_attribution(decisions)
    experiment_rows = experiment_design_receipts(queue_rows)
    judgment_rows = result_judgment()
    gates = gate_audit(decisions, queue_rows, prune_rows, memory_rows)
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "source_review_result": {
            "trade_records": source_payload.get("trade_record_count"),
            "time_slice_rows": source_payload.get("time_slice_row_count"),
            "curve_rows": len(curve_rows),
            "candidate_profile_rows": len(candidate_rows),
            "candidate_summary_rows": len(summary_rows),
            "profile_axis_rows": len(profile_rows),
            "negative_slices": len(negative_rows),
            "source_attribution_rows": len(source_attr_rows),
        },
        "feature_blueprints": feature_rows,
        "branch_decisions": decisions,
        "materialization_queue": queue_rows,
        "prune_matrix": prune_rows,
        "failure_memory": memory_rows,
        "performance_attribution": attribution_rows,
        "experiment_design_receipts": experiment_rows,
        "result_judgment": judgment_rows,
        "gate_audit": gates,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "outputs": {
            "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
            "branch_decisions": rel(BRANCH_DECISION_PATH),
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

    write_csv(FEATURE_BLUEPRINT_PATH, feature_rows, FEATURE_BLUEPRINT_COLUMNS)
    write_csv(BRANCH_DECISION_PATH, decisions, BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, queue_rows, MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, prune_rows, PRUNE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, memory_rows, FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, attribution_rows, PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, experiment_rows, EXPERIMENT_DESIGN_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows, RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, gates, GATE_AUDIT_COLUMNS)
    write_json(RUN_MANIFEST_PATH, run_manifest(created_at, result))
    write_json(LINEAGE_PATH, lineage(created_at))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> int:
    result = build_result()
    print(
        json.dumps(
            {
                "status": result["status"],
                "branch_decisions": len(result["branch_decisions"]),
                "materialization_queue": len(result["materialization_queue"]),
                "prune_rows": len(result["prune_matrix"]),
                "failure_memory": len(result["failure_memory"]),
                "gate_passes": sum(1 for row in result["gate_audit"] if row["status"] == "pass"),
                "gate_rows": len(result["gate_audit"]),
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": result["outputs"]["report"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
