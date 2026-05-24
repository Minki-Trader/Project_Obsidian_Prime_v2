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
from stage_pipelines.stage290 import design_materialize_payoff_weighted_edge_model_rebuild as s290  # noqa: E402
from stage_pipelines.stage293 import design_materialize_profit_scale_density_calibration_rebuild as s293  # noqa: E402
from stage_pipelines.stage294 import design_materialize_mt5_outcome_relabel_directional_flip_rebuild as s294  # noqa: E402


STAGE_ID = "295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild"
RUN_ID = "run295A_design_split_consistent_outcome_distillation_rebuild_v1"
RUN_NUMBER = "run295A"
SOURCE_STAGE_ID = "294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild"
SOURCE_RUN_ID = "run294C_review_mt5_outcome_relabel_directional_flip_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
NEXT_ACTION = "run295B_execute_split_consistent_outcome_distillation_mt5_probe"
STATUS = "completed_split_consistent_outcome_distillation_candidates_materialized_no_selection"
JUDGMENT = "split_consistent_outcome_distillation_inputs_materialized_no_candidate_selection"
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

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_RUN294A = SOURCE_STAGE / "02_runs" / "run294A"
SOURCE_RUN294B = SOURCE_STAGE / "02_runs" / "run294B"
SOURCE_RUN294C = SOURCE_STAGE / "02_runs" / "run294C"
SOURCE_MANIFEST = SOURCE_RUN294A / "candidate_payload_manifest.csv"
SOURCE_MODEL_MANIFEST = SOURCE_RUN294A / "model_artifact_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN294C / "mt5_outcome_relabel_directional_flip_review_scoreboard.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN294C / "failure_memory.csv"

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
REPORT = REVIEWS / "run295A_split_consistent_outcome_distillation_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


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
    dataset_id: str = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"


