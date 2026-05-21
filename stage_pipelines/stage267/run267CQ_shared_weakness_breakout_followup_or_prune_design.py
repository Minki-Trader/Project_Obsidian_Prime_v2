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
    run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267CQ"
RUN_ID = "run267CQ_stage267_shared_weakness_breakout_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267CQ_shared_weakness_breakout_followup_or_prune_design_completed"
JUDGMENT = "experiment_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CR_materialize_shared_weakness_breakout_followup_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_PROFILE_PATH = source_review.CANDIDATE_PROFILE_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CQ_shared_weakness_breakout_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CQ_shared_weakness_breakout_followup_or_prune_design.py")

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

CANDIDATE_ORDER = ("s264_lc", "s264_aia", "s264_aih", "s262_lih", "s258_stc")

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
    "weakest_weekday",
    "weakest_weekday_net",
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
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, item in enumerate(lines):
        if needle in item:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            break
    return "\n".join(lines) + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            break
    return "\n".join(lines) + "\n"


def prepend_current_focus(text: str, focus_line: str) -> str:
    if f"`{STATUS}`" in text:
        return text
    return text.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)


def group_by(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get(key)), []).append(row)
    return grouped


def best_profile_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            as_float(row.get("net_profit")),
            as_float(row.get("profit_factor")),
            -as_float(row.get("report_equity_drawdown_percent")),
        ),
    )


def feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_id": "cq_fb01_state_phase_monday_replacement",
            "feature_family": "non_calendar_state_phase(비달력 상태 국면)",
            "market_meaning": "Monday(월요일) 손실을 요일 필터가 아니라 volatility/trend phase(변동성/추세 국면)로 설명하는지 확인한다.",
            "candidate_scope": "s264_aih;s264_lc;s262_lih;s264_aia;s258_stc",
            "source_evidence": "run267CP negative slices: Monday loss appears across all five baseline candidates(월요일 손실이 후보 5개 전체에서 반복).",
            "changed_variables": "state phase interaction, ATR percentile slope, trend persistence bucket, loss-shape cooldown",
            "similar_replacement_axis": "ADX/DI strength can be replaced with trend-persistence and range-expansion proxies(추세 강도는 추세 지속/범위 확장 대체 지표로 점검).",
            "aggressive_or_defensive": "balanced(균형)",
            "do_not_use_as": "literal Monday-off or calendar ban(월요일 제외/달력 금지 규칙)",
            "success_read": "Monday net improves at least 30% without reducing trade count below useful supply(월요일 순손실 30% 이상 완화, 거래 수 유지).",
            "failure_read": "headline net improves but one month or weekday hole deepens(대표 순수익은 좋아도 월/요일 구멍이 깊어짐).",
            "materialization_note": "run267CR should create feature/model/set inputs for pool-wide MT5 pressure.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cq_fb02_anchor_cross_period_pressure",
            "feature_family": "cross_period_anchor_pressure(확장 기간 앵커 압박)",
            "market_meaning": "s264_lc와 s264_aia의 높은 net/PF가 2024에만 예쁜지 2023H2/2025H1/2025H2로 압박한다.",
            "candidate_scope": "s264_lc;s264_aia",
            "source_evidence": "s264_lc net=1883.88 DD=13.52; s264_aia net=1659.28 PF=1.533047 but DD=28.17.",
            "changed_variables": "period packs, OOS anchor stress, identical cost and tester settings",
            "similar_replacement_axis": "period-adjacent replacement(인접 기간 대체)",
            "aggressive_or_defensive": "defensive_pressure(방어 압박)",
            "do_not_use_as": "candidate selection or operating reference(후보 선택/운영 기준)",
            "success_read": "both candidates avoid deep weak-month expansion across adjacent periods(인접 기간에서 약한 월 확대가 없음).",
            "failure_read": "2024 profit vanishes or DD expands above 30%(2024 수익이 사라지거나 DD가 30% 초과).",
            "materialization_note": "run267CR should preserve run267CO controls and change only period pressure surfaces.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cq_fb03_aggressive_shock_supply_expansion",
            "feature_family": "aggressive_shock_supply(공격형 충격 공급)",
            "market_meaning": "s264_aih aggressive shock-release의 PF는 좋지만 거래 수가 작으므로 공급을 늘리며 곡선이 버티는지 본다.",
            "candidate_scope": "s264_aih;s258_stc",
            "source_evidence": "s264_aih aggressive profile PF=1.722415 trades=219; s258_stc net=1775.7 but DD=31.52.",
            "changed_variables": "shock release width, reentry delay, impulse persistence, DD-shape guard",
            "similar_replacement_axis": "shock/impulse proxies replace a single indicator dependence(충격/임펄스 대체 지표로 단일 지표 의존 점검).",
            "aggressive_or_defensive": "aggressive(공격형)",
            "do_not_use_as": "defensive filter stacking(방어 필터 덧칠)",
            "success_read": "net remains strong, trades >= 300, PF >= 1.45, DD < 24%, weak slices do not deepen.",
            "failure_read": "PF stays high only because supply collapses or DD remains red-zone(공급 붕괴로 PF만 높거나 DD 고위험 유지).",
            "materialization_note": "run267CR should force at least one explosive variant instead of only more filters.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cq_fb04_buy_side_loss_shape_replacement",
            "feature_family": "directional_loss_shape(방향 손실 형태)",
            "market_meaning": "s264_aih buy side(매수 방향) 손실을 방향 금지가 아니라 entry lifecycle(진입 생명주기) 대체로 분해한다.",
            "candidate_scope": "s264_aih;s262_lih",
            "source_evidence": "s264_aih shared profile buy net=-156.13 and Monday net=-291.01.",
            "changed_variables": "entry lifecycle bucket, trend-persistence replacement, adverse excursion proxy",
            "similar_replacement_axis": "DI spread/ADX proxy to directional persistence replacement(DI 차이/ADX 대체).",
            "aggressive_or_defensive": "diagnostic(진단)",
            "do_not_use_as": "side ban or one-sided overconstraint(방향 금지/한쪽 과제약)",
            "success_read": "buy-side damage improves while long/short mix remains non-degenerate(매수 손상이 완화되고 방향 비율이 붕괴하지 않음).",
            "failure_read": "buy-side loss just moves to another month/session(매수 손실이 다른 월/세션으로 이동).",
            "materialization_note": "run267CR should include trace fields for direction and adverse excursion.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_id": "cq_fb05_validation_stress_guardrail_receipt",
            "feature_family": "guardrail_receipt(가드레일 영수증)",
            "market_meaning": "s262_lih와 s258_stc를 살리려는 감정 대신 validation/stress failure detector(검증/압박 실패 감지기)로 쓴다.",
            "candidate_scope": "s262_lih;s258_stc",
            "source_evidence": "s262_lih worst month floor=-138.46; s258_stc DD=31.52 and worst month=-218.65.",
            "changed_variables": "guardrail thresholds only as measurement receipt, not promotion gate",
            "similar_replacement_axis": "validation-heavy vs stress challenger role replacement(검증 중심/압박 도전자 역할 대체).",
            "aggressive_or_defensive": "guardrail(가드레일)",
            "do_not_use_as": "selection veto without evidence(근거 없는 선택 거부권)",
            "success_read": "new explosive queue names exactly where validation or stress candidate breaks.",
            "failure_read": "guardrail rows are ignored when headline net looks good.",
            "materialization_note": "run267CR should attach guardrail attempts or receipts to P0 variants.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_branch_decisions(candidate_rows: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped = group_by(candidate_rows, "candidate_alias")
    summary_by_alias = {str(row.get("candidate_alias")): row for row in summary_rows}
    decisions: list[dict[str, Any]] = []
    for alias in CANDIDATE_ORDER:
        rows = grouped.get(alias, [])
        summary = summary_by_alias.get(alias, {})
        if rows:
            best = best_profile_row(rows)
        else:
            best = summary
        candidate_id = str(best.get("candidate_id") or summary.get("candidate_id") or "")
        role = str(best.get("candidate_role") or summary.get("candidate_role") or "")
        net = as_float(best.get("net_profit") or summary.get("avg_net_profit"))
        pf = as_float(best.get("profit_factor") or summary.get("avg_profit_factor"))
        dd = as_float(best.get("report_equity_drawdown_percent") or summary.get("avg_equity_drawdown_percent"))
        trades = as_int(best.get("trade_count") or summary.get("avg_trade_count"))
        worst_month = str(best.get("worst_month") or "mixed")
        worst_month_net = as_float(best.get("worst_month_net") or summary.get("worst_month_floor"))
        weakest_weekday = str(best.get("weakest_weekday") or "Monday")
        weakest_weekday_net = as_float(best.get("weakest_weekday_net"))
        best_profile = str(best.get("test_id") or summary.get("best_test_id") or "summary_only")

        if alias == "s264_lc":
            label = "p0_defensive_control_pressure_no_selection(P0 방어 대조 압박, 선택 아님)"
            next_use = "cross_period_anchor_pressure_and_pool_control(확장 기간 앵커 압박과 후보군 대조)"
            why = "highest run267CP net with the lowest DD, but Monday and 2024-06 holes remain(최고 순수익과 최저 DD지만 월요일/2024-06 구멍이 남음)."
            risk = "do not call it baseline because 2024-only pressure and weak slices are unresolved(2024 단일 압박과 약한 구간 미해결)."
            reopen = "materialize cross-period and state-phase replacement; continue only if weak-slice floor improves."
        elif alias == "s264_aia":
            label = "p0_oos_anchor_dd_relief_watch(P0 OOS 앵커 DD 완화 관찰)"
            next_use = "anchor_cross_period_pressure_with_dd_relief(앵커 확장 기간 압박과 DD 완화)"
            why = "strong PF and net, but DD is close to uncomfortable range(강한 PF/순수익이지만 DD가 불편한 범위에 가까움)."
            risk = "OOS anchor only; not a selected candidate(OOS 앵커 관찰 전용, 선택 후보 아님)."
            reopen = "continue if adjacent periods do not deepen 2024-06 style weakness."
        elif alias == "s264_aih":
            label = "p0_aggressive_core_reentry_supply_expansion(P0 공격형 핵심 재진입 공급 확장)"
            next_use = "explosive_shock_release_reentry_v2(폭발형 충격 해소 재진입 v2)"
            why = "core challenger still has constructive profiles; aggressive PF is high but supply is thin(핵심 도전자는 단서가 있고 공격형 PF는 높지만 공급이 얇음)."
            risk = "do not hide low trade count behind PF(PF 뒤에 낮은 거래 수를 숨기지 않음)."
            reopen = "require trades >= 300 and weaker Monday/2024-12 damage before any stronger claim."
        elif alias == "s262_lih":
            label = "p1_validation_heavy_guardrail_keep(P1 검증 중심 가드레일 유지)"
            next_use = "validation_damage_detector_for_new_features(새 피처 검증 손상 감지기)"
            why = "worst month floor is less bad than others but net/PF are not leading(최악 월 바닥은 덜 나쁘지만 순수익/PF는 선두가 아님)."
            risk = "do not overfit validation-heavy role into a standalone selection(검증 중심 역할을 단독 선택으로 과적합 금지)."
            reopen = "use as guardrail when P0 variants are materialized."
        else:
            label = "p1_redzone_stress_blast_or_prune(P1 고위험 압박 폭발 또는 가지치기)"
            next_use = "stress_challenger_redzone_receipt(압박 도전자 고위험 영수증)"
            why = "net is high, but DD above 30% and weak months are uncomfortable(순수익은 높지만 DD 30% 초과와 약한 월이 불편)."
            risk = "do not deep-repair for more than one next branch(다음 한 분기 이상 깊은 수리 금지)."
            reopen = "only keep if aggressive variant lowers DD without killing net/trade supply."

        decisions.append(
            {
                "decision_id": f"cq_decision_{alias}",
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": role,
                "best_profile": best_profile,
                "best_net_profit": net,
                "best_profit_factor": pf,
                "best_equity_drawdown_percent": dd,
                "best_trade_count": trades,
                "worst_month": worst_month,
                "worst_month_net": worst_month_net,
                "weakest_weekday": weakest_weekday,
                "weakest_weekday_net": weakest_weekday_net,
                "decision_label": label,
                "next_use": next_use,
                "why": why,
                "risk_boundary": risk,
                "reopen_condition": reopen,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return decisions


def materialization_queue() -> list[dict[str, Any]]:
    common_controls = (
        "symbol=US100;timeframe=M5;broker=FPMarkets;deposit=500;"
        "run267CO MT5 cost/model settings;candidate model identity unchanged unless queue says feature replacement"
    )
    sample_scope = "historical_2024 first, then adjacent periods 2023H2/2025H1/2025H2 when materialized"
    return [
        {
            "queue_id": "run267cr_q01_pool_monday_state_phase_replacement",
            "priority": "P0",
            "workstream": "pool_wide_shared_weakness_state_phase(후보군 전체 공유 약점 상태 국면)",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia;s258_stc",
            "feature_blueprint_scope": "cq_fb01_state_phase_monday_replacement;cq_fb05_validation_stress_guardrail_receipt",
            "hypothesis": "The Monday loss cluster is a hidden market-state cluster, not a weekday permission rule(월요일 손실은 요일 규칙이 아니라 숨은 시장 상태 군집이다).",
            "decision_use": "decide whether shared weakness breakout deserves one more MT5 batch or should be pruned",
            "comparison_baseline": "run267CP candidate profile and negative-slice summary",
            "control_variables": common_controls,
            "changed_variables": "state phase interaction;ATR percentile slope;trend persistence bucket;loss-shape cooldown",
            "sample_scope": sample_scope,
            "success_criteria": "Monday net improves >=30%; worst month floor improves; trades stay >=300 for broad candidates; DD does not exceed run267CP row by >3pp.",
            "failure_criteria": "weak slice moves to another month/session or trade supply collapses below 220.",
            "invalid_conditions": "changed cost settings, missing trade list, parser errors, or non-comparable report identity.",
            "stop_conditions": "if every candidate keeps deep Monday loss, prune literal shared-state repair and pivot to cross-period/Adapter audit.",
            "evidence_plan": "feature manifest;attempt manifest;MT5 report;trade_records;time_slice_kpi;curve_diagnostics;guardrail receipts",
            "materialization_instruction": "Build one pool-wide feature replacement variant and attach s262_lih/s258_stc guardrail receipts.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cr_q02_lc_aia_anchor_cross_period_pressure",
            "priority": "P0",
            "workstream": "anchor_cross_period_pressure(앵커 확장 기간 압박)",
            "candidate_aliases": "s264_lc;s264_aia",
            "feature_blueprint_scope": "cq_fb02_anchor_cross_period_pressure",
            "hypothesis": "s264_lc low-DD supply and s264_aia OOS anchor clue survive adjacent periods without a new month hole.",
            "decision_use": "decide whether these remain research controls or are pruned from main racing pressure",
            "comparison_baseline": "run267CP s264_lc/s264_aia shared_state rows",
            "control_variables": common_controls,
            "changed_variables": "period pack only: 2023H2, 2025H1, 2025H2; no threshold polish",
            "sample_scope": "Tier A and duplicate-boundary Tier A+B adjacent-period pressure; true fallback not claimed",
            "success_criteria": "PF >=1.25, DD <25 for s264_lc and <30 for s264_aia, trade count useful, no single period dominates profit.",
            "failure_criteria": "2024 edge disappears, DD rises above 30, or one adjacent period is deeply negative.",
            "invalid_conditions": "period data missing, report overwrite, route manifest gap treated as true fallback.",
            "stop_conditions": "drop from P0 if two adjacent periods fail; keep only as failure memory or guardrail.",
            "evidence_plan": "period materialization manifests;MT5 reports;balance/time-slice review;artifact hashes",
            "materialization_instruction": "Materialize period-only pressure rows before adding any new filters.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cr_q03_aih_aggressive_shock_supply_expansion",
            "priority": "P0",
            "workstream": "aggressive_explosive_reentry(공격형 폭발 재진입)",
            "candidate_aliases": "s264_aih",
            "feature_blueprint_scope": "cq_fb03_aggressive_shock_supply_expansion;cq_fb04_buy_side_loss_shape_replacement",
            "hypothesis": "s264_aih can keep high PF while expanding trade supply if shock/reentry and buy-side loss shape are replaced together.",
            "decision_use": "decide whether core challenger deserves Adapter branch later or should be demoted",
            "comparison_baseline": "run267CP s264_aih shared_state and aggressive_shock_release_reentry rows",
            "control_variables": common_controls,
            "changed_variables": "shock release width;reentry delay;impulse persistence;buy-side adverse excursion proxy",
            "sample_scope": sample_scope,
            "success_criteria": "net >1100; PF >=1.45; trades >=300; DD <24; Monday > -180; 2024-12 > -150.",
            "failure_criteria": "PF remains high only with trades <260 or DD/worst month stays uncomfortable.",
            "invalid_conditions": "direction labels missing, report list malformed, or source feature order changed without receipt.",
            "stop_conditions": "one aggressive follow-up only; if supply/DD does not improve, prune deep repair loop.",
            "evidence_plan": "feature order receipt;attempt manifest;MT5 report;direction slice;balance/time-slice review",
            "materialization_instruction": "Force one explosive variant; avoid another purely defensive filter.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cr_q04_stc_redzone_stress_blast",
            "priority": "P1",
            "workstream": "redzone_stress_challenger(고위험 압박 도전자)",
            "candidate_aliases": "s258_stc",
            "feature_blueprint_scope": "cq_fb03_aggressive_shock_supply_expansion;cq_fb05_validation_stress_guardrail_receipt",
            "hypothesis": "s258_stc is either a useful stress challenger or should be pruned quickly because DD is already red-zone.",
            "decision_use": "decide keep-as-stress or prune-after-one-branch",
            "comparison_baseline": "run267CP s258_stc shared_state row",
            "control_variables": common_controls,
            "changed_variables": "loss-shape DD relief;impulse persistence;stress risk receipt",
            "sample_scope": "historical_2024 red-zone stress branch only",
            "success_criteria": "net >1500; PF >=1.4; DD <28; worst month > -190.",
            "failure_criteria": "DD remains >=30 or worst month <= -220 after one follow-up.",
            "invalid_conditions": "cost drift or missing DD evidence.",
            "stop_conditions": "do not continue a third repair stage; prune if red-zone remains.",
            "evidence_plan": "MT5 report;DD curve;negative_slice_summary;failure_memory update",
            "materialization_instruction": "Materialize only one stress blast row, not a long repair branch.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cr_q05_lih_validation_guardrail_trace",
            "priority": "P1",
            "workstream": "validation_heavy_guardrail(검증 중심 가드레일)",
            "candidate_aliases": "s262_lih",
            "feature_blueprint_scope": "cq_fb04_buy_side_loss_shape_replacement;cq_fb05_validation_stress_guardrail_receipt",
            "hypothesis": "s262_lih can reveal whether new state/impulse features damage validation-style stability.",
            "decision_use": "guardrail check for P0 variants, not selected candidate",
            "comparison_baseline": "run267CP s262_lih shared_state row",
            "control_variables": common_controls,
            "changed_variables": "validation guardrail receipt;directional loss-shape trace",
            "sample_scope": sample_scope,
            "success_criteria": "new queue does not worsen s262_lih worst month floor or DD by more than 3pp.",
            "failure_criteria": "validation-heavy profile breaks while headline candidates improve.",
            "invalid_conditions": "guardrail row omitted or synthetic combined result mislabeled.",
            "stop_conditions": "downgrade any P0 variant that passes only by breaking validation guardrail.",
            "evidence_plan": "guardrail receipt;candidate profile review;negative slices;curve review",
            "materialization_instruction": "Attach as guardrail attempt or receipt next to P0 rows.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cr_q06_buy_side_similar_replacement_probe",
            "priority": "P2",
            "workstream": "similar_feature_replacement(유사 피처 대체)",
            "candidate_aliases": "s264_aih;s262_lih",
            "feature_blueprint_scope": "cq_fb04_buy_side_loss_shape_replacement",
            "hypothesis": "The buy-side weakness is feature meaning dependent, not a single indicator accident.",
            "decision_use": "decide whether buy-side replacement merits wider Adapter design later",
            "comparison_baseline": "run267CP direction slices and s264_aih buy-side damage",
            "control_variables": common_controls,
            "changed_variables": "replace direction-strength feature with trend persistence/adverse excursion proxies",
            "sample_scope": "historical_2024 diagnostic, optionally adjacent period after P0",
            "success_criteria": "buy-side net improves without side ban and without reducing trades below 280.",
            "failure_criteria": "loss transfers to short side, session, or a single weak month.",
            "invalid_conditions": "direction attribution unavailable or feature order receipt missing.",
            "stop_conditions": "if replacement only acts like a hidden side filter, prune.",
            "evidence_plan": "feature replacement receipt;direction time-slice;trade quality;curve diagnostics",
            "materialization_instruction": "Keep as diagnostic unless P0 fails to explain direction damage.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "cq_prune_01_no_literal_calendar_filter",
            "prune_label": "no_literal_calendar_filter(달력 직접 필터 금지)",
            "affected_scope": "Monday;2024-06;2024-07;2024-12",
            "why_pruned": "run267CP uses calendar buckets for attribution only; a calendar-off rule would overfit.",
            "reopen_condition": "Only reopen as a state feature if non-calendar variables explain the same cluster.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cq_prune_02_no_s258_stc_long_repair",
            "prune_label": "no_s258_stc_long_repair(s258_stc 장기 수리 금지)",
            "affected_scope": "s258_stc stress challenger",
            "why_pruned": "DD 31.52 and worst month -218.65 make it a stress receipt, not a long repair branch.",
            "reopen_condition": "One red-zone stress blast lowers DD below 28 while keeping net >1500.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cq_prune_03_no_pf_only_aih_selection",
            "prune_label": "no_pf_only_s264_aih_selection(PF 단독 s264_aih 선택 금지)",
            "affected_scope": "s264_aih aggressive shock-release",
            "why_pruned": "PF 1.72 is attractive but trades 219 and net 612.76 are too thin.",
            "reopen_condition": "Supply expands to trades >=300 with DD <24 and weak-month relief.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "prune_id": "cq_prune_04_no_baseline_claim_from_2024",
            "prune_label": "no_baseline_claim_from_2024(2024 단독 기준 후보 주장 금지)",
            "affected_scope": "all run267CP rows",
            "why_pruned": "Current evidence is historical 2024 pressure with duplicate-boundary Tier A+B, not full R&D survivor proof.",
            "reopen_condition": "Cross-period, ablation/replacement, Adapter, runtime reproduction, and ONNX parity evidence are all present.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    monday_aliases = sorted({str(row.get("candidate_alias")) for row in negative_rows if row.get("axis") == "weekday" and row.get("bucket") == "Monday"})
    june_aliases = sorted({str(row.get("candidate_alias")) for row in negative_rows if row.get("axis") == "month" and row.get("bucket") == "2024-06"})
    december_aliases = sorted({str(row.get("candidate_alias")) for row in negative_rows if row.get("axis") == "month" and row.get("bucket") == "2024-12"})
    return [
        {
            "memory_id": "cq_memory_01_monday_cluster",
            "pattern": "shared_monday_loss_cluster(공유 월요일 손실 군집)",
            "affected_scope": ";".join(monday_aliases),
            "evidence": "run267CP negative_slice_summary Monday rows across candidate pool",
            "why_fragile": "headline net hides a repeated weekday/state weakness.",
            "do_not_repeat": "do not add Monday-off filter; build state-phase replacement instead.",
            "salvage_angle": "state phase, volatility slope, trend persistence, loss-shape cooldown",
            "reopen_condition": "state variables reduce Monday damage without moving loss elsewhere.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cq_memory_02_june_july_december_split",
            "pattern": "month_hole_split(월별 구멍 분기)",
            "affected_scope": f"2024-06:{';'.join(june_aliases)}|2024-12:{';'.join(december_aliases)}",
            "evidence": "s264_lc/s264_aia/s258_stc weak June/July; s264_aih/s262_lih weak December",
            "why_fragile": "different candidates fail in different month regimes, so one repair knob is unlikely to generalize.",
            "do_not_repeat": "do not tune one month threshold.",
            "salvage_angle": "cross-period pressure and state regime split",
            "reopen_condition": "candidate-specific month holes improve under adjacent-period pressure.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cq_memory_03_aggressive_supply_gap",
            "pattern": "high_pf_thin_supply(높은 PF 얇은 공급)",
            "affected_scope": "s264_aih aggressive_shock_release_reentry",
            "evidence": "PF=1.722415 but trades=219 and net=612.76",
            "why_fragile": "small supply can make PF look cleaner than the underlying curve.",
            "do_not_repeat": "do not select an aggressive profile from PF alone.",
            "salvage_angle": "shock supply expansion with direction loss-shape trace",
            "reopen_condition": "trades >=300, net >1100, DD <24, weak-month relief.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "cq_memory_04_duplicate_boundary",
            "pattern": "duplicate_boundary_not_true_fallback(중복 경계, 실제 대체 아님)",
            "affected_scope": "run267CO/run267CP evidence boundary",
            "evidence": "Tier A and duplicate-boundary Tier A+B materialized; true fallback remains outside claim.",
            "why_fragile": "fallback effect cannot be inferred from duplicate-boundary rows.",
            "do_not_repeat": "do not call duplicate-boundary rows actual routed total.",
            "salvage_angle": "route manifest repair or explicitly bounded Tier A pressure",
            "reopen_condition": "true fallback manifest and routed output exist.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def performance_attribution(
    candidate_rows: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    summary = {str(row.get("candidate_alias")): row for row in summary_rows}
    negatives = group_by(negative_rows, "candidate_alias")
    output: list[dict[str, Any]] = []
    for alias in CANDIDATE_ORDER:
        row = summary.get(alias, {})
        negs = negatives.get(alias, [])
        top_negs = sorted(negs, key=lambda item: as_float(item.get("net_profit")))[:3]
        rows = [item for item in candidate_rows if item.get("candidate_alias") == alias]
        avg_pf = as_float(row.get("avg_profit_factor"))
        avg_dd = as_float(row.get("avg_equity_drawdown_percent"))
        avg_trades = as_float(row.get("avg_trade_count"))
        observed = f"avg_net={row.get('avg_net_profit')};avg_pf={avg_pf};avg_dd={avg_dd};avg_trades={avg_trades}"
        segment = ";".join(f"{item.get('axis')}={item.get('bucket')}:{item.get('net_profit')}" for item in top_negs)
        output.append(
            {
                "attribution_id": f"cq_attr_{alias}",
                "observed_change": observed,
                "comparison_baseline": "run267CP candidate summary and profile review",
                "likely_drivers": f"profile_count={len(rows)};negative_slice_count={len(negs)};candidate_read={row.get('candidate_read')}",
                "segment_checks": segment,
                "trade_shape": f"avg_trades={avg_trades};worst_month_floor={row.get('worst_month_floor')}",
                "alternative_explanations": "2024-only pressure;duplicate-boundary Tier A+B;feature overfit;broker-history cost shape",
                "attribution_confidence": "medium_low(중간-낮음)",
                "next_probe": NEXT_ACTION,
            }
        )
    return output


def experiment_design_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": str(row["queue_id"]),
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
            "receipt_id": "cq_data_integrity_run267cp_source",
            "data_source": f"{rel(SOURCE_REVIEW_RESULT_PATH)};{rel(SOURCE_CANDIDATE_PROFILE_PATH)};{rel(SOURCE_NEGATIVE_SLICE_PATH)}",
            "time_axis": "MT5 report trade open/close times, report-time weekday/hour/session buckets; US100 M5 research context",
            "sample_scope": "historical_2024;Tier A and duplicate-boundary Tier A+B;true Tier B fallback not claimed",
            "missing_or_duplicate_check": f"parser_errors={len(source_result.get('parser_errors', []))};trade_records={source_result.get('trade_record_count')};negative_slices={len(source_result.get('negative_slices', []))}",
            "feature_label_boundary": "design-only; no new feature or label value is computed in run267CQ",
            "split_boundary": "run267CP review source only; future run267CR must materialize new attempts before KPI claims",
            "leakage_risk": "selection bias from designing around 2024 weak slices; mitigated by cross-period queue and no selection claim",
            "data_hash_or_identity": f"source_review_sha256={sha256_file_lf_normalized(SOURCE_REVIEW_RESULT_PATH)}",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        }
    ]


def model_validation_receipts() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "cq_model_validation_design_only",
            "model_family": "baseline candidate bundles from run267CO; no new trained model in run267CQ",
            "target_and_label": "unchanged from source candidate artifacts; no relabeling in this design run",
            "split_method": "historical_2024 review-derived design with planned adjacent-period pressure",
            "selection_metric": "no selection metric; queue uses net/PF/DD/trade_count/weak-slice criteria for next evidence",
            "secondary_metrics": "worst month, Monday net, direction slice, trade count, DD, parser/report identity",
            "threshold_policy": "no threshold selected; any future threshold must be materialized and reviewed",
            "overfit_risk": "high if 2024 weak slices are repaired literally; mitigated by state-phase and cross-period requirements",
            "calibration_risk": "candidate scores are not probability claims; only ranking/trade-shape evidence is used",
            "comparison_baseline": "run267CP candidate profile and summary",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
        }
    ]


def result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CQ shared weakness breakout follow-up/prune design(267CQ 공유 약점 돌파 후속/가지치기 설계)",
            "evidence_available": "run267CP review_result, candidate profile, candidate summary, negative slices, performance attribution",
            "evidence_missing": "run267CR materialization, MT5 execution, balance/time-slice review, Adapter package, runtime reproduction, ONNX parity",
            "judgment_label": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 단계는 후보를 뽑는 것이 아니라 다음 실험 큐를 넓히고 깊은 수리 루프를 끊는 단계다.",
        }
    ]


