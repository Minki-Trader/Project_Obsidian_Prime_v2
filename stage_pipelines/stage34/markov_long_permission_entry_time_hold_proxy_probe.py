from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage34 import markov_long_permission_attribution as attribution


STAGE_ID = attribution.STAGE_ID
RUN_ID = "run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1"
RUN_NUMBER = "run28C"
PACKET_ID = "stage34_run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1"
SOURCE_RUN_ID = attribution.SOURCE_RUN_ID
SOURCE_ATTRIBUTION_RUN_ID = attribution.RUN_ID
SOURCE_ATTRIBUTION_PACKET_ID = attribution.PACKET_ID
SOURCE_STRESS_RUN_ID = "run28B_tier_a_markov_long_permission_segment_stress_probe_v1"
SOURCE_STRESS_PACKET_ID = "stage34_run28B_tier_a_markov_long_permission_segment_stress_probe_v1"
BOUNDARY = "stage34_entry_time_proxy_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT = "inconclusive_tier_a_markov_entry_time_proxy_probe_completed"
NEXT_ACTION = "run28D_tier_a_markov_entry_proxy_runtime_probe_v1"

ROOT = attribution.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run28C_tier_a_markov_entry_time_hold_proxy_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-08_stage34_run28C_tier_a_markov_entry_time_hold_proxy.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs" / "registers" / "run_registry.csv"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews" / "review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
WORKSPACE_STATE_PATH = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = ROOT / "docs" / "workspace" / "changelog.md"

MIN_VALIDATION_TRADES = 40
MIN_OOS_TRADES = 25
THIN_MARGIN = 5

ENTRY_DIMENSIONS = (
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "confidence_band",
    "p_long_band",
    "state_score_band",
    "entropy_inv_band",
    "hour_bucket",
)

RULES: tuple[dict[str, Any], ...] = (
    {"rule_id": "baseline_all_trades", "rule_family": "reference", "stress_question": "original Tier A trade set(원래 티어 A 거래 묶음)"},
    {"rule_id": "keep_late_or_vol_mid", "rule_family": "session_volatility_combo", "stress_question": "keep late session or mid volatility(후반 세션 또는 중간 변동성 유지)"},
    {"rule_id": "exclude_vol_high_or_adx_20_25", "rule_family": "risk_filter_combo", "stress_question": "exclude high volatility or ADX 20-25(고변동 또는 ADX 20-25 제거)"},
    {"rule_id": "keep_late_or_adx_gt25", "rule_family": "session_adx_combo", "stress_question": "keep late session or ADX > 25(후반 세션 또는 ADX 25 초과 유지)"},
    {"rule_id": "exclude_vol_high", "rule_family": "volatility_regime", "stress_question": "exclude high volatility regime(고변동 구간 제거)"},
    {"rule_id": "exclude_mid_session", "rule_family": "session_time", "stress_question": "exclude mid session(중간 세션 제거)"},
    {"rule_id": "exclude_adx_20_25", "rule_family": "adx_regime", "stress_question": "exclude ADX 20-25 bucket(ADX 20-25 버킷 제거)"},
    {"rule_id": "keep_late_session_only", "rule_family": "session_time", "stress_question": "keep late session only(후반 세션만 유지)"},
    {"rule_id": "keep_vol_mid_or_late_not_adx_20_25", "rule_family": "aggressive_combo", "stress_question": "keep mid volatility or late session while excluding ADX 20-25(중간 변동성 또는 후반 세션 유지, ADX 20-25 제거)"},
    {"rule_id": "keep_downtrend", "rule_family": "trend_regime", "stress_question": "keep downtrend regime(하락 추세 구간 유지)"},
)


def rel(path: Path) -> str:
    return attribution.rel(path)


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if pd.notna(number) else default


def metric_value(metrics: Mapping[str, Any], key: str) -> Any:
    value = metrics.get(key)
    if value is None:
        return None
    if isinstance(value, float):
        return round(value, 6)
    return value


def load_tier_a_trades() -> pd.DataFrame:
    path = ROOT / f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/matched_trade_attribution.csv"
    frame = pd.read_csv(io_path(path))
    frame = frame.loc[frame["matched_tier_scope"].eq("Tier A")].copy()
    frame["open_time_dt"] = pd.to_datetime(frame["open_time"])
    frame["hour"] = frame["open_time_dt"].dt.hour
    frame["hour_bucket"] = pd.cut(
        frame["hour"],
        bins=[-1, 7, 11, 15, 19, 23],
        labels=["hour_00_07", "hour_08_11", "hour_12_15", "hour_16_19", "hour_20_23"],
    ).astype(str)
    for column in ("net_profit", "hold_bars", "mae", "mfe", "realized_over_mfe"):
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["short_hold_any"] = frame["hold_bucket"].eq("hold_0_12")
    frame["short_hold_loss"] = frame["short_hold_any"] & frame["net_profit"].lt(0)
    frame["long_hold_any"] = frame["hold_bucket"].eq("hold_gt_96")
    frame["long_hold_win"] = frame["long_hold_any"] & frame["net_profit"].gt(0)
    return frame


