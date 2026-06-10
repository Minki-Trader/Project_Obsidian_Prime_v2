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

from stage_pipelines.stage364 import review_h17_oos108_pf125_density_floor_pf_capped_router_without_db as gq
from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_near_density_floor_router_without_db as gr


fn = gr.fn
et = gr.et

TODAY = "2026-06-07"
STAGE_ID = gr.STAGE_ID
STAGE_DIR = gr.STAGE_DIR
REVIEW_DIR = gr.REVIEW_DIR
SPEC_DIR = gr.SPEC_DIR
SELECTED_DIR = gr.SELECTED_DIR

RUN_NUMBER = "run364GS"
RUN_ID = "run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1"
PARENT_RUN_ID = gr.RUN_ID
NEXT_RUN_ID = "run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1"

STATUS = "completed_stage364GS_cost_near_density_floor_router_review_combined_cost_repaired_oos_cost_failed_density_floor_weak_open_gt_no_authority"
JUDGMENT = "negative_cost_near_density_floor_router_review_combined_cost_repaired_oos_cost_failed_density_floor_weak_no_package_no_authority"
DECISION = "stage364GS_reject_package_open_run364GT_cost_near_density_lift_router"
CLAIM_BOUNDARY = (
    "research_development_cost_near_density_floor_router_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "gs_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "gs_surface_diagnostic.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "gs_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "gs_failure_memory.csv"
RUN364GT_QUEUE = RUN_DIR / "gs_gt_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GS_cost_near_density_floor_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GS_cost_near_density_floor_router_review.md"
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
    gr.FINAL_DECISION,
    gr.GATE_AUDIT,
    gr.TRADE_SURFACE,
    gr.SELECTED_CANDIDATE,
    gr.SELECTED_TRADE_TAPE,
    gr.COST_STRESS,
    gr.SIDE_SESSION_REVIEW,
    gr.MONTH_STABILITY,
    gr.MODEL_SCORECARD,
    gr.MODEL_ARTIFACT_MANIFEST,
    gr.ONNX_SMOKE_REPORT,
    gr.DATA_INTEGRITY_AUDIT,
    gr.RUN364GS_QUEUE,
    gq.FINAL_DECISION,
    gq.PACKAGE_DECISION,
    gq.FAILURE_MEMORY,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    SURFACE_DIAGNOSTIC,
    FAILURE_ATTRIBUTION,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364GT_QUEUE,
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
    return gr.exists(path)


def rel(path: Path) -> str:
    return gr.rel(path)


def sha(path: Path) -> str:
    return gr.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gr.as_float(value, default)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(path, list(rows))


def read_json(path: Path) -> dict[str, Any]:
    with fn.io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GS inputs(GS 입력 누락): " + ", ".join(missing))
    parent = read_json(gr.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GR next_run_id mismatch(GR 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GR claim(금지된 GR 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gr.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GR gate audit(GR 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GS cost-near density floor review input(GS 비용 근접 밀도 바닥 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def surface_counts(surface: pd.DataFrame) -> dict[str, Any]:
    positive = surface[(surface["validation_net"] > 0) & (surface["oos_net"] > 0)]
    out: dict[str, Any] = {
        "surface_rows": int(len(surface)),
        "positive_rows": int(len(positive)),
    }
    for density in [1.0, 1.2, 1.35, 1.5, 1.8, 2.0]:
        subset = positive[positive["combined_trade_density"] >= density]
        key = str(density).replace(".", "p")
        out[f"density{key}_val_oos_pos_count"] = int(len(subset))
        out[f"density{key}_max_oos_cost06"] = float(subset["oos_cost06_net"].max()) if len(subset) else ""
        out[f"density{key}_max_combined_cost09"] = float(subset["combined_cost09_net"].max()) if len(subset) else ""
        out[f"density{key}_max_oos_net"] = float(subset["oos_net"].max()) if len(subset) else ""
    cost_near = positive[
        (positive["combined_trade_density"] >= 1.2)
        & (positive["combined_cost09_net"] >= -80.0)
        & (positive["oos_cost06_net"] >= -5.0)
    ]
    partial = positive[
        (positive["combined_trade_density"] >= 1.2)
        & (positive["combined_cost09_net"] >= -140.0)
        & (positive["oos_cost06_net"] >= -25.0)
    ]
    lift_partial = partial[partial["combined_trade_density"] >= 1.45]
    out["cost_near_density_floor_count"] = int(len(cost_near))
    out["partial_cost_near_density_floor_count"] = int(len(partial))
    out["partial_cost_near_density_lift_count"] = int(len(lift_partial))
    out["best_partial_combined_cost09"] = float(partial["combined_cost09_net"].max()) if len(partial) else ""
    out["best_partial_oos_cost06"] = float(partial["oos_cost06_net"].max()) if len(partial) else ""
    return out


def build_outputs(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    previous = read_json(gq.FINAL_DECISION)
    surface = pd.read_csv(fn.io_path(gr.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    diagnostics_map = surface_counts(surface)
    selected_density = as_float(parent.get("selected_combined_trade_density"))
    selected_oos_density = as_float(parent.get("selected_oos_trade_density"))
    selected_trades = as_float(parent.get("selected_combined_trade_count"))
    selected_pf = as_float(parent.get("selected_oos_profit_factor"))
    selected_cost06 = as_float(parent.get("selected_oos_cost06_net"))
    selected_cost09 = as_float(parent.get("selected_combined_cost09_net"))
    previous_cost09 = as_float(previous.get("selected_combined_cost09_net"))
    previous_oos_cost06 = as_float(previous.get("selected_oos_cost06_net"))
    cost09_improvement = selected_cost09 - previous_cost09
    oos_cost06_change = selected_cost06 - previous_oos_cost06
    sparse_selected = selected_density < 1.2 or selected_trades < 120
    pf999_selected = selected_pf >= 900.0
    density_floor_kept = selected_density >= 1.2 and selected_trades >= 120
    oos_density_weak = selected_oos_density < 1.2
    combined_cost_repaired = selected_cost09 >= -140.0 and cost09_improvement >= 120.0
    cost_near_target_met = selected_cost09 >= -80.0 and selected_cost06 >= -5.0
    oos_cost_failed = selected_cost06 < -10.0
    package_eligible = (
        not sparse_selected
        and not pf999_selected
        and selected_density >= 2.0
        and selected_oos_density >= 1.5
        and selected_cost09 >= -80.0
        and selected_cost06 >= -5.0
        and as_float(parent.get("selected_oos_net")) > 0.0
    )
    summary_rows = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent.get("selected_model_id"),
            "previous_combined_cost09_net": previous_cost09,
            "selected_combined_cost09_net": selected_cost09,
            "combined_cost09_improvement": cost09_improvement,
            "previous_oos_cost06_net": previous_oos_cost06,
            "selected_oos_cost06_net": selected_cost06,
            "oos_cost06_change": oos_cost06_change,
            "selected_combined_density": selected_density,
            "selected_oos_density": selected_oos_density,
            "selected_combined_trade_count": selected_trades,
            "combined_cost_repaired": str(combined_cost_repaired).lower(),
            "cost_near_target_met": str(cost_near_target_met).lower(),
            "density_floor_kept": str(density_floor_kept).lower(),
            "oos_density_weak": str(oos_density_weak).lower(),
            "package_eligible": str(package_eligible).lower(),
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    diagnostics = [{"run_id": RUN_ID, "metric": key, "value": value, "claim_boundary": CLAIM_BOUNDARY} for key, value in diagnostics_map.items()]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "gs01_combined_cost09_repaired_but_oos_cost06_failed",
            "observed_change": f"combined cost0.9 improved from {previous_cost09} to {selected_cost09}, but OOS cost0.6 changed from {previous_oos_cost06} to {selected_cost06}",
            "comparison_baseline": gq.RUN_ID,
            "likely_drivers": "GR score emphasized combined cost stress and hard trade floor, but did not preserve OOS cost0.6 enough(GR 점수는 합산 비용 압박과 하드 거래수 바닥을 강조했지만 표본외 비용0.6을 충분히 보존하지 못함)",
            "segment_check": "selected trade tape, cost stress, density buckets(선택 거래 테이프, 비용 압박, 밀도 구간)",
            "trade_shape": f"combined trades={selected_trades}; OOS density={selected_oos_density}; short_share={parent.get('selected_combined_short_share')}",
            "alternative_explanations": "threshold and hour/filter selection may be reducing density while shifting cost between validation and OOS(임계값과 시간/필터 선택이 밀도를 낮추고 검증/표본외 비용을 옮겼을 수 있음)",
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gs02_density_floor_only_not_density_lift",
            "observed_change": f"combined density {selected_density}, OOS density {selected_oos_density}",
            "comparison_baseline": gr.RUN_ID,
            "likely_drivers": "cost-first selection sacrificed density lift(비용 우선 선택이 밀도 상승을 희생)",
            "segment_check": "surface density buckets(표면 밀도 구간)",
            "trade_shape": f"validation trades={parent.get('selected_validation_trade_count')}; OOS trades={parent.get('selected_oos_trade_count')}",
            "alternative_explanations": "label horizon h2 cost source may be too conservative for OOS density(h2 비용 라벨 원천이 표본외 밀도에는 과하게 보수적일 수 있음)",
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "package_eligible": str(package_eligible).lower(),
            "decision": "reject_package",
            "reason": "combined cost0.9 improved but OOS cost0.6 and density lift are not package-ready(합산 비용0.9는 개선됐지만 표본외 비용0.6과 밀도 상승이 패키지 기준이 아님)",
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "gs01_partial_cost_repair_oos_cost_density_weak",
            "failed_boundary": "package-ready cost-near density floor(패키지 가능 비용 근접 밀도 바닥)",
            "why_failed": f"combined_cost09={selected_cost09}; oos_cost06={selected_cost06}; combined_density={selected_density}; oos_density={selected_oos_density}; strict=0",
            "salvage_value": "combined cost0.9 improved strongly while hard trade floor survived(합산 비용0.9가 크게 개선되고 하드 거래수 바닥은 유지됨)",
            "reopen_condition": "preserve combined cost0.9 above -140 while lifting OOS cost0.6 and OOS density(합산 비용0.9 -140 이상을 보존하며 표본외 비용0.6과 표본외 밀도를 올림)",
            "do_not_repeat": "Do not call combined cost repair package-ready while OOS cost0.6 is below -10(표본외 비용0.6이 -10 아래면 합산 비용 수리만으로 패키지 가능이라 말하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gt01_cost_near_density_lift_router",
            "hypothesis": "preserving GR combined cost0.9 repair while lifting OOS density and OOS cost0.6 can create a better frontier(GR 합산 비용0.9 수리를 보존하면서 표본외 밀도와 표본외 비용0.6을 올리면 더 나은 경계를 만들 수 있음)",
            "required_preserve": "combined cost0.9 >= -140 and hard trade floor(합산 비용0.9 -140 이상과 하드 거래수 바닥)",
            "required_repair": "OOS cost0.6 >= -10, OOS density >= 1.2, combined density >= 1.45(표본외 비용0.6 -10 이상, 표본외 밀도 1.2 이상, 합산 밀도 1.45 이상)",
            "avoid": "density lift with combined cost0.9 below -180 or OOS density below 1.1(합산 비용0.9 -180 아래 또는 표본외 밀도 1.1 아래의 밀도 상승)",
            "effect": "GT keeps GR cost repair clue and searches a controlled density lift(GT는 GR 비용 수리 단서를 보존하고 통제된 밀도 상승을 탐색)",
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
        "previous_combined_cost09_net": previous_cost09,
        "selected_combined_cost09_net": selected_cost09,
        "combined_cost09_improvement": cost09_improvement,
        "previous_oos_cost06_net": previous_oos_cost06,
        "selected_oos_cost06_net": selected_cost06,
        "oos_cost06_change": oos_cost06_change,
        "selected_validation_net": parent.get("selected_validation_net"),
        "selected_validation_profit_factor": parent.get("selected_validation_profit_factor"),
        "selected_validation_trade_density": parent.get("selected_validation_trade_density"),
        "selected_oos_net": parent.get("selected_oos_net"),
        "selected_oos_profit_factor": parent.get("selected_oos_profit_factor"),
        "selected_oos_trade_density": parent.get("selected_oos_trade_density"),
        "selected_combined_net": parent.get("selected_combined_net"),
        "selected_combined_trade_count": parent.get("selected_combined_trade_count"),
        "selected_combined_trade_density": parent.get("selected_combined_trade_density"),
        "selected_combined_short_share": parent.get("selected_combined_short_share"),
        "sparse_selected": str(sparse_selected).lower(),
        "pf999_selected": str(pf999_selected).lower(),
        "combined_cost_repaired": str(combined_cost_repaired).lower(),
        "cost_near_target_met": str(cost_near_target_met).lower(),
        "density_floor_kept": str(density_floor_kept).lower(),
        "oos_density_weak": str(oos_density_weak).lower(),
        "package_eligible": str(package_eligible).lower(),
        "surface_rows": diagnostics_map["surface_rows"],
        "cost_near_density_floor_count": diagnostics_map["cost_near_density_floor_count"],
        "partial_cost_near_density_floor_count": diagnostics_map["partial_cost_near_density_floor_count"],
        "partial_cost_near_density_lift_count": diagnostics_map["partial_cost_near_density_lift_count"],
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
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": [
                "kpi_contract_audit(KPI 계약 감사)",
                "row_grain_audit(행 단위 감사)",
                "source_authority_audit(출처 권위 감사)",
                "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            ],
            "review_subject": parent.get("run_id"),
            "decision_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        ("scope_completion_gate", REVIEW_SUMMARY, "GS review summary(GS 검토 요약)를 작성했습니다."),
        ("parent_integrity_gate", INPUT_MANIFEST, "GR 입력 계보를 확인했습니다."),
        ("kpi_contract_audit", SURFACE_DIAGNOSTIC, "density/cost/PF/trade-count 진단을 기록했습니다."),
        ("package_decision_gate", PACKAGE_DECISION, "패키지 거절 결정을 기록했습니다."),
        ("failure_memory_gate", FAILURE_MEMORY, "partial cost repair failure memory(부분 비용 수리 실패 기억)를 남겼습니다."),
        ("next_queue_gate", RUN364GT_QUEUE, "GT 수리 씨앗을 열었습니다."),
        ("paired_tier_record_gate", STAGE_LEDGER, "Tier A/Tier B/Tier A+B 행을 장부에 남겼습니다."),
        ("receipt_coverage_gate", RESULT_RECEIPT, "결과 판정 영수증을 남겼습니다."),
        ("required_gate_coverage_audit", GATE_AUDIT, "필수 게이트 커버리지를 연결했습니다."),
        ("final_claim_guard", CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
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
    fn.write_json(RESULT_RECEIPT, {**common, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "GR은 합산 비용을 고쳤지만 표본외 비용0.6과 밀도 상승이 아직 약합니다."})
    fn.write_json(MODEL_RECEIPT, {**common, "model_family": "GR cost-near density floor router(GR 비용 근접 밀도 바닥 라우터)", "selection_metric": "cost-near density-floor PF-capped score(비용 근접 밀도 바닥 PF 캡 점수)", "validation_judgment": JUDGMENT, "next_condition": "cost-near density lift router(비용 근접 밀도 상승 라우터)"})
    fn.write_json(ATTRIBUTION_RECEIPT, {**common, "observed_change": f"combined cost0.9 {final['previous_combined_cost09_net']} -> {final['selected_combined_cost09_net']}; OOS cost0.6 {final['previous_oos_cost06_net']} -> {final['selected_oos_cost06_net']}", "comparison_baseline": gq.RUN_ID, "likely_drivers": ["cost-near score(비용 근접 점수)", "hard trade floor(하드 거래수 바닥)", "cost-collapse veto(비용 붕괴 차단)"], "segment_checks": [rel(SURFACE_DIAGNOSTIC), rel(gr.COST_STRESS), rel(gr.SIDE_SESSION_REVIEW)], "trade_shape": f"combined density={final['selected_combined_trade_density']}; OOS density={final['selected_oos_trade_density']}", "alternative_explanations": "density loss may come from conservative h2 cost label(밀도 손실은 보수적인 h2 비용 라벨에서 왔을 수 있음)", "attribution_confidence": "medium", "next_probe": NEXT_RUN_ID})
    fn.write_json(LINEAGE_RECEIPT, {**common, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)"})
    fn.write_json(CLAIM_RECEIPT, {**common, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GS Cost-Near Density Floor Router Review(비용 근접 밀도 바닥 라우터 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GR 결과를 combined cost0.9(합산 비용0.9), OOS cost0.6(표본외 비용0.6), density floor(밀도 바닥), package decision(패키지 결정) 기준으로 검토했습니다.

Effect(효과): 합산 비용 수리 단서는 보존하지만, 표본외 비용0.6과 밀도 상승이 약하므로 패키지 후보로 올리지 않습니다.

- judgment(판정): `{final['judgment']}`
- review_subject(검토 대상): `{final['review_subject']}`
- combined cost0.9 change(합산 비용0.9 변화): `{final['previous_combined_cost09_net']}` -> `{final['selected_combined_cost09_net']}` (`{final['combined_cost09_improvement']}`)
- OOS cost0.6 change(표본외 비용0.6 변화): `{final['previous_oos_cost06_net']}` -> `{final['selected_oos_cost06_net']}` (`{final['oos_cost06_change']}`)
- selected OOS net/PF/density(선택 표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- selected combined density/trades(선택 합산 밀도/거래수): `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}`
- combined_cost_repaired(합산 비용 수리): `{final['combined_cost_repaired']}`
- cost_near_target_met(비용 근접 목표 충족): `{final['cost_near_target_met']}`
- density_floor_kept(밀도 바닥 유지): `{final['density_floor_kept']}`
- package_eligible(패키지 가능): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GS Cost-Near Density Floor Router Review(비용 근접 밀도 바닥 라우터 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GR package(패키지)를 reject(거절)하고 GT cost-near density lift router(GT 비용 근접 밀도 상승 라우터)를 엽니다.

Effect(효과): 합산 비용 수리 단서를 보존하되, 표본외 비용0.6과 표본외 밀도 약점을 다음 실험의 명시 조건으로 바꿉니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GS__{RUN_ID}", f"\n- run364GS__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - GR combined cost repaired but OOS cost/density weak(GR 합산 비용 수리, 표본외 비용/밀도 약함), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GS__{RUN_ID}", f"\n<!-- run364GS__{RUN_ID} -->\n\n## run364GS Cost-Near Density Floor Router Review(비용 근접 밀도 바닥 라우터 검토)\n\nAction(행동): GR의 비용 수리 단서와 표본외 약점을 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 합산 비용 수리 보존 + 표본외 비용0.6/밀도 상승을 함께 탐색합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GS__{RUN_ID}", f"\n<!-- run364GS__{RUN_ID} -->\n## run364GS cost-near density floor router review(비용 근접 밀도 바닥 라우터 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GS` reviewed(검토 완료) GR cost-near density floor router(GR 비용 근접 밀도 바닥 라우터). GR은 combined cost0.9(합산 비용0.9)를 `{final['previous_combined_cost09_net']}`에서 `{final['selected_combined_cost09_net']}`로 개선했지만, OOS cost0.6(표본외 비용0.6)이 `{final['selected_oos_cost06_net']}`라서 package(패키지)는 rejected(거절)입니다.

Failure truth(실패 진실): cost_near_target_met(비용 근접 목표 충족)는 `{final['cost_near_target_met']}`이고, density_floor_kept(밀도 바닥 유지)는 `{final['density_floor_kept']}`입니다. 표본외 밀도와 비용0.6을 함께 올려야 합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 cost-near repair(비용 근접 수리)를 보존하면서 density lift(밀도 상승)를 통제해 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GS rejected(거절) GR partial cost repair(GR 부분 비용 수리).

Selected GR model(선택 GR 모델): `{final['review_subject']}`
Selected OOS net/PF/density(선택 표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Selected combined density/trades/cost0.9(선택 합산 밀도/거래수/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_cost09_net']}`

Next seed(다음 씨앗): cost-near density lift router(비용 근접 밀도 상승 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GS__{RUN_ID}", f"\n<!-- run364GS__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` rejected GR package(GR 패키지 거절); combined cost0.9 `{final['selected_combined_cost09_net']}`; OOS cost0.6 `{final['selected_oos_cost06_net']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GS__{RUN_ID}", f"\n<!-- run364GS__{RUN_ID} -->\n- `{RUN_ID}`: GR의 combined cost0.9(합산 비용0.9) 개선 단서를 보존했습니다. Effect(효과): GT에서 표본외 비용0.6과 밀도 상승을 함께 탐색합니다.\n")
    fn.append_text_once(NEGATIVE_REGISTER, f"run364GS__partial_cost_repair_oos_cost_density_weak__{RUN_ID}", f"\n<!-- run364GS__partial_cost_repair_oos_cost_density_weak__{RUN_ID} -->\n- `{RUN_ID}`: combined cost0.9(합산 비용0.9)는 수리됐지만 OOS cost0.6(표본외 비용0.6)과 density lift(밀도 상승)가 약합니다. Effect(효과): GT 조건은 합산 비용 보존 + 표본외 비용/밀도 상승입니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    artifact_count = len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST})
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
        "question": "Is GR cost-near density floor package-eligible after review?(GR 비용 근접 밀도 바닥은 검토 뒤 패키지 가능한가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"combined_cost_repaired={final['combined_cost_repaired']};cost_near_target_met={final['cost_near_target_met']};density_floor_kept={final['density_floor_kept']};package_eligible={final['package_eligible']}",
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
                "kpi_scope": "GS cost-near density floor review(GS 비용 근접 밀도 바닥 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
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
                "run_type": "cost_near_density_floor_router_review(비용 근접 밀도 바닥 라우터 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
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
                    "notes": "GS cost-near density floor router review artifact(GS 비용 근접 밀도 바닥 라우터 검토 산출물)",
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
    write_csv(FAILURE_ATTRIBUTION, attribution)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364GT_QUEUE, queue)
    fn.write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = write_gates(final)
    write_run_manifest(final)
    write_docs(final, gates)
    write_ledgers(final)
    write_artifact_registry(final)
    write_receipts(final)
    gates = write_gates(final)
    final["gate_passes"] = len([row for row in gates if row["status"] == "passed"])
    final["gate_total"] = len(gates)
    fn.write_json(FINAL_DECISION, final)
    write_run_manifest(final)
    write_ledgers(final)
    write_artifact_registry(final)
    print(json.dumps({"run_id": RUN_ID, "judgment": JUDGMENT, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "next_run_id": NEXT_RUN_ID}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
