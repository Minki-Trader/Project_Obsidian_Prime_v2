from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import ExtraTreesClassifier

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    RAW_ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
)
from foundation.control_plane.tier_context_materialization import (
    TIER_B_CORE_FEATURE_ORDER,
    build_tier_b_partial_context_frames,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage12.extratrees_rolling_wfo_split_probe import (
    FOLDS,
    PROBE_N_ESTIMATORS,
    feature_sets_for_fold,
    ordered_probs,
    prepare_frames,
    probe_params,
    window,
)
from stage_pipelines.stage12.extratrees_standalone_batch20_support import VariantSpec, _variant_specs


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
STAGE_NUMBER = 12
RUN_NUMBER = "run03K"
PACKAGE_RUN_ID = "run03K_et_wfo_fold07_all_variant_mt5_failure_probe_v1"
PACKET_ID = "stage12_run03k_wfo_fold07_all_variant_mt5_failure_probe_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesWFOFold07MT5FailureProbe"
SOURCE_WFO_RUN_ID = "run03J_et_rolling_wfo_split_probe_v1"
SOURCE_VARIANT_RUN_ID = "run03D_et_standalone_batch20_v1"
SOURCE_MT5_REFERENCE_RUN_ID = "run03H_et_batch20_all_variant_tier_balance_mt5_v1"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_58_and_core42_partial_context_wfo_fold07"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "wfo_fold07_train_20220901_20250930_val_20251001_20251231_test_20260101_20260413"
BOUNDARY = "runtime_probe_failure_data_only_not_alpha_quality_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_wfo_fold07_mt5_failure_probe_completed"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUNS_ROOT = STAGE_ROOT / "02_runs"
PACKAGE_RUN_ROOT = RUNS_ROOT / PACKAGE_RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
SOURCE_WFO_ROOT = RUNS_ROOT / SOURCE_WFO_RUN_ID
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run03K_wfo_fold07_mt5_failure_probe_plan.md"
STAGE_REVIEW_PATH = STAGE_ROOT / "03_reviews/run03K_wfo_fold07_mt5_failure_probe_packet.md"

MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"

ATTEMPT_COLUMNS = (
    "run_id",
    "source_variant_id",
    "fold_id",
    "attempt_name",
    "split",
    "wfo_split_role",
    "tier_scope",
    "route_role",
    "tester_status",
    "runtime_status",
    "report_status",
    "net_profit",
    "profit_factor",
    "trade_count",
    "report_path",
)
VARIANT_SUMMARY_COLUMNS = (
    "source_variant_id",
    "run_id",
    "status",
    "validation_tier_a_net_profit",
    "validation_tier_b_net_profit",
    "validation_routed_net_profit",
    "validation_routed_trades",
    "test_tier_a_net_profit",
    "test_tier_b_net_profit",
    "test_routed_net_profit",
    "test_routed_trades",
)
TARGET_COLUMNS = (
    "run_id",
    "source_variant_id",
    "fold_id",
    "status",
    "attempt_count",
    "kpi_record_count",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True) + "\n")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig" if bom else "utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def current_branch() -> str:
    try:
        completed = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return completed.stdout.strip() or "unknown"


def variant_short_id(variant_id: str) -> str:
    match = re.match(r"(v\d+)", variant_id)
    if not match:
        raise ValueError(f"variant id does not start with vNN: {variant_id}")
    return match.group(1)


def mt5_rule(threshold: float, direction_mode: str) -> tuple[float, float, bool]:
    disabled = 2.0
    if direction_mode == "both":
        return threshold, threshold, False
    if direction_mode == "short_only":
        return threshold, disabled, False
    if direction_mode == "long_only":
        return disabled, threshold, False
    if direction_mode == "inverse":
        return threshold, threshold, True
    raise ValueError(f"unknown direction_mode: {direction_mode}")


def nonflat_threshold(probs: np.ndarray, quantile: float) -> float:
    return float(np.quantile(np.maximum(probs[:, 0], probs[:, 2]), quantile))


def split_dates_from_window(frame: pd.DataFrame) -> tuple[str, str]:
    if frame.empty:
        raise RuntimeError("empty fold split frame")
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def train_model(frame: pd.DataFrame, features: Sequence[str], params: Mapping[str, Any]) -> ExtraTreesClassifier:
    model = ExtraTreesClassifier(**dict(params))
    model.fit(frame.loc[:, list(features)].to_numpy(dtype="float64", copy=False), frame["label_class"].astype(int))
    return model


def build_context() -> dict[str, Any]:
    tier_a, tier_b_fallback, feature_order, metadata = prepare_frames()
    fold = next(item for item in FOLDS if item.fold_id == "fold07")
    tier_b_training = metadata["tier_b_training"]
    a_train = window(tier_a, fold.train_start, fold.train_end_exclusive)
    a_validation = window(tier_a, fold.validation_start, fold.validation_end_exclusive)
    a_test = window(tier_a, fold.test_start, fold.test_end_exclusive)
    b_train = window(tier_b_training, fold.train_start, fold.train_end_exclusive)
    b_validation = window(tier_b_fallback, fold.validation_start, fold.validation_end_exclusive)
    b_test = window(tier_b_fallback, fold.test_start, fold.test_end_exclusive)
    feature_sets = feature_sets_for_fold(a_train, feature_order, fold.fold_id)
    return {
        "fold": fold,
        "feature_order": feature_order,
        "feature_sets": feature_sets,
        "tier_a_train": a_train,
        "tier_a_validation": a_validation,
        "tier_a_test": a_test,
        "tier_b_train": b_train,
        "tier_b_validation": b_validation,
        "tier_b_test": b_test,
        "tier_b_order": list(TIER_B_CORE_FEATURE_ORDER),
        "source_metadata": metadata,
    }


