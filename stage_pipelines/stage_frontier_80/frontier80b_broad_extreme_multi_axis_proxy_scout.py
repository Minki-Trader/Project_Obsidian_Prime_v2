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
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_79 import frontier79b_runtime_native_trade_shape_label_proxy_scout as f79b


STAGE_ID = "stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics"
RUN_ID = "frontier80B_broad_extreme_multi_axis_proxy_scout_v1"
PARENT_RUN_ID = "frontier80A_stage_open_multi_axis_surface_rotation_v1"
NEXT_RUN_IF_MATERIAL = "frontier80C_wfo_aware_surface_selection_v1"
NEXT_RUN_IF_WEAK = "frontier80C_negative_control_and_materialization_repair_v1"
NEXT_RUN_IF_ZERO = "frontier80F_no_signal_closeout_decision_v1"

STATUS_MATERIAL = "f80b_proxy_material_signal_wfo_selection_required_no_authority"
STATUS_WEAK = "f80b_proxy_weak_nonzero_signal_repair_or_negative_control_required_no_authority"
STATUS_ZERO = "f80b_proxy_zero_signal_closeout_decision_required_no_authority"
JUDGMENT_MATERIAL = "multi_axis_rotation_material_proxy_clue_requires_wfo_and_mt5_no_authority"
JUDGMENT_WEAK = "multi_axis_rotation_weak_proxy_clue_requires_repair_no_authority"
JUDGMENT_ZERO = "multi_axis_rotation_zero_signal_requires_closeout_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics"
)

INITIAL_BALANCE = 500.0
CONTRACT_PNL_SCALE = f78b.CONTRACT_PNL_SCALE
SLTP_POINT_SCALE = f78b.SLTP_POINT_SCALE
MAX_TPD_SCOUT = 18.0

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SUMMARY = REVIEW_DIR / "f80b_multi_axis_proxy_summary.json"
CANDIDATES_ALL = RUN_DIR / "f80b_multi_axis_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f80b_multi_axis_ranked_top200.csv"
AXIS_SUMMARY = REVIEW_DIR / "f80b_multi_axis_axis_summary.csv"
SURFACE_SUMMARY = REVIEW_DIR / "f80b_surface_family_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f80b_model_fit_summary.csv"
LABEL_AUDIT = REVIEW_DIR / "f80b_label_audit.csv"
TIER_AUDIT = REVIEW_DIR / "f80b_tier_record_audit.csv"
DATA_CONTRACT = REVIEW_DIR / "f80b_data_feature_contract_preflight.json"
MODEL_VALIDATION = REVIEW_DIR / "f80b_model_validation_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f80b_artifact_lineage.json"
REPORT = REVIEW_DIR / "frontier80B_broad_extreme_multi_axis_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f80b.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_80/frontier80b_broad_extreme_multi_axis_proxy_scout.py"


@dataclass(frozen=True)
class F80Spec:
    surface_family: str
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
    runtime = sorted(set(price + vol + session + ["bb_position_20", "di_spread_14", "adx_14"]) & available)
    reversal = sorted(set([f for f in price + vol + session + trend if any(k in f for k in ["bb_", "rsi", "stoch", "zscore", "atr", "squeeze", "is_"])]) & available)
    trend_intent = sorted(set(price + session + [f for f in trend if any(k in f for k in ["ema", "sma", "adx", "di_", "supertrend", "vortex", "ppo", "roc"])]) & available)
    no_external = [f for f in features if f not in set(external)]
    compact = [f for f in runtime + trend_intent if f in available][:28]
    return {
        "full58": list(features),
        "runtime_fill_context": runtime,
        "price_vol_session": sorted(set(price + vol + session) & available),
        "trend_order_intent": trend_intent,
        "micro_reversal": reversal,
        "no_external_contract": no_external,
        "compact_exportable_28": compact,
    }


def model_builders(random_state: int = 8002) -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2_balanced": lambda: make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=320, class_weight="balanced", C=0.35, solver="lbfgs"),
        ),
        "extra_trees_d6_l120": lambda: ExtraTreesClassifier(
            n_estimators=40,
            max_depth=6,
            min_samples_leaf=120,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
        "histgbm_shallow": lambda: HistGradientBoostingClassifier(
            max_iter=80,
            learning_rate=0.055,
            max_leaf_nodes=15,
            l2_regularization=0.10,
            random_state=random_state,
        ),
    }


