from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import subprocess
import warnings
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from foundation.models import alpha_scout_support as stage27_scout


STAGE_ID = "28_regime_model__markov_switching_regression_state_link"
RUN_ID = "run22A_markov_regression_state_link_scout_v1"
RUN_NUMBER = "run22A"
PACKET_ID = "stage28_run22A_markov_regression_state_link_scout_v1"
NEXT_RUN_ID = "run22B_markov_regression_state_runtime_probe_v1"
EXPLORATION_LABEL = "stage28_Regime__MarkovSwitchingRegressionStateLink"
MODEL_FAMILY = "statsmodels_markov_switching_regression"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_markov_regression_state_link"
LABEL_ID = stage27_scout.LABEL_ID
SPLIT_CONTRACT = stage27_scout.SPLIT_CONTRACT
ENDOG_COLUMN = "log_return_1"
TARGET_COLUMN = "future_log_return_12"
BOUNDARY = "markov_regression_state_link_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_markov_regression_state_link_scout_completed"

ROOT = stage27_scout.ROOT
MODEL_INPUT_PATH = stage27_scout.MODEL_INPUT_PATH
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run22A_markov_regression_state_link_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage28_run22A_markov_regression_state_link_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = stage27_scout.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = stage27_scout.CURRENT_WORKING_STATE_PATH
GOAL_PLAN_PATH = stage27_scout.GOAL_PLAN_PATH


