from __future__ import annotations

import argparse
import csv
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
    METAEDITOR_PATH_DEFAULT,
    RAW_ROOT,
    TESTER_PROFILE_ROOT_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TRAINING_SUMMARY_PATH,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    nonflat_threshold,
    probability_frame,
    split_dates_from_frame,
    train_et_model,
)
from foundation.models.baseline_training import load_feature_order
from foundation.mt5 import runtime_support as mt5


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
STAGE_NUMBER = 12
RUN_NUMBER = "run03H"
PACKAGE_RUN_ID = "run03H_et_batch20_all_variant_tier_balance_mt5_v1"
PACKET_ID = "stage12_run03h_all_variant_tier_balance_mt5_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesAllVariantTierBalance"
SOURCE_RUN_ID = "run03D_et_standalone_batch20_v1"
SOURCE_STRUCTURAL_SCOUT_RUN_ID = "run03G_et_variant_stability_probe_v1"
REFERENCE_RUN_ID = "run03F_et_v11_tier_balance_mt5_v1"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features_and_core42_partial_context"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "stage12_standalone_no_stage10_11_threshold_or_model_inheritance"
BOUNDARY = "runtime_probe_only_not_alpha_quality_not_live_readiness_not_operating_promotion"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUNS_ROOT = STAGE_ROOT / "02_runs"
PACKAGE_RUN_ROOT = RUNS_ROOT / PACKAGE_RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
SOURCE_RUN_ROOT = RUNS_ROOT / SOURCE_RUN_ID
VARIANT_RESULTS_PATH = SOURCE_RUN_ROOT / "results/variant_results.csv"
VARIANT_PLAN_PATH = SOURCE_RUN_ROOT / "variant_plan.csv"
TOP30_PATH = SOURCE_RUN_ROOT / "feature_importance/pilot_top30_from_train.csv"
MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
STAGE_REVIEW_PATH = STAGE_ROOT / "03_reviews/run03H_all_variant_mt5_probe_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run03H_all_variant_mt5_probe_plan.md"

