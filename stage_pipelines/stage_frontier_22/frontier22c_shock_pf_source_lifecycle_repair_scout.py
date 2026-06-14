from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import dataclass
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
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b
from stage_pipelines.stage_frontier_21.frontier21b_f20_seed_lifecycle_proxy_scout import (
    LifecycleProfile,
    evaluate_aggregates,
    evaluate_subperiods,
    simulate_profile,
)
from stage_pipelines.stage_frontier_22 import frontier22b_session_return_shock_pf_source_proxy_scout as f22b


STAGE_ID = "stage_frontier_22__session_return_shock_pf_source_onnx_scout"
RUN_ID = "frontier22C_shock_pf_source_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier22C"
PARENT_RUN_ID = "frontier22B_session_return_shock_pf_source_proxy_scout_v1"
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier22D_grok_pre_expensive_shock_lifecycle_handoff_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier22D_stage_closeout_shock_pf_source_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_22/frontier22c_shock_pf_source_lifecycle_repair_scout.py")

F22A_LOCK = STAGE_ROOT / "02_runs" / f22b.PARENT_RUN_ID / "shock_pf_source_lock.json"
F22B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "final_summary.json"
F22B_CANDIDATES = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "candidate_summary.csv"
FEATURE_ORDER_PATH = f22b.FEATURE_ORDER_PATH

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

TOP_SOURCE_CANDIDATES = 8
SCOUT_MIN_PF = 1.05
SCOUT_DENSITY_LOW = 3.0
SCOUT_DENSITY_HIGH = 12.0
SCOUT_DD_CAP = 25.0
SEED_PF = 1.20
SEED_DD_CAP = 15.0
HANDOFF_PF = 1.50
HANDOFF_DD_CAP = 12.0

REPAIR_GRID = (
    LifecycleProfile("hold2_atr0p8_tp1p6_cd0", "fast_low_dd_repair(빠른 낮은 손실폭 수리)", 2, 0.8, 1.6, 0, False),
    LifecycleProfile("hold4_atr0p8_tp1p6_cd1", "compact_containment(압축 위험 억제)", 4, 0.8, 1.6, 1, False),
    LifecycleProfile("hold6_atr1p0_tp2p0_cd2", "balanced_containment(균형 위험 억제)", 6, 1.0, 2.0, 2, False),
    LifecycleProfile("hold8_atr1p2_tp2p4_cd3", "wide_containment(넓은 위험 억제)", 8, 1.2, 2.4, 3, False),
)