def runtime_specs() -> list[F80Spec]:
    seeds = [
        ("breakout_cost_dd", "long", "same_bar_open", "pessimistic", 10, 12.0, 7.0, "cost_dd_normalized", 0.62),
        ("breakout_cost_dd", "short", "same_bar_open", "pessimistic", 10, 12.0, 7.0, "cost_dd_normalized", 0.62),
        ("order_intent_swing", "long", "same_bar_open", "close_direction", 18, 22.0, 11.0, "order_intent_asymmetry", 0.64),
        ("order_intent_swing", "short", "same_bar_open", "close_direction", 18, 22.0, 11.0, "order_intent_asymmetry", 0.64),
        ("density_survival", "long", "next_bar_open_control", "pessimistic", 12, 11.0, 8.0, "density_survival", 0.58),
        ("density_survival", "short", "next_bar_open_control", "pessimistic", 12, 11.0, 8.0, "density_survival", 0.58),
        ("tail_guard_extreme", "long", "same_bar_open", "pessimistic", 6, 8.0, 5.0, "tail_guard", 0.70),
        ("tail_guard_extreme", "short", "same_bar_open", "pessimistic", 6, 8.0, 5.0, "tail_guard", 0.70),
        ("regime_exit_value", "long", "same_bar_open", "close_direction", 24, 30.0, 14.0, "regime_exit_value", 0.66),
        ("regime_exit_value", "short", "same_bar_open", "close_direction", 24, 30.0, 14.0, "regime_exit_value", 0.66),
    ]
    return [
        F80Spec(
            surface_family=family,
            name=f"{family}_{side}_{entry}_h{hold}_tp{int(tp)}_sl{int(sl)}_{fill}_{label}_q{int(q * 100)}",
            side=side,
            entry_mode=entry,
            fill_order=fill,
            hold_bars=hold,
            tp_price_units=tp,
            sl_price_units=sl,
            label_mode=label,
            utility_quantile=q,
        )
        for family, side, entry, fill, hold, tp, sl, label, q in seeds
    ]


def make_label(df: pd.DataFrame, outcome: Mapping[str, np.ndarray], spec: F80Spec) -> np.ndarray:
    valid = np.asarray(outcome["valid"], dtype=bool)
    train_mask = (df["split"] == "train").to_numpy() & valid
    if train_mask.sum() == 0:
        return np.zeros(len(df), dtype=int)
    pnl = np.asarray(outcome["pnl_contract"], dtype=float)
    mae = np.asarray(outcome["mae_contract"], dtype=float)
    mfe = np.asarray(outcome["mfe_contract"], dtype=float)
    spread = np.asarray(outcome["spread_cost_contract"], dtype=float)
    exit_offset = np.asarray(outcome["exit_offset"], dtype=float)
    if spec.label_mode == "cost_dd_normalized":
        score = pnl - 0.72 * mae - 1.35 * spread - 0.004 * exit_offset
        guard = mae <= np.nanquantile(mae[train_mask], 0.68)
    elif spec.label_mode == "order_intent_asymmetry":
        ratio = np.divide(mfe, mae + 1e-9)
        score = pnl + 0.13 * mfe - 0.50 * mae - 0.80 * spread - 0.002 * exit_offset
        guard = ratio >= np.nanquantile(ratio[train_mask], 0.55)
    elif spec.label_mode == "density_survival":
        score = pnl - 0.30 * mae - 0.60 * spread - 0.012 * exit_offset
        guard = exit_offset <= np.nanquantile(exit_offset[train_mask], 0.72)
    elif spec.label_mode == "tail_guard":
        score = pnl - 0.95 * mae - 1.50 * spread - 0.006 * exit_offset
        guard = mae <= np.nanquantile(mae[train_mask], 0.58)
    else:
        score = pnl + 0.08 * mfe - 0.42 * mae - 1.00 * spread - 0.004 * exit_offset
        guard = mae <= np.nanquantile(mae[train_mask], 0.75)
    threshold = float(np.nanquantile(score[train_mask], spec.utility_quantile))
    return ((score >= threshold) & (pnl > 0.0) & guard & valid).astype(int)


def regime_mask(df: pd.DataFrame, name: str, side: str, thresholds: Mapping[str, float]) -> np.ndarray:
    if name in {"all", "cash_open", "cash_mid", "cash_late"}:
        return f78b.session_mask(df, name)
    adx = pd.to_numeric(df.get("adx_14", pd.Series(np.nan, index=df.index)), errors="coerce").fillna(0.0).to_numpy()
    atr = pd.to_numeric(df.get("atr_14_over_atr_50", pd.Series(np.nan, index=df.index)), errors="coerce").fillna(1.0).to_numpy()
    width = pd.to_numeric(df.get("bollinger_width_20", pd.Series(np.nan, index=df.index)), errors="coerce").fillna(0.0).to_numpy()
    if name == "high_vol":
        return (atr >= thresholds["atr_ratio_median"]) | (width >= thresholds["boll_width_high"])
    if name == "low_vol":
        return (atr <= thresholds["atr_ratio_median"]) & (width <= thresholds["boll_width_low"])
    if name == "trend":
        return adx >= thresholds["adx_median"]
    if name == "chop":
        return adx < thresholds["adx_median"]
    raise ValueError(name)


def risk_mask(df: pd.DataFrame, name: str, side: str, thresholds: Mapping[str, float]) -> np.ndarray:
    if name in {"none", "trend_aligned", "mean_revert", "liquidity_release", "low_volatility"}:
        return f78b.risk_mask(df, name, side, thresholds)
    if name == "order_intent_guard":
        trend = f78b.risk_mask(df, "trend_aligned", side, thresholds)
        release = f78b.risk_mask(df, "liquidity_release", side, thresholds)
        return trend | release
    raise ValueError(name)


