from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_21 import frontier21b_f20_seed_lifecycle_proxy_scout as f21b


STAGE_ID = f21b.STAGE_ID
RUN_ID = "frontier21D_lifecycle_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier21D"
PARENT_RUN_ID = "frontier21C_lifecycle_density_repair_scout_v1"
NEXT_FRONTIER_RUN_ID = "frontier22A_stage_open_new_pf_edge_source_hypothesis_design_v1"
STATUS = "closed_preserved_clue_negative_memory_lifecycle_low_dd_density_no_pf_edge_no_handoff"
JUDGMENT = "preserved_clue_negative_memory(보존 단서+부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_21/frontier21d_lifecycle_closeout.py")

F21B_SUMMARY = STAGE_ROOT / "02_runs/frontier21B_f20_seed_lifecycle_proxy_scout_v1/final_summary.json"
F21C_SUMMARY = STAGE_ROOT / "02_runs/frontier21C_lifecycle_density_repair_scout_v1/final_summary.json"
F21C_CANDIDATES = STAGE_ROOT / "02_runs/frontier21C_lifecycle_density_repair_scout_v1/candidate_summary.csv"
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier21_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")


PRESERVED_CLUE = "f21_low_dd_lifecycle_shapes_preserved_as_risk_containment_reference_only(전선21 낮은 손실폭 생명주기 모양은 위험 억제 참고 단서 전용)"
NEGATIVE_MEMORY = "lifecycle_dd_density_repair_alone_does_not_create_pf_edge_or_handoff(생명주기 손실폭/빈도 수리 단독은 수익 팩터 우위나 인계를 만들지 못함)"
RUNTIME_BLOCKER = "runtime_probe_ineligible_no_handoff_candidate_after_capped_repair(상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격)"
ONNX_BLOCKER = "onnx_branch_unattempted_no_seed_or_handoff_candidate(씨앗 또는 인계 후보가 없어 ONNX 분기 미개시)"


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    normalize_grok_markdown()
    created_at = utc_now()
    f21b_summary = read_json(F21B_SUMMARY)
    f21c_summary = read_json(F21C_SUMMARY)
    grok = read_grok_packet(GROK_PACKET)
    local = local_verification(f21b_summary, f21c_summary, grok)
    final = build_final(created_at, f21b_summary, f21c_summary, grok, local)
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
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path.exists():
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
        "output_excerpt": output[:2600],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "accept with minor adjust" in lowered or "수용, 소폭 조정" in text:
        return "accepted_with_minor_adjustments(소폭 조정 수용)"
    if "decision" in lowered and "accept" in lowered:
        return "accepted(수용)"
    if "decision" in lowered and "adjust" in lowered:
        return "accepted_with_adjustments(조정 수용)"
    if "decision" in lowered and "reject" in lowered:
        return "rejected(거절)"
    return "classification_missing(분류 누락)"


def local_verification(f21b_summary: dict[str, Any], f21c_summary: dict[str, Any], grok: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "f21b_no_scout_seed_handoff": f21b_summary.get("scout_clue_rows") == 0 and f21b_summary.get("seed_surface_rows") == 0 and f21b_summary.get("handoff_candidate_rows") == 0,
        "f21c_scout_three_seed_zero_handoff_zero": f21c_summary.get("scout_clue_rows") == 3 and f21c_summary.get("seed_surface_rows") == 0 and f21c_summary.get("handoff_candidate_rows") == 0,
        "f21c_best_profile_matches": f21c_summary.get("best_profile_id") == "f21c_hold2_atr0p8_tp1p6_cd0",
        "f21c_best_pf_below_seed_floor": float(f21c_summary.get("best_profile", {}).get("oos_profit_factor", 999.0)) < 1.2,
        "f21c_best_density_in_goal_band": 5.0 <= float(f21c_summary.get("best_profile", {}).get("oos_trades_per_day", 0.0)) <= 10.0,
        "f21c_best_dd_low": float(f21c_summary.get("best_profile", {}).get("oos_dd_risk_percent", 999.0)) < 5.0,
        "grok_success": grok["success"] and not grok["timed_out"] and grok["returncode"] == 0,
        "grok_accepts_closeout": grok["classification"] in {"accepted_with_minor_adjustments(소폭 조정 수용)", "accepted(수용)", "accepted_with_adjustments(조정 수용)"},
        "grok_no_unexpected_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_closeout_ready(마감 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
    }


