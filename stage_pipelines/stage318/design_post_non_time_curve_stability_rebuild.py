from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage280.validate_directional_mapping_stability import (  # noqa: E402
    drawdown_stats,
    profit_factor,
    trade_frame,
)
from stage_pipelines.stage317 import design_fresh_non_time_profit_source_rebuild as s317  # noqa: E402


s310 = s317.s310

STAGE_ID = "318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild"
RUN_ID = "run318A_design_post_non_time_curve_stability_rebuild_packet_v1"
RUN_NUMBER = "run318A"
SOURCE_STAGE_ID = "317_onnx_candidate_campaign__fresh_non_time_profit_source_rebuild"
SOURCE_RUN_ID = "run317C_review_fresh_non_time_profit_source_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_post_non_time_curve_stability_candidates_materialized_no_selection"
JUDGMENT = "post_non_time_curve_stability_outcome_distillation_materialized_no_candidate_selection"
NEXT_ACTION = "run318B_execute_post_non_time_curve_stability_mt5_probe"
BOUNDARY = s317.BOUNDARY

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
SOURCE_RUN317A = SOURCE_STAGE / "02_runs" / "run317A"
SOURCE_RUN317C = SOURCE_STAGE / "02_runs" / "run317C"
SOURCE_MANIFEST = SOURCE_RUN317A / "candidate_payload_manifest.csv"
SOURCE_REPORT_RECEIPT = SOURCE_RUN317C / "report_source_path_receipt.csv"
SOURCE_REVIEW_SCOREBOARD = SOURCE_RUN317C / "fresh_non_time_profit_source_review_scoreboard.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN317C / "failure_memory.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run317C_review_stage318_open.md"

TRADE_FRAME = RUN_ROOT / "run318A_stage317_actual_trade_frame.csv"
SEGMENT_SUMMARY = RUN_ROOT / "run318A_stage317_actual_segment_summary.csv"
DUAL_POSITIVE = RUN_ROOT / "run318A_stage317_dual_positive_actual_fragments.csv"
TRAINING_SET = RUN_ROOT / "runtime_outcome_training_set.csv"
TRAINING_DIAGNOSTICS = RUN_ROOT / "runtime_outcome_training_diagnostics.json"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
ESTIMATED_REPLAY = RUN_ROOT / "estimated_actual_replay_scoreboard.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run318A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage318/design_post_non_time_curve_stability_rebuild.py")
RUNTIME_FEATURE_ORDER = ("route_signal_value",)

MODEL_FEATURES = (
    "log_return_1",
    "log_return_3",
    "return_zscore_20",
    "hl_zscore_50",
    "return_1_over_atr_14",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
    "payoff_edge_score",
    "anti_meta_score",
    "profit_quality_score",
    "density_head_score",
    "runtime_calibration_score",
    "profit_scale_score",
    "smooth_curve_score",
    "anti_regime_flag",
    "smooth_regime_flag",
    "precondition_pass",
    "stage316_positive_hour_sell_score",
    "stage316_intrahour_stagger_score",
    "stage316_curve_guard_score",
    "stage317_adx_short_score",
    "stage317_usdx_extreme_score",
    "stage317_momentum_breadth_score",
    "stage317_quality_scale_score",
    "stage317_bollinger_extreme_score",
    "stage317_hybrid_router_score",
    "source_code",
    "hyp_signal",
)

