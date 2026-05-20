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
RUN_ID = "run267J_stage267_retrained_soft_context_adapter_design_v1"
RUN_NUMBER = "run267J"
STATUS = "run267J_retrained_soft_context_adapter_design_completed"
NEXT_ACTION = "run267K_audit_retrain_source_and_materialize_soft_context_p0"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "retrained_soft_context_adapter_design"

RUN267I_ROOT = STAGE_ROOT / "02_runs" / "run267I" / "p0_soft_noncalendar_adapter_materialization"
RUN267H_ROOT = STAGE_ROOT / "02_runs" / "run267H" / "soft_noncalendar_adapter_design"
RUN267B_ROOT = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024"

INPUT_CANDIDATE_REVIEW_PATH = RUN267I_ROOT / "candidate_soft_adapter_review.csv"
INPUT_NEGATIVE_SLICE_PATH = RUN267I_ROOT / "negative_slice_summary.csv"
INPUT_CURVE_DIAGNOSTICS_PATH = RUN267I_ROOT / "curve_diagnostics.csv"
INPUT_REVIEW_RESULT_PATH = RUN267I_ROOT / "review_result.json"
INPUT_RUN267H_QUEUE_PATH = RUN267H_ROOT / "experiment_queue.csv"
INPUT_RUN267B_KPI_PATH = RUN267B_ROOT / "mt5_kpi_summary.csv"

RETRAIN_PROBE_DESIGN_PATH = DESIGN_ROOT / "retrain_probe_design.csv"
WEAKNESS_TARGET_MATRIX_PATH = DESIGN_ROOT / "weakness_target_matrix.csv"
STOP_RULES_PATH = DESIGN_ROOT / "stop_rules.csv"
INTEGRITY_VALIDATION_PLAN_PATH = DESIGN_ROOT / "data_integrity_model_validation_plan.csv"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267J_retrained_soft_context_adapter_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267J_retrained_soft_context_adapter_design.py")

STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

ALIASES = ("s264_aih", "s264_lc")
ALIAS_TO_ID = {
    "s264_aih": "s264_allow_inner_high_quarter",
    "s264_lc": "s264_lowrank_control",
}
ALIAS_ROLE = {
    "s264_aih": "challenger_core(핵심 도전자)",
    "s264_lc": "defensive_control(방어 기준)",
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
        if math.isinf(value):
            return "inf"
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


def fmt(value: Any) -> str:
    number = as_float(value)
    return f"{number:.2f}"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
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
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + suffix


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_section(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker, start + len(start_marker))
    if start == -1 or end == -1:
        return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


def replace_tail_from_marker(text: str, marker: str, replacement: str) -> str:
    start = text.find(marker)
    if start == -1:
        return text.rstrip() + "\n" + replacement.rstrip() + "\n"
    return text[:start].rstrip() + "\n" + replacement.rstrip() + "\n"


def by_alias(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("candidate_alias")): dict(row) for row in rows}


def find_slice(
    rows: Sequence[Mapping[str, str]],
    alias: str,
    axis: str,
    bucket: str,
) -> dict[str, str]:
    for row in rows:
        if row.get("candidate_alias") == alias and row.get("axis") == axis and row.get("bucket") == bucket:
            return dict(row)
    return {}


