from __future__ import annotations

import csv
import hashlib
import json
import os
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
from stage_pipelines.stage309 import design_split_coherent_profit_curve_source_rebuild as s309  # noqa: E402


STAGE_ID = "310_onnx_candidate_campaign__runtime_positive_fragment_allocation_rebuild"
RUN_ID = "run310A_design_runtime_positive_fragment_allocation_rebuild_packet_v1"
RUN_NUMBER = "run310A"
SOURCE_STAGE_ID = "309_onnx_candidate_campaign__split_coherent_profit_curve_source_rebuild"
SOURCE_RUN_ID = "run309C_review_split_coherent_profit_curve_source_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_runtime_positive_fragment_allocation_candidates_materialized_no_selection"
JUDGMENT = "runtime_positive_fragment_allocation_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run310B_execute_runtime_positive_fragment_allocation_mt5_probe"
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
SOURCE_RUN309A = SOURCE_STAGE / "02_runs" / "run309A"
SOURCE_RUN309C = SOURCE_STAGE / "02_runs" / "run309C"
SOURCE_MANIFEST = SOURCE_RUN309A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN309C / "split_coherent_profit_curve_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN309C / "stage310_seed_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run309C_review_stage310_open.md"

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
REPORT = REVIEWS / "run310A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage310/design_runtime_positive_fragment_allocation_rebuild.py")
RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = s309.DECISION_FEATURES + (
    "stage310_fragment_agreement_score",
    "stage310_allocation_support_score",
    "stage310_curve_floor_score",
)

SOURCE_PACKAGES = {
    "A": "cp309A_validation_curve_trend_guard_density50_hold5_surface",
    "C": "cp309C_trend_breadth_confirmation_density55_hold5_surface",
    "D": "cp309D_open_mid_reversion_curve_floor_density80_hold3_surface",
    "E": "cp309E_aggressive_oos_scale_trend_reallocation_density45_hold8_surface",
    "F": "cp309F_session_balanced_dual_source_density70_hold4_surface",
}

