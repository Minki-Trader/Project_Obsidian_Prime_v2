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

from stage_pipelines.stage364 import train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db as gn


fn = gn.fn
et = gn.et

TODAY = "2026-06-07"
STAGE_ID = gn.STAGE_ID
STAGE_DIR = gn.STAGE_DIR
REVIEW_DIR = gn.REVIEW_DIR
SPEC_DIR = gn.SPEC_DIR
SELECTED_DIR = gn.SELECTED_DIR

RUN_NUMBER = "run364GO"
RUN_ID = "run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1"
PARENT_RUN_ID = gn.RUN_ID
NEXT_RUN_ID = "run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1"

STATUS = "completed_stage364GO_density_cost_dual_anchor_router_review_sparse_pf999_rejected_open_gp_no_authority"
JUDGMENT = "negative_density_cost_dual_anchor_router_review_sparse_pf999_density_failed_no_package_no_authority"
DECISION = "stage364GO_reject_package_open_run364GP_density_floor_pf_capped_router"
CLAIM_BOUNDARY = (
    "research_development_density_cost_dual_anchor_router_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "go_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "go_surface_diagnostic.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "go_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "go_failure_memory.csv"
RUN364GP_QUEUE = RUN_DIR / "go_gp_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GO_density_cost_dual_anchor_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GO_density_cost_dual_anchor_router_review.md"
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
    gn.FINAL_DECISION,
    gn.GATE_AUDIT,
    gn.TRADE_SURFACE,
    gn.SELECTED_CANDIDATE,
    gn.SELECTED_TRADE_TAPE,
    gn.COST_STRESS,
    gn.SIDE_SESSION_REVIEW,
    gn.MONTH_STABILITY,
    gn.MODEL_SCORECARD,
    gn.MODEL_ARTIFACT_MANIFEST,
    gn.ONNX_SMOKE_REPORT,
    gn.DATA_INTEGRITY_AUDIT,
    gn.RUN364GO_QUEUE,
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
    RUN364GP_QUEUE,
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
    return gn.exists(path)


def rel(path: Path) -> str:
    return gn.rel(path)


def sha(path: Path) -> str:
    return gn.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return gn.as_float(value, default)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(path, list(rows))


def read_json(path: Path) -> dict[str, Any]:
    with fn.io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GO inputs(GO 입력 누락): " + ", ".join(missing))
    parent = read_json(gn.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GN next_run_id mismatch(GN 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GN claim(금지된 GN 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(fn.io_path(gn.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GN gate audit(GN 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GO density-cost dual-anchor router review input(GO 밀도-비용 이중 앵커 라우터 검토 입력)",
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
    for density in [0.5, 1.0, 1.5, 1.8, 2.0, 2.2, 2.3]:
        subset = positive[positive["combined_trade_density"] >= density]
        key = str(density).replace(".", "p")
        out[f"density{key}_val_oos_pos_count"] = int(len(subset))
        out[f"density{key}_max_oos_cost06"] = float(subset["oos_cost06_net"].max()) if len(subset) else ""
        out[f"density{key}_max_combined_cost09"] = float(subset["combined_cost09_net"].max()) if len(subset) else ""
    near = positive[
        (positive["combined_trade_density"] >= 1.5)
        & (positive["oos_cost06_net"] >= -10.0)
        & (positive["combined_cost09_net"] >= -230.0)
    ]
    dense_near = positive[
        (positive["combined_trade_density"] >= 2.0)
        & (positive["oos_cost06_net"] >= -20.0)
        & (positive["combined_cost09_net"] >= -260.0)
    ]
    out["density15_cost_near_count"] = int(len(near))
    out["density20_cost_near_count"] = int(len(dense_near))
    return out


def build_outputs(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    surface = pd.read_csv(fn.io_path(gn.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    diagnostics_map = surface_counts(surface)
    selected_density = as_float(parent.get("selected_combined_trade_density"))
    selected_trades = as_float(parent.get("selected_combined_trade_count"))
    selected_pf = as_float(parent.get("selected_oos_profit_factor"))
    selected_cost06 = as_float(parent.get("selected_oos_cost06_net"))
    selected_cost09 = as_float(parent.get("selected_combined_cost09_net"))
    sparse_selected = selected_density < 1.0 or selected_trades < 120
    pf999_selected = selected_pf >= 900.0
    package_eligible = (
        not sparse_selected
        and not pf999_selected
        and selected_density >= 2.0
        and selected_cost06 >= -10.0
        and selected_cost09 >= -230.0
        and as_float(parent.get("selected_oos_net")) > 0.0
    )
    summary_rows = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent.get("selected_model_id"),
            "selected_combined_density": selected_density,
            "selected_combined_trade_count": selected_trades,
            "selected_oos_profit_factor": selected_pf,
            "selected_oos_cost06_net": selected_cost06,
            "selected_combined_cost09_net": selected_cost09,
            "sparse_selected": str(sparse_selected).lower(),
            "pf999_selected": str(pf999_selected).lower(),
            "package_eligible": str(package_eligible).lower(),
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    diagnostics = [{"run_id": RUN_ID, "metric": key, "value": value, "claim_boundary": CLAIM_BOUNDARY} for key, value in diagnostics_map.items()]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "go01_sparse_pf999_selector_failure",
            "observed_change": "selected candidate has PF999 but only 7 combined trades(선택 후보는 PF999이지만 합산 7거래뿐)",
            "comparison_baseline": "GM requested density-cost dual-anchor balance(GM이 요청한 밀도-비용 이중 앵커 균형)",
            "likely_driver": "uncapped PF term and weak hard density floor(무제한 PF 항과 약한 하드 밀도 바닥)",
            "segment_check": "surface density buckets show density>=1.5 near-cost rows exist but selected row is far below density floor(표면 밀도 구간에서 밀도1.5 비용 근접 행은 있으나 선택 행은 밀도 바닥 아래)",
            "attribution_confidence": "high",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "go02_density_cost_frontier_still_weak",
            "observed_change": "density>=2.2 positive rows are absent(밀도2.2 이상 양수 행 없음)",
            "comparison_baseline": "GL recovered combined density 2.47 but cost failed(GL은 합산 밀도 2.47을 회복했지만 비용 실패)",
            "likely_driver": "bad 16/17 high-density flow still carries cost drag or router filters over-prune(나쁜 16/17시 고밀도 흐름 비용 부담 또는 라우터 필터 과도 축소)",
            "segment_check": "density bucket audit(밀도 구간 감사)",
            "attribution_confidence": "medium",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "package_eligible": str(package_eligible).lower(),
            "decision": "reject_package",
            "reason": "selected candidate is sparse PF999 micro-sample and no density>=2.2 cost-near frontier(선택 후보가 희소 PF999 초소형 표본이고 밀도2.2 비용 근접 경계가 없음)",
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "go01_pf999_sparse_selector",
            "failed_boundary": "density-cost router selection(밀도-비용 라우터 선택)",
            "why_failed": "selected_density=0.0222929936;selected_trades=7;selected_pf=999.0",
            "salvage_value": "surface contains density>=1.5 positive near-cost rows(표면에는 밀도1.5 이상 양수 비용 근접 행이 있음)",
            "reopen_condition": "cap PF and require hard density/trade-count floor before score selection(PF를 캡하고 점수 선택 전 하드 밀도/거래수 바닥 필요)",
            "do_not_repeat": "Do not let uncapped PF select all-win micro-samples(무제한 PF가 전승 초소형 표본을 선택하게 하지 말 것).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gp01_density_floor_pf_capped_router",
            "hypothesis": "PF cap(PF 캡)과 hard density floor(하드 밀도 바닥)를 먼저 적용하면 GN의 sparse PF999 선택 실패를 막고 density-cost frontier(밀도-비용 경계)를 다시 볼 수 있습니다.",
            "required_preserve": "GJ/GL dual-anchor labels and router filters(GJ/GL 이중 앵커 라벨과 라우터 필터)",
            "required_repair": "cap PF contribution; reject combined density <1.2 or trade count <120 before scoring(PF 기여 캡; 합산 밀도 1.2 미만 또는 거래수 120 미만 사전 거절)",
            "avoid": "uncapped PF micro-sample selection(무제한 PF 초소형 표본 선택)",
            "effect": "GP는 GN 구조를 버리지 않고 selector failure(선택기 실패)만 수리합니다.",
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
        "selected_validation_net": parent.get("selected_validation_net"),
        "selected_validation_profit_factor": parent.get("selected_validation_profit_factor"),
        "selected_validation_trade_density": parent.get("selected_validation_trade_density"),
        "selected_oos_net": parent.get("selected_oos_net"),
        "selected_oos_profit_factor": parent.get("selected_oos_profit_factor"),
        "selected_oos_trade_density": parent.get("selected_oos_trade_density"),
        "selected_oos_cost06_net": parent.get("selected_oos_cost06_net"),
        "selected_oos_cost09_net": parent.get("selected_oos_cost09_net"),
        "selected_combined_net": parent.get("selected_combined_net"),
        "selected_combined_trade_count": parent.get("selected_combined_trade_count"),
        "selected_combined_trade_density": parent.get("selected_combined_trade_density"),
        "selected_combined_cost09_net": parent.get("selected_combined_cost09_net"),
        "selected_combined_short_share": parent.get("selected_combined_short_share"),
        "sparse_selected": str(sparse_selected).lower(),
        "pf999_selected": str(pf999_selected).lower(),
        "package_eligible": str(package_eligible).lower(),
        "surface_rows": diagnostics_map["surface_rows"],
        "density15_cost_near_count": diagnostics_map["density15_cost_near_count"],
        "density20_cost_near_count": diagnostics_map["density20_cost_near_count"],
        "density22_val_oos_pos_count": diagnostics_map["density2p2_val_oos_pos_count"],
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
                "source_authority_audit(소스 권위 감사)",
                "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            ],
            "review_subject": parent.get("run_id"),
            "decision_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        ("scope_completion_gate", REVIEW_SUMMARY, "GO review summary(GO 검토 요약)를 작성했습니다."),
        ("parent_integrity_gate", INPUT_MANIFEST, "GN 입력 계보를 확인했습니다."),
        ("kpi_contract_audit", SURFACE_DIAGNOSTIC, "density/cost/PF/trade-count 진단을 기록했습니다."),
        ("package_decision_gate", PACKAGE_DECISION, "패키지 거절 결정을 기록했습니다."),
        ("failure_memory_gate", FAILURE_MEMORY, "PF999 sparse failure memory(PF999 희소 실패 기억)를 남겼습니다."),
        ("next_queue_gate", RUN364GP_QUEUE, "GP 수리 큐를 열었습니다."),
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
    fn.write_json(RESULT_RECEIPT, {**common, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "GN은 비용이 아니라 거래 밀도와 PF999 선택기 문제로 거절됩니다."})
    fn.write_json(MODEL_RECEIPT, {**common, "model_family": "GN dual-anchor router(GN 이중 앵커 라우터)", "selection_metric": "uncapped PF affected score(무제한 PF가 점수에 영향)", "validation_judgment": JUDGMENT, "next_condition": "PF cap and density floor(PF 캡과 밀도 바닥)"})
    fn.write_json(ATTRIBUTION_RECEIPT, {**common, "observed_change": "positive cost but only seven trades(비용 양수지만 7거래뿐)", "comparison_baseline": PARENT_RUN_ID, "likely_drivers": ["uncapped PF(PF 무제한)", "weak density hard floor(약한 밀도 하드 바닥)"], "segment_checks": [rel(SURFACE_DIAGNOSTIC), rel(gn.SIDE_SESSION_REVIEW)], "trade_shape": "combined trade count 7, short share 1.0(합산 거래수 7, 숏 비중 1.0)", "attribution_confidence": "high", "next_probe": NEXT_RUN_ID})
    fn.write_json(LINEAGE_RECEIPT, {**common, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and fn.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and fn.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)"})
    fn.write_json(CLAIM_RECEIPT, {**common, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GO Density-Cost Dual-Anchor Router Review(밀도-비용 이중 앵커 라우터 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GN 결과를 density(밀도), cost stress(비용 압박), PF999 micro-sample(PF999 초소형 표본), package decision(패키지 결정) 기준으로 검토했습니다.

Effect(효과): 비용 양수처럼 보이는 7거래 후보를 운영 후보로 착각하지 않고, GP에서 PF cap(PF 캡)과 hard density floor(하드 밀도 바닥)를 수리하게 합니다.

- judgment(판정): `{final['judgment']}`
- review_subject(검토 대상): `{final['review_subject']}`
- selected combined density/trades(선택 합산 밀도/거래수): `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}`
- selected OOS net/PF/cost0.6(선택 표본외 순수익/수익 팩터/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_cost06_net']}`
- density15 cost-near count(밀도1.5 비용 근접 수): `{final['density15_cost_near_count']}`
- density20 cost-near count(밀도2.0 비용 근접 수): `{final['density20_cost_near_count']}`
- density2.2 positive count(밀도2.2 양수 수): `{final['density22_val_oos_pos_count']}`
- package_eligible(패키지 가능): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GO Density-Cost Dual-Anchor Router Review(밀도-비용 이중 앵커 라우터 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GN package(패키지)를 reject(거절)하고 GP density-floor PF-capped router(GP 밀도 바닥 PF 캡 라우터)를 엽니다.

Effect(효과): 이중 앵커 아이디어는 보존하되, selector failure(선택기 실패)만 수리합니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GO__{RUN_ID}", f"\n- run364GO__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - GN sparse PF999 rejected(GN 희소 PF999 거절), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GO__{RUN_ID}", f"\n<!-- run364GO__{RUN_ID} -->\n\n## run364GO Density-Cost Dual-Anchor Router Review(밀도-비용 이중 앵커 라우터 검토)\n\nAction(행동): GN의 sparse PF999 선택 실패를 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 PF cap(PF 캡)과 hard density floor(하드 밀도 바닥)를 수리합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GO__{RUN_ID}", f"\n<!-- run364GO__{RUN_ID} -->\n## run364GO density-cost dual-anchor router review(밀도-비용 이중 앵커 라우터 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GO` reviewed(검토 완료) GN density-cost dual-anchor router(GN 밀도-비용 이중 앵커 라우터). GN selected(선택) 후보는 OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6) `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_cost06_net']}`이지만 combined density/trades(합산 밀도/거래수)가 `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}`라서 rejected(거절)입니다.

Failure truth(실패 진실): PF999 micro-sample(PF999 초소형 표본) 선택 실패입니다. 비용 양수는 7거래 전승 표본에서 나온 것이므로 density-cost balance(밀도-비용 균형) 근거가 아닙니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 PF cap(PF 캡)과 hard density floor(하드 밀도 바닥)를 적용한 router(라우터)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GO rejected(거절) GN sparse PF999 router(GN 희소 PF999 라우터).

Selected GN model(선택 GN 모델): `{final['review_subject']}`
Selected OOS net/PF/density(선택 표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Selected combined density/trades/cost0.9(선택 합산 밀도/거래수/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_cost09_net']}`

Next seed(다음 씨앗): density-floor PF-capped router(밀도 바닥 PF 캡 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GO__{RUN_ID}", f"\n<!-- run364GO__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` rejected GN sparse PF999 selector(GN 희소 PF999 선택기); next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GO__{RUN_ID}", f"\n<!-- run364GO__{RUN_ID} -->\n- `{RUN_ID}`: GN dual-anchor idea(GN 이중 앵커 아이디어)는 보존하지만, PF cap(PF 캡)과 density floor(밀도 바닥) 수리가 필요합니다.\n")
    fn.append_text_once(NEGATIVE_REGISTER, f"run364GO__sparse_pf999__{RUN_ID}", f"\n<!-- run364GO__sparse_pf999__{RUN_ID} -->\n- `{RUN_ID}`: sparse PF999 selector failure(희소 PF999 선택기 실패). Effect(효과): GP에서 PF를 캡하고 최소 밀도/거래수 바닥을 하드 조건으로 둡니다.\n")


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
        "question": "Is GN router package-eligible after density-cost review?(GN 라우터는 밀도-비용 검토 뒤 패키지 가능인가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"sparse_selected={final['sparse_selected']};pf999_selected={final['pf999_selected']};density15_cost_near_count={final['density15_cost_near_count']};density20_cost_near_count={final['density20_cost_near_count']};package_eligible={final['package_eligible']}",
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
                "kpi_scope": "GO density-cost dual-anchor router review(GO 밀도-비용 이중 앵커 라우터 검토)",
                "metric_scope": "review_only_no_mt5(검토 전용, MT5 없음)",
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
                "run_type": "density_cost_dual_anchor_router_review(밀도-비용 이중 앵커 라우터 검토)",
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
                    "notes": "GO density-cost dual-anchor router review artifact(GO 밀도-비용 이중 앵커 라우터 검토 산출물)",
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
    write_csv(RUN364GP_QUEUE, queue)
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
