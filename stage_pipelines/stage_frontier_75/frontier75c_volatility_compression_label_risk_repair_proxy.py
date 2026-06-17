from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from stage_pipelines.stage_frontier_75 import frontier75b_volatility_compression_liquidity_release_proxy_scout as base


ROOT = base.ROOT
STAGE_ID = base.STAGE_ID
RUN_ID = "frontier75C_volatility_compression_label_risk_repair_proxy_v1"
PARENT_RUN_ID = base.RUN_ID
CLAIM_BOUNDARY = (
    "proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

RUN_DIR = ROOT / "stages" / STAGE_ID / "02_runs" / RUN_ID
REVIEW_DIR = ROOT / "stages" / STAGE_ID / "03_reviews"
REPORT_PATH = f"stages/{STAGE_ID}/03_reviews/frontier75C_volatility_compression_label_risk_repair_proxy_report.md"
GATE_AUDIT_PATH = f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f75c.md"
RUN_MANIFEST_PATH = f"stages/{STAGE_ID}/02_runs/{RUN_ID}/run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR):
        base.fs_path(path).mkdir(parents=True, exist_ok=True)


def add_repair_features(df: pd.DataFrame, feature_order: list[str]) -> tuple[pd.DataFrame, list[str]]:
    repaired = df.copy()
    repaired["prev_bw_3_min"] = repaired["bollinger_width_20"].shift(1).rolling(3, min_periods=1).min()
    repaired["prev_bw_6_min"] = repaired["bollinger_width_20"].shift(1).rolling(6, min_periods=2).min()
    repaired["prev_hv_3_mean"] = repaired["historical_vol_5_over_20"].shift(1).rolling(3, min_periods=1).mean()
    repaired["prev_squeeze_3_max"] = repaired["bb_squeeze"].shift(1).rolling(3, min_periods=1).max()
    repaired["release_range_z"] = repaired["hl_zscore_50"]
    repaired["short_return_shock"] = -repaired["return_zscore_20"]
    repaired["negative_di_pressure"] = -repaired["di_spread_14"]
    repaired["short_release_rule_score"] = (
        repaired["short_return_shock"].clip(lower=-3, upper=5)
        + repaired["release_range_z"].clip(lower=-3, upper=5) * 0.5
        + repaired["negative_di_pressure"].clip(lower=-30, upper=30) / 15.0
    )
    derived = [
        "prev_bw_3_min",
        "prev_bw_6_min",
        "prev_hv_3_mean",
        "prev_squeeze_3_max",
        "release_range_z",
        "short_return_shock",
        "negative_di_pressure",
        "short_release_rule_score",
    ]
    return repaired, feature_order + derived


def context_masks(df: pd.DataFrame) -> dict[str, np.ndarray]:
    train = df["split"].eq("train")
    bw30 = float(df.loc[train, "prev_bw_3_min"].quantile(0.30))
    bw40 = float(df.loc[train, "prev_bw_6_min"].quantile(0.40))
    hv35 = float(df.loc[train, "prev_hv_3_mean"].quantile(0.35))
    ret65 = float(df.loc[train, "short_return_shock"].quantile(0.65))
    range65 = float(df.loc[train, "release_range_z"].quantile(0.65))
    di65 = float(df.loc[train, "negative_di_pressure"].quantile(0.65))
    rule70 = float(df.loc[train, "short_release_rule_score"].quantile(0.70))
    return {
        "prior_bw_downshock": (df["prev_bw_3_min"].le(bw30) & df["short_return_shock"].ge(ret65)).to_numpy(),
        "prior_hv_range_expand": (df["prev_hv_3_mean"].le(hv35) & df["release_range_z"].ge(range65)).to_numpy(),
        "squeeze_exit_short": (df["prev_squeeze_3_max"].ge(1) & df["bb_squeeze"].lt(1) & df["short_return_shock"].gt(0)).to_numpy(),
        "prior_bw_di_release": (df["prev_bw_6_min"].le(bw40) & df["negative_di_pressure"].ge(di65)).to_numpy(),
        "repair_rule_score_q70": df["short_release_rule_score"].ge(rule70).to_numpy(),
    }


def session_masks(df: pd.DataFrame) -> dict[str, np.ndarray]:
    minutes = df["minutes_from_cash_open"]
    cash = df["is_us_cash_open"].eq(1)
    return {
        "cash_all": cash.to_numpy(),
        "cash_open_180": (cash & minutes.ge(0) & minutes.le(180)).to_numpy(),
        "cash_mid_late": (cash & minutes.ge(90)).to_numpy(),
        "cash_late_150": (cash & minutes.ge(240)).to_numpy(),
    }


def feature_bundles(feature_order: list[str]) -> dict[str, list[str]]:
    derived_core = [
        "prev_bw_3_min",
        "prev_bw_6_min",
        "prev_hv_3_mean",
        "prev_squeeze_3_max",
        "release_range_z",
        "short_return_shock",
        "negative_di_pressure",
        "short_release_rule_score",
        "bollinger_width_20",
        "historical_vol_5_over_20",
        "bb_squeeze",
        "atr_14",
        "atr_14_over_atr_50",
        "adx_14",
        "di_spread_14",
        "return_zscore_20",
        "hl_zscore_50",
        "minutes_from_cash_open",
    ]
    macro = [
        "vix_change_1",
        "vix_zscore_20",
        "us10yr_change_1",
        "usdx_change_1",
        "mega8_equal_return_1",
        "mega8_dispersion_5",
        "us100_minus_mega8_equal_return_1",
        "us100_minus_top3_weighted_return_1",
    ]
    available = set(feature_order)
    return {
        "repair_core": [col for col in derived_core if col in available],
        "repair_macro": [col for col in derived_core + macro if col in available],
        "all58_plus_repair": feature_order,
    }


def density_rows(
    df: pd.DataFrame,
    outcomes: dict[tuple[int, float, float], tuple[np.ndarray, np.ndarray, np.ndarray]],
    contexts: dict[str, np.ndarray],
    sessions: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    rows = []
    for (horizon, target_mult, stop_mult), (pnl, _, future_ok) in outcomes.items():
        profitable = pnl > 0
        for context_name, context_mask in contexts.items():
            for session_name, session_mask in sessions.items():
                mask = context_mask & session_mask & future_ok
                row: dict[str, Any] = {
                    "direction": "short",
                    "horizon": horizon,
                    "target_atr_mult": target_mult,
                    "stop_atr_mult": stop_mult,
                    "context_gate": context_name,
                    "session_gate": session_name,
                }
                for split in ("train", "validation", "oos"):
                    split_mask = mask & df["split"].eq(split).to_numpy()
                    count = int(split_mask.sum())
                    positive = int((split_mask & profitable).sum())
                    row[f"{split}_rows"] = count
                    row[f"{split}_positive"] = positive
                    row[f"{split}_positive_rate"] = float(positive / count) if count else 0.0
                rows.append(row)
    return rows


def classify(row: dict[str, Any]) -> tuple[int, int, int]:
    val_pf = float(row["validation_profit_factor"])
    oos_pf = float(row["oos_profit_factor"])
    val_net = float(row["validation_net_profit"])
    oos_net = float(row["oos_net_profit"])
    val_dd = float(row["validation_max_drawdown_percent"])
    oos_dd = float(row["oos_max_drawdown_percent"])
    oos_tpd = float(row["oos_trades_day"])
    scout = int(val_net > 0 and oos_net > 0 and val_pf >= 1.20 and oos_pf >= 1.15 and val_dd < 10 and oos_dd < 10)
    meaningful = int(scout and val_pf >= 1.45 and oos_pf >= 1.30 and oos_tpd >= 3.0)
    final_like = int(meaningful and val_pf >= 2.0 and oos_pf >= 2.0 and 5.0 <= oos_tpd <= 10.0)
    return scout, meaningful, final_like


def run_repair(df: pd.DataFrame, feature_order: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    close = df["close"].to_numpy(dtype=float)
    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    spread_cost = df["spread_points"].to_numpy(dtype=float) * base.SPREAD_POINT_VALUE
    atr = df["atr_14"].to_numpy(dtype=float)
    contexts = context_masks(df)
    sessions = session_masks(df)
    bundles = feature_bundles(feature_order)
    builders = base.model_builders()
    label_configs = [
        {"horizon": 3, "target_mult": 0.45, "stop_mult": 0.30},
        {"horizon": 6, "target_mult": 0.60, "stop_mult": 0.35},
        {"horizon": 9, "target_mult": 0.80, "stop_mult": 0.45},
        {"horizon": 12, "target_mult": 1.00, "stop_mult": 0.55},
    ]
    target_trade_days = [3.5, 5.0, 8.0, 10.0]
    split_day_counts = {split: base.split_days(df, split) for split in ("train", "validation", "oos")}
    outcomes: dict[tuple[int, float, float], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for config in label_configs:
        horizon = int(config["horizon"])
        future_ok = base.future_continuity_ok(df["timestamp"], horizon)
        pnl, exit_bars = base.first_touch_outcome(
            close=close,
            high=high,
            low=low,
            spread_cost=spread_cost,
            atr=atr,
            future_ok=future_ok,
            horizon=horizon,
            target_mult=float(config["target_mult"]),
            stop_mult=float(config["stop_mult"]),
            direction="short",
        )
        outcomes[(horizon, float(config["target_mult"]), float(config["stop_mult"]))] = (pnl, exit_bars, future_ok)

    density = density_rows(df, outcomes, contexts, sessions)
    split_values = df["split"].to_numpy()
    train_base = split_values == "train"
    val_base = split_values == "validation"
    oos_base = split_values == "oos"
    results: list[dict[str, Any]] = []
    candidate_id = 0

    for (horizon, target_mult, stop_mult), (pnl, exit_bars, future_ok) in outcomes.items():
        y = (pnl > 0).astype(int)
        valid_label = np.isfinite(pnl) & future_ok
        for context_name, context_mask in contexts.items():
            for session_name, session_mask in sessions.items():
                gate = context_mask & session_mask & valid_label
                train_mask = gate & train_base
                val_mask = gate & val_base
                oos_mask = gate & oos_base
                if int(train_mask.sum()) < 350 or int(val_mask.sum()) < 70 or int(oos_mask.sum()) < 70:
                    continue
                if int((train_mask & (y == 1)).sum()) < 35 or int((train_mask & (y == 0)).sum()) < 35:
                    continue
                for bundle_name, cols in bundles.items():
                    if len(cols) < 8:
                        continue
                    X_train = df.loc[train_mask, cols]
                    y_train = y[train_mask]
                    for model_name, builder in builders.items():
                        model = builder()
                        model.fit(X_train, y_train)
                        scores = np.full(len(df), np.nan, dtype=float)
                        scored = gate & (val_base | oos_base)
                        scores[scored] = model.predict_proba(df.loc[scored, cols])[:, 1]
                        val_scores = scores[val_mask]
                        val_scores = val_scores[np.isfinite(val_scores)]
                        if len(val_scores) < 30:
                            continue
                        for target_tpd in target_trade_days:
                            target_count = int(math.ceil(target_tpd * split_day_counts["validation"]))
                            if target_count < 5 or target_count > len(val_scores):
                                continue
                            threshold = float(np.sort(val_scores)[-target_count])
                            row: dict[str, Any] = {
                                "candidate_id": f"f75c_{candidate_id:04d}",
                                "direction": "short",
                                "horizon": horizon,
                                "target_atr_mult": target_mult,
                                "stop_atr_mult": stop_mult,
                                "context_gate": context_name,
                                "session_gate": session_name,
                                "feature_bundle": bundle_name,
                                "feature_count": len(cols),
                                "model_family": model_name,
                                "target_trades_day": target_tpd,
                                "validation_threshold": threshold,
                                "train_rows": int(train_mask.sum()),
                                "train_positive_rate": float(y_train.mean()),
                                "validation_rows": int(val_mask.sum()),
                                "oos_rows": int(oos_mask.sum()),
                            }
                            for split, split_mask in (("validation", val_mask), ("oos", oos_mask)):
                                idx = np.where(split_mask & np.isfinite(scores) & (scores >= threshold))[0]
                                selected = base.non_overlapping_indices(idx, int(horizon))
                                metrics = base.trade_metrics(pnl[selected], exit_bars[selected], split_day_counts[split])
                                for name, value in metrics.items():
                                    row[f"{split}_{name}"] = value
                                row[f"selected_{split}_indices"] = ";".join(map(str, selected[:20]))
                            scout, meaningful, final_like = classify(row)
                            row["scout_clue"] = scout
                            row["meaningful_signal"] = meaningful
                            row["final_like_reference_only"] = final_like
                            row["joint_score"] = base.score_candidate(row)
                            results.append(row)
                            candidate_id += 1

    results.sort(key=lambda item: float(item["joint_score"]), reverse=True)
    summary = {
        "candidate_rows": len(results),
        "scout_clue_count": int(sum(int(row["scout_clue"]) for row in results)),
        "meaningful_signal_count": int(sum(int(row["meaningful_signal"]) for row in results)),
        "final_like_reference_only_count": int(sum(int(row["final_like_reference_only"]) for row in results)),
        "split_days": split_day_counts,
        "best_candidate_id": results[0]["candidate_id"] if results else "",
    }
    return results, density, summary


def write_artifacts(df: pd.DataFrame, results: list[dict[str, Any]], density: list[dict[str, Any]], summary: dict[str, Any], data_identity: dict[str, Any], created_at: str) -> tuple[str, str, str]:
    best = results[0] if results else {}
    next_run_id = (
        "frontier75D_pre_mt5_grok_volatility_compression_runtime_probe_v1"
        if summary["meaningful_signal_count"] > 0
        else "frontier75D_pre_mt5_grok_volatility_compression_negative_control_runtime_probe_v1"
    )
    status = (
        "proxy_repair_meaningful_signal_pre_mt5_required_no_authority"
        if summary["meaningful_signal_count"] > 0
        else "proxy_repair_no_meaningful_signal_negative_control_probe_required_no_authority"
    )
    result_fields = list(results[0].keys()) if results else ["candidate_id"]
    density_fields = list(density[0].keys()) if density else ["direction"]
    base.write_csv(RUN_DIR / "f75c_candidate_results.csv", results, result_fields)
    base.write_csv(RUN_DIR / "f75c_candidate_results_ranked_top50.csv", results[:50], result_fields)
    base.write_csv(RUN_DIR / "f75c_label_density_table.csv", density, density_fields)
    base.write_csv(REVIEW_DIR / "f75c_candidate_results_ranked_top50.csv", results[:50], result_fields)
    base.write_csv(REVIEW_DIR / "f75c_label_density_table.csv", density, density_fields)
    enriched = {
        **summary,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": status,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "data_identity": data_identity,
        "best_candidate": best,
        "created_at_utc": created_at,
    }
    base.write_json(RUN_DIR / "f75c_summary.json", enriched)
    base.write_json(REVIEW_DIR / "f75c_summary.json", enriched)
    base.write_json(
        REVIEW_DIR / "f75c_model_validation.json",
        {
            "model_family": "ExtraTrees, HistGradientBoosting, LogisticRegression(엑스트라트리/히스토그램 그래디언트 부스팅/로지스틱 회귀)",
            "target_and_label": "short-only prior-compression current-release first-touch label(숏 전용 직전 압축 현재 방출 선도달 라벨)",
            "split_method": "train fit, validation threshold selection, OOS read(학습 적합, 검증 임계값 선택, 표본외 판독)",
            "selection_metric": "joint_score(공동 점수)",
            "threshold_policy": "validation target trades/day search(검증 목표 일거래 수 탐색)",
            "overfit_risk": "repair after F75B and multi-candidate search(F75B 뒤 수리와 다중 후보 탐색)",
            "calibration_risk": "rank scores only(순위 점수 전용)",
            "validation_judgment": "exploratory_proxy_repair(탐색 프록시 수리)",
        },
    )
    base.write_json(
        REVIEW_DIR / "f75c_data_integrity.json",
        {
            "data_source": [base.DATASET_PATH, base.RAW_PATH],
            "time_axis": "same as F75B; prior features use shifted current-row features(F75B와 같고, 직전 피처는 shift된 현재 행 피처 사용).",
            "feature_label_boundary": "derived repair features(수리 파생 피처)는 past/current only(과거/현재 전용), future OHLC(미래 시고저종)는 label/outcome only(라벨/결과 전용).",
            "split_boundary": "time ordered train/validation/oos(시간순 학습/검증/표본외).",
            "leakage_risk": "shifted rolling features may cross session gaps(shift rolling 피처가 세션 갭을 넘을 수 있음), recorded as proxy boundary(프록시 경계로 기록).",
            "data_hash_or_identity": data_identity,
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    best_line = "No candidate rows(후보 행 없음)."
    if best:
        best_line = (
            f"Best candidate(최선 후보): `{best['candidate_id']}` validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래) "
            f"`{best['validation_net_profit']:.4f}/{best['validation_profit_factor']:.4f}/{best['validation_max_drawdown_percent']:.4f}/{best['validation_trades_day']:.4f}`, "
            f"OOS(표본외) `{best['oos_net_profit']:.4f}/{best['oos_profit_factor']:.4f}/{best['oos_max_drawdown_percent']:.4f}/{best['oos_trades_day']:.4f}`."
        )
    report = f"""# Frontier75C Label/Risk Repair Proxy Report(전선75C 라벨/위험 수리 프록시 보고서)

Run id(실행 ID): `{RUN_ID}`

Status(상태): `{status}`

Judgment(판정): `{status}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Repair Hypothesis(수리 가설)

Action(행동): F75B의 compression-in-place entry(압축 중 진입)를 prior compression + current release trigger(직전 압축 + 현재 방출 트리거) short setup(숏 설정)으로 바꿨다.

Effect(효과): F75B의 OOS PF(표본외 수익 팩터) 약화와 low density(낮은 밀도)가 진입 타이밍 문제인지 확인한다.

## Proxy KPI(프록시 KPI)

- candidates(후보): `{summary["candidate_rows"]}`
- scout clue(탐색 단서): `{summary["scout_clue_count"]}`
- meaningful signal(의미 신호): `{summary["meaningful_signal_count"]}`
- final-like reference only(최종형 참고 전용): `{summary["final_like_reference_only_count"]}`
- {best_line}

## Gap Read(간극 판독)

Meaningful signal(의미 신호)이 없으면 F75는 그래도 mandatory Runtime Probe(필수 런타임 탐침)를 위해 negative-control candidate(부정 대조 후보)를 Grok(Grok, 그록)에 먼저 검토시킨다.

## Next Action(다음 행동)

`{next_run_id}`
"""
    base.write_text(REVIEW_DIR / "frontier75C_volatility_compression_label_risk_repair_proxy_report.md", report)
    gate_audit = f"""# Required Gate Coverage Audit F75C(필수 게이트 커버리지 감사 F75C)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| data_integrity(데이터 무결성) | passed_with_boundary(경계 포함 통과) | `stages/{STAGE_ID}/03_reviews/f75c_data_integrity.json` |
| model_validation(모델 검증) | exploratory_only(탐색 전용) | `stages/{STAGE_ID}/03_reviews/f75c_model_validation.json` |
| proxy_kpi_record(프록시 KPI 기록) | passed(통과) | `stages/{STAGE_ID}/03_reviews/f75c_summary.json` |
| repair_novelty(수리 신규성) | passed(통과) | prior compression + current release trigger(직전 압축 + 현재 방출 트리거) |
| runtime_probe_rule(런타임 탐침 규칙) | next_required(다음 필수) | `{next_run_id}` |
| claim_guard(주장 보호) | passed(통과) | `{CLAIM_BOUNDARY}` |
"""
    base.write_text(REVIEW_DIR / "required_gate_coverage_audit_f75c.md", gate_audit)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "created_at_utc": created_at,
        "status": status,
        "judgment": status,
        "claim_boundary": CLAIM_BOUNDARY,
        "artifacts": {
            "summary": f"stages/{STAGE_ID}/03_reviews/f75c_summary.json",
            "report": REPORT_PATH,
            "candidate_results": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f75c_candidate_results.csv",
            "ranked_top50": f"stages/{STAGE_ID}/03_reviews/f75c_candidate_results_ranked_top50.csv",
            "label_density": f"stages/{STAGE_ID}/03_reviews/f75c_label_density_table.csv",
            "gate_audit": GATE_AUDIT_PATH,
        },
    }
    base.write_json(RUN_DIR / "run_manifest.json", manifest)
    return status, status, next_run_id


def update_state_and_ledgers(status: str, judgment: str, next_run_id: str, summary: dict[str, Any], created_at: str) -> None:
    best = summary.get("best_candidate") or {}
    workspace_state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run_id}
runtime_probe_status: pending_pre_mt5_grok_negative_control_or_candidate_probe
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f74_closeout_f75_closeout_will_trigger
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F75C label/risk repair proxy(라벨/위험 수리 프록시)를 실행했다."
  - "Effect(효과): prior compression + current release trigger(직전 압축 + 현재 방출 트리거) 수리의 후보성을 측정했다."
  - "Next(다음): {next_run_id}"
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    base.write_text(ROOT / "docs/workspace/workspace_state.yaml", workspace_state)
    best_line = "No candidate rows(후보 행 없음)."
    if best:
        best_line = (
            f"Best(최선): `{best.get('candidate_id')}` validation/OOS PF-DD-tpd(검증/표본외 수익 팩터-손실폭-일거래) "
            f"`{float(best.get('validation_profit_factor', 0.0)):.4f}/{float(best.get('validation_max_drawdown_percent', 0.0)):.4f}/{float(best.get('validation_trades_day', 0.0)):.4f}` "
            f"and `{float(best.get('oos_profit_factor', 0.0)):.4f}/{float(best.get('oos_max_drawdown_percent', 0.0)):.4f}/{float(best.get('oos_trades_day', 0.0)):.4f}`."
        )
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run_id}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(맥락 고정점): `{CONTEXT_ANCHOR_PATH}`

## Current Truth(현재 진실)

Action(행동): F75C label/risk repair proxy(라벨/위험 수리 프록시)를 실행했다.

Effect(효과): F75B의 low-density weak-PF surface(낮은 밀도/약한 수익 팩터 표면)를 entry timing repair(진입 타이밍 수리)로 다시 시험했다.

## Proxy Repair Result(프록시 수리 결과)

- candidate rows(후보 수): `{summary.get("candidate_rows")}`
- scout clue(탐색 단서): `{summary.get("scout_clue_count")}`
- meaningful signal(의미 신호): `{summary.get("meaningful_signal_count")}`
- {best_line}

## Open Work(열린 작업)

Next run(다음 실행): `{next_run_id}`

Runtime rule(런타임 규칙): F75는 stage(단계)마다 MT5 Runtime Probe(MT5 런타임 탐침)가 필요하므로, 다음에는 Grok pre-MT5 review(MT5 전 Grok 검토) 후 candidate or negative-control probe(후보 또는 부정 대조 탐침)를 물질화한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(ROOT / "docs/context/current_working_state.md", current)

    ledger_row_id = f"{RUN_ID}__proxy_repair"
    common = {
        "ledger_row_id": ledger_row_id,
        "row_id": ledger_row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "label_risk_repair_proxy(라벨 위험 수리 프록시)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "proxy_repair_kpi(프록시 수리 KPI)",
        "scoreboard_lane": "trade_shape(거래 형태)",
        "status": status,
        "judgment": judgment,
        "result_judgment": judgment,
        "path": REPORT_PATH,
        "report_path": REPORT_PATH,
        "primary_report": REPORT_PATH,
        "primary_kpi": f"candidates={summary.get('candidate_rows')};scout={summary.get('scout_clue_count')};meaningful={summary.get('meaningful_signal_count')}",
        "guardrail_kpi": "proxy_repair_only;runtime_probe_next_required",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(MT5는 다음 검증 범위)",
        "notes": "F75C repairs F75B with prior compression plus current short release trigger(F75C는 직전 압축 + 현재 숏 방출 트리거로 F75B를 수리).",
        "run_number": "frontier75C",
        "date": "2026-06-17",
        "run_date": "2026-06-17",
        "decision": judgment,
        "next_run_id": next_run_id,
        "rows": str(summary.get("candidate_rows", "")),
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_artifact": RUN_MANIFEST_PATH,
        "candidate_rows": str(summary.get("candidate_rows", "")),
        "positive_proxy_rows": str(summary.get("scout_clue_count", "")),
        "result_status": status,
        "evidence_boundary": "proxy_repair_only_no_runtime(프록시 수리 전용, 런타임 없음)",
        "work_family": "frontier_proxy_repair(전선 프록시 수리)",
        "question": "Does entry timing repair improve compression-release economics?(진입 타이밍 수리가 압축-방출 경제성을 개선하나?)",
        "next_action": next_run_id,
        "gate_audit_path": GATE_AUDIT_PATH,
        "required_gate_audit": GATE_AUDIT_PATH,
        "created_at": created_at,
        "created_at_utc": created_at,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_proxy_repair(전선 프록시 수리)",
        "run_type": "volatility_compression_release_repair(변동성 압축 방출 수리)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": RUN_MANIFEST_PATH,
        "result_path": REPORT_PATH,
        "artifact_count": "10",
    }
    if best:
        common.update(
            {
                "best_model_id": best.get("candidate_id", ""),
                "best_proxy_net": best.get("oos_net_profit", ""),
                "best_net_profit": best.get("oos_net_profit", ""),
                "best_profit_factor": best.get("oos_profit_factor", ""),
                "net_profit": best.get("oos_net_profit", ""),
                "profit_factor": best.get("oos_profit_factor", ""),
                "drawdown": best.get("oos_max_drawdown_percent", ""),
                "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
                "trade_count": best.get("oos_trade_count", ""),
                "trade_density": best.get("oos_trades_day", ""),
                "expectancy": best.get("oos_expectancy", ""),
                "recovery_factor": best.get("oos_recovery_factor", ""),
                "feature_count": best.get("feature_count", ""),
                "candidate_model_id": best.get("candidate_id", ""),
            }
        )
    run_registry = ROOT / "docs/registers/run_registry.csv"
    alpha_ledger = ROOT / "docs/registers/alpha_run_ledger.csv"
    with base.fs_path(run_registry).open("r", encoding="utf-8-sig", newline="") as handle:
        run_fields = list(csv.DictReader(handle).fieldnames or [])
    with base.fs_path(alpha_ledger).open("r", encoding="utf-8-sig", newline="") as handle:
        alpha_fields = list(csv.DictReader(handle).fieldnames or [])
    base.upsert_csv_row(run_registry, "run_id", common, run_fields)
    base.upsert_csv_row(alpha_ledger, "ledger_row_id", common, alpha_fields)
    base.upsert_csv_row(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", common, alpha_fields)
    idea_path = ROOT / "docs/registers/idea_registry.md"
    text = base.read_text(idea_path)
    marker = "<!-- frontier75C_volatility_compression_label_risk_repair_proxy_v1 -->"
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` executed F75 label/risk repair proxy(F75 라벨/위험 수리 프록시). Result(결과): `{judgment}`. Candidates(후보) `{summary.get('candidate_rows')}`, scout clue(탐색 단서) `{summary.get('scout_clue_count')}`, meaningful signal(의미 신호) `{summary.get('meaningful_signal_count')}`. Evidence(근거): `{REPORT_PATH}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run_id}`.
"""
        base.write_text(idea_path, text.rstrip() + addition)


def main() -> None:
    ensure_dirs()
    created_at = base.now_utc()
    df, feature_order, data_identity = base.load_inputs()
    df, repaired_features = add_repair_features(df, feature_order)
    data_identity = {**data_identity, "repair_feature_count": len(repaired_features), "repair_features_added": len(repaired_features) - len(feature_order)}
    results, density, summary = run_repair(df, repaired_features)
    status, judgment, next_run_id = write_artifacts(df, results, density, summary, data_identity, created_at)
    summary_payload = json.loads(base.read_text(REVIEW_DIR / "f75c_summary.json"))
    update_state_and_ledgers(status, judgment, next_run_id, summary_payload, created_at)
    print(json.dumps({
        "status": status,
        "judgment": judgment,
        "candidate_rows": summary_payload["candidate_rows"],
        "scout_clue_count": summary_payload["scout_clue_count"],
        "meaningful_signal_count": summary_payload["meaningful_signal_count"],
        "best_candidate_id": summary_payload["best_candidate_id"],
        "next_run_id": next_run_id,
        "report": REPORT_PATH,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