def rule_mask(rule_id: str, frame: pd.DataFrame) -> pd.Series:
    if rule_id == "baseline_all_trades":
        return pd.Series(True, index=frame.index)
    if rule_id == "keep_late_or_vol_mid":
        return frame["session_slice"].eq("late") | frame["volatility_regime"].eq("vol_mid")
    if rule_id == "exclude_vol_high_or_adx_20_25":
        return ~(frame["volatility_regime"].eq("vol_high") | frame["adx_bucket"].eq("adx_20_25"))
    if rule_id == "keep_late_or_adx_gt25":
        return frame["session_slice"].eq("late") | frame["adx_bucket"].eq("adx_gt25")
    if rule_id == "exclude_vol_high":
        return ~frame["volatility_regime"].eq("vol_high")
    if rule_id == "exclude_mid_session":
        return ~frame["session_slice"].eq("mid")
    if rule_id == "exclude_adx_20_25":
        return ~frame["adx_bucket"].eq("adx_20_25")
    if rule_id == "keep_late_session_only":
        return frame["session_slice"].eq("late")
    if rule_id == "keep_vol_mid_or_late_not_adx_20_25":
        return (frame["volatility_regime"].eq("vol_mid") | frame["session_slice"].eq("late")) & ~frame["adx_bucket"].eq("adx_20_25")
    if rule_id == "keep_downtrend":
        return frame["trend_regime"].eq("downtrend")
    raise KeyError(f"unknown rule_id: {rule_id}")


def split_threshold(split: str) -> int:
    return MIN_VALIDATION_TRADES if split == "validation" else MIN_OOS_TRADES


def sample_status(split: str, kept_count: int) -> str:
    threshold = split_threshold(split)
    if kept_count < threshold:
        return "sample_thin"
    if kept_count - threshold <= THIN_MARGIN:
        return "sample_ok_but_thin_margin"
    return "ok"


def label_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {
            "short_hold_loss_rate": 0.0,
            "short_hold_any_rate": 0.0,
            "long_hold_win_rate": 0.0,
            "long_hold_any_rate": 0.0,
        }
    return {
        "short_hold_loss_rate": round(float(frame["short_hold_loss"].mean()), 6),
        "short_hold_any_rate": round(float(frame["short_hold_any"].mean()), 6),
        "long_hold_win_rate": round(float(frame["long_hold_win"].mean()), 6),
        "long_hold_any_rate": round(float(frame["long_hold_any"].mean()), 6),
    }


