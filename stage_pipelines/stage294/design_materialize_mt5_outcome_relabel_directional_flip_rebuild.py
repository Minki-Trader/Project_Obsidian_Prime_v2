from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

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


STAGE_ID = "294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild"
RUN_ID = "run294A_design_mt5_outcome_relabel_directional_flip_rebuild_v1"
RUN_NUMBER = "run294A"
SOURCE_RUN_ID = "run293C_review_profit_scale_density_calibration_mt5_probe_v1"
STATUS = "completed_mt5_outcome_relabel_directional_flip_candidates_materialized_no_selection"
JUDGMENT = "mt5_outcome_relabel_directional_flip_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run294B_execute_mt5_outcome_relabel_directional_flip_mt5_probe"
UPDATED_ON = "2026-05-24"
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

STAGE293 = ROOT / "stages" / "293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild"
STAGE294_SEED_QUEUE = STAGE_ROOT / "01_inputs" / "stage294_seed_queue.csv"
SOURCE_MANIFEST = STAGE293 / "02_runs" / "run293A" / "candidate_payload_manifest.csv"
SOURCE_MODEL_MANIFEST = STAGE293 / "02_runs" / "run293A" / "model_artifact_manifest.csv"
SOURCE_SCOREBOARD = STAGE293 / "02_runs" / "run293C" / "profit_scale_density_calibration_review_scoreboard.csv"
SOURCE_FAILURE = STAGE293 / "02_runs" / "run293C" / "failure_memory.csv"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
REPORT = REVIEWS / "run294A_mt5_outcome_relabel_directional_flip_materialization_report.md"

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
    dataset_id: str
    max_hold_bars: int
    transform_id: str
    target_density: float
    hypothesis: str
    changed_variables: str
    risk_logic: str


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


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    upsert_csv_rows(path, columns, rows, key=key)


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
            package_id="cp294A_cp293F_full_outcome_flip_hold5_surface",
            source_materialized_id="run293A_cp293F_asymmetric_tail_control_xgb_hold5",
            source_package_id="cp293F_asymmetric_tail_control_xgb_hold5_surface",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            transform_id="full_flip",
            target_density=6.8,
            hypothesis="Full outcome flip(전체 결과 반전)이 cp293F(293F 후보)의 근본전 음수 기대값을 양수 방향으로 바꿀 수 있다.",
            changed_variables="route_signal_value multiplied by -1; hold5 and close-on-flat retained(경로 신호 -1배, 5봉 보유와 관망 청산 유지)",
            risk_logic="max_hold_bars=5;close_on_flat_signal=true;same_direction_reentry_cooldown_bars=0",
        ),
        CandidateSpec(
            package_id="cp294B_cp293F_cost_aware_flip_skip_hold5_surface",
            source_materialized_id="run293A_cp293F_asymmetric_tail_control_xgb_hold5",
            source_package_id="cp293F_asymmetric_tail_control_xgb_hold5_surface",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            transform_id="cost_aware_flip_skip",
            target_density=5.8,
            hypothesis="Cost-aware flip/skip(비용 인식 반전/회피)가 cp293F(293F 후보)의 손실 구간을 줄이면서 일 4-10거래를 유지할 수 있다.",
            changed_variables="flip source signal, then veto high-volatility/non-cash weak cost states(원천 신호 반전 뒤 고변동/비현금장 비용 약점 거부)",
            risk_logic="max_hold_bars=5;close_on_flat_signal=true;cost_proxy_veto=true",
        ),
        CandidateSpec(
            package_id="cp294C_cp293A_density_trimmed_flip_hold5_surface",
            source_materialized_id="run293A_cp293A_runtime_calibrated_histgb_hold5",
            source_package_id="cp293A_runtime_calibrated_histgb_hold5_surface",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            transform_id="density_trimmed_flip",
            target_density=9.2,
            hypothesis="Density-trimmed flip(밀도 절단 반전)이 cp293A(293A 후보)의 과밀 OOS(표본외) 구간을 10거래/일 아래로 누르면서 손실 방향을 되돌릴 수 있다.",
            changed_variables="flip source signal and trim by source decision score to target density(원천 신호 반전 및 원천 판단 점수로 밀도 절단)",
            risk_logic="max_hold_bars=5;close_on_flat_signal=true;density_target=9.2",
        ),
        CandidateSpec(
            package_id="cp294D_cp293A_smooth_curve_flip_router_hold5_surface",
            source_materialized_id="run293A_cp293A_runtime_calibrated_histgb_hold5",
            source_package_id="cp293A_runtime_calibrated_histgb_hold5_surface",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            transform_id="smooth_curve_flip_router",
            target_density=6.2,
            hypothesis="Smooth curve flip router(곡선 완화 반전 라우터)가 cp293A(293A 후보)의 깊은 local pocket(국소 포켓)을 줄일 수 있다.",
            changed_variables="flip source signal only in smoother session/volatility states(더 부드러운 세션/변동성 상태에서만 원천 신호 반전)",
            risk_logic="max_hold_bars=5;close_on_flat_signal=true;smooth_state_veto=true",
        ),
        CandidateSpec(
            package_id="cp294E_cp293F_near_breakeven_flip_smoother_hold5_surface",
            source_materialized_id="run293A_cp293F_asymmetric_tail_control_xgb_hold5",
            source_package_id="cp293F_asymmetric_tail_control_xgb_hold5_surface",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            transform_id="near_breakeven_flip_smoother",
            target_density=6.0,
            hypothesis="Near-breakeven flip smoother(근본전 반전 완화)가 cp293F(293F 후보)의 작은 손실을 매끄러운 양수 곡선으로 바꿀 수 있다.",
            changed_variables="flip source signal, reduce exposure in extreme z-score and late-pocket proxy states(원천 신호 반전, 극단 z점수와 후반 포켓 대리 상태 노출 축소)",
            risk_logic="max_hold_bars=5;close_on_flat_signal=true;local_pocket_proxy_veto=true",
        ),
        CandidateSpec(
            package_id="cp294F_aggressive_cp293A_cp293F_union_flip_hold5_surface",
            source_materialized_id="run293A_cp293A_runtime_calibrated_histgb_hold5",
            source_package_id="cp293A_runtime_calibrated_histgb_hold5_surface",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            transform_id="aggressive_union_flip",
            target_density=9.8,
            hypothesis="Aggressive union flip(공격형 결합 반전)이 cp293A/cp293F(293A/293F 후보)의 음수 방향을 결합해 순수익 규모를 키울 수 있다.",
            changed_variables="union cp293A and cp293F flipped signals, then trim to <=10 trades/day(293A/293F 반전 신호 결합 후 일 10거래 이하 절단)",
            risk_logic="max_hold_bars=5;close_on_flat_signal=true;density_target=9.8;union_flip=true",
        ),
    ]


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def model_manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_MODEL_MANIFEST)}


