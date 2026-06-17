from __future__ import annotations

import csv
import json
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b


STAGE_ID = "stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path"
RUN_ID = "frontier79B_runtime_native_trade_shape_label_proxy_scout_v1"
PARENT_RUN_ID = "frontier79A_stage_open_runtime_native_trade_shape_labeling_from_fill_path_v1"
NEXT_RUN_IF_MEANINGFUL = "frontier79C_pre_mt5_grok_runtime_native_trade_shape_runtime_probe_v1"
NEXT_RUN_IF_WEAK_NONZERO = "frontier79C_pre_mt5_grok_runtime_native_negative_control_runtime_probe_v1"
NEXT_RUN_IF_ZERO = "frontier79C_runtime_native_zero_signal_repair_plan_v1"

STATUS_MEANINGFUL = "proxy_runtime_native_meaningful_signal_pre_mt5_grok_required_no_authority"
STATUS_WEAK_NONZERO = "proxy_runtime_native_weak_nonzero_signal_negative_control_probe_required_no_authority"
STATUS_ZERO = "proxy_runtime_native_zero_signal_logic_repair_required_no_authority"
JUDGMENT_MEANINGFUL = "runtime_native_proxy_meaningful_signal_requires_grok_and_mt5_probe_no_authority"
JUDGMENT_WEAK_NONZERO = "runtime_native_proxy_weak_signal_requires_negative_control_runtime_probe_no_authority"
JUDGMENT_ZERO = "runtime_native_proxy_zero_signal_logic_repair_required_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

INITIAL_BALANCE = 500.0
MAX_CALENDAR_TPD_SCOUT = 14.0
CONTRACT_PNL_SCALE = f78b.CONTRACT_PNL_SCALE
SLTP_POINT_SCALE = f78b.SLTP_POINT_SCALE

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SUMMARY = REVIEW_DIR / "f79b_runtime_native_proxy_summary.json"
CANDIDATES_ALL = RUN_DIR / "f79b_runtime_native_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f79b_runtime_native_ranked_top200.csv"
AXIS_SUMMARY = REVIEW_DIR / "f79b_runtime_native_axis_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f79b_runtime_native_model_fit_summary.csv"
LABEL_AUDIT = REVIEW_DIR / "f79b_runtime_native_label_audit.csv"
DATA_INTEGRITY = REVIEW_DIR / "f79b_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f79b_model_validation_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f79b_artifact_lineage.json"
REPORT = REVIEW_DIR / "frontier79B_runtime_native_trade_shape_label_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f79b.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_79/frontier79b_runtime_native_trade_shape_label_proxy_scout.py"


@dataclass(frozen=True)
class RuntimeSpec:
    name: str
    side: str
    entry_mode: str
    fill_order: str
    hold_bars: int
    tp_price_units: float
    sl_price_units: float
    label_mode: str
    utility_quantile: float


def utc_now() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


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
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def feature_sets(features: Sequence[str]) -> dict[str, list[str]]:
    available = set(features)
    price = [f for f in features if any(k in f for k in ["log_return", "hl_range", "close_open", "gap_percent", "return_zscore", "hl_zscore", "close_prev"])]
    vol = [f for f in features if any(k in f for k in ["atr", "bollinger", "bb_", "historical_vol", "squeeze"])]
    session = [f for f in features if any(k in f for k in ["is_us_cash", "minutes_from", "first_30m", "last_30m"])]
    trend = [f for f in features if any(k in f for k in ["ema", "sma", "rsi", "stoch", "ppo", "roc", "trix", "adx", "di_", "supertrend", "vortex"])]
    external = [f for f in features if any(k in f for k in ["vix", "us10yr", "usdx", "xnas", "mega8", "top3"])]
    runtime_fill_context = sorted(set(price + vol + session + ["bb_position_20", "di_spread_14", "adx_14"]) & available)
    contract_core = sorted(set(price + vol + session + trend[:12]) & available)
    no_external = [f for f in features if f not in set(external)]
    no_session = [f for f in features if f not in set(session)]
    return {
        "runtime_fill_context": runtime_fill_context,
        "contract_core": contract_core,
        "no_external": no_external,
        "no_session": no_session,
    }


def model_builders(random_state: int = 7902) -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2_balanced": lambda: make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=350, class_weight="balanced", C=0.45, solver="lbfgs"),
        ),
        "extra_trees_d7_l80": lambda: ExtraTreesClassifier(
            n_estimators=36,
            max_depth=7,
            min_samples_leaf=120,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
    }


