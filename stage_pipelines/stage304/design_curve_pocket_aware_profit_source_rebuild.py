from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage290 import design_materialize_payoff_weighted_edge_model_rebuild as s290  # noqa: E402
from stage_pipelines.stage293 import design_materialize_profit_scale_density_calibration_rebuild as s293  # noqa: E402


STAGE_ID = "304_onnx_candidate_campaign__curve_pocket_aware_profit_source_rebuild"
RUN_ID = "run304A_design_curve_pocket_aware_profit_source_rebuild_v1"
RUN_NUMBER = "run304A"
SOURCE_STAGE_ID = "303_onnx_candidate_campaign__regime_balanced_profit_scale_router"
SOURCE_RUN_ID = "run303C_review_regime_balanced_profit_scale_router_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_curve_pocket_aware_profit_source_candidates_materialized_no_selection"
JUDGMENT = "curve_pocket_aware_profit_source_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run304B_execute_curve_pocket_aware_profit_source_mt5_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
MODEL_DIR = RUN_ROOT / "models"
HANDOFF_DIR = RUN_ROOT / "handoff"

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run303C_regime_balanced_profit_scale_router_review_stage304_open_report.md"
SOURCE_SCOREBOARD = SOURCE_STAGE / "02_runs" / "run303C" / "regime_balanced_profit_scale_router_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_STAGE / "02_runs" / "run303C" / "stage304_seed_queue.csv"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_ROOT / "model_receipt.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run304A_curve_pocket_aware_profit_source_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

FEATURE_ORDER = ("route_signal_value",)
MODEL_RECEIPT_COLUMNS = (
    "model_key",
    "model_family",
    "prediction_kind",
    "train_rows",
    "feature_count",
    "target",
    "selection_policy",
    "feature_order_hash",
    "claim_boundary",
)
MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage304_branch_id",
    "stage303_branch_id",
    "stage301_branch_id",
    "stage293_branch_id",
    "stage291_branch_id",
    "stage290_branch_id",
    "package_id",
    "queue_role",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "model_artifact_path",
    "model_artifact_hash",
    "model_feature_order_path",
    "model_feature_order_hash",
    "direction_surface_hash",
    "direction_feature_order_hash",
    "max_hold_bars",
    "close_on_flat_signal",
    "same_direction_reentry_cooldown_bars",
    "atr_sltp_enabled",
    "atr_period",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "atr_min_stop_points",
    "atr_max_stop_points",
    "atr_min_take_profit_points",
    "atr_max_take_profit_points",
    "exit_risk_overlay_enabled",
    "exit_risk_close_long_feature_index",
    "exit_risk_close_short_feature_index",
    "exit_risk_close_threshold",
    "exit_risk_min_hold_bars",
    "exit_risk_max_hold_feature_index",
    "model_risk_sizing_enabled",
    "model_risk_min_pct",
    "model_risk_max_pct",
    "model_risk_confidence_floor",
    "model_risk_confidence_ceiling",
    "model_risk_fallback_lot",
    "fixed_lot",
    "approx_validation_trades_per_day",
    "approx_oos_trades_per_day",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
