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

from stage_pipelines.stage364 import review_h17_oos108_pf125_density_cost_floor_rejoin_without_db as gk
from stage_pipelines.stage364 import train_h17_oos108_pf125_density_cost_floor_rejoin_without_db as gj


fn = gj.fn
et = gj.et
base = gj.gh

TODAY = "2026-06-07"
STAGE_ID = gj.STAGE_ID
STAGE_DIR = gj.STAGE_DIR
REVIEW_DIR = gj.REVIEW_DIR
SPEC_DIR = gj.SPEC_DIR
SELECTED_DIR = gj.SELECTED_DIR

RUN_NUMBER = "run364GL"
RUN_ID = "run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1"
PARENT_RUN_ID = gk.RUN_ID
NEXT_RUN_ID = "run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1"

STATUS_NO_STRICT = "completed_stage364GL_cost_repaired_density_reexpand_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364GL_cost_repaired_density_reexpand_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_cost_repaired_density_reexpand_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_cost_repaired_density_reexpand_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364GL_open_run364GM_cost_repaired_density_reexpand_review"
DECISION_STRICT = "stage364GL_open_run364GM_cost_repaired_density_reexpand_review"
CLAIM_BOUNDARY = (
    "research_development_cost_repaired_density_reexpand_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "gl_feature_audit.csv"
LABEL_SUMMARY = RUN_DIR / "gl_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "gl_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "gl_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_gl_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_gl_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_gl_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_gl_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_gl_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364GM_QUEUE = RUN_DIR / "gl_gm_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364GL_cost_repaired_density_reexpand.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GL_cost_repaired_density_reexpand.md"
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
    {"label_id": "gl_sym_h1_m0p30", "horizon_m5": 1, "threshold_points": 0.30, "mode": "symmetric"},
    {"label_id": "gl_sym_h1_m0p35", "horizon_m5": 1, "threshold_points": 0.35, "mode": "symmetric"},
    {"label_id": "gl_sym_h1_m0p40", "horizon_m5": 1, "threshold_points": 0.40, "mode": "symmetric"},
    {
        "label_id": "gl_asym_h1_l0p35_s0p70",
        "horizon_m5": 1,
        "threshold_points": 0.50,
        "long_threshold_points": 0.35,
        "short_threshold_points": 0.70,
        "mode": "asymmetric",
    },
]
TARGET_DENSITIES = [2.20, 2.40, 2.60, 2.80, 3.00, 3.20]
MARGINS = [-0.24, -0.20, -0.16, -0.12, -0.08, -0.04]
HOUR_SETS = {
    "gl_density_reexpand_13_22": list(range(13, 23)),
    "gl_cost_guard_13_21": list(range(13, 22)),
    "gl_open_core_14_21": list(range(14, 22)),
    "gl_no_late_13_20": list(range(13, 21)),
}
EXTRA_FILTERS = [
    "none",
    "gl_h1_density_cost_guard",
    "gl_cost_repair_preserve_guard",
    "gl_late_loss_veto_guard",
    "gl_short_balance_density_guard",
]