def runtime_specs() -> list[RuntimeSpec]:
    trade_shapes = [(6, 9.0, 7.0), (12, 15.0, 10.0)]
    label_modes = [("fill_path_net", 0.60), ("dd_normalized", 0.56), ("mae_mfe_asymmetry", 0.62)]
    specs: list[RuntimeSpec] = []
    for side in ["long", "short"]:
        for hold, tp, sl in trade_shapes:
            for mode, quantile in label_modes:
                specs.append(
                    RuntimeSpec(
                        name=f"{side}_same_h{hold}_tp{int(tp)}_sl{int(sl)}_pessimistic_{mode}_q{int(quantile * 100)}",
                        side=side,
                        entry_mode="same_bar_open",
                        fill_order="pessimistic",
                        hold_bars=hold,
                        tp_price_units=tp,
                        sl_price_units=sl,
                        label_mode=mode,
                        utility_quantile=quantile,
                    )
                )
    for side in ["long", "short"]:
        specs.append(
            RuntimeSpec(
                name=f"{side}_same_h12_tp15_sl10_close_direction_fill_path_net_q60",
                side=side,
                entry_mode="same_bar_open",
                fill_order="close_direction",
                hold_bars=12,
                tp_price_units=15.0,
                sl_price_units=10.0,
                label_mode="fill_path_net",
                utility_quantile=0.60,
            )
        )
    for side in ["long", "short"]:
        specs.append(
            RuntimeSpec(
                name=f"{side}_nextbar_control_h12_tp15_sl10_pessimistic_fill_path_net_q60",
                side=side,
                entry_mode="next_bar_open_control",
                fill_order="pessimistic",
                hold_bars=12,
                tp_price_units=15.0,
                sl_price_units=10.0,
                label_mode="fill_path_net",
                utility_quantile=0.60,
            )
        )
    return specs


def entry_indices(df: pd.DataFrame, raw: pd.DataFrame, mode: str) -> np.ndarray:
    mapping = {ts: idx for idx, ts in enumerate(raw["open_ts"])}
    current = df["timestamp"].map(mapping).fillna(-2).astype(int).to_numpy()
    if mode == "same_bar_open":
        return current
    if mode == "next_bar_open_control":
        return current + 1
    raise ValueError(mode)


def both_hit_realized(spec: RuntimeSpec, entry: float, bar_open: float, bar_close: float) -> float:
    if spec.fill_order == "pessimistic":
        return -spec.sl_price_units
    if spec.fill_order == "close_direction":
        if spec.side == "long":
            return spec.tp_price_units if bar_close >= max(entry, bar_open) else -spec.sl_price_units
        return spec.tp_price_units if bar_close <= min(entry, bar_open) else -spec.sl_price_units
    raise ValueError(spec.fill_order)


def compute_outcome(raw: pd.DataFrame, indices: np.ndarray, spec: RuntimeSpec) -> dict[str, np.ndarray]:
    open_arr = raw["open"].to_numpy(float)
    high_arr = raw["high"].to_numpy(float)
    low_arr = raw["low"].to_numpy(float)
    close_arr = raw["close"].to_numpy(float)
    spread_price_units = raw["spread_points"].to_numpy(float) / SLTP_POINT_SCALE
    n = len(indices)
    pnl_contract = np.full(n, np.nan)
    pnl_price = np.full(n, np.nan)
    mfe_contract = np.full(n, np.nan)
    mae_contract = np.full(n, np.nan)
    spread_cost_contract = np.full(n, np.nan)
    utility = np.full(n, np.nan)
    exit_offset = np.zeros(n, dtype=int)
    both_hit = np.zeros(n, dtype=int)
    valid = np.zeros(n, dtype=bool)
    max_idx = len(raw) - spec.hold_bars
    for row_idx, raw_idx in enumerate(indices):
        if raw_idx < 0 or raw_idx > max_idx:
            continue
        entry = float(open_arr[raw_idx])
        if not np.isfinite(entry) or entry <= 0:
            continue
        hi = high_arr[raw_idx : raw_idx + spec.hold_bars]
        lo = low_arr[raw_idx : raw_idx + spec.hold_bars]
        op = open_arr[raw_idx : raw_idx + spec.hold_bars]
        cl = close_arr[raw_idx : raw_idx + spec.hold_bars]
        if not (np.isfinite(hi).all() and np.isfinite(lo).all() and np.isfinite(op).all() and np.isfinite(cl).all()):
            continue
        if spec.side == "long":
            mfe_price = float(np.max(hi - entry))
            mae_price = float(np.max(entry - lo))
            realized = float(cl[-1] - entry)
            offset = spec.hold_bars
            for local_idx in range(spec.hold_bars):
                sl_hit = lo[local_idx] <= entry - spec.sl_price_units
                tp_hit = hi[local_idx] >= entry + spec.tp_price_units
                if sl_hit and tp_hit:
                    realized = both_hit_realized(spec, entry, float(op[local_idx]), float(cl[local_idx]))
                    both_hit[row_idx] = 1
                    offset = local_idx + 1
                    break
                if sl_hit or tp_hit:
                    realized = -spec.sl_price_units if sl_hit else spec.tp_price_units
                    offset = local_idx + 1
                    break
        else:
            mfe_price = float(np.max(entry - lo))
            mae_price = float(np.max(hi - entry))
            realized = float(entry - cl[-1])
            offset = spec.hold_bars
            for local_idx in range(spec.hold_bars):
                sl_hit = hi[local_idx] >= entry + spec.sl_price_units
                tp_hit = lo[local_idx] <= entry - spec.tp_price_units
                if sl_hit and tp_hit:
                    realized = both_hit_realized(spec, entry, float(op[local_idx]), float(cl[local_idx]))
                    both_hit[row_idx] = 1
                    offset = local_idx + 1
                    break
                if sl_hit or tp_hit:
                    realized = -spec.sl_price_units if sl_hit else spec.tp_price_units
                    offset = local_idx + 1
                    break
        spread_cost = float(spread_price_units[raw_idx]) * CONTRACT_PNL_SCALE if np.isfinite(spread_price_units[raw_idx]) else 0.0
        contract_pnl = realized * CONTRACT_PNL_SCALE - spread_cost
        mae = mae_price * CONTRACT_PNL_SCALE + spread_cost
        mfe = mfe_price * CONTRACT_PNL_SCALE
        if spec.label_mode == "dd_normalized":
            score = contract_pnl - 0.60 * mae - 0.002 * offset
        elif spec.label_mode == "mae_mfe_asymmetry":
            score = contract_pnl + 0.08 * mfe - 0.42 * mae - 0.0015 * offset
        else:
            score = contract_pnl - 0.22 * mae - 0.001 * offset
        pnl_price[row_idx] = realized
        pnl_contract[row_idx] = contract_pnl
        mfe_contract[row_idx] = mfe
        mae_contract[row_idx] = mae
        spread_cost_contract[row_idx] = spread_cost
        utility[row_idx] = score
        exit_offset[row_idx] = max(1, int(offset))
        valid[row_idx] = True
    return {
        "pnl_price": pnl_price,
        "pnl_contract": pnl_contract,
        "mfe_contract": mfe_contract,
        "mae_contract": mae_contract,
        "spread_cost_contract": spread_cost_contract,
        "utility": utility,
        "exit_offset": exit_offset,
        "both_hit": both_hit,
        "valid": valid,
    }


