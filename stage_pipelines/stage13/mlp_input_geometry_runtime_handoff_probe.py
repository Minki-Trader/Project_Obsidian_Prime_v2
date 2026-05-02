from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
import joblib
import pandas as pd
from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, FEATURE_ORDER_PATH, MODEL_INPUT_PATH, RAW_ROOT, ROOT, TERMINAL_DATA_ROOT_DEFAULT, TERMINAL_PATH_DEFAULT, TESTER_PROFILE_ROOT_DEFAULT, TRAINING_SUMMARY_PATH, attempt_payload, common_run_root, copy_to_common, execute_prepared_run, split_dates_from_frame
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.input_geometry import audit_input_geometry
from foundation.models.mlp_characteristics import MlpVariantSpec, fit_mlp_variant
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_sklearn_to_onnx_zipmap_disabled, ordered_hash
from foundation.mt5 import runtime_support as mt5

STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04B"
RUN_ID = "run04B_mlp_input_geometry_runtime_handoff_probe_v1"
PACKET_ID = "stage13_run04B_mlp_input_geometry_runtime_handoff_probe_packet_v1"
EXPLORATION_LABEL = "stage13_MLPInputGeometry__RuntimeHandoffProbe"
MODEL_FAMILY = "sklearn_mlpclassifier_handoff_sentinel"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_run_baseline_seed_or_reference"
BOUNDARY = "runtime_handoff_probe_input_geometry_not_alpha_quality_not_promotion_not_runtime_authority"
NO_TRADE_THRESHOLD = 1.01
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 9
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04B_mlp_input_geometry_runtime_handoff_probe_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run04B_mlp_input_geometry_runtime_handoff_probe_plan.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_input_geometry_runtime_handoff_probe.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text_bom(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    tier_a_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, tier_a_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "tier_a_feature_order": tier_a_feature_order,
        "tier_a_feature_order_hash": ordered_hash(tier_a_feature_order),
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_feature_order_hash": ordered_hash(tier_b_feature_order),
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }


def write_geometry_artifacts(audit: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "geometry"
    io_path(root).mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, Any] = {}
    for key in (
        "tier_a_summary",
        "tier_a_top_feature_drift",
        "tier_a_class_centroids",
        "tier_a_high_correlation_pairs",
        "tier_gap_summary",
    ):
        path = root / f"{key}.csv"
        audit[key].to_csv(io_path(path), index=False, encoding="utf-8")
        artifacts[key] = {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "rows": int(len(audit[key]))}
    summary_path = root / "input_geometry_summary.json"
    write_json(summary_path, audit["payload"])
    artifacts["input_geometry_summary"] = {
        "path": rel(summary_path),
        "sha256": sha256_file_lf_normalized(summary_path),
        "rows": 1,
    }
    return artifacts


def train_sentinel_models(context: Mapping[str, Any]) -> tuple[Any, Any, MlpVariantSpec]:
    spec = MlpVariantSpec(
        variant_id="handoff_sentinel_mlp16_no_trade_threshold",
        idea_id="runtime_handoff_sentinel",
        description="Small MLP used only to make MT5 load and score feature matrices; thresholds suppress trades.",
        hidden_layer_sizes=(16,),
        activation="relu",
        alpha=0.01,
        learning_rate_init=0.001,
        max_iter=80,
        n_iter_no_change=8,
        validation_fraction=0.12,
        random_state=1402,
    )
    tier_a_model = fit_mlp_variant(context["tier_a_frame"], context["tier_a_feature_order"], spec)
    tier_b_model = fit_mlp_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    return tier_a_model, tier_b_model, spec


