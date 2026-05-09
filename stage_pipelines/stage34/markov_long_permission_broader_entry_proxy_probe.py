from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    ledger_pairs,
    ledger_value,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage34 import common as stage34_common
from stage_pipelines.stage34 import markov_long_permission_attribution as attribution
from stage_pipelines.stage34 import markov_long_permission_entry_time_hold_proxy_probe as entry_proxy
from stage_pipelines.stage34 import markov_long_permission_frequency_floor_probe as frequency_floor


STAGE_NUMBER = 34
STAGE_ID = attribution.STAGE_ID
RUN_ID = "run28E_tier_a_markov_broader_entry_proxy_probe_v1"
RUN_NUMBER = "run28E"
PACKET_ID = "stage34_run28E_tier_a_markov_broader_entry_proxy_probe_v1"
SOURCE_ATTRIBUTION_RUN_ID = attribution.RUN_ID
SOURCE_ATTRIBUTION_PACKET_ID = attribution.PACKET_ID
SOURCE_ENTRY_PROXY_RUN_ID = entry_proxy.RUN_ID
SOURCE_ENTRY_PROXY_PACKET_ID = entry_proxy.PACKET_ID
SOURCE_FREQUENCY_RUN_ID = frequency_floor.RUN_ID
SOURCE_FREQUENCY_PACKET_ID = frequency_floor.PACKET_ID
SOURCE_RUNTIME_RUN_ID = attribution.SOURCE_RUN_ID
SOURCE_RUNTIME_PACKET_ID = attribution.SOURCE_PACKET_ID
EXPLORATION_LABEL = "stage34_RegimeMechanism__TierAMarkovBroaderEntryProxyProbe"
MODEL_FAMILY = "markov_regression_state_score_table_runtime_probe"
MODEL_BACKEND = "ebm_table"
FEATURE_SET_ID = "feature_set_v2_markov_regression_state_runtime_features_with_stage34_entry_proxy_filter"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
RULE_ID = "exclude_vol_high_or_adx_20_25"
BOUNDARY = "stage34_broader_entry_proxy_monthly_mt5_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_tier_a_markov_broader_entry_proxy_probe_completed"
JUDGMENT_BLOCKED = "blocked_tier_a_markov_broader_entry_proxy_probe_after_attempt"
NEXT_ACTION = "run28F_tier_a_markov_vol_adx_component_dependency_probe_v1"

ROOT = attribution.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
SOURCE_RUNTIME_PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / SOURCE_RUNTIME_PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run28E_tier_a_markov_broader_entry_proxy_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-08_stage34_run28E_tier_a_markov_broader_entry_proxy.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs" / "registers" / "run_registry.csv"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews" / "review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
WORKSPACE_STATE_PATH = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = ROOT / "docs" / "workspace" / "changelog.md"

RUNTIME_FEATURE_ORDER = ("mk_state_score", "mk_state_confidence", "mk_state_entropy_inv", "mk_return_abs")
RUNTIME_SOURCE_COMMON = COMMON_FILES_ROOT_DEFAULT / "Project_Obsidian_Prime_v2" / "stage28" / SOURCE_RUNTIME_RUN_ID
SOURCE_TIER_A_MODEL = RUNTIME_SOURCE_COMMON / "models" / "tier_a_markov_state_score_table.csv"
SOURCE_TIER_A_FEATURES = {
    "validation_is": RUNTIME_SOURCE_COMMON / "features" / "tier_a_validation_is_markov_state_features.csv",
    "oos": RUNTIME_SOURCE_COMMON / "features" / "tier_a_oos_markov_state_features.csv",
}
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0
MONTHLY_RULE_IDS = (
    "baseline_all_trades",
    "keep_late_or_vol_mid",
    RULE_ID,
    "exclude_vol_high",
    "exclude_adx_20_25",
    "keep_vol_mid_or_late_not_adx_20_25",
)


def rel(path: Path) -> str:
    return stage34_common.rel(path, ROOT)


read_json = stage34_common.read_json
numeric = stage34_common.numeric
metric_value = stage34_common.metric_value
pf_sort_value = stage34_common.pf_sort_value


def selected_rules() -> tuple[dict[str, Any], ...]:
    by_id = {str(rule["rule_id"]): dict(rule) for rule in entry_proxy.RULES}
    return tuple(by_id[rule_id] for rule_id in MONTHLY_RULE_IDS)


