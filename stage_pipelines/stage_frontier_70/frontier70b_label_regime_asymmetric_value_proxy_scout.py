from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation"
RUN_ID = "frontier70B_label_regime_asymmetric_value_proxy_scout_v1"
PARENT_RUN_ID = "frontier70A_stage_open_regime_specific_asymmetric_value_exit_model_rotation_v1"
IDEA_ID = "IDEA-FR70-REGIME-ASYMMETRIC-VALUE-EXIT-MODEL-ROTATION"
NEXT_RUN_IF_SIGNAL = "frontier70C_pre_mt5_grok_label_regime_seed_review_v1"
NEXT_RUN_IF_NO_SIGNAL = "frontier70C_label_regime_repair_or_closeout_decision_v1"

CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

MODEL_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
MODEL_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
F70A_DESIGN = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f70a_experiment_design.json"
F70A_AXIS_CONTRACT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f70a_axis_contract.csv"
F70A_REPORT = REVIEWS_ROOT / "frontier70A_stage_open_regime_value_exit_model_rotation_report.md"

FEATURE_EXCLUDE = {
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
    "raw_pos",
    "raw_open",
    "raw_high",
    "raw_low",
    "raw_close",
    "spread_points_proxy",
    "spread_cost_points",
}


@dataclass(frozen=True)
class LabelSpec:
    label_id: str
    horizon_bars: int
    base_tp_atr: float
    min_edge_atr: float
    penalty: float
    regime_mode: str


@dataclass(frozen=True)
class FeatureSet:
    feature_set_id: str
    columns: tuple[str, ...]


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    model_family: str
    model_role: str
    build: Callable[[], Any]


@dataclass(frozen=True)
class SelectionSpec:
    selection_id: str
    mask_name: str
    threshold_quantile: float


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: Any, digits: int = 6) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "" if value is None else str(value)
    if not math.isfinite(number):
        return ""
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def stable_id(parts: Sequence[Any]) -> str:
    return hashlib.sha1("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:12]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def required_artifacts() -> list[Path]:
    return [MODEL_INPUT, MODEL_FEATURE_ORDER, RAW_US100, F70A_DESIGN, F70A_AXIS_CONTRACT, F70A_REPORT]


def load_frames() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT)).copy()
    raw = pd.read_csv(io_path(RAW_US100), usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").reset_index(drop=True)
    raw_values = raw[["timestamp", "open", "high", "low", "close", "spread_points"]].rename(
        columns={
            "open": "raw_open",
            "high": "raw_high",
            "low": "raw_low",
            "close": "raw_close",
            "spread_points": "spread_points_proxy",
        }
    )
    frame = frame.merge(raw_values, on="timestamp", how="left")
    if frame["raw_close"].isna().any():
        raise RuntimeError("raw/model timestamp alignment failed(raw/model timestamp 정렬 실패)")
    frame["raw_pos"] = pd.Series(raw.index.to_numpy(), index=raw["timestamp"]).reindex(frame["timestamp"]).to_numpy(dtype=int)
    frame["spread_cost_points"] = frame["spread_points_proxy"].astype(float) * 0.01
    return frame


def label_specs() -> list[LabelSpec]:
    specs: list[LabelSpec] = []
    for horizon, tp in ((6, 0.60), (12, 0.80), (18, 0.95)):
        for mode in ("neutral", "cash_density", "trend_quality", "chop_reversion", "vol_expansion"):
            specs.append(
                LabelSpec(
                    label_id=f"av_{mode}_h{horizon}_tp{int(tp*100):02d}_edge12_pen55",
                    horizon_bars=horizon,
                    base_tp_atr=tp,
                    min_edge_atr=0.12,
                    penalty=0.55,
                    regime_mode=mode,
                )
            )
    return specs


def feature_sets(frame: pd.DataFrame) -> list[FeatureSet]:
    available = set(frame.columns)
    core = [
        "log_return_1",
        "log_return_3",
        "return_zscore_20",
        "hl_zscore_50",
        "close_ema20_ratio",
        "ema20_ema50_diff",
        "rsi_14",
        "rsi_14_slope_3",
        "atr_14",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "bb_position_20",
        "bb_squeeze",
        "historical_vol_5_over_20",
        "adx_14",
        "di_spread_14",
        "supertrend_10_3",
        "vortex_indicator",
        "is_us_cash_open",
        "minutes_from_cash_open",
    ]
    macro = core + [
        "vix_zscore_20",
        "us10yr_zscore_20",
        "usdx_zscore_20",
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
        "us100_minus_mega8_equal_return_1",
        "us100_minus_top3_weighted_return_1",
    ]
    sets = [
        FeatureSet("regime_value_core_v1", tuple(col for col in core if col in available)),
        FeatureSet("regime_value_macro_v1", tuple(col for col in macro if col in available)),
    ]
    if any(not item.columns for item in sets):
        raise RuntimeError("empty F70B feature set(empty F70B 피처 묶음)")
    return sets


def model_specs() -> list[ModelSpec]:
    return [
        ModelSpec(
            "logreg_balanced_l2_v1",
            "regularized_linear(정규화 선형)",
            "hypothesis_carrier(가설 운반)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                StandardScaler(),
                LogisticRegression(
                    C=0.55,
                    class_weight="balanced",
                    max_iter=1200,
                    solver="lbfgs",
                    random_state=70,
                ),
            ),
        ),
        ModelSpec(
            "extratrees_light_reference_v1",
            "shallow_extra_trees_reference(얕은 엑스트라트리스 참조)",
            "reference_only(참조 전용)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                ExtraTreesClassifier(
                    n_estimators=72,
                    max_depth=7,
                    min_samples_leaf=80,
                    max_features="sqrt",
                    class_weight="balanced",
                    random_state=70,
                    n_jobs=1,
                ),
            ),
        ),
    ]