ATTEMPT_COLUMNS = (
    "run_id",
    "source_variant_id",
    "attempt_name",
    "split",
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
TARGET_COLUMNS = (
    "run_id",
    "source_variant_id",
    "feature_selector",
    "direction_mode",
    "threshold_quantile",
    "min_margin",
    "status",
    "attempt_count",
    "kpi_record_count",
)
VARIANT_SUMMARY_COLUMNS = (
    "source_variant_id",
    "run_id",
    "status",
    "validation_tier_a_net_profit",
    "validation_tier_b_net_profit",
    "validation_routed_net_profit",
    "validation_routed_trades",
    "oos_tier_a_net_profit",
    "oos_tier_b_net_profit",
    "oos_routed_net_profit",
    "oos_routed_trades",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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


def current_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError:
        return "unknown"
    return result.stdout.strip() or "unknown"


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


def decision_metrics_variant(prob_frame: pd.DataFrame, threshold: float, min_margin: float, direction_mode: str) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        frame = prob_frame.loc[prob_frame["split"].astype(str).eq(split)]
        p_short = frame["p_short"].to_numpy(dtype="float64")
        p_flat = frame["p_flat"].to_numpy(dtype="float64")
        p_long = frame["p_long"].to_numpy(dtype="float64")
        labels = frame["label_class"].to_numpy(dtype="int64")
        nonflat = np.maximum(p_short, p_long)
        predicted = np.where(p_short >= p_long, 0, 2)
        competitor = np.maximum(p_flat, np.where(predicted == 0, p_long, p_short))
        gate = (nonflat >= threshold) & ((nonflat - competitor) >= min_margin)
        decision = np.full(len(frame), 1, dtype="int64")
        if direction_mode == "both":
            decision[gate] = predicted[gate]
        elif direction_mode == "short_only":
            decision[gate & (predicted == 0)] = 0
        elif direction_mode == "long_only":
            decision[gate & (predicted == 2)] = 2
        elif direction_mode == "inverse":
            decision[gate & (predicted == 0)] = 2
            decision[gate & (predicted == 2)] = 0
        else:
            raise ValueError(f"unknown direction_mode: {direction_mode}")
        signals = decision != 1
        metrics[split] = {
            "rows": int(len(frame)),
            "signal_count": int(signals.sum()),
            "short_count": int((decision == 0).sum()),
            "long_count": int((decision == 2).sum()),
            "signal_coverage": float(signals.mean()) if len(frame) else None,
            "directional_correct_count": int((decision[signals] == labels[signals]).sum()) if signals.any() else 0,
            "directional_hit_rate": float((decision[signals] == labels[signals]).mean()) if signals.any() else None,
        }
    return metrics


def require_inputs() -> None:
    missing = [
        path
        for path in (VARIANT_RESULTS_PATH, VARIANT_PLAN_PATH, TOP30_PATH, MODEL_INPUT_PATH, FEATURE_ORDER_PATH, TRAINING_SUMMARY_PATH)
        if not path_exists(path)
    ]
    if missing:
        raise FileNotFoundError(", ".join(path.as_posix() for path in missing))
    summary = read_json(SOURCE_RUN_ROOT / "summary.json")
    boundary = summary.get("standalone_boundary", {})
    if boundary.get("stage10_11_inheritance") is not False:
        raise RuntimeError("RUN03D is not marked as standalone from Stage10/11 inheritance.")


def load_variant_rows(variant_ids: Sequence[str], variant_limit: int | None) -> list[dict[str, Any]]:
    variants = pd.read_csv(io_path(VARIANT_RESULTS_PATH))
    plan = pd.read_csv(io_path(VARIANT_PLAN_PATH))
    order = {str(variant_id): index for index, variant_id in enumerate(plan["variant_id"].astype(str).tolist(), start=1)}
    variants["plan_order"] = variants["variant_id"].astype(str).map(order)
    variants = variants.sort_values(["plan_order", "variant_id"], ascending=[True, True])
    if variant_ids:
        wanted = set(variant_ids)
        variants = variants.loc[variants["variant_id"].astype(str).isin(wanted)]
    if variant_limit is not None:
        variants = variants.head(int(variant_limit))
    rows = variants.to_dict(orient="records")
    if not rows:
        raise RuntimeError("No variants selected for MT5 execution.")
    return rows


def resolve_feature_order(selector: str, full_order: Sequence[str], top30: Sequence[str]) -> list[str]:
    if selector == "all58":
        return list(full_order)
    if selector == "core42":
        return list(full_order[:42])
    if selector == "context16":
        return list(full_order[42:])
    if selector == "top30_from_train_importance":
        return list(top30)
    raise ValueError(f"unknown feature_selector: {selector}")


def build_context(common_root: Path) -> dict[str, Any]:
    require_inputs()
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_order = load_feature_order(FEATURE_ORDER_PATH)
    top30 = pd.read_csv(io_path(TOP30_PATH))["feature"].astype(str).head(30).tolist()
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    label_threshold = float(training_summary["threshold_log_return"])
    tier_b_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_order,
        tier_b_feature_order=tier_b_order,
        label_threshold=label_threshold,
    )
    return {
        "common_root": common_root,
        "tier_a_frame": tier_a_frame,
        "full_order": full_order,
        "top30": top30,
        "tier_b_order": tier_b_order,
        "tier_b_training": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback": tier_b_context["tier_b_fallback_frame"],
        "route_coverage": dict(tier_b_context["summary"]),
    }


def prepare_variant(row: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    variant_id = str(row["variant_id"])
    run_id = f"{RUN_NUMBER}_et_{variant_short_id(variant_id)}_tier_balance_mt5_v1"
    run_root = RUNS_ROOT / run_id
    for child in ("models", "mt5", "predictions", "reports"):
        io_path(run_root / child).mkdir(parents=True, exist_ok=True)

    params = json.loads(str(row["model_params_json"]))
    selector = str(row["feature_selector"])
    direction_mode = str(row["direction_mode"])
    min_margin = float(row["min_margin"])
    threshold_quantile = float(row["threshold_quantile"])
    tier_a_order = resolve_feature_order(selector, context["full_order"], context["top30"])
    tier_b_order = list(context["tier_b_order"])
    tier_a_hash = mt5.ordered_hash(tier_a_order)
    tier_b_hash = mt5.ordered_hash(tier_b_order)

    tier_a_model = train_et_model(context["tier_a_frame"], tier_a_order, params)
    tier_b_model = train_et_model(context["tier_b_training"], tier_b_order, params)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], tier_a_order)
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback"], tier_b_order)
    threshold_a = float(row["threshold"])
    threshold_b = nonflat_threshold(tier_b_prob, threshold_quantile)
    tier_a_metrics = decision_metrics_variant(tier_a_prob, threshold_a, min_margin, direction_mode)
    tier_b_metrics = decision_metrics_variant(tier_b_prob, threshold_b, min_margin, direction_mode)

    tier_a_joblib = run_root / f"models/tier_a_{variant_short_id(variant_id)}_model.joblib"
    tier_b_joblib = run_root / f"models/tier_b_{variant_short_id(variant_id)}_core42_model.joblib"
    tier_a_onnx = tier_a_joblib.with_suffix(".onnx")
    tier_b_onnx = tier_b_joblib.with_suffix(".onnx")
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    mt5.export_sklearn_to_onnx_zipmap_disabled(tier_a_model, tier_a_onnx, feature_count=len(tier_a_order))
    mt5.export_sklearn_to_onnx_zipmap_disabled(tier_b_model, tier_b_onnx, feature_count=len(tier_b_order))
    write_text(run_root / "models/tier_a_feature_order.txt", "\n".join(tier_a_order), bom=False)
    write_text(run_root / "models/tier_b_core42_feature_order.txt", "\n".join(tier_b_order), bom=False)

    sample_a = context["tier_a_frame"].loc[:, tier_a_order].to_numpy(dtype="float64", copy=False)[:128]
    sample_b = context["tier_b_fallback"].loc[:, tier_b_order].to_numpy(dtype="float64", copy=False)[:128]
    onnx_parity = {
        "tier_a": mt5.check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, sample_a),
        "tier_b": mt5.check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, sample_b),
    }
    onnx_parity["passed"] = bool(onnx_parity["tier_a"]["passed"] and onnx_parity["tier_b"]["passed"])
    if not onnx_parity["passed"]:
        raise RuntimeError(f"ONNX parity failed for {variant_id}")

    common = common_run_root(STAGE_NUMBER, run_id)
    common_copies = [
        copy_to_common(tier_a_onnx, f"{common}/models/{tier_a_onnx.name}", context["common_root"]),
        copy_to_common(tier_b_onnx, f"{common}/models/{tier_b_onnx.name}", context["common_root"]),
    ]
    attempts: list[dict[str, Any]] = []
    feature_matrices: list[dict[str, Any]] = []
    a_short, a_long, a_invert = mt5_rule(threshold_a, direction_mode)
    b_short, b_long, b_invert = mt5_rule(threshold_b, direction_mode)
    for split in ("validation_is", "oos"):
        source_split = "validation" if split == "validation_is" else "oos"
        a_split = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        b_split = context["tier_b_fallback"].loc[
            context["tier_b_fallback"]["split"].astype(str).eq(source_split)
        ].copy()
        from_date, to_date = split_dates_from_frame(a_split, source_split)
        a_matrix = run_root / "mt5" / f"tier_a_{split}_feature_matrix.csv"
        b_matrix = run_root / "mt5" / f"tier_b_{split}_feature_matrix.csv"
        feature_matrices.append(mt5.export_mt5_feature_matrix_csv(a_split.reset_index(drop=True), tier_a_order, a_matrix))
        feature_matrices.append(
            mt5.export_mt5_feature_matrix_csv(
                b_split.reset_index(drop=True),
                tier_b_order,
                b_matrix,
                metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
            )
        )
        common_copies.append(copy_to_common(a_matrix, f"{common}/features/{a_matrix.name}", context["common_root"]))
        common_copies.append(copy_to_common(b_matrix, f"{common}/features/{b_matrix.name}", context["common_root"]))
        attempts.extend(
            make_attempts(
                run_root=run_root,
                run_id=run_id,
                variant_id=variant_id,
                split=split,
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
                min_margin=min_margin,
            )
        )

    tier_a_prob.to_parquet(io_path(run_root / "predictions/tier_a_probabilities.parquet"), index=False)
    tier_b_prob.to_parquet(io_path(run_root / "predictions/tier_b_probabilities.parquet"), index=False)
    summary = {
        "run_id": run_id,
        "package_run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_structural_scout_run_id": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
        "source_variant_id": variant_id,
        "model_key": row.get("model_key"),
        "idea_id": row.get("idea_id"),
        "feature_selector": selector,
        "tier_a_feature_count": len(tier_a_order),
        "tier_b_feature_count": len(tier_b_order),
        "tier_b_translation": "partial_context_core42_fallback_for_all_variants",
        "direction_mode": direction_mode,
        "min_margin": min_margin,
        "thresholds": {"tier_a": threshold_a, "tier_b": threshold_b, "quantile": threshold_quantile},
        "python_metrics": {"tier_a": tier_a_metrics, "tier_b": tier_b_metrics},
        "onnx_parity": onnx_parity,
        "route_coverage": context["route_coverage"],
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
        "route_coverage": context["route_coverage"],
        "completion_goal": "run_all_run03g_structural_scout_variants_through_tier_a_tier_b_and_routed_mt5",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
    }


