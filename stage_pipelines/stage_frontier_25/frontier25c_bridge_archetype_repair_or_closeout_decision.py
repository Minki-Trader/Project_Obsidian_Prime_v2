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
from stage_pipelines.stage_frontier_25 import frontier25b_bridge_archetype_preselection_proxy_scout as f25b
from stage_pipelines.stage_frontier_25 import materialize_frontier25a_stage_open as f25a


STAGE_ID = f25a.STAGE_ID
RUN_ID = "frontier25C_bridge_archetype_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier25C"
PARENT_RUN_ID = f25b.RUN_ID
NEXT_CLOSEOUT_RUN_ID = "frontier25D_stage_closeout_bridge_archetype_preselection_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_25/frontier25c_bridge_archetype_repair_or_closeout_decision.py")

F25A_SUMMARY = STAGE_ROOT / "02_runs" / f25a.RUN_ID / "stage_open_summary.json"
F25A_LOCK = STAGE_ROOT / "02_runs" / f25a.RUN_ID / "bridge_archetype_preselection_lock.json"
F25B_SUMMARY = STAGE_ROOT / "02_runs" / f25b.RUN_ID / "final_summary.json"
F25B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f25b.RUN_ID / "archetype_candidate_summary.csv"
F25B_REPORT = STAGE_ROOT / "03_reviews" / f"{f25b.RUN_ID}_report.md"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SEED_PF = f25a.CRITERIA["seed_surface"]["pf"]
SEED_DD_CAP = f25a.CRITERIA["seed_surface"]["dd_cap"]
SCOUT_PF = f25a.CRITERIA["scout_clue"]["pf"]
HANDOFF_PF = f25a.CRITERIA["handoff_candidate"]["pf"]
HANDOFF_DD_CAP = f25a.CRITERIA["handoff_candidate"]["dd_cap"]