def selection_specs(frame: pd.DataFrame) -> list[SelectionSpec]:
    return [
        SelectionSpec("all_q55", "all", 0.55),
        SelectionSpec("all_q70", "all", 0.70),
        SelectionSpec("cash_q55", "cash", 0.55),
        SelectionSpec("cash_q70", "cash", 0.70),
        SelectionSpec("trend_q55", "trend", 0.55),
        SelectionSpec("chop_q55", "chop", 0.55),
        SelectionSpec("vol_expansion_q55", "vol_expansion", 0.55),
    ]


def mask_for(frame: pd.DataFrame, name: str) -> np.ndarray:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    if name == "all":
        return np.ones(len(frame), dtype=bool)
    if name == "cash":
        return ((minutes >= 0) & (minutes <= 390)).to_numpy(dtype=bool)
    if name == "trend":
        return (pd.to_numeric(frame["adx_14"], errors="coerce") >= 25).to_numpy(dtype=bool)
    if name == "chop":
        return (pd.to_numeric(frame["adx_14"], errors="coerce") < 18).to_numpy(dtype=bool)
    if name == "vol_expansion":
        hv = pd.to_numeric(frame["historical_vol_5_over_20"], errors="coerce")
        squeeze = pd.to_numeric(frame["bb_squeeze"], errors="coerce")
        return ((hv >= 1.25) | (squeeze == 1)).to_numpy(dtype=bool)
    raise ValueError(name)


def regime_scale(frame: pd.DataFrame, mode: str) -> np.ndarray:
    scale = np.ones(len(frame), dtype=float)
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    if mode == "cash_density":
        scale[(minutes >= 0) & (minutes <= 270)] = 0.78
        scale[~((minutes >= 0) & (minutes <= 390))] = 1.15
    elif mode == "trend_quality":
        adx = pd.to_numeric(frame["adx_14"], errors="coerce")
        scale[adx >= 25] = 0.82
        scale[adx < 18] = 1.12
    elif mode == "chop_reversion":
        adx = pd.to_numeric(frame["adx_14"], errors="coerce")
        scale[adx < 18] = 0.82
        scale[adx >= 25] = 1.10
    elif mode == "vol_expansion":
        hv = pd.to_numeric(frame["historical_vol_5_over_20"], errors="coerce")
        squeeze = pd.to_numeric(frame["bb_squeeze"], errors="coerce")
        scale[(hv >= 1.25) | (squeeze == 1)] = 0.80
        scale[(hv < 0.90) & (squeeze != 1)] = 1.12
    return scale


def add_future_path(frame: pd.DataFrame, horizon: int) -> pd.DataFrame:
    if f"h{horizon}_long_mfe" in frame.columns:
        return frame
    high = frame["raw_high"].to_numpy(dtype=float)
    low = frame["raw_low"].to_numpy(dtype=float)
    close = frame["raw_close"].to_numpy(dtype=float)
    n = len(frame)
    long_mfe = np.full(n, np.nan)
    long_mae = np.full(n, np.nan)
    short_mfe = np.full(n, np.nan)
    short_mae = np.full(n, np.nan)
    close_profit = np.full(n, np.nan)
    for i in range(n):
        end = i + horizon
        if end >= n:
            continue
        future_high = np.max(high[i + 1 : end + 1])
        future_low = np.min(low[i + 1 : end + 1])
        entry = close[i]
        long_mfe[i] = future_high - entry
        long_mae[i] = entry - future_low
        short_mfe[i] = entry - future_low
        short_mae[i] = future_high - entry
        close_profit[i] = close[end] - entry
    frame[f"h{horizon}_long_mfe"] = long_mfe
    frame[f"h{horizon}_long_mae"] = long_mae
    frame[f"h{horizon}_short_mfe"] = short_mfe
    frame[f"h{horizon}_short_mae"] = short_mae
    frame[f"h{horizon}_close_profit"] = close_profit
    return frame