def gate_audit(queue_rows: Sequence[Mapping[str, Any]], prune_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "work_packet_schema_lint",
            "status": "passed(통과)",
            "evidence": f"queue_rows={len(queue_rows)};prune_rows={len(prune_rows)};receipts include experiment/data/model/judgment",
            "effect": "experiment_design primary family has explicit hypothesis, controls, criteria, and evidence plan.",
        },
        {
            "gate_id": "anti_overfit_claim_boundary",
            "status": "passed(통과)",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed",
            "effect": "prevents 2024-only or headline-profit baseline closure.",
        },
        {
            "gate_id": "aggressive_experiment_requirement",
            "status": "passed(통과)",
            "evidence": "run267cr_q03_aih_aggressive_shock_supply_expansion and run267cr_q04_stc_redzone_stress_blast",
            "effect": "keeps the pipeline from becoming only defensive filter stacking.",
        },
    ]


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = [
        ("stage267_run267CQ_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Run267CQ feature blueprint."),
        ("stage267_run267CQ_branch_decisions", "branch_decisions", BRANCH_DECISION_PATH, "Run267CQ branch decisions."),
        ("stage267_run267CQ_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267CQ next materialization queue."),
        ("stage267_run267CQ_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, "Run267CQ prune matrix."),
        ("stage267_run267CQ_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267CQ failure memory."),
        ("stage267_run267CQ_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267CQ performance attribution."),
        ("stage267_run267CQ_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267CQ experiment design receipt."),
        ("stage267_run267CQ_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267CQ data integrity receipt."),
        ("stage267_run267CQ_model_validation_receipt", "model_validation_receipt", MODEL_VALIDATION_RECEIPT_PATH, "Run267CQ model validation receipt."),
        ("stage267_run267CQ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CQ result judgment."),
        ("stage267_run267CQ_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CQ gate audit."),
        ("stage267_run267CQ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CQ run manifest."),
        ("stage267_run267CQ_lineage", "lineage", LINEAGE_PATH, "Run267CQ lineage."),
        ("stage267_run267CQ_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CQ review JSON."),
        ("stage267_run267CQ_report", "review_report", REPORT_PATH, "Run267CQ user-facing report."),
    ]
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in artifacts
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    decisions = list(result["branch_decisions"])
    queue = list(result["materialization_queue"])
    prune = list(result["prune_matrix"])
    memory = list(result["failure_memory"])
    attribution = list(result["performance_attribution"])

    lines: list[str] = [
        "# Stage267 Run267CQ Shared Weakness Breakout Follow-Up/Prune Design(267단계 267CQ 공유 약점 돌파 후속/가지치기 설계)",
        "",
        "- action(행동): run267CP(267CP 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 branch decision(분기 판단), materialization queue(물질화 대기열), prune matrix(가지치기 행렬)로 바꿨다.",
        "- effect(효과): 후보를 성급히 고르지 않고, `s264_lc`의 안정 단서, `s264_aih`의 공격형 단서, `s258_stc`의 고위험 단서를 다음 실행 가능한 실험으로 분리한다.",
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
        "run267CP(267CP 실행)는 baseline 후보군이 모두 한 번씩 좋아 보이는 구석이 있지만, 월요일과 특정 월에서 반복적으로 파인다는 것을 보여줬다. 그래서 run267CQ(267CQ 실행)는 후보를 뽑지 않는다.",
        "",
        "이번 설계의 핵심은 세 갈래다. 첫째, `s264_lc`와 `s264_aia`는 cross-period pressure(확장 기간 압박)로 정말 덜 깨지는지 본다. 둘째, `s264_aih`는 방어 필터만 붙이지 않고 aggressive shock supply expansion(공격형 충격 공급 확장)으로 강하게 다시 밀어본다. 셋째, `s258_stc`는 한 번만 red-zone stress blast(고위험 압박 폭발)를 허용하고 실패하면 깊은 수리를 끊는다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | role(역할) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) | decision(판단) | next use(다음 용도) |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in decisions:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['candidate_role']} | `{row['best_profile']}` | "
            f"{row['best_net_profit']} | {row['best_profit_factor']} | {row['best_equity_drawdown_percent']} | "
            f"{row['decision_label']} | {row['next_use']} |"
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
    for row in queue:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | "
            f"{row['workstream']} | {row['success_criteria']} |"
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
    for row in prune:
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
    for row in memory:
        lines.append(f"| `{row['memory_id']}` | {row['pattern']} | {row['affected_scope']} | {row['do_not_repeat']} |")

    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀속)",
            "",
        ]
    )
    for row in attribution:
        lines.append(f"- `{row['attribution_id']}`: {row['observed_change']}; segment_checks(구간 점검): {row['segment_checks']}.")

    lines.extend(
        [
            "",
            "## Required Receipts(필수 영수증)",
            "",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- data_integrity_receipt(데이터 무결성 영수증): `{rel(DATA_INTEGRITY_RECEIPT_PATH)}`",
            f"- model_validation_receipt(모델 검증 영수증): `{rel(MODEL_VALIDATION_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
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
            f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267CQ_shared_weakness_breakout_followup_or_prune_design`.",
            "- judgment_label(판정 라벨): `exploratory_design_only(탐색 설계 전용)`.",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
        ]
    )
    return "\n".join(lines)


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
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
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
        "row_id": "stage267_run267CQ_shared_weakness_breakout_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_followup_or_prune_design",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B run267CP review-derived design; true Tier B fallback not claimed",
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
        "lane": "baseline_candidate_racing_shared_weakness_breakout_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_followup_or_prune_design",
        "tier_scope": "Tier A run267CP design; Tier B fallback remains outside claim",
        "kpi_scope": "experiment_design_feature_blueprint_queue_failure_memory",
        "scoreboard_lane": "shared_weakness_breakout_followup_design",
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


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267CQ_shared_weakness_breakout_followup_or_prune_design"
        f"(267CQ 공유 약점 돌파 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267CQ_summary(267CQ 요약): run267CP(267CP 실행)의 약한 구간을 "
        f"feature blueprint(피처 청사진) `{result['feature_blueprint_count']}`개, "
        f"materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개, "
        f"prune rows(가지치기 행) `{result['prune_count']}`개로 바꿨다. "
        "Effect(효과): s264_lc/s264_aia는 확장 기간 압박, s264_aih는 공격형 공급 확장, s258_stc는 한 번의 고위험 압박으로 분리한다."
    )
    block = "\n".join(
        [
            "Run267CQ(267CQ 실행)는 run267CP(267CP 실행)의 후보 선택 보류 상태를 다음 실험 설계로 바꿨다.",
            f"Effect(효과): queue(대기열) `{result['materialization_queue_count']}`개 중 P0에는 pool-wide state phase replacement(후보군 전체 상태 국면 대체), lc/aia cross-period pressure(확장 기간 압박), aih aggressive supply expansion(공격형 공급 확장)을 둔다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_followup_or_prune_design`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "run267CQ_shared_weakness_breakout_followup_or_prune_design", summary_line)
            text = append_block_once(text, "Run267CQ(267CQ 실행)는 run267CP", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review", report_line)
            text = append_block_once(text, "Run267CQ(267CQ 실행)는 run267CP", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review", report_line)
            text = append_block_once(text, "Run267CQ(267CQ 실행)는 run267CP", block)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CQ(267CQ 실행) shared weakness breakout follow-up/prune design"
        f"(공유 약점 돌파 후속/가지치기 설계) `{STATUS}`. Effect(효과): run267CP(267CP 실행)의 Monday(월요일), "
        "2024-06/2024-07/2024-12(월별 구멍), s264_aih aggressive thin supply(공격형 얇은 공급)를 "
        f"materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개와 prune matrix(가지치기 행렬) `{result['prune_count']}`개로 바꿨고, "
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
        "run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review_report_path",
        f"  run267CQ_shared_weakness_breakout_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_PROFILE_PATH)
    summary_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    features = feature_blueprints()
    decisions = make_branch_decisions(candidate_rows, summary_rows)
    queue_rows = materialization_queue()
    prune_rows = prune_matrix()
    failure_rows = failure_memory(negative_rows)
    attribution_rows = performance_attribution(candidate_rows, summary_rows, negative_rows)
    design_rows = experiment_design_receipts(queue_rows)
    data_rows = data_integrity_receipts(source_result)
    model_rows = model_validation_receipts()
    judgment_rows = result_judgment()
    gates = gate_audit(queue_rows, prune_rows)
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
    return {
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
        "performance_attribution": attribution_rows,
        "experiment_design_receipt": design_rows,
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
            "run267CP_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267CP_candidate_profile": rel(SOURCE_CANDIDATE_PROFILE_PATH),
            "run267CP_candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "run267CP_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "run267CP_attribution": rel(SOURCE_ATTRIBUTION_PATH),
            "run267CP_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": outputs,
    }


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
