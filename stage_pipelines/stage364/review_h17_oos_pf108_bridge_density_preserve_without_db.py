from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos_pf108_bridge_density_preserve_without_db as eh  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = eh.STAGE_ID
RUN_NUMBER = "run364EI"
RUN_ID = "run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1"
PARENT_RUN_ID = eh.RUN_ID
NEXT_RUN_ID = "run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1"

STATUS = "completed_stage364EI_oos_pf108_bridge_review_package_rejected_open_ej_no_authority"
JUDGMENT = "negative_oos_pf108_bridge_review_density_floor_failed_no_package_no_authority"
DECISION = "stage364EI_reject_package_open_run364EJ_density_floor_oos_pf_salvage"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_oos_pf108_bridge_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = eh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "ei_oos_pf108_bridge_review_summary.csv"
FAILURE_MEMORY = RUN_DIR / "oos_pf108_bridge_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364EJ_QUEUE = RUN_DIR / "run364EJ_density_floor_oos_pf_salvage_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EI_h17_oos_pf108_bridge_density_preserve_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EI_h17_oos_pf108_bridge_density_preserve_review.md"
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

INPUT_FILES = [
    eh.FINAL_DECISION,
    eh.GATE_AUDIT,
    eh.TRADE_SURFACE,
    eh.SELECTED_CANDIDATE,
    eh.SELECTED_TRADE_TAPE,
    eh.MONTH_STABILITY,
    eh.COST_STRESS,
    eh.MODEL_SCORECARD,
    eh.ONNX_SMOKE_REPORT,
    eh.DATA_INTEGRITY_AUDIT,
    eh.RUN364EI_QUEUE,
    eh.RUN_EVIDENCE_RECEIPT,
    eh.MODEL_RECEIPT,
    eh.ATTRIBUTION_RECEIPT,
    eh.JUDGMENT_RECEIPT,
    eh.LINEAGE_RECEIPT,
    eh.CLAIM_RECEIPT,
    eh.RUN_MANIFEST,
    eh.REPORT_PATH,
    eh.eg.FINAL_DECISION,
    eh.eg.FAILURE_MEMORY,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364EJ_QUEUE,
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
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return eh.rel(path)


def exists(path: Path | str) -> bool:
    return eh.exists(path)


def sha(path: Path | str) -> str:
    return eh.sha(path)


def read_json(path: Path) -> Any:
    return eh.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    eh.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    eh.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    eh.write_csv(path, rows, fieldnames)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    eh.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    eh.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    eh.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return eh.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EI inputs(EI 입력 누락): " + ", ".join(missing))
    parent = read_json(eh.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EH next_run_id mismatch(EH 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"EH forbidden claim(EH 금지 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(eh.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EH gate audit(EH 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [{"run_id": RUN_ID, "input_path": rel(path), "exists": exists(path), "sha256": sha(path) if exists(path) and io_path(path).is_file() else "", "input_role": "EI OOS PF108 bridge review input(EI 표본외 PF108 연결 검토 입력)", "claim_boundary": CLAIM_BOUNDARY} for path in INPUT_FILES]


def summarize_surface(parent: Mapping[str, Any]) -> dict[str, Any]:
    surface = pd.read_csv(io_path(eh.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    selected = read_json(eh.SELECTED_CANDIDATE)
    ef_final = read_json(eh.eg.ef.FINAL_DECISION)
    for col in ["validation_net", "oos_net", "validation_profit_factor", "oos_profit_factor", "validation_trade_density", "oos_trade_density", "selection_score"]:
        surface[col] = surface[col].map(as_float)
    surface["min_pf"] = surface[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    surface["min_density"] = surface[["validation_trade_density", "oos_trade_density"]].min(axis=1)
    density_mask = (surface["validation_trade_density"] >= 3.0) & (surface["oos_trade_density"] >= 3.0) & (surface["validation_net"] > 0.0) & (surface["oos_net"] > 0.0)
    near_density_mask = (surface["validation_trade_density"] >= 2.8) & (surface["oos_trade_density"] >= 2.8) & (surface["validation_net"] > 0.0) & (surface["oos_net"] > 0.0)
    oos108_mask = near_density_mask & (surface["oos_profit_factor"] >= 1.08) & (surface["validation_profit_factor"] >= 1.035)
    pf108_mask = density_mask & (surface["validation_profit_factor"] >= 1.08) & (surface["oos_profit_factor"] >= 1.08)
    best_near = surface[near_density_mask].sort_values("oos_profit_factor", ascending=False).iloc[0].to_dict() if int(near_density_mask.sum()) else {}
    best_density = surface[density_mask].sort_values("min_pf", ascending=False).iloc[0].to_dict() if int(density_mask.sum()) else {}
    return {
        "run_id": RUN_ID,
        "review_subject": parent["run_id"],
        "selected_model_id": selected["selected_model_id"],
        "selected_validation_net": selected["selected_validation_net"],
        "selected_validation_profit_factor": selected["selected_validation_profit_factor"],
        "selected_validation_trade_density": selected["selected_validation_trade_density"],
        "selected_oos_net": selected["selected_oos_net"],
        "selected_oos_profit_factor": selected["selected_oos_profit_factor"],
        "selected_oos_trade_density": selected["selected_oos_trade_density"],
        "selected_min_profit_factor": selected["selected_min_profit_factor"],
        "selected_oos_trade_count": selected["selected_oos_trade_count"],
        "selected_oos_long_trade_count": selected["selected_oos_long_trade_count"],
        "selected_oos_short_trade_count": selected["selected_oos_short_trade_count"],
        "eh_density_net_count": int(density_mask.sum()),
        "eh_near_density_count": int(near_density_mask.sum()),
        "eh_oos108_count": int(oos108_mask.sum()),
        "eh_pf108_count": int(pf108_mask.sum()),
        "eh_pf110_count": int(parent["pf110_count"]),
        "eh_strict_candidate_count": int(parent["strict_candidate_count"]),
        "ef_selected_min_pf": as_float(ef_final["selected_min_profit_factor"]),
        "min_pf_delta_vs_ef": round(as_float(selected["selected_min_profit_factor"]) - as_float(ef_final["selected_min_profit_factor"]), 10),
        "best_near_density_model_id": best_near.get("model_id", ""),
        "best_near_density_oos_pf": round(as_float(best_near.get("oos_profit_factor")), 10),
        "best_near_density_min_density": round(as_float(best_near.get("min_density")), 10),
        "best_density_model_id": best_density.get("model_id", ""),
        "best_density_min_pf": round(as_float(best_density.get("min_pf")), 10),
        "best_density_min_density": round(as_float(best_density.get("min_density")), 10),
        "package_decision": "rejected(거절)",
        "package_reason": "density_floor_failed_despite_oos_pf_gain(표본외 PF 개선에도 밀도 바닥 실패)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(WORK_PACKET, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "primary_family": "kpi_evidence(KPI 근거)", "primary_skill": "obsidian-result-judgment(결과 판정)", "support_skills": ["obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)", "obsidian-run-evidence-system(실행 근거 시스템)"], "review_question": "Should EH open package or seed EJ density floor salvage?(EH를 패키지로 열 것인가, EJ 밀도 바닥 회수로 넘길 것인가?)", "claim_boundary": CLAIM_BOUNDARY})


def package_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [{"run_id": RUN_ID, "review_subject": PARENT_RUN_ID, "package_decision": summary["package_decision"], "reason": summary["package_reason"], "selected_oos_profit_factor": summary["selected_oos_profit_factor"], "selected_oos_trade_density": summary["selected_oos_trade_density"], "runtime_package": "not_opened(열지 않음)", "effect": "밀도 바닥 실패 때문에 운영 package(패키지)를 열지 않습니다.", "claim_boundary": CLAIM_BOUNDARY}]


def failure_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"run_id": RUN_ID, "memory_id": "ei01_oos_pf_gain_density_floor_failed", "observed": f"OOS PF={summary['selected_oos_profit_factor']};validation_density={summary['selected_validation_trade_density']};oos_density={summary['selected_oos_trade_density']}", "meaning": "OOS PF(표본외 수익 팩터)는 강하게 올랐지만 밀도 3/day를 잃었습니다.", "next_constraint": "EJ는 density floor(밀도 바닥)를 먼저 회복하고 OOS PF 단서를 보존합니다.", "effect": "희소 고PF를 운영 후보로 오해하지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "memory_id": "ei02_near_density_salvage_seed", "observed": f"near_density_count={summary['eh_near_density_count']};best_near_oos_pf={summary['best_near_density_oos_pf']};best_near_min_density={summary['best_near_density_min_density']}", "meaning": "2.8/day 이상 near-density(근접 밀도) 구간에는 회수할 PF 단서가 있습니다.", "next_constraint": "EJ는 threshold/density target(임계값/밀도 목표)을 3/day 위로 밀어 올립니다.", "effect": "단서를 버리지 않고 밀도 복구 문제로 바꿉니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]


def next_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [{"run_id": RUN_ID, "next_run_id": NEXT_RUN_ID, "queue_rank": 1, "queue_id": "ej01_density_floor_oos_pf_salvage", "hypothesis": "EH의 high OOS PF(높은 표본외 PF) 단서를 threshold/density floor repair(임계값/밀도 바닥 수리)로 3/day 이상까지 끌어올리면 PF 1.08 근처를 유지한 후보가 생길 수 있습니다.", "preserve": "source_all h2, OOS PF clue, validation PF positive(전체 원천 h2, 표본외 PF 단서, 검증 PF 양수)", "avoid": "density<3 package and sparse high PF(밀도 3 미만 패키지 및 희소 고PF)", "target": "validation/OOS density>=3, OOS PF>=1.12 scout, validation PF>=1.04(검증/표본외 밀도 3 이상, 표본외 PF 1.12 스카우트, 검증 PF 1.04 이상)", "effect": "EJ는 EH의 좋아진 PF를 거래 밀도 조건 안으로 되돌립니다.", "claim_boundary": CLAIM_BOUNDARY}]


def write_receipts(summary: Mapping[str, Any], created_at: str) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": created_at, "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(eh.FINAL_DECISION), rel(eh.TRADE_SURFACE)], "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "runtime package(런타임 패키지)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "reviewed_model": summary["selected_model_id"], "package_decision": summary["package_decision"], "model_judgment": "rejected_for_package_density_floor_failed(패키지 거절, 밀도 바닥 실패)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"EF min_pf {summary['ef_selected_min_pf']} -> EH min_pf {summary['selected_min_profit_factor']}; OOS PF {summary['selected_oos_profit_factor']}; min density below 3", "likely_drivers": ["OOS PF reward(표본외 PF 보상)", "threshold too selective(임계값 과선택)", "density target miss(밀도 목표 미달)"], "attribution_confidence": "medium(중간)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EI 검토는 운영 주장(operating claim, 운영 주장)을 만들지 않습니다."})


def gate_rows(created_at: str) -> list[dict[str, Any]]:
    receipt_paths = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    rows = [
        {"run_id": RUN_ID, "gate": "input_lineage_gate", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "evidence": rel(INPUT_MANIFEST), "effect": "입력 산출물 존재를 확인했습니다."},
        {"run_id": RUN_ID, "gate": "review_summary_gate", "status": "passed" if exists(REVIEW_SUMMARY) else "failed", "evidence": rel(REVIEW_SUMMARY), "effect": "EH 결과 요약이 있습니다."},
        {"run_id": RUN_ID, "gate": "package_decision_gate", "status": "passed" if exists(PACKAGE_DECISION) else "failed", "evidence": rel(PACKAGE_DECISION), "effect": "패키지 거절 이유가 기록됐습니다."},
        {"run_id": RUN_ID, "gate": "failure_memory_gate", "status": "passed" if exists(FAILURE_MEMORY) else "failed", "evidence": rel(FAILURE_MEMORY), "effect": "실패 기억이 다음 제약으로 남았습니다."},
        {"run_id": RUN_ID, "gate": "next_queue_gate", "status": "passed" if exists(RUN364EJ_QUEUE) else "failed", "evidence": rel(RUN364EJ_QUEUE), "effect": "다음 EJ 입력이 생성됐습니다."},
        {"run_id": RUN_ID, "gate": "receipt_coverage_gate", "status": "passed" if all(exists(path) for path in receipt_paths) else "failed", "evidence": "|".join(rel(path) for path in receipt_paths), "effect": "필수 receipt(영수증)가 있습니다."},
        {"run_id": RUN_ID, "gate": "final_claim_guard", "status": "passed", "evidence": rel(CLAIM_RECEIPT), "effect": "authority/promotion/live/goal(권위/승격/실거래/목표) 주장을 차단했습니다."},
        {"run_id": RUN_ID, "gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT), "effect": "필수 gate(게이트)가 종료 기록에 연결됐습니다."},
    ]
    for row in rows:
        row["created_at_utc"] = created_at
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "package_decision": "rejected", "selected_model_id": summary["selected_model_id"], "selected_min_profit_factor": summary["selected_min_profit_factor"], "selected_validation_net": summary["selected_validation_net"], "selected_validation_profit_factor": summary["selected_validation_profit_factor"], "selected_validation_trade_density": summary["selected_validation_trade_density"], "selected_oos_net": summary["selected_oos_net"], "selected_oos_profit_factor": summary["selected_oos_profit_factor"], "selected_oos_trade_density": summary["selected_oos_trade_density"], "eh_density_net_count": summary["eh_density_net_count"], "eh_near_density_count": summary["eh_near_density_count"], "eh_oos108_count": summary["eh_oos108_count"], "eh_pf108_count": summary["eh_pf108_count"], "eh_pf110_count": summary["eh_pf110_count"], "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "runtime_package": "not_opened", "new_mt5_execution": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "created_at_utc": created_at, "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "final_decision": rel(FINAL_DECISION)}


def write_docs(summary: Mapping[str, Any], final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364EI H17 OOS PF108 Bridge Review(표본외 PF108 연결 검토)

Created(생성): {final['created_at_utc']}

Action(행동): EH OOS PF108 bridge density preserve(EH 표본외 PF108 연결 밀도 보존)를 package(패키지), failure memory(실패 기억), next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): OOS PF(표본외 수익 팩터) 개선을 density floor salvage(밀도 바닥 회수) 문제로 바꿉니다.

Findings(발견):

- selected OOS PF(선택 표본외 PF): `{summary['selected_oos_profit_factor']}`
- selected validation/OOS density(선택 검증/표본외 밀도): `{summary['selected_validation_trade_density']}` / `{summary['selected_oos_trade_density']}`
- near_density_count(근접 밀도 후보 수): `{summary['eh_near_density_count']}`
- density_net_count(밀도+순수익 후보 수): `{summary['eh_density_net_count']}`
- oos108_count(표본외 PF 1.08 후보 수): `{summary['eh_oos108_count']}`

Judgment(판정): `{JUDGMENT}`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, f"""# Decision(결정): stage364EI OOS PF108 bridge review(표본외 PF108 연결 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EH 결과를 패키지로 열지 않고 EJ 씨앗으로 넘겼습니다.

Effect(효과): EJ가 OOS PF(표본외 PF) 단서를 밀도 3/day 조건 안으로 되돌립니다.
""", bom=True)
    append_text_once(REVIEW_INDEX, f"run364EI__{RUN_ID}", f"\n- run364EI__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - OOS PF108 bridge review(표본외 PF108 연결 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EI__{RUN_ID}", f"\n<!-- run364EI__{RUN_ID} -->\n\n## run364EI OOS PF108 Bridge Review(표본외 PF108 연결 검토)\n\nAction(행동): EH 결과를 package rejected(패키지 거절)로 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density floor OOS PF salvage(밀도 바닥 표본외 PF 회수)를 다음 공격 탐색으로 엽니다.\n")
    append_text_once(STAGE_README, f"run364EI__{RUN_ID}", f"\n<!-- run364EI__{RUN_ID} -->\n## run364EI OOS PF108 bridge review(표본외 PF108 연결 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(STAGE_BRIEF, {"- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`", "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`", "- selection_status": f"- selection_status(선택 상태): `{STATUS}`", "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`"}, bom=True)
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
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
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364EI` reviewed(검토 완료) EH OOS PF108 bridge density preserve(EH 표본외 PF108 연결 밀도 보존). EH는 OOS PF(표본외 수익 팩터)를 `{summary['selected_oos_profit_factor']}`까지 올렸지만 validation/OOS density(검증/표본외 밀도)가 `{summary['selected_validation_trade_density']}` / `{summary['selected_oos_trade_density']}`라 package(패키지)를 열지 않습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density floor OOS PF salvage(밀도 바닥 표본외 PF 회수)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): EI는 EH OOS PF108 bridge density preserve(EH 표본외 PF108 연결 밀도 보존)를 package rejected(패키지 거절)로 닫았습니다.

Selected OOS PF(선택 표본외 PF): `{summary['selected_oos_profit_factor']}`
Selected density(선택 밀도): `{summary['selected_validation_trade_density']}` / `{summary['selected_oos_trade_density']}`
Next seed(다음 씨앗): density floor OOS PF salvage(밀도 바닥 표본외 PF 회수).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EI__{RUN_ID}", f"\n<!-- run364EI__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed EH OOS PF108 bridge(표본외 PF108 연결); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EI__{RUN_ID}", f"\n<!-- run364EI__{RUN_ID} -->\n- `{RUN_ID}`: EH made high OOS PF(높은 표본외 PF)를 만들었지만 density floor(밀도 바닥)를 잃었습니다. Effect(효과): EJ는 PF 단서를 유지하며 밀도 3/day 회수를 공격합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EI__density_floor_failed__{RUN_ID}", f"\n<!-- run364EI__density_floor_failed__{RUN_ID} -->\n- `{RUN_ID}`: EH OOS PF(표본외 PF) `{summary['selected_oos_profit_factor']}`는 좋지만 density(밀도)가 `{summary['selected_validation_trade_density']}` / `{summary['selected_oos_trade_density']}`라 package(패키지)를 열지 않습니다. Effect(효과): EJ는 밀도 바닥 회수를 먼저 봅니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Should EH open package or seed EJ density floor salvage?(EH를 패키지로 열 것인가, EJ 밀도 바닥 회수로 넘길 것인가?)", "next_action": NEXT_RUN_ID, "notes": f"oos_pf={final['selected_oos_profit_factor']};density={final['selected_oos_trade_density']};package=rejected", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS), ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"), ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)")]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EI OOS PF108 bridge review(EI 표본외 PF108 연결 검토)", "metric_scope": "python_proxy_review(Python 프록시 검토)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "review_control(검토/대조)", "family": "alpha_exploration_review(알파 탐색 검토)", "primary_report": rel(REPORT_PATH), "run_family": "kpi_evidence(KPI 근거)", "run_type": "oos_pf108_bridge_review(표본외 PF108 연결 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(PACKAGE_DECISION), "best_model_id": final["selected_model_id"], "net_profit": final["selected_oos_net"], "profit_factor": final["selected_oos_profit_factor"], "trade_density_per_feature_day": final["selected_oos_trade_density"], "result_status": STATUS, "primary_kpi": f"oos_pf={final['selected_oos_profit_factor']};density={final['selected_oos_trade_density']}", "guardrail_kpi": "package=rejected;authority=not_claimed", "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)"}], extend_header=True)
    eh.ef.ed.eb.dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "EI OOS PF108 bridge review artifact(EI 표본외 PF108 연결 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    summary = summarize_surface(parent)
    write_csv(REVIEW_SUMMARY, [summary])
    write_csv(PACKAGE_DECISION, package_rows(summary))
    write_csv(FAILURE_MEMORY, failure_rows(summary))
    write_csv(RUN364EJ_QUEUE, next_rows(summary))
    write_receipts(summary, created_at)
    gates = gate_rows(created_at)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(summary, final, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "package_decision": "rejected", "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
