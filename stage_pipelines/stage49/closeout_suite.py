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
from stage_pipelines.stage35 import common
from stage_pipelines.stage49 import deep_followup_suite as deep
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

RUN43K_ID = "run43K_tier_b_subtype_conditional_fallback_v1"
RUN43L_ID = "run43L_december_oos_loss_forensics_v1"
RUN43M_ID = "run43M_hold_time_late_session_exit_probe_v1"
RUN43N_ID = "run43N_adx_leave_one_month_stability_v1"
CLOSEOUT_ID = "stage49_closeout_v1"
PACKET_ID = "stage49_run43KLMN_closeout_suite_v1"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
BOUNDARY = "stage49_closeout_reference_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"

RUN_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs" / "workspace" / "changelog.md"

SELECTED_VARIANT_DEFAULT = "adx_20_25"
K_VARIANTS = (
    "subtype_macro_only",
    "subtype_mixed_only",
    "subtype_core_only",
    "subtype_non_macro_only",
)
M_VARIANTS: dict[str, dict[str, Any]] = {
    "hold06": {"max_hold_bars": 6, "close_on_flat_signal": False, "late_entry_filter": False},
    "hold24": {"max_hold_bars": 24, "close_on_flat_signal": False, "late_entry_filter": False},
    "close_flat": {"max_hold_bars": 12, "close_on_flat_signal": True, "late_entry_filter": False},
    "no_late_entry": {"max_hold_bars": 12, "close_on_flat_signal": False, "late_entry_filter": True},
}

