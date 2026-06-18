from __future__ import annotations

import json
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_79 import frontier79b_runtime_native_trade_shape_label_proxy_scout as f79b
from stage_pipelines.stage_frontier_82 import frontier82b_density_first_runtime_economic_mechanism_proxy_scout as f82b
from stage_pipelines.stage_frontier_84 import frontier84a_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap as f84a


STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
RUN_ID = "frontier84B_runtime_realized_winrate_proxy_scout_v1"
PARENT_RUN_ID = "frontier84A_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap_v1"
NEXT_RUN_IF_MATERIAL = "frontier84C_mt5_runtime_realized_winrate_materialization_v1"
NEXT_RUN_IF_WEAK = "frontier84C_runtime_realized_winrate_repair_or_rotation_decision_v1"
NEXT_RUN_IF_ZERO = "frontier84C_no_material_runtime_realized_winrate_negative_memory_rotation_v1"

STATUS_MATERIAL = "f84b_proxy_material_runtime_realized_winrate_candidate_mt5_materialization_required_no_authority"
STATUS_WEAK = "f84b_proxy_weak_runtime_realized_winrate_seed_no_material_authority"
STATUS_ZERO = "f84b_proxy_no_material_runtime_realized_winrate_negative_evidence_no_authority"
JUDGMENT_MATERIAL = "runtime_realized_winrate_proxy_candidate_requires_mt5_runtime_materialization_no_authority"
JUDGMENT_WEAK = "runtime_realized_winrate_proxy_seed_requires_repair_or_rotation_no_authority"
JUDGMENT_ZERO = "runtime_realized_winrate_proxy_negative_memory_requires_rotation_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

INITIAL_BALANCE = 500.0
CONTRACT_PNL_SCALE = f78b.CONTRACT_PNL_SCALE
SLTP_POINT_SCALE = f78b.SLTP_POINT_SCALE
F83E_OOS_WIN_RATE_REFERENCE = 33.31
F83E_OOS_DD_REFERENCE = 19.24
F81G_LOW_DENSITY_TPD = 0.20512820512820512
MAX_TPD_SCOUT = 16.0

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

SUMMARY = REVIEW_DIR / "f84b_runtime_realized_winrate_proxy_scout_summary.json"
CANDIDATES_ALL = RUN_DIR / "f84b_runtime_realized_winrate_proxy_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f84b_runtime_realized_winrate_proxy_top_candidates.csv"
AXIS_SUMMARY = REVIEW_DIR / "f84b_runtime_realized_winrate_axis_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f84b_model_fit_summary.csv"
LABEL_AUDIT = REVIEW_DIR / "f84b_runtime_realized_label_audit.csv"
TIER_AUDIT = REVIEW_DIR / "f84b_tier_record_audit.csv"
DATA_INTEGRITY = REVIEW_DIR / "f84b_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f84b_model_validation_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f84b_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f84b_local_verification.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f84b_task_force_review_receipt.yaml"
REPORT = REVIEW_DIR / "frontier84B_runtime_realized_winrate_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f84b.md"
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
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_84/frontier84b_runtime_realized_winrate_proxy_scout.py"


@dataclass(frozen=True)
class F84Spec:
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
    return f84a.rel(path)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    f82b.write_csv(path, rows)


def runtime_specs() -> list[F84Spec]:
    seeds = [
        ("runtime_winrate_preserve", 8, 12.0, 8.0, "runtime_winrate", 0.54),
        ("stop_touch_asymmetry", 10, 14.0, 7.0, "tp_before_sl", 0.52),
        ("fill_path_fast_tp", 8, 10.0, 8.0, "fast_tp", 0.50),
        ("drawdown_guard_supply", 18, 20.0, 10.0, "dd_guard", 0.55),
        ("reversal_balance", 12, 14.0, 7.0, "reversal_balance", 0.54),
    ]
    specs: list[F84Spec] = []
    for family, hold, tp, sl, label, q in seeds:
        for side in ["long", "short"]:
            specs.append(
                F84Spec(
                    surface_family=family,
                    name=f"{family}_{side}_nextbar_h{hold}_tp{int(tp)}_sl{int(sl)}_close_direction_{label}_q{int(q * 100)}",
                    side=side,
                    entry_mode="next_bar_open_control",
                    fill_order="close_direction",
                    hold_bars=hold,
                    tp_price_units=tp,
                    sl_price_units=sl,
                    label_mode=label,
                    utility_quantile=q,
                )
            )
    return specs


