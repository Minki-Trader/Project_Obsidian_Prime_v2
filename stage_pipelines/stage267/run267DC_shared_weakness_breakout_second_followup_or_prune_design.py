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
    run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267DC"
RUN_ID = "run267DC_stage267_shared_weakness_breakout_second_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267DC_shared_weakness_breakout_second_followup_or_prune_design_completed"
JUDGMENT = "second_followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267DD_materialize_shared_weakness_breakout_second_followup_or_prune_queue"
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DC_shared_weakness_breakout_second_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DC_shared_weakness_breakout_second_followup_or_prune_design.py")

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


def weakest_slice(candidate_alias: str, negative_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    rows = [row for row in negative_rows if row.get("candidate_alias") == candidate_alias]
    if not rows:
        return {}
    return min(rows, key=lambda row: as_float(row.get("net_profit")))


def slice_text(row: Mapping[str, Any]) -> str:
    if not row:
        return "missing"
    return f"{row.get('axis')}:{row.get('bucket')}:{row.get('net_profit')}"


def feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "dc_fb01_s258_session_cross_period_stress",
            "feature_family": "session cross-period stress(세션 확장 기간 압박)",
            "market_meaning": "s258_stc의 높은 순익이 얇은 세션 구멍을 숨기는지, 2023H2/2025H1/2025H2에서 깨뜨려 본다.",
            "candidate_scope": "s258_stc",
            "source_evidence": "run267DB s258_stc net=2311.59, PF=1.4773, trades=533, DD=16.4, session_07_12=-162.28.",
            "changed_variables": "target period(대상 기간), session loss-shape pressure(세션 손실 형태 압박), drawdown cluster zoom(손실폭 군집 확대).",
            "similar_replacement_axis": "redzone/explosive state(위험 구역/폭발형 상태)를 volatility energy(변동성 에너지)와 session liquidity pocket(세션 유동성 포켓)으로 대체한다.",
            "aggressive_or_defensive": "aggressive_stress(공격형 압박)",
            "do_not_use_as": "selected candidate(선택 후보) 또는 ONNX readiness(ONNX 준비) 근거",
            "success_read": "2개 이상 기간에서 PF>=1.35, DD<=20%, trades>=300, worst_session_net>-140이면 강한 생존 단서다.",
            "failure_read": "한 기간이라도 net<=0 또는 DD>=26%이면 stress-only(압박 전용)로 낮춘다.",
            "materialization_note": "run267DD는 s258_stc를 세션/기간 압박으로 먼저 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dc_fb02_s264_aia_adapter_watch_replacement",
            "feature_family": "OOS anchor adapter watch and replacement(표본외 앵커 어댑터 관찰과 대체)",
            "market_meaning": "s264_aia가 두 프로필에서 낮은 DD(손실폭)를 유지했으므로 Adapter(어댑터)로 구조화할 가치가 있는지 확인한다.",
            "candidate_scope": "s264_aia",
            "source_evidence": "run267DB s264_aia rows: net=1489.15/DD=14.2 and net=1445.48/DD=14.69, worst month floor=-95.66.",
            "changed_variables": "similar feature replacement(유사 피처 대체), validation-damage zoom(검증 손상 확대), adapter feature order receipt(어댑터 피처 순서 영수증).",
            "similar_replacement_axis": "state phase(상태 국면)를 range expansion(범위 확장), ATR compression(ATR 압축), shock persistence(충격 지속)로 대체한다.",
            "aggressive_or_defensive": "balanced_adapter_probe(균형 어댑터 탐침)",
            "do_not_use_as": "OOS anchor(표본외 앵커) 단독 선택",
            "success_read": "similar replacement 후 net drawdown <=35%, DD 악화 <=5%p, PF>=1.25, trades>=400이면 Adapter watch(어댑터 관찰)를 유지한다.",
            "failure_read": "유사 대체나 제거에서 net이 절반 이하로 줄면 feature reliance(피처 의존)로 기록한다.",
            "materialization_note": "run267DD는 s264_aia를 구조 후보가 아니라 관찰 후보로 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dc_fb03_s264_aih_destructive_prune_probe",
            "feature_family": "AIH destructive prune probe(AIH 파괴적 가지치기 탐침)",
            "market_meaning": "s264_aih는 높은 PF(수익 팩터)에도 2024-12, Monday(월요일), chron_mid(중간 시간 구간) 구멍이 깊으므로 살리는 실험이 아니라 깨뜨리는 실험으로 본다.",
            "candidate_scope": "s264_aih",
            "source_evidence": "run267DB s264_aih final_supply 2024-12=-261.4, Monday=-246.7; explosive chron_mid=-207.27, DD=24.03.",
            "changed_variables": "worst-month stress(최악 월 압박), chron_mid stress(중간 시간 구간 압박), supply widening disabled(공급 확대 금지).",
            "similar_replacement_axis": "supply repair(공급 수리)를 liquidity shock rejection(유동성 충격 거부)과 DD-shape(손실폭 형태)로 대체한다.",
            "aggressive_or_defensive": "destructive_prune(파괴적 가지치기)",
            "do_not_use_as": "repair loop(수리 반복)",
            "success_read": "불리한 구간에서도 DD<=20%, 2024-12>-180, Monday>-180, chron_mid>0이면 관찰만 유지한다.",
            "failure_read": "위 조건 실패 시 s264_aih high-challenger path(고도전자 경로)를 가지치기한다.",
            "materialization_note": "run267DD는 s264_aih를 추가 수리하지 않고 prune/crash probe(가지치기/충돌 탐침)로 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dc_fb04_control_pair_weekday_dd_audit",
            "feature_family": "control pair weekday/DD audit(대조 쌍 요일/손실폭 감사)",
            "market_meaning": "s264_lc와 s262_lih가 방어/검증 대조 역할을 계속 할 수 있는지 Monday(월요일)와 DD(손실폭)를 기준으로 본다.",
            "candidate_scope": "s264_lc;s262_lih",
            "source_evidence": "run267DB s264_lc DD=24.39, Monday=-235.05; s262_lih DD=13.95, Monday=-135.08.",
            "changed_variables": "weekday/DD attribution(요일/손실폭 귀속), no new alpha filter(새 알파 필터 없음), control comparison(대조 비교).",
            "similar_replacement_axis": "validation-heavy stability(검증 중심 안정성)를 weekday loss-shape(요일 손실 형태)와 session liquidity(세션 유동성)로 읽는다.",
            "aggressive_or_defensive": "control_guardrail(대조 가드레일)",
            "do_not_use_as": "공격형 실험을 막는 방어 필터",
            "success_read": "s262_lih가 낮은 DD를 유지하고 s264_lc의 Monday/DD가 설명 가능하면 control lane(대조 레인)을 유지한다.",
            "failure_read": "둘 다 같은 요일/세션에서 깊게 깨지면 shared weakness(공유 약점)로 기록한다.",
            "materialization_note": "run267DD는 공격형 큐 옆에 compact control pair(작은 대조 쌍)를 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dc_fb05_pool_ablation_replacement_gate",
            "feature_family": "pool ablation replacement gate(후보군 제거/대체 게이트)",
            "market_meaning": "강하게 보인 후보가 특정 engineered feature(엔지니어링 피처)에 붙은 우연인지 확인한다.",
            "candidate_scope": "s258_stc;s264_aia;s262_lih",
            "source_evidence": "run267DB strong and broad constructive rows need feature reliance proof before Adapter(어댑터).",
            "changed_variables": "remove one feature family(피처군 하나 제거), replace with similar market meaning(유사 시장 의미 대체).",
            "similar_replacement_axis": "ADX/trend strength(추세 강도)를 volatility energy(변동성 에너지), range expansion(범위 확장), loss persistence(손실 지속)로 대체한다.",
            "aggressive_or_defensive": "robustness_gate(견고성 게이트)",
            "do_not_use_as": "미세 조정 반복",
            "success_read": "net이 35% 이상 무너지지 않고 DD 악화가 5%p 이하이면 구조 단서다.",
            "failure_read": "PF<1.10 또는 net 절반 이하이면 feature over-reliance(피처 과의존)로 기록한다.",
            "materialization_note": "P0 압박 생존 후보만 제거/대체로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "dc_fb06_runtime_handoff_gap_audit",
            "feature_family": "runtime handoff gap audit(런타임 인계 공백 감사)",
            "market_meaning": "아직 ONNX format(ONNX 형식)이나 runtime authority(런타임 권위)가 아니라도, Adapter(어댑터) 후보가 되려면 feature order(피처 순서), decision surface(의사결정 표면), MT5 handoff(인계) 공백을 기록해야 한다.",
            "candidate_scope": "pool_survivors(후보군 생존자)",
            "source_evidence": "run267DB uses Tier A and duplicate-boundary Tier A+B; true fallback and runtime reproduction are not proved.",
            "changed_variables": "manifest completeness(목록 완전성), feature order receipt(피처 순서 영수증), no runtime claim(런타임 주장 없음).",
            "similar_replacement_axis": "not_applicable_for_signal(신호 대체 아님)",
            "aggressive_or_defensive": "infrastructure_guardrail(기반 가드레일)",
            "do_not_use_as": "runtime authority(런타임 권위)",
            "success_read": "다음 물질화가 model/set/ini/manifest(모델/설정/초기화/목록) 해시를 빠짐없이 남기면 충분하다.",
            "failure_read": "인계 목록이나 route role(라우트 역할)이 빠지면 MT5 실행 전에 차단한다.",
            "materialization_note": "run267DD materialization(물질화) 산출물에 receipt(영수증)를 포함한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def branch_decisions(
    candidate_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped = rows_by_alias(candidate_rows)
    result: list[dict[str, Any]] = []
    order = ("s258_stc", "s264_aia", "s264_aih", "s264_lc", "s262_lih")
    for alias in order:
        row = best_row(grouped.get(alias, []))
        weak = weakest_slice(alias, negative_rows)
        if alias == "s258_stc":
            label = "high_profit_stress_challenger_no_selection(고수익 압박 도전자, 선택 아님)"
            next_use = "P0 session/cross-period aggressive stress(P0 세션/확장 기간 공격 압박)"
            why = "net=2311.59, PF=1.4773, trades=533, DD=16.4는 강하지만 session_07_12=-162.28 구멍이 있다."
            risk = "stress challenger(압박 도전자)로만 보며 validation/DD(검증/손실폭) 안정 후보가 아니다."
            reopen = "인접 기간 2개 이상에서 PF>=1.35, DD<=20, trades>=300이면 Adapter watch(어댑터 관찰)로 승격 가능하다."
        elif alias == "s264_aia":
            label = "broad_oos_anchor_adapter_watch_no_selection(넓은 표본외 앵커 어댑터 관찰, 선택 아님)"
            next_use = "P0/P1 similar replacement and Adapter watch(P0/P1 유사 대체와 어댑터 관찰)"
            why = "두 profile(프로필)이 모두 14%대 DD와 500개 이상 거래를 보였지만 validation damage(검증 손상) 증명은 아직 없다."
            risk = "OOS anchor(표본외 앵커) 숫자만으로 후보를 고르면 안 된다."
            reopen = "유사 대체에서 PF>=1.25, DD 악화<=5%p, net 유지율>=65%이면 계속 관찰한다."
        elif alias == "s264_aih":
            label = "fragile_high_pf_prune_gate(높은 수익 팩터 취약 가지치기 게이트)"
            next_use = "destructive prune/crash probe only(파괴적 가지치기/충돌 탐침 전용)"
            why = "final_supply는 PF=1.6705지만 2024-12=-261.4와 Monday=-246.7이고, explosive는 chron_mid=-207.27과 DD=24.03이다."
            risk = "repair loop(수리 반복)로 끌면 필터 덧붙이기 연구가 된다."
            reopen = "한 번의 파괴적 압박에서 2024-12>-180, Monday>-180, chron_mid>0이면 관찰만 유지한다."
        elif alias == "s264_lc":
            label = "defensive_control_dd_warning_no_selection(방어 대조 손실폭 경고, 선택 아님)"
            next_use = "control pair weekday/DD audit(대조 쌍 요일/손실폭 감사)"
            why = "net=1522.61은 좋지만 DD=24.39와 Monday=-235.05가 방어 대조 역할을 흔든다."
            risk = "방어 후보라고 부르기 전에 실제로 덜 깨지는지 봐야 한다."
            reopen = "같은 조건에서 s262_lih보다 DD와 Monday가 개선되면 control lane(대조 레인)에 남긴다."
        else:
            label = "validation_heavy_control_watch_no_selection(검증 중심 대조 관찰, 선택 아님)"
            next_use = "control pair and feature reliance gate(대조 쌍 및 피처 의존 게이트)"
            why = "DD=13.95로 안정적이지만 net=1304.06과 Monday=-135.08, chron_mid=-10.3이 남아 있다."
            risk = "validation-heavy(검증 중심)라고 해서 확장성이나 Adapter(어댑터) 가치를 보장하지 않는다."
            reopen = "control pair에서 가장 덜 깨지고 유사 대체에서도 유지되면 구조 대조로 남긴다."
        result.append(
            {
                "decision_id": f"dc_decision_{alias}",
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
                "weakest_slice": slice_text(weak),
                "decision_label": label,
                "next_use": next_use,
                "why": why,
                "risk_boundary": risk,
                "reopen_condition": reopen,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return result


def materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "dc_q01_s258_session_cross_period_stress",
            "priority": "P0_aggressive_stress(우선순위0 공격 압박)",
            "workstream": "s258_session_cross_period(세션 확장 기간)",
            "candidate_aliases": "s258_stc",
            "feature_blueprint_scope": "dc_fb01_s258_session_cross_period_stress",
            "hypothesis": "s258_stc가 진짜 강하면 session_07_12(보고 시간 07-12 세션) 구멍과 인접 기간 압박에서도 덜 깨진다.",
            "decision_use": "s258_stc를 stress-only(압박 전용)로 낮출지, Adapter watch(어댑터 관찰)로 넘길지 판단한다.",
            "comparison_baseline": "run267DB s258_stc net=2311.59, PF=1.4773, trades=533, DD=16.4, worst_session=-162.28.",
            "control_variables": "US100 M5, cost/spread/risk, feature order(피처 순서), MT5 tester profile(테스터 프로필).",
            "changed_variables": "period pack(기간 묶음) 2023H2/2025H1/2025H2 and session loss-shape stress(세션 손실 형태 압박).",
            "sample_scope": "historical_2024 plus adjacent periods(2024 과거 압박 및 인접 기간)",
            "success_criteria": "2개 이상 기간에서 PF>=1.35, DD<=20%, trades>=300, worst_session_net>-140.",
            "failure_criteria": "net<=0, DD>=26%, or session loss deepens below -220.",
            "invalid_conditions": "hidden calendar ban(숨은 달력 금지), feature order mismatch(피처 순서 불일치), missing MT5 report(MT5 보고서 누락).",
            "stop_conditions": "한 기간에서 DD>=26이면 s258_stc를 stress-only로 낮추고 반복 수리를 중단한다.",
            "evidence_plan": "MT5 KPI, trade list(거래 목록), curve diagnostics(곡선 진단), month/weekday/session slices(월/요일/세션 구간).",
            "materialization_instruction": "Create compact cross-period TA/RT attempts for s258_stc without adding calendar filters.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dc_q02_s264_aia_adapter_replacement_watch",
            "priority": "P0_adapter_watch(우선순위0 어댑터 관찰)",
            "workstream": "s264_aia_adapter_replacement(어댑터 대체 관찰)",
            "candidate_aliases": "s264_aia",
            "feature_blueprint_scope": "dc_fb02_s264_aia_adapter_watch_replacement",
            "hypothesis": "s264_aia가 특정 state feature(상태 피처)에 우연히 붙은 것이 아니라면 유사 대체에서도 DD(손실폭)가 낮게 유지된다.",
            "decision_use": "s264_aia를 Adapter(어댑터) 구조화 관찰 후보로 유지할지 결정한다.",
            "comparison_baseline": "run267DB s264_aia best net=1489.15, PF=1.4019, trades=529, DD=14.2.",
            "control_variables": "same model surface(같은 모델 표면), risk/cost, source feature order(원천 피처 순서), historical_2024.",
            "changed_variables": "similar replacement(유사 대체), one-category ablation(범주 1개 제거), validation-damage zoom(검증 손상 확대).",
            "sample_scope": "historical_2024 first, adjacent period only if structural receipt is complete(2024 우선, 구조 영수증 완료 시 인접 기간).",
            "success_criteria": "net retention>=65%, PF>=1.25, DD worsening<=5%p, trades>=400.",
            "failure_criteria": "PF<1.10, net retention<50%, or DD>=22%.",
            "invalid_conditions": "changed risk/cost(위험/비용 변경), missing feature order receipt(피처 순서 영수증 누락).",
            "stop_conditions": "두 대체 축 모두 무너지면 OOS anchor(표본외 앵커) 분기를 낮춘다.",
            "evidence_plan": "delta KPI(차이 KPI), feature order receipt, curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토).",
            "materialization_instruction": "Materialize s264_aia with one similar replacement and one ablation candidate; no selection claim.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dc_q03_s264_aih_destructive_prune_probe",
            "priority": "P0_destructive_prune(우선순위0 파괴적 가지치기)",
            "workstream": "s264_aih_prune_or_crash(가지치기 또는 충돌)",
            "candidate_aliases": "s264_aih",
            "feature_blueprint_scope": "dc_fb03_s264_aih_destructive_prune_probe",
            "hypothesis": "s264_aih가 정말 핵심 도전자라면 최악 월/월요일/중간 구간을 직접 압박해도 무너지지 않아야 한다.",
            "decision_use": "s264_aih high-challenger path(고도전자 경로)를 유지할지 가지치기할지 결정한다.",
            "comparison_baseline": "run267DB final_supply PF=1.6705 but 2024-12=-261.4 and Monday=-246.7; explosive DD=24.03 and chron_mid=-207.27.",
            "control_variables": "no additional supply repair(추가 공급 수리 없음), same cost/risk/feature order.",
            "changed_variables": "worst-month stress, Monday/DD-shape stress, chron_mid stress(최악 월/월요일/중간구간 압박).",
            "sample_scope": "historical_2024 destructive probe only(2024 파괴적 탐침 전용)",
            "success_criteria": "2024-12>-180, Monday>-180, chron_mid>0, DD<=20.",
            "failure_criteria": "any target slice remains below threshold or DD>=24.",
            "invalid_conditions": "turning the probe into a new repair loop(탐침을 새 수리 반복으로 바꿈).",
            "stop_conditions": "one failed destructive probe prunes the high-challenger path.",
            "evidence_plan": "month/weekday/chron slices, curve DD, trade count(월/요일/시간순 구간, 곡선 손실폭, 거래 수).",
            "materialization_instruction": "Create at most one s264_aih destructive probe; do not tune thresholds afterward.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dc_q04_control_pair_weekday_dd_audit",
            "priority": "P1_control_guardrail(우선순위1 대조 가드레일)",
            "workstream": "control_pair_weekday_dd(대조 쌍 요일 손실폭)",
            "candidate_aliases": "s264_lc;s262_lih",
            "feature_blueprint_scope": "dc_fb04_control_pair_weekday_dd_audit",
            "hypothesis": "방어/검증 대조 후보는 공격형 후보 옆에서 실제로 덜 깨지는지 보여야 한다.",
            "decision_use": "s264_lc와 s262_lih의 control lane(대조 레인)을 유지할지 조정할지 결정한다.",
            "comparison_baseline": "run267DB s264_lc DD=24.39/Monday=-235.05 vs s262_lih DD=13.95/Monday=-135.08.",
            "control_variables": "no new alpha feature(새 알파 피처 없음), same MT5 settings(같은 MT5 설정), same period/cost/risk.",
            "changed_variables": "weekday/DD attribution only(요일/손실폭 귀속만).",
            "sample_scope": "same period as P0 stress attempts(우선순위0 압박과 같은 기간)",
            "success_criteria": "one control is clearly less broken in DD and weak weekday while retaining PF>=1.25.",
            "failure_criteria": "both controls share the same deep month/session hole.",
            "invalid_conditions": "omitting controls while making pool-wide claims(후보군 전체 주장 중 대조 누락).",
            "stop_conditions": "if controls add no explanatory value, record failure memory and stop that lane.",
            "evidence_plan": "control KPI, weak-slice comparison, candidate decision update(대조 KPI/약점 비교/후보 판단 갱신).",
            "materialization_instruction": "Materialize compact control pair attempts beside aggressive queue.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dc_q05_survivor_ablation_replacement_gate",
            "priority": "P1_robustness_gate(우선순위1 견고성 게이트)",
            "workstream": "survivor_ablation_replacement(생존 후보 제거/대체)",
            "candidate_aliases": "s258_stc;s264_aia;s262_lih",
            "feature_blueprint_scope": "dc_fb05_pool_ablation_replacement_gate",
            "hypothesis": "생존 후보는 feature/category ablation(피처/범주 제거)과 similar replacement(유사 대체)에서도 완전히 무너지지 않아야 한다.",
            "decision_use": "Adapter(어댑터) 개발 가치가 있는 구조인지 확인한다.",
            "comparison_baseline": "run267DB constructive rows and run267DD P0 survivors(건설적 행과 다음 P0 생존 후보).",
            "control_variables": "same period/cost/risk/model family(같은 기간/비용/위험/모델 계열).",
            "changed_variables": "remove one feature family and replace one similar axis(피처군 하나 제거 및 유사 축 하나 대체).",
            "sample_scope": "only candidates surviving dc_q01/dc_q02/dc_q04(dc_q01/dc_q02/dc_q04 생존 후보만).",
            "success_criteria": "net retention>=65%, PF>=1.20, DD worsening<=5%p.",
            "failure_criteria": "net retention<50%, PF<1.10, or DD worsening>8%p.",
            "invalid_conditions": "running before survivor set exists(생존 후보 확정 전 실행).",
            "stop_conditions": "if no P0 survivor exists, hold this queue and record blocked reason.",
            "evidence_plan": "delta KPI, feature order receipt, curve/time-slice review(차이 KPI/피처 순서 영수증/곡선 시간구간 검토).",
            "materialization_instruction": "Hold until P0 survivor list exists; then materialize narrow ablation/replacement.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dc_q06_runtime_handoff_receipt_gap",
            "priority": "P2_handoff_guardrail(우선순위2 인계 가드레일)",
            "workstream": "runtime_handoff_receipt_gap(런타임 인계 영수증 공백)",
            "candidate_aliases": "pool_survivors",
            "feature_blueprint_scope": "dc_fb06_runtime_handoff_gap_audit",
            "hypothesis": "다음 단계로 갈 후보는 성과뿐 아니라 model/set/ini/manifest(모델/설정/초기화/목록)와 feature order(피처 순서) 추적이 가능해야 한다.",
            "decision_use": "Adapter package(어댑터 패키지) 전환 전 필요한 인계 공백을 닫는다.",
            "comparison_baseline": "run267DB duplicate-boundary rows; true fallback and runtime reproduction not claimed.",
            "control_variables": "no ONNX export(ONNX 내보내기 없음), no runtime authority(런타임 권위 없음), no operating claim(운영 주장 없음).",
            "changed_variables": "manifest completeness and handoff receipt only(목록 완전성과 인계 영수증만).",
            "sample_scope": "run267DD materialization outputs(267DD 물질화 산출물)",
            "success_criteria": "every attempt has model hash, feature order, set/ini, route role, report path.",
            "failure_criteria": "any attempt lacks identity needed for later MT5 reproduction.",
            "invalid_conditions": "using receipt completeness to imply runtime authority(영수증 완전성을 런타임 권위로 해석).",
            "stop_conditions": "block MT5 execution if handoff identity is incomplete.",
            "evidence_plan": "run_manifest, artifact registry, feature order receipt, handoff checks(실행 목록/산출물 등록/피처 순서/인계 검사).",
            "materialization_instruction": "Add required receipts to run267DD materialization package before MT5 execution.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "dc_prune_headline_profit_selection",
            "prune_label": "headline_profit_selection_forbidden(대표 수익 선택 금지)",
            "affected_scope": "all candidates(전체 후보)",
            "why_pruned": "run267DB에서 s258_stc와 s264_aia 숫자가 좋아 보여도 기간/피처/구간 검증이 아직 부족하다.",
            "reopen_condition": "확장 기간, ablation/replacement(제거/대체), curve zoom(곡선 확대), trade quality(거래 품질)를 통과할 때만 재검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dc_prune_s264_aih_repair_loop",
            "prune_label": "s264_aih_repair_loop_pruned(s264_aih 수리 반복 가지치기)",
            "affected_scope": "s264_aih supply/final repair",
            "why_pruned": "2024-12=-261.4, Monday=-246.7, chron_mid=-207.27이 남아 수리 반복으로 끌면 과제약 연구가 된다.",
            "reopen_condition": "one destructive probe(파괴적 탐침 1회)에서 target weak slices(대상 약점 구간)가 동시에 살아날 때만 관찰로 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dc_prune_calendar_only_monday_ban",
            "prune_label": "calendar_only_monday_ban_pruned(달력 월요일 금지만 가지치기)",
            "affected_scope": "Monday/session weakness repair(월요일/세션 약점 수리)",
            "why_pruned": "요일 금지만 붙이는 방식은 필터 덕지덕지 연구가 되며 시장 의미를 설명하지 못한다.",
            "reopen_condition": "volatility/session loss-shape(변동성/세션 손실 형태)로 유사 대체 의미가 확인될 때만 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dc_prune_duplicate_boundary_as_true_fallback",
            "prune_label": "duplicate_boundary_not_true_fallback(중복 경계는 실제 대체 아님)",
            "affected_scope": "Tier A+B duplicate-boundary rows(티어 A+B 중복 경계 행)",
            "why_pruned": "run267DB는 Tier A와 duplicate-boundary Tier A+B만 있으며 true Tier B fallback(진짜 티어 B 대체)을 증명하지 않는다.",
            "reopen_condition": "actual routed total(실제 라우팅 전체)과 Tier B fallback component(티어 B 대체 구성)를 분리 기록할 때만 재개한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "dc_prune_onnx_before_adapter_evidence",
            "prune_label": "onnx_before_adapter_evidence_forbidden(어댑터 근거 전 ONNX 금지)",
            "affected_scope": "all current survivors(현재 생존 후보 전체)",
            "why_pruned": "run267DB는 balance/time-slice review(잔액/시간구간 검토)일 뿐 Adapter package(어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)가 없다.",
            "reopen_condition": "Adapter structure, feature order, decision surface, MT5 reproduction evidence(어댑터 구조/피처 순서/의사결정 표면/MT5 재현 근거)가 쌓일 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "dc_memory_s264_aih_month_weekday_chron_holes",
            "pattern": "s264_aih month/weekday/chron holes(s264_aih 월/요일/시간순 구멍)",
            "affected_scope": "s264_aih",
            "evidence": "run267DB: final_supply 2024-12=-261.4, Monday=-246.7; explosive chron_mid=-207.27.",
            "why_fragile": "높은 PF(수익 팩터)가 깊은 특정 구간 손실을 숨긴다.",
            "do_not_repeat": "s264_aih supply repair(공급 수리)를 계속 넓히기.",
            "salvage_angle": "one destructive prune probe(파괴적 가지치기 탐침 1회)로 살릴지 닫을지 정한다.",
            "reopen_condition": "target weak slices(대상 약점 구간)가 동시에 개선될 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dc_memory_s258_sparse_session_hole",
            "pattern": "s258 sparse session hole(s258 얇은 세션 구멍)",
            "affected_scope": "s258_stc",
            "evidence": "run267DB: net=2311.59 but session_07_12=-162.28 with 3 trades.",
            "why_fragile": "거래 수 전체는 충분해도 특정 세션의 작은 표본 손실이 curve(곡선)를 흔들 수 있다.",
            "do_not_repeat": "session(세션)을 단순 금지 필터로 막기.",
            "salvage_angle": "session liquidity pocket(세션 유동성 포켓)과 volatility energy(변동성 에너지)로 유사 대체한다.",
            "reopen_condition": "인접 기간에서도 세션 손실이 얕아지고 전체 성과가 유지될 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dc_memory_control_monday_dd_split",
            "pattern": "control Monday/DD split(대조 후보 월요일/손실폭 분리)",
            "affected_scope": "s264_lc;s262_lih",
            "evidence": "run267DB: s264_lc DD=24.39/Monday=-235.05; s262_lih DD=13.95/Monday=-135.08.",
            "why_fragile": "control(대조) 후보도 같은 약점에서 깨질 수 있어 대조 역할을 자동으로 믿으면 안 된다.",
            "do_not_repeat": "defensive control(방어 대조) 라벨만 보고 안전하다고 말하기.",
            "salvage_angle": "weekday/DD audit(요일/손실폭 감사)로 s262_lih와 s264_lc의 역할을 분리한다.",
            "reopen_condition": "대조 후보가 공격형 후보보다 명확히 덜 깨지는 축이 확인될 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dc_memory_feature_reliance_unproven",
            "pattern": "feature reliance unproven(피처 의존 미검증)",
            "affected_scope": "s258_stc;s264_aia;s262_lih",
            "evidence": "run267DB is curve/time-slice review only; ablation/replacement survival is not yet proved.",
            "why_fragile": "좋은 숫자가 특정 engineered feature(엔지니어링 피처)에 우연히 붙었을 수 있다.",
            "do_not_repeat": "feature ablation(피처 제거) 없이 Adapter(어댑터)나 ONNX format(ONNX 형식)을 논하기.",
            "salvage_angle": "survivor-only ablation/replacement gate(생존 후보 전용 제거/대체 게이트)를 둔다.",
            "reopen_condition": "유사 대체에서도 net/PF/DD가 유지될 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "dc_memory_duplicate_boundary_not_runtime",
            "pattern": "duplicate boundary is not runtime proof(중복 경계는 런타임 근거 아님)",
            "affected_scope": "all run267DB rows",
            "evidence": "run267DB has Tier A and duplicate-boundary Tier A+B; true fallback and runtime reproduction remain unproved.",
            "why_fragile": "duplicate-boundary(중복 경계)를 actual routed total(실제 라우팅 전체)처럼 읽으면 근거가 과장된다.",
            "do_not_repeat": "runtime authority(런타임 권위) 또는 ONNX readiness(ONNX 준비) 주장하기.",
            "salvage_angle": "next materialization(다음 물질화)에 handoff receipts(인계 영수증)를 붙인다.",
            "reopen_condition": "actual routed total과 runtime handoff evidence가 생길 때.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def performance_attribution(source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    observed = "; ".join(
        f"{row.get('candidate_alias')}:{row.get('test_id')}:{row.get('observed_change')}"
        for row in source_rows[:7]
    )
    return [
        {
            "attribution_id": "dc_attr_headline_profit_vs_curve_holes",
            "observed_change": observed,
            "comparison_baseline": "run267DB candidate_profile_review and negative_slice_summary(후보-프로필 검토와 음수 구간 요약)",
            "likely_drivers": "explosive/session/state profiles(폭발형/세션/상태 프로필), candidate role differences(후보 역할 차이), weak-slice concentration(약점 구간 집중).",
            "segment_checks": "month, weekday, session_report, chron_segment, route_role(月/요일/세션/시간순/라우트 역할).",
            "trade_shape": "s258_stc trades=533; s264_aia trades=529/543; s264_aih trades=307/516; controls trades=462/473.",
            "alternative_explanations": "duplicate-boundary replication(중복 경계 반복), 2024-only fit(2024 전용 적합), sparse session losses(얇은 세션 손실).",
            "attribution_confidence": "medium(중간): trade list and time-slice evidence exists but cross-period/replacement evidence is still missing.",
            "next_probe": "run267DD materialization should split aggressive pressure, adapter watch, destructive prune, and control audit.",
        }
    ]


def experiment_design_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"dc_design_{row['queue_id']}",
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
            "result_subject": "run267DC shared weakness second follow-up/prune design(267DC 공유 약점 2차 후속/가지치기 설계)",
            "evidence_available": "run267DB trade records(거래 기록), candidate profile review(후보 프로필 검토), negative slice summary(음수 구간 요약), performance attribution(성과 귀인)",
            "evidence_missing": "run267DD materialization(물질화), MT5 execution(실행), cross-period results(확장 기간 결과), ablation/replacement results(제거/대체 결과), Adapter package(어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)",
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
        ("all_five_candidates_decided", len(decisions) == 5, f"decision_rows={len(decisions)}", "keeps whole Baseline candidate pool(기준 후보군 전체)을 다룬다."),
        ("aggressive_queue_present", any("aggressive" in row["priority"] or "destructive" in row["priority"] for row in queue_rows), "aggressive/destructive queue present", "prevents overly defensive-only progress(방어 전용 진행 방지)."),
        ("ablation_replacement_present", any("ablation" in row["queue_id"] or "replacement" in row["queue_id"] for row in queue_rows), "ablation/replacement queue present", "keeps feature reliance check alive(피처 의존 점검 유지)."),
        ("control_pair_present", any("control" in row["queue_id"] for row in queue_rows), "control queue present", "keeps defensive/validation controls(방어/검증 대조)을 붙인다."),
        ("prune_blocks_headline_and_onnx", any("headline" in row["prune_id"] for row in prune_rows) and any("onnx" in row["prune_id"] for row in prune_rows), "headline and ONNX prune rows present", "prevents number-only selection and premature ONNX(숫자 선택 및 조기 ONNX 방지)."),
        ("failure_memory_present", len(memory_rows) >= 4, f"failure_memory={len(memory_rows)}", "records failures as next research material(실패를 다음 연구 재료로 남긴다)."),
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


def run_manifest(
    created_at: str,
    queue_rows: Sequence[Mapping[str, Any]],
    prune_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "parent_run_id": PARENT_RUN_ID,
        "purpose": "Convert run267DB balance/time-slice/trade-quality evidence into next materialization design.",
        "candidate_pool": CANDIDATE_POOL,
        "inputs": {
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_candidate_profile": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "source_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "source_profile_axis": rel(SOURCE_PROFILE_AXIS_PATH),
            "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_attribution": rel(SOURCE_ATTRIBUTION_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
        },
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
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "queue_count": len(queue_rows),
        "prune_count": len(prune_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(created_at: str) -> dict[str, Any]:
    return {
        "lineage_id": "stage267_run267DC_lineage",
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "parent_run": PARENT_RUN_ID,
        "input_artifacts": [
            rel(SOURCE_REVIEW_RESULT_PATH),
            rel(SOURCE_CANDIDATE_PROFILE_PATH),
            rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            rel(SOURCE_PROFILE_AXIS_PATH),
            rel(SOURCE_NEGATIVE_SLICE_PATH),
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
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267DC Shared Weakness Second Follow-up/Prune Design(267단계 267DC 공유 약점 2차 후속/가지치기 설계)",
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
        "## Design Read(설계 판독)",
        "",
        "Run267DB(267DB 실행)는 강한 숫자와 깊은 약점을 동시에 보여줬다. Run267DC(267DC 실행)는 이를 후보 선택이 아니라 다음 압박 설계로 바꾼다.",
        "",
        "- `s258_stc`: high profit stress challenger(고수익 압박 도전자). 세션/확장 기간으로 더 깨뜨려 본다.",
        "- `s264_aia`: adapter watch(어댑터 관찰). 유사 피처 대체와 제거에서 버티는지 본다.",
        "- `s264_aih`: destructive prune probe(파괴적 가지치기 탐침). 수리 반복이 아니라 깨뜨려 보고 닫을지 정한다.",
        "- `s264_lc`, `s262_lih`: control pair(대조 쌍). 월요일/DD(손실폭)로 대조 역할을 다시 검증한다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | label(라벨) | next_use(다음 사용) | weakest_slice(최약 구간) |",
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
            "이 설계는 R&D racing(연구개발 경주)을 앞으로 밀기 위한 것이다. 후보 선택, 운영 승격, runtime authority(런타임 권위), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- feature_blueprint(피처 청사진): `{rel(FEATURE_BLUEPRINT_PATH)}`",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DC_producer", "producer_script", PRODUCER_PATH, "Builds run267DC second follow-up/prune design."),
        ("stage267_run267DC_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Feature blueprint."),
        ("stage267_run267DC_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Branch decision matrix."),
        ("stage267_run267DC_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Materialization queue."),
        ("stage267_run267DC_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Prune matrix."),
        ("stage267_run267DC_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Failure memory."),
        ("stage267_run267DC_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Performance attribution."),
        ("stage267_run267DC_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DC_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DC_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DC_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DC_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DC_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DC_report", "review_report", REPORT_PATH, "User-facing report."),
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
        "row_id": "stage267_run267DC_shared_weakness_breakout_second_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_second_followup_or_prune_design",
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
        "lane": "baseline_candidate_racing_shared_weakness_second_followup_prune_design",
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
        "tier_scope": "Tier A and duplicate-boundary design evidence",
        "kpi_scope": "experiment_design_queue_failure_memory",
        "scoreboard_lane": "shared_weakness_followup_design",
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
        "- run267DC_shared_weakness_breakout_second_followup_or_prune_design"
        f"(267DC 공유 약점 2차 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        f"- latest_design(최신 설계): run267DC(267DC 실행) branch_decisions(분기 판단) `{len(result['branch_decisions'])}`, "
        f"materialization_queue(물질화 대기열) `{len(result['materialization_queue'])}`, "
        f"prune_rows(가지치기 행) `{len(result['prune_matrix'])}`, failure_memory(실패 기억) `{len(result['failure_memory'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DC(267DC 실행)는 run267DB(267DB 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 second follow-up/prune design(2차 후속/가지치기 설계)으로 바꿨다.",
            f"Effect(효과): branch decisions(분기 판단) `{len(result['branch_decisions'])}`, materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`, failure memory(실패 기억) `{len(result['failure_memory'])}`를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "stage267_run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review.md", report_line)
    current = append_after_contains(current, "## Current Next Action", summary_line)
    current = append_block_once(current, "Run267DC(267DC 실행)는 run267DB", block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review", report_line)
    selection = append_block_once(selection, "Run267DC(267DC 실행)는 run267DB", block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review", report_line)
    review_index = append_block_once(review_index, "Run267DC(267DC 실행)는 run267DB", block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DC(267DC 실행) shared weakness breakout second follow-up/prune design"
        f"(공유 약점 돌파 2차 후속/가지치기 설계) `{STATUS}`. "
        f"Effect(효과): run267DB(267DB 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 근거를 "
        f"materialization queue(물질화 대기열) `{len(result['materialization_queue'])}`개, prune matrix(가지치기 행렬) `{len(result['prune_matrix'])}`개, "
        f"failure memory(실패 기억) `{len(result['failure_memory'])}`개로 바꿨고, selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_review.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {PARENT_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {PARENT_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  next_action: {source_review.NEXT_ACTION}", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267DB_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_report_path",
        f"  run267DC_shared_weakness_breakout_second_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    workspace = prepend_current_focus(workspace, focus_line)
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_review_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_PROFILE_PATH)
    summary_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    profile_rows = read_csv(SOURCE_PROFILE_AXIS_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    source_attr_rows = read_csv(SOURCE_ATTRIBUTION_PATH)

    feature_rows = feature_blueprints()
    decisions = branch_decisions(candidate_rows, negative_rows)
    queue_rows = materialization_queue()
    prune_rows = prune_matrix()
    memory_rows = failure_memory(negative_rows)
    attribution_rows = performance_attribution(source_attr_rows)
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
            "trade_records": source_review_result.get("trade_record_count"),
            "time_slice_rows": source_review_result.get("time_slice_row_count"),
            "candidate_profile_rows": len(candidate_rows),
            "candidate_summary_rows": len(summary_rows),
            "profile_axis_rows": len(profile_rows),
            "negative_slices": len(negative_rows),
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
    write_json(RUN_MANIFEST_PATH, run_manifest(created_at, queue_rows, prune_rows))
    write_json(LINEAGE_PATH, lineage(created_at))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> None:
    result = build_result()
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
                "report": result["outputs"]["report"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
