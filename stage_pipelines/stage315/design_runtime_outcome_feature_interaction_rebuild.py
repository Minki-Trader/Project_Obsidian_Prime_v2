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

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage314 import design_runtime_outcome_feature_source_rebuild as s314  # noqa: E402


s310 = s314.s310

STAGE_ID = "315_onnx_candidate_campaign__runtime_outcome_feature_interaction_rebuild"
RUN_ID = "run315A_design_runtime_outcome_feature_interaction_rebuild_packet_v1"
RUN_NUMBER = "run315A"
SOURCE_STAGE_ID = "314_onnx_candidate_campaign__runtime_outcome_feature_source_rebuild"
SOURCE_RUN_ID = "run314C_review_runtime_outcome_feature_source_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_runtime_outcome_feature_interaction_candidates_materialized_no_selection"
JUDGMENT = "runtime_outcome_feature_interaction_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run315B_execute_runtime_outcome_feature_interaction_mt5_probe"
BOUNDARY = s314.BOUNDARY

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
SOURCE_RUN314A = SOURCE_STAGE / "02_runs" / "run314A"
SOURCE_RUN314C = SOURCE_STAGE / "02_runs" / "run314C"
SOURCE_MANIFEST = SOURCE_RUN314A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN314C / "runtime_outcome_feature_source_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN314C / "stage315_seed_queue.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN314C / "failure_memory.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run314C_review_stage315_open.md"

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
REPORT = REVIEWS / "run315A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage315/design_runtime_outcome_feature_interaction_rebuild.py")
RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = s314.DECISION_FEATURES + (
    "stage315_hour20_actual_outcome_interaction_score",
    "stage315_lowvol_midtrend_interaction_score",
    "stage315_mirror_pressure_interaction_score",
    "stage315_hour20_flag",
    "stage315_hour22_sell_release_flag",
    "stage315_hour19_21_mirror_flag",
)

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
    close_on_flat_signal: bool = False
    same_direction_reentry_cooldown_bars: int = 1
    atr_sltp_enabled: bool = True
    atr_period: int = 14
    model_risk_min_pct: float = 0.006
    model_risk_confidence_floor: float = 0.54
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            package_id="cp315A_hour20_sell_lowvol_mirror19_21_hold3_surface",
            model_surface="hour20_sell_lowvol_mirror19_21",
            target_density=5.4,
            max_hold_bars=3,
            fixed_lot=0.46,
            atr_stop_multiplier=1.06,
            atr_take_profit_multiplier=4.90,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.036,
            hypothesis="Stage314(314단계) 실제 MT5(메타트레이더5)에서 20시 sell(매도)은 검증/표본외 모두 양수였고 19/21시 sell(매도)은 손실 집중이었다. 20시 sell(매도)을 중심으로 두고 19/21시는 저변동 중간 추세에서 buy mirror(매수 반전)로 바꾸면 거래수와 수익 규모를 같이 회복할 수 있다.",
            changed_variables="시간 보정 반복이 아니라 실제 결과 기반 feature interaction(피처 상호작용)이다. 20시 sell(매도), 19/21시 buy mirror(매수 반전), 저변동/중간 추세 조건을 같이 쓴다.",
        ),
        CandidateSpec(
            package_id="cp315B_hour20_22_sell_full_mirror_hold3_surface",
            model_surface="hour20_22_sell_full_mirror",
            target_density=6.6,
            max_hold_bars=3,
            fixed_lot=0.44,
            atr_stop_multiplier=1.04,
            atr_take_profit_multiplier=4.55,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.034,
            hypothesis="20시 sell(매도)과 22시 sell release(매도 해제)는 실제 결과에서 상대적으로 나았다. 여기에 19/21시 손실 구간은 폭넓은 buy mirror(매수 반전)로 채워 4-10 trades/day(일 4-10거래)를 유지한다.",
            changed_variables="19/21시를 같은 sell(매도)로 고치지 않고, 20/22시 sell(매도)과 19/21시 buy mirror(매수 반전)를 섞은 mixed direction surface(혼합 방향 표면)로 바꾼다.",
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp315C_hour20_sell_21mirror_19guard_hold2_surface",
            model_surface="hour20_sell_21mirror_19guard",
            target_density=4.8,
            max_hold_bars=2,
            fixed_lot=0.52,
            atr_stop_multiplier=0.94,
            atr_take_profit_multiplier=3.95,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.038,
            hypothesis="21시 sell(매도) 손실이 19시보다 깊었다. 21시를 buy mirror(매수 반전)로 돌리고 19시는 강한 손실 압력일 때만 제한적으로 mirror(반전)하면 곡선 포켓을 줄일 수 있다.",
            changed_variables="21시 손실 축을 공격적으로 반전하고 19시는 guard(보호 조건)를 붙인다. hold(보유)를 2봉으로 줄여 국소 손실 포켓을 압축한다.",
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp315D_curve_guard_hour20_22_sell_mirror_release_hold2_surface",
            model_surface="curve_guard_hour20_22_sell_mirror_release",
            target_density=5.1,
            max_hold_bars=2,
            fixed_lot=0.48,
            atr_stop_multiplier=0.90,
            atr_take_profit_multiplier=3.70,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.033,
            hypothesis="순수익보다 곡선 움푹 파임을 먼저 줄이는 defensive experiment(방어형 실험)이다. 20/22시 sell(매도)을 살리고 19/21시 mirror(반전)는 저변동과 중간 RSI(상대강도지수)에서만 허용한다.",
            changed_variables="profit scale(수익 규모)을 조금 낮추더라도 curve pocket(곡선 포켓) 방어를 우선한다. 손실이 깊었던 고변동/극단 점수 구간은 flat(관망) 처리한다.",
        ),
        CandidateSpec(
            package_id="cp315E_hour20_sell_23buy_asymmetric_release_hold3_surface",
            model_surface="hour20_sell_23buy_asymmetric_release",
            target_density=5.7,
            max_hold_bars=3,
            fixed_lot=0.45,
            atr_stop_multiplier=1.02,
            atr_take_profit_multiplier=4.80,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.035,
            hypothesis="23시 buy(매수)는 거래수는 적지만 표본외 upside(상방)가 있었다. 20시 sell(매도)과 19/21시 mirror(반전)에 23시 buy release(매수 해제)를 붙이면 수익 규모 꼬리를 키울 수 있다.",
            changed_variables="새 수익 꼬리 실험이다. 23시 buy(매수)를 저충격 조건에서만 허용해 aggressive/defensive balance(공격/방어 균형)를 맞춘다.",
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp315F_aggressive_hour20_sell_inversion_convexity_hold4_surface",
            model_surface="aggressive_hour20_sell_inversion_convexity",
            target_density=7.2,
            max_hold_bars=4,
            fixed_lot=0.62,
            atr_stop_multiplier=1.22,
            atr_take_profit_multiplier=6.35,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.046,
            hypothesis="Stage314(314단계)의 factor(팩터)는 괜찮지만 순수익 규모가 약했다. 검증/표본외 공통 양수인 20시 sell(매도)을 중심으로, 19/21시를 과감히 inversion(반전)하고 보상 볼록성을 키워 scale(규모)을 압박한다.",
            changed_variables="공격형 실험이다. lot(랏), TP(익절), hold(보유)를 키우되 실패 조건은 DD(손실폭)와 curve pocket(곡선 포켓)으로 명확히 둔다.",
            same_direction_reentry_cooldown_bars=2,
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s310.rel(path)


def read_text(path: Path) -> str:
    return s310.read_text(path)


def write_text(path: Path, text: str) -> None:
    s314.write_text(path, text)


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


def signal_label(value: int) -> str:
    return s314.signal_label(value)


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    return s314.ncol(frame, column, default)


def zscore(values: np.ndarray) -> np.ndarray:
    return s314.zscore(values)


def positive(values: np.ndarray) -> np.ndarray:
    return s314.positive(values)


def quantile(values: np.ndarray, pct: float) -> float:
    return s314.quantile(values, pct)


def band(values: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return s314.band(values, lo, hi)


def risk_manifest_fields(spec: CandidateSpec) -> dict[str, Any]:
    return {
        "atr_sltp_enabled": spec.atr_sltp_enabled,
        "atr_period": spec.atr_period,
        "atr_stop_multiplier": spec.atr_stop_multiplier,
        "atr_take_profit_multiplier": spec.atr_take_profit_multiplier,
        "atr_min_stop_points": 80,
        "atr_max_stop_points": 900,
        "atr_min_take_profit_points": 120,
        "atr_max_take_profit_points": 1600,
        "exit_risk_overlay_enabled": False,
        "exit_risk_close_long_feature_index": -1,
        "exit_risk_close_short_feature_index": -1,
        "exit_risk_close_threshold": 0.0,
        "exit_risk_min_hold_bars": 1,
        "exit_risk_max_hold_feature_index": -1,
        "model_risk_sizing_enabled": spec.model_risk_sizing_enabled,
        "model_risk_min_pct": spec.model_risk_min_pct,
        "model_risk_max_pct": spec.model_risk_max_pct,
        "model_risk_confidence_floor": spec.model_risk_confidence_floor,
        "model_risk_confidence_ceiling": spec.model_risk_confidence_ceiling,
        "model_risk_fallback_lot": spec.model_risk_fallback_lot,
        "fixed_lot": spec.fixed_lot,
    }


def source_seed() -> str:
    rows = read_csv_dicts(SOURCE_SEED_QUEUE)
    if rows:
        return rows[0].get("seed_id", "stage314_runtime_outcome_feature_source_review_seed")
    return "stage314_runtime_outcome_feature_source_review_seed"


def source_manifest_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv_dicts(SOURCE_MANIFEST) if row.get("payload_path")]
    return rows[:6]


def load_sources() -> tuple[dict[str, pd.DataFrame], dict[str, str]]:
    sources: dict[str, pd.DataFrame] = {}
    packages: dict[str, str] = {}
    for index, row in enumerate(source_manifest_rows(), start=1):
        key = chr(ord("A") + index - 1)
        path = ROOT / row["payload_path"]
        frame = pd.read_parquet(s314.long_path(path))
        sources[key] = frame
        packages[key] = row["package_id"]
    if len(sources) < 6:
        raise RuntimeError(f"expected six Stage314 source payloads, found {len(sources)}")
    return sources, packages


def source_arrays(sources: Mapping[str, pd.DataFrame]) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    signals: dict[str, np.ndarray] = {}
    scores: dict[str, np.ndarray] = {}
    for key, frame in sources.items():
        signals[key] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
        scores[key] = zscore(pd.to_numeric(frame["candidate_decision_score"], errors="coerce").fillna(0.0).to_numpy(dtype="float64"))
    return signals, scores


def add_stage315_features(base: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    frame = base.copy()
    signals, scores = source_arrays(sources)
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    hour = ts.dt.hour.to_numpy()
    score_stack = np.vstack([scores[key] for key in sorted(scores)])
    signal_stack = np.vstack([signals[key] for key in sorted(signals)])
    avg_score = zscore(score_stack.mean(axis=0))
    score_spread = zscore(score_stack.max(axis=0) - score_stack.min(axis=0))
    sell_vote = (signal_stack == -1).sum(axis=0).astype("float64")
    buy_vote = (signal_stack == 1).sum(axis=0).astype("float64")
    shock = s310.s309.s308.shock_score(frame)
    quality = zscore(ncol(frame, "profit_quality_score"))
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    scale = zscore(ncol(frame, "profit_scale_score"))
    rsi = zscore(ncol(frame, "rsi_14"))
    ret = zscore(ncol(frame, "return_zscore_20"))
    vol = zscore(ncol(frame, "historical_vol_5_over_20"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.45 * zscore(ncol(frame, "di_spread_14")) + 0.30 * zscore(ncol(frame, "ppo_hist_12_26_9"))
    breadth = zscore(ncol(frame, "mega8_pos_breadth_1")) + 0.35 * zscore(ncol(frame, "top3_weighted_return_1"))
    low_vol = vol < quantile(vol, 58)
    midtrend = band(trend, 22, 78)
    mid_rsi = band(rsi, 18, 76)
    mid_breadth = band(breadth, 16, 82)
    mirror_pressure = (
        0.45 * positive(avg_score)
        + 0.35 * positive(score_spread)
        + 0.25 * positive(quality)
        + 0.20 * positive(scale)
        + 0.25 * positive(-ret)
        - 0.55 * positive(shock)
    )
    frame["stage315_hour20_actual_outcome_interaction_score"] = (
        (hour == 20).astype("float64")
        + 0.45 * low_vol.astype("float64")
        + 0.35 * midtrend.astype("float64")
        + 0.30 * mid_rsi.astype("float64")
        + 0.20 * mid_breadth.astype("float64")
        + 0.10 * sell_vote
        - 0.45 * positive(shock)
    )
    frame["stage315_lowvol_midtrend_interaction_score"] = (
        low_vol.astype("float64")
        + 0.55 * midtrend.astype("float64")
        + 0.35 * mid_rsi.astype("float64")
        + 0.30 * mid_breadth.astype("float64")
        - 0.35 * positive(shock)
    )
    frame["stage315_mirror_pressure_interaction_score"] = mirror_pressure
    frame["stage315_hour20_flag"] = (hour == 20).astype("int8")
    frame["stage315_hour22_sell_release_flag"] = ((hour == 22) & low_vol & (shock < quantile(shock, 82))).astype("int8")
    frame["stage315_hour19_21_mirror_flag"] = (np.isin(hour, [19, 21]) & (mirror_pressure > quantile(mirror_pressure, 42)) & (shock < quantile(shock, 88))).astype("int8")
    return frame


def support_arrays(frame: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> tuple[np.ndarray, np.ndarray]:
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    hour = ts.dt.hour.to_numpy()
    shock = s310.s309.s308.shock_score(frame)
    lowvol_mid = ncol(frame, "stage315_lowvol_midtrend_interaction_score")
    hour20 = hour == 20
    hour22 = (hour == 22) & (shock < quantile(shock, 84))
    mirror = (np.isin(hour, [19, 21])) & (ncol(frame, "stage315_mirror_pressure_interaction_score") > quantile(ncol(frame, "stage315_mirror_pressure_interaction_score"), 38))
    buy23 = (hour == 23) & (shock < quantile(shock, 55)) & (lowvol_mid > quantile(lowvol_mid, 58))
    signal = np.where(hour20 | hour22, -1, np.where(mirror | buy23, 1, 0)).astype("int8")
    score = (
        0.90 * hour20.astype("float64")
        + 0.62 * hour22.astype("float64")
        + 0.54 * mirror.astype("float64")
        + 0.34 * buy23.astype("float64")
        + 0.48 * lowvol_mid
        - 0.55 * positive(shock)
    )
    return signal, np.asarray(score, dtype="float64")


def transform_signal(spec: CandidateSpec, frame: pd.DataFrame, sources: Mapping[str, pd.DataFrame]) -> tuple[np.ndarray, np.ndarray]:
    support_signal, support_score = support_arrays(frame, sources)
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    hour = ts.dt.hour.to_numpy()
    shock = s310.s309.s308.shock_score(frame)
    lowvol_mid = ncol(frame, "stage315_lowvol_midtrend_interaction_score")
    hour20_score = ncol(frame, "stage315_hour20_actual_outcome_interaction_score")
    mirror_pressure = ncol(frame, "stage315_mirror_pressure_interaction_score")
    rsi = zscore(ncol(frame, "rsi_14"))
    ret = zscore(ncol(frame, "return_zscore_20"))
    vol = zscore(ncol(frame, "historical_vol_5_over_20"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.45 * zscore(ncol(frame, "di_spread_14")) + 0.30 * zscore(ncol(frame, "ppo_hist_12_26_9"))
    low_vol = vol < quantile(vol, 62)
    mid_rsi = band(rsi, 14, 80)
    pullback = ret < quantile(ret, 70)
    hour20_sell = (hour == 20) & (hour20_score > quantile(hour20_score, 26)) & (shock < quantile(shock, 90))
    hour22_sell = (hour == 22) & low_vol & (shock < quantile(shock, 82))
    mirror19 = (hour == 19) & (mirror_pressure > quantile(mirror_pressure, 46)) & low_vol & mid_rsi
    mirror21 = (hour == 21) & (mirror_pressure > quantile(mirror_pressure, 38)) & (shock < quantile(shock, 88))
    buy23 = (hour == 23) & (shock < quantile(shock, 58)) & (lowvol_mid > quantile(lowvol_mid, 62))

    if spec.model_surface == "hour20_sell_lowvol_mirror19_21":
        raw = np.where(hour20_sell | hour22_sell, -1, np.where((mirror19 | mirror21) & pullback, 1, 0)).astype("int8")
        score = 0.88 * hour20_score + 0.52 * lowvol_mid + 0.45 * mirror_pressure - 0.45 * positive(shock)
        keep = score > quantile(score, 21)
    elif spec.model_surface == "hour20_22_sell_full_mirror":
        broad_mirror = (np.isin(hour, [19, 21])) & (mirror_pressure > quantile(mirror_pressure, 30)) & (shock < quantile(shock, 92))
        raw = np.where(hour20_sell | hour22_sell, -1, np.where(broad_mirror, 1, 0)).astype("int8")
        score = 0.75 * hour20_score + 0.58 * broad_mirror.astype("float64") + 0.42 * lowvol_mid - 0.38 * positive(shock)
        keep = score > quantile(score, 18)
    elif spec.model_surface == "hour20_sell_21mirror_19guard":
        guarded19 = mirror19 & (trend < quantile(trend, 70))
        raw = np.where(hour20_sell | hour22_sell, -1, np.where(mirror21 | guarded19, 1, 0)).astype("int8")
        score = 0.84 * hour20_score + 0.70 * mirror21.astype("float64") + 0.32 * guarded19.astype("float64") - 0.42 * positive(shock)
        keep = score > quantile(score, 24)
    elif spec.model_surface == "curve_guard_hour20_22_sell_mirror_release":
        guarded_mirror = (mirror19 | mirror21) & low_vol & mid_rsi & (shock < quantile(shock, 74))
        raw = np.where((hour20_sell | hour22_sell) & low_vol, -1, np.where(guarded_mirror, 1, 0)).astype("int8")
        score = 0.90 * hour20_score + 0.62 * lowvol_mid + 0.24 * guarded_mirror.astype("float64") - 0.70 * positive(shock)
        keep = score > quantile(score, 25)
    elif spec.model_surface == "hour20_sell_23buy_asymmetric_release":
        raw = np.where(hour20_sell | hour22_sell, -1, np.where(mirror19 | mirror21 | buy23, 1, 0)).astype("int8")
        score = 0.78 * hour20_score + 0.46 * mirror_pressure + 0.42 * buy23.astype("float64") + 0.30 * lowvol_mid - 0.42 * positive(shock)
        keep = score > quantile(score, 20)
    elif spec.model_surface == "aggressive_hour20_sell_inversion_convexity":
        aggressive_mirror = (np.isin(hour, [19, 21])) & (mirror_pressure > quantile(mirror_pressure, 24)) & (shock < quantile(shock, 94))
        raw = np.where(hour20_sell | hour22_sell, -1, np.where(aggressive_mirror | buy23, 1, 0)).astype("int8")
        score = 0.72 * hour20_score + 0.66 * aggressive_mirror.astype("float64") + 0.40 * lowvol_mid + 0.20 * positive(-ret) - 0.32 * positive(shock)
        keep = score > quantile(score, 16)
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


def materialize_payload(
    spec: CandidateSpec,
    sources: Mapping[str, pd.DataFrame],
    source_packages: Mapping[str, str],
    seed_id: str,
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = transform_signal(spec, frame, sources)
    branch_id = f"run315A_{spec.package_id.replace('_surface', '')}"
    payload = sources["A"].copy()
    payload["stage315_branch_id"] = branch_id
    payload["stage314_seed_id"] = seed_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "runtime_outcome_feature_interaction_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = ";".join(source_packages[key] for key in sorted(source_packages))
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
        "source_packages": dict(source_packages),
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
    sources, source_packages = load_sources()
    frame = add_stage315_features(sources["A"], sources)
    seed_id = source_seed()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, sources, source_packages, seed_id, frame)
        branch_id = f"run315A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_feature_interaction_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(s314.long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage315_branch_id": branch_id,
                "stage314_seed_id": seed_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage315 MT5 probe(315단계 MT5 탐침)",
                "claim_boundary": BOUNDARY,
            },
        )
        candidate_supply = s310.supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        density_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s310.s309.s308.s307.prev.s290.selection_score(validation_metrics)
            + s310.s309.s308.s307.prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.45
            + min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])) * 55.0
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
                "decision_use": "MT5 runtime probe(MT5 런타임 탐침) 대상 후보인지 판단한다.",
                "comparison_baseline": "Stage314 no-selection(314단계 선택 없음) and Stage314 actual hour outcome attribution(314단계 실제 시간별 결과 귀속).",
                "control_variables": "US100 M5, split_v1(분할 v1), Tier A/B paired accounting(티어 A/B 쌍 기록), Stage314 source payloads(314단계 원천 페이로드).",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리) and MT5 runtime probe(MT5 런타임 탐침).",
                "success_criteria": "actual MT5 validation/OOS positive(검증/표본외 양수), minimum trade count(최소 거래수), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), smooth curve(매끄러운 곡선).",
                "failure_criteria": "validation loss(검증 손실), OOS loss(표본외 손실), density outside 4-10(거래 밀도 이탈), weak scale(약한 규모), deep curve pocket(깊은 곡선 포켓).",
                "invalid_conditions": "source payload mismatch(원천 페이로드 불일치), feature order mismatch(피처 순서 불일치), MT5 report parse missing(MT5 보고서 파싱 누락).",
                "stop_conditions": "candidate gate pass(후보 관문 통과) -> Adapter(어댑터); all fail(전체 실패) -> next fresh thesis(다음 새 논제).",
                "evidence_plan": "branch queue(분기 대기열), proxy scoreboard(대리 점수판), payload manifest(페이로드 목록), MT5 queue(MT5 대기열), run315B/run315C.",
                "feature_surface": "Stage314 actual outcome hour clue(314단계 실제 시간 단서), hour20 sell(20시 매도), hour19/21 mirror(19/21시 반전), low volatility/mid trend interaction(저변동/중간 추세 상호작용).",
                "model_surface": "rule_surface_runtime_outcome_feature_interaction",
                "decision_surface": spec.model_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생); Adapter trace(어댑터 추적)는 후보 관문 후 시작한다.",
                "failure_memory_plan": "hour20 edge(20시 거래우위), mirror failure(반전 실패), density(밀도), profit scale(수익 규모), curve pocket(곡선 포켓)을 분리 기록한다.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run315A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": str(payload.get("stage309_branch_id", pd.Series([""])).iloc[0]) if "stage309_branch_id" in payload else "",
                "stage308_branch_id": str(payload.get("stage308_branch_id", pd.Series([""])).iloc[0]) if "stage308_branch_id" in payload else "",
                "stage307_branch_id": str(payload.get("stage307_branch_id", pd.Series([""])).iloc[0]) if "stage307_branch_id" in payload else "",
                "stage306_branch_id": str(payload.get("stage306_branch_id", pd.Series([""])).iloc[0]) if "stage306_branch_id" in payload else "",
                "package_id": spec.package_id,
                "queue_role": "runtime_outcome_feature_interaction_surface",
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
                "model_family": "runtime_outcome_feature_interaction_rule_surface",
                "prediction_kind": "runtime_direction_interaction",
                "dataset_id": "stage314_runtime_outcome_feature_source_actual_hour_attribution",
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
                "model_family": "runtime_outcome_feature_interaction_rule_surface",
                "prediction_kind": "runtime_direction_interaction",
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
            "user_explanation_hook": "20시 sell(매도) 양수 단서와 19/21시 손실 반전을 실제 MT5(메타트레이더5)로 압박한다.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "hour20 edge(20시 거래우위)와 mirror interaction(반전 상호작용)으로 질문을 바꿨다."},
        {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
        {"gate_name": "density_proxy(밀도 대리)", "status": "passed" if density_pass else "failed", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day(일 4-10거래) 대리 조건을 확인했다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "MT5 review(MT5 검토) 전에는 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "후보 선택 전에는 ONNX(온엑스)를 시작하지 않는다."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run315A Runtime Outcome Feature Interaction Materialization(315A 런타임 결과 피처 상호작용 물질화)",
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
        "Effect(효과): Stage314(314단계)의 약한 순수익을 그대로 repair(수리)하지 않고, 실제 MT5(메타트레이더5) 시간별 결과에서 20시 sell(매도) 양수 단서와 19/21시 손실 반전 단서를 feature interaction(피처 상호작용) 후보로 물질화했다.",
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
            "hypothesis": "Stage314(314단계) 실제 MT5(메타트레이더5)에서는 20시 sell(매도)이 공통 양수이고 19/21시 sell(매도)이 손실 포켓이었다. 시간 자체가 아니라 hour/outcome feature interaction(시간/결과 피처 상호작용)으로 방향을 바꾸면 trade count(거래 수), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), curve quality(곡선 품질)을 동시에 개선할 수 있다.",
            "decision_use": "run315B MT5 runtime probe(MT5 런타임 탐침) 대상을 만든다.",
            "comparison_baseline": "Stage314 no-selection(314단계 선택 없음) and Stage314 actual MT5 hour attribution(실제 MT5 시간별 귀속).",
            "control_variables": ["US100 M5", "split_v1", "Stage314 source payloads(314단계 원천 페이로드)", "Tier A/B paired accounting(티어 A/B 쌍 기록)"],
            "changed_variables": ["hour20 sell edge(20시 매도 거래우위)", "hour19/21 mirror(19/21시 반전)", "low-vol mid-trend interaction(저변동 중간 추세 상호작용)", "risk/reward convexity(위험/보상 볼록성)"],
            "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리), then MT5 runtime probe(MT5 런타임 탐침).",
            "success_criteria": ["actual MT5 validation/OOS net positive(검증/표본외 순수익 양수)", "minimum trade count(최소 거래수)", "4-10 trades/day(일 4-10거래)", "profit scale(수익 규모)", "smooth rising curve(꾸준한 우상향 곡선)"],
            "failure_criteria": ["weak net profit(약한 순수익)", "PF/recovery/expectancy weak(수익 팩터/회복/기대값 약함)", "deep curve pocket(깊은 곡선 포켓)", "density outside 4-10(밀도 이탈)"],
            "invalid_conditions": ["source payload alignment failure(원천 페이로드 정렬 실패)", "feature order mismatch(피처 순서 불일치)", "MT5 report missing(MT5 보고서 누락)"],
            "stop_conditions": ["candidate gate pass(후보 관문 통과) -> Adapter(어댑터)", "all fail(전체 실패) -> new stage fresh thesis(새 단계 새 논제)"],
            "evidence_plan": [rel(BRANCH_QUEUE), rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run315B MT5 KPI", "run315C review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_seed_queue": rel(SOURCE_SEED_QUEUE),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY),
            "decision_feature_count": len(DECISION_FEATURES),
            "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
            "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts = [rel(path) for path in payload_artifacts] + [
        rel(path)
        for path in (
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
        )
    ]
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
            "artifacts": artifacts,
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
            "artifact_paths": artifacts,
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
    safe_upsert(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_outcome_feature_interaction_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};selected_candidate=none;next_action={NEXT_ACTION}."}], "run_id")
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
                "record_view": "runtime_outcome_feature_interaction_materialization",
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
    safe_upsert(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "runtime_outcome_feature_interaction_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")
    artifact_rows = []
    for path in artifacts:
        if not s310.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage315_runtime_outcome_feature_interaction_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "Stage315 design/materialization artifact",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run315A_report", f"- run315A_report(315A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run315A_mt5_queue", f"- run315A_mt5_queue(315A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = append_once(review_index, "run315A_report", f"- run315A_report(315A 보고서): `{rel(REPORT)}`\n- run315A_scoreboard(315A 점수판): `{rel(MODEL_SCOREBOARD)}`\n- run315A_mt5_queue(315A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run315A_summary", f"- run315A_summary(315A 요약): runtime outcome feature interaction(런타임 결과 피처 상호작용) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): 20시 sell(매도) 양수 단서와 19/21시 mirror(반전)를 결합한 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.")
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage315(315단계) run315A(315A 실행) runtime outcome feature interaction materialization(런타임 결과 피처 상호작용 물질화) `{RUN_ID}`. "
        f"Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += (
            f"\n## {UPDATED_ON} run315A Runtime outcome feature interaction materialization(315A 런타임 결과 피처 상호작용 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): 후보 `{len(scoreboard_rows)}`개와 MT5 대기열 `{len(manifest_rows)}`개를 만들었다.\n"
            "- boundary(경계): 선택 후보, Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 없다.\n"
        )
    write_text(CHANGELOG, changelog)

    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} runtime_outcome_feature_interaction(런타임 결과 피처 상호작용)\n\n"
            "- idea_id(아이디어 ID): `stage315_runtime_outcome_feature_interaction`\n"
            "- hypothesis(가설): actual hour outcome(실제 시간별 결과)과 feature interaction(피처 상호작용)을 결합하면 trade density(거래 밀도)와 profit scale(수익 규모)을 같이 회복할 수 있다.\n"
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