BASE_FEATURES = tuple(name for name in MODEL_FEATURES if name not in {"source_code", "hyp_signal"})
MODEL_FEATURE_ORDER_HASH = ordered_hash(MODEL_FEATURES)
RUNTIME_FEATURE_ORDER_HASH = ordered_hash(RUNTIME_FEATURE_ORDER)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    source_package_id: str
    model_surface: str
    probability_floor: float
    target_raw_signals_per_day: float
    score_probability_weight: float
    hypothesis: str
    changed_variables: str


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            "cp318A_outcome_dense20_curve_stability_surface",
            "cp317A_usdx_extreme_follow_hold1_dense_surface",
            "actual_outcome_dense20_curve_stability",
            0.44,
            20.0,
            20.0,
            "Stage317(317단계) high-density USDX(달러지수) surface(표면)의 실제 손실 구간을 outcome distillation(결과 증류)로 줄이면 actual trades/day(실제 일 거래수) 4-10과 순수익 규모를 같이 만들 수 있다.",
            "Stage317(317단계) cp317A(317A 후보)의 방향은 유지하되 실제 MT5(메타트레이더5) 체결 손익으로 학습한 curve stability score(곡선 안정성 점수)를 붙인다.",
        ),
        CandidateSpec(
            "cp318B_outcome_dense22_pocket_guard_surface",
            "cp317A_usdx_extreme_follow_hold1_dense_surface",
            "actual_outcome_dense22_pocket_guard",
            0.44,
            22.0,
            20.0,
            "cp318A(318A 후보)보다 raw signal density(원천 신호 밀도)를 넓혀 curve pocket(곡선 포켓)이 다시 깊어지는지 압박한다.",
            "같은 source(원천)라도 target density(목표 밀도)와 threshold(임계값)를 다르게 둔 공격형/방어형 균형 실험이다.",
        ),
        CandidateSpec(
            "cp318C_bollinger_curve_stability10_surface",
            "cp317E_bollinger_position_extreme_hold1_surface",
            "actual_outcome_bollinger_stability10",
            0.44,
            10.0,
            20.0,
            "Stage317(317단계)에서 가장 덜 나쁜 actual MT5(실제 메타트레이더5) 표면인 Bollinger(볼린저) extreme(극단) 조각을 곡선 안정성 구조로 다시 압축한다.",
            "Bollinger/return state(볼린저/수익률 상태) 신호를 outcome score(결과 점수)로 걸러 OOS(표본외) 상방과 validation(검증) 손상을 동시에 본다.",
        ),
        CandidateSpec(
            "cp318D_adx_short_defensive10_surface",
            "cp317C_adx_high_short_hold1_defensive_surface",
            "actual_outcome_adx_short_defensive10",
            0.48,
            10.0,
            20.0,
            "ADX high short(ADX 고수준 매도) 방어 표면은 source(원천) 손실이 컸지만 실제 양수 조각을 많이 품고 있어 방어형 안정성 후보로 다시 본다.",
            "short-only(매도 전용) 성격은 유지하되 실제 손익 기반 score(점수)로 위험 구간을 veto(거부)한다.",
        ),
        CandidateSpec(
            "cp318E_scale_hold2_24_surface",
            "cp317B_usdx_extreme_follow_hold2_scale_surface",
            "actual_outcome_scale_hold2_24",
            0.44,
            24.0,
            20.0,
            "hold2(2봉 보유) scale(규모) 구조가 outcome score(결과 점수) 필터 뒤에도 profit scale(수익 규모)을 유지하는지 본다.",
            "Stage317(317단계) cp317B(317B 후보)의 reward/risk(보상/위험) 구조를 유지하고 실제 손실 조각만 줄인다.",
        ),
        CandidateSpec(
            "cp318F_adx_short_density12_surface",
            "cp317C_adx_high_short_hold1_defensive_surface",
            "actual_outcome_adx_short_density12",
            0.48,
            12.0,
            20.0,
            "cp318D(318D 후보)보다 밀도를 넓혀 ADX(평균방향지수) short(매도) 조각의 scale(규모) 한계를 압박한다.",
            "같은 ADX source(ADX 원천)를 방어형과 밀도형으로 나눠 곡선 pocket(포켓)과 거래수 trade count(거래 수)의 균형점을 본다.",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s310.rel(path)


def read_text(path: Path) -> str:
    return s310.read_text(path)


def write_text(path: Path, text: str) -> None:
    s317.write_text(path, text)


def write_json(path: Path, payload: Any) -> None:
    s310.write_json(path, payload)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    s310.write_csv(path, columns, rows)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s310.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return s310.sha256_file(path)


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def signal_label(value: int) -> str:
    return s317.signal_label(value)


def long_path(path: Path) -> str:
    return s317.s316.s315.s314.long_path(path)


def source_manifest_rows() -> list[dict[str, str]]:
    return [row for row in s317.read_csv_dicts(SOURCE_MANIFEST) if row.get("payload_path")]


def read_payloads() -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, str]], list[str]]:
    payloads: dict[str, pd.DataFrame] = {}
    manifest_by_package: dict[str, dict[str, str]] = {}
    packages: list[str] = []
    for row in source_manifest_rows():
        package_id = row["package_id"]
        frame = pd.read_parquet(long_path(ROOT / row["payload_path"]))
        frame["ts_floor"] = pd.to_datetime(frame["timestamp"], utc=True).dt.tz_convert(None).dt.floor("5min")
        payloads[package_id] = frame
        manifest_by_package[package_id] = row
        packages.append(package_id)
    return payloads, manifest_by_package, packages


def build_trade_frame() -> pd.DataFrame:
    rows = pd.read_csv(SOURCE_REPORT_RECEIPT)
    frames: list[pd.DataFrame] = []
    for _, row in rows.iterrows():
        report = Path(str(row["report_path"]))
        frame = trade_frame(report)
        if frame.empty:
            continue
        frame["materialized_branch_id"] = row["materialized_branch_id"]
        frame["package_id"] = row["package_id"]
        frame["split"] = row["split"]
        frame["report_path"] = str(report)
        frame["open_floor"] = pd.to_datetime(frame["open_time"]).dt.floor("5min")
        frame["dir_val"] = frame["direction"].map({"buy": 1, "sell": -1}).astype(int)
        frames.append(frame)
    if not frames:
        raise RuntimeError("Stage317 actual MT5 trade frame is empty")
    out = pd.concat(frames, ignore_index=True)
    out = out.sort_values(["package_id", "split", "open_time", "close_time"]).reset_index(drop=True)
    out.to_csv(long_path(TRADE_FRAME), index=False, encoding="utf-8-sig")
    return out


def summarize_profits(values: Sequence[float]) -> dict[str, Any]:
    profits = [float(value) for value in values]
    dd = drawdown_stats(profits)
    return {
        "trade_count": len(profits),
        "net_profit": round(sum(profits), 2),
        "profit_factor": round(profit_factor(profits), 6),
        "expectancy": round((sum(profits) / len(profits)) if profits else 0.0, 6),
        "max_drawdown": round(dd["max_drawdown"], 2),
        "recovery_factor": round(dd["recovery_factor"], 6),
        "new_high_count": dd["new_high_count"],
        "underwater_trade_count": dd["underwater_trade_count"],
    }


