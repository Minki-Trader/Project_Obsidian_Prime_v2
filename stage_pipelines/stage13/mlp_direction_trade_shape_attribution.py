from __future__ import annotations

import argparse
import csv
import json
import math
import random
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.alpha_run_ledgers import materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
STAGE_NUMBER = 13
RUN_ID = "run04G_mlp_direction_trade_shape_attribution_v1"
PACKET_ID = "stage13_run04G_mlp_direction_trade_shape_attribution_packet_v1"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
EXPLORATION_LABEL = "stage13_MLPDirection__TradeShapeAttribution"
BOUNDARY = "trade_shape_attribution_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
REPORT_PATH = STAGE_ROOT / "03_reviews/run04G_mlp_direction_trade_shape_attribution_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_direction_trade_shape_attribution.md"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"


SUMMARY_COLUMNS = (
    "record_view",
    "split",
    "trade_count",
    "net_profit",
    "report_net_profit",
    "net_diff",
    "profit_factor",
    "max_drawdown",
    "win_rate",
    "avg_win",
    "avg_loss",
    "payoff_ratio",
    "largest_loss",
    "avg_hold_bars",
    "median_hold_bars",
    "max_hold_bars",
    "report_avg_hold_bars",
    "consecutive_losses",
    "long_trade_count",
    "short_trade_count",
    "long_net_profit",
    "short_net_profit",
    "report_path",
    "report_sha256",
)

TRADE_COLUMNS = (
    "record_view",
    "split",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "volume",
    "open_price",
    "close_price",
    "gross_profit",
    "net_profit",
    "swap",
    "commission",
)

DAMAGE_COLUMNS = (
    "split",
    "separate_sum_net",
    "both_net",
    "net_damage",
    "separate_sum_trades",
    "both_trades",
    "trade_count_delta",
    "both_max_drawdown",
    "max_component_drawdown",
    "drawdown_delta_vs_max_component",
    "long_side_delta",
    "short_side_delta",
    "driver",
)

SIDE_IDENTITY_COLUMNS = (
    "split",
    "side",
    "separate_count",
    "both_side_count",
    "same_exact_trades",
    "same_open_trades",
    "separate_net",
    "both_side_net",
    "net_delta",
    "common_exact_net",
    "separate_only_net",
    "both_only_net",
)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: _csv_value(row.get(column)) for column in columns})


def _csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.6g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_source_records() -> list[dict[str, Any]]:
    source = read_json(SOURCE_ROOT / "kpi_record.json")
    records = source["mt5"]["kpi_records"]
    if len(records) != 6:
        raise RuntimeError(f"expected 6 RUN04F MT5 KPI records, found {len(records)}")
    return [dict(record) for record in records]


def analyze_record(record: Mapping[str, Any]) -> dict[str, Any]:
    metrics = dict(record["metrics"])
    report_path = Path(str(metrics["report_path"]))
    report = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(report["deals"])
    payloads = [_trade_payload(record["record_view"], record["split"], trade) for trade in trades]
    summary = _trade_summary(record, payloads, report["summary"], report_path)
    return {"record": dict(record), "summary": summary, "trades": payloads, "report_summary": report["summary"]}


def _trade_payload(record_view: str, split: str, trade: Any) -> dict[str, Any]:
    hold_bars = (trade.close_time - trade.open_time).total_seconds() / 60.0 / 5.0
    return {
        "record_view": record_view,
        "split": split,
        "trade_index": trade.index,
        "direction": trade.direction,
        "open_time": trade.open_time.isoformat(),
        "close_time": trade.close_time.isoformat(),
        "hold_bars": hold_bars,
        "volume": trade.volume,
        "open_price": trade.open_price,
        "close_price": trade.close_price,
        "gross_profit": trade.gross_profit,
        "net_profit": trade.net_profit,
        "swap": trade.swap,
        "commission": trade.commission,
    }


