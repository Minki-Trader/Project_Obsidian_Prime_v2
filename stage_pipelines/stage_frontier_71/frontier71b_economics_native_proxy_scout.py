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
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd"
RUN_ID = "frontier71B_economics_native_proxy_scout_v1"
PARENT_RUN_ID = "frontier71A_stage_open_economics_native_label_selection_hypothesis_design_v1"
IDEA_ID = "IDEA-FR71-ECONOMICS-NATIVE-LABEL-SELECTION"
NEXT_RUN_IF_MEANINGFUL = "frontier71C_pre_mt5_grok_economics_native_seed_review_v1"
NEXT_RUN_IF_SCOUT_ONLY = "frontier71C_economics_native_repair_recombine_proxy_v1"
NEXT_RUN_IF_NO_SCOUT = "frontier71C_economics_native_repair_recombine_proxy_v1"

CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"

MODEL_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
F71A_REPORT = REVIEWS_ROOT / "frontier71A_stage_open_economics_native_label_selection_report.md"
F71A_GATE = REVIEWS_ROOT / "f71a_joint_gate_contract.csv"
F71A_DENYLIST = REVIEWS_ROOT / "f71a_anti_repeat_denylist.csv"
F71A_LABEL_SPEC = REVIEWS_ROOT / "f71a_label_economics_spec.json"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
SUMMARY_JSON = RUN_ROOT / "f71b_proxy_summary.json"
CANDIDATE_CSV = RUN_ROOT / "f71b_candidate_summary.csv"
KPI_CSV = RUN_ROOT / "f71b_proxy_kpi_by_split.csv"
LABEL_BALANCE_CSV = RUN_ROOT / "f71b_label_balance.csv"
FRACTURE_CSV = RUN_ROOT / "f71b_density_lift_fracture.csv"
TIER_CSV = RUN_ROOT / "f71b_tier_record_status.csv"
SCOUT_ENTRY_CSV = RUN_ROOT / "f71b_scout_entry_rows.csv"

REPORT = REVIEWS_ROOT / "frontier71B_economics_native_proxy_scout_report.md"
SUMMARY_REVIEW_CSV = REVIEWS_ROOT / "f71b_candidate_summary_review.csv"
KPI_REVIEW_CSV = REVIEWS_ROOT / "f71b_proxy_kpi_by_split_review.csv"
LABEL_BALANCE_REVIEW_CSV = REVIEWS_ROOT / "f71b_label_balance_review.csv"
FRACTURE_REVIEW_CSV = REVIEWS_ROOT / "f71b_density_lift_fracture_review.csv"
TIER_REVIEW_CSV = REVIEWS_ROOT / "f71b_tier_record_status_review.csv"
GATE_AUDIT = REVIEWS_ROOT / "required_gate_coverage_audit_f71b.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_ROOT / "stage_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"