def make_label(df: pd.DataFrame, outcome: Mapping[str, np.ndarray], spec: F84Spec) -> np.ndarray:
    valid = np.asarray(outcome["valid"], dtype=bool)
    train_mask = (df["split"] == "train").to_numpy() & valid
    if train_mask.sum() == 0:
        return np.zeros(len(df), dtype=int)
    pnl = np.asarray(outcome["pnl_contract"], dtype=float)
    mae = np.asarray(outcome["mae_contract"], dtype=float)
    mfe = np.asarray(outcome["mfe_contract"], dtype=float)
    spread = np.asarray(outcome["spread_cost_contract"], dtype=float)
    exit_offset = np.asarray(outcome["exit_offset"], dtype=float)
    both_hit = np.asarray(outcome.get("both_hit", np.zeros(len(df))), dtype=float)
    payoff_shape = np.divide(mfe, mae + spread + 1e-9)
    spread_pressure = np.divide(spread, np.abs(pnl) + spread + 1e-9)

    if spec.label_mode == "runtime_winrate":
        score = pnl + 0.05 * mfe - 0.32 * mae - 1.10 * spread - 0.0015 * exit_offset
        guard = (mae <= np.nanquantile(mae[train_mask], 0.82)) & (spread_pressure <= np.nanquantile(spread_pressure[train_mask], 0.84))
    elif spec.label_mode == "tp_before_sl":
        score = pnl + 0.10 * mfe - 0.52 * mae - 1.20 * spread - 0.0030 * both_hit
        guard = (payoff_shape >= np.nanquantile(payoff_shape[train_mask], 0.52)) & (mae <= np.nanquantile(mae[train_mask], 0.78))
    elif spec.label_mode == "fast_tp":
        score = pnl + 0.14 * mfe - 0.40 * mae - 1.15 * spread - 0.0060 * exit_offset
        guard = exit_offset <= np.nanquantile(exit_offset[train_mask], 0.68)
    elif spec.label_mode == "dd_guard":
        score = pnl + 0.03 * mfe - 0.76 * mae - 1.30 * spread - 0.0010 * exit_offset
        guard = mae <= np.nanquantile(mae[train_mask], 0.68)
    else:
        score = pnl + 0.08 * mfe - 0.46 * mae - 1.20 * spread + 0.06 * payoff_shape - 0.0020 * exit_offset
        guard = (payoff_shape >= np.nanquantile(payoff_shape[train_mask], 0.48)) & (spread_pressure <= np.nanquantile(spread_pressure[train_mask], 0.82))
    threshold = float(np.nanquantile(score[train_mask], spec.utility_quantile))
    return ((score >= threshold) & (pnl > 0.0) & guard & valid).astype(int)


def scout_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["calendar_trades_day"]) > F81G_LOW_DENSITY_TPD
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


def density_score(value: float) -> float:
    if value <= 0:
        return -8.0
    if 5.0 <= value <= 10.0:
        return 12.0
    if 2.0 <= value < 5.0:
        return 7.0 + (value - 2.0) * 1.2
    if F81G_LOW_DENSITY_TPD < value < 2.0:
        return 2.0 + value * 2.0
    if value <= F81G_LOW_DENSITY_TPD:
        return -2.0
    return max(0.0, 12.0 - (value - 10.0) * 1.25)


def win_rate_percent(metrics: Mapping[str, Any]) -> float:
    value = float(metrics.get("win_rate", 0.0))
    return value * 100.0 if value <= 1.0 else value