def _trade_summary(
    record: Mapping[str, Any],
    trades: Sequence[Mapping[str, Any]],
    report_summary: Mapping[str, Any],
    report_path: Path,
) -> dict[str, Any]:
    metrics = dict(record["metrics"])
    pnl = [float(row["net_profit"]) for row in trades]
    wins = [value for value in pnl if value > 0.0]
    losses = [value for value in pnl if value < 0.0]
    hold = [float(row["hold_bars"]) for row in trades]
    long_rows = [row for row in trades if row["direction"] == "buy"]
    short_rows = [row for row in trades if row["direction"] == "sell"]
    net = sum(pnl)
    report_net = float(metrics.get("net_profit") or 0.0)
    avg_win = _mean(wins)
    avg_loss = _mean(losses)
    return {
        "record_view": record["record_view"],
        "split": record["split"],
        "trade_count": len(trades),
        "net_profit": round(net, 6),
        "report_net_profit": report_net,
        "net_diff": round(net - report_net, 6),
        "profit_factor": metrics.get("profit_factor"),
        "max_drawdown": metrics.get("max_drawdown_amount"),
        "win_rate": _ratio(len(wins), len(trades)),
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": avg_win / abs(avg_loss) if avg_win is not None and avg_loss else None,
        "largest_loss": min(pnl) if pnl else None,
        "avg_hold_bars": _mean(hold),
        "median_hold_bars": _median(hold),
        "max_hold_bars": max(hold) if hold else None,
        "report_avg_hold_bars": report_summary.get("average_position_holding_bars"),
        "consecutive_losses": _max_consecutive_losses(pnl),
        "long_trade_count": len(long_rows),
        "short_trade_count": len(short_rows),
        "long_net_profit": round(_sum(long_rows, "net_profit"), 6),
        "short_net_profit": round(_sum(short_rows, "net_profit"), 6),
        "report_path": report_path.as_posix(),
        "report_sha256": sha256_file_lf_normalized(report_path),
    }


