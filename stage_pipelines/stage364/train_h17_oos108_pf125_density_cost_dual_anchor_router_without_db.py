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

from stage_pipelines.stage364 import review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db as gm
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db as gl
from stage_pipelines.stage364 import train_h17_oos108_pf125_density_cost_floor_rejoin_without_db as gj


fn = gl.fn
et = gl.et
base = gl.base

GJ_FINAL_DECISION = gj.FINAL_DECISION
GJ_TRADE_SURFACE = gj.TRADE_SURFACE
GJ_SELECTED_CANDIDATE = gj.SELECTED_CANDIDATE
GJ_SELECTED_TRADE_TAPE = gj.SELECTED_TRADE_TAPE
GJ_COST_STRESS = gj.COST_STRESS
GL_FINAL_DECISION = gl.FINAL_DECISION
GL_TRADE_SURFACE = gl.TRADE_SURFACE
GL_SELECTED_CANDIDATE = gl.SELECTED_CANDIDATE
GL_SELECTED_TRADE_TAPE = gl.SELECTED_TRADE_TAPE
GL_COST_STRESS = gl.COST_STRESS

TODAY = "2026-06-07"
STAGE_ID = gl.STAGE_ID
STAGE_DIR = gl.STAGE_DIR
REVIEW_DIR = gl.REVIEW_DIR
SPEC_DIR = gl.SPEC_DIR
SELECTED_DIR = gl.SELECTED_DIR

RUN_NUMBER = "run364GN"
RUN_ID = "run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1"
PARENT_RUN_ID = gm.RUN_ID
NEXT_RUN_ID = "run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1"