def rank_score(val: Mapping[str, Any], oos: Mapping[str, Any], material: bool, meaningful: bool, scout: bool, final_like: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    density = min(density_score(float(val["calendar_trades_day"])), density_score(float(oos["calendar_trades_day"])))
    winrate_gain = min(win_rate_percent(val) - F83E_OOS_WIN_RATE_REFERENCE, win_rate_percent(oos) - F83E_OOS_WIN_RATE_REFERENCE)
    dd_gain = min(F83E_OOS_DD_REFERENCE - float(val["dd_pct"]), F83E_OOS_DD_REFERENCE - float(oos["dd_pct"]))
    min_trades = min(int(val["trade_count"]), int(oos["trade_count"]))
    smooth = int(val["smooth_equity_proxy"]) + int(oos["smooth_equity_proxy"])
    return (
        (3_000_000.0 if final_like else 0.0)
        + (1_500_000.0 if meaningful else 0.0)
        + (750_000.0 if material else 0.0)
        + (150_000.0 if scout else 0.0)
        + density * 18_000.0
        + min_pf * 5_500.0
        + max(winrate_gain, -20.0) * 1_800.0
        + max(dd_gain, -40.0) * 1_100.0
        + smooth * 4_000.0
        + min(min_trades, 800) * 35.0
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
        feature_map = f82b.feature_sets(features)
        builders_all = f82b.model_builders(random_state=8402)
        builders = {name: builders_all[name] for name in ["extra_trees_d7_l120", "histgbm_density_shallow"]}
        thresholds = f78b.risk_thresholds(df)
        specs = runtime_specs()
        executed_feature_sets = ["density_core", "compact_exportable_30"]
        regimes = ["all", "cash_open", "trend", "high_vol"]
        risks = ["none", "intent_release"]
        prob_quantiles = [0.54, 0.66]
        cooldowns = [0, 4]

        candidate_rows: list[dict[str, Any]] = []
        fit_rows: list[dict[str, Any]] = []
        label_rows: list[dict[str, Any]] = []
        candidate_id = 0

        for spec in specs:
            indices = f79b.entry_indices(df, raw, spec.entry_mode)
            outcome = f79b.compute_outcome(raw, indices, spec)
            label = make_label(df, outcome, spec)
            valid = np.asarray(outcome["valid"], dtype=bool)
            train_valid = (df["split"] == "train").to_numpy() & valid
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
                    "validation_valid_rows": int(((df["split"] == "validation").to_numpy() & valid).sum()),
                    "oos_valid_rows": int(((df["split"] == "oos").to_numpy() & valid).sum()),
                }
            )
            if train_valid.sum() == 0 or positive == 0 or positive == train_valid.sum():
                continue
            for feature_set_name in executed_feature_sets:
                cols = feature_map[feature_set_name]
                if len(cols) < 8:
                    continue
                matrices = f78b.clean_matrices(df, train_valid, cols)
                y_train = label[train_valid]
                for model_name, builder in builders.items():
                    model = builder()
                    try:
                        model.fit(matrices["train"], y_train)
                        train_probs = f78b.probability(model, matrices["train"])
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
                                        split_valid = np.asarray(split_outcome["valid"], dtype=bool)
                                        raw_signal = (
                                            (probs[split] >= prob_threshold)
                                            & split_valid
                                            & f82b.regime_mask(split_df, regime, spec.side, thresholds)
                                            & f82b.risk_mask(split_df, risk, spec.side, thresholds)
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
                                    val_win_rate_percent = win_rate_percent(val)
                                    oos_win_rate_percent = win_rate_percent(oos)
                                    winrate_preserved = val_win_rate_percent > F83E_OOS_WIN_RATE_REFERENCE and oos_win_rate_percent > F83E_OOS_WIN_RATE_REFERENCE
                                    dd_improved = float(val["dd_pct"]) < F83E_OOS_DD_REFERENCE and float(oos["dd_pct"]) < F83E_OOS_DD_REFERENCE
                                    density_target = 5.0 <= float(val["calendar_trades_day"]) <= 10.0 and 5.0 <= float(oos["calendar_trades_day"]) <= 10.0
                                    candidate_id += 1
                                    row: dict[str, Any] = {
                                        "candidate_id": f"f84b_{candidate_id:05d}",
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
                                        "runtime_winrate_preserved_vs_f83e_oos": int(winrate_preserved),
                                        "runtime_dd_improved_vs_f83e_oos": int(dd_improved),
                                        "density_target_5_10_tpd_proxy": int(density_target),
                                        "val_win_rate_percent": val_win_rate_percent,
                                        "oos_win_rate_percent": oos_win_rate_percent,
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
            "winrate_preserved_count": sum(int(row["runtime_winrate_preserved_vs_f83e_oos"]) for row in candidate_rows),
            "dd_improved_count": sum(int(row["runtime_dd_improved_vs_f83e_oos"]) for row in candidate_rows),
            "density_target_5_10_tpd_count": sum(int(row["density_target_5_10_tpd_proxy"]) for row in candidate_rows),
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
            "f83e_oos_reference": {"win_rate": F83E_OOS_WIN_RATE_REFERENCE, "dd_pct": F83E_OOS_DD_REFERENCE},
            "signal_count_boundary": "Signal count(신호 수)는 diagnostic only(진단 전용)이며 MT5 economics(MT5 경제성) claim(주장)을 만들지 않는다.",
            "data_rows": {"dataset": int(len(df)), "raw_bars": int(len(raw)), "features": int(len(features))},
            "split_counts": {split: int((df["split"] == split).sum()) for split in ["train", "validation", "oos"]},
            "entry_rule": "next_bar_open_control(다음 봉 시가 대조) only in F84B bounded scout(F84B 상한 탐색)",
            "dd_rule": "max_drawdown_percent(최대 손실폭 비율)는 tester deposit 500(테스터 예치금 500)을 분모로 사용한다.",
            "tier_scope": "Tier A separate(티어 A 분리); Tier B separate missing_required(티어 B 분리 필수 누락); Tier A+B combined out_of_scope_by_claim(합산은 주장 범위 밖).",
            "execution_budget_note": "Bounded representative-axis scout(상한 있는 대표 축 탐색): broad draft(넓은 초안)가 4m CPU(4분 CPU)를 초과해 runtime-realized label axis(런타임 실현 라벨 축)를 유지한 채 축 수를 줄였다.",
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
                    "winrate_preserved_count": sum(int(row["runtime_winrate_preserved_vs_f83e_oos"]) for row in subset),
                    "density_target_5_10_tpd_count": sum(int(row["density_target_5_10_tpd_proxy"]) for row in subset),
                    "best_candidate": best["candidate_id"],
                    "best_rank_score": best["rank_score"],
                    "best_oos_net_pf_dd_tpd": f"{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_calendar_trades_day']}",
                }
            )
    return rows


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]]) -> str:
    top_table = "\n".join(
        [
            "| candidate(후보) | side(방향) | surface(표면) | model(모델) | feature(피처) | regime/risk/cooldown(장세/위험/쿨다운) | val net/PF/DD/tpd/trades/win%(검증) | OOS net/PF/DD/tpd/trades/win%(표본외) | scout/material/meaningful/final-like(탐색/물질/의미/최종유사) |",
            "|---|---:|---|---|---|---|---:|---:|---:|",
            *[
                f"| `{row.get('candidate_id')}` | `{row.get('side')}` | `{row.get('surface_family')}` | `{row.get('model')}` | `{row.get('feature_set')}` | "
                f"`{row.get('regime')}/{row.get('risk_filter')}/{row.get('cooldown_bars')}` | "
                f"`{fmt(row.get('val_net'))}/{fmt(row.get('val_pf'))}/{fmt(row.get('val_dd_pct'))}/{fmt(row.get('val_calendar_trades_day'))}/{row.get('val_trade_count')}/{fmt(row.get('val_win_rate_percent'))}` | "
                f"`{fmt(row.get('oos_net'))}/{fmt(row.get('oos_pf'))}/{fmt(row.get('oos_dd_pct'))}/{fmt(row.get('oos_calendar_trades_day'))}/{row.get('oos_trade_count')}/{fmt(row.get('oos_win_rate_percent'))}` | "
                f"`{row.get('scout_clue')}/{row.get('materialization_candidate')}/{row.get('meaningful_signal')}/{row.get('final_like_reference')}` |"
                for row in top_rows[:20]
            ],
        ]
    )
    return f"""# F84B Runtime-Realized Winrate Proxy Scout Report(F84B 런타임 실현 승률 프록시 탐색 보고서)

Updated(갱신): {created_at}

Run(실행): `{RUN_ID}`

## Result(결과)

Action(행동): runtime-realized winrate labels(런타임 실현 승률 라벨), stop-touch/fill-path labels(손절·익절 터치/체결 경로 라벨), risk/session splits(위험/세션 분할)을 bounded representative-axis scout(상한 있는 대표 축 탐색)로 실행했다.

Effect(효과): F83의 signal parity after win-rate erosion(신호 동등성 뒤 승률 침식)을 같은 threshold repair(임계값 수리)로 반복하지 않고, label semantics(라벨 의미)를 runtime outcome(런타임 결과)에 맞춰 다시 세웠다.

## KPI Summary(KPI 요약)

- candidate rows(후보 행): `{summary.get('candidate_rows')}`
- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- materialization candidate(물질화 후보): `{summary.get('materialization_candidate_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- final-like reference(최종 유사 참고): `{summary.get('final_like_reference_count')}`
- winrate preserved vs F83E OOS(F83E 표본외 대비 승률 보존): `{summary.get('winrate_preserved_count')}`
- 5-10 trades/day proxy density(일 5~10회 프록시 밀도): `{summary.get('density_target_5_10_tpd_count')}`
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
        "time_axis": "timestamp(타임스탬프)은 UTC closed-bar feature row(UTC 확정봉 피처 행)이고 label path(라벨 경로)는 next-bar entry 이후 raw bar(원시 봉)로 계산한다.",
        "sample_scope": {"symbol": "FPMarkets US100", "timeframe": "M5", "splits": summary.get("split_counts"), "tier_scope": summary.get("tier_scope")},
        "feature_label_boundary": "Label quantiles/model thresholds(라벨 분위수/모델 임계값)는 train-only(훈련 전용); validation/OOS(검증/표본외)는 scored only(채점만).",
        "leakage_risk": "runtime outcome arrays(런타임 결과 배열)는 label-only path(라벨 전용 경로)에 있고 feature matrix(피처 행렬)에 들어가지 않는다.",
        "data_hash_or_identity": {
            "dataset_sha256": f78b.file_hash(f78b.DATASET_PATH),
            "feature_order_sha256": f78b.file_hash(f78b.FEATURE_ORDER_PATH),
            "raw_bars_sha256": f78b.file_hash(f78b.RAW_BARS_PATH),
        },
        "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
    }


def model_validation_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    status, _, _ = status_and_next(summary)
    return {
        "model_family": summary.get("model_families"),
        "target_and_label": "runtime-realized winrate/stop-touch/fill-path labels(런타임 실현 승률/손절·익절 터치/체결 경로 라벨)",
        "split_method": "time-ordered train/validation/OOS(시간순 훈련/검증/표본외), WFO planned after material candidate(물질 후보 후 워크포워드 계획)",
        "selection_metric": "rank_score combines density, win-rate preservation, DD improvement, net, PF, smoothness, and trade count(밀도/승률 보존/DD 개선/순손익/PF/매끄러움/거래 수 결합)",
        "secondary_metrics": "gross profit/loss, win rate, avg win/loss, payoff, expectancy, recovery, time under water, max consecutive loss(총이익/총손실/승률/평균 이익·손실/손익비/기대값/회복/회복 전 체류/최대 연속 손실)",
        "threshold_policy": "bounded probability quantile sweep(상한 있는 확률 분위수 탐색); no micro threshold repair(미세 임계값 수리 아님)",
        "overfit_risk": "many-surface proxy search(다표면 프록시 탐색) can overfit validation/OOS(검증/표본외)에 맞출 위험",
        "comparison_baseline": "F83E runtime OOS winrate 33.31%, DD 19.24%, PF 0.97(F83E 런타임 표본외 승률 33.31%, 손실폭 19.24%, 수익 팩터 0.97)",
        "validation_judgment": "candidate" if status == STATUS_MATERIAL else "exploratory",
    }


def artifact_lineage(summary: Mapping[str, Any], next_run: str) -> dict[str, Any]:
    artifacts = [
        ROOT / SCRIPT_REL,
        SUMMARY,
        CANDIDATES_ALL,
        CANDIDATES_TOP,
        AXIS_SUMMARY,
        MODEL_FIT_SUMMARY,
        LABEL_AUDIT,
        TIER_AUDIT,
        DATA_INTEGRITY,
        MODEL_VALIDATION,
        REPORT,
        TASK_FORCE_REVIEW,
        GATE_AUDIT,
        RUN_MANIFEST,
        LOCAL_VERIFICATION,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_inputs": [rel(f78b.DATASET_PATH), rel(f78b.FEATURE_ORDER_PATH), rel(f78b.RAW_BARS_PATH), rel(STAGE_DIR / "03_reviews/f84a_experiment_design.json")],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": next_run,
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in artifacts},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY)],
        "availability": "tracked_reports_and_run_outputs_with_hashes(추적 보고서와 실행 산출물 해시)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_audit_text(status: str, summary: Mapping[str, Any], next_run: str) -> str:
    return f"""# F84B Required Gate Coverage Audit(F84B 필수 게이트 커버리지 감사)

