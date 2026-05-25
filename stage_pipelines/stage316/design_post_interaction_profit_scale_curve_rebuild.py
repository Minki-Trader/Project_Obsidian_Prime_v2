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
from stage_pipelines.stage315 import design_runtime_outcome_feature_interaction_rebuild as s315  # noqa: E402


s310 = s315.s310

STAGE_ID = "316_onnx_candidate_campaign__post_interaction_profit_scale_curve_rebuild"
RUN_ID = "run316A_design_post_interaction_profit_scale_curve_rebuild_packet_v1"
RUN_NUMBER = "run316A"
SOURCE_STAGE_ID = "315_onnx_candidate_campaign__runtime_outcome_feature_interaction_rebuild"
SOURCE_RUN_ID = "run315C_review_runtime_outcome_feature_interaction_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_post_interaction_profit_scale_curve_candidates_materialized_no_selection"
JUDGMENT = "post_interaction_profit_scale_curve_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run316B_execute_post_interaction_profit_scale_curve_mt5_probe"
BOUNDARY = s315.BOUNDARY

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
SOURCE_RUN315A = SOURCE_STAGE / "02_runs" / "run315A"
SOURCE_RUN315C = SOURCE_STAGE / "02_runs" / "run315C"
SOURCE_MANIFEST = SOURCE_RUN315A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN315C / "runtime_outcome_feature_interaction_review_scoreboard.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN315C / "stage316_seed_queue.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN315C / "failure_memory.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run315C_review_stage316_open.md"

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
REPORT = REVIEWS / "run316A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage316/design_post_interaction_profit_scale_curve_rebuild.py")
RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = s315.DECISION_FEATURES + (
    "stage316_positive_hour_sell_score",
    "stage316_intrahour_stagger_score",
    "stage316_curve_guard_score",
    "stage316_hour20_22_flag",
    "stage316_no_mirror_guard_flag",
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
            "cp316A_hour20_22_stagger_sell_hold2_surface",
            "hour20_22_stagger_sell_hold2",
            5.4,
            2,
            0.54,
            0.92,
            4.25,
            0.038,
            "Stage315(315단계) mirror(반전)는 계좌 손상을 만들었다. Stage314(314단계)에서 실제 양수였던 20/22시 sell(매도)만 남기고 intrahour stagger(시간 내부 분산)로 4-10 trades/day(일 4-10거래)를 맞추면 수익 규모와 곡선을 함께 볼 수 있다.",
            "19/21시 mirror(반전)를 제거하고 20/22시 sell-only(매도 전용) 시간 내부 샘플링으로 바꾼다.",
        ),
        CandidateSpec(
            "cp316B_hour20_22_dense_sell_curve_guard_hold1_surface",
            "hour20_22_dense_sell_curve_guard_hold1",
            6.8,
            1,
            0.46,
            0.78,
            3.20,
            0.032,
            "손실 포켓을 줄이는 defensive experiment(방어형 실험)이다. 짧은 hold(보유)와 타이트한 손절/익절로 20/22시 sell(매도) 곡선이 움푹 파이는지 본다.",
            "max hold(최대 보유)를 1봉으로 줄이고 curve guard(곡선 보호)를 강화한다.",
        ),
        CandidateSpec(
            "cp316C_hour20_primary_22_support_sell_scale_hold3_surface",
            "hour20_primary_22_support_sell_scale_hold3",
            4.8,
            3,
            0.68,
            1.04,
            5.55,
            0.046,
            "순수익 규모를 키우는 aggressive experiment(공격형 실험)이다. 20시 sell(매도)을 주력으로 두고 22시는 보조로 써서 수익 볼록성을 압박한다.",
            "20시 sell(매도) 비중을 높이고 lot(랏), TP(익절), hold(보유)를 키운다.",
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            "cp316D_hour20_22_lowvol_sell_smooth_hold2_surface",
            "hour20_22_lowvol_sell_smooth_hold2",
            5.0,
            2,
            0.58,
            0.88,
            4.60,
            0.037,
            "저변동/중간 추세에서만 20/22시 sell(매도)을 허용하면 거래수와 곡선 안정성을 같이 맞출 수 있는지 본다.",
            "low volatility(저변동), mid trend(중간 추세), low shock(낮은 충격) 조건을 결합한다.",
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            "cp316E_hour20_22_sell_23buy_tail_hold2_surface",
            "hour20_22_sell_23buy_tail_hold2",
            5.6,
            2,
            0.52,
            0.96,
            4.35,
            0.036,
            "23시 buy(매수)는 작지만 표본외 꼬리 수익 단서가 있었다. 20/22시 sell(매도)에 아주 제한적인 23시 buy(매수)를 붙여 수익 꼬리를 본다.",
            "23시 buy tail(매수 꼬리)을 저충격 조건으로만 붙인다.",
        ),
        CandidateSpec(
            "cp316F_aggressive_hour20_22_sell_convexity_hold3_surface",
            "aggressive_hour20_22_sell_convexity_hold3",
            6.2,
            3,
            0.76,
            1.16,
            6.20,
            0.052,
            "수익 규모가 부족하면 끝낼 수 없다. 20/22시 sell-only(매도 전용) 구조에서 risk/reward convexity(위험/보상 볼록성)를 키워 scale gate(규모 관문)를 압박한다.",
            "공격형 lot(랏), TP(익절), hold(보유)를 쓰되 19/21시 mirror(반전)는 금지한다.",
            same_direction_reentry_cooldown_bars=1,
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s310.rel(path)


def read_text(path: Path) -> str:
    return s310.read_text(path)


def write_text(path: Path, text: str) -> None:
    s315.write_text(path, text)


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
    return s315.zscore(values)


def positive(values: np.ndarray) -> np.ndarray:
    return s315.positive(values)


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    return s315.ncol(frame, column, default)


def quantile(values: np.ndarray, pct: float) -> float:
    return s315.quantile(values, pct)


def band(values: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return s315.band(values, lo, hi)


def signal_label(value: int) -> str:
    return s315.signal_label(value)


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
        return rows[0].get("seed_id", "stage315_runtime_outcome_feature_interaction_review_seed")
    return "stage315_runtime_outcome_feature_interaction_review_seed"


def source_manifest_rows() -> list[dict[str, str]]:
    return [row for row in read_csv_dicts(SOURCE_MANIFEST) if row.get("payload_path")][:6]


def load_source_frame() -> pd.DataFrame:
    rows = source_manifest_rows()
    if not rows:
        raise RuntimeError("missing Stage315 source manifest rows")
    return pd.read_parquet(s315.s314.long_path(ROOT / rows[0]["payload_path"]))


def add_stage316_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    ts = pd.to_datetime(out["timestamp"], utc=True)
    hour = ts.dt.hour.to_numpy()
    minute = ts.dt.minute.to_numpy()
    slot = (minute // 5).astype("int16")
    shock = s310.s309.s308.shock_score(out)
    vol = zscore(ncol(out, "historical_vol_5_over_20"))
    rsi = zscore(ncol(out, "rsi_14"))
    ret = zscore(ncol(out, "return_zscore_20"))
    trend = zscore(ncol(out, "ema20_ema50_diff")) + 0.45 * zscore(ncol(out, "di_spread_14")) + 0.30 * zscore(ncol(out, "ppo_hist_12_26_9"))
    breadth = zscore(ncol(out, "mega8_pos_breadth_1")) + 0.35 * zscore(ncol(out, "top3_weighted_return_1"))
    pos_hour = np.isin(hour, [20, 22])
    stagger = np.isin(slot, [0, 3, 6, 9]).astype("float64")
    low_vol = vol < quantile(vol, 62)
    mid_state = band(rsi, 12, 82) & band(trend, 14, 84) & band(breadth, 10, 88)
    curve_guard = low_vol & mid_state & (shock < quantile(shock, 84))
    out["stage316_positive_hour_sell_score"] = pos_hour.astype("float64") + 0.45 * low_vol.astype("float64") + 0.25 * positive(-ret) - 0.55 * positive(shock)
    out["stage316_intrahour_stagger_score"] = stagger + 0.35 * np.isin(slot, [1, 5, 9]).astype("float64") + 0.25 * low_vol.astype("float64")
    out["stage316_curve_guard_score"] = curve_guard.astype("float64") + 0.35 * mid_state.astype("float64") - 0.65 * positive(shock)
    out["stage316_hour20_22_flag"] = pos_hour.astype("int8")
    out["stage316_no_mirror_guard_flag"] = (~np.isin(hour, [19, 21])).astype("int8")
    return out


def support_arrays(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    hour = ts.dt.hour.to_numpy()
    minute = ts.dt.minute.to_numpy()
    slot = (minute // 5).astype("int16")
    shock = s310.s309.s308.shock_score(frame)
    pos_hour = np.isin(hour, [20, 22])
    support = pos_hour & np.isin(slot, [0, 2, 4, 6, 8, 10]) & (shock < quantile(shock, 90))
    buy23 = (hour == 23) & np.isin(slot, [1, 7]) & (shock < quantile(shock, 55))
    signal = np.where(support, -1, np.where(buy23, 1, 0)).astype("int8")
    score = ncol(frame, "stage316_positive_hour_sell_score") + 0.35 * ncol(frame, "stage316_intrahour_stagger_score") + 0.25 * ncol(frame, "stage316_curve_guard_score")
    return signal, np.asarray(score, dtype="float64")


def transform_signal(spec: CandidateSpec, frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    hour = ts.dt.hour.to_numpy()
    minute = ts.dt.minute.to_numpy()
    slot = (minute // 5).astype("int16")
    shock = s310.s309.s308.shock_score(frame)
    vol = zscore(ncol(frame, "historical_vol_5_over_20"))
    curve = ncol(frame, "stage316_curve_guard_score")
    pos_score = ncol(frame, "stage316_positive_hour_sell_score")
    stagger_score = ncol(frame, "stage316_intrahour_stagger_score")
    low_vol = vol < quantile(vol, 64)
    sell20 = hour == 20
    sell22 = hour == 22
    safe = shock < quantile(shock, 88)
    if spec.model_surface == "hour20_22_stagger_sell_hold2":
        active = (sell20 | sell22) & np.isin(slot, [0, 3, 6, 9]) & safe
        score = pos_score + 0.55 * stagger_score + 0.35 * curve
    elif spec.model_surface == "hour20_22_dense_sell_curve_guard_hold1":
        active = (sell20 | sell22) & np.isin(slot, [0, 2, 4, 6, 8, 10]) & (curve > quantile(curve, 38)) & safe
        score = 0.75 * pos_score + 0.70 * curve + 0.45 * stagger_score
    elif spec.model_surface == "hour20_primary_22_support_sell_scale_hold3":
        active = ((sell20 & np.isin(slot, [0, 2, 4, 6, 8, 10])) | (sell22 & np.isin(slot, [0, 4, 8]))) & safe
        score = 0.95 * sell20.astype("float64") + 0.35 * sell22.astype("float64") + 0.45 * pos_score - 0.30 * positive(shock)
    elif spec.model_surface == "hour20_22_lowvol_sell_smooth_hold2":
        active = (sell20 | sell22) & np.isin(slot, [1, 4, 7, 10]) & low_vol & (curve > quantile(curve, 44)) & safe
        score = 0.70 * pos_score + 0.82 * curve + 0.20 * positive(-vol)
    elif spec.model_surface == "hour20_22_sell_23buy_tail_hold2":
        buy23 = (hour == 23) & np.isin(slot, [1, 7]) & (shock < quantile(shock, 50)) & (curve > quantile(curve, 54))
        active = ((sell20 | sell22) & np.isin(slot, [0, 3, 6, 9]) & safe) | buy23
        raw = np.where(buy23, 1, np.where(active, -1, 0)).astype("int8")
        score = 0.78 * pos_score + 0.48 * curve + 0.35 * buy23.astype("float64")
        support_signal, support_score = support_arrays(frame)
        signal = np.where(score > quantile(score, 20), raw, 0).astype("int8")
        signal = s310.density_fit(frame, signal, score, support_signal, support_score, hold_bars=spec.max_hold_bars, target_density=spec.target_density)
        return signal.astype("int8"), np.asarray(score, dtype="float64")
    elif spec.model_surface == "aggressive_hour20_22_sell_convexity_hold3":
        active = (sell20 | sell22) & np.isin(slot, [0, 2, 3, 5, 6, 8, 9, 11]) & safe
        score = 0.95 * pos_score + 0.40 * stagger_score + 0.20 * curve - 0.20 * positive(shock)
    else:
        raise ValueError(f"unsupported model surface: {spec.model_surface}")
    raw = np.where(active, -1, 0).astype("int8")
    support_signal, support_score = support_arrays(frame)
    signal = np.where(score > quantile(score, 18), raw, 0).astype("int8")
    signal = s310.density_fit(frame, signal, score, support_signal, support_score, hold_bars=spec.max_hold_bars, target_density=spec.target_density)
    return signal.astype("int8"), np.asarray(score, dtype="float64")


def materialize_payload(spec: CandidateSpec, frame: pd.DataFrame, seed_id: str) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = transform_signal(spec, frame)
    branch_id = f"run316A_{spec.package_id.replace('_surface', '')}"
    payload = frame.copy()
    payload["stage316_branch_id"] = branch_id
    payload["stage315_seed_id"] = seed_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "post_interaction_profit_scale_curve_surface"
    payload["candidate_decision_score"] = score
    payload["source_package_id"] = "stage315_no_selection_failure_memory"
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
    frame = add_stage316_features(load_source_frame())
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
        branch_id = f"run316A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_post_interaction_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(s315.s314.long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage316_branch_id": branch_id,
                "stage315_seed_id": seed_id,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage316 MT5 probe(316단계 MT5 탐침)",
                "claim_boundary": BOUNDARY,
            },
        )
        candidate_supply = s310.supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        density_gate = s310.gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = s310.gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = s310.gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s310.s309.s308.s307.prev.s290.selection_score(validation_metrics)
            + s310.s309.s308.s307.prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])) * 60.0
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
                "comparison_baseline": "Stage315 no-selection(315단계 선택 없음) and Stage314 positive-hour evidence(314단계 양수 시간 근거).",
                "control_variables": "US100 M5, split_v1(분할 v1), Tier A/B paired accounting(티어 A/B 쌍 기록), no 19/21 mirror(19/21시 반전 금지).",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리) and MT5 runtime probe(MT5 런타임 탐침).",
                "success_criteria": "actual MT5 validation/OOS positive(검증/표본외 양수), minimum trade count(최소 거래수), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), smooth curve(매끄러운 곡선).",
                "failure_criteria": "loss, density outside 4-10(밀도 이탈), weak scale(약한 규모), deep curve pocket(깊은 곡선 포켓).",
                "invalid_conditions": "payload mismatch(페이로드 불일치), feature order mismatch(피처 순서 불일치), MT5 report parse missing(MT5 보고서 파싱 누락).",
                "stop_conditions": "candidate gate pass(후보 관문 통과) -> Adapter(어댑터); all fail(전체 실패) -> next fresh thesis(다음 새 논제).",
                "evidence_plan": "branch queue(분기 대기열), proxy scoreboard(대리 점수판), MT5 queue(MT5 대기열), run316B/run316C.",
                "feature_surface": "20/22시 sell-only(매도 전용), intrahour sampling(시간 내부 샘플링), curve guard(곡선 보호).",
                "model_surface": "rule_surface_post_interaction_profit_scale_curve",
                "decision_surface": spec.model_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생); Adapter trace(어댑터 추적)는 후보 관문 후 시작한다.",
                "failure_memory_plan": "hour20/22 density(20/22시 밀도), profit scale(수익 규모), curve pocket(곡선 포켓)을 분리 기록한다.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run316A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": str(payload.get("stage309_branch_id", pd.Series([""])).iloc[0]) if "stage309_branch_id" in payload else "",
                "stage308_branch_id": str(payload.get("stage308_branch_id", pd.Series([""])).iloc[0]) if "stage308_branch_id" in payload else "",
                "stage307_branch_id": str(payload.get("stage307_branch_id", pd.Series([""])).iloc[0]) if "stage307_branch_id" in payload else "",
                "stage306_branch_id": str(payload.get("stage306_branch_id", pd.Series([""])).iloc[0]) if "stage306_branch_id" in payload else "",
                "package_id": spec.package_id,
                "queue_role": "post_interaction_profit_scale_curve_surface",
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
                "model_family": "post_interaction_profit_scale_curve_rule_surface",
                "prediction_kind": "runtime_direction_sell_only_sampling",
                "dataset_id": "stage315_failure_memory_plus_stage314_positive_hour_attribution",
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
                "model_family": "post_interaction_profit_scale_curve_rule_surface",
                "prediction_kind": "runtime_direction_sell_only_sampling",
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
                "user_explanation_hook": "19/21시 반전을 버리고 20/22시 sell-only(매도 전용) 시간 내부 샘플링을 MT5(메타트레이더5)로 압박한다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        s310.GATE_COLUMNS,
        [
            {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "mirror(반전)를 폐기하고 sell-only sampling(매도 전용 샘플링)으로 질문을 바꿨다."},
            {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
            {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "MT5 review(MT5 검토) 전에는 Adapter(어댑터)를 만들지 않는다."},
            {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "후보 선택 전에는 ONNX(온엑스)를 시작하지 않는다."},
        ],
    )
    write_json(EXPERIMENT_DESIGN, {"hypothesis": "20/22시 sell-only(매도 전용) intrahour sampling(시간 내부 샘플링)이 거래수 4-10/day(일 4-10거래)와 수익 규모/곡선을 같이 만족할 수 있는지 본다.", "decision_use": NEXT_ACTION, "comparison_baseline": "Stage315 no-selection(315단계 선택 없음)", "control_variables": ["US100 M5", "split_v1", "no 19/21 mirror(19/21시 반전 금지)"], "changed_variables": ["intrahour sampling(시간 내부 샘플링)", "risk/reward scale(위험/보상 규모)"], "success_criteria": ["actual MT5 validation/OOS positive(검증/표본외 양수)", "4-10 trades/day(일 4-10거래)", "smooth curve(매끄러운 곡선)"], "failure_criteria": ["loss(손실)", "density out of range(밀도 이탈)", "deep curve pocket(깊은 곡선 포켓)"], "claim_boundary": BOUNDARY})
    write_json(DATA_RECEIPT, {"source_manifest": rel(SOURCE_MANIFEST), "source_scoreboard": rel(SOURCE_SCOREBOARD), "source_failure_memory": rel(SOURCE_FAILURE_MEMORY), "model_feature_order_hash": ordered_hash(DECISION_FEATURES), "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER), "claim_boundary": BOUNDARY})
    artifacts = [rel(path) for path in payload_artifacts] + [rel(path) for path in (BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "candidate_count": len(scoreboard_rows), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "artifacts": artifacts, "claim_boundary": BOUNDARY})
    write_json(LINEAGE, {"run_id": RUN_ID, "producer": str(PRODUCER), "source_inputs": [rel(SOURCE_MANIFEST), rel(SOURCE_SCOREBOARD), rel(SOURCE_SEED_QUEUE), rel(SOURCE_FAILURE_MEMORY), rel(SOURCE_REVIEW)], "consumer": NEXT_ACTION, "artifact_paths": artifacts, "availability": "tracked_manifest_plus_payloads", "lineage_judgment": "connected_with_boundary", "claim_boundary": BOUNDARY})
    write_text(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return list(payload_artifacts) + [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run316A Post Interaction Profit Scale Curve Materialization(316A 상호작용 이후 수익 규모/곡선 물질화)",
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
        "Effect(효과): Stage315(315단계)의 mirror(반전) 실패를 버리고, 20/22시 sell-only(매도 전용) 시간 내부 샘플링으로 수익 규모와 곡선을 다시 압박한다.",
        "",
        "| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일 거래) | gates(관문) |",
        "|---|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        gates = ",".join(name for name, key in (("density", "density_gate"), ("edge", "proxy_edge_gate"), ("curve", "curve_proxy_gate")) if row[key] != "passed") or "passed"
        lines.append(f"| {row['package_id']} | {float(row['validation_proxy_net_bp']):.2f} | {float(row['oos_proxy_net_bp']):.2f} | {float(row['validation_proxy_trades_per_day']):.2f}/{float(row['oos_proxy_trades_per_day']):.2f} | {gates} |")
    lines.extend(["", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    safe_upsert(RUN_REGISTRY, s310.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_interaction_profit_scale_curve_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};selected_candidate=none;next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, s310.s309.s308.s307.prev.s290.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "post_interaction_profit_scale_curve_materialization", "tier_scope": "Tier A separate/Tier B separate/Tier A+B routed preparation", "kpi_scope": "proxy_plus_mt5_queue", "scoreboard_lane": "onnx_candidate_campaign", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}", "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started", "external_verification_status": "prepared_not_executed", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, s310.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "post_interaction_profit_scale_curve_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")
    rows = []
    for path in artifacts:
        if not s310.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append({"artifact_id": f"{RUN_ID}__{artifact_id}", "artifact_type": "stage316_post_interaction_profit_scale_curve_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "Stage316 design/materialization artifact"})
    safe_upsert(ARTIFACT_REGISTRY, s310.ARTIFACT_COLUMNS, rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = replace_line_prefix(read_text(SELECTED), "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run316A_report", f"- run316A_report(316A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run316A_mt5_queue", f"- run316A_mt5_queue(316A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)
    review_index = append_once(read_text(REVIEW_INDEX), "run316A_report", f"- run316A_report(316A 보고서): `{rel(REPORT)}`\n- run316A_scoreboard(316A 점수판): `{rel(MODEL_SCOREBOARD)}`\n- run316A_mt5_queue(316A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)
    current = replace_line_prefix(read_text(CURRENT_STATE), "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run316A_summary", f"- run316A_summary(316A 요약): post interaction profit scale/curve(상호작용 이후 수익 규모/곡선) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): 19/21시 mirror(반전)를 버리고 20/22시 sell-only(매도 전용) MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었으며 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.")
    write_text(CURRENT_STATE, current)
    workspace = replace_line_prefix(read_text(WORKSPACE_STATE), "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage316(316단계) run316A(316A 실행) post interaction profit scale/curve materialization(상호작용 이후 수익 규모/곡선 물질화) `{RUN_ID}`. Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run316A Post interaction profit scale/curve materialization(316A 상호작용 이후 수익 규모/곡선 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): 후보 `{len(scoreboard_rows)}`개와 MT5 대기열 `{len(manifest_rows)}`개를 만들었다.\n- boundary(경계): 선택 후보, Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 없다.\n"
    write_text(CHANGELOG, changelog)
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += f"\n## {RUN_ID} post_interaction_profit_scale_curve(상호작용 이후 수익 규모/곡선)\n\n- idea_id(아이디어 ID): `stage316_post_interaction_profit_scale_curve`\n- hypothesis(가설): 20/22시 sell-only(매도 전용) 시간 내부 샘플링이 거래수와 곡선을 같이 맞출 수 있다.\n- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        write_text(IDEA_REGISTER, idea)


def main() -> None:
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts)
    update_registers(scoreboard_rows, manifest_rows, artifacts, utc_now())
    update_docs(scoreboard_rows, manifest_rows)
    print(json.dumps({"status": STATUS, "judgment": JUDGMENT, "candidate_rows": len(scoreboard_rows), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