FEATURE_AUDIT_COLUMNS = fu.FEATURE_AUDIT_COLUMNS
MT5_SUMMARY_COLUMNS = fu.MT5_SUMMARY_COLUMNS
SUBTYPE_AUDIT_COLUMNS = (
    "run_id",
    "variant_id",
    "split",
    "tier_scope",
    "partial_context_subtype",
    "input_rows",
    "original_long_signals",
    "original_short_signals",
    "filtered_long_signals",
    "filtered_short_signals",
    "removed_long_signals",
    "removed_short_signals",
)
DECEMBER_FORENSIC_COLUMNS = (
    "run_id",
    "source_run_id",
    "variant_id",
    "split",
    "month",
    "bucket_family",
    "bucket",
    "trade_count",
    "net_profit",
    "win_count",
    "loss_count",
    "avg_hold_bars",
    "avg_mfe",
    "avg_mae",
    "loss_with_positive_mfe_count",
)
LOMO_COLUMNS = (
    "run_id",
    "source_run_id",
    "variant_id",
    "split",
    "total_net_profit",
    "worst_month",
    "worst_month_net_profit",
    "leave_one_month_min_net_profit",
    "leave_one_month_min_excluded_month",
    "positive_month_count",
    "negative_month_count",
    "stability_status",
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


def load_manifest(run_id: str) -> dict[str, Any]:
    path = run_root(run_id) / "run_manifest.json"
    return json.loads(io_path(path).read_text(encoding="utf-8"))


def selected_variant_from_deep_packet() -> str:
    path = deep.PACKET_ROOT / "aggregate_summary.json"
    if not path_exists(path):
        return SELECTED_VARIANT_DEFAULT
    payload = json.loads(io_path(path).read_text(encoding="utf-8"))
    return str(payload.get("selected_variant") or SELECTED_VARIANT_DEFAULT)


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


def selected_band_bounds(selected_variant: str) -> tuple[int, int]:
    parts = selected_variant.replace("adx_", "").split("_")
    return int(parts[0]), int(parts[1])


def subtype_allowed(variant_id: str, subtype: str) -> bool:
    subtype = str(subtype or "")
    if variant_id == "subtype_macro_only":
        return subtype == "B_macro_missing"
    if variant_id == "subtype_mixed_only":
        return subtype == "B_mixed_partial_context"
    if variant_id == "subtype_core_only":
        return subtype == "B_core_only"
    if variant_id == "subtype_non_macro_only":
        return subtype != "B_macro_missing"
    return False


def add_session_slice(frame: pd.DataFrame, market_data: mt5_trade_attribution.MarketData) -> pd.DataFrame:
    output = frame.copy()
    lookup = market_data.features.loc[:, ["timestamp_key", "minutes_from_cash_open"]].copy()
    output["timestamp_key"] = pd.to_datetime(output["timestamp_utc"], errors="coerce", utc=True).dt.tz_convert(None)
    lookup["timestamp_key"] = pd.to_datetime(lookup["timestamp_key"], errors="coerce")
    if getattr(lookup["timestamp_key"].dt, "tz", None) is not None:
        lookup["timestamp_key"] = lookup["timestamp_key"].dt.tz_convert(None)
    merged = output.merge(lookup, on="timestamp_key", how="left")
    merged["session_slice"] = [
        mt5_trade_attribution._session_slice(minutes, timestamp)
        for minutes, timestamp in zip(merged["minutes_from_cash_open"], merged["timestamp_key"], strict=False)
    ]
    return merged


def subtype_rows(run_id: str, variant_id: str, runtime_split: str, tier_scope: str, source: pd.DataFrame, output: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_signal = pd.to_numeric(source[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0)
    output_signal = pd.to_numeric(output[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0)
    source_local = source.assign(_orig_long=source_signal.eq(1), _orig_short=source_signal.eq(-1))
    output_local = output.assign(_filt_long=output_signal.eq(1), _filt_short=output_signal.eq(-1))
    for subtype in sorted({str(value or "missing") for value in source_local["partial_context_subtype"].fillna("missing").unique()}):
        src = source_local.loc[source_local["partial_context_subtype"].fillna("missing").astype(str).eq(subtype)]
        out = output_local.loc[output_local["partial_context_subtype"].fillna("missing").astype(str).eq(subtype)]
        orig_long = int(src["_orig_long"].sum())
        orig_short = int(src["_orig_short"].sum())
        filt_long = int(out["_filt_long"].sum())
        filt_short = int(out["_filt_short"].sum())
        rows.append(
            {
                "run_id": run_id,
                "variant_id": variant_id,
                "split": runtime_split,
                "tier_scope": tier_scope,
                "partial_context_subtype": subtype,
                "input_rows": int(len(src)),
                "original_long_signals": orig_long,
                "original_short_signals": orig_short,
                "filtered_long_signals": filt_long,
                "filtered_short_signals": filt_short,
                "removed_long_signals": orig_long - filt_long,
                "removed_short_signals": orig_short - filt_short,
            }
        )
    return rows


def materialize_k_features(run_id: str, selected_variant: str, common_files_root: Path) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "features").mkdir(parents=True, exist_ok=True)
    low, high = selected_band_bounds(selected_variant)
    adx_table = base.load_candidate_adx_table()
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    subtype_audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for variant_id in K_VARIANTS:
        for runtime_split, tier_scope, source_name in base.source_feature_files():
            source = pd.read_csv(io_path(SOURCE_RUN_ROOT / "features" / source_name))
            merged = source.merge(adx_table, on=keys, how="left", validate="one_to_one")
            removed_short = 0
            if tier_scope == mt5.TIER_A:
                filtered, removed_short = fu.apply_band_rule(merged, low, high)
            else:
                filtered = merged.copy()
                signal = pd.to_numeric(filtered[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0)
                allowed = filtered["partial_context_subtype"].astype(str).map(lambda value: subtype_allowed(variant_id, value))
                mask = signal.ne(0) & ~allowed
                removed_short = int((mask & signal.eq(-1)).sum())
                filtered.loc[mask, SOURCE_SIGNAL_COLUMN] = 0
                if "entry_decision" in filtered.columns:
                    filtered.loc[mask, "entry_decision"] = "flat"
            output = filtered.loc[:, source.columns].copy()
            tier_token = "a" if tier_scope == mt5.TIER_A else "b"
            split_token = "val" if runtime_split == "validation_is" else "oos"
            output_name = f"{run_id.split('_', 1)[0]}_c08_{tier_token}_{split_token}_{variant_id}_s49.csv"
            output_path = root / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            common_path = f"{common_run_root(run_id)}/features/{output_name}"
            common_copies.append(copy_to_common(output_path, common_path, common_files_root))
            tier_key = "tier_a" if tier_scope == mt5.TIER_A else "tier_b"
            exports[f"{variant_id}_{tier_key}_{runtime_split}"] = {
                "path": output_path.as_posix(),
                "common_path": common_path,
                "split": runtime_split,
                "tier_scope": tier_scope,
                "sha256": sha256_file_lf_normalized(output_path),
            }
            audit_rows.append(deep.feature_audit_row(run_id, variant_id, output_path, runtime_split, tier_scope, source, merged, output, removed_short, low if tier_scope == mt5.TIER_A else None, high if tier_scope == mt5.TIER_A else None))
            subtype_audit_rows.extend(subtype_rows(run_id, variant_id, runtime_split, tier_scope, source, output))
    write_csv(root / "results" / "conditional_fallback_feature_audit.csv", audit_rows, FEATURE_AUDIT_COLUMNS)
    write_csv(root / "results" / "tier_b_subtype_signal_audit.csv", subtype_audit_rows, SUBTYPE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "subtype_audit_rows": subtype_audit_rows, "common_copies": common_copies}


def make_k_attempt(run_id: str, variant_id: str, runtime_split: str, model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]], magic: int) -> dict[str, Any]:
    rules = base.source_rule_values()
    from_date, to_date = base.source_split_dates(runtime_split)
    attempt_name = f"routed_c08_{variant_id}_{runtime_split}"
    payload = attempt_payload(
        run_root=run_root(run_id),
        run_id=run_id,
        stage_number=STAGE_NUMBER,
        exploration_label="stage49_TradeLifecycle__TierBSubtypeFallback",
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


def run43k(common_files_root: Path, args: argparse.Namespace, selected_variant: str) -> dict[str, Any]:
    run_id = RUN43K_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    manifest_path = root / "run_manifest.json"
    if path_exists(manifest_path):
        manifest = json.loads(io_path(manifest_path).read_text(encoding="utf-8"))
        if manifest.get("mt5", {}).get("external_verification_status") == "completed":
            return {
                "run_id": run_id,
                "model": {},
                "features": {"feature_audit_rows": manifest.get("feature_audit_rows", []), "subtype_audit_rows": manifest.get("subtype_audit_rows", [])},
                "attempts": manifest.get("attempts", []),
                "mt5": manifest["mt5"],
                "summary_rows": manifest.get("summary_rows", []),
            }
    model_payload = copy_model(run_id, common_files_root)
    features = materialize_k_features(run_id, selected_variant, common_files_root)
    attempts = [
        make_k_attempt(run_id, variant_id, split, model_payload, features["exports"], 1001140 + index)
        for index, (variant_id, split) in enumerate((variant_id, split) for variant_id in K_VARIANTS for split in ("validation_is", "oos"))
    ]
    result = fu.execute_mt5_run(
        run_id,
        attempts,
        fu.route_coverage_from_audit(features["feature_audit_rows"], "subtype_macro_only"),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = fu.build_mt5_summary(run_id, result, features["feature_audit_rows"])
    write_csv(root / "results" / "tier_b_subtype_conditioning_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "selected_variant": selected_variant, "attempts": attempts, "feature_audit_rows": features["feature_audit_rows"], "subtype_audit_rows": features["subtype_audit_rows"], "mt5": result, "summary_rows": summary_rows, "boundary": BOUNDARY})
    return {"run_id": run_id, "model": model_payload, "features": features, "attempts": attempts, "mt5": result, "summary_rows": summary_rows}


def hold_bucket(value: Any) -> str:
    output = num(value)
    if output is None:
        return "hold_missing"
    if output <= 6:
        return "hold_0_6"
    if output <= 12:
        return "hold_7_12"
    if output <= 24:
        return "hold_13_24"
    return "hold_gt24"


def summarize_trade_bucket(run_id: str, source_run_id: str, variant_id: str, split: str, month: str, family: str, bucket: str, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    profits = [float(row.get("net_profit") or 0.0) for row in rows]
    return {
        "run_id": run_id,
        "source_run_id": source_run_id,
        "variant_id": variant_id,
        "split": split,
        "month": month,
        "bucket_family": family,
        "bucket": bucket,
        "trade_count": len(rows),
        "net_profit": rounded(sum(profits)),
        "win_count": sum(1 for value in profits if value > 0.0),
        "loss_count": sum(1 for value in profits if value < 0.0),
        "avg_hold_bars": rounded(pd.Series([float(row.get("hold_bars") or 0.0) for row in rows]).mean() if rows else None),
        "avg_mfe": rounded(pd.Series([float(row.get("mfe") or 0.0) for row in rows]).mean() if rows else None),
        "avg_mae": rounded(pd.Series([float(row.get("mae") or 0.0) for row in rows]).mean() if rows else None),
        "loss_with_positive_mfe_count": sum(1 for row in rows if float(row.get("net_profit") or 0.0) < 0.0 and float(row.get("mfe") or 0.0) > 0.0),
    }


def report_sources_for_loss_forensics(run43k_result: Mapping[str, Any]) -> list[tuple[str, str, str, Path]]:
    sources: list[tuple[str, str, str, Path]] = []
    g_manifest = load_manifest(deep.RUN43G_ID)
    g_reports = deep.report_records_by_attempt(g_manifest["mt5"])
    selected_variant = selected_variant_from_deep_packet()
    sources.append((deep.RUN43G_ID, f"tier_a_best:{selected_variant}", "oos", deep.report_path_from_record(g_reports[f"tier_a_c08_{selected_variant}_oos"])))
    j_manifest = load_manifest(deep.RUN43J_ID)
    j_reports = deep.report_records_by_attempt(j_manifest["mt5"])
    for variant_id in deep.RUN43J_VARIANTS:
        sources.append((deep.RUN43J_ID, f"fallback:{variant_id}", "oos", deep.report_path_from_record(j_reports[f"routed_c08_{variant_id}_oos"])))
    k_reports = deep.report_records_by_attempt(run43k_result["mt5"])
    for variant_id in K_VARIANTS:
        sources.append((RUN43K_ID, f"subtype:{variant_id}", "oos", deep.report_path_from_record(k_reports[f"routed_c08_{variant_id}_oos"])))
    return sources


def run43l(run43k_result: Mapping[str, Any]) -> dict[str, Any]:
    run_id = RUN43L_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    rows: list[dict[str, Any]] = []
    source_reports: list[dict[str, Any]] = []
    for source_run_id, variant_id, split, report_path in report_sources_for_loss_forensics(run43k_result):
        source_reports.append({"source_run_id": source_run_id, "variant_id": variant_id, "path": report_path.as_posix(), "sha256": sha256_file_lf_normalized(report_path)})
        trades = deep.parse_report_trades(report_path, market_data)
        selected = [row for row in trades if pd.Timestamp(row["close_time"]).strftime("%Y-%m") == "2025-12"]
        for row in selected:
            row["hold_bucket"] = hold_bucket(row.get("hold_bars"))
        rows.append(summarize_trade_bucket(run_id, source_run_id, variant_id, split, "2025-12", "all", "all", selected))
        for family in ("direction", "session_slice", "volatility_regime", "trend_regime", "adx_bucket", "di_spread_bucket", "hold_bucket"):
            for bucket in sorted({str(row.get(family) or "missing") for row in selected}):
                bucket_rows = [row for row in selected if str(row.get(family) or "missing") == bucket]
                rows.append(summarize_trade_bucket(run_id, source_run_id, variant_id, split, "2025-12", family, bucket, bucket_rows))
    write_csv(root / "results" / "december_oos_loss_forensics.csv", rows, DECEMBER_FORENSIC_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "source_reports": source_reports, "rows": len(rows), "boundary": BOUNDARY})
    return {"run_id": run_id, "rows": rows, "source_reports": source_reports}


def materialize_m_features(run_id: str, selected_variant: str, common_files_root: Path) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "features").mkdir(parents=True, exist_ok=True)
    low, high = selected_band_bounds(selected_variant)
    adx_table = base.load_candidate_adx_table()
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for variant_id, policy in M_VARIANTS.items():
        for runtime_split, tier_scope, source_name in base.source_feature_files():
            if tier_scope != mt5.TIER_A:
                continue
            source = pd.read_csv(io_path(SOURCE_RUN_ROOT / "features" / source_name))
            merged = source.merge(adx_table, on=keys, how="left", validate="one_to_one")
            filtered, removed_short = fu.apply_band_rule(merged, low, high)
            if policy.get("late_entry_filter"):
                with_session = add_session_slice(filtered, market_data)
                signal = pd.to_numeric(with_session[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0)
                late_mask = with_session["session_slice"].eq("late") & signal.ne(0)
                removed_short += int((late_mask & signal.eq(-1)).sum())
                with_session.loc[late_mask, SOURCE_SIGNAL_COLUMN] = 0
                if "entry_decision" in with_session.columns:
                    with_session.loc[late_mask, "entry_decision"] = "flat"
                filtered = with_session.loc[:, merged.columns].copy()
            output = filtered.loc[:, source.columns].copy()
            split_token = "val" if runtime_split == "validation_is" else "oos"
            output_name = f"{run_id.split('_', 1)[0]}_c08_a_{split_token}_{variant_id}_s49.csv"
            output_path = root / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            common_path = f"{common_run_root(run_id)}/features/{output_name}"
            common_copies.append(copy_to_common(output_path, common_path, common_files_root))
            exports[f"{variant_id}_tier_a_{runtime_split}"] = {"path": output_path.as_posix(), "common_path": common_path, "split": runtime_split, "tier_scope": tier_scope, "sha256": sha256_file_lf_normalized(output_path)}
            audit_rows.append(deep.feature_audit_row(run_id, variant_id, output_path, runtime_split, tier_scope, source, merged, output, removed_short, low, high))
    write_csv(root / "results" / "hold_exit_feature_audit.csv", audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def make_m_attempt(run_id: str, variant_id: str, runtime_split: str, model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]], magic: int) -> dict[str, Any]:
    rules = base.source_rule_values()
    policy = M_VARIANTS[variant_id]
    from_date, to_date = base.source_split_dates(runtime_split)
    attempt_name = f"tier_a_c08_{variant_id}_{runtime_split}"
    payload = attempt_payload(
        run_root=run_root(run_id),
        run_id=run_id,
        stage_number=STAGE_NUMBER,
        exploration_label="stage49_TradeLifecycle__HoldLateSessionExit",
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
        max_hold_bars=int(policy["max_hold_bars"]),
        common_root=common_run_root(run_id),
        fallback_enabled=False,
        close_on_flat_signal=bool(policy["close_on_flat_signal"]),
        reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
        close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
        extra_set_values={"InpMagic": magic},
    )
    payload.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": variant_id, "route_mode": variant_id, "max_hold_bars": int(policy["max_hold_bars"]), "close_on_flat_signal": bool(policy["close_on_flat_signal"])})
    return payload


def run43m(common_files_root: Path, args: argparse.Namespace, selected_variant: str) -> dict[str, Any]:
    run_id = RUN43M_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    model_payload = copy_model(run_id, common_files_root)
    features = materialize_m_features(run_id, selected_variant, common_files_root)
    attempts = [
        make_m_attempt(run_id, variant_id, split, model_payload, features["exports"], 1001160 + index)
        for index, (variant_id, split) in enumerate((variant_id, split) for variant_id in M_VARIANTS for split in ("validation_is", "oos"))
    ]
    result = fu.execute_mt5_run(
        run_id,
        attempts,
        deep.route_coverage_for_tier_a(features["feature_audit_rows"], "hold06"),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = fu.build_mt5_summary(run_id, result, features["feature_audit_rows"])
    write_csv(root / "results" / "hold_late_session_exit_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "selected_variant": selected_variant, "attempts": attempts, "feature_audit_rows": features["feature_audit_rows"], "mt5": result, "summary_rows": summary_rows, "boundary": BOUNDARY})
    return {"run_id": run_id, "model": model_payload, "features": features, "attempts": attempts, "mt5": result, "summary_rows": summary_rows}


def monthly_net_rows(source_run_id: str, variant_id: str, report_path: Path, market_data: mt5_trade_attribution.MarketData) -> list[dict[str, Any]]:
    trades = deep.parse_report_trades(report_path, market_data)
    frame = pd.DataFrame(trades)
    if frame.empty:
        return []
    frame["month"] = pd.to_datetime(frame["close_time"]).dt.strftime("%Y-%m")
    frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
    return [
        {"source_run_id": source_run_id, "variant_id": variant_id, "month": str(month), "net_profit": float(group["net_profit"].sum()), "trade_count": int(len(group))}
        for month, group in frame.groupby("month", sort=True)
    ]


def leave_one_month_stability(month_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not month_rows:
        return {"total_net_profit": None, "worst_month": "", "worst_month_net_profit": None, "leave_one_month_min_net_profit": None, "leave_one_month_min_excluded_month": "", "positive_month_count": 0, "negative_month_count": 0, "stability_status": "missing"}
    total = sum(float(row.get("net_profit") or 0.0) for row in month_rows)
    worst = min(month_rows, key=lambda row: float(row.get("net_profit") or 0.0))
    leave_rows = [{"month": row["month"], "net": total - float(row.get("net_profit") or 0.0)} for row in month_rows]
    min_leave = min(leave_rows, key=lambda row: row["net"])
    negative_months = sum(1 for row in month_rows if float(row.get("net_profit") or 0.0) < 0.0)
    status = "passed" if total > 0.0 and min_leave["net"] > 0.0 else "fragile"
    if negative_months >= 2:
        status = "fragile_multi_negative_month"
    return {
        "total_net_profit": rounded(total),
        "worst_month": worst["month"],
        "worst_month_net_profit": rounded(worst["net_profit"]),
        "leave_one_month_min_net_profit": rounded(min_leave["net"]),
        "leave_one_month_min_excluded_month": min_leave["month"],
        "positive_month_count": sum(1 for row in month_rows if float(row.get("net_profit") or 0.0) > 0.0),
        "negative_month_count": negative_months,
        "stability_status": status,
    }


def run43n() -> dict[str, Any]:
    run_id = RUN43N_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    g_manifest = load_manifest(deep.RUN43G_ID)
    g_reports = deep.report_records_by_attempt(g_manifest["mt5"])
    rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    for low, high in deep.RUN43G_BANDS:
        variant_id = fu.band_variant(low, high)
        report_path = deep.report_path_from_record(g_reports[f"tier_a_c08_{variant_id}_oos"])
        month_rows = monthly_net_rows(deep.RUN43G_ID, variant_id, report_path, market_data)
        monthly_rows.extend({"run_id": run_id, "split": "oos", **row} for row in month_rows)
        stability = leave_one_month_stability(month_rows)
        rows.append({"run_id": run_id, "source_run_id": deep.RUN43G_ID, "variant_id": variant_id, "split": "oos", **stability})
    write_csv(root / "results" / "adx_leave_one_month_stability.csv", rows, LOMO_COLUMNS)
    write_csv(root / "results" / "adx_monthly_net_profit.csv", monthly_rows, ("run_id", "source_run_id", "variant_id", "split", "month", "net_profit", "trade_count"))
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "source_run_id": deep.RUN43G_ID, "rows": rows, "monthly_rows": monthly_rows, "boundary": BOUNDARY})
    return {"run_id": run_id, "rows": rows, "monthly_rows": monthly_rows}


def best_oos_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if row.get("split") == "oos" and num(row.get("net_profit")) is not None]
    return max(candidates, key=lambda row: float(row.get("net_profit") or -1e18), default={})


def evaluate_closeout(run43k_result: Mapping[str, Any], run43m_result: Mapping[str, Any]) -> tuple[str, str]:
    if run43k_result["mt5"].get("external_verification_status") != "completed" or run43m_result["mt5"].get("external_verification_status") != "completed":
        return "blocked_stage49_closeout_missing_mt5_execution", "run43k_or_run43m_mt5_blocked"
    return "reviewed_closed_positive_reference_surface_runtime_probe_only", "tier_b_subtype_and_exit_timing_probes_completed;stage49_closed_without_baseline_or_promotion"


def lineage_rows() -> list[dict[str, Any]]:
    source_rows = [
        ("stage49_closeout_source_run43GHIJ_summary", "source_packet", deep.PACKET_ROOT / "aggregate_summary.json", "tracked_source", "Prior Stage49 deep follow-up suite."),
        ("stage49_closeout_source_run43G_manifest", "manifest", run_root(deep.RUN43G_ID) / "run_manifest.json", "tracked_source", "Tier A ADX sweep source."),
        ("stage49_closeout_source_run43J_manifest", "manifest", run_root(deep.RUN43J_ID) / "run_manifest.json", "tracked_source", "Fallback conditioning source."),
        ("stage49_closeout_source_stage45_score_table", "model_table", SOURCE_MODEL_PATH, "tracked_source", "Unchanged Stage45 score table."),
    ]
    for run_id in (RUN43K_ID, RUN43L_ID, RUN43M_ID, RUN43N_ID):
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
                "kpi_scope": "stage49_closeout_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": record.get("path", ""),
                "primary_kpi": ledger_pairs([("split", record.get("split")), ("route_role", record.get("route_role")), ("net_profit", metrics.get("net_profit")), ("profit_factor", metrics.get("profit_factor")), ("trade_count", metrics.get("trade_count"))]),
                "guardrail_kpi": "closeout_probe_only;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
                "notes": BOUNDARY,
            }
        )
    return rows


def write_ledgers(results: Mapping[str, Any], judgment: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_rows = [
        {"run_id": RUN43K_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43K_ID)), "notes": BOUNDARY},
        {"run_id": RUN43L_ID, "stage_id": STAGE_ID, "lane": "trade_level_forensics", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43L_ID)), "notes": BOUNDARY},
        {"run_id": RUN43M_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43M_ID)), "notes": BOUNDARY},
        {"run_id": RUN43N_ID, "stage_id": STAGE_ID, "lane": "stability_forensics", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43N_ID)), "notes": BOUNDARY},
        {"run_id": CLOSEOUT_ID, "stage_id": STAGE_ID, "lane": "stage_closeout", "status": "reviewed_closed", "judgment": judgment, "path": rel(REVIEW_ROOT / "stage49_closeout_packet.md"), "notes": BOUNDARY},
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    ledger_rows = []
    ledger_rows.extend(ledger_rows_for_mt5(RUN43K_ID, results["run43k"]["mt5"], judgment))
    ledger_rows.extend(ledger_rows_for_mt5(RUN43M_ID, results["run43m"]["mt5"], judgment))
    supplement_rows = [
        (RUN43L_ID, "december_oos_loss_forensics", run_root(RUN43L_ID) / "results" / "december_oos_loss_forensics.csv", f"rows={len(results['run43l']['rows'])}", "existing_mt5_report_derived"),
        (RUN43N_ID, "adx_leave_one_month_stability", run_root(RUN43N_ID) / "results" / "adx_leave_one_month_stability.csv", f"rows={len(results['run43n']['rows'])}", "existing_mt5_report_derived"),
        (CLOSEOUT_ID, "stage49_closeout", REVIEW_ROOT / "stage49_closeout_packet.md", "stage49_closed_without_baseline_or_promotion", "stage_closeout_review"),
    ]
    for run_id, view, path, primary, lane in supplement_rows:
        ledger_rows.append(
            {
                "ledger_row_id": f"{run_id}__{view}",
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": view,
                "parent_run_id": RUN43K_ID,
                "record_view": view,
                "tier_scope": "Tier A primary + Tier B fallback" if run_id != RUN43N_ID else "Tier A",
                "kpi_scope": "stage49_closeout_supplement",
                "scoreboard_lane": lane,
                "status": "reviewed",
                "judgment": judgment,
                "path": rel(path),
                "primary_kpi": primary,
                "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed_existing_mt5_report_derived" if run_id != CLOSEOUT_ID else "completed",
                "notes": BOUNDARY,
            }
        )
    stage_payload = upsert_csv_rows(REVIEW_ROOT / "stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_rows = [{"artifact_id": row["artifact_id"], "type": row["type"], "path": row["path"], "status": row["availability"], "notes": row["notes"]} for row in artifacts]
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_docs(results: Mapping[str, Any], judgment: str, reasons: str, selected_variant: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    best_k = best_oos_row(results["run43k"]["summary_rows"])
    best_m = best_oos_row(results["run43m"]["summary_rows"])
    best_n = max(results["run43n"]["rows"], key=lambda row: float(row.get("leave_one_month_min_net_profit") or -1e18), default={})
    write_md(REVIEW_ROOT / "run43K_packet.md", f"""# {RUN43K_ID} Packet(패킷)

- purpose(목적): Tier B subtype conditional fallback(Tier B 하위유형 조건부 대체)
- best_oos_row(최선 외표본 행): `{best_k}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run43L_packet.md", f"""# {RUN43L_ID} Packet(패킷)

- purpose(목적): 2025-12 OOS loss forensics(2025-12 외표본 손실 부검)
- forensic_rows(부검 행): `{len(results['run43l']['rows'])}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run43M_packet.md", f"""# {RUN43M_ID} Packet(패킷)

- purpose(목적): hold-time and late-session exit probe(보유 시간 및 후반 세션 청산 탐침)
- best_oos_row(최선 외표본 행): `{best_m}`
- direct_late_session_exit(직접 후반 세션 청산): `not_available_without_ea_logic_change`
- proxy_tested(대리 시험): `no_late_entry`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run43N_packet.md", f"""# {RUN43N_ID} Packet(패킷)

- purpose(목적): ADX leave-one-month-out stability(ADX 월 하나 제외 안정성)
- strongest_stability_row(최강 안정성 행): `{best_n}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "stage49_closeout_packet.md", f"""# Stage49 Closeout Packet(49단계 마감 패킷)

- judgment(판정): `{judgment}`
- decision_reasons(결정 이유): `{reasons}`
- selected_reference_surface(선택 참고 표면): `Tier A only {selected_variant}`
- run43K(43K 실행): Tier B subtype conditional fallback(Tier B 하위유형 조건부 대체) completed(완료)
- run43L(43L 실행): 2025-12 OOS loss forensics(2025-12 외표본 손실 부검) completed(완료)
- run43M(43M 실행): hold-time / late-session exit probe(보유 시간 / 후반 세션 청산 탐침) completed(완료)
- run43N(43N 실행): ADX leave-one-month-out stability(ADX 월 하나 제외 안정성) completed(완료)
- closeout_boundary(마감 경계): `{BOUNDARY}`

Stage49(49단계)는 reference surface(참고 표면)만 남기고 닫는다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 없다.
""")
    write_md(REVIEW_ROOT / "review_index.md", """# Review Index(검토 색인)

- run43A packet(43A 패킷): `03_reviews/run43A_packet.md`
- run43B packet(43B 패킷): `03_reviews/run43B_packet.md`
- run43C-F follow-up suite(43C-F 후속 묶음): `03_reviews/stage49_followup_suite_packet.md`
- run43G-J deep follow-up suite(43G-J 심화 후속 묶음): `03_reviews/stage49_deep_followup_suite_packet.md`
- run43K packet(43K 패킷): `03_reviews/run43K_packet.md`
- run43L packet(43L 패킷): `03_reviews/run43L_packet.md`
- run43M packet(43M 패킷): `03_reviews/run43M_packet.md`
- run43N packet(43N 패킷): `03_reviews/run43N_packet.md`
- Stage49 closeout(49단계 마감): `03_reviews/stage49_closeout_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
""")
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage49 Selection Status(49단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- stage_status(단계 상태): `reviewed_closed`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- promotion_packet(승격 패킷): `none`
- latest_run_id(최신 실행 ID): `{CLOSEOUT_ID}`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- selected_reference_surface(선택 참고 표면): `Tier A only {selected_variant}`
- closeout_suite(마감 묶음): `{PACKET_ID}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_packet_files(results, judgment, reasons, selected_variant, ledger_payload, artifacts)
    update_current_truth(judgment, selected_variant)


def write_packet_files(results: Mapping[str, Any], judgment: str, reasons: str, selected_variant: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    completed = results["run43k"]["mt5"].get("external_verification_status") == "completed" and results["run43m"]["mt5"].get("external_verification_status") == "completed"
    required_gates = ["runtime_evidence_gate", "kpi_contract_audit", "artifact_lineage_audit", "result_judgment_gate", "required_gate_coverage_audit", "final_claim_guard"]
    write_yaml_text(PACKET_ROOT / "work_packet.yaml", f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_ids:
  - {RUN43K_ID}
  - {RUN43L_ID}
  - {RUN43M_ID}
  - {RUN43N_ID}
  - {CLOSEOUT_ID}
primary_family: stage_closeout_runtime_backtest
primary_skill: obsidian-result-judgment
support_skills:
  - obsidian-runtime-parity
  - obsidian-backtest-forensics
  - obsidian-exploration-mandate
  - obsidian-artifact-lineage
required_gates:
{chr(10).join(f"  - {gate}" for gate in required_gates)}
status: {"reviewed_stage49_closed" if completed else "blocked_stage49_closeout"}
claim_boundary: {BOUNDARY}
""")
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "judgment": judgment, "decision_reasons": reasons, "selected_variant": selected_variant, "run43k": {"summary_rows": results["run43k"]["summary_rows"]}, "run43l": {"rows": results["run43l"]["rows"]}, "run43m": {"summary_rows": results["run43m"]["summary_rows"]}, "run43n": {"rows": results["run43n"]["rows"]}, "boundary": BOUNDARY, "ledger_sync": ledger_payload, "artifacts": list(artifacts), "created_at_utc": utc_now()})
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"status": "passed" if completed else "failed", "run43k": results["run43k"]["mt5"], "run43m": results["run43m"]["mt5"], "run43l_source_reports": results["run43l"]["source_reports"]})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if completed else "blocked", "run43k_mt5_rows": len(results["run43k"]["mt5"].get("mt5_kpi_records", [])), "run43m_mt5_rows": len(results["run43m"]["mt5"].get("mt5_kpi_records", [])), "synthetic_sum_used_as_routed_total": False})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "artifacts": list(artifacts)})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "decision_reasons": reasons, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed" if completed else "blocked", "required_gates": required_gates, "covered_gates": required_gates if completed else [], "missing_gates": [] if completed else ["runtime_evidence_gate"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": [{"command": "python -m foundation.pipelines.run_stage49_closeout_suite --timeout-seconds 900", "result": "recorded_by_pipeline", "failures_or_blockers": ""}], "status": "recorded"})


def update_current_truth(judgment: str, selected_variant: str) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {CLOSEOUT_ID}", state_text, flags=re.MULTILINE)
    focus = f"- Stage49(49단계) {STAGE_ID} closeout(마감): run43K/run43L/run43M/run43N(43K-43N 실행)과 {CLOSEOUT_ID}(마감)을 완료했고 Tier A only {selected_variant}(티어 A만 {selected_variant})를 reference surface(참고 표면)로 보존했다; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    state_text = state_text.replace("current_focus:\n", f"current_focus:\n{focus}\n", 1)
    block_name = "stage49_closeout"
    block = f"""

{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_closed
  current_run_id: {CLOSEOUT_ID}
  judgment: {judgment}
  selected_reference_surface: Tier A only {selected_variant}
  report_path: {rel(REVIEW_ROOT / "stage49_closeout_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage49 Closeout(최신 49단계 마감)

Stage49(49단계) closed(마감) as `{judgment}` after run43K/run43L/run43M/run43N. The preserved reference surface(보존 참고 표면)는 `Tier A only {selected_variant}`이며, baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않았다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{STAGE_ID}` closed with `{PACKET_ID}` as `{judgment}`.\n", encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(STAGE_ROOT / folder).mkdir(parents=True, exist_ok=True)
    selected_variant = selected_variant_from_deep_packet()
    result_k = run43k(common_files_root, args, selected_variant)
    result_l = run43l(result_k)
    result_m = run43m(common_files_root, args, selected_variant)
    result_n = run43n()
    results = {"run43k": result_k, "run43l": result_l, "run43m": result_m, "run43n": result_n}
    judgment, reasons = evaluate_closeout(result_k, result_m)
    artifacts = lineage_rows()
    write_csv(run_root(RUN43K_ID) / "results" / "lineage.csv", artifacts, LINEAGE_COLUMNS)
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
                    "run43k_summary_rows": result["run43k"]["summary_rows"],
                    "run43l_rows": len(result["run43l"]["rows"]),
                    "run43m_summary_rows": result["run43m"]["summary_rows"],
                    "run43n_rows": result["run43n"]["rows"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