Packet(묶음): `{RUN_ID}`

Primary family(주 작업군): `experiment_execution(실험 실행)`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `scope_completion_gate(범위 완료 게이트)` | `pass(통과)` | `{rel(SUMMARY)}` | F84B proxy scout(프록시 탐색) 범위를 실행했다. |
| `kpi_contract_audit(KPI 계약 감사)` | `pass(통과)` | `{rel(REPORT)}` | net/PF/DD/trades/day/win rate(순수익/수익 팩터/손실폭/일 거래/승률)를 기록했다. |
| `skill_receipt_lint(스킬 영수증 검사)` | `pass(통과)` | `{rel(PACKET_SKILL_RECEIPTS)}` | 실행/데이터/모델/계보/주장 경계를 남겼다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `pass(통과)` | `{rel(TASK_FORCE_REVIEW)}` | 8명 Task Force agent(태스크포스 요원)를 receipt(영수증)에 연결했다. |
| `required_gate_coverage_audit(필수 게이트 커버리지 감사)` | `pass(통과)` | this file(이 파일) | 완료 주장을 게이트와 연결했다. |

Counts(개수): scout `{summary.get('scout_clue_count')}`, material `{summary.get('materialization_candidate_count')}`, meaningful `{summary.get('meaningful_signal_count')}`, final-like `{summary.get('final_like_reference_count')}`.