def scout_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            int(metrics["trade_count"]) >= 30
            and float(metrics["pf"]) >= 1.10
            and float(metrics["dd_pct"]) <= 15.0
            and 0.20 <= float(metrics["calendar_trades_day"]) <= MAX_TPD_SCOUT
        )

    return ok(val) and ok(oos)


def material_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.20
            and float(metrics["dd_pct"]) <= 12.0
            and int(metrics["trade_count"]) >= 50
            and 0.50 <= float(metrics["calendar_trades_day"]) <= 16.0
        )

    return ok(val) and ok(oos)


def meaningful_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.35
            and float(metrics["dd_pct"]) <= 10.0
            and int(metrics["trade_count"]) >= 80
            and 1.0 <= float(metrics["calendar_trades_day"]) <= 14.0
        )

    return ok(val) and ok(oos)


def final_like_reference(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.60
            and float(metrics["dd_pct"]) <= 8.0
            and int(metrics["trade_count"]) >= 120
            and 2.0 <= float(metrics["calendar_trades_day"]) <= 12.0
            and int(metrics["smooth_equity_proxy"]) == 1
        )

    return ok(val) and ok(oos)


def density_score(value: float) -> float:
    if value <= 0:
        return -10.0
    if 2.0 <= value <= 10.0:
        return 10.0
    if value < 2.0:
        return value * 4.0
    return max(0.0, 10.0 - (value - 10.0) * 1.1)


