from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
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
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage34 import common as stage34_common
from stage_pipelines.stage34 import markov_long_permission_attribution as attribution
from stage_pipelines.stage34 import markov_long_permission_broader_entry_proxy_probe as run28e
from stage_pipelines.stage34 import markov_long_permission_entry_time_hold_proxy_probe as entry_proxy
from stage_pipelines.stage34 import markov_long_permission_frequency_floor_probe as frequency_floor


STAGE_NUMBER = 34
STAGE_ID = attribution.STAGE_ID
RUN_ID = "run28F_tier_a_markov_vol_adx_component_dependency_probe_v1"
RUN_NUMBER = "run28F"
PACKET_ID = "stage34_run28F_tier_a_markov_vol_adx_component_dependency_probe_v1"
SOURCE_RUNTIME_RUN_ID = attribution.SOURCE_RUN_ID
SOURCE_RUNTIME_PACKET_ID = attribution.SOURCE_PACKET_ID
SOURCE_ATTRIBUTION_RUN_ID = attribution.RUN_ID
SOURCE_ATTRIBUTION_PACKET_ID = attribution.PACKET_ID
SOURCE_RUN28E_ID = run28e.RUN_ID
SOURCE_RUN28E_PACKET_ID = run28e.PACKET_ID
EXPLORATION_LABEL = "stage34_RegimeMechanism__TierAMarkovVolAdxDependencyProbe"
MODEL_FAMILY = "markov_regression_state_score_table_runtime_probe"
MODEL_BACKEND = "ebm_table"
FEATURE_SET_ID = "feature_set_v2_markov_state_runtime_features_stage34_vol_adx_components"
LABEL_ID = run28e.LABEL_ID
SPLIT_CONTRACT = run28e.SPLIT_CONTRACT
BOUNDARY = "stage34_vol_adx_dependency_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_tier_a_markov_vol_adx_dependency_probe_completed"
JUDGMENT_BLOCKED = "blocked_tier_a_markov_vol_adx_dependency_probe_after_attempt"
NEXT_ACTION = "run28G_tier_a_markov_hold_management_runtime_probe_v1"

ROOT = attribution.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
SOURCE_RUNTIME_PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / SOURCE_RUNTIME_PACKET_ID
SOURCE_RUN28E_PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / SOURCE_RUN28E_PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run28F_tier_a_markov_vol_adx_dependency_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-08_stage34_run28F_tier_a_markov_vol_adx_dependency.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs" / "registers" / "run_registry.csv"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews" / "review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
WORKSPACE_STATE_PATH = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = ROOT / "docs" / "workspace" / "changelog.md"

RUNTIME_FEATURE_ORDER = run28e.RUNTIME_FEATURE_ORDER
SOURCE_TIER_A_MODEL = run28e.SOURCE_TIER_A_MODEL
SOURCE_TIER_A_FEATURES = run28e.SOURCE_TIER_A_FEATURES
MAX_HOLD_BARS = run28e.MAX_HOLD_BARS
MIN_MARGIN = run28e.MIN_MARGIN
UNION_RULE_ID = "exclude_vol_high_or_adx_20_25"
COMPONENT_RULE_IDS = (
    "baseline_all_trades",
    "exclude_vol_high",
    "exclude_adx_20_25",
    "exclude_vol_high_and_adx_20_25",
    UNION_RULE_ID,
)
MT5_COMPONENT_RULE_IDS = (
    "exclude_vol_high",
    "exclude_adx_20_25",
    "exclude_vol_high_and_adx_20_25",
)


def rel(path: Path) -> str:
    return stage34_common.rel(path, ROOT)


read_json = stage34_common.read_json
write_json = stage34_common.write_json
numeric = stage34_common.numeric
metric_value = stage34_common.metric_value


def component_rule_mask(rule_id: str, frame: pd.DataFrame) -> pd.Series:
    if rule_id == "baseline_all_trades":
        return pd.Series(True, index=frame.index)
    if rule_id == "exclude_vol_high_and_adx_20_25":
        return ~(frame["volatility_regime"].eq("vol_high") & frame["adx_bucket"].eq("adx_20_25"))
    return entry_proxy.rule_mask(rule_id, frame)


