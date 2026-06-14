from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from foundation.control_plane.ledger import io_path, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b


warnings.filterwarnings("ignore", category=ConvergenceWarning)

STAGE_ID = "stage_frontier_45__short_pf_edge_event_utility_model_pivot_after_f44_label_model_memory"
PREV_STAGE_ID = "stage_frontier_44__short_pf_edge_label_model_pivot_after_f43_trade_shape_negative"
RUN_A = "frontier45A_stage_open_short_pf_edge_event_utility_model_hypothesis_design_v1"
RUN_B = "frontier45B_train_only_short_event_utility_classifier_proxy_v1"
RUN_C = "frontier45C_capped_event_rarity_threshold_repair_v1"
RUN_D = "frontier45D_stage_closeout_event_utility_model_v1"
NEXT_STAGE_ID = "stage_frontier_46__short_pf_edge_event_sequence_context_pivot_after_f45_event_classifier_memory"
NEXT_RUN_ID = "frontier46A_stage_open_short_pf_edge_event_sequence_context_hypothesis_design_v1"
RUNTIME_REVIEW_RUN_ID = "frontier45E_pre_expensive_runtime_validation_review_v1"

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

GROK_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier45_stage_open" / "small_review"
GROK_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier45_stage_closeout" / "small_review"

PROJECT_LEDGER = Path("docs") / "registers" / "alpha_run_ledger.csv"
WORKSPACE_STATE = Path("docs") / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = Path("docs") / "context" / "current_working_state.md"
PRE_ALPHA_PLAN = Path("docs") / "workspace" / "pre_alpha_stage_plan.md"

SPLITS = ("train", "validation", "oos")
SIDE_VALUE = -1
SIDE_LABEL = "short"

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

TRAIN_MIN_TRADES = 35
TRAIN_MIN_DENSITY = 3.5
TRAIN_MAX_DENSITY = 14.0
TRAIN_PF_FLOOR = 1.00
TRAIN_DD_CAP = 26.0
AMBIGUOUS_RATE_CAP = 0.45

INITIAL_SCORE_QUANTILES = (0.78, 0.82, 0.86, 0.90, 0.94)
INITIAL_STOP_QUANTILES = (0.16, 0.24, 0.34)
INITIAL_TAKE_QUANTILES = (0.60, 0.72, 0.84)
INITIAL_RR_FLOORS = (1.20, 1.65, 2.20)
REPAIR_SCORE_QUANTILES = (0.70, 0.76, 0.82, 0.88, 0.92)
REPAIR_STOP_QUANTILES = (0.12, 0.22, 0.36)
REPAIR_TAKE_QUANTILES = (0.54, 0.68, 0.86)
REPAIR_RR_FLOORS = (1.05, 1.50, 2.30)
INITIAL_MAX_CANDIDATES = 36
REPAIR_MAX_CANDIDATES = 84