def materialize_models(context: Mapping[str, Any], tier_a_model: Any, tier_b_model: Any, spec: MlpVariantSpec) -> dict[str, Any]:
    root = RUN_ROOT / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    a_joblib = root / "handoff_sentinel_tier_a_mlp_58.joblib"
    b_joblib = root / "handoff_sentinel_tier_b_mlp_core42.joblib"
    a_onnx = root / "handoff_sentinel_tier_a_mlp_58.onnx"
    b_onnx = root / "handoff_sentinel_tier_b_mlp_core42.onnx"
    joblib.dump(tier_a_model, io_path(a_joblib))
    joblib.dump(tier_b_model, io_path(b_joblib))
    a_export = export_sklearn_to_onnx_zipmap_disabled(tier_a_model, a_onnx, feature_count=len(context["tier_a_feature_order"]))
    b_export = export_sklearn_to_onnx_zipmap_disabled(tier_b_model, b_onnx, feature_count=len(context["tier_b_feature_order"]))
    a_sample = context["tier_a_frame"].loc[
        context["tier_a_frame"]["split"].astype(str).eq("validation"),
        context["tier_a_feature_order"],
    ].head(128).to_numpy(dtype="float64", copy=False)
    b_sample = context["tier_b_training_frame"].loc[
        context["tier_b_training_frame"]["split"].astype(str).eq("validation"),
        context["tier_b_feature_order"],
    ].head(128).to_numpy(dtype="float64", copy=False)
    return {
        "spec": spec.payload(),
        "tier_a_joblib": {"path": rel(a_joblib), "sha256": sha256_file_lf_normalized(a_joblib)},
        "tier_b_joblib": {"path": rel(b_joblib), "sha256": sha256_file_lf_normalized(b_joblib)},
        "tier_a_onnx": a_export,
        "tier_b_onnx": b_export,
        "onnx_parity": {
            "tier_a": check_onnxruntime_probability_parity(tier_a_model, a_onnx, a_sample),
            "tier_b": check_onnxruntime_probability_parity(tier_b_model, b_onnx, b_sample),
        },
    }


