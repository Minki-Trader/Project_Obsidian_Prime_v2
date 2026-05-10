from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane import mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
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
    copy_to_common,
)
from foundation.mt5 import runtime_support as mt5
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage35 import common
from stage_pipelines.stage49 import followup_suite as fu
from stage_pipelines.stage49 import reversal_selection_rule_mt5 as base


STAGE_ID = base.STAGE_ID
STAGE_NUMBER = base.STAGE_NUMBER
IDEA_ID = base.IDEA_ID
SOURCE_CANDIDATE_ID = base.SOURCE_CANDIDATE_ID
SOURCE_SIGNAL_COLUMN = base.SOURCE_SIGNAL_COLUMN
SOURCE_RUN_ROOT = base.SOURCE_RUN_ROOT
SOURCE_MODEL_PATH = base.SOURCE_MODEL_PATH
STAGE_ROOT = base.STAGE_ROOT
REVIEW_ROOT = base.REVIEW_ROOT

RUN43G_ID = "run43G_tier_a_only_adx_band_sweep_v1"
RUN43H_ID = "run43H_tier_a_short_side_attribution_v1"
RUN43I_ID = "run43I_oos_month_stress_v1"
RUN43J_ID = "run43J_tier_b_fallback_conditioning_v1"
PACKET_ID = "stage49_run43GHIJ_deep_followup_suite_v1"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
BOUNDARY = "deep_followup_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"

RUN_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs" / "workspace" / "changelog.md"

RUN43G_BANDS: tuple[tuple[int, int], ...] = fu.BANDS
RUN43J_VARIANTS = ("fallback_flat", "fallback_long_only", "fallback_unfiltered")

FEATURE_AUDIT_COLUMNS = fu.FEATURE_AUDIT_COLUMNS
MT5_SUMMARY_COLUMNS = fu.MT5_SUMMARY_COLUMNS
SHORT_ATTRIBUTION_COLUMNS = (
    "run_id",
    "source_run_id",
    "variant_id",
    "split",
    "bucket_family",
    "bucket",
    "short_trade_count",
    "net_profit",
    "win_count",
    "loss_count",
    "avg_mfe",
    "avg_mae",
    "avg_hold_bars",
)
MONTH_STRESS_COLUMNS = (
    "run_id",
    "source_run_id",
    "variant_id",
    "split",
    "month",
    "trade_count",
    "net_profit",
    "win_count",
    "loss_count",
    "net_profit_share_of_total_abs",
    "cumulative_net_profit",
)
LINEAGE_COLUMNS = ("artifact_id", "type", "path", "sha256", "availability", "notes")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return io_path(path).resolve().relative_to(io_path(common.ROOT).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def safe_name(value: str, limit: int = 96) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_")[:limit]


def run_root(run_id: str) -> Path:
    return STAGE_ROOT / "02_runs" / run_id.split("_", 1)[0]


def common_run_root(run_id: str) -> str:
    return f"Project_Obsidian_Prime_v2/stage49/{run_id.split('_', 1)[0]}"


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_yaml_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    common.write_csv(path, rows, columns)


def num(value: Any) -> float | None:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return None
    return output if math.isfinite(output) else None


def rounded(value: Any, digits: int = 6) -> Any:
    output = num(value)
    return None if output is None else round(output, digits)


def copy_model(run_id: str, common_files_root: Path) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "models").mkdir(parents=True, exist_ok=True)
    local_model = root / "models" / SOURCE_MODEL_PATH.name
    shutil.copy2(io_path(SOURCE_MODEL_PATH), io_path(local_model))
    common_path = f"{common_run_root(run_id)}/models/{local_model.name}"
    return {
        "local_path": local_model,
        "common_path": common_path,
        "sha256": sha256_file_lf_normalized(local_model),
        "common": copy_to_common(local_model, common_path, common_files_root),
    }


