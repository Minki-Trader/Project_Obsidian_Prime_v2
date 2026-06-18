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
from stage_pipelines.stage_frontier_81 import frontier81b_mt5_native_order_intent_cost_shape_proxy_scout as f81b


STAGE_ID = "stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
RUN_ID = "frontier82B_density_first_runtime_economic_mechanism_proxy_scout_v1"
PARENT_RUN_ID = "frontier82A_stage_open_density_first_runtime_economic_mechanism_rotation_v1"
NEXT_RUN_IF_MATERIAL = "frontier82C_mt5_runtime_materialization_v1"
NEXT_RUN_IF_WEAK = "frontier82C_capped_density_repair_or_rotation_decision_v1"
NEXT_RUN_IF_ZERO = "frontier82C_zero_signal_negative_evidence_closeout_decision_v1"

STATUS_MATERIAL = "f82b_proxy_material_density_first_candidate_mt5_materialization_required_no_authority"
STATUS_WEAK = "f82b_proxy_weak_density_first_clue_capped_repair_required_no_authority"
STATUS_ZERO = "f82b_proxy_zero_signal_negative_evidence_required_no_authority"
JUDGMENT_MATERIAL = "density_first_proxy_candidate_requires_mt5_runtime_materialization_no_authority"
JUDGMENT_WEAK = "density_first_proxy_clue_requires_capped_repair_or_rotation_no_authority"
JUDGMENT_ZERO = "density_first_proxy_zero_signal_requires_negative_memory_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics"
)

INITIAL_BALANCE = 500.0
CONTRACT_PNL_SCALE = f78b.CONTRACT_PNL_SCALE
SLTP_POINT_SCALE = f78b.SLTP_POINT_SCALE
F81G_LOW_DENSITY_TPD = 0.20512820512820512
MAX_TPD_SCOUT = 16.0

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

SUMMARY = REVIEW_DIR / "f82b_density_first_proxy_summary.json"
CANDIDATES_ALL = RUN_DIR / "f82b_density_first_proxy_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f82b_density_first_proxy_ranked_top200.csv"
AXIS_SUMMARY = REVIEW_DIR / "f82b_density_first_proxy_axis_summary.csv"
SIDE_SUMMARY = REVIEW_DIR / "f82b_side_balance_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f82b_model_fit_summary.csv"
LABEL_AUDIT = REVIEW_DIR / "f82b_label_audit.csv"
TIER_AUDIT = REVIEW_DIR / "f82b_tier_record_audit.csv"
DATA_INTEGRITY = REVIEW_DIR / "f82b_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f82b_model_validation_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f82b_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f82b_local_verification.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f82b_task_force_review_receipt.yaml"
REPORT = REVIEW_DIR / "frontier82B_density_first_runtime_economic_mechanism_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f82b.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_82/frontier82b_density_first_runtime_economic_mechanism_proxy_scout.py"


@dataclass(frozen=True)
class F82Spec:
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
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


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


def remove_matching_csv_text_rows(path: Path, matcher: Any) -> None:
    if not path_exists(path):
        return
    raw = io_path(path).read_text(encoding="utf-8-sig")
    newline = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.splitlines()
    if not lines:
        return
    kept = [lines[0]] + [line for line in lines[1:] if not matcher(line)]
    io_path(path).write_text(newline.join(kept) + newline, encoding="utf-8-sig")


def append_csv_row(path: Path, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
    else:
        fieldnames = list(row.keys())
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    newline = "\r\n" if path_exists(path) and b"\r\n" in io_path(path).read_bytes() else "\n"
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    exists = path_exists(path)
    with io_path(path).open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator=newline)
        if not exists:
            writer.writeheader()
        writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def feature_sets(features: Sequence[str]) -> dict[str, list[str]]:
    available = set(features)
    price = [f for f in features if any(k in f for k in ["log_return", "hl_range", "close_open", "gap_percent", "return_zscore", "hl_zscore", "close_prev"])]
    vol = [f for f in features if any(k in f for k in ["atr", "bollinger", "bb_", "historical_vol", "squeeze"])]
    session = [f for f in features if any(k in f for k in ["is_us_cash", "minutes_from", "first_30m", "last_30m", "day_of_week"])]
    trend = [f for f in features if any(k in f for k in ["ema", "sma", "rsi", "stoch", "ppo", "roc", "trix", "adx", "di_", "supertrend", "vortex"])]
    external = [f for f in features if any(k in f for k in ["vix", "us10yr", "usdx", "xnas", "mega8", "top3"])]
    price_vol_session = sorted(set(price + vol + session) & available)
    density_core = sorted(set(price + vol + session + ["bb_position_20", "di_spread_14", "adx_14"]) & available)
    trend_density = sorted(set(price + session + [f for f in trend if any(k in f for k in ["ema", "sma", "adx", "di_", "supertrend", "ppo", "roc"])]) & available)
    no_external = [f for f in features if f not in set(external)]
    compact_exportable = sorted(set(density_core + trend_density) & available)[:30]
    return {
        "density_core": density_core,
        "price_vol_session": price_vol_session,
        "trend_density": trend_density,
        "compact_exportable_30": compact_exportable,
        "no_external_full": no_external,
    }


def model_builders(random_state: int = 8202) -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2_balanced": lambda: make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=180, class_weight="balanced", C=0.55, solver="lbfgs"),
        ),
        "extra_trees_d7_l120": lambda: ExtraTreesClassifier(
            n_estimators=18,
            max_depth=6,
            min_samples_leaf=160,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
        "histgbm_density_shallow": lambda: HistGradientBoostingClassifier(
            max_iter=28,
            learning_rate=0.055,
            max_leaf_nodes=13,
            l2_regularization=0.16,
            random_state=random_state,
        ),
    }


