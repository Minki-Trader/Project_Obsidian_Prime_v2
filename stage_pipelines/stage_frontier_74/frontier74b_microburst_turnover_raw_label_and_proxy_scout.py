from __future__ import annotations

import csv
import json
import math
import sys
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path"
RUN_ID = "frontier74B_microburst_turnover_raw_label_and_proxy_scout_v1"
PARENT_RUN_ID = "frontier74A_stage_open_new_hypothesis_after_f73_session_regime_negative_memory_v1"
NEXT_REPAIR_RUN_ID = "frontier74C_microburst_label_feature_repair_proxy_v1"
NEXT_PRE_MT5_RUN_ID = "frontier74C_pre_mt5_grok_microburst_turnover_runtime_probe_v1"
STATUS = "proxy_scout_completed_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

F74A_MANIFEST = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F74A_REPORT = REVIEWS_ROOT / "frontier74A_stage_open_microburst_turnover_label_report.md"
FWD12_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD12_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"

ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"

INITIAL_EQUITY = 10000.0
POINT_SIZE = 0.01
POINT_VALUE = 1.0
TARGET_TPD_VALUES = [5.0, 7.0, 9.0]

warnings.filterwarnings("ignore", category=ConvergenceWarning)


@dataclass(frozen=True)
class AxisSpec:
    axis_id: str
    horizon_bars: int
    side: str
    direction: int
    target_atr: float
    stop_atr: float


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, lines: Sequence[str]) -> None:
    write_text(path, "\n".join(lines))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        rows = [{"empty": "true"}]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.rstrip())


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise FileNotFoundError(f"ledger header missing: {path}")
    if key not in fieldnames:
        raise KeyError(f"{key} not found in {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def required_inputs() -> list[Path]:
    return [F74A_MANIFEST, F74A_REPORT, FWD12_INPUT, FWD12_FEATURE_ORDER, RAW_US100, ALPHA_LEDGER, RUN_REGISTRY]


def axis_specs() -> list[AxisSpec]:
    out: list[AxisSpec] = []
    for horizon, target, stop in ((3, 0.35, 0.30), (6, 0.55, 0.40), (9, 0.75, 0.50)):
        out.append(AxisSpec(f"microburst_h{horizon}_long", horizon, "long(롱)", 1, target, stop))
        out.append(AxisSpec(f"microburst_h{horizon}_short", horizon, "short(숏)", -1, target, stop))
    return out


def split_days(timestamps: pd.Series) -> float:
    if timestamps.empty:
        return 1.0
    span = timestamps.max() - timestamps.min()
    return max(float(span.days) + 1.0, 1.0)


def max_drawdown(values: np.ndarray) -> tuple[float, float]:
    if len(values) == 0:
        return 0.0, 0.0
    equity = INITIAL_EQUITY + np.cumsum(values)
    peaks = np.maximum.accumulate(equity)
    drawdowns = peaks - equity
    amount = float(np.max(drawdowns))
    return amount, float(amount / INITIAL_EQUITY * 100.0)


def smoothness_r2(values: np.ndarray) -> float:
    if len(values) < 3:
        return 0.0
    equity = np.cumsum(values)
    x_axis = np.arange(len(equity), dtype=float)
    if np.allclose(equity, equity[0]):
        return 0.0
    corr = np.corrcoef(x_axis, equity)[0, 1]
    return float(0.0 if np.isnan(corr) else corr * corr)


def trade_metrics(timestamps: pd.Series, pnl: np.ndarray, direction: np.ndarray) -> dict[str, Any]:
    count = int(len(pnl))
    days = split_days(timestamps)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(losses.sum()) if len(losses) else 0.0
    profit_factor = float(gross_profit / abs(gross_loss)) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0)
    net = float(pnl.sum())
    dd_amount, dd_percent = max_drawdown(pnl)
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    payoff = float(avg_win / abs(avg_loss)) if avg_loss < 0 else 0.0
    max_loss = 0
    current = 0
    for value in pnl:
        if value < 0:
            current += 1
            max_loss = max(max_loss, current)
        else:
            current = 0
    return {
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor,
        "max_drawdown_amount": dd_amount,
        "max_drawdown_percent": dd_percent,
        "trade_count": count,
        "trades_day": float(count / days),
        "win_rate": float(len(wins) / count) if count else 0.0,
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": payoff,
        "expectancy": float(net / count) if count else 0.0,
        "recovery_factor": float(net / dd_amount) if dd_amount > 0 else (999.0 if net > 0 else 0.0),
        "smoothness_r2": smoothness_r2(pnl),
        "max_consecutive_loss": max_loss,
        "long_trade_count": int(np.sum(direction > 0)),
        "short_trade_count": int(np.sum(direction < 0)),
    }


def load_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(FWD12_INPUT))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return frame.sort_values("timestamp").reset_index(drop=True)


