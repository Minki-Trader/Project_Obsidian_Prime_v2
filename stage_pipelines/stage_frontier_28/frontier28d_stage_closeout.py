from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_28 import frontier28b_train_only_stability_gap_proxy_scout as f28b
from stage_pipelines.stage_frontier_28 import frontier28c_stability_gap_repair_or_closeout_decision as f28c
from stage_pipelines.stage_frontier_28 import materialize_frontier28a_stage_open as f28a


STAGE_ID = f28a.STAGE_ID
RUN_ID = "frontier28D_stage_closeout_stability_gap_penalty_v1"
RUN_NUMBER = "frontier28D"
PARENT_RUN_ID = f28c.RUN_ID
STATUS = "closed_preserved_clue_negative_memory_stability_gap_scout_only_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"
NEXT_STAGE_ID = "stage_frontier_29__train_only_loss_concentration_veto_for_pf_dd_balance_onnx_scout"
NEXT_RUN_ID = "frontier29A_stage_open_train_only_loss_concentration_veto_pf_dd_balance_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_28_train_only_stability_gap_penalty_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_28/frontier28d_stage_closeout.py")

F28A_SUMMARY = STAGE_ROOT / "02_runs" / f28a.RUN_ID / "stage_open_summary.json"
F28B_SUMMARY = STAGE_ROOT / "02_runs" / f28b.RUN_ID / "final_summary.json"
F28B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f28b.RUN_ID / "stability_gap_candidate_summary.csv"
F28B_CHUNK_METRICS = STAGE_ROOT / "02_runs" / f28b.RUN_ID / "stability_gap_chunk_metrics.csv"
F28C_SUMMARY = STAGE_ROOT / "02_runs" / f28c.RUN_ID / "final_summary.json"
F28C_REPAIR_AUDIT = STAGE_ROOT / "02_runs" / f28c.RUN_ID / "repair_rejection_audit.csv"

GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier28_stage_open/small_review_retry")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier28_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = f28c.PRESERVED_CLUE
NEGATIVE_MEMORY = f28c.NEGATIVE_MEMORY
NEXT_HYPOTHESIS_CLUE = f28c.NEXT_HYPOTHESIS_CLUE
REPAIR_DECISION = f28c.REPAIR_DECISION
RUNTIME_PROBE_BLOCKER = (
    "runtime_probe_ineligible_no_handoff_candidate_after_f28c_repair_decision"
    "(전선28C 수리 결정 뒤 인계 후보 없어 런타임 탐침 부적격)"
)
ONNX_BLOCKER = (
    "onnx_branch_unattempted_no_handoff_candidate_after_f28c_repair_decision"
    "(전선28C 수리 결정 뒤 인계 후보 없어 ONNX 미시도)"
)


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    stage_open = read_json(F28A_SUMMARY)
    f28b_summary = read_json(F28B_SUMMARY)
    f28c_summary = read_json(F28C_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F28B_CANDIDATE_SUMMARY))
    chunk_metrics = pd.read_csv(io_path(F28B_CHUNK_METRICS))
    repair_audit = pd.read_csv(io_path(F28C_REPAIR_AUDIT))
    grok = load_grok_closeout()
    local = validate_context(stage_open, f28b_summary, f28c_summary, candidate_summary, chunk_metrics, repair_audit, grok)
    final = build_final(created_at, stage_open, f28b_summary, f28c_summary, candidate_summary, chunk_metrics, repair_audit, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "preserved_clue": final["preserved_clue"],
        "negative_memory": final["negative_memory"],
        "runtime_probe_blocker": final["runtime_probe_blocker"],
        "onnx_blocker": final["onnx_blocker"],
        "grok_classification": final["grok_closeout"]["classification"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_CLOSEOUT_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def load_grok_closeout() -> dict[str, Any]:
    metadata = read_json(GROK_CLOSEOUT_PACKET / "metadata.json")
    output = read_text(GROK_CLOSEOUT_PACKET / "clean_output.md")
    lower = output.lower()
    accepted = (
        "verdict" in lower
        and "accepted" in lower
        and "closeout_class_ok" in lower
        and "yes" in lower
        and "repair_rejection_ok" in lower
        and "runtime_probe_status_ok" in lower
        and "next_clue_ok" in lower
    )
    return {
        "packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "prompt": (GROK_CLOSEOUT_PACKET / "prompt.md").as_posix(),
        "clean_output": (GROK_CLOSEOUT_PACKET / "clean_output.md").as_posix(),
        "metadata": (GROK_CLOSEOUT_PACKET / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": "accepted_preserved_clue_negative_memory_closeout(수용, 보존 단서+부정 기억 마감)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "accepted": accepted,
        "output_excerpt": output[:3200],
    }


def validate_context(
    stage_open: dict[str, Any],
    f28b_summary: dict[str, Any],
    f28c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    chunk_metrics: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier28": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier28d": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == f28a.RUN_ID,
        "stage_open_grok_retry_accepted": stage_open.get("grok", {}).get("retry", {}).get("classification", "").startswith("accepted"),
        "f28b_parent_matches": f28b_summary.get("run_id") == f28b.RUN_ID,
        "f28b_reference_stability_rows": int(f28b_summary.get("reference_union_rows", -1)) == 234
        and int(f28b_summary.get("stability_candidate_rows", -1)) == 234,
        "f28b_scout_19_seed_handoff_zero": int(f28b_summary.get("scout_clue_rows", -1)) == 19
        and int(f28b_summary.get("seed_surface_rows", -1)) == 0
        and int(f28b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f28c_parent_matches": f28c_summary.get("run_id") == f28c.RUN_ID,
        "f28c_next_closeout_matches": f28c_summary.get("next_run_id") == RUN_ID,
        "f28c_preserved_clue_matches": f28c_summary.get("preserved_clue") == PRESERVED_CLUE,
        "f28c_negative_memory_matches": f28c_summary.get("negative_memory") == NEGATIVE_MEMORY,
        "f28c_valid_repair_zero": int(f28c_summary.get("diagnosis", {}).get("valid_train_chunk_repair_opportunity_rows", -1)) == 0,
        "candidate_summary_present": not candidate_summary.empty and len(candidate_summary) == 234,
        "chunk_metrics_present": not chunk_metrics.empty and len(chunk_metrics) == 234 * 4,
        "repair_audit_present": not repair_audit.empty,
        "grok_closeout_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_closeout_accepted": grok["accepted"],
        "grok_stage_open_packet_present": path_exists(GROK_STAGE_OPEN_PACKET / "metadata.json"),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    f28b_summary: dict[str, Any],
    f28c_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    chunk_metrics: pd.DataFrame,
    repair_audit: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_ready(마감 준비 통과)":
        raise RuntimeError(f"Frontier28D closeout local checks failed: {json.dumps(local, ensure_ascii=False)}")
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "repair_decision": REPAIR_DECISION,
        "runtime_probe_blocker": RUNTIME_PROBE_BLOCKER,
        "onnx_blocker": ONNX_BLOCKER,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("retry", {}).get("classification", ""),
        },
        "f28b_summary": {
            "status": f28b_summary.get("status"),
            "judgment": f28b_summary.get("judgment"),
            "reference_union_rows": f28b_summary.get("reference_union_rows"),
            "stability_candidate_rows": f28b_summary.get("stability_candidate_rows"),
            "density_bridge_rows": f28b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f28b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f28b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f28b_summary.get("handoff_candidate_rows"),
            "best_stability_union_id": f28b_summary.get("best_stability_union_id"),
            "best_forward_readonly_union_id": f28b_summary.get("best_forward_readonly_union_id"),
            "best_stability_union": f28b_summary.get("best_stability_union", {}),
            "best_forward_readonly_union": f28b_summary.get("best_forward_readonly_union", {}),
        },
        "f28c_summary": {
            "status": f28c_summary.get("status"),
            "judgment": f28c_summary.get("judgment"),
            "repair_decision": f28c_summary.get("repair_decision"),
            "preserved_clue": f28c_summary.get("preserved_clue"),
            "negative_memory": f28c_summary.get("negative_memory"),
            "diagnosis": f28c_summary.get("diagnosis", {}),
        },
        "candidate_summary_rows": int(len(candidate_summary)),
        "chunk_metric_rows": int(len(chunk_metrics)),
        "repair_audit_rows": int(len(repair_audit)),
        "grok_closeout": grok,
        "local_verification": local,
        "result_boundary": "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_runtime_authority(단계 마감 보존 단서+부정 기억, WFO/MT5/런타임 권위 없음)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "final_closeout_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt(final))
    f03b.write_text_sig(LOCAL_VERIFICATION_PATH, local_verification_text(final))
    f03b.write_text_sig(REQUIRED_GATE_AUDIT_PATH, required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(DECISION_PATH, decision_text(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F28A_SUMMARY,
        F28B_SUMMARY,
        F28B_CANDIDATE_SUMMARY,
        F28B_CHUNK_METRICS,
        F28C_SUMMARY,
        F28C_REPAIR_AUDIT,
        GROK_STAGE_OPEN_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        GROK_RECEIPT_PATH,
        REPORT_PATH,
        REQUIRED_GATE_AUDIT_PATH,
        STAGE_ROOT / "04_selected" / "preserved_clue.md",
        STAGE_ROOT / "04_selected" / "negative_memory.md",
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "closeout": {
            "status": final["status"],
            "judgment": final["judgment"],
            "preserved_clue": final["preserved_clue"],
            "negative_memory": final["negative_memory"],
            "runtime_probe_blocker": final["runtime_probe_blocker"],
            "onnx_blocker": final["onnx_blocker"],
        },
        "grok": {
            "stage_open_packet": GROK_STAGE_OPEN_PACKET.as_posix(),
            "stage_closeout_packet": GROK_CLOSEOUT_PACKET.as_posix(),
            "closeout_classification": final["grok_closeout"]["classification"],
        },
        "compatibility": {"schema_version": "frontier28d_stage_closeout_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any]) -> str:
    f28b_summary = final["f28b_summary"]
    best = f28b_summary.get("best_stability_union", {})
    forward = f28b_summary.get("best_forward_readonly_union", {})
    diagnosis = final["f28c_summary"].get("diagnosis", {})
    return f"""# Frontier28D Stage Closeout Report(전선28D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F28(전선28) train-only stability gap penalty(학습 전용 안정성 격차 페널티) 가설을 preserved clue + negative memory(보존 단서 + 부정 기억)로 closeout(마감)했습니다.

Effect(효과): stability ranking(안정성 순위)이 표면을 재정렬했지만 seed/handoff(씨앗/인계)를 만들지 못했다는 경계를 기록하고, MT5/ONNX/WFO(메타트레이더5/온엑스/워크포워드 최적화)를 열지 않습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

F28B reference/stability/density/scout/seed/handoff(전선28B 참조/안정성/빈도/탐색/씨앗/인계): `{f28b_summary['reference_union_rows']}` / `{f28b_summary['stability_candidate_rows']}` / `{f28b_summary['density_bridge_rows']}` / `{f28b_summary['scout_clue_rows']}` / `{f28b_summary['seed_surface_rows']}` / `{f28b_summary['handoff_candidate_rows']}`

Best stability union(최상 안정성 합집합): `{f28b_summary['best_stability_union_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Best forward read-only union(최상 전진 읽기 전용 합집합): `{f28b_summary['best_forward_readonly_union_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(forward.get('validation_profit_factor'))}/{fmt(forward.get('validation_trades_per_day'))}/{fmt(forward.get('validation_dd_risk'))}` and `{fmt(forward.get('oos_profit_factor'))}/{fmt(forward.get('oos_trades_per_day'))}/{fmt(forward.get('oos_dd_risk'))}`.

F28C repair audit(전선28C 수리 감사): near_seed_under_dd_rows(손실폭 충족 근접 씨앗 행) `{diagnosis.get('near_seed_under_dd_rows')}`, pf_ready_dd_blocked_rows(PF 준비/손실폭 차단 행) `{diagnosis.get('pf_ready_dd_blocked_rows')}`, valid_train_chunk_repair_opportunity_rows(유효 학습 조각 수리 기회 행) `{diagnosis.get('valid_train_chunk_repair_opportunity_rows')}`.

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier28D Grok Closeout Receipt(전선28D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout(단계 마감)은 Grok review(그록 검토)가 필요합니다.

Packet(묶음): `{grok['packet']}`

Prompt(프롬프트): `{grok['prompt']}`

Clean output(정리 출력): `{grok['clean_output']}`

Metadata(메타데이터): `{grok['metadata']}`

Prompt hash(프롬프트 해시): `{grok['prompt_hash']}`

Transport success(전송 성공): `{grok['success']}`, returncode(반환 코드) `{grok['returncode']}`, timed_out(시간 초과) `{grok['timed_out']}`

Codex classification(Codex 분류): `{grok['classification']}`

Accepted advice(수용 조언): closeout class(마감 분류), repair rejection(수리 거절), runtime probe ineligible(런타임 탐침 부적격), ONNX unattempted(온엑스 미시도), and next clue(다음 단서)를 수용했습니다.

Needs local verification(로컬 검증 필요): F28D materialization(전선28D 물질화), receipt/gate audit(영수증/게이트 감사), commit/push(커밋/푸시)는 Codex가 로컬에서 확인합니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in final["local_verification"]["checks"].items()]
    return f"""# Frontier28D Local Verification(전선28D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 조언을 자동 실행하지 않고 local files/registers/artifacts(로컬 파일/등록부/산출물)로 재검증한 뒤 closeout(마감)했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    f28b_summary = final["f28b_summary"]
    diagnosis = final["f28c_summary"].get("diagnosis", {})
    return f"""# Frontier28 Required Gate Coverage Audit(전선28 필수 게이트 커버리지 감사)

- stage_open_grok_gate(단계 개방 그록 게이트): `{GROK_STAGE_OPEN_PACKET.as_posix()}` recorded(기록)
- proxy_gate(프록시 게이트): `{f28b.RUN_ID}` produced reference/stability/scout/seed/handoff(참조/안정성/탐색/씨앗/인계) `{f28b_summary['reference_union_rows']}/{f28b_summary['stability_candidate_rows']}/{f28b_summary['scout_clue_rows']}/{f28b_summary['seed_surface_rows']}/{f28b_summary['handoff_candidate_rows']}`
- repair_decision_gate(수리 결정 게이트): `{f28c.RUN_ID}` recorded valid_train_chunk_repair_opportunity_rows(유효 학습 조각 수리 기회 행) `{diagnosis.get('valid_train_chunk_repair_opportunity_rows')}`
- stage_closeout_grok_gate(단계 마감 그록 게이트): `{GROK_CLOSEOUT_PACKET.as_posix()}` classification(분류) `{final['grok_closeout']['classification']}`
- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_blocker']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B(티어 A/B/A+B) rows(행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    f28b_summary = final["f28b_summary"]
    return f"""# Frontier28 Preserved Clue(전선28 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F28B(전선28B)는 `{f28b_summary['reference_union_rows']}` reference union rows(참조 합집합 행)을 train-only chunk stability rank(학습 전용 조각 안정성 순위)로 재정렬했고 `{f28b_summary['scout_clue_rows']}` scout rows(탐색 행)를 보존했습니다.

Use boundary(사용 경계): reference only(참조 전용). This is not baseline/promotion/runtime authority(기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    f28b_summary = final["f28b_summary"]
    diagnosis = final["f28c_summary"].get("diagnosis", {})
    return f"""# Frontier28 Negative Memory(전선28 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): locked train chunk stability rank(잠금 학습 조각 안정성 순위)는 scout rows(탐색 행) `{f28b_summary['scout_clue_rows']}`개를 유지했지만 seed/handoff(씨앗/인계)는 `{f28b_summary['seed_surface_rows']}` / `{f28b_summary['handoff_candidate_rows']}`개로 남았습니다.

Repair result(수리 결과): valid_train_chunk_repair_opportunity_rows(유효 학습 조각 수리 기회 행) `{diagnosis.get('valid_train_chunk_repair_opportunity_rows')}`.

Do not repeat(반복 금지): same stability rank weight/threshold tweak(같은 안정성 순위 가중치/임계값 미세 조정)를 seed/handoff(씨앗/인계) 해결책처럼 반복하지 않습니다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier28 Selection Status(전선28 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier28 Stability Gap Scout(전선28 안정성 격차 탐색 마감)

Date(날짜): 2026-06-14

Decision(결정): Close(마감) `{STAGE_ID}` as preserved_clue_negative_memory(보존 단서+부정 기억).

Effect(효과): train-only stability ranking(학습 전용 안정성 순위)은 보존하지만 seed/handoff failure(씨앗/인계 실패)는 반복 금지 기억으로 남기고, 다음 frontier(전선)를 새 손실 집중 차단 가설로 시작합니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`

Next run(다음 실행): `{final['next_run_id']}`
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    f28b_summary = final["f28b_summary"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "family": "publish_handoff(게시/인계)",
        "work_family": "publish_handoff(게시/인계)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"preserved={final['preserved_clue']};negative={final['negative_memory']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"candidate={f28b_summary['stability_candidate_rows']};scout={f28b_summary['scout_clue_rows']};seed={f28b_summary['seed_surface_rows']};handoff={f28b_summary['handoff_candidate_rows']}",
        "guardrail_kpi": "closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_authority(마감 보존 단서+부정 기억, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_blocker"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    f28b_summary = final["f28b_summary"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stage_closeout_preserved_clue_negative_memory_not_runtime(단계 마감 보존 단서+부정 기억, 런타임 아님)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"candidate={f28b_summary['stability_candidate_rows']};scout={f28b_summary['scout_clue_rows']};seed={f28b_summary['seed_surface_rows']};handoff={f28b_summary['handoff_candidate_rows']}",
        "guardrail_kpi": "no_wfo_no_mt5_no_runtime_authority(WFO/MT5/런타임 권위 없음)",
        "external_verification_status": final["runtime_probe_blocker"],
        "notes": f"{final['preserved_clue']};{final['negative_memory']};{final['onnx_blocker']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }
    tier_b = {
        **primary,
        "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
        "subrun_id": f"{RUN_ID}__tier_b_missing_required",
        "record_view": "Tier B separate(티어 B 분리)",
        "tier_scope": "Tier B(티어 B)",
        "kpi_scope": "missing_required(필수 누락)",
        "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)",
        "guardrail_kpi": "no_tier_b_claim(티어 B 주장 없음)",
        "external_verification_status": "not_applicable_stage_closeout_no_mt5(단계 마감이라 MT5 없음)",
        "notes": "Tier B source absent(티어 B 원천 없음)",
    }
    combined = {
        **primary,
        "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "record_view": "Tier A+B combined(티어 A+B 합산)",
        "tier_scope": "Tier A+B(티어 A+B)",
        "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
        "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)",
        "guardrail_kpi": "no_synthetic_combined_claim(합성 합산 주장 없음)",
        "external_verification_status": "not_applicable_stage_closeout_no_mt5(단계 마감이라 MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier28(전선28 마감). "
        f"Effect(효과): preserved clue(보존 단서) `{final['preserved_clue']}` and negative memory(부정 기억) `{final['negative_memory']}` recorded; next run(다음 실행) `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR28-TRAIN-ONLY-STABILITY-GAP-PENALTY-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` closed as preserved_clue_negative_memory(보존 단서+부정 기억). "
        f"Effect(효과): stability gap rank(안정성 격차 순위)는 참조 단서로 보존하지만 seed/handoff(씨앗/인계) 없음으로 MT5/ONNX(메타트레이더5/온엑스)는 열지 않습니다; next clue(다음 단서) `{final['next_hypothesis_clue']}`.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: `{final['negative_memory']}`. Preserved clue(보존 단서): `{final['preserved_clue']}`. "
        f"Runtime blocker(런타임 차단): `{final['runtime_probe_blocker']}`. ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`. "
        "Effect(효과): 다음 전선은 stability rank tweak(안정성 순위 미세 조정)을 반복하지 않고 train-only loss concentration veto(학습 전용 손실 집중 차단)를 새 가설로 엽니다.\n"
    )


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {final['status']}",
        f"current_judgment: {final['judgment']}",
        f"next_stage_id: {final['next_stage_id']}",
        f"next_run_id: {final['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def current_working_state(final: dict[str, Any]) -> str:
    f28b_summary = final["f28b_summary"]
    diagnosis = final["f28c_summary"].get("diagnosis", {})
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next stage(다음 단계): `{final['next_stage_id']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F28(전선28) train-only stability gap rank(학습 전용 안정성 격차 순위) 가설을 preserved clue + negative memory(보존 단서+부정 기억)로 closeout(마감)했습니다.

Effect(효과): candidate/scout/seed/handoff(후보/탐색/씨앗/인계) `{f28b_summary['stability_candidate_rows']}/{f28b_summary['scout_clue_rows']}/{f28b_summary['seed_surface_rows']}/{f28b_summary['handoff_candidate_rows']}`와 valid train repair(유효 학습 수리) `{diagnosis.get('valid_train_chunk_repair_opportunity_rows')}`를 근거로 다음 전선을 새 가설로 넘깁니다.

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_probe_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "pending_or_missing(대기 또는 누락)"}


def sha256_io(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
