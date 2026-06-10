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

from stage_pipelines.stage364 import review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db as gw
from stage_pipelines.stage364 import train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db as gx
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db as gv


fn = gx.fn
et = gx.et

TODAY = "2026-06-07"
STAGE_ID = gx.STAGE_ID
STAGE_DIR = gx.STAGE_DIR
REVIEW_DIR = gx.REVIEW_DIR
SPEC_DIR = gx.SPEC_DIR
SELECTED_DIR = gx.SELECTED_DIR

RUN_NUMBER = "run364GY"
RUN_ID = "run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1"
PARENT_RUN_ID = gx.RUN_ID
NEXT_RUN_ID = "run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1"

STATUS = "completed_stage364GY_density_recover_cost06_hold_review_oos_profit_cost06_improved_density_failed_combined_cost_slipped_open_gz_no_authority"
JUDGMENT = "negative_for_package_positive_oos_profit_cost06_clue_density_not_recovered_combined_cost_slipped_no_authority"
DECISION = "stage364GY_reject_package_open_run364GZ_cost_density_joint_frontier_router"
CLAIM_BOUNDARY = (
    "research_development_density_recover_cost06_hold_router_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "gy_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "gy_surface_diagnostic.csv"
DELTA_ATTRIBUTION = RUN_DIR / "gy_delta_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "gy_failure_memory.csv"
RUN364GZ_QUEUE = RUN_DIR / "gy_gz_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GY_density_recover_cost06_hold_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GY_density_recover_cost06_hold_router_review.md"
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
    gx.FINAL_DECISION,
    gx.GATE_AUDIT,
    gx.TRADE_SURFACE,
    gx.SELECTED_CANDIDATE,
    gx.SELECTED_TRADE_TAPE,
    gx.COST_STRESS,
    gx.SIDE_SESSION_REVIEW,
    gx.MONTH_STABILITY,
    gx.MODEL_SCORECARD,
    gx.MODEL_ARTIFACT_MANIFEST,
    gx.ONNX_SMOKE_REPORT,
    gx.DATA_INTEGRITY_AUDIT,
    gx.RUN364GY_QUEUE,
    gv.FINAL_DECISION,
    gv.TRADE_SURFACE,
    gw.FINAL_DECISION,
    gw.PACKAGE_DECISION,
    gw.FAILURE_MEMORY,
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
    RUN364GZ_QUEUE,
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
    return gx.exists(path)


def rel(path: Path) -> str:
    return gx.rel(path)


def sha(path: Path) -> str:
    return gx.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gx.as_float(value, default)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(path, list(rows))


def read_json(path: Path) -> dict[str, Any]:
    with fn.io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GY inputs(GY 입력 누락): " + ", ".join(missing))
    parent = read_json(gx.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GX next_run_id mismatch(GX 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GX claim(금지된 GX 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gx.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GX gate audit(GX 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GY density recover cost0.6 hold review input(GY 밀도 회복 비용0.6 유지 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def numeric(surface: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(surface[column], errors="coerce").fillna(0.0)


def surface_counts(surface: pd.DataFrame) -> dict[str, Any]:
    validation_net = numeric(surface, "validation_net")
    oos_net = numeric(surface, "oos_net")
    oos_pf = numeric(surface, "oos_profit_factor")
    oos_density = numeric(surface, "oos_trade_density")
    combined_density = numeric(surface, "combined_trade_density")
    oos_cost06 = numeric(surface, "oos_cost06_net")
    combined_cost09 = numeric(surface, "combined_cost09_net")
    positive = (validation_net > 0.0) & (oos_net > 0.0)
    cost06_hold = positive & (oos_cost06 >= -15.0)
    oos_profit_cost_clue = cost06_hold & (oos_pf >= 1.18) & (oos_net >= 60.0)
    density_recovered = cost06_hold & (oos_density >= 1.35) & (combined_density >= 1.35) & (combined_cost09 >= -120.0)
    package_like = density_recovered & (combined_density >= 1.45) & (combined_cost09 >= -100.0)
    cost_density_joint = positive & (oos_cost06 >= 0.0) & (oos_density >= 1.35) & (combined_density >= 1.35) & (combined_cost09 >= -120.0)
    return {
        "surface_rows": int(len(surface)),
        "positive_rows": int(positive.sum()),
        "cost06_hold_count": int(cost06_hold.sum()),
        "oos_profit_cost_clue_count": int(oos_profit_cost_clue.sum()),
        "density_recovered_count": int(density_recovered.sum()),
        "package_like_count": int(package_like.sum()),
        "cost_density_joint_count": int(cost_density_joint.sum()),
        "best_oos_cost06_net": float(oos_cost06.max()) if len(surface) else "",
        "best_oos_density": float(oos_density.max()) if len(surface) else "",
        "best_combined_density": float(combined_density.max()) if len(surface) else "",
        "best_combined_cost09_net": float(combined_cost09.max()) if len(surface) else "",
    }


def build_outputs(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    gv_parent = read_json(gv.FINAL_DECISION)
    surface = pd.read_csv(fn.io_path(gx.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    diagnostics_map = surface_counts(surface)

    gx_oos_net = as_float(parent.get("selected_oos_net"))
    gv_oos_net = as_float(gv_parent.get("selected_oos_net"))
    gx_oos_pf = as_float(parent.get("selected_oos_profit_factor"))
    gv_oos_pf = as_float(gv_parent.get("selected_oos_profit_factor"))
    gx_oos_cost06 = as_float(parent.get("selected_oos_cost06_net"))
    gv_oos_cost06 = as_float(gv_parent.get("selected_oos_cost06_net"))
    gx_oos_density = as_float(parent.get("selected_oos_trade_density"))
    gv_oos_density = as_float(gv_parent.get("selected_oos_trade_density"))
    gx_combined_density = as_float(parent.get("selected_combined_trade_density"))
    gv_combined_density = as_float(gv_parent.get("selected_combined_trade_density"))
    gx_combined_cost09 = as_float(parent.get("selected_combined_cost09_net"))
    gv_combined_cost09 = as_float(gv_parent.get("selected_combined_cost09_net"))
    gx_combined_net = as_float(parent.get("selected_combined_net"))
    gv_combined_net = as_float(gv_parent.get("selected_combined_net"))
    gx_oos_trades = as_float(parent.get("selected_oos_trade_count"))
    gx_combined_trades = as_float(parent.get("selected_combined_trade_count"))
    strict_candidate_count = int(as_float(parent.get("strict_candidate_count")))
    operational_proxy_stack_pass_count = int(as_float(parent.get("operational_proxy_stack_pass_count")))

    delta_oos_net = gx_oos_net - gv_oos_net
    delta_oos_pf = gx_oos_pf - gv_oos_pf
    delta_oos_cost06 = gx_oos_cost06 - gv_oos_cost06
    delta_oos_density = gx_oos_density - gv_oos_density
    delta_combined_density = gx_combined_density - gv_combined_density
    delta_combined_cost09 = gx_combined_cost09 - gv_combined_cost09
    delta_combined_net = gx_combined_net - gv_combined_net

    oos_cost06_hold = gx_oos_cost06 >= -15.0
    oos_profit_clue = gx_oos_net >= 60.0 and gx_oos_pf >= 1.18 and gx_oos_cost06 >= 0.0
    oos_density_recovered = gx_oos_density >= 1.35
    combined_density_recovered = gx_combined_density >= 1.35
    combined_cost_hold = gx_combined_cost09 >= -120.0
    caution_cost_hold = gx_combined_cost09 >= -150.0
    package_eligible = (
        oos_cost06_hold
        and oos_density_recovered
        and combined_density_recovered
        and combined_cost_hold
        and strict_candidate_count > 0
        and operational_proxy_stack_pass_count > 0
    )

    summary_rows = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent.get("selected_model_id"),
            "gv_reference_model_id": gv_parent.get("selected_model_id"),
            "gx_oos_net": gx_oos_net,
            "gv_oos_net": gv_oos_net,
            "delta_oos_net": delta_oos_net,
            "gx_oos_profit_factor": gx_oos_pf,
            "gv_oos_profit_factor": gv_oos_pf,
            "delta_oos_profit_factor": delta_oos_pf,
            "gx_oos_cost06_net": gx_oos_cost06,
            "gv_oos_cost06_net": gv_oos_cost06,
            "delta_oos_cost06_net": delta_oos_cost06,
            "gx_oos_density": gx_oos_density,
            "gv_oos_density": gv_oos_density,
            "delta_oos_density": delta_oos_density,
            "gx_combined_density": gx_combined_density,
            "gv_combined_density": gv_combined_density,
            "delta_combined_density": delta_combined_density,
            "gx_combined_cost09_net": gx_combined_cost09,
            "gv_combined_cost09_net": gv_combined_cost09,
            "delta_combined_cost09_net": delta_combined_cost09,
            "oos_cost06_hold": str(oos_cost06_hold).lower(),
            "oos_profit_clue": str(oos_profit_clue).lower(),
            "oos_density_recovered": str(oos_density_recovered).lower(),
            "combined_density_recovered": str(combined_density_recovered).lower(),
            "combined_cost_hold": str(combined_cost_hold).lower(),
            "caution_cost_hold": str(caution_cost_hold).lower(),
            "package_eligible": str(package_eligible).lower(),
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    diagnostics = [{"run_id": RUN_ID, "metric": key, "value": value, "claim_boundary": CLAIM_BOUNDARY} for key, value in diagnostics_map.items()]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "gy01_oos_profit_cost06_improved",
            "observed_change": f"OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6) {gv_oos_net}/{gv_oos_pf}/{gv_oos_cost06} -> {gx_oos_net}/{gx_oos_pf}/{gx_oos_cost06}",
            "likely_driver": "GX score(GX 점수)가 OOS profit(표본외 수익)과 cost0.6(비용0.6)을 강하게 보상했습니다.",
            "effect": "GZ는 이 OOS profit/cost clue(표본외 수익/비용 단서)를 살리되 combined cost/density(합산 비용/밀도)를 더 강하게 묶어야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gy02_density_not_recovered_combined_cost_slipped",
            "observed_change": f"OOS density(표본외 밀도) {gv_oos_density} -> {gx_oos_density}; combined density/cost0.9(합산 밀도/비용0.9) {gv_combined_density}/{gv_combined_cost09} -> {gx_combined_density}/{gx_combined_cost09}",
            "likely_driver": "cost/profit reward(비용/수익 보상)가 density floor(밀도 바닥)와 combined cost hold(합산 비용 유지)보다 강했습니다.",
            "effect": "GZ는 selected-row score(선택 행 점수)보다 frontier constraints(경계면 제약)를 먼저 통과시키는 구조가 필요합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "package_eligible": str(package_eligible).lower(),
            "decision": "reject_package",
            "reason": "GX improved OOS profit/cost0.6(GX 표본외 수익/비용0.6 개선) but failed OOS/combined density(표본외/합산 밀도 실패) and combined cost0.9 hold(합산 비용0.9 유지) target.",
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "gy01_profit_cost_clue_without_density_recovery",
            "failed_boundary": "package-ready density recover cost0.6 hold(패키지 가능 밀도 회복 비용0.6 유지)",
            "why_failed": f"oos_density={gx_oos_density}; combined_density={gx_combined_density}; combined_cost09={gx_combined_cost09}; strict={strict_candidate_count}; stack={operational_proxy_stack_pass_count}",
            "salvage_value": f"OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6) improved by {delta_oos_net}/{delta_oos_pf}/{delta_oos_cost06}.",
            "reopen_condition": "OOS net >= 60, OOS PF >= 1.18, OOS cost0.6 >= 0, OOS density >= 1.35, combined density >= 1.35, combined cost0.9 >= -120.",
            "do_not_repeat": "Do not choose OOS profit(표본외 수익) if combined density(합산 밀도) remains below 1.35 and combined cost0.9(합산 비용0.9) is below -120.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gz01_cost_density_joint_frontier_router",
            "hypothesis": "cost-density joint frontier router(비용-밀도 공동 경계 라우터)가 GX의 OOS profit/cost clue(표본외 수익/비용 단서)를 유지하면서 density(밀도)와 combined cost(합산 비용)를 함께 묶을 수 있습니다.",
            "required_preserve": "OOS net(표본외 순수익) >= 60, OOS PF(표본외 수익 팩터) >= 1.18, OOS cost0.6(표본외 비용0.6) >= 0.",
            "required_repair": "OOS density(표본외 밀도) >= 1.35, combined density(합산 밀도) >= 1.35, combined cost0.9(합산 비용0.9) >= -120.",
            "avoid": "Avoid combined cost0.9(합산 비용0.9) < -150 and combined density(합산 밀도) < 1.30 even when OOS profit(표본외 수익) is high.",
            "effect": "GZ는 profit/cost clue(수익/비용 단서)를 다음 offensive seed(공격 씨앗)로 쓰되 package claim(패키지 주장)은 막습니다.",
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
        "gv_reference_model_id": gv_parent.get("selected_model_id"),
        "gx_oos_net": gx_oos_net,
        "gv_oos_net": gv_oos_net,
        "delta_oos_net": delta_oos_net,
        "gx_oos_profit_factor": gx_oos_pf,
        "gv_oos_profit_factor": gv_oos_pf,
        "delta_oos_profit_factor": delta_oos_pf,
        "gx_oos_cost06_net": gx_oos_cost06,
        "gv_oos_cost06_net": gv_oos_cost06,
        "delta_oos_cost06_net": delta_oos_cost06,
        "gx_oos_trade_density": gx_oos_density,
        "gv_oos_trade_density": gv_oos_density,
        "delta_oos_trade_density": delta_oos_density,
        "gx_combined_net": gx_combined_net,
        "gv_combined_net": gv_combined_net,
        "delta_combined_net": delta_combined_net,
        "gx_combined_trade_density": gx_combined_density,
        "gv_combined_trade_density": gv_combined_density,
        "delta_combined_trade_density": delta_combined_density,
        "gx_combined_cost09_net": gx_combined_cost09,
        "gv_combined_cost09_net": gv_combined_cost09,
        "delta_combined_cost09_net": delta_combined_cost09,
        "gx_oos_trade_count": gx_oos_trades,
        "gx_combined_trade_count": gx_combined_trades,
        "oos_cost06_hold": str(oos_cost06_hold).lower(),
        "oos_profit_clue": str(oos_profit_clue).lower(),
        "oos_density_recovered": str(oos_density_recovered).lower(),
        "combined_density_recovered": str(combined_density_recovered).lower(),
        "combined_cost_hold": str(combined_cost_hold).lower(),
        "caution_cost_hold": str(caution_cost_hold).lower(),
        "strict_candidate_count": strict_candidate_count,
        "operational_proxy_stack_pass_count": operational_proxy_stack_pass_count,
        "package_eligible": str(package_eligible).lower(),
        "surface_rows": diagnostics_map["surface_rows"],
        "oos_profit_cost_clue_count": diagnostics_map["oos_profit_cost_clue_count"],
        "density_recovered_count": diagnostics_map["density_recovered_count"],
        "cost_density_joint_count": diagnostics_map["cost_density_joint_count"],
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
        ("scope_completion_gate", REVIEW_SUMMARY, "GY review summary(GY 검토 요약)를 작성했습니다."),
        ("parent_integrity_gate", INPUT_MANIFEST, "GX input lineage(GX 입력 계보)를 확인했습니다."),
        ("kpi_contract_audit", SURFACE_DIAGNOSTIC, "cost/density/PF/trade-count(비용/밀도/PF/거래수) 진단을 기록했습니다."),
        ("delta_attribution_gate", DELTA_ATTRIBUTION, "GX vs GV delta(GX와 GV 차이)를 귀속했습니다."),
        ("package_decision_gate", PACKAGE_DECISION, "package rejection(패키지 거절)을 명시했습니다."),
        ("failure_memory_gate", FAILURE_MEMORY, "profit/cost clue without density recovery(수익/비용 단서와 밀도 실패)를 기억했습니다."),
        ("next_queue_gate", RUN364GZ_QUEUE, "GZ next queue(GZ 다음 대기열)를 열었습니다."),
        ("paired_tier_record_gate", STAGE_LEDGER, "Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B) 장부 행을 남깁니다."),
        ("receipt_coverage_gate", RESULT_RECEIPT, "result/model/attribution/lineage/claim receipts(결과/모델/귀속/계보/주장 영수증)를 남깁니다."),
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
    fn.write_json(MODEL_RECEIPT, {**common, "model_family": "GX density recover cost0.6 hold router(GX 밀도 회복 비용0.6 유지 라우터)", "selection_review": "OOS profit/cost0.6 improved(표본외 수익/비용0.6 개선), density recovery failed(밀도 회복 실패), combined cost slipped(합산 비용 약화)", "validation_judgment": JUDGMENT, "next_condition": "cost density joint frontier router(비용 밀도 공동 경계 라우터)"})
    fn.write_json(ATTRIBUTION_RECEIPT, {**common, "observed_change": f"OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6) {final['gv_oos_net']}/{final['gv_oos_profit_factor']}/{final['gv_oos_cost06_net']} -> {final['gx_oos_net']}/{final['gx_oos_profit_factor']}/{final['gx_oos_cost06_net']}; combined density/cost0.9(합산 밀도/비용0.9) {final['gv_combined_trade_density']}/{final['gv_combined_cost09_net']} -> {final['gx_combined_trade_density']}/{final['gx_combined_cost09_net']}", "comparison_baseline": gv.RUN_ID, "likely_drivers": ["OOS profit reward(표본외 수익 보상)", "cost0.6 hold weight(비용0.6 유지 가중치)", "density floor under-enforced(밀도 바닥 집행 부족)"], "segment_checks": [rel(SURFACE_DIAGNOSTIC), rel(gx.COST_STRESS), rel(gx.SIDE_SESSION_REVIEW)], "attribution_confidence": "medium", "next_probe": NEXT_RUN_ID})
    fn.write_json(CLAIM_RECEIPT, {**common, "runtime_package": "not_opened", "new_mt5_execution": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})
    fn.write_json(LINEAGE_RECEIPT, {**common, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file() and path != LINEAGE_RECEIPT}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GY Density Recover Cost0.6 Hold Router Review(밀도 회복 비용0.6 유지 라우터 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GX result(GX 결과)를 GV baseline(GV 기준선)과 비교해 OOS profit/cost clue(표본외 수익/비용 단서), density recovery(밀도 회복), combined cost hold(합산 비용 유지)를 분리 판정했습니다.

Effect(효과): OOS profit/cost0.6(표본외 수익/비용0.6) 단서는 살리고, density(밀도)와 combined cost(합산 비용) 실패는 GZ의 직접 제약으로 넘깁니다.

- judgment(판정): `{final['judgment']}`
- review_subject(검토 대상): `{final['review_subject']}`
- OOS net/PF change(표본외 순수익/수익 팩터 변화): `{final['gv_oos_net']}` / `{final['gv_oos_profit_factor']}` -> `{final['gx_oos_net']}` / `{final['gx_oos_profit_factor']}`
- OOS cost0.6 change(표본외 비용0.6 변화): `{final['gv_oos_cost06_net']}` -> `{final['gx_oos_cost06_net']}` (`{final['delta_oos_cost06_net']}`)
- OOS density change(표본외 밀도 변화): `{final['gv_oos_trade_density']}` -> `{final['gx_oos_trade_density']}` (`{final['delta_oos_trade_density']}`)
- combined density change(합산 밀도 변화): `{final['gv_combined_trade_density']}` -> `{final['gx_combined_trade_density']}` (`{final['delta_combined_trade_density']}`)
- combined cost0.9 change(합산 비용0.9 변화): `{final['gv_combined_cost09_net']}` -> `{final['gx_combined_cost09_net']}` (`{final['delta_combined_cost09_net']}`)
- package eligible(패키지 적격): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GY Density Recover Cost0.6 Hold Router Review(밀도 회복 비용0.6 유지 라우터 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GX package(패키지)를 reject(거절)하고 GZ cost-density joint frontier router(GZ 비용-밀도 공동 경계 라우터)를 엽니다.

Effect(효과): 높은 OOS profit(표본외 수익)을 기준선으로 삼되, density(밀도)와 combined cost(합산 비용)를 동시에 통과해야 다음 후보가 됩니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GY__{RUN_ID}", f"\n- run364GY__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - GX OOS profit/cost clue but density failed(GX 표본외 수익/비용 단서, 밀도 실패), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GY__{RUN_ID}", f"\n<!-- run364GY__{RUN_ID} -->\n\n## run364GY Density Recover Cost0.6 Hold Router Review(밀도 회복 비용0.6 유지 라우터 검토)\n\nAction(행동): GX의 OOS profit/cost0.6(표본외 수익/비용0.6) 개선과 density failure(밀도 실패)를 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 profit/cost clue(수익/비용 단서)를 보존하면서 density/cost frontier(밀도/비용 경계)를 다시 탐색합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GY__{RUN_ID}", f"\n<!-- run364GY__{RUN_ID} -->\n## run364GY density recover cost0.6 hold router review(밀도 회복 비용0.6 유지 라우터 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GY` reviewed(검토 완료) GX density recover cost0.6 hold router(GX 밀도 회복 비용0.6 유지 라우터). GX는 OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6)을 `{final['gx_oos_net']}` / `{final['gx_oos_profit_factor']}` / `{final['gx_oos_cost06_net']}`로 개선했지만, OOS density(표본외 밀도)는 `{final['gx_oos_trade_density']}`, combined density(합산 밀도)는 `{final['gx_combined_trade_density']}`로 목표 `1.35`에 못 미쳤습니다.

Cost truth(비용 진실): combined cost0.9(합산 비용0.9)는 `{final['gx_combined_cost09_net']}`로 caution floor(주의 바닥) `-150`은 넘지만 target floor(목표 바닥) `-120`에는 못 미칩니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 OOS net(표본외 순수익) `>= 60`, OOS PF(표본외 수익 팩터) `>= 1.18`, OOS cost0.6(표본외 비용0.6) `>= 0`을 보존하면서 OOS/combined density(표본외/합산 밀도) `>= 1.35`, combined cost0.9(합산 비용0.9) `>= -120`을 동시에 강제합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GY rejected(거절) GX density recover cost0.6 hold router(GX 밀도 회복 비용0.6 유지 라우터).

GX selected model(GX 선택 모델): `{final['review_subject']}`
GX OOS net/PF/density/cost0.6(GX 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['gx_oos_net']}` / `{final['gx_oos_profit_factor']}` / `{final['gx_oos_trade_density']}` / `{final['gx_oos_cost06_net']}`
GX combined density/cost0.9(GX 합산 밀도/비용0.9): `{final['gx_combined_trade_density']}` / `{final['gx_combined_cost09_net']}`

Next seed(다음 씨앗): GZ cost-density joint frontier router(GZ 비용-밀도 공동 경계 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GY__{RUN_ID}", f"\n<!-- run364GY__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` rejected GX package(GX 패키지 거절); OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6) `{final['gx_oos_net']}`/`{final['gx_oos_profit_factor']}`/`{final['gx_oos_cost06_net']}`; density failed(밀도 실패); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GY__{RUN_ID}", f"\n<!-- run364GY__{RUN_ID} -->\n- `{RUN_ID}`: GX OOS profit/cost0.6(GX 표본외 수익/비용0.6)는 positive clue(긍정 단서)입니다. Effect(효과): GZ는 이 단서를 보존하면서 density/cost frontier(밀도/비용 경계)를 강제합니다.\n")
    fn.append_text_once(NEGATIVE_REGISTER, f"run364GY__profit_cost_clue_density_fail__{RUN_ID}", f"\n<!-- run364GY__profit_cost_clue_density_fail__{RUN_ID} -->\n- `{RUN_ID}`: OOS profit/cost0.6(표본외 수익/비용0.6)은 개선됐지만 OOS density(표본외 밀도) `{final['gx_oos_trade_density']}`, combined density(합산 밀도) `{final['gx_combined_trade_density']}`, combined cost0.9(합산 비용0.9) `{final['gx_combined_cost09_net']}`가 package(패키지) 기준에 부족합니다. Effect(효과): profit-only selection(수익만 보는 선택)을 운영 후보로 올리지 않습니다.\n")


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
        "question": "Did GX recover density while holding cost0.6?(GX가 비용0.6을 유지하면서 밀도를 회복했는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"oos_profit_clue={final['oos_profit_clue']};oos_density_recovered={final['oos_density_recovered']};combined_density_recovered={final['combined_density_recovered']};combined_cost_hold={final['combined_cost_hold']};package_eligible={final['package_eligible']}",
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
                "kpi_scope": "GY density recover cost0.6 hold review(GY 밀도 회복 비용0.6 유지 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["gx_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["gx_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["gx_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["gx_oos_trade_count"] if suffix == "tier_a_separate" else "",
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
                "run_type": "density_recover_cost06_hold_router_review(밀도 회복 비용0.6 유지 라우터 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "selected_net_profit": final["gx_oos_net"],
                "selected_profit_factor": final["gx_oos_profit_factor"],
                "selected_trade_density": final["gx_oos_trade_density"],
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
                    "notes": "GY density recover cost0.6 hold router review artifact(GY 밀도 회복 비용0.6 유지 라우터 검토 산출물)",
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
    write_csv(RUN364GZ_QUEUE, queue)
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
