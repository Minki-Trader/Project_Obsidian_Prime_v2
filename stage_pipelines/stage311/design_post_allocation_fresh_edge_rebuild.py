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

from foundation.control_plane import ledger  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage310 import design_runtime_positive_fragment_allocation_rebuild as s310  # noqa: E402


STAGE_ID = "311_onnx_candidate_campaign__post_allocation_fresh_edge_rebuild"
RUN_ID = "run311A_design_post_allocation_fresh_edge_rebuild_packet_v1"
RUN_NUMBER = "run311A"
SOURCE_STAGE_ID = "310_onnx_candidate_campaign__runtime_positive_fragment_allocation_rebuild"
SOURCE_RUN_ID = "run310C_review_runtime_positive_fragment_allocation_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_post_allocation_fresh_edge_candidates_materialized_no_selection"
JUDGMENT = "post_allocation_fresh_edge_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run311B_execute_post_allocation_fresh_edge_mt5_probe"
BOUNDARY = s310.BOUNDARY

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
SOURCE_RUN310A = SOURCE_STAGE / "02_runs" / "run310A"
SOURCE_RUN310C = SOURCE_STAGE / "02_runs" / "run310C"
SOURCE_MANIFEST = SOURCE_RUN310A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN310C / "runtime_positive_fragment_allocation_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN310C / "stage311_seed_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run310C_review_stage311_open.md"

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
REPORT = REVIEWS / "run311A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage311/design_post_allocation_fresh_edge_rebuild.py")
RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = s310.DECISION_FEATURES + (
    "stage311_adverse_hour_score",
    "stage311_session_mirror_score",
)

SOURCE_PACKAGES = {
    "A": "cp310A_overlap_density_lift_hold4_surface",
    "C": "cp310C_aggressive_fragment_union_hold5_surface",
    "E": "cp310E_drawdown_avoidance_reallocation_hold3_surface",
}