def load_source_payload(materialized_id: str) -> pd.DataFrame:
    manifest = manifest_by_id()
    if materialized_id not in manifest:
        raise KeyError(f"Missing source materialized id: {materialized_id}")
    path = ROOT / manifest[materialized_id]["payload_path"]
    frame = pd.read_parquet(io_path(path)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["route_signal_value"] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    return frame.sort_values(["tier_scope", "timestamp"]).reset_index(drop=True)


def source_score(frame: pd.DataFrame) -> pd.Series:
    if "candidate_decision_score" in frame.columns:
        return pd.to_numeric(frame["candidate_decision_score"], errors="coerce").fillna(0.0).abs()
    return pd.Series(1.0, index=frame.index, dtype="float64")


def feature_masks(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    hour = timestamps.dt.hour.to_numpy()
    zabs = pd.to_numeric(frame.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
    vol = pd.to_numeric(frame.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy()
    cash = pd.to_numeric(frame.get("is_us_cash_open", 0.0), errors="coerce").fillna(0.0).to_numpy() > 0.5
    minutes = pd.to_numeric(frame.get("minutes_from_cash_open", 0.0), errors="coerce").fillna(0.0).to_numpy()
    return {
        "cost_ok": ((cash & (minutes >= 20) & (minutes <= 390)) | ((hour >= 14) & (hour <= 20))) & (vol <= 1.75) & (zabs <= 1.95),
        "smooth_ok": (hour >= 8) & (hour <= 21) & (vol <= 1.65) & (zabs <= 1.70),
        "near_ok": (vol <= 1.85) & (zabs >= 0.20) & (zabs <= 1.95) & ~((hour >= 21) & (zabs > 1.30)),
        "aggressive_ok": (vol <= 2.05) & (zabs <= 2.20) & (hour >= 7) & (hour <= 22),
    }


def route_label(values: Sequence[int]) -> list[str]:
    return [s290.signal_label(int(value)) for value in values]


def trim_to_density(frame: pd.DataFrame, signal: np.ndarray, score: np.ndarray, hold_bars: int, target_density: float) -> np.ndarray:
    out = signal.astype("int8").copy()
    for (_tier, split), index in frame.groupby(["tier_scope", "split"], sort=False).groups.items():
        idx = np.asarray(list(index), dtype=int)
        if split not in {"validation", "oos"}:
            continue
        days = pd.to_datetime(frame.iloc[idx]["timestamp"], utc=True).dt.date.nunique()
        if not days:
            continue
        current_tpd = s290.approximate_trades(out[idx], hold_bars) / float(days)
        if current_tpd <= target_density:
            continue
        active_scores = score[idx][out[idx] != 0]
        if len(active_scores) == 0:
            continue
        best = out[idx].copy()
        best_gap = abs(current_tpd - target_density)
        for quantile in np.linspace(0.02, 0.88, 60):
            threshold = float(np.quantile(active_scores, quantile))
            trial = out[idx].copy()
            trial[score[idx] < threshold] = 0
            tpd = s290.approximate_trades(trial, hold_bars) / float(days)
            if 4.0 <= tpd <= target_density + 0.15:
                gap = abs(tpd - target_density)
                if gap < best_gap:
                    best = trial
                    best_gap = gap
            elif tpd < 4.0:
                break
        out[idx] = best
    return out.astype("int8")


def transform_signal(spec: CandidateSpec, source: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    raw = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    score = source_score(source).to_numpy(dtype="float64")
    masks = feature_masks(source)
    signal = (-raw).astype("int8")
    if spec.transform_id == "full_flip":
        return signal, score
    if spec.transform_id == "cost_aware_flip_skip":
        signal = np.where(masks["cost_ok"], signal, 0).astype("int8")
        signal = trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
        return signal, score * masks["cost_ok"].astype("float64")
    if spec.transform_id == "density_trimmed_flip":
        signal = trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
        return signal, score
    if spec.transform_id == "smooth_curve_flip_router":
        signal = np.where(masks["smooth_ok"], signal, 0).astype("int8")
        signal = trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
        return signal, score * masks["smooth_ok"].astype("float64")
    if spec.transform_id == "near_breakeven_flip_smoother":
        signal = np.where(masks["near_ok"], signal, 0).astype("int8")
        signal = trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
        return signal, score * masks["near_ok"].astype("float64")
    if spec.transform_id == "aggressive_union_flip":
        other = load_source_payload("run293A_cp293F_asymmetric_tail_control_xgb_hold5")
        other_signal = (-pd.to_numeric(other["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()).astype("int8")
        other_score = source_score(other).to_numpy(dtype="float64")
        preferred = np.where(np.abs(other_score) > np.abs(score), other_signal, signal)
        signal = np.where(raw != 0, signal, preferred).astype("int8")
        signal = np.where(masks["aggressive_ok"], signal, 0).astype("int8")
        score = np.maximum(score, other_score)
        signal = trim_to_density(source, signal, score, spec.max_hold_bars, spec.target_density)
        return signal, score * masks["aggressive_ok"].astype("float64")
    return signal, score


def metrics_for_payload(spec: CandidateSpec, payload: pd.DataFrame, signal: np.ndarray, split: str) -> dict[str, Any]:
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
            float(validation_metrics["worst_rolling_20_bp"]) >= -260.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -260.0
            and float(validation_metrics["positive_month_share"]) >= 0.45
            and float(oos_metrics["positive_month_share"]) >= 0.45
            and float(validation_metrics["underwater_ratio"]) <= 0.92
            and float(oos_metrics["underwater_ratio"]) <= 0.92
        )
    return "passed" if ok else "failed"


def materialize_payload(spec: CandidateSpec) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any], list[Path]]:
    source = load_source_payload(spec.source_materialized_id)
    signal, decision_score = transform_signal(spec, source)
    branch_id = f"run294A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    payload["stage294_branch_id"] = branch_id
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "mt5_outcome_relabel_directional_flip_surface"
    payload["candidate_decision_score"] = decision_score
    payload["source_branch_id"] = spec.source_materialized_id
    payload["source_active_mask"] = (pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy() != 0).astype("int8")
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = route_label(signal)
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = 0.01
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = True
    payload["same_direction_reentry_cooldown_bars"] = 0
    surface_identity = {
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
    surface_hash = hashlib.sha256(json.dumps(surface_identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(("route_signal_value",))
    payload["model_feature_order_hash"] = "rule_surface_no_model_artifact"
    payload["payload_claim_boundary"] = BOUNDARY
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    validation_metrics = metrics_for_payload(spec, payload, signal, "validation")
    oos_metrics = metrics_for_payload(spec, payload, signal, "oos")
    return payload, surface_identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics, []


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
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, surface_identity, validation_metrics, oos_metrics, extra_artifacts = materialize_payload(spec)
        branch_id = f"run294A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "stage294_branch_id": branch_id,
                "package_id": spec.package_id,
                "source_materialized_id": spec.source_materialized_id,
                "source_package_id": spec.source_package_id,
                "dataset_id": spec.dataset_id,
                "feature_order": ["route_signal_value"],
                "feature_order_hash": ordered_hash(("route_signal_value",)),
                "transform_id": spec.transform_id,
                "target_density": spec.target_density,
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": True,
                "same_direction_reentry_cooldown_bars": 0,
                "runtime_handoff": "precomputed route_signal_value replay for MT5 outcome relabel directional flip probe",
                "claim_boundary": BOUNDARY,
                "surface_identity": surface_identity,
            },
        )
        candidate_supply = supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        for split_name, metrics in (("validation_proxy", validation_metrics), ("oos_proxy", oos_metrics)):
            wfo_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "fold_id": split_name,
                    "mode": spec.transform_id,
                    "quantile": 0.0,
                    "threshold": 0.0,
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
        manifest_rows.append(
            {
                "queue_id": f"run294A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "mt5_outcome_relabel_directional_flip_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": "",
                "model_artifact_hash": "",
                "model_feature_order_path": "",
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "direction_surface_hash": surface_identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(("route_signal_value",)),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": True,
                "same_direction_reentry_cooldown_bars": 0,
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
                "model_family": "rule_based_mt5_outcome_relabel_directional_flip",
                "prediction_kind": "precomputed_route_signal_rule_surface",
                "dataset_id": spec.dataset_id,
                "model_artifact_path": "",
                "model_artifact_hash": "",
                "model_feature_order_path": "",
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "imputation_path": "",
                "imputation_hash": "",
                "classes": "short|flat|long",
                "payoff_weight_policy": "source_mt5_negative_outcome_relabel_flip_skip_density",
                "onnx_exportability_note": "rule surface requires Adapter formalization or model distillation before ONNX export; export deferred until candidate gate",
            }
        )
        wfo_net = float(validation_metrics["net_bp"]) + float(oos_metrics["net_bp"])
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": "rule_based_mt5_outcome_relabel_directional_flip",
                "prediction_kind": "precomputed_route_signal_rule_surface",
                "mode": spec.transform_id,
                "quantile": 0.0,
                "threshold": 0.0,
                "precondition": spec.transform_id,
                "wfo_net_bp": wfo_net,
                "wfo_positive_fold_share": float(sum(1 for item in (validation_metrics, oos_metrics) if float(item["net_bp"]) > 0.0) / 2.0),
                "wfo_worst_fold_net_bp": float(min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"]))),
                "wfo_mean_trades_per_day": float(np.mean([float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])])),
                "wfo_min_trades_per_day": float(min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"]))),
                "wfo_max_trades_per_day": float(max(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"]))),
                "selection_score": wfo_net,
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
                "density_gate": gate_label(validation_metrics, oos_metrics, "density"),
                "proxy_edge_gate": gate_label(validation_metrics, oos_metrics, "edge"),
                "curve_proxy_gate": gate_label(validation_metrics, oos_metrics, "curve"),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        branch_rows.append(
            {
                "stage293_branch_id": branch_id,
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "idea_id": "IDEA-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP",
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe seed only; no candidate selection until run294B/run294C evidence",
                "comparison_baseline": "Stage293 valid negative runtime scoreboard plus cp293A/cp293F near-breakeven dense loss clue",
                "control_variables": "FPMarkets US100 M5 split_v1; Stage293 route-signal replay handoff; hold5; Tier A/B paired runtime accounting",
                "changed_variables": spec.changed_variables,
                "sample_scope": f"{spec.dataset_id}; validation/oos proxy read; Tier A and Tier B duplicated for paired runtime accounting",
                "success_criteria": "4-10 trades/day in validation and OOS, positive MT5 net/PF/recovery/expectancy, and no deep local curve pockets",
                "failure_criteria": "MT5 validation or OOS net/PF fails, density outside 4-10, or local curve pockets dominate",
                "invalid_conditions": "payload contains label/future columns, source payload missing, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "after full run294B MT5 probe and run294C review; no narrow transform repair inside Stage294",
                "evidence_plan": "model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run294B MT5 KPI; run294C curve/time-slice review",
                "model_family": "rule_based_mt5_outcome_relabel_directional_flip",
                "dataset_id": spec.dataset_id,
                "prediction_kind": "precomputed_route_signal_rule_surface",
                "objective_surface": "mt5_outcome_relabel_directional_flip",
                "selection_mode": spec.transform_id,
                "selection_quantile": 0.0,
                "selection_threshold": 0.0,
                "precondition": spec.transform_id,
                "risk_logic": spec.risk_logic,
                "adapter_path": "deferred_until_candidate_survives_run294B_run294C",
                "runtime_handoff": "route_signal_value replay now; rule identity retained for Adapter package if selected",
                "claim_boundary": BOUNDARY,
            }
        )
        artifacts.extend([payload_path, handoff_path, *extra_artifacts])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, [path for path in artifacts if path]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = []
    for row in scoreboard_rows:
        lines.append(
            f"- `{row['package_id']}`: mode(모드) `{row['mode']}`, validation(검증) `{float(row['validation_proxy_net_bp']):.2f}`bp/`{float(row['validation_proxy_trades_per_day']):.2f}` trades/day(일거래), "
            f"OOS(표본외) `{float(row['oos_proxy_net_bp']):.2f}`bp/`{float(row['oos_proxy_trades_per_day']):.2f}` trades/day(일거래), gates(관문) `{row['density_gate']}/{row['proxy_edge_gate']}/{row['curve_proxy_gate']}`."
        )
    queue_lines = [
        f"- `{row['package_id']}` -> `{row['materialized_branch_id']}` validation approx(검증 근사) `{float(row['approx_validation_trades_per_day']):.2f}`/day, OOS approx(표본외 근사) `{float(row['approx_oos_trades_per_day']):.2f}`/day"
        for row in manifest_rows
    ]
    return f"""# run294A MT5 Outcome Relabel Directional Flip Materialization(294A MT5 결과 재라벨 방향 반전 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_count(분기 수): `{len(manifest_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Thesis(논제)

Stage293(293단계)는 밀도는 일부 맞췄지만 실제 MT5 net profit(순수익)이 모두 음수였다. Stage294(294단계)는 이 음수 결과를 보존 단서로 써서 full flip(전체 반전), cost-aware skip(비용 인식 회피), density trim(밀도 절단), smooth curve routing(곡선 완화 라우팅)을 새 decision surface(판단 표면)로 만든다.

## Scoreboard(점수표)

{chr(10).join(lines)}

## MT5 Queue(MT5 대기열)

{chr(10).join(queue_lines)}

## Boundary(경계)

선택 후보, Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 주장하지 않는다. 이 산출물은 run294B(294B 실행) MT5 runtime probe(MT5 런타임 탐침) 입력이다.
"""


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
    for path in (RUN_ROOT, REVIEWS, PAYLOAD_DIR, HANDOFF_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(BRANCH_QUEUE, s293.BRANCH_COLUMNS, branch_rows)
    write_csv(MODEL_SCOREBOARD, s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, s293.SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, s293.MODEL_COLUMNS, model_rows)
    write_csv(WFO_FOLD_SCOREBOARD, s293.WFO_COLUMNS, wfo_rows)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "MT5 outcome relabeling and directional flip can convert Stage293 dense near-breakeven losses into a positive, smooth, 4-10 trades/day candidate seed.",
            "decision_use": "Decide whether Stage294 should proceed to full MT5 runtime probe and candidate review.",
            "comparison_baseline": "Stage293 run293C valid negative actual routed total scoreboard.",
            "control_variables": "US100 M5 split_v1; Stage293 source payloads; route_signal_value replay; max_hold_bars=5; close_on_flat_signal=true.",
            "changed_variables": "full flip, cost-aware skip, density trim, smooth-state veto, aggressive union flip.",
            "sample_scope": "Tier A and Tier B paired labels; validation/OOS source payload scope from Stage293.",
            "success_criteria": "4-10 trades/day, positive MT5 net/PF/recovery/expectancy, and no deep zoomed curve pocket.",
            "failure_criteria": "runtime negative, density outside 4-10, or curve pocket/concentration failure.",
            "invalid_conditions": "source payload missing, label/future columns leak into runtime payload, MT5 handoff mismatch, or report missing.",
            "stop_conditions": "run294B MT5 probe plus run294C review; do not repair one branch repeatedly inside Stage294.",
            "evidence_plan": "scoreboard, supply diagnostics, payload manifest, MT5 queue, run294B KPI, run294C curve review.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_model_manifest": rel(SOURCE_MODEL_MANIFEST),
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_failure_memory": rel(SOURCE_FAILURE),
            "runtime_payload_label_future_columns_removed": True,
            "tier_pairing": "Tier A and Tier B duplicated from source payloads for runtime accounting",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        s293.RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"branches={len(branch_rows)};mt5_queue_rows={len(manifest_rows)};report={rel(REPORT)}",
                "evidence_missing": "MT5 runtime KPI; trade report curve review; candidate package; Adapter package; ONNX parity",
                "judgment_label": JUDGMENT,
                "judgment_class": "materialization_no_candidate(물질화, 후보 아님)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "Stage294(294단계)는 아직 후보 선택이 아니라 MT5로 검증할 반전/회피 입력을 만든 상태다.",
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
                "evidence_path": rel(EXPERIMENT_DESIGN),
                "effect": "fresh thesis(새 논제), success/failure gate(성공/실패 관문), stop condition(정지 조건)을 기록했다.",
            },
            {
                "gate_name": "runtime_payload_integrity(런타임 페이로드 무결성)",
                "status": "passed",
                "evidence_path": rel(DATA_RECEIPT),
                "effect": "label/future column(라벨/미래 열)을 런타임 페이로드에서 제거했다.",
            },
            {
                "gate_name": "candidate_claim_boundary(후보 주장 경계)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)를 주장하지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    final_paths = [
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
            "created_at_utc": created_at,
            "branch_count": len(branch_rows),
            "mt5_queue_rows": len(manifest_rows),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
            "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path_exists(path)},
        },
    )
    final_paths.append(RUN_MANIFEST)
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source_artifacts": [rel(SOURCE_MANIFEST), rel(SOURCE_MODEL_MANIFEST), rel(SOURCE_SCOREBOARD), rel(SOURCE_FAILURE), rel(STAGE294_SEED_QUEUE)],
            "producer": rel(Path("stage_pipelines/stage294/design_materialize_mt5_outcome_relabel_directional_flip_rebuild.py")),
            "artifact_paths": [rel(path) for path in final_paths if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path_exists(path)},
            "claim_boundary": BOUNDARY,
        },
    )
    final_paths.append(LINEAGE)
    return [path for path in final_paths if path_exists(path)]


def update_artifact_registry(paths: Sequence[Path], created_at: str) -> None:
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage294_mt5_outcome_relabel_directional_flip_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run294A MT5 outcome relabel directional flip materialization",
        }
        for path in paths
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "mt5_outcome_relabel_directional_flip_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    upsert_csv(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "mt5_outcome_relabel_directional_flip_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_transform_and_runtime_queue",
                "scoreboard_lane": "mt5_outcome_relabel_directional_flip",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)};proxy_rows={len(scoreboard_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_materialization_only",
                "notes": "MT5 probe required before candidate judgment.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv(
        STAGE_LEDGER,
        s293.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "mt5_outcome_relabel_directional_flip_materialization",
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
    update_artifact_registry(artifacts, created_at)
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else "# Stage294 Selection Status(294단계 선택 상태)\n"
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run294A_report", f"- run294A_report(294A 보고): `{rel(REPORT)}`")
    selected = append_once(selected, "run294A_mt5_queue", f"- run294A_mt5_queue(294A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage294 Review Index(294단계 검토 색인)\n"
    review_index = append_once(review_index, "run294A_report", f"- run294A_report(294A 보고): `{rel(REPORT)}`\n- run294A_mt5_queue(294A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run294A_summary",
        f"- run294A_summary(294A 요약): MT5 outcome relabel directional flip(MT5 결과 재라벨 방향 반전) 후보 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): run294B(294B 실행)에서 일 4-10거래, 순수익, PF(수익 팩터), 회복, 곡선을 MT5 runtime probe(MT5 런타임 탐침)로 검증할 수 있게 했고 선택 후보/어댑터/온엑스는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage294(294단계) run294A(294A 실행) MT5 outcome relabel directional flip materialization(MT5 결과 재라벨 방향 반전 물질화) `{RUN_ID}`. "
        f"Effect(효과): 후보 `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열)를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run294A MT5 outcome relabel directional flip materialization(294A MT5 결과 재라벨 방향 반전 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
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
                "branch_count": len(branch_rows),
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