INPUT_FILES = [
    gk.FINAL_DECISION,
    gk.GATE_AUDIT,
    gk.REVIEW_SUMMARY,
    gk.SURFACE_DIAGNOSTIC,
    gk.FAILURE_ATTRIBUTION,
    gk.PACKAGE_DECISION,
    gk.FAILURE_MEMORY,
    gk.RUN364GL_QUEUE,
    gj.FINAL_DECISION,
    gj.GATE_AUDIT,
    gj.TRADE_SURFACE,
    gj.SELECTED_CANDIDATE,
    gj.SELECTED_TRADE_TAPE,
    gj.COST_STRESS,
    gj.SIDE_SESSION_REVIEW,
    gj.MONTH_STABILITY,
    gj.MODEL_SCORECARD,
    gj.MODEL_ARTIFACT_MANIFEST,
    gj.ONNX_SMOKE_REPORT,
    gj.DATA_INTEGRITY_AUDIT,
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
    RUN364GM_QUEUE,
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
    return gj.exists(path)


def rel(path: Path) -> str:
    return gj.rel(path)


def sha(path: Path) -> str:
    return gj.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gj.as_float(value, default)


def readiness(value: float, floor: float, span: float) -> float:
    return gj.readiness(value, floor, span)


def gl_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base_cols = list(feature_order)
    derived = et.dt.derived_features()
    price = [c for c in base_cols if any(token in c for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [c for c in base_cols if any(token in c for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [c for c in base_cols if any(token in c for token in ["cash", "minutes", "open", "close"])]
    behavior = [c for c in base_cols if any(token in c for token in ["trend", "momentum", "range", "body", "wick", "spread"])]
    return {
        "gl_all72": list(dict.fromkeys(base_cols + derived)),
        "gl_density_cost_blend": list(dict.fromkeys(price + macro + session + behavior + derived)),
        "gl_h1_session_regime": list(dict.fromkeys(price + macro + session + derived)),
    }


def gl_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et7_l10_n132",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=132, max_depth=7, min_samples_leaf=10, class_weight="balanced", random_state=951, n_jobs=1),
        ),
        (
            "et8_l14_n132",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=132, max_depth=8, min_samples_leaf=14, class_weight="balanced", random_state=952, n_jobs=1),
        ),
        (
            "rf8_l18_n132",
            "RandomForest(랜덤포레스트)",
            et.dt.dp.RandomForestClassifier(n_estimators=132, max_depth=8, min_samples_leaf=18, class_weight="balanced_subsample", random_state=953, n_jobs=1),
        ),
    ]


def gl_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = base.col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = base.col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = base.col(frame, "log_return_3", 0.0)
    vix_stress = base.col(frame, "vix_zscore_20", 0.0)
    range_ratio = base.col(frame, "range_5_over_20", 1.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "gl_h1_density_cost_guard":
        long_ok = (side == "long") & np.isin(hour, [13, 14, 16, 17, 18, 19, 20, 21]) & (breadth >= 0.24) & (range_ratio >= 0.42) & (vix_stress <= 2.18)
        short_ok = (side == "short") & np.isin(hour, [15, 16, 17, 18, 19, 20, 21]) & (vol_ratio >= 0.52) & ((breadth <= 0.70) | (log_return_3 < -0.000005))
        return mask & (long_ok | short_ok)
    if extra_filter == "gl_cost_repair_preserve_guard":
        long_ok = (side == "long") & np.isin(hour, [14, 16, 17, 18, 19, 20]) & (breadth >= 0.30) & (range_ratio >= 0.48) & (vix_stress <= 2.02)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18, 20, 21]) & (vol_ratio >= 0.57) & ((breadth <= 0.66) | (log_return_3 < -0.000015))
        return mask & (long_ok | short_ok)
    if extra_filter == "gl_late_loss_veto_guard":
        veto = (
            ((side == "long") & np.isin(hour, [21, 22]) & (breadth < 0.48))
            | ((side == "long") & (vix_stress > 2.25))
            | ((side == "short") & (hour == 16) & (breadth > 0.63))
            | ((side == "short") & (hour == 20) & (breadth > 0.70) & (vol_ratio < 0.66))
        )
        density_ok = np.isin(hour, [13, 14, 15, 16, 17, 18, 19, 20, 21]) & (range_ratio >= 0.40)
        return mask & density_ok & ~veto
    if extra_filter == "gl_short_balance_density_guard":
        long_ok = (side == "long") & np.isin(hour, [13, 14, 16, 17, 18, 19, 20]) & (breadth >= 0.26) & (vix_stress <= 2.12)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18, 19, 20, 21]) & (vol_ratio >= 0.55) & (breadth <= 0.72)
        return mask & (long_ok | short_ok)
    raise ValueError(f"unknown GL filter(알 수 없는 GL 필터): {extra_filter}")


