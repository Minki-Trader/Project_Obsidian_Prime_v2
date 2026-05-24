from __future__ import annotations

import hashlib
import json
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
from stage_pipelines.stage294 import design_materialize_mt5_outcome_relabel_directional_flip_rebuild as s294  # noqa: E402
from stage_pipelines.stage295 import design_materialize_split_consistent_outcome_distillation_rebuild as s295  # noqa: E402


STAGE_ID = "296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild"
RUN_ID = "run296A_design_density_floor_profit_expansion_rebuild_v1"
RUN_NUMBER = "run296A"
SOURCE_STAGE_ID = "295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild"
SOURCE_RUN_ID = "run295C_review_split_consistent_outcome_distillation_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
NEXT_ACTION = "run296B_execute_density_floor_profit_expansion_mt5_probe"
STATUS = "completed_density_floor_profit_expansion_candidates_materialized_no_selection"
JUDGMENT = "density_floor_profit_expansion_inputs_materialized_no_candidate_selection"
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

SOURCE_STAGE295 = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_SEED_QUEUE = SOURCE_STAGE295 / "02_runs" / "run295C" / "stage296_seed_queue.csv"
SOURCE_STAGE295_REVIEW = SOURCE_STAGE295 / "02_runs" / "run295C" / "split_consistent_outcome_distillation_review_scoreboard.csv"
SOURCE_STAGE294_MANIFEST = ROOT / "stages" / "294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild" / "02_runs" / "run294A" / "candidate_payload_manifest.csv"

PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run296A_density_floor_profit_expansion_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

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
    source_materialized_id: str
    source_package_id: str
    transform_id: str
    thesis: str
    changed_variables: str
    risk_logic: str
    target_density: float
    max_hold_bars: int
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    dataset_id: str = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"