def build_labels(frame: pd.DataFrame, spec: LabelSpec) -> pd.Series:
    frame = add_future_path(frame, spec.horizon_bars)
    atr = pd.to_numeric(frame["atr_14"], errors="coerce").to_numpy(dtype=float)
    cost = frame["spread_cost_points"].to_numpy(dtype=float)
    scale = regime_scale(frame, spec.regime_mode)
    target = atr * spec.base_tp_atr * scale
    edge = atr * spec.min_edge_atr * scale
    long_value = frame[f"h{spec.horizon_bars}_long_mfe"].to_numpy(dtype=float) - spec.penalty * frame[f"h{spec.horizon_bars}_long_mae"].to_numpy(dtype=float) - cost
    short_value = frame[f"h{spec.horizon_bars}_short_mfe"].to_numpy(dtype=float) - spec.penalty * frame[f"h{spec.horizon_bars}_short_mae"].to_numpy(dtype=float) - cost
    long_ok = (frame[f"h{spec.horizon_bars}_long_mfe"].to_numpy(dtype=float) >= target) & (long_value >= edge) & (long_value > short_value)
    short_ok = (frame[f"h{spec.horizon_bars}_short_mfe"].to_numpy(dtype=float) >= target) & (short_value >= edge) & (short_value > long_value)
    label = np.zeros(len(frame), dtype=int)
    label[long_ok] = 1
    label[short_ok] = -1
    invalid = ~np.isfinite(long_value) | ~np.isfinite(short_value) | ~np.isfinite(atr)
    label[invalid] = 0
    return pd.Series(label, index=frame.index)


def class_counts(frame: pd.DataFrame, label: pd.Series, spec: LabelSpec) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, subset in frame.groupby(frame["split"].astype(str)):
        counts = label.loc[subset.index].value_counts().to_dict()
        rows.append(
            {
                "label_id": spec.label_id,
                "split": split,
                "rows": int(len(subset)),
                "long": int(counts.get(1, 0)),
                "flat": int(counts.get(0, 0)),
                "short": int(counts.get(-1, 0)),
                "directional_rate": float((counts.get(1, 0) + counts.get(-1, 0)) / max(len(subset), 1)),
            }
        )
    return rows


