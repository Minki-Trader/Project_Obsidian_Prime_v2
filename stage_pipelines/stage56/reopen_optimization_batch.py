from __future__ import annotations

import argparse
import csv
import json
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_trade_attribution import (  # noqa: E402
    MarketData,
    compute_trade_attribution,
)
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402
from stage_pipelines.stage56 import deep_repair_suite as deep  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50E"
PARENT_RUN_ID = "run50E_stage56_density_reentry_tier_b_disablement_v1"
PACKET_ID = "stage56_run50E_density_reentry_tier_b_disablement_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__DensityReentryTierBDisablement"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
REPORT_PATH = REVIEWS_ROOT / "run50E_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50E_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50E_audit.csv"
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")
D390H10_SUMMARY_PATH = (
    STAGE_ROOT / "02_runs/run50D/d390h10/summary.json"
)
VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0


@dataclass(frozen=True)
class BatchVariant:
    variant_id: str
    group: str
    tier_a_short_threshold: float
    tier_a_long_threshold: float
    tier_a_min_margin: float
    tier_b_short_threshold: float
    tier_b_long_threshold: float
    tier_b_min_margin: float
    max_hold_bars: int
    routed_fallback_enabled: bool
    session_slice_id: str | None = None
    tier_b_allowed_subtypes: tuple[str, ...] = ()
    notes: str = ""

    @property
    def base_id(self) -> str:
        text = self.variant_id
        for suffix in ("_aonly", "_ab_b040", "_ab_b042"):
            if text.endswith(suffix):
                return text[: -len(suffix)]
        return text

    def to_deep_variant(self) -> deep.RepairVariant:
        return deep.RepairVariant(
            self.variant_id,
            self.group,
            self.tier_a_short_threshold,
            self.tier_a_long_threshold,
            self.tier_a_min_margin,
            self.tier_b_short_threshold,
            self.tier_b_long_threshold,
            self.tier_b_min_margin,
            self.max_hold_bars,
            session_slice_id=self.session_slice_id,
            tier_b_allowed_subtypes=self.tier_b_allowed_subtypes,
            notes=self.notes,
        )


DEFAULT_VARIANTS: tuple[BatchVariant, ...] = (
    BatchVariant("d390h10_aonly", "tier_b_disablement", 0.390, 0.390, 0.0, 0.400, 0.400, 0.0, 10, False, notes="d390h10 A-only comparison for Tier B damage"),
    BatchVariant("d380h08_aonly", "hold_compression", 0.380, 0.380, 0.0, 0.400, 0.400, 0.0, 8, False, notes="d38 shorter hold without Tier B"),
    BatchVariant("d370h08_aonly", "hold_compression", 0.370, 0.370, 0.0, 0.400, 0.400, 0.0, 8, False, notes="density repair without Tier B"),
    BatchVariant("d360h07_aonly", "hold_compression", 0.360, 0.360, 0.0, 0.400, 0.400, 0.0, 7, False, notes="density repair plus shorter hold"),
    BatchVariant("d350h06_aonly", "hold_compression", 0.350, 0.350, 0.0, 0.400, 0.400, 0.0, 6, False, notes="near d35h07 density with A-only routing"),
    BatchVariant("d340h06_aonly", "density_frontier_audit", 0.340, 0.340, 0.0, 0.400, 0.400, 0.0, 6, False, notes="prior dense frontier retest with B disabled"),
    BatchVariant("d335h06_aonly", "density_frontier_audit", 0.335, 0.335, 0.0, 0.400, 0.400, 0.0, 6, False, notes="extra density pressure with B disabled"),
    BatchVariant("d350h06_ab_b040", "tier_b_comparison", 0.350, 0.350, 0.0, 0.400, 0.400, 0.0, 6, True, notes="matched A+B comparison with stricter Tier B"),
    BatchVariant("d340h06_ab_b040", "tier_b_comparison", 0.340, 0.340, 0.0, 0.400, 0.400, 0.0, 6, True, notes="matched dense A+B comparison with stricter Tier B"),
)


def _configure_deep_globals() -> None:
    deep.RUN_NUMBER = RUN_NUMBER
    deep.PARENT_RUN_ID = PARENT_RUN_ID
    deep.PACKET_ID = PACKET_ID
    deep.EXPLORATION_LABEL = EXPLORATION_LABEL
    deep.RUN_ROOT = RUN_ROOT
    deep.REPORT_PATH = REPORT_PATH
    deep.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    deep.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    deep.STAGE_RUN_LEDGER_PATH = STAGE_RUN_LEDGER_PATH
    deep.PROJECT_ALPHA_LEDGER_PATH = PROJECT_ALPHA_LEDGER_PATH
    deep.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH


def _read_json(path: Path) -> Any:
    return json.loads(_project_path(path).read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _write_bom_text(path: Path, lines: Sequence[str]) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def _project_path(path: Path) -> Path:
    resolved = path if path.is_absolute() else REPO_ROOT / path
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def _metric(summary: Mapping[str, Any], record_view: str, metric: str) -> Any:
    record = deep._record_by_view(summary, record_view)
    metrics = record.get("metrics", {}) if isinstance(record, Mapping) else {}
    return metrics.get(metric) if isinstance(metrics, Mapping) else None


def _float(value: Any, default: float = 0.0) -> float:
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _days_for_view(record_view: str) -> float:
    return VALIDATION_DAYS if "validation" in record_view else OOS_DAYS


def _resolve(path_text: Any) -> Path | None:
    if not path_text:
        return None
    path = Path(str(path_text))
    return path if path.is_absolute() else REPO_ROOT / path


def _path_exists(path: Path) -> bool:
    return _project_path(path).exists()


def _select_variants(
    *,
    selected_ids: Iterable[str] | None,
    selected_groups: Iterable[str] | None,
    max_variants: int | None,
) -> tuple[BatchVariant, ...]:
    selected = list(DEFAULT_VARIANTS)
    if selected_groups:
        wanted_groups = {group.strip() for group in selected_groups if group.strip()}
        selected = [variant for variant in selected if variant.group in wanted_groups]
    if selected_ids:
        wanted = {variant_id.strip() for variant_id in selected_ids if variant_id.strip()}
        selected = [variant for variant in selected if variant.variant_id in wanted]
        missing = sorted(wanted.difference(variant.variant_id for variant in selected))
        if missing:
            raise ValueError(f"Unknown variant ids: {missing}")
    if max_variants is not None:
        selected = selected[: int(max_variants)]
    if not selected:
        raise ValueError("At least one variant is required.")
    return tuple(selected)


def _split_values(values: Sequence[str]) -> tuple[str, ...]:
    parts: list[str] = []
    for value in values:
        parts.extend(part.strip() for part in str(value).split(",") if part.strip())
    return tuple(parts)


def _run_variant(
    variant: BatchVariant,
    *,
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    force: bool,
) -> dict[str, Any]:
    deep_variant = variant.to_deep_variant()
    result = deep._run_variant(
        deep_variant,
        attempt_mt5=attempt_mt5,
        routed_fallback_enabled=variant.routed_fallback_enabled,
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
        terminal_path=terminal_path,
        metaeditor_path=metaeditor_path,
        force=force,
    )
    result["variant_id"] = variant.variant_id
    result["variant_spec"] = {
        "group": variant.group,
        "base_id": variant.base_id,
        "routed_fallback_enabled": variant.routed_fallback_enabled,
        "tier_a_short_threshold": variant.tier_a_short_threshold,
        "tier_a_long_threshold": variant.tier_a_long_threshold,
        "tier_a_min_margin": variant.tier_a_min_margin,
        "tier_b_short_threshold": variant.tier_b_short_threshold,
        "tier_b_long_threshold": variant.tier_b_long_threshold,
        "tier_b_min_margin": variant.tier_b_min_margin,
        "max_hold_bars": variant.max_hold_bars,
        "session_slice_id": variant.session_slice_id,
        "tier_b_allowed_subtypes": list(variant.tier_b_allowed_subtypes),
    }
    return result


def _augment_rows(rows: list[dict[str, Any]], variants: Sequence[BatchVariant]) -> None:
    by_id = {variant.variant_id: variant for variant in variants}
    for row in rows:
        variant = by_id.get(str(row.get("variant_id") or ""))
        row["base_id"] = "" if variant is None else variant.base_id
        row["routed_fallback_enabled"] = "" if variant is None else str(variant.routed_fallback_enabled).lower()
        summary_path = Path(str(row.get("summary_path") or "")) if row.get("summary_path") else None
        summary = _read_json(summary_path) if summary_path and summary_path.exists() else {}
        for stem, view in (
            ("routed_validation", "mt5_routed_total_validation_is"),
            ("routed_oos", "mt5_routed_total_oos"),
        ):
            row[f"{stem}_report_path"] = _metric(summary, view, "report_path") or ""
            row[f"{stem}_aggregation"] = _metric(summary, view, "aggregation") or ""


def _trade_rows(report_path: Path, market_data: MarketData) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    parsed = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(parsed["deals"])
    if not trades:
        return [], parsed.get("summary", {})
    payload = compute_trade_attribution(trades, market_data)
    return list(payload.get("trades", [])), parsed.get("summary", {})


def _profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    gross_profit = sum(max(_float(row.get("net_profit")), 0.0) for row in rows)
    gross_loss = sum(min(_float(row.get("net_profit")), 0.0) for row in rows)
    if gross_loss == 0.0:
        return None if gross_profit == 0.0 else 999.0
    return gross_profit / abs(gross_loss)


def _same_direction_reentries(rows: Sequence[Mapping[str, Any]], window_bars: int) -> tuple[int, set[int]]:
    ordered = sorted(rows, key=lambda row: row["open_time"])
    last_close_by_direction: dict[str, Any] = {}
    reentry_indices: set[int] = set()
    for row in ordered:
        direction = str(row.get("direction"))
        previous_close = last_close_by_direction.get(direction)
        if previous_close is not None:
            bars_after_close = (row["open_time"] - previous_close).total_seconds() / 60.0 / 5.0
            if 0.0 <= bars_after_close <= float(window_bars):
                reentry_indices.add(int(row["trade_index"]))
        last_close_by_direction[direction] = row["close_time"]
    return len(reentry_indices), reentry_indices


def _cooldown_metrics(rows: Sequence[Mapping[str, Any]], *, days: float, window_bars: int = 12) -> dict[str, Any]:
    _, blocked_indices = _same_direction_reentries(rows, window_bars)
    filtered = [row for row in rows if int(row["trade_index"]) not in blocked_indices]
    net = sum(_float(row.get("net_profit")) for row in filtered)
    trade_count = len(filtered)
    return {
        "cooldown_window_bars": window_bars,
        "cooldown_removed_trades": len(rows) - trade_count,
        "trade_count_after_cooldown": trade_count,
        "trades_per_day_after_cooldown": trade_count / days if days else None,
        "net_after_cooldown": net,
        "profit_factor_after_cooldown": _profit_factor(filtered),
    }


def _audit_report(
    *,
    variant_id: str,
    run_id: str,
    record_view: str,
    report_path: Path,
    market_data: MarketData,
    cost_stress_per_trade: float,
    reference_capture: float | None,
) -> dict[str, Any]:
    days = _days_for_view(record_view)
    try:
        rows, report_summary = _trade_rows(report_path, market_data)
    except Exception as exc:  # pragma: no cover - parser evidence is still useful.
        return {
            "variant_id": variant_id,
            "run_id": run_id,
            "record_view": record_view,
            "split": "validation_is" if "validation" in record_view else "oos",
            "status": "parser_failed",
            "report_path": report_path.as_posix(),
            "error": str(exc),
        }
    trade_count = len(rows)
    winners = [row for row in rows if _float(row.get("net_profit")) > 0.0]
    losers = [row for row in rows if _float(row.get("net_profit")) < 0.0]
    capture_values = [
        _float(row.get("realized_over_mfe"))
        for row in winners
        if row.get("realized_over_mfe") is not None
    ]
    all_capture_values = [
        _float(row.get("realized_over_mfe"))
        for row in rows
        if row.get("realized_over_mfe") is not None
    ]
    mfe_capture_ratio = sum(capture_values) / len(capture_values) if capture_values else None
    mfe_capture_ratio_all = sum(all_capture_values) / len(all_capture_values) if all_capture_values else None
    winner_truncations = [
        row
        for row in winners
        if row.get("realized_over_mfe") is not None and _float(row.get("realized_over_mfe")) < 0.50
    ]
    loser_escapes = [
        row
        for row in losers
        if _float(row.get("mae")) > 0.0 and abs(_float(row.get("net_profit"))) / _float(row.get("mae")) <= 0.50
    ]
    same_3, _ = _same_direction_reentries(rows, 3)
    same_6, _ = _same_direction_reentries(rows, 6)
    same_12, _ = _same_direction_reentries(rows, 12)
    cooldown = _cooldown_metrics(rows, days=days, window_bars=12)
    net = sum(_float(row.get("net_profit")) for row in rows)
    expectancy = net / trade_count if trade_count else None
    cost_stressed_expectancy = None if expectancy is None else expectancy - cost_stress_per_trade
    materially_worse = False
    if reference_capture is not None and mfe_capture_ratio is not None and reference_capture > 0.0:
        materially_worse = mfe_capture_ratio < reference_capture * 0.85
    return {
        "variant_id": variant_id,
        "run_id": run_id,
        "record_view": record_view,
        "split": "validation_is" if "validation" in record_view else "oos",
        "status": "completed",
        "report_path": report_path.as_posix(),
        "trade_count": trade_count,
        "trades_per_day": trade_count / days if days else None,
        "net_profit": net,
        "profit_factor_recomputed": _profit_factor(rows),
        "expectancy": expectancy,
        "cost_stress_per_trade": cost_stress_per_trade,
        "cost_stressed_expectancy": cost_stressed_expectancy,
        "mfe_capture_ratio": mfe_capture_ratio,
        "mfe_capture_ratio_all_trades": mfe_capture_ratio_all,
        "reference_mfe_capture_ratio": reference_capture,
        "mfe_capture_delta_vs_d390h10": None if reference_capture is None or mfe_capture_ratio is None else mfe_capture_ratio - reference_capture,
        "mfe_capture_materially_worse_than_d390h10": materially_worse,
        "winner_count": len(winners),
        "winner_truncation_rate": len(winner_truncations) / len(winners) if winners else None,
        "loser_count": len(losers),
        "loser_escape_rate": len(loser_escapes) / len(losers) if losers else None,
        "same_direction_reentry_3_bars": same_3,
        "same_direction_reentry_6_bars": same_6,
        "same_direction_reentry_12_bars": same_12,
        "same_move_reentry_ratio": same_12 / trade_count if trade_count else None,
        "density_gain_survives_12bar_cooldown": (
            cooldown["trades_per_day_after_cooldown"] is not None
            and cooldown["trades_per_day_after_cooldown"] >= 5.0
        ),
        "mt5_average_position_holding_bars": report_summary.get("average_position_holding_bars"),
        **cooldown,
        "error": "",
    }


def _reference_capture_by_split(market_data: MarketData, cost_stress_per_trade: float) -> tuple[list[dict[str, Any]], dict[str, float]]:
    if not D390H10_SUMMARY_PATH.exists():
        return [], {}
    summary = _read_json(D390H10_SUMMARY_PATH)
    rows: list[dict[str, Any]] = []
    by_split: dict[str, float] = {}
    for view in ("mt5_routed_total_validation_is", "mt5_routed_total_oos"):
        report_path = _resolve(_metric(summary, view, "report_path"))
        if report_path is None or not _path_exists(report_path):
            continue
        row = _audit_report(
            variant_id="d390h10_reference",
            run_id=str(summary.get("run_id") or "run50D_d390h10_logreg_deep_v1"),
            record_view=view,
            report_path=report_path,
            market_data=market_data,
            cost_stress_per_trade=cost_stress_per_trade,
            reference_capture=None,
        )
        rows.append(row)
        if row.get("status") == "completed" and row.get("mfe_capture_ratio") is not None:
            by_split[str(row["split"])] = _float(row.get("mfe_capture_ratio"))
    return rows, by_split


def _audit_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    market_data: MarketData,
    cost_stress_per_trade: float,
    reference_capture: Mapping[str, float],
) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    for row in rows:
        summary_path = Path(str(row.get("summary_path") or "")) if row.get("summary_path") else None
        summary = _read_json(summary_path) if summary_path and summary_path.exists() else {}
        for view in ("mt5_routed_total_validation_is", "mt5_routed_total_oos"):
            report_path = _resolve(_metric(summary, view, "report_path"))
            if report_path is None or not _path_exists(report_path):
                audits.append(
                    {
                        "variant_id": row.get("variant_id", ""),
                        "run_id": row.get("run_id", ""),
                        "record_view": view,
                        "split": "validation_is" if "validation" in view else "oos",
                        "status": "missing_report",
                        "report_path": "" if report_path is None else report_path.as_posix(),
                        "error": "report_path_missing",
                    }
                )
                continue
            split = "validation_is" if "validation" in view else "oos"
            audits.append(
                _audit_report(
                    variant_id=str(row.get("variant_id") or ""),
                    run_id=str(row.get("run_id") or ""),
                    record_view=view,
                    report_path=report_path,
                    market_data=market_data,
                    cost_stress_per_trade=cost_stress_per_trade,
                    reference_capture=reference_capture.get(split),
                )
            )
    return audits