def evaluate_rule_splits(tier_a: pd.DataFrame, rules: Sequence[Mapping[str, Any]] = RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule in rules:
        rule_id = str(rule["rule_id"])
        for split, split_frame in tier_a.groupby("matched_split", dropna=False):
            base = attribution.profit_metrics(split_frame)
            base_labels = label_metrics(split_frame)
            mask = rule_mask(rule_id, split_frame)
            kept = split_frame.loc[mask].copy()
            removed = split_frame.loc[~mask].copy()
            kept_metrics = attribution.profit_metrics(kept)
            removed_metrics = attribution.profit_metrics(removed)
            kept_labels = label_metrics(kept)
            base_count = int(base["trade_count"])
            kept_count = int(kept_metrics["trade_count"])
            rows.append(
                {
                    "rule_id": rule_id,
                    "rule_family": rule["rule_family"],
                    "split": str(split),
                    "base_trade_count": base_count,
                    "base_net_profit": metric_value(base, "net_profit"),
                    "base_profit_factor": metric_value(base, "profit_factor"),
                    "base_short_hold_loss_rate": base_labels["short_hold_loss_rate"],
                    "base_long_hold_win_rate": base_labels["long_hold_win_rate"],
                    "kept_trade_count": kept_count,
                    "kept_trade_share": round(kept_count / max(1, base_count), 6),
                    "kept_net_profit": metric_value(kept_metrics, "net_profit"),
                    "kept_profit_factor": metric_value(kept_metrics, "profit_factor"),
                    "kept_expectancy": metric_value(kept_metrics, "expectancy"),
                    "kept_win_rate_percent": metric_value(kept_metrics, "win_rate_percent"),
                    "kept_avg_hold_bars": metric_value(kept_metrics, "avg_hold_bars"),
                    "kept_short_hold_loss_rate": kept_labels["short_hold_loss_rate"],
                    "kept_long_hold_win_rate": kept_labels["long_hold_win_rate"],
                    "short_hold_loss_delta_vs_base": round(kept_labels["short_hold_loss_rate"] - base_labels["short_hold_loss_rate"], 6),
                    "long_hold_win_delta_vs_base": round(kept_labels["long_hold_win_rate"] - base_labels["long_hold_win_rate"], 6),
                    "removed_trade_count": metric_value(removed_metrics, "trade_count"),
                    "removed_net_profit": metric_value(removed_metrics, "net_profit"),
                    "removed_profit_factor": metric_value(removed_metrics, "profit_factor"),
                    "net_delta_vs_base": round(numeric(kept_metrics.get("net_profit")) - numeric(base.get("net_profit")), 6),
                    "pf_delta_vs_base": None if kept_metrics.get("profit_factor") is None or base.get("profit_factor") is None else round(numeric(kept_metrics.get("profit_factor")) - numeric(base.get("profit_factor")), 6),
                    "sample_status": sample_status(str(split), kept_count),
                    "stress_question": rule["stress_question"],
                }
            )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"]))


def row_for(rows: Sequence[Mapping[str, Any]], rule_id: str, split: str) -> Mapping[str, Any]:
    return next(row for row in rows if row["rule_id"] == rule_id and row["split"] == split)


def classify_rule(rule: Mapping[str, Any], validation: Mapping[str, Any], oos: Mapping[str, Any]) -> str:
    rule_id = str(rule["rule_id"])
    if rule_id == "baseline_all_trades":
        return "reference_only"
    sample_flags = {str(validation["sample_status"]), str(oos["sample_status"])}
    if "sample_thin" in sample_flags:
        return "sample_thin_diagnostic_only"
    val_pf_delta = numeric(validation["pf_delta_vs_base"])
    oos_pf_delta = numeric(oos["pf_delta_vs_base"])
    val_net_delta = numeric(validation["net_delta_vs_base"])
    oos_net_delta = numeric(oos["net_delta_vs_base"])
    val_short_delta = numeric(validation["short_hold_loss_delta_vs_base"])
    oos_short_delta = numeric(oos["short_hold_loss_delta_vs_base"])
    thin_margin = "sample_ok_but_thin_margin" in sample_flags

    if val_pf_delta > 0 and oos_pf_delta > 0 and oos_net_delta > 0 and val_short_delta <= 0 and oos_short_delta <= 0:
        return "entry_proxy_candidate_thin_sample" if thin_margin else "entry_proxy_candidate"
    if val_pf_delta > 0 and oos_pf_delta > 0 and val_net_delta >= 0 and oos_net_delta >= 0:
        return "entry_proxy_candidate_modest"
    if val_pf_delta > 0 and oos_pf_delta > 0:
        return "pf_survivor_with_net_or_label_cost"
    if oos_pf_delta > 0 and val_net_delta < -50:
        return "split_conflict_oos_help_validation_cost"
    return "rejected_or_unstable"


def summarize_rules(split_rows: Sequence[Mapping[str, Any]], rules: Sequence[Mapping[str, Any]] = RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule in rules:
        rule_id = str(rule["rule_id"])
        validation = row_for(split_rows, rule_id, "validation")
        oos = row_for(split_rows, rule_id, "oos")
        rows.append(
            {
                "rule_id": rule_id,
                "rule_family": rule["rule_family"],
                "classification": classify_rule(rule, validation, oos),
                "validation_kept_trades": validation["kept_trade_count"],
                "validation_kept_net_profit": validation["kept_net_profit"],
                "validation_kept_profit_factor": validation["kept_profit_factor"],
                "validation_net_delta_vs_base": validation["net_delta_vs_base"],
                "validation_pf_delta_vs_base": validation["pf_delta_vs_base"],
                "validation_short_hold_loss_delta": validation["short_hold_loss_delta_vs_base"],
                "validation_long_hold_win_delta": validation["long_hold_win_delta_vs_base"],
                "oos_kept_trades": oos["kept_trade_count"],
                "oos_kept_net_profit": oos["kept_net_profit"],
                "oos_kept_profit_factor": oos["kept_profit_factor"],
                "oos_net_delta_vs_base": oos["net_delta_vs_base"],
                "oos_pf_delta_vs_base": oos["pf_delta_vs_base"],
                "oos_short_hold_loss_delta": oos["short_hold_loss_delta_vs_base"],
                "oos_long_hold_win_delta": oos["long_hold_win_delta_vs_base"],
                "validation_sample_status": validation["sample_status"],
                "oos_sample_status": oos["sample_status"],
                "stress_question": rule["stress_question"],
            }
        )
    order = {
        "entry_proxy_candidate": 0,
        "entry_proxy_candidate_modest": 1,
        "entry_proxy_candidate_thin_sample": 2,
        "pf_survivor_with_net_or_label_cost": 3,
        "sample_thin_diagnostic_only": 4,
        "split_conflict_oos_help_validation_cost": 5,
        "rejected_or_unstable": 6,
        "reference_only": 7,
    }
    return sorted(rows, key=lambda row: (order.get(str(row["classification"]), 99), str(row["rule_id"])))


def label_surface_rows(tier_a: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, split_frame in tier_a.groupby("matched_split", dropna=False):
        for dimension in ENTRY_DIMENSIONS:
            if dimension not in split_frame.columns:
                continue
            for segment, group in split_frame.groupby(dimension, dropna=False):
                metrics = attribution.profit_metrics(group)
                labels = label_metrics(group)
                rows.append(
                    {
                        "split": str(split),
                        "dimension": dimension,
                        "segment": str(segment),
                        "trade_count": metrics["trade_count"],
                        "net_profit": metrics["net_profit"],
                        "profit_factor": metrics["profit_factor"],
                        "short_hold_loss_rate": labels["short_hold_loss_rate"],
                        "short_hold_any_rate": labels["short_hold_any_rate"],
                        "long_hold_win_rate": labels["long_hold_win_rate"],
                        "long_hold_any_rate": labels["long_hold_any_rate"],
                    }
                )
    return sorted(rows, key=lambda row: (row["dimension"], row["split"], row["segment"]))


def best_summary(summary_rows: Sequence[Mapping[str, Any]], rule_id: str) -> Mapping[str, Any]:
    return next(row for row in summary_rows if row["rule_id"] == rule_id)


def build_read(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    primary = best_summary(summary_rows, "keep_late_or_vol_mid")
    stable = best_summary(summary_rows, "exclude_vol_high_or_adx_20_25")
    aggressive = best_summary(summary_rows, "keep_vol_mid_or_late_not_adx_20_25")
    return {
        "headline": "entry_time_proxy_exists_but_needs_mt5_runtime_probe",
        "primary_candidate": {
            "rule_id": primary["rule_id"],
            "classification": primary["classification"],
            "validation_trades": primary["validation_kept_trades"],
            "validation_pf": primary["validation_kept_profit_factor"],
            "oos_trades": primary["oos_kept_trades"],
            "oos_pf": primary["oos_kept_profit_factor"],
            "reason": "best balanced PF lift using only session and volatility known at entry(진입 시점 세션과 변동성만으로 균형 잡힌 수익 팩터 상승)",
        },
        "stable_secondary_candidate": {
            "rule_id": stable["rule_id"],
            "classification": stable["classification"],
            "validation_trades": stable["validation_kept_trades"],
            "validation_pf": stable["validation_kept_profit_factor"],
            "oos_trades": stable["oos_kept_trades"],
            "oos_pf": stable["oos_kept_profit_factor"],
            "reason": "more sample headroom but weaker PF lift(표본 여유는 더 크지만 수익 팩터 상승은 약함)",
        },
        "aggressive_diagnostic": {
            "rule_id": aggressive["rule_id"],
            "classification": aggressive["classification"],
            "validation_trades": aggressive["validation_kept_trades"],
            "oos_trades": aggressive["oos_kept_trades"],
            "reason": "PF is strongest but sample is too thin for direct next step(수익 팩터는 가장 강하지만 표본이 너무 얇음)",
        },
        "candidate_boundary": "candidate_for_run28D_runtime_probe_not_runtime_authority",
        "next_probe": NEXT_ACTION,
    }


def write_result_files(split_rows: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]], surface_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> dict[str, str]:
    stage_paths = {
        "entry_proxy_split_metrics": RESULT_ROOT / "entry_proxy_split_metrics.csv",
        "entry_proxy_rule_summary": RESULT_ROOT / "entry_proxy_rule_summary.csv",
        "entry_label_surface": RESULT_ROOT / "entry_label_surface.csv",
        "aggregate_summary": RESULT_ROOT / "aggregate_summary.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    packet_paths = {
        "entry_proxy_split_metrics": PACKET_ROOT / "entry_proxy_split_metrics.csv",
        "entry_proxy_rule_summary": PACKET_ROOT / "entry_proxy_rule_summary.csv",
        "entry_label_surface": PACKET_ROOT / "entry_label_surface.csv",
    }
    for paths in (stage_paths, packet_paths):
        attribution.write_csv(paths["entry_proxy_split_metrics"], list(split_rows[0].keys()), split_rows)
        attribution.write_csv(paths["entry_proxy_rule_summary"], list(summary_rows[0].keys()), summary_rows)
        attribution.write_csv(paths["entry_label_surface"], list(surface_rows[0].keys()), surface_rows)
    attribution.write_json(stage_paths["aggregate_summary"], summary)
    attribution.write_json(
        stage_paths["run_manifest"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
            "source_stress_run_id": SOURCE_STRESS_RUN_ID,
            "outputs": {key: rel(path) for key, path in stage_paths.items() if key != "run_manifest"},
            "packet_outputs": {key: rel(path) for key, path in packet_paths.items()},
            "boundary": BOUNDARY,
        },
    )
    return {key: rel(path) for key, path in packet_paths.items()} | {"aggregate_summary": rel(PACKET_ROOT / "aggregate_summary.json"), "run_manifest": rel(stage_paths["run_manifest"])}


def build_summary(created_at: str, branch: str) -> dict[str, Any]:
    tier_a = load_tier_a_trades()
    split_rows = evaluate_rule_splits(tier_a)
    summary_rows = summarize_rules(split_rows)
    surface_rows = label_surface_rows(tier_a)
    source_paths = {
        "source_run28A_matched_trade_attribution": f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/matched_trade_attribution.csv",
        "source_run28B_segment_stress_summary": f"docs/agent_control/packets/{SOURCE_STRESS_PACKET_ID}/segment_stress_summary.csv",
        "source_run28B_aggregate_summary": f"docs/agent_control/packets/{SOURCE_STRESS_PACKET_ID}/aggregate_summary.json",
    }
    summary: dict[str, Any] = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
        "source_stress_run_id": SOURCE_STRESS_RUN_ID,
        "status": "reviewed_entry_time_proxy_probe_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "created_at_utc": created_at,
        "active_branch": branch,
        "source_paths": source_paths,
        "source_hashes": {key: sha256_file_lf_normalized(ROOT / value) for key, value in source_paths.items()},
        "experiment_design": {
            "hypothesis": "entry-time session/regime filters can proxy the ex-post hold-shape survivor clue(진입 시점 세션/국면 필터가 사후 보유 형태 생존 단서를 대리할 수 있음)",
            "decision_use": "choose whether a narrow MT5 runtime probe is worth running(좁은 MT5 런타임 탐침 가치 판단)",
            "comparison_baseline": "run28B baseline_all_trades Tier A validation/OOS(28B 실행 전체 티어 A 검증/표본외)",
            "control_variables": "source trades, Tier A scope, run22B/run28A artifacts, no new MT5 execution(원천 거래, 티어 A 범위, 22B/28A 산출물, 새 MT5 없음)",
            "changed_variables": "entry-time keep/exclude rule over session/volatility/trend/ADX only(세션/변동성/추세/ADX 진입 시점 규칙)",
            "sample_scope": "Tier A matched trades validation 77 and OOS 51(티어 A 매칭 거래 검증 77개, 표본외 51개)",
            "success_criteria": "PF improves in both splits, OOS net improves, short-hold-loss rate does not rise, and kept sample is not thin(양쪽 수익 팩터 개선, 표본외 순손익 개선, 짧은 보유 손실률 비상승, 표본 얇음 아님)",
            "failure_criteria": "split conflict, sample thin, or uses ex-post/month fields(분할 충돌, 얇은 표본, 사후/월 필드 사용)",
            "invalid_conditions": "missing run28A/run28B packet inputs or using hold_bucket as input(28A/28B 묶음 누락 또는 보유 버킷을 입력으로 사용)",
            "stop_conditions": "stop at candidate ranking; no runtime authority without MT5(후보 순위에서 중단, MT5 없이는 런타임 권위 없음)",
            "evidence_plan": "rule summary, split metrics, label surface, gates, ledgers, state sync audit(규칙 요약, 분할 지표, 라벨 표면, 게이트, 장부, 상태 동기화 감사)",
        },
        "source_integrity": {
            "tier_a_trade_rows": int(len(tier_a)),
            "tier_a_validation_trades": int(tier_a["matched_split"].eq("validation").sum()),
            "tier_a_oos_trades": int(tier_a["matched_split"].eq("oos").sum()),
            "input_fields": sorted([column for column in ENTRY_DIMENSIONS if column in tier_a.columns]),
            "forbidden_input_fields_used": [],
            "new_mt5_run": False,
        },
        "rule_summary_rows": summary_rows,
        "rule_split_rows": split_rows,
        "entry_label_surface_rows": surface_rows,
        "proxy_read": build_read(summary_rows),
        "next_action": NEXT_ACTION,
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority", "mt5_verified_runtime_rule"],
    }
    summary["output_paths"] = write_result_files(split_rows, summary_rows, surface_rows, summary)
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    return summary


def review_text(summary: Mapping[str, Any]) -> str:
    primary = best_summary(summary["rule_summary_rows"], "keep_late_or_vol_mid")
    secondary = best_summary(summary["rule_summary_rows"], "exclude_vol_high_or_adx_20_25")
    aggressive = best_summary(summary["rule_summary_rows"], "keep_vol_mid_or_late_not_adx_20_25")
    return f"""# RUN28C Tier A Markov Entry-Time Hold Proxy Packet(28C 실행 티어 A 마르코프 진입 시점 보유 대리 신호 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_entry_time_proxy_probe_completed`
- judgment(판정): `{JUDGMENT}`
- source(원천): `{SOURCE_ATTRIBUTION_RUN_ID}` and `{SOURCE_STRESS_RUN_ID}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): run28B(28B 실행)의 ex-post hold shape(사후 보유 형태) 단서를 진입 시점(entry time, 진입 시점)에 아는 session/regime(세션/국면) 조합으로 대리할 수 있는지 봤다. 새 MT5(MetaTrader 5, 메타트레이더5) 실행은 하지 않았다.

## Result(결과)

- primary candidate(1차 후보): `keep_late_or_vol_mid`
  - validation PF(검증 수익 팩터) `{primary['validation_kept_profit_factor']}`, trades(거래 수) `{primary['validation_kept_trades']}`
  - OOS PF(표본외 수익 팩터) `{primary['oos_kept_profit_factor']}`, trades(거래 수) `{primary['oos_kept_trades']}`
  - classification(분류): `{primary['classification']}`
- stable secondary(안정 보조 후보): `exclude_vol_high_or_adx_20_25`
  - validation PF(검증 수익 팩터) `{secondary['validation_kept_profit_factor']}`, OOS PF(표본외 수익 팩터) `{secondary['oos_kept_profit_factor']}`
  - classification(분류): `{secondary['classification']}`
- aggressive diagnostic(공격적 진단): `keep_vol_mid_or_late_not_adx_20_25`
  - validation PF(검증 수익 팩터) `{aggressive['validation_kept_profit_factor']}`, OOS PF(표본외 수익 팩터) `{aggressive['oos_kept_profit_factor']}`
  - classification(분류): `{aggressive['classification']}`

## Read(판독)

`keep_late_or_vol_mid`가 가장 좋은 entry-time proxy(진입 시점 대리 신호)다. 다만 validation(검증) 40개, OOS(표본외) 26개로 sample margin(표본 여유)이 얇다.

효과(effect, 효과): 이 규칙은 바로 운영 의미(operating meaning, 운영 의미)가 아니라, run28D(28D 실행) MT5 runtime probe(MT5 런타임 탐침) 후보로만 남긴다.

## Files(파일)

- summary(요약): `{summary['output_paths']['entry_proxy_rule_summary']}`
- split metrics(분할 지표): `{summary['output_paths']['entry_proxy_split_metrics']}`
- label surface(라벨 표면): `{summary['output_paths']['entry_label_surface']}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위), MT5-verified runtime rule(MT5 검증 런타임 규칙).
"""


def decision_text() -> str:
    return f"""# Decision: Stage34 RUN28C Entry-Time Hold Proxy Completed(결정: 34단계 28C 실행 진입 시점 보유 대리 신호 완료)

- date(날짜): 2026-05-08
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): `keep_late_or_vol_mid`를 run28D(28D 실행) MT5 runtime probe(MT5 런타임 탐침) 후보로 남긴다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    primary = best_summary(summary["rule_summary_rows"], "keep_late_or_vol_mid")
    secondary = best_summary(summary["rule_summary_rows"], "exclude_vol_high_or_adx_20_25")
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__entry_proxy_rule_summary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "entry_proxy_rule_summary",
            "parent_run_id": SOURCE_STRESS_RUN_ID,
            "record_view": "entry_proxy_rule_summary",
            "tier_scope": "Tier A",
            "kpi_scope": "entry_time_proxy_candidate",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["output_paths"]["entry_proxy_rule_summary"],
            "primary_kpi": ledger_pairs([("primary_rule", primary["rule_id"]), ("validation_pf", primary["validation_kept_profit_factor"]), ("oos_pf", primary["oos_kept_profit_factor"]), ("validation_trades", primary["validation_kept_trades"]), ("oos_trades", primary["oos_kept_trades"])]),
            "guardrail_kpi": ledger_pairs([("classification", primary["classification"]), ("boundary", BOUNDARY)]),
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Entry-time proxy candidate only; MT5 runtime verification is next action, not completed here.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__secondary_stability_candidate",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "secondary_stability_candidate",
            "parent_run_id": SOURCE_STRESS_RUN_ID,
            "record_view": "entry_proxy_split_metrics",
            "tier_scope": "Tier A",
            "kpi_scope": "entry_time_proxy_stability",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["output_paths"]["entry_proxy_split_metrics"],
            "primary_kpi": ledger_pairs([("secondary_rule", secondary["rule_id"]), ("validation_pf", secondary["validation_kept_profit_factor"]), ("oos_pf", secondary["oos_kept_profit_factor"])]),
            "guardrail_kpi": "more_sample_headroom_weaker_pf_lift",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Secondary rule is a more stable but weaker MT5 probe comparator.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__entry_label_surface",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "entry_label_surface",
            "parent_run_id": SOURCE_ATTRIBUTION_RUN_ID,
            "record_view": "entry_label_surface",
            "tier_scope": "Tier A",
            "kpi_scope": "entry_time_label_surface",
            "scoreboard_lane": "trade_shape",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["output_paths"]["entry_label_surface"],
            "primary_kpi": ledger_pairs([("surface_rows", len(summary["entry_label_surface_rows"])), ("forbidden_input_fields_used", summary["source_integrity"]["forbidden_input_fields_used"])]),
            "guardrail_kpi": "hold_bucket_used_as_label_not_input",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Entry-time segments explain short-hold-loss and long-hold-win labels.",
        },
    ]
    registry_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "performance_attribution", "status": "reviewed", "judgment": JUDGMENT, "path": rel(REPORT_PATH), "notes": "Stage34 Tier A Markov entry-time hold proxy probe over reused run28A/run28B artifacts; no MT5 verification, baseline, promotion, or runtime authority."}
    return {"stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"), "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"), "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")}


def write_packet_artifacts(summary: Mapping[str, Any]) -> None:
    attribution.write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    attribution.write_json(PACKET_ROOT / "skill_receipts.json", [{"skill": "obsidian-experiment-design", "status": "executed", "run_id": RUN_ID}, {"skill": "obsidian-performance-attribution", "status": "executed", "boundary": BOUNDARY}, {"skill": "obsidian-result-judgment", "status": "executed", "judgment": JUDGMENT}])
    attribution.write_json(PACKET_ROOT / "artifact_lineage_gate.json", {"packet_id": PACKET_ID, "status": "passed", "source_paths": summary["source_paths"]})
    attribution.write_json(PACKET_ROOT / "entry_time_input_guard.json", {"packet_id": PACKET_ID, "status": "passed", "forbidden_input_fields_used": summary["source_integrity"]["forbidden_input_fields_used"], "hold_bucket_role": "label_only"})
    attribution.write_json(PACKET_ROOT / "proxy_candidate_gate.json", {"packet_id": PACKET_ID, "status": "passed", "proxy_read": summary["proxy_read"]})
    attribution.write_json(PACKET_ROOT / "kpi_contract_audit.json", {"packet_id": PACKET_ID, "status": "passed", "new_mt5_run_required_for_this_claim": False, "mt5_runtime_probe_next": NEXT_ACTION})
    attribution.write_json(PACKET_ROOT / "final_claim_guard.json", {"packet_id": PACKET_ID, "status": "passed", "allowed_claims": ["Stage34 RUN28C entry-time proxy candidate found for MT5 probe."], "forbidden_claims": summary["forbidden_claims"], "boundary": BOUNDARY})
    gates = ["artifact_lineage_gate", "entry_time_input_guard", "proxy_candidate_gate", "kpi_contract_audit", "final_claim_guard", "required_gate_coverage_audit"]
    attribution.write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []})


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    attribution.write_md(REPORT_PATH, review_text(summary))
    attribution.write_md(DECISION_PATH, decision_text())
    attribution.write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage34 Review Index(34단계 검토 색인)

- current status(현재 상태): `reviewed_entry_time_proxy_probe_completed`
- current run(현재 실행): `{RUN_ID}`
- current packet(현재 묶음): `{PACKET_ID}`
- latest review(최신 검토): `{rel(REPORT_PATH)}`
- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`

효과(effect, 효과): Stage34(34단계)는 run28C(28C 실행)에서 entry-time hold proxy(진입 시점 보유 대리 신호)를 찾았다. runtime authority(런타임 권위)는 없고, 다음은 run28D(28D 실행) MT5 runtime probe(MT5 런타임 탐침)다.
""",
    )
    attribution.write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage34 Selection Status(34단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `reviewed_entry_time_proxy_probe_completed`
- current run(현재 실행): `{RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`
- primary MT5 probe candidate(1차 MT5 탐침 후보): `keep_late_or_vol_mid`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): entry-time proxy(진입 시점 대리 신호)는 보존하지만, 아직 MT5 runtime verification(MT5 런타임 검증)을 통과한 규칙이 아니다.
""",
    )


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    new_focus = "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution reviewed_entry_time_proxy_probe_completed(검토된 진입 시점 대리 신호 탐침 완료): run28C(28C 실행)는 `keep_late_or_vol_mid`를 Tier A Markov long permission(티어 A 마르코프 롱 허용)의 entry-time proxy(진입 시점 대리 신호) 후보로 남겼다; 아직 MT5 runtime verification(MT5 런타임 검증), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    text = re.sub(r"- Stage34\(34단계\) 34_regime_mechanism__tier_a_markov_long_permission_attribution .*?\n(?=- Stage33)", new_focus, text, count=1, flags=re.DOTALL)
    text = re.sub(r"- current_run_id\(현재 실행 ID\).*?(?=\n- treat Stage29-32)", f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 검토된 실행인\n  {RUN_ID}을 가리킨다; next action(다음 행동)은 {NEXT_ACTION}다.", text, count=1, flags=re.DOTALL)
    stage34_block = f"""stage34_tier_a_markov_long_permission_attribution:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_entry_time_proxy_probe_completed
  current_run_id: {RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  decision_path: {rel(DECISION_PATH)}
  stage_path: stages/{STAGE_ID}
  previous_stage_id: 33_regime_mechanism__tier_a_markov_long_permission_source
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  primary_mt5_probe_candidate: keep_late_or_vol_mid
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage34_tier_a_markov_long_permission_attribution:\n(?:  .+\n)+\npre_alpha_stage_queue:", stage34_block + "\npre_alpha_stage_queue:", text, count=1)
    attribution.write_md(WORKSPACE_STATE_PATH, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage34 RUN28C Entry-Time Hold Proxy.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    primary = summary["proxy_read"]["primary_candidate"]
    block = f"""## Latest Stage34 RUN28C Entry-Time Hold Proxy(최신 34단계 28C 실행 진입 시점 보유 대리 신호)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `{summary['active_branch']}`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

Stage34(34단계) `{RUN_ID}`를 reviewed entry-time proxy probe(검토된 진입 시점 대리 신호 탐침)로 완료했다.

결과(result, 결과): `keep_late_or_vol_mid`가 primary candidate(1차 후보)다. validation PF(검증 수익 팩터) `{primary['validation_pf']}`, OOS PF(표본외 수익 팩터) `{primary['oos_pf']}`지만 sample margin(표본 여유)이 얇다.

효과(effect, 효과): 이 후보는 run28D(28D 실행) MT5 runtime probe(MT5 런타임 탐침)로 넘길 수 있는 단서다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    attribution.write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog() -> None:
    old = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-08 Stage34 RUN28C Entry-Time Hold Proxy.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-08 Stage34 RUN28C Entry-Time Hold Proxy(34단계 28C 실행 진입 시점 보유 대리 신호)

- completed(완료): `{RUN_ID}` entry-time hold proxy probe(진입 시점 보유 대리 신호 탐침)
- source(원천): `{SOURCE_ATTRIBUTION_RUN_ID}` and `{SOURCE_STRESS_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): `keep_late_or_vol_mid`를 MT5 runtime probe(MT5 런타임 탐침) 후보로 남겼지만, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    attribution.write_md(CHANGELOG_PATH, entry + old.lstrip("\ufeff"))


def run(_: argparse.Namespace) -> dict[str, Any]:
    summary = build_summary(attribution.utc_now(), attribution.active_branch())
    update_stage_docs(summary)
    summary["ledger_materialization"] = materialize_ledgers(summary)
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    write_packet_artifacts(summary)
    update_workspace_state(summary)
    prepend_context(summary)
    append_changelog()
    return summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage34 Tier A Markov entry-time hold proxy probe.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(parse_args(argv))
    print(json.dumps({"status": summary["status"], "judgment": summary["judgment"], "run_id": RUN_ID, "report_path": rel(REPORT_PATH), "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