def load_raw() -> pd.DataFrame:
    raw = pd.read_csv(io_path(RAW_US100))
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    return raw.sort_values("time_close_unix").reset_index(drop=True)


def align_raw(frame: pd.DataFrame, raw: pd.DataFrame) -> np.ndarray:
    positions = pd.Series(raw.index.to_numpy(), index=raw["timestamp"])
    return positions.reindex(frame["timestamp"]).to_numpy(dtype=float)


def compute_axis_path(frame: pd.DataFrame, raw: pd.DataFrame, positions: np.ndarray, axis: AxisSpec) -> dict[str, np.ndarray]:
    hit = np.zeros(len(frame), dtype=bool)
    pnl = np.full(len(frame), np.nan)
    first_touch_bar = np.full(len(frame), -1, dtype=int)
    adverse_first = np.zeros(len(frame), dtype=bool)
    atr = pd.to_numeric(frame["atr_14"], errors="coerce").to_numpy(dtype=float)
    open_values = raw["open"].to_numpy(dtype=float)
    high_values = raw["high"].to_numpy(dtype=float)
    low_values = raw["low"].to_numpy(dtype=float)
    close_values = raw["close"].to_numpy(dtype=float)
    spread_cost = pd.to_numeric(raw["spread_points"], errors="coerce").fillna(0).to_numpy(dtype=float) * POINT_SIZE
    max_pos = len(raw) - axis.horizon_bars - 2
    for idx, pos_float in enumerate(positions):
        if not np.isfinite(pos_float):
            continue
        pos = int(pos_float)
        a = atr[idx]
        if pos < 0 or pos > max_pos or not np.isfinite(a) or a <= 0:
            continue
        entry_idx = pos + 1
        exit_idx = pos + axis.horizon_bars
        entry = open_values[entry_idx]
        target = axis.target_atr * a
        stop = axis.stop_atr * a
        realized: float | None = None
        for bar_offset, raw_idx in enumerate(range(entry_idx, exit_idx + 1), start=1):
            if axis.direction > 0:
                hit_stop = low_values[raw_idx] <= entry - stop
                hit_target = high_values[raw_idx] >= entry + target
            else:
                hit_stop = high_values[raw_idx] >= entry + stop
                hit_target = low_values[raw_idx] <= entry - target
            if hit_stop and hit_target:
                realized = -stop
                adverse_first[idx] = True
                first_touch_bar[idx] = bar_offset
                break
            if hit_stop:
                realized = -stop
                adverse_first[idx] = True
                first_touch_bar[idx] = bar_offset
                break
            if hit_target:
                realized = target
                hit[idx] = True
                first_touch_bar[idx] = bar_offset
                break
        if realized is None:
            realized = axis.direction * (close_values[exit_idx] - entry)
        pnl[idx] = (realized - spread_cost[entry_idx]) * POINT_VALUE
    return {
        "hit": hit,
        "pnl": pnl,
        "direction": np.full(len(frame), axis.direction, dtype=int),
        "first_touch_bar": first_touch_bar,
        "adverse_first": adverse_first,
    }


def raw_density_rows(frame: pd.DataFrame, paths: Mapping[str, Mapping[str, np.ndarray]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis in axis_specs():
        path = paths[axis.axis_id]
        finite = np.isfinite(path["pnl"])
        for split in ("train", "validation", "oos"):
            split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool) & finite
            hit_mask = split_mask & path["hit"]
            days = split_days(frame.loc[split_mask, "timestamp"])
            rows.append(
                {
                    "axis_id": axis.axis_id,
                    "split": split,
                    "side": axis.side,
                    "horizon_bars": axis.horizon_bars,
                    "target_atr": axis.target_atr,
                    "stop_atr": axis.stop_atr,
                    "rows": int(split_mask.sum()),
                    "hit_count": int(hit_mask.sum()),
                    "raw_hit_rate": float(hit_mask.sum() / max(split_mask.sum(), 1)),
                    "raw_trades_day": float(hit_mask.sum() / days),
                    "raw_density_gate_ge_2_day": bool(hit_mask.sum() / days >= 2.0),
                    "raw_density_gate_ge_4_day": bool(hit_mask.sum() / days >= 4.0),
                }
            )
    return rows


def feature_order() -> list[str]:
    return [line.strip() for line in read_text(FWD12_FEATURE_ORDER).splitlines() if line.strip()]


def feature_bundles(features: Sequence[str]) -> dict[str, list[str]]:
    features = list(features)
    core_tokens = (
        "log_return",
        "hl_",
        "close_",
        "gap_",
        "return_",
        "ema",
        "sma",
        "rsi",
        "stoch",
        "ppo",
        "roc",
        "trix",
        "atr",
        "bollinger",
        "bb_",
        "historical_vol",
        "adx",
        "di_",
        "supertrend",
        "vortex",
    )
    session = ["is_us_cash_open", "minutes_from_cash_open", "is_first_30m_after_open", "is_last_30m_before_cash_close"]
    micro = [
        "return_zscore_20",
        "hl_zscore_50",
        "return_1_over_atr_14",
        "atr_14_over_atr_50",
        "historical_vol_5_over_20",
        "adx_14",
        "di_spread_14",
        "bb_position_20",
        "bollinger_width_20",
        "rsi_14",
        "rsi_14_slope_3",
        "ppo_hist_12_26_9",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "ema20_ema50_diff",
    ]
    core = [feature for feature in features if feature.startswith(core_tokens)]
    micro = [feature for feature in micro if feature in features]
    session_core = sorted(set(micro + [feature for feature in session if feature in features]))
    return {
        "micro_path_core": micro,
        "session_micro_path": session_core,
        "core_no_external": core,
    }


def model_factories() -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(max_iter=250, class_weight="balanced", C=0.75, random_state=7402),
        ),
        "extra_trees_ref": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(
                n_estimators=70,
                min_samples_leaf=35,
                max_features="sqrt",
                class_weight="balanced_subsample",
                n_jobs=-1,
                random_state=7403,
            ),
        ),
        "hist_gbm": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            HistGradientBoostingClassifier(
                max_iter=90,
                learning_rate=0.055,
                max_leaf_nodes=15,
                l2_regularization=0.02,
                random_state=7404,
            ),
        ),
    }