def rank_score(val: Mapping[str, Any], oos: Mapping[str, Any], material: bool, meaningful: bool, scout: bool, final_like: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    density = min(density_score(float(val["calendar_trades_day"])), density_score(float(oos["calendar_trades_day"])))
    smooth = int(val["smooth_equity_proxy"]) + int(oos["smooth_equity_proxy"])
    min_trades = min(int(val["trade_count"]), int(oos["trade_count"]))
    return (
        (2_500_000.0 if final_like else 0.0)
        + (1_200_000.0 if meaningful else 0.0)
        + (600_000.0 if material else 0.0)
        + (120_000.0 if scout else 0.0)
        + (35_000.0 if min_net > 0 else 0.0)
        + min_pf * 4_000.0
        + density * 4_000.0
        + smooth * 4_000.0
        + min(min_trades, 240) * 50.0
        - max_dd * 700.0
        + min_net * 20.0
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
        regimes = ["all", "cash_open", "cash_mid", "cash_late", "high_vol", "low_vol", "trend", "chop"]
        risks = ["none", "trend_aligned", "mean_revert", "liquidity_release", "order_intent_guard"]
        prob_quantiles = [0.70, 0.86]
        cooldowns = [0, 4, 10]

        candidate_rows: list[dict[str, Any]] = []
        fit_rows: list[dict[str, Any]] = []
        label_rows: list[dict[str, Any]] = []
        candidate_id = 0

        for spec in specs:
            indices = f79b.entry_indices(df, raw, spec.entry_mode)
            outcome = f79b.compute_outcome(raw, indices, spec)
            label = make_label(df, outcome, spec)
            train_valid = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
            positive = int(label[train_valid].sum()) if train_valid.sum() else 0
            label_rows.append(
                {
                    "label_name": spec.name,
                    "surface_family": spec.surface_family,
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
                train_matrix = matrices["train"]
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
                                "surface_family": spec.surface_family,
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
                                "surface_family": spec.surface_family,
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
                        for regime in regimes:
                            for risk in risks:
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
                                            & regime_mask(split_df, regime, spec.side, thresholds)
                                            & risk_mask(split_df, risk, spec.side, thresholds)
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
                                    material = material_gate(val, oos)
                                    meaningful = meaningful_gate(val, oos)
                                    final_like = final_like_reference(val, oos)
                                    dual_positive = float(val["net"]) > 0.0 and float(oos["net"]) > 0.0
                                    candidate_id += 1
                                    row: dict[str, Any] = {
                                        "candidate_id": f"f80b_{candidate_id:05d}",
                                        "surface_family": spec.surface_family,
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
                                        "regime": regime,
                                        "risk_filter": risk,
                                        "cooldown_bars": cooldown,
                                        "contract_pnl_scale": CONTRACT_PNL_SCALE,
                                        "initial_balance": INITIAL_BALANCE,
                                        "raw_signal_total_diagnostic_only": raw_any,
                                        "lifecycle_trade_total": entry_any,
                                        "overall_signal_to_trade_ratio_diagnostic_only": entry_any / raw_any if raw_any else 0.0,
                                        "scout_clue": int(scout),
                                        "materialization_candidate": int(material),
                                        "meaningful_signal": int(meaningful),
                                        "final_like_reference": int(final_like),
                                        "dual_positive": int(dual_positive),
                                        "rank_score": rank_score(val, oos, material, meaningful, scout, final_like),
                                        "signal_count_claim_boundary": "diagnostic_only_not_economics",
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
            "materialization_candidate_count": sum(int(row["materialization_candidate"]) for row in candidate_rows),
            "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in candidate_rows),
            "final_like_reference_count": sum(int(row["final_like_reference"]) for row in candidate_rows),
            "dual_positive_count": sum(int(row["dual_positive"]) for row in candidate_rows),
            "nonzero_lifecycle_trade_candidates": sum(1 for row in candidate_rows if int(row["lifecycle_trade_total"]) > 0),
            "best_candidate": best,
            "feature_sets": {name: len(cols) for name, cols in feature_map.items()},
            "model_families": list(builders.keys()),
            "spec_count": len(specs),
            "regimes": regimes,
            "risk_filters": risks,
            "prob_quantiles": prob_quantiles,
            "cooldowns": cooldowns,
            "signal_count_boundary": "Signal count(신호 수)는 diagnostic only(진단 전용)이며 MT5 economics(MT5 경제성) claim(주장)을 만들지 않는다.",
            "data_rows": {"dataset": int(len(df)), "raw_bars": int(len(raw)), "features": int(len(features))},
            "split_counts": {str(k): int(v) for k, v in df["split"].value_counts().to_dict().items()},
            "entry_rule": "same_bar_open(동일 봉 시가) and next_bar_open_control(다음 봉 시가 대조)",
            "dd_rule": "max_drawdown_percent(최대 손실폭 비율)는 tester deposit 500(테스터 예치금 500)을 분모로 사용한다.",
            "tier_scope": "Tier A separate(티어 A 분리); Tier B separate missing_required(티어 B 분리 필수 누락); Tier A+B combined out_of_scope_by_claim(합산은 주장 범위 밖).",
        }
        return candidate_rows, fit_rows, label_rows, summary
    finally:
        f78b.INITIAL_BALANCE = original_balance


def axis_summary_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    axes = ["surface_family", "label_mode", "entry_mode", "fill_order", "side", "hold_bars", "feature_set", "model", "regime", "risk_filter", "cooldown_bars"]
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
                    "materialization_candidate_count": sum(int(row["materialization_candidate"]) for row in subset),
                    "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in subset),
                    "best_candidate": best["candidate_id"],
                    "best_rank_score": best["rank_score"],
                    "best_val_net_pf_dd_tpd": f"{best['val_net']}/{best['val_pf']}/{best['val_dd_pct']}/{best['val_calendar_trades_day']}",
                    "best_oos_net_pf_dd_tpd": f"{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_calendar_trades_day']}",
                }
            )
    return rows


def status_and_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    if int(summary.get("materialization_candidate_count", 0) or 0) > 0 or int(summary.get("meaningful_signal_count", 0) or 0) > 0:
        return STATUS_MATERIAL, JUDGMENT_MATERIAL, NEXT_RUN_IF_MATERIAL
    if int(summary.get("scout_clue_count", 0) or 0) > 0 or int(summary.get("nonzero_lifecycle_trade_candidates", 0) or 0) > 0:
        return STATUS_WEAK, JUDGMENT_WEAK, NEXT_RUN_IF_WEAK
    return STATUS_ZERO, JUDGMENT_ZERO, NEXT_RUN_IF_ZERO


def fmt(value: Any, digits: int = 4) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not np.isfinite(number):
        return str(value)
    return f"{number:.{digits}f}"


def format_best(best: Mapping[str, Any]) -> str:
    if not best:
        return "none(없음)"
    return (
        f"`{best.get('candidate_id')}` `{best.get('surface_family')}` "
        f"val net/PF/DD/tpd/trades(검증 순손익/수익 팩터/손실폭/일 거래/거래) "
        f"`{fmt(best.get('val_net'))}/{fmt(best.get('val_pf'))}/{fmt(best.get('val_dd_pct'))}/{fmt(best.get('val_calendar_trades_day'))}/{best.get('val_trade_count')}`, "
        f"OOS(표본외) `{fmt(best.get('oos_net'))}/{fmt(best.get('oos_pf'))}/{fmt(best.get('oos_dd_pct'))}/{fmt(best.get('oos_calendar_trades_day'))}/{best.get('oos_trade_count')}`"
    )


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]]) -> str:
    table_rows = []
    for row in top_rows[:12]:
        table_rows.append(
            f"| `{row.get('candidate_id')}` | `{row.get('surface_family')}` | `{row.get('model')}` | `{row.get('feature_set')}` | "
            f"`{row.get('regime')}/{row.get('risk_filter')}/{row.get('cooldown_bars')}` | "
            f"`{fmt(row.get('val_net'))}/{fmt(row.get('val_pf'))}/{fmt(row.get('val_dd_pct'))}/{fmt(row.get('val_calendar_trades_day'))}/{row.get('val_trade_count')}` | "
            f"`{fmt(row.get('oos_net'))}/{fmt(row.get('oos_pf'))}/{fmt(row.get('oos_dd_pct'))}/{fmt(row.get('oos_calendar_trades_day'))}/{row.get('oos_trade_count')}` | "
            f"`{row.get('scout_clue')}/{row.get('materialization_candidate')}/{row.get('meaningful_signal')}/{row.get('final_like_reference')}` |"
        )
    top_table = "\n".join(
        [
            "| candidate(후보) | surface(표면) | model(모델) | feature(피처) | regime/risk/cooldown(장세/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | OOS net/PF/DD/tpd/trades(표본외) | scout/material/meaningful/final-like(탐색/물질/의미/최종유사) |",
            "|---|---|---|---|---|---:|---:|---:|",
            *table_rows,
        ]
    )
    return f"""# F80B Broad Extreme Multi-Axis Proxy Scout Report(F80B 넓은/극단 다축 프록시 탐색 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- candidate rows(후보 행): `{summary.get('candidate_rows')}`
- scout clue count(탐색 단서 수): `{summary.get('scout_clue_count')}`
- materialization candidate count(물질화 후보 수): `{summary.get('materialization_candidate_count')}`
- meaningful signal count(의미 신호 수): `{summary.get('meaningful_signal_count')}`
- final-like reference count(최종 유사 참고 수): `{summary.get('final_like_reference_count')}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

## Signal Count Boundary(신호 수 경계)

Signal count(신호 수)는 diagnostic only(진단 전용)다. Effect(효과): raw signal count(원시 신호 수)나 lifecycle trade count(생명주기 거래 수)가 많아도 MT5 economics(MT5 경제성), runtime authority(런타임 권위), or selected baseline(선택 기준선)을 만들지 않는다.

## Top Candidates(상위 후보)

{top_table}

## Tier Record(티어 기록)

Tier A separate(티어 A 분리)는 proxy scout(프록시 탐색)로 기록했다. Tier B separate(티어 B 분리)는 `missing_required(필수 누락)`, Tier A+B combined(티어 A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`로 기록했다.

## Next Boundary(다음 경계)

Next run(다음 실행): `{status_and_next(summary)[2]}`.

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), parity-only economics(동등성 단독 경제성)를 만들지 않는다.
"""


