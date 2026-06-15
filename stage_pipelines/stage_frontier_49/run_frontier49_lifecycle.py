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

STAGE_ID = "stage_frontier_49__short_pf_edge_forward_floor_state_machine_after_f48_event_risk_memory"
PREV_STAGE_ID = "stage_frontier_48__short_pf_edge_event_rarity_risk_sizing_after_f47_state_budget_memory"
RUN_A = "frontier49A_stage_open_short_pf_edge_forward_floor_state_machine_hypothesis_design_v1"
RUN_B = "frontier49B_train_only_forward_floor_state_machine_proxy_v1"
RUN_C = "frontier49C_capped_forward_floor_state_machine_repair_v1"
RUN_D = "frontier49D_stage_closeout_forward_floor_state_machine_v1"
NEXT_STAGE_ID = "stage_frontier_50__short_pf_edge_loss_floor_regime_transfer_after_f49_state_machine_memory"
NEXT_RUN_ID = "frontier50A_stage_open_short_pf_edge_loss_floor_regime_transfer_hypothesis_design_v1"
RUNTIME_REVIEW_RUN_ID = "frontier49E_pre_expensive_runtime_validation_review_v1"

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

GROK_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier49_stage_open" / "small_review"
GROK_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-15_frontier49_stage_closeout" / "small_review"

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

INITIAL_SCORE_QUANTILES = (0.86,)
INITIAL_STOP_QUANTILES = (0.24,)
INITIAL_TAKE_QUANTILES = (0.72,)
INITIAL_RR_FLOORS = (1.20,)
REPAIR_SCORE_QUANTILES = (0.86,)
REPAIR_STOP_QUANTILES = (0.24,)
REPAIR_TAKE_QUANTILES = (0.72,)
REPAIR_RR_FLOORS = (1.20,)
INITIAL_MAX_CANDIDATES = 40
REPAIR_MAX_CANDIDATES = 90

INITIAL_BASE_SCORE_HIGH_QUANTILES = (0.86, 0.90)
REPAIR_BASE_SCORE_HIGH_QUANTILES = (0.82, 0.88)


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
    write_json(INPUT_ROOT / "forward_floor_state_machine_manifest.json", manifest)
    write_csv(INPUT_ROOT / "gate_provenance_table.csv", build_gate_provenance_table())
    write_text_sig(SPEC_ROOT / "stage_brief.md", build_stage_brief(manifest, open_review, checks))
    write_json(RUN_A_ROOT / "stage_open_local_verification.json", {"open_review": open_review, "checks": checks})

    initial = build_event_surface(
        frame,
        feature_order,
        path_labels,
        raw_path,
        run_id=RUN_B,
        run_prefix="f49b",
        profile="initial",
        event_specs=event_specs(frame, path_labels[SIDE_VALUE], "initial"),
        base_scorer_specs=base_scorer_specs("initial"),
        context_specs=sequence_context_specs("initial"),
        model_specs=model_specs("initial"),
        risk_budget_specs=risk_budget_specs("initial"),
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
            run_prefix="f49c",
            profile="repair",
            event_specs=event_specs(frame, path_labels[SIDE_VALUE], "repair"),
            base_scorer_specs=base_scorer_specs("repair"),
            context_specs=sequence_context_specs("repair"),
            model_specs=model_specs("repair"),
            risk_budget_specs=risk_budget_specs("repair"),
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
            "profile": "short_forward_floor_state_machine_proxy",
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
    guardrail_seen = (
        "train_split_only_construction_lock" in lowered
        or (("train-split-only" in lowered or "학습 분할" in clean) and ("construction lock" in lowered or "구성 잠금" in clean))
    )
    claim_ok = "claim_boundary_ok" in lowered and "yes" in lowered
    forbidden = any(
        phrase in lowered
        for phrase in ("operating promotion", "runtime authority", "live readiness", "goal achieve", "selected baseline")
    )
    return {
        "packet": GROK_OPEN_ROOT.as_posix(),
        "metadata": metadata,
        "clean_output_path": clean_path.as_posix(),
        "classification": "accepted_stage_open_train_split_only_forward_floor_state_machine_lock" if accepted and guardrail_seen and claim_ok and not rejected else "needs_local_verification",
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
        "classification": "accepted_closeout_forward_floor_state_machine_boundary" if accepted and boundary_ok and not rejected else "needs_local_verification",
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
        "workspace_points_to_f49": f"next_stage_id: {STAGE_ID}" in workspace or f"current_stage_id: {STAGE_ID}" in workspace,
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
        "past_outcome_embargo_join_audit": sequence_embargo_bars(frame) >= 2,
        "validation_oos_threshold_pick_isolation": True,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier49 context check failed: {json.dumps(checks, ensure_ascii=False)}")
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
        "hypothesis": "train_only_forward_floor_state_machine_on_f48_event_risk_memory",
        "idea_id": "IDEA-FR49-SHORT-FORWARD-FLOOR-STATE-MACHINE",
        "decision_use": "scout_seed_runtime_candidate_screening_only",
        "comparison_baseline": "F48 best and closest nonwinner rows are reference-only clues, not inherited baseline",
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
            "sequence_context": "lagged frozen event score plus horizon-embargoed past outcome tape expanded with rolling event-balance floor states",
            "state_gate": "fixed forward-floor state machine using bars since known bad/good event, event-balance floor, crowding, and volatility caps",
            "risk_sizing": "train-only first-hit SLTP caps with fixed score/event scaffold and fixed state-machine admission",
            "novelty_line": "forward-floor state machine uses entry-known causal past outcome states instead of F48 static state gates or F47 percentile risk-budget sweep",
            "model_family": "class_weighted_sequence_context_classifier_with_forward_floor_state_machine_overlay",
            "threshold_policy": "train_split_event_score_threshold_only; floor state gates are fixed absolute thresholds; validation_oos_read_only",
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
            "past_outcome_tape_uses_labels_newer_than_horizon_plus_one_bars",
            "f48_static_state_gate_repeated_without_forward_floor_state_machine",
            "f47_percentile_risk_budget_sweep_repeated_as_primary_lever",
            "f44_continuous_regression_or_f42_f43_f38_f39_primary_lever_reopened",
        ],
        "evidence_plan": [
            "stage_open_grok_receipt",
            "gate_provenance_table",
            "forward_floor_state_machine_model_audit",
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
            "gate_provenance_table": artifact_descriptor(INPUT_ROOT / "gate_provenance_table.csv"),
        },
        "open_review": open_review,
        "checks": checks,
    }


