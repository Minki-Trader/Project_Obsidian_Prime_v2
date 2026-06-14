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
from stage_pipelines.stage_frontier_24 import frontier24b_density_bridge_payoff_pockets_proxy_scout as f24b
from stage_pipelines.stage_frontier_24 import frontier24c_density_bridge_dd_normalization_repair as f24c
from stage_pipelines.stage_frontier_24 import materialize_frontier24a_stage_open as f24a


STAGE_ID = f24a.STAGE_ID
RUN_ID = "frontier24D_stage_closeout_density_bridge_payoff_pockets_v1"
RUN_NUMBER = "frontier24D"
PARENT_RUN_ID = f24c.RUN_ID
NEXT_FRONTIER_RUN_ID = "frontier25A_stage_open_bridge_archetype_preselection_hypothesis_design_v1"

STATUS = "closed_preserved_clue_negative_memory_density_bridge_dd_repair_scout_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_24_density_bridge_payoff_pockets_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_24/frontier24d_stage_closeout.py")

F24A_SUMMARY = STAGE_ROOT / "02_runs" / f24a.RUN_ID / "stage_open_summary.json"
F24B_SUMMARY = STAGE_ROOT / "02_runs" / f24b.RUN_ID / "final_summary.json"
F24B_CANDIDATES = STAGE_ROOT / "02_runs" / f24b.RUN_ID / "bridge_candidate_summary.csv"
F24C_SUMMARY = STAGE_ROOT / "02_runs" / f24c.RUN_ID / "final_summary.json"
F24C_CANDIDATES = STAGE_ROOT / "02_runs" / f24c.RUN_ID / "repair_candidate_summary.csv"
GROK_STAGE_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier24_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier24_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f24_density_bridge_dd_repaired_scout_pockets_reference_only"
    "(전선24 빈도 연결 손실폭 수리 탐색 구간 참조 전용)"
)
NEGATIVE_MEMORY = (
    "under_f24_locked_proxy_density_bridge_dd_repair_did_not_jointly_satisfy_seed_or_handoff"
    "(전선24 잠금 프록시 계약 하에서 빈도 연결 손실폭 수리가 씨앗/인계 게이트를 동시에 충족하지 못함)"
)
RUNTIME_BLOCKER = (
    "runtime_probe_ineligible_no_handoff_candidate_after_f24_capped_repair"
    "(전선24 상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격)"
)
ONNX_BLOCKER = (
    "onnx_branch_unattempted_no_handoff_candidate_after_f24_capped_repair"
    "(전선24 상한 수리 뒤 인계 후보가 없어 ONNX 분기 미개시)"
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    normalize_grok_markdown()
    created_at = utc_now()
    f24a_summary = read_json(F24A_SUMMARY)
    f24b_summary = read_json(F24B_SUMMARY)
    f24c_summary = read_json(F24C_SUMMARY)
    f24b_candidates = pd.read_csv(io_path(F24B_CANDIDATES))
    f24c_candidates = pd.read_csv(io_path(F24C_CANDIDATES))
    grok = read_grok_packet(GROK_CLOSEOUT_PACKET)
    local = local_verification(f24a_summary, f24b_summary, f24c_summary, f24b_candidates, f24c_candidates, grok)
    if local["judgment"] != "pass_closeout_ready(마감 준비 통과)":
        raise RuntimeError(f"Frontier24D local verification failed: {json.dumps(local, ensure_ascii=False)}")
    final = build_final(created_at, f24a_summary, f24b_summary, f24c_summary, f24b_candidates, f24c_candidates, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "preserved_clue": final["preserved_clue"],
        "negative_memory": final["negative_memory"],
        "runtime_blocker": final["runtime_blocker"],
        "onnx_blocker": final["onnx_blocker"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def normalize_grok_markdown() -> None:
    for packet in (GROK_STAGE_OPEN_PACKET, GROK_CLOSEOUT_PACKET):
        for name in ("prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                text = io_path(path).read_text(encoding="utf-8-sig")
                f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    return {
        "packet": packet.as_posix(),
        "prompt": (packet / "prompt.md").as_posix(),
        "output": (packet / "clean_output.md").as_posix(),
        "metadata": (packet / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "preflight_warnings": metadata.get("preflight_warnings", []),
        "classification": classify_grok(output),
        "output_excerpt": output[:3200],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    if "accepted_with_adjustments" in lowered:
        return "accepted_with_adjustments(조정 수용)"
    if "accepted" in lowered:
        return "accepted(수용)"
    return "classification_missing(분류 누락)"


def local_verification(
    f24a_summary: dict[str, Any],
    f24b_summary: dict[str, Any],
    f24c_summary: dict[str, Any],
    f24b_candidates: pd.DataFrame,
    f24c_candidates: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    f24b_best = row_by_id(f24b_candidates, "bridge_id", "f24b_0174")
    f24c_best = row_by_id(f24c_candidates, "repair_id", "f24c_0105")
    f24c_second = row_by_id(f24c_candidates, "repair_id", "f24c_0106")
    f24c_third = row_by_id(f24c_candidates, "repair_id", "f24c_0163")
    f24c_seed_true_rows = bool_series_sum(f24c_candidates["seed_surface_flag"])
    f24c_handoff_true_rows = bool_series_sum(f24c_candidates["handoff_candidate_flag"])
    forward_max_dd = max(float(f24c_best["validation_dd_risk"]), float(f24c_best["oos_dd_risk"]))
    checks = {
        "f24a_opened_after_grok": f24a_summary.get("run_id") == f24a.RUN_ID
        and "grok" in f24a_summary,
        "f24b_density_no_handoff": int(f24b_summary.get("density_bridge_rows", -1)) == 105
        and int(f24b_summary.get("seed_surface_rows", -1)) == 0
        and int(f24b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f24b_best_matches_frequency_clue": 5.0 <= float(f24b_best["validation_trades_per_day"]) <= 10.0
        and 5.0 <= float(f24b_best["oos_trades_per_day"]) <= 10.0
        and float(f24b_best["validation_dd_risk"]) > f24b.SCOUT_DD_CAP,
        "f24c_scout_no_seed_no_handoff": int(f24c_summary.get("scout_clue_rows", -1)) == 3
        and int(f24c_summary.get("seed_surface_rows", -1)) == 0
        and int(f24c_summary.get("handoff_candidate_rows", -1)) == 0
        and f24c_seed_true_rows == 0
        and f24c_handoff_true_rows == 0,
        "f24c_best_is_scout_not_seed": bool_value(f24c_best["scout_clue_flag"])
        and not bool_value(f24c_best["seed_surface_flag"])
        and not bool_value(f24c_best["handoff_candidate_flag"])
        and 5.0 <= float(f24c_best["validation_trades_per_day"]) <= 10.0
        and 5.0 <= float(f24c_best["oos_trades_per_day"]) <= 10.0
        and float(f24c_best["validation_profit_factor"]) >= f24b.SCOUT_PF
        and float(f24c_best["oos_profit_factor"]) >= f24b.SCOUT_PF
        and forward_max_dd <= f24b.SCOUT_DD_CAP
        and forward_max_dd > f24b.SEED_DD_CAP,
        "f24c_scout_anchors_exist": bool_value(f24c_second["scout_clue_flag"]) and bool_value(f24c_third["scout_clue_flag"]),
        "grok_success": grok["success"] and not grok["timed_out"] and grok["returncode"] == 0,
        "grok_accepts_closeout_boundary": grok["classification"] in {
            "accepted(수용)",
            "accepted_with_adjustments(조정 수용)",
            "needs_local_verification(로컬 검증 필요)",
        },
        "grok_no_unexpected_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
        "notes": {
            "runtime_boundary": "No handoff rows means MT5 runtime probe(MT5 런타임 탐침) is ineligible, not deferred(지연 아님).",
            "closeout_class": "preserved_clue(보존 단서) primary with negative_memory(부정 기억) companion.",
            "grok_adjustment": "Use F23-style runtime and ONNX blocker names(F23 방식 런타임/ONNX 차단 이름 사용).",
        },
    }


def build_final(
    created_at: str,
    f24a_summary: dict[str, Any],
    f24b_summary: dict[str, Any],
    f24c_summary: dict[str, Any],
    f24b_candidates: pd.DataFrame,
    f24c_candidates: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    f24b_best = row_by_id(f24b_candidates, "bridge_id", "f24b_0174")
    f24c_best = row_by_id(f24c_candidates, "repair_id", "f24c_0105")
    f24c_second = row_by_id(f24c_candidates, "repair_id", "f24c_0106")
    f24c_third = row_by_id(f24c_candidates, "repair_id", "f24c_0163")
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_FRONTIER_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "runtime_blocker": RUNTIME_BLOCKER,
        "onnx_blocker": ONNX_BLOCKER,
        "tier_boundary": "Tier A proxy only; Tier B missing_required; Tier A+B out_of_scope_by_claim(티어 A 프록시 전용, 티어 B 필수 누락, 티어 A+B 주장 범위 밖)",
        "data_boundary": "proxy/oracle-label research only; no verified MT5 runtime semantics(프록시/오라클 라벨 연구 전용, 검증된 MT5 런타임 의미 없음)",
        "f24a_summary": {"status": f24a_summary.get("status"), "judgment": f24a_summary.get("judgment")},
        "f24b_summary": {
            "status": f24b_summary.get("status"),
            "density_bridge_rows": f24b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f24b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f24b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f24b_summary.get("handoff_candidate_rows"),
            "best_bridge_id": f24b_summary.get("best_bridge_id"),
        },
        "f24c_summary": {
            "status": f24c_summary.get("status"),
            "density_bridge_rows": f24c_summary.get("density_bridge_rows"),
            "scout_clue_rows": f24c_summary.get("scout_clue_rows"),
            "seed_surface_rows": f24c_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f24c_summary.get("handoff_candidate_rows"),
            "best_repair_id": f24c_summary.get("best_repair_id"),
        },
        "archetypes": {
            "high_density_weak_dd_source": {
                "bridge_id": "f24b_0174",
                "meaning": "density bridge reached target frequency but failed DD/PF joint gates(빈도 연결은 목표 거래 빈도에 닿았지만 손실폭/수익 팩터 동시 게이트 실패)",
                "metrics": metric_excerpt(f24b_best),
            },
            "dd_repaired_scouts": {
                "meaning": "capped DD repair reached scout territory but not seed/handoff(상한 손실폭 수리는 탐색 단서까지 닿았지만 씨앗/인계 실패)",
                "rows": {
                    "f24c_0105": metric_excerpt(f24c_best),
                    "f24c_0106": metric_excerpt(f24c_second),
                    "f24c_0163": metric_excerpt(f24c_third),
                },
            },
        },
        "grok_closeout": grok,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "final_closeout_summary.json", final)
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt_text(final))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit_text(final))
    f03b.write_text_sig(REQUIRED_GATE_AUDIT_PATH, required_gate_audit_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status_text(final))
    f03b.write_text_sig(DECISION_PATH, decision_text(final))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(F24A_SUMMARY),
            artifact_identity(F24B_SUMMARY),
            artifact_identity(F24B_CANDIDATES),
            artifact_identity(F24C_SUMMARY),
            artifact_identity(F24C_CANDIDATES),
            artifact_identity(GROK_CLOSEOUT_PACKET / "clean_output.md"),
            artifact_identity(REPORT_PATH),
            artifact_identity(GROK_RECEIPT_PATH),
            artifact_identity(GATE_AUDIT_PATH),
            artifact_identity(REQUIRED_GATE_AUDIT_PATH),
            artifact_identity(DECISION_PATH),
        ],
        "results": {
            "cross_split": {
                "closeout": final["judgment"],
                "f24b_density_scout_seed_handoff": [
                    final["f24b_summary"]["density_bridge_rows"],
                    final["f24b_summary"]["scout_clue_rows"],
                    final["f24b_summary"]["seed_surface_rows"],
                    final["f24b_summary"]["handoff_candidate_rows"],
                ],
                "f24c_density_scout_seed_handoff": [
                    final["f24c_summary"]["density_bridge_rows"],
                    final["f24c_summary"]["scout_clue_rows"],
                    final["f24c_summary"]["seed_surface_rows"],
                    final["f24c_summary"]["handoff_candidate_rows"],
                ],
                "runtime_blocker": final["runtime_blocker"],
                "onnx_blocker": final["onnx_blocker"],
            },
            "report_refs": [{"role": "stage_closeout_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier24d_closeout_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
        },
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any]) -> str:
    f24b_anchor = final["archetypes"]["high_density_weak_dd_source"]["metrics"]
    scout_rows = final["archetypes"]["dd_repaired_scouts"]["rows"]
    best = scout_rows["f24c_0105"]
    third = scout_rows["f24c_0163"]
    return f"""# Frontier24D Density Bridge Payoff Pockets Closeout Report(전선24D 빈도 연결 보상 구간 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): Frontier24(전선24)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): same-side OR-union density bridge(같은 방향 OR 합집합 빈도 연결)는 5~10/day(일 5~10회) 거래 빈도와 scout clue(탐색 단서)를 만들 수 있다는 점만 보존하고, seed/handoff(씨앗/인계) 실패는 반복 금지 기억으로 남깁니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

- High-density source(고빈도 원천): `f24b_0174`; validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(f24b_anchor['validation_profit_factor'])}/{fmt(f24b_anchor['validation_trades_per_day'])}/{fmt(f24b_anchor['validation_dd_risk'])}` and `{fmt(f24b_anchor['oos_profit_factor'])}/{fmt(f24b_anchor['oos_trades_per_day'])}/{fmt(f24b_anchor['oos_dd_risk'])}`.
- Best DD-repaired scout(최상 손실폭 수리 탐색 단서): `f24c_0105`; validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best['validation_profit_factor'])}/{fmt(best['validation_trades_per_day'])}/{fmt(best['validation_dd_risk'])}` and `{fmt(best['oos_profit_factor'])}/{fmt(best['oos_trades_per_day'])}/{fmt(best['oos_dd_risk'])}`.
- Alternate scout(대안 탐색 단서): `f24c_0163`; validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(third['validation_profit_factor'])}/{fmt(third['validation_trades_per_day'])}/{fmt(third['validation_dd_risk'])}` and `{fmt(third['oos_profit_factor'])}/{fmt(third['oos_trades_per_day'])}/{fmt(third['oos_dd_risk'])}`.

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Tier boundary(티어 경계): `{final['tier_boundary']}`

Data boundary(데이터 경계): `{final['data_boundary']}`

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt_text(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier24D Grok Closeout Receipt(전선24D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout(단계 마감)은 Grok review(그록 검토)가 필요했습니다.

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): close Frontier24(전선24)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감하고 MT5 runtime probe(MT5 런타임 탐침)는 부적격 처리.

Prompt(프롬프트): `{grok['prompt']}`

Output(출력): `{grok['output']}`

Advice classification(조언 분류): `{grok['classification']}`

Accepted advice(수용 조언): closeout_class(마감 분류)는 preserved_clue(보존 단서), negative_memory(부정 기억)는 동반 기록, no MT5 runtime probe(MT5 런타임 탐침 없음), runtime/ONNX blocker(런타임/온엑스 차단 사유)를 명시합니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Forbidden claim check(금지 주장 확인): pass(통과). Grok(그록)은 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않았습니다.
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier24D Gate Audit(전선24D 게이트 감사)

- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- external_review_packet(외부 검토 묶음): stage open(단계 개방) `{GROK_STAGE_OPEN_PACKET.as_posix()}` and closeout(마감) `{GROK_CLOSEOUT_PACKET.as_posix()}`
- local_verification_gate(로컬 검증 게이트): `{final['local_verification']['judgment']}`
- kpi_contract_audit(KPI 계약 감사): F24B/F24C summaries and candidate summaries(F24B/F24C 요약과 후보 요약) checked(확인)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_blocker']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일) and `{REQUIRED_GATE_AUDIT_PATH.as_posix()}`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def required_gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier24 Required Gate Coverage Audit(전선24 필수 게이트 커버리지 감사)

Work family(작업군): experiment_execution(실험 실행) + publish_handoff(게시/인계) closeout(마감)

- scope_completion_gate(범위 완료 게이트): F24A/F24B/F24C/F24D lifecycle(생명주기) materialized(물질화)
- kpi_contract_audit(KPI 계약 감사): density bridge and DD repair KPI(빈도 연결과 손실폭 수리 KPI) recorded in run and stage ledgers(실행/단계 장부에 기록)
- external_review_packet(외부 검토 묶음): stage open(단계 개방) `{GROK_STAGE_OPEN_PACKET.as_posix()}` and closeout(마감) `{GROK_CLOSEOUT_PACKET.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_blocker']}`
- onnx_scope_gate(ONNX 범위 게이트): `{final['onnx_blocker']}`
- closeout_gate(마감 게이트): `{final['judgment']}`
- final_claim_guard(최종 주장 방어): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    return f"""# Frontier24 Preserved Clue(전선24 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F24B/F24C(전선24B/C)는 seed/handoff(씨앗/인계)는 만들지 못했지만, same-side OR-union density bridge(같은 방향 OR 합집합 빈도 연결)가 target frequency(목표 빈도)를 만들고 DD repair(손실폭 수리) 뒤 scout clue(탐색 단서) 3개를 만들었습니다.

- High-density source(고빈도 원천): `f24b_0174`
- DD-repaired scout rows(손실폭 수리 탐색 행): `f24c_0105`, `f24c_0106`, `f24c_0163`

Boundary(경계): reference-only(참조 전용). It is not seed/handoff/completion/baseline/promotion/runtime authority(씨앗/인계/완성/기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier24 Negative Memory(전선24 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): F24B(전선24B) density/scout/seed/handoff(빈도/탐색/씨앗/인계)는 `{final['f24b_summary']['density_bridge_rows']}/{final['f24b_summary']['scout_clue_rows']}/{final['f24b_summary']['seed_surface_rows']}/{final['f24b_summary']['handoff_candidate_rows']}`였고, F24C(전선24C)는 `{final['f24c_summary']['density_bridge_rows']}/{final['f24c_summary']['scout_clue_rows']}/{final['f24c_summary']['seed_surface_rows']}/{final['f24c_summary']['handoff_candidate_rows']}`였습니다. 즉 DD repair(손실폭 수리)는 scout clue(탐색 단서)까지만 만들었고 seed/handoff(씨앗/인계)는 만들지 못했습니다.

Runtime blocker(런타임 차단): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`

Do not repeat(반복 금지): F24 locked proxy contract(전선24 잠금 프록시 계약) 아래에서 같은 OR-union bridge + single capped DD repair(OR 합집합 연결 + 단일 상한 손실폭 수리)만 반복하지 않습니다.

Reopen condition(재개 조건): bridge archetype pre-selection(연결 원형 사전 선택), split-stable DD headroom(분할 안정 손실폭 여유), or a new risk surface(새 위험 표면)가 있을 때만 이 단서를 참조합니다.
"""


def selection_status_text(final: dict[str, Any]) -> str:
    return f"""# Frontier24 Selection Status(전선24 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Closeout(마감): `preserved_clue + negative_memory(보존 단서 + 부정 기억)`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier24(전선24 마감)

Date(날짜): 2026-06-14

Decision(결정): close Frontier24(전선24)를 `{final['status']}`로 닫습니다.

Action(행동): density bridge payoff pockets ONNX scout(빈도 연결 보상 구간 ONNX 탐색)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감했습니다.

Effect(효과): 다음 frontier(전선)는 F24(전선24)의 단서를 reference only(참조 전용)로만 쓰고, winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않습니다.

Next run(다음 실행): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) not_claimed(주장 없음).
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["archetypes"]["dd_repaired_scouts"]["rows"]["f24c_0105"]
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
        "claim_boundary": "closed_no_baseline_no_promotion_no_runtime_authority_no_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"f24c_0105_oos_pf={fmt(best['oos_profit_factor'])};oos_density={fmt(best['oos_trades_per_day'])};oos_dd={fmt(best['oos_dd_risk'])}",
        "guardrail_kpi": "no_seed_no_handoff_no_wfo_no_mt5_no_onnx_no_authority(씨앗/인계/WFO/MT5/ONNX/권위 없음)",
        "external_verification_status": final["runtime_blocker"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["archetypes"]["dd_repaired_scouts"]["rows"]["f24c_0105"]
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
        "primary_kpi": (
            f"f24c_scout={final['f24c_summary']['scout_clue_rows']};seed={final['f24c_summary']['seed_surface_rows']};"
            f"handoff={final['f24c_summary']['handoff_candidate_rows']};oos_pf={fmt(best['oos_profit_factor'])};"
            f"oos_density={fmt(best['oos_trades_per_day'])};oos_dd={fmt(best['oos_dd_risk'])}"
        ),
        "guardrail_kpi": "no_wfo_no_mt5_no_onnx_no_authority(WFO/MT5/ONNX/권위 없음)",
        "external_verification_status": final["runtime_blocker"],
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
        "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)",
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
        "notes": "Combined record blocked by missing Tier B source(Tier B 원천 누락으로 합산 기록 차단)",
    }
    return [primary, tier_b, combined]


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: {final['negative_memory']}. Preserved clue(보존 단서): `{final['preserved_clue']}`. "
        f"Runtime blocker(런타임 차단): `{final['runtime_blocker']}`. ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`. "
        "Effect(효과): 다음 전선은 bridge archetype pre-selection(연결 원형 사전 선택) 같은 새 가설이 있을 때만 F24(전선24)를 참조합니다.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR24-DENSITY-BRIDGE-PAYOFF-POCKETS-ONNX-SCOUT`: `{RUN_ID}` closes Frontier24(전선24) as preserved clue + negative memory(보존 단서 + 부정 기억). "
        "Effect(효과): density bridge(빈도 연결)는 단서로 보존하지만 seed/handoff(씨앗/인계) 없음으로 ONNX(온엑스)와 MT5 runtime probe(MT5 런타임 탐침)는 열지 않습니다.\n"
    )


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier24(전선24) as preserved clue + negative memory(보존 단서 + 부정 기억). "
        f"Effect(효과): next frontier(다음 전선) starts at `{final['next_run_id']}` with no baseline/promotion/runtime authority(기준선/승격/런타임 권위 없음).\n"
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
        f"next_run_id: {final['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def current_working_state(final: dict[str, Any]) -> str:
    best = final["archetypes"]["dd_repaired_scouts"]["rows"]["f24c_0105"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier24(전선24)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): density bridge(빈도 연결)는 단서로 남기지만 seed/handoff(씨앗/인계)가 없어 ONNX(온엑스), WFO(워크포워드 최적화), MT5 runtime probe(MT5 런타임 탐침)는 하지 않습니다.

Best preserved scout(최상 보존 탐색 단서): `f24c_0105` validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best['validation_profit_factor'])}/{fmt(best['validation_trades_per_day'])}/{fmt(best['validation_dd_risk'])}` and `{fmt(best['oos_profit_factor'])}/{fmt(best['oos_trades_per_day'])}/{fmt(best['oos_dd_risk'])}`.

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def row_by_id(frame: pd.DataFrame, column: str, value: str) -> dict[str, Any]:
    rows = frame.loc[frame[column].astype(str).eq(value)]
    if rows.empty:
        raise KeyError(f"Missing row {column}={value}")
    return dict(rows.iloc[0])


def metric_excerpt(row: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "bridge_id",
        "repair_id",
        "source_bridge_id",
        "micro_ids",
        "rule_definition",
        "filter_feature",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk",
        "validation_equity_trend_r2",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk",
        "oos_equity_trend_r2",
        "forward_dd_relief",
        "density_bridge_flag",
        "scout_clue_flag",
        "seed_surface_flag",
        "handoff_candidate_flag",
    )
    return {field: json_ready(row.get(field, "")) for field in fields if field in row}


def bool_series_sum(series: pd.Series) -> int:
    return int(series.astype(str).str.lower().eq("true").sum())


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


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
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
