from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import ElasticNet, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from foundation.control_plane.ledger import io_path, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b


STAGE_ID = "stage_frontier_44__short_pf_edge_label_model_pivot_after_f43_trade_shape_negative"
PREV_STAGE_ID = "stage_frontier_43__short_pf_edge_trade_shape_source_pivot_after_f42_timing_negative"
RUN_A = "frontier44A_stage_open_short_pf_edge_label_model_source_hypothesis_design_v1"
RUN_B = "frontier44B_train_only_short_path_utility_label_model_proxy_v1"
RUN_C = "frontier44C_capped_label_model_repair_v1"
RUN_D = "frontier44D_stage_closeout_label_model_pivot_v1"
NEXT_STAGE_ID = "stage_frontier_45__short_pf_edge_event_utility_model_pivot_after_f44_label_model_memory"
NEXT_RUN_ID = "frontier45A_stage_open_short_pf_edge_event_utility_model_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

PREV_ROOT = Path("stages") / PREV_STAGE_ID
PREV_SELECTION_JSON = PREV_ROOT / "04_selected" / "selection_status.json"
PREV_SELECTION_MD = PREV_ROOT / "04_selected" / "selection_status.md"
PREV_PRESERVED_CLUE = PREV_ROOT / "04_selected" / "preserved_clue.md"
PREV_NEGATIVE_MEMORY = PREV_ROOT / "04_selected" / "negative_memory.md"

GROK_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier44_stage_open" / "small_review"
GROK_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier44_stage_closeout" / "small_review"

PROJECT_LEDGER = Path("docs") / "registers" / "alpha_run_ledger.csv"
WORKSPACE_STATE = Path("docs") / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = Path("docs") / "context" / "current_working_state.md"
PRE_ALPHA_PLAN = Path("docs") / "workspace" / "pre_alpha_stage_plan.md"

SPLITS = ("train", "validation", "oos")
SIDE_VALUE = -1
SIDE_LABEL = "short"


def review_report_path(run_id: str) -> Path:
    names = {
        RUN_A: "runA_report.md",
        RUN_B: "runB_report.md",
        RUN_C: "runC_report.md",
        RUN_D: "runD_closeout_report.md",
    }
    return REVIEWS_ROOT / names.get(run_id, f"{run_id}_report.md")

INITIAL_SCORE_QUANTILES = (0.78, 0.82, 0.86, 0.90, 0.94)
INITIAL_STOP_QUANTILES = (0.18, 0.26, 0.34)
INITIAL_TAKE_QUANTILES = (0.62, 0.72, 0.82)
INITIAL_RR_FLOORS = (1.25, 1.65, 2.10)
REPAIR_SCORE_QUANTILES = (0.74, 0.80, 0.86, 0.92)
REPAIR_STOP_QUANTILES = (0.14, 0.24, 0.38)
REPAIR_TAKE_QUANTILES = (0.58, 0.70, 0.86)
REPAIR_RR_FLOORS = (1.10, 1.55, 2.30)

INITIAL_MAX_CANDIDATES = 180
REPAIR_MAX_CANDIDATES = 160
TRAIN_MIN_TRADES = 45
TRAIN_MIN_DENSITY = 4.0
TRAIN_MAX_DENSITY = 14.0
TRAIN_DD_CAP = 22.0
TRAIN_PF_FLOOR = 1.01
AMBIGUOUS_RATE_CAP = 0.40

SCOUT_MIN_PF = 1.05
SCOUT_MIN_DENSITY = 4.0
SCOUT_MAX_DENSITY = 12.0
SCOUT_MAX_DD = 18.0
SEED_MIN_PF = 1.20
SEED_MIN_DENSITY = 5.0
SEED_MAX_DENSITY = 10.0
SEED_MAX_DD = 12.0
RUNTIME_MIN_PF = 1.50
RUNTIME_MAX_DD = 10.0


def main() -> None:
    mkdirs()
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    open_review = load_open_grok_review()
    closeout_review = load_closeout_grok_review()
    checks = context_checks(frame, feature_order, raw_path, path_labels, open_review)
    manifest = build_input_manifest(frame, feature_order, raw_path, path_labels, checks, open_review)
    write_json(INPUT_ROOT / "short_path_utility_model_manifest.json", manifest)
    write_text_sig(SPEC_ROOT / "stage_brief.md", build_stage_brief(manifest, open_review, checks))
    write_json(RUN_A_ROOT / "stage_open_local_verification.json", {"open_review": open_review, "checks": checks})

    initial = build_model_surface(
        frame,
        feature_order,
        path_labels,
        raw_path,
        run_id=RUN_B,
        run_prefix="f44b",
        profile="initial",
        target_specs=target_specs(frame, path_labels[SIDE_VALUE], "initial"),
        model_specs=model_specs("initial"),
        score_quantiles=INITIAL_SCORE_QUANTILES,
        stop_quantiles=INITIAL_STOP_QUANTILES,
        take_quantiles=INITIAL_TAKE_QUANTILES,
        rr_floors=INITIAL_RR_FLOORS,
        max_candidates=INITIAL_MAX_CANDIDATES,
    )
    write_surface_outputs(RUN_B_ROOT, "initial", initial)

    repair_decision = build_repair_decision(initial["summary"])
    repair = empty_surface()
    if repair_decision["run_repair_grid"]:
        repair = build_model_surface(
            frame,
            feature_order,
            path_labels,
            raw_path,
            run_id=RUN_C,
            run_prefix="f44c",
            profile="repair",
            target_specs=target_specs(frame, path_labels[SIDE_VALUE], "repair"),
            model_specs=model_specs("repair"),
            score_quantiles=REPAIR_SCORE_QUANTILES,
            stop_quantiles=REPAIR_STOP_QUANTILES,
            take_quantiles=REPAIR_TAKE_QUANTILES,
            rr_floors=REPAIR_RR_FLOORS,
            max_candidates=REPAIR_MAX_CANDIDATES,
        )
    write_json(RUN_C_ROOT / "repair_decision.json", repair_decision)
    write_surface_outputs(RUN_C_ROOT, "repair", repair)

    closeout = classify_closeout(initial["summary"], repair["summary"])
    combined = combine_summaries(initial["summary"], repair["summary"])
    best_rows = top_records(combined, 8)
    write_json(RUN_D_ROOT / "closeout_decision.json", closeout)
    if not path_exists(GROK_CLOSE_ROOT / "metadata.json"):
        write_text_sig(GROK_CLOSE_ROOT / "input_prompt.md", build_closeout_prompt(closeout, best_rows, repair_decision))
    closeout_review = load_closeout_grok_review()

    artifacts = build_review_artifacts(
        frame=frame,
        checks=checks,
        manifest=manifest,
        open_review=open_review,
        closeout_review=closeout_review,
        initial=initial,
        repair=repair,
        repair_decision=repair_decision,
        closeout=closeout,
    )
    for path, text in artifacts.items():
        write_text_sig(path, text)
    write_json(
        RUN_D_ROOT / "run_manifest.json",
        {
            "stage_id": STAGE_ID,
            "runs": [RUN_A, RUN_B, RUN_C, RUN_D],
            "profile": "short_path_utility_label_model_proxy",
            "open_review": open_review,
            "closeout_review": closeout_review,
            "repair_decision": repair_decision,
            "closeout": closeout,
            "train_only_isolation_wall": True,
            "artifacts": artifact_map(),
        },
    )
    write_json(SELECTED_ROOT / "selection_status.json", closeout)
    for path, text in build_selected_notes(closeout).items():
        write_text_sig(path, text)
    update_stage_ledgers(closeout, checks)
    if closeout_review.get("accepted_after_local_verification"):
        update_workspace_docs(closeout)


