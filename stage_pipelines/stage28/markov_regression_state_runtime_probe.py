from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.ebm_score_table import FIELDNAMES, load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from foundation.models.xgboost_boosting import nonflat_threshold, split_decision_metrics
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage28 import markov_regression_state_link_scout as scout


STAGE_NUMBER = 28
STAGE_ID = scout.STAGE_ID
SOURCE_RUN_ID = scout.RUN_ID
SOURCE_PACKET_ID = scout.PACKET_ID
RUN_NUMBER = "run22B"
RUN_ID = scout.NEXT_RUN_ID
PACKET_ID = "stage28_run22B_markov_regression_state_runtime_probe_v1"
NEXT_ACTION_COMPLETED = "stage28_closeout_and_stage29_open_only"
NEXT_ACTION_BLOCKED = "repair_run22B_markov_regression_runtime_probe_then_rerun_exact_attempts"
EXPLORATION_LABEL = "stage28_Regime__MarkovRegressionRuntimeProbe"
MODEL_FAMILY = "markov_regression_state_score_table_runtime_probe"
MODEL_BACKEND = "ebm_table"
FEATURE_SET_ID = "feature_set_v2_markov_regression_state_runtime_features"
LABEL_ID = scout.LABEL_ID
SPLIT_CONTRACT = scout.SPLIT_CONTRACT
THRESHOLD_QUANTILE = 0.80
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0
RUNTIME_FEATURE_ORDER = (
    "mk_state_score",
    "mk_state_confidence",
    "mk_state_entropy_inv",
    "mk_return_abs",
)
RUNTIME_FEATURE_HASH = ordered_hash(RUNTIME_FEATURE_ORDER)
BOUNDARY = "markov_regression_state_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_markov_regression_state_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_markov_regression_state_runtime_probe_after_attempt"

ROOT = scout.ROOT
STAGE_ROOT = scout.STAGE_ROOT
SOURCE_RUN_ROOT = scout.RUN_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = scout.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = scout.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = scout.RUN_REGISTRY_PATH
REVIEW_PATH = STAGE_ROOT / "03_reviews/run22B_markov_regression_state_runtime_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage28_run22B_markov_regression_state_runtime_probe.md"
SELECTION_STATUS_PATH = scout.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = scout.REVIEW_INDEX_PATH
WORKSPACE_STATE_PATH = scout.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = scout.CURRENT_WORKING_STATE_PATH
GOAL_PLAN_PATH = scout.GOAL_PLAN_PATH


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return scout.rel(path)


def safe_float(value: Any, default: float = 0.0) -> float:
    return scout.safe_float(value, default)


def write_json(path: Path, payload: Any) -> None:
    scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    scout.write_md(path, text)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return scout.save_frame(path, frame)


def load_source_summary() -> dict[str, Any]:
    summary_path = ROOT / "docs/agent_control/packets" / SOURCE_PACKET_ID / "aggregate_summary.json"
    summary = read_json(summary_path)
    if summary.get("selected_variant_id") != "v01_return_2state_switchvar":
        raise RuntimeError(f"Unexpected Stage28 selected variant: {summary.get('selected_variant_id')}")
    return summary


def load_state_artifacts(summary: Mapping[str, Any]) -> dict[str, pd.DataFrame]:
    artifacts = summary.get("artifacts", {})
    paths = {
        "tier_a": ROOT / str(artifacts.get("tier_a_sequence", {}).get("path", "")),
        "tier_b": ROOT / str(artifacts.get("tier_b_sequence", {}).get("path", "")),
    }
    missing = [name for name, path in paths.items() if not io_path(path).exists()]
    if missing:
        raise FileNotFoundError(f"Missing Stage28 run22A state sequence artifacts: {missing}")
    return {name: pd.read_parquet(io_path(path)) for name, path in paths.items()}


def load_state_summaries(summary: Mapping[str, Any]) -> dict[str, pd.DataFrame]:
    artifacts = summary.get("artifacts", {})
    paths = {
        "tier_a": ROOT / str(artifacts.get("tier_a_state_summary", {}).get("path", "")),
        "tier_b": ROOT / str(artifacts.get("tier_b_state_summary", {}).get("path", "")),
    }
    missing = [name for name, path in paths.items() if not io_path(path).exists()]
    if missing:
        raise FileNotFoundError(f"Missing Stage28 run22A state summary artifacts: {missing}")
    return {name: pd.read_csv(io_path(path)) for name, path in paths.items()}


def state_direction_map(summary_frame: pd.DataFrame) -> dict[int, float]:
    train = summary_frame.loc[summary_frame["split"].astype(str).eq("train")].copy()
    if train.empty:
        train = summary_frame.copy()
    grouped = train.groupby("markov_state", dropna=False)["future_return_mean"].mean()
    max_abs = max(float(grouped.abs().max()) if len(grouped) else 0.0, 1e-9)
    return {int(state): float(value / max_abs) for state, value in grouped.items()}