BRANCH_COLUMNS = (
    "branch_id",
    "package_id",
    "source_stage_id",
    "source_run_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "feature_surface",
    "model_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "failure_memory_plan",
    "claim_boundary",
)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    model_family: str
    prediction_kind: str
    dataset_id: str
    max_hold_bars: int
    precondition: str
    sample_weight_policy: str
    objective_surface: str
    hypothesis: str
    changed_variables: str
    target_density: float
    modes: tuple[str, ...]
    fixed_lot: float
    atr_sltp_enabled: bool
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_sizing_enabled: bool
    model_risk_max_pct: float
    same_direction_reentry_cooldown_bars: int = 0
    close_on_flat_signal: bool = True
    atr_period: int = 14
    model_risk_min_pct: float = 0.006
    model_risk_confidence_floor: float = 0.54
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8-sig" if bom else "utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def safe_upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    try:
        upsert_csv_rows(path, columns, rows, key=key)
        return
    except OSError:
        existing = read_csv_dicts(path)
        incoming = {str(row.get(key, "")): row for row in rows}
        merged = [row for row in existing if str(row.get(key, "")) not in incoming]
        merged.extend(rows)
        io_path(path.parent).mkdir(parents=True, exist_ok=True)
        with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
            writer.writeheader()
            for row in merged:
                writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            package_id="cp304A_histgb_smooth_cash_density65_hold4_scale_surface",
            model_family="histgb_return_curve_weighted",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=4,
            precondition="smooth_session_balance",
            sample_weight_policy="runtime_gap_recency",
            objective_surface="smooth_curve_router",
            hypothesis="Curve-pocket-aware train folds may retain a steadier cash-session edge before risk scale is added.",
            changed_variables="HistGB return model, smooth-session precondition, curve-pocket WFO score, density 6.5, hold4, fixed lot 0.20.",
            target_density=6.5,
            modes=("smooth_curve_router", "quality_veto_direct", "runtime_calibrated_inverse"),
            fixed_lot=0.20,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.55,
            atr_take_profit_multiplier=3.40,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
        ),
        CandidateSpec(
            package_id="cp304B_extratrees_quality_veto_density55_hold4_scale_surface",
            model_family="extratrees_return_curve_veto",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=4,
            precondition="cash_midvol_profit",
            sample_weight_policy="runtime_gap_side_balance_recency",
            objective_surface="two_head_router",
            hypothesis="Nonlinear tree voting can veto the repeated low-PF pockets while preserving a mid-density cash source.",
            changed_variables="ExtraTrees return model, two-head quality router, cash mid-vol precondition, density 5.5, fixed lot 0.22.",
            target_density=5.5,
            modes=("two_head_router", "quality_veto_direct", "smooth_curve_router"),
            fixed_lot=0.22,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.65,
            atr_take_profit_multiplier=3.75,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
        ),
        CandidateSpec(
            package_id="cp304C_histgb_classifier_density_router_hold6_surface",
            model_family="histgb_multiclass_curve_density",
            prediction_kind="multiclass_probability",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="dense_band",
            sample_weight_policy="runtime_gap_tail_side_balance",
            objective_surface="density_profit_scale_router",
            hypothesis="A probability surface can rebalance direction and density so smoothness is not bought by too few trades.",
            changed_variables="HistGB multiclass model, density-profit router, dense-band precondition, density 7.5, hold6, fixed lot 0.18.",
            target_density=7.5,
            modes=("density_profit_scale_router", "smooth_curve_router", "runtime_calibrated_inverse"),
            fixed_lot=0.18,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.75,
            atr_take_profit_multiplier=4.10,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.020,
        ),
        CandidateSpec(
            package_id="cp304D_histgb_return_profit_scale_density85_hold6_surface",
            model_family="histgb_return_curve_scale",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="runtime_gap_balanced",
            sample_weight_policy="runtime_gap_tail_recency",
            objective_surface="profit_scale_direct",
            hypothesis="Profit scale should be tested with a curve penalty in selection rather than with post-hoc risk multipliers only.",
            changed_variables="HistGB return model, runtime-gap balanced precondition, profit-scale direct mode, density 8.5, model risk cap 2.8%.",
            target_density=8.5,
            modes=("profit_scale_direct", "density_profit_scale_router", "quality_veto_direct"),
            fixed_lot=0.16,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.85,
            atr_take_profit_multiplier=4.60,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.028,
            same_direction_reentry_cooldown_bars=1,
            close_on_flat_signal=False,
        ),
        CandidateSpec(
            package_id="cp304E_extratrees_inverse_pocket_guard_density45_hold3_surface",
            model_family="extratrees_return_curve_guard",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=3,
            precondition="controlled_tail",
            sample_weight_policy="runtime_gap_tail_side_balance",
            objective_surface="runtime_calibrated_inverse",
            hypothesis="The inverse source is not discarded, but it must pass a controlled-tail pocket guard before scale is trusted.",
            changed_variables="ExtraTrees return model, controlled-tail inverse guard, density 4.5, hold3, fixed lot 0.24.",
            target_density=4.5,
            modes=("runtime_calibrated_inverse", "conditional_inverse", "quality_veto_inverse"),
            fixed_lot=0.24,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.45,
            atr_take_profit_multiplier=3.20,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
        ),
        CandidateSpec(
            package_id="cp304F_histgb_aggressive_curve_capped_density95_hold8_surface",
            model_family="histgb_return_aggressive_curve_capped",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=8,
            precondition="dense_band",
            sample_weight_policy="runtime_gap_tail_recency",
            objective_surface="density_profit_scale_router",
            hypothesis="An aggressive branch is allowed only if the fold objective keeps local pockets capped at the 9-10 trades/day edge.",
            changed_variables="HistGB return model, density-profit router, dense band, density 9.5, hold8, capped model risk 3.0%.",
            target_density=9.5,
            modes=("density_profit_scale_router", "profit_scale_direct", "runtime_calibrated_inverse"),
            fixed_lot=0.16,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.95,
            atr_take_profit_multiplier=5.00,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            same_direction_reentry_cooldown_bars=2,
            close_on_flat_signal=False,
        ),
    ]


