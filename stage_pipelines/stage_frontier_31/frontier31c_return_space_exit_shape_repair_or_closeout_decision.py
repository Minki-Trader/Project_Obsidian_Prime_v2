from __future__ import annotations

import csv
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
from stage_pipelines.stage_frontier_31 import frontier31b_return_space_exit_shape_proxy_scout as f31b


STAGE_ID = f31b.STAGE_ID
RUN_ID = "frontier31C_return_space_exit_shape_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier31C"
PARENT_RUN_ID = f31b.RUN_ID
NEXT_RUN_ID = "frontier31D_stage_closeout_return_space_exit_shape_v1"
STATUS = "return_space_exit_shape_executable_mapping_repair_queued_no_runtime_authority"
JUDGMENT = "preserved_handoff_surface_requires_executable_mapping_before_mt5"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_31/frontier31c_return_space_exit_shape_repair_or_closeout_decision.py")

F31A_SUMMARY = STAGE_ROOT / "02_runs" / f31b.f31a.RUN_ID / "stage_open_summary.json"
F31B_SUMMARY = STAGE_ROOT / "02_runs" / f31b.RUN_ID / "final_summary.json"
F31B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f31b.RUN_ID / "return_space_exit_shape_candidate_summary.csv"
F31B_TOP_FORWARD = STAGE_ROOT / "02_runs" / f31b.RUN_ID / "top_forward_readonly_diagnostic.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f31_return_space_exit_shape_created_realistic_handoff_surface_pf2_dd5_density6_reference_only"
    "(전선31 수익률 공간 청산 형태는 PF 2대, DD 5% 안팎, 밀도 6회대 현실적 인계 표면을 만들었지만 참조 전용)"
)
NEGATIVE_MEMORY = (
    "return_space_clip_without_intrabar_or_mt5_sl_tp_probe_cannot_claim_runtime_or_onnx"
    "(봉내 경로 또는 MT5 SL/TP 탐침 없는 수익률 클립은 런타임이나 ONNX를 주장할 수 없음)"
)
NEXT_HYPOTHESIS_CLUE = (
    "executable_sl_tp_mapping_for_return_space_exit_shape_handoff_surface_reference_only"
    "(수익률 공간 인계 표면을 실행 가능한 SL/TP 매핑으로 번역하는 다음 단서)"
)
RUNTIME_PROBE_STATUS = "runtime_probe_out_of_scope_by_claim_return_space_proxy_only_executable_mapping_not_validated"
ONNX_BLOCKER = "onnx_branch_unattempted_return_space_proxy_only_no_executable_runtime_mapping"


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    f31a_summary = read_json(F31A_SUMMARY)
    f31b_summary = read_json(F31B_SUMMARY)
    candidates = pd.read_csv(io_path(F31B_CANDIDATE_SUMMARY))
    queue = build_executable_mapping_queue(candidates)
    local = validate_context(f31a_summary, f31b_summary, candidates, queue)
    final = build_final(created_at, f31a_summary, f31b_summary, candidates, queue, local)
    write_outputs(final, queue)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "handoff_candidate_rows": final["diagnosis"]["handoff_candidate_rows"],
        "realistic_handoff_candidate_rows": final["diagnosis"]["realistic_handoff_candidate_rows"],
        "executable_handoff_candidate_rows": final["diagnosis"]["executable_handoff_candidate_rows"],
        "mapping_queue_rows": final["mapping_queue_rows"],
        "runtime_probe_status": final["runtime_probe_status"],
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def build_executable_mapping_queue(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = candidates.loc[
        candidates["handoff_candidate_flag"].astype(bool)
        & candidates["realistic_handoff_candidate_flag"].astype(bool)
        & ~candidates["executable_exit_representation_available"].astype(bool)
    ].copy()
    rows = rows.sort_values(["forward_read_score", "train_exit_shape_score"], ascending=[False, False]).reset_index(drop=True)
    keep = [
        "candidate_id",
        "f30_candidate_id",
        "source_stability_union_id",
        "source_soft_union_id",
        "micro_ids",
        "side_value",
        "side",
        "transform_family",
        "stop_cap_log_return",
        "take_cap_log_return",
        "loss_quantile",
        "take_quantile",
        "train_loss_capped_fraction",
        "train_win_capped_fraction",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk",
        "validation_max_loss_streak",
        "validation_equity_trend_r2",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk",
        "oos_max_loss_streak",
        "oos_equity_trend_r2",
        "forward_min_pf",
        "forward_max_dd",
        "forward_min_density",
        "forward_max_density",
        "forward_read_score",
        "train_exit_shape_score",
        "smoothness_proxy_pass",
    ]
    queue = rows[keep].copy()
    queue.insert(0, "queue_rank", range(1, len(queue) + 1))
    queue["mapping_type"] = "fixed_log_return_sl_tp_candidate"
    queue["executable_gap"] = "requires_intrabar_or_mt5_sl_tp_probe"
    queue["runtime_attempt_allowed_now"] = False
    queue["pre_expensive_grok_required"] = True
    queue["top_six_repair_seed"] = queue["queue_rank"] <= 6
    queue["next_action"] = "derive_symbol_point_sl_tp_and_run_micro_mt5_probe"
    return queue


def validate_context(
    f31a_summary: dict[str, Any],
    f31b_summary: dict[str, Any],
    candidates: pd.DataFrame,
    queue: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_frontier31b_or_frontier31c": f"current_run_id: {f31b.RUN_ID}" in workspace
        or f"current_run_id: {RUN_ID}" in workspace,
        "workspace_next_run_frontier31c_or_frontier31d": f"next_run_id: {RUN_ID}" in workspace
        or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f31a_grok_stage_open_accepted": f31a_summary.get("grok", {}).get("classification", "").startswith("accepted"),
        "f31a_lock_blocks_runtime_claim_from_clip": "claim_mt5_executable_behavior_from_return_space_clip_only"
        in f31a_summary.get("locks", {}).get("forbidden_primary_path", []),
        "f31b_handoff_surface_present": int(f31b_summary.get("handoff_candidate_rows", -1)) == 16,
        "f31b_realistic_handoff_rows_present": int(f31b_summary.get("realistic_handoff_candidate_rows", -1)) == 16,
        "f31b_executable_rows_zero": int(f31b_summary.get("executable_handoff_candidate_rows", -1)) == 0,
        "f31b_runtime_pending_executable_repair": f31b_summary.get("runtime_probe_status")
        == "runtime_probe_pending_executable_exit_representation_repair_before_mt5",
        "candidate_summary_rows_match": len(candidates) == int(f31b_summary.get("summary_rows", -1)),
        "queue_rows_match_realistic_handoff": len(queue) == int(f31b_summary.get("realistic_handoff_candidate_rows", -1)),
        "queue_all_requires_executable_probe": bool(len(queue))
        and queue["executable_gap"].astype(str).eq("requires_intrabar_or_mt5_sl_tp_probe").all(),
        "queue_all_blocks_runtime_now": bool(len(queue))
        and (~queue["runtime_attempt_allowed_now"].astype(bool)).all(),
        "best_forward_readonly_matches_queue_head": bool(len(queue))
        and str(queue.iloc[0]["candidate_id"]) == str(f31b_summary.get("best_forward_readonly_candidate_id", "")),
    }
    return {
        "checks": checks,
        "judgment": "pass_repair_queue_ready_for_closeout" if all(checks.values()) else "needs_manual_review",
    }


def build_final(
    created_at: str,
    f31a_summary: dict[str, Any],
    f31b_summary: dict[str, Any],
    candidates: pd.DataFrame,
    queue: pd.DataFrame,
    local: dict[str, Any],
) -> dict[str, Any]:
    if local["judgment"] != "pass_repair_queue_ready_for_closeout":
        raise RuntimeError(f"Frontier31C local checks failed: {json.dumps(local, ensure_ascii=False)}")
    best = f31b_summary.get("best_forward_readonly_candidate", {})
    diagnosis = {
        "candidate_rows": int(len(candidates)),
        "density_bridge_rows": int(f31b_summary.get("density_bridge_rows", 0)),
        "scout_clue_rows": int(f31b_summary.get("scout_clue_rows", 0)),
        "seed_surface_rows": int(f31b_summary.get("seed_surface_rows", 0)),
        "handoff_candidate_rows": int(f31b_summary.get("handoff_candidate_rows", 0)),
        "realistic_handoff_candidate_rows": int(f31b_summary.get("realistic_handoff_candidate_rows", 0)),
        "executable_handoff_candidate_rows": int(f31b_summary.get("executable_handoff_candidate_rows", 0)),
        "mapping_queue_rows": int(len(queue)),
        "top_six_repair_seed_rows": int(queue["top_six_repair_seed"].astype(bool).sum()) if len(queue) else 0,
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
        "repair_decision": "preserve_handoff_surface_and_queue_executable_mapping_repair",
        "closeout_class_preview": "preserved_clue",
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "diagnosis": diagnosis,
        "mapping_queue_rows": int(len(queue)),
        "top_mapping_queue_candidate_ids": queue.head(6)["candidate_id"].astype(str).tolist(),
        "best_forward_readonly_candidate_id": f31b_summary.get("best_forward_readonly_candidate_id"),
        "best_forward_readonly_candidate": best,
        "f31a_summary": {
            "status": f31a_summary.get("status"),
            "judgment": f31a_summary.get("judgment"),
            "grok_classification": f31a_summary.get("grok", {}).get("classification"),
            "active_changed_variable": f31a_summary.get("locks", {}).get("active_changed_variable"),
        },
        "f31b_summary": {
            "status": f31b_summary.get("status"),
            "judgment": f31b_summary.get("judgment"),
            "runtime_probe_status": f31b_summary.get("runtime_probe_status"),
            "result_boundary": f31b_summary.get("result_boundary"),
        },
        "local_verification": local,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "onnx_blocker": ONNX_BLOCKER,
        "result_boundary": "repair_queue_decision_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], queue: pd.DataFrame) -> None:
    queue.to_csv(io_path(RUN_ROOT / "executable_mapping_queue.csv"), index=False, encoding="utf-8-sig")
    queue.head(6).to_csv(io_path(RUN_ROOT / "top_executable_mapping_queue.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F31A_SUMMARY,
        F31B_SUMMARY,
        F31B_CANDIDATE_SUMMARY,
        F31B_TOP_FORWARD,
        RUN_ROOT / "executable_mapping_queue.csv",
        RUN_ROOT / "top_executable_mapping_queue.csv",
        RUN_ROOT / "final_summary.json",
        REPORT_PATH,
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
        "repair_decision": final["repair_decision"],
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f31b.f31a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    d = final["diagnosis"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"handoff={d['handoff_candidate_rows']};realistic={d['realistic_handoff_candidate_rows']};executable={d['executable_handoff_candidate_rows']};queue={d['mapping_queue_rows']};next={NEXT_RUN_ID}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"handoff={d['handoff_candidate_rows']};realistic={d['realistic_handoff_candidate_rows']};queue={d['mapping_queue_rows']}",
        "guardrail_kpi": "return_space_proxy_only_executable_mapping_required_no_mt5_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    d = final["diagnosis"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__repair_queue_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__repair_queue_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "proxy_repair_queue_no_runtime(프록시 수리 큐, 런타임 아님)",
        "scoreboard_lane": "repair_decision(수리 결정)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"handoff={d['handoff_candidate_rows']};realistic={d['realistic_handoff_candidate_rows']};queue={d['mapping_queue_rows']}",
        "guardrail_kpi": "executable_mapping_required_before_mt5_or_onnx",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "repair_decision(수리 결정)",
    }
    return [primary]


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
    best = final["best_forward_readonly_candidate"]
    return f"""# Frontier31C Repair Decision Report(전선31C 수리 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F31B(전선31B)의 return-space exit-shape proxy(수익률 공간 청산 형태 프록시)를 executable mapping queue(실행 매핑 큐)로 정리했습니다.

Effect(효과): handoff candidate(인계 후보) `{d['handoff_candidate_rows']}`개 중 realistic handoff candidate(현실적 인계 후보) `{d['realistic_handoff_candidate_rows']}`개를 보존하되, executable handoff candidate(실행 가능 인계 후보)가 `{d['executable_handoff_candidate_rows']}`개라 MT5 runtime probe(엠티5 런타임 탐침)는 실행하지 않습니다.

Best read-only forward candidate(최상 읽기 전용 전진 후보): `{final['best_forward_readonly_candidate_id']}` from F30(전선30) `{best.get('f30_candidate_id', '')}`.

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}`

Repair decision(수리 결정): `{final['repair_decision']}`

Mapping queue rows(매핑 큐 행): `{final['mapping_queue_rows']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX blocker(온엑스 차단 사유): `{final['onnx_blocker']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Frontier31C Gate Audit(전선31C 게이트 감사)

- proxy_source_gate(프록시 원천 게이트): `{F31B_CANDIDATE_SUMMARY.as_posix()}` read(읽음)
- handoff_surface_gate(인계 표면 게이트): handoff/realistic/executable(인계/현실적/실행 가능) `{d['handoff_candidate_rows']}/{d['realistic_handoff_candidate_rows']}/{d['executable_handoff_candidate_rows']}`
- executable_mapping_gate(실행 매핑 게이트): queue rows(큐 행) `{d['mapping_queue_rows']}`, top six repair seed(상위 6개 수리 씨앗) `{d['top_six_repair_seed_rows']}`
- leakage_guard(누수 방어): validation/OOS(검증/표본외)는 read-only diagnostics(읽기 전용 진단)로만 유지
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- onnx_gate(온엑스 게이트): `{final['onnx_blocker']}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Frontier31 Selection Status(전선31 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest decision(최근 결정): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Scout/seed/handoff(탐색/씨앗/인계): `{d['scout_clue_rows']}` / `{d['seed_surface_rows']}` / `{d['handoff_candidate_rows']}`

Realistic/executable handoff(현실적/실행 가능 인계): `{d['realistic_handoff_candidate_rows']}` / `{d['executable_handoff_candidate_rows']}`

Mapping queue(매핑 큐): `{final['mapping_queue_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
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

Action(행동): F31C(전선31C)는 F31B(전선31B)의 return-space handoff surface(수익률 공간 인계 표면)를 executable mapping queue(실행 매핑 큐)로 보존했습니다.

Effect(효과): realistic handoff candidate(현실적 인계 후보) `{d['realistic_handoff_candidate_rows']}`개가 남았지만 executable exit representation(실행 가능한 청산 표현)은 `{d['executable_handoff_candidate_rows']}`개라, 실제 MT5 runtime probe(엠티5 런타임 탐침)는 다음 executable SL/TP mapping(실행 가능한 손절/익절 매핑) 전까지 주장하지 않습니다.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` queued executable mapping repair(실행 매핑 수리 큐). "
        f"Effect(효과): handoff={d['handoff_candidate_rows']}, realistic={d['realistic_handoff_candidate_rows']}, executable={d['executable_handoff_candidate_rows']}, queue={d['mapping_queue_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR31-RETURN-SPACE-EXIT-SHAPE-PF-LIFT-ONNX-SCOUT`: `{RUN_ID}` preserved return-space handoff surface(수익률 공간 인계 표면) and queued executable SL/TP mapping(실행 가능한 손절/익절 매핑). "
        f"Effect(효과): preserved clue(보존 단서) `{PRESERVED_CLUE}`; negative memory(부정 기억) `{NEGATIVE_MEMORY}`.\n"
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


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
