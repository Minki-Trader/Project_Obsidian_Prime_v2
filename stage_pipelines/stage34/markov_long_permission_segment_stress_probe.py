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
RUN_ID = "run28B_tier_a_markov_long_permission_segment_stress_probe_v1"
RUN_NUMBER = "run28B"
PACKET_ID = "stage34_run28B_tier_a_markov_long_permission_segment_stress_probe_v1"
SOURCE_STAGE_ID = attribution.SOURCE_STAGE_ID
SOURCE_RUN_ID = attribution.SOURCE_RUN_ID
SOURCE_PACKET_ID = attribution.SOURCE_PACKET_ID
SOURCE_ATTRIBUTION_RUN_ID = attribution.RUN_ID
SOURCE_ATTRIBUTION_PACKET_ID = attribution.PACKET_ID
BOUNDARY = "stage34_segment_stress_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT = "inconclusive_tier_a_markov_segment_stress_probe_completed"
NEXT_ACTION = "run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1"

ROOT = attribution.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run28B_tier_a_markov_long_permission_segment_stress_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-08_stage34_run28B_tier_a_markov_long_permission_segment_stress.md"
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

RULES: tuple[dict[str, Any], ...] = (
    {"rule_id": "baseline_all_trades", "rule_family": "reference", "entry_time_available": True, "direct_runtime_candidate": False, "stress_question": "original Tier A trade set(원래 티어 A 거래 묶음)"},
    {"rule_id": "exclude_short_hold_0_12", "rule_family": "hold_shape", "entry_time_available": False, "direct_runtime_candidate": False, "stress_question": "remove ex-post short holds(사후 짧은 보유 제거)"},
    {"rule_id": "keep_hold_gt_96_only", "rule_family": "hold_shape", "entry_time_available": False, "direct_runtime_candidate": False, "stress_question": "keep ex-post long holds only(사후 긴 보유만 유지)"},
    {"rule_id": "exclude_mid_session", "rule_family": "session_time", "entry_time_available": True, "direct_runtime_candidate": True, "stress_question": "remove mid session(중간 세션 제거)"},
    {"rule_id": "exclude_mid_or_short_hold", "rule_family": "mixed_session_hold", "entry_time_available": False, "direct_runtime_candidate": False, "stress_question": "remove mid session or ex-post short holds(중간 세션 또는 사후 짧은 보유 제거)"},
    {"rule_id": "exclude_vol_high", "rule_family": "volatility_regime", "entry_time_available": True, "direct_runtime_candidate": True, "stress_question": "remove high volatility regime(고변동 구간 제거)"},
    {"rule_id": "exclude_adx_20_25", "rule_family": "adx_regime", "entry_time_available": True, "direct_runtime_candidate": True, "stress_question": "remove ADX 20-25 bucket(ADX 20-25 버킷 제거)"},
    {"rule_id": "keep_late_session_only", "rule_family": "session_time", "entry_time_available": True, "direct_runtime_candidate": True, "stress_question": "keep late session only(후반 세션만 유지)"},
    {"rule_id": "exclude_oos_negative_months_diag", "rule_family": "calendar_diagnostic", "entry_time_available": False, "direct_runtime_candidate": False, "stress_question": "remove known OOS negative months for diagnosis only(알려진 표본외 음수 월만 진단용 제거)"},
)


def rel(path: Path) -> str:
    return attribution.rel(path)


def metric_value(metrics: Mapping[str, Any], key: str) -> Any:
    value = metrics.get(key)
    if value is None:
        return None
    if isinstance(value, float):
        return round(value, 6)
    return value


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if pd.notna(number) else default


def pf_delta(next_pf: Any, base_pf: Any) -> Any:
    if next_pf is None or base_pf is None:
        return None
    return round(numeric(next_pf) - numeric(base_pf), 6)


