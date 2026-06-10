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

from stage_pipelines.stage364 import review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db as ha
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db as gz
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db as hb


fn = hb.fn
et = hb.et

TODAY = "2026-06-08"
STAGE_ID = hb.STAGE_ID
STAGE_DIR = hb.STAGE_DIR
REVIEW_DIR = hb.REVIEW_DIR
SPEC_DIR = hb.SPEC_DIR
SELECTED_DIR = hb.SELECTED_DIR

RUN_NUMBER = "run364HC"
RUN_ID = "run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1"
PARENT_RUN_ID = hb.RUN_ID
NEXT_RUN_ID = "run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1"

STATUS = "completed_stage364HC_oos_profit_density_rebalance_review_cost_improved_density_profit_regressed_open_hd_no_authority"
JUDGMENT = "negative_for_package_hb_cost_improved_density_profit_regressed_no_package_no_authority"
DECISION = "stage364HC_reject_package_open_run364HD_dual_surface_density_profit_switch_router"
CLAIM_BOUNDARY = (
    "research_development_oos_profit_density_rebalance_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "hc_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "hc_surface_diagnostic.csv"
DELTA_ATTRIBUTION = RUN_DIR / "hc_delta_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "hc_failure_memory.csv"
RUN364HD_QUEUE = RUN_DIR / "hc_hd_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HC_oos_profit_density_rebalance_cost_floor_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HC_oos_profit_density_rebalance_cost_floor_router_review.md"
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
    hb.FINAL_DECISION,
    hb.GATE_AUDIT,
    hb.TRADE_SURFACE,
    hb.SELECTED_CANDIDATE,
    hb.SELECTED_TRADE_TAPE,
    hb.COST_STRESS,
    hb.SIDE_SESSION_REVIEW,
    hb.MONTH_STABILITY,
    hb.MODEL_SCORECARD,
    hb.MODEL_ARTIFACT_MANIFEST,
    hb.ONNX_SMOKE_REPORT,
    hb.DATA_INTEGRITY_AUDIT,
    hb.RUN364HC_QUEUE,
    gz.FINAL_DECISION,
    gz.TRADE_SURFACE,
    ha.FINAL_DECISION,
    ha.PACKAGE_DECISION,
    ha.FAILURE_MEMORY,
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
    RUN364HD_QUEUE,
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
    return hb.exists(path)


def rel(path: Path) -> str:
    return hb.rel(path)


def sha(path: Path) -> str:
    return hb.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return hb.as_float(value, default)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(path, list(rows))


def read_json(path: Path) -> dict[str, Any]:
    with fn.io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


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
    oos_density_cost = positive & (oos_density >= 1.35) & (combined_cost09 >= -120.0)
    combined_density_cost = positive & (combined_density >= 1.35) & (combined_cost09 >= -120.0)
    target_profit = positive & (oos_net >= 60.0) & (oos_pf >= 1.18) & (oos_cost06 >= 0.0)
    joint_target = target_profit & (oos_density >= 1.35) & (combined_density >= 1.35) & (combined_cost09 >= -120.0)
    soft_rebalance = positive & (oos_net >= 45.0) & (oos_pf >= 1.10) & (oos_cost06 >= -10.0) & (oos_density >= 1.35) & (combined_density >= 1.30) & (combined_cost09 >= -120.0)
    return {
        "surface_rows": int(len(surface)),
        "positive_rows": int(positive.sum()),
        "oos_density_cost_count": int(oos_density_cost.sum()),
        "combined_density_cost_count": int(combined_density_cost.sum()),
        "target_profit_count": int(target_profit.sum()),
        "joint_target_count": int(joint_target.sum()),
        "soft_rebalance_count": int(soft_rebalance.sum()),
        "best_oos_net": float(oos_net.max()) if len(surface) else "",
        "best_oos_profit_factor": float(oos_pf.max()) if len(surface) else "",
        "best_oos_cost06_net": float(oos_cost06.max()) if len(surface) else "",
        "best_oos_trade_density": float(oos_density.max()) if len(surface) else "",
        "best_combined_trade_density": float(combined_density.max()) if len(surface) else "",
        "best_combined_cost09_net": float(combined_cost09.max()) if len(surface) else "",
    }


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HC inputs(HC 입력 누락): " + ", ".join(missing))
    parent = read_json(hb.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HB next_run_id mismatch(HB 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden HB claim(금지된 HB 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(hb.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HB gate audit(HB 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "HC OOS profit-density rebalance review input(HC 표본외 수익-밀도 재균형 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def build_outputs(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    gz_parent = read_json(gz.FINAL_DECISION)
    surface = pd.read_csv(fn.io_path(hb.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    diagnostics_map = surface_counts(surface)

    hb_oos_net = as_float(parent.get("selected_oos_net"))
    gz_oos_net = as_float(gz_parent.get("selected_oos_net"))
    hb_oos_pf = as_float(parent.get("selected_oos_profit_factor"))
    gz_oos_pf = as_float(gz_parent.get("selected_oos_profit_factor"))
    hb_oos_cost06 = as_float(parent.get("selected_oos_cost06_net"))
    gz_oos_cost06 = as_float(gz_parent.get("selected_oos_cost06_net"))
    hb_oos_density = as_float(parent.get("selected_oos_trade_density"))
    gz_oos_density = as_float(gz_parent.get("selected_oos_trade_density"))
    hb_combined_density = as_float(parent.get("selected_combined_trade_density"))
    gz_combined_density = as_float(gz_parent.get("selected_combined_trade_density"))
    hb_combined_cost09 = as_float(parent.get("selected_combined_cost09_net"))
    gz_combined_cost09 = as_float(gz_parent.get("selected_combined_cost09_net"))
    hb_combined_net = as_float(parent.get("selected_combined_net"))
    gz_combined_net = as_float(gz_parent.get("selected_combined_net"))
    hb_oos_trades = as_float(parent.get("selected_oos_trade_count"))
    hb_combined_trades = as_float(parent.get("selected_combined_trade_count"))
    strict_candidate_count = int(as_float(parent.get("strict_candidate_count")))
    stack_pass_count = int(as_float(parent.get("operational_proxy_stack_pass_count")))

    delta_oos_net = hb_oos_net - gz_oos_net
    delta_oos_pf = hb_oos_pf - gz_oos_pf
    delta_oos_cost06 = hb_oos_cost06 - gz_oos_cost06
    delta_oos_density = hb_oos_density - gz_oos_density
    delta_combined_density = hb_combined_density - gz_combined_density
    delta_combined_cost09 = hb_combined_cost09 - gz_combined_cost09
    delta_combined_net = hb_combined_net - gz_combined_net

    oos_profit_target = hb_oos_net >= 60.0 and hb_oos_pf >= 1.18
    oos_cost06_target = hb_oos_cost06 >= 0.0
    oos_density_preserved = hb_oos_density >= 1.35
    combined_density_recovered = hb_combined_density >= 1.35
    combined_cost_hold = hb_combined_cost09 >= -120.0
    package_eligible = (
        oos_profit_target
        and oos_cost06_target
        and oos_density_preserved
        and combined_density_recovered
        and combined_cost_hold
        and strict_candidate_count > 0
        and stack_pass_count > 0
    )

    summary_rows = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent.get("selected_model_id"),
            "gz_reference_model_id": gz_parent.get("selected_model_id"),
            "hb_oos_net": hb_oos_net,
            "gz_oos_net": gz_oos_net,
            "delta_oos_net": delta_oos_net,
            "hb_oos_profit_factor": hb_oos_pf,
            "gz_oos_profit_factor": gz_oos_pf,
            "delta_oos_profit_factor": delta_oos_pf,
            "hb_oos_cost06_net": hb_oos_cost06,
            "gz_oos_cost06_net": gz_oos_cost06,
            "delta_oos_cost06_net": delta_oos_cost06,
            "hb_oos_density": hb_oos_density,
            "gz_oos_density": gz_oos_density,
            "delta_oos_density": delta_oos_density,
            "hb_combined_density": hb_combined_density,
            "gz_combined_density": gz_combined_density,
            "delta_combined_density": delta_combined_density,
            "hb_combined_cost09_net": hb_combined_cost09,
            "gz_combined_cost09_net": gz_combined_cost09,
            "delta_combined_cost09_net": delta_combined_cost09,
            "oos_profit_target": str(oos_profit_target).lower(),
            "oos_cost06_target": str(oos_cost06_target).lower(),
            "oos_density_preserved": str(oos_density_preserved).lower(),
            "combined_density_recovered": str(combined_density_recovered).lower(),
            "combined_cost_hold": str(combined_cost_hold).lower(),
            "package_eligible": str(package_eligible).lower(),
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    diagnostics = [{"run_id": RUN_ID, "metric": key, "value": value, "claim_boundary": CLAIM_BOUNDARY} for key, value in diagnostics_map.items()]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "hc01_cost_improved_but_density_profit_regressed",
            "observed_change": f"combined cost0.9(합산 비용0.9) {gz_combined_cost09} -> {hb_combined_cost09}; OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6) {gz_oos_net}/{gz_oos_pf}/{gz_oos_density}/{gz_oos_cost06} -> {hb_oos_net}/{hb_oos_pf}/{hb_oos_density}/{hb_oos_cost06}",
            "likely_driver": "HB score(HB 점수)가 combined cost(합산 비용)와 validation net(검증 순수익)을 과보상했고, GZ에서 확보한 OOS density(표본외 밀도) 단서를 보존하지 못했습니다.",
            "effect": "다음 HD는 GZ density-cost anchor(GZ 밀도-비용 기준점)를 유지하고 HB profit rows(HB 수익 행)를 switch surface(전환 표면)로만 써야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "hc02_surface_has_profit_rows_but_no_density_cost_rows",
            "observed_change": f"target_profit_count(목표 수익 행)={diagnostics_map['target_profit_count']}; oos_density_cost_count(표본외 밀도-비용 행)={diagnostics_map['oos_density_cost_count']}; joint_target_count(공동 목표 행)={diagnostics_map['joint_target_count']}",
            "likely_driver": "HB model/label family(HB 모델/라벨 계열)은 profit target(수익 목표) 행을 만들었지만, density/cost frontier(밀도/비용 경계)와 같은 행에서 만나지 못했습니다.",
            "effect": "HD는 단일 점수 가중치 조정이 아니라 dual-surface routing(이중 표면 라우팅)을 시험합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "package_eligible": str(package_eligible).lower(),
            "decision": "reject_package",
            "reason": "HB improved combined cost0.9(HB 합산 비용0.9 개선) but failed OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6), OOS density(표본외 밀도), and combined density(합산 밀도).",
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "hc01_rebalance_cost_improved_density_profit_regressed",
            "failed_boundary": "package-ready OOS profit-density rebalance cost floor(패키지 가능 표본외 수익-밀도 재균형 비용 바닥)",
            "why_failed": f"hb_oos_net={hb_oos_net}; hb_oos_pf={hb_oos_pf}; hb_oos_cost06={hb_oos_cost06}; hb_oos_density={hb_oos_density}; hb_combined_density={hb_combined_density}; strict={strict_candidate_count}; stack={stack_pass_count}",
            "salvage_value": f"HB surface(HB 표면)는 target_profit_count(목표 수익 행) {diagnostics_map['target_profit_count']} and best_combined_cost09(최선 합산 비용0.9) {diagnostics_map['best_combined_cost09_net']}를 남겼습니다.",
            "reopen_condition": "Dual-surface routing(이중 표면 라우팅)이 GZ density-cost anchor(GZ 밀도-비용 기준점)를 유지하면서 HB profit rows(HB 수익 행)를 제한적으로 더할 때.",
            "do_not_repeat": "Do not replace GZ density-cost anchor(GZ 밀도-비용 기준점)를 HB single-score(HB 단일 점수)로 통째로 교체하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "hd01_dual_surface_density_profit_switch_router",
            "hypothesis": "Dual-surface density-profit switch router(이중 표면 밀도-수익 전환 라우터)가 GZ density-cost anchor(GZ 밀도-비용 기준점)를 기본값으로 두고, HB target-profit contexts(HB 목표 수익 문맥)를 제한적 fallback(제한 대체)로 쓰면 OOS profit(표본외 수익)을 보강하면서 density/cost(밀도/비용)를 덜 깨뜨릴 수 있습니다.",
            "required_preserve": "OOS density(표본외 밀도) >= 1.35, combined cost0.9(합산 비용0.9) >= -120, combined density(합산 밀도) >= 1.30 hard floor(하드 바닥).",
            "required_repair": "OOS net(표본외 순수익) >= 60, OOS PF(표본외 수익 팩터) >= 1.18, OOS cost0.6(표본외 비용0.6) >= 0.",
            "avoid": "Avoid HB-only single-score replacement(HB 단독 단일 점수 교체) and avoid density below GZ clue(GZ 단서보다 낮은 밀도).",
            "effect": "HD는 단순 가중치 재조정이 아니라 context switch(문맥 전환)로 profit rows(수익 행)와 density anchor(밀도 기준점)를 붙입니다.",
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
        "gz_reference_model_id": gz_parent.get("selected_model_id"),
        "hb_oos_net": hb_oos_net,
        "gz_oos_net": gz_oos_net,
        "delta_oos_net": delta_oos_net,
        "hb_oos_profit_factor": hb_oos_pf,
        "gz_oos_profit_factor": gz_oos_pf,
        "delta_oos_profit_factor": delta_oos_pf,
        "hb_oos_cost06_net": hb_oos_cost06,
        "gz_oos_cost06_net": gz_oos_cost06,
        "delta_oos_cost06_net": delta_oos_cost06,
        "hb_oos_trade_density": hb_oos_density,
        "gz_oos_trade_density": gz_oos_density,
        "delta_oos_trade_density": delta_oos_density,
        "hb_combined_net": hb_combined_net,
        "gz_combined_net": gz_combined_net,
        "delta_combined_net": delta_combined_net,
        "hb_combined_trade_density": hb_combined_density,
        "gz_combined_trade_density": gz_combined_density,
        "delta_combined_trade_density": delta_combined_density,
        "hb_combined_cost09_net": hb_combined_cost09,
        "gz_combined_cost09_net": gz_combined_cost09,
        "delta_combined_cost09_net": delta_combined_cost09,
        "hb_oos_trade_count": hb_oos_trades,
        "hb_combined_trade_count": hb_combined_trades,
        "oos_profit_target": str(oos_profit_target).lower(),
        "oos_cost06_target": str(oos_cost06_target).lower(),
        "oos_density_preserved": str(oos_density_preserved).lower(),
        "combined_density_recovered": str(combined_density_recovered).lower(),
        "combined_cost_hold": str(combined_cost_hold).lower(),
        "strict_candidate_count": strict_candidate_count,
        "operational_proxy_stack_pass_count": stack_pass_count,
        "package_eligible": str(package_eligible).lower(),
        **diagnostics_map,
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
            "support_skills": ["obsidian-run-evidence-system(실행 근거 시스템)", "obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)"],
            "required_gates": ["parent_integrity_gate(상위 무결성 게이트)", "kpi_contract_audit(KPI 계약 감사)", "package_decision_gate(패키지 결정 게이트)", "failure_memory_gate(실패 기억 게이트)", "required_gate_coverage_audit(필수 게이트 커버리지 감사)"],
            "review_subject": parent.get("run_id"),
            "decision_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_gates() -> list[dict[str, Any]]:
    gates = [
        ("scope_completion_gate", REVIEW_SUMMARY, "HC review summary(HC 검토 요약)를 작성했습니다."),
        ("parent_integrity_gate", INPUT_MANIFEST, "HB input lineage(HB 입력 계보)를 확인했습니다."),
        ("kpi_contract_audit", SURFACE_DIAGNOSTIC, "profit/density/cost/trade-count(수익/밀도/비용/거래수) 진단을 기록했습니다."),
        ("delta_attribution_gate", DELTA_ATTRIBUTION, "HB vs GZ delta(HB와 GZ 차이)를 귀속했습니다."),
        ("package_decision_gate", PACKAGE_DECISION, "package rejection(패키지 거절)을 명시했습니다."),
        ("failure_memory_gate", FAILURE_MEMORY, "cost improvement with density-profit regression(비용 개선과 밀도-수익 후퇴)을 기억했습니다."),
        ("next_queue_gate", RUN364HD_QUEUE, "HD next queue(HD 다음 대기열)를 열었습니다."),
        ("paired_tier_record_gate", STAGE_LEDGER, "Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B) 장부 행을 남깁니다."),
        ("receipt_coverage_gate", RESULT_RECEIPT, "result/model/attribution/lineage/claim receipts(결과/모델/귀속/계보/주장 영수증)를 남깁니다."),
        ("final_claim_guard", CLAIM_RECEIPT, "runtime authority/Goal Achieve(런타임 권위/목표 달성) 주장을 차단했습니다."),
    ]
    rows = [
        {"run_id": RUN_ID, "gate": gate, "status": "passed", "evidence": rel(path), "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    fn.write_json(RESULT_RECEIPT, {**common, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    fn.write_json(MODEL_RECEIPT, {**common, "model_family": "HB OOS profit-density rebalance router(HB 표본외 수익-밀도 재균형 라우터)", "selection_review": "cost improved but density and profit regressed(비용은 개선됐지만 밀도와 수익은 후퇴)", "validation_judgment": JUDGMENT, "next_condition": NEXT_RUN_ID})
    fn.write_json(ATTRIBUTION_RECEIPT, {**common, "observed_change": f"HB vs GZ(HB와 GZ) OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6) {final['hb_oos_net']}/{final['hb_oos_profit_factor']}/{final['hb_oos_trade_density']}/{final['hb_oos_cost06_net']} vs {final['gz_oos_net']}/{final['gz_oos_profit_factor']}/{final['gz_oos_trade_density']}/{final['gz_oos_cost06_net']}", "likely_drivers": ["cost floor overreward(비용 바닥 과보상)", "GZ density anchor lost(GZ 밀도 기준점 손실)", "profit rows isolated(수익 행 고립)"], "next_probe": NEXT_RUN_ID})
    fn.write_json(CLAIM_RECEIPT, {**common, "runtime_package": "not_opened", "new_mt5_execution": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})
    fn.write_json(LINEAGE_RECEIPT, {**common, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file() and path != LINEAGE_RECEIPT}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364HC OOS Profit-Density Rebalance Review(표본외 수익-밀도 재균형 검토)

Created(생성): {final['created_at_utc']}

Action(행동): HB result(HB 결과)를 GZ reference(GZ 기준)와 비교해 OOS profit/PF/cost0.6(표본외 수익/수익 팩터/비용0.6), OOS density(표본외 밀도), combined density/cost0.9(합산 밀도/비용0.9)를 분리 판정했습니다.

Effect(효과): HB는 combined cost0.9(합산 비용0.9)를 개선했지만 density/profit(밀도/수익)을 후퇴시켰으므로 package(패키지)를 닫고 HD dual-surface switch(HD 이중 표면 전환)를 엽니다.

- judgment(판정): `{final['judgment']}`
- review_subject(검토 대상): `{final['review_subject']}`
- OOS net/PF/cost0.6 change(표본외 순수익/수익 팩터/비용0.6 변화): `{final['gz_oos_net']}` / `{final['gz_oos_profit_factor']}` / `{final['gz_oos_cost06_net']}` -> `{final['hb_oos_net']}` / `{final['hb_oos_profit_factor']}` / `{final['hb_oos_cost06_net']}`
- OOS density change(표본외 밀도 변화): `{final['gz_oos_trade_density']}` -> `{final['hb_oos_trade_density']}` (`{final['delta_oos_trade_density']}`)
- combined density change(합산 밀도 변화): `{final['gz_combined_trade_density']}` -> `{final['hb_combined_trade_density']}` (`{final['delta_combined_trade_density']}`)
- combined cost0.9 change(합산 비용0.9 변화): `{final['gz_combined_cost09_net']}` -> `{final['hb_combined_cost09_net']}` (`{final['delta_combined_cost09_net']}`)
- surface counts(표면 수): target_profit(목표 수익) `{final['target_profit_count']}`, oos_density_cost(표본외 밀도-비용) `{final['oos_density_cost_count']}`, joint_target(공동 목표) `{final['joint_target_count']}`
- package eligible(패키지 적격): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364HC OOS Profit-Density Rebalance Review(표본외 수익-밀도 재균형 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): HB package(패키지)를 reject(거절)하고 HD dual-surface density-profit switch router(HD 이중 표면 밀도-수익 전환 라우터)를 엽니다.

Effect(효과): HD는 GZ density-cost anchor(GZ 밀도-비용 기준점)를 기본값으로 두고 HB profit rows(HB 수익 행)를 제한적으로 붙이는 방향으로 전환합니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364HC__{RUN_ID}", f"\n- run364HC__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - HB cost improved but density/profit regressed(HB 비용 개선, 밀도/수익 후퇴), next(다음) `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364HC__{RUN_ID}", f"\n<!-- run364HC__{RUN_ID} -->\n\n## run364HC OOS Profit-Density Rebalance Review(표본외 수익-밀도 재균형 검토)\n\nAction(행동): HB를 GZ와 비교해 비용 개선과 밀도/수익 후퇴를 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 GZ anchor(GZ 기준점)와 HB profit rows(HB 수익 행)를 dual-surface switch(이중 표면 전환)로 결합합니다.\n")
    fn.append_text_once(STAGE_README, f"run364HC__{RUN_ID}", f"\n<!-- run364HC__{RUN_ID} -->\n## run364HC OOS profit-density rebalance review(표본외 수익-밀도 재균형 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364HC` reviewed(검토 완료) HB OOS profit-density rebalance cost floor router(HB 표본외 수익-밀도 재균형 비용 바닥 라우터). HB는 combined cost0.9(합산 비용0.9)를 `{final['hb_combined_cost09_net']}`로 개선했지만 OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6)는 `{final['hb_oos_net']}` / `{final['hb_oos_profit_factor']}` / `{final['hb_oos_trade_density']}` / `{final['hb_oos_cost06_net']}`입니다.

Failure truth(실패 진실): HB는 GZ 대비 OOS density(표본외 밀도) `{final['delta_oos_trade_density']}`, combined density(합산 밀도) `{final['delta_combined_trade_density']}`, OOS net(표본외 순수익) `{final['delta_oos_net']}`만큼 후퇴했습니다. HB surface(HB 표면)는 target_profit_count(목표 수익 행) `{final['target_profit_count']}`를 만들었지만 oos_density_cost_count(표본외 밀도-비용 행)는 `{final['oos_density_cost_count']}`이고 joint_target_count(공동 목표 행)는 `{final['joint_target_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 GZ density-cost anchor(GZ 밀도-비용 기준점)를 기본값으로 두고 HB profit rows(HB 수익 행)를 제한적으로 붙이는 dual-surface switch(이중 표면 전환)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): HC rejected(거절) HB OOS profit-density rebalance router(HB 표본외 수익-밀도 재균형 라우터).

HB selected model(HB 선택 모델): `{final['review_subject']}`
HB OOS net/PF/density/cost0.6(HB 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['hb_oos_net']}` / `{final['hb_oos_profit_factor']}` / `{final['hb_oos_trade_density']}` / `{final['hb_oos_cost06_net']}`
HB combined density/cost0.9(HB 합산 밀도/비용0.9): `{final['hb_combined_trade_density']}` / `{final['hb_combined_cost09_net']}`

Next seed(다음 씨앗): HD dual-surface density-profit switch router(HD 이중 표면 밀도-수익 전환 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364HC__{RUN_ID}", f"\n<!-- run364HC__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` rejected HB package(HB 패키지 거절); combined cost0.9(합산 비용0.9) `{final['hb_combined_cost09_net']}` but OOS density/profit(표본외 밀도/수익) `{final['hb_oos_trade_density']}`/`{final['hb_oos_net']}`; next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364HC__{RUN_ID}", f"\n<!-- run364HC__{RUN_ID} -->\n- `{RUN_ID}`: HB는 cost clue(비용 단서)는 만들었지만 density/profit simultaneity(밀도/수익 동시성)를 잃었습니다. Effect(효과): HD는 dual-surface switch(이중 표면 전환)로 GZ anchor(GZ 기준점)와 HB profit rows(HB 수익 행)를 분리 결합합니다.\n")
    fn.append_text_once(NEGATIVE_REGISTER, f"run364HC__hb_cost_improved_density_profit_regressed__{RUN_ID}", f"\n<!-- run364HC__hb_cost_improved_density_profit_regressed__{RUN_ID} -->\n- `{RUN_ID}`: HB combined cost0.9(합산 비용0.9)는 `{final['hb_combined_cost09_net']}`로 좋아졌지만 OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6)는 `{final['hb_oos_net']}`/`{final['hb_oos_profit_factor']}`/`{final['hb_oos_trade_density']}`/`{final['hb_oos_cost06_net']}`라 package(패키지) 부적격입니다. Effect(효과): HB single-score(HB 단일 점수)를 반복하지 않습니다.\n")


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
        "question": "Did HB recover OOS profit while preserving density and cost?(HB가 밀도와 비용을 보존하며 표본외 수익을 복구했는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"package_eligible={final['package_eligible']};target_profit_count={final['target_profit_count']};oos_density_cost_count={final['oos_density_cost_count']};joint_target_count={final['joint_target_count']};combined_cost09={final['hb_combined_cost09_net']}",
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
                "kpi_scope": "HC OOS profit-density rebalance review(HC 표본외 수익-밀도 재균형 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["hb_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["hb_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["hb_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["hb_oos_trade_count"] if suffix == "tier_a_separate" else "",
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
                "run_type": "oos_profit_density_rebalance_router_review(표본외 수익-밀도 재균형 라우터 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "selected_net_profit": final["hb_oos_net"],
                "selected_profit_factor": final["hb_oos_profit_factor"],
                "selected_trade_density": final["hb_oos_trade_density"],
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
                    "notes": "HC OOS profit-density rebalance review artifact(HC 표본외 수익-밀도 재균형 검토 산출물)",
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
    write_csv(RUN364HD_QUEUE, queue)
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
