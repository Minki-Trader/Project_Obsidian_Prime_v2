from __future__ import annotations

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
from stage_pipelines.stage_frontier_32 import frontier32b_executable_sl_tp_path_proxy_scout as f32b


STAGE_ID = f32b.STAGE_ID
RUN_ID = "frontier32C_executable_sl_tp_mapping_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier32C"
PARENT_RUN_ID = f32b.RUN_ID
NEXT_RUN_ID = "frontier32D_stage_closeout_executable_sl_tp_mapping_v1"
STATUS = "executable_sl_tp_mapping_closeout_queued_negative_memory_no_runtime_authority"
JUDGMENT = "negative_memory_return_space_surface_failed_raw_path_sl_tp_proxy"
REPAIR_DECISION = "close_without_repair_active_translation_axis_exhausted_no_path_proxy_scout"
CLOSEOUT_CLASS = "negative_memory"
RUNTIME_PROBE_STATUS = "runtime_probe_ineligible_no_path_proxy_candidate_after_f32b"
ONNX_BLOCKER = "onnx_unattempted_no_path_proxy_seed_or_runtime_candidate"
NEGATIVE_MEMORY = (
    "f32_return_space_handoff_surface_failed_executable_sl_tp_raw_path_proxy"
    "(F32 수익률 공간 인계 표면은 실행 가능한 손절/익절 원천 경로 프록시에서 실패)"
)
USEFUL_OBSERVATION = (
    "density_bridge_can_survive_without_edge_but_is_not_enough"
    "(밀도 연결은 살아남을 수 있지만 수익 우위 없이는 충분하지 않음)"
)
NEXT_HYPOTHESIS_CLUE = (
    "path_native_exit_label_or_mfe_mae_surface_instead_of_return_space_cap_translation"
    "(수익률 공간 한도 번역 대신 경로 기반 청산 라벨 또는 유리/불리 이동 표면)"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_32/frontier32c_executable_sl_tp_mapping_repair_or_closeout_decision.py")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier32_stage_closeout/small_review")
GROK_PROMPT_PATH = GROK_CLOSEOUT_PACKET / "input_prompt.md"