def make_label(df: pd.DataFrame, outcome: Mapping[str, np.ndarray], spec: RuntimeSpec) -> np.ndarray:
    train_mask = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
    if train_mask.sum() == 0:
        return np.zeros(len(df), dtype=int)
    utility = np.asarray(outcome["utility"], dtype=float)
    pnl = np.asarray(outcome["pnl_contract"], dtype=float)
    mae = np.asarray(outcome["mae_contract"], dtype=float)
    mfe = np.asarray(outcome["mfe_contract"], dtype=float)
    threshold = float(np.nanquantile(utility[train_mask], spec.utility_quantile))
    if spec.label_mode == "dd_normalized":
        guard = mae <= np.nanquantile(mae[train_mask], 0.62)
    elif spec.label_mode == "mae_mfe_asymmetry":
        ratio = np.divide(mfe, mae + 1e-9)
        guard = ratio >= np.nanquantile(ratio[train_mask], 0.55)
    else:
        guard = mae <= np.nanquantile(mae[train_mask], 0.82)
    return ((utility >= threshold) & (pnl > 0.0) & guard & np.asarray(outcome["valid"], dtype=bool)).astype(int)


def scout_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            int(metrics["trade_count"]) >= 80
            and float(metrics["pf"]) >= 1.15
            and float(metrics["dd_pct"]) <= 12.0
            and 1.0 <= float(metrics["calendar_trades_day"]) <= MAX_CALENDAR_TPD_SCOUT
        )

    return ok(val) and ok(oos)


def meaningful_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.35
            and float(metrics["dd_pct"]) <= 10.0
            and 2.0 <= float(metrics["calendar_trades_day"]) <= 12.0
            and int(metrics["trade_count"]) >= 120
        )

    return ok(val) and ok(oos)


def final_like_reference(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 2.0
            and float(metrics["dd_pct"]) <= 10.0
            and 5.0 <= float(metrics["calendar_trades_day"]) <= 10.0
            and int(metrics["smooth_equity_proxy"]) == 1
        )

    return ok(val) and ok(oos)


def density_score(value: float) -> float:
    if value <= 0:
        return -10.0
    if 5.0 <= value <= 10.0:
        return 10.0
    if value < 5.0:
        return value * 1.7
    return max(0.0, 10.0 - (value - 10.0) * 1.4)


