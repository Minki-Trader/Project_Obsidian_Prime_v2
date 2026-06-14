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
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_23 import frontier23c_payoff_asymmetry_entry_filter_repair as f23c


STAGE_ID = f23b.STAGE_ID
RUN_ID = "frontier23D_stage_closeout_payoff_asymmetry_pf_source_v1"
RUN_NUMBER = "frontier23D"
PARENT_RUN_ID = f23c.RUN_ID
NEXT_FRONTIER_RUN_ID = "frontier24A_stage_open_density_bridge_payoff_pockets_hypothesis_design_v1"

STATUS = "closed_preserved_clue_negative_memory_payoff_asymmetry_pf_lift_pockets_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_23_payoff_asymmetry_pf_source_onnx_scout_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_23/frontier23d_stage_closeout.py")

F23B_SUMMARY = STAGE_ROOT / "02_runs" / f23b.RUN_ID / "final_summary.json"
F23B_CANDIDATES = STAGE_ROOT / "02_runs" / f23b.RUN_ID / "candidate_summary.csv"
F23C_SUMMARY = STAGE_ROOT / "02_runs" / f23c.RUN_ID / "final_summary.json"
F23C_CANDIDATES = STAGE_ROOT / "02_runs" / f23c.RUN_ID / "repair_candidate_summary.csv"
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier23_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f23_payoff_asymmetry_near_seed_pockets_reference_only"
    "(전선23 보상 비대칭 근접 씨앗 구간 참조 전용)"
)
NEGATIVE_MEMORY = (
    "under_f23_locked_proxy_payoff_asymmetry_entry_filters_did_not_jointly_satisfy_seed_or_handoff"
    "(전선23 잠금 프록시 계약 하에서 보상 비대칭 진입 필터가 씨앗/인계 게이트를 동시에 충족하지 못함)"
)
RUNTIME_BLOCKER = (
    "runtime_probe_ineligible_no_handoff_candidate_after_f23_capped_repair"
    "(전선23 상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격)"
)
ONNX_BLOCKER = (
    "onnx_branch_unattempted_no_handoff_candidate_after_f23_capped_repair"
    "(전선23 상한 수리 뒤 인계 후보가 없어 ONNX 분기 미개시)"
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    normalize_grok_markdown()
    created_at = utc_now()
    f23b_summary = read_json(F23B_SUMMARY)
    f23c_summary = read_json(F23C_SUMMARY)
    f23b_candidates = pd.read_csv(io_path(F23B_CANDIDATES))
    f23c_candidates = pd.read_csv(io_path(F23C_CANDIDATES))
    grok = read_grok_packet(GROK_PACKET)
    local = local_verification(f23b_summary, f23c_summary, f23b_candidates, f23c_candidates, grok)
    if local["judgment"] != "pass_closeout_ready(마감 준비 통과)":
        raise RuntimeError(f"Frontier23D local verification failed: {json.dumps(local, ensure_ascii=False)}")
    final = build_final(created_at, f23b_summary, f23c_summary, f23b_candidates, f23c_candidates, grok, local)
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
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
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
    if "accepted_with_adjustments" in lowered or "조정 수용" in text:
        return "accepted_with_adjustments(조정 수용)"
    if "needs_local_verification" in lowered or "로컬 검증 필요" in text:
        return "needs_local_verification(로컬 검증 필요)"
    if "accepted" in lowered or "수용" in text:
        return "accepted(수용)"
    return "classification_missing(분류 누락)"


def local_verification(
    f23b_summary: dict[str, Any],
    f23c_summary: dict[str, Any],
    f23b_candidates: pd.DataFrame,
    f23c_candidates: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    f23b_best = row_by_id(f23b_candidates, "candidate_id", "f23b_0333")
    f23c_best = row_by_id(f23c_candidates, "repair_id", "f23c_0123")
    high_pf_low_density = row_by_id(f23c_candidates, "repair_id", "f23c_0071")
    pf_density_dd_fail = row_by_id(f23c_candidates, "repair_id", "f23c_0233")
    f23b_seed_true_rows = bool_series_sum(f23b_candidates["seed_surface_flag"])
    f23b_handoff_true_rows = bool_series_sum(f23b_candidates["handoff_candidate_flag"])
    f23c_seed_true_rows = bool_series_sum(f23c_candidates["seed_surface_flag"])
    f23c_handoff_true_rows = bool_series_sum(f23c_candidates["handoff_candidate_flag"])
    checks = {
        "f23b_sanity_gate_passed": bool(f23b_summary.get("sanity_gate_pass")) and int(f23b_summary.get("sanity_pass_rows", 0)) == 78,
        "f23b_seed_and_handoff_zero": int(f23b_summary.get("seed_surface_rows", -1)) == 0
        and int(f23b_summary.get("handoff_candidate_rows", -1)) == 0
        and f23b_seed_true_rows == 0
        and f23b_handoff_true_rows == 0,
        "f23b_best_density_aligned_but_oos_pf_weak": 5.0 <= float(f23b_best["oos_trades_per_day"]) <= 10.0
        and float(f23b_best["oos_profit_factor"]) < f23b.SEED_PF,
        "f23c_seed_and_handoff_zero": int(f23c_summary.get("seed_surface_rows", -1)) == 0
        and int(f23c_summary.get("handoff_candidate_rows", -1)) == 0
        and f23c_seed_true_rows == 0
        and f23c_handoff_true_rows == 0,
        "f23c_scout_clues_exist": int(f23c_summary.get("scout_clue_rows", 0)) > 0,
        "f23c_best_density_aligned_but_oos_pf_weak": 5.0 <= float(f23c_best["oos_trades_per_day"]) <= 10.0
        and float(f23c_best["oos_profit_factor"]) < f23b.SEED_PF,
        "f23c_high_pf_low_density_anchor": float(high_pf_low_density["validation_profit_factor"]) >= f23b.SEED_PF
        and float(high_pf_low_density["oos_profit_factor"]) >= f23b.SEED_PF
        and float(high_pf_low_density["validation_trades_per_day"]) < f23b.SEED_DENSITY_LOW
        and float(high_pf_low_density["oos_trades_per_day"]) < f23b.SEED_DENSITY_LOW,
        "f23c_pf_density_dd_fail_anchor": float(pf_density_dd_fail["validation_profit_factor"]) >= f23b.SEED_PF
        and float(pf_density_dd_fail["oos_profit_factor"]) >= f23b.SEED_PF
        and f23b.SEED_DENSITY_LOW <= float(pf_density_dd_fail["validation_trades_per_day"]) <= f23b.SEED_DENSITY_HIGH
        and f23b.SEED_DENSITY_LOW <= float(pf_density_dd_fail["oos_trades_per_day"]) <= f23b.SEED_DENSITY_HIGH
        and float(pf_density_dd_fail["validation_dd_risk"]) > f23c.SEED_DD_CAP,
        "grok_success": grok["success"] and not grok["timed_out"] and grok["returncode"] == 0,
        "grok_accepts_closeout_boundary": grok["classification"] in {
            "accepted_with_adjustments(조정 수용)",
            "accepted(수용)",
            "needs_local_verification(로컬 검증 필요)",
        },
        "grok_no_unexpected_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
        "notes": {
            "seed_gate": f"F23C uses repair seed DD cap {f23c.SEED_DD_CAP:.0f}%(전선23C 수리 씨앗 손실폭 상한). f23c_0233 fails under that cap and under the final 10% goal boundary(최종 10% 목표 경계).",
            "runtime_boundary": "No handoff rows means MT5 runtime probe(런타임 탐침) is ineligible, not merely deferred.",
            "grok_adjustment": "Preserved clue(보존 단서) keeps density-aligned weak-OOS-PF and high-PF low-density archetypes separately.",
        },
    }


def build_final(
    created_at: str,
    f23b_summary: dict[str, Any],
    f23c_summary: dict[str, Any],
    f23b_candidates: pd.DataFrame,
    f23c_candidates: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    f23b_best = row_by_id(f23b_candidates, "candidate_id", "f23b_0333")
    f23c_best = row_by_id(f23c_candidates, "repair_id", "f23c_0123")
    high_pf_low_density = row_by_id(f23c_candidates, "repair_id", "f23c_0071")
    pf_density_dd_fail = row_by_id(f23c_candidates, "repair_id", "f23c_0233")
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
        "tier_boundary": "Tier A proxy only; Tier B missing_required; Tier A+B out_of_scope_by_claim(Tier A 프록시 전용, Tier B 필수 누락, Tier A+B 주장 범위 밖)",
        "data_boundary": "proxy/oracle-label research only; no verified MT5 payoff-asymmetry runtime semantics(프록시/오라클 라벨 연구 전용, 검증된 MT5 보상 비대칭 런타임 의미 없음)",
        "pocket_archetypes": {
            "density_aligned_weak_oos_pf": {
                "candidate_id": "f23b_0333",
                "repair_id": "f23c_0123",
                "meaning": "density 5-10/day is present, but OOS PF remains below seed floor(빈도 5~10회/일은 있으나 표본외 PF가 씨앗 바닥 미만)",
                "f23b_best": metric_excerpt(f23b_best),
                "f23c_best": metric_excerpt(f23c_best),
            },
            "high_pf_low_density": {
                "repair_id": "f23c_0071",
                "meaning": "validation/OOS PF passes 1.20, but density is below 5/day and DD is still above final goal(검증/표본외 PF는 1.20을 넘지만 빈도는 5회/일 미만이고 손실폭은 최종 목표 초과)",
                "metrics": metric_excerpt(high_pf_low_density),
            },
            "pf_density_but_dd_fail": {
                "repair_id": "f23c_0233",
                "meaning": "PF and density are usable, but validation DD blocks seed(수익 팩터와 빈도는 쓸 만하지만 검증 손실폭이 씨앗을 차단)",
                "metrics": metric_excerpt(pf_density_dd_fail),
            },
        },
        "f23b_scout_clue_rows": f23b_summary.get("scout_clue_rows"),
        "f23b_seed_surface_rows": f23b_summary.get("seed_surface_rows"),
        "f23b_handoff_candidate_rows": f23b_summary.get("handoff_candidate_rows"),
        "f23c_scout_clue_rows": f23c_summary.get("scout_clue_rows"),
        "f23c_seed_surface_rows": f23c_summary.get("seed_surface_rows"),
        "f23c_handoff_candidate_rows": f23c_summary.get("handoff_candidate_rows"),
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
            "next_run_id": NEXT_FRONTIER_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(F23B_SUMMARY),
            artifact_identity(F23B_CANDIDATES),
            artifact_identity(F23C_SUMMARY),
            artifact_identity(F23C_CANDIDATES),
            artifact_identity(GROK_PACKET / "clean_output.md"),
            artifact_identity(REPORT_PATH),
            artifact_identity(GROK_RECEIPT_PATH),
            artifact_identity(GATE_AUDIT_PATH),
            artifact_identity(REQUIRED_GATE_AUDIT_PATH),
            artifact_identity(DECISION_PATH),
        ],
        "results": {
            "cross_split": {
                "closeout": final["judgment"],
                "f23b_scout_seed_handoff": [
                    final["f23b_scout_clue_rows"],
                    final["f23b_seed_surface_rows"],
                    final["f23b_handoff_candidate_rows"],
                ],
                "f23c_scout_seed_handoff": [
                    final["f23c_scout_clue_rows"],
                    final["f23c_seed_surface_rows"],
                    final["f23c_handoff_candidate_rows"],
                ],
                "runtime_blocker": final["runtime_blocker"],
                "onnx_blocker": final["onnx_blocker"],
            },
            "report_refs": [{"role": "stage_closeout_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier23d_closeout_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
        },
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any]) -> str:
    density = final["pocket_archetypes"]["density_aligned_weak_oos_pf"]
    high_pf = final["pocket_archetypes"]["high_pf_low_density"]["metrics"]
    dd_fail = final["pocket_archetypes"]["pf_density_but_dd_fail"]["metrics"]
    return f"""# Frontier23D Payoff Asymmetry PF Source Closeout Report(전선23D 보상 비대칭 수익 팩터 원천 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): Frontier23(전선23)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): payoff asymmetry(보상 비대칭)는 PF-positive pocket(PF 양수 구간)을 찾는 단서로 보존하지만, density/DD/PF(빈도/손실폭/수익 팩터)가 동시에 맞지 않아 seed/handoff(씨앗/인계)로 보내지 않습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

- Density-aligned weak-OOS-PF(빈도 맞음, 표본외 PF 약함): `f23b_0333` -> `f23c_0123`; validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(density['f23c_best']['validation_profit_factor'])}/{fmt(density['f23c_best']['validation_trades_per_day'])}/{fmt(density['f23c_best']['validation_dd_risk'])}` and `{fmt(density['f23c_best']['oos_profit_factor'])}/{fmt(density['f23c_best']['oos_trades_per_day'])}/{fmt(density['f23c_best']['oos_dd_risk'])}`.
- High-PF low-density(고 PF, 저 빈도): `f23c_0071`; validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(high_pf['validation_profit_factor'])}/{fmt(high_pf['validation_trades_per_day'])}/{fmt(high_pf['validation_dd_risk'])}` and `{fmt(high_pf['oos_profit_factor'])}/{fmt(high_pf['oos_trades_per_day'])}/{fmt(high_pf['oos_dd_risk'])}`.
- PF-density but DD fail(PF-빈도 가능, 손실폭 실패): `f23c_0233`; validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(dd_fail['validation_profit_factor'])}/{fmt(dd_fail['validation_trades_per_day'])}/{fmt(dd_fail['validation_dd_risk'])}` and `{fmt(dd_fail['oos_profit_factor'])}/{fmt(dd_fail['oos_trades_per_day'])}/{fmt(dd_fail['oos_dd_risk'])}`.

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
    return f"""# Frontier23D Grok Closeout Receipt(전선23D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout(단계 마감)에 Grok review(그록 검토)가 필요했습니다.

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): close Frontier23(전선23)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감.

Prompt(프롬프트): `{grok['prompt']}`

Output(출력): `{grok['output']}`

Advice classification(조언 분류): `{grok['classification']}`

Accepted advice(수용 조언): near-miss(근접 미달)를 묻지 말고 density-aligned weak-OOS-PF(빈도 맞음, 표본외 PF 약함)와 high-PF low-density(고 PF, 저 빈도)를 분리해 보존합니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Forbidden claim check(금지 주장 확인): pass(통과). Grok(그록)은 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않았습니다.

Final Codex direction(최종 Codex 방향): close as preserved clue + negative memory(보존 단서 + 부정 기억으로 마감).
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier23D Gate Audit(전선23D 게이트 감사)

- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- external_review_packet(외부 검토 묶음): `{GROK_PACKET.as_posix()}`
- local_verification_gate(로컬 검증 게이트): `{final['local_verification']['judgment']}`
- kpi_contract_audit(KPI 계약 감사): F23B/F23C summaries and candidate summaries(F23B/F23C 요약과 후보 요약) checked(확인)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_blocker']}`
- onnx_gate(ONNX 게이트): `{final['onnx_blocker']}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일) and `{REQUIRED_GATE_AUDIT_PATH.as_posix()}`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def required_gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier23 Required Gate Coverage Audit(전선23 필수 게이트 커버리지 감사)

Work family(작업군): experiment_execution(실험 실행) + publish_handoff(게시/인계) closeout(마감)

- scope_completion_gate(범위 완료 게이트): F23A/F23B/F23C/F23D lifecycle(생명주기) materialized(물질화)
- kpi_contract_audit(KPI 계약 감사): proxy and repair KPI(프록시와 수리 KPI) recorded in run and stage ledgers(실행/단계 장부에 기록)
- external_review_packet(외부 검토 묶음): stage open(단계 개방) `docs/agent_control/grok_reviews/2026-06-14_frontier23_stage_open/small_review` and closeout(마감) `{GROK_PACKET.as_posix()}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_blocker']}`
- onnx_scope_gate(ONNX 범위 게이트): `{final['onnx_blocker']}`
- closeout_gate(마감 게이트): `{final['judgment']}`
- final_claim_guard(최종 주장 방어): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    return f"""# Frontier23 Preserved Clue(전선23 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F23B/F23C(전선23B/C)는 seed/handoff(씨앗/인계)을 만들지 못했지만, payoff asymmetry(보상 비대칭)가 두 종류의 near-miss pocket(근접 미달 구간)을 드러냈습니다.

- Density-aligned weak-OOS-PF(빈도 맞음, 표본외 PF 약함): `f23c_0123`
- High-PF low-density(고 PF, 저 빈도): `f23c_0071`
- PF-density but DD fail(PF-빈도 가능, 손실폭 실패): `f23c_0233`

Boundary(경계): reference-only(참조 전용). It is not seed/handoff/completion/baseline/promotion/runtime authority(씨앗/인계/완성/기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier23 Negative Memory(전선23 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): F23B(전선23B)는 scout/seed/handoff(탐색/씨앗/인계) `{final['f23b_scout_clue_rows']}/{final['f23b_seed_surface_rows']}/{final['f23b_handoff_candidate_rows']}`였고, F23C(전선23C)는 `{final['f23c_scout_clue_rows']}/{final['f23c_seed_surface_rows']}/{final['f23c_handoff_candidate_rows']}`였습니다. 보상 비대칭 진입 필터는 PF(수익 팩터), density(빈도), DD(손실폭)를 동시에 맞추지 못했습니다.

Runtime blocker(런타임 차단): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`

Do not repeat(반복 금지): F23 locked proxy contract(전선23 잠금 프록시 계약) 아래에서 같은 payoff asymmetry + capped entry-known filter(보상 비대칭 + 상한 진입시점 필터)만 반복하지 않습니다.

Reopen condition(재개 조건): 새 가설이 density bridge(빈도 연결) 또는 DD normalization(손실폭 정규화)을 먼저 해결하고 seed/handoff(씨앗/인계)를 다시 만들 때만 이 단서를 참조합니다.
"""


def selection_status_text(final: dict[str, Any]) -> str:
    return f"""# Frontier23 Selection Status(전선23 선택 상태)

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
    return f"""# Decision(결정): Close Frontier23(전선23 마감)

Date(날짜): 2026-06-14

Decision(결정): close Frontier23(전선23)을 `{final['status']}`로 닫습니다.

Action(행동): payoff asymmetry PF source scout(보상 비대칭 수익 팩터 원천 탐색)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감했습니다.

Effect(효과): 다음 전선(frontier, 전선)은 F23(전선23)의 단서를 reference only(참조 전용)로만 쓰고, winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않습니다.

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
    density = final["pocket_archetypes"]["density_aligned_weak_oos_pf"]["f23c_best"]
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
        "primary_kpi": f"f23c_0123_oos_pf={fmt(density['oos_profit_factor'])};oos_density={fmt(density['oos_trades_per_day'])};oos_dd={fmt(density['oos_dd_risk'])}",
        "guardrail_kpi": "no_seed_no_handoff_no_wfo_no_mt5_no_onnx_no_authority(씨앗/인계/WFO/MT5/ONNX/권위 없음)",
        "external_verification_status": final["runtime_blocker"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    density = final["pocket_archetypes"]["density_aligned_weak_oos_pf"]["f23c_best"]
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
            f"f23c_scout={final['f23c_scout_clue_rows']};seed={final['f23c_seed_surface_rows']};"
            f"handoff={final['f23c_handoff_candidate_rows']};oos_pf={fmt(density['oos_profit_factor'])};"
            f"oos_density={fmt(density['oos_trades_per_day'])};oos_dd={fmt(density['oos_dd_risk'])}"
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
        "Effect(효과): 다음 전선은 density bridge(빈도 연결) 또는 DD normalization(손실폭 정규화)을 새 가설로 다루며 F23(전선23)을 상속하지 않습니다.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR23-PAYOFF-ASYMMETRY-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` closes Frontier23(전선23) as preserved clue + negative memory(보존 단서 + 부정 기억). "
        "Effect(효과): PF-positive pocket(PF 양수 구간)은 보존하지만 seed/handoff(씨앗/인계) 없음으로 ONNX(온엑스)와 MT5 runtime probe(MT5 런타임 탐침)는 열지 않습니다.\n"
    )


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier23(전선23) as preserved clue + negative memory(보존 단서 + 부정 기억). "
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
    high_pf = final["pocket_archetypes"]["high_pf_low_density"]["metrics"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier23(전선23)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): payoff asymmetry(보상 비대칭)는 PF-positive pocket(PF 양수 구간) 단서로 남기되, seed/handoff(씨앗/인계)가 없어서 ONNX(온엑스), WFO(워크포워드 최적화), MT5 runtime probe(MT5 런타임 탐침)는 열지 않습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Notable near-miss(주요 근접 미달): `f23c_0071` validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(high_pf['validation_profit_factor'])}/{fmt(high_pf['validation_trades_per_day'])}/{fmt(high_pf['validation_dd_risk'])}` and `{fmt(high_pf['oos_profit_factor'])}/{fmt(high_pf['oos_trades_per_day'])}/{fmt(high_pf['oos_dd_risk'])}`.

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
        "candidate_id",
        "repair_id",
        "source_candidate_id",
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
        "scout_clue_flag",
        "seed_surface_flag",
        "handoff_candidate_flag",
    )
    return {field: json_ready(row.get(field, "")) for field in fields if field in row}


def bool_series_sum(series: pd.Series) -> int:
    return int(series.astype(str).str.lower().eq("true").sum())


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