def build_retrain_design(candidate_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    candidates = by_alias(candidate_rows)
    rows: list[dict[str, Any]] = []
    p0_specs = (
        (
            "run267J_p0_s264_aih_softctx_retrain_core",
            1,
            "s264_aih",
            "softctx_retrain_p0_core(부드러운 문맥 재학습 우선 핵심)",
            "trade_count>=340;net_profit>170;profit_factor>1.10;equity_dd_percent<=28.5;Monday_net>-100;July_net>-80;chron_mid_net>-60",
            "trade_count<330 or net_profit<=run267I or profit_factor<=run267I or equity_dd_percent>=run267I or weak_slice_floors_not_met",
        ),
        (
            "run267J_p0_s264_lc_softctx_retrain_control",
            2,
            "s264_lc",
            "softctx_retrain_p0_defensive_control(부드러운 문맥 재학습 우선 방어 기준)",
            "trade_count>=337;net_profit>=145;profit_factor>=1.09;equity_dd_percent<=29.5;Monday_net>-105;July_net>-85;chron_mid_net>-65",
            "trade_count<325 or net_profit<=run267I or profit_factor<1.08 or equity_dd_percent>=run267I or defensive_control_breaks",
        ),
    )
    for design_id, priority, alias, role, target_gate, failure_gate in p0_specs:
        source = candidates.get(alias, {})
        rows.append(
            {
                "design_id": design_id,
                "priority": priority,
                "candidate_id": ALIAS_TO_ID[alias],
                "candidate_alias": alias,
                "candidate_role": ALIAS_ROLE[alias],
                "source_feature_design": source.get("feature_design", "adx_atr_soft_score"),
                "source_model_materialization_type": source.get(
                    "model_materialization_type",
                    "research_score_table_extension_not_retrained",
                ),
                "source_net_profit": source.get("net_profit"),
                "source_profit_factor": source.get("profit_factor"),
                "source_trade_count": source.get("trade_count"),
                "source_equity_dd_percent": source.get("report_equity_drawdown_percent"),
                "source_weak_month": source.get("weakest_month"),
                "source_weak_month_net": source.get("weakest_month_net"),
                "source_weak_weekday": source.get("weakest_weekday"),
                "source_weak_weekday_net": source.get("weakest_weekday_net"),
                "source_weak_chron": source.get("weakest_chron_segment"),
                "source_weak_chron_net": source.get("weakest_chron_net"),
                "retrain_probe_role": role,
                "materialization_lane": "audit_then_materialize_p0(감사 후 우선 물질화)",
                "feature_engineering_surface": (
                    "stage267_adx_atr_soft_score;adx_20_25_soft_distance;"
                    "atr_14_over_atr_50_z;weak_context_score"
                ),
                "model_training_source_requirement": (
                    "locate_original_training_dataset_feature_order_label_definition_and_split_contract"
                ),
                "label_and_split_requirement": (
                    "do_not_train_from_2024_MT5_profit_or_weak_slice_outcomes;"
                    "2024_is_historical_stress_read_only"
                ),
                "comparison_anchor": "run267I_score_table_extension_not_retrained(267I 점수표 확장, 재학습 아님)",
                "target_gate": target_gate,
                "failure_gate": failure_gate,
                "next_action": "run267K_source_audit_required_before_any_training",
                "claim_boundary": "design_only_no_candidate_selection_no_onnx_readiness",
            }
        )

    hold_specs = (
        (
            "run267J_p1_s264_aih_di_adx_atr_interaction_hold",
            3,
            "s264_aih",
            "di_adx_atr_continuous_interaction(방향성/추세/변동성 연속 상호작용)",
            "hold_until_p0_source_audit_passes(우선 원천 감사 통과 전 보류)",
        ),
        (
            "run267J_p1_s264_lc_di_adx_atr_interaction_hold",
            4,
            "s264_lc",
            "di_adx_atr_continuous_interaction(방향성/추세/변동성 연속 상호작용)",
            "hold_until_p0_source_audit_passes(우선 원천 감사 통과 전 보류)",
        ),
        (
            "run267J_p2_soft_exit_overlay_hold",
            5,
            "s264_aih",
            "soft_exit_overlay_flag(부드러운 청산 덮개 표식)",
            "hold_until_retrained_entry_surface_survives(재학습 진입 표면 생존 전 보류)",
        ),
    )
    for design_id, priority, alias, surface, lane in hold_specs:
        source = candidates.get(alias, {})
        rows.append(
            {
                "design_id": design_id,
                "priority": priority,
                "candidate_id": ALIAS_TO_ID[alias],
                "candidate_alias": alias,
                "candidate_role": ALIAS_ROLE[alias],
                "source_feature_design": source.get("feature_design", "adx_atr_soft_score"),
                "source_model_materialization_type": source.get(
                    "model_materialization_type",
                    "research_score_table_extension_not_retrained",
                ),
                "source_net_profit": source.get("net_profit"),
                "source_profit_factor": source.get("profit_factor"),
                "source_trade_count": source.get("trade_count"),
                "source_equity_dd_percent": source.get("report_equity_drawdown_percent"),
                "source_weak_month": source.get("weakest_month"),
                "source_weak_month_net": source.get("weakest_month_net"),
                "source_weak_weekday": source.get("weakest_weekday"),
                "source_weak_weekday_net": source.get("weakest_weekday_net"),
                "source_weak_chron": source.get("weakest_chron_segment"),
                "source_weak_chron_net": source.get("weakest_chron_net"),
                "retrain_probe_role": "held_followup(보류 후속)",
                "materialization_lane": lane,
                "feature_engineering_surface": surface,
                "model_training_source_requirement": "same_source_audit_as_p0_required",
                "label_and_split_requirement": (
                    "do_not_revive_exact_dilowq33_hard_filter;"
                    "do_not_fit_directly_to_2024_weak_month_or_weekday"
                ),
                "comparison_anchor": "run267I_and_p0_retrain_result_required_before_followup",
                "target_gate": "no_target_until_p0_retrain_result_exists",
                "failure_gate": "blocked_if_p0_retrain_source_unresolved_or_p0_underperforms",
                "next_action": "hold",
                "claim_boundary": "design_hold_no_materialization",
            }
        )
    return rows


def build_weakness_matrix(
    candidate_rows: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    targets = {
        "s264_aih": {
            ("weekday", "Monday"): (-100, 0.75, 25.0),
            ("month", "2024-07"): (-80, 0.75, 23.0),
            ("chron_segment", "chron_mid"): (-60, 0.90, 32.0),
            ("session_report", "session_07_12_report_time"): (-60, 0.50, 16.0),
            ("close_hour_report", "12"): (-30, 0.70, 12.0),
        },
        "s264_lc": {
            ("weekday", "Monday"): (-105, 0.72, 25.0),
            ("month", "2024-07"): (-85, 0.72, 23.0),
            ("chron_segment", "chron_mid"): (-65, 0.88, 32.0),
            ("session_report", "session_07_12_report_time"): (-65, 0.50, 16.0),
            ("close_hour_report", "12"): (-35, 0.70, 12.0),
        },
    }
    rows: list[dict[str, Any]] = []
    for alias in ALIASES:
        for (axis, bucket), (net_floor, pf_floor, dd_ceiling) in targets[alias].items():
            source = find_slice(negative_rows, alias, axis, bucket)
            rows.append(
                {
                    "candidate_alias": alias,
                    "candidate_id": ALIAS_TO_ID[alias],
                    "candidate_role": ALIAS_ROLE[alias],
                    "weakness_axis": axis,
                    "weakness_bucket": bucket,
                    "run267i_trade_count": source.get("trade_count"),
                    "run267i_net_profit": source.get("net_profit"),
                    "run267i_profit_factor": source.get("profit_factor"),
                    "run267i_drawdown": source.get("closed_balance_max_drawdown"),
                    "target_net_floor": net_floor,
                    "target_profit_factor_floor": pf_floor,
                    "target_drawdown_ceiling": dd_ceiling,
                    "target_effect": (
                        "weak_slice_reduction_without_trade_count_collapse"
                        "(거래 수 붕괴 없는 약점 구간 완화)"
                    ),
                    "validation_note": (
                        "use_as_materialization_gate_not_as_training_label"
                        "(물질화 게이트로만 쓰고 학습 라벨로 쓰지 않음)"
                    ),
                }
            )
    return rows


def build_stop_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "J_STOP_01_missing_training_source",
            "gate_type": "source_audit(원천 감사)",
            "trigger": "original_training_dataset_or_feature_order_or_label_split_contract_unresolved",
            "action": "stop_materialization_and_record_blocked",
            "effect": "prevents_fake_true_retrain_claim(가짜 재학습 주장 방지)",
            "claim_boundary": "blocked_no_candidate_selection",
        },
        {
            "rule_id": "J_STOP_02_2024_outcome_fit",
            "gate_type": "data_integrity(데이터 무결성)",
            "trigger": "training_target_uses_2024_MT5_profit_or_weak_slice_outcome",
            "action": "mark_invalid_and_return_to_source_feature_design",
            "effect": "prevents_historical_stress_leakage(과거 압박 누수 방지)",
            "claim_boundary": "invalid_no_materialization",
        },
        {
            "rule_id": "J_STOP_03_p0_underperforms_run267I",
            "gate_type": "model_validation(모델 검증)",
            "trigger": "p0_retrain_net_or_PF_worse_than_run267I_or_DD_worse_or_trade_count_collapses",
            "action": "close_soft_context_branch_after_run267K_review",
            "effect": "prevents_score_table_micro_loop(점수표 미세 반복 방지)",
            "claim_boundary": "negative_result_memory_only",
        },
        {
            "rule_id": "J_STOP_04_weak_slices_not_repaired",
            "gate_type": "time_slice_kpi(시간 구간 핵심 성과 지표)",
            "trigger": "Monday_or_2024_07_or_chron_mid_remains_below_target_floor",
            "action": "do_not_extend_repair_more_than_one_followup_without_new_structure",
            "effect": "prevents_single_slice_bottleneck(한 구간 병목 방지)",
            "claim_boundary": "watch_or_negative_no_selection",
        },
        {
            "rule_id": "J_STOP_05_control_breaks",
            "gate_type": "candidate_pair_control(후보 쌍 기준)",
            "trigger": "s264_aih_improves_but_s264_lc_defensive_control_breaks_badly",
            "action": "keep_s264_aih_as_scout_only_and_do_not_promote_group",
            "effect": "separates_challenger_from_robust_candidate(도전자와 견고 후보 분리)",
            "claim_boundary": "scout_only",
        },
        {
            "rule_id": "J_STOP_06_feature_order_or_runtime_mapping_unresolved",
            "gate_type": "runtime_parity_precheck(런타임 동등성 사전 점검)",
            "trigger": "feature_order_decision_surface_or_risk_ATR_handoff_cannot_be_traced",
            "action": "block_MT5_materialization_until_mapping_is_written",
            "effect": "prevents_untraceable_adapter_surface(추적 불가 어댑터 표면 방지)",
            "claim_boundary": "no_runtime_reproduction_claim",
        },
        {
            "rule_id": "J_STOP_07_curve_shape_not_clean",
            "gate_type": "curve_quality(곡선 품질)",
            "trigger": "balance_equity_curve_has_deep_local_hole_even_if_summary_KPI_improves",
            "action": "reject_as_ONNX_review_input",
            "effect": "keeps_graph_quality_ahead_of_single_KPI(단일 지표보다 곡선 품질 우선)",
            "claim_boundary": "no_onnx_readiness",
        },
        {
            "rule_id": "J_STOP_08_exact_dilowq33_hard_filter",
            "gate_type": "failure_memory(실패 기억)",
            "trigger": "proposal_revives_exact_DI_low_q33_hard_filter",
            "action": "keep_blocked_unless_new_continuous_interaction_evidence_exists",
            "effect": "uses_prior_failure_memory_without_freezing_exploration(실패 기억을 쓰되 탐색은 막지 않음)",
            "claim_boundary": "blocked_variant",
        },
    ]


