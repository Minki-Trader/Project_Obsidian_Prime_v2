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
from stage_pipelines.stage316 import design_post_interaction_profit_scale_curve_rebuild as s316  # noqa: E402


s310 = s316.s310

STAGE_ID = "317_onnx_candidate_campaign__fresh_non_time_profit_source_rebuild"
RUN_ID = "run317A_design_fresh_non_time_profit_source_rebuild_packet_v1"
RUN_NUMBER = "run317A"
SOURCE_STAGE_ID = "316_onnx_candidate_campaign__post_interaction_profit_scale_curve_rebuild"
SOURCE_RUN_ID = "run316C_review_post_interaction_profit_scale_curve_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_fresh_non_time_profit_source_candidates_materialized_no_selection"
JUDGMENT = "fresh_non_time_profit_source_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run317B_execute_fresh_non_time_profit_source_mt5_probe"
BOUNDARY = s316.BOUNDARY

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
SOURCE_RUN316A = SOURCE_STAGE / "02_runs" / "run316A"
SOURCE_RUN316C = SOURCE_STAGE / "02_runs" / "run316C"
SOURCE_MANIFEST = SOURCE_RUN316A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN316C / "post_interaction_profit_scale_curve_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN316C / "stage317_seed_queue.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN316C / "failure_memory.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run316C_review_stage317_open.md"

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
REPORT = REVIEWS / "run317A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage317/design_fresh_non_time_profit_source_rebuild.py")
RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = s316.DECISION_FEATURES + (
    "stage317_adx_short_score",
    "stage317_usdx_extreme_score",
    "stage317_momentum_breadth_score",
    "stage317_quality_scale_score",
    "stage317_bollinger_extreme_score",
    "stage317_hybrid_router_score",
    "stage317_non_time_source_flag",
)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    model_surface: str
    target_density: float
    max_hold_bars: int
    fixed_lot: float
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_max_pct: float
    hypothesis: str
    changed_variables: str
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    atr_sltp_enabled: bool = True
    atr_period: int = 14
    model_risk_sizing_enabled: bool = True
    model_risk_min_pct: float = 0.006
    model_risk_confidence_floor: float = 0.54
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            "cp317A_usdx_extreme_follow_hold1_dense_surface",
            "usdx_extreme_follow_hold1_dense",
            9.0,
            1,
            0.62,
            0.78,
            3.35,
            0.040,
            "USDX extreme follow(달러지수 극단 추종) surface(표면)는 시간 조건 없이 달러 강세/약세 극단을 방향 신호로 쓴다.",
            "hour bucket(시간 묶음)을 제거하고 USDX z-score(달러지수 표준점수) 극단을 long/short(매수/매도) 라우터로 바꾼다.",
        ),
        CandidateSpec(
            "cp317B_usdx_extreme_follow_hold2_scale_surface",
            "usdx_extreme_follow_hold2_scale",
            7.8,
            2,
            0.68,
            0.86,
            4.10,
            0.045,
            "USDX extreme follow(달러지수 극단 추종)를 hold2(2봉 보유)와 높은 reward(보상)로 키워 profit scale(수익 규모)을 압박한다.",
            "동일한 비시간 원천을 risk/reward(위험/보상)와 hold(보유)만 달리해 공격형으로 시험한다.",
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            "cp317C_adx_high_short_hold1_defensive_surface",
            "adx_high_short_hold1_defensive",
            4.8,
            1,
            0.48,
            0.72,
            2.95,
            0.030,
            "ADX high short(ADX 높음 매도)는 강한 추세/확장 국면의 short continuation(매도 지속) 단서가 양 split(분할)에서 보였는지 확인한다.",
            "방어형 surface(표면)로 거래 밀도 하단을 맞추고 DD(drawdown, 손실폭)를 낮춘다.",
        ),
        CandidateSpec(
            "cp317D_momentum_breadth_long_hold1_surface",
            "momentum_breadth_long_hold1",
            6.2,
            1,
            0.56,
            0.76,
            3.45,
            0.036,
            "3-bar momentum(3봉 모멘텀), PPO histogram(PPO 히스토그램), mega-cap breadth(대형주 폭)가 같이 양수일 때 long(매수)만 취한다.",
            "수익 규모가 큰 long-only(매수 전용) 공격형 단서를 OOS(표본외) 약화 조건과 함께 시험한다.",
        ),
        CandidateSpec(
            "cp317E_bollinger_position_extreme_hold1_surface",
            "bollinger_position_extreme_hold1",
            4.8,
            1,
            0.52,
            0.74,
            3.05,
            0.033,
            "Bollinger position extreme(볼린저 위치 극단)은 price position(가격 위치)과 return z-score(수익률 표준점수)를 섞어 양방향 평균회귀/추종을 본다.",
            "시간 조건 대신 가격 위치 극단만으로 4-10 trades/day(일 4-10거래)를 맞춘다.",
        ),
        CandidateSpec(
            "cp317F_usdx_adx_hybrid_router_hold1_surface",
            "usdx_adx_hybrid_router_hold1",
            6.8,
            1,
            0.64,
            0.80,
            3.80,
            0.042,
            "USDX extreme(달러지수 극단)을 우선하고, 빈 구간은 ADX high short(ADX 높음 매도)로 채우는 hybrid router(혼합 라우터)다.",
            "비시간 원천 두 개를 우선순위 라우터로 결합해 scale(규모)와 density(밀도)를 동시에 본다.",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s310.rel(path)


def read_text(path: Path) -> str:
    return s310.read_text(path)


def write_text(path: Path, text: str) -> None:
    s316.write_text(path, text)


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


def zscore(values: np.ndarray) -> np.ndarray:
    return s316.zscore(values)


def positive(values: np.ndarray) -> np.ndarray:
    return s316.positive(values)


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    return s316.ncol(frame, column, default)


def quantile(values: np.ndarray, pct: float) -> float:
    return s316.quantile(values, pct)


def signal_label(value: int) -> str:
    return s316.signal_label(value)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return s310.replace_line_prefix(text, prefix, replacement)


def append_once(text: str, marker: str, addition: str) -> str:
    return s310.append_once(text, marker, addition)


def prepend_focus(text: str, focus: str, marker: str) -> str:
    return s310.prepend_focus(text, focus, marker)


def risk_manifest_fields(spec: CandidateSpec) -> dict[str, Any]:
    return {
        "atr_sltp_enabled": spec.atr_sltp_enabled,
        "atr_period": spec.atr_period,
        "atr_stop_multiplier": spec.atr_stop_multiplier,
        "atr_take_profit_multiplier": spec.atr_take_profit_multiplier,
        "atr_min_stop_points": 70,
        "atr_max_stop_points": 900,
        "atr_min_take_profit_points": 100,
        "atr_max_take_profit_points": 1800,
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
        return rows[0].get("seed_id", "stage316_post_interaction_profit_scale_curve_review_seed")
    return "stage316_post_interaction_profit_scale_curve_review_seed"


def source_manifest_rows() -> list[dict[str, str]]:
    return [row for row in read_csv_dicts(SOURCE_MANIFEST) if row.get("payload_path")][:6]


def load_source_frame() -> pd.DataFrame:
    rows = source_manifest_rows()
    if not rows:
        raise RuntimeError("missing Stage316 source manifest rows")
    return pd.read_parquet(s316.s315.s314.long_path(ROOT / rows[0]["payload_path"]))


def feature_arrays(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    shock = s310.s309.s308.shock_score(frame)
    top3 = zscore(ncol(frame, "top3_weighted_return_1"))
    breadth = zscore(ncol(frame, "mega8_pos_breadth_1")) + 0.35 * top3
    return {
        "shock": shock,
        "adx": zscore(ncol(frame, "adx_14")),
        "usdx": zscore(ncol(frame, "usdx_zscore_20")),
        "log3": zscore(ncol(frame, "log_return_3")),
        "ppo": zscore(ncol(frame, "ppo_hist_12_26_9")),
        "top3": top3,
        "breadth": breadth,
        "bb": zscore(ncol(frame, "bb_position_20")),
        "ret": zscore(ncol(frame, "return_zscore_20")),
        "edge": zscore(ncol(frame, "payoff_edge_score")),
        "cal": zscore(ncol(frame, "runtime_calibration_score")),
        "atr": zscore(ncol(frame, "atr_14_over_atr_50")),
        "pq": zscore(ncol(frame, "profit_quality_score")),
        "ps": zscore(ncol(frame, "profit_scale_score")),
        "smooth": zscore(ncol(frame, "smooth_curve_score")),
    }


def add_stage317_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    arr = feature_arrays(out)
    shock = arr["shock"]
    out["stage317_adx_short_score"] = arr["adx"] + 0.25 * arr["atr"] - 0.20 * positive(shock) + 0.15 * arr["cal"]
    out["stage317_usdx_extreme_score"] = np.abs(arr["usdx"]) + 0.20 * arr["edge"] + 0.15 * arr["cal"] - 0.20 * positive(shock)
    out["stage317_momentum_breadth_score"] = arr["log3"] + 0.35 * arr["ppo"] + 0.25 * arr["top3"] + 0.20 * arr["breadth"] - 0.20 * positive(shock)
    out["stage317_quality_scale_score"] = arr["pq"] + 0.50 * arr["ps"] + 0.35 * arr["smooth"] + 0.25 * arr["edge"] - 0.25 * positive(shock)
    out["stage317_bollinger_extreme_score"] = np.abs(arr["bb"]) + 0.25 * np.abs(arr["ret"]) + 0.25 * arr["edge"] - 0.20 * positive(shock)
    out["stage317_hybrid_router_score"] = 0.70 * out["stage317_usdx_extreme_score"] + 0.30 * out["stage317_adx_short_score"]
    out["stage317_non_time_source_flag"] = 1
    return out


def usdx_arrays(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    arr = feature_arrays(frame)
    usdx = arr["usdx"]
    score = ncol(frame, "stage317_usdx_extreme_score")
    raw = np.where(usdx > quantile(usdx, 78), 1, np.where(usdx < quantile(usdx, 22), -1, 0)).astype("int8")
    support = np.where(usdx > quantile(usdx, 56), 1, np.where(usdx < quantile(usdx, 44), -1, 0)).astype("int8")
    return raw, score, support, score + 0.25 * np.abs(usdx)


def adx_arrays(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    arr = feature_arrays(frame)
    adx = arr["adx"]
    shock = arr["shock"]
    safe = shock < quantile(shock, 86)
    score = ncol(frame, "stage317_adx_short_score")
    raw = np.where((adx > quantile(adx, 82)) & safe, -1, 0).astype("int8")
    support = np.where(adx > quantile(adx, 68), -1, 0).astype("int8")
    return raw, score, support, score + 0.25 * np.abs(adx)


def transform_signal(spec: CandidateSpec, frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    arr = feature_arrays(frame)
    if spec.model_surface in {"usdx_extreme_follow_hold1_dense", "usdx_extreme_follow_hold2_scale"}:
        raw, score, support, support_score = usdx_arrays(frame)
    elif spec.model_surface == "adx_high_short_hold1_defensive":
        raw, score, support, support_score = adx_arrays(frame)
    elif spec.model_surface == "momentum_breadth_long_hold1":
        score = ncol(frame, "stage317_momentum_breadth_score")
        raw = np.where((arr["log3"] > quantile(arr["log3"], 78)) & (arr["ppo"] > quantile(arr["ppo"], 60)) & (arr["top3"] > quantile(arr["top3"], 55)), 1, 0).astype("int8")
        support = np.where((arr["log3"] > quantile(arr["log3"], 55)) & (arr["breadth"] > quantile(arr["breadth"], 50)), 1, 0).astype("int8")
        support_score = score + 0.25 * np.abs(arr["log3"])
    elif spec.model_surface == "bollinger_position_extreme_hold1":
        score = ncol(frame, "stage317_bollinger_extreme_score")
        raw = np.where((arr["bb"] > quantile(arr["bb"], 82)) & (arr["ret"] > quantile(arr["ret"], 55)), 1, np.where((arr["bb"] < quantile(arr["bb"], 18)) & (arr["ret"] < quantile(arr["ret"], 45)), -1, 0)).astype("int8")
        support = np.where(arr["bb"] > quantile(arr["bb"], 55), 1, np.where(arr["bb"] < quantile(arr["bb"], 45), -1, 0)).astype("int8")
        support_score = score + 0.25 * np.abs(arr["bb"])
    elif spec.model_surface == "usdx_adx_hybrid_router_hold1":
        raw_b, score_b, support_b, support_score_b = usdx_arrays(frame)
        raw_a, score_a, support_a, support_score_a = adx_arrays(frame)
        raw = np.where(raw_b != 0, raw_b, raw_a).astype("int8")
        support = np.where(support_b != 0, support_b, support_a).astype("int8")
        score = 0.70 * score_b + 0.30 * score_a
        support_score = 0.70 * support_score_b + 0.30 * support_score_a
    else:
        raise ValueError(f"unsupported model surface: {spec.model_surface}")
    signal = s310.density_fit(frame, raw, score, support, support_score, hold_bars=spec.max_hold_bars, target_density=spec.target_density)
    return signal.astype("int8"), np.asarray(score, dtype="float64")


def materialize_payload(spec: CandidateSpec, frame: pd.DataFrame, seed_id: str) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = transform_signal(spec, frame)
    branch_id = f"run317A_{spec.package_id.replace('_surface', '')}"
    payload = frame.copy()
    payload["stage317_branch_id"] = branch_id
    payload["stage316_seed_id"] = seed_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "fresh_non_time_profit_source_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = "stage316_failure_memory_non_time_rebuild"
    payload["source_transform_id"] = spec.model_surface
    payload["source_active_mask"] = (pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy() != 0).astype("int8")
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_seed_id": seed_id,
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
    return payload.drop(columns=drop_columns, errors="ignore"), identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    frame = add_stage317_features(load_source_frame())
    seed_id = source_seed()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, frame, seed_id)
        branch_id = f"run317A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_fresh_non_time_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(s316.s315.s314.long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "package_id": spec.package_id,
                "materialized_branch_id": branch_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage317 MT5 probe(317단계 MT5 탐침)",
                "claim_boundary": BOUNDARY,
            },
        )
        candidate_supply = s310.supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        density_gate = "passed" if 4.0 <= float(validation_metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0 else "failed"
        edge_gate = "passed" if float(validation_metrics["net_bp"]) > 0.0 and float(oos_metrics["net_bp"]) > 0.0 and float(validation_metrics["pf"]) >= 1.01 and float(oos_metrics["pf"]) >= 1.01 else "failed"
        curve_gate = "passed" if float(validation_metrics["worst_rolling_20_bp"]) >= -2400.0 and float(oos_metrics["worst_rolling_20_bp"]) >= -1200.0 else "failed"
        selection_score = (
            s310.s309.s308.s307.prev.s290.selection_score(validation_metrics)
            + s310.s309.s308.s307.prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])) * 70.0
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 2.0
            - max(0.0, -float(validation_metrics["worst_rolling_20_bp"])) * 0.20
            - max(0.0, -float(oos_metrics["worst_rolling_20_bp"])) * 0.20
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe(MT5 런타임 탐침) 전 후보인지 판단한다.",
                "comparison_baseline": "Stage316 no-selection(316단계 선택 없음) and non-time vector scan(비시간 벡터 스캔).",
                "control_variables": "US100 M5, split_v1(분할 v1), Tier A/B paired accounting(티어 A/B 쌍 기록), no hour bucket(시간 묶음 없음).",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리) and MT5 runtime probe(MT5 런타임 탐침).",
                "success_criteria": "actual MT5 validation/OOS positive(검증/표본외 양수), minimum trade count(최소 거래수), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), smooth curve(매끄러운 곡선).",
                "failure_criteria": "loss(손실), density outside 4-10(밀도 이탈), weak scale(약한 규모), deep curve pocket(깊은 곡선 포켓).",
                "invalid_conditions": "payload mismatch(페이로드 불일치), feature order mismatch(피처 순서 불일치), MT5 report parse missing(MT5 보고서 파싱 누락).",
                "stop_conditions": "candidate gate pass(후보 관문 통과) -> Adapter(어댑터); all fail(전체 실패) -> next fresh thesis(다음 새 논제).",
                "evidence_plan": "branch queue(분기 대기열), proxy scoreboard(대리 점수표), MT5 queue(MT5 대기열), run317B/run317C.",
                "feature_surface": "non-time state features(비시간 상태 피처): USDX, ADX, momentum, breadth, Bollinger.",
                "model_surface": "rule_surface_fresh_non_time_profit_source",
                "decision_surface": spec.model_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생); Adapter trace(어댑터 추적)는 후보 관문 후 시작한다.",
                "failure_memory_plan": "non-time source(비시간 원천), profit scale(수익 규모), curve pocket(곡선 포켓)을 분리 기록한다.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run317A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": str(payload.get("stage309_branch_id", pd.Series([""])).iloc[0]) if "stage309_branch_id" in payload else "",
                "stage308_branch_id": str(payload.get("stage308_branch_id", pd.Series([""])).iloc[0]) if "stage308_branch_id" in payload else "",
                "stage307_branch_id": str(payload.get("stage307_branch_id", pd.Series([""])).iloc[0]) if "stage307_branch_id" in payload else "",
                "stage306_branch_id": str(payload.get("stage306_branch_id", pd.Series([""])).iloc[0]) if "stage306_branch_id" in payload else "",
                "package_id": spec.package_id,
                "queue_role": "fresh_non_time_profit_source_surface",
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
                "model_family": "fresh_non_time_profit_source_rule_surface",
                "prediction_kind": "runtime_direction_non_time_state_router",
                "dataset_id": "stage316_failure_memory_plus_non_time_vector_scan",
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
                "model_family": "fresh_non_time_profit_source_rule_surface",
                "prediction_kind": "runtime_direction_non_time_state_router",
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