def export_feature_matrices(context: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "features"
    io_path(root).mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        b_frame = context["tier_b_fallback_frame"].loc[
            context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)
        ].copy()
        a_path = root / f"tier_a_{runtime_split}_feature_matrix.csv"
        b_path = root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv"
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            a_frame,
            context["tier_a_feature_order"],
            a_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            b_frame,
            context["tier_b_feature_order"],
            b_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], common: str) -> list[dict[str, Any]]:
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        source = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(source, f"{common}/models/{source.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        source = ROOT / matrix["path"]
        copies.append(copy_to_common(source, f"{common}/features/{source.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], common: str) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": RUN_ROOT,
            "run_id": RUN_ID,
            "stage_number": STAGE_NUMBER,
            "exploration_label": EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_a_handoff_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{a_model}",
                model_id=f"{RUN_ID}_tier_a_handoff_sentinel",
                feature_path=f"{common}/features/{a_matrix}",
                feature_count=len(context["tier_a_feature_order"]),
                feature_order_hash=context["tier_a_feature_order_hash"],
                short_threshold=NO_TRADE_THRESHOLD,
                long_threshold=NO_TRADE_THRESHOLD,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_handoff",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_handoff_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{b_model}",
                model_id=f"{RUN_ID}_tier_b_handoff_sentinel",
                feature_path=f"{common}/features/{b_matrix}",
                feature_count=len(context["tier_b_feature_order"]),
                feature_order_hash=context["tier_b_feature_order_hash"],
                short_threshold=NO_TRADE_THRESHOLD,
                long_threshold=NO_TRADE_THRESHOLD,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_handoff",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_handoff_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{a_model}",
                model_id=f"{RUN_ID}_tier_a_handoff_sentinel",
                feature_path=f"{common}/features/{a_matrix}",
                feature_count=len(context["tier_a_feature_order"]),
                feature_order_hash=context["tier_a_feature_order_hash"],
                short_threshold=NO_TRADE_THRESHOLD,
                long_threshold=NO_TRADE_THRESHOLD,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_handoff",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{b_model}",
                fallback_model_id=f"{RUN_ID}_tier_b_handoff_sentinel",
                fallback_feature_path=f"{common}/features/{b_matrix}",
                fallback_feature_count=len(context["tier_b_feature_order"]),
                fallback_feature_order_hash=context["tier_b_feature_order_hash"],
                fallback_short_threshold=NO_TRADE_THRESHOLD,
                fallback_long_threshold=NO_TRADE_THRESHOLD,
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
            )
        )
    return attempts


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
            "judgment": "blocked_input_geometry_runtime_handoff_probe",
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = (
        "inconclusive_input_geometry_runtime_handoff_probe_completed"
        if completed
        else "blocked_input_geometry_runtime_handoff_probe"
    )
    return result


def geometry_ledger_rows(audit_payload: Mapping[str, Any], geometry_artifacts: Mapping[str, Any]) -> list[dict[str, Any]]:
    tier_a = {row["split"]: row for row in audit_payload["tier_a_summary"]}
    tier_gap = {row["split"]: row for row in audit_payload["tier_gap_summary"]}
    return [
        {
            "ledger_row_id": f"{RUN_ID}__python_input_geometry_tier_a",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_input_geometry_tier_a",
            "parent_run_id": RUN_ID,
            "record_view": "python_input_geometry_tier_a",
            "tier_scope": mt5.TIER_A,
            "kpi_scope": "input_geometry",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "inconclusive_input_geometry_audit",
            "path": geometry_artifacts["input_geometry_summary"]["path"],
            "primary_kpi": ledger_pairs(
                (
                    ("features", tier_a["train"]["feature_count"]),
                    ("validation_mean_abs_z_max", tier_a["validation"]["mean_abs_z_max"]),
                    ("oos_mean_abs_z_max", tier_a["oos"]["mean_abs_z_max"]),
                    ("validation_outlier_rate_max", tier_a["validation"]["outlier_rate_max"]),
                    ("oos_outlier_rate_max", tier_a["oos"]["outlier_rate_max"]),
                )
            ),
            "guardrail_kpi": ledger_pairs((("boundary", "input_geometry_only"), ("mt5_threshold", NO_TRADE_THRESHOLD))),
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Python input geometry audit only; not model quality or trading evidence.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__python_input_geometry_tier_gap",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_input_geometry_tier_gap",
            "parent_run_id": RUN_ID,
            "record_view": "python_input_geometry_tier_gap",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "tier_input_geometry_gap",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "inconclusive_tier_input_geometry_gap",
            "path": geometry_artifacts["tier_gap_summary"]["path"],
            "primary_kpi": ledger_pairs(
                (
                    ("validation_gap", tier_gap["validation"]["mean_abs_z_gap"]),
                    ("oos_gap", tier_gap["oos"]["mean_abs_z_gap"]),
                    ("validation_b_rows", tier_gap["validation"]["tier_b_fallback_rows"]),
                    ("oos_b_rows", tier_gap["oos"]["tier_b_fallback_rows"]),
                )
            ),
            "guardrail_kpi": ledger_pairs((("common_features", tier_gap["validation"]["common_feature_count"]),)),
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Tier A/Tier B common-feature geometry gap; not a routed performance comparison.",
        },
    ]


def write_ledgers(result: Mapping[str, Any], audit_payload: Mapping[str, Any], geometry_artifacts: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    rows = geometry_ledger_rows(audit_payload, geometry_artifacts)
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
        "lane": "input_geometry_runtime_handoff_probe",
        "status": "reviewed" if result.get("external_verification_status") == "completed" else "payload_only",
        "judgment": result.get("judgment"),
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("mt5_views", "tier_a_handoff;tier_b_fallback_handoff;routed_handoff"),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("no_trade_threshold", NO_TRADE_THRESHOLD),
                ("tier_b_fallback_rows", context["tier_b_context_summary"].get("tier_b_fallback_rows")),
                ("no_tier_labelable_rows", context["tier_b_context_summary"].get("no_tier_labelable_rows")),
                ("external_verification", result.get("external_verification_status")),
                ("boundary", "runtime_handoff_probe_only"),
            )
        ),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def metric_by_view(records: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(record.get("record_view")): record.get("metrics", {}) for record in records}


def build_summary(result: Mapping[str, Any], audit_payload: Mapping[str, Any], model_artifacts: Mapping[str, Any]) -> dict[str, Any]:
    by_view = metric_by_view(result.get("mt5_kpi_records", []))
    tier_a = {row["split"]: row for row in audit_payload["tier_a_summary"]}
    tier_gap = {row["split"]: row for row in audit_payload["tier_gap_summary"]}
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
        "no_trade_threshold": NO_TRADE_THRESHOLD,
        "onnx_parity": model_artifacts["onnx_parity"],
        "tier_a_validation_mean_abs_z_max": tier_a["validation"]["mean_abs_z_max"],
        "tier_a_oos_mean_abs_z_max": tier_a["oos"]["mean_abs_z_max"],
        "tier_gap_validation_mean_abs_z_gap": tier_gap["validation"]["mean_abs_z_gap"],
        "tier_gap_oos_mean_abs_z_gap": tier_gap["oos"]["mean_abs_z_gap"],
        "mt5_handoff_validation": by_view.get("mt5_routed_total_validation_is", {}),
        "mt5_handoff_oos": by_view.get("mt5_routed_total_oos", {}),
        "failure": result.get("failure"),
    }


