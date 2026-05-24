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
from sklearn.ensemble import HistGradientBoostingRegressor


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


STAGE_ID = "301_onnx_candidate_campaign__orthogonal_profit_source_rebuild"
RUN_ID = "run301A_design_orthogonal_profit_source_rebuild_v1"
RUN_NUMBER = "run301A"
SOURCE_STAGE_ID = "300_onnx_candidate_campaign__split_forward_trade_shape_generalization_rebuild"
SOURCE_RUN_ID = "run300C_review_split_forward_trade_shape_generalization_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
NEXT_ACTION = "run301B_execute_orthogonal_profit_source_mt5_probe"
STATUS = "completed_orthogonal_profit_source_candidates_materialized_no_selection"
JUDGMENT = "orthogonal_profit_source_inputs_materialized_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"
FEATURE_ORDER = ("route_signal_value",)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run300C_split_forward_trade_shape_generalization_review_stage301_open_report.md"
SOURCE_SCOREBOARD = SOURCE_STAGE / "02_runs" / "run300C" / "split_forward_trade_shape_generalization_review_scoreboard.csv"
SOURCE_PAYLOAD_MANIFEST = SOURCE_STAGE / "02_runs" / "run300A" / "candidate_payload_manifest.csv"

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
MODEL_RECEIPT = RUN_ROOT / "orthogonal_profit_source_model_receipt.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run301A_orthogonal_profit_source_materialization_report.md"

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

MODEL_RECEIPT_COLUMNS = (
    "model_key",
    "model_family",
    "train_rows",
    "feature_count",
    "target",
    "selection_policy",
    "inversion_policy",
    "feature_order_hash",
    "claim_boundary",
)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    mode: str
    target_density: float
    max_hold_bars: int
    score_quantile: float
    filter_id: str
    l2_regularization: float
    weighted: bool
    thesis: str
    changed_variables: str
    risk_logic: str
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    dataset_id: str = DATASET_ID


