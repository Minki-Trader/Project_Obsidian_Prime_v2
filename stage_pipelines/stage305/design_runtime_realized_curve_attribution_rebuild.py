from __future__ import annotations

import csv
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
from stage_pipelines.stage294 import design_materialize_mt5_outcome_relabel_directional_flip_rebuild as s294  # noqa: E402


STAGE_ID = "305_onnx_candidate_campaign__runtime_realized_curve_attribution_rebuild"
RUN_ID = "run305A_design_runtime_realized_curve_attribution_rebuild_v1"
RUN_NUMBER = "run305A"
SOURCE_STAGE_ID = "304_onnx_candidate_campaign__curve_pocket_aware_profit_source_rebuild"
SOURCE_RUN_ID = "run304C_review_curve_pocket_aware_profit_source_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_runtime_realized_curve_attribution_candidates_materialized_no_selection"
JUDGMENT = "runtime_realized_curve_attribution_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run305B_execute_runtime_realized_curve_attribution_mt5_probe"
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
HANDOFF_DIR = RUN_ROOT / "handoff"
MODEL_DIR = RUN_ROOT / "models"

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_MANIFEST = SOURCE_STAGE / "02_runs" / "run304A" / "candidate_payload_manifest.csv"
SOURCE_REVIEW_SCOREBOARD = SOURCE_STAGE / "02_runs" / "run304C" / "curve_pocket_aware_profit_source_review_scoreboard.csv"
SOURCE_TRADE_QUALITY = SOURCE_STAGE / "02_runs" / "run304C" / "trade_quality_summary.csv"
SOURCE_STAGE305_QUEUE = SOURCE_STAGE / "02_runs" / "run304C" / "stage305_seed_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run304C_curve_pocket_aware_profit_source_review_stage305_open_report.md"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run305A_runtime_realized_curve_attribution_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

FEATURE_ORDER = ("route_signal_value",)
MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage305_branch_id",
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
MODEL_COLUMNS = s293.MODEL_COLUMNS


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    source_package_id: str
    transform_id: str
    target_density: float
    max_hold_bars: int
    fixed_lot: float
    atr_sltp_enabled: bool
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_sizing_enabled: bool
    model_risk_max_pct: float
    hypothesis: str
    changed_variables: str
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    atr_period: int = 14
    model_risk_min_pct: float = 0.006
    model_risk_confidence_floor: float = 0.54
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            package_id="cp305A_runtime_loss_flip_cp304D_mid_density65_hold4_surface",
            source_package_id="cp304D_histgb_return_profit_scale_density85_hold6_surface",
            transform_id="full_flip_mid",
            target_density=6.5,
            max_hold_bars=4,
            fixed_lot=0.18,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.65,
            atr_take_profit_multiplier=3.90,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.026,
            hypothesis="Stage304 actual losses imply the cp304D signal direction is useful after a mid-session inversion with risk capped.",
            changed_variables="flip cp304D signal in mid-session, density 6.5, hold4, ATR 1.65/3.90, model risk cap 2.6%.",
        ),
        CandidateSpec(
            package_id="cp305B_runtime_loss_flip_cp304E_mid_density65_hold4_surface",
            source_package_id="cp304E_extratrees_inverse_pocket_guard_density45_hold3_surface",
            transform_id="full_flip_mid",
            target_density=6.5,
            max_hold_bars=4,
            fixed_lot=0.22,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.50,
            atr_take_profit_multiplier=3.50,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
            hypothesis="The least bad Stage304 branch may become a positive source when the realized loss direction is inverted.",
            changed_variables="flip cp304E mid-session signal, density 6.5, hold4, fixed lot 0.22.",
        ),
        CandidateSpec(
            package_id="cp305C_cp304E_hour19_direct_else_flip_density80_hold6_surface",
            source_package_id="cp304E_extratrees_inverse_pocket_guard_density45_hold3_surface",
            transform_id="hour19_direct_else_flip",
            target_density=8.0,
            max_hold_bars=6,
            fixed_lot=0.18,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.70,
            atr_take_profit_multiplier=4.20,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.024,
            hypothesis="Hour 19, hour 22, and high-ADX pockets were less harmful; keep those direct and invert the rest.",
            changed_variables="direct high-ADX/hour19/hour22, flip other mid-session cp304E signal, density 8.0, hold6.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp305D_cp304C_broad_flip_density65_hold4_surface",
            source_package_id="cp304C_histgb_classifier_density_router_hold6_surface",
            transform_id="full_flip_wide",
            target_density=6.5,
            max_hold_bars=4,
            fixed_lot=0.18,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.60,
            atr_take_profit_multiplier=3.75,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.022,
            hypothesis="The strongest proxy anti-surface came from flipping cp304C broadly while widening supply above the 4/day floor.",
            changed_variables="wide mid-session flip of cp304C, density 6.5, hold4, model risk cap 2.2%.",
        ),
        CandidateSpec(
            package_id="cp305E_cp304D_lowvol_flip_density55_hold4_surface",
            source_package_id="cp304D_histgb_return_profit_scale_density85_hold6_surface",
            transform_id="lowvol_flip",
            target_density=5.5,
            max_hold_bars=4,
            fixed_lot=0.20,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.45,
            atr_take_profit_multiplier=3.30,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
            hypothesis="Low-volatility realized loss pockets may invert cleanly with lower trade frequency and fixed risk.",
            changed_variables="flip cp304D only in low-volatility mid-session context, density 5.5, hold4.",
        ),
        CandidateSpec(
            package_id="cp305F_cp304F_aggressive_flip_mid_density85_hold6_surface",
            source_package_id="cp304F_histgb_aggressive_curve_capped_density95_hold8_surface",
            transform_id="full_flip_mid",
            target_density=8.5,
            max_hold_bars=6,
            fixed_lot=0.16,
            atr_sltp_enabled=True,
            atr_stop_multiplier=1.85,
            atr_take_profit_multiplier=4.80,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            hypothesis="An aggressive flip branch tests whether cp304F's runtime loss scale can become profit scale without exceeding 10 trades/day.",
            changed_variables="flip cp304F mid-session, density 8.5, hold6, model risk cap 3.0%.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
    ]


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
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
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