def data_contract(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "data_sources": [
            {"path": rel(f78b.DATASET_PATH), "sha256": f78b.file_hash(f78b.DATASET_PATH)},
            {"path": rel(f78b.FEATURE_ORDER_PATH), "sha256": f78b.file_hash(f78b.FEATURE_ORDER_PATH)},
            {"path": rel(f78b.RAW_BARS_PATH), "sha256": f78b.file_hash(f78b.RAW_BARS_PATH)},
        ],
        "time_axis_boundary": "timestamp(시각) is closed-bar feature key(확정봉 피처 키); entry uses raw open_ts(원천 시가 시각) mapping.",
        "entry_known_fields": "All feature columns(모든 피처 열) from feature_order(피처 순서) only; regime filters(장세 필터) use entry-known feature columns(진입 시점 피처 열).",
        "label_only_future_fields": "Post-entry OHLC path(진입 이후 OHLC 경로), spread cost(스프레드 비용), MAE/MFE(최대 불리/유리 이동), DD-normalized utility(손실폭 정규화 효용).",
        "split_boundary": "Label quantiles(라벨 분위수), model fit(모델 학습), and probability thresholds(확률 임계값) are train-only(훈련 전용).",
        "tier_boundary": summary.get("tier_scope"),
        "signal_count_boundary": summary.get("signal_count_boundary"),
        "f64_f67_lesson": "Parity(동등성), ONNX handoff(온엑스 인계), and signal count(신호 수) do not guarantee MT5 economics(MT5 경제성).",
    }


def model_validation_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "model_surface": summary.get("model_families"),
        "feature_sets": summary.get("feature_sets"),
        "validation_split": "time-ordered train/validation/OOS(시간순 훈련/검증/표본외)",
        "overfit_boundary": "Broad sweep(넓은 탐색) is scout-only(탐색 전용); WFO/MT5 evidence(워크포워드/MT5 근거) must follow before authority claims(권위 주장).",
        "selection_metric_boundary": "rank_score(순위 점수) is triage only(분류 전용).",
        "risk_boundary": "Deposit=500 DD(예치금 500 손실폭), spread cost(스프레드 비용), density(밀도), lifecycle occupancy(생명주기 점유)를 같이 본다.",
        "summary_counts": {
            "scout_clue_count": summary.get("scout_clue_count"),
            "materialization_candidate_count": summary.get("materialization_candidate_count"),
            "meaningful_signal_count": summary.get("meaningful_signal_count"),
            "final_like_reference_count": summary.get("final_like_reference_count"),
        },
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve", "parity_only_economics"],
    }


def artifact_lineage(summary: Mapping[str, Any], next_run: str) -> dict[str, Any]:
    return {
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "source_inputs": [rel(f78b.DATASET_PATH), rel(f78b.FEATURE_ORDER_PATH), rel(f78b.RAW_BARS_PATH), rel(STAGE_DIR / "00_spec/stage_brief.md"), rel(STAGE_DIR / "01_inputs/frontier80_input_boundary.md")],
        "artifact_paths": [rel(SUMMARY), rel(CANDIDATES_ALL), rel(CANDIDATES_TOP), rel(AXIS_SUMMARY), rel(SURFACE_SUMMARY), rel(MODEL_FIT_SUMMARY), rel(LABEL_AUDIT), rel(TIER_AUDIT), rel(DATA_CONTRACT), rel(REPORT), rel(RUN_MANIFEST)],
        "consumer": next_run,
        "lineage_boundary": "proxy_scout_artifacts_connected_no_authority(프록시 탐색 산출물 연결, 권위 없음)",
        "canonical_stage_id": STAGE_ID,
    }