def build_damage_rows(by_view: Mapping[str, Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    damage_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        long_view = f"mt5_tier_a_long_only_{split}"
        short_view = f"mt5_tier_a_short_only_{split}"
        both_view = f"mt5_tier_a_both_no_fallback_{split}"
        long_summary = by_view[long_view]["summary"]
        short_summary = by_view[short_view]["summary"]
        both_summary = by_view[both_view]["summary"]
        long_identity = side_identity(split, "long", by_view[long_view]["trades"], by_view[both_view]["trades"])
        short_identity = side_identity(split, "short", by_view[short_view]["trades"], by_view[both_view]["trades"])
        identity_rows.extend([long_identity, short_identity])
        separate_sum_net = float(long_summary["net_profit"]) + float(short_summary["net_profit"])
        separate_sum_trades = int(long_summary["trade_count"]) + int(short_summary["trade_count"])
        both_net = float(both_summary["net_profit"])
        trade_delta = int(both_summary["trade_count"]) - separate_sum_trades
        max_component_dd = max(float(long_summary["max_drawdown"]), float(short_summary["max_drawdown"]))
        driver = _damage_driver(split, trade_delta, both_net - separate_sum_net, long_identity, short_identity, both_summary, max_component_dd)
        damage_rows.append(
            {
                "split": split,
                "separate_sum_net": round(separate_sum_net, 6),
                "both_net": round(both_net, 6),
                "net_damage": round(both_net - separate_sum_net, 6),
                "separate_sum_trades": separate_sum_trades,
                "both_trades": both_summary["trade_count"],
                "trade_count_delta": trade_delta,
                "both_max_drawdown": both_summary["max_drawdown"],
                "max_component_drawdown": max_component_dd,
                "drawdown_delta_vs_max_component": round(float(both_summary["max_drawdown"]) - max_component_dd, 6),
                "long_side_delta": long_identity["net_delta"],
                "short_side_delta": short_identity["net_delta"],
                "driver": driver,
            }
        )
    return damage_rows, identity_rows


def side_identity(
    split: str,
    side: str,
    separate_trades: Sequence[Mapping[str, Any]],
    both_trades: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    direction = "buy" if side == "long" else "sell"
    separate = [row for row in separate_trades if row["direction"] == direction]
    both = [row for row in both_trades if row["direction"] == direction]
    sep_key = {_trade_key(row): float(row["net_profit"]) for row in separate}
    both_key = {_trade_key(row): float(row["net_profit"]) for row in both}
    common = set(sep_key) & set(both_key)
    sep_open = {row["open_time"] for row in separate}
    both_open = {row["open_time"] for row in both}
    separate_net = sum(sep_key.values())
    both_net = sum(both_key.values())
    return {
        "split": split,
        "side": side,
        "separate_count": len(separate),
        "both_side_count": len(both),
        "same_exact_trades": len(common),
        "same_open_trades": len(sep_open & both_open),
        "separate_net": round(separate_net, 6),
        "both_side_net": round(both_net, 6),
        "net_delta": round(both_net - separate_net, 6),
        "common_exact_net": round(sum(sep_key[key] for key in common), 6),
        "separate_only_net": round(sum(sep_key[key] for key in set(sep_key) - common), 6),
        "both_only_net": round(sum(both_key[key] for key in set(both_key) - common), 6),
    }


def _trade_key(row: Mapping[str, Any]) -> tuple[str, str, str]:
    return (str(row["open_time"]), str(row["close_time"]), str(row["direction"]))


def _damage_driver(
    split: str,
    trade_delta: int,
    net_damage: float,
    long_identity: Mapping[str, Any],
    short_identity: Mapping[str, Any],
    both_summary: Mapping[str, Any],
    max_component_dd: float,
) -> str:
    dd_delta = float(both_summary["max_drawdown"]) - max_component_dd
    if split == "oos" and trade_delta == 0 and net_damage < 0.0:
        return "not_trade_count; short_side_flipped_under_both; drawdown_expanded_vs_components"
    if split == "validation_is" and net_damage < 0.0:
        return "small_trade_count_increase; long_side_deteriorated; drawdown_not_worse_than_long_only" if dd_delta <= 0 else "trade_count_and_drawdown_mixed"
    return "no_clear_damage"


def short_oos_fragility(short_oos: Mapping[str, Any]) -> dict[str, Any]:
    trades = short_oos["trades"]
    pnl = [float(row["net_profit"]) for row in trades]
    totals, means = _bootstrap_profit(pnl, iterations=20000, seed=1517)
    month_pnl: dict[str, float] = {}
    for row in trades:
        month = str(row["close_time"])[:7]
        month_pnl[month] = month_pnl.get(month, 0.0) + float(row["net_profit"])
    total = sum(pnl)
    leave_one_month = {month: round(total - value, 6) for month, value in sorted(month_pnl.items())}
    return {
        "record_view": short_oos["summary"]["record_view"],
        "trade_count": len(pnl),
        "net_profit": round(total, 6),
        "mean_trade_profit": _mean(pnl),
        "win_rate": _ratio(sum(1 for value in pnl if value > 0.0), len(pnl)),
        "bootstrap_total_profit_ci_95": [_percentile(totals, 2.5), _percentile(totals, 50.0), _percentile(totals, 97.5)],
        "bootstrap_mean_profit_ci_95": [_percentile(means, 2.5), _percentile(means, 50.0), _percentile(means, 97.5)],
        "bootstrap_positive_total_probability": _ratio(sum(1 for value in totals if value > 0.0), len(totals)),
        "months": len(month_pnl),
        "positive_months": sum(1 for value in month_pnl.values() if value > 0.0),
        "positive_month_ratio": _ratio(sum(1 for value in month_pnl.values() if value > 0.0), len(month_pnl)),
        "month_pnl": {month: round(value, 6) for month, value in sorted(month_pnl.items())},
        "leave_one_month_out_net_profit": leave_one_month,
        "largest_win": max(pnl) if pnl else None,
        "largest_loss": min(pnl) if pnl else None,
        "judgment": "thin_sample_positive_clue_but_confidence_interval_crosses_zero",
    }


def _bootstrap_profit(values: Sequence[float], *, iterations: int, seed: int) -> tuple[list[float], list[float]]:
    if not values:
        return [], []
    rng = random.Random(seed)
    totals: list[float] = []
    means: list[float] = []
    count = len(values)
    for _ in range(iterations):
        total = sum(values[rng.randrange(count)] for _ in range(count))
        totals.append(total)
        means.append(total / count)
    return totals, means


def build_ledgers(summary_rows: Sequence[Mapping[str, Any]], damage_rows: Sequence[Mapping[str, Any]], fragility: Mapping[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = [
        _scope_row("Tier B", "tier_b_out_of_scope"),
        _scope_row("Tier A+B", "tier_abb_out_of_scope"),
    ]
    for row in summary_rows:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{row['record_view']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": row["record_view"],
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": row["record_view"],
                "tier_scope": "Tier A",
                "kpi_scope": "trade_shape_attribution",
                "scoreboard_lane": "runtime_probe_attribution",
                "status": "completed",
                "judgment": "inconclusive_trade_shape_attribution_completed",
                "path": row["report_path"],
                "primary_kpi": ledger_pairs((("trades", row["trade_count"]), ("avg_win", row["avg_win"]), ("avg_loss", row["avg_loss"]), ("largest_loss", row["largest_loss"]))),
                "guardrail_kpi": ledger_pairs((("avg_hold", row["avg_hold_bars"]), ("max_hold", row["max_hold_bars"]), ("consec_loss", row["consecutive_losses"]), ("source_run", SOURCE_RUN_ID))),
                "external_verification_status": "completed_from_existing_mt5_reports",
                "notes": "Trade-shape attribution from RUN04F MT5 Strategy Tester deal list.",
            }
        )
    for row in damage_rows:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__damage_{row['split']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"damage_{row['split']}",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": f"damage_{row['split']}",
                "tier_scope": "Tier A",
                "kpi_scope": "direction_damage_attribution",
                "scoreboard_lane": "runtime_probe_attribution",
                "status": "completed",
                "judgment": "inconclusive_direction_damage_attribution_completed",
                "path": rel(RUN_ROOT / "damage_attribution.csv"),
                "primary_kpi": ledger_pairs((("net_damage", row["net_damage"]), ("trade_delta", row["trade_count_delta"]), ("dd_delta", row["drawdown_delta_vs_max_component"]))),
                "guardrail_kpi": ledger_pairs((("long_delta", row["long_side_delta"]), ("short_delta", row["short_side_delta"]), ("driver", row["driver"]))),
                "external_verification_status": "completed_from_existing_mt5_reports",
                "notes": "Compares both-direction tester path against separate long-only plus short-only tester paths; not synthetic promotion evidence.",
            }
        )
    rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__short_oos_sample_fragility",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "short_oos_sample_fragility",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "short_oos_sample_fragility",
            "tier_scope": "Tier A",
            "kpi_scope": "sample_fragility",
            "scoreboard_lane": "runtime_probe_attribution",
            "status": "completed",
            "judgment": "inconclusive_thin_sample_positive_clue",
            "path": rel(RUN_ROOT / "sample_fragility.json"),
            "primary_kpi": ledger_pairs((("trades", fragility["trade_count"]), ("net", fragility["net_profit"]), ("positive_bootstrap", fragility["bootstrap_positive_total_probability"]))),
            "guardrail_kpi": ledger_pairs((("ci95", fragility["bootstrap_total_profit_ci_95"]), ("positive_month_ratio", fragility["positive_month_ratio"]), ("boundary", "sample_too_small_for_alpha_quality"))),
            "external_verification_status": "completed_from_existing_mt5_reports",
            "notes": "Bootstrap check uses RUN04F short-only OOS trade profit list and does not validate alpha quality.",
        }
    )
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "direction_trade_shape_attribution",
        "status": "reviewed",
        "judgment": "inconclusive_trade_shape_attribution_completed",
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs((("source_run", SOURCE_RUN_ID), ("views", "long_only;short_only;both_no_fallback"), ("short_oos_trades", fragility["trade_count"]), ("boundary", "trade_shape_attribution_only"))),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def _scope_row(tier_scope: str, suffix: str) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__{suffix}",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": suffix,
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": suffix,
        "tier_scope": tier_scope,
        "kpi_scope": "claim_scope_boundary",
        "scoreboard_lane": "runtime_probe_attribution",
        "status": "completed",
        "judgment": "out_of_scope_by_claim_trade_shape_attribution",
        "path": rel(RUN_ROOT / "summary.json"),
        "primary_kpi": ledger_pairs((("source_run", SOURCE_RUN_ID),)),
        "guardrail_kpi": ledger_pairs((("boundary", "tier_a_direction_trade_shape_only"),)),
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "RUN04G analyzes RUN04F Tier A direction trade shape only.",
    }


