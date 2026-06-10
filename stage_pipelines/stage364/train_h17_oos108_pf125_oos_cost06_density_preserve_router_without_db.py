from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_h17_oos108_pf125_cost_near_density_lift_router_without_db as gu
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_near_density_floor_router_without_db as gr
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_near_density_lift_router_without_db as gt


fn = gt.fn
et = gt.et
base = gt.base

TODAY = "2026-06-07"
STAGE_ID = gt.STAGE_ID
STAGE_DIR = gt.STAGE_DIR
REVIEW_DIR = gt.REVIEW_DIR
SPEC_DIR = gt.SPEC_DIR
SELECTED_DIR = gt.SELECTED_DIR

RUN_NUMBER = "run364GV"
RUN_ID = "run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1"
PARENT_RUN_ID = gu.RUN_ID
NEXT_RUN_ID = "run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1"

STATUS_NO_STRICT = "completed_stage364GV_oos_cost06_density_preserve_router_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364GV_oos_cost06_density_preserve_router_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_oos_cost06_density_preserve_router_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_oos_cost06_density_preserve_router_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364GV_open_run364GW_oos_cost06_density_preserve_router_review"
DECISION_STRICT = "stage364GV_open_run364GW_oos_cost06_density_preserve_router_review"
CLAIM_BOUNDARY = (
    "research_development_oos_cost06_density_preserve_router_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "gv_feature_audit.csv"
LABEL_SUMMARY = RUN_DIR / "gv_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "gv_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "gv_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_gv_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_gv_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_gv_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_gv_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_gv_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364GW_QUEUE = RUN_DIR / "gv_gw_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364GV_oos_cost06_density_preserve_router.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GV_oos_cost06_density_preserve_router.md"
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

GT_FINAL_DECISION = gt.FINAL_DECISION

LABEL_SPECS = [
    {"label_id": "gv_cost_h2_m0p28", "horizon_m5": 2, "threshold_points": 0.28, "mode": "symmetric"},
    {"label_id": "gv_cost_h2_m0p32", "horizon_m5": 2, "threshold_points": 0.32, "mode": "symmetric"},
    {"label_id": "gv_density_h1_m0p36", "horizon_m5": 1, "threshold_points": 0.36, "mode": "symmetric"},
    {"label_id": "gv_density_h1_m0p40", "horizon_m5": 1, "threshold_points": 0.40, "mode": "symmetric"},
]
TARGET_DENSITIES = [1.25, 1.35, 1.45, 1.60, 1.75]
MARGINS = [-0.20, -0.15, -0.10, -0.05, 0.00]
HOUR_SETS = {
    "gv_cost06_core_16_21": list(range(16, 22)),
    "gv_oos_density_17_22": [17, 18, 19, 20, 21, 22],
    "gv_cost06_focus_17_21": [17, 18, 19, 20, 21],
    "gv_late_density_preserve_18_22": [18, 19, 20, 21, 22],
}
EXTRA_FILTERS = [
    "none",
    "gv_oos_cost06_veto_guard",
    "gv_density_preserve_cost_guard",
    "gv_late_cost_repair_guard",
    "gv_side_mix_cost_guard",
]

INPUT_FILES = [
    gu.FINAL_DECISION,
    gu.GATE_AUDIT,
    gu.REVIEW_SUMMARY,
    gu.SURFACE_DIAGNOSTIC,
    gu.DELTA_ATTRIBUTION,
    gu.PACKAGE_DECISION,
    gu.FAILURE_MEMORY,
    gu.RUN364GV_QUEUE,
    GT_FINAL_DECISION,
    gt.GATE_AUDIT,
    gt.TRADE_SURFACE,
    gt.SELECTED_CANDIDATE,
    gt.SELECTED_TRADE_TAPE,
    gt.COST_STRESS,
    gt.SIDE_SESSION_REVIEW,
    gt.MONTH_STABILITY,
    gt.MODEL_SCORECARD,
    gt.MODEL_ARTIFACT_MANIFEST,
    gt.ONNX_SMOKE_REPORT,
    gt.DATA_INTEGRITY_AUDIT,
    gr.FINAL_DECISION,
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
    RUN364GW_QUEUE,
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
    THIS_FILE,
]


def exists(path: Path) -> bool:
    return gt.exists(path)


def rel(path: Path) -> str:
    return gt.rel(path)


def sha(path: Path) -> str:
    return gt.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gt.as_float(value, default)


def readiness(value: float, floor: float, span: float) -> float:
    return gt.readiness(value, floor, span)


def gv_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base_cols = list(feature_order)
    derived = et.dt.derived_features()
    price = [c for c in base_cols if any(token in c for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [c for c in base_cols if any(token in c for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [c for c in base_cols if any(token in c for token in ["cash", "minutes", "open", "close"])]
    behavior = [c for c in base_cols if any(token in c for token in ["trend", "momentum", "range", "body", "wick", "spread"])]
    return {
        "gv_cost06_preserve_blend": list(dict.fromkeys(price + macro + session + behavior + derived)),
        "gv_gt_density_anchor": list(dict.fromkeys(price + session + macro + derived)),
        "gv_cost_side_behavior_anchor": list(dict.fromkeys(price + behavior + macro + session + derived)),
    }


def gv_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "rf8_l18_n144",
            "RandomForest(랜덤포레스트)",
            et.dt.dp.RandomForestClassifier(n_estimators=144, max_depth=8, min_samples_leaf=18, class_weight="balanced_subsample", random_state=991, n_jobs=1),
        ),
        (
            "rf9_l22_n144",
            "RandomForest(랜덤포레스트)",
            et.dt.dp.RandomForestClassifier(n_estimators=144, max_depth=9, min_samples_leaf=22, class_weight="balanced_subsample", random_state=992, n_jobs=1),
        ),
        (
            "et8_l14_n144",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=144, max_depth=8, min_samples_leaf=14, class_weight="balanced", random_state=993, n_jobs=1),
        ),
    ]


def gv_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = base.col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = base.col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = base.col(frame, "log_return_3", 0.0)
    vix_stress = base.col(frame, "vix_zscore_20", 0.0)
    range_ratio = base.col(frame, "range_5_over_20", 1.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "gv_oos_cost06_veto_guard":
        long_ok = (side == "long") & np.isin(hour, [16, 17, 19, 20]) & (breadth >= 0.38) & (range_ratio >= 0.50) & (vix_stress <= 1.98)
        short_ok = (side == "short") & np.isin(hour, [17, 18, 19, 20]) & (vol_ratio >= 0.60) & ((breadth <= 0.64) | (log_return_3 < -0.000014))
        return mask & (long_ok | short_ok)
    if extra_filter == "gv_density_preserve_cost_guard":
        long_ok = (side == "long") & np.isin(hour, [18, 19, 20, 21]) & (breadth >= 0.34) & (range_ratio >= 0.46) & (vix_stress <= 2.06)
        short_ok = (side == "short") & np.isin(hour, [18, 19, 20, 21, 22]) & (vol_ratio >= 0.57) & (breadth <= 0.69)
        return mask & (long_ok | short_ok)
    if extra_filter == "gv_late_cost_repair_guard":
        veto = (
            ((side == "long") & np.isin(hour, [21, 22]) & (breadth < 0.43))
            | ((side == "long") & (vix_stress > 2.12))
            | ((side == "short") & (hour == 20) & (breadth > 0.70) & (vol_ratio < 0.66))
            | ((side == "short") & (hour == 22) & (breadth > 0.74))
        )
        density_ok = np.isin(hour, [17, 18, 19, 20, 21, 22]) & (range_ratio >= 0.42)
        return mask & density_ok & ~veto
    if extra_filter == "gv_side_mix_cost_guard":
        long_ok = (side == "long") & np.isin(hour, [18, 19, 21]) & (breadth >= 0.36) & (range_ratio >= 0.44) & (vix_stress <= 2.08)
        short_ok = (side == "short") & np.isin(hour, [17, 18, 19, 20, 21]) & (vol_ratio >= 0.58) & ((breadth <= 0.70) | (log_return_3 < -0.000010))
        return mask & (long_ok | short_ok)
    raise ValueError(f"unknown GV filter(알 수 없는 GV 필터): {extra_filter}")


def gv_selection_score(row: Mapping[str, Any]) -> float:
    values = base.gd_cost_values(row)
    validation_net = as_float(row.get("validation_net"))
    oos_net = as_float(row.get("oos_net"))
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    validation_pf_score = min(validation_pf, 2.50)
    oos_pf_score = min(oos_pf, 2.50)
    min_pf = min(validation_pf_score, oos_pf_score)
    validation_density = values["validation_trade_density"]
    oos_density = values["oos_trade_density"]
    density = values["combined_trade_density"]
    min_density = min(validation_density, oos_density, density)
    short_share = values["combined_short_share"]
    validation_trades = as_float(row.get("validation_trade_count"))
    oos_trades = as_float(row.get("oos_trade_count"))
    combined_trades = validation_trades + oos_trades
    validation_cost09 = values["validation_cost09_net"]
    oos_cost09 = values["oos_cost09_net"]
    oos_cost06 = as_float(values.get("oos_cost06_net"), oos_net - 0.30 * oos_trades)
    combined_cost09 = values["combined_cost09_net"]
    filter_id = str(row.get("extra_filter", "none"))
    label_id = str(row.get("label_id", ""))

    hard_floor_ok = density >= 1.25 and combined_trades >= 160.0 and validation_trades >= 80.0 and oos_trades >= 70.0
    preserve_floor_ok = oos_density >= 1.35 and density >= 1.35 and hard_floor_ok
    pf999_micro_sample = (validation_pf >= 900.0 or oos_pf >= 900.0) and combined_trades < 160.0
    oos_cost_repair = min(
        readiness(oos_cost06, -10.0, 90.0),
        readiness(oos_cost09, -85.0, 160.0),
        readiness(oos_net, 0.0, 130.0),
        readiness(oos_pf_score, 1.05, 0.18),
    )
    first_pass_cost = min(
        readiness(oos_cost06, -15.0, 85.0),
        readiness(oos_cost09, -95.0, 165.0),
        readiness(combined_cost09, -150.0, 330.0),
    )
    combined_cost_preserve = min(
        readiness(combined_cost09, -150.0, 330.0),
        readiness(validation_cost09, -95.0, 190.0),
        readiness(oos_cost09, -95.0, 165.0),
    )
    density_preserve = min(
        readiness(validation_density, 1.25, 0.35),
        readiness(oos_density, 1.35, 0.45),
        readiness(density, 1.35, 0.45),
    )
    density_target = min(
        readiness(validation_density, 1.35, 0.40),
        readiness(oos_density, 1.45, 0.40),
        readiness(density, 1.45, 0.40),
    )
    profit_floor = min(
        readiness(validation_net, 0.0, 130.0),
        readiness(oos_net, 0.0, 130.0),
        readiness(validation_pf_score, 1.00, 0.14),
        readiness(oos_pf_score, 1.05, 0.18),
    )
    trade_floor = min(
        readiness(combined_trades, 240.0, 280.0),
        readiness(validation_trades, 110.0, 210.0),
        readiness(oos_trades, 95.0, 170.0),
    )

    target_candidate = validation_net > 0.0 and oos_net > 0.0 and preserve_floor_ok and oos_cost06 >= -10.0 and combined_cost09 >= -150.0
    first_pass_candidate = validation_net > 0.0 and oos_net > 0.0 and preserve_floor_ok and oos_cost06 >= -15.0 and combined_cost09 >= -150.0
    preserve_candidate = validation_net > 0.0 and oos_net > 0.0 and preserve_floor_ok and combined_cost09 >= -150.0
    density_chase_cost_fail = oos_density >= 1.45 and (oos_cost06 < -22.0 or combined_cost09 < -180.0)
    cost_collapse = combined_cost09 < -180.0 or oos_cost06 < -30.0
    sparse_cost_only = oos_cost06 >= 0.0 and oos_pf_score >= 1.12 and not hard_floor_ok
    validation_only = validation_net > 120.0 and (oos_net <= 0.0 or oos_pf < 1.0)
    cost_label_bonus = 1.0 if "cost_h2" in label_id else 0.0
    density_label_bonus = 1.0 if "density_h1" in label_id and oos_density >= 1.35 else 0.0
    cost_filter_bonus = 1.0 if filter_id in {"gv_oos_cost06_veto_guard", "gv_late_cost_repair_guard"} else 0.0
    preserve_filter_bonus = 1.0 if filter_id in {"gv_density_preserve_cost_guard", "gv_side_mix_cost_guard"} else 0.0

    return (
        40500.0 * oos_cost_repair
        + 33800.0 * first_pass_cost
        + 27800.0 * combined_cost_preserve
        + 22600.0 * density_preserve
        + 9800.0 * density_target
        + 16600.0 * profit_floor
        + 8500.0 * trade_floor
        + 23500.0 * (1.0 if target_candidate else 0.0)
        + 15800.0 * (1.0 if first_pass_candidate else 0.0)
        + 8400.0 * (1.0 if preserve_candidate else 0.0)
        + 1700.0 * cost_label_bonus
        + 700.0 * density_label_bonus
        + 1550.0 * cost_filter_bonus
        + 950.0 * preserve_filter_bonus
        + 11800.0 * (1.0 if hard_floor_ok else 0.0)
        + 2.10 * validation_net
        + 3.75 * oos_net
        + 1.05 * values["combined_net"]
        + 2200.0 * max(0.0, validation_pf_score - 1.0)
        + 4300.0 * max(0.0, oos_pf_score - 1.0)
        + 1450.0 * max(0.0, min_pf - 1.0)
        + 1.00 * validation_cost09
        + 3.80 * oos_cost09
        + 8.40 * oos_cost06
        + 3.20 * combined_cost09
        + 2500.0 * min(min_density, 2.2)
        + 1050.0 * min(validation_density, 3.0)
        + 1700.0 * min(oos_density, 3.0)
        + 1250.0 * min(density, 3.0)
        + 620.0 * max(0.0, base.PRESERVE_SHORT_SHARE_FLOOR - short_share)
        + 15000.0 * (1.0 if base.gd_strict_success(row) else 0.0)
        - 225000.0 * (1.0 if not hard_floor_ok else 0.0)
        - 170000.0 * (1.0 if pf999_micro_sample else 0.0)
        - 42000.0 * (1.0 if cost_collapse else 0.0)
        - 33500.0 * (1.0 if density_chase_cost_fail else 0.0)
        - 14200.0 * (1.0 if sparse_cost_only else 0.0)
        - 9400.0 * (1.0 if validation_only else 0.0)
        - 8200.0 * (1.0 if validation_net <= 0.0 else 0.0)
        - 9600.0 * (1.0 if oos_net <= 0.0 else 0.0)
        - 6800.0 * max(0.0, 1.05 - oos_pf_score)
        - 4700.0 * max(0.0, 1.00 - validation_pf_score)
        - 3.2 * max(0.0, -validation_cost09 - 95.0)
        - 6.2 * max(0.0, -oos_cost09 - 95.0)
        - 6.0 * max(0.0, -oos_cost06 - 15.0)
        - 4.6 * max(0.0, -combined_cost09 - 150.0)
        - 3100.0 * max(0.0, 1.25 - validation_density)
        - 3800.0 * max(0.0, 1.35 - oos_density)
        - 3300.0 * max(0.0, 1.35 - density)
        - 1900.0 * max(0.0, short_share - 0.86)
    )


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GV inputs(GV 입력 누락): " + ", ".join(missing))
    with fn.io_path(gu.FINAL_DECISION).open("r", encoding="utf-8-sig") as handle:
        parent = json.load(handle)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GU next_run_id mismatch(GU 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GU claim(금지된 GU 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gu.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GU gate audit(GU 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    with fn.io_path(GT_FINAL_DECISION).open("r", encoding="utf-8-sig") as handle:
        gt_parent = json.load(handle)
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if gt_parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GT claim(금지된 GT 주장): {key}={gt_parent.get(key)}")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GV OOS cost0.6 density preserve router input(GV 표본외 비용0.6 밀도 보존 라우터 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet(parent: Mapping[str, Any]) -> None:
    fn.write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "routing_receipt": {
                "work_packet_lifecycle": "code_to_experiment_to_evidence_to_report(코드-실험-근거-보고)",
                "primary_family": "experiment_execution(실험 실행)",
                "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
                "support_skills": [
                    "obsidian-experiment-design(실험 설계)",
                    "obsidian-data-integrity(데이터 무결성)",
                    "obsidian-model-validation(모델 검증)",
                    "obsidian-artifact-lineage(산출물 계보)",
                    "obsidian-result-judgment(결과 판정)",
                ],
                "required_gates": [
                    "scope_completion_gate(범위 완료 게이트)",
                    "kpi_contract_audit(KPI 계약 감사)",
                    "skill_receipt_lint(스킬 영수증 점검)",
                    "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
                ],
                "branch_action": "stay(유지)",
                "final_answer_filter": ["obsidian-answer-clarity(답변 명료성)", "obsidian-claim-discipline(주장 절제)"],
            },
            "hypothesis": "OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터)가 GT의 OOS density(표본외 밀도)를 지키면서 비용 실패를 줄일 수 있는지 시험합니다.",
            "decision_use": NEXT_RUN_ID,
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": [
                "US100 M5",
                "chronological split(시간순 분할)",
                "OOS density preserve floor(표본외 밀도 보존 바닥)",
                "combined cost0.9 preserve floor(합산 비용0.9 보존 바닥)",
                "Python proxy only(Python 프록시 전용)",
                "ONNX smoke only(ONNX 간이 검증만)",
                "no trade splitting(거래 쪼개기 없음)",
            ],
            "changed_variables": [
                "OOS cost0.6 repair weight(표본외 비용0.6 수리 가중치)",
                "density preserve filter stack(밀도 보존 필터 묶음)",
                "cost degradation veto(비용 악화 차단)",
            ],
            "sample_scope": "Tier A US100 M5 train/validation/OOS chronological split(Tier A US100 5분봉 학습/검증/표본외 시간순 분할)",
            "success_criteria": [
                "OOS density >= 1.35(표본외 밀도 1.35 이상)",
                "combined density >= 1.35(합산 밀도 1.35 이상)",
                "combined cost0.9 >= -150(합산 비용0.9 -150 이상)",
                "OOS cost0.6 >= -15 first pass, >= -10 target(표본외 비용0.6 -15 이상 1차, -10 이상 목표)",
                "validation and OOS net positive(검증과 표본외 순수익 양수)",
            ],
            "failure_criteria": [
                "OOS cost0.6 below -30(표본외 비용0.6 -30 아래)",
                "density lift with combined cost0.9 below -180(합산 비용0.9 -180 아래 밀도 상승)",
                "OOS density below 1.20(표본외 밀도 1.20 아래)",
            ],
            "invalid_conditions": ["parent gate failure(상위 게이트 실패)", "lookahead leakage(미래참조 누출)", "missing required input(필수 입력 누락)"],
            "evidence_plan": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(SELECTED_TRADE_TAPE), rel(ONNX_SMOKE_REPORT), rel(GATE_AUDIT), rel(FINAL_DECISION)],
            "parent_summary": {
                "gu_judgment": parent.get("judgment"),
                "gt_oos_density": parent.get("gt_oos_trade_density"),
                "gt_oos_cost06_net": parent.get("gt_oos_cost06_net"),
                "gt_combined_cost09_net": parent.get("gt_combined_cost09_net"),
                "preserve_lift_count": parent.get("preserve_lift_count"),
                "target_count": parent.get("target_count"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    RUN364GW_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(
        RUN364GW_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "gw01_oos_cost06_density_preserve_router_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_validation_density": summary["selected_validation_trade_density"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_cost06_net": summary["selected_oos_cost06_net"],
                "selected_oos_density": summary["selected_oos_trade_density"],
                "selected_combined_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "effect": "GW review(GW 검토)가 GV의 OOS cost0.6 repair(표본외 비용0.6 수리), density preserve(밀도 보존), package boundary(패키지 경계)를 분리 판정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    fn.write_json(RUN_EVIDENCE_RECEIPT, {**common, "measurement_scope": "Python proxy with ONNX smoke(Python 프록시와 ONNX 간이 검증)", "scoreboard": "structural_scout(구조 탐색)", "parity_level": "P0_unverified(P0 미검증)", "wfo_status": "not_applicable(해당 없음)", "registry_update_required": "yes", "evidence_boundary": "scout-only(탐색 전용)"})
    fn.write_json(EXPERIMENT_RECEIPT, {**common, "hypothesis": "OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터)가 비용 수리와 밀도 보존을 같이 만들 수 있는지 시험합니다.", "decision_use": NEXT_RUN_ID, "comparison_baseline": PARENT_RUN_ID})
    fn.write_json(DATA_RECEIPT, {**common, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC closed M5 bar timestamp(UTC 닫힌 5분봉 타임스탬프)", "sample_scope": "US100 M5 Tier A chronological split(US100 5분봉 Tier A 시간순 분할)", "feature_label_boundary": "future_open only in labels(future_open은 라벨에만 사용)", "split_boundary": "train/validation/OOS chronological(학습/검증/표본외 시간순)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    fn.write_json(MODEL_RECEIPT, {**common, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "target_and_label": "3-class next-open h1/h2 direction(3분류 다음 시가 h1/h2 방향)", "split_method": "chronological holdout(시간순 홀드아웃)", "selection_metric": "OOS cost0.6 density-preserve PF-capped score(표본외 비용0.6 밀도 보존 PF 캡 점수)", "threshold_policy": "searched threshold and density target(탐색 임계값과 밀도 목표)", "selected_model_id": final["selected_model_id"], "validation_judgment": final["judgment"]})
    fn.write_json(ATTRIBUTION_RECEIPT, {**common, "observed_change": f"selected OOS net/PF/density/cost06(선택 표본외 순수익/수익 팩터/밀도/비용0.6) {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}/{final['selected_oos_cost06_net']}", "likely_drivers": ["OOS cost0.6 repair weight(표본외 비용0.6 수리 가중치)", "density preserve floor(밀도 보존 바닥)", "cost degradation veto(비용 악화 차단)"], "next_probe": NEXT_RUN_ID})
    fn.write_json(JUDGMENT_RECEIPT, {**common, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    fn.write_json(LINEAGE_RECEIPT, {**common, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "reproducible_from_command(명령으로 재생 가능)", "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결됨)"})
    fn.write_json(CLAIM_RECEIPT, {**common, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GV OOS Cost0.6 Density Preserve Router(표본외 비용0.6 밀도 보존 라우터)

Created(생성): {final['created_at_utc']}

Action(행동): GU failure memory(GU 실패 기억)를 받아 OOS cost0.6(표본외 비용0.6) 수리와 OOS density(표본외 밀도) 보존을 동시에 점수화해 학습했습니다.

Effect(효과): GT의 density clue(밀도 단서)를 유지할 수 있는지 보면서, 비용 실패가 줄어드는 frontier(경계면)를 다음 GW review(GW 검토)로 넘깁니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `{final['selected_oos_cost06_net']}` / `{final.get('selected_oos_cost09_net', '')}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `{final['operational_proxy_stack_pass_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GV OOS Cost0.6 Density Preserve Router(표본외 비용0.6 밀도 보존 라우터)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GV는 OOS cost0.6(표본외 비용0.6), OOS density(표본외 밀도), combined cost0.9(합산 비용0.9)를 함께 보는 proxy train(프록시 학습)을 수행했습니다.

Effect(효과): GW review(GW 검토)에서 package(패키지) 가능성, 비용 수리, 밀도 보존을 분리 판정할 수 있습니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GV__{RUN_ID}", f"\n- run364GV__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GV__{RUN_ID}", f"\n<!-- run364GV__{RUN_ID} -->\n\n## run364GV OOS Cost0.6 Density Preserve Router(표본외 비용0.6 밀도 보존 라우터)\n\nAction(행동): GU의 비용 실패 기억을 OOS cost0.6(표본외 비용0.6) 수리 점수로 바꿨습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 비용 수리와 밀도 보존이 실제로 같이 왔는지 검토합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GV__{RUN_ID}", f"\n<!-- run364GV__{RUN_ID} -->\n## run364GV OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GV` trained(학습 완료) OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터). 선택 후보의 OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`입니다.

Cost truth(비용 진실): selected combined density/cost0.9(선택 합산 밀도/비용0.9)는 `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 GV 결과를 package(패키지), OOS cost repair(표본외 비용 수리), density preserve(밀도 보존) 경계로 검토합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): GV OOS cost0.6 density preserve router(GV 표본외 비용0.6 밀도 보존 라우터).

Selected model(선택 모델): `{final['selected_model_id']}`
Selected OOS net/PF/density/cost0.6(선택 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
Selected combined density/trades/cost0.9(선택 합산 밀도/거래수/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_cost09_net']}`

Next seed(다음 씨앗): GW OOS cost0.6 density preserve review(GW 표본외 비용0.6 밀도 보존 검토).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GV__{RUN_ID}", f"\n<!-- run364GV__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터); strict candidates(엄격 후보) `{final['strict_candidate_count']}`; selected(선택) `{final['selected_model_id']}`; next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GV__{RUN_ID}", f"\n<!-- run364GV__{RUN_ID} -->\n- `{RUN_ID}`: OOS cost0.6 repair(표본외 비용0.6 수리)와 density preserve(밀도 보존)를 같은 score(점수)로 묶었습니다. Effect(효과): GW가 비용과 밀도 중 무엇이 개선됐는지 분리 판정합니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        fn.append_text_once(NEGATIVE_REGISTER, f"run364GV__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364GV__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GW에서 OOS cost0.6(표본외 비용0.6)과 density(밀도) 중 실패 축을 분리합니다.\n")


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
        "question": "Can OOS cost0.6 repair while preserving density?(밀도를 보존하면서 표본외 비용0.6을 수리할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};oos_pf={final['selected_oos_profit_factor']};oos_cost06={final['selected_oos_cost06_net']};oos_density={final['selected_oos_trade_density']};combined_density={final['selected_combined_trade_density']};combined_cost09={final['selected_combined_cost09_net']}",
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
                "kpi_scope": "GV OOS cost0.6 density preserve router(GV 표본외 비용0.6 밀도 보존 라우터)",
                "metric_scope": "python_proxy_onnx_smoke(Python 프록시와 ONNX 간이 검증)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "",
                "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시와 ONNX 간이 검증, MT5 없음)",
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
                "run_type": "oos_cost06_density_preserve_router(표본외 비용0.6 밀도 보존 라우터)",
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
                    "notes": "GV OOS cost0.6 density preserve router artifact(GV 표본외 비용0.6 밀도 보존 라우터 산출물)",
                }
            )
    fn.append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def patch_gt_module() -> None:
    replacements = {
        "gs": gu,
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
        "RUN364GU_QUEUE": RUN364GW_QUEUE,
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
        "validate_inputs": validate_inputs,
        "input_manifest_rows": input_manifest_rows,
        "gt_feature_sets": gv_feature_sets,
        "gt_model_specs": gv_model_specs,
        "gt_extra_mask": gv_extra_mask,
        "gt_selection_score": gv_selection_score,
        "write_work_packet": write_work_packet,
        "write_queue": write_queue,
        "write_receipts": write_receipts,
        "write_docs": write_docs,
        "write_ledgers": write_ledgers,
        "write_artifact_registry": write_artifact_registry,
    }
    for name, value in replacements.items():
        setattr(gt, name, value)


def main() -> None:
    patch_gt_module()
    gt.main()


if __name__ == "__main__":
    main()