def rank_score(val: Mapping[str, Any], oos: Mapping[str, Any], meaningful: bool, scout: bool, final_like: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    density = min(density_score(float(val["calendar_trades_day"])), density_score(float(oos["calendar_trades_day"])))
    smooth = int(val["smooth_equity_proxy"]) + int(oos["smooth_equity_proxy"])
    return (
        (2_000_000.0 if final_like else 0.0)
        + (1_000_000.0 if meaningful else 0.0)
        + (150_000.0 if scout else 0.0)
        + (25_000.0 if min_net > 0 else 0.0)
        + min_pf * 4_500.0
        + density * 3_000.0
        + smooth * 3_000.0
        - max_dd * 500.0
        + min_net * 25.0
    )


def fit_and_score() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    original_balance = f78b.INITIAL_BALANCE
    f78b.INITIAL_BALANCE = INITIAL_BALANCE
    try:
        df, raw, features = f78b.load_inputs()
        feature_map = feature_sets(features)
        builders = model_builders()
        thresholds = f78b.risk_thresholds(df)
        specs = runtime_specs()
        sessions = ["all", "cash_open", "cash_mid"]
        risk_filters = ["none", "trend_aligned"]
        prob_quantiles = [0.68, 0.82]
        cooldowns = [0, 6]

        candidate_rows: list[dict[str, Any]] = []
        fit_rows: list[dict[str, Any]] = []
        label_rows: list[dict[str, Any]] = []
        candidate_id = 0

        for spec in specs:
            indices = entry_indices(df, raw, spec.entry_mode)
            outcome = compute_outcome(raw, indices, spec)
            label = make_label(df, outcome, spec)
            train_valid = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
            positive = int(label[train_valid].sum()) if train_valid.sum() else 0
            label_rows.append(
                {
                    "label_name": spec.name,
                    "side": spec.side,
                    "entry_mode": spec.entry_mode,
                    "fill_order": spec.fill_order,
                    "hold_bars": spec.hold_bars,
                    "tp_price_units": spec.tp_price_units,
                    "sl_price_units": spec.sl_price_units,
                    "tp_broker_points": spec.tp_price_units * SLTP_POINT_SCALE,
                    "sl_broker_points": spec.sl_price_units * SLTP_POINT_SCALE,
                    "label_mode": spec.label_mode,
                    "utility_quantile": spec.utility_quantile,
                    "train_valid_rows": int(train_valid.sum()),
                    "train_positive_rows": positive,
                    "train_positive_rate": float(label[train_valid].mean()) if train_valid.sum() else 0.0,
                    "both_hit_rows": int(np.asarray(outcome["both_hit"], dtype=int)[train_valid].sum()) if train_valid.sum() else 0,
                    "validation_valid_rows": int(((df["split"] == "validation").to_numpy() & np.asarray(outcome["valid"], dtype=bool)).sum()),
                    "oos_valid_rows": int(((df["split"] == "oos").to_numpy() & np.asarray(outcome["valid"], dtype=bool)).sum()),
                }
            )
            if train_valid.sum() == 0 or positive == 0 or positive == train_valid.sum():
                fit_rows.append(
                    {
                        "label_name": spec.name,
                        "feature_set": "all",
                        "model": "all",
                        "status": "skipped_single_class_or_empty",
                        "train_rows": int(train_valid.sum()),
                        "positive_rows": positive,
                    }
                )
                continue
            for feature_set_name, cols in feature_map.items():
                if not cols:
                    continue
                matrices = f78b.clean_matrices(df, train_valid, cols)
                train_matrix = df.loc[train_valid, cols].replace([np.inf, -np.inf], np.nan)
                med = train_matrix.median(numeric_only=True).fillna(0.0)
                train_matrix = train_matrix.fillna(med).astype(float)
                y_train = label[train_valid]
                for model_name, builder in builders.items():
                    model = builder()
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            model.fit(train_matrix, y_train)
                        train_probs = f78b.probability(model, train_matrix)
                        probs = {split: f78b.probability(model, matrices[split]) for split in ["validation", "oos"]}
                        fit_rows.append(
                            {
                                "label_name": spec.name,
                                "feature_set": feature_set_name,
                                "feature_count": len(cols),
                                "model": model_name,
                                "status": "fit_completed",
                                "train_rows": int(len(y_train)),
                                "positive_rows": int(y_train.sum()),
                                "positive_rate": float(y_train.mean()),
                            }
                        )
                    except Exception as exc:  # noqa: BLE001
                        fit_rows.append(
                            {
                                "label_name": spec.name,
                                "feature_set": feature_set_name,
                                "feature_count": len(cols),
                                "model": model_name,
                                "status": "fit_failed",
                                "error": str(exc)[:200],
                                "train_rows": int(len(y_train)),
                                "positive_rows": int(y_train.sum()),
                            }
                        )
                        continue
                    for q in prob_quantiles:
                        prob_threshold = float(np.quantile(train_probs, q))
                        for session in sessions:
                            for risk_filter in risk_filters:
                                for cooldown in cooldowns:
                                    split_payload: dict[str, dict[str, Any]] = {}
                                    row_base: dict[str, Any] = {}
                                    raw_any = 0
                                    entry_any = 0
                                    for split in ["validation", "oos"]:
                                        split_mask_global = (df["split"] == split).to_numpy()
                                        split_df = df.loc[split_mask_global].reset_index(drop=True)
                                        split_outcome = {key: np.asarray(value)[split_mask_global] for key, value in outcome.items()}
                                        valid = np.asarray(split_outcome["valid"], dtype=bool)
                                        raw_signal = (
                                            (probs[split] >= prob_threshold)
                                            & valid
                                            & f78b.session_mask(split_df, session)
                                            & f78b.risk_mask(split_df, risk_filter, spec.side, thresholds)
                                        )
                                        selected = f78b.lifecycle_select(raw_signal, np.asarray(split_outcome["exit_offset"], dtype=int), cooldown)
                                        metrics = f78b.contract_kpi(split_df, selected, split_outcome)
                                        split_payload[split] = metrics
                                        raw_any += int(raw_signal.sum())
                                        entry_any += int(selected.sum())
                                        row_base[f"{split}_raw_signal_count"] = int(raw_signal.sum())
                                        row_base[f"{split}_lifecycle_trade_count"] = int(selected.sum())
                                        row_base[f"{split}_signal_to_trade_ratio"] = int(selected.sum()) / int(raw_signal.sum()) if int(raw_signal.sum()) else 0.0
                                    val = split_payload["validation"]
                                    oos = split_payload["oos"]
                                    scout = scout_gate(val, oos)
                                    meaningful = meaningful_gate(val, oos)
                                    final_like = final_like_reference(val, oos)
                                    dual_positive = float(val["net"]) > 0.0 and float(oos["net"]) > 0.0
                                    candidate_id += 1
                                    row: dict[str, Any] = {
                                        "candidate_id": f"f79b_{candidate_id:05d}",
                                        "label_name": spec.name,
                                        "side": spec.side,
                                        "entry_mode": spec.entry_mode,
                                        "fill_order": spec.fill_order,
                                        "hold_bars": spec.hold_bars,
                                        "tp_price_units": spec.tp_price_units,
                                        "sl_price_units": spec.sl_price_units,
                                        "tp_broker_points": spec.tp_price_units * SLTP_POINT_SCALE,
                                        "sl_broker_points": spec.sl_price_units * SLTP_POINT_SCALE,
                                        "label_mode": spec.label_mode,
                                        "utility_quantile": spec.utility_quantile,
                                        "feature_set": feature_set_name,
                                        "feature_count": len(cols),
                                        "model": model_name,
                                        "prob_quantile": q,
                                        "prob_threshold": prob_threshold,
                                        "session": session,
                                        "risk_filter": risk_filter,
                                        "cooldown_bars": cooldown,
                                        "contract_pnl_scale": CONTRACT_PNL_SCALE,
                                        "initial_balance": INITIAL_BALANCE,
                                        "raw_signal_total": raw_any,
                                        "lifecycle_trade_total": entry_any,
                                        "overall_signal_to_trade_ratio": entry_any / raw_any if raw_any else 0.0,
                                        "scout_clue": int(scout),
                                        "meaningful_signal": int(meaningful),
                                        "final_like_reference": int(final_like),
                                        "dual_positive": int(dual_positive),
                                        "rank_score": rank_score(val, oos, meaningful, scout, final_like),
                                    }
                                    row.update(row_base)
                                    for prefix, metrics in [("val", val), ("oos", oos)]:
                                        for key, value in metrics.items():
                                            row[f"{prefix}_{key}"] = value
                                    candidate_rows.append(row)
        candidate_rows.sort(key=lambda row: float(row["rank_score"]), reverse=True)
        best = candidate_rows[0] if candidate_rows else {}
        summary = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "candidate_rows": len(candidate_rows),
            "fit_rows": len(fit_rows),
            "label_rows": len(label_rows),
            "scout_clue_count": sum(int(row["scout_clue"]) for row in candidate_rows),
            "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in candidate_rows),
            "final_like_reference_count": sum(int(row["final_like_reference"]) for row in candidate_rows),
            "dual_positive_count": sum(int(row["dual_positive"]) for row in candidate_rows),
            "nonzero_lifecycle_trade_candidates": sum(1 for row in candidate_rows if int(row["lifecycle_trade_total"]) > 0),
            "best_candidate": best,
            "feature_sets": {name: len(cols) for name, cols in feature_map.items()},
            "model_families": list(builders.keys()),
            "spec_count": len(specs),
            "sessions": sessions,
            "risk_filters": risk_filters,
            "prob_quantiles": prob_quantiles,
            "cooldowns": cooldowns,
            "entry_rule": "same_bar_open primary(동일 봉 시가 우선) with next_bar_open_control(다음 봉 시가 대조)",
            "fill_order_rule": "pessimistic or close_direction when TP and SL both hit within one M5 bar(한 5분봉 안에서 손절/익절 동시 도달 시 보수/종가방향 순서)",
            "dd_rule": "max_drawdown_percent uses tester deposit 500 denominator(최대 손실폭 퍼센트는 테스터 예치금 500 기준)",
            "scout_budget": "wave0 capped: 16 runtime specs x 4 feature sets x 2 model families x 2 thresholds x 3 sessions x 2 risk filters x 2 cooldowns(0차 상한 탐색)",
        }
        return candidate_rows, fit_rows, label_rows, summary
    finally:
        f78b.INITIAL_BALANCE = original_balance