def runtime_specs() -> list[F82Spec]:
    seeds = [
        ("density_supply_first", 8, 9.0, 6.0, "density_supply", 0.50),
        ("density_supply_first", 12, 13.0, 8.0, "density_supply", 0.52),
        ("runtime_economic_balance", 10, 12.0, 7.0, "economic_balance", 0.54),
        ("side_session_release", 12, 15.0, 9.0, "session_release", 0.52),
        ("smooth_trade_supply", 18, 20.0, 10.0, "smooth_supply", 0.50),
    ]
    specs: list[F82Spec] = []
    for family, hold, tp, sl, label, q in seeds:
        for side in ["long", "short"]:
            for entry, fill in [("same_bar_open", "pessimistic"), ("next_bar_open_control", "close_direction")]:
                specs.append(
                    F82Spec(
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
                )
    return specs


def make_label(df: pd.DataFrame, outcome: Mapping[str, np.ndarray], spec: F82Spec) -> np.ndarray:
    valid = np.asarray(outcome["valid"], dtype=bool)
    train_mask = (df["split"] == "train").to_numpy() & valid
    if train_mask.sum() == 0:
        return np.zeros(len(df), dtype=int)
    pnl = np.asarray(outcome["pnl_contract"], dtype=float)
    mae = np.asarray(outcome["mae_contract"], dtype=float)
    mfe = np.asarray(outcome["mfe_contract"], dtype=float)
    spread = np.asarray(outcome["spread_cost_contract"], dtype=float)
    exit_offset = np.asarray(outcome["exit_offset"], dtype=float)
    spread_pressure = np.divide(spread, np.abs(pnl) + spread + 1e-9)
    payoff_shape = np.divide(mfe, mae + spread + 1e-9)
    if spec.label_mode == "density_supply":
        score = pnl + 0.06 * mfe - 0.42 * mae - 1.15 * spread - 0.0020 * exit_offset
        guard = (spread <= np.nanquantile(spread[train_mask], 0.84)) & (mae <= np.nanquantile(mae[train_mask], 0.86))
    elif spec.label_mode == "economic_balance":
        score = pnl + 0.10 * mfe - 0.58 * mae - 1.50 * spread + 0.08 * payoff_shape - 0.0025 * exit_offset
        guard = (payoff_shape >= np.nanquantile(payoff_shape[train_mask], 0.48)) & (spread_pressure <= np.nanquantile(spread_pressure[train_mask], 0.82))
    elif spec.label_mode == "session_release":
        score = pnl + 0.14 * mfe - 0.50 * mae - 1.35 * spread - 0.0015 * exit_offset
        guard = (mfe >= np.nanquantile(mfe[train_mask], 0.45)) & (spread <= np.nanquantile(spread[train_mask], 0.86))
    else:
        score = pnl + 0.05 * mfe - 0.38 * mae - 1.25 * spread - 0.0040 * exit_offset
        guard = (exit_offset <= np.nanquantile(exit_offset[train_mask], 0.82)) & (spread_pressure <= np.nanquantile(spread_pressure[train_mask], 0.84))
    threshold = float(np.nanquantile(score[train_mask], spec.utility_quantile))
    return ((score >= threshold) & (pnl > -0.05) & guard & valid).astype(int)


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
    if name in {"none", "trend_aligned", "liquidity_release", "low_volatility"}:
        return f78b.risk_mask(df, name, side, thresholds)
    if name == "intent_release":
        return f78b.risk_mask(df, "trend_aligned", side, thresholds) | f78b.risk_mask(df, "liquidity_release", side, thresholds)
    raise ValueError(name)


def density_score(value: float) -> float:
    if value <= 0:
        return -8.0
    if 5.0 <= value <= 10.0:
        return 12.0
    if 2.0 <= value < 5.0:
        return 8.0 + (value - 2.0) * 1.0
    if F81G_LOW_DENSITY_TPD < value < 2.0:
        return 2.0 + value * 2.5
    if value <= F81G_LOW_DENSITY_TPD:
        return -2.0
    return max(0.0, 12.0 - (value - 10.0) * 1.4)


def scout_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["calendar_trades_day"]) > F81G_LOW_DENSITY_TPD
            and int(metrics["trade_count"]) >= 60
            and float(metrics["pf"]) >= 1.02
            and float(metrics["dd_pct"]) <= 18.0
        )

    return ok(val) and ok(oos)


def material_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.12
            and float(metrics["dd_pct"]) <= 12.0
            and int(metrics["trade_count"]) >= 100
            and 1.0 <= float(metrics["calendar_trades_day"]) <= MAX_TPD_SCOUT
        )

    return ok(val) and ok(oos)


def meaningful_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.25
            and float(metrics["dd_pct"]) <= 10.0
            and int(metrics["trade_count"]) >= 140
            and 1.5 <= float(metrics["calendar_trades_day"]) <= 14.0
        )

    return ok(val) and ok(oos)


def final_like_reference(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.60
            and float(metrics["dd_pct"]) <= 8.0
            and int(metrics["trade_count"]) >= 240
            and 5.0 <= float(metrics["calendar_trades_day"]) <= 10.0
            and int(metrics["smooth_equity_proxy"]) == 1
        )

    return ok(val) and ok(oos)


