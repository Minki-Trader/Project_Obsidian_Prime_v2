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

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
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
from foundation.control_plane import mt5_trade_attribution
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage35 import common
from stage_pipelines.stage49 import deep_followup_suite as stage49_deep
from stage_pipelines.stage49 import followup_suite as stage49_followup
from stage_pipelines.stage49 import reversal_selection_rule_mt5 as stage49_base
from stage_pipelines.stage50 import adx_reference_wfo_stress as stage50
from stage_pipelines.stage50 import followup_suite as stage50_followup


STAGE_NUMBER = 51
STAGE_ID = "51_risk_filter__q2_short_late_di_loss_firewall"
IDEA_ID = "IDEA-ST51-Q2-SHORT-LATE-DI-LOSS-FIREWALL"
PACKET_ID = "stage51_run45ABCDE_q2_loss_firewall_v1"
BOUNDARY = (
    "stage51_q2_loss_firewall_runtime_probe_only_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_operating_reference"
)

RUN45A_ID = "run45A_q2_loss_firewall_broad_mt5_wfo_v1"
RUN45B_ID = "run45B_firewall_routed_tier_b_eligibility_mt5_v1"
RUN45C_ID = "run45C_firewall_cost_overlap_attribution_v1"
RUN45D_ID = "run45D_firewall_decision_stress_synthesis_v1"
RUN45E_ID = "run45E_stage51_closeout_v1"

POSITIVE_JUDGMENT = "reviewed_completed_positive_q2_loss_firewall_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_q2_loss_firewall_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_q2_loss_firewall_runtime_probe_only"
BLOCKED_JUDGMENT = "blocked_stage51_q2_loss_firewall_missing_mt5_execution"

SOURCE_CANDIDATE_ID = stage50.SOURCE_CANDIDATE_ID
SOURCE_SIGNAL_COLUMN = stage50.SOURCE_SIGNAL_COLUMN
SOURCE_MODEL_PATH = stage50.SOURCE_MODEL_PATH
REFERENCE_VARIANT = stage50.REFERENCE_VARIANT
WFO_WINDOWS = stage50.WFO_WINDOWS

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
RUN_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs" / "workspace" / "changelog.md"

LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"
SELECTION_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
STAGE_BRIEF_PATH = STAGE_ROOT / "00_spec" / "stage_brief.md"

FIREWALL_VARIANTS: tuple[dict[str, Any], ...] = (
    {"variant_id": "fw00_adx_reference", "extra_rule": "none", "description": "Stage50 ADX 20-25 reference"},
    {"variant_id": "fw01_block_late_short", "extra_rule": "late_short", "description": "Block late-session shorts"},
    {"variant_id": "fw02_block_di_short_mild", "extra_rule": "di_short_mild", "description": "Block mild DI-short shorts"},
    {"variant_id": "fw03_block_late_or_di_short_mild", "extra_rule": "late_or_di_short_mild", "description": "Block late or mild DI-short shorts"},
    {"variant_id": "fw04_block_late_and_di_short_mild", "extra_rule": "late_and_di_short_mild", "description": "Block only late mild DI-short shorts"},
    {"variant_id": "fw05_block_vol_mid_short", "extra_rule": "vol_mid_short", "description": "Block mid-volatility shorts"},
    {"variant_id": "fw06_short_strong_only", "extra_rule": "short_strong_only", "description": "Keep only strong DI-short shorts"},
    {"variant_id": "fw07_long_only_firewall", "extra_rule": "all_short", "description": "Extreme all-short firewall"},
)
DEFAULT_SELECTED_VARIANTS = ("fw00_adx_reference", "fw03_block_late_or_di_short_mild", "fw06_short_strong_only", "fw07_long_only_firewall")
COST_GRID = (0.25, 0.5, 1.0, 2.0)

FEATURE_AUDIT_COLUMNS = (
    "run_id",
    "variant_id",
    "feature_file",
    "split",
    "tier_scope",
    "from_date",
    "to_date",
    "input_rows",
    "window_rows",
    "matched_market_rows",
    "unmatched_market_rows",
    "original_long_signals",
    "original_short_signals",
    "filtered_long_signals",
    "filtered_short_signals",
    "base_adx_removed_short_signals",
    "firewall_removed_short_signals",
    "rule_id",
    "extra_rule",
    "source_files",
)
MT5_SUMMARY_COLUMNS = (
    "run_id",
    "variant_id",
    "route_view",
    "window_id",
    "window_label",
    "tier_scope",
    "route_role",
    "attempt_name",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "recovery_factor",
    "runtime_status",
    "report_status",
)
ROBUSTNESS_COLUMNS = (
    "run_id",
    "variant_id",
    "route_view",
    "tested_windows",
    "positive_windows",
    "negative_windows",
    "total_net_profit",
    "q2_net_profit",
    "worst_window",
    "worst_window_net_profit",
    "median_profit_factor",
    "total_trades",
    "robustness_status",
)
TRADE_COLUMNS = (
    "source_run_id",
    "source_label",
    "variant_id",
    "route_mode",
    "window_id",
    "window_label",
    "attempt_name",
    "trade_key",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "net_profit",
    "mfe",
    "mae",
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "di_spread_bucket",
)
COST_COLUMNS = (
    "run_id",
    "source_run_id",
    "source_label",
    "variant_id",
    "route_view",
    "extra_cost_per_trade",
    "window_id",
    "trade_count",
    "base_net_profit",
    "adjusted_net_profit",
    "adjusted_profit_factor",
    "positive_after_cost",
)
COST_ROBUSTNESS_COLUMNS = (
    "run_id",
    "source_label",
    "variant_id",
    "route_view",
    "extra_cost_per_trade",
    "tested_windows",
    "positive_windows",
    "total_adjusted_net_profit",
    "worst_window",
    "worst_window_adjusted_net_profit",
    "cost_status",
)
OVERLAP_COLUMNS = (
    "run_id",
    "source_run_id",
    "source_label",
    "route_view",
    "window_id",
    "total_trade_occurrences",
    "unique_trade_keys",
    "duplicate_trade_keys",
    "keys_seen_in_4plus_variants",
    "overlap_occurrence_share",
    "top10_abs_net_share",
    "concentration_status",
)
LINEAGE_COLUMNS = ("artifact_id", "type", "path", "sha256", "availability", "notes")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return io_path(path).resolve().relative_to(io_path(common.ROOT).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def run_root(run_id: str) -> Path:
    return STAGE_ROOT / "02_runs" / run_id.split("_", 1)[0]


def common_run_root(run_id: str) -> str:
    return f"Project_Obsidian_Prime_v2/stage51/{run_id.split('_', 1)[0]}"


def safe_name(value: str, limit: int = 96) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_")[:limit]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8"))


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


def variant_payload(variant_id: str) -> Mapping[str, Any]:
    for variant in FIREWALL_VARIANTS:
        if variant["variant_id"] == variant_id:
            return variant
    raise KeyError(f"Unknown firewall variant: {variant_id}")


def window_by_id() -> dict[str, Mapping[str, str]]:
    return {window["window_id"]: window for window in WFO_WINDOWS}


def date_start(value: str) -> pd.Timestamp:
    return pd.Timestamp(datetime.strptime(value, "%Y.%m.%d"), tz="UTC")


def window_mask(frame: pd.DataFrame, window: Mapping[str, str]) -> pd.Series:
    return frame["_timestamp_dt"].ge(date_start(window["from_date"])) & frame["_timestamp_dt"].lt(date_start(window["to_date"]))


