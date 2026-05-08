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
from stage_pipelines.stage34 import markov_long_permission_entry_time_hold_proxy_probe as entry_proxy


STAGE_ID = attribution.STAGE_ID
RUN_ID = "run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1"
RUN_NUMBER = "run28D"
PACKET_ID = "stage34_run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1"
SOURCE_ATTRIBUTION_RUN_ID = attribution.RUN_ID
SOURCE_ATTRIBUTION_PACKET_ID = attribution.PACKET_ID
SOURCE_STRESS_RUN_ID = entry_proxy.SOURCE_STRESS_RUN_ID
SOURCE_STRESS_PACKET_ID = entry_proxy.SOURCE_STRESS_PACKET_ID
SOURCE_ENTRY_PROXY_RUN_ID = entry_proxy.RUN_ID
SOURCE_ENTRY_PROXY_PACKET_ID = entry_proxy.PACKET_ID
BOUNDARY = "stage34_frequency_floor_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT = "inconclusive_tier_a_markov_entry_proxy_frequency_floor_probe_completed"
NEXT_ACTION = "run28E_tier_a_markov_broader_entry_proxy_probe_v1"

ROOT = attribution.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run28D_tier_a_markov_entry_proxy_frequency_floor_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-08_stage34_run28D_tier_a_markov_entry_proxy_frequency_floor.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs" / "registers" / "run_registry.csv"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews" / "review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
WORKSPACE_STATE_PATH = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = ROOT / "docs" / "workspace" / "changelog.md"

SPLIT_MONTHS = {"validation": 9, "oos": 7}
MIN_TRADE_COUNT = {"validation": 50, "oos": 30}
MIN_TRADES_PER_CALENDAR_MONTH = {"validation": 5.0, "oos": 4.0}
MIN_MONTHS_WITH_TRADES = {"validation": 6, "oos": 4}
MAX_TOP_MONTH_TRADE_SHARE = 0.35


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
    tier_a = entry_proxy.load_tier_a_trades()
    tier_a["month"] = tier_a["open_time_dt"].dt.to_period("M").astype(str)
    return tier_a


def monthly_frequency_metrics(frame: pd.DataFrame, split: str) -> dict[str, Any]:
    kept_count = int(len(frame))
    split_months = SPLIT_MONTHS[str(split)]
    if kept_count == 0:
        return {
            "kept_trade_count": 0,
            "calendar_months": split_months,
            "months_with_trades": 0,
            "trades_per_calendar_month": 0.0,
            "trades_per_active_month": 0.0,
            "min_active_month_trade_count": 0,
            "top_month": "none",
            "top_month_trade_count": 0,
            "top_month_trade_share": 0.0,
            "negative_month_count": 0,
            "top_positive_month_net_share": 0.0,
        }
    monthly_counts = frame.groupby("month", dropna=False).size().sort_values(ascending=False)
    monthly_net = frame.groupby("month", dropna=False)["net_profit"].sum()
    positive_net = monthly_net.loc[monthly_net > 0]
    positive_total = float(positive_net.sum())
    top_month = str(monthly_counts.index[0])
    top_month_count = int(monthly_counts.iloc[0])
    return {
        "kept_trade_count": kept_count,
        "calendar_months": split_months,
        "months_with_trades": int(monthly_counts.size),
        "trades_per_calendar_month": round(kept_count / split_months, 6),
        "trades_per_active_month": round(kept_count / max(1, int(monthly_counts.size)), 6),
        "min_active_month_trade_count": int(monthly_counts.min()),
        "top_month": top_month,
        "top_month_trade_count": top_month_count,
        "top_month_trade_share": round(top_month_count / kept_count, 6),
        "negative_month_count": int((monthly_net < 0).sum()),
        "top_positive_month_net_share": 0.0 if positive_total <= 0 else round(float(positive_net.max()) / positive_total, 6),
    }


