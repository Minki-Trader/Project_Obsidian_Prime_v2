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
from stage_pipelines.stage296 import design_density_floor_profit_expansion_rebuild as s296  # noqa: E402
from stage_pipelines.stage301 import design_orthogonal_profit_source_rebuild as s301  # noqa: E402


STAGE_ID = "302_onnx_candidate_campaign__payoff_convexity_profit_scale_rebuild"
RUN_ID = "run302A_design_payoff_convexity_profit_scale_rebuild_v1"
RUN_NUMBER = "run302A"
SOURCE_STAGE_ID = "301_onnx_candidate_campaign__orthogonal_profit_source_rebuild"
SOURCE_RUN_ID = "run301C_review_orthogonal_profit_source_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
NEXT_ACTION = "run302B_execute_payoff_convexity_profit_scale_mt5_probe"
STATUS = "completed_payoff_convexity_profit_scale_candidates_materialized_no_selection"
JUDGMENT = "payoff_convexity_profit_scale_inputs_materialized_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

DATASET_ID = s301.DATASET_ID
FEATURE_ORDER = ("route_signal_value",)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run301C_orthogonal_profit_source_review_stage302_open_report.md"
SOURCE_SCOREBOARD = SOURCE_STAGE / "02_runs" / "run301C" / "orthogonal_profit_source_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_STAGE / "02_runs" / "run301C" / "stage302_seed_queue.csv"

PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MODEL_DIR = RUN_ROOT / "models"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
MODEL_RECEIPT = RUN_ROOT / "payoff_convexity_model_receipt.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run302A_payoff_convexity_profit_scale_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

BRANCH_COLUMNS = s301.BRANCH_COLUMNS
MODEL_RECEIPT_COLUMNS = s301.MODEL_RECEIPT_COLUMNS
MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage302_branch_id",
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


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    model_key: str
    filter_id: str
    score_mode: str
    target_density: float
    max_hold_bars: int
    score_quantile: float
    close_on_flat_signal: bool
    same_direction_reentry_cooldown_bars: int
    atr_sltp_enabled: bool
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_sizing_enabled: bool
    model_risk_max_pct: float
    thesis: str
    changed_variables: str
    risk_logic: str
    dataset_id: str = DATASET_ID
    atr_period: int = 14
    atr_min_stop_points: float = 0.0
    atr_max_stop_points: float = 0.0
    atr_min_take_profit_points: float = 0.0
    atr_max_take_profit_points: float = 0.0
    model_risk_min_pct: float = 0.005
    model_risk_confidence_floor: float = 0.55
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10
    fixed_lot: float = 0.10


