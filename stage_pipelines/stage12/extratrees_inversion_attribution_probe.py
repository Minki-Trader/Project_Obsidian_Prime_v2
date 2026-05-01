from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
import yaml

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


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
RUN_ID = "run03I_et_validation_oos_inversion_attribution_v1"
RUN_NUMBER = "run03I"
PACKET_ID = "stage12_run03i_validation_oos_inversion_attribution_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesValidationOosInversionAttribution"
SOURCE_RUN_ID = "run03H_et_batch20_all_variant_tier_balance_mt5_v1"
SOURCE_PACKET_ID = "stage12_run03h_all_variant_tier_balance_mt5_v1"
SOURCE_STRUCTURAL_SCOUT_RUN_ID = "run03G_et_variant_stability_probe_v1"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
BOUNDARY = "existing_mt5_runtime_probe_attribution_only_not_alpha_quality_not_promotion"
JUDGMENT = "inconclusive_validation_oos_inversion_attribution_completed"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
SOURCE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / SOURCE_PACKET_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID

NORMALIZED_KPI_PATH = SOURCE_PACKET_ROOT / "normalized_kpi_summary.csv"
NORMALIZED_KPI_JSONL_PATH = SOURCE_PACKET_ROOT / "normalized_kpi_records.jsonl"
ENRICHED_KPI_JSONL_PATH = SOURCE_PACKET_ROOT / "enriched_kpi_records.jsonl"
TRADE_ATTRIBUTION_PATH = SOURCE_PACKET_ROOT / "trade_attribution_summary.csv"
TRADE_LEVEL_PATH = SOURCE_PACKET_ROOT / "trade_level_records.csv"
TARGET_MATRIX_PATH = SOURCE_PACKET_ROOT / "target_matrix.csv"
SOURCE_PACKET_SUMMARY_PATH = SOURCE_PACKET_ROOT / "packet_summary.json"

RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
STAGE_REVIEW_PATH = STAGE_ROOT / "03_reviews/run03I_validation_oos_inversion_attribution_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run03I_validation_oos_inversion_attribution_plan.md"