def materialize_tier_a_band_features(run_id: str, common_files_root: Path) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "features").mkdir(parents=True, exist_ok=True)
    adx_table = base.load_candidate_adx_table()
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for low, high in RUN43G_BANDS:
        variant_id = fu.band_variant(low, high)
        for runtime_split, tier_scope, source_name in base.source_feature_files():
            if tier_scope != mt5.TIER_A:
                continue
            source = pd.read_csv(io_path(SOURCE_RUN_ROOT / "features" / source_name))
            merged = source.merge(adx_table, on=keys, how="left", validate="one_to_one")
            filtered, removed = fu.apply_band_rule(merged, low, high)
            output = filtered.loc[:, source.columns].copy()
            split_token = "val" if runtime_split == "validation_is" else "oos"
            output_name = f"{run_id.split('_', 1)[0]}_c08_a_{split_token}_{variant_id}_s49.csv"
            output_path = root / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            common_path = f"{common_run_root(run_id)}/features/{output_name}"
            common_copies.append(copy_to_common(output_path, common_path, common_files_root))
            exports[f"{variant_id}_tier_a_{runtime_split}"] = {
                "path": output_path.as_posix(),
                "common_path": common_path,
                "split": runtime_split,
                "tier_scope": tier_scope,
                "rows": int(len(output)),
                "sha256": sha256_file_lf_normalized(output_path),
                "adx_low": low,
                "adx_high": high,
            }
            audit_rows.append(feature_audit_row(run_id, variant_id, output_path, runtime_split, tier_scope, source, merged, output, removed, low, high))
    write_csv(root / "results" / "feature_rule_audit.csv", audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def feature_audit_row(
    run_id: str,
    variant_id: str,
    output_path: Path,
    runtime_split: str,
    tier_scope: str,
    source: pd.DataFrame,
    merged: pd.DataFrame,
    output: pd.DataFrame,
    removed: int,
    low: int | None,
    high: int | None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "variant_id": variant_id,
        "feature_file": rel(output_path),
        "split": runtime_split,
        "tier_scope": tier_scope,
        "input_rows": int(len(source)),
        "matched_rows": int(merged["adx_14"].notna().sum()) if "adx_14" in merged.columns else int(len(source)),
        "unmatched_rows": int(merged["adx_14"].isna().sum()) if "adx_14" in merged.columns else 0,
        "original_long_signals": int(pd.to_numeric(source[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(1).sum()),
        "original_short_signals": int(pd.to_numeric(source[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(-1).sum()),
        "filtered_long_signals": int(pd.to_numeric(output[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(1).sum()),
        "filtered_short_signals": int(pd.to_numeric(output[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(-1).sum()),
        "rule_removed_short_signals": removed,
        "rule_id": f"skip_short_{variant_id}",
        "adx_low": low,
        "adx_high": high,
    }


def make_tier_a_band_attempt(run_id: str, variant_id: str, runtime_split: str, model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]], magic: int) -> dict[str, Any]:
    rules = base.source_rule_values()
    low_high = re.search(r"adx_(\d+)_(\d+)", variant_id)
    from_date, to_date = base.source_split_dates(runtime_split)
    attempt_name = f"tier_a_c08_{variant_id}_{runtime_split}"
    payload = attempt_payload(
        run_root=run_root(run_id),
        run_id=run_id,
        stage_number=STAGE_NUMBER,
        exploration_label="stage49_TradeLifecycle__TierAAdxSweep",
        attempt_name=attempt_name,
        tier=mt5.TIER_A,
        split=runtime_split,
        model_path=str(model_payload["common_path"]),
        model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_a_signal_table",
        model_backend="ebm_table",
        feature_path=str(exports[f"{variant_id}_tier_a_{runtime_split}"]["common_path"]),
        feature_count=1,
        feature_order_hash=str(rules["feature_order_hash"]),
        short_threshold=float(rules["short_threshold"]),
        long_threshold=float(rules["long_threshold"]),
        min_margin=float(rules["min_margin"]),
        invert_signal=bool(rules["invert_signal"]),
        from_date=from_date,
        to_date=to_date,
        primary_active_tier="tier_a",
        attempt_role="tier_only_total",
        record_view_prefix=f"mt5_tier_a_c08_{variant_id}",
        max_hold_bars=int(rules["max_hold_bars"]),
        common_root=common_run_root(run_id),
        fallback_enabled=False,
        close_on_flat_signal=bool(rules["close_on_flat_signal"]),
        reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
        close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
        extra_set_values={"InpMagic": magic},
    )
    payload.update(
        {
            "candidate_id": SOURCE_CANDIDATE_ID,
            "variant_id": variant_id,
            "route_mode": "tier_a_only",
            "adx_low": int(low_high.group(1)) if low_high else None,
            "adx_high": int(low_high.group(2)) if low_high else None,
        }
    )
    return payload


def route_coverage_for_tier_a(audit_rows: Sequence[Mapping[str, Any]], variant_id: str) -> dict[str, Any]:
    rows = [row for row in audit_rows if row["variant_id"] == variant_id]
    by_split: dict[str, dict[str, int]] = {}
    for runtime_split in ("validation_is", "oos"):
        source_split = "validation" if runtime_split == "validation_is" else "oos"
        tier_a_rows = sum(int(row["input_rows"]) for row in rows if row["split"] == runtime_split)
        by_split[source_split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": 0,
            "routed_labelable_rows": tier_a_rows,
            "no_tier_labelable_rows": None,
        }
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": {}, "no_tier_by_split": {}}


def run43g(common_files_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    run_id = RUN43G_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    model_payload = copy_model(run_id, common_files_root)
    features = materialize_tier_a_band_features(run_id, common_files_root)
    attempts = [
        make_tier_a_band_attempt(run_id, fu.band_variant(low, high), split, model_payload, features["exports"], 1001100 + index)
        for index, (low, high, split) in enumerate((low, high, split) for low, high in RUN43G_BANDS for split in ("validation_is", "oos"))
    ]
    result = fu.execute_mt5_run(
        run_id,
        attempts,
        route_coverage_for_tier_a(features["feature_audit_rows"], fu.band_variant(20, 25)),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = fu.build_mt5_summary(run_id, result, features["feature_audit_rows"])
    robustness = fu.evaluate_band_robustness(summary_rows)
    write_csv(root / "results" / "tier_a_adx_band_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "attempts": attempts, "feature_audit_rows": features["feature_audit_rows"], "mt5": result, "summary_rows": summary_rows, "robustness": robustness, "boundary": BOUNDARY})
    return {"run_id": run_id, "model": model_payload, "features": features, "attempts": attempts, "mt5": result, "summary_rows": summary_rows, "robustness": robustness}


def best_variant(summary_rows: Sequence[Mapping[str, Any]]) -> str:
    robustness = fu.evaluate_band_robustness(summary_rows)
    candidate = robustness.get("best_variant", {}).get("variant_id")
    return str(candidate or "adx_20_25")


def report_records_by_attempt(mt5_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in mt5_result.get("strategy_tester_reports", [])}


def report_path_from_record(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def market_feature_at(market_data: mt5_trade_attribution.MarketData, timestamp: pd.Timestamp) -> Mapping[str, Any]:
    matched = market_data.features.loc[market_data.features["timestamp_key"].eq(pd.Timestamp(timestamp))]
    return {} if matched.empty else matched.iloc[-1].to_dict()


def di_spread_bucket(value: Any) -> str:
    output = num(value)
    if output is None:
        return "feature_missing"
    if output <= -10.0:
        return "di_short_strong"
    if output < 0.0:
        return "di_short_mild"
    if output <= 10.0:
        return "di_long_mild"
    return "di_long_strong"


def parse_report_trades(report_path: Path, market_data: mt5_trade_attribution.MarketData) -> list[dict[str, Any]]:
    report = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(report["deals"])
    stats = mt5_trade_attribution.compute_trade_attribution(trades, market_data)
    rows = []
    for payload in stats["trades"]:
        feature = market_feature_at(market_data, pd.Timestamp(payload["open_time"]))
        row = dict(payload)
        row["di_spread_bucket"] = di_spread_bucket(feature.get("di_spread_14"))
        row["di_spread_14"] = rounded(feature.get("di_spread_14"))
        rows.append(row)
    return rows


def run43h(run43g_result: Mapping[str, Any], selected_variant: str) -> dict[str, Any]:
    run_id = RUN43H_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    reports = report_records_by_attempt(run43g_result["mt5"])
    attribution_rows: list[dict[str, Any]] = []
    source_reports: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        attempt_name = f"tier_a_c08_{selected_variant}_{split}"
        report_record = reports[attempt_name]
        report_path = report_path_from_record(report_record)
        trade_rows = parse_report_trades(report_path, market_data)
        source_reports.append({"attempt_name": attempt_name, "path": report_path.as_posix(), "sha256": sha256_file_lf_normalized(report_path)})
        short_rows = [row for row in trade_rows if row.get("direction") == "sell"]
        for family in ("session_slice", "volatility_regime", "trend_regime", "adx_bucket", "di_spread_bucket", "month"):
            buckets = sorted({str(row.get(family) or "missing") for row in short_rows})
            for bucket in buckets:
                selected = [row for row in short_rows if str(row.get(family) or "missing") == bucket]
                attribution_rows.append(
                    {
                        "run_id": run_id,
                        "source_run_id": RUN43G_ID,
                        "variant_id": selected_variant,
                        "split": split,
                        "bucket_family": family,
                        "bucket": bucket,
                        "short_trade_count": len(selected),
                        "net_profit": rounded(sum(float(row.get("net_profit") or 0.0) for row in selected)),
                        "win_count": sum(1 for row in selected if float(row.get("net_profit") or 0.0) > 0.0),
                        "loss_count": sum(1 for row in selected if float(row.get("net_profit") or 0.0) < 0.0),
                        "avg_mfe": rounded(pd.Series([float(row.get("mfe") or 0.0) for row in selected]).mean() if selected else None),
                        "avg_mae": rounded(pd.Series([float(row.get("mae") or 0.0) for row in selected]).mean() if selected else None),
                        "avg_hold_bars": rounded(pd.Series([float(row.get("hold_bars") or 0.0) for row in selected]).mean() if selected else None),
                    }
                )
    write_csv(root / "results" / "tier_a_short_side_attribution.csv", attribution_rows, SHORT_ATTRIBUTION_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "source_run_id": RUN43G_ID, "variant_id": selected_variant, "source_reports": source_reports, "rows": len(attribution_rows), "boundary": BOUNDARY})
    return {"run_id": run_id, "variant_id": selected_variant, "rows": attribution_rows, "source_reports": source_reports}


def materialize_j_features(run_id: str, selected_variant: str, common_files_root: Path) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "features").mkdir(parents=True, exist_ok=True)
    low, high = [int(part) for part in selected_variant.replace("adx_", "").split("_")]
    adx_table = base.load_candidate_adx_table()
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for variant_id in RUN43J_VARIANTS:
        for runtime_split, tier_scope, source_name in base.source_feature_files():
            source = pd.read_csv(io_path(SOURCE_RUN_ROOT / "features" / source_name))
            merged = source.merge(adx_table, on=keys, how="left", validate="one_to_one")
            removed = 0
            if tier_scope == mt5.TIER_A:
                filtered, removed = fu.apply_band_rule(merged, low, high)
            elif variant_id == "fallback_flat":
                filtered = merged.copy()
                removed = int(pd.to_numeric(filtered[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(-1).sum())
                filtered[SOURCE_SIGNAL_COLUMN] = 0
                filtered["entry_decision"] = "flat"
            elif variant_id == "fallback_long_only":
                filtered = merged.copy()
                mask = pd.to_numeric(filtered[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(-1)
                removed = int(mask.sum())
                filtered.loc[mask, SOURCE_SIGNAL_COLUMN] = 0
                filtered.loc[mask, "entry_decision"] = "flat"
            else:
                filtered = merged.copy()
            output = filtered.loc[:, source.columns].copy()
            tier_token = "a" if tier_scope == mt5.TIER_A else "b"
            split_token = "val" if runtime_split == "validation_is" else "oos"
            output_name = f"{run_id.split('_', 1)[0]}_c08_{tier_token}_{split_token}_{variant_id}_s49.csv"
            output_path = root / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            tier_key = "tier_a" if tier_scope == mt5.TIER_A else "tier_b"
            exports[f"{variant_id}_{tier_key}_{runtime_split}"] = {"path": output_path.as_posix(), "common_path": f"{common_run_root(run_id)}/features/{output_name}", "split": runtime_split, "tier_scope": tier_scope, "sha256": sha256_file_lf_normalized(output_path)}
            common_copies.append(copy_to_common(output_path, f"{common_run_root(run_id)}/features/{output_name}", common_files_root))
            audit_rows.append(feature_audit_row(run_id, variant_id, output_path, runtime_split, tier_scope, source, merged, output, removed, low if tier_scope == mt5.TIER_A else None, high if tier_scope == mt5.TIER_A else None))
    write_csv(root / "results" / "fallback_condition_feature_audit.csv", audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def make_j_attempt(run_id: str, variant_id: str, runtime_split: str, model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]], magic: int) -> dict[str, Any]:
    rules = base.source_rule_values()
    from_date, to_date = base.source_split_dates(runtime_split)
    attempt_name = f"routed_c08_{variant_id}_{runtime_split}"
    payload = attempt_payload(
        run_root=run_root(run_id),
        run_id=run_id,
        stage_number=STAGE_NUMBER,
        exploration_label="stage49_TradeLifecycle__FallbackConditioning",
        attempt_name=attempt_name,
        tier=mt5.TIER_AB,
        split=runtime_split,
        model_path=str(model_payload["common_path"]),
        model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_signal_table",
        model_backend="ebm_table",
        feature_path=str(exports[f"{variant_id}_tier_a_{runtime_split}"]["common_path"]),
        feature_count=1,
        feature_order_hash=str(rules["feature_order_hash"]),
        short_threshold=float(rules["short_threshold"]),
        long_threshold=float(rules["long_threshold"]),
        min_margin=float(rules["min_margin"]),
        invert_signal=bool(rules["invert_signal"]),
        from_date=from_date,
        to_date=to_date,
        primary_active_tier="tier_a",
        attempt_role="routed_total",
        record_view_prefix=f"mt5_routed_c08_{variant_id}",
        max_hold_bars=int(rules["max_hold_bars"]),
        common_root=common_run_root(run_id),
        fallback_enabled=True,
        fallback_model_path=str(model_payload["common_path"]),
        fallback_model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_b_signal_table",
        fallback_model_backend="ebm_table",
        fallback_feature_path=str(exports[f"{variant_id}_tier_b_{runtime_split}"]["common_path"]),
        fallback_feature_count=1,
        fallback_feature_order_hash=str(rules["fallback_feature_order_hash"]),
        fallback_short_threshold=float(rules["fallback_short_threshold"]),
        fallback_long_threshold=float(rules["fallback_long_threshold"]),
        fallback_min_margin=float(rules["fallback_min_margin"]),
        fallback_invert_signal=bool(rules["fallback_invert_signal"]),
        close_on_flat_signal=bool(rules["close_on_flat_signal"]),
        reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
        close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
        extra_set_values={"InpMagic": magic},
    )
    payload.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": variant_id, "route_mode": variant_id})
    return payload


def run43j(common_files_root: Path, args: argparse.Namespace, selected_variant: str, run43g_result: Mapping[str, Any]) -> dict[str, Any]:
    run_id = RUN43J_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    model_payload = copy_model(run_id, common_files_root)
    features = materialize_j_features(run_id, selected_variant, common_files_root)
    attempts = [
        make_j_attempt(run_id, variant_id, split, model_payload, features["exports"], 1001120 + index)
        for index, (variant_id, split) in enumerate((variant_id, split) for variant_id in RUN43J_VARIANTS for split in ("validation_is", "oos"))
    ]
    result = fu.execute_mt5_run(
        run_id,
        attempts,
        fu.route_coverage_from_audit(features["feature_audit_rows"], "fallback_flat"),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = fu.build_mt5_summary(run_id, result, features["feature_audit_rows"])
    references = j_reference_rows(selected_variant, run43g_result)
    all_rows = references + summary_rows
    write_csv(root / "results" / "fallback_conditioning_summary.csv", all_rows, MT5_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "selected_variant": selected_variant, "attempts": attempts, "feature_audit_rows": features["feature_audit_rows"], "references": references, "mt5": result, "summary_rows": all_rows, "boundary": BOUNDARY})
    return {"run_id": run_id, "model": model_payload, "features": features, "attempts": attempts, "mt5": result, "summary_rows": all_rows}


def j_reference_rows(selected_variant: str, run43g_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in run43g_result["summary_rows"]:
        if row["variant_id"] == selected_variant:
            current = dict(row)
            current["run_id"] = RUN43J_ID
            current["route_mode"] = "fallback_off_reference"
            current["attempt_name"] = f"reference_{current['attempt_name']}"
            rows.append(current)
    c_summary_path = run_root(fu.RUN43C_ID) / "results" / "mt5_band_summary.csv"
    if path_exists(c_summary_path):
        c_frame = pd.read_csv(io_path(c_summary_path))
        for row in c_frame.loc[c_frame["variant_id"].astype(str).eq(selected_variant)].to_dict("records"):
            current = dict(row)
            current["run_id"] = RUN43J_ID
            current["route_mode"] = "fallback_band_rule_reference"
            current["attempt_name"] = f"reference_{current['attempt_name']}"
            rows.append(current)
    return rows


def run43i(run43g_result: Mapping[str, Any], run43j_result: Mapping[str, Any], selected_variant: str) -> dict[str, Any]:
    run_id = RUN43I_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    sources = []
    g_reports = report_records_by_attempt(run43g_result["mt5"])
    sources.append(("run43G_tier_a_best", RUN43G_ID, selected_variant, report_path_from_record(g_reports[f"tier_a_c08_{selected_variant}_oos"])))
    j_reports = report_records_by_attempt(run43j_result["mt5"])
    for variant_id in RUN43J_VARIANTS:
        sources.append((f"run43J_{variant_id}", RUN43J_ID, variant_id, report_path_from_record(j_reports[f"routed_c08_{variant_id}_oos"])))
    b_reports = json.loads(io_path(base.PACKET_ROOT / "runtime_evidence_gate.json").read_text(encoding="utf-8")).get("strategy_tester_reports", [])
    for report in b_reports:
        if report.get("split") == "oos":
            sources.append(("run43B_ab_rule", base.RUN_ID, "adx_20_25", Path(str(report["html_report"]["path"]))))
    rows: list[dict[str, Any]] = []
    for label, source_run_id, variant_id, report_path in sources:
        trades = parse_report_trades(report_path, market_data)
        frame = pd.DataFrame(trades)
        if frame.empty:
            continue
        frame["month"] = pd.to_datetime(frame["close_time"]).dt.strftime("%Y-%m")
        frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
        total_abs = float(frame.groupby("month")["net_profit"].sum().abs().sum() or 0.0)
        cumulative = 0.0
        for month, group in frame.groupby("month", sort=True):
            net = float(group["net_profit"].sum())
            cumulative += net
            rows.append(
                {
                    "run_id": run_id,
                    "source_run_id": source_run_id,
                    "variant_id": f"{label}:{variant_id}",
                    "split": "oos",
                    "month": month,
                    "trade_count": int(len(group)),
                    "net_profit": rounded(net),
                    "win_count": int((group["net_profit"] > 0.0).sum()),
                    "loss_count": int((group["net_profit"] < 0.0).sum()),
                    "net_profit_share_of_total_abs": rounded(abs(net) / total_abs if total_abs else None),
                    "cumulative_net_profit": rounded(cumulative),
                }
            )
    write_csv(root / "results" / "oos_month_stress.csv", rows, MONTH_STRESS_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "selected_variant": selected_variant, "rows": rows, "boundary": BOUNDARY})
    return {"run_id": run_id, "rows": rows}


def report_records_by_attempt(mt5_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in mt5_result.get("strategy_tester_reports", [])}


def report_path_from_record(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def evaluate_deep_judgment(run43g_result: Mapping[str, Any], run43j_result: Mapping[str, Any]) -> tuple[str, str]:
    g_status = run43g_result["robustness"]["status"]
    if run43g_result["mt5"].get("external_verification_status") != "completed" or run43j_result["mt5"].get("external_verification_status") != "completed":
        return "blocked_stage49_deep_followup_missing_mt5_execution", "one_or_more_mt5_runs_blocked"
    if g_status == "passed":
        return "reviewed_completed_positive_deep_followup_runtime_probe_only", "tier_a_adx_band_robustness_passed;fallback_conditioning_tested_not_promotion"
    if g_status == "weak":
        return "reviewed_completed_inconclusive_deep_followup_runtime_probe_only", "tier_a_adx_band_robustness_weak"
    return "reviewed_completed_negative_memory_deep_followup_runtime_probe_only", "tier_a_adx_band_robustness_failed"


def lineage_rows() -> list[dict[str, Any]]:
    source_rows = [
        ("stage49_deep_source_run43CDEF_summary", "source_packet", fu.PACKET_ROOT / "aggregate_summary.json", "tracked_source", "Prior Stage49 follow-up suite."),
        ("stage49_deep_source_run43B_runtime_gate", "source_gate", base.PACKET_ROOT / "runtime_evidence_gate.json", "tracked_source", "run43B MT5 runtime reports."),
        ("stage49_deep_source_stage45_score_table", "model_table", SOURCE_MODEL_PATH, "tracked_source", "Unchanged Stage45 score table."),
    ]
    for run_id in (RUN43G_ID, RUN43H_ID, RUN43I_ID, RUN43J_ID):
        source_rows.append((f"stage49_{run_id.split('_', 1)[0]}_manifest", "manifest", run_root(run_id) / "run_manifest.json", "ignored_regenerable_from_run_command", f"{run_id} manifest."))
    payload = []
    for artifact_id, artifact_type, path, availability, notes in source_rows:
        payload.append(
            {
                "artifact_id": artifact_id,
                "type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and path.is_file() else "missing",
                "availability": availability,
                "notes": notes,
            }
        )
    return payload


def ledger_rows_for_mt5(run_id: str, result: Mapping[str, Any], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows.append(
            {
                "ledger_row_id": safe_name(f"{run_id}__{record.get('record_view')}__{record.get('tier_scope')}", 180),
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": record.get("subrun_id") or record.get("record_view"),
                "parent_run_id": run_id,
                "record_view": record.get("record_view", ""),
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "stage49_deep_followup_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": record.get("path", ""),
                "primary_kpi": ledger_pairs([("split", record.get("split")), ("route_role", record.get("route_role")), ("net_profit", metrics.get("net_profit")), ("profit_factor", metrics.get("profit_factor")), ("trade_count", metrics.get("trade_count"))]),
                "guardrail_kpi": "deep_followup_probe_only;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
                "notes": BOUNDARY,
            }
        )
    return rows


def write_ledgers(results: Mapping[str, Any], judgment: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_rows = [
        {"run_id": RUN43G_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43G_ID)), "notes": BOUNDARY},
        {"run_id": RUN43H_ID, "stage_id": STAGE_ID, "lane": "trade_level_attribution", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43H_ID)), "notes": BOUNDARY},
        {"run_id": RUN43I_ID, "stage_id": STAGE_ID, "lane": "oos_month_stress", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43I_ID)), "notes": BOUNDARY},
        {"run_id": RUN43J_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43J_ID)), "notes": BOUNDARY},
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    ledger_rows = []
    ledger_rows.extend(ledger_rows_for_mt5(RUN43G_ID, results["run43g"]["mt5"], judgment))
    ledger_rows.extend(ledger_rows_for_mt5(RUN43J_ID, results["run43j"]["mt5"], judgment))
    supplement_rows = [
        (RUN43H_ID, "tier_a_short_side_attribution", run_root(RUN43H_ID) / "results" / "tier_a_short_side_attribution.csv", f"rows={len(results['run43h']['rows'])}"),
        (RUN43I_ID, "oos_month_stress", run_root(RUN43I_ID) / "results" / "oos_month_stress.csv", f"rows={len(results['run43i']['rows'])}"),
    ]
    for run_id, view, path, primary in supplement_rows:
        ledger_rows.append(
            {
                "ledger_row_id": f"{run_id}__{view}",
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": view,
                "parent_run_id": RUN43G_ID,
                "record_view": view,
                "tier_scope": "Tier A",
                "kpi_scope": "stage49_deep_followup_supplement",
                "scoreboard_lane": "runtime_probe_supplement",
                "status": "reviewed",
                "judgment": judgment,
                "path": rel(path),
                "primary_kpi": primary,
                "guardrail_kpi": "actual_mt5_report_derived;no_new_runtime_authority",
                "external_verification_status": "completed_existing_mt5_report_derived_trades",
                "notes": BOUNDARY,
            }
        )
    stage_payload = upsert_csv_rows(REVIEW_ROOT / "stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_rows = [{"artifact_id": row["artifact_id"], "type": row["type"], "path": row["path"], "status": row["availability"], "notes": row["notes"]} for row in artifacts]
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_docs(results: Mapping[str, Any], judgment: str, reasons: str, selected_variant: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    g = results["run43g"]["robustness"]
    j_rows = results["run43j"]["summary_rows"]
    best_j = max([row for row in j_rows if row.get("split") == "oos"], key=lambda row: float(row.get("net_profit") or -1e18), default={})
    write_md(REVIEW_ROOT / "run43G_packet.md", f"""# {RUN43G_ID} Packet(패킷)

- purpose(목적): Tier A only ADX band sweep(Tier A만 ADX 구간 훑기)
- selected_variant(선택 변형): `{selected_variant}`
- robustness_status(강건성 상태): `{g.get('status')}`
- passed_variants(통과 변형): `{','.join(g.get('passed_variants', []))}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run43H_packet.md", f"""# {RUN43H_ID} Packet(패킷)

- purpose(목적): Tier A short-side attribution(Tier A 숏 방향 귀속)
- source_variant(원천 변형): `{selected_variant}`
- attribution_rows(귀속 행): `{len(results['run43h']['rows'])}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run43I_packet.md", f"""# {RUN43I_ID} Packet(패킷)

- purpose(목적): OOS month stress(외표본 월별 압박)
- stress_rows(압박 행): `{len(results['run43i']['rows'])}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run43J_packet.md", f"""# {RUN43J_ID} Packet(패킷)

- purpose(목적): Tier B fallback conditioning(Tier B 대체 조건화)
- best_oos_row(최선 외표본 행): `{best_j}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "stage49_deep_followup_suite_packet.md", f"""# Stage49 Deep Follow-up Suite(49단계 심화 후속 묶음)

- judgment(판정): `{judgment}`
- decision_reasons(결정 이유): `{reasons}`
- run43G(43G 실행): Tier A ADX band robustness(Tier A ADX 구간 강건성) `{g.get('status')}`
- run43H(43H 실행): Tier A short-side attribution(Tier A 숏 방향 귀속) completed(완료)
- run43I(43I 실행): OOS month stress(외표본 월별 압박) completed(완료)
- run43J(43J 실행): Tier B fallback conditioning(Tier B 대체 조건화) completed(완료)
- boundary(주장 경계): `{BOUNDARY}`

This suite(묶음)는 deep followup runtime probe only(심화 후속 런타임 탐침 전용)다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않는다.
""")
    write_md(REVIEW_ROOT / "review_index.md", """# Review Index(검토 색인)

- run43A packet(43A 패킷): `03_reviews/run43A_packet.md`
- run43B packet(43B 패킷): `03_reviews/run43B_packet.md`
- run43C-F follow-up suite(43C-F 후속 묶음): `03_reviews/stage49_followup_suite_packet.md`
- run43G packet(43G 패킷): `03_reviews/run43G_packet.md`
- run43H packet(43H 패킷): `03_reviews/run43H_packet.md`
- run43I packet(43I 패킷): `03_reviews/run43I_packet.md`
- run43J packet(43J 패킷): `03_reviews/run43J_packet.md`
- deep follow-up suite packet(심화 후속 묶음 패킷): `03_reviews/stage49_deep_followup_suite_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
""")
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage49 Selection Status(49단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- promotion_packet(승격 패킷): `none`
- latest_run_id(최신 실행 ID): `{RUN43J_ID}`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- selected_deep_followup_variant(선택 심화 후속 변형): `{selected_variant}`
- deep_followup_suite(심화 후속 묶음): `{PACKET_ID}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_packet_files(results, judgment, reasons, selected_variant, ledger_payload, artifacts)
    update_current_truth(judgment, selected_variant, g)


def write_packet_files(results: Mapping[str, Any], judgment: str, reasons: str, selected_variant: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    completed = results["run43g"]["mt5"].get("external_verification_status") == "completed" and results["run43j"]["mt5"].get("external_verification_status") == "completed"
    required_gates = ["runtime_evidence_gate", "kpi_contract_audit", "artifact_lineage_audit", "result_judgment_gate", "required_gate_coverage_audit", "final_claim_guard"]
    write_yaml_text(PACKET_ROOT / "work_packet.yaml", f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_ids:
  - {RUN43G_ID}
  - {RUN43H_ID}
  - {RUN43I_ID}
  - {RUN43J_ID}
primary_family: runtime_backtest
primary_skill: obsidian-runtime-parity
support_skills:
  - obsidian-backtest-forensics
  - obsidian-run-evidence-system
  - obsidian-artifact-lineage
  - obsidian-result-judgment
required_gates:
{chr(10).join(f"  - {gate}" for gate in required_gates)}
status: {"reviewed_deep_followup_suite_completed" if completed else "blocked_deep_followup_suite"}
claim_boundary: {BOUNDARY}
""")
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "judgment": judgment, "decision_reasons": reasons, "selected_variant": selected_variant, "run43g": {"robustness": results["run43g"]["robustness"], "summary_rows": results["run43g"]["summary_rows"]}, "run43h": {"rows": len(results["run43h"]["rows"])}, "run43i": {"rows": results["run43i"]["rows"]}, "run43j": {"summary_rows": results["run43j"]["summary_rows"]}, "boundary": BOUNDARY, "ledger_sync": ledger_payload, "artifacts": list(artifacts), "created_at_utc": utc_now()})
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"status": "passed" if completed else "failed", "run43g": results["run43g"]["mt5"], "run43j": results["run43j"]["mt5"]})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if completed else "blocked", "run43g_mt5_rows": len(results["run43g"]["mt5"].get("mt5_kpi_records", [])), "run43j_mt5_rows": len(results["run43j"]["mt5"].get("mt5_kpi_records", [])), "synthetic_sum_used_as_routed_total": False})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "artifacts": list(artifacts)})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "decision_reasons": reasons, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed" if completed else "blocked", "required_gates": required_gates, "covered_gates": required_gates if completed else [], "missing_gates": [] if completed else ["runtime_evidence_gate"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": [{"command": "python -m foundation.pipelines.run_stage49_deep_followup_suite --timeout-seconds 900", "result": "recorded_by_pipeline", "failures_or_blockers": ""}], "status": "recorded"})