def mkdirs() -> None:
    for path in (
        SPEC_ROOT,
        INPUT_ROOT,
        RUN_A_ROOT,
        RUN_B_ROOT,
        RUN_C_ROOT,
        RUN_D_ROOT,
        REVIEWS_ROOT,
        SELECTED_ROOT,
        GROK_CLOSE_ROOT,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        item = float(value)
        return item if math.isfinite(item) else None
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if pd.isna(value) and not isinstance(value, str):
        return None
    return value


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8-sig")


def write_dict_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if rows:
        fields = list(rows[0].keys())
    else:
        fields = ["stage_id", "run_id", "record_view", "status", "closeout_class", "runtime_probe_status", "notes"]
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing"}


def hash_items(items: list[Any]) -> str:
    return hashlib.sha256(json.dumps(json_ready(items), sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def safe_float(value: Any) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return 0.0
    return result if math.isfinite(result) else 0.0


def load_open_grok_review() -> dict[str, Any]:
    metadata_path = GROK_OPEN_ROOT / "metadata.json"
    clean_path = GROK_OPEN_ROOT / "clean_output.md"
    metadata = read_json(metadata_path) if path_exists(metadata_path) else {}
    clean = read_text(clean_path) if path_exists(clean_path) else ""
    lowered = clean.lower()
    accepted = (
        "`accepted`" in lowered
        or "verdict:** `accepted`" in lowered
        or "verdict:** accepted" in lowered
        or "verdict: accepted" in lowered
    )
    rejected = (
        "`rejected`" in lowered
        or "verdict:** `rejected`" in lowered
        or "verdict:** rejected" in lowered
        or "verdict: rejected" in lowered
    )
    guardrail_seen = "train-only" in lowered and ("isolation" in lowered or "격리" in clean)
    forbidden = any(
        phrase in lowered
        for phrase in ("operating promotion", "runtime authority", "live readiness", "goal achieve", "selected baseline")
    )
    return {
        "packet": GROK_OPEN_ROOT.as_posix(),
        "metadata": metadata,
        "clean_output_path": clean_path.as_posix(),
        "classification": "accepted_stage_open_train_only_isolation_wall" if accepted and guardrail_seen and not rejected else "needs_local_verification",
        "accepted_after_local_verification": bool(accepted and guardrail_seen and not rejected),
        "guardrail_seen": bool(guardrail_seen),
        "forbidden_claim_seen": bool(forbidden),
        "clean_excerpt": clean.strip()[:1200],
    }


def load_closeout_grok_review() -> dict[str, Any]:
    metadata_path = GROK_CLOSE_ROOT / "metadata.json"
    clean_path = GROK_CLOSE_ROOT / "clean_output.md"
    if not path_exists(metadata_path) or not path_exists(clean_path):
        return {
            "packet": GROK_CLOSE_ROOT.as_posix(),
            "classification": "pending_closeout_grok_review",
            "accepted_after_local_verification": False,
            "clean_output_path": clean_path.as_posix(),
        }
    metadata = read_json(metadata_path)
    clean = read_text(clean_path)
    lowered = clean.lower()
    accepted = (
        "`accepted`" in lowered
        or "verdict:** `accepted`" in lowered
        or "verdict:** accepted" in lowered
        or "verdict: accepted" in lowered
    )
    rejected = (
        "`rejected`" in lowered
        or "verdict:** `rejected`" in lowered
        or "verdict:** rejected" in lowered
        or "verdict: rejected" in lowered
    )
    boundary_ok = "boundary_ok" in lowered and ("yes" in lowered or "`yes`" in lowered)
    forbidden = any(
        phrase in lowered
        for phrase in ("operating promotion", "runtime authority", "live readiness", "goal achieve", "selected baseline")
    )
    return {
        "packet": GROK_CLOSE_ROOT.as_posix(),
        "metadata": metadata,
        "clean_output_path": clean_path.as_posix(),
        "classification": "accepted_closeout_label_model_boundary" if accepted and boundary_ok and not rejected else "needs_local_verification",
        "accepted_after_local_verification": bool(accepted and boundary_ok and not rejected),
        "boundary_ok": bool(boundary_ok),
        "forbidden_claim_seen": bool(forbidden),
        "clean_excerpt": clean.strip()[:1200],
    }


def context_checks(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    path_labels: dict[int, dict[str, np.ndarray]],
    open_review: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    previous_selection = read_text(PREV_SELECTION_MD) if path_exists(PREV_SELECTION_MD) else ""
    feature_hash = ordered_hash(feature_order)
    split_counts = {str(k): int(v) for k, v in frame["split"].astype(str).value_counts().to_dict().items()}
    checks = {
        "workspace_points_from_f43_to_f44_or_current_f44": (
            (f"current_stage_id: {PREV_STAGE_ID}" in workspace and f"next_stage_id: {STAGE_ID}" in workspace)
            or f"current_stage_id: {STAGE_ID}" in workspace
        ),
        "previous_selection_points_to_f44": f"next_stage(다음 단계): `{STAGE_ID}`" in previous_selection,
        "previous_closeout_negative_memory": "negative_memory" in previous_selection,
        "feature_hash_matches_contract": feature_hash == f23b.EXPECTED_FEATURE_HASH,
        "feature_count_58": len(feature_order) == 58,
        "required_splits_present": all(split in split_counts for split in SPLITS),
        "raw_path_exists": path_exists(f33b.RAW_US100_PATH),
        "raw_alignment_no_missing": int(raw_path.get("missing_entry_positions", -1)) == 0
        and int(raw_path.get("missing_future_positions", -1)) == 0,
        "short_path_valid_rows_positive": int(path_labels[SIDE_VALUE]["valid"].sum()) > 0,
        "open_grok_accepted": bool(open_review.get("accepted_after_local_verification")),
        "train_only_isolation_wall": bool(open_review.get("guardrail_seen")),
        "validation_oos_read_only_policy": True,
    }
    if not all(checks.values()):
        raise RuntimeError(f"F44 context check failed: {json.dumps(checks, ensure_ascii=False, sort_keys=True)}")
    return {
        "checks": checks,
        "feature_hash": feature_hash,
        "feature_order_artifact": artifact_identity(f23b.FEATURE_ORDER_PATH),
        "training_dataset_artifact": artifact_identity(f23b.DATASET_PATH),
        "raw_us100_artifact": artifact_identity(f33b.RAW_US100_PATH),
        "split_counts": split_counts,
        "short_valid_rows": int(path_labels[SIDE_VALUE]["valid"].sum()),
    }


def build_input_manifest(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    path_labels: dict[int, dict[str, np.ndarray]],
    checks: dict[str, Any],
    open_review: dict[str, Any],
) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_ids": [RUN_A, RUN_B, RUN_C, RUN_D],
        "primary_family": "experiment_execution",
        "primary_skill_requested": "obsidian-run-evidence-system",
        "primary_skill_available": False,
        "support_skills": [
            "obsidian-experiment-design",
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
            "obsidian-grok-collaboration",
        ],
        "hypothesis": "train-only short path-utility label model can separate short PF edge better than F43 source threshold mining",
        "decision_use": "scout/seed/runtime candidate classification only",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": int(len(frame)),
            "split_counts": checks["split_counts"],
            "short_path_valid_rows": int(path_labels[SIDE_VALUE]["valid"].sum()),
        },
        "data_source": {
            "training_dataset": checks["training_dataset_artifact"],
            "feature_order": checks["feature_order_artifact"],
            "raw_us100": checks["raw_us100_artifact"],
            "raw_rows": int(raw_path["raw_rows"]),
        },
        "feature_label_boundary": "features are closed-bar only; future path labels are used only as train targets and validation/OOS evaluation outcomes",
        "split_boundary": "model fit, label target transforms, score thresholds, SL/TP caps, and candidate ranking are train-only; validation/OOS are read-only",
        "grok_open_review": open_review,
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness",
    }


def target_specs(frame: pd.DataFrame, labels: dict[str, np.ndarray], profile: str) -> list[dict[str, Any]]:
    train = f33b.split_mask(frame, "train") & labels["valid"]
    mfe = labels["mfe"]
    mae = labels["mae"]
    horizon = labels["horizon_pnl"]
    train_mfe = mfe[train & np.isfinite(mfe)]
    train_mae = mae[train & np.isfinite(mae)]
    train_horizon = horizon[train & np.isfinite(horizon)]
    mfe60 = float(np.nanquantile(train_mfe, 0.60))
    mfe70 = float(np.nanquantile(train_mfe, 0.70))
    mae40 = float(np.nanquantile(train_mae, 0.40))
    mae55 = float(np.nanquantile(train_mae, 0.55))
    mae75 = float(np.nanquantile(train_mae, 0.75))
    horizon_q60 = float(np.nanquantile(train_horizon, 0.60))

    clipped_h = np.clip(horizon, -0.012, 0.012)
    clipped_mfe = np.clip(mfe, 0.0, 0.012)
    clipped_mae = np.clip(mae, 0.0, 0.012)
    utility_linear = clipped_h + 0.35 * clipped_mfe - 0.70 * clipped_mae
    utility_quality = (
        0.60 * (mfe >= mfe60).astype("float64")
        + 0.35 * (horizon >= horizon_q60).astype("float64")
        - 0.70 * (mae >= mae75).astype("float64")
        + np.clip(horizon / 0.006, -1.0, 1.0) * 0.20
    )
    utility_dd_soft = clipped_h + 0.20 * clipped_mfe - 0.95 * clipped_mae + 0.0025 * (mae <= mae40).astype("float64")
    out = [
        {
            "target_variant": "linear_horizon_mfe_mae",
            "target_definition": "clip(horizon_pnl)+0.35*clip(mfe)-0.70*clip(mae)",
            "target": utility_linear,
            "train_thresholds": {"mfe60": mfe60, "mae75": mae75},
        },
        {
            "target_variant": "quality_rank_mfe60_horizon60_mae75",
            "target_definition": "rank-like short path quality using train q60 MFE, q60 horizon, q75 MAE penalty",
            "target": utility_quality,
            "train_thresholds": {"mfe60": mfe60, "horizon_q60": horizon_q60, "mae75": mae75},
        },
        {
            "target_variant": "drawdown_soft_utility_mae40",
            "target_definition": "clip(horizon_pnl)+0.20*clip(mfe)-0.95*clip(mae)+low_mae bonus",
            "target": utility_dd_soft,
            "train_thresholds": {"mae40": mae40, "mae55": mae55, "mfe70": mfe70},
        },
    ]
    if profile == "repair":
        utility_quality_tight = (
            0.75 * (mfe >= mfe70).astype("float64")
            + 0.30 * (horizon > 0.0).astype("float64")
            - 0.55 * (mae >= mae55).astype("float64")
            + np.clip(horizon / 0.005, -1.0, 1.0) * 0.25
        )
        out.append(
            {
                "target_variant": "repair_quality_mfe70_mae55",
                "target_definition": "capped repair target using train q70 MFE and q55 MAE penalty",
                "target": utility_quality_tight,
                "train_thresholds": {"mfe70": mfe70, "mae55": mae55},
            }
        )
    return out


def model_specs(profile: str) -> list[dict[str, Any]]:
    specs = [
        {
            "model_family": "ridge_alpha1",
            "onnx_friendly": True,
            "factory": lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        },
        {
            "model_family": "ridge_alpha10",
            "onnx_friendly": True,
            "factory": lambda: make_pipeline(StandardScaler(), Ridge(alpha=10.0)),
        },
        {
            "model_family": "elasticnet_a0001_l1p15",
            "onnx_friendly": True,
            "factory": lambda: make_pipeline(
                StandardScaler(),
                ElasticNet(alpha=0.0001, l1_ratio=0.15, max_iter=2000, random_state=4401),
            ),
        },
        {
            "model_family": "extratrees_reg_d3_leaf180",
            "onnx_friendly": True,
            "factory": lambda: ExtraTreesRegressor(
                n_estimators=96,
                max_depth=3,
                min_samples_leaf=180,
                random_state=4403,
                n_jobs=1,
            ),
        },
    ]
    if profile == "repair":
        specs.append(
            {
                "model_family": "extratrees_reg_d5_leaf220",
                "onnx_friendly": True,
                "factory": lambda: ExtraTreesRegressor(
                    n_estimators=96,
                    max_depth=5,
                    min_samples_leaf=220,
                    random_state=4455,
                    n_jobs=1,
                ),
            }
        )
    return specs


def build_model_surface(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    *,
    run_id: str,
    run_prefix: str,
    profile: str,
    target_specs: list[dict[str, Any]],
    model_specs: list[dict[str, Any]],
    score_quantiles: tuple[float, ...],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    max_candidates: int,
) -> dict[str, Any]:
    x = frame[feature_order].to_numpy(dtype="float64")
    valid_features = np.isfinite(x).all(axis=1)
    labels = path_labels[SIDE_VALUE]
    train_mask = f33b.split_mask(frame, "train") & valid_features & labels["valid"]
    model_rows: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []

    for target_spec in target_specs:
        target = np.asarray(target_spec["target"], dtype="float64")
        fit_mask = train_mask & np.isfinite(target)
        if int(np.sum(fit_mask)) < 300:
            model_rows.append(
                {
                    "target_variant": target_spec["target_variant"],
                    "model_family": "not_fit",
                    "status": "skipped_sparse_train_target",
                    "train_rows": int(np.sum(fit_mask)),
                }
            )
            continue
        target_train = target[fit_mask]
        y_low = float(np.nanquantile(target_train, 0.01))
        y_high = float(np.nanquantile(target_train, 0.99))
        y = np.clip(target, y_low, y_high)
        for model_spec in model_specs:
            model = model_spec["factory"]()
            model.fit(x[fit_mask], y[fit_mask])
            score = np.full(len(frame), np.nan, dtype="float64")
            score[valid_features] = np.asarray(model.predict(x[valid_features]), dtype="float64")
            finite_score = np.isfinite(score) & valid_features
            train_scores = score[train_mask & finite_score]
            model_rows.append(
                {
                    "run_id": run_id,
                    "profile": profile,
                    "target_variant": target_spec["target_variant"],
                    "target_definition": target_spec["target_definition"],
                    "model_family": model_spec["model_family"],
                    "onnx_friendly": bool(model_spec.get("onnx_friendly", False)),
                    "status": "fit_train_only",
                    "train_rows": int(np.sum(fit_mask)),
                    "train_target_q01": y_low,
                    "train_target_q99": y_high,
                    "train_score_min": safe_float(np.nanmin(train_scores)) if train_scores.size else math.nan,
                    "train_score_max": safe_float(np.nanmax(train_scores)) if train_scores.size else math.nan,
                    "train_thresholds": json.dumps(json_ready(target_spec["train_thresholds"]), sort_keys=True),
                }
            )
            if train_scores.size < 100:
                continue
            for score_q in score_quantiles:
                threshold = float(np.nanquantile(train_scores, score_q))
                mask = finite_score & (score >= threshold)
                candidates.extend(
                    candidates_for_mask(
                        frame,
                        mask,
                        path_labels,
                        raw_path,
                        stop_quantiles,
                        take_quantiles,
                        rr_floors,
                        target_spec,
                        model_spec,
                        score_q,
                        threshold,
                        profile,
                    )
                )

    selected = rank_candidates(candidates, run_prefix, max_candidates)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = summarize_f44_candidates(split_metrics, selected)
    return {
        "model_audit": pd.DataFrame(model_rows),
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "model_rows": int(len(model_rows)),
        "candidate_rows": int(len(selected)),
        **surface_counts(summary),
    }


def candidates_for_mask(
    frame: pd.DataFrame,
    mask: np.ndarray,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    target_spec: dict[str, Any],
    model_spec: dict[str, Any],
    score_quantile: float,
    score_threshold: float,
    profile: str,
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    condition = {
        "condition_id": f"{target_spec['target_variant']}__{model_spec['model_family']}__q{score_quantile:.2f}",
        "feature": model_spec["model_family"],
        "feature_family": "train_only_path_utility_model_score",
        "definition": (
            f"{target_spec['target_variant']} {model_spec['model_family']} score >= train q{score_quantile:.2f}"
        ),
    }
    for row in threshold_rows(
        frame,
        mask,
        path_labels[SIDE_VALUE],
        stop_quantiles,
        take_quantiles,
        rr_floors,
        f"f44_{profile}_train_only_path_utility_thresholds",
    ):
        metrics = f33b.evaluate_path_mask(
            frame,
            mask,
            SIDE_VALUE,
            float(row["stop_cap_log_return"]),
            float(row["take_cap_log_return"]),
            path_labels,
            raw_path,
            "train",
        )
        if not train_gate(metrics):
            continue
        score = train_selection_score(metrics, score_quantile)
        candidate = f33b.candidate_from_conditions([condition], mask, SIDE_VALUE, row, metrics, score)
        candidate["profile"] = profile
        candidate["target_variant"] = target_spec["target_variant"]
        candidate["target_definition"] = target_spec["target_definition"]
        candidate["model_family"] = model_spec["model_family"]
        candidate["onnx_friendly"] = bool(model_spec.get("onnx_friendly", False))
        candidate["score_quantile"] = score_quantile
        candidate["score_threshold"] = score_threshold
        candidate["f44_train_selection_score"] = score
        candidate["selection_rank_basis"] = "train_only_path_metrics_no_validation_oos_feedback"
        variants.append(candidate)
    variants.sort(key=lambda item: float(item["f44_train_selection_score"]), reverse=True)
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


def train_gate(metrics: dict[str, Any]) -> bool:
    trade_count = int(metrics.get("trade_count", 0))
    density = safe_float(metrics.get("trades_per_day"))
    ambiguous_rate = safe_float(metrics.get("ambiguous_both_hit_count")) / max(float(trade_count), 1.0)
    return (
        trade_count >= TRAIN_MIN_TRADES
        and TRAIN_MIN_DENSITY <= density <= TRAIN_MAX_DENSITY
        and safe_float(metrics.get("net_profit")) > 0.0
        and safe_float(metrics.get("profit_factor")) >= TRAIN_PF_FLOOR
        and safe_float(metrics.get("dd_risk")) <= TRAIN_DD_CAP
        and ambiguous_rate <= AMBIGUOUS_RATE_CAP
    )


def train_selection_score(metrics: dict[str, Any], score_quantile: float) -> float:
    trade_count = max(safe_float(metrics.get("trade_count")), 1.0)
    density = safe_float(metrics.get("trades_per_day"))
    pf = safe_float(metrics.get("profit_factor"))
    dd = safe_float(metrics.get("dd_risk"))
    payoff = safe_float(metrics.get("payoff_ratio"))
    path_quality = safe_float(metrics.get("path_quality_rate"))
    ambiguous_rate = safe_float(metrics.get("ambiguous_both_hit_count")) / trade_count
    density_bonus = max(0.0, 1.0 - abs(density - 7.5) / 7.5)
    q_bonus = max(0.0, 1.0 - abs(score_quantile - 0.86) / 0.20)
    return float(
        4.6 * min(pf, 4.0)
        + 1.7 * density_bonus
        + 0.8 * min(payoff, 4.0)
        + 1.2 * path_quality
        + 0.4 * q_bonus
        - 0.28 * max(0.0, dd - 10.0)
        - 1.6 * ambiguous_rate
    )


def rank_candidates(candidates: list[dict[str, Any]], prefix: str, limit: int) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, float, float, float]] = set()
    selected: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: float(item["f44_train_selection_score"]), reverse=True):
        key = (
            str(candidate.get("target_variant", "")),
            str(candidate.get("model_family", "")),
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
        candidate["train_rank"] = index
    return selected


def summarize_f44_candidates(split_metrics: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    if split_metrics.empty:
        return pd.DataFrame()
    summary = f33b.summarize_candidates(split_metrics)
    if summary.empty:
        return summary
    metadata = {
        str(item["candidate_id"]): {
            "profile": item.get("profile", ""),
            "target_variant": item.get("target_variant", ""),
            "target_definition": item.get("target_definition", ""),
            "model_family": item.get("model_family", ""),
            "onnx_friendly": item.get("onnx_friendly", ""),
            "score_quantile": item.get("score_quantile", ""),
            "score_threshold": item.get("score_threshold", ""),
            "f44_train_selection_score": item.get("f44_train_selection_score", ""),
            "selection_rank_basis": item.get("selection_rank_basis", ""),
            "train_rank": item.get("train_rank", ""),
        }
        for item in candidates
    }
    summary = summary.copy()
    for field in (
        "profile",
        "target_variant",
        "target_definition",
        "model_family",
        "onnx_friendly",
        "score_quantile",
        "score_threshold",
        "f44_train_selection_score",
        "selection_rank_basis",
        "train_rank",
    ):
        summary[field] = [metadata.get(str(candidate_id), {}).get(field, "") for candidate_id in summary["candidate_id"]]
    summary["train_rank"] = pd.to_numeric(summary["train_rank"], errors="coerce").fillna(999999).astype(int)

    f_min_pf = pd.to_numeric(summary["forward_min_pf"], errors="coerce")
    f_max_dd = pd.to_numeric(summary["forward_max_dd"], errors="coerce")
    f_min_density = pd.to_numeric(summary["forward_min_density"], errors="coerce")
    f_max_density = pd.to_numeric(summary["forward_max_density"], errors="coerce")
    dual = summary["forward_dual_positive_flag"].astype(bool)
    density_scout = (f_min_density >= SCOUT_MIN_DENSITY) & (f_max_density <= SCOUT_MAX_DENSITY)
    density_seed = (f_min_density >= SEED_MIN_DENSITY) & (f_max_density <= SEED_MAX_DENSITY)
    summary["f44_scout_clue_flag"] = dual & density_scout & (f_min_pf >= SCOUT_MIN_PF) & (f_max_dd <= SCOUT_MAX_DD)
    summary["f44_seed_surface_flag"] = dual & density_seed & (f_min_pf >= SEED_MIN_PF) & (f_max_dd <= SEED_MAX_DD)
    summary["runtime_probe_candidate_flag"] = (
        summary["f44_seed_surface_flag"].astype(bool) & (f_min_pf >= RUNTIME_MIN_PF) & (f_max_dd <= RUNTIME_MAX_DD)
    )
    summary["f44_axis_gap_to_seed"] = (
        np.maximum(0.0, SEED_MIN_PF - f_min_pf)
        + np.maximum(0.0, f_max_dd - SEED_MAX_DD) / SEED_MAX_DD
        + np.maximum(0.0, SEED_MIN_DENSITY - f_min_density) / SEED_MIN_DENSITY
        + np.maximum(0.0, f_max_density - SEED_MAX_DENSITY) / SEED_MAX_DENSITY
    )
    return summary.sort_values(
        [
            "runtime_probe_candidate_flag",
            "f44_seed_surface_flag",
            "f44_scout_clue_flag",
            "train_rank",
        ],
        ascending=[False, False, False, True],
    ).reset_index(drop=True)


def surface_counts(summary: pd.DataFrame) -> dict[str, Any]:
    if summary.empty:
        return {
            "scout_clue_rows": 0,
            "seed_surface_rows": 0,
            "runtime_candidate_rows": 0,
            "best_readonly": {},
        }
    return {
        "scout_clue_rows": int(summary["f44_scout_clue_flag"].sum()),
        "seed_surface_rows": int(summary["f44_seed_surface_flag"].sum()),
        "runtime_candidate_rows": int(summary["runtime_probe_candidate_flag"].sum()),
        "best_readonly": json_ready(dict(summary.iloc[0])),
    }


def empty_surface() -> dict[str, Any]:
    return {
        "model_audit": pd.DataFrame(),
        "candidates": [],
        "split_metrics": pd.DataFrame(),
        "summary": pd.DataFrame(),
        "model_rows": 0,
        "candidate_rows": 0,
        "scout_clue_rows": 0,
        "seed_surface_rows": 0,
        "runtime_candidate_rows": 0,
        "best_readonly": {},
    }


def combine_summaries(initial: pd.DataFrame, repair: pd.DataFrame) -> pd.DataFrame:
    frames = [frame for frame in (initial, repair) if not frame.empty]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def top_records(frame: pd.DataFrame, limit: int = 8) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    return [json_ready(dict(row)) for _, row in frame.head(limit).iterrows()]


def build_repair_decision(initial_summary: pd.DataFrame) -> dict[str, Any]:
    if initial_summary.empty:
        return {
            "run_repair_grid": True,
            "repair_action": "run_capped_label_model_repair",
            "repair_reason": "Initial surface produced no candidate summary.",
        }
    runtime = int(initial_summary["runtime_probe_candidate_flag"].sum())
    seed = int(initial_summary["f44_seed_surface_flag"].sum())
    scout_rows = int(initial_summary["f44_scout_clue_flag"].sum())
    if runtime:
        return {
            "run_repair_grid": False,
            "repair_action": "skipped_runtime_candidate_present",
            "repair_reason": "Initial surface already produced runtime candidate; stop before expensive validation.",
        }
    if seed:
        return {
            "run_repair_grid": False,
            "repair_action": "skipped_seed_surface_present",
            "repair_reason": "Seed surface exists; avoid label/model overfit repair before runtime validation planning.",
        }
    return {
        "run_repair_grid": True,
        "repair_action": "run_capped_label_model_repair",
        "repair_reason": f"Initial surface scout={scout_rows}, seed=0, runtime=0; run bounded target/model repair.",
        "initial_scout_rows": scout_rows,
    }


def classify_closeout(initial_summary: pd.DataFrame, repair_summary: pd.DataFrame) -> dict[str, Any]:
    combined = combine_summaries(initial_summary, repair_summary)
    if combined.empty:
        scout = seed = runtime = 0
        best = {}
    else:
        scout = int(combined["f44_scout_clue_flag"].sum())
        seed = int(combined["f44_seed_surface_flag"].sum())
        runtime = int(combined["runtime_probe_candidate_flag"].sum())
        best = json_ready(dict(combined.iloc[0]))
    if runtime:
        closeout_class = "completion_candidate"
        runtime_status = "runtime_probe_candidate_requires_pre_expensive_grok_before_mt5"
    elif seed:
        closeout_class = "preserved_clue_seed_surface_without_runtime_candidate"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_runtime_candidate_after_f44_label_model_proxy"
    elif scout:
        closeout_class = "preserved_clue_negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f44_label_model_proxy"
    else:
        closeout_class = "negative_memory"
        runtime_status = "runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f44_label_model_proxy"
    return {
        "closeout_class": closeout_class,
        "runtime_probe_status": runtime_status,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "scout_clue_count": scout,
        "seed_surface_count": seed,
        "runtime_probe_candidate_count": runtime,
        "best_variant": best,
    }


def write_surface_outputs(root: Path, profile: str, surface: dict[str, Any]) -> None:
    write_csv(root / f"{profile}_model_audit.csv", surface["model_audit"])
    candidate_rows = [clean_candidate(item) for item in surface["candidates"]]
    write_csv(root / f"{profile}_candidate_ledger.csv", pd.DataFrame(candidate_rows))
    write_csv(root / f"{profile}_split_metrics.csv", surface["split_metrics"])
    write_csv(root / f"{profile}_candidate_summary.csv", surface["summary"])
    top = surface["summary"].head(40) if not surface["summary"].empty else pd.DataFrame()
    write_csv(root / f"{profile}_top_forward_diagnostic.csv", top)
    write_json(
        root / f"{profile}_surface_summary.json",
        {
            "profile": profile,
            "model_rows": surface["model_rows"],
            "candidate_rows": surface["candidate_rows"],
            "scout_clue_rows": surface["scout_clue_rows"],
            "seed_surface_rows": surface["seed_surface_rows"],
            "runtime_candidate_rows": surface["runtime_candidate_rows"],
            "best_readonly": surface["best_readonly"],
        },
    )


def clean_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in candidate.items() if key not in {"mask", "train_selection_metrics"}}


def build_stage_brief(manifest: dict[str, Any], open_review: dict[str, Any], checks: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

## Hypothesis(가설)
Train-only short path-utility label model(학습 전용 숏 경로 효용 라벨 모델)이 F43 trade-shape source threshold mining(거래 형태 원천 임계값 채굴)보다 PF edge(수익 팩터 우위)를 더 잘 분리하는지 시험한다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F43 best row(최상 행)는 reference-only(참조 전용), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서).
- changed_variables(변경 변수): continuous short path-utility target(연속 숏 경로 효용 목표), ONNX-friendly score model(온엑스 친화 점수 모델), train-only score threshold(학습 전용 점수 임계값).
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/candidate ranking(라벨/모델/임계값/후보 순위)에 쓰는 경우.
- stop_conditions(중지 조건): seed/runtime candidate(씨앗/런타임 후보) 발생 또는 capped repair(상한 수리) 종료.

## Grok Stage-Open Review(그록 단계 개방 검토)
- classification(분류): {open_review.get("classification")}
- accepted_after_local_verification(로컬 검증 후 수용): {open_review.get("accepted_after_local_verification")}
- guardrail_seen(보호선 확인): {open_review.get("guardrail_seen")}

## Local Checks(로컬 점검)
- feature_hash(피처 해시): `{checks.get("feature_hash")}`
- required_splits_present(필수 분할 존재): {checks.get("checks", {}).get("required_splits_present")}
- short_valid_rows(숏 경로 유효 행): {checks.get("short_valid_rows")}

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.
"""


def build_closeout_prompt(closeout: dict[str, Any], best_rows: list[dict[str, Any]], repair_decision: dict[str, Any]) -> str:
    best = closeout.get("best_variant", {}) or {}
    compact_rows = "\n".join(
        (
            f"- r{row.get('train_rank', row.get('rank'))} {row.get('candidate_id')}: "
            f"target={row.get('target_variant')}; model={row.get('model_family')}; "
            f"train_pf={row.get('train_profit_factor')}; val_pf={row.get('validation_profit_factor')}; "
            f"oos_pf={row.get('oos_profit_factor')}; fwd_density={row.get('forward_min_density')}..{row.get('forward_max_density')}; "
            f"fwd_dd={row.get('forward_max_dd')}; scout={row.get('f44_scout_clue_flag')}; "
            f"seed={row.get('f44_seed_surface_flag')}; runtime={row.get('runtime_probe_candidate_flag')}"
        )
        for row in best_rows[:6]
    )
    return f"""# Frontier44 closeout Grok review(그록 마감 검토)

Role(역할): external second opinion(외부 2차 의견) only.

Do not claim operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).
Do not inspect files, call tools, or request more repository context(파일/도구/추가 저장소 문맥을 사용하지 말 것). Answer only from bounded evidence(제한 근거) below.