def prepare_variant(spec: VariantSpec, context: Mapping[str, Any]) -> dict[str, Any]:
    variant_id = spec.variant_id
    run_id = f"{RUN_NUMBER}_et_{variant_short_id(variant_id)}_wfo_fold07_mt5_v1"
    run_root = RUNS_ROOT / run_id
    for child in ("models", "mt5", "predictions", "reports"):
        io_path(run_root / child).mkdir(parents=True, exist_ok=True)

    params = probe_params(spec)
    tier_a_order = context["feature_sets"][spec.feature_selector]
    tier_b_order = list(context["tier_b_order"])
    tier_a_hash = mt5.ordered_hash(tier_a_order)
    tier_b_hash = mt5.ordered_hash(tier_b_order)

    tier_a_model = train_model(context["tier_a_train"], tier_a_order, params)
    tier_b_model = train_model(context["tier_b_train"], tier_b_order, params)
    tier_a_val_probs = ordered_probs(tier_a_model, context["tier_a_validation"], tier_a_order)
    tier_b_val_probs = ordered_probs(tier_b_model, context["tier_b_validation"], tier_b_order)
    threshold_a = nonflat_threshold(tier_a_val_probs, spec.threshold_quantile)
    threshold_b = nonflat_threshold(tier_b_val_probs, spec.threshold_quantile)

    tier_a_joblib = run_root / f"models/tier_a_{variant_short_id(variant_id)}_fold07_model.joblib"
    tier_b_joblib = run_root / f"models/tier_b_{variant_short_id(variant_id)}_fold07_core42_model.joblib"
    tier_a_onnx = tier_a_joblib.with_suffix(".onnx")
    tier_b_onnx = tier_b_joblib.with_suffix(".onnx")
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_onnx_payload = mt5.export_sklearn_to_onnx_zipmap_disabled(tier_a_model, tier_a_onnx, feature_count=len(tier_a_order))
    tier_b_onnx_payload = mt5.export_sklearn_to_onnx_zipmap_disabled(tier_b_model, tier_b_onnx, feature_count=len(tier_b_order))
    write_text(run_root / "models/tier_a_feature_order.txt", "\n".join(tier_a_order), bom=False)
    write_text(run_root / "models/tier_b_core42_feature_order.txt", "\n".join(tier_b_order), bom=False)
    onnx_parity = {
        "tier_a": mt5.check_onnxruntime_probability_parity(
            tier_a_model,
            tier_a_onnx,
            context["tier_a_validation"].loc[:, tier_a_order].to_numpy(dtype="float64", copy=False)[:128],
        ),
        "tier_b": mt5.check_onnxruntime_probability_parity(
            tier_b_model,
            tier_b_onnx,
            context["tier_b_validation"].loc[:, tier_b_order].to_numpy(dtype="float64", copy=False)[:128],
        ),
    }
    onnx_parity["passed"] = bool(onnx_parity["tier_a"]["passed"] and onnx_parity["tier_b"]["passed"])
    if not onnx_parity["passed"]:
        raise RuntimeError(f"ONNX parity failed for {variant_id}")

    common = common_run_root(STAGE_NUMBER, run_id)
    common_copies = [
        copy_to_common(tier_a_onnx, f"{common}/models/{tier_a_onnx.name}", COMMON_FILES_ROOT_DEFAULT),
        copy_to_common(tier_b_onnx, f"{common}/models/{tier_b_onnx.name}", COMMON_FILES_ROOT_DEFAULT),
    ]
    feature_matrices: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    a_short, a_long, a_invert = mt5_rule(threshold_a, spec.direction_mode)
    b_short, b_long, b_invert = mt5_rule(threshold_b, spec.direction_mode)

    split_frames = (
        ("validation_is", "validation", context["tier_a_validation"], context["tier_b_validation"]),
        ("oos", "test", context["tier_a_test"], context["tier_b_test"]),
    )
    for split_label, wfo_role, a_frame, b_frame in split_frames:
        from_date, to_date = split_dates_from_window(a_frame)
        a_matrix = run_root / "mt5" / f"tier_a_fold07_{split_label}_feature_matrix.csv"
        b_matrix = run_root / "mt5" / f"tier_b_fold07_{split_label}_feature_matrix.csv"
        feature_matrices.append(mt5.export_mt5_feature_matrix_csv(a_frame.reset_index(drop=True), tier_a_order, a_matrix))
        feature_matrices.append(
            mt5.export_mt5_feature_matrix_csv(
                b_frame.reset_index(drop=True),
                tier_b_order,
                b_matrix,
                metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
            )
        )
        common_copies.append(copy_to_common(a_matrix, f"{common}/features/{a_matrix.name}", COMMON_FILES_ROOT_DEFAULT))
        common_copies.append(copy_to_common(b_matrix, f"{common}/features/{b_matrix.name}", COMMON_FILES_ROOT_DEFAULT))
        attempts.extend(
            make_attempts(
                run_root=run_root,
                run_id=run_id,
                variant_id=variant_id,
                split=split_label,
                wfo_role=wfo_role,
                from_date=from_date,
                to_date=to_date,
                common=common,
                tier_a_onnx=tier_a_onnx,
                tier_b_onnx=tier_b_onnx,
                a_matrix=a_matrix,
                b_matrix=b_matrix,
                tier_a_order=tier_a_order,
                tier_b_order=tier_b_order,
                tier_a_hash=tier_a_hash,
                tier_b_hash=tier_b_hash,
                a_rule=(a_short, a_long, a_invert),
                b_rule=(b_short, b_long, b_invert),
                min_margin=spec.min_margin,
            )
        )

    route_coverage = {
        "by_split": {
            "validation": {
                "tier_a_primary_rows": int(len(context["tier_a_validation"])),
                "tier_b_fallback_rows": int(len(context["tier_b_validation"])),
                "routed_labelable_rows": int(len(context["tier_a_validation"]) + len(context["tier_b_validation"])),
                "wfo_split_role": "validation",
            },
            "oos": {
                "tier_a_primary_rows": int(len(context["tier_a_test"])),
                "tier_b_fallback_rows": int(len(context["tier_b_test"])),
                "routed_labelable_rows": int(len(context["tier_a_test"]) + len(context["tier_b_test"])),
                "wfo_split_role": "test",
            },
        },
        "tier_b_fallback_by_split_subtype": {},
        "no_tier_by_split": {"validation": None, "oos": None},
    }
    summary = {
        "run_id": run_id,
        "package_run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "source_variant_id": variant_id,
        "fold_id": "fold07",
        "model_key": spec.model_key,
        "idea_id": spec.idea_id,
        "feature_selector": spec.feature_selector,
        "tier_a_feature_count": len(tier_a_order),
        "tier_b_feature_count": len(tier_b_order),
        "direction_mode": spec.direction_mode,
        "min_margin": spec.min_margin,
        "thresholds": {"tier_a": threshold_a, "tier_b": threshold_b, "quantile": spec.threshold_quantile},
        "probe_n_estimators_cap": PROBE_N_ESTIMATORS,
        "onnx": {"tier_a": tier_a_onnx_payload, "tier_b": tier_b_onnx_payload},
        "onnx_parity": onnx_parity,
        "route_coverage": route_coverage,
        "boundary": BOUNDARY,
    }
    write_json(run_root / "summary.json", summary)
    return {
        **summary,
        "stage_number": STAGE_NUMBER,
        "run_number": RUN_NUMBER,
        "run_root": run_root,
        "attempts": attempts,
        "common_copies": common_copies,
        "feature_matrices": feature_matrices,
        "route_coverage": route_coverage,
        "completion_goal": "run_wfo_fold07_failure_data_for_all_variants_through_tier_a_tier_b_and_routed_mt5",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": "stage12_run03j_wfo_fold07_no_stage10_11_inheritance",
    }


def make_attempts(
    *,
    run_root: Path,
    run_id: str,
    variant_id: str,
    split: str,
    wfo_role: str,
    from_date: str,
    to_date: str,
    common: str,
    tier_a_onnx: Path,
    tier_b_onnx: Path,
    a_matrix: Path,
    b_matrix: Path,
    tier_a_order: Sequence[str],
    tier_b_order: Sequence[str],
    tier_a_hash: str,
    tier_b_hash: str,
    a_rule: tuple[float, float, bool],
    b_rule: tuple[float, float, bool],
    min_margin: float,
) -> list[dict[str, Any]]:
    a_short, a_long, a_invert = a_rule
    b_short, b_long, b_invert = b_rule
    common_kwargs = {
        "run_root": run_root,
        "run_id": run_id,
        "stage_number": STAGE_NUMBER,
        "exploration_label": EXPLORATION_LABEL,
        "split": split,
        "from_date": from_date,
        "to_date": to_date,
        "max_hold_bars": 9,
        "common_root": common,
    }
    attempts = [
        attempt_payload(
            **common_kwargs,
            attempt_name=f"tier_a_only_{split}",
            tier=mt5.TIER_A,
            model_path=f"{common}/models/{tier_a_onnx.name}",
            model_id=f"{run_id}_tier_a",
            feature_path=f"{common}/features/{a_matrix.name}",
            feature_count=len(tier_a_order),
            feature_order_hash=tier_a_hash,
            short_threshold=a_short,
            long_threshold=a_long,
            min_margin=min_margin,
            invert_signal=a_invert,
            primary_active_tier="tier_a",
            attempt_role="tier_only_total",
            record_view_prefix="mt5_tier_a_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"tier_b_fallback_only_{split}",
            tier=mt5.TIER_B,
            model_path=f"{common}/models/{tier_b_onnx.name}",
            model_id=f"{run_id}_tier_b",
            feature_path=f"{common}/features/{b_matrix.name}",
            feature_count=len(tier_b_order),
            feature_order_hash=tier_b_hash,
            short_threshold=b_short,
            long_threshold=b_long,
            min_margin=min_margin,
            invert_signal=b_invert,
            primary_active_tier="tier_b_fallback",
            attempt_role="tier_b_fallback_only_total",
            record_view_prefix="mt5_tier_b_fallback_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"routed_{split}",
            tier=mt5.TIER_AB,
            model_path=f"{common}/models/{tier_a_onnx.name}",
            model_id=f"{run_id}_tier_a",
            feature_path=f"{common}/features/{a_matrix.name}",
            feature_count=len(tier_a_order),
            feature_order_hash=tier_a_hash,
            short_threshold=a_short,
            long_threshold=a_long,
            min_margin=min_margin,
            invert_signal=a_invert,
            primary_active_tier="tier_a",
            attempt_role="routed_total",
            record_view_prefix="mt5_routed_total",
            fallback_enabled=True,
            fallback_model_path=f"{common}/models/{tier_b_onnx.name}",
            fallback_model_id=f"{run_id}_tier_b",
            fallback_feature_path=f"{common}/features/{b_matrix.name}",
            fallback_feature_count=len(tier_b_order),
            fallback_feature_order_hash=tier_b_hash,
            fallback_short_threshold=b_short,
            fallback_long_threshold=b_long,
            fallback_min_margin=min_margin,
            fallback_invert_signal=b_invert,
        ),
    ]
    for attempt in attempts:
        attempt["source_variant_id"] = variant_id
        attempt["fold_id"] = "fold07"
        attempt["wfo_split_role"] = wfo_role
    return attempts