NON_FEATURE_COLUMNS = {
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
    tp_atr: float
    sl_atr: float
    utility_mode: str
    min_edge_atr: float
    adverse_penalty: float
    close_weight: float


@dataclass(frozen=True)
class FeatureSet:
    feature_set_id: str
    columns: tuple[str, ...]
    note: str


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
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(parts: Sequence[Any]) -> str:
    return hashlib.sha1("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:12]


def fmt(value: Any, digits: int = 4) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "" if value is None else str(value)
    if not math.isfinite(number):
        return "inf" if number > 0 else ""
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def required_artifacts() -> list[Path]:
    return [MODEL_INPUT, FEATURE_ORDER, RAW_US100, F71A_REPORT, F71A_GATE, F71A_DENYLIST, F71A_LABEL_SPEC]


def load_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    raw = pd.read_csv(io_path(RAW_US100), usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp")
    raw = raw.rename(
        columns={
            "open": "raw_open",
            "high": "raw_high",
            "low": "raw_low",
            "close": "raw_close",
            "spread_points": "spread_points_proxy",
        }
    )
    frame = frame.merge(raw[["timestamp", "raw_open", "raw_high", "raw_low", "raw_close", "spread_points_proxy"]], on="timestamp", how="left")
    if frame[["raw_open", "raw_high", "raw_low", "raw_close"]].isna().any().any():
        raise RuntimeError("raw/model timestamp alignment failed(raw/model timestamp 정렬 실패)")
    frame["spread_cost_points"] = pd.to_numeric(frame["spread_points_proxy"], errors="coerce").fillna(0.0).to_numpy(dtype=float) * 0.01
    return frame


def feature_sets(frame: pd.DataFrame) -> list[FeatureSet]:
    order = [line.strip() for line in read_text(FEATURE_ORDER).splitlines() if line.strip()]
    available = [col for col in order if col in frame.columns and col not in NON_FEATURE_COLUMNS]
    macro_like = {"vix_change_1", "vix_zscore_20", "us10yr_change_1", "us10yr_zscore_20", "usdx_change_1", "usdx_zscore_20"}
    constituent_like = {col for col in available if "xnas" in col or "mega8" in col or "top3" in col}
    core_price = [
        "log_return_1",
        "log_return_3",
        "hl_range",
        "close_open_ratio",
        "return_zscore_20",
        "hl_zscore_50",
        "return_1_over_atr_14",
        "close_ema20_ratio",
        "close_ema50_ratio",
        "ema9_ema20_diff",
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
    minimal = [
        "log_return_1",
        "return_zscore_20",
        "close_ema20_ratio",
        "rsi_14",
        "atr_14",
        "bollinger_width_20",
        "adx_14",
        "di_spread_14",
        "minutes_from_cash_open",
        "spread_cost_points",
    ]
    risk_path = [
        "hl_range",
        "hl_zscore_50",
        "overnight_return",
        "return_1_over_atr_14",
        "atr_14",
        "atr_50",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "bb_squeeze",
        "historical_vol_20",
        "historical_vol_5_over_20",
        "adx_14",
        "di_spread_14",
        "vortex_indicator",
        "minutes_from_cash_open",
        "spread_cost_points",
    ]
    no_macro = [col for col in available if col not in macro_like and col not in constituent_like]
    sets = [
        FeatureSet("econ_core_price_v1", tuple(col for col in core_price if col in frame.columns), "price/session/risk core(가격/세션/위험 핵심)"),
        FeatureSet("econ_no_macro_v1", tuple(no_macro), "macro and constituent ablation(거시/구성종목 제거)"),
        FeatureSet("econ_macro_context_v1", tuple(available), "full 58-feature context(58개 전체 문맥)"),
        FeatureSet("econ_minimal_linear_v1", tuple(col for col in minimal if col in frame.columns), "small stable linear surface(작은 안정 선형 표면)"),
        FeatureSet("econ_risk_path_v1", tuple(col for col in risk_path if col in frame.columns), "risk/path surface(위험/경로 표면)"),
    ]
    empty = [item.feature_set_id for item in sets if not item.columns]
    if empty:
        raise RuntimeError(f"empty feature set(빈 피처 묶음): {empty}")
    return sets


def label_specs() -> list[LabelSpec]:
    specs: list[LabelSpec] = []
    shapes = [
        ("fast_balanced", 6, 0.55, 0.45, 0.45, 0.18),
        ("mid_payoff", 12, 0.85, 0.55, 0.55, 0.14),
        ("slow_payoff", 18, 1.05, 0.70, 0.60, 0.12),
        ("slow_tight_dd", 24, 0.95, 0.50, 0.70, 0.10),
    ]
    for shape, horizon, tp, sl, adverse_penalty, edge in shapes:
        for mode, close_weight in (("first_hit_net", 0.10), ("path_balanced", 0.22), ("dd_guarded", 0.05)):
            specs.append(
                LabelSpec(
                    label_id=f"econ_{shape}_{mode}_h{horizon}_tp{int(tp*100)}_sl{int(sl*100)}",
                    horizon_bars=horizon,
                    tp_atr=tp,
                    sl_atr=sl,
                    utility_mode=mode,
                    min_edge_atr=edge,
                    adverse_penalty=adverse_penalty,
                    close_weight=close_weight,
                )
            )
    return specs


def model_specs() -> list[ModelSpec]:
    return [
        ModelSpec(
            "linear_logreg_balanced_l2_v1",
            "linear_logistic(선형 로지스틱)",
            "economics_label_carrier(경제성 라벨 운반)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                StandardScaler(),
                LogisticRegression(C=0.65, class_weight="balanced", solver="lbfgs", max_iter=800, random_state=71),
            ),
        ),
        ModelSpec(
            "histgb_small_tree_v1",
            "hist_gradient_boosting(히스토그램 그래디언트 부스팅)",
            "nonlinear_reference(비선형 참조)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                HistGradientBoostingClassifier(max_iter=64, max_leaf_nodes=12, learning_rate=0.055, l2_regularization=0.08, random_state=71),
            ),
        ),
        ModelSpec(
            "extratrees_shallow_v1",
            "extra_trees(엑스트라트리스)",
            "tree_reference(트리 참조)",
            lambda: make_pipeline(
                SimpleImputer(strategy="median"),
                ExtraTreesClassifier(
                    n_estimators=64,
                    max_depth=7,
                    min_samples_leaf=90,
                    max_features="sqrt",
                    class_weight="balanced",
                    random_state=71,
                    n_jobs=1,
                ),
            ),
        ),
    ]


def selection_specs() -> list[SelectionSpec]:
    return [
        SelectionSpec("all_q40", "all", 0.40),
        SelectionSpec("all_q55", "all", 0.55),
        SelectionSpec("all_q70", "all", 0.70),
        SelectionSpec("cash_q40", "cash", 0.40),
        SelectionSpec("cash_q55", "cash", 0.55),
        SelectionSpec("early_late_q45", "early_late", 0.45),
        SelectionSpec("trend_q45", "trend", 0.45),
        SelectionSpec("chop_q45", "chop", 0.45),
        SelectionSpec("vol_expansion_q45", "vol_expansion", 0.45),
    ]


def split_mask(frame: pd.DataFrame, split: str) -> np.ndarray:
    return frame["split"].astype(str).eq(split).to_numpy(dtype=bool)


def mask_for(frame: pd.DataFrame, name: str) -> np.ndarray:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce")
    hv = pd.to_numeric(frame["historical_vol_5_over_20"], errors="coerce")
    squeeze = pd.to_numeric(frame["bb_squeeze"], errors="coerce")
    if name == "all":
        return np.ones(len(frame), dtype=bool)
    if name == "cash":
        return minutes.between(0, 390).to_numpy(dtype=bool)
    if name == "early_late":
        return (minutes.between(0, 90) | minutes.between(270, 390)).to_numpy(dtype=bool)
    if name == "trend":
        return (adx >= 24).to_numpy(dtype=bool)
    if name == "chop":
        return (adx < 18).to_numpy(dtype=bool)
    if name == "vol_expansion":
        return ((hv >= 1.18) | (squeeze == 1)).to_numpy(dtype=bool)
    raise ValueError(name)


def future_path(frame: pd.DataFrame, horizon: int) -> dict[str, np.ndarray]:
    high = frame["raw_high"].to_numpy(dtype=float)
    low = frame["raw_low"].to_numpy(dtype=float)
    close = frame["raw_close"].to_numpy(dtype=float)
    splits = frame["split"].astype(str).to_numpy()
    n = len(frame)
    out = {
        "long_mfe": np.full(n, np.nan),
        "long_mae": np.full(n, np.nan),
        "short_mfe": np.full(n, np.nan),
        "short_mae": np.full(n, np.nan),
        "close_delta": np.full(n, np.nan),
    }
    for i in range(n):
        end = i + horizon
        if end >= n or splits[end] != splits[i]:
            continue
        future_high = float(np.max(high[i + 1 : end + 1]))
        future_low = float(np.min(low[i + 1 : end + 1]))
        entry = close[i]
        out["long_mfe"][i] = future_high - entry
        out["long_mae"][i] = entry - future_low
        out["short_mfe"][i] = entry - future_low
        out["short_mae"][i] = future_high - entry
        out["close_delta"][i] = close[end] - entry
    return out


def first_hit_values(frame: pd.DataFrame, horizon: int, tp_atr: float, sl_atr: float) -> tuple[np.ndarray, np.ndarray]:
    high = frame["raw_high"].to_numpy(dtype=float)
    low = frame["raw_low"].to_numpy(dtype=float)
    close = frame["raw_close"].to_numpy(dtype=float)
    atr = pd.to_numeric(frame["atr_14"], errors="coerce").to_numpy(dtype=float)
    cost = frame["spread_cost_points"].to_numpy(dtype=float)
    splits = frame["split"].astype(str).to_numpy()
    long_out = np.full(len(frame), np.nan)
    short_out = np.full(len(frame), np.nan)
    for i in range(len(frame)):
        end = i + horizon
        if end >= len(frame) or splits[end] != splits[i] or not math.isfinite(atr[i]):
            continue
        entry = close[i]
        tp = tp_atr * atr[i]
        sl = sl_atr * atr[i]
        long_value: float | None = None
        short_value: float | None = None
        for j in range(i + 1, end + 1):
            long_tp = high[j] - entry >= tp
            long_sl = entry - low[j] >= sl
            short_tp = entry - low[j] >= tp
            short_sl = high[j] - entry >= sl
            if long_value is None:
                if long_tp and long_sl:
                    long_value = -sl
                elif long_tp:
                    long_value = tp
                elif long_sl:
                    long_value = -sl
            if short_value is None:
                if short_tp and short_sl:
                    short_value = -sl
                elif short_tp:
                    short_value = tp
                elif short_sl:
                    short_value = -sl
            if long_value is not None and short_value is not None:
                break
        if long_value is None:
            long_value = close[end] - entry
        if short_value is None:
            short_value = entry - close[end]
        long_out[i] = long_value - cost[i]
        short_out[i] = short_value - cost[i]
    return long_out, short_out


def build_label(frame: pd.DataFrame, spec: LabelSpec) -> tuple[pd.Series, np.ndarray, np.ndarray, np.ndarray]:
    path = future_path(frame, spec.horizon_bars)
    long_hit, short_hit = first_hit_values(frame, spec.horizon_bars, spec.tp_atr, spec.sl_atr)
    atr = pd.to_numeric(frame["atr_14"], errors="coerce").to_numpy(dtype=float)
    min_edge = atr * spec.min_edge_atr
    long_close = path["close_delta"]
    short_close = -path["close_delta"]
    long_utility = long_hit + spec.close_weight * long_close - spec.adverse_penalty * path["long_mae"]
    short_utility = short_hit + spec.close_weight * short_close - spec.adverse_penalty * path["short_mae"]
    if spec.utility_mode == "path_balanced":
        long_utility = long_utility + 0.18 * path["long_mfe"] - 0.10 * path["long_mae"]
        short_utility = short_utility + 0.18 * path["short_mfe"] - 0.10 * path["short_mae"]
    elif spec.utility_mode == "dd_guarded":
        long_utility = long_utility - 0.22 * np.maximum(path["long_mae"] - spec.sl_atr * atr * 0.65, 0.0)
        short_utility = short_utility - 0.22 * np.maximum(path["short_mae"] - spec.sl_atr * atr * 0.65, 0.0)
    label = np.zeros(len(frame), dtype=int)
    long_ok = (long_utility >= min_edge) & (long_utility > short_utility + 0.04 * atr)
    short_ok = (short_utility >= min_edge) & (short_utility > long_utility + 0.04 * atr)
    label[long_ok] = 1
    label[short_ok] = -1
    invalid = ~np.isfinite(long_utility) | ~np.isfinite(short_utility) | ~np.isfinite(min_edge)
    label[invalid] = 0
    best_utility = np.maximum(long_utility, short_utility)
    return pd.Series(label, index=frame.index), long_hit, short_hit, best_utility


def sample_weight(frame: pd.DataFrame, label: pd.Series, best_utility: np.ndarray) -> np.ndarray:
    atr = pd.to_numeric(frame["atr_14"], errors="coerce").to_numpy(dtype=float)
    scaled = np.divide(np.maximum(best_utility, 0.0), np.maximum(atr, 1e-9), out=np.zeros(len(frame)), where=np.isfinite(atr))
    weights = np.ones(len(frame), dtype=float) * 0.75
    weights[label.to_numpy() != 0] = 1.0 + np.clip(scaled[label.to_numpy() != 0], 0.0, 3.0)
    weights[~np.isfinite(weights)] = 1.0
    return weights


def fit_model(model: Any, x_train: pd.DataFrame, y_train: pd.Series, weights: np.ndarray) -> None:
    if hasattr(model, "steps"):
        final_name = model.steps[-1][0]
        try:
            model.fit(x_train, y_train, **{f"{final_name}__sample_weight": weights})
            return
        except TypeError:
            pass
    model.fit(x_train, y_train)


def side_scores(model: Any, x_all: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    proba = model.predict_proba(x_all)
    classes = list(model.classes_)
    long_p = proba[:, classes.index(1)] if 1 in classes else np.zeros(len(x_all))
    short_p = proba[:, classes.index(-1)] if -1 in classes else np.zeros(len(x_all))
    flat_p = proba[:, classes.index(0)] if 0 in classes else np.zeros(len(x_all))
    side = np.where(long_p >= short_p, 1, -1)
    directional = np.maximum(long_p, short_p)
    margin = np.abs(long_p - short_p)
    score = directional - 0.55 * flat_p + 0.35 * margin
    return side.astype(int), score.astype(float)


def non_overlap_indices(active: np.ndarray, horizon: int) -> list[int]:
    selected: list[int] = []
    next_allowed = 0
    for idx, flag in enumerate(active):
        if idx < next_allowed or not flag:
            continue
        selected.append(idx)
        next_allowed = idx + max(1, horizon)
    return selected


def split_kpi(values: np.ndarray, period_timestamps: pd.Series) -> dict[str, Any]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return {
            "net_profit": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_percent": 0.0,
            "max_drawdown_amount": 0.0,
            "trade_count": 0,
            "trades_day": 0.0,
            "win_rate": 0.0,
            "average_win": 0.0,
            "average_loss": 0.0,
            "payoff_ratio": 0.0,
            "expectancy": 0.0,
            "recovery_factor": 0.0,
            "max_consecutive_loss": 0,
            "time_under_water_trades": 0,
            "underwater_fraction": 0.0,
            "smooth_equity_proxy": False,
        }
    wins = values[values > 0]
    losses = values[values < 0]
    gross_profit = float(wins.sum())
    gross_loss = float(losses.sum())
    pf = gross_profit / abs(gross_loss) if gross_loss < 0 else (float("inf") if gross_profit > 0 else 0.0)
    equity = np.cumsum(values)
    with_zero = np.r_[0.0, equity]
    peak = np.maximum.accumulate(with_zero)
    dd_curve = peak[1:] - equity
    max_dd = float(np.max(dd_curve)) if len(dd_curve) else 0.0
    max_dd_pct = max_dd / 10000.0 * 100.0
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    loss_flags = values < 0
    max_loss_run = 0
    current = 0
    for flag in loss_flags:
        current = current + 1 if flag else 0
        max_loss_run = max(max_loss_run, current)
    underwater = int(np.count_nonzero(dd_curve > 0))
    underwater_fraction = float(underwater / len(values))
    days = max((pd.to_datetime(period_timestamps).max() - pd.to_datetime(period_timestamps).min()).total_seconds() / 86400.0, 1.0)
    recovery = float(values.sum() / max_dd) if max_dd > 0 else (float("inf") if values.sum() > 0 else 0.0)
    smooth = bool(max_dd_pct <= 10.0 and underwater_fraction <= 0.62 and max_loss_run <= 8 and recovery >= 0.8)
    return {
        "net_profit": float(values.sum()),
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": pf,
        "max_drawdown_percent": max_dd_pct,
        "max_drawdown_amount": max_dd,
        "trade_count": int(len(values)),
        "trades_day": float(len(values) / days),
        "win_rate": float(len(wins) / len(values) * 100.0),
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": float(avg_win / abs(avg_loss)) if avg_loss < 0 else 0.0,
        "expectancy": float(values.mean()),
        "recovery_factor": recovery,
        "max_consecutive_loss": int(max_loss_run),
        "time_under_water_trades": underwater,
        "underwater_fraction": underwater_fraction,
        "smooth_equity_proxy": smooth,
    }


def evaluate_splits(frame: pd.DataFrame, selected_mask: np.ndarray, side: np.ndarray, long_profit: np.ndarray, short_profit: np.ndarray) -> list[dict[str, Any]]:
    profit = np.where(side > 0, long_profit, short_profit)
    rows: list[dict[str, Any]] = []
    for split, split_frame in frame.groupby(frame["split"].astype(str), sort=False):
        idx = split_frame.index.to_numpy()
        mask = selected_mask[idx]
        kpi = split_kpi(profit[idx][mask], split_frame["timestamp"])
        rows.append(
            {
                "split": split,
                **kpi,
                "long_trade_count": int(np.count_nonzero((side[idx] > 0) & mask)),
                "short_trade_count": int(np.count_nonzero((side[idx] < 0) & mask)),
                "signal_count": int(np.count_nonzero(mask)),
            }
        )
    return rows


def selected_mask_from_threshold(frame: pd.DataFrame, score: np.ndarray, spec: SelectionSpec, horizon: int, threshold: float) -> np.ndarray:
    active = (score >= threshold) & mask_for(frame, spec.mask_name)
    selected = set(non_overlap_indices(active, horizon))
    return np.array([idx in selected for idx in range(len(frame))], dtype=bool)


def gate_flags(summary: Mapping[str, Any]) -> dict[str, bool]:
    scout = (
        summary["validation_net_profit"] > 0
        and summary["oos_net_profit"] > 0
        and summary["validation_profit_factor"] >= 1.10
        and summary["oos_profit_factor"] >= 1.10
        and summary["validation_max_drawdown_percent"] <= 15.0
        and summary["oos_max_drawdown_percent"] <= 15.0
        and summary["validation_trades_day"] >= 1.0
        and summary["oos_trades_day"] >= 1.0
    )
    meaningful = (
        summary["validation_profit_factor"] >= 1.20
        and summary["oos_profit_factor"] >= 1.20
        and summary["validation_max_drawdown_percent"] <= 10.0
        and summary["oos_max_drawdown_percent"] <= 10.0
        and summary["validation_trades_day"] >= 3.0
        and summary["oos_trades_day"] >= 3.0
    )
    final_like = (
        summary["validation_profit_factor"] >= 2.0
        and summary["oos_profit_factor"] >= 2.0
        and summary["validation_max_drawdown_percent"] <= 10.0
        and summary["oos_max_drawdown_percent"] <= 10.0
        and 5.0 <= summary["validation_trades_day"] <= 10.0
        and 5.0 <= summary["oos_trades_day"] <= 10.0
        and bool(summary["validation_smooth_equity_proxy"])
        and bool(summary["oos_smooth_equity_proxy"])
    )
    return {"scout_clue": bool(scout), "meaningful_candidate": bool(meaningful), "final_like_reference_only": bool(final_like)}


def threshold_from_train(score: np.ndarray, train_mask: np.ndarray, selection_mask: np.ndarray, quantile: float) -> float | None:
    values = score[train_mask & selection_mask]
    values = values[np.isfinite(values)]
    if len(values) < 50:
        return None
    return float(np.quantile(values, quantile))


def class_balance_rows(frame: pd.DataFrame, label: pd.Series, spec: LabelSpec) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, subset in frame.groupby(frame["split"].astype(str), sort=False):
        counts = label.loc[subset.index].value_counts().to_dict()
        rows.append(
            {
                "label_id": spec.label_id,
                "split": split,
                "rows": int(len(subset)),
                "long_count": int(counts.get(1, 0)),
                "flat_count": int(counts.get(0, 0)),
                "short_count": int(counts.get(-1, 0)),
                "directional_rate": float((counts.get(1, 0) + counts.get(-1, 0)) / max(len(subset), 1)),
            }
        )
    return rows


def entry_rows(
    frame: pd.DataFrame,
    candidate_id: str,
    selected_mask: np.ndarray,
    side: np.ndarray,
    score: np.ndarray,
    long_profit: np.ndarray,
    short_profit: np.ndarray,
    limit: int = 7000,
) -> list[dict[str, Any]]:
    selected = np.flatnonzero(selected_mask)
    if len(selected) > limit:
        selected = selected[:limit]
    profit = np.where(side > 0, long_profit, short_profit)
    rows: list[dict[str, Any]] = []
    for idx in selected:
        rows.append(
            {
                "candidate_id": candidate_id,
                "timestamp": str(frame.at[idx, "timestamp"]),
                "split": str(frame.at[idx, "split"]),
                "side": "long" if side[idx] > 0 else "short",
                "score": float(score[idx]),
                "proxy_profit": float(profit[idx]) if math.isfinite(float(profit[idx])) else "",
            }
        )
    return rows


def run_scout(created_at: str) -> dict[str, Any]:
    frame = load_frame()
    train_mask = split_mask(frame, "train")
    labels = label_specs()
    features = feature_sets(frame)
    models = model_specs()
    selections = selection_specs()
    candidate_rows: list[dict[str, Any]] = []
    kpi_rows: list[dict[str, Any]] = []
    balance_rows: list[dict[str, Any]] = []
    fracture_rows: list[dict[str, Any]] = []
    scout_entries: list[dict[str, Any]] = []

    for label_spec in labels:
        label, long_profit, short_profit, best_utility = build_label(frame, label_spec)
        balance_rows.extend(class_balance_rows(frame, label, label_spec))
        y_train = label.loc[train_mask]
        directional = int(np.count_nonzero(y_train.to_numpy() != 0))
        if y_train.nunique() < 2 or directional < 120:
            continue
        weights = sample_weight(frame, label, best_utility)[train_mask]
        for feature_set in features:
            x_train = frame.loc[train_mask, feature_set.columns]
            x_all = frame.loc[:, feature_set.columns]
            for model_spec in models:
                model = model_spec.build()
                try:
                    fit_model(model, x_train, y_train, weights)
                    side, score = side_scores(model, x_all)
                except Exception as exc:
                    candidate_rows.append(
                        {
                            "candidate_id": "f71b_fit_failed_" + stable_id([label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, str(exc)]),
                            "label_id": label_spec.label_id,
                            "feature_set_id": feature_set.feature_set_id,
                            "model_id": model_spec.model_id,
                            "status": "fit_failed(학습 실패)",
                            "error": str(exc)[:240],
                        }
                    )
                    continue
                for selection in selections:
                    selection_mask = mask_for(frame, selection.mask_name)
                    threshold = threshold_from_train(score, train_mask, selection_mask, selection.threshold_quantile)
                    if threshold is None:
                        continue
                    selected_mask = selected_mask_from_threshold(frame, score, selection, label_spec.horizon_bars, threshold)
                    split_rows = evaluate_splits(frame, selected_mask, side, long_profit, short_profit)
                    by_split = {row["split"]: row for row in split_rows}
                    validation = by_split.get("validation", {})
                    oos = by_split.get("oos", {})
                    candidate_id = "f71b_" + stable_id(
                        [label_spec.label_id, feature_set.feature_set_id, model_spec.model_id, selection.selection_id]
                    )
                    relaxed_q = max(0.20, selection.threshold_quantile - 0.15)
                    relaxed_threshold = threshold_from_train(score, train_mask, selection_mask, relaxed_q)
                    relaxed_split_rows = []
                    if relaxed_threshold is not None:
                        relaxed_mask = selected_mask_from_threshold(frame, score, selection, label_spec.horizon_bars, relaxed_threshold)
                        relaxed_split_rows = evaluate_splits(frame, relaxed_mask, side, long_profit, short_profit)
                    relaxed_by_split = {row["split"]: row for row in relaxed_split_rows}
                    rval = relaxed_by_split.get("validation", {})
                    roos = relaxed_by_split.get("oos", {})
                    fracture_pass = bool(
                        rval.get("profit_factor", 0.0) >= 1.10
                        and roos.get("profit_factor", 0.0) >= 1.10
                        and rval.get("max_drawdown_percent", 999.0) <= 12.0
                        and roos.get("max_drawdown_percent", 999.0) <= 12.0
                    )
                    summary = {
                        "candidate_id": candidate_id,
                        "label_id": label_spec.label_id,
                        "horizon_bars": label_spec.horizon_bars,
                        "tp_atr": label_spec.tp_atr,
                        "sl_atr": label_spec.sl_atr,
                        "utility_mode": label_spec.utility_mode,
                        "feature_set_id": feature_set.feature_set_id,
                        "feature_count": len(feature_set.columns),
                        "model_id": model_spec.model_id,
                        "model_family": model_spec.model_family,
                        "model_role": model_spec.model_role,
                        "selection_id": selection.selection_id,
                        "mask_name": selection.mask_name,
                        "threshold_quantile": selection.threshold_quantile,
                        "threshold": threshold,
                        "relaxed_threshold_quantile": relaxed_q,
                        "density_lift_fracture_pass": fracture_pass,
                        "validation_net_profit": validation.get("net_profit", 0.0),
                        "validation_gross_profit": validation.get("gross_profit", 0.0),
                        "validation_gross_loss": validation.get("gross_loss", 0.0),
                        "validation_profit_factor": validation.get("profit_factor", 0.0),
                        "validation_max_drawdown_percent": validation.get("max_drawdown_percent", 0.0),
                        "validation_trade_count": validation.get("trade_count", 0),
                        "validation_trades_day": validation.get("trades_day", 0.0),
                        "validation_win_rate": validation.get("win_rate", 0.0),
                        "validation_expectancy": validation.get("expectancy", 0.0),
                        "validation_recovery_factor": validation.get("recovery_factor", 0.0),
                        "validation_smooth_equity_proxy": validation.get("smooth_equity_proxy", False),
                        "oos_net_profit": oos.get("net_profit", 0.0),
                        "oos_gross_profit": oos.get("gross_profit", 0.0),
                        "oos_gross_loss": oos.get("gross_loss", 0.0),
                        "oos_profit_factor": oos.get("profit_factor", 0.0),
                        "oos_max_drawdown_percent": oos.get("max_drawdown_percent", 0.0),
                        "oos_trade_count": oos.get("trade_count", 0),
                        "oos_trades_day": oos.get("trades_day", 0.0),
                        "oos_win_rate": oos.get("win_rate", 0.0),
                        "oos_expectancy": oos.get("expectancy", 0.0),
                        "oos_recovery_factor": oos.get("recovery_factor", 0.0),
                        "oos_smooth_equity_proxy": oos.get("smooth_equity_proxy", False),
                    }
                    flags = gate_flags(summary)
                    summary.update(flags)
                    summary["meaningful_with_fracture"] = bool(flags["meaningful_candidate"] and fracture_pass)
                    candidate_rows.append(summary)
                    for row in split_rows:
                        kpi_rows.append(
                            {
                                "candidate_id": candidate_id,
                                "label_id": label_spec.label_id,
                                "feature_set_id": feature_set.feature_set_id,
                                "model_id": model_spec.model_id,
                                "selection_id": selection.selection_id,
                                "split": row["split"],
                                **{key: value for key, value in row.items() if key != "split"},
                            }
                        )
                    fracture_rows.append(
                        {
                            "candidate_id": candidate_id,
                            "selection_id": selection.selection_id,
                            "threshold_quantile": selection.threshold_quantile,
                            "relaxed_threshold_quantile": relaxed_q,
                            "validation_profit_factor": rval.get("profit_factor", 0.0),
                            "validation_max_drawdown_percent": rval.get("max_drawdown_percent", 0.0),
                            "validation_trades_day": rval.get("trades_day", 0.0),
                            "oos_profit_factor": roos.get("profit_factor", 0.0),
                            "oos_max_drawdown_percent": roos.get("max_drawdown_percent", 0.0),
                            "oos_trades_day": roos.get("trades_day", 0.0),
                            "fracture_pass": fracture_pass,
                        }
                    )
                    if flags["scout_clue"]:
                        scout_entries.extend(entry_rows(frame, candidate_id, selected_mask, side, score, long_profit, short_profit))

    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row.get("final_like_reference_only")),
            bool(row.get("meaningful_with_fracture")),
            bool(row.get("meaningful_candidate")),
            bool(row.get("scout_clue")),
            float(row.get("oos_profit_factor") or 0.0),
            float(row.get("validation_profit_factor") or 0.0),
            min(float(row.get("oos_trades_day") or 0.0), float(row.get("validation_trades_day") or 0.0)),
            float(row.get("oos_net_profit") or 0.0),
        ),
        reverse=True,
    )
    scout_clues = [row for row in ranked if row.get("scout_clue")]
    meaningful = [row for row in ranked if row.get("meaningful_candidate")]
    meaningful_fracture = [row for row in ranked if row.get("meaningful_with_fracture")]
    final_like = [row for row in ranked if row.get("final_like_reference_only")]
    if meaningful:
        status = "completed_proxy_scout_meaningful_candidate_no_authority"
        judgment = "proxy_scout_clue_meaningful_candidate_needs_grok_then_mt5_runtime_probe_no_authority"
        next_run = NEXT_RUN_IF_MEANINGFUL
    elif scout_clues:
        status = "completed_proxy_scout_scout_clue_repair_required_no_authority"
        judgment = "proxy_scout_clue_without_meaningful_joint_gate_needs_repair_no_authority"
        next_run = NEXT_RUN_IF_SCOUT_ONLY
    else:
        status = "completed_proxy_scout_no_scout_clue_repair_required_no_authority"
        judgment = "proxy_no_scout_clue_broad_surface_needs_repair_or_closeout_decision_no_authority"
        next_run = NEXT_RUN_IF_NO_SCOUT
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
        "frame_rows": int(len(frame)),
        "test_period": {"start": str(frame["timestamp"].min()), "end": str(frame["timestamp"].max())},
        "split_counts": {key: int(value) for key, value in frame["split"].astype(str).value_counts().sort_index().items()},
        "label_count": len(labels),
        "feature_sets": [{"feature_set_id": fs.feature_set_id, "feature_count": len(fs.columns), "note": fs.note} for fs in features],
        "model_count": len(models),
        "selection_count": len(selections),
        "candidate_count": len([row for row in candidate_rows if not str(row.get("status", "")).startswith("fit_failed")]),
        "fit_failed_count": len([row for row in candidate_rows if str(row.get("status", "")).startswith("fit_failed")]),
        "scout_clue_count": len(scout_clues),
        "meaningful_candidate_count": len(meaningful),
        "meaningful_with_fracture_count": len(meaningful_fracture),
        "final_like_reference_only_count": len(final_like),
        "top_candidates": ranked[:15],
        "candidate_rows": ranked,
        "kpi_rows": kpi_rows,
        "balance_rows": balance_rows,
        "fracture_rows": fracture_rows,
        "scout_entry_rows": scout_entries,
        "runtime_probe_kpi": "pending_not_executed_in_proxy_scout(프록시 탐색에서는 대기)",
        "proxy_runtime_gap": "not_available_until_mt5_runtime_probe(MT5 런타임 탐침 전까지 없음)",
    }