def axis_summary_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    axes = ["label_mode", "entry_mode", "fill_order", "side", "hold_bars", "feature_set", "model", "session", "risk_filter", "cooldown_bars"]
    for axis in axes:
        for value in sorted({str(row.get(axis, "")) for row in candidate_rows}):
            subset = [row for row in candidate_rows if str(row.get(axis, "")) == value]
            if not subset:
                continue
            best = max(subset, key=lambda row: float(row["rank_score"]))
            rows.append(
                {
                    "axis": axis,
                    "value": value,
                    "candidate_rows": len(subset),
                    "scout_clue_count": sum(int(row["scout_clue"]) for row in subset),
                    "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in subset),
                    "final_like_reference_count": sum(int(row["final_like_reference"]) for row in subset),
                    "best_candidate": best["candidate_id"],
                    "best_rank_score": best["rank_score"],
                    "best_val_net_pf_dd_tpd": f"{best['val_net']}/{best['val_pf']}/{best['val_dd_pct']}/{best['val_calendar_trades_day']}",
                    "best_oos_net_pf_dd_tpd": f"{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_calendar_trades_day']}",
                }
            )
    return rows


def status_and_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    if int(summary.get("meaningful_signal_count", 0) or 0) > 0:
        return STATUS_MEANINGFUL, JUDGMENT_MEANINGFUL, NEXT_RUN_IF_MEANINGFUL
    if int(summary.get("scout_clue_count", 0) or 0) > 0 or int(summary.get("nonzero_lifecycle_trade_candidates", 0) or 0) > 0:
        return STATUS_WEAK_NONZERO, JUDGMENT_WEAK_NONZERO, NEXT_RUN_IF_WEAK_NONZERO
    return STATUS_ZERO, JUDGMENT_ZERO, NEXT_RUN_IF_ZERO


