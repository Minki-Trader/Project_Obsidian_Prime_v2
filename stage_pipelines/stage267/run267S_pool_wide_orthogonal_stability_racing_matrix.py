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
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_NUMBER = "run267S"
RUN_ID = "run267S_stage267_pool_wide_orthogonal_stability_racing_matrix_v1"
PARENT_RUN_ID = "run267R_stage267_internal_adapter_stability_followup_or_prune_v1"
STATUS = "run267S_pool_wide_orthogonal_stability_racing_matrix_materialized"
NEXT_ACTION = "run267T_build_pool_wide_orthogonal_stability_mt5_attempts"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_stability_racing_matrix"

BASELINE_POOL_PATH = STAGE_ROOT / "01_inputs" / "baseline_candidate_pool.csv"
RUN267R_ROOT = STAGE_ROOT / "02_runs" / "run267R" / "internal_adapter_stability_followup_or_prune"
RUN267R_QUEUE_PATH = RUN267R_ROOT / "next_pool_wide_stability_queue.csv"
RUN267R_PRUNE_PATH = RUN267R_ROOT / "internal_adapter_prune_matrix.csv"
RUN267R_FAILURE_PATH = RUN267R_ROOT / "failure_memory.csv"
RUN267R_RESULT_PATH = RUN267R_ROOT / "result.json"
RUN267R_REPORT_PATH = REVIEWS_ROOT / "stage267_run267R_internal_adapter_stability_followup_or_prune.md"

RUN267O_ROOT = STAGE_ROOT / "02_runs" / "run267O" / "pool_wide_balance_timeslice_trade_quality_review"
RUN267O_CANDIDATE_SUMMARY_PATH = RUN267O_ROOT / "candidate_balance_timeslice_summary.csv"
RUN267O_TEST_REVIEW_PATH = RUN267O_ROOT / "candidate_test_review.csv"
RUN267O_NEGATIVE_SLICE_PATH = RUN267O_ROOT / "negative_slice_summary.csv"
RUN267O_CURVE_DIAGNOSTICS_PATH = RUN267O_ROOT / "curve_diagnostics.csv"

RUN267P_ROOT = STAGE_ROOT / "02_runs" / "run267P" / "pool_wide_internal_feature_order_confirmation_and_adapter_design"
RUN267P_DECISION_PATH = RUN267P_ROOT / "candidate_axis_decision.csv"
RUN267P_QUEUE_PATH = RUN267P_ROOT / "adapter_design_queue.csv"
RUN267P_FAILURE_PATH = RUN267P_ROOT / "failure_memory.csv"

PRIOR_AUDIT_PATH = REVIEWS_ROOT / "stage267_prior_research_utilization_audit.md"

CANDIDATE_SCOPE_PATH = RUN_ROOT / "candidate_scope_update.csv"
ORTHOGONAL_MATRIX_PATH = RUN_ROOT / "orthogonal_stability_matrix.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
FAILURE_MEMORY_LINK_PATH = RUN_ROOT / "failure_memory_link.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
GATE_RECEIPT_PATH = RUN_ROOT / "gate_receipt.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267S_pool_wide_orthogonal_stability_racing_matrix.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267S_pool_wide_orthogonal_stability_racing_matrix.py")

STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

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

ALIAS_BY_ID = {
    "s264_allow_inner_high_quarter": "s264_aih",
    "s264_lowrank_control": "s264_lc",
    "s262_lowrank_inner_half_filter": "s262_lih",
    "s264_allow_inner_all_oos_anchor": "s264_aia",
    "s258_short_tight_control": "s258_stc",
}
ROLE_BY_ID = {
    "s264_allow_inner_high_quarter": "challenger_core",
    "s264_lowrank_control": "defensive_control",
    "s262_lowrank_inner_half_filter": "validation_heavy",
    "s264_allow_inner_all_oos_anchor": "oos_anchor",
    "s258_short_tight_control": "stress_challenger",
}
ROLE_READ_BY_ID = {
    "s264_allow_inner_high_quarter": "core challenger(핵심 도전자)",
    "s264_lowrank_control": "defensive control(방어 통제)",
    "s262_lowrank_inner_half_filter": "validation-heavy(검증 중심)",
    "s264_allow_inner_all_oos_anchor": "OOS anchor(표본외 앵커)",
    "s258_short_tight_control": "stress challenger(압박 도전자)",
}


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
        return int(float(value))
    except (TypeError, ValueError):
        return default


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def require_inputs() -> None:
    required = (
        BASELINE_POOL_PATH,
        RUN267R_QUEUE_PATH,
        RUN267R_PRUNE_PATH,
        RUN267R_FAILURE_PATH,
        RUN267R_RESULT_PATH,
        RUN267O_CANDIDATE_SUMMARY_PATH,
        RUN267O_TEST_REVIEW_PATH,
        RUN267O_NEGATIVE_SLICE_PATH,
        RUN267O_CURVE_DIAGNOSTICS_PATH,
        RUN267P_DECISION_PATH,
        RUN267P_QUEUE_PATH,
        PRIOR_AUDIT_PATH,
    )
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required run267S inputs: " + ";".join(missing))


