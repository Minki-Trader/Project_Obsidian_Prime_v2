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
from stage_pipelines.stage_frontier_28 import frontier28b_train_only_stability_gap_proxy_scout as f28b
from stage_pipelines.stage_frontier_28 import materialize_frontier28a_stage_open as f28a


STAGE_ID = f28a.STAGE_ID
RUN_ID = "frontier28C_stability_gap_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier28C"
PARENT_RUN_ID = f28b.RUN_ID
NEXT_RUN_ID = "frontier28D_stage_closeout_stability_gap_penalty_v1"
STATUS = "stability_gap_repair_rejected_scout_only_no_seed_no_authority"
JUDGMENT = "preserved_clue_negative_memory_requires_stage_closeout_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_28/frontier28c_stability_gap_repair_or_closeout_decision.py")

F28A_SUMMARY = STAGE_ROOT / "02_runs" / f28a.RUN_ID / "stage_open_summary.json"
F28A_LOCK = STAGE_ROOT / "02_runs" / f28a.RUN_ID / "stability_gap_penalty_lock.json"
F28B_SUMMARY = STAGE_ROOT / "02_runs" / f28b.RUN_ID / "final_summary.json"
F28B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f28b.RUN_ID / "stability_gap_candidate_summary.csv"
F28B_CHUNK_METRICS = STAGE_ROOT / "02_runs" / f28b.RUN_ID / "stability_gap_chunk_metrics.csv"
F28B_FORWARD_DIAGNOSTIC = STAGE_ROOT / "02_runs" / f28b.RUN_ID / "top_forward_readonly_diagnostic.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SEED_PF = f28b.SEED_PF
SEED_DD_CAP = f28b.SEED_DD_CAP
HANDOFF_PF = f28b.HANDOFF_PF
HANDOFF_DD_CAP = f28b.HANDOFF_DD_CAP

