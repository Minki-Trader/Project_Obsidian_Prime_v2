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

from stage_pipelines.stage364 import review_h17_oos108_pf125_positive_density_floor_reseed_without_db as fq
from stage_pipelines.stage364 import train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db as fn


TODAY = "2026-06-07"
STAGE_ID = fn.STAGE_ID
RUN_NUMBER = "run364FR"
RUN_ID = "run364FR_train_h17_oos108_pf125_density3_regime_split_repair_without_db_v1"
PARENT_RUN_ID = fq.RUN_ID
NEXT_RUN_ID = "run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1"

STATUS_NO_STRICT = "completed_stage364FR_density3_regime_split_repair_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364FR_density3_regime_split_repair_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_density3_regime_split_repair_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_density3_regime_split_repair_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364FR_open_run364FS_density3_regime_split_repair_review"
DECISION_STRICT = "stage364FR_open_run364FS_density3_regime_split_repair_review"
CLAIM_BOUNDARY = (
    "research_development_density3_regime_split_repair_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = fn.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "fr_feature_audit.csv"
LABEL_SUMMARY = RUN_DIR / "fr_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "fr_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "fr_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_fr_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_fr_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_fr_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_fr_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_fr_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364FS_QUEUE = RUN_DIR / "fr_fs_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364FR_density3_regime_split_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364FR_density3_regime_split_repair.md"
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
et = fn.et

INPUT_FILES = [
    fq.FINAL_DECISION,
    fq.GATE_AUDIT,
    fq.REVIEW_SUMMARY,
    fq.SURFACE_DIAGNOSTIC,
    fq.FAILURE_ATTRIBUTION,
    fq.PACKAGE_DECISION,
    fq.FAILURE_MEMORY,
    fq.RUN364FR_QUEUE,
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
    RUN364FS_QUEUE,
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
    {"label_id": "fr_sym_h1_m1p25", "horizon_m5": 1, "threshold_points": 1.25, "mode": "symmetric"},
    {"label_id": "fr_sym_h1_m1p5", "horizon_m5": 1, "threshold_points": 1.50, "mode": "symmetric"},
    {"label_id": "fr_sym_h2_m1p5", "horizon_m5": 2, "threshold_points": 1.50, "mode": "symmetric"},
    {"label_id": "fr_asym_h2_l1p5_s2p5", "horizon_m5": 2, "threshold_points": 2.00, "long_threshold_points": 1.50, "short_threshold_points": 2.50, "mode": "asymmetric"},
]
TARGET_DENSITIES = [3.0, 3.08, 3.2, 3.4, 3.75]
MARGINS = [-0.12, -0.08, -0.04, -0.02, 0.0]
HOUR_SETS = {
    "fr_cash_15_to_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "fr_dense_no_h19": [15, 16, 17, 18, 20, 21, 22],
    "fr_us_open_15_16_17_18": [15, 16, 17, 18],
    "fr_regime_core_15_16_18_20_22": [15, 16, 18, 20, 22],
    "fr_late_non19_16_18_20_21_22": [16, 18, 20, 21, 22],
}
EXTRA_FILTERS = [
    "none",
    "fr_risk_on_long_risk_off_short",
    "fr_low_vix_breadth",
    "fr_high_vol_short_guard",
    "fr_side_balance",
    "fr_no_bleed_regime",
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
        raise FileNotFoundError("missing FR inputs(FR 입력 누락): " + ", ".join(missing))
    with fn.io_path(fq.FINAL_DECISION).open("r", encoding="utf-8-sig") as handle:
        parent = json.load(handle)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"FQ next_run_id mismatch(FQ 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden FQ claim(금지된 FQ 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(fq.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("FQ gate audit(FQ 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "FR density3 regime split repair input(FR 밀도3 국면 분할 수리 입력)",
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


def fr_label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
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


def fr_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base = list(feature_order)
    derived = et.dt.derived_features()
    price = [column for column in base if any(token in column for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [column for column in base if any(token in column for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [column for column in base if any(token in column for token in ["cash", "minutes", "open", "close"])]
    behavior = [column for column in base if any(token in column for token in ["trend", "momentum", "range", "body", "wick", "spread"])]
    return {
        "fr_all72": list(dict.fromkeys(base + derived)),
        "fr_regime_macro": list(dict.fromkeys(price + macro + session + derived)),
        "fr_session_side": list(dict.fromkeys(price + session + behavior + derived)),
    }


def fr_model_specs() -> list[tuple[str, str, Any]]:
    return [
        ("et7_l10_n160", "ExtraTrees(엑스트라트리)", et.dt.dp.ExtraTreesClassifier(n_estimators=160, max_depth=7, min_samples_leaf=10, class_weight="balanced", random_state=871, n_jobs=1)),
        ("et8_l16_n160", "ExtraTrees(엑스트라트리)", et.dt.dp.ExtraTreesClassifier(n_estimators=160, max_depth=8, min_samples_leaf=16, class_weight="balanced", random_state=872, n_jobs=1)),
        ("rf8_l20_n160", "RandomForest(랜덤포레스트)", et.dt.dp.RandomForestClassifier(n_estimators=160, max_depth=8, min_samples_leaf=20, class_weight="balanced_subsample", random_state=873, n_jobs=1)),
    ]


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> np.ndarray:
    if name in frame.columns:
        return frame[name].to_numpy(dtype=float)
    return np.full(len(frame), default, dtype=float)


def fr_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = col(frame, "log_return_3", 0.0)
    vix_stress = col(frame, "vix_zscore_20", 0.0)
    range_ratio = col(frame, "range_5_over_20", 1.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "fr_risk_on_long_risk_off_short":
        long_ok = (side == "long") & np.isin(hour, [15, 16, 17, 18, 20, 21, 22]) & (breadth >= 0.42) & (vix_stress <= 1.35)
        short_ok = (side == "short") & np.isin(hour, [16, 18, 20, 22]) & ((breadth <= 0.54) | (vix_stress >= 0.25)) & (vol_ratio >= 0.78)
        return mask & (long_ok | short_ok)
    if extra_filter == "fr_low_vix_breadth":
        long_ok = (side == "long") & (breadth >= 0.48) & (vix_stress <= 1.10) & np.isin(hour, [15, 16, 18, 20, 21, 22])
        short_ok = (side == "short") & (breadth <= 0.50) & (vol_ratio >= 0.86) & np.isin(hour, [16, 18, 22])
        return mask & (long_ok | short_ok)
    if extra_filter == "fr_high_vol_short_guard":
        long_ok = (side == "long") & (vix_stress <= 1.55) & (range_ratio >= 0.66) & np.isin(hour, [15, 16, 18, 21, 22])
        short_ok = (side == "short") & (vol_ratio >= 0.90) & ((breadth <= 0.55) | (log_return_3 < -0.00009)) & np.isin(hour, [16, 18, 20, 22])
        return mask & (long_ok | short_ok)
    if extra_filter == "fr_side_balance":
        long_ok = (side == "long") & (breadth >= 0.38) & (vix_stress <= 1.65) & np.isin(hour, [15, 16, 18, 20, 21, 22])
        short_ok = (side == "short") & (vol_ratio >= 0.80) & (breadth <= 0.58) & np.isin(hour, [16, 17, 18, 22])
        return mask & (long_ok | short_ok)
    if extra_filter == "fr_no_bleed_regime":
        veto = (
            ((side == "short") & (hour == 20) & (vol_ratio < 0.88))
            | ((side == "short") & (hour == 17) & (breadth > 0.62))
            | ((side == "long") & (hour == 19))
            | ((side == "long") & (vix_stress > 1.85))
        )
        return mask & ~veto
    raise ValueError(f"unknown FR filter(알 수 없는 FR 필터): {extra_filter}")


def fr_cost_values(row: Mapping[str, Any]) -> dict[str, float]:
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


def fr_strict_success(row: Mapping[str, Any]) -> bool:
    values = fr_cost_values(row)
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


def fr_operational_stack(row: Mapping[str, Any]) -> bool:
    values = fr_cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return fr_strict_success(row) and values["combined_net"] >= RUNTIME_NET_REFERENCE and min_pf >= OPERATIONAL_MIN_PF_FLOOR


def readiness(value: float, target: float, span: float) -> float:
    return max(0.0, min(1.0, (value - target + span) / span))


def fr_selection_score(row: Mapping[str, Any]) -> float:
    values = fr_cost_values(row)
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
    regime_filter_bonus = 1.0 if filter_id != "none" else 0.0
    density3_ready = min(
        readiness(validation_density, DENSITY_FLOOR, 0.38),
        readiness(oos_density, DENSITY_FLOOR, 0.38),
        readiness(density, DENSITY_FLOOR, 0.38),
    )
    positive_dense_ready = min(
        density3_ready,
        readiness(validation_net, 0.0, 150.0),
        readiness(oos_net, 0.0, 150.0),
    )
    pf105_ready = min(density3_ready, readiness(oos_pf, 1.05, 0.18), readiness(min_pf, 1.00, 0.16))
    cost_scout_ready = min(readiness(oos_pf, OOS_PF_TARGET, 0.30), readiness(oos_cost09, 0.0, 220.0))
    validation_positive_density = validation_net > 0.0 and validation_density >= DENSITY_FLOOR and density >= DENSITY_FLOOR
    all_positive_density = validation_positive_density and oos_net > 0.0 and oos_density >= DENSITY_FLOOR
    low_density_cost_only = oos_pf >= OOS_PF_TARGET and oos_cost09 >= 0.0 and min_density < 2.90
    dense_negative = density3_ready >= 1.0 and (validation_net <= 0.0 or oos_net <= 0.0)
    strict_shape_bonus = 1.0 if fr_strict_success(row) else 0.0
    return (
        5200.0 * density3_ready
        + 7200.0 * positive_dense_ready
        + 4200.0 * pf105_ready
        + 1400.0 * cost_scout_ready
        + 1200.0 * regime_filter_bonus
        + 4200.0 * (1.0 if validation_positive_density else 0.0)
        + 6500.0 * (1.0 if all_positive_density else 0.0)
        + 1.45 * validation_net
        + 1.25 * oos_net
        + 0.88 * values["combined_net"]
        + 1700.0 * max(0.0, validation_pf - 1.0)
        + 2300.0 * max(0.0, oos_pf - 1.0)
        + 1050.0 * max(0.0, min_pf - 1.0)
        + 1.10 * validation_cost09
        + 1.65 * oos_cost09
        + 1.05 * values["combined_cost09_net"]
        + 1800.0 * min(min_density, 4.2)
        + 700.0 * min(validation_density, 5.0)
        + 640.0 * min(oos_density, 5.0)
        + 750.0 * max(0.0, PRESERVE_SHORT_SHARE_FLOOR - short_share)
        + 9200.0 * strict_shape_bonus
        - 9800.0 * (1.0 if low_density_cost_only else 0.0)
        - 4800.0 * (1.0 if dense_negative else 0.0)
        - 2600.0 * max(0.0, OOS_PF_TARGET - oos_pf)
        - 3600.0 * (1.0 if validation_net <= 0.0 else 0.0)
        - 2100.0 * (1.0 if oos_net <= 0.0 else 0.0)
        - 5.2 * max(0.0, -validation_cost09)
        - 5.6 * max(0.0, -oos_cost09)
        - 2.6 * max(0.0, -values["combined_cost09_net"] - 120.0)
        - 6400.0 * max(0.0, DENSITY_FLOOR - validation_density)
        - 6400.0 * max(0.0, DENSITY_FLOOR - oos_density)
        - 6800.0 * max(0.0, DENSITY_FLOOR - density)
        - 1800.0 * max(0.0, short_share - PRESERVE_SHORT_SHARE_FLOOR)
    )


def write_work_packet(parent: Mapping[str, Any]) -> None:
    fn.write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(옵시디언 실험 설계)",
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-model-validation(옵시디언 모델 검증)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "hypothesis": "FR density3 regime split repair(FR 밀도3 국면 분할 수리)가 고밀도 손실 행을 regime/session/side(국면/세션/방향)별로 나눠 양수 밀도3 후보를 회복할 수 있는지 시험합니다.",
            "preserve_conditions": ["density3_all_splits_count>0(전 분할 밀도3 수 0 초과)", "OOS PF125/cost0.9 scout clue(표본외 PF125/비용0.9 탐색 단서)"],
            "repair_conditions": ["validation_positive_density3_count>0(검증 양수 밀도3 수 0 초과)", "density3_all_splits_valpos_oospos_count>0(전 분할 양수 밀도3 수 0 초과)", "OOS PF>=1.05 before PF1.25(표본외 PF1.25 전 PF1.05 먼저 회복)"],
            "avoid": "low-density cost-only package review and threshold-only lowering(저밀도 비용 전용 패키지 검토와 임계값만 낮추기)",
            "parent_summary": {
                "selected_model_id": parent.get("selected_model_id"),
                "validation_positive_density3_count": parent.get("validation_positive_density3_count"),
                "density3_all_splits_count": parent.get("density3_all_splits_count"),
                "density3_all_splits_valpos_oospos_count": parent.get("density3_all_splits_valpos_oospos_count"),
                "oos_pf125_cost09_count": parent.get("oos_pf125_cost09_count"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    RUN364FS_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(
        RUN364FS_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "fs01_density3_regime_split_repair_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_validation_density": summary["selected_validation_trade_density"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_cost06_net": summary["selected_oos_cost06_net"],
                "selected_combined_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "selected_combined_short_share": summary["selected_combined_short_share"],
                "effect": "FS review(FS 검토)가 FR의 density3 regime split repair(밀도3 국면 분할 수리)가 package(패키지) 후보인지 실패 기억인지 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    fn.write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke(Python 프록시와 ONNX 스모크), no MT5(MT5 없음)"})
    fn.write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "FR density3 regime split repair(FR 밀도3 국면 분할 수리)가 국면/세션/방향 분리로 양수 밀도3을 찾는지 시험합니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    fn.write_json(DATA_RECEIPT, {**base, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp(UTC 모델 입력 타임스탬프)", "sample_scope": "US100 M5 Tier A proxy split(US100 M5 Tier A 프록시 분할)", "feature_label_boundary": "future_open only in labels(future_open은 라벨에만 사용)", "split_boundary": "chronological train/validation/OOS(시간순 학습/검증/표본외)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    fn.write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "target_and_label": "3-class next-open horizon direction(3분류 다음 시가 horizon 방향)", "split_method": "chronological holdout(시간순 홀드아웃)", "selection_metric": "FR score rewards dense positive regime split(FR 점수는 양수 고밀도 국면 분할을 보상)", "threshold_policy": "searched threshold and density target(탐색 임계값과 밀도 목표)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    fn.write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation/OOS net/PF/density {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']} and {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["regime filters(국면 필터)", "session split(세션 분할)", "side balance(방향 균형)"], "next_probe": NEXT_RUN_ID})
    fn.write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    fn.write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    fn.write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "FR 모델 단서를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364FR Density3 Regime Split Repair(밀도3 국면 분할 수리)

Created(생성): {final['created_at_utc']}

Action(행동): FQ failure memory(FQ 실패 기억)를 받아 regime/session/side split(국면/세션/방향 분할), density3 score(밀도3 점수), cost scout guard(비용 탐색 가드)를 학습했습니다.

Effect(효과): FP의 dense losing rows(고밀도 손실 행)가 섞임 문제인지 확인하고, validation positive density3(검증 양수 밀도3)를 되살릴 수 있는 하위 국면을 찾습니다.

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
    decision_doc = f"""# Decision(결정): stage364FR Density3 Regime Split Repair(밀도3 국면 분할 수리)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): FR model/label/score(모델/라벨/점수) 재시드를 실행하고 FS review(FS 검토)로 넘겼습니다.

Effect(효과): 고밀도 손실 행의 국면 분할 결과를 운영 주장 없이 다음 판정으로 보냅니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364FR__{RUN_ID}", f"\n- run364FR__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density3 regime split repair(밀도3 국면 분할 수리), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364FR__{RUN_ID}", f"\n<!-- run364FR__{RUN_ID} -->\n\n## run364FR Density3 Regime Split Repair(밀도3 국면 분할 수리)\n\nAction(행동): 고밀도 손실 행을 국면/세션/방향으로 분리해 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 패키지 가능성과 실패 경계를 검토합니다.\n")
    fn.append_text_once(STAGE_README, f"run364FR__{RUN_ID}", f"\n<!-- run364FR__{RUN_ID} -->\n## run364FR density3 regime split repair(밀도3 국면 분할 수리)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364FR` trained(학습 완료) density3 regime split repair(밀도3 국면 분할 수리). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost/side truth(비용/방향 진실): OOS cost0.6 net(표본외 비용0.6 순수익)은 `{final['selected_oos_cost06_net']}`이고, combined cost0.9/short share(합산 비용0.9/숏 비중)는 `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 FR 결과를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): FR density3 regime split repair(FR 밀도3 국면 분할 수리).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364FR__{RUN_ID}", f"\n<!-- run364FR__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed density3 regime split repair(밀도3 국면 분할 수리); strict candidates `{final['strict_candidate_count']}`; selected `{final['selected_model_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364FR__{RUN_ID}", f"\n<!-- run364FR__{RUN_ID} -->\n- `{RUN_ID}`: density3 regime split repair(밀도3 국면 분할 수리)를 학습했습니다. Effect(효과): FQ 실패 기억을 국면/세션/방향 분할로 공격했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        fn.append_text_once(NEGATIVE_REGISTER, f"run364FR__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364FR__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: density3 regime split repair(밀도3 국면 분할 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FS에서 실패 경계와 회수 단서를 분리합니다.\n")


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
        "question": "Can regime/session/side split turn density3 rows positive?(국면/세션/방향 분할이 밀도3 행을 양수로 바꿀 수 있는가?)",
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
                "kpi_scope": "FR density3 regime split repair(FR 밀도3 국면 분할 수리)",
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
                "run_type": "density3_regime_split_repair(밀도3 국면 분할 수리)",
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
                    "notes": "FR density3 regime split repair artifact(FR 밀도3 국면 분할 수리 산출물)",
                }
            )
    fn.append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def apply_fr_patch() -> None:
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
        "RUN364FO_QUEUE": RUN364FS_QUEUE,
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
    fn.fm = fq
    fn.validate_inputs = validate_inputs
    fn.input_manifest_rows = input_manifest_rows
    fn.full_label_spec = full_label_spec
    fn.fn_label_values = fr_label_values
    fn.fn_feature_sets = fr_feature_sets
    fn.fn_model_specs = fr_model_specs
    fn.fn_extra_mask = fr_extra_mask
    fn.fn_cost_values = fr_cost_values
    fn.fn_strict_success = fr_strict_success
    fn.fn_operational_stack = fr_operational_stack
    fn.fn_selection_score = fr_selection_score
    fn.write_work_packet = write_work_packet
    fn.write_queue = write_queue
    fn.write_receipts = write_receipts
    fn.write_docs = write_docs
    fn.write_ledgers = write_ledgers
    fn.write_artifact_registry = write_artifact_registry


def main() -> None:
    apply_fr_patch()
    fn.main()


if __name__ == "__main__":
    main()
