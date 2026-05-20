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

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_NUMBER = "run267L"
RUN_ID = "run267L_stage267_retrained_soft_context_followup_or_prune_v1"
STATUS = "run267L_retrained_soft_context_followup_or_prune_completed"
NEXT_ACTION = "run267M_design_pool_wide_ablation_replacement_and_weak_slice_matrix"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "retrained_soft_context_followup_or_prune"

RUN267J_ROOT = STAGE_ROOT / "02_runs" / "run267J" / "retrained_soft_context_adapter_design"
RUN267K_ROOT = STAGE_ROOT / "02_runs" / "run267K" / "retrained_soft_context_adapter_materialization"
RUN267B_ROOT = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024"

RUN267J_STOP_RULES = RUN267J_ROOT / "stop_rules.csv"
RUN267J_WEAKNESS_TARGETS = RUN267J_ROOT / "weakness_target_matrix.csv"
RUN267K_CANDIDATE_REVIEW = RUN267K_ROOT / "candidate_retrained_soft_context_review.csv"
RUN267K_NEGATIVE_SLICES = RUN267K_ROOT / "negative_slice_summary.csv"
RUN267K_CURVE_DIAGNOSTICS = RUN267K_ROOT / "curve_diagnostics.csv"
RUN267B_KPI_SUMMARY = RUN267B_ROOT / "mt5_kpi_summary.csv"

DECISION_MATRIX_PATH = DESIGN_ROOT / "followup_or_prune_decision_matrix.csv"
STOP_AUDIT_PATH = DESIGN_ROOT / "stop_rule_audit.csv"
NEXT_EXPERIMENT_PATH = DESIGN_ROOT / "next_pool_wide_experiment_design.csv"
VALIDATION_RECEIPT_PATH = DESIGN_ROOT / "design_validation_receipt.csv"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267L_retrained_soft_context_followup_or_prune.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267L_retrained_soft_context_followup_or_prune.py")

STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

BASELINE_POOL = (
    "s264_allow_inner_high_quarter",
    "s264_lowrank_control",
    "s262_lowrank_inner_half_filter",
    "s264_allow_inner_all_oos_anchor",
    "s258_short_tight_control",
)

TARGETS = {
    "s264_aih": {
        "net_floor": 170.0,
        "pf_floor": 1.10,
        "trade_floor": 340,
        "dd_ceiling": 28.5,
        "monday_floor": -100.0,
        "july_floor": -80.0,
        "chron_mid_floor": -60.0,
    },
    "s264_lc": {
        "net_floor": 145.0,
        "pf_floor": 1.09,
        "trade_floor": 337,
        "dd_ceiling": 29.5,
        "monday_floor": -105.0,
        "july_floor": -85.0,
        "chron_mid_floor": -65.0,
    },
}


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
    if isinstance(value, (list, tuple)):
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


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
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


def replace_tail_from_marker(text: str, marker: str, replacement: str) -> str:
    start = text.find(marker)
    if start == -1:
        return text.rstrip() + "\n" + replacement.rstrip() + "\n"
    return text[:start].rstrip() + "\n" + replacement.rstrip() + "\n"


def find_slice(rows: Sequence[Mapping[str, str]], alias: str, axis: str, bucket: str) -> dict[str, str]:
    for row in rows:
        if row.get("candidate_alias") == alias and row.get("axis") == axis and row.get("bucket") == bucket:
            return dict(row)
    return {}


def pass_fail(condition: bool) -> str:
    return "pass(통과)" if condition else "fail(실패)"