def curve_aware_fold_selection_score(metrics: Sequence[Mapping[str, Any]], spec: CandidateSpec) -> float:
    if not metrics:
        return -1_000_000.0
    nets = [float(row["net_bp"]) for row in metrics]
    densities = [float(row["trades_per_day"]) for row in metrics]
    pfs = [float(row["pf"]) for row in metrics]
    recoveries = [float(row["recovery"]) for row in metrics]
    worst20 = [float(row["worst_rolling_20_bp"]) for row in metrics]
    worst50 = [float(row["worst_rolling_50_bp"]) for row in metrics]
    worst_months = [float(row["worst_month_bp"]) for row in metrics]
    underwater = [float(row["underwater_ratio"]) for row in metrics]
    density_penalty = sum(abs(value - spec.target_density) * 75.0 for value in densities)
    density_penalty += sum(1800.0 + abs(value - spec.target_density) * 220.0 for value in densities if value < 4.0 or value > 10.0)
    pocket_penalty = sum(abs(min(0.0, value)) * 0.95 for value in worst20)
    pocket_penalty += sum(abs(min(0.0, value)) * 0.62 for value in worst50)
    month_penalty = sum(abs(min(0.0, value)) * 0.42 for value in worst_months)
    water_penalty = sum(max(0.0, value - 0.78) * 520.0 for value in underwater)
    worst_fold_penalty = abs(min(0.0, min(nets))) * 1.25
    consistency_bonus = sum(1 for value in nets if value > 0.0) / len(nets) * 620.0
    scale_bonus = max(0.0, sum(nets)) * 0.16
    pf_bonus = sum(max(0.0, value - 1.0) * 420.0 for value in pfs)
    recovery_bonus = sum(max(0.0, min(value, 8.0)) * 40.0 for value in recoveries)
    return float(
        sum(nets)
        + scale_bonus
        + consistency_bonus
        + pf_bonus
        + recovery_bonus
        - density_penalty
        - pocket_penalty
        - month_penalty
        - water_penalty
        - worst_fold_penalty
    )


def configure_stage293_helpers() -> None:
    s293.MODEL_DIR = MODEL_DIR
    s293.fold_selection_score = curve_aware_fold_selection_score  # type: ignore[assignment]


def split_metrics(scored: pd.DataFrame, quantile: float, mode: str, hold_limit: int, split: str) -> tuple[dict[str, Any], np.ndarray, float]:
    part = scored.loc[scored["split"].astype(str).eq(split)].copy()
    train_part = scored.loc[scored["split"].astype(str).eq("train")].copy()
    threshold = s293.threshold_for_quantile(train_part, quantile, mode)
    signal = s293.build_signal(part, threshold, mode)
    return s290.curve_metrics(part, signal, hold_limit), signal, threshold