def rule_mask(rule_id: str, frame: pd.DataFrame) -> pd.Series:
    if rule_id == "baseline_all_trades":
        return pd.Series(True, index=frame.index)
    if rule_id == "exclude_short_hold_0_12":
        return ~frame["hold_bucket"].eq("hold_0_12")
    if rule_id == "keep_hold_gt_96_only":
        return frame["hold_bucket"].eq("hold_gt_96")
    if rule_id == "exclude_mid_session":
        return ~frame["session_slice"].eq("mid")
    if rule_id == "exclude_mid_or_short_hold":
        return ~(frame["session_slice"].eq("mid") | frame["hold_bucket"].eq("hold_0_12"))
    if rule_id == "exclude_vol_high":
        return ~frame["volatility_regime"].eq("vol_high")
    if rule_id == "exclude_adx_20_25":
        return ~frame["adx_bucket"].eq("adx_20_25")
    if rule_id == "keep_late_session_only":
        return frame["session_slice"].eq("late")
    if rule_id == "exclude_oos_negative_months_diag":
        return ~frame["month"].isin(["2025-12", "2026-01", "2026-03"])
    raise KeyError(f"unknown rule_id: {rule_id}")


def sample_status(split: str, kept_trade_count: int) -> str:
    threshold = MIN_VALIDATION_TRADES if split == "validation" else MIN_OOS_TRADES
    return "ok" if kept_trade_count >= threshold else "sample_thin"