def build_decision_matrix(
    candidate_rows: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in candidate_rows:
        alias = str(source.get("candidate_alias"))
        target = TARGETS.get(alias, {})
        if not target:
            continue
        monday = find_slice(negative_rows, alias, "weekday", "Monday")
        july = find_slice(negative_rows, alias, "month", "2024-07")
        december = find_slice(negative_rows, alias, "month", "2024-12")
        chron_mid = find_slice(negative_rows, alias, "chron_segment", "chron_mid")
        net_profit = as_float(source.get("net_profit"))
        profit_factor = as_float(source.get("profit_factor"))
        trade_count = as_int(source.get("trade_count"))
        drawdown = as_float(source.get("report_equity_drawdown_percent"))
        monday_net = as_float(monday.get("net_profit"))
        july_net = as_float(july.get("net_profit"))
        december_net = as_float(december.get("net_profit"))
        chron_mid_net = as_float(chron_mid.get("net_profit"), as_float(source.get("weakest_chron_net")))
        pass_count = sum(
            [
                net_profit >= target["net_floor"],
                profit_factor >= target["pf_floor"],
                trade_count >= target["trade_floor"],
                drawdown <= target["dd_ceiling"],
                monday_net > target["monday_floor"],
                july_net > target["july_floor"],
                chron_mid_net > target["chron_mid_floor"],
            ]
        )
        decision = "prune_standalone_retrain_branch(독립 재학습 분기 가지치기)"
        if pass_count >= 6 and monday_net > target["monday_floor"]:
            decision = "allow_one_structural_followup(구조 후속 1회 허용)"
        rows.append(
            {
                "candidate_id": source.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": source.get("candidate_role"),
                "net_profit": net_profit,
                "profit_factor": profit_factor,
                "trade_count": trade_count,
                "equity_dd_percent": drawdown,
                "monday_net": monday_net,
                "july_net": july_net,
                "december_net": december_net,
                "chron_mid_net": chron_mid_net,
                "net_gate": pass_fail(net_profit >= target["net_floor"]),
                "pf_gate": pass_fail(profit_factor >= target["pf_floor"]),
                "trade_gate": pass_fail(trade_count >= target["trade_floor"]),
                "dd_gate": pass_fail(drawdown <= target["dd_ceiling"]),
                "monday_gate": pass_fail(monday_net > target["monday_floor"]),
                "july_gate": pass_fail(july_net > target["july_floor"]),
                "chron_mid_gate": pass_fail(chron_mid_net > target["chron_mid_floor"]),
                "passed_gate_count": pass_count,
                "decision": decision,
                "salvage_value": (
                    "keep_soft_context_score_as_candidate_feature(부드러운 문맥 점수는 후보 피처로 보존)"
                ),
                "do_not_repeat": (
                    "do_not_extend_score_table_retrain_without_new_structure(새 구조 없는 점수표 재학습 반복 금지)"
                ),
            }
        )
    return rows


def build_stop_audit(decision_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    any_trade_fail = any("fail" in str(row.get("trade_gate")) for row in decision_rows)
    any_monday_fail = any("fail" in str(row.get("monday_gate")) for row in decision_rows)
    any_december_hole = any(as_float(row.get("december_net")) < -200.0 for row in decision_rows)
    all_net_pf_improved = all(as_float(row.get("net_profit")) > 600.0 and as_float(row.get("profit_factor")) > 1.30 for row in decision_rows)
    return [
        {
            "rule_id": "J_STOP_03_p0_underperforms_run267I",
            "trigger_evidence": "net_pf_dd_improved_but_trade_count_collapsed(순수익/수익 팩터/손실폭 개선, 거래 수 축소)",
            "status": "partial_trigger(부분 발동)",
            "action": "do_not_close_as_failure_but_stop_pure_retrain_loop(실패 종료는 아니지만 순수 재학습 반복 중단)",
            "effect": "preserves_improvement_without_micro_loop(개선 단서는 보존하고 미세 반복은 막음)",
            "evidence_path": rel(RUN267K_CANDIDATE_REVIEW),
        },
        {
            "rule_id": "J_STOP_04_weak_slices_not_repaired",
            "trigger_evidence": "Monday_and_2024_12_remain_deep_negative(월요일과 2024-12 깊은 음수 유지)",
            "status": "triggered(발동)",
            "action": "prune_standalone_retrain_branch_and_return_to_pool_wide_design(독립 재학습 분기 가지치기 후 후보군 전체 설계 복귀)",
            "effect": "prevents_single_slice_bottleneck(단일 구간 병목 방지)",
            "evidence_path": rel(RUN267K_NEGATIVE_SLICES),
        },
        {
            "rule_id": "GOAL_GUARD_trade_count_and_curve",
            "trigger_evidence": f"trade_count_fail={any_trade_fail};monday_fail={any_monday_fail};december_hole={any_december_hole};net_pf_improved={all_net_pf_improved}",
            "status": "not_goal_candidate(목표 후보 아님)",
            "action": "no_selected_candidate_no_onnx(선택 후보 없음, ONNX 없음)",
            "effect": "keeps_RnD_racing_boundary(연구개발 경주 경계 유지)",
            "evidence_path": rel(RUN267K_CURVE_DIAGNOSTICS),
        },
    ]


def build_next_experiment() -> list[dict[str, Any]]:
    pool = ";".join(BASELINE_POOL)
    return [
        {
            "design_id": "run267M_pool_wide_weak_slice_ablation_matrix",
            "hypothesis": (
                "weak_slices_are_feature_structure_problem_not_single_threshold_problem"
                "(약한 구간은 단일 문턱값이 아니라 피처 구조 문제)"
            ),
            "decision_use": "rank_prune_or_salvage_baseline_candidates(후보 순위화/가지치기/회수 결정)",
            "comparison_baseline": "run267B_historical_2024_and_run267K_retrain_review(267B 2024와 267K 재학습 검토)",
            "candidate_scope": pool,
            "changed_variables": (
                "feature_category_ablation_and_trend_strength_replacement"
                "(피처 범주 제거와 추세 강도 유사 대체)"
            ),
            "control_variables": "US100;M5;2024 historical stress;same cost/deposit/tester contract(US100;M5;2024 과거 압박;동일 비용/예치금/테스터 계약)",
            "success_criteria": (
                "DD_and_weak_month_reduced_without_trade_count_collapse"
                "(손실폭과 약한 월 감소, 거래 수 붕괴 없음)"
            ),
            "failure_criteria": (
                "candidate_only_survives_one_month_or_one_feature"
                "(한 달 또는 한 피처에서만 생존)"
            ),
            "invalid_conditions": (
                "feature_order_or_label_split_unresolved_or_2024_outcome_used"
                "(피처 순서/라벨 분리 미확인 또는 2024 결과 사용)"
            ),
            "evidence_plan": (
                "candidate_review;negative_slice_summary;curve_diagnostics;trade_records;ledger_rows"
                "(후보 검토, 음수 구간, 곡선 진단, 거래 기록, 장부 행)"
            ),
        },
        {
            "design_id": "run267M_replacement_axis_adx_atr_di_family",
            "hypothesis": (
                "trend_strength_signal_should_survive_similar_replacement"
                "(추세 강도 신호는 유사 대체에서도 버텨야 함)"
            ),
            "decision_use": "separate_real_signal_from_indicator_accident(실제 신호와 지표 우연 분리)",
            "comparison_baseline": "stage267_adx_atr_soft_score_and_run267K_supervised_retrain(ADX/ATR 점수와 267K 지도 재학습)",
            "candidate_scope": pool,
            "changed_variables": (
                "ADX_ATR_soft_score_replaced_by_DI_spread_ATR_rank_volatility_state"
                "(ADX/ATR 점수를 DI 스프레드/ATR 순위/변동성 상태로 대체)"
            ),
            "control_variables": "same split, same MT5 tester, same route interpretation(동일 분리, 동일 MT5 테스터, 동일 라우팅 해석)",
            "success_criteria": "candidate_degrades_gracefully(후보가 완만하게 약화)",
            "failure_criteria": "performance_disappears_when_ADX_removed(ADX 제거 시 성과 소멸)",
            "invalid_conditions": "replacement_feature_uses_future_bar(대체 피처가 미래 봉 사용)",
            "evidence_plan": "feature_manifest;parity_check;time_slice_kpi;curve_review(피처 목록, 동등성 점검, 시간 구간 KPI, 곡선 검토)",
        },
        {
            "design_id": "run267M_pool_return_prune_receipt",
            "hypothesis": "pure_retrain_branch_is_salvage_not_candidate(순수 재학습 분기는 후보가 아니라 회수 단서)",
            "decision_use": "prevent_repair_loop_longer_than_allowed(허용보다 긴 수리 루프 방지)",
            "comparison_baseline": "run267J_stop_rules_and_run267K_actual_review(267J 중단 규칙과 267K 실제 검토)",
            "candidate_scope": "s264_aih;s264_lc salvage only(회수 단서만)",
            "changed_variables": "none_design_gate_only(없음, 설계 게이트만)",
            "control_variables": "claim_boundary_no_candidate_no_onnx(선택 후보 없음, ONNX 없음)",
            "success_criteria": "next_work_targets_all_five_candidates(다음 작업이 다섯 후보 전체를 겨냥)",
            "failure_criteria": "next_work_tunes_only_Monday_threshold(다음 작업이 월요일 문턱값만 조정)",
            "invalid_conditions": "missing_run267K_review_evidence(267K 검토 근거 누락)",
            "evidence_plan": "this_report_and_state_sync(이 보고서와 상태 동기화)",
        },
    ]


def build_validation_receipt() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "experiment_design_receipt",
            "check_family": "obsidian-experiment-design(실험 설계)",
            "requirement": "hypothesis_comparison_controls_success_failure_stop_evidence_named(가설/비교/통제/성공/실패/중단/근거 명명)",
            "evidence_source": rel(NEXT_EXPERIMENT_PATH),
            "pass_condition": "all_rows_have_required_fields(모든 행 필수 필드 존재)",
            "failure_action": "do_not_materialize_run267M(267M 물질화 금지)",
            "effect": "prevents_vague_followup(모호한 후속 방지)",
        },
        {
            "check_id": "data_integrity_receipt",
            "check_family": "obsidian-data-integrity(데이터 무결성)",
            "requirement": "source_time_axis_split_leakage_boundary_named(원천/시간축/분리/누수 경계 명명)",
            "evidence_source": rel(REPORT_PATH),
            "pass_condition": "2024_outcome_not_used_for_training_target(2024 결과를 학습 목표로 쓰지 않음)",
            "failure_action": "mark_invalid(무효 처리)",
            "effect": "prevents_historical_stress_leakage(과거 압박 누수 방지)",
        },
        {
            "check_id": "model_validation_receipt",
            "check_family": "obsidian-model-validation(모델 검증)",
            "requirement": "model_family_threshold_policy_overfit_risk_named(모델군/문턱값 정책/과적합 위험 명명)",
            "evidence_source": rel(REPORT_PATH),
            "pass_condition": "no_model_selection_claim(모델 선택 주장 없음)",
            "failure_action": "downgrade_to_inconclusive(불충분으로 낮춤)",
            "effect": "prevents_one_split_model_claim(단일 분리 모델 주장 방지)",
        },
        {
            "check_id": "result_judgment_receipt",
            "check_family": "obsidian-result-judgment(결과 판정)",
            "requirement": "claim_boundary_selected_candidate_onnx_goal_all_named(주장 경계/선택 후보/ONNX/목표 상태 명명)",
            "evidence_source": rel(REPORT_PATH),
            "pass_condition": "selected_candidate_none_and_onnx_not_claimed(선택 후보 없음과 ONNX 미주장)",
            "failure_action": "block_closeout_claim(종료 주장 차단)",
            "effect": "keeps_research_boundary(연구 경계 유지)",
        },
    ]


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    items = [
        ("stage267_run267L_followup_or_prune_script", "producer_script", PRODUCER_PATH, "Builds run267L follow-up-or-prune decision."),
        ("stage267_run267L_decision_matrix", "decision_matrix", DECISION_MATRIX_PATH, "Run267L follow-up-or-prune candidate decision matrix."),
        ("stage267_run267L_stop_rule_audit", "stop_rule_audit", STOP_AUDIT_PATH, "Run267L stop-rule audit against run267J and run267K."),
        ("stage267_run267L_next_experiment_design", "experiment_design", NEXT_EXPERIMENT_PATH, "Run267L pool-wide next experiment design."),
        ("stage267_run267L_validation_receipt", "validation_receipt", VALIDATION_RECEIPT_PATH, "Run267L design validation receipt."),
        ("stage267_run267L_lineage", "lineage", LINEAGE_PATH, "Run267L lineage."),
        ("stage267_run267L_result", "result", RESULT_PATH, "Run267L JSON result."),
        ("stage267_run267L_report", "review_report", REPORT_PATH, "User-facing run267L report."),
    ]
    rows = []
    for artifact_id, artifact_type, path, notes in items:
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


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    candidate_rows = read_csv(RUN267K_CANDIDATE_REVIEW)
    negative_rows = read_csv(RUN267K_NEGATIVE_SLICES)
    decision_rows = build_decision_matrix(candidate_rows, negative_rows)
    stop_rows = build_stop_audit(decision_rows)
    next_rows = build_next_experiment()
    validation_rows = build_validation_receipt()
    lineage = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "inputs": {
            "run267J_stop_rules": rel(RUN267J_STOP_RULES),
            "run267J_weakness_targets": rel(RUN267J_WEAKNESS_TARGETS),
            "run267K_candidate_review": rel(RUN267K_CANDIDATE_REVIEW),
            "run267K_negative_slices": rel(RUN267K_NEGATIVE_SLICES),
            "run267K_curve_diagnostics": rel(RUN267K_CURVE_DIAGNOSTICS),
            "run267B_kpi_summary": rel(RUN267B_KPI_SUMMARY),
        },
        "outputs": {
            "decision_matrix": rel(DECISION_MATRIX_PATH),
            "stop_rule_audit": rel(STOP_AUDIT_PATH),
            "next_experiment_design": rel(NEXT_EXPERIMENT_PATH),
            "validation_receipt": rel(VALIDATION_RECEIPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    return {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "decision": "prune_standalone_retrain_branch_and_return_to_pool_wide_racing",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "decision_matrix": decision_rows,
        "stop_rule_audit": stop_rows,
        "next_experiment_design": next_rows,
        "validation_receipt": validation_rows,
        "lineage": lineage,
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        DECISION_MATRIX_PATH,
        result["decision_matrix"],
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "net_profit",
            "profit_factor",
            "trade_count",
            "equity_dd_percent",
            "monday_net",
            "july_net",
            "december_net",
            "chron_mid_net",
            "net_gate",
            "pf_gate",
            "trade_gate",
            "dd_gate",
            "monday_gate",
            "july_gate",
            "chron_mid_gate",
            "passed_gate_count",
            "decision",
            "salvage_value",
            "do_not_repeat",
        ),
    )
    write_csv(
        STOP_AUDIT_PATH,
        result["stop_rule_audit"],
        ("rule_id", "trigger_evidence", "status", "action", "effect", "evidence_path"),
    )
    write_csv(
        NEXT_EXPERIMENT_PATH,
        result["next_experiment_design"],
        (
            "design_id",
            "hypothesis",
            "decision_use",
            "comparison_baseline",
            "candidate_scope",
            "changed_variables",
            "control_variables",
            "success_criteria",
            "failure_criteria",
            "invalid_conditions",
            "evidence_plan",
        ),
    )
    write_csv(
        VALIDATION_RECEIPT_PATH,
        result["validation_receipt"],
        ("check_id", "check_family", "requirement", "evidence_source", "pass_condition", "failure_action", "effect"),
    )
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def fmt(value: Any) -> str:
    return f"{as_float(value):.2f}"


def report_markdown(result: Mapping[str, Any]) -> str:
    decision_rows = list(result["decision_matrix"])
    stop_rows = list(result["stop_rule_audit"])
    next_rows = list(result["next_experiment_design"])
    lines = [
        "# Stage267 Run267L Retrained Soft-Context Follow-up or Prune(267L 재학습 부드러운 문맥 후속 또는 가지치기)",
        "",
        "## Summary(요약)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        "- primary_family(주 작업군): `experiment_design(실험 설계)`.",
        "- primary_skill(주 스킬): `obsidian-experiment-design(실험 설계)`.",
        "- support_skills(보조 스킬): `obsidian-data-integrity(데이터 무결성)`, `obsidian-model-validation(모델 검증)`, `obsidian-result-judgment(결과 판정)`, `obsidian-performance-attribution(성과 귀인)`.",
        "- action(행동): run267K(267K 실행)의 재학습 결과를 run267J(267J 실행) 중단 규칙과 대조해 후속 또는 가지치기를 결정했다.",
        "- effect(효과): 순수익 개선 단서는 보존하지만, Monday(월요일)와 2024-12 약점 때문에 독립 retrain branch(재학습 분기)를 더 끌지 않는다.",
        "",
        "## Decision Matrix(결정 행렬)",
        "",
        "| candidate(후보) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | Monday(월요일) | 2024-12 | gates(게이트) | decision(결정) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in decision_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | {fmt(row['net_profit'])} | {fmt(row['profit_factor'])} | "
            f"{row['trade_count']} | {fmt(row['equity_dd_percent'])} | {fmt(row['monday_net'])} | "
            f"{fmt(row['december_net'])} | {row['passed_gate_count']}/7 | {row['decision']} |"
        )
    lines.extend(
        [
            "",
            "## Stop Audit(중단 감사)",
            "",
            "| rule(규칙) | status(상태) | action(행동) | effect(효과) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in stop_rows:
        lines.append(f"| `{row['rule_id']}` | {row['status']} | {row['action']} | {row['effect']} |")
    lines.extend(
        [
            "",
            "## Experiment Design(실험 설계)",
            "",
            "- hypothesis(가설): weak slices(약한 구간)는 단일 threshold(문턱값) 문제가 아니라 feature structure(피처 구조)와 exposure shape(노출 형태) 문제일 가능성이 크다.",
            "- decision_use(결정 사용처): 다섯 Baseline candidates(기준 후보)를 유지, 가지치기, 회수할지 정한다.",
            "- comparison_baseline(비교 기준): run267B(267B 실행) 2024 historical stress(2024 과거 압박), run267K(267K 실행) retrain review(재학습 검토).",
            "- control_variables(통제 변수): US100, M5, 2024 historical stress(2024 과거 압박), 동일 tester contract(테스터 계약), 동일 비용/예치금.",
            "- changed_variables(변경 변수): feature/category ablation(피처/범주 제거), similar replacement(유사 대체), weak-slice exposure matrix(약한 구간 노출 행렬).",
            "- success_criteria(성공 기준): DD(drawdown, 손실폭)와 weak month(약한 월)가 줄면서 trade count(거래 수)가 붕괴하지 않는다.",
            "- failure_criteria(실패 기준): 한 feature(피처), 한 month(월), 한 weekday(요일)에만 붙어 있으면 실패다.",
            "- invalid_conditions(무효 조건): 2024 outcome(2024 결과)을 학습 목표로 쓰거나 feature order(피처 순서), split(분리), label boundary(라벨 경계)가 확인되지 않으면 무효다.",
            "- stop_conditions(중단 조건): 다음 follow-up(후속)이 Monday(월요일) threshold(문턱값)만 깎으면 중단하고 후보군 전체 실험으로 되돌린다.",
            "- evidence_plan(근거 계획): candidate review(후보 검토), negative slice summary(음수 구간 요약), curve diagnostics(곡선 진단), trade records(거래 기록), ledger rows(장부 행).",
            "",
            "## Next Designs(다음 설계)",
            "",
        ]
    )
    for row in next_rows:
        lines.append(f"- `{row['design_id']}`: {row['hypothesis']} Effect(효과): {row['decision_use']}.")
    lines.extend(
        [
            "",
            "## Data and Model Boundary(데이터와 모델 경계)",
            "",
            "- data_source(데이터 원천): run267K MT5(MetaTrader 5, 메타트레이더5) output(출력), run267J stop rules(중단 규칙), run267B 2024 baseline stress(2024 기준 압박).",
            "- time_axis(시간축): FPMarkets US100 M5 broker time(FPMarkets US100 M5 브로커 시간), 2024-01-02부터 2025-01-01 이전까지의 strategy tester(전략 테스터) 결과다.",
            "- sample_scope(표본 범위): Tier A(티어 A) routed total(라우팅 전체) 진단이며 Tier B fallback(티어 B 대체) 사용은 없었다.",
            "- feature_label_boundary(피처/라벨 경계): run267L(267L 실행)은 설계 판정만 하며 새 학습을 하지 않는다.",
            "- split_boundary(분리 경계): 2024 구간은 historical stress(과거 압박) 판독이며 학습 선택 근거로 과장하지 않는다.",
            "- leakage_risk(누수 위험): 다음 run267M(267M 실행)에서 2024 약점 자체를 학습 목표로 쓰면 무효다.",
            "- integrity_judgment(무결성 판정): `usable_with_boundary(경계付き 사용 가능)`.",
            "- model_family(모델군): supervised EBM score table(지도학습 EBM 점수표) 결과를 판정했지만 새 모델을 선택하지 않는다.",
            "- threshold_policy(문턱값 정책): fixed runtime settings(고정 런타임 설정) 비교이며 새 threshold search(문턱값 탐색)는 없다.",
            "- overfit_risk(과적합 위험): Monday(월요일)나 2024-12만 좁게 깎는 수리 루프가 가장 큰 위험이다.",
            "- validation_judgment(검증 판정): `exploratory_prune_to_salvage(탐색적 가지치기와 회수)`.",
            "",
            "## Attribution and Judgment(귀인과 판정)",
            "",
            "- observed_change(관찰 변화): run267K(267K 실행)는 run267I(267I 실행)보다 net/PF/DD(순수익/수익 팩터/손실폭)가 좋아졌지만 trade count(거래 수)가 줄고 Monday(월요일), 2024-12 손실이 깊다.",
            "- likely_drivers(가능한 원인): soft-context supervised retrain(부드러운 문맥 지도 재학습)이 전체 점수 형태는 개선했지만 약한 시간 구간 exposure(노출)를 제어하지 못했다.",
            "- alternative_explanations(대안 설명): 특정 2024 구간에 맞은 우연, 거래 수 축소에 따른 분산, ADX/ATR 계열 feature(피처) 의존 가능성이 있다.",
            "- attribution_confidence(귀인 신뢰도): `medium_with_boundary(경계付き 중간)`.",
            "- result_subject(판정 대상): run267K retrained soft-context branch(267K 재학습 부드러운 문맥 분기).",
            "- evidence_available(있는 근거): MT5 execution(실행), trade records(거래 기록), curve diagnostics(곡선 진단), negative slice summary(음수 구간 요약), run267J stop rules(중단 규칙).",
            "- evidence_missing(없는 근거): 다섯 후보 전체 ablation/replacement(제거/대체), WFO(walk-forward optimization, 워크포워드 최적화), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `exploratory_prune_to_salvage_no_candidate_selection(탐색적 가지치기와 회수, 선택 후보 없음)`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- decision_matrix(결정 행렬): `{rel(DECISION_MATRIX_PATH)}`",
            f"- stop_rule_audit(중단 규칙 감사): `{rel(STOP_AUDIT_PATH)}`",
            f"- next_experiment_design(다음 실험 설계): `{rel(NEXT_EXPERIMENT_PATH)}`",
            f"- validation_receipt(검증 영수증): `{rel(VALIDATION_RECEIPT_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267L_retrained_soft_context_followup_or_prune",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "retrained_soft_context_followup_or_prune",
            "tier_scope": "Tier A diagnostic plus pool-wide next design",
            "scoreboard": "experiment_design",
            "status": STATUS,
            "judgment": "exploratory_prune_to_salvage_no_candidate_selection",
            "evidence_boundary": "design_and_prune_receipt_only_no_candidate_selection_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"decision_rows={len(result['decision_matrix'])};next_design_rows={len(result['next_experiment_design'])};next_action={NEXT_ACTION}.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__retrained_soft_context_followup_or_prune",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "retrained_soft_context_followup_or_prune",
            "parent_run_id": RUN_ID,
            "record_view": "retrained_soft_context_followup_or_prune",
            "tier_scope": "Tier A diagnostic plus pool-wide next design",
            "kpi_scope": "stop_rule_audit_and_next_experiment_design",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": "exploratory_prune_to_salvage_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"decision_rows={len(result['decision_matrix'])};next_design_rows={len(result['next_experiment_design'])}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_applicable_design_only",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_retrained_soft_context_followup_or_prune",
            "status": STATUS,
            "judgment": "exploratory_prune_to_salvage_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267L prunes standalone retrain branch; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    for row in artifact_rows(created_at):
        upsert_csv(
            ARTIFACT_REGISTRY_PATH,
            "artifact_id",
            row,
            ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        )


def update_current_working_state() -> None:
    text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `soft_context_retrain_branch_pruned_to_salvage`")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    evidence_line = f"- Stage267(267단계) run267L retrained soft-context follow-up/prune(재학습 부드러운 문맥 후속/가지치기): `{rel(REPORT_PATH)}`"
    text = append_after_contains(text, "stage267_run267K_retrained_soft_context_adapter_mt5_review.md", evidence_line)
    latest_line = f"- latest_design(최신 설계): run267L(267L 실행) follow-up/prune(후속/가지치기) report(보고서) `{rel(REPORT_PATH)}`."
    text = append_after_contains(text, "latest_materialization(최신 물질화)", latest_line)
    old = "- next_run(다음 실행): `run267L_design_retrained_soft_context_adapter_followup_or_prune`"
    text = text.replace(old, f"- next_run(다음 실행): `{NEXT_ACTION}`")
    text = replace_line_prefix(
        text,
        "- action(행동):",
        " ".join(
            [
                "- action(행동): run267L(267L 실행)는 run267K(267K 실행)의 개선과 약점을 대조해",
                "standalone retrain branch(독립 재학습 분기)를 salvage clue(회수 단서)로 가지치기했다.",
            ]
        ),
    )
    text = replace_line_prefix(
        text,
        "- effect(효과):",
        " ".join(
            [
                "- effect(효과): 다음 작업은 한 구간 미세 수리가 아니라 다섯 Baseline candidates(기준 후보) 전체의",
                "ablation/replacement(제거/대체)와 weak-slice matrix(약한 구간 행렬)로 돌아간다.",
            ]
        ),
    )
    text = replace_line_prefix(
        text,
        "- next_action(다음 행동):",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체)와 weak-slice matrix(약한 구간 행렬)로 되돌아간다.",
    )
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭)가 여전히 불편해 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267J(267J 실행)는 retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계)을 완료했다.\n"
            "Effect(효과): run267I(267I 실행)의 개선을 선택 후보(selected candidate, 선택 후보)로 올리지 않고, 원천 감사와 짧은 중단 규칙으로 다음 run267K(267K 실행)를 제한했다.\n\n"
            "Run267K(267K 실행)는 retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 크게 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), 2024-12 약점이 남아 선택 후보(selected candidate, 선택 후보)는 없다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 standalone candidate(독립 후보)가 아니라 salvage clue(회수 단서)로 가지치기했다.\n"
            f"Effect(효과): 다음 행동(next action, 다음 행동)은 `{NEXT_ACTION}`이고, 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체)와 weak-slice matrix(약한 구간 행렬)로 되돌아간다.\n"
        ),
    )
    write_md(CURRENT_WORKING_STATE_PATH, text)


