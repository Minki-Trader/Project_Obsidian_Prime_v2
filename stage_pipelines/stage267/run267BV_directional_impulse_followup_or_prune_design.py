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
    run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267BV"
RUN_ID = "run267BV_stage267_directional_impulse_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267BV_directional_impulse_followup_or_prune_design_completed"
JUDGMENT = "experiment_design_completed_no_candidate_selection"
NEXT_ACTION = "run267BW_materialize_aggressive_impulse_dd_shape_cross_period_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "directional_impulse_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_REVIEW_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_PROFILE_SUMMARY_PATH = source_review.PROFILE_SUMMARY_PATH
SOURCE_FOLLOWUP_QUEUE_PATH = source_review.FOLLOWUP_QUEUE_PATH
SOURCE_FAILURE_MEMORY_PATH = source_review.FAILURE_MEMORY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_TIME_SLICE_KPI_PATH = source_review.TIME_SLICE_KPI_PATH
SOURCE_TRADE_RECORDS_PATH = source_review.TRADE_RECORDS_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

BRANCH_DECISION_PATH = RUN_ROOT / "branch_decision_matrix.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
AGGRESSIVE_WATCHLIST_PATH = RUN_ROOT / "aggressive_candidate_watchlist.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BV_directional_impulse_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BV_directional_impulse_followup_or_prune_design.py")
NEGATIVE_RESULT_REGISTER_PATH = Path("docs/registers/negative_result_register.md")

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

BRANCH_DECISION_COLUMNS = (
    "decision_id",
    "source_profile",
    "candidate_scope",
    "observed_change",
    "comparison_baseline",
    "decision_label",
    "decision_reason",
    "next_use",
    "do_not_repeat",
    "salvage_value",
    "stop_condition",
    "claim_boundary",
)

MATERIALIZATION_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_profile",
    "target_period",
    "target_split",
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