def component_allowed_mask(rule_id: str, frame: pd.DataFrame) -> pd.Series:
    vol_high = frame["volatility_regime"].eq("vol_high")
    adx_mid = frame["adx_bucket"].eq("adx_20_25")
    if rule_id == "exclude_vol_high":
        return ~vol_high
    if rule_id == "exclude_adx_20_25":
        return ~adx_mid
    if rule_id == "exclude_vol_high_and_adx_20_25":
        return ~(vol_high & adx_mid)
    if rule_id == UNION_RULE_ID:
        return ~(vol_high | adx_mid)
    if rule_id == "baseline_all_trades":
        return pd.Series(True, index=frame.index)
    raise KeyError(f"unknown component rule: {rule_id}")


def removal_reason(frame: pd.DataFrame) -> pd.Series:
    vol_high = frame["volatility_regime"].eq("vol_high")
    adx_mid = frame["adx_bucket"].eq("adx_20_25")
    return pd.Series(
        np.select(
            [vol_high & adx_mid, vol_high, adx_mid],
            ["both_vol_high_and_adx_20_25", "vol_high_only", "adx_20_25_only"],
            default="kept_context",
        ),
        index=frame.index,
    )


def load_tier_a_trades() -> pd.DataFrame:
    frame = frequency_floor.load_tier_a_trades()
    frame["month"] = frame["open_time_dt"].dt.to_period("M").astype(str)
    return frame