def update_selection_status() -> None:
    text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    text = append_after_contains(
        text,
        "run267K_retrained_soft_context_adapter_mt5_review",
        f"- run267L_retrained_soft_context_followup_or_prune(267L 재학습 부드러운 문맥 후속/가지치기): `{rel(REPORT_PATH)}`",
    )
    text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267K(267K 실행)는 retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 좋아졌지만 Monday(월요일), 2024-12 약점과 거래 수 축소가 남았다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 standalone candidate(독립 후보)가 아니라 salvage clue(회수 단서)로 가지치기했다.\n"
            f"Effect(효과): selected candidate(선택 후보)는 여전히 없고, next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
        ),
    )
    write_md(SELECTION_STATUS_PATH, text)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    text = append_after_contains(
        text,
        "run267K_retrained_soft_context_adapter_mt5_review",
        f"- run267L_retrained_soft_context_followup_or_prune(267L 재학습 부드러운 문맥 후속/가지치기): `{rel(REPORT_PATH)}`",
    )
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267K(267K 실행)는 retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 좋아졌지만 Monday(월요일), 2024-12 약점과 거래 수 축소가 남았다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 standalone candidate(독립 후보)가 아니라 salvage clue(회수 단서)로 가지치기했다.\n"
            f"Effect(효과): selected candidate(선택 후보)는 여전히 없고, next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
        ),
    )
    write_md(REVIEW_INDEX_PATH, text)


