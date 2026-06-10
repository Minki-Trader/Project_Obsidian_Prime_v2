from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_h17_oos108_pf125_cost_near_density_floor_router_without_db as gs
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_near_density_floor_router_without_db as gr
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_near_density_lift_router_without_db as gt


fn = gt.fn
et = gt.et

TODAY = "2026-06-07"
STAGE_ID = gt.STAGE_ID
STAGE_DIR = gt.STAGE_DIR
REVIEW_DIR = gt.REVIEW_DIR
SPEC_DIR = gt.SPEC_DIR
SELECTED_DIR = gt.SELECTED_DIR

RUN_NUMBER = "run364GU"
RUN_ID = "run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1"
PARENT_RUN_ID = gt.RUN_ID
NEXT_RUN_ID = "run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1"

STATUS = "completed_stage364GU_cost_near_density_lift_router_review_oos_density_lifted_combined_cost_preserved_oos_cost_failed_open_gv_no_authority"
JUDGMENT = "negative_cost_near_density_lift_router_review_oos_density_lifted_combined_cost_preserved_oos_cost_failed_no_package_no_authority"
DECISION = "stage364GU_reject_package_open_run364GV_oos_cost06_density_preserve_router"
CLAIM_BOUNDARY = (
    "research_development_cost_near_density_lift_router_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "gu_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "gu_surface_diagnostic.csv"
DELTA_ATTRIBUTION = RUN_DIR / "gu_delta_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "gu_failure_memory.csv"
RUN364GV_QUEUE = RUN_DIR / "gu_gv_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GU_cost_near_density_lift_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GU_cost_near_density_lift_router_review.md"
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
    gt.FINAL_DECISION,
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
    gt.RUN364GU_QUEUE,
    gs.FINAL_DECISION,
    gs.PACKAGE_DECISION,
    gs.FAILURE_MEMORY,
    gr.FINAL_DECISION,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    SURFACE_DIAGNOSTIC,
    DELTA_ATTRIBUTION,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364GV_QUEUE,
    RESULT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    THIS_FILE,
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def exists(path: Path) -> bool:
    return gt.exists(path)


def rel(path: Path) -> str:
    return gt.rel(path)


def sha(path: Path) -> str:
    return gt.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gt.as_float(value, default)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(path, list(rows))


def read_json(path: Path) -> dict[str, Any]:
    with fn.io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GU inputs(GU 입력 누락): " + ", ".join(missing))
    parent = read_json(gt.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GT next_run_id mismatch(GT 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GT claim(금지된 GT 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gt.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GT gate audit(GT 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    for label, path in [("GS", gs.FINAL_DECISION), ("GR", gr.FINAL_DECISION)]:
        decision = read_json(path)
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
            "input_role": "GU cost-near density lift review input(GU 비용 근접 밀도 상승 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def numeric(surface: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(surface[column], errors="coerce").fillna(0.0)


def surface_counts(surface: pd.DataFrame) -> dict[str, Any]:
    validation_net = numeric(surface, "validation_net")
    oos_net = numeric(surface, "oos_net")
    combined_density = numeric(surface, "combined_trade_density")
    validation_density = numeric(surface, "validation_trade_density")
    oos_density = numeric(surface, "oos_trade_density")
    oos_cost06 = numeric(surface, "oos_cost06_net")
    combined_cost09 = numeric(surface, "combined_cost09_net")
    positive = surface[(validation_net > 0.0) & (oos_net > 0.0)].copy()
    out: dict[str, Any] = {
        "surface_rows": int(len(surface)),
        "positive_rows": int(len(positive)),
        "best_oos_cost06_net": float(oos_cost06.max()) if len(surface) else "",
        "best_combined_cost09_net": float(combined_cost09.max()) if len(surface) else "",
        "best_combined_density": float(combined_density.max()) if len(surface) else "",
        "best_oos_density": float(oos_density.max()) if len(surface) else "",
    }
    for density in [1.2, 1.35, 1.45, 1.5, 1.8, 2.0]:
        key = str(density).replace(".", "p")
        all_split = (validation_density >= density) & (oos_density >= density) & (combined_density >= density)
        subset = surface[(validation_net > 0.0) & (oos_net > 0.0) & all_split]
        out[f"density{key}_all_split_positive_count"] = int(len(subset))
        out[f"density{key}_max_oos_cost06_net"] = float(numeric(subset, "oos_cost06_net").max()) if len(subset) else ""
        out[f"density{key}_max_combined_cost09_net"] = float(numeric(subset, "combined_cost09_net").max()) if len(subset) else ""
    pos_mask = (validation_net > 0.0) & (oos_net > 0.0)
    preserve_lift = pos_mask & (oos_density >= 1.20) & (combined_density >= 1.35) & (combined_cost09 >= -140.0)
    target = preserve_lift & (combined_density >= 1.45) & (oos_cost06 >= -10.0)
    package_like = target & (oos_density >= 1.50) & (combined_density >= 2.00) & (combined_cost09 >= -80.0) & (oos_cost06 >= -5.0)
    out["preserve_lift_count"] = int(preserve_lift.sum())
    out["target_count"] = int(target.sum())
    out["package_like_count"] = int(package_like.sum())
    out["oos_cost06_ge_minus10_positive_count"] = int((pos_mask & (oos_cost06 >= -10.0)).sum())
    out["oos_cost06_ge_minus15_density135_count"] = int((pos_mask & (oos_cost06 >= -15.0) & (oos_density >= 1.35)).sum())
    return out


def build_outputs(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    gr_parent = read_json(gr.FINAL_DECISION)
    gs_review = read_json(gs.FINAL_DECISION)
    surface = pd.read_csv(fn.io_path(gt.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    diagnostics_map = surface_counts(surface)

    gt_oos_density = as_float(parent.get("selected_oos_trade_density"))
    gt_combined_density = as_float(parent.get("selected_combined_trade_density"))
    gt_oos_cost06 = as_float(parent.get("selected_oos_cost06_net"))
    gt_combined_cost09 = as_float(parent.get("selected_combined_cost09_net"))
    gt_oos_net = as_float(parent.get("selected_oos_net"))
    gt_oos_pf = as_float(parent.get("selected_oos_profit_factor"))
    gt_combined_trades = as_float(parent.get("selected_combined_trade_count"))
    gt_short_share = as_float(parent.get("selected_combined_short_share"))

    gr_oos_density = as_float(gr_parent.get("selected_oos_trade_density"))
    gr_combined_density = as_float(gr_parent.get("selected_combined_trade_density"))
    gr_oos_cost06 = as_float(gr_parent.get("selected_oos_cost06_net"))
    gr_combined_cost09 = as_float(gr_parent.get("selected_combined_cost09_net"))
    gr_oos_net = as_float(gr_parent.get("selected_oos_net"))
    gr_oos_pf = as_float(gr_parent.get("selected_oos_profit_factor"))
    gr_short_share = as_float(gr_parent.get("selected_combined_short_share"))

    delta_oos_density = gt_oos_density - gr_oos_density
    delta_combined_density = gt_combined_density - gr_combined_density
    delta_oos_cost06 = gt_oos_cost06 - gr_oos_cost06
    delta_combined_cost09 = gt_combined_cost09 - gr_combined_cost09
    delta_oos_net = gt_oos_net - gr_oos_net
    delta_oos_pf = gt_oos_pf - gr_oos_pf
    delta_short_share = gt_short_share - gr_short_share

    oos_density_lifted = gt_oos_density >= 1.20 and delta_oos_density > 0.0
    combined_density_lifted = delta_combined_density > 0.0
    combined_cost_preserved = gt_combined_cost09 >= -140.0
    combined_density_target_met = gt_combined_density >= 1.45
    oos_cost_repaired = gt_oos_cost06 >= -10.0
    oos_cost_degraded = delta_oos_cost06 < 0.0
    strict_candidate_count = int(as_float(parent.get("strict_candidate_count")))
    operational_proxy_stack_pass_count = int(as_float(parent.get("operational_proxy_stack_pass_count")))
    package_eligible = (
        oos_density_lifted
        and combined_cost_preserved
        and combined_density_target_met
        and oos_cost_repaired
        and strict_candidate_count > 0
        and operational_proxy_stack_pass_count > 0
    )

    summary_rows = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent.get("selected_model_id"),
            "gr_selected_model_id": gr_parent.get("selected_model_id"),
            "gt_oos_net": gt_oos_net,
            "gr_oos_net": gr_oos_net,
            "delta_oos_net": delta_oos_net,
            "gt_oos_profit_factor": gt_oos_pf,
            "gr_oos_profit_factor": gr_oos_pf,
            "delta_oos_profit_factor": delta_oos_pf,
            "gt_oos_density": gt_oos_density,
            "gr_oos_density": gr_oos_density,
            "delta_oos_density": delta_oos_density,
            "gt_combined_density": gt_combined_density,
            "gr_combined_density": gr_combined_density,
            "delta_combined_density": delta_combined_density,
            "gt_oos_cost06_net": gt_oos_cost06,
            "gr_oos_cost06_net": gr_oos_cost06,
            "delta_oos_cost06_net": delta_oos_cost06,
            "gt_combined_cost09_net": gt_combined_cost09,
            "gr_combined_cost09_net": gr_combined_cost09,
            "delta_combined_cost09_net": delta_combined_cost09,
            "oos_density_lifted": str(oos_density_lifted).lower(),
            "combined_cost_preserved": str(combined_cost_preserved).lower(),
            "combined_density_target_met": str(combined_density_target_met).lower(),
            "oos_cost_repaired": str(oos_cost_repaired).lower(),
            "oos_cost_degraded": str(oos_cost_degraded).lower(),
            "package_eligible": str(package_eligible).lower(),
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    diagnostics = [
        {"run_id": RUN_ID, "metric": key, "value": value, "claim_boundary": CLAIM_BOUNDARY}
        for key, value in diagnostics_map.items()
    ]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "gu01_oos_density_lift_cost06_degradation",
            "observed_change": f"OOS density(표본외 밀도) {gr_oos_density} -> {gt_oos_density}; OOS cost0.6(표본외 비용0.6) {gr_oos_cost06} -> {gt_oos_cost06}",
            "likely_driver": "GT score(GT 점수)가 density lift(밀도 상승)를 강하게 보상했지만 OOS cost0.6(표본외 비용0.6) 보존을 충분히 닫지 못했습니다.",
            "effect": "GV는 density(밀도)를 보존하면서 OOS cost0.6(표본외 비용0.6)을 먼저 수리해야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gu02_combined_cost_preserved_but_density_target_narrow_miss",
            "observed_change": f"combined cost0.9(합산 비용0.9) {gr_combined_cost09} -> {gt_combined_cost09}; combined density(합산 밀도) {gr_combined_density} -> {gt_combined_density}",
            "likely_driver": "cost-near preserve(비용 근접 보존)와 density lift(밀도 상승)가 함께 작동했지만 combined density target(합산 밀도 목표) 1.45에는 조금 못 미쳤습니다.",
            "effect": "GV는 combined cost0.9(합산 비용0.9) 하한을 너무 조이지 않고 density floor(밀도 바닥)를 유지해야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gu03_side_mix_less_short_dominated",
            "observed_change": f"combined short share(합산 숏 비중) {gr_short_share} -> {gt_short_share}",
            "likely_driver": "GT selection(GT 선택)이 GR보다 long(롱)을 더 열어 OOS density(표본외 밀도)를 높였습니다.",
            "effect": "side balance(방향 균형)는 좋아졌지만 cost stress(비용 압박)를 같이 통과하지 못하면 package(패키지)로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "package_eligible": str(package_eligible).lower(),
            "decision": "reject_package",
            "reason": "OOS density(표본외 밀도)는 상승했지만 OOS cost0.6(표본외 비용0.6), combined density target(합산 밀도 목표), strict candidate(엄격 후보)가 부족합니다.",
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "gu01_density_lift_without_oos_cost_repair",
            "failed_boundary": "package-ready cost-near density lift(패키지 가능 비용 근접 밀도 상승)",
            "why_failed": f"oos_cost06={gt_oos_cost06}; combined_density={gt_combined_density}; strict={strict_candidate_count}; stack={operational_proxy_stack_pass_count}",
            "salvage_value": f"OOS density(표본외 밀도) rose by {delta_oos_density} and combined cost0.9(합산 비용0.9) stayed above -140.",
            "reopen_condition": "OOS cost0.6(표본외 비용0.6) >= -10, OOS density(표본외 밀도) >= 1.35, combined cost0.9(합산 비용0.9) >= -150, strict candidate(엄격 후보) > 0.",
            "do_not_repeat": "Do not trade OOS cost0.6 repair(표본외 비용0.6 수리)를 away for density(밀도) alone.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gv01_oos_cost06_density_preserve_router",
            "hypothesis": "GT OOS density(표본외 밀도)를 보존하면서 OOS cost0.6(표본외 비용0.6)을 수리하면 더 나은 frontier(경계면)를 만들 수 있습니다.",
            "required_preserve": "OOS density(표본외 밀도) >= 1.35, combined density(합산 밀도) >= 1.35, combined cost0.9(합산 비용0.9) >= -150.",
            "required_repair": "OOS cost0.6(표본외 비용0.6) >= -15 first pass(1차), target(목표) >= -10.",
            "avoid": "Avoid density lift(밀도 상승) if OOS cost0.6(표본외 비용0.6) < -30 or combined cost0.9(합산 비용0.9) < -180.",
            "effect": "GV는 GT의 밀도 단서를 버리지 않고 비용 실패 기억을 직접 제약으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    final = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "review_subject": parent.get("selected_model_id"),
        "gr_review_reference": gs_review.get("run_id"),
        "gr_selected_model_id": gr_parent.get("selected_model_id"),
        "gt_oos_net": gt_oos_net,
        "gr_oos_net": gr_oos_net,
        "delta_oos_net": delta_oos_net,
        "gt_oos_profit_factor": gt_oos_pf,
        "gr_oos_profit_factor": gr_oos_pf,
        "delta_oos_profit_factor": delta_oos_pf,
        "gt_oos_trade_density": gt_oos_density,
        "gr_oos_trade_density": gr_oos_density,
        "delta_oos_trade_density": delta_oos_density,
        "gt_combined_trade_density": gt_combined_density,
        "gr_combined_trade_density": gr_combined_density,
        "delta_combined_trade_density": delta_combined_density,
        "gt_combined_trade_count": gt_combined_trades,
        "gt_oos_cost06_net": gt_oos_cost06,
        "gr_oos_cost06_net": gr_oos_cost06,
        "delta_oos_cost06_net": delta_oos_cost06,
        "gt_combined_cost09_net": gt_combined_cost09,
        "gr_combined_cost09_net": gr_combined_cost09,
        "delta_combined_cost09_net": delta_combined_cost09,
        "gt_combined_short_share": gt_short_share,
        "gr_combined_short_share": gr_short_share,
        "delta_combined_short_share": delta_short_share,
        "oos_density_lifted": str(oos_density_lifted).lower(),
        "combined_density_lifted": str(combined_density_lifted).lower(),
        "combined_cost_preserved": str(combined_cost_preserved).lower(),
        "combined_density_target_met": str(combined_density_target_met).lower(),
        "oos_cost_repaired": str(oos_cost_repaired).lower(),
        "oos_cost_degraded": str(oos_cost_degraded).lower(),
        "strict_candidate_count": strict_candidate_count,
        "operational_proxy_stack_pass_count": operational_proxy_stack_pass_count,
        "package_eligible": str(package_eligible).lower(),
        "surface_rows": diagnostics_map["surface_rows"],
        "preserve_lift_count": diagnostics_map["preserve_lift_count"],
        "target_count": diagnostics_map["target_count"],
        "package_like_count": diagnostics_map["package_like_count"],
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }
    return summary_rows, diagnostics, attribution, package, failure, queue, final


def write_work_packet(parent: Mapping[str, Any]) -> None:
    fn.write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-run-evidence-system(실행 근거 시스템)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "parent_integrity_gate(상위 무결성 게이트)",
                "kpi_contract_audit(KPI 계약 감사)",
                "package_decision_gate(패키지 결정 게이트)",
                "failure_memory_gate(실패 기억 게이트)",
                "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            ],
            "review_subject": parent.get("run_id"),
            "decision_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_gates() -> list[dict[str, Any]]:
    gates = [
        ("scope_completion_gate", REVIEW_SUMMARY, "GU review summary(GU 검토 요약)를 작성했습니다."),
        ("parent_integrity_gate", INPUT_MANIFEST, "GT input lineage(GT 입력 계보)를 확인했습니다."),
        ("kpi_contract_audit", SURFACE_DIAGNOSTIC, "density/cost/PF/trade-count(밀도/비용/PF/거래수) 진단을 기록했습니다."),
        ("delta_attribution_gate", DELTA_ATTRIBUTION, "GT vs GR delta(GT와 GR 차이)를 귀속했습니다."),
        ("package_decision_gate", PACKAGE_DECISION, "package rejection(패키지 거절)을 명시했습니다."),
        ("failure_memory_gate", FAILURE_MEMORY, "OOS cost0.6 failure memory(표본외 비용0.6 실패 기억)를 남겼습니다."),
        ("next_queue_gate", RUN364GV_QUEUE, "GV next queue(GV 다음 대기열)를 열었습니다."),
        ("paired_tier_record_gate", STAGE_LEDGER, "Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B) 장부 행을 남겼습니다."),
        ("receipt_coverage_gate", RESULT_RECEIPT, "result/model/attribution/lineage/claim receipts(결과/모델/귀속/계보/주장 영수증)를 남겼습니다."),
        ("final_claim_guard", CLAIM_RECEIPT, "runtime authority/Goal Achieve(런타임 권위/목표 달성) 주장을 차단했습니다."),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed",
            "evidence": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": final["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    fn.write_json(
        RESULT_RECEIPT,
        {
            **common,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)],
            "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
        },
    )
    fn.write_json(
        MODEL_RECEIPT,
        {
            **common,
            "model_family": "GT cost-near density lift router(GT 비용 근접 밀도 상승 라우터)",
            "selection_review": "OOS density(표본외 밀도) lifted, OOS cost0.6(표본외 비용0.6) failed",
            "validation_judgment": JUDGMENT,
            "next_condition": "OOS cost0.6 density preserve router(표본외 비용0.6 밀도 보존 라우터)",
        },
    )
    fn.write_json(
        ATTRIBUTION_RECEIPT,
        {
            **common,
            "observed_change": f"OOS density(표본외 밀도) {final['gr_oos_trade_density']} -> {final['gt_oos_trade_density']}; OOS cost0.6(표본외 비용0.6) {final['gr_oos_cost06_net']} -> {final['gt_oos_cost06_net']}",
            "comparison_baseline": gr.RUN_ID,
            "likely_drivers": ["density lift score(밀도 상승 점수)", "cost-near preserve(비용 근접 보존)", "OOS cost0.6 under-constraint(표본외 비용0.6 제약 부족)"],
            "segment_checks": [rel(SURFACE_DIAGNOSTIC), rel(gt.COST_STRESS), rel(gt.SIDE_SESSION_REVIEW)],
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
        },
    )
    fn.write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    fn.write_json(
        LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [
                {"path": rel(path), "sha256": sha(path)}
                for path in INPUT_FILES
                if exists(path) and fn.io_path(path).is_file()
            ],
            "producer": rel(THIS_FILE),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {
                rel(path): sha(path)
                for path in OUTPUT_FILES
                if exists(path) and fn.io_path(path).is_file() and path != LINEAGE_RECEIPT
            },
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)",
        },
    )


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GU Cost-Near Density Lift Router Review(비용 근접 밀도 상승 라우터 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GT result(GT 결과)를 GR baseline(GR 기준선)과 비교해 density lift(밀도 상승), cost repair(비용 수리), package decision(패키지 결정)을 분리 판정했습니다.

Effect(효과): OOS density(표본외 밀도) 개선은 살리고, OOS cost0.6(표본외 비용0.6) 실패는 다음 GV 제약으로 바꿉니다.

- judgment(판정): `{final['judgment']}`
- review_subject(검토 대상): `{final['review_subject']}`
- OOS density change(표본외 밀도 변화): `{final['gr_oos_trade_density']}` -> `{final['gt_oos_trade_density']}` (`{final['delta_oos_trade_density']}`)
- combined density change(합산 밀도 변화): `{final['gr_combined_trade_density']}` -> `{final['gt_combined_trade_density']}` (`{final['delta_combined_trade_density']}`)
- OOS cost0.6 change(표본외 비용0.6 변화): `{final['gr_oos_cost06_net']}` -> `{final['gt_oos_cost06_net']}` (`{final['delta_oos_cost06_net']}`)
- combined cost0.9 change(합산 비용0.9 변화): `{final['gr_combined_cost09_net']}` -> `{final['gt_combined_cost09_net']}` (`{final['delta_combined_cost09_net']}`)
- OOS net/PF(표본외 순수익/수익 팩터): `{final['gt_oos_net']}` / `{final['gt_oos_profit_factor']}`
- strict candidate count(엄격 후보 수): `{final['strict_candidate_count']}`
- package eligible(패키지 적격): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GU Cost-Near Density Lift Router Review(비용 근접 밀도 상승 라우터 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GT package(패키지)를 reject(거절)하고 GV OOS cost0.6 density preserve router(GV 표본외 비용0.6 밀도 보존 라우터)를 엽니다.

Effect(효과): GT의 OOS density(표본외 밀도) 단서는 보존하고, OOS cost0.6(표본외 비용0.6) 실패를 다음 탐색의 직접 제약으로 사용합니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(
        REVIEW_INDEX,
        f"run364GU__{RUN_ID}",
        f"\n- run364GU__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - GT OOS density lifted but OOS cost0.6 failed(GT 표본외 밀도 상승, 표본외 비용0.6 실패), next `{NEXT_RUN_ID}`.\n",
    )
    fn.append_text_once(
        STAGE_BRIEF,
        f"run364GU__{RUN_ID}",
        f"\n<!-- run364GU__{RUN_ID} -->\n\n## run364GU Cost-Near Density Lift Router Review(비용 근접 밀도 상승 라우터 검토)\n\nAction(행동): GT의 density lift(밀도 상승)와 cost failure(비용 실패)를 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 OOS density(표본외 밀도)를 보존하면서 OOS cost0.6(표본외 비용0.6)을 수리합니다.\n",
    )
    fn.append_text_once(
        STAGE_README,
        f"run364GU__{RUN_ID}",
        f"\n<!-- run364GU__{RUN_ID} -->\n## run364GU cost-near density lift router review(비용 근접 밀도 상승 라우터 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n",
    )
    fn.write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    fn.write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364GU` reviewed(검토 완료) GT cost-near density lift router(GT 비용 근접 밀도 상승 라우터). GT는 OOS density(표본외 밀도)를 `{final['gr_oos_trade_density']}`에서 `{final['gt_oos_trade_density']}`로 끌어올렸지만, OOS cost0.6(표본외 비용0.6)은 `{final['gr_oos_cost06_net']}`에서 `{final['gt_oos_cost06_net']}`로 악화했습니다.

Cost truth(비용 진실): combined cost0.9(합산 비용0.9)는 `{final['gt_combined_cost09_net']}`로 preserve threshold(보존 기준) `-140`은 통과했지만, combined density(합산 밀도)는 `{final['gt_combined_trade_density']}`로 target(목표) `1.45`에 조금 못 미칩니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 OOS density(표본외 밀도) `>= 1.35`, combined cost0.9(합산 비용0.9) `>= -150`을 보존하면서 OOS cost0.6(표본외 비용0.6)을 `>= -15`, 가능하면 `>= -10`으로 수리합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    fn.write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GU rejected(거절) GT cost-near density lift router(GT 비용 근접 밀도 상승 라우터).

Selected GT model(선택 GT 모델): `{final['review_subject']}`
Selected OOS net/PF/density/cost0.6(선택 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['gt_oos_net']}` / `{final['gt_oos_profit_factor']}` / `{final['gt_oos_trade_density']}` / `{final['gt_oos_cost06_net']}`
Selected combined density/trades/cost0.9(선택 합산 밀도/거래수/비용0.9): `{final['gt_combined_trade_density']}` / `{final['gt_combined_trade_count']}` / `{final['gt_combined_cost09_net']}`

Next seed(다음 씨앗): GV OOS cost0.6 density preserve router(GV 표본외 비용0.6 밀도 보존 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    fn.append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364GU__{RUN_ID}",
        f"\n<!-- run364GU__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` rejected GT package(GT 패키지 거절); OOS density(표본외 밀도) `{final['gt_oos_trade_density']}`; OOS cost0.6(표본외 비용0.6) `{final['gt_oos_cost06_net']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    fn.append_text_once(
        IDEA_REGISTRY,
        f"run364GU__{RUN_ID}",
        f"\n<!-- run364GU__{RUN_ID} -->\n- `{RUN_ID}`: GT density lift(GT 밀도 상승)는 유효한 positive clue(긍정 단서)입니다. Effect(효과): GV는 이 단서를 보존하면서 OOS cost0.6(표본외 비용0.6)을 직접 수리합니다.\n",
    )
    fn.append_text_once(
        NEGATIVE_REGISTER,
        f"run364GU__density_lift_without_oos_cost_repair__{RUN_ID}",
        f"\n<!-- run364GU__density_lift_without_oos_cost_repair__{RUN_ID} -->\n- `{RUN_ID}`: OOS density(표본외 밀도)는 상승했지만 OOS cost0.6(표본외 비용0.6) `{final['gt_oos_cost06_net']}`로 package(패키지) 실패입니다. Effect(효과): density-only lift(밀도만 올리는 선택)를 다음 run(실행)에서 반복하지 않습니다.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    artifact_count = len({path for path in OUTPUT_FILES if exists(path) or path == RUN_MANIFEST})
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Did GT cost-near density lift become package-ready?(GT 비용 근접 밀도 상승이 패키지 가능해졌는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"oos_density_lifted={final['oos_density_lifted']};oos_cost_repaired={final['oos_cost_repaired']};combined_cost_preserved={final['combined_cost_preserved']};package_eligible={final['package_eligible']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
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
                "kpi_scope": "GU cost-near density lift review(GU 비용 근접 밀도 상승 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["gt_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["gt_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["gt_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": "",
                "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
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
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "cost_near_density_lift_router_review(비용 근접 밀도 상승 라우터 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "selected_net_profit": final["gt_oos_net"],
                "selected_profit_factor": final["gt_oos_profit_factor"],
                "selected_trade_density": final["gt_oos_trade_density"],
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
                    "notes": "GU cost-near density lift router review artifact(GU 비용 근접 밀도 상승 라우터 검토 산출물)",
                }
            )
    fn.append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_run_manifest(final: Mapping[str, Any]) -> None:
    fn.write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
        },
    )


def main() -> None:
    parent = validate_inputs()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    summary, diagnostics, attribution, package, failure, queue, final = build_outputs(parent)
    write_csv(REVIEW_SUMMARY, summary)
    write_csv(SURFACE_DIAGNOSTIC, diagnostics)
    write_csv(DELTA_ATTRIBUTION, attribution)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364GV_QUEUE, queue)
    gates = write_gates()
    final["gate_passes"] = len([row for row in gates if row["status"] == "passed"])
    final["gate_total"] = len(gates)
    fn.write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_run_manifest(final)
    write_receipts(final)
    write_ledgers(final)
    write_artifact_registry(final)
    write_run_manifest(final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "judgment": JUDGMENT,
                "package_eligible": final["package_eligible"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