CANDIDATES: tuple[CandidateSpec, ...] = (
    CandidateSpec(
        package_id="cp295A_cp294D_split_veto_distill_hold5_surface",
        source_materialized_id="run294A_cp294D_cp293A_smooth_curve_flip_router_hold5",
        source_package_id="cp294D_cp293A_smooth_curve_flip_router_hold5_surface",
        transform_id="split_veto_midcash_volshape_hold5",
        thesis="Least-damaged validation source cp294D is distilled through mid-session and volatility-shape veto.",
        changed_variables="remove first/last cash edges, high volatility bursts, and extreme z-score pockets.",
        risk_logic="max_hold_bars=5;close_on_flat_signal=true;split_consistent_validation_damage_veto=true",
        target_density=5.8,
        max_hold_bars=5,
    ),
    CandidateSpec(
        package_id="cp295B_cp294C_oos_preserve_validation_veto_hold5_surface",
        source_materialized_id="run294A_cp294C_cp293A_density_trimmed_flip_hold5",
        source_package_id="cp294C_cp293A_density_trimmed_flip_hold5_surface",
        transform_id="oos_preserve_validation_damage_veto_hold5",
        thesis="Strongest OOS source cp294C is narrowed by a validation damage veto without dropping below density floor.",
        changed_variables="reject high atr expansion, weak breadth extremes, early/late cash pockets, then trim to 7.6 trades/day.",
        risk_logic="max_hold_bars=5;close_on_flat_signal=true;oos_edge_preserve_gate=true",
        target_density=7.6,
        max_hold_bars=5,
    ),
    CandidateSpec(
        package_id="cp295C_cp294B_cost_curve_distill_hold5_surface",
        source_materialized_id="run294A_cp294B_cp293F_cost_aware_flip_skip_hold5",
        source_package_id="cp294B_cp293F_cost_aware_flip_skip_hold5_surface",
        transform_id="cost_curve_mid_session_distill_hold5",
        thesis="Cost-aware cp294B keeps OOS PF positive; Stage295 adds curve-state and session quality veto.",
        changed_variables="mid-session cash, non-extreme return, lower atr expansion, and side-alignment filter.",
        risk_logic="max_hold_bars=5;close_on_flat_signal=true;cost_curve_distillation=true",
        target_density=5.1,
        max_hold_bars=5,
    ),
    CandidateSpec(
        package_id="cp295D_cp294E_smooth_state_hold4_surface",
        source_materialized_id="run294A_cp294E_cp293F_near_breakeven_flip_smoother_hold5",
        source_package_id="cp294E_cp293F_near_breakeven_flip_smoother_hold5_surface",
        transform_id="smooth_state_shorter_hold4",
        thesis="Near-breakeven smoother cp294E is tested with shorter hold to cut validation damage pockets.",
        changed_variables="shorten hold to 4 bars, keep only smooth volatility and aligned side states.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;shorter_hold_validation_damage_control=true",
        target_density=5.4,
        max_hold_bars=4,
    ),
    CandidateSpec(
        package_id="cp295E_union_oos_band_rescale_hold5_surface",
        source_materialized_id="run294A_cp294F_aggressive_cp293A_cp293F_union_flip_hold5",
        source_package_id="cp294F_aggressive_cp293A_cp293F_union_flip_hold5_surface",
        transform_id="aggressive_union_oos_band_rescale_hold5",
        thesis="Aggressive union is rebuilt as a voted OOS-positive band instead of raw over-density.",
        changed_variables="vote cp294B/cp294C/cp294D/cp294E/cp294F signals, apply validation veto, cap at 9.4 trades/day.",
        risk_logic="max_hold_bars=5;close_on_flat_signal=true;voted_union_rescale=true",
        target_density=9.4,
        max_hold_bars=5,
    ),
    CandidateSpec(
        package_id="cp295F_defensive_damage_flat_router_hold3_surface",
        source_materialized_id="run294A_cp294D_cp293A_smooth_curve_flip_router_hold5",
        source_package_id="cp294D_cp293A_smooth_curve_flip_router_hold5_surface",
        transform_id="defensive_damage_flat_router_hold3",
        thesis="Defensive flat router sacrifices some exposure to test whether validation damage is mainly hold/pocket driven.",
        changed_variables="hold3, stricter pocket veto, side alignment, and 4-trade density floor.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;damage_flat_router=true",
        target_density=4.3,
        max_hold_bars=3,
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    import csv

    with io_path(path).open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


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


def ordered_hash(values: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def load_source_payload(materialized_id: str) -> pd.DataFrame:
    manifest = manifest_by_id()
    if materialized_id not in manifest:
        raise KeyError(f"Missing source materialized id: {materialized_id}")
    frame = pd.read_parquet(io_path(ROOT / manifest[materialized_id]["payload_path"])).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["route_signal_value"] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    return frame.sort_values(["tier_scope", "timestamp"]).reset_index(drop=True)


def source_score(frame: pd.DataFrame) -> np.ndarray:
    if "candidate_decision_score" in frame.columns:
        values = pd.to_numeric(frame["candidate_decision_score"], errors="coerce").fillna(0.0).abs().to_numpy(dtype="float64")
    else:
        values = np.ones(len(frame), dtype="float64")
    return np.nan_to_num(values, nan=0.0, posinf=0.0, neginf=0.0)


def feature_masks(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    minutes = pd.to_numeric(frame.get("minutes_from_cash_open", 999.0), errors="coerce").fillna(999.0).to_numpy(dtype="float64")
    zabs = pd.to_numeric(frame.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy(dtype="float64")
    vol = pd.to_numeric(frame.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy(dtype="float64")
    atr_ratio = pd.to_numeric(frame.get("atr_14_over_atr_50", 1.0), errors="coerce").fillna(1.0).to_numpy(dtype="float64")
    adx = pd.to_numeric(frame.get("adx_14", 20.0), errors="coerce").fillna(20.0).to_numpy(dtype="float64")
    di = pd.to_numeric(frame.get("di_spread_14", 0.0), errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    breadth = pd.to_numeric(frame.get("mega8_pos_breadth_1", 0.5), errors="coerce").fillna(0.5).to_numpy(dtype="float64")
    cash = pd.to_numeric(frame.get("is_us_cash_open", 0.0), errors="coerce").fillna(0.0).to_numpy(dtype="float64") > 0.5
    signal = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    side_aligned = np.where(signal > 0, di > -16.0, np.where(signal < 0, di < 16.0, True))
    strong_side_aligned = np.where(signal > 0, di > -8.0, np.where(signal < 0, di < 8.0, True))
    return {
        "cash_core": cash & (minutes >= 35.0) & (minutes <= 305.0),
        "cash_mid": cash & (minutes >= 55.0) & (minutes <= 255.0),
        "not_edge": cash & (minutes >= 25.0) & (minutes <= 320.0),
        "vol_shape": (vol >= 0.45) & (vol <= 1.38) & (atr_ratio <= 1.58),
        "strict_vol_shape": (vol >= 0.55) & (vol <= 1.18) & (atr_ratio <= 1.38),
        "z_ok": zabs <= 1.95,
        "z_strict": zabs <= 1.45,
        "trend_ok": (adx >= 15.0) & (adx <= 42.0),
        "trend_strict": (adx >= 17.0) & (adx <= 34.0),
        "breadth_ok": (breadth >= 0.125) & (breadth <= 0.875),
        "breadth_mid": (breadth >= 0.25) & (breadth <= 0.75),
        "side_aligned": side_aligned,
        "strong_side_aligned": strong_side_aligned,
    }


def voted_union_signal(source: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    member_ids = [
        "run294A_cp294B_cp293F_cost_aware_flip_skip_hold5",
        "run294A_cp294C_cp293A_density_trimmed_flip_hold5",
        "run294A_cp294D_cp293A_smooth_curve_flip_router_hold5",
        "run294A_cp294E_cp293F_near_breakeven_flip_smoother_hold5",
        "run294A_cp294F_aggressive_cp293A_cp293F_union_flip_hold5",
    ]
    signals: list[np.ndarray] = []
    scores: list[np.ndarray] = []
    key = source[["timestamp", "tier_scope", "split"]].copy()
    for materialized_id in member_ids:
        frame = load_source_payload(materialized_id)
        merged = key.merge(
            frame[["timestamp", "tier_scope", "split", "route_signal_value", "candidate_decision_score"]],
            on=["timestamp", "tier_scope", "split"],
            how="left",
            validate="one_to_one",
        )
        signals.append(pd.to_numeric(merged["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy())
        scores.append(pd.to_numeric(merged["candidate_decision_score"], errors="coerce").fillna(0.0).abs().to_numpy(dtype="float64"))
    stack = np.vstack(signals)
    score_stack = np.vstack(scores)
    vote_sum = stack.sum(axis=0)
    out = np.where(vote_sum > 0, 1, np.where(vote_sum < 0, -1, 0)).astype("int8")
    out[np.abs(vote_sum) < 2] = 0
    score = np.nanmean(score_stack, axis=0) * np.abs(vote_sum)
    return out, np.nan_to_num(score, nan=0.0)


def transform_signal(spec: CandidateSpec, source: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    raw = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    score = source_score(source)
    masks = feature_masks(source)
    if spec.transform_id == "split_veto_midcash_volshape_hold5":
        keep = masks["cash_core"] & masks["vol_shape"] & masks["z_ok"] & masks["trend_ok"] & masks["side_aligned"]
        signal = np.where(keep, raw, 0).astype("int8")
        score = score * keep.astype("float64")
    elif spec.transform_id == "oos_preserve_validation_damage_veto_hold5":
        keep = masks["not_edge"] & masks["vol_shape"] & masks["z_ok"] & masks["breadth_ok"] & masks["side_aligned"]
        signal = np.where(keep, raw, 0).astype("int8")
        score = score * keep.astype("float64") * 1.08
    elif spec.transform_id == "cost_curve_mid_session_distill_hold5":
        keep = masks["cash_mid"] & masks["strict_vol_shape"] & masks["z_ok"] & masks["breadth_mid"] & masks["side_aligned"]
        signal = np.where(keep, raw, 0).astype("int8")
        score = score * keep.astype("float64") * 1.15
    elif spec.transform_id == "smooth_state_shorter_hold4":
        keep = masks["cash_core"] & masks["strict_vol_shape"] & masks["z_strict"] & masks["trend_ok"] & masks["strong_side_aligned"]
        signal = np.where(keep, raw, 0).astype("int8")
        score = score * keep.astype("float64") * 1.20
    elif spec.transform_id == "aggressive_union_oos_band_rescale_hold5":
        signal, vote_score = voted_union_signal(source)
        keep = masks["not_edge"] & masks["vol_shape"] & masks["z_ok"] & masks["breadth_ok"] & masks["side_aligned"]
        signal = np.where(keep, signal, 0).astype("int8")
        score = vote_score * keep.astype("float64")
    elif spec.transform_id == "defensive_damage_flat_router_hold3":
        keep = masks["cash_mid"] & masks["strict_vol_shape"] & masks["z_strict"] & masks["trend_strict"] & masks["breadth_mid"] & masks["strong_side_aligned"]
        signal = np.where(keep, raw, 0).astype("int8")
        score = score * keep.astype("float64") * 1.25
    else:
        signal = raw
    signal = s294.trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score


def metrics_for_payload(spec: CandidateSpec, payload: pd.DataFrame, split: str) -> dict[str, Any]:
    tier = payload.loc[payload["tier_scope"].astype(str).eq("Tier A")].copy()
    dataset = s290.load_dataset(spec.dataset_id)[["timestamp", "split", "future_log_return_12"]].copy()
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    tier = tier.merge(dataset, on=["timestamp", "split"], how="left", validate="many_to_one")
    part = tier.loc[tier["split"].astype(str).eq(split)].copy()
    part_signal = pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    return s290.curve_metrics(part, part_signal, spec.max_hold_bars)


def gate_label(validation_metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(validation_metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "edge":
        ok = float(validation_metrics["net_bp"]) > 0.0 and float(oos_metrics["net_bp"]) > 0.0 and float(validation_metrics["pf"]) >= 1.03 and float(oos_metrics["pf"]) >= 1.02
    else:
        ok = (
            float(validation_metrics["worst_rolling_20_bp"]) >= -240.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -240.0
            and float(validation_metrics["positive_month_share"]) >= 0.45
            and float(oos_metrics["positive_month_share"]) >= 0.45
            and float(validation_metrics["underwater_ratio"]) <= 0.90
            and float(oos_metrics["underwater_ratio"]) <= 0.90
        )
    return "passed" if ok else "failed"


def materialize_payload(spec: CandidateSpec) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = load_source_payload(spec.source_materialized_id)
    signal, score = transform_signal(spec, source)
    branch_id = f"run295A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    payload["stage295_branch_id"] = branch_id
    payload["stage294_branch_id"] = payload.get("stage294_branch_id", spec.source_materialized_id)
    payload["stage293_branch_id"] = payload.get("stage293_branch_id", spec.source_materialized_id)
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "split_consistent_outcome_distillation_surface"
    payload["candidate_decision_score"] = score
    payload["source_branch_id"] = spec.source_materialized_id
    payload["source_active_mask"] = (pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy() != 0).astype("int8")
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = 0.01
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = True
    payload["same_direction_reentry_cooldown_bars"] = 0
    identity = {
        "package_id": spec.package_id,
        "source_materialized_id": spec.source_materialized_id,
        "source_package_id": spec.source_package_id,
        "dataset_id": spec.dataset_id,
        "transform_id": spec.transform_id,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
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
        branch_id = f"run295A_{spec.package_id.replace('_surface', '')}"
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
                "runtime_handoff": "precomputed route_signal_value replay for split-consistent outcome distillation probe",
                "claim_boundary": BOUNDARY,
            },
        )
        density_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 0.40
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.thesis,
                "comparison_baseline": "Stage294 valid negative runtime scoreboard with OOS-positive and validation-negative clue",
                "control_variables": "US100 M5 split_v1; Stage294 route-signal replay handoff; Tier A/B paired runtime accounting",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A and Tier B paired labels; validation/OOS source payload scope from Stage294",
                "success_criteria": "validation and OOS positive, 4-10 trades/day, PF/recovery/expectancy positive, no deep zoomed curve hollow",
                "failure_criteria": "validation remains negative, OOS edge disappears, density falls below 4/day, or curve pocket remains deep",
                "invalid_conditions": "payload contains label/future columns, source payload missing, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise run295C review opens a fresh thesis",
                "evidence_plan": "model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run295B MT5 KPI; run295C curve review",
                "feature_surface": spec.transform_id,
                "model_surface": "rule_surface_from_stage294_signals",
                "decision_surface": spec.transform_id,
                "risk_logic": spec.risk_logic,
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; rule identity retained for Adapter package if selected",
                "failure_memory_plan": "record validation damage, OOS edge loss, density loss, or curve pocket as Stage295 negative memory",
                "claim_boundary": BOUNDARY,
            }
        )
        supply_rows.extend(supply_rows_for_payload(payload, spec))
        manifest_rows.append(
            {
                "queue_id": f"run295A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "split_consistent_outcome_distillation_surface",
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
                "close_on_flat_signal": True,
                "same_direction_reentry_cooldown_bars": 0,
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
                    "split": split_name,
                    "net_bp": metrics["net_bp"],
                    "pf": metrics["pf"],
                    "trade_count": metrics["trade_count"],
                    "trades_per_day": metrics["trades_per_day"],
                    "max_drawdown_bp": metrics["max_drawdown_bp"],
                    "recovery": metrics["recovery"],
                    "worst_month_bp": metrics["worst_month_bp"],
                    "worst_rolling_20_bp": metrics["worst_rolling_20_bp"],
                    "worst_rolling_50_bp": metrics["worst_rolling_50_bp"],
                    "positive_month_share": metrics["positive_month_share"],
                    "underwater_ratio": metrics["underwater_ratio"],
                    "claim_boundary": BOUNDARY,
                }
            )
        artifacts.extend([payload_path, handoff_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, artifacts


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run295A Split-Consistent Outcome Distillation Materialization(295A 분할 일관 결과 증류 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage294(294단계)의 OOS(표본외) 양수 단서를 좁게 수리하지 않고, validation damage(검증 손상)를 직접 거부하거나 증류하는 새 후보 6개를 MT5(메타트레이더5) 탐침 대기열로 만든다.",
        "",
        "| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.2f} | {vd:.2f} | {on:.2f} | {od:.2f} | {dg} | {eg} | {cg} |".format(
                pkg=row["package_id"],
                vn=float(row["validation_proxy_net_bp"]),
                vd=float(row["validation_proxy_trades_per_day"]),
                on=float(row["oos_proxy_net_bp"]),
                od=float(row["oos_proxy_trades_per_day"]),
                dg=row["density_gate"],
                eg=row["proxy_edge_gate"],
                cg=row["curve_proxy_gate"],
            )
        )
    lines.extend(
        [
            "",
            f"- mt5_queue_rows(MT5 대기열 행): `{len(manifest_rows)}`",
            "",
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
    for path in (RUN_ROOT, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(BRANCH_QUEUE, s293.BRANCH_COLUMNS, branch_rows)
    write_csv(MODEL_SCOREBOARD, s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, s293.SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, s293.MODEL_COLUMNS, model_rows)
    write_csv(WFO_FOLD_SCOREBOARD, s293.WFO_COLUMNS, wfo_rows)
    write_csv(
        RESULT_JUDGMENT,
        s293.RESULT_COLUMNS,
        [
            {
                "result_subject": "Stage295 split-consistent outcome distillation materialization(295단계 분할 일관 결과 증류 물질화)",
                "evidence_available": f"branches={len(branch_rows)};mt5_queue_rows={len(manifest_rows)};source_scoreboard={rel(SOURCE_SCOREBOARD)}",
                "evidence_missing": "MT5 runtime KPI(MT5 런타임 KPI), curve review(곡선 검토), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
                "judgment_label": "exploratory",
                "judgment_class": JUDGMENT,
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "후보를 고른 것이 아니라 검증 손상 거부/증류 후보를 외부 MT5 탐침으로 넘길 준비를 끝냈다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        s293.GATE_COLUMNS,
        [
            {
                "gate_name": "experiment_design(실험 설계)",
                "status": "passed",
                "evidence_path": rel(BRANCH_QUEUE),
                "effect": "가설, 비교 기준, 고정/변경 변수, 성공/실패 조건을 각 후보에 붙였다.",
            },
            {
                "gate_name": "runtime_payload_integrity(런타임 페이로드 무결성)",
                "status": "passed",
                "evidence_path": rel(PAYLOAD_MANIFEST),
                "effect": "label/future 열을 제거하고 route_signal_value 단일 인계 표면으로 만들었다.",
            },
            {
                "gate_name": "candidate_selection(후보 선택)",
                "status": "not_started",
                "evidence_path": rel(MODEL_SCOREBOARD),
                "effect": "MT5 런타임 탐침 전에는 선택 후보를 주장하지 않는다.",
            },
        ],
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_stage_id": SOURCE_STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "next_action": NEXT_ACTION,
            "created_at_utc": created_at,
            "artifacts": [
                rel(path)
                for path in (
                    BRANCH_QUEUE,
                    MODEL_SCOREBOARD,
                    CANDIDATE_SUPPLY,
                    PAYLOAD_MANIFEST,
                    MT5_QUEUE,
                    MODEL_MANIFEST,
                    WFO_FOLD_SCOREBOARD,
                    RESULT_JUDGMENT,
                    GATE_AUDIT,
                    REPORT,
                    LINEAGE,
                )
            ],
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source": {
                "stage294_manifest": rel(SOURCE_MANIFEST),
                "stage294_scoreboard": rel(SOURCE_SCOREBOARD),
                "stage294_failure_memory": rel(SOURCE_FAILURE_MEMORY),
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
    return [
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


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "split_consistent_outcome_distillation_materialization",
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
                "record_view": "split_consistent_outcome_distillation_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "split_consistent_outcome_distillation",
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
                "view": "split_consistent_outcome_distillation_materialization",
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
            "artifact_type": "stage295_split_consistent_outcome_distillation_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run295A split-consistent outcome distillation materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_md(
        SELECTED,
        f"""# Stage295 Selection Status(295단계 선택 상태)

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
- run295A_report(295A 보고): `{rel(REPORT)}`
- run295A_mt5_queue(295A MT5 대기열): `{rel(MT5_QUEUE)}`
""",
    )
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage295 Review Index(295단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run295A_report",
        f"- run295A_report(295A 보고): `{rel(REPORT)}`\n- run295A_mt5_queue(295A MT5 대기열): `{rel(MT5_QUEUE)}`",
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
        "run295A_summary",
        f"- run295A_summary(295A 요약): split-consistent outcome distillation(분할 일관 결과 증류) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected_candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage295(295단계) run295A(295A 실행) split-consistent outcome distillation materialization(분할 일관 결과 증류 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 주장하지 않는다.\n"
    )
    workspace = s293.prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run295A split-consistent outcome distillation materialization(295A 분할 일관 결과 증류 물질화)\n\n"
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
