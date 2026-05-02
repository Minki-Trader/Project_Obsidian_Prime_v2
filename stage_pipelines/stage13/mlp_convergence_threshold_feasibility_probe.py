from __future__ import annotations

import argparse
import json
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
from sklearn.exceptions import ConvergenceWarning

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    execute_prepared_run,
)
from foundation.models.mlp_characteristics import MlpVariantSpec, fit_mlp_variant, probability_frame, probability_shape_metrics
from foundation.models.mlp_convergence_thresholds import (
    representative_threshold_rows,
    routed_threshold_feasibility_table,
    threshold_feasibility_table,
    threshold_summary,
    training_history_summary,
    training_history_table,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage13.mlp_convergence_threshold_docs import (
    report_markdown,
    sync_docs,
    work_packet_markdown,
    write_text_bom,
)
from stage_pipelines.stage13.mlp_handoff_support import (
    Stage13HandoffConfig,
    copy_runtime_inputs,
    export_feature_matrices,
    load_context,
    make_no_trade_attempts,
    materialize_models,
    rel,
    write_runtime_probability_artifacts,
)


STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04D"
RUN_ID = "run04D_mlp_convergence_threshold_feasibility_probe_v1"
PACKET_ID = "stage13_run04D_mlp_convergence_threshold_feasibility_probe_packet_v1"
EXPLORATION_LABEL = "stage13_MLPConvergence__ThresholdFeasibility"
MODEL_FAMILY = "sklearn_mlpclassifier_convergence_threshold_probe"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_run_baseline_seed_or_reference"
BOUNDARY = "convergence_threshold_feasibility_probe_not_alpha_quality_not_promotion_not_runtime_authority"
RUNTIME_PROBABILITY_BOUNDARY = "runtime_probability_proxy_for_no_trade_handoff_only"
NO_TRADE_THRESHOLD = 1.01
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 9
QUANTILES = (0.70, 0.80, 0.90, 0.95, 0.97, 0.99)
MARGINS = (0.0, 0.03, 0.06)
REPRESENTATIVE_THRESHOLD_ID = "q90_m000"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04D_mlp_convergence_threshold_feasibility_probe_packet.md"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def convergence_threshold_spec() -> MlpVariantSpec:
    return MlpVariantSpec(
        variant_id="convergence_threshold_relu64_l2",
        idea_id="relu_convergence_threshold_shape",
        description="Single-hidden-layer ReLU MLP used to inspect convergence curve and threshold-density feasibility.",
        hidden_layer_sizes=(64,),
        activation="relu",
        alpha=0.001,
        learning_rate_init=0.001,
        max_iter=180,
        n_iter_no_change=12,
        validation_fraction=0.12,
        random_state=1517,
    )


def fit_with_warning_capture(frame: pd.DataFrame, feature_order: Sequence[str], spec: MlpVariantSpec) -> tuple[Any, list[str]]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model = fit_mlp_variant(frame, feature_order, spec)
    messages = [str(item.message) for item in caught if issubclass(item.category, ConvergenceWarning)]
    return model, messages


def write_convergence_artifacts(
    *,
    tier_a_model: Any,
    tier_b_model: Any,
    tier_a_warnings: Sequence[str],
    tier_b_warnings: Sequence[str],
) -> dict[str, Any]:
    root = RUN_ROOT / "convergence"
    io_path(root).mkdir(parents=True, exist_ok=True)
    history = pd.concat(
        [
            training_history_table(tier_a_model, scope=mt5.TIER_A, warning_messages=tier_a_warnings),
            training_history_table(tier_b_model, scope=mt5.TIER_B, warning_messages=tier_b_warnings),
        ],
        ignore_index=True,
    )
    summary_rows = [
        training_history_summary(tier_a_model, scope=mt5.TIER_A, warning_messages=tier_a_warnings),
        training_history_summary(tier_b_model, scope=mt5.TIER_B, warning_messages=tier_b_warnings),
    ]
    history_path = root / "training_history.csv"
    summary_csv = root / "training_history_summary.csv"
    summary_json = root / "training_history_summary.json"
    history.to_csv(io_path(history_path), index=False, encoding="utf-8")
    pd.DataFrame(summary_rows).to_csv(io_path(summary_csv), index=False, encoding="utf-8")
    payload = {
        "rows": summary_rows,
        "boundary": "convergence_curve_only_not_model_quality",
        "loss_curve_source": "sklearn MLPClassifier.loss_curve_",
        "validation_score_source": "sklearn MLPClassifier.validation_scores_",
    }
    write_json(summary_json, payload)
    return {
        "training_history_csv": {"path": rel(history_path), "rows": len(history), "sha256": sha256_file_lf_normalized(history_path)},
        "training_history_summary_csv": {"path": rel(summary_csv), "rows": len(summary_rows), "sha256": sha256_file_lf_normalized(summary_csv)},
        "training_history_summary_json": {"path": rel(summary_json), "rows": len(summary_rows), "sha256": sha256_file_lf_normalized(summary_json)},
        "payload": payload,
    }


def write_threshold_artifacts(*, tier_a_model: Any, tier_b_model: Any, context: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "thresholds"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["tier_a_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_fallback_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    detail = pd.concat(
        [
            threshold_feasibility_table(tier_a_prob, scope=mt5.TIER_A, quantiles=QUANTILES, margins=MARGINS),
            threshold_feasibility_table(tier_b_prob, scope=mt5.TIER_B, quantiles=QUANTILES, margins=MARGINS),
            routed_threshold_feasibility_table(
                tier_a_prob_frame=tier_a_prob,
                tier_b_fallback_prob_frame=tier_b_fallback_prob,
                scope=mt5.TIER_AB,
                quantiles=QUANTILES,
                margins=MARGINS,
            ),
        ],
        ignore_index=True,
    )
    summary_frame = threshold_summary(detail)
    representative = representative_threshold_rows(summary_frame, REPRESENTATIVE_THRESHOLD_ID)
    shape_payload = {
        "tier_a": probability_shape_metrics(tier_a_prob),
        "tier_b": probability_shape_metrics(tier_b_prob),
        "tier_b_fallback": probability_shape_metrics(tier_b_fallback_prob),
        "boundary": "probability_shape_and_threshold_density_only",
    }
    return _write_threshold_payloads(root, detail, summary_frame, representative, shape_payload)


def _write_threshold_payloads(
    root: Path,
    detail: pd.DataFrame,
    summary_frame: pd.DataFrame,
    representative: pd.DataFrame,
    shape_payload: Mapping[str, Any],
) -> dict[str, Any]:
    detail_path = root / "threshold_feasibility_detail.csv"
    summary_path = root / "threshold_feasibility_summary.csv"
    representative_path = root / "representative_threshold_rows.csv"
    shape_path = root / "probability_shape_summary.json"
    payload_path = root / "threshold_feasibility_summary.json"
    detail.to_csv(io_path(detail_path), index=False, encoding="utf-8")
    summary_frame.to_csv(io_path(summary_path), index=False, encoding="utf-8")
    representative.to_csv(io_path(representative_path), index=False, encoding="utf-8")
    write_json(shape_path, shape_payload)
    payload = {
        "representative_threshold_id": REPRESENTATIVE_THRESHOLD_ID,
        "representative_rows": representative.to_dict(orient="records"),
        "density_label_counts": summary_frame["density_label"].value_counts(dropna=False).to_dict(),
        "boundary": "threshold_density_feasibility_only_not_threshold_selection",
    }
    write_json(payload_path, payload)
    return {
        "threshold_feasibility_detail_csv": {"path": rel(detail_path), "rows": len(detail), "sha256": sha256_file_lf_normalized(detail_path)},
        "threshold_feasibility_summary_csv": {"path": rel(summary_path), "rows": len(summary_frame), "sha256": sha256_file_lf_normalized(summary_path)},
        "representative_threshold_rows_csv": {"path": rel(representative_path), "rows": len(representative), "sha256": sha256_file_lf_normalized(representative_path)},
        "probability_shape_summary_json": {"path": rel(shape_path), "rows": 1, "sha256": sha256_file_lf_normalized(shape_path)},
        "threshold_feasibility_summary_json": {"path": rel(payload_path), "rows": 1, "sha256": sha256_file_lf_normalized(payload_path)},
        "payload": payload,
        "shape_payload": shape_payload,
    }


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "blocked_materialize_only_no_mt5_execution",
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "blocked_convergence_threshold_feasibility_probe",
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    result["judgment"] = (
        "inconclusive_convergence_threshold_feasibility_probe_completed"
        if result.get("external_verification_status") == "completed"
        else "blocked_convergence_threshold_feasibility_probe"
    )
    return result


def convergence_ledger_rows(convergence_artifacts: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in convergence_artifacts["payload"]["rows"]:
        scope = str(row["scope"])
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__python_convergence_{scope_slug(scope)}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"python_convergence_{scope_slug(scope)}",
                "parent_run_id": RUN_ID,
                "record_view": f"python_convergence_{scope_slug(scope)}",
                "tier_scope": scope,
                "kpi_scope": "mlp_convergence_diagnostics",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": "inconclusive_convergence_diagnostic",
                "path": convergence_artifacts["training_history_summary_json"]["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("n_iter", row.get("n_iter")),
                        ("max_iter", row.get("max_iter")),
                        ("loss_first", row.get("loss_first")),
                        ("loss_last", row.get("loss_last")),
                        ("loss_drop_ratio", row.get("loss_drop_ratio")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("validation_best", row.get("validation_score_best")),
                        ("validation_gap_last", row.get("validation_best_gap_last")),
                        ("warning_count", row.get("warning_count")),
                        ("label", row.get("convergence_label")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": "Python MLP convergence curve only; not model quality or trading evidence.",
            }
        )
    return rows


def threshold_ledger_rows(threshold_artifacts: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in threshold_artifacts["payload"]["representative_rows"]:
        scope = str(row["scope"])
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__python_threshold_feasibility_{scope_slug(scope)}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"python_threshold_feasibility_{scope_slug(scope)}",
                "parent_run_id": RUN_ID,
                "record_view": f"python_threshold_feasibility_{scope_slug(scope)}",
                "tier_scope": scope,
                "kpi_scope": "threshold_density_feasibility",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": "inconclusive_threshold_density_feasibility",
                "path": threshold_artifacts["threshold_feasibility_summary_json"]["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("threshold_id", row.get("threshold_id")),
                        ("validation_signals", row.get("validation_signal_count")),
                        ("validation_coverage", row.get("validation_signal_coverage")),
                        ("oos_signals", row.get("oos_signal_count")),
                        ("oos_coverage", row.get("oos_signal_coverage")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("density_label", row.get("density_label")),
                        ("validation_hit", row.get("validation_directional_hit_rate")),
                        ("oos_hit", row.get("oos_directional_hit_rate")),
                        ("boundary", "density_only_not_threshold_selection"),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": "Representative q90 threshold-density checkpoint; not an optimized trading threshold.",
            }
        )
    return rows


def write_ledgers(
    *,
    result: Mapping[str, Any],
    convergence_artifacts: Mapping[str, Any],
    threshold_artifacts: Mapping[str, Any],
    runtime_probability_artifacts: Mapping[str, Any],
    context: Mapping[str, Any],
) -> dict[str, Any]:
    rows = convergence_ledger_rows(convergence_artifacts) + threshold_ledger_rows(threshold_artifacts)
    rows.extend(
        build_mt5_alpha_ledger_rows(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            mt5_kpi_records=result.get("mt5_kpi_records", []),
            run_output_root=Path(rel(RUN_ROOT)),
            external_verification_status=str(result.get("external_verification_status")),
        )
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "convergence_threshold_feasibility_runtime_handoff_probe",
        "status": "reviewed" if result.get("external_verification_status") == "completed" else "payload_only",
        "judgment": result.get("judgment"),
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("convergence_artifact", convergence_artifacts["training_history_summary_json"]["path"]),
                ("threshold_artifact", threshold_artifacts["threshold_feasibility_summary_json"]["path"]),
                ("runtime_probability_artifact", runtime_probability_artifacts["runtime_probability_summary_json"]["path"]),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("no_trade_threshold", NO_TRADE_THRESHOLD),
                ("tier_b_fallback_rows", context["tier_b_context_summary"].get("tier_b_fallback_rows")),
                ("external_verification", result.get("external_verification_status")),
                ("boundary", "convergence_threshold_feasibility_probe_only"),
            )
        ),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def build_summary(
    *,
    result: Mapping[str, Any],
    convergence_artifacts: Mapping[str, Any],
    threshold_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    runtime_probability_artifacts: Mapping[str, Any],
) -> dict[str, Any]:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in result.get("mt5_kpi_records", [])}
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
        "no_trade_threshold": NO_TRADE_THRESHOLD,
        "representative_threshold_id": REPRESENTATIVE_THRESHOLD_ID,
        "spec": model_artifacts["spec"],
        "onnx_parity": model_artifacts["onnx_parity"],
        "convergence": {row["scope"]: row for row in convergence_artifacts["payload"]["rows"]},
        "representative_thresholds": {row["scope"]: row for row in threshold_artifacts["payload"]["representative_rows"]},
        "threshold_density_label_counts": threshold_artifacts["payload"]["density_label_counts"],
        "probability_shape": threshold_artifacts["shape_payload"],
        "mt5_handoff_validation": by_view.get("mt5_routed_total_validation_is", {}),
        "mt5_handoff_oos": by_view.get("mt5_routed_total_oos", {}),
        "runtime_probability_summary": runtime_probability_artifacts["payload"],
        "failure": result.get("failure"),
    }


def skill_receipts(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    status = "executed" if result.get("external_verification_status") == "completed" else "blocked"
    return {
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "receipts": [
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-reentry-read",
                "status": status,
                "source_current_truth_docs": [rel(WORKSPACE_STATE_PATH), rel(CURRENT_WORKING_STATE_PATH)],
                "active_stage": STAGE_ID,
                "current_run": RUN_ID,
                "detected_conflicts": ["current_working_state_stage12_stale_section_rewritten(현재 작업 상태 Stage12 낡은 문단 갱신)"],
                "allowed_claims": ["run04D_completed_if_mt5_completed"],
                "forbidden_claims": ["baseline", "promotion", "runtime_authority"],
            },
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-experiment-design",
                "status": status,
                "hypothesis": "MLP convergence(수렴)와 threshold density(임계값 밀도)가 모델 계열 특성을 보여준다.",
                "baseline": "internal Tier A/B(티어 A/B) split read only; no Stage10/11/12 baseline(기준선 없음)",
                "changed_variables": "observation target changed to convergence and threshold feasibility(수렴/임계값 가능성)",
                "invalid_conditions": "missing convergence artifact(수렴 산출물 누락) or missing MT5 handoff(인계 누락)",
                "evidence_plan": [rel(RUN_ROOT / "convergence/training_history_summary.json"), rel(RUN_ROOT / "thresholds/threshold_feasibility_summary.json")],
            },
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-model-validation",
                "status": status,
                "model_or_threshold_surface": "MLPClassifier convergence curve(수렴 곡선) and q-grid threshold density(q 격자 임계값 밀도)",
                "validation_split": SPLIT_CONTRACT,
                "overfit_checks": "single split only(단일 분할만); no selection claim(선택 주장 없음)",
                "selection_metric_boundary": "representative q90 density checkpoint(대표 q90 밀도 확인점), not optimized(최적화 아님)",
                "allowed_claims": ["threshold_feasibility_observed"],
                "forbidden_claims": ["calibrated_probability", "selected_threshold", "alpha_quality"],
            },
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-runtime-parity",
                "status": status,
                "python_artifact": rel(RUN_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.joblib"),
                "runtime_artifact": rel(RUN_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.onnx"),
                "compared_surface": "ONNX probability parity(확률 동등성) and MT5 no-trade handoff(MT5 무거래 인계)",
                "parity_level": "runtime_probe(런타임 탐침)",
                "tester_identity": "MT5 Strategy Tester(전략 테스터) US100 M5",
                "missing_evidence": ["none(없음)"],
                "allowed_claims": ["runtime_probe_completed"],
                "forbidden_claims": ["runtime_authority", "live_readiness", "promotion"],
            },
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-data-integrity",
                "status": status,
                "data_sources_checked": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT],
                "time_axis_boundary": "existing Stage04/03 timestamp contract(기존 시간축 계약)",
                "split_boundary": "train/validation/oos split_v1(학습/검증/표본외 분할)",
                "leakage_checks": "threshold grid derived from validation confidence only(검증 확신값에서만 임계값 격자 생성)",
                "missing_data_boundary": "Tier B partial context(부분 문맥) remains fallback-labelled(대체 라벨 유지)",
            },
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-backtest-forensics",
                "status": status,
                "tester_report": rel(RUN_ROOT / "mt5/reports"),
                "tester_settings": rel(RUN_ROOT / "mt5"),
                "spread_commission_slippage": "tester settings only(테스터 설정만); no profit claim(수익 주장 없음)",
                "trade_list_identity": "zero-trade no-trade threshold probe(무거래 임계값 탐침)",
                "forensic_gaps": ["none(없음)"],
            },
            {
                "packet_id": PACKET_ID,
                "skill": "obsidian-artifact-lineage",
                "status": status,
                "source_inputs": [FEATURE_SET_ID, LABEL_ID],
                "produced_artifacts": [rel(RUN_ROOT / "run_manifest.json"), rel(RUN_ROOT / "convergence/training_history_summary.json")],
                "raw_evidence": [rel(RUN_ROOT / "thresholds/threshold_feasibility_summary.json"), rel(RUN_ROOT / "runtime_probability/runtime_probability_summary.json")],
                "machine_readable": [rel(RUN_ROOT / "kpi_record.json")],
                "human_readable": [rel(REVIEW_PATH)],
                "hashes_or_missing_reasons": "hashes recorded in manifest/artifact records(해시를 목록/산출물 기록에 남김)",
                "lineage_boundary": BOUNDARY,
            },
        ],
    }


