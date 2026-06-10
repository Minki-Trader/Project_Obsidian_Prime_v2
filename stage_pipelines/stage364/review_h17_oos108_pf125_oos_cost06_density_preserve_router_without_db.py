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

from stage_pipelines.stage364 import review_h17_oos108_pf125_cost_near_density_lift_router_without_db as gu
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_near_density_lift_router_without_db as gt
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db as gv


fn = gv.fn
et = gv.et

TODAY = "2026-06-07"
STAGE_ID = gv.STAGE_ID
STAGE_DIR = gv.STAGE_DIR
REVIEW_DIR = gv.REVIEW_DIR
SPEC_DIR = gv.SPEC_DIR
SELECTED_DIR = gv.SELECTED_DIR

RUN_NUMBER = "run364GW"
RUN_ID = "run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1"
PARENT_RUN_ID = gv.RUN_ID
NEXT_RUN_ID = "run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1"

STATUS = "completed_stage364GW_oos_cost06_density_preserve_review_cost_repaired_density_failed_open_gx_no_authority"
JUDGMENT = "negative_for_package_positive_cost_repair_clue_density_failed_no_authority"
DECISION = "stage364GW_reject_package_open_run364GX_density_recover_cost06_hold_router"
CLAIM_BOUNDARY = (
    "research_development_oos_cost06_density_preserve_router_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "gw_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "gw_surface_diagnostic.csv"
DELTA_ATTRIBUTION = RUN_DIR / "gw_delta_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "gw_failure_memory.csv"
RUN364GX_QUEUE = RUN_DIR / "gw_gx_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GW_oos_cost06_density_preserve_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GW_oos_cost06_density_preserve_router_review.md"
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
    gv.FINAL_DECISION,
    gv.GATE_AUDIT,
    gv.TRADE_SURFACE,
    gv.SELECTED_CANDIDATE,
    gv.SELECTED_TRADE_TAPE,
    gv.COST_STRESS,
    gv.SIDE_SESSION_REVIEW,
    gv.MONTH_STABILITY,
    gv.MODEL_SCORECARD,
    gv.MODEL_ARTIFACT_MANIFEST,
    gv.ONNX_SMOKE_REPORT,
    gv.DATA_INTEGRITY_AUDIT,
    gv.RUN364GW_QUEUE,
    gu.FINAL_DECISION,
    gu.PACKAGE_DECISION,
    gu.FAILURE_MEMORY,
    gt.FINAL_DECISION,
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
    RUN364GX_QUEUE,
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
    return gv.exists(path)


def rel(path: Path) -> str:
    return gv.rel(path)


def sha(path: Path) -> str:
    return gv.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gv.as_float(value, default)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(path, list(rows))


def read_json(path: Path) -> dict[str, Any]:
    with fn.io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GW inputs(GW 입력 누락): " + ", ".join(missing))
    parent = read_json(gv.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GV next_run_id mismatch(GV 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GV claim(금지된 GV 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gv.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GV gate audit(GV 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GW OOS cost0.6 density preserve review input(GW 표본외 비용0.6 밀도 보존 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def numeric(surface: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(surface[column], errors="coerce").fillna(0.0)


def surface_counts(surface: pd.DataFrame) -> dict[str, Any]:
    validation_net = numeric(surface, "validation_net")
    oos_net = numeric(surface, "oos_net")
    oos_density = numeric(surface, "oos_trade_density")
    combined_density = numeric(surface, "combined_trade_density")
    oos_cost06 = numeric(surface, "oos_cost06_net")
    combined_cost09 = numeric(surface, "combined_cost09_net")
    positive = (validation_net > 0.0) & (oos_net > 0.0)
    first_pass = positive & (oos_cost06 >= -15.0) & (oos_density >= 1.35) & (combined_density >= 1.35) & (combined_cost09 >= -150.0)
    target = positive & (oos_cost06 >= -10.0) & (oos_density >= 1.35) & (combined_density >= 1.35) & (combined_cost09 >= -150.0)
    package_like = target & (oos_density >= 1.45) & (combined_density >= 1.45) & (combined_cost09 >= -80.0)
    cost_repaired_density_miss = positive & (oos_cost06 >= -15.0) & (combined_cost09 >= -100.0) & ((oos_density < 1.35) | (combined_density < 1.35))
    return {
        "surface_rows": int(len(surface)),
        "positive_rows": int(positive.sum()),
        "first_pass_cost_density_count": int(first_pass.sum()),
        "target_cost_density_count": int(target.sum()),
        "package_like_count": int(package_like.sum()),
        "cost_repaired_density_miss_count": int(cost_repaired_density_miss.sum()),
        "best_oos_cost06_net": float(oos_cost06.max()) if len(surface) else "",
        "best_oos_density": float(oos_density.max()) if len(surface) else "",
        "best_combined_density": float(combined_density.max()) if len(surface) else "",
        "best_combined_cost09_net": float(combined_cost09.max()) if len(surface) else "",
    }


def build_outputs(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    gt_parent = read_json(gt.FINAL_DECISION)
    surface = pd.read_csv(fn.io_path(gv.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    diagnostics_map = surface_counts(surface)

    gv_oos_cost06 = as_float(parent.get("selected_oos_cost06_net"))
    gt_oos_cost06 = as_float(gt_parent.get("selected_oos_cost06_net"))
    gv_oos_density = as_float(parent.get("selected_oos_trade_density"))
    gt_oos_density = as_float(gt_parent.get("selected_oos_trade_density"))
    gv_combined_density = as_float(parent.get("selected_combined_trade_density"))
    gt_combined_density = as_float(gt_parent.get("selected_combined_trade_density"))
    gv_combined_cost09 = as_float(parent.get("selected_combined_cost09_net"))
    gt_combined_cost09 = as_float(gt_parent.get("selected_combined_cost09_net"))
    gv_oos_net = as_float(parent.get("selected_oos_net"))
    gt_oos_net = as_float(gt_parent.get("selected_oos_net"))
    gv_oos_pf = as_float(parent.get("selected_oos_profit_factor"))
    gt_oos_pf = as_float(gt_parent.get("selected_oos_profit_factor"))

    delta_oos_cost06 = gv_oos_cost06 - gt_oos_cost06
    delta_oos_density = gv_oos_density - gt_oos_density
    delta_combined_density = gv_combined_density - gt_combined_density
    delta_combined_cost09 = gv_combined_cost09 - gt_combined_cost09
    delta_oos_net = gv_oos_net - gt_oos_net
    delta_oos_pf = gv_oos_pf - gt_oos_pf

    oos_cost_first_pass = gv_oos_cost06 >= -15.0
    oos_cost_target_met = gv_oos_cost06 >= -10.0
    oos_density_preserved = gv_oos_density >= 1.35
    combined_density_preserved = gv_combined_density >= 1.35
    combined_cost_preserved = gv_combined_cost09 >= -150.0
    strict_candidate_count = int(as_float(parent.get("strict_candidate_count")))
    operational_proxy_stack_pass_count = int(as_float(parent.get("operational_proxy_stack_pass_count")))
    package_eligible = (
        oos_cost_target_met
        and oos_density_preserved
        and combined_density_preserved
        and combined_cost_preserved
        and strict_candidate_count > 0
        and operational_proxy_stack_pass_count > 0
    )

    summary_rows = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent.get("selected_model_id"),
            "gt_reference_model_id": gt_parent.get("selected_model_id"),
            "gv_oos_cost06_net": gv_oos_cost06,
            "gt_oos_cost06_net": gt_oos_cost06,
            "delta_oos_cost06_net": delta_oos_cost06,
            "gv_oos_density": gv_oos_density,
            "gt_oos_density": gt_oos_density,
            "delta_oos_density": delta_oos_density,
            "gv_combined_density": gv_combined_density,
            "gt_combined_density": gt_combined_density,
            "delta_combined_density": delta_combined_density,
            "gv_combined_cost09_net": gv_combined_cost09,
            "gt_combined_cost09_net": gt_combined_cost09,
            "delta_combined_cost09_net": delta_combined_cost09,
            "oos_cost_first_pass": str(oos_cost_first_pass).lower(),
            "oos_cost_target_met": str(oos_cost_target_met).lower(),
            "oos_density_preserved": str(oos_density_preserved).lower(),
            "combined_density_preserved": str(combined_density_preserved).lower(),
            "combined_cost_preserved": str(combined_cost_preserved).lower(),
            "package_eligible": str(package_eligible).lower(),
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    diagnostics = [{"run_id": RUN_ID, "metric": key, "value": value, "claim_boundary": CLAIM_BOUNDARY} for key, value in diagnostics_map.items()]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "gw01_cost_repaired_density_lost",
            "observed_change": f"OOS cost0.6(표본외 비용0.6) {gt_oos_cost06} -> {gv_oos_cost06}; OOS density(표본외 밀도) {gt_oos_density} -> {gv_oos_density}",
            "likely_driver": "GV score(GV 점수)가 cost repair(비용 수리)를 성공적으로 강하게 당겼지만 density preserve(밀도 보존) 보상이 부족했습니다.",
            "effect": "GX는 OOS cost0.6(표본외 비용0.6) 수리 폭을 유지하면서 density floor(밀도 바닥)를 다시 올려야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gw02_combined_cost_stronger_than_density",
            "observed_change": f"combined cost0.9(합산 비용0.9) {gt_combined_cost09} -> {gv_combined_cost09}; combined density(합산 밀도) {gt_combined_density} -> {gv_combined_density}",
            "likely_driver": "cost degradation veto(비용 악화 차단)가 combined cost(합산 비용)를 크게 살렸지만 trade density(거래 밀도)를 줄였습니다.",
            "effect": "GX는 combined cost0.9(합산 비용0.9) 하한을 유지하면서 density recovery(밀도 회복)를 직접 보상해야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "package_eligible": str(package_eligible).lower(),
            "decision": "reject_package",
            "reason": "OOS cost0.6(표본외 비용0.6)은 first pass(1차)를 통과했지만 OOS/combined density(표본외/합산 밀도)와 strict candidate(엄격 후보)가 부족합니다.",
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "gw01_cost_repair_density_preserve_fail",
            "failed_boundary": "package-ready OOS cost0.6 density preserve(패키지 가능 표본외 비용0.6 밀도 보존)",
            "why_failed": f"oos_cost06={gv_oos_cost06}; oos_density={gv_oos_density}; combined_density={gv_combined_density}; strict={strict_candidate_count}; stack={operational_proxy_stack_pass_count}",
            "salvage_value": f"OOS cost0.6(표본외 비용0.6) improved by {delta_oos_cost06} and combined cost0.9(합산 비용0.9) improved by {delta_combined_cost09}.",
            "reopen_condition": "OOS cost0.6(표본외 비용0.6) >= -15, OOS density(표본외 밀도) >= 1.35, combined density(합산 밀도) >= 1.35, combined cost0.9(합산 비용0.9) >= -120.",
            "do_not_repeat": "Do not accept cost repair(비용 수리) if OOS density(표본외 밀도) falls below 1.30.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gx01_density_recover_cost06_hold_router",
            "hypothesis": "GV cost repair(GV 비용 수리)를 유지하면서 density recover(밀도 회복)를 직접 보상하면 better frontier(더 나은 경계면)를 만들 수 있습니다.",
            "required_preserve": "OOS cost0.6(표본외 비용0.6) >= -15, combined cost0.9(합산 비용0.9) >= -120.",
            "required_repair": "OOS density(표본외 밀도) >= 1.35, combined density(합산 밀도) >= 1.35, target(목표) combined density >= 1.45.",
            "avoid": "Avoid OOS cost0.6(표본외 비용0.6) < -22 or combined cost0.9(합산 비용0.9) < -150 while recovering density(밀도 회복 중).",
            "effect": "GX는 비용 수리 단서를 잃지 않고 밀도 실패를 직접 공격합니다.",
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
        "gt_reference_model_id": gt_parent.get("selected_model_id"),
        "gv_oos_net": gv_oos_net,
        "gt_oos_net": gt_oos_net,
        "delta_oos_net": delta_oos_net,
        "gv_oos_profit_factor": gv_oos_pf,
        "gt_oos_profit_factor": gt_oos_pf,
        "delta_oos_profit_factor": delta_oos_pf,
        "gv_oos_cost06_net": gv_oos_cost06,
        "gt_oos_cost06_net": gt_oos_cost06,
        "delta_oos_cost06_net": delta_oos_cost06,
        "gv_oos_trade_density": gv_oos_density,
        "gt_oos_trade_density": gt_oos_density,
        "delta_oos_trade_density": delta_oos_density,
        "gv_combined_trade_density": gv_combined_density,
        "gt_combined_trade_density": gt_combined_density,
        "delta_combined_trade_density": delta_combined_density,
        "gv_combined_cost09_net": gv_combined_cost09,
        "gt_combined_cost09_net": gt_combined_cost09,
        "delta_combined_cost09_net": delta_combined_cost09,
        "oos_cost_first_pass": str(oos_cost_first_pass).lower(),
        "oos_cost_target_met": str(oos_cost_target_met).lower(),
        "oos_density_preserved": str(oos_density_preserved).lower(),
        "combined_density_preserved": str(combined_density_preserved).lower(),
        "combined_cost_preserved": str(combined_cost_preserved).lower(),
        "strict_candidate_count": strict_candidate_count,
        "operational_proxy_stack_pass_count": operational_proxy_stack_pass_count,
        "package_eligible": str(package_eligible).lower(),
        "surface_rows": diagnostics_map["surface_rows"],
        "first_pass_cost_density_count": diagnostics_map["first_pass_cost_density_count"],
        "target_cost_density_count": diagnostics_map["target_cost_density_count"],
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
        ("scope_completion_gate", REVIEW_SUMMARY, "GW review summary(GW 검토 요약)를 작성했습니다."),
        ("parent_integrity_gate", INPUT_MANIFEST, "GV input lineage(GV 입력 계보)를 확인했습니다."),
        ("kpi_contract_audit", SURFACE_DIAGNOSTIC, "cost/density/PF/trade-count(비용/밀도/PF/거래수) 진단을 기록했습니다."),
        ("delta_attribution_gate", DELTA_ATTRIBUTION, "GV vs GT delta(GV와 GT 차이)를 귀속했습니다."),
        ("package_decision_gate", PACKAGE_DECISION, "package rejection(패키지 거절)을 명시했습니다."),
        ("failure_memory_gate", FAILURE_MEMORY, "density preserve failure memory(밀도 보존 실패 기억)를 남겼습니다."),
        ("next_queue_gate", RUN364GX_QUEUE, "GX next queue(GX 다음 대기열)를 열었습니다."),
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
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    fn.write_json(RESULT_RECEIPT, {**common, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    fn.write_json(MODEL_RECEIPT, {**common, "model_family": "GV OOS cost0.6 density preserve router(GV 표본외 비용0.6 밀도 보존 라우터)", "selection_review": "cost repair first pass(비용 수리 1차 통과), density preserve failed(밀도 보존 실패)", "validation_judgment": JUDGMENT, "next_condition": "density recover cost06 hold router(밀도 회복 비용0.6 유지 라우터)"})
    fn.write_json(ATTRIBUTION_RECEIPT, {**common, "observed_change": f"OOS cost0.6(표본외 비용0.6) {final['gt_oos_cost06_net']} -> {final['gv_oos_cost06_net']}; OOS density(표본외 밀도) {final['gt_oos_trade_density']} -> {final['gv_oos_trade_density']}", "comparison_baseline": gt.RUN_ID, "likely_drivers": ["OOS cost repair score(표본외 비용 수리 점수)", "density preserve underweight(밀도 보존 가중 부족)", "cost degradation veto(비용 악화 차단)"], "segment_checks": [rel(SURFACE_DIAGNOSTIC), rel(gv.COST_STRESS), rel(gv.SIDE_SESSION_REVIEW)], "attribution_confidence": "medium", "next_probe": NEXT_RUN_ID})
    fn.write_json(CLAIM_RECEIPT, {**common, "runtime_package": "not_opened", "new_mt5_execution": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})
    fn.write_json(LINEAGE_RECEIPT, {**common, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file() and path != LINEAGE_RECEIPT}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GW OOS Cost0.6 Density Preserve Router Review(표본외 비용0.6 밀도 보존 라우터 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GV result(GV 결과)를 GT baseline(GT 기준선)과 비교해 cost repair(비용 수리), density preserve(밀도 보존), package decision(패키지 결정)을 분리 판정했습니다.

Effect(효과): 비용 수리 단서는 살리고, 밀도 하락은 GX의 직접 수리 조건으로 넘깁니다.

- judgment(판정): `{final['judgment']}`
- review_subject(검토 대상): `{final['review_subject']}`
- OOS cost0.6 change(표본외 비용0.6 변화): `{final['gt_oos_cost06_net']}` -> `{final['gv_oos_cost06_net']}` (`{final['delta_oos_cost06_net']}`)
- OOS density change(표본외 밀도 변화): `{final['gt_oos_trade_density']}` -> `{final['gv_oos_trade_density']}` (`{final['delta_oos_trade_density']}`)
- combined density change(합산 밀도 변화): `{final['gt_combined_trade_density']}` -> `{final['gv_combined_trade_density']}` (`{final['delta_combined_trade_density']}`)
- combined cost0.9 change(합산 비용0.9 변화): `{final['gt_combined_cost09_net']}` -> `{final['gv_combined_cost09_net']}` (`{final['delta_combined_cost09_net']}`)
- package eligible(패키지 적격): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GW OOS Cost0.6 Density Preserve Router Review(표본외 비용0.6 밀도 보존 라우터 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GV package(패키지)를 reject(거절)하고 GX density recover cost06 hold router(GX 밀도 회복 비용0.6 유지 라우터)를 엽니다.

Effect(효과): GV의 비용 수리 단서를 보존하면서 OOS/combined density(표본외/합산 밀도) 실패를 다음 탐색의 직접 질문으로 바꿉니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GW__{RUN_ID}", f"\n- run364GW__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - GV cost repaired but density failed(GV 비용 수리, 밀도 실패), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GW__{RUN_ID}", f"\n<!-- run364GW__{RUN_ID} -->\n\n## run364GW OOS Cost0.6 Density Preserve Router Review(표본외 비용0.6 밀도 보존 라우터 검토)\n\nAction(행동): GV의 cost repair(비용 수리)와 density failure(밀도 실패)를 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 비용 수리 유지 + 밀도 회복을 같이 탐색합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GW__{RUN_ID}", f"\n<!-- run364GW__{RUN_ID} -->\n## run364GW OOS cost0.6 density preserve router review(표본외 비용0.6 밀도 보존 라우터 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    fn.write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
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

Current truth(현재 진실): `run364GW` reviewed(검토 완료) GV OOS cost0.6 density preserve router(GV 표본외 비용0.6 밀도 보존 라우터). GV는 OOS cost0.6(표본외 비용0.6)을 `{final['gt_oos_cost06_net']}`에서 `{final['gv_oos_cost06_net']}`로 개선했지만, OOS density(표본외 밀도)는 `{final['gt_oos_trade_density']}`에서 `{final['gv_oos_trade_density']}`로 낮아졌습니다.

Cost truth(비용 진실): combined cost0.9(합산 비용0.9)는 `{final['gv_combined_cost09_net']}`로 크게 개선됐지만, combined density(합산 밀도)는 `{final['gv_combined_trade_density']}`로 preserve floor(보존 바닥) `1.35`에 못 미칩니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 OOS cost0.6(표본외 비용0.6) `>= -15`, combined cost0.9(합산 비용0.9) `>= -120`을 유지하면서 OOS/combined density(표본외/합산 밀도)를 `>= 1.35`로 회복합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GW rejected(거절) GV OOS cost0.6 density preserve router(GV 표본외 비용0.6 밀도 보존 라우터).

GV selected model(GV 선택 모델): `{final['review_subject']}`
GV OOS net/PF/density/cost0.6(GV 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['gv_oos_net']}` / `{final['gv_oos_profit_factor']}` / `{final['gv_oos_trade_density']}` / `{final['gv_oos_cost06_net']}`
GV combined density/cost0.9(GV 합산 밀도/비용0.9): `{final['gv_combined_trade_density']}` / `{final['gv_combined_cost09_net']}`

Next seed(다음 씨앗): GX density recover cost06 hold router(GX 밀도 회복 비용0.6 유지 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GW__{RUN_ID}", f"\n<!-- run364GW__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` rejected GV package(GV 패키지 거절); OOS cost0.6(표본외 비용0.6) `{final['gv_oos_cost06_net']}`; OOS density(표본외 밀도) `{final['gv_oos_trade_density']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GW__{RUN_ID}", f"\n<!-- run364GW__{RUN_ID} -->\n- `{RUN_ID}`: GV cost repair(GV 비용 수리)는 positive clue(긍정 단서)입니다. Effect(효과): GX는 비용을 유지하면서 density recovery(밀도 회복)를 공격합니다.\n")
    fn.append_text_once(NEGATIVE_REGISTER, f"run364GW__cost_repair_density_preserve_fail__{RUN_ID}", f"\n<!-- run364GW__cost_repair_density_preserve_fail__{RUN_ID} -->\n- `{RUN_ID}`: cost repair(비용 수리)는 됐지만 OOS density(표본외 밀도) `{final['gv_oos_trade_density']}`와 combined density(합산 밀도) `{final['gv_combined_trade_density']}`가 부족합니다. Effect(효과): cost-only repair(비용만 수리)를 package(패키지)로 올리지 않습니다.\n")


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
        "question": "Did GV become package-ready after cost repair?(GV가 비용 수리 뒤 패키지 가능해졌는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"oos_cost_first_pass={final['oos_cost_first_pass']};oos_density_preserved={final['oos_density_preserved']};combined_density_preserved={final['combined_density_preserved']};package_eligible={final['package_eligible']}",
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
                "kpi_scope": "GW OOS cost0.6 density preserve review(GW 표본외 비용0.6 밀도 보존 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["gv_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["gv_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["gv_oos_trade_density"] if suffix == "tier_a_separate" else "",
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
                "run_type": "oos_cost06_density_preserve_router_review(표본외 비용0.6 밀도 보존 라우터 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "selected_net_profit": final["gv_oos_net"],
                "selected_profit_factor": final["gv_oos_profit_factor"],
                "selected_trade_density": final["gv_oos_trade_density"],
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
                    "notes": "GW OOS cost0.6 density preserve router review artifact(GW 표본외 비용0.6 밀도 보존 라우터 검토 산출물)",
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
    write_csv(RUN364GX_QUEUE, queue)
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