def write_attribution_summaries(trades: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    segment_rows: list[dict[str, Any]] = []
    for cols in (
        ("package_id", "split"),
        ("package_id", "split", "direction"),
        ("package_id", "split", "session"),
        ("package_id", "split", "hour"),
        ("package_id", "split", "month"),
    ):
        for keys, group in trades.groupby(list(cols), dropna=False, observed=True):
            key_tuple = keys if isinstance(keys, tuple) else (keys,)
            row = {"segment_family": "|".join(cols)}
            row.update({col: value for col, value in zip(cols, key_tuple)})
            row.update(summarize_profits(group["net_profit"].tolist()))
            segment_rows.append(row)
    write_csv(SEGMENT_SUMMARY, list(segment_rows[0].keys()), segment_rows)

    positive_rows: list[dict[str, Any]] = []
    frame = pd.DataFrame(segment_rows)
    for family in sorted(frame["segment_family"].unique()):
        cols = family.split("|")
        if "split" not in cols:
            continue
        non_split = [col for col in cols if col != "split"]
        sub = frame[frame["segment_family"] == family]
        for keys, group in sub.groupby(non_split, dropna=False, observed=True):
            key_tuple = keys if isinstance(keys, tuple) else (keys,)
            splits = set(group["split"].astype(str))
            if {"validation_is", "oos"} <= splits:
                val = group[group["split"] == "validation_is"].iloc[0]
                oos = group[group["split"] == "oos"].iloc[0]
                if float(val["net_profit"]) > 0 and float(oos["net_profit"]) > 0:
                    row = {"segment_family": family}
                    row.update({col: value for col, value in zip(non_split, key_tuple)})
                    row.update(
                        {
                            "validation_net": val["net_profit"],
                            "validation_pf": val["profit_factor"],
                            "validation_trades": val["trade_count"],
                            "oos_net": oos["net_profit"],
                            "oos_pf": oos["profit_factor"],
                            "oos_trades": oos["trade_count"],
                            "combined_net": round(float(val["net_profit"]) + float(oos["net_profit"]), 2),
                        }
                    )
                    positive_rows.append(row)
    if positive_rows:
        positive_rows.sort(key=lambda row: (float(row["combined_net"]), int(row["validation_trades"]) + int(row["oos_trades"])), reverse=True)
        write_csv(DUAL_POSITIVE, list(positive_rows[0].keys()), positive_rows)
    else:
        write_csv(DUAL_POSITIVE, ["segment_family", "note"], [{"segment_family": "none", "note": "no simple dual-positive actual fragment"}])
    return segment_rows, positive_rows


def build_training_set(payloads: Mapping[str, pd.DataFrame], packages: Sequence[str], trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for code, package_id in enumerate(packages):
        payload = payloads[package_id]
        cols = [name for name in BASE_FEATURES if name in payload.columns]
        source = payload[cols + ["ts_floor", "route_signal_value", "split"]].copy()
        package_trades = trades[trades["package_id"] == package_id].copy()
        merged = package_trades.merge(source, left_on="open_floor", right_on="ts_floor", how="inner", suffixes=("", "_payload"))
        merged["source_code"] = code
        merged["hyp_signal"] = merged["dir_val"]
        merged["positive_trade"] = (pd.to_numeric(merged["net_profit"], errors="coerce").fillna(0.0) > 0.0).astype(int)
        rows.append(merged)
    training = pd.concat(rows, ignore_index=True)
    for feature in MODEL_FEATURES:
        if feature not in training.columns:
            training[feature] = 0.0
    training.to_csv(long_path(TRAINING_SET), index=False, encoding="utf-8-sig")
    return training


def train_models(training: pd.DataFrame) -> tuple[Any, Any, dict[str, Any]]:
    features = training[list(MODEL_FEATURES)]
    target = pd.to_numeric(training["net_profit"], errors="coerce").fillna(0.0)
    target_class = (target > 0.0).astype(int)
    regressor = make_pipeline(
        SimpleImputer(strategy="median"),
        ExtraTreesRegressor(n_estimators=700, max_depth=9, min_samples_leaf=15, random_state=3184, n_jobs=-1),
    )
    classifier = make_pipeline(
        SimpleImputer(strategy="median"),
        ExtraTreesClassifier(n_estimators=700, max_depth=9, min_samples_leaf=15, class_weight="balanced", random_state=3184, n_jobs=-1),
    )
    regressor.fit(features, target)
    classifier.fit(features, target_class)
    prob = classifier.predict_proba(features)[:, 1]
    diagnostics = {
        "training_rows": int(len(training)),
        "positive_rate": float(target_class.mean()),
        "net_profit_total": float(target.sum()),
        "feature_count": len(MODEL_FEATURES),
        "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
        "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
        "auc_in_sample": float(roc_auc_score(target_class, prob)) if len(set(target_class)) > 1 else 0.0,
        "training_scope": "Stage317 validation+OOS actual MT5 trades(317단계 검증+표본외 실제 MT5 거래)",
        "leakage_boundary": "exploratory_design_only_requires_run318B_actual_mt5_and_later_stability_pressure",
    }
    write_json(TRAINING_DIAGNOSTICS, diagnostics)
    return regressor, classifier, diagnostics


def save_shared_models(regressor: Any, classifier: Any) -> tuple[Path, Path]:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    regressor_path = MODEL_DIR / "run318A_runtime_outcome_regressor.joblib"
    classifier_path = MODEL_DIR / "run318A_runtime_outcome_classifier.joblib"
    joblib.dump(regressor, long_path(regressor_path))
    joblib.dump(classifier, long_path(classifier_path))
    return regressor_path, classifier_path


def source_risk_fields(row: Mapping[str, str]) -> dict[str, Any]:
    bool_fields = {
        "close_on_flat_signal",
        "atr_sltp_enabled",
        "exit_risk_overlay_enabled",
        "model_risk_sizing_enabled",
    }
    int_fields = {
        "max_hold_bars",
        "same_direction_reentry_cooldown_bars",
        "atr_period",
        "atr_min_stop_points",
        "atr_max_stop_points",
        "atr_min_take_profit_points",
        "atr_max_take_profit_points",
        "exit_risk_close_long_feature_index",
        "exit_risk_close_short_feature_index",
        "exit_risk_min_hold_bars",
        "exit_risk_max_hold_feature_index",
    }
    fields = (
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
    )
    out: dict[str, Any] = {}
    for field in fields:
        value = row.get(field, "")
        if field in bool_fields:
            out[field] = 1 if str(value).strip().lower() in {"1", "true", "yes"} else 0
        elif field in int_fields:
            out[field] = int(number(value, 0.0))
        else:
            out[field] = number(value, 0.0)
    return out


def threshold_for_target(frame: pd.DataFrame, score: np.ndarray, mask: np.ndarray, target: float) -> float:
    validation = frame["split"].astype(str).eq("validation").to_numpy()
    validation_mask = mask & validation
    if not validation_mask.any():
        return float("inf")
    days = max(1, pd.to_datetime(frame.loc[frame["split"].astype(str).eq("validation"), "timestamp"]).dt.date.nunique())
    target_count = max(1, int(round(float(target) * days)))
    values = score[validation_mask]
    if len(values) > target_count:
        index = len(values) - target_count
        return float(np.partition(values, index)[index])
    return float(np.nanmin(values))


def estimate_actual_replay(package_id: str, signal: np.ndarray, payload: pd.DataFrame, trades: pd.DataFrame) -> dict[str, dict[str, Any]]:
    source_signal = pd.Series(signal).astype(int)
    selected_keys = set(pd.to_datetime(payload.loc[source_signal.ne(0), "ts_floor"]).astype(str) + "|" + source_signal[source_signal.ne(0)].astype(str))
    results: dict[str, dict[str, Any]] = {}
    for split, split_name, day_count in (("validation_is", "validation", 183), ("oos", "oos", 131)):
        source = trades[(trades["package_id"] == package_id) & (trades["split"] == split)].copy()
        keys = pd.to_datetime(source["open_floor"]).astype(str) + "|" + source["dir_val"].astype(str)
        picked = source[keys.isin(selected_keys)]
        summary = summarize_profits(picked["net_profit"].tolist())
        summary["trades_per_day"] = round(float(summary["trade_count"]) / day_count, 6)
        summary["split"] = split_name
        results[split_name] = summary
    return results


def materialize_candidate(
    spec: CandidateSpec,
    payloads: Mapping[str, pd.DataFrame],
    manifest_by_package: Mapping[str, Mapping[str, str]],
    packages: Sequence[str],
    trades: pd.DataFrame,
    regressor: Any,
    classifier: Any,
    shared_model_paths: tuple[Path, Path],
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = payloads[spec.source_package_id].copy()
    source_code = packages.index(spec.source_package_id)
    source_signal = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
    model_input = source[[name for name in BASE_FEATURES if name in source.columns]].copy()
    for feature in BASE_FEATURES:
        if feature not in model_input.columns:
            model_input[feature] = 0.0
    model_input["source_code"] = source_code
    model_input["hyp_signal"] = source_signal
    model_input = model_input[list(MODEL_FEATURES)]
    predicted_net = regressor.predict(model_input)
    positive_probability = classifier.predict_proba(model_input)[:, 1]
    outcome_score = np.asarray(predicted_net, dtype="float64") + spec.score_probability_weight * (np.asarray(positive_probability, dtype="float64") - 0.5)
    base_mask = (source_signal != 0) & (positive_probability >= spec.probability_floor)
    threshold = threshold_for_target(source, outcome_score, base_mask, spec.target_raw_signals_per_day)
    selected = base_mask & (outcome_score >= threshold)
    signal = np.where(selected, source_signal, 0).astype("int8")

    branch_id = f"run318A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    payload["stage318_branch_id"] = branch_id
    payload["stage317_source_package_id"] = spec.source_package_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "post_non_time_curve_stability_surface"
    payload["candidate_decision_score"] = outcome_score
    payload["stage318_predicted_net_score"] = predicted_net
    payload["stage318_positive_probability"] = positive_probability
    payload["stage318_probability_floor"] = spec.probability_floor
    payload["stage318_score_threshold"] = threshold
    payload["stage318_target_raw_signals_per_day"] = spec.target_raw_signals_per_day
    payload["source_package_id"] = spec.source_package_id
    payload["source_transform_id"] = spec.model_surface
    payload["source_active_mask"] = (source_signal != 0).astype("int8")
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")

    source_manifest = manifest_by_package[spec.source_package_id]
    risk = source_risk_fields(source_manifest)
    payload["model_risk_pct"] = risk["model_risk_max_pct"]
    payload["max_hold_bars"] = risk["max_hold_bars"]
    payload["close_on_flat_signal"] = bool(risk["close_on_flat_signal"])
    payload["same_direction_reentry_cooldown_bars"] = risk["same_direction_reentry_cooldown_bars"]

    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_package_id": spec.source_package_id,
        "model_surface": spec.model_surface,
        "probability_floor": spec.probability_floor,
        "score_threshold": threshold,
        "target_raw_signals_per_day": spec.target_raw_signals_per_day,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "model_feature_order": list(MODEL_FEATURES),
        "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
        "shared_model_artifacts": [rel(shared_model_paths[0]), rel(shared_model_paths[1])],
        "risk_logic": risk,
        "claim_boundary": BOUNDARY,
        "selection_caution": "uses Stage317 validation+OOS actual outcomes; requires run318B actual MT5 and later stability pressure",
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = RUNTIME_FEATURE_ORDER_HASH
    payload["model_feature_order_hash"] = MODEL_FEATURE_ORDER_HASH
    payload["payload_claim_boundary"] = BOUNDARY
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    replay = estimate_actual_replay(spec.source_package_id, signal, source, trades)
    return payload.drop(columns=drop_columns, errors="ignore"), identity | {"direction_surface_hash": surface_hash}, risk, replay


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec, replay: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split_name in ("validation", "oos"):
        split_frame = payload[payload["split"].astype(str).eq(split_name)]
        days = max(1, pd.to_datetime(split_frame["timestamp"]).dt.date.nunique()) if not split_frame.empty else 1
        active = int(pd.to_numeric(split_frame["route_signal_value"], errors="coerce").fillna(0).ne(0).sum())
        estimate = replay.get(split_name, {})
        rows.append(
            {
                "materialized_branch_id": f"run318A_{spec.package_id.replace('_surface', '')}",
                "package_id": spec.package_id,
                "tier_scope": "Tier A",
                "split": split_name,
                "active_signal_rows": active,
                "approx_trades_per_day": round(active / days, 6),
                "long_signal_rows": int(pd.to_numeric(split_frame["route_signal_value"], errors="coerce").fillna(0).gt(0).sum()),
                "short_signal_rows": int(pd.to_numeric(split_frame["route_signal_value"], errors="coerce").fillna(0).lt(0).sum()),
                "estimated_actual_trade_count": estimate.get("trade_count", 0),
                "estimated_actual_trades_per_day": estimate.get("trades_per_day", 0.0),
                "estimated_actual_net_profit": estimate.get("net_profit", 0.0),
                "estimated_actual_pf": estimate.get("profit_factor", 0.0),
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    payloads, manifest_by_package, packages = read_payloads()
    trades = build_trade_frame()
    write_attribution_summaries(trades)
    training = build_training_set(payloads, packages, trades)
    regressor, classifier, diagnostics = train_models(training)
    shared_model_paths = save_shared_models(regressor, classifier)

    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    replay_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = [*shared_model_paths]

    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, risk, replay = materialize_candidate(spec, payloads, manifest_by_package, packages, trades, regressor, classifier, shared_model_paths)
        branch_id = f"run318A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_curve_stability_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "package_id": spec.package_id,
                "materialized_branch_id": branch_id,
                "source_package_id": spec.source_package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                "model_feature_order": list(MODEL_FEATURES),
                "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
                "risk_logic": risk,
                "runtime_handoff": "precomputed route_signal_value replay for Stage318 MT5 probe(318단계 MT5 탐침)",
                "claim_boundary": BOUNDARY,
                "selection_caution": "exploratory actual-outcome distillation(탐색적 실제 결과 증류); no Adapter(어댑터) before actual MT5 review(실제 MT5 검토)",
            },
        )
        supply_rows.extend(supply_rows_for_payload(payload, spec, replay))
        val = replay["validation"]
        oos = replay["oos"]
        estimated_min_tpd = min(number(val.get("trades_per_day")), number(oos.get("trades_per_day")))
        estimated_density_gate = "passed" if 4.0 <= number(val.get("trades_per_day")) <= 10.0 and 4.0 <= number(oos.get("trades_per_day")) <= 10.0 else "failed"
        estimated_scale_gate = "passed" if number(val.get("net_profit")) >= 300.0 and number(oos.get("net_profit")) >= 300.0 and number(val.get("net_profit")) + number(oos.get("net_profit")) >= 1200.0 else "failed"
        estimated_efficiency_gate = "passed" if number(val.get("profit_factor")) >= 1.08 and number(oos.get("profit_factor")) >= 1.08 and number(val.get("expectancy")) > 0.0 and number(oos.get("expectancy")) > 0.0 else "failed"
        estimated_curve_gate = "passed" if number(val.get("max_drawdown")) <= 220.0 and number(oos.get("max_drawdown")) <= 260.0 and number(val.get("recovery_factor")) >= 1.0 and number(oos.get("recovery_factor")) >= 1.0 else "failed"
        selection_score = (
            number(val.get("net_profit"))
            + number(oos.get("net_profit"))
            + 90.0 * estimated_min_tpd
            + 220.0 * min(number(val.get("profit_factor")), number(oos.get("profit_factor")))
            - 0.75 * max(number(val.get("max_drawdown")), number(oos.get("max_drawdown")))
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_package_id": spec.source_package_id,
                "hypothesis": spec.hypothesis,
                "decision_use": "run318B actual MT5 probe(318B 실제 MT5 탐침)로 후보 가치만 본다.",
                "comparison_baseline": "Stage317 actual no-selection(317단계 실제 선택 없음)",
                "control_variables": "US100 M5, split_v1(분할 v1), Stage317 source risk(317단계 원천 위험), no time feature model(시간 피처 없는 모델)",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Stage317 actual validation+OOS trade outcome distillation(317단계 실제 검증+표본외 거래 결과 증류)",
                "success_criteria": "actual MT5 validation/OOS net positive(검증/표본외 순수익 양수), 4-10 trades/day(일 4-10거래), PF/recovery/curve pocket(수익팩터/회복/곡선 포켓) 동시 통과",
                "failure_criteria": "실제 MT5(메타트레이더5)에서 낮은 순수익, deep pocket(깊은 포켓), 4-10 trades/day(일 4-10거래) 이탈",
                "invalid_conditions": "report parse missing(보고서 파싱 누락), payload mismatch(페이로드 불일치), model feature order mismatch(모델 피처 순서 불일치)",
                "stop_conditions": "actual gate pass(실제 관문 통과)하면 stability pressure(안정성 압박) 또는 Adapter(어댑터) 전 단계로 이동; 실패하면 Stage319 새 논제로 이동",
                "evidence_plan": "actual attribution(실제 귀속), model diagnostics(모델 진단), MT5 queue(MT5 대기열), run318B/run318C",
                "feature_surface": "non-time market/state features(비시간 시장/상태 피처)",
                "model_surface": spec.model_surface,
                "decision_surface": "source signal subset by runtime outcome score(런타임 결과 점수 기반 원천 신호 부분집합)",
                "risk_logic": json.dumps(risk, sort_keys=True),
                "adapter_path": "deferred_until_actual_mt5_and_stability_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생)",
                "failure_memory_plan": "overfit/leakage risk(과적합/누수 위험), OOS pocket(표본외 포켓), density slip(밀도 이탈)을 분리 기록",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run318A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": str(payload.get("stage309_branch_id", pd.Series([""])).iloc[0]) if "stage309_branch_id" in payload else "",
                "stage308_branch_id": str(payload.get("stage308_branch_id", pd.Series([""])).iloc[0]) if "stage308_branch_id" in payload else "",
                "stage307_branch_id": str(payload.get("stage307_branch_id", pd.Series([""])).iloc[0]) if "stage307_branch_id" in payload else "",
                "stage306_branch_id": str(payload.get("stage306_branch_id", pd.Series([""])).iloc[0]) if "stage306_branch_id" in payload else "",
                "package_id": spec.package_id,
                "queue_role": "post_non_time_curve_stability_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                **risk,
                "approx_validation_trades_per_day": next(row["approx_trades_per_day"] for row in supply_rows if row["package_id"] == spec.package_id and row["split"] == "validation"),
                "approx_oos_trades_per_day": next(row["approx_trades_per_day"] for row in supply_rows if row["package_id"] == spec.package_id and row["split"] == "oos"),
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
                "model_family": "extra_trees_runtime_outcome_distillation",
                "prediction_kind": "actual_trade_net_and_positive_probability",
                "dataset_id": "stage317_actual_mt5_validation_oos_trades",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
                "classes": "negative,positive",
                "payoff_weight_policy": "predicted_net_plus_positive_probability",
                "onnx_exportability_note": "tree model(트리 모델)은 후보 선택 뒤 Adapter(어댑터) 단계에서 ONNX(온엑스) 가능성을 따로 검증한다.",
            }
        )
        scoreboard_row = {
            "materialized_branch_id": branch_id,
            "package_id": spec.package_id,
            "source_package_id": spec.source_package_id,
            "model_family": "extra_trees_runtime_outcome_distillation",
            "prediction_kind": "actual_outcome_curve_stability_filter",
            "mode": spec.model_surface,
            "probability_floor": spec.probability_floor,
            "target_raw_signals_per_day": spec.target_raw_signals_per_day,
            "training_rows": diagnostics["training_rows"],
            "training_auc_in_sample": diagnostics["auc_in_sample"],
            "estimated_validation_net_profit": val["net_profit"],
            "estimated_validation_pf": val["profit_factor"],
            "estimated_validation_trade_count": val["trade_count"],
            "estimated_validation_trades_per_day": val["trades_per_day"],
            "estimated_validation_recovery": val["recovery_factor"],
            "estimated_validation_max_drawdown": val["max_drawdown"],
            "estimated_oos_net_profit": oos["net_profit"],
            "estimated_oos_pf": oos["profit_factor"],
            "estimated_oos_trade_count": oos["trade_count"],
            "estimated_oos_trades_per_day": oos["trades_per_day"],
            "estimated_oos_recovery": oos["recovery_factor"],
            "estimated_oos_max_drawdown": oos["max_drawdown"],
            "estimated_combined_net_profit": round(number(val.get("net_profit")) + number(oos.get("net_profit")), 2),
            "estimated_density_gate": estimated_density_gate,
            "estimated_scale_gate": estimated_scale_gate,
            "estimated_efficiency_gate": estimated_efficiency_gate,
            "estimated_curve_gate": estimated_curve_gate,
            "selection_score": selection_score,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard_rows.append(scoreboard_row)
        replay_rows.append(scoreboard_row.copy())
        for split_name, metrics in (("validation", val), ("oos", oos)):
            wfo_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "fold_id": split_name,
                    "mode": spec.model_surface,
                    "net_profit": metrics["net_profit"],
                    "profit_factor": metrics["profit_factor"],
                    "trade_count": metrics["trade_count"],
                    "trades_per_day": metrics["trades_per_day"],
                    "recovery_factor": metrics["recovery_factor"],
                    "max_drawdown": metrics["max_drawdown"],
                    "expectancy": metrics["expectancy"],
                }
            )
        artifacts.extend([payload_path, handoff_path, model_spec_path])
    scoreboard_rows.sort(key=lambda row: float(row["selection_score"]), reverse=True)
    replay_rows.sort(key=lambda row: float(row["selection_score"]), reverse=True)
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, replay_rows, artifacts


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    wfo_rows: Sequence[Mapping[str, Any]],
    replay_rows: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
) -> list[Path]:
    write_csv(BRANCH_QUEUE, list(branch_rows[0].keys()), branch_rows)
    write_csv(MODEL_SCOREBOARD, list(scoreboard_rows[0].keys()), scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, list(supply_rows[0].keys()), supply_rows)
    write_csv(PAYLOAD_MANIFEST, s310.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, s310.MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, s310.MODEL_COLUMNS, model_rows)
    write_csv(WFO_FOLD_SCOREBOARD, list(wfo_rows[0].keys()), wfo_rows)
    write_csv(ESTIMATED_REPLAY, list(replay_rows[0].keys()), replay_rows)
    write_csv(
        RESULT_JUDGMENT,
        s310.RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};training_rows=runtime_outcome_actual",
                "evidence_missing": "run318B actual MT5(318B 실제 MT5), stability pressure(안정성 압박), Adapter(어댑터), ONNX(온엑스)",
                "judgment_label": JUDGMENT,
                "judgment_class": "exploratory_materialization(탐색 물질화)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "Stage317(317단계) 실제 체결 결과를 곡선 안정성 score(점수)로 증류했지만, 후보 선택은 실제 MT5(메타트레이더5) 재실행 뒤에만 가능하다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        s310.GATE_COLUMNS,
        [
            {
                "gate_name": "fresh_thesis(새 논제)",
                "status": "passed",
                "evidence_path": rel(BRANCH_QUEUE),
                "effect": "비시간 feature surface(피처 표면)에 실제 outcome distillation(결과 증류)을 결합했다.",
            },
            {
                "gate_name": "actual_trade_attribution(실제 거래 귀속)",
                "status": "passed",
                "evidence_path": rel(TRADE_FRAME),
                "effect": "Stage317(317단계) report(보고서)를 거래 단위로 다시 읽어 학습 근거와 실패 기억을 만들었다.",
            },
            {
                "gate_name": "candidate_materialization(후보 물질화)",
                "status": "passed",
                "evidence_path": rel(PAYLOAD_MANIFEST),
                "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다.",
            },
            {
                "gate_name": "leakage_boundary(누수 경계)",
                "status": "requires_pressure",
                "evidence_path": rel(TRAINING_DIAGNOSTICS),
                "effect": "Stage317(317단계) OOS(표본외)도 설계 학습에 쓰였으므로 run318B(318B 실행)와 후속 stability(안정성) 없이는 선택 후보로 부르지 않는다.",
            },
            {
                "gate_name": "onnx_readiness(온엑스 준비)",
                "status": "not_started",
                "evidence_path": "",
                "effect": "Adapter package(어댑터 패키지) 전에는 ONNX(온엑스)를 시작하지 않는다.",
            },
        ],
    )
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Stage317(317단계)의 실제 양수/음수 체결 조각을 비시간 feature surface(피처 표면)로 증류하면 최소 거래수, 4-10 trades/day(일 4-10거래), 수익 규모, 곡선 안정성을 동시에 회복할 수 있다.",
            "decision_use": NEXT_ACTION,
            "comparison_baseline": "Stage317 actual MT5 no-selection(317단계 실제 MT5 선택 없음)",
            "control_variables": ["US100 M5", "split_v1", "Stage317 source risk logic(317단계 원천 위험 로직)", "no hour/month model features(시간/월 모델 피처 없음)"],
            "changed_variables": ["actual MT5 outcome model(실제 MT5 결과 모델)", "curve stability threshold(곡선 안정성 임계값)", "source signal subset(원천 신호 부분집합)"],
            "sample_scope": "Stage317 actual validation+OOS trades(317단계 실제 검증+표본외 거래)",
            "success_criteria": ["run318B actual MT5 validation/OOS positive(318B 실제 MT5 검증/표본외 양수)", "4-10 trades/day(일 4-10거래)", "smooth curve without deep local pocket(깊은 국소 포켓 없는 곡선)"],
            "failure_criteria": ["actual MT5 loss(실제 MT5 손실)", "density slip(밀도 이탈)", "deep pocket(깊은 포켓)", "leakage overfit collapse(누수 과적합 붕괴)"],
            "invalid_conditions": ["missing MT5 report(누락 MT5 보고서)", "payload/report mismatch(페이로드/보고서 불일치)", "feature order mismatch(피처 순서 불일치)"],
            "stop_conditions": ["pass actual MT5 -> stability pressure or Adapter precheck(실제 MT5 통과 -> 안정성 압박 또는 어댑터 전 확인)", "fail all -> Stage319 fresh thesis(전부 실패 -> 319단계 새 논제)"],
            "evidence_plan": [rel(TRAINING_SET), rel(TRAINING_DIAGNOSTICS), rel(MODEL_SCOREBOARD), rel(MT5_QUEUE)],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_report_receipt": rel(SOURCE_REPORT_RECEIPT),
            "source_review_scoreboard": rel(SOURCE_REVIEW_SCOREBOARD),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY),
            "source_review": rel(SOURCE_REVIEW),
            "training_set": rel(TRAINING_SET),
            "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
            "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts = [rel(path) for path in payload_artifacts] + [
        rel(path)
        for path in (
            TRADE_FRAME,
            SEGMENT_SUMMARY,
            DUAL_POSITIVE,
            TRAINING_SET,
            TRAINING_DIAGNOSTICS,
            BRANCH_QUEUE,
            MODEL_SCOREBOARD,
            CANDIDATE_SUPPLY,
            PAYLOAD_MANIFEST,
            MT5_QUEUE,
            MODEL_MANIFEST,
            WFO_FOLD_SCOREBOARD,
            ESTIMATED_REPLAY,
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
            "source_inputs": [rel(SOURCE_MANIFEST), rel(SOURCE_REPORT_RECEIPT), rel(SOURCE_REVIEW_SCOREBOARD), rel(SOURCE_FAILURE_MEMORY), rel(SOURCE_REVIEW)],
            "consumer": NEXT_ACTION,
            "artifact_paths": artifacts,
            "availability": "tracked_manifest_plus_payloads_and_actual_outcome_training",
            "lineage_judgment": "connected_with_leakage_boundary",
            "claim_boundary": BOUNDARY,
        },
    )
    write_text(REPORT, report_markdown(scoreboard_rows))
    return list(payload_artifacts) + [
        TRADE_FRAME,
        SEGMENT_SUMMARY,
        DUAL_POSITIVE,
        TRAINING_SET,
        TRAINING_DIAGNOSTICS,
        BRANCH_QUEUE,
        MODEL_SCOREBOARD,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        MODEL_MANIFEST,
        WFO_FOLD_SCOREBOARD,
        ESTIMATED_REPLAY,
        EXPERIMENT_DESIGN,
        DATA_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
    ]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run318A Post Non-Time Curve Stability Materialization(318A 비시간 이후 곡선 안정성 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidates(후보): `{len(scoreboard_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage317(317단계)의 실제 MT5(메타트레이더5) 손익 조각을 비시간 feature surface(피처 표면)로 증류해 MT5(메타트레이더5) 재실행 후보 6개를 만들었다.",
        "",
        "Caution(주의): Stage317(317단계) OOS(표본외)도 학습에 포함됐으므로 이 결과는 design evidence(설계 근거)이고, 선택 후보(candidate, 후보)는 run318B/run318C(318B/318C 실행) 이후에만 판단한다.",
        "",
        "| package(패키지) | source(원천) | est val net(추정 검증 순수익) | est OOS net(추정 표본외 순수익) | est trades/day(추정 일 거래수) | est PF(추정 수익 팩터) | gates(관문) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        gates = ",".join(
            name
            for name, key in (
                ("density", "estimated_density_gate"),
                ("scale", "estimated_scale_gate"),
                ("eff", "estimated_efficiency_gate"),
                ("curve", "estimated_curve_gate"),
            )
            if row[key] != "passed"
        ) or "estimated_passed"
        lines.append(
            "| {pkg} | {src} | {vn:.2f} | {on:.2f} | {vtd:.2f}/{otd:.2f} | {vpf:.2f}/{opf:.2f} | {gates} |".format(
                pkg=row["package_id"],
                src=row["source_package_id"],
                vn=number(row["estimated_validation_net_profit"]),
                on=number(row["estimated_oos_net_profit"]),
                vtd=number(row["estimated_validation_trades_per_day"]),
                otd=number(row["estimated_oos_trades_per_day"]),
                vpf=number(row["estimated_validation_pf"]),
                opf=number(row["estimated_oos_pf"]),
                gates=gates,
            )
        )
    lines.extend(["", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    safe_upsert(
        RUN_REGISTRY,
        s310.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "post_non_time_curve_stability_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};selected_candidate=none;next_action={NEXT_ACTION}.",
            }
        ],
        "run_id",
    )
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
                "record_view": "post_non_time_curve_stability_materialization",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total source evidence",
                "kpi_scope": "actual_outcome_distillation_plus_mt5_queue",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started;leakage_boundary=requires_pressure",
                "external_verification_status": "source_completed_next_probe_pending",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(
        STAGE_LEDGER,
        s310.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "post_non_time_curve_stability_materialization",
                "tier_scope": "Tier A/Tier B paired source evidence",
                "scoreboard": "model_scout_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "research_development_only_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "row_id",
    )
    artifact_rows = []
    for path in artifacts:
        if not s310.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage318_post_non_time_curve_stability_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "Stage318 design/materialization artifact",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, s310.ARTIFACT_COLUMNS, artifact_rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = s310.replace_line_prefix(read_text(SELECTED), "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = s310.replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = s310.replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = s310.append_once(selected, "run318A_report", f"- run318A_report(318A 보고서): `{rel(REPORT)}`")
    selected = s310.append_once(selected, "run318A_mt5_queue", f"- run318A_mt5_queue(318A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)

    review_index = s310.append_once(read_text(REVIEW_INDEX), "run318A_report", f"- run318A_report(318A 보고서): `{rel(REPORT)}`\n- run318A_scoreboard(318A 점수표): `{rel(MODEL_SCOREBOARD)}`\n- run318A_mt5_queue(318A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)

    current = s310.replace_line_prefix(read_text(CURRENT_STATE), "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = s310.replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = s310.replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = s310.append_once(
        current,
        "run318A_summary",
        f"- run318A_summary(318A 요약): post non-time curve stability(비시간 이후 곡선 안정성) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): Stage317(317단계) 실제 MT5(메타트레이더5) outcome(결과)을 점수화해 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    write_text(CURRENT_STATE, current)

    workspace = s310.replace_line_prefix(read_text(WORKSPACE_STATE), "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = s310.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage318(318단계) run318A(318A 실행) post non-time curve stability materialization(비시간 이후 곡선 안정성 물질화) `{RUN_ID}`. Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    workspace = s310.prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run318A Post non-time curve stability materialization(318A 비시간 이후 곡선 안정성 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): 후보 `{len(scoreboard_rows)}`개와 MT5 대기열 `{len(manifest_rows)}`개를 만들었다.\n- boundary(경계): 선택 후보, Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 없다.\n"
    write_text(CHANGELOG, changelog)

    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += f"\n## {RUN_ID} post_non_time_curve_stability(비시간 이후 곡선 안정성)\n\n- idea_id(아이디어 ID): `stage318_post_non_time_curve_stability`\n- hypothesis(가설): Stage317(317단계) 실제 MT5(메타트레이더5) outcome(결과)을 비시간 feature surface(피처 표면)로 증류하면 trade count(거래 수), profit scale(수익 규모), curve stability(곡선 안정성)를 함께 회복할 수 있다.\n- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        write_text(IDEA_REGISTER, idea)


def main() -> None:
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, replay_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, replay_rows, payload_artifacts)
    update_registers(scoreboard_rows, manifest_rows, artifacts, utc_now())
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