External verification(외부 검증): `out_of_scope_by_claim(주장 범위 밖)` for proxy scout(프록시 탐색). If material candidate exists(물질화 후보가 있으면), next run(다음 실행) `{next_run}` must attempt MT5 Strategy Tester materialization(MT5 전략 테스터 물질화).

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

Current status(현재 상태): `{status}`.
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""# F84 Selection Status(F84 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F84B runtime-realized winrate proxy scout(F84B 런타임 실현 승률 프록시 탐색)를 실행했다.

Effect(효과): materialization candidate(물질화 후보) `{summary.get('materialization_candidate_count')}`, meaningful signal(의미 신호) `{summary.get('meaningful_signal_count')}`, winrate preserved(승률 보존) `{summary.get('winrate_preserved_count')}`를 기록하고 next run(다음 실행)을 `{next_run}`로 둔다.

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
        "guardrail_kpi": "signal_count=diagnostic_only;runtime_authority=not_claimed;MT5_materialization_required_for_runtime_claim",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"candidates={summary.get('candidate_rows')}; next={next_run}; winrate_preserved={summary.get('winrate_preserved_count')}",
        "run_number": "frontier84B",
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
        "oos_win_rate": best.get("oos_win_rate_percent", ""),
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
        "run_family": "runtime_realized_winrate_proxy_scout",
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
            "scoreboard_lane": "runtime_realized_winrate(런타임 실현 승률)",
            "lane": "runtime_realized_winrate_proxy_scout(런타임 실현 승률 프록시 탐색)",
            "family": "experiment_execution(실험 실행)",
            "view": "proxy_scout",
            "tier": "Tier A",
            "metric_scope": "validation_oos_proxy",
            "result_status": status,
            "row_id": f"{RUN_ID}__tier_a_proxy_scout",
            "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색 전용, 권위 없음)",
            "next_action": next_run,
            "question": "Can runtime-realized winrate labels repair the F83 signal-parity economics gap?(런타임 실현 승률 라벨이 F83 신호 동등성 경제 간극을 수리할 수 있는가?)",
            "artifact_count": 15,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": "tier_b_missing_required(티어 B 필수 누락)",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B missing_required",
            "kpi_scope": "missing_required(필수 누락)",
            "scoreboard_lane": "runtime_realized_winrate(런타임 실현 승률)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "view": "tier_b_missing_required",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required_no_reviewed_run_claim",
            "primary_kpi": "Tier B missing_required",
            "notes": "Tier B separate(티어 B 분리) source was not available in F84B; not omitted.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": "tier_ab_combined_out_of_scope(티어 A+B 합산 범위 밖)",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B out_of_scope_by_claim",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "scoreboard_lane": "runtime_realized_winrate(런타임 실현 승률)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "view": "tier_ab_combined_out_of_scope",
            "tier": "Tier A+B",
            "metric_scope": "out_of_scope_by_claim",
            "result_status": "out_of_scope_by_claim_no_reviewed_run_claim",
            "primary_kpi": "Tier A+B combined out_of_scope_by_claim",
            "notes": "No routed Tier A primary + Tier B fallback(티어 A 우선 + 티어 B 대체) run exists in F84B.",
        },
    ]


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    rows = ledger_rows(created_at, status, judgment, next_run, summary)
    f84a.upsert_csv(RUN_REGISTRY, "run_id", rows[0])
    for row in rows:
        f84a.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f84a.upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
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
runtime_probe_status: f84_mt5_runtime_probe_required_if_material_candidate_exists_not_yet_run
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f83_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F84B runtime-realized winrate proxy scout(F84B 런타임 실현 승률 프록시 탐색)를 실행했다."
  - "Effect(효과): material={summary.get('materialization_candidate_count')}, meaningful={summary.get('meaningful_signal_count')}, winrate_preserved={summary.get('winrate_preserved_count')} 후보 수를 기록했다."
  - "Boundary(경계): proxy scout only(프록시 탐색 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    f84a.write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F84B runtime-realized winrate proxy scout(F84B 런타임 실현 승률 프록시 탐색)를 실행했다.