def build_integrity_validation_plan() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "J_DATA_01_input_hashes",
            "check_family": "artifact_lineage(산출물 계보)",
            "requirement": "hash_run267I_review_inputs_and_run267H_design_queue",
            "evidence_source": "candidate_review;negative_slice_summary;curve_diagnostics;run267H_experiment_queue",
            "pass_condition": "all_required_inputs_exist_with_sha256",
            "failure_action": "record_missing_required_before_run267K",
            "effect": "keeps_design_tied_to_actual_prior_outputs(설계를 실제 이전 산출물에 연결)",
        },
        {
            "check_id": "J_DATA_02_time_axis",
            "check_family": "data_integrity(데이터 무결성)",
            "requirement": "report_time_axis_is_broker_or_server_report_time_until_audit_says_otherwise",
            "evidence_source": "run267I_trade_records_and_MT5_reports",
            "pass_condition": "time_slice_labels_are_not_reinterpreted_as_UTC",
            "failure_action": "rename_or_recompute_time_slices",
            "effect": "prevents_wrong_session_read(잘못된 세션 해석 방지)",
        },
        {
            "check_id": "J_DATA_03_split_boundary",
            "check_family": "data_integrity(데이터 무결성)",
            "requirement": "2024_historical_stress_is_not_used_as_OOS_or_training_target",
            "evidence_source": "run267B_and_run267I_manifests",
            "pass_condition": "2024_role_written_as_train_era_stress_read_only",
            "failure_action": "mark_invalid",
            "effect": "prevents_split_boundary_drift(스플릿 경계 흔들림 방지)",
        },
        {
            "check_id": "J_DATA_04_feature_label_boundary",
            "check_family": "data_integrity(데이터 무결성)",
            "requirement": "soft_context_features_must_be_available_at_decision_time",
            "evidence_source": "feature_manifest_and_runtime_feature_inputs",
            "pass_condition": "no_future_trade_result_or_close_outcome_in_feature",
            "failure_action": "remove_feature_or_block_retrain",
            "effect": "prevents_feature_label_leakage(피처/라벨 누수 방지)",
        },
        {
            "check_id": "J_MODEL_01_model_family_resolution",
            "check_family": "model_validation(모델 검증)",
            "requirement": "resolve_whether_source_is_EBM_GAM_or_score_table_rule_before_training",
            "evidence_source": "source_model_manifest_and_training_scripts",
            "pass_condition": "model_family_and_exporter_are_named",
            "failure_action": "do_not_claim_true_retrain",
            "effect": "keeps_retraining_claim_precise(재학습 주장을 정확히 유지)",
        },
        {
            "check_id": "J_MODEL_02_target_label",
            "check_family": "model_validation(모델 검증)",
            "requirement": "use_original_label_definition_not_2024_profit",
            "evidence_source": "training_label_split_contract",
            "pass_condition": "label_name_label_horizon_and_split_version_are_recorded",
            "failure_action": "block_training",
            "effect": "prevents_outcome_chasing(결과 맞추기 방지)",
        },
        {
            "check_id": "J_MODEL_03_threshold_policy",
            "check_family": "model_validation(모델 검증)",
            "requirement": "keep_thresholds_0_54_and_0_52_unless_change_is_explicitly_materialized",
            "evidence_source": "run267I_set_files_and_materialization_manifest",
            "pass_condition": "threshold_change_is_none_or_separate_variant",
            "failure_action": "split_variant_and_record_delta",
            "effect": "prevents_hidden_threshold_tuning(숨은 임계값 튜닝 방지)",
        },
        {
            "check_id": "J_MODEL_04_calibration_boundary",
            "check_family": "model_validation(모델 검증)",
            "requirement": "score_table_scores_are_not_claimed_as_probabilities_without_calibration",
            "evidence_source": "model_export_manifest",
            "pass_condition": "score_semantics_are_written",
            "failure_action": "downgrade_claim_to_rank_score",
            "effect": "prevents_probability_overclaim(확률 과장 방지)",
        },
        {
            "check_id": "J_MODEL_05_overfit_guard",
            "check_family": "experiment_design(실험 설계)",
            "requirement": "weak_slices_define_evaluation_targets_not_training_objective",
            "evidence_source": "weakness_target_matrix",
            "pass_condition": "no direct optimization on Monday_or_July_profit",
            "failure_action": "mark_overfit_risk_high_and_stop",
            "effect": "keeps_research_from_single_slice_fitting(단일 구간 맞춤 방지)",
        },
        {
            "check_id": "J_RUNTIME_01_handoff_trace",
            "check_family": "runtime_parity_precheck(런타임 동등성 사전 점검)",
            "requirement": "feature_order_decision_surface_risk_ATR_and_model_bundle_hashes_are_traceable",
            "evidence_source": "run267K_materialization_manifest",
            "pass_condition": "MT5_set_ini_model_feature_manifest_hashes_match",
            "failure_action": "block_MT5_reproduction_claim",
            "effect": "prepares_adapter_without_claiming_runtime_authority(런타임 권위 주장 없이 어댑터 준비)",
        },
    ]