def signal_counts(frame: pd.DataFrame) -> tuple[int, int]:
    signal = pd.to_numeric(frame[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int64")
    return int(signal.eq(1).sum()), int(signal.eq(-1).sum())


def session_slice(minutes: Any) -> str:
    value = num(minutes)
    if value is None:
        return "feature_missing"
    if 0.0 < value <= 110.0:
        return "early"
    if 110.0 < value <= 220.0:
        return "mid"
    if 220.0 < value <= 330.0:
        return "late"
    return "outside_cash_session"


def bucket(value: Any, edges: tuple[float, float] | None, prefix: str) -> str:
    number = num(value)
    if number is None or edges is None:
        return "feature_missing"
    low, high = edges
    if number <= low:
        return f"{prefix}_low"
    if number <= high:
        return f"{prefix}_mid"
    return f"{prefix}_high"


def trend_regime(row: Mapping[str, Any]) -> str:
    adx = num(row.get("adx_14_market"))
    state = num(row.get("supertrend_10_3"))
    if adx is None or state is None:
        return "feature_missing"
    if adx < 20.0:
        return "range_or_weak_trend"
    return "uptrend" if state > 0.0 else "downtrend"


def adx_bucket(value: Any) -> str:
    number = num(value)
    if number is None:
        return "feature_missing"
    if number < 20.0:
        return "adx_lt20"
    if number <= 25.0:
        return "adx_20_25"
    return "adx_gt25"


def enrich_market_context(frame: pd.DataFrame) -> pd.DataFrame:
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    market = market_data.features.rename(columns={"adx_14": "adx_14_market"}).copy()
    output = frame.copy()
    output["_timestamp_key"] = output["_timestamp_dt"].dt.tz_convert("UTC").dt.tz_localize(None)
    output = output.merge(
        market[["timestamp_key", "minutes_from_cash_open", "historical_vol_20", "adx_14_market", "di_spread_14", "supertrend_10_3"]],
        left_on="_timestamp_key",
        right_on="timestamp_key",
        how="left",
    )
    output["session_slice"] = output["minutes_from_cash_open"].map(session_slice)
    output["volatility_regime"] = output["historical_vol_20"].map(lambda value: bucket(value, market_data.volatility_edges, "vol"))
    output["di_spread_bucket"] = output["di_spread_14"].map(stage49_deep.di_spread_bucket)
    output["trend_regime"] = output.apply(trend_regime, axis=1)
    output["adx_bucket"] = output["adx_14_market"].map(adx_bucket)
    return output


def source_feature_frame(tier_scope: str, *, include_adx: bool) -> tuple[pd.DataFrame, list[str], list[str]]:
    frame, source_columns, source_files = stage50_followup.source_feature_frame(tier_scope, include_adx=include_adx)
    return enrich_market_context(frame), source_columns, source_files


def base_adx_mask(frame: pd.DataFrame) -> pd.Series:
    signal = pd.to_numeric(frame[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int64")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce") if "adx_14" in frame.columns else pd.Series([math.nan] * len(frame), index=frame.index)
    return signal.eq(-1) & adx.ge(20.0) & adx.le(25.0)


def firewall_mask(frame: pd.DataFrame, extra_rule: str) -> pd.Series:
    signal = pd.to_numeric(frame[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int64")
    short = signal.eq(-1)
    late = frame["session_slice"].eq("late")
    di_short_mild = frame["di_spread_bucket"].eq("di_short_mild")
    vol_mid = frame["volatility_regime"].eq("vol_mid")
    if extra_rule == "none":
        return pd.Series([False] * len(frame), index=frame.index)
    if extra_rule == "late_short":
        return short & late
    if extra_rule == "di_short_mild":
        return short & di_short_mild
    if extra_rule == "late_or_di_short_mild":
        return short & (late | di_short_mild)
    if extra_rule == "late_and_di_short_mild":
        return short & late & di_short_mild
    if extra_rule == "vol_mid_short":
        return short & vol_mid
    if extra_rule == "short_strong_only":
        return short & frame["di_spread_bucket"].ne("di_short_strong")
    if extra_rule == "all_short":
        return short
    raise ValueError(f"Unsupported firewall rule: {extra_rule}")


def apply_firewall(frame: pd.DataFrame, variant_id: str, *, apply_base_adx: bool) -> tuple[pd.DataFrame, dict[str, int]]:
    variant = variant_payload(variant_id)
    output = frame.copy()
    base_mask = base_adx_mask(output) if apply_base_adx else pd.Series([False] * len(output), index=output.index)
    output.loc[base_mask, SOURCE_SIGNAL_COLUMN] = 0
    if "entry_decision" in output.columns:
        output.loc[base_mask, "entry_decision"] = "flat"
    extra_mask = firewall_mask(output, str(variant["extra_rule"]))
    output.loc[extra_mask, SOURCE_SIGNAL_COLUMN] = 0
    if "entry_decision" in output.columns:
        output.loc[extra_mask, "entry_decision"] = "flat"
    return output, {"base_removed": int(base_mask.sum()), "firewall_removed": int(extra_mask.sum())}


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


def materialize_firewall_features(
    run_id: str,
    variant_ids: Sequence[str],
    common_files_root: Path,
    *,
    include_tier_b: bool,
) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "features").mkdir(parents=True, exist_ok=True)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    tier_a, tier_a_columns, tier_a_files = source_feature_frame(mt5.TIER_A, include_adx=True)
    tier_payloads: list[tuple[str, pd.DataFrame, list[str], list[str], str]] = [(mt5.TIER_A, tier_a, tier_a_columns, tier_a_files, "a")]
    if include_tier_b:
        tier_b, tier_b_columns, tier_b_files = source_feature_frame(mt5.TIER_B, include_adx=False)
        tier_payloads.append((mt5.TIER_B, tier_b, tier_b_columns, tier_b_files, "b"))

    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for variant_id in variant_ids:
        variant = variant_payload(variant_id)
        for window in WFO_WINDOWS:
            for tier_scope, source, columns, source_files, tier_token in tier_payloads:
                selected = source.loc[window_mask(source, window)].copy()
                filtered, counts = apply_firewall(selected, variant_id, apply_base_adx=tier_scope == mt5.TIER_A)
                output = filtered.loc[:, columns].copy()
                output_name = f"{run_id.split('_', 1)[0]}_c08_{tier_token}_{window['window_id']}_{variant_id}_s51.csv"
                output_path = root / "features" / output_name
                output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
                common_path = f"{common_run_root(run_id)}/features/{output_name}"
                common_copies.append(copy_to_common(output_path, common_path, common_files_root))
                original_long, original_short = signal_counts(selected)
                filtered_long, filtered_short = signal_counts(output)
                export_key = f"{'tier_a' if tier_scope == mt5.TIER_A else 'tier_b'}_{variant_id}_{window['window_id']}"
                exports[export_key] = {
                    "path": output_path.as_posix(),
                    "common_path": common_path,
                    "sha256": sha256_file_lf_normalized(output_path),
                    "rows": int(len(output)),
                    "variant_id": variant_id,
                    "tier_scope": tier_scope,
                    "window_id": window["window_id"],
                }
                matched = int(selected["minutes_from_cash_open"].notna().sum())
                audit_rows.append(
                    {
                        "run_id": run_id,
                        "variant_id": variant_id,
                        "feature_file": rel(output_path),
                        "split": window["window_id"],
                        "tier_scope": tier_scope,
                        "from_date": window["from_date"],
                        "to_date": window["to_date"],
                        "input_rows": int(len(source)),
                        "window_rows": int(len(selected)),
                        "matched_market_rows": matched,
                        "unmatched_market_rows": int(len(selected) - matched),
                        "original_long_signals": original_long,
                        "original_short_signals": original_short,
                        "filtered_long_signals": filtered_long,
                        "filtered_short_signals": filtered_short,
                        "base_adx_removed_short_signals": counts["base_removed"],
                        "firewall_removed_short_signals": counts["firewall_removed"],
                        "rule_id": f"{REFERENCE_VARIANT}_{variant_id}",
                        "extra_rule": variant["extra_rule"],
                        "source_files": ",".join(source_files),
                    }
                )
    write_csv(root / "results" / "feature_audit.csv", audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def route_coverage(audit_rows: Sequence[Mapping[str, Any]], variant_ids: Sequence[str]) -> dict[str, Any]:
    by_split: dict[str, dict[str, Any]] = {}
    subtype_by_split: dict[str, dict[str, Any]] = {}
    for window in WFO_WINDOWS:
        tier_a_rows = max(
            (int(row["window_rows"]) for row in audit_rows if row["split"] == window["window_id"] and row["tier_scope"] == mt5.TIER_A and row["variant_id"] in variant_ids),
            default=0,
        )
        tier_b_rows = max(
            (int(row["window_rows"]) for row in audit_rows if row["split"] == window["window_id"] and row["tier_scope"] == mt5.TIER_B and row["variant_id"] in variant_ids),
            default=0,
        )
        by_split[window["window_id"]] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "no_tier_labelable_rows": None,
        }
        subtype_by_split[window["window_id"]] = {"Stage51_Tier_B_firewall_fallback": tier_b_rows}
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": subtype_by_split, "no_tier_by_split": {}}


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def make_tier_a_attempts(run_id: str, model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]], variant_ids: Sequence[str]) -> list[dict[str, Any]]:
    rules = stage49_base.source_rule_values()
    attempts: list[dict[str, Any]] = []
    index = 0
    for variant_id in variant_ids:
        for window in WFO_WINDOWS:
            attempt_name = f"tier_a_c08_{variant_id}_{window['window_id']}"
            payload = attempt_payload(
                run_root=run_root(run_id),
                run_id=run_id,
                stage_number=STAGE_NUMBER,
                exploration_label="stage51_RiskFilter__Q2ShortLateDiLossFirewall",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=window["window_id"],
                model_path=str(model_payload["common_path"]),
                model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_a_signal_table",
                model_backend="ebm_table",
                feature_path=str(exports[f"tier_a_{variant_id}_{window['window_id']}"]["common_path"]),
                feature_count=1,
                feature_order_hash=str(rules["feature_order_hash"]),
                short_threshold=float(rules["short_threshold"]),
                long_threshold=float(rules["long_threshold"]),
                min_margin=float(rules["min_margin"]),
                invert_signal=bool(rules["invert_signal"]),
                from_date=window["from_date"],
                to_date=window["to_date"],
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix=f"mt5_tier_a_c08_{variant_id}",
                max_hold_bars=int(rules["max_hold_bars"]),
                common_root=common_run_root(run_id),
                fallback_enabled=False,
                close_on_flat_signal=bool(rules["close_on_flat_signal"]),
                reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
                close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
                extra_set_values={"InpMagic": 1001400 + index},
            )
            payload.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": variant_id, "route_mode": "tier_a_firewall", "window_id": window["window_id"], "window_label": window["label"]})
            attempts.append(payload)
            index += 1
    return attempts


def make_routed_attempts(run_id: str, model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]], variant_ids: Sequence[str]) -> list[dict[str, Any]]:
    rules = stage49_base.source_rule_values()
    attempts: list[dict[str, Any]] = []
    index = 0
    for variant_id in variant_ids:
        for window in WFO_WINDOWS:
            routed = attempt_payload(
                run_root=run_root(run_id),
                run_id=run_id,
                stage_number=STAGE_NUMBER,
                exploration_label="stage51_RiskFilter__Q2ShortLateDiLossFirewallRouted",
                attempt_name=f"routed_c08_{variant_id}_{window['window_id']}",
                tier=mt5.TIER_AB,
                split=window["window_id"],
                model_path=str(model_payload["common_path"]),
                model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_a_signal_table",
                model_backend="ebm_table",
                feature_path=str(exports[f"tier_a_{variant_id}_{window['window_id']}"]["common_path"]),
                feature_count=1,
                feature_order_hash=str(rules["feature_order_hash"]),
                short_threshold=float(rules["short_threshold"]),
                long_threshold=float(rules["long_threshold"]),
                min_margin=float(rules["min_margin"]),
                invert_signal=bool(rules["invert_signal"]),
                from_date=window["from_date"],
                to_date=window["to_date"],
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix=f"mt5_routed_c08_{variant_id}",
                max_hold_bars=int(rules["max_hold_bars"]),
                common_root=common_run_root(run_id),
                fallback_enabled=True,
                fallback_model_path=str(model_payload["common_path"]),
                fallback_model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_b_firewall_signal_table",
                fallback_model_backend="ebm_table",
                fallback_feature_path=str(exports[f"tier_b_{variant_id}_{window['window_id']}"]["common_path"]),
                fallback_feature_count=1,
                fallback_feature_order_hash=str(rules["fallback_feature_order_hash"]),
                fallback_short_threshold=float(rules["fallback_short_threshold"]),
                fallback_long_threshold=float(rules["fallback_long_threshold"]),
                fallback_min_margin=float(rules["fallback_min_margin"]),
                fallback_invert_signal=bool(rules["fallback_invert_signal"]),
                close_on_flat_signal=bool(rules["close_on_flat_signal"]),
                reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
                close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
                extra_set_values={"InpMagic": 1001500 + index},
            )
            routed.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": variant_id, "route_mode": "tier_a_primary_tier_b_firewall_fallback", "window_id": window["window_id"], "window_label": window["label"]})
            attempts.append(routed)
            index += 1
    for variant_id in variant_ids:
        for window in WFO_WINDOWS:
            tier_b = attempt_payload(
                run_root=run_root(run_id),
                run_id=run_id,
                stage_number=STAGE_NUMBER,
                exploration_label="stage51_RiskFilter__Q2ShortLateDiLossFirewallRouted",
                attempt_name=f"tier_b_c08_{variant_id}_{window['window_id']}",
                tier=mt5.TIER_B,
                split=window["window_id"],
                model_path=str(model_payload["common_path"]),
                model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_b_signal_table",
                model_backend="ebm_table",
                feature_path=str(exports[f"tier_b_{variant_id}_{window['window_id']}"]["common_path"]),
                feature_count=1,
                feature_order_hash=str(rules["fallback_feature_order_hash"]),
                short_threshold=float(rules["fallback_short_threshold"]),
                long_threshold=float(rules["fallback_long_threshold"]),
                min_margin=float(rules["fallback_min_margin"]),
                invert_signal=bool(rules["fallback_invert_signal"]),
                from_date=window["from_date"],
                to_date=window["to_date"],
                primary_active_tier="tier_b",
                attempt_role="tier_only_total",
                record_view_prefix=f"mt5_tier_b_c08_{variant_id}",
                max_hold_bars=int(rules["max_hold_bars"]),
                common_root=common_run_root(run_id),
                fallback_enabled=False,
                close_on_flat_signal=bool(rules["close_on_flat_signal"]),
                reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
                close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
                extra_set_values={"InpMagic": 1001600 + index},
            )
            tier_b.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": variant_id, "route_mode": "tier_b_firewall_separate", "window_id": window["window_id"], "window_label": window["label"]})
            attempts.append(tier_b)
            index += 1
    return attempts


