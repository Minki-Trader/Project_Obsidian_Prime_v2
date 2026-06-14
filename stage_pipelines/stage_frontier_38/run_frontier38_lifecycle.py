from __future__ import annotations

import csv
import json
import math
import sys
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


STAGE_ID = "stage_frontier_38__short_pf_edge_source_family_or_model_pivot_after_payoff_label_negative"
RUN_A = "frontier38A_stage_open_short_pf_edge_source_family_or_model_pivot_hypothesis_design_v1"
RUN_B = "frontier38B_train_only_model_score_source_proxy_scout_v1"
RUN_C = "frontier38C_model_score_quantile_capped_repair_or_closeout_decision_v1"
RUN_D = "frontier38D_stage_closeout_model_score_source_pivot_v1"
NEXT_STAGE_ID = "stage_frontier_39__short_pf_edge_model_score_source_or_regime_pivot_after_f38_scout_only"
NEXT_RUN_ID = "frontier39A_stage_open_short_pf_edge_model_score_or_regime_pivot_hypothesis_design_v1"

PREV_STAGE_ID = "stage_frontier_37__short_pf_edge_label_family_pivot_after_source_utility_scout"
PREV_RUN_D = "frontier37D_stage_closeout_payoff_label_family_pivot_v1"
PREV_NEGATIVE_MEMORY = (
    "f37_train_only_payoff_dominance_and_balanced_label_family_pivot_did_not_create_seed_or_runtime_candidate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_38/run_frontier38_lifecycle.py")

GROK_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier38_stage_open/small_review")
GROK_OPEN_RETRY_PACKET = GROK_OPEN_PACKET / "retry"
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier38_stage_closeout/small_review")
GROK_CLOSEOUT_RETRY_PACKET = GROK_CLOSEOUT_PACKET / "retry"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PROXY_SCORE_QUANTILES = (0.70, 0.80, 0.90, 0.95)
PROXY_STOP_QUANTILES = (0.22, 0.34)
PROXY_TAKE_QUANTILES = (0.62, 0.78)
PROXY_RR_FLOORS = (1.00, 1.40)
REPAIR_SCORE_QUANTILES = (0.86, 0.88, 0.90, 0.92)
REPAIR_STOP_QUANTILES = (0.18, 0.22, 0.26, 0.30, 0.34)
REPAIR_TAKE_QUANTILES = (0.70, 0.78, 0.86)
REPAIR_RR_FLOORS = (1.00, 1.20, 1.40)

SCOUT_PF = 1.02
SCOUT_DENSITY_LOW = 4.0
SCOUT_DENSITY_HIGH = 12.0
SCOUT_DD_CAP = 18.0
NEAR_SEED_PF = 1.12
NEAR_SEED_DD_CAP = 14.0
SEED_PF = 1.20
SEED_DENSITY_LOW = 5.0
SEED_DENSITY_HIGH = 10.0
SEED_DD_CAP = 12.0
RUNTIME_PF = 1.50
RUNTIME_DD_CAP = 10.0

PRESERVED_CLUE = "f38_train_only_model_score_source_restored_density_dd_scout_surface_but_pf_below_seed"
NEGATIVE_MEMORY = "f38_shallow_model_score_source_family_did_not_create_seed_or_runtime_candidate"


