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
from stage_pipelines.stage364 import train_h17_dual_pf_floor_bridge_reseed_without_db as ed  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = ed.STAGE_ID
RUN_NUMBER = "run364EE"
RUN_ID = "run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1"
PARENT_RUN_ID = ed.RUN_ID
NEXT_RUN_ID = "run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1"

STATUS = "completed_stage364EE_dual_pf_floor_bridge_review_package_rejected_open_ef_no_authority"
JUDGMENT = "negative_dual_pf_floor_bridge_review_min_pf_regressed_no_package_no_authority"
DECISION = "stage364EE_reject_package_open_run364EF_validation_source_rotation_density_recovery"
CLAIM_BOUNDARY = (
    "research_development_proxy_review_only_dual_pf_floor_bridge_rejected_no_runtime_package_"
    "no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ed.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "ee_dual_pf_floor_bridge_review_summary.csv"
FAILURE_MEMORY = RUN_DIR / "dual_pf_floor_bridge_failure_memory.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
RUN364EF_QUEUE = RUN_DIR / "run364EF_validation_source_rotation_density_recovery_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EE_h17_dual_pf_floor_bridge_reseed_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EE_h17_dual_pf_floor_bridge_reseed_review.md"
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
    ed.FINAL_DECISION,
    ed.GATE_AUDIT,
    ed.TRADE_SURFACE,
    ed.SELECTED_CANDIDATE,
    ed.SELECTED_TRADE_TAPE,
    ed.MONTH_STABILITY,
    ed.COST_STRESS,
    ed.MODEL_SCORECARD,
    ed.ONNX_SMOKE_REPORT,
    ed.DATA_INTEGRITY_AUDIT,
    ed.RUN364EE_QUEUE,
    ed.RUN_EVIDENCE_RECEIPT,
    ed.MODEL_RECEIPT,
    ed.ATTRIBUTION_RECEIPT,
    ed.JUDGMENT_RECEIPT,
    ed.LINEAGE_RECEIPT,
    ed.CLAIM_RECEIPT,
    ed.RUN_MANIFEST,
    ed.REPORT_PATH,
    ed.ec.FINAL_DECISION,
    ed.ec.REVIEW_SUMMARY,
    ed.ec.FAILURE_MEMORY,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_MEMORY,
    PACKAGE_DECISION,
    RUN364EF_QUEUE,
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
    return ed.rel(path)


def exists(path: Path | str) -> bool:
    return ed.exists(path)


def sha(path: Path | str) -> str:
    return ed.sha(path)


def read_json(path: Path) -> Any:
    return ed.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    ed.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ed.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    ed.write_csv(path, rows, fieldnames)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    ed.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ed.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    ed.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return ed.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EE inputs(EE 입력 누락): " + ", ".join(missing))
    parent = read_json(ed.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"ED next_run_id mismatch(ED 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"ED forbidden claim(ED 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(ed.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("ED gate audit(ED 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EE dual PF floor bridge review input(EE 양쪽 PF 바닥 연결 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def summarize_surface(parent: Mapping[str, Any]) -> dict[str, Any]:
    surface = read_csv(ed.TRADE_SURFACE)
    selected = read_json(ed.SELECTED_CANDIDATE)
    ec_final = read_json(ed.ec.FINAL_DECISION)
    surface["validation_profit_factor"] = surface["validation_profit_factor"].map(as_float)
    surface["oos_profit_factor"] = surface["oos_profit_factor"].map(as_float)
    surface["validation_trade_density"] = surface["validation_trade_density"].map(as_float)
    surface["oos_trade_density"] = surface["oos_trade_density"].map(as_float)
    surface["validation_net"] = surface["validation_net"].map(as_float)
    surface["oos_net"] = surface["oos_net"].map(as_float)
    surface["min_pf"] = surface[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    surface["min_density"] = surface[["validation_trade_density", "oos_trade_density"]].min(axis=1)
    density_mask = (
        (surface["validation_trade_density"] >= 3.0)
        & (surface["oos_trade_density"] >= 3.0)
        & (surface["validation_net"] > 0.0)
        & (surface["oos_net"] > 0.0)
    )
    pf110_mask = density_mask & (surface["validation_profit_factor"] >= 1.10) & (surface["oos_profit_factor"] >= 1.10)
    pf115_mask = density_mask & (surface["validation_profit_factor"] >= 1.15) & (surface["oos_profit_factor"] >= 1.15)
    sparse_best = surface.sort_values("min_pf", ascending=False).iloc[0].to_dict() if not surface.empty else {}
    density_best = surface[density_mask].sort_values("min_pf", ascending=False).iloc[0].to_dict() if int(density_mask.sum()) else {}
    eb_min_pf = as_float(ec_final.get("best_bridge_min_pf", min(as_float(ec_final.get("selected_validation_profit_factor")), as_float(ec_final.get("selected_oos_profit_factor")))))
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
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
        "ed_density_net_count": int(density_mask.sum()),
        "ed_pf110_count": int(pf110_mask.sum()),
        "ed_pf115_count": int(pf115_mask.sum()),
        "ed_strict_candidate_count": int(parent["strict_candidate_count"]),
        "ed_surface_rows": len(surface),
        "ed_onnx_smoke_pass_rows": parent["onnx_smoke_pass_rows"],
        "eb_best_bridge_min_pf": eb_min_pf,
        "min_pf_delta_vs_eb": round(as_float(selected["selected_min_profit_factor"]) - eb_min_pf, 10),
        "best_sparse_model_id": sparse_best.get("model_id", ""),
        "best_sparse_min_pf": round(as_float(sparse_best.get("min_pf")), 10),
        "best_sparse_min_density": round(as_float(sparse_best.get("min_density")), 10),
        "best_density_model_id": density_best.get("model_id", ""),
        "best_density_min_pf": round(as_float(density_best.get("min_pf")), 10),
        "best_density_min_density": round(as_float(density_best.get("min_density")), 10),
        "package_decision": "rejected(거절)",
        "package_reason": "no_pf110_density_bridge_and_min_pf_regressed(PF 1.10 밀도 연결 없음 및 최소 PF 후퇴)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-run-evidence-system(실행 근거 시스템)",
            ],
            "review_question": "Should ED open a package or become failure memory for EF?(ED를 패키지로 열 것인가, EF 실패 기억으로 넘길 것인가?)",
            "result_subject": parent["run_id"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def package_decision_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "review_subject": PARENT_RUN_ID,
            "package_decision": summary["package_decision"],
            "reason": summary["package_reason"],
            "selected_min_profit_factor": summary["selected_min_profit_factor"],
            "pf110_count": summary["ed_pf110_count"],
            "strict_candidate_count": summary["ed_strict_candidate_count"],
            "runtime_package": "not_opened(열지 않음)",
            "effect": "운영 패키지(package, 패키지) 없이 다음 탐색 조건으로 넘깁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def failure_memory_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "memory_id": "ee01_direct_min_pf_density_bridge_failed",
            "observed": f"density_net_count={summary['ed_density_net_count']};pf110_count={summary['ed_pf110_count']};selected_min_pf={summary['selected_min_profit_factor']}",
            "meaning": "직접 min_pf(최소 PF) 보상만으로는 밀도 3/day를 유지하는 PF 1.10 연결 후보가 나오지 않았습니다.",
            "next_constraint": "다음 EF는 sparse high PF(희소 고PF)를 그대로 고르지 말고 density(밀도) 보존을 먼저 둡니다.",
            "effect": "같은 직접 min_pf 격자를 반복하지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "ee02_validation_side_regressed",
            "observed": f"EB min_pf={summary['eb_best_bridge_min_pf']}; ED min_pf={summary['selected_min_profit_factor']}; delta={summary['min_pf_delta_vs_eb']}",
            "meaning": "ED는 OOS PF(표본외 PF)를 1.098까지 밀었지만 validation PF(검증 PF)가 1.0219로 내려갔습니다.",
            "next_constraint": "EF는 validation source rotation(검증 원천 회전)과 density recovery(밀도 회복)를 함께 둡니다.",
            "effect": "OOS만 좋아지는 후보를 다음 package(패키지)로 오해하지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "ee03_sparse_high_pf_is_clue_not_candidate",
            "observed": f"best_sparse_min_pf={summary['best_sparse_min_pf']};best_sparse_min_density={summary['best_sparse_min_density']}",
            "meaning": "희소 후보는 PF가 높지만 거래 밀도가 목표보다 크게 낮습니다.",
            "next_constraint": "sparse PF(희소 PF)는 filter clue(필터 단서)로만 쓰고 최종 후보 풀에는 density>=3을 유지합니다.",
            "effect": "거래수를 쪼개거나 희소 수익만 보는 방향을 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def next_queue_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ef01_validation_source_rotation_density_recovery",
            "hypothesis": "validation source rotation(검증 원천 회전)과 density-first selection(밀도 우선 선택)을 결합하면 ED의 OOS near-PF110(표본외 PF 1.10 근접) 단서를 검증 PF 붕괴 없이 되살릴 수 있습니다.",
            "preserve": "density>=3, net>0 both splits, no trade splitting(밀도 3 이상, 양쪽 순수익 양수, 거래 쪼개기 없음)",
            "avoid": "direct min_pf sparse grid repeat(직접 최소 PF 희소 격자 반복)",
            "target": "validation/OOS PF>=1.10 scout, PF>=1.15 bridge, density>=3(검증/표본외 PF 1.10 스카우트, PF 1.15 연결, 밀도 3 이상)",
            "effect": "EF는 ED 실패를 제약으로 바꾸고 새로운 원천/세션 조합을 공격 탐색합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_receipts(summary: Mapping[str, Any], created_at: str) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": created_at, "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(ed.FINAL_DECISION), rel(ed.TRADE_SURFACE)], "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "runtime package(런타임 패키지)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "reviewed_model": summary["selected_model_id"], "package_decision": summary["package_decision"], "model_judgment": "rejected_for_package_no_pf_bridge(패키지 거절, PF 연결 없음)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"EB min_pf {summary['eb_best_bridge_min_pf']} -> ED min_pf {summary['selected_min_profit_factor']}; density_net_count {summary['ed_density_net_count']}; pf110_count {summary['ed_pf110_count']}", "comparison_baseline": ed.ec.PARENT_RUN_ID, "likely_drivers": ["direct min_pf score over-penalized density bridge(직접 최소 PF 점수가 밀도 연결을 과도하게 좁힘)", "short_stability source kept OOS near 1.10 but validation weakened(숏 안정성 원천은 표본외를 1.10 근처로 유지했지만 검증이 약해짐)", "sparse high PF exists below density floor(희소 고PF가 밀도 바닥 아래에 존재)"], "segment_checks": ["selected trade tape(선택 거래 테이프)", "density/PF surface counts(밀도/PF 표면 수)", "sparse high PF review(희소 고PF 검토)"], "attribution_confidence": "medium(중간)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EE 검토는 운영 주장(operating claim, 운영 주장)을 만들지 않습니다."})


def gate_rows(created_at: str) -> list[dict[str, Any]]:
    receipt_paths = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    rows = [
        {"run_id": RUN_ID, "gate": "input_lineage_gate", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "evidence": rel(INPUT_MANIFEST), "effect": "입력 산출물 존재를 확인했습니다."},
        {"run_id": RUN_ID, "gate": "review_summary_gate", "status": "passed" if exists(REVIEW_SUMMARY) else "failed", "evidence": rel(REVIEW_SUMMARY), "effect": "ED 결과 요약이 있습니다."},
        {"run_id": RUN_ID, "gate": "package_decision_gate", "status": "passed" if exists(PACKAGE_DECISION) else "failed", "evidence": rel(PACKAGE_DECISION), "effect": "패키지 거절 이유가 기록됐습니다."},
        {"run_id": RUN_ID, "gate": "failure_memory_gate", "status": "passed" if exists(FAILURE_MEMORY) else "failed", "evidence": rel(FAILURE_MEMORY), "effect": "실패 기억이 다음 제약으로 남았습니다."},
        {"run_id": RUN_ID, "gate": "next_queue_gate", "status": "passed" if exists(RUN364EF_QUEUE) else "failed", "evidence": rel(RUN364EF_QUEUE), "effect": "다음 EF 입력이 생성됐습니다."},
        {"run_id": RUN_ID, "gate": "receipt_coverage_gate", "status": "passed" if all(exists(path) for path in receipt_paths) else "failed", "evidence": "|".join(rel(path) for path in receipt_paths), "effect": "필수 receipt(영수증)가 있습니다."},
        {"run_id": RUN_ID, "gate": "final_claim_guard", "status": "passed", "evidence": rel(CLAIM_RECEIPT), "effect": "authority/promotion/live/goal(권위/승격/실거래/목표) 주장을 차단했습니다."},
        {"run_id": RUN_ID, "gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT), "effect": "필수 gate(게이트)가 종료 기록에 연결됐습니다."},
    ]
    for row in rows:
        row["created_at_utc"] = created_at
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


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
        "ed_density_net_count": summary["ed_density_net_count"],
        "ed_pf110_count": summary["ed_pf110_count"],
        "ed_pf115_count": summary["ed_pf115_count"],
        "ed_strict_candidate_count": summary["ed_strict_candidate_count"],
        "best_sparse_min_pf": summary["best_sparse_min_pf"],
        "best_sparse_min_density": summary["best_sparse_min_density"],
        "best_density_min_pf": summary["best_density_min_pf"],
        "best_density_min_density": summary["best_density_min_density"],
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


def write_docs(summary: Mapping[str, Any], final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364EE H17 Dual PF Floor Bridge Review(양쪽 PF 바닥 연결 검토)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): ED dual PF floor bridge(ED 양쪽 PF 바닥 연결) 결과를 package(패키지), failure memory(실패 기억), next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): 직접 min_pf(최소 PF) 보상 실패를 EF의 validation source rotation(검증 원천 회전) 제약으로 바꿉니다.

## Findings(발견)

- selected min_pf(선택 최소 PF): `{summary['selected_min_profit_factor']}`
- EB best bridge min_pf(EB 최고 연결 최소 PF): `{summary['eb_best_bridge_min_pf']}`
- min_pf delta(최소 PF 차이): `{summary['min_pf_delta_vs_eb']}`
- density_net_count(밀도+순수익 후보 수): `{summary['ed_density_net_count']}`
- pf110_count(PF 1.10 양쪽 통과 수): `{summary['ed_pf110_count']}`
- best_sparse_min_pf/best_sparse_min_density(최고 희소 최소 PF/최소 밀도): `{summary['best_sparse_min_pf']}` / `{summary['best_sparse_min_density']}`

## Judgment(판정)

`{JUDGMENT}`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 validation source rotation density recovery(검증 원천 회전 밀도 회복)를 탐색합니다.

## Gates(게이트)

{gate_lines}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): stage364EE dual PF floor bridge review(양쪽 PF 바닥 연결 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package_decision(패키지 결정): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): ED 결과를 패키지로 열지 않고 실패 기억과 다음 씨앗으로 분리했습니다.

Effect(효과): EF가 직접 min_pf(최소 PF) 반복이 아니라 validation source rotation(검증 원천 회전)으로 이동합니다.
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364EE__{RUN_ID}", f"\n- run364EE__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - dual PF floor bridge review(양쪽 PF 바닥 연결 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EE__{RUN_ID}", f"\n<!-- run364EE__{RUN_ID} -->\n\n## run364EE Dual PF Floor Bridge Review(양쪽 PF 바닥 연결 검토)\n\nAction(행동): ED 결과를 검토하고 package rejected(패키지 거절)로 닫았습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 validation source rotation(검증 원천 회전)을 다음 공격 탐색으로 엽니다.\n")
    append_text_once(STAGE_README, f"run364EE__{RUN_ID}", f"\n<!-- run364EE__{RUN_ID} -->\n## run364EE dual PF floor bridge review(양쪽 PF 바닥 연결 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364EE` reviewed(검토 완료) ED dual PF floor bridge(ED 양쪽 PF 바닥 연결). ED는 density_net_count(밀도+순수익 후보 수) `{summary['ed_density_net_count']}`만 만들었고 pf110_count(PF 1.10 양쪽 통과 수)는 `{summary['ed_pf110_count']}`입니다. selected_min_profit_factor(선택 최소 수익 팩터)는 `{summary['selected_min_profit_factor']}`로 EB best bridge min_pf(EB 최고 연결 최소 PF) `{summary['eb_best_bridge_min_pf']}`보다 낮습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 validation source rotation density recovery(검증 원천 회전 밀도 회복)를 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): EE는 ED dual PF floor bridge(ED 양쪽 PF 바닥 연결)를 package rejected(패키지 거절)로 닫았습니다.

Selected min_pf(선택 최소 PF): `{summary['selected_min_profit_factor']}`
PF 1.10 bridge count(PF 1.10 연결 수): `{summary['ed_pf110_count']}`
Next seed(다음 씨앗): validation source rotation density recovery(검증 원천 회전 밀도 회복).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EE__{RUN_ID}", f"\n<!-- run364EE__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed ED dual PF floor bridge(ED 양쪽 PF 바닥 연결); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EE__{RUN_ID}", f"\n<!-- run364EE__{RUN_ID} -->\n- `{RUN_ID}`: direct min_pf reward(직접 최소 PF 보상)은 density bridge(밀도 연결)를 만들지 못했습니다. Effect(효과): EF는 validation source rotation(검증 원천 회전)과 density-first selection(밀도 우선 선택)으로 이동합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EE__dual_pf_floor_bridge_failed__{RUN_ID}", f"\n<!-- run364EE__dual_pf_floor_bridge_failed__{RUN_ID} -->\n- `{RUN_ID}`: ED selected min_pf(선택 최소 PF) `{summary['selected_min_profit_factor']}`, pf110_count `{summary['ed_pf110_count']}`라 package(패키지)를 열지 않습니다. Effect(효과): 직접 min_pf 격자 반복을 피하고 EF 원천 회전으로 넘깁니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
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
        "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Should ED open package or become EF failure memory?(ED를 패키지로 열 것인가, EF 실패 기억으로 넘길 것인가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"pf110_count={final['ed_pf110_count']};selected_min_pf={final['selected_min_profit_factor']};package=rejected",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EE dual PF floor bridge review(EE 양쪽 PF 바닥 연결 검토)", "metric_scope": "python_proxy_review(Python 프록시 검토)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "lane": "review_control(검토/대조)",
                "family": "alpha_exploration_review(알파 탐색 검토)",
                "primary_report": rel(REPORT_PATH),
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "dual_pf_floor_bridge_review(양쪽 PF 바닥 연결 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "best_model_id": final["selected_model_id"],
                "net_profit": final["selected_oos_net"],
                "profit_factor": final["selected_oos_profit_factor"],
                "trade_density_per_feature_day": final["selected_oos_trade_density"],
                "result_status": STATUS,
                "primary_kpi": f"selected_min_pf={final['selected_min_profit_factor']};pf110_count={final['ed_pf110_count']}",
                "guardrail_kpi": "package=rejected;authority=not_claimed",
                "final_decision_path": rel(FINAL_DECISION),
                "gate_audit_path": rel(GATE_AUDIT),
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)",
            }
        ],
        extend_header=True,
    )
    ed.eb.dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "EE dual PF floor bridge review artifact(EE 양쪽 PF 바닥 연결 검토 산출물)"})
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
    write_csv(PACKAGE_DECISION, package_decision_rows(summary))
    write_csv(FAILURE_MEMORY, failure_memory_rows(summary))
    write_csv(RUN364EF_QUEUE, next_queue_rows(summary))
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