CANDIDATES: tuple[CandidateSpec, ...] = (
    CandidateSpec(
        package_id="cp296A_cp294C_validation_counter_density8_hold4_surface",
        source_materialized_id="run294A_cp294C_cp293A_density_trimmed_flip_hold5",
        source_package_id="cp294C_cp293A_density_trimmed_flip_hold5_surface",
        transform_id="validation_counter_density8_hold4",
        thesis="cp294C has density and OOS upside; Stage296 adds validation-damage counterfeatures without dropping below density floor.",
        changed_variables="wider not-edge cash band, moderate volatility, breadth guard, side alignment, target 8.5 active trades/day, hold4.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;validation_damage_countermodel=true",
        target_density=8.5,
        max_hold_bars=4,
    ),
    CandidateSpec(
        package_id="cp296B_cp294F_union_counter_density9_hold4_surface",
        source_materialized_id="run294A_cp294F_aggressive_cp293A_cp293F_union_flip_hold5",
        source_package_id="cp294F_aggressive_cp293A_cp293F_union_flip_hold5_surface",
        transform_id="union_counter_density9_hold4",
        thesis="The aggressive union can keep OOS payoff scale if validation damage pockets are capped while density remains above four trades/day.",
        changed_variables="voted union source, not-edge cash, moderate z/volatility, breadth guard, target 9.5 active trades/day, hold4.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;union_validation_counter=true",
        target_density=9.5,
        max_hold_bars=4,
    ),
    CandidateSpec(
        package_id="cp296C_cp294D_profit_expand_density7_hold4_surface",
        source_materialized_id="run294A_cp294D_cp293A_smooth_curve_flip_router_hold5",
        source_package_id="cp294D_cp293A_smooth_curve_flip_router_hold5_surface",
        transform_id="profit_expand_density7_hold4",
        thesis="cp294D is less damaged in validation; Stage296 expands nearby states to restore density without losing the OOS clue.",
        changed_variables="loose smooth-state expansion around cp295D profit clue, target 7.5 active trades/day, hold4.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;profit_state_expansion=true",
        target_density=7.5,
        max_hold_bars=4,
    ),
    CandidateSpec(
        package_id="cp296D_cp294D_session_quota_density9_hold3_surface",
        source_materialized_id="run294A_cp294D_cp293A_smooth_curve_flip_router_hold5",
        source_package_id="cp294D_cp293A_smooth_curve_flip_router_hold5_surface",
        transform_id="session_quota_density9_hold3",
        thesis="Shorter hold and session quota can restore 4-10 trades/day while avoiding long validation pockets.",
        changed_variables="cash-core session quota, trend range, side alignment, target 9 active trades/day, hold3.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;session_density_quota=true",
        target_density=9.0,
        max_hold_bars=3,
    ),
    CandidateSpec(
        package_id="cp296E_cp294C_payoff_tail_density10_hold4_surface",
        source_materialized_id="run294A_cp294C_cp293A_density_trimmed_flip_hold5",
        source_package_id="cp294C_cp293A_density_trimmed_flip_hold5_surface",
        transform_id="payoff_tail_density10_hold4",
        thesis="Payoff-tail capture can raise net scale if expansion is capped inside 10 trades/day and keeps validation counterfeatures.",
        changed_variables="payoff score weighted widening, volatility cap, target 10 active trades/day, hold4.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;payoff_tail_capture=true",
        target_density=10.0,
        max_hold_bars=4,
    ),
    CandidateSpec(
        package_id="cp296F_cp294E_lowdensity_profit_expand_density8_hold4_surface",
        source_materialized_id="run294A_cp294E_cp293F_near_breakeven_flip_smoother_hold5",
        source_package_id="cp294E_cp293F_near_breakeven_flip_smoother_hold5_surface",
        transform_id="lowdensity_profit_expand_density8_hold4",
        thesis="cp295D's low-density profit clue is re-expanded from its cp294E source with broader state acceptance.",
        changed_variables="mid-to-core cash expansion, moderate volatility, no extreme z-score, target 8.5 active trades/day, hold4.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;lowdensity_profit_reexpand=true",
        target_density=8.5,
        max_hold_bars=4,
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def feature_arrays(source: pd.DataFrame) -> dict[str, np.ndarray]:
    return {
        "zabs": pd.to_numeric(source.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy(dtype="float64"),
        "vol": pd.to_numeric(source.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy(dtype="float64"),
        "atr_ratio": pd.to_numeric(source.get("atr_14_over_atr_50", 1.0), errors="coerce").fillna(1.0).to_numpy(dtype="float64"),
        "adx": pd.to_numeric(source.get("adx_14", 20.0), errors="coerce").fillna(20.0).to_numpy(dtype="float64"),
        "breadth": pd.to_numeric(source.get("mega8_pos_breadth_1", 0.5), errors="coerce").fillna(0.5).to_numpy(dtype="float64"),
        "score": s295.source_score(source),
    }


def transform_signal(spec: CandidateSpec, source: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    raw = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    masks = s295.feature_masks(source)
    arrays = feature_arrays(source)
    zabs = arrays["zabs"]
    vol = arrays["vol"]
    atr_ratio = arrays["atr_ratio"]
    adx = arrays["adx"]
    breadth = arrays["breadth"]
    score = arrays["score"].copy()
    signal = raw.copy()
    if spec.transform_id == "validation_counter_density8_hold4":
        keep = masks["not_edge"] & (zabs <= 2.35) & (vol >= 0.38) & (vol <= 1.58) & (atr_ratio <= 1.82) & (breadth >= 0.08) & (breadth <= 0.92) & masks["side_aligned"]
        score *= keep.astype("float64") * (1.0 + 0.15 * ((breadth > 0.25) & (breadth < 0.75)).astype("float64"))
    elif spec.transform_id == "union_counter_density9_hold4":
        signal, vote_score = s295.voted_union_signal(source)
        keep = masks["not_edge"] & (zabs <= 2.50) & (vol >= 0.35) & (vol <= 1.65) & (breadth >= 0.10) & (breadth <= 0.90) & masks["side_aligned"]
        score = vote_score * keep.astype("float64")
    elif spec.transform_id == "profit_expand_density7_hold4":
        keep = masks["not_edge"] & (zabs <= 2.35) & (vol >= 0.38) & (vol <= 1.58) & (atr_ratio <= 1.82) & (breadth >= 0.08) & (breadth <= 0.92) & masks["side_aligned"]
        score *= keep.astype("float64") * (1.0 + 0.20 * ((adx >= 16.0) & (adx <= 36.0)).astype("float64"))
    elif spec.transform_id == "session_quota_density9_hold3":
        keep = masks["cash_core"] & (zabs <= 2.70) & (vol >= 0.32) & (vol <= 1.72) & (atr_ratio <= 1.95) & (adx >= 12.0) & (adx <= 48.0) & masks["side_aligned"]
        score *= keep.astype("float64") * (1.0 + 0.20 * ((adx >= 17.0) & (adx <= 34.0)).astype("float64"))
    elif spec.transform_id == "payoff_tail_density10_hold4":
        keep = masks["not_edge"] & (zabs <= 2.65) & (vol >= 0.34) & (vol <= 1.80) & (atr_ratio <= 2.05) & (breadth >= 0.05) & (breadth <= 0.95) & masks["side_aligned"]
        score *= keep.astype("float64") * 1.25
    elif spec.transform_id == "lowdensity_profit_expand_density8_hold4":
        keep = masks["not_edge"] & (zabs <= 2.35) & (vol >= 0.38) & (vol <= 1.58) & (atr_ratio <= 1.82) & (breadth >= 0.08) & (breadth <= 0.92) & masks["side_aligned"]
        score *= keep.astype("float64") * (1.0 + 0.12 * ((breadth > 0.20) & (breadth < 0.80)).astype("float64"))
    else:
        keep = np.ones(len(source), dtype=bool)
    signal = np.where(keep, signal, 0).astype("int8")
    signal = s294.trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score


def metrics_for_payload(spec: CandidateSpec, payload: pd.DataFrame, split: str) -> dict[str, Any]:
    tier = payload.loc[payload["tier_scope"].astype(str).eq("Tier A")].copy()
    dataset = s290.load_dataset(spec.dataset_id)[["timestamp", "split", "future_log_return_12"]].copy()
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    tier = tier.merge(dataset, on=["timestamp", "split"], how="left", validate="many_to_one")
    part = tier.loc[tier["split"].astype(str).eq(split)].copy()
    signal = pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    return s290.curve_metrics(part, signal, spec.max_hold_bars)


def gate_label(validation_metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(validation_metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "edge":
        ok = float(validation_metrics["net_bp"]) > 0.0 and float(oos_metrics["net_bp"]) > 0.0 and float(validation_metrics["pf"]) >= 1.03 and float(oos_metrics["pf"]) >= 1.02
    else:
        ok = (
            float(validation_metrics["worst_rolling_20_bp"]) >= -450.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -450.0
            and float(validation_metrics["positive_month_share"]) >= 0.33
            and float(oos_metrics["positive_month_share"]) >= 0.50
            and float(validation_metrics["underwater_ratio"]) <= 0.97
            and float(oos_metrics["underwater_ratio"]) <= 0.95
        )
    return "passed" if ok else "failed"


def materialize_payload(spec: CandidateSpec) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = s295.load_source_payload(spec.source_materialized_id)
    signal, score = transform_signal(spec, source)
    branch_id = f"run296A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    payload["stage296_branch_id"] = branch_id
    payload["stage295_branch_id"] = payload.get("stage295_branch_id", branch_id)
    payload["stage294_branch_id"] = payload.get("stage294_branch_id", spec.source_materialized_id)
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "density_floor_profit_expansion_surface"
    payload["candidate_decision_score"] = score
    payload["source_branch_id"] = spec.source_materialized_id
    payload["source_active_mask"] = (pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy() != 0).astype("int8")
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = 0.01
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_materialized_id": spec.source_materialized_id,
        "source_package_id": spec.source_package_id,
        "dataset_id": spec.dataset_id,
        "transform_id": spec.transform_id,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "close_on_flat_signal": spec.close_on_flat_signal,
        "same_direction_reentry_cooldown_bars": spec.same_direction_reentry_cooldown_bars,
        "direction_feature_order_hash": ordered_hash(("route_signal_value",)),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(("route_signal_value",))
    payload["model_feature_order_hash"] = "rule_surface_no_model_artifact"
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = metrics_for_payload(spec, payload, "validation")
    oos_metrics = metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    class SupplySpec:
        package_id = spec.package_id
        max_hold_bars = spec.max_hold_bars

    return s290.supply_rows_for_payload(payload, SupplySpec())  # type: ignore[arg-type]


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(CANDIDATES, start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec)
        branch_id = f"run296A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "package_id": spec.package_id,
                "materialized_branch_id": branch_id,
                "source_materialized_id": spec.source_materialized_id,
                "feature_order": ["route_signal_value"],
                "feature_order_hash": ordered_hash(("route_signal_value",)),
                "decision_surface": identity,
                "risk_logic": spec.risk_logic,
                "runtime_handoff": "precomputed route_signal_value replay for density-floor profit expansion probe",
                "claim_boundary": BOUNDARY,
            },
        )
        density_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 0.50
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.thesis,
                "decision_use": "Choose whether density-floor profit expansion is worth MT5 runtime probing.",
                "comparison_baseline": "Stage294 high-density OOS-positive validation-negative surfaces and Stage295 low-density profit/OOS clues",
                "control_variables": "US100 M5 split_v1; Stage294 source payloads; Tier A/B paired runtime accounting",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A and Tier B paired labels; validation/OOS source payload scope from Stage294",
                "success_criteria": "validation and OOS positive, 4-10 trades/day, PF/recovery/expectancy positive, no deep zoomed curve hollow",
                "failure_criteria": "validation remains negative, OOS edge disappears, density falls below 4/day, or curve pocket remains deep",
                "invalid_conditions": "payload contains label/future columns, source payload missing, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise review opens a fresh thesis or discard",
                "evidence_plan": "model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run296B MT5 KPI; run296C curve review",
                "feature_surface": spec.transform_id,
                "model_surface": "rule_surface_from_stage294_signals",
                "decision_surface": spec.transform_id,
                "risk_logic": spec.risk_logic,
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; rule identity retained for Adapter package if selected",
                "failure_memory_plan": "record validation damage, OOS edge loss, density loss, or curve pocket as Stage296 negative memory",
                "claim_boundary": BOUNDARY,
            }
        )
        supply_rows.extend(supply_rows_for_payload(payload, spec))
        manifest_rows.append(
            {
                "queue_id": f"run296A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "density_floor_profit_expansion_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": "",
                "model_artifact_hash": "",
                "model_feature_order_path": "",
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(("route_signal_value",)),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": spec.close_on_flat_signal,
                "same_direction_reentry_cooldown_bars": spec.same_direction_reentry_cooldown_bars,
                "approx_validation_trades_per_day": round(float(validation_metrics["trades_per_day"]), 5),
                "approx_oos_trades_per_day": round(float(oos_metrics["trades_per_day"]), 5),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        model_rows.append(
            {
                "model_id": f"{branch_id}_rule_surface",
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "rule_surface",
                "model_artifact_path": "",
                "model_artifact_hash": "",
                "feature_order_path": "",
                "feature_order_hash": ordered_hash(("route_signal_value",)),
                "prediction_kind": "precomputed_route_signal_rule_surface",
                "claim_boundary": BOUNDARY,
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": "rule_surface",
                "prediction_kind": "precomputed_route_signal_rule_surface",
                "mode": spec.transform_id,
                "quantile": "",
                "threshold": "",
                "precondition": spec.changed_variables,
                "wfo_net_bp": float(validation_metrics["net_bp"]) + float(oos_metrics["net_bp"]),
                "wfo_positive_fold_share": float((float(validation_metrics["net_bp"]) > 0.0) + (float(oos_metrics["net_bp"]) > 0.0)) / 2.0,
                "wfo_worst_fold_net_bp": min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])),
                "wfo_mean_trades_per_day": (float(validation_metrics["trades_per_day"]) + float(oos_metrics["trades_per_day"])) / 2.0,
                "wfo_min_trades_per_day": min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])),
                "wfo_max_trades_per_day": max(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])),
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
                "density_gate": density_gate,
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
                    "mode": spec.transform_id,
                    "quantile": "",
                    "threshold": "",
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
        artifacts.extend([payload_path, handoff_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, artifacts


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    rows = [
        {
            "result_subject": "Stage296 density-floor profit expansion materialization(296단계 거래 밀도 하한 수익 확장 물질화)",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI(MT5 런타임 KPI), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage296는 후보 선택이 아니라, 4-10 trades/day(일 4-10거래)를 되살린 새 표면을 MT5로 보낼 준비다.",
        }
    ]
    gates = [
        {
            "gate_name": "fresh_thesis(새 논제)",
            "status": "passed",
            "evidence_path": rel(BRANCH_QUEUE),
            "effect": "Stage295의 저밀도 수리 반복이 아니라 density-floor profit expansion(거래 밀도 하한 수익 확장)으로 질문을 바꿨다.",
        },
        {
            "gate_name": "proxy_density_screen(대리 밀도 선별)",
            "status": "passed" if density_pass else "failed",
            "evidence_path": rel(MODEL_SCOREBOARD),
            "effect": "MT5 전에 validation/OOS(검증/표본외) 4-10 trades/day(일 4-10거래) 가능성을 본다.",
        },
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "prepared",
            "evidence_path": rel(MT5_QUEUE),
            "effect": "선택 후보를 주장하지 않고 run296B(296B 실행) 외부 검증으로 넘긴다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 게이트 전에는 Adapter(어댑터)를 만들지 않는다.",
        },
        {
            "gate_name": "onnx_readiness(ONNX 준비)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "Adapter(어댑터)와 parity(동등성) 전에는 ONNX(온엑스)를 시작하지 않는다.",
        },
    ]
    return rows, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run296A Density-Floor Profit Expansion Materialization(296A 거래 밀도 하한 수익 확장 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage295(295단계)의 저밀도 수익 단서를 후보로 보존하지 않고, Stage294(294단계)의 고밀도 OOS(표본외) 단서와 결합해 MT5(메타트레이더5) runtime probe(런타임 탐침) 후보 6개를 만들었다.",
        "",
        "| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.1f} | {vtd:.2f} | {on:.1f} | {otd:.2f} | {den} | {edge} | {curve} |".format(
                pkg=row["package_id"],
                vn=float(row["validation_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                on=float(row["oos_proxy_net_bp"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                den=row["density_gate"],
                edge=row["proxy_edge_gate"],
                curve=row["curve_proxy_gate"],
            )
        )
    lines.extend(
        [
            "",
            f"MT5 queue(MT5 대기열): `{len(manifest_rows)}` rows(행)",
            f"Claim boundary(주장 경계): `{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    wfo_rows: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, manifest_rows)
    write_csv_rows(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv_rows(MODEL_SCOREBOARD, s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv_rows(CANDIDATE_SUPPLY, s293.SUPPLY_COLUMNS, supply_rows)
    write_csv_rows(PAYLOAD_MANIFEST, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MT5_QUEUE, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MODEL_MANIFEST, s293.MODEL_COLUMNS, model_rows)
    write_csv_rows(WFO_FOLD_SCOREBOARD, s293.WFO_COLUMNS, wfo_rows)
    write_csv_rows(RESULT_JUDGMENT, s293.RESULT_COLUMNS, result)
    write_csv_rows(GATE_AUDIT, s293.GATE_COLUMNS, gates)
    artifacts = [
        BRANCH_QUEUE,
        MODEL_SCOREBOARD,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        MODEL_MANIFEST,
        WFO_FOLD_SCOREBOARD,
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
            "artifacts": [rel(path) for path in artifacts if path != RUN_MANIFEST],
            "created_at_utc": created_at,
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source": {
                "stage296_seed_queue": rel(SOURCE_SEED_QUEUE),
                "stage295_review_scoreboard": rel(SOURCE_STAGE295_REVIEW),
                "stage294_manifest": rel(SOURCE_STAGE294_MANIFEST),
            },
            "outputs": {
                "payload_manifest": rel(PAYLOAD_MANIFEST),
                "mt5_queue": rel(MT5_QUEUE),
                "scoreboard": rel(MODEL_SCOREBOARD),
                "report": rel(REPORT),
            },
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return artifacts


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "density_floor_profit_expansion_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        s293.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "density_floor_profit_expansion_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "density_floor_profit_expansion",
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
    upsert_csv_rows(
        STAGE_LEDGER,
        s293.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "density_floor_profit_expansion_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "scoreboard": "model_scout_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "materialization_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage296_density_floor_profit_expansion_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run296A density-floor profit expansion materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_md(
        SELECTED,
        f"""# Stage296 Selection Status(296단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- target_candidate(목표 후보): `none`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- run296A_report(296A 보고): `{rel(REPORT)}`
- run296A_mt5_queue(296A MT5 대기열): `{rel(MT5_QUEUE)}`
""",
    )
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage296 Review Index(296단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run296A_report",
        f"- run296A_report(296A 보고): `{rel(REPORT)}`\n- run296A_mt5_queue(296A MT5 대기열): `{rel(MT5_QUEUE)}`",
    )
    write_md(REVIEW_INDEX, review_index)
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run296A_summary",
        f"- run296A_summary(296A 요약): density-floor profit expansion(거래 밀도 하한 수익 확장) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected_candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage296(296단계) run296A(296A 실행) density-floor profit expansion materialization(거래 밀도 하한 수익 확장 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 주장하지 않는다.\n"
    )
    workspace = s293.prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run296A Density-floor profit expansion materialization(296A 거래 밀도 하한 수익 확장 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 아직 없다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts, created_at)
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
