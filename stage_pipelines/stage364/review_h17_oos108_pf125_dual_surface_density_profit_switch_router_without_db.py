from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db as gz  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db as hd  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db as hb  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = hd.STAGE_ID
STAGE_DIR = hd.STAGE_DIR
REVIEW_DIR = hd.REVIEW_DIR
SPEC_DIR = hd.SPEC_DIR
SELECTED_DIR = hd.SELECTED_DIR

RUN_NUMBER = "run364HE"
RUN_ID = "run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1"
PARENT_RUN_ID = hd.RUN_ID
NEXT_RUN_ID = "run364HF_train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1"

STATUS = "completed_stage364HE_dual_surface_router_review_near_miss_positive_clue_no_package_no_authority"
JUDGMENT = "positive_clue_no_package_hd_near_miss_improved_oos_profit_cost_density_missed_net_pf_targets_no_authority"
DECISION = "stage364HE_open_run364HF_near_miss_profit_pf_lift_switch_router"
CLAIM_BOUNDARY = (
    "review_only_dual_surface_router_near_miss_positive_clue_no_runtime_package_no_new_mt5_execution_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "he_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "he_surface_diagnostic.csv"
DELTA_ATTRIBUTION = RUN_DIR / "he_delta_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "he_package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "he_failure_memory.csv"
RUN364HF_QUEUE = RUN_DIR / "he_hf_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HE_dual_surface_density_profit_switch_router_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HE_dual_surface_density_profit_switch_router_review.md"
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
    hd.FINAL_DECISION,
    hd.GATE_AUDIT,
    hd.TRADE_SURFACE,
    hd.SELECTED_CANDIDATE,
    hd.SELECTED_TRADE_TAPE,
    hd.SOURCE_CANDIDATE_AUDIT,
    hd.ROUTE_ATTRIBUTION,
    hd.ONNX_SMOKE_REPORT,
    hd.DATA_INTEGRITY_AUDIT,
    hd.RUN364HE_QUEUE,
    gz.FINAL_DECISION,
    hb.FINAL_DECISION,
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
    RUN364HF_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    THIS_FILE,
]


def rel(path: Path | str) -> str:
    return hd.rel(path)


def exists(path: Path | str) -> bool:
    return hd.exists(path)


def sha(path: Path | str) -> str:
    return hd.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return hd.as_float(value, default)


def read_json(path: Path) -> dict[str, Any]:
    return hd.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    hd.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    hd.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    hd.write_csv(path, rows)