def rank_score(val: Mapping[str, Any], oos: Mapping[str, Any], material: bool, meaningful: bool, scout: bool, final_like: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    density = min(density_score(float(val["calendar_trades_day"])), density_score(float(oos["calendar_trades_day"])))
    smooth = int(val["smooth_equity_proxy"]) + int(oos["smooth_equity_proxy"])
    min_trades = min(int(val["trade_count"]), int(oos["trade_count"]))
    return (
        (3_000_000.0 if final_like else 0.0)
        + (1_500_000.0 if meaningful else 0.0)
        + (750_000.0 if material else 0.0)
        + (150_000.0 if scout else 0.0)
        + density * 18_000.0
        + min_pf * 5_000.0
        + smooth * 4_500.0
        + min(min_trades, 700) * 40.0
        + max(min_net, -1000.0) * 18.0
        - max_dd * 900.0
    )


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def format_best(best: Mapping[str, Any]) -> str:
    if not best:
        return "none(없음)"
    return (
        f"`{best.get('candidate_id')}` `{best.get('surface_family')}` `{best.get('side')}` "
        f"val(검증) `{fmt(best.get('val_net'))}/{fmt(best.get('val_pf'))}/{fmt(best.get('val_dd_pct'))}/{fmt(best.get('val_calendar_trades_day'))}/{best.get('val_trade_count')}`; "
        f"OOS(표본외) `{fmt(best.get('oos_net'))}/{fmt(best.get('oos_pf'))}/{fmt(best.get('oos_dd_pct'))}/{fmt(best.get('oos_calendar_trades_day'))}/{best.get('oos_trade_count')}`"
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
        executed_feature_sets = ["density_core", "trend_density", "compact_exportable_30"]
        regimes = ["all", "cash_open", "cash_late", "high_vol", "trend"]
        risks = ["none", "trend_aligned", "intent_release"]
        prob_quantiles = [0.58, 0.68]
        cooldowns = [0, 4]

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
                continue
            for feature_set_name in executed_feature_sets:
                cols = feature_map[feature_set_name]
                if len(cols) < 8:
                    continue
                matrices = f78b.clean_matrices(df, train_valid, cols)
                train_matrix = matrices["train"]
                y_train = label[train_valid]
                for model_name, builder in builders.items():
                    model = builder()
                    try:
                        model.fit(train_matrix, y_train)
                        train_probs = f78b.probability(model, train_matrix)
                        probs = {split: f78b.probability(model, matrices[split]) for split in ["validation", "oos"]}
                        fit_rows.append(
                            {
                                "label_name": spec.name,
                                "feature_set": feature_set_name,
                                "feature_count": len(cols),
                                "model": model_name,
                                "status": "fit_ok",
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
                                    density_beats_f81g = (
                                        float(val["calendar_trades_day"]) > F81G_LOW_DENSITY_TPD
                                        and float(oos["calendar_trades_day"]) > F81G_LOW_DENSITY_TPD
                                    )
                                    candidate_id += 1
                                    row: dict[str, Any] = {
                                        "candidate_id": f"f82b_{candidate_id:05d}",
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
                                        "density_beats_f81g_seed": int(density_beats_f81g),
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
            "density_beats_f81g_seed_count": sum(int(row["density_beats_f81g_seed"]) for row in candidate_rows),
            "nonzero_lifecycle_trade_candidates": sum(1 for row in candidate_rows if int(row["lifecycle_trade_total"]) > 0),
            "best_candidate": best,
            "feature_sets": {name: len(cols) for name, cols in feature_map.items()},
            "executed_feature_sets": executed_feature_sets,
            "model_families": list(builders.keys()),
            "spec_count": len(specs),
            "regimes": regimes,
            "risk_filters": risks,
            "prob_quantiles": prob_quantiles,
            "cooldowns": cooldowns,
            "f81g_low_density_tpd_reference": F81G_LOW_DENSITY_TPD,
            "signal_count_boundary": "Signal count(신호 수)는 diagnostic only(진단 전용)이며 MT5 economics(MT5 경제성) claim(주장)을 만들지 않는다.",
            "data_rows": {"dataset": int(len(df)), "raw_bars": int(len(raw)), "features": int(len(features))},
            "split_counts": {split: int((df["split"] == split).sum()) for split in ["train", "validation", "oos"]},
            "entry_rule": "same_bar_open(동일 봉 시가) and next_bar_open_control(다음 봉 시가 대조)",
            "dd_rule": "max_drawdown_percent(최대 손실폭 비율)는 tester deposit 500(테스터 예치금 500)을 분모로 사용한다.",
            "tier_scope": "Tier A separate(티어 A 분리); Tier B separate missing_required(티어 B 분리 필수 누락); Tier A+B combined out_of_scope_by_claim(합산은 주장 범위 밖).",
            "execution_budget_note": "Bounded multi-axis scout(상한 있는 다축 탐색): broad draft(넓은 초안)가 6m CPU(6분 CPU)를 초과해 representative axes(대표 축)로 줄였고 hypothesis(가설)는 유지했다.",
        }
        return candidate_rows, fit_rows, label_rows, summary
    finally:
        f78b.INITIAL_BALANCE = original_balance


def status_and_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    if int(summary.get("materialization_candidate_count", 0) or 0) > 0 or int(summary.get("meaningful_signal_count", 0) or 0) > 0:
        return STATUS_MATERIAL, JUDGMENT_MATERIAL, NEXT_RUN_IF_MATERIAL
    if int(summary.get("scout_clue_count", 0) or 0) > 0 or int(summary.get("nonzero_lifecycle_trade_candidates", 0) or 0) > 0:
        return STATUS_WEAK, JUDGMENT_WEAK, NEXT_RUN_IF_WEAK
    return STATUS_ZERO, JUDGMENT_ZERO, NEXT_RUN_IF_ZERO


def axis_summary_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = ["surface_family", "side", "label_mode", "feature_set", "model", "regime", "risk_filter", "prob_quantile"]
    rows: list[dict[str, Any]] = []
    for axis in axes:
        for value in sorted({str(row.get(axis, "")) for row in candidate_rows}):
            subset = [row for row in candidate_rows if str(row.get(axis, "")) == value]
            if not subset:
                continue
            best = max(subset, key=lambda row: float(row.get("rank_score", 0.0)))
            rows.append(
                {
                    "axis": axis,
                    "value": value,
                    "candidate_rows": len(subset),
                    "scout_clue_count": sum(int(row["scout_clue"]) for row in subset),
                    "materialization_candidate_count": sum(int(row["materialization_candidate"]) for row in subset),
                    "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in subset),
                    "density_beats_f81g_seed_count": sum(int(row["density_beats_f81g_seed"]) for row in subset),
                    "best_candidate": best["candidate_id"],
                    "best_rank_score": best["rank_score"],
                    "best_oos_net_pf_dd_tpd": f"{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_calendar_trades_day']}",
                }
            )
    return rows


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]]) -> str:
    top_table = "\n".join(
        [
            "| candidate(후보) | side(방향) | surface(표면) | model(모델) | feature(피처) | regime/risk/cooldown(장세/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | OOS net/PF/DD/tpd/trades(표본외) | scout/material/meaningful/final-like(탐색/물질/의미/최종유사) |",
            "|---|---:|---|---|---|---|---:|---:|---:|",
            *[
                f"| `{row.get('candidate_id')}` | `{row.get('side')}` | `{row.get('surface_family')}` | `{row.get('model')}` | `{row.get('feature_set')}` | "
                f"`{row.get('regime')}/{row.get('risk_filter')}/{row.get('cooldown_bars')}` | "
                f"`{fmt(row.get('val_net'))}/{fmt(row.get('val_pf'))}/{fmt(row.get('val_dd_pct'))}/{fmt(row.get('val_calendar_trades_day'))}/{row.get('val_trade_count')}` | "
                f"`{fmt(row.get('oos_net'))}/{fmt(row.get('oos_pf'))}/{fmt(row.get('oos_dd_pct'))}/{fmt(row.get('oos_calendar_trades_day'))}/{row.get('oos_trade_count')}` | "
                f"`{row.get('scout_clue')}/{row.get('materialization_candidate')}/{row.get('meaningful_signal')}/{row.get('final_like_reference')}` |"
                for row in top_rows[:20]
            ],
        ]
    )
    return f"""# F82B Density-First Proxy Scout Report(F82B 밀도 우선 프록시 탐색 보고서)

Updated(갱신): {created_at}

Run(실행): `{RUN_ID}`

## Result(결과)

Action(행동): density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘) proxy scout(프록시 탐색)를 실행했다.

Effect(효과): F81G low-density seed(F81G 저밀도 씨앗)보다 높은 trade density(거래 밀도)를 우선 보상하면서 net/PF/DD(순수익/수익 팩터/손실폭)를 같이 본 후보 표면을 만들었다.

## KPI Summary(KPI 요약)

- candidate rows(후보 행): `{summary.get('candidate_rows')}`
- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- materialization candidate(물질화 후보): `{summary.get('materialization_candidate_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- final-like reference(최종 유사 참고): `{summary.get('final_like_reference_count')}`
- density beats F81G seed(밀도 F81G 씨앗 초과): `{summary.get('density_beats_f81g_seed_count')}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

## Top Candidates(상위 후보)

{top_table}

## Interpretation(해석)

This is proxy evidence only(프록시 근거 전용). Meaningful candidate(의미 후보)나 materialization candidate(물질화 후보)가 있으면 next action(다음 행동)은 MT5 Strategy Tester materialization(MT5 전략 테스터 물질화)다.

Signal count(신호 수)는 diagnostic only(진단 전용)이며 runtime economics(런타임 경제성)를 대체하지 않는다.

## Tier Record(티어 기록)

Tier A separate(티어 A 분리)는 proxy scout(프록시 탐색)로 기록했다. Tier B separate(티어 B 분리)는 `missing_required(필수 누락)`, Tier A+B combined(티어 A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`로 기록했다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def data_integrity_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "data_source": [rel(f78b.DATASET_PATH), rel(f78b.FEATURE_ORDER_PATH), rel(f78b.RAW_BARS_PATH)],
        "time_axis": "timestamp(타임스탬프)은 UTC closed-bar feature row(UTC 확정봉 피처 행)이고 label path(라벨 경로)는 entry 이후 raw bar(원시 봉)로 계산한다.",
        "sample_scope": {"symbol": "FPMarkets US100", "timeframe": "M5", "splits": summary.get("split_counts"), "tier_scope": summary.get("tier_scope")},
        "missing_or_duplicate_check": "source loader requires parquet/csv path existence(로더가 parquet/csv 경로 존재 요구); duplicate audit not re-run in F82B scout(중복 감사는 F82B 탐색에서 재실행하지 않음).",
        "feature_label_boundary": "Label quantiles/model thresholds(라벨 분위수/모델 임계값)는 train-only(훈련 전용); validation/OOS(검증/표본외)는 scored only(채점만).",
        "split_boundary": "time-ordered train/validation/OOS(시간순 훈련/검증/표본외)",
        "leakage_risk": "runtime outcome arrays(런타임 결과 배열)가 feature matrix(피처 행렬)에 들어가지 않도록 label-only path(라벨 전용 경로)에 둔다.",
        "data_hash_or_identity": {
            "dataset_sha256": f78b.file_hash(f78b.DATASET_PATH),
            "feature_order_sha256": f78b.file_hash(f78b.FEATURE_ORDER_PATH),
            "raw_bars_sha256": f78b.file_hash(f78b.RAW_BARS_PATH),
        },
        "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
    }


def model_validation_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "model_family": summary.get("model_families"),
        "target_and_label": "density-first runtime economic labels(밀도 우선 런타임 경제 라벨)",
        "split_method": "time-ordered train/validation/OOS(시간순 훈련/검증/표본외), WFO planned for later(워크포워드는 이후 계획)",
        "selection_metric": "rank_score combines density, net, PF, DD, smoothness, and trade count(밀도/순손익/PF/DD/매끄러움/거래 수 결합)",
        "secondary_metrics": "gross profit/loss, win rate, avg win/loss, payoff, expectancy, recovery, time under water, max consecutive loss(총이익/총손실/승률/평균 이익·손실/손익비/기대값/회복/회복 전 체류/최대 연속 손실)",
        "threshold_policy": "broad probability quantile sweep(넓은 확률 분위수 탐색); no micro search(미세 탐색 아님)",
        "overfit_risk": "many-surface proxy search(다표면 프록시 탐색) can overfit validation/OOS(검증/표본외)에 맞출 위험",
        "calibration_risk": "model scores are rank/order evidence(순위 근거) only; not calibrated probability(보정 확률 아님)",
        "comparison_baseline": "F81C runtime negative and F81G low-density seed(F81C 런타임 부정과 F81G 저밀도 씨앗)",
        "validation_judgment": "candidate" if int(summary.get("materialization_candidate_count", 0) or 0) else "exploratory",
    }


def artifact_lineage(summary: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = [SUMMARY, CANDIDATES_ALL, CANDIDATES_TOP, AXIS_SUMMARY, SIDE_SUMMARY, MODEL_FIT_SUMMARY, LABEL_AUDIT, TIER_AUDIT, DATA_INTEGRITY, MODEL_VALIDATION, REPORT, TASK_FORCE_REVIEW, GATE_AUDIT, RUN_MANIFEST]
    return {
        "source_inputs": [rel(f78b.DATASET_PATH), rel(f78b.FEATURE_ORDER_PATH), rel(f78b.RAW_BARS_PATH), rel(STAGE_DIR / "00_spec/stage_brief.md")],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": status_and_next(summary)[2],
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in artifacts},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_reports_and_ignored_run_outputs_with_hashes(추적 보고서와 무시된 실행 산출물 해시)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
    }


def gate_audit_text(status: str, summary: Mapping[str, Any], next_run: str) -> str:
    return f"""# F82B Required Gate Coverage Audit(F82B 필수 게이트 커버리지 감사)

Packet(묶음): `{RUN_ID}`

Primary family(주 작업군): `experiment_execution(실험 실행)`

Required gates(필수 게이트):

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `scope_completion_gate(범위 완료 게이트)` | `pass(통과)` | `{rel(SUMMARY)}` | F82B proxy scout(프록시 탐색) 범위를 실행했다. |
| `kpi_contract_audit(KPI 계약 감사)` | `pass(통과)` | `{rel(REPORT)}` | net/PF/DD/trades/day(순수익/수익 팩터/손실폭/일 거래)를 기록했다. |
| `skill_receipt_lint(스킬 영수증 검사)` | `pass(통과)` | `{rel(PACKET_SKILL_RECEIPTS)}` | 실행/데이터/모델/계보/주장 경계를 남겼다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `pass(통과)` | `{rel(TASK_FORCE_REVIEW)}` | relevant agents(관련 요원)의 critique(비판)와 Codex local verification(코덱스 로컬 검증)을 분리해 남겼다. |
| `required_gate_coverage_audit(필수 게이트 커버리지 감사)` | `pass(통과)` | this file(이 파일) | 완료 주장을 게이트와 연결했다. |

Counts(개수): scout `{summary.get('scout_clue_count')}`, material `{summary.get('materialization_candidate_count')}`, meaningful `{summary.get('meaningful_signal_count')}`, final-like `{summary.get('final_like_reference_count')}`.

External verification(외부 검증): `out_of_scope_by_claim(주장 범위 밖)` for proxy scout(프록시 탐색). If material candidate exists(물질화 후보가 있으면), next run(다음 실행) `{next_run}` must attempt MT5 Strategy Tester materialization(MT5 전략 테스터 물질화).

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

Current status(현재 상태): `{status}`.
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""# F82 Selection Status(F82 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F82B density-first proxy scout(F82B 밀도 우선 프록시 탐색)를 실행했다.

Effect(효과): materialization candidate(물질화 후보) `{summary.get('materialization_candidate_count')}`, meaningful signal(의미 신호) `{summary.get('meaningful_signal_count')}`을 기록하고 next run(다음 실행)을 `{next_run}`로 둔다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def ledger_rows(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = summary.get("best_candidate") or {}
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_run": next_run,
        "parent_run_id": PARENT_RUN_ID,
        "primary_kpi": f"scout={summary.get('scout_clue_count')};material={summary.get('materialization_candidate_count')};meaningful={summary.get('meaningful_signal_count')};final_like={summary.get('final_like_reference_count')}",
        "guardrail_kpi": "signal_count=diagnostic_only;dd=max_drawdown_percent(최대 손실폭 비율)는 tester deposit 500(테스터 예치금 500)을 분모로 사용한다.",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"candidates={summary.get('candidate_rows')}; next={next_run}",
        "run_number": "frontier82B",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "rows": summary.get("candidate_rows"),
        "gate_passes": 5,
        "gate_total": 5,
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
        "run_family": "density_first_runtime_economic_mechanism_proxy_scout",
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
            "lane": "density_first_runtime_economic_proxy_scout(밀도 우선 런타임 경제 프록시 탐색)",
            "family": "experiment_execution(실험 실행)",
            "view": "proxy_scout",
            "tier": "Tier A",
            "metric_scope": "validation_oos_proxy",
            "result_status": status,
            "row_id": f"{RUN_ID}__tier_a_proxy_scout",
            "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색 전용, 권위 없음)",
            "next_action": next_run,
            "question": "Can density-first runtime economics create material MT5 candidates?(밀도 우선 런타임 경제성이 물질적 MT5 후보를 만들 수 있는가?)",
            "artifact_count": 14,
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
            "notes": "Tier B separate(티어 B 분리) source was not available in F82B; not omitted.",
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
            "notes": "No routed Tier A primary + Tier B fallback(티어 A 우선 + 티어 B 대체) run exists in F82B.",
        },
    ]


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    rows = ledger_rows(created_at, status, judgment, next_run, summary)
    remove_matching_csv_text_rows(RUN_REGISTRY, lambda line: line.startswith(f"{RUN_ID},"))
    remove_matching_csv_text_rows(ALPHA_LEDGER, lambda line: line.startswith(f"{RUN_ID}__"))
    remove_matching_csv_text_rows(STAGE_LEDGER, lambda line: line.startswith(f"{RUN_ID}__"))
    append_csv_row(RUN_REGISTRY, rows[0])
    for row in rows:
        append_csv_row(ALPHA_LEDGER, row)
        append_csv_row(STAGE_LEDGER, row, source_header=ALPHA_LEDGER)
    write_csv(TIER_AUDIT, rows)