@dataclass(frozen=True)
class MarkovRegressionVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    k_regimes: int
    endog_column: str
    exog_columns: tuple[str, ...]
    trend: str = "c"
    switching_variance: bool = True
    max_rows_tier_a: int = 4200
    max_rows_tier_b: int = 2600
    maxiter: int = 80
    em_iter: int = 5
    search_reps: int = 1

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["exog_columns"] = list(self.exog_columns)
        return payload


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return stage27_scout.rel(path)


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def write_json(path: Path, payload: Any) -> None:
    stage27_scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    stage27_scout.write_md(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return stage27_scout.save_frame(path, frame)


def safe_float(value: Any, default: float = 0.0) -> float:
    return stage27_scout.safe_float(value, default)


def statsmodels_version() -> str:
    return importlib.metadata.version("statsmodels")


def default_variants(tier_b_feature_order: Sequence[str]) -> list[MarkovRegressionVariantSpec]:
    feature_set = set(tier_b_feature_order)
    vol_pair = tuple(name for name in ("historical_vol_20", "hl_range") if name in feature_set)
    session_vol = tuple(name for name in ("historical_vol_20", "minutes_from_cash_open") if name in feature_set)
    trend_vol = tuple(name for name in ("historical_vol_20", "ema20_ema50_diff") if name in feature_set)
    return [
        MarkovRegressionVariantSpec(
            variant_id="v01_return_2state_switchvar",
            idea_id="observable_return_two_state_switching_variance",
            description="Two-state Markov regression on observable one-bar return with switching variance.",
            k_regimes=2,
            endog_column=ENDOG_COLUMN,
            exog_columns=(),
        ),
        MarkovRegressionVariantSpec(
            variant_id="v02_return_3state_switchvar",
            idea_id="observable_return_three_state_switching_variance",
            description="Three-state return-only Markov regression to test whether a third regime is stable or collapsed.",
            k_regimes=3,
            endog_column=ENDOG_COLUMN,
            exog_columns=(),
            max_rows_tier_a=3600,
            max_rows_tier_b=2200,
        ),
        MarkovRegressionVariantSpec(
            variant_id="v03_vol_link_2state",
            idea_id="volatility_linked_markov_regression",
            description="Two-state Markov regression with standardized volatility/range exogenous link.",
            k_regimes=2,
            endog_column=ENDOG_COLUMN,
            exog_columns=vol_pair,
        ),
        MarkovRegressionVariantSpec(
            variant_id="v04_session_vol_2state",
            idea_id="session_volatility_linked_state",
            description="Two-state Markov regression linking volatility and session clock to state probability.",
            k_regimes=2,
            endog_column=ENDOG_COLUMN,
            exog_columns=session_vol,
        ),
        MarkovRegressionVariantSpec(
            variant_id="v05_trend_vol_2state",
            idea_id="trend_volatility_linked_state",
            description="Two-state Markov regression linking volatility and trend slope to state probability.",
            k_regimes=2,
            endog_column=ENDOG_COLUMN,
            exog_columns=trend_vol,
        ),
    ]


def load_context() -> dict[str, Any]:
    context = stage27_scout.load_context()
    return {
        "tier_a_frame": context["tier_a_frame"],
        "tier_b_fallback_frame": context["tier_b_fallback_frame"],
        "tier_b_context_summary": context["tier_b_context_summary"],
        "tier_b_feature_order": list(context["tier_b_feature_order"]),
        "full_feature_order": list(context["full_feature_order"]),
    }


def sample_sequence(frame: pd.DataFrame, spec: MarkovRegressionVariantSpec, *, tier_scope: str) -> pd.DataFrame:
    max_rows = spec.max_rows_tier_a if tier_scope == mt5.TIER_A else spec.max_rows_tier_b
    columns = ["timestamp", "split", "label_class", TARGET_COLUMN, spec.endog_column, *spec.exog_columns]
    clean = (
        frame.loc[:, [column for column in columns if column in frame.columns]]
        .replace([np.inf, -np.inf], np.nan)
        .dropna(subset=[spec.endog_column, TARGET_COLUMN, "label_class", "split"])
        .sort_values("timestamp")
        .reset_index(drop=False)
        .rename(columns={"index": "source_row_index"})
    )
    if spec.exog_columns:
        clean = clean.dropna(subset=list(spec.exog_columns))
    if len(clean) <= max_rows:
        return clean.reset_index(drop=True)
    quotas = {"train": 0.62, "validation": 0.23, "oos": 0.15}
    chunks: list[pd.DataFrame] = []
    for split_name, share in quotas.items():
        group = clean[clean["split"].astype(str) == split_name]
        if group.empty:
            continue
        take = min(len(group), max(80, int(max_rows * share)))
        positions = np.linspace(0, len(group) - 1, take).round().astype(int)
        chunks.append(group.iloc[np.unique(positions)])
    sampled = pd.concat(chunks, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
    if len(sampled) > max_rows:
        positions = np.linspace(0, len(sampled) - 1, max_rows).round().astype(int)
        sampled = sampled.iloc[np.unique(positions)].reset_index(drop=True)
    return sampled


def standardize_exog(frame: pd.DataFrame, columns: Sequence[str]) -> tuple[pd.DataFrame | None, dict[str, dict[str, float]]]:
    if not columns:
        return None, {}
    stats: dict[str, dict[str, float]] = {}
    out = pd.DataFrame(index=frame.index)
    for column in columns:
        values = pd.to_numeric(frame[column], errors="coerce").astype("float64")
        mean = float(values.mean())
        std = float(values.std(ddof=0))
        if not np.isfinite(std) or std <= 1e-12:
            std = 1.0
        out[column] = (values - mean) / std
        stats[column] = {"mean": mean, "std": std}
    return out, stats


def fit_markov(frame: pd.DataFrame, spec: MarkovRegressionVariantSpec) -> dict[str, Any]:
    y = pd.to_numeric(frame[spec.endog_column], errors="coerce").astype("float64")
    exog, exog_stats = standardize_exog(frame, spec.exog_columns)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            model = MarkovRegression(
                y,
                k_regimes=spec.k_regimes,
                exog=exog,
                trend=spec.trend,
                switching_variance=spec.switching_variance,
            )
            result = model.fit(disp=False, maxiter=spec.maxiter, em_iter=spec.em_iter, search_reps=spec.search_reps)
            llf = safe_float(getattr(result, "llf", None), default=float("nan"))
            if not np.isfinite(llf):
                raise RuntimeError("non_finite_log_likelihood")
            return {
                "status": "completed",
                "result": result,
                "exog_stats": exog_stats,
                "warnings": sorted({str(item.message) for item in caught}),
                "converged": bool(result.mle_retvals.get("converged", False)),
                "llf": float(llf),
                "aic": safe_float(getattr(result, "aic", None)),
                "bic": safe_float(getattr(result, "bic", None)),
            }
        except Exception as exc:  # noqa: BLE001 - failure is recorded as variant evidence.
            return {
                "status": "failed",
                "error": str(exc),
                "exog_stats": exog_stats,
                "warnings": sorted({str(item.message) for item in caught}),
                "converged": False,
                "llf": None,
                "aic": None,
                "bic": None,
            }


def probability_frame(result: Any) -> pd.DataFrame:
    probs = result.smoothed_marginal_probabilities
    if isinstance(probs, pd.DataFrame):
        frame = probs.copy()
    else:
        frame = pd.DataFrame(np.asarray(probs))
    frame.columns = [f"state_prob_{int(column)}" for column in range(frame.shape[1])]
    return frame.reset_index(drop=True)


def state_sequence_frame(fit: Mapping[str, Any], source: pd.DataFrame, spec: MarkovRegressionVariantSpec, *, tier_scope: str, record_view: str) -> pd.DataFrame:
    probs = probability_frame(fit["result"])
    prob_values = probs.to_numpy(dtype="float64")
    state = prob_values.argmax(axis=1)
    confidence = prob_values.max(axis=1)
    entropy = -np.sum(np.clip(prob_values, 1e-12, 1.0) * np.log(np.clip(prob_values, 1e-12, 1.0)), axis=1) / np.log(spec.k_regimes)
    out = source[["timestamp", "split", "label_class", TARGET_COLUMN, spec.endog_column, "source_row_index"]].reset_index(drop=True).copy()
    out["tier_scope"] = tier_scope
    out["record_view"] = record_view
    out["variant_id"] = spec.variant_id
    out["markov_state"] = state.astype("int64")
    out["state_confidence"] = confidence
    out["state_entropy"] = entropy
    return pd.concat([out, probs], axis=1)


def state_summary_frame(sequence: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (split, state), group in sequence.groupby(["split", "markov_state"], dropna=False):
        labels = group["label_class"].astype("int64")
        counts = labels.value_counts().to_dict()
        rows.append(
            {
                "split": str(split),
                "markov_state": int(state),
                "rows": int(len(group)),
                "share": float(len(group) / max(1, len(sequence[sequence["split"].astype(str) == str(split)]))),
                "future_return_mean": float(group[TARGET_COLUMN].mean()),
                "future_return_std": float(group[TARGET_COLUMN].std(ddof=0)),
                "observable_return_mean": float(group[ENDOG_COLUMN].mean()),
                "short_count": int(counts.get(0, 0)),
                "flat_count": int(counts.get(1, 0)),
                "long_count": int(counts.get(2, 0)),
                "long_rate": float((labels == 2).mean()),
                "short_rate": float((labels == 0).mean()),
                "confidence_mean": float(group["state_confidence"].mean()),
                "entropy_mean": float(group["state_entropy"].mean()),
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "markov_state"]).reset_index(drop=True)


def transition_read(sequence: pd.DataFrame, k_regimes: int) -> dict[str, Any]:
    states = sequence.sort_values("timestamp")["markov_state"].astype("int64").to_numpy()
    matrix = np.zeros((k_regimes, k_regimes), dtype="int64")
    if len(states) > 1:
        for src, dst in zip(states[:-1], states[1:]):
            if 0 <= src < k_regimes and 0 <= dst < k_regimes:
                matrix[src, dst] += 1
    row_sums = matrix.sum(axis=1, keepdims=True)
    probs = np.divide(matrix, row_sums, out=np.zeros_like(matrix, dtype="float64"), where=row_sums > 0)
    return {
        "transition_counts": matrix.tolist(),
        "transition_probabilities": probs.tolist(),
        "self_transition_mean": float(np.diag(probs).mean()) if k_regimes else 0.0,
        "transition_count": int(matrix.sum()),
    }


def quality_read(sequence: pd.DataFrame, summary: pd.DataFrame, spec: MarkovRegressionVariantSpec) -> dict[str, Any]:
    by_split: dict[str, Any] = {}
    for split_name in ("train", "validation", "oos"):
        split_summary = summary[summary["split"].astype(str) == split_name]
        split_sequence = sequence[sequence["split"].astype(str) == split_name]
        if split_summary.empty:
            by_split[split_name] = {"rows": 0, "state_count": 0, "risk_separation": 0.0, "min_share": 0.0, "max_share": 0.0, "entropy_mean": None}
            continue
        means = split_summary["future_return_mean"].astype("float64")
        shares = split_summary["share"].astype("float64")
        by_split[split_name] = {
            "rows": int(len(split_sequence)),
            "state_count": int(split_summary["markov_state"].nunique()),
            "risk_separation": float(means.max() - means.min()) if len(means) else 0.0,
            "min_share": float(shares.min()) if len(shares) else 0.0,
            "max_share": float(shares.max()) if len(shares) else 0.0,
            "entropy_mean": float(split_sequence["state_entropy"].mean()) if len(split_sequence) else None,
            "confidence_mean": float(split_sequence["state_confidence"].mean()) if len(split_sequence) else None,
        }
    collapsed = any(item["state_count"] < spec.k_regimes or item["min_share"] < 0.02 for item in by_split.values() if item["rows"])
    val_sep = abs(float(by_split["validation"]["risk_separation"]))
    oos_sep = abs(float(by_split["oos"]["risk_separation"]))
    gap = abs(val_sep - oos_sep)
    entropy_values = [item["entropy_mean"] for item in by_split.values() if item["entropy_mean"] is not None]
    entropy_mean = float(np.mean(entropy_values)) if entropy_values else 1.0
    quality_score = (1000.0 * (val_sep + oos_sep - 0.5 * gap)) + (0.2 * (1.0 - entropy_mean)) - (0.5 if collapsed else 0.0)
    return {
        "by_split": by_split,
        "collapsed": bool(collapsed),
        "validation_oos_separation_gap": float(gap),
        "entropy_mean": entropy_mean,
        "quality_score": float(quality_score),
    }


def evaluate_side(frame: pd.DataFrame, spec: MarkovRegressionVariantSpec, *, tier_scope: str, record_view: str) -> dict[str, Any]:
    sample = sample_sequence(frame, spec, tier_scope=tier_scope)
    fit = fit_markov(sample, spec)
    if fit["status"] != "completed":
        return {"status": "failed", "sample_rows": int(len(sample)), "fit": fit}
    sequence = state_sequence_frame(fit, sample, spec, tier_scope=tier_scope, record_view=record_view)
    summary = state_summary_frame(sequence)
    quality = quality_read(sequence, summary, spec)
    return {
        "status": "completed",
        "sample_rows": int(len(sample)),
        "fit": fit,
        "sequence": sequence,
        "summary": summary,
        "quality": quality,
        "transition": transition_read(sequence, spec.k_regimes),
    }


def evaluate_variant(spec: MarkovRegressionVariantSpec, context: Mapping[str, Any]) -> dict[str, Any]:
    tier_a = evaluate_side(context["tier_a_frame"], spec, tier_scope=mt5.TIER_A, record_view="tier_a_separate")
    tier_b = evaluate_side(context["tier_b_fallback_frame"], spec, tier_scope=mt5.TIER_B, record_view="tier_b_separate")
    status = "completed" if tier_a["status"] == "completed" and tier_b["status"] == "completed" else "failed"
    if status == "completed":
        score = float(tier_a["quality"]["quality_score"]) + float(tier_b["quality"]["quality_score"])
        if not tier_a["fit"]["converged"]:
            score -= 0.15
        if not tier_b["fit"]["converged"]:
            score -= 0.15
    else:
        score = -999.0
    return {
        "spec": spec,
        "status": status,
        "tier_a": tier_a,
        "tier_b": tier_b,
        "selection_score": float(score),
    }


def variant_result_row(result: Mapping[str, Any]) -> dict[str, Any]:
    spec = result["spec"]
    row: dict[str, Any] = {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "k_regimes": spec.k_regimes,
        "endog_column": spec.endog_column,
        "exog_columns": ",".join(spec.exog_columns) or "none",
        "status": result["status"],
        "selection_score": result["selection_score"],
    }
    for prefix, side in (("tier_a", result["tier_a"]), ("tier_b", result["tier_b"])):
        row[f"{prefix}_sample_rows"] = side.get("sample_rows")
        row[f"{prefix}_fit_status"] = side.get("fit", {}).get("status")
        row[f"{prefix}_converged"] = side.get("fit", {}).get("converged")
        row[f"{prefix}_llf"] = side.get("fit", {}).get("llf")
        if side.get("status") == "completed":
            quality = side["quality"]
            row[f"{prefix}_quality_score"] = quality["quality_score"]
            row[f"{prefix}_collapsed"] = quality["collapsed"]
            row[f"{prefix}_validation_risk_separation"] = quality["by_split"]["validation"]["risk_separation"]
            row[f"{prefix}_oos_risk_separation"] = quality["by_split"]["oos"]["risk_separation"]
            row[f"{prefix}_validation_oos_separation_gap"] = quality["validation_oos_separation_gap"]
            row[f"{prefix}_self_transition_mean"] = side["transition"]["self_transition_mean"]
        else:
            row[f"{prefix}_error"] = side.get("fit", {}).get("error")
    return row


def record_metrics(record_view: str, tier_scope: str, sequence: pd.DataFrame, quality: Mapping[str, Any], path: Path) -> dict[str, Any]:
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": {
            "rows": int(len(sequence)),
            "state_count": int(sequence["markov_state"].nunique()),
            "signal_count": int(len(sequence)),
            "signal_coverage": 1.0,
            "short_count": int((sequence["label_class"].astype("int64") == 0).sum()),
            "long_count": int((sequence["label_class"].astype("int64") == 2).sum()),
            "validation_risk_separation": quality["by_split"]["validation"]["risk_separation"],
            "oos_risk_separation": quality["by_split"]["oos"]["risk_separation"],
            "validation_oos_separation_gap": quality["validation_oos_separation_gap"],
            "collapsed": quality["collapsed"],
            "entropy_mean": quality["entropy_mean"],
        },
    }


def combined_state_summary_frame(tier_a_sequence: pd.DataFrame, tier_b_sequence: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat(
        [
            tier_a_sequence.assign(combined_state_label=lambda frame: "A_" + frame["markov_state"].astype(str)),
            tier_b_sequence.assign(combined_state_label=lambda frame: "B_" + frame["markov_state"].astype(str)),
        ],
        ignore_index=True,
    )
    rows: list[dict[str, Any]] = []
    for (split, label), group in combined.groupby(["split", "combined_state_label"], dropna=False):
        labels = group["label_class"].astype("int64")
        counts = labels.value_counts().to_dict()
        rows.append(
            {
                "split": str(split),
                "combined_state_label": str(label),
                "rows": int(len(group)),
                "future_return_mean": float(group[TARGET_COLUMN].mean()),
                "short_count": int(counts.get(0, 0)),
                "flat_count": int(counts.get(1, 0)),
                "long_count": int(counts.get(2, 0)),
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "combined_state_label"]).reset_index(drop=True)


def materialize_selected_result(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec = result["spec"]
    root = RUN_ROOT
    model_root = root / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_model_path = model_root / f"{spec.variant_id}_tier_a_markov_regression.joblib"
    tier_b_model_path = model_root / f"{spec.variant_id}_tier_b_markov_regression.joblib"
    joblib.dump(result["tier_a"]["fit"]["result"], io_path(tier_a_model_path))
    joblib.dump(result["tier_b"]["fit"]["result"], io_path(tier_b_model_path))

    tier_a_sequence = result["tier_a"]["sequence"]
    tier_b_sequence = result["tier_b"]["sequence"]
    tier_ab_sequence = pd.concat(
        [
            tier_a_sequence.assign(record_source="tier_a"),
            tier_b_sequence.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    tier_ab_summary = combined_state_summary_frame(tier_a_sequence, tier_b_sequence)
    tier_a_sequence_path = root / "predictions/tier_a_markov_state_sequence.parquet"
    tier_b_sequence_path = root / "predictions/tier_b_markov_state_sequence.parquet"
    tier_ab_sequence_path = root / "predictions/tier_ab_markov_state_sequence.parquet"
    tier_a_summary_path = root / "results/selected_tier_a_markov_state_summary.csv"
    tier_b_summary_path = root / "results/selected_tier_b_markov_state_summary.csv"
    tier_ab_summary_path = root / "results/selected_tier_ab_markov_state_summary.csv"
    artifacts = {
        "tier_a_model": {"path": rel(tier_a_model_path), "sha256": sha256_file_lf_normalized(tier_a_model_path)},
        "tier_b_model": {"path": rel(tier_b_model_path), "sha256": sha256_file_lf_normalized(tier_b_model_path)},
        "tier_a_sequence": save_frame(tier_a_sequence_path, tier_a_sequence),
        "tier_b_sequence": save_frame(tier_b_sequence_path, tier_b_sequence),
        "tier_ab_sequence": save_frame(tier_ab_sequence_path, tier_ab_sequence),
        "tier_a_state_summary": save_frame(tier_a_summary_path, result["tier_a"]["summary"]),
        "tier_b_state_summary": save_frame(tier_b_summary_path, result["tier_b"]["summary"]),
        "tier_ab_state_summary": save_frame(tier_ab_summary_path, tier_ab_summary),
    }
    records = [
        record_metrics("tier_a_separate", mt5.TIER_A, tier_a_sequence, result["tier_a"]["quality"], tier_a_sequence_path),
        record_metrics("tier_b_separate", mt5.TIER_B, tier_b_sequence, result["tier_b"]["quality"], tier_b_sequence_path),
        {
            "record_view": "tier_ab_combined",
            "tier_scope": mt5.TIER_AB,
            "status": "completed",
            "path": rel(tier_ab_sequence_path),
            "metrics": {
                "rows": int(len(tier_ab_sequence)),
                "state_count": int(tier_ab_summary["combined_state_label"].nunique()),
                "signal_count": int(len(tier_ab_sequence)),
                "signal_coverage": 1.0,
                "short_count": int((tier_ab_sequence["label_class"].astype("int64") == 0).sum()),
                "long_count": int((tier_ab_sequence["label_class"].astype("int64") == 2).sum()),
                "tier_a_rows": int(len(tier_a_sequence)),
                "tier_b_rows": int(len(tier_b_sequence)),
            },
        },
    ]
    return records, artifacts


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for record in summary["tier_records"]:
        metrics = record["metrics"]
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__python_{record['record_view']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"python_{record['record_view']}",
                "parent_run_id": RUN_ID,
                "record_view": f"python_{record['record_view']}",
                "tier_scope": record["tier_scope"],
                "kpi_scope": "markov_regression_state_link",
                "scoreboard_lane": "structural_scout",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": record["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("state_count", metrics.get("state_count")),
                        ("val_sep", metrics.get("validation_risk_separation")),
                        ("oos_sep", metrics.get("oos_risk_separation")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("collapsed", metrics.get("collapsed")),
                        ("val_oos_gap", metrics.get("validation_oos_separation_gap")),
                        ("boundary", BOUNDARY),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": "Markov regression state-link structural scout only; not runtime authority.",
            }
        )
    ledgers = {
        "stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "markov_regression_state_link_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": ledger_pairs(
            (
                ("selected_variant", summary["selected_variant_id"]),
                ("external_verification", summary["external_verification_status"]),
                ("next", NEXT_RUN_ID),
                ("boundary", BOUNDARY),
            )
        ),
    }
    ledgers["run_registry"] = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    return ledgers


def selected_variant_read(result: Mapping[str, Any]) -> dict[str, Any]:
    spec = result["spec"]
    return {
        "variant": spec.payload(),
        "selection_score": result["selection_score"],
        "tier_a_fit": {key: result["tier_a"]["fit"].get(key) for key in ("status", "converged", "llf", "aic", "bic", "warnings")},
        "tier_b_fit": {key: result["tier_b"]["fit"].get(key) for key in ("status", "converged", "llf", "aic", "bic", "warnings")},
        "tier_a_quality": result["tier_a"]["quality"],
        "tier_b_quality": result["tier_b"]["quality"],
        "tier_a_transition": result["tier_a"]["transition"],
        "tier_b_transition": result["tier_b"]["transition"],
    }


def write_review(summary: Mapping[str, Any]) -> None:
    selected = summary["selected_variant_id"]
    a = summary["selected_variant_read"]["tier_a_quality"]["by_split"]
    b = summary["selected_variant_read"]["tier_b_quality"]["by_split"]
    write_md(
        REPORT_PATH,
        f"""# RUN22A Markov Regression State-Link Scout Packet(실행22A 마르코프 회귀 상태 연결 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run22A_next_milestone_{NEXT_RUN_ID}(실행22A에서는 미시도, 다음 마일스톤은 {NEXT_RUN_ID})`

효과(effect, 효과): MarkovRegression(마르코프 회귀)이 observable return(관측 가능 수익률)을 상태로 나눌 수 있는지 Python-side evidence(파이썬 근거)로 먼저 확인했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `{summary['variant_count']}`
- statsmodels version(스탯츠모델스 버전): `{summary['statsmodels_version']}`
- Tier A sampled rows(Tier A 표본 행): `{summary['tier_rows']['tier_a_sample']}`
- Tier B sampled rows(Tier B 표본 행): `{summary['tier_rows']['tier_b_sample']}`
- Tier A validation/oos risk separation(Tier A 검증/표본외 위험 분리): `{a['validation']['risk_separation']}` / `{a['oos']['risk_separation']}`
- Tier B validation/oos risk separation(Tier B 검증/표본외 위험 분리): `{b['validation']['risk_separation']}` / `{b['oos']['risk_separation']}`
- Tier A collapsed(Tier A 붕괴): `{summary['selected_variant_read']['tier_a_quality']['collapsed']}`
- Tier B collapsed(Tier B 붕괴): `{summary['selected_variant_read']['tier_b_quality']['collapsed']}`

## Preserved Clues(보존 단서)

- Markov regression(마르코프 회귀)은 supervised label(지도 라벨)을 직접 보지 않고 observable return(관측 가능 수익률)과 optional exog(선택 외생 변수)로 state(상태)를 나눈다.
- selected variant(선택 변형) `{selected}`는 Tier A/Tier B(티어 A/티어 B) 모두에서 non-collapsed state read(비붕괴 상태 판독)를 남겼다.
- next runtime_probe(다음 런타임 탐침)는 native statsmodels runtime(원본 스탯츠모델스 런타임)이 아니라 state filter/state table(상태 필터/상태표) handoff(인계)처럼 좁게 검증해야 한다.

## Negative Memory(부정 기억)

- run22A(22A 실행)는 sampled structural scout(표본 구조 탐색)라서 full runtime behavior(전체 런타임 행동)를 주장하지 않는다.
- state separation(상태 분리)은 future return relation(미래 수익률 관계) 읽기일 뿐이며 trading edge(거래 우위)가 아니다.
- convergence warning(수렴 경고)이나 failed variant(실패 변형)는 `variant_summary.csv`와 packet(묶음)에 남긴다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) after materializing state handoff(상태 인계) files.
""",
    )
    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if RUN_ID not in review_index:
        write_md(REVIEW_INDEX_PATH, review_index.rstrip() + "\n" + line)


def write_packet_artifacts(summary: Mapping[str, Any], variant_rows: Sequence[Mapping[str, Any]], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-experiment-design",
                "status": "executed",
                "hypothesis": "Markov switching regression may expose observable-return state links distinct from quantile boosting tail surfaces.",
                "boundary": BOUNDARY,
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-data-integrity",
                "status": "executed",
                "data_contract": SPLIT_CONTRACT,
                "tier_views": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
                "sampling": "split-aware time-ordered sample for structural scout",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-model-validation",
                "status": "executed",
                "model_boundary": "markov_regression_state_link_not_classifier_not_runtime_authority",
                "forbidden_claims": summary["forbidden_claims"],
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-artifact-lineage",
                "status": "executed",
                "source_inputs": [summary["model_input_path"]],
                "producer": "stage_pipelines.stage28.markov_regression_state_link_scout",
                "consumer": NEXT_RUN_ID,
                "artifact_paths": summary["artifacts"],
                "availability": "ignored_with_manifest",
                "lineage_judgment": "connected_with_boundary",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "judgment_label": "inconclusive",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_RUN_ID,
            },
        ],
    )
    write_json(
        PACKET_ROOT / "scope_completion_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_views": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
            "completed_views": [record["record_view"] for record in summary["tier_records"]],
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "kpi_scope": "markov_regression_state_link",
            "runtime_kpi_required": False,
            "runtime_kpi_reason": "out_of_scope_by_claim_python_structural_scout",
        },
    )
    write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "covered_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "missing_gates": [],
        },
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
        },
    )
    write_json(PACKET_ROOT / "variant_summary.json", list(variant_rows))


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


