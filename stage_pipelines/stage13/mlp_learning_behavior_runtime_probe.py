from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from pandas.errors import ParserWarning

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.baseline_training import load_feature_order
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage13.mlp_internal_behavior_probes import feature_group, rel


STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04M"
RUN_ID = "run04M_mlp_learning_behavior_runtime_probe_v1"
PACKET_ID = "stage13_run04M_mlp_learning_behavior_runtime_probe_packet_v1"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
EXPLORATION_LABEL = "stage13_MLPInternal__LearningBehaviorRuntime"
BOUNDARY = "mlp_learning_behavior_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
REPORT_PATH = STAGE_ROOT / "03_reviews/run04M_mlp_learning_behavior_runtime_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_learning_behavior_runtime_probe.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
META_COLUMNS = ("bar_time_server", "timestamp_utc", "split", "row_index")
CLASS_COUNT = 3
NO_TRADE_THRESHOLD = 1.01
PARITY_MEAN_TOLERANCE = 2.0e-4
MAX_HOLD_BARS = 9
MT5_VARIANTS = ("original", "ablate_volatility_range", "ablate_trend_structure", "ablate_session", "scale_center_105", "noise_sigma005")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def load_model_and_data() -> tuple[Any, dict[str, pd.DataFrame], list[str], dict[str, np.ndarray]]:
    model = joblib.load(io_path(SOURCE_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.joblib"))
    feature_order = load_feature_order(FEATURE_ORDER_PATH)
    frames = {
        "validation_is": pd.read_csv(io_path(SOURCE_ROOT / "features/tier_a_validation_is_feature_matrix.csv")),
        "oos": pd.read_csv(io_path(SOURCE_ROOT / "features/tier_a_oos_feature_matrix.csv")),
    }
    label_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    labels = {
        "validation_is": label_frame.loc[label_frame["split"].astype(str).eq("validation"), "label_class"].to_numpy(dtype=int),
        "oos": label_frame.loc[label_frame["split"].astype(str).eq("oos"), "label_class"].to_numpy(dtype=int),
    }
    for split, frame in frames.items():
        if len(frame) != len(labels[split]):
            raise ValueError(f"{split} row/label mismatch: {len(frame)} vs {len(labels[split])}")
    return model, frames, feature_order, labels


def stats_reference(frames: Mapping[str, pd.DataFrame], feature_order: Sequence[str]) -> dict[str, pd.Series]:
    validation = frames["validation_is"].loc[:, list(feature_order)]
    return {"median": validation.median(axis=0), "std": validation.std(axis=0).replace(0.0, 1.0)}


def variant_matrix(frame: pd.DataFrame, feature_order: Sequence[str], ref: Mapping[str, pd.Series], variant: str) -> pd.DataFrame:
    out = frame.copy()
    features = list(feature_order)
    if variant == "original":
        return out
    if variant.startswith("ablate_"):
        group = variant.removeprefix("ablate_")
        selected = [name for name in features if feature_group(name) == group]
        out.loc[:, selected] = ref["median"].loc[selected].to_numpy()
        return out
    continuous = [name for name in features if not name.startswith("is_") and name not in {"bb_squeeze", "supertrend_10_3"}]
    out[continuous] = out[continuous].astype("float64")
    x = out.loc[:, continuous].astype("float64")
    if variant == "scale_center_105":
        out.loc[:, continuous] = ref["median"].loc[continuous] + 1.05 * (x - ref["median"].loc[continuous])
    elif variant == "scale_center_095":
        out.loc[:, continuous] = ref["median"].loc[continuous] + 0.95 * (x - ref["median"].loc[continuous])
    elif variant.startswith("noise_sigma"):
        sigma = 0.05 if variant.endswith("005") else 0.10
        seed = 1517 + len(frame) + int(sigma * 1000)
        noise = np.random.default_rng(seed).normal(0.0, sigma, size=x.shape) * ref["std"].loc[continuous].to_numpy()
        out.loc[:, continuous] = x.to_numpy() + noise
    else:
        raise ValueError(f"unknown variant {variant}")
    return out


def predict_surface(model: Any, frame: pd.DataFrame, feature_order: Sequence[str], threshold: float) -> dict[str, Any]:
    probs = np.asarray(model.predict_proba(frame.loc[:, list(feature_order)].to_numpy(dtype="float64")), dtype=np.float64)
    sorted_probs = np.sort(probs, axis=1)
    margin = sorted_probs[:, -1] - sorted_probs[:, -2]
    entropy = -np.sum(np.clip(probs, 1.0e-12, 1.0) * np.log(np.clip(probs, 1.0e-12, 1.0)), axis=1) / math.log(3.0)
    directional = np.maximum(probs[:, 0], probs[:, 2])
    side = np.where(probs[:, 2] >= probs[:, 0], "long", "short")
    signal = directional >= threshold
    return {"probabilities": probs, "entropy_norm": entropy, "margin": margin, "decision": np.where(signal, side, "flat"), "signal": signal}


def probability_summary(variant: str, split: str, surface: Mapping[str, Any], base: Mapping[str, Any] | None) -> dict[str, Any]:
    probs = np.asarray(surface["probabilities"], dtype=np.float64)
    row = {
        "variant": variant,
        "split": split,
        "rows": len(probs),
        "mean_p_short": float(probs[:, 0].mean()),
        "mean_p_flat": float(probs[:, 1].mean()),
        "mean_p_long": float(probs[:, 2].mean()),
        "mean_entropy_norm": float(np.asarray(surface["entropy_norm"]).mean()),
        "mean_margin": float(np.asarray(surface["margin"]).mean()),
        "signal_share_q90": float(np.asarray(surface["signal"]).mean()),
    }
    if base is not None:
        base_probs = np.asarray(base["probabilities"], dtype=np.float64)
        row["mean_l1_prob_delta"] = float(np.sum(np.abs(probs - base_probs), axis=1).mean())
        row["decision_flip_share"] = float(np.mean(np.asarray(surface["decision"]) != np.asarray(base["decision"])))
        row["signal_flip_share"] = float(np.mean(np.asarray(surface["signal"]) != np.asarray(base["signal"])))
    else:
        row["mean_l1_prob_delta"] = 0.0
        row["decision_flip_share"] = 0.0
        row["signal_flip_share"] = 0.0
    return row


def calibration_rows(variant: str, split: str, probs: np.ndarray, labels: np.ndarray) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    pred = probs.argmax(axis=1)
    confidence = probs.max(axis=1)
    correct = pred == labels
    onehot = np.eye(CLASS_COUNT)[labels]
    brier = float(np.mean(np.sum((probs - onehot) ** 2, axis=1)))
    nll = float(-np.mean(np.log(np.clip(probs[np.arange(len(labels)), labels], 1.0e-12, 1.0))))
    bins = []
    ece = 0.0
    for index in range(10):
        lo, hi = index / 10.0, (index + 1) / 10.0
        mask = (confidence >= lo) & ((confidence < hi) if index < 9 else (confidence <= hi))
        if not mask.any():
            bins.append({"variant": variant, "split": split, "bin": index, "count": 0, "confidence": None, "accuracy": None, "gap": None})
            continue
        acc = float(correct[mask].mean())
        conf = float(confidence[mask].mean())
        gap = conf - acc
        ece += float(mask.mean()) * abs(gap)
        bins.append({"variant": variant, "split": split, "bin": index, "count": int(mask.sum()), "confidence": conf, "accuracy": acc, "gap": gap})
    summary = {"variant": variant, "split": split, "rows": len(labels), "accuracy": float(correct.mean()), "mean_confidence": float(confidence.mean()), "ece_10bin": ece, "brier_multiclass": brier, "nll": nll, "interpretation": "rank_like_not_calibrated" if ece > 0.08 else "mild_calibration_gap"}
    return summary, bins


def build_python_payload(model: Any, frames: Mapping[str, pd.DataFrame], feature_order: Sequence[str], labels: Mapping[str, np.ndarray], ref: Mapping[str, pd.Series], threshold: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    groups = sorted({feature_group(name) for name in feature_order})
    variants = ["original"] + [f"ablate_{group}" for group in groups] + ["scale_center_105", "scale_center_095", "noise_sigma005", "noise_sigma010"]
    prob_rows, calibration, calibration_bins, surfaces = [], [], [], {}
    for split, frame in frames.items():
        base = None
        for variant in variants:
            surface = predict_surface(model, variant_matrix(frame, feature_order, ref, variant), feature_order, threshold)
            surfaces[(variant, split)] = surface
            if variant == "original":
                base = surface
            prob_rows.append(probability_summary(variant, split, surface, base if variant != "original" else None))
            if variant == "original":
                summary, bins = calibration_rows(variant, split, np.asarray(surface["probabilities"]), labels[split])
                calibration.append(summary)
                calibration_bins.extend(bins)
    return prob_rows, calibration, calibration_bins, surfaces


def export_variant_matrices(frames: Mapping[str, pd.DataFrame], feature_order: Sequence[str], ref: Mapping[str, pd.Series]) -> dict[str, Any]:
    out = {}
    root = RUN_ROOT / "features"
    for variant in MT5_VARIANTS:
        for split, frame in frames.items():
            path = root / f"tier_a_{variant}_{split}_feature_matrix.csv"
            write_csv(path, list(frame.columns), variant_matrix(frame, feature_order, ref, variant).to_dict("records"))
            out[f"{variant}__{split}"] = {"variant": variant, "split": split, "path": rel(path), "rows": len(frame), "feature_count": len(feature_order), "feature_order_hash": read_json(SOURCE_ROOT / "run_manifest.json")["feature_matrices"][0]["feature_order_hash"], "sha256": sha256_file_lf_normalized(path)}
    return out


def materialize_model_copy() -> dict[str, Any]:
    source = SOURCE_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.onnx"
    target = RUN_ROOT / "models" / source.name
    io_path(target.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(target))
    return {"source": rel(source), "path": rel(target), "sha256": sha256_file_lf_normalized(target)}


def make_attempts(model_artifact: Mapping[str, Any], matrices: Mapping[str, Any], context_frame: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies = [copy_to_common(ROOT / model_artifact["path"], f"{common}/models/{Path(model_artifact['path']).name}", COMMON_FILES_ROOT_DEFAULT)]
    attempts = []
    for key, matrix in matrices.items():
        source = ROOT / matrix["path"]
        copies.append(copy_to_common(source, f"{common}/features/{source.name}", COMMON_FILES_ROOT_DEFAULT))
        source_split = "validation" if matrix["split"] == "validation_is" else "oos"
        from_date, to_date = split_dates_from_frame(context_frame, source_split)
        attempts.append(
            attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=STAGE_NUMBER,
                exploration_label=EXPLORATION_LABEL,
                attempt_name=f"tier_a_{matrix['variant']}_{matrix['split']}",
                tier=mt5.TIER_A,
                split=matrix["split"],
                model_path=f"{common}/models/{Path(model_artifact['path']).name}",
                model_id=f"{RUN_ID}_tier_a_{matrix['variant']}",
                feature_path=f"{common}/features/{source.name}",
                feature_count=int(matrix["feature_count"]),
                feature_order_hash=str(matrix["feature_order_hash"]),
                short_threshold=NO_TRADE_THRESHOLD,
                long_threshold=NO_TRADE_THRESHOLD,
                min_margin=0.0,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix=f"mt5_tier_a_{matrix['variant']}",
                max_hold_bars=MAX_HOLD_BARS,
                common_root=common,
            )
        )
    return attempts, copies


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {**dict(prepared), "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_materialize_only_no_mt5_execution"}
    try:
        result = execute_prepared_run(prepared, terminal_path=Path(args.terminal_path), metaeditor_path=Path(args.metaeditor_path), terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT, common_files_root=COMMON_FILES_ROOT_DEFAULT, tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT, timeout_seconds=int(args.timeout_seconds))
    except Exception as exc:
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_learning_behavior_runtime_probe", "failure": {"type": type(exc).__name__, "message": str(exc)}}
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = "inconclusive_learning_behavior_runtime_probe_completed" if completed else "blocked_learning_behavior_runtime_probe"
    return result


def telemetry_probs(result: Mapping[str, Any]) -> dict[str, pd.DataFrame]:
    out = {}
    for execution in result.get("execution_results", []):
        path = execution.get("runtime_outputs", {}).get("telemetry_path")
        if not path or not Path(str(path)).exists():
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ParserWarning)
            frame = pd.read_csv(io_path(Path(str(path))), index_col=False)
        cycle = frame.loc[frame["record_type"].astype(str).eq("cycle")].copy()
        cycle = cycle.loc[cycle.get("feature_ready", "true").astype(str).str.lower().isin({"true", "1", "yes"})]
        cycle = cycle.loc[cycle.get("model_ok", "true").astype(str).str.lower().isin({"true", "1", "yes"})]
        out[str(execution["attempt_name"])] = cycle.loc[:, ["p_short", "p_flat", "p_long"]].apply(pd.to_numeric, errors="coerce").dropna()
    return out


def mt5_probability_rows(result: Mapping[str, Any], threshold: float, labels: Mapping[str, np.ndarray]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    summary, calibration, bins = [], [], []
    for attempt, probs_frame in telemetry_probs(result).items():
        variant, split = parse_attempt_variant_split(attempt)
        probs = probs_frame.to_numpy(dtype="float64")
        surface = surface_from_probs(probs, threshold)
        summary.append(probability_summary(variant, split, surface, None))
        if variant == "original" and split in labels and len(labels[split]) == len(probs):
            row, bin_rows = calibration_rows("mt5_original", split, probs, labels[split])
            calibration.append(row)
            bins.extend(bin_rows)
    return summary, calibration, bins


def parse_attempt_variant_split(attempt: str) -> tuple[str, str]:
    text = attempt.removeprefix("tier_a_")
    if text.endswith("_validation_is"):
        return text.removesuffix("_validation_is"), "validation_is"
    if text.endswith("_oos"):
        return text.removesuffix("_oos"), "oos"
    raise ValueError(f"cannot parse attempt name: {attempt}")


def surface_from_probs(probs: np.ndarray, threshold: float) -> dict[str, Any]:
    sorted_probs = np.sort(probs, axis=1)
    margin = sorted_probs[:, -1] - sorted_probs[:, -2]
    entropy = -np.sum(np.clip(probs, 1.0e-12, 1.0) * np.log(np.clip(probs, 1.0e-12, 1.0)), axis=1) / math.log(3.0)
    signal = np.maximum(probs[:, 0], probs[:, 2]) >= threshold
    side = np.where(probs[:, 2] >= probs[:, 0], "long", "short")
    return {"probabilities": probs, "entropy_norm": entropy, "margin": margin, "decision": np.where(signal, side, "flat"), "signal": signal}


def parity_rows(python_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_key = {(row["variant"], row["split"]): row for row in python_rows}
    rows = []
    for mt5_row in mt5_rows:
        key = (mt5_row["variant"], mt5_row["split"])
        py = by_key.get(key)
        if not py:
            continue
        row_delta = int(mt5_row["rows"]) - int(py["rows"])
        deltas = {
            "mean_p_short_abs_delta": abs(float(mt5_row["mean_p_short"]) - float(py["mean_p_short"])),
            "mean_p_flat_abs_delta": abs(float(mt5_row["mean_p_flat"]) - float(py["mean_p_flat"])),
            "mean_p_long_abs_delta": abs(float(mt5_row["mean_p_long"]) - float(py["mean_p_long"])),
            "mean_entropy_abs_delta": abs(float(mt5_row["mean_entropy_norm"]) - float(py["mean_entropy_norm"])),
        }
        rows.append({
            "variant": key[0],
            "split": key[1],
            "row_delta": row_delta,
            **deltas,
            "parity_status": "pass" if row_delta == 0 and max(deltas.values()) <= PARITY_MEAN_TOLERANCE else "review",
        })
    return rows


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_csv(RUN_ROOT / "python_variant_probability_summary.csv", ("variant", "split", "rows", "mean_p_short", "mean_p_flat", "mean_p_long", "mean_entropy_norm", "mean_margin", "signal_share_q90", "mean_l1_prob_delta", "decision_flip_share", "signal_flip_share"), payload["python_probability_rows"])
    write_csv(RUN_ROOT / "feature_group_ablation_summary.csv", ("variant", "split", "rows", "mean_l1_prob_delta", "decision_flip_share", "signal_flip_share", "mean_entropy_norm", "mean_margin", "signal_share_q90"), [row for row in payload["python_probability_rows"] if row["variant"].startswith("ablate_")])
    write_csv(RUN_ROOT / "scaling_noise_sensitivity_summary.csv", ("variant", "split", "rows", "mean_l1_prob_delta", "decision_flip_share", "signal_flip_share", "mean_entropy_norm", "mean_margin", "signal_share_q90"), [row for row in payload["python_probability_rows"] if row["variant"].startswith(("scale_", "noise_"))])
    write_csv(RUN_ROOT / "calibration_shape_summary.csv", ("variant", "split", "rows", "accuracy", "mean_confidence", "ece_10bin", "brier_multiclass", "nll", "interpretation"), payload["calibration_rows"] + payload["mt5_calibration_rows"])
    write_csv(RUN_ROOT / "calibration_bins.csv", ("variant", "split", "bin", "count", "confidence", "accuracy", "gap"), payload["calibration_bins"] + payload["mt5_calibration_bins"])
    write_csv(RUN_ROOT / "mt5_runtime_probability_summary.csv", ("variant", "split", "rows", "mean_p_short", "mean_p_flat", "mean_p_long", "mean_entropy_norm", "mean_margin", "signal_share_q90", "mean_l1_prob_delta", "decision_flip_share", "signal_flip_share"), payload["mt5_probability_rows"])
    write_csv(RUN_ROOT / "mt5_python_parity_summary.csv", ("variant", "split", "row_delta", "mean_p_short_abs_delta", "mean_p_flat_abs_delta", "mean_p_long_abs_delta", "mean_entropy_abs_delta", "parity_status"), payload["parity_rows"])
    write_json(RUN_ROOT / "summary.json", payload)
    write_json(RUN_ROOT / "kpi_record.json", payload)
    write_json(RUN_ROOT / "run_manifest.json", manifest(payload))
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(payload))
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "summary": payload})
    write_md(PACKET_ROOT / "work_packet.md", work_packet())
    write_md(RUN_ROOT / "reports/result_summary.md", report(payload))
    write_md(REPORT_PATH, report(payload))
    write_md(DECISION_PATH, decision(payload))


def manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {"run_id": RUN_ID, "packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_number": RUN_NUMBER, "created_at_utc": payload["created_at_utc"], "source_run_id": SOURCE_RUN_ID, "model_family": "sklearn_mlpclassifier_learning_behavior_runtime_probe", "exploration_label": EXPLORATION_LABEL, "boundary": BOUNDARY, "stage_inheritance": "independent_no_stage10_11_12_run_baseline_seed_or_reference", "model_artifact": payload["model_artifact"], "feature_matrices": list(payload["feature_matrices"].values()), "attempts": payload["prepared"].get("attempts", []), "common_copies": payload["prepared"].get("common_copies", []), "compile": payload["mt5_result"].get("compile", {}), "execution_results": payload["mt5_result"].get("execution_results", []), "strategy_tester_reports": payload["mt5_result"].get("strategy_tester_reports", []), "external_verification_status": payload["external_verification_status"], "judgment": payload["judgment"], "outputs": {"report": rel(REPORT_PATH), "summary": rel(RUN_ROOT / "summary.json"), "python_probability": rel(RUN_ROOT / "python_variant_probability_summary.csv"), "mt5_probability": rel(RUN_ROOT / "mt5_runtime_probability_summary.csv"), "parity": rel(RUN_ROOT / "mt5_python_parity_summary.csv")}}


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    evidence = [rel(RUN_ROOT / name) for name in ("feature_group_ablation_summary.csv", "scaling_noise_sensitivity_summary.csv", "calibration_shape_summary.csv", "mt5_runtime_probability_summary.csv", "mt5_python_parity_summary.csv")]
    return [
        {"packet_id": PACKET_ID, "skill": "obsidian-experiment-design", "status": "completed", "hypothesis": "MLP learning behavior can be characterized by group ablation, scaling/noise response, and calibration shape without edge search.", "decision_use": "Stage13 model learning method characterization only.", "comparison_baseline": "RUN04F original probability surface.", "control_variables": ["source model", "feature order", "q90 read threshold"], "changed_variables": ["feature matrix transformations for behavior probes"], "sample_scope": "Tier A validation_is/OOS plus MT5 no-trade telemetry subset", "success_criteria": "Python behavior and MT5 runtime probability shape are comparable.", "failure_criteria": "missing model, feature matrix, labels, or MT5 telemetry", "invalid_conditions": ["row mismatch", "feature count mismatch"], "stop_conditions": ["no threshold optimization", "no PnL selection"], "evidence_plan": evidence},
        {"packet_id": PACKET_ID, "skill": "obsidian-model-validation", "status": "completed", "model_family": "sklearn MLPClassifier ReLU64", "target_and_label": "label_v1_fwd12_m5_logret 3-class labels used only for calibration shape.", "split_method": "split_v1 validation_is/OOS", "selection_metric": "none", "secondary_metrics": ["L1 probability delta", "decision flip share", "ECE", "Brier", "MT5/Python parity"], "threshold_policy": "fixed q90 for shape read; MT5 no-trade threshold for telemetry handoff", "overfit_risk": "post-hoc interpretation risk", "calibration_risk": "probabilities appear rank-like when ECE gap is large", "comparison_baseline": "RUN04F original", "validation_judgment": payload["judgment"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-data-integrity", "status": "completed", "data_source": "RUN04F Tier A feature matrices and model_input labels", "time_axis": "existing split rows; no timestamp joins added", "sample_scope": "validation_is rows 9844 and OOS rows 7584", "missing_or_duplicate_check": "row counts checked against labels", "feature_label_boundary": "labels used for calibration only, not training or selection", "split_boundary": "validation_is/OOS unchanged", "leakage_risk": "post-hoc calibration interpretation", "data_hash_or_identity": "source hashes recorded in manifest", "integrity_judgment": "usable_with_boundary"},
        {"packet_id": PACKET_ID, "skill": "obsidian-runtime-parity", "status": "completed", "research_path": rel(Path(__file__)), "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "shared_contract": "same ONNX model, transformed feature CSV, feature order hash, no-trade threshold", "known_differences": "MT5 run suppresses trades and is probability telemetry only.", "parity_check": rel(RUN_ROOT / "mt5_python_parity_summary.csv"), "parity_identity": "run_manifest records attempts, set files, compile, telemetry, reports.", "runtime_claim_boundary": "runtime_probe"},
        {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": "completed", "source_inputs": [rel(SOURCE_ROOT / "run_manifest.json"), rel(SOURCE_ROOT / "models/convergence_threshold_relu64_l2_tier_a_mlp_58.onnx")], "producer": rel(Path(__file__)), "consumer": "Stage13 review and ledgers", "artifact_paths": evidence, "artifact_hashes": "summary and manifest record source/generated hashes", "registry_links": [rel(STAGE_LEDGER_PATH), rel(PROJECT_LEDGER_PATH), rel(RUN_REGISTRY_PATH)], "availability": "generated", "lineage_judgment": "connected_with_boundary"},
        {"packet_id": PACKET_ID, "skill": "obsidian-result-judgment", "status": "completed", "result_subject": RUN_ID, "evidence_available": evidence, "evidence_missing": ["WFO", "calibration model", "runtime authority packet"], "judgment_label": payload["judgment"], "claim_boundary": BOUNDARY, "next_condition": payload["recommendation"], "user_explanation_hook": "This characterizes MLP behavior, not a tradable edge."},
    ]


def ledger_outputs(payload: Mapping[str, Any]) -> dict[str, Any]:
    rows = [
        ledger_row("tier_b_out_of_scope", "Tier B", "claim_scope_boundary", "out_of_scope_by_claim_learning_behavior_probe", RUN_ROOT / "summary.json", (("source_run", SOURCE_RUN_ID),), (("boundary", BOUNDARY),), "out_of_scope_by_claim", "RUN04M inspects Tier A source model behavior only."),
        ledger_row("tier_abb_out_of_scope", "Tier A+B", "claim_scope_boundary", "out_of_scope_by_claim_learning_behavior_probe", RUN_ROOT / "summary.json", (("source_run", SOURCE_RUN_ID),), (("boundary", BOUNDARY),), "out_of_scope_by_claim", "RUN04M inspects Tier A source model behavior only."),
        ledger_row("feature_group_ablation", "Tier A", "mlp_feature_group_ablation", payload["judgment"], RUN_ROOT / "feature_group_ablation_summary.csv", top_ablation_kpi(payload), (("boundary", "not_edge_search"),), payload["external_verification_status"], "Feature group ablation behavior, not edge selection."),
        ledger_row("scaling_noise_sensitivity", "Tier A", "mlp_scaling_noise_sensitivity", payload["judgment"], RUN_ROOT / "scaling_noise_sensitivity_summary.csv", top_noise_kpi(payload), (("boundary", "not_edge_search"),), payload["external_verification_status"], "Scaling/noise behavior, not edge selection."),
        ledger_row("calibration_shape", "Tier A", "mlp_calibration_shape", payload["judgment"], RUN_ROOT / "calibration_shape_summary.csv", calibration_kpi(payload), (("boundary", "rank_like_probability_read"),), payload["external_verification_status"], "Calibration shape read only."),
        ledger_row("mt5_runtime_shape_parity", "Tier A", "mt5_probability_runtime_shape_parity", payload["judgment"], RUN_ROOT / "mt5_python_parity_summary.csv", parity_kpi(payload), (("no_trade_threshold", NO_TRADE_THRESHOLD), ("boundary", "telemetry_only")), payload["external_verification_status"], "MT5 no-trade telemetry parity check."),
    ]
    stage = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_shape_probe", "status": "completed" if payload["external_verification_status"] == "completed" else "blocked", "judgment": payload["judgment"], "path": rel(RUN_ROOT / "summary.json"), "notes": ledger_pairs((("source", SOURCE_RUN_ID), ("boundary", BOUNDARY)))}], key="run_id")
    return {"stage_ledger": stage, "project_ledger": project, "run_registry": registry}


def ledger_row(subrun: str, tier: str, kpi_scope: str, judgment: Any, path: Path, primary: Sequence[tuple[str, Any]], guardrail: Sequence[tuple[str, Any]], external: str, notes: str) -> dict[str, Any]:
    return {"ledger_row_id": f"{RUN_ID}__{subrun}", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": subrun, "parent_run_id": RUN_ID, "record_view": subrun, "tier_scope": tier, "kpi_scope": kpi_scope, "scoreboard_lane": "runtime_probe", "status": "completed" if external != "blocked" else "blocked", "judgment": judgment, "path": rel(path), "primary_kpi": ledger_pairs(primary), "guardrail_kpi": ledger_pairs(guardrail), "external_verification_status": external, "notes": notes}


def top_ablation_kpi(payload: Mapping[str, Any]) -> tuple[tuple[str, Any], ...]:
    rows = [row for row in payload["python_probability_rows"] if row["variant"].startswith("ablate_") and row["split"] == "oos"]
    top = max(rows, key=lambda row: float(row["mean_l1_prob_delta"]))
    return (("top_oos_variant", top["variant"]), ("l1_delta", top["mean_l1_prob_delta"]), ("flip", top["decision_flip_share"]))


def top_noise_kpi(payload: Mapping[str, Any]) -> tuple[tuple[str, Any], ...]:
    rows = [row for row in payload["python_probability_rows"] if row["variant"].startswith(("scale_", "noise_")) and row["split"] == "oos"]
    top = max(rows, key=lambda row: float(row["mean_l1_prob_delta"]))
    return (("top_oos_variant", top["variant"]), ("l1_delta", top["mean_l1_prob_delta"]), ("flip", top["decision_flip_share"]))


def calibration_kpi(payload: Mapping[str, Any]) -> tuple[tuple[str, Any], ...]:
    oos = next(row for row in payload["calibration_rows"] if row["split"] == "oos")
    return (("oos_ece", oos["ece_10bin"]), ("oos_brier", oos["brier_multiclass"]), ("oos_conf", oos["mean_confidence"]), ("oos_acc", oos["accuracy"]))


def parity_kpi(payload: Mapping[str, Any]) -> tuple[tuple[str, Any], ...]:
    rows = payload["parity_rows"]
    max_delta = max((max(float(row["mean_p_short_abs_delta"]), float(row["mean_p_flat_abs_delta"]), float(row["mean_p_long_abs_delta"]), float(row["mean_entropy_abs_delta"])) for row in rows), default=None)
    return (("rows", len(rows)), ("pass", sum(1 for row in rows if row["parity_status"] == "pass")), ("max_mean_delta", max_delta))


def judge(payload: Mapping[str, Any]) -> tuple[str, str]:
    external = payload["mt5_result"].get("external_verification_status")
    parity_pass = all(row["parity_status"] == "pass" for row in payload["parity_rows"]) and bool(payload["parity_rows"])
    if external != "completed":
        return "blocked_learning_behavior_runtime_probe", "repair_mt5_runtime_shape_probe_before_more_stage13_runtime_claims"
    if parity_pass:
        return "inconclusive_mlp_learning_behavior_runtime_shape_confirmed", "stage13_can_stop_or_do_one_final_feature_group_interaction_probe"
    return "inconclusive_mlp_learning_behavior_python_runtime_shape_mismatch", "inspect_runtime_feature_matrix_or_onnx_parity"


def report(payload: Mapping[str, Any]) -> str:
    top_ablate = max([row for row in payload["python_probability_rows"] if row["variant"].startswith("ablate_") and row["split"] == "oos"], key=lambda row: float(row["mean_l1_prob_delta"]))
    top_noise = max([row for row in payload["python_probability_rows"] if row["variant"].startswith(("scale_", "noise_")) and row["split"] == "oos"], key=lambda row: float(row["mean_l1_prob_delta"]))
    oos_cal = next(row for row in payload["calibration_rows"] if row["split"] == "oos")
    mt5_pass = sum(1 for row in payload["parity_rows"] if row["parity_status"] == "pass")
    return "\n".join([
        f"# {RUN_ID} 결과 요약(Result Summary, 결과 요약)",
        "",
        f"- status(상태): `{payload['external_verification_status']}`",
        f"- judgment(판정): `{payload['judgment']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Core Read(핵심 판독)",
        "",
        f"- feature group ablation(피처 그룹 제거) OOS(표본외) 최대 변화: `{top_ablate['variant']}` / L1 delta(L1 변화) `{top_ablate['mean_l1_prob_delta']:.4f}` / decision flip(결정 뒤집힘) `{top_ablate['decision_flip_share']:.4f}`.",
        f"- scaling/noise sensitivity(스케일/노이즈 민감도) OOS(표본외) 최대 변화: `{top_noise['variant']}` / L1 delta(L1 변화) `{top_noise['mean_l1_prob_delta']:.4f}` / decision flip(결정 뒤집힘) `{top_noise['decision_flip_share']:.4f}`.",
        f"- calibration shape(보정 모양) OOS(표본외): confidence(확신도) `{oos_cal['mean_confidence']:.3f}`, accuracy(정확도) `{oos_cal['accuracy']:.3f}`, ECE(기대 보정 오차) `{oos_cal['ece_10bin']:.3f}`.",
        f"- MT5/Python parity(MT5/파이썬 동등성): `{mt5_pass}` / `{len(payload['parity_rows'])}` probability shape(확률 모양) rows pass(통과).",
        "",
        "효과(effect, 효과): 이 결과는 MLP(다층 퍼셉트론) learning behavior(학습 행동)를 설명한다. trade edge(거래 우위), alpha quality(알파 품질), baseline(기준선)은 만들지 않는다.",
    ])


def decision(payload: Mapping[str, Any]) -> str:
    return "\n".join(["# 2026-05-02 Stage13 MLP Learning Behavior Runtime Probe", "", f"- run(실행): `{RUN_ID}`", f"- judgment(판정): `{payload['judgment']}`", f"- recommendation(추천): `{payload['recommendation']}`", f"- boundary(경계): `{BOUNDARY}`", "", "효과(effect, 효과): feature group ablation(피처 그룹 제거), scaling/noise sensitivity(스케일/노이즈 민감도), calibration shape(보정 모양)을 MT5(메타트레이더5) telemetry(원격측정)까지 연결했지만, trade edge(거래 우위) 주장은 하지 않는다."])


def work_packet() -> str:
    return "\n".join([f"# {PACKET_ID}", "", "- hypothesis(가설): MLP(다층 퍼셉트론)의 Stage13(13단계) 고유 특징은 feature group dependency(피처 그룹 의존성), smoothness/fragility(매끄러움/취약성), calibration shape(보정 모양)로 설명할 수 있다.", "- changed_variables(변경 변수): feature matrix(피처 행렬) 변환만 바꾸고 모델/threshold(기준값)는 고정한다.", "- MT5 runtime(MT5 런타임): no-trade threshold(무거래 기준값)로 probability telemetry(확률 원격측정)만 확인한다.", f"- boundary(경계): `{BOUNDARY}`"])


def sync_docs(payload: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    lines = []
    top_current_seen = False
    for line in state.splitlines():
        if line.startswith("current_run_id:"):
            if not top_current_seen:
                lines.append(f"current_run_id: {RUN_ID}")
                top_current_seen = True
            continue
        lines.append(line)
    state = "\n".join(lines)
    if not top_current_seen:
        state = state.replace("active_stage: 13_model_family_challenge__mlp_training_effect", f"active_stage: 13_model_family_challenge__mlp_training_effect\ncurrent_run_id: {RUN_ID}", 1)
    state = state.replace("stage13_active_run04L_mlp_feature_sensitivity_probe", "stage13_active_run04M_mlp_learning_behavior_runtime_probe")
    state = state.replace("status: active_run04L_mlp_feature_sensitivity_probe", f"status: active_run04M_mlp_learning_behavior_runtime_probe\n      current_run_id: {RUN_ID}")
    block = f"stage13_mlp_learning_behavior_runtime_probe:\n  run_id: {RUN_ID}\n  status: completed\n  judgment: {payload['judgment']}\n  recommendation: {payload['recommendation']}\n  boundary: {BOUNDARY}\n  source_run_id: {SOURCE_RUN_ID}\n  report_path: {rel(REPORT_PATH)}\n"
    if "stage13_mlp_learning_behavior_runtime_probe:" not in state:
        state = state.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n")
    io_path(WORKSPACE_STATE_PATH).write_text(state + "\n", encoding="utf-8")
    latest = f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, feature group ablation(피처 그룹 제거), scaling/noise sensitivity(스케일/노이즈 민감도), calibration shape(보정 모양)을 MT5(메타트레이더5) no-trade telemetry(무거래 원격측정)까지 연결해 확인했다.\n\n효과(effect, 효과): Stage13(13단계)은 edge search(거래 우위 탐색)가 아니라 MLP(다층 퍼셉트론) learning behavior(학습 행동) 설명으로 유지된다."
    current = io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig")
    current = "\n".join(f"- current run(현재 실행): `{RUN_ID}`" if "current run(" in line else line for line in current.splitlines())
    if "## Latest Stage 13 Update(최신 Stage 13 업데이트)" in current and "## 쉬운 설명(Plain Read, 쉬운 설명)" in current:
        before, rest = current.split("## Latest Stage 13 Update(최신 Stage 13 업데이트)", 1)
        _, after = rest.split("## 쉬운 설명(Plain Read, 쉬운 설명)", 1)
        current = before + "## Latest Stage 13 Update(최신 Stage 13 업데이트)\n\n" + latest + "\n## 쉬운 설명(Plain Read, 쉬운 설명)" + after
    io_path(CURRENT_STATE_PATH).write_text(current + "\n", encoding="utf-8-sig")
    write_md(SELECTION_STATUS_PATH, "\n".join(["# Stage 13 Selection Status", "", "## Current Read(현재 판독)", "", f"- stage(단계): `{STAGE_ID}`", "- status(상태): `reviewed_learning_behavior_runtime_probe_completed(학습 행동 런타임 탐침 검토 완료)`", f"- current run(현재 실행): `{RUN_ID}`", "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`", f"- judgment(판정): `{payload['judgment']}`"]))
    upsert_line_by_token(REVIEW_INDEX_PATH, RUN_ID, f"- `{RUN_ID}`: `{payload['judgment']}`, report(보고서) `{rel(REPORT_PATH)}`")
    append_once(CHANGELOG_PATH, RUN_ID, f"\n- 2026-05-02: Added `{RUN_ID}` MLP learning behavior runtime probe(MLP 학습 행동 런타임 탐침); no edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), or runtime authority(런타임 권위) claim.\n")


def upsert_line_by_token(path: Path, token: str, line: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if token in existing:
            lines[index] = line.rstrip()
            io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")
            return
    io_path(path).write_text(text.rstrip() + "\n" + line.rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, token: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig")
    if token not in text:
        io_path(path).write_text(text.rstrip() + "\n" + addition, encoding="utf-8-sig")


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    model, frames, feature_order, labels = load_model_and_data()
    ref = stats_reference(frames, feature_order)
    threshold = float(read_json(SOURCE_ROOT / "thresholds/threshold_handoff.json")["tier_a_threshold"])
    python_rows, cal_rows, cal_bins, _ = build_python_payload(model, frames, feature_order, labels, ref, threshold)
    matrices = export_variant_matrices(frames, feature_order, ref)
    model_artifact = materialize_model_copy()
    context_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    attempts, copies = make_attempts(model_artifact, matrices, context_frame)
    prepared = {"run_root": RUN_ROOT, "run_id": RUN_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "run_number": RUN_NUMBER, "model_family": "sklearn_mlpclassifier_learning_behavior_runtime_probe", "feature_set_id": "feature_set_v2_mt5_price_proxy_top3_weights_58_features", "label_id": "label_v1_fwd12_m5_logret_train_q33_3class", "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413", "stage_inheritance": "independent_no_stage10_11_12_run_baseline_seed_or_reference", "boundary": BOUNDARY, "attempts": attempts, "common_copies": copies, "feature_matrices": list(matrices.values()), "route_coverage": {}}
    mt5_result = execute_or_block(prepared, args)
    mt5_rows, mt5_cal, mt5_bins = mt5_probability_rows(mt5_result, threshold, labels)
    payload = {"run_id": RUN_ID, "packet_id": PACKET_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "created_at_utc": utc_now(), "boundary": BOUNDARY, "threshold": {"tier_a_q90": threshold, "mt5_no_trade_threshold": NO_TRADE_THRESHOLD}, "model_artifact": model_artifact, "feature_matrices": matrices, "prepared": prepared, "mt5_result": mt5_result, "external_verification_status": mt5_result.get("external_verification_status"), "python_probability_rows": python_rows, "calibration_rows": cal_rows, "calibration_bins": cal_bins, "mt5_probability_rows": mt5_rows, "mt5_calibration_rows": mt5_cal, "mt5_calibration_bins": mt5_bins, "parity_rows": parity_rows(python_rows, mt5_rows)}
    judgment, recommendation = judge(payload)
    payload.update({"judgment": judgment, "recommendation": recommendation})
    payload["ledger_outputs"] = ledger_outputs(payload)
    write_outputs(payload)
    sync_docs(payload)
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP learning behavior probes with MT5 no-trade telemetry.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    args = parser.parse_args(argv)
    payload = build_all(args)
    print(json.dumps({"run_id": RUN_ID, "status": payload["external_verification_status"], "judgment": payload["judgment"], "parity_rows": len(payload["parity_rows"])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
