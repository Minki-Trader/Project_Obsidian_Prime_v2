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
from stage_pipelines.stage_frontier_27 import frontier27b_soft_joint_satisfaction_penalty_proxy_scout as f27b
from stage_pipelines.stage_frontier_27 import materialize_frontier27a_stage_open as f27a


STAGE_ID = f27a.STAGE_ID
RUN_ID = "frontier27C_soft_joint_satisfaction_penalty_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier27C"
PARENT_RUN_ID = f27b.RUN_ID
NEXT_RUN_ID = "frontier27D_stage_closeout_soft_joint_satisfaction_penalty_v1"
STATUS = "soft_penalty_repair_rejected_scout_only_no_seed_no_authority"
JUDGMENT = "preserved_clue_negative_memory_requires_stage_closeout_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_27/frontier27c_soft_penalty_repair_or_closeout_decision.py")

F27A_SUMMARY = STAGE_ROOT / "02_runs" / f27a.RUN_ID / "stage_open_summary.json"
F27B_SUMMARY = STAGE_ROOT / "02_runs" / f27b.RUN_ID / "final_summary.json"
F27B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f27b.RUN_ID / "soft_penalty_union_candidate_summary.csv"
F27B_REPEAT_AUDIT = STAGE_ROOT / "02_runs" / f27b.RUN_ID / "f24b_f25b_f26b_top10_nonrepeat_audit.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f27_soft_penalty_restored_union_surface_and_19_scout_rows_reference_only"
    "(F27 연성 페널티는 합집합 표면과 19개 탐색 행을 복원한 참조 전용 단서)"
)
NEGATIVE_MEMORY = (
    "under_f27_locked_soft_penalty_rank_seed_and_handoff_remained_zero"
    "(F27 잠금 연성 페널티 순위 아래 씨앗과 인계는 0개로 남음)"
)
NEXT_HYPOTHESIS_CLUE = (
    "train_only_stability_gap_penalty_for_forward_pf_dd_balance_reference_only"
    "(전방 PF/DD 균형을 위한 학습 전용 안정성 격차 페널티 참조 단서)"
)
REPAIR_DECISION = (
    "repair_not_run_because_allowed_train_only_filters_found_no_seed_and_heavier_coverage_probe_timed_out"
    "(허용된 학습 전용 필터는 씨앗을 찾지 못했고 더 무거운 구성 범위 탐침은 시간 초과되어 수리 미실행)"
)
RUNTIME_PROBE_STATUS = "out_of_scope_by_claim_no_handoff_candidate_after_f27b(전선27B 뒤 인계 후보 없어 주장 범위 밖)"


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F27A_SUMMARY)
    f27b_summary = read_json(F27B_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F27B_CANDIDATE_SUMMARY))
    repeat_audit = pd.read_csv(io_path(F27B_REPEAT_AUDIT))
    context = validate_context(stage_open, f27b_summary, candidate_summary)
    repair_audit = build_repair_audit(candidate_summary)
    final = build_final(created_at, stage_open, f27b_summary, candidate_summary, repeat_audit, repair_audit, context)
    write_outputs(final, repair_audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "repair_decision": final["repair_decision"],
        "preserved_clue": final["preserved_clue"],
        "negative_memory": final["negative_memory"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(stage_open: dict[str, Any], f27b_summary: dict[str, Any], candidate_summary: pd.DataFrame) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier27": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier27c": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == f27a.RUN_ID,
        "f27b_parent_matches": f27b_summary.get("run_id") == PARENT_RUN_ID,
        "f27b_scout_rows_positive": int(f27b_summary.get("scout_clue_rows", -1)) == 19,
        "f27b_seed_handoff_zero": int(f27b_summary.get("seed_surface_rows", -1)) == 0
        and int(f27b_summary.get("handoff_candidate_rows", -1)) == 0,
        "candidate_summary_present": not candidate_summary.empty,
        "candidate_summary_has_seed_zero": int(candidate_summary["seed_surface_flag"].astype(bool).sum()) == 0,
        "no_runtime_authority_claim": f27b_summary.get("claim_boundary", {}).get("runtime_authority") == "not_claimed(주장 없음)",
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier27C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_repair_audit(summary: pd.DataFrame) -> pd.DataFrame:
    frame = summary.copy()
    frame["fwd_min_pf"] = frame[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    frame["fwd_max_dd"] = frame[["validation_dd_risk", "oos_dd_risk"]].max(axis=1)
    frame["fwd_min_density"] = frame[["validation_trades_per_day", "oos_trades_per_day"]].min(axis=1)
    frame["fwd_max_density"] = frame[["validation_trades_per_day", "oos_trades_per_day"]].max(axis=1)
    rows: list[dict[str, Any]] = []
    filters = {
        "train_dd_le18_pf_ge1_25_density5_8": (frame.train_dd_risk <= 18)
        & (frame.train_profit_factor >= 1.25)
        & (frame.train_trades_per_day.between(5, 8)),
        "train_dd_le17_pf_ge1_25_density5_7": (frame.train_dd_risk <= 17)
        & (frame.train_profit_factor >= 1.25)
        & (frame.train_trades_per_day.between(5, 7)),
        "train_dd_le18_pf_ge1_30_density5_8": (frame.train_dd_risk <= 18)
        & (frame.train_profit_factor >= 1.30)
        & (frame.train_trades_per_day.between(5, 8)),
        "micro_dd_le18_density5_8": (frame.micro_train_dd_max <= 18)
        & (frame.train_trades_per_day.between(5, 8)),
    }
    for name, mask in filters.items():
        subset = frame.loc[mask].copy()
        rows.append({
            "repair_probe": name,
            "allowed_basis": "train_only_filter_scan(학습 전용 필터 점검)",
            "candidate_rows": int(len(subset)),
            "scout_rows": int(subset["scout_clue_flag"].astype(bool).sum()) if not subset.empty else 0,
            "seed_rows": int(subset["seed_surface_flag"].astype(bool).sum()) if not subset.empty else 0,
            "handoff_rows": int(subset["handoff_candidate_flag"].astype(bool).sum()) if not subset.empty else 0,
            "best_forward_min_pf": max_or_blank(subset["fwd_min_pf"]) if not subset.empty else "",
            "best_forward_max_dd_min": min_or_blank(subset["fwd_max_dd"]) if not subset.empty else "",
            "decision": "no_seed_found_do_not_repair(씨앗 없음, 수리하지 않음)",
        })
    rows.extend([
        {
            "repair_probe": "all80_pair_coverage_probe",
            "allowed_basis": "construction_coverage_probe(구성 범위 탐침)",
            "candidate_rows": "",
            "scout_rows": "",
            "seed_rows": "",
            "handoff_rows": "",
            "best_forward_min_pf": "",
            "best_forward_max_dd_min": "",
            "decision": "attempted_timeout_300s_no_result_no_claim(300초 시간 초과, 결과 주장 없음)",
        },
        {
            "repair_probe": "validation_oos_targeted_filter",
            "allowed_basis": "forbidden_path(금지 경로)",
            "candidate_rows": "",
            "scout_rows": "",
            "seed_rows": "",
            "handoff_rows": "",
            "best_forward_min_pf": "",
            "best_forward_max_dd_min": "",
            "decision": "rejected_invalid_validation_targeted_repair(검증 표적 수리라 무효로 거절)",
        },
        {
            "repair_probe": "f26_hard_gate_numeric_relaxation",
            "allowed_basis": "forbidden_path(금지 경로)",
            "candidate_rows": "",
            "scout_rows": "",
            "seed_rows": "",
            "handoff_rows": "",
            "best_forward_min_pf": "",
            "best_forward_max_dd_min": "",
            "decision": "rejected_invalid_repeats_f26_threshold_relaxation(F26 임계값 완화 반복이라 무효로 거절)",
        },
    ])
    return pd.DataFrame(rows)


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    f27b_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
    repair_audit: pd.DataFrame,
    context: dict[str, Any],
) -> dict[str, Any]:
    best = f27b_summary.get("best_soft_union", {})
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "context": context,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "f27b_summary": {
            "status": f27b_summary.get("status"),
            "judgment": f27b_summary.get("judgment"),
            "soft_micro_pool_rows": f27b_summary.get("soft_micro_pool_rows"),
            "soft_union_candidate_rows": f27b_summary.get("soft_union_candidate_rows"),
            "density_bridge_rows": f27b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f27b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f27b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f27b_summary.get("handoff_candidate_rows"),
            "best_soft_union_id": f27b_summary.get("best_soft_union_id"),
            "best_validation_pf": best.get("validation_profit_factor", ""),
            "best_oos_pf": best.get("oos_profit_factor", ""),
            "best_forward_max_dd": max(
                float(best.get("validation_dd_risk", math.nan)),
                float(best.get("oos_dd_risk", math.nan)),
            ) if best else "",
        },
        "candidate_summary_rows": int(len(candidate_summary)),
        "repeat_top10_f24": int(repeat_audit["in_f24b_top10"].sum()) if not repeat_audit.empty else 0,
        "repeat_top10_f25": int(repeat_audit["in_f25b_top10"].sum()) if not repeat_audit.empty else 0,
        "repeat_top10_f26": int(repeat_audit["in_f26b_top10_or_rejection"].sum()) if not repeat_audit.empty else 0,
        "repair_decision": REPAIR_DECISION,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "repair_audit_rows": int(len(repair_audit)),
        "result_boundary": "repair_or_closeout_decision_no_wfo_no_mt5_no_runtime_authority(수리 또는 마감 결정, WFO/MT5/런타임 권위 없음)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], repair_audit: pd.DataFrame) -> None:
    repair_audit.to_csv(io_path(RUN_ROOT / "repair_rejection_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, repair_audit))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F27B_SUMMARY,
        F27B_CANDIDATE_SUMMARY,
        F27B_REPEAT_AUDIT,
        RUN_ROOT / "repair_rejection_audit.csv",
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


def report_text(final: dict[str, Any], repair_audit: pd.DataFrame) -> str:
    table_rows = []
    for _, row in repair_audit.iterrows():
        table_rows.append(
            f"| `{row['repair_probe']}` | `{row['allowed_basis']}` | {row['candidate_rows']} | {row['scout_rows']} | {row['seed_rows']} | {row['handoff_rows']} | `{row['decision']}` |"
        )
    table = "\n".join(table_rows)
    return f"""# Frontier27C Repair or Closeout Decision(전선27C 수리 또는 마감 결정)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F27B(전선27B) scout-only surface(탐색 전용 표면)에 대해 train-only repair scan(학습 전용 수리 점검)을 했습니다.

Effect(효과): validation/OOS-targeted repair(검증/OOS 표적 수리)나 F26 threshold relaxation(F26 임계값 완화)을 쓰지 않고, 현재 stage(단계)를 preserved clue + negative memory(보존 단서+부정 기억)로 마감할 준비를 합니다.

F27B density/scout/seed/handoff(전선27B 빈도/탐색/씨앗/인계): `{final['f27b_summary']['density_bridge_rows']}` / `{final['f27b_summary']['scout_clue_rows']}` / `{final['f27b_summary']['seed_surface_rows']}` / `{final['f27b_summary']['handoff_candidate_rows']}`

Best F27B validation/OOS PF(최상 F27B 검증/OOS 수익 팩터): `{fmt(final['f27b_summary']['best_validation_pf'])}` / `{fmt(final['f27b_summary']['best_oos_pf'])}`

Repair decision(수리 결정): `{final['repair_decision']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Repair Audit(수리 감사)

| probe(탐침) | basis(근거) | rows(행) | scout(탐색) | seed(씨앗) | handoff(인계) | decision(결정) |
|---|---|---:|---:|---:|---:|---|
{table}

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier27C Gate Audit(전선27C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): repair decision(수리 결정) materialized(물질화) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- repair_policy_gate(수리 정책 게이트): validation/OOS-targeted repair(검증/OOS 표적 수리) rejected(거절)
- train_only_scan_gate(학습 전용 점검 게이트): repair audit rows(수리 감사 행) `{final['repair_audit_rows']}`
- timeout_probe_record_gate(시간 초과 탐침 기록 게이트): all80 pair coverage probe(전체80 쌍 구성 범위 탐침) recorded as no-claim timeout(결과 주장 없는 시간 초과로 기록)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier27 Selection Status(전선27 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest decision(최근 결정): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": f"repair={final['repair_decision']};preserved={final['preserved_clue']};negative={final['negative_memory']};next={NEXT_RUN_ID}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"density={final['f27b_summary']['density_bridge_rows']};scout={final['f27b_summary']['scout_clue_rows']};seed=0;handoff=0",
        "guardrail_kpi": "repair_not_run_no_wfo_no_mt5_no_authority(수리 미실행, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_repair_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_repair_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "repair_or_closeout_decision_not_runtime(수리 또는 마감 결정, 런타임 아님)",
        "scoreboard_lane": "repair_decision_proxy(수리 결정 프록시)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"scout={final['f27b_summary']['scout_clue_rows']};seed=0;handoff=0",
        "guardrail_kpi": "no_validation_targeted_repair_no_mt5_no_authority(검증 표적 수리 없음, MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"{final['preserved_clue']};{final['negative_memory']};{final['repair_decision']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` rejected Frontier27 repair and prepared closeout(전선27 수리 거절 및 마감 준비). "
        f"Effect(효과): preserved clue(보존 단서) `{final['preserved_clue']}` and negative memory(부정 기억) `{final['negative_memory']}` recorded.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR27-SOFT-JOINT-SATISFACTION-PENALTY-BRIDGE-UNION-ONNX-SCOUT`: `{RUN_ID}` rejected repair after scout-only surface(탐색 전용 표면 뒤 수리 거절). "
        f"Effect(효과): `{final['preserved_clue']}` and `{final['negative_memory']}` recorded before closeout(마감 전 기록).\n"
    )


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
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
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F27C(전선27C)가 F27B(전선27B) scout-only result(탐색 전용 결과)에 대한 repair decision(수리 결정)을 닫았습니다.

Effect(효과): allowed train-only filters(허용된 학습 전용 필터)는 seed(씨앗)를 만들지 못했고, validation/OOS-targeted repair(검증/OOS 표적 수리)와 F26 threshold relaxation(F26 임계값 완화)은 무효로 거절했습니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def max_or_blank(series: pd.Series) -> str:
    if series.empty:
        return ""
    return f"{float(series.max()):.6f}"


def min_or_blank(series: pd.Series) -> str:
    if series.empty:
        return ""
    return f"{float(series.min()):.6f}"


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
        return "inf"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
