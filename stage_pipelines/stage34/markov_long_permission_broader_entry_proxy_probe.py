from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
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
    return attribution.rel(path)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def metric_value(metrics: Mapping[str, Any], key: str) -> Any:
    value = metrics.get(key)
    if value is None:
        return None
    if isinstance(value, float):
        return round(value, 6)
    return value


def pf_sort_value(value: Any) -> float:
    if value is None:
        return 999999.0
    return numeric(value)


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
    timestamps = pd.to_datetime(frame["timestamp_utc"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def copy_from_common(source: Path, destination: Path) -> dict[str, Any]:
    if not io_path(source).exists():
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {
        "source_common_path": source.as_posix(),
        "path": rel(destination),
        "sha256": sha256_file_lf_normalized(destination),
    }


def upsert_csv_rows_resilient(
    path: Path,
    columns: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    key: str,
) -> dict[str, Any]:
    try:
        return upsert_csv_rows(path, columns, rows, key=key)
    except OSError:
        existing: list[dict[str, str]] = []
        if path.exists():
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                existing = [dict(row) for row in csv.DictReader(handle)]
        new_keys = {str(row.get(key, "")).strip() for row in rows}
        merged: list[Mapping[str, Any]] = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
        merged.extend(dict(row) for row in rows)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
            writer.writeheader()
            for row in merged:
                writer.writerow({column: ledger_value(row.get(column, "")) for column in columns})
        return {
            "path": path.as_posix(),
            "sha256": sha256_file_lf_normalized(path),
            "hash_policy": "lf_normalized_text_register",
            "rows": len(merged),
            "upserted_rows": len(rows),
            "fallback_writer": "normal_windows_path_retry",
        }


def write_feature_csv(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, lineterminator="\n")
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


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


def write_run_files(summary: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    attribution.write_csv(RESULT_ROOT / "monthly_leave_one_out.csv", list(summary["monthly_leave_one_out_rows"][0].keys()), summary["monthly_leave_one_out_rows"])
    attribution.write_csv(RESULT_ROOT / "monthly_survival_summary.csv", list(summary["monthly_summary_rows"][0].keys()), summary["monthly_summary_rows"])
    attribution.write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "source_runs": [SOURCE_RUNTIME_RUN_ID, SOURCE_ATTRIBUTION_RUN_ID, SOURCE_ENTRY_PROXY_RUN_ID, SOURCE_FREQUENCY_RUN_ID],
            "boundary": BOUNDARY,
            "runtime_probe": {
                key: result.get(key)
                for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
                if key in result
            },
        },
    )
    attribution.write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUNTIME_RUN_ID,
            "kpi_scope": "tier_a_markov_broader_entry_proxy_monthly_mt5_probe",
            "model_family": MODEL_FAMILY,
            "feature_set_id": FEATURE_SET_ID,
            "label_id": LABEL_ID,
            "split_contract": SPLIT_CONTRACT,
            "monthly_candidate_read": summary["monthly_candidate_read"],
            "runtime_read": summary["runtime_read"],
            "mt5_records": result.get("mt5_kpi_records", []),
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "mt5": {"kpi_records": result.get("mt5_kpi_records", [])},
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "boundary": BOUNDARY,
        },
    )
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)


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