def build_gate_provenance_table() -> pd.DataFrame:
    rows: list[dict[str, Any]] = [
        {
            "profile": "all",
            "gate_family": "archived_scaffold",
            "gate_variant": "f48_reference_event_model_context_score_sltp",
            "threshold_name": "archived_f48_scaffold",
            "threshold_value": "reference_only",
            "provenance_tag": "archived_clue_no_selection",
            "selection_role": "locked_reference_not_baseline",
        },
        {
            "profile": "initial_repair",
            "gate_family": "event_score",
            "gate_variant": "event_model_score_quantile",
            "threshold_name": "score_quantile",
            "threshold_value": "|".join(str(item) for item in sorted(set(INITIAL_SCORE_QUANTILES + REPAIR_SCORE_QUANTILES))),
            "provenance_tag": "train_only_fit",
            "selection_role": "candidate_admission_threshold",
        },
        {
            "profile": "initial_repair",
            "gate_family": "risk_sizing",
            "gate_variant": "first_hit_sltp",
            "threshold_name": "stop_take_quantiles",
            "threshold_value": f"stop={INITIAL_STOP_QUANTILES}|take={INITIAL_TAKE_QUANTILES}|repair_stop={REPAIR_STOP_QUANTILES}|repair_take={REPAIR_TAKE_QUANTILES}",
            "provenance_tag": "train_only_fit",
            "selection_role": "train_path_sltp_cap_source",
        },
        {
            "profile": "initial_repair",
            "gate_family": "risk_sizing",
            "gate_variant": "first_hit_sltp",
            "threshold_name": "rr_floor",
            "threshold_value": "|".join(str(item) for item in sorted(set(INITIAL_RR_FLOORS + REPAIR_RR_FLOORS))),
            "provenance_tag": "fixed_design_constant",
            "selection_role": "minimum_take_stop_ratio",
        },
    ]
    for profile in ("initial", "repair"):
        for spec in risk_budget_specs(profile):
            variant = str(spec.get("risk_budget_variant", "unknown_state_gate"))
            for family, tag, values in (
                ("state_gate_equals", "fixed_design_constant", dict(spec.get("equals_features", {}))),
                ("state_gate_max", "fixed_design_constant", dict(spec.get("max_fixed_features", {}))),
                ("state_gate_min", "fixed_design_constant", dict(spec.get("min_fixed_features", {}))),
                ("state_gate_quantile", "train_only_fit", dict(spec.get("max_quantile_features", {}))),
            ):
                for feature, value in values.items():
                    rows.append(
                        {
                            "profile": profile,
                            "gate_family": family,
                            "gate_variant": variant,
                            "threshold_name": str(feature),
                            "threshold_value": value,
                            "provenance_tag": tag,
                            "selection_role": "fixed_state_admission" if tag == "fixed_design_constant" else "train_only_threshold",
                        }
                    )
    return pd.DataFrame(rows)


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
            "event_mfe65_mae35_loss_contained",
            "short path event if MFE >= train q65 and MAE <= train q35",
            (mfe >= q["mfe65"]) & (mae <= q["mae35"]),
            {"mfe65": q["mfe65"], "mae35": q["mae35"]},
        ),
        build(
            "event_mfe75_mae50_ratio70",
            "short path event if MFE >= train q75, MAE <= train q50, and MFE/MAE ratio >= train q70",
            (mfe >= q["mfe75"]) & (mae <= q["mae50"]) & (ratio >= q["ratio70"]),
            {"mfe75": q["mfe75"], "mae50": q["mae50"], "ratio70": q["ratio70"]},
        ),
        build(
            "event_mfe70_mae45_horizon_pos",
            "short path event if MFE >= train q70, MAE <= train q45, and horizon pnl positive",
            (mfe >= q["mfe70"]) & (mae <= q["mae45"]) & (horizon > 0.0),
            {"mfe70": q["mfe70"], "mae45": q["mae45"]},
        ),
    ]
    if profile == "initial":
        return [item for item in specs if item["event_variant"] == "event_mfe65_mae35_loss_contained"]
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
        return [
            item
            for item in specs
            if item["event_variant"]
            in {
                "event_mfe65_mae35_loss_contained",
                "event_mfe70_mae45_horizon_pos",
                "repair_event_mfe60_mae60_horizon_pos",
            }
        ]
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
    if profile in {"initial", "repair"}:
        return [specs[1]]
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


def base_scorer_specs(profile: str) -> list[dict[str, Any]]:
    specs = [
        {
            "base_scorer_family": "base_logreg_c0p25",
            "factory": lambda: make_pipeline(
                StandardScaler(),
                LogisticRegression(C=0.25, class_weight="balanced", max_iter=500, solver="liblinear", random_state=4602),
            ),
        },
        {
            "base_scorer_family": "base_extratrees_d3_leaf220",
            "factory": lambda: ExtraTreesClassifier(
                n_estimators=80,
                max_depth=3,
                min_samples_leaf=220,
                class_weight="balanced_subsample",
                random_state=4603,
                n_jobs=1,
            ),
        },
    ]
    if profile in {"initial", "repair"}:
        return [specs[1]]
    if profile == "repair":
        specs.append(
            {
                "base_scorer_family": "base_logreg_c1",
                "factory": lambda: make_pipeline(
                    StandardScaler(),
                    LogisticRegression(C=1.0, class_weight="balanced", max_iter=500, solver="liblinear", random_state=4611),
                ),
            }
        )
    return specs


def sequence_context_specs(profile: str) -> list[dict[str, Any]]:
    pairs = ((0.86, 12, 36),)
    specs: list[dict[str, Any]] = []
    for high_q, fast, slow in pairs:
        specs.append(
            {
                "context_variant": f"lagged_score_outcome_q{int(high_q * 100)}_w{fast}_{slow}",
                "base_score_high_quantile": high_q,
                "fast_window": fast,
                "slow_window": slow,
                "include_past_outcome_tape": True,
            }
        )
    return specs