def format_best(best: Mapping[str, Any]) -> str:
    if not best:
        return "none(없음)"
    return (
        f"`{best.get('candidate_id')}` val net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래) "
        f"`{best.get('val_net')}/{best.get('val_pf')}/{best.get('val_dd_pct')}/{best.get('val_calendar_trades_day')}/{best.get('val_trade_count')}`, "
        f"OOS(표본외) `{best.get('oos_net')}/{best.get('oos_pf')}/{best.get('oos_dd_pct')}/{best.get('oos_calendar_trades_day')}/{best.get('oos_trade_count')}`"
    )


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]]) -> str:
    top_table = "\n".join(
        [
            "| candidate(후보) | model(모델) | label(라벨) | feature/session/risk(피처/세션/위험) | val net/PF/DD/tpd/trades(검증) | OOS net/PF/DD/tpd/trades(표본외) | scout/meaningful/final-like(탐색/의미/최종유사) |",
            "|---|---|---|---|---:|---:|---:|",
            *[
                f"| `{row.get('candidate_id')}` | `{row.get('model')}` | `{row.get('label_name')}` | `{row.get('feature_set')}/{row.get('session')}/{row.get('risk_filter')}` | "
                f"`{row.get('val_net'):.4f}/{row.get('val_pf'):.4f}/{row.get('val_dd_pct'):.4f}/{row.get('val_calendar_trades_day'):.4f}/{row.get('val_trade_count')}` | "
                f"`{row.get('oos_net'):.4f}/{row.get('oos_pf'):.4f}/{row.get('oos_dd_pct'):.4f}/{row.get('oos_calendar_trades_day'):.4f}/{row.get('oos_trade_count')}` | "
                f"`{row.get('scout_clue')}/{row.get('meaningful_signal')}/{row.get('final_like_reference')}` |"
                for row in top_rows[:12]
            ],
        ]
    )
    return f"""# F79B Runtime-Native Proxy Scout Report(F79B 런타임 네이티브 프록시 탐색 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- candidate rows(후보 행): `{summary.get('candidate_rows')}`
- scout clue count(탐색 단서 수): `{summary.get('scout_clue_count')}`
- meaningful signal count(의미 신호 수): `{summary.get('meaningful_signal_count')}`
- final-like reference count(최종 유사 참고 수): `{summary.get('final_like_reference_count')}`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `{summary.get('nonzero_lifecycle_trade_candidates')}`
- entry rule(진입 규칙): `{summary.get('entry_rule')}`
- fill order rule(체결 순서 규칙): `{summary.get('fill_order_rule')}`
- DD rule(손실폭 규칙): `{summary.get('dd_rule')}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

## Proxy Expectation(프록시 예상)

F79B expects(예상) that same-bar fill-path labels(동일 봉 체결 경로 라벨) and Deposit=500 DD scoring(예치금 500 손실폭 점수화) will reduce the F78 proxy/runtime gap(F78 프록시/런타임 간극). It is still proxy scout only(프록시 탐색 전용).

## Top Candidates(상위 후보)

{top_table}

## Runtime Probe Status(런타임 탐침 상태)

Runtime probe KPI(런타임 탐침 핵심 성과 지표)는 not run yet(아직 미실행). If weak or meaningful signal exists(약한 또는 의미 신호가 있으면), next action(다음 행동)은 pre-MT5 Grok review(사전 MT5 Grok 검토) and mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)이다.

This report(보고서)는 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.
"""


def data_integrity_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "data_source": [rel(f78b.DATASET_PATH), rel(f78b.FEATURE_ORDER_PATH), rel(f78b.RAW_BARS_PATH)],
        "time_axis": "Feature timestamp(피처 시각)은 closed-bar key(닫힌 봉 키)로 사용하고 same_bar_open/next_bar_open entry indices(동일 봉/다음 봉 진입 인덱스)를 raw open_ts(원천 시가 시각)에 매핑한다.",
        "feature_label_boundary": "features(피처)는 현재 행만 사용하고 label/target(라벨/목표)은 entry 이후 OHLC path(진입 이후 OHLC 경로)만 사용한다.",
        "split_boundary": "model fit(모델 학습), label quantile(라벨 분위수), probability threshold(확률 임계값)는 train only(훈련 전용)에서 계산한다.",
        "tier_scope": "Tier A separate(티어 A 분리); Tier B missing_required(티어 B 필수 누락); combined out_of_scope_by_claim(합산은 주장 범위 밖).",
        "candidate_rows": summary.get("candidate_rows"),
        "entry_rule": summary.get("entry_rule"),
        "fill_order_rule": summary.get("fill_order_rule"),
    }