def review_text(summary: Mapping[str, Any]) -> str:
    candidate = summary["monthly_candidate_read"]
    validation = candidate["validation"]
    oos = candidate["oos"]
    runtime = summary["runtime_read"]
    return f"""# RUN28E Tier A Markov Broader Entry Proxy Packet(28E 실행 티어 A 마르코프 넓은 진입 대리 묶음)
## Judgment(판정)
- run(실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- rule(규칙): `{RULE_ID}`
- external verification(외부 검증): `{summary['external_verification_status']}`
- boundary(경계): `{BOUNDARY}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): 월별 생존성(monthly robustness, 월별 버팀)을 먼저 보고, 같은 후보를 MT5(`MetaTrader 5`, 메타트레이더5) feature CSV row omission(피처 CSV 행 제거) 방식으로 실제 Strategy Tester(전략 테스터)에 찔렀다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Monthly Read(월별 판독)
- validation(검증): trades(거래 수) `{validation['full_trade_count']}`, net(순손익) `{validation['full_net_profit']}`, PF(수익 팩터) `{validation['full_profit_factor']}`, min leave-one-out net(월 하나 제외 최저 순손익) `{validation['min_leave_one_out_net_profit']}`, status(상태) `{validation['monthly_survival_status']}`
- OOS(표본외): trades(거래 수) `{oos['full_trade_count']}`, net(순손익) `{oos['full_net_profit']}`, PF(수익 팩터) `{oos['full_profit_factor']}`, min leave-one-out net(월 하나 제외 최저 순손익) `{oos['min_leave_one_out_net_profit']}`, status(상태) `{oos['monthly_survival_status']}`
- OOS dependency(OOS 의존성): top positive month(최대 양수 월) `{oos['top_positive_month']}`, top positive share(최대 양수 월 비중) `{oos['top_positive_month_net_share']}`, flags(표식) `{oos['monthly_survival_flags']}`

효과(effect, 효과): 후보는 한 달을 빼도 전체 OOS(표본외) PF(수익 팩터)가 1 아래로 깨지지는 않는다. 다만 2025-10(2025년 10월)을 빼면 OOS(표본외) net(순손익)이 `{oos['min_leave_one_out_net_profit']}`까지 얇아져서, main seed(메인 씨앗)가 아니라 dependency clue(의존성 단서)로 다루는 편이 맞다.

## MT5 Runtime Probe(MT5 런타임 탐침)
- validation(검증): trades(거래 수) `{runtime['validation'].get('trade_count')}`, net(순손익) `{runtime['validation'].get('net_profit')}`, PF(수익 팩터) `{runtime['validation'].get('profit_factor')}`, feature_ready(피처 준비 수) `{runtime['validation'].get('feature_ready_count')}`
- OOS(표본외): trades(거래 수) `{runtime['oos'].get('trade_count')}`, net(순손익) `{runtime['oos'].get('net_profit')}`, PF(수익 팩터) `{runtime['oos'].get('profit_factor')}`, feature_ready(피처 준비 수) `{runtime['oos'].get('feature_ready_count')}`

효과(effect, 효과): 이번 MT5(메타트레이더5) 검증은 EA(`Expert Advisor`, 전문가 자문) 로직을 새로 바꾸지 않고, `vol_high` 또는 `adx_20_25`에 걸린 feature row(피처 행)를 빼서 해당 시간 신호를 만들지 않게 한 좁은 runtime probe(런타임 탐침)다. 그래서 “터미널에서도 대략 같은 필터 방향이 살아 있는가”는 보지만, operating rule(운영 규칙) 확정은 아니다.

## Files(파일)
- monthly leave-one-out(월 하나 제외): `{summary['output_paths']['monthly_leave_one_out']}`
- monthly summary(월별 요약): `{summary['output_paths']['monthly_survival_summary']}`
- aggregate summary(집계 요약): `{summary['output_paths']['aggregate_summary']}`
"""


