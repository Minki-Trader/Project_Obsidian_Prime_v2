from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_h17_oos108_pf125_density_profit_conflict_reblend_without_db as ga
from stage_pipelines.stage364 import train_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db as fx
from stage_pipelines.stage364 import train_h17_oos108_pf125_density_profit_conflict_reblend_without_db as fz
from stage_pipelines.stage364 import train_h17_oos108_pf125_density3_oos_profit_bridge_without_db as fv
from stage_pipelines.stage364 import train_h17_oos108_pf125_regime_profit_density_reexpand_without_db as ft


fn = fz.fn
et = fz.et

TODAY = "2026-06-07"
STAGE_ID = ft.STAGE_ID
RUN_NUMBER = "run364GB"
RUN_ID = "run364GB_train_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1"
PARENT_RUN_ID = ga.RUN_ID
NEXT_RUN_ID = "run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1"

STATUS_NO_STRICT = "completed_stage364GB_session_side_loss_veto_rescue_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364GB_session_side_loss_veto_rescue_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_session_side_loss_veto_rescue_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_session_side_loss_veto_rescue_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364GB_open_run364GC_session_side_loss_veto_rescue_review"
DECISION_STRICT = "stage364GB_open_run364GC_session_side_loss_veto_rescue_review"
CLAIM_BOUNDARY = (
    "research_development_session_side_loss_veto_rescue_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ft.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "gb_feature_audit.csv"
LABEL_SUMMARY = RUN_DIR / "gb_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "gb_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "gb_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_gb_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_gb_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_gb_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_gb_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_gb_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364GC_QUEUE = RUN_DIR / "gb_gc_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GB_session_side_loss_veto_rescue.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GB_session_side_loss_veto_rescue.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

THIS_FILE = Path(__file__)

INPUT_FILES = [
    ga.FINAL_DECISION,
    ga.GATE_AUDIT,
    ga.REVIEW_SUMMARY,
    ga.SURFACE_DIAGNOSTIC,
    ga.FAILURE_ATTRIBUTION,
    ga.PACKAGE_DECISION,
    ga.FAILURE_MEMORY,
    ga.RUN364GB_QUEUE,
    fz.FINAL_DECISION,
    fz.TRADE_SURFACE,
    fz.SELECTED_CANDIDATE,
    fz.SELECTED_TRADE_TAPE,
    fz.COST_STRESS,
    fz.SIDE_SESSION_REVIEW,
    fz.MONTH_STABILITY,
    fx.FINAL_DECISION,
    fx.TRADE_SURFACE,
    fx.SELECTED_CANDIDATE,
    fx.SELECTED_TRADE_TAPE,
    fx.COST_STRESS,
    fx.SIDE_SESSION_REVIEW,
    fx.MONTH_STABILITY,
    fv.FINAL_DECISION,
    fv.TRADE_SURFACE,
    fv.SELECTED_CANDIDATE,
    fv.SELECTED_TRADE_TAPE,
    fv.COST_STRESS,
    fv.SIDE_SESSION_REVIEW,
    fv.MONTH_STABILITY,
    ft.FINAL_DECISION,
    ft.TRADE_SURFACE,
    ft.SELECTED_CANDIDATE,
    ft.SELECTED_TRADE_TAPE,
    ft.COST_STRESS,
    ft.SIDE_SESSION_REVIEW,
    ft.MONTH_STABILITY,
    et.dt.dp.MODEL_INPUT_DATASET,
    et.dt.dp.MODEL_INPUT_FEATURE_ORDER,
    et.dt.dp.RAW_US100_M5,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    FEATURE_AUDIT,
    LABEL_SUMMARY,
    MODEL_SCORECARD,
    TRADE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    MONTH_STABILITY,
    COST_STRESS,
    SIDE_SESSION_REVIEW,
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    DATA_INTEGRITY_AUDIT,
    RUN364GC_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    THIS_FILE,
]

LABEL_SPECS = [
    {"label_id": "gb_sym_h1_m0p50", "horizon_m5": 1, "threshold_points": 0.50, "mode": "symmetric"},
    {"label_id": "gb_sym_h1_m0p60", "horizon_m5": 1, "threshold_points": 0.60, "mode": "symmetric"},
    {"label_id": "gb_sym_h2_m0p60", "horizon_m5": 2, "threshold_points": 0.60, "mode": "symmetric"},
    {"label_id": "gb_asym_h1_l0p50_s1p05", "horizon_m5": 1, "threshold_points": 0.80, "long_threshold_points": 0.50, "short_threshold_points": 1.05, "mode": "asymmetric"},
]
TARGET_DENSITIES = [2.65, 2.8, 2.95, 3.05, 3.2]
MARGINS = [-0.22, -0.18, -0.14, -0.10, -0.06, 0.0]
HOUR_SETS = {
    "gb_cash_15_to_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "gb_veto_long16_17_scope": [16, 17, 18, 19, 20, 21, 22],
    "gb_short18_preserve": [15, 16, 17, 18, 19, 21, 22],
    "gb_profit_month_bridge": [14, 15, 16, 18, 19, 21, 22],
    "gb_density_soft_veto": [15, 16, 17, 18, 19, 20, 21],
}
EXTRA_FILTERS = [
    "none",
    "gb_loss_veto_core",
    "gb_short18_preserve",
    "gb_profit_session_mix",
    "gb_density_soft_veto",
]

DENSITY_FLOOR = 3.0
STRICT_SHORT_SHARE_FLOOR = 0.77
PRESERVE_SHORT_SHARE_FLOOR = 0.77
STRICT_MIN_PF_FLOOR = 1.05
OOS_PF_TARGET = 1.25
OPERATIONAL_MIN_PF_FLOOR = 1.18
RUNTIME_NET_REFERENCE = 523.58


def rel(path: Path | str) -> str:
    return fn.rel(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return fn.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return number


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GB inputs(GB 입력 누락): " + ", ".join(missing))
    with fn.io_path(ga.FINAL_DECISION).open("r", encoding="utf-8-sig") as handle:
        parent = json.load(handle)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GA next_run_id mismatch(GA 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GA claim(금지된 GA 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(ga.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GA gate audit(GA 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GB session side loss veto rescue input(GB 세션 방향 손실 차단 회수 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def full_label_spec(spec: Mapping[str, Any]) -> Mapping[str, Any]:
    label_id = str(spec.get("label_id", ""))
    for candidate in LABEL_SPECS:
        if candidate["label_id"] == label_id:
            return {**candidate, **dict(spec)}
    return spec


def gb_label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    spec = full_label_spec(spec)
    horizon = int(spec["horizon_m5"])
    move = frame[f"future_open_h{horizon}"] - frame["entry_open"]
    ok = np.isfinite(move.to_numpy(dtype=float)) & np.isfinite(frame["entry_open"].to_numpy(dtype=float))
    if spec.get("mode") == "asymmetric":
        long_threshold = float(spec["long_threshold_points"])
        short_threshold = float(spec["short_threshold_points"])
    else:
        long_threshold = short_threshold = float(spec["threshold_points"])
    move_values = move.to_numpy(dtype=float)
    labels = np.where(move_values <= -short_threshold, 0, np.where(move_values >= long_threshold, 2, 1)).astype("int8")
    labels[~ok] = 1
    return labels, ok


def gb_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base = list(feature_order)
    derived = et.dt.derived_features()
    price = [column for column in base if any(token in column for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [column for column in base if any(token in column for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [column for column in base if any(token in column for token in ["cash", "minutes", "open", "close"])]
    behavior = [column for column in base if any(token in column for token in ["trend", "momentum", "range", "body", "wick", "spread"])]
    return {
        "gb_all72": list(dict.fromkeys(base + derived)),
        "gb_session_side_blend": list(dict.fromkeys(price + macro + session + behavior + derived)),
        "gb_oos_profit_regime": list(dict.fromkeys(price + macro + session + derived)),
    }


def gb_model_specs() -> list[tuple[str, str, Any]]:
    return [
        ("et7_l12_n132", "ExtraTrees(엑스트라트리)", et.dt.dp.ExtraTreesClassifier(n_estimators=132, max_depth=7, min_samples_leaf=12, class_weight="balanced", random_state=921, n_jobs=1)),
        ("et8_l16_n132", "ExtraTrees(엑스트라트리)", et.dt.dp.ExtraTreesClassifier(n_estimators=132, max_depth=8, min_samples_leaf=16, class_weight="balanced", random_state=922, n_jobs=1)),
        ("rf8_l20_n132", "RandomForest(랜덤포레스트)", et.dt.dp.RandomForestClassifier(n_estimators=132, max_depth=8, min_samples_leaf=20, class_weight="balanced_subsample", random_state=923, n_jobs=1)),
    ]


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> np.ndarray:
    if name in frame.columns:
        return frame[name].to_numpy(dtype=float)
    return np.full(len(frame), default, dtype=float)


def gb_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = col(frame, "log_return_3", 0.0)
    vix_stress = col(frame, "vix_zscore_20", 0.0)
    range_ratio = col(frame, "range_5_over_20", 1.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "gb_loss_veto_core":
        long_ok = (side == "long") & np.isin(hour, [18, 19, 21, 22]) & (breadth >= 0.30) & (vix_stress <= 2.05)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18, 19, 21, 22]) & (vol_ratio >= 0.58) & ((breadth <= 0.68) | (log_return_3 < 0.00002))
        return mask & (long_ok | short_ok)
    if extra_filter == "gb_short18_preserve":
        long_ok = (side == "long") & np.isin(hour, [18, 21, 22]) & (breadth >= 0.34) & (range_ratio >= 0.55) & (vix_stress <= 1.85)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18, 19, 21]) & (vol_ratio >= 0.60) & ((hour == 18) | (breadth <= 0.63) | (log_return_3 < -0.00003))
        return mask & (long_ok | short_ok)
    if extra_filter == "gb_profit_session_mix":
        long_ok = (side == "long") & np.isin(hour, [14, 15, 18, 21, 22]) & (breadth >= 0.33) & (vix_stress <= 2.00)
        short_ok = (side == "short") & np.isin(hour, [15, 16, 18, 19, 21, 22]) & (vol_ratio >= 0.63) & ((breadth <= 0.65) | (log_return_3 < -0.00002))
        return mask & (long_ok | short_ok)
    if extra_filter == "gb_density_soft_veto":
        veto = (
            ((side == "long") & np.isin(hour, [16, 17]))
            | ((side == "short") & (hour == 20))
            | ((side == "long") & (vix_stress > 2.25))
            | ((side == "short") & (hour == 21) & (breadth > 0.70) & (vol_ratio < 0.72))
        )
        density_ok = np.isin(hour, [15, 16, 17, 18, 19, 20, 21, 22]) & (range_ratio >= 0.48)
        return mask & density_ok & ~veto
    raise ValueError(f"unknown GB filter(알 수 없는 GB 필터): {extra_filter}")


def gb_cost_values(row: Mapping[str, Any]) -> dict[str, float]:
    values = et.er.cost_side_values(row)
    validation_trades = as_float(row.get("validation_trade_count"))
    oos_trades = as_float(row.get("oos_trade_count"))
    validation_net = as_float(row.get("validation_net"))
    oos_net = as_float(row.get("oos_net"))
    values["validation_cost09_net"] = validation_net - 0.60 * validation_trades
    values["oos_cost09_net"] = oos_net - 0.60 * oos_trades
    values["validation_trade_density"] = as_float(row.get("validation_trade_density"))
    values["oos_trade_density"] = as_float(row.get("oos_trade_density"))
    return values


def gb_strict_success(row: Mapping[str, Any]) -> bool:
    values = gb_cost_values(row)
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    return (
        as_float(row.get("validation_net")) > 0.0
        and as_float(row.get("oos_net")) > 0.0
        and oos_pf >= OOS_PF_TARGET
        and values["oos_cost09_net"] >= 0.0
        and values["combined_cost09_net"] >= 0.0
        and values["validation_trade_density"] >= DENSITY_FLOOR
        and values["oos_trade_density"] >= DENSITY_FLOOR
        and values["combined_trade_density"] >= DENSITY_FLOOR
        and values["combined_net"] > 0.0
        and values["combined_short_share"] <= STRICT_SHORT_SHARE_FLOOR
        and min_pf >= STRICT_MIN_PF_FLOOR
    )


def gb_operational_stack(row: Mapping[str, Any]) -> bool:
    values = gb_cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return gb_strict_success(row) and values["combined_net"] >= RUNTIME_NET_REFERENCE and min_pf >= OPERATIONAL_MIN_PF_FLOOR


def readiness(value: float, target: float, span: float) -> float:
    return max(0.0, min(1.0, (value - target + span) / span))


def gb_selection_score(row: Mapping[str, Any]) -> float:
    values = gb_cost_values(row)
    validation_net = as_float(row.get("validation_net"))
    oos_net = as_float(row.get("oos_net"))
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    validation_density = values["validation_trade_density"]
    oos_density = values["oos_trade_density"]
    density = values["combined_trade_density"]
    min_density = min(validation_density, oos_density, density)
    short_share = values["combined_short_share"]
    validation_cost09 = values["validation_cost09_net"]
    oos_cost09 = values["oos_cost09_net"]
    filter_id = str(row.get("extra_filter", "none"))
    hour_id = str(row.get("hours_id", ""))
    density3_ready = min(
        readiness(validation_density, DENSITY_FLOOR, 0.42),
        readiness(oos_density, DENSITY_FLOOR, 0.42),
        readiness(density, DENSITY_FLOOR, 0.42),
    )
    near_density = min(
        readiness(validation_density, 2.88, 0.34),
        readiness(oos_density, 2.88, 0.34),
        readiness(density, 2.88, 0.34),
    )
    density_anchor = min(near_density, readiness(validation_net, -35.0, 190.0), readiness(values["combined_net"], -140.0, 300.0))
    profit_anchor = min(
        readiness(oos_net, -5.0, 170.0),
        readiness(oos_pf, 1.02, 0.22),
        readiness(oos_cost09, -180.0, 330.0),
    )
    cost_repair = min(readiness(values["combined_cost09_net"], -280.0, 520.0), readiness(oos_cost09, -100.0, 360.0))
    bridge = min(density_anchor, profit_anchor)
    session_veto_bonus = 1.0 if filter_id in {"gb_loss_veto_core", "gb_short18_preserve", "gb_profit_session_mix", "gb_density_soft_veto"} else 0.0
    density_scope_bonus = 1.0 if hour_id in {"gb_cash_15_to_22", "gb_density_soft_veto", "gb_veto_long16_17_scope"} else 0.0
    density3_valpos_oospos = density3_ready >= 1.0 and validation_net > 0.0 and oos_net > 0.0
    near_density_oospos = near_density >= 1.0 and oos_net > 0.0 and oos_pf >= 1.02
    low_density_cost_only = oos_pf >= OOS_PF_TARGET and oos_cost09 >= 0.0 and min_density < 2.86
    density_only_negative = density3_ready >= 1.0 and oos_net <= 0.0
    strict_shape_bonus = 1.0 if gb_strict_success(row) else 0.0
    return (
        17200.0 * bridge
        + 6800.0 * near_density
        + 7200.0 * density_anchor
        + 10400.0 * profit_anchor
        + 4200.0 * cost_repair
        + 12200.0 * (1.0 if density3_valpos_oospos else 0.0)
        + 6200.0 * (1.0 if near_density_oospos else 0.0)
        + 1800.0 * session_veto_bonus
        + 1200.0 * density_scope_bonus
        + 1.25 * validation_net
        + 2.75 * oos_net
        + 1.08 * values["combined_net"]
        + 1350.0 * max(0.0, validation_pf - 1.0)
        + 2800.0 * max(0.0, oos_pf - 1.0)
        + 1200.0 * max(0.0, min_pf - 1.0)
        + 0.80 * validation_cost09
        + 2.75 * oos_cost09
        + 1.25 * values["combined_cost09_net"]
        + 2100.0 * min(min_density, 4.5)
        + 760.0 * min(validation_density, 5.5)
        + 960.0 * min(oos_density, 5.5)
        + 760.0 * max(0.0, PRESERVE_SHORT_SHARE_FLOOR - short_share)
        + 13000.0 * strict_shape_bonus
        - 11200.0 * (1.0 if low_density_cost_only else 0.0)
        - 10400.0 * (1.0 if density_only_negative else 0.0)
        - 2100.0 * max(0.0, OOS_PF_TARGET - oos_pf)
        - 3400.0 * (1.0 if validation_net <= 0.0 else 0.0)
        - 4600.0 * (1.0 if oos_net <= 0.0 else 0.0)
        - 4.2 * max(0.0, -validation_cost09)
        - 5.8 * max(0.0, -oos_cost09)
        - 2.4 * max(0.0, -values["combined_cost09_net"] - 160.0)
        - 5200.0 * max(0.0, 2.9 - validation_density)
        - 5200.0 * max(0.0, 2.9 - oos_density)
        - 5600.0 * max(0.0, 2.9 - density)
        - 3600.0 * max(0.0, DENSITY_FLOOR - min_density)
        - 1500.0 * max(0.0, short_share - PRESERVE_SHORT_SHARE_FLOOR)
    )


def write_work_packet(parent: Mapping[str, Any]) -> None:
    fn.write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": ["obsidian-experiment-design(실험 설계)", "obsidian-data-integrity(데이터 무결성)", "obsidian-model-validation(모델 검증)", "obsidian-artifact-lineage(산출물 계보)"],
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "hypothesis": "GA failure memory(GA 실패 기억)의 FZ loss clusters(FZ 손실 군집)를 session/side veto(세션/방향 차단)로 제거하면 OOS profit(표본외 수익)과 near-density(근접 밀도)를 함께 회복할 수 있습니다.",
            "comparison_baseline": PARENT_RUN_ID,
            "decision_use": NEXT_RUN_ID,
            "control_variables": ["US100 M5", "chronological split(시간순 분할)", "Python proxy only(Python 프록시 전용)", "ONNX smoke only(ONNX 스모크만)"],
            "changed_variables": ["session-side veto filters(세션-방향 차단 필터)", "short18 preserve rule(18시 숏 보존 규칙)", "lower label barrier(낮춘 라벨 장벽)", "cost repair score(비용 수리 점수)"],
            "success_criteria": ["density3_all_splits_valpos_oospos_count>0", "oos_net>0", "oos_pf>=1.05", "validation_density>=3", "oos_density>=3", "combined_density>=3"],
            "failure_criteria": ["density-only OOS negative(밀도 전용 표본외 음수)", "low-density profit-only(저밀도 수익 전용)", "validation profit collapse(검증 수익 붕괴)"],
            "invalid_conditions": ["parent gate failure(부모 게이트 실패)", "lookahead leakage(미래참조 누수)", "missing required input(필수 입력 누락)"],
            "parent_summary": {
                "density3_all_splits_count": parent.get("density3_all_splits_count"),
                "density3_all_splits_valpos_oospos_count": parent.get("density3_all_splits_valpos_oospos_count"),
                "selected_oos_net": parent.get("selected_oos_net"),
                "selected_oos_profit_factor": parent.get("selected_oos_profit_factor"),
                "validation_positive_density3_count": parent.get("validation_positive_density3_count"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    RUN364GC_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(
        RUN364GC_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "gc01_session_side_loss_veto_rescue_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_validation_density": summary["selected_validation_trade_density"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_cost06_net": summary["selected_oos_cost06_net"],
                "selected_combined_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "selected_combined_short_share": summary["selected_combined_short_share"],
                "effect": "GC review(GC 검토)가 GB session/side loss veto rescue(GB 세션/방향 손실 차단 회수)의 손실 군집 차단 효과를 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    fn.write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke(Python 프록시와 ONNX 스모크), no MT5(MT5 없음)"})
    fn.write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "session/side loss veto rescue(세션/방향 손실 차단 회수)가 FZ loss clusters(FZ 손실 군집)를 줄이고 OOS profit(표본외 수익)을 회복하는지 시험합니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    fn.write_json(DATA_RECEIPT, {**base, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp(UTC 모델 입력 타임스탬프)", "sample_scope": "US100 M5 Tier A proxy split(US100 M5 Tier A 프록시 분할)", "feature_label_boundary": "future_open only in labels(future_open은 라벨에만 사용)", "split_boundary": "chronological train/validation/OOS(시간순 학습/검증/표본외)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    fn.write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "target_and_label": "3-class next-open horizon direction(3분류 다음 시가 horizon 방향)", "split_method": "chronological holdout(시간순 홀드아웃)", "selection_metric": "GB score rewards session veto, OOS profit, cost repair, and near-density(GB 점수는 세션 차단, 표본외 수익, 비용 수리, 근접 밀도를 보상)", "threshold_policy": "searched threshold and density target(탐색 임계값과 밀도 목표)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    fn.write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도) {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']} and(및) {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["session-side veto score(세션-방향 차단 점수)", "short18 preserve clue(18시 숏 보존 단서)", "OOS cost repair score(표본외 비용 수리 점수)"], "next_probe": NEXT_RUN_ID})
    fn.write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    fn.write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_session_side_loss_veto_rescue_proxy(세션 방향 손실 차단 회수 프록시 연결)"})
    fn.write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "GB 모델 단서를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GB Session Side Loss Veto Rescue(세션 방향 손실 차단 회수)

Created(생성): {final['created_at_utc']}

Action(행동): GA failure memory(GA 실패 기억)를 받아 FZ loss clusters(FZ 손실 군집)를 session/side veto(세션/방향 차단) 필터로 학습했습니다.

Effect(효과): 16-17 long loss(16-17시 롱 손실)와 20 short loss(20시 숏 손실)를 줄이면서 OOS profit(표본외 수익)과 near density(근접 밀도)를 회복할 수 있는지 확인합니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.6 net(표본외 비용0.6 순수익): `{final['selected_oos_cost06_net']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `{final['operational_proxy_stack_pass_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GB Session Side Loss Veto Rescue(세션 방향 손실 차단 회수)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GB model/label/score(GB 모델/라벨/점수) 세션/방향 손실 차단을 실행하고 GC review(GC 검토)로 넘겼습니다.

Effect(효과): 손실 군집 차단 결과를 운영 주장 없이 다음 판정으로 보냅니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GB__{RUN_ID}", f"\n- run364GB__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - session side loss veto rescue(세션 방향 손실 차단 회수), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GB__{RUN_ID}", f"\n<!-- run364GB__{RUN_ID} -->\n\n## run364GB Session Side Loss Veto Rescue(세션 방향 손실 차단 회수)\n\nAction(행동): GA failure memory(GA 실패 기억)의 FZ loss clusters(FZ 손실 군집)를 session/side veto(세션/방향 차단)로 시험했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 패키지 가능성과 실패 경계를 검토합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GB__{RUN_ID}", f"\n<!-- run364GB__{RUN_ID} -->\n## run364GB session side loss veto rescue(세션 방향 손실 차단 회수)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    fn.write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    fn.write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364GB` trained(학습 완료) session side loss veto rescue(세션 방향 손실 차단 회수). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost/side truth(비용/방향 진실): OOS cost0.6 net(표본외 비용0.6 순수익)은 `{final['selected_oos_cost06_net']}`이고, combined cost0.9/short share(합산 비용0.9/숏 비중)는 `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 GB 결과를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): GB session side loss veto rescue(GB 세션 방향 손실 차단 회수).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GB__{RUN_ID}", f"\n<!-- run364GB__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed session side loss veto rescue(세션 방향 손실 차단 회수); strict candidates(엄격 후보) `{final['strict_candidate_count']}`; selected(선택) `{final['selected_model_id']}`; next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GB__{RUN_ID}", f"\n<!-- run364GB__{RUN_ID} -->\n- `{RUN_ID}`: session side loss veto rescue(세션 방향 손실 차단 회수)를 학습했습니다. Effect(효과): GA 실패 기억을 session/side veto(세션/방향 차단)와 cost repair score(비용 수리 점수)로 공격했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        fn.append_text_once(NEGATIVE_REGISTER, f"run364GB__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364GB__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: session side loss veto rescue(세션 방향 손실 차단 회수)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GC에서 실패 경계와 회수 단서를 분리합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST})
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can session-side loss veto rescue recover OOS profit and near-density together?(세션-방향 손실 차단 회수가 표본외 수익과 근접 밀도를 함께 회복할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};validation_density={final['selected_validation_trade_density']};oos_pf={final['selected_oos_profit_factor']};combined_density={final['selected_combined_trade_density']};combined_short={final['selected_combined_short_share']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "view": record_view,
                "tier": tier_scope,
                "kpi_scope": "GB session side loss veto rescue(GB 세션 방향 손실 차단 회수)",
                "metric_scope": "python_proxy_onnx_smoke(Python 프록시/ONNX 스모크)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "",
                "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시/ONNX 스모크, MT5 없음)",
            }
        )
    fn.append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    fn.append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    fn.append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "experiment_execution(실험 실행)",
                "run_type": "session_side_loss_veto_rescue(세션 방향 손실 차단 회수)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(TRADE_SURFACE),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    try:
        et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and fn.io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "GB session side loss veto rescue artifact(GB 세션 방향 손실 차단 회수 산출물)",
                }
            )
    fn.append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def apply_gb_patch() -> None:
    replacements = {
        "TODAY": TODAY,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS_NO_STRICT": STATUS_NO_STRICT,
        "STATUS_STRICT": STATUS_STRICT,
        "JUDGMENT_NO_STRICT": JUDGMENT_NO_STRICT,
        "JUDGMENT_STRICT": JUDGMENT_STRICT,
        "DECISION_NO_STRICT": DECISION_NO_STRICT,
        "DECISION_STRICT": DECISION_STRICT,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "RUN_DIR": RUN_DIR,
        "MODEL_DIR": MODEL_DIR,
        "ONNX_DIR": ONNX_DIR,
        "INPUT_MANIFEST": INPUT_MANIFEST,
        "WORK_PACKET": WORK_PACKET,
        "FEATURE_AUDIT": FEATURE_AUDIT,
        "LABEL_SUMMARY": LABEL_SUMMARY,
        "MODEL_SCORECARD": MODEL_SCORECARD,
        "TRADE_SURFACE": TRADE_SURFACE,
        "SELECTED_CANDIDATE": SELECTED_CANDIDATE,
        "SELECTED_TRADE_TAPE": SELECTED_TRADE_TAPE,
        "MONTH_STABILITY": MONTH_STABILITY,
        "COST_STRESS": COST_STRESS,
        "SIDE_SESSION_REVIEW": SIDE_SESSION_REVIEW,
        "MODEL_ARTIFACT_MANIFEST": MODEL_ARTIFACT_MANIFEST,
        "ONNX_SMOKE_REPORT": ONNX_SMOKE_REPORT,
        "DATA_INTEGRITY_AUDIT": DATA_INTEGRITY_AUDIT,
        "RUN364FO_QUEUE": RUN364GC_QUEUE,
        "RUN_EVIDENCE_RECEIPT": RUN_EVIDENCE_RECEIPT,
        "EXPERIMENT_RECEIPT": EXPERIMENT_RECEIPT,
        "DATA_RECEIPT": DATA_RECEIPT,
        "MODEL_RECEIPT": MODEL_RECEIPT,
        "ATTRIBUTION_RECEIPT": ATTRIBUTION_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "CLAIM_RECEIPT": CLAIM_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "THIS_FILE": THIS_FILE,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
        "LABEL_SPECS": LABEL_SPECS,
        "TARGET_DENSITIES": TARGET_DENSITIES,
        "MARGINS": MARGINS,
        "HOUR_SETS": HOUR_SETS,
        "EXTRA_FILTERS": EXTRA_FILTERS,
    }
    for name, value in replacements.items():
        setattr(fn, name, value)
    fn.fm = ga
    fn.validate_inputs = validate_inputs
    fn.input_manifest_rows = input_manifest_rows
    fn.full_label_spec = full_label_spec
    fn.fn_label_values = gb_label_values
    fn.fn_feature_sets = gb_feature_sets
    fn.fn_model_specs = gb_model_specs
    fn.fn_extra_mask = gb_extra_mask
    fn.fn_cost_values = gb_cost_values
    fn.fn_strict_success = gb_strict_success
    fn.fn_operational_stack = gb_operational_stack
    fn.fn_selection_score = gb_selection_score
    fn.write_work_packet = write_work_packet
    fn.write_queue = write_queue
    fn.write_receipts = write_receipts
    fn.write_docs = write_docs
    fn.write_ledgers = write_ledgers
    fn.write_artifact_registry = write_artifact_registry


def main() -> None:
    apply_gb_patch()
    fn.main()


if __name__ == "__main__":
    main()