def gl_selection_score(row: Mapping[str, Any]) -> float:
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
    density_reexpand = min(
        readiness(validation_density, 2.30, 0.55),
        readiness(oos_density, 2.25, 0.55),
        readiness(density, 2.30, 0.55),
    )
    density_bridge = min(
        readiness(validation_density, 2.55, 0.50),
        readiness(oos_density, 2.45, 0.50),
        readiness(density, 2.50, 0.50),
    )
    cost_preserve = min(
        readiness(oos_cost06, -8.0, 85.0),
        readiness(oos_cost09, -75.0, 170.0),
        readiness(combined_cost09, -170.0, 430.0),
    )
    profit_floor = min(
        readiness(validation_net, 0.0, 120.0),
        readiness(oos_net, 0.0, 130.0),
        readiness(oos_pf, 1.05, 0.18),
        readiness(validation_pf, 1.00, 0.14),
    )
    useful_reexpand = validation_net > 0 and oos_net > 0 and oos_pf >= 1.05 and oos_cost06 >= -8.0 and min_density >= 2.15 and combined_cost09 >= -220.0
    strong_reexpand = validation_net > 0 and oos_net > 0 and oos_pf >= 1.08 and oos_cost06 >= 0.0 and min_density >= 2.25
    density_only_collapse = min_density >= 2.45 and (validation_net <= 0 or oos_cost06 < -35.0 or combined_cost09 < -330.0)
    sparse_cost_only = oos_cost06 >= 0.0 and oos_pf >= 1.15 and min_density < 1.65
    guard_bonus = 1.0 if filter_id in {"gl_h1_density_cost_guard", "gl_late_loss_veto_guard", "gl_short_balance_density_guard"} else 0.0
    cost_guard_bonus = 1.0 if filter_id == "gl_cost_repair_preserve_guard" else 0.0
    return (
        25200.0 * density_reexpand
        + 16800.0 * density_bridge
        + 20500.0 * cost_preserve
        + 16600.0 * profit_floor
        + 12200.0 * (1.0 if useful_reexpand else 0.0)
        + 8200.0 * (1.0 if strong_reexpand else 0.0)
        + 1600.0 * guard_bonus
        + 1100.0 * cost_guard_bonus
        + 2.55 * validation_net
        + 3.15 * oos_net
        + 1.30 * values["combined_net"]
        + 2500.0 * max(0.0, validation_pf - 1.0)
        + 3800.0 * max(0.0, oos_pf - 1.0)
        + 1600.0 * max(0.0, min_pf - 1.0)
        + 1.30 * validation_cost09
        + 2.80 * oos_cost09
        + 4.80 * oos_cost06
        + 1.90 * combined_cost09
        + 4200.0 * min(min_density, 3.3)
        + 1350.0 * min(validation_density, 4.4)
        + 1650.0 * min(oos_density, 4.4)
        + 1450.0 * min(density, 4.4)
        + 550.0 * max(0.0, base.PRESERVE_SHORT_SHARE_FLOOR - short_share)
        + 15000.0 * (1.0 if base.gd_strict_success(row) else 0.0)
        - 11800.0 * (1.0 if density_only_collapse else 0.0)
        - 8600.0 * (1.0 if sparse_cost_only else 0.0)
        - 8400.0 * (1.0 if validation_net <= 0.0 else 0.0)
        - 8600.0 * (1.0 if oos_net <= 0.0 else 0.0)
        - 6100.0 * max(0.0, 1.03 - oos_pf)
        - 4700.0 * max(0.0, 1.00 - validation_pf)
        - 5200.0 * (1.0 if oos_cost06 < -20.0 else 0.0)
        - 3.0 * max(0.0, -validation_cost09 - 80.0)
        - 4.4 * max(0.0, -oos_cost09 - 105.0)
        - 2.6 * max(0.0, -combined_cost09 - 230.0)
        - 2500.0 * max(0.0, 2.05 - validation_density)
        - 2600.0 * max(0.0, 2.00 - oos_density)
        - 2500.0 * max(0.0, 2.05 - density)
        - 1800.0 * max(0.0, short_share - 0.86)
    )


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GL inputs(GL 입력 누락): " + ", ".join(missing))
    with fn.io_path(gk.FINAL_DECISION).open("r", encoding="utf-8-sig") as handle:
        parent = json.load(handle)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GK next_run_id mismatch(GK 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GK claim(금지된 GK 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gk.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GK gate audit(GK 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GL cost-repaired density reexpand input(GL 비용 수리 후 밀도 재확장 입력)",
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
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(옵시디언 실험 설계)",
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-model-validation(옵시디언 모델 검증)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate(범위 완료 게이트)",
                "kpi_contract_audit(KPI 계약 감사)",
                "skill_receipt_lint(스킬 영수증 점검)",
                "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            ],
            "hypothesis": "h1 density supply(h1 밀도 공급)를 GJ cost repair(GJ 비용 수리) 제약 아래 다시 넓히면 density-cost balance(밀도-비용 균형)가 개선될 수 있습니다.",
            "decision_use": NEXT_RUN_ID,
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": ["US100 M5", "chronological split(시간순 분할)", "Python proxy only(Python 프록시 전용)", "ONNX smoke only(ONNX 온엑스 간이 검증만)", "no trade splitting(거래 쪼개기 없음)"],
            "changed_variables": ["h1-only labels(h1 전용 라벨)", "density reexpand filters(밀도 재확장 필터)", "cost-preserve score(비용 보존 점수)", "density target ladder(밀도 목표 사다리)"],
            "success_criteria": ["combined density >=2.3 then >=2.6(합산 밀도 2.3 이상, 그 다음 2.6 이상)", "OOS cost0.6 near zero or positive(표본외 비용0.6 0 근처 또는 양수)", "validation and OOS net positive(검증과 표본외 순수익 양수)"],
            "failure_criteria": ["density-only cost collapse(밀도 전용 비용 붕괴)", "sparse cost-only recovery(희소 비용 전용 회복)", "validation-only optimization(검증 전용 최적화)"],
            "parent_summary": {
                "selected_oos_cost06_net": parent.get("selected_oos_cost06_net"),
                "selected_combined_density": parent.get("selected_combined_trade_density"),
                "density20_cost06_count": parent.get("density20_valpos_oospos_cost06_nonneg_count"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    et.write_csv(
        RUN364GM_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "gm01_cost_repaired_density_reexpand_review",
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
                "effect": "GM review(GM 검토)가 GL의 밀도 재확장과 비용 보존을 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base_payload = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    fn.write_json(RUN_EVIDENCE_RECEIPT, {**base_payload, "measurement_scope": "Python proxy with ONNX smoke(Python 프록시와 ONNX 온엑스 간이 검증)", "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "parity_level": "P0_unverified(P0 미검증)"})
    fn.write_json(EXPERIMENT_RECEIPT, {**base_payload, "hypothesis": "cost-repaired density reexpand(비용 수리 후 밀도 재확장)이 비용 회복을 잃지 않고 밀도를 회복하는지 시험합니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    fn.write_json(DATA_RECEIPT, {**base_payload, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC closed M5 bar timestamp(UTC 닫힌 5분봉 타임스탬프)", "sample_scope": "US100 M5 Tier A chronological split(US100 5분봉 Tier A 시간순 분할)", "feature_label_boundary": "future_open only in labels(future_open은 라벨에만 사용)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    fn.write_json(MODEL_RECEIPT, {**base_payload, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selection_metric": "GL density reexpand with cost preserve score(GL 비용 보존 밀도 재확장 점수)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    fn.write_json(ATTRIBUTION_RECEIPT, {**base_payload, "observed_change": f"validation/OOS net/PF/density(검증/표본외 순수익/수익 팩터/밀도) {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']} and {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["h1 density labels(h1 밀도 라벨)", "cost-preserve scoring(비용 보존 점수)", "late loss veto(후반 손실 차단)"], "next_probe": NEXT_RUN_ID})
    fn.write_json(JUDGMENT_RECEIPT, {**base_payload, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    fn.write_json(LINEAGE_RECEIPT, {**base_payload, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결됨)"})
    fn.write_json(CLAIM_RECEIPT, {**base_payload, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GL Cost-Repaired Density Reexpand(비용 수리 후 밀도 재확장)

Created(생성): {final['created_at_utc']}

Action(행동): GK failure memory(GK 실패 기억)를 받아 h1 density supply(h1 밀도 공급)를 GJ cost repair(GJ 비용 수리) 조건 아래 다시 넓혔습니다.

Effect(효과): 희소 h2 cost-only recovery(희소 h2 비용 전용 회복)를 피하면서 combined density(합산 밀도)를 다시 올릴 수 있는지 확인합니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `{final['selected_oos_cost06_net']}` / `{final.get('selected_oos_cost09_net', '')}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GL Cost-Repaired Density Reexpand(비용 수리 후 밀도 재확장)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GL model/label/filter/score(GL 모델/라벨/필터/점수)로 cost-repaired density reexpand(비용 수리 후 밀도 재확장)을 실행했습니다.

Effect(효과): Python proxy(Python 프록시)와 ONNX smoke(ONNX 온엑스 간이 검증) 근거만 남기고 운영 권위(runtime authority, 런타임 권위)는 주장하지 않습니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GL__{RUN_ID}", f"\n- run364GL__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cost-repaired density reexpand(비용 수리 후 밀도 재확장), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GL__{RUN_ID}", f"\n<!-- run364GL__{RUN_ID} -->\n\n## run364GL Cost-Repaired Density Reexpand(비용 수리 후 밀도 재확장)\n\nAction(행동): GK 실패 기억을 비용 보존 밀도 재확장 제약으로 바꾸어 재학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 GL 결과를 검토합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GL__{RUN_ID}", f"\n<!-- run364GL__{RUN_ID} -->\n## run364GL cost-repaired density reexpand(비용 수리 후 밀도 재확장)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GL` trained(학습 완료) cost-repaired density reexpand(비용 수리 후 밀도 재확장). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 그리고 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost truth(비용 진실): OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익)은 `{final['selected_oos_cost06_net']}` / `{final.get('selected_oos_cost09_net', '')}`이고, combined density/cost0.9(합산 밀도/비용0.9)는 `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 GL 결과를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): GL cost-repaired density reexpand(GL 비용 수리 후 밀도 재확장).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `{final['selected_oos_cost06_net']}` / `{final.get('selected_oos_cost09_net', '')}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GL__{RUN_ID}", f"\n<!-- run364GL__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed cost-repaired density reexpand(비용 수리 후 밀도 재확장); strict candidates(엄격 후보) `{final['strict_candidate_count']}`; selected(선택) `{final['selected_model_id']}`; next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GL__{RUN_ID}", f"\n<!-- run364GL__{RUN_ID} -->\n- `{RUN_ID}`: cost-repaired density reexpand(비용 수리 후 밀도 재확장)를 학습했습니다. Effect(효과): GK 실패 기억을 h1 density supply(h1 밀도 공급), cost preserve(비용 보존), late loss veto(후반 손실 차단) 점수로 공격했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        fn.append_text_once(NEGATIVE_REGISTER, f"run364GL__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364GL__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: cost-repaired density reexpand(비용 수리 후 밀도 재확장)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): GM에서 밀도 회복과 비용 보존을 분리합니다.\n")


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
        "question": "Can cost-repaired density reexpand recover density without losing cost repair?(비용 수리 후 밀도 재확장이 비용 수리를 잃지 않고 밀도를 회복할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};validation_net={final['selected_validation_net']};oos_pf={final['selected_oos_profit_factor']};oos_cost06={final['selected_oos_cost06_net']};combined_density={final['selected_combined_trade_density']}",
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
                "kpi_scope": "GL cost-repaired density reexpand(GL 비용 수리 후 밀도 재확장)",
                "metric_scope": "python_proxy_onnx_smoke(Python 프록시와 ONNX 온엑스 간이 검증)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "",
                "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시와 ONNX 온엑스 간이 검증, MT5 없음)",
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
                "run_type": "cost_repaired_density_reexpand(비용 수리 후 밀도 재확장)",
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
                    "notes": "GL cost-repaired density reexpand artifact(GL 비용 수리 후 밀도 재확장 산출물)",
                }
            )
    fn.append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def patch_gj_module() -> None:
    replacements = {
        "gi": gk,
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
        "RUN364GK_QUEUE": RUN364GM_QUEUE,
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
        "gj_feature_sets": gl_feature_sets,
        "gj_model_specs": gl_model_specs,
        "gj_extra_mask": gl_extra_mask,
        "gj_selection_score": gl_selection_score,
        "write_work_packet": write_work_packet,
        "write_queue": write_queue,
        "write_receipts": write_receipts,
        "write_docs": write_docs,
        "write_ledgers": write_ledgers,
        "write_artifact_registry": write_artifact_registry,
    }
    for name, value in replacements.items():
        setattr(gj, name, value)


def main() -> None:
    patch_gj_module()
    gj.main()


if __name__ == "__main__":
    main()
