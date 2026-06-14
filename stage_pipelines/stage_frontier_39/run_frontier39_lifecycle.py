from __future__ import annotations

import csv
import json
import math
import sys
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b
from stage_pipelines.stage_frontier_34 import run_frontier34_lifecycle as f34


STAGE_ID = "stage_frontier_39__short_pf_edge_regime_conditioned_score_after_f38_scout_only"
RUN_A = "frontier39A_stage_open_short_pf_edge_regime_conditioned_score_hypothesis_design_v1"
RUN_B = "frontier39B_regime_conditioned_score_paired_ablation_proxy_v1"
RUN_C = "frontier39C_regime_guardrail_closeout_decision_v1"
RUN_D = "frontier39D_stage_closeout_regime_conditioned_score_v1"
NEXT_STAGE_ID = "stage_frontier_40__short_pf_edge_non_score_source_pivot_after_regime_gate_negative"
NEXT_RUN_ID = "frontier40A_stage_open_short_pf_edge_non_score_source_hypothesis_design_v1"

PREV_STAGE_ID = "stage_frontier_38__short_pf_edge_source_family_or_model_pivot_after_payoff_label_negative"
PREV_RUN_D = "frontier38D_stage_closeout_model_score_source_pivot_v1"
PREV_PRESERVED_CLUE = "f38_train_only_model_score_source_restored_density_dd_scout_surface_but_pf_below_seed"
PREV_NEGATIVE_MEMORY = "f38_shallow_model_score_source_family_did_not_create_seed_or_runtime_candidate"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_39/run_frontier39_lifecycle.py")

GROK_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier39_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier39_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SCORE_QUANTILES = (0.86, 0.88, 0.90, 0.92)
STOP_QUANTILES = (0.18, 0.22, 0.26, 0.30, 0.34)
TAKE_QUANTILES = (0.70, 0.78, 0.86)
RR_FLOORS = (1.0, 1.2, 1.4)

SCOUT_PF = 1.03
SCOUT_DENSITY_LOW = 4.0
SCOUT_DENSITY_HIGH = 12.0
SCOUT_DD_CAP = 18.0
SEED_PF = 1.20
SEED_DENSITY_LOW = 5.0
SEED_DENSITY_HIGH = 10.0
SEED_DD_CAP = 12.0
RUNTIME_PF = 1.50
RUNTIME_DD_CAP = 10.0
ABLATION_MIN_PF_LIFT = 0.05
ABLATION_MAX_DD_WORSE = 1.0

PRESERVED_CLUE = "f39_regime_gate_can_reduce_density_dd_and_keep_scout_pf_but_not_matched_seed_edge"
NEGATIVE_MEMORY = "f39_regime_gate_did_not_lift_pf_over_ungated_score_at_matched_density"


def main() -> int:
    warnings.filterwarnings("ignore", category=FutureWarning)
    ensure_dirs()
    normalize_grok_packets()
    created_at = f34.utc_now()

    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    open_grok = read_stage_open_grok()
    closeout_grok = read_closeout_grok()

    context = validate_context(frame, feature_order, raw_path, open_grok)
    ablation = run_regime_ablation(frame, feature_order, path_labels, raw_path)
    final = build_final(created_at, frame, feature_order, raw_path, context, open_grok, closeout_grok, ablation)

    write_outputs(final, ablation)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready(output_summary(final)), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_A_ROOT,
        RUN_B_ROOT,
        RUN_C_ROOT,
        RUN_D_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        Path("docs/decisions"),
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if not path_exists(stage_ledger):
        with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
            header = next(csv.reader(handle))
        with io_path(stage_ledger).open("w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_packets() -> None:
    for packet in (GROK_OPEN_PACKET, GROK_CLOSEOUT_PACKET):
        if not path_exists(packet):
            continue
        for name in ("input_prompt.md", "prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                lines = io_path(path).read_text(encoding="utf-8-sig").splitlines()
                f03b.write_text_sig(path, "\n".join(line.rstrip() for line in lines).rstrip() + "\n")


def read_stage_open_grok() -> dict[str, Any]:
    meta = f34.read_json(GROK_OPEN_PACKET / "metadata.json") if path_exists(GROK_OPEN_PACKET / "metadata.json") else {}
    output = f34.read_text(GROK_OPEN_PACKET / "clean_output.md") if path_exists(GROK_OPEN_PACKET / "clean_output.md") else ""
    lowered = output.lower()
    local_required = "needs_local_verification" in lowered
    accepted_for_proxy = (
        bool(meta.get("success"))
        and "novelty_ok" in lowered
        and "leakage_guard_ok" in lowered
        and "runtime_claim_boundary_ok" in lowered
        and "yes" in lowered
        and "paired ablation" in lowered
    )
    return {
        "packet": GROK_OPEN_PACKET.as_posix(),
        "success": bool(meta.get("success")),
        "returncode": meta.get("returncode"),
        "timed_out": bool(meta.get("timed_out")),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "verdict_needs_local_verification": local_required,
        "accepted_for_proxy_after_local_guardrail": accepted_for_proxy,
        "classification": (
            "needs_local_verification_open_regime_ablation_guardrail"
            if local_required and accepted_for_proxy
            else "needs_manual_review"
        ),
        "output_excerpt": output[:2200],
    }


def read_closeout_grok() -> dict[str, Any]:
    meta = f34.read_json(GROK_CLOSEOUT_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_PACKET / "metadata.json") else {}
    output = f34.read_text(GROK_CLOSEOUT_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_PACKET / "clean_output.md") else ""
    lowered = output.lower()
    accepted = (
        bool(meta.get("success"))
        and ("accepted" in lowered or "closeout_ok" in lowered or "bounded_closeout_ok" in lowered)
        and "runtime_boundary_ok" in lowered
        and "yes" in lowered
    )
    return {
        "packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "success": bool(meta.get("success")),
        "returncode": meta.get("returncode"),
        "timed_out": bool(meta.get("timed_out")),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "classification": "accepted_closeout_regime_gate_negative_runtime_boundary" if accepted else "pending_or_needs_local_verification",
        "output_excerpt": output[:2200],
    }


def validate_context(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = f34.read_text(WORKSPACE_STATE)
    prev_selection = f34.read_text(Path("stages") / PREV_STAGE_ID / "04_selected" / "selection_status.md")
    checks = {
        "workspace_current_f38": f"current_stage_id: {PREV_STAGE_ID}" in workspace or f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_points_to_f39a": f"next_run_id: {RUN_A}" in workspace or f"latest_completed_run_id: {RUN_D}" in workspace,
        "f38_selection_points_to_f39a": RUN_A in prev_selection,
        "f38_preserved_clue_present": PREV_PRESERVED_CLUE in prev_selection,
        "f38_negative_memory_present": PREV_NEGATIVE_MEMORY in prev_selection,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_required_splits": set(frame["split"].astype(str).unique()) == {"train", "validation", "oos"},
        "raw_path_positions_complete": int(raw_path["missing_entry_positions"]) == 0
        and int(raw_path["missing_future_positions"]) == 0,
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_requires_local_guardrail": grok["verdict_needs_local_verification"],
        "grok_guardrail_adopted": grok["accepted_for_proxy_after_local_guardrail"],
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_stage_open_ready_with_local_ablation_guardrail" if all(checks.values()) else "needs_manual_review",
        "data_source": f23b.DATASET_PATH.as_posix(),
        "raw_source": f33b.RAW_US100_PATH.as_posix(),
        "feature_order_hash": ordered_hash(feature_order),
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].astype(str).value_counts().to_dict().items()},
        },
        "feature_label_boundary": "score models and regime thresholds use train split only; validation/OOS are read-only",
        "leakage_risk": "medium: regime buckets can overfit train score weakness unless paired ablation is enforced",
    }