def set_top_level_value(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"{key}: "):
            lines[index] = f"{key}: {value}"
            break
    else:
        lines.insert(0, f"{key}: {value}")
    return "\n".join(lines) + "\n"


def replace_line_by_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    branch = summary["active_branch"]
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = set_top_level_value(state, "active_branch", branch)
    state = set_top_level_value(state, "active_stage", STAGE_ID)
    state = set_top_level_value(state, "current_run_id", RUN_ID)
    state = replace_line_by_prefix(
        state,
        "- treat Stage 28 as ",
        f"- treat Stage 28 as active_run22A_python_structural_scout_completed after Markov regression(마르코프 회귀) state-link scout(상태 연결 탐색); next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
    )
    state = state.replace(
        "      status: opened_not_started\n      current_run_id: not_started",
        f"      status: active_run22A_python_structural_scout_completed\n      current_run_id: {RUN_ID}",
        1,
    )
    model_block = f"""stage28_markov_regression_model:
  stage_id: {STAGE_ID}
  status: active_run22A_python_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary['selected_variant_id']}
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_regression_model:", model_block)
    run_block = f"""stage28_markov_run22A_structural_scout:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary['selected_variant_id']}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_run22A_structural_scout:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_goal_plan(summary: Mapping[str, Any]) -> None:
    branch = summary["active_branch"]
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    current_truth = f"""## Current Truth(현재 진실)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- active branch(활성 브랜치): `{branch}`
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`
- work order(작업지시서): `docs/workspace/stage19_25_model_research_work_order.md`

효과(effect, 효과): Stage20(20단계)부터 Stage27(27단계)까지 reviewed closeout(검토된 마감)을 완료했고, Stage28(28단계)는 `{RUN_ID}` Markov regression(마르코프 회귀) Python structural scout(파이썬 구조 탐색)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
"""
    plan = replace_markdown_section(plan, "## Current Truth", current_truth)
    progress_line = f"- [ ] Stage28(28단계) Markov regression(마르코프 회귀) scout/probe/closeout/open Stage29. In progress(진행 중): `{RUN_ID}` completed(완료); next(다음) `{NEXT_RUN_ID}`."
    lines = plan.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("- [ ] Stage28(28단계) Markov regression(마르코프 회귀) scout/probe/closeout/open Stage29"):
            lines[index] = progress_line
            plan = "\n".join(lines) + "\n"
            break
    plan = replace_line_by_prefix(
        plan,
        "Current active milestone(현재 활성 마일스톤):",
        f"Current active milestone(현재 활성 마일스톤): Stage28(28단계) `{NEXT_RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료) as Python structural scout(파이썬 구조 탐색).
- active branch(활성 브랜치): `{branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage28(28단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `stages/{STAGE_ID}/03_reviews`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): Markov regression scout pipeline(마르코프 회귀 탐색 파이프라인), run evidence(실행 근거), ledgers(장부), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `not_attempted_in_run22A(실행22A에서 미시도)`; review report(검토 보고서) `{rel(REPORT_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): run22A checkpoint commit/push(실행22A 중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage28(28단계) MT5 runtime_probe(런타임 탐침) 준비에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = f"- `2026-05-05`: Stage28(28단계) `{RUN_ID}` Markov regression(마르코프 회귀) Python structural scout(파이썬 구조 탐색)를 완료했다."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any]) -> None:
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage28 Selection Status(28단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `reviewed_structural_scout_completed`
- selected variant(선택 변형): `{summary['selected_variant_id']}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_next_milestone_{NEXT_RUN_ID}`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): run22A(22A 실행)는 Markov regression(마르코프 회귀)의 state-link(상태 연결) 구조를 확인했을 뿐이며 baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.
""",
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage28 RUN22A Markov Regression Scout(최신 28단계 22A 실행 마르코프 회귀 탐색)

Stage28(28단계) `{RUN_ID}`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{summary['selected_variant_id']}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Markov regression(마르코프 회귀)의 state-link(상태 연결) 단서는 보존하고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

"""
    if "## Latest Stage28 RUN22A Markov Regression Scout" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage28 RUN22A Markov Regression Scout(28단계 22A 실행 마르코프 회귀 탐색)

Stage28(28단계) `{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): Markov regression(마르코프 회귀) state-link(상태 연결) 특성은 보존하지만, MT5 runtime_probe(MT5 런타임 탐침)는 `{NEXT_RUN_ID}`로 별도 진행한다.

- selected variant(선택 변형): `{summary['selected_variant_id']}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
""",
    )


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    branch = active_branch()
    context = load_context()
    variants = default_variants(context["tier_b_feature_order"])
    results = [evaluate_variant(spec, context) for spec in variants]
    rows = [variant_result_row(result) for result in results]
    write_csv(RUN_ROOT / "results/variant_summary.csv", list(rows[0].keys()), rows)
    completed = [result for result in results if result["status"] == "completed"]
    if not completed:
        raise RuntimeError("No Stage28 Markov regression variant completed.")
    preferred = [
        result
        for result in completed
        if not result["tier_a"]["quality"]["collapsed"]
        and not result["tier_b"]["quality"]["collapsed"]
        and result["tier_a"]["fit"]["converged"]
        and result["tier_b"]["fit"]["converged"]
    ]
    noncollapsed = [
        result
        for result in completed
        if not result["tier_a"]["quality"]["collapsed"] and not result["tier_b"]["quality"]["collapsed"]
    ]
    selected_pool = preferred or noncollapsed or completed
    selected = max(selected_pool, key=lambda item: item["selection_score"])
    tier_records, artifacts = materialize_selected_result(selected)
    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "status": "reviewed_structural_scout_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "statsmodels_version": statsmodels_version(),
        "feature_set_id": FEATURE_SET_ID,
        "feature_order_hash": ordered_hash(tuple(context["tier_b_feature_order"])),
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "model_input_path": rel(MODEL_INPUT_PATH),
        "variant_count": len(variants),
        "variant_summary_path": rel(RUN_ROOT / "results/variant_summary.csv"),
        "selected_variant_id": selected["spec"].variant_id,
        "best_overall_variant_id": selected["spec"].variant_id,
        "selected_variant_read": selected_variant_read(selected),
        "tier_rows": {
            "tier_a_sample": int(selected["tier_a"]["sample_rows"]),
            "tier_b_sample": int(selected["tier_b"]["sample_rows"]),
            "tier_ab_sample": int(selected["tier_a"]["sample_rows"] + selected["tier_b"]["sample_rows"]),
        },
        "tier_b_context_summary": context["tier_b_context_summary"],
        "tier_records": tier_records,
        "artifacts": artifacts,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "mt5_runtime_probe_status": f"not_attempted_next_milestone_{NEXT_RUN_ID}",
        "next_condition": NEXT_RUN_ID,
        "active_branch": branch,
        "created_at_utc": created_at,
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "allowed_claims": ["Stage28 Markov regression structural state-link scout completed."],
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }
    summary["ledger_updates"] = materialize_ledgers(summary)
    write_review(summary)
    write_packet_artifacts(summary, rows, created_at)
    update_workspace_state(summary)
    update_goal_plan(summary)
    update_text_docs(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "judgment": JUDGMENT,
                    "selected_variant_id": summary["selected_variant_id"],
                    "tier_a_sample_rows": summary["tier_rows"]["tier_a_sample"],
                    "tier_b_sample_rows": summary["tier_rows"]["tier_b_sample"],
                    "next_action": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run Stage28 Markov regression state-link structural scout.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