def gate_thresholds(frame: pd.DataFrame) -> dict[str, float]:
    train = frame["split"].astype(str).eq("train")
    return {
        "vol_median": float(pd.to_numeric(frame.loc[train, "historical_vol_5_over_20"], errors="coerce").median()),
        "adx_median": float(pd.to_numeric(frame.loc[train, "adx_14"], errors="coerce").median()),
    }


def gate_mask(frame: pd.DataFrame, gate_id: str, thresholds: Mapping[str, float]) -> np.ndarray:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    vol = pd.to_numeric(frame["historical_vol_5_over_20"], errors="coerce")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce")
    if gate_id == "all":
        return np.ones(len(frame), dtype=bool)
    if gate_id == "cash_open_90m":
        return ((minutes >= 0) & (minutes <= 90)).fillna(False).to_numpy(dtype=bool)
    if gate_id == "cash_mid_late":
        return ((minutes > 90) & (minutes <= 390)).fillna(False).to_numpy(dtype=bool)
    if gate_id == "vol_adx_active":
        return ((vol >= thresholds["vol_median"]) & (adx >= thresholds["adx_median"] * 0.75)).fillna(False).to_numpy(dtype=bool)
    raise ValueError(f"unknown gate_id={gate_id}")


def train_scores(
    frame: pd.DataFrame,
    features: Sequence[str],
    y: np.ndarray,
    gate: np.ndarray,
    factory: Callable[[], Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    finite_y = np.isfinite(y)
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool) & gate & finite_y
    if int(train_mask.sum()) < 700:
        raise ValueError("too_few_train_rows")
    y_train = y[train_mask].astype(int)
    positives = int(np.sum(y_train == 1))
    negatives = int(np.sum(y_train == 0))
    if positives < 50 or negatives < 50:
        raise ValueError("class_too_small")
    estimator = factory()
    estimator.fit(frame.loc[train_mask, list(features)], y_train)
    score_mask = finite_y
    scores = np.full(len(frame), np.nan)
    if hasattr(estimator, "predict_proba"):
        scores[score_mask] = estimator.predict_proba(frame.loc[score_mask, list(features)])[:, 1]
    else:
        scores[score_mask] = estimator.decision_function(frame.loc[score_mask, list(features)])
    auc = float(roc_auc_score(y_train, scores[train_mask])) if len(np.unique(y_train)) == 2 else 0.0
    return scores, {"train_rows": int(train_mask.sum()), "train_positive_rate": float(np.mean(y_train)), "train_auc": auc}


def score_threshold(scores: np.ndarray, timestamps: pd.Series, target_tpd: float) -> float:
    valid = scores[np.isfinite(scores)]
    if len(valid) == 0:
        return 999.0
    target_count = max(int(round(split_days(timestamps) * target_tpd)), 1)
    target_count = min(target_count, len(valid))
    return float(np.partition(valid, len(valid) - target_count)[len(valid) - target_count])


def lifecycle_filter(frame: pd.DataFrame, selected: np.ndarray, positions: np.ndarray, hold_bars: int) -> np.ndarray:
    out = np.zeros(len(frame), dtype=bool)
    last_exit = -10**9
    order = np.argsort(frame["timestamp"].to_numpy())
    for idx in order:
        if not selected[idx] or not np.isfinite(positions[idx]):
            continue
        pos = int(positions[idx])
        if pos <= last_exit:
            continue
        out[idx] = True
        last_exit = pos + hold_bars
    return out


def evaluate_candidate(
    frame: pd.DataFrame,
    positions: np.ndarray,
    scores: np.ndarray,
    path: Mapping[str, np.ndarray],
    gate: np.ndarray,
    axis: AxisSpec,
    target_tpd: float,
) -> dict[str, Any]:
    validation_mask = frame["split"].astype(str).eq("validation").to_numpy(dtype=bool) & gate & np.isfinite(scores)
    threshold = score_threshold(scores[validation_mask], frame.loc[validation_mask, "timestamp"], target_tpd)
    result: dict[str, Any] = {"score_threshold": threshold}
    for split in ("train", "validation", "oos"):
        raw_mask = (
            frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
            & gate
            & np.isfinite(scores)
            & np.isfinite(path["pnl"])
            & (scores >= threshold)
        )
        mask = lifecycle_filter(frame, raw_mask, positions, axis.horizon_bars)
        metrics = trade_metrics(frame.loc[mask, "timestamp"], path["pnl"][mask], path["direction"][mask])
        for key, value in metrics.items():
            result[f"{split}_{key}"] = value
        result[f"{split}_raw_selected_count_before_lifecycle"] = int(raw_mask.sum())
    return result


def is_scout(row: Mapping[str, Any]) -> bool:
    return (
        row["validation_net_profit"] > 0
        and row["oos_net_profit"] > 0
        and row["validation_profit_factor"] >= 1.10
        and row["oos_profit_factor"] >= 1.10
        and row["validation_max_drawdown_percent"] <= 15.0
        and row["oos_max_drawdown_percent"] <= 15.0
        and row["validation_trades_day"] >= 2.0
        and row["oos_trades_day"] >= 2.0
    )


def is_meaningful(row: Mapping[str, Any]) -> bool:
    return (
        is_scout(row)
        and row["validation_profit_factor"] >= 1.25
        and row["oos_profit_factor"] >= 1.25
        and row["validation_max_drawdown_percent"] <= 10.0
        and row["oos_max_drawdown_percent"] <= 10.0
        and row["validation_trades_day"] >= 3.0
        and row["oos_trades_day"] >= 3.0
    )


def is_final_like(row: Mapping[str, Any]) -> bool:
    return (
        row["validation_profit_factor"] >= 2.0
        and row["oos_profit_factor"] >= 2.0
        and row["validation_max_drawdown_percent"] < 10.0
        and row["oos_max_drawdown_percent"] < 10.0
        and 5.0 <= row["validation_trades_day"] <= 10.0
        and 5.0 <= row["oos_trades_day"] <= 10.0
        and row["oos_smoothness_r2"] >= 0.25
    )


def data_integrity(frame: pd.DataFrame, raw: pd.DataFrame, positions: np.ndarray) -> dict[str, Any]:
    return {
        "data_source": [rel(FWD12_INPUT), rel(RAW_US100)],
        "time_axis": "frame timestamp and raw time_close_unix are UTC bar-close aligned(프레임 timestamp와 원시 time_close_unix는 UTC 봉마감 정렬)",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "frame_rows": int(len(frame)),
            "raw_rows": int(len(raw)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        },
        "missing_or_duplicate_check": {
            "frame_duplicate_timestamps": int(frame["timestamp"].duplicated().sum()),
            "raw_duplicate_time_close_unix": int(raw["time_close_unix"].duplicated().sum()),
            "aligned_frame_rows": int(np.isfinite(positions).sum()),
        },
        "feature_label_boundary": "features use current/past row; microburst label uses entry at next bar open and future path inside declared horizon(피처는 현재/과거 행, 라벨은 다음 봉 시가 진입과 선언 수평선 내부 미래 경로 사용)",
        "split_boundary": "train/validation/oos inherited from model input split(모델 입력 분할 상속)",
        "leakage_risk": "threshold selection on validation may overfit scout; OOS kept as separate read(검증 임계값 선택은 탐색 과최적화 위험, 표본외는 별도 판독)",
        "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
    }


def model_validation(candidate_rows: Sequence[Mapping[str, Any]], meaningful_count: int) -> dict[str, Any]:
    return {
        "model_family": "logistic_l2, extra_trees_ref, hist_gbm",
        "target_and_label": "microburst first-touch reward-before-risk(마이크로버스트 위험 전 보상 선도달)",
        "split_method": "time holdout scout(시간 홀드아웃 탐색)",
        "selection_metric": "validation score threshold to target trades/day then lifecycle-filtered KPI(검증 점수 임계값으로 일거래 목표 후 생명주기 필터 KPI)",
        "secondary_metrics": ["PF(수익 팩터)", "DD(손실폭)", "trades/day(일거래)", "smoothness_r2(매끄러움 R2)", "validation/OOS pair(검증/표본외 쌍)"],
        "threshold_policy": "searched on validation by target_tpd(검증에서 목표 일거래별 탐색)",
        "overfit_risk": "many axes/bundles/models/gates tried; scout-only claim(많은 축/묶음/모델/게이트 시도, 탐색 전용 주장)",
        "calibration_risk": "scores are ranking signals, not calibrated probabilities(점수는 순위 신호이지 보정 확률 아님)",
        "comparison_baseline": "F73F runtime observation and F74A design boundary(F73F 런타임 관찰과 F74A 설계 경계)",
        "validation_judgment": "proxy_scout_clue" if meaningful_count else "exploratory_no_meaningful_candidate_yet",
        "candidate_rows": len(candidate_rows),
        "meaningful_candidate_count": meaningful_count,
    }


def run_scout() -> dict[str, Any]:
    frame = load_frame()
    raw = load_raw()
    positions = align_raw(frame, raw)
    axes = axis_specs()
    paths = {axis.axis_id: compute_axis_path(frame, raw, positions, axis) for axis in axes}
    raw_rows = raw_density_rows(frame, paths)
    raw_density_pass_axes = sorted(
        {
            row["axis_id"]
            for row in raw_rows
            if row["split"] in {"validation", "oos"} and row["raw_density_gate_ge_2_day"]
        }
    )
    features = feature_order()
    bundles = feature_bundles(features)
    factories = model_factories()
    thresholds = gate_thresholds(frame)
    gate_ids = ["all", "cash_open_90m", "cash_mid_late", "vol_adx_active"]
    candidate_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    selected_cache: dict[str, tuple[np.ndarray, Mapping[str, np.ndarray], AxisSpec, np.ndarray]] = {}
    for axis in axes:
        path = paths[axis.axis_id]
        y = path["hit"].astype(float)
        y[~np.isfinite(path["pnl"])] = np.nan
        for bundle_id, bundle_features in bundles.items():
            if not bundle_features:
                failure_rows.append({"axis_id": axis.axis_id, "feature_bundle": bundle_id, "reason": "empty_feature_bundle"})
                continue
            for gate_id in gate_ids:
                gate = gate_mask(frame, gate_id, thresholds)
                for model_id, factory in factories.items():
                    try:
                        scores, fit_meta = train_scores(frame, bundle_features, y, gate, factory)
                    except Exception as exc:  # noqa: BLE001 - recorded as scout failure evidence.
                        failure_rows.append(
                            {
                                "axis_id": axis.axis_id,
                                "feature_bundle": bundle_id,
                                "gate_id": gate_id,
                                "model_id": model_id,
                                "reason": str(exc),
                            }
                        )
                        continue
                    for target_tpd in TARGET_TPD_VALUES:
                        row = {
                            "candidate_id": f"f74b_{len(candidate_rows):04d}",
                            "axis_id": axis.axis_id,
                            "side": axis.side,
                            "horizon_bars": axis.horizon_bars,
                            "target_atr": axis.target_atr,
                            "stop_atr": axis.stop_atr,
                            "feature_bundle": bundle_id,
                            "feature_count": len(bundle_features),
                            "gate_id": gate_id,
                            "model_id": model_id,
                            "target_trades_day": target_tpd,
                            **fit_meta,
                        }
                        row.update(evaluate_candidate(frame, positions, scores, path, gate, axis, target_tpd))
                        row["scout_clue"] = is_scout(row)
                        row["meaningful_candidate"] = is_meaningful(row)
                        row["final_like_reference_only"] = is_final_like(row)
                        candidate_rows.append(row)
                        selected_cache[row["candidate_id"]] = (scores, path, axis, gate)
    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row["meaningful_candidate"]),
            bool(row["scout_clue"]),
            row["oos_profit_factor"],
            row["oos_net_profit"],
            -row["oos_max_drawdown_percent"],
            row["oos_trades_day"],
        ),
        reverse=True,
    )
    best = ranked[0] if ranked else {}
    selected_rows = selected_trade_rows(frame, positions, selected_cache, best)
    return {
        "frame": frame,
        "raw": raw,
        "positions": positions,
        "raw_density_rows": raw_rows,
        "raw_density_pass_axes": raw_density_pass_axes,
        "candidate_rows": candidate_rows,
        "failure_rows": failure_rows,
        "ranked_rows": ranked,
        "best": best,
        "selected_rows": selected_rows,
        "data_integrity": data_integrity(frame, raw, positions),
    }