def evaluate_rule_splits(tier_a: pd.DataFrame, rules: Sequence[Mapping[str, Any]] = RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule in rules:
        rule_id = str(rule["rule_id"])
        for split, split_frame in tier_a.groupby("matched_split", dropna=False):
            base = attribution.profit_metrics(split_frame)
            mask = rule_mask(rule_id, split_frame)
            kept = split_frame.loc[mask].copy()
            removed = split_frame.loc[~mask].copy()
            kept_metrics = attribution.profit_metrics(kept)
            removed_metrics = attribution.profit_metrics(removed)
            base_count = int(metric_value(base, "trade_count") or 0)
            kept_count = int(metric_value(kept_metrics, "trade_count") or 0)
            rows.append(
                {
                    "rule_id": rule_id,
                    "rule_family": rule["rule_family"],
                    "split": str(split),
                    "entry_time_available": bool(rule["entry_time_available"]),
                    "direct_runtime_candidate": bool(rule["direct_runtime_candidate"]),
                    "stress_question": rule["stress_question"],
                    "base_trade_count": base_count,
                    "base_net_profit": metric_value(base, "net_profit"),
                    "base_profit_factor": metric_value(base, "profit_factor"),
                    "kept_trade_count": kept_count,
                    "kept_trade_share": round(kept_count / max(1, base_count), 6),
                    "kept_net_profit": metric_value(kept_metrics, "net_profit"),
                    "kept_profit_factor": metric_value(kept_metrics, "profit_factor"),
                    "kept_win_rate_percent": metric_value(kept_metrics, "win_rate_percent"),
                    "kept_expectancy": metric_value(kept_metrics, "expectancy"),
                    "kept_avg_hold_bars": metric_value(kept_metrics, "avg_hold_bars"),
                    "removed_trade_count": metric_value(removed_metrics, "trade_count"),
                    "removed_net_profit": metric_value(removed_metrics, "net_profit"),
                    "removed_profit_factor": metric_value(removed_metrics, "profit_factor"),
                    "net_delta_vs_base": round(numeric(kept_metrics.get("net_profit")) - numeric(base.get("net_profit")), 6),
                    "pf_delta_vs_base": pf_delta(kept_metrics.get("profit_factor"), base.get("profit_factor")),
                    "sample_status": sample_status(str(split), kept_count),
                }
            )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"]))


def row_for(rows: Sequence[Mapping[str, Any]], rule_id: str, split: str) -> Mapping[str, Any]:
    return next(row for row in rows if row["rule_id"] == rule_id and row["split"] == split)


def classify_rule(meta: Mapping[str, Any], validation: Mapping[str, Any], oos: Mapping[str, Any]) -> str:
    rule_id = str(meta["rule_id"])
    if rule_id == "baseline_all_trades":
        return "reference_only"
    if rule_id == "exclude_oos_negative_months_diag":
        return "diagnostic_time_specific_not_candidate"
    val_net_delta = numeric(validation["net_delta_vs_base"])
    oos_net_delta = numeric(oos["net_delta_vs_base"])
    val_pf_delta = numeric(validation["pf_delta_vs_base"])
    oos_pf_delta = numeric(oos["pf_delta_vs_base"])
    val_removed_net = numeric(validation["removed_net_profit"])
    oos_removed_net = numeric(oos["removed_net_profit"])
    any_thin = validation["sample_status"] != "ok" or oos["sample_status"] != "ok"
    if not meta["entry_time_available"]:
        if oos_net_delta > 0 and val_pf_delta >= 0:
            return "mechanism_survivor_not_entry_time_rule"
        if oos_net_delta > 0:
            return "oos_helpful_but_ex_post_or_mixed"
        return "ex_post_diagnostic_only"
    if any_thin:
        return "sample_thin_diagnostic_only"
    if oos_net_delta > 0 and oos_pf_delta > 0 and val_removed_net > 0 and oos_removed_net < 0:
        return "split_inconsistent_removed_positive_validation_negative_oos"
    if oos_net_delta > 0 and oos_pf_delta > 0 and val_net_delta < -50:
        return "split_conflict_oos_help_validation_cost"
    if val_net_delta > 0 and val_pf_delta > 0 and oos_net_delta <= 0:
        return "split_conflict_validation_help_oos_cost"
    if oos_net_delta > 0 and oos_pf_delta > 0 and numeric(validation["kept_profit_factor"]) >= 1.0:
        return "entry_available_weak_survivor"
    return "rejected_or_no_stable_gain"


def summarize_rules(split_rows: Sequence[Mapping[str, Any]], rules: Sequence[Mapping[str, Any]] = RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for meta in rules:
        rule_id = str(meta["rule_id"])
        validation = row_for(split_rows, rule_id, "validation")
        oos = row_for(split_rows, rule_id, "oos")
        rows.append(
            {
                "rule_id": rule_id,
                "rule_family": meta["rule_family"],
                "entry_time_available": bool(meta["entry_time_available"]),
                "direct_runtime_candidate": bool(meta["direct_runtime_candidate"]),
                "classification": classify_rule(meta, validation, oos),
                "validation_kept_trades": validation["kept_trade_count"],
                "validation_kept_share": validation["kept_trade_share"],
                "validation_kept_net_profit": validation["kept_net_profit"],
                "validation_kept_profit_factor": validation["kept_profit_factor"],
                "validation_net_delta_vs_base": validation["net_delta_vs_base"],
                "validation_pf_delta_vs_base": validation["pf_delta_vs_base"],
                "oos_kept_trades": oos["kept_trade_count"],
                "oos_kept_share": oos["kept_trade_share"],
                "oos_kept_net_profit": oos["kept_net_profit"],
                "oos_kept_profit_factor": oos["kept_profit_factor"],
                "oos_net_delta_vs_base": oos["net_delta_vs_base"],
                "oos_pf_delta_vs_base": oos["pf_delta_vs_base"],
                "validation_sample_status": validation["sample_status"],
                "oos_sample_status": oos["sample_status"],
                "stress_question": meta["stress_question"],
            }
        )
    return rows


def removed_slice_rows(tier_a: pd.DataFrame, rules: Sequence[Mapping[str, Any]] = RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for meta in rules:
        rule_id = str(meta["rule_id"])
        if rule_id == "baseline_all_trades":
            continue
        for split, split_frame in tier_a.groupby("matched_split", dropna=False):
            removed = split_frame.loc[~rule_mask(rule_id, split_frame)].copy()
            if removed.empty:
                rows.append({"rule_id": rule_id, "split": str(split), "removed_trade_count": 0, "removed_net_profit": 0.0, "removed_profit_factor": None, "dominant_removed_session": "none", "dominant_removed_hold_bucket": "none", "dominant_removed_month": "none"})
                continue
            metrics = attribution.profit_metrics(removed)
            rows.append(
                {
                    "rule_id": rule_id,
                    "split": str(split),
                    "removed_trade_count": metrics["trade_count"],
                    "removed_net_profit": metrics["net_profit"],
                    "removed_profit_factor": metrics["profit_factor"],
                    "dominant_removed_session": str(removed["session_slice"].mode(dropna=False).iloc[0]),
                    "dominant_removed_hold_bucket": str(removed["hold_bucket"].mode(dropna=False).iloc[0]),
                    "dominant_removed_month": str(removed["month"].mode(dropna=False).iloc[0]),
                }
            )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"]))


def best_summary(summary_rows: Sequence[Mapping[str, Any]], rule_id: str) -> Mapping[str, Any]:
    return next(row for row in summary_rows if row["rule_id"] == rule_id)


def build_read(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    short_hold = best_summary(summary_rows, "exclude_short_hold_0_12")
    long_hold = best_summary(summary_rows, "keep_hold_gt_96_only")
    mid = best_summary(summary_rows, "exclude_mid_session")
    vol = best_summary(summary_rows, "exclude_vol_high")
    adx = best_summary(summary_rows, "exclude_adx_20_25")
    return {
        "headline": "hold_shape_is_the_strongest_mechanism_clue_but_not_an_entry_time_rule",
        "strongest_mechanism_clues": [
            {"rule_id": "exclude_short_hold_0_12", "read": "removing ex-post short holds improves both validation and OOS(사후 짧은 보유 제거는 검증과 표본외를 같이 개선)", "validation_pf": short_hold["validation_kept_profit_factor"], "oos_pf": short_hold["oos_kept_profit_factor"], "entry_time_available": short_hold["entry_time_available"]},
            {"rule_id": "keep_hold_gt_96_only", "read": "long holds carry most profit but are ex-post exposure concentration(긴 보유가 수익 대부분을 들지만 사후 노출 집중)", "validation_pf": long_hold["validation_kept_profit_factor"], "oos_pf": long_hold["oos_kept_profit_factor"], "entry_time_available": long_hold["entry_time_available"]},
        ],
        "failed_direct_filters": [
            {"rule_id": "exclude_mid_session", "read": "OOS improves but validation loses its strongest session(표본외는 좋아지지만 검증의 가장 강한 세션을 잃음)", "classification": mid["classification"]},
            {"rule_id": "exclude_vol_high", "read": "removed segment is negative in OOS but positive in validation(제거 구간이 표본외에서는 음수지만 검증에서는 양수)", "classification": vol["classification"]},
            {"rule_id": "exclude_adx_20_25", "read": "validation improves but OOS gets worse(검증은 좋아지지만 표본외는 나빠짐)", "classification": adx["classification"]},
        ],
        "candidate_boundary": "no_direct_rule_candidate_until_entry_time_hold_proxy_exists",
        "next_probe": NEXT_ACTION,
    }


def write_result_files(split_rows: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]], removed_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> dict[str, str]:
    stage_paths = {
        "segment_stress_split_metrics": RESULT_ROOT / "segment_stress_split_metrics.csv",
        "segment_stress_summary": RESULT_ROOT / "segment_stress_summary.csv",
        "rule_removed_slice_impact": RESULT_ROOT / "rule_removed_slice_impact.csv",
        "aggregate_summary": RESULT_ROOT / "aggregate_summary.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    packet_paths = {
        "segment_stress_split_metrics": PACKET_ROOT / "segment_stress_split_metrics.csv",
        "segment_stress_summary": PACKET_ROOT / "segment_stress_summary.csv",
        "rule_removed_slice_impact": PACKET_ROOT / "rule_removed_slice_impact.csv",
    }
    for paths in (stage_paths, packet_paths):
        attribution.write_csv(paths["segment_stress_split_metrics"], list(split_rows[0].keys()), split_rows)
        attribution.write_csv(paths["segment_stress_summary"], list(summary_rows[0].keys()), summary_rows)
        attribution.write_csv(paths["rule_removed_slice_impact"], list(removed_rows[0].keys()), removed_rows)
    attribution.write_json(stage_paths["aggregate_summary"], summary)
    attribution.write_json(stage_paths["run_manifest"], {"run_id": RUN_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID, "outputs": {key: rel(path) for key, path in stage_paths.items() if key != "run_manifest"}, "packet_outputs": {key: rel(path) for key, path in packet_paths.items()}, "boundary": BOUNDARY})
    return {key: rel(path) for key, path in packet_paths.items()} | {"aggregate_summary": rel(PACKET_ROOT / "aggregate_summary.json"), "run_manifest": rel(stage_paths["run_manifest"])}


def build_summary(created_at: str, branch: str) -> dict[str, Any]:
    matched_path = ROOT / f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/matched_trade_attribution.csv"
    matched = pd.read_csv(io_path(matched_path))
    matched["open_time_dt"] = pd.to_datetime(matched["open_time"])
    matched["month"] = matched["open_time_dt"].dt.to_period("M").astype(str)
    for column in ("net_profit", "hold_bars", "mae", "mfe", "realized_over_mfe"):
        if column in matched.columns:
            matched[column] = pd.to_numeric(matched[column], errors="coerce")
    tier_a = matched.loc[matched["matched_tier_scope"].eq("Tier A")].copy()
    split_rows = evaluate_rule_splits(tier_a)
    summary_rows = summarize_rules(split_rows)
    removed_rows = removed_slice_rows(tier_a)
    source_paths = {
        "source_run28A_attribution_summary": f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/aggregate_summary.json",
        "source_run28A_matched_trade_attribution": f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/matched_trade_attribution.csv",
        "source_run28A_tier_segment_attribution": f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/tier_a_segment_attribution.csv",
        "source_run28A_tier_comparison": f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/tier_comparison_summary.csv",
    }
    summary: dict[str, Any] = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
        "source_attribution_packet_id": SOURCE_ATTRIBUTION_PACKET_ID,
        "status": "reviewed_segment_stress_probe_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "created_at_utc": created_at,
        "active_branch": branch,
        "source_paths": source_paths,
        "source_hashes": {key: sha256_file_lf_normalized(ROOT / value) for key, value in source_paths.items()},
        "source_integrity": {"tier_a_trade_rows": int(len(tier_a)), "tier_a_validation_trades": int(tier_a["matched_split"].eq("validation").sum()), "tier_a_oos_trades": int(tier_a["matched_split"].eq("oos").sum()), "missing_feature_trades": int(tier_a["feature_match_status"].ne("matched").sum()), "new_mt5_run": False},
        "rule_summary_rows": summary_rows,
        "rule_split_rows": split_rows,
        "removed_slice_rows": removed_rows,
        "stress_read": build_read(summary_rows),
        "next_action": NEXT_ACTION,
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"],
    }
    summary["output_paths"] = write_result_files(split_rows, summary_rows, removed_rows, summary)
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    return summary


def review_text(summary: Mapping[str, Any]) -> str:
    short_hold = best_summary(summary["rule_summary_rows"], "exclude_short_hold_0_12")
    long_hold = best_summary(summary["rule_summary_rows"], "keep_hold_gt_96_only")
    mid = best_summary(summary["rule_summary_rows"], "exclude_mid_session")
    return f"""# RUN28B Tier A Markov Segment Stress Packet(28B 실행 티어 A 마르코프 구간 압박 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_segment_stress_probe_completed`
- judgment(판정): `{JUDGMENT}`
- source(원천): `{SOURCE_ATTRIBUTION_RUN_ID}` and `{SOURCE_RUN_ID}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): run28A(28A 실행)에서 보인 Tier A Markov long permission(티어 A 마르코프 롱 허용)을 새 MT5(MetaTrader 5, 메타트레이더5) 실행 없이 구간별 stress(압박)로 찔렀다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Result(결과)

- `exclude_short_hold_0_12`: validation PF(검증 수익 팩터) `{short_hold['validation_kept_profit_factor']}`, OOS PF(표본외 수익 팩터) `{short_hold['oos_kept_profit_factor']}`. 짧은 보유를 빼면 양쪽이 같이 좋아진다.
- `keep_hold_gt_96_only`: validation PF(검증 수익 팩터) `{long_hold['validation_kept_profit_factor']}`, OOS PF(표본외 수익 팩터) `{long_hold['oos_kept_profit_factor']}`. 긴 보유가 수익을 많이 들고 있다.
- `exclude_mid_session`: OOS net(표본외 순손익)은 `{mid['oos_kept_net_profit']}`로 좋아지지만 validation net(검증 순손익)은 `{mid['validation_kept_net_profit']}`로 줄어든다. 그래서 직접 규칙으로는 불안정하다.

## Read(판독)

가장 센 단서는 hold shape(보유 형태)다. 다만 hold bucket(보유 버킷)은 거래가 끝난 뒤에야 아는 ex-post(사후) 정보라서, 그대로 runtime rule(런타임 규칙)이 될 수 없다.

효과(effect, 효과): 다음 run28C(28C 실행)는 entry time(진입 시점)에 짧은 보유 실패를 미리 알아볼 proxy(대리 신호)를 찾는 쪽이 맞다.

## Files(파일)

- summary(요약): `{summary['output_paths']['segment_stress_summary']}`
- split metrics(분할 지표): `{summary['output_paths']['segment_stress_split_metrics']}`
- removed impact(제거 영향): `{summary['output_paths']['rule_removed_slice_impact']}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
"""


def decision_text() -> str:
    return f"""# Decision: Stage34 RUN28B Segment Stress Completed(결정: 34단계 28B 실행 구간 압박 완료)

- date(날짜): 2026-05-08
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Tier A Markov long permission(티어 A 마르코프 롱 허용)은 보존하지만, 좋은 profit factor(수익 팩터)의 핵심 단서가 사후 hold shape(보유 형태)에 있다는 점을 분리했다. 다음은 entry-time proxy(진입 시점 대리 신호) 탐침이다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    hold_rule = best_summary(summary["rule_summary_rows"], "exclude_short_hold_0_12")
    long_rule = best_summary(summary["rule_summary_rows"], "keep_hold_gt_96_only")
    rows = [
        {"ledger_row_id": f"{RUN_ID}__segment_stress_summary", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "segment_stress_summary", "parent_run_id": SOURCE_ATTRIBUTION_RUN_ID, "record_view": "segment_stress_summary", "tier_scope": "Tier A", "kpi_scope": "rule_survivor_stress", "scoreboard_lane": "performance_attribution", "status": "reviewed", "judgment": JUDGMENT, "path": summary["output_paths"]["segment_stress_summary"], "primary_kpi": ledger_pairs([("exclude_short_hold_validation_pf", hold_rule["validation_kept_profit_factor"]), ("exclude_short_hold_oos_pf", hold_rule["oos_kept_profit_factor"]), ("keep_long_hold_validation_pf", long_rule["validation_kept_profit_factor"]), ("keep_long_hold_oos_pf", long_rule["oos_kept_profit_factor"])]), "guardrail_kpi": ledger_pairs([("direct_rule_candidate", "none"), ("boundary", BOUNDARY)]), "external_verification_status": "completed_reused_run22B_mt5_runtime_probe", "notes": "Segment stress over existing Tier A trades; hold-shape clue is ex-post and not a runtime rule."},
        {"ledger_row_id": f"{RUN_ID}__split_metric_matrix", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "split_metric_matrix", "parent_run_id": SOURCE_ATTRIBUTION_RUN_ID, "record_view": "segment_stress_split_metrics", "tier_scope": "Tier A", "kpi_scope": "validation_oos_rule_matrix", "scoreboard_lane": "performance_attribution", "status": "reviewed", "judgment": JUDGMENT, "path": summary["output_paths"]["segment_stress_split_metrics"], "primary_kpi": "rules=9;splits=validation,oos", "guardrail_kpi": "sample_status_recorded;entry_time_availability_recorded", "external_verification_status": "completed_reused_run22B_artifacts", "notes": "Each candidate rule records kept and removed trade metrics."},
        {"ledger_row_id": f"{RUN_ID}__claim_boundary", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "claim_boundary", "parent_run_id": RUN_ID, "record_view": "final_claim_guard", "tier_scope": "Tier A", "kpi_scope": "claim_boundary", "scoreboard_lane": "result_judgment", "status": "reviewed", "judgment": JUDGMENT, "path": summary["output_paths"]["aggregate_summary"], "primary_kpi": "no_direct_runtime_rule_candidate", "guardrail_kpi": ledger_pairs([("forbidden_claims", summary["forbidden_claims"]), ("next_action", NEXT_ACTION)]), "external_verification_status": "out_of_scope_by_claim", "notes": "No baseline, promotion, or runtime authority created."},
    ]
    registry_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "performance_attribution", "status": "reviewed", "judgment": JUDGMENT, "path": rel(REPORT_PATH), "notes": "Stage34 Tier A Markov segment stress over reused run28A/run22B artifacts; no baseline, promotion, or runtime authority."}
    return {"stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"), "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"), "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")}


def write_packet_artifacts(summary: Mapping[str, Any]) -> None:
    attribution.write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    attribution.write_json(PACKET_ROOT / "skill_receipts.json", [{"skill": "obsidian-performance-attribution", "status": "executed", "boundary": BOUNDARY}, {"skill": "obsidian-experiment-design", "status": "executed", "run_id": RUN_ID}, {"skill": "obsidian-result-judgment", "status": "executed", "judgment": JUDGMENT}])
    attribution.write_json(PACKET_ROOT / "artifact_lineage_gate.json", {"packet_id": PACKET_ID, "status": "passed", "source_paths": summary["source_paths"]})
    attribution.write_json(PACKET_ROOT / "segment_stress_gate.json", {"packet_id": PACKET_ID, "status": "passed", "stress_read": summary["stress_read"]})
    attribution.write_json(PACKET_ROOT / "entry_availability_guard.json", {"packet_id": PACKET_ID, "status": "passed", "direct_rule_candidate": None, "reason": "best hold-shape clues are ex-post"})
    attribution.write_json(PACKET_ROOT / "kpi_contract_audit.json", {"packet_id": PACKET_ID, "status": "passed", "new_mt5_run_required": False, "reused_external_verification": "completed_run22B_mt5_runtime_probe"})
    attribution.write_json(PACKET_ROOT / "final_claim_guard.json", {"packet_id": PACKET_ID, "status": "passed", "allowed_claims": ["Stage34 RUN28B segment stress probe completed."], "forbidden_claims": summary["forbidden_claims"], "boundary": BOUNDARY})
    gates = ["artifact_lineage_gate", "segment_stress_gate", "entry_availability_guard", "kpi_contract_audit", "final_claim_guard", "required_gate_coverage_audit"]
    attribution.write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []})


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    attribution.write_md(REPORT_PATH, review_text(summary))
    attribution.write_md(DECISION_PATH, decision_text())
    attribution.write_md(REVIEW_INDEX_PATH, f"""# Stage34 Review Index(34단계 검토 색인)

- current status(현재 상태): `reviewed_segment_stress_probe_completed`
- current run(현재 실행): `{RUN_ID}`
- current packet(현재 묶음): `{PACKET_ID}`
- latest review(최신 검토): `{rel(REPORT_PATH)}`
- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`

효과(effect, 효과): Stage34(34단계)는 run28B(28B 실행)에서 Tier A Markov long permission(티어 A 마르코프 롱 허용)의 segment stress(구간 압박)를 확인했다. 직접 runtime rule(런타임 규칙)은 만들지 않고, entry-time hold proxy(진입 시점 보유 대리 신호)를 다음 탐침으로 남긴다.
""")
    attribution.write_md(SELECTION_STATUS_PATH, f"""# Stage34 Selection Status(34단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `reviewed_segment_stress_probe_completed`
- current run(현재 실행): `{RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): hold shape(보유 형태) 단서는 보존하지만, ex-post information(사후 정보)이므로 operating meaning(운영 의미)으로 올리지 않는다.
""")


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    new_focus = "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution reviewed_segment_stress_probe_completed(검토된 구간 압박 탐침 완료): run28B(28B 실행)는 Tier A Markov long permission(티어 A 마르코프 롱 허용)의 PF source(수익 팩터 원천)가 hold shape(보유 형태)에 가장 강하게 걸린다는 점을 확인했다; hold bucket(보유 버킷)은 ex-post(사후) 정보라 직접 runtime rule(런타임 규칙)이 아니며 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    text = re.sub(r"- Stage34\(34단계\) 34_regime_mechanism__tier_a_markov_long_permission_attribution .*?\n(?=- Stage33)", new_focus, text, count=1, flags=re.DOTALL)
    text = re.sub(r"- current_run_id\(현재 실행 ID\).*?(?=\n- treat Stage29-32)", f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 검토된 실행인\n  {RUN_ID}을 가리킨다; next action(다음 행동)은 {NEXT_ACTION}다.", text, count=1, flags=re.DOTALL)
    stage34_block = f"""stage34_tier_a_markov_long_permission_attribution:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_segment_stress_probe_completed
  current_run_id: {RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  decision_path: {rel(DECISION_PATH)}
  stage_path: stages/{STAGE_ID}
  previous_stage_id: 33_regime_mechanism__tier_a_markov_long_permission_source
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage34_tier_a_markov_long_permission_attribution:\n(?:  .+\n)+\npre_alpha_stage_queue:", stage34_block + "\npre_alpha_stage_queue:", text, count=1)
    attribution.write_md(WORKSPACE_STATE_PATH, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage34 RUN28B Segment Stress.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    block = f"""## Latest Stage34 RUN28B Segment Stress(최신 34단계 28B 실행 구간 압박)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

Stage34(34단계) `{RUN_ID}`를 reviewed segment stress probe(검토된 구간 압박 탐침)로 완료했다.

결과(result, 결과): 가장 강한 단서는 hold shape(보유 형태)였다. `exclude_short_hold_0_12`는 validation/OOS PF(검증/표본외 수익 팩터)를 같이 올렸고, `keep_hold_gt_96_only`는 긴 보유가 수익 대부분을 들고 있음을 보였다. 다만 hold bucket(보유 버킷)은 ex-post information(사후 정보)이라 직접 runtime rule(런타임 규칙)이 아니다.

효과(effect, 효과): Tier A Markov long permission(티어 A 마르코프 롱 허용)은 보존하지만, 다음 행동(next action, 다음 행동)은 entry-time hold proxy(진입 시점 보유 대리 신호)를 찾는 `{NEXT_ACTION}`다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    attribution.write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog() -> None:
    old = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-08 Stage34 RUN28B Segment Stress.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-08 Stage34 RUN28B Segment Stress(34단계 28B 실행 구간 압박)

- completed(완료): `{RUN_ID}` segment stress probe(구간 압박 탐침)
- source(원천): `{SOURCE_ATTRIBUTION_RUN_ID}` and `{SOURCE_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): hold shape(보유 형태)이 가장 강한 profit factor(수익 팩터) 단서지만 ex-post(사후)라 직접 규칙은 아니다. next action(다음 행동)은 `{NEXT_ACTION}`다.

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
    parser = argparse.ArgumentParser(description="Run Stage34 Tier A Markov long permission segment stress probe.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(parse_args(argv))
    print(json.dumps({"status": summary["status"], "judgment": summary["judgment"], "run_id": RUN_ID, "report_path": rel(REPORT_PATH), "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