def main() -> int:
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
    proxy = build_model_score_proxy(frame, feature_order, path_labels, raw_path)
    repair = build_model_score_repair(frame, feature_order, path_labels, raw_path)
    final = build_final(created_at, frame, feature_order, raw_path, context, open_grok, closeout_grok, proxy, repair)

    write_outputs(final, proxy, repair)
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
    for packet in (GROK_OPEN_PACKET, GROK_OPEN_RETRY_PACKET, GROK_CLOSEOUT_PACKET, GROK_CLOSEOUT_RETRY_PACKET):
        if not path_exists(packet):
            continue
        for name in ("input_prompt.md", "input_prompt_retry.md", "prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                text = io_path(path).read_text(encoding="utf-8-sig").rstrip() + "\n"
                f03b.write_text_sig(path, text)


def read_stage_open_grok() -> dict[str, Any]:
    first_meta = f34.read_json(GROK_OPEN_PACKET / "metadata.json") if path_exists(GROK_OPEN_PACKET / "metadata.json") else {}
    first_output = f34.read_text(GROK_OPEN_PACKET / "clean_output.md") if path_exists(GROK_OPEN_PACKET / "clean_output.md") else ""
    retry_meta = f34.read_json(GROK_OPEN_RETRY_PACKET / "metadata.json") if path_exists(GROK_OPEN_RETRY_PACKET / "metadata.json") else {}
    retry_output = f34.read_text(GROK_OPEN_RETRY_PACKET / "clean_output.md") if path_exists(GROK_OPEN_RETRY_PACKET / "clean_output.md") else ""
    lowered = retry_output.lower()
    accepted = (
        bool(retry_meta.get("success"))
        and ("bounded_exploration_ok" in lowered or "accepted" in lowered)
        and "novelty_ok" in lowered
        and "runtime_claim_boundary_ok" in lowered
        and "yes" in lowered
    )
    return {
        "first_packet": GROK_OPEN_PACKET.as_posix(),
        "first_success": bool(first_meta.get("success")),
        "first_returncode": first_meta.get("returncode"),
        "first_output_excerpt": first_output[:800],
        "retry_packet": GROK_OPEN_RETRY_PACKET.as_posix(),
        "retry_success": bool(retry_meta.get("success")),
        "retry_returncode": retry_meta.get("returncode"),
        "retry_timed_out": bool(retry_meta.get("timed_out")),
        "retry_unexpected_top_level_artifacts": retry_meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "classification": "accepted_stage_open_model_score_source_with_train_only_guard" if accepted else "needs_local_verification",
        "retry_output_excerpt": retry_output[:1600],
    }


def read_closeout_grok() -> dict[str, Any]:
    first_meta = f34.read_json(GROK_CLOSEOUT_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_PACKET / "metadata.json") else {}
    first_output = f34.read_text(GROK_CLOSEOUT_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_PACKET / "clean_output.md") else ""
    retry_meta = f34.read_json(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_RETRY_PACKET / "metadata.json") else {}
    retry_output = f34.read_text(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md") else ""
    effective_meta = retry_meta if retry_meta else first_meta
    effective_output = retry_output if retry_meta else first_output
    lowered = effective_output.lower()
    accepted = (
        bool(effective_meta.get("success"))
        and ("accepted" in lowered or "closeout_ok" in lowered or "bounded_closeout_ok" in lowered)
        and "runtime_boundary_ok" in lowered
        and "yes" in lowered
    )
    return {
        "first_packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "first_success": bool(first_meta.get("success")),
        "first_returncode": first_meta.get("returncode"),
        "first_output_excerpt": first_output[:800],
        "retry_packet": GROK_CLOSEOUT_RETRY_PACKET.as_posix(),
        "retry_success": bool(retry_meta.get("success")),
        "retry_returncode": retry_meta.get("returncode"),
        "retry_timed_out": bool(retry_meta.get("timed_out")),
        "retry_unexpected_top_level_artifacts": retry_meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "classification": "accepted_closeout_model_score_source_negative_runtime_boundary" if accepted else "pending_or_needs_local_verification",
        "retry_output_excerpt": retry_output[:1600],
        "effective_packet": (GROK_CLOSEOUT_RETRY_PACKET if retry_meta else GROK_CLOSEOUT_PACKET).as_posix(),
        "effective_output_excerpt": effective_output[:1600],
    }


def validate_context(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = f34.read_text(WORKSPACE_STATE)
    prev_selection = f34.read_text(Path("stages") / PREV_STAGE_ID / "04_selected" / "selection_status.md")
    prev_closeout = f34.read_text(Path("stages") / PREV_STAGE_ID / "03_reviews" / f"{PREV_RUN_D}_report.md")
    checks = {
        "workspace_current_f37": f"current_stage_id: {PREV_STAGE_ID}" in workspace or f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_points_to_f38a": f"next_run_id: {RUN_A}" in workspace or f"latest_completed_run_id: {RUN_D}" in workspace,
        "f37_selection_points_to_f38a": RUN_A in prev_selection,
        "f37_negative_memory_present": PREV_NEGATIVE_MEMORY in prev_selection or PREV_NEGATIVE_MEMORY in prev_closeout,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_required_splits": set(frame["split"].astype(str).unique()) == {"train", "validation", "oos"},
        "raw_path_positions_complete": int(raw_path["missing_entry_positions"]) == 0
        and int(raw_path["missing_future_positions"]) == 0,
        "grok_retry_transport_success": grok["retry_success"] and grok["retry_returncode"] == 0 and not grok["retry_timed_out"],
        "grok_retry_accepted": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["retry_unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_stage_open_ready_with_retry_grok" if all(checks.values()) else "needs_manual_review",
        "data_source": f23b.DATASET_PATH.as_posix(),
        "raw_source": f33b.RAW_US100_PATH.as_posix(),
        "feature_order_hash": ordered_hash(feature_order),
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].astype(str).value_counts().to_dict().items()},
        },
        "feature_label_boundary": "model targets and score thresholds are fit on train split only; validation/OOS are read-only",
        "leakage_risk": "medium: shallow train-only model source can overfit score shape and recreate F37 payoff dominance indirectly",
    }


def build_model_score_proxy(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> dict[str, Any]:
    return build_model_score_surface(
        frame,
        feature_order,
        path_labels,
        raw_path,
        run_prefix="f38b",
        threshold_source="f38b_train_only_model_score_source_proxy",
        model_specs=proxy_model_specs(),
        label_specs=proxy_label_specs(frame, path_labels[-1]),
        score_quantiles=PROXY_SCORE_QUANTILES,
        stop_quantiles=PROXY_STOP_QUANTILES,
        take_quantiles=PROXY_TAKE_QUANTILES,
        rr_floors=PROXY_RR_FLOORS,
        max_candidates=180,
        train_pf_floor=1.01,
        train_dd_cap=22.0,
    )


def build_model_score_repair(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> dict[str, Any]:
    return build_model_score_surface(
        frame,
        feature_order,
        path_labels,
        raw_path,
        run_prefix="f38c",
        threshold_source="f38c_capped_model_score_quantile_repair",
        model_specs=repair_model_specs(),
        label_specs=repair_label_specs(frame, path_labels[-1]),
        score_quantiles=REPAIR_SCORE_QUANTILES,
        stop_quantiles=REPAIR_STOP_QUANTILES,
        take_quantiles=REPAIR_TAKE_QUANTILES,
        rr_floors=REPAIR_RR_FLOORS,
        max_candidates=180,
        train_pf_floor=1.01,
        train_dd_cap=22.0,
    )


def build_model_score_surface(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    *,
    run_prefix: str,
    threshold_source: str,
    model_specs: list[dict[str, Any]],
    label_specs: list[dict[str, Any]],
    score_quantiles: tuple[float, ...],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    max_candidates: int,
    train_pf_floor: float,
    train_dd_cap: float,
) -> dict[str, Any]:
    x = frame[feature_order].to_numpy(dtype="float64")
    valid_feature_rows = np.isfinite(x).all(axis=1)
    train_mask = f33b.split_mask(frame, "train") & valid_feature_rows & path_labels[-1]["valid"]
    candidates: list[dict[str, Any]] = []
    model_audit_rows: list[dict[str, Any]] = []

    for label_spec in label_specs:
        y = np.asarray(label_spec["target"], dtype=int)
        fit_mask = train_mask & np.isfinite(y)
        positives = int(np.sum(y[fit_mask] == 1))
        negatives = int(np.sum(y[fit_mask] == 0))
        if positives < 80 or negatives < 80:
            model_audit_rows.append({
                "label_variant": label_spec["label_variant"],
                "model_family": "not_fit",
                "status": "skipped_sparse_label",
                "train_rows": int(np.sum(fit_mask)),
                "positive_rows": positives,
                "negative_rows": negatives,
            })
            continue
        for model_spec in model_specs:
            model = model_spec["factory"]()
            model.fit(x[fit_mask], y[fit_mask])
            score = predict_score(model, x)
            finite_score = np.isfinite(score) & valid_feature_rows
            train_scores = score[train_mask & finite_score]
            model_audit_rows.append({
                "label_variant": label_spec["label_variant"],
                "model_family": model_spec["model_family"],
                "status": "fit_train_only",
                "train_rows": int(np.sum(fit_mask)),
                "positive_rows": positives,
                "negative_rows": negatives,
                "train_score_min": safe_float(np.nanmin(train_scores)) if train_scores.size else math.nan,
                "train_score_max": safe_float(np.nanmax(train_scores)) if train_scores.size else math.nan,
            })
            if train_scores.size < 100:
                continue
            for side_name, comparator in (("high", np.greater_equal), ("low", np.less_equal)):
                for score_q in score_quantiles:
                    threshold = float(np.nanquantile(train_scores, score_q))
                    mask = finite_score & comparator(score, threshold)
                    conditions = [condition_stub(label_spec, model_spec, side_name, score_q, threshold)]
                    candidates.extend(
                        candidates_for_mask(
                            frame,
                            conditions,
                            mask,
                            path_labels,
                            raw_path,
                            stop_quantiles,
                            take_quantiles,
                            rr_floors,
                            threshold_source,
                            label_spec,
                            model_spec,
                            side_name,
                            score_q,
                            threshold,
                            train_pf_floor,
                            train_dd_cap,
                        )
                    )

    selected = rank_candidates(candidates, run_prefix, max_candidates)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = add_f38_flags(f33b.summarize_candidates(split_metrics), selected)
    return {
        "model_audit": pd.DataFrame(model_audit_rows),
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "model_rows": int(len(model_audit_rows)),
        **section_counts(summary, selected),
    }


def proxy_model_specs() -> list[dict[str, Any]]:
    return [
        {
            "model_family": "logreg_C0.1",
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.1, solver="liblinear", class_weight="balanced", max_iter=300),
            ),
        },
        {
            "model_family": "logreg_C0.3",
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.3, solver="liblinear", class_weight="balanced", max_iter=300),
            ),
        },
        {
            "model_family": "extratrees_d3_leaf120",
            "factory": lambda: ExtraTreesClassifier(
                n_estimators=96,
                max_depth=3,
                min_samples_leaf=120,
                random_state=3803,
                n_jobs=1,
                class_weight="balanced_subsample",
            ),
        },
        {
            "model_family": "extratrees_d5_leaf120",
            "factory": lambda: ExtraTreesClassifier(
                n_estimators=96,
                max_depth=5,
                min_samples_leaf=120,
                random_state=3805,
                n_jobs=1,
                class_weight="balanced_subsample",
            ),
        },
    ]