def selected_trade_rows(
    frame: pd.DataFrame,
    positions: np.ndarray,
    selected_cache: Mapping[str, tuple[np.ndarray, Mapping[str, np.ndarray], AxisSpec, np.ndarray]],
    best: Mapping[str, Any],
) -> list[dict[str, Any]]:
    if not best:
        return []
    scores, path, axis, gate = selected_cache[str(best["candidate_id"])]
    raw_mask = gate & np.isfinite(scores) & np.isfinite(path["pnl"]) & (scores >= float(best["score_threshold"]))
    mask = lifecycle_filter(frame, raw_mask, positions, axis.horizon_bars)
    selected = frame.loc[mask, ["timestamp", "split", "minutes_from_cash_open"]].copy()
    selected["candidate_id"] = best["candidate_id"]
    selected["axis_id"] = best["axis_id"]
    selected["score"] = scores[mask]
    selected["pnl"] = path["pnl"][mask]
    selected["direction"] = path["direction"][mask]
    return selected.sort_values("timestamp").head(5000).to_dict(orient="records")


def split_summary_rows(rows: Sequence[Mapping[str, Any]], best: Mapping[str, Any]) -> list[dict[str, Any]]:
    if not best:
        return []
    out = []
    for split in ("train", "validation", "oos"):
        out.append(
            {
                "split": split,
                "net_profit": best.get(f"{split}_net_profit"),
                "gross_profit": best.get(f"{split}_gross_profit"),
                "gross_loss": best.get(f"{split}_gross_loss"),
                "profit_factor": best.get(f"{split}_profit_factor"),
                "drawdown_percent": best.get(f"{split}_max_drawdown_percent"),
                "trade_count": best.get(f"{split}_trade_count"),
                "trades_day": best.get(f"{split}_trades_day"),
                "win_rate": best.get(f"{split}_win_rate"),
                "expectancy": best.get(f"{split}_expectancy"),
                "smoothness_r2": best.get(f"{split}_smoothness_r2"),
            }
        )
    return out


