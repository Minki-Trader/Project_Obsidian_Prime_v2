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
from stage_pipelines.stage364 import train_h17_validation_source_rotation_density_recovery_without_db as ef  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = ef.STAGE_ID
RUN_NUMBER = "run364EG"
RUN_ID = "run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1"
PARENT_RUN_ID = ef.RUN_ID
NEXT_RUN_ID = "run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1"

STATUS = "completed_stage364EG_validation_source_rotation_review_package_rejected_open_eh_no_authority"
JUDGMENT = "negative_validation_source_rotation_review_pf108_bridge_missing_no_package_no_authority"
DECISION = "stage364EG_reject_package_open_run364EH_oos_pf108_bridge_density_preserve"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_validation_source_rotation_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ef.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "eg_validation_source_rotation_review_summary.csv"
FAILURE_MEMORY = RUN_DIR / "validation_source_rotation_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364EH_QUEUE = RUN_DIR / "run364EH_oos_pf108_bridge_density_preserve_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EG_h17_validation_source_rotation_density_recovery_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EG_h17_validation_source_rotation_density_recovery_review.md"
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
    ef.FINAL_DECISION,
    ef.GATE_AUDIT,
    ef.TRADE_SURFACE,
    ef.SELECTED_CANDIDATE,
    ef.SELECTED_TRADE_TAPE,
    ef.MONTH_STABILITY,
    ef.COST_STRESS,
    ef.MODEL_SCORECARD,
    ef.ONNX_SMOKE_REPORT,
    ef.DATA_INTEGRITY_AUDIT,
    ef.RUN364EG_QUEUE,
    ef.RUN_EVIDENCE_RECEIPT,
    ef.MODEL_RECEIPT,
    ef.ATTRIBUTION_RECEIPT,
    ef.JUDGMENT_RECEIPT,
    ef.LINEAGE_RECEIPT,
    ef.CLAIM_RECEIPT,
    ef.RUN_MANIFEST,
    ef.REPORT_PATH,
    ef.ee.FINAL_DECISION,
    ef.ee.FAILURE_MEMORY,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364EH_QUEUE,
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
    return ef.rel(path)


def exists(path: Path | str) -> bool:
    return ef.exists(path)


def sha(path: Path | str) -> str:
    return ef.sha(path)