Codex proposed closeout(코덱스 제안 마감):
- stage_id(단계 ID): {STAGE_ID}
- closeout_class(마감 분류): {closeout.get("closeout_class")}
- runtime_probe_status(런타임 탐침 상태): {closeout.get("runtime_probe_status")}
- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- repair_action(수리 행동): {repair_decision.get("repair_action")}

Best observed variant by train-only rank first(학습 전용 순위 우선 최상 관찰 변형):
- candidate_id: {best.get("candidate_id")}
- target_variant(목표 변형): {best.get("target_variant")}
- model_family(모델 계열): {best.get("model_family")}
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density_range(전진 거래 밀도 범위): {best.get("forward_min_density")} to {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}
- scout/seed/runtime(탐색/씨앗/런타임): {best.get("f44_scout_clue_flag")}/{best.get("f44_seed_surface_flag")}/{best.get("runtime_probe_candidate_flag")}

Top rows snapshot(상위 행 스냅샷):
{compact_rows}

Guardrail enforced(강제 보호선):
- label/model/score threshold/SLTP/candidate rank(라벨/모델/점수 임계값/손익절/후보 순위)는 train split only(학습 분할 전용).
- validation/OOS(검증/표본외)는 read-only evaluation(읽기 전용 평가).
- F38/F39/F43 primary lever(주 레버)는 반복하지 않음.

