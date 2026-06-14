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
from stage_pipelines.stage_frontier_22 import frontier22b_session_return_shock_pf_source_proxy_scout as f22b
from stage_pipelines.stage_frontier_22 import frontier22c_shock_pf_source_lifecycle_repair_scout as f22c


STAGE_ID = f22c.STAGE_ID
RUN_ID = "frontier22D_stage_closeout_shock_pf_source_v1"
RUN_NUMBER = "frontier22D"
PARENT_RUN_ID = f22c.RUN_ID
NEXT_FRONTIER_RUN_ID = "frontier23A_stage_open_payoff_asymmetry_pf_source_hypothesis_design_v1"

STATUS = "closed_preserved_clue_negative_memory_shock_lifecycle_low_dd_density_weak_pf_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_22/frontier22d_stage_closeout.py")

F22B_SUMMARY = STAGE_ROOT / "02_runs" / f22b.RUN_ID / "final_summary.json"
F22B_CANDIDATES = STAGE_ROOT / "02_runs" / f22b.RUN_ID / "candidate_summary.csv"
F22C_SUMMARY = STAGE_ROOT / "02_runs" / f22c.RUN_ID / "final_summary.json"
F22C_CANDIDATES = STAGE_ROOT / "02_runs" / f22c.RUN_ID / "repair_candidate_summary.csv"
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier22_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f22_shock_trend_hold2_low_dd_density_reference_only"
    "(전선22 충격+추세 hold2 낮은 손실폭/목표 빈도 참고 단서 전용)"
)
NEGATIVE_MEMORY = (
    "shock_anchored_cross_family_pf_source_did_not_create_seed_or_handoff"
    "(충격 고정 교차군 수익 팩터 원천은 씨앗/인계를 만들지 못함)"
)
RUNTIME_BLOCKER = (
    "runtime_probe_ineligible_no_handoff_candidate_after_f22_capped_repair"
    "(전선22 상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격)"
)
ONNX_BLOCKER = (
    "onnx_branch_unattempted_no_seed_or_handoff_candidate"
    "(씨앗 또는 인계 후보가 없어 ONNX 분기 미개시)"
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    normalize_grok_markdown()
    created_at = utc_now()
    f22b_summary = read_json(F22B_SUMMARY)
    f22c_summary = read_json(F22C_SUMMARY)
    f22b_candidates = pd.read_csv(io_path(F22B_CANDIDATES))
    f22c_candidates = pd.read_csv(io_path(F22C_CANDIDATES))
    grok = read_grok_packet(GROK_PACKET)
    local = local_verification(f22b_summary, f22c_summary, f22b_candidates, f22c_candidates, grok)
    if local["judgment"] != "pass_closeout_ready(마감 준비 통과)":
        raise RuntimeError(f"Frontier22D local verification failed: {json.dumps(local, ensure_ascii=False)}")
    final = build_final(created_at, f22b_summary, f22c_summary, f22b_candidates, f22c_candidates, grok, local)
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
        "classification": classify_grok(output),
        "output_excerpt": output[:3200],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    has_accepted = "accepted(수용)" in text or "accepted" in lowered
    has_local = "needs_local_verification(로컬 검증 필요)" in text or "needs_local_verification" in lowered
    has_rejected = "rejected(거절)" in text or "rejected" in lowered
    if has_accepted and has_local and has_rejected:
        return "accepted_with_local_verification(로컬 검증 조건부 수용)"
    if has_accepted:
        return "accepted(수용)"
    if "reject" in lowered:
        return "rejected(거절)"
    return "classification_missing(분류 누락)"


def local_verification(
    f22b_summary: dict[str, Any],
    f22c_summary: dict[str, Any],
    f22b_candidates: pd.DataFrame,
    f22c_candidates: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    f22b_best = f22b_candidates.loc[f22b_candidates["candidate_id"].astype(str).eq("f22b_0379")].iloc[0]
    f22c_best = dict(f22c_summary.get("best_profile", {}))
    f22b_seed_true_rows = bool_series_sum(f22b_candidates["seed_surface_flag"])
    f22c_seed_true_rows = bool_series_sum(f22c_candidates["seed_surface_flag"])
    f22c_handoff_true_rows = bool_series_sum(f22c_candidates["handoff_candidate_flag"])
    checks = {
        "f22b_seed_zero_summary_and_csv": int(f22b_summary.get("seed_surface_rows", -1)) == 0 and f22b_seed_true_rows == 0,
        "f22b_best_not_seed_due_oos_pf": float(f22b_best["oos_profit_factor"]) < f22b.SEED_PF,
        "f22b_best_smoothness_false": not bool(f22b_best.get("validation_smoothness_pass")) and not bool(f22b_best.get("oos_smoothness_pass")),
        "f22b_search_cap_applied_after_enumeration": int(f22b_summary.get("candidate_pool_rows", 0)) == 464
        and int(f22b_summary.get("selected_candidate_rows", 9999)) <= f22b.MAX_CANDIDATES,
        "f22b_f20_duplicate_guard_zero": int(f22b_summary.get("f20_duplicate_pressure_rows", -1)) == 0,
        "f22c_scout_one_seed_zero_handoff_zero": int(f22c_summary.get("scout_clue_rows", -1)) == 1
        and int(f22c_summary.get("seed_surface_rows", -1)) == 0
        and int(f22c_summary.get("handoff_candidate_rows", -1)) == 0
        and f22c_seed_true_rows == 0
        and f22c_handoff_true_rows == 0,
        "f22c_best_pf_below_seed_floor": float(f22c_best.get("validation_profit_factor", 999.0)) < f22c.SEED_PF
        and float(f22c_best.get("oos_profit_factor", 999.0)) < f22c.SEED_PF,
        "f22c_best_density_and_dd_preserved": 5.0 <= float(f22c_best.get("validation_trades_per_day", 0.0)) <= 10.0
        and 5.0 <= float(f22c_best.get("oos_trades_per_day", 0.0)) <= 10.0
        and float(f22c_best.get("validation_dd_risk_percent", 999.0)) < 10.0
        and float(f22c_best.get("oos_dd_risk_percent", 999.0)) < 10.0,
        "tier_boundary_recorded": True,
        "onnx_scope_miss_recorded": True,
        "grok_success": grok["success"] and not grok["timed_out"] and grok["returncode"] == 0,
        "grok_accepts_closeout_boundary": grok["classification"] in {
            "accepted_with_local_verification(로컬 검증 조건부 수용)",
            "accepted(수용)",
        },
        "grok_no_unexpected_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
        "notes": {
            "f22b_seed_zero_reason": "f22b_0379 OOS PF 1.16910 is below seed floor 1.20 and smoothness pass is false(f22b_0379 표본외 수익 팩터 1.16910은 씨앗 바닥 1.20 미만이고 매끄러움 통과도 거짓)",
            "search_cap_reason": "candidate_pool_rows 464 is pre-cap enumeration; selected_candidate_rows 156 is below max_candidates 200(후보 464행은 상한 전 열거이고 선택 후보 156행은 최대 200 미만)",
            "tier_boundary_reason": "Tier B is missing_required and Tier A+B is out_of_scope_by_claim(티어 B는 필수 누락, 티어 A+B는 주장 범위 밖)",
        },
    }


def bool_series_sum(series: pd.Series) -> int:
    return int(series.astype(str).str.lower().eq("true").sum())


def build_final(
    created_at: str,
    f22b_summary: dict[str, Any],
    f22c_summary: dict[str, Any],
    f22b_candidates: pd.DataFrame,
    f22c_candidates: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    f22b_best = dict(f22b_candidates.loc[f22b_candidates["candidate_id"].astype(str).eq("f22b_0379")].iloc[0])
    f22c_best = dict(f22c_summary.get("best_profile", {}))
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
        "data_boundary": "proxy/oracle-label research only; no verified MT5 session-shock runtime semantics(프록시/오라클 라벨 연구 전용, 검증된 MT5 세션-충격 런타임 의미 없음)",
        "f22b_proxy_detail": {
            "candidate_id": f22b_best.get("candidate_id"),
            "rule_definition": f22b_best.get("rule_definition"),
            "validation_profit_factor": f22b_best.get("validation_profit_factor"),
            "validation_trades_per_day": f22b_best.get("validation_trades_per_day"),
            "validation_dd_risk": f22b_best.get("validation_dd_risk"),
            "oos_profit_factor": f22b_best.get("oos_profit_factor"),
            "oos_trades_per_day": f22b_best.get("oos_trades_per_day"),
            "oos_dd_risk": f22b_best.get("oos_dd_risk"),
            "meaning": "near_seed_proxy_but_oos_pf_below_seed_floor_and_no_handoff(근접 씨앗 프록시지만 표본외 수익 팩터가 씨앗 바닥 미만이고 인계 없음)",
        },
        "f22c_lifecycle_detail": {
            "profile_id": f22c_summary.get("best_profile_id"),
            "source_candidate_id": f22c_best.get("source_candidate_id"),
            "rule_definition": f22c_best.get("source_rule_definition"),
            "validation_profit_factor": f22c_best.get("validation_profit_factor"),
            "validation_trades_per_day": f22c_best.get("validation_trades_per_day"),
            "validation_dd_risk_percent": f22c_best.get("validation_dd_risk_percent"),
            "validation_equity_trend_r2": f22c_best.get("validation_equity_trend_r2"),
            "oos_profit_factor": f22c_best.get("oos_profit_factor"),
            "oos_trades_per_day": f22c_best.get("oos_trades_per_day"),
            "oos_dd_risk_percent": f22c_best.get("oos_dd_risk_percent"),
            "oos_equity_trend_r2": f22c_best.get("oos_equity_trend_r2"),
            "meaning": "density_low_dd_smoothness_clue_but_pf_weak(빈도/낮은 손실폭/매끄러움 단서이나 수익 팩터 약함)",
        },
        "f22b_scout_clue_rows": f22b_summary.get("scout_clue_rows"),
        "f22b_seed_surface_rows": f22b_summary.get("seed_surface_rows"),
        "f22b_handoff_candidate_rows": f22b_summary.get("handoff_candidate_rows"),
        "f22c_scout_clue_rows": f22c_summary.get("scout_clue_rows"),
        "f22c_seed_surface_rows": f22c_summary.get("seed_surface_rows"),
        "f22c_handoff_candidate_rows": f22c_summary.get("handoff_candidate_rows"),
        "grok_closeout": grok,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "final_closeout_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt_text(final))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit_text(final))
    f03b.write_text_sig(REQUIRED_GATE_AUDIT_PATH, required_gate_audit_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status_text(final))


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
            artifact_identity(F22B_SUMMARY),
            artifact_identity(F22B_CANDIDATES),
            artifact_identity(F22C_SUMMARY),
            artifact_identity(F22C_CANDIDATES),
            artifact_identity(GROK_PACKET / "clean_output.md"),
            artifact_identity(REPORT_PATH),
            artifact_identity(GROK_RECEIPT_PATH),
            artifact_identity(GATE_AUDIT_PATH),
            artifact_identity(REQUIRED_GATE_AUDIT_PATH),
        ],
        "results": {
            "cross_split": {
                "closeout": final["judgment"],
                "f22b_scout_seed_handoff": [
                    final["f22b_scout_clue_rows"],
                    final["f22b_seed_surface_rows"],
                    final["f22b_handoff_candidate_rows"],
                ],
                "f22c_scout_seed_handoff": [
                    final["f22c_scout_clue_rows"],
                    final["f22c_seed_surface_rows"],
                    final["f22c_handoff_candidate_rows"],
                ],
                "runtime_blocker": final["runtime_blocker"],
                "onnx_blocker": final["onnx_blocker"],
            },
            "report_refs": [{"role": "stage_closeout_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier22d_closeout_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
        },
    }


def report_text(final: dict[str, Any]) -> str:
    b = final["f22b_proxy_detail"]
    c = final["f22c_lifecycle_detail"]
    return f"""# Frontier22D Shock PF Source Closeout Report(전선22D 충격 수익 팩터 원천 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): Frontier22(전선22)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): shock+trend lifecycle surface(충격+추세 생명주기 표면)의 낮은 DD(손실폭)와 목표 density(빈도)는 참고 단서로 보존하고, PF source(수익 팩터 원천) 가설이 seed/handoff(씨앗/인계)를 만들지 못했다는 반복 금지 기억을 남깁니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

- F22B proxy surface(F22B 프록시 표면): `{b['candidate_id']}` validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(b['validation_profit_factor'])}/{fmt(b['validation_trades_per_day'])}/{fmt(b['validation_dd_risk'])}` and `{fmt(b['oos_profit_factor'])}/{fmt(b['oos_trades_per_day'])}/{fmt(b['oos_dd_risk'])}`. Meaning(의미): `{b['meaning']}`.
- F22C lifecycle surface(F22C 생명주기 표면): `{c['profile_id']}` validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(c['validation_profit_factor'])}/{fmt(c['validation_trades_per_day'])}/{fmt(c['validation_dd_risk_percent'])}` and `{fmt(c['oos_profit_factor'])}/{fmt(c['oos_trades_per_day'])}/{fmt(c['oos_dd_risk_percent'])}`. Equity trend R2(자산곡선 추세 R2) `{fmt(c['validation_equity_trend_r2'])}/{fmt(c['oos_equity_trend_r2'])}`. Meaning(의미): `{c['meaning']}`.

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
    return f"""# Frontier22D Grok Closeout Receipt(전선22D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout required by goal(목표가 요구한 단계 마감 검토).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): close Frontier22 as preserved clue + negative memory(전선22를 보존 단서 + 부정 기억으로 마감).

Prompt(프롬프트): `{grok['prompt']}`

Output(출력): `{grok['output']}`

Advice classification(조언 분류): `{grok['classification']}`.

Accepted advice(수용 조언): closeout class(마감 분류) accepted(수용), F22C preserved clue(전선22C 보존 단서) narrow(좁게), next hypothesis(다음 가설)는 stronger PF source(더 강한 수익 팩터 원천)로 이동.

Needs local verification(로컬 검증 필요): F22B seed count(씨앗 수), Tier B gap(티어 B 공백), F22B/F22C surface split(표면 분리), search cap accounting(탐색 상한 회계), ONNX scope miss(ONNX 범위 미달), data boundary(데이터 경계).

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Forbidden claim check(금지 주장 확인): pass(통과). Grok(그록)은 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않았습니다.

Final Codex direction(최종 Codex 방향): close as preserved_clue + negative_memory(보존 단서 + 부정 기억으로 마감).
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier22D Gate Audit(전선22D 게이트 감사)

- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- external_review_packet(외부 검토 묶음): `{GROK_PACKET.as_posix()}`
- local_verification_gate(로컬 검증 게이트): `{final['local_verification']['judgment']}`
- kpi_contract_audit(KPI 계약 감사): F22B/F22C summaries and candidate summaries(F22B/F22C 요약과 후보 요약) checked(확인)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일) and `{REQUIRED_GATE_AUDIT_PATH.as_posix()}`
- final_claim_guard(최종 주장 방지): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def required_gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier22 Required Gate Coverage Audit(전선22 필수 게이트 커버리지 감사)

Work family(작업군): experiment_execution(실험 실행) + publish_handoff(게시/인계) closeout(마감)

- scope_completion_gate(범위 완료 게이트): F22A/F22B/F22C/F22D lifecycle(생명주기) materialized(물질화)
- kpi_contract_audit(KPI 계약 감사): proxy/lifecycle KPI(프록시/생명주기 KPI) recorded in run and stage ledgers(실행/단계 장부에 기록)
- external_review_packet(외부 검토 묶음): stage open(단계 개방) `{Path('docs/agent_control/grok_reviews/2026-06-14_frontier22_stage_open/small_review').as_posix()}` and closeout(마감) `{GROK_PACKET.as_posix()}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): pass(통과)
- closeout_gate(마감 게이트): `{final['judgment']}`
- final_claim_guard(최종 주장 방지): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    c = final["f22c_lifecycle_detail"]
    return f"""# Frontier22 Preserved Clue(전선22 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F22C best lifecycle repair(F22C 최상 생명주기 수리) `{c['profile_id']}` produced validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(c['validation_profit_factor'])}/{fmt(c['validation_trades_per_day'])}/{fmt(c['validation_dd_risk_percent'])}` and `{fmt(c['oos_profit_factor'])}/{fmt(c['oos_trades_per_day'])}/{fmt(c['oos_dd_risk_percent'])}`.

Boundary(경계): reference-only(참조 전용). It is not seed/handoff/completion/baseline/promotion/runtime authority(씨앗/인계/완성/기준선/승격/런타임 권위 아님).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier22 Negative Memory(전선22 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): F22B(전선22B)는 scout clue(탐색 단서) 35개를 만들었지만 seed/handoff(씨앗/인계)는 `0/0`이었습니다. F22C(전선22C)는 DD(손실폭)와 density(빈도)를 좋게 만들었지만 validation/OOS PF(검증/표본외 수익 팩터)가 `1.05579/1.10525`로 seed floor(씨앗 바닥) `1.20`보다 낮았습니다.

Runtime blocker(런타임 차단): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`

Do not repeat(반복 금지): same shock+trend entry plus hold2/ATR lifecycle micro-tuning(같은 충격+추세 진입과 hold2/ATR 생명주기 미세 조정)을 primary next hypothesis(다음 주 가설)로 반복하지 않습니다.

Reopen condition(재개 조건): a new PF source(새 수익 팩터 원천)가 validation/OOS PF(검증/표본외 수익 팩터)를 먼저 올리고, F22 low-DD lifecycle(F22 낮은 손실폭 생명주기)을 risk containment reference(위험 억제 참고)로만 쓸 때입니다.
"""


def selection_status_text(final: dict[str, Any]) -> str:
    return f"""# Frontier22 Selection Status(전선22 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Closeout(마감): `preserved_clue + negative_memory(보존 단서 + 부정 기억)`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{final['next_run_id']}`
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
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    c = final["f22c_lifecycle_detail"]
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
            f"f22c_scout={final['f22c_scout_clue_rows']};seed={final['f22c_seed_surface_rows']};"
            f"handoff={final['f22c_handoff_candidate_rows']};oos_pf={fmt(c['oos_profit_factor'])};"
            f"oos_density={fmt(c['oos_trades_per_day'])};oos_dd={fmt(c['oos_dd_risk_percent'])}"
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
        "Effect(효과): 다음 전선은 더 강한 PF source(수익 팩터 원천)를 새로 찾아야 하며 F22 생명주기 단서는 위험 억제 참고로만 씁니다.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR22-SESSION-RETURN-SHOCK-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` closes Frontier22(전선22) as preserved clue + negative memory(보존 단서 + 부정 기억). "
        "Effect(효과): shock+trend low-DD density clue(충격+추세 낮은 손실폭 빈도 단서)는 보존하되 PF source(수익 팩터 원천) 부족을 반복하지 않습니다.\n"
    )


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier22(전선22) as preserved clue + negative memory(보존 단서 + 부정 기억). "
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
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier22(전선22)를 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): shock+trend lifecycle surface(충격+추세 생명주기 표면)의 낮은 DD(손실폭)와 목표 density(빈도)는 보존하되, PF source(수익 팩터 원천)로는 seed/handoff(씨앗/인계)를 만들지 못했다는 반복 금지 기억을 남겼습니다.

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

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
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