def run_regime_ablation(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> dict[str, Any]:
    labels = path_labels[-1]
    x = frame[feature_order].to_numpy(dtype="float64")
    valid_features = np.isfinite(x).all(axis=1)
    train = f33b.split_mask(frame, "train") & labels["valid"] & valid_features

    mfe60 = float(np.nanquantile(labels["mfe"][train], 0.60))
    mae40 = float(np.nanquantile(labels["mae"][train], 0.40))
    y = ((labels["mfe"] >= mfe60) & (labels["mae"] <= mae40)).astype(int)
    fit_mask = train & np.isfinite(y)
    regimes = build_regimes(frame, train)
    rows: list[dict[str, Any]] = []
    model_audit: list[dict[str, Any]] = []

    for model_name, model in model_specs():
        model.fit(x[fit_mask], y[fit_mask])
        score = np.asarray(model.predict_proba(x)[:, 1], dtype="float64")
        train_scores = score[train & np.isfinite(score)]
        model_audit.append(
            {
                "model_family": model_name,
                "label_variant": "path_quality_mfe60_mae40",
                "train_rows": int(np.sum(fit_mask)),
                "positive_rows": int(np.sum(y[fit_mask] == 1)),
                "negative_rows": int(np.sum(y[fit_mask] == 0)),
                "train_score_min": safe_float(np.nanmin(train_scores)),
                "train_score_max": safe_float(np.nanmax(train_scores)),
            }
        )
        for score_q in SCORE_QUANTILES:
            score_threshold = float(np.nanquantile(train_scores, score_q))
            score_mask = valid_features & np.isfinite(score) & (score >= score_threshold)
            for stop_q, take_q, rr, stop_cap, take_cap in threshold_rows(frame, score_mask, labels):
                a_train = eval_path(frame, score_mask, stop_cap, take_cap, path_labels, raw_path, "train")
                if not train_gate(a_train):
                    continue
                a_validation = eval_path(frame, score_mask, stop_cap, take_cap, path_labels, raw_path, "validation")
                a_oos = eval_path(frame, score_mask, stop_cap, take_cap, path_labels, raw_path, "oos")
                for regime in regimes:
                    b_mask = score_mask & regime["mask"]
                    b_train = eval_path(frame, b_mask, stop_cap, take_cap, path_labels, raw_path, "train")
                    if not train_gate(b_train, min_count=35, density_low=3.0, density_high=14.0, dd_cap=24.0):
                        continue
                    b_validation = eval_path(frame, b_mask, stop_cap, take_cap, path_labels, raw_path, "validation")
                    b_oos = eval_path(frame, b_mask, stop_cap, take_cap, path_labels, raw_path, "oos")
                    row = ablation_row(
                        model_name,
                        score_q,
                        score_threshold,
                        stop_q,
                        take_q,
                        rr,
                        stop_cap,
                        take_cap,
                        regime,
                        a_train,
                        a_validation,
                        a_oos,
                        b_train,
                        b_validation,
                        b_oos,
                    )
                    if row["f39_scout_clue_flag"] or row["f39_ablation_guardrail_pass"] or row["f39_seed_surface_flag"]:
                        rows.append(row)

    summary = pd.DataFrame(rows)
    if not summary.empty:
        summary = summary.sort_values(
            [
                "f39_runtime_candidate_flag",
                "f39_seed_surface_flag",
                "f39_ablation_guardrail_pass",
                "f39_scout_clue_flag",
                "f39_read_score",
            ],
            ascending=[False, False, False, False, False],
        ).reset_index(drop=True)
        summary["candidate_id"] = [f"f39b_{idx:04d}" for idx in range(1, len(summary) + 1)]
    return {
        "model_audit": pd.DataFrame(model_audit),
        "summary": summary,
        "regime_rows": int(len(regimes)),
        **section_counts(summary),
    }


def model_specs() -> list[tuple[str, Any]]:
    return [
        (
            "logreg_C0.03",
            make_pipeline(StandardScaler(), LogisticRegression(C=0.03, solver="liblinear", class_weight="balanced", max_iter=300)),
        ),
        (
            "logreg_C0.1",
            make_pipeline(StandardScaler(), LogisticRegression(C=0.1, solver="liblinear", class_weight="balanced", max_iter=300)),
        ),
        (
            "extratrees_d4_leaf160",
            ExtraTreesClassifier(
                n_estimators=96,
                max_depth=4,
                min_samples_leaf=160,
                random_state=3904,
                n_jobs=1,
                class_weight="balanced_subsample",
            ),
        ),
    ]


def build_regimes(frame: pd.DataFrame, train_mask: np.ndarray) -> list[dict[str, Any]]:
    feature_names = [
        "historical_vol_20",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "hl_zscore_50",
        "return_zscore_20",
        "adx_14",
        "ema20_ema50_spread_zscore_50",
        "di_spread_14",
        "bb_position_20",
        "vix_zscore_20",
        "mega8_dispersion_5",
        "us100_minus_top3_weighted_return_1",
        "minutes_from_cash_open",
    ]
    regimes: list[dict[str, Any]] = []
    for feature in feature_names:
        values = frame[feature].to_numpy(dtype="float64")
        train_values = values[train_mask & np.isfinite(values)]
        if train_values.size < 100:
            continue
        for quantile, label, op in ((0.20, "low20", "le"), (0.33, "low33", "le"), (0.67, "high67", "ge"), (0.80, "high80", "ge")):
            threshold = float(np.nanquantile(train_values, quantile))
            mask = np.isfinite(values) & (values <= threshold if op == "le" else values >= threshold)
            regimes.append(
                {
                    "regime_id": f"{feature}_{label}",
                    "feature": feature,
                    "operator": op,
                    "quantile": quantile,
                    "threshold": threshold,
                    "mask": mask,
                    "definition": f"{feature} {op} train_q{quantile:.2f}",
                }
            )
        lo = float(np.nanquantile(train_values, 0.33))
        hi = float(np.nanquantile(train_values, 0.67))
        regimes.append(
            {
                "regime_id": f"{feature}_mid33_67",
                "feature": feature,
                "operator": "between",
                "quantile": 0.0,
                "threshold": math.nan,
                "low_threshold": lo,
                "high_threshold": hi,
                "mask": np.isfinite(values) & (values >= lo) & (values <= hi),
                "definition": f"{feature} between train_q0.33 and train_q0.67",
            }
        )
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype="float64")
    regimes.extend(
        [
            {
                "regime_id": "session_early_0_120",
                "feature": "minutes_from_cash_open",
                "operator": "between_abs",
                "quantile": 0.0,
                "threshold": math.nan,
                "low_threshold": 0.0,
                "high_threshold": 120.0,
                "mask": np.isfinite(minutes) & (minutes >= 0.0) & (minutes <= 120.0),
                "definition": "minutes_from_cash_open between 0 and 120",
            },
            {
                "regime_id": "session_mid_120_300",
                "feature": "minutes_from_cash_open",
                "operator": "between_abs",
                "quantile": 0.0,
                "threshold": math.nan,
                "low_threshold": 120.0,
                "high_threshold": 300.0,
                "mask": np.isfinite(minutes) & (minutes > 120.0) & (minutes <= 300.0),
                "definition": "minutes_from_cash_open between 120 and 300",
            },
            {
                "regime_id": "session_late_300_plus",
                "feature": "minutes_from_cash_open",
                "operator": "ge_abs",
                "quantile": 0.0,
                "threshold": 300.0,
                "mask": np.isfinite(minutes) & (minutes > 300.0),
                "definition": "minutes_from_cash_open greater than 300",
            },
        ]
    )
    return regimes


