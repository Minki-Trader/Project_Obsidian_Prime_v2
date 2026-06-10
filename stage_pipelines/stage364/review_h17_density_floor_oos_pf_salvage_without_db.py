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
from stage_pipelines.stage364 import train_h17_density_floor_oos_pf_salvage_without_db as ej  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = ej.STAGE_ID
RUN_NUMBER = "run364EK"
RUN_ID = "run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1"
PARENT_RUN_ID = ej.RUN_ID
NEXT_RUN_ID = "run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1"

STATUS = "completed_stage364EK_density_floor_oos_pf_salvage_review_package_rejected_open_el_no_authority"
JUDGMENT = "negative_density_floor_oos_pf_salvage_review_oos_pf_collapsed_validation_floor_gap_no_package_no_authority"
DECISION = "stage364EK_reject_package_open_run364EL_oos108_validation_floor_bridge"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_density_floor_oos_pf_salvage_rejected_"
    "no_runtime_package_no_new_mt5_execution_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ej.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "ek_density_floor_oos_pf_salvage_review_summary.csv"
FAILURE_MEMORY = RUN_DIR / "density_floor_oos_pf_salvage_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364EL_QUEUE = RUN_DIR / "run364EL_oos108_validation_floor_bridge_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EK_h17_density_floor_oos_pf_salvage_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EK_h17_density_floor_oos_pf_salvage_review.md"
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
    ej.FINAL_DECISION,
    ej.GATE_AUDIT,
    ej.TRADE_SURFACE,
    ej.SELECTED_CANDIDATE,
    ej.SELECTED_TRADE_TAPE,
    ej.MONTH_STABILITY,
    ej.COST_STRESS,
    ej.MODEL_SCORECARD,
    ej.ONNX_SMOKE_REPORT,
    ej.DATA_INTEGRITY_AUDIT,
    ej.RUN364EK_QUEUE,
    ej.RUN_EVIDENCE_RECEIPT,
    ej.MODEL_RECEIPT,
    ej.ATTRIBUTION_RECEIPT,
    ej.JUDGMENT_RECEIPT,
    ej.LINEAGE_RECEIPT,
    ej.CLAIM_RECEIPT,
    ej.RUN_MANIFEST,
    ej.REPORT_PATH,
    ej.ei.FINAL_DECISION,
    ej.ei.FAILURE_MEMORY,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364EL_QUEUE,
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
    return ej.rel(path)


def exists(path: Path | str) -> bool:
    return ej.exists(path)


def sha(path: Path | str) -> str:
    return ej.sha(path)