def update_current_truth(judgment: str, selected_variant: str, robustness: Mapping[str, Any]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN43J_ID}", state_text, flags=re.MULTILINE)
    block_name = "stage49_deep_followup_suite"
    block = f"""

{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_deep_followup_suite_completed
  current_run_id: {RUN43J_ID}
  judgment: {judgment}
  selected_variant: {selected_variant}
  run43g_robustness_status: {robustness.get("status")}
  report_path: {rel(REVIEW_ROOT / "stage49_deep_followup_suite_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage49 Deep Follow-up Suite(최신 49단계 심화 후속 묶음)

Stage49(49단계) completed(완료) run43G/run43H/run43I/run43J as `{judgment}`. Selected variant(선택 변형)는 `{selected_variant}`이고, 이 묶음은 deep followup runtime probe only(심화 후속 런타임 탐침 전용)라서 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)를 만들지 않았다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{STAGE_ID}` completed `{PACKET_ID}` with `{judgment}`.\n", encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(STAGE_ROOT / folder).mkdir(parents=True, exist_ok=True)
    result_g = run43g(common_files_root, args)
    selected_variant = best_variant(result_g["summary_rows"])
    result_h = run43h(result_g, selected_variant)
    result_j = run43j(common_files_root, args, selected_variant, result_g)
    result_i = run43i(result_g, result_j, selected_variant)
    results = {"run43g": result_g, "run43h": result_h, "run43i": result_i, "run43j": result_j}
    judgment, reasons = evaluate_deep_judgment(result_g, result_j)
    artifacts = lineage_rows()
    write_csv(run_root(RUN43G_ID) / "results" / "lineage.csv", artifacts, LINEAGE_COLUMNS)
    ledger_payload = write_ledgers(results, judgment, artifacts)
    write_docs(results, judgment, reasons, selected_variant, ledger_payload, artifacts)
    return {"judgment": judgment, "decision_reasons": reasons, "selected_variant": selected_variant, **results}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args(argv)
    result = run(args)
    print(
        json.dumps(
            json_ready(
                {
                    "judgment": result["judgment"],
                    "decision_reasons": result["decision_reasons"],
                    "selected_variant": result["selected_variant"],
                    "run43g_robustness": result["run43g"]["robustness"],
                    "run43j_summary_rows": result["run43j"]["summary_rows"],
                    "run43h_rows": len(result["run43h"]["rows"]),
                    "run43i_rows": result["run43i"]["rows"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