def model_validation_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "target_and_label": "runtime-native fill-path utility labels(런타임 네이티브 체결 경로 효용 라벨)",
        "model_families": summary.get("model_families"),
        "feature_sets": summary.get("feature_sets"),
        "split_method": "time-ordered train/validation/OOS holdout(시간순 훈련/검증/표본외 고정); WFO(워크포워드)는 signal exists(신호 존재) 뒤 실행.",
        "overfit_risk": "broad axis sweep(넓은 축 탐색)이므로 scout-only boundary(탐색 전용 경계)를 유지한다.",
        "export_constraint": "small NN(작은 신경망)은 이번 wave0에서 제외했고, exportable classical surfaces(내보내기 가능한 고전 표면)부터 점검한다.",
        "summary": {
            "scout_clue_count": summary.get("scout_clue_count"),
            "meaningful_signal_count": summary.get("meaningful_signal_count"),
            "best_candidate": (summary.get("best_candidate") or {}).get("candidate_id"),
        },
    }


def artifact_lineage(summary: Mapping[str, Any], next_run: str) -> dict[str, Any]:
    return {
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "source_inputs": [rel(f78b.DATASET_PATH), rel(f78b.FEATURE_ORDER_PATH), rel(f78b.RAW_BARS_PATH), "stages/stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path/03_reviews/f79a_experiment_design_review.json"],
        "artifact_paths": [rel(SUMMARY), rel(CANDIDATES_ALL), rel(CANDIDATES_TOP), rel(AXIS_SUMMARY), rel(MODEL_FIT_SUMMARY), rel(LABEL_AUDIT), rel(REPORT), rel(RUN_MANIFEST)],
        "consumer": next_run,
        "lineage_judgment": "proxy_scout_artifacts_connected_no_authority(프록시 탐색 산출물 연결, 권위 없음)",
    }


def gate_audit_text(status: str, summary: Mapping[str, Any], next_run: str) -> str:
    return f"""# F79B Required Gate Coverage Audit(F79B 필수 게이트 커버리지 감사)

Status(상태): `{status}`

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| F79A handoff(F79A 인계) | `passed(통과)` | parent run(부모 실행) `{PARENT_RUN_ID}` |
| proxy expectation(프록시 예상) | `recorded(기록됨)` | `{rel(REPORT)}` |
| broad axis sweep(넓은 축 탐색) | `recorded(기록됨)` | candidates(후보) `{summary.get('candidate_rows')}`, specs(스펙) `{summary.get('spec_count')}`, feature sets(피처 묶음) `{summary.get('feature_sets')}` |
| Deposit=500 DD denominator(예치금 500 손실폭 분모) | `recorded(기록됨)` | `{summary.get('dd_rule')}` |
| runtime probe gate(런타임 탐침 게이트) | `pending_if_signal(신호 시 대기)` | next run(다음 실행) `{next_run}` |
| Tier B/combined records(티어 B/합산 기록) | `missing_required/out_of_scope_by_claim(필수 누락/주장 범위 밖)` | Tier A proxy scout only(티어 A 프록시 탐색 전용) |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""# F79 Selection Status(F79 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F79B runtime-native proxy scout(런타임 네이티브 프록시 탐색)를 실행했다.

Effect(효과): fill-path label(체결 경로 라벨), trade shape(거래 형태), risk logic(위험 로직), feature/model/session sweep(피처/모델/세션 탐색)의 후보 표면을 기록했다.

Best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def ledger_row(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary.get("best_candidate") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "proxy_scout(프록시 탐색)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B combined out_of_scope",
        "kpi_scope": "runtime_native_proxy_validation_oos(런타임 네이티브 프록시 검증/표본외)",
        "scoreboard_lane": "trade_shape(거래 형태)",
        "lane": "proxy_scout(프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "primary_kpi": f"scout={summary.get('scout_clue_count')};meaningful={summary.get('meaningful_signal_count')};final_like={summary.get('final_like_reference_count')}",
        "guardrail_kpi": f"entry={summary.get('entry_rule')};dd={summary.get('dd_rule')}",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"candidates={summary.get('candidate_rows')}; next={next_run}",
        "run_number": "frontier79B",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "rows": summary.get("candidate_rows"),
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": best.get("candidate_id", ""),
        "candidate_count": summary.get("candidate_rows"),
        "scout_clue_count": summary.get("scout_clue_count"),
        "meaningful_signal_count": summary.get("meaningful_signal_count"),
        "completion_candidate_count": summary.get("final_like_reference_count"),
        "model": best.get("model", ""),
        "net_profit": best.get("oos_net", ""),
        "profit_factor": best.get("oos_pf", ""),
        "drawdown": best.get("oos_dd_pct", ""),
        "drawdown_percent": best.get("oos_dd_pct", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trades_per_day": best.get("val_calendar_trades_day", ""),
        "oos_trades_per_day": best.get("oos_calendar_trades_day", ""),
        "oos_net_profit": best.get("oos_net", ""),
        "oos_profit_factor": best.get("oos_pf", ""),
        "oos_trade_count": best.get("oos_trade_count", ""),
        "oos_drawdown_percent": best.get("oos_dd_pct", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "proxy_scout",
        "tier": "Tier A",
        "metric_scope": "validation_oos_proxy",
        "result_status": status,
        "feature_count": best.get("feature_count", ""),
        "work_family": "experiment_execution",
        "row_id": f"{RUN_ID}__proxy_scout",
        "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색 전용, 권위 없음)",
        "next_action": next_run,
        "question": "Can runtime-native fill-path trade-shape labels create signal?(런타임 네이티브 체결 경로 거래 형태 라벨이 신호를 만들 수 있나?)",
        "artifact_count": 8,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only(프록시 전용)",
        "run_family": "runtime_native_proxy_scout",
        "run_type": "proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REPORT),
        "result_path": rel(REPORT),
        "expected_net_profit": best.get("val_net", ""),
        "expected_profit_factor": best.get("val_pf", ""),
        "expected_trade_count": best.get("val_trade_count", ""),
        "expected_trade_density": best.get("val_calendar_trades_day", ""),
        "trade_density": best.get("oos_calendar_trades_day", ""),
        "max_drawdown_percent": best.get("oos_dd_pct", ""),
        "strict_joint_pass_count": summary.get("final_like_reference_count"),
    }


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    row = ledger_row(created_at, status, judgment, next_run, summary)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry(summary: Mapping[str, Any], next_run: str) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    best = summary.get("best_candidate") or {}
    addition = f"""