def repair_model_specs() -> list[dict[str, Any]]:
    return [
        {
            "model_family": "logreg_C0.03",
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.03, solver="liblinear", class_weight="balanced", max_iter=300),
            ),
        },
        {
            "model_family": "logreg_C0.1",
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.1, solver="liblinear", class_weight="balanced", max_iter=300),
            ),
        },
        {
            "model_family": "logreg_C0.3",
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.3, solver="liblinear", class_weight="balanced", max_iter=300),
            ),
        },
        {
            "model_family": "extratrees_d5_leaf120",
            "factory": lambda: ExtraTreesClassifier(
                n_estimators=96,
                max_depth=5,
                min_samples_leaf=120,
                random_state=3885,
                n_jobs=1,
                class_weight="balanced_subsample",
            ),
        },
    ]


def proxy_label_specs(frame: pd.DataFrame, labels: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    train = f33b.split_mask(frame, "train") & labels["valid"]
    mfe60 = float(np.nanquantile(labels["mfe"][train], 0.60))
    mae40 = float(np.nanquantile(labels["mae"][train], 0.40))
    return [
        {
            "label_variant": "horizon_positive",
            "label_definition": "short horizon pnl greater than zero",
            "target": (labels["horizon_pnl"] > 0.0).astype(int),
        },
        {
            "label_variant": "path_quality_mfe60_mae40",
            "label_definition": "short MFE >= train q60 and short MAE <= train q40",
            "target": ((labels["mfe"] >= mfe60) & (labels["mae"] <= mae40)).astype(int),
        },
    ]


def repair_label_specs(frame: pd.DataFrame, labels: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    train = f33b.split_mask(frame, "train") & labels["valid"]
    mfe60 = float(np.nanquantile(labels["mfe"][train], 0.60))
    mae40 = float(np.nanquantile(labels["mae"][train], 0.40))
    mfe65 = float(np.nanquantile(labels["mfe"][train], 0.65))
    mae45 = float(np.nanquantile(labels["mae"][train], 0.45))
    return [
        {
            "label_variant": "path_quality_mfe60_mae40",
            "label_definition": "short MFE >= train q60 and short MAE <= train q40",
            "target": ((labels["mfe"] >= mfe60) & (labels["mae"] <= mae40)).astype(int),
        },
        {
            "label_variant": "path_quality_mfe65_mae45",
            "label_definition": "short MFE >= train q65 and short MAE <= train q45",
            "target": ((labels["mfe"] >= mfe65) & (labels["mae"] <= mae45)).astype(int),
        },
    ]


def predict_score(model: Any, x: np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(x)
        if isinstance(proba, list):
            proba = proba[0]
        return np.asarray(proba, dtype="float64")[:, 1]
    decision = np.asarray(model.decision_function(x), dtype="float64")
    return 1.0 / (1.0 + np.exp(-decision))


def condition_stub(
    label_spec: dict[str, Any],
    model_spec: dict[str, Any],
    side_name: str,
    score_q: float,
    threshold: float,
) -> dict[str, Any]:
    condition_id = f"{label_spec['label_variant']}__{model_spec['model_family']}__{side_name}_q{score_q:.2f}"
    return {
        "condition_id": condition_id,
        "feature": model_spec["model_family"],
        "feature_family": "train_only_model_score_source",
        "definition": (
            f"{label_spec['label_variant']} {model_spec['model_family']} score "
            f"{side_name} train q{score_q:.2f} threshold {threshold:.6f}"
        ),
    }


def candidates_for_mask(
    frame: pd.DataFrame,
    conditions: list[dict[str, Any]],
    mask: np.ndarray,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    threshold_source: str,
    label_spec: dict[str, Any],
    model_spec: dict[str, Any],
    score_side: str,
    score_quantile: float,
    score_threshold: float,
    train_pf_floor: float,
    train_dd_cap: float,
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    for row in threshold_rows(frame, mask, path_labels[-1], stop_quantiles, take_quantiles, rr_floors, threshold_source):
        metrics = f33b.evaluate_path_mask(
            frame,
            mask,
            -1,
            float(row["stop_cap_log_return"]),
            float(row["take_cap_log_return"]),
            path_labels,
            raw_path,
            "train",
        )
        if not train_gate(metrics, train_pf_floor, train_dd_cap):
            continue
        score = train_edge_score(metrics, score_quantile)
        candidate = f33b.candidate_from_conditions(conditions, mask, -1, row, metrics, score)
        candidate["label_variant"] = label_spec["label_variant"]
        candidate["label_definition"] = label_spec["label_definition"]
        candidate["model_family"] = model_spec["model_family"]
        candidate["score_side"] = score_side
        candidate["score_quantile"] = score_quantile
        candidate["score_threshold"] = score_threshold
        candidate["f38_model_edge_score"] = score
        candidate["threshold_family_id"] = (
            f"{threshold_source}__sq{row['stop_quantile']}_tq{row['take_quantile']}_rr{row['rr_floor']}"
        )
        variants.append(candidate)
    variants.sort(key=lambda item: float(item["f38_model_edge_score"]), reverse=True)
    return variants[:2]


def threshold_rows(
    frame: pd.DataFrame,
    mask: np.ndarray,
    labels: dict[str, np.ndarray],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    threshold_source: str,
) -> list[dict[str, Any]]:
    train = f33b.split_mask(frame, "train") & np.asarray(mask, dtype=bool) & labels["valid"]
    mfe = labels["mfe"][train]
    mae = labels["mae"][train]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    if mfe.size < 35 or mae.size < 35:
        return []
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for stop_q in stop_quantiles:
        stop_cap = max(float(np.nanquantile(mae, stop_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
        for take_q in take_quantiles:
            raw_take = max(float(np.nanquantile(mfe, take_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
            for rr_floor in rr_floors:
                take_cap = max(raw_take, stop_cap * rr_floor)
                key = (int(round(stop_cap * 1_000_000)), int(round(take_cap * 1_000_000)))
                if key in seen:
                    continue
                seen.add(key)
                rows.append(
                    {
                        "threshold_source": threshold_source,
                        "stop_quantile": stop_q,
                        "take_quantile": take_q,
                        "rr_floor": rr_floor,
                        "stop_cap_log_return": stop_cap,
                        "take_cap_log_return": take_cap,
                        "train_threshold_sample_rows": int(min(mfe.size, mae.size)),
                    }
                )
    return rows


def train_gate(metrics: dict[str, Any], pf_floor: float, dd_cap: float) -> bool:
    trade_count = int(metrics["trade_count"])
    density = float(metrics["trades_per_day"])
    ambiguous_rate = float(metrics["ambiguous_both_hit_count"]) / max(float(trade_count), 1.0)
    return (
        trade_count >= 45
        and 4.0 <= density <= 14.0
        and float(metrics["net_profit"]) > 0.0
        and float(metrics["profit_factor"]) >= pf_floor
        and float(metrics["dd_risk"]) <= dd_cap
        and ambiguous_rate <= 0.40
    )


def train_edge_score(metrics: dict[str, Any], score_quantile: float) -> float:
    trade_count = max(safe_float(metrics.get("trade_count")), 1.0)
    density = safe_float(metrics.get("trades_per_day"))
    pf = safe_float(metrics.get("profit_factor"))
    dd = safe_float(metrics.get("dd_risk"))
    payoff = safe_float(metrics.get("payoff_ratio"))
    path_quality = safe_float(metrics.get("path_quality_rate"))
    ambiguous_rate = safe_float(metrics.get("ambiguous_both_hit_count")) / trade_count
    density_bonus = max(0.0, 1.0 - abs(density - 7.5) / 7.5)
    sparsity_penalty = abs(score_quantile - 0.90)
    return float(
        4.8 * min(pf, 4.0)
        + 1.4 * density_bonus
        + 0.6 * min(payoff, 4.0)
        + 1.1 * path_quality
        - 0.25 * max(0.0, dd - 10.0)
        - 1.8 * ambiguous_rate
        - sparsity_penalty
    )


def rank_candidates(candidates: list[dict[str, Any]], prefix: str, limit: int) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str, float, float, float]] = set()
    selected: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: float(item["f38_model_edge_score"]), reverse=True):
        key = (
            str(candidate.get("label_variant", "")),
            str(candidate.get("model_family", "")),
            str(candidate.get("score_side", "")),
            round(float(candidate.get("score_quantile", 0.0)), 4),
            round(float(candidate.get("stop_cap_log_return", 0.0)), 7),
            round(float(candidate.get("take_cap_log_return", 0.0)), 7),
        )
        if key in seen:
            continue
        seen.add(key)
        selected.append(candidate)
        if len(selected) >= limit:
            break
    for index, candidate in enumerate(selected, start=1):
        candidate["candidate_id"] = f"{prefix}_{index:04d}"
    return selected


def add_f38_flags(summary: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    if summary.empty:
        return summary
    metadata = {
        str(item["candidate_id"]): {
            "label_variant": item.get("label_variant", ""),
            "label_definition": item.get("label_definition", ""),
            "model_family": item.get("model_family", ""),
            "score_side": item.get("score_side", ""),
            "score_quantile": item.get("score_quantile", ""),
            "score_threshold": item.get("score_threshold", ""),
            "f38_model_edge_score": item.get("f38_model_edge_score", ""),
            "threshold_family_id": item.get("threshold_family_id", ""),
        }
        for item in candidates
    }
    summary = summary.copy()
    for field in (
        "label_variant",
        "label_definition",
        "model_family",
        "score_side",
        "score_quantile",
        "score_threshold",
        "f38_model_edge_score",
        "threshold_family_id",
    ):
        summary[field] = [metadata.get(str(candidate_id), {}).get(field, "") for candidate_id in summary["candidate_id"]]

    f_min_pf = pd.to_numeric(summary["forward_min_pf"], errors="coerce")
    f_max_dd = pd.to_numeric(summary["forward_max_dd"], errors="coerce")
    f_min_density = pd.to_numeric(summary["forward_min_density"], errors="coerce")
    f_max_density = pd.to_numeric(summary["forward_max_density"], errors="coerce")
    dual = summary["forward_dual_positive_flag"].astype(bool)
    density_scout = (f_min_density >= SCOUT_DENSITY_LOW) & (f_max_density <= SCOUT_DENSITY_HIGH)
    density_seed = (f_min_density >= SEED_DENSITY_LOW) & (f_max_density <= SEED_DENSITY_HIGH)
    summary["f38_scout_clue_flag"] = dual & density_scout & (f_min_pf >= SCOUT_PF) & (f_max_dd <= SCOUT_DD_CAP)
    summary["f38_near_seed_flag"] = dual & density_scout & (f_min_pf >= NEAR_SEED_PF) & (f_max_dd <= NEAR_SEED_DD_CAP)
    summary["f38_seed_surface_flag"] = dual & density_seed & (f_min_pf >= SEED_PF) & (f_max_dd <= SEED_DD_CAP)
    summary["f38_runtime_candidate_flag"] = (
        summary["f38_seed_surface_flag"].astype(bool) & (f_min_pf >= RUNTIME_PF) & (f_max_dd <= RUNTIME_DD_CAP)
    )
    summary["f38_completion_axis_distance"] = (
        np.maximum(0.0, SEED_PF - f_min_pf)
        + np.maximum(0.0, f_max_dd - SEED_DD_CAP) / SEED_DD_CAP
        + np.maximum(0.0, SEED_DENSITY_LOW - f_min_density) / SEED_DENSITY_LOW
        + np.maximum(0.0, f_max_density - SEED_DENSITY_HIGH) / SEED_DENSITY_HIGH
    )
    return summary.sort_values(
        [
            "f38_runtime_candidate_flag",
            "f38_seed_surface_flag",
            "f38_near_seed_flag",
            "f38_scout_clue_flag",
            "path_read_score",
        ],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)


def section_counts(summary: pd.DataFrame, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if summary.empty:
        return {
            "candidate_rows": int(len(candidates)),
            "scout_rows": 0,
            "near_seed_rows": 0,
            "seed_rows": 0,
            "runtime_rows": 0,
            "best_readonly": {},
        }
    return {
        "candidate_rows": int(len(candidates)),
        "scout_rows": int(summary["f38_scout_clue_flag"].sum()),
        "near_seed_rows": int(summary["f38_near_seed_flag"].sum()),
        "seed_rows": int(summary["f38_seed_surface_flag"].sum()),
        "runtime_rows": int(summary["f38_runtime_candidate_flag"].sum()),
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
    proxy: dict[str, Any],
    repair: dict[str, Any],
) -> dict[str, Any]:
    best = repair.get("best_readonly") or proxy.get("best_readonly") or {}
    runtime_rows = int(proxy["runtime_rows"]) + int(repair["runtime_rows"])
    seed_rows = int(proxy["seed_rows"]) + int(repair["seed_rows"])
    scout_rows = int(proxy["scout_rows"]) + int(repair["scout_rows"])
    if runtime_rows:
        closeout_class = "completion_candidate_pending_pre_expensive_grok_and_mt5"
        runtime_status = "runtime_probe_ready_needs_pre_expensive_grok_before_mt5"
        status = "completion_candidate_pending_runtime_probe_no_authority"
        judgment = "runtime_candidate_requires_pre_expensive_grok_and_mt5_micro_probe_no_authority"
    elif seed_rows:
        closeout_class = "preserved_clue_seed_surface_without_runtime_candidate"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_surface_no_runtime_candidate"
        status = "seed_surface_no_runtime_candidate_no_authority"
        judgment = "seed_surface_requires_new_lifecycle_or_runtime_repair_no_authority"
    elif scout_rows:
        closeout_class = "preserved_clue_negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f38c_model_score_repair"
        status = "closed_preserved_clue_negative_memory_model_score_source_scout_only_no_runtime_authority"
        judgment = "preserved_clue_negative_memory(F38 model score source scout only)"
    else:
        closeout_class = "negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f38c_model_score_repair"
        status = "closed_negative_memory_model_score_source_no_scout_no_runtime_authority"
        judgment = "negative_memory(F38 model score source no forward scout)"

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
            "status": "opened_with_bounded_grok_model_score_source_hypothesis",
            "judgment": "hypothesis_ready_for_proxy",
            "grok": open_grok,
        },
        "proxy": {
            "run_id": RUN_B,
            "status": "model_score_source_proxy_scout_complete_no_runtime_authority",
            "judgment": "scout_surface_only_no_seed_runtime" if proxy["scout_rows"] else "no_forward_scout",
            "model_rows": proxy["model_rows"],
            "candidate_rows": proxy["candidate_rows"],
            "scout_rows": proxy["scout_rows"],
            "near_seed_rows": proxy["near_seed_rows"],
            "seed_rows": proxy["seed_rows"],
            "runtime_rows": proxy["runtime_rows"],
            "best_readonly": proxy["best_readonly"],
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_proxy_no_seed_or_runtime_candidate",
        },
        "repair": {
            "run_id": RUN_C,
            "status": "capped_model_score_quantile_repair_complete_no_runtime_authority",
            "judgment": "scout_surface_only_no_seed_runtime" if repair["scout_rows"] else "repair_no_forward_scout",
            "model_rows": repair["model_rows"],
            "candidate_rows": repair["candidate_rows"],
            "scout_rows": repair["scout_rows"],
            "near_seed_rows": repair["near_seed_rows"],
            "seed_rows": repair["seed_rows"],
            "runtime_rows": repair["runtime_rows"],
            "best_readonly": repair["best_readonly"],
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_repair_no_seed_or_runtime_candidate",
        },
        "closeout": {
            "run_id": RUN_D,
            "status": status,
            "judgment": judgment,
            "closeout_class": closeout_class,
            "runtime_probe_status": runtime_status,
            "preserved_clue": PRESERVED_CLUE if scout_rows else "",
            "negative_memory": NEGATIVE_MEMORY,
            "best_readonly": best,
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


def write_outputs(final: dict[str, Any], proxy: dict[str, Any], repair: dict[str, Any]) -> None:
    proxy["model_audit"].to_csv(io_path(RUN_B_ROOT / "model_score_proxy_model_audit.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_candidate_for_csv(item) for item in proxy["candidates"]]).to_csv(
        io_path(RUN_B_ROOT / "model_score_proxy_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    proxy["split_metrics"].to_csv(io_path(RUN_B_ROOT / "model_score_proxy_split_metrics.csv"), index=False, encoding="utf-8-sig")
    proxy["summary"].to_csv(io_path(RUN_B_ROOT / "model_score_proxy_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    proxy["summary"].head(40).to_csv(io_path(RUN_B_ROOT / "top_model_score_proxy_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")

    repair["model_audit"].to_csv(io_path(RUN_C_ROOT / "model_score_repair_model_audit.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_candidate_for_csv(item) for item in repair["candidates"]]).to_csv(
        io_path(RUN_C_ROOT / "model_score_repair_candidate_ledger.csv"), index=False, encoding="utf-8-sig"
    )
    repair["split_metrics"].to_csv(io_path(RUN_C_ROOT / "model_score_repair_split_metrics.csv"), index=False, encoding="utf-8-sig")
    repair["summary"].to_csv(io_path(RUN_C_ROOT / "model_score_repair_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    repair["summary"].head(40).to_csv(io_path(RUN_C_ROOT / "top_model_score_repair_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")

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
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_report.md", run_report(final, final["proxy"], proxy["summary"], RUN_C))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_gate_audit.md", gate_audit_text(final, final["proxy"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_report.md", run_report(final, final["repair"], repair["summary"], RUN_D))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_gate_audit.md", gate_audit_text(final, final["repair"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md", closeout_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_38_model_score_source_open.md"), decision_open(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_38_model_score_source_closeout.md"), decision_closeout(final))


def clean_candidate_for_csv(candidate: dict[str, Any]) -> dict[str, Any]:
    row = f33b.clean_candidate_for_csv(candidate)
    for key in (
        "label_variant",
        "label_definition",
        "model_family",
        "score_side",
        "score_quantile",
        "score_threshold",
        "f38_model_edge_score",
        "threshold_family_id",
    ):
        row[key] = candidate.get(key, "")
    return row


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_OPEN_PACKET / "prompt.md",
        GROK_OPEN_RETRY_PACKET / "clean_output.md",
        GROK_OPEN_RETRY_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "prompt.md",
        GROK_CLOSEOUT_PACKET / "clean_output.md",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        GROK_CLOSEOUT_RETRY_PACKET / "clean_output.md",
        GROK_CLOSEOUT_RETRY_PACKET / "metadata.json",
        RUN_B_ROOT / "model_score_proxy_candidate_summary.csv",
        RUN_C_ROOT / "model_score_repair_candidate_summary.csv",
        RUN_D_ROOT / "stage_closeout_summary.json",
        STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md",
        STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md",
    ]
    artifacts = [path for path in artifacts if path_exists(path)]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "parent_run_id": RUN_C,
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [f34.artifact_identity(path) for path in artifacts],
        "changed_variable": "train_only_model_score_source_family_for_short_path_quality_entry_masks",
        "fixed_variables": "US100_M5_58_features_chronological_splits_f33_path_native_first_hit_replay_validation_oos_read_only",
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
    close = final["closeout"]
    return [
        registry_row(
            RUN_A,
            "stage_open(단계 개방)",
            final["stage_open"]["status"],
            final["stage_open"]["judgment"],
            f"grok={final['stage_open']['grok']['classification']};next={RUN_B};no_authority",
            created,
            "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority",
            "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet",
            RUN_B,
        ),
        registry_row(
            RUN_B,
            "proxy_scout(프록시 탐색)",
            final["proxy"]["status"],
            final["proxy"]["judgment"],
            f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};near_seed={final['proxy']['near_seed_rows']};seed={final['proxy']['seed_rows']}",
            created,
            "python_model_score_proxy_only_no_wfo_no_mt5_no_onnx_no_authority",
            final["proxy"]["runtime_probe_status"],
            RUN_C,
            final["proxy"]["best_readonly"],
        ),
        registry_row(
            RUN_C,
            "repair_or_closeout_decision(수리 또는 마감 결정)",
            final["repair"]["status"],
            final["repair"]["judgment"],
            f"candidate={final['repair']['candidate_rows']};scout={final['repair']['scout_rows']};near_seed={final['repair']['near_seed_rows']};seed={final['repair']['seed_rows']}",
            created,
            "capped_model_score_quantile_repair_no_wfo_no_mt5_no_onnx_no_authority",
            final["repair"]["runtime_probe_status"],
            RUN_D,
            final["repair"]["best_readonly"],
        ),
        registry_row(
            RUN_D,
            "stage_closeout(단계 마감)",
            close["status"],
            close["judgment"],
            f"closeout={close['closeout_class']};preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}",
            created,
            "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority",
            close["runtime_probe_status"],
            NEXT_RUN_ID,
            close["best_readonly"],
        ),
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
            f"val_pf={f34.fmt(best.get('validation_profit_factor'))};"
            f"val_density={f34.fmt(best.get('validation_trades_per_day'))};"
            f"val_dd={f34.fmt(best.get('validation_dd_risk'))};"
            f"oos_pf={f34.fmt(best.get('oos_profit_factor'))};"
            f"oos_density={f34.fmt(best.get('oos_trades_per_day'))};"
            f"oos_dd={f34.fmt(best.get('oos_dd_risk'))}"
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
        "guardrail_kpi": "train_only_model_source_validation_oos_read_only_no_runtime_authority",
        "external_verification_status": external_status,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": report.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        ledger_row(
            RUN_A,
            f"{RUN_A}__stage_open",
            "stage_open(단계 개방)",
            "not_applicable_stage_open(단계 개방 해당 없음)",
            "planning_only_no_trading_kpi(계획 전용 거래 KPI 없음)",
            final["stage_open"]["status"],
            final["stage_open"]["judgment"],
            f"grok={final['stage_open']['grok']['classification']}",
            "stage_open_no_runtime",
            "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet",
            f"next={RUN_B}",
        ),
        ledger_row(
            RUN_B,
            f"{RUN_B}__tier_a_model_score_proxy",
            "Tier A separate(Tier A 분리)",
            "Tier A(티어 A)",
            "python_model_score_proxy_no_mt5(파이썬 모델 점수 프록시, MT5 아님)",
            final["proxy"]["status"],
            final["proxy"]["judgment"],
            f"candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};seed={final['proxy']['seed_rows']}",
            "train_only_model_source_no_authority",
            final["proxy"]["runtime_probe_status"],
            f"next={RUN_C}",
        ),
        ledger_row(
            RUN_B,
            f"{RUN_B}__tier_b_missing_required",
            "Tier B separate(Tier B 분리)",
            "Tier B(티어 B)",
            "missing_required(필수 누락)",
            final["proxy"]["status"],
            final["proxy"]["judgment"],
            "missing_required_no_tier_b_model_input",
            "no_tier_b_claim",
            "not_applicable_proxy_no_mt5",
            "Tier B(티어 B)는 F38 proxy(프록시) 입력으로 물질화하지 않았다.",
        ),
        ledger_row(
            RUN_B,
            f"{RUN_B}__tier_ab_combined_out_of_scope",
            "Tier A+B combined(Tier A+B 합산)",
            "Tier A+B(티어 A+B)",
            "out_of_scope_by_claim(주장 범위 밖)",
            final["proxy"]["status"],
            final["proxy"]["judgment"],
            "out_of_scope_by_claim_no_combined_source",
            "no_synthetic_combined_claim",
            "not_applicable_proxy_no_mt5",
            "Combined tier(합산 티어)는 F38 proxy(프록시)에서 주장하지 않았다.",
        ),
        ledger_row(
            RUN_C,
            f"{RUN_C}__tier_a_model_score_repair",
            "repair_or_closeout_decision(수리 또는 마감 결정)",
            "Tier A(티어 A)",
            "capped_model_score_repair_no_mt5(상한 있는 모델 점수 수리, MT5 아님)",
            final["repair"]["status"],
            final["repair"]["judgment"],
            f"candidate={final['repair']['candidate_rows']};scout={final['repair']['scout_rows']};seed={final['repair']['seed_rows']}",
            "capped_repair_no_authority",
            final["repair"]["runtime_probe_status"],
            f"next={RUN_D}",
        ),
        ledger_row(
            RUN_D,
            f"{RUN_D}__stage_closeout",
            "stage_closeout(단계 마감)",
            "Tier A(티어 A)",
            "stage_closeout_no_runtime(단계 마감, 런타임 아님)",
            final["closeout"]["status"],
            final["closeout"]["judgment"],
            f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY}",
            "preserved_clue_negative_memory_no_authority",
            final["closeout"]["runtime_probe_status"],
            f"next={NEXT_RUN_ID}",
        ),
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
    return f"""# Frontier38 Stage Brief(전선38 단계 요약)

Opened(개방): {final['created_at_utc']}

Hypothesis(가설): F37 payoff label family(보상 라벨 패밀리)만으로는 seed/runtime candidate(씨앗/런타임 후보)를 만들지 못했으므로, F38은 train-only model score source(학습 전용 모델 점수 소스)로 short path-quality(숏 경로 품질)를 순위화한다.

Action(행동): shallow model score(얕은 모델 점수)를 train split(학습 분할)에서만 fit(적합)하고, validation/OOS(검증/표본밖)는 read-only(읽기 전용)로 평가한다.

Effect(효과): F37 negative memory(부정 기억)를 반복하지 않으면서, source family(소스 패밀리) 자체를 바꾼 단서가 PF/density/DD(수익 팩터/밀도/손실폭)를 동시에 개선하는지 본다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def stage_open_report(final: dict[str, Any]) -> str:
    grok = final["stage_open"]["grok"]
    return f"""# Frontier38A Stage Open Report(전선38A 단계 개방 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['stage_open']['status']}`

Judgment(판정): `{final['stage_open']['judgment']}`

Action(행동): F38(전선38)을 train-only model score source(학습 전용 모델 점수 소스) pivot(전환)으로 열었다.

Effect(효과): F37 payoff-dominance label family(보상 우세 라벨 패밀리) 반복을 피하고, 검증/표본밖 threshold tuning(임계값 조정)을 금지한 채 proxy(프록시)를 시작한다.

Grok classification(그록 분류): `{grok['classification']}`

Next action(다음 행동): `{RUN_B}`
"""


def run_report(final: dict[str, Any], section: dict[str, Any], summary: pd.DataFrame, next_run: str) -> str:
    best = section.get("best_readonly", {})
    table = top_table(summary)
    return f"""# {section['run_id']} Report({section['run_id']} 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{section['status']}`

Judgment(판정): `{section['judgment']}`

Action(행동): model score source(모델 점수 소스) candidate(후보)를 train-only(학습 전용)로 만들고 path-native first-hit replay(경로 네이티브 최초 터치 재생)로 평가했다.

Effect(효과): feature/source pivot(피처/소스 전환)이 forward PF-density-DD(전진 수익 팩터-밀도-손실폭)에 실제 단서를 주는지 확인한다.

Candidate/scout/near-seed/seed/runtime rows(후보/탐색/근접 씨앗/씨앗/런타임 행): `{section.get('candidate_rows', 0)}` / `{section.get('scout_rows', 0)}` / `{section.get('near_seed_rows', 0)}` / `{section.get('seed_rows', 0)}` / `{section.get('runtime_rows', 0)}`

Best read-only candidate(최상 읽기 전용 후보): `{best.get('candidate_id', '')}`

Best validation PF-density-DD(최상 검증 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}/day` / `{f34.fmt(best.get('validation_dd_risk'))}%`

Best OOS PF-density-DD(최상 표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}/day` / `{f34.fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{section.get('runtime_probe_status', '')}`

| candidate(후보) | label(라벨) | model(모델) | side(방향) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | near seed | seed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{next_run}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def top_table(summary: pd.DataFrame) -> str:
    if summary.empty:
        return "| none(없음) | | | | | | | | | | | | |"
    rows: list[str] = []
    for _, row in summary.head(12).iterrows():
        rows.append(
            f"| `{row['candidate_id']}` | `{row.get('label_variant', '')}` | `{row.get('model_family', '')}` | `{row.get('score_side', '')}` | "
            f"{f34.fmt(row['validation_profit_factor'])} | {f34.fmt(row['validation_trades_per_day'])} | {f34.fmt(row['validation_dd_risk'])} | "
            f"{f34.fmt(row['oos_profit_factor'])} | {f34.fmt(row['oos_trades_per_day'])} | {f34.fmt(row['oos_dd_risk'])} | "
            f"{row['f38_scout_clue_flag']} | {row['f38_near_seed_flag']} | {row['f38_seed_surface_flag']} |"
        )
    return "\n".join(rows)


def closeout_report(final: dict[str, Any]) -> str:
    best_b = final["proxy"]["best_readonly"]
    best_c = final["repair"]["best_readonly"]
    close = final["closeout"]
    return f"""# Frontier38D Stage Closeout Report(전선38D 단계 마감 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{close['status']}`

Judgment(판정): `{close['judgment']}`

Closeout class(마감 분류): `{close['closeout_class']}`

Action(행동): F38(전선38)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았다.

Effect(효과): model score source(모델 점수 소스)는 density/DD(밀도/손실폭) 단서를 회복했지만, seed/runtime(씨앗/런타임) 기준을 넘지 못한 사실을 다음 frontier stage(전선 단계)의 입력으로 제한한다.

Proxy best validation/OOS PF-density-DD(프록시 최상 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best_b.get('validation_profit_factor'))}` / `{f34.fmt(best_b.get('validation_trades_per_day'))}` / `{f34.fmt(best_b.get('validation_dd_risk'))}` and `{f34.fmt(best_b.get('oos_profit_factor'))}` / `{f34.fmt(best_b.get('oos_trades_per_day'))}` / `{f34.fmt(best_b.get('oos_dd_risk'))}`

Repair best validation/OOS PF-density-DD(수리 최상 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best_c.get('validation_profit_factor'))}` / `{f34.fmt(best_c.get('validation_trades_per_day'))}` / `{f34.fmt(best_c.get('validation_dd_risk'))}` and `{f34.fmt(best_c.get('oos_profit_factor'))}` / `{f34.fmt(best_c.get('oos_trades_per_day'))}` / `{f34.fmt(best_c.get('oos_dd_risk'))}`

Runtime probe status(런타임 탐침 상태): `{close['runtime_probe_status']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Grok closeout classification(그록 마감 분류): `{close['grok']['classification']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def grok_stage_open_receipt(final: dict[str, Any]) -> str:
    grok = final["stage_open"]["grok"]
    return f"""# Grok Stage Open Receipt(그록 단계 개방 영수증)

Classification(분류): `{grok['classification']}`

Accepted(수용): `{grok['accepted']}`

Action(행동): Grok(그록) stage open(단계 개방) 의견을 bounded evidence(제한 근거)로 분류했다.

Effect(효과): 외부 의견을 자동 실행하지 않고, local verification(로컬 검증) 후 F38 proxy(프록시)에만 반영했다.

First returncode(첫 반환 코드): `{grok['first_returncode']}`

Retry returncode(재시도 반환 코드): `{grok['retry_returncode']}`

Effective packet(유효 묶음): `{grok.get('effective_packet', grok['retry_packet'])}`

Unexpected top-level artifacts(예상 밖 최상위 산출물): `{grok['retry_unexpected_top_level_artifacts']}`
"""


def grok_stage_closeout_receipt(final: dict[str, Any]) -> str:
    grok = final["closeout"]["grok"]
    return f"""# Grok Stage Closeout Receipt(그록 단계 마감 영수증)

Classification(분류): `{grok['classification']}`

Accepted(수용): `{grok['accepted']}`

Action(행동): Grok(그록) closeout(마감) 의견을 accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) 경계로 분류했다.

Effect(효과): closeout(마감) 판단은 Codex(코덱스)가 local artifacts(로컬 산출물), register(등록부), runtime probe status(런타임 탐침 상태)로 다시 확인하게 한다.

First returncode(첫 반환 코드): `{grok['first_returncode']}`

Retry returncode(재시도 반환 코드): `{grok['retry_returncode']}`

Effective packet(유효 묶음): `{grok.get('effective_packet', grok['retry_packet'])}`

Unexpected top-level artifacts(예상 밖 최상위 산출물): `{grok['retry_unexpected_top_level_artifacts']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    checks = "\n".join(f"- `{name}`: `{value}`" for name, value in final["context"]["checks"].items())
    return f"""# Frontier38 Local Verification(전선38 로컬 검증)

Updated(갱신): {final['created_at_utc']}

Action(행동): workspace state(작업공간 상태), feature hash(피처 해시), split(분할), raw path alignment(원천 경로 정렬), Grok transport(그록 전송)를 확인했다.

Effect(효과): F38 결과가 낡은 stage(단계)나 깨진 데이터 경계에서 나온 것이 아님을 확인한다.

{checks}

Context judgment(맥락 판정): `{final['context']['judgment']}`

Feature order hash(피처 순서 해시): `{final['feature_order_hash']}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
"""


def gate_audit_text(final: dict[str, Any], section: dict[str, Any]) -> str:
    return f"""# {section['run_id']} Gate Audit({section['run_id']} 게이트 감사)

Action(행동): required gates(필수 게이트)를 run(실행) 산출물과 연결했다.

Effect(효과): proxy/repair(프록시/수리)가 final completion review(최종 완성 검토)의 hard gate(강제 게이트)를 앞당겨 주장하지 않게 한다.

- experiment_design(실험 설계): stage brief(단계 요약)와 Grok stage open(그록 단계 개방) receipt(영수증)로 충족
- data_integrity(데이터 무결성): feature hash(피처 해시), split(분할), raw path alignment(원천 경로 정렬) 확인
- model_validation(모델 검증): train-only fit(학습 전용 적합), validation/OOS read-only(검증/표본밖 읽기 전용)
- artifact_lineage(산출물 계보): run_manifest(실행 목록)와 summary CSV(요약 CSV) 기록
- result_judgment(결과 판정): `{section['judgment']}`
- runtime_probe(런타임 탐침): `{section['runtime_probe_status']}`
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier38 Required Gate Coverage Audit(전선38 필수 게이트 커버리지 감사)

Action(행동): F38 work packet(작업 묶음)의 required gates(필수 게이트)를 closeout(마감) 산출물에 연결했다.

Effect(효과): 완료 주장(completion claim, 완료 주장) 없이도 어떤 근거가 닫혔고 어떤 주장이 금지되는지 분명해진다.

- primary_family(주 작업군): `experiment_execution(실험 실행)`
- primary_skill(주 스킬): `obsidian-experiment-design(옵시디언 실험 설계)`
- support_skills(보조 스킬): exploration_mandate/data_integrity/model_validation/artifact_lineage/result_judgment/grok_collaboration/reentry_read(탐색 규율/데이터 무결성/모델 검증/산출물 계보/결과 판정/그록 협업/재진입 읽기)
- stage open Grok(단계 개방 그록): `{final['stage_open']['grok']['classification']}`
- closeout Grok(마감 그록): `{final['closeout']['grok']['classification']}`
- proxy rows(프록시 행): `{final['proxy']['candidate_rows']}`, scout(탐색): `{final['proxy']['scout_rows']}`, seed(씨앗): `{final['proxy']['seed_rows']}`, runtime(런타임): `{final['proxy']['runtime_rows']}`
- repair rows(수리 행): `{final['repair']['candidate_rows']}`, scout(탐색): `{final['repair']['scout_rows']}`, seed(씨앗): `{final['repair']['seed_rows']}`, runtime(런타임): `{final['repair']['runtime_rows']}`
- runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Claim boundary(주장 경계): baseline/promotion/runtime authority/live readiness/Goal Achieve(기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return f"""# Frontier38 Preserved Clue(전선38 보존 단서)

Clue(단서): `{PRESERVED_CLUE}`

Action(행동): train-only model score source(학습 전용 모델 점수 소스)가 scout surface(탐색 표면)를 만든 사실만 보존한다.

Effect(효과): 다음 stage(단계)는 density/DD(밀도/손실폭) 회복을 참고하되, seed/runtime authority(씨앗/런타임 권위)를 상속하지 않는다.

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Validation/OOS PF-density-DD(검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}` / `{f34.fmt(best.get('validation_dd_risk'))}` and `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}` / `{f34.fmt(best.get('oos_dd_risk'))}`
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier38 Negative Memory(전선38 부정 기억)

Memory(기억): `{NEGATIVE_MEMORY}`

Action(행동): shallow model score source family(얕은 모델 점수 소스 패밀리)가 seed/runtime candidate(씨앗/런타임 후보)를 만들지 못한 결과를 남긴다.

Effect(효과): 다음 frontier stage(전선 단계)에서 같은 score/quantile repair(점수/분위수 수리)를 반복해 시간을 쓰지 않게 한다.

Do not repeat(반복 금지): 같은 shallow model score source(얕은 모델 점수 소스)와 같은 path-quality quantile(경로 품질 분위수) 조합만 넓히는 수리.

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier38 Selection Status(전선38 선택 상태)

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Action(행동): F38(전선38)은 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫고, `{NEXT_STAGE_ID}`를 다음 질문으로 남긴다.

Effect(효과): F38 scout clue(탐색 단서)를 reference-only(참조 전용)로 보존하고, baseline/promotion/runtime authority(기준선/승격/런타임 권위)는 만들지 않는다.

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`
"""


def decision_open(final: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier38 Model Score Source(결정: 전선38 모델 점수 소스 개방)

Date(날짜): 2026-06-15

Decision(결정): `{RUN_A}` starts `{STAGE_ID}`.

Action(행동): source family(소스 패밀리)를 train-only model score(학습 전용 모델 점수)로 바꾼다.

Effect(효과): F37 payoff label family(보상 라벨 패밀리) 실패를 반복하지 않고 새 hypothesis lifecycle(가설 생명주기)을 시작한다.

Grok classification(그록 분류): `{final['stage_open']['grok']['classification']}`
"""


def decision_closeout(final: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier38 Model Score Source(결정: 전선38 모델 점수 소스 마감)

Date(날짜): 2026-06-15

Decision(결정): `{RUN_D}` closes `{STAGE_ID}` as `{final['closeout']['closeout_class']}`.

Action(행동): F38(전선38)을 scout-only(탐색 전용) 단서와 negative memory(부정 기억)로 닫는다.

Effect(효과): 다음 stage(단계)는 model score(모델 점수) 단서를 참고하되, seed/runtime candidate(씨앗/런타임 후보) 부재를 상속받아 같은 수리를 반복하지 않는다.

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return f"""

## {RUN_D}

- Action(행동): F38 train-only model score source(학습 전용 모델 점수 소스) proxy/repair/closeout(프록시/수리/마감)을 기록했다.
- Effect(효과): scout clue(탐색 단서)는 보존하고 seed/runtime authority(씨앗/런타임 권위)는 주장하지 않는다.
- Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
- Next(다음): `{NEXT_RUN_ID}`
"""


def idea_registry_open(final: dict[str, Any]) -> str:
    return f"""

### {RUN_A}

- Stage(단계): `{STAGE_ID}`
- Idea(아이디어): train-only model score source(학습 전용 모델 점수 소스)로 short path-quality(숏 경로 품질)를 순위화한다.
- Effect(효과): F37 payoff label family(보상 라벨 패밀리) 반복 대신 source family(소스 패밀리)를 바꾼다.
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
- Action(행동): shallow model score source(얕은 모델 점수 소스) proxy/repair(프록시/수리)가 seed/runtime candidate(씨앗/런타임 후보)를 만들지 못한 결과를 기록했다.
- Effect(효과): 같은 score quantile repair(점수 분위수 수리)를 신규성 없이 반복하지 않는다.
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

Action(행동): F38(전선38)을 train-only model score source(학습 전용 모델 점수 소스) lifecycle(생명주기)로 닫았다.

Effect(효과): scout clue(탐색 단서)는 보존하고, seed/runtime candidate(씨앗/런타임 후보) 부재를 negative memory(부정 기억)로 남긴다.

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Best validation/OOS PF-density-DD(최상 검증/표본밖 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}` / `{f34.fmt(best.get('validation_dd_risk'))}` and `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}` / `{f34.fmt(best.get('oos_dd_risk'))}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)이다.
"""


def output_summary(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "closeout_run_id": RUN_D,
        "proxy_candidate_rows": final["proxy"]["candidate_rows"],
        "proxy_scout_rows": final["proxy"]["scout_rows"],
        "proxy_near_seed_rows": final["proxy"]["near_seed_rows"],
        "proxy_seed_rows": final["proxy"]["seed_rows"],
        "repair_candidate_rows": final["repair"]["candidate_rows"],
        "repair_scout_rows": final["repair"]["scout_rows"],
        "repair_near_seed_rows": final["repair"]["near_seed_rows"],
        "repair_seed_rows": final["repair"]["seed_rows"],
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