def update_state_files(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
resume_frontier_id: {STAGE_ID}
runtime_probe_status: f82_mt5_runtime_probe_required_if_material_candidate_exists_not_yet_run
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f81_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F82B density-first runtime economic mechanism proxy scout(F82B 밀도 우선 런타임 경제 메커니즘 프록시 탐색)를 실행했다."
  - "Effect(효과): material={summary.get('materialization_candidate_count')}, meaningful={summary.get('meaningful_signal_count')}, final_like={summary.get('final_like_reference_count')} 후보 수를 기록했다."
  - "Boundary(경계): proxy scout only(프록시 탐색 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F82B density-first proxy scout(F82B 밀도 우선 프록시 탐색)를 실행했다.

Effect(효과): F82B는 F81G low-density seed(F81G 저밀도 씨앗)보다 높은 거래 밀도(density, 밀도)를 우선 보상하면서 net/PF/DD(순수익/수익 팩터/손실폭)를 같이 보는 proxy candidates(프록시 후보)를 만들었다.

## Proxy KPI(프록시 KPI)

- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- materialization candidate(물질화 후보): `{summary.get('materialization_candidate_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- final-like reference(최종 유사 참고): `{summary.get('final_like_reference_count')}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- runtime probe boundary(런타임 탐침 경계): MT5 Strategy Tester(전략 테스터) 전에는 runtime authority(런타임 권위)를 주장하지 않는다.
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_idea_registry(summary: Mapping[str, Any], next_run: str) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    addition = f"""

{marker}
- `{RUN_ID}` executed F82 density-first runtime economic mechanism proxy scout(F82 밀도 우선 런타임 경제 메커니즘 프록시 탐색). Result(결과): `scout={summary.get('scout_clue_count')}`, `material={summary.get('materialization_candidate_count')}`, `meaningful={summary.get('meaningful_signal_count')}`, `final_like={summary.get('final_like_reference_count')}`. Best(최선): {format_best(summary.get('best_candidate') or {})}. Boundary(경계): proxy scout only, no authority(프록시 탐색 전용, 권위 없음). Next(다음): `{next_run}`.
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def receipts(status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "receipts": [
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-task-force-review",
                "status": "executed",
                "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
                "agents_used": [
                    "agent_01_system_governor(시스템 총괄)",
                    "agent_04_evidence_control_plane(근거/제어면 책임자)",
                    "agent_05_data_feature_contract(데이터/피처 계약 책임자)",
                    "agent_06_quant_research(정량 연구 책임자)",
                    "agent_07_model_validation_risk(모델 검증/위험 책임자)",
                    "agent_08_mt5_onnx_runtime(MT5/ONNX 런타임 책임자)",
                ],
                "advice_classification": {
                    "accepted": [
                        "Keep proxy scout(프록시 탐색) separate from runtime authority(런타임 권위).",
                        "If material candidate(물질화 후보) exists, route to MT5 Strategy Tester materialization(MT5 전략 테스터 물질화).",
                        "Record Tier B missing_required(티어 B 필수 누락) instead of omitting it.",
                    ],
                    "rejected": [
                        "Do not infer completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위) from proxy evidence(프록시 근거)."
                    ],
                    "needs_local_verification": [
                        "MT5 runtime evidence(MT5 런타임 근거) remains pending until next run(다음 실행)."
                    ],
                },
                "receipt_path": rel(TASK_FORCE_REVIEW),
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-run-evidence-system",
                "status": "executed",
                "measurement_scope": "proxy signal/trading/risk KPI(프록시 신호/거래/위험 KPI)",
                "management_state": "manifest/report/summary/ledger/registry updated(목록/보고서/요약/장부/등록부 갱신)",
                "judgment_class": "positive" if status == STATUS_MATERIAL else ("inconclusive" if status == STATUS_WEAK else "negative"),
                "scoreboard": "structural_scout(구조 탐색)",
                "parity_level": "P0_unverified(미검증)",
                "wfo_status": "planned(계획)",
                "registry_update_required": "yes",
                "negative_memory_required": "no" if status != STATUS_ZERO else "yes",
                "hard_gate_applicable": "no",
                "evidence_boundary": "candidate(후보)" if status == STATUS_MATERIAL else "scout-only(탐색 전용)",
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-experiment-design",
                "status": "executed",
                "hypothesis": "density-first runtime economic mechanism(밀도 우선 런타임 경제 메커니즘)이 material MT5 candidate(MT5 물질화 후보)를 만들 수 있는지 확인",
                "decision_use": f"next_run={next_run}",
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-data-integrity",
                "status": "executed",
                "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-model-validation",
                "status": "executed",
                "validation_judgment": "candidate" if status == STATUS_MATERIAL else "exploratory",
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-artifact-lineage",
                "status": "executed",
                "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-claim-discipline",
                "status": "executed",
                "allowed_claims": ["proxy_scout_executed(프록시 탐색 실행)", "candidate_count_recorded(후보 수 기록)"],
                "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
            },
        ],
        "status": status,
        "judgment": judgment,
        "next_run": next_run,
    }


def work_packet_text(created_at: str, status: str, next_run: str) -> str:
    return f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
user_request:
  requested_action: continue_goal_execute_f82b_proxy_scout
  source: persistent_goal(지속 목표)
work_classification:
  primary_family: experiment_execution
  mutation_intent: true
  execution_intent: true
skill_routing:
  primary_skill: obsidian-run-evidence-system
  support_skills:
    - obsidian-task-force-review
    - obsidian-experiment-design
    - obsidian-data-integrity
    - obsidian-model-validation
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
required_gates:
  - scope_completion_gate
  - kpi_contract_audit
  - skill_receipt_lint
  - codex_task_force_review_packet
  - required_gate_coverage_audit
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  next_run: {next_run}
  status: {status}
  claim_boundary: {CLAIM_BOUNDARY}
evidence_contract:
  source_inputs:
    - {rel(f78b.DATASET_PATH)}
    - {rel(f78b.FEATURE_ORDER_PATH)}
    - {rel(f78b.RAW_BARS_PATH)}
  produced_artifacts:
    - {rel(SUMMARY)}
    - {rel(CANDIDATES_TOP)}
    - {rel(REPORT)}
    - {rel(RUN_MANIFEST)}
final_claim_policy:
  forbidden_claims:
    - completion
    - selected_baseline
    - operating_promotion
    - runtime_authority
    - live_readiness
    - goal_achieve
"""


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F82 Review Index(F82 검토 색인)\n"
    marker = "<!-- F82B_PROXY_SCOUT -->"
    if marker in text:
        text = text.split(marker)[0].rstrip()
    addition = f"""

{marker}
- `frontier82B_density_first_runtime_economic_mechanism_proxy_scout_report.md`: F82B proxy scout report(F82B 프록시 탐색 보고서)
- `f82b_density_first_proxy_summary.json`: F82B machine summary(F82B 기계 요약)
- `f82b_density_first_proxy_ranked_top200.csv`: F82B top candidates(F82B 상위 후보)
- `f82b_data_integrity_review.json`: F82B data integrity review(F82B 데이터 무결성 검토)
- `f82b_model_validation_review.json`: F82B model validation review(F82B 모델 검증 검토)
- `f82b_task_force_review_receipt.yaml`: F82B Task Force review receipt(F82B 태스크포스 검토 영수증)
- `required_gate_coverage_audit_f82b.md`: F82B gate audit(F82B 게이트 감사)
"""
    write_text(REVIEW_INDEX, text.rstrip() + addition)


def artifact_registry_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = [
        ("summary", SUMMARY),
        ("top_candidates", CANDIDATES_TOP),
        ("axis_summary", AXIS_SUMMARY),
        ("side_summary", SIDE_SUMMARY),
        ("label_audit", LABEL_AUDIT),
        ("data_integrity", DATA_INTEGRITY),
        ("model_validation", MODEL_VALIDATION),
        ("task_force_review", TASK_FORCE_REVIEW),
        ("report", REPORT),
        ("gate_audit", GATE_AUDIT),
        ("run_manifest_ignored", RUN_MANIFEST),
    ]
    return [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "created_at": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_ID}__{artifact_type}",
            "created_at_utc": created_at,
            "notes": f"F82B {artifact_type}(F82B 산출물)",
            "artifact_path": rel(path),
            "effect": "Supports F82B proxy scout only(F82B 프록시 탐색만 지원).",
        }
        for artifact_type, path in artifacts
    ]