def update_workspace_state() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = text.replace("current_run_id: run267K_stage267_retrained_soft_context_adapter_materialization_v1", f"current_run_id: {RUN_ID}", 1)
    new_focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267L(267L 실행) retrained soft-context follow-up/prune(재학습 부드러운 문맥 후속/가지치기) `{STATUS}`. Effect(효과): run267K(267K 실행)의 순수익 개선 단서는 보존하되 Monday(월요일), 2024-12, trade count(거래 수) 약점 때문에 standalone retrain branch(독립 재학습 분기)는 salvage clue(회수 단서)로 낮추고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in text:
        text = text.replace("current_focus:", new_focus, 1)
    text = text.replace(
        "  Next action(다음 행동)는 `run267L_design_retrained_soft_context_adapter_followup_or_prune`이다. Effect(효과): retrain branch(재학습 분기)를 한 번 더 좁게 수리할지, 아니면 후보군 경주(candidate racing, 후보 경주)로 되돌려 가지치기할지 결정한다.",
        f"  Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체)와 weak-slice matrix(약한 구간 행렬)로 되돌아간다.",
        1,
    )
    text = text.replace(
        "is active_run267K_retrained_soft_context_adapter_mt5_review_completed(267K 재학습 부드러운 문맥 어댑터 MT5 검토 완료 활성).",
        "is active_run267L_retrained_soft_context_followup_or_prune_completed(267L 재학습 부드러운 문맥 후속/가지치기 완료 활성).",
        1,
    )
    text = text.replace("  status: run267K_retrained_soft_context_adapter_mt5_review_completed", f"  status: {STATUS}", 1)
    text = text.replace("  current_run_id: run267K_stage267_retrained_soft_context_adapter_materialization_v1", f"  current_run_id: {RUN_ID}", 1)
    text = text.replace("  last_completed_run_id: run267K_stage267_retrained_soft_context_adapter_materialization_v1", f"  last_completed_run_id: {RUN_ID}", 1)
    text = append_after_contains(
        text,
        "run267K_retrained_soft_context_adapter_mt5_review_path",
        f"  run267L_retrained_soft_context_followup_or_prune_path: {rel(REPORT_PATH)}",
    )
    text = text.replace("  next_action: run267L_design_retrained_soft_context_adapter_followup_or_prune", f"  next_action: {NEXT_ACTION}", 1)
    write_md(WORKSPACE_STATE_PATH, text)


def update_docs() -> None:
    update_current_working_state()
    update_selection_status()
    update_review_index()
    update_workspace_state()


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_docs()
    print(
        json.dumps(
            {
                "status": STATUS,
                "decision_rows": len(result["decision_matrix"]),
                "stop_audit_rows": len(result["stop_rule_audit"]),
                "next_design_rows": len(result["next_experiment_design"]),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