PRESERVED_CLUE = (
    "f25_dd_headroom_first_archetype_nonrepeat_scout_clue_reference_only"
    "(F25 손실폭 여유 우선 원형 비반복 탐색 단서 참조 전용)"
)
NEGATIVE_MEMORY = (
    "under_f25_locked_proxy_dd_headroom_first_preselection_did_not_break_seed_tradeoff"
    "(F25 잠금 프록시 아래 손실폭 여유 우선 사전 선택은 씨앗 상충을 깨지 못함)"
)
REPAIR_DECISION = (
    "capped_repair_not_run_to_avoid_validation_targeted_filtering"
    "(검증 표적 필터링을 피하기 위해 상한 수리를 실행하지 않음)"
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F25A_SUMMARY)
    lock = read_json(F25A_LOCK)
    f25b_summary = read_json(F25B_SUMMARY)
    candidates = pd.read_csv(io_path(F25B_CANDIDATE_SUMMARY))
    context = validate_context(stage_open, lock, f25b_summary, candidates)
    audit = build_repair_feasibility_audit(candidates)
    diagnosis = build_diagnosis(audit)
    final = build_final(created_at, stage_open, lock, f25b_summary, context, diagnosis, audit)
    write_outputs(final, audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "f25b_density_scout_seed_handoff": final["f25b_counts"],
        "pf_ready_dd_blocked_rows": final["diagnosis"]["pf_ready_dd_blocked_rows"],
        "dd_ready_pf_blocked_rows": final["diagnosis"]["dd_ready_pf_blocked_rows"],
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
    f25b_summary: dict[str, Any],
    candidates: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier25": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier25c": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches": stage_open.get("run_id") == f25a.RUN_ID,
        "f25b_parent_matches": f25b_summary.get("run_id") == PARENT_RUN_ID,
        "f25b_zero_seed": int(f25b_summary.get("seed_surface_rows", -1)) == 0,
        "f25b_zero_handoff": int(f25b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f25b_has_scout_clue": int(f25b_summary.get("scout_clue_rows", 0)) > 0,
        "f25b_candidate_table_available": path_exists(F25B_CANDIDATE_SUMMARY) and not candidates.empty,
        "lock_allows_f25c_optional_repair": "no_repair_in_frontier25b" in lock.get("locks", {}),
        "lock_no_validation_selection": lock.get("locks", {}).get("forward_splits") == "validation_oos_read_only",
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier25C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_repair_feasibility_audit(candidates: pd.DataFrame) -> pd.DataFrame:
    df = candidates.copy()
    for column in (
        "validation_profit_factor",
        "oos_profit_factor",
        "validation_trades_per_day",
        "oos_trades_per_day",
        "validation_dd_risk",
        "oos_dd_risk",
        "train_dd_risk",
        "train_profit_factor",
        "train_underwater_ratio",
        "train_max_loss_streak",
        "train_equity_trend_r2",
    ):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in ("density_bridge_flag", "scout_clue_flag", "seed_surface_flag", "handoff_candidate_flag"):
        df[column] = df[column].map(as_bool)
    df["forward_max_dd"] = df[["validation_dd_risk", "oos_dd_risk"]].max(axis=1)
    df["forward_min_pf"] = df[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    df["seed_pf_gap"] = (SEED_PF - df["forward_min_pf"]).clip(lower=0.0)
    df["seed_dd_gap"] = (df["forward_max_dd"] - SEED_DD_CAP).clip(lower=0.0)
    df["handoff_pf_gap"] = (HANDOFF_PF - df["forward_min_pf"]).clip(lower=0.0)
    df["handoff_dd_gap"] = (df["forward_max_dd"] - HANDOFF_DD_CAP).clip(lower=0.0)
    df["pf_ready_dd_blocked"] = (
        df["density_bridge_flag"]
        & (df["validation_profit_factor"] >= SEED_PF)
        & (df["oos_profit_factor"] >= SEED_PF)
        & (df["forward_max_dd"] > SEED_DD_CAP)
    )
    df["dd_ready_pf_blocked"] = (
        df["density_bridge_flag"]
        & (df["forward_max_dd"] <= SEED_DD_CAP)
        & (df["forward_min_pf"] < SEED_PF)
    )
    df["scout_not_seed"] = df["scout_clue_flag"] & ~df["seed_surface_flag"]
    df["seed_total_gap"] = df["seed_pf_gap"] + (df["seed_dd_gap"] / max(SEED_DD_CAP, 1.0))
    keep = [
        "archetype_id",
        "train_rank",
        "micro_key",
        "train_profit_factor",
        "train_trades_per_day",
        "train_dd_risk",
        "train_underwater_ratio",
        "train_max_loss_streak",
        "train_equity_trend_r2",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk",
        "forward_min_pf",
        "forward_max_dd",
        "seed_pf_gap",
        "seed_dd_gap",
        "handoff_pf_gap",
        "handoff_dd_gap",
        "density_bridge_flag",
        "scout_clue_flag",
        "seed_surface_flag",
        "handoff_candidate_flag",
        "pf_ready_dd_blocked",
        "dd_ready_pf_blocked",
        "scout_not_seed",
        "seed_total_gap",
    ]
    return df[keep].sort_values(["seed_surface_flag", "scout_clue_flag", "seed_total_gap"], ascending=[False, False, True])


def build_diagnosis(audit: pd.DataFrame) -> dict[str, Any]:
    density_count = int(audit["density_bridge_flag"].sum())
    scout_count = int(audit["scout_clue_flag"].sum())
    seed_count = int(audit["seed_surface_flag"].sum())
    handoff_count = int(audit["handoff_candidate_flag"].sum())
    pf_ready_dd_blocked = audit.loc[audit["pf_ready_dd_blocked"]]
    dd_ready_pf_blocked = audit.loc[audit["dd_ready_pf_blocked"]]
    scout_not_seed = audit.loc[audit["scout_not_seed"]]
    closest = dict(audit.iloc[0]) if not audit.empty else {}
    correlations = {}
    if len(audit) >= 3:
        for column in ("train_dd_risk", "train_underwater_ratio", "train_max_loss_streak", "train_equity_trend_r2"):
            correlations[f"{column}_to_forward_max_dd"] = safe_corr(audit[column], audit["forward_max_dd"])
    return {
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "pf_ready_dd_blocked_rows": int(len(pf_ready_dd_blocked)),
        "dd_ready_pf_blocked_rows": int(len(dd_ready_pf_blocked)),
        "scout_not_seed_rows": int(len(scout_not_seed)),
        "closest_seed_gap_archetype": json_ready(closest),
        "train_proxy_forward_dd_correlations": correlations,
        "decision_reason": (
            "F25B already found non-repeat scout rows, but seed-ready PF rows need validation DD relief "
            "while DD-ready rows need OOS PF lift. A new filter repair would have to target those "
            "forward diagnostics, so this capped repair path is closed without claiming authority."
            "(F25B는 비반복 탐색 행을 찾았지만, 씨앗 수익 팩터 충족 행은 검증 손실폭 완화가 필요하고 "
            "손실폭 충족 행은 표본외 수익 팩터 상승이 필요합니다. 새 필터 수리는 전방 진단을 표적으로 삼아야 "
            "하므로, 권위 주장 없이 이 상한 수리 경로를 닫습니다.)"
        ),
    }


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    f25b_summary: dict[str, Any],
    context: dict[str, Any],
    diagnosis: dict[str, Any],
    audit: pd.DataFrame,
) -> dict[str, Any]:
    best = dict(audit.iloc[0]) if not audit.empty else {}
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_CLOSEOUT_RUN_ID,
        "status": "bridge_archetype_repair_rejected_scout_clue_no_seed_proxy_no_authority",
        "judgment": "preserved_clue_negative_memory_requires_stage_closeout_no_authority",
        "repair_decision": REPAIR_DECISION,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "context": context,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "lock_summary": {
            "changed_variable": lock.get("locks", {}).get("changed_variable"),
            "forward_splits": lock.get("locks", {}).get("forward_splits"),
            "no_repair_in_frontier25b": lock.get("locks", {}).get("no_repair_in_frontier25b"),
        },
        "f25b_counts": {
            "density_bridge_rows": f25b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f25b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f25b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f25b_summary.get("handoff_candidate_rows"),
            "top10_f24b_overlap_count": f25b_summary.get("top10_f24b_overlap_count"),
        },
        "diagnosis": diagnosis,
        "best_gap_archetype_id": best.get("archetype_id", ""),
        "best_gap_archetype": json_ready(best),
        "result_boundary": (
            "repair_or_closeout_decision_proxy_no_wfo_no_mt5_no_runtime_authority"
            "(수리 또는 마감 결정 프록시, WFO/MT5/런타임 권위 없음)"
        ),
        "runtime_probe_status": (
            "out_of_scope_by_claim_no_handoff_candidate_after_f25c_repair_decision"
            "(F25C 수리 결정 뒤 인계 후보 없어 주장 범위 밖)"
        ),
        "onnx_status": "unattempted_no_handoff_candidate(인계 후보 없어 미시도)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], audit: pd.DataFrame) -> None:
    audit.to_csv(io_path(RUN_ROOT / "repair_feasibility_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, audit))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F25A_SUMMARY,
        F25A_LOCK,
        F25B_SUMMARY,
        F25B_CANDIDATE_SUMMARY,
        RUN_ROOT / "repair_feasibility_audit.csv",
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
        "artifacts": [artifact_identity(path) for path in artifacts],
        "decision": {
            "repair_decision": final["repair_decision"],
            "preserved_clue": final["preserved_clue"],
            "negative_memory": final["negative_memory"],
            "runtime_probe_status": final["runtime_probe_status"],
        },
        "compatibility": {"schema_version": "frontier25c_repair_or_closeout_decision_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], audit: pd.DataFrame) -> str:
    diagnosis = final["diagnosis"]
    best = final["best_gap_archetype"]
    rows = []
    for _, row in audit.head(10).iterrows():
        rows.append(
            f"| `{row['archetype_id']}` | `{row['micro_key']}` | {fmt(row['forward_min_pf'])} | "
            f"{fmt(row['forward_max_dd'])} | {fmt(row['seed_pf_gap'])} | {fmt(row['seed_dd_gap'])} | "
            f"{row['scout_clue_flag']} | {row['pf_ready_dd_blocked']} | {row['dd_ready_pf_blocked']} |"
        )
    table = "\n".join(rows) if rows else "| none(없음) | | | | | | | | |"
    return f"""# Frontier25C Repair Or Closeout Decision Report(전선25C 수리 또는 마감 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F25B(전선25B)의 train-only DD-headroom-first archetype preselection(학습 전용 손실폭 여유 우선 원형 사전 선택) 결과를 repair feasibility audit(수리 가능성 감사)로 분해했습니다.

Effect(효과): validation/OOS(검증/표본외)를 표적으로 삼는 새 필터 수리를 피하고, preserved clue(보존 단서)와 negative memory(부정 기억)를 closeout(마감)으로 넘깁니다.

F25B counts(전선25B 개수): density/scout/seed/handoff(빈도/탐색/씨앗/인계) `{final['f25b_counts']['density_bridge_rows']}` / `{final['f25b_counts']['scout_clue_rows']}` / `{final['f25b_counts']['seed_surface_rows']}` / `{final['f25b_counts']['handoff_candidate_rows']}`

Repair decision(수리 결정): `{final['repair_decision']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Closest seed-gap archetype(씨앗 간격 최저 원형): `{final['best_gap_archetype_id']}` with forward min PF/max DD(전방 최소 수익 팩터/최대 손실폭) `{fmt(best.get('forward_min_pf'))}` / `{fmt(best.get('forward_max_dd'))}`

## Bottleneck Audit(병목 감사)

- pf_ready_dd_blocked_rows(수익 팩터 충족, 손실폭 차단 행): `{diagnosis['pf_ready_dd_blocked_rows']}`
- dd_ready_pf_blocked_rows(손실폭 충족, 수익 팩터 차단 행): `{diagnosis['dd_ready_pf_blocked_rows']}`
- scout_not_seed_rows(탐색이나 씨앗 아님 행): `{diagnosis['scout_not_seed_rows']}`

| archetype(원형) | micro key(미세 키) | forward min PF(전방 최소 수익 팩터) | forward max DD(전방 최대 손실폭) | seed PF gap(씨앗 수익 팩터 간격) | seed DD gap(씨앗 손실폭 간격) | scout(탐색) | PF ready DD blocked(수익 팩터 충족 손실폭 차단) | DD ready PF blocked(손실폭 충족 수익 팩터 차단) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier25C Gate Audit(전선25C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): repair decision artifacts(수리 결정 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- parent_proxy_gate(부모 프록시 게이트): F25B(전선25B) zero seed/handoff(씨앗/인계 0개) verified(검증)
- leakage_guard(누수 방어): capped repair(상한 수리) not run(미실행) because it would target validation/OOS bottlenecks(검증/표본외 병목)
- runtime_probe_gate(런타임 탐침 게이트): no handoff candidate(인계 후보 없음), MT5 runtime probe(MT5 런타임 탐침) out_of_scope_by_claim(주장 범위 밖)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier25 Selection Status(전선25 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest run(최근 실행): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

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
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
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
        "primary_kpi": f"pf_ready_dd_blocked={final['diagnosis']['pf_ready_dd_blocked_rows']};dd_ready_pf_blocked={final['diagnosis']['dd_ready_pf_blocked_rows']}",
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
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"scout={final['f25b_counts']['scout_clue_rows']};seed={final['f25b_counts']['seed_surface_rows']};handoff={final['f25b_counts']['handoff_candidate_rows']}",
        "guardrail_kpi": "no_validation_targeted_repair_no_mt5_no_authority(검증 표적 수리 없음, MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"{final['preserved_clue']};{final['negative_memory']}",
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
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` materialized repair/closeout decision(수리/마감 결정 물질화). "
        f"Effect(효과): F25B scout clue(전선25B 탐색 단서)는 preserved(보존)하고 seed/handoff failure(씨앗/인계 실패)는 negative memory(부정 기억)로 closeout(마감) 이동.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR25-BRIDGE-ARCHETYPE-PRESELECTION-ONNX-SCOUT`: `{RUN_ID}` closed the optional repair path(선택 수리 경로 종료). "
        f"Effect(효과): `{final['preserved_clue']}` and `{final['negative_memory']}` recorded before stage closeout(단계 마감 전 기록).\n"
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

Action(행동): F25C(전선25C)가 F25B(전선25B) 결과를 repair feasibility audit(수리 가능성 감사)로 나눴습니다.

Effect(효과): validation/OOS(검증/표본외)를 표적으로 삼는 새 필터 수리를 피하고, F25(전선25)를 closeout(마감)으로 이동합니다.

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

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


def safe_corr(left: pd.Series, right: pd.Series) -> float:
    try:
        corr = float(pd.to_numeric(left, errors="coerce").corr(pd.to_numeric(right, errors="coerce")))
    except Exception:
        return 0.0
    return corr if math.isfinite(corr) else 0.0


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
