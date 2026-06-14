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
from stage_pipelines.stage_frontier_26 import frontier26b_joint_micro_satisfaction_proxy_scout as f26b
from stage_pipelines.stage_frontier_26 import materialize_frontier26a_stage_open as f26a


STAGE_ID = f26a.STAGE_ID
RUN_ID = "frontier26C_joint_micro_satisfaction_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier26C"
PARENT_RUN_ID = f26b.RUN_ID
NEXT_CLOSEOUT_RUN_ID = "frontier26D_stage_closeout_joint_micro_satisfaction_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_26/frontier26c_joint_micro_repair_or_closeout_decision.py")

F26A_SUMMARY = STAGE_ROOT / "02_runs" / f26a.RUN_ID / "stage_open_summary.json"
F26A_LOCK = STAGE_ROOT / "02_runs" / f26a.RUN_ID / "joint_micro_satisfaction_lock.json"
F26B_SUMMARY = STAGE_ROOT / "02_runs" / f26b.RUN_ID / "final_summary.json"
F26B_MICRO_AUDIT = STAGE_ROOT / "02_runs" / f26b.RUN_ID / "micro_joint_pass_audit.csv"
F26B_REJECTION_AUDIT = STAGE_ROOT / "02_runs" / f26b.RUN_ID / "joint_union_rejection_audit.csv"
F26B_REPORT = STAGE_ROOT / "03_reviews" / f"{f26b.RUN_ID}_report.md"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f26_joint_micro_gate_survivor_triplet_reference_only"
    "(F26 합동 미세 게이트 생존 3개 참조 전용)"
)
NEGATIVE_MEMORY = (
    "under_f26_locked_joint_micro_satisfaction_gate_collapsed_union_surface"
    "(F26 잠금 합동 미세 충족 게이트는 합집합 표면을 붕괴시킴)"
)
INVALID_SETUP = (
    "invalid_setup_joint_gate_left_three_passers_zero_valid_unions"
    "(무효 설정: 합동 게이트 통과 3개, 유효 합집합 0개)"
)
REPAIR_DECISION = (
    "repair_not_run_because_only_threshold_relaxation_could_create_unions"
    "(합집합을 만들려면 임계값 완화만 가능하므로 수리 미실행)"
)
NEXT_HYPOTHESIS_CLUE = (
    "soft_joint_satisfaction_penalty_instead_of_hard_component_gate_reference_only"
    "(경성 구성 게이트 대신 연성 합동 충족 페널티 참조 단서)"
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F26A_SUMMARY)
    lock = read_json(F26A_LOCK)
    f26b_summary = read_json(F26B_SUMMARY)
    micro_audit = pd.read_csv(io_path(F26B_MICRO_AUDIT))
    rejection_audit = pd.read_csv(io_path(F26B_REJECTION_AUDIT))
    context = validate_context(stage_open, lock, f26b_summary, micro_audit, rejection_audit)
    diagnosis = build_diagnosis(f26b_summary, micro_audit, rejection_audit)
    final = build_final(created_at, stage_open, lock, f26b_summary, context, diagnosis)
    write_outputs(final, rejection_audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "invalid_setup": final["invalid_setup"],
        "repair_decision": final["repair_decision"],
        "runtime_probe_status": final["runtime_probe_status"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    f26b_summary: dict[str, Any],
    micro_audit: pd.DataFrame,
    rejection_audit: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier26": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier26c": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches": stage_open.get("run_id") == f26a.RUN_ID,
        "lock_changed_variable_joint_micro": lock.get("locks", {}).get("changed_variable") == "joint_micro_satisfaction_before_bridge_union",
        "lock_no_repair_frontier26b": "no_repair_in_frontier26b" in lock.get("locks", {}),
        "f26b_parent_matches": f26b_summary.get("run_id") == PARENT_RUN_ID,
        "f26b_zero_union": int(f26b_summary.get("joint_union_candidate_rows", -1)) == 0,
        "f26b_zero_seed": int(f26b_summary.get("seed_surface_rows", -1)) == 0,
        "f26b_zero_handoff": int(f26b_summary.get("handoff_candidate_rows", -1)) == 0,
        "micro_audit_available": path_exists(F26B_MICRO_AUDIT) and not micro_audit.empty,
        "rejection_audit_available": path_exists(F26B_REJECTION_AUDIT) and not rejection_audit.empty,
        "f26b_report_available": path_exists(F26B_REPORT),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier26C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_diagnosis(f26b_summary: dict[str, Any], micro_audit: pd.DataFrame, rejection_audit: pd.DataFrame) -> dict[str, Any]:
    passers = micro_audit.loc[micro_audit["joint_micro_pass_flag"].map(as_bool)].copy()
    rejection = rejection_audit.copy()
    for column in ("train_profit_factor", "train_trades_per_day", "train_dd_risk", "train_overlap_ratio", "min_unique_density_contribution"):
        rejection[column] = pd.to_numeric(rejection[column], errors="coerce")
    failure_counts = rejection["failure_reason"].fillna("").value_counts().to_dict()
    closest = rejection.assign(
        density_gap=(f26b.UNION_MIN_DENSITY - rejection["train_trades_per_day"]).clip(lower=0.0),
        dd_gap=(rejection["train_dd_risk"] - f26b.UNION_MAX_DD).clip(lower=0.0),
        overlap_gap=(rejection["train_overlap_ratio"] - f26b.MAX_OVERLAP_RATIO).clip(lower=0.0),
    ).sort_values(["dd_gap", "density_gap", "overlap_gap"]).head(1)
    closest_row = dict(closest.iloc[0]) if not closest.empty else {}
    return {
        "micro_pocket_rows": int(f26b_summary.get("micro_pocket_rows", 0)),
        "joint_micro_pass_rows": int(f26b_summary.get("joint_micro_pass_rows", 0)),
        "joint_union_attempt_rows": int(f26b_summary.get("joint_union_attempt_rows", len(rejection))),
        "joint_union_candidate_rows": int(f26b_summary.get("joint_union_candidate_rows", 0)),
        "density_bridge_rows": int(f26b_summary.get("density_bridge_rows", 0)),
        "scout_clue_rows": int(f26b_summary.get("scout_clue_rows", 0)),
        "seed_surface_rows": int(f26b_summary.get("seed_surface_rows", 0)),
        "handoff_candidate_rows": int(f26b_summary.get("handoff_candidate_rows", 0)),
        "failure_counts": failure_counts,
        "passer_micro_ids": "|".join(str(value) for value in passers["micro_id"].tolist()),
        "closest_union_near_miss": json_ready(closest_row),
        "decision_reason": (
            "The locked joint micro gate left only three passers. All four possible pair/triple unions failed the locked union gate: "
            "three pairs were below the 5/day density floor and above the 16% train DD cap, while the triple exceeded the train DD cap and overlap cap. "
            "Creating a union would require relaxing the locked density, DD, or overlap contract, so repair is rejected and the setup closes invalid."
            "(잠긴 합동 미세 게이트는 통과 3개만 남겼습니다. 가능한 쌍/삼중 합집합 4개는 모두 잠긴 합집합 게이트를 실패했습니다. "
            "쌍 3개는 일 5회 빈도 하한 미만이면서 학습 손실폭 16% 상한을 넘었고, 삼중은 손실폭 상한과 중복 상한을 넘었습니다. "
            "합집합을 만들려면 빈도/손실폭/중복 계약을 완화해야 하므로 수리를 거절하고 무효 설정으로 닫습니다.)"
        ),
    }


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    f26b_summary: dict[str, Any],
    context: dict[str, Any],
    diagnosis: dict[str, Any],
) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_CLOSEOUT_RUN_ID,
        "status": "joint_micro_repair_rejected_invalid_setup_no_union_no_authority",
        "judgment": "invalid_setup_requires_stage_closeout_no_authority",
        "invalid_setup": INVALID_SETUP,
        "repair_decision": REPAIR_DECISION,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "context": context,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "lock_summary": {
            "changed_variable": lock.get("locks", {}).get("changed_variable"),
            "forward_splits": lock.get("locks", {}).get("forward_splits"),
            "no_repair_in_frontier26b": lock.get("locks", {}).get("no_repair_in_frontier26b"),
            "micro_gate_contract": lock.get("locks", {}).get("micro_gate_contract"),
            "union_gate_contract": lock.get("locks", {}).get("union_gate_contract"),
        },
        "f26b_counts": {
            "micro_pocket_rows": f26b_summary.get("micro_pocket_rows"),
            "joint_micro_pass_rows": f26b_summary.get("joint_micro_pass_rows"),
            "joint_union_attempt_rows": f26b_summary.get("joint_union_attempt_rows"),
            "joint_union_candidate_rows": f26b_summary.get("joint_union_candidate_rows"),
            "density_bridge_rows": f26b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f26b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f26b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f26b_summary.get("handoff_candidate_rows"),
        },
        "diagnosis": diagnosis,
        "result_boundary": (
            "repair_or_closeout_decision_invalid_setup_no_wfo_no_mt5_no_runtime_authority"
            "(수리 또는 마감 결정 무효 설정, WFO/MT5/런타임 권위 없음)"
        ),
        "runtime_probe_status": (
            "out_of_scope_by_claim_no_handoff_candidate_after_f26c_invalid_setup_decision"
            "(F26C 무효 설정 결정 뒤 인계 후보 없어 주장 범위 밖)"
        ),
        "onnx_status": "unattempted_no_handoff_candidate(인계 후보 없어 미시도)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], rejection_audit: pd.DataFrame) -> None:
    rejection_audit.to_csv(io_path(RUN_ROOT / "repair_rejection_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, rejection_audit))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F26A_SUMMARY,
        F26A_LOCK,
        F26B_SUMMARY,
        F26B_MICRO_AUDIT,
        F26B_REJECTION_AUDIT,
        RUN_ROOT / "repair_rejection_audit.csv",
        RUN_ROOT / "final_summary.json",
        REPORT_PATH,
        GATE_AUDIT_PATH,
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "decision": {
            "invalid_setup": final["invalid_setup"],
            "repair_decision": final["repair_decision"],
            "preserved_clue": final["preserved_clue"],
            "negative_memory": final["negative_memory"],
            "runtime_probe_status": final["runtime_probe_status"],
            "onnx_status": final["onnx_status"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "compatibility": {"schema_version": "frontier26c_repair_or_closeout_decision_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], rejection_audit: pd.DataFrame) -> str:
    diagnosis = final["diagnosis"]
    rows = []
    for _, row in rejection_audit.head(10).iterrows():
        rows.append(
            f"| `{row['union_type']}` | `{row['micro_ids']}` | {fmt(row['train_profit_factor'])} | "
            f"{fmt(row['train_trades_per_day'])} | {fmt(row['train_dd_risk'])} | "
            f"{fmt(row['train_overlap_ratio'])} | `{row['failure_reason']}` |"
        )
    table = "\n".join(rows) if rows else "| none(없음) | | | | | | |"
    closest = diagnosis["closest_union_near_miss"]
    return f"""# Frontier26C Repair Or Closeout Decision Report(전선26C 수리 또는 마감 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F26B(전선26B)의 joint micro satisfaction before union(합집합 전 미세 구간 합동 충족) 결과를 repair decision(수리 결정)으로 분해했습니다.

Effect(효과): 유효 합집합 0개를 만들기 위해 gate relaxation(게이트 완화)을 하는 경로를 막고, invalid setup(무효 설정) 마감으로 이동합니다.

Invalid setup(무효 설정): `{final['invalid_setup']}`

Repair decision(수리 결정): `{final['repair_decision']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

F26B counts(전선26B 개수): micro/pass/attempt/union/density/scout/seed/handoff(미세/통과/시도/합집합/빈도/탐색/씨앗/인계) `{diagnosis['micro_pocket_rows']}` / `{diagnosis['joint_micro_pass_rows']}` / `{diagnosis['joint_union_attempt_rows']}` / `{diagnosis['joint_union_candidate_rows']}` / `{diagnosis['density_bridge_rows']}` / `{diagnosis['scout_clue_rows']}` / `{diagnosis['seed_surface_rows']}` / `{diagnosis['handoff_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Closest union near miss(가장 가까운 합집합 근접 실패): `{closest.get('micro_ids', '')}` with train PF/density/DD/overlap(학습 수익 팩터/빈도/손실폭/중복) `{fmt(closest.get('train_profit_factor'))}` / `{fmt(closest.get('train_trades_per_day'))}` / `{fmt(closest.get('train_dd_risk'))}` / `{fmt(closest.get('train_overlap_ratio'))}`.

## Union Rejection Audit(합집합 거절 감사)

Failure counts(실패 개수): `{json.dumps(diagnosis['failure_counts'], ensure_ascii=False, sort_keys=True)}`

| type(유형) | micro ids(미세 ID) | train PF | train density | train DD | overlap | failure reason(실패 이유) |
|---|---|---:|---:|---:|---:|---|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    diagnosis = final["diagnosis"]
    return f"""# Frontier26C Gate Audit(전선26C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): repair decision artifacts(수리 결정 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- parent_proxy_gate(부모 프록시 게이트): F26B(전선26B) pass/attempt/union(통과/시도/합집합) `{diagnosis['joint_micro_pass_rows']}` / `{diagnosis['joint_union_attempt_rows']}` / `{diagnosis['joint_union_candidate_rows']}` verified(검증)
- leakage_guard(누수 방어): repair(수리) not run(미실행) because it would relax locked train-only gates(잠긴 학습 전용 게이트를 완화해야 함)
- runtime_probe_gate(런타임 탐침 게이트): no handoff candidate(인계 후보 없음), MT5 runtime probe(MT5 런타임 탐침) out_of_scope_by_claim(주장 범위 밖)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier26 Selection Status(전선26 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest run(최근 실행): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Invalid setup(무효 설정): `{final['invalid_setup']}`

Repair decision(수리 결정): `{final['repair_decision']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    diagnosis = final["diagnosis"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"invalid={final['invalid_setup']};repair={final['repair_decision']};pass={diagnosis['joint_micro_pass_rows']};union={diagnosis['joint_union_candidate_rows']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"pass={diagnosis['joint_micro_pass_rows']};attempt={diagnosis['joint_union_attempt_rows']};union={diagnosis['joint_union_candidate_rows']}",
        "guardrail_kpi": "repair_not_run_no_wfo_no_mt5_no_authority(수리 미실행, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    diagnosis = final["diagnosis"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_repair_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_repair_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "repair_or_closeout_decision_invalid_setup_not_runtime(수리 또는 마감 결정 무효 설정, 런타임 아님)",
        "scoreboard_lane": "repair_decision_proxy(수리 결정 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"pass={diagnosis['joint_micro_pass_rows']};attempt={diagnosis['joint_union_attempt_rows']};union={diagnosis['joint_union_candidate_rows']}",
        "guardrail_kpi": "no_gate_relaxation_no_mt5_no_authority(게이트 완화 없음, MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"{final['invalid_setup']};{final['repair_decision']};{final['negative_memory']}",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시라 MT5 없음)",
        "notes": "Tier B source absent(Tier B 원천 없음)",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시라 MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    diagnosis = final["diagnosis"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` materialized F26 repair/closeout decision(F26 수리/마감 결정 물질화). "
        f"Effect(효과): joint pass/attempt/union(합동 통과/시도/합집합) {diagnosis['joint_micro_pass_rows']}/{diagnosis['joint_union_attempt_rows']}/{diagnosis['joint_union_candidate_rows']} closes as invalid setup(무효 설정) without gate relaxation(게이트 완화 없음).\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR26-JOINT-MICRO-SATISFACTION-BEFORE-UNION-ONNX-SCOUT`: `{RUN_ID}` rejected repair after invalid union collapse(무효 합집합 붕괴 뒤 수리 거절). "
        f"Effect(효과): `{final['invalid_setup']}` and `{final['negative_memory']}` recorded before stage closeout(단계 마감 전 기록).\n"
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
    diagnosis = final["diagnosis"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F26C(전선26C)가 F26B(전선26B) 결과를 repair decision(수리 결정)으로 닫았습니다.

Effect(효과): 유효 합집합 0개를 만들기 위한 gate relaxation(게이트 완화)을 하지 않고, F26(전선26)을 invalid setup closeout(무효 설정 마감)으로 이동합니다.

Invalid setup(무효 설정): `{final['invalid_setup']}`

Micro/pass/attempt/union(미세/통과/시도/합집합): `{diagnosis['micro_pocket_rows']}` / `{diagnosis['joint_micro_pass_rows']}` / `{diagnosis['joint_union_attempt_rows']}` / `{diagnosis['joint_union_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

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


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


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