def materialize_payload(prepared: Any, scored: pd.DataFrame, quantile: float, threshold: float, mode: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    spec: CandidateSpec = prepared.spec
    signal = s293.build_signal(scored, threshold, mode)
    runtime = scored.copy()
    branch_id = f"run304A_{spec.package_id.replace('_surface', '')}"
    runtime["stage304_branch_id"] = branch_id
    runtime["stage303_branch_id"] = branch_id
    runtime["stage301_branch_id"] = branch_id
    runtime["stage293_branch_id"] = branch_id
    runtime["stage291_branch_id"] = branch_id
    runtime["stage290_branch_id"] = branch_id
    runtime["materialized_branch_id"] = branch_id
    runtime["package_id"] = spec.package_id
    runtime["queue_role"] = "curve_pocket_aware_profit_source_surface"
    runtime["candidate_decision_score"] = s293.activation_score(runtime, mode)
    runtime["direction_signal_value"] = signal
    runtime["route_signal_value"] = signal
    runtime["route_signal_label"] = [s290.signal_label(int(value)) for value in signal]
    runtime["signal_active"] = (signal != 0).astype("int8")
    runtime["model_risk_pct"] = spec.model_risk_max_pct if spec.model_risk_sizing_enabled else 0.0
    runtime["max_hold_bars"] = spec.max_hold_bars
    runtime["close_on_flat_signal"] = spec.close_on_flat_signal
    runtime["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    surface_identity = {
        "package_id": spec.package_id,
        "model_family": spec.model_family,
        "prediction_kind": spec.prediction_kind,
        "dataset_id": spec.dataset_id,
        "selection_quantile": quantile,
        "selection_threshold": threshold,
        "mode": mode,
        "precondition": spec.precondition,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "fixed_lot": spec.fixed_lot,
        "atr_sltp_enabled": spec.atr_sltp_enabled,
        "atr_stop_multiplier": spec.atr_stop_multiplier,
        "atr_take_profit_multiplier": spec.atr_take_profit_multiplier,
        "model_risk_sizing_enabled": spec.model_risk_sizing_enabled,
        "model_risk_max_pct": spec.model_risk_max_pct,
        "feature_order_hash": ordered_hash(prepared.feature_order),
        "direction_feature_order_hash": ordered_hash(FEATURE_ORDER),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(surface_identity, sort_keys=True).encode("utf-8")).hexdigest()
    runtime["direction_surface_hash"] = surface_hash
    runtime["variant_decision_surface_hash"] = surface_hash
    runtime["direction_feature_order_hash"] = ordered_hash(FEATURE_ORDER)
    runtime["model_feature_order_hash"] = ordered_hash(prepared.feature_order)
    runtime["payload_claim_boundary"] = BOUNDARY
    drop_columns = [
        name
        for name in runtime.columns
        if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}
    ]
    runtime = runtime.drop(columns=drop_columns, errors="ignore")
    tier_a = runtime.copy()
    tier_a["tier_scope"] = "Tier A"
    tier_b = runtime.copy()
    tier_b["tier_scope"] = "Tier B"
    payload = pd.concat([tier_a, tier_b], ignore_index=True)
    return payload, surface_identity | {"direction_surface_hash": surface_hash}


def density_gate(validation: Mapping[str, Any], oos: Mapping[str, Any]) -> str:
    ok = 4.0 <= float(validation["trades_per_day"]) <= 10.0 and 4.0 <= float(oos["trades_per_day"]) <= 10.0
    return "passed" if ok else "failed"


def proxy_edge_gate(validation: Mapping[str, Any], oos: Mapping[str, Any]) -> str:
    ok = (
        float(validation["net_bp"]) > 0.0
        and float(oos["net_bp"]) > 0.0
        and float(validation["pf"]) >= 1.05
        and float(oos["pf"]) >= 1.02
    )
    return "passed" if ok else "failed"


def curve_proxy_gate(validation: Mapping[str, Any], oos: Mapping[str, Any]) -> str:
    ok = (
        float(validation["worst_rolling_20_bp"]) >= -260.0
        and float(oos["worst_rolling_20_bp"]) >= -260.0
        and float(validation["worst_rolling_50_bp"]) >= -520.0
        and float(oos["worst_rolling_50_bp"]) >= -520.0
        and float(validation["positive_month_share"]) >= 0.50
        and float(oos["positive_month_share"]) >= 0.45
        and float(validation["underwater_ratio"]) <= 0.90
        and float(oos["underwater_ratio"]) <= 0.92
    )
    return "passed" if ok else "failed"