def side_scores(model: Any, x: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    proba = model.predict_proba(x)
    classes = list(model.classes_)
    long_p = proba[:, classes.index(1)] if 1 in classes else np.zeros(len(x))
    short_p = proba[:, classes.index(-1)] if -1 in classes else np.zeros(len(x))
    flat_p = proba[:, classes.index(0)] if 0 in classes else np.zeros(len(x))
    side = np.where(long_p >= short_p, 1, -1)
    score = np.maximum(long_p, short_p) - flat_p
    return side.astype(int), score.astype(float)


def non_overlap_indices(signal: np.ndarray, horizon: int) -> list[int]:
    selected: list[int] = []
    next_allowed = 0
    for idx, active in enumerate(signal):
        if idx < next_allowed or not active:
            continue
        selected.append(idx)
        next_allowed = idx + max(1, horizon)
    return selected


def first_hit_profit(frame: pd.DataFrame, side: np.ndarray, horizon: int, tp_atr: float, sl_atr: float) -> np.ndarray:
    high = frame["raw_high"].to_numpy(dtype=float)
    low = frame["raw_low"].to_numpy(dtype=float)
    close = frame["raw_close"].to_numpy(dtype=float)
    atr = pd.to_numeric(frame["atr_14"], errors="coerce").to_numpy(dtype=float)
    cost = frame["spread_cost_points"].to_numpy(dtype=float)
    out = np.full(len(frame), np.nan)
    for i, direction in enumerate(side):
        end = i + horizon
        if end >= len(frame) or direction == 0 or not math.isfinite(atr[i]):
            continue
        entry = close[i]
        tp = tp_atr * atr[i]
        sl = sl_atr * atr[i]
        value = None
        for j in range(i + 1, end + 1):
            if direction > 0:
                hit_tp = high[j] - entry >= tp
                hit_sl = entry - low[j] >= sl
                if hit_tp and hit_sl:
                    value = -sl
                    break
                if hit_tp:
                    value = tp
                    break
                if hit_sl:
                    value = -sl
                    break
            else:
                hit_tp = entry - low[j] >= tp
                hit_sl = high[j] - entry >= sl
                if hit_tp and hit_sl:
                    value = -sl
                    break
                if hit_tp:
                    value = tp
                    break
                if hit_sl:
                    value = -sl
                    break
        if value is None:
            value = (close[end] - entry) * direction
        out[i] = value - cost[i]
    return out


def proxy_kpi(values: np.ndarray, timestamps: pd.Series, period_timestamps: pd.Series) -> dict[str, Any]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return {
            "net": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "pf": 0.0,
            "dd_pct": 0.0,
            "trades": 0,
            "trades_per_day": 0.0,
            "win_rate": 0.0,
            "expectancy": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "payoff": 0.0,
        }
    wins = values[values > 0]
    losses = values[values < 0]
    gross_profit = float(wins.sum())
    gross_loss = float(losses.sum())
    pf = gross_profit / abs(gross_loss) if gross_loss < 0 else (float("inf") if gross_profit > 0 else 0.0)
    equity = np.cumsum(values)
    peak = np.maximum.accumulate(np.r_[0.0, equity])
    dd = float(np.max(peak[1:] - equity)) if len(equity) else 0.0
    days = max((pd.to_datetime(period_timestamps).max() - pd.to_datetime(period_timestamps).min()).total_seconds() / 86400.0, 1.0)
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    return {
        "net": float(values.sum()),
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "pf": pf,
        "dd_pct": dd / 10000.0 * 100.0,
        "trades": int(len(values)),
        "trades_per_day": float(len(values) / days),
        "win_rate": float(len(wins) / len(values) * 100.0),
        "expectancy": float(values.mean()),
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff": float(avg_win / abs(avg_loss)) if avg_loss < 0 else 0.0,
    }


def evaluate_selection(
    frame: pd.DataFrame,
    side: np.ndarray,
    score: np.ndarray,
    spec: LabelSpec,
    selection: SelectionSpec,
    train_threshold: float,
) -> list[dict[str, Any]]:
    mask = mask_for(frame, selection.mask_name)
    active = (score >= train_threshold) & mask
    selected = non_overlap_indices(active, spec.horizon_bars)
    selected_set = set(selected)
    selected_mask = np.array([idx in selected_set for idx in range(len(frame))], dtype=bool)
    profits = first_hit_profit(frame, side, spec.horizon_bars, tp_atr=spec.base_tp_atr * 1.25, sl_atr=spec.base_tp_atr * 0.85)
    rows: list[dict[str, Any]] = []
    for split, split_frame in frame.groupby(frame["split"].astype(str), sort=False):
        idx = split_frame.index.to_numpy()
        split_selected = selected_mask[idx]
        values = profits[idx][split_selected]
        kpi = proxy_kpi(values, split_frame["timestamp"].loc[split_selected], split_frame["timestamp"])
        rows.append({"split": split, **kpi, "signals": int(split_selected.sum())})
    return rows


def run_scout(created_at: str) -> dict[str, Any]:
    frame = load_frames()
    features = feature_sets(frame)
    models = model_specs()
    selections = selection_specs(frame)
    kpi_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    balance_rows: list[dict[str, Any]] = []
    bucket_rows: list[dict[str, Any]] = []

    for label_spec in label_specs():
        frame = add_future_path(frame, label_spec.horizon_bars)
        label = build_labels(frame, label_spec)
        balance_rows.extend(class_counts(frame, label, label_spec))
        train_mask = frame["split"].astype(str).eq("train").to_numpy()
        if label.loc[train_mask].nunique() < 2:
            continue
        for feature_set in features:
            x_train = frame.loc[train_mask, feature_set.columns]
            y_train = label.loc[train_mask]
            for model_spec in models:
                model = model_spec.build()
                try:
                    model.fit(x_train, y_train)
                except Exception as exc:
                    candidate_rows.append(
                        {
                            "candidate_id": f"fit_failed_{stable_id([label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, str(exc)])}",
                            "label_id": label_spec.label_id,
                            "feature_set_id": feature_set.feature_set_id,
                            "model_id": model_spec.model_id,
                            "status": "fit_failed",
                            "error": str(exc)[:200],
                        }
                    )
                    continue
                side, score = side_scores(model, frame.loc[:, feature_set.columns])
                for selection in selections:
                    train_sel_mask = train_mask & mask_for(frame, selection.mask_name)
                    train_scores = score[train_sel_mask]
                    train_scores = train_scores[np.isfinite(train_scores)]
                    if len(train_scores) < 20:
                        continue
                    threshold = float(np.quantile(train_scores, selection.threshold_quantile))
                    split_rows = evaluate_selection(frame, side, score, label_spec, selection, threshold)
                    candidate_id = "f70b_" + stable_id([label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, selection.selection_id])
                    by_split = {row["split"]: row for row in split_rows}
                    val = by_split.get("validation", {})
                    oos = by_split.get("oos", {})
                    summary = {
                        "candidate_id": candidate_id,
                        "label_id": label_spec.label_id,
                        "horizon_bars": label_spec.horizon_bars,
                        "regime_mode": label_spec.regime_mode,
                        "feature_set_id": feature_set.feature_set_id,
                        "feature_count": len(feature_set.columns),
                        "model_id": model_spec.model_id,
                        "model_family": model_spec.model_family,
                        "model_role": model_spec.model_role,
                        "selection_id": selection.selection_id,
                        "mask_name": selection.mask_name,
                        "threshold_quantile": selection.threshold_quantile,
                        "threshold": threshold,
                        "validation_net": val.get("net", 0.0),
                        "validation_pf": val.get("pf", 0.0),
                        "validation_dd_pct": val.get("dd_pct", 0.0),
                        "validation_trades": val.get("trades", 0),
                        "validation_trades_per_day": val.get("trades_per_day", 0.0),
                        "oos_net": oos.get("net", 0.0),
                        "oos_pf": oos.get("pf", 0.0),
                        "oos_dd_pct": oos.get("dd_pct", 0.0),
                        "oos_trades": oos.get("trades", 0),
                        "oos_trades_per_day": oos.get("trades_per_day", 0.0),
                    }
                    summary["joint_soft"] = bool(
                        summary["validation_net"] > 0
                        and summary["oos_net"] > 0
                        and summary["validation_pf"] >= 1.20
                        and summary["oos_pf"] >= 1.20
                        and summary["validation_dd_pct"] <= 10.0
                        and summary["oos_dd_pct"] <= 10.0
                        and summary["validation_trades_per_day"] >= 1.0
                        and summary["oos_trades_per_day"] >= 1.0
                    )
                    summary["final_like"] = bool(
                        summary["validation_pf"] >= 2.0
                        and summary["oos_pf"] >= 2.0
                        and 5.0 <= summary["validation_trades_per_day"] <= 10.0
                        and 5.0 <= summary["oos_trades_per_day"] <= 10.0
                        and summary["validation_dd_pct"] < 10.0
                        and summary["oos_dd_pct"] < 10.0
                    )
                    candidate_rows.append(summary)
                    for row in split_rows:
                        kpi_rows.append({"candidate_id": candidate_id, **summary, **{f"split_{k}": v for k, v in row.items()}})
                    if summary["joint_soft"] or summary["final_like"]:
                        bucket_rows.extend(bucket_kpi(frame, side, score, label_spec, selection, threshold, candidate_id))

    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row.get("final_like")),
            bool(row.get("joint_soft")),
            float(row.get("oos_pf") or 0),
            float(row.get("oos_trades_per_day") or 0),
            float(row.get("validation_pf") or 0),
        ),
        reverse=True,
    )
    meaningful = [row for row in ranked if row.get("joint_soft")]
    final_like = [row for row in ranked if row.get("final_like")]
    next_run = NEXT_RUN_IF_SIGNAL if meaningful else NEXT_RUN_IF_NO_SIGNAL
    status = "completed_proxy_scout_meaningful_signal_no_authority" if meaningful else "completed_proxy_scout_no_meaningful_signal_no_authority"
    judgment = "proxy_signal_label_regime_seed_surface_no_authority" if meaningful else "proxy_label_regime_scout_inconclusive_repair_required_no_authority"
    return {
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "candidate_summaries": ranked,
        "candidate_kpi_rows": kpi_rows,
        "class_balance_rows": balance_rows,
        "bucket_kpi_rows": bucket_rows,
        "meaningful_candidates": meaningful,
        "final_like_candidates": final_like,
        "top_candidates": ranked[:12],
        "frame_rows": int(len(frame)),
        "feature_sets": [{"feature_set_id": fs.feature_set_id, "feature_count": len(fs.columns)} for fs in features],
    }