def write_run_files(
    *,
    created_at: str,
    context: Mapping[str, Any],
    spec: MlpVariantSpec,
    convergence_artifacts: Mapping[str, Any],
    threshold_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    prepared: Mapping[str, Any],
    result: Mapping[str, Any],
    runtime_probability_artifacts: Mapping[str, Any],
    ledgers: Mapping[str, Any],
) -> dict[str, Any]:
    summary = build_summary(
        result=result,
        convergence_artifacts=convergence_artifacts,
        threshold_artifacts=threshold_artifacts,
        model_artifacts=model_artifacts,
        runtime_probability_artifacts=runtime_probability_artifacts,
    )
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "boundary": BOUNDARY,
        "spec": spec.payload(),
        "convergence_artifacts": convergence_artifacts,
        "threshold_artifacts": threshold_artifacts,
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
        "attempts": prepared["attempts"],
        "common_copies": prepared["common_copies"],
        "runtime_probability_artifacts": runtime_probability_artifacts,
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "failure": result.get("failure"),
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_payload(context, threshold_artifacts, convergence_artifacts, result, runtime_probability_artifacts))
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(PACKET_ROOT / "ledger_outputs.json", ledgers)
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(created_at, result))
    write_text_bom(RUN_ROOT / "reports/result_summary.md", report_markdown(summary, result))
    write_text_bom(PACKET_ROOT / "work_packet.md", work_packet_markdown(summary, created_at))
    sync_docs(summary, result)
    return summary