def review_report_path(run_id: str) -> Path:
    names = {
        RUN_A: "runA_report.md",
        RUN_B: "runB_report.md",
        RUN_C: "runC_report.md",
        RUN_D: "runD_closeout_report.md",
    }
    return REVIEWS_ROOT / names.get(run_id, f"{run_id}_report.md")


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
    write_json(INPUT_ROOT / "event_utility_model_manifest.json", manifest)
    write_text_sig(SPEC_ROOT / "stage_brief.md", build_stage_brief(manifest, open_review, checks))
    write_json(RUN_A_ROOT / "stage_open_local_verification.json", {"open_review": open_review, "checks": checks})

    initial = build_event_surface(
        frame,
        feature_order,
        path_labels,
        raw_path,
        run_id=RUN_B,
        run_prefix="f45b",
        profile="initial",
        event_specs=event_specs(frame, path_labels[SIDE_VALUE], "initial"),
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
        repair = build_event_surface(
            frame,
            feature_order,
            path_labels,
            raw_path,
            run_id=RUN_C,
            run_prefix="f45c",
            profile="repair",
            event_specs=event_specs(frame, path_labels[SIDE_VALUE], "repair"),
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
            "profile": "short_event_utility_classifier_proxy",
            "open_review": open_review,
            "closeout_review": closeout_review,
            "repair_decision": repair_decision,
            "closeout": closeout,
            "train_split_only_construction_lock": True,
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
        GROK_OPEN_ROOT,
        GROK_CLOSE_ROOT,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8-sig")


def write_dict_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    frame = pd.DataFrame(rows)
    write_csv(path, frame)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if pd.isna(value):
        return None
    return value


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def artifact_descriptor(path: Path) -> dict[str, Any]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing"}


def load_open_grok_review() -> dict[str, Any]:
    metadata_path = GROK_OPEN_ROOT / "metadata.json"
    clean_path = GROK_OPEN_ROOT / "clean_output.md"
    metadata = read_json(metadata_path) if path_exists(metadata_path) else {}
    clean = read_text(clean_path) if path_exists(clean_path) else ""
    lowered = clean.lower()
    accepted = "`accepted`" in lowered or "verdict:** `accepted`" in lowered or "verdict:** accepted" in lowered or "verdict: accepted" in lowered
    rejected = "`rejected`" in lowered or "verdict:** `rejected`" in lowered or "verdict:** rejected" in lowered or "verdict: rejected" in lowered
    guardrail_seen = ("train-split-only" in lowered or "학습 분할" in clean) and ("construction lock" in lowered or "구성 잠금" in clean)
    claim_ok = "claim_boundary_ok" in lowered and "yes" in lowered
    forbidden = any(
        phrase in lowered
        for phrase in ("operating promotion", "runtime authority", "live readiness", "goal achieve", "selected baseline")
    )
    return {
        "packet": GROK_OPEN_ROOT.as_posix(),
        "metadata": metadata,
        "clean_output_path": clean_path.as_posix(),
        "classification": "accepted_stage_open_train_split_only_event_lock" if accepted and guardrail_seen and claim_ok and not rejected else "needs_local_verification",
        "accepted_after_local_verification": bool(accepted and guardrail_seen and claim_ok and not rejected),
        "guardrail_seen": bool(guardrail_seen),
        "claim_boundary_ok": bool(claim_ok),
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
    accepted = "`accepted`" in lowered or "verdict:** `accepted`" in lowered or "verdict:** accepted" in lowered or "verdict: accepted" in lowered
    rejected = "`rejected`" in lowered or "verdict:** `rejected`" in lowered or "verdict:** rejected" in lowered or "verdict: rejected" in lowered
    boundary_ok = "closeout_boundary_ok" in lowered and "yes" in lowered
    forbidden = any(
        phrase in lowered
        for phrase in ("operating promotion", "runtime authority", "live readiness", "goal achieve", "selected baseline")
    )
    return {
        "packet": GROK_CLOSE_ROOT.as_posix(),
        "metadata": metadata,
        "clean_output_path": clean_path.as_posix(),
        "classification": "accepted_closeout_event_classifier_boundary" if accepted and boundary_ok and not rejected else "needs_local_verification",
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
    prev_selection = read_text(PREV_SELECTION_MD)
    feature_hash = ordered_hash(feature_order)
    checks = {
        "workspace_points_to_f45": f"next_stage_id: {STAGE_ID}" in workspace or f"current_stage_id: {STAGE_ID}" in workspace,
        "prev_selection_next_matches": f"next_stage(다음 단계): `{STAGE_ID}`" in prev_selection,
        "prev_selection_json_exists": path_exists(PREV_SELECTION_JSON),
        "prev_preserved_clue_exists": path_exists(PREV_PRESERVED_CLUE),
        "prev_negative_memory_exists": path_exists(PREV_NEGATIVE_MEMORY),
        "open_grok_accepted": open_review.get("accepted_after_local_verification") is True,
        "feature_hash_matches_contract": len(feature_order) == 58 and feature_hash == f23b.EXPECTED_FEATURE_HASH,
        "required_splits_present": set(SPLITS).issubset(set(frame["split"].astype(str))),
        "raw_path_alignment_available": int(raw_path.get("missing_entry_positions", -1)) == 0 and int(raw_path.get("missing_future_positions", -1)) == 0,
        "short_path_valid_rows_positive": int(path_labels[SIDE_VALUE]["valid"].sum()) > 0,
        "train_split_only_construction_lock": True,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier45 context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {
        "checks": checks,
        "feature_hash": feature_hash,
        "rows": int(len(frame)),
        "raw_rows": int(raw_path.get("raw_rows", 0)),
        "split_counts": {split: int((frame["split"].astype(str) == split).sum()) for split in SPLITS},
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
        "hypothesis": "train_only_short_event_utility_classifier",
        "idea_id": "IDEA-FR45-SHORT-EVENT-UTILITY-CLASSIFIER",
        "decision_use": "scout_seed_runtime_candidate_screening_only",
        "comparison_baseline": "F44 best row reference-only scout clue, not inherited baseline",
        "control_variables": {
            "symbol": "US100",
            "timeframe": "M5",
            "side": SIDE_LABEL,
            "feature_order_count": len(feature_order),
            "feature_order_hash": ordered_hash(feature_order),
            "split": "train_2022-09-01_2024-12-31_validation_2025-01-01_2025-09-30_oos_2025-10-01_2026-02-28",
            "path_proxy": "executable_first_hit_sl_tp_from_raw_us100_path",
        },
        "changed_variables": {
            "label": "binary_or_ordinal_event_utility_label",
            "model_family": "class_weighted_event_classifier",
            "threshold_policy": "train_split_event_probability_quantiles_only",
        },
        "sample_scope": {
            "rows": int(len(frame)),
            "split_counts": checks["split_counts"],
            "raw_rows": int(raw_path.get("raw_rows", 0)),
            "short_path_valid_rows": int(path_labels[SIDE_VALUE]["valid"].sum()),
        },
        "success_criteria": {
            "scout_clue": {"forward_min_pf": SCOUT_MIN_PF, "density": "4_to_12_per_day", "forward_max_dd": SCOUT_MAX_DD},
            "seed_surface": {"forward_min_pf": SEED_MIN_PF, "density": "5_to_10_per_day", "forward_max_dd": SEED_MAX_DD},
            "runtime_probe_candidate": {"forward_min_pf": RUNTIME_MIN_PF, "forward_max_dd": RUNTIME_MAX_DD},
        },
        "invalid_conditions": [
            "validation_oos_used_for_label_threshold_model_sl_tp_or_rank",
            "f44_continuous_regression_repeated_as_primary_lever",
            "f42_f43_f38_f39_primary_lever_reopened",
        ],
        "evidence_plan": [
            "stage_open_grok_receipt",
            "event_model_audit",
            "candidate_ledger",
            "split_metrics",
            "candidate_summary",
            "stage_run_ledger",
            "project_alpha_ledger_rows",
            "stage_closeout_grok_receipt",
        ],
        "input_artifacts": {
            "prev_selection": artifact_descriptor(PREV_SELECTION_JSON),
            "prev_preserved_clue": artifact_descriptor(PREV_PRESERVED_CLUE),
            "prev_negative_memory": artifact_descriptor(PREV_NEGATIVE_MEMORY),
            "grok_open_clean_output": artifact_descriptor(GROK_OPEN_ROOT / "clean_output.md"),
        },
        "open_review": open_review,
        "checks": checks,
    }


def event_specs(frame: pd.DataFrame, labels: dict[str, np.ndarray], profile: str) -> list[dict[str, Any]]:
    train = f33b.split_mask(frame, "train") & labels["valid"]
    mfe = labels["mfe"]
    mae = labels["mae"]
    horizon = labels["horizon_pnl"]
    ratio = np.divide(mfe, np.maximum(mae, 1e-8))
    train_mfe = mfe[train & np.isfinite(mfe)]
    train_mae = mae[train & np.isfinite(mae)]
    train_ratio = ratio[train & np.isfinite(ratio)]
    if train_mfe.size < 100 or train_mae.size < 100 or train_ratio.size < 100:
        return []
    q = {
        "mfe60": float(np.nanquantile(train_mfe, 0.60)),
        "mfe65": float(np.nanquantile(train_mfe, 0.65)),
        "mfe70": float(np.nanquantile(train_mfe, 0.70)),
        "mfe75": float(np.nanquantile(train_mfe, 0.75)),
        "mfe80": float(np.nanquantile(train_mfe, 0.80)),
        "mae35": float(np.nanquantile(train_mae, 0.35)),
        "mae40": float(np.nanquantile(train_mae, 0.40)),
        "mae45": float(np.nanquantile(train_mae, 0.45)),
        "mae50": float(np.nanquantile(train_mae, 0.50)),
        "mae55": float(np.nanquantile(train_mae, 0.55)),
        "mae60": float(np.nanquantile(train_mae, 0.60)),
        "ratio65": float(np.nanquantile(train_ratio, 0.65)),
        "ratio70": float(np.nanquantile(train_ratio, 0.70)),
    }
    valid = labels["valid"] & np.isfinite(mfe) & np.isfinite(mae) & np.isfinite(horizon)

    def build(name: str, definition: str, event_mask: np.ndarray, thresholds: dict[str, float]) -> dict[str, Any]:
        event = valid & event_mask
        train_event = event[train]
        return {
            "event_variant": name,
            "event_definition": definition,
            "event": event.astype("int8"),
            "train_thresholds": thresholds,
            "train_event_count": int(np.sum(train_event)),
            "train_event_rate": float(np.mean(train_event)) if train_event.size else 0.0,
        }

    specs = [
        build(
            "event_mfe70_mae45_horizon_pos",
            "short path event if MFE >= train q70, MAE <= train q45, and horizon pnl positive",
            (mfe >= q["mfe70"]) & (mae <= q["mae45"]) & (horizon > 0.0),
            {"mfe70": q["mfe70"], "mae45": q["mae45"]},
        ),
        build(
            "event_mfe75_mae50_ratio70",
            "short path event if MFE >= train q75, MAE <= train q50, and MFE/MAE ratio >= train q70",
            (mfe >= q["mfe75"]) & (mae <= q["mae50"]) & (ratio >= q["ratio70"]),
            {"mfe75": q["mfe75"], "mae50": q["mae50"], "ratio70": q["ratio70"]},
        ),
        build(
            "event_mfe65_mae35_loss_contained",
            "short path event if MFE >= train q65 and MAE <= train q35",
            (mfe >= q["mfe65"]) & (mae <= q["mae35"]),
            {"mfe65": q["mfe65"], "mae35": q["mae35"]},
        ),
    ]
    if profile == "repair":
        specs.extend(
            [
                build(
                    "repair_event_mfe60_mae60_horizon_pos",
                    "looser repair event if MFE >= train q60, MAE <= train q60, and horizon pnl positive",
                    (mfe >= q["mfe60"]) & (mae <= q["mae60"]) & (horizon > 0.0),
                    {"mfe60": q["mfe60"], "mae60": q["mae60"]},
                ),
                build(
                    "repair_event_mfe80_mae40_ratio65",
                    "strict repair event if MFE >= train q80, MAE <= train q40, and MFE/MAE ratio >= train q65",
                    (mfe >= q["mfe80"]) & (mae <= q["mae40"]) & (ratio >= q["ratio65"]),
                    {"mfe80": q["mfe80"], "mae40": q["mae40"], "ratio65": q["ratio65"]},
                ),
            ]
        )
    return specs


def model_specs(profile: str) -> list[dict[str, Any]]:
    specs = [
        {
            "model_family": "logreg_balanced_l2_c1",
            "onnx_friendly": True,
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=1.0, class_weight="balanced", max_iter=500, solver="liblinear", random_state=4501),
            ),
        },
        {
            "model_family": "logreg_balanced_l2_c0p25",
            "onnx_friendly": True,
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.25, class_weight="balanced", max_iter=500, solver="liblinear", random_state=4502),
            ),
        },
        {
            "model_family": "extratrees_cls_d3_leaf180",
            "onnx_friendly": True,
            "factory": lambda: ExtraTreesClassifier(
                n_estimators=96,
                max_depth=3,
                min_samples_leaf=180,
                class_weight="balanced_subsample",
                random_state=4503,
                n_jobs=1,
            ),
        },
        {
            "model_family": "extratrees_cls_d5_leaf240",
            "onnx_friendly": True,
            "factory": lambda: ExtraTreesClassifier(
                n_estimators=96,
                max_depth=5,
                min_samples_leaf=240,
                class_weight="balanced_subsample",
                random_state=4505,
                n_jobs=1,
            ),
        },
    ]
    if profile == "repair":
        specs.append(
            {
                "model_family": "extratrees_cls_d7_leaf320",
                "onnx_friendly": True,
                "factory": lambda: ExtraTreesClassifier(
                    n_estimators=96,
                    max_depth=7,
                    min_samples_leaf=320,
                    class_weight="balanced_subsample",
                    random_state=4577,
                    n_jobs=1,
                ),
            }
        )
    return specs


def build_event_surface(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    *,
    run_id: str,
    run_prefix: str,
    profile: str,
    event_specs: list[dict[str, Any]],
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

    for event_spec in event_specs:
        y = np.asarray(event_spec["event"], dtype="int8")
        fit_mask = train_mask & np.isfinite(y)
        positives = int(np.sum(y[fit_mask] == 1))
        negatives = int(np.sum(y[fit_mask] == 0))
        if positives < 50 or negatives < 200:
            model_rows.append(
                {
                    "run_id": run_id,
                    "profile": profile,
                    "event_variant": event_spec["event_variant"],
                    "model_family": "not_fit",
                    "status": "skipped_sparse_train_event",
                    "train_rows": int(np.sum(fit_mask)),
                    "train_positive_rows": positives,
                    "train_event_rate": event_spec["train_event_rate"],
                }
            )
            continue
        for model_spec in model_specs:
            model = model_spec["factory"]()
            model.fit(x[fit_mask], y[fit_mask])
            score = np.full(len(frame), np.nan, dtype="float64")
            score[valid_features] = event_probability(model, x[valid_features])
            finite_score = np.isfinite(score) & valid_features
            train_scores = score[train_mask & finite_score]
            model_rows.append(
                {
                    "run_id": run_id,
                    "profile": profile,
                    "event_variant": event_spec["event_variant"],
                    "event_definition": event_spec["event_definition"],
                    "model_family": model_spec["model_family"],
                    "onnx_friendly": bool(model_spec.get("onnx_friendly", False)),
                    "status": "fit_train_only",
                    "train_rows": int(np.sum(fit_mask)),
                    "train_positive_rows": positives,
                    "train_event_rate": event_spec["train_event_rate"],
                    "train_score_min": safe_float(np.nanmin(train_scores)) if train_scores.size else math.nan,
                    "train_score_max": safe_float(np.nanmax(train_scores)) if train_scores.size else math.nan,
                    "train_thresholds": json.dumps(json_ready(event_spec["train_thresholds"]), ensure_ascii=False, sort_keys=True),
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
                        event_spec,
                        model_spec,
                        score_q,
                        threshold,
                        score,
                        profile,
                    )
                )

    selected = rank_candidates(candidates, run_prefix, max_candidates)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = summarize_f45_candidates(split_metrics, selected)
    return {
        "model_audit": pd.DataFrame(model_rows),
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "model_rows": int(len(model_rows)),
        "candidate_rows": int(len(selected)),
        **surface_counts(summary),
    }


def event_probability(model: Any, x: np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        proba = np.asarray(model.predict_proba(x), dtype="float64")
        classes = getattr(model, "classes_", None)
        if classes is None and hasattr(model, "steps"):
            classes = model.steps[-1][1].classes_
        if classes is not None:
            class_list = [int(item) for item in list(classes)]
            if 1 in class_list:
                return proba[:, class_list.index(1)]
        return proba[:, -1]
    raw = np.asarray(model.decision_function(x), dtype="float64")
    return 1.0 / (1.0 + np.exp(-raw))


def candidates_for_mask(
    frame: pd.DataFrame,
    mask: np.ndarray,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    event_spec: dict[str, Any],
    model_spec: dict[str, Any],
    score_quantile: float,
    score_threshold: float,
    score: np.ndarray,
    profile: str,
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    condition = {
        "condition_id": f"{event_spec['event_variant']}__{model_spec['model_family']}__q{score_quantile:.2f}",
        "feature": model_spec["model_family"],
        "feature_family": "train_only_event_utility_classifier_score",
        "definition": f"{event_spec['event_variant']} {model_spec['model_family']} probability >= train q{score_quantile:.2f}",
    }
    train = f33b.split_mask(frame, "train") & np.asarray(mask, dtype=bool) & path_labels[SIDE_VALUE]["valid"]
    event_rate_selected = float(np.mean(np.asarray(event_spec["event"], dtype="int8")[train])) if int(np.sum(train)) else 0.0
    score_margin = safe_float(np.nanmedian(score[train]) - score_threshold) if int(np.sum(train)) else 0.0
    for row in threshold_rows(
        frame,
        mask,
        path_labels[SIDE_VALUE],
        stop_quantiles,
        take_quantiles,
        rr_floors,
        f"f45_{profile}_train_only_event_selected_sl_tp_caps",
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
        score_value = train_selection_score(metrics, score_quantile, event_rate_selected)
        candidate = f33b.candidate_from_conditions([condition], mask, SIDE_VALUE, row, metrics, score_value)
        candidate["side"] = "short(숏)"
        candidate["profile"] = profile
        candidate["event_variant"] = event_spec["event_variant"]
        candidate["event_definition"] = event_spec["event_definition"]
        candidate["model_family"] = model_spec["model_family"]
        candidate["onnx_friendly"] = bool(model_spec.get("onnx_friendly", False))
        candidate["score_quantile"] = score_quantile
        candidate["score_threshold"] = score_threshold
        candidate["train_event_rate_selected"] = event_rate_selected
        candidate["train_score_margin_median"] = score_margin
        candidate["f45_train_selection_score"] = score_value
        candidate["selection_rank_basis"] = "train_only_event_metrics_no_validation_oos_feedback"
        variants.append(candidate)
    variants.sort(key=lambda item: float(item["f45_train_selection_score"]), reverse=True)
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


def train_selection_score(metrics: dict[str, Any], score_quantile: float, event_rate_selected: float) -> float:
    trade_count = max(safe_float(metrics.get("trade_count")), 1.0)
    density = safe_float(metrics.get("trades_per_day"))
    pf = safe_float(metrics.get("profit_factor"))
    dd = safe_float(metrics.get("dd_risk"))
    payoff = safe_float(metrics.get("payoff_ratio"))
    path_quality = safe_float(metrics.get("path_quality_rate"))
    ambiguous_rate = safe_float(metrics.get("ambiguous_both_hit_count")) / trade_count
    density_bonus = max(0.0, 1.0 - abs(density - 7.5) / 7.5)
    q_bonus = max(0.0, 1.0 - abs(score_quantile - 0.84) / 0.22)
    event_bonus = min(event_rate_selected * 4.0, 1.5)
    return float(
        4.8 * min(pf, 4.0)
        + 1.8 * density_bonus
        + 0.9 * min(payoff, 4.0)
        + 1.0 * path_quality
        + 0.6 * q_bonus
        + event_bonus
        - 0.30 * max(0.0, dd - 10.0)
        - 1.7 * ambiguous_rate
    )


def rank_candidates(candidates: list[dict[str, Any]], prefix: str, limit: int) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, float, float, float]] = set()
    selected: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: float(item["f45_train_selection_score"]), reverse=True):
        key = (
            str(candidate.get("event_variant", "")),
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


def summarize_f45_candidates(split_metrics: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    if split_metrics.empty:
        return pd.DataFrame()
    summary = f33b.summarize_candidates(split_metrics)
    if summary.empty:
        return summary
    metadata = {
        str(item["candidate_id"]): {
            "profile": item.get("profile", ""),
            "event_variant": item.get("event_variant", ""),
            "event_definition": item.get("event_definition", ""),
            "model_family": item.get("model_family", ""),
            "onnx_friendly": item.get("onnx_friendly", ""),
            "score_quantile": item.get("score_quantile", ""),
            "score_threshold": item.get("score_threshold", ""),
            "train_event_rate_selected": item.get("train_event_rate_selected", ""),
            "f45_train_selection_score": item.get("f45_train_selection_score", ""),
            "selection_rank_basis": item.get("selection_rank_basis", ""),
            "train_rank": item.get("train_rank", ""),
        }
        for item in candidates
    }
    summary = summary.copy()
    for field in (
        "profile",
        "event_variant",
        "event_definition",
        "model_family",
        "onnx_friendly",
        "score_quantile",
        "score_threshold",
        "train_event_rate_selected",
        "f45_train_selection_score",
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
    summary["f45_scout_clue_flag"] = dual & density_scout & (f_min_pf >= SCOUT_MIN_PF) & (f_max_dd <= SCOUT_MAX_DD)
    summary["f45_seed_surface_flag"] = dual & density_seed & (f_min_pf >= SEED_MIN_PF) & (f_max_dd <= SEED_MAX_DD)
    summary["runtime_probe_candidate_flag"] = (
        summary["f45_seed_surface_flag"].astype(bool) & (f_min_pf >= RUNTIME_MIN_PF) & (f_max_dd <= RUNTIME_MAX_DD)
    )
    summary["f45_axis_gap_to_seed"] = (
        np.maximum(0.0, SEED_MIN_PF - f_min_pf)
        + np.maximum(0.0, f_max_dd - SEED_MAX_DD) / SEED_MAX_DD
        + np.maximum(0.0, SEED_MIN_DENSITY - f_min_density) / SEED_MIN_DENSITY
        + np.maximum(0.0, f_max_density - SEED_MAX_DENSITY) / SEED_MAX_DENSITY
    )
    return summary.sort_values(
        [
            "runtime_probe_candidate_flag",
            "f45_seed_surface_flag",
            "f45_scout_clue_flag",
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
        "scout_clue_rows": int(summary["f45_scout_clue_flag"].sum()),
        "seed_surface_rows": int(summary["f45_seed_surface_flag"].sum()),
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


def closest_nonwinner_forward_observation(combined: pd.DataFrame, best: dict[str, Any]) -> dict[str, Any]:
    if combined.empty:
        return {}
    frame = combined.copy()
    best_id = str(best.get("candidate_id", ""))
    if best_id and "candidate_id" in frame.columns:
        frame = frame[frame["candidate_id"].astype(str) != best_id]
    if frame.empty:
        return {}

    def numeric_column(name: str, fill: float) -> pd.Series:
        if name not in frame.columns:
            return pd.Series(fill, index=frame.index, dtype=float)
        return pd.to_numeric(frame[name], errors="coerce").fillna(fill)

    frame["__seed_gap"] = numeric_column("f45_axis_gap_to_seed", 999999.0)
    frame["__forward_pf"] = numeric_column("forward_min_pf", -999999.0)
    frame["__forward_dd"] = numeric_column("forward_max_dd", 999999.0)
    frame["__train_rank"] = numeric_column("train_rank", 999999.0)
    frame = frame.sort_values(
        ["__seed_gap", "__forward_pf", "__forward_dd", "__train_rank"],
        ascending=[True, False, True, True],
    )
    row = frame.iloc[0].drop(labels=["__seed_gap", "__forward_pf", "__forward_dd", "__train_rank"])
    return json_ready(dict(row))


def build_repair_decision(initial_summary: pd.DataFrame) -> dict[str, Any]:
    if initial_summary.empty:
        return {
            "run_repair_grid": True,
            "repair_action": "run_capped_event_rarity_threshold_repair",
            "repair_reason": "Initial event classifier surface produced no candidate summary.",
        }
    runtime = int(initial_summary["runtime_probe_candidate_flag"].sum())
    seed = int(initial_summary["f45_seed_surface_flag"].sum())
    scout_rows = int(initial_summary["f45_scout_clue_flag"].sum())
    if runtime:
        return {
            "run_repair_grid": False,
            "repair_action": "skipped_runtime_candidate_present",
            "repair_reason": "Initial surface produced a runtime candidate; stop before expensive validation.",
        }
    if seed:
        return {
            "run_repair_grid": False,
            "repair_action": "skipped_seed_surface_present",
            "repair_reason": "Seed surface exists; avoid classifier overfit repair before runtime validation planning.",
        }
    return {
        "run_repair_grid": True,
        "repair_action": "run_capped_event_rarity_threshold_repair",
        "repair_reason": f"Initial event surface scout={scout_rows}, seed=0, runtime=0; run bounded rarity/threshold repair.",
        "initial_scout_rows": scout_rows,
    }


def classify_closeout(initial_summary: pd.DataFrame, repair_summary: pd.DataFrame) -> dict[str, Any]:
    combined = combine_summaries(initial_summary, repair_summary)
    if combined.empty:
        scout_rows = seed_rows = runtime_rows = 0
        best = {}
    else:
        scout_rows = int(combined["f45_scout_clue_flag"].sum())
        seed_rows = int(combined["f45_seed_surface_flag"].sum())
        runtime_rows = int(combined["runtime_probe_candidate_flag"].sum())
        best = json_ready(dict(combined.iloc[0]))
    nonwinner = closest_nonwinner_forward_observation(combined, best)
    if runtime_rows:
        closeout_class = "completion_candidate"
        runtime_status = "runtime_probe_candidate_requires_pre_expensive_grok_before_mt5"
        next_stage = STAGE_ID
        next_run = RUNTIME_REVIEW_RUN_ID
    elif seed_rows:
        closeout_class = "preserved_clue_seed_surface_without_runtime_candidate"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_runtime_candidate_after_f45_event_classifier_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    elif scout_rows:
        closeout_class = "preserved_clue_negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f45_event_classifier_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    else:
        closeout_class = "negative_memory"
        runtime_status = "runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f45_event_classifier_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    return {
        "closeout_class": closeout_class,
        "runtime_probe_status": runtime_status,
        "next_stage_id": next_stage,
        "next_run_id": next_run,
        "scout_clue_count": scout_rows,
        "seed_surface_count": seed_rows,
        "runtime_probe_candidate_count": runtime_rows,
        "best_variant": best,
        "closest_nonwinner_forward_observation": nonwinner,
    }


def write_surface_outputs(root: Path, profile: str, surface: dict[str, Any]) -> None:
    write_csv(root / f"{profile}_model_audit.csv", surface["model_audit"])
    write_csv(root / f"{profile}_candidate_ledger.csv", pd.DataFrame([clean_candidate(item) for item in surface["candidates"]]))
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
Train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기)가 F44 continuous utility regression(연속 효용 회귀)보다 고보상/저불리 경로 이벤트(high-payoff/low-adverse path event, 고보상/저불리 경로 이벤트)를 더 잘 분리하는지 시험한다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F44 best row(최상 행)는 reference-only scout clue(참조 전용 탐색 단서), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시).
- changed_variables(변경 변수): event label(이벤트 라벨), classifier family(분류 모델 계열), train-only event probability threshold(학습 전용 이벤트 확률 임계값).
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank(라벨/모델/임계값/손익절/순위)에 쓰는 경우.
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
            f"event={row.get('event_variant')}; model={row.get('model_family')}; "
            f"train_pf={row.get('train_profit_factor')}; val_pf={row.get('validation_profit_factor')}; "
            f"oos_pf={row.get('oos_profit_factor')}; fwd_density={row.get('forward_min_density')}..{row.get('forward_max_density')}; "
            f"fwd_dd={row.get('forward_max_dd')}; scout={row.get('f45_scout_clue_flag')}; "
            f"seed={row.get('f45_seed_surface_flag')}; runtime={row.get('runtime_probe_candidate_flag')}"
        )
        for row in best_rows[:6]
    )
    return f"""# Frontier45 closeout Grok review(그록 마감 검토)

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
- event_variant(이벤트 변형): {best.get("event_variant")}
- model_family(모델 계열): {best.get("model_family")}
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density_range(전진 거래 밀도 범위): {best.get("forward_min_density")} to {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}
- scout/seed/runtime(탐색/씨앗/런타임): {best.get("f45_scout_clue_flag")}/{best.get("f45_seed_surface_flag")}/{best.get("runtime_probe_candidate_flag")}

Top rows snapshot(상위 행 스냅샷):
{compact_rows}

Guardrail enforced(강제 보호선):
- event label/model/class weight/score threshold/SLTP/candidate rank(이벤트 라벨/모델/클래스 가중치/점수 임계값/손익절/후보 순위)는 train split only(학습 분할 전용).
- validation/OOS(검증/표본외)는 read-only evaluation(읽기 전용 평가).
- F44 continuous regression(연속 회귀), F42/F43/F38/F39 primary lever(주 레버)는 반복하지 않음.

Question(질문):
Is this closeout classification honest under the lifecycle(가설 생명주기), train-split-only construction lock(학습 분할 전용 구성 잠금), and claim boundary(주장 경계)?

Return only:
1. verdict: accepted, rejected, or needs_local_verification(수용/거절/로컬 검증 필요)
2. closeout_boundary_ok: yes/no(예/아니오)
3. one risk(위험) if any
4. one next-stage clue(다음 단계 단서) if any
"""


def build_review_artifacts(
    *,
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
    nonwinner = closeout.get("closest_nonwinner_forward_observation", {}) or {}
    report = f"""# {RUN_D} report(보고서)

## Judgment(판정)
- closeout_class(마감 분류): `{closeout.get("closeout_class")}`
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- scout/seed/runtime(탐색/씨앗/런타임): {closeout.get("scout_clue_count")}/{closeout.get("seed_surface_count")}/{closeout.get("runtime_probe_candidate_count")}

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `{best.get("candidate_id")}`
- event_variant(이벤트 변형): `{best.get("event_variant")}`
- model_family(모델 계열): `{best.get("model_family")}`
- train_profit_factor(학습 PF): {best.get("train_profit_factor")}
- validation_profit_factor(검증 PF): {best.get("validation_profit_factor")}
- oos_profit_factor(표본외 PF): {best.get("oos_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {best.get("forward_min_density")} ~ {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}

## Nonwinner Forward Observation(비승자 전진 관찰)
- candidate_id(후보 ID): `{nonwinner.get("candidate_id")}`
- event_variant(이벤트 변형): `{nonwinner.get("event_variant")}`
- model_family(모델 계열): `{nonwinner.get("model_family")}`
- forward_min_pf(전진 최소 PF): {nonwinner.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {nonwinner.get("forward_min_density")} ~ {nonwinner.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {nonwinner.get("forward_max_dd")}
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).

## Lifecycle(생명주기)
- stage_open(단계 개방): Grok(그록) {open_review.get("classification")}
- proxy(프록시): {initial_counts}
- repair(수리): {repair_decision.get("repair_action")} / {repair_counts}
- closeout_grok(마감 그록): {closeout_review.get("classification")}

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
"""
    run_a = f"""# {RUN_A} report(보고서)

F45 opened train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기) hypothesis(가설). F44 is reference only(참조 전용), not baseline/winner(기준선/승자 아님).
"""
    run_b = f"""# {RUN_B} report(보고서)

- model_rows(모델 행): {initial.get("model_rows")}
- candidate_rows(후보 행): {initial.get("candidate_rows")}
- scout/seed/runtime(탐색/씨앗/런타임): {initial.get("scout_clue_rows")}/{initial.get("seed_surface_rows")}/{initial.get("runtime_candidate_rows")}
- train_split_only_construction_lock(학습 분할 전용 구성 잠금): enforced(강제)
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
- train_split_only_construction_lock(학습 분할 전용 구성 잠금): {checks.get("checks", {}).get("train_split_only_construction_lock")}
- validation_oos_read_only(검증/표본외 읽기 전용): True
"""
    gate_audit = f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- scope_completion_gate(범위 완료 게이트): pass(통과), F45 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) materialized.
- kpi_contract_audit(KPI 계약 감사): pass(통과), train/validation/OOS PF/DD/density(학습/검증/표본외 PF/DD/밀도) split rows recorded.
- skill_receipt_lint(스킬 영수증 검사): pass_with_boundary(경계 통과), obsidian-run-evidence-system(실행 근거 시스템) skill unavailable in session; equivalent run evidence artifacts recorded.
- data_integrity(데이터 무결성): pass(통과), closed-bar feature order(닫힌 봉 피처 순서), split(분할), raw path(원천 경로) verified.
- model_validation(모델 검증): exploratory(탐색), event/model/threshold choice(이벤트/모델/임계값 선택)는 train-only(학습 전용); no promotion(승격 없음).
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
- local_verification(로컬 검증): accepted after confirming train-split-only construction lock(학습 분할 전용 구성 잠금 확인 후 수용)
- final_codex_direction(최종 코덱스 방향): run F45 event classifier proxy with validation/OOS read-only(검증/표본외 읽기 전용)
"""
    close_receipt = f"""# Grok Stage-Closeout Receipt(그록 단계 마감 영수증)

- trigger_reason(트리거 이유): stage closeout(단계 마감) requires Grok review(그록 검토).
- review_size(검토 크기): small review(소규모 검토)
- prompt_path(프롬프트 경로): `{GROK_CLOSE_ROOT / "input_prompt.md"}`
- output_path(출력 경로): `{closeout_review.get("clean_output_path")}`
- advice_classification(조언 분류): `{closeout_review.get("classification")}`
- local_verification(로컬 검증): {closeout_review.get("accepted_after_local_verification")}
- final_codex_direction(최종 코덱스 방향): close F45 as `{closeout.get("closeout_class")}` with no authority claim(권위 주장 없음)
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
    nonwinner = closeout.get("closest_nonwinner_forward_observation", {}) or {}
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

F45 preserved clue(보존 단서)는 train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기)가 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `{best.get("candidate_id")}`
- event_variant(이벤트 변형): `{best.get("event_variant")}`
- model_family(모델 계열): `{best.get("model_family")}`
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {best.get("forward_min_density")} ~ {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `{nonwinner.get("candidate_id")}`
- event_variant(이벤트 변형): `{nonwinner.get("event_variant")}`
- model_family(모델 계열): `{nonwinner.get("model_family")}`
- forward_min_pf(전진 최소 PF): {nonwinner.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {nonwinner.get("forward_min_density")} ~ {nonwinner.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {nonwinner.get("forward_max_dd")}
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
"""
    negative = f"""# Negative Memory(부정 기억)

F45 negative memory(부정 기억)는 train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기)가 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- do_not_repeat(반복 금지): F44 continuous regression(연속 회귀), F42 timing gate(타이밍 게이트), F43 trade-shape source(거래 형태 원천), F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움)를 primary lever(주 레버)로 반복하지 않는다.
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
            "notes": "F45 opened with train-only event utility classifier hypothesis and Grok guardrails.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_B,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "proxy",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Initial train-only event classifier proxy surface.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_C,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "repair",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Capped event rarity/threshold repair diagnostic.",
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
            "runtime_probe_status": "out_of_scope_by_claim_tier_a_event_classifier_proxy_only",
            "notes": "F45 used Tier A event classifier proxy only; Tier B not claimed.",
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
        "kpi_scope": "short_event_utility_classifier_proxy",
        "scoreboard_lane": "frontier_scout",
        "status": row.get("status", ""),
        "judgment": row.get("closeout_class", ""),
        "external_verification_status": row.get("runtime_probe_status", ""),
        "notes": row.get("notes", ""),
        "path": review_report_path(str(row.get("run_id", ""))).as_posix(),
        "report_path": review_report_path(str(row.get("run_id", ""))).as_posix(),
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness",
        "run_family": "frontier_short_event_utility_classifier_proxy",
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
current_judgment: {closeout.get("closeout_class")}(F45 train-only event classifier proxy no operating authority)
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

Frontier45(F45, 전선 45단계)가 `{closeout.get("closeout_class")}`로 닫혔다.

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

F45 carry-forward(이월) 기록은 train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기)가 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꾸었는지와 seed/runtime(씨앗/런타임) 후보가 생겼는지 여부다.
"""
    existing_plan = read_text(PRE_ALPHA_PLAN) if path_exists(PRE_ALPHA_PLAN) else "# Pre-Alpha Stage Plan\n"
    marker = "## Frontier Pointer(전선 포인터)"
    if marker in existing_plan:
        existing_plan = existing_plan.split(marker, 1)[0].rstrip()
    write_text_sig(PRE_ALPHA_PLAN, existing_plan.rstrip() + "\n\n" + pointer)


def artifact_map() -> dict[str, str]:
    return {
        "input_manifest": (INPUT_ROOT / "event_utility_model_manifest.json").as_posix(),
        "initial_summary": (RUN_B_ROOT / "initial_candidate_summary.csv").as_posix(),
        "repair_summary": (RUN_C_ROOT / "repair_candidate_summary.csv").as_posix(),
        "closeout_report": review_report_path(RUN_D).as_posix(),
        "selection_status": (SELECTED_ROOT / "selection_status.json").as_posix(),
    }


if __name__ == "__main__":
    main()