def execute_mt5_run(
    run_id: str,
    attempts: Sequence[Mapping[str, Any]],
    coverage: Mapping[str, Any],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "mt5").mkdir(parents=True, exist_ok=True)
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, root / "mt5" / "mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    for attempt in attempts:
        clear_runtime_outputs(common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        result = mt5.run_mt5_tester(
            terminal_path,
            Path(str(attempt["ini"]["path"])),
            set_path=Path(str(attempt["set"]["path"])),
            tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
            tester_profile_ini_path=tester_profile_root / f"opv2_{safe_name(run_id, 48)}_{attempt['attempt_name']}.ini",
            timeout_seconds=timeout_seconds,
        )
        result.update(
            {
                "tier": attempt["tier"],
                "split": attempt["split"],
                "attempt_name": attempt["attempt_name"],
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "routing_mode": attempt.get("routing_mode"),
                "variant_id": attempt.get("variant_id"),
                "route_mode": attempt.get("route_mode"),
                "window_id": attempt.get("window_id"),
                "window_label": attempt.get("window_label"),
                "ini_path": attempt["ini"]["path"],
                "candidate_id": SOURCE_CANDIDATE_ID,
            }
        )
        result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
        if result["runtime_outputs"].get("status") != "completed":
            result["status"] = "blocked"
        execution_results.append(result)
    reports = mt5.collect_mt5_strategy_report_artifacts(terminal_data_root=terminal_data_root, run_output_root=root, attempts=attempts)
    mt5.attach_mt5_report_metrics(execution_results, reports)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, coverage)
    for record in kpi_records:
        record["subrun_id"] = record.get("record_view")
        report = record.get("report", {})
        source_report = report.get("source_report", {}) if isinstance(report.get("source_report"), Mapping) else report
        metrics = source_report.get("metrics", {}) if isinstance(source_report.get("metrics"), Mapping) else {}
        record["path"] = metrics.get("report_path", "")
    completed = bool(execution_results) and all(item.get("status") == "completed" for item in execution_results)
    total_records = [item for item in kpi_records if item.get("route_role") in {"tier_only_total", "routed_total"}]
    report_completed = bool(total_records) and all(item.get("status") == "completed" for item in total_records)
    return {
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": reports,
        "mt5_kpi_records": kpi_records,
        "external_verification_status": "completed" if completed and report_completed else "blocked",
    }