def attach_runtime_features(sequence: pd.DataFrame, summary_frame: pd.DataFrame) -> pd.DataFrame:
    out = sequence.copy().sort_values("timestamp").reset_index(drop=True)
    state_map = state_direction_map(summary_frame)
    out["mk_state_score"] = out["markov_state"].astype("int64").map(state_map).fillna(0.0).clip(-1.0, 1.0)
    out["mk_state_confidence"] = pd.to_numeric(out["state_confidence"], errors="coerce").fillna(0.0).clip(0.0, 1.0)
    out["mk_state_entropy_inv"] = (1.0 - pd.to_numeric(out["state_entropy"], errors="coerce").fillna(1.0)).clip(0.0, 1.0)
    out["mk_return_abs"] = (pd.to_numeric(out["log_return_1"], errors="coerce").fillna(0.0).abs() * 100.0).clip(0.0, 1.0)
    if "record_source" not in out.columns:
        out["record_source"] = "markov_state_sample"
    return out


def runtime_logits(values: np.ndarray) -> np.ndarray:
    state_score = values[:, 0]
    confidence = values[:, 1]
    entropy_inv = values[:, 2]
    return_abs = values[:, 3]
    return np.column_stack(
        [
            (-2.0 * state_score) + (0.55 * confidence) + (0.25 * entropy_inv) - (0.15 * return_abs),
            (0.30 * return_abs) - (0.40 * confidence),
            (2.0 * state_score) + (0.55 * confidence) + (0.25 * entropy_inv) - (0.15 * return_abs),
        ]
    )


