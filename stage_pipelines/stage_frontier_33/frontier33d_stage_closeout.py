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
from stage_pipelines.stage_frontier_33 import frontier33c_path_native_exit_label_repair_or_closeout_decision as f33c


STAGE_ID = f33c.STAGE_ID
RUN_ID = "frontier33D_stage_closeout_path_native_exit_label_v1"
RUN_NUMBER = "frontier33D"
PARENT_RUN_ID = f33c.RUN_ID
NEXT_STAGE_ID = "stage_frontier_34__path_native_short_scout_dd_compression_state_gate_for_seed_surface_onnx_scout"
NEXT_RUN_ID = "frontier34A_stage_open_path_native_short_scout_dd_compression_state_gate_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_grok_closeout_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_local_verification.md"
REQUIRED_GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_33/frontier33d_stage_closeout.py")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_33_path_native_exit_label_closeout.md")

F33A_SUMMARY = STAGE_ROOT / "02_runs" / f33c.f33b.f33a.RUN_ID / "stage_open_summary.json"
F33B_SUMMARY = STAGE_ROOT / "02_runs" / f33c.f33b.RUN_ID / "final_summary.json"
F33B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f33c.f33b.RUN_ID / "path_native_candidate_summary.csv"
F33C_SUMMARY = STAGE_ROOT / "02_runs" / f33c.RUN_ID / "final_summary.json"
F33C_REPAIR_SUMMARY = STAGE_ROOT / "02_runs" / f33c.RUN_ID / "repair_candidate_summary.csv"
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier33_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