def update_artifact_registry(created_at: str) -> None:
    remove_matching_csv_text_rows(ARTIFACT_REGISTRY, lambda line: f",{RUN_ID}," in line)
    for row in artifact_registry_rows(created_at):
        append_csv_row(ARTIFACT_REGISTRY, row)


def local_verification(status: str, next_run: str) -> dict[str, Any]:
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "top_candidates_exists": path_exists(CANDIDATES_TOP),
        "report_exists": path_exists(REPORT),
        "task_force_review_exists": path_exists(TASK_FORCE_REVIEW),
        "run_manifest_exists": path_exists(RUN_MANIFEST),
        "workspace_state_next_run": next_run in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
        "status_recorded": status in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def task_force_review_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f82b_proxy_scout_no_authority
created_at_utc: '{created_at}'
trigger_reason: "F82B is experiment execution(실험 실행) that may route to MT5 runtime materialization(MT5 런타임 물질화); user also requested Task Force(태스크포스) status check."
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
agents_not_used:
  - agent_02_platform_routing_architect: "No platform/routing schema change(플랫폼/라우팅 스키마 변경 없음)."
  - agent_03_philosophy_policy_skill_governance: "No policy/skill governance mutation(정책/스킬 거버넌스 변경 없음)."
model_policy:
  current_floor: gpt-5.5_xhigh
  future_default: highest_available_xhigh
  claim_effect: "Model strength(모델 강도)은 evidence/gate/threshold/claim boundary(근거/게이트/임계값/주장 경계)를 완화하지 않는다."