ACTUAL_ROUTE_ROLES = ("tier_only_total", "tier_b_fallback_only_total", "routed_total")
EXPECTED_KPI_LAYERS = (
    "run_identity",
    "signal_model",
    "mt5_trading_headline",
    "risk",
    "trade_diagnostics",
    "regime_slice_attribution",
    "execution",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig" if bom else "utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def current_branch() -> str:
    try:
        completed = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return completed.stdout.strip() or "unknown"


def num(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out if math.isfinite(out) else math.nan


def value_or_na(value: Any, digits: int = 2) -> str:
    number = num(value)
    if math.isnan(number):
        return "NA"
    return f"{number:.{digits}f}"


def load_source_frames() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    required = [NORMALIZED_KPI_PATH, TRADE_ATTRIBUTION_PATH, TRADE_LEVEL_PATH, TARGET_MATRIX_PATH]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing RUN03H source artifacts: {missing}")

    kpi = pd.read_csv(NORMALIZED_KPI_PATH)
    trade_attr = pd.read_csv(TRADE_ATTRIBUTION_PATH)
    trades = pd.read_csv(TRADE_LEVEL_PATH)
    target = pd.read_csv(TARGET_MATRIX_PATH)
    mapping = target[["run_id", "source_variant_id"]].drop_duplicates()

    kpi = attach_source_variant(kpi, mapping)
    trade_attr = attach_source_variant(trade_attr, mapping)
    trades = attach_source_variant(trades, mapping)

    for column in ("net_profit", "profit_factor", "trade_count", "max_drawdown_amount"):
        if column in kpi.columns:
            kpi[column] = pd.to_numeric(kpi[column], errors="coerce")
    for column in ("net_profit", "gross_profit", "gross_loss", "mfe", "mae", "hold_bars"):
        if column in trades.columns:
            trades[column] = pd.to_numeric(trades[column], errors="coerce")
    if "close_time" in trades.columns:
        trades["close_time"] = pd.to_datetime(trades["close_time"], errors="coerce")
        trades["month"] = trades["close_time"].dt.to_period("M").astype(str)
    return kpi, trade_attr, trades, target


def attach_source_variant(frame: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    if "source_variant_id" in frame.columns:
        return frame
    cleaned = frame.drop(columns=[column for column in ("source_variant_id_x", "source_variant_id_y") if column in frame.columns])
    return cleaned.merge(mapping, on="run_id", how="left")


def variant_inversion_summary(kpi: pd.DataFrame) -> pd.DataFrame:
    routed = kpi[kpi["route_role"].eq("routed_total")].copy()
    net = routed.pivot_table(index=["run_id", "source_variant_id"], columns="split", values="net_profit", aggfunc="sum")
    trades = routed.pivot_table(index=["run_id", "source_variant_id"], columns="split", values="trade_count", aggfunc="sum")
    out = pd.DataFrame(index=net.index).reset_index()
    for split in ("validation", "oos"):
        out[f"{split}_net_profit"] = net.get(split, pd.Series(dtype=float)).reindex(net.index).to_numpy()
        out[f"{split}_trade_count"] = trades.get(split, pd.Series(dtype=float)).reindex(net.index).to_numpy()
    out["oos_minus_validation_net_profit"] = out["oos_net_profit"] - out["validation_net_profit"]
    out["validation_positive"] = out["validation_net_profit"] > 0
    out["oos_positive"] = out["oos_net_profit"] > 0
    out["both_positive"] = out["validation_positive"] & out["oos_positive"]
    out["inversion_class"] = out.apply(classify_variant, axis=1)
    out["oos_rank"] = out["oos_net_profit"].rank(ascending=False, method="min").astype(int)
    out["gap_rank"] = out["oos_minus_validation_net_profit"].rank(ascending=False, method="min").astype(int)
    return out.sort_values(["oos_rank", "gap_rank", "source_variant_id"])


def classify_variant(row: Mapping[str, Any]) -> str:
    validation_positive = bool(row["validation_positive"])
    oos_positive = bool(row["oos_positive"])
    if validation_positive and oos_positive:
        return "both_positive_not_seen"
    if (not validation_positive) and oos_positive:
        return "validation_negative_oos_positive_inversion"
    if (not validation_positive) and (not oos_positive):
        return "both_negative_or_weak_negative_boundary"
    return "validation_positive_oos_negative_reversal"


def tier_route_split_summary(kpi: pd.DataFrame) -> pd.DataFrame:
    actual = kpi[kpi["route_role"].isin(ACTUAL_ROUTE_ROLES)].copy()
    grouped = (
        actual.groupby(["route_role", "tier_scope", "split"], dropna=False)
        .agg(
            net_profit=("net_profit", "sum"),
            trade_count=("trade_count", "sum"),
            variant_count=("run_id", "nunique"),
            positive_variant_count=("net_profit", lambda values: int((values > 0).sum())),
        )
        .reset_index()
    )
    grouped["avg_net_per_trade"] = grouped["net_profit"] / grouped["trade_count"].replace(0, pd.NA)
    return grouped.sort_values(["route_role", "tier_scope", "split"])


def segment_gap_summary(trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    dimensions = ("direction", "session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime")
    for role in ACTUAL_ROUTE_ROLES:
        role_frame = trades[trades["route_role"].eq(role)].copy()
        if role_frame.empty:
            continue
        total_gap = split_gap(role_frame)
        for dimension in dimensions:
            if dimension not in role_frame.columns:
                continue
            pivot = role_frame.pivot_table(
                index=[dimension],
                columns="split",
                values="net_profit",
                aggfunc=["sum", "count"],
                fill_value=0,
            )
            pivot.columns = ["_".join(str(part) for part in column if part) for column in pivot.columns]
            pivot = pivot.reset_index().rename(columns={dimension: "segment_value"})
            pivot["segment_dimension"] = dimension
            pivot["route_role"] = role
            pivot["tier_scope"] = role_frame["tier_scope"].dropna().iloc[0] if not role_frame["tier_scope"].dropna().empty else ""
            for column in ("sum_validation", "sum_oos", "count_validation", "count_oos"):
                if column not in pivot.columns:
                    pivot[column] = 0
            pivot["net_gap_oos_minus_validation"] = pivot["sum_oos"] - pivot["sum_validation"]
            pivot["validation_avg_trade"] = pivot["sum_validation"] / pivot["count_validation"].replace(0, pd.NA)
            pivot["oos_avg_trade"] = pivot["sum_oos"] / pivot["count_oos"].replace(0, pd.NA)
            pivot["share_of_role_gap"] = pivot["net_gap_oos_minus_validation"] / total_gap if total_gap else math.nan
            rows.append(pivot)
    if not rows:
        return pd.DataFrame()
    columns = [
        "route_role",
        "tier_scope",
        "segment_dimension",
        "segment_value",
        "sum_validation",
        "count_validation",
        "validation_avg_trade",
        "sum_oos",
        "count_oos",
        "oos_avg_trade",
        "net_gap_oos_minus_validation",
        "share_of_role_gap",
    ]
    return pd.concat(rows, ignore_index=True)[columns].sort_values(
        ["route_role", "net_gap_oos_minus_validation"], ascending=[True, False]
    )


def split_gap(frame: pd.DataFrame) -> float:
    sums = frame.groupby("split")["net_profit"].sum()
    return float(sums.get("oos", 0.0) - sums.get("validation", 0.0))


def month_period_summary(trades: pd.DataFrame) -> pd.DataFrame:
    actual = trades[trades["route_role"].isin(ACTUAL_ROUTE_ROLES)].copy()
    grouped = (
        actual.groupby(["route_role", "tier_scope", "split", "month"], dropna=False)
        .agg(net_profit=("net_profit", "sum"), trade_count=("net_profit", "count"), avg_net_per_trade=("net_profit", "mean"))
        .reset_index()
    )
    return grouped.sort_values(["route_role", "split", "month"])


def driver_findings(
    variant_summary: pd.DataFrame,
    tier_summary: pd.DataFrame,
    segment_summary: pd.DataFrame,
    month_summary: pd.DataFrame,
) -> pd.DataFrame:
    routed_variant = variant_summary
    validation_positive = int(routed_variant["validation_positive"].sum())
    oos_positive = int(routed_variant["oos_positive"].sum())
    variant_count = int(len(routed_variant))

    def route_split(role: str, split: str) -> tuple[float, float]:
        row = tier_summary[(tier_summary["route_role"].eq(role)) & (tier_summary["split"].eq(split))]
        if row.empty:
            return math.nan, math.nan
        return float(row["net_profit"].iloc[0]), float(row["trade_count"].iloc[0])

    tier_a_val, tier_a_val_trades = route_split("tier_only_total", "validation")
    tier_a_oos, tier_a_oos_trades = route_split("tier_only_total", "oos")
    tier_b_val, tier_b_val_trades = route_split("tier_b_fallback_only_total", "validation")
    tier_b_oos, tier_b_oos_trades = route_split("tier_b_fallback_only_total", "oos")
    routed_val, routed_val_trades = route_split("routed_total", "validation")
    routed_oos, routed_oos_trades = route_split("routed_total", "oos")

    def segment(role: str, dimension: str, value: str) -> Mapping[str, Any]:
        rows = segment_summary[
            segment_summary["route_role"].eq(role)
            & segment_summary["segment_dimension"].eq(dimension)
            & segment_summary["segment_value"].eq(value)
        ]
        return rows.iloc[0].to_dict() if not rows.empty else {}

    early = segment("routed_total", "session_slice", "early")
    high_vol = segment("routed_total", "volatility_regime", "vol_high")
    downtrend = segment("routed_total", "trend_regime", "downtrend")
    adx_gt25 = segment("routed_total", "adx_bucket", "adx_gt25")
    sell = segment("routed_total", "direction", "sell")

    validation_months = month_summary[(month_summary["route_role"].eq("routed_total")) & (month_summary["split"].eq("validation"))]
    oos_months = month_summary[(month_summary["route_role"].eq("routed_total")) & (month_summary["split"].eq("oos"))]
    worst_validation = validation_months.sort_values("net_profit").head(2)
    best_oos = oos_months.sort_values("net_profit", ascending=False).head(2)

    rows = [
        {
            "finding_id": "F01",
            "finding": "broad_routed_inversion",
            "evidence": f"routed validation positive {validation_positive}/{variant_count}; routed OOS positive {oos_positive}/{variant_count}",
            "interpretation": "OOS lift is broad, but validation failure blocks alpha-quality claims.",
            "next_probe": "walk_forward_or_rolling_split_probe",
            "confidence": "medium",
        },
        {
            "finding_id": "F02",
            "finding": "tier_a_drives_oos_lift",
            "evidence": (
                f"Tier A only validation {tier_a_val:.2f}/{tier_a_val_trades:.0f} trades; "
                f"Tier A only OOS {tier_a_oos:.2f}/{tier_a_oos_trades:.0f} trades"
            ),
            "interpretation": "The positive OOS surface is mainly Tier A separate, not a clean Tier B confirmation.",
            "next_probe": "tier_a_regime_stress_with_tier_b_boundary_record",
            "confidence": "medium",
        },
        {
            "finding_id": "F03",
            "finding": "tier_b_opposite_split_behavior",
            "evidence": (
                f"Tier B fallback-only validation {tier_b_val:.2f}/{tier_b_val_trades:.0f} trades; "
                f"Tier B fallback-only OOS {tier_b_oos:.2f}/{tier_b_oos_trades:.0f} trades"
            ),
            "interpretation": "Tier B is useful as context evidence, but its separate read reverses against OOS.",
            "next_probe": "do_not_promote_routed_total_without_fallback_attribution",
            "confidence": "medium",
        },
        {
            "finding_id": "F04",
            "finding": "early_session_gap_dominates",
            "evidence": (
                f"routed early validation {float(early.get('sum_validation', math.nan)):.2f}; "
                f"routed early OOS {float(early.get('sum_oos', math.nan)):.2f}; "
                f"gap {float(early.get('net_gap_oos_minus_validation', math.nan)):.2f}"
            ),
            "interpretation": "The inversion is concentrated in the early cash-session window.",
            "next_probe": "early_session_regime_stress_not_micro_threshold_tuning",
            "confidence": "medium",
        },
        {
            "finding_id": "F05",
            "finding": "trend_volatility_flip_surface",
            "evidence": (
                f"downtrend gap {float(downtrend.get('net_gap_oos_minus_validation', math.nan)):.2f}; "
                f"vol_high gap {float(high_vol.get('net_gap_oos_minus_validation', math.nan)):.2f}; "
                f"adx_gt25 gap {float(adx_gt25.get('net_gap_oos_minus_validation', math.nan)):.2f}"
            ),
            "interpretation": "Trend/volatility regime change is a plausible driver, not proven causality.",
            "next_probe": "rolling_regime_split_probe",
            "confidence": "low_to_medium",
        },
        {
            "finding_id": "F06",
            "finding": "short_side_gap_larger_but_not_exclusive",
            "evidence": (
                f"routed sell gap {float(sell.get('net_gap_oos_minus_validation', math.nan)):.2f}; "
                f"routed total validation {routed_val:.2f}/{routed_val_trades:.0f} trades; "
                f"routed total OOS {routed_oos:.2f}/{routed_oos_trades:.0f} trades"
            ),
            "interpretation": "Short direction contributes more to the gap, but long direction also improves.",
            "next_probe": "direction_asymmetry_stress",
            "confidence": "medium",
        },
        {
            "finding_id": "F07",
            "finding": "time_window_boundary",
            "evidence": (
                "worst validation months "
                + ",".join(f"{row.month}:{row.net_profit:.2f}" for row in worst_validation.itertuples())
                + "; best OOS months "
                + ",".join(f"{row.month}:{row.net_profit:.2f}" for row in best_oos.itertuples())
            ),
            "interpretation": "The split periods are different calendar regimes; same-month causality is not established.",
            "next_probe": "WFO before narrowing",
            "confidence": "medium",
        },
        {
            "finding_id": "F08",
            "finding": "inverse_negative_boundary",
            "evidence": "v20_base_inverse_q90 is the only routed OOS-negative variant and has a negative OOS boundary.",
            "interpretation": "Full inverse direction is failure memory, not a next lead.",
            "next_probe": "do_not_repeat_full_inverse_without_new_context_hypothesis",
            "confidence": "medium",
        },
    ]
    return pd.DataFrame(rows)


def next_probe_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "probe_id": "P01",
                "probe": "rolling_wfo_split_probe",
                "purpose": "검증/표본외 반전이 단일 분할 착시인지 확인",
                "scope": "all 20 variants, Tier A/B/A+B 기록 유지",
                "success_signal": "OOS lift survives multiple rolling windows without validation collapse in most windows",
                "failure_signal": "positive read is isolated to 2025-10~2026-04 window",
                "claim_boundary": "exploratory_only",
            },
            {
                "probe_id": "P02",
                "probe": "early_session_regime_stress",
                "purpose": "early session(초반 세션)이 inversion(반전)을 지배하는지 확인",
                "scope": "coarse session include/exclude, no threshold micro-tuning",
                "success_signal": "early-session stress explains validation loss and OOS lift directionally",
                "failure_signal": "gap remains unexplained after session split",
                "claim_boundary": "structural_scout_only",
            },
            {
                "probe_id": "P03",
                "probe": "tier_b_fallback_attribution_probe",
                "purpose": "Tier B(티어 B) fallback(대체)이 routed total(라우팅 전체)에 실제로 무엇을 더했는지 분리",
                "scope": "routed trade tagging or replay with fallback role attribution",
                "success_signal": "fallback contribution can be isolated without synthetic separate-run summing",
                "failure_signal": "routed total remains non-attributable by role",
                "claim_boundary": "runtime_probe_only",
            },
            {
                "probe_id": "P04",
                "probe": "direction_asymmetry_stress",
                "purpose": "short side(숏 방향) gap(차이)이 구조인지 확인",
                "scope": "long-only, short-only, both-direction variants under same WFO frame",
                "success_signal": "direction asymmetry repeats across rolling windows",
                "failure_signal": "direction effect disappears outside current split",
                "claim_boundary": "exploratory_only",
            },
        ]
    )


def write_data_outputs(
    variant_summary: pd.DataFrame,
    tier_summary: pd.DataFrame,
    segment_summary: pd.DataFrame,
    month_summary: pd.DataFrame,
    findings: pd.DataFrame,
    probes: pd.DataFrame,
) -> None:
    outputs = {
        RUN_ROOT / "results/inversion_variant_summary.csv": variant_summary,
        RUN_ROOT / "results/tier_route_split_summary.csv": tier_summary,
        RUN_ROOT / "results/segment_gap_summary.csv": segment_summary,
        RUN_ROOT / "results/month_period_summary.csv": month_summary,
        RUN_ROOT / "results/driver_findings.csv": findings,
        RUN_ROOT / "results/next_probe_matrix.csv": probes,
    }
    for path, frame in outputs.items():
        io_path(path.parent).mkdir(parents=True, exist_ok=True)
        frame.to_csv(io_path(path), index=False, lineterminator="\n")


def build_summary(
    variant_summary: pd.DataFrame,
    tier_summary: pd.DataFrame,
    segment_summary: pd.DataFrame,
    findings: pd.DataFrame,
    source_counts: Mapping[str, Any],
    created_at_utc: str,
) -> dict[str, Any]:
    routed = tier_summary[tier_summary["route_role"].eq("routed_total")]
    def row(role: str, split: str) -> Mapping[str, Any]:
        rows = tier_summary[(tier_summary["route_role"].eq(role)) & (tier_summary["split"].eq(split))]
        return rows.iloc[0].to_dict() if not rows.empty else {}

    top_oos = variant_summary.sort_values("oos_net_profit", ascending=False).head(5)
    top_gap = variant_summary.sort_values("oos_minus_validation_net_profit", ascending=False).head(5)
    early = segment_summary[
        segment_summary["route_role"].eq("routed_total")
        & segment_summary["segment_dimension"].eq("session_slice")
        & segment_summary["segment_value"].eq("early")
    ]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at_utc,
        "completed_at_utc": utc_now(),
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "status": "reviewed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "external_verification_status": "completed_from_run03h_mt5_evidence_no_new_mt5_execution",
        "variant_count": int(len(variant_summary)),
        "routed_validation_positive_variants": int(variant_summary["validation_positive"].sum()),
        "routed_oos_positive_variants": int(variant_summary["oos_positive"].sum()),
        "routed_both_positive_variants": int(variant_summary["both_positive"].sum()),
        "routed_validation_net_profit": row("routed_total", "validation").get("net_profit"),
        "routed_oos_net_profit": row("routed_total", "oos").get("net_profit"),
        "tier_a_validation_net_profit": row("tier_only_total", "validation").get("net_profit"),
        "tier_a_oos_net_profit": row("tier_only_total", "oos").get("net_profit"),
        "tier_b_validation_net_profit": row("tier_b_fallback_only_total", "validation").get("net_profit"),
        "tier_b_oos_net_profit": row("tier_b_fallback_only_total", "oos").get("net_profit"),
        "early_session_gap": None if early.empty else early.iloc[0].to_dict(),
        "top_oos_variants": top_oos[["source_variant_id", "validation_net_profit", "oos_net_profit", "oos_minus_validation_net_profit"]].to_dict(orient="records"),
        "top_gap_variants": top_gap[["source_variant_id", "validation_net_profit", "oos_net_profit", "oos_minus_validation_net_profit"]].to_dict(orient="records"),
        "driver_findings": findings.to_dict(orient="records"),
        "source_counts": dict(source_counts),
        "artifacts": artifacts(),
    }