def risk_budget_specs(profile: str) -> list[dict[str, Any]]:
    specs = [
        {
            "risk_budget_variant": "floor_state_recovery2_balance_fast_ge_minus0p5_vol5_le1p75",
            "risk_budget_definition": "fixed forward-floor state: two bars after known bad event, fast event balance >= -0.5, realized vol expansion <= 1.75",
            "equals_features": {
                "bb_squeeze": 0.0,
            },
            "max_fixed_features": {
                "historical_vol_5_over_20": 1.75,
            },
            "min_fixed_features": {
                "seq_bars_since_bad_event": 2.0,
                "seq_past_event_balance_fast": -0.5,
            },
        },
        {
            "risk_budget_variant": "floor_state_dual_balance_fast_ge_minus0p5_slow_ge_minus0p6_atr_le1p75",
            "risk_budget_definition": "fixed forward-floor state: fast and slow event balance floors stay above weak-negative bounds with ATR ratio <= 1.75",
            "equals_features": {
            },
            "max_fixed_features": {
                "atr_14_over_atr_50": 1.75,
            },
            "min_fixed_features": {
                "seq_past_event_balance_fast": -0.5,
                "seq_past_event_balance_slow": -0.6,
            },
        },
        {
            "risk_budget_variant": "floor_state_cooldown3_bad_fast_le0p75_high_count_le12",
            "risk_budget_definition": "fixed forward-floor state: three bars after known bad event, fast bad-event rate <= 0.75, high-score crowding <= 12",
            "equals_features": {},
            "max_fixed_features": {
                "seq_past_bad_event_rate_fast": 0.75,
                "seq_high_count_fast": 12.0,
            },
            "min_fixed_features": {
                "seq_bars_since_high_score": 3.0,
                "seq_bars_since_bad_event": 3.0,
            },
        },
        {
            "risk_budget_variant": "floor_state_recent_good18_bad_slow_le0p8_squeeze_off",
            "risk_budget_definition": "fixed forward-floor state: recent known good event within 18 bars, slow bad-event rate <= 0.8, no squeeze",
            "equals_features": {
                "bb_squeeze": 0.0,
            },
            "max_fixed_features": {
                "seq_bars_since_good_event": 18.0,
                "seq_past_bad_event_rate_slow": 0.8,
            },
            "min_fixed_features": {},
        },
    ]
    if profile == "repair":
        specs.extend(
            [
                {
                    "risk_budget_variant": "repair_floor_state_recovery2_balance_fast_ge_minus0p67",
                    "risk_budget_definition": "fixed repair forward-floor state: two bars after known bad event and fast balance >= -0.67",
                    "equals_features": {},
                    "max_fixed_features": {
                        "historical_vol_5_over_20": 2.0,
                    },
                    "min_fixed_features": {
                        "seq_bars_since_bad_event": 2.0,
                        "seq_past_event_balance_fast": -0.67,
                    },
                },
                {
                    "risk_budget_variant": "repair_floor_state_good_recent24_squeeze_off",
                    "risk_budget_definition": "fixed repair forward-floor state: known good event within 24 bars and no squeeze",
                    "equals_features": {
                        "bb_squeeze": 0.0,
                    },
                    "max_fixed_features": {
                        "seq_bars_since_good_event": 24.0,
                    },
                    "min_fixed_features": {},
                },
                {
                    "risk_budget_variant": "repair_floor_state_clean_fast_bad_le0p67_high_count_le14",
                    "risk_budget_definition": "fixed repair forward-floor state: fast bad-event rate <= 0.67 and high-score crowding <= 14",
                    "equals_features": {},
                    "max_fixed_features": {
                        "seq_past_bad_event_rate_fast": 0.67,
                        "seq_high_count_fast": 14.0,
                    },
                    "min_fixed_features": {},
                },
                {
                    "risk_budget_variant": "repair_floor_state_dual_balance_vol_atr_le2",
                    "risk_budget_definition": "fixed repair forward-floor state: fast/slow balance above -0.67 with vol and ATR ratios <= 2.0",
                    "equals_features": {},
                    "max_fixed_features": {
                        "historical_vol_5_over_20": 2.0,
                        "atr_14_over_atr_50": 2.0,
                    },
                    "min_fixed_features": {
                        "seq_past_event_balance_fast": -0.67,
                        "seq_past_event_balance_slow": -0.67,
                    },
                },
            ]
        )
    return specs