def skill_receipts(fragility: Mapping[str, Any]) -> list[dict[str, Any]]:
    status = "completed"
    return [
        {"packet_id": PACKET_ID, "skill": "obsidian-performance-attribution", "status": status, "attribution_layers_checked": ["trade_shape", "direction", "drawdown", "sample_fragility"], "missing_layers": ["regime_context", "WFO"], "allowed_claims": ["trade_shape_attribution_completed"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-backtest-forensics", "status": status, "tester_report": rel(SOURCE_ROOT / "mt5/reports"), "tester_settings": "RUN04F MT5 Strategy Tester reports, US100 M5, deposit 500, leverage 1:100, model every tick based on real ticks equivalent profile value 4", "spread_commission_slippage": "same RUN04F Strategy Tester reports; no new cost model introduced", "trade_list_identity": "six RUN04F HTML deal lists parsed with foundation.mt5.trade_report", "forensic_gaps": ["no new MT5 execution", "trade-list bootstrap is exploratory"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": status, "source_inputs": [rel(SOURCE_ROOT / "kpi_record.json"), rel(SOURCE_ROOT / "mt5/reports")], "produced_artifacts": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "trade_shape_summary.csv"), rel(RUN_ROOT / "damage_attribution.csv"), rel(REPORT_PATH)], "raw_evidence": [rel(SOURCE_ROOT / "mt5/reports")], "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "sample_fragility.json")], "human_readable": [rel(REPORT_PATH), rel(DECISION_PATH)], "hashes_or_missing_reasons": "report sha256 recorded per row; no model hash copied because no new model was produced", "lineage_boundary": "connected_with_boundary_from_RUN04F_existing_MT5_reports"},
        {"packet_id": PACKET_ID, "skill": "obsidian-result-judgment", "status": status, "judgment_boundary": "inconclusive_trade_shape_attribution_completed; short-only OOS positive clue remains thin sample", "allowed_claims": ["direction_trade_shape_read"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"], "evidence_used": [rel(RUN_ROOT / "trade_shape_summary.csv"), rel(RUN_ROOT / "sample_fragility.json")]},
        {"packet_id": PACKET_ID, "skill": "obsidian-experiment-design", "status": status, "hypothesis": "RUN04F both-direction damage is driven by trade-shape interaction rather than simple trade-count increase.", "baseline": "RUN04F long-only and short-only separate MT5 reports", "changed_variables": ["analysis only; no threshold or model change"], "invalid_conditions": ["missing deal list", "report net and paired-trade net mismatch"], "evidence_plan": ["trade_shape_summary", "damage_attribution", "short_oos_bootstrap"]},
    ]


def report_markdown(summary: Mapping[str, Any]) -> str:
    rows = summary["trade_shape_summary"]
    damage = summary["damage_attribution"]
    fragility = summary["short_oos_fragility"]
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        "- status(상태): `completed`",
        "- judgment(판정): `inconclusive_trade_shape_attribution_completed`",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Trade Shape(거래 형태)",
        "",
        "| view(보기) | split(분할) | trades(거래) | net(순수익) | avg win(평균 승) | avg loss(평균 패) | largest loss(최대 단일 손실) | avg hold bars(평균 보유 봉) | consec losses(연속 손실) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {record_view} | {split} | {trade_count} | {net_profit:.2f} | {avg_win:.2f} | {avg_loss:.2f} | {largest_loss:.2f} | {avg_hold_bars:.2f} | {consecutive_losses} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Damage Attribution(손상 기여도)",
            "",
            "| split(분할) | separate net(분리 합산 순수익) | both net(양방향 순수익) | damage(손상) | trade delta(거래 수 차이) | DD delta(손실 차이) | driver(주된 원인) |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in damage:
        lines.append(
            f"| {row['split']} | {row['separate_sum_net']:.2f} | {row['both_net']:.2f} | {row['net_damage']:.2f} | {row['trade_count_delta']} | {row['drawdown_delta_vs_max_component']:.2f} | {row['driver']} |"
        )
    lines.extend(
        [
            "",
            "## Short OOS Fragility(숏 표본외 취약성)",
            "",
            f"- short-only OOS trades(숏 전용 표본외 거래): `{fragility['trade_count']}`",
            f"- net(순수익): `{fragility['net_profit']:.2f}`",
            f"- bootstrap total CI95(부트스트랩 총수익 95% 구간): `{_fmt_ci(fragility['bootstrap_total_profit_ci_95'])}`",
            f"- positive bootstrap probability(부트스트랩 양수 확률): `{fragility['bootstrap_positive_total_probability']:.3f}`",
            f"- positive months(양수 월): `{fragility['positive_months']}/{fragility['months']}`",
            "",
            "효과(effect, 효과): short-only OOS(숏 전용 표본외)는 좋은 단서지만, 49 trades(49개 거래)와 CI95(95% 구간) 하단 음수 때문에 alpha quality(알파 품질)로 올릴 수 없다.",
        ]
    )
    return "\n".join(lines)


def decision_markdown(summary: Mapping[str, Any]) -> str:
    fragility = summary["short_oos_fragility"]
    oos_damage = next(row for row in summary["damage_attribution"] if row["split"] == "oos")
    return "\n".join(
        [
            "# 2026-05-02 Stage 13 MLP Direction Trade Shape Attribution",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- source(원천): `{SOURCE_RUN_ID}`",
            "- decision(결정): 방향별 거래 형태 기여도만 기록한다.",
            f"- OOS both damage(표본외 양방향 손상): `{oos_damage['net_damage']:.2f}`",
            f"- OOS trade count delta(표본외 거래 수 차이): `{oos_damage['trade_count_delta']}`",
            f"- short-only OOS bootstrap CI95(숏 전용 표본외 부트스트랩 95% 구간): `{_fmt_ci(fragility['bootstrap_total_profit_ci_95'])}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): 다음 탐색에서 short-only(숏 전용)를 기준선처럼 쓰지 않고, 작은 표본의 생존 단서로만 보존한다.",
        ]
    )


def update_state_docs(summary: Mapping[str, Any]) -> None:
    section = (
        "stage13_mlp_direction_trade_shape_attribution:\n"
        f"  run_id: {RUN_ID}\n"
        "  status: completed\n"
        "  judgment: inconclusive_trade_shape_attribution_completed\n"
        f"  boundary: {BOUNDARY}\n"
        f"  source_run_id: {SOURCE_RUN_ID}\n"
        f"  report_path: {rel(REPORT_PATH)}\n"
    )
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state_text = state_text.replace("active_run04F_mlp_direction_asymmetry_runtime_probe", "active_run04G_mlp_direction_trade_shape_attribution")
    if "stage13_mlp_direction_trade_shape_attribution:" not in state_text:
        state_text = state_text.replace("stage01_raw_m5_inventory:\n", section + "stage01_raw_m5_inventory:\n")
    io_path(WORKSPACE_STATE_PATH).write_text(state_text, encoding="utf-8")

    current_text = io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = current_text.replace(f"current run(현재 실행): `{SOURCE_RUN_ID}`", f"current run(현재 실행): `{RUN_ID}`")
    latest = (
        "Stage13(13단계)의 현재 실행(current run, 현재 실행)은 "
        f"`{RUN_ID}`이고, RUN04F(실행 04F)의 MT5(메타트레이더5) 거래 목록을 trade shape attribution(거래 형태 기여도 분해)로 재분석했다.\n\n"
        "효과(effect, 효과): 방향별 평균 승/패, 최대 단일 손실, 보유 시간, 연속 손실, 양방향 손상 원인, short-only OOS(숏 전용 표본외) 표본 취약성을 확인했다."
    )
    marker = "## 쉬운 설명(Plain Read, 쉬운 설명)"
    if marker in current_text:
        before, after = current_text.split(marker, 1)
        head = before.split("## Latest Stage 13 Update(최신 Stage 13 업데이트)", 1)[0]
        current_text = head + "## Latest Stage 13 Update(최신 Stage 13 업데이트)\n\n" + latest + "\n## 쉬운 설명(Plain Read, 쉬운 설명)" + after
    io_path(CURRENT_STATE_PATH).write_text(current_text, encoding="utf-8-sig")

    selection = "\n".join(
        [
            "# Stage 13 Selection Status",
            "",
            "## Current Read(현재 판독)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            "- status(상태): `reviewed_trade_shape_attribution_completed`",
            "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
            "- exploration depth(탐색 깊이): `trade_shape_attribution_only(거래 형태 기여도만)`",
            "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
            f"- current run(현재 실행): `{RUN_ID}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            "- external verification status(외부 검증 상태): `completed_from_existing_mt5_reports(기존 MT5 보고서에서 완료)`",
            "- judgment(판정): `inconclusive_trade_shape_attribution_completed`",
            "",
            "효과(effect, 효과): short-only OOS(숏 전용 표본외)를 단서로 보존하되 alpha quality(알파 품질)나 운영 의미는 만들지 않는다.",
        ]
    )
    write_md(SELECTION_STATUS_PATH, selection)
    review_index = "\n".join(
        [
            "# Stage 13 Review Index",
            "",
            "- `run04A_mlp_characteristic_runtime_probe_v1`: `inconclusive_mlp_characteristic_runtime_probe_completed`",
            "- `run04B_mlp_input_geometry_runtime_handoff_probe_v1`: `inconclusive_input_geometry_runtime_handoff_probe_completed`",
            "- `run04C_mlp_activation_runtime_probe_v1`: `inconclusive_activation_runtime_probe_completed`",
            "- `run04D_mlp_convergence_threshold_feasibility_probe_v1`: `inconclusive_convergence_threshold_feasibility_probe_completed`",
            "- `run04E_mlp_q90_threshold_trading_runtime_probe_v1`: `inconclusive_q90_threshold_trading_runtime_probe_completed`",
            "- `run04F_mlp_direction_asymmetry_runtime_probe_v1`: `inconclusive_direction_asymmetry_runtime_probe_completed`",
            f"- `{RUN_ID}`: `inconclusive_trade_shape_attribution_completed`, report(보고서) `{rel(REPORT_PATH)}`",
            "",
            "효과(effect, 효과): Stage13(13단계)의 실행 근거 위치를 한 곳에서 찾게 한다.",
        ]
    )
    write_md(REVIEW_INDEX_PATH, review_index)
    changelog_line = f"\n- 2026-05-02: Added `{RUN_ID}` trade-shape attribution(거래 형태 기여도 분해) from RUN04F MT5 reports; no alpha quality(알파 품질) or promotion(승격) claim.\n"
    io_path(CHANGELOG_PATH).write_text(io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") + changelog_line, encoding="utf-8-sig")


def build_summary(created_at: str) -> dict[str, Any]:
    records = load_source_records()
    analyses = [analyze_record(record) for record in records]
    by_view = {item["summary"]["record_view"]: item for item in analyses}
    summary_rows = [item["summary"] for item in analyses]
    trade_rows = [trade for item in analyses for trade in item["trades"]]
    damage_rows, side_identity_rows = build_damage_rows(by_view)
    fragility = short_oos_fragility(by_view["mt5_tier_a_short_only_oos"])
    summary = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "exploration_label": EXPLORATION_LABEL,
        "status": "completed",
        "judgment": "inconclusive_trade_shape_attribution_completed",
        "boundary": BOUNDARY,
        "trade_shape_summary": summary_rows,
        "damage_attribution": damage_rows,
        "side_identity": side_identity_rows,
        "short_oos_fragility": fragility,
    }
    write_csv(RUN_ROOT / "trade_shape_summary.csv", SUMMARY_COLUMNS, summary_rows)
    write_csv(RUN_ROOT / "trade_level_records.csv", TRADE_COLUMNS, trade_rows)
    write_csv(RUN_ROOT / "damage_attribution.csv", DAMAGE_COLUMNS, damage_rows)
    write_csv(RUN_ROOT / "side_identity.csv", SIDE_IDENTITY_COLUMNS, side_identity_rows)
    write_json(RUN_ROOT / "sample_fragility.json", fragility)
    ledger_outputs = build_ledgers(summary_rows, damage_rows, fragility)
    summary["ledger_outputs"] = ledger_outputs
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": "run04G",
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "model_family": "sklearn_mlpclassifier_trade_shape_attribution",
        "exploration_label": EXPLORATION_LABEL,
        "stage_inheritance": "independent_no_stage10_11_12_run_baseline_seed_or_reference",
        "boundary": BOUNDARY,
        "inputs": {
            "source_kpi_record": rel(SOURCE_ROOT / "kpi_record.json"),
            "source_reports_root": rel(SOURCE_ROOT / "mt5/reports"),
        },
        "outputs": {
            "summary": rel(RUN_ROOT / "summary.json"),
            "trade_shape_summary": rel(RUN_ROOT / "trade_shape_summary.csv"),
            "damage_attribution": rel(RUN_ROOT / "damage_attribution.csv"),
            "sample_fragility": rel(RUN_ROOT / "sample_fragility.json"),
            "report": rel(REPORT_PATH),
        },
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", summary)
    write_md(RUN_ROOT / "reports/result_summary.md", report_markdown(summary))
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(fragility))
    write_md(PACKET_ROOT / "work_packet.md", work_packet_markdown())
    write_md(REPORT_PATH, report_markdown(summary))
    write_md(DECISION_PATH, decision_markdown(summary))
    update_state_docs(summary)
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "summary": summary})
    return summary


