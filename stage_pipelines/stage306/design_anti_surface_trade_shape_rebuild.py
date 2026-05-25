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

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage305 import design_runtime_realized_curve_attribution_rebuild as prev  # noqa: E402


STAGE_ID = "306_onnx_candidate_campaign__anti_surface_trade_shape_rebuild"
RUN_ID = "run306A_design_anti_surface_trade_shape_rebuild_v1"
RUN_NUMBER = "run306A"
SOURCE_STAGE_ID = "305_onnx_candidate_campaign__runtime_realized_curve_attribution_rebuild"
SOURCE_RUN_ID = "run305C_review_runtime_realized_curve_attribution_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_anti_surface_trade_shape_candidates_materialized_no_selection"
JUDGMENT = "anti_surface_trade_shape_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run306B_execute_anti_surface_trade_shape_mt5_probe"
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
SOURCE_RUN305A = SOURCE_STAGE / "02_runs" / "run305A"
SOURCE_RUN305C = SOURCE_STAGE / "02_runs" / "run305C"
SOURCE_MANIFEST = SOURCE_RUN305A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN305C / "runtime_realized_curve_attribution_review_scoreboard.csv"
SOURCE_TRADE_QUALITY = SOURCE_RUN305C / "trade_quality_summary.csv"
SOURCE_SESSION = SOURCE_RUN305C / "session_attribution.csv"
SOURCE_MONTHLY = SOURCE_RUN305C / "monthly_attribution.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN305C / "stage306_seed_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run305C_runtime_realized_curve_attribution_review_stage306_open_report.md"

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
REPORT = REVIEWS / "run306A_anti_surface_trade_shape_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

FEATURE_ORDER = ("route_signal_value",)

MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage306_branch_id",
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


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    source_package_ids: tuple[str, ...]
    transform_id: str
    target_density: float
    max_hold_bars: int
    fixed_lot: float
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_sizing_enabled: bool
    model_risk_max_pct: float
    hypothesis: str
    changed_variables: str
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    atr_sltp_enabled: bool = True
    atr_period: int = 14
    model_risk_min_pct: float = 0.006
    model_risk_confidence_floor: float = 0.54
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            package_id="cp306A_cp305D_good_pocket_direct_density50_hold4_surface",
            source_package_ids=("cp305D_cp304C_broad_flip_density65_hold4_surface",),
            transform_id="good_pocket_direct",
            target_density=5.0,
            max_hold_bars=4,
            fixed_lot=0.26,
            atr_stop_multiplier=1.45,
            atr_take_profit_multiplier=4.30,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.028,
            hypothesis="Use cp305D only where actual MT5 trade attribution showed favorable hour, volatility, ADX, and z-shape pockets.",
            changed_variables="suppress hour 17/18/21 and ADX 24-30 pockets; keep hour 19/20/22 and favorable volatility/z-shape; density 5/day; higher payoff ratio.",
        ),
        CandidateSpec(
            package_id="cp306B_cp305D_bad_pocket_inverse_density65_hold3_surface",
            source_package_ids=("cp305D_cp304C_broad_flip_density65_hold4_surface",),
            transform_id="bad_pocket_inverse",
            target_density=6.5,
            max_hold_bars=3,
            fixed_lot=0.24,
            atr_stop_multiplier=1.25,
            atr_take_profit_multiplier=3.90,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
            hypothesis="The largest Stage305 losses were concentrated in repeatable buckets, so inverse entries there may create scale without adding new model training.",
            changed_variables="direct favorable pockets, invert hour 17/18/21 plus ADX 24-30 or bad-vol pockets, density 6.5/day, tight hold3 risk.",
        ),
        CandidateSpec(
            package_id="cp306C_cp305C305D_hour20_payoff_router_density70_hold5_surface",
            source_package_ids=(
                "cp305C_cp304E_hour19_direct_else_flip_density80_hold6_surface",
                "cp305D_cp304C_broad_flip_density65_hold4_surface",
            ),
            transform_id="hour20_payoff_router",
            target_density=7.0,
            max_hold_bars=5,
            fixed_lot=0.24,
            atr_stop_multiplier=1.55,
            atr_take_profit_multiplier=4.80,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            hypothesis="Route cp305C's hour19/22 edge and cp305D's hour20 edge into one trade-shape surface, while flattening the worst actual pockets.",
            changed_variables="multi-source hour router: cp305C for hour19/22, cp305D for hour20/late favorable pockets, suppress hour18 and bad-vol/ADX pockets.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp306D_cp305E_vol_adx_payoff_shape_density55_hold5_surface",
            source_package_ids=("cp305E_cp304D_lowvol_flip_density55_hold4_surface",),
            transform_id="vol_adx_payoff_shape",
            target_density=5.5,
            max_hold_bars=5,
            fixed_lot=0.28,
            atr_stop_multiplier=1.35,
            atr_take_profit_multiplier=4.60,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.026,
            hypothesis="cp305E had validation efficiency, so rebuild it as a volatility/ADX payoff-shape surface rather than a low-vol-only flip.",
            changed_variables="avoid very low volatility and mid-z pockets, prefer vol 0.95-1.40 with ADX 18-24/30-36/>45, density 5.5/day.",
        ),
        CandidateSpec(
            package_id="cp306E_cp305F_late_runner_density85_hold8_surface",
            source_package_ids=("cp305F_cp304F_aggressive_flip_mid_density85_hold6_surface",),
            transform_id="late_runner",
            target_density=8.5,
            max_hold_bars=8,
            fixed_lot=0.20,
            atr_stop_multiplier=1.75,
            atr_take_profit_multiplier=5.40,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.034,
            hypothesis="cp305F produced validation profit scale but failed OOS; isolate late-session runner trades to test whether scale survives with fewer bad pockets.",
            changed_variables="late-session direct surface, suppress cash-open and hour18/21 loss pockets, keep longer hold8 and aggressive TP.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp306F_blended_trade_shape_scale_density90_hold4_surface",
            source_package_ids=(
                "cp305C_cp304E_hour19_direct_else_flip_density80_hold6_surface",
                "cp305D_cp304C_broad_flip_density65_hold4_surface",
                "cp305E_cp304D_lowvol_flip_density55_hold4_surface",
            ),
            transform_id="blended_trade_shape_scale",
            target_density=9.0,
            max_hold_bars=4,
            fixed_lot=0.22,
            atr_stop_multiplier=1.40,
            atr_take_profit_multiplier=4.20,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.032,
            hypothesis="Blend the three positive Stage305 sources by realized trade-shape buckets to target scale while staying inside 4-10 trades/day.",
            changed_variables="source blend by hour/vol/ADX/z pocket, inverse only for the worst pockets, density 9/day, hold4.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return prev.rel(path)


def read_text(path: Path) -> str:
    return prev.read_text(path)


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    prev.write_json(path, payload, bom=bom)


def write_md(path: Path, text: str) -> None:
    prev.write_md(path, text)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    return prev.read_csv_dicts(path)


def safe_upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    prev.safe_upsert_csv_rows(path, columns, rows, key)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return prev.replace_line_prefix(text, prefix, replacement)


def append_once(text: str, marker: str, addition: str) -> str:
    return prev.append_once(text, marker, addition)


def prepend_focus(text: str, focus: str, marker: str) -> str:
    return prev.prepend_focus(text, focus, marker)


def source_manifest() -> dict[str, dict[str, str]]:
    return {row["package_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def source_payloads(spec: CandidateSpec, manifest: Mapping[str, Mapping[str, str]]) -> dict[str, pd.DataFrame]:
    payloads: dict[str, pd.DataFrame] = {}
    for package_id in spec.source_package_ids:
        row = manifest[package_id]
        payloads[package_id] = pd.read_parquet(prev.io_path(ROOT / row["payload_path"]))
    return payloads


def signal_components(payload: pd.DataFrame) -> dict[str, np.ndarray]:
    timestamp = pd.to_datetime(payload["timestamp"], utc=True)
    hour = timestamp.dt.hour.to_numpy()
    minutes = pd.to_numeric(payload.get("minutes_from_cash_open", 0.0), errors="coerce").fillna(0.0).to_numpy()
    zabs = pd.to_numeric(payload.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
    vol = pd.to_numeric(payload.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy()
    adx = pd.to_numeric(payload.get("adx_14", 20.0), errors="coerce").fillna(20.0).to_numpy()
    score = pd.to_numeric(payload.get("candidate_decision_score", 1.0), errors="coerce").fillna(1.0).abs().to_numpy(dtype="float64")
    prob_long = pd.to_numeric(payload.get("prob_long", 0.0), errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    prob_short = pd.to_numeric(payload.get("prob_short", 0.0), errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    payoff_dir = pd.to_numeric(payload.get("payoff_edge_direction", 0.0), errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    model_dir = np.where(np.abs(payoff_dir) > 0.0, np.sign(payoff_dir), np.sign(prob_long - prob_short)).astype("int8")
    raw = pd.to_numeric(payload["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    base = np.where(raw != 0, raw, model_dir).astype("int8")
    return {
        "hour": hour,
        "minutes": minutes,
        "zabs": zabs,
        "vol": vol,
        "adx": adx,
        "score": score,
        "raw": raw,
        "base": base,
        "model_dir": model_dir,
    }


def pocket_masks(c: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    hour = c["hour"]
    minutes = c["minutes"]
    zabs = c["zabs"]
    vol = c["vol"]
    adx = c["adx"]
    good_session = ((hour == 19) | (hour == 20) | ((hour == 22) & (minutes >= 300))) & (minutes >= 120) & (minutes <= 360)
    late_runner = ((hour == 19) | (hour == 20) | (hour == 22)) & (minutes >= 150) & (minutes <= 360)
    bad_session = (hour == 18) | ((hour == 17) & (minutes >= 30)) | (hour == 21) | ((minutes >= 60) & (minutes < 120)) | ((minutes >= 240) & (minutes < 300))
    good_adx = ((adx >= 18) & (adx < 24)) | ((adx >= 30) & (adx < 36)) | (adx >= 45)
    bad_adx = (adx >= 24) & (adx < 30)
    good_vol = ((vol >= 0.95) & (vol <= 1.40)) | (((hour == 19) | (hour == 21)) & (vol >= 0.75) & (vol < 0.95))
    bad_vol = (vol < 0.75) | (vol > 1.80) | (((hour == 17) | (hour == 18)) & (vol < 0.95))
    z_good = (zabs <= 0.80) | ((zabs >= 1.70) & (zabs <= 2.40))
    z_bad = (zabs > 0.80) & (zabs < 1.70)
    return {
        "good_session": good_session,
        "late_runner": late_runner,
        "bad_session": bad_session,
        "good_adx": good_adx,
        "bad_adx": bad_adx,
        "good_vol": good_vol,
        "bad_vol": bad_vol,
        "z_good": z_good,
        "z_bad": z_bad,
        "good_shape": good_session & good_adx & good_vol & z_good,
        "bad_shape": bad_session & (bad_adx | bad_vol | z_bad),
    }


def align_secondary(primary: pd.DataFrame, secondary: pd.DataFrame, column: str) -> np.ndarray:
    if len(primary) == len(secondary) and primary["timestamp"].equals(secondary["timestamp"]) and primary["tier_scope"].equals(secondary["tier_scope"]):
        return pd.to_numeric(secondary[column], errors="coerce").fillna(0).astype("int8").to_numpy()
    key_cols = ["timestamp", "split", "tier_scope"]
    merged = primary[key_cols].merge(secondary[key_cols + [column]], on=key_cols, how="left", validate="one_to_one")
    return pd.to_numeric(merged[column], errors="coerce").fillna(0).astype("int8").to_numpy()


def transform_signal(spec: CandidateSpec, payloads: Mapping[str, pd.DataFrame]) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    primary = payloads[spec.source_package_ids[0]].copy()
    c = signal_components(primary)
    masks = pocket_masks(c)
    raw = c["raw"]
    base = c["base"]
    score = c["score"].copy()
    signal = np.zeros(len(primary), dtype="int8")

    if spec.transform_id == "good_pocket_direct":
        keep = (
            ((c["hour"] == 19) | (c["hour"] == 20) | (c["hour"] == 22) | ((c["hour"] == 17) & (c["vol"] >= 0.95) & (c["vol"] <= 1.15)))
            & (c["minutes"] >= 60)
            & (c["minutes"] <= 360)
            & (masks["good_adx"] | masks["good_vol"])
            & ~((c["hour"] == 18) | ((c["hour"] == 21) & masks["bad_vol"]))
        )
        signal = np.where(keep, base, 0).astype("int8")
        score = score * keep.astype("float64") * (1.0 + 0.25 * (c["hour"] == 20))
    elif spec.transform_id == "bad_pocket_inverse":
        direct = ((c["hour"] == 19) | (c["hour"] == 20) | (c["hour"] == 22)) & (c["minutes"] >= 90) & (c["minutes"] <= 360) & ~masks["bad_vol"]
        inverse = ((c["hour"] == 17) | (c["hour"] == 18) | ((c["hour"] == 21) & masks["bad_adx"]) | masks["bad_shape"]) & (c["minutes"] >= 30) & (c["minutes"] <= 330)
        signal = np.where(direct, base, np.where(inverse, -base, 0)).astype("int8")
        score = score * (direct.astype("float64") * 1.15 + inverse.astype("float64") * 0.95)
    elif spec.transform_id == "hour20_payoff_router":
        second = align_secondary(primary, payloads[spec.source_package_ids[1]], "route_signal_value")
        second = np.where(second != 0, second, base).astype("int8")
        keep_c = ((c["hour"] == 19) | (c["hour"] == 22)) & (c["minutes"] >= 90) & (c["minutes"] <= 360) & ~masks["bad_vol"]
        keep_d = ((c["hour"] == 20) | ((c["hour"] == 21) & masks["good_vol"])) & (masks["good_adx"] | (c["vol"] >= 0.75)) & ~((c["zabs"] > 1.20) & (c["zabs"] < 1.70))
        fallback = (c["minutes"] >= 150) & (c["minutes"] <= 330) & masks["good_adx"] & masks["good_vol"]
        signal = np.where(keep_c, base, np.where(keep_d | fallback, second, 0)).astype("int8")
        score = score * (keep_c.astype("float64") * 1.20 + keep_d.astype("float64") * 1.30)
    elif spec.transform_id == "vol_adx_payoff_shape":
        direct = ((c["vol"] >= 0.75) & (c["vol"] <= 1.40) & (masks["good_adx"] | (c["hour"] == 20)) & (c["minutes"] >= 60) & (c["minutes"] <= 360) & ~(c["hour"] == 18))
        inverse = (c["hour"] == 18) & masks["bad_adx"] & (c["minutes"] >= 60) & (c["minutes"] <= 210)
        signal = np.where(direct, base, np.where(inverse, -base, 0)).astype("int8")
        score = score * (direct.astype("float64") * 1.15 + inverse.astype("float64") * 0.80)
    elif spec.transform_id == "late_runner":
        keep = (((c["hour"] == 19) | (c["hour"] == 20) | (c["hour"] == 22) | ((c["hour"] == 21) & masks["good_vol"])) & (c["minutes"] >= 120) & (c["minutes"] <= 360) & (masks["good_adx"] | (c["vol"] >= 0.75)) & ~((c["vol"] < 0.75) & (c["hour"] == 22)))
        signal = np.where(keep, base, 0).astype("int8")
        score = score * keep.astype("float64") * (1.0 + 0.30 * (c["hour"] == 20) + 0.15 * (c["hour"] == 22))
    elif spec.transform_id == "blended_trade_shape_scale":
        raw_c = base
        raw_d = align_secondary(primary, payloads[spec.source_package_ids[1]], "route_signal_value")
        raw_e = align_secondary(primary, payloads[spec.source_package_ids[2]], "route_signal_value")
        raw_d = np.where(raw_d != 0, raw_d, base).astype("int8")
        raw_e = np.where(raw_e != 0, raw_e, base).astype("int8")
        use_c = ((c["hour"] == 19) | (c["hour"] == 22)) & (c["minutes"] >= 90) & (c["minutes"] <= 360) & ~masks["bad_vol"]
        use_d = ((c["hour"] == 20) | ((c["hour"] == 17) & (c["vol"] >= 0.95) & (c["vol"] <= 1.15))) & ((c["adx"] >= 18) | (c["vol"] >= 0.95)) & ~((c["vol"] < 0.75) & (c["minutes"] < 180))
        use_e = ((c["minutes"] >= 120) & (c["minutes"] <= 300) & (c["vol"] >= 0.75) & (c["vol"] <= 1.40) & (masks["z_good"] | masks["good_adx"]))
        inverse = (c["hour"] == 18) & masks["bad_adx"] & masks["bad_vol"]
        signal = np.where(use_c, raw_c, np.where(use_d, raw_d, np.where(use_e, raw_e, np.where(inverse, -raw_d, 0)))).astype("int8")
        score = score * (use_c.astype("float64") * 1.10 + use_d.astype("float64") * 1.25 + use_e.astype("float64") * 1.00 + inverse.astype("float64") * 0.70)
    else:
        raise ValueError(f"unknown transform_id: {spec.transform_id}")

    signal = np.where(base != 0, signal, 0).astype("int8")
    score = np.where(signal != 0, np.maximum(score, 1e-6), 0.0).astype("float64")
    signal = prev.s294.trim_to_density(primary, signal, score, spec.max_hold_bars, spec.target_density)
    return primary, signal.astype("int8"), score.astype("float64")


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
    payloads = source_payloads(spec, manifest)
    source, signal, score = transform_signal(spec, payloads)
    branch_id = f"run306A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    source_row = manifest[spec.source_package_ids[0]]
    payload["stage306_branch_id"] = branch_id
    payload["stage305_branch_id"] = payload.get("stage305_branch_id", source_row.get("materialized_branch_id", ""))
    payload["stage304_branch_id"] = payload.get("stage304_branch_id", "")
    payload["stage303_branch_id"] = payload.get("stage303_branch_id", "")
    payload["stage301_branch_id"] = payload.get("stage301_branch_id", "")
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "anti_surface_trade_shape_rebuild_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = "|".join(spec.source_package_ids)
    payload["source_transform_id"] = spec.transform_id
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [prev.s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct if spec.model_risk_sizing_enabled else 0.0
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_package_ids": list(spec.source_package_ids),
        "transform_id": spec.transform_id,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "feature_order": list(FEATURE_ORDER),
        "risk_logic": risk_manifest_fields(spec),
        "trade_shape_thesis": "actual Stage305 MT5 trade attribution: avoid/suppress 17-18/21, ADX 24-30, very-low-vol and mid-z pockets; emphasize 19/20/22 favorable pockets.",
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(FEATURE_ORDER)
    payload["model_feature_order_hash"] = "rule_surface_no_model_artifact"
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = prev.metrics_for_payload(spec, payload, "validation")
    oos_metrics = prev.metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def gate_label(validation: Mapping[str, Any], oos: Mapping[str, Any], gate: str) -> str:
    return prev.gate_label(validation, oos, gate)


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    frame = payload.copy()
    frame["date"] = pd.to_datetime(frame["timestamp"], utc=True).dt.date.astype(str)
    for (tier_scope, split), part in frame.groupby(["tier_scope", "split"], observed=True):
        active = part.loc[pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).ne(0)]
        days = max(1, int(part["date"].nunique()))
        approx_trade_count = int(len(active) / max(1, spec.max_hold_bars))
        approx_tpd = approx_trade_count / days
        rows.append(
            {
                "materialized_branch_id": str(part["materialized_branch_id"].iloc[0]),
                "package_id": spec.package_id,
                "tier_scope": tier_scope,
                "split": split,
                "rows": len(part),
                "days": days,
                "active_signal_count": len(active),
                "long_signal_count": int((pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0) > 0).sum()),
                "short_signal_count": int((pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0) < 0).sum()),
                "active_signals_per_day": len(active) / days,
                "approx_trade_count": approx_trade_count,
                "approx_trades_per_day": approx_tpd,
                "max_hold_bars": spec.max_hold_bars,
                "trade_density_screen": "passed" if 4.0 <= approx_tpd <= 10.0 else "failed",
            }
        )
    return rows


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
        branch_id = f"run306A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_rule_surface.json"
        prev.io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(prev.io_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage306_branch_id": branch_id,
                "source_package_ids": list(spec.source_package_ids),
                "package_id": spec.package_id,
                "feature_order": list(FEATURE_ORDER),
                "feature_order_hash": ordered_hash(FEATURE_ORDER),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage306 MT5 probe",
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
            prev.s290.selection_score(validation_metrics)
            + prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.50
            + min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])) * 20.0
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "Check whether actual MT5 trade-shape attribution can create a higher-scale ONNX-worthy candidate seed.",
                "comparison_baseline": "Stage305 actual MT5 positive-but-small direction-flip review.",
                "control_variables": "US100 M5 split_v1; Stage305 source payloads; Tier A/B paired runtime accounting; no Adapter or ONNX claim.",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Stage305 payload replay transformed by actual MT5 session/volatility/ADX/z-shape attribution.",
                "success_criteria": "MT5 validation/OOS positive, minimum trade count, 4-10 trades/day, profit scale, PF/recovery/expectancy, and no deep parsed curve pocket.",
                "failure_criteria": "Profit scale absent, OOS negative, density outside 4-10, or parsed curve pocket remains deep.",
                "invalid_conditions": "source payload missing, feature order mismatch, label leakage, or MT5 report parse missing.",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise close Stage306 and pivot to a new source instead of micro repair.",
                "evidence_plan": "branch queue, proxy scoreboard, payload manifest, MT5 queue, run306B KPI, run306C parsed curve review.",
                "feature_surface": "Stage305 source payload features: hour/minute, volatility, ADX, z-shape, route_signal_value.",
                "model_surface": "rule_surface_no_train_model",
                "decision_surface": spec.transform_id,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; rule surface retained for Adapter trace if candidate gate passes.",
                "failure_memory_plan": "Record which trade-shape bucket failed: session, volatility, ADX, z-shape, blend, density, or risk scale.",
                "claim_boundary": BOUNDARY,
            }
        )
        source_row = manifest[spec.source_package_ids[0]]
        manifest_rows.append(
            {
                "queue_id": f"run306A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage306_branch_id": branch_id,
                "stage305_branch_id": source_row.get("materialized_branch_id", ""),
                "stage304_branch_id": source_row.get("stage304_branch_id", ""),
                "stage303_branch_id": source_row.get("stage303_branch_id", ""),
                "stage301_branch_id": source_row.get("stage301_branch_id", ""),
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "anti_surface_trade_shape_rebuild_surface",
                "payload_path": rel(payload_path),
                "payload_hash": prev.sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": prev.sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": prev.sha256_file_lf_normalized(model_spec_path),
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
                "model_family": "anti_surface_trade_shape_rule_surface",
                "prediction_kind": "precomputed_direction_replay",
                "dataset_id": "fwd12_proxy58",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": prev.sha256_file_lf_normalized(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "imputation_path": rel(model_spec_path),
                "imputation_hash": prev.sha256_file_lf_normalized(model_spec_path),
                "classes": "-1,0,1",
                "payoff_weight_policy": "actual_mt5_trade_shape_attribution",
                "onnx_exportability_note": "Adapter required before ONNX; rule surface and route_signal handoff are traceable.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": "fwd12_proxy58",
                "model_family": "anti_surface_trade_shape_rule_surface",
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
            "result_subject": "Stage306 anti-surface trade-shape materialization",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI, Adapter package, ONNX parity",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage306 turns actual Stage305 trade-shape attribution into new runtime probe surfaces; it does not select before MT5 evidence.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis", "status": "passed", "evidence_path": rel(EXPERIMENT_DESIGN), "effect": "Direction flip repair is replaced with trade-shape routing by session/volatility/ADX/z pockets."},
        {"gate_name": "source_lineage", "status": "passed", "evidence_path": rel(LINEAGE), "effect": "Each branch points back to Stage305 source payloads and actual MT5 review evidence."},
        {"gate_name": "proxy_density_edge_curve_screen", "status": "passed" if density_pass and edge_pass else "partial", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day and proxy edge are screened before MT5."},
        {"gate_name": "mt5_runtime_probe", "status": "prepared", "evidence_path": rel(MT5_QUEUE), "effect": "run306B can execute Tier A, Tier B fallback, and actual routed total attempts."},
        {"gate_name": "adapter_package", "status": "not_started", "evidence_path": "", "effect": "No Adapter before candidate gate."},
        {"gate_name": "onnx_readiness", "status": "not_started", "evidence_path": "", "effect": "ONNX waits for Adapter and parity gates."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = sorted(scoreboard_rows, key=lambda row: float(row["selection_score"]), reverse=True)
    lines = [
        "# run306A Anti-Surface Trade Shape Materialization",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage305(305단계)의 실제 MT5(메타트레이더5) 거래 기여도를 사용해 session/volatility/ADX/z-shape(세션/변동성/추세강도/변동 형태) 기준의 새 후보를 만들었다.",
        "",
        "| package(패키지) | transform(변환) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |",
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
    lines.extend(["", f"- mt5_queue_rows(MT5 대기열 수): `{len(manifest_rows)}`", f"- claim_boundary(주장 경계): `{BOUNDARY}`"])
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
    prev.write_csv_rows(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    prev.write_csv_rows(MODEL_SCOREBOARD, prev.s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    prev.write_csv_rows(CANDIDATE_SUPPLY, prev.s293.SUPPLY_COLUMNS, supply_rows)
    prev.write_csv_rows(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    prev.write_csv_rows(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    prev.write_csv_rows(MODEL_MANIFEST, prev.MODEL_COLUMNS, model_rows)
    prev.write_csv_rows(WFO_FOLD_SCOREBOARD, prev.s293.WFO_COLUMNS, wfo_rows)
    prev.write_csv_rows(RESULT_JUDGMENT, prev.s293.RESULT_COLUMNS, result)
    prev.write_csv_rows(GATE_AUDIT, prev.s293.GATE_COLUMNS, gates)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Actual MT5 trade-shape attribution can rebuild the Stage305 small-positive surfaces into higher-scale candidates.",
            "decision_use": "Open or reject MT5 runtime probe candidates before Adapter and ONNX work.",
            "comparison_baseline": "Stage305 actual MT5 positive-but-small direction-flip review.",
            "control_variables": ["US100 M5", "split_v1", "Stage305 source payloads", "Tier A/B paired accounting"],
            "changed_variables": ["session router", "volatility/ADX/z-shape pockets", "source blending", "density target", "hold horizon", "risk logic"],
            "sample_scope": "Stage305 payload replay transformed by actual MT5 trade attribution.",
            "success_criteria": ["MT5 validation/OOS positive", "minimum trade count", "4-10 trades/day", "profit scale", "PF/recovery/expectancy acceptable", "no deep parsed curve pocket"],
            "failure_criteria": ["weak net scale", "density outside 4-10", "OOS negative", "deep curve pocket"],
            "invalid_conditions": ["source payload missing", "feature order mismatch", "runtime report parse missing"],
            "stop_conditions": ["candidate gate pass moves to Adapter package", "otherwise pivot away from this trade-shape packet"],
            "evidence_plan": [rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run306B MT5 KPI", "run306C parsed curve review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_trade_quality": rel(SOURCE_TRADE_QUALITY),
            "source_session_attribution": rel(SOURCE_SESSION),
            "source_monthly_attribution": rel(SOURCE_MONTHLY),
            "source_seed_queue": rel(SOURCE_SEED_QUEUE),
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
            "artifacts": [rel(path) for path in artifacts if path != RUN_MANIFEST and prev.path_exists(path)],
            "created_at_utc": created_at,
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": "stage_pipelines/stage306/design_anti_surface_trade_shape_rebuild.py",
            "source_inputs": [rel(SOURCE_REVIEW), rel(SOURCE_MANIFEST), rel(SOURCE_SCOREBOARD), rel(SOURCE_TRADE_QUALITY), rel(SOURCE_SESSION), rel(SOURCE_MONTHLY), rel(SOURCE_SEED_QUEUE)],
            "consumer": "run306B_execute_anti_surface_trade_shape_mt5_probe",
            "artifact_paths": {"scoreboard": rel(MODEL_SCOREBOARD), "mt5_queue": rel(MT5_QUEUE), "report": rel(REPORT)},
            "availability": "tracked_manifest_plus_reproducible_payloads",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return artifacts


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    safe_upsert_csv_rows(
        RUN_REGISTRY,
        prev.RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "anti_surface_trade_shape_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="run_id",
    )
    safe_upsert_csv_rows(
        ALPHA_LEDGER,
        prev.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "anti_surface_trade_shape_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "anti_surface_trade_shape",
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
        prev.s293.STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "anti_surface_trade_shape_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage306_anti_surface_trade_shape_artifact",
            "path": rel(path),
            "sha256": prev.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run306A anti-surface trade-shape materialization",
        }
        for path in artifacts
        if prev.path_exists(path)
    ]
    safe_upsert_csv_rows(ARTIFACT_REGISTRY, prev.s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    brief = "\n".join(
        [
            "# Stage306 Brief(306단계 개요)",
            "",
            f"- stage_id(단계 ID): `{STAGE_ID}`",
            f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            "- question(질문): Can actual MT5 trade-shape attribution rebuild a higher-scale, smoother ONNX-worthy candidate seed rather than repeating direction-flip repair?",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "Effect(효과): Stage305(305단계)의 작지만 양수인 runtime evidence(런타임 근거)를 새 trade-shape(거래 형태) 후보의 seed data(씨앗 데이터)로만 사용한다.",
        ]
    )
    write_md(STAGE_ROOT / "00_spec" / "stage_brief.md", brief)
    selected = "\n".join(
        [
            "# Stage306 Selection Status(306단계 선택 상태)",
            "",
            f"- stage_status(단계 상태): `{STATUS}`",
            f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`",
            f"- current_run(현재 실행): `{RUN_ID}`",
            f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
            "- target_candidate(목표 후보): `none`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(온엑스 준비): `not_started`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            f"- run306A_report(306A 보고서): `{rel(REPORT)}`",
            f"- run306A_mt5_queue(306A MT5 대기열): `{rel(MT5_QUEUE)}`",
        ]
    )
    write_md(SELECTED, selected)
    review_index = "\n".join(
        [
            "# Stage306 Review Index(306단계 검토 색인)",
            "",
            f"- run306A_report(306A 보고서): `{rel(REPORT)}`",
            f"- run306A_mt5_queue(306A MT5 대기열): `{rel(MT5_QUEUE)}`",
        ]
    )
    write_md(REVIEW_INDEX, review_index)
    idea_text = read_text(IDEA_REGISTER)
    idea_text = append_once(
        idea_text,
        "stage306_anti_surface_trade_shape",
        "## stage306_anti_surface_trade_shape\n\n- hypothesis(가설): actual MT5(메타트레이더5) trade-shape attribution(거래 형태 기여도) can create a larger smoother candidate than direction-flip repair.\n- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).\n",
    )
    write_md(IDEA_REGISTER, idea_text)
    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run306A_summary",
        f"- run306A_summary(306A 요약): anti-surface trade-shape(반표면 거래 형태) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): Stage305(305단계)의 작고 불안정한 양수 결과를 session/volatility/ADX/z-shape(세션/변동성/추세강도/변동 형태) 후보로 바꾸고 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었으며, 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage306(306단계) run306A(306A 실행) anti-surface trade-shape materialization(반표면 거래 형태 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run306A Anti-surface trade-shape materialization(306A 반표면 거래 형태 물질화)\n\n"
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