STATUS_NO_STRICT = "completed_stage364GN_density_cost_dual_anchor_router_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364GN_density_cost_dual_anchor_router_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_density_cost_dual_anchor_router_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_density_cost_dual_anchor_router_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364GN_open_run364GO_density_cost_dual_anchor_router_review"
DECISION_STRICT = "stage364GN_open_run364GO_density_cost_dual_anchor_router_review"
CLAIM_BOUNDARY = (
    "research_development_density_cost_dual_anchor_router_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "gn_feature_audit.csv"
LABEL_SUMMARY = RUN_DIR / "gn_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "gn_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "gn_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_gn_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_gn_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_gn_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_gn_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_gn_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364GO_QUEUE = RUN_DIR / "gn_go_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364GN_density_cost_dual_anchor_router.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GN_density_cost_dual_anchor_router.md"
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

LABEL_SPECS = [
    {"label_id": "gn_cost_h2_m0p35", "horizon_m5": 2, "threshold_points": 0.35, "mode": "symmetric"},
    {"label_id": "gn_cost_h2_m0p30", "horizon_m5": 2, "threshold_points": 0.30, "mode": "symmetric"},
    {"label_id": "gn_density_h1_m0p40", "horizon_m5": 1, "threshold_points": 0.40, "mode": "symmetric"},
    {"label_id": "gn_density_h1_m0p42", "horizon_m5": 1, "threshold_points": 0.42, "mode": "symmetric"},
]
TARGET_DENSITIES = [1.90, 2.10, 2.30, 2.50, 2.70]
MARGINS = [-0.26, -0.21, -0.16, -0.11, -0.06]
HOUR_SETS = {
    "gn_cash_16_22": list(range(16, 23)),
    "gn_cost_anchor_16_21": list(range(16, 22)),
    "gn_density_addback_18_22": [18, 19, 20, 21, 22],
    "gn_router_core_17_21": list(range(17, 22)),
}
EXTRA_FILTERS = [
    "none",
    "gn_gj_cost_anchor_guard",
    "gn_gl_bad16_17_veto",
    "gn_dual_anchor_router_guard",
    "gn_late_quality_addback_guard",
]

INPUT_FILES = [
    gm.FINAL_DECISION,
    gm.GATE_AUDIT,
    gm.REVIEW_SUMMARY,
    gm.SURFACE_DIAGNOSTIC,
    gm.FAILURE_ATTRIBUTION,
    gm.PACKAGE_DECISION,
    gm.FAILURE_MEMORY,
    gm.RUN364GN_QUEUE,
    GJ_FINAL_DECISION,
    GJ_TRADE_SURFACE,
    GJ_SELECTED_CANDIDATE,
    GJ_SELECTED_TRADE_TAPE,
    GJ_COST_STRESS,
    GL_FINAL_DECISION,
    GL_TRADE_SURFACE,
    GL_SELECTED_CANDIDATE,
    GL_SELECTED_TRADE_TAPE,
    GL_COST_STRESS,
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
    RUN364GO_QUEUE,
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
    return gl.exists(path)


def rel(path: Path) -> str:
    return gl.rel(path)


def sha(path: Path) -> str:
    return gl.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gl.as_float(value, default)


def readiness(value: float, floor: float, span: float) -> float:
    return gl.readiness(value, floor, span)


def gn_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base_cols = list(feature_order)
    derived = et.dt.derived_features()
    price = [c for c in base_cols if any(token in c for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [c for c in base_cols if any(token in c for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [c for c in base_cols if any(token in c for token in ["cash", "minutes", "open", "close"])]
    behavior = [c for c in base_cols if any(token in c for token in ["trend", "momentum", "range", "body", "wick", "spread"])]
    return {
        "gn_dual_anchor_blend": list(dict.fromkeys(price + macro + session + behavior + derived)),
        "gn_gj_cost_anchor": list(dict.fromkeys(price + macro + session + derived)),
        "gn_gl_density_anchor": list(dict.fromkeys(price + session + behavior + macro + derived)),
    }


def gn_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et7_l12_n132",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(
                n_estimators=132,
                max_depth=7,
                min_samples_leaf=12,
                class_weight="balanced",
                random_state=961,
                n_jobs=1,
            ),
        ),
        (
            "et8_l16_n132",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(
                n_estimators=132,
                max_depth=8,
                min_samples_leaf=16,
                class_weight="balanced",
                random_state=962,
                n_jobs=1,
            ),
        ),
        (
            "rf8_l20_n132",
            "RandomForest(랜덤포레스트)",
            et.dt.dp.RandomForestClassifier(
                n_estimators=132,
                max_depth=8,
                min_samples_leaf=20,
                class_weight="balanced_subsample",
                random_state=963,
                n_jobs=1,
            ),
        ),
    ]


def gn_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = base.col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = base.col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = base.col(frame, "log_return_3", 0.0)
    vix_stress = base.col(frame, "vix_zscore_20", 0.0)
    range_ratio = base.col(frame, "range_5_over_20", 1.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "gn_gj_cost_anchor_guard":
        long_ok = (side == "long") & np.isin(hour, [16, 17, 19, 20]) & (breadth >= 0.30) & (range_ratio >= 0.46) & (vix_stress <= 2.08)
        short_ok = (side == "short") & np.isin(hour, [17, 18, 19]) & (vol_ratio >= 0.56) & ((breadth <= 0.68) | (log_return_3 < -0.00001))
        return mask & (long_ok | short_ok)
    if extra_filter == "gn_gl_bad16_17_veto":
        early_bad = (
            ((side == "short") & np.isin(hour, [16, 17]))
            | ((side == "long") & (hour == 16) & (breadth < 0.42))
            | ((side == "long") & (hour == 17) & (vix_stress > 2.05))
        )
        density_ok = np.isin(hour, [17, 18, 19, 20, 21, 22]) & (range_ratio >= 0.40)
        return mask & density_ok & ~early_bad
    if extra_filter == "gn_dual_anchor_router_guard":
        cost_long = (side == "long") & np.isin(hour, [16, 17, 19, 20]) & (breadth >= 0.32) & (range_ratio >= 0.48) & (vix_stress <= 2.05)
        cost_short = (side == "short") & np.isin(hour, [17, 18, 19]) & (vol_ratio >= 0.58) & ((breadth <= 0.66) | (log_return_3 < -0.000015))
        density_long = (side == "long") & np.isin(hour, [19, 21, 22]) & (breadth >= 0.30) & (vix_stress <= 2.15)
        density_short = (side == "short") & np.isin(hour, [18, 19, 22]) & (vol_ratio >= 0.52) & (breadth <= 0.72)
        return mask & (cost_long | cost_short | density_long | density_short)
    if extra_filter == "gn_late_quality_addback_guard":
        long_ok = (side == "long") & np.isin(hour, [19, 21, 22]) & (breadth >= 0.28) & (range_ratio >= 0.38) & (vix_stress <= 2.20)
        short_ok = (side == "short") & np.isin(hour, [18, 19, 22]) & (vol_ratio >= 0.50) & ((breadth <= 0.74) | (log_return_3 < -0.000005))
        return mask & (long_ok | short_ok)
    raise ValueError(f"unknown GN filter(알 수 없는 GN 필터): {extra_filter}")


def gn_selection_score(row: Mapping[str, Any]) -> float:
    values = base.gd_cost_values(row)
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
    oos_cost06 = as_float(values.get("oos_cost06_net"), oos_net - 0.30 * as_float(row.get("oos_trade_count")))
    combined_cost09 = values["combined_cost09_net"]
    filter_id = str(row.get("extra_filter", "none"))
    label_id = str(row.get("label_id", ""))

    density_anchor = min(
        readiness(validation_density, 2.05, 0.55),
        readiness(oos_density, 2.00, 0.55),
        readiness(density, 2.05, 0.55),
    )
    density_reexpand = min(
        readiness(validation_density, 2.30, 0.50),
        readiness(oos_density, 2.20, 0.50),
        readiness(density, 2.25, 0.50),
    )
    cost_anchor = min(
        readiness(oos_cost06, -6.0, 90.0),
        readiness(oos_cost09, -85.0, 190.0),
        readiness(combined_cost09, -210.0, 470.0),
    )
    cost_strong = min(
        readiness(oos_cost06, 0.0, 80.0),
        readiness(oos_cost09, -45.0, 170.0),
        readiness(combined_cost09, -120.0, 420.0),
    )
    profit_anchor = min(
        readiness(validation_net, 0.0, 120.0),
        readiness(oos_net, 0.0, 130.0),
        readiness(oos_pf, 1.05, 0.18),
        readiness(validation_pf, 1.00, 0.14),
    )
    router_balance = min(density_anchor, cost_anchor, profit_anchor)
    useful_router = (
        validation_net > 0.0
        and oos_net > 0.0
        and oos_pf >= 1.05
        and oos_cost06 >= -15.0
        and combined_cost09 >= -260.0
        and min_density >= 1.90
    )
    strong_router = (
        validation_net > 0.0
        and oos_net > 0.0
        and oos_pf >= 1.08
        and oos_cost06 >= -6.0
        and combined_cost09 >= -220.0
        and min_density >= 2.05
    )
    dense_cost_near = (
        validation_net > 0.0
        and oos_net > 0.0
        and oos_pf >= 1.05
        and oos_cost06 >= -18.0
        and min_density >= 2.20
    )
    density_only_collapse = min_density >= 2.20 and (oos_cost06 < -45.0 or combined_cost09 < -340.0)
    sparse_cost_only = oos_cost06 >= 0.0 and oos_pf >= 1.12 and min_density < 1.60
    validation_only = validation_net > 110.0 and (oos_net <= 0.0 or oos_pf < 1.0)
    cost_label_bonus = 1.0 if "cost_h2" in label_id else 0.0
    density_label_bonus = 1.0 if "density_h1" in label_id and min_density >= 2.05 else 0.0
    router_filter_bonus = 1.0 if filter_id in {"gn_gj_cost_anchor_guard", "gn_dual_anchor_router_guard"} else 0.0
    addback_filter_bonus = 1.0 if filter_id in {"gn_gl_bad16_17_veto", "gn_late_quality_addback_guard"} else 0.0

    return (
        24500.0 * router_balance
        + 18500.0 * density_anchor
        + 14200.0 * density_reexpand
        + 21500.0 * cost_anchor
        + 9800.0 * cost_strong
        + 16800.0 * profit_anchor
        + 13800.0 * (1.0 if useful_router else 0.0)
        + 9200.0 * (1.0 if strong_router else 0.0)
        + 6900.0 * (1.0 if dense_cost_near else 0.0)
        + 1100.0 * cost_label_bonus
        + 900.0 * density_label_bonus
        + 1300.0 * router_filter_bonus
        + 900.0 * addback_filter_bonus
        + 2.40 * validation_net
        + 3.25 * oos_net
        + 1.25 * values["combined_net"]
        + 2450.0 * max(0.0, validation_pf - 1.0)
        + 3900.0 * max(0.0, oos_pf - 1.0)
        + 1550.0 * max(0.0, min_pf - 1.0)
        + 1.30 * validation_cost09
        + 3.05 * oos_cost09
        + 5.10 * oos_cost06
        + 2.15 * combined_cost09
        + 3900.0 * min(min_density, 3.2)
        + 1250.0 * min(validation_density, 4.4)
        + 1600.0 * min(oos_density, 4.4)
        + 1350.0 * min(density, 4.4)
        + 560.0 * max(0.0, base.PRESERVE_SHORT_SHARE_FLOOR - short_share)
        + 15000.0 * (1.0 if base.gd_strict_success(row) else 0.0)
        - 13200.0 * (1.0 if density_only_collapse else 0.0)
        - 9800.0 * (1.0 if sparse_cost_only else 0.0)
        - 9000.0 * (1.0 if validation_only else 0.0)
        - 7600.0 * (1.0 if validation_net <= 0.0 else 0.0)
        - 8700.0 * (1.0 if oos_net <= 0.0 else 0.0)
        - 6100.0 * max(0.0, 1.04 - oos_pf)
        - 4700.0 * max(0.0, 1.00 - validation_pf)
        - 6200.0 * (1.0 if oos_cost06 < -25.0 else 0.0)
        - 3.2 * max(0.0, -validation_cost09 - 80.0)
        - 5.2 * max(0.0, -oos_cost09 - 105.0)
        - 2.7 * max(0.0, -combined_cost09 - 230.0)
        - 2200.0 * max(0.0, 1.90 - validation_density)
        - 2450.0 * max(0.0, 1.85 - oos_density)
        - 2300.0 * max(0.0, 1.90 - density)
        - 1850.0 * max(0.0, short_share - 0.86)
    )


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GN inputs(GN 입력 누락): " + ", ".join(missing))
    with fn.io_path(gm.FINAL_DECISION).open("r", encoding="utf-8-sig") as handle:
        parent = json.load(handle)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GM next_run_id mismatch(GM 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GM claim(금지된 GM 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gm.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GM gate audit(GM 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    for label, path in [("GJ", GJ_FINAL_DECISION), ("GL", GL_FINAL_DECISION)]:
        with fn.io_path(path).open("r", encoding="utf-8-sig") as handle:
            decision = json.load(handle)
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if decision.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"forbidden {label} claim(금지된 {label} 주장): {key}={decision.get(key)}")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GN density-cost dual-anchor router input(GN 밀도-비용 이중 앵커 라우터 입력)",
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
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate(범위 완료 게이트)",
                "kpi_contract_audit(KPI 계약 감사)",
                "skill_receipt_lint(스킬 영수증 점검)",
                "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            ],
            "hypothesis": "GJ cost anchor(GJ 비용 앵커)와 GL density anchor(GL 밀도 앵커)를 분리 라우팅하면 sparse cost-only(희소 비용 전용)와 dense cost-collapse(고밀도 비용 붕괴)의 왕복을 줄일 수 있습니다.",
            "decision_use": NEXT_RUN_ID,
            "comparison_baseline": "GJ cost-repaired sparse candidate(GJ 비용 수리 희소 후보) and GL dense cost-failed candidate(GL 고밀도 비용 실패 후보)",
            "control_variables": ["US100 M5", "chronological split(시간순 분할)", "Python proxy only(Python 프록시 전용)", "ONNX smoke only(ONNX 간이 검증만)", "no trade splitting(거래 쪼개기 없음)"],
            "changed_variables": ["h1/h2 dual labels(h1/h2 이중 라벨)", "router filters(라우터 필터)", "separate density and cost anchor score(분리된 밀도·비용 앵커 점수)"],
            "sample_scope": "Tier A US100 M5 model input, train/validation/OOS split(Tier A US100 M5 모델 입력, 학습/검증/표본외 분할)",
            "success_criteria": ["validation and OOS net positive(검증과 표본외 순수익 양수)", "min density near or above 2.0(최소 밀도 2.0 근처 이상)", "OOS cost0.6 near zero(표본외 비용0.6 0 근처)", "combined cost0.9 materially better than GL(합산 비용0.9가 GL보다 실질 개선)"],
            "failure_criteria": ["density-only cost collapse(밀도 전용 비용 붕괴)", "sparse cost-only recovery(희소 비용 전용 회복)", "validation-only optimization(검증 전용 최적화)"],
            "invalid_conditions": ["parent gate failure(상위 게이트 실패)", "lookahead leakage(미래참조 누수)", "missing required input(필수 입력 누락)"],
            "stop_conditions": ["no density-cost-near rows(밀도-비용 근접 행 없음)", "selected candidate fails OOS cost badly(선택 후보 표본외 비용 대폭 실패)", "authority evidence still missing(권위 근거 계속 누락)"],
            "evidence_plan": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(SELECTED_TRADE_TAPE), rel(ONNX_SMOKE_REPORT), rel(GATE_AUDIT), rel(FINAL_DECISION)],
            "parent_summary": {
                "gm_judgment": parent.get("judgment"),
                "gl_selected_density": parent.get("selected_combined_trade_density"),
                "gl_oos_cost06": parent.get("selected_oos_cost06_net"),
                "gl_combined_cost09": parent.get("selected_combined_cost09_net"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    RUN364GO_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(
        RUN364GO_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "go01_density_cost_dual_anchor_router_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_validation_density": summary["selected_validation_trade_density"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_cost06_net": summary["selected_oos_cost06_net"],
                "selected_combined_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "effect": "GO review(GO 검토)가 GN dual-anchor router(GN 이중 앵커 라우터)의 비용·밀도 균형을 판정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    fn.write_json(RUN_EVIDENCE_RECEIPT, {**common, "measurement_scope": "Python proxy with ONNX smoke(Python 프록시와 ONNX 간이 검증)", "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "parity_level": "P0_unverified(P0 미검증)"})
    fn.write_json(EXPERIMENT_RECEIPT, {**common, "hypothesis": "density-cost dual-anchor router(밀도-비용 이중 앵커 라우터)가 GJ 비용 단서와 GL 밀도 단서를 분리해 균형 후보를 찾는지 시험합니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    fn.write_json(DATA_RECEIPT, {**common, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC closed M5 bar timestamp(UTC 종가 5분봉 타임스탬프)", "sample_scope": "US100 M5 Tier A chronological split(US100 5분봉 Tier A 시간순 분할)", "feature_label_boundary": "future_open only in labels(future_open은 라벨에만 사용)", "split_boundary": "train/validation/OOS chronological(학습/검증/표본외 시간순)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    fn.write_json(MODEL_RECEIPT, {**common, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "target_and_label": "3-class next-open h1/h2 direction(3분류 다음 시가 h1/h2 방향)", "split_method": "chronological holdout(시간순 홀드아웃)", "selection_metric": "separate density anchor plus cost anchor router score(분리된 밀도 앵커와 비용 앵커 라우터 점수)", "threshold_policy": "searched threshold and density target(탐색 임계값과 밀도 목표)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    fn.write_json(ATTRIBUTION_RECEIPT, {**common, "observed_change": f"selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도) {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']} and {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["GJ cost-anchor labels(GJ 비용 앵커 라벨)", "GL density-anchor labels(GL 밀도 앵커 라벨)", "bad 16/17 density veto(나쁜 16/17시 밀도 차단)"], "next_probe": NEXT_RUN_ID})
    fn.write_json(JUDGMENT_RECEIPT, {**common, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    fn.write_json(LINEAGE_RECEIPT, {**common, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결됨)"})
    fn.write_json(CLAIM_RECEIPT, {**common, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GN Density-Cost Dual-Anchor Router(밀도-비용 이중 앵커 라우터)

Created(생성): {final['created_at_utc']}

Action(행동): GJ cost anchor(GJ 비용 앵커)와 GL density anchor(GL 밀도 앵커)를 같은 점수로 뭉개지 않고, label(라벨), filter(필터), score(점수)를 분리해 학습했습니다.

Effect(효과): sparse cost-only(희소 비용 전용)와 dense cost-collapse(고밀도 비용 붕괴) 사이의 왕복을 줄일 수 있는지 확인합니다.

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
    decision_doc = f"""# Decision(결정): stage364GN Density-Cost Dual-Anchor Router(밀도-비용 이중 앵커 라우터)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GN은 GJ 비용 앵커와 GL 밀도 앵커를 분리한 router score(라우터 점수)로 탐색했습니다.

Effect(효과): 결과는 GO review(GO 검토)로 넘겨 density-cost balance(밀도-비용 균형), cost stress(비용 압박), package decision(패키지 결정)을 판정합니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GN__{RUN_ID}", f"\n- run364GN__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density-cost dual-anchor router(밀도-비용 이중 앵커 라우터), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GN__{RUN_ID}", f"\n<!-- run364GN__{RUN_ID} -->\n\n## run364GN Density-Cost Dual-Anchor Router(밀도-비용 이중 앵커 라우터)\n\nAction(행동): GM 실패 기억을 받아 비용 앵커와 밀도 앵커를 분리한 라우터 탐색을 실행했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 GN 결과를 검토합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GN__{RUN_ID}", f"\n<!-- run364GN__{RUN_ID} -->\n## run364GN density-cost dual-anchor router(밀도-비용 이중 앵커 라우터)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GN` trained(학습 완료) density-cost dual-anchor router(밀도-비용 이중 앵커 라우터). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 그리고 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost truth(비용 진실): OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익)은 `{final['selected_oos_cost06_net']}` / `{final.get('selected_oos_cost09_net', '')}`이고, combined density/cost0.9(합산 밀도/비용0.9)는 `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 GN router(GN 라우터)를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): GN density-cost dual-anchor router(GN 밀도-비용 이중 앵커 라우터).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `{final['selected_oos_cost06_net']}` / `{final.get('selected_oos_cost09_net', '')}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GN__{RUN_ID}", f"\n<!-- run364GN__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed density-cost dual-anchor router(밀도-비용 이중 앵커 라우터); strict candidates(엄격 후보) `{final['strict_candidate_count']}`; selected(선택) `{final['selected_model_id']}`; next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GN__{RUN_ID}", f"\n<!-- run364GN__{RUN_ID} -->\n- `{RUN_ID}`: density-cost dual-anchor router(밀도-비용 이중 앵커 라우터)를 학습했습니다. Effect(효과): GJ 비용 앵커와 GL 밀도 앵커를 분리해 새 균형 단서를 찾습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        fn.append_text_once(NEGATIVE_REGISTER, f"run364GN__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364GN__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GO에서 비용·밀도 균형 후보와 실패 경계를 분리합니다.\n")


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
        "question": "Can a density-cost dual-anchor router reduce sparse cost-only and dense cost-collapse oscillation?(밀도-비용 이중 앵커 라우터가 희소 비용 전용과 고밀도 비용 붕괴 왕복을 줄일 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};validation_net={final['selected_validation_net']};oos_pf={final['selected_oos_profit_factor']};oos_cost06={final['selected_oos_cost06_net']};combined_density={final['selected_combined_trade_density']};combined_cost09={final['selected_combined_cost09_net']}",
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
                "kpi_scope": "GN density-cost dual-anchor router(GN 밀도-비용 이중 앵커 라우터)",
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
                "run_type": "density_cost_dual_anchor_router(밀도-비용 이중 앵커 라우터)",
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
                    "notes": "GN density-cost dual-anchor router artifact(GN 밀도-비용 이중 앵커 라우터 산출물)",
                }
            )
    fn.append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def patch_gl_module() -> None:
    replacements = {
        "gk": gm,
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
        "RUN364GM_QUEUE": RUN364GO_QUEUE,
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
        "gl_feature_sets": gn_feature_sets,
        "gl_model_specs": gn_model_specs,
        "gl_extra_mask": gn_extra_mask,
        "gl_selection_score": gn_selection_score,
        "write_work_packet": write_work_packet,
        "write_queue": write_queue,
        "write_receipts": write_receipts,
        "write_docs": write_docs,
        "write_ledgers": write_ledgers,
        "write_artifact_registry": write_artifact_registry,
    }
    for name, value in replacements.items():
        setattr(gl, name, value)


def main() -> None:
    patch_gl_module()
    gl.main()


if __name__ == "__main__":
    main()