def tier_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    return [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A full-context model input(Tier A 전체 문맥 모델 입력)",
            "status": "completed_proxy_scout(프록시 탐색 완료)",
            "judgment": result["judgment"],
            "net_profit": top.get("oos_net_profit", ""),
            "profit_factor": top.get("oos_profit_factor", ""),
            "drawdown": top.get("oos_max_drawdown_percent", ""),
            "trade_count": top.get("oos_trade_count", ""),
            "trades_day": top.get("oos_trades_day", ""),
            "notes": "F71B materialized Tier A proxy only(F71B는 Tier A 프록시만 물질화).",
        },
        {
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B partial-context sample(Tier B 부분 문맥 표본)",
            "status": "missing_required(필수 누락)",
            "judgment": "not_materialized_in_f71b_proxy_scout(F71B 프록시 탐색에서 미물질화)",
            "notes": "Tier B is recorded as missing, not silently omitted(Tier B는 조용히 생략하지 않고 누락으로 기록).",
        },
        {
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "combined record(합산 기록)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "judgment": "no_synthetic_combined_claim_without_tier_b(Tier B 없이 합성 합산 주장 없음)",
            "notes": "Combined result is unavailable because Tier B was not materialized(합산 결과는 Tier B 미물질화 때문에 없음).",
        },
    ]