def next_action(summary: Mapping[str, Any]) -> tuple[str, str]:
    if int(summary["meaningful_candidate_count"]) > 0:
        return NEXT_PRE_MT5_RUN_ID, "proxy_meaningful_signal_pre_mt5_grok_required(프록시 의미 신호, MT5 전 Grok 필요)"
    if int(summary["scout_clue_count"]) > 0:
        return NEXT_PRE_MT5_RUN_ID, "proxy_scout_clue_pre_mt5_grok_required(프록시 탐색 단서, MT5 전 Grok 필요)"
    return NEXT_REPAIR_RUN_ID, "raw_density_passed_but_proxy_needs_repair(원시 밀도는 통과했지만 프록시 수리 필요)"


def report_lines(created_at: str, summary: Mapping[str, Any], best: Mapping[str, Any], next_run: str) -> list[str]:
    best_line = "none(없음)"
    if best:
        best_line = (
            f"`{best['candidate_id']}` {best['axis_id']} {best['model_id']} "
            f"OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래) "
            f"`{best['oos_net_profit']:.4f}/{best['oos_profit_factor']:.4f}/"
            f"{best['oos_max_drawdown_percent']:.4f}/{best['oos_trades_day']:.4f}`"
        )
    return [
        "# Frontier74B Raw Label And Proxy Scout(F74B 원시 라벨 및 프록시 탐색)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        f"- next_run_id(다음 실행 ID): `{next_run}`",
        "",
        "## Hypothesis(가설)",
        "",
        "microburst first-touch reward-before-risk labels(마이크로버스트 위험 전 보상 선도달 라벨)이 raw density(원시 밀도)를 먼저 통과하고, lifecycle-aware proxy(생명주기 인식 프록시)에서도 더 촘촘하고 매끄러운 경로를 만들 수 있는지 시험했다.",
        "",
        "## KPI Summary(KPI 요약)",
        "",
        f"- raw_density_pass_axes(원시 밀도 통과 축): `{summary['raw_density_pass_axis_count']}`",
        f"- candidate_rows(후보 행): `{summary['candidate_count']}`",
        f"- scout_clue_count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary['meaningful_candidate_count']}`",
        f"- final_like_reference_only(최종 유사 참조 전용): `{summary['final_like_reference_only_count']}`",
        f"- best_candidate(최선 후보): {best_line}",
        "",
        "## Boundary(경계)",
        "",
        "This is proxy_scout_only(프록시 탐색 전용) and has no MT5 Runtime Probe(MT5 런타임 탐침) yet. Therefore no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
    ]