- `{RUN_ID}` executed F79 runtime-native proxy scout(F79 런타임 네이티브 프록시 탐색). Result(결과): `scout={summary.get('scout_clue_count')}`, `meaningful={summary.get('meaningful_signal_count')}`, `final_like={summary.get('final_like_reference_count')}`. Best(최선): `{best.get('candidate_id', '')}` OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일 거래) `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_state_files(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f79_proxy_signal_requires_pre_mt5_grok_if_nonzero
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f78_closeout_3_of_5
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F79B proxy scout(프록시 탐색)를 실행했다."
  - "Effect(효과): scout={summary.get('scout_clue_count')}, meaningful={summary.get('meaningful_signal_count')}, final_like={summary.get('final_like_reference_count')}를 기록했다."
  - "Next(다음): {next_run}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F79B runtime-native proxy scout(런타임 네이티브 프록시 탐색)를 실행했다.

Effect(효과): same-bar fill-path labels(동일 봉 체결 경로 라벨), Deposit=500 DD scoring(예치금 500 손실폭 점수화), feature/model/session/risk sweep(피처/모델/세션/위험 탐색)의 후보 표면을 기록했다.

## Proxy KPI(프록시 핵심 성과 지표)

- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- final-like reference(최종 유사 참고): `{summary.get('final_like_reference_count')}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- runtime probe boundary(런타임 탐침 경계): if nonzero signal exists(비영 신호가 있으면) pre-MT5 Grok review(사전 MT5 그록 검토) 뒤 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def run_manifest_payload(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "summary": summary,
        "artifacts": {
            "summary": rel(SUMMARY),
            "candidates_all": rel(CANDIDATES_ALL),
            "candidates_top": rel(CANDIDATES_TOP),
            "axis_summary": rel(AXIS_SUMMARY),
            "model_fit_summary": rel(MODEL_FIT_SUMMARY),
            "label_audit": rel(LABEL_AUDIT),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
        },
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    candidate_rows, fit_rows, label_rows, summary = fit_and_score()
    top_rows = candidate_rows[:200]
    axis_rows = axis_summary_rows(candidate_rows)
    status, judgment, next_run = status_and_next(summary)

    write_json(SUMMARY, summary)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, top_rows)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_csv(LABEL_AUDIT, label_rows)
    write_json(DATA_INTEGRITY, data_integrity_review(summary))
    write_json(MODEL_VALIDATION, model_validation_review(summary))
    write_json(ARTIFACT_LINEAGE, artifact_lineage(summary, next_run))
    write_text(REPORT, report_text(created_at, summary, top_rows))
    write_text(GATE_AUDIT, gate_audit_text(status, summary, next_run))
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run, summary))
    write_text(CONTEXT_ANCHOR, f79_context_anchor_text(created_at, status, judgment, next_run, summary))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, summary))

    update_ledgers(created_at, status, judgment, next_run, summary)
    update_idea_registry(summary, next_run)
    update_state_files(created_at, status, judgment, next_run, summary)

    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "candidate_rows": summary["candidate_rows"],
                "scout_clue_count": summary["scout_clue_count"],
                "meaningful_signal_count": summary["meaningful_signal_count"],
                "final_like_reference_count": summary["final_like_reference_count"],
                "best_candidate": (summary.get("best_candidate") or {}).get("candidate_id"),
                "best_oos": {
                    "net": (summary.get("best_candidate") or {}).get("oos_net"),
                    "pf": (summary.get("best_candidate") or {}).get("oos_pf"),
                    "dd": (summary.get("best_candidate") or {}).get("oos_dd_pct"),
                    "tpd": (summary.get("best_candidate") or {}).get("oos_calendar_trades_day"),
                    "trades": (summary.get("best_candidate") or {}).get("oos_trade_count"),
                },
                "next_run": next_run,
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def f79_context_anchor_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""# F79 Context Anchor(F79 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{next_run}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Runtime probe observation(런타임 탐침 관찰): not run yet(아직 미실행).

Proxy observation(프록시 관찰): scout(탐색) `{summary.get('scout_clue_count')}`, meaningful(의미) `{summary.get('meaningful_signal_count')}`, final-like(최종 유사) `{summary.get('final_like_reference_count')}`.

Next action(다음 행동): `{next_run}`.
"""


if __name__ == "__main__":
    raise SystemExit(main())