def build_final(created_at: str, f21b_summary: dict[str, Any], f21c_summary: dict[str, Any], grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    best_b = f21b_summary.get("best_profile", {})
    best_c = f21c_summary.get("best_profile", {})
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
        "tier_boundary": "Tier A lifecycle proxy only; Tier B missing_required and Tier A+B out_of_scope_by_claim(티어 A 생명주기 프록시 전용, 티어 B 필수 누락 및 티어 A+B 주장 범위 밖)",
        "f21b_preserved_detail": {
            "profile_id": f21b_summary.get("best_profile_id"),
            "validation_profit_factor": best_b.get("validation_profit_factor"),
            "validation_trades_per_day": best_b.get("validation_trades_per_day"),
            "validation_dd_risk_percent": best_b.get("validation_dd_risk_percent"),
            "oos_profit_factor": best_b.get("oos_profit_factor"),
            "oos_trades_per_day": best_b.get("oos_trades_per_day"),
            "oos_dd_risk_percent": best_b.get("oos_dd_risk_percent"),
            "meaning": "low_dd_pf_maintained_but_density_below_goal(낮은 손실폭과 PF 유지는 보였지만 빈도 목표 미달)",
        },
        "f21c_preserved_detail": {
            "profile_id": f21c_summary.get("best_profile_id"),
            "validation_profit_factor": best_c.get("validation_profit_factor"),
            "validation_trades_per_day": best_c.get("validation_trades_per_day"),
            "validation_dd_risk_percent": best_c.get("validation_dd_risk_percent"),
            "oos_profit_factor": best_c.get("oos_profit_factor"),
            "oos_trades_per_day": best_c.get("oos_trades_per_day"),
            "oos_dd_risk_percent": best_c.get("oos_dd_risk_percent"),
            "meaning": "density_and_low_dd_aligned_but_pf_edge_missing(빈도와 낮은 손실폭은 정렬됐지만 수익 팩터 우위 없음)",
        },
        "scout_clue_rows": f21c_summary.get("scout_clue_rows"),
        "seed_surface_rows": f21c_summary.get("seed_surface_rows"),
        "handoff_candidate_rows": f21c_summary.get("handoff_candidate_rows"),
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
            artifact_identity(F21B_SUMMARY),
            artifact_identity(F21C_SUMMARY),
            artifact_identity(F21C_CANDIDATES),
            artifact_identity(GROK_PACKET / "clean_output.md"),
            artifact_identity(REPORT_PATH),
            artifact_identity(GROK_RECEIPT_PATH),
            artifact_identity(GATE_AUDIT_PATH),
        ],
        "results": {
            "cross_split": {
                "closeout": final["judgment"],
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "runtime_blocker": final["runtime_blocker"],
                "onnx_blocker": final["onnx_blocker"],
            },
            "report_refs": [{"role": "stage_closeout_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier21d_closeout_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
    }


def report_text(final: dict[str, Any]) -> str:
    b = final["f21b_preserved_detail"]
    c = final["f21c_preserved_detail"]
    return f"""# Frontier21D Lifecycle Closeout Report(전선21D 생명주기 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): Frontier21(전선21)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): low-DD lifecycle shapes(낮은 손실폭 생명주기 모양)는 위험 억제 참고 단서로 남기고, lifecycle/DD/density repair(생명주기/손실폭/빈도 수리) 단독으로 PF edge(수익 팩터 우위)를 만들 수 있다는 가정은 막습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

- F21B(전선21B): `{b['profile_id']}` validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{f21b.fmt(b['validation_profit_factor'])}/{f21b.fmt(b['validation_trades_per_day'])}/{f21b.fmt(b['validation_dd_risk_percent'])}` and `{f21b.fmt(b['oos_profit_factor'])}/{f21b.fmt(b['oos_trades_per_day'])}/{f21b.fmt(b['oos_dd_risk_percent'])}`. Meaning(의미): `{b['meaning']}`.
- F21C(전선21C): `{c['profile_id']}` validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{f21b.fmt(c['validation_profit_factor'])}/{f21b.fmt(c['validation_trades_per_day'])}/{f21b.fmt(c['validation_dd_risk_percent'])}` and `{f21b.fmt(c['oos_profit_factor'])}/{f21b.fmt(c['oos_trades_per_day'])}/{f21b.fmt(c['oos_dd_risk_percent'])}`. Meaning(의미): `{c['meaning']}`.

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Tier boundary(티어 경계): `{final['tier_boundary']}`

Grok closeout classification(그록 마감 분류): `{final['grok_closeout']['classification']}`

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt_text(final: dict[str, Any]) -> str:
    grok = final["grok_closeout"]
    return f"""# Frontier21D Grok Closeout Receipt(전선21D 그록 마감 영수증)

Trigger reason(트리거 이유): stage closeout required by goal(목표가 요구한 단계 마감 검토).

Review size(검토 크기): small review(소규모 검토).

Prompt(프롬프트): `{grok['prompt']}`

Output(출력): `{grok['output']}`

Advice classification(조언 분류): `{grok['classification']}`.

Accepted advice(수용 조언): split F21B and F21C preserved clues(F21B/F21C 보존 단서 분리), record ONNX branch unattempted(ONNX 분기 미개시 기록), state Tier A only boundary(Tier A 전용 경계 명시).

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Final Codex direction(최종 코덱스 방향): close as preserved_clue + negative_memory(보존 단서 + 부정 기억으로 마감).
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier21D Gate Audit(전선21D 게이트 감사)

- closeout_gate(마감 게이트): `{final['judgment']}` with report(보고서) `{REPORT_PATH.as_posix()}`
- external_review_packet(외부 검토 묶음): `{GROK_PACKET.as_posix()}`
- kpi_contract_audit(KPI 계약 감사): F21B/F21C final summaries and candidate summaries(F21B/F21C 최종 요약과 후보 요약)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    c = final["f21c_preserved_detail"]
    return f"""# Frontier21 Preserved Clue(전선21 보존 단서)

Preserved clue(보존 단서): `{final['preserved_clue']}`

Evidence(근거): F21C best repair(전선21C 최상 수리) `{c['profile_id']}` produced validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{f21b.fmt(c['validation_profit_factor'])}/{f21b.fmt(c['validation_trades_per_day'])}/{f21b.fmt(c['validation_dd_risk_percent'])}` and `{f21b.fmt(c['oos_profit_factor'])}/{f21b.fmt(c['oos_trades_per_day'])}/{f21b.fmt(c['oos_dd_risk_percent'])}`.

Boundary(경계): risk containment reference only(위험 억제 참고 전용). No PF edge claim(수익 팩터 우위 주장 없음), no handoff(인계 없음), no runtime authority(런타임 권위 없음).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier21 Negative Memory(전선21 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Why failed(실패 이유): F21C(전선21C)는 density(빈도)와 DD(손실폭)를 맞췄지만 best OOS PF(최상 표본외 수익 팩터)가 `1.079`로 seed floor(씨앗 바닥) `1.2`보다 낮았고 seed/handoff(씨앗/인계)는 `0/0`이었습니다.

Runtime blocker(런타임 차단): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`

Do not repeat(반복 금지): fixed F20 seed(고정 F20 씨앗)에 lifecycle/density repair(생명주기/빈도 수리)만 더 얹는 방식으로 PF 부족을 반복 수리하지 않습니다.

Reopen condition(재개 조건): new PF edge source(새 수익 팩터 우위 원천)가 생기고 F21 low-DD lifecycle shape(낮은 손실폭 생명주기 모양)를 risk containment reference(위험 억제 참고)로만 쓸 때.
"""


def selection_status_text(final: dict[str, Any]) -> str:
    return f"""# Frontier21 Selection Status(전선21 선택 상태)

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
        "primary_kpi": "f21c_scout=3;seed=0;handoff=0;oos_pf=1.079;oos_density=6.369565;oos_dd=3.233934",
        "guardrail_kpi": "no_wfo_no_mt5_no_onnx_no_authority(WFO/MT5/ONNX/권위 없음)",
        "external_verification_status": final["runtime_blocker"],
        "notes": f"{final['preserved_clue']};{final['negative_memory']};{final['onnx_blocker']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }
    tier_b = {**primary, "ledger_row_id": f"{RUN_ID}__tier_b_missing_required", "subrun_id": f"{RUN_ID}__tier_b_missing_required", "record_view": "Tier B separate(티어 B 분리)", "tier_scope": "Tier B(티어 B)", "kpi_scope": "missing_required(필수 누락)", "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)", "guardrail_kpi": "no_tier_b_claim(티어 B 주장 없음)", "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)"}
    combined = {**primary, "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope", "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope", "record_view": "Tier A+B combined(티어 A+B 합산)", "tier_scope": "Tier A+B(티어 A+B)", "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)", "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)", "guardrail_kpi": "no_synthetic_combined_claim(합성 합산 주장 없음)", "notes": "Combined record blocked by missing Tier B source(Tier B 원천 누락으로 합산 기록 차단)"}
    return [primary, tier_b, combined]


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: {final['negative_memory']}. Preserved clue(보존 단서): `{final['preserved_clue']}`. "
        f"Runtime blocker(런타임 차단): `{final['runtime_blocker']}`. ONNX blocker(ONNX 차단): `{final['onnx_blocker']}`. "
        "Effect(효과): 다음 전선은 PF edge source(수익 팩터 우위 원천)를 새로 만들어야 하며 F21 생명주기 모양은 위험 억제 참고로만 씁니다.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR21-F20-SEED-LIFECYCLE-DD-CONTAINMENT-ONNX-SCOUT`: `{RUN_ID}` closes Frontier21(전선21) as preserved clue + negative memory(보존 단서 + 부정 기억). "
        "Effect(효과): low-DD lifecycle(낮은 손실폭 생명주기)은 보존하되 PF edge(수익 팩터 우위) 부족을 반복하지 않습니다.\n"
    )


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier21(전선21) as preserved clue + negative memory(보존 단서 + 부정 기억). "
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

Action(행동): Frontier21(전선21)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): F21 low-DD lifecycle shape(전선21 낮은 손실폭 생명주기 모양)는 위험 억제 참고 단서로 남기고, lifecycle/density repair(생명주기/빈도 수리) 단독으로 PF edge(수익 팩터 우위)를 만들 수 있다는 반복은 막습니다.

Runtime probe blocker(런타임 탐침 차단 사유): `{final['runtime_blocker']}`

ONNX blocker(ONNX 차단 사유): `{final['onnx_blocker']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path.exists() else "pending_or_missing(대기 또는 누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