def input_lineage() -> list[dict[str, Any]]:
    inputs = (
        ("run267I_candidate_review", INPUT_CANDIDATE_REVIEW_PATH),
        ("run267I_negative_slice_summary", INPUT_NEGATIVE_SLICE_PATH),
        ("run267I_curve_diagnostics", INPUT_CURVE_DIAGNOSTICS_PATH),
        ("run267I_review_result", INPUT_REVIEW_RESULT_PATH),
        ("run267H_experiment_queue", INPUT_RUN267H_QUEUE_PATH),
        ("run267B_2024_kpi_summary", INPUT_RUN267B_KPI_PATH),
    )
    rows: list[dict[str, Any]] = []
    for artifact_id, path in inputs:
        rows.append(
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            }
        )
    return rows


def report_markdown(result: Mapping[str, Any]) -> str:
    design_rows = result["retrain_probe_design"]
    weakness_rows = result["weakness_target_matrix"]
    stop_rows = result["stop_rules"]
    lines = [
        "# Stage267 Run267J Retrained Soft-Context Adapter Design(267단계 267J 재학습 부드러운 문맥 어댑터 설계)",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "- action(행동): run267I(267I 실행)의 `adx_atr_soft_score` 결과를 true retrain(진짜 재학습) 후보로 바로 부르지 않고, 원천 감사(source audit, 원천 감사), 약점 목표, 중단 규칙으로 다시 설계했다.",
        "- effect(효과): Stage58 이후 쌓인 model/source/score-table 연구를 다음 실행에서 실제로 확인할 수 있게 만들고, 점수표 확장(score-table extension, 점수표 확장) 반복을 길게 끌지 않는다.",
        "- judgment(판정): design completed(설계 완료)이다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.",
        "",
        "## Run267I Input Read(267I 입력 판독)",
        "",
        "| candidate(후보) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | weak month(약한 월) | weak weekday(약한 요일) | weak chron(약한 순서 구간) |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in design_rows[:2]:
        lines.append(
            "| `{candidate_alias}` | {net} | {pf} | {trades} | {dd} | `{month}` {month_net} | `{weekday}` {weekday_net} | `{chron}` {chron_net} |".format(
                candidate_alias=row["candidate_alias"],
                net=fmt(row["source_net_profit"]),
                pf=row["source_profit_factor"],
                trades=row["source_trade_count"],
                dd=fmt(row["source_equity_dd_percent"]),
                month=row["source_weak_month"],
                month_net=fmt(row["source_weak_month_net"]),
                weekday=row["source_weak_weekday"],
                weekday_net=fmt(row["source_weak_weekday_net"]),
                chron=row["source_weak_chron"],
                chron_net=fmt(row["source_weak_chron_net"]),
            )
        )
    lines.extend(
        [
            "",
            "## Retrain Probe Design(재학습 탐침 설계)",
            "",
            "| priority(우선순위) | design_id(설계 ID) | lane(진행선) | target gate(목표 게이트) |",
            "|---:|---|---|---|",
        ]
    )
    for row in design_rows:
        lines.append(
            f"| {row['priority']} | `{row['design_id']}` | {row['materialization_lane']} | `{row['target_gate']}` |"
        )
    lines.extend(
        [
            "",
            "## Weakness Targets(약점 목표)",
            "",
            "| candidate(후보) | axis(축) | bucket(구간) | run267I net(267I 순수익) | target floor(목표 하한) |",
            "|---|---|---|---:|---:|",
        ]
    )
    for row in weakness_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['weakness_axis']}` | `{row['weakness_bucket']}` | {fmt(row['run267i_net_profit'])} | {fmt(row['target_net_floor'])} |"
        )
    lines.extend(
        [
            "",
            "## Stop Rules(중단 규칙)",
            "",
            "| rule(규칙) | trigger(조건) | action(행동) | effect(효과) |",
            "|---|---|---|---|",
        ]
    )
    for row in stop_rows:
        lines.append(f"| `{row['rule_id']}` | {row['trigger']} | {row['action']} | {row['effect']} |")
    lines.extend(
        [
            "",
            "## Data And Model Gates(데이터와 모델 게이트)",
            "",
            "- data integrity(데이터 무결성): 2024년 MT5(MetaTrader 5, 메타트레이더5) 손익, 약한 월, 약한 요일을 학습 라벨로 쓰지 않는다.",
            "- model validation(모델 검증): 원래 label(라벨), split(스플릿), feature order(피처 순서), model family(모델군)를 찾기 전에는 true retrain(진짜 재학습)을 주장하지 않는다.",
            "- runtime parity precheck(런타임 동등성 사전 점검): feature order(피처 순서), decision surface(결정 표면), risk/ATR(위험/ATR), bundle hash(번들 해시)가 이어져야 MT5 reproduction(MT5 재현)을 시도한다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- retrain_probe_design(재학습 탐침 설계): `{rel(RETRAIN_PROBE_DESIGN_PATH)}`",
            f"- weakness_target_matrix(약점 목표 행렬): `{rel(WEAKNESS_TARGET_MATRIX_PATH)}`",
            f"- stop_rules(중단 규칙): `{rel(STOP_RULES_PATH)}`",
            f"- data_integrity_model_validation_plan(데이터 무결성 모델 검증 계획): `{rel(INTEGRITY_VALIDATION_PLAN_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
            f"- result(결과): `{rel(RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267J_retrained_soft_context_adapter_design`.",
            "- judgment_label(판정 라벨): `design_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    stage_row = {
        "row_id": "stage267_run267J_retrained_soft_context_adapter_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "retrained_soft_context_adapter_design",
        "tier_scope": "Tier A and Tier A+B historical 2024 design",
        "scoreboard": "experiment_design_source_audit_plan",
        "status": STATUS,
        "judgment": "design_completed_no_candidate_selection",
        "evidence_boundary": "design_and_source_audit_plan_only_no_materialization_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": (
            f"design_rows={len(result['retrain_probe_design'])};"
            f"weakness_targets={len(result['weakness_target_matrix'])};"
            f"stop_rules={len(result['stop_rules'])};next_action={NEXT_ACTION}."
        ),
    }
    rows = [item for item in read_csv(STAGE_LEDGER_PATH) if item.get("row_id") != stage_row["row_id"]]
    rows.append(stage_row)
    write_csv(
        STAGE_LEDGER_PATH,
        rows,
        (
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
        ),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_retrained_soft_context_adapter_design",
            "status": STATUS,
            "judgment": "design_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": (
                "Run267J true retrain source-audit design; selected_candidate=none; "
                f"onnx_readiness=not_claimed; next_action={NEXT_ACTION}."
            ),
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__retrained_soft_context_adapter_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "retrained_soft_context_adapter_design",
            "parent_run_id": RUN_ID,
            "record_view": "retrained_soft_context_adapter_design",
            "tier_scope": "Tier A and Tier A+B historical 2024 design",
            "kpi_scope": "design_weakness_targets_stop_rules_source_audit",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": "design_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": (
                f"design_rows={len(result['retrain_probe_design'])};"
                f"weakness_targets={len(result['weakness_target_matrix'])};"
                f"stop_rules={len(result['stop_rules'])}"
            ),
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_required_design_only",
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
    entries = (
        ("stage267_run267J_retrain_design_script", "producer_script", PRODUCER_PATH, "Builds run267J retrained soft-context Adapter design."),
        ("stage267_run267J_retrain_probe_design", "retrain_probe_design", RETRAIN_PROBE_DESIGN_PATH, "Run267J retrain probe design queue."),
        ("stage267_run267J_weakness_target_matrix", "weakness_target_matrix", WEAKNESS_TARGET_MATRIX_PATH, "Run267J weak-slice target gates."),
        ("stage267_run267J_stop_rules", "stop_rules", STOP_RULES_PATH, "Run267J stop rules for source audit and materialization."),
        ("stage267_run267J_integrity_validation_plan", "data_integrity_model_validation_plan", INTEGRITY_VALIDATION_PLAN_PATH, "Run267J data/model validation gates."),
        ("stage267_run267J_lineage", "lineage", LINEAGE_PATH, "Run267J input and output lineage."),
        ("stage267_run267J_result", "result", RESULT_PATH, "Run267J design JSON payload."),
        ("stage267_run267J_report", "review_report", REPORT_PATH, "User-facing run267J retrained soft-context design report."),
    )
    registry_rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
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
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_working_state() -> None:
    text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(
        text,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `soft_context_retrain_source_audit_design`",
    )
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    report_line = (
        f"- Stage267(267단계) run267J retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계): `{rel(REPORT_PATH)}`"
    )
    text = append_after_contains(text, "stage267_run267I_soft_noncalendar_adapter_mt5_review.md", report_line)
    replacement = "\n".join(
        [
            "## Current Next Action(현재 다음 행동)",
            f"- latest_design(최신 설계): `{rel(REPORT_PATH)}`.",
            "",
            f"- next_run(다음 실행): `{NEXT_ACTION}`",
            "- action(행동): run267J(267J 실행)는 run267I(267I 실행)의 점수표 확장 결과를 true retrain(진짜 재학습) 후보로 바로 부르지 않고 source audit(원천 감사), weakness target(약점 목표), stop rule(중단 규칙)로 재설계했다.",
            "- effect(효과): Stage58 이후 이어진 model/source/score-table 연구를 다음 실행에서 확인할 수 있게 만들고, Monday(월요일), July(7월), chron_mid(중간 순서 구간), DD(drawdown, 손실폭)를 명시 게이트로 둔다.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 원천 데이터, label(라벨), split(스플릿), feature order(피처 순서)가 확인될 때만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다.",
        ]
    )
    text = replace_section(text, "## Current Next Action(현재 다음 행동)", "Forbidden claims(금지 주장):", replacement)
    summary_tail = (
        "Run267I(267I 실행)는 P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토)를 완료했다.\n"
        "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭)가 여전히 불편해 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
        "Run267J(267J 실행)는 retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계)을 완료했다.\n"
        "Effect(효과): run267I(267I 실행)의 개선을 선택 후보(selected candidate, 선택 후보)로 올리지 않고, 원천 감사와 짧은 중단 규칙으로 다음 run267K(267K 실행)를 제한한다."
    )
    text = replace_tail_from_marker(text, "Run267I(267I 실행)는", summary_tail)
    write_md(CURRENT_WORKING_STATE_PATH, text)


def update_selection_status() -> None:
    text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    report_line = (
        f"- run267J_retrained_soft_context_adapter_design(267J 재학습 부드러운 문맥 어댑터 설계): `{rel(REPORT_PATH)}`"
    )
    text = append_after_contains(text, "run267I_soft_noncalendar_adapter_mt5_review", report_line)
    text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    old_next = (
        "Next action(다음 행동): `run267J_design_retrained_soft_context_adapter_probe_with_stop_rules`. "
        "Effect(효과): score-table extension(점수표 확장) 반복을 막고, true retrain(진짜 재학습) "
        "soft-context Adapter probe(부드러운 문맥 어댑터 탐침)를 설계하거나 짧은 stop rule(중단 규칙)로 분기를 닫는다."
    )
    new_next = (
        f"Next action(다음 행동): `{NEXT_ACTION}`. Effect(효과): source audit(원천 감사)에서 "
        "label(라벨), split(스플릿), feature order(피처 순서)가 확인될 때만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다."
    )
    text = text.replace(old_next, new_next)
    summary_tail = (
        "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
        "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
        "Run267J(267J 실행)는 retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계)을 완료했다.\n"
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 여전히 없고, run267K(267K 실행)는 원천 감사 통과 없이는 물질화하지 않는다.\n"
        f"Next action(다음 행동): `{NEXT_ACTION}`. Effect(효과): source audit(원천 감사)에서 label(라벨), split(스플릿), feature order(피처 순서)가 확인될 때만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다."
    )
    text = replace_tail_from_marker(text, "Run267I(267I 실행)는", summary_tail)
    write_md(SELECTION_STATUS_PATH, text)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    report_line = (
        f"- run267J_retrained_soft_context_adapter_design(267J 재학습 부드러운 문맥 어댑터 설계): `{rel(REPORT_PATH)}`"
    )
    text = append_after_contains(text, "run267I_soft_noncalendar_adapter_mt5_review", report_line)
    old_next = (
        "Next action(다음 행동): `run267J_design_retrained_soft_context_adapter_probe_with_stop_rules`. "
        "Effect(효과): score-table extension(점수표 확장) 반복을 막고, true retrain(진짜 재학습) "
        "soft-context Adapter probe(부드러운 문맥 어댑터 탐침)를 설계하거나 짧은 stop rule(중단 규칙)로 분기를 닫는다."
    )
    new_next = (
        f"Next action(다음 행동): `{NEXT_ACTION}`. Effect(효과): source audit(원천 감사)에서 "
        "label(라벨), split(스플릿), feature order(피처 순서)가 확인될 때만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다."
    )
    text = text.replace(old_next, new_next)
    summary_tail = (
        "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
        "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
        "Run267J(267J 실행)는 retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계)을 완료했다.\n"
        "Effect(효과): run267I(267I 실행)의 약점과 이전 연구를 run267K(267K 실행)의 원천 감사 및 중단 규칙으로 연결한다.\n"
        f"Next action(다음 행동): `{NEXT_ACTION}`. Effect(효과): source audit(원천 감사)에서 label(라벨), split(스플릿), feature order(피처 순서)가 확인될 때만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다."
    )
    text = replace_tail_from_marker(text, "Run267I(267I 실행)는", summary_tail)
    write_md(REVIEW_INDEX_PATH, text)


def update_workspace_state() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = text.replace(
        "current_run_id: run267I_stage267_p0_soft_noncalendar_adapter_materialization_v1",
        f"current_run_id: {RUN_ID}",
        1,
    )
    new_focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267J(267J 실행) retrained soft-context Adapter design(재학습 부드러운 문맥 어댑터 설계) `{STATUS}`. Effect(효과): run267I(267I 실행)의 점수표 확장 결과를 source audit(원천 감사), weakness target(약점 목표), stop rule(중단 규칙)로 연결했고 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in text:
        text = text.replace("current_focus:", new_focus, 1)
    old_next = (
        "  Next action(다음 행동)는 `run267J_design_retrained_soft_context_adapter_probe_with_stop_rules`이다. "
        "Effect(효과): score-table extension(점수표 확장) 반복을 막고 true retrain(진짜 재학습) "
        "soft-context Adapter probe(부드러운 문맥 어댑터 탐침)를 설계하거나 짧은 stop rule(중단 규칙)로 분기를 닫는다."
    )
    new_next = (
        f"  Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): source audit(원천 감사)에서 "
        "label(라벨), split(스플릿), feature order(피처 순서)를 확인한 뒤에만 P0 soft-context Adapter(우선 부드러운 문맥 어댑터)를 물질화한다."
    )
    text = text.replace(old_next, new_next, 1)
    text = text.replace(
        "  status: run267I_p0_soft_noncalendar_adapter_mt5_review_completed",
        f"  status: {STATUS}",
        1,
    )
    text = text.replace(
        "  next_action: run267J_design_retrained_soft_context_adapter_probe_with_stop_rules",
        f"  next_action: {NEXT_ACTION}",
        1,
    )
    text = append_after_contains(
        text,
        "run267I_soft_noncalendar_adapter_mt5_review_path",
        f"  run267J_retrained_soft_context_adapter_design_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, text)


def update_docs() -> None:
    update_current_working_state()
    update_selection_status()
    update_review_index()
    update_workspace_state()


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    candidate_rows = read_csv(INPUT_CANDIDATE_REVIEW_PATH)
    negative_rows = read_csv(INPUT_NEGATIVE_SLICE_PATH)
    retrain_design = build_retrain_design(candidate_rows)
    weakness_matrix = build_weakness_matrix(candidate_rows, negative_rows)
    stop_rules = build_stop_rules()
    integrity_validation_plan = build_integrity_validation_plan()
    lineage = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "inputs": input_lineage(),
        "outputs": {
            "retrain_probe_design": rel(RETRAIN_PROBE_DESIGN_PATH),
            "weakness_target_matrix": rel(WEAKNESS_TARGET_MATRIX_PATH),
            "stop_rules": rel(STOP_RULES_PATH),
            "data_integrity_model_validation_plan": rel(INTEGRITY_VALIDATION_PLAN_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "source_boundary": (
            "run267J_is_design_only;run267K_must_audit_training_source_before_materialization"
        ),
    }
    result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_candidate_review_rows": len(candidate_rows),
        "source_negative_slice_rows": len(negative_rows),
        "retrain_probe_design": retrain_design,
        "weakness_target_matrix": weakness_matrix,
        "stop_rules": stop_rules,
        "data_integrity_model_validation_plan": integrity_validation_plan,
        "lineage": lineage,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": lineage["outputs"],
    }
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        RETRAIN_PROBE_DESIGN_PATH,
        result["retrain_probe_design"],
        (
            "design_id",
            "priority",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_feature_design",
            "source_model_materialization_type",
            "source_net_profit",
            "source_profit_factor",
            "source_trade_count",
            "source_equity_dd_percent",
            "source_weak_month",
            "source_weak_month_net",
            "source_weak_weekday",
            "source_weak_weekday_net",
            "source_weak_chron",
            "source_weak_chron_net",
            "retrain_probe_role",
            "materialization_lane",
            "feature_engineering_surface",
            "model_training_source_requirement",
            "label_and_split_requirement",
            "comparison_anchor",
            "target_gate",
            "failure_gate",
            "next_action",
            "claim_boundary",
        ),
    )
    write_csv(
        WEAKNESS_TARGET_MATRIX_PATH,
        result["weakness_target_matrix"],
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "weakness_axis",
            "weakness_bucket",
            "run267i_trade_count",
            "run267i_net_profit",
            "run267i_profit_factor",
            "run267i_drawdown",
            "target_net_floor",
            "target_profit_factor_floor",
            "target_drawdown_ceiling",
            "target_effect",
            "validation_note",
        ),
    )
    write_csv(
        STOP_RULES_PATH,
        result["stop_rules"],
        ("rule_id", "gate_type", "trigger", "action", "effect", "claim_boundary"),
    )
    write_csv(
        INTEGRITY_VALIDATION_PLAN_PATH,
        result["data_integrity_model_validation_plan"],
        ("check_id", "check_family", "requirement", "evidence_source", "pass_condition", "failure_action", "effect"),
    )
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(str(result["created_at_utc"]), result)
    update_docs()
    print(
        json.dumps(
            {
                "status": result["status"],
                "design_rows": len(result["retrain_probe_design"]),
                "weakness_targets": len(result["weakness_target_matrix"]),
                "stop_rules": len(result["stop_rules"]),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