STATUS = "closed_preserved_clue_negative_memory_path_native_exit_label_scout_only_no_runtime_authority"
JUDGMENT = "preserved_clue_negative_memory(F33 path-native MFE/MAE scout only no seed/runtime)"
PRESERVED_CLUE = (
    "f33_short_path_native_first_hit_scout_created_density_7_to_8_oos_dd_under_10_reference_only_"
    "validation_dd_13_to_15_limits_seed_claim"
)
NEGATIVE_MEMORY = (
    "f33_path_native_mfe_mae_first_hit_repair_failed_to_reach_seed_or_runtime_candidate_"
    "under_train_only_threshold_lock"
)


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    f33a_summary = read_json(F33A_SUMMARY)
    f33b_summary = read_json(F33B_SUMMARY)
    f33c_summary = read_json(F33C_SUMMARY)
    b_candidates = pd.read_csv(io_path(F33B_CANDIDATE_SUMMARY))
    c_candidates = pd.read_csv(io_path(F33C_REPAIR_SUMMARY))
    grok = read_grok_packet(GROK_PACKET)
    local = local_verification(f33a_summary, f33b_summary, f33c_summary, b_candidates, c_candidates, grok)
    if local["judgment"] != "pass_closeout_ready_preserved_clue_negative_memory":
        raise RuntimeError(f"Frontier33D local verification failed: {json.dumps(local, ensure_ascii=False)}")
    final = build_final(created_at, f33a_summary, f33b_summary, f33c_summary, b_candidates, c_candidates, grok, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "closeout_class": final["closeout_class"],
        "preserved_clue": final["preserved_clue"],
        "negative_memory": final["negative_memory"],
        "runtime_probe_status": final["runtime_probe_status"],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def normalize_grok_markdown() -> None:
    for name in ("input_prompt.md", "prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    lowered = output.lower()
    accepted = (
        ("verdict:** accepted" in lowered or "verdict: accepted" in lowered)
        and ("closeout_class_ok:** yes" in lowered or "closeout_class_ok: yes" in lowered)
        and ("preserved_clue_ok:** yes" in lowered or "preserved_clue_ok: yes" in lowered)
        and ("negative_memory_ok:** yes" in lowered or "negative_memory_ok: yes" in lowered)
        and ("runtime_probe_boundary_ok:** yes" in lowered or "runtime_probe_boundary_ok: yes" in lowered)
        and ("invalid_or_blocked_instead:** no" in lowered or "invalid_or_blocked_instead: no" in lowered)
    )
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
        "classification": "accepted_closeout_preserved_clue_negative_memory_with_oos_only_clue_caveat" if accepted else "needs_local_verification",
        "accepted": accepted,
        "output_excerpt": output[:3600],
    }


def local_verification(
    f33a_summary: dict[str, Any],
    f33b_summary: dict[str, Any],
    f33c_summary: dict[str, Any],
    b_candidates: pd.DataFrame,
    c_candidates: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    b_scout = b_candidates.loc[b_candidates["path_scout_clue_flag"].astype(bool)]
    c_scout = c_candidates.loc[c_candidates["path_scout_clue_flag"].astype(bool)]
    best_c = dict(c_candidates.iloc[0]) if not c_candidates.empty else {}
    checks = {
        "workspace_current_frontier33c_or_33d": f"current_stage_id: {STAGE_ID}" in workspace
        and (f"current_run_id: {PARENT_RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace),
        "workspace_next_frontier33d_or_frontier34a": f"next_run_id: {RUN_ID}" in workspace or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f33a_opened_after_grok": str(f33a_summary.get("grok", {}).get("classification", "")).startswith("accepted"),
        "f33b_scout_no_seed_runtime": int(f33b_summary.get("path_scout_clue_rows", -1)) == 4
        and int(f33b_summary.get("path_seed_surface_rows", -1)) == 0
        and int(f33b_summary.get("runtime_probe_candidate_rows", -1)) == 0,
        "f33c_repair_no_seed_runtime": int(f33c_summary.get("repair_scout_clue_rows", -1)) == 76
        and int(f33c_summary.get("repair_seed_surface_rows", -1)) == 0
        and int(f33c_summary.get("repair_runtime_candidate_rows", -1)) == 0,
        "scout_rows_exist": len(b_scout) == 4 and len(c_scout) == 76,
        "best_repair_validation_dd_not_seed": safe_float(best_c.get("validation_dd_risk")) > 10.0
        and safe_float(best_c.get("validation_profit_factor")) < 1.20,
        "best_repair_oos_dd_under_10": safe_float(best_c.get("oos_dd_risk")) < 10.0,
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepted_closeout": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_ready_preserved_clue_negative_memory" if all(checks.values()) else "needs_manual_review",
        "best_repair_candidate": json_ready(best_c),
        "grok_caveat": "Preserved clue is OOS DD under 10 only; validation DD remains 13-15% and blocks seed/runtime.",
    }


def build_final(
    created_at: str,
    f33a_summary: dict[str, Any],
    f33b_summary: dict[str, Any],
    f33c_summary: dict[str, Any],
    b_candidates: pd.DataFrame,
    c_candidates: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    best_b = dict(b_candidates.iloc[0]) if not b_candidates.empty else {}
    best_c = dict(c_candidates.iloc[0]) if not c_candidates.empty else {}
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
        "closeout_class": "preserved_clue_negative_memory",
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "f33a": {"run_id": f33a_summary.get("run_id"), "grok": f33a_summary.get("grok", {}).get("classification")},
        "f33b": {
            "run_id": f33b_summary.get("run_id"),
            "condition_pool_rows": f33b_summary.get("condition_pool_rows"),
            "candidate_rows": f33b_summary.get("candidate_rows"),
            "path_scout_clue_rows": f33b_summary.get("path_scout_clue_rows"),
            "path_seed_surface_rows": f33b_summary.get("path_seed_surface_rows"),
            "runtime_probe_candidate_rows": f33b_summary.get("runtime_probe_candidate_rows"),
            "best_candidate": json_ready(best_b),
        },
        "f33c": {
            "run_id": f33c_summary.get("run_id"),
            "source_scout_rows": f33c_summary.get("source_scout_rows"),
            "repair_candidate_rows": f33c_summary.get("repair_candidate_rows"),
            "repair_scout_clue_rows": f33c_summary.get("repair_scout_clue_rows"),
            "repair_seed_surface_rows": f33c_summary.get("repair_seed_surface_rows"),
            "repair_runtime_candidate_rows": f33c_summary.get("repair_runtime_candidate_rows"),
            "best_repair_candidate": json_ready(best_c),
        },
        "grok": grok,
        "local_verification": local,
        "runtime_probe_status": "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f33c_bounded_repair",
        "result_boundary": "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_closeout_summary.json", final)
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
        F33A_SUMMARY,
        F33B_SUMMARY,
        F33B_CANDIDATE_SUMMARY,
        F33C_SUMMARY,
        F33C_REPAIR_SUMMARY,
        GROK_PACKET / "prompt.md",
        GROK_PACKET / "clean_output.md",
        GROK_PACKET / "metadata.json",
        RUN_ROOT / "stage_closeout_summary.json",
        REPORT_PATH,
        GROK_RECEIPT_PATH,
        LOCAL_VERIFICATION_PATH,
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
        "closeout_class": final["closeout_class"],
        "runtime_claim_boundary": "stage_closeout_no_mt5_runtime_authority",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f33c.f33b.f33a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["f33c"]["best_repair_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "family": "publish_handoff(게시/인계)",
        "work_family": "publish_handoff(게시/인계)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"closeout={final['closeout_class']};repair_scout={final['f33c']['repair_scout_clue_rows']};seed=0;runtime_candidate=0;next={NEXT_RUN_ID}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={best.get('candidate_id','')};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "preserved_clue_negative_memory_no_runtime_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["f33c"]["best_repair_candidate"]
    return [{
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stage_closeout_no_runtime(단계 마감, 런타임 아님)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"repair_scout={final['f33c']['repair_scout_clue_rows']};seed=0;runtime_candidate=0;best_oos_pf={fmt(best.get('oos_profit_factor'))}",
        "guardrail_kpi": "preserved_clue_negative_memory_no_runtime_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"next={NEXT_RUN_ID};preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
    }]


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
        f"next_stage_id: {NEXT_STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def report_text(final: dict[str, Any]) -> str:
    best = final["f33c"]["best_repair_candidate"]
    return f"""# Frontier33D Stage Closeout Report(전선33D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Closeout class(마감 분류): `{final['closeout_class']}`

Action(행동): F33(전선33)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): path-native MFE/MAE first-hit surface(경로 기반 최대 유리/불리 이동 선터치 표면)는 scout clue(탐색 단서)로 보존하지만, seed/runtime candidate(씨앗/런타임 후보)는 없으므로 MT5 runtime probe(MT5 런타임 탐침)는 부적격으로 낮춥니다.

F33B path scout/seed/runtime(전선33B 경로 탐색/씨앗/런타임): `{final['f33b']['path_scout_clue_rows']}` / `{final['f33b']['path_seed_surface_rows']}` / `{final['f33b']['runtime_probe_candidate_rows']}`

F33C repair scout/seed/runtime(전선33C 수리 탐색/씨앗/런타임): `{final['f33c']['repair_scout_clue_rows']}` / `{final['f33c']['repair_seed_surface_rows']}` / `{final['f33c']['repair_runtime_candidate_rows']}`

Best repair validation PF/density/DD(최상 수리 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best repair OOS PF/density/DD(최상 수리 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Grok closeout classification(그록 마감 분류): `{final['grok']['classification']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(final: dict[str, Any]) -> str:
    grok = final["grok"]
    return f"""# Frontier33D Grok Closeout Receipt(전선33D 그록 마감 영수증)

Trigger reason(호출 이유): goal(목표)이 stage closeout(단계 마감)에 Grok second opinion(그록 2차 의견)을 요구합니다.

Review size(검토 크기): small review(소규모 검토)

Direction before Grok(그록 전 방향): F33(전선33)을 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫는 분류를 검토했습니다.

Prompt(프롬프트): `{grok['prompt']}`

Output(출력): `{grok['output']}`

Metadata(메타데이터): `{grok['metadata']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): closeout class(마감 분류), preserved clue(보존 단서), negative memory(부정 기억), runtime probe boundary(런타임 탐침 경계)를 수용했습니다.

Local verification(로컬 검증): `{final['local_verification']['judgment']}`

Grok caveat(그록 주의): preserved clue(보존 단서)는 OOS DD under 10%(표본외 손실폭 10% 미만)에 한정하고, validation DD 13~15%(검증 손실폭 13~15%)는 seed/runtime 차단 근거로 기록합니다.
"""


def local_verification_text(final: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in final["local_verification"]["checks"].items()]
    return f"""# Frontier33D Local Verification(전선33D 로컬 검증)

Judgment(판정): `{final['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 조언을 F33B/F33C summary(요약), candidate metrics(후보 지표), workspace state(작업공간 상태), forbidden claim guard(금지 주장 방어)와 대조한 뒤 closeout(마감)을 기록했습니다.
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier33 Required Gate Coverage Audit(전선33 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): stage open(단계 개방) and closeout(마감) Grok packets(그록 묶음) recorded(기록됨)
- scope_completion_gate(범위 완료 게이트): F33A/F33B/F33C/F33D artifacts(산출물) recorded(기록됨)
- kpi_contract_audit(KPI 계약 감사): F33B/F33C split metrics(분할 지표) and summaries(요약) recorded(기록됨)
- runtime_evidence_gate(런타임 근거 게이트): `{final['runtime_probe_status']}`
- closeout_gate(마감 게이트): preserved clue + negative memory(보존 단서 + 부정 기억)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    best = final["f33c"]["best_repair_candidate"]
    return f"""# Frontier33 Preserved Clue(전선33 보존 단서)

Clue(단서): `{final['preserved_clue']}`

Evidence(근거): best repair candidate(최상 수리 후보) `{best.get('candidate_id', '')}` reached validation/OOS density(검증/표본외 밀도) `{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('oos_trades_per_day'))}` per day and OOS DD(표본외 손실폭) `{fmt(best.get('oos_dd_risk'))}%`.

Boundary(경계): validation DD(검증 손실폭) `{fmt(best.get('validation_dd_risk'))}%` and PF below seed(씨앗 미만 수익 팩터) keep this reference-only(참조 전용) with no runtime authority(런타임 권위 없음).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier33 Negative Memory(전선33 부정 기억)

Negative memory(부정 기억): `{final['negative_memory']}`

Evidence(근거): F33B path scout/seed/runtime(전선33B 경로 탐색/씨앗/런타임) `{final['f33b']['path_scout_clue_rows']}/{final['f33b']['path_seed_surface_rows']}/{final['f33b']['runtime_probe_candidate_rows']}` and F33C repair scout/seed/runtime(전선33C 수리 탐색/씨앗/런타임) `{final['f33c']['repair_scout_clue_rows']}/{final['f33c']['repair_seed_surface_rows']}/{final['f33c']['repair_runtime_candidate_rows']}`.

Do-not-repeat(반복 금지): Do not keep widening only MFE/MAE threshold quantiles(최대 유리/불리 이동 분위수만 계속 확장 금지) without a new DD compression source(손실폭 압축 원천) or state gate(상태 게이트).
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier33 Selection Status(전선33 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage closeout(단계 마감): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Closeout class(마감 분류): `{final['closeout_class']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Close Frontier33 Path-Native Exit Label(전선33 경로 기반 청산 라벨 마감)

Date(날짜): 2026-06-14

Decision(결정): Close(마감) `{STAGE_ID}` as preserved clue + negative memory(보존 단서 + 부정 기억).

Effect(효과): path-native MFE/MAE first-hit scout(경로 기반 최대 유리/불리 이동 선터치 탐색)는 참고 단서로 보존하고, seed/runtime(씨앗/런타임) 실패는 다음 frontier stage(전선 단계)에서 DD compression state gate(손실폭 압축 상태 게이트) 가설로 넘깁니다.

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def current_working_state(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next stage(다음 단계): `{NEXT_STAGE_ID}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F33(전선33)을 path-native exit label(경로 기반 청산 라벨) preserved clue + negative memory(보존 단서 + 부정 기억)로 닫았습니다.

Effect(효과): short path-native first-hit scout clue(숏 경로 기반 선터치 탐색 단서)는 reference-only(참조 전용)로 보존하고, validation DD/PF(검증 손실폭/수익 팩터) 때문에 seed/runtime candidate(씨앗/런타임 후보)는 없다고 기록했습니다.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier33 path-native exit label(전선33 경로 기반 청산 라벨). "
        f"Effect(효과): preserved clue(보존 단서) + negative memory(부정 기억), next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR33-PATH-NATIVE-EXIT-LABEL-ONNX-SCOUT`: `{RUN_ID}` closed as preserved clue + negative memory(보존 단서 + 부정 기억). "
        "Effect(효과): 다음 질문은 short scout DD compression state gate(숏 탐색 단서 손실폭 압축 상태 게이트)입니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: {NEGATIVE_MEMORY}. Evidence(근거): F33C repair scout/seed/runtime(수리 탐색/씨앗/런타임) "
        f"{final['f33c']['repair_scout_clue_rows']}/{final['f33c']['repair_seed_surface_rows']}/{final['f33c']['repair_runtime_candidate_rows']}. "
        "Effect(효과): MFE/MAE quantile widening only(최대 유리/불리 이동 분위수 확장만)은 반복 금지입니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


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