@dataclass(frozen=True)
class SourceCandidate:
    candidate_id: str
    signal: np.ndarray
    metadata: dict[str, Any]


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    lock = read_json(F22A_LOCK)
    f22b_summary = read_json(F22B_SUMMARY)
    f22b_candidates = pd.read_csv(io_path(F22B_CANDIDATES))
    feature_order = f22b.read_feature_order()
    full, raw, source_integrity = f07b.load_training_packet()
    context = validate_context(lock, f22b_summary, full, feature_order)
    selected_sources = rebuild_source_candidates(full, lock, f22b_candidates)
    result = run_repair_grid(full, raw, selected_sources)
    summary = summarize_repair(result["metrics"], f22b_candidates)
    final = build_final(created_at, lock, f22b_summary, feature_order, source_integrity, context, selected_sources, result, summary)
    write_outputs(final, result, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "source_candidate_count": final["source_candidate_count"],
        "profile_count": final["profile_count"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_profile_id": final["best_profile_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(lock: dict[str, Any], f22b_summary: dict[str, Any], full: pd.DataFrame, feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier22": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier22c": f"next_run_id: {RUN_ID}" in workspace,
        "f22b_parent_matches": f22b_summary.get("run_id") == PARENT_RUN_ID,
        "f22b_has_scout_no_seed": int(f22b_summary.get("scout_clue_rows", 0)) > 0 and int(f22b_summary.get("seed_surface_rows", 0)) == 0,
        "lock_forbids_first_proxy_lifecycle_only": "f21_guard" in lock.get("locks", {}),
        "feature_order_hash_matches_contract": ordered_hash(feature_order) == f22b.EXPECTED_FEATURE_HASH,
        "raw_index_available": "raw_index" in full.columns,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier22C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def rebuild_source_candidates(full: pd.DataFrame, lock: dict[str, Any], f22b_candidates: pd.DataFrame) -> list[SourceCandidate]:
    condition_pool = f22b.build_condition_pool(full, lock["buckets"])
    candidate_pool = f22b.build_candidate_pool(full, condition_pool)
    selected = f22b.select_candidates(full, candidate_pool)
    selected_by_id = {item["candidate_id"]: item for item in selected}

    ordered = f22b_candidates.copy()
    if "scout_clue_flag" in ordered:
        scout_mask = ordered["scout_clue_flag"].astype(str).str.lower().eq("true")
        if scout_mask.any():
            ordered = ordered.loc[scout_mask].copy()
    ordered = ordered.sort_values("forward_read_score", ascending=False).head(TOP_SOURCE_CANDIDATES)
    sources: list[SourceCandidate] = []
    for _, row in ordered.iterrows():
        candidate_id = str(row["candidate_id"])
        item = selected_by_id.get(candidate_id)
        if item is None:
            continue
        signal = np.asarray(item["mask"], dtype=bool).astype("int64") * int(item["side"])
        sources.append(SourceCandidate(candidate_id=candidate_id, signal=signal, metadata=dict(row)))
    if not sources:
        raise RuntimeError("No source candidates could be rebuilt(원천 후보 재구성 실패).")
    return sources


def run_repair_grid(full: pd.DataFrame, raw: pd.DataFrame, selected_sources: list[SourceCandidate]) -> dict[str, Any]:
    trade_rows: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    subperiod_rows: list[dict[str, Any]] = []
    for source in selected_sources:
        for base_profile in REPAIR_GRID:
            profile = LifecycleProfile(
                profile_id=f"{source.candidate_id}__{base_profile.profile_id}",
                role=base_profile.role,
                max_hold_bars=base_profile.max_hold_bars,
                atr_stop_multiplier=base_profile.atr_stop_multiplier,
                atr_take_profit_multiplier=base_profile.atr_take_profit_multiplier,
                cooldown_bars=base_profile.cooldown_bars,
                early_adverse_exit_enabled=base_profile.early_adverse_exit_enabled,
            )
            trades = simulate_profile(full, raw, source.signal, profile)
            for row in trades:
                row["source_candidate_id"] = source.candidate_id
                row["source_rule_definition"] = source.metadata.get("rule_definition", "")
            trade_rows.extend(trades)
            metric_rows.extend(add_source_to_rows(evaluate_aggregates(trades, profile), source))
            subperiod_rows.extend(add_source_to_rows(evaluate_subperiods(trades, profile), source))
    return {
        "trades": trade_rows,
        "metrics": metric_rows,
        "subperiod_metrics": subperiod_rows,
    }


def add_source_to_rows(rows: list[dict[str, Any]], source: SourceCandidate) -> list[dict[str, Any]]:
    for row in rows:
        row["source_candidate_id"] = source.candidate_id
        row["source_rule_definition"] = source.metadata.get("rule_definition", "")
        row["source_lane"] = source.metadata.get("lane", "")
        row["source_shock_feature"] = source.metadata.get("shock_feature", "")
        row["source_context_feature"] = source.metadata.get("context_feature", "")
    return rows


def summarize_repair(metrics: list[dict[str, Any]], f22b_candidates: pd.DataFrame) -> pd.DataFrame:
    frame = pd.DataFrame(metrics)
    rows: list[dict[str, Any]] = []
    for profile_id, group in frame.groupby("profile_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        source_id = str(train["source_candidate_id"])
        source = dict(f22b_candidates.loc[f22b_candidates["candidate_id"].astype(str).eq(source_id)].iloc[0])
        base = {
            "profile_id": profile_id,
            "source_candidate_id": source_id,
            "source_lane": train.get("source_lane", ""),
            "source_rule_definition": train.get("source_rule_definition", ""),
            "source_shock_feature": train.get("source_shock_feature", ""),
            "source_context_feature": train.get("source_context_feature", ""),
            "max_hold_bars": train["max_hold_bars"],
            "atr_stop_multiplier": train["atr_stop_multiplier"],
            "atr_take_profit_multiplier": train["atr_take_profit_multiplier"],
            "cooldown_bars": train["cooldown_bars"],
            "source_validation_pf": source.get("validation_profit_factor"),
            "source_oos_pf": source.get("oos_profit_factor"),
            "source_validation_dd": source.get("validation_dd_risk"),
            "source_oos_dd": source.get("oos_dd_risk"),
        }
        for prefix, row in (("train", train), ("validation", validation), ("oos", oos)):
            for field in (
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "dd_risk_percent",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
            ):
                source_field = "dd_risk_percent" if field == "dd_risk_percent" else field
                base[f"{prefix}_{field}"] = row.get(source_field)
        base["scout_clue_flag"] = bool(
            validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and validation["profit_factor"] >= SCOUT_MIN_PF
            and oos["profit_factor"] >= SCOUT_MIN_PF
            and SCOUT_DENSITY_LOW <= validation["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and SCOUT_DENSITY_LOW <= oos["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and max(validation["dd_risk_percent"], oos["dd_risk_percent"]) <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(
            validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and validation["profit_factor"] >= SEED_PF
            and oos["profit_factor"] >= SEED_PF
            and f22b.scout.DENSITY_TARGET_LOW <= validation["trades_per_day"] <= f22b.scout.DENSITY_TARGET_HIGH
            and f22b.scout.DENSITY_TARGET_LOW <= oos["trades_per_day"] <= f22b.scout.DENSITY_TARGET_HIGH
            and max(validation["dd_risk_percent"], oos["dd_risk_percent"]) <= SEED_DD_CAP
        )
        base["handoff_candidate_flag"] = bool(
            base["seed_surface_flag"]
            and validation["profit_factor"] >= HANDOFF_PF
            and oos["profit_factor"] >= HANDOFF_PF
            and max(validation["dd_risk_percent"], oos["dd_risk_percent"]) <= HANDOFF_DD_CAP
            and validation["equity_trend_r2"] >= 0.35
            and oos["equity_trend_r2"] >= 0.35
        )
        base["repair_score"] = float(
            min(validation["profit_factor"], 3.0)
            * min(oos["profit_factor"], 3.0)
            * min(validation["trades_per_day"], oos["trades_per_day"], 12.0)
            / (1.0 + max(validation["dd_risk_percent"], oos["dd_risk_percent"]) / 12.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "repair_score"],
        ascending=[False, False, False, False],
    )


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def build_final(
    created_at: str,
    lock: dict[str, Any],
    f22b_summary: dict[str, Any],
    feature_order: list[str],
    source_integrity: dict[str, Any],
    context: dict[str, Any],
    selected_sources: list[SourceCandidate],
    result: dict[str, Any],
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["scout_clue_flag"].sum()) if "scout_clue_flag" in summary else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if "seed_surface_flag" in summary else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if "handoff_candidate_flag" in summary else 0
    if handoff_count:
        status = "shock_lifecycle_repair_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "shock_lifecycle_repair_seed_surface_proxy_no_authority"
        judgment = "seed_surface_preserved_clue_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "shock_lifecycle_repair_scout_clue_proxy_no_authority"
        judgment = "preserved_clue_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    else:
        status = "shock_lifecycle_repair_no_seed_or_handoff_proxy_no_authority"
        judgment = "negative_pressure_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    best = dict(summary.iloc[0]) if len(summary) else {}
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
        "source_integrity": source_integrity,
        "context": context,
        "lock": lock,
        "f22b_summary": {
            "status": f22b_summary.get("status"),
            "scout_clue_rows": f22b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f22b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f22b_summary.get("handoff_candidate_rows"),
            "best_candidate_id": f22b_summary.get("best_candidate_id"),
        },
        "source_candidate_count": len(selected_sources),
        "profile_count": len(REPAIR_GRID),
        "metric_rows": len(result["metrics"]),
        "subperiod_metric_rows": len(result["subperiod_metrics"]),
        "trade_rows": len(result["trades"]),
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_profile_id": best.get("profile_id", ""),
        "best_profile": json_ready(best),
        "result_boundary": "capped_repair_proxy_no_wfo_no_mt5_no_runtime_authority(상한 수리 프록시, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 그록 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], result: dict[str, Any], summary: pd.DataFrame) -> None:
    artifacts = {
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "final_summary": RUN_ROOT / "final_summary.json",
        "repair_candidate_summary": RUN_ROOT / "repair_candidate_summary.csv",
        "metrics_by_split": RUN_ROOT / "metrics_by_split.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "trade_log": RUN_ROOT / "trade_log.csv",
        "report": REPORT_PATH,
        "gate_audit": STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md",
    }
    write_json(artifacts["run_manifest"], run_manifest(final, artifacts))
    write_json(artifacts["final_summary"], final)
    summary.to_csv(io_path(artifacts["repair_candidate_summary"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["metrics"]).to_csv(io_path(artifacts["metrics_by_split"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["subperiod_metrics"]).to_csv(io_path(artifacts["subperiod_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["trades"]).to_csv(io_path(artifacts["trade_log"]), index=False, encoding="utf-8-sig")
    f03b.write_text_sig(REPORT_PATH, report_text(final, artifacts))
    f03b.write_text_sig(artifacts["gate_audit"], gate_audit(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(F22A_LOCK),
            artifact_identity(F22B_SUMMARY),
            artifact_identity(F22B_CANDIDATES),
            *[artifact_identity(path) for path in artifacts.values() if path != artifacts["run_manifest"]],
        ],
        "feature_schema": {
            "feature_count": final["feature_count"],
            "feature_order_hash": final["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "runtime_snapshot": {
            "symbol": "US100",
            "timeframe": "M5",
            "entry_timing": "closed_bar_signal_next_bar_open_proxy(종료봉 신호 다음 봉 시가 프록시)",
            "max_concurrent_positions": 1,
            "cost_behavior": "rough_log_return_cost_proxy_only(거친 로그수익 비용 프록시 전용)",
        },
        "rule_stack": {
            "entry": "top_f22b_shock_context_candidates(상위 F22B 충격/문맥 후보)",
            "position_exit": "capped_lifecycle_repair_grid(상한 생명주기 수리 격자)",
        },
        "results": {
            "by_split": {"proxy": "metrics_by_split.csv"},
            "cross_split": {
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_profile_id": final["best_profile_id"],
            },
            "report_refs": [{"role": "repair_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier22c_lifecycle_repair_proxy_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
            "required_output_schema": "not_applicable_no_onnx_export_yet(ONNX 내보내기 전이라 해당 없음)",
        },
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_profile"]
    return f"""# Frontier22C Shock PF Source Lifecycle Repair Scout Report(전선22C 충격 수익 팩터 원천 생명주기 수리 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F22B(전선22B)의 상위 shock+context scout clue(충격+문맥 탐색 단서)에 capped lifecycle repair(상한 생명주기 수리)를 적용했습니다.

Effect(효과): F21 생명주기 수리를 반복 원천으로 쓰지 않고, F22의 PF source(수익 팩터 원천)가 있을 때 DD(손실폭)를 억제할 수 있는지만 좁게 확인했습니다.

Source/profile rows(원천/프로필 수): `{final['source_candidate_count']}` / `{final['profile_count']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best repair profile(최상 수리 프로필): `{final['best_profile_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk_percent'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk_percent'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Artifacts(산출물): `{artifacts['repair_candidate_summary'].as_posix()}`, `{artifacts['metrics_by_split'].as_posix()}`, `{artifacts['trade_log'].as_posix()}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier22C Gate Audit(전선22C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): repair artifacts created(수리 산출물 생성) `{artifacts['final_summary'].as_posix()}`
- kpi_contract_audit(KPI 계약 감사): metrics/summary/trade log(지표/요약/거래 기록) created(생성)
- capped_repair_gate(상한 수리 게이트): source candidates(원천 후보) `{final['source_candidate_count']}`, profiles(프로필) `{final['profile_count']}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier22 Selection Status(전선22 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest repair(최근 수리): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best repair profile(최상 수리 프로필): `{final['best_profile_id']}`

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
    best = final["best_profile"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "shock_lifecycle_repair_proxy_scout(충격 생명주기 수리 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_profile_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_profile_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk_percent'))}",
        "guardrail_kpi": "capped_repair_proxy_no_wfo_no_mt5_no_authority(상한 수리 프록시, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_profile"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_lifecycle_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_lifecycle_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "shock_lifecycle_repair_proxy_not_runtime(충격 생명주기 수리 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_profile_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk_percent'))}",
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
        f"- {final['created_at_utc']}: `{RUN_ID}` ran capped lifecycle repair on F22B shock clues(F22B 충격 단서 상한 생명주기 수리). "
        f"Effect(효과): scout/seed/handoff(탐색/씨앗/인계) counts are {final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR22-SESSION-RETURN-SHOCK-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` applied capped lifecycle repair(상한 생명주기 수리) to F22B shock clues(F22B 충격 단서). "
        f"Effect(효과): best repair `{final['best_profile_id']}` remains no-authority(권위 없음) until closeout or pre-expensive review.\n"
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
    best = final["best_profile"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F22C(전선22C)가 F22B shock clue(충격 단서)에 capped lifecycle repair(상한 생명주기 수리)를 적용했습니다.

Effect(효과): PF source(수익 팩터 원천)를 바꾸지 않고 DD(손실폭) 억제 가능성만 좁게 확인했습니다.

Best repair(최상 수리): `{final['best_profile_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk_percent'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk_percent'))}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


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