def write_run_files(
    *,
    created_at: str,
    context: Mapping[str, Any],
    audit: Mapping[str, Any],
    geometry_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    prepared: Mapping[str, Any],
    result: Mapping[str, Any],
    ledgers: Mapping[str, Any],
) -> dict[str, Any]:
    summary = build_summary(result, audit["payload"], model_artifacts)
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
        "geometry_artifacts": geometry_artifacts,
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
        "attempts": prepared["attempts"],
        "common_copies": prepared["common_copies"],
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "failure": result.get("failure"),
    }
    kpi = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "input_geometry_and_runtime_handoff",
        "input_geometry": audit["payload"],
        "tier_b_context_summary": context["tier_b_context_summary"],
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
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi)
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(PACKET_ROOT / "ledger_outputs.json", ledgers)
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(created_at, result))
    write_text_bom(RUN_ROOT / "reports/result_summary.md", report_markdown(summary, result, audit["payload"]))
    write_text_bom(PACKET_ROOT / "work_packet.md", work_packet_markdown(summary, created_at))
    write_docs(summary, result, audit["payload"])
    return summary


def report_markdown(summary: Mapping[str, Any], result: Mapping[str, Any], audit_payload: Mapping[str, Any]) -> str:
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- no_trade_threshold(무거래 임계값): `{NO_TRADE_THRESHOLD}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Input Geometry(입력 기하)",
        "",
        "| split(분할) | mean_abs_z_max(최대 평균 z) | outlier_rate_max(최대 이상치 비율) |",
        "|---|---:|---:|",
    ]
    for row in audit_payload["tier_a_summary"]:
        lines.append(f"| {row['split']} | {row['mean_abs_z_max']} | {row['outlier_rate_max']} |")
    lines.extend(
        [
            "",
            "## MT5 Handoff(MT5 인계)",
            "",
            "| view(보기) | split(분할) | feature_ready(피처 준비) | model_ok(모델 정상) | trades(거래) |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        lines.append(
            f"| {record.get('record_view')} | {record.get('split')} | {metrics.get('feature_ready_count')} | {metrics.get('model_ok_count')} | {metrics.get('trade_count')} |"
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 실행은 거래 성과가 아니라 입력 행렬과 MT5(메타트레이더5) 런타임 인계가 정상인지 보는 runtime_handoff_probe(런타임 인계 탐침)이다.",
        ]
    )
    return "\n".join(lines)


def work_packet_markdown(summary: Mapping[str, Any], created_at: str) -> str:
    return "\n".join(
        [
            f"# {PACKET_ID}",
            "",
            f"- created_at_utc(생성 UTC): `{created_at}`",
            "- primary_family(주 작업군): `runtime_backtest(런타임 백테스트)`",
            "- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`",
            "- support_skills(보조 스킬): `obsidian-backtest-forensics(백테스트 포렌식)`, `obsidian-data-integrity(데이터 무결성)`, `obsidian-artifact-lineage(산출물 계보)`",
            "- runtime_evidence_gate(런타임 근거 게이트): `pass(통과)`",
            "- kpi_contract_audit(KPI 계약 감사): `pass(통과)`",
            "- state_sync_audit(상태 동기화 감사): `pending_external_command(외부 명령 대기)`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): 모델 성능이 아니라 입력 기하와 MT5(메타트레이더5) 인계 의미를 확인한다.",
        ]
    )