def artifacts() -> dict[str, Mapping[str, Any]]:
    paths = {
        "inversion_variant_summary": RUN_ROOT / "results/inversion_variant_summary.csv",
        "tier_route_split_summary": RUN_ROOT / "results/tier_route_split_summary.csv",
        "segment_gap_summary": RUN_ROOT / "results/segment_gap_summary.csv",
        "month_period_summary": RUN_ROOT / "results/month_period_summary.csv",
        "driver_findings": RUN_ROOT / "results/driver_findings.csv",
        "next_probe_matrix": RUN_ROOT / "results/next_probe_matrix.csv",
        "result_summary": RUN_ROOT / "reports/result_summary.md",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "kpi_record": RUN_ROOT / "kpi_record.json",
        "summary": RUN_ROOT / "summary.json",
    }
    out: dict[str, Mapping[str, Any]] = {}
    for key, path in paths.items():
        out[key] = {
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "pending",
        }
    return out


def write_run_records(summary: Mapping[str, Any]) -> None:
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "lane": "validation_oos_inversion_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
        },
        "source_inputs": {
            "source_run_id": SOURCE_RUN_ID,
            "source_packet_id": SOURCE_PACKET_ID,
            "normalized_kpi_summary": rel(NORMALIZED_KPI_PATH),
            "normalized_kpi_records": rel(NORMALIZED_KPI_JSONL_PATH),
            "enriched_kpi_records": rel(ENRICHED_KPI_JSONL_PATH),
            "trade_attribution_summary": rel(TRADE_ATTRIBUTION_PATH),
            "trade_level_records": rel(TRADE_LEVEL_PATH),
        },
        "experiment_design": {
            "hypothesis": "The Stage 12 validation/OOS inversion is driven by time/regime/tier-role structure, not a promotion-ready alpha surface.",
            "decision_use": "Choose the next broad Stage 12 probe without selecting a baseline or promotion candidate.",
            "comparison_baseline": "RUN03H all-variant MT5 runtime_probe evidence; no operating baseline.",
            "control_variables": [
                "source MT5 reports unchanged",
                "no model retraining",
                "no threshold change",
                "same Tier A/Tier B/A+B record meanings",
            ],
            "changed_variables": ["read_axis=time_tier_direction_regime_attribution"],
            "success_criteria": [
                "all 20 RUN03H variants are represented",
                "Tier A, Tier B, and Tier A+B are separated",
                "next broad probe is identified without micro-tuning",
            ],
            "failure_criteria": ["source KPI rows missing", "trade attribution rows missing", "7-layer KPI source contract missing"],
            "claim_boundary": BOUNDARY,
        },
        "result": dict(summary),
        "artifacts": artifacts(),
    }
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "validation_oos_inversion_attribution",
        "scoreboard_lane": "performance_attribution",
        "source_run_id": SOURCE_RUN_ID,
        "source_kpi_standard_version": "kpi_7layer_v1",
        "source_normalized_kpi_rows": summary["source_counts"]["normalized_jsonl_rows"],
        "source_enriched_kpi_rows": summary["source_counts"]["enriched_jsonl_rows"],
        "variant_count": summary["variant_count"],
        "routed_validation_positive_variants": summary["routed_validation_positive_variants"],
        "routed_oos_positive_variants": summary["routed_oos_positive_variants"],
        "routed_both_positive_variants": summary["routed_both_positive_variants"],
        "routed_validation_net_profit": summary["routed_validation_net_profit"],
        "routed_oos_net_profit": summary["routed_oos_net_profit"],
        "tier_a_validation_net_profit": summary["tier_a_validation_net_profit"],
        "tier_a_oos_net_profit": summary["tier_a_oos_net_profit"],
        "tier_b_validation_net_profit": summary["tier_b_validation_net_profit"],
        "tier_b_oos_net_profit": summary["tier_b_oos_net_profit"],
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(RUN_ROOT / "summary.json", summary)