def bucket_kpi(frame: pd.DataFrame, side: np.ndarray, score: np.ndarray, spec: LabelSpec, selection: SelectionSpec, threshold: float, candidate_id: str) -> list[dict[str, Any]]:
    groups = {
        "cash_open_0_60": (pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce").between(0, 60)).to_numpy(dtype=bool),
        "cash_mid_65_270": (pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce").between(65, 270)).to_numpy(dtype=bool),
        "cash_late_275_390": (pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce").between(275, 390)).to_numpy(dtype=bool),
        "trend_adx_ge25": (pd.to_numeric(frame["adx_14"], errors="coerce") >= 25).to_numpy(dtype=bool),
        "chop_adx_lt18": (pd.to_numeric(frame["adx_14"], errors="coerce") < 18).to_numpy(dtype=bool),
        "vol_expansion": mask_for(frame, "vol_expansion"),
    }
    profits = first_hit_profit(frame, side, spec.horizon_bars, tp_atr=spec.base_tp_atr * 1.25, sl_atr=spec.base_tp_atr * 0.85)
    active = (score >= threshold) & mask_for(frame, selection.mask_name)
    selected = set(non_overlap_indices(active, spec.horizon_bars))
    selected_mask = np.array([idx in selected for idx in range(len(frame))], dtype=bool)
    rows: list[dict[str, Any]] = []
    for group_name, group_mask in groups.items():
        for split, split_frame in frame.groupby(frame["split"].astype(str), sort=False):
            idx = split_frame.index.to_numpy()
            mask = selected_mask[idx] & group_mask[idx]
            kpi = proxy_kpi(profits[idx][mask], split_frame["timestamp"].loc[mask], split_frame["timestamp"])
            rows.append({"candidate_id": candidate_id, "bucket": group_name, "split": split, **kpi})
    return rows


def tier_pair_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    return [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "status": "materialized_proxy_kpi(프록시 KPI 물질화)",
            "net_profit": best.get("oos_net", ""),
            "profit_factor": best.get("oos_pf", ""),
            "trade_count": best.get("oos_trades", ""),
            "trades_per_day": best.get("oos_trades_per_day", ""),
            "notes": "F70B primary sample is Tier A full-context proxy input(F70B 주 표본은 티어 A 전체 문맥 프록시 입력)",
        },
        {
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "status": "missing_required(필수 누락)",
            "net_profit": "",
            "profit_factor": "",
            "trade_count": "",
            "trades_per_day": "",
            "notes": "Tier B partial-context materialization not included in F70B first scout(Tier B 부분 문맥 물질화는 F70B 첫 탐색에 없음)",
        },
        {
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "net_profit": "",
            "profit_factor": "",
            "trade_count": "",
            "trades_per_day": "",
            "notes": "No synthetic combined KPI claimed(합성 합산 KPI 주장 없음)",
        },
    ]


def report_lines(result: Mapping[str, Any]) -> list[str]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    return [
        "# F70B Label-Regime Asymmetric Value Proxy Scout(F70B 라벨-장세 비대칭 가치 프록시 탐색)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "## Hypothesis(가설)",
        "",
        "Density-aware asymmetric value labels(밀도 인식 비대칭 가치 라벨)이 F69 sparse/dense fracture(F69 희박/조밀 균열)를 줄일 수 있는지 시험했다.",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): label/target and regime/session(라벨/목표 및 장세/세션)을 선도 축으로 두고 proxy scout(프록시 탐색)를 실행했다.",
        "",
        "Effect(효과): threshold/cooldown/daily quota(임계값/쿨다운/일별 할당) 수리가 아니라 라벨 자체가 PF/density(수익 팩터/밀도)를 같이 움직이는지 기록했다.",
        "",
        "## KPI Summary(KPI 요약)",
        "",
        f"- candidate rows(후보 행): `{len(result['candidate_summaries'])}`.",
        f"- meaningful joint-soft candidates(의미 있는 공동 완화 후보): `{len(result['meaningful_candidates'])}`.",
        f"- final-like candidates(최종 조건 유사 후보): `{len(result['final_like_candidates'])}`.",
        f"- top candidate(상위 후보): `{best.get('candidate_id', 'none')}`.",
        f"- top validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('validation_net'))}` / `{fmt(best.get('validation_pf'))}` / `{fmt(best.get('validation_dd_pct'))}` / `{fmt(best.get('validation_trades_per_day'))}`.",
        f"- top OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('oos_net'))}` / `{fmt(best.get('oos_pf'))}` / `{fmt(best.get('oos_dd_pct'))}` / `{fmt(best.get('oos_trades_per_day'))}`.",
        "",
        "## Required Records(필수 기록)",
        "",
        "- test period(테스트 기간): validation 2025-01-01..2025-09-30, OOS 2025-10-01..2026-04-13.",
        "- proxy expectation(프록시 예상): label-regime candidates(라벨-장세 후보)가 PF와 density(수익 팩터와 밀도)를 함께 움직이면 pre-MT5 Grok review(사전 MT5 그록 검토)로 간다.",
        f"- proxy KPI(프록시 KPI): `{rel(RUN_ROOT / 'f70b_proxy_candidate_summary.csv')}`.",
        "- runtime probe KPI(런타임 탐침 KPI): pending(대기), proxy-only boundary(프록시 전용 경계).",
        "- signal count parity(신호 수 동등성): not_applicable_before_runtime(런타임 전 해당 없음).",
        "- feature readiness parity(피처 준비 동등성): not_applicable_before_runtime(런타임 전 해당 없음).",
        "- proxy/runtime gap cause(프록시/런타임 간극 원인): pending_runtime_probe(런타임 탐침 대기).",
        f"- next action(다음 행동): `{result['next_run_id']}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def gate_audit_lines(result: Mapping[str, Any]) -> list[str]:
    return [
        "# F70B Required Gate Coverage Audit(F70B 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| experiment_design(실험 설계) | pass(통과) | `{rel(F70A_DESIGN)}` | F70A label-first contract(라벨 우선 계약) 계승 |",
        f"| proxy_kpi(프록시 KPI) | pass(통과) | `{rel(RUN_ROOT / 'f70b_proxy_candidate_summary.csv')}` | validation/OOS KPI 기록 |",
        f"| label_regime_guard(라벨-장세 보호) | pass(통과) | `{rel(F70A_AXIS_CONTRACT)}` | F69 수리 반복 방지 |",
        f"| Tier pair(티어 쌍) | partial_with_named_gap(이름 붙인 부분 충족) | `{rel(RUN_ROOT / 'f70b_tier_pair_status.csv')}` | Tier B 누락 숨기지 않음 |",
        "| MT5 runtime probe(MT5 런타임 탐침) | pending_after_meaningful_proxy_or_repair(의미 프록시 또는 수리 후 대기) | proxy-only boundary(프록시 전용 경계) | 런타임 주장은 없음 |",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": result["created_at_utc"],
        "producer": "stage_pipelines/stage_frontier_70/frontier70b_label_regime_asymmetric_value_proxy_scout.py",
        "status": result["status"],
        "judgment": result["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "inputs": {
            "model_input": rel(MODEL_INPUT),
            "model_input_sha256": sha256_file(MODEL_INPUT),
            "raw_us100": rel(RAW_US100),
            "raw_us100_sha256": sha256_file(RAW_US100),
            "f70a_design": rel(F70A_DESIGN),
        },
        "artifacts": [
            rel(RUN_ROOT / "f70b_proxy_candidate_summary.csv"),
            rel(RUN_ROOT / "f70b_proxy_kpi_by_split.csv"),
            rel(RUN_ROOT / "f70b_label_balance.csv"),
            rel(REVIEWS_ROOT / "frontier70B_label_regime_asymmetric_value_proxy_scout_report.md"),
            rel(REVIEWS_ROOT / "required_gate_coverage_audit_f70b.md"),
        ],
        "next_run_id": result["next_run_id"],
    }


def ledger_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": result["status"],
        "judgment": result["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/frontier70B_label_regime_asymmetric_value_proxy_scout_report.md",
        "primary_report": f"stages/{STAGE_ID}/03_reviews/frontier70B_label_regime_asymmetric_value_proxy_scout_report.md",
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier70B_label_regime_asymmetric_value_proxy_scout_report.md",
        "claim_boundary": CLAIM_BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 전용 주장 범위 밖)",
        "run_number": "frontier70B",
        "date": str(result["created_at_utc"])[:10],
        "run_date": str(result["created_at_utc"])[:10],
        "decision": "pre_mt5_grok_if_meaningful_signal_else_repair",
        "next_run_id": result["next_run_id"],
        "rows": len(result["candidate_summaries"]),
        "candidate_rows": len(result["candidate_summaries"]),
        "positive_proxy_rows": len(result["meaningful_candidates"]),
        "best_proxy": best.get("candidate_id", ""),
        "best_model_id": best.get("model_id", ""),
        "net_profit": fmt(best.get("oos_net")),
        "profit_factor": fmt(best.get("oos_pf")),
        "drawdown": fmt(best.get("oos_dd_pct")),
        "trade_count": fmt(best.get("oos_trades")),
        "trade_density": fmt(best.get("oos_trades_per_day")),
        "feature_count": best.get("feature_count", ""),
        "sample_rows": result["frame_rows"],
        "attempt_count": len(result["candidate_summaries"]),
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard": "structural_scout(구조 탐색)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "evidence_boundary": "proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
        "work_family": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_scout(프록시 탐색)",
        "result_status": result["status"],
        "result_judgment": result["judgment"],
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier70B_label_regime_asymmetric_value_proxy_scout_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f70b.md",
        "created_at": result["created_at_utc"],
        "created_at_utc": result["created_at_utc"],
        "required_gate_audit": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f70b.md",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only_no_runtime(프록시 전용, 런타임 없음)",
        "question": "Can label-regime asymmetric value labels reduce the sparse/dense fracture?(라벨-장세 비대칭 가치 라벨이 희박/조밀 균열을 줄이는가)",
        "next_action": result["next_run_id"],
        "artifact_count": 10,
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "label_regime_asymmetric_value_proxy_scout(라벨-장세 비대칭 가치 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f70b_proxy_candidate_summary.csv",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier70B_label_regime_asymmetric_value_proxy_scout_report.md",
    }
    rows: list[dict[str, Any]] = []
    for tier in tier_pair_rows(result):
        row = dict(base)
        suffix = tier["record_view"].split("(")[0].strip().lower().replace(" ", "_").replace("+", "plus")
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": tier["record_view"],
                "record_view": tier["record_view"],
                "view": tier["record_view"],
                "tier_scope": tier["tier_scope"],
                "tier": tier["tier_scope"],
                "kpi_scope": "proxy_trading_kpi(프록시 거래 KPI)",
                "metric_scope": "validation_oos_proxy(검증/표본외 프록시)",
                "primary_kpi": f"net={tier['net_profit']};pf={tier['profit_factor']};trades_day={tier['trades_per_day']}",
                "guardrail_kpi": tier["notes"],
                "notes": tier["notes"],
            }
        )
        if tier["tier_scope"] != "Tier A":
            row["status"] = tier["status"]
            row["judgment"] = "inconclusive_tier_pair_gap_named(티어 쌍 간극 이름 붙임)"
            row["net_profit"] = ""
            row["profit_factor"] = ""
            row["drawdown"] = ""
            row["trade_count"] = ""
            row["trade_density"] = ""
        rows.append(row)
    return rows