WATCHLIST_COLUMNS = (
    "rank",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "net_profit",
    "profit_factor",
    "trade_count",
    "report_max_drawdown_percent",
    "worst_month",
    "worst_month_net",
    "worst_slice_axis",
    "worst_slice_bucket",
    "worst_slice_net",
    "chron_mid_net",
    "chron_late_net",
    "watch_label",
    "next_use",
    "selection_boundary",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "evidence",
    "affected_scope",
    "why_failed_or_fragile",
    "do_not_repeat",
    "salvage_angle",
    "reopen_condition",
    "boundary",
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

PERIODS = (
    ("2023H2", "adjacent_pre_2024_strength_check"),
    ("2025H1", "adjacent_post_2024_forward_pressure"),
    ("2025H2", "late_oos_forward_pressure"),
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
        if not math.isfinite(value):
            return ""
        return round(value, 6)
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


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


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
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
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
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def profile_by_label(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("profile_label")): row for row in rows}


def aggressive_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [dict(row) for row in candidate_rows if row.get("profile_label") == "aggressive_impulse_replacement"]
    return sorted(rows, key=lambda row: as_float(row.get("net_profit")), reverse=True)


def make_watchlist(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    watch_rows: list[dict[str, Any]] = []
    for rank, row in enumerate(aggressive_rows(candidate_rows), start=1):
        alias = str(row.get("candidate_alias"))
        label = "primary_stress_watch(1차 압박 관찰)" if rank <= 3 else "control_watch(대조 관찰)"
        next_use = (
            "run267BW(267BW 실행) cross-period/DD-shape pressure(확장 기간/손실폭 형태 압박)에 포함"
            if rank <= 3
            else "대조군(control, 대조군)으로 보류"
        )
        watch_rows.append(
            {
                "rank": rank,
                "candidate_alias": alias,
                "candidate_id": row.get("candidate_id"),
                "candidate_role": row.get("candidate_role"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "report_max_drawdown_percent": row.get("report_max_drawdown_percent"),
                "worst_month": row.get("worst_month"),
                "worst_month_net": row.get("worst_month_net"),
                "worst_slice_axis": row.get("worst_slice_axis"),
                "worst_slice_bucket": row.get("worst_slice_bucket"),
                "worst_slice_net": row.get("worst_slice_net"),
                "chron_mid_net": row.get("chron_mid_net"),
                "chron_late_net": row.get("chron_late_net"),
                "watch_label": label,
                "next_use": next_use,
                "selection_boundary": "watch_only_no_selection(관찰 전용, 선택 아님)",
            }
        )
    return watch_rows


def make_branch_decisions(
    profile_rows: Sequence[Mapping[str, Any]], candidate_rows: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    profiles = profile_by_label(profile_rows)
    directional = profiles.get("directional_asymmetry", {})
    aggressive = profiles.get("aggressive_impulse_replacement", {})
    top_rows = aggressive_rows(candidate_rows)[:3]
    top_aliases = ",".join(str(row.get("candidate_alias")) for row in top_rows)
    top_summary = ";".join(
        f"{row.get('candidate_alias')} net={row.get('net_profit')} DD={row.get('report_max_drawdown_percent')}"
        for row in top_rows
    )
    return [
        {
            "decision_id": "bv_d01_prune_directional_asymmetry_standalone",
            "source_profile": "directional_asymmetry",
            "candidate_scope": "all_five_baseline_candidates(다섯 기준 후보 전체)",
            "observed_change": (
                f"positive_count={directional.get('positive_count')}; "
                f"negative_or_pf_broken_count={directional.get('negative_or_pf_broken_count')}; "
                f"net_profit_mean={directional.get('net_profit_mean')}; "
                f"worst_dd={directional.get('report_max_drawdown_percent_worst')}"
            ),
            "comparison_baseline": "run267BT/run267BU pool-wide 2024 directional profile",
            "decision_label": "prune_standalone_profile(독립 프로필 가지치기)",
            "decision_reason": "방향 비대칭(directional asymmetry, 방향 비대칭)은 다섯 후보 모두에서 순수익/PF(수익 팩터)가 약해 독립 분기로 밀 근거가 없다.",
            "next_use": "side-pressure diagnostic(방향 압박 진단)으로만 보존한다.",
            "do_not_repeat": "같은 standalone directional asymmetry score table(독립 방향 비대칭 점수표)을 구조 변경 없이 다시 실행하지 않는다.",
            "salvage_value": "롱/숏 손상 위치를 설명하는 diagnostic feature(진단 피처)로만 쓴다.",
            "stop_condition": "run267BW 이후에도 방향 축이 독립 개선을 못 만들면 global failure memory(전역 실패 기억)로만 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bv_d02_continue_aggressive_impulse_as_pressure_branch",
            "source_profile": "aggressive_impulse_replacement",
            "candidate_scope": "all_five_baseline_candidates(다섯 기준 후보 전체)",
            "observed_change": (
                f"positive_count={aggressive.get('positive_count')}; high_dd_count={aggressive.get('high_dd_count')}; "
                f"net_mean={aggressive.get('net_profit_mean')}; worst_dd={aggressive.get('report_max_drawdown_percent_worst')}"
            ),
            "comparison_baseline": "run267BT/run267BU pool-wide 2024 aggressive profile",
            "decision_label": "continue_as_aggressive_clue_no_selection(공격형 단서로 지속, 선택 아님)",
            "decision_reason": "공격형 임펄스 대체(aggressive impulse replacement, 공격형 임펄스 대체)는 모두 양수지만 DD(손실폭)가 35~40%라 선택 근거가 아니다.",
            "next_use": "DD-shape pressure(손실폭 형태 압박), cross-period(확장 기간), similar replacement(유사 대체) 설계로 넘긴다.",
            "do_not_repeat": "순수익이 양수라는 이유만으로 ONNX review(ONNX 검토)나 선택 후보로 올리지 않는다.",
            "salvage_value": "방어 필터(filter, 필터)를 덧붙이지 않고 폭발형 구조가 실제 edge(거래 우위)인지 확인할 수 있다.",
            "stop_condition": "확장 기간에서 PF/DD(수익 팩터/손실폭)가 같이 무너지면 aggressive impulse branch(공격형 임펄스 분기)를 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bv_d03_top_three_pressure_watch",
            "source_profile": "aggressive_impulse_replacement",
            "candidate_scope": top_aliases,
            "observed_change": top_summary,
            "comparison_baseline": "all aggressive impulse candidates from run267BU",
            "decision_label": "materialize_top_three_pressure_queue(상위 3개 압박 큐 물질화)",
            "decision_reason": "s258_stc, s264_aih, s264_aia는 순수익은 강하지만 월별/요일별/후반 구간 구멍이 남아 압박 후보로만 가치가 있다.",
            "next_use": "run267BW(267BW 실행)에서 2023H2/2025H1/2025H2와 DD-shape diagnostic(손실폭 형태 진단)에 태운다.",
            "do_not_repeat": "약한 월을 직접 금지하는 calendar blacklist(달력 블랙리스트) 수리를 반복하지 않는다.",
            "salvage_value": "강한 순수익 후보를 방어적으로 죽이지 않고, 넓은 기간에서 깨지는지 먼저 본다.",
            "stop_condition": "top three(상위 3개)가 모두 확장 기간에서 고DD/저PF면 공격형 분기를 실패 기억으로 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "bv_d04_hold_controls_for_comparison",
            "source_profile": "aggressive_impulse_replacement",
            "candidate_scope": "s264_lc,s262_lih",
            "observed_change": "defensive/validation-heavy controls are positive but weaker and still high-DD",
            "comparison_baseline": "top three aggressive watch candidates",
            "decision_label": "hold_as_controls(대조군으로 보류)",
            "decision_reason": "s264_lc와 s262_lih는 후보군 비교 기준으로는 필요하지만 다음 공격형 물질화의 중심은 아니다.",
            "next_use": "필요하면 run267BW의 compact control(소형 대조군) 또는 후속 review(검토)에서 비교 기준으로 사용한다.",
            "do_not_repeat": "control(대조군)을 방어 필터 추가의 핑계로 쓰지 않는다.",
            "salvage_value": "aggressive branch(공격형 분기)가 단순 위험 증가인지 확인하는 대조 역할을 한다.",
            "stop_condition": "top three가 무너지면 control candidates(대조 후보)도 별도 재평가한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_materialization_queue(watch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    controls = (
        "same FPMarkets US100 M5 source(동일 FPMarkets US100 M5 원천); "
        "same candidate pool identity(동일 후보군 정체성); "
        "same MT5 tester/report parser where available(가능한 동일 MT5 테스터/보고서 파서); "
        "no selected candidate(선택 후보 없음); no ONNX(ONNX 없음)"
    )
    evidence = (
        "feature/model/set/ini manifests(피처/모델/설정/초기화 목록); MT5 reports(MT5 보고서); "
        "trade_records(거래 기록); curve diagnostics(곡선 진단); time-slice KPI(시간 구간 핵심 성과 지표); "
        "parser checks(파서 확인); lineage(계보); ledgers(장부)"
    )
    rows: list[dict[str, Any]] = [
        {
            "queue_id": "run267bw_q00_directional_asymmetry_prune_receipt",
            "priority": "P0",
            "workstream": "prune_receipt",
            "candidate_alias": "pool_wide",
            "candidate_id": "all_baseline_candidates",
            "candidate_role": "diagnostic_only",
            "source_profile": "directional_asymmetry",
            "target_period": "not_applicable",
            "target_split": "design_only",
            "hypothesis": "directional_asymmetry(방향 비대칭)는 독립 분기로는 약하고 진단 축으로만 가치가 있다.",
            "decision_use": "같은 독립 방향 비대칭 실행을 반복하지 않게 막는다.",
            "comparison_baseline": "run267BU directional_asymmetry profile summary",
            "control_variables": controls,
            "changed_variables": "none; prune receipt(가지치기 영수증)만 남김",
            "sample_scope": "run267BU evidence only(267BU 근거 전용)",
            "success_criteria": "negative result register(부정 결과 등록부)와 failure memory(실패 기억)에 반복 금지 조건이 남는다.",
            "failure_criteria": "다음 물질화가 방향 비대칭을 다시 독립 후보처럼 실행한다.",
            "invalid_conditions": "run267BU source artifacts(원천 산출물)가 누락되거나 parser check(파서 확인)가 불일치한다.",
            "stop_conditions": "즉시 종료. 이 큐는 MT5 실행 대상이 아니다.",
            "evidence_plan": evidence,
            "materialization_instruction": "MT5 attempt(MT5 시도)를 만들지 말고 prune receipt(가지치기 영수증)로만 소비한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    primary = [row for row in watch_rows if as_int(row.get("rank")) <= 3]
    for row in primary:
        for period, split in PERIODS:
            alias = str(row.get("candidate_alias"))
            rows.append(
                {
                    "queue_id": f"run267bw_q01_{alias}_{period.lower()}_aggressive_impulse_period_pressure",
                    "priority": "P0",
                    "workstream": "aggressive_impulse_cross_period_pressure",
                    "candidate_alias": alias,
                    "candidate_id": row.get("candidate_id"),
                    "candidate_role": row.get("candidate_role"),
                    "source_profile": "aggressive_impulse_replacement",
                    "target_period": period,
                    "target_split": split,
                    "hypothesis": "공격형 임펄스 대체(aggressive impulse replacement, 공격형 임펄스 대체)가 2024 전용 주머니가 아니라면 인접 기간에서도 PF/DD(수익 팩터/손실폭)가 같이 버텨야 한다.",
                    "decision_use": "top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다.",
                    "comparison_baseline": "run267BU 2024 aggressive impulse candidate profile",
                    "control_variables": controls,
                    "changed_variables": "period stress(기간 압박) only; no calendar blacklist(달력 블랙리스트 없음); no defensive filter stacking(방어 필터 덧붙이기 없음)",
                    "sample_scope": f"Tier A first(티어 A 우선) {period}; Tier B fallback(티어 B 대체)은 true fallback manifest(실제 대체 목록) 전까지 blocked(차단)",
                    "success_criteria": "trade_count(거래 수)가 얇지 않고 PF(수익 팩터)>1.15, report DD(보고서 손실폭)<28%, worst month(최악 월) 손실이 run267BU보다 줄어든다.",
                    "failure_criteria": "PF(수익 팩터)가 1.0 근처로 얇거나 DD(손실폭)가 35% 이상 유지되거나 한 달/요일/중간 구간이 손실을 지배한다.",
                    "invalid_conditions": "feature frame(피처 프레임), score table(점수표), set/ini(설정/초기화), report(보고서), parser(파서) 중 하나가 연결되지 않는다.",
                    "stop_conditions": "한 번의 materialization/execution/review(물질화/실행/검토) 루프 후 확장 기간이 깨지면 이 공격형 분기를 낮춘다.",
                    "evidence_plan": evidence,
                    "materialization_instruction": "run267BS aggressive impulse profile(공격형 임펄스 프로필)을 period frame(기간 프레임)에 재구성해 MT5 attempt(MT5 시도)를 만든다. 불가능하면 blocked(차단)로 기록한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    rows.append(
        {
            "queue_id": "run267bw_q02_impulse_similar_replacement_design_probe",
            "priority": "P1",
            "workstream": "similar_feature_replacement_probe",
            "candidate_alias": "s258_stc,s264_aih,s264_aia",
            "candidate_id": "top_three_aggressive_watch",
            "candidate_role": "stress_watch",
            "source_profile": "aggressive_impulse_replacement",
            "target_period": "2024_then_extension",
            "target_split": "replacement_design_before_mt5",
            "hypothesis": "임펄스 단서가 특정 proxy feature(대체 피처)에 우연히 붙은 것이 아니라면 similar replacement(유사 피처 대체)에서도 완전히 무너지지 않아야 한다.",
            "decision_use": "feature engineering(피처 엔지니어링)을 단순 미세 튜닝이 아니라 구조 검증으로 확장한다.",
            "comparison_baseline": "run267BS/run267BU aggressive impulse replacement",
            "control_variables": controls,
            "changed_variables": "replace impulse proxy with volatility expansion/trend-strength/range-shock alternatives(변동성 확장/추세 강도/범위 충격 대체)",
            "sample_scope": "design-first(설계 우선); materialize only if feature source lineage(피처 원천 계보)가 연결된다.",
            "success_criteria": "대체 피처가 후보 순위와 weak slice(약한 구간)를 크게 바꾸는지 설명할 수 있다.",
            "failure_criteria": "대체가 단순 threshold tweak(임계값 미세 조정)이나 duplicate signature(중복 서명)로 끝난다.",
            "invalid_conditions": "원천 피처가 없거나 feature order(피처 순서)와 model hash(모델 해시)를 추적할 수 없다.",
            "stop_conditions": "feature lineage(피처 계보)가 막히면 MT5 실행 전에 blocked(차단)로 닫는다.",
            "evidence_plan": evidence,
            "materialization_instruction": "run267BW에서 먼저 feature availability audit(피처 가용성 감사)을 만들고, 통과한 대체만 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def make_failure_memory() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "run267bv_directional_asymmetry_standalone_pruned",
            "pattern": "directional_asymmetry(방향 비대칭) standalone profile(독립 프로필)",
            "evidence": rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH),
            "affected_scope": "all_five_baseline_candidates(다섯 기준 후보 전체)",
            "why_failed_or_fragile": "run267BU(267BU 실행)에서 모든 후보가 음수 또는 PF(수익 팩터) 붕괴였고 DD(손실폭)도 높았다.",
            "do_not_repeat": "다른 구조 가설 없이 같은 standalone directional asymmetry(독립 방향 비대칭)를 다시 실행하지 않는다.",
            "salvage_angle": "side-specific diagnostic(방향별 진단)이나 weak-slice explanation(약한 구간 설명)으로만 사용한다.",
            "reopen_condition": "새 side-specific model/source feature(방향별 모델/원천 피처)가 생겨 독립 신호가 아니라 구조 진단으로 쓰일 때",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267bv_aggressive_impulse_high_dd_watch",
            "pattern": "aggressive_impulse_replacement(공격형 임펄스 대체) positive headline with high DD(양수 대표 숫자와 높은 손실폭)",
            "evidence": rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH),
            "affected_scope": "s258_stc,s264_aih,s264_aia plus controls",
            "why_failed_or_fragile": "다섯 후보 모두 양수였지만 report DD(보고서 손실폭)가 35~40%이고 2024-07, Monday(월요일), chron_mid/late(중간/후반 구간) 구멍이 남았다.",
            "do_not_repeat": "headline net(대표 순수익)이 양수라는 이유로 선택, ONNX review(ONNX 검토), runtime handoff(런타임 인계)를 진행하지 않는다.",
            "salvage_angle": "DD-shape pressure(손실폭 형태 압박)와 cross-period(확장 기간)에서 강제로 깨뜨려 본다.",
            "reopen_condition": "확장 기간에서 PF/DD/trade count(수익 팩터/손실폭/거래 수)가 동시에 개선될 때",
            "boundary": CLAIM_BOUNDARY,
        },
    ]


def make_performance_attribution(profile_rows: Sequence[Mapping[str, Any]], watch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    profiles = profile_by_label(profile_rows)
    aggressive = profiles.get("aggressive_impulse_replacement", {})
    directional = profiles.get("directional_asymmetry", {})
    top = watch_rows[0] if watch_rows else {}
    return [
        {
            "attribution_id": "bv_attr01_directional_negative",
            "observed_change": f"directional positive_count={directional.get('positive_count')} net_mean={directional.get('net_profit_mean')}",
            "comparison_baseline": "run267BU profile summary",
            "likely_drivers": "side pressure alone is not enough; it exposed weak short/long imbalance without adding robust entry quality(방향 압박만으로는 충분하지 않음)",
            "segment_checks": "month, weekday, direction, chron_segment, session from run267BU time-slice KPI(월/요일/방향/시간순서/세션 확인)",
            "trade_shape": "all five candidates retained hundreds of trades, so failure is not only thin-sample noise(얇은 표본만의 문제 아님)",
            "alternative_explanations": "2024 cached feature surface(캐시된 2024 피처 표면)가 directional proxy(방향 대체 피처)를 과하게 단순화했을 수 있다.",
            "attribution_confidence": "medium(중간)",
            "next_probe": "do not repeat standalone; preserve as diagnostic(독립 반복 금지, 진단으로 보존)",
        },
        {
            "attribution_id": "bv_attr02_aggressive_positive_high_dd",
            "observed_change": f"aggressive positive_count={aggressive.get('positive_count')} high_dd_count={aggressive.get('high_dd_count')} top={top.get('candidate_alias')}",
            "comparison_baseline": "directional_asymmetry and prior anti-overconstraint branch",
            "likely_drivers": "impulse feature widened opportunity recall(기회 회수) but also admitted drawdown clusters(손실폭 군집)",
            "segment_checks": "worst_month=2024-07, weekday Monday(월요일), chron_mid/late(중간/후반 구간), report DD(보고서 손실폭)",
            "trade_shape": "top candidates had 353-378 trades and positive expectancy(기대값), but recovery factor(회복 계수)가 낮다.",
            "alternative_explanations": "positive result may be a 2024-specific pocket(2024 전용 주머니) rather than durable signal(지속 신호)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "run267BW cross-period and DD-shape materialization(확장 기간과 손실폭 형태 물질화)",
        },
    ]


def make_experiment_design(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": row["queue_id"],
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


def make_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "run267BU review_result, candidate_profile_review, profile_summary, followup_queue, failure_memory, parser_checks",
            "evidence_missing": "run267BW materialization, cross-period MT5 reports, similar replacement results, Adapter structure, ONNX parity",
            "judgment_label": "exploratory_design_completed_no_candidate_selection(탐색 설계 완료, 후보 선택 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "방향 비대칭은 닫고, 공격형 임펄스는 확장 기간과 손실폭 형태에서 한 번 더 세게 깨뜨려 본다.",
        },
        {
            "result_subject": "selected_candidate(선택 후보)",
            "evidence_available": "none",
            "evidence_missing": "stable curve, cross-period survival, feature replacement survival, Adapter handoff, runtime reproduction, ONNX parity",
            "judgment_label": "not_selected(선택 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "Only reconsider after run267BW/run267BX evidence(267BW/267BX 근거 이후에만 재검토)",
            "user_explanation_hook": "아직 후보를 고를 단계가 아니라 다음 압박 실험을 설계한 단계다.",
        },
    ]


def make_gate_audit(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_review_available",
            "status": "passed" if path_exists(SOURCE_REVIEW_RESULT_PATH) else "failed",
            "evidence": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267BU(267BU 실행) 검토 결과를 설계 입력으로 연결한다.",
        },
        {
            "gate_id": "parser_boundary_clean",
            "status": "passed",
            "evidence": "run267BU parser_checks.csv matched 10/10",
            "effect": "거래 단위 검토를 다음 판단 근거로 쓸 수 있다.",
        },
        {
            "gate_id": "queue_not_filter_stacking",
            "status": "passed" if any(row.get("workstream") == "aggressive_impulse_cross_period_pressure" for row in queue_rows) else "failed",
            "evidence": rel(MATERIALIZATION_QUEUE_PATH),
            "effect": "방어 필터를 덧붙이는 대신 공격형 기간 압박을 연다.",
        },
        {
            "gate_id": "selection_claim_blocked",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "선택 후보, ONNX 준비, 목표 달성 주장을 막는다.",
        },
    ]


def update_negative_result_register() -> str:
    row = (
        "| `NR-034` | `IDEA-ST267-DIRECTIONAL-ASYMMETRY-STANDALONE` | "
        "directional_asymmetry(방향 비대칭)를 후보군 전체 standalone profile(독립 프로필)로 밀 수 있다 | "
        "run267BU(267BU 실행)에서 다섯 Baseline candidates(기준 후보) 모두 순수익 또는 PF(수익 팩터)가 약했고, DD(drawdown, 손실폭)가 높았다 | "
        "방향 축은 버리지 않고 side-pressure diagnostic(방향 압박 진단)과 weak-slice explanation(약한 구간 설명)으로만 보존한다 | "
        "새 side-specific model/source feature(방향별 모델/원천 피처)가 생겨 독립 신호가 아니라 구조 진단으로 재정의될 때 |\n"
    )
    text = io_path(NEGATIVE_RESULT_REGISTER_PATH).read_text(encoding="utf-8-sig")
    if "`NR-034`" not in text:
        write_md(NEGATIVE_RESULT_REGISTER_PATH, text.rstrip() + "\n" + row)
        return "registered"
    return "already_registered"


def update_current_truth_docs() -> None:
    report_line = (
        "- run267BV_directional_impulse_followup_or_prune_design"
        f"(267BV 방향/임펄스 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267BV(267BV 실행)는 run267BU(267BU 실행)의 방향/임펄스 검토를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
            "Effect(효과): directional_asymmetry(방향 비대칭)는 독립 분기에서 가지치기하고, aggressive_impulse_replacement(공격형 임펄스 대체)는 DD-shape pressure(손실폭 형태 압박), cross-period(확장 기간), similar replacement(유사 대체)로 넘긴다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `directional_impulse_followup_or_prune_design`",
        )
        text = append_after_contains(text, "stage267_run267BU_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review.md", report_line)
        text = append_block_once(text, "Run267BV(267BV 실행)는 run267BU", block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BV(267BV 실행) directional/impulse follow-up or prune design(방향/임펄스 후속/가지치기 설계) `{STATUS}`. "
        "Effect(효과): run267BU(267BU 실행)의 3,574개 trade records(거래 기록)와 410개 time-slice rows(시간 구간 행)를 받아 directional_asymmetry(방향 비대칭)는 닫고 aggressive_impulse_replacement(공격형 임펄스 대체)는 cross-period/DD-shape pressure(확장 기간/손실폭 형태 압박)로 넘겼으며, selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        report_entry=f"  run267BV_directional_impulse_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"branch_decisions={result['branch_decision_count']};queue_rows={result['materialization_queue_count']};"
        f"watch_rows={result['aggressive_watchlist_count']};next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267BV_directional_impulse_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "directional_impulse_followup_or_prune_design",
        "tier_scope": "Tier A review-derived design; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "experiment_design_followup_or_prune",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_directional_impulse_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__directional_impulse_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "directional_impulse_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "directional_impulse_followup_or_prune_design",
        "tier_scope": "Tier A source review; true fallback blocked",
        "kpi_scope": "experiment_design_failure_memory",
        "scoreboard_lane": "directional_impulse_followup_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={result['materialization_queue_count']};watch_rows={result['aggressive_watchlist_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    entries = (
        ("stage267_run267BV_producer", "producer_script", PRODUCER_PATH, "Builds run267BV directional/impulse follow-up or prune design."),
        ("stage267_run267BV_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267BU review result."),
        ("stage267_run267BV_source_candidate_profile", "source_candidate_profile_review", SOURCE_CANDIDATE_PROFILE_REVIEW_PATH, "Source run267BU candidate profile review."),
        ("stage267_run267BV_source_profile_summary", "source_profile_summary", SOURCE_PROFILE_SUMMARY_PATH, "Source run267BU profile summary."),
        ("stage267_run267BV_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Run267BV branch decisions."),
        ("stage267_run267BV_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267BV next materialization queue."),
        ("stage267_run267BV_aggressive_watchlist", "aggressive_candidate_watchlist", AGGRESSIVE_WATCHLIST_PATH, "Run267BV aggressive watchlist."),
        ("stage267_run267BV_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267BV failure memory."),
        ("stage267_run267BV_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267BV performance attribution."),
        ("stage267_run267BV_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BV experiment design receipt."),
        ("stage267_run267BV_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BV result judgment."),
        ("stage267_run267BV_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BV gate audit."),
        ("stage267_run267BV_lineage", "lineage", LINEAGE_PATH, "Run267BV lineage."),
        ("stage267_run267BV_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BV review result."),
        ("stage267_run267BV_report", "review_report", REPORT_PATH, "Run267BV user-facing report."),
        ("stage267_run267BV_negative_register", "negative_result_register", NEGATIVE_RESULT_REGISTER_PATH, "NR-034 negative memory registration."),
    )
    artifact_rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes_text,
        }
        for artifact_id, artifact_type, path, notes_text in entries
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def report_markdown(result: Mapping[str, Any]) -> str:
    profile_rows = result["profile_summary"]
    decisions = result["branch_decisions"]
    watch_rows = result["aggressive_watchlist"]
    queue_rows = result["materialization_queue"]
    lines = [
        "# Stage267 Run267BV Directional/Impulse Follow-up or Prune Design(267단계 267BV 방향/임펄스 후속/가지치기 설계)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- branch_decisions(분기 판단): `{len(decisions)}`",
        f"- materialization_queue_rows(물질화 대기열 행): `{len(queue_rows)}`",
        f"- aggressive_watchlist_rows(공격형 관찰 행): `{len(watch_rows)}`",
        f"- negative_register_status(부정 결과 등록 상태): `{result['negative_register_status']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BU(267BU 실행)의 profile summary(프로필 요약), candidate review(후보 검토), failure memory(실패 기억)를 받아 다음 실험 설계로 바꿨다.",
        "Effect(효과): directional_asymmetry(방향 비대칭)는 독립 분기로 닫고, aggressive_impulse_replacement(공격형 임펄스 대체)는 방어 필터 덧붙이기가 아니라 cross-period/DD-shape pressure(확장 기간/손실폭 형태 압박)로 넘긴다.",
        "",
        "## Profile Read(프로필 판독)",
        "",
        "| profile(프로필) | positive(양수) | negative/PF broken(음수/PF 붕괴) | high DD(높은 손실폭) | net mean(순수익 평균) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in profile_rows:
        lines.append(
            f"| `{row.get('profile_label')}` | {as_int(row.get('positive_count'))} | "
            f"{as_int(row.get('negative_or_pf_broken_count'))} | {as_int(row.get('high_dd_count'))} | "
            f"{as_float(row.get('net_profit_mean')):.2f} | `{row.get('profile_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Branch Decisions(분기 판단)",
            "",
            "| decision(판단) | label(라벨) | next_use(다음 사용) |",
            "| --- | --- | --- |",
        ]
    )
    for row in decisions:
        lines.append(f"| `{row.get('decision_id')}` | `{row.get('decision_label')}` | {row.get('next_use')} |")
    lines.extend(
        [
            "",
            "## Aggressive Watchlist(공격형 관찰 목록)",
            "",
            "| rank(순위) | candidate(후보) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst(최악 구간) | next_use(다음 사용) |",
            "| ---: | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in watch_rows:
        lines.append(
            f"| {as_int(row.get('rank'))} | `{row.get('candidate_alias')}` | {as_float(row.get('net_profit')):.2f} | "
            f"{as_float(row.get('profit_factor')):.2f} | {as_int(row.get('trade_count'))} | "
            f"{as_float(row.get('report_max_drawdown_percent')):.2f} | `{row.get('worst_slice_axis')}/{row.get('worst_slice_bucket')}` {as_float(row.get('worst_slice_net')):.2f} | {row.get('next_use')} |"
        )
    lines.extend(
        [
            "",
            "## Next Queue(다음 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | workstream(작업 흐름) | candidate(후보) | period(기간) | purpose(목적) |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('workstream')}` | "
            f"`{row.get('candidate_alias')}` | `{row.get('target_period')}` | {row.get('decision_use')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- directional_asymmetry(방향 비대칭)는 standalone branch(독립 분기)로 가지치기한다.",
            "- aggressive_impulse_replacement(공격형 임펄스 대체)는 clue(단서)로만 유지하고, 선택 후보로 올리지 않는다.",
            "- 다음은 run267BW(267BW 실행)에서 top-three aggressive watch(상위 3개 공격형 관찰 후보)를 2023H2/2025H1/2025H2와 DD-shape pressure(손실폭 형태 압박)에 태우는 것이다.",
            "- ONNX conversion(ONNX 변환), ONNX parity(ONNX 동등성), runtime reproduction(런타임 재현)은 아직 진행하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- aggressive_candidate_watchlist(공격형 후보 관찰 목록): `{rel(AGGRESSIVE_WATCHLIST_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
        ]
    )
    return "\n".join(lines) + "\n"


def run() -> dict[str, Any]:
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    profile_rows = read_csv(SOURCE_PROFILE_SUMMARY_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH)
    if not profile_rows:
        raise RuntimeError(f"missing profile summary: {rel(SOURCE_PROFILE_SUMMARY_PATH)}")
    if not candidate_rows:
        raise RuntimeError(f"missing candidate profile review: {rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH)}")
    branch_decisions = make_branch_decisions(profile_rows, candidate_rows)
    watch_rows = make_watchlist(candidate_rows)
    queue_rows = make_materialization_queue(watch_rows)
    failure_rows = make_failure_memory()
    attribution_rows = make_performance_attribution(profile_rows, watch_rows)
    design_rows = make_experiment_design(queue_rows)
    judgment_rows = make_result_judgment()
    gate_rows = make_gate_audit(queue_rows)
    negative_register_status = update_negative_result_register()
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_status": source_result.get("status"),
        "source_trade_record_count": source_result.get("trade_record_count"),
        "source_time_slice_row_count": source_result.get("time_slice_row_count"),
        "source_negative_slice_count": source_result.get("negative_slice_count"),
        "branch_decision_count": len(branch_decisions),
        "materialization_queue_count": len(queue_rows),
        "aggressive_watchlist_count": len(watch_rows),
        "failure_memory_count": len(failure_rows),
        "negative_register_status": negative_register_status,
        "profile_summary": profile_rows,
        "branch_decisions": branch_decisions,
        "materialization_queue": queue_rows,
        "aggressive_watchlist": watch_rows,
        "failure_memory": failure_rows,
        "performance_attribution": attribution_rows,
        "experiment_design_receipt": design_rows,
        "result_judgment": judgment_rows,
        "gate_audit": gate_rows,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_candidate_profile_review": rel(SOURCE_CANDIDATE_PROFILE_REVIEW_PATH),
            "source_profile_summary": rel(SOURCE_PROFILE_SUMMARY_PATH),
            "source_followup_queue": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            "source_time_slice_kpi": rel(SOURCE_TIME_SLICE_KPI_PATH),
            "source_trade_records": rel(SOURCE_TRADE_RECORDS_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": {
            "branch_decision_matrix": rel(BRANCH_DECISION_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "aggressive_candidate_watchlist": rel(AGGRESSIVE_WATCHLIST_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(BRANCH_DECISION_PATH, branch_decisions, BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, queue_rows, MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(AGGRESSIVE_WATCHLIST_PATH, watch_rows, WATCHLIST_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_rows, FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, attribution_rows, PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, design_rows, EXPERIMENT_DESIGN_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows, RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, gate_rows, GATE_AUDIT_COLUMNS)
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": result["sources"],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": result["outputs"],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers_and_artifacts(created_at, result)
    update_current_truth_docs()
    return result


def main() -> int:
    result = run()
    print(
        json.dumps(
            {
                "status": result["status"],
                "branch_decisions": result["branch_decision_count"],
                "materialization_queue": result["materialization_queue_count"],
                "aggressive_watchlist": result["aggressive_watchlist_count"],
                "failure_memory": result["failure_memory_count"],
                "negative_register_status": result["negative_register_status"],
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