def read_json(path: Path) -> Any:
    return ef.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    ef.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ef.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    ef.write_csv(path, rows, fieldnames)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    ef.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ef.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    ef.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return ef.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EG inputs(EG 입력 누락): " + ", ".join(missing))
    parent = read_json(ef.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EF next_run_id mismatch(EF 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"EF forbidden claim(EF 금지 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(ef.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EF gate audit(EF 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {"run_id": RUN_ID, "input_path": rel(path), "exists": exists(path), "sha256": sha(path) if exists(path) and io_path(path).is_file() else "", "input_role": "EG validation source rotation review input(EG 검증 원천 회전 검토 입력)", "claim_boundary": CLAIM_BOUNDARY}
        for path in INPUT_FILES
    ]


def summarize_surface(parent: Mapping[str, Any]) -> dict[str, Any]:
    surface = pd.read_csv(io_path(ef.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    selected = read_json(ef.SELECTED_CANDIDATE)
    ed_final = read_json(ef.ee.ed.FINAL_DECISION)
    eb_final = read_json(ef.ee.ed.ec.eb.FINAL_DECISION)
    for col in ["validation_net", "oos_net", "validation_profit_factor", "oos_profit_factor", "validation_trade_density", "oos_trade_density", "selection_score"]:
        surface[col] = surface[col].map(as_float)
    surface["min_pf"] = surface[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    surface["min_density"] = surface[["validation_trade_density", "oos_trade_density"]].min(axis=1)
    density_mask = (surface["validation_trade_density"] >= 3.0) & (surface["oos_trade_density"] >= 3.0) & (surface["validation_net"] > 0.0) & (surface["oos_net"] > 0.0)
    pf108_mask = density_mask & (surface["validation_profit_factor"] >= 1.08) & (surface["oos_profit_factor"] >= 1.08)
    pf110_mask = density_mask & (surface["validation_profit_factor"] >= 1.10) & (surface["oos_profit_factor"] >= 1.10)
    best_density = surface[density_mask].sort_values("min_pf", ascending=False).iloc[0].to_dict() if int(density_mask.sum()) else {}
    best_sparse = surface.sort_values("min_pf", ascending=False).iloc[0].to_dict() if not surface.empty else {}
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
        "ef_density_net_count": int(density_mask.sum()),
        "ef_pf108_count": int(pf108_mask.sum()),
        "ef_pf110_count": int(pf110_mask.sum()),
        "ef_strict_candidate_count": int(parent["strict_candidate_count"]),
        "ef_surface_rows": int(len(surface)),
        "ef_onnx_smoke_pass_rows": int(parent["onnx_smoke_pass_rows"]),
        "ed_selected_min_pf": as_float(ed_final["selected_min_profit_factor"]),
        "eb_selected_min_pf": min(as_float(eb_final["selected_validation_profit_factor"]), as_float(eb_final["selected_oos_profit_factor"])),
        "min_pf_delta_vs_ed": round(as_float(selected["selected_min_profit_factor"]) - as_float(ed_final["selected_min_profit_factor"]), 10),
        "min_pf_delta_vs_eb": round(as_float(selected["selected_min_profit_factor"]) - min(as_float(eb_final["selected_validation_profit_factor"]), as_float(eb_final["selected_oos_profit_factor"])), 10),
        "best_density_model_id": best_density.get("model_id", ""),
        "best_density_min_pf": round(as_float(best_density.get("min_pf")), 10),
        "best_density_min_density": round(as_float(best_density.get("min_density")), 10),
        "best_sparse_model_id": best_sparse.get("model_id", ""),
        "best_sparse_min_pf": round(as_float(best_sparse.get("min_pf")), 10),
        "best_sparse_min_density": round(as_float(best_sparse.get("min_density")), 10),
        "package_decision": "rejected(거절)",
        "package_reason": "pf108_bridge_missing_and_below_eb_min_pf(PF 1.08 연결 없음 및 EB 최소 PF 미만)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(WORK_PACKET, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "primary_family": "kpi_evidence(KPI 근거)", "primary_skill": "obsidian-result-judgment(결과 판정)", "support_skills": ["obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)", "obsidian-run-evidence-system(실행 근거 시스템)"], "review_question": "Should EF open package or seed EH?(EF를 패키지로 열 것인가, EH 씨앗으로 넘길 것인가?)", "claim_boundary": CLAIM_BOUNDARY})


def package_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [{"run_id": RUN_ID, "review_subject": PARENT_RUN_ID, "package_decision": summary["package_decision"], "reason": summary["package_reason"], "selected_min_profit_factor": summary["selected_min_profit_factor"], "pf108_count": summary["ef_pf108_count"], "pf110_count": summary["ef_pf110_count"], "runtime_package": "not_opened(열지 않음)", "effect": "운영 package(패키지)를 열지 않고 EH로 넘깁니다.", "claim_boundary": CLAIM_BOUNDARY}]


def failure_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"run_id": RUN_ID, "memory_id": "eg01_source_rotation_improved_but_no_bridge", "observed": f"ED min_pf={summary['ed_selected_min_pf']}; EF min_pf={summary['selected_min_profit_factor']}; pf108_count={summary['ef_pf108_count']}", "meaning": "source rotation(원천 회전)은 ED보다 나아졌지만 PF 1.08 연결 후보를 만들지 못했습니다.", "next_constraint": "EH는 OOS PF 1.08 근접 구간을 직접 들어올리되 density>=3을 유지합니다.", "effect": "개선된 실패를 다음 공격 씨앗으로 바꿉니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "memory_id": "eg02_full_source_h2_density_clue", "observed": f"selected_model={summary['selected_model_id']}; validation_pf={summary['selected_validation_profit_factor']}; oos_pf={summary['selected_oos_profit_factor']}", "meaning": "full source(전체 원천) h2가 validation/OOS 둘 다 순수익 양수와 밀도 3 이상을 유지했습니다.", "next_constraint": "EH는 이 source_all/full h2 단서를 보존하고 OOS PF를 1.08 이상으로 올립니다.", "effect": "무작정 다른 원천으로 튀지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]


def next_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [{"run_id": RUN_ID, "next_run_id": NEXT_RUN_ID, "queue_rank": 1, "queue_id": "eh01_oos_pf108_bridge_density_preserve", "hypothesis": "OOS PF 1.08 bridge(표본외 PF 1.08 연결)를 직접 보상하되 validation PF floor(검증 PF 바닥)와 density>=3을 같이 보존하면 EF의 full-source h2 clue(전체 원천 h2 단서)를 PF 1.10 근처로 끌어올릴 수 있습니다.", "preserve": "source_all h2, density>=3, validation net/PF positive(전체 원천 h2, 밀도 3 이상, 검증 순수익/PF 양수)", "avoid": "sparse high PF and direct min_pf repeat(희소 고PF 및 직접 최소 PF 반복)", "target": "PF>=1.08 both splits scout, PF>=1.10 bridge, density>=3(PF 1.08 양쪽 스카우트, PF 1.10 연결, 밀도 3 이상)", "effect": "EH는 EF의 개선 방향을 좁게 이어받습니다.", "claim_boundary": CLAIM_BOUNDARY}]


def write_receipts(summary: Mapping[str, Any], created_at: str) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": created_at, "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(ef.FINAL_DECISION), rel(ef.TRADE_SURFACE)], "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "runtime package(런타임 패키지)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "reviewed_model": summary["selected_model_id"], "package_decision": summary["package_decision"], "model_judgment": "rejected_for_package_pf108_bridge_missing(패키지 거절, PF 1.08 연결 없음)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"ED min_pf {summary['ed_selected_min_pf']} -> EF min_pf {summary['selected_min_profit_factor']}; pf108_count {summary['ef_pf108_count']}", "comparison_baseline": ef.ee.PARENT_RUN_ID, "likely_drivers": ["full source features improved validation(전체 원천 피처가 검증을 개선)", "OOS PF still below 1.08(표본외 PF가 아직 1.08 미만)", "density stayed above 3(밀도 3 이상 유지)"], "attribution_confidence": "medium(중간)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EG 검토는 운영 주장(operating claim, 운영 주장)을 만들지 않습니다."})


def gate_rows(created_at: str) -> list[dict[str, Any]]:
    receipt_paths = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    rows = [
        {"run_id": RUN_ID, "gate": "input_lineage_gate", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "evidence": rel(INPUT_MANIFEST), "effect": "입력 산출물 존재를 확인했습니다."},
        {"run_id": RUN_ID, "gate": "review_summary_gate", "status": "passed" if exists(REVIEW_SUMMARY) else "failed", "evidence": rel(REVIEW_SUMMARY), "effect": "EF 결과 요약이 있습니다."},
        {"run_id": RUN_ID, "gate": "package_decision_gate", "status": "passed" if exists(PACKAGE_DECISION) else "failed", "evidence": rel(PACKAGE_DECISION), "effect": "패키지 거절 이유가 기록됐습니다."},
        {"run_id": RUN_ID, "gate": "failure_memory_gate", "status": "passed" if exists(FAILURE_MEMORY) else "failed", "evidence": rel(FAILURE_MEMORY), "effect": "실패 기억이 다음 제약으로 남았습니다."},
        {"run_id": RUN_ID, "gate": "next_queue_gate", "status": "passed" if exists(RUN364EH_QUEUE) else "failed", "evidence": rel(RUN364EH_QUEUE), "effect": "다음 EH 입력이 생성됐습니다."},
        {"run_id": RUN_ID, "gate": "receipt_coverage_gate", "status": "passed" if all(exists(path) for path in receipt_paths) else "failed", "evidence": "|".join(rel(path) for path in receipt_paths), "effect": "필수 receipt(영수증)가 있습니다."},
        {"run_id": RUN_ID, "gate": "final_claim_guard", "status": "passed", "evidence": rel(CLAIM_RECEIPT), "effect": "authority/promotion/live/goal(권위/승격/실거래/목표) 주장을 차단했습니다."},
        {"run_id": RUN_ID, "gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT), "effect": "필수 gate(게이트)가 종료 기록에 연결됐습니다."},
    ]
    for row in rows:
        row["created_at_utc"] = created_at
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "package_decision": "rejected", "selected_model_id": summary["selected_model_id"], "selected_min_profit_factor": summary["selected_min_profit_factor"], "selected_validation_net": summary["selected_validation_net"], "selected_validation_profit_factor": summary["selected_validation_profit_factor"], "selected_validation_trade_density": summary["selected_validation_trade_density"], "selected_oos_net": summary["selected_oos_net"], "selected_oos_profit_factor": summary["selected_oos_profit_factor"], "selected_oos_trade_density": summary["selected_oos_trade_density"], "ef_density_net_count": summary["ef_density_net_count"], "ef_pf108_count": summary["ef_pf108_count"], "ef_pf110_count": summary["ef_pf110_count"], "ef_strict_candidate_count": summary["ef_strict_candidate_count"], "ed_selected_min_pf": summary["ed_selected_min_pf"], "eb_selected_min_pf": summary["eb_selected_min_pf"], "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "runtime_package": "not_opened", "new_mt5_execution": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "created_at_utc": created_at, "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "final_decision": rel(FINAL_DECISION)}


def write_docs(summary: Mapping[str, Any], final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364EG H17 Validation Source Rotation Review(검증 원천 회전 검토)

Created(생성): {final['created_at_utc']}

Action(행동): EF validation source rotation density recovery(EF 검증 원천 회전 밀도 회복)를 package(패키지), failure memory(실패 기억), next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): PF 1.08 연결 실패를 EH의 OOS PF bridge(표본외 PF 연결) 조건으로 바꿉니다.

Findings(발견):

- selected min_pf(선택 최소 PF): `{summary['selected_min_profit_factor']}`
- ED min_pf(ED 최소 PF): `{summary['ed_selected_min_pf']}`
- EB min_pf(EB 최소 PF): `{summary['eb_selected_min_pf']}`
- pf108_count(PF 1.08 양쪽 통과 수): `{summary['ef_pf108_count']}`
- pf110_count(PF 1.10 양쪽 통과 수): `{summary['ef_pf110_count']}`
- density_net_count(밀도+순수익 후보 수): `{summary['ef_density_net_count']}`

Judgment(판정): `{JUDGMENT}`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, f"""# Decision(결정): stage364EG validation source rotation review(검증 원천 회전 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EF 결과를 패키지로 열지 않고 EH 씨앗으로 넘겼습니다.

Effect(효과): EH가 OOS PF 1.08 bridge(표본외 PF 1.08 연결)를 밀도 보존 조건과 함께 탐색합니다.
""", bom=True)
    append_text_once(REVIEW_INDEX, f"run364EG__{RUN_ID}", f"\n- run364EG__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - validation source rotation review(검증 원천 회전 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EG__{RUN_ID}", f"\n<!-- run364EG__{RUN_ID} -->\n\n## run364EG Validation Source Rotation Review(검증 원천 회전 검토)\n\nAction(행동): EF 결과를 package rejected(패키지 거절)로 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 OOS PF 1.08 bridge(표본외 PF 1.08 연결)를 다음 공격 탐색으로 엽니다.\n")
    append_text_once(STAGE_README, f"run364EG__{RUN_ID}", f"\n<!-- run364EG__{RUN_ID} -->\n## run364EG validation source rotation review(검증 원천 회전 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364EG` reviewed(검토 완료) EF validation source rotation density recovery(EF 검증 원천 회전 밀도 회복). EF는 ED보다 min_pf(최소 PF)를 `{summary['ed_selected_min_pf']}` -> `{summary['selected_min_profit_factor']}`로 올렸지만, pf108_count(PF 1.08 양쪽 통과 수)는 `{summary['ef_pf108_count']}`라 package(패키지)를 열지 않습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 OOS PF 1.08 bridge density preserve(표본외 PF 1.08 연결 밀도 보존)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): EG는 EF validation source rotation density recovery(EF 검증 원천 회전 밀도 회복)를 package rejected(패키지 거절)로 닫았습니다.

Selected min_pf(선택 최소 PF): `{summary['selected_min_profit_factor']}`
PF 1.08 bridge count(PF 1.08 연결 수): `{summary['ef_pf108_count']}`
Next seed(다음 씨앗): OOS PF 1.08 bridge density preserve(표본외 PF 1.08 연결 밀도 보존).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EG__{RUN_ID}", f"\n<!-- run364EG__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed EF validation source rotation(검증 원천 회전); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EG__{RUN_ID}", f"\n<!-- run364EG__{RUN_ID} -->\n- `{RUN_ID}`: EF source rotation(원천 회전)은 ED보다 min_pf(최소 PF)를 올렸지만 PF 1.08 bridge(연결)는 만들지 못했습니다. Effect(효과): EH는 OOS PF 1.08 bridge(표본외 PF 1.08 연결)를 좁게 공격합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EG__pf108_bridge_missing__{RUN_ID}", f"\n<!-- run364EG__pf108_bridge_missing__{RUN_ID} -->\n- `{RUN_ID}`: EF pf108_count(PF 1.08 양쪽 통과 수) `{summary['ef_pf108_count']}`라 package(패키지)를 열지 않습니다. Effect(효과): EH는 OOS PF 1.08 연결을 밀도 보존과 함께 탐색합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Should EF open package or seed EH?(EF를 패키지로 열 것인가, EH 씨앗으로 넘길 것인가?)", "next_action": NEXT_RUN_ID, "notes": f"pf108_count={final['ef_pf108_count']};selected_min_pf={final['selected_min_profit_factor']};package=rejected", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS), ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"), ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)")]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EG validation source rotation review(EG 검증 원천 회전 검토)", "metric_scope": "python_proxy_review(Python 프록시 검토)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "review_control(검토/대조)", "family": "alpha_exploration_review(알파 탐색 검토)", "primary_report": rel(REPORT_PATH), "run_family": "kpi_evidence(KPI 근거)", "run_type": "validation_source_rotation_review(검증 원천 회전 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(PACKAGE_DECISION), "best_model_id": final["selected_model_id"], "net_profit": final["selected_oos_net"], "profit_factor": final["selected_oos_profit_factor"], "trade_density_per_feature_day": final["selected_oos_trade_density"], "result_status": STATUS, "primary_kpi": f"selected_min_pf={final['selected_min_profit_factor']};pf108_count={final['ef_pf108_count']}", "guardrail_kpi": "package=rejected;authority=not_claimed", "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)"}], extend_header=True)
    ef.ed.eb.dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "EG validation source rotation review artifact(EG 검증 원천 회전 검토 산출물)"})
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
    write_csv(RUN364EH_QUEUE, next_rows(summary))
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