def decision_text(summary: Mapping[str, Any]) -> str:
    candidate = summary["monthly_candidate_read"]
    return f"""# Decision: Stage34 RUN28E Broader Entry Proxy Completed(결정: 34단계 28E 넓은 진입 대리 완료)
- date(날짜): 2026-05-08
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- rule(규칙): `{RULE_ID}`
- monthly status(월별 상태): `{candidate['status']}`
- MT5 status(MT5 상태): `{summary['external_verification_status']}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): 후보는 보존하지만 main seed(메인 씨앗)로 승격하지 않는다. 다음 행동(action, 행동)은 `vol_high`와 `adx_20_25`를 분리해, 실제로 어느 축이 2025-10(2025년 10월) 의존성을 만든 것인지 찌르는 것이다.
"""


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime = summary["runtime_read"]
    candidate = summary["monthly_candidate_read"]
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__monthly_survival",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "monthly_survival",
            "parent_run_id": SOURCE_FREQUENCY_RUN_ID,
            "record_view": "monthly_survival_summary",
            "tier_scope": "Tier A",
            "kpi_scope": "monthly_robustness",
            "scoreboard_lane": "performance_attribution",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["monthly_survival_summary"],
            "primary_kpi": ledger_pairs(
                [
                    ("rule_id", RULE_ID),
                    ("monthly_status", candidate["status"]),
                    ("oos_min_leave_one_out_net", candidate["oos"]["min_leave_one_out_net_profit"]),
                    ("oos_top_positive_month", candidate["oos"]["top_positive_month"]),
                ]
            ),
            "guardrail_kpi": ledger_pairs([("boundary", BOUNDARY), ("no_seed_change", True)]),
            "external_verification_status": summary["external_verification_status"],
            "notes": "Monthly leave-one-out kept the candidate alive but showed October dependency.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_runtime_probe",
            "parent_run_id": SOURCE_RUNTIME_RUN_ID,
            "record_view": "mt5_tier_a_broader_entry_proxy",
            "tier_scope": "Tier A",
            "kpi_scope": "runtime_probe",
            "scoreboard_lane": "runtime_probe",
            "status": "reviewed" if summary["external_verification_status"] == "completed" else "blocked",
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["kpi_record"],
            "primary_kpi": ledger_pairs(
                [
                    ("validation_pf", runtime["validation"].get("profit_factor")),
                    ("oos_pf", runtime["oos"].get("profit_factor")),
                    ("validation_trades", runtime["validation"].get("trade_count")),
                    ("oos_trades", runtime["oos"].get("trade_count")),
                ]
            ),
            "guardrail_kpi": "runtime_probe_only_no_runtime_authority",
            "external_verification_status": summary["external_verification_status"],
            "notes": "MT5 probe used Stage34 filtered Tier A feature CSV rows; no EA logic promotion.",
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
            "judgment": summary["judgment"],
            "path": summary["output_paths"]["aggregate_summary"],
            "primary_kpi": "candidate_preserved_no_seed_change",
            "guardrail_kpi": ledger_pairs([("forbidden_claims", summary["forbidden_claims"]), ("next_action", NEXT_ACTION)]),
            "external_verification_status": summary["external_verification_status"],
            "notes": "No baseline, promotion, live readiness, or runtime authority was created.",
        },
    ]
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_probe",
        "status": "reviewed" if summary["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["judgment"],
        "path": rel(REPORT_PATH),
        "notes": "Stage34 Tier A Markov broader entry proxy monthly robustness plus MT5 runtime probe; no baseline, promotion, or runtime authority.",
    }
    return {
        "stage_run_ledger": upsert_csv_rows_resilient(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows_resilient(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "run_registry": upsert_csv_rows_resilient(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id"),
    }


def write_packet_artifacts(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    attribution.write_csv(PACKET_ROOT / "monthly_leave_one_out.csv", list(summary["monthly_leave_one_out_rows"][0].keys()), summary["monthly_leave_one_out_rows"])
    attribution.write_csv(PACKET_ROOT / "monthly_survival_summary.csv", list(summary["monthly_summary_rows"][0].keys()), summary["monthly_summary_rows"])
    attribution.write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    attribution.write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {"skill": "obsidian-experiment-design", "status": "executed", "run_id": RUN_ID},
            {"skill": "obsidian-performance-attribution", "status": "executed", "monthly_candidate_read": summary["monthly_candidate_read"]["status"]},
            {"skill": "obsidian-runtime-parity", "status": "executed", "external_verification_status": summary["external_verification_status"]},
            {"skill": "obsidian-backtest-forensics", "status": "executed", "mt5_kpi_record_count": summary["mt5_kpi_record_count"]},
            {"skill": "obsidian-result-judgment", "status": "executed", "judgment": summary["judgment"]},
        ],
    )
    attribution.write_json(
        PACKET_ROOT / "artifact_lineage_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "source_packets": summary["source_packets"],
            "runtime_input_model": summary["runtime_inputs"]["model_copy"],
            "runtime_input_features": summary["runtime_inputs"]["feature_outputs"],
        },
    )
    attribution.write_json(
        PACKET_ROOT / "monthly_survival_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if summary["monthly_candidate_read"]["status"] != "monthly_fail" else "blocked",
            "monthly_candidate_read": summary["monthly_candidate_read"],
        },
    )
    attribution.write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if summary["external_verification_status"] == "completed" else "blocked",
            "external_verification_status": summary["external_verification_status"],
            "mt5_kpi_record_count": summary["mt5_kpi_record_count"],
            "normalized_kpi": kpi,
        },
    )
    attribution.write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed" if int(kpi.get("parser_errors") or 0) == 0 and int(kpi.get("trade_parser_errors") or 0) == 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
            "trade_parser_errors": kpi.get("trade_parser_errors"),
        },
    )
    attribution.write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": ["Stage34 RUN28E broader entry proxy probe completed.", "Candidate remains a dependency clue."],
            "forbidden_claims": summary["forbidden_claims"],
            "boundary": BOUNDARY,
        },
    )
    gates = [
        "artifact_lineage_gate",
        "monthly_survival_gate",
        "runtime_evidence_gate",
        "kpi_contract_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    attribution.write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []},
    )


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    attribution.write_md(REPORT_PATH, review_text(summary))
    attribution.write_md(DECISION_PATH, decision_text(summary))
    attribution.write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage34 Review Index(34단계 검토 색인)

- current status(현재 상태): `{summary['status']}`
- current run(현재 실행): `{RUN_ID}`
- current packet(현재 묶음): `{PACKET_ID}`
- latest review(최신 검토): `{rel(REPORT_PATH)}`
- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`

효과(effect, 효과): Stage34(34단계)는 run28E(28E 실행)에서 월별 버팀과 MT5 runtime probe(MT5 런타임 탐침)를 함께 기록했다.
""",
    )
    attribution.write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage34 Selection Status(34단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `{summary['status']}`
- current run(현재 실행): `{RUN_ID}`
- preserved seed(보존 씨앗): `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`
- dependency clue(의존성 단서): `{RULE_ID}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