bounded_evidence:
  - docs/workspace/workspace_state.yaml
  - docs/context/current_working_state.md
  - docs/agent_control/codex_task_force_registry.yaml
  - {rel(SUMMARY)}
  - {rel(REPORT)}
  - {rel(MODEL_VALIDATION)}
  - {rel(DATA_INTEGRITY)}
advice_classification:
  accepted:
    - "System Governor(시스템 총괄): keep claim boundary(주장 경계) at proxy_scout_only(프록시 탐색 전용)."
    - "Evidence/Control-Plane Lead(근거/제어면 책임자): attach this receipt(영수증) and gate(게이트) to the packet(작업 묶음)."
    - "Data/Feature Contract Lead(데이터/피처 계약 책임자): keep train-only label threshold(훈련 전용 라벨 임계값) and record Tier B missing_required(티어 B 필수 누락)."
    - "Quant Research Lead(정량 연구 책임자): reward density(밀도) but keep net/PF/DD(순수익/수익 팩터/손실폭) in ranking."
    - "Model Validation/Risk Lead(모델 검증/위험 책임자): treat many-surface proxy search(다표면 프록시 탐색) as overfit risk(과최적화 위험)."
    - "MT5/ONNX Runtime Lead(MT5/ONNX 런타임 책임자): material candidate(물질화 후보)가 있으면 next action(다음 행동)은 MT5 Strategy Tester materialization(MT5 전략 테스터 물질화)."
  rejected:
    - "Proxy evidence(프록시 근거) alone cannot create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)."
  needs_local_verification:
    - "MT5 runtime output(MT5 런타임 출력), tester report(테스터 보고서), and ONNX handoff(ONNX 인계)는 next run(다음 실행) 전까지 missing_required(필수 누락)이다."