def rows_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")).strip(): row for row in rows if str(row.get(key, "")).strip()}


def rows_by_alias(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return rows_by(rows, "candidate_alias")


def candidate_rows() -> list[dict[str, Any]]:
    pool_rows = read_csv_rows(BASELINE_POOL_PATH)
    summary_by_alias = rows_by_alias(read_csv_rows(RUN267O_CANDIDATE_SUMMARY_PATH))
    decision_by_alias = rows_by_alias(read_csv_rows(RUN267P_DECISION_PATH))
    prune_by_alias = rows_by_alias(read_csv_rows(RUN267R_PRUNE_PATH))
    candidates: list[dict[str, Any]] = []
    for order, row in enumerate(pool_rows, start=1):
        candidate_id = row["candidate_id"]
        alias = ALIAS_BY_ID[candidate_id]
        summary = summary_by_alias.get(alias, {})
        decision = decision_by_alias.get(alias, {})
        prune = prune_by_alias.get(alias, {})
        internal_status = "not_in_run267R_internal_branch_restore_to_pool"
        if prune:
            internal_status = "run267R_internal_branch_pruned_to_salvage_clue"
        candidates.append(
            {
                "candidate_order": order,
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": ROLE_BY_ID[candidate_id],
                "candidate_role_read": ROLE_READ_BY_ID[candidate_id],
                "source_stage": row.get("source_stage", ""),
                "source_run": row.get("source_run", ""),
                "initial_racing_use": row.get("initial_racing_use", ""),
                "known_strength": row.get("known_strength", ""),
                "known_risk": row.get("known_risk", ""),
                "run267O_candidate_read": summary.get("candidate_read", "missing_required"),
                "run267O_best_test": summary.get("best_test_id", ""),
                "run267O_best_net_profit": as_float(summary.get("best_net_profit")),
                "run267O_best_profit_factor": as_float(summary.get("best_profit_factor")),
                "run267O_worst_month_floor": as_float(summary.get("worst_month_floor")),
                "run267P_candidate_decision": decision.get("candidate_decision", "missing_required"),
                "run267P_p0_tests": decision.get("p0_tests", ""),
                "run267P_p1_tests": decision.get("p1_tests", ""),
                "run267P_failure_rows": as_int(decision.get("failure_rows")),
                "run267R_internal_status": internal_status,
                "run267R_monday_net": as_float(prune.get("monday_net")),
                "run267R_session_07_12_net": as_float(prune.get("session_07_12_net")),
                "pool_decision": "retain_for_run267S_matrix_no_selection",
                "pool_decision_reason": pool_reason(candidate_id, prune, decision),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return candidates


def pool_reason(candidate_id: str, prune: Mapping[str, str], decision: Mapping[str, str]) -> str:
    if prune:
        return (
            "run267R(267R 실행)에서 내부 Adapter(어댑터) 단독 분기는 가지치기됐지만 "
            "후보 자체는 직교 안정성 경주에 남긴다."
        )
    failure_rows = as_int(decision.get("failure_rows"))
    if failure_rows:
        return (
            "run267P(267P 실행)에서 실패 기억이 있어 방어적으로 남기되, "
            "다음 비교에서는 같은 축으로 다시 본다."
        )
    if candidate_id == "s258_short_tight_control":
        return "stress challenger(압박 도전자)로 남겨 강한 숫자가 더 넓은 조건에서 버티는지 본다."
    return "run267Q(267Q 실행)에서 빠진 후보를 같은 안정성 축에 복귀시켜 후보군 비교 공백을 줄인다."


def axis_class(queue_id: str) -> str:
    if "variant_distinguishability" in queue_id:
        return "variant_distinguishability(변형 구분성)"
    if "weak_slice_resilience" in queue_id:
        return "non_calendar_weak_slice_resilience(비달력 약점 구간 견고성)"
    if "prune_or_restore" in queue_id:
        return "candidate_pool_prune_or_restore(후보군 가지치기 또는 복귀)"
    return "orthogonal_stability_axis(직교 안정성 축)"


def required_action_for(queue_id: str) -> str:
    if "variant_distinguishability" in queue_id:
        return (
            "ablation/replacement(제거/대체) 결과가 같은 KPI shape(핵심 성과 지표 모양)으로 "
            "접히는지 후보별로 다시 물질화한다."
        )
    if "weak_slice_resilience" in queue_id:
        return (
            "weekday/session(요일/세션)을 직접 맞추지 않고 volatility/trend/risk "
            "(변동성/추세/위험) 구조 feature(피처)로 약한 구간을 줄이는지 본다."
        )
    if "prune_or_restore" in queue_id:
        return "다섯 후보 유지/탈락/회수 조건을 같은 evidence(근거) 단위로 갱신한다."
    return "공통 안정성 축을 물질화한다."


def carryover_risk(candidate: Mapping[str, Any]) -> str:
    if candidate["run267R_internal_status"].startswith("run267R"):
        return "internal_adapter_variant_collapse_and_monday_session_weakness(내부 어댑터 변형 접힘과 월요일/세션 약점)"
    if as_int(candidate.get("run267P_failure_rows")) > 0:
        return "prior_failure_memory_requires_defensive_watch(이전 실패 기억으로 방어 관찰 필요)"
    return "not_in_internal_branch_needs_pool_wide_reinclude(내부 분기에 없어서 후보군 전체 복귀 필요)"


def build_orthogonal_matrix(candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue_rows = read_csv_rows(RUN267R_QUEUE_PATH)
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        for queue in queue_rows:
            queue_id = queue["queue_id"]
            suffix = queue_id.replace("run267S_axis", "axis")
            rows.append(
                {
                    "matrix_id": f"{RUN_NUMBER}_{candidate['candidate_alias']}_{suffix}",
                    "candidate_order": candidate["candidate_order"],
                    "candidate_id": candidate["candidate_id"],
                    "candidate_alias": candidate["candidate_alias"],
                    "candidate_role": candidate["candidate_role"],
                    "axis_id": queue_id,
                    "axis_class": axis_class(queue_id),
                    "priority": queue["priority"],
                    "hypothesis": queue["hypothesis"],
                    "comparison_baseline": queue["comparison_baseline"],
                    "control_variables": queue["control_variables"],
                    "changed_variables": queue["changed_variables"],
                    "sample_scope": queue["sample_scope"],
                    "source_evidence": (
                        f"{rel(RUN267R_QUEUE_PATH)};{rel(RUN267O_CANDIDATE_SUMMARY_PATH)};"
                        f"{rel(RUN267P_DECISION_PATH)}"
                    ),
                    "carryover_risk": carryover_risk(candidate),
                    "required_action": required_action_for(queue_id),
                    "success_criteria": queue["success_criteria"],
                    "failure_criteria": queue["failure_criteria"],
                    "invalid_conditions": queue["invalid_conditions"],
                    "stop_conditions": queue["stop_conditions"],
                    "evidence_plan": queue["evidence_plan"],
                    "materialization_status": "matrix_materialized_no_mt5_execution_yet",
                    "selected_candidate": "none",
                    "onnx_readiness": "not_claimed",
                }
            )
    return rows


def build_materialization_queue(matrix_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for order, row in enumerate(matrix_rows, start=1):
        axis_id = str(row["axis_id"])
        rows.append(
            {
                "queue_order": order,
                "queue_id": f"run267T_{row['candidate_alias']}_{axis_id.replace('run267S_', '')}",
                "priority": row["priority"],
                "queue_class": "pool_wide_orthogonal_stability_materialization",
                "candidate_id": row["candidate_id"],
                "candidate_alias": row["candidate_alias"],
                "candidate_role": row["candidate_role"],
                "axis_id": axis_id,
                "axis_class": row["axis_class"],
                "required_inputs": (
                    f"{rel(BASELINE_POOL_PATH)};{rel(RUN267R_QUEUE_PATH)};"
                    f"{rel(RUN267O_TEST_REVIEW_PATH)};{rel(RUN267P_QUEUE_PATH)}"
                ),
                "required_action": row["required_action"],
                "risk_runtime_checks": (
                    "feature order(피처 순서);set/ini identity(설정/초기화 정체성);"
                    "trade list(거래 목록);balance/equity curve(잔액/평가금 곡선);"
                    "time-slice KPI(시간 구간 핵심 성과 지표)"
                ),
                "stop_rule": row["stop_conditions"],
                "next_action": NEXT_ACTION,
                "queue_status": "queued_for_next_materialization_not_executed",
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return rows


def build_failure_memory_link(candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    run267r_failure_by_alias = rows_by_alias(read_csv_rows(RUN267R_FAILURE_PATH))
    run267p_failure_rows = read_csv_rows(RUN267P_FAILURE_PATH) if path_exists(RUN267P_FAILURE_PATH) else []
    run267p_failure_by_alias = rows_by_alias(run267p_failure_rows)
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        alias = str(candidate["candidate_alias"])
        r_memory = run267r_failure_by_alias.get(alias)
        p_memory = run267p_failure_by_alias.get(alias)
        if r_memory:
            rows.append(
                {
                    "candidate_alias": alias,
                    "candidate_id": candidate["candidate_id"],
                    "memory_source": "run267R_internal_adapter_prune",
                    "failed_boundary": r_memory.get("failed_boundary", ""),
                    "evidence": r_memory.get("weak_slice_evidence", ""),
                    "carry_forward_rule": "do_not_reopen_internal_branch_without_pool_wide_distinct_shape",
                    "reopen_condition": r_memory.get("reopen_condition", ""),
                    "do_not_repeat": r_memory.get("do_not_repeat", ""),
                }
            )
        elif p_memory or as_int(candidate.get("run267P_failure_rows")) > 0:
            rows.append(
                {
                    "candidate_alias": alias,
                    "candidate_id": candidate["candidate_id"],
                    "memory_source": "run267P_candidate_axis_decision",
                    "failed_boundary": "pool_wide_axis_contains_failure_memory",
                    "evidence": f"failure_rows={candidate.get('run267P_failure_rows')}",
                    "carry_forward_rule": "retain_as_defensive_watch_not_selection",
                    "reopen_condition": "only_if_orthogonal_axis_survives_curve_time_trade_review",
                    "do_not_repeat": "do_not_promote_single_kpi_improvement_without_curve_and_slice_survival",
                }
            )
        else:
            rows.append(
                {
                    "candidate_alias": alias,
                    "candidate_id": candidate["candidate_id"],
                    "memory_source": "run267S_scope_update",
                    "failed_boundary": "no_direct_failure_memory_for_this_axis",
                    "evidence": "retained_for_common_axis_comparison",
                    "carry_forward_rule": "watch_under_same_axes_before_candidate_prune_or_restore",
                    "reopen_condition": "not_applicable",
                    "do_not_repeat": "do_not_drop_candidate_without_common_axis_evidence",
                }
            )
    return rows


def build_experiment_design_receipt() -> list[dict[str, Any]]:
    return [
        {
            "design_field": "hypothesis(가설)",
            "status": "passed",
            "evidence": rel(RUN267R_QUEUE_PATH),
            "effect": "세 축이 후보별로 무엇을 깨려는지 명확하다.",
        },
        {
            "design_field": "comparison(비교)",
            "status": "passed",
            "evidence": f"{rel(RUN267O_CANDIDATE_SUMMARY_PATH)};{rel(RUN267P_DECISION_PATH)}",
            "effect": "run267O/P(267O/P 실행) 근거가 후보군 비교의 기준면이 된다.",
        },
        {
            "design_field": "controls(통제)",
            "status": "passed",
            "evidence": rel(RUN267R_QUEUE_PATH),
            "effect": "US100/M5, 2024 historical stress(2024 과거 압박), 금지 주장 경계를 유지한다.",
        },
        {
            "design_field": "success_failure_stop(성공/실패/중단)",
            "status": "passed",
            "evidence": rel(ORTHOGONAL_MATRIX_PATH),
            "effect": "좋은 숫자보다 덜 깨지는지를 먼저 보게 한다.",
        },
        {
            "design_field": "prior_research_use(이전 연구 활용)",
            "status": "bounded",
            "evidence": rel(PRIOR_AUDIT_PATH),
            "effect": "Stage58(58단계) 이후 연구는 부분 활용됐지만 충분하지 않았다는 판정을 다음 행렬에 반영한다.",
        },
        {
            "design_field": "claim_boundary(주장 경계)",
            "status": "passed",
            "evidence": CLAIM_BOUNDARY,
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), 운영 의미를 주장하지 않는다.",
        },
    ]


def build_gate_receipts() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "experiment_design",
            "gate_status": "passed",
            "evidence": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "effect": "가설, 비교, 통제, 중단 조건을 고정했다.",
        },
        {
            "gate_id": "artifact_lineage",
            "gate_status": "passed",
            "evidence": rel(LINEAGE_PATH),
            "effect": "run267R/O/P(267R/O/P 실행) 입력과 run267S(267S 실행) 산출물을 연결했다.",
        },
        {
            "gate_id": "data_integrity",
            "gate_status": "bounded",
            "evidence": rel(RUN267O_TEST_REVIEW_PATH),
            "effect": "새 학습이나 MT5(MetaTrader 5, 메타트레이더5) 실행 없이 기존 검토 근거만 재배열했다.",
        },
        {
            "gate_id": "model_validation",
            "gate_status": "bounded",
            "evidence": rel(ORTHOGONAL_MATRIX_PATH),
            "effect": "모델 선택이 아니라 다음 검증 표면 물질화라서 선택 후보는 없다.",
        },
        {
            "gate_id": "result_judgment",
            "gate_status": "passed",
            "evidence": rel(REPORT_PATH),
            "effect": "Goal Achieve(목표 달성), ONNX readiness(ONNX 준비)를 주장하지 않는다.",
        },
        {
            "gate_id": "required_gate_coverage_audit",
            "gate_status": "passed",
            "evidence": rel(GATE_RECEIPT_PATH),
            "effect": "이번 작업 묶음의 필수 gate(게이트)를 closeout(종료 기록)에 연결했다.",
        },
    ]


def build_lineage() -> dict[str, Any]:
    return {
        "producer": rel(PRODUCER_PATH),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": [
            rel(BASELINE_POOL_PATH),
            rel(RUN267R_QUEUE_PATH),
            rel(RUN267R_PRUNE_PATH),
            rel(RUN267R_FAILURE_PATH),
            rel(RUN267R_RESULT_PATH),
            rel(RUN267O_CANDIDATE_SUMMARY_PATH),
            rel(RUN267O_TEST_REVIEW_PATH),
            rel(RUN267O_NEGATIVE_SLICE_PATH),
            rel(RUN267O_CURVE_DIAGNOSTICS_PATH),
            rel(RUN267P_DECISION_PATH),
            rel(RUN267P_QUEUE_PATH),
            rel(PRIOR_AUDIT_PATH),
        ],
        "outputs": {
            "candidate_scope": rel(CANDIDATE_SCOPE_PATH),
            "orthogonal_matrix": rel(ORTHOGONAL_MATRIX_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "failure_memory_link": rel(FAILURE_MEMORY_LINK_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "gate_receipt": rel(GATE_RECEIPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "lineage_judgment": "connected_materialization_matrix_no_candidate_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_report(result: Mapping[str, Any]) -> str:
    candidates = result["candidate_scope"]
    matrix_rows = result["orthogonal_matrix"]
    lines = [
        "# Stage267 Run267S Pool-wide Orthogonal Stability Racing Matrix(267단계 267S 후보군 전체 직교 안정성 경주 행렬)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(부모 실행): `{PARENT_RUN_ID}`",
        f"- candidate_count(후보 수): `{len(candidates)}`",
        f"- axis_count(축 수): `{result['axis_count']}`",
        f"- matrix_rows(행렬 행): `{len(matrix_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267R(267R 실행)은 내부 Adapter(어댑터) 분기를 선택하지 않고 회수 단서로 낮췄다.",
        "Effect(효과): 변형 차이가 같은 KPI shape(핵심 성과 지표 모양)으로 접히고 Monday/session(월요일/세션) 약점이 반복된 분기를 계속 미세 수리하지 않는다.",
        "",
        "run267S(267S 실행)는 그 결과를 다섯 Baseline candidates(기준 후보) 전체에 다시 펼쳤다.",
        "Effect(효과): 한 후보나 한 feature(피처)에 붙지 않고, 누가 더 넓은 조건에서 덜 깨지는지 보는 다음 물질화 큐를 만든다.",
        "",
        "## Stage58 Question(58단계 질문)",
        "",
        "질문은 Stage58(58단계)부터 본격적인 Baseline 후보(기준 후보)를 정하면서 이전 연구를 충분히 이후 stage(단계)에 썼느냐였다.",
        "판정은 `partially_used_but_not_sufficient_for_current_goal(부분 활용, 현재 목표에는 불충분)`이다.",
        "Effect(효과): 이전 연구를 버리지는 않았지만, 압축 feature(피처)와 gate/rank bucket(게이트/순위 구간)에 너무 접힌 부분을 run267S(267S 실행)부터 후보군 전체 축으로 다시 벌린다.",
        "",
        "## Candidate Scope(후보 범위)",
        "",
        "| candidate(후보) | role(역할) | run267R status(267R 상태) | pool decision(후보군 판정) |",
        "| --- | --- | --- | --- |",
    ]
    for row in candidates:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['candidate_role_read']} | `{row['run267R_internal_status']}` | `{row['pool_decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Axes(축)",
            "",
            "| axis(축) | priority(우선순위) | effect(효과) |",
            "| --- | --- | --- |",
        ]
    )
    seen_axes: set[str] = set()
    for row in matrix_rows:
        axis_id = str(row["axis_id"])
        if axis_id in seen_axes:
            continue
        seen_axes.add(axis_id)
        lines.append(f"| `{axis_id}` | `{row['priority']}` | {row['required_action']} |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- judgment(판정): `matrix_materialized_execution_pending_no_candidate_selection(행렬 물질화, 실행 대기, 선택 후보 없음)`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).",
            "",
            "## Artifacts(산출물)",
            "",
            f"- candidate_scope(후보 범위): `{rel(CANDIDATE_SCOPE_PATH)}`",
            f"- orthogonal_matrix(직교 행렬): `{rel(ORTHOGONAL_MATRIX_PATH)}`",
            f"- materialization_queue(물질화 큐): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- failure_memory_link(실패 기억 연결): `{rel(FAILURE_MEMORY_LINK_PATH)}`",
            f"- experiment_design_receipt(실험 설계 기록): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- gate_receipt(게이트 기록): `{rel(GATE_RECEIPT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = (
        ("stage267_run267S_script", "producer_script", PRODUCER_PATH, "Builds run267S pool-wide orthogonal stability racing matrix."),
        ("stage267_run267S_candidate_scope", "candidate_scope", CANDIDATE_SCOPE_PATH, "Run267S candidate scope update."),
        ("stage267_run267S_orthogonal_matrix", "orthogonal_stability_matrix", ORTHOGONAL_MATRIX_PATH, "Run267S orthogonal stability matrix."),
        ("stage267_run267S_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267S next materialization queue."),
        ("stage267_run267S_failure_memory_link", "failure_memory_link", FAILURE_MEMORY_LINK_PATH, "Run267S failure memory link."),
        ("stage267_run267S_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267S experiment design receipt."),
        ("stage267_run267S_gate_receipt", "gate_receipt", GATE_RECEIPT_PATH, "Run267S gate receipt."),
        ("stage267_run267S_lineage", "lineage", LINEAGE_PATH, "Run267S artifact lineage."),
        ("stage267_run267S_result", "result", RESULT_PATH, "Run267S result payload."),
        ("stage267_run267S_report", "review_report", REPORT_PATH, "Run267S user-facing report."),
    )
    rows = []
    for artifact_id, artifact_type, path, notes in artifacts:
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


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        CANDIDATE_SCOPE_PATH,
        result["candidate_scope"],
        (
            "candidate_order",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "candidate_role_read",
            "source_stage",
            "source_run",
            "initial_racing_use",
            "known_strength",
            "known_risk",
            "run267O_candidate_read",
            "run267O_best_test",
            "run267O_best_net_profit",
            "run267O_best_profit_factor",
            "run267O_worst_month_floor",
            "run267P_candidate_decision",
            "run267P_p0_tests",
            "run267P_p1_tests",
            "run267P_failure_rows",
            "run267R_internal_status",
            "run267R_monday_net",
            "run267R_session_07_12_net",
            "pool_decision",
            "pool_decision_reason",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        ORTHOGONAL_MATRIX_PATH,
        result["orthogonal_matrix"],
        (
            "matrix_id",
            "candidate_order",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "axis_id",
            "axis_class",
            "priority",
            "hypothesis",
            "comparison_baseline",
            "control_variables",
            "changed_variables",
            "sample_scope",
            "source_evidence",
            "carryover_risk",
            "required_action",
            "success_criteria",
            "failure_criteria",
            "invalid_conditions",
            "stop_conditions",
            "evidence_plan",
            "materialization_status",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        MATERIALIZATION_QUEUE_PATH,
        result["materialization_queue"],
        (
            "queue_order",
            "queue_id",
            "priority",
            "queue_class",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "axis_id",
            "axis_class",
            "required_inputs",
            "required_action",
            "risk_runtime_checks",
            "stop_rule",
            "next_action",
            "queue_status",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        FAILURE_MEMORY_LINK_PATH,
        result["failure_memory_link"],
        (
            "candidate_alias",
            "candidate_id",
            "memory_source",
            "failed_boundary",
            "evidence",
            "carry_forward_rule",
            "reopen_condition",
            "do_not_repeat",
        ),
    )
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("design_field", "status", "evidence", "effect"))
    write_csv(GATE_RECEIPT_PATH, result["gate_receipt"], ("gate_id", "gate_status", "evidence", "effect"))
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, build_report(result))


def update_ledgers(result: Mapping[str, Any]) -> None:
    primary_kpi = (
        f"candidates={result['candidate_count']};axes={result['axis_count']};"
        f"matrix_rows={result['matrix_row_count']};queue_rows={result['queue_row_count']}"
    )
    guardrail = "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed"
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267S_pool_wide_orthogonal_stability_racing_matrix",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pool_wide_orthogonal_stability_racing_matrix",
                "tier_scope": "Tier A and actual routed total historical 2024 matrix planning",
                "scoreboard": "experiment_design_artifact_lineage_result_judgment",
                "status": STATUS,
                "judgment": "matrix_materialized_execution_pending_no_candidate_selection",
                "evidence_boundary": "matrix_and_queue_only_no_mt5_execution_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"{primary_kpi};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_stability_racing_matrix",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "pool_wide_orthogonal_stability_racing_matrix",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "pool_wide_orthogonal_stability_racing_matrix",
                "tier_scope": "Tier A and actual routed total historical 2024 matrix planning",
                "kpi_scope": "matrix_materialization_no_mt5_kpi",
                "scoreboard_lane": "experiment_design_artifact_lineage_result_judgment",
                "status": STATUS,
                "judgment": "matrix_materialized_execution_pending_no_candidate_selection",
                "path": rel(REPORT_PATH),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "external_verification_status": "not_started_matrix_only",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "pool_wide_orthogonal_stability_racing_matrix",
                "status": STATUS,
                "judgment": "matrix_materialized_execution_pending_no_candidate_selection",
                "path": rel(REPORT_PATH),
                "notes": f"Run267S matrix materialized; {primary_kpi}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(str(result["created_at_utc"])),
        key="artifact_id",
    )


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267S_pool_wide_orthogonal_stability_racing_matrix(267S 후보군 전체 직교 안정성 경주 행렬): "
        f"`{rel(REPORT_PATH)}`"
    )
    status_line = f"`{STATUS}`"
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_stability_matrix`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): {status_line}")
    current = append_after_contains(current, "run267R_internal_adapter_stability_followup_or_prune", report_line)
    latest_line = (
        "- latest_matrix(최신 행렬): run267S(267S 실행) pool-wide orthogonal stability racing matrix"
        f"(후보군 전체 직교 안정성 경주 행렬) `{rel(REPORT_PATH)}`."
    )
    current = append_after_contains(current, "latest_design(최신 설계): run267R", latest_line)
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- action(행동):",
        "- action(행동): run267S(267S 실행)는 run267R(267R 실행)의 가지치기 결과를 다섯 Baseline candidates(기준 후보) 전체의 직교 안정성 행렬로 물질화했다.",
    )
    current = replace_line_prefix(
        current,
        "- effect(효과):",
        "- effect(효과): 한 후보 내부 Adapter(어댑터) 수리로 좁아지지 않고, 후보군 전체가 같은 축에서 덜 깨지는지 비교할 수 있다.",
    )
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_block_once(
        current,
        "Run267S(267S 실행)는 다섯 Baseline candidates",
        (
            "Run267S(267S 실행)는 다섯 Baseline candidates(기준 후보)의 orthogonal stability racing matrix"
            "(직교 안정성 경주 행렬)를 물질화했다.\n"
            "Effect(효과): Stage58(58단계) 이후 연구가 부분 활용에 그쳤다는 감사를 받아, "
            "후보군 전체를 ablation/replacement(제거/대체), non-calendar weak-slice resilience"
            "(비달력 약점 구간 견고성), prune/restore(가지치기/복귀) 축에 다시 올렸다."
        ),
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    for path, status_prefix in (
        (SELECTION_STATUS_PATH, "- stage_status(단계 상태):"),
        (REVIEW_INDEX_PATH, "- status(상태):"),
    ):
        text = read_text(path)
        text = replace_line_prefix(text, status_prefix, f"{status_prefix} {status_line}")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, "run267R_internal_adapter_stability_followup_or_prune", report_line)
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_block_once(
            text,
            "Run267S(267S 실행)는 후보군 전체 직교 안정성 경주 행렬을 물질화했다.",
            (
                "Run267S(267S 실행)는 후보군 전체 직교 안정성 경주 행렬을 물질화했다.\n"
                "Effect(효과): selected candidate(선택 후보) 없이 다음 MT5(MetaTrader 5, 메타트레이더5) "
                "물질화/실행 큐로 넘어갈 수 있게 후보, 축, 실패 기억, 중단 조건을 연결했다."
            ),
        )
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267S(267S 실행) pool-wide orthogonal stability racing matrix"
        f"(후보군 전체 직교 안정성 경주 행렬) `{STATUS}`. Effect(효과): 다섯 Baseline candidates"
        "(기준 후보)를 같은 세 안정성 축에 다시 올렸고 selected candidate(선택 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267S_materialize_pool_wide_orthogonal_stability_racing_matrix`이다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
        1,
    )
    workspace = workspace.replace(
        "run267R(267R 실행)의 가지치기 결과를 받아 다섯 Baseline candidates(기준 후보) 전체의 orthogonal stability racing(직교 안정성 경주)을 물질화한다.",
        "run267S(267S 실행) 행렬을 받아 다음 MT5(MetaTrader 5, 메타트레이더5) 물질화 후보를 만든다.",
        1,
    )
    workspace = workspace.replace(f"  status: run267R_internal_adapter_stability_followup_or_prune_completed", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {PARENT_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {PARENT_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = append_after_contains(
        workspace,
        "run267R_internal_adapter_stability_followup_or_prune_path",
        f"  run267S_pool_wide_orthogonal_stability_racing_matrix_path: {rel(REPORT_PATH)}",
    )
    workspace = workspace.replace(
        "  next_action: run267S_materialize_pool_wide_orthogonal_stability_racing_matrix",
        f"  next_action: {NEXT_ACTION}",
        1,
    )
    workspace = workspace.replace(
        "active_run267R_internal_adapter_stability_followup_or_prune_completed(267R 내부 어댑터 안정성 후속/가지치기 완료, 후보군 전체 안정성 경주 물질화 대기 활성)",
        "active_run267S_pool_wide_orthogonal_stability_racing_matrix_materialized(267S 후보군 전체 직교 안정성 경주 행렬 물질화 완료, 다음 MT5 물질화 대기 활성)",
        1,
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    require_inputs()
    candidates = candidate_rows()
    matrix = build_orthogonal_matrix(candidates)
    queue = build_materialization_queue(matrix)
    failure_memory = build_failure_memory_link(candidates)
    design_receipt = build_experiment_design_receipt()
    gate_receipt = build_gate_receipts()
    lineage = build_lineage()
    axis_count = len({row["axis_id"] for row in matrix})
    result = {
        "created_at_utc": utc_now(),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "candidate_count": len(candidates),
        "axis_count": axis_count,
        "matrix_row_count": len(matrix),
        "queue_row_count": len(queue),
        "failure_memory_rows": len(failure_memory),
        "candidate_scope": candidates,
        "orthogonal_matrix": matrix,
        "materialization_queue": queue,
        "failure_memory_link": failure_memory,
        "experiment_design_receipt": design_receipt,
        "gate_receipt": gate_receipt,
        "lineage": lineage,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return result


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_current_docs(result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "candidate_count": result["candidate_count"],
                "axis_count": result["axis_count"],
                "matrix_row_count": result["matrix_row_count"],
                "queue_row_count": result["queue_row_count"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