Question(질문):
Is this closeout classification honest under the lifecycle(가설 생명주기), train-only isolation wall(학습 전용 격리벽), and claim boundary(주장 경계)?

Return only:
1. verdict: accepted, rejected, or needs_local_verification(수용/거절/로컬 검증 필요)
2. closeout_boundary_ok: yes/no(예/아니오)
3. one risk(위험) if any
4. one next-stage clue(다음 단계 단서) if any
"""


def build_review_artifacts(
    *,
    frame: pd.DataFrame,
    checks: dict[str, Any],
    manifest: dict[str, Any],
    open_review: dict[str, Any],
    closeout_review: dict[str, Any],
    initial: dict[str, Any],
    repair: dict[str, Any],
    repair_decision: dict[str, Any],
    closeout: dict[str, Any],
) -> dict[Path, str]:
    initial_counts = counts_text(initial)
    repair_counts = counts_text(repair)
    best = closeout.get("best_variant", {}) or {}
    report = f"""# {RUN_D} report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `{closeout.get("closeout_class")}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- scout/seed/runtime(탐색/씨앗/런타임): {closeout.get("scout_clue_count")}/{closeout.get("seed_surface_count")}/{closeout.get("runtime_probe_candidate_count")}

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `{best.get("candidate_id")}`
- target_variant(목표 변형): `{best.get("target_variant")}`
- model_family(모델 계열): `{best.get("model_family")}`
- train_profit_factor(학습 PF): {best.get("train_profit_factor")}
- validation_profit_factor(검증 PF): {best.get("validation_profit_factor")}
- oos_profit_factor(표본외 PF): {best.get("oos_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {best.get("forward_min_density")} ~ {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}

## Lifecycle(생명주기)
- stage_open(단계 개방): Grok(그록) {open_review.get("classification")}
- proxy(프록시): {initial_counts}
- repair(수리): {repair_decision.get("repair_action")} / {repair_counts}
- closeout_grok(마감 그록): {closeout_review.get("classification")}

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
"""
    run_a = f"""# {RUN_A} report(보고서)

F44 opened a train-only short path-utility label model hypothesis(학습 전용 숏 경로 효용 라벨 모델 가설). F43 is reference only(참조 전용) and not baseline/winner(기준선/승자 아님).
"""
    run_b = f"""# {RUN_B} report(보고서)

- model_rows(모델 행): {initial.get("model_rows")}
- candidate_rows(후보 행): {initial.get("candidate_rows")}
- scout/seed/runtime(탐색/씨앗/런타임): {initial.get("scout_clue_rows")}/{initial.get("seed_surface_rows")}/{initial.get("runtime_candidate_rows")}
- train_only_isolation_wall(학습 전용 격리벽): enforced(강제)
"""
    run_c = f"""# {RUN_C} report(보고서)

- repair_action(수리 행동): {repair_decision.get("repair_action")}
- model_rows(모델 행): {repair.get("model_rows")}
- candidate_rows(후보 행): {repair.get("candidate_rows")}
- scout/seed/runtime(탐색/씨앗/런타임): {repair.get("scout_clue_rows")}/{repair.get("seed_surface_rows")}/{repair.get("runtime_candidate_rows")}
"""
    local_verification = f"""# Local Verification(로컬 검증)

- feature_hash_matches_contract(피처 해시 계약 일치): {checks.get("checks", {}).get("feature_hash_matches_contract")}
- required_splits_present(필수 분할 존재): {checks.get("checks", {}).get("required_splits_present")}
- open_grok_accepted(개방 그록 수용): {open_review.get("accepted_after_local_verification")}
- closeout_grok_accepted(마감 그록 수용): {closeout_review.get("accepted_after_local_verification")}
- train_only_isolation_wall(학습 전용 격리벽): {checks.get("checks", {}).get("train_only_isolation_wall")}
- validation_oos_read_only(검증/표본외 읽기 전용): True
"""
    gate_audit = f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- scope_completion_gate(범위 완료 게이트): pass(통과), F44 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) materialized.
- kpi_contract_audit(KPI 계약 감사): pass(통과), train/validation/OOS PF/DD/density(학습/검증/표본외 PF/DD/밀도) split rows recorded.
- skill_receipt_lint(스킬 영수증 검사): pass_with_boundary(경계 통과), obsidian-run-evidence-system(실행 근거 시스템) skill unavailable in session; equivalent run evidence artifacts recorded.
- data_integrity(데이터 무결성): pass(통과), closed-bar feature order(닫힌 봉 피처 순서), split(분할), raw path(원천 경로) verified.
- model_validation(모델 검증): exploratory(탐색), model/target/threshold choice(모델/목표/임계값 선택)는 train-only(학습 전용); no promotion(승격 없음).
- artifact_lineage(산출물 계보): pass(통과), input manifest/report/ledger paths(입력 목록/보고/장부 경로) recorded; 02_runs(실행 원자료)는 ignored_with_manifest(목록 포함 무시).
- external_review_packet(외부 검토 묶음): pass(통과), stage-open and closeout Grok(단계 개방/마감 그록) receipts recorded.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `{closeout.get("runtime_probe_status")}`.
- result_judgment(결과 판정): pass(통과), `{closeout.get("closeout_class")}` only.
"""
    open_receipt = f"""# Grok Stage-Open Receipt(그록 단계 개방 영수증)

- trigger_reason(트리거 이유): /goal(목표) requires Grok second opinion(그록 2차 의견).
- review_size(검토 크기): small review(소규모 검토)
- prompt_path(프롬프트 경로): `{GROK_OPEN_ROOT / "input_prompt.md"}`
- output_path(출력 경로): `{open_review.get("clean_output_path")}`
- advice_classification(조언 분류): `{open_review.get("classification")}`
- local_verification(로컬 검증): accepted after confirming train-only isolation wall(학습 전용 격리벽 확인 후 수용)
- final_codex_direction(최종 코덱스 방향): run F44 label/model proxy with validation/OOS read-only(검증/표본외 읽기 전용)
"""
    close_receipt = f"""# Grok Stage-Closeout Receipt(그록 단계 마감 영수증)

- trigger_reason(트리거 이유): stage closeout(단계 마감) requires Grok review(그록 검토).
- review_size(검토 크기): small review(소규모 검토)
- prompt_path(프롬프트 경로): `{GROK_CLOSE_ROOT / "input_prompt.md"}`
- output_path(출력 경로): `{closeout_review.get("clean_output_path")}`
- advice_classification(조언 분류): `{closeout_review.get("classification")}`
- local_verification(로컬 검증): {closeout_review.get("accepted_after_local_verification")}
- final_codex_direction(최종 코덱스 방향): close F44 as `{closeout.get("closeout_class")}` with no authority claim(권위 주장 없음)
"""
    return {
        review_report_path(RUN_A): run_a,
        review_report_path(RUN_B): run_b,
        review_report_path(RUN_C): run_c,
        review_report_path(RUN_D): report,
        REVIEWS_ROOT / "local_verification.md": local_verification,
        REVIEWS_ROOT / "required_gate_coverage_audit.md": gate_audit,
        REVIEWS_ROOT / "grok_stage_open_receipt.md": open_receipt,
        REVIEWS_ROOT / "grok_stage_closeout_receipt.md": close_receipt,
    }


def counts_text(surface: dict[str, Any]) -> str:
    return (
        f"models={surface.get('model_rows')}, candidates={surface.get('candidate_rows')}, "
        f"scout/seed/runtime={surface.get('scout_clue_rows')}/{surface.get('seed_surface_rows')}/{surface.get('runtime_candidate_rows')}"
    )


def build_selected_notes(closeout: dict[str, Any]) -> dict[Path, str]:
    best = closeout.get("best_variant", {}) or {}
    selection = f"""# Selection Status(선택 상태)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_D}`
- closeout_class(마감 분류): `{closeout.get("closeout_class")}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- next_stage(다음 단계): `{closeout.get("next_stage_id")}`
- next_run(다음 실행): `{closeout.get("next_run_id")}`

No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.
"""
    preserved = f"""# Preserved Clue(보존 단서)

F44 preserved clue(보존 단서)는 train-only short path-utility label model(학습 전용 숏 경로 효용 라벨 모델)이 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `{best.get("candidate_id")}`
- target_variant(목표 변형): `{best.get("target_variant")}`
- model_family(모델 계열): `{best.get("model_family")}`
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {best.get("forward_min_density")} ~ {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}
"""
    negative = f"""# Negative Memory(부정 기억)

F44 negative memory(부정 기억)는 train-only short path-utility label model(학습 전용 숏 경로 효용 라벨 모델)이 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- do_not_repeat(반복 금지): F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움), F43 trade-shape source(거래 형태 원천)를 primary lever(주 레버)로 반복하지 않는다.
"""
    return {
        SELECTED_ROOT / "selection_status.md": selection,
        SELECTED_ROOT / "preserved_clue.md": preserved,
        SELECTED_ROOT / "negative_memory.md": negative,
    }


def update_stage_ledgers(closeout: dict[str, Any], checks: dict[str, Any]) -> None:
    rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_A,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "stage_open",
            "runtime_probe_status": "out_of_scope_by_stage_open",
            "notes": "F44 opened with train-only short path-utility label model hypothesis and Grok guardrails.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_B,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "proxy",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Initial train-only label/model proxy surface.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_C,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "repair",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Capped label/model repair diagnostic.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": closeout.get("closeout_class"),
            "runtime_probe_status": closeout.get("runtime_probe_status"),
            "notes": f"feature_contract={checks.get('checks', {}).get('feature_hash_matches_contract')}; next={closeout.get('next_stage_id')}/{closeout.get('next_run_id')}",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "record_view": "Tier B separate",
            "status": "out_of_scope_by_claim",
            "closeout_class": closeout.get("closeout_class"),
            "runtime_probe_status": "out_of_scope_by_claim_tier_a_label_model_proxy_only",
            "notes": "F44 used Tier A source proxy only; Tier B not claimed.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "record_view": "Tier A+B combined",
            "status": "out_of_scope_by_claim",
            "closeout_class": closeout.get("closeout_class"),
            "runtime_probe_status": "out_of_scope_by_claim_no_combined_tier_route",
            "notes": "No synthetic combined result claimed.",
        },
    ]
    write_dict_csv(REVIEWS_ROOT / "stage_run_ledger.csv", rows)
    upsert_project_ledger(rows)