def source_manifest() -> dict[str, dict[str, str]]:
    rows = read_csv_dicts(SOURCE_MANIFEST)
    return {row["package_id"]: row for row in rows}


def source_payload(spec: CandidateSpec, manifest: Mapping[str, Mapping[str, str]]) -> pd.DataFrame:
    row = manifest[spec.source_package_id]
    return pd.read_parquet(io_path(ROOT / row["payload_path"]))


def transform_signal(spec: CandidateSpec, source: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    timestamp = pd.to_datetime(source["timestamp"], utc=True)
    hour = timestamp.dt.hour.to_numpy()
    minutes = pd.to_numeric(source.get("minutes_from_cash_open", 0.0), errors="coerce").fillna(0.0).to_numpy()
    zabs = pd.to_numeric(source.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
    vol = pd.to_numeric(source.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy()
    adx = pd.to_numeric(source.get("adx_14", 20.0), errors="coerce").fillna(20.0).to_numpy()
    raw = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    base_score = pd.to_numeric(source.get("candidate_decision_score", 1.0), errors="coerce").fillna(1.0).abs().to_numpy(dtype="float64")
    if spec.transform_id == "full_flip_mid":
        keep = (minutes >= 30) & (minutes <= 330) & (zabs <= 1.90) & (vol <= 1.70)
        signal = (-raw).astype("int8")
        score = base_score * keep.astype("float64") * (1.0 + 0.10 * (adx >= 30))
    elif spec.transform_id == "full_flip_wide":
        keep = (minutes >= 15) & (minutes <= 330) & (zabs <= 2.10) & (vol <= 1.95)
        signal = (-raw).astype("int8")
        score = base_score * keep.astype("float64") * (1.0 + 0.08 * (hour >= 18))
    elif spec.transform_id == "hour19_direct_else_flip":
        keep = (minutes >= 30) & (minutes <= 330) & (zabs <= 2.00) & (vol <= 1.80)
        direct = ((hour == 19) | (hour == 22) | ((adx >= 45) & (minutes >= 150)))
        signal = np.where(direct, raw, -raw).astype("int8")
        score = base_score * keep.astype("float64") * (1.0 + 0.18 * direct.astype("float64"))
    elif spec.transform_id == "lowvol_flip":
        keep = (vol <= 0.90) & (zabs <= 1.80) & (minutes >= 30) & (minutes <= 330)
        signal = (-raw).astype("int8")
        score = base_score * keep.astype("float64") * (1.0 + 0.15 * (adx >= 24))
    else:
        keep = np.ones(len(raw), dtype=bool)
        signal = raw
        score = base_score
    signal = np.where(keep, signal, 0).astype("int8")
    signal = s294.trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score.astype("float64")


def metrics_for_payload(spec: CandidateSpec, payload: pd.DataFrame, split: str) -> dict[str, Any]:
    dataset = s290.load_dataset("fwd12_proxy58")[["timestamp", "split", "future_log_return_12"]].copy()
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    tier = payload.loc[payload["tier_scope"].astype(str).eq("Tier A")].copy()
    tier = tier.merge(dataset, on=["timestamp", "split"], how="left", validate="many_to_one")
    part = tier.loc[tier["split"].astype(str).eq(split)].copy()
    signal = pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    return s290.curve_metrics(part, signal, spec.max_hold_bars)


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
        "exit_risk_close_threshold": 0.5,
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


def materialize_payload(spec: CandidateSpec, manifest: Mapping[str, Mapping[str, str]]) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = source_payload(spec, manifest)
    signal, score = transform_signal(spec, source)
    branch_id = f"run305A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    payload["stage305_branch_id"] = branch_id
    payload["stage304_branch_id"] = payload.get("stage304_branch_id", manifest[spec.source_package_id].get("materialized_branch_id", ""))
    payload["stage303_branch_id"] = payload.get("stage303_branch_id", branch_id)
    payload["stage301_branch_id"] = payload.get("stage301_branch_id", branch_id)
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "runtime_realized_curve_attribution_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = spec.source_package_id
    payload["source_transform_id"] = spec.transform_id
    payload["source_active_mask"] = (pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy() != 0).astype("int8")
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct if spec.model_risk_sizing_enabled else 0.0
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_package_id": spec.source_package_id,
        "transform_id": spec.transform_id,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "risk_logic": risk_manifest_fields(spec),
        "direction_feature_order_hash": ordered_hash(FEATURE_ORDER),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(FEATURE_ORDER)
    payload["model_feature_order_hash"] = "rule_surface_no_model_artifact"
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = metrics_for_payload(spec, payload, "validation")
    oos_metrics = metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def gate_label(validation: Mapping[str, Any], oos: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(validation["trades_per_day"]) <= 10.0 and 4.0 <= float(oos["trades_per_day"]) <= 10.0
    elif gate == "edge":
        ok = float(validation["net_bp"]) > 0.0 and float(oos["net_bp"]) > 0.0 and float(validation["pf"]) >= 1.03 and float(oos["pf"]) >= 1.02
    else:
        ok = (
            float(validation["positive_month_share"]) >= 0.35
            and float(oos["positive_month_share"]) >= 0.45
            and float(validation["underwater_ratio"]) <= 0.94
            and float(oos["underwater_ratio"]) <= 0.94
        )
    return "passed" if ok else "failed"


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    return s290.supply_rows_for_payload(payload, spec)  # type: ignore[arg-type]


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    manifest = source_manifest()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, manifest)
        branch_id = f"run305A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_rule_surface.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage305_branch_id": branch_id,
                "source_package_id": spec.source_package_id,
                "package_id": spec.package_id,
                "feature_order": list(FEATURE_ORDER),
                "feature_order_hash": ordered_hash(FEATURE_ORDER),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage305 MT5 probe",
                "claim_boundary": BOUNDARY,
            },
        )
        candidate_supply = supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        den_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.35
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "Check whether runtime-realized loss direction inversion is worth MT5 runtime probing.",
                "comparison_baseline": "Stage304 actual MT5 negative review with parsed curve-pocket attribution.",
                "control_variables": "US100 M5 split_v1; source payloads from Stage304; Tier A/B paired runtime accounting; no Adapter or ONNX claim.",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Stage304 payload replay transformed by actual MT5 attribution clues; validation/OOS proxy and MT5 are evaluation.",
                "success_criteria": "validation/OOS both positive, 4-10 trades/day, profit scale, PF/recovery/expectancy acceptable, no deep parsed curve pocket.",
                "failure_criteria": "MT5 net scale absent, density outside 4-10, OOS negative, or curve pocket remains deep.",
                "invalid_conditions": "source payload missing, label/future leakage, feature order mismatch, or runtime report parse missing.",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise next stage must pivot away from this anti-surface family.",
                "evidence_plan": "branch queue, proxy scoreboard, payload manifest, MT5 queue, run305B KPI, run305C parsed curve review.",
                "feature_surface": "Stage304 source route_signal_value plus runtime-realized transform rules.",
                "model_surface": "rule_surface_no_train_model",
                "decision_surface": spec.transform_id,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; rule surface retained for Adapter trace if candidate gate passes.",
                "failure_memory_plan": "If runtime fails, record whether full flip, direct/flip router, density, or risk scale failed.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run305A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage305_branch_id": branch_id,
                "stage304_branch_id": manifest[spec.source_package_id].get("materialized_branch_id", ""),
                "stage303_branch_id": branch_id,
                "stage301_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "runtime_realized_curve_attribution_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file_lf_normalized(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "direction_surface_hash": identity["direction_surface_hash"],
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
                "model_family": "runtime_realized_rule_surface",
                "prediction_kind": "precomputed_direction_replay",
                "dataset_id": "fwd12_proxy58",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file_lf_normalized(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "imputation_path": rel(model_spec_path),
                "imputation_hash": sha256_file_lf_normalized(model_spec_path),
                "classes": "-1,0,1",
                "payoff_weight_policy": "runtime_realized_direction_transform",
                "onnx_exportability_note": "Adapter required before ONNX; rule surface and route_signal handoff are traceable.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": "fwd12_proxy58",
                "model_family": "runtime_realized_rule_surface",
                "prediction_kind": "direction_replay",
                "mode": spec.transform_id,
                "quantile": "",
                "threshold": "",
                "precondition": spec.transform_id,
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
        artifacts.extend([payload_path, handoff_path, model_spec_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, artifacts


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    result = [
        {
            "result_subject": "Stage305 runtime-realized curve attribution materialization",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI, Adapter package, ONNX parity",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage305 turns actual Stage304 loss direction into anti-surface candidates; it does not select before MT5 runtime evidence.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis", "status": "passed", "evidence_path": rel(EXPERIMENT_DESIGN), "effect": "Stage304 threshold repair is replaced with runtime-realized direction transform."},
        {"gate_name": "source_lineage", "status": "passed", "evidence_path": rel(LINEAGE), "effect": "Each candidate points back to a Stage304 source payload and review evidence."},
        {"gate_name": "proxy_density_edge_curve_screen", "status": "passed" if density_pass and edge_pass else "partial", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day and positive proxy are screened before MT5."},
        {"gate_name": "mt5_runtime_probe", "status": "prepared", "evidence_path": rel(MT5_QUEUE), "effect": "run305B can execute Tier A, Tier B fallback, and actual routed total attempts."},
        {"gate_name": "adapter_package", "status": "not_started", "evidence_path": "", "effect": "No Adapter before candidate gate."},
        {"gate_name": "onnx_readiness", "status": "not_started", "evidence_path": "", "effect": "ONNX waits for Adapter and parity gates."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = sorted(scoreboard_rows, key=lambda row: float(row["selection_score"]), reverse=True)
    lines = [
        "# run305A Runtime-Realized Curve Attribution Materialization(305A 런타임 실제 곡선 기여도 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage304(304단계) 실제 MT5(메타트레이더5) 손실 방향을 repair(수리)하지 않고 anti-surface(반대 표면) 후보로 재구성했다.",
        "",
        "| package(패키지) | transform(변환) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(거래우위) | curve(곡선) |",
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
    payload_artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, manifest_rows)
    write_csv_rows(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv_rows(MODEL_SCOREBOARD, s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv_rows(CANDIDATE_SUPPLY, s293.SUPPLY_COLUMNS, supply_rows)
    write_csv_rows(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MODEL_MANIFEST, MODEL_COLUMNS, model_rows)
    write_csv_rows(WFO_FOLD_SCOREBOARD, s293.WFO_COLUMNS, wfo_rows)
    write_csv_rows(RESULT_JUDGMENT, s293.RESULT_COLUMNS, result)
    write_csv_rows(GATE_AUDIT, s293.GATE_COLUMNS, gates)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Stage304 actual losing directions can be inverted or conditionally kept to create a stronger runtime-realized profit source.",
            "decision_use": "Open or reject MT5 runtime probe candidates before Adapter and ONNX work.",
            "comparison_baseline": "Stage304 actual MT5 negative review with parsed curve-pocket attribution.",
            "control_variables": ["US100 M5", "split_v1", "Stage304 source payloads", "Tier A/B paired accounting"],
            "changed_variables": ["direction transform", "density target", "hold horizon", "risk logic"],
            "success_criteria": ["MT5 validation/OOS positive", "minimum trade count", "4-10 trades/day", "PF/recovery/expectancy acceptable", "no deep parsed curve pocket"],
            "failure_criteria": ["weak net scale", "density outside 4-10", "OOS negative", "deep curve pocket"],
            "invalid_conditions": ["source payload missing", "feature order mismatch", "runtime report parse missing"],
            "stop_conditions": ["candidate gate pass moves to Adapter package", "otherwise pivot away from this anti-surface family"],
            "evidence_plan": [rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run305B MT5 KPI", "run305C parsed curve review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_review_scoreboard": rel(SOURCE_REVIEW_SCOREBOARD),
            "source_trade_quality": rel(SOURCE_TRADE_QUALITY),
            "source_stage305_queue": rel(SOURCE_STAGE305_QUEUE),
            "payload_future_label_columns_removed": True,
            "feature_order_hash": ordered_hash(FEATURE_ORDER),
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
            "producer": "stage_pipelines/stage305/design_runtime_realized_curve_attribution_rebuild.py",
            "inputs": [rel(SOURCE_REVIEW), rel(SOURCE_MANIFEST), rel(SOURCE_REVIEW_SCOREBOARD), rel(SOURCE_TRADE_QUALITY), rel(SOURCE_STAGE305_QUEUE)],
            "outputs": {"scoreboard": rel(MODEL_SCOREBOARD), "mt5_queue": rel(MT5_QUEUE), "report": rel(REPORT)},
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
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_realized_curve_attribution_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
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
                "record_view": "runtime_realized_curve_attribution_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "runtime_realized_curve_attribution",
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
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "runtime_realized_curve_attribution_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage305_runtime_realized_curve_attribution_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run305A runtime-realized curve attribution materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    safe_upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run305A_report", f"- run305A_report(305A 보고): `{rel(REPORT)}`\n- run305A_mt5_queue(305A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)
    review_index = read_text(REVIEW_INDEX) or "# Stage305 Review Index(305단계 검토 색인)\n"
    review_index = append_once(review_index, "run305A_report", f"- run305A_report(305A 보고): `{rel(REPORT)}`\n- run305A_mt5_queue(305A MT5 대기열): `{rel(MT5_QUEUE)}`")
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
        "run305A_summary",
        f"- run305A_summary(305A 요약): runtime-realized curve attribution(런타임 실제 곡선 기여도) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): Stage304(304단계) 손실 방향을 조건부 flip(반전)한 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage305(305단계) run305A(305A 실행) runtime-realized curve attribution materialization(런타임 실제 곡선 기여도 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run305A Runtime-realized curve attribution materialization(305A 런타임 실제 곡선 기여도 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 아직 없다.\n",
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