def work_packet_markdown() -> str:
    return "\n".join(
        [
            f"# {PACKET_ID}",
            "",
            "- primary_family(주 작업군): `performance_attribution(성과 기여도 분해)`",
            "- primary_skill(주 스킬): `obsidian-performance-attribution(성과 기여도 분해)`",
            "- source_run(원천 실행): `run04F_mlp_direction_asymmetry_runtime_probe_v1`",
            "- hypothesis(가설): both-direction(양방향) 손상은 trade count(거래 수) 증가보다 방향 상호작용과 drawdown shape(손실 형태)에서 온다.",
            "- evidence_plan(근거 계획): MT5 report deal list(MT5 보고서 거래 목록), damage attribution(손상 기여도), bootstrap sample fragility(부트스트랩 표본 취약성).",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): RUN04F(실행 04F)를 더 깊게 튜닝하지 않고 거래 형태만 분해한다.",
        ]
    )


def _mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _median(values: Sequence[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def _sum(rows: Sequence[Mapping[str, Any]], key: str) -> float:
    return sum(float(row.get(key) or 0.0) for row in rows)


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _max_consecutive_losses(values: Sequence[float]) -> int:
    current = 0
    maximum = 0
    for value in values:
        if value < 0.0:
            current += 1
            maximum = max(maximum, current)
        else:
            current = 0
    return maximum


def _percentile(values: Sequence[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = (len(ordered) - 1) * percentile / 100.0
    low = math.floor(index)
    high = math.ceil(index)
    if low == high:
        return ordered[low]
    return ordered[low] * (high - index) + ordered[high] * (index - low)


def _fmt_ci(values: Sequence[Any]) -> str:
    return ", ".join("NA" if value is None else f"{float(value):.2f}" for value in values)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP direction trade-shape attribution.")
    parser.parse_args(argv)
    summary = build_summary(utc_now())
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