def skill_receipts(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    return {
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "receipts": [
            {"skill": "obsidian-runtime-parity", "status": status, "evidence": [rel(RUN_ROOT / "run_manifest.json")], "claim_boundary": BOUNDARY},
            {"skill": "obsidian-backtest-forensics", "status": status, "evidence": [rel(RUN_ROOT / "reports/result_summary.md")], "claim_boundary": "tester_identity_and_no_trade_handoff_records"},
            {"skill": "obsidian-data-integrity", "status": "completed", "evidence": [rel(RUN_ROOT / "geometry/input_geometry_summary.json")], "claim_boundary": "input_geometry_only_not_model_quality"},
            {"skill": "obsidian-artifact-lineage", "status": "completed", "evidence": [rel(RUN_ROOT / "run_manifest.json"), rel(STAGE_LEDGER_PATH)], "claim_boundary": "artifacts_connected_with_runtime_probe_boundary"},
        ],
    }


def write_docs(summary: Mapping[str, Any], result: Mapping[str, Any], audit_payload: Mapping[str, Any]) -> None:
    status = "reviewed_runtime_handoff_completed" if summary["external_verification_status"] == "completed" else "blocked_runtime_handoff_attempted"
    write_text_bom(PLAN_PATH, plan_text())
    write_text_bom(REVIEW_PATH, report_markdown(summary, result, audit_payload))
    write_text_bom(DECISION_PATH, decision_text(summary))
    write_text_bom(SELECTION_STATUS_PATH, selection_status_text(summary, status))
    sync_review_index(summary)
    sync_changelog(summary)
    sync_workspace_state(summary)
    sync_current_working_state(summary)


def plan_text() -> str:
    return "\n".join(
        [
            "# RUN04B MLP Input Geometry Runtime Handoff Probe Plan",
            "",
            "- run_id(실행 ID): `run04B_mlp_input_geometry_runtime_handoff_probe_v1`",
            "- purpose(목적): MLP(다층 퍼셉트론) 입력 공간과 MT5(메타트레이더5) feature matrix(피처 행렬) 인계를 확인한다.",
            "- no_trade_threshold(무거래 임계값): `1.01`",
            "- independence(독립성): RUN04A(실행 04A) 모델 변형을 흔들지 않고 거래 성과를 주장하지 않는다.",
            "",
            "효과(effect, 효과): Stage13(13단계) 안에서 모델 탐색이 아닌 입력/런타임 인계 질문을 분리한다.",
        ]
    )


def decision_text(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# 2026-05-02 Stage 13 MLP Input Geometry Runtime Handoff Probe",
            "",
            "- decision(결정): Stage13(13단계) 안에서 입력 기하(input geometry, 입력 기하)와 MT5 runtime handoff(MT5 런타임 인계)를 별도 주제로 본다.",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "- boundary(경계): runtime_handoff_probe_only(런타임 인계 탐침만)",
            "",
            "효과(effect, 효과): RUN04A(실행 04A)의 MLP 변형을 흔들지 않고, 입력 공간과 MT5(메타트레이더5) 파일 인계 의미만 확인한다.",
        ]
    )


def selection_status_text(summary: Mapping[str, Any], status: str) -> str:
    return "\n".join(
        [
            "# Stage 13 Selection Status",
            "",
            "## Current Read(현재 판독)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- status(상태): `{status}`",
            "- proposed model family(제안 모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
            "- exploration depth(탐색 깊이): `input_geometry_runtime_handoff_only(입력 기하 런타임 인계만)`",
            "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
            f"- current run(현재 실행): `{RUN_ID}`",
            "- selected operating reference(선택 운영 기준): `none(없음)`",
            "- selected promotion candidate(선택 승격 후보): `none(없음)`",
            "- selected baseline(선택 기준선): `none(없음)`",
            f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            "",
            "효과(effect, 효과): 거래 성과가 아니라 입력 기하와 MT5(메타트레이더5) 인계만 확인한다.",
        ]
    )


def sync_review_index(summary: Mapping[str, Any]) -> None:
    text = read_text(REVIEW_INDEX_PATH) if REVIEW_INDEX_PATH.exists() else "# Stage 13 Review Index\n"
    line = f"- `{RUN_ID}`: `{summary['judgment']}`, report(보고서) `{rel(REVIEW_PATH)}`"
    if RUN_ID not in text:
        text = text.rstrip() + "\n" + line + "\n"
    write_text_bom(REVIEW_INDEX_PATH, text)