def write_outputs(branch_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]], supply_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], model_rows: Sequence[Mapping[str, Any]], wfo_rows: Sequence[Mapping[str, Any]], payload_artifacts: Sequence[Path]) -> list[Path]:
    write_csv(BRANCH_QUEUE, s310.BRANCH_COLUMNS, branch_rows)
    write_csv(MODEL_SCOREBOARD, s310.SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, s310.SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, s310.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, s310.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, s310.MODEL_COLUMNS, model_rows)
    write_csv(WFO_FOLD_SCOREBOARD, s310.WFO_COLUMNS, wfo_rows)
    write_csv(
        RESULT_JUDGMENT,
        s310.RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}",
                "evidence_missing": "actual MT5 KPI(실제 MT5 핵심 성과 지표);Adapter(어댑터);ONNX(온엑스)",
                "judgment_label": JUDGMENT,
                "judgment_class": "exploratory_materialization(탐색 물질화)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "시간 축을 버리고 USDX/ADX/momentum/Bollinger(달러지수/ADX/모멘텀/볼린저) 비시간 원천을 MT5(메타트레이더5)로 압박한다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        s310.GATE_COLUMNS,
        [
            {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "hour-only repair(시간 전용 수리)를 버리고 non-time source(비시간 원천)를 만들었다."},
            {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
            {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "MT5 review(MT5 검토) 전에는 Adapter(어댑터)를 만들지 않는다."},
            {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "후보 선택 전에는 ONNX(온엑스)를 시작하지 않는다."},
        ],
    )
    write_json(EXPERIMENT_DESIGN, {"hypothesis": "non-time profit source(비시간 수익 원천)가 최소 거래수, 4-10 trades/day(일 4-10거래), profit scale(수익 규모), curve quality(곡선 품질)를 같이 만족할 수 있는지 본다.", "decision_use": NEXT_ACTION, "comparison_baseline": "Stage316 no-selection(316단계 선택 없음)", "control_variables": ["US100 M5", "split_v1", "no hour bucket(시간 묶음 없음)"], "changed_variables": ["USDX/ADX/momentum/Bollinger state(달러지수/ADX/모멘텀/볼린저 상태)", "risk/reward scale(위험/보상 규모)"], "success_criteria": ["actual MT5 validation/OOS positive(검증/표본외 양수)", "4-10 trades/day(일 4-10거래)", "smooth curve(매끄러운 곡선)"], "failure_criteria": ["loss(손실)", "density out of range(밀도 이탈)", "deep curve pocket(깊은 곡선 포켓)"], "claim_boundary": BOUNDARY})
    write_json(DATA_RECEIPT, {"source_manifest": rel(SOURCE_MANIFEST), "source_scoreboard": rel(SOURCE_SCOREBOARD), "source_seed_queue": rel(SOURCE_SEED_QUEUE), "source_failure_memory": rel(SOURCE_FAILURE_MEMORY), "model_feature_order_hash": ordered_hash(DECISION_FEATURES), "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER), "claim_boundary": BOUNDARY})
    artifacts = [rel(path) for path in payload_artifacts] + [rel(path) for path in (BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "candidate_count": len(scoreboard_rows), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "artifacts": artifacts, "claim_boundary": BOUNDARY})
    write_json(LINEAGE, {"run_id": RUN_ID, "producer": str(PRODUCER), "source_inputs": [rel(SOURCE_MANIFEST), rel(SOURCE_SCOREBOARD), rel(SOURCE_SEED_QUEUE), rel(SOURCE_FAILURE_MEMORY), rel(SOURCE_REVIEW)], "consumer": NEXT_ACTION, "artifact_paths": artifacts, "availability": "tracked_manifest_plus_payloads", "lineage_judgment": "connected_with_boundary", "claim_boundary": BOUNDARY})
    write_text(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return list(payload_artifacts) + [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run317A Fresh Non-Time Profit Source Materialization(317A 비시간 수익 원천 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidates(후보): `{len(scoreboard_rows)}`",
        f"- MT5 queue rows(MT5 대기열 행): `{len(manifest_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage316(316단계)의 시간 기반 실패를 버리고 USDX/ADX/momentum/Bollinger(달러지수/ADX/모멘텀/볼린저) 비시간 feature surface(피처 표면)를 MT5(메타트레이더5) 압박 대상으로 만들었다.",
        "",
        "| package(패키지) | val bp(검증 bp) | val PF(검증 수익 팩터) | OOS bp(표본외 bp) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | gates(관문) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        gates = ",".join(name for name, key in (("density", "density_gate"), ("edge", "proxy_edge_gate"), ("curve", "curve_proxy_gate")) if row[key] != "passed") or "passed"
        lines.append(f"| {row['package_id']} | {float(row['validation_proxy_net_bp']):.2f} | {float(row['validation_proxy_pf']):.2f} | {float(row['oos_proxy_net_bp']):.2f} | {float(row['oos_proxy_pf']):.2f} | {float(row['validation_proxy_trades_per_day']):.2f}/{float(row['oos_proxy_trades_per_day']):.2f} | {gates} |")
    lines.extend(["", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    safe_upsert(RUN_REGISTRY, s310.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "fresh_non_time_profit_source_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};selected_candidate=none;next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, s310.s309.s308.s307.prev.s290.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "fresh_non_time_profit_source_materialization", "tier_scope": "Tier A separate/Tier B separate/Tier A+B routed preparation", "kpi_scope": "proxy_plus_mt5_queue", "scoreboard_lane": "onnx_candidate_campaign", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}", "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started", "external_verification_status": "prepared_not_executed", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, s310.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "fresh_non_time_profit_source_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")
    rows = []
    for path in artifacts:
        if not s310.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append({"artifact_id": f"{RUN_ID}__{artifact_id}", "artifact_type": "stage317_fresh_non_time_profit_source_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "Stage317 design/materialization artifact"})
    safe_upsert(ARTIFACT_REGISTRY, s310.ARTIFACT_COLUMNS, rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = replace_line_prefix(read_text(SELECTED), "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run317A_report", f"- run317A_report(317A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run317A_mt5_queue", f"- run317A_mt5_queue(317A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)
    review_index = append_once(read_text(REVIEW_INDEX), "run317A_report", f"- run317A_report(317A 보고서): `{rel(REPORT)}`\n- run317A_scoreboard(317A 점수표): `{rel(MODEL_SCOREBOARD)}`\n- run317A_mt5_queue(317A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)
    current = replace_line_prefix(read_text(CURRENT_STATE), "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run317A_summary", f"- run317A_summary(317A 요약): fresh non-time profit source(새 비시간 수익 원천) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): USDX/ADX/momentum/Bollinger(달러지수/ADX/모멘텀/볼린저) MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.")
    write_text(CURRENT_STATE, current)
    workspace = replace_line_prefix(read_text(WORKSPACE_STATE), "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage317(317단계) run317A(317A 실행) fresh non-time profit source materialization(새 비시간 수익 원천 물질화) `{RUN_ID}`. Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run317A Fresh non-time profit source materialization(317A 새 비시간 수익 원천 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): 후보 `{len(scoreboard_rows)}`개와 MT5 대기열 `{len(manifest_rows)}`개를 만들었다.\n- boundary(경계): 선택 후보, Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 없다.\n"
    write_text(CHANGELOG, changelog)
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += f"\n## {RUN_ID} fresh_non_time_profit_source(새 비시간 수익 원천)\n\n- idea_id(아이디어 ID): `stage317_fresh_non_time_profit_source`\n- hypothesis(가설): 시간 조건 없이 USDX/ADX/momentum/Bollinger(달러지수/ADX/모멘텀/볼린저) 상태 조합이 거래수와 수익 규모를 같이 만들 수 있다.\n- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        write_text(IDEA_REGISTER, idea)


def main() -> None:
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts)
    update_registers(scoreboard_rows, manifest_rows, artifacts, utc_now())
    update_docs(scoreboard_rows, manifest_rows)
    print(json.dumps({"status": STATUS, "judgment": JUDGMENT, "candidate_rows": len(scoreboard_rows), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