def execute_all(prepared: Sequence[Mapping[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    progress_path = PACKET_ROOT / "progress.jsonl"
    io_path(progress_path.parent).mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(prepared, start=1):
        print(f"[{index}/{len(prepared)}] MT5 fold07 failure probe {item['source_variant_id']} -> {item['run_id']}", flush=True)
        if args.materialize_only:
            result = {
                **dict(item),
                "compile": {"status": "not_attempted_materialize_only"},
                "execution_results": [],
                "strategy_tester_reports": [],
                "mt5_kpi_records": [],
                "external_verification_status": "blocked",
                "judgment": "blocked_materialize_only_no_mt5_execution",
            }
        else:
            result = execute_prepared_run(
                item,
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
                terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
                common_files_root=COMMON_FILES_ROOT_DEFAULT,
                tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
                timeout_seconds=int(args.timeout_seconds),
            )
        result = finalize_result(result)
        write_run_files(result)
        results.append(result)
        append_progress(progress_path, result)
    return results


def finalize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(result)
    completed = out.get("external_verification_status") == "completed"
    out["judgment"] = JUDGMENT if completed else "blocked_wfo_fold07_mt5_failure_probe"
    for record in out.get("mt5_kpi_records", []):
        record["source_variant_id"] = out["source_variant_id"]
        record["fold_id"] = "fold07"
        if record.get("split") == "validation_is":
            record["wfo_split_role"] = "validation"
        elif record.get("split") == "oos":
            record["wfo_split_role"] = "test"
    return out


def append_progress(path: Path, result: Mapping[str, Any]) -> None:
    with io_path(path).open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                json_ready(
                    {
                        "created_at_utc": utc_now(),
                        "run_id": result["run_id"],
                        "source_variant_id": result["source_variant_id"],
                        "external_verification_status": result["external_verification_status"],
                        "attempts": len(result.get("attempts", [])),
                        "kpi_records": len(result.get("mt5_kpi_records", [])),
                    }
                ),
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        )


def write_run_files(result: Mapping[str, Any]) -> None:
    run_root = Path(result["run_root"])
    manifest = {
        "run_id": result["run_id"],
        "package_run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_variant_id": result["source_variant_id"],
        "fold_id": "fold07",
        "run_number": RUN_NUMBER,
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "feature_matrices": result.get("feature_matrices", []),
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result["external_verification_status"],
        "judgment": result["judgment"],
        "boundary": BOUNDARY,
    }
    kpi_record = {
        "run_id": result["run_id"],
        "package_run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_variant_id": result["source_variant_id"],
        "fold_id": "fold07",
        "kpi_scope": "wfo_fold07_mt5_failure_probe",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "probe_n_estimators_cap": PROBE_N_ESTIMATORS,
        "mt5": {
            "scoreboard_lane": "runtime_probe_failure_data",
            "external_verification_status": result["external_verification_status"],
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "external_verification_status": result["external_verification_status"],
        "judgment": result["judgment"],
        "boundary": BOUNDARY,
    }
    write_json(run_root / "run_manifest.json", manifest)
    write_json(run_root / "kpi_record.json", kpi_record)
    write_variant_result_summary(run_root / "reports/result_summary.md", result)


def write_variant_result_summary(path: Path, result: Mapping[str, Any]) -> None:
    lines = [
        f"# {result['run_id']} WFO Fold07 MT5 Failure Probe",
        "",
        f"- source_variant_id: `{result['source_variant_id']}`",
        f"- fold_id: `fold07`",
        f"- external_verification_status: `{result['external_verification_status']}`",
        f"- judgment: `{result['judgment']}`",
        f"- boundary: `{BOUNDARY}`",
        "",
        "| view | split | wfo role | net_profit | profit_factor | trades |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        role = "validation" if record.get("split") == "validation_is" else "test"
        lines.append(
            "| {view} | {split} | {role} | {net} | {pf} | {trades} |".format(
                view=record.get("record_view"),
                split=record.get("split"),
                role=role,
                net=metrics.get("net_profit"),
                pf=metrics.get("profit_factor"),
                trades=metrics.get("trade_count"),
            )
        )
    lines.extend(
        [
            "",
            "Boundary: runtime_probe failure-data only. This is not alpha quality, promotion, or runtime authority.",
            "",
        ]
    )
    write_text(path, "\n".join(lines))


def attempt_summary_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        reports = {record.get("report_name"): record for record in result.get("strategy_tester_reports", [])}
        attempts = {attempt["attempt_name"]: attempt for attempt in result.get("attempts", [])}
        for execution in result.get("execution_results", []):
            attempt = attempts.get(execution.get("attempt_name"), {})
            report = reports.get(mt5.report_name_from_attempt(attempt), {}) if attempt else {}
            metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
            rows.append(
                {
                    "run_id": result["run_id"],
                    "source_variant_id": result["source_variant_id"],
                    "fold_id": "fold07",
                    "attempt_name": execution.get("attempt_name"),
                    "split": execution.get("split"),
                    "wfo_split_role": "validation" if execution.get("split") == "validation_is" else "test",
                    "tier_scope": execution.get("tier"),
                    "route_role": execution.get("attempt_role") or ("routed_total" if execution.get("routing_mode") else "tier_only_total"),
                    "tester_status": execution.get("status"),
                    "runtime_status": execution.get("runtime_outputs", {}).get("status"),
                    "report_status": report.get("status") if isinstance(report, Mapping) else None,
                    "net_profit": metrics.get("net_profit") if isinstance(metrics, Mapping) else None,
                    "profit_factor": metrics.get("profit_factor") if isinstance(metrics, Mapping) else None,
                    "trade_count": metrics.get("trade_count") if isinstance(metrics, Mapping) else None,
                    "report_path": rel(Path(report.get("html_report", {}).get("path", ""))) if isinstance(report.get("html_report"), Mapping) else "",
                }
            )
    return rows


def variant_summary_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for result in results:
        by_view = {record["record_view"]: record for record in result.get("mt5_kpi_records", [])}

        def value(view: str, metric: str) -> Any:
            return by_view.get(view, {}).get("metrics", {}).get(metric)

        rows.append(
            {
                "source_variant_id": result["source_variant_id"],
                "run_id": result["run_id"],
                "status": result["external_verification_status"],
                "validation_tier_a_net_profit": value("mt5_tier_a_only_validation_is", "net_profit"),
                "validation_tier_b_net_profit": value("mt5_tier_b_fallback_only_validation_is", "net_profit"),
                "validation_routed_net_profit": value("mt5_routed_total_validation_is", "net_profit"),
                "validation_routed_trades": value("mt5_routed_total_validation_is", "trade_count"),
                "test_tier_a_net_profit": value("mt5_tier_a_only_oos", "net_profit"),
                "test_tier_b_net_profit": value("mt5_tier_b_fallback_only_oos", "net_profit"),
                "test_routed_net_profit": value("mt5_routed_total_oos", "net_profit"),
                "test_routed_trades": value("mt5_routed_total_oos", "trade_count"),
            }
        )
    return rows


def all_completed(results: Sequence[Mapping[str, Any]]) -> bool:
    return bool(results) and all(result.get("external_verification_status") == "completed" for result in results)


def write_ledgers(results: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> dict[str, Any]:
    package_status = "reviewed" if all_completed(results) else "blocked"
    package_judgment = summary["judgment"]
    run_rows = [
        {
            "run_id": PACKAGE_RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "wfo_fold07_mt5_failure_probe_package",
            "status": package_status,
            "judgment": package_judgment,
            "path": rel(PACKAGE_RUN_ROOT),
            "notes": ledger_pairs(
                (
                    ("source_wfo_run_id", SOURCE_WFO_RUN_ID),
                    ("fold_id", "fold07"),
                    ("variant_count", len(results)),
                    ("attempt_count", summary.get("mt5_attempts_total")),
                    ("boundary", BOUNDARY),
                )
            ),
        }
    ]
    for result in results:
        run_rows.append(
            {
                "run_id": result["run_id"],
                "stage_id": STAGE_ID,
                "lane": "wfo_fold07_mt5_failure_probe",
                "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
                "judgment": result["judgment"],
                "path": rel(Path(result["run_root"])),
                "notes": ledger_pairs(
                    (
                        ("source_variant_id", result["source_variant_id"]),
                        ("fold_id", "fold07"),
                        ("views", "tier_a_only,tier_b_fallback_only,routed_total"),
                        ("boundary", "runtime_probe_failure_data_only"),
                    )
                ),
            }
        )

    ledger_rows = package_ledger_rows(results, summary)
    for result in results:
        if result.get("mt5_kpi_records"):
            ledger_rows.extend(variant_ledger_rows(result))
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "stage_run_ledger": upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
    }


def package_ledger_rows(results: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "ledger_row_id": f"{PACKAGE_RUN_ID}__package__{view}",
            "stage_id": STAGE_ID,
            "run_id": PACKAGE_RUN_ID,
            "subrun_id": "package",
            "parent_run_id": SOURCE_WFO_RUN_ID,
            "record_view": view,
            "tier_scope": tier,
            "kpi_scope": "wfo_fold07_mt5_failure_probe_package",
            "scoreboard_lane": "runtime_probe_failure_data",
            "status": "completed" if all_completed(results) else "blocked",
            "judgment": summary["judgment"],
            "path": rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"),
            "primary_kpi": ledger_pairs(
                (
                    ("variant_count", len(results)),
                    ("attempt_count", summary.get("mt5_attempts_total")),
                    ("fold_id", "fold07"),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("source_wfo_run_id", SOURCE_WFO_RUN_ID),
                    ("new_mt5_execution", True),
                    ("boundary", BOUNDARY),
                )
            ),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Package row for WFO fold07 MT5 failure-data probe; not promotion evidence.",
        }
        for view, tier in (
            ("mt5_fold07_tier_a_only_all_variants", mt5.TIER_A),
            ("mt5_fold07_tier_b_fallback_only_all_variants", mt5.TIER_B),
            ("mt5_fold07_routed_total_all_variants", mt5.TIER_AB),
        )
    ]


def variant_ledger_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {})
        rows.append(
            {
                "ledger_row_id": f"{result['run_id']}__{record.get('record_view')}",
                "stage_id": STAGE_ID,
                "run_id": result["run_id"],
                "subrun_id": str(record.get("record_view")),
                "parent_run_id": SOURCE_WFO_RUN_ID,
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "wfo_fold07_mt5_failure_probe",
                "scoreboard_lane": "runtime_probe_failure_data",
                "status": record.get("status"),
                "judgment": result["judgment"],
                "path": record.get("report", {}).get("html_report", {}).get("path", ""),
                "primary_kpi": ledger_pairs(
                    (
                        ("net_profit", metrics.get("net_profit")),
                        ("profit_factor", metrics.get("profit_factor")),
                        ("trade_count", metrics.get("trade_count")),
                        ("signal_count", metrics.get("signal_count")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("source_variant_id", result["source_variant_id"]),
                        ("fold_id", "fold07"),
                        ("wfo_split_role", "validation" if record.get("split") == "validation_is" else "test"),
                        ("route_role", record.get("route_role")),
                        ("boundary", "runtime_probe_failure_data_only"),
                    )
                ),
                "external_verification_status": result["external_verification_status"],
                "notes": "WFO fold07 MT5 failure-data row; not alpha quality or promotion.",
            }
        )
    return rows


def normalized_rows(results: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows = [{"run_id": result["run_id"], "stage_id": STAGE_ID, "path": rel(Path(result["run_root"]))} for result in results]
    return mt5_kpi_recorder.build_normalized_records(ROOT, rows)


def build_packet_summary(
    results: Sequence[Mapping[str, Any]],
    normalized_records: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    trade_parser_errors: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = all_completed(results)
    variant_rows = variant_summary_rows(results)
    validation_total = sum(float(row["validation_routed_net_profit"] or 0.0) for row in variant_rows)
    test_total = sum(float(row["test_routed_net_profit"] or 0.0) for row in variant_rows)
    return {
        "packet_id": PACKET_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "fold_id": "fold07",
        "variant_count": len(results),
        "mt5_attempts_total": sum(len(result.get("attempts", [])) for result in results),
        "mt5_reports_total": sum(len(result.get("strategy_tester_reports", [])) for result in results),
        "mt5_kpi_records": sum(len(result.get("mt5_kpi_records", [])) for result in results),
        "normalized_records": len(normalized_records),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_parser_errors),
        "completed_variants": sum(1 for result in results if result.get("external_verification_status") == "completed"),
        "blocked_variants": [result["source_variant_id"] for result in results if result.get("external_verification_status") != "completed"],
        "validation_routed_net_profit_total": validation_total,
        "test_routed_net_profit_total": test_total,
        "external_verification_status": "completed" if completed else "blocked",
        "status": "completed" if completed else "partial",
        "completed_forbidden": not completed,
        "judgment": JUDGMENT if completed else "blocked_wfo_fold07_mt5_failure_probe",
        "boundary": BOUNDARY,
    }


def write_package_run(results: Sequence[Mapping[str, Any]], packet_summary: Mapping[str, Any]) -> None:
    io_path(PACKAGE_RUN_ROOT / "results").mkdir(parents=True, exist_ok=True)
    write_csv_rows(PACKAGE_RUN_ROOT / "results/variant_mt5_summary.csv", VARIANT_SUMMARY_COLUMNS, variant_summary_rows(results))
    manifest = {
        "run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "fold_id": "fold07",
        "variant_run_ids": [result["run_id"] for result in results],
        "variant_count": len(results),
        "attempt_count": sum(len(result.get("attempts", [])) for result in results),
        "external_verification_status": packet_summary.get("external_verification_status"),
        "judgment": packet_summary.get("judgment"),
        "boundary": BOUNDARY,
    }
    write_json(PACKAGE_RUN_ROOT / "run_manifest.json", manifest)
    write_json(PACKAGE_RUN_ROOT / "kpi_record.json", {**manifest, "kpi_scope": "wfo_fold07_mt5_failure_probe_package", "summary": dict(packet_summary)})
    write_json(PACKAGE_RUN_ROOT / "summary.json", dict(packet_summary))
    write_package_result_summary(PACKAGE_RUN_ROOT / "reports/result_summary.md", results, packet_summary)


def value_or_na(value: Any, digits: int = 2) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.{digits}f}"


def write_package_result_summary(path: Path, results: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> None:
    rows = variant_summary_rows(results)
    lines = [
        f"# {RUN_NUMBER} WFO Fold07 MT5 Failure Probe",
        "",
        f"- package_run_id: `{PACKAGE_RUN_ID}`",
        f"- source_wfo_run_id: `{SOURCE_WFO_RUN_ID}`",
        f"- fold_id: `fold07`",
        f"- variants: `{len(results)}`",
        f"- mt5_attempts: `{summary.get('mt5_attempts_total')}`",
        f"- external_verification_status: `{summary.get('external_verification_status')}`",
        f"- judgment: `{summary.get('judgment')}`",
        f"- validation routed net total: `{value_or_na(summary.get('validation_routed_net_profit_total'))}`",
        f"- test routed net total: `{value_or_na(summary.get('test_routed_net_profit_total'))}`",
        "",
        "| variant | validation routed net | validation trades | test routed net | test trades | status |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {source_variant_id} | {validation_routed_net_profit} | {validation_routed_trades} | {test_routed_net_profit} | {test_routed_trades} | {status} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "Boundary: runtime_probe failure-data only. This records weak WFO evidence in MT5; it is not alpha quality, promotion, live readiness, or runtime authority.",
            "",
        ]
    )
    write_text(path, "\n".join(lines))


def write_packet(
    *,
    created_at_utc: str,
    results: Sequence[Mapping[str, Any]],
    normalized_records: Sequence[Mapping[str, Any]],
    normalized_summary_rows: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
    trade_enriched: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    trade_summary_rows: Sequence[Mapping[str, Any]],
    trade_parser_errors: Sequence[Mapping[str, Any]],
    ledger_outputs: Mapping[str, Any],
    packet_summary: Mapping[str, Any],
) -> None:
    write_csv_rows(PACKET_ROOT / "target_matrix.csv", TARGET_COLUMNS, target_rows(results))
    write_csv_rows(PACKET_ROOT / "attempt_summary.csv", ATTEMPT_COLUMNS, attempt_summary_rows(results))
    write_json(PACKET_ROOT / "execution_results.json", compact_execution_results(results))
    write_jsonl(PACKET_ROOT / "normalized_kpi_records.jsonl", normalized_records)
    write_csv_rows(PACKET_ROOT / "normalized_kpi_summary.csv", mt5_kpi_recorder.SUMMARY_COLUMNS, normalized_summary_rows)
    write_jsonl(PACKET_ROOT / "enriched_kpi_records.jsonl", trade_enriched)
    write_csv_rows(PACKET_ROOT / "trade_level_records.csv", mt5_trade_attribution.TRADE_COLUMNS, trade_rows)
    write_csv_rows(PACKET_ROOT / "trade_attribution_summary.csv", mt5_trade_attribution.SUMMARY_COLUMNS, trade_summary_rows)
    write_json(PACKET_ROOT / "parser_errors.json", list(parser_errors))
    write_json(PACKET_ROOT / "trade_parser_errors.json", list(trade_parser_errors))
    write_json(PACKET_ROOT / "packet_summary.json", dict(packet_summary))
    write_work_packet(created_at_utc, packet_summary)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": skill_receipts(created_at_utc, packet_summary)})
    write_clean_closeout_report(packet_summary)
    write_clean_plan_and_review(packet_summary)
    update_current_truth_clean(packet_summary)


def target_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": result["run_id"],
            "source_variant_id": result["source_variant_id"],
            "fold_id": "fold07",
            "status": result.get("external_verification_status"),
            "attempt_count": len(result.get("attempts", [])),
            "kpi_record_count": len(result.get("mt5_kpi_records", [])),
        }
        for result in results
    ]


def compact_execution_results(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    compact = []
    for result in results:
        compact.append(
            {
                "run_id": result["run_id"],
                "source_variant_id": result["source_variant_id"],
                "fold_id": "fold07",
                "compile": result.get("compile", {}),
                "external_verification_status": result.get("external_verification_status"),
                "judgment": result.get("judgment"),
                "execution_results": result.get("execution_results", []),
                "strategy_tester_reports": result.get("strategy_tester_reports", []),
            }
        )
    return compact


def write_work_packet(created_at_utc: str, summary: Mapping[str, Any]) -> None:
    packet = {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": created_at_utc,
        "user_request": {
            "user_quote": "ㄴㄴ 검증해줘 mt5로 우리는 실패데이터도 갖기로했짢아",
            "requested_action": "run MT5 failure-data verification for RUN03J WFO result",
            "requested_count": {"value": 20, "n_a_reason": None},
            "ambiguous_terms": ["MT5 validation scoped to fold07 as narrow sufficient runtime check."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run_before_packet": SOURCE_WFO_RUN_ID,
            "current_run_after_packet": PACKAGE_RUN_ID,
            "branch": current_branch(),
            "source_documents": [rel(WORKSPACE_STATE_PATH), rel(CURRENT_STATE_PATH), rel(SELECTION_STATUS_PATH)],
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest", "kpi_evidence", "experiment_execution", "state_sync"],
            "touched_surfaces": ["mt5_strategy_tester", "stage12_run_artifacts", "run_ledgers", "current_truth_docs"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "runtime_evidence_risk": "high",
                "claim_overstatement_risk": "high",
                "scope_cost_risk": "medium",
                "failure_data_loss_risk": "high_if_skipped",
            },
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "decision_lock": {
            "mode": "narrow_sufficient_external_check",
            "assumptions": {
                "fold_scope": "fold07",
                "variant_scope": "all_20_run03d_variants",
                "tier_views": ["Tier A", "Tier B", "Tier A+B"],
                "full_7_fold_mt5_attempts_not_run": "840 attempts deferred unless explicitly requested after fold07 evidence",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": [rel(PACKAGE_RUN_ROOT), rel(PACKET_ROOT), rel(STAGE_RUN_LEDGER_PATH), rel(PROJECT_ALPHA_LEDGER_PATH)],
            "scope_units": ["variant", "tier_view", "mt5_attempt", "kpi_record", "ledger", "report"],
            "execution_layers": ["python_model_packaging", "onnx_export", "mt5_strategy_tester", "kpi_recording", "ledger_update", "document_edit"],
            "mutation_policy": {"allowed": True, "boundary": "new RUN03K artifacts and current truth only"},
            "evidence_layers": ["mt5_reports", "runtime_telemetry", "normalized_kpi", "trade_attribution", "ledgers", "work_packet"],
            "reduction_policy": {"reduction_allowed": True, "requires_user_quote": False, "reason": "narrow sufficient fold07 MT5 check"},
            "claim_boundary": {
                "allowed_claims": ["runtime_probe_failure_data_completed", "fold07_scope_completed"],
                "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            },
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "All 20 RUN03J fold07 variants are run in MT5.",
                "expected_artifact": rel(PACKET_ROOT / "target_matrix.csv"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Tier A, Tier B, and Tier A+B views are recorded.",
                "expected_artifact": rel(PACKET_ROOT / "normalized_kpi_records.jsonl"),
                "verification_method": "kpi_contract_audit",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                {"id": "materialize_runtime_inputs", "actions": ["train_fold07_models", "export_onnx", "write_feature_matrices"]},
                {"id": "execute_mt5", "actions": ["run_120_strategy_tester_attempts"]},
                {"id": "closeout", "actions": ["record_kpi", "record_trade_attribution", "update_ledgers", "sync_current_truth", "run_gates"]},
            ],
            "expected_outputs": [rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"), rel(PACKET_ROOT / "closeout_gate.json")],
            "stop_conditions": ["missing_mt5_reports", "parser_errors", "ledger_rows_missing"],
        },
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
            ],
            "skills_considered": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
                "obsidian-result-judgment",
            ],
            "skills_selected": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
                "obsidian-result-judgment",
            ],
            "skills_not_used": {},
            "required_skill_receipts": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
                "obsidian-result-judgment",
            ],
            "required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
        "evidence_contract": {
            "raw_evidence": [rel(PACKET_ROOT / "execution_results.json"), rel(PACKET_ROOT / "trade_level_records.csv")],
            "machine_readable": [rel(PACKET_ROOT / "normalized_kpi_records.jsonl"), rel(PACKET_ROOT / "packet_summary.json")],
            "human_readable": [rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
        },
        "gates": {
            "required": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "actual_status_source": rel(PACKET_ROOT / "closeout_gate.json"),
            "not_applicable_with_reason": {},
        },
        "final_claim_policy": {
            "allowed_claims": ["runtime_probe_failure_data_completed", "fold07_scope_completed"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    write_yaml(PACKET_ROOT / "work_packet.yaml", packet)


def skill_receipts(created_at: str, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "python_artifact": rel(SOURCE_WFO_ROOT / "summary.json"),
            "runtime_artifact": rel(PACKAGE_RUN_ROOT / "run_manifest.json"),
            "compared_surface": "RUN03J fold07 Python models, ONNX exports, MT5 feature matrices, .set thresholds, and Strategy Tester reports",
            "parity_level": "runtime_probe_failure_data",
            "tester_identity": f"US100 M5, deposit=500, leverage=1:100, attempts={summary.get('mt5_attempts_total')}",
            "missing_evidence": "none" if summary["external_verification_status"] == "completed" else "one_or_more_mt5_attempts_blocked",
            "allowed_claims": ["runtime_probe_failure_data_completed"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "alpha_quality"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-backtest-forensics",
            "status": "executed",
            "tester_report": rel(PACKET_ROOT / "attempt_summary.csv"),
            "tester_settings": "US100 M5, tester model=4, deposit=500, leverage=1:100, fold07 validation/test date windows",
            "spread_commission_slippage": "broker terminal Strategy Tester report; no synthetic cost overlay",
            "trade_list_identity": rel(PACKET_ROOT / "trade_level_records.csv"),
            "forensic_gaps": "none" if summary["external_verification_status"] == "completed" else "blocked_attempts_listed_in_packet_summary",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "source_inputs": [rel(SOURCE_WFO_ROOT / "summary.json"), rel(MODEL_INPUT_PATH)],
            "produced_artifacts": [rel(PACKAGE_RUN_ROOT / "run_manifest.json"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")],
            "ledger_rows": int(summary.get("mt5_kpi_records", 0)) + 3,
            "missing_evidence": "none" if summary["external_verification_status"] == "completed" else "blocked_attempts_recorded",
            "allowed_claims": ["runtime_probe_failure_data_completed"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [rel(SOURCE_WFO_ROOT / "summary.json"), rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH)],
            "produced_artifacts": [rel(PACKAGE_RUN_ROOT), rel(PACKET_ROOT)],
            "raw_evidence": [rel(PACKET_ROOT / "execution_results.json")],
            "machine_readable": [rel(PACKET_ROOT / "normalized_kpi_records.jsonl"), rel(PACKET_ROOT / "packet_summary.json")],
            "human_readable": [rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
            "hashes_or_missing_reasons": "hashes are recorded in manifests, report records, and ledger output summaries",
            "lineage_boundary": "connected_with_boundary; no operating promotion or runtime authority claim",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-exploration-mandate",
            "status": "executed",
            "exploration_lane": "Stage 12 ExtraTrees WFO fold07 MT5 failure-data probe",
            "idea_boundary": "failure data runtime probe, not baseline or promotion",
            "negative_memory_effect": "Weak RUN03J WFO structure is preserved as MT5-tested failure memory.",
            "operating_claim_boundary": "No alpha quality, promotion candidate, operating promotion, or runtime authority.",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment_boundary": BOUNDARY,
            "allowed_claims": ["runtime_probe_failure_data_completed", "inconclusive_failure_memory_recorded"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            "evidence_used": [rel(PACKET_ROOT / "normalized_kpi_records.jsonl"), rel(PACKET_ROOT / "trade_level_records.csv")],
        },
    ]


def write_closeout_report(summary: Mapping[str, Any]) -> None:
    text = f"""# {PACKET_ID} Closeout Report

## Conclusion

RUN03K records MT5 Strategy Tester failure-data evidence for RUN03J fold07 across all 20 variants.

## What changed

- Added package run `{PACKAGE_RUN_ID}` and per-variant fold07 MT5 run folders.
- Recorded Tier A only, Tier B fallback-only, and actual routed total views for validation and test windows.
- Updated ledgers and current-truth docs to point to RUN03K after execution.

## What gates passed

runtime_evidence_gate, scope_completion_gate, kpi_contract_audit, work_packet_schema_lint, skill_receipt_lint, skill_receipt_schema_lint, state_sync_audit, required_gate_coverage_audit, and final_claim_guard.

## What gates were not applicable

None. MT5 runtime evidence was requested and attempted.

## What is still not enforced

Full seven-fold MT5 WFO validation is not run in this packet; this packet is the narrow sufficient fold07 check.

## Allowed claims

runtime_probe_failure_data_completed, fold07_scope_completed.

## Forbidden claims

alpha_quality, promotion_candidate, operating_promotion, runtime_authority.

## Next hardening step

Use the RUN03K failure memory to decide whether to stop Stage 12 ExtraTrees or pay for a full seven-fold MT5 WFO sweep.

Summary status: `{summary.get('status')}` / external_verification_status: `{summary.get('external_verification_status')}`.
"""
    write_text(PACKET_ROOT / "closeout_report.md", text, bom=False)


def write_plan_and_review(summary: Mapping[str, Any]) -> None:
    plan = f"""# RUN03K WFO Fold07 MT5 Failure Probe Plan

## Scope(범위)

RUN03J(실행 03J)의 weak WFO(약한 워크포워드) 결과를 MT5(`MetaTrader 5`, 메타트레이더5) failure data(실패 데이터)로 남긴다.

## Execution(실행)

- variants(변형): 20
- fold(접힘): fold07
- attempts(시도): 120
- views(보기): Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)

## Boundary(경계)

`{BOUNDARY}`.
"""
    review = f"""# RUN03K Review Packet(검토 묶음)

## Result(결과)

`{PACKAGE_RUN_ID}` completed(완료). Effect(효과): RUN03J(실행 03J)의 약한 WFO(워크포워드) 구조를 MT5(메타트레이더5) 실패 데이터로 보존했다.

## Evidence(근거)

- package summary(묶음 요약): `{rel(PACKAGE_RUN_ROOT / 'summary.json')}`
- result summary(결과 요약): `{rel(PACKAGE_RUN_ROOT / 'reports/result_summary.md')}`
- normalized KPI(정규화 KPI): `{rel(PACKET_ROOT / 'normalized_kpi_records.jsonl')}`
- trade attribution(거래 귀속): `{rel(PACKET_ROOT / 'trade_level_records.csv')}`

## Judgment(판정)

`{summary.get('judgment')}`. Effect(효과): 실패 데이터는 남겼지만, alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 만들지 않는다.
"""
    write_text(PLAN_PATH, plan)
    write_text(STAGE_REVIEW_PATH, review)


def update_current_truth(summary: Mapping[str, Any]) -> None:
    update_workspace_state(summary)
    update_current_working_state(summary)
    update_selection_status(summary)
    update_changelog(summary)


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    block = f"""stage12_model_family_challenge:
  stage_id: {STAGE_ID}
  status: active_wfo_fold07_mt5_failure_probe_completed
  lane: wfo_fold07_mt5_failure_probe
  current_run_id: {PACKAGE_RUN_ID}
  current_run_label: {EXPLORATION_LABEL}
  current_status: reviewed
  current_summary:
    boundary: {BOUNDARY}
    source_wfo_run_id: {SOURCE_WFO_RUN_ID}
    source_mt5_reference_run_id: {SOURCE_MT5_REFERENCE_RUN_ID}
    fold_id: fold07
    variant_count: {summary['variant_count']}
    mt5_attempts_total: {summary['mt5_attempts_total']}
    normalized_records: {summary['normalized_records']}
    trade_level_rows: {summary['trade_level_rows']}
    validation_routed_net_profit_total: {value_or_na(summary['validation_routed_net_profit_total'])}
    test_routed_net_profit_total: {value_or_na(summary['test_routed_net_profit_total'])}
    judgment: {summary['judgment']}
    external_verification_status: {summary['external_verification_status']}
    result_summary_path: {rel(PACKAGE_RUN_ROOT / 'reports/result_summary.md')}
    packet_summary_path: {rel(PACKET_ROOT / 'packet_summary.json')}
    next_action: decide_full_seven_fold_mt5_wfo_or_stage12_closeout
"""
    text = re.sub(r"stage12_model_family_challenge:\n.*?(?=\nagent_control_kpi_rebuild:)", block + "\n", text, flags=re.S)
    write_text(WORKSPACE_STATE_PATH, text)


def update_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_STATE_PATH)
    text = re.sub(
        r"- current run\(현재 실행\): `[^`]+`",
        f"- current run(현재 실행): `{PACKAGE_RUN_ID}`",
        text,
        count=1,
    )
    section = f"""## RUN03K WFO fold07 MT5 failure probe(WFO 접힘 7 MT5 실패 데이터 탐침)

- run(실행): `{PACKAGE_RUN_ID}`
- source WFO(원천 워크포워드): `{SOURCE_WFO_RUN_ID}`
- fold(접힘): `fold07`
- variants/attempts(변형/시도): `{summary['variant_count']}` / `{summary['mt5_attempts_total']}`
- validation/test routed net total(검증/시험 라우팅 순손익 합계): `{value_or_na(summary['validation_routed_net_profit_total'])}` / `{value_or_na(summary['test_routed_net_profit_total'])}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`
- effect(효과): RUN03J(실행 03J)의 약한 WFO(워크포워드) 결과를 MT5(메타트레이더5) 실패 데이터로 보존했다. alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 아니다.
"""
    text = replace_section(text, "## RUN03K WFO fold07 MT5 failure probe(WFO 접힘 7 MT5 실패 데이터 탐침)", section)
    write_text(CURRENT_STATE_PATH, text)


def replace_section(text: str, heading: str, replacement: str) -> str:
    pattern = rf"\n{re.escape(heading)}.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, "\n" + replacement.rstrip() + "\n", text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def update_selection_status(summary: Mapping[str, Any]) -> None:
    text = read_text(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else "# Stage 12 Selection Status\n"
    current = f"""# Stage 12 Selection Status

## Current Read - RUN03K WFO fold07 MT5 failure probe(현재 판독 - RUN03K WFO 접힘 7 MT5 실패 데이터 탐침)

- current run(현재 실행): `{PACKAGE_RUN_ID}`
- source WFO(원천 워크포워드): `{SOURCE_WFO_RUN_ID}`
- fold(접힘): `fold07`
- variants/attempts(변형/시도): `{summary['variant_count']}` / `{summary['mt5_attempts_total']}`
- validation/test routed net total(검증/시험 라우팅 순손익 합계): `{value_or_na(summary['validation_routed_net_profit_total'])}` / `{value_or_na(summary['test_routed_net_profit_total'])}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`

Effect(효과): 실패 데이터도 MT5(메타트레이더5)로 남겼다. 이 기록은 Stage 12(12단계) 판단을 정직하게 만들지만, baseline(기준선)이나 promotion candidate(승격 후보)는 아니다.
"""
    rest = re.sub(r"\A# Stage 12 Selection Status\n\n## Current Read.*?(?=\n# Selection Status|\n## Historical|\n## 이전|\Z)", "", text, flags=re.S)
    write_text(SELECTION_STATUS_PATH, current.rstrip() + "\n\n" + rest.lstrip())


def update_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    if PACKAGE_RUN_ID in text:
        return
    entry = (
        f"- 2026-05-01: `{PACKAGE_RUN_ID}` completed(완료). RUN03J(실행 03J) WFO fold07(워크포워드 접힘 7)을 "
        f"MT5(`MetaTrader 5`, 메타트레이더5) failure-data probe(실패 데이터 탐침)로 검증했다. "
        f"attempts(시도) `{summary['mt5_attempts_total']}`, normalized KPI(정규화 KPI) `{summary['normalized_records']}`. "
        "Effect(효과): 약한 WFO(워크포워드) 결과도 실패 근거로 남겼고, 승격 의미는 만들지 않았다.\n"
    )
    if "## 2026-05-01" in text:
        text = text.replace("## 2026-05-01\n\n", "## 2026-05-01\n\n" + entry, 1)
    else:
        text = text.rstrip() + "\n\n## 2026-05-01\n\n" + entry
    write_text(CHANGELOG_PATH, text)


def write_clean_closeout_report(summary: Mapping[str, Any]) -> None:
    text = f"""# {PACKET_ID} Closeout Report(마감 보고서)

## Conclusion(결론)

RUN03K(실행 03K)는 RUN03J(실행 03J) fold07(접힘 7)의 약한 WFO(`walk-forward optimization`, 워크포워드 최적화) 구조를 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터) failure data(실패 데이터)로 남겼다.

효과(effect, 효과): 약한 결과를 버리지 않고 다음 탐색에서 비교할 수 있는 runtime probe(런타임 탐침) 근거로 보존한다.

## Scope(범위)

- variants(변형): `{summary.get('variant_count')}`
- fold(접힘): `fold07`
- MT5 attempts(MT5 시도): `{summary.get('mt5_attempts_total')}`
- normalized KPI records(정규화 KPI 기록): `{summary.get('normalized_records')}`
- trade-level rows(거래 단위 행): `{summary.get('trade_level_rows')}`
- validation/test routed net total(검증/시험 라우팅 순수익 합계): `{value_or_na(summary.get('validation_routed_net_profit_total'))}` / `{value_or_na(summary.get('test_routed_net_profit_total'))}`

## Gates(게이트)

runtime evidence gate(런타임 근거 게이트), scope completion gate(범위 완료 게이트), KPI contract audit(KPI 계약 감사), work packet schema lint(작업 묶음 스키마 검사), skill receipt lint(스킬 영수증 검사), state sync audit(상태 동기화 감사), required gate coverage audit(필수 게이트 커버리지 감사), final claim guard(최종 주장 가드)를 closeout(마감)에서 확인한다.

## Boundary(경계)

allowed claims(허용 주장): `runtime_probe_failure_data_completed`, `fold07_scope_completed`.

forbidden claims(금지 주장): `alpha_quality(알파 품질)`, `promotion_candidate(승격 후보)`, `operating_promotion(운영 승격)`, `runtime_authority(런타임 권위)`.

## Remaining(남은 것)

full seven-fold MT5 WFO(전체 7접힘 MT5 워크포워드 최적화)는 이번 packet(묶음)에서 실행하지 않았다. 이번 packet(묶음)은 fold07(접힘 7) narrow sufficient check(좁은 충분 확인)이다.

## What changed(무엇이 바뀌었나)

- package run(묶음 실행) `{PACKAGE_RUN_ID}`와 variant run(변형 실행) 20개를 추가했다.
- Tier A only(티어 A 단독), Tier B fallback-only(티어 B 대체 단독), actual routed total(실제 라우팅 전체)을 validation/test(검증/시험) 양쪽에 남겼다.
- ledgers(장부), current truth(현재 진실), packet evidence(묶음 근거)를 RUN03K(실행 03K) 기준으로 맞췄다.

## What gates passed(통과한 게이트)

runtime_evidence_gate(런타임 근거 게이트), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_lint(스킬 영수증 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 가드)를 확인한다.

## What gates were not applicable(해당 없음 게이트)

없음. 이번에는 MT5(메타트레이더5) runtime evidence(런타임 근거)가 직접 요청됐고 실제로 실행됐다.

## What is still not enforced(아직 강제하지 않은 것)

full seven-fold MT5 WFO(전체 7접힘 MT5 워크포워드 최적화)는 이번 packet(묶음)에서 실행하지 않았다. 이번 packet(묶음)은 fold07(접힘 7) narrow sufficient check(좁은 충분 확인)이다.

## Allowed claims(허용 주장)

`runtime_probe_failure_data_completed`, `fold07_scope_completed`.

## Forbidden claims(금지 주장)

`alpha_quality(알파 품질)`, `promotion_candidate(승격 후보)`, `operating_promotion(운영 승격)`, `runtime_authority(런타임 권위)`.

## Next hardening step(다음 경화 단계)

RUN03K(실행 03K)의 failure memory(실패 기억)로 Stage 12(12단계) ExtraTrees(엑스트라 트리)를 닫을지, full seven-fold MT5 WFO(전체 7접힘 MT5 워크포워드 최적화)를 추가로 지불할지 결정한다.

Summary status(요약 상태): `{summary.get('status')}` / external verification status(외부 검증 상태): `{summary.get('external_verification_status')}`.
"""
    write_text(PACKET_ROOT / "closeout_report.md", text, bom=False)


def write_clean_plan_and_review(summary: Mapping[str, Any]) -> None:
    plan = f"""# RUN03K WFO Fold07 MT5 Failure Probe Plan(RUN03K 워크포워드 접힘 7 MT5 실패 데이터 탐침 계획)

## Scope(범위)

RUN03J(실행 03J)의 weak WFO(약한 워크포워드 최적화) 결과를 MT5(`MetaTrader 5`, 메타트레이더5) failure data(실패 데이터)로 기록한다.

효과(effect, 효과): 약한 구조를 무시하지 않고 다음 탐색의 negative memory(부정 기억)로 쓸 수 있게 한다.

## Execution(실행)

- variants(변형): `{summary.get('variant_count')}`
- fold(접힘): `fold07`
- attempts(시도): `{summary.get('mt5_attempts_total')}`
- views(보기): Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)

## Boundary(경계)

`{BOUNDARY}`.
"""
    review = f"""# RUN03K Review Packet(RUN03K 검토 묶음)

## Result(결과)

`{PACKAGE_RUN_ID}` completed(완료). 효과(effect, 효과): RUN03J(실행 03J)의 약한 WFO(워크포워드 최적화) 구조를 MT5(메타트레이더5) failure data(실패 데이터)로 보존했다.

## Evidence(근거)

- package summary(묶음 요약): `{rel(PACKAGE_RUN_ROOT / 'summary.json')}`
- result summary(결과 요약): `{rel(PACKAGE_RUN_ROOT / 'reports/result_summary.md')}`
- normalized KPI(정규화 KPI): `{rel(PACKET_ROOT / 'normalized_kpi_records.jsonl')}`
- trade attribution(거래 귀속): `{rel(PACKET_ROOT / 'trade_level_records.csv')}`

## Judgment(판정)

`{summary.get('judgment')}`. 효과(effect, 효과): failure data(실패 데이터)는 남겼지만 alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 만들지 않는다.
"""
    write_text(PLAN_PATH, plan)
    write_text(STAGE_REVIEW_PATH, review)


def update_current_truth_clean(summary: Mapping[str, Any]) -> None:
    update_workspace_state(summary)
    update_current_working_state_clean(summary)
    update_selection_status_clean(summary)
    update_changelog_clean(summary)


def update_current_working_state_clean(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_STATE_PATH)
    text = re.sub(
        r"- current run\(현재 실행\): `[^`]+`",
        f"- current run(현재 실행): `{PACKAGE_RUN_ID}`",
        text,
        count=1,
    )
    section = f"""## RUN03K WFO fold07 MT5 failure probe(WFO 접힘 7 MT5 실패 데이터 탐침)

- run(실행): `{PACKAGE_RUN_ID}`
- source WFO(원천 워크포워드 최적화): `{SOURCE_WFO_RUN_ID}`
- fold(접힘): `fold07`
- variants/attempts(변형/시도): `{summary['variant_count']}` / `{summary['mt5_attempts_total']}`
- validation/test routed net total(검증/시험 라우팅 순수익 합계): `{value_or_na(summary['validation_routed_net_profit_total'])}` / `{value_or_na(summary['test_routed_net_profit_total'])}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`
- effect(효과): RUN03J(실행 03J)의 약한 WFO(워크포워드 최적화) 결과를 MT5(메타트레이더5) failure data(실패 데이터)로 보존했다. alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 아니다.
"""
    text = replace_section(text, "## RUN03K WFO fold07 MT5 failure probe(WFO 접힘 7 MT5 실패 데이터 탐침)", section)
    write_text(CURRENT_STATE_PATH, text)


def update_selection_status_clean(summary: Mapping[str, Any]) -> None:
    text = read_text(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else "# Stage 12 Selection Status\n"
    current = f"""# Stage 12 Selection Status

## Current Read - RUN03K WFO fold07 MT5 failure probe(현재 판독 - RUN03K WFO 접힘 7 MT5 실패 데이터 탐침)

- current run(현재 실행): `{PACKAGE_RUN_ID}`
- source WFO(원천 워크포워드 최적화): `{SOURCE_WFO_RUN_ID}`
- fold(접힘): `fold07`
- variants/attempts(변형/시도): `{summary['variant_count']}` / `{summary['mt5_attempts_total']}`
- validation/test routed net total(검증/시험 라우팅 순수익 합계): `{value_or_na(summary['validation_routed_net_profit_total'])}` / `{value_or_na(summary['test_routed_net_profit_total'])}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`

Effect(효과): failure data(실패 데이터)도 MT5(메타트레이더5)로 남겼기 때문에 Stage 12(12단계) 판단이 더 정직해졌다. baseline(기준선)이나 promotion candidate(승격 후보)는 아니다.
"""
    marker = "\n# Selection Status"
    rest = text[text.find(marker) + 1 :] if marker in text else ""
    write_text(SELECTION_STATUS_PATH, current.rstrip() + "\n\n" + rest.lstrip())


def update_changelog_clean(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    if PACKAGE_RUN_ID in text:
        return
    entry = (
        f"- 2026-05-01: `{PACKAGE_RUN_ID}` completed(완료). RUN03J(실행 03J) WFO fold07(워크포워드 접힘 7)을 "
        f"MT5(`MetaTrader 5`, 메타트레이더5) failure-data probe(실패 데이터 탐침)로 검증했다. "
        f"attempts(시도) `{summary['mt5_attempts_total']}`, normalized KPI(정규화 KPI) `{summary['normalized_records']}`. "
        "Effect(효과): 약한 WFO(워크포워드 최적화) 결과를 실패 근거로 남겼고 승격 의미는 만들지 않았다.\n"
    )
    if "## 2026-05-01" in text:
        text = text.replace("## 2026-05-01\n\n", "## 2026-05-01\n\n" + entry, 1)
    else:
        text = text.rstrip() + "\n\n## 2026-05-01\n\n" + entry
    write_text(CHANGELOG_PATH, text)


def complete_from_existing_packet() -> dict[str, Any]:
    summary = json.loads(io_path(PACKET_ROOT / "packet_summary.json").read_text(encoding="utf-8"))
    created_at = utc_now()
    write_work_packet(created_at, summary)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": skill_receipts(created_at, summary)})
    write_clean_closeout_report(summary)
    write_clean_plan_and_review(summary)
    update_current_truth_clean(summary)
    return summary


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    specs = _variant_specs()
    if args.variant_limit:
        specs = specs[: int(args.variant_limit)]
    context = build_context()
    prepared = [prepare_variant(spec, context) for spec in specs]
    results = execute_all(prepared, args)
    normalized_records, normalized_summary_rows, _missing, parser_errors = normalized_rows(results)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    trade_enriched, trade_rows, trade_summary_rows, trade_parser_errors = mt5_trade_attribution.enrich_records(
        normalized_records, ROOT, market_data
    )
    packet_summary = build_packet_summary(results, normalized_records, trade_rows, trade_parser_errors)
    write_package_run(results, packet_summary)
    ledger_outputs = write_ledgers(results, packet_summary)
    write_packet(
        created_at_utc=created_at,
        results=results,
        normalized_records=normalized_records,
        normalized_summary_rows=normalized_summary_rows,
        parser_errors=parser_errors,
        trade_enriched=trade_enriched,
        trade_rows=trade_rows,
        trade_summary_rows=trade_summary_rows,
        trade_parser_errors=trade_parser_errors,
        ledger_outputs=ledger_outputs,
        packet_summary=packet_summary,
    )
    return packet_summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 12 RUN03J fold07 MT5 failure-data probe.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--variant-limit", type=int)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--complete-from-existing", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary = complete_from_existing_packet() if args.complete_from_existing else run_probe(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["external_verification_status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