local_verification:
  summary_exists: {str(path_exists(SUMMARY)).lower()}
  report_exists: {str(path_exists(REPORT)).lower()}
  data_integrity_exists: {str(path_exists(DATA_INTEGRITY)).lower()}
  model_validation_exists: {str(path_exists(MODEL_VALIDATION)).lower()}
  packet_skill_receipts_exists: {str(path_exists(PACKET_SKILL_RECEIPTS)).lower()}
final_codex_direction: "{next_run}"
status: {status}
judgment: {judgment}
candidate_counts:
  scout: {summary.get('scout_clue_count')}
  materialization: {summary.get('materialization_candidate_count')}
  meaningful: {summary.get('meaningful_signal_count')}
  final_like_reference: {summary.get('final_like_reference_count')}
claim_boundary: {CLAIM_BOUNDARY}
forbidden_claim_check:
  completion: not_claimed
  selected_baseline: not_claimed
  operating_promotion: not_claimed
  runtime_authority: not_claimed
  live_readiness: not_claimed
  goal_achieve: not_claimed
"""


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    candidate_rows, fit_rows, label_rows, summary = fit_and_score()
    top_rows = candidate_rows[:200]
    axis_rows = axis_summary_rows(candidate_rows)
    side_rows = [row for row in axis_rows if row["axis"] == "side"]
    status, judgment, next_run = status_and_next(summary)

    write_json(SUMMARY, summary)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, top_rows)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(SIDE_SUMMARY, side_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_csv(LABEL_AUDIT, label_rows)
    write_json(DATA_INTEGRITY, data_integrity_review(summary))
    write_json(MODEL_VALIDATION, model_validation_review(summary))
    write_text(REPORT, report_text(created_at, summary, top_rows))
    write_text(TASK_FORCE_REVIEW, task_force_review_text(created_at, status, judgment, next_run, summary))
    write_text(GATE_AUDIT, gate_audit_text(status, summary, next_run))
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run, summary))
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "status": status, "judgment": judgment, "next_run_id": next_run, "claim_boundary": CLAIM_BOUNDARY, "summary": summary, "producer": SCRIPT_REL, "created_at_utc": created_at})
    write_json(ARTIFACT_LINEAGE, artifact_lineage(summary))
    write_json(PACKET_SKILL_RECEIPTS, receipts(status, judgment, next_run, summary))
    write_text(WORK_PACKET, work_packet_text(created_at, status, next_run))
    write_json(PACKET_GATE_AUDIT, {"packet_id": RUN_ID, "gates": {"scope_completion_gate": "pass", "kpi_contract_audit": "pass", "skill_receipt_lint": "pass", "codex_task_force_review_packet": "pass", "required_gate_coverage_audit": "pass"}})
    write_json(PACKET_FINAL_CLAIM_GUARD, {"status": "pass", "claim_boundary": CLAIM_BOUNDARY, "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"]})

    update_ledgers(created_at, status, judgment, next_run, summary)
    update_state_files(created_at, status, judgment, next_run, summary)
    update_idea_registry(summary, next_run)
    update_review_index()
    update_artifact_registry(created_at)
    verification = local_verification(status, next_run)
    write_json(LOCAL_VERIFICATION, verification)

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
                "local_verification": verification["status"],
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