F32A_SUMMARY = STAGE_ROOT / "02_runs" / f32b.f32a.RUN_ID / "stage_open_summary.json"
F32B_SUMMARY = STAGE_ROOT / "02_runs" / f32b.RUN_ID / "final_summary.json"
F32B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f32b.RUN_ID / "path_candidate_summary.csv"
F32B_TOP_FORWARD = STAGE_ROOT / "02_runs" / f32b.RUN_ID / "top_path_forward_diagnostic.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    f32a_summary = read_json(F32A_SUMMARY)
    f32b_summary = read_json(F32B_SUMMARY)
    candidates = pd.read_csv(io_path(F32B_CANDIDATE_SUMMARY))
    top_forward = pd.read_csv(io_path(F32B_TOP_FORWARD))
    local = validate_context(f32a_summary, f32b_summary, candidates, top_forward)
    final = build_final(created_at, f32a_summary, f32b_summary, candidates, top_forward, local)
    write_outputs(final)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "repair_decision": final["repair_decision"],
        "closeout_class_preview": final["closeout_class_preview"],
        "runtime_probe_status": final["runtime_probe_status"],
        "next_run_id": NEXT_RUN_ID,
        "grok_prompt": GROK_PROMPT_PATH.as_posix(),
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", GROK_CLOSEOUT_PACKET):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(
    f32a_summary: dict[str, Any],
    f32b_summary: dict[str, Any],
    candidates: pd.DataFrame,
    top_forward: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    best = f32b_summary.get("best_path_candidate", {})
    checks = {
        "workspace_current_frontier32b_or_frontier32c": f"current_stage_id: {STAGE_ID}" in workspace
        and (f"current_run_id: {f32b.RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace),
        "workspace_next_frontier32c_or_frontier32d": f"next_run_id: {RUN_ID}" in workspace
        or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "stage_open_grok_accepted": f32a_summary.get("grok", {}).get("classification", "").startswith("accepted"),
        "stage_open_changed_variable_locked": f32a_summary.get("locks", {}).get("active_changed_variable")
        == "fixed_log_return_caps_to_price_path_sl_tp_representation",
        "f32b_queue_rows_sixteen": int(f32b_summary.get("queue_rows", -1)) == 16,
        "f32b_summary_rows_sixteen": int(f32b_summary.get("summary_rows", -1)) == 16,
        "candidate_summary_rows_match": len(candidates) == int(f32b_summary.get("summary_rows", -1)),
        "top_forward_rows_match": len(top_forward) == min(16, len(candidates)),
        "no_path_scout_rows": int(f32b_summary.get("path_scout_clue_rows", -1)) == 0,
        "no_path_seed_rows": int(f32b_summary.get("path_seed_surface_rows", -1)) == 0,
        "no_runtime_probe_candidate_rows": int(f32b_summary.get("runtime_probe_candidate_rows", -1)) == 0,
        "runtime_probe_ineligible": f32b_summary.get("runtime_probe_status") == RUNTIME_PROBE_STATUS,
        "best_validation_pf_below_scout": safe_float(best.get("validation_profit_factor")) < f32b.SCOUT_PF,
        "best_oos_pf_negative": safe_float(best.get("oos_profit_factor")) < 1.0,
        "best_oos_dd_above_seed_cap": safe_float(best.get("oos_dd_risk")) > f32b.SEED_DD_CAP,
        "all_runtime_flags_false": not bool(candidates["runtime_probe_candidate_flag"].astype(bool).any()),
        "all_seed_flags_false": not bool(candidates["path_seed_surface_flag"].astype(bool).any()),
        "claim_boundary_not_claimed": all(value == "not_claimed" for value in f32b_summary.get("claim_boundary", {}).values()),
    }
    return {
        "checks": checks,
        "judgment": "pass_closeout_decision_ready" if all(checks.values()) else "needs_manual_review",
    }


def build_final(
    created_at: str,
    f32a_summary: dict[str, Any],
    f32b_summary: dict[str, Any],
    candidates: pd.DataFrame,
    top_forward: pd.DataFrame,
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_closeout_decision_ready":
        raise RuntimeError(f"Frontier32C local checks failed: {json.dumps(local, ensure_ascii=False)}")
    best = f32b_summary.get("best_path_candidate", {})
    diagnosis = {
        "queue_rows": int(f32b_summary.get("queue_rows", 0)),
        "path_candidate_rows": int(f32b_summary.get("path_candidate_rows", 0)),
        "path_scout_clue_rows": int(f32b_summary.get("path_scout_clue_rows", 0)),
        "path_seed_surface_rows": int(f32b_summary.get("path_seed_surface_rows", 0)),
        "runtime_probe_candidate_rows": int(f32b_summary.get("runtime_probe_candidate_rows", 0)),
        "runtime_strict_candidate_rows": int(f32b_summary.get("runtime_strict_candidate_rows", 0)),
        "density_bridge_rows": int(candidates["path_density_bridge_flag"].astype(bool).sum()),
        "path_dual_positive_rows": int(candidates["forward_dual_positive_flag"].astype(bool).sum()),
        "top_forward_rows": int(len(top_forward)),
        "best_path_candidate_id": f32b_summary.get("best_path_candidate_id", ""),
        "best_source_f31_candidate_id": best.get("source_f31_candidate_id", ""),
        "best_validation_profit_factor": safe_float(best.get("validation_profit_factor")),
        "best_validation_trades_per_day": safe_float(best.get("validation_trades_per_day")),
        "best_validation_dd_risk": safe_float(best.get("validation_dd_risk")),
        "best_oos_profit_factor": safe_float(best.get("oos_profit_factor")),
        "best_oos_trades_per_day": safe_float(best.get("oos_trades_per_day")),
        "best_oos_dd_risk": safe_float(best.get("oos_dd_risk")),
        "best_forward_pf_retention": safe_float(best.get("f31_to_path_forward_pf_retention")),
        "best_forward_dd_delta": safe_float(best.get("f31_to_path_forward_dd_delta")),
    }
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "repair_decision": REPAIR_DECISION,
        "closeout_class_preview": CLOSEOUT_CLASS,
        "negative_memory": NEGATIVE_MEMORY,
        "useful_observation": USEFUL_OBSERVATION,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "onnx_blocker": ONNX_BLOCKER,
        "diagnosis": diagnosis,
        "f32a_summary": {
            "status": f32a_summary.get("status"),
            "judgment": f32a_summary.get("judgment"),
            "grok_classification": f32a_summary.get("grok", {}).get("classification"),
            "active_changed_variable": f32a_summary.get("locks", {}).get("active_changed_variable"),
            "alignment_p99_abs_delta": f32a_summary.get("alignment_audit", {}).get("p99_abs_delta"),
        },
        "f32b_summary": {
            "status": f32b_summary.get("status"),
            "judgment": f32b_summary.get("judgment"),
            "runtime_probe_status": f32b_summary.get("runtime_probe_status"),
            "result_boundary": f32b_summary.get("result_boundary"),
            "best_path_candidate": best,
        },
        "local_verification": local,
        "result_boundary": "repair_closeout_decision_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(GROK_PROMPT_PATH, grok_prompt(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F32A_SUMMARY,
        F32B_SUMMARY,
        F32B_CANDIDATE_SUMMARY,
        F32B_TOP_FORWARD,
        RUN_ROOT / "final_summary.json",
        REPORT_PATH,
        GATE_AUDIT_PATH,
        GROK_PROMPT_PATH,
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f32b.f32a.f31d.f31b.f31a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    d = final["diagnosis"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "runtime_backtest(런타임 백테스트)",
        "work_family": "runtime_backtest(런타임 백테스트)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"closeout_class={CLOSEOUT_CLASS};path_scout={d['path_scout_clue_rows']};seed={d['path_seed_surface_rows']};runtime_candidate={d['runtime_probe_candidate_rows']};next={NEXT_RUN_ID}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best_v_pf={fmt(d['best_validation_profit_factor'])};best_oos_pf={fmt(d['best_oos_profit_factor'])};best_oos_dd={fmt(d['best_oos_dd_risk'])}",
        "guardrail_kpi": "no_path_scout_no_seed_no_mt5_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    d = final["diagnosis"]
    return [{
        "ledger_row_id": f"{RUN_ID}__closeout_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__closeout_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "path_proxy_closeout_decision_no_mt5(경로 프록시 마감 결정, MT5 아님)",
        "scoreboard_lane": "closeout_decision(마감 결정)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"path_scout={d['path_scout_clue_rows']};seed={d['path_seed_surface_rows']};runtime_candidate={d['runtime_probe_candidate_rows']}",
        "guardrail_kpi": "negative_memory_no_runtime_probe_candidate",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "closeout_decision(마감 결정)",
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
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def report_text(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Frontier32C Repair Or Closeout Decision Report(전선32C 수리 또는 마감 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F32B(전선32B)의 executable SL/TP path proxy(실행 가능한 손절/익절 경로 프록시)를 수리 반복 없이 closeout(마감) 후보로 분류했습니다.

Effect(효과): fixed translation axis(고정 번역 축)에서 path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보)가 0/0/0이므로, 같은 수리를 되풀이하지 않고 negative memory(부정 기억)로 닫을 준비를 합니다.

Repair decision(수리 결정): `{final['repair_decision']}`

Closeout class preview(마감 분류 예고): `{final['closeout_class_preview']}`

Best path candidate(최상 경로 후보): `{d['best_path_candidate_id']}` from F31(전선31) `{d['best_source_f31_candidate_id']}`.

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(d['best_validation_profit_factor'])}` / `{fmt(d['best_validation_trades_per_day'])}` / `{fmt(d['best_validation_dd_risk'])}`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(d['best_oos_profit_factor'])}` / `{fmt(d['best_oos_trades_per_day'])}` / `{fmt(d['best_oos_dd_risk'])}`

Path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보): `{d['path_scout_clue_rows']}` / `{d['path_seed_surface_rows']}` / `{d['runtime_probe_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단 사유): `{final['onnx_blocker']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Useful observation(유용 관찰): `{final['useful_observation']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Next action(다음 행동): Grok closeout review(그록 마감 검토) 후 `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Frontier32C Gate Audit(전선32C 게이트 감사)

- f32a_stage_open_gate(F32A 단계 개방 게이트): `{F32A_SUMMARY.as_posix()}` read(읽음)
- f32b_path_proxy_gate(F32B 경로 프록시 게이트): `{F32B_SUMMARY.as_posix()}` read(읽음)
- path_candidate_gate(경로 후보 게이트): path/scout/seed/runtime(경로/탐색/씨앗/런타임) `{d['path_candidate_rows']}/{d['path_scout_clue_rows']}/{d['path_seed_surface_rows']}/{d['runtime_probe_candidate_rows']}`
- best_forward_gate(최상 전진 게이트): validation/OOS PF-DD(검증/표본외 수익 팩터-손실폭) `{fmt(d['best_validation_profit_factor'])}/{fmt(d['best_validation_dd_risk'])}` and `{fmt(d['best_oos_profit_factor'])}/{fmt(d['best_oos_dd_risk'])}`
- repair_cap_gate(수리 상한 게이트): same fixed translation axis(같은 고정 번역 축) repair(수리) 반복 없음
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- closeout_grok_gate(마감 그록 게이트): prompt(프롬프트) written(작성됨) `{GROK_PROMPT_PATH.as_posix()}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier32 Selection Status(전선32 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest decision(최근 결정): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Closeout class preview(마감 분류 예고): `{final['closeout_class_preview']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}` after Grok closeout review(그록 마감 검토 후).

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def grok_prompt(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Grok Review Request: Frontier32 Stage Closeout(그록 검토 요청: 전선32 단계 마감)

Codex direction before Grok(그록 전 코덱스 방향): close Frontier32(전선32)를 negative_memory(부정 기억)로 닫으려 합니다.

Current truth(현재 진실):
- F32A stage-open(단계 개방)은 Grok accepted(그록 수용) 후 fixed_log_return_caps_to_price_path_sl_tp_representation(고정 수익률 한도에서 가격 경로 손절/익절 표현으로 번역)을 유일한 changed variable(변경 변수)로 잠갔습니다.
- F32B path proxy(경로 프록시)는 fixed queue(고정 큐) 16개를 raw Bid OHLC(원천 매수호가 시가/고가/저가/종가)로 재측정했습니다.
- path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보)는 `{d['path_scout_clue_rows']}/{d['path_seed_surface_rows']}/{d['runtime_probe_candidate_rows']}`입니다.
- best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭)는 `{fmt(d['best_validation_profit_factor'])}/{fmt(d['best_validation_trades_per_day'])}/{fmt(d['best_validation_dd_risk'])}`입니다.
- best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭)는 `{fmt(d['best_oos_profit_factor'])}/{fmt(d['best_oos_trades_per_day'])}/{fmt(d['best_oos_dd_risk'])}`입니다.
- runtime_probe_status(런타임 탐침 상태)는 `{final['runtime_probe_status']}`입니다. MT5 runtime probe(MT5 런타임 탐침)는 후보가 없어 ineligible(부적격)입니다.
- completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

Proposed closeout(제안 마감):
- closeout_class(마감 분류): `{final['closeout_class_preview']}`
- negative_memory(부정 기억): `{final['negative_memory']}`
- useful_observation(유용 관찰): `{final['useful_observation']}`
- next_hypothesis_clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Output rule(출력 규칙): return only the following key lines(아래 키 줄만 반환). Do not add preface, repo inspection, tool notes, or narrative(머리말, 저장소 검사, 도구 메모, 서술을 추가하지 마세요).

Please answer with these exact keys(아래 키로 답해주세요):
- verdict: accepted / rejected / needs_local_verification(수용 / 거절 / 로컬 검증 필요)
- closeout_class_ok: yes/no(예/아니오)
- runtime_probe_status_ok: yes/no(예/아니오)
- mt5_deferral_ok: yes/no(예/아니오)
- negative_memory_ok: yes/no(예/아니오)
- next_hypothesis_ok: yes/no(예/아니오)
- claim_boundary_ok: yes/no(예/아니오)
- main_risk: one short sentence(짧은 한 문장)
"""


def current_working_state(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F32C(전선32C)는 F32B(전선32B) 결과를 closeout decision(마감 결정)으로 정리했습니다.

Effect(효과): path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보)가 `{d['path_scout_clue_rows']}/{d['path_seed_surface_rows']}/{d['runtime_probe_candidate_rows']}`라서 MT5 runtime probe(MT5 런타임 탐침)를 실행하지 않고, Grok closeout review(그록 마감 검토)를 거친 뒤 negative memory(부정 기억)로 닫을 준비를 합니다.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` queued Frontier32 closeout decision(전선32 마감 결정). "
        f"Effect(효과): path_scout={d['path_scout_clue_rows']}, seed={d['path_seed_surface_rows']}, "
        f"runtime_candidate={d['runtime_probe_candidate_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR32-EXECUTABLE-SLTP-MAPPING-ONNX-SCOUT`: `{RUN_ID}` prepared negative memory(부정 기억) "
        f"`{NEGATIVE_MEMORY}`. Effect(효과): next hypothesis clue(다음 가설 단서)는 `{NEXT_HYPOTHESIS_CLUE}`입니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": f32b.sha256_io(path) if path_exists(path) else "missing"}


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