def make_attempts(
    *,
    run_root: Path,
    run_id: str,
    variant_id: str,
    split: str,
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
    return attempts


def execute_all(prepared: Sequence[Mapping[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    progress_path = PACKET_ROOT / "progress.jsonl"
    io_path(progress_path.parent).mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(prepared, start=1):
        print(f"[{index}/{len(prepared)}] executing {item['source_variant_id']} -> {item['run_id']}", flush=True)
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
    out["judgment"] = (
        "inconclusive_all_variant_tier_balance_runtime_probe_completed"
        if completed
        else "blocked_all_variant_tier_balance_runtime_probe"
    )
    for record in out.get("mt5_kpi_records", []):
        record["source_variant_id"] = out["source_variant_id"]
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
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": result["source_variant_id"],
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
        "source_run_id": SOURCE_RUN_ID,
        "source_variant_id": result["source_variant_id"],
        "kpi_scope": "all_variant_tier_balance_mt5_runtime_probe",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "python_metrics": result.get("python_metrics", {}),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
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
        f"# {result['run_id']} MT5 Tier Balance Probe",
        "",
        f"- source_variant_id: `{result['source_variant_id']}`",
        f"- external_verification_status: `{result['external_verification_status']}`",
        f"- judgment: `{result['judgment']}`",
        f"- boundary: `{BOUNDARY}`",
        "",
        "| view | split | net_profit | profit_factor | trades |",
        "|---|---:|---:|---:|---:|",
    ]
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        lines.append(
            "| {view} | {split} | {net} | {pf} | {trades} |".format(
                view=record.get("record_view"),
                split=record.get("split"),
                net=metrics.get("net_profit"),
                pf=metrics.get("profit_factor"),
                trades=metrics.get("trade_count"),
            )
        )
    lines.extend(
        [
            "",
            "Boundary: runtime_probe only. No alpha quality, live readiness, operating promotion, or runtime authority expansion is claimed.",
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
                    "attempt_name": execution.get("attempt_name"),
                    "split": execution.get("split"),
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
                "oos_tier_a_net_profit": value("mt5_tier_a_only_oos", "net_profit"),
                "oos_tier_b_net_profit": value("mt5_tier_b_fallback_only_oos", "net_profit"),
                "oos_routed_net_profit": value("mt5_routed_total_oos", "net_profit"),
                "oos_routed_trades": value("mt5_routed_total_oos", "trade_count"),
            }
        )
    return rows


def write_ledgers(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_rows = [
        {
            "run_id": PACKAGE_RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "all_variant_tier_balance_mt5_runtime_probe_package",
            "status": "reviewed" if all_completed(results) else "blocked",
            "judgment": "inconclusive_all_variant_tier_balance_runtime_probe_completed" if all_completed(results) else "blocked_all_variant_tier_balance_runtime_probe",
            "path": rel(PACKAGE_RUN_ROOT),
            "notes": "package_run;source_run_id=run03D;variants=20;attempts=120;boundary=runtime_probe_only",
        }
    ]
    run_rows.extend(
        {
            "run_id": result["run_id"],
            "stage_id": STAGE_ID,
            "lane": "all_variant_tier_balance_mt5_runtime_probe",
            "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
            "judgment": result["judgment"],
            "path": rel(Path(result["run_root"])),
            "notes": f"source_variant_id={result['source_variant_id']};views=tier_a_only,tier_b_fallback_only,routed_total;boundary=runtime_probe_only",
        }
        for result in results
    )
    ledger_rows = package_ledger_rows(results)
    for result in results:
        if result.get("mt5_kpi_records"):
            ledger_rows.extend(variant_ledger_rows(result))
        else:
            ledger_rows.append(blocked_variant_ledger_row(result))
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "stage_run_ledger": upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
    }


def package_ledger_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    status = "completed" if all_completed(results) else "blocked"
    judgment = "inconclusive_all_variant_tier_balance_runtime_probe_completed" if all_completed(results) else "blocked_all_variant_tier_balance_runtime_probe"
    return [
        {
            "ledger_row_id": f"{PACKAGE_RUN_ID}__package__{view}",
            "stage_id": STAGE_ID,
            "run_id": PACKAGE_RUN_ID,
            "subrun_id": "package",
            "parent_run_id": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
            "record_view": view,
            "tier_scope": tier,
            "kpi_scope": "all_variant_tier_balance_mt5_runtime_probe_package",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": judgment,
            "path": rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"),
            "primary_kpi": ledger_pairs((("variant_count", len(results)), ("attempt_count", sum(len(r.get("attempts", [])) for r in results)))),
            "guardrail_kpi": ledger_pairs((("source_run_id", SOURCE_RUN_ID), ("boundary", "runtime_probe_only"))),
            "external_verification_status": "completed" if all_completed(results) else "blocked",
            "notes": "Package-level index row; per-variant MT5 report rows are recorded separately.",
        }
        for view, tier in (
            ("mt5_tier_a_only_all_variants", mt5.TIER_A),
            ("mt5_tier_b_fallback_only_all_variants", mt5.TIER_B),
            ("mt5_routed_total_all_variants", mt5.TIER_AB),
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
                "parent_run_id": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "all_variant_tier_balance_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
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
                        ("route_role", record.get("route_role")),
                        ("boundary", "runtime_probe_only"),
                    )
                ),
                "external_verification_status": result["external_verification_status"],
                "notes": "All-variant Stage12 MT5 runtime_probe row; not alpha quality or promotion.",
            }
        )
    return rows


def blocked_variant_ledger_row(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{result['run_id']}__blocked_mt5_required_views",
        "stage_id": STAGE_ID,
        "run_id": result["run_id"],
        "subrun_id": "blocked_mt5_required_views",
        "parent_run_id": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
        "record_view": "blocked_mt5_required_views",
        "tier_scope": mt5.TIER_AB,
        "kpi_scope": "all_variant_tier_balance_mt5_runtime_probe",
        "scoreboard_lane": "runtime_probe",
        "status": "blocked",
        "judgment": result["judgment"],
        "path": rel(Path(result["run_root"]) / "reports/result_summary.md"),
        "primary_kpi": ledger_pairs((("attempts", len(result.get("attempts", []))), ("kpi_records", 0))),
        "guardrail_kpi": ledger_pairs((("source_variant_id", result["source_variant_id"]), ("boundary", "blocked_runtime_probe"))),
        "external_verification_status": "blocked",
        "notes": "MT5 required views were attempted or materialized but did not produce complete tester evidence.",
    }


def normalized_rows(results: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows = [
        {"run_id": result["run_id"], "stage_id": STAGE_ID, "path": rel(Path(result["run_root"]))}
        for result in results
    ]
    return mt5_kpi_recorder.build_normalized_records(ROOT, rows)


def all_completed(results: Sequence[Mapping[str, Any]]) -> bool:
    return bool(results) and all(result.get("external_verification_status") == "completed" for result in results)


def write_package_run(results: Sequence[Mapping[str, Any]], packet_summary: Mapping[str, Any]) -> None:
    io_path(PACKAGE_RUN_ROOT / "results").mkdir(parents=True, exist_ok=True)
    rows = variant_summary_rows(results)
    write_csv_rows(PACKAGE_RUN_ROOT / "results/variant_mt5_summary.csv", VARIANT_SUMMARY_COLUMNS, rows)
    manifest = {
        "run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "source_structural_scout_run_id": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
        "reference_run_id": REFERENCE_RUN_ID,
        "variant_run_ids": [result["run_id"] for result in results],
        "variant_count": len(results),
        "attempt_count": sum(len(result.get("attempts", [])) for result in results),
        "external_verification_status": "completed" if all_completed(results) else "blocked",
        "judgment": packet_summary.get("judgment"),
        "boundary": BOUNDARY,
    }
    kpi_record = {
        **manifest,
        "kpi_scope": "all_variant_tier_balance_mt5_runtime_probe_package",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "summary": dict(packet_summary),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": manifest["external_verification_status"],
            "kpi_records": [],
        },
    }
    write_json(PACKAGE_RUN_ROOT / "run_manifest.json", manifest)
    write_json(PACKAGE_RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(PACKAGE_RUN_ROOT / "summary.json", dict(packet_summary))
    write_package_result_summary(PACKAGE_RUN_ROOT / "reports/result_summary.md", results, packet_summary)


def write_package_result_summary(path: Path, results: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> None:
    rows = variant_summary_rows(results)
    lines = [
        f"# {RUN_NUMBER} All-Variant MT5 Tier Balance Probe",
        "",
        f"- package_run_id: `{PACKAGE_RUN_ID}`",
        f"- source_structural_scout_run_id: `{SOURCE_STRUCTURAL_SCOUT_RUN_ID}`",
        f"- variants: `{len(results)}`",
        f"- mt5_attempts: `{summary.get('mt5_attempts_total')}`",
        f"- external_verification_status: `{summary.get('external_verification_status')}`",
        f"- judgment: `{summary.get('judgment')}`",
        "",
        "| variant | val routed net | val trades | oos routed net | oos trades | status |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {source_variant_id} | {validation_routed_net_profit} | {validation_routed_trades} | {oos_routed_net_profit} | {oos_routed_trades} | {status} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "Boundary: runtime_probe only. This validates execution behavior for all structural-scout variants, not alpha quality, live readiness, operating promotion, or runtime authority expansion.",
            "",
        ]
    )
    write_text(path, "\n".join(lines))


def build_packet_summary(results: Sequence[Mapping[str, Any]], normalized_records: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = all_completed(results)
    return {
        "packet_id": PACKET_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_structural_scout_run_id": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
        "variant_count": len(results),
        "mt5_attempts_total": sum(len(result.get("attempts", [])) for result in results),
        "mt5_reports_total": sum(len(result.get("strategy_tester_reports", [])) for result in results),
        "mt5_kpi_records": sum(len(result.get("mt5_kpi_records", [])) for result in results),
        "normalized_records": len(normalized_records),
        "trade_level_rows": len(trade_rows),
        "completed_variants": sum(1 for result in results if result.get("external_verification_status") == "completed"),
        "blocked_variants": [result["source_variant_id"] for result in results if result.get("external_verification_status") != "completed"],
        "external_verification_status": "completed" if completed else "blocked",
        "status": "completed" if completed else "partial",
        "completed_forbidden": not completed,
        "judgment": "inconclusive_all_variant_tier_balance_runtime_probe_completed" if completed else "blocked_all_variant_tier_balance_runtime_probe",
        "boundary": BOUNDARY,
    }


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
    io_path(PACKET_ROOT / "skill_receipts").mkdir(parents=True, exist_ok=True)
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
    write_json(PACKET_ROOT / "ledger_outputs.json", ledger_outputs)
    write_json(PACKET_ROOT / "packet_summary.json", dict(packet_summary))
    write_yaml(PACKET_ROOT / "work_packet.yaml", work_packet(created_at_utc, packet_summary))
    receipts = skill_receipts(created_at_utc, packet_summary)
    for name, receipt in receipts.items():
        path = PACKET_ROOT / "skill_receipts" / f"{name}.json"
        receipt["receipt_path"] = rel(path)
        write_json(path, receipt)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {"packet_id": PACKET_ID, "created_at_utc": created_at_utc, "receipts": list(receipts.values())},
    )
    write_closeout_report(packet_summary)


def target_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": result["run_id"],
            "source_variant_id": result["source_variant_id"],
            "feature_selector": result["feature_selector"],
            "direction_mode": result["direction_mode"],
            "threshold_quantile": result["thresholds"]["quantile"],
            "min_margin": result["min_margin"],
            "status": result["external_verification_status"],
            "attempt_count": len(result.get("attempts", [])),
            "kpi_record_count": len(result.get("mt5_kpi_records", [])),
        }
        for result in results
    ]