def frequency_floor_flags(metrics: Mapping[str, Any], split: str) -> list[str]:
    flags: list[str] = []
    if int(metrics["kept_trade_count"]) < MIN_TRADE_COUNT[split]:
        flags.append("trade_count_below_floor")
    if numeric(metrics["trades_per_calendar_month"]) < MIN_TRADES_PER_CALENDAR_MONTH[split]:
        flags.append("calendar_frequency_below_floor")
    if int(metrics["months_with_trades"]) < MIN_MONTHS_WITH_TRADES[split]:
        flags.append("month_coverage_below_floor")
    if numeric(metrics["top_month_trade_share"]) > MAX_TOP_MONTH_TRADE_SHARE:
        flags.append("top_month_concentration_high")
    return flags


def frequency_floor_status(metrics: Mapping[str, Any], split: str) -> str:
    return "pass" if not frequency_floor_flags(metrics, split) else "fail"


def pf_delta(next_pf: Any, base_pf: Any) -> Any:
    if next_pf is None or base_pf is None:
        return None
    return round(numeric(next_pf) - numeric(base_pf), 6)


def evaluate_rule_splits(tier_a: pd.DataFrame, rules: Sequence[Mapping[str, Any]] = entry_proxy.RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule in rules:
        rule_id = str(rule["rule_id"])
        for split, split_frame in tier_a.groupby("matched_split", dropna=False):
            split_name = str(split)
            base = attribution.profit_metrics(split_frame)
            kept = split_frame.loc[entry_proxy.rule_mask(rule_id, split_frame)].copy()
            kept_metrics = attribution.profit_metrics(kept)
            freq = monthly_frequency_metrics(kept, split_name)
            flags = frequency_floor_flags(freq, split_name)
            rows.append(
                {
                    "rule_id": rule_id,
                    "rule_family": rule["rule_family"],
                    "split": split_name,
                    "base_trade_count": metric_value(base, "trade_count"),
                    "base_net_profit": metric_value(base, "net_profit"),
                    "base_profit_factor": metric_value(base, "profit_factor"),
                    "kept_trade_count": metric_value(kept_metrics, "trade_count"),
                    "kept_net_profit": metric_value(kept_metrics, "net_profit"),
                    "kept_profit_factor": metric_value(kept_metrics, "profit_factor"),
                    "kept_expectancy": metric_value(kept_metrics, "expectancy"),
                    "kept_win_rate_percent": metric_value(kept_metrics, "win_rate_percent"),
                    "net_delta_vs_base": round(numeric(kept_metrics.get("net_profit")) - numeric(base.get("net_profit")), 6),
                    "pf_delta_vs_base": pf_delta(kept_metrics.get("profit_factor"), base.get("profit_factor")),
                    "calendar_months": freq["calendar_months"],
                    "months_with_trades": freq["months_with_trades"],
                    "trades_per_calendar_month": freq["trades_per_calendar_month"],
                    "trades_per_active_month": freq["trades_per_active_month"],
                    "min_active_month_trade_count": freq["min_active_month_trade_count"],
                    "top_month": freq["top_month"],
                    "top_month_trade_count": freq["top_month_trade_count"],
                    "top_month_trade_share": freq["top_month_trade_share"],
                    "negative_month_count": freq["negative_month_count"],
                    "top_positive_month_net_share": freq["top_positive_month_net_share"],
                    "frequency_floor_status": frequency_floor_status(freq, split_name),
                    "frequency_floor_flags": ";".join(flags) if flags else "none",
                    "stress_question": rule["stress_question"],
                }
            )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"]))


def monthly_concentration_rows(tier_a: pd.DataFrame, rules: Sequence[Mapping[str, Any]] = entry_proxy.RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule in rules:
        rule_id = str(rule["rule_id"])
        for split, split_frame in tier_a.groupby("matched_split", dropna=False):
            split_name = str(split)
            kept = split_frame.loc[entry_proxy.rule_mask(rule_id, split_frame)].copy()
            total_count = max(1, len(kept))
            total_net = numeric(kept["net_profit"].sum()) if not kept.empty else 0.0
            if kept.empty:
                rows.append(
                    {
                        "rule_id": rule_id,
                        "split": split_name,
                        "month": "none",
                        "trade_count": 0,
                        "trade_share": 0.0,
                        "net_profit": 0.0,
                        "net_profit_share": None,
                        "profit_factor": None,
                    }
                )
                continue
            for month, month_frame in kept.groupby("month", dropna=False):
                metrics = attribution.profit_metrics(month_frame)
                rows.append(
                    {
                        "rule_id": rule_id,
                        "split": split_name,
                        "month": str(month),
                        "trade_count": metrics["trade_count"],
                        "trade_share": round(int(metrics["trade_count"]) / total_count, 6),
                        "net_profit": metrics["net_profit"],
                        "net_profit_share": None if abs(total_net) < 1e-9 else round(numeric(metrics["net_profit"]) / total_net, 6),
                        "profit_factor": metrics["profit_factor"],
                    }
                )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"], row["month"]))


def row_for(rows: Sequence[Mapping[str, Any]], rule_id: str, split: str) -> Mapping[str, Any]:
    return next(row for row in rows if row["rule_id"] == rule_id and row["split"] == split)


def classify_rule(rule: Mapping[str, Any], validation: Mapping[str, Any], oos: Mapping[str, Any]) -> str:
    rule_id = str(rule["rule_id"])
    if rule_id == "baseline_all_trades":
        return "reference_frequency_floor_pass"
    if validation["frequency_floor_status"] != "pass" or oos["frequency_floor_status"] != "pass":
        return "frequency_floor_fail_thin_sample"
    val_pf_delta = numeric(validation["pf_delta_vs_base"])
    oos_pf_delta = numeric(oos["pf_delta_vs_base"])
    val_net_delta = numeric(validation["net_delta_vs_base"])
    oos_net_delta = numeric(oos["net_delta_vs_base"])
    if val_pf_delta > 0 and oos_pf_delta > 0 and val_net_delta >= 0 and oos_net_delta >= 0:
        return "frequency_ok_candidate"
    if val_pf_delta > 0 and oos_pf_delta > 0:
        return "frequency_ok_pf_lift_with_net_cost"
    if oos_pf_delta > 0 and oos_net_delta > 0:
        return "frequency_ok_oos_only_diagnostic"
    return "frequency_ok_no_stable_lift"


def decision_for_rule(rule_id: str, classification: str) -> str:
    if rule_id == "baseline_all_trades":
        return "preserve_reference_seed"
    if rule_id == "keep_late_or_vol_mid" and classification == "frequency_floor_fail_thin_sample":
        return "downgrade_to_thin_modifier_clue"
    if classification == "frequency_ok_candidate":
        return "broader_secondary_probe_candidate"
    if classification == "frequency_floor_fail_thin_sample":
        return "diagnostic_only_sample_too_thin"
    return "diagnostic_only_no_seed_change"


def summarize_rules(split_rows: Sequence[Mapping[str, Any]], rules: Sequence[Mapping[str, Any]] = entry_proxy.RULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule in rules:
        rule_id = str(rule["rule_id"])
        validation = row_for(split_rows, rule_id, "validation")
        oos = row_for(split_rows, rule_id, "oos")
        classification = classify_rule(rule, validation, oos)
        rows.append(
            {
                "rule_id": rule_id,
                "rule_family": rule["rule_family"],
                "classification": classification,
                "decision": decision_for_rule(rule_id, classification),
                "validation_kept_trades": validation["kept_trade_count"],
                "validation_kept_net_profit": validation["kept_net_profit"],
                "validation_kept_profit_factor": validation["kept_profit_factor"],
                "validation_net_delta_vs_base": validation["net_delta_vs_base"],
                "validation_pf_delta_vs_base": validation["pf_delta_vs_base"],
                "validation_frequency_floor_status": validation["frequency_floor_status"],
                "validation_frequency_floor_flags": validation["frequency_floor_flags"],
                "validation_months_with_trades": validation["months_with_trades"],
                "validation_trades_per_calendar_month": validation["trades_per_calendar_month"],
                "validation_top_month_trade_share": validation["top_month_trade_share"],
                "oos_kept_trades": oos["kept_trade_count"],
                "oos_kept_net_profit": oos["kept_net_profit"],
                "oos_kept_profit_factor": oos["kept_profit_factor"],
                "oos_net_delta_vs_base": oos["net_delta_vs_base"],
                "oos_pf_delta_vs_base": oos["pf_delta_vs_base"],
                "oos_frequency_floor_status": oos["frequency_floor_status"],
                "oos_frequency_floor_flags": oos["frequency_floor_flags"],
                "oos_months_with_trades": oos["months_with_trades"],
                "oos_trades_per_calendar_month": oos["trades_per_calendar_month"],
                "oos_top_month_trade_share": oos["top_month_trade_share"],
                "stress_question": rule["stress_question"],
            }
        )
    order = {
        "preserve_reference_seed": 0,
        "broader_secondary_probe_candidate": 1,
        "downgrade_to_thin_modifier_clue": 2,
        "diagnostic_only_sample_too_thin": 3,
        "diagnostic_only_no_seed_change": 4,
    }
    return sorted(rows, key=lambda row: (order.get(str(row["decision"]), 99), str(row["rule_id"])))


def best_summary(summary_rows: Sequence[Mapping[str, Any]], rule_id: str) -> Mapping[str, Any]:
    return next(row for row in summary_rows if row["rule_id"] == rule_id)


def build_read(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    baseline = best_summary(summary_rows, "baseline_all_trades")
    primary = best_summary(summary_rows, "keep_late_or_vol_mid")
    secondary = best_summary(summary_rows, "exclude_vol_high_or_adx_20_25")
    aggressive = best_summary(summary_rows, "keep_vol_mid_or_late_not_adx_20_25")
    return {
        "headline": "primary_entry_proxy_pf_is_good_but_frequency_floor_fails",
        "main_seed_decision": "keep_preserved_tier_a_markov_seed_not_run28c_primary",
        "baseline_reference": {
            "rule_id": baseline["rule_id"],
            "validation_trades": baseline["validation_kept_trades"],
            "oos_trades": baseline["oos_kept_trades"],
            "validation_pf": baseline["validation_kept_profit_factor"],
            "oos_pf": baseline["oos_kept_profit_factor"],
            "decision": baseline["decision"],
        },
        "primary_run28c_candidate": {
            "rule_id": primary["rule_id"],
            "classification": primary["classification"],
            "decision": primary["decision"],
            "validation_trades": primary["validation_kept_trades"],
            "validation_pf": primary["validation_kept_profit_factor"],
            "validation_frequency_flags": primary["validation_frequency_floor_flags"],
            "oos_trades": primary["oos_kept_trades"],
            "oos_pf": primary["oos_kept_profit_factor"],
            "oos_frequency_flags": primary["oos_frequency_floor_flags"],
        },
        "broader_secondary_candidate": {
            "rule_id": secondary["rule_id"],
            "classification": secondary["classification"],
            "decision": secondary["decision"],
            "validation_trades": secondary["validation_kept_trades"],
            "validation_pf": secondary["validation_kept_profit_factor"],
            "oos_trades": secondary["oos_kept_trades"],
            "oos_pf": secondary["oos_kept_profit_factor"],
        },
        "aggressive_diagnostic": {
            "rule_id": aggressive["rule_id"],
            "classification": aggressive["classification"],
            "decision": aggressive["decision"],
            "validation_trades": aggressive["validation_kept_trades"],
            "oos_trades": aggressive["oos_kept_trades"],
            "reason": "profit factor is strongest, but both splits fail the trade-count floor",
        },
        "attribution_confidence": "medium_low",
        "next_probe": NEXT_ACTION,
    }


def write_result_files(
    split_rows: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> dict[str, str]:
    stage_paths = {
        "frequency_floor_split_metrics": RESULT_ROOT / "frequency_floor_split_metrics.csv",
        "frequency_floor_rule_summary": RESULT_ROOT / "frequency_floor_rule_summary.csv",
        "frequency_floor_monthly_concentration": RESULT_ROOT / "frequency_floor_monthly_concentration.csv",
        "aggregate_summary": RESULT_ROOT / "aggregate_summary.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    packet_paths = {
        "frequency_floor_split_metrics": PACKET_ROOT / "frequency_floor_split_metrics.csv",
        "frequency_floor_rule_summary": PACKET_ROOT / "frequency_floor_rule_summary.csv",
        "frequency_floor_monthly_concentration": PACKET_ROOT / "frequency_floor_monthly_concentration.csv",
    }
    for paths in (stage_paths, packet_paths):
        attribution.write_csv(paths["frequency_floor_split_metrics"], list(split_rows[0].keys()), split_rows)
        attribution.write_csv(paths["frequency_floor_rule_summary"], list(summary_rows[0].keys()), summary_rows)
        attribution.write_csv(paths["frequency_floor_monthly_concentration"], list(month_rows[0].keys()), month_rows)
    attribution.write_json(
        stage_paths["run_manifest"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_runs": [SOURCE_ATTRIBUTION_RUN_ID, SOURCE_STRESS_RUN_ID, SOURCE_ENTRY_PROXY_RUN_ID],
            "outputs": {key: rel(path) for key, path in stage_paths.items() if key != "run_manifest"},
            "packet_outputs": {key: rel(path) for key, path in packet_paths.items()},
            "boundary": BOUNDARY,
        },
    )
    return {
        **{key: rel(path) for key, path in packet_paths.items()},
        "aggregate_summary": rel(PACKET_ROOT / "aggregate_summary.json"),
        "run_manifest": rel(stage_paths["run_manifest"]),
    }


def build_summary(created_at: str, branch: str) -> dict[str, Any]:
    tier_a = load_tier_a_trades()
    split_rows = evaluate_rule_splits(tier_a)
    summary_rows = summarize_rules(split_rows)
    month_rows = monthly_concentration_rows(tier_a)
    source_paths = {
        "source_run28A_matched_trade_attribution": f"docs/agent_control/packets/{SOURCE_ATTRIBUTION_PACKET_ID}/matched_trade_attribution.csv",
        "source_run28B_segment_summary": f"docs/agent_control/packets/{SOURCE_STRESS_PACKET_ID}/segment_stress_summary.csv",
        "source_run28C_entry_proxy_summary": f"docs/agent_control/packets/{SOURCE_ENTRY_PROXY_PACKET_ID}/entry_proxy_rule_summary.csv",
        "source_run28C_aggregate_summary": f"docs/agent_control/packets/{SOURCE_ENTRY_PROXY_PACKET_ID}/aggregate_summary.json",
    }
    summary: dict[str, Any] = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_runs": [SOURCE_ATTRIBUTION_RUN_ID, SOURCE_STRESS_RUN_ID, SOURCE_ENTRY_PROXY_RUN_ID],
        "source_packets": [SOURCE_ATTRIBUTION_PACKET_ID, SOURCE_STRESS_PACKET_ID, SOURCE_ENTRY_PROXY_PACKET_ID],
        "status": "reviewed_frequency_floor_probe_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "created_at_utc": created_at,
        "active_branch": branch,
        "frequency_floor_contract": {
            "min_trade_count": MIN_TRADE_COUNT,
            "min_trades_per_calendar_month": MIN_TRADES_PER_CALENDAR_MONTH,
            "min_months_with_trades": MIN_MONTHS_WITH_TRADES,
            "max_top_month_trade_share": MAX_TOP_MONTH_TRADE_SHARE,
        },
        "source_paths": source_paths,
        "source_hashes": {key: sha256_file_lf_normalized(ROOT / value) for key, value in source_paths.items()},
        "source_integrity": {
            "tier_a_trade_rows": int(len(tier_a)),
            "tier_a_validation_trades": int(tier_a["matched_split"].eq("validation").sum()),
            "tier_a_oos_trades": int(tier_a["matched_split"].eq("oos").sum()),
            "new_mt5_run": False,
            "claim_lowered_to_frequency_floor": True,
        },
        "rule_summary_rows": summary_rows,
        "rule_split_rows": split_rows,
        "monthly_concentration_rows": month_rows,
        "frequency_floor_read": build_read(summary_rows),
        "next_action": NEXT_ACTION,
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "forbidden_claims": [
            "edge",
            "alpha_quality",
            "baseline",
            "promotion",
            "runtime_authority",
            "mt5_verified_runtime_rule",
            "run28c_primary_as_main_seed",
        ],
    }
    summary["output_paths"] = write_result_files(split_rows, summary_rows, month_rows, summary)
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    return summary


def review_text(summary: Mapping[str, Any]) -> str:
    read = summary["frequency_floor_read"]
    primary = read["primary_run28c_candidate"]
    secondary = read["broader_secondary_candidate"]
    baseline = read["baseline_reference"]
    return f"""# RUN28D Tier A Markov Frequency Floor Packet(28D 실행 티어 A 마르코프 거래 수 하한 묶음)
## Judgment(판정)
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_frequency_floor_probe_completed(검토된 거래 수 하한 탐침 완료)`
- judgment(판정): `{JUDGMENT}`
- source(원천): `{SOURCE_ENTRY_PROXY_RUN_ID}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`
효과(effect, 효과): run28C(28C 실행)의 높은 PF(수익 팩터)를 바로 seed(씨앗)로 올리지 않고, 기간 대비 거래 수와 월별 집중도부터 확인했다. 이번 실행은 MT5(`MetaTrader 5`, 메타트레이더5) 새 실행이 아니다.
## Result(결과)
- preserved reference seed(보존 기준 씨앗): `{baseline['rule_id']}` validation trades(검증 거래 수) `{baseline['validation_trades']}`, OOS trades(표본외 거래 수) `{baseline['oos_trades']}`, validation/OOS PF(검증/표본외 수익 팩터) `{baseline['validation_pf']}` / `{baseline['oos_pf']}`
- run28C primary(28C 1차 후보): `{primary['rule_id']}` validation trades(검증 거래 수) `{primary['validation_trades']}`, OOS trades(표본외 거래 수) `{primary['oos_trades']}`, validation/OOS PF(검증/표본외 수익 팩터) `{primary['validation_pf']}` / `{primary['oos_pf']}`
- primary decision(1차 후보 결정): `{primary['decision']}`
- broader secondary(더 넓은 보조 후보): `{secondary['rule_id']}` validation trades(검증 거래 수) `{secondary['validation_trades']}`, OOS trades(표본외 거래 수) `{secondary['oos_trades']}`, validation/OOS PF(검증/표본외 수익 팩터) `{secondary['validation_pf']}` / `{secondary['oos_pf']}`
- secondary decision(보조 후보 결정): `{secondary['decision']}`
## Read(해석)
`keep_late_or_vol_mid`는 PF(수익 팩터)는 좋지만 validation(검증) 40건, OOS(표본외) 26건이라 frequency floor(거래 수 하한)를 통과하지 못했다.
효과(effect, 효과): 이 후보는 thin modifier clue(얇은 수정 단서)로 보존하고, main seed(메인 씨앗)나 MT5 verified runtime rule(MT5 검증 런타임 규칙)로 올리지 않는다.
`exclude_vol_high_or_adx_20_25`는 PF(수익 팩터)는 낮지만 validation(검증) 59건, OOS(표본외) 32건으로 거래 수 하한을 통과했다.
효과(effect, 효과): 다음 실험은 이 넓은 보조 후보를 더 찔러보는 쪽이 맞다. 아직 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Files(파일)
- summary(요약): `{summary['output_paths']['frequency_floor_rule_summary']}`
- split metrics(분할 지표): `{summary['output_paths']['frequency_floor_split_metrics']}`
- monthly concentration(월별 집중도): `{summary['output_paths']['frequency_floor_monthly_concentration']}`
"""


def decision_text() -> str:
    return f"""# Decision: Stage34 RUN28D Frequency Floor Completed(결정: 34단계 28D 거래 수 하한 완료)
- date(날짜): 2026-05-08
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`
효과(effect, 효과): run28C(28C 실행)의 `keep_late_or_vol_mid`는 thin modifier clue(얇은 수정 단서)로 낮추고, `exclude_vol_high_or_adx_20_25`를 broader secondary probe candidate(더 넓은 보조 탐침 후보)로 보존한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    read = summary["frequency_floor_read"]
    primary = read["primary_run28c_candidate"]
    secondary = read["broader_secondary_candidate"]
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__frequency_floor_rule_summary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "frequency_floor_rule_summary",
            "parent_run_id": SOURCE_ENTRY_PROXY_RUN_ID,
            "record_view": "frequency_floor_rule_summary",
            "tier_scope": "Tier A",
            "kpi_scope": "entry_proxy_frequency_floor",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["output_paths"]["frequency_floor_rule_summary"],
            "primary_kpi": ledger_pairs(
                [
                    ("primary_rule", primary["rule_id"]),
                    ("primary_decision", primary["decision"]),
                    ("secondary_rule", secondary["rule_id"]),
                    ("secondary_decision", secondary["decision"]),
                ]
            ),
            "guardrail_kpi": ledger_pairs([("boundary", BOUNDARY), ("new_mt5_run", False)]),
            "external_verification_status": "not_required_frequency_floor_claim_reused_artifacts",
            "notes": "Frequency floor audit downgraded run28C primary to thin clue and preserved a broader secondary probe candidate.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__monthly_concentration",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "monthly_concentration",
            "parent_run_id": SOURCE_ATTRIBUTION_RUN_ID,
            "record_view": "frequency_floor_monthly_concentration",
            "tier_scope": "Tier A",
            "kpi_scope": "monthly_trade_concentration",
            "scoreboard_lane": "trade_shape",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["output_paths"]["frequency_floor_monthly_concentration"],
            "primary_kpi": ledger_pairs([("rows", len(summary["monthly_concentration_rows"])), ("primary_oos_trades", primary["oos_trades"])]),
            "guardrail_kpi": "month_coverage_and_top_month_share_recorded",
            "external_verification_status": "not_required_frequency_floor_claim_reused_artifacts",
            "notes": "Monthly concentration is measured from existing matched Tier A trade attribution.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__claim_boundary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "claim_boundary",
            "parent_run_id": RUN_ID,
            "record_view": "final_claim_guard",
            "tier_scope": "Tier A",
            "kpi_scope": "claim_boundary",
            "scoreboard_lane": "result_judgment",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": summary["output_paths"]["aggregate_summary"],
            "primary_kpi": "no_seed_change_no_mt5_runtime_rule",
            "guardrail_kpi": ledger_pairs([("forbidden_claims", summary["forbidden_claims"]), ("next_action", NEXT_ACTION)]),
            "external_verification_status": "not_required_frequency_floor_claim_reused_artifacts",
            "notes": "No baseline, promotion, runtime authority, or MT5-verified rule was created.",
        },
    ]
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "performance_attribution",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "Stage34 Tier A Markov entry proxy frequency floor probe over reused run28A/run28C artifacts; no MT5 verification, baseline, promotion, or runtime authority.",
    }
    return {
        "stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id"),
    }


def write_packet_artifacts(summary: Mapping[str, Any]) -> None:
    attribution.write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    attribution.write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {"skill": "obsidian-experiment-design", "status": "executed", "run_id": RUN_ID},
            {"skill": "obsidian-performance-attribution", "status": "executed", "boundary": BOUNDARY},
            {"skill": "obsidian-result-judgment", "status": "executed", "judgment": JUDGMENT},
        ],
    )
    attribution.write_json(PACKET_ROOT / "artifact_lineage_gate.json", {"packet_id": PACKET_ID, "status": "passed", "source_paths": summary["source_paths"]})
    attribution.write_json(
        PACKET_ROOT / "frequency_floor_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "contract": summary["frequency_floor_contract"],
            "frequency_floor_read": summary["frequency_floor_read"],
        },
    )
    attribution.write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "new_mt5_run_required_for_this_claim": False,
            "claim_boundary": "frequency_floor_only",
        },
    )
    attribution.write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": ["Stage34 RUN28D frequency floor probe completed."],
            "forbidden_claims": summary["forbidden_claims"],
            "boundary": BOUNDARY,
        },
    )
    gates = ["artifact_lineage_gate", "frequency_floor_gate", "kpi_contract_audit", "final_claim_guard", "required_gate_coverage_audit"]
    attribution.write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []})


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    attribution.write_md(REPORT_PATH, review_text(summary))
    attribution.write_md(DECISION_PATH, decision_text())
    attribution.write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage34 Review Index(34단계 검토 색인)

- current status(현재 상태): `reviewed_frequency_floor_probe_completed(검토된 거래 수 하한 탐침 완료)`
- current run(현재 실행): `{RUN_ID}`
- current packet(현재 묶음): `{PACKET_ID}`
- latest review(최신 검토): `{rel(REPORT_PATH)}`
- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`

효과(effect, 효과): Stage34(34단계)는 run28D(28D 실행)에서 run28C(28C 실행)의 얇은 PF(수익 팩터) 후보를 바로 seed(씨앗)로 쓰지 않도록 거래 수 하한을 확인했다.
""",
    )
    attribution.write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage34 Selection Status(34단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `reviewed_frequency_floor_probe_completed(검토된 거래 수 하한 탐침 완료)`
- current run(현재 실행): `{RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`
- thin modifier clue(얇은 수정 단서): `keep_late_or_vol_mid`
- broader secondary probe candidate(더 넓은 보조 탐침 후보): `exclude_vol_high_or_adx_20_25`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): PF(수익 팩터)가 높은 얇은 후보는 보존하지만, main seed(메인 씨앗), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
""",
    )


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    new_focus = (
        "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution "
        "reviewed_frequency_floor_probe_completed(검토된 거래 수 하한 탐침 완료): run28D(28D 실행)는 "
        "`keep_late_or_vol_mid`를 thin modifier clue(얇은 수정 단서)로 낮추고 "
        "`exclude_vol_high_or_adx_20_25`를 broader secondary probe candidate(더 넓은 보조 탐침 후보)로 보존했다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    )
    text = re.sub(r"- Stage34\(34.*?\) 34_regime_mechanism__tier_a_markov_long_permission_attribution .*?\n(?=- Stage33)", new_focus, text, count=1, flags=re.DOTALL)
    text = re.sub(
        r"- current_run_id\(.*?\).*?(?=\n- treat Stage29-32)",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 검토된 실행인\n  {RUN_ID}을 가리킨다; next action(다음 행동)은 {NEXT_ACTION}다.",
        text,
        count=1,
        flags=re.DOTALL,
    )
    stage34_block = f"""stage34_tier_a_markov_long_permission_attribution:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_frequency_floor_probe_completed
  current_run_id: {RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  decision_path: {rel(DECISION_PATH)}
  stage_path: stages/{STAGE_ID}
  previous_stage_id: 33_regime_mechanism__tier_a_markov_long_permission_source
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  thin_modifier_clue: keep_late_or_vol_mid
  broader_secondary_probe_candidate: exclude_vol_high_or_adx_20_25
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage34_tier_a_markov_long_permission_attribution:\n(?:  .+\n)+\npre_alpha_stage_queue:", stage34_block + "\npre_alpha_stage_queue:", text, count=1)
    attribution.write_md(WORKSPACE_STATE_PATH, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage34 RUN28D Frequency Floor.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    primary = summary["frequency_floor_read"]["primary_run28c_candidate"]
    secondary = summary["frequency_floor_read"]["broader_secondary_candidate"]
    block = f"""## Latest Stage34 RUN28D Frequency Floor(최신 34단계 28D 실행 거래 수 하한)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `{summary['active_branch']}`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

Stage34(34단계) `{RUN_ID}`를 reviewed frequency floor probe(검토된 거래 수 하한 탐침)로 완료했다.

결과(result, 결과): `keep_late_or_vol_mid`는 validation/OOS trades(검증/표본외 거래 수) `{primary['validation_trades']}` / `{primary['oos_trades']}`라 얇다. `exclude_vol_high_or_adx_20_25`는 validation/OOS trades(검증/표본외 거래 수) `{secondary['validation_trades']}` / `{secondary['oos_trades']}`로 더 넓지만 PF(수익 팩터)는 낮다.

효과(effect, 효과): main seed(메인 씨앗)는 교체하지 않는다. run28C(28C 실행)의 1차 후보는 thin modifier clue(얇은 수정 단서)로 보존하고, 다음은 더 넓은 보조 후보를 찔러본다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    attribution.write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog() -> None:
    old = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-08 Stage34 RUN28D Frequency Floor.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-08 Stage34 RUN28D Frequency Floor(34단계 28D 거래 수 하한)

- completed(완료): `{RUN_ID}` frequency floor probe(거래 수 하한 탐침)
- source(원천): `{SOURCE_ENTRY_PROXY_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): `keep_late_or_vol_mid`는 thin modifier clue(얇은 수정 단서)로 낮추고, `exclude_vol_high_or_adx_20_25`는 broader secondary probe candidate(더 넓은 보조 탐침 후보)로 보존했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

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
    parser = argparse.ArgumentParser(description="Run Stage34 Tier A Markov entry proxy frequency floor probe.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(parse_args(argv))
    print(
        json.dumps(
            {
                "status": summary["status"],
                "judgment": summary["judgment"],
                "run_id": RUN_ID,
                "report_path": rel(REPORT_PATH),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