MANIFEST_COLUMNS = s309.MANIFEST_COLUMNS
BRANCH_COLUMNS = s309.BRANCH_COLUMNS
SCOREBOARD_COLUMNS = s309.SCOREBOARD_COLUMNS
SUPPLY_COLUMNS = s309.SUPPLY_COLUMNS
WFO_COLUMNS = s309.WFO_COLUMNS
MODEL_COLUMNS = s309.MODEL_COLUMNS
RESULT_COLUMNS = s309.RESULT_COLUMNS
GATE_COLUMNS = s309.GATE_COLUMNS
RUN_REGISTRY_COLUMNS = s309.RUN_REGISTRY_COLUMNS
STAGE_LEDGER_COLUMNS = s309.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = s309.ARTIFACT_COLUMNS


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    allocation_surface: str
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
            package_id="cp310A_overlap_density_lift_hold4_surface",
            allocation_surface="overlap_density_lift",
            target_density=7.2,
            max_hold_bars=4,
            fixed_lot=0.30,
            atr_stop_multiplier=1.25,
            atr_take_profit_multiplier=4.40,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            hypothesis="A/E/C positive fragments(A/E/C 양수 조각) overlap(겹침)을 우선 쓰고 부족한 밀도는 같은 방향 support(지원)로 채우면 실제 거래수와 곡선이 같이 개선된다.",
            changed_variables="cp309A/cp309E/cp309C signals(신호)을 후보가 아니라 allocation sources(배분 원천)로 재조합하고 hold4(4봉 보유)로 실제 거래 밀도를 올린다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp310B_curve_floor_session_allocator_hold3_surface",
            allocation_surface="curve_floor_session_allocator",
            target_density=8.4,
            max_hold_bars=3,
            fixed_lot=0.24,
            atr_stop_multiplier=1.10,
            atr_take_profit_multiplier=3.60,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.024,
            hypothesis="Session allocator(세션 배분기)가 open/mid/late(초반/중반/후반)의 다른 양수 조각을 나누면 국소 곡선 포켓을 줄일 수 있다.",
            changed_variables="cash open(현금장 초반)은 C, mid(중반)는 A, late(후반)는 E를 우선하고 D reversion(D 되돌림)은 curve floor(곡선 바닥) 보조로만 쓴다.",
            same_direction_reentry_cooldown_bars=0,
        ),
        CandidateSpec(
            package_id="cp310C_aggressive_fragment_union_hold5_surface",
            allocation_surface="aggressive_fragment_union",
            target_density=6.8,
            max_hold_bars=5,
            fixed_lot=0.34,
            atr_stop_multiplier=1.48,
            atr_take_profit_multiplier=5.30,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.035,
            hypothesis="Aggressive union(공격형 합집합)이 cp309E(309E)의 OOS scale(표본외 규모)을 cp309A/cp309C(309A/309C)의 보강 거래와 연결해 수익 규모를 키운다.",
            changed_variables="E priority(E 우선), A fallback(A 보조), C breadth(C 폭 확인) 순서로 배분하고 payoff target(보상 목표)을 높인다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp310D_alternating_session_fragment_router_hold4_surface",
            allocation_surface="alternating_session_fragment_router",
            target_density=7.6,
            max_hold_bars=4,
            fixed_lot=0.28,
            atr_stop_multiplier=1.22,
            atr_take_profit_multiplier=4.10,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.028,
            hypothesis="Alternating session router(교대 세션 라우터)가 한 표면의 약한 시간대를 다른 조각으로 교체하면 움푹 파인 구간을 줄인다.",
            changed_variables="세션별 A/C/E priority(우선순위)를 바꾸고 shock guard(충격 방어)를 더한다.",
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp310E_drawdown_avoidance_reallocation_hold3_surface",
            allocation_surface="drawdown_avoidance_reallocation",
            target_density=6.4,
            max_hold_bars=3,
            fixed_lot=0.26,
            atr_stop_multiplier=1.08,
            atr_take_profit_multiplier=3.90,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.026,
            hypothesis="Drawdown avoidance(손실폭 회피) 조건으로 양수 조각만 재배치하면 순수익은 유지하면서 회복 계수와 곡선 품질이 오른다.",
            changed_variables="low shock(낮은 충격), high smooth(높은 평활성), quality support(품질 지원)에서만 A/C를 쓰고 E는 late trend(후반 추세)에 제한한다.",
            same_direction_reentry_cooldown_bars=0,
        ),
        CandidateSpec(
            package_id="cp310F_scale_density_dual_book_hold4_surface",
            allocation_surface="scale_density_dual_book",
            target_density=9.0,
            max_hold_bars=4,
            fixed_lot=0.31,
            atr_stop_multiplier=1.30,
            atr_take_profit_multiplier=4.70,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.032,
            hypothesis="Dual book(이중 장부) 방식으로 trend book(추세 장부)과 reversion book(되돌림 장부)을 나누면 scale(규모)와 density(밀도)를 함께 확보한다.",
            changed_variables="A/E trend book(추세 장부)과 C/D/F support book(지원 장부)을 score(점수)로 경쟁시킨다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def long_path(path: Path) -> str:
    resolved = str(path.resolve())
    if os.name == "nt" and not resolved.startswith("\\\\?\\"):
        return "\\\\?\\" + resolved
    return resolved


def path_exists(path: Path) -> bool:
    try:
        return ledger.path_exists(path)
    except OSError:
        return path.exists()


def rel(path: Path | str) -> str:
    return s309.rel(path)


def read_text(path: Path) -> str:
    return s309.read_text(path)


def write_text(path: Path, text: str) -> None:
    s309.write_text(path, text)


def write_json(path: Path, payload: Any) -> None:
    s309.write_json(path, payload)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    s309.write_csv(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    return s309.read_csv_dicts(path)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s309.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return s309.sha256_file(path)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return s309.replace_line_prefix(text, prefix, replacement)


def append_once(text: str, marker: str, addition: str) -> str:
    return s309.append_once(text, marker, addition)


def prepend_focus(text: str, focus: str, marker: str) -> str:
    return s309.prepend_focus(text, focus, marker)


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    return s309.ncol(frame, column, default)


def zscore(values: np.ndarray) -> np.ndarray:
    return s309.zscore(values)


def positive(values: np.ndarray) -> np.ndarray:
    return s309.positive(values)


def signal_label(value: int) -> str:
    return s309.s308.s307.prev.s290.signal_label(value)


def read_source_manifest() -> dict[str, dict[str, str]]:
    rows = read_csv_dicts(SOURCE_MANIFEST)
    return {row["package_id"]: row for row in rows}


def read_source_payload(row: Mapping[str, str]) -> pd.DataFrame:
    path = ROOT / str(row["payload_path"])
    return pd.read_parquet(long_path(path))


def load_sources() -> dict[str, pd.DataFrame]:
    manifest = read_source_manifest()
    sources: dict[str, pd.DataFrame] = {}
    for key, package_id in SOURCE_PACKAGES.items():
        if package_id not in manifest:
            raise FileNotFoundError(f"missing source package in stage309 manifest: {package_id}")
        sources[key] = read_source_payload(manifest[package_id])
    base = sources["A"]
    check_cols = ["timestamp", "tier_scope", "split"]
    base_key = base[check_cols].astype(str).agg("|".join, axis=1)
    for key, frame in sources.items():
        frame_key = frame[check_cols].astype(str).agg("|".join, axis=1)
        if len(frame) != len(base) or not frame_key.equals(base_key):
            raise ValueError(f"source payload alignment failed for {key}")
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
    signals: dict[str, np.ndarray] = {}
    scores: dict[str, np.ndarray] = {}
    for key, frame in sources.items():
        signals[key] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
        score_col = "candidate_decision_score" if "candidate_decision_score" in frame.columns else "split_coherent_score_value"
        scores[key] = zscore(pd.to_numeric(frame[score_col], errors="coerce").fillna(0.0).to_numpy(dtype="float64"))
    return signals, scores


def weighted_direction(parts: Sequence[tuple[np.ndarray, np.ndarray, float]]) -> np.ndarray:
    total: np.ndarray | None = None
    for signal, score, weight in parts:
        piece = signal.astype("float64") * (1.0 + positive(score)) * weight
        total = piece if total is None else total + piece
    assert total is not None
    return np.sign(total).astype("int8")


def apply_mask(signal: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return np.where(mask, signal, 0).astype("int8")


def density_fit(
    frame: pd.DataFrame,
    signal: np.ndarray,
    score: np.ndarray,
    support_signal: np.ndarray,
    support_score: np.ndarray,
    *,
    hold_bars: int,
    target_density: float,
) -> np.ndarray:
    out = signal.astype("int8").copy()
    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    for (_tier, split), index in frame.groupby(["tier_scope", "split"], sort=False).groups.items():
        if split not in {"validation", "oos"}:
            continue
        idx = np.asarray(list(index), dtype=int)
        days = max(1, int(timestamp.iloc[idx].dt.date.nunique()))
        active_target = int(round(target_density * days * hold_bars))
        active_cap = int(round(10.0 * days * hold_bars))
        active_floor = int(round(4.05 * days * hold_bars))
        current_active = int(np.count_nonzero(out[idx]))
        if current_active < active_floor:
            candidate_idx = idx[(out[idx] == 0) & (support_signal[idx] != 0)]
            if len(candidate_idx):
                order = np.argsort(-support_score[candidate_idx])
                take = min(len(candidate_idx), max(active_floor, active_target) - current_active)
                chosen = candidate_idx[order[: max(0, take)]]
                out[chosen] = support_signal[chosen]
        current_active = int(np.count_nonzero(out[idx]))
        if current_active < active_target:
            candidate_idx = idx[(out[idx] == 0) & (support_signal[idx] != 0)]
            if len(candidate_idx):
                order = np.argsort(-support_score[candidate_idx])
                take = min(len(candidate_idx), active_target - current_active)
                chosen = candidate_idx[order[: max(0, take)]]
                out[chosen] = support_signal[chosen]
        if int(np.count_nonzero(out[idx])) > active_cap:
            out = s309.s308.s307.prev.s294.trim_to_density(
                frame,
                out,
                np.asarray(np.maximum(score, support_score), dtype="float64"),
                hold_bars,
                min(9.8, target_density),
            )
    return out.astype("int8")


def allocation_signal(spec: CandidateSpec, frame: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> tuple[np.ndarray, np.ndarray]:
    signals, scores = source_arrays(sources)
    outside, cash_open, mid, late = s309.s308.session_arrays(frame)
    minutes = ncol(frame, "minutes_from_cash_open")
    shock = s309.s308.shock_score(frame)
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    quality = zscore(ncol(frame, "profit_quality_score"))
    scale = zscore(ncol(frame, "profit_scale_score"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.55 * zscore(ncol(frame, "di_spread_14")) + 0.35 * zscore(ncol(frame, "ppo_hist_12_26_9"))
    breadth = zscore(ncol(frame, "mega8_pos_breadth_1")) + 0.50 * zscore(ncol(frame, "top3_weighted_return_1"))
    reversion = -(0.65 * zscore(ncol(frame, "return_zscore_20")) + 0.55 * zscore(ncol(frame, "bb_position_20", 0.5) - 0.5))
    trend_raw = np.sign(trend + 0.25 * breadth).astype("int8")
    reversion_raw = np.sign(reversion).astype("int8")
    session_support = 0.35 * cash_open + 0.55 * mid + 0.45 * late
    agreement = (signals["A"] == signals["E"]) & (signals["A"] != 0)
    two_of_three = np.sign(signals["A"].astype(int) + signals["C"].astype(int) + signals["E"].astype(int)).astype("int8")
    support_raw = np.where(two_of_three != 0, two_of_three, np.where(np.abs(trend) >= np.abs(reversion), trend_raw, reversion_raw)).astype("int8")
    support_score = (
        0.35 * positive(scores["A"])
        + 0.35 * positive(scores["E"])
        + 0.25 * positive(scores["C"])
        + 0.30 * positive(smooth)
        + 0.25 * positive(quality)
        + 0.25 * positive(scale)
        + 0.20 * session_support
        - 0.45 * shock
    )

    if spec.allocation_surface == "overlap_density_lift":
        raw = np.where(agreement, signals["A"], support_raw).astype("int8")
        score = support_score + 0.75 * agreement.astype("float64") - 0.25 * shock
        keep = (score > np.nanpercentile(score, 28)) & (shock < np.nanpercentile(shock, 86))
    elif spec.allocation_surface == "curve_floor_session_allocator":
        session_raw = np.where(cash_open > 0.0, signals["C"], np.where(mid > 0.0, signals["A"], signals["E"]))
        floor_raw = np.where(session_raw != 0, session_raw, np.where((minutes >= 20) & (minutes <= 330), signals["D"], support_raw))
        raw = floor_raw.astype("int8")
        score = 0.55 * support_score + 0.55 * positive(smooth) + 0.30 * mid + 0.20 * cash_open - 0.55 * shock
        keep = (score > np.nanpercentile(score, 22)) & (outside < 0.5)
    elif spec.allocation_surface == "aggressive_fragment_union":
        raw = np.where(signals["E"] != 0, signals["E"], np.where(signals["A"] != 0, signals["A"], support_raw)).astype("int8")
        score = 0.55 * positive(scores["E"]) + 0.35 * positive(scores["A"]) + 0.30 * positive(scale) + 0.25 * late + 0.20 * mid - 0.35 * shock
        keep = (score > np.nanpercentile(score, 34)) & (shock < np.nanpercentile(shock, 90))
    elif spec.allocation_surface == "alternating_session_fragment_router":
        raw = np.where(cash_open > 0.0, signals["C"], np.where(mid > 0.0, signals["A"], np.where(late > 0.0, signals["E"], support_raw))).astype("int8")
        score = 0.65 * support_score + 0.35 * (cash_open + mid + late) - 0.55 * shock
        keep = (score > np.nanpercentile(score, 25)) & (shock < np.nanpercentile(shock, 84))
    elif spec.allocation_surface == "drawdown_avoidance_reallocation":
        raw = np.where(late > 0.0, signals["E"], np.where(signals["A"] != 0, signals["A"], signals["C"])).astype("int8")
        score = 0.70 * positive(smooth) + 0.50 * positive(quality) + 0.35 * positive(scores["A"]) + 0.25 * positive(scores["C"]) - 0.85 * shock
        keep = (score > np.nanpercentile(score, 38)) & (shock < np.nanpercentile(shock, 70))
    elif spec.allocation_surface == "scale_density_dual_book":
        trend_book = weighted_direction(((signals["A"], scores["A"], 0.70), (signals["E"], scores["E"], 0.95), (trend_raw, support_score, 0.35)))
        support_book = weighted_direction(((signals["C"], scores["C"], 0.65), (signals["D"], scores["D"], 0.45), (signals["F"], scores["F"], 0.35), (reversion_raw, support_score, 0.25)))
        use_trend = (positive(scale) + positive(scores["E"]) + late) >= (positive(smooth) + positive(scores["C"]) + mid)
        raw = np.where(use_trend, trend_book, support_book).astype("int8")
        score = 0.45 * support_score + 0.35 * np.maximum(positive(scores["E"]), positive(scores["C"])) + 0.30 * (mid + late) - 0.40 * shock
        keep = (score > np.nanpercentile(score, 20)) & (shock < np.nanpercentile(shock, 88))
    else:
        raise ValueError(f"unsupported allocation_surface: {spec.allocation_surface}")

    signal = apply_mask(raw, keep)
    signal = density_fit(
        frame,
        signal,
        np.asarray(score, dtype="float64"),
        support_raw,
        np.asarray(support_score, dtype="float64"),
        hold_bars=spec.max_hold_bars,
        target_density=spec.target_density,
    )
    return signal.astype("int8"), np.asarray(score, dtype="float64")


def add_stage310_features(base: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    frame = s309.add_stage309_features(base)
    signals, scores = source_arrays(sources)
    agreement = ((signals["A"] == signals["E"]) & (signals["A"] != 0)).astype("float64")
    support = positive(scores["A"]) + positive(scores["C"]) + positive(scores["E"])
    frame["stage310_fragment_agreement_score"] = agreement
    frame["stage310_allocation_support_score"] = support
    frame["stage310_curve_floor_score"] = positive(zscore(ncol(frame, "smooth_curve_score"))) + 0.5 * positive(zscore(ncol(frame, "profit_quality_score")))
    return frame


def source_stage309_seed() -> str:
    rows = read_csv_dicts(SOURCE_SEED_QUEUE)
    return rows[0].get("seed_id", "stage309_positive_fragment_allocation_seed") if rows else "stage309_positive_fragment_allocation_seed"


def materialize_payload(spec: CandidateSpec, sources: Mapping[str, pd.DataFrame], seed_id: str, frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = allocation_signal(spec, frame, sources)
    branch_id = f"run310A_{spec.package_id.replace('_surface', '')}"
    base = sources["A"].copy()
    payload = base.copy()
    payload["stage310_branch_id"] = branch_id
    payload["stage309_branch_id"] = seed_id
    payload["stage308_branch_id"] = payload.get("stage308_branch_id", "")
    payload["stage307_branch_id"] = payload.get("stage307_branch_id", "")
    payload["stage306_branch_id"] = payload.get("stage306_branch_id", "")
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "runtime_positive_fragment_allocation_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = "cp309A/cp309C/cp309D/cp309E/cp309F"
    payload["source_transform_id"] = spec.allocation_surface
    payload["source_active_mask"] = (pd.to_numeric(base["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy() != 0).astype("int8")
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
        "allocation_surface": spec.allocation_surface,
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
    validation_metrics = s309.s308.s307.prev.metrics_for_payload(spec, payload, "validation")
    oos_metrics = s309.s308.s307.prev.metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


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


def gate_label(validation: Mapping[str, Any], oos: Mapping[str, Any], gate: str) -> str:
    return s309.gate_label(validation, oos, gate)


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    sources = load_sources()
    frame = add_stage310_features(sources["A"], sources)
    seed_id = source_stage309_seed()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, sources, seed_id, frame)
        branch_id = f"run310A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_allocation_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage310_branch_id": branch_id,
                "stage309_seed_id": seed_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage310 MT5 probe(310단계 MT5 탐침)",
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
            s309.s308.s307.prev.s290.selection_score(validation_metrics)
            + s309.s308.s307.prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.50
            + min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])) * 35.0
            - max(0.0, -float(validation_metrics["worst_rolling_20_bp"])) * 0.08
            - max(0.0, -float(oos_metrics["worst_rolling_20_bp"])) * 0.10
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe(MT5 런타임 탐침) 후보를 만들지 판단한다.",
                "comparison_baseline": "Stage309 cp309A/cp309E/cp309C positive fragments(309A/309E/309C 양수 조각) with no selected candidate(선택 후보 없음).",
                "control_variables": "US100 M5, split_v1(분할 v1), Stage309 source payloads(원천 페이로드), Tier A/B paired accounting(티어 쌍 기록).",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리) and MT5 runtime probe(MT5 런타임 탐침).",
                "success_criteria": "actual MT5 validation/OOS positive(검증/표본외 양수), minimum trade count(최소 거래수), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), smooth curve(매끄러운 곡선).",
                "failure_criteria": "trade density below 4/day(일 4거래 미만), weak net profit(약한 순수익), PF/recovery weakness(수익 팩터/회복 약점), deep local curve pocket(깊은 국소 곡선 포켓).",
                "invalid_conditions": "source payload mismatch(원천 페이로드 불일치), feature order mismatch(피처 순서 불일치), MT5 report parse missing(MT5 보고서 파싱 누락).",
                "stop_conditions": "candidate gate pass(후보 관문 통과) -> Adapter(어댑터); all fail(전부 실패) -> fresh edge rebuild(새 엣지 재구축).",
                "evidence_plan": "branch queue(분기 대기열), proxy scoreboard(대리 점수판), payload manifest(페이로드 목록), MT5 queue(MT5 대기열), run310B/run310C.",
                "feature_surface": "Stage309 source signals(원천 신호), fragment agreement(조각 일치), allocation support(배분 지원), curve floor(곡선 바닥).",
                "model_surface": "rule_surface_runtime_positive_fragment_allocation",
                "decision_surface": spec.allocation_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생); Adapter trace(어댑터 추적)는 후보 관문 뒤에 시작한다.",
                "failure_memory_plan": "allocation별 scale/density/curve failure(규모/밀도/곡선 실패)를 분리 기록한다.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run310A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": seed_id,
                "stage308_branch_id": str(payload.get("stage308_branch_id", pd.Series([""])).iloc[0]) if "stage308_branch_id" in payload else "",
                "stage307_branch_id": str(payload.get("stage307_branch_id", pd.Series([""])).iloc[0]) if "stage307_branch_id" in payload else "",
                "stage306_branch_id": str(payload.get("stage306_branch_id", pd.Series([""])).iloc[0]) if "stage306_branch_id" in payload else "",
                "package_id": spec.package_id,
                "queue_role": "runtime_positive_fragment_allocation_surface",
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
                "model_family": "runtime_positive_fragment_allocation_rule_surface",
                "prediction_kind": "runtime_positive_fragment_allocator",
                "dataset_id": "stage309_positive_fragments_plus_stage306_features",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "classes": "-1,0,1",
                "payoff_weight_policy": spec.allocation_surface,
                "onnx_exportability_note": "Adapter(어댑터) 전에는 ONNX(온엑스)를 시작하지 않는다.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "runtime_positive_fragment_allocation_rule_surface",
                "prediction_kind": "runtime_positive_fragment_allocator",
                "mode": spec.allocation_surface,
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
                    "mode": spec.allocation_surface,
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


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    result = [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "actual MT5 KPI(실제 MT5 KPI);parsed curve review(곡선 검토);candidate package(후보 패키지);Adapter package(어댑터 패키지);ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "judgment_class": "exploratory_materialization(탐색 물질화)",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage310(310단계)은 후보를 아직 고르지 않고 allocation layer(배분 계층)를 MT5(메타트레이더5)에 넘긴다.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Stage309(309단계) 양수 조각을 새 allocation layer(배분 계층) 질문으로 바꿨다."},
        {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
        {"gate_name": "density_proxy(밀도 대리)", "status": "passed" if density_pass else "failed", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day(일 4-10거래) proxy(대리)를 확인했다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "MT5 review(MT5 검토) 전에는 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "후보 선택 전에는 ONNX(온엑스)를 시작하지 않는다."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run310A Runtime Positive Fragment Allocation Materialization(310A 런타임 양수 조각 배분 물질화)",
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
        "Effect(효과): Stage309(309단계)의 cp309A/cp309E/cp309C 양수 조각을 후보로 승격하지 않고, runtime allocation layer(런타임 배분 계층) 후보로 다시 만든다.",
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
    result, gates = result_rows(scoreboard_rows, manifest_rows)
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
            "hypothesis": "runtime positive fragment allocation(런타임 양수 조각 배분)이 Stage309(309단계)의 양수 조각을 4-10 trades/day(일 4-10거래)와 smooth curve(매끄러운 곡선)로 바꿀 수 있는지 본다.",
            "decision_use": "run310B MT5 runtime probe(MT5 런타임 탐침) 대상으로 넘길 후보 표면을 만든다.",
            "comparison_baseline": "Stage309 no-selection(선택 없음), best positive fragments(최고 양수 조각) cp309A/cp309E/cp309C.",
            "control_variables": ["US100 M5", "split_v1", "Stage309 source payloads(원천 페이로드)", "Tier A/B paired accounting(티어 쌍 기록)"],
            "changed_variables": ["fragment allocation layer(조각 배분 계층)", "session allocation(세션 배분)", "density lift(밀도 상승)", "drawdown avoidance(손실폭 회피)", "risk profile(위험 프로필)"],
            "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리), then MT5 runtime probe(MT5 런타임 탐침).",
            "success_criteria": ["actual MT5 validation/OOS net positive(검증/표본외 순수익 양수)", "minimum trade count(최소 거래수)", "4-10 trades/day(일 4-10거래)", "profit scale(수익 규모)", "shallow curve pocket(얕은 곡선 포켓)"],
            "failure_criteria": ["density below target(밀도 미달)", "net profit too small(순수익 부족)", "PF/recovery weak(수익 팩터/회복 약함)", "deep curve pocket(깊은 곡선 포켓)"],
            "invalid_conditions": ["source payload alignment failure(원천 페이로드 정렬 실패)", "feature order mismatch(피처 순서 불일치)", "MT5 report missing(MT5 보고서 누락)"],
            "stop_conditions": ["candidate gate pass(후보 관문 통과) -> Adapter(어댑터)", "all fail(전부 실패) -> new stage fresh edge(새 단계 새 엣지)"],
            "evidence_plan": [rel(BRANCH_QUEUE), rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run310B MT5 KPI", "run310C review"],
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
    safe_upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_positive_fragment_allocation_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        "run_id",
    )
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
                "record_view": "runtime_positive_fragment_allocation_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_density_edge_curve_screen",
                "scoreboard_lane": "runtime_positive_fragment_allocation",
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
    safe_upsert(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "runtime_positive_fragment_allocation_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        "row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage310_runtime_positive_fragment_allocation_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run310A runtime positive fragment allocation materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run310A_report", f"- run310A_report(310A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run310A_mt5_queue", f"- run310A_mt5_queue(310A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX) or "# Stage310 Review Index(310단계 검토 색인)\n"
    review_index = append_once(review_index, "run310A_report", f"- run310A_report(310A 보고서): `{rel(REPORT)}`")
    review_index = append_once(review_index, "run310A_mt5_queue", f"- run310A_mt5_queue(310A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)

    idea = read_text(IDEA_REGISTER)
    idea = append_once(
        idea,
        "stage310_runtime_positive_fragment_allocation",
        "## stage310_runtime_positive_fragment_allocation\n\n- hypothesis(가설): Stage309(309단계)의 runtime positive fragments(런타임 양수 조각)를 allocation layer(배분 계층)로 묶으면 거래수와 곡선 품질이 같이 개선될 수 있다.\n- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).\n",
    )
    write_text(IDEA_REGISTER, idea)

    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run310A_summary",
        f"- run310A_summary(310A 요약): runtime positive fragment allocation(런타임 양수 조각 배분) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): Stage309(309단계)의 양수 조각을 후보로 보존하지 않고 새 allocation surface(배분 표면) MT5 queue(MT5 대기열) `{len(manifest_rows)}`개로 넘겼으며 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage310(310단계) run310A(310A 실행) runtime positive fragment allocation materialization(런타임 양수 조각 배분 물질화) `{RUN_ID}`. "
        f"Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run310A Runtime positive fragment allocation materialization(310A 런타임 양수 조각 배분 물질화)\n\n"
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