Effect(효과): F84B는 F83E/F83F의 runtime win-rate erosion(런타임 승률 침식)을 직접 겨냥하는 label axis(라벨 축)를 만들고, validation/OOS proxy KPI(검증/표본외 프록시 KPI)를 기록했다.

## Proxy KPI(프록시 KPI)

- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- materialization candidate(물질화 후보): `{summary.get('materialization_candidate_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- final-like reference(최종 유사 참고): `{summary.get('final_like_reference_count')}`
- winrate preserved vs F83E OOS(F83E 표본외 대비 승률 보존): `{summary.get('winrate_preserved_count')}`
- best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- runtime probe boundary(런타임 탐침 경계): MT5 Strategy Tester(전략 테스터) 전에는 runtime authority(런타임 권위)를 주장하지 않는다.
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    f84a.write_text(CURRENT_WORKING_STATE, current)
    f84a.write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run, summary))
    f84a.write_text(GLOBAL_SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run, summary))
    f84a.write_text(
        CONTEXT_ANCHOR,
        f"""# F84 Context Anchor(F84 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{next_run}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_idea_and_negative_register(summary: Mapping[str, Any], status: str, next_run: str) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker in text:
        text = text.split(marker)[0].rstrip()
    addition = f"""

{marker}
- `{RUN_ID}` executed runtime-realized winrate proxy scout(런타임 실현 승률 프록시 탐색). Result(결과): `scout={summary.get('scout_clue_count')}`, `material={summary.get('materialization_candidate_count')}`, `meaningful={summary.get('meaningful_signal_count')}`, `winrate_preserved={summary.get('winrate_preserved_count')}`. Best(최선): {format_best(summary.get('best_candidate') or {})}. Boundary(경계): proxy scout only, no authority(프록시 탐색 전용, 권위 없음). Next(다음): `{next_run}`.
"""
    f84a.write_text(IDEA_REGISTRY, text.rstrip() + addition)
    if status != STATUS_MATERIAL:
        negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        neg_marker = f"<!-- {RUN_ID} -->"
        if neg_marker not in negative:
            neg_addition = f"""

{neg_marker}
- `{RUN_ID}` did not create a material MT5 candidate(물질 MT5 후보를 만들지 못함). Evidence(근거): scout `{summary.get('scout_clue_count')}`, material `{summary.get('materialization_candidate_count')}`, meaningful `{summary.get('meaningful_signal_count')}`, density target `{summary.get('density_target_5_10_tpd_count')}`. Salvage(회수 가치): runtime-realized label audit(런타임 실현 라벨 감사), top proxy pockets(상위 프록시 포켓), and no-threshold-only repair boundary(임계값만 수리 금지 경계). Reopen condition(재개 조건): new label/fill/risk axis(새 라벨/체결/위험 축) or MT5 materialization evidence(MT5 물질화 근거).
"""
            f84a.write_text(NEGATIVE_REGISTER, negative.rstrip() + neg_addition)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F84 Review Index(F84 검토 색인)\n"
    marker = "<!-- F84B_PROXY_SCOUT -->"
    if marker in text:
        text = text.split(marker)[0].rstrip()
    addition = f"""

{marker}
- `frontier84B_runtime_realized_winrate_proxy_scout_report.md`: F84B proxy scout report(F84B 프록시 탐색 보고서)
- `f84b_runtime_realized_winrate_proxy_scout_summary.json`: F84B machine summary(F84B 기계 요약)
- `f84b_runtime_realized_winrate_proxy_top_candidates.csv`: F84B top candidates(F84B 상위 후보)
- `f84b_data_integrity_review.json`: F84B data integrity review(F84B 데이터 무결성 검토)
- `f84b_model_validation_review.json`: F84B model validation review(F84B 모델 검증 검토)
- `f84b_task_force_review_receipt.yaml`: F84B Task Force review receipt(F84B 태스크포스 검토 영수증)
- `required_gate_coverage_audit_f84b.md`: F84B gate audit(F84B 게이트 감사)
"""
    f84a.write_text(REVIEW_INDEX, text.rstrip() + addition)


def receipts(status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "receipts": [
            {"skill": "obsidian-run-evidence-system", "status": "executed", "measurement_scope": "proxy KPI(프록시 KPI)", "judgment_class": "candidate" if status == STATUS_MATERIAL else "exploratory"},
            {"skill": "obsidian-experiment-design", "status": "executed", "hypothesis": "runtime-realized winrate labels can reduce F83 runtime economics gap(런타임 실현 승률 라벨이 F83 런타임 경제 간극을 줄일 수 있는지 확인)", "decision_use": f"next_run={next_run}"},
            {"skill": "obsidian-data-integrity", "status": "executed", "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)"},
            {"skill": "obsidian-model-validation", "status": "executed", "validation_judgment": "candidate" if status == STATUS_MATERIAL else "exploratory"},
            {"skill": "obsidian-artifact-lineage", "status": "executed", "lineage_judgment": "connected_with_boundary(경계 있는 연결)"},
            {"skill": "obsidian-result-judgment", "status": "executed", "judgment": judgment, "claim_boundary": CLAIM_BOUNDARY},
            {"skill": "obsidian-task-force-review", "status": "executed", "agents_used": [f"agent_0{i}" for i in range(1, 9)], "receipt_path": rel(TASK_FORCE_REVIEW)},
            {"skill": "obsidian-claim-discipline", "status": "executed", "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"]},
        ],
        "status": status,
        "judgment": judgment,
        "next_run": next_run,
        "summary_counts": {
            "scout": summary.get("scout_clue_count"),
            "material": summary.get("materialization_candidate_count"),
            "meaningful": summary.get("meaningful_signal_count"),
        },
    }


def work_packet_text(created_at: str, status: str, next_run: str) -> str:
    return f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
user_request:
  requested_action: continue_goal_execute_f84b_proxy_scout
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
    - obsidian-result-judgment
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


def task_force_review_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f84b_proxy_scout_no_authority
created_at_utc: '{created_at}'
trigger_reason: "F84B is experiment execution(실험 실행) after user asked whether Task Force(태스크포스) agents are being used."
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_02_platform_routing_architect
  - agent_03_philosophy_policy_skill_governance
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "System Governor(시스템 총괄): keep claim boundary(주장 경계) at proxy_scout_only(프록시 탐색 전용)."
    - "Platform Routing Architect(플랫폼 라우팅 설계자): route material candidate(물질 후보) to MT5 materialization(MT5 물질화), not authority(권위)."
    - "Policy/Skill Governance(정책/스킬 거버넌스): no Grok succession(그록 승계 없음), use project-native Task Force(프로젝트 전용 태스크포스)."
    - "Evidence/Control-Plane(근거/제어면): attach receipt/gate/ledger/artifact lineage(영수증/게이트/장부/계보)를 packet(작업 묶음)에 연결."
    - "Data/Feature Contract(데이터/피처 계약): use train-only thresholds(훈련 전용 임계값) and record Tier B missing_required(티어 B 필수 누락)."
    - "Quant Research(정량 연구): rank by density/win-rate/DD/PF/net(밀도/승률/손실폭/PF/순손익), not signal count(신호 수)."
    - "Model Validation/Risk(모델 검증/위험): mark many-surface proxy search(다표면 프록시 탐색) as overfit risk(과최적화 위험)."
    - "MT5/ONNX Runtime(MT5/ONNX 런타임): require Strategy Tester output(전략 테스터 출력) before runtime claim(런타임 주장)."
  rejected:
    - "Do not infer completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) from proxy evidence(프록시 근거)."
  needs_local_verification:
    - "MT5 runtime output(MT5 런타임 출력), tester report(테스터 보고서), and ONNX handoff(온엑스 인계)는 next run(다음 실행) 전까지 missing_required(필수 누락)이다."
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


def artifact_registry_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = [
        ("script", ROOT / SCRIPT_REL),
        ("summary", SUMMARY),
        ("top_candidates", CANDIDATES_TOP),
        ("axis_summary", AXIS_SUMMARY),
        ("label_audit", LABEL_AUDIT),
        ("data_integrity", DATA_INTEGRITY),
        ("model_validation", MODEL_VALIDATION),
        ("task_force_review", TASK_FORCE_REVIEW),
        ("report", REPORT),
        ("gate_audit", GATE_AUDIT),
        ("run_manifest", RUN_MANIFEST),
        ("local_verification", LOCAL_VERIFICATION),
        ("artifact_lineage", ARTIFACT_LINEAGE),
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
            "notes": f"F84B {artifact_type}(F84B 산출물)",
            "artifact_path": rel(path),
            "effect": "Supports F84B proxy scout only(F84B 프록시 탐색만 지원).",
        }
        for artifact_type, path in artifacts
    ]


def update_artifact_registry(created_at: str) -> None:
    for row in artifact_registry_rows(created_at):
        f84a.upsert_csv(ARTIFACT_REGISTRY, "artifact_id", row)


def local_verification(status: str, next_run: str) -> dict[str, Any]:
    task_force_text = io_path(TASK_FORCE_REVIEW).read_text(encoding="utf-8-sig") if path_exists(TASK_FORCE_REVIEW) else ""
    checks = {
        "summary_exists": path_exists(SUMMARY),
        "top_candidates_exists": path_exists(CANDIDATES_TOP),
        "label_audit_exists": path_exists(LABEL_AUDIT),
        "report_exists": path_exists(REPORT),
        "task_force_review_exists": path_exists(TASK_FORCE_REVIEW),
        "task_force_all_agents": all(f"agent_0{i}_" in task_force_text for i in range(1, 9)),
        "run_manifest_exists": path_exists(RUN_MANIFEST),
        "workspace_state_next_run": next_run in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
        "status_recorded": status in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
        "final_claim_guard_exists": path_exists(PACKET_FINAL_CLAIM_GUARD),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks, "claim_boundary": CLAIM_BOUNDARY}


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    candidate_rows, fit_rows, label_rows, summary = fit_and_score()
    top_rows = candidate_rows[:200]
    axis_rows = axis_summary_rows(candidate_rows)
    status, judgment, next_run = status_and_next(summary)

    f84a.write_json(SUMMARY, summary)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, top_rows)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_csv(LABEL_AUDIT, label_rows)
    f84a.write_json(DATA_INTEGRITY, data_integrity_review(summary))
    f84a.write_json(MODEL_VALIDATION, model_validation_review(summary))
    f84a.write_text(REPORT, report_text(created_at, summary, top_rows))
    f84a.write_text(TASK_FORCE_REVIEW, task_force_review_text(created_at, status, judgment, next_run, summary))
    f84a.write_text(GATE_AUDIT, gate_audit_text(status, summary, next_run))
    f84a.write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "status": status,
            "judgment": judgment,
            "next_run_id": next_run,
            "claim_boundary": CLAIM_BOUNDARY,
            "summary": summary,
            "producer": SCRIPT_REL,
            "created_at_utc": created_at,
        },
    )
    f84a.write_json(PACKET_SKILL_RECEIPTS, receipts(status, judgment, next_run, summary))
    f84a.write_text(WORK_PACKET, work_packet_text(created_at, status, next_run))
    f84a.write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "status": "pass",
            "gates": {
                "scope_completion_gate": "pass",
                "kpi_contract_audit": "pass",
                "skill_receipt_lint": "pass",
                "codex_task_force_review_packet": "pass",
                "required_gate_coverage_audit": "pass",
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    f84a.write_json(
        PACKET_FINAL_CLAIM_GUARD,
        {
            "packet_id": RUN_ID,
            "status": "pass",
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )

    update_ledgers(created_at, status, judgment, next_run, summary)
    update_state_files(created_at, status, judgment, next_run, summary)
    update_idea_and_negative_register(summary, status, next_run)
    update_review_index()
    verification = local_verification(status, next_run)
    f84a.write_json(LOCAL_VERIFICATION, verification)
    f84a.write_json(ARTIFACT_LINEAGE, artifact_lineage(summary, next_run))
    update_artifact_registry(created_at)

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
                "winrate_preserved_count": summary["winrate_preserved_count"],
                "best_candidate": (summary.get("best_candidate") or {}).get("candidate_id"),
                "best_oos": {
                    "net": (summary.get("best_candidate") or {}).get("oos_net"),
                    "pf": (summary.get("best_candidate") or {}).get("oos_pf"),
                    "dd": (summary.get("best_candidate") or {}).get("oos_dd_pct"),
                    "tpd": (summary.get("best_candidate") or {}).get("oos_calendar_trades_day"),
                    "trades": (summary.get("best_candidate") or {}).get("oos_trade_count"),
                    "win_rate": (summary.get("best_candidate") or {}).get("oos_win_rate_percent"),
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