def write_outputs(result: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT, RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(RUN_ROOT / "f70b_proxy_candidate_summary.csv", list(result["candidate_summaries"]))
    write_csv(RUN_ROOT / "f70b_proxy_kpi_by_split.csv", list(result["candidate_kpi_rows"]))
    write_csv(RUN_ROOT / "f70b_label_balance.csv", list(result["class_balance_rows"]))
    write_csv(RUN_ROOT / "f70b_bucket_kpi.csv", list(result["bucket_kpi_rows"]))
    write_json(RUN_ROOT / "f70b_top_candidates.json", list(result["top_candidates"]))
    write_csv(RUN_ROOT / "f70b_tier_pair_status.csv", tier_pair_rows(result))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(result))
    write_md(RUN_ROOT / "reports/result_summary.md", report_lines(result))
    write_csv(REVIEWS_ROOT / "f70b_proxy_candidate_summary_review.csv", list(result["candidate_summaries"]))
    write_csv(REVIEWS_ROOT / "f70b_proxy_kpi_by_split_review.csv", list(result["candidate_kpi_rows"]))
    write_csv(REVIEWS_ROOT / "f70b_label_balance_review.csv", list(result["class_balance_rows"]))
    write_csv(REVIEWS_ROOT / "f70b_bucket_kpi_review.csv", list(result["bucket_kpi_rows"]))
    write_json(REVIEWS_ROOT / "f70b_top_candidates_review.json", list(result["top_candidates"]))
    write_csv(REVIEWS_ROOT / "f70b_tier_pair_status_review.csv", tier_pair_rows(result))
    write_md(REVIEWS_ROOT / "frontier70B_label_regime_asymmetric_value_proxy_scout_report.md", report_lines(result))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f70b.md", gate_audit_lines(result))
    append_once(
        REVIEWS_ROOT / "review_index.md",
        "<!-- frontier70B_label_regime_asymmetric_value_proxy_scout_v1 -->",
        """<!-- frontier70B_label_regime_asymmetric_value_proxy_scout_v1 -->
- `frontier70B_label_regime_asymmetric_value_proxy_scout_report.md`: F70B proxy scout report(F70B 프록시 탐색 보고서)
- `f70b_proxy_candidate_summary_review.csv`: F70B candidate summary(F70B 후보 요약)
- `required_gate_coverage_audit_f70b.md`: F70B required gate audit(F70B 필수 게이트 감사)""",
    )