CANDIDATES: tuple[CandidateSpec, ...] = (
    CandidateSpec(
        package_id="cp302A_hgb10_quiet_revert_atrscore_hold8_density95_atr_rr_surface",
        model_key="hgb_inverse_l2_0p10_unweighted",
        filter_id="quiet_revert",
        score_mode="atr",
        target_density=9.5,
        max_hold_bars=8,
        score_quantile=0.20,
        close_on_flat_signal=False,
        same_direction_reentry_cooldown_bars=2,
        atr_sltp_enabled=True,
        atr_stop_multiplier=2.05,
        atr_take_profit_multiplier=4.95,
        model_risk_sizing_enabled=True,
        model_risk_max_pct=0.024,
        thesis="The small Stage301 edge may need quiet-regime payoff convexity rather than more threshold repair.",
        changed_variables="regularized inverse HGB, quiet-revert filter, ATR-weighted score, hold8, density 9.5, ATR SL/TP, model risk sizing.",
        risk_logic="ATR stop 2.05, ATR take-profit 4.95, model risk cap 2.4%, close_on_flat=false, same-side cooldown2.",
    ),
    CandidateSpec(
        package_id="cp302B_hgb10_cash_mid_late_atrscore_hold8_density95_atr_rr_surface",
        model_key="hgb_inverse_l2_0p10_unweighted",
        filter_id="cash_mid_late",
        score_mode="atr",
        target_density=9.5,
        max_hold_bars=8,
        score_quantile=0.20,
        close_on_flat_signal=False,
        same_direction_reentry_cooldown_bars=2,
        atr_sltp_enabled=True,
        atr_stop_multiplier=2.18,
        atr_take_profit_multiplier=5.05,
        model_risk_sizing_enabled=True,
        model_risk_max_pct=0.026,
        thesis="Cash-to-late session coverage may preserve density while ATR payoff asymmetry handles scale.",
        changed_variables="cash-mid-late filter, regularized inverse HGB, ATR score, hold8, density 9.5, risk cap 2.6%.",
        risk_logic="ATR stop 2.18, ATR take-profit 5.05, model risk cap 2.6%, close_on_flat=false, same-side cooldown2.",
    ),
    CandidateSpec(
        package_id="cp302C_hgb02_quiet_revert_atrscore_hold4_density45_fixed_control_surface",
        model_key="hgb_inverse_l2_0p02_unweighted",
        filter_id="quiet_revert",
        score_mode="atr",
        target_density=4.5,
        max_hold_bars=4,
        score_quantile=0.20,
        close_on_flat_signal=True,
        same_direction_reentry_cooldown_bars=0,
        atr_sltp_enabled=False,
        atr_stop_multiplier=0.0,
        atr_take_profit_multiplier=0.0,
        model_risk_sizing_enabled=False,
        model_risk_max_pct=0.0,
        thesis="Defensive control: confirm whether quiet-revert selection alone improves OOS quality without risk scaling.",
        changed_variables="unregularized inverse HGB, quiet-revert filter, ATR score, hold4, density 4.5, fixed lot.",
        risk_logic="fixed lot 0.10, close_on_flat=true, no ATR SL/TP, no model risk sizing.",
    ),
    CandidateSpec(
        package_id="cp302D_hgb10_balanced_band_atrscore_hold8_density75_defensive_rr_surface",
        model_key="hgb_inverse_l2_0p10_unweighted",
        filter_id="balanced_band",
        score_mode="atr",
        target_density=7.5,
        max_hold_bars=8,
        score_quantile=0.20,
        close_on_flat_signal=False,
        same_direction_reentry_cooldown_bars=3,
        atr_sltp_enabled=True,
        atr_stop_multiplier=1.86,
        atr_take_profit_multiplier=4.20,
        model_risk_sizing_enabled=True,
        model_risk_max_pct=0.0215,
        thesis="Balanced volatility bands may remove local hollows before risk-scaled payoff is applied.",
        changed_variables="balanced volatility band, regularized inverse HGB, ATR score, hold8, density 7.5, lower risk cap.",
        risk_logic="ATR stop 1.86, ATR take-profit 4.20, model risk cap 2.15%, close_on_flat=false, same-side cooldown3.",
    ),
    CandidateSpec(
        package_id="cp302E_hgb10_late_us_atrscore_hold6_density75_convex_rr_surface",
        model_key="hgb_inverse_l2_0p10_unweighted",
        filter_id="late_us",
        score_mode="atr",
        target_density=7.5,
        max_hold_bars=6,
        score_quantile=0.20,
        close_on_flat_signal=False,
        same_direction_reentry_cooldown_bars=2,
        atr_sltp_enabled=True,
        atr_stop_multiplier=1.95,
        atr_take_profit_multiplier=4.40,
        model_risk_sizing_enabled=True,
        model_risk_max_pct=0.024,
        thesis="Stage301 late-session edge was small but positive; test it with convex exits instead of threshold repair.",
        changed_variables="late US filter, regularized inverse HGB, ATR score, hold6, density 7.5, ATR payoff asymmetry.",
        risk_logic="ATR stop 1.95, ATR take-profit 4.40, model risk cap 2.4%, close_on_flat=false, same-side cooldown2.",
    ),
    CandidateSpec(
        package_id="cp302F_hgb02_vol_convex_late_absscore_hold5_density55_rr_surface",
        model_key="hgb_inverse_l2_0p02_unweighted",
        filter_id="vol_convex_late",
        score_mode="abs",
        target_density=5.5,
        max_hold_bars=5,
        score_quantile=0.20,
        close_on_flat_signal=False,
        same_direction_reentry_cooldown_bars=2,
        atr_sltp_enabled=True,
        atr_stop_multiplier=2.10,
        atr_take_profit_multiplier=4.85,
        model_risk_sizing_enabled=True,
        model_risk_max_pct=0.023,
        thesis="Volatility-convex late-session selection may keep the upside while cutting quiet churn.",
        changed_variables="volatility-convex filter, unregularized inverse HGB, absolute score, hold5, density 5.5, ATR payoff asymmetry.",
        risk_logic="ATR stop 2.10, ATR take-profit 4.85, model risk cap 2.3%, close_on_flat=false, same-side cooldown2.",
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


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def safe_upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    try:
        upsert_csv_rows(path, columns, rows, key=key)
        return
    except OSError:
        existing = read_csv_dicts(path)
        new_keys = {str(row.get(key, "")) for row in rows}
        merged: list[dict[str, Any]] = [row for row in existing if str(row.get(key, "")) not in new_keys]
        merged.extend(dict(row) for row in rows)
        io_path(path.parent).mkdir(parents=True, exist_ok=True)
        with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
            writer.writeheader()
            for row in merged:
                writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def filter_mask(frame: pd.DataFrame, filter_id: str) -> np.ndarray:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    hours = timestamps.dt.hour.to_numpy()
    zabs = pd.to_numeric(frame.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
    atr = pd.to_numeric(frame.get("atr_14_over_atr_50", 1.0), errors="coerce").fillna(1.0).to_numpy()
    rsi = pd.to_numeric(frame.get("rsi_14", 50.0), errors="coerce").fillna(50.0).to_numpy()
    hv = pd.to_numeric(frame.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy()
    if filter_id == "quiet_revert":
        return (hours >= 16) & (hours <= 23) & (zabs <= 1.4) & (hv <= 1.4) & (atr >= 0.70)
    if filter_id == "cash_mid_late":
        return (hours >= 16) & (hours <= 23) & (zabs <= 2.5) & (atr >= 0.75)
    if filter_id == "balanced_band":
        return (hours >= 16) & (hours <= 23) & (zabs <= 2.0) & (atr >= 0.80) & (atr <= 1.45) & (hv <= 1.6)
    if filter_id == "late_us":
        return (hours >= 18) & (hours <= 23) & (zabs <= 2.7) & (atr >= 0.70)
    if filter_id == "vol_convex_late":
        return (hours >= 16) & (hours <= 23) & (zabs >= 0.25) & (zabs <= 2.2) & (atr >= 0.85) & (atr <= 1.7) & ((rsi <= 45) | (rsi >= 55))
    return np.ones(len(frame), dtype=bool)


def score_values(frame: pd.DataFrame, predicted: np.ndarray, score_mode: str) -> np.ndarray:
    score = np.abs(predicted).astype("float64")
    atr = pd.to_numeric(frame.get("atr_14_over_atr_50", 1.0), errors="coerce").fillna(1.0).to_numpy()
    zabs = pd.to_numeric(frame.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
    if score_mode == "atr":
        return score * atr
    if score_mode == "zatr":
        return score * (1.0 + zabs) * atr
    return score


def build_signal(spec: CandidateSpec, base: pd.DataFrame, predicted: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    raw_signal = np.sign(-predicted).astype("int8")
    score = score_values(base, predicted, spec.score_mode)
    mask = filter_mask(base, spec.filter_id)
    raw_signal[~mask] = 0
    score = score * mask.astype("float64")
    active = raw_signal != 0
    if active.any():
        threshold = float(np.quantile(score[active], spec.score_quantile))
        raw_signal[score < threshold] = 0
    signal = s294.trim_to_density(base, raw_signal, score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score.astype("float64")


def model_key_for_s301(spec: CandidateSpec) -> str:
    if spec.model_key == "hgb_inverse_l2_0p10_unweighted":
        return "hgb_inverse_l20p1_unweighted"
    return "hgb_inverse_l20p02_unweighted"


def model_spec_path(spec: CandidateSpec) -> Path:
    return MODEL_DIR / f"{spec.model_key}_model_spec.json"


def materialize_payload(
    spec: CandidateSpec,
    base: pd.DataFrame,
    predicted: np.ndarray,
    feature_cols: Sequence[str],
    medians: pd.Series,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = build_signal(spec, base, predicted)
    branch_id = f"run302A_{spec.package_id.replace('_surface', '')}"
    payload = base.copy()
    payload["stage302_branch_id"] = branch_id
    payload["stage301_branch_id"] = payload.get("stage301_branch_id", "")
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "payoff_convexity_profit_scale_surface"
    payload["candidate_decision_score"] = score
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
        "dataset_id": spec.dataset_id,
        "mode": "payoff_convexity_inverse_hgb",
        "model_key": spec.model_key,
        "filter_id": spec.filter_id,
        "score_mode": spec.score_mode,
        "target_density": spec.target_density,
        "score_quantile": spec.score_quantile,
        "max_hold_bars": spec.max_hold_bars,
        "risk_logic": spec.risk_logic,
        "model_feature_order_hash": ordered_hash(tuple(feature_cols)),
        "direction_feature_order_hash": ordered_hash(FEATURE_ORDER),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(FEATURE_ORDER)
    payload["model_feature_order_hash"] = ordered_hash(tuple(feature_cols))
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = s296.metrics_for_payload(spec, payload, "validation")
    oos_metrics = s296.metrics_for_payload(spec, payload, "oos")
    drop_columns = [column for column in payload.columns if column.startswith(("label", "future_")) or column in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    class SupplySpec:
        package_id = spec.package_id
        max_hold_bars = spec.max_hold_bars

    return s290.supply_rows_for_payload(payload, SupplySpec())  # type: ignore[arg-type]


def gate_label(validation_metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(validation_metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "scale":
        ok = float(validation_metrics["net_bp"]) >= 1500.0 and float(oos_metrics["net_bp"]) >= 750.0
    else:
        ok = (
            float(validation_metrics["pf"]) >= 1.07
            and float(oos_metrics["pf"]) >= 1.05
            and float(validation_metrics["worst_rolling_20_bp"]) >= -2600.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -1200.0
        )
    return "passed" if ok else "failed"


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    base = s301.load_base_payload()
    dataset, feature_cols, medians = s301.dataset_and_features()
    models, s301_receipts = s301.train_models(dataset, feature_cols, medians)
    x_all = base[list(feature_cols)].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(medians)
    predictions = {key: np.asarray(model.predict(x_all), dtype="float64") for key, model in models.items()}
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    model_receipts: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    seen_model_keys: set[str] = set()
    for spec in CANDIDATES:
        if spec.model_key in seen_model_keys:
            continue
        seen_model_keys.add(spec.model_key)
        source_key = model_key_for_s301(spec)
        source_receipt = next(row for row in s301_receipts if row["model_key"] == source_key)
        spec_payload = {
            "model_key": spec.model_key,
            "source_model_key": source_key,
            "model_family": source_receipt["model_family"],
            "feature_columns": list(feature_cols),
            "feature_medians": {key: float(value) for key, value in medians.items()},
            "target": source_receipt["target"],
            "training_policy": "Stage302 reuses Stage301 train-only HGB fit and changes payoff/risk surface.",
            "inversion_policy": "route signal is sign(-predicted_return), then filtered/scored for payoff convexity.",
            "claim_boundary": BOUNDARY,
        }
        write_json(MODEL_DIR / f"{spec.model_key}_model_spec.json", spec_payload)
        model_receipts.append(
            {
                "model_key": spec.model_key,
                "model_family": "HistGradientBoostingRegressor(히스토그램 그래디언트 부스팅 회귀)",
                "train_rows": source_receipt["train_rows"],
                "feature_count": len(feature_cols),
                "target": "future_log_return_12 train split only(학습 구간 전용)",
                "selection_policy": "Stage302 payoff convexity proxy screen; no candidate selected before MT5.",
                "inversion_policy": "sign(-predicted_return) with payoff-convex filtering",
                "feature_order_hash": ordered_hash(tuple(feature_cols)),
                "claim_boundary": BOUNDARY,
            }
        )
    for index, spec in enumerate(CANDIDATES, start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, base, predictions[model_key_for_s301(spec)], feature_cols, medians)
        branch_id = f"run302A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        spec_path = model_spec_path(spec)
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "package_id": spec.package_id,
                "materialized_branch_id": branch_id,
                "feature_order": list(FEATURE_ORDER),
                "feature_order_hash": ordered_hash(FEATURE_ORDER),
                "model_feature_order_hash": ordered_hash(tuple(feature_cols)),
                "decision_surface": identity,
                "risk_logic": spec.risk_logic,
                "runtime_handoff": "precomputed route_signal_value replay plus MT5 ATR/risk set values for Stage302 probe",
                "claim_boundary": BOUNDARY,
            },
        )
        density_gate = gate_label(validation_metrics, oos_metrics, "density")
        scale_gate = gate_label(validation_metrics, oos_metrics, "scale")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.60
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.thesis,
                "decision_use": "Test whether payoff convexity and risk/reward asymmetry can scale the Stage301 positive-small edge.",
                "comparison_baseline": "Stage301 actual MT5 positive-small no ONNX-worthy candidate",
                "control_variables": "US100 M5 split_v1; train-only HGB model family; Tier A/B paired runtime accounting; no Adapter or ONNX claim",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Train split fits HGB; validation/OOS proxy and MT5 are evaluation; Tier A primary plus Tier B fallback payloads",
                "success_criteria": "actual MT5 validation/OOS both profitable, 4-10 trades/day, enough net scale, PF/recovery/expectancy acceptable, no deep zoomed curve hollow",
                "failure_criteria": "profit scale absent, OOS weak, density outside 4-10, or local curve pocket remains deep",
                "invalid_conditions": "payload contains label/future columns, model feature order missing, source payload missing, or runtime handoff mismatch",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise review opens a fresh thesis or discard",
                "evidence_plan": "model receipt; proxy scoreboard; payload manifest; MT5 queue; run302B MT5 KPI; run302C curve review",
                "feature_surface": "raw model input features plus inverse HGB predicted return score and payoff-convex filters",
                "model_surface": spec.model_key,
                "decision_surface": "payoff_convexity_inverse_hgb",
                "risk_logic": spec.risk_logic,
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay plus set-value risk handoff",
                "failure_memory_plan": "Record whether signal filter, ATR SL/TP, risk sizing, or hold horizon caused failure.",
                "claim_boundary": BOUNDARY,
            }
        )
        payload_hash = sha256_file_lf_normalized(payload_path)
        handoff_hash = sha256_file_lf_normalized(handoff_path)
        model_hash = sha256_file_lf_normalized(spec_path)
        manifest_rows.append(
            {
                "queue_id": f"run302A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage302_branch_id": branch_id,
                "stage301_branch_id": spec.package_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "payoff_convexity_profit_scale_surface",
                "payload_path": rel(payload_path),
                "payload_hash": payload_hash,
                "handoff_path": rel(handoff_path),
                "handoff_hash": handoff_hash,
                "model_artifact_path": rel(spec_path),
                "model_artifact_hash": model_hash,
                "model_feature_order_path": rel(spec_path),
                "model_feature_order_hash": ordered_hash(tuple(feature_cols)),
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(FEATURE_ORDER),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": int(spec.close_on_flat_signal),
                "same_direction_reentry_cooldown_bars": spec.same_direction_reentry_cooldown_bars,
                "atr_sltp_enabled": int(spec.atr_sltp_enabled),
                "atr_period": spec.atr_period,
                "atr_stop_multiplier": spec.atr_stop_multiplier,
                "atr_take_profit_multiplier": spec.atr_take_profit_multiplier,
                "atr_min_stop_points": spec.atr_min_stop_points,
                "atr_max_stop_points": spec.atr_max_stop_points,
                "atr_min_take_profit_points": spec.atr_min_take_profit_points,
                "atr_max_take_profit_points": spec.atr_max_take_profit_points,
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
                "approx_validation_trades_per_day": validation_metrics["trades_per_day"],
                "approx_oos_trades_per_day": oos_metrics["trades_per_day"],
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
                "model_family": "HistGradientBoostingRegressor_payoff_convexity_inverse",
                "prediction_kind": "precomputed_direction_replay",
                "dataset_id": spec.dataset_id,
                "model_artifact_path": rel(spec_path),
                "model_artifact_hash": model_hash,
                "model_feature_order_path": rel(spec_path),
                "model_feature_order_hash": ordered_hash(tuple(feature_cols)),
                "imputation_path": rel(spec_path),
                "imputation_hash": model_hash,
                "classes": "-1,0,1",
                "payoff_weight_policy": "sign(-predicted_future_return)_x_payoff_convex_filter",
                "onnx_exportability_note": "Adapter required before ONNX(온엑스); current output is precomputed route_signal_value with model spec receipt.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": "HistGradientBoostingRegressor_payoff_convexity_inverse",
                "prediction_kind": "direction_replay",
                "mode": "payoff_convexity_inverse_hgb",
                "quantile": spec.score_quantile,
                "threshold": "",
                "precondition": f"{spec.filter_id}_{spec.score_mode}",
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
                "proxy_edge_gate": scale_gate,
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
                    "mode": "payoff_convexity_inverse_hgb",
                    "quantile": spec.score_quantile,
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
        supply_rows.extend(supply_rows_for_payload(payload, spec))
        artifacts.extend([payload_path, handoff_path, spec_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, model_receipts, artifacts


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    scale_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    result = [
        {
            "result_subject": "Stage302 payoff convexity materialization(302단계 보상 볼록성 물질화)",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};scale_proxy_pass={scale_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI(MT5 런타임 핵심 성과 지표), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
            "judgment_label": "exploratory(탐색)",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage302(302단계)는 Stage301(301단계)의 작은 양수 edge(우위)를 ATR/risk(ATR/위험) 보상 구조로 키우려는 새 논제다.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Stage301(301단계)의 threshold repair(임계값 수정)가 아니라 payoff/risk surface(보상/위험 표면)를 새로 만들었다."},
        {"gate_name": "train_only_model_boundary(학습 전용 모델 경계)", "status": "passed", "evidence_path": rel(MODEL_RECEIPT), "effect": "HGB(히스토그램 그래디언트 부스팅) 모델은 train split(학습 구간)만 사용했다."},
        {"gate_name": "proxy_density_scale_screen(대리 밀도/규모 선별)", "status": "passed" if density_pass and scale_pass else "partial", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "MT5(메타트레이더5) 전에 4-10 trades/day(일 4-10거래)와 수익 규모 방향을 확인했다."},
        {"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "prepared", "evidence_path": rel(MT5_QUEUE), "effect": "run302B(302B 실행) 실제 tester output(테스터 출력) 대기열을 만들었다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "후보 관문 전이라 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(ONNX 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전 단계라 ONNX(온엑스)를 시작하지 않는다."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run302A Payoff Convexity Profit Scale Materialization(302A 보상 볼록성 수익 규모 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage301(301단계)의 작은 양수 edge(우위)를 보상/위험 비대칭으로 키울 후보 6개를 만들었다.",
        "",
        "| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.1f} | {vtd:.2f} | {on:.1f} | {otd:.2f} | {den} | {scale} | {curve} |".format(
                pkg=row["package_id"],
                vn=float(row["validation_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                on=float(row["oos_proxy_net_bp"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                den=row["density_gate"],
                scale=row["proxy_edge_gate"],
                curve=row["curve_proxy_gate"],
            )
        )
    lines.extend(["", f"MT5 queue(MT5 대기열): `{len(manifest_rows)}` rows(행)", f"Claim boundary(주장 경계): `{BOUNDARY}`"])
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
    artifacts = [
        BRANCH_QUEUE,
        MODEL_SCOREBOARD,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        MODEL_MANIFEST,
        WFO_FOLD_SCOREBOARD,
        MODEL_RECEIPT,
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
                "stage301_review": rel(SOURCE_REVIEW),
                "stage301_scoreboard": rel(SOURCE_SCOREBOARD),
                "stage302_seed_queue": rel(SOURCE_SEED_QUEUE),
                "dataset_id": DATASET_ID,
            },
            "outputs": {
                "model_receipt": rel(MODEL_RECEIPT),
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
    safe_upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "payoff_convexity_profit_scale_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
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
                "record_view": "payoff_convexity_profit_scale_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "payoff_convexity_profit_scale",
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
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "payoff_convexity_profit_scale_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage302_payoff_convexity_profit_scale_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run302A payoff convexity profit scale materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    safe_upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run302A_report", f"- run302A_report(302A 보고): `{rel(REPORT)}`\n- run302A_mt5_queue(302A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)
    review_index = read_text(REVIEW_INDEX) or "# Stage302 Review Index(302단계 검토 색인)\n"
    review_index = append_once(review_index, "run302A_report", f"- run302A_report(302A 보고): `{rel(REPORT)}`\n- run302A_mt5_queue(302A MT5 대기열): `{rel(MT5_QUEUE)}`\n- run302A_model_receipt(302A 모델 영수증): `{rel(MODEL_RECEIPT)}`")
    write_md(REVIEW_INDEX, review_index)
    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run302A_summary", f"- run302A_summary(302A 요약): payoff convexity(보상 볼록성) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): ATR SL/TP(ATR 손절/익절)와 model risk sizing(모델 위험 크기)을 MT5 queue(MT5 대기열)로 넘겼고 selected_candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.")
    write_md(CURRENT_STATE, current)
    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage302(302단계) run302A(302A 실행) payoff convexity profit scale materialization(보상 볼록성 수익 규모 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = s293.prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run302A Payoff convexity profit scale materialization(302A 보상 볼록성 수익 규모 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 아직 없다.\n",
    )
    write_md(CHANGELOG, changelog)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, model_receipts, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, model_receipts, payload_artifacts, created_at)
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