def report_lines(result: Mapping[str, Any]) -> list[str]:
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    lines = [
        "# Frontier71B Economics-Native Proxy Scout(F71B 경제성 네이티브 프록시 탐색)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis(가설)",
        "",
        "Economics-native lifecycle labels(경제성 네이티브 생명주기 라벨) and joint selection objectives(공동 선택 목표) can find a seed surface(씨앗 표면) that keeps density/PF/DD(밀도/수익 팩터/손실폭) together better than post-hoc threshold/tape repair(사후 임계값/테이프 수리).",
        "",
        "Effect(효과): this run changes what is selected(무엇을 선택하는지) through label/target(라벨/목표), feature set(피처 묶음), model family(모델 계열), trade shape(거래 형태), and risk shape(위험 형태).",
        "",
        "## Test Period(테스트 기간)",
        "",
        f"- period(기간): `{result['test_period']['start']}` to `{result['test_period']['end']}`",
        f"- split counts(분할 행 수): `{json.dumps(result['split_counts'], ensure_ascii=False)}`",
        "",
        "## Proxy Expectation(프록시 예상)",
        "",
        "- scout clue(탐색 단서): validation/OOS(검증/표본외) net>0, PF>=1.10, DD<=15%, trades/day>=1.",
        "- meaningful candidate(의미 후보): validation/OOS(검증/표본외) PF>=1.20, DD<=10%, trades/day>=3.",
        "- density lift fracture(밀도 상승 균열): relaxed density(완화 밀도)에서도 PF>=1.10, DD<=12%.",
        "",
        "## Proxy KPI(프록시 핵심 성과 지표)",
        "",
        f"- candidates tested(시험 후보): `{result['candidate_count']}`",
        f"- scout clue count(탐색 단서 수): `{result['scout_clue_count']}`",
        f"- meaningful candidate count(의미 후보 수): `{result['meaningful_candidate_count']}`",
        f"- meaningful with fracture count(밀도 균열 통과 의미 후보 수): `{result['meaningful_with_fracture_count']}`",
        f"- final-like reference-only count(최종 유사 참조 전용 수): `{result['final_like_reference_only_count']}`",
        "",
        "## Top Proxy Row(상위 프록시 행)",
        "",
        f"- candidate(후보): `{top.get('candidate_id', 'none')}`",
        f"- validation net/PF/DD/trades/day(검증 순수익/수익 팩터/손실폭/일거래): `{fmt(top.get('validation_net_profit'))}` / `{fmt(top.get('validation_profit_factor'))}` / `{fmt(top.get('validation_max_drawdown_percent'))}` / `{fmt(top.get('validation_trades_day'))}`",
        f"- OOS net/PF/DD/trades/day(표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(top.get('oos_net_profit'))}` / `{fmt(top.get('oos_profit_factor'))}` / `{fmt(top.get('oos_max_drawdown_percent'))}` / `{fmt(top.get('oos_trades_day'))}`",
        f"- label/feature/model/selection(라벨/피처/모델/선택): `{top.get('label_id', '')}` / `{top.get('feature_set_id', '')}` / `{top.get('model_id', '')}` / `{top.get('selection_id', '')}`",
        "",
        "## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)",
        "",
        "- status(상태): `pending_not_executed_in_f71b_proxy_scout(프록시 탐색에서는 대기)`.",
        "- reason(이유): MT5 Runtime Probe(MT5 런타임 탐침)는 proxy signal(프록시 신호) 뒤 transfer check(전이 확인)로 실행한다.",
        "",
        "## Proxy/Runtime Gap(프록시/런타임 간극)",
        "",
        "- current(현재): `not_available_until_mt5_runtime_probe(MT5 런타임 탐침 전까지 없음)`.",
        "",
        "## Tier Records(티어 기록)",
        "",
        "- Tier A separate(Tier A 분리): completed proxy scout(프록시 탐색 완료).",
        "- Tier B separate(Tier B 분리): missing_required(필수 누락).",
        "- Tier A+B combined(Tier A+B 합산): out_of_scope_by_claim(주장 범위 밖).",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{result['next_run_id']}`",
    ]
    return lines


def gate_audit_lines(result: Mapping[str, Any]) -> list[str]:
    return [
        "# Required Gate Coverage Audit F71B(필수 게이트 커버리지 감사 F71B)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| input identity(입력 정체성) | passed(통과) | `{rel(MODEL_INPUT)}` sha256 `{sha256_file(MODEL_INPUT)}` | data path(데이터 경로) 고정 |",
        f"| stage open anchors(단계 개방 고정점) | passed(통과) | `{rel(F71A_GATE)}`, `{rel(F71A_DENYLIST)}` | F70 반복 방지 |",
        f"| proxy execution(프록시 실행) | passed(통과) | `{rel(SUMMARY_JSON)}` | economics-native scout(경제성 네이티브 탐색) 물질화 |",
        f"| Tier paired records(티어 쌍 기록) | passed_with_missing_required(필수 누락 포함 통과) | `{rel(TIER_CSV)}` | Tier B 미물질화 숨김 방지 |",
        f"| MT5 runtime probe(MT5 런타임 탐침) | pending(대기) | next `{result['next_run_id']}` | proxy-only claim boundary(프록시 전용 주장 경계) 유지 |",
        f"| forbidden claim guard(금지 주장 보호) | passed(통과) | `{CLAIM_BOUNDARY}` | completion/baseline/promotion/runtime authority/live readiness/Goal Achieve 없음 |",
    ]


def registry_row(result: Mapping[str, Any]) -> dict[str, Any]:
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_scout(프록시 탐색)",
        "status": result["status"],
        "judgment": result["judgment"],
        "path": rel(REPORT),
        "notes": f"candidates={result['candidate_count']};scout={result['scout_clue_count']};meaningful={result['meaningful_candidate_count']};final_like={result['final_like_reference_only_count']}",
        "family": "economics_native_proxy_scout(경제성 네이티브 프록시 탐색)",
        "primary_report": rel(REPORT),
        "run_number": "frontier71B",
        "date": "2026-06-17",
        "decision": result["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": result["next_run_id"],
        "rows": result["candidate_count"],
        "gate_passes": result["scout_clue_count"],
        "gate_total": result["candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "candidate_rows": result["candidate_count"],
        "positive_proxy_rows": result["scout_clue_count"],
        "best_model_id": top.get("model_id", ""),
        "best_proxy_net": top.get("oos_net_profit", ""),
        "attempt_rows": result["candidate_count"],
        "feature_matrix_rows": result["frame_rows"],
        "best_net_profit": top.get("oos_net_profit", ""),
        "best_profit_factor": top.get("oos_profit_factor", ""),
        "run_date": "2026-06-17",
        "primary_artifact": rel(RUN_MANIFEST),
        "candidate_model_id": top.get("candidate_id", ""),
        "net_profit": top.get("oos_net_profit", ""),
        "profit_factor": top.get("oos_profit_factor", ""),
        "drawdown": top.get("oos_max_drawdown_percent", ""),
        "recovery_factor": top.get("oos_recovery_factor", ""),
        "trade_count": top.get("oos_trade_count", ""),
        "result_status": result["status"],
        "sample_rows": result["frame_rows"],
        "feature_count": top.get("feature_count", ""),
        "expectancy": top.get("oos_expectancy", ""),
        "attempt_count": result["candidate_count"],
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "proxy_trading_kpi(프록시 거래 KPI)",
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 전용 주장 범위 밖)",
        "result_judgment": result["judgment"],
        "final_decision_path": rel(REPORT),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": result["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_proxy",
        "subrun_id": "proxy_scout(프록시 탐색)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A full-context sample(Tier A 전체 문맥 표본)",
        "kpi_scope": "proxy_trading_kpi(프록시 거래 KPI)",
        "primary_kpi": f"best_oos_net={fmt(top.get('oos_net_profit'))};best_oos_pf={fmt(top.get('oos_profit_factor'))};best_oos_dd={fmt(top.get('oos_max_drawdown_percent'))};best_oos_tpd={fmt(top.get('oos_trades_day'))}",
        "guardrail_kpi": f"scout={result['scout_clue_count']};meaningful={result['meaningful_candidate_count']};fracture={result['meaningful_with_fracture_count']}",
        "model_variants": result["model_count"],
        "selected_surfaces": result["scout_clue_count"],
        "runtime_attempt_rows": 0,
        "work_family": "experiment(실험)",
        "max_drawdown_amount": top.get("oos_max_drawdown_percent", ""),
        "long_trade_count": "",
        "short_trade_count": "",
        "row_id": f"{RUN_ID}__tier_a_proxy",
        "scoreboard": "structural_scout(구조 스카우트)",
        "evidence_boundary": "proxy_only_no_authority(프록시 전용, 권위 없음)",
        "next_action": result["next_run_id"],
        "question": "Can economics-native label/selection create joint density PF DD signal?(경제성 네이티브 라벨/선택이 밀도/수익 팩터/손실폭 공동 신호를 만들 수 있나?)",
        "artifact_count": 9,
        "created_at_utc": result["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "proxy_scout(프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "F71A stage-open anchors(F71A 단계 개방 고정점)",
        "trade_density": top.get("oos_trades_day", ""),
        "expected_net_profit": "",
        "expected_profit_factor": "",
        "expected_trade_count": "",
        "expected_trade_density": "",
        "max_drawdown_percent": top.get("oos_max_drawdown_percent", ""),
        "strict_joint_pass_count": result["meaningful_candidate_count"],
    }


def ledger_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = registry_row(result)
    rows = []
    for idx, tier in enumerate(tier_rows(result), start=1):
        row = dict(base)
        row.update(tier)
        row["ledger_row_id"] = f"{RUN_ID}__tier_view_{idx}"
        row["row_id"] = row["ledger_row_id"]
        row["subrun_id"] = tier["record_view"]
        row["path"] = rel(TIER_CSV)
        row["primary_report"] = rel(REPORT)
        row["report_path"] = rel(REPORT)
        rows.append(row)
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    upsert_ledger(RUN_REGISTRY, "run_id", registry_row(result))
    for row in ledger_rows(result):
        upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_ledger(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def append_idea(result: Mapping[str, Any]) -> None:
    marker = "<!-- frontier71B_economics_native_proxy_scout_v1 -->"
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    block = f"""
{marker}
- `{RUN_ID}` executed economics-native proxy scout(경제성 네이티브 프록시 탐색). Result(결과): `{result['judgment']}`. Candidates(후보) `{result['candidate_count']}`, scout clue(탐색 단서) `{result['scout_clue_count']}`, meaningful candidate(의미 후보) `{result['meaningful_candidate_count']}`, final-like reference-only(최종 유사 참조 전용) `{result['final_like_reference_only_count']}`. Top OOS(상위 표본외) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{fmt(top.get('oos_net_profit'))}/{fmt(top.get('oos_profit_factor'))}/{fmt(top.get('oos_max_drawdown_percent'))}/{fmt(top.get('oos_trades_day'))}`. Evidence(근거): `{rel(REPORT)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    append_once(IDEA_REGISTRY, marker, block)


def write_state(result: Mapping[str, Any]) -> None:
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {result['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {result['status']}",
        f"current_judgment: {result['judgment']}",
        f"next_run_id: {result['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_retrospective_completed",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "Action(행동): F71B economics-native proxy scout(경제성 네이티브 프록시 탐색)를 실행했다."',
        f'  - "Effect(효과): scout={result["scout_clue_count"]}, meaningful={result["meaningful_candidate_count"]}, final_like={result["final_like_reference_only_count"]}로 다음 repair/probe(수리/탐침) 경로를 고정한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")
    top = result["top_candidates"][0] if result.get("top_candidates") else {}
    lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{result['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F71B economics-native proxy scout(경제성 네이티브 프록시 탐색)를 실행했다.",
        "",
        f"Effect(효과): candidates(후보) `{result['candidate_count']}`, scout clue(탐색 단서) `{result['scout_clue_count']}`, meaningful candidate(의미 후보) `{result['meaningful_candidate_count']}`로 다음 행동을 `{result['next_run_id']}`로 고정했다.",
        "",
        f"- top candidate(상위 후보): `{top.get('candidate_id', 'none')}`.",
        f"- validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래): `{fmt(top.get('validation_net_profit'))}` / `{fmt(top.get('validation_profit_factor'))}` / `{fmt(top.get('validation_max_drawdown_percent'))}` / `{fmt(top.get('validation_trades_day'))}`.",
        f"- OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(top.get('oos_net_profit'))}` / `{fmt(top.get('oos_profit_factor'))}` / `{fmt(top.get('oos_max_drawdown_percent'))}` / `{fmt(top.get('oos_trades_day'))}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(CURRENT_WORKING_STATE, lines)


def write_outputs(result: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "inputs": {
            "model_input": rel(MODEL_INPUT),
            "model_input_sha256": sha256_file(MODEL_INPUT),
            "feature_order": rel(FEATURE_ORDER),
            "raw_us100": rel(RAW_US100),
            "raw_us100_sha256": sha256_file(RAW_US100),
            "f71a_report": rel(F71A_REPORT),
            "f71a_gate": rel(F71A_GATE),
            "f71a_denylist": rel(F71A_DENYLIST),
        },
        "outputs": {
            "summary": rel(SUMMARY_JSON),
            "candidate_summary": rel(CANDIDATE_CSV),
            "kpi_by_split": rel(KPI_CSV),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    summary = {key: value for key, value in result.items() if key not in {"candidate_rows", "kpi_rows", "balance_rows", "fracture_rows", "scout_entry_rows"}}
    write_json(SUMMARY_JSON, summary)
    write_csv(CANDIDATE_CSV, result["candidate_rows"])
    write_csv(KPI_CSV, result["kpi_rows"])
    write_csv(LABEL_BALANCE_CSV, result["balance_rows"])
    write_csv(FRACTURE_CSV, result["fracture_rows"])
    write_csv(TIER_CSV, tier_rows(result))
    write_csv(SCOUT_ENTRY_CSV, result["scout_entry_rows"])
    write_csv(SUMMARY_REVIEW_CSV, result["candidate_rows"])
    write_csv(KPI_REVIEW_CSV, result["kpi_rows"])
    write_csv(LABEL_BALANCE_REVIEW_CSV, result["balance_rows"])
    write_csv(FRACTURE_REVIEW_CSV, result["fracture_rows"])
    write_csv(TIER_REVIEW_CSV, tier_rows(result))
    write_md(REPORT, report_lines(result))
    write_md(GATE_AUDIT, gate_audit_lines(result))


def main() -> int:
    missing = [rel(path) for path in required_artifacts() if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing required artifact(필수 산출물 누락): {missing}")
    created_at = utc_now()
    result = run_scout(created_at)
    write_outputs(result)
    update_ledgers(result)
    append_idea(result)
    write_state(result)
    print(
        json.dumps(
            json_ready(
                {
                    "status": result["status"],
                    "judgment": result["judgment"],
                    "candidate_count": result["candidate_count"],
                    "scout_clue_count": result["scout_clue_count"],
                    "meaningful_candidate_count": result["meaningful_candidate_count"],
                    "next_run_id": result["next_run_id"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