PRESERVED_CLUE = (
    "f28_train_only_stability_gap_reordered_union_surface_but_preserved_19_scout_rows_reference_only"
    "(전선28 학습 전용 안정성 격차는 합집합 표면을 재정렬했지만 19개 탐색 행만 참조 전용 보존)"
)
NEGATIVE_MEMORY = (
    "under_f28_locked_train_chunk_stability_rank_seed_and_handoff_remained_zero"
    "(전선28 잠금 학습 조각 안정성 순위 아래 씨앗과 인계는 0개로 남음)"
)
NEXT_HYPOTHESIS_CLUE = (
    "train_only_loss_concentration_veto_for_pf_dd_balance_reference_only"
    "(수익 팩터/손실폭 균형을 위한 학습 전용 손실 집중 차단 참조 전용 단서)"
)
REPAIR_DECISION = (
    "repair_not_run_no_valid_train_only_chunk_target_and_forward_targeted_repair_forbidden"
    "(유효한 학습 전용 조각 표적이 없고 전진 표적 수리는 금지라 수리 미실행)"
)
RUNTIME_PROBE_STATUS = (
    "out_of_scope_by_claim_no_handoff_candidate_after_f28b"
    "(전선28B 뒤 인계 후보 없어 주장 범위 밖)"
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F28A_SUMMARY)
    lock = read_json(F28A_LOCK)
    f28b_summary = read_json(F28B_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F28B_CANDIDATE_SUMMARY))
    chunk_metrics = pd.read_csv(io_path(F28B_CHUNK_METRICS))
    forward_diagnostic = pd.read_csv(io_path(F28B_FORWARD_DIAGNOSTIC))
    context = validate_context(stage_open, lock, f28b_summary, candidate_summary, chunk_metrics)
    audit = build_repair_audit(candidate_summary)
    diagnosis = build_diagnosis(audit, forward_diagnostic)
    final = build_final(created_at, stage_open, lock, f28b_summary, candidate_summary, chunk_metrics, diagnosis, context)
    write_outputs(final, audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "scout_seed_handoff": {
            "scout": final["f28b_summary"]["scout_clue_rows"],
            "seed": final["f28b_summary"]["seed_surface_rows"],
            "handoff": final["f28b_summary"]["handoff_candidate_rows"],
        },
        "near_seed_under_dd_rows": final["diagnosis"]["near_seed_under_dd_rows"],
        "pf_ready_dd_blocked_rows": final["diagnosis"]["pf_ready_dd_blocked_rows"],
        "valid_train_chunk_repair_opportunity_rows": final["diagnosis"]["valid_train_chunk_repair_opportunity_rows"],
        "repair_decision": final["repair_decision"],
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
    f28b_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    chunk_metrics: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    locks = lock.get("locks", {})
    checks = {
        "workspace_current_stage_frontier28": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier28c": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == f28a.RUN_ID,
        "stage_open_grok_retry_accepted": stage_open.get("grok", {}).get("retry", {}).get("classification", "").startswith("accepted"),
        "lock_changed_variable_stability_gap": locks.get("changed_variable") == "train_subperiod_pf_dd_balance_stability_gap_rank",
        "lock_forward_read_only": locks.get("forward_splits") == "validation_oos_read_only",
        "f28b_parent_matches": f28b_summary.get("run_id") == PARENT_RUN_ID,
        "f28b_next_run_matches": f28b_summary.get("next_run_id") == RUN_ID,
        "f28b_reference_candidate_rows": int(f28b_summary.get("reference_union_rows", -1)) == 234
        and int(f28b_summary.get("stability_candidate_rows", -1)) == 234,
        "f28b_scout_19_seed_handoff_zero": int(f28b_summary.get("scout_clue_rows", -1)) == 19
        and int(f28b_summary.get("seed_surface_rows", -1)) == 0
        and int(f28b_summary.get("handoff_candidate_rows", -1)) == 0,
        "candidate_summary_present": not candidate_summary.empty and len(candidate_summary) == 234,
        "candidate_summary_seed_zero": int(candidate_summary["seed_surface_flag"].map(as_bool).sum()) == 0,
        "candidate_summary_handoff_zero": int(candidate_summary["handoff_candidate_flag"].map(as_bool).sum()) == 0,
        "chunk_metrics_four_per_candidate": not chunk_metrics.empty and len(chunk_metrics) == 234 * 4,
        "runtime_authority_not_claimed": f28b_summary.get("claim_boundary", {}).get("runtime_authority") == "not_claimed(주장 없음)",
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier28C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_repair_audit(summary: pd.DataFrame) -> pd.DataFrame:
    df = summary.copy()
    numeric_columns = [
        "train_profit_factor",
        "train_trades_per_day",
        "train_dd_risk",
        "chunk_pf_floor",
        "chunk_dd_max",
        "chunk_density_cv",
        "chunk_net_positive_count",
        "chunk_equity_r2_floor",
        "chunk_max_loss_streak_max",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk",
        "forward_read_score",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in ("density_bridge_flag", "scout_clue_flag", "seed_surface_flag", "handoff_candidate_flag"):
        df[column] = df[column].map(as_bool)
    df["forward_min_pf"] = df[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    df["forward_max_dd"] = df[["validation_dd_risk", "oos_dd_risk"]].max(axis=1)
    df["forward_min_density"] = df[["validation_trades_per_day", "oos_trades_per_day"]].min(axis=1)
    df["seed_pf_gap"] = (SEED_PF - df["forward_min_pf"]).clip(lower=0.0)
    df["seed_dd_gap"] = (df["forward_max_dd"] - SEED_DD_CAP).clip(lower=0.0)
    df["handoff_pf_gap"] = (HANDOFF_PF - df["forward_min_pf"]).clip(lower=0.0)
    df["handoff_dd_gap"] = (df["forward_max_dd"] - HANDOFF_DD_CAP).clip(lower=0.0)
    df["near_seed_under_dd"] = (
        df["density_bridge_flag"]
        & (df["forward_max_dd"] <= SEED_DD_CAP)
        & (df["forward_min_pf"] >= 1.15)
        & ~df["seed_surface_flag"]
    )
    df["pf_ready_dd_blocked"] = (
        df["density_bridge_flag"]
        & (df["validation_profit_factor"] >= SEED_PF)
        & (df["oos_profit_factor"] >= SEED_PF)
        & (df["forward_max_dd"] > SEED_DD_CAP)
    )
    df["clear_train_chunk_defect"] = (
        (df["chunk_pf_floor"] < 1.05)
        | (df["chunk_dd_max"] > 20.0)
        | (df["chunk_net_positive_count"] < 3.0)
    )
    df["valid_train_chunk_repair_opportunity"] = (
        (df["near_seed_under_dd"] | df["pf_ready_dd_blocked"])
        & df["clear_train_chunk_defect"]
    )
    df["scout_not_seed"] = df["scout_clue_flag"] & ~df["seed_surface_flag"]
    df["stability_ok_forward_failed"] = (
        (df["chunk_pf_floor"] >= 1.05)
        & (df["chunk_dd_max"] <= 20.0)
        & (df["chunk_net_positive_count"] >= 3.0)
        & df["density_bridge_flag"]
        & ~df["seed_surface_flag"]
    )
    df["seed_total_gap"] = df["seed_pf_gap"] + (df["seed_dd_gap"] / max(SEED_DD_CAP, 1.0))
    keep = [
        "stability_union_id",
        "stability_rank",
        "source_soft_union_id",
        "micro_key",
        "micro_ids",
        "train_profit_factor",
        "train_trades_per_day",
        "train_dd_risk",
        "chunk_pf_floor",
        "chunk_dd_max",
        "chunk_density_cv",
        "chunk_net_positive_count",
        "chunk_equity_r2_floor",
        "chunk_max_loss_streak_max",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk",
        "forward_min_pf",
        "forward_max_dd",
        "forward_min_density",
        "seed_pf_gap",
        "seed_dd_gap",
        "handoff_pf_gap",
        "handoff_dd_gap",
        "density_bridge_flag",
        "scout_clue_flag",
        "seed_surface_flag",
        "handoff_candidate_flag",
        "near_seed_under_dd",
        "pf_ready_dd_blocked",
        "clear_train_chunk_defect",
        "valid_train_chunk_repair_opportunity",
        "scout_not_seed",
        "stability_ok_forward_failed",
        "seed_total_gap",
        "forward_read_score",
    ]
    return df[keep].sort_values(
        ["valid_train_chunk_repair_opportunity", "seed_surface_flag", "scout_clue_flag", "seed_total_gap", "stability_rank"],
        ascending=[False, False, False, True, True],
    )


def build_diagnosis(audit: pd.DataFrame, forward_diagnostic: pd.DataFrame) -> dict[str, Any]:
    under_dd = audit.loc[audit["forward_max_dd"] <= SEED_DD_CAP].sort_values("forward_min_pf", ascending=False)
    pf_ready = audit.loc[audit["pf_ready_dd_blocked"]].sort_values("forward_max_dd", ascending=True)
    opportunities = audit.loc[audit["valid_train_chunk_repair_opportunity"]]
    scout = audit.loc[audit["scout_clue_flag"]]
    best_under_dd = dict(under_dd.iloc[0]) if not under_dd.empty else {}
    best_pf_ready = dict(pf_ready.iloc[0]) if not pf_ready.empty else {}
    best_forward = dict(forward_diagnostic.iloc[0]) if not forward_diagnostic.empty else {}
    return {
        "density_bridge_rows": int(audit["density_bridge_flag"].sum()),
        "scout_clue_rows": int(audit["scout_clue_flag"].sum()),
        "seed_surface_rows": int(audit["seed_surface_flag"].sum()),
        "handoff_candidate_rows": int(audit["handoff_candidate_flag"].sum()),
        "near_seed_under_dd_rows": int(audit["near_seed_under_dd"].sum()),
        "pf_ready_dd_blocked_rows": int(audit["pf_ready_dd_blocked"].sum()),
        "scout_not_seed_rows": int(audit["scout_not_seed"].sum()),
        "valid_train_chunk_repair_opportunity_rows": int(len(opportunities)),
        "stability_ok_forward_failed_rows": int(audit["stability_ok_forward_failed"].sum()),
        "best_forward_under_seed_dd": json_ready(best_under_dd),
        "best_pf_ready_dd_blocked": json_ready(best_pf_ready),
        "best_forward_readonly_diagnostic": json_ready(best_forward),
        "max_forward_min_pf_when_dd_le_seed_cap": float(under_dd["forward_min_pf"].max()) if not under_dd.empty else None,
        "min_forward_max_dd_when_pf_ge_seed_floor": float(pf_ready["forward_max_dd"].min()) if not pf_ready.empty else None,
        "best_scout_forward_min_pf": float(scout["forward_min_pf"].max()) if not scout.empty else None,
        "decision_reason": (
            "F28B found the same 19 scout rows but no seed or handoff. Rows with DD <= 18% stay below the 1.20 seed PF floor, "
            "and rows with PF >= 1.20 break the 18% DD cap. The near rows are already train-stable, so a valid train-only "
            "chunk repair target is absent; selecting the PF/DD bottleneck directly would be validation/OOS-targeted."
            "(F28B는 같은 19개 탐색 행을 찾았지만 씨앗과 인계는 0개입니다. DD 18% 이하 행은 씨앗 PF 1.20에 못 미치고, "
            "PF 1.20 이상 행은 DD 18% 상한을 깹니다. 근접 행은 이미 학습 안정성이 있으므로 유효한 학습 전용 조각 수리 표적이 없고, "
            "PF/DD 병목을 직접 고르는 것은 검증/OOS 표적 수리가 됩니다.)"
        ),
    }


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    f28b_summary: dict[str, Any],
    candidate_summary: pd.DataFrame,
    chunk_metrics: pd.DataFrame,
    diagnosis: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    best = f28b_summary.get("best_stability_union", {})
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
            "grok_classification": stage_open.get("grok", {}).get("retry", {}).get("classification", ""),
        },
        "lock_summary": {
            "changed_variable": lock.get("locks", {}).get("changed_variable"),
            "forward_splits": lock.get("locks", {}).get("forward_splits"),
            "selection_boundary": lock.get("locks", {}).get("selection_boundary"),
        },
        "f28b_summary": {
            "status": f28b_summary.get("status"),
            "judgment": f28b_summary.get("judgment"),
            "reference_union_rows": f28b_summary.get("reference_union_rows"),
            "stability_candidate_rows": f28b_summary.get("stability_candidate_rows"),
            "density_bridge_rows": f28b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f28b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f28b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f28b_summary.get("handoff_candidate_rows"),
            "best_stability_union_id": f28b_summary.get("best_stability_union_id"),
            "best_forward_readonly_union_id": f28b_summary.get("best_forward_readonly_union_id"),
            "best_stability_union": best,
        },
        "candidate_summary_rows": int(len(candidate_summary)),
        "chunk_metric_rows": int(len(chunk_metrics)),
        "diagnosis": diagnosis,
        "repair_decision": REPAIR_DECISION,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "result_boundary": "repair_or_closeout_decision_no_wfo_no_mt5_no_runtime_authority(수리 또는 마감 결정, WFO/MT5/런타임 권위 없음)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], audit: pd.DataFrame) -> None:
    audit.to_csv(io_path(RUN_ROOT / "repair_rejection_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, audit))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F28A_SUMMARY,
        F28A_LOCK,
        F28B_SUMMARY,
        F28B_CANDIDATE_SUMMARY,
        F28B_CHUNK_METRICS,
        F28B_FORWARD_DIAGNOSTIC,
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
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "decision": {
            "repair_decision": final["repair_decision"],
            "preserved_clue": final["preserved_clue"],
            "negative_memory": final["negative_memory"],
            "runtime_probe_status": final["runtime_probe_status"],
        },
        "compatibility": {"schema_version": "frontier28c_repair_or_closeout_decision_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], audit: pd.DataFrame) -> str:
    diagnosis = final["diagnosis"]
    best_stability = final["f28b_summary"]["best_stability_union"]
    under_dd = diagnosis["best_forward_under_seed_dd"]
    pf_ready = diagnosis["best_pf_ready_dd_blocked"]
    rows = []
    for _, row in audit.head(12).iterrows():
        rows.append(
            f"| `{row['stability_union_id']}` | `{row['source_soft_union_id']}` | {fmt(row['forward_min_pf'])} | "
            f"{fmt(row['forward_max_dd'])} | {fmt(row['chunk_pf_floor'])} | {fmt(row['chunk_dd_max'])} | "
            f"{row['scout_clue_flag']} | {row['near_seed_under_dd']} | {row['pf_ready_dd_blocked']} | {row['valid_train_chunk_repair_opportunity']} |"
        )
    table = "\n".join(rows) if rows else "| none(없음) | | | | | | | | | |"
    return f"""# Frontier28C Repair Or Closeout Decision Report(전선28C 수리 또는 마감 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F28B(전선28B) train-only stability gap proxy(학습 전용 안정성 격차 프록시) 결과를 repair feasibility audit(수리 가능성 감사)로 분해했습니다.

Effect(효과): validation/OOS(검증/표본외)를 표적으로 삼는 수리를 막고, 학습 전용 조각 안정성 안에서 고칠 표적이 있는지만 판정했습니다.

F28B reference/stability/density/scout/seed/handoff rows(전선28B 참조/안정성/빈도/탐색/씨앗/인계 행): `{final['f28b_summary']['reference_union_rows']}` / `{final['f28b_summary']['stability_candidate_rows']}` / `{final['f28b_summary']['density_bridge_rows']}` / `{final['f28b_summary']['scout_clue_rows']}` / `{final['f28b_summary']['seed_surface_rows']}` / `{final['f28b_summary']['handoff_candidate_rows']}`

Best stability union(최상 안정성 합집합): `{final['f28b_summary']['best_stability_union_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best_stability.get('validation_profit_factor'))}/{fmt(best_stability.get('validation_trades_per_day'))}/{fmt(best_stability.get('validation_dd_risk'))}` and `{fmt(best_stability.get('oos_profit_factor'))}/{fmt(best_stability.get('oos_trades_per_day'))}/{fmt(best_stability.get('oos_dd_risk'))}`.

Repair decision(수리 결정): `{final['repair_decision']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Next hypothesis clue(다음 가설 단서): `{final['next_hypothesis_clue']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Bottleneck Audit(병목 감사)

- near_seed_under_dd_rows(손실폭 충족 근접 씨앗 행): `{diagnosis['near_seed_under_dd_rows']}`
- pf_ready_dd_blocked_rows(PF 준비/손실폭 차단 행): `{diagnosis['pf_ready_dd_blocked_rows']}`
- valid_train_chunk_repair_opportunity_rows(유효 학습 조각 수리 기회 행): `{diagnosis['valid_train_chunk_repair_opportunity_rows']}`
- max_forward_min_pf_when_dd_le_seed_cap(씨앗 손실폭 이하에서 최대 전진 최소 PF): `{fmt(diagnosis['max_forward_min_pf_when_dd_le_seed_cap'])}`
- min_forward_max_dd_when_pf_ge_seed_floor(씨앗 PF 이상에서 최소 전진 최대 DD): `{fmt(diagnosis['min_forward_max_dd_when_pf_ge_seed_floor'])}`

Best under DD cap(손실폭 상한 아래 최상): `{under_dd.get('stability_union_id', '')}` with forward min PF/max DD(전진 최소 PF/최대 DD) `{fmt(under_dd.get('forward_min_pf'))}` / `{fmt(under_dd.get('forward_max_dd'))}`.

Best PF-ready DD-blocked(PF 준비 손실폭 차단 최상): `{pf_ready.get('stability_union_id', '')}` with forward min PF/max DD(전진 최소 PF/최대 DD) `{fmt(pf_ready.get('forward_min_pf'))}` / `{fmt(pf_ready.get('forward_max_dd'))}`.

Diagnosis(진단): {diagnosis['decision_reason']}

| union(합집합) | source(원천) | forward min PF(전진 최소 PF) | forward max DD(전진 최대 DD) | chunk PF floor(조각 PF 바닥) | chunk DD max(조각 DD 최대) | scout(탐색) | near seed under DD(DD 아래 근접 씨앗) | PF ready DD blocked(PF 준비 DD 차단) | valid repair(유효 수리) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier28C Gate Audit(전선28C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): repair decision artifact(수리 결정 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- parent_proxy_gate(부모 프록시 게이트): F28B(전선28B) seed/handoff(씨앗/인계) `0/0` verified(검증)
- train_only_repair_gate(학습 전용 수리 게이트): valid_train_chunk_repair_opportunity_rows(유효 학습 조각 수리 기회 행) `{final['diagnosis']['valid_train_chunk_repair_opportunity_rows']}`
- leakage_guard(누수 방어): validation/OOS-targeted repair(검증/표본외 표적 수리) rejected(거절)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B(티어 A/B/A+B) rows(행) written(기록)
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier28 Selection Status(전선28 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest decision(최근 결정): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Repair decision(수리 결정): `{final['repair_decision']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

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
        "primary_kpi": (
            f"near_under_dd={final['diagnosis']['near_seed_under_dd_rows']};"
            f"pf_ready_dd_blocked={final['diagnosis']['pf_ready_dd_blocked_rows']};"
            f"valid_repair={final['diagnosis']['valid_train_chunk_repair_opportunity_rows']}"
        ),
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
        "primary_kpi": (
            f"scout={final['f28b_summary']['scout_clue_rows']};"
            f"seed={final['f28b_summary']['seed_surface_rows']};"
            f"handoff={final['f28b_summary']['handoff_candidate_rows']}"
        ),
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시라 MT5 없음)",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시라 MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` rejected Frontier28 repair and prepared closeout(전선28 수리 거절 및 마감 준비). "
        f"Effect(효과): preserved clue(보존 단서) `{final['preserved_clue']}` and negative memory(부정 기억) `{final['negative_memory']}` recorded.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR28-TRAIN-ONLY-STABILITY-GAP-PENALTY-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` rejected repair after scout-only stability gap surface(탐색 전용 안정성 격차 표면 뒤 수리 거절). "
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

Action(행동): F28C(전선28C)가 F28B(전선28B) scout-only result(탐색 전용 결과)에 대해 repair feasibility audit(수리 가능성 감사)을 닫았습니다.

Effect(효과): allowed train-only chunk repair(허용된 학습 전용 조각 수리) 표적은 `0`개였고, validation/OOS-targeted repair(검증/표본외 표적 수리)는 금지라 closeout(마감)으로 이동합니다.

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