def risk_manifest_fields(spec: CandidateSpec) -> dict[str, Any]:
    return {
        "atr_sltp_enabled": int(spec.atr_sltp_enabled),
        "atr_period": spec.atr_period,
        "atr_stop_multiplier": spec.atr_stop_multiplier,
        "atr_take_profit_multiplier": spec.atr_take_profit_multiplier,
        "atr_min_stop_points": 0.0,
        "atr_max_stop_points": 0.0,
        "atr_min_take_profit_points": 0.0,
        "atr_max_take_profit_points": 0.0,
        "exit_risk_overlay_enabled": 0,
        "exit_risk_close_long_feature_index": -1,
        "exit_risk_close_short_feature_index": -1,
        "exit_risk_close_threshold": 0.50,
        "exit_risk_min_hold_bars": 0,
        "exit_risk_max_hold_feature_index": -1,
        "model_risk_sizing_enabled": int(spec.model_risk_sizing_enabled),
        "model_risk_min_pct": spec.model_risk_min_pct,
        "model_risk_max_pct": spec.model_risk_max_pct,
        "model_risk_confidence_floor": spec.model_risk_confidence_floor,
        "model_risk_confidence_ceiling": spec.model_risk_confidence_ceiling,
        "model_risk_fallback_lot": spec.model_risk_fallback_lot,
        "fixed_lot": spec.fixed_lot,
    }


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    configure_stage293_helpers()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    model_receipts: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    dataset_cache: dict[str, pd.DataFrame] = {}
    for index, spec in enumerate(candidate_specs(), start=1):
        frame = dataset_cache.setdefault(spec.dataset_id, s290.load_dataset(spec.dataset_id))
        mode, quantile, score, fold_rows, wfo_summary = s293.choose_wfo_mode(spec, frame)
        train = frame.loc[frame["split"].astype(str).eq("train")].copy()
        prepared = s293.train_prepared(spec, train, seed=3040 + index, persist=True)
        scored = s293.score_edges(prepared, frame)
        train_scored = scored.loc[scored["split"].astype(str).eq("train")].copy()
        threshold = s293.threshold_for_quantile(train_scored, quantile, mode)
        validation_metrics, _validation_signal, _ = split_metrics(scored, quantile, mode, spec.max_hold_bars, "validation")
        oos_metrics, _oos_signal, _ = split_metrics(scored, quantile, mode, spec.max_hold_bars, "oos")
        payload, surface_identity = materialize_payload(prepared, scored, quantile, threshold, mode)
        branch_id = f"run304A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "stage304_branch_id": branch_id,
                "package_id": spec.package_id,
                "feature_order": list(FEATURE_ORDER),
                "feature_order_hash": ordered_hash(FEATURE_ORDER),
                "model_feature_order": prepared.feature_order,
                "model_feature_order_hash": ordered_hash(prepared.feature_order),
                "selection_quantile": quantile,
                "selection_threshold": threshold,
                "selection_mode": mode,
                "precondition": spec.precondition,
                "max_hold_bars": spec.max_hold_bars,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for MT5 probe; model artifact retained for Adapter/ONNX only if candidate survives",
                "claim_boundary": BOUNDARY,
                "surface_identity": surface_identity,
            },
        )
        candidate_supply = s290.supply_rows_for_payload(payload, spec)  # type: ignore[arg-type]
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        for fold_row in fold_rows:
            fold_row["materialized_branch_id"] = branch_id
            wfo_rows.append(fold_row)
        model_artifact_path = prepared.model_path or Path("")
        feature_order_path = prepared.feature_order_path or Path("")
        imputation_path = prepared.imputation_path or Path("")
        manifest_rows.append(
            {
                "queue_id": f"run304A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage304_branch_id": branch_id,
                "stage303_branch_id": branch_id,
                "stage301_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "curve_pocket_aware_profit_source_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": rel(model_artifact_path),
                "model_artifact_hash": sha256_file_lf_normalized(model_artifact_path) if model_artifact_path and path_exists(model_artifact_path) else "",
                "model_feature_order_path": rel(feature_order_path),
                "model_feature_order_hash": ordered_hash(prepared.feature_order),
                "direction_surface_hash": surface_identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(FEATURE_ORDER),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": int(spec.close_on_flat_signal),
                "same_direction_reentry_cooldown_bars": spec.same_direction_reentry_cooldown_bars,
                **risk_manifest_fields(spec),
                "approx_validation_trades_per_day": val_supply["approx_trades_per_day"],
                "approx_oos_trades_per_day": oos_supply["approx_trades_per_day"],
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        model_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": spec.model_family,
                "prediction_kind": spec.prediction_kind,
                "dataset_id": spec.dataset_id,
                "model_artifact_path": rel(model_artifact_path),
                "model_artifact_hash": sha256_file_lf_normalized(model_artifact_path) if model_artifact_path and path_exists(model_artifact_path) else "",
                "model_feature_order_path": rel(feature_order_path),
                "model_feature_order_hash": ordered_hash(prepared.feature_order),
                "imputation_path": rel(imputation_path),
                "imputation_hash": sha256_file_lf_normalized(imputation_path) if imputation_path and path_exists(imputation_path) else "",
                "classes": "|".join(str(item) for item in s293.LABEL_ORDER) if spec.prediction_kind == "multiclass_probability" else "return_regression",
                "payoff_weight_policy": spec.sample_weight_policy,
                "onnx_exportability_note": "Adapter package required before ONNX export; this run keeps model order and replay handoff traceable.",
            }
        )
        model_receipts.append(
            {
                "model_key": spec.package_id,
                "model_family": spec.model_family,
                "prediction_kind": spec.prediction_kind,
                "train_rows": len(train),
                "feature_count": len(prepared.feature_order),
                "target": "future_log_return_12 or label_class, train split only",
                "selection_policy": "WFO folds use curve-pocket-aware objective; validation/OOS are not used to fit model",
                "feature_order_hash": ordered_hash(prepared.feature_order),
                "claim_boundary": BOUNDARY,
            }
        )
        den_gate = density_gate(validation_metrics, oos_metrics)
        edge_gate = proxy_edge_gate(validation_metrics, oos_metrics)
        curve_gate = curve_proxy_gate(validation_metrics, oos_metrics)
        selection_score = (
            float(wfo_summary["selection_score"])
            + s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.45
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": spec.model_family,
                "prediction_kind": spec.prediction_kind,
                "mode": mode,
                "quantile": quantile,
                "threshold": threshold,
                "precondition": spec.precondition,
                "wfo_net_bp": wfo_summary["wfo_net_bp"],
                "wfo_positive_fold_share": wfo_summary["wfo_positive_fold_share"],
                "wfo_worst_fold_net_bp": wfo_summary["wfo_worst_fold_net_bp"],
                "wfo_mean_trades_per_day": wfo_summary["wfo_mean_trades_per_day"],
                "wfo_min_trades_per_day": wfo_summary["wfo_min_trades_per_day"],
                "wfo_max_trades_per_day": wfo_summary["wfo_max_trades_per_day"],
                "validation_proxy_net_bp": validation_metrics["net_bp"],
                "validation_proxy_pf": validation_metrics["pf"],
                "validation_proxy_trade_count": validation_metrics["trade_count"],
                "validation_proxy_trades_per_day": validation_metrics["trades_per_day"],
                "validation_proxy_recovery": validation_metrics["recovery"],
                "validation_proxy_worst_month_bp": validation_metrics["worst_month_bp"],
                "validation_proxy_worst_rolling_20_bp": validation_metrics["worst_rolling_20_bp"],
                "validation_proxy_worst_rolling_50_bp": validation_metrics["worst_rolling_50_bp"],
                "validation_proxy_positive_month_share": validation_metrics["positive_month_share"],
                "validation_proxy_underwater_ratio": validation_metrics["underwater_ratio"],
                "oos_proxy_net_bp": oos_metrics["net_bp"],
                "oos_proxy_pf": oos_metrics["pf"],
                "oos_proxy_trade_count": oos_metrics["trade_count"],
                "oos_proxy_trades_per_day": oos_metrics["trades_per_day"],
                "oos_proxy_recovery": oos_metrics["recovery"],
                "oos_proxy_worst_month_bp": oos_metrics["worst_month_bp"],
                "oos_proxy_worst_rolling_20_bp": oos_metrics["worst_rolling_20_bp"],
                "oos_proxy_worst_rolling_50_bp": oos_metrics["worst_rolling_50_bp"],
                "oos_proxy_positive_month_share": oos_metrics["positive_month_share"],
                "oos_proxy_underwater_ratio": oos_metrics["underwater_ratio"],
                "density_gate": den_gate,
                "proxy_edge_gate": edge_gate,
                "curve_proxy_gate": curve_gate,
                "selection_score": selection_score,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        for split_name, metrics in (("validation", validation_metrics), ("oos", oos_metrics)):
            wfo_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "fold_id": split_name,
                    "mode": mode,
                    "quantile": quantile,
                    "threshold": threshold,
                    "net_bp": metrics["net_bp"],
                    "pf": metrics["pf"],
                    "trade_count": metrics["trade_count"],
                    "trades_per_day": metrics["trades_per_day"],
                    "recovery": metrics["recovery"],
                    "worst_month_bp": metrics["worst_month_bp"],
                    "worst_rolling_20_bp": metrics["worst_rolling_20_bp"],
                    "worst_rolling_50_bp": metrics["worst_rolling_50_bp"],
                    "positive_month_share": metrics["positive_month_share"],
                    "underwater_ratio": metrics["underwater_ratio"],
                }
            )
        artifacts.extend([payload_path, handoff_path, model_artifact_path, feature_order_path, imputation_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, model_receipts, artifacts


def branch_rows_from_scoreboard(scoreboard_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    specs = {spec.package_id: spec for spec in candidate_specs()}
    rows: list[dict[str, Any]] = []
    for item in scoreboard_rows:
        spec = specs[str(item["package_id"])]
        rows.append(
            {
                "branch_id": item["materialized_branch_id"],
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "Decide whether a curve-pocket-aware profit source is worth an MT5 runtime probe.",
                "comparison_baseline": "Stage303 actual MT5 review: density passed but profit scale, efficiency, and curve conditions failed.",
                "control_variables": "US100 M5 split_v1; train-only model fit; Tier A/B paired runtime accounting; no Adapter or ONNX claim.",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Train split fits models; WFO folds select mode/quantile; validation/OOS and MT5 are evaluation.",
                "success_criteria": "minimum trades pass, 4-10 trades/day, validation and OOS positive net, PF/recovery/expectancy acceptable, no deep local curve pocket.",
                "failure_criteria": "MT5 net scale absent, density outside 4-10, PF/recovery weak, or curve has zoomed drawdown pockets.",
                "invalid_conditions": "future/label leakage, feature order mismatch, payload handoff mismatch, or missing MT5 runtime output.",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise review opens a fresh thesis or discard.",
                "evidence_plan": "experiment/data/model receipts, WFO scoreboard, payload manifest, MT5 probe queue, run304B MT5 KPI, run304C curve review.",
                "feature_surface": "FPMarkets US100 M5 proxy58 features plus score-derived route_signal_value replay.",
                "model_surface": spec.model_family,
                "decision_surface": f"{item['mode']} with {spec.precondition}",
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; model artifact retained for Adapter trace if candidate gate passes.",
                "failure_memory_plan": "Record whether model family, direction mode, density, risk scale, or curve pocket veto failed.",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    result = [
        {
            "result_subject": "Stage304 curve-pocket-aware profit source materialization",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI, Adapter package, ONNX parity",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage304 creates new curve-aware candidates; it does not select a candidate before MT5 runtime evidence.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis", "status": "passed", "evidence_path": rel(EXPERIMENT_DESIGN), "effect": "Stage303 router repair is replaced with curve-pocket-aware source construction."},
        {"gate_name": "train_only_model_boundary", "status": "passed", "evidence_path": rel(MODEL_RECEIPT), "effect": "Models are fit on train split only; validation and OOS are evaluation."},
        {"gate_name": "proxy_density_edge_curve_screen", "status": "passed" if density_pass and edge_pass and curve_pass else "partial", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "Candidates are screened for 4-10 trades/day, proxy edge, and local pocket risk before MT5."},
        {"gate_name": "mt5_runtime_probe", "status": "prepared", "evidence_path": rel(MT5_QUEUE), "effect": "run304B can execute Tier A, Tier B fallback, and actual routed total attempts."},
        {"gate_name": "adapter_package", "status": "not_started", "evidence_path": "", "effect": "No Adapter is created before a candidate gate passes."},
        {"gate_name": "onnx_readiness", "status": "not_started", "evidence_path": "", "effect": "ONNX work waits for selected candidate and Adapter package."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = sorted(scoreboard_rows, key=lambda row: float(row["selection_score"]), reverse=True)
    lines = [
        "# run304A Curve-Pocket-Aware Profit Source Materialization(304A 곡선 포켓 인식 수익 원천 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage303(303단계)의 low net profit(낮은 순수익)과 curve pocket(곡선 포켓) 실패를 좁게 수리하지 않고, WFO(walk-forward optimization, 워크포워드 최적화)에서 local pocket(국소 포켓)을 벌점으로 넣은 새 후보 6개를 MT5(메타트레이더5) 대기열로 넘긴다.",
        "",
        "| package(패키지) | mode(모드) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(거래우위) | curve(곡선) |",
        "|---|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in ordered:
        lines.append(
            "| {pkg} | {mode} | {vn:.1f} | {vtd:.2f} | {on:.1f} | {otd:.2f} | {den} | {edge} | {curve} |".format(
                pkg=row["package_id"],
                mode=row["mode"],
                vn=float(row["validation_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                on=float(row["oos_proxy_net_bp"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                den=row["density_gate"],
                edge=row["proxy_edge_gate"],
                curve=row["curve_proxy_gate"],
            )
        )
    lines.extend(["", f"- mt5_queue_rows(MT5 대기열 행): `{len(manifest_rows)}`", f"- claim_boundary(주장 경계): `{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    wfo_rows: Sequence[Mapping[str, Any]],
    model_receipts: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, manifest_rows)
    write_csv_rows(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv_rows(MODEL_SCOREBOARD, s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv_rows(CANDIDATE_SUPPLY, s293.SUPPLY_COLUMNS, supply_rows)
    write_csv_rows(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MODEL_MANIFEST, s293.MODEL_COLUMNS, model_rows)
    write_csv_rows(WFO_FOLD_SCOREBOARD, s293.WFO_COLUMNS, wfo_rows)
    write_csv_rows(MODEL_RECEIPT, MODEL_RECEIPT_COLUMNS, model_receipts)
    write_csv_rows(RESULT_JUDGMENT, s293.RESULT_COLUMNS, result)
    write_csv_rows(GATE_AUDIT, s293.GATE_COLUMNS, gates)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Curve-pocket-aware WFO selection plus balanced risk scale can produce minimum trade count, 4-10 trades/day, and steadier validation/OOS curves.",
            "decision_use": "Open or reject MT5 runtime probe candidates before Adapter and ONNX work.",
            "comparison_baseline": "Stage303 actual MT5 review with density pass but scale/efficiency/curve failures.",
            "control_variables": ["US100 M5", "split_v1", "train-only model fit", "Tier A/B paired accounting"],
            "changed_variables": ["model family", "direction mode", "precondition", "density target", "risk logic"],
            "success_criteria": ["MT5 validation and OOS positive", "minimum trade count", "4-10 trades/day", "PF/recovery/expectancy acceptable", "no deep local curve pocket"],
            "failure_criteria": ["weak net scale", "density outside 4-10", "PF/recovery weak", "local curve pocket remains deep"],
            "invalid_conditions": ["feature order mismatch", "label leakage", "MT5 runtime output missing", "report/trade parser missing"],
            "stop_conditions": ["candidate gate pass moves to Adapter package", "otherwise close and pivot without narrow repair"],
            "evidence_plan": [rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run304B MT5 KPI", "run304C curve review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "dataset_ids": sorted({row["dataset_id"] for row in scoreboard_rows}),
            "train_boundary": "model fit uses split=train only",
            "validation_oos_boundary": "validation and oos are evaluation and MT5 probe inputs",
            "feature_order_hashes": sorted({row["model_feature_order_hash"] for row in model_rows}),
            "label_future_columns_removed_from_payload": True,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts = [
        BRANCH_QUEUE,
        MODEL_SCOREBOARD,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        MODEL_MANIFEST,
        WFO_FOLD_SCOREBOARD,
        MODEL_RECEIPT,
        EXPERIMENT_DESIGN,
        DATA_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
        *payload_artifacts,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "artifacts": [rel(path) for path in artifacts if path != RUN_MANIFEST and path_exists(path)],
            "created_at_utc": created_at,
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": "stage_pipelines/stage304/design_curve_pocket_aware_profit_source_rebuild.py",
            "inputs": {
                "stage303_review": rel(SOURCE_REVIEW),
                "stage303_scoreboard": rel(SOURCE_SCOREBOARD),
                "stage304_seed_queue": rel(SOURCE_SEED_QUEUE),
            },
            "outputs": {
                "model_scoreboard": rel(MODEL_SCOREBOARD),
                "mt5_queue": rel(MT5_QUEUE),
                "report": rel(REPORT),
            },
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return artifacts


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    safe_upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "curve_pocket_aware_profit_source_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="run_id",
    )
    safe_upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "curve_pocket_aware_profit_source_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "curve_pocket_aware_profit_source",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)};proxy_rows={len(scoreboard_rows)}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_materialization_only",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    safe_upsert_csv_rows(
        STAGE_LEDGER,
        s293.STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "curve_pocket_aware_profit_source_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage304_curve_pocket_aware_profit_source_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run304A curve-pocket-aware profit source materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    safe_upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run304A_report", f"- run304A_report(304A 보고): `{rel(REPORT)}`\n- run304A_mt5_queue(304A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX) or "# Stage304 Review Index(304단계 검토 색인)\n"
    review_index = append_once(review_index, "run304A_report", f"- run304A_report(304A 보고): `{rel(REPORT)}`\n- run304A_mt5_queue(304A MT5 대기열): `{rel(MT5_QUEUE)}`\n- run304A_model_receipt(304A 모델 영수증): `{rel(MODEL_RECEIPT)}`")
    write_md(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run304A_summary",
        f"- run304A_summary(304A 요약): curve-pocket-aware profit source(곡선 포켓 인식 수익 원천) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): WFO(walk-forward optimization, 워크포워드 최적화)에서 local pocket(국소 포켓)을 벌점화하고 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었으며 selected_candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage304(304단계) run304A(304A 실행) curve-pocket-aware profit source materialization(곡선 포켓 인식 수익 원천 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run304A Curve-pocket-aware profit source materialization(304A 곡선 포켓 인식 수익 원천 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 아직 없다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    _, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, model_receipts, payload_artifacts = build_outputs()
    branch_rows = branch_rows_from_scoreboard(scoreboard_rows)
    artifacts = write_outputs(
        branch_rows,
        scoreboard_rows,
        supply_rows,
        manifest_rows,
        model_rows,
        wfo_rows,
        model_receipts,
        payload_artifacts,
        created_at,
    )
    update_docs(created_at, artifacts, manifest_rows, scoreboard_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "branch_count": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