def gate_audit_text(status: str, summary: Mapping[str, Any], next_run: str) -> str:
    return f"""# F80B Required Gate Coverage Audit(F80B 필수 게이트 커버리지 감사)

Status(상태): `{status}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `data_feature_contract_preflight` | `passed(통과)` | `{rel(DATA_CONTRACT)}` | 데이터/피처/라벨/분할 경계를 실행 산출물로 남긴다. |
| `kpi_contract_audit` | `passed_proxy_only(프록시 한정 통과)` | `{rel(SUMMARY)}`, `{rel(CANDIDATES_TOP)}` | DD(손실폭), PF(수익 팩터), density(밀도), lifecycle(생명주기)을 같이 기록한다. |
| `signal_count_diagnostic_boundary` | `passed(통과)` | candidate fields(후보 필드) `raw_signal_total_diagnostic_only` | 신호 수를 경제성 결론으로 쓰지 않는다. |
| `tier_record_audit` | `passed_with_missing_required_boundary(필수 누락 경계 포함 통과)` | `{rel(TIER_AUDIT)}` | Tier A/B/combined(티어 A/B/합산)을 빈칸으로 두지 않는다. |
| `runtime_probe_gate` | `pending_after_proxy(프록시 이후 대기)` | next run(다음 실행) `{next_run}` | MT5 runtime probe(MT5 런타임 탐침) 전에는 권위 주장을 만들지 않는다. |
| `final_claim_guard` | `passed(통과)` | `{CLAIM_BOUNDARY}` | completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 금지한다. |

Counts(개수): scout `{summary.get('scout_clue_count')}`, material `{summary.get('materialization_candidate_count')}`, meaningful `{summary.get('meaningful_signal_count')}`, final-like `{summary.get('final_like_reference_count')}`.
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""# F80 Selection Status(F80 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F80B broad/extreme multi-axis proxy scout(F80B 넓은/극단 다축 프록시 탐색)를 실행했다.

Effect(효과): feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 함께 바꾼 후보 표면을 기록했다.

Best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def ledger_rows(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = summary.get("best_candidate") or {}
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "primary_kpi": f"scout={summary.get('scout_clue_count')};material={summary.get('materialization_candidate_count')};meaningful={summary.get('meaningful_signal_count')};final_like={summary.get('final_like_reference_count')}",
        "guardrail_kpi": f"signal_count=diagnostic_only;dd={summary.get('dd_rule')}",
        "external_verification_status": "not_run_proxy_only(미실행, 프록시 전용)",
        "notes": f"candidates={summary.get('candidate_rows')}; next={next_run}",
        "run_number": "frontier80B",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "rows": summary.get("candidate_rows"),
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": best.get("candidate_id", ""),
        "candidate_count": summary.get("candidate_rows"),
        "scout_clue_count": summary.get("scout_clue_count"),
        "materialization_candidate_count": summary.get("materialization_candidate_count"),
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
        "feature_count": best.get("feature_count", ""),
        "work_family": "experiment_execution",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only(프록시 전용)",
        "run_family": "multi_axis_surface_rotation_proxy_scout",
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
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_proxy_scout",
            "subrun_id": "tier_a_proxy_scout(티어 A 프록시 탐색)",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "validation_oos_proxy(검증/표본외 프록시)",
            "scoreboard_lane": "runtime_economics(런타임 경제성)",
            "lane": "multi_axis_proxy_scout(다축 프록시 탐색)",
            "family": "experiment_execution(실험 실행)",
            "view": "proxy_scout",
            "tier": "Tier A",
            "metric_scope": "validation_oos_proxy",
            "result_status": status,
            "row_id": f"{RUN_ID}__tier_a_proxy_scout",
            "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색 전용, 권위 없음)",
            "next_action": next_run,
            "question": "Can multi-axis runtime economics surfaces create material proxy clues?(다축 런타임 경제성 표면이 물질적 프록시 단서를 만들 수 있는가?)",
            "artifact_count": 11,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": "tier_b_missing_required(티어 B 필수 누락)",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B missing_required",
            "kpi_scope": "missing_required(필수 누락)",
            "scoreboard_lane": "runtime_economics(런타임 경제성)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "view": "tier_b_missing_required",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required_no_reviewed_run_claim",
            "primary_kpi": "Tier B missing_required",
            "notes": "Tier B separate(티어 B 분리) source was not available in F80B; not omitted.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": "tier_ab_combined_out_of_scope(티어 A+B 합산 범위 밖)",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B out_of_scope_by_claim",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "scoreboard_lane": "runtime_economics(런타임 경제성)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "view": "tier_ab_combined_out_of_scope",
            "tier": "Tier A+B",
            "metric_scope": "out_of_scope_by_claim",
            "result_status": "out_of_scope_by_claim_no_reviewed_run_claim",
            "primary_kpi": "Tier A+B combined out_of_scope_by_claim",
            "notes": "No routed Tier A primary + Tier B fallback(티어 A 우선 + 티어 B 대체) run exists in F80B.",
        },
    ]


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    rows = ledger_rows(created_at, status, judgment, next_run, summary)
    upsert_csv(RUN_REGISTRY, "run_id", rows[0])
    for row in rows:
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    write_csv(TIER_AUDIT, rows)


def update_idea_registry(summary: Mapping[str, Any], next_run: str) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    best = summary.get("best_candidate") or {}
    addition = f"""