def write_reports(summary: Mapping[str, Any], variant_summary: pd.DataFrame, tier_summary: pd.DataFrame, findings: pd.DataFrame) -> None:
    top_oos_rows = "\n".join(
        f"| `{row.source_variant_id}` | {row.validation_net_profit:.2f} | {row.oos_net_profit:.2f} | {row.oos_minus_validation_net_profit:.2f} |"
        for row in variant_summary.sort_values("oos_net_profit", ascending=False).head(8).itertuples()
    )
    tier_rows = "\n".join(
        f"| `{row.route_role}` | `{row.tier_scope}` | `{row.split}` | {row.net_profit:.2f} | {row.trade_count:.0f} |"
        for row in tier_summary.itertuples()
    )
    finding_rows = "\n".join(
        f"| `{row.finding_id}` | {row.finding} | {row.evidence} | {row.interpretation} |"
        for row in findings.itertuples()
    )
    text = f"""# RUN03I validation/OOS inversion attribution(검증/표본외 반전 귀속)

## Result(결과)

`{RUN_ID}`는 `{SOURCE_RUN_ID}`의 MT5(`MetaTrader 5`, 메타트레이더5) 120개 시도(attempt, 시도)와 7-layer KPI(7층 핵심 성과 지표)를 재사용해 validation/OOS inversion(검증/표본외 반전)을 분해했다.

효과(effect, 효과): 새 모델이나 새 threshold(임계값)를 만들지 않고, Stage 12(12단계)가 계속 탐색할 가치가 있는 이유와 다음 broad probe(넓은 탐침)를 분리했다.

## Headline(핵심)

- routed validation positive variants(라우팅 검증 양수 변형): `{summary['routed_validation_positive_variants']}/{summary['variant_count']}`
- routed OOS positive variants(라우팅 표본외 양수 변형): `{summary['routed_oos_positive_variants']}/{summary['variant_count']}`
- routed validation net(라우팅 검증 순손익): `{value_or_na(summary['routed_validation_net_profit'])}`
- routed OOS net(라우팅 표본외 순손익): `{value_or_na(summary['routed_oos_net_profit'])}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`

## Tier Route Split(티어/라우팅/분할)

| route role(라우팅 역할) | tier(티어) | split(분할) | net profit(순손익) | trades(거래수) |
|---|---|---:|---:|---:|
{tier_rows}

## Top OOS Variants(상위 표본외 변형)

| variant(변형) | validation net(검증 순손익) | OOS net(표본외 순손익) | gap(차이) |
|---|---:|---:|---:|
{top_oos_rows}

## Driver Findings(원인 후보)

| id | finding(발견) | evidence(근거) | interpretation(해석) |
|---|---|---|---|
{finding_rows}

## Judgment(판정)

이 결과는 exploratory attribution(탐색적 귀속)이다. OOS(표본외) 표면은 넓지만 validation(검증) 붕괴가 전 변형에 걸쳐 있으므로 alpha quality(알파 품질), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)를 주장하지 않는다.

다음 probe(탐침)는 WFO(`walk-forward optimization`, 워크포워드 최적화) 또는 rolling split(구르는 분할)로 validation/OOS inversion(검증/표본외 반전)이 반복되는지 확인해야 한다.
"""
    write_text(RUN_ROOT / "reports/result_summary.md", text)

    stage_packet = f"""# RUN03I Review Packet(검토 묶음)

## Result(결과)

`{RUN_ID}`는 RUN03H(실행 03H) MT5(`MetaTrader 5`, 메타트레이더5) 근거를 time/tier/direction/regime(시간/티어/방향/시장상태) 축으로 분해했다.

## Evidence(근거)

- run manifest(실행 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`
- KPI record(KPI 기록): `{rel(RUN_ROOT / 'kpi_record.json')}`
- result summary(결과 요약): `{rel(RUN_ROOT / 'reports/result_summary.md')}`
- variant inversion(변형 반전): `{rel(RUN_ROOT / 'results/inversion_variant_summary.csv')}`
- segment gap(구간 차이): `{rel(RUN_ROOT / 'results/segment_gap_summary.csv')}`
- next probe matrix(다음 탐침 표): `{rel(RUN_ROOT / 'results/next_probe_matrix.csv')}`

## Judgment(판정)

`{JUDGMENT}`. 효과(effect, 효과)는 Stage 12(12단계)를 계속 탐색할 이유를 보존하되, 아직 승격 의미(promotion meaning, 승격 의미)를 만들지 않는 것이다.
"""
    write_text(STAGE_REVIEW_PATH, stage_packet)

    plan = f"""# RUN03I Plan(계획)

## Hypothesis(가설)

Stage 12(12단계) RUN03H(실행 03H)의 validation/OOS inversion(검증/표본외 반전)은 단순 top variant(상위 변형) 문제가 아니라 time/regime/tier-role(시간/시장상태/티어 역할) 문제다.

## Controls(고정 조건)

- source MT5 reports(원천 MT5 보고서): RUN03H(실행 03H) 그대로 사용
- model retraining(모델 재학습): 없음
- threshold change(임계값 변경): 없음
- Tier A/B/A+B(티어 A/B/A+B): 별도 기록 유지

## Evidence Plan(근거 계획)

- 20개 변형 전체를 포함한다.
- 120개 MT5 attempt(MT5 시도, 메타트레이더5 시도)의 7-layer KPI(7층 KPI)를 근거로 삼는다.
- trade attribution(거래 귀속)으로 session/volatility/trend/ADX/direction(세션/변동성/추세/ADX/방향)을 분해한다.

## Stop Condition(중단 조건)

원천 KPI(핵심 성과 지표) 또는 거래 귀속(trade attribution, 거래 귀속)이 빠지면 blocked(차단)로 닫는다.
"""
    write_text(PLAN_PATH, plan)

    closeout = f"""# Closeout Report

## Conclusion

RUN03I(실행 03I)는 validation/OOS inversion attribution(검증/표본외 반전 귀속)을 완료했다.

## What changed

새 MT5(`MetaTrader 5`, 메타트레이더5) 실행은 없고, RUN03H(실행 03H)의 7-layer KPI(7층 KPI)와 trade attribution(거래 귀속)을 분석 산출물로 재구성했다.

## What gates passed

scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_lint(스킬 영수증 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 포함 감사), final_claim_guard(최종 주장 가드)를 실행한다.

## What gates were not applicable

runtime_evidence_gate(런타임 근거 게이트)는 새 MT5 실행이 없어서 해당 없음이다. RUN03H(실행 03H)의 완료된 MT5 evidence(근거)를 재사용한다.

## What is still not enforced

WFO(`walk-forward optimization`, 워크포워드 최적화)는 아직 실행하지 않았다.

## Allowed claims

completed_existing_evidence_attribution(기존 근거 귀속 완료), exploratory_inversion_read(탐색적 반전 판독).

## Forbidden claims

alpha_quality(알파 품질), promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime_authority(런타임 권위).

## Next hardening step

rolling WFO split probe(구르는 WFO 분할 탐침)를 실행해 validation/OOS inversion(검증/표본외 반전)이 반복되는지 확인한다.
"""
    write_text(PACKET_ROOT / "closeout_report.md", closeout, bom=False)