def component_python_rows(tier_a: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, split_frame in tier_a.groupby("matched_split", dropna=False):
        split_name = str(split)
        baseline = attribution.profit_metrics(split_frame)
        for rule_id in COMPONENT_RULE_IDS:
            mask = component_rule_mask(rule_id, split_frame)
            kept = split_frame.loc[mask].copy()
            removed = split_frame.loc[~mask].copy()
            kept_metrics = attribution.profit_metrics(kept)
            removed_metrics = attribution.profit_metrics(removed)
            rows.append(
                {
                    "rule_id": rule_id,
                    "split": split_name,
                    "kept_trade_count": metric_value(kept_metrics, "trade_count"),
                    "kept_net_profit": metric_value(kept_metrics, "net_profit"),
                    "kept_profit_factor": metric_value(kept_metrics, "profit_factor"),
                    "kept_expectancy": metric_value(kept_metrics, "expectancy"),
                    "kept_win_rate_percent": metric_value(kept_metrics, "win_rate_percent"),
                    "removed_trade_count": metric_value(removed_metrics, "trade_count"),
                    "removed_net_profit": metric_value(removed_metrics, "net_profit"),
                    "removed_profit_factor": metric_value(removed_metrics, "profit_factor"),
                    "net_delta_vs_baseline": round(numeric(kept_metrics.get("net_profit")) - numeric(baseline.get("net_profit")), 6),
                    "pf_delta_vs_baseline": None
                    if kept_metrics.get("profit_factor") is None or baseline.get("profit_factor") is None
                    else round(numeric(kept_metrics.get("profit_factor")) - numeric(baseline.get("profit_factor")), 6),
                    "trade_delta_vs_baseline": int(metric_value(kept_metrics, "trade_count")) - int(metric_value(baseline, "trade_count")),
                }
            )
    return sorted(rows, key=lambda row: (row["rule_id"], row["split"]))


def component_driver_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_key = {(str(row["rule_id"]), str(row["split"])): row for row in rows}
    read: dict[str, Any] = {}
    for split in ("validation", "oos"):
        candidates = [by_key[(rule_id, split)] for rule_id in COMPONENT_RULE_IDS if rule_id != "baseline_all_trades"]
        best_pf = max(candidates, key=lambda row: numeric(row["kept_profit_factor"], -999.0))
        best_net = max(candidates, key=lambda row: numeric(row["kept_net_profit"], -999999.0))
        read[split] = {
            "baseline": by_key[("baseline_all_trades", split)],
            "best_profit_factor_rule": best_pf["rule_id"],
            "best_profit_factor": best_pf["kept_profit_factor"],
            "best_net_rule": best_net["rule_id"],
            "best_net_profit": best_net["kept_net_profit"],
            "exclude_vol_high": by_key[("exclude_vol_high", split)],
            "exclude_adx_20_25": by_key[("exclude_adx_20_25", split)],
            "exclude_overlap_only": by_key[("exclude_vol_high_and_adx_20_25", split)],
            "exclude_union": by_key[(UNION_RULE_ID, split)],
        }
    read["interpretation"] = (
        "validation(검증)은 ADX 20-25 제거가 더 강하고, OOS(표본외)는 vol_high 제거가 net(순손익)을 더 살린다. "
        "union(합집합) 필터는 PF(수익 팩터)는 좋지만 2025-10(2025년 10월) 의존성이 남는다."
    )
    return read


def feature_context_frame() -> pd.DataFrame:
    context = run28e.feature_context_frame().copy()
    return context[["bar_time_server", "volatility_regime", "adx_bucket"]].drop_duplicates("bar_time_server", keep="last")


def score_feature_frame(frame: pd.DataFrame, table_path: Path, threshold: float) -> pd.DataFrame:
    out = frame.copy()
    values = out.loc[:, list(RUNTIME_FEATURE_ORDER)].to_numpy(dtype="float64", copy=False)
    probs = score_ebm_table_probabilities(load_ebm_score_table(table_path, feature_count=len(RUNTIME_FEATURE_ORDER)), values)
    out["p_short"] = probs[:, 0]
    out["p_flat"] = probs[:, 1]
    out["p_long"] = probs[:, 2]
    sorted_prob = np.sort(probs, axis=1)
    out["probability_margin"] = sorted_prob[:, -1] - sorted_prob[:, -2]
    out["long_signal"] = out["p_long"].ge(float(threshold))
    return out


def merge_feature_context(source: pd.DataFrame, context: pd.DataFrame, table_path: Path, threshold: float) -> pd.DataFrame:
    scored = score_feature_frame(source, table_path, threshold)
    merged = scored.merge(context, on="bar_time_server", how="left")
    merged["volatility_regime"] = merged["volatility_regime"].fillna("missing_context")
    merged["adx_bucket"] = merged["adx_bucket"].fillna("missing_context")
    merged["removal_reason"] = removal_reason(merged)
    merged["month"] = pd.to_datetime(merged["bar_time_server"].str.replace(".", "-", regex=False)).dt.to_period("M").astype(str)
    return merged


def feature_filter_frame(source: pd.DataFrame, context: pd.DataFrame, rule_id: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    original_columns = list(source.columns)
    merged = source.merge(context, on="bar_time_server", how="left")
    missing = merged["volatility_regime"].isna() | merged["adx_bucket"].isna()
    merged["volatility_regime"] = merged["volatility_regime"].fillna("missing_context")
    merged["adx_bucket"] = merged["adx_bucket"].fillna("missing_context")
    allowed = component_allowed_mask(rule_id, merged) | missing
    kept = merged.loc[allowed, original_columns].copy()
    removed = merged.loc[~allowed].copy()
    reason_counts = removed.assign(removal_reason=removal_reason(removed)).groupby("removal_reason").size().to_dict()
    return kept, {
        "rule_id": rule_id,
        "source_rows": int(len(source)),
        "kept_rows": int(len(kept)),
        "filtered_rows": int(len(removed)),
        "missing_context_rows_kept": int(missing.sum()),
        "removed_reason_counts": {str(key): int(value) for key, value in reason_counts.items()},
    }


def feature_ready_summary_rows(features_by_split: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for runtime_split, frame in features_by_split.items():
        for rule_id in COMPONENT_RULE_IDS:
            allowed = component_allowed_mask(rule_id, frame)
            for group_name, subset in (("kept", frame.loc[allowed]), ("removed", frame.loc[~allowed])):
                if subset.empty:
                    rows.append(
                        {
                            "rule_id": rule_id,
                            "runtime_split": runtime_split,
                            "group": group_name,
                            "removal_reason": "none",
                            "row_count": 0,
                            "long_signal_count": 0,
                            "avg_p_long": 0.0,
                            "top_month": "none",
                        }
                    )
                    continue
                grouped = subset.groupby("removal_reason") if group_name == "removed" else [("kept_by_rule", subset)]
                for reason, reason_frame in grouped:
                    by_month = reason_frame.groupby("month").size().sort_values(ascending=False)
                    rows.append(
                        {
                            "rule_id": rule_id,
                            "runtime_split": runtime_split,
                            "group": group_name,
                            "removal_reason": str(reason),
                            "row_count": int(len(reason_frame)),
                            "long_signal_count": int(reason_frame["long_signal"].sum()),
                            "long_signal_share": round(float(reason_frame["long_signal"].mean()), 6),
                            "avg_p_long": round(float(reason_frame["p_long"].mean()), 6),
                            "top_month": str(by_month.index[0]) if len(by_month) else "none",
                            "top_month_rows": int(by_month.iloc[0]) if len(by_month) else 0,
                        }
                    )
    return sorted(rows, key=lambda row: (row["rule_id"], row["runtime_split"], row["group"], row["removal_reason"]))


def feature_ready_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    def row(rule_id: str, runtime_split: str, group: str, reason: str) -> Mapping[str, Any]:
        return next(
            item
            for item in rows
            if item["rule_id"] == rule_id and item["runtime_split"] == runtime_split and item["group"] == group and item["removal_reason"] == reason
        )

    return {
        "validation_union_kept_rows": row(UNION_RULE_ID, "validation_is", "kept", "kept_by_rule")["row_count"],
        "oos_union_kept_rows": row(UNION_RULE_ID, "oos", "kept", "kept_by_rule")["row_count"],
        "validation_union_removed_long_signals": sum(
            int(item["long_signal_count"])
            for item in rows
            if item["rule_id"] == UNION_RULE_ID and item["runtime_split"] == "validation_is" and item["group"] == "removed"
        ),
        "oos_union_removed_long_signals": sum(
            int(item["long_signal_count"])
            for item in rows
            if item["rule_id"] == UNION_RULE_ID and item["runtime_split"] == "oos" and item["group"] == "removed"
        ),
        "read": "feature_ready 감소는 대부분 vol_high 제거에서 오고, 일부는 adx_20_25 제거와 overlap(겹침)에서 온다.",
    }


def write_feature_csv(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return stage34_common.write_feature_csv(path, frame, ROOT)


def split_dates_from_feature_csv(frame: pd.DataFrame) -> tuple[str, str]:
    return stage34_common.split_dates_from_feature_csv(frame)


def materialize_runtime_inputs(source_summary: Mapping[str, Any]) -> dict[str, Any]:
    context = feature_context_frame()
    local_model = RUN_ROOT / "models" / "tier_a_markov_state_score_table.csv"
    model_copy = run28e.copy_from_common(SOURCE_TIER_A_MODEL, local_model)
    model_artifacts = source_summary["model_artifacts"]
    threshold = float(model_artifacts["thresholds"]["tier_a"])
    features_by_split: dict[str, pd.DataFrame] = {}
    feature_outputs: dict[str, dict[str, Any]] = {}
    for runtime_split, source_path in SOURCE_TIER_A_FEATURES.items():
        source = pd.read_csv(io_path(source_path))
        features_by_split[runtime_split] = merge_feature_context(source, context, local_model, threshold)
        from_date, to_date = split_dates_from_feature_csv(source)
        feature_outputs[runtime_split] = {}
        for rule_id in MT5_COMPONENT_RULE_IDS:
            filtered, filter_summary = feature_filter_frame(source, context, rule_id)
            output = RUN_ROOT / "features" / f"tier_a_{runtime_split}_{rule_id}_features.csv"
            feature_outputs[runtime_split][rule_id] = {
                **write_feature_csv(output, filtered),
                "source_common_path": source_path.as_posix(),
                "filter_summary": filter_summary,
                "tester_window_from_date": from_date,
                "tester_window_to_date": to_date,
            }
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    common_copies = [copy_to_common(local_model, f"{common}/models/{local_model.name}", COMMON_FILES_ROOT_DEFAULT)]
    for split_outputs in feature_outputs.values():
        for feature in split_outputs.values():
            local_feature = ROOT / str(feature["path"])
            common_copies.append(copy_to_common(local_feature, f"{common}/features/{local_feature.name}", COMMON_FILES_ROOT_DEFAULT))
    return {
        "model_copy": model_copy,
        "feature_outputs": feature_outputs,
        "common_copies": common_copies,
        "threshold": threshold,
        "feature_order_hash": str(model_artifacts["runtime_feature_order_hash"]),
        "known_runtime_difference": str(source_summary.get("known_runtime_difference") or model_artifacts.get("known_runtime_difference")),
        "source_runtime_summary": {
            "source_packet_id": SOURCE_RUNTIME_PACKET_ID,
            "source_run_id": SOURCE_RUNTIME_RUN_ID,
            "selected_variant_id": source_summary.get("selected_variant_id"),
            "source_mt5_status": source_summary.get("external_verification_status"),
        },
        "features_by_split": features_by_split,
    }


def build_mt5_attempts(runtime_inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    threshold = float(runtime_inputs["threshold"])
    feature_order_hash = str(runtime_inputs["feature_order_hash"])
    for runtime_split in ("validation_is", "oos"):
        for rule_id in MT5_COMPONENT_RULE_IDS:
            feature = runtime_inputs["feature_outputs"][runtime_split][rule_id]
            local_feature = Path(str(feature["path"]))
            attempts.append(
                attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=STAGE_NUMBER,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"tier_a_{rule_id}_{runtime_split}",
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
                    from_date=str(feature["tester_window_from_date"]),
                    to_date=str(feature["tester_window_to_date"]),
                    primary_active_tier="tier_a",
                    attempt_role="tier_only_total",
                    record_view_prefix=f"mt5_tier_a_component_{rule_id}",
                    max_hold_bars=MAX_HOLD_BARS,
                    common_root=common,
                    close_on_flat_signal=True,
                )
            )
    return attempts


def rule_from_record_view(record_view: str) -> str:
    for rule_id in sorted(MT5_COMPONENT_RULE_IDS, key=len, reverse=True):
        if rule_id in record_view:
            return rule_id
    if "broader_entry_proxy" in record_view:
        return UNION_RULE_ID
    return "unknown"


def normalized_mt5_records(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for record in records:
        current = dict(record)
        current["source_rule_id"] = rule_from_record_view(str(current.get("record_view", "")))
        current["source_variant_id"] = "v01_return_2state_switchvar"
        current["topic_read"] = "stage34_vol_adx_component_dependency_probe"
        current["max_hold_bars"] = MAX_HOLD_BARS
        metrics = dict(current.get("metrics", {})) if isinstance(current.get("metrics"), Mapping) else {}
        metrics["route_role"] = "tier_only_total"
        current["route_role"] = "tier_only_total"
        current["metrics"] = metrics
        out.append(current)
    return out


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
    result["mt5_kpi_records"] = normalized_mt5_records(result.get("mt5_kpi_records", []))
    return result


def mt5_component_rows(result: Mapping[str, Any], union_records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, records in (("run28F_component_mt5", result.get("mt5_kpi_records", [])), ("run28E_union_mt5", union_records)):
        for record in records:
            metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
            rows.append(
                {
                    "source": source,
                    "rule_id": record.get("source_rule_id") or rule_from_record_view(str(record.get("record_view", ""))),
                    "record_view": record.get("record_view"),
                    "split": record.get("split"),
                    "trade_count": metrics.get("trade_count"),
                    "net_profit": metrics.get("net_profit"),
                    "profit_factor": metrics.get("profit_factor"),
                    "max_drawdown_amount": metrics.get("max_drawdown_amount"),
                    "feature_ready_count": metrics.get("feature_ready_count"),
                    "model_ok_count": metrics.get("model_ok_count"),
                    "order_fill_count": metrics.get("order_fill_count"),
                    "status": record.get("status"),
                }
            )
    return sorted(rows, key=lambda row: (str(row["rule_id"]), str(row["split"]), str(row["source"])))


def mt5_component_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    read: dict[str, Any] = {}
    for split in ("validation_is", "oos"):
        split_rows = [row for row in rows if str(row["split"]) == split]
        best_pf = max(split_rows, key=lambda row: numeric(row["profit_factor"], -999.0)) if split_rows else {}
        best_net = max(split_rows, key=lambda row: numeric(row["net_profit"], -999999.0)) if split_rows else {}
        read[split] = {
            "best_profit_factor_rule": best_pf.get("rule_id"),
            "best_profit_factor": best_pf.get("profit_factor"),
            "best_net_rule": best_net.get("rule_id"),
            "best_net_profit": best_net.get("net_profit"),
            "rows": split_rows,
        }
    return read


def monthly_dependency_rows(tier_a: pd.DataFrame, run28e_trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    python_union = tier_a.loc[component_rule_mask(UNION_RULE_ID, tier_a)].copy()
    sources = [("python_union", python_union, "matched_split")]
    if not run28e_trades.empty:
        mt5_frame = run28e_trades.copy()
        mt5_frame["month"] = pd.to_datetime(mt5_frame["open_time"]).dt.to_period("M").astype(str)
        sources.append(("mt5_union_run28E", mt5_frame, "split"))
    for source, frame, split_column in sources:
        for split, split_frame in frame.groupby(split_column, dropna=False):
            full = attribution.profit_metrics(split_frame)
            for month, month_frame in split_frame.groupby("month", dropna=False):
                month_metrics = attribution.profit_metrics(month_frame)
                without = split_frame.loc[~split_frame["month"].eq(month)].copy()
                without_metrics = attribution.profit_metrics(without)
                rows.append(
                    {
                        "source": source,
                        "split": str(split),
                        "month": str(month),
                        "full_trade_count": metric_value(full, "trade_count"),
                        "full_net_profit": metric_value(full, "net_profit"),
                        "full_profit_factor": metric_value(full, "profit_factor"),
                        "month_trade_count": metric_value(month_metrics, "trade_count"),
                        "month_net_profit": metric_value(month_metrics, "net_profit"),
                        "month_profit_factor": metric_value(month_metrics, "profit_factor"),
                        "month_net_share": None
                        if abs(numeric(full.get("net_profit"))) < 1e-9
                        else round(numeric(month_metrics.get("net_profit")) / numeric(full.get("net_profit")), 6),
                        "without_month_trade_count": metric_value(without_metrics, "trade_count"),
                        "without_month_net_profit": metric_value(without_metrics, "net_profit"),
                        "without_month_profit_factor": metric_value(without_metrics, "profit_factor"),
                    }
                )
    return sorted(rows, key=lambda row: (row["source"], row["split"], row["month"]))


def october_dependency_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    key_rows = [row for row in rows if row["month"] == "2025-10" and row["split"] in {"oos", "oos"}]
    read = {row["source"]: row for row in key_rows}
    return {
        "python_without_2025_10_net": read.get("python_union", {}).get("without_month_net_profit"),
        "python_without_2025_10_pf": read.get("python_union", {}).get("without_month_profit_factor"),
        "mt5_without_2025_10_net": read.get("mt5_union_run28E", {}).get("without_month_net_profit"),
        "mt5_without_2025_10_pf": read.get("mt5_union_run28E", {}).get("without_month_profit_factor"),
        "read": "2025-10(2025년 10월)을 빼도 MT5(메타트레이더5)는 남지만, Python(파이썬) matched trade(매칭 거래)는 거의 평평해진다.",
    }


def hold_duration_rows(run28e_trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if run28e_trades.empty:
        return rows
    frame = run28e_trades.copy()
    frame["hold_bars"] = pd.to_numeric(frame["hold_bars"], errors="coerce")
    for split, split_frame in frame.groupby("split", dropna=False):
        hold = split_frame["hold_bars"].dropna()
        metrics = attribution.profit_metrics(split_frame)
        long_hold = split_frame.loc[split_frame["hold_bars"].gt(96)].copy()
        long_metrics = attribution.profit_metrics(long_hold)
        rows.append(
            {
                "source": "mt5_union_run28E",
                "split": str(split),
                "trade_count": metric_value(metrics, "trade_count"),
                "net_profit": metric_value(metrics, "net_profit"),
                "profit_factor": metric_value(metrics, "profit_factor"),
                "max_hold_config_bars": MAX_HOLD_BARS,
                "avg_hold_bars": round(float(hold.mean()), 6) if len(hold) else 0.0,
                "median_hold_bars": round(float(hold.median()), 6) if len(hold) else 0.0,
                "p75_hold_bars": round(float(hold.quantile(0.75)), 6) if len(hold) else 0.0,
                "p90_hold_bars": round(float(hold.quantile(0.90)), 6) if len(hold) else 0.0,
                "max_hold_bars": round(float(hold.max()), 6) if len(hold) else 0.0,
                "gt_12_count": int(hold.gt(12).sum()),
                "gt_96_count": int(hold.gt(96).sum()),
                "gt_288_count": int(hold.gt(288).sum()),
                "gt_96_net_profit": metric_value(long_metrics, "net_profit"),
                "gt_96_profit_factor": metric_value(long_metrics, "profit_factor"),
            }
        )
    return rows


def hold_duration_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_split = {str(row["split"]): row for row in rows}
    return {
        "validation_avg_hold_bars": by_split.get("validation", {}).get("avg_hold_bars"),
        "oos_avg_hold_bars": by_split.get("oos", {}).get("avg_hold_bars"),
        "validation_gt_96_count": by_split.get("validation", {}).get("gt_96_count"),
        "oos_gt_96_count": by_split.get("oos", {}).get("gt_96_count"),
        "mechanism_read": (
            "EA(전문가 자문)는 feature_ready(피처 준비) 바에서만 Execute(실행)를 호출한다. "
            "feature row omission(피처 행 제거) 때문에 skipped bar(스킵 봉)에서는 max hold(최대 보유) 카운터가 진행되지 않아 실제 시간 보유가 길어진다."
        ),
    }


def load_run28e_mt5_records() -> list[dict[str, Any]]:
    kpi = read_json(STAGE_ROOT / "02_runs" / SOURCE_RUN28E_ID / "kpi_record.json")
    return run28e.normalized_mt5_records(kpi.get("mt5_kpi_records", []))


def load_run28e_trade_rows() -> pd.DataFrame:
    path = SOURCE_RUN28E_PACKET_ROOT / "trade_level_records.json"
    rows = read_json(path)
    return pd.DataFrame(rows)


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
    write_json(PACKET_ROOT / "normalized_kpi_records.json", records)
    write_json(PACKET_ROOT / "normalized_kpi_summary.json", summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(PACKET_ROOT / "enriched_kpi_records.json", enriched)
    write_json(PACKET_ROOT / "trade_level_records.json", trade_rows)
    write_json(PACKET_ROOT / "trade_attribution_summary.json", trade_summary)
    write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
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
    run28e_records = load_run28e_mt5_records()
    run28e_trades = load_run28e_trade_rows()
    component_rows = component_python_rows(tier_a)
    feature_rows = feature_ready_summary_rows(runtime_inputs["features_by_split"])
    mt5_rows = mt5_component_rows(result, run28e_records)
    month_rows = monthly_dependency_rows(tier_a, run28e_trades)
    hold_rows = hold_duration_rows(run28e_trades)
    completed = result.get("external_verification_status") == "completed"
    summary: dict[str, Any] = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_runs": [SOURCE_RUNTIME_RUN_ID, SOURCE_ATTRIBUTION_RUN_ID, SOURCE_RUN28E_ID],
        "source_packets": [SOURCE_RUNTIME_PACKET_ID, SOURCE_ATTRIBUTION_PACKET_ID, SOURCE_RUN28E_PACKET_ID],
        "created_at_utc": created_at,
        "active_branch": branch,
        "status": "reviewed_vol_adx_dependency_probe_completed" if completed else "blocked_vol_adx_dependency_probe_after_attempt",
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "boundary": BOUNDARY,
        "component_python_rows": component_rows,
        "feature_ready_summary_rows": feature_rows,
        "mt5_component_rows": mt5_rows,
        "monthly_dependency_rows": month_rows,
        "hold_duration_rows": hold_rows,
        "component_driver_read": component_driver_read(component_rows),
        "feature_ready_read": feature_ready_read(feature_rows),
        "mt5_component_read": mt5_component_read(mt5_rows),
        "october_dependency_read": october_dependency_read(month_rows),
        "hold_duration_read": hold_duration_read(hold_rows),
        "runtime_inputs": {key: value for key, value in runtime_inputs.items() if key != "features_by_split"},
        "external_verification_status": result.get("external_verification_status"),
        "mt5_attempt_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "known_runtime_difference": runtime_inputs.get("known_runtime_difference"),
        "next_action": NEXT_ACTION,
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority", "live_readiness"],
    }
    summary["output_paths"] = {
        "component_python_metrics": rel(RESULT_ROOT / "component_python_metrics.csv"),
        "feature_ready_summary": rel(RESULT_ROOT / "feature_ready_summary.csv"),
        "mt5_component_summary": rel(RESULT_ROOT / "mt5_component_summary.csv"),
        "monthly_dependency": rel(RESULT_ROOT / "monthly_dependency.csv"),
        "hold_duration_diagnostics": rel(RESULT_ROOT / "hold_duration_diagnostics.csv"),
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
    from stage_pipelines.stage34 import markov_long_permission_vol_adx_dependency_artifacts as artifacts

    artifacts.write_run_files(summary, result)
    kpi = write_normalized_kpi()
    summary["kpi_management"] = kpi
    summary["ledger_materialization"] = artifacts.materialize_ledgers(summary)
    write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    artifacts.write_packet_artifacts(summary, kpi)
    artifacts.update_stage_docs(summary)
    artifacts.update_workspace_state(summary)
    artifacts.prepend_context(summary)
    artifacts.append_changelog(summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage34 Tier A Markov vol/adx dependency probe.")
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