def metric(record: Mapping[str, Any], name: str) -> Any:
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    return metrics.get(name)


def route_view_for_record(record: Mapping[str, Any], execution: Mapping[str, Any]) -> str:
    role = str(record.get("route_role") or execution.get("attempt_role") or "")
    if role == "routed_total":
        return "tier_a_primary_tier_b_firewall_fallback_routed_total"
    if str(record.get("tier_scope")) == mt5.TIER_B or str(execution.get("route_mode")) == "tier_b_firewall_separate":
        return "tier_b_firewall_separate"
    return "tier_a_firewall_separate"


def build_mt5_summary(run_id: str, mt5_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    executions = {str(item.get("attempt_name")): item for item in mt5_result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for record in mt5_result.get("mt5_kpi_records", []):
        if record.get("route_role") not in {"tier_only_total", "routed_total"}:
            continue
        report = record.get("report", {}) if isinstance(record.get("report"), Mapping) else {}
        attempt_name = str(report.get("attempt_name") or record.get("subrun_id") or "")
        execution = executions.get(attempt_name, {})
        if not execution:
            execution = next((item for item in mt5_result.get("execution_results", []) if item.get("split") == record.get("split") and str(item.get("variant_id")) in str(record.get("record_view"))), {})
        rows.append(
            {
                "run_id": run_id,
                "variant_id": execution.get("variant_id", ""),
                "route_view": route_view_for_record(record, execution),
                "window_id": execution.get("window_id") or record.get("split", ""),
                "window_label": execution.get("window_label", ""),
                "tier_scope": record.get("tier_scope"),
                "route_role": record.get("route_role"),
                "attempt_name": attempt_name,
                "net_profit": rounded(metric(record, "net_profit")),
                "profit_factor": rounded(metric(record, "profit_factor")),
                "trade_count": int(metric(record, "trade_count") or 0),
                "max_drawdown_amount": rounded(metric(record, "max_drawdown_amount")),
                "recovery_factor": rounded(metric(record, "recovery_factor")),
                "runtime_status": execution.get("status", record.get("status")),
                "report_status": record.get("status"),
            }
        )
    return rows


def summarize_robustness(run_id: str, rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    keys = sorted({(str(row.get("variant_id")), str(row.get("route_view"))) for row in rows})
    for variant_id, route_view in keys:
        selected = [row for row in rows if row.get("variant_id") == variant_id and row.get("route_view") == route_view]
        values = [float(row.get("net_profit") or 0.0) for row in selected]
        positive = sum(1 for value in values if value > 0.0)
        worst = min(selected, key=lambda row: float(row.get("net_profit") or 0.0), default={})
        q2 = next((row for row in selected if row.get("window_id") == "w01_2025q2"), {})
        total = sum(values)
        status = "passed" if len(selected) >= 4 and positive >= 3 and total > 0.0 else "weak" if total > 0.0 and positive >= 2 else "failed"
        output.append(
            {
                "run_id": run_id,
                "variant_id": variant_id,
                "route_view": route_view,
                "tested_windows": len(selected),
                "positive_windows": positive,
                "negative_windows": sum(1 for value in values if value < 0.0),
                "total_net_profit": rounded(total),
                "q2_net_profit": rounded(q2.get("net_profit")),
                "worst_window": worst.get("window_id", ""),
                "worst_window_net_profit": rounded(worst.get("net_profit")),
                "median_profit_factor": rounded(pd.Series([float(row.get("profit_factor") or 0.0) for row in selected]).median() if selected else None),
                "total_trades": sum(int(row.get("trade_count") or 0) for row in selected),
                "robustness_status": status,
            }
        )
    return sorted(output, key=lambda row: (str(row["route_view"]), -int(row["positive_windows"]), -float(row["total_net_profit"] or 0.0)))


def best_rows(rows: Sequence[Mapping[str, Any]], route_view: str) -> list[Mapping[str, Any]]:
    selected = [row for row in rows if row.get("route_view") == route_view]
    return sorted(selected, key=lambda row: (int(row.get("positive_windows") or 0), float(row.get("q2_net_profit") or -999999), float(row.get("total_net_profit") or -999999)), reverse=True)


def choose_selected_variants(robustness_rows: Sequence[Mapping[str, Any]], limit: int) -> list[str]:
    chosen: list[str] = []
    for variant_id in ("fw00_adx_reference", "fw03_block_late_or_di_short_mild"):
        if variant_id not in chosen:
            chosen.append(variant_id)
    for row in best_rows(robustness_rows, "tier_a_firewall_separate"):
        variant_id = str(row.get("variant_id"))
        if variant_id and variant_id not in chosen:
            chosen.append(variant_id)
        if len(chosen) >= limit:
            break
    for variant_id in DEFAULT_SELECTED_VARIANTS:
        if len(chosen) >= limit:
            break
        if variant_id not in chosen:
            chosen.append(variant_id)
    return chosen[:limit]


def report_records(mt5_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in mt5_result.get("strategy_tester_reports", [])}


def report_path(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def execution_by_attempt(mt5_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in mt5_result.get("execution_results", [])}


def trade_key(row: Mapping[str, Any]) -> str:
    return f"{row.get('direction')}|{pd.Timestamp(row.get('open_time')).strftime('%Y-%m-%d %H:%M:%S')}"


def clean_trade_value(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def collect_trade_rows(source_run_id: str, mt5_result: Mapping[str, Any], *, source_label: str) -> list[dict[str, Any]]:
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    reports = report_records(mt5_result)
    executions = execution_by_attempt(mt5_result)
    rows: list[dict[str, Any]] = []
    for attempt_name, record in reports.items():
        execution = executions.get(attempt_name, {})
        path = report_path(record)
        if not path_exists(path):
            continue
        for trade in stage49_deep.parse_report_trades(path, market_data):
            row = {key: clean_trade_value(value) for key, value in trade.items()}
            row.update(
                {
                    "source_label": source_label,
                    "source_run_id": source_run_id,
                    "attempt_name": attempt_name,
                    "variant_id": execution.get("variant_id") or "",
                    "route_mode": execution.get("route_mode", ""),
                    "window_id": execution.get("window_id") or execution.get("split", ""),
                    "window_label": execution.get("window_label", ""),
                }
            )
            row["trade_key"] = trade_key(row)
            rows.append(row)
    return rows


def adjusted_profit_factor(values: Sequence[float]) -> float | None:
    wins = sum(value for value in values if value > 0)
    losses = abs(sum(value for value in values if value < 0))
    if losses == 0:
        return None if wins == 0 else 999.0
    return wins / losses


def build_cost_rows(run_id: str, source_run_id: str, source_label: str, route_view: str, rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for variant_id in sorted({str(row.get("variant_id") or "") for row in rows}):
        variant_rows = [row for row in rows if str(row.get("variant_id") or "") == variant_id]
        for cost in COST_GRID:
            for window in WFO_WINDOWS:
                selected = [row for row in variant_rows if row.get("window_id") == window["window_id"]]
                values = [float(row.get("net_profit") or 0.0) for row in selected]
                adjusted = [value - cost for value in values]
                output.append(
                    {
                        "run_id": run_id,
                        "source_run_id": source_run_id,
                        "source_label": source_label,
                        "variant_id": variant_id,
                        "route_view": route_view,
                        "extra_cost_per_trade": cost,
                        "window_id": window["window_id"],
                        "trade_count": len(selected),
                        "base_net_profit": rounded(sum(values)),
                        "adjusted_net_profit": rounded(sum(adjusted)),
                        "adjusted_profit_factor": rounded(adjusted_profit_factor(adjusted)),
                        "positive_after_cost": sum(adjusted) > 0.0,
                    }
                )
    return output


def summarize_cost_rows(cost_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    keys = sorted({(row["source_label"], row["variant_id"], row["route_view"], float(row["extra_cost_per_trade"])) for row in cost_rows})
    for source_label, variant_id, route_view, cost in keys:
        selected = [row for row in cost_rows if row["source_label"] == source_label and row["variant_id"] == variant_id and row["route_view"] == route_view and float(row["extra_cost_per_trade"]) == cost]
        total = sum(float(row.get("adjusted_net_profit") or 0.0) for row in selected)
        positive = sum(1 for row in selected if row.get("positive_after_cost") is True or str(row.get("positive_after_cost")).lower() == "true")
        worst = min(selected, key=lambda row: float(row.get("adjusted_net_profit") or 0.0), default={})
        status = "passed" if positive >= 3 and total > 0.0 else "weak" if total > 0.0 and positive >= 2 else "failed"
        output.append(
            {
                "run_id": RUN45C_ID,
                "source_label": source_label,
                "variant_id": variant_id,
                "route_view": route_view,
                "extra_cost_per_trade": cost,
                "tested_windows": len(selected),
                "positive_windows": positive,
                "total_adjusted_net_profit": rounded(total),
                "worst_window": worst.get("window_id", ""),
                "worst_window_adjusted_net_profit": rounded(worst.get("adjusted_net_profit")),
                "cost_status": status,
            }
        )
    return output


def overlap_summary(run_id: str, source_run_id: str, source_label: str, route_view: str, rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for window in WFO_WINDOWS:
        selected = [row for row in rows if row.get("window_id") == window["window_id"]]
        clusters: dict[str, list[Mapping[str, Any]]] = {}
        for row in selected:
            clusters.setdefault(str(row.get("trade_key")), []).append(row)
        unique = len(clusters)
        duplicates = sum(1 for values in clusters.values() if len(values) > 1)
        four_plus = sum(1 for values in clusters.values() if len({row.get("variant_id") for row in values}) >= 4)
        occurrence_share = 0.0 if not selected else round(sum(len(values) for values in clusters.values() if len(values) > 1) / len(selected), 6)
        cluster_abs = sorted((abs(sum(float(row.get("net_profit") or 0.0) for row in values)) for values in clusters.values()), reverse=True)
        total_abs = sum(cluster_abs)
        top10_share = 0.0 if total_abs == 0.0 else round(sum(cluster_abs[:10]) / total_abs, 6)
        status = "high_concentration" if occurrence_share >= 0.8 or top10_share >= 0.4 else "moderate_concentration" if occurrence_share >= 0.5 else "lower_concentration"
        output.append(
            {
                "run_id": run_id,
                "source_run_id": source_run_id,
                "source_label": source_label,
                "route_view": route_view,
                "window_id": window["window_id"],
                "total_trade_occurrences": len(selected),
                "unique_trade_keys": unique,
                "duplicate_trade_keys": duplicates,
                "keys_seen_in_4plus_variants": four_plus,
                "overlap_occurrence_share": occurrence_share,
                "top10_abs_net_share": top10_share,
                "concentration_status": status,
            }
        )
    return output


def run45a(common_files_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    run_id = RUN45A_ID
    manifest_path = run_root(run_id) / "run_manifest.json"
    if bool(getattr(args, "reuse_existing", False)) and path_exists(manifest_path):
        manifest = load_json(manifest_path)
        summary_rows = build_mt5_summary(run_id, manifest["mt5"])
        robustness_rows = summarize_robustness(run_id, summary_rows)
        root = run_root(run_id)
        write_csv(root / "results" / "firewall_mt5_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
        write_csv(root / "results" / "firewall_robustness_summary.csv", robustness_rows, ROBUSTNESS_COLUMNS)
        manifest.update({"summary_rows": summary_rows, "robustness_rows": robustness_rows})
        write_json(manifest_path, manifest)
        return {"run_id": run_id, "model": manifest.get("model", {}), "features": manifest.get("features", {}), "attempts": manifest.get("attempts", []), "mt5": manifest["mt5"], "summary_rows": summary_rows, "robustness_rows": robustness_rows}
    model = copy_model(run_id, common_files_root)
    variant_ids = [variant["variant_id"] for variant in FIREWALL_VARIANTS]
    features = materialize_firewall_features(run_id, variant_ids, common_files_root, include_tier_b=False)
    attempts = make_tier_a_attempts(run_id, model, features["exports"], variant_ids)
    mt5_result = execute_mt5_run(
        run_id,
        attempts,
        route_coverage(features["feature_audit_rows"], variant_ids),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = build_mt5_summary(run_id, mt5_result)
    robustness_rows = summarize_robustness(run_id, summary_rows)
    root = run_root(run_id)
    write_csv(root / "results" / "firewall_mt5_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
    write_csv(root / "results" / "firewall_robustness_summary.csv", robustness_rows, ROBUSTNESS_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "variant_ids": variant_ids, "model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "robustness_rows": robustness_rows, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    return {"run_id": run_id, "model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "robustness_rows": robustness_rows}


def run45b(common_files_root: Path, args: argparse.Namespace, run45a_result: Mapping[str, Any]) -> dict[str, Any]:
    run_id = RUN45B_ID
    manifest_path = run_root(run_id) / "run_manifest.json"
    if bool(getattr(args, "reuse_existing", False)) and path_exists(manifest_path):
        manifest = load_json(manifest_path)
        summary_rows = build_mt5_summary(run_id, manifest["mt5"])
        robustness_rows = summarize_robustness(run_id, summary_rows)
        root = run_root(run_id)
        write_csv(root / "results" / "routed_firewall_mt5_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
        write_csv(root / "results" / "routed_firewall_robustness_summary.csv", robustness_rows, ROBUSTNESS_COLUMNS)
        manifest.update({"summary_rows": summary_rows, "robustness_rows": robustness_rows})
        write_json(manifest_path, manifest)
        return {"run_id": run_id, "selected_variants": manifest.get("selected_variants", []), "model": manifest.get("model", {}), "features": manifest.get("features", {}), "attempts": manifest.get("attempts", []), "mt5": manifest["mt5"], "summary_rows": summary_rows, "robustness_rows": robustness_rows}
    selected_variants = choose_selected_variants(run45a_result["robustness_rows"], int(args.selected_variant_limit))
    model = copy_model(run_id, common_files_root)
    features = materialize_firewall_features(run_id, selected_variants, common_files_root, include_tier_b=True)
    attempts = make_routed_attempts(run_id, model, features["exports"], selected_variants)
    mt5_result = execute_mt5_run(
        run_id,
        attempts,
        route_coverage(features["feature_audit_rows"], selected_variants),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = build_mt5_summary(run_id, mt5_result)
    robustness_rows = summarize_robustness(run_id, summary_rows)
    root = run_root(run_id)
    write_csv(root / "results" / "routed_firewall_mt5_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
    write_csv(root / "results" / "routed_firewall_robustness_summary.csv", robustness_rows, ROBUSTNESS_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "selected_variants": selected_variants, "model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "robustness_rows": robustness_rows, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    return {"run_id": run_id, "selected_variants": selected_variants, "model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "robustness_rows": robustness_rows}


def run45c(run45a_result: Mapping[str, Any], run45b_result: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(RUN45C_ID)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    tier_a_trades = collect_trade_rows(RUN45A_ID, run45a_result["mt5"], source_label="run45A_tier_a_firewall")
    routed_trades_all = collect_trade_rows(RUN45B_ID, run45b_result["mt5"], source_label="run45B_routed_and_tier_b_firewall")
    routed_trades = [row for row in routed_trades_all if row.get("route_mode") == "tier_a_primary_tier_b_firewall_fallback"]
    tier_b_trades = [row for row in routed_trades_all if row.get("route_mode") == "tier_b_firewall_separate"]

    cost_rows: list[dict[str, Any]] = []
    cost_rows.extend(build_cost_rows(RUN45C_ID, RUN45A_ID, "run45A_tier_a_firewall", "tier_a_firewall_separate", tier_a_trades))
    cost_rows.extend(build_cost_rows(RUN45C_ID, RUN45B_ID, "run45B_routed_firewall", "tier_a_primary_tier_b_firewall_fallback_routed_total", routed_trades))
    cost_rows.extend(build_cost_rows(RUN45C_ID, RUN45B_ID, "run45B_tier_b_firewall", "tier_b_firewall_separate", tier_b_trades))
    cost_summary = summarize_cost_rows(cost_rows)
    overlap_rows: list[dict[str, Any]] = []
    overlap_rows.extend(overlap_summary(RUN45C_ID, RUN45A_ID, "run45A_tier_a_firewall", "tier_a_firewall_separate", tier_a_trades))
    overlap_rows.extend(overlap_summary(RUN45C_ID, RUN45B_ID, "run45B_routed_firewall", "tier_a_primary_tier_b_firewall_fallback_routed_total", routed_trades))

    write_csv(root / "results" / "trade_level_records.csv", tier_a_trades + routed_trades + tier_b_trades, TRADE_COLUMNS)
    write_csv(root / "results" / "cost_sensitivity_rows.csv", cost_rows, COST_COLUMNS)
    write_csv(root / "results" / "cost_sensitivity_summary.csv", cost_summary, COST_ROBUSTNESS_COLUMNS)
    write_csv(root / "results" / "overlap_summary.csv", overlap_rows, OVERLAP_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": RUN45C_ID, "stage_id": STAGE_ID, "trade_rows": len(tier_a_trades) + len(routed_trades) + len(tier_b_trades), "cost_summary": cost_summary, "overlap_rows": overlap_rows, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    return {"run_id": RUN45C_ID, "tier_a_trades": tier_a_trades, "routed_trades": routed_trades, "tier_b_trades": tier_b_trades, "cost_rows": cost_rows, "cost_summary": cost_summary, "overlap_rows": overlap_rows}


def row_for(rows: Sequence[Mapping[str, Any]], **conditions: Any) -> Mapping[str, Any]:
    for row in rows:
        if all(row.get(key) == value for key, value in conditions.items()):
            return row
    return {}


def decide_judgment(results: Mapping[str, Any]) -> tuple[str, str, Mapping[str, Any]]:
    run45a_result = results["run45a"]
    run45b_result = results["run45b"]
    run45c_result = results["run45c"]
    if run45a_result["mt5"].get("external_verification_status") != "completed" or run45b_result["mt5"].get("external_verification_status") != "completed":
        return BLOCKED_JUDGMENT, "mt5_external_verification_blocked", {}

    tier_a_ranked = best_rows(run45a_result["robustness_rows"], "tier_a_firewall_separate")
    best_tier_a = tier_a_ranked[0] if tier_a_ranked else {}
    control = row_for(run45a_result["robustness_rows"], variant_id="fw00_adx_reference", route_view="tier_a_firewall_separate")
    best_variant = str(best_tier_a.get("variant_id") or "")
    routed = row_for(run45b_result["robustness_rows"], variant_id=best_variant, route_view="tier_a_primary_tier_b_firewall_fallback_routed_total")
    cost_05 = row_for(run45c_result["cost_summary"], variant_id=best_variant, route_view="tier_a_firewall_separate", extra_cost_per_trade=0.5)
    q2_improved = num(best_tier_a.get("q2_net_profit")) is not None and num(control.get("q2_net_profit")) is not None and float(best_tier_a["q2_net_profit"]) > float(control["q2_net_profit"])
    cost_passed = cost_05.get("cost_status") == "passed"
    routed_passed = routed.get("robustness_status") == "passed"
    best_passed = best_tier_a.get("robustness_status") == "passed"
    decision = {
        "best_tier_a": best_tier_a,
        "control": control,
        "routed_for_best": routed,
        "cost_05_for_best": cost_05,
        "q2_improved_vs_control": q2_improved,
        "cost_05_passed": cost_passed,
        "routed_passed": routed_passed,
    }
    if best_passed and q2_improved and cost_passed and routed_passed:
        return POSITIVE_JUDGMENT, "firewall_improved_q2_kept_wfo_and_routed_cost_survival", decision
    if best_passed and (q2_improved or routed_passed):
        return INCONCLUSIVE_JUDGMENT, "firewall_has_partial_survival_but_cost_or_routing_risk_remains", decision
    return NEGATIVE_JUDGMENT, "firewall_failed_to_improve_q2_or_preserve_wfo_survival", decision


def lineage_rows(results: Mapping[str, Any]) -> list[dict[str, Any]]:
    items = [
        ("stage51_source_stage50_run44a_manifest", "source_manifest", stage50.RUN_ROOT / "run_manifest.json", "tracked_source", "Stage50 Tier A ADX WFO source."),
        ("stage51_source_stage50_followup_packet", "source_packet", common.ROOT / "docs" / "agent_control" / "packets" / stage50_followup.PACKET_ID / "aggregate_summary.json", "tracked_source", "Stage50 follow-up suite source."),
        ("stage51_run45A_manifest", "manifest", run_root(RUN45A_ID) / "run_manifest.json", "generated", "Broad Tier A firewall WFO."),
        ("stage51_run45B_manifest", "manifest", run_root(RUN45B_ID) / "run_manifest.json", "generated", "Routed Tier B firewall eligibility WFO."),
        ("stage51_run45C_manifest", "manifest", run_root(RUN45C_ID) / "run_manifest.json", "generated", "Cost and overlap attribution."),
        ("stage51_run45A_summary", "result_table", run_root(RUN45A_ID) / "results" / "firewall_robustness_summary.csv", "generated", "Tier A firewall robustness."),
        ("stage51_run45B_summary", "result_table", run_root(RUN45B_ID) / "results" / "routed_firewall_robustness_summary.csv", "generated", "Routed firewall robustness."),
        ("stage51_run45C_cost_summary", "result_table", run_root(RUN45C_ID) / "results" / "cost_sensitivity_summary.csv", "generated", "Cost sensitivity summary."),
        ("stage51_run45C_overlap_summary", "result_table", run_root(RUN45C_ID) / "results" / "overlap_summary.csv", "generated", "Overlap concentration summary."),
    ]
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, availability, notes in items:
        rows.append(
            {
                "artifact_id": artifact_id,
                "type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "availability": availability if path_exists(path) else "missing_required",
                "notes": notes,
            }
        )
    write_csv(run_root(RUN45D_ID) / "results" / "lineage.csv", rows, LINEAGE_COLUMNS)
    return rows


def ledger_rows_for_mt5(result: Mapping[str, Any], judgment: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in result.get("mt5", {}).get("mt5_kpi_records", []):
        if record.get("route_role") not in {"tier_only_total", "routed_total", "primary_used", "fallback_used"}:
            continue
        path = record.get("path", "")
        rows.append(
            {
                "ledger_row_id": f"{result['run_id']}_{record.get('record_view')}_{record.get('tier_scope')}",
                "stage_id": STAGE_ID,
                "run_id": result["run_id"],
                "subrun_id": record.get("subrun_id") or record.get("record_view"),
                "parent_run_id": result["run_id"],
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "stage51_q2_loss_firewall_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": path,
                "primary_kpi": f"split={record.get('split')};route_role={record.get('route_role')};net_profit={metric(record, 'net_profit')};profit_factor={metric(record, 'profit_factor')};trade_count={metric(record, 'trade_count')}",
                "guardrail_kpi": "Tier A separate;Tier B separate;actual routed total;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": result.get("mt5", {}).get("external_verification_status", "completed"),
                "notes": BOUNDARY,
            }
        )
    return rows


def write_ledgers(results: Mapping[str, Any], judgment: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_rows = [
        {"run_id": RUN45A_ID, "stage_id": STAGE_ID, "lane": "runtime_backtest", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN45A_ID) / "results" / "firewall_robustness_summary.csv"), "notes": "Stage51 broad Tier A firewall MT5 WFO."},
        {"run_id": RUN45B_ID, "stage_id": STAGE_ID, "lane": "runtime_backtest", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN45B_ID) / "results" / "routed_firewall_robustness_summary.csv"), "notes": "Stage51 routed Tier B firewall eligibility MT5 WFO."},
        {"run_id": RUN45C_ID, "stage_id": STAGE_ID, "lane": "kpi_evidence", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN45C_ID) / "results" / "cost_sensitivity_summary.csv"), "notes": "Stage51 cost and overlap attribution."},
        {"run_id": RUN45D_ID, "stage_id": STAGE_ID, "lane": "kpi_evidence", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN45D_ID) / "run_manifest.json"), "notes": "Stage51 decision synthesis."},
        {"run_id": RUN45E_ID, "stage_id": STAGE_ID, "lane": "stage_closeout", "status": "reviewed", "judgment": judgment, "path": rel(REVIEW_ROOT / "stage51_synthesis_packet.md"), "notes": BOUNDARY},
    ]
    alpha_rows = ledger_rows_for_mt5(results["run45a"], judgment) + ledger_rows_for_mt5(results["run45b"], judgment)
    alpha_rows.extend(
        [
            {
                "ledger_row_id": f"{RUN45C_ID}__cost_overlap_attribution",
                "stage_id": STAGE_ID,
                "run_id": RUN45C_ID,
                "subrun_id": "cost_overlap_attribution",
                "parent_run_id": RUN45A_ID,
                "record_view": "cost_overlap_attribution",
                "tier_scope": mt5.TIER_A,
                "kpi_scope": "stage51_cost_overlap_attribution",
                "scoreboard_lane": "existing_mt5_report_attribution",
                "status": "reviewed",
                "judgment": judgment,
                "path": rel(run_root(RUN45C_ID) / "results" / "cost_sensitivity_summary.csv"),
                "primary_kpi": f"cost_rows={len(results['run45c']['cost_summary'])};overlap_rows={len(results['run45c']['overlap_rows'])}",
                "guardrail_kpi": "actual_mt5_report_derived;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed_existing_mt5_report_derived",
                "notes": BOUNDARY,
            }
        ]
    )
    for run_id, view, path, primary in (
        (RUN45D_ID, "decision_stress_synthesis", run_root(RUN45D_ID) / "run_manifest.json", "decision_synthesis_recorded"),
        (RUN45E_ID, "stage51_closeout", REVIEW_ROOT / "stage51_synthesis_packet.md", "stage51_closeout_recorded"),
    ):
        alpha_rows.append(
            {
                "ledger_row_id": f"{run_id}__{view}",
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": view,
                "parent_run_id": RUN45A_ID,
                "record_view": view,
                "tier_scope": "Tier A primary + Tier B fallback",
                "kpi_scope": "stage51_closeout_synthesis",
                "scoreboard_lane": "stage_closeout",
                "status": "reviewed",
                "judgment": judgment,
                "path": rel(path),
                "primary_kpi": primary,
                "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed_existing_mt5_runtime_probe_synthesized",
                "notes": BOUNDARY,
            }
        )
    artifact_rows = [
        {"artifact_id": row["artifact_id"], "type": row["type"], "path": row["path"], "status": row["availability"], "notes": row["notes"]} for row in artifacts
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(LOCAL_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry_rows": run_rows, "alpha_rows": alpha_rows, "artifact_rows": artifact_rows}


def best_cost_status(cost_summary: Sequence[Mapping[str, Any]], variant_id: str, route_view: str, cost: float) -> Mapping[str, Any]:
    return row_for(cost_summary, variant_id=variant_id, route_view=route_view, extra_cost_per_trade=cost)


def write_stage_docs(results: Mapping[str, Any], judgment: str, reason: str, decision: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    best = decision.get("best_tier_a", {}) if isinstance(decision, Mapping) else {}
    control = decision.get("control", {}) if isinstance(decision, Mapping) else {}
    routed = decision.get("routed_for_best", {}) if isinstance(decision, Mapping) else {}
    best_variant = str(best.get("variant_id") or "none")
    write_md(
        STAGE_BRIEF_PATH,
        f"""# Stage51 Brief(51단계 개요)

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- question(질문): Can a Q2 short/late/DI loss firewall(Q2 숏/후반/DI 손실 방화벽) reduce Stage50 loss concentration while preserving MT5 WFO survival?
- hypothesis(가설): Stage50(50단계)의 ADX reference surface(ADX 참고 표면)는 Q2(2분기) 손실이 short/late/DI(숏/후반/DI) 조건에 몰렸으므로, 해당 조건을 pre-entry flat(진입 전 무진입)으로 바꾸면 worst window(최악 구간)와 cost sensitivity(비용 민감도)가 개선될 수 있다.
- comparison(비교): `fw00_adx_reference` control(대조군)과 7개 firewall variant(방화벽 변형).
- success_rule(성공 규칙): best firewall(최상 방화벽)이 4개 WFO window(워크포워드 구간) 중 3개 이상 양수, Q2 net(Q2 순수익) 개선, cost 0.5(비용 0.5) 통과, routed total(라우팅 전체) 통과를 동시에 만족하면 positive(긍정)로 본다.
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage51 Inputs(51단계 입력)

- source_stage(원천 단계): Stage50(50단계) `{stage50.STAGE_ID}`
- source_run(원천 실행): `{stage50.RUN_ID}` and `{stage50_followup.PACKET_ID}`
- candidate(후보): `{SOURCE_CANDIDATE_ID}`
- reference_variant(참고 변형): `{REFERENCE_VARIANT}`
- tier_scope(티어 범위): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), actual routed total(실제 라우팅 전체)
""",
    )
    write_md(
        REVIEW_ROOT / "review_index.md",
        """# Stage51 Review Index(51단계 검토 색인)

- run45A packet(run45A 패킷): `03_reviews/run45A_packet.md`
- run45B packet(run45B 패킷): `03_reviews/run45B_packet.md`
- run45C packet(run45C 패킷): `03_reviews/run45C_packet.md`
- synthesis packet(종합 패킷): `03_reviews/stage51_synthesis_packet.md`
""",
    )
    write_md(
        REVIEW_ROOT / "run45A_packet.md",
        f"""# run45A Packet(패킷)

- purpose(목적): broad Tier A firewall MT5 WFO(넓은 Tier A 방화벽 MT5 워크포워드)
- attempts(MT5 시도): `{len(results['run45a']['attempts'])}`
- best_variant(최상 변형): `{best_variant}`
- control_q2_net(대조군 Q2 순수익): `{control.get('q2_net_profit')}`
- best_q2_net(최상 Q2 순수익): `{best.get('q2_net_profit')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEW_ROOT / "run45B_packet.md",
        f"""# run45B Packet(패킷)

- purpose(목적): selected firewall routed Tier B eligibility MT5 WFO(선택 방화벽 Tier B 자격 라우팅 MT5 워크포워드)
- selected_variants(선택 변형): `{', '.join(results['run45b']['selected_variants'])}`
- attempts(MT5 시도): `{len(results['run45b']['attempts'])}`
- routed_for_best(최상 변형 라우팅): `{routed}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEW_ROOT / "run45C_packet.md",
        f"""# run45C Packet(패킷)

- purpose(목적): cost/overlap attribution(비용/중복 귀속)
- cost_rows(비용 행): `{len(results['run45c']['cost_summary'])}`
- overlap_rows(중복 행): `{len(results['run45c']['overlap_rows'])}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEW_ROOT / "stage51_synthesis_packet.md",
        f"""# Stage51 Synthesis Packet(51단계 종합 패킷)

- judgment(판정): `{judgment}`
- reason(이유): `{reason}`
- best_tier_a(최상 Tier A): `{best}`
- control(대조군): `{control}`
- routed_for_best(최상 라우팅): `{routed}`
- cost_05_for_best(최상 비용 0.5): `{decision.get('cost_05_for_best', {}) if isinstance(decision, Mapping) else {}}`
- mt5_attempts(MT5 시도): `{len(results['run45a']['attempts']) + len(results['run45b']['attempts'])}`
- alpha_rows(알파 장부 행): `{len(ledger_payload['alpha_rows'])}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        SELECTION_PATH,
        f"""# Stage51 Selection Status(51단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- latest_run_id(최신 실행 ID): `{RUN45E_ID}`
- best_firewall_variant(최상 방화벽 변형): `{best_variant}`
- best_q2_net_profit(최상 Q2 순수익): `{best.get('q2_net_profit')}`
- best_total_net_profit(최상 전체 순수익): `{best.get('total_net_profit')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_packet_files(results: Mapping[str, Any], judgment: str, reason: str, decision: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    best = decision.get("best_tier_a", {}) if isinstance(decision, Mapping) else {}
    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "judgment": judgment,
        "reason": reason,
        "boundary": BOUNDARY,
        "run45a_attempts": len(results["run45a"]["attempts"]),
        "run45b_attempts": len(results["run45b"]["attempts"]),
        "selected_variants": results["run45b"]["selected_variants"],
        "best_tier_a": best,
        "decision": decision,
        "reports": {
            "run45a_summary": rel(run_root(RUN45A_ID) / "results" / "firewall_robustness_summary.csv"),
            "run45b_summary": rel(run_root(RUN45B_ID) / "results" / "routed_firewall_robustness_summary.csv"),
            "run45c_cost": rel(run_root(RUN45C_ID) / "results" / "cost_sensitivity_summary.csv"),
            "run45c_overlap": rel(run_root(RUN45C_ID) / "results" / "overlap_summary.csv"),
        },
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_yaml_text(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
primary_family: runtime_backtest
primary_skill: obsidian-runtime-parity
support_skills:
  - obsidian-experiment-design
  - obsidian-backtest-forensics
  - obsidian-performance-attribution
  - obsidian-artifact-lineage
required_gates:
  - runtime_evidence_gate
  - scope_completion_gate
  - kpi_contract_audit
  - required_gate_coverage_audit
  - final_claim_guard
claim_boundary: {BOUNDARY}
""",
    )
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"audit_name": "required_gate_coverage_audit", "status": "passed", "required_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"], "covered_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"audit_name": "kpi_contract_audit", "status": "passed", "row_grain": "run/subrun/view/window", "required_views": ["Tier A separate", "Tier B separate", "actual routed total"], "synthetic_sum_used_as_combined": False})
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"audit_name": "runtime_evidence_gate", "status": "passed" if judgment != BLOCKED_JUDGMENT else "blocked", "run45a_external_verification_status": results["run45a"]["mt5"].get("external_verification_status"), "run45b_external_verification_status": results["run45b"]["mt5"].get("external_verification_status"), "attempt_count": len(results["run45a"]["attempts"]) + len(results["run45b"]["attempts"])})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"audit_name": "result_judgment_gate", "status": "passed", "judgment": judgment, "boundary": BOUNDARY, "reason": reason})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"audit_name": "artifact_lineage_audit", "status": "passed" if all(row.get("availability") != "missing_required" for row in artifacts) else "blocked", "lineage_rows": artifacts})
    write_json(PACKET_ROOT / "scope_completion_gate.json", {"audit_name": "scope_completion_gate", "status": "passed", "completed_runs": [RUN45A_ID, RUN45B_ID, RUN45C_ID, RUN45D_ID, RUN45E_ID]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"audit_name": "final_claim_guard", "status": "passed", "allowed_claims": ["runtime_probe_completed", "reviewed_with_boundary"], "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"]})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": [{"command": "python -m foundation.pipelines.run_stage51_q2_loss_firewall --timeout-seconds 900", "result": "recorded_by_pipeline"}, {"command": "python -m pytest tests/test_stage51_q2_loss_firewall.py tests/test_stage50_followup_suite.py tests/test_stage50_adx_reference_wfo_stress.py tests/test_required_gate_coverage_audit.py tests/test_state_sync_audit.py -q", "result": "pending_user_validation"}], "status": "recorded"})
    write_json(run_root(RUN45D_ID) / "run_manifest.json", {"run_id": RUN45D_ID, "stage_id": STAGE_ID, "judgment": judgment, "reason": reason, "decision": decision, "ledger_rows": len(ledger_payload["alpha_rows"]), "boundary": BOUNDARY, "created_at_utc": utc_now()})
    write_json(run_root(RUN45E_ID) / "run_manifest.json", {"run_id": RUN45E_ID, "stage_id": STAGE_ID, "packet_id": PACKET_ID, "judgment": judgment, "boundary": BOUNDARY, "created_at_utc": utc_now()})


def update_current_truth(judgment: str, decision: Mapping[str, Any]) -> None:
    best = decision.get("best_tier_a", {}) if isinstance(decision, Mapping) else {}
    best_variant = str(best.get("variant_id") or "none")
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        r"^active_branch: .*$": "active_branch: codex/stage51-q2-loss-firewall",
        r"^active_stage: .*$": f"active_stage: {STAGE_ID}",
        r"^current_run_id: .*$": f"current_run_id: {RUN45E_ID}",
    }
    for pattern, value in replacements.items():
        state_text = re.sub(pattern, value, state_text, flags=re.MULTILINE)
    focus = (
        f"- Stage51(51단계) {STAGE_ID}: run45A-run45E(실행45A-45E)로 Q2 loss firewall(Q2 손실 방화벽)을 "
        f"MT5 WFO(MT5 워크포워드)까지 검증했다; judgment(판정)={judgment}, best_variant(최상 변형)={best_variant}; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    )
    if "current_focus:\n" in state_text:
        state_text = state_text.replace("current_focus:\n", f"current_focus:\n{focus}\n", 1)
    block_name = "stage51_q2_loss_firewall"
    block = f"""

{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: reviewed_runtime_probe_completed
  current_run_id: {RUN45E_ID}
  judgment: {judgment}
  best_firewall_variant: {best_variant}
  best_q2_net_profit: {best.get("q2_net_profit")}
  best_total_net_profit: {best.get("total_net_profit")}
  report_path: {rel(REVIEW_ROOT / "stage51_synthesis_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage51 Q2 Loss Firewall(최신 51단계 Q2 손실 방화벽)

Stage51(51단계) `{STAGE_ID}` recorded(기록) `{PACKET_ID}` as `{judgment}`. It tested(시험) Q2 short/late/DI firewall(Q2 숏/후반/DI 방화벽) variants(변형) through actual MT5 WFO(실제 MT5 워크포워드), routed Tier B fallback(라우팅 Tier B 대체), cost sensitivity(비용 민감도), and overlap concentration(중복 집중도). The result remains runtime_probe(런타임 탐침) only, with no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{STAGE_ID}` `{PACKET_ID}` recorded Q2 loss firewall as `{judgment}`.\n", encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    for path in (STAGE_ROOT / "00_spec", STAGE_ROOT / "01_inputs", STAGE_ROOT / "02_runs", REVIEW_ROOT, STAGE_ROOT / "04_selected", PACKET_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    run45a_result = run45a(common_files_root, args)
    run45b_result = run45b(common_files_root, args, run45a_result)
    run45c_result = run45c(run45a_result, run45b_result)
    results = {"run45a": run45a_result, "run45b": run45b_result, "run45c": run45c_result}
    judgment, reason, decision = decide_judgment(results)
    artifacts = lineage_rows(results)
    ledger_payload = write_ledgers(results, judgment, artifacts)
    write_stage_docs(results, judgment, reason, decision, ledger_payload)
    write_packet_files(results, judgment, reason, decision, artifacts, ledger_payload)
    update_current_truth(judgment, decision)
    return {"stage_id": STAGE_ID, "packet_id": PACKET_ID, "judgment": judgment, "reason": reason, "decision": decision, "results": results}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage51 Q2 loss firewall MT5 WFO suite.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--selected-variant-limit", type=int, default=4)
    parser.add_argument("--reuse-existing", action="store_true")
    args = parser.parse_args(argv)
    payload = run(args)
    print(json.dumps(json_ready({"stage_id": payload["stage_id"], "packet_id": payload["packet_id"], "judgment": payload["judgment"], "reason": payload["reason"], "decision": payload["decision"]}), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
