from __future__ import annotations

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
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b


STAGE_ID = f23b.STAGE_ID
RUN_ID = "frontier23C_payoff_asymmetry_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier23C"
PARENT_RUN_ID = f23b.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier23D_grok_pre_expensive_payoff_asymmetry_repaired_handoff_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier23D_stage_closeout_payoff_asymmetry_pf_source_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_23/frontier23c_payoff_asymmetry_entry_filter_repair.py")

F23B_SUMMARY = STAGE_ROOT / "02_runs" / f23b.RUN_ID / "final_summary.json"
F23B_CANDIDATES = STAGE_ROOT / "02_runs" / f23b.RUN_ID / "candidate_summary.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SOURCE_KEEP = 16
FILTER_KEEP = 120
MAX_REPAIR_CANDIDATES = 240
MIN_REPAIR_TRADES = 35
MIN_REPAIR_DENSITY = 2.0
MAX_REPAIR_DENSITY = 15.0

SCOUT_MIN_PF = f23b.SCOUT_MIN_PF
SCOUT_DENSITY_LOW = f23b.SCOUT_DENSITY_LOW
SCOUT_DENSITY_HIGH = f23b.SCOUT_DENSITY_HIGH
SCOUT_DD_CAP = 30.0
SEED_PF = f23b.SEED_PF
SEED_DD_CAP = 18.0
HANDOFF_PF = f23b.HANDOFF_PF
HANDOFF_DD_CAP = f23b.HANDOFF_DD_CAP


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    f23b_summary = read_json(F23B_SUMMARY)
    f23b_candidates = pd.read_csv(io_path(F23B_CANDIDATES))
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(f23b_summary, feature_order)
    baselines = f23b.build_unconditional_baselines(frame)
    condition_pool = f23b.build_condition_pool(frame, feature_order, baselines)
    source_candidates = rebuild_source_candidates(frame, condition_pool, f23b_candidates)
    repair_candidates = build_repair_candidates(frame, condition_pool, source_candidates)
    metrics = evaluate_repair_candidates(frame, repair_candidates)
    summary = summarize_repair(metrics)
    final = build_final(created_at, f23b_summary, feature_order, context, source_candidates, repair_candidates, metrics, summary)
    write_outputs(final, repair_candidates, metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "source_candidate_count": final["source_candidate_count"],
        "repair_candidate_rows": final["repair_candidate_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_repair_id": final["best_repair_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(f23b_summary: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier23": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier23c": f"next_run_id: {RUN_ID}" in workspace,
        "f23b_parent_matches": f23b_summary.get("run_id") == PARENT_RUN_ID,
        "f23b_scout_no_seed": int(f23b_summary.get("scout_clue_rows", 0)) > 0 and int(f23b_summary.get("seed_surface_rows", -1)) == 0,
        "feature_order_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier23C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def rebuild_source_candidates(frame: pd.DataFrame, condition_pool: pd.DataFrame, f23b_candidates: pd.DataFrame) -> list[dict[str, Any]]:
    candidates = f23b.build_candidate_pool(frame, condition_pool)
    by_id = {item["candidate_id"]: item for item in candidates}
    ordered = f23b_candidates.copy()
    scout_mask = ordered.get("scout_clue_flag", pd.Series(False, index=ordered.index)).astype(str).str.lower().eq("true")
    if scout_mask.any():
        ordered = ordered.loc[scout_mask].copy()
    ordered = ordered.sort_values("forward_read_score", ascending=False).head(SOURCE_KEEP)
    sources: list[dict[str, Any]] = []
    for _, row in ordered.iterrows():
        candidate_id = str(row["candidate_id"])
        item = by_id.get(candidate_id)
        if item is None:
            continue
        source_train = f23b.evaluate_mask(frame, item["mask"], int(item["side_value"]), "train")
        sources.append({
            "source_candidate_id": candidate_id,
            "source_summary": dict(row),
            "source_candidate": item,
            "source_train": source_train,
        })
    if not sources:
        raise RuntimeError("No source candidates could be rebuilt(원천 후보 재구성 실패).")
    return sources


def build_repair_candidates(frame: pd.DataFrame, condition_pool: pd.DataFrame, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    filter_rows = condition_pool.loc[condition_pool["sanity_pass"].astype(bool)].sort_values("train_payoff_score", ascending=False).head(FILTER_KEEP)
    filters = filter_rows.to_dict("records")
    repair_rows: list[dict[str, Any]] = []
    for source in sources:
        item = source["source_candidate"]
        source_features = set(str(item["features"]).split("|"))
        source_mask = np.asarray(item["mask"], dtype=bool)
        source_side = int(item["side_value"])
        source_train = source["source_train"]
        for filter_row in filters:
            if int(filter_row["side_value"]) != source_side:
                continue
            filter_feature = str(filter_row["feature"])
            if filter_feature in source_features:
                continue
            filter_mask = np.asarray(filter_row["_mask"], dtype=bool)
            for repair_type, repaired_mask in (("include", source_mask & filter_mask), ("veto", source_mask & ~filter_mask)):
                metrics = f23b.evaluate_mask(frame, repaired_mask, source_side, "train")
                if metrics["trade_count"] < MIN_REPAIR_TRADES:
                    continue
                if not (MIN_REPAIR_DENSITY <= metrics["trades_per_day"] <= MAX_REPAIR_DENSITY):
                    continue
                if metrics["net_profit"] <= 0 or metrics["profit_factor"] < 1.02:
                    continue
                score = repair_score(metrics, source_train)
                if score <= 0:
                    continue
                repair_rows.append({
                    "repair_id": f"f23c_{len(repair_rows)+1:04d}",
                    "source_candidate_id": source["source_candidate_id"],
                    "source_features": item["features"],
                    "source_rule_definition": item["rule_definition"],
                    "side_value": source_side,
                    "side": item["side"],
                    "repair_type": repair_type,
                    "filter_condition_id": filter_row["condition_id"],
                    "filter_feature": filter_feature,
                    "filter_family": filter_row["feature_family"],
                    "filter_definition": filter_row["definition"],
                    "rule_definition": f"{item['rule_definition']} {'&' if repair_type == 'include' else '& NOT'} ({filter_row['definition']})",
                    "train_repair_score": score,
                    "source_train_profit_factor": source_train["profit_factor"],
                    "source_train_payoff_ratio": source_train["payoff_ratio"],
                    "source_train_adverse_loss_p10_abs": source_train["adverse_loss_p10_abs"],
                    "mask": repaired_mask,
                    "train_selection_metrics": metrics,
                })
    repair_rows.sort(key=lambda row: float(row["train_repair_score"]), reverse=True)
    selected = repair_rows[:MAX_REPAIR_CANDIDATES]
    for index, row in enumerate(selected, start=1):
        row["repair_id"] = f"f23c_{index:04d}"
    return selected


def repair_score(metrics: dict[str, Any], source_train: dict[str, Any]) -> float:
    pf_lift = float(metrics["profit_factor"]) - float(source_train["profit_factor"])
    payoff_lift = float(metrics["payoff_ratio"]) - float(source_train["payoff_ratio"])
    adverse_lift = float(source_train["adverse_loss_p10_abs"]) - float(metrics["adverse_loss_p10_abs"])
    if pf_lift < 0.02 and payoff_lift < 0.03 and adverse_lift <= 0:
        return 0.0
    density_penalty = abs(float(metrics["trades_per_day"]) - 7.5) / 7.5
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 12.0) / 18.0
    return float(
        (1.0 + max(pf_lift, 0.0))
        * (1.0 + max(payoff_lift, 0.0))
        * (1.0 + max(adverse_lift * 100.0, 0.0))
        * max(metrics["net_profit"], 0.0)
        * min(metrics["profit_factor"], 4.0)
        / (1.0 + density_penalty + dd_penalty)
    )


def evaluate_repair_candidates(frame: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(candidates, start=1):
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "repair_id": candidate["repair_id"],
                "train_rank": rank,
                "source_candidate_id": candidate["source_candidate_id"],
                "source_features": candidate["source_features"],
                "side": candidate["side"],
                "side_value": candidate["side_value"],
                "repair_type": candidate["repair_type"],
                "filter_condition_id": candidate["filter_condition_id"],
                "filter_feature": candidate["filter_feature"],
                "filter_family": candidate["filter_family"],
                "rule_definition": candidate["rule_definition"],
                "split": split,
                "record_view": "Tier A separate(티어 A 분리)",
                "tier_scope": "Tier A(티어 A)",
                "trade_count": metrics["trade_count"],
                "days_in_scope": metrics["days_in_scope"],
                "trades_per_day": metrics["trades_per_day"],
                "net_profit": metrics["net_profit"],
                "profit_factor": metrics["profit_factor"],
                "expectancy": metrics["expectancy"],
                "win_rate": metrics["win_rate"],
                "payoff_ratio": metrics["payoff_ratio"],
                "right_tail_loss_tail_ratio": metrics["right_tail_loss_tail_ratio"],
                "adverse_loss_p10_abs": metrics["adverse_loss_p10_abs"],
                "dd_risk": metrics["dd_risk"],
                "underwater_ratio": metrics["underwater_ratio"],
                "max_loss_streak": metrics["max_loss_streak"],
                "equity_trend_r2": metrics["equity_trend_r2"],
                "selection_boundary": "train_only_repair_rank(학습 전용 수리 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    return pd.DataFrame(rows)


def summarize_repair(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for repair_id, group in metrics.groupby("repair_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "repair_id": repair_id,
            "train_rank": int(train["train_rank"]),
            "source_candidate_id": train["source_candidate_id"],
            "source_features": train["source_features"],
            "side": train["side"],
            "repair_type": train["repair_type"],
            "filter_feature": train["filter_feature"],
            "filter_family": train["filter_family"],
            "rule_definition": train["rule_definition"],
        }
        for prefix, row in (("train", train), ("validation", validation), ("oos", oos)):
            for field in (
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "payoff_ratio",
                "right_tail_loss_tail_ratio",
                "adverse_loss_p10_abs",
                "dd_risk",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
            ):
                base[f"{prefix}_{field}"] = row[field]
        base["scout_clue_flag"] = bool(
            validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and validation["profit_factor"] >= SCOUT_MIN_PF
            and oos["profit_factor"] >= SCOUT_MIN_PF
            and SCOUT_DENSITY_LOW <= validation["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and SCOUT_DENSITY_LOW <= oos["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and max(validation["dd_risk"], oos["dd_risk"]) <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(
            base["scout_clue_flag"]
            and validation["profit_factor"] >= SEED_PF
            and oos["profit_factor"] >= SEED_PF
            and f23b.SEED_DENSITY_LOW <= validation["trades_per_day"] <= f23b.SEED_DENSITY_HIGH
            and f23b.SEED_DENSITY_LOW <= oos["trades_per_day"] <= f23b.SEED_DENSITY_HIGH
            and max(validation["dd_risk"], oos["dd_risk"]) <= SEED_DD_CAP
        )
        base["handoff_candidate_flag"] = bool(
            base["seed_surface_flag"]
            and validation["profit_factor"] >= HANDOFF_PF
            and oos["profit_factor"] >= HANDOFF_PF
            and max(validation["dd_risk"], oos["dd_risk"]) <= HANDOFF_DD_CAP
            and validation["equity_trend_r2"] >= 0.35
            and oos["equity_trend_r2"] >= 0.35
        )
        base["forward_read_score"] = float(
            min(validation["profit_factor"], 4.0)
            * min(oos["profit_factor"], 4.0)
            * min(validation["payoff_ratio"], 4.0)
            * min(oos["payoff_ratio"], 4.0)
            * min(validation["trades_per_day"], oos["trades_per_day"], 12.0)
            / (1.0 + max(validation["dd_risk"], oos["dd_risk"]) / 10.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "forward_read_score"],
        ascending=[False, False, False, False],
    )


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def build_final(
    created_at: str,
    f23b_summary: dict[str, Any],
    feature_order: list[str],
    context: dict[str, Any],
    sources: list[dict[str, Any]],
    repair_candidates: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    if handoff_count:
        status = "payoff_asymmetry_entry_filter_repair_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "payoff_asymmetry_entry_filter_repair_seed_surface_proxy_no_authority"
        judgment = "seed_surface_preserved_clue_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "payoff_asymmetry_entry_filter_repair_scout_clue_proxy_no_authority"
        judgment = "preserved_clue_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    else:
        status = "payoff_asymmetry_entry_filter_repair_no_seed_or_handoff_proxy_no_authority"
        judgment = "negative_pressure_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
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
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "context": context,
        "f23b_summary": {
            "status": f23b_summary.get("status"),
            "scout_clue_rows": f23b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f23b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f23b_summary.get("handoff_candidate_rows"),
            "best_candidate_id": f23b_summary.get("best_candidate_id"),
        },
        "source_candidate_count": int(len(sources)),
        "repair_candidate_rows": int(len(repair_candidates)),
        "metric_rows": int(len(metrics)) if not metrics.empty else 0,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_repair_id": best.get("repair_id", ""),
        "best_repair": json_ready(best),
        "result_boundary": "capped_entry_filter_repair_proxy_no_wfo_no_mt5_no_runtime_authority(상한 진입 필터 수리 프록시, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 그록 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], repair_candidates: list[dict[str, Any]], metrics: pd.DataFrame, summary: pd.DataFrame) -> None:
    pd.DataFrame([clean_candidate_for_csv(row) for row in repair_candidates]).to_csv(io_path(RUN_ROOT / "train_ranked_repair_candidates.csv"), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(RUN_ROOT / "repair_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "repair_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md", gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F23B_SUMMARY,
        F23B_CANDIDATES,
        RUN_ROOT / "train_ranked_repair_candidates.csv",
        RUN_ROOT / "repair_metrics_by_split.csv",
        RUN_ROOT / "repair_candidate_summary.csv",
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
        "feature_schema": {
            "feature_count": final["feature_count"],
            "feature_order_hash": final["feature_order_hash"],
            "feature_order_path": f23b.FEATURE_ORDER_PATH.as_posix(),
        },
        "rule_stack": {
            "entry": "F23B payoff asymmetry source candidates(F23B 보상 비대칭 원천 후보)",
            "repair": "train-only include/veto entry-known filter(학습 전용 포함/제외 진입시점 필터)",
            "forbidden": "no lifecycle repair, no ONNX, no MT5 before handoff(인계 전 생명주기 수리/ONNX/MT5 없음)",
        },
        "results": {
            "cross_split": {
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_repair_id": final["best_repair_id"],
            },
            "report_refs": [{"role": "entry_filter_repair_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier23c_entry_filter_repair_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_repair"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['repair_id']}` | `{row['source_candidate_id']}` | {row['repair_type']} | `{row['filter_feature']}` | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | |"
    return f"""# Frontier23C Payoff Asymmetry Entry Filter Repair Report(전선23C 보상 비대칭 진입 필터 수리 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F23B(전선23B) scout clue(탐색 단서)에 train-only include/veto filter(학습 전용 포함/제외 필터)를 붙여 entry-known repair(진입시점 수리)를 실행했습니다.

Effect(효과): seed(씨앗) 전 lifecycle repair(생명주기 수리) 없이 PF(수익 팩터), density(빈도), DD(손실폭)가 같이 좋아지는지 확인했습니다.

Source/repair/metric rows(원천/수리/지표 행): `{final['source_candidate_count']}` / `{final['repair_candidate_rows']}` / `{final['metric_rows']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best repair(최상 수리): `{final['best_repair_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Repair Rows(상위 수리 행)

| repair(수리) | source(원천) | type(유형) | filter(필터) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier23C Gate Audit(전선23C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): repair artifacts created(수리 산출물 생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- capped_repair_gate(상한 수리 게이트): source candidates(원천 후보) `{final['source_candidate_count']}`, repair candidates(수리 후보) `{final['repair_candidate_rows']}`
- no_lifecycle_before_seed_gate(씨앗 전 생명주기 금지 게이트): pass(통과), only entry-known filters used(진입시점 필터만 사용)
- kpi_contract_audit(KPI 계약 감사): repair metrics/summary(수리 지표/요약) created(생성)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier23 Selection Status(전선23 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest repair(최근 수리): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best repair(최상 수리): `{final['best_repair_id']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

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
    best = final["best_repair"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "payoff_asymmetry_entry_filter_repair(보상 비대칭 진입 필터 수리)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_repair_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_repair_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "capped_entry_filter_repair_no_wfo_no_mt5_no_authority(상한 진입 필터 수리, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_repair"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_entry_filter_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_entry_filter_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "payoff_asymmetry_entry_filter_repair_not_runtime(보상 비대칭 진입 필터 수리, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_repair_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "capped_repair_proxy_no_wfo_no_mt5_no_authority(상한 수리 프록시, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran capped entry-filter repair(상한 진입 필터 수리). "
        f"Effect(효과): scout/seed/handoff(탐색/씨앗/인계) counts are {final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR23-PAYOFF-ASYMMETRY-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` applied capped entry-known include/veto repair(상한 진입시점 포함/제외 수리). "
        f"Effect(효과): best repair `{final['best_repair_id']}` remains no-authority(권위 없음) until closeout or pre-expensive review.\n"
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
    best = final["best_repair"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F23C(전선23C)가 F23B payoff asymmetry scout clue(전선23B 보상 비대칭 탐색 단서)에 capped entry filter repair(상한 진입 필터 수리)를 적용했습니다.

Effect(효과): lifecycle repair(생명주기 수리) 없이 진입시점에 알 수 있는 include/veto filter(포함/제외 필터)만으로 PF(수익 팩터), density(빈도), DD(손실폭)가 같이 좋아지는지 확인했습니다.

Best repair(최상 수리): `{final['best_repair_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def clean_candidate_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    cleaned = {key: value for key, value in row.items() if key not in {"mask", "train_selection_metrics"}}
    cleaned.update({f"train_{key}": value for key, value in row.get("train_selection_metrics", {}).items()})
    return cleaned


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "pending_or_missing(대기 또는 누락)"}


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