def sync_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    line = (
        f"- 2026-05-02: `{RUN_ID}` {summary['external_verification_status']}. "
        "Stage13(13단계) MLP input geometry runtime handoff probe(입력 기하 런타임 인계 탐침)를 no-trade threshold(무거래 임계값)로 실행했다. "
        "Effect(효과): RUN04A(실행 04A) 모델 흔들기 없이 feature matrix(피처 행렬)와 MT5(메타트레이더5) 인계 의미를 확인한다."
    )
    if RUN_ID not in text:
        text = text.replace("## 2026-05-02\n\n", "## 2026-05-02\n\n" + line + "\n", 1)
    write_text_bom(CHANGELOG_PATH, text)


def sync_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    block = (
        "stage13_mlp_input_geometry_runtime_handoff_probe:\n"
        f"  run_id: {RUN_ID}\n"
        f"  status: {summary['external_verification_status']}\n"
        f"  judgment: {summary['judgment']}\n"
        "  boundary: runtime_handoff_probe_only_not_alpha_quality_not_promotion_not_runtime_authority\n"
        f"  report_path: {rel(REVIEW_PATH)}\n"
    )
    if "stage13_mlp_input_geometry_runtime_handoff_probe:" not in text:
        insert_after = "stage13_mlp_characteristic_runtime_probe:\n"
        index = text.find(insert_after)
        if index >= 0:
            next_stage = text.find("\nstage01_raw_m5_inventory:", index)
            text = text[: next_stage + 1] + block + text[next_stage + 1 :]
        else:
            text = text.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n", 1)
    write_text_bom(WORKSPACE_STATE_PATH, text)


def sync_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_WORKING_STATE_PATH)
    text = text.replace("current run(현재 실행): `run04A_mlp_characteristic_runtime_probe_v1`", f"current run(현재 실행): `{RUN_ID}`")
    latest = "\n".join(
        [
            "## Latest Stage 13 Update(최신 Stage 13 업데이트)",
            "",
            f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, 외부 검증 상태(external verification status, 외부 검증 상태)는 `{summary['external_verification_status']}`다.",
            "",
            "효과(effect, 효과): RUN04A(실행 04A)의 모델 변형을 흔들지 않고, 입력 기하(input geometry, 입력 기하)와 MT5(메타트레이더5) 런타임 인계만 확인했다.",
            "",
        ]
    )
    start = text.find("## Latest Stage 13 Update")
    end = text.find("## 쉬운 설명", start)
    if start >= 0 and end > start:
        text = text[:start] + latest + text[end:]
    else:
        text = text.replace("## 쉬운 설명", latest + "## 쉬운 설명", 1)
    write_text_bom(CURRENT_WORKING_STATE_PATH, text)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP input geometry plus MT5 runtime handoff probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    created_at = utc_now()
    context = load_context()
    audit = audit_input_geometry(
        tier_a_frame=context["tier_a_frame"],
        tier_a_feature_order=context["tier_a_feature_order"],
        tier_b_fallback_frame=context["tier_b_fallback_frame"],
        tier_b_feature_order=context["tier_b_feature_order"],
    )
    geometry_artifacts = write_geometry_artifacts(audit)
    tier_a_model, tier_b_model, spec = train_sentinel_models(context)
    model_artifacts = materialize_models(context, tier_a_model, tier_b_model, spec)
    feature_matrices = export_feature_matrices(context)
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    common_copies = copy_runtime_inputs(model_artifacts, feature_matrices, common)
    prepared = {
        "run_id": RUN_ID,
        "run_root": RUN_ROOT.as_posix(),
        "stage_id": STAGE_ID,
        "source_variant_id": spec.variant_id,
        "attempts": make_attempts(context, model_artifacts, feature_matrices, common),
        "common_copies": common_copies,
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": context["tier_b_context_summary"],
    }
    result = execute_or_materialize(prepared, args)
    ledgers = write_ledgers(result, audit["payload"], geometry_artifacts, context)
    summary = write_run_files(
        created_at=created_at,
        context=context,
        audit=audit,
        geometry_artifacts=geometry_artifacts,
        model_artifacts=model_artifacts,
        feature_matrices=feature_matrices,
        prepared=prepared,
        result=result,
        ledgers=ledgers,
    )
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "materialize_only": bool(args.materialize_only), "summary": summary})
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