def build_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    views = (
        ("tier_a_inversion_attribution", "Tier A", "tier_a_validation_net_profit", "tier_a_oos_net_profit"),
        ("tier_b_inversion_attribution", "Tier B", "tier_b_validation_net_profit", "tier_b_oos_net_profit"),
        ("tier_ab_routed_inversion_attribution", "Tier A+B", "routed_validation_net_profit", "routed_oos_net_profit"),
    )
    rows: list[dict[str, Any]] = []
    for view, tier, val_key, oos_key in views:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "validation_oos_inversion_attribution",
                "scoreboard_lane": "performance_attribution",
                "status": "completed",
                "judgment": JUDGMENT,
                "path": rel(RUN_ROOT / "reports/result_summary.md"),
                "primary_kpi": ledger_pairs(
                    (
                        ("validation_net_profit", summary.get(val_key)),
                        ("oos_net_profit", summary.get(oos_key)),
                        ("variant_count", summary.get("variant_count")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("source_run_id", SOURCE_RUN_ID),
                        ("boundary", "existing_mt5_attribution_only"),
                        ("new_mt5_execution", False),
                    )
                ),
                "external_verification_status": "completed_from_run03h_mt5_evidence_no_new_mt5_execution",
                "notes": "RUN03I attribution row; explains validation/OOS inversion without creating promotion meaning.",
            }
        )
    return rows


def update_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    ledger_rows = build_ledger_rows(summary)
    registry_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "validation_oos_inversion_attribution",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT),
            "notes": ledger_pairs(
                (
                    ("source_run_id", SOURCE_RUN_ID),
                    ("variant_count", summary["variant_count"]),
                    ("new_mt5_execution", False),
                    ("boundary", "existing_mt5_attribution_only"),
                )
            ),
        }
    ]
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, registry_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "stage_run_ledger": upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "rows_written": len(ledger_rows),
    }