def _audit_lookup(audit_rows: Sequence[Mapping[str, Any]]) -> dict[tuple[str, str], Mapping[str, Any]]:
    return {
        (str(row.get("variant_id") or ""), str(row.get("record_view") or "")): row
        for row in audit_rows
    }


def _bool_text(value: Any) -> bool:
    return str(value).lower() in {"true", "1", "yes"}


def _base_pairs(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Mapping[str, Any]]]:
    pairs: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        base_id = str(row.get("base_id") or row.get("variant_id") or "")
        side = "enabled" if _bool_text(row.get("routed_fallback_enabled")) else "disabled"
        pairs.setdefault(base_id, {})[side] = row
    return pairs


def _tier_b_gate(row: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> tuple[bool, str]:
    tier_b_oos_net = _float(row.get("tier_b_oos_net_profit"))
    tier_b_oos_pf = _float(row.get("tier_b_oos_profit_factor"))
    if _bool_text(row.get("routed_fallback_enabled")):
        if tier_b_oos_net >= 0.0:
            return True, "Tier B fallback-only OOS non-negative"
        return False, "Tier B enabled but fallback-only OOS is negative"
    pairs = _base_pairs(rows)
    pair = pairs.get(str(row.get("base_id") or ""), {})
    enabled = pair.get("enabled")
    if enabled is None:
        return False, "Tier B disabled but no matched enabled comparison in this batch"
    disabled_total = _float(row.get("routed_validation_net_profit")) + _float(row.get("routed_oos_net_profit"))
    enabled_total = _float(enabled.get("routed_validation_net_profit")) + _float(enabled.get("routed_oos_net_profit"))
    disabled_pf_floor = min(_float(row.get("routed_validation_profit_factor")), _float(row.get("routed_oos_profit_factor")))
    enabled_pf_floor = min(_float(enabled.get("routed_validation_profit_factor")), _float(enabled.get("routed_oos_profit_factor")))
    tier_b_damaging = tier_b_oos_net < 0.0 or tier_b_oos_pf < 1.0
    enabled_not_enough = enabled_total <= disabled_total + 25.0 and enabled_pf_floor <= disabled_pf_floor + 0.02
    if tier_b_damaging and enabled_not_enough:
        return True, "Tier B disabled with matched A-only vs A+B evidence"
    return False, "Tier B disablement evidence incomplete or A+B still improves enough"


def _gate_checks(
    row: Mapping[str, Any],
    *,
    rows: Sequence[Mapping[str, Any]],
    audit_by_key: Mapping[tuple[str, str], Mapping[str, Any]],
) -> list[dict[str, Any]]:
    variant_id = str(row.get("variant_id") or "")
    val_audit = audit_by_key.get((variant_id, "mt5_routed_total_validation_is"), {})
    oos_audit = audit_by_key.get((variant_id, "mt5_routed_total_oos"), {})
    tier_b_ok, tier_b_reason = _tier_b_gate(row, rows)
    checks = [
        ("actual_mt5_completed", row.get("external_verification_status") == "completed", "actual MT5 summaries completed"),
        ("validation_density", _float(row.get("routed_validation_trades_per_day")) >= 5.0, "validation trades/day >= 5.0"),
        ("oos_density", _float(row.get("routed_oos_trades_per_day")) >= 5.0, "OOS trades/day >= 5.0"),
        ("validation_net_positive", _float(row.get("routed_validation_net_profit")) > 0.0, "validation net > 0"),
        ("oos_net_positive", _float(row.get("routed_oos_net_profit")) > 0.0, "OOS net > 0"),
        ("validation_pf", _float(row.get("routed_validation_profit_factor")) >= 1.10, "validation PF >= 1.10"),
        ("oos_pf", _float(row.get("routed_oos_profit_factor")) >= 1.10, "OOS PF >= 1.10"),
        ("cost_stressed_expectancy", _float(val_audit.get("cost_stressed_expectancy")) > 0.0 and _float(oos_audit.get("cost_stressed_expectancy")) > 0.0, "cost-stressed expectancy positive"),
        ("mfe_capture", not bool(val_audit.get("mfe_capture_materially_worse_than_d390h10")) and not bool(oos_audit.get("mfe_capture_materially_worse_than_d390h10")), "MFE capture not materially worse than d390h10"),
        ("same_move_density", bool(val_audit.get("density_gain_survives_12bar_cooldown")) and bool(oos_audit.get("density_gain_survives_12bar_cooldown")) and _float(val_audit.get("same_move_reentry_ratio"), 1.0) <= 0.35 and _float(oos_audit.get("same_move_reentry_ratio"), 1.0) <= 0.35, "density survives cooldown and is not mainly same-move re-entry"),
        ("tier_b_rule", tier_b_ok, tier_b_reason),
        ("actual_routed_path", row.get("routed_validation_aggregation") == "actual_routed_tester_run" and row.get("routed_oos_aggregation") == "actual_routed_tester_run", "actual routed reports are tester runs, not synthetic aggregation"),
        ("summary_csv_json", bool(row.get("summary_path")) and Path(str(row.get("summary_path"))).exists(), "summary.json exists; batch CSV is written separately"),
    ]
    return [
        {"check": name, "passed": bool(passed), "reason": reason}
        for name, passed, reason in checks
    ]


def _selected_read(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    audit_by_key = _audit_lookup(audit_rows)
    candidates: list[tuple[Mapping[str, Any], list[dict[str, Any]]]] = []
    checked: list[dict[str, Any]] = []
    for row in rows:
        checks = _gate_checks(row, rows=rows, audit_by_key=audit_by_key)
        passed = all(check["passed"] for check in checks)
        checked.append(
            {
                "variant_id": row.get("variant_id"),
                "passed": passed,
                "failed_checks": [check for check in checks if not check["passed"]],
            }
        )
        if passed:
            candidates.append((row, checks))
    if candidates:
        selected = max((candidate[0] for candidate in candidates), key=deep._candidate_score)
        return {
            "stage56_judgment": "selected_research_baseline",
            "selected_research_baseline": selected.get("variant_id"),
            "best_variant": dict(selected),
            "reason": "all Stage56 selected_research_baseline gates passed",
            "gate_checks": checked,
            "stage56_remains_open": False,
            "next_hypothesis_branch": "selected_research_baseline_evidence_packaging",
        }
    best = deep._best_row(rows)
    best_checks = next((entry for entry in checked if entry.get("variant_id") == (best or {}).get("variant_id")), None)
    return {
        "stage56_judgment": "in_progress_no_selected_research_baseline",
        "selected_research_baseline": None,
        "best_variant": None if best is None else dict(best),
        "reason": "no variant passed every selected_research_baseline gate",
        "best_variant_failed_checks": [] if best_checks is None else best_checks.get("failed_checks", []),
        "gate_checks": checked,
        "stage56_remains_open": True,
        "next_hypothesis_branch": "continue_density_repair_without_same_move_splitting_and_tier_b_damage_control",
    }


def _ledger_parent_row(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    best = final_read.get("best_variant")
    best_map = best if isinstance(best, Mapping) else {}
    completed_count = sum(1 for row in rows if row.get("external_verification_status") == "completed")
    status = "completed" if completed_count else "blocked"
    return {
        "ledger_row_id": f"{PARENT_RUN_ID}__parent_review",
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "subrun_id": "parent_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage56_reopen_optimization_parent_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage56_selected_research_baseline_search",
        "scoreboard_lane": "runtime_probe",
        "status": status,
        "judgment": str(final_read.get("stage56_judgment")),
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": ledger_pairs(
            (
                ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                ("best_variant", best_map.get("variant_id")),
                ("routed_validation_trades_per_day", best_map.get("routed_validation_trades_per_day")),
                ("routed_oos_trades_per_day", best_map.get("routed_oos_trades_per_day")),
                ("routed_validation_pf", best_map.get("routed_validation_profit_factor")),
                ("routed_oos_pf", best_map.get("routed_oos_profit_factor")),
                ("routed_validation_net", best_map.get("routed_validation_net_profit")),
                ("routed_oos_net", best_map.get("routed_oos_net_profit")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("completed_variants", completed_count),
                ("variant_count", len(rows)),
                ("terminal_condition", "selected_research_baseline_only"),
                ("stage56_remains_open", bool(final_read.get("stage56_remains_open"))),
                ("no_operating_claim", True),
            )
        ),
        "external_verification_status": "completed" if completed_count else "blocked",
        "notes": ledger_pairs((("reason", final_read.get("reason")), ("actual_routed_total_only", True))),
    }


def _write_parent_rows(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    parent_row = _ledger_parent_row(rows, final_read)
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage56_reopen_optimization_campaign",
                "status": "completed" if parent_row["status"] == "completed" else "blocked",
                "judgment": str(final_read.get("stage56_judgment")),
                "path": REPORT_PATH.as_posix(),
                "notes": ledger_pairs(
                    (
                        ("variant_count", len(rows)),
                        ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                        ("stage56_remains_open", bool(final_read.get("stage56_remains_open"))),
                        ("boundary", "research_baseline_selection_only_no_operating_claim"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    return {
        "stage_run_ledger": stage_payload,
        "project_alpha_run_ledger": project_payload,
        "run_registry": registry_payload,
    }


def _format(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def _write_report(
    rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    final_read: Mapping[str, Any],
    *,
    attempt_mt5: bool,
) -> None:
    best = final_read.get("best_variant")
    best_line = "`none`" if not isinstance(best, Mapping) else f"`{best.get('variant_id')}`"
    has_actual_mt5_evidence = any(
        row.get("external_verification_status") == "completed"
        or (row.get("routed_validation_report_path") and row.get("routed_oos_report_path"))
        for row in rows
    )
    lines = [
        f"# {PARENT_RUN_ID}(Stage56 재개 최적화 묶음)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`",
        f"- mt5_attempted(MT5 시도): `{bool(attempt_mt5 or has_actual_mt5_evidence)}`",
        f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
        f"- judgment(판정): `{final_read.get('stage56_judgment')}`",
        f"- best_variant(최선 변형): {best_line}",
        "- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`",
        "",
        "## Design(설계)",
        "",
        "Action(행동): threshold(임계값), hold(보유), Tier B fallback(대체) disablement(비활성화)을 실제 MT5 validation/OOS(검증/표본외)로 비교했다.",
        "Effect(효과): 거래 밀도 증가가 same-move split re-entry(동일 이동 분할 재진입)인지, Tier B(티어 B)가 실제 라우팅 전체를 돕는지 확인한다.",
        "",
        "## Variant Results(변형 결과)",
        "",
        "| variant(변형) | fallback(대체) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {fallback} | {vpd} | {opd} | {vpf} | {opf} | {vn} | {on} | `{judgment}` |".format(
                variant=row.get("variant_id", ""),
                fallback=row.get("routed_fallback_enabled", ""),
                vpd=row.get("routed_validation_trades_per_day", ""),
                opd=row.get("routed_oos_trades_per_day", ""),
                vpf=row.get("routed_validation_profit_factor", ""),
                opf=row.get("routed_oos_profit_factor", ""),
                vn=row.get("routed_validation_net_profit", ""),
                on=row.get("routed_oos_net_profit", ""),
                judgment=row.get("judgment", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Hold/Re-entry Audit(보유/재진입 감사)",
            "",
            "| variant(변형) | split(분할) | MFE capture(MFE 포착) | cost-stressed exp(비용 압박 기대값) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 후 일 거래) | density survives(밀도 생존) |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in audit_rows:
        if row.get("variant_id") == "d390h10_reference":
            continue
        lines.append(
            "| {variant} | {split} | {mfe} | {cse} | {same} | {cool} | {survives} |".format(
                variant=row.get("variant_id", ""),
                split=row.get("split", ""),
                mfe=_format(row.get("mfe_capture_ratio")),
                cse=_format(row.get("cost_stressed_expectancy")),
                same=_format(row.get("same_move_reentry_ratio")),
                cool=_format(row.get("trades_per_day_after_cooldown")),
                survives=row.get("density_gain_survives_12bar_cooldown", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Read(판독)",
            "",
            f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
            f"- stage56_remains_open(56단계 열림 유지): `{bool(final_read.get('stage56_remains_open'))}`",
            f"- reason(이유): {final_read.get('reason')}",
            f"- next_hypothesis_branch(다음 가설 가지): `{final_read.get('next_hypothesis_branch')}`",
        ]
    )
    if final_read.get("best_variant_failed_checks"):
        lines.append("")
        lines.append("## Best Variant Failed Checks(최선 변형 실패 조건)")
        lines.append("")
        for check in final_read.get("best_variant_failed_checks", []):
            lines.append(f"- `{check.get('check')}`: {check.get('reason')}")
    _write_bom_text(REPORT_PATH, lines)


def _write_progress_log(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant")
    best_map = best if isinstance(best, Mapping) else {}
    lines = [
        "# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)",
        "",
        "- packet_id(묶음 ID): `stage56_reopen_goal_v1`",
        "- stage_status(단계 상태): `active_in_progress(활성 진행 중)`",
        f"- latest_batch(최신 후보 묶음): `{PARENT_RUN_ID}`",
        f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
        "- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)",
        "- non_final_prior_packets(비최종 이전 묶음): `stage56_closeout_v1`, `stage56_reopened_closeout_v2`",
        "",
        "Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 open(열림) 상태다.",
        "Effect(효과): progress log(진행 기록)는 Stage56(56단계)을 닫지 않고 다음 hypothesis branch(가설 가지)를 정한다.",
        "",
        "## Current Bottleneck(현재 병목)",
        "",
        "- density(밀도): selected_research_baseline(선택 연구 기준선)은 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)를 요구한다.",
        "- Tier B OOS damage(Tier B 표본외 손상): Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 음수이면 disablement(비활성화) 근거가 필요하다.",
        "- hold compression audit(보유 압축 감사): density gain(밀도 증가)이 same-move split-trading(동일 이동 분할 거래)인지 확인해야 한다.",
        "",
        "## Prior Batch Summary(이전 묶음 요약)",
        "",
        "- run50B/run50C/run50D(실행50B/50C/50D)는 preserved intermediate evidence(보존 중간 근거)이며 final closeout(최종 종료)이 아니다.",
        "- d390h10(변형)는 stronger candidate(강한 후보)일 뿐 selected_research_baseline(선택 연구 기준선)이 아니다. 효과(effect, 효과): 품질 참조는 남기지만 Stage56(56단계)을 닫지 않는다.",
        "- d38h10(변형)는 prior candidate/reference(이전 후보/참조)일 뿐 selected_research_baseline(선택 연구 기준선)이 아니다.",
        "- d35h07(변형)는 density frontier(밀도 경계)였지만 quality(품질)가 실패해 selected_research_baseline(선택 연구 기준선)이 아니다.",
        "- run50E(실행50E)는 d340h06_ab_b040/d350h06_ab_b040(변형)이 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)에 도달했지만 PF(수익 팩터), cost-stressed expectancy(비용 압박 기대값), same-move audit(동일 이동 감사)가 실패했다.",
        "- run50F(실행50F)는 re-entry cooldown(재진입 쿨다운)과 stricter Tier B(더 엄격한 Tier B)를 시험했지만 OOS density(표본외 밀도), PF(수익 팩터), cost-stressed expectancy(비용 압박 기대값), Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 기준을 통과하지 못했다.",
        "- selected_research_baseline(선택 연구 기준선)은 계속 none(없음)이다. 효과(effect, 효과): 다음 hypothesis branch(가설 가지)를 이어가며 Stage56(56단계)을 open(열림)으로 유지한다.",
        "",
        "## Attempted Variants(시도 변형)",
        "",
        "| variant(변형) | hypothesis family(가설군) | fallback(대체) | report paths(보고서 경로) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | reason(이유) |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    failed_by_variant = {
        str(entry.get("variant_id")): entry.get("failed_checks", [])
        for entry in final_read.get("gate_checks", [])
    }
    for row in rows:
        failed = failed_by_variant.get(str(row.get("variant_id")), [])
        reason = "advanced" if not failed else "; ".join(str(item.get("check")) for item in failed[:4])
        paths = f"{row.get('routed_validation_report_path','')} ; {row.get('routed_oos_report_path','')}"
        lines.append(
            "| {variant} | {group} | {fallback} | {paths} | {vpd} | {opd} | {vpf} | {opf} | {vn} | {on} | {reason} |".format(
                variant=row.get("variant_id", ""),
                group=row.get("group", ""),
                fallback=row.get("routed_fallback_enabled", ""),
                paths=paths,
                vpd=row.get("routed_validation_trades_per_day", ""),
                opd=row.get("routed_oos_trades_per_day", ""),
                vpf=row.get("routed_validation_profit_factor", ""),
                opf=row.get("routed_oos_profit_factor", ""),
                vn=row.get("routed_validation_net_profit", ""),
                on=row.get("routed_oos_net_profit", ""),
                reason=reason,
            )
        )
    lines.extend(
        [
            "",
            "## Tier Views(티어 보기)",
            "",
            "| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |",
            "|---|---|---|---|---|",
        ]
    )
    for row in rows:
        tier_a = f"net {row.get('tier_a_validation_net_profit','')}/{row.get('tier_a_oos_net_profit','')}, PF {row.get('tier_a_validation_profit_factor','')}/{row.get('tier_a_oos_profit_factor','')}"
        tier_b = f"net {row.get('tier_b_validation_net_profit','')}/{row.get('tier_b_oos_net_profit','')}, PF {row.get('tier_b_validation_profit_factor','')}/{row.get('tier_b_oos_profit_factor','')}"
        routed = f"net {row.get('routed_validation_net_profit','')}/{row.get('routed_oos_net_profit','')}, PF {row.get('routed_validation_profit_factor','')}/{row.get('routed_oos_profit_factor','')}"
        contribution = f"fallback bars {row.get('routed_validation_b_fallback_bars','')}/{row.get('routed_oos_b_fallback_bars','')}"
        lines.append(f"| {row.get('variant_id','')} | {tier_a} | {tier_b} | {routed} | {contribution} |")
    lines.extend(
        [
            "",
            "## Hold/Re-entry Audit(보유/재진입 감사)",
            "",
            "| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |",
            "|---|---|---:|---:|---:|---|---:|---:|---:|",
        ]
    )
    for row in audit_rows:
        if row.get("variant_id") == "d390h10_reference":
            continue
        reentry = f"{row.get('same_direction_reentry_3_bars','')}/{row.get('same_direction_reentry_6_bars','')}/{row.get('same_direction_reentry_12_bars','')}"
        lines.append(
            "| {variant} | {split} | {mfe} | {win} | {loss} | {reentry} | {same} | {cse} | {survives} |".format(
                variant=row.get("variant_id", ""),
                split=row.get("split", ""),
                mfe=_format(row.get("mfe_capture_ratio")),
                win=_format(row.get("winner_truncation_rate")),
                loss=_format(row.get("loser_escape_rate")),
                reentry=reentry,
                same=_format(row.get("same_move_reentry_ratio")),
                cse=_format(row.get("cost_stressed_expectancy")),
                survives=row.get("density_gain_survives_12bar_cooldown", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Current Read(현재 판독)",
            "",
            f"- best_variant(최선 변형): `{best_map.get('variant_id') or 'none'}`",
            f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
            f"- stage56_remains_open(56단계 열림 유지): `{bool(final_read.get('stage56_remains_open'))}`",
            f"- next_hypothesis_branch(다음 가설 가지): `{final_read.get('next_hypothesis_branch')}`",
        ]
    )
    failed_attempt_path = Path("docs/agent_control/packets") / PACKET_ID / "failed_attempt_metaeditor_path.json"
    if _path_exists(failed_attempt_path):
        lines.extend(
            [
                "",
                "## Failed Attempt Records(실패 시도 기록)",
                "",
                f"- failed_attempt_record(실패 시도 기록): `{failed_attempt_path.as_posix()}`",
                "- repair_status(수정 상태): recorded before repaired rerun(수정 재실행 전 기록됨).",
                "- effect(효과): blocked tester attempt(차단된 테스터 시도)를 숨기지 않고, repaired actual MT5 rerun(수정된 실제 MT5 재실행)과 분리한다.",
            ]
        )
    _write_bom_text(PROGRESS_LOG_PATH, lines)


def _write_aggregate_summary(
    results: Sequence[Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    final_read: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    artifacts = {
        "report_path": REPORT_PATH.as_posix(),
        "results_csv_path": RESULTS_CSV_PATH.as_posix(),
        "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
        "progress_log_path": PROGRESS_LOG_PATH.as_posix(),
        "ledger_payload": dict(ledger_payload),
    }
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "completed" if any(row.get("external_verification_status") == "completed" for row in rows) else "blocked",
        "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
        "final_read": final_read,
        "variant_rows": [dict(row) for row in rows],
        "audit_rows": [dict(row) for row in audit_rows],
        "variant_payloads": [dict(result) for result in results],
        "artifacts": artifacts,
        "artifact_hashes": {
            "report_sha256": sha256_file_lf_normalized(REPORT_PATH) if REPORT_PATH.exists() else None,
            "results_csv_sha256": sha256_file_lf_normalized(RESULTS_CSV_PATH) if RESULTS_CSV_PATH.exists() else None,
            "audit_csv_sha256": sha256_file_lf_normalized(AUDIT_CSV_PATH) if AUDIT_CSV_PATH.exists() else None,
            "progress_log_sha256": sha256_file_lf_normalized(PROGRESS_LOG_PATH) if PROGRESS_LOG_PATH.exists() else None,
        },
        "boundary": "research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference",
    }
    _write_json(AGGREGATE_SUMMARY_PATH, payload)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 reopened optimization MT5 batch.")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true", default=True)
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--groups", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(deep.logreg_scout.DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(deep.logreg_scout.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(deep.logreg_scout.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _configure_deep_globals()
    args = parse_args(argv)
    variants = _select_variants(
        selected_ids=_split_values(args.variant_id),
        selected_groups=_split_values(args.groups),
        max_variants=args.max_variants,
    )
    deep_variants = tuple(variant.to_deep_variant() for variant in variants)
    results: list[dict[str, Any]] = []
    for variant in variants:
        try:
            result = _run_variant(
                variant,
                attempt_mt5=bool(args.attempt_mt5),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
                force=bool(args.force),
            )
        except Exception as exc:  # pragma: no cover - long MT5 batches must keep evidence.
            error_path = RUN_ROOT / variant.variant_id / "error.json"
            error_payload = {
                "variant_id": variant.variant_id,
                "run_id": variant.to_deep_variant().run_id,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            }
            _write_json(error_path, error_payload)
            result = {
                "status": "error",
                "variant_id": variant.variant_id,
                "run_id": variant.to_deep_variant().run_id,
                "external_verification_status": "blocked",
                "error": str(exc),
                "error_path": error_path.as_posix(),
            }
            if not args.continue_on_error:
                results.append(result)
                break
        results.append(dict(result))

    rows = deep._summary_rows(results, deep_variants)
    _augment_rows(rows, variants)

    market_data = MarketData.load(REPO_ROOT)
    reference_audits, reference_capture = _reference_capture_by_split(market_data, float(args.cost_stress_per_trade))
    audit_rows = reference_audits + _audit_rows(
        rows,
        market_data=market_data,
        cost_stress_per_trade=float(args.cost_stress_per_trade),
        reference_capture=reference_capture,
    )
    final_read = _selected_read(rows, audit_rows)

    _write_csv(RESULTS_CSV_PATH, rows, SUMMARY_COLUMNS)
    _write_csv(AUDIT_CSV_PATH, audit_rows, AUDIT_COLUMNS)
    _write_report(rows, audit_rows, final_read, attempt_mt5=bool(args.attempt_mt5))
    _write_progress_log(rows, audit_rows, final_read)
    ledger_payload = _write_parent_rows(rows, final_read)
    _write_aggregate_summary(results, rows, audit_rows, final_read, ledger_payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": PARENT_RUN_ID,
                "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
                "final_read": final_read.get("stage56_judgment"),
                "stage56_remains_open": bool(final_read.get("stage56_remains_open")),
                "results_csv_path": RESULTS_CSV_PATH.as_posix(),
                "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
                "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


SUMMARY_COLUMNS = tuple(
    list(deep.SUMMARY_COLUMNS[:-4])
    + [
        "base_id",
        "routed_fallback_enabled",
        "routed_validation_report_path",
        "routed_validation_aggregation",
        "routed_oos_report_path",
        "routed_oos_aggregation",
    ]
    + list(deep.SUMMARY_COLUMNS[-4:])
)

AUDIT_COLUMNS = (
    "variant_id",
    "run_id",
    "record_view",
    "split",
    "status",
    "report_path",
    "trade_count",
    "trades_per_day",
    "net_profit",
    "profit_factor_recomputed",
    "expectancy",
    "cost_stress_per_trade",
    "cost_stressed_expectancy",
    "mfe_capture_ratio",
    "mfe_capture_ratio_all_trades",
    "reference_mfe_capture_ratio",
    "mfe_capture_delta_vs_d390h10",
    "mfe_capture_materially_worse_than_d390h10",
    "winner_count",
    "winner_truncation_rate",
    "loser_count",
    "loser_escape_rate",
    "same_direction_reentry_3_bars",
    "same_direction_reentry_6_bars",
    "same_direction_reentry_12_bars",
    "same_move_reentry_ratio",
    "cooldown_window_bars",
    "cooldown_removed_trades",
    "trade_count_after_cooldown",
    "trades_per_day_after_cooldown",
    "net_after_cooldown",
    "profit_factor_after_cooldown",
    "density_gain_survives_12bar_cooldown",
    "mt5_average_position_holding_bars",
    "error",
)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