def kpi_payload(
    context: Mapping[str, Any],
    threshold_artifacts: Mapping[str, Any],
    convergence_artifacts: Mapping[str, Any],
    result: Mapping[str, Any],
    runtime_probability_artifacts: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "convergence_threshold_feasibility_and_no_trade_handoff",
        "convergence": convergence_artifacts["payload"],
        "thresholds": threshold_artifacts["payload"],
        "probability_shape": threshold_artifacts["shape_payload"],
        "tier_b_context_summary": context["tier_b_context_summary"],
        "runtime_probability": runtime_probability_artifacts["payload"],
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result.get("external_verification_status"),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }


def scope_slug(scope: str) -> str:
    return scope.lower().replace(" ", "_").replace("+", "b")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP convergence and threshold feasibility probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)

    created_at = utc_now()
    context = load_context()
    spec = convergence_threshold_spec()
    tier_a_model, tier_a_warnings = fit_with_warning_capture(context["tier_a_frame"], context["tier_a_feature_order"], spec)
    tier_b_model, tier_b_warnings = fit_with_warning_capture(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    convergence_artifacts = write_convergence_artifacts(
        tier_a_model=tier_a_model,
        tier_b_model=tier_b_model,
        tier_a_warnings=tier_a_warnings,
        tier_b_warnings=tier_b_warnings,
    )
    threshold_artifacts = write_threshold_artifacts(tier_a_model=tier_a_model, tier_b_model=tier_b_model, context=context)
    config = Stage13HandoffConfig(
        stage_number=STAGE_NUMBER,
        run_id=RUN_ID,
        exploration_label=EXPLORATION_LABEL,
        run_root=RUN_ROOT,
        no_trade_threshold=NO_TRADE_THRESHOLD,
        min_margin=MIN_MARGIN,
        max_hold_bars=MAX_HOLD_BARS,
    )
    model_artifacts = materialize_models(
        config=config,
        spec=spec,
        tier_a_model=tier_a_model,
        tier_b_model=tier_b_model,
        tier_a_frame=context["tier_a_frame"],
        tier_b_training_frame=context["tier_b_training_frame"],
        tier_a_feature_order=context["tier_a_feature_order"],
        tier_b_feature_order=context["tier_b_feature_order"],
        artifact_prefix=spec.variant_id,
    )
    feature_matrices = export_feature_matrices(config, context)
    prepared = {
        "run_id": RUN_ID,
        "run_root": RUN_ROOT.as_posix(),
        "stage_id": STAGE_ID,
        "source_variant_id": spec.variant_id,
        "attempts": make_no_trade_attempts(
            config=config,
            context=context,
            model_artifacts=model_artifacts,
            feature_matrices=feature_matrices,
            model_id_suffix="convergence_threshold_probe",
            record_prefix_suffix="convergence_threshold_proxy",
        ),
        "common_copies": copy_runtime_inputs(config=config, model_artifacts=model_artifacts, feature_matrices=feature_matrices),
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": context["tier_b_context_summary"],
    }
    result = execute_or_materialize(prepared, args)
    runtime_probability_artifacts = write_runtime_probability_artifacts(
        result=result,
        output_root=RUN_ROOT / "runtime_probability",
        boundary=RUNTIME_PROBABILITY_BOUNDARY,
    )
    ledgers = write_ledgers(
        result=result,
        convergence_artifacts=convergence_artifacts,
        threshold_artifacts=threshold_artifacts,
        runtime_probability_artifacts=runtime_probability_artifacts,
        context=context,
    )
    summary = write_run_files(
        created_at=created_at,
        context=context,
        spec=spec,
        convergence_artifacts=convergence_artifacts,
        threshold_artifacts=threshold_artifacts,
        model_artifacts=model_artifacts,
        feature_matrices=feature_matrices,
        prepared=prepared,
        result=result,
        runtime_probability_artifacts=runtime_probability_artifacts,
        ledgers=ledgers,
    )
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "materialize_only": bool(args.materialize_only), "summary": summary})
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