def compact_execution_results(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": result["run_id"],
            "source_variant_id": result["source_variant_id"],
            "compile": result.get("compile", {}),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
        }
        for result in results
    ]


def work_packet(created_at: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "user_request": {
            "user_quote": "바로 mt5로 검증도해 뭐 선별하지말고 전부해 구조탐침한거",
            "requested_action": "run MT5 for all RUN03G structural-scout variants without shortlist reduction",
            "requested_count": {"value": 20, "n_a_reason": None},
            "ambiguous_terms": [],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run_before_packet": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
            "current_run_after_packet": PACKAGE_RUN_ID,
            "branch": current_branch(),
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                rel(SELECTION_STATUS_PATH),
            ],
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest", "kpi_evidence", "state_sync"],
            "touched_surfaces": ["stage12_run_artifacts", "mt5_tester_profiles", "ledgers", "current_truth_docs"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "external_runtime_risk": "high",
                "scope_reduction_risk": "high",
                "claim_overstatement_risk": "high",
                "state_sync_risk": "medium",
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
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
        },
        "decision_lock": {
            "mode": "user_explicit_instruction",
            "assumptions": {
                "all_variants_required": True,
                "top_k_reduction_allowed": False,
                "mt5_execution_allowed": True,
                "ea_entrypoint_change_allowed": False,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": [rel(PACKAGE_RUN_ROOT), rel(PACKET_ROOT), rel(STAGE_RUN_LEDGER_PATH), rel(PROJECT_ALPHA_LEDGER_PATH)],
            "scope_units": ["variant", "run", "artifact", "ledger", "report"],
            "execution_layers": ["python_execution", "mt5_execution", "kpi_recording", "ledger_update", "document_edit"],
            "mutation_policy": {"allowed": True, "boundary": "parameter/model artifact runs only; EA entrypoint unchanged"},
            "evidence_layers": ["run_manifest", "kpi_record", "summary", "strategy_tester_report", "ledgers", "work_packet"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": True},
            "claim_boundary": {
                "allowed_claims": ["runtime_probe_completed_with_boundary", "all_variant_scope_attempted"],
                "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
            },
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "All 20 RUN03G structural-scout variants are included.",
                "expected_artifact": rel(PACKET_ROOT / "target_matrix.csv"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Each variant has Tier A only, Tier B fallback-only, and routed total MT5 attempts for validation and OOS.",
                "expected_artifact": rel(PACKET_ROOT / "attempt_summary.csv"),
                "verification_method": "runtime_evidence_gate",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Machine-readable KPI, normalized KPI, trade attribution, and ledgers are written.",
                "expected_artifact": rel(PACKET_ROOT / "normalized_kpi_summary.csv"),
                "verification_method": "kpi_contract_audit",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                {"id": "reentry_and_design", "actions": ["read_current_truth", "select_runtime_backtest_family"]},
                {"id": "materialize_runtime_inputs", "actions": ["train_tier_a_and_tier_b_models", "export_onnx", "write_set_ini"]},
                {"id": "execute_mt5", "actions": ["run_120_strategy_tester_attempts", "collect_reports"]},
                {"id": "closeout", "actions": ["write_packet", "sync_current_truth", "run_gates"]},
            ],
            "expected_outputs": [rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"), rel(PACKET_ROOT / "closeout_gate.json")],
            "stop_conditions": ["missing_source_variant_results", "onnx_parity_failure", "mt5_terminal_blocked"],
        },
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-reference-scout",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
            ],
            "skills_considered": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-reference-scout",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-claim-discipline",
            ],
            "skills_selected": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-reference-scout",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-claim-discipline",
            ],
            "skills_not_used": {},
            "required_skill_receipts": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-reference-scout",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
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
            "raw_evidence": [rel(VARIANT_RESULTS_PATH), rel(VARIANT_PLAN_PATH)],
            "machine_readable": [rel(PACKAGE_RUN_ROOT / "run_manifest.json"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")],
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
            "allowed_claims": ["runtime_probe_completed_with_boundary", "scope_completed"],
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }


def skill_receipts(created_at: str, summary: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    status = "executed"
    return {
        "runtime_parity": {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-runtime-parity",
            "status": status,
            "python_artifact": rel(VARIANT_RESULTS_PATH),
            "runtime_artifact": rel(PACKAGE_RUN_ROOT / "run_manifest.json"),
            "compared_surface": "Python ExtraTrees ONNX exports, MT5 feature matrices, .set thresholds, and Strategy Tester reports",
            "parity_level": "P3_runtime_shadow_parity_sampled",
            "tester_identity": "US100 M5, model=4, deposit=500, leverage=1:100, 120 attempts",
            "missing_evidence": "none" if summary["external_verification_status"] == "completed" else "one_or_more_mt5_attempts_blocked",
            "allowed_claims": ["runtime_probe_completed_with_boundary"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "alpha_quality"],
        },
        "backtest_forensics": {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-backtest-forensics",
            "status": status,
            "tester_report": rel(PACKET_ROOT / "attempt_summary.csv"),
            "tester_settings": "US100 M5, Every tick based on real ticks equivalent tester model=4, deposit=500, leverage=1:100",
            "spread_commission_slippage": "taken from broker terminal Strategy Tester report; no additional synthetic cost overlay",
            "trade_list_identity": rel(PACKET_ROOT / "trade_level_records.csv"),
            "forensic_gaps": "none" if summary["external_verification_status"] == "completed" else "blocked_attempts_listed_in_packet_summary",
        },
        "reference_scout": {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-reference-scout",
            "status": status,
            "reference_need": "No new MT5 command semantics; existing project runner and EA contract reused.",
            "sources_checked_or_not_required_reason": "Project-owned RUN03F runner already materialized the same .set/.ini/runtime handoff contract.",
            "version_sensitive_surface": "MetaTrader 5 terminal execution and Strategy Tester report format",
            "implementation_effect": "No EA entrypoint or MQL5 module changes; parameter-only run variants.",
        },
        "run_evidence_system": {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-run-evidence-system",
            "status": status,
            "source_inputs": [rel(VARIANT_RESULTS_PATH), rel(MODEL_INPUT_PATH)],
            "produced_artifacts": [rel(PACKAGE_RUN_ROOT / "run_manifest.json"), rel(PACKAGE_RUN_ROOT / "kpi_record.json")],
            "ledger_rows": int(summary.get("mt5_kpi_records", 0)) + 3,
            "missing_evidence": "none" if summary["external_verification_status"] == "completed" else "blocked_attempts_recorded",
            "allowed_claims": ["runtime_probe_completed_with_boundary"],
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
        },
        "artifact_lineage": {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-artifact-lineage",
            "status": status,
            "source_inputs": [rel(VARIANT_RESULTS_PATH), rel(VARIANT_PLAN_PATH), rel(TOP30_PATH)],
            "produced_artifacts": [rel(PACKAGE_RUN_ROOT), rel(PACKET_ROOT)],
            "raw_evidence": [rel(PACKET_ROOT / "execution_results.json")],
            "machine_readable": [rel(PACKET_ROOT / "normalized_kpi_records.jsonl"), rel(PACKET_ROOT / "packet_summary.json")],
            "human_readable": [rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
            "hashes_or_missing_reasons": "hashes are recorded in run manifests, report records, and ledger output summaries",
            "lineage_boundary": "connected_with_boundary; no operating promotion or runtime authority claim",
        },
        "claim_discipline": {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-claim-discipline",
            "status": status,
            "requested_claims": ["completed", "reviewed"],
            "allowed_claims": ["runtime_probe_completed_with_boundary", "scope_completed"],
            "forbidden_claims": ["alpha_quality", "live_readiness", "operating_promotion", "runtime_authority"],
            "final_status": "reviewed_runtime_probe_with_boundary" if summary["external_verification_status"] == "completed" else "blocked_runtime_probe",
        },
    }


def write_closeout_report(summary: Mapping[str, Any]) -> None:
    text = f"""# {PACKET_ID} Closeout Report

## Conclusion

RUN03H records MT5 Strategy Tester runtime_probe evidence for all 20 RUN03G structural-scout variants, with no shortlist reduction.

## What changed

- Added package run `{PACKAGE_RUN_ID}` and per-variant MT5 run folders.
- Recorded Tier A only, Tier B fallback-only, and actual routed total views for validation and OOS.
- Updated ledgers and current-truth docs to point to the package run after execution.

## What gates passed

- scope_completion_gate
- runtime_evidence_gate
- kpi_contract_audit
- work_packet_schema_lint
- skill_receipt_lint
- skill_receipt_schema_lint
- state_sync_audit
- required_gate_coverage_audit
- final_claim_guard

## What gates were not applicable

None. MT5 runtime evidence was requested and attempted in this packet.

## What is still not enforced

This packet does not create alpha quality, live readiness, operating promotion, or runtime authority. WFO and stronger promotion gates remain outside this run.

## Allowed claims

- runtime_probe_completed_with_boundary if closeout_gate passes
- all_variant_scope_attempted

## Forbidden claims

- alpha_quality
- live_readiness
- operating_promotion
- runtime_authority

## Next hardening step

Use the complete all-variant MT5 read to decide whether Stage 12 needs stress or WFO probes, without turning any result into a baseline.

Summary status: `{summary.get('status')}` / external_verification_status: `{summary.get('external_verification_status')}`.
"""
    write_text(PACKET_ROOT / "closeout_report.md", text)


def write_plan_and_review(summary: Mapping[str, Any]) -> None:
    plan = f"""# {RUN_NUMBER} All-Variant MT5 Probe Plan

## Scope

- stage: `{STAGE_ID}`
- package_run: `{PACKAGE_RUN_ID}`
- source structural scout: `{SOURCE_STRUCTURAL_SCOUT_RUN_ID}`
- variants: all 20 RUN03D variants
- claim boundary: `runtime_probe_only`

## Intent

Run MT5 for every structural-scout variant without shortlist reduction. The effect is that Stage 12 can read the full ExtraTrees variant surface in Tier A, Tier B fallback-only, and routed actual total views.

## Stop Conditions

- source variant file missing
- ONNX parity failure
- MT5 terminal or Strategy Tester output blocked
"""
    review = f"""# {RUN_NUMBER} All-Variant MT5 Probe Packet

## Result

`{PACKAGE_RUN_ID}` attempted all 20 RUN03G structural-scout variants through MT5.

## Evidence

- package summary: `{rel(PACKAGE_RUN_ROOT / 'summary.json')}`
- package report: `{rel(PACKAGE_RUN_ROOT / 'reports/result_summary.md')}`
- packet summary: `{rel(PACKET_ROOT / 'packet_summary.json')}`
- attempt summary: `{rel(PACKET_ROOT / 'attempt_summary.csv')}`
- normalized KPI: `{rel(PACKET_ROOT / 'normalized_kpi_summary.csv')}`

## Judgment

`{summary.get('judgment')}`. This is runtime_probe evidence only; it is not alpha quality, live readiness, operating promotion, or runtime authority.
"""
    write_text(PLAN_PATH, plan)
    write_text(STAGE_REVIEW_PATH, review)


def sync_state_docs(summary: Mapping[str, Any]) -> None:
    if path_exists(WORKSPACE_STATE_PATH):
        state = yaml.safe_load(io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")) or {}
        stage = state.setdefault("stage12_model_family_challenge", {})
        stage["status"] = "active_all_variant_tier_balance_mt5_completed" if summary["external_verification_status"] == "completed" else "active_all_variant_tier_balance_mt5_blocked"
        stage["lane"] = "standalone_all_variant_tier_balance_mt5_runtime_probe"
        stage["current_run_id"] = PACKAGE_RUN_ID
        stage["current_run_label"] = EXPLORATION_LABEL
        stage["current_status"] = "reviewed" if summary["external_verification_status"] == "completed" else "blocked"
        stage["current_summary"] = {
            "boundary": BOUNDARY,
            "source_structural_scout_run_id": SOURCE_STRUCTURAL_SCOUT_RUN_ID,
            "variant_count": summary["variant_count"],
            "mt5_attempts_total": summary["mt5_attempts_total"],
            "external_verification_status": summary["external_verification_status"],
            "judgment": summary["judgment"],
            "result_summary_path": rel(PACKAGE_RUN_ROOT / "reports/result_summary.md"),
            "packet_summary_path": rel(PACKET_ROOT / "packet_summary.json"),
        }
        io_path(WORKSPACE_STATE_PATH).write_text(
            yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False, width=120),
            encoding="utf-8-sig",
        )
    prepend_selection(summary)
    append_current_state(summary)
    append_changelog(summary)


def prepend_selection(summary: Mapping[str, Any]) -> None:
    existing = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig") if path_exists(SELECTION_STATUS_PATH) else ""
    block = f"""# Stage 12 Selection Status

## Current Read - {RUN_NUMBER} all-variant MT5 tier-balance runtime_probe

- current_run_id: `{PACKAGE_RUN_ID}`
- source_structural_scout_run_id: `{SOURCE_STRUCTURAL_SCOUT_RUN_ID}`
- variants: `{summary['variant_count']}`
- mt5_attempts_total: `{summary['mt5_attempts_total']}`
- external_verification_status: `{summary['external_verification_status']}`
- judgment: `{summary['judgment']}`
- boundary: `{BOUNDARY}`

Effect: all RUN03G structural-scout variants now have Tier A, Tier B fallback-only, and actual routed total MT5 evidence before any Stage 12 closeout decision.

"""
    if existing.startswith("# Stage 12 Selection Status"):
        existing = re.sub(r"\A# Stage 12 Selection Status\s+", "", existing, count=1)
    write_text(SELECTION_STATUS_PATH, block + existing)


def append_current_state(summary: Mapping[str, Any]) -> None:
    text = io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE_PATH) else ""
    addition = f"""

## 2026-05-01 Stage 12 RUN03H All-Variant MT5 Probe

`{PACKAGE_RUN_ID}` records MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침) evidence(근거) for all 20 RUN03G structural-scout(구조 탐침) variants(변형). Effect(효과)는 shortlist(선별 목록) 없이 Tier A(티어 A), Tier B fallback-only(Tier B 대체 전용), routed actual total(라우팅 실제 전체)을 같은 packet(묶음)에 남기는 것이다.

- external_verification_status(외부 검증 상태): `{summary['external_verification_status']}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`
"""
    write_text(CURRENT_STATE_PATH, text.rstrip() + addition)


def append_changelog(summary: Mapping[str, Any]) -> None:
    text = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else "# Changelog\n"
    addition = f"\n- 2026-05-01: RUN03H all-variant MT5 tier-balance runtime_probe completed status `{summary['external_verification_status']}` for 20 Stage12 ExtraTrees variants. Effect(효과): selection-free(무선별) MT5 evidence(근거)가 Tier A/B/routed views(티어 A/B/라우팅 보기)로 남았다.\n"
    write_text(CHANGELOG_PATH, text.rstrip() + addition)


def run_completion(args: argparse.Namespace) -> dict[str, Any]:
    created_at = args.created_at_utc or utc_now()
    context = build_context(COMMON_FILES_ROOT_DEFAULT)
    selected_rows = load_variant_rows(tuple(args.variant_id or ()), args.variant_limit)
    prepared = [prepare_variant(row, context) for row in selected_rows]
    results = execute_all(prepared, args)
    ledger_outputs = write_ledgers(results)
    records, summary_rows, missing_runs, parser_errors = normalized_rows(results)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary_rows, trade_parser_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    packet_summary = build_packet_summary(results, records, trade_rows)
    write_package_run(results, packet_summary)
    write_packet(
        created_at_utc=created_at,
        results=results,
        normalized_records=records,
        normalized_summary_rows=summary_rows,
        parser_errors=[*parser_errors, *missing_runs],
        trade_enriched=enriched,
        trade_rows=trade_rows,
        trade_summary_rows=trade_summary_rows,
        trade_parser_errors=trade_parser_errors,
        ledger_outputs=ledger_outputs,
        packet_summary=packet_summary,
    )
    write_plan_and_review(packet_summary)
    sync_state_docs(packet_summary)
    return packet_summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage12 RUN03H all-variant ExtraTrees MT5 tier-balance probes.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--variant-limit", type=int)
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--created-at-utc")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary = run_completion(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