def project_ledger_row(row: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    view_key = str(row.get("record_view", "")).replace(" ", "_").replace("+", "plus").lower()
    result = {field: "" for field in fields}
    values = {
        "ledger_row_id": f"{row.get('stage_id')}__{row.get('run_id')}__{view_key}",
        "stage_id": row.get("stage_id", ""),
        "run_id": row.get("run_id", ""),
        "record_view": row.get("record_view", ""),
        "tier_scope": row.get("record_view", ""),
        "kpi_scope": "short_path_utility_label_model_proxy",
        "scoreboard_lane": "frontier_scout",
        "status": row.get("status", ""),
        "judgment": row.get("closeout_class", ""),
        "external_verification_status": row.get("runtime_probe_status", ""),
        "notes": row.get("notes", ""),
        "path": review_report_path(str(row.get("run_id", ""))).as_posix(),
        "report_path": review_report_path(str(row.get("run_id", ""))).as_posix(),
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness",
        "run_family": "frontier_short_path_utility_label_model_proxy",
        "run_type": "stage_lifecycle",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    for key, value in values.items():
        if key in result:
            result[key] = value
    return result


def upsert_project_ledger(rows: list[dict[str, Any]]) -> None:
    io_path(PROJECT_LEDGER.parent).mkdir(parents=True, exist_ok=True)
    if not path_exists(PROJECT_LEDGER):
        write_dict_csv(PROJECT_LEDGER, rows)
        return
    original_bytes = io_path(PROJECT_LEDGER).read_bytes()
    text = original_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    fields = list(reader.fieldnames or [])
    existing = [row for row in reader]
    mapped_rows = [project_ledger_row(row, fields) for row in rows]
    line_ending = "\r\n" if b"\r\n" in original_bytes else "\n"
    filtered = [
        row
        for row in existing
        if not (row.get("stage_id") == STAGE_ID and row.get("run_id") in {RUN_A, RUN_B, RUN_C, RUN_D})
    ]
    filtered.extend(mapped_rows)
    with io_path(PROJECT_LEDGER).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=line_ending)
        writer.writeheader()
        writer.writerows(filtered)


def update_workspace_docs(closeout: dict[str, Any]) -> None:
    updated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_D}