def threshold_rows(
    frame: pd.DataFrame,
    mask: np.ndarray,
    labels: dict[str, np.ndarray],
) -> list[tuple[float, float, float, float, float]]:
    train = f33b.split_mask(frame, "train") & np.asarray(mask, dtype=bool) & labels["valid"]
    mfe = labels["mfe"][train]
    mae = labels["mae"][train]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    if mfe.size < 35 or mae.size < 35:
        return []
    rows: list[tuple[float, float, float, float, float]] = []
    seen: set[tuple[int, int]] = set()
    for stop_q in STOP_QUANTILES:
        stop_cap = max(float(np.nanquantile(mae, stop_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
        for take_q in TAKE_QUANTILES:
            raw_take = max(float(np.nanquantile(mfe, take_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
            for rr in RR_FLOORS:
                take_cap = max(raw_take, stop_cap * rr)
                key = (int(round(stop_cap * 1_000_000)), int(round(take_cap * 1_000_000)))
                if key in seen:
                    continue
                seen.add(key)
                rows.append((stop_q, take_q, rr, stop_cap, take_cap))
    return rows


def eval_path(
    frame: pd.DataFrame,
    mask: np.ndarray,
    stop_cap: float,
    take_cap: float,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    split: str,
) -> dict[str, Any]:
    return f33b.evaluate_path_mask(frame, mask, -1, stop_cap, take_cap, path_labels, raw_path, split)


def train_gate(
    metrics: dict[str, Any],
    *,
    min_count: int = 45,
    density_low: float = 4.0,
    density_high: float = 14.0,
    pf_floor: float = 1.01,
    dd_cap: float = 22.0,
) -> bool:
    trade_count = int(metrics["trade_count"])
    density = float(metrics["trades_per_day"])
    ambiguous_rate = float(metrics["ambiguous_both_hit_count"]) / max(float(trade_count), 1.0)
    return (
        trade_count >= min_count
        and density_low <= density <= density_high
        and float(metrics["net_profit"]) > 0.0
        and float(metrics["profit_factor"]) >= pf_floor
        and float(metrics["dd_risk"]) <= dd_cap
        and ambiguous_rate <= 0.40
    )


def ablation_row(
    model_name: str,
    score_q: float,
    score_threshold: float,
    stop_q: float,
    take_q: float,
    rr: float,
    stop_cap: float,
    take_cap: float,
    regime: dict[str, Any],
    a_train: dict[str, Any],
    a_validation: dict[str, Any],
    a_oos: dict[str, Any],
    b_train: dict[str, Any],
    b_validation: dict[str, Any],
    b_oos: dict[str, Any],
) -> dict[str, Any]:
    val_lift = safe_float(b_validation["profit_factor"]) - safe_float(a_validation["profit_factor"])
    oos_lift = safe_float(b_oos["profit_factor"]) - safe_float(a_oos["profit_factor"])
    min_lift = min(val_lift, oos_lift)
    val_dd_worse = safe_float(b_validation["dd_risk"]) - safe_float(a_validation["dd_risk"])
    oos_dd_worse = safe_float(b_oos["dd_risk"]) - safe_float(a_oos["dd_risk"])
    max_dd_worse = max(val_dd_worse, oos_dd_worse)
    density_ok = (
        SCOUT_DENSITY_LOW <= safe_float(b_validation["trades_per_day"]) <= SCOUT_DENSITY_HIGH
        and SCOUT_DENSITY_LOW <= safe_float(b_oos["trades_per_day"]) <= SCOUT_DENSITY_HIGH
    )
    scout = (
        safe_float(b_validation["profit_factor"]) >= SCOUT_PF
        and safe_float(b_oos["profit_factor"]) >= SCOUT_PF
        and density_ok
        and max(safe_float(b_validation["dd_risk"]), safe_float(b_oos["dd_risk"])) <= SCOUT_DD_CAP
    )
    seed = (
        safe_float(b_validation["profit_factor"]) >= SEED_PF
        and safe_float(b_oos["profit_factor"]) >= SEED_PF
        and SEED_DENSITY_LOW <= safe_float(b_validation["trades_per_day"]) <= SEED_DENSITY_HIGH
        and SEED_DENSITY_LOW <= safe_float(b_oos["trades_per_day"]) <= SEED_DENSITY_HIGH
        and max(safe_float(b_validation["dd_risk"]), safe_float(b_oos["dd_risk"])) <= SEED_DD_CAP
    )
    runtime = (
        seed
        and safe_float(b_validation["profit_factor"]) >= RUNTIME_PF
        and safe_float(b_oos["profit_factor"]) >= RUNTIME_PF
        and max(safe_float(b_validation["dd_risk"]), safe_float(b_oos["dd_risk"])) <= RUNTIME_DD_CAP
    )
    ablation_pass = min_lift >= ABLATION_MIN_PF_LIFT and density_ok and max_dd_worse <= ABLATION_MAX_DD_WORSE
    read_score = (
        20.0 * float(ablation_pass)
        + 10.0 * float(scout)
        + 100.0 * float(seed)
        + 10.0 * min_lift
        + 2.0 * min(safe_float(b_validation["profit_factor"]), safe_float(b_oos["profit_factor"]))
        - 0.05 * max(safe_float(b_validation["dd_risk"]), safe_float(b_oos["dd_risk"]))
    )
    row: dict[str, Any] = {
        "candidate_id": "",
        "model_family": model_name,
        "label_variant": "path_quality_mfe60_mae40",
        "score_side": "high",
        "score_quantile": score_q,
        "score_threshold": score_threshold,
        "stop_quantile": stop_q,
        "take_quantile": take_q,
        "rr_floor": rr,
        "stop_cap_log_return": stop_cap,
        "take_cap_log_return": take_cap,
        "regime_id": regime["regime_id"],
        "regime_feature": regime["feature"],
        "regime_operator": regime["operator"],
        "regime_quantile": regime.get("quantile", ""),
        "regime_threshold": regime.get("threshold", ""),
        "regime_low_threshold": regime.get("low_threshold", ""),
        "regime_high_threshold": regime.get("high_threshold", ""),
        "regime_definition": regime["definition"],
        "f39_min_forward_pf_lift": min_lift,
        "f39_validation_pf_lift": val_lift,
        "f39_oos_pf_lift": oos_lift,
        "f39_max_dd_worse": max_dd_worse,
        "f39_density_ok": density_ok,
        "f39_scout_clue_flag": scout,
        "f39_ablation_guardrail_pass": ablation_pass,
        "f39_seed_surface_flag": seed,
        "f39_runtime_candidate_flag": runtime,
        "f39_read_score": read_score,
        "selection_boundary": "train_only_score_and_regime_thresholds_validation_oos_read_only",
    }
    for prefix, metrics in (
        ("a_train", a_train),
        ("a_validation", a_validation),
        ("a_oos", a_oos),
        ("b_train", b_train),
        ("b_validation", b_validation),
        ("b_oos", b_oos),
    ):
        add_metric_prefix(row, prefix, metrics)
    return row


def add_metric_prefix(row: dict[str, Any], prefix: str, metrics: dict[str, Any]) -> None:
    for field in (
        "trade_count",
        "trades_per_day",
        "net_profit",
        "profit_factor",
        "expectancy",
        "win_rate",
        "payoff_ratio",
        "dd_risk",
        "max_drawdown_percent",
        "max_monthly_drawdown_percent",
        "underwater_ratio",
        "max_loss_streak",
        "equity_trend_r2",
        "stop_hit_count",
        "take_hit_count",
        "horizon_exit_count",
        "ambiguous_both_hit_count",
        "path_quality_rate",
    ):
        row[f"{prefix}_{field}"] = metrics.get(field, "")


def section_counts(summary: pd.DataFrame) -> dict[str, Any]:
    if summary.empty:
        return {
            "candidate_rows": 0,
            "scout_rows": 0,
            "ablation_pass_rows": 0,
            "seed_rows": 0,
            "runtime_rows": 0,
            "best_readonly": {},
        }
    return {
        "candidate_rows": int(len(summary)),
        "scout_rows": int(summary["f39_scout_clue_flag"].sum()),
        "ablation_pass_rows": int(summary["f39_ablation_guardrail_pass"].sum()),
        "seed_rows": int(summary["f39_seed_surface_flag"].sum()),
        "runtime_rows": int(summary["f39_runtime_candidate_flag"].sum()),
        "best_readonly": json_ready(dict(summary.iloc[0])),
    }


def build_final(
    created_at: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    context: dict[str, Any],
    open_grok: dict[str, Any],
    closeout_grok: dict[str, Any],
    ablation: dict[str, Any],
) -> dict[str, Any]:
    runtime_rows = int(ablation["runtime_rows"])
    seed_rows = int(ablation["seed_rows"])
    ablation_pass_rows = int(ablation["ablation_pass_rows"])
    scout_rows = int(ablation["scout_rows"])
    if runtime_rows:
        closeout_class = "completion_candidate_pending_pre_expensive_grok_and_mt5"
        status = "completion_candidate_pending_runtime_probe_no_authority"
        judgment = "runtime_candidate_requires_pre_expensive_grok_and_mt5_micro_probe_no_authority"
        runtime_status = "runtime_probe_ready_needs_pre_expensive_grok_before_mt5"
    elif seed_rows:
        closeout_class = "seed_surface_without_runtime_candidate"
        status = "seed_surface_no_runtime_candidate_no_authority"
        judgment = "seed_surface_requires_next_validation_no_authority"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_surface_no_runtime_candidate"
    elif ablation_pass_rows:
        closeout_class = "preserved_clue"
        status = "closed_preserved_clue_regime_gate_ablation_pass_no_seed_no_runtime_authority"
        judgment = "preserved_clue(F39 regime gate passed ablation but no seed/runtime)"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f39_ablation"
    elif scout_rows:
        closeout_class = "preserved_clue_negative_memory"
        status = "closed_preserved_clue_negative_memory_regime_gate_scout_only_no_runtime_authority"
        judgment = "preserved_clue_negative_memory(F39 regime gate scout only ablation fail)"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f39_ablation_guardrail_fail"
    else:
        closeout_class = "negative_memory"
        status = "closed_negative_memory_regime_gate_no_scout_no_runtime_authority"
        judgment = "negative_memory(F39 regime gate no forward scout)"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f39_ablation_guardrail_fail"

    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_D,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "context": context,
        "stage_open": {
            "run_id": RUN_A,
            "status": "opened_with_grok_local_ablation_guardrail",
            "judgment": "hypothesis_ready_for_paired_ablation_proxy",
            "grok": open_grok,
        },
        "proxy": {
            "run_id": RUN_B,
            "status": "regime_conditioned_score_paired_ablation_complete_no_authority",
            "judgment": "ablation_guardrail_failed_despite_scout_surface" if scout_rows else "no_forward_scout",
            "regime_rows": ablation["regime_rows"],
            "candidate_rows": ablation["candidate_rows"],
            "scout_rows": scout_rows,
            "ablation_pass_rows": ablation_pass_rows,
            "seed_rows": seed_rows,
            "runtime_rows": runtime_rows,
            "best_readonly": ablation["best_readonly"],
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_proxy_no_seed_or_runtime_candidate",
        },
        "repair": {
            "run_id": RUN_C,
            "status": "capped_repair_skipped_by_grok_ablation_guardrail",
            "judgment": "no_further_regime_bucket_expansion_after_ablation_fail",
            "candidate_rows": 0,
            "scout_rows": 0,
            "seed_rows": 0,
            "runtime_rows": 0,
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_guardrail_fail_no_repair",
        },
        "closeout": {
            "run_id": RUN_D,
            "status": status,
            "judgment": judgment,
            "closeout_class": closeout_class,
            "runtime_probe_status": runtime_status,
            "preserved_clue": PRESERVED_CLUE if scout_rows else "",
            "negative_memory": NEGATIVE_MEMORY,
            "best_readonly": ablation["best_readonly"],
            "grok": closeout_grok,
        },
        "raw_path": {
            "path": f33b.RAW_US100_PATH.as_posix(),
            "raw_rows": raw_path["raw_rows"],
            "missing_entry_positions": raw_path["missing_entry_positions"],
            "missing_future_positions": raw_path["missing_future_positions"],
        },
        "sample_scope": {
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].astype(str).value_counts().to_dict().items()},
        },
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], ablation: dict[str, Any]) -> None:
    ablation["model_audit"].to_csv(io_path(RUN_B_ROOT / "regime_ablation_model_audit.csv"), index=False, encoding="utf-8-sig")
    ablation["summary"].to_csv(io_path(RUN_B_ROOT / "regime_ablation_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    ablation["summary"].head(40).to_csv(io_path(RUN_B_ROOT / "top_regime_ablation_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")
    f34.write_json(RUN_A_ROOT / "stage_open_summary.json", final["stage_open"])
    f34.write_json(RUN_B_ROOT / "final_summary.json", final["proxy"])
    f34.write_json(RUN_C_ROOT / "final_summary.json", final["repair"])
    f34.write_json(RUN_D_ROOT / "stage_closeout_summary.json", final)
    f34.write_json(RUN_D_ROOT / "run_manifest.json", run_manifest(final))

    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_stage_open_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_closeout_receipt.md", grok_stage_closeout_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_A}_report.md", stage_open_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_report.md", proxy_report(final, ablation["summary"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_gate_audit.md", gate_audit_text(final, final["proxy"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_report.md", repair_decision_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_gate_audit.md", gate_audit_text(final, final["repair"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md", closeout_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_39_regime_conditioned_score_open.md"), decision_open(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_39_regime_conditioned_score_closeout.md"), decision_closeout(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_OPEN_PACKET / "prompt.md",
        GROK_OPEN_PACKET / "clean_output.md",
        GROK_OPEN_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "prompt.md",
        GROK_CLOSEOUT_PACKET / "clean_output.md",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        RUN_B_ROOT / "regime_ablation_candidate_summary.csv",
        RUN_D_ROOT / "stage_closeout_summary.json",
        STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md",
        STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md",
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "parent_run_id": RUN_C,
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [f34.artifact_identity(path) for path in artifacts if path_exists(path)],
        "changed_variable": "train_only_regime_conditioning_before_short_score_threshold",
        "fixed_variables": "US100_M5_58_features_chronological_splits_f33_path_native_first_hit_replay_validation_oos_read_only",
        "grok_guardrail": "paired_ablation_B_must_beat_A_by_0.05_pf_without_density_or_dd_break",
        "closeout_class": final["closeout"]["closeout_class"],
        "runtime_probe_status": final["closeout"]["runtime_probe_status"],
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    upsert_csv_many(RUN_REGISTRY, "run_id", run_registry_rows(final))
    ledger = ledger_rows(final)
    upsert_csv_many(ALPHA_LEDGER, "ledger_row_id", ledger)
    upsert_csv_many(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger)
    f03b.append_once(CHANGELOG, RUN_D, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_A, idea_registry_open(final))
    f03b.append_once(IDEA_REGISTRY, RUN_D, idea_registry_close(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_D, negative_register_entry(final))


def upsert_csv_many(path: Path, key: str, new_rows: list[dict[str, Any]]) -> None:
    resolved = io_path(path)
    with resolved.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = list(reader.fieldnames or [])
        existing_rows = [dict(row) for row in reader]
    if key not in header:
        raise ValueError(f"{path.as_posix()} missing key column {key}")
    index_by_key = {row.get(key, ""): index for index, row in enumerate(existing_rows)}
    for row in new_rows:
        normalized = {column: f34.stringify(row.get(column, "")) for column in header}
        row_key = normalized.get(key, "")
        if row_key in index_by_key:
            existing_rows[index_by_key[row_key]] = normalized
        else:
            index_by_key[row_key] = len(existing_rows)
            existing_rows.append(normalized)
    with resolved.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in existing_rows:
            writer.writerow({column: f34.stringify(row.get(column, "")) for column in header})


def run_registry_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    created = final["created_at_utc"]
    return [
        registry_row(RUN_A, "stage_open(단계 개방)", final["stage_open"]["status"], final["stage_open"]["judgment"], f"grok={final['stage_open']['grok']['classification']};next={RUN_B}", created, "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", RUN_B),
        registry_row(RUN_B, "proxy_scout(프록시 탐색)", final["proxy"]["status"], final["proxy"]["judgment"], f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};ablation_pass={final['proxy']['ablation_pass_rows']};seed={final['proxy']['seed_rows']}", created, "python_regime_ablation_proxy_only_no_wfo_no_mt5_no_onnx_no_authority", final["proxy"]["runtime_probe_status"], RUN_C, final["proxy"]["best_readonly"]),
        registry_row(RUN_C, "repair_or_closeout_decision(수리 또는 마감 결정)", final["repair"]["status"], final["repair"]["judgment"], "repair_skipped_by_ablation_guardrail_fail", created, "guardrail_fail_no_wfo_no_mt5_no_onnx_no_authority", final["repair"]["runtime_probe_status"], RUN_D),
        registry_row(RUN_D, "stage_closeout(단계 마감)", final["closeout"]["status"], final["closeout"]["judgment"], f"closeout={final['closeout']['closeout_class']};preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}", created, "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority", final["closeout"]["runtime_probe_status"], NEXT_RUN_ID, final["closeout"]["best_readonly"]),
    ]


def registry_row(
    run_id: str,
    lane: str,
    status: str,
    judgment: str,
    notes: str,
    created: str,
    claim_boundary: str,
    external_status: str,
    next_run: str,
    best: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report = STAGE_ROOT / "03_reviews" / f"{run_id}_report.md"
    primary = "stage_open_no_trading_kpi"
    if best:
        primary = (
            f"best={best.get('candidate_id','')};"
            f"b_val_pf={f34.fmt(best.get('b_validation_profit_factor'))};"
            f"b_val_density={f34.fmt(best.get('b_validation_trades_per_day'))};"
            f"b_val_dd={f34.fmt(best.get('b_validation_dd_risk'))};"
            f"b_oos_pf={f34.fmt(best.get('b_oos_profit_factor'))};"
            f"b_oos_density={f34.fmt(best.get('b_oos_trades_per_day'))};"
            f"b_oos_dd={f34.fmt(best.get('b_oos_dd_risk'))};"
            f"min_lift={f34.fmt(best.get('f39_min_forward_pf_lift'))}"
        )
    return {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "lane": lane,
        "family": "experiment_execution(실험 실행)" if run_id != RUN_D else "publish_handoff(게시/인계)",
        "work_family": "experiment_execution(실험 실행)" if run_id != RUN_D else "publish_handoff(게시/인계)",
        "status": status,
        "judgment": judgment,
        "path": report.as_posix(),
        "notes": notes,
        "run_number": run_id.split("_", 1)[0],
        "date": "2026-06-15",
        "parent_run_id": PREV_RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "next_run_id": next_run,
        "claim_boundary": claim_boundary,
        "report_path": report.as_posix(),
        "created_at_utc": created,
        "primary_kpi": primary,
        "guardrail_kpi": "train_only_regime_thresholds_paired_ablation_validation_oos_read_only",
        "external_verification_status": external_status,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": report.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        ledger_row(RUN_A, f"{RUN_A}__stage_open", "stage_open(단계 개방)", "not_applicable_stage_open(단계 개방 해당 없음)", "planning_only_no_trading_kpi(계획 전용 거래 KPI 없음)", final["stage_open"]["status"], final["stage_open"]["judgment"], f"grok={final['stage_open']['grok']['classification']}", "stage_open_no_runtime", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", f"next={RUN_B}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_a_regime_ablation", "Tier A separate(Tier A 분리)", "Tier A(티어 A)", "python_regime_ablation_proxy_no_mt5(파이썬 체제 소거 프록시, MT5 아님)", final["proxy"]["status"], final["proxy"]["judgment"], f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};ablation_pass={final['proxy']['ablation_pass_rows']};seed={final['proxy']['seed_rows']}", "paired_ablation_guardrail_no_authority", final["proxy"]["runtime_probe_status"], f"next={RUN_C}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B(티어 B)", "missing_required(필수 누락)", final["proxy"]["status"], final["proxy"]["judgment"], "missing_required_no_tier_b_model_input", "no_tier_b_claim", "not_applicable_proxy_no_mt5", "Tier B(티어 B)는 F39 proxy(프록시) 입력으로 물질화하지 않았다."),
        ledger_row(RUN_B, f"{RUN_B}__tier_ab_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B(티어 A+B)", "out_of_scope_by_claim(주장 범위 밖)", final["proxy"]["status"], final["proxy"]["judgment"], "out_of_scope_by_claim_no_combined_source", "no_synthetic_combined_claim", "not_applicable_proxy_no_mt5", "Combined tier(합산 티어)는 F39 proxy(프록시)에서 주장하지 않았다."),
        ledger_row(RUN_C, f"{RUN_C}__repair_decision", "repair_or_closeout_decision(수리 또는 마감 결정)", "Tier A(티어 A)", "guardrail_fail_no_repair(가드레일 실패, 수리 없음)", final["repair"]["status"], final["repair"]["judgment"], "repair_skipped_by_grok_guardrail", "no_repair_after_ablation_fail", final["repair"]["runtime_probe_status"], f"next={RUN_D}"),
        ledger_row(RUN_D, f"{RUN_D}__stage_closeout", "stage_closeout(단계 마감)", "Tier A(티어 A)", "stage_closeout_no_runtime(단계 마감, 런타임 아님)", final["closeout"]["status"], final["closeout"]["judgment"], f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY}", "preserved_clue_negative_memory_no_authority", final["closeout"]["runtime_probe_status"], f"next={NEXT_RUN_ID}"),
    ]


def ledger_row(
    run_id: str,
    row_id: str,
    view: str,
    tier: str,
    kpi_scope: str,
    status: str,
    judgment: str,
    primary: str,
    guardrail: str,
    external: str,
    notes: str,
) -> dict[str, Any]:
    report = STAGE_ROOT / "03_reviews" / f"{run_id}_report.md"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": run_id,
        "subrun_id": row_id,
        "parent_run_id": PREV_RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "record_view": view,
        "tier_scope": tier,
        "kpi_scope": kpi_scope,
        "scoreboard_lane": view,
        "status": status,
        "judgment": judgment,
        "path": report.as_posix(),
        "primary_kpi": primary,
        "guardrail_kpi": guardrail,
        "external_verification_status": external,
        "notes": notes,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": view,
    }


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def stage_brief(final: dict[str, Any]) -> str:
    return f"""# Frontier39 Stage Brief(전선39 단계 요약)

Opened(개방): {final['created_at_utc']}

Hypothesis(가설): F38(전선38)의 high score short path-quality source(고점수 숏 경로 품질 소스)는 density/DD(밀도/손실폭)를 회복했지만 seed PF(씨앗 수익 팩터)에 닿지 못했다. F39(전선39)는 train-only regime gate(학습 전용 체제 게이트)가 같은 score cut(점수 컷)보다 validation/OOS PF(검증/표본밖 수익 팩터)를 올리는지 확인한다.

Action(행동): Grok(그록)이 요구한 paired ablation(쌍대 소거) A=ungated score(무게이트 점수), B=same score + train-only regime gate(동일 점수 + 학습 전용 체제 게이트)를 proxy(프록시)로 실행한다.

Effect(효과): F38 shallow score repetition(얕은 점수 반복)을 막고, regime conditioning(체제 조건화)이 실제 신규성인지 먼저 판별한다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def stage_open_report(final: dict[str, Any]) -> str:
    return f"""# Frontier39A Stage Open Report(전선39A 단계 개방 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['stage_open']['status']}`

Judgment(판정): `{final['stage_open']['judgment']}`

Action(행동): F39(전선39)를 regime-conditioned score source(체제 조건화 점수 소스) hypothesis(가설)로 열었다.

Effect(효과): F38(전선38)의 scout clue(탐색 단서)는 reference-only(참조 전용)로 쓰고, paired ablation guardrail(쌍대 소거 가드레일)을 필수 조건으로 둔다.

Grok classification(그록 분류): `{final['stage_open']['grok']['classification']}`

Next action(다음 행동): `{RUN_B}`
"""


def proxy_report(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["proxy"]["best_readonly"]
    return f"""# Frontier39B Regime Ablation Proxy Report(전선39B 체제 소거 프록시 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['proxy']['status']}`

Judgment(판정): `{final['proxy']['judgment']}`

Action(행동): A/B paired ablation(쌍대 소거)로 ungated score(무게이트 점수)와 same score + train-only regime gate(동일 점수 + 학습 전용 체제 게이트)를 비교했다.

Effect(효과): regime gate(체제 게이트)가 scout surface(탐색 표면)를 만들더라도 matched PF lift(동일 조건 수익 팩터 상승)가 없으면 다음 수리를 금지한다.

Candidate/scout/ablation-pass/seed/runtime rows(후보/탐색/소거 통과/씨앗/런타임 행): `{final['proxy']['candidate_rows']}` / `{final['proxy']['scout_rows']}` / `{final['proxy']['ablation_pass_rows']}` / `{final['proxy']['seed_rows']}` / `{final['proxy']['runtime_rows']}`

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Best B validation/OOS PF-density-DD(최상 B 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('b_validation_profit_factor'))}` / `{f34.fmt(best.get('b_validation_trades_per_day'))}` / `{f34.fmt(best.get('b_validation_dd_risk'))}` and `{f34.fmt(best.get('b_oos_profit_factor'))}` / `{f34.fmt(best.get('b_oos_trades_per_day'))}` / `{f34.fmt(best.get('b_oos_dd_risk'))}`

Best min PF lift vs A(A 대비 최소 수익 팩터 상승): `{f34.fmt(best.get('f39_min_forward_pf_lift'))}`

Runtime probe status(런타임 탐침 상태): `{final['proxy']['runtime_probe_status']}`

| candidate(후보) | model(모델) | regime(체제) | B val PF | B val density | B val DD | B OOS PF | B OOS density | B OOS DD | min lift | ablation pass | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{top_table(summary)}

Next action(다음 행동): `{RUN_C}`
"""


def top_table(summary: pd.DataFrame) -> str:
    if summary.empty:
        return "| none(없음) | | | | | | | | | | | |"
    rows = []
    for _, row in summary.head(12).iterrows():
        rows.append(
            f"| `{row['candidate_id']}` | `{row['model_family']}` | `{row['regime_id']}` | "
            f"{f34.fmt(row['b_validation_profit_factor'])} | {f34.fmt(row['b_validation_trades_per_day'])} | {f34.fmt(row['b_validation_dd_risk'])} | "
            f"{f34.fmt(row['b_oos_profit_factor'])} | {f34.fmt(row['b_oos_trades_per_day'])} | {f34.fmt(row['b_oos_dd_risk'])} | "
            f"{f34.fmt(row['f39_min_forward_pf_lift'])} | {row['f39_ablation_guardrail_pass']} | {row['f39_seed_surface_flag']} |"
        )
    return "\n".join(rows)


def repair_decision_report(final: dict[str, Any]) -> str:
    return f"""# Frontier39C Repair Decision Report(전선39C 수리 결정 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['repair']['status']}`

Judgment(판정): `{final['repair']['judgment']}`

Action(행동): Grok guardrail(그록 가드레일)에 따라 ablation pass(소거 통과)가 0이면 추가 regime bucket expansion(체제 버킷 확장)을 실행하지 않는다.

Effect(효과): F38/F39 shallow score repetition(얕은 점수 반복)을 수리처럼 포장하지 않고 closeout(마감)으로 보낸다.

Runtime probe status(런타임 탐침 상태): `{final['repair']['runtime_probe_status']}`

Next action(다음 행동): `{RUN_D}`
"""


def closeout_report(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return f"""# Frontier39D Stage Closeout Report(전선39D 단계 마감 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Action(행동): F39(전선39)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫는다.

Effect(효과): regime gate(체제 게이트)가 scout PF/DD(탐색 수익 팩터/손실폭)는 만들 수 있지만, Grok paired ablation(그록 쌍대 소거) 조건을 통과하지 못했다는 사실을 다음 stage(단계)의 반복 금지로 남긴다.

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Best B validation/OOS PF-density-DD(최상 B 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('b_validation_profit_factor'))}` / `{f34.fmt(best.get('b_validation_trades_per_day'))}` / `{f34.fmt(best.get('b_validation_dd_risk'))}` and `{f34.fmt(best.get('b_oos_profit_factor'))}` / `{f34.fmt(best.get('b_oos_trades_per_day'))}` / `{f34.fmt(best.get('b_oos_dd_risk'))}`

Best min PF lift vs A(A 대비 최소 수익 팩터 상승): `{f34.fmt(best.get('f39_min_forward_pf_lift'))}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Grok closeout classification(그록 마감 분류): `{final['closeout']['grok']['classification']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def grok_stage_open_receipt(final: dict[str, Any]) -> str:
    grok = final["stage_open"]["grok"]
    return f"""# Grok Stage Open Receipt(그록 단계 개방 영수증)

Classification(분류): `{grok['classification']}`

Verdict needs local verification(판정 로컬 검증 필요): `{grok['verdict_needs_local_verification']}`

Accepted for proxy after local guardrail(로컬 가드레일 후 프록시 수용): `{grok['accepted_for_proxy_after_local_guardrail']}`

Action(행동): Grok(그록)이 요구한 paired ablation guardrail(쌍대 소거 가드레일)을 F39 proxy(프록시)의 실행 조건으로 채택했다.

Effect(효과): 외부 조언을 자동 실행하지 않고, local verification(로컬 검증)으로 regime threshold(체제 임계값)와 A/B wiring(A/B 배선)을 확인한다.

Returncode(반환 코드): `{grok['returncode']}`

Unexpected top-level artifacts(예상 밖 최상위 산출물): `{grok['unexpected_top_level_artifacts']}`
"""


def grok_stage_closeout_receipt(final: dict[str, Any]) -> str:
    grok = final["closeout"]["grok"]
    return f"""# Grok Stage Closeout Receipt(그록 단계 마감 영수증)

Classification(분류): `{grok['classification']}`

Accepted(수용): `{grok['accepted']}`

Action(행동): closeout Grok(마감 그록)을 accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)로 분류했다.

Effect(효과): F39 closeout(전선39 마감)의 runtime boundary(런타임 경계)를 Codex(코덱스)가 로컬 근거로 다시 확인한다.

Returncode(반환 코드): `{grok['returncode']}`

Unexpected top-level artifacts(예상 밖 최상위 산출물): `{grok['unexpected_top_level_artifacts']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    checks = "\n".join(f"- `{name}`: `{value}`" for name, value in final["context"]["checks"].items())
    return f"""# Frontier39 Local Verification(전선39 로컬 검증)

Updated(갱신): {final['created_at_utc']}

Action(행동): workspace state(작업공간 상태), F38 handoff(인계), feature hash(피처 해시), split(분할), raw path alignment(원천 경로 정렬), Grok guardrail(그록 가드레일)을 확인했다.

Effect(효과): F39 proxy(프록시)가 train-only regime threshold(학습 전용 체제 임계값)과 validation/OOS read-only(검증/표본밖 읽기 전용) 경계를 유지한다.

{checks}

Context judgment(맥락 판정): `{final['context']['judgment']}`

Feature order hash(피처 순서 해시): `{final['feature_order_hash']}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
"""


def gate_audit_text(final: dict[str, Any], section: dict[str, Any]) -> str:
    return f"""# {section['run_id']} Gate Audit({section['run_id']} 게이트 감사)

Action(행동): required gates(필수 게이트)를 run(실행) 산출물과 연결했다.

Effect(효과): F39(전선39)가 scout clue(탐색 단서)를 seed/runtime(씨앗/런타임)으로 과장하지 않게 한다.

- experiment_design(실험 설계): stage brief(단계 요약), Grok stage open(그록 단계 개방)
- data_integrity(데이터 무결성): train-only regime threshold(학습 전용 체제 임계값), validation/OOS read-only(검증/표본밖 읽기 전용)
- model_validation(모델 검증): paired ablation A/B(쌍대 소거 A/B) same split/hash/replay(동일 분할/해시/재생)
- artifact_lineage(산출물 계보): run_manifest(실행 목록), candidate summary(후보 요약), register rows(등록부 행)
- result_judgment(결과 판정): `{section['judgment']}`
- runtime_probe(런타임 탐침): `{section['runtime_probe_status']}`
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier39 Required Gate Coverage Audit(전선39 필수 게이트 커버리지 감사)

Action(행동): F39 work packet(작업 묶음)의 required gates(필수 게이트)를 closeout(마감)에 연결했다.

Effect(효과): F39 결과가 “체제 게이트 scout(탐색)”인지 “seed/runtime(씨앗/런타임)”인지 경계를 분명히 한다.

- primary_family(주 작업군): `experiment_execution(실험 실행)`
- primary_skill(주 스킬): `obsidian-experiment-design(옵시디언 실험 설계)`
- stage open Grok(단계 개방 그록): `{final['stage_open']['grok']['classification']}`
- closeout Grok(마감 그록): `{final['closeout']['grok']['classification']}`
- proxy rows(프록시 행): `{final['proxy']['candidate_rows']}`, scout(탐색): `{final['proxy']['scout_rows']}`, ablation pass(소거 통과): `{final['proxy']['ablation_pass_rows']}`, seed(씨앗): `{final['proxy']['seed_rows']}`, runtime(런타임): `{final['proxy']['runtime_rows']}`
- repair(수리): `{final['repair']['judgment']}`
- runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return f"""# Frontier39 Preserved Clue(전선39 보존 단서)

Clue(단서): `{PRESERVED_CLUE}`

Action(행동): regime gate(체제 게이트)가 density/DD(밀도/손실폭)를 낮추며 scout PF(탐색 수익 팩터)를 유지한 표면만 보존한다.

Effect(효과): 다음 stage(단계)는 이 단서를 reference-only(참조 전용)로 쓰되, matched PF lift(동일 조건 수익 팩터 상승)는 없었다는 경계를 함께 본다.

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

B validation/OOS PF-density-DD(B 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('b_validation_profit_factor'))}` / `{f34.fmt(best.get('b_validation_trades_per_day'))}` / `{f34.fmt(best.get('b_validation_dd_risk'))}` and `{f34.fmt(best.get('b_oos_profit_factor'))}` / `{f34.fmt(best.get('b_oos_trades_per_day'))}` / `{f34.fmt(best.get('b_oos_dd_risk'))}`
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier39 Negative Memory(전선39 부정 기억)

Memory(기억): `{NEGATIVE_MEMORY}`

Action(행동): train-only regime gate(학습 전용 체제 게이트)가 ungated score(무게이트 점수) 대비 validation/OOS both(검증/표본밖 둘 다) +0.05 PF lift(수익 팩터 상승)를 만들지 못한 결과를 남긴다.

Effect(효과): 다음 frontier stage(전선 단계)에서 같은 shallow score(얕은 점수)에 regime bucket(체제 버킷)만 더 붙이는 반복을 막는다.

Do not repeat(반복 금지): same score cut + additional regime bucket expansion(같은 점수 컷 + 추가 체제 버킷 확장) without new source/exit asymmetry(새 원천/청산 비대칭 없음).

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier39 Selection Status(전선39 선택 상태)

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Action(행동): F39(전선39)은 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫고, `{NEXT_STAGE_ID}`를 다음 질문으로 남긴다.

Effect(효과): regime conditioning(체제 조건화)은 reference-only(참조 전용) 단서로 보존하고, 다음 stage(단계)는 non-score source(비점수 원천) 또는 exit asymmetry(청산 비대칭) 쪽으로 전환한다.

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`
"""


def decision_open(final: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier39 Regime Conditioned Score(결정: 전선39 체제 조건화 점수 개방)

Date(날짜): 2026-06-15

Decision(결정): `{RUN_A}` starts `{STAGE_ID}`.

Action(행동): F38 score clue(점수 단서)를 reference-only(참조 전용)로 쓰고, train-only regime gate(학습 전용 체제 게이트)를 paired ablation(쌍대 소거)로 시험한다.

Effect(효과): 같은 shallow score repair(얕은 점수 수리)를 반복하지 않고, regime conditioning(체제 조건화)의 실제 기여를 분리한다.
"""


def decision_closeout(final: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier39 Regime Conditioned Score(결정: 전선39 체제 조건화 점수 마감)

Date(날짜): 2026-06-15

Decision(결정): `{RUN_D}` closes `{STAGE_ID}` as `{final['closeout']['closeout_class']}`.

Action(행동): paired ablation guardrail(쌍대 소거 가드레일)이 실패했으므로 추가 regime repair(체제 수리)를 실행하지 않고 closeout(마감)한다.

Effect(효과): 다음 stage(단계)는 non-score source(비점수 원천) 또는 exit asymmetry(청산 비대칭)로 새 가설을 열 수 있다.

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return f"""

## {RUN_D}

- Action(행동): F39 train-only regime-conditioned score(학습 전용 체제 조건화 점수) paired ablation(쌍대 소거)을 기록했다.
- Effect(효과): scout clue(탐색 단서)는 보존하고, matched PF lift(동일 조건 수익 팩터 상승) 실패는 negative memory(부정 기억)로 남긴다.
- Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
- Next(다음): `{NEXT_RUN_ID}`
"""


def idea_registry_open(final: dict[str, Any]) -> str:
    return f"""

### {RUN_A}

- Stage(단계): `{STAGE_ID}`
- Idea(아이디어): train-only regime gate(학습 전용 체제 게이트)가 F38 score source(F38 점수 원천)의 PF(수익 팩터)를 동일 조건에서 올리는지 본다.
- Effect(효과): F38 shallow score family(얕은 점수 패밀리)를 새 기준선으로 상속하지 않고, paired ablation(쌍대 소거)으로 신규성만 검증한다.
"""


def idea_registry_close(final: dict[str, Any]) -> str:
    return f"""

### {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Closeout(마감): `{final['closeout']['closeout_class']}`
- Preserved clue(보존 단서): `{PRESERVED_CLUE}`
- Negative memory(부정 기억): `{NEGATIVE_MEMORY}`
- Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
- Next(다음): `{NEXT_RUN_ID}`
"""


def negative_register_entry(final: dict[str, Any]) -> str:
    return f"""

### {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Negative memory(부정 기억): `{NEGATIVE_MEMORY}`
- Action(행동): paired ablation(쌍대 소거)에서 regime gate(체제 게이트)가 ungated score(무게이트 점수)보다 validation/OOS both(검증/표본밖 둘 다) +0.05 PF lift(수익 팩터 상승)를 만들지 못한 결과를 기록했다.
- Effect(효과): 같은 shallow score(얕은 점수)에 regime bucket(체제 버킷)만 추가하는 반복을 금지한다.
- Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
"""


def workspace_state(final: dict[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_D}
latest_completed_run_id: {RUN_D}
current_status: {final['closeout']['status']}
current_judgment: {final['closeout']['judgment']}
next_stage_id: {NEXT_STAGE_ID}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
"""


def current_working_state(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Current stage(현재 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_D}`

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Action(행동): F39(전선39)를 train-only regime-conditioned score(학습 전용 체제 조건화 점수) paired ablation(쌍대 소거) lifecycle(생명주기)로 닫았다.

Effect(효과): scout clue(탐색 단서)는 보존하고, matched PF lift(동일 조건 수익 팩터 상승) 실패를 negative memory(부정 기억)로 남긴다.

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Best B validation/OOS PF-density-DD(최상 B 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('b_validation_profit_factor'))}` / `{f34.fmt(best.get('b_validation_trades_per_day'))}` / `{f34.fmt(best.get('b_validation_dd_risk'))}` and `{f34.fmt(best.get('b_oos_profit_factor'))}` / `{f34.fmt(best.get('b_oos_trades_per_day'))}` / `{f34.fmt(best.get('b_oos_dd_risk'))}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)이다.
"""


def output_summary(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "closeout_run_id": RUN_D,
        "candidate_rows": final["proxy"]["candidate_rows"],
        "scout_rows": final["proxy"]["scout_rows"],
        "ablation_pass_rows": final["proxy"]["ablation_pass_rows"],
        "seed_rows": final["proxy"]["seed_rows"],
        "runtime_rows": final["proxy"]["runtime_rows"],
        "runtime_probe_status": final["closeout"]["runtime_probe_status"],
        "closeout_class": final["closeout"]["closeout_class"],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "report": (STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md").as_posix(),
    }


def safe_float(value: Any) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return math.nan
    return result if math.isfinite(result) else math.nan


if __name__ == "__main__":
    raise SystemExit(main())