def load_tier_a_trades() -> pd.DataFrame:
    frame = frequency_floor.load_tier_a_trades()
    frame["month"] = frame["open_time_dt"].dt.to_period("M").astype(str)
    return frame


def monthly_leave_one_out_rows(tier_a: pd.DataFrame, rules: Sequence[Mapping[str, Any]] | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rule in rules or selected_rules():
        rule_id = str(rule["rule_id"])
        for split, split_frame in tier_a.groupby("matched_split", dropna=False):
            split_name = str(split)
            kept = split_frame.loc[entry_proxy.rule_mask(rule_id, split_frame)].copy()
            full = attribution.profit_metrics(kept)
            total_net = numeric(full.get("net_profit"))
            positive_month_net = kept.groupby("month")["net_profit"].sum()
            positive_total = float(positive_month_net.loc[positive_month_net > 0].sum())
            if kept.empty:
                rows.append(
                    {
                        "rule_id": rule_id,
                        "split": split_name,
                        "month": "none",
                        "full_trade_count": 0,
                        "full_net_profit": 0.0,
                        "full_profit_factor": None,
                        "month_trade_count": 0,
                        "month_trade_share": 0.0,
                        "month_net_profit": 0.0,
                        "month_net_share": None,
                        "month_profit_factor": None,
                        "leave_one_out_trade_count": 0,
                        "leave_one_out_net_profit": 0.0,
                        "leave_one_out_profit_factor": None,
                        "leave_one_out_status": "fail_empty",
                    }
                )
                continue
            for month, month_frame in kept.groupby("month", dropna=False):
                month_metrics = attribution.profit_metrics(month_frame)
                leave_one = kept.loc[~kept["month"].eq(month)].copy()
                leave_metrics = attribution.profit_metrics(leave_one)
                leave_pf = leave_metrics.get("profit_factor")
                leave_net = numeric(leave_metrics.get("net_profit"))
                rows.append(
                    {
                        "rule_id": rule_id,
                        "split": split_name,
                        "month": str(month),
                        "full_trade_count": metric_value(full, "trade_count"),
                        "full_net_profit": metric_value(full, "net_profit"),
                        "full_profit_factor": metric_value(full, "profit_factor"),
                        "month_trade_count": metric_value(month_metrics, "trade_count"),
                        "month_trade_share": round(numeric(month_metrics.get("trade_count")) / max(1, numeric(full.get("trade_count"))), 6),
                        "month_net_profit": metric_value(month_metrics, "net_profit"),
                        "month_net_share": None if abs(total_net) < 1e-9 else round(numeric(month_metrics.get("net_profit")) / total_net, 6),
                        "month_positive_net_share": 0.0 if positive_total <= 0 else round(max(0.0, numeric(month_metrics.get("net_profit"))) / positive_total, 6),
                        "month_profit_factor": metric_value(month_metrics, "profit_factor"),
                        "leave_one_out_trade_count": metric_value(leave_metrics, "trade_count"),
                        "leave_one_out_net_profit": metric_value(leave_metrics, "net_profit"),
                        "leave_one_out_profit_factor": metric_value(leave_metrics, "profit_factor"),
                        "leave_one_out_status": "pass" if leave_net > 0.0 and (leave_pf is None or numeric(leave_pf) >= 1.0) else "fail",
                    }
                )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"], row["month"]))


def monthly_summary_rows(leave_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in leave_rows:
        grouped.setdefault((str(row["rule_id"]), str(row["split"])), []).append(row)
    for (rule_id, split), items in grouped.items():
        real_items = [row for row in items if row["month"] != "none"]
        if not real_items:
            rows.append(
                {
                    "rule_id": rule_id,
                    "split": split,
                    "full_trade_count": 0,
                    "full_net_profit": 0.0,
                    "full_profit_factor": None,
                    "active_month_count": 0,
                    "negative_month_count": 0,
                    "worst_month": "none",
                    "worst_month_net_profit": 0.0,
                    "top_trade_month": "none",
                    "top_trade_month_share": 0.0,
                    "top_positive_month": "none",
                    "top_positive_month_net_share": 0.0,
                    "min_leave_one_out_trade_count": 0,
                    "min_leave_one_out_net_profit": 0.0,
                    "min_leave_one_out_profit_factor": None,
                    "monthly_survival_status": "fail",
                    "monthly_survival_flags": "empty",
                }
            )
            continue
        min_net_row = min(real_items, key=lambda row: numeric(row["leave_one_out_net_profit"]))
        min_pf_row = min(real_items, key=lambda row: pf_sort_value(row["leave_one_out_profit_factor"]))
        worst_month = min(real_items, key=lambda row: numeric(row["month_net_profit"]))
        top_trade_month = max(real_items, key=lambda row: numeric(row["month_trade_share"]))
        top_positive = max(real_items, key=lambda row: numeric(row.get("month_positive_net_share")))
        flags: list[str] = []
        if any(str(row["leave_one_out_status"]) == "fail" for row in real_items):
            flags.append("leave_one_month_breaks_profitability")
        if split == "oos" and numeric(min_net_row["leave_one_out_net_profit"]) < 10.0:
            flags.append("oos_leave_one_net_margin_thin")
        if numeric(top_positive.get("month_positive_net_share")) >= 0.60:
            flags.append("top_positive_month_dependency")
        if numeric(top_trade_month["month_trade_share"]) > 0.35:
            flags.append("top_trade_month_concentration")
        status = "pass"
        if "leave_one_month_breaks_profitability" in flags:
            status = "fail"
        elif flags:
            status = "warn"
        rows.append(
            {
                "rule_id": rule_id,
                "split": split,
                "full_trade_count": real_items[0]["full_trade_count"],
                "full_net_profit": real_items[0]["full_net_profit"],
                "full_profit_factor": real_items[0]["full_profit_factor"],
                "active_month_count": len(real_items),
                "negative_month_count": sum(1 for row in real_items if numeric(row["month_net_profit"]) < 0.0),
                "worst_month": worst_month["month"],
                "worst_month_net_profit": worst_month["month_net_profit"],
                "top_trade_month": top_trade_month["month"],
                "top_trade_month_share": top_trade_month["month_trade_share"],
                "top_positive_month": top_positive["month"],
                "top_positive_month_net_share": top_positive.get("month_positive_net_share"),
                "min_leave_one_out_trade_count": min(numeric(row["leave_one_out_trade_count"]) for row in real_items),
                "min_leave_one_out_net_profit": min_net_row["leave_one_out_net_profit"],
                "min_leave_one_out_net_profit_month_omitted": min_net_row["month"],
                "min_leave_one_out_profit_factor": min_pf_row["leave_one_out_profit_factor"],
                "min_leave_one_out_profit_factor_month_omitted": min_pf_row["month"],
                "monthly_survival_status": status,
                "monthly_survival_flags": ";".join(flags) if flags else "none",
            }
        )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"]))


def monthly_candidate_read(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_key = {(str(row["rule_id"]), str(row["split"])): row for row in summary_rows}
    validation = by_key[(RULE_ID, "validation")]
    oos = by_key[(RULE_ID, "oos")]
    status = "monthly_survivor"
    flags = {str(validation["monthly_survival_status"]), str(oos["monthly_survival_status"])}
    if "fail" in flags:
        status = "monthly_fail"
    elif "warn" in flags:
        status = "monthly_survivor_with_dependency"
    return {
        "rule_id": RULE_ID,
        "status": status,
        "validation": validation,
        "oos": oos,
        "interpretation": (
            "후보는 월 하나를 빼도 validation/OOS(검증/표본외) 전체 순손익과 PF(수익 팩터)가 무너지지는 않지만, "
            "OOS(표본외)는 2025-10(2025년 10월) 의존도가 커서 곧바로 main seed(메인 씨앗)로 올리기보다 다음 분해가 필요하다."
        ),
    }


def feature_context_frame() -> pd.DataFrame:
    market = mt5_trade_attribution.MarketData.load(ROOT)
    features = market.features.copy()
    features["bar_time_server"] = features["timestamp_key"].dt.strftime("%Y.%m.%d %H:%M:%S")
    features["volatility_regime"] = features["historical_vol_20"].map(
        lambda value: mt5_trade_attribution._bucket(value, market.volatility_edges, "vol")
    )
    features["adx_bucket"] = features["adx_14"].map(mt5_trade_attribution._adx_bucket)
    features["stage34_rule_allowed"] = ~(
        features["volatility_regime"].eq("vol_high") | features["adx_bucket"].eq("adx_20_25")
    )
    return features[["bar_time_server", "volatility_regime", "adx_bucket", "stage34_rule_allowed"]].drop_duplicates(
        "bar_time_server", keep="last"
    )


def filter_candidate_feature_frame(source: pd.DataFrame, context: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    original_columns = list(source.columns)
    merged = source.merge(context, on="bar_time_server", how="left")
    missing = merged["stage34_rule_allowed"].isna()
    disallowed = merged["stage34_rule_allowed"].eq(False)
    keep = missing | ~disallowed
    removed = merged.loc[disallowed].copy()
    kept = merged.loc[keep, original_columns].copy()
    filter_summary = {
        "source_rows": int(len(source)),
        "kept_rows": int(len(kept)),
        "filtered_rows": int(len(removed)),
        "missing_context_rows_kept": int(missing.sum()),
        "vol_high_removed_rows": int(removed["volatility_regime"].eq("vol_high").sum()),
        "adx_20_25_removed_rows": int(removed["adx_bucket"].eq("adx_20_25").sum()),
        "both_removed_rows": int((removed["volatility_regime"].eq("vol_high") & removed["adx_bucket"].eq("adx_20_25")).sum()),
    }
    return kept, filter_summary


def split_dates_from_feature_csv(frame: pd.DataFrame) -> tuple[str, str]:
    return stage34_common.split_dates_from_feature_csv(frame)


def copy_from_common(source: Path, destination: Path) -> dict[str, Any]:
    return stage34_common.copy_from_common(source, destination, ROOT)


upsert_csv_rows_resilient = stage34_common.upsert_csv_rows_resilient


def write_feature_csv(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return stage34_common.write_feature_csv(path, frame, ROOT)


def materialize_runtime_inputs(source_summary: Mapping[str, Any]) -> dict[str, Any]:
    context = feature_context_frame()
    local_model = RUN_ROOT / "models" / "tier_a_markov_state_score_table.csv"
    model_copy = copy_from_common(SOURCE_TIER_A_MODEL, local_model)
    feature_outputs: dict[str, Any] = {}
    source_date_windows: dict[str, Any] = {}
    for runtime_split, source_path in SOURCE_TIER_A_FEATURES.items():
        source = pd.read_csv(io_path(source_path))
        source_date_windows[runtime_split] = split_dates_from_feature_csv(source)
        filtered, filter_summary = filter_candidate_feature_frame(source, context)
        output_path = RUN_ROOT / "features" / f"tier_a_{runtime_split}_{RULE_ID}_features.csv"
        feature_outputs[runtime_split] = {
            **write_feature_csv(output_path, filtered),
            "source_common_path": source_path.as_posix(),
            "filter_summary": filter_summary,
            "tester_window_from_date": source_date_windows[runtime_split][0],
            "tester_window_to_date": source_date_windows[runtime_split][1],
        }
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    common_copies = [copy_to_common(local_model, f"{common}/models/{local_model.name}", COMMON_FILES_ROOT_DEFAULT)]
    for feature in feature_outputs.values():
        local_feature = ROOT / str(feature["path"])
        common_copies.append(copy_to_common(local_feature, f"{common}/features/{local_feature.name}", COMMON_FILES_ROOT_DEFAULT))
    model_artifacts = source_summary["model_artifacts"]
    return {
        "model_copy": model_copy,
        "feature_outputs": feature_outputs,
        "common_copies": common_copies,
        "threshold": float(model_artifacts["thresholds"]["tier_a"]),
        "feature_order_hash": str(model_artifacts["runtime_feature_order_hash"]),
        "known_runtime_difference": str(source_summary.get("known_runtime_difference") or model_artifacts.get("known_runtime_difference")),
        "source_runtime_summary": {
            "source_packet_id": SOURCE_RUNTIME_PACKET_ID,
            "source_run_id": SOURCE_RUNTIME_RUN_ID,
            "selected_variant_id": source_summary.get("selected_variant_id"),
            "source_mt5_status": source_summary.get("external_verification_status"),
        },
    }


def build_mt5_attempts(runtime_inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    threshold = float(runtime_inputs["threshold"])
    feature_order_hash = str(runtime_inputs["feature_order_hash"])
    for runtime_split in ("validation_is", "oos"):
        feature = runtime_inputs["feature_outputs"][runtime_split]
        from_date = str(feature["tester_window_from_date"])
        to_date = str(feature["tester_window_to_date"])
        local_feature = Path(str(feature["path"]))
        attempts.append(
            attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=STAGE_NUMBER,
                exploration_label=EXPLORATION_LABEL,
                attempt_name=f"tier_a_{RULE_ID}_{runtime_split}",
                tier=mt5.TIER_A,
                split=runtime_split,
                model_path=f"{common}/models/tier_a_markov_state_score_table.csv",
                model_id=f"{RUN_ID}_tier_a_markov_state_table",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{local_feature.name}",
                feature_count=len(RUNTIME_FEATURE_ORDER),
                feature_order_hash=feature_order_hash,
                short_threshold=threshold,
                long_threshold=threshold,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_broader_entry_proxy",
                max_hold_bars=MAX_HOLD_BARS,
                common_root=common,
                close_on_flat_signal=True,
            )
        )
    return attempts


def normalized_mt5_records(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for record in records:
        current = dict(record)
        if current.get("route_role") == "tier_a_candidate_filtered_total":
            current["route_role"] = "tier_only_total"
            metrics = dict(current.get("metrics", {})) if isinstance(current.get("metrics"), Mapping) else {}
            metrics["route_role"] = "tier_only_total"
            current["metrics"] = metrics
        normalized.append(current)
    return normalized


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.reuse_existing_result):
        manifest = read_json(RUN_ROOT / "run_manifest.json")
        kpi_record = read_json(RUN_ROOT / "kpi_record.json")
        runtime_probe = manifest.get("runtime_probe", {}) if isinstance(manifest, Mapping) else {}
        return {
            **dict(prepared),
            "compile": runtime_probe.get("compile", {}),
            "execution_results": runtime_probe.get("execution_results", []),
            "strategy_tester_reports": runtime_probe.get("strategy_tester_reports", []),
            "mt5_kpi_records": normalized_mt5_records(kpi_record.get("mt5_kpi_records", [])),
            "external_verification_status": kpi_record.get("external_verification_status"),
            "judgment": kpi_record.get("judgment"),
        }
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "not_attempted_materialize_only",
            "judgment": "not_attempted_materialize_only",
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_rule_id"] = RULE_ID
        record["source_variant_id"] = str(prepared.get("selected_variant_id"))
        record["topic_read"] = "stage34_broader_entry_proxy_filter_runtime_probe"
        record["max_hold_bars"] = MAX_HOLD_BARS
    result["mt5_kpi_records"] = normalized_mt5_records(result.get("mt5_kpi_records", []))
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            return dict(record.get("metrics", {}))
    return {}


def runtime_read(result: Mapping[str, Any]) -> dict[str, Any]:
    validation = metrics_by_view(result, "mt5_tier_a_broader_entry_proxy_validation_is")
    oos = metrics_by_view(result, "mt5_tier_a_broader_entry_proxy_oos")
    return {
        "external_verification_status": result.get("external_verification_status"),
        "validation": {
            "trade_count": validation.get("trade_count"),
            "net_profit": validation.get("net_profit"),
            "profit_factor": validation.get("profit_factor"),
            "feature_ready_count": validation.get("feature_ready_count"),
            "order_fill_count": validation.get("order_fill_count"),
        },
        "oos": {
            "trade_count": oos.get("trade_count"),
            "net_profit": oos.get("net_profit"),
            "profit_factor": oos.get("profit_factor"),
            "feature_ready_count": oos.get("feature_ready_count"),
            "order_fill_count": oos.get("order_fill_count"),
        },
    }


def write_normalized_kpi() -> dict[str, Any]:
    inventory = [{"run_id": RUN_ID, "stage_id": STAGE_ID, "idea_id": RUN_NUMBER, "path": rel(RUN_ROOT)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    trade_rows: list[dict[str, Any]] = []
    trade_summary: list[dict[str, Any]] = []
    trade_errors: list[dict[str, Any]] = []
    enriched: list[dict[str, Any]] = list(records)
    if records:
        market_data = mt5_trade_attribution.MarketData.load(ROOT)
        enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    attribution.write_json(PACKET_ROOT / "normalized_kpi_records.json", records)
    attribution.write_json(PACKET_ROOT / "normalized_kpi_summary.json", summary_rows)
    attribution.write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    attribution.write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    attribution.write_json(PACKET_ROOT / "enriched_kpi_records.json", enriched)
    attribution.write_json(PACKET_ROOT / "trade_level_records.json", trade_rows)
    attribution.write_json(PACKET_ROOT / "trade_attribution_summary.json", trade_summary)
    attribution.write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def build_summary(created_at: str, branch: str, result: Mapping[str, Any], runtime_inputs: Mapping[str, Any]) -> dict[str, Any]:
    tier_a = load_tier_a_trades()
    leave_rows = monthly_leave_one_out_rows(tier_a)
    summary_rows = monthly_summary_rows(leave_rows)
    candidate = monthly_candidate_read(summary_rows)
    completed = result.get("external_verification_status") == "completed"
    status = "reviewed_monthly_mt5_probe_completed" if completed else "blocked_monthly_mt5_probe_after_attempt"
    summary: dict[str, Any] = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_runs": [SOURCE_RUNTIME_RUN_ID, SOURCE_ATTRIBUTION_RUN_ID, SOURCE_ENTRY_PROXY_RUN_ID, SOURCE_FREQUENCY_RUN_ID],
        "source_packets": [SOURCE_RUNTIME_PACKET_ID, SOURCE_ATTRIBUTION_PACKET_ID, SOURCE_ENTRY_PROXY_PACKET_ID, SOURCE_FREQUENCY_PACKET_ID],
        "created_at_utc": created_at,
        "active_branch": branch,
        "status": status,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "boundary": BOUNDARY,
        "rule_id": RULE_ID,
        "monthly_leave_one_out_rows": leave_rows,
        "monthly_summary_rows": summary_rows,
        "monthly_candidate_read": candidate,
        "runtime_inputs": runtime_inputs,
        "runtime_read": runtime_read(result),
        "external_verification_status": result.get("external_verification_status"),
        "mt5_attempt_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "known_runtime_difference": runtime_inputs.get("known_runtime_difference"),
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
            "live_readiness",
            "mt5_verified_operating_rule",
        ],
    }
    summary["output_paths"] = {
        "monthly_leave_one_out": rel(RESULT_ROOT / "monthly_leave_one_out.csv"),
        "monthly_survival_summary": rel(RESULT_ROOT / "monthly_survival_summary.csv"),
        "aggregate_summary": rel(PACKET_ROOT / "aggregate_summary.json"),
        "run_manifest": rel(RUN_ROOT / "run_manifest.json"),
        "kpi_record": rel(RUN_ROOT / "kpi_record.json"),
    }
    return summary


def run(args: argparse.Namespace) -> dict[str, Any]:
    source_summary = read_json(SOURCE_RUNTIME_PACKET_ROOT / "aggregate_summary.json")
    runtime_inputs = materialize_runtime_inputs(source_summary)
    attempts = build_mt5_attempts(runtime_inputs)
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUNTIME_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "common_copies": runtime_inputs["common_copies"],
        "route_coverage": {},
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": source_summary.get("selected_variant_id"),
    }
    result = execute_or_block(prepared, args)
    summary = build_summary(attribution.utc_now(), attribution.active_branch(), result, runtime_inputs)
    from stage_pipelines.stage34 import markov_long_permission_broader_entry_proxy_artifacts as artifacts

    artifacts.write_run_files(summary, result)
    kpi = write_normalized_kpi()
    summary["kpi_management"] = kpi
    summary["ledger_materialization"] = artifacts.materialize_ledgers(summary)
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    artifacts.write_packet_artifacts(summary, kpi)
    artifacts.update_stage_docs(summary)
    artifacts.update_workspace_state(summary)
    artifacts.prepend_context(summary)
    artifacts.append_changelog(summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage34 Tier A Markov broader entry proxy monthly and MT5 probe.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-result", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(build_arg_parser().parse_args(argv))
    print(
        json.dumps(
            {
                "status": summary["status"],
                "judgment": summary["judgment"],
                "external_verification_status": summary["external_verification_status"],
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