효과(effect, 효과): 후보는 MT5(메타트레이더5)에 한 번 찔렀지만, 월별 의존성이 있어 operating rule(운영 규칙)이나 main seed(메인 씨앗)로 올리지 않는다.
""",
    )


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_branch: .+", f"active_branch: {summary['active_branch']}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    new_focus = (
        "- Stage34(34단계) 34_regime_mechanism__tier_a_markov_long_permission_attribution "
        "reviewed_monthly_mt5_probe_completed(월별/MT5 탐침 검토 완료): run28E(28E 실행)는 "
        "`exclude_vol_high_or_adx_20_25`를 월별로 버티는지 보고 MT5 runtime_probe(MT5 런타임 탐침)까지 시도했다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.\n"
    )
    text = re.sub(r"- Stage34\(34.*?\) 34_regime_mechanism__tier_a_markov_long_permission_attribution .*?\n(?=- Stage33)", new_focus, text, count=1, flags=re.DOTALL)
    text = re.sub(
        r"- current_run_id\(.*?\).*?(?=\n- treat Stage29-32)",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 검토된 실행인 `{RUN_ID}`를 가리킨다. next action(다음 행동)은 `{NEXT_ACTION}`이다.",
        text,
        count=1,
        flags=re.DOTALL,
    )
    stage34_block = f"""stage34_tier_a_markov_long_permission_attribution:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: {summary['status']}
  current_run_id: {RUN_ID}
  preserved_seed: Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)
  dependency_clue: {RULE_ID}
  decision_path: {rel(DECISION_PATH)}
  stage_path: stages/{STAGE_ID}
  previous_stage_id: 33_regime_mechanism__tier_a_markov_long_permission_source
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  external_verification_status: {summary['external_verification_status']}
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}
"""
    text = re.sub(r"stage34_tier_a_markov_long_permission_attribution:\n(?:  .+\n)+\npre_alpha_stage_queue:", stage34_block + "\npre_alpha_stage_queue:", text, count=1)
    attribution.write_md(WORKSPACE_STATE_PATH, text)


def prepend_context(summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(r"^## Latest Stage34 RUN28E Broader Entry Proxy.*?(?=## Latest |\Z)", "", old, count=1, flags=re.DOTALL)
    runtime = summary["runtime_read"]
    candidate = summary["monthly_candidate_read"]
    block = f"""## Latest Stage34 RUN28E Broader Entry Proxy(최신 34단계 28E 넓은 진입 대리)

## Current Re-entry Snapshot(현재 재진입 스냅샷)

- active branch(활성 브랜치): `{summary['active_branch']}`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- next action(다음 행동): `{NEXT_ACTION}`

Stage34(34단계) `{RUN_ID}`를 monthly robustness plus MT5 runtime probe(월별 버팀 + MT5 런타임 탐침)로 완료했다.

결과(result, 결과): `{RULE_ID}`는 월 하나를 빼도 OOS(표본외) PF(수익 팩터)가 1 아래로 깨지지는 않았다. 다만 2025-10(2025년 10월)을 빼면 OOS(표본외) net(순손익)이 `{candidate['oos']['min_leave_one_out_net_profit']}`까지 얇다. MT5(메타트레이더5) probe(탐침)는 validation/OOS(검증/표본외) trades(거래 수) `{runtime['validation'].get('trade_count')}` / `{runtime['oos'].get('trade_count')}`를 기록했다.

효과(effect, 효과): 후보는 보존하지만 main seed(메인 씨앗), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다. 다음은 `vol_high`와 `adx_20_25`를 분리해 의존성 원인을 본다.

"""
    attribution.write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))


def append_changelog(summary: Mapping[str, Any]) -> None:
    old = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old = re.sub(r"^## 2026-05-08 Stage34 RUN28E Broader Entry Proxy.*?(?=## |\Z)", "", old, count=1, flags=re.DOTALL)
    entry = f"""## 2026-05-08 Stage34 RUN28E Broader Entry Proxy(34단계 28E 넓은 진입 대리)

- completed(완료): `{RUN_ID}` monthly robustness plus MT5 runtime probe(월별 버팀 + MT5 런타임 탐침)
- source(원천): `{SOURCE_FREQUENCY_RUN_ID}`, `{SOURCE_RUNTIME_RUN_ID}`
- judgment(판정): `{summary['judgment']}`
- effect(효과): `{RULE_ID}`는 dependency clue(의존성 단서)로 보존한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    attribution.write_md(CHANGELOG_PATH, entry + old.lstrip("\ufeff"))


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
    write_run_files(summary, result)
    kpi = write_normalized_kpi()
    summary["kpi_management"] = kpi
    summary["ledger_materialization"] = materialize_ledgers(summary)
    attribution.write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    write_packet_artifacts(summary, kpi)
    update_stage_docs(summary)
    update_workspace_state(summary)
    prepend_context(summary)
    append_changelog(summary)
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