MANIFEST_COLUMNS = s310.MANIFEST_COLUMNS
BRANCH_COLUMNS = s310.BRANCH_COLUMNS
SCOREBOARD_COLUMNS = s310.SCOREBOARD_COLUMNS
SUPPLY_COLUMNS = s310.SUPPLY_COLUMNS
WFO_COLUMNS = s310.WFO_COLUMNS
MODEL_COLUMNS = s310.MODEL_COLUMNS
RESULT_COLUMNS = s310.RESULT_COLUMNS
GATE_COLUMNS = s310.GATE_COLUMNS
RUN_REGISTRY_COLUMNS = s310.RUN_REGISTRY_COLUMNS
STAGE_LEDGER_COLUMNS = s310.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = s310.ARTIFACT_COLUMNS


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    decision_surface: str
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
            package_id="cp311A_hour16_19_direction_mirror_hold4_surface",
            decision_surface="hour16_19_direction_mirror",
            target_density=7.0,
            max_hold_bars=4,
            fixed_lot=0.30,
            atr_stop_multiplier=1.22,
            atr_take_profit_multiplier=4.30,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            hypothesis="Stage310 cp310A(310A)에서 validation/OOS(검증/표본외) 모두 hour16/hour19(16시/19시)가 손실원이므로 방향 반전이 새 edge(엣지)가 될 수 있다.",
            changed_variables="cp310A base signal(기본 신호)을 유지하되 hour16/hour19(16시/19시)에서 mirror(반전)한다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp311B_hour16_mirror_19_veto_hold4_surface",
            decision_surface="hour16_mirror_19_veto",
            target_density=6.4,
            max_hold_bars=4,
            fixed_lot=0.29,
            atr_stop_multiplier=1.18,
            atr_take_profit_multiplier=4.00,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.028,
            hypothesis="hour16(16시)은 mirror(반전)하고 hour19(19시)는 veto(차단)하면 validation(검증) 손실을 줄이면서 OOS(표본외) 강점을 보존할 수 있다.",
            changed_variables="hour16 mirror(16시 반전), hour19 veto(19시 차단), A/C support(지원)로 밀도 보강.",
        ),
        CandidateSpec(
            package_id="cp311C_adverse_cluster_mirror_hold3_surface",
            decision_surface="adverse_cluster_mirror",
            target_density=8.2,
            max_hold_bars=3,
            fixed_lot=0.26,
            atr_stop_multiplier=1.08,
            atr_take_profit_multiplier=3.70,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.026,
            hypothesis="validation adverse cluster(검증 불리 군집) 16/19/21시를 반전하고 20/22시는 품질 조건으로만 허용하면 곡선 포켓이 얕아진다.",
            changed_variables="hour16/19/21 mirror(시간 반전), hour20/22 quality gate(품질 관문), hold3(3봉 보유).",
            same_direction_reentry_cooldown_bars=0,
        ),
        CandidateSpec(
            package_id="cp311D_oos_scale_preserve_16_19_mirror_hold5_surface",
            decision_surface="oos_scale_preserve_16_19_mirror",
            target_density=5.8,
            max_hold_bars=5,
            fixed_lot=0.34,
            atr_stop_multiplier=1.45,
            atr_take_profit_multiplier=5.10,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.034,
            hypothesis="cp310A의 OOS scale(표본외 규모)을 보존하면서 16/19시 방향만 반전하면 profit scale(수익 규모)을 크게 키울 수 있다.",
            changed_variables="A/E trend book(추세 장부)을 보존하고 adverse hour(불리 시간대) 방향만 바꾼다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp311E_conservative_17_18_20_router_hold3_surface",
            decision_surface="conservative_17_18_20_router",
            target_density=5.2,
            max_hold_bars=3,
            fixed_lot=0.24,
            atr_stop_multiplier=1.05,
            atr_take_profit_multiplier=3.50,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.024,
            hypothesis="validation(검증)에서 상대적으로 덜 깨진 17/18/20시만 쓰고 부족한 밀도는 low-shock support(저충격 지원)로 채우면 안정성이 오른다.",
            changed_variables="safe-hour router(안전 시간 라우터), low shock support(저충격 지원), defensive risk(방어 위험).",
        ),
        CandidateSpec(
            package_id="cp311F_model_feature_adverse_hour_blend_hold4_surface",
            decision_surface="model_feature_adverse_hour_blend",
            target_density=7.4,
            max_hold_bars=4,
            fixed_lot=0.30,
            atr_stop_multiplier=1.24,
            atr_take_profit_multiplier=4.40,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.031,
            hypothesis="adverse-hour mirror(불리 시간대 반전)와 feature trend/reversion blend(피처 추세/되돌림 혼합)를 결합하면 단순 시간 규칙보다 덜 취약한 표면이 된다.",
            changed_variables="hour mirror(시간 반전), trend/reversion feature support(추세/되돌림 피처 지원), A/C/E source competition(원천 경쟁).",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s310.rel(path)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    return s310.read_csv_dicts(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    s310.write_csv(path, columns, rows)


def write_text(path: Path, text: str) -> None:
    s310.write_text(path, text)


def write_json(path: Path, payload: Any) -> None:
    s310.write_json(path, payload)


def read_text(path: Path) -> str:
    return s310.read_text(path)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s310.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return s310.sha256_file(path)


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    return s310.ncol(frame, column, default)


def zscore(values: np.ndarray) -> np.ndarray:
    return s310.zscore(values)


def positive(values: np.ndarray) -> np.ndarray:
    return s310.positive(values)


def signal_label(value: int) -> str:
    return s310.signal_label(value)


def read_source_manifest() -> dict[str, dict[str, str]]:
    rows = read_csv_dicts(SOURCE_MANIFEST)
    return {row["package_id"]: row for row in rows}


def load_sources() -> dict[str, pd.DataFrame]:
    manifest = read_source_manifest()
    sources: dict[str, pd.DataFrame] = {}
    for key, package_id in SOURCE_PACKAGES.items():
        row = manifest[package_id]
        sources[key] = pd.read_parquet(s310.long_path(ROOT / row["payload_path"]))
    base = sources["A"]
    base_key = base[["timestamp", "tier_scope", "split"]].astype(str).agg("|".join, axis=1)
    for key, frame in sources.items():
        frame_key = frame[["timestamp", "tier_scope", "split"]].astype(str).agg("|".join, axis=1)
        if len(frame) != len(base) or not frame_key.equals(base_key):
            raise ValueError(f"source alignment failed for {key}")
    return sources


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


def source_arrays(sources: Mapping[str, pd.DataFrame]) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    return s310.source_arrays(sources)


def add_stage311_features(base: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    frame = s310.add_stage310_features(base, sources)
    hour = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    adverse = np.isin(hour, [16, 19]).astype("float64")
    cluster = np.isin(hour, [16, 19, 21]).astype("float64")
    frame["stage311_adverse_hour_score"] = adverse + 0.5 * cluster
    frame["stage311_session_mirror_score"] = np.where(np.isin(hour, [16, 19, 21]), 1.0, 0.0)
    return frame


def support_arrays(frame: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> tuple[np.ndarray, np.ndarray]:
    signals, scores = source_arrays(sources)
    hour = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    shock = s310.s309.s308.shock_score(frame)
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    quality = zscore(ncol(frame, "profit_quality_score"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.55 * zscore(ncol(frame, "di_spread_14")) + 0.35 * zscore(ncol(frame, "ppo_hist_12_26_9"))
    ret = zscore(ncol(frame, "return_zscore_20"))
    bb = zscore(ncol(frame, "bb_position_20", 0.5) - 0.5)
    reversion = -(0.65 * ret + 0.55 * bb)
    feature_raw = np.where(np.abs(trend) >= np.abs(reversion), np.sign(trend), np.sign(reversion)).astype("int8")
    source_vote = np.sign(signals["A"].astype(int) + signals["C"].astype(int) + signals["E"].astype(int)).astype("int8")
    raw = np.where(source_vote != 0, source_vote, feature_raw).astype("int8")
    score = (
        0.45 * positive(scores["A"])
        + 0.30 * positive(scores["C"])
        + 0.25 * positive(scores["E"])
        + 0.35 * positive(smooth)
        + 0.25 * positive(quality)
        + 0.20 * np.isin(hour, [17, 18, 20, 22]).astype("float64")
        - 0.45 * shock
    )
    return raw, score


def transform_signal(spec: CandidateSpec, frame: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> tuple[np.ndarray, np.ndarray]:
    signals, scores = source_arrays(sources)
    base = signals["A"].copy()
    support_raw, support_score = support_arrays(frame, sources)
    hour = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    shock = s310.s309.s308.shock_score(frame)
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    quality = zscore(ncol(frame, "profit_quality_score"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.55 * zscore(ncol(frame, "di_spread_14"))
    ret = zscore(ncol(frame, "return_zscore_20"))
    mirror_16_19 = np.isin(hour, [16, 19])
    mirror_cluster = np.isin(hour, [16, 19, 21])
    quality_ok = (positive(smooth) + positive(quality) - 0.65 * shock) > np.nanpercentile(positive(smooth) + positive(quality) - 0.65 * shock, 36)

    if spec.decision_surface == "hour16_19_direction_mirror":
        raw = np.where(mirror_16_19, -base, base).astype("int8")
        score = support_score + 0.65 * mirror_16_19.astype("float64") - 0.20 * shock
    elif spec.decision_surface == "hour16_mirror_19_veto":
        raw = np.where(hour == 16, -base, base).astype("int8")
        raw = np.where(hour == 19, 0, raw).astype("int8")
        score = support_score + 0.45 * (hour == 16).astype("float64") - 0.25 * shock
    elif spec.decision_surface == "adverse_cluster_mirror":
        raw = np.where(mirror_cluster, -base, base).astype("int8")
        raw = np.where(np.isin(hour, [20, 22]) & ~quality_ok, 0, raw).astype("int8")
        score = support_score + 0.55 * mirror_cluster.astype("float64") + 0.25 * quality_ok.astype("float64") - 0.25 * shock
    elif spec.decision_surface == "oos_scale_preserve_16_19_mirror":
        trend_book = np.where(signals["E"] != 0, signals["E"], base)
        raw = np.where(mirror_16_19, -trend_book, trend_book).astype("int8")
        score = 0.55 * positive(scores["E"]) + 0.35 * positive(scores["A"]) + 0.25 * np.isin(hour, [18, 20, 22]).astype("float64") - 0.25 * shock
    elif spec.decision_surface == "conservative_17_18_20_router":
        raw = np.where(np.isin(hour, [17, 18, 20]), base, 0).astype("int8")
        raw = np.where((raw == 0) & (shock < np.nanpercentile(shock, 55)) & quality_ok, support_raw, raw).astype("int8")
        score = support_score + 0.40 * np.isin(hour, [17, 18, 20]).astype("float64") - 0.55 * shock
    elif spec.decision_surface == "model_feature_adverse_hour_blend":
        feature_raw = np.where(np.abs(trend) >= np.abs(ret), np.sign(trend), -np.sign(ret)).astype("int8")
        blend = np.where(np.abs(support_score) > np.nanpercentile(np.abs(support_score), 45), support_raw, feature_raw).astype("int8")
        raw = np.where(mirror_16_19, -blend, blend).astype("int8")
        score = support_score + 0.30 * positive(zscore(np.abs(trend))) + 0.35 * mirror_16_19.astype("float64") - 0.30 * shock
    else:
        raise ValueError(f"unsupported decision surface: {spec.decision_surface}")

    keep = (raw != 0) & (score > np.nanpercentile(score, 18)) & (shock < np.nanpercentile(shock, 92))
    signal = np.where(keep, raw, 0).astype("int8")
    signal = s310.density_fit(
        frame,
        signal,
        np.asarray(score, dtype="float64"),
        support_raw,
        np.asarray(support_score, dtype="float64"),
        hold_bars=spec.max_hold_bars,
        target_density=spec.target_density,
    )
    return signal.astype("int8"), np.asarray(score, dtype="float64")


def source_seed() -> str:
    rows = read_csv_dicts(SOURCE_SEED_QUEUE)
    return rows[0].get("seed_id", "stage310_allocation_review_seed") if rows else "stage310_allocation_review_seed"


def materialize_payload(spec: CandidateSpec, sources: Mapping[str, pd.DataFrame], seed_id: str, frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = transform_signal(spec, frame, sources)
    branch_id = f"run311A_{spec.package_id.replace('_surface', '')}"
    payload = sources["A"].copy()
    payload["stage311_branch_id"] = branch_id
    payload["stage310_branch_id"] = seed_id
    payload["stage309_branch_id"] = payload.get("stage309_branch_id", "")
    payload["stage308_branch_id"] = payload.get("stage308_branch_id", "")
    payload["stage307_branch_id"] = payload.get("stage307_branch_id", "")
    payload["stage306_branch_id"] = payload.get("stage306_branch_id", "")
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "post_allocation_fresh_edge_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = "cp310A/cp310C/cp310E"
    payload["source_transform_id"] = spec.decision_surface
    payload["source_active_mask"] = (pd.to_numeric(sources["A"]["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy() != 0).astype("int8")
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct if spec.model_risk_sizing_enabled else 0.0
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_seed_id": seed_id,
        "source_packages": SOURCE_PACKAGES,
        "decision_surface": spec.decision_surface,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "model_feature_order": list(DECISION_FEATURES),
        "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
        "risk_logic": risk_manifest_fields(spec),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(RUNTIME_FEATURE_ORDER)
    payload["model_feature_order_hash"] = ordered_hash(DECISION_FEATURES)
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = s310.s309.s308.s307.prev.metrics_for_payload(spec, payload, "validation")
    oos_metrics = s310.s309.s308.s307.prev.metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def gate_label(validation: Mapping[str, Any], oos: Mapping[str, Any], gate: str) -> str:
    return s310.gate_label(validation, oos, gate)


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    sources = load_sources()
    frame = add_stage311_features(sources["A"], sources)
    seed_id = source_seed()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, sources, seed_id, frame)
        branch_id = f"run311A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_fresh_edge_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(s310.long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage311_branch_id": branch_id,
                "stage310_seed_id": seed_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage311 MT5 probe(311단계 MT5 탐침)",
                "claim_boundary": BOUNDARY,
            },
        )
        candidate_supply = s310.supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        den_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s310.s309.s308.s307.prev.s290.selection_score(validation_metrics)
            + s310.s309.s308.s307.prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.45
            + min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])) * 35.0
            - max(0.0, -float(validation_metrics["worst_rolling_20_bp"])) * 0.12
            - max(0.0, -float(oos_metrics["worst_rolling_20_bp"])) * 0.12
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe(MT5 런타임 탐침) 후보를 만들지 판단한다.",
                "comparison_baseline": "Stage310 cp310A OOS-positive validation-negative allocation(표본외 양수/검증 음수 배분).",
                "control_variables": "US100 M5, split_v1(분할 v1), Stage310 source payloads(원천 페이로드), Tier A/B paired accounting(티어 쌍 기록).",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리) and MT5 runtime probe(MT5 런타임 탐침).",
                "success_criteria": "actual MT5 validation/OOS positive(검증/표본외 양수), minimum trade count(최소 거래수), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), smooth curve(매끄러운 곡선).",
                "failure_criteria": "validation loss(검증 손실), density outside 4-10(밀도 이탈), weak profit scale(약한 수익 규모), deep curve pocket(깊은 곡선 포켓).",
                "invalid_conditions": "source payload mismatch(원천 페이로드 불일치), feature order mismatch(피처 순서 불일치), MT5 report parse missing(MT5 보고서 파싱 누락).",
                "stop_conditions": "candidate gate pass(후보 관문 통과) -> Adapter(어댑터); all fail(전부 실패) -> next fresh edge(다음 새 엣지).",
                "evidence_plan": "branch queue(분기 대기열), proxy scoreboard(대리 점수판), payload manifest(페이로드 목록), MT5 queue(MT5 대기열), run311B/run311C.",
                "feature_surface": "Stage310 source signals(원천 신호), adverse hour score(불리 시간 점수), session mirror score(세션 반전 점수), trend/reversion support(추세/되돌림 지원).",
                "model_surface": "rule_surface_post_allocation_fresh_edge",
                "decision_surface": spec.decision_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생); Adapter trace(어댑터 추적)는 후보 관문 뒤에 시작한다.",
                "failure_memory_plan": "adverse-hour mirror(불리 시간 반전)별 scale/density/curve failure(규모/밀도/곡선 실패)를 분리 기록한다.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run311A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": str(payload.get("stage309_branch_id", pd.Series([""])).iloc[0]) if "stage309_branch_id" in payload else "",
                "stage308_branch_id": str(payload.get("stage308_branch_id", pd.Series([""])).iloc[0]) if "stage308_branch_id" in payload else "",
                "stage307_branch_id": str(payload.get("stage307_branch_id", pd.Series([""])).iloc[0]) if "stage307_branch_id" in payload else "",
                "stage306_branch_id": str(payload.get("stage306_branch_id", pd.Series([""])).iloc[0]) if "stage306_branch_id" in payload else "",
                "package_id": spec.package_id,
                "queue_role": "post_allocation_fresh_edge_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
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
                "model_family": "post_allocation_fresh_edge_rule_surface",
                "prediction_kind": "adverse_hour_directional_mirror",
                "dataset_id": "stage310_actual_failure_memory_plus_stage310_payloads",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "classes": "-1,0,1",
                "payoff_weight_policy": spec.decision_surface,
                "onnx_exportability_note": "Adapter(어댑터) 전에는 ONNX(온엑스)를 시작하지 않는다.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "post_allocation_fresh_edge_rule_surface",
                "prediction_kind": "adverse_hour_directional_mirror",
                "mode": spec.decision_surface,
                "validation_proxy_net_bp": validation_metrics["net_bp"],
                "validation_proxy_pf": validation_metrics["pf"],
                "validation_proxy_trade_count": validation_metrics["trade_count"],
                "validation_proxy_trades_per_day": validation_metrics["trades_per_day"],
                "validation_proxy_recovery": validation_metrics["recovery"],
                "validation_proxy_worst_month_bp": validation_metrics["worst_month_bp"],
                "validation_proxy_worst_rolling_20_bp": validation_metrics["worst_rolling_20_bp"],
                "validation_proxy_worst_rolling_50_bp": validation_metrics["worst_rolling_50_bp"],
                "validation_proxy_positive_month_share": validation_metrics["positive_month_share"],
                "oos_proxy_net_bp": oos_metrics["net_bp"],
                "oos_proxy_pf": oos_metrics["pf"],
                "oos_proxy_trade_count": oos_metrics["trade_count"],
                "oos_proxy_trades_per_day": oos_metrics["trades_per_day"],
                "oos_proxy_recovery": oos_metrics["recovery"],
                "oos_proxy_worst_month_bp": oos_metrics["worst_month_bp"],
                "oos_proxy_worst_rolling_20_bp": oos_metrics["worst_rolling_20_bp"],
                "oos_proxy_worst_rolling_50_bp": oos_metrics["worst_rolling_50_bp"],
                "oos_proxy_positive_month_share": oos_metrics["positive_month_share"],
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
                    "mode": spec.decision_surface,
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
    scoreboard_rows.sort(key=lambda row: float(row["selection_score"]), reverse=True)
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, artifacts


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run311A Post-Allocation Fresh Edge Materialization(311A 배분 이후 새 엣지 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidates(후보): `{len(scoreboard_rows)}`",
        f"- MT5 queue rows(MT5 대기열 행): `{len(manifest_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage310(310단계)의 배분 실패를 좁게 수리하지 않고, adverse-hour mirror(불리 시간대 방향 반전)와 feature support(피처 지원)를 새 표면으로 만든다.",
        "",
        "| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일 거래) | gates(관문) |",
        "|---|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        gate_text = ",".join(name for name, key in (("density", "density_gate"), ("edge", "proxy_edge_gate"), ("curve", "curve_proxy_gate")) if row[key] != "passed")
        lines.append(
            "| {pkg} | {val:.2f} | {oos:.2f} | {vtd:.2f}/{otd:.2f} | {gates} |".format(
                pkg=row["package_id"],
                val=float(row["validation_proxy_net_bp"]),
                oos=float(row["oos_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                gates=gate_text or "passed",
            )
        )
    lines.extend(["", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    wfo_rows: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
) -> list[Path]:
    result = [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}",
            "evidence_missing": "actual MT5 KPI(실제 MT5 KPI);candidate package(후보 패키지);Adapter package(어댑터 패키지);ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "judgment_class": "exploratory_materialization(탐색 물질화)",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage311(311단계)은 adverse-hour fresh edge(불리 시간대 새 엣지)를 MT5(메타트레이더5)에 넘긴다.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Stage310(310단계) allocation failure(배분 실패)를 adverse-hour mirror(불리 시간 반전) 질문으로 바꿨다."},
        {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "MT5 review(MT5 검토) 전에는 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "후보 선택 전에는 ONNX(온엑스)를 시작하지 않는다."},
    ]
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(MODEL_SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, MODEL_COLUMNS, model_rows)
    write_csv(WFO_FOLD_SCOREBOARD, WFO_COLUMNS, wfo_rows)
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result)
    write_csv(GATE_AUDIT, GATE_COLUMNS, gates)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "adverse-hour directional mirror(불리 시간대 방향 반전)가 Stage310(310단계)의 validation loss(검증 손실)를 줄이고 OOS scale(표본외 규모)을 유지할 수 있는지 본다.",
            "decision_use": "run311B MT5 runtime probe(MT5 런타임 탐침) 대상으로 넘길 후보 표면을 만든다.",
            "comparison_baseline": "Stage310 no-selection(선택 없음), cp310A validation-negative/OOS-positive(검증 음수/표본외 양수).",
            "control_variables": ["US100 M5", "split_v1", "Stage310 source payloads(원천 페이로드)", "Tier A/B paired accounting(티어 쌍 기록)"],
            "changed_variables": ["adverse-hour mirror(불리 시간 반전)", "session veto(세션 차단)", "feature trend/reversion support(피처 추세/되돌림 지원)", "risk profile(위험 프로필)"],
            "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리), then MT5 runtime probe(MT5 런타임 탐침).",
            "success_criteria": ["actual MT5 validation/OOS net positive(검증/표본외 순수익 양수)", "minimum trade count(최소 거래수)", "4-10 trades/day(일 4-10거래)", "profit scale(수익 규모)", "shallow curve pocket(얕은 곡선 포켓)"],
            "failure_criteria": ["validation still negative(검증 여전히 음수)", "density outside 4-10(밀도 이탈)", "PF/recovery weak(수익 팩터/회복 약함)", "deep curve pocket(깊은 곡선 포켓)"],
            "invalid_conditions": ["source payload alignment failure(원천 페이로드 정렬 실패)", "feature order mismatch(피처 순서 불일치)", "MT5 report missing(MT5 보고서 누락)"],
            "stop_conditions": ["candidate gate pass(후보 관문 통과) -> Adapter(어댑터)", "all fail(전부 실패) -> next fresh edge(다음 새 엣지)"],
            "evidence_plan": [rel(BRANCH_QUEUE), rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run311B MT5 KPI", "run311C review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_seed_queue": rel(SOURCE_SEED_QUEUE),
            "source_packages": SOURCE_PACKAGES,
            "decision_feature_count": len(DECISION_FEATURES),
            "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
            "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
            "claim_boundary": BOUNDARY,
        },
    )
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
            "artifacts": [rel(path) for path in [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, LINEAGE, REPORT]],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": str(PRODUCER),
            "source_inputs": [rel(SOURCE_MANIFEST), rel(SOURCE_SCOREBOARD), rel(SOURCE_SEED_QUEUE), rel(SOURCE_REVIEW)],
            "consumer": NEXT_ACTION,
            "artifact_paths": {"scoreboard": rel(MODEL_SCOREBOARD), "mt5_queue": rel(MT5_QUEUE), "report": rel(REPORT)},
            "artifact_hashes": {"model_feature_order_hash": ordered_hash(DECISION_FEATURES), "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER)},
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": BOUNDARY,
        },
    )
    write_text(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return list(payload_artifacts) + [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT]


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    safe_upsert(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_allocation_fresh_edge_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}], "run_id")
    safe_upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "post_allocation_fresh_edge_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_density_edge_curve_screen",
                "scoreboard_lane": "post_allocation_fresh_edge",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"materialized={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "post_allocation_fresh_edge_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}], "row_id")
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage311_post_allocation_fresh_edge_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run311A post-allocation fresh edge materialization",
        }
        for path in artifacts
        if s310.path_exists(path)
    ]
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = s310.replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = s310.replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = s310.replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = s310.append_once(selected, "run311A_report", f"- run311A_report(311A 보고서): `{rel(REPORT)}`")
    selected = s310.append_once(selected, "run311A_mt5_queue", f"- run311A_mt5_queue(311A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX) or "# Stage311 Review Index(311단계 검토 색인)\n"
    review_index = s310.append_once(review_index, "run311A_report", f"- run311A_report(311A 보고서): `{rel(REPORT)}`")
    review_index = s310.append_once(review_index, "run311A_mt5_queue", f"- run311A_mt5_queue(311A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)

    idea = read_text(IDEA_REGISTER)
    idea = s310.append_once(
        idea,
        "stage311_post_allocation_fresh_edge",
        "## stage311_post_allocation_fresh_edge\n\n- hypothesis(가설): Stage310(310단계)의 validation loss(검증 손실) 시간 구조를 adverse-hour mirror(불리 시간대 방향 반전)로 바꾸면 새 edge(엣지)가 될 수 있다.\n- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).\n",
    )
    write_text(IDEA_REGISTER, idea)

    current = read_text(CURRENT_STATE)
    current = s310.replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = s310.replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = s310.replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = s310.replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = s310.replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = s310.replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = s310.append_once(current, "run311A_summary", f"- run311A_summary(311A 요약): adverse-hour mirror fresh edge(불리 시간대 방향 반전 새 엣지) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): Stage310(310단계) 배분 실패를 좁게 반복하지 않고 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개로 넘겼으며 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.")
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = s310.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = s310.replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = s310.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage311(311단계) run311A(311A 실행) post-allocation fresh edge materialization(배분 이후 새 엣지 물질화) `{RUN_ID}`. "
        f"Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = s310.prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = s310.append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run311A Post-allocation fresh edge materialization(311A 배분 이후 새 엣지 물질화)\n\n"
        f"- run_id(실행 ID): `{RUN_ID}`\n"
        f"- status(상태): `{STATUS}`\n"
        f"- candidates(후보): `{len(scoreboard_rows)}`\n"
        f"- mt5_queue_rows(MT5 대기열 행): `{len(manifest_rows)}`\n"
        f"- next_action(다음 행동): `{NEXT_ACTION}`\n",
    )
    write_text(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts)
    update_registers(scoreboard_rows, manifest_rows, artifacts, created_at)
    update_docs(scoreboard_rows, manifest_rows)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_count": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "best_proxy": scoreboard_rows[0]["package_id"] if scoreboard_rows else "none",
                "best_validation_net_bp": scoreboard_rows[0]["validation_proxy_net_bp"] if scoreboard_rows else 0,
                "best_oos_net_bp": scoreboard_rows[0]["oos_proxy_net_bp"] if scoreboard_rows else 0,
                "next_action": NEXT_ACTION,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