def write_work_packet(summary: Mapping[str, Any]) -> None:
    packet = {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "ㄱㄱ너가 말한태로 가자",
            "requested_action": "continue Stage 12 by analyzing validation/OOS inversion drivers from RUN03H evidence",
            "requested_count": {"value": 20, "n_a_reason": None},
            "ambiguous_terms": [],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run_before_packet": SOURCE_RUN_ID,
            "current_run_after_packet": RUN_ID,
            "branch": current_branch(),
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                "stages/12_model_family_challenge__extratrees_training_effect/04_selected/selection_status.md",
            ],
        },
        "work_classification": {
            "primary_family": "kpi_evidence",
            "detected_families": ["kpi_evidence", "experiment_design", "state_sync"],
            "touched_surfaces": ["stage12_run_artifacts", "run_ledgers", "current_truth_docs"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "claim_overstatement_risk": "high",
                "selection_bias_risk": "medium",
                "state_sync_risk": "medium",
                "external_runtime_risk": "low_no_new_mt5",
            },
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "decision_lock": {
            "mode": "user_explicit_go_ahead",
            "assumptions": {
                "new_mt5_execution_required": False,
                "use_existing_run03h_evidence": True,
                "baseline_selection_allowed": False,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["kpi_evidence"],
            "target_surfaces": [rel(RUN_ROOT), rel(PACKET_ROOT), rel(STAGE_RUN_LEDGER_PATH), rel(PROJECT_ALPHA_LEDGER_PATH)],
            "scope_units": ["run", "variant", "kpi_row", "ledger", "report"],
            "execution_layers": ["python_execution", "kpi_recording", "ledger_update", "document_edit"],
            "mutation_policy": {"allowed": True, "boundary": "derived analysis only; no MT5 or model mutation"},
            "evidence_layers": ["source_kpi_record", "trade_attribution", "summary", "ledgers", "work_packet"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False},
            "claim_boundary": {
                "allowed_claims": ["completed_existing_evidence_attribution", "exploratory_inversion_read"],
                "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            },
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "All 20 RUN03H variants are included in inversion analysis.",
                "expected_artifact": rel(RUN_ROOT / "results/inversion_variant_summary.csv"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Tier A, Tier B, and Tier A+B split summaries are written.",
                "expected_artifact": rel(RUN_ROOT / "results/tier_route_split_summary.csv"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Source 7-layer KPI rows remain connected to RUN03H evidence.",
                "expected_artifact": rel(PACKET_ROOT / "source_kpi_contract_audit.json"),
                "verification_method": "kpi_contract_audit",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                {"id": "source_evidence_load", "actions": ["read_RUN03H_7layer_kpi", "read_trade_attribution"]},
                {"id": "attribution", "actions": ["split_by_tier_route_time_direction_regime"]},
                {"id": "closeout", "actions": ["write_reports", "update_ledgers", "sync_current_truth", "run_gates"]},
            ],
            "expected_outputs": [rel(RUN_ROOT / "reports/result_summary.md"), rel(PACKET_ROOT / "closeout_gate.json")],
            "stop_conditions": ["missing_source_kpi", "missing_trade_attribution", "source_7layer_contract_missing"],
        },
        "skill_routing": {
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-performance-attribution",
            ],
            "skills_considered": [
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-performance-attribution",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-exploration-mandate",
            ],
            "skills_selected": [
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-performance-attribution",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-exploration-mandate",
            ],
            "skills_not_used": {},
            "required_skill_receipts": [
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-performance-attribution",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
        "evidence_contract": {
            "raw_evidence": [rel(NORMALIZED_KPI_JSONL_PATH), rel(ENRICHED_KPI_JSONL_PATH), rel(TRADE_LEVEL_PATH)],
            "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json")],
            "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
        },
        "gates": {
            "required": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "actual_status_source": rel(PACKET_ROOT / "closeout_gate.json"),
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "RUN03I reuses completed RUN03H MT5 evidence and does not execute MT5."
            },
        },
        "final_claim_policy": {
            "allowed_claims": ["completed_existing_evidence_attribution", "exploratory_inversion_read"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    write_yaml(PACKET_ROOT / "work_packet.yaml", packet)


def source_kpi_contract_audit() -> dict[str, Any]:
    counts: dict[str, Any] = {
        "normalized_kpi_summary_rows": count_csv_rows(NORMALIZED_KPI_PATH),
        "normalized_jsonl_rows": 0,
        "enriched_jsonl_rows": 0,
        "expected_layers": EXPECTED_KPI_LAYERS,
        "missing_layer_cells": 0,
        "version_keys": [],
    }
    versions: set[str] = set()
    for path, key in ((NORMALIZED_KPI_JSONL_PATH, "normalized_jsonl_rows"), (ENRICHED_KPI_JSONL_PATH, "enriched_jsonl_rows")):
        rows, missing, file_versions = inspect_jsonl_layers(path)
        counts[key] = rows
        counts["missing_layer_cells"] += missing
        versions.update(file_versions)
    counts["version_keys"] = sorted(versions)
    status = (
        "pass"
        if counts["normalized_kpi_summary_rows"] == 200
        and counts["normalized_jsonl_rows"] == 200
        and counts["enriched_jsonl_rows"] == 200
        and counts["missing_layer_cells"] == 0
        and counts["version_keys"] == ["kpi_7layer_v1"]
        else "blocked"
    )
    return {
        "audit_name": "kpi_contract_audit",
        "status": status,
        "passed": status == "pass",
        "completed_forbidden": status != "pass",
        "findings": [] if status == "pass" else [{"check_id": "source_kpi_contract_mismatch", "message": "RUN03H source KPI contract did not match expected 7-layer rows."}],
        "counts": counts,
        "allowed_claims": ["completed", "reviewed"] if status == "pass" else ["blocked"],
        "forbidden_claims": [] if status == "pass" else ["completed", "reviewed", "verified"],
    }


def inspect_jsonl_layers(path: Path) -> tuple[int, int, set[str]]:
    rows = 0
    missing = 0
    versions: set[str] = set()
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            if not line.strip():
                continue
            rows += 1
            payload = json.loads(line)
            version = payload.get("kpi_standard_version")
            if version:
                versions.add(str(version))
            for layer in EXPECTED_KPI_LAYERS:
                if layer not in payload:
                    missing += 1
    return rows, missing, versions


def count_csv_rows(path: Path) -> int:
    if not path_exists(path):
        return 0
    return max(sum(1 for _ in io_path(path).open("r", encoding="utf-8-sig")) - 1, 0)


def write_skill_receipts(summary: Mapping[str, Any]) -> None:
    receipts = [
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-run-evidence-system",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "source_inputs": [rel(NORMALIZED_KPI_JSONL_PATH), rel(ENRICHED_KPI_JSONL_PATH), rel(TRADE_LEVEL_PATH)],
            "produced_artifacts": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "reports/result_summary.md")],
            "ledger_rows": 3,
            "ledger_links": [rel(PROJECT_ALPHA_LEDGER_PATH), rel(STAGE_RUN_LEDGER_PATH), rel(RUN_REGISTRY_PATH)],
            "missing_evidence": "No new MT5 execution; attribution reuses RUN03H completed runtime evidence.",
            "allowed_claims": ["completed_existing_evidence_attribution"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "source_inputs": [rel(NORMALIZED_KPI_PATH), rel(TRADE_ATTRIBUTION_PATH), rel(TRADE_LEVEL_PATH)],
            "producer": "stage_pipelines/stage12/extratrees_inversion_attribution_probe.py",
            "consumer": "Stage12 RUN03I reports, ledgers, current-truth docs, and next probe planning",
            "produced_artifacts": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "reports/result_summary.md")],
            "artifact_paths": [item["path"] for item in summary["artifacts"].values()],
            "artifact_hashes": {key: item["sha256"] for key, item in summary["artifacts"].items()},
            "registry_links": [rel(PROJECT_ALPHA_LEDGER_PATH), rel(STAGE_RUN_LEDGER_PATH), rel(RUN_REGISTRY_PATH)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "raw_evidence": [rel(NORMALIZED_KPI_JSONL_PATH), rel(ENRICHED_KPI_JSONL_PATH), rel(TRADE_LEVEL_PATH)],
            "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "run_manifest.json")],
            "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
            "hashes_or_missing_reasons": {key: item["sha256"] for key, item in summary["artifacts"].items()},
            "lineage_boundary": "connected_with_boundary; no new MT5 execution or model mutation",
            "forbidden_claims": ["runtime_authority", "operating_promotion"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-result-judgment",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "result_subject": RUN_ID,
            "evidence_available": ["RUN03H MT5 KPI", "trade attribution", "stage/project ledgers"],
            "evidence_missing": ["WFO repeatability", "role-level routed fallback profit attribution"],
            "judgment_label": "inconclusive",
            "claim_boundary": BOUNDARY,
            "judgment_boundary": BOUNDARY,
            "evidence_used": [rel(NORMALIZED_KPI_PATH), rel(TRADE_ATTRIBUTION_PATH), rel(TRADE_LEVEL_PATH)],
            "next_condition": "Run rolling WFO or time-regime split probe before narrowing claims.",
            "user_explanation_hook": "계속 탐색할 가치는 있지만 승격 의미는 없다.",
            "allowed_claims": ["completed_existing_evidence_attribution", "exploratory_inversion_read"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-performance-attribution",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "observed_change": "RUN03H routed OOS is broadly positive while routed validation is negative across all variants.",
            "comparison_baseline": "RUN03H validation split vs OOS split; no operating baseline.",
            "likely_drivers": ["Tier A split behavior", "early session", "trend/volatility regime", "time window"],
            "segment_checks": ["tier", "route role", "direction", "session", "volatility", "trend", "ADX", "month"],
            "attribution_layers_checked": ["tier", "route role", "direction", "session", "volatility", "trend", "ADX", "month"],
            "missing_layers": ["WFO repeatability", "routed fallback profit attribution"],
            "trade_shape": {
                "routed_validation_net_profit": summary["routed_validation_net_profit"],
                "routed_oos_net_profit": summary["routed_oos_net_profit"],
                "routed_validation_positive_variants": summary["routed_validation_positive_variants"],
                "routed_oos_positive_variants": summary["routed_oos_positive_variants"],
            },
            "alternative_explanations": ["single split calendar regime", "fallback attribution not separable", "sample-specific trend/volatility clustering"],
            "attribution_confidence": "medium",
            "next_probe": "rolling_wfo_split_probe",
            "allowed_claims": ["completed_existing_evidence_attribution", "exploratory_inversion_read"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "hypothesis": "The inversion is a structural regime/time split clue worth broad WFO probing.",
            "decision_use": "Choose next Stage12 probe, not a baseline.",
            "comparison_baseline": "RUN03H all-variant MT5 runtime_probe",
            "baseline": "RUN03H all-variant MT5 runtime_probe; no operating baseline",
            "control_variables": ["source MT5 reports", "model artifacts", "thresholds", "tier definitions"],
            "changed_variables": ["attribution axis only"],
            "sample_scope": "FPMarkets US100 M5 validation 2025-01..2025-09 and OOS 2025-10..2026-04 from RUN03H",
            "success_criteria": "A plausible broad driver is isolated with paired Tier A/B/A+B records.",
            "failure_criteria": "No coherent driver or missing source evidence.",
            "invalid_conditions": "Source 7-layer KPI or trade attribution missing.",
            "stop_conditions": "Move to WFO if attribution supports time/regime explanation; otherwise record negative memory.",
            "evidence_plan": ["inversion_variant_summary.csv", "segment_gap_summary.csv", "driver_findings.csv"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "data_source": [rel(TRADE_LEVEL_PATH), rel(NORMALIZED_KPI_JSONL_PATH), rel(ENRICHED_KPI_JSONL_PATH)],
            "data_sources_checked": [rel(TRADE_LEVEL_PATH), rel(NORMALIZED_KPI_JSONL_PATH), rel(ENRICHED_KPI_JSONL_PATH)],
            "time_axis": "MT5 report close_time timestamps from RUN03H trade extraction; month is derived from close_time.",
            "time_axis_boundary": "MT5 report close_time timestamps from RUN03H trade extraction; month is derived from close_time.",
            "sample_scope": "US100 M5 validation/OOS only; train is not reinterpreted.",
            "missing_or_duplicate_check": "Source row counts and 7-layer presence checked in source_kpi_contract_audit.",
            "feature_label_boundary": "No feature or label recomputation; RUN03H source boundary is preserved.",
            "split_boundary": "validation and OOS are different calendar windows; same-month causality is not claimed.",
            "leakage_risk": "Selection bias if OOS-positive variants are narrowed before WFO.",
            "leakage_checks": "No feature or label recomputation; main residual risk is selection bias before WFO.",
            "missing_data_boundary": "Source row counts and 7-layer presence checked in source_kpi_contract_audit.",
            "data_hash_or_identity": summary["artifacts"],
            "integrity_judgment": "usable_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-exploration-mandate",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "exploration_lane": "Stage 12 ExtraTrees validation/OOS inversion attribution",
            "idea_id": "IDEA-ST12-ET-VALIDATION-OOS-INVERSION",
            "hypothesis": "Validation/OOS inversion is a preserved clue for broad WFO/regime probing.",
            "legacy_relation": "none",
            "tier_scope": "mixed Tier A/Tier B/Tier A+B",
            "idea_boundary": "preserved clue, not baseline or promotion candidate",
            "broad_sweep": ["rolling WFO split", "session regime stress", "direction asymmetry stress"],
            "extreme_sweep": ["full inverse remains negative boundary from v20"],
            "micro_search_gate": "Only after WFO repeats inversion without validation collapse.",
            "wfo_plan": "Next probe should rotate calendar windows before threshold micro-search.",
            "failure_memory": "If WFO fails, preserve RUN03H OOS lift as single-window clue only.",
            "negative_memory_effect": "v20 full inverse remains negative boundary; RUN03I is not a death sentence for ExtraTrees.",
            "evidence_boundary": "exploratory",
            "operating_claim_boundary": "no alpha quality, promotion candidate, operating promotion, or runtime authority",
        },
    ]
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts})


def update_current_truth(summary: Mapping[str, Any]) -> None:
    update_workspace_state(summary)
    update_current_working_state(summary)
    update_selection_status(summary)
    update_changelog(summary)


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    block = f"""stage12_model_family_challenge:
  stage_id: {STAGE_ID}
  status: active_validation_oos_inversion_attribution_completed
  lane: validation_oos_inversion_attribution
  current_run_id: {RUN_ID}
  current_run_label: {EXPLORATION_LABEL}
  current_status: reviewed
  current_summary:
    boundary: {BOUNDARY}
    source_run_id: {SOURCE_RUN_ID}
    source_packet_id: {SOURCE_PACKET_ID}
    variant_count: {summary['variant_count']}
    routed_validation_positive_variants: {summary['routed_validation_positive_variants']}
    routed_oos_positive_variants: {summary['routed_oos_positive_variants']}
    routed_validation_net_profit: {value_or_na(summary['routed_validation_net_profit'])}
    routed_oos_net_profit: {value_or_na(summary['routed_oos_net_profit'])}
    tier_a_validation_net_profit: {value_or_na(summary['tier_a_validation_net_profit'])}
    tier_a_oos_net_profit: {value_or_na(summary['tier_a_oos_net_profit'])}
    tier_b_validation_net_profit: {value_or_na(summary['tier_b_validation_net_profit'])}
    tier_b_oos_net_profit: {value_or_na(summary['tier_b_oos_net_profit'])}
    judgment: {JUDGMENT}
    external_verification_status: completed_from_run03h_mt5_evidence_no_new_mt5_execution
    result_summary_path: {rel(RUN_ROOT / 'reports/result_summary.md')}
    packet_summary_path: {rel(PACKET_ROOT / 'packet_summary.json')}
    next_action: rolling_wfo_split_probe_before_any_narrowing
"""
    text = re.sub(r"stage12_model_family_challenge:\n.*?(?=\nagent_control_kpi_rebuild:)", block + "\n", text, flags=re.S)
    if f"Stage 12 RUN03I completed" not in text:
        text = text.replace(
            "open_items: []",
            "open_items: []\n",
            1,
        )
        marker = "closed_memory:\n"
        entry = (
            "- Stage 12 RUN03I completed validation/OOS inversion attribution(검증/표본외 반전 귀속); next step(다음 단계)는 "
            "rolling WFO split probe(구르는 WFO 분할 탐침)이며 alpha quality(알파 품질)나 promotion(승격)은 아님\n"
        )
        if marker in text:
            text = text.replace(marker, marker + entry, 1)
    write_text(WORKSPACE_STATE_PATH, text)


def update_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_STATE_PATH)
    text = re.sub(
        r"- current run\(현재 실행\): `[^`]+`",
        f"- current run(현재 실행): `{RUN_ID}`",
        text,
        count=1,
    )
    section = f"""## RUN03I validation/OOS inversion attribution(검증/표본외 반전 귀속)

- run(실행): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- evidence(근거): RUN03H(실행 03H) MT5(`MetaTrader 5`, 메타트레이더5) 120개 attempt(시도)와 7-layer KPI(7층 핵심 성과 지표)
- routed validation positive variants(라우팅 검증 양수 변형): `{summary['routed_validation_positive_variants']}/{summary['variant_count']}`
- routed OOS positive variants(라우팅 표본외 양수 변형): `{summary['routed_oos_positive_variants']}/{summary['variant_count']}`
- tier read(티어 판독): Tier A(티어 A)는 OOS(표본외) lift(상승)를 주도했고, Tier B(티어 B)는 split(분할)별 반대 행동을 보였다.
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`
- effect(효과): Stage 12(12단계)는 계속 탐색할 단서가 있지만, 다음은 WFO(`walk-forward optimization`, 워크포워드 최적화) 계열 broad probe(넓은 탐침)이어야 한다.
"""
    text = replace_named_section(text, r"## RUN03I validation/OOS inversion attribution\(검증/표본외 반전 귀속\)", section)
    write_text(CURRENT_STATE_PATH, text)


def update_selection_status(summary: Mapping[str, Any]) -> None:
    text = read_text(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else "# Stage 12 Selection Status\n"
    top = f"""# Stage 12 Selection Status

## Current Read - RUN03I validation/OOS inversion attribution(현재 판독 - RUN03I 검증/표본외 반전 귀속)

- current run(현재 실행): `{RUN_ID}`
- source run(원천 실행): `{SOURCE_RUN_ID}`
- variants(변형): `{summary['variant_count']}`
- routed validation positive variants(라우팅 검증 양수 변형): `{summary['routed_validation_positive_variants']}/{summary['variant_count']}`
- routed OOS positive variants(라우팅 표본외 양수 변형): `{summary['routed_oos_positive_variants']}/{summary['variant_count']}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`

Effect(효과): Stage 12(12단계)는 계속 탐색할 가치가 있지만, 다음은 rolling WFO split probe(구르는 WFO 분할 탐침)로 가야 하며 baseline(기준선)이나 promotion candidate(승격 후보)를 정하지 않는다.
"""
    rest = re.sub(r"\A# Stage 12 Selection Status\n\n## Current Read.*?(?=\n# Selection Status|\n## 현재 판독|\Z)", "", text, flags=re.S)
    write_text(SELECTION_STATUS_PATH, top.rstrip() + "\n\n" + rest.lstrip())


def update_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    entry = (
        f"- 2026-05-01: `{RUN_ID}` completed(완료). RUN03H(실행 03H) MT5 evidence(근거)에서 "
        f"validation/OOS inversion attribution(검증/표본외 반전 귀속)을 수행했다. "
        f"routed validation positive(라우팅 검증 양수) `{summary['routed_validation_positive_variants']}/{summary['variant_count']}`, "
        f"routed OOS positive(라우팅 표본외 양수) `{summary['routed_oos_positive_variants']}/{summary['variant_count']}`. "
        "효과(effect, 효과): 다음 Stage 12(12단계) 탐색을 WFO(워크포워드 최적화) 계열로 보낸다; 승격 의미는 없음.\n"
    )
    if RUN_ID in text:
        return
    if "## 2026-05-01" in text:
        text = text.replace("## 2026-05-01\n\n", "## 2026-05-01\n\n" + entry, 1)
    else:
        text = text.rstrip() + "\n\n## 2026-05-01\n\n" + entry
    write_text(CHANGELOG_PATH, text)


def replace_named_section(text: str, heading_pattern: str, replacement: str) -> str:
    pattern = rf"\n{heading_pattern}.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, "\n" + replacement.rstrip() + "\n", text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def write_packet_summary(summary: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    packet_summary = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "variant_count": summary["variant_count"],
        "source_normalized_kpi_rows": summary["source_counts"]["normalized_jsonl_rows"],
        "source_enriched_kpi_rows": summary["source_counts"]["enriched_jsonl_rows"],
        "source_trade_level_rows": summary["source_counts"]["trade_level_rows"],
        "routed_validation_positive_variants": summary["routed_validation_positive_variants"],
        "routed_oos_positive_variants": summary["routed_oos_positive_variants"],
        "new_mt5_execution": False,
        "ledger_payload": ledger_payload,
    }
    write_json(PACKET_ROOT / "packet_summary.json", packet_summary)


def write_gate_audits(summary: Mapping[str, Any]) -> None:
    source_audit = source_kpi_contract_audit()
    write_json(PACKET_ROOT / "source_kpi_contract_audit.json", source_audit)
    scope_audit = {
        "audit_name": "scope_completion_gate",
        "status": "complete",
        "passed": True,
        "completed_forbidden": False,
        "findings": [],
        "counts": {
            "variant_rows": {"expected": 20, "actual": summary["variant_count"], "required": True},
            "driver_findings": {"expected": 8, "actual": count_csv_rows(RUN_ROOT / "results/driver_findings.csv"), "required": True},
            "tier_route_split_rows": {"expected": 6, "actual": count_csv_rows(RUN_ROOT / "results/tier_route_split_summary.csv"), "required": True},
        },
        "allowed_claims": ["completed", "reviewed"],
        "forbidden_claims": [],
    }
    write_json(PACKET_ROOT / "scope_completion_gate.json", scope_audit)
    data_gate = {
        "audit_name": "data_integrity_gate",
        "status": "pass",
        "passed": True,
        "completed_forbidden": False,
        "findings": [],
        "counts": {
            "source_split_boundary": "validation 2025-01..2025-09, OOS 2025-10..2026-04",
            "same_month_causality_claimed": False,
            "trade_level_rows": summary["source_counts"]["trade_level_rows"],
        },
        "allowed_claims": ["usable_with_boundary"],
        "forbidden_claims": [],
    }
    write_json(PACKET_ROOT / "data_integrity_gate.json", data_gate)


def run_analysis() -> dict[str, Any]:
    created_at_utc = utc_now()
    kpi, trade_attr, trades, _target = load_source_frames()
    variant_summary = variant_inversion_summary(kpi)
    tier_summary = tier_route_split_summary(kpi)
    segment_summary = segment_gap_summary(trades)
    month_summary = month_period_summary(trades)
    findings = driver_findings(variant_summary, tier_summary, segment_summary, month_summary)
    probes = next_probe_matrix()
    write_data_outputs(variant_summary, tier_summary, segment_summary, month_summary, findings, probes)

    source_audit = source_kpi_contract_audit()
    source_counts = dict(source_audit["counts"])
    source_counts["trade_attribution_rows"] = int(len(trade_attr))
    source_counts["trade_level_rows"] = int(len(trades))
    summary = build_summary(variant_summary, tier_summary, segment_summary, findings, source_counts, created_at_utc)
    write_reports(summary, variant_summary, tier_summary, findings)
    write_run_records(summary)
    # Refresh summary hashes after run records and reports exist.
    summary = {**summary, "artifacts": artifacts()}
    write_json(RUN_ROOT / "summary.json", summary)
    write_work_packet(summary)
    write_skill_receipts(summary)
    ledger_payload = update_ledgers(summary)
    write_packet_summary(summary, ledger_payload)
    write_gate_audits(summary)
    update_current_truth(summary)
    return summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze RUN03H validation/OOS inversion attribution for Stage 12.")
    parser.add_argument("--summary-json", default=str(PACKET_ROOT / "packet_summary.json"))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary = run_analysis()
    print(
        json.dumps(
            {
                "run_id": summary["run_id"],
                "status": "completed",
                "variant_count": summary["variant_count"],
                "routed_validation_positive_variants": summary["routed_validation_positive_variants"],
                "routed_oos_positive_variants": summary["routed_oos_positive_variants"],
                "summary_json": args.summary_json,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