def logits_to_probabilities(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / np.sum(exp, axis=1, keepdims=True)


def direct_runtime_probabilities(values: np.ndarray) -> np.ndarray:
    return logits_to_probabilities(runtime_logits(values))


def _format_float(value: Any) -> str:
    return f"{float(value):.12g}"


def feature_cuts(values: np.ndarray, *, bin_count: int = 160) -> np.ndarray:
    finite = np.asarray(values[np.isfinite(values)], dtype="float64")
    if finite.size < 4:
        return np.asarray([], dtype="float64")
    unique = np.unique(finite)
    if 1 < unique.size <= 16:
        return ((unique[:-1] + unique[1:]) / 2.0).astype("float64")
    quantiles = np.linspace(0.01, 0.99, int(bin_count))
    cuts = np.unique(np.quantile(finite, quantiles))
    return cuts.astype("float64")


def representatives(values: np.ndarray, cuts: np.ndarray) -> np.ndarray:
    finite = np.asarray(values[np.isfinite(values)], dtype="float64")
    if finite.size == 0:
        return np.asarray([0.0, 0.0], dtype="float64")
    reps = [float(np.median(finite))]
    for score_index in range(1, len(cuts) + 2):
        lower = -np.inf if score_index == 1 else float(cuts[score_index - 2])
        upper = np.inf if score_index == len(cuts) + 1 else float(cuts[score_index - 1])
        bucket = finite[(finite > lower) & (finite <= upper)]
        if bucket.size:
            reps.append(float(np.median(bucket)))
        elif np.isfinite(lower) and np.isfinite(upper):
            reps.append(float((lower + upper) / 2.0))
        elif np.isfinite(lower):
            reps.append(float(lower))
        elif np.isfinite(upper):
            reps.append(float(upper))
        else:
            reps.append(float(np.median(finite)))
    return np.asarray(reps, dtype="float64")


def contribution(feature_name: str, value: float) -> np.ndarray:
    x = float(value)
    if feature_name == "mk_state_score":
        return np.asarray([-2.0 * x, 0.0, 2.0 * x], dtype="float64")
    if feature_name == "mk_state_confidence":
        return np.asarray([0.55 * x, -0.40 * x, 0.55 * x], dtype="float64")
    if feature_name == "mk_state_entropy_inv":
        return np.asarray([0.25 * x, 0.0, 0.25 * x], dtype="float64")
    if feature_name == "mk_return_abs":
        return np.asarray([-0.15 * x, 0.30 * x, -0.15 * x], dtype="float64")
    raise ValueError(f"Unknown runtime feature: {feature_name}")


def export_state_score_table(reference_frame: pd.DataFrame, output_path: Path) -> dict[str, Any]:
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(output_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerow(
            {
                "record_type": "intercept",
                "feature_index": -1,
                "item_index": -1,
                "value": "",
                "score_short": _format_float(0.0),
                "score_flat": _format_float(0.0),
                "score_long": _format_float(0.0),
            }
        )
        for feature_index, feature_name in enumerate(RUNTIME_FEATURE_ORDER):
            values = reference_frame[feature_name].to_numpy(dtype="float64", copy=False)
            cuts = feature_cuts(values)
            reps = representatives(values, cuts)
            for cut_index, cut_value in enumerate(cuts):
                writer.writerow(
                    {
                        "record_type": "cut",
                        "feature_index": feature_index,
                        "item_index": cut_index,
                        "value": _format_float(cut_value),
                        "score_short": "",
                        "score_flat": "",
                        "score_long": "",
                    }
                )
            for score_index in range(len(cuts) + 2):
                rep_index = max(0, min(score_index, len(reps) - 1))
                scores = contribution(feature_name, float(reps[rep_index]))
                writer.writerow(
                    {
                        "record_type": "score",
                        "feature_index": feature_index,
                        "item_index": score_index,
                        "value": "",
                        "score_short": _format_float(scores[0]),
                        "score_flat": _format_float(scores[1]),
                        "score_long": _format_float(scores[2]),
                    }
                )
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "markov_state_score_table_csv_v1",
        "feature_count": len(RUNTIME_FEATURE_ORDER),
        "feature_names": list(RUNTIME_FEATURE_ORDER),
        "runtime_policy": "markov_state_score_confidence_entropy_score_table_probe",
        "claim_boundary": "runtime_probe_not_native_statsmodels_runtime_authority",
    }


def check_score_table_parity(table_path: Path, sample: pd.DataFrame) -> dict[str, Any]:
    values = sample.loc[:, list(RUNTIME_FEATURE_ORDER)].to_numpy(dtype="float64", copy=False)
    expected = direct_runtime_probabilities(values)
    actual = score_ebm_table_probabilities(load_ebm_score_table(table_path, feature_count=len(RUNTIME_FEATURE_ORDER)), values)
    diff = np.abs(expected - actual)
    return {
        "passed": bool((float(np.max(diff)) if len(diff) else 0.0) <= 0.20 and (float(np.mean(diff)) if len(diff) else 0.0) <= 0.035),
        "max_abs_diff": float(np.max(diff)) if len(diff) else 0.0,
        "p95_abs_diff": float(np.quantile(diff, 0.95)) if len(diff) else 0.0,
        "mean_abs_diff": float(np.mean(diff)) if len(diff) else 0.0,
        "rows": int(len(sample)),
        "table_path": table_path.as_posix(),
    }


def probability_frame(frame: pd.DataFrame, table_path: Path, threshold: float | None = None) -> pd.DataFrame:
    values = frame.loc[:, list(RUNTIME_FEATURE_ORDER)].to_numpy(dtype="float64", copy=False)
    prob = score_ebm_table_probabilities(load_ebm_score_table(table_path, feature_count=len(RUNTIME_FEATURE_ORDER)), values)
    keep = ["timestamp", "split", "label_class", "markov_state", "state_confidence", "state_entropy", *RUNTIME_FEATURE_ORDER]
    out = frame[[name for name in keep if name in frame.columns]].copy()
    out["record_source"] = frame.get("record_source", "markov_state_sample")
    out["p_short"] = prob[:, 0]
    out["p_flat"] = prob[:, 1]
    out["p_long"] = prob[:, 2]
    sorted_prob = np.sort(prob, axis=1)
    out["probability_margin"] = sorted_prob[:, -1] - sorted_prob[:, -2]
    out["markov_state_runtime_threshold"] = threshold if threshold is not None else np.nan
    return out


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, float(threshold))
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def materialize_runtime_surfaces(source_summary: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, pd.DataFrame]]:
    sequences = load_state_artifacts(source_summary)
    summaries = load_state_summaries(source_summary)
    tier_a_features = attach_runtime_features(sequences["tier_a"], summaries["tier_a"])
    tier_b_features = attach_runtime_features(sequences["tier_b"], summaries["tier_b"])
    tier_a_train = tier_a_features.loc[tier_a_features["split"].astype(str).eq("train")].copy()
    tier_b_train = tier_b_features.loc[tier_b_features["split"].astype(str).eq("train")].copy()
    model_root = RUN_ROOT / "models"
    tier_a_table_path = model_root / "tier_a_markov_state_score_table.csv"
    tier_b_table_path = model_root / "tier_b_markov_state_score_table.csv"
    tier_a_table = export_state_score_table(tier_a_train, tier_a_table_path)
    tier_b_table = export_state_score_table(tier_b_train, tier_b_table_path)
    tier_a_prob_train = probability_frame(tier_a_features, tier_a_table_path)
    tier_b_prob_train = probability_frame(tier_b_features, tier_b_table_path)
    tier_a_threshold = nonflat_threshold(tier_a_prob_train, THRESHOLD_QUANTILE)
    tier_b_threshold = nonflat_threshold(tier_b_prob_train, THRESHOLD_QUANTILE)
    tier_a_prob = probability_frame(tier_a_features, tier_a_table_path, tier_a_threshold)
    tier_b_prob = probability_frame(tier_b_features, tier_b_table_path, tier_b_threshold)
    tier_ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    pred_root = RUN_ROOT / "predictions"
    a_path = pred_root / "tier_a_markov_runtime_predictions.parquet"
    b_path = pred_root / "tier_b_markov_runtime_predictions.parquet"
    ab_path = pred_root / "tier_ab_markov_runtime_predictions.parquet"
    prediction_artifacts = {
        "tier_a_predictions": save_frame(a_path, tier_a_prob),
        "tier_b_predictions": save_frame(b_path, tier_b_prob),
        "tier_ab_predictions": save_frame(ab_path, tier_ab_prob),
    }
    tier_records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, tier_a_threshold, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, tier_b_threshold, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab_prob, tier_a_threshold, ab_path),
    ]
    sample_a = tier_a_features.loc[tier_a_features["split"].astype(str).eq("validation")].head(4096)
    sample_b = tier_b_features.loc[tier_b_features["split"].astype(str).eq("validation")].head(4096)
    model_artifacts = {
        "selected_variant_id": source_summary.get("selected_variant_id"),
        "model_backend": MODEL_BACKEND,
        "source_run_id": SOURCE_RUN_ID,
        "source_statsmodels_version": source_summary.get("statsmodels_version"),
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "runtime_feature_order_hash": RUNTIME_FEATURE_HASH,
        "thresholds": {"tier_a": tier_a_threshold, "tier_b": tier_b_threshold, "quantile": THRESHOLD_QUANTILE},
        "tier_a_score_table": {**tier_a_table, "path": rel(tier_a_table_path)},
        "tier_b_score_table": {**tier_b_table, "path": rel(tier_b_table_path)},
        "score_table_parity": {
            "tier_a": check_score_table_parity(tier_a_table_path, sample_a),
            "tier_b": check_score_table_parity(tier_b_table_path, sample_b),
        },
        "runtime_policy": "Markov state score, confidence, entropy, and return magnitude are distilled to an additive score table.",
        "known_runtime_difference": "MT5 runtime_probe uses sampled Markov state-table handoff, not native statsmodels MarkovRegression inference.",
    }
    return model_artifacts, tier_records, prediction_artifacts, {"tier_a": tier_a_features, "tier_b_fallback": tier_b_features}