CANDIDATES: tuple[CandidateSpec, ...] = (
    CandidateSpec(
        package_id="cp301A_hgb_inverse_tail_density45_hold2_surface",
        mode="hgb_inverse_mean_reversion",
        target_density=4.5,
        max_hold_bars=2,
        score_quantile=0.28,
        filter_id="none",
        l2_regularization=0.02,
        weighted=False,
        thesis="Train-only HGB shows the strongest proxy edge when the predicted forward return is inverted, suggesting a mean-reversion profit source rather than Stage300 shape repair.",
        changed_variables="unweighted HGB inverse signal, hold2, density 4.5, no Stage300 threshold repair.",
        risk_logic="max_hold_bars=2;close_on_flat_signal=true;inverse_mean_reversion_tail=true",
    ),
    CandidateSpec(
        package_id="cp301B_hgb_inverse_efficiency_density55_hold3_surface",
        mode="hgb_inverse_mean_reversion",
        target_density=5.5,
        max_hold_bars=3,
        score_quantile=0.30,
        filter_id="none",
        l2_regularization=0.02,
        weighted=False,
        thesis="Keep the inverse HGB source at a moderate density to test efficiency before scale is pushed.",
        changed_variables="unweighted HGB inverse signal, hold3, density 5.5, moderate score cut.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;inverse_mean_reversion_efficiency=true",
    ),
    CandidateSpec(
        package_id="cp301C_hgb_inverse_balance_density70_hold4_surface",
        mode="hgb_inverse_mean_reversion",
        target_density=7.0,
        max_hold_bars=4,
        score_quantile=0.25,
        filter_id="none",
        l2_regularization=0.02,
        weighted=False,
        thesis="Balanced branch: keep enough daily trades while testing whether inverse HGB survives OOS without a local hollow.",
        changed_variables="unweighted HGB inverse signal, hold4, density 7.0.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;inverse_mean_reversion_balanced=true",
    ),
    CandidateSpec(
        package_id="cp301D_hgb_inverse_scale_density85_hold4_surface",
        mode="hgb_inverse_mean_reversion",
        target_density=8.5,
        max_hold_bars=4,
        score_quantile=0.22,
        filter_id="none",
        l2_regularization=0.02,
        weighted=False,
        thesis="Aggressive scale branch: push the inverse HGB source near the top of the 4-10 trades/day window.",
        changed_variables="unweighted HGB inverse signal, hold4, density 8.5.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;inverse_mean_reversion_scale=true",
    ),
    CandidateSpec(
        package_id="cp301E_hgb_inverse_late_us_density70_hold4_surface",
        mode="hgb_inverse_mean_reversion",
        target_density=7.0,
        max_hold_bars=4,
        score_quantile=0.24,
        filter_id="late_us",
        l2_regularization=0.02,
        weighted=False,
        thesis="Session branch: isolate late US hours where inverse HGB has a different payoff shape from the Stage300 trade-shape failure.",
        changed_variables="late-US filter, unweighted HGB inverse signal, hold4, density 7.0.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;late_us_inverse_source=true",
    ),
    CandidateSpec(
        package_id="cp301F_hgb_inverse_regularized_density85_hold4_surface",
        mode="hgb_inverse_regularized",
        target_density=8.5,
        max_hold_bars=4,
        score_quantile=0.22,
        filter_id="none",
        l2_regularization=0.10,
        weighted=False,
        thesis="Regularized control: use a smoother inverse HGB model to test whether profit scale survives lower model variance.",
        changed_variables="unweighted HGB inverse signal, l2 0.10, hold4, density 8.5.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;regularized_inverse_mean_reversion=true",
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
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
            writer.writeheader()
            for row in merged:
                writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def load_base_payload() -> pd.DataFrame:
    rows = read_csv_dicts(SOURCE_PAYLOAD_MANIFEST)
    if not rows:
        raise FileNotFoundError(f"missing source payload manifest: {SOURCE_PAYLOAD_MANIFEST}")
    frame = pd.read_parquet(io_path(ROOT / rows[0]["payload_path"])).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return frame.sort_values(["tier_scope", "split", "timestamp"]).reset_index(drop=True)


def dataset_and_features() -> tuple[pd.DataFrame, list[str], pd.Series]:
    dataset = s290.load_dataset(DATASET_ID).copy()
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    exclude = {
        "timestamp",
        "symbol",
        "future_timestamp",
        "future_log_return_12",
        "label",
        "label_class",
        "label_id",
        "split",
        "split_id",
        "horizon_bars",
        "horizon_minutes",
    }
    feature_cols = [column for column in dataset.columns if column not in exclude and pd.api.types.is_numeric_dtype(dataset[column])]
    for column in feature_cols:
        dataset[column] = pd.to_numeric(dataset[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
    medians = dataset.loc[dataset["split"].eq("train"), feature_cols].median(numeric_only=True)
    return dataset, feature_cols, medians


def model_key(spec: CandidateSpec) -> str:
    weight_token = "weighted" if spec.weighted else "unweighted"
    return f"hgb_inverse_l2{str(spec.l2_regularization).replace('.', 'p')}_{weight_token}"


def train_models(dataset: pd.DataFrame, feature_cols: Sequence[str], medians: pd.Series) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    train = dataset.loc[dataset["split"].eq("train")].copy()
    x_train = train[list(feature_cols)].fillna(medians)
    y_train = train["future_log_return_12"].astype(float)
    scale = float(np.nanmedian(np.abs(y_train))) or 1.0
    weights = np.clip(np.abs(y_train) / scale, 0.25, 8.0)
    models: dict[str, Any] = {}
    receipt_rows: list[dict[str, Any]] = []
    for spec in CANDIDATES:
        key = model_key(spec)
        if key in models:
            continue
        model = HistGradientBoostingRegressor(
            max_iter=240,
            learning_rate=0.045,
            max_leaf_nodes=31,
            l2_regularization=spec.l2_regularization,
            random_state=303,
        )
        if spec.weighted:
            model.fit(x_train, y_train, sample_weight=weights)
        else:
            model.fit(x_train, y_train)
        models[key] = model
        receipt_rows.append(
            {
                "model_key": key,
                "model_family": "HistGradientBoostingRegressor(히스토그램 그래디언트 부스팅 회귀)",
                "train_rows": len(train),
                "feature_count": len(feature_cols),
                "target": "future_log_return_12 train split only(학습 구간만)",
                "selection_policy": "fixed Stage301 candidate specs; proxy metrics are evidence, not selection",
                "inversion_policy": "route signal is sign(-predicted_return), interpreted as mean-reversion source",
                "feature_order_hash": ordered_hash(tuple(feature_cols)),
                "claim_boundary": BOUNDARY,
            }
        )
    return models, receipt_rows


def filter_mask(frame: pd.DataFrame, filter_id: str) -> np.ndarray:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    hours = timestamps.dt.hour.to_numpy()
    zabs = pd.to_numeric(frame.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
    atr = pd.to_numeric(frame.get("atr_14_over_atr_50", 1.0), errors="coerce").fillna(1.0).to_numpy()
    minutes = pd.to_numeric(frame.get("minutes_from_cash_open", 0.0), errors="coerce").fillna(0.0).to_numpy()
    if filter_id == "late_us":
        return (hours >= 18) & (hours <= 23) & (zabs <= 2.7) & (atr >= 0.70)
    return np.ones(len(frame), dtype=bool)


def build_signal(spec: CandidateSpec, base: pd.DataFrame, model: Any, feature_cols: Sequence[str], medians: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    x_all = base[list(feature_cols)].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(medians)
    predicted = np.asarray(model.predict(x_all), dtype="float64")
    raw_signal = np.sign(-predicted).astype("int8")
    score = np.abs(predicted).astype("float64")
    mask = filter_mask(base, spec.filter_id)
    raw_signal[~mask] = 0
    score = score * mask.astype("float64")
    active = raw_signal != 0
    if active.any():
        threshold = float(np.quantile(score[active], spec.score_quantile))
        raw_signal[score < threshold] = 0
    signal = s294.trim_to_density(base, raw_signal, score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score.astype("float64")


def gate_label(validation_metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(validation_metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "scale":
        ok = float(validation_metrics["net_bp"]) >= 2200.0 and float(oos_metrics["net_bp"]) >= 300.0
    else:
        ok = (
            float(validation_metrics["pf"]) >= 1.12
            and float(oos_metrics["pf"]) >= 1.00
            and float(validation_metrics["worst_rolling_20_bp"]) >= -2600.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -1200.0
        )
    return "passed" if ok else "failed"


def materialize_payload(
    spec: CandidateSpec,
    base: pd.DataFrame,
    model: Any,
    feature_cols: Sequence[str],
    medians: pd.Series,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = build_signal(spec, base, model, feature_cols, medians)
    branch_id = f"run301A_{spec.package_id.replace('_surface', '')}"
    payload = base.copy()
    payload["stage301_branch_id"] = branch_id
    payload["stage300_branch_id"] = payload.get("stage300_branch_id", "")
    payload["stage299_branch_id"] = payload.get("stage299_branch_id", "")
    payload["stage298_branch_id"] = payload.get("stage298_branch_id", "")
    payload["stage297_branch_id"] = payload.get("stage297_branch_id", "")
    payload["stage296_branch_id"] = payload.get("stage296_branch_id", "")
    payload["stage295_branch_id"] = payload.get("stage295_branch_id", "")
    payload["stage294_branch_id"] = payload.get("stage294_branch_id", "")
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "orthogonal_profit_source_surface"
    payload["candidate_decision_score"] = score
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
        "dataset_id": spec.dataset_id,
        "mode": spec.mode,
        "model_key": model_key(spec),
        "filter_id": spec.filter_id,
        "target_density": spec.target_density,
        "score_quantile": spec.score_quantile,
        "max_hold_bars": spec.max_hold_bars,
        "source": "train_only_inverse_hgb_mean_reversion_profit_source",
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


def model_spec_path(spec: CandidateSpec) -> Path:
    return MODEL_DIR / f"{model_key(spec)}_model_spec.json"


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    base = load_base_payload()
    dataset, feature_cols, medians = dataset_and_features()
    models, model_receipts = train_models(dataset, feature_cols, medians)
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    for receipt in model_receipts:
        spec_payload = {
            "model_key": receipt["model_key"],
            "model_family": receipt["model_family"],
            "feature_columns": list(feature_cols),
            "feature_medians": {key: float(value) for key, value in medians.items()},
            "target": receipt["target"],
            "training_policy": receipt["selection_policy"],
            "inversion_policy": receipt["inversion_policy"],
            "claim_boundary": BOUNDARY,
        }
        write_json(MODEL_DIR / f"{receipt['model_key']}_model_spec.json", spec_payload)
    for index, spec in enumerate(CANDIDATES, start=1):
        model = models[model_key(spec)]
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, base, model, feature_cols, medians)
        branch_id = f"run301A_{spec.package_id.replace('_surface', '')}"
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
                "runtime_handoff": "precomputed route_signal_value replay for Stage301 MT5 probe",
                "claim_boundary": BOUNDARY,
            },
        )
        density_gate = gate_label(validation_metrics, oos_metrics, "density")
        scale_gate = gate_label(validation_metrics, oos_metrics, "scale")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.30
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.thesis,
                "decision_use": "Check whether an orthogonal inverse-HGB mean-reversion source is worth MT5 runtime probing.",
                "comparison_baseline": "Stage300 split-forward trade-shape actual MT5 negative review",
                "control_variables": "US100 M5 split_v1; train-only model fit; Tier A/B paired runtime accounting; no Adapter or ONNX claim",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Train split fits HGB; validation/OOS proxy and MT5 are evaluation; Tier A primary plus Tier B fallback payloads",
                "success_criteria": "validation/OOS both positive, 4-10 trades/day, enough net scale, PF/recovery/expectancy acceptable, no deep zoomed curve hollow",
                "failure_criteria": "MT5 net scale absent, OOS negative, density outside 4-10, or local curve pocket remains deep",
                "invalid_conditions": "payload contains label/future columns, model feature order missing, source payload missing, or runtime handoff mismatch",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise review opens a fresh thesis or discard",
                "evidence_plan": "model receipt; model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run301B MT5 KPI; run301C curve review",
                "feature_surface": "raw model input features plus inverse HGB predicted return score",
                "model_surface": model_key(spec),
                "decision_surface": spec.mode,
                "risk_logic": spec.risk_logic,
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; model spec retained for Adapter trace if candidate gate passes",
                "failure_memory_plan": "If runtime fails, record whether inverse source, session filter, density, or hold horizon caused failure.",
                "claim_boundary": BOUNDARY,
            }
        )
        payload_hash = sha256_file_lf_normalized(payload_path)
        handoff_hash = sha256_file_lf_normalized(handoff_path)
        model_hash = sha256_file_lf_normalized(spec_path)
        manifest_rows.append(
            {
                "queue_id": f"run301A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "orthogonal_profit_source_surface",
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
                "model_family": "HistGradientBoostingRegressor_inverse_mean_reversion",
                "prediction_kind": "precomputed_direction_replay",
                "dataset_id": spec.dataset_id,
                "model_artifact_path": rel(spec_path),
                "model_artifact_hash": model_hash,
                "model_feature_order_path": rel(spec_path),
                "model_feature_order_hash": ordered_hash(tuple(feature_cols)),
                "imputation_path": rel(spec_path),
                "imputation_hash": model_hash,
                "classes": "-1,0,1",
                "payoff_weight_policy": "sign(-predicted_future_return)",
                "onnx_exportability_note": "Adapter required before ONNX(온엑스); current output is precomputed route_signal_value with model spec receipt.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": "HistGradientBoostingRegressor_inverse_mean_reversion",
                "prediction_kind": "direction_replay",
                "mode": spec.mode,
                "quantile": spec.score_quantile,
                "threshold": "",
                "precondition": "train_only_inverse_hgb_mean_reversion_source",
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
                    "mode": spec.mode,
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
            "result_subject": "Stage301 orthogonal profit source materialization(301단계 직교 수익 원천 물질화)",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};scale_proxy_pass={scale_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI(MT5 런타임 핵심 성과 지표), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
            "judgment_label": "exploratory(탐색)",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage301(301단계)은 Stage300(300단계)의 거래 형태 수정을 버리고 train-only inverse HGB(학습 전용 역방향 HGB) 수익 원천을 만들었다.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Stage300(300단계)의 shape repair(형태 수정)를 반복하지 않고 새 수익 원천을 만들었다."},
        {"gate_name": "train_only_model_boundary(학습 전용 모델 경계)", "status": "passed", "evidence_path": rel(MODEL_RECEIPT), "effect": "모델은 train split(학습 구간)만으로 fit(적합)했다."},
        {"gate_name": "proxy_density_scale_screen(대리 밀도/규모 선별)", "status": "passed" if density_pass and scale_pass else "partial", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day(일 4-10거래)와 수익 규모 방향을 MT5(메타트레이더5) 전에 확인했다."},
        {"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "prepared", "evidence_path": rel(MT5_QUEUE), "effect": "run301B(301B 실행)에서 실제 tester output(테스터 출력)을 확인할 대기열을 만들었다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "후보 gate(관문) 전에는 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전 단계이므로 ONNX(온엑스)를 시작하지 않는다."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run301A Orthogonal Profit Source Materialization(301A 직교 수익 원천 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): train-only HGB(학습 전용 히스토그램 그래디언트 부스팅)의 predicted return(예측 수익률)을 반대로 써서 mean-reversion(평균회귀) 수익 원천 후보 6개를 만들었다.",
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
    write_csv_rows(PAYLOAD_MANIFEST, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MT5_QUEUE, s293.MANIFEST_COLUMNS, manifest_rows)
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
                "stage300_review": rel(SOURCE_REVIEW),
                "stage300_scoreboard": rel(SOURCE_SCOREBOARD),
                "source_payload_manifest": rel(SOURCE_PAYLOAD_MANIFEST),
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
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "orthogonal_profit_source_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "orthogonal_profit_source_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "orthogonal_profit_source",
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
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "orthogonal_profit_source_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage301_orthogonal_profit_source_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run301A orthogonal profit source materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    safe_upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_md(
        SELECTED,
        f"""# Stage301 Selection Status(301단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- target_candidate(목표 후보): `none`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- run301A_report(301A 보고): `{rel(REPORT)}`
- run301A_mt5_queue(301A MT5 대기열): `{rel(MT5_QUEUE)}`
""",
    )
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage301 Review Index(301단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run301A_report",
        f"- run301A_report(301A 보고): `{rel(REPORT)}`\n- run301A_mt5_queue(301A MT5 대기열): `{rel(MT5_QUEUE)}`\n- run301A_model_receipt(301A 모델 영수증): `{rel(MODEL_RECEIPT)}`",
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
        "run301A_summary",
        f"- run301A_summary(301A 요약): orthogonal profit source(직교 수익 원천) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected_candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage301(301단계) run301A(301A 실행) orthogonal profit source materialization(직교 수익 원천 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = s293.prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run301A Orthogonal profit source materialization(301A 직교 수익 원천 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 아직 없다.\n",
    )
    write_md(CHANGELOG, changelog)


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