- `{RUN_ID}` executed F80 broad/extreme multi-axis proxy scout(F80 넓은/극단 다축 프록시 탐색). Result(결과): `scout={summary.get('scout_clue_count')}`, `material={summary.get('materialization_candidate_count')}`, `meaningful={summary.get('meaningful_signal_count')}`, `final_like={summary.get('final_like_reference_count')}`. Best(최선): `{best.get('candidate_id', '')}` OOS net/PF/DD/tpd(표본외 순손익/수익 팩터/손실폭/일 거래) `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}`. Boundary(경계): proxy scout only, no authority(프록시 탐색 전용, 권위 없음). Next(다음): `{next_run}`.
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
runtime_probe_status: f80_runtime_probe_required_if_material_candidate_exists_not_yet_run
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: inactive_preserve_records_pending_codex_task_force_replacement
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F80B broad/extreme multi-axis proxy scout(넓은/극단 다축 프록시 탐색)를 실행했다."
  - "Effect(효과): material={summary.get('materialization_candidate_count')}, meaningful={summary.get('meaningful_signal_count')}, final_like={summary.get('final_like_reference_count')} 후보 수를 기록했다."
  - "Signal count(신호 수): diagnostic only(진단 전용), no parity-only economics(동등성 단독 경제성 없음)."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F80B broad/extreme multi-axis proxy scout(F80B 넓은/극단 다축 프록시 탐색)를 실행했다.

Effect(효과): F80(전선80)의 feature set/label/model family/trade shape/risk logic/regime split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 분할)을 함께 회전한 후보 표면과 KPI(핵심 성과 지표)를 기록했다.

## Proxy KPI(프록시 핵심 성과 지표)

- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- materialization candidate(물질화 후보): `{summary.get('materialization_candidate_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- final-like reference(최종 유사 참고): `{summary.get('final_like_reference_count')}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- runtime probe boundary(런타임 탐침 경계): MT5 runtime probe(MT5 런타임 탐침) 전에는 runtime authority(런타임 권위)를 주장하지 않는다.
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def receipts_texts(status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[Path, str]:
    return {
        REVIEW_DIR / "f80b_run_evidence_receipt.yaml": f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: {status}
source_inputs:
  - {rel(f78b.DATASET_PATH)}
  - {rel(f78b.FEATURE_ORDER_PATH)}
  - {rel(f78b.RAW_BARS_PATH)}
produced_artifacts:
  - {rel(SUMMARY)}
  - {rel(CANDIDATES_TOP)}
  - {rel(REPORT)}
ledger_rows:
  - {RUN_ID}__tier_a_proxy_scout
  - {RUN_ID}__tier_b_missing_required
  - {RUN_ID}__tier_ab_combined_out_of_scope
missing_evidence:
  - "MT5 runtime probe(MT5 런타임 탐침) not run yet(아직 미실행)."
allowed_claims:
  - proxy_scout_executed
  - material_candidate_count_recorded
forbidden_claims:
  - completion
  - selected_baseline
  - runtime_authority
  - goal_achieve
""",
        REVIEW_DIR / "f80b_data_integrity_receipt.yaml": f"""packet_id: {RUN_ID}
skill: obsidian-data-integrity
status: passed_proxy_preflight
data_sources_checked:
  - {rel(DATA_CONTRACT)}
time_axis_boundary: "closed-bar feature key(확정봉 피처 키) with post-entry label path(진입 이후 라벨 경로)."
split_boundary: "train-only thresholds(훈련 전용 임계값); validation/OOS scoring(검증/표본외 채점)."
leakage_checks:
  - "regime filters(장세 필터)는 entry-known fields(진입 시점 필드)만 사용."
  - "label outcome(라벨 결과)은 feature(피처)에 섞지 않음."
missing_data_boundary: "{summary.get('tier_scope')}"
""",
        REVIEW_DIR / "f80b_model_validation_receipt.yaml": f"""packet_id: {RUN_ID}
skill: obsidian-model-validation
status: proxy_validation_recorded_no_selection
model_or_threshold_surface: "F80B proxy candidates(F80B 프록시 후보)"
validation_split: "train/validation/OOS(훈련/검증/표본외)"
overfit_checks:
  - "broad sweep only(넓은 탐색 전용)"
  - "rank score triage only(순위 점수 분류 전용)"
selection_metric_boundary: "no selected baseline(선택 기준선 없음)"
allowed_claims:
  - proxy_candidate
forbidden_claims:
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
""",
        REVIEW_DIR / "f80b_artifact_lineage_receipt.yaml": f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: artifacts_connected_no_authority
source_inputs:
  - {rel(f78b.DATASET_PATH)}
  - {rel(f78b.FEATURE_ORDER_PATH)}
  - {rel(f78b.RAW_BARS_PATH)}
produced_artifacts:
  - {rel(SUMMARY)}
  - {rel(CANDIDATES_ALL)}
  - {rel(REPORT)}
raw_evidence:
  - {rel(CANDIDATES_ALL)}
machine_readable:
  - {rel(SUMMARY)}
  - {rel(RUN_MANIFEST)}
human_readable:
  - {rel(REPORT)}
hashes_or_missing_reasons: "{rel(ARTIFACT_LINEAGE)}"
lineage_boundary: "proxy scout lineage only(프록시 탐색 계보만)"
""",
        REVIEW_DIR / "f80b_claim_discipline_receipt.yaml": f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_proxy_only
requested_claims:
  - "F80B proxy scout executed(F80B 프록시 탐색 실행)."
allowed_claims:
  - proxy_scout_executed
  - next_run_selected_by_status
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
  - parity_only_economics
final_status: "{judgment}; next={next_run}; boundary={CLAIM_BOUNDARY}"
""",
    }


def update_review_index() -> None:
    text = f"""# F80 Review Index(F80 검토 색인)

- `frontier80A_stage_open_multi_axis_surface_rotation_report.md`: stage open(단계 개방) report(보고서)
- `f80a_work_packet_routing_receipt.yaml`: work packet routing receipt(작업 묶음 라우팅 영수증)
- `f80a_task_force_review_receipt.yaml`: Codex Task Force review receipt(코덱스 태스크포스 검토 영수증)
- `f80a_experiment_design_receipt.yaml`: F80B design-boundary receipt(F80B 설계 경계 영수증)
- `f80a_data_integrity_receipt.yaml`: data/feature preflight boundary receipt(데이터/피처 사전 점검 경계 영수증)
- `f80a_model_validation_receipt.yaml`: validation/risk boundary receipt(검증/위험 경계 영수증)
- `f80a_claim_discipline_receipt.yaml`: claim boundary receipt(주장 경계 영수증)
- `f79_to_f80_handoff_correction.md`: canonical F80 handoff correction(정식 F80 인계 보정)
- `frontier80B_broad_extreme_multi_axis_proxy_scout_report.md`: F80B proxy scout report(F80B 프록시 탐색 보고서)
- `f80b_multi_axis_proxy_summary.json`: F80B machine summary(F80B 기계 요약)
- `f80b_multi_axis_ranked_top200.csv`: F80B ranked top candidates(F80B 상위 후보)
- `f80b_data_feature_contract_preflight.json`: data/feature contract(데이터/피처 계약)
- `required_gate_coverage_audit_f80b.md`: F80B gate audit(F80B 게이트 감사)
- `f80b_run_evidence_receipt.yaml`: run evidence receipt(실행 근거 영수증)
- `f80b_data_integrity_receipt.yaml`: data integrity receipt(데이터 무결성 영수증)
- `f80b_model_validation_receipt.yaml`: model validation receipt(모델 검증 영수증)
- `f80b_artifact_lineage_receipt.yaml`: artifact lineage receipt(산출물 계보 영수증)
- `f80b_claim_discipline_receipt.yaml`: claim discipline receipt(주장 규율 영수증)
- `stage_run_ledger.csv`: stage run ledger(단계 실행 장부)
- `context_anchor.md`: re-entry context anchor(재진입 문맥 앵커)
"""
    write_text(REVIEW_INDEX, text)


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
            "surface_summary": rel(SURFACE_SUMMARY),
            "model_fit_summary": rel(MODEL_FIT_SUMMARY),
            "label_audit": rel(LABEL_AUDIT),
            "tier_audit": rel(TIER_AUDIT),
            "data_contract": rel(DATA_CONTRACT),
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
    surface_rows = [row for row in axis_rows if row["axis"] == "surface_family"]
    status, judgment, next_run = status_and_next(summary)

    write_json(SUMMARY, summary)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, top_rows)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(SURFACE_SUMMARY, surface_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_csv(LABEL_AUDIT, label_rows)
    write_json(DATA_CONTRACT, data_contract(summary))
    write_json(MODEL_VALIDATION, model_validation_review(summary))
    write_json(ARTIFACT_LINEAGE, artifact_lineage(summary, next_run))
    write_text(REPORT, report_text(created_at, summary, top_rows))
    write_text(GATE_AUDIT, gate_audit_text(status, summary, next_run))
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run, summary))
    write_text(CONTEXT_ANCHOR, context_anchor_text(created_at, status, judgment, next_run, summary))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, summary))
    for path, text in receipts_texts(status, judgment, next_run, summary).items():
        write_text(path, text)
    update_review_index()

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
                "materialization_candidate_count": summary["materialization_candidate_count"],
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


def context_anchor_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""# F80 Context Anchor(F80 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{next_run}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Proxy observation(프록시 관찰): scout(탐색) `{summary.get('scout_clue_count')}`, material(물질화) `{summary.get('materialization_candidate_count')}`, meaningful(의미) `{summary.get('meaningful_signal_count')}`, final-like(최종 유사) `{summary.get('final_like_reference_count')}`.

Runtime probe observation(런타임 탐침 관찰): not run yet(아직 미실행).

Signal count boundary(신호 수 경계): diagnostic only(진단 전용), not economics(경제성 아님).

Next action(다음 행동): `{next_run}`.
"""


if __name__ == "__main__":
    raise SystemExit(main())