def update_ledgers(created_at: str, summary: Mapping[str, Any], best: Mapping[str, Any], next_run: str, judgment: str) -> None:
    report = REVIEWS_ROOT / "frontier74B_microburst_turnover_raw_label_and_proxy_scout_report.md"
    manifest = RUN_ROOT / "run_manifest.json"
    audit = REVIEWS_ROOT / "required_gate_coverage_audit_f74b.md"
    row = {
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "row_id": f"{RUN_ID}__proxy_scout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "raw_label_and_proxy_scout(원시 라벨 및 프록시 탐색)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)",
        "view": "proxy_scout(프록시 탐색)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "tier": "Tier A separate(티어 A 분리)",
        "kpi_scope": "raw_density_and_proxy_kpi(원시 밀도 및 프록시 KPI)",
        "metric_scope": "proxy_scout(프록시 탐색)",
        "scoreboard_lane": "trade_shape(거래 형태)",
        "lane": "proxy_scout(프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "status": STATUS,
        "result_status": STATUS,
        "judgment": judgment,
        "result_judgment": judgment,
        "path": rel(report),
        "report_path": rel(report),
        "primary_report": rel(report),
        "primary_artifact": rel(manifest),
        "output_path": rel(manifest),
        "result_path": rel(report),
        "primary_kpi": f"candidates={summary['candidate_count']};scout={summary['scout_clue_count']};meaningful={summary['meaningful_candidate_count']}",
        "guardrail_kpi": f"raw_density_pass_axes={summary['raw_density_pass_axis_count']};final_like={summary['final_like_reference_only_count']}",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(MT5는 다음 검증 범위)",
        "notes": "F74B raw density and lifecycle-aware proxy scout; no authority(F74B 원시 밀도 및 생명주기 인식 프록시 탐색, 권위 없음).",
        "run_number": "frontier74B",
        "date": created_at[:10],
        "run_date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "next_action": next_run,
        "rows": summary["candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_rows": summary["candidate_count"],
        "positive_proxy_rows": summary["scout_clue_count"],
        "best_model_id": best.get("candidate_id", ""),
        "best_proxy_net": best.get("oos_net_profit", ""),
        "best_net_profit": best.get("oos_net_profit", ""),
        "best_profit_factor": best.get("oos_profit_factor", ""),
        "net_profit": best.get("oos_net_profit", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_max_drawdown_percent", ""),
        "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trade_density": best.get("oos_trades_day", ""),
        "expectancy": best.get("oos_expectancy", ""),
        "recovery_factor": best.get("oos_recovery_factor", ""),
        "feature_count": best.get("feature_count", ""),
        "candidate_model_id": best.get("candidate_id", ""),
        "created_at_utc": created_at,
        "required_gate_audit": rel(audit),
        "gate_audit_path": rel(audit),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "microburst_turnover_label_proxy(마이크로버스트 회전 라벨 프록시)",
        "input_run_id": PARENT_RUN_ID,
        "question": "Can raw microburst labels and lifecycle proxy create dense smooth seed surface?(원시 마이크로버스트 라벨과 생명주기 프록시가 조밀하고 매끄러운 씨앗 표면을 만들 수 있나?)",
        "evidence_boundary": "proxy_scout_only_no_runtime(프록시 탐색 전용, 런타임 없음)",
    }
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers(judgment: str, summary: Mapping[str, Any], best: Mapping[str, Any], next_run: str) -> None:
    marker = "<!-- frontier74B_microburst_turnover_raw_label_proxy_scout_v1 -->"
    best_text = "none(없음)"
    if best:
        best_text = (
            f"{best.get('candidate_id')} OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래) "
            f"{best.get('oos_net_profit')}/{best.get('oos_profit_factor')}/{best.get('oos_max_drawdown_percent')}/{best.get('oos_trades_day')}"
        )
    block = f"""<!-- frontier74B_microburst_turnover_raw_label_proxy_scout_v1 -->
- `{RUN_ID}` executed F74 raw label density and proxy scout(F74 원시 라벨 밀도 및 프록시 탐색). Result(결과): `{judgment}`. Raw density pass axes(원시 밀도 통과 축) `{summary['raw_density_pass_axis_count']}`, candidates(후보) `{summary['candidate_count']}`, scout clues(탐색 단서) `{summary['scout_clue_count']}`, meaningful candidates(의미 후보) `{summary['meaningful_candidate_count']}`. Best(최선): {best_text}. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state(created_at: str, judgment: str, next_run: str) -> None:
    workspace_state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {next_run}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {judgment}",
        f"next_run_id: {next_run}",
        "runtime_probe_status: f74_proxy_scout_completed_runtime_probe_pending_if_signal",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f73_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F74B raw label density/proxy scout(원시 라벨 밀도/프록시 탐색)를 실행했다."',
        '  - "Effect(효과): 라벨 자체 밀도와 생명주기 인식 프록시 KPI를 분리해서 다음 수리 또는 MT5 전 검토 행동을 정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    write_text(WORKSPACE_STATE, "\n".join(workspace_state))
    write_md(
        SELECTED_ROOT / "selection_status.md",
        [
            "# F74 Selection Status(F74 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{next_run}`",
            f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
            f"- status(상태): `{STATUS}`",
            f"- judgment(판정): `{judgment}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            f"- next_action(다음 행동): `{next_run}`",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`",
        ],
    )
    write_md(
        CURRENT_WORKING_STATE,
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {created_at}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            f"Current run(현재 실행): `{next_run}`",
            f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F74B raw label density/proxy scout(원시 라벨 밀도/프록시 탐색)를 실행했다.",
            "",
            f"Effect(효과): 다음 실행을 `{next_run}`로 설정했다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def gate_audit_lines(created_at: str, summary: Mapping[str, Any], next_reason: str) -> list[str]:
    return [
        "# F74B Required Gate Coverage Audit(F74B 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        f"| raw label density gate(원시 라벨 밀도 게이트) | `{'pass(통과)' if summary['raw_density_pass_axis_count'] else 'fail(실패)'}` | pass axes(통과 축) `{summary['raw_density_pass_axis_count']}` |",
        "| proxy KPI measurement(프록시 KPI 측정) | `pass(통과)` | candidate rows(후보 행) recorded(기록됨). |",
        "| data integrity boundary(데이터 무결성 경계) | `pass_with_boundary(경계 포함 통과)` | next-bar entry and declared horizon(다음 봉 진입과 선언 수평선). |",
        "| model validation boundary(모델 검증 경계) | `pass_scout_only(탐색 전용 통과)` | scores are rank signals, not calibrated probability(점수는 순위 신호이지 보정 확률 아님). |",
        f"| next action routing(다음 행동 배치) | `{next_reason}` | MT5 is not claimed yet(MT5는 아직 주장하지 않음). |",
        "| final claim guard(최종 주장 보호) | `pass(통과)` | no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). |",
    ]


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F74B required material missing: {missing}")

    created_at = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    result = run_scout()
    candidates = result["candidate_rows"]
    ranked = result["ranked_rows"]
    best = result["best"]
    meaningful_count = sum(1 for row in candidates if row.get("meaningful_candidate"))
    scout_count = sum(1 for row in candidates if row.get("scout_clue"))
    final_like_count = sum(1 for row in candidates if row.get("final_like_reference_only"))
    judgment = (
        "proxy_scout_meaningful_candidate_pre_mt5_required_no_authority"
        if meaningful_count
        else ("proxy_scout_clue_pre_mt5_required_no_authority" if scout_count else "raw_density_passed_proxy_repair_required_no_authority")
    )
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": judgment,
        "raw_density_pass_axis_count": len(result["raw_density_pass_axes"]),
        "raw_density_pass_axes": result["raw_density_pass_axes"],
        "candidate_count": len(candidates),
        "failure_count": len(result["failure_rows"]),
        "scout_clue_count": scout_count,
        "meaningful_candidate_count": meaningful_count,
        "final_like_reference_only_count": final_like_count,
        "best_candidate": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    next_run, next_reason = next_action(summary)
    summary["next_run_id"] = next_run
    summary["next_reason"] = next_reason
    model_validation_block = model_validation(candidates, meaningful_count)

    write_csv(RUN_ROOT / "f74b_raw_label_density_table.csv", result["raw_density_rows"])
    write_csv(RUN_ROOT / "f74b_candidate_results.csv", candidates)
    write_csv(RUN_ROOT / "f74b_candidate_results_ranked_top50.csv", ranked[:50])
    write_csv(RUN_ROOT / "f74b_failure_rows.csv", result["failure_rows"] or [{"reason": "none"}])
    write_csv(RUN_ROOT / "f74b_selected_trades_top_candidate.csv", result["selected_rows"] or [{"empty": "true"}])
    write_json(RUN_ROOT / "f74b_summary.json", summary)
    write_json(RUN_ROOT / "f74b_data_integrity.json", result["data_integrity"])
    write_json(RUN_ROOT / "f74b_model_validation.json", model_validation_block)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": next_run,
            "status": STATUS,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "external_verification_status": "out_of_scope_by_claim_proxy_only(MT5는 다음 검증 범위)",
            "artifacts": {
                "raw_density": rel(RUN_ROOT / "f74b_raw_label_density_table.csv"),
                "candidates": rel(RUN_ROOT / "f74b_candidate_results.csv"),
                "summary": rel(RUN_ROOT / "f74b_summary.json"),
            },
        },
    )

    write_csv(REVIEWS_ROOT / "f74b_raw_label_density_table.csv", result["raw_density_rows"])
    write_csv(REVIEWS_ROOT / "f74b_candidate_results_ranked_top50.csv", ranked[:50])
    write_csv(REVIEWS_ROOT / "f74b_split_summary_best_candidate.csv", split_summary_rows(candidates, best))
    write_json(REVIEWS_ROOT / "f74b_summary.json", summary)
    write_json(REVIEWS_ROOT / "f74b_data_integrity.json", result["data_integrity"])
    write_json(REVIEWS_ROOT / "f74b_model_validation.json", model_validation_block)
    write_md(REVIEWS_ROOT / "frontier74B_microburst_turnover_raw_label_and_proxy_scout_report.md", report_lines(created_at, summary, best, next_run))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f74b.md", gate_audit_lines(created_at, summary, next_reason))

    update_ledgers(created_at, summary, best, next_run, judgment)
    update_registers(judgment, summary, best, next_run)
    update_state(created_at, judgment, next_run)

    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