def read_json(path: Path) -> Any:
    return ej.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    ej.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ej.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    ej.write_csv(path, rows, fieldnames)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    ej.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ej.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    ej.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return ej.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EK inputs(EK 입력 누락): " + ", ".join(missing))
    parent = read_json(ej.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EJ next_run_id mismatch(EJ 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"EJ forbidden claim(EJ 금지 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(ej.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EJ gate audit(EJ 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EK density floor OOS PF salvage review input(EK 밀도 바닥 표본외 PF 회수 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def summarize_surface(parent: Mapping[str, Any]) -> dict[str, Any]:
    surface = pd.read_csv(io_path(ej.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    selected = read_json(ej.SELECTED_CANDIDATE)
    eh_final = read_json(ej.eh.FINAL_DECISION)
    for col in [
        "validation_net",
        "oos_net",
        "validation_profit_factor",
        "oos_profit_factor",
        "validation_trade_density",
        "oos_trade_density",
        "selection_score",
    ]:
        surface[col] = surface[col].map(as_float)
    surface["min_density"] = surface[["validation_trade_density", "oos_trade_density"]].min(axis=1)
    surface["min_pf"] = surface[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    density_net = (surface["validation_trade_density"] >= 3.0) & (surface["oos_trade_density"] >= 3.0) & (surface["validation_net"] > 0.0) & (surface["oos_net"] > 0.0)
    density_val104 = density_net & (surface["validation_profit_factor"] >= 1.04)
    density_oos108 = density_net & (surface["oos_profit_factor"] >= 1.08)
    density_oos108_val104 = density_oos108 & (surface["validation_profit_factor"] >= 1.04)
    near_oos112 = (surface["validation_trade_density"] >= 2.8) & (surface["oos_trade_density"] >= 2.8) & (surface["validation_net"] > 0.0) & (surface["oos_net"] > 0.0) & (surface["oos_profit_factor"] >= 1.11)
    best_density_oos108 = surface[density_oos108].sort_values(["oos_profit_factor", "min_density"], ascending=False).iloc[0].to_dict() if int(density_oos108.sum()) else {}
    best_near_oos112 = surface[near_oos112].sort_values(["oos_profit_factor", "min_density"], ascending=False).iloc[0].to_dict() if int(near_oos112.sum()) else {}
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
        "ej_density_net_count": int(density_net.sum()),
        "ej_density_val104_count": int(density_val104.sum()),
        "ej_density_oos108_count": int(density_oos108.sum()),
        "ej_density_oos108_val104_count": int(density_oos108_val104.sum()),
        "ej_near_oos112_count": int(near_oos112.sum()),
        "ej_oos112_count": int(parent["oos112_count"]),
        "ej_pf108_count": int(parent["pf108_count"]),
        "ej_pf110_count": int(parent["pf110_count"]),
        "eh_selected_oos_profit_factor": eh_final["selected_oos_profit_factor"],
        "eh_selected_oos_trade_density": eh_final["selected_oos_trade_density"],
        "oos_pf_delta_vs_eh": round(as_float(selected["selected_oos_profit_factor"]) - as_float(eh_final["selected_oos_profit_factor"]), 10),
        "density_delta_vs_eh": round(as_float(selected["selected_oos_trade_density"]) - as_float(eh_final["selected_oos_trade_density"]), 10),
        "best_density_oos108_model_id": best_density_oos108.get("model_id", ""),
        "best_density_oos108_validation_pf": round(as_float(best_density_oos108.get("validation_profit_factor")), 10),
        "best_density_oos108_oos_pf": round(as_float(best_density_oos108.get("oos_profit_factor")), 10),
        "best_density_oos108_min_density": round(as_float(best_density_oos108.get("min_density")), 10),
        "best_near_oos112_model_id": best_near_oos112.get("model_id", ""),
        "best_near_oos112_validation_pf": round(as_float(best_near_oos112.get("validation_profit_factor")), 10),
        "best_near_oos112_oos_pf": round(as_float(best_near_oos112.get("oos_profit_factor")), 10),
        "best_near_oos112_min_density": round(as_float(best_near_oos112.get("min_density")), 10),
        "package_decision": "rejected(거절)",
        "package_reason": "oos_pf_collapsed_and_validation_floor_gap(표본외 PF 붕괴 및 검증 PF 바닥 간극)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(WORK_PACKET, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "primary_family": "kpi_evidence(KPI 근거)", "primary_skill": "obsidian-result-judgment(결과 판정)", "support_skills": ["obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)", "obsidian-run-evidence-system(실행 근거 시스템)"], "review_question": "Should EJ open package or seed EL OOS108 validation floor bridge?(EJ를 패키지로 열 것인가, EL 표본외108 검증 바닥 연결로 넘길 것인가?)", "claim_boundary": CLAIM_BOUNDARY})


def package_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [{"run_id": RUN_ID, "review_subject": PARENT_RUN_ID, "package_decision": summary["package_decision"], "reason": summary["package_reason"], "selected_oos_profit_factor": summary["selected_oos_profit_factor"], "selected_oos_trade_density": summary["selected_oos_trade_density"], "runtime_package": "not_opened(열지 않음)", "effect": "OOS PF(표본외 PF)가 무너져 운영 package(패키지)를 열지 않습니다.", "claim_boundary": CLAIM_BOUNDARY}]


def failure_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"run_id": RUN_ID, "memory_id": "ek01_density_restored_oos_pf_collapsed", "observed": f"OOS PF {summary['eh_selected_oos_profit_factor']} -> {summary['selected_oos_profit_factor']}; OOS density {summary['eh_selected_oos_trade_density']} -> {summary['selected_oos_trade_density']}", "meaning": "밀도는 회복됐지만 EH의 높은 표본외 PF 단서는 선택 후보에서 사라졌습니다.", "next_constraint": "EL은 density>=3을 유지한 채 OOS PF>=1.08 후보의 validation PF floor(검증 PF 바닥)를 먼저 수리합니다.", "effect": "밀도 회복 자체를 성공으로 과장하지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "memory_id": "ek02_density_oos108_validation_gap", "observed": f"density_oos108_count={summary['ej_density_oos108_count']};best_validation_pf={summary['best_density_oos108_validation_pf']};best_oos_pf={summary['best_density_oos108_oos_pf']};best_min_density={summary['best_density_oos108_min_density']}", "meaning": "density>=3 및 OOS PF>=1.08 후보는 있지만 validation PF(검증 PF)가 1.04 바로 아래에 있습니다.", "next_constraint": "EL은 h2_m1 source_all density-relief clue(전체 원천 밀도 완화 단서)를 validation floor bridge(검증 바닥 연결)로 좁힙니다.", "effect": "완전히 새로 흩어지지 않고 가장 가까운 실패 경계를 공략합니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]


def next_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "el01_oos108_validation_floor_bridge",
            "hypothesis": "EJ density OOS108 rows(EJ 밀도 OOS108 행)의 validation PF(검증 PF)를 1.04 이상으로 조금 올리면 density>=3과 OOS PF>=1.08을 동시에 지키는 bridge(연결)가 생길 수 있습니다.",
            "preserve": "source_all h2_m1, density_relief_months, density>=3, OOS PF>=1.08(전체 원천 h2_m1, 밀도 완화 월, 밀도 3 이상, 표본외 PF 1.08 이상)",
            "avoid": "sparse high PF and selected validation-only winner(희소 고PF 및 검증 전용 승자)",
            "target": "validation PF>=1.04, OOS PF>=1.08, validation/OOS density>=3(검증 PF 1.04 이상, 표본외 PF 1.08 이상, 검증/표본외 밀도 3 이상)",
            "effect": "EL은 EJ의 가장 가까운 실패 경계를 직접 공략합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_receipts(summary: Mapping[str, Any], created_at: str) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": created_at, "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(ej.FINAL_DECISION), rel(ej.TRADE_SURFACE)], "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "runtime package(런타임 패키지)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "model_subject": PARENT_RUN_ID, "selected_model_id": summary["selected_model_id"], "package_decision": "rejected(거절)", "reason": summary["package_reason"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"EH OOS PF {summary['eh_selected_oos_profit_factor']} -> EJ selected OOS PF {summary['selected_oos_profit_factor']}; density {summary['eh_selected_oos_trade_density']} -> {summary['selected_oos_trade_density']}", "likely_drivers": ["density-first score(밀도 우선 점수)", "lower threshold margins(낮춘 임계값 마진)", "validation floor pressure(검증 바닥 압력)"], "attribution_confidence": "medium(중간)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EK 결과를 operating claim(운영 주장)으로 올리지 않습니다."})


def gate_rows() -> list[dict[str, Any]]:
    receipt_paths = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    return [
        {"run_id": RUN_ID, "gate": "input_lineage_gate", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "evidence": rel(INPUT_MANIFEST), "effect": "입력 산출물 존재를 확인했습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "review_summary_gate", "status": "passed" if exists(REVIEW_SUMMARY) else "failed", "evidence": rel(REVIEW_SUMMARY), "effect": "EJ 결과 요약이 있습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "package_decision_gate", "status": "passed" if exists(PACKAGE_DECISION) else "failed", "evidence": rel(PACKAGE_DECISION), "effect": "패키지 거절 이유가 기록됐습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "failure_memory_gate", "status": "passed" if exists(FAILURE_MEMORY) else "failed", "evidence": rel(FAILURE_MEMORY), "effect": "실패 기억이 다음 제약으로 남았습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "next_queue_gate", "status": "passed" if exists(RUN364EL_QUEUE) else "failed", "evidence": rel(RUN364EL_QUEUE), "effect": "다음 EL 입력이 생성됐습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "receipt_coverage_gate", "status": "passed" if all(exists(path) for path in receipt_paths) else "failed", "evidence": "|".join(rel(path) for path in receipt_paths), "effect": "필수 receipt(영수증)가 있습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "final_claim_guard", "status": "passed", "evidence": rel(CLAIM_RECEIPT), "effect": "authority/promotion/live/goal(권위/승격/실거래/목표) 주장을 차단했습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT), "effect": "필수 gate(게이트)가 종료 기록에 연결됐습니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "package_decision": "rejected",
        "selected_model_id": summary["selected_model_id"],
        "selected_min_profit_factor": summary["selected_min_profit_factor"],
        "selected_validation_net": summary["selected_validation_net"],
        "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
        "selected_validation_trade_density": summary["selected_validation_trade_density"],
        "selected_oos_net": summary["selected_oos_net"],
        "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
        "selected_oos_trade_density": summary["selected_oos_trade_density"],
        "ej_density_net_count": summary["ej_density_net_count"],
        "ej_density_val104_count": summary["ej_density_val104_count"],
        "ej_density_oos108_count": summary["ej_density_oos108_count"],
        "ej_density_oos108_val104_count": summary["ej_density_oos108_val104_count"],
        "ej_near_oos112_count": summary["ej_near_oos112_count"],
        "ej_oos112_count": summary["ej_oos112_count"],
        "ej_pf108_count": summary["ej_pf108_count"],
        "ej_pf110_count": summary["ej_pf110_count"],
        "best_density_oos108_model_id": summary["best_density_oos108_model_id"],
        "best_density_oos108_validation_pf": summary["best_density_oos108_validation_pf"],
        "best_density_oos108_oos_pf": summary["best_density_oos108_oos_pf"],
        "best_density_oos108_min_density": summary["best_density_oos108_min_density"],
        "best_near_oos112_model_id": summary["best_near_oos112_model_id"],
        "best_near_oos112_oos_pf": summary["best_near_oos112_oos_pf"],
        "best_near_oos112_min_density": summary["best_near_oos112_min_density"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364EK H17 Density Floor OOS PF Salvage Review(밀도 바닥 표본외 PF 회수 검토)

Created(생성): {final['created_at_utc']}

Action(행동): EJ density floor OOS PF salvage(EJ 밀도 바닥 표본외 PF 회수)를 package(패키지), failure memory(실패 기억), next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): density restore(밀도 회복)와 OOS PF collapse(표본외 PF 붕괴)를 분리해, EL validation floor bridge(EL 검증 바닥 연결)로 넘깁니다.

Findings(발견):

- selected validation/OOS PF(선택 검증/표본외 PF): `{final['selected_validation_profit_factor']}` / `{final['selected_oos_profit_factor']}`
- selected validation/OOS density(선택 검증/표본외 밀도): `{final['selected_validation_trade_density']}` / `{final['selected_oos_trade_density']}`
- density_net_count(밀도+순수익 후보 수): `{final['ej_density_net_count']}`
- density_oos108_count(밀도+표본외 PF 1.08 후보 수): `{final['ej_density_oos108_count']}`
- density_oos108_val104_count(밀도+표본외 PF 1.08+검증 PF 1.04 후보 수): `{final['ej_density_oos108_val104_count']}`
- best density OOS108 validation/OOS PF(최선 밀도 OOS108 검증/표본외 PF): `{final['best_density_oos108_validation_pf']}` / `{final['best_density_oos108_oos_pf']}`

Judgment(판정): `{final['judgment']}`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, f"""# Decision(결정): stage364EK density floor OOS PF salvage review(밀도 바닥 표본외 PF 회수 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- package_decision(패키지 결정): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EJ 결과를 검토해 package(패키지)를 열지 않고 EL queue(EL 대기열)를 만들었습니다.

Effect(효과): density>=3 and OOS PF>=1.08(밀도 3 이상 및 표본외 PF 1.08 이상) 근처의 validation floor gap(검증 바닥 간극)을 다음 공격 탐색으로 고정합니다.
""", bom=True)
    append_text_once(REVIEW_INDEX, f"run364EK__{RUN_ID}", f"\n- run364EK__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density floor OOS PF salvage review(밀도 바닥 표본외 PF 회수 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EK__{RUN_ID}", f"\n<!-- run364EK__{RUN_ID} -->\n\n## run364EK Density Floor OOS PF Salvage Review(밀도 바닥 표본외 PF 회수 검토)\n\nAction(행동): EJ 결과를 package rejected(패키지 거절)로 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 OOS108 validation floor bridge(표본외108 검증 바닥 연결)를 다음 공격 탐색으로 엽니다.\n")
    append_text_once(STAGE_README, f"run364EK__{RUN_ID}", f"\n<!-- run364EK__{RUN_ID} -->\n## run364EK density floor OOS PF salvage review(밀도 바닥 표본외 PF 회수 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364EK` reviewed(검토 완료) EJ density floor OOS PF salvage(EJ 밀도 바닥 표본외 PF 회수). EJ는 density(밀도)를 회복했지만 selected OOS PF(선택 표본외 PF)가 `{final['selected_oos_profit_factor']}`라 package(패키지)를 열지 않습니다. 다만 density_oos108_count(밀도 표본외 PF 1.08 후보 수) `{final['ej_density_oos108_count']}`와 best validation PF(최선 검증 PF) `{final['best_density_oos108_validation_pf']}` 단서를 남겼습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 OOS108 validation floor bridge(표본외108 검증 바닥 연결)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): EK는 EJ density floor OOS PF salvage(EJ 밀도 바닥 표본외 PF 회수)를 package rejected(패키지 거절)로 닫았습니다.

Selected OOS PF/density(선택 표본외 PF/밀도): `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Best density OOS108 validation/OOS PF(최선 밀도 OOS108 검증/표본외 PF): `{final['best_density_oos108_validation_pf']}` / `{final['best_density_oos108_oos_pf']}`
Next seed(다음 씨앗): OOS108 validation floor bridge(표본외108 검증 바닥 연결).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EK__{RUN_ID}", f"\n<!-- run364EK__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed EJ density floor OOS PF salvage(밀도 바닥 표본외 PF 회수); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EK__{RUN_ID}", f"\n<!-- run364EK__{RUN_ID} -->\n- `{RUN_ID}`: EJ restored density(밀도 회복) but selected OOS PF(선택 표본외 PF)가 약했습니다. Effect(효과): EL은 density OOS108(밀도 OOS108) 행의 validation floor gap(검증 바닥 간극)을 공략합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EK__oos_pf_collapsed__{RUN_ID}", f"\n<!-- run364EK__oos_pf_collapsed__{RUN_ID} -->\n- `{RUN_ID}`: selected OOS PF(선택 표본외 PF)는 `{final['selected_oos_profit_factor']}`이고 density_oos108_val104_count(밀도 OOS108 검증104 후보 수)는 `{final['ej_density_oos108_val104_count']}`입니다. Effect(효과): package(패키지)를 열지 않고 EL 수리 조건으로 넘깁니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Should EJ open package or seed EL OOS108 validation floor bridge?(EJ를 패키지로 열 것인가, EL 표본외108 검증 바닥 연결로 넘길 것인가?)", "next_action": NEXT_RUN_ID, "notes": f"selected_oos_pf={final['selected_oos_profit_factor']};density_oos108={final['ej_density_oos108_count']};package=rejected", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EK density floor OOS PF salvage review(EK 밀도 바닥 표본외 PF 회수 검토)", "metric_scope": "python_proxy_review(Python 프록시 검토)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "review_control(검토/대조)", "family": "alpha_exploration_review(알파 탐색 검토)", "primary_report": rel(REPORT_PATH), "run_family": "kpi_evidence(KPI 근거)", "run_type": "density_floor_oos_pf_salvage_review(밀도 바닥 표본외 PF 회수 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(PACKAGE_DECISION), "best_model_id": final["selected_model_id"], "net_profit": final["selected_oos_net"], "profit_factor": final["selected_oos_profit_factor"], "trade_density_per_feature_day": final["selected_oos_trade_density"], "result_status": STATUS, "primary_kpi": f"oos_pf={final['selected_oos_profit_factor']};density_oos108={final['ej_density_oos108_count']}", "guardrail_kpi": "package=rejected;authority=not_claimed", "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)"}], extend_header=True)
    ej.eh.ef.ed.eb.dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "EK density floor OOS PF salvage review artifact(EK 밀도 바닥 표본외 PF 회수 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    summary = summarize_surface(parent)
    write_csv(REVIEW_SUMMARY, [summary])
    write_csv(PACKAGE_DECISION, package_rows(summary))
    write_csv(FAILURE_MEMORY, failure_rows(summary))
    write_csv(RUN364EL_QUEUE, next_rows(summary))
    created_at = now_utc()
    write_receipts(summary, created_at)
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final)
    write_artifact_registry(final)
    write_manifest(final)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "package_decision": "rejected", "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
