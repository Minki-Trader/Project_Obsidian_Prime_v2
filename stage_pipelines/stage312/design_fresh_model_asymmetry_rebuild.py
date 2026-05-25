from __future__ import annotations

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

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage310 import design_runtime_positive_fragment_allocation_rebuild as s310  # noqa: E402


STAGE_ID = "312_onnx_candidate_campaign__fresh_model_asymmetry_rebuild"
RUN_ID = "run312A_design_fresh_model_asymmetry_rebuild_packet_v1"
RUN_NUMBER = "run312A"
SOURCE_STAGE_ID = "311_onnx_candidate_campaign__post_allocation_fresh_edge_rebuild"
SOURCE_RUN_ID = "run311C_review_post_allocation_fresh_edge_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_fresh_model_asymmetry_candidates_materialized_no_selection"
JUDGMENT = "fresh_model_asymmetry_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run312B_execute_fresh_model_asymmetry_mt5_probe"
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
SOURCE_RUN311A = SOURCE_STAGE / "02_runs" / "run311A"
SOURCE_RUN311C = SOURCE_STAGE / "02_runs" / "run311C"
SOURCE_MANIFEST = SOURCE_RUN311A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN311C / "post_allocation_fresh_edge_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN311C / "stage312_seed_queue.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN311C / "failure_memory.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run311C_review_stage312_open.md"

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
REPORT = REVIEWS / "run312A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage312/design_fresh_model_asymmetry_rebuild.py")
RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = s310.DECISION_FEATURES + (
    "stage312_empirical_asymmetry_score",
    "stage312_short_bias_score",
    "stage312_curve_guard_score",
)