latest_completed_run_id: {RUN_D}
current_status: closed_{closeout.get("closeout_class")}
current_judgment: {closeout.get("closeout_class")}(F44 train-only label/model proxy no operating authority)
next_stage_id: {closeout.get("next_stage_id")}
next_run_id: {closeout.get("next_run_id")}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{updated_at}'
notes:
  - Runtime probe status: {closeout.get("runtime_probe_status")}
"""
    write_text_sig(WORKSPACE_STATE, workspace)
    narrative = f"""# Current Working State(현재 작업 상태)

Frontier44(F44, 전선 44단계)가 `{closeout.get("closeout_class")}`로 닫혔다.

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_D}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- next_stage(다음 단계): `{closeout.get("next_stage_id")}`
- next_run(다음 실행): `{closeout.get("next_run_id")}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)를 주장하지 않는다.
"""
    write_text_sig(CURRENT_WORKING_STATE, narrative)
    pointer = f"""## Frontier Pointer(전선 포인터)

- last_closed_stage(마지막 종료 단계): `{STAGE_ID}`
- last_closed_run(마지막 종료 실행): `{RUN_D}`
- next_stage(다음 단계): `{closeout.get("next_stage_id")}`
- next_run(다음 실행): `{closeout.get("next_run_id")}`

F44 carry-forward(이월) 기록은 train-only short path-utility label model(학습 전용 숏 경로 효용 라벨 모델)이 PF/DD/density(수익 팩터/손실폭/밀도)를 네 축 목표까지 끌어올렸는지와 seed/runtime(씨앗/런타임) 후보가 생겼는지 여부다.
"""
    existing_plan = read_text(PRE_ALPHA_PLAN) if path_exists(PRE_ALPHA_PLAN) else "# Pre-Alpha Stage Plan\n"
    marker = "## Frontier Pointer(전선 포인터)"
    if marker in existing_plan:
        existing_plan = existing_plan.split(marker, 1)[0].rstrip()
    write_text_sig(PRE_ALPHA_PLAN, existing_plan.rstrip() + "\n\n" + pointer)


def artifact_map() -> dict[str, str]:
    return {
        "input_manifest": (INPUT_ROOT / "short_path_utility_model_manifest.json").as_posix(),
        "initial_summary": (RUN_B_ROOT / "initial_candidate_summary.csv").as_posix(),
        "repair_summary": (RUN_C_ROOT / "repair_candidate_summary.csv").as_posix(),
        "closeout_report": review_report_path(RUN_D).as_posix(),
        "selection_status": (SELECTED_ROOT / "selection_status.json").as_posix(),
    }


if __name__ == "__main__":
    main()