def append_text_once(path: Path, marker: str, text: str) -> None:
    hd.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    hd.append_or_replace_csv(path, key_fields, rows)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        hd.io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HE inputs(HE 입력 누락): " + ", ".join(missing))
    parent = read_json(hd.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HD next_run_id mismatch(HD 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden HD claim(금지된 HD 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(hd.io_path(hd.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HD gate audit(HD 게이트 감사)가 모두 passed(통과)가 아닙니다.")


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and hd.io_path(path).is_file() else "",
            "input_role": "HE review input(HE 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "result_review(결과 검토)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-run-evidence-system(실행 근거 시스템)",
            ],
            "review_question": "Does HD dual-surface router deserve package work or only near-miss continuation?(HD 이중 표면 라우터가 패키지 작업 가치가 있는가, 아니면 근접 실패 후속 탐색인가?)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def diagnostic_rows(hd_final: Mapping[str, Any], surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "diagnostic": "selected_near_miss(선택 근접 실패)",
            "observed": f"oos_net={hd_final['selected_oos_net']};oos_pf={hd_final['selected_oos_profit_factor']};oos_cost06={hd_final['selected_oos_cost06_net']};oos_density={hd_final['selected_oos_trade_density']}",
            "effect": "cost0.6(비용0.6)과 density(밀도)는 통과했지만 net/PF(순수익/수익 팩터)가 목표선에 못 미칩니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "diagnostic": "surface_counts(표면 수)",
            "observed": f"surface_rows={len(surface)};preserve={hd_final['preserve_floor_pass_count']};repair={hd_final['repair_target_pass_count']};strict={hd_final['strict_candidate_count']}",
            "effect": "preserve floor(보존 바닥)는 많이 통과했지만 repair target(수리 목표)은 통과하지 못했습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for column, target in [("oos_net", 60.0), ("oos_profit_factor", 1.18), ("oos_cost06_net", 0.0), ("oos_trade_density", 1.35), ("combined_trade_density", 1.30), ("combined_cost09_net", -120.0)]:
        value = as_float(hd_final.get(f"selected_{column}", hd_final.get(column)))
        rows.append(
            {
                "run_id": RUN_ID,
                "diagnostic": f"target_gap_{column}(목표 차이 {column})",
                "observed": round(value - target, 10),
                "effect": "양수면 해당 목표를 넘었고 음수면 아직 부족합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SURFACE_DIAGNOSTIC, rows)
    return rows


def delta_rows(hd_final: Mapping[str, Any], gz_final: Mapping[str, Any], hb_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    metrics = [
        ("oos_net", "selected_oos_net"),
        ("oos_profit_factor", "selected_oos_profit_factor"),
        ("oos_cost06_net", "selected_oos_cost06_net"),
        ("oos_trade_density", "selected_oos_trade_density"),
        ("combined_trade_density", "selected_combined_trade_density"),
        ("combined_cost09_net", "selected_combined_cost09_net"),
    ]
    rows = []
    for label, key in metrics:
        hd_value = as_float(hd_final[key])
        gz_value = as_float(gz_final[key])
        hb_value = as_float(hb_final[key])
        rows.append(
            {
                "run_id": RUN_ID,
                "metric": label,
                "hd_value": round(hd_value, 10),
                "gz_value": round(gz_value, 10),
                "hb_value": round(hb_value, 10),
                "delta_vs_gz": round(hd_value - gz_value, 10),
                "delta_vs_hb": round(hd_value - hb_value, 10),
                "effect": "HD가 기준 GZ와 단독 HB 중 어느 실패 축을 수리했는지 보여줍니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(DELTA_ATTRIBUTION, rows)
    return rows


def review_summary_rows(hd_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "review_subject": PARENT_RUN_ID,
            "selected_route_variant_id": hd_final["selected_route_variant_id"],
            "selected_route_policy": hd_final["selected_route_policy"],
            "oos_net": hd_final["selected_oos_net"],
            "oos_profit_factor": hd_final["selected_oos_profit_factor"],
            "oos_cost06_net": hd_final["selected_oos_cost06_net"],
            "oos_trade_density": hd_final["selected_oos_trade_density"],
            "combined_trade_density": hd_final["selected_combined_trade_density"],
            "combined_cost09_net": hd_final["selected_combined_cost09_net"],
            "strict_candidate_count": hd_final["strict_candidate_count"],
            "review_judgment": JUDGMENT,
            "effect": "HD는 package(패키지)는 아니지만 다음 미세 수익/PF 리프트 탐색 가치가 있는 positive clue(긍정 단서)입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(REVIEW_SUMMARY, rows)
    return rows


def package_decision_rows(hd_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    reasons = [
        "strict_candidate_count=0",
        f"oos_net={hd_final['selected_oos_net']}<60",
        f"oos_pf={hd_final['selected_oos_profit_factor']}<1.18",
        "no_runtime_package(MT5 런타임 패키지 없음)",
        "no_mt5_runtime_probe(MT5 런타임 탐침 없음)",
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "package_eligible": "false",
            "promotion_candidate": "false",
            "positive_clue": "true",
            "decision": "no_package_open_hf_near_miss_profit_pf_lift(패키지 없음, HF 근접 실패 수익/PF 리프트 열기)",
            "reasons": "|".join(reasons),
            "effect": "좋아진 프록시 수치를 운영 패키지로 착각하지 않고 다음 탐색 조건으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(PACKAGE_DECISION, rows)
    return rows


def failure_memory_rows(hd_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "memory_id": "hd_near_miss_profit_pf_gap(HD 근접 실패 수익/PF 차이)",
            "failure_axis": "net_pf_target_miss(순수익/PF 목표 미달)",
            "observed": f"oos_net_gap={round(60.0 - as_float(hd_final['selected_oos_net']), 4)};pf_gap={round(1.18 - as_float(hd_final['selected_oos_profit_factor']), 10)}",
            "do_next": "HF should lift net/PF with validation-side quality filters, not broad fallback expansion(HF는 넓은 대체 확장이 아니라 검증 측 품질 필터로 순수익/PF를 올려야 함)",
            "avoid": "do not lower density floor or accept extra OOS-only overfit(밀도 바닥 완화나 표본외 전용 과적합 금지)",
            "effect": "실패를 금지 조건이 아니라 다음 공격 탐색의 제약으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "hd_preserve_success_clue(HD 보존 성공 단서)",
            "failure_axis": "none_positive_clue(없음, 긍정 단서)",
            "observed": f"delta_oos_cost06_vs_gz={hd_final['delta_oos_cost06_vs_gz']};delta_oos_density_vs_gz={hd_final['delta_oos_density_vs_gz']}",
            "do_next": "preserve GZ anchor and small HB score-plus fallback pattern(GZ 기준과 작은 HB 점수 추가 대체 패턴 보존)",
            "avoid": "do not switch to HB-only single-score replacement(HB 단독 단일 점수 교체 금지)",
            "effect": "HD에서 실제로 좋아진 축을 HF의 seed(씨앗)로 유지합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(FAILURE_MEMORY, rows)
    return rows


def queue_rows(hd_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "hf01_near_miss_profit_pf_lift_switch_router(근접 실패 수익/PF 리프트 전환 라우터)",
            "seed_route": hd_final["selected_route_variant_id"],
            "seed_policy": hd_final["selected_route_policy"],
            "required_preserve": "oos_density>=1.35;combined_density>=1.30;combined_cost0.9>=-120",
            "required_repair": "oos_net>=60;oos_pf>=1.18;oos_cost0.6>=0",
            "exploration_direction": "score-band microgrid, validation-positive loss veto, source row neighborhood(점수 구간 미세 격자, 검증 양수 손실 차단, 원천 행 이웃)",
            "effect": "HD near miss(근접 실패)를 작은 품질 리프트 탐색으로 이어갑니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364HF_QUEUE, rows)
    return rows


def gate_rows(final: Mapping[str, Any], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION) and exists(FAILURE_MEMORY), REVIEW_SUMMARY, "HE 검토 요약/패키지 결정/실패 기억을 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "HD/GZ/HB 입력 계보를 기록했습니다."),
        ("kpi_review_gate", exists(SURFACE_DIAGNOSTIC) and exists(DELTA_ATTRIBUTION), DELTA_ATTRIBUTION, "KPI 차이와 목표 미달 축을 분리했습니다."),
        ("package_boundary_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "패키지 미개방과 긍정 단서를 분리했습니다."),
        ("next_action_gate", exists(RUN364HF_QUEUE), RUN364HF_QUEUE, "HF 다음 탐색 조건을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 영수증을 작성했습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트 커버리지 감사를 종료 기록에 연결했습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]
    write_csv(GATE_AUDIT, rows)
    return rows


def final_payload(created_at: str, gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    hd_final = read_json(hd.FINAL_DECISION)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "package_eligible": False,
        "promotion_candidate": False,
        "positive_clue": True,
        "selected_route_variant_id": hd_final["selected_route_variant_id"],
        "selected_route_policy": hd_final["selected_route_policy"],
        "selected_oos_net": hd_final["selected_oos_net"],
        "selected_oos_profit_factor": hd_final["selected_oos_profit_factor"],
        "selected_oos_cost06_net": hd_final["selected_oos_cost06_net"],
        "selected_oos_trade_density": hd_final["selected_oos_trade_density"],
        "selected_combined_trade_density": hd_final["selected_combined_trade_density"],
        "selected_combined_cost09_net": hd_final["selected_combined_cost09_net"],
        "delta_oos_net_vs_gz": hd_final["delta_oos_net_vs_gz"],
        "delta_oos_profit_factor_vs_gz": hd_final["delta_oos_profit_factor_vs_gz"],
        "delta_oos_cost06_vs_gz": hd_final["delta_oos_cost06_vs_gz"],
        "delta_oos_density_vs_gz": hd_final["delta_oos_density_vs_gz"],
        "delta_combined_density_vs_gz": hd_final["delta_combined_density_vs_gz"],
        "delta_combined_cost09_vs_gz": hd_final["delta_combined_cost09_vs_gz"],
        "strict_candidate_count": hd_final["strict_candidate_count"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "runtime_package": "not_opened",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "review_summary": rel(REVIEW_SUMMARY), "surface_diagnostic": rel(SURFACE_DIAGNOSTIC), "package_decision": rel(PACKAGE_DECISION), "measurement_boundary": "review of Python proxy router only(Python 프록시 라우터 검토 전용)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change_vs_gz": {"delta_oos_net": final["delta_oos_net_vs_gz"], "delta_oos_pf": final["delta_oos_profit_factor_vs_gz"], "delta_oos_cost06": final["delta_oos_cost06_vs_gz"], "delta_oos_density": final["delta_oos_density_vs_gz"], "delta_combined_density": final["delta_combined_density_vs_gz"], "delta_combined_cost09": final["delta_combined_cost09_vs_gz"]}, "meaning": "HD improves several GZ axes but misses package target(HD는 GZ 여러 축을 개선했지만 패키지 목표는 미달)"})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(DELTA_ATTRIBUTION), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": JUDGMENT, "claim_boundary": "positive clue only, no package/no authority(긍정 단서만, 패키지/권위 없음)", "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and hd.io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and hd.io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "review_connected_to_next_seed(검토가 다음 씨앗에 연결됨)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "HD near miss(근접 실패)를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364HE Dual-Surface Router Review(이중 표면 라우터 검토)

Created(생성): {final['created_at_utc']}

Action(행동): HD dual-surface router(HD 이중 표면 라우터)를 GZ/HB 기준과 비교하고, package(패키지) 가능성, positive clue(긍정 단서), next seed(다음 씨앗)를 분리했습니다.

Effect(효과): 좋아진 프록시(proxy, 프록시)를 운영 후보로 과장하지 않고, HF near-miss lift(HF 근접 실패 리프트)로 이어갑니다.

- judgment(판정): `{final['judgment']}`
- package_eligible(패키지 적격): `{final['package_eligible']}`
- positive_clue(긍정 단서): `{final['positive_clue']}`
- selected route(선택 라우트): `{final['selected_route_variant_id']}`
- OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
- delta vs GZ(기준 GZ 대비 차이): net `{final['delta_oos_net_vs_gz']}`, PF `{final['delta_oos_profit_factor_vs_gz']}`, cost0.6 `{final['delta_oos_cost06_vs_gz']}`, density `{final['delta_oos_density_vs_gz']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364HE Dual-Surface Router Review(이중 표면 라우터 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): HD는 package(패키지)로 열지 않고 HF near-miss profit/PF lift(HF 근접 실패 수익/PF 리프트)로 넘깁니다.

Effect(효과): 수익 복구 단서는 살리고 운영 주장은 차단합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364HE__{RUN_ID}", f"\n- run364HE__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - dual-surface router review(이중 표면 라우터 검토), next(다음) `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HE__{RUN_ID}", f"\n<!-- run364HE__{RUN_ID} -->\n\n## run364HE Dual-Surface Router Review(이중 표면 라우터 검토)\n\nAction(행동): HD 근접 실패를 검토하고 package(패키지)는 열지 않았습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 수익/PF 미세 리프트를 시도합니다.\n")
    append_text_once(STAGE_README, f"run364HE__{RUN_ID}", f"\n<!-- run364HE__{RUN_ID} -->\n## run364HE dual-surface router review(이중 표면 라우터 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
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

Current truth(현재 진실): `run364HE` reviewed(검토 완료) HD dual-surface router(HD 이중 표면 라우터). HD는 OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6) `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`로 GZ 대비 개선했지만, package(패키지)는 열지 않았습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 score-band microgrid(점수 구간 미세 격자)와 validation-positive loss veto(검증 양수 손실 차단)로 수익/PF를 작게 끌어올립니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): HE marked(표시) HD as positive clue no package(긍정 단서, 패키지 없음).

HD OOS net/PF/density/cost0.6(HD 표본외 순수익/수익 팩터/밀도/비용0.6): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_cost06_net']}`
HD delta vs GZ(HD 기준 GZ 대비 차이): net `{final['delta_oos_net_vs_gz']}`, PF `{final['delta_oos_profit_factor_vs_gz']}`, cost0.6 `{final['delta_oos_cost06_vs_gz']}`, density `{final['delta_oos_density_vs_gz']}`

Next seed(다음 씨앗): HF near-miss profit/PF lift switch router(HF 근접 실패 수익/PF 리프트 전환 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364HE__{RUN_ID}", f"\n<!-- run364HE__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed HD dual-surface router(HD 이중 표면 라우터); positive clue(긍정 단서) but no package(패키지 없음); next(다음) `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HE__{RUN_ID}", f"\n<!-- run364HE__{RUN_ID} -->\n- `{RUN_ID}`: HD near miss(HD 근접 실패)를 positive clue(긍정 단서)로 보존했습니다. Effect(효과): HF에서 작은 수익/PF 리프트를 공격적으로 탐색합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HE__package_rejected__{RUN_ID}", f"\n<!-- run364HE__package_rejected__{RUN_ID} -->\n- `{RUN_ID}`: HD는 package(패키지)로 열지 않았습니다. 이유(reason, 이유): strict_candidate_count=0, OOS net/PF 목표 미달, MT5 runtime probe(MT5 런타임 탐침) 없음. Effect(효과): 운영 주장을 차단하고 HF 탐색 조건으로 바꿉니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len([path for path in OUTPUT_FILES if exists(path)])
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Should HD near miss become package or next seed?(HD 근접 실패를 패키지로 열지 다음 씨앗으로 넘길지?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"package_eligible={final['package_eligible']};positive_clue={final['positive_clue']};oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
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
                "kpi_scope": "HE review(HE 검토)",
                "metric_scope": "review_of_python_proxy_router(Python 프록시 라우터 검토)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "source_authority": "review_no_mt5(검토, MT5 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "result_review(결과 검토)",
                "run_type": "dual_surface_router_review(이중 표면 라우터 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(REVIEW_SUMMARY),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    try:
        hb.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and hd.io_path(path).is_file():
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
                    "notes": "HE dual-surface router review artifact(HE 이중 표면 라우터 검토 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "command": f"python {rel(THIS_FILE)}",
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and hd.io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if hd.io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    hd_final = read_json(hd.FINAL_DECISION)
    gz_final = read_json(gz.FINAL_DECISION)
    hb_final = read_json(hb.FINAL_DECISION)
    surface = pd.read_csv(hd.io_path(hd.TRADE_SURFACE), encoding="utf-8-sig").fillna("")
    review_summary_rows(hd_final)
    diagnostic_rows(hd_final, surface)
    delta_rows(hd_final, gz_final, hb_final)
    package_decision_rows(hd_final)
    failure_memory_rows(hd_final)
    queue_rows(hd_final)
    created_at = hd.now_utc()
    gates = gate_rows({"runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"}, final_written=False)
    final = final_payload(created_at, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, final_written=True)
    final = final_payload(created_at, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(hd.json_ready({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "package_eligible": final["package_eligible"], "positive_clue": final["positive_clue"], "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "next_run_id": NEXT_RUN_ID}), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