SOURCE_PACKAGES = {
    "A": "cp311E_conservative_17_18_20_router_hold3_surface",
    "B": "cp311F_model_feature_adverse_hour_blend_hold4_surface",
    "C": "cp311B_hour16_mirror_19_veto_hold4_surface",
    "D": "cp311D_oos_scale_preserve_16_19_mirror_hold5_surface",
    "E": "cp311A_hour16_19_direction_mirror_hold4_surface",
    "F": "cp311C_adverse_cluster_mirror_hold3_surface",
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
    model_surface: str
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
            package_id="cp312A_cash_short_asymmetry_hold3_surface",
            model_surface="cash_short_asymmetry",
            target_density=6.4,
            max_hold_bars=3,
            fixed_lot=0.30,
            atr_stop_multiplier=1.12,
            atr_take_profit_multiplier=4.10,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            hypothesis="Stage310/311 actual MT5(실제 메타트레이더5) failure memory(실패 기억)에서 17/18/20시 sell(매도)이 양수 조각이고 16시와 buy(매수) 과잉이 손실 축이면, short-side asymmetry(매도 비대칭) 표면이 곡선 포켓을 줄일 수 있다.",
            changed_variables="hour mirror(시간 반전) 규칙을 버리고, empirical direction table(경험 방향 표)과 quality/curve guard(품질/곡선 방어)로 sell 17/18/20 중심 신호를 만든다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp312B_short_core_buy19_release_hold3_surface",
            model_surface="short_core_buy19_release",
            target_density=6.8,
            max_hold_bars=3,
            fixed_lot=0.29,
            atr_stop_multiplier=1.10,
            atr_take_profit_multiplier=3.95,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.028,
            hypothesis="17/18/20시 sell(매도) 핵심에 19시 high-scale buy(고규모 매수)만 제한적으로 풀면 OOS(표본외) 양수 조각을 살리면서 검증 손실을 줄일 수 있다.",
            changed_variables="sell core(매도 핵심), 19시 buy release(매수 해제), 16시 veto(차단), shock cap(충격 상한)을 새 판단 표면으로 쓴다.",
        ),
        CandidateSpec(
            package_id="cp312C_defensive_curve_guard_short_hold2_surface",
            model_surface="defensive_curve_guard_short",
            target_density=8.0,
            max_hold_bars=2,
            fixed_lot=0.23,
            atr_stop_multiplier=0.95,
            atr_take_profit_multiplier=3.20,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.022,
            hypothesis="짧은 보유와 낮은 위험으로 sell(매도) 비대칭을 촘촘히 반복하면 minimum trade count(최소 거래 수)와 4-10 trades/day(일 4-10거래)를 지키면서 깊은 포켓을 얕게 만들 수 있다.",
            changed_variables="hold2(2봉 보유), defensive risk(방어 위험), curve guard(곡선 방어), density floor(거래 밀도 하한)를 함께 바꾼다.",
        ),
        CandidateSpec(
            package_id="cp312D_aggressive_short_convexity_hold4_surface",
            model_surface="aggressive_short_convexity",
            target_density=5.6,
            max_hold_bars=4,
            fixed_lot=0.36,
            atr_stop_multiplier=1.38,
            atr_take_profit_multiplier=5.35,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.036,
            hypothesis="수익 규모가 낮다는 사용자 피드백을 반영해, sell(매도) 비대칭에 payoff convexity(보상 볼록성)를 붙이면 scale(규모)을 키울 수 있다.",
            changed_variables="aggressive take profit(공격형 익절), larger lot(큰 랏), short convexity score(매도 볼록 점수), 22시 제한 진입을 바꾼다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp312E_profile_table_density_balancer_hold3_surface",
            model_surface="profile_table_density_balancer",
            target_density=8.4,
            max_hold_bars=3,
            fixed_lot=0.27,
            atr_stop_multiplier=1.05,
            atr_take_profit_multiplier=3.70,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.026,
            hypothesis="actual hour-direction profile(실제 시간-방향 표)를 밀도 조절기에 넣으면 좋은 조각을 보존하면서 과도한 하루 거래 수를 피할 수 있다.",
            changed_variables="hour-direction empirical table(시간-방향 경험표), density balancer(밀도 조절기), 16시 hard veto(강제 차단)를 도입한다.",
        ),
        CandidateSpec(
            package_id="cp312F_split_consensus_asymmetry_hold4_surface",
            model_surface="split_consensus_asymmetry",
            target_density=6.0,
            max_hold_bars=4,
            fixed_lot=0.31,
            atr_stop_multiplier=1.22,
            atr_take_profit_multiplier=4.55,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.031,
            hypothesis="Stage311 source consensus(원천 합의)와 empirical short bias(경험 매도 편향)가 같은 방향일 때만 거래하면 검증과 표본외의 방향 불일치를 줄일 수 있다.",
            changed_variables="source consensus(원천 합의), empirical asymmetry(경험 비대칭), split-consistent guard(분할 일관 방어)를 결합한다.",
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


def rel(path: Path | str) -> str:
    return s310.rel(path)


def read_text(path: Path) -> str:
    return s310.read_text(path)


def write_text(path: Path, text: str) -> None:
    s310.write_text(path, text)


def write_json(path: Path, payload: Any) -> None:
    s310.write_json(path, payload)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    s310.write_csv(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    return s310.read_csv_dicts(path)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s310.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return s310.sha256_file(path)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return s310.replace_line_prefix(text, prefix, replacement)


def append_once(text: str, marker: str, addition: str) -> str:
    return s310.append_once(text, marker, addition)


def prepend_focus(text: str, focus: str, marker: str) -> str:
    return s310.prepend_focus(text, focus, marker)


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    return s310.ncol(frame, column, default)


def zscore(values: np.ndarray) -> np.ndarray:
    return s310.zscore(values)


def positive(values: np.ndarray) -> np.ndarray:
    return s310.positive(values)


def signal_label(value: int) -> str:
    return s310.signal_label(value)


def read_source_manifest() -> dict[str, dict[str, str]]:
    return {row["package_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def load_sources() -> dict[str, pd.DataFrame]:
    manifest = read_source_manifest()
    sources: dict[str, pd.DataFrame] = {}
    for key, package_id in SOURCE_PACKAGES.items():
        row = manifest[package_id]
        sources[key] = pd.read_parquet(long_path(ROOT / row["payload_path"]))
    base = sources["A"]
    check = base[["timestamp", "tier_scope", "split"]].astype(str).agg("|".join, axis=1)
    for key, frame in sources.items():
        other = frame[["timestamp", "tier_scope", "split"]].astype(str).agg("|".join, axis=1)
        if len(frame) != len(base) or not other.equals(check):
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
    signals: dict[str, np.ndarray] = {}
    scores: dict[str, np.ndarray] = {}
    for key, frame in sources.items():
        signals[key] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
        scores[key] = zscore(pd.to_numeric(frame["candidate_decision_score"], errors="coerce").fillna(0.0).to_numpy(dtype="float64"))
    return signals, scores


def add_stage312_features(base: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    frame = base.copy()
    signals, scores = source_arrays(sources)
    hour = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    shock = s310.s309.s308.shock_score(frame)
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    quality = zscore(ncol(frame, "profit_quality_score"))
    scale = zscore(ncol(frame, "profit_scale_score"))
    short_bias = np.isin(hour, [17, 18, 20]).astype("float64") - 0.85 * (hour == 16).astype("float64")
    empirical = (
        0.90 * np.isin(hour, [17, 18, 20]).astype("float64")
        + 0.25 * (hour == 19).astype("float64")
        - 0.75 * (hour == 16).astype("float64")
        - 0.25 * np.isin(hour, [21, 22]).astype("float64")
    )
    consensus = np.sign(sum(signal.astype("int16") for signal in signals.values())).astype("float64")
    frame["stage312_empirical_asymmetry_score"] = empirical + 0.20 * consensus
    frame["stage312_short_bias_score"] = short_bias + 0.35 * positive(-zscore(ncol(frame, "ema20_ema50_diff")))
    frame["stage312_curve_guard_score"] = positive(smooth) + positive(quality) + 0.30 * positive(scale) - 0.80 * shock
    return frame


def support_arrays(frame: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> tuple[np.ndarray, np.ndarray]:
    signals, scores = source_arrays(sources)
    hour = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    shock = s310.s309.s308.shock_score(frame)
    quality = zscore(ncol(frame, "profit_quality_score"))
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    scale = zscore(ncol(frame, "profit_scale_score"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.55 * zscore(ncol(frame, "di_spread_14")) + 0.35 * zscore(ncol(frame, "ppo_hist_12_26_9"))
    breadth = zscore(ncol(frame, "mega8_pos_breadth_1")) + 0.45 * zscore(ncol(frame, "top3_weighted_return_1"))
    consensus = np.sign(sum(signal.astype("int16") for signal in signals.values())).astype("int8")
    short_hours = np.isin(hour, [17, 18, 20])
    buy_release = (hour == 19) & (scale > np.nanpercentile(scale, 55)) & (trend > np.nanpercentile(trend, 45))
    fallback = np.where(short_hours, -1, np.where(buy_release, 1, consensus)).astype("int8")
    fallback = np.where(hour == 16, 0, fallback).astype("int8")
    score = (
        0.42 * positive(scores["A"])
        + 0.28 * positive(scores["B"])
        + 0.22 * positive(scores["C"])
        + 0.45 * positive(quality)
        + 0.40 * positive(smooth)
        + 0.28 * positive(scale)
        + 0.25 * positive(-trend)
        + 0.16 * positive(breadth)
        + 0.50 * short_hours.astype("float64")
        - 0.72 * shock
    )
    return fallback.astype("int8"), np.asarray(score, dtype="float64")


def transform_signal(spec: CandidateSpec, frame: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> tuple[np.ndarray, np.ndarray]:
    signals, scores = source_arrays(sources)
    support_signal, support_score = support_arrays(frame, sources)
    hour = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    shock = s310.s309.s308.shock_score(frame)
    quality = zscore(ncol(frame, "profit_quality_score"))
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    scale = zscore(ncol(frame, "profit_scale_score"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.55 * zscore(ncol(frame, "di_spread_14")) + 0.35 * zscore(ncol(frame, "ppo_hist_12_26_9"))
    breadth = zscore(ncol(frame, "mega8_pos_breadth_1")) + 0.45 * zscore(ncol(frame, "top3_weighted_return_1"))
    consensus = np.sign(sum(signal.astype("int16") for signal in signals.values())).astype("int8")
    curve_guard = positive(smooth) + positive(quality) + 0.30 * positive(scale) - 0.85 * shock
    short_hours = np.isin(hour, [17, 18, 20])
    hard_veto = (hour == 16) | (shock >= np.nanpercentile(shock, 92))

    if spec.model_surface == "cash_short_asymmetry":
        raw = np.where(short_hours, -1, 0).astype("int8")
        score = support_score + 0.55 * short_hours.astype("float64") + 0.25 * positive(-trend) - 0.35 * shock
        keep = (score > np.nanpercentile(score, 18)) & ~hard_veto
    elif spec.model_surface == "short_core_buy19_release":
        buy_release = (hour == 19) & (scale > np.nanpercentile(scale, 58)) & (curve_guard > np.nanpercentile(curve_guard, 36))
        raw = np.where(short_hours, -1, np.where(buy_release, 1, 0)).astype("int8")
        score = support_score + 0.50 * short_hours.astype("float64") + 0.30 * buy_release.astype("float64") - 0.38 * shock
        keep = (score > np.nanpercentile(score, 20)) & ~hard_veto
    elif spec.model_surface == "defensive_curve_guard_short":
        raw = np.where(np.isin(hour, [17, 18, 20]) & (curve_guard > np.nanpercentile(curve_guard, 28)), -1, 0).astype("int8")
        score = 0.70 * curve_guard + 0.35 * positive(scores["A"]) + 0.25 * short_hours.astype("float64") - 0.50 * shock
        keep = (score > np.nanpercentile(score, 24)) & (shock < np.nanpercentile(shock, 78))
    elif spec.model_surface == "aggressive_short_convexity":
        extra_short = np.isin(hour, [17, 18, 20, 22]) & (scale > np.nanpercentile(scale, 45))
        buy_release = (hour == 19) & (scale > np.nanpercentile(scale, 62)) & (trend > np.nanpercentile(trend, 50))
        raw = np.where(extra_short, -1, np.where(buy_release, 1, 0)).astype("int8")
        score = support_score + 0.45 * positive(scale) + 0.42 * positive(-trend) + 0.25 * extra_short.astype("float64") - 0.28 * shock
        keep = (score > np.nanpercentile(score, 25)) & (shock < np.nanpercentile(shock, 88)) & (hour != 16)
    elif spec.model_surface == "profile_table_density_balancer":
        profile = np.zeros(len(frame), dtype="int8")
        profile[np.isin(hour, [17, 18, 20])] = -1
        profile[(hour == 19) & (curve_guard > np.nanpercentile(curve_guard, 42))] = 1
        profile[(hour == 1) & (consensus < 0)] = -1
        raw = profile
        score = support_score + 0.35 * np.isin(hour, [17, 18, 20]).astype("float64") + 0.22 * positive(breadth) - 0.35 * shock
        keep = (score > np.nanpercentile(score, 17)) & ~hard_veto
    elif spec.model_surface == "split_consensus_asymmetry":
        raw = np.where(short_hours & (consensus <= 0), -1, np.where((hour == 19) & (consensus >= 0) & (scale > np.nanpercentile(scale, 56)), 1, 0)).astype("int8")
        score = support_score + 0.35 * (consensus != 0).astype("float64") + 0.35 * positive(quality) + 0.25 * positive(smooth) - 0.42 * shock
        keep = (score > np.nanpercentile(score, 19)) & ~hard_veto
    else:
        raise ValueError(f"unsupported model surface: {spec.model_surface}")

    signal = np.where(keep, raw, 0).astype("int8")
    signal = s310.density_fit(
        frame,
        signal,
        np.asarray(score, dtype="float64"),
        support_signal,
        np.asarray(support_score, dtype="float64"),
        hold_bars=spec.max_hold_bars,
        target_density=spec.target_density,
    )
    return signal.astype("int8"), np.asarray(score, dtype="float64")


def source_seed() -> str:
    rows = read_csv_dicts(SOURCE_SEED_QUEUE)
    return rows[0].get("seed_id", "stage311_fresh_edge_review_seed") if rows else "stage311_fresh_edge_review_seed"


def materialize_payload(spec: CandidateSpec, sources: Mapping[str, pd.DataFrame], seed_id: str, frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = transform_signal(spec, frame, sources)
    branch_id = f"run312A_{spec.package_id.replace('_surface', '')}"
    payload = sources["A"].copy()
    payload["stage312_branch_id"] = branch_id
    payload["stage311_branch_id"] = seed_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "fresh_model_asymmetry_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = "cp311E/cp311F/cp311B/cp311D/cp311A/cp311C"
    payload["source_transform_id"] = spec.model_surface
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
        "model_surface": spec.model_surface,
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
    frame = add_stage312_features(sources["A"], sources)
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
        branch_id = f"run312A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_model_asymmetry_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage312_branch_id": branch_id,
                "stage311_seed_id": seed_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage312 MT5 probe(312단계 MT5 탐침)",
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
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.35
            + min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])) * 42.0
            - max(0.0, -float(validation_metrics["worst_rolling_20_bp"])) * 0.10
            - max(0.0, -float(oos_metrics["worst_rolling_20_bp"])) * 0.10
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe(MT5 런타임 탐침) 대상 후보인지 판단한다.",
                "comparison_baseline": "Stage311 no-selection(선택 없음) and Stage310/311 actual hour-direction failure memory(실제 시간-방향 실패 기억).",
                "control_variables": "US100 M5, split_v1(분할 v1), Tier A/B paired accounting(티어 A/B 쌍 기록), Stage311 source payloads(311단계 원천 페이로드).",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리) and MT5 runtime probe(MT5 런타임 탐침).",
                "success_criteria": "actual MT5 validation/OOS positive(검증/표본외 양수), minimum trade count(최소 거래 수), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), smooth curve(매끈한 곡선).",
                "failure_criteria": "validation loss(검증 손실), OOS loss(표본외 손실), density outside 4-10(밀도 이탈), weak scale(약한 규모), deep curve pocket(깊은 곡선 포켓).",
                "invalid_conditions": "source payload mismatch(원천 페이로드 불일치), feature order mismatch(피처 순서 불일치), MT5 report parse missing(MT5 보고서 파싱 누락).",
                "stop_conditions": "candidate gate pass(후보 관문 통과) -> Adapter(어댑터); all fail(전부 실패) -> next fresh thesis(다음 새 논제).",
                "evidence_plan": "branch queue(분기 대기열), proxy scoreboard(대리 점수판), payload manifest(페이로드 목록), MT5 queue(MT5 대기열), run312B/run312C.",
                "feature_surface": "Stage311 source signals(원천 신호), actual hour-direction memory(실제 시간-방향 기억), quality/curve/scale guards(품질/곡선/규모 방어).",
                "model_surface": "rule_surface_fresh_model_asymmetry",
                "decision_surface": spec.model_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생); Adapter trace(어댑터 추적)는 후보 관문 뒤에 시작한다.",
                "failure_memory_plan": "direction asymmetry(방향 비대칭), density(밀도), profit scale(수익 규모), curve pocket(곡선 포켓)을 분리해 기록한다.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run312A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": str(payload.get("stage309_branch_id", pd.Series([""])).iloc[0]) if "stage309_branch_id" in payload else "",
                "stage308_branch_id": str(payload.get("stage308_branch_id", pd.Series([""])).iloc[0]) if "stage308_branch_id" in payload else "",
                "stage307_branch_id": str(payload.get("stage307_branch_id", pd.Series([""])).iloc[0]) if "stage307_branch_id" in payload else "",
                "stage306_branch_id": str(payload.get("stage306_branch_id", pd.Series([""])).iloc[0]) if "stage306_branch_id" in payload else "",
                "package_id": spec.package_id,
                "queue_role": "fresh_model_asymmetry_surface",
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
                "model_family": "fresh_model_asymmetry_rule_surface",
                "prediction_kind": "runtime_direction_asymmetry",
                "dataset_id": "stage311_actual_failure_memory_plus_stage311_payloads",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "classes": "-1,0,1",
                "payoff_weight_policy": spec.model_surface,
                "onnx_exportability_note": "Adapter(어댑터) 전에는 ONNX(온엑스)를 시작하지 않는다.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "fresh_model_asymmetry_rule_surface",
                "prediction_kind": "runtime_direction_asymmetry",
                "mode": spec.model_surface,
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
                    "mode": spec.model_surface,
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
            "evidence_missing": "actual MT5 KPI(실제 MT5 핵심 성과 지표);parsed curve review(곡선 검토);candidate package(후보 패키지);Adapter package(어댑터 패키지);ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "judgment_class": "exploratory_materialization(탐색 물질화)",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "312단계는 수익 규모와 거래 밀도 요구를 설계 입력으로 넣고 실제 MT5(메타트레이더5)에서 확인한다.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "시간대 보정 반복이 아니라 방향 비대칭 모델 표면으로 질문을 바꿨다."},
        {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
        {"gate_name": "density_proxy(밀도 대리)", "status": "passed" if density_pass else "failed", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day(일 4-10거래) 대리 조건을 확인했다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "MT5 review(MT5 검토) 전에는 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "후보 선택 전에는 ONNX(온엑스)를 시작하지 않는다."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run312A Fresh Model Asymmetry Materialization(312A 새 모델 비대칭 물질화)",
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
        "Effect(효과): Stage311(311단계) 시간대 반전 실패를 그대로 고치지 않고, 실제 시간-방향 손익 기억과 품질/곡선 방어를 새 decision surface(판단 표면)로 물질화했다.",
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
            "hypothesis": "fresh model asymmetry(새 모델 비대칭)가 Stage310/311 actual MT5(실제 MT5) 실패 기억의 방향 손실을 줄이고 4-10 trades/day(일 4-10거래)와 수익 규모를 함께 만족할 수 있는지 본다.",
            "decision_use": "run312B MT5 runtime probe(MT5 런타임 탐침) 대상을 만든다.",
            "comparison_baseline": "Stage311 no-selection(선택 없음) and Stage310/311 hour-direction failure memory(시간-방향 실패 기억).",
            "control_variables": ["US100 M5", "split_v1", "Stage311 source payloads(311단계 원천 페이로드)", "Tier A/B paired accounting(티어 A/B 쌍 기록)"],
            "changed_variables": ["direction asymmetry(방향 비대칭)", "empirical hour-direction table(경험 시간-방향 표)", "density balancer(밀도 조절기)", "risk/reward asymmetry(위험/보상 비대칭)"],
            "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리), then MT5 runtime probe(MT5 런타임 탐침).",
            "success_criteria": ["actual MT5 validation/OOS net positive(검증/표본외 순수익 양수)", "minimum trade count(최소 거래 수)", "4-10 trades/day(일 4-10거래)", "profit scale(수익 규모)", "smooth rising curve(매끈한 우상향 곡선)"],
            "failure_criteria": ["weak net profit(약한 순수익)", "PF/recovery/expectancy weak(수익 팩터/회복/기대값 약함)", "deep curve pocket(깊은 곡선 포켓)", "density outside 4-10(밀도 이탈)"],
            "invalid_conditions": ["source payload alignment failure(원천 페이로드 정렬 실패)", "feature order mismatch(피처 순서 불일치)", "MT5 report missing(MT5 보고서 누락)"],
            "stop_conditions": ["candidate gate pass(후보 관문 통과) -> Adapter(어댑터)", "all fail(전부 실패) -> new stage fresh thesis(새 단계 새 논제)"],
            "evidence_plan": [rel(BRANCH_QUEUE), rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run312B MT5 KPI", "run312C review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_seed_queue": rel(SOURCE_SEED_QUEUE),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY),
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
            "candidate_count": len(scoreboard_rows),
            "mt5_queue_rows": len(manifest_rows),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_started",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "artifacts": [rel(path) for path in payload_artifacts]
            + [rel(path) for path in (BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT)],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": str(PRODUCER),
            "source_inputs": [rel(SOURCE_MANIFEST), rel(SOURCE_SCOREBOARD), rel(SOURCE_SEED_QUEUE), rel(SOURCE_FAILURE_MEMORY), rel(SOURCE_REVIEW)],
            "consumer": NEXT_ACTION,
            "artifact_paths": json.loads(RUN_MANIFEST.read_text(encoding="utf-8"))["artifacts"] if RUN_MANIFEST.exists() else [],
            "availability": "tracked_manifest_plus_payloads",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": BOUNDARY,
        },
    )
    write_text(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return list(payload_artifacts) + [
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
    ]


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    safe_upsert(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "fresh_model_asymmetry_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};selected_candidate=none;next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(
        ALPHA_LEDGER,
        s310.s309.s308.s307.prev.s290.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "fresh_model_asymmetry_materialization",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B routed preparation",
                "kpi_scope": "proxy_plus_mt5_queue",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started",
                "external_verification_status": "prepared_not_executed",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "fresh_model_asymmetry_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")
    artifact_rows = []
    for path in artifacts:
        if not s310.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage312_fresh_model_asymmetry_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "Stage312 design/materialization artifact",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run312A_report", f"- run312A_report(312A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run312A_mt5_queue", f"- run312A_mt5_queue(312A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = append_once(review_index, "run312A_report", f"- run312A_report(312A 보고서): `{rel(REPORT)}`\n- run312A_scoreboard(312A 점수판): `{rel(MODEL_SCOREBOARD)}`\n- run312A_mt5_queue(312A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run312A_summary", f"- run312A_summary(312A 요약): fresh model asymmetry(새 모델 비대칭) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): 최소 거래 수와 4-10 trades/day(일 4-10거래)를 설계 밀도로 맞춘 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.")
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage312(312단계) run312A(312A 실행) fresh model asymmetry materialization(새 모델 비대칭 물질화) `{RUN_ID}`. "
        f"Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += (
            f"\n## {UPDATED_ON} run312A Fresh model asymmetry materialization(312A 새 모델 비대칭 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): 후보 `{len(scoreboard_rows)}`개와 MT5 대기열 `{len(manifest_rows)}`개를 만들었다.\n"
            "- boundary(경계): 선택 후보, Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 없다.\n"
        )
    write_text(CHANGELOG, changelog)

    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} fresh_model_asymmetry(새 모델 비대칭)\n\n"
            "- idea_id(아이디어 ID): `stage312_fresh_model_asymmetry`\n"
            "- hypothesis(가설): actual hour-direction memory(실제 시간-방향 기억)를 새 decision surface(판단 표면)로 쓰면 수익 규모와 밀도를 동시에 압박할 수 있다.\n"
            "- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        )
        write_text(IDEA_REGISTER, idea)


def main() -> None:
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts)
    created_at = utc_now()
    update_registers(scoreboard_rows, manifest_rows, artifacts, created_at)
    update_docs(scoreboard_rows, manifest_rows)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_rows": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
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