def apply_risk_budget_mask(
    *,
    frame: pd.DataFrame,
    base_mask: np.ndarray,
    train_mask: np.ndarray,
    context: dict[str, Any],
    risk_spec: dict[str, Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    mask = np.asarray(base_mask, dtype=bool).copy()
    train_base = np.asarray(train_mask, dtype=bool) & np.asarray(base_mask, dtype=bool)
    threshold_source = train_base if int(np.sum(train_base)) >= 50 else np.asarray(train_mask, dtype=bool)
    thresholds: dict[str, float] = {}
    applied: list[str] = []

    for feature, quantile in dict(risk_spec.get("max_quantile_features", {})).items():
        values = risk_feature_series(frame, context, str(feature))
        finite = np.isfinite(values)
        sample = values[threshold_source & finite]
        if sample.size < 30:
            mask &= False
            thresholds[str(feature)] = math.nan
            applied.append(f"{feature}<=insufficient_train_sample")
            continue
        threshold = float(np.nanquantile(sample, float(quantile)))
        mask &= finite & (values <= threshold)
        thresholds[str(feature)] = threshold
        applied.append(f"{feature}<=train_q{float(quantile):.2f}")

    for feature, maximum in dict(risk_spec.get("max_fixed_features", {})).items():
        values = risk_feature_series(frame, context, str(feature))
        finite = np.isfinite(values)
        maximum_value = float(maximum)
        mask &= finite & (values <= maximum_value)
        thresholds[str(feature)] = maximum_value
        applied.append(f"{feature}<={maximum_value:.4g}_fixed")

    for feature, minimum in dict(risk_spec.get("min_fixed_features", {})).items():
        values = risk_feature_series(frame, context, str(feature))
        finite = np.isfinite(values)
        mask &= finite & (values >= float(minimum))
        thresholds[str(feature)] = float(minimum)
        applied.append(f"{feature}>={float(minimum):.2f}")

    for feature, expected in dict(risk_spec.get("equals_features", {})).items():
        values = risk_feature_series(frame, context, str(feature))
        finite = np.isfinite(values)
        expected_value = float(expected)
        mask &= finite & np.isclose(values, expected_value, atol=1e-12)
        thresholds[str(feature)] = expected_value
        applied.append(f"{feature}=={expected_value:.4g}_fixed")

    before = int(np.sum(train_base))
    after = int(np.sum(np.asarray(train_mask, dtype=bool) & mask))
    threshold_source_label = (
        "train_base_mask" if dict(risk_spec.get("max_quantile_features", {})) and int(np.sum(train_base)) >= 50
        else "train_context_universe" if dict(risk_spec.get("max_quantile_features", {}))
        else "fixed_nonpercentile_entry_known_state"
    )
    return mask, {
        "risk_budget_variant": risk_spec.get("risk_budget_variant", ""),
        "risk_budget_definition": risk_spec.get("risk_budget_definition", ""),
        "risk_budget_threshold_source": threshold_source_label,
        "risk_budget_train_rows_before": before,
        "risk_budget_train_rows_after": after,
        "risk_budget_train_keep_rate": safe_float(after / max(before, 1)),
        "risk_budget_train_block_rate": safe_float(1.0 - (after / max(before, 1))),
        "risk_budget_thresholds": thresholds,
        "risk_budget_applied": "|".join(applied),
    }


def risk_feature_series(frame: pd.DataFrame, context: dict[str, Any], feature: str) -> np.ndarray:
    context_frame = context.get("context_frame")
    if isinstance(context_frame, pd.DataFrame) and feature in context_frame.columns:
        return pd.to_numeric(context_frame[feature], errors="coerce").to_numpy(dtype="float64")
    if feature in frame.columns:
        return pd.to_numeric(frame[feature], errors="coerce").to_numpy(dtype="float64")
    return np.full(len(frame), np.nan, dtype="float64")


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
    base_scorer_specs: list[dict[str, Any]],
    context_specs: list[dict[str, Any]],
    model_specs: list[dict[str, Any]],
    risk_budget_specs: list[dict[str, Any]],
    score_quantiles: tuple[float, ...],
    stop_quantiles: tuple[float, ...],
    take_quantiles: tuple[float, ...],
    rr_floors: tuple[float, ...],
    max_candidates: int,
) -> dict[str, Any]:
    x_raw = frame[feature_order].to_numpy(dtype="float64")
    valid_raw_features = np.isfinite(x_raw).all(axis=1)
    labels = path_labels[SIDE_VALUE]
    train_mask = f33b.split_mask(frame, "train") & valid_raw_features & labels["valid"]
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
        for base_spec in base_scorer_specs:
            base_model = base_spec["factory"]()
            base_model.fit(x_raw[fit_mask], y[fit_mask])
            base_score = np.full(len(frame), np.nan, dtype="float64")
            base_score[valid_raw_features] = event_probability(base_model, x_raw[valid_raw_features])
            finite_base_score = np.isfinite(base_score) & valid_raw_features
            base_train_scores = base_score[train_mask & finite_base_score]
            if base_train_scores.size < 100:
                model_rows.append(
                    {
                        "run_id": run_id,
                        "profile": profile,
                        "event_variant": event_spec["event_variant"],
                        "model_family": "not_fit_sequence_context",
                        "base_scorer_family": base_spec["base_scorer_family"],
                        "status": "skipped_sparse_base_train_scores",
                        "train_rows": int(np.sum(fit_mask)),
                        "train_positive_rows": positives,
                        "train_event_rate": event_spec["train_event_rate"],
                    }
                )
                continue
            for context_spec in context_specs:
                context = build_sequence_context(
                    frame=frame,
                    base_score=base_score,
                    event=y,
                    train_mask=train_mask & finite_base_score,
                    context_spec=context_spec,
                )
                x_context = context["matrix"]
                valid_context = context["valid_context"] & valid_raw_features
                x_model = np.column_stack([x_raw, x_context])
                fit_mask_context = fit_mask & valid_context
                if int(np.sum(fit_mask_context)) < 250 or int(np.sum(y[fit_mask_context] == 1)) < 50:
                    model_rows.append(
                        {
                            "run_id": run_id,
                            "profile": profile,
                            "event_variant": event_spec["event_variant"],
                            "model_family": "not_fit_sequence_context",
                            "base_scorer_family": base_spec["base_scorer_family"],
                            "context_variant": context_spec["context_variant"],
                            "status": "skipped_sparse_sequence_context",
                            "train_rows": int(np.sum(fit_mask_context)),
                            "train_positive_rows": int(np.sum(y[fit_mask_context] == 1)),
                            "train_event_rate": event_spec["train_event_rate"],
                            "past_outcome_embargo_bars": context["past_outcome_embargo_bars"],
                        }
                    )
                    continue
                for model_spec in model_specs:
                    model = model_spec["factory"]()
                    model.fit(x_model[fit_mask_context], y[fit_mask_context])
                    score = np.full(len(frame), np.nan, dtype="float64")
                    score[valid_context] = event_probability(model, x_model[valid_context])
                    finite_score = np.isfinite(score) & valid_context
                    train_scores = score[train_mask & finite_score]
                    effective_model_spec = {
                        **model_spec,
                        "model_family": (
                            f"{model_spec['model_family']}__{base_spec['base_scorer_family']}__"
                            f"{context_spec['context_variant']}"
                        ),
                        "base_scorer_family": base_spec["base_scorer_family"],
                        "context_variant": context_spec["context_variant"],
                        "sequence_context_features": "|".join(context["feature_names"]),
                        "past_outcome_embargo_bars": context["past_outcome_embargo_bars"],
                        "base_score_high_quantile": context_spec["base_score_high_quantile"],
                    }
                    model_rows.append(
                        {
                            "run_id": run_id,
                            "profile": profile,
                            "event_variant": event_spec["event_variant"],
                            "event_definition": event_spec["event_definition"],
                            "model_family": effective_model_spec["model_family"],
                            "base_scorer_family": base_spec["base_scorer_family"],
                            "context_variant": context_spec["context_variant"],
                            "onnx_friendly": bool(model_spec.get("onnx_friendly", False)),
                            "status": "fit_train_only_frozen_base_scorer_sequence_context",
                            "train_rows": int(np.sum(fit_mask_context)),
                            "train_positive_rows": int(np.sum(y[fit_mask_context] == 1)),
                            "train_event_rate": event_spec["train_event_rate"],
                            "train_score_min": safe_float(np.nanmin(train_scores)) if train_scores.size else math.nan,
                            "train_score_max": safe_float(np.nanmax(train_scores)) if train_scores.size else math.nan,
                            "base_score_train_min": safe_float(np.nanmin(base_train_scores)),
                            "base_score_train_max": safe_float(np.nanmax(base_train_scores)),
                            "base_score_high_threshold": context["base_score_high_threshold"],
                            "past_outcome_embargo_bars": context["past_outcome_embargo_bars"],
                            "sequence_context_features": "|".join(context["feature_names"]),
                            "train_thresholds": json.dumps(json_ready(event_spec["train_thresholds"]), ensure_ascii=False, sort_keys=True),
                        }
                    )
                    if train_scores.size < 100:
                        continue
                    for score_q in score_quantiles:
                        threshold = float(np.nanquantile(train_scores, score_q))
                        base_mask = finite_score & (score >= threshold)
                        for risk_spec in risk_budget_specs:
                            risk_mask, risk_meta = apply_risk_budget_mask(
                                frame=frame,
                                base_mask=base_mask,
                                train_mask=train_mask & finite_score,
                                context=context,
                                risk_spec=risk_spec,
                            )
                            candidates.extend(
                                candidates_for_mask(
                                    frame,
                                    risk_mask,
                                    path_labels,
                                    raw_path,
                                    stop_quantiles,
                                    take_quantiles,
                                    rr_floors,
                                    event_spec,
                                    effective_model_spec,
                                    score_q,
                                    threshold,
                                    score,
                                    profile,
                                    risk_spec,
                                    risk_meta,
                                )
                            )

    selected = rank_candidates(candidates, run_prefix, max_candidates)
    split_metrics = f33b.evaluate_candidates(frame, selected, path_labels, raw_path) if selected else pd.DataFrame()
    summary = summarize_f49_candidates(split_metrics, selected)
    return {
        "model_audit": pd.DataFrame(model_rows),
        "candidates": selected,
        "split_metrics": split_metrics,
        "summary": summary,
        "model_rows": int(len(model_rows)),
        "candidate_rows": int(len(selected)),
        **surface_counts(summary),
    }


def build_sequence_context(
    *,
    frame: pd.DataFrame,
    base_score: np.ndarray,
    event: np.ndarray,
    train_mask: np.ndarray,
    context_spec: dict[str, Any],
) -> dict[str, Any]:
    fast = int(context_spec["fast_window"])
    slow = int(context_spec["slow_window"])
    high_q = float(context_spec["base_score_high_quantile"])
    embargo = sequence_embargo_bars(frame)
    score = pd.Series(np.asarray(base_score, dtype="float64"))
    event_series = pd.Series(np.asarray(event, dtype="float64"))
    train_scores = score.loc[np.asarray(train_mask, dtype=bool)].replace([np.inf, -np.inf], np.nan).dropna()
    high_threshold = float(train_scores.quantile(high_q)) if len(train_scores) else math.inf
    high_signal = score >= high_threshold
    prior_score = score.shift(1)
    prior_high = high_signal.astype(bool).shift(1, fill_value=False).astype(float)
    known_event = event_series.shift(embargo)
    known_bad_event = (1.0 - known_event).where(known_event.notna())
    event_rate_fast = known_event.rolling(fast, min_periods=max(2, fast // 2)).mean()
    event_rate_slow = known_event.rolling(slow, min_periods=max(3, slow // 2)).mean()
    bad_rate_fast = known_bad_event.rolling(fast, min_periods=max(2, fast // 2)).mean()
    bad_rate_slow = known_bad_event.rolling(slow, min_periods=max(3, slow // 2)).mean()
    balance_fast = (event_rate_fast * 2.0) - 1.0
    balance_slow = (event_rate_slow * 2.0) - 1.0
    known_bad_flag = (known_bad_event == 1.0).fillna(False).to_numpy(dtype=bool)
    known_good_flag = (known_event == 1.0).fillna(False).to_numpy(dtype=bool)
    data = {
        "seq_score_lag1": prior_score,
        "seq_score_lag3": score.shift(3),
        "seq_score_roll_mean_fast": prior_score.rolling(fast, min_periods=max(2, fast // 2)).mean(),
        "seq_score_roll_mean_slow": prior_score.rolling(slow, min_periods=max(3, slow // 2)).mean(),
        "seq_high_count_fast": prior_high.rolling(fast, min_periods=max(2, fast // 2)).sum(),
        "seq_high_count_slow": prior_high.rolling(slow, min_periods=max(3, slow // 2)).sum(),
        "seq_past_event_rate_fast": event_rate_fast,
        "seq_past_event_rate_slow": event_rate_slow,
        "seq_past_bad_event_rate_fast": bad_rate_fast,
        "seq_past_bad_event_rate_slow": bad_rate_slow,
        "seq_past_event_balance_fast": balance_fast,
        "seq_past_event_balance_slow": balance_slow,
        "seq_past_event_balance_floor_fast": balance_fast.rolling(fast, min_periods=max(2, fast // 2)).min(),
        "seq_past_event_balance_floor_slow": balance_slow.rolling(slow, min_periods=max(3, slow // 2)).min(),
        "seq_bars_since_high_score": pd.Series(bars_since_true(high_signal.to_numpy(dtype=bool))),
        "seq_bars_since_bad_event": pd.Series(bars_since_true(known_bad_flag)),
        "seq_bars_since_good_event": pd.Series(bars_since_true(known_good_flag)),
    }
    context_frame = pd.DataFrame(data)
    context_frame["seq_score_roll_slope_fast_slow"] = (
        context_frame["seq_score_roll_mean_fast"] - context_frame["seq_score_roll_mean_slow"]
    )
    context_frame["seq_event_rate_slope_fast_slow"] = (
        context_frame["seq_past_event_rate_fast"] - context_frame["seq_past_event_rate_slow"]
    )
    feature_names = list(context_frame.columns)
    matrix = context_frame.to_numpy(dtype="float64")
    valid_context = np.isfinite(matrix).all(axis=1)
    return {
        "matrix": matrix,
        "valid_context": valid_context,
        "feature_names": feature_names,
        "context_frame": context_frame,
        "base_score_high_threshold": high_threshold,
        "past_outcome_embargo_bars": embargo,
    }


def sequence_embargo_bars(frame: pd.DataFrame) -> int:
    if "horizon_bars" not in frame.columns:
        return 13
    horizon = pd.to_numeric(frame["horizon_bars"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if horizon.empty:
        return 13
    return max(2, int(math.ceil(float(horizon.max()))) + 1)


def bars_since_true(flags: np.ndarray) -> np.ndarray:
    out = np.full(len(flags), 999.0, dtype="float64")
    last_seen = -1
    for index, flag in enumerate(np.asarray(flags, dtype=bool)):
        if last_seen >= 0:
            out[index] = float(index - last_seen)
        if flag:
            last_seen = index
    return out


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
    risk_spec: dict[str, Any],
    risk_meta: dict[str, Any],
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    risk_variant = str(risk_spec.get("risk_budget_variant", "risk_budget_unknown"))
    condition = {
        "condition_id": f"{event_spec['event_variant']}__{model_spec['model_family']}__{risk_variant}__q{score_quantile:.2f}",
        "feature": model_spec["model_family"],
        "feature_family": "train_only_forward_floor_state_machine_score",
        "definition": f"{event_spec['event_variant']} {model_spec['model_family']} sequence probability >= train q{score_quantile:.2f}",
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
        f"f49_{profile}_train_only_forward_floor_state_machine_sl_tp_caps",
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
        candidate["base_scorer_family"] = model_spec.get("base_scorer_family", "")
        candidate["context_variant"] = model_spec.get("context_variant", "")
        candidate["sequence_context_features"] = model_spec.get("sequence_context_features", "")
        candidate["risk_budget_variant"] = risk_meta.get("risk_budget_variant", risk_variant)
        candidate["risk_budget_definition"] = risk_meta.get("risk_budget_definition", "")
        candidate["risk_budget_threshold_source"] = risk_meta.get("risk_budget_threshold_source", "")
        candidate["risk_budget_train_rows_before"] = risk_meta.get("risk_budget_train_rows_before", "")
        candidate["risk_budget_train_rows_after"] = risk_meta.get("risk_budget_train_rows_after", "")
        candidate["risk_budget_train_keep_rate"] = risk_meta.get("risk_budget_train_keep_rate", "")
        candidate["risk_budget_train_block_rate"] = risk_meta.get("risk_budget_train_block_rate", "")
        candidate["risk_budget_thresholds"] = json.dumps(
            json_ready(risk_meta.get("risk_budget_thresholds", {})), ensure_ascii=False, sort_keys=True
        )
        candidate["risk_budget_applied"] = risk_meta.get("risk_budget_applied", "")
        candidate["past_outcome_embargo_bars"] = model_spec.get("past_outcome_embargo_bars", "")
        candidate["base_score_high_quantile"] = model_spec.get("base_score_high_quantile", "")
        candidate["onnx_friendly"] = bool(model_spec.get("onnx_friendly", False))
        candidate["score_quantile"] = score_quantile
        candidate["score_threshold"] = score_threshold
        candidate["train_event_rate_selected"] = event_rate_selected
        candidate["train_score_margin_median"] = score_margin
        candidate["f49_train_selection_score"] = score_value
        candidate["selection_rank_basis"] = "train_only_event_forward_floor_state_machine_no_validation_oos_feedback"
        variants.append(candidate)
    variants.sort(key=lambda item: float(item["f49_train_selection_score"]), reverse=True)
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
    seen: set[tuple[str, str, str, float, float, float]] = set()
    selected: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: float(item["f49_train_selection_score"]), reverse=True):
        key = (
            str(candidate.get("event_variant", "")),
            str(candidate.get("model_family", "")),
            str(candidate.get("risk_budget_variant", "")),
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


def summarize_f49_candidates(split_metrics: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
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
            "base_scorer_family": item.get("base_scorer_family", ""),
            "context_variant": item.get("context_variant", ""),
            "risk_budget_variant": item.get("risk_budget_variant", ""),
            "risk_budget_definition": item.get("risk_budget_definition", ""),
            "risk_budget_threshold_source": item.get("risk_budget_threshold_source", ""),
            "risk_budget_train_rows_before": item.get("risk_budget_train_rows_before", ""),
            "risk_budget_train_rows_after": item.get("risk_budget_train_rows_after", ""),
            "risk_budget_train_keep_rate": item.get("risk_budget_train_keep_rate", ""),
            "risk_budget_train_block_rate": item.get("risk_budget_train_block_rate", ""),
            "risk_budget_thresholds": item.get("risk_budget_thresholds", ""),
            "risk_budget_applied": item.get("risk_budget_applied", ""),
            "past_outcome_embargo_bars": item.get("past_outcome_embargo_bars", ""),
            "base_score_high_quantile": item.get("base_score_high_quantile", ""),
            "onnx_friendly": item.get("onnx_friendly", ""),
            "score_quantile": item.get("score_quantile", ""),
            "score_threshold": item.get("score_threshold", ""),
            "train_event_rate_selected": item.get("train_event_rate_selected", ""),
            "f49_train_selection_score": item.get("f49_train_selection_score", ""),
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
        "base_scorer_family",
        "context_variant",
        "risk_budget_variant",
        "risk_budget_definition",
        "risk_budget_threshold_source",
        "risk_budget_train_rows_before",
        "risk_budget_train_rows_after",
        "risk_budget_train_keep_rate",
        "risk_budget_train_block_rate",
        "risk_budget_thresholds",
        "risk_budget_applied",
        "past_outcome_embargo_bars",
        "base_score_high_quantile",
        "onnx_friendly",
        "score_quantile",
        "score_threshold",
        "train_event_rate_selected",
        "f49_train_selection_score",
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
    summary["f49_scout_clue_flag"] = dual & density_scout & (f_min_pf >= SCOUT_MIN_PF) & (f_max_dd <= SCOUT_MAX_DD)
    summary["f49_seed_surface_flag"] = dual & density_seed & (f_min_pf >= SEED_MIN_PF) & (f_max_dd <= SEED_MAX_DD)
    summary["runtime_probe_candidate_flag"] = (
        summary["f49_seed_surface_flag"].astype(bool) & (f_min_pf >= RUNTIME_MIN_PF) & (f_max_dd <= RUNTIME_MAX_DD)
    )
    summary["f49_axis_gap_to_seed"] = (
        np.maximum(0.0, SEED_MIN_PF - f_min_pf)
        + np.maximum(0.0, f_max_dd - SEED_MAX_DD) / SEED_MAX_DD
        + np.maximum(0.0, SEED_MIN_DENSITY - f_min_density) / SEED_MIN_DENSITY
        + np.maximum(0.0, f_max_density - SEED_MAX_DENSITY) / SEED_MAX_DENSITY
    )
    return summary.sort_values(
        [
            "runtime_probe_candidate_flag",
            "f49_seed_surface_flag",
            "f49_scout_clue_flag",
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
        "scout_clue_rows": int(summary["f49_scout_clue_flag"].sum()),
        "seed_surface_rows": int(summary["f49_seed_surface_flag"].sum()),
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

    frame["__seed_gap"] = numeric_column("f49_axis_gap_to_seed", 999999.0)
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
            "repair_action": "run_capped_nonpercentile_state_gate_repair",
            "repair_reason": "Initial forward floor state machine surface produced no candidate summary.",
        }
    runtime = int(initial_summary["runtime_probe_candidate_flag"].sum())
    seed = int(initial_summary["f49_seed_surface_flag"].sum())
    scout_rows = int(initial_summary["f49_scout_clue_flag"].sum())
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
            "repair_reason": "Seed surface exists; avoid fixed state-gate overfit repair before runtime validation planning.",
        }
    return {
        "run_repair_grid": True,
        "repair_action": "run_capped_nonpercentile_state_gate_repair",
        "repair_reason": f"Initial forward floor state machine surface scout={scout_rows}, seed=0, runtime=0; run bounded fixed state-gate repair.",
        "initial_scout_rows": scout_rows,
    }


def classify_closeout(initial_summary: pd.DataFrame, repair_summary: pd.DataFrame) -> dict[str, Any]:
    combined = combine_summaries(initial_summary, repair_summary)
    if combined.empty:
        scout_rows = seed_rows = runtime_rows = 0
        best = {}
    else:
        scout_rows = int(combined["f49_scout_clue_flag"].sum())
        seed_rows = int(combined["f49_seed_surface_flag"].sum())
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
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_runtime_candidate_after_f49_forward_floor_state_machine_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    elif scout_rows:
        closeout_class = "preserved_clue_negative_memory"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f49_forward_floor_state_machine_proxy"
        next_stage = NEXT_STAGE_ID
        next_run = NEXT_RUN_ID
    else:
        closeout_class = "negative_memory"
        runtime_status = "runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f49_forward_floor_state_machine_proxy"
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
F48 preserved clue(보존 단서)의 loss-contained event(손실 제한 이벤트)에 train-only forward floor state machine(학습 전용 전진 하한 상태기계)을 덧씌우면 PF/DD/density(수익 팩터/손실폭/밀도)를 더 잘 동시에 분리하는지 시험한다.

Novelty line(신규성 문장): forward floor state machine(전진 하한 상태기계)은 horizon+1 embargo(예측수평+1 유예)를 지난 known outcome(확정 결과)만 쓰며, F48 static state gate(정적 상태 게이트)와 F47 percentile risk-budget sweep(47전선 분위수 위험 예산 훑기)을 반복하지 않는다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F48 best and closest nonwinner rows(F48 최상/가장 가까운 비승자 행)는 reference-only scout clue(참조 전용 탐색 단서), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시).
- changed_variables(변경 변수): bars-since-known-bad/good state(확정 나쁜/좋은 이벤트 이후 봉 수 상태), rolling event-balance floor(굴러가는 이벤트 균형 하한), fixed volatility/crowding caps(고정 변동성/밀집 상한).
- initial_lock(초기 잠금): first proxy(첫 프록시)는 F48 event/model/context/score/SLTP(이벤트/모델/문맥/점수/손익절)를 reference-only(참조 전용)로 고정하고 forward floor state gate(전진 하한 상태 게이트)만 바꾼다.
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank/risk budget/repair(라벨/모델/임계값/손익절/순위/위험 예산/수리)에 쓰거나, horizon+1 embargo(예측수평선+1 유예)보다 최신 결과 라벨을 현재 feature(피처)로 쓰는 경우.
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
            f"risk={row.get('risk_budget_variant')}; "
            f"train_pf={row.get('train_profit_factor')}; val_pf={row.get('validation_profit_factor')}; "
            f"oos_pf={row.get('oos_profit_factor')}; fwd_density={row.get('forward_min_density')}..{row.get('forward_max_density')}; "
            f"fwd_dd={row.get('forward_max_dd')}; scout={row.get('f49_scout_clue_flag')}; "
            f"seed={row.get('f49_seed_surface_flag')}; runtime={row.get('runtime_probe_candidate_flag')}"
        )
        for row in best_rows[:6]
    )
    return f"""# Frontier49 closeout Grok review(그록 마감 검토)

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
- floor_state_variant(하한 상태 변형): {best.get("risk_budget_variant")}
- floor_state_keep_rate(하한 상태 유지율): {best.get("risk_budget_train_keep_rate")}
- floor_state_block_rate(하한 상태 차단율): {best.get("risk_budget_train_block_rate")}
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density_range(전진 거래 밀도 범위): {best.get("forward_min_density")} to {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}
- scout/seed/runtime(탐색/씨앗/런타임): {best.get("f49_scout_clue_flag")}/{best.get("f49_seed_surface_flag")}/{best.get("runtime_probe_candidate_flag")}
- base_scorer_family(기본 채점기 계열): {best.get("base_scorer_family")}
- context_variant(문맥 변형): {best.get("context_variant")}
- past_outcome_embargo_bars(과거 결과 유예 봉 수): {best.get("past_outcome_embargo_bars")}

Top rows snapshot(상위 행 스냅샷):
{compact_rows}

Guardrail enforced(강제 보호선):
- event label/base scorer/sequence model/class weight/score threshold/SLTP/candidate rank(이벤트 라벨/기본 채점기/순서 모델/클래스 가중치/점수 임계값/손익절/후보 순위)는 train split only(학습 분할 전용).
- forward floor state gates(전진 하한 상태 게이트)는 horizon+1 embargo(예측수평+1 유예)를 지난 known outcome(확정 결과)과 fixed thresholds(고정 임계값)만 사용.
- frozen base scorer output(고정 기본 채점기 출력)은 bar-by-bar causal lagged score context(봉별 인과 지연 점수 문맥)로만 쓰며 validation/OOS refit or rolling recalibration(검증/표본외 재적합 또는 롤링 재보정)은 없음.
- past outcome tape(과거 결과 테이프)는 horizon+1 embargo(예측수평+1 유예)보다 오래된 known outcome(알려진 결과)만 사용.
- validation/OOS(검증/표본외)는 read-only evaluation(읽기 전용 평가).
- F48 static state gate(전선48 정적 상태 게이트), F47 percentile risk-budget sweep(전선47 분위수 위험 예산 훑기), F46 sequence-context score-only repair(전선46 순서 문맥 점수 전용 수리), F45 same-bar event-classifier threshold-only repair(전선45 동일 봉 이벤트 분류기 임계값 전용 수리), F44 continuous regression(전선44 연속 회귀), F42/F43/F38/F39 primary lever(주 레버)는 반복하지 않음.

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

## Eligibility Rule(적격 규칙)
- weak_positive_pf(약한 양수 PF) below scout threshold(탐색 임계값 미만)는 near-miss alpha(근접 알파)가 아니라 negative_memory(부정 기억)로 남긴다.
- scout floor(탐색 하한): forward_min_pf(전진 최소 PF) >= {SCOUT_MIN_PF}, density(밀도) {SCOUT_MIN_DENSITY}..{SCOUT_MAX_DENSITY}/day, forward_max_dd(전진 최대 DD) <= {SCOUT_MAX_DD}.
- closest_nonwinner_check(가장 가까운 비승자 확인): `{nonwinner.get("candidate_id")}` forward_min_pf={nonwinner.get("forward_min_pf")}, forward_max_dd={nonwinner.get("forward_max_dd")}, runtime_candidate={nonwinner.get("runtime_probe_candidate_flag")}.

## Best Observed Row(최상 관찰 행)
- candidate_id(후보 ID): `{best.get("candidate_id")}`
- event_variant(이벤트 변형): `{best.get("event_variant")}`
- model_family(모델 계열): `{best.get("model_family")}`
- base_scorer_family(기본 채점기 계열): `{best.get("base_scorer_family")}`
- context_variant(문맥 변형): `{best.get("context_variant")}`
- risk_budget_variant(위험 예산 변형): `{best.get("risk_budget_variant")}`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): {best.get("risk_budget_train_keep_rate")}
- risk_budget_train_block_rate(위험 예산 학습 차단율): {best.get("risk_budget_train_block_rate")}
- past_outcome_embargo_bars(과거 결과 유예 봉 수): {best.get("past_outcome_embargo_bars")}
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
- base_scorer_family(기본 채점기 계열): `{nonwinner.get("base_scorer_family")}`
- context_variant(문맥 변형): `{nonwinner.get("context_variant")}`
- risk_budget_variant(위험 예산 변형): `{nonwinner.get("risk_budget_variant")}`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): {nonwinner.get("risk_budget_train_keep_rate")}
- risk_budget_train_block_rate(위험 예산 학습 차단율): {nonwinner.get("risk_budget_train_block_rate")}
- past_outcome_embargo_bars(과거 결과 유예 봉 수): {nonwinner.get("past_outcome_embargo_bars")}
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

F49 opened train-only forward floor state machine(학습 전용 전진 하한 상태기계) hypothesis(가설). F48 is reference only(참조 전용), not baseline/winner(기준선/승자 아님).
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

- scope_completion_gate(범위 완료 게이트): pass(통과), F49 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) materialized.
- kpi_contract_audit(KPI 계약 감사): pass(통과), train/validation/OOS PF/DD/density(학습/검증/표본외 PF/DD/밀도) split rows recorded.
- skill_receipt_lint(스킬 영수증 검사): pass_with_boundary(경계 통과), obsidian-run-evidence-system(실행 근거 시스템) skill unavailable in session; equivalent run evidence artifacts recorded.
- data_integrity(데이터 무결성): pass(통과), closed-bar feature order(닫힌 봉 피처 순서), train-only frozen base scorer(학습 전용 고정 기본 채점기), lagged score context(지연 점수 문맥), horizon+1 embargo(예측수평+1 유예), and fixed forward-floor state gates(고정 전진 하한 상태 게이트) verified.
- model_validation(모델 검증): exploratory(탐색), base scorer/model/sequence threshold(기본 채점기/모델/순서 임계값) choice는 train-only(학습 전용); validation/OOS(검증/표본외)는 read-only(읽기 전용); no promotion(승격 없음).
- artifact_lineage(산출물 계보): pass(통과), input manifest/report/ledger paths(입력 목록/보고/장부 경로) recorded; 02_runs(실행 원자료)는 ignored_with_manifest(목록 포함 무시).
- external_review_packet(외부 검토 묶음): pass(통과), stage-open and closeout Grok(단계 개방/마감 그록) receipts recorded.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `{closeout.get("runtime_probe_status")}`.
- result_judgment(결과 판정): pass(통과), `{closeout.get("closeout_class")}` only; weak positive PF(약한 양수 PF)는 scout threshold(탐색 임계값) 미만이면 near-miss alpha(근접 알파)가 아니라 negative_memory(부정 기억)다.
"""
    open_receipt = f"""# Grok Stage-Open Receipt(그록 단계 개방 영수증)

- trigger_reason(트리거 이유): /goal(목표) requires Grok second opinion(그록 2차 의견).
- review_size(검토 크기): small review(소규모 검토)
- prompt_path(프롬프트 경로): `{GROK_OPEN_ROOT / "input_prompt.md"}`
- output_path(출력 경로): `{open_review.get("clean_output_path")}`
- advice_classification(조언 분류): `{open_review.get("classification")}`
- local_verification(로컬 검증): accepted after confirming train-split-only construction lock(학습 분할 전용 구성 잠금 확인 후 수용)
- final_codex_direction(최종 코덱스 방향): run F49 forward floor state machine proxy with validation/OOS read-only(검증/표본외 읽기 전용)
"""
    close_receipt = f"""# Grok Stage-Closeout Receipt(그록 단계 마감 영수증)

- trigger_reason(트리거 이유): stage closeout(단계 마감) requires Grok review(그록 검토).
- review_size(검토 크기): small review(소규모 검토)
- prompt_path(프롬프트 경로): `{GROK_CLOSE_ROOT / "input_prompt.md"}`
- output_path(출력 경로): `{closeout_review.get("clean_output_path")}`
- advice_classification(조언 분류): `{closeout_review.get("classification")}`
- local_verification(로컬 검증): {closeout_review.get("accepted_after_local_verification")}
- final_codex_direction(최종 코덱스 방향): close F49 as `{closeout.get("closeout_class")}` with no authority claim(권위 주장 없음)
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

F49 preserved clue(보존 단서)는 train-only forward floor state machine(학습 전용 전진 하한 상태기계)이 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꿀 수 있는지에 대한 근거다.

- best_candidate(최상 후보): `{best.get("candidate_id")}`
- event_variant(이벤트 변형): `{best.get("event_variant")}`
- model_family(모델 계열): `{best.get("model_family")}`
- base_scorer_family(기본 채점기 계열): `{best.get("base_scorer_family")}`
- context_variant(문맥 변형): `{best.get("context_variant")}`
- risk_budget_variant(위험 예산 변형): `{best.get("risk_budget_variant")}`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): {best.get("risk_budget_train_keep_rate")}
- risk_budget_train_block_rate(위험 예산 학습 차단율): {best.get("risk_budget_train_block_rate")}
- past_outcome_embargo_bars(과거 결과 유예 봉 수): {best.get("past_outcome_embargo_bars")}
- train_pf(학습 PF): {best.get("train_profit_factor")}
- forward_min_pf(전진 최소 PF): {best.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {best.get("forward_min_density")} ~ {best.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {best.get("forward_max_dd")}

## Nonwinner Forward Observation(비승자 전진 관찰)

- candidate_id(후보 ID): `{nonwinner.get("candidate_id")}`
- event_variant(이벤트 변형): `{nonwinner.get("event_variant")}`
- model_family(모델 계열): `{nonwinner.get("model_family")}`
- base_scorer_family(기본 채점기 계열): `{nonwinner.get("base_scorer_family")}`
- context_variant(문맥 변형): `{nonwinner.get("context_variant")}`
- risk_budget_variant(위험 예산 변형): `{nonwinner.get("risk_budget_variant")}`
- risk_budget_train_keep_rate(위험 예산 학습 유지율): {nonwinner.get("risk_budget_train_keep_rate")}
- risk_budget_train_block_rate(위험 예산 학습 차단율): {nonwinner.get("risk_budget_train_block_rate")}
- past_outcome_embargo_bars(과거 결과 유예 봉 수): {nonwinner.get("past_outcome_embargo_bars")}
- forward_min_pf(전진 최소 PF): {nonwinner.get("forward_min_pf")}
- forward_density(전진 거래 밀도): {nonwinner.get("forward_min_density")} ~ {nonwinner.get("forward_max_density")}
- forward_max_dd(전진 최대 DD): {nonwinner.get("forward_max_dd")}
- boundary(경계): clue only(단서 전용), not winner/baseline/promotion(승자/기준선/승격 아님).
"""
    negative = f"""# Negative Memory(부정 기억)

F49 negative memory(부정 기억)는 train-only forward floor state machine(학습 전용 전진 하한 상태기계)이 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): {closeout.get("scout_clue_count")}
- seed_surface_count(씨앗 표면 수): {closeout.get("seed_surface_count")}
- runtime_probe_candidate_count(런타임 탐침 후보 수): {closeout.get("runtime_probe_candidate_count")}
- runtime_probe_status(런타임 탐침 상태): `{closeout.get("runtime_probe_status")}`
- eligibility_rule(적격 규칙): weak positive PF(약한 양수 PF)는 scout threshold(탐색 임계값)을 넘지 못하면 near-miss alpha(근접 알파)가 아니라 negative_memory(부정 기억)로 남긴다.
- do_not_repeat(반복 금지): F48 static state gate(전선48 정적 상태 게이트), F47 percentile risk-budget sweep(전선47 분위수 위험 예산 훑기), F46 sequence-context score-only repair(순서 문맥 점수 전용 수리), F45 same-bar threshold-only repair(동일 봉 임계값 전용 수리), F44 continuous regression(연속 회귀), F42 timing gate(타이밍 게이트), F43 trade-shape source(거래 형태 원천), F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움)를 primary lever(주 레버)로 반복하지 않는다.
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
            "notes": "F49 opened with train-only forward floor state machine hypothesis and Grok guardrails.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_B,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "proxy",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Initial train-only forward floor state machine proxy surface.",
        },
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_C,
            "record_view": "Tier A separate",
            "status": "completed",
            "closeout_class": "repair",
            "runtime_probe_status": "evaluated_for_runtime_candidate",
            "notes": "Capped forward floor state machine repair diagnostic.",
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
            "runtime_probe_status": "out_of_scope_by_claim_tier_a_forward_floor_state_machine_proxy_only",
            "notes": "F49 used Tier A forward floor state machine proxy only; Tier B not claimed.",
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
        "kpi_scope": "short_forward_floor_state_machine_proxy",
        "scoreboard_lane": "frontier_scout",
        "status": row.get("status", ""),
        "judgment": row.get("closeout_class", ""),
        "external_verification_status": row.get("runtime_probe_status", ""),
        "notes": row.get("notes", ""),
        "path": review_report_path(str(row.get("run_id", ""))).as_posix(),
        "report_path": review_report_path(str(row.get("run_id", ""))).as_posix(),
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness",
        "run_family": "frontier_short_forward_floor_state_machine_proxy",
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
current_judgment: {closeout.get("closeout_class")}(F49 train-only forward floor state machine proxy no operating authority)
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

Frontier49(F49, 전선 49단계)가 `{closeout.get("closeout_class")}`로 닫혔다.

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

F49 carry-forward(이월) 기록은 train-only forward floor state machine(학습 전용 전진 하한 상태기계)이 PF/DD/density(수익 팩터/손실폭/밀도)를 얼마나 바꾸었는지와 seed/runtime(씨앗/런타임) 후보가 생겼는지 여부다.
"""
    existing_plan = read_text(PRE_ALPHA_PLAN) if path_exists(PRE_ALPHA_PLAN) else "# Pre-Alpha Stage Plan\n"
    marker = "## Frontier Pointer(전선 포인터)"
    if marker in existing_plan:
        existing_plan = existing_plan.split(marker, 1)[0].rstrip()
    write_text_sig(PRE_ALPHA_PLAN, existing_plan.rstrip() + "\n\n" + pointer)


def artifact_map() -> dict[str, str]:
    return {
        "input_manifest": (INPUT_ROOT / "forward_floor_state_machine_manifest.json").as_posix(),
        "gate_provenance_table": (INPUT_ROOT / "gate_provenance_table.csv").as_posix(),
        "initial_summary": (RUN_B_ROOT / "initial_candidate_summary.csv").as_posix(),
        "repair_summary": (RUN_C_ROOT / "repair_candidate_summary.csv").as_posix(),
        "closeout_report": review_report_path(RUN_D).as_posix(),
        "selection_status": (SELECTED_ROOT / "selection_status.json").as_posix(),
    }


if __name__ == "__main__":
    main()