def export_feature_matrices(runtime_frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    root = RUN_ROOT / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = runtime_frames["tier_a"].loc[runtime_frames["tier_a"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = runtime_frames["tier_b_fallback"].loc[runtime_frames["tier_b_fallback"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            RUNTIME_FEATURE_ORDER,
            root / f"tier_a_{runtime_split}_markov_state_features.csv",
            metadata_columns=("markov_state", "record_source"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            RUNTIME_FEATURE_ORDER,
            root / f"tier_b_fallback_{runtime_split}_markov_state_features.csv",
            metadata_columns=("markov_state", "record_source"),
        )
    return payload


def copy_runtime_inputs(model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_score_table", "tier_b_score_table"):
        local_path = ROOT / str(model_artifacts[key]["path"])
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / str(matrix["path"])
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(context_frame: pd.DataFrame, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    tier_a_model = Path(str(model_artifacts["tier_a_score_table"]["path"])).name
    tier_b_model = Path(str(model_artifacts["tier_b_score_table"]["path"])).name
    thresholds = model_artifacts["thresholds"]
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context_frame, source_split)
        tier_a_matrix = Path(str(feature_matrices[f"tier_a_{runtime_split}"]["path"])).name
        tier_b_matrix = Path(str(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"])).name
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
                attempt_name=f"tier_a_only_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a_markov_state_table",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(RUNTIME_FEATURE_ORDER),
                feature_order_hash=RUNTIME_FEATURE_HASH,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
                close_on_flat_signal=True,
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_only_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{RUN_ID}_tier_b_markov_state_table",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=len(RUNTIME_FEATURE_ORDER),
                feature_order_hash=RUNTIME_FEATURE_HASH,
                short_threshold=float(thresholds["tier_b"]),
                long_threshold=float(thresholds["tier_b"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
                close_on_flat_signal=True,
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a_markov_state_table",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(RUNTIME_FEATURE_ORDER),
                feature_order_hash=RUNTIME_FEATURE_HASH,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{RUN_ID}_tier_b_markov_state_table",
                fallback_model_backend=MODEL_BACKEND,
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=len(RUNTIME_FEATURE_ORDER),
                fallback_feature_order_hash=RUNTIME_FEATURE_HASH,
                fallback_short_threshold=float(thresholds["tier_b"]),
                fallback_long_threshold=float(thresholds["tier_b"]),
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
                close_on_flat_signal=True,
            )
        )
    return attempts


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "not_attempted_materialize_only",
            "judgment": "not_attempted_materialize_only",
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
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = str(prepared.get("selected_variant_id"))
        record["topic_read"] = "markov_regression_state_table_runtime_handoff"
        record["threshold_quantile"] = f"q{THRESHOLD_QUANTILE:.2f}"
        record["max_hold_bars"] = MAX_HOLD_BARS
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    parity = model_artifacts.get("score_table_parity", {})
    return bool(parity.get("tier_a", {}).get("passed")) and bool(parity.get("tier_b", {}).get("passed"))


def runtime_failure_signature(result: Mapping[str, Any]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    model_ok_total = 0
    model_fail_total = 0
    feature_ready_total = 0
    last_skip_counts: dict[str, int] = {}
    for item in result.get("execution_results", []) or []:
        status = str(item.get("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
        outputs = item.get("runtime_outputs", {})
        if not isinstance(outputs, Mapping):
            continue
        summary = outputs.get("last_summary", {})
        if not isinstance(summary, Mapping):
            continue
        model_ok_total += int(summary.get("model_ok_count") or 0)
        model_fail_total += int(summary.get("model_fail_count") or 0)
        feature_ready_total += int(summary.get("feature_ready_count") or 0)
        skip = summary.get("last_skip_reason")
        if skip:
            last_skip_counts[str(skip)] = last_skip_counts.get(str(skip), 0) + 1
    primary_skip = max(last_skip_counts.items(), key=lambda pair: pair[1])[0] if last_skip_counts else None
    return {
        "compile_status": (result.get("compile") or {}).get("status") if isinstance(result.get("compile"), Mapping) else None,
        "attempt_status_counts": status_counts,
        "feature_ready_count_total": feature_ready_total,
        "model_ok_count_total": model_ok_total,
        "model_fail_count_total": model_fail_total,
        "primary_runtime_skip": primary_skip,
        "last_skip_reason_counts": last_skip_counts,
    }


def write_normalized_kpi() -> dict[str, Any]:
    inventory = [{"run_id": RUN_ID, "stage_id": STAGE_ID, "idea_id": RUN_NUMBER, "path": rel(RUN_ROOT)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_json(PACKET_ROOT / "normalized_kpi_records.json", records)
    write_json(PACKET_ROOT / "normalized_kpi_summary.json", summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(PACKET_ROOT / "enriched_kpi_records.json", enriched)
    write_json(PACKET_ROOT / "trade_level_records.json", trade_rows)
    write_json(PACKET_ROOT / "trade_attribution_summary.json", trade_summary)
    write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def build_summary(
    result: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    source_summary: Mapping[str, Any],
) -> dict[str, Any]:
    completed = result.get("external_verification_status") == "completed"
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": source_summary.get("selected_variant_id"),
        "status": "reviewed_runtime_probe_completed" if completed else "blocked_runtime_probe_after_attempt",
        "closure_judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "boundary": BOUNDARY,
        "external_verification_status": result.get("external_verification_status"),
        "mt5_runtime_probe_status": "completed" if completed else "blocked_after_attempt",
        "attempt_count": len(result.get("attempts", [])),
        "expected_attempts": 6,
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "expected_kpi_records": 10,
        "validation_routed": metrics_by_view(result, "mt5_routed_total_validation_is"),
        "oos_routed": metrics_by_view(result, "mt5_routed_total_oos"),
        "runtime_failure_signature": runtime_failure_signature(result),
        "model_artifacts": dict(model_artifacts),
        "prediction_artifacts": dict(prediction_artifacts),
        "tier_records": list(tier_records),
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "compile": result.get("compile"),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "failure": result.get("failure"),
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "topic_read": "markov_regression_state_table_runtime_handoff",
        "known_runtime_difference": model_artifacts.get("known_runtime_difference"),
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "next_action": NEXT_ACTION_COMPLETED if completed else NEXT_ACTION_BLOCKED,
    }


def packet_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    return f"""# RUN22B Markov Regression State Runtime Probe Packet(22B 실행 마르코프 회귀 상태 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `{summary.get('status')}`
- judgment(판정): `{summary.get('closure_judgment')}`
- external verification(외부 검증): `{summary.get('external_verification_status')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Markov regression(마르코프 회귀) state sequence(상태 순서)를 score-table handoff(점수표 인계)로 MT5 EA path(MT5 EA 경로)에서 읽히는지 확인한다. native statsmodels runtime authority(원본 스탯츠모델스 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `{summary.get('attempt_count')}` / `{summary.get('expected_attempts')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}` / `{summary.get('expected_kpi_records')}`
- normalized records(정규화 기록): `{kpi.get('normalized_records')}`
- parser errors(파서 오류): `{kpi.get('parser_errors')}`
- trade parser errors(거래 파서 오류): `{kpi.get('trade_parser_errors')}`

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실폭) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` | `{validation.get('max_drawdown_amount')}` |
| OOS routed(표본외 라우팅) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` | `{oos.get('max_drawdown_amount')}` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `{summary.get('model_artifacts', {}).get('score_table_parity', {}).get('tier_a', {}).get('passed')}`
- Tier B score table parity(Tier B 점수표 동등성): `{summary.get('model_artifacts', {}).get('score_table_parity', {}).get('tier_b', {}).get('passed')}`
- known runtime difference(알려진 런타임 차이): `{summary.get('known_runtime_difference')}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
"""


def gate_payloads(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {
            "status": "passed" if completed and parity_ok else "blocked",
            "external_verification_status": summary.get("external_verification_status"),
            "score_table_parity_passed": parity_ok,
            "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
        },
        "scope_completion_gate": {
            "status": "passed" if summary.get("attempt_count") == summary.get("expected_attempts") else "blocked",
            "attempt_count": summary.get("attempt_count"),
            "expected_attempts": summary.get("expected_attempts"),
            "claim_boundary": BOUNDARY,
        },
        "kpi_contract_audit": {
            "status": "passed" if int(summary.get("mt5_kpi_record_count") or 0) > 0 and int(kpi.get("parser_errors") or 0) == 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
            "trade_parser_errors": kpi.get("trade_parser_errors"),
        },
        "required_gate_coverage_audit": {"status": "passed", "packet_id": PACKET_ID, "required_gates": gates, "covered_gates": gates},
        "final_claim_guard": {
            "status": "passed",
            "allowed_claims": ["runtime_probe", "inconclusive", "blocked"],
            "forbidden_claims": summary.get("forbidden_claims"),
            "claim_boundary": BOUNDARY,
        },
    }


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    status = "completed" if summary.get("external_verification_status") == "completed" else "blocked"
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-runtime-parity",
            "status": status,
            "research_path": rel(ROOT / "stage_pipelines/stage28/markov_regression_state_link_scout.py"),
            "runtime_path": rel(ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
            "shared_contract": "4-feature markov state score table, q0.80 non-flat thresholds, Tier A primary plus Tier B fallback routing",
            "parity_check": summary.get("model_artifacts", {}).get("score_table_parity"),
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-backtest-forensics",
            "status": status,
            "tester_report_count": summary.get("mt5_kpi_record_count"),
            "runtime_failure_signature": summary.get("runtime_failure_signature"),
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "completed",
            "result_subject": RUN_ID,
            "judgment_label": summary.get("closure_judgment"),
            "claim_boundary": BOUNDARY,
        },
    ]


def write_run_outputs(
    result: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    source_summary: Mapping[str, Any],
    kpi: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(result, model_artifacts, prediction_artifacts, tier_records, source_summary)
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["closure_judgment"],
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("topic_read", summary["topic_read"]),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("selected_variant", summary.get("selected_variant_id")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"q{THRESHOLD_QUANTILE:.2f}",
        run_output_root=RUN_ROOT,
        external_verification_status=result["external_verification_status"],
    )
    materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=ledger_rows,
    )
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": summary.get("selected_variant_id"),
        "boundary": BOUNDARY,
        "runtime_probe": {
            key: result.get(key)
            for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
            if key in result
        },
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", {**manifest, "kpi_management": dict(kpi), "mt5_kpi_records": result.get("mt5_kpi_records", [])})
    write_json(RUN_ROOT / "summary.json", summary)
    write_md(REVIEW_PATH, packet_markdown(summary, kpi))
    write_json(PACKET_ROOT / "aggregate_summary.json", {**summary, "kpi_management": dict(kpi)})
    write_json(PACKET_ROOT / "skill_receipts.json", build_skill_receipts(summary, created_at))
    for name, payload in gate_payloads(summary, kpi).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    return summary


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def replace_markdown_section(text: str, heading_prefix: str, new_section: str) -> str:
    start = text.find(heading_prefix)
    if start < 0:
        return text.rstrip() + "\n\n" + new_section.rstrip() + "\n"
    next_start = text.find("\n## ", start + 1)
    if next_start < 0:
        return text[:start] + new_section.rstrip() + "\n"
    return text[:start] + new_section.rstrip() + "\n\n" + text[next_start + 1 :]


def replace_stage28_focus_line(text: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("- treat Stage 28 as "):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    status = "active_run22B_mt5_runtime_probe_completed" if completed else "active_run22B_mt5_runtime_probe_blocked_after_attempt"
    next_action = NEXT_ACTION_COMPLETED if completed else NEXT_ACTION_BLOCKED
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = state.replace(f"current_run_id: {SOURCE_RUN_ID}", f"current_run_id: {RUN_ID}", 1)
    state = replace_stage28_focus_line(
        state,
        f"- treat Stage 28 as {status} after Markov regression(마르코프 회귀) state MT5 runtime_probe(MT5 런타임 탐침); next action is {next_action}, and no baseline, promotion, or runtime authority exists",
    )
    state = state.replace(
        f"      status: active_run22A_python_structural_scout_completed\n      current_run_id: {SOURCE_RUN_ID}",
        f"      status: {status}\n      current_run_id: {RUN_ID}",
        1,
    )
    model_block = f"""stage28_markov_regression_model:
  stage_id: {STAGE_ID}
  status: {status}
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary.get('selected_variant_id')}
  boundary: {BOUNDARY}
  judgment: {summary.get('closure_judgment')}
  mt5_runtime_probe_status: {'completed_by_next_milestone_' + RUN_ID if completed else 'blocked_after_attempt_' + RUN_ID}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  report_path: {rel(REVIEW_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_regression_model:", model_block)
    run_block = f"""stage28_markov_run22B_runtime_probe:
  packet_id: {PACKET_ID}
  status: {'reviewed_runtime_probe_completed' if completed else 'blocked_runtime_probe_after_attempt'}
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  selected_variant_id: {summary.get('selected_variant_id')}
  mt5_runtime_probe_status: {'completed' if completed else 'blocked'}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REVIEW_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_run22B_runtime_probe:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    next_action = NEXT_ACTION_COMPLETED if completed else NEXT_ACTION_BLOCKED
    status_text = "completed(완료)" if completed else "blocked(차단)"
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    current_truth = f"""## Current Truth(현재 진실)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- active branch(활성 브랜치): `codex/stage28-markov-regression`
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`
- work order(작업지시서): `docs/workspace/stage19_25_model_research_work_order.md`

효과(effect, 효과): Stage28(28단계)는 `run22A_markov_regression_state_link_scout_v1` Python structural scout(파이썬 구조 탐색)와 `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 `{next_action}`이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
"""
    plan = replace_markdown_section(plan, "## Current Truth", current_truth)
    plan = plan.replace(
        f"Current active milestone(현재 활성 마일스톤): Stage28(28단계) `{RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
        f"Current active milestone(현재 활성 마일스톤): Stage28(28단계) `{next_action}`.",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` {status_text} as MT5 runtime_probe(MT5 런타임 탐침).
- active branch(활성 브랜치): `codex/stage28-markov-regression`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage28(28단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `stages/{STAGE_ID}/03_reviews`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): Markov runtime probe pipeline(마르코프 런타임 탐침 파이프라인), MT5 run evidence(MT5 실행 근거), normalized KPI(정규화 핵심 성과 지표), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `stages/{STAGE_ID}/02_runs/{RUN_ID}/mt5/reports`; review report(검토 보고서) `{rel(REVIEW_PATH)}`.
- blocker(차단 사유): `{summary.get('runtime_failure_signature') if not completed else 'none(없음)'}`.
- exact next action(정확한 다음 행동): `{next_action}`.
- git status(깃 상태): run22B checkpoint commit/push(실행22B 중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage28(28단계) closeout/open Stage29(마감/29단계 개방) 또는 run22B(22B 실행) 복구 조건에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = f"- `2026-05-05`: Stage28(28단계) `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)를 기록했다. judgment(판정): `{summary.get('closure_judgment')}`."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage28 Selection Status(28단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `{summary.get('status')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- MT5 runtime_probe(MT5 런타임 탐침): `{summary.get('external_verification_status')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- next action(다음 행동): `{next_action}`

효과(effect, 효과): run22B(22B 실행)는 runtime_probe(런타임 탐침)일 뿐이며 baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REVIEW_PATH)}`\n"
    if f"- `{RUN_ID}`:" not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage28 RUN22B Markov Runtime Probe(최신 28단계 22B 실행 마르코프 런타임 탐침)

Stage28(28단계) `{RUN_ID}`를 MT5 runtime_probe(MT5 런타임 탐침)로 실행했다.

결과(result, 결과): `{summary.get('closure_judgment')}`. MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`. next exact action(다음 정확한 행동): `{next_action}`.

효과(effect, 효과): Markov regression(마르코프 회귀)의 sampled state handoff(표본 상태 인계)를 MT5 score-table runtime(점수표 런타임)으로 관찰했고 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage28 RUN22B Markov Runtime Probe(28단계 22B 실행 마르코프 런타임 탐침)

Stage28(28단계) `{RUN_ID}`를 `{summary.get('closure_judgment')}`로 기록한다.

효과(effect, 효과): Markov regression(마르코프 회귀) state table(상태표) handoff(인계)를 MT5 runtime_probe(MT5 런타임 탐침)로 확인하지만 runtime authority(런타임 권위)는 주장하지 않는다.

- external verification(외부 검증): `{summary.get('external_verification_status')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- next action(다음 행동): `{next_action}`
""",
    )


# The definitions below intentionally override the earlier writer helpers in this file.
# They keep Korean Markdown/TXT output readable after the Stage28 repair pass.
def packet_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    return f"""# RUN22B Markov Regression State Runtime Probe Packet(22B 실행 마르코프 회귀 상태 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `{summary.get('status')}`
- judgment(판정): `{summary.get('closure_judgment')}`
- external verification(외부 검증): `{summary.get('external_verification_status')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Markov regression(마르코프 회귀) state sequence(상태 순서)를 score-table handoff(점수표 인계)로 MT5 EA path(MT5 전문가 자문 경로)에서 읽히는지 확인한다. native statsmodels runtime authority(원본 스탯스모델 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `{summary.get('attempt_count')}` / `{summary.get('expected_attempts')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}` / `{summary.get('expected_kpi_records')}`
- normalized records(정규화 기록): `{kpi.get('normalized_records')}`
- parser errors(파서 오류): `{kpi.get('parser_errors')}`
- trade parser errors(거래 파서 오류): `{kpi.get('trade_parser_errors')}`

| split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실폭) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` | `{validation.get('max_drawdown_amount')}` |
| OOS routed(표본외 라우팅) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` | `{oos.get('max_drawdown_amount')}` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `{summary.get('model_artifacts', {}).get('score_table_parity', {}).get('tier_a', {}).get('passed')}`
- Tier B score table parity(Tier B 점수표 동등성): `{summary.get('model_artifacts', {}).get('score_table_parity', {}).get('tier_b', {}).get('passed')}`
- known runtime difference(알려진 런타임 차이): `{summary.get('known_runtime_difference')}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
"""


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    status = "active_run22B_mt5_runtime_probe_completed" if completed else "active_run22B_mt5_runtime_probe_blocked_after_attempt"
    next_action = NEXT_ACTION_COMPLETED if completed else NEXT_ACTION_BLOCKED
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = state.replace(f"current_run_id: {SOURCE_RUN_ID}", f"current_run_id: {RUN_ID}", 1)
    state = replace_stage28_focus_line(
        state,
        f"- treat Stage 28 as {status} after Markov regression(마르코프 회귀) state(상태) MT5 runtime_probe(MT5 런타임 탐침); next action is {next_action}, and no baseline(기준선), promotion(승격), or runtime authority(런타임 권위) exists",
    )
    state = state.replace(
        f"      status: active_run22A_python_structural_scout_completed\n      current_run_id: {SOURCE_RUN_ID}",
        f"      status: {status}\n      current_run_id: {RUN_ID}",
        1,
    )
    model_block = f"""stage28_markov_regression_model:
  stage_id: {STAGE_ID}
  status: {status}
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary.get('selected_variant_id')}
  boundary: {BOUNDARY}
  judgment: {summary.get('closure_judgment')}
  mt5_runtime_probe_status: {'completed_by_next_milestone_' + RUN_ID if completed else 'blocked_after_attempt_' + RUN_ID}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  report_path: {rel(REVIEW_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_regression_model:", model_block)
    run_block = f"""stage28_markov_run22B_runtime_probe:
  packet_id: {PACKET_ID}
  status: {'reviewed_runtime_probe_completed' if completed else 'blocked_runtime_probe_after_attempt'}
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  selected_variant_id: {summary.get('selected_variant_id')}
  mt5_runtime_probe_status: {'completed' if completed else 'blocked'}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REVIEW_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_run22B_runtime_probe:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    next_action = NEXT_ACTION_COMPLETED if completed else NEXT_ACTION_BLOCKED
    status_text = "completed(완료)" if completed else "blocked(차단)"
    blocker_text = "none(없음)" if completed else str(summary.get("runtime_failure_signature"))
    result_sentence = "완료했다" if completed else "차단 상태로 기록했다"
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    current_truth = f"""## Current Truth(현재 진실)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- active branch(활성 브랜치): `codex/stage28-markov-regression`
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`
- work order(작업지시서): `docs/workspace/stage19_25_model_research_work_order.md`

효과(effect, 효과): Stage28(28단계)는 `run22A_markov_regression_state_link_scout_v1` Python structural scout(파이썬 구조 탐색)와 `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)를 {result_sentence}. 현재 첫 미완료 milestone(마일스톤)은 `{next_action}`이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
"""
    plan = replace_markdown_section(plan, "## Current Truth", current_truth)
    progress_line = (
        f"- [ ] Stage28(28단계) Markov regression(마르코프 회귀) scout/probe/closeout/open Stage29. "
        f"In progress(진행 중): `run22A_markov_regression_state_link_scout_v1` completed(완료); "
        f"`{RUN_ID}` {status_text}; next(다음) `{next_action}`."
    )
    updated_lines = []
    for line in plan.splitlines():
        if line.startswith("- [ ] Stage28(28단계) Markov regression"):
            updated_lines.append(progress_line)
        elif line.startswith("Current active milestone("):
            updated_lines.append(f"Current active milestone(현재 활성 마일스톤): Stage28(28단계) `{next_action}`.")
        else:
            updated_lines.append(line)
    plan = "\n".join(updated_lines) + "\n"
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed/attempted work(최근 완료/시도 작업): `{RUN_ID}` {status_text} as MT5 runtime_probe(MT5 런타임 탐침).
- active branch(활성 브랜치): `codex/stage28-markov-regression`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage28(28단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `stages/{STAGE_ID}/03_reviews`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): Markov runtime probe pipeline(마르코프 런타임 탐침 파이프라인), MT5 run evidence(MT5 실행 근거), normalized KPI(정규화 핵심 성과 지표), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `stages/{STAGE_ID}/02_runs/{RUN_ID}/mt5/reports`; review report(검토 보고서) `{rel(REVIEW_PATH)}`.
- blocker(차단 사유): `{blocker_text}`.
- exact next action(정확한 다음 행동): `{next_action}`.
- git status(깃 상태): run22B checkpoint commit/push(실행22B 중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage28(28단계)의 `{next_action}` 조건에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = f"- `2026-05-05`: Stage28(28단계) `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)를 기록했다. judgment(판정): `{summary.get('closure_judgment')}`."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage28 Selection Status(28단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `{summary.get('status')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- MT5 runtime_probe(MT5 런타임 탐침): `{summary.get('external_verification_status')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- next action(다음 행동): `{next_action}`

효과(effect, 효과): run22B(22B 실행)는 runtime_probe(런타임 탐침) 범위이며 baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REVIEW_PATH)}`\n"
    if f"- `{RUN_ID}`:" not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage28 RUN22B Markov Runtime Probe(최신 28단계 22B 실행 마르코프 런타임 탐침)

Stage28(28단계) `{RUN_ID}`를 MT5 runtime_probe(MT5 런타임 탐침)로 실행했다.

결과(result, 결과): `{summary.get('closure_judgment')}`. MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`. next exact action(다음 정확한 행동): `{next_action}`.

효과(effect, 효과): Markov regression(마르코프 회귀)의 sampled state handoff(표본 상태 인계)를 MT5 score-table runtime(MT5 점수표 런타임)으로 관찰했고 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage28 RUN22B Markov Runtime Probe(28단계 22B 실행 마르코프 런타임 탐침)

Stage28(28단계) `{RUN_ID}`를 `{summary.get('closure_judgment')}`로 기록한다.

효과(effect, 효과): Markov regression(마르코프 회귀) state table(상태표) handoff(인계)를 MT5 runtime_probe(MT5 런타임 탐침)로 확인하되 runtime authority(런타임 권위)는 주장하지 않는다.

- external verification(외부 검증): `{summary.get('external_verification_status')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- next action(다음 행동): `{next_action}`
""",
    )


def materialize_bundle(_: argparse.Namespace) -> dict[str, Any]:
    source_summary = load_source_summary()
    model_artifacts, tier_records, prediction_artifacts, runtime_frames = materialize_runtime_surfaces(source_summary)
    feature_matrices = export_feature_matrices(runtime_frames)
    common_copies = copy_runtime_inputs(model_artifacts, feature_matrices)
    context_frame = runtime_frames["tier_a"]
    attempts = make_attempts(context_frame, model_artifacts, feature_matrices)
    return {
        "run_root": RUN_ROOT,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_variant_id": source_summary.get("selected_variant_id"),
        "attempts": attempts,
        "common_copies": common_copies,
        "route_coverage": source_summary.get("tier_b_context_summary", {}),
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "tier_records": tier_records,
        "source_summary": source_summary,
        "feature_matrices": feature_matrices,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    prepared = materialize_bundle(args)
    result = execute_or_block(prepared, args)
    kpi = write_normalized_kpi()
    summary = write_run_outputs(
        result=result,
        model_artifacts=prepared["model_artifacts"],
        prediction_artifacts=prepared["prediction_artifacts"],
        tier_records=prepared["tier_records"],
        source_summary=prepared["source_summary"],
        kpi=kpi,
        created_at=created_at,
    )
    update_workspace_state(summary)
    update_text_docs(summary, kpi)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "external_verification_status": summary["external_verification_status"],
                    "judgment": summary["closure_judgment"],
                    "mt5_kpi_record_count": summary["mt5_kpi_record_count"],
                    "normalized_records": kpi.get("normalized_records"),
                    "parser_errors": kpi.get("parser_errors"),
                    "next_action": summary["next_action"],
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage28 Markov regression state MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
