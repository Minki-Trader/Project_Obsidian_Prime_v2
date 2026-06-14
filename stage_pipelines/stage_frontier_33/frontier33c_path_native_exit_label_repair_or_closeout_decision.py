from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b


STAGE_ID = f33b.STAGE_ID
RUN_ID = "frontier33C_path_native_exit_label_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier33C"
PARENT_RUN_ID = f33b.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = f33b.NEXT_PRE_EXPENSIVE_GROK_RUN_ID
NEXT_CLOSEOUT_RUN_ID = "frontier33D_stage_closeout_path_native_exit_label_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_33/frontier33c_path_native_exit_label_repair_or_closeout_decision.py")

F33B_SUMMARY = STAGE_ROOT / "02_runs" / f33b.RUN_ID / "final_summary.json"
F33B_CONDITION_POOL = STAGE_ROOT / "02_runs" / f33b.RUN_ID / "path_native_condition_pool.csv"
F33B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f33b.RUN_ID / "path_native_candidate_summary.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

REPAIR_TAKE_QUANTILES = (0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70)
REPAIR_STOP_QUANTILES = (0.30, 0.35, 0.40, 0.50, 0.60, 0.70)
MAX_SOURCE_SCOUTS = 4
MAX_REPAIR_CANDIDATES = 220


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    parent = read_json(F33B_SUMMARY)
    frame = f23b.load_frame()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    condition_pool = pd.read_csv(io_path(F33B_CONDITION_POOL))
    parent_summary = pd.read_csv(io_path(F33B_CANDIDATE_SUMMARY))
    context = validate_context(parent, condition_pool, parent_summary)
    candidates = build_repair_candidates(frame, condition_pool, parent_summary, path_labels, raw_path)
    split_metrics = f33b.evaluate_candidates(frame, candidates, path_labels, raw_path)
    summary = f33b.summarize_candidates(split_metrics)
    final = build_final(created_at, parent, context, candidates, split_metrics, summary)
    write_outputs(final, candidates, split_metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "source_scout_rows": final["source_scout_rows"],
        "repair_candidate_rows": final["repair_candidate_rows"],
        "repair_scout_clue_rows": final["repair_scout_clue_rows"],
        "repair_seed_surface_rows": final["repair_seed_surface_rows"],
        "repair_runtime_candidate_rows": final["repair_runtime_candidate_rows"],
        "best_repair_candidate_id": final["best_repair_candidate_id"],
        "runtime_probe_status": final["runtime_probe_status"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(parent: dict[str, Any], condition_pool: pd.DataFrame, parent_summary: pd.DataFrame) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    scout_rows = parent_summary.loc[parent_summary["path_scout_clue_flag"].astype(bool)]
    checks = {
        "workspace_current_frontier33b_or_33c": f"current_stage_id: {STAGE_ID}" in workspace
        and (f"current_run_id: {PARENT_RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace),
        "workspace_next_run_frontier33c": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "parent_run_matches": parent.get("run_id") == PARENT_RUN_ID,
        "parent_scout_only": int(parent.get("path_scout_clue_rows", 0)) > 0
        and int(parent.get("path_seed_surface_rows", -1)) == 0
        and int(parent.get("runtime_probe_candidate_rows", -1)) == 0,
        "condition_pool_available": len(condition_pool) > 0,
        "source_scout_rows_available": 0 < len(scout_rows) <= MAX_SOURCE_SCOUTS,
        "no_runtime_authority_claimed": parent.get("claim_boundary", {}).get("runtime_authority") == "not_claimed",
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier33C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks, "source_scout_rows": int(len(scout_rows))}


def build_repair_candidates(
    frame: pd.DataFrame,
    condition_pool: pd.DataFrame,
    parent_summary: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> list[dict[str, Any]]:
    condition_map = {str(row["condition_id"]): row for _, row in condition_pool.iterrows()}
    source = parent_summary.loc[parent_summary["path_scout_clue_flag"].astype(bool)].head(MAX_SOURCE_SCOUTS)
    repair_candidates: list[dict[str, Any]] = []
    for _, source_row in source.iterrows():
        condition_ids = [token for token in str(source_row["condition_ids"]).split("|") if token]
        conditions = [condition_map[token] for token in condition_ids if token in condition_map]
        if len(conditions) != len(condition_ids):
            continue
        masks = [condition_mask(frame, item) for item in conditions]
        mask = np.logical_and.reduce(masks) if len(masks) > 1 else masks[0]
        side = int(source_row["side_value"])
        variants = repair_threshold_variants(frame, mask, side, path_labels)
        for threshold_row in variants:
            metrics = f33b.evaluate_path_mask(
                frame,
                mask,
                side,
                threshold_row["stop_cap_log_return"],
                threshold_row["take_cap_log_return"],
                path_labels,
                raw_path,
                "train",
            )
            if metrics["trade_count"] < f33b.MIN_SINGLE_TRAIN_TRADES:
                continue
            if not (f33b.MIN_TRAIN_DENSITY <= metrics["trades_per_day"] <= f33b.MAX_TRAIN_DENSITY):
                continue
            if metrics["net_profit"] <= 0.0 or metrics["profit_factor"] < 1.01:
                continue
            score = f33b.train_path_score(metrics, threshold_row)
            repair_candidates.append(repair_candidate_from_source(conditions, mask, side, threshold_row, metrics, score, source_row))
    repair_candidates.sort(key=lambda item: float(item["train_path_score"]), reverse=True)
    repair_candidates = repair_candidates[:MAX_REPAIR_CANDIDATES]
    for index, candidate in enumerate(repair_candidates, start=1):
        candidate["candidate_id"] = f"f33c_{index:04d}"
    return repair_candidates


def repair_threshold_variants(
    frame: pd.DataFrame,
    mask: np.ndarray,
    side: int,
    path_labels: dict[int, dict[str, np.ndarray]],
) -> list[dict[str, Any]]:
    labels = path_labels[side]
    train = f33b.split_mask(frame, "train") & np.asarray(mask, dtype=bool) & labels["valid"]
    mfe = labels["mfe"][train]
    mae = labels["mae"][train]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    if mfe.size < 30 or mae.size < 30:
        return []
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for take_q in REPAIR_TAKE_QUANTILES:
        take_cap = max(float(np.nanquantile(mfe, take_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
        for stop_q in REPAIR_STOP_QUANTILES:
            stop_cap = max(float(np.nanquantile(mae, stop_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
            key = (int(round(stop_cap * 1_000_000)), int(round(take_cap * 1_000_000)))
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "threshold_source": "repair_train_split_mfe_mae_fine_quantiles_only",
                "stop_quantile": stop_q,
                "take_quantile": take_q,
                "stop_cap_log_return": stop_cap,
                "take_cap_log_return": take_cap,
                "train_threshold_sample_rows": int(min(mfe.size, mae.size)),
            })
    return rows


def repair_candidate_from_source(
    conditions: list[pd.Series],
    mask: np.ndarray,
    side: int,
    threshold_row: dict[str, Any],
    train_metrics: dict[str, Any],
    score: float,
    source_row: pd.Series,
) -> dict[str, Any]:
    features = [str(item["feature"]) for item in conditions]
    families = [str(item["feature_family"]) for item in conditions]
    return {
        "candidate_id": "",
        "source_f33b_candidate_id": str(source_row["candidate_id"]),
        "condition_count": len(conditions),
        "condition_ids": "|".join(str(item["condition_id"]) for item in conditions),
        "features": "|".join(features),
        "feature_families": "|".join(families),
        "side_value": side,
        "side": f"{'long' if side > 0 else 'short'}({'롱' if side > 0 else '숏'})",
        "rule_definition": " & ".join(str(item["definition"]) for item in conditions),
        "threshold_source": threshold_row["threshold_source"],
        "stop_quantile": threshold_row["stop_quantile"],
        "take_quantile": threshold_row["take_quantile"],
        "stop_cap_log_return": threshold_row["stop_cap_log_return"],
        "take_cap_log_return": threshold_row["take_cap_log_return"],
        "train_threshold_sample_rows": threshold_row["train_threshold_sample_rows"],
        "train_path_score": score,
        "executable_first_hit_representation": True,
        "mask": mask,
        "train_selection_metrics": train_metrics,
    }


def condition_mask(frame: pd.DataFrame, row: pd.Series) -> np.ndarray:
    values = pd.to_numeric(frame[str(row["feature"])], errors="coerce").to_numpy(dtype="float64")
    finite = np.isfinite(values)
    threshold = float(row["threshold_value"])
    operator = str(row["operator"])
    if operator == "<=":
        return (values <= threshold) & finite
    if operator == ">=":
        return (values >= threshold) & finite
    if operator == "<":
        return (values < threshold) & finite
    if operator == ">":
        return (values > threshold) & finite
    raise ValueError(f"Unsupported operator(지원하지 않는 연산자): {operator}")


def build_final(
    created_at: str,
    parent: dict[str, Any],
    context: dict[str, Any],
    candidates: list[dict[str, Any]],
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["path_scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["path_seed_surface_flag"].sum()) if not summary.empty else 0
    runtime_count = int(summary["runtime_probe_candidate_flag"].sum()) if not summary.empty else 0
    strict_count = int(summary["runtime_strict_candidate_flag"].sum()) if not summary.empty else 0
    if runtime_count:
        status = "path_native_exit_label_repair_runtime_candidate_needs_pre_expensive_grok_no_authority"
        judgment = "runtime_probe_candidates_require_grok_before_mt5_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
        runtime_probe_status = "runtime_probe_candidate_pending_pre_expensive_grok_and_mt5_micro_probe"
    elif seed_count:
        status = "path_native_exit_label_repair_seed_surface_closeout_queued_no_authority"
        judgment = "seed_surface_preserved_clue_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_repair_seed_only_no_runtime_candidate"
    elif scout_count:
        status = "path_native_exit_label_repair_scout_only_closeout_queued_no_authority"
        judgment = "scout_clue_preserved_but_no_seed_runtime_requires_closeout"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_repair_scout_only_no_runtime_candidate"
    else:
        status = "path_native_exit_label_repair_rejected_closeout_queued_no_authority"
        judgment = "negative_memory_repair_failed_to_improve_scout_to_seed_or_runtime"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_ineligible_no_path_native_repair_candidate_after_f33c"
    best = dict(summary.iloc[0]) if not summary.empty else {}
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "context": context,
        "parent": {
            "run_id": parent.get("run_id"),
            "path_scout_clue_rows": parent.get("path_scout_clue_rows"),
            "path_seed_surface_rows": parent.get("path_seed_surface_rows"),
            "runtime_probe_candidate_rows": parent.get("runtime_probe_candidate_rows"),
        },
        "source_scout_rows": int(context["source_scout_rows"]),
        "repair_candidate_rows": int(len(candidates)),
        "repair_split_metric_rows": int(len(split_metrics)) if not split_metrics.empty else 0,
        "repair_summary_rows": int(len(summary)) if not summary.empty else 0,
        "repair_scout_clue_rows": scout_count,
        "repair_seed_surface_rows": seed_count,
        "repair_runtime_candidate_rows": runtime_count,
        "repair_runtime_strict_candidate_rows": strict_count,
        "best_repair_candidate_id": best.get("candidate_id", ""),
        "best_repair_candidate": json_ready(best),
        "runtime_probe_status": runtime_probe_status,
        "result_boundary": "bounded_repair_python_path_native_proxy_only_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    candidates: list[dict[str, Any]],
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    pd.DataFrame([f33b.clean_candidate_for_csv(item) for item in candidates]).to_csv(io_path(RUN_ROOT / "repair_candidate_ledger.csv"), index=False, encoding="utf-8-sig")
    split_metrics.to_csv(io_path(RUN_ROOT / "repair_split_metrics.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "repair_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.head(30).to_csv(io_path(RUN_ROOT / "top_repair_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")
    else:
        pd.DataFrame().to_csv(io_path(RUN_ROOT / "top_repair_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F33B_SUMMARY,
        F33B_CONDITION_POOL,
        F33B_CANDIDATE_SUMMARY,
        RUN_ROOT / "repair_candidate_ledger.csv",
        RUN_ROOT / "repair_split_metrics.csv",
        RUN_ROOT / "repair_candidate_summary.csv",
        RUN_ROOT / "top_repair_forward_diagnostic.csv",
        RUN_ROOT / "final_summary.json",
        REPORT_PATH,
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
        "repair_boundary": {
            "source": "F33B scout clue rows only",
            "threshold_source": "repair train-only MFE/MAE fine quantiles",
            "max_source_scouts": MAX_SOURCE_SCOUTS,
            "max_repair_candidates": MAX_REPAIR_CANDIDATES,
        },
        "runtime_claim_boundary": "bounded_repair_proxy_only_no_mt5_runtime_authority",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f33b.f33a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    if final["repair_runtime_candidate_rows"] == 0:
        f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_register_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_repair_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"source_scout={final['source_scout_rows']};repair_scout={final['repair_scout_clue_rows']};seed={final['repair_seed_surface_rows']};runtime_candidate={final['repair_runtime_candidate_rows']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_repair_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "bounded_train_only_repair_no_forward_rerank_no_mt5_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_repair_candidate"]
    return [{
        "ledger_row_id": f"{RUN_ID}__repair_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__repair_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "bounded_repair_no_runtime(상한 수리, 런타임 아님)",
        "scoreboard_lane": "repair_decision(수리 결정)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_repair_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "bounded_repair_no_validation_oos_threshold_selection_no_mt5_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"source_scout={final['source_scout_rows']};repair_scout={final['repair_scout_clue_rows']};seed={final['repair_seed_surface_rows']};runtime_candidate={final['repair_runtime_candidate_rows']};next={final['next_run_id']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "repair_decision(수리 결정)",
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
        f"next_run_id: {final['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_repair_candidate"]
    return f"""# Frontier33C Path-Native Exit Label Repair Decision Report(전선33C 경로 기반 청산 라벨 수리 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F33B scout clue(전선33B 탐색 단서) `{final['source_scout_rows']}`개에만 bounded train-only MFE/MAE fine quantile repair(상한 있는 학습 전용 최대 유리/불리 이동 세밀 분위수 수리)를 적용했습니다.

Effect(효과): validation/OOS(검증/표본외)를 임계값 선택에 쓰지 않고, scout clue(탐색 단서)가 seed/runtime candidate(씨앗/런타임 후보)로 올라갈 수 있는지만 확인했습니다.

Repair candidate rows(수리 후보 행): `{final['repair_candidate_rows']}`

Repair scout/seed/runtime candidate(수리 탐색/씨앗/런타임 후보): `{final['repair_scout_clue_rows']}` / `{final['repair_seed_surface_rows']}` / `{final['repair_runtime_candidate_rows']}`

Best repair candidate(최상 수리 후보): `{final['best_repair_candidate_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier33C Gate Audit(전선33C 게이트 감사)

- repair_boundary_gate(수리 경계 게이트): source scout rows(원천 탐색 단서 행) `{final['source_scout_rows']}`, max `{MAX_SOURCE_SCOUTS}`
- threshold_source_gate(임계값 원천 게이트): repair train-only MFE/MAE fine quantiles(수리 학습 전용 최대 유리/불리 이동 세밀 분위수)
- no_forward_rerank_gate(전진 재순위 금지 게이트): validation/OOS(검증/표본외)는 read-only(읽기 전용)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- closeout_gate(마감 게이트): next run(다음 실행) `{final['next_run_id']}`
- final_claim_guard(최종 주장 방지): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier33 Selection Status(전선33 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest repair decision(최근 수리 결정): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Repair scout/seed/runtime candidate(수리 탐색/씨앗/런타임 후보): `{final['repair_scout_clue_rows']}` / `{final['repair_seed_surface_rows']}` / `{final['repair_runtime_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_repair_candidate"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F33C(전선33C)는 F33B scout clue(전선33B 탐색 단서)를 bounded repair(상한 수리)로 재측정했습니다.

Effect(효과): repair scout/seed/runtime candidate(수리 탐색/씨앗/런타임 후보)는 `{final['repair_scout_clue_rows']}/{final['repair_seed_surface_rows']}/{final['repair_runtime_candidate_rows']}`이고, 다음 행동은 closeout(마감) 또는 pre-expensive Grok(비싼 실행 전 그록)로 고정됩니다.

Best repair candidate(최상 수리 후보): `{final['best_repair_candidate_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-밀도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran bounded path-native repair(상한 있는 경로 기반 수리). "
        f"Effect(효과): repair_scout={final['repair_scout_clue_rows']}, seed={final['repair_seed_surface_rows']}, runtime_candidate={final['repair_runtime_candidate_rows']}, next=`{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR33-PATH-NATIVE-EXIT-LABEL-ONNX-SCOUT`: `{RUN_ID}` repaired F33B scout clues(전선33B 탐색 단서 수리). "
        f"Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`이며 authority(권위)는 없습니다.\n"
    )


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: bounded path-native repair(상한 경로 기반 수리) did not produce runtime candidate(런타임 후보 미생성). "
        f"Evidence(근거): repair_scout/seed/runtime={final['repair_scout_clue_rows']}/{final['repair_seed_surface_rows']}/{final['repair_runtime_candidate_rows']}. "
        f"Effect(효과): closeout(마감)에서 preserved clue(보존 단서)와 negative memory(부정 기억)를 분리합니다.\n"
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