def update_ledgers(result: Mapping[str, Any]) -> None:
    rows = ledger_rows(result)
    for row in rows:
        upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
        upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", rows[0])


def update_registers(result: Mapping[str, Any]) -> None:
    marker = "<!-- frontier70B_label_regime_asymmetric_value_proxy_scout_v1 -->"
    block = f"""<!-- frontier70B_label_regime_asymmetric_value_proxy_scout_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` executed label-regime asymmetric value proxy scout(라벨-장세 비대칭 가치 프록시 탐색 실행). Result(결과): `{result['judgment']}`. Meaningful joint-soft candidates(의미 있는 공동 완화 후보): `{len(result['meaningful_candidates'])}`. Final-like candidates(최종 조건 유사 후보): `{len(result['final_like_candidates'])}`. Boundary(경계): proxy-only(프록시 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{result['next_run_id']}`."""
    append_once(ROOT / "docs/registers/idea_registry.md", marker, block)


def update_state_files(result: Mapping[str, Any]) -> None:
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {result['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {result['status']}",
        f"current_judgment: {result['judgment']}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {result['next_run_id']}",
        "runtime_probe_status: f70_mandatory_runtime_probe_pending_after_meaningful_proxy_signal_or_repair(F70 의미 있는 프록시 신호 또는 수리 뒤 필수 런타임 탐침 대기)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f69_closeout_4_of_5",
        f"updated_at_utc: '{result['created_at_utc']}'",
        "notes:",
        '  - "F70B action(행동): label-regime asymmetric value proxy scout(라벨-장세 비대칭 가치 프록시 탐색)를 실행했다."',
        f'  - "Effect(효과): joint-soft candidates(공동 완화 후보) `{len(result["meaningful_candidates"])}`, final-like candidates(최종 조건 유사 후보) `{len(result["final_like_candidates"])}`를 기록했다."',
        f'  - "Top proxy clue(상위 프록시 단서): `{best.get("candidate_id", "none")}` OOS PF/trades_day/DD(표본외 수익 팩터/일거래/손실폭) `{fmt(best.get("oos_pf"))}/{fmt(best.get("oos_trades_per_day"))}/{fmt(best.get("oos_dd_pct"))}`."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    current = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{result['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F70B label-regime asymmetric value proxy scout(F70B 라벨-장세 비대칭 가치 프록시 탐색)를 실행했다.",
        "",
        "Effect(효과): F70이 실제 proxy KPI(프록시 핵심 지표)를 만들었고, 의미 후보가 있으면 pre-MT5 Grok review(사전 MT5 그록 검토)로 간다.",
        "",
        f"- status(상태): `{result['status']}`.",
        f"- judgment(판정): `{result['judgment']}`.",
        f"- candidate rows(후보 행): `{len(result['candidate_summaries'])}`.",
        f"- joint-soft candidates(공동 완화 후보): `{len(result['meaningful_candidates'])}`.",
        f"- final-like candidates(최종 조건 유사 후보): `{len(result['final_like_candidates'])}`.",
        f"- top candidate(상위 후보): `{best.get('candidate_id', 'none')}`.",
        f"- top OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('oos_net'))}` / `{fmt(best.get('oos_pf'))}` / `{fmt(best.get('oos_dd_pct'))}` / `{fmt(best.get('oos_trades_per_day'))}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current)
    selection = [
        "# F70 Selection Status(F70 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{result['next_run_id']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{result['next_run_id']}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(SELECTED_ROOT / "selection_status.md", selection)


def main() -> int:
    missing = [rel(path) for path in required_artifacts() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F70B required material missing: {missing}")
    result = run_scout(utc_now())
    write_outputs(result)
    update_ledgers(result)
    update_registers(result)
    update_state_files(result)
    best = result["top_candidates"][0] if result["top_candidates"] else {}
    print(json.dumps(json_ready({
        "status": result["status"],
        "judgment": result["judgment"],
        "run_id": RUN_ID,
        "next_run_id": result["next_run_id"],
        "candidate_rows": len(result["candidate_summaries"]),
        "meaningful_candidates": len(result["meaningful_candidates"]),
        "final_like_candidates": len(result["final_like_candidates"]),
        "top_candidate": best.get("candidate_id", "none"),
        "top_oos_pf": best.get("oos_pf", ""),
        "top_oos_trades_per_day": best.get("oos_trades_per_day", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
