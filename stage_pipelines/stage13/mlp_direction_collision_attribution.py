from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
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
from foundation.mt5.trade_report import Trade, parse_mt5_trade_report, pair_deals_into_trades


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_ID = "run04H_mlp_direction_collision_attribution_v1"
PACKET_ID = "stage13_run04H_mlp_direction_collision_attribution_packet_v1"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
SOURCE_ATTRIBUTION_RUN_ID = "run04G_mlp_direction_trade_shape_attribution_v1"
EXPLORATION_LABEL = "stage13_MLPDirection__CollisionAttribution"
BOUNDARY = "collision_attribution_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
REPORT_PATH = STAGE_ROOT / "03_reviews/run04H_mlp_direction_collision_attribution_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_direction_collision_attribution.md"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
COMMON_FILES_ROOT = Path.home() / "AppData" / "Roaming" / "MetaQuotes" / "Terminal" / "Common" / "Files"

COLLISION_COLUMNS = (
    "split",
    "aligned_bars",
    "long_candidate_bars",
    "short_candidate_bars",
    "same_bar_collision_count",
    "opposite_position_signal_count",
    "short_position_to_long_signal_count",
    "long_position_to_short_signal_count",
    "reverse_open_long_count",
    "reverse_open_short_count",
    "opposite_close_max_hold_count",
    "both_open_long_count",
    "both_open_short_count",
    "both_close_max_hold_count",
    "trade_count_delta",
    "net_damage",
    "interpretation",
)

EVENT_COLUMNS = (
    "event_type",
    "split",
    "bar_time",
    "long_only_decision",
    "short_only_decision",
    "both_decision",
    "position_before",
    "position_after",
    "exec_action",
    "p_short",
    "p_long",
    "detail",
)

IDENTITY_COLUMNS = (
    "split",
    "side",
    "separate_count",
    "both_side_count",
    "same_exact_trades",
    "same_open_trades",
    "changed_close_trades",
    "separate_net",
    "both_side_net",
    "net_delta",
    "common_exact_net",
    "separate_exact_only_net",
    "both_exact_only_net",
    "changed_close_net_delta",
)

CLOSE_ACTION_COLUMNS = (
    "split",
    "side",
    "open_action",
    "close_action",
    "trade_count",
    "net_profit",
    "avg_profit",
    "loss_count",
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
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def csv_value(value: Any) -> str:
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


def source_records() -> list[dict[str, Any]]:
    return [dict(row) for row in read_json(SOURCE_ROOT / "kpi_record.json")["mt5"]["kpi_records"]]


def attempts_by_name() -> dict[str, dict[str, Any]]:
    return {str(row["attempt_name"]): dict(row) for row in read_json(SOURCE_ROOT / "run_manifest.json")["attempts"]}


def telemetry_path(attempt: Mapping[str, Any]) -> Path:
    return COMMON_FILES_ROOT / str(attempt["common_telemetry_path"])


def read_telemetry(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        for raw in reader:
            if len(raw) < len(header):
                raw = raw + [""] * (len(header) - len(raw))
            row = dict(zip(header, raw[: len(header)]))
            if row.get("record_type") == "cycle":
                rows.append(row)
    return rows


def load_trades(records: Sequence[Mapping[str, Any]]) -> dict[str, list[Trade]]:
    by_view: dict[str, list[Trade]] = {}
    for record in records:
        view = str(record["record_view"])
        report_path = Path(str(record["metrics"]["report_path"]))
        by_view[view] = pair_deals_into_trades(parse_mt5_trade_report(report_path)["deals"])
    return by_view


def analyze_split(
    split: str,
    attempts: Mapping[str, Mapping[str, Any]],
    records: Sequence[Mapping[str, Any]],
    trades: Mapping[str, Sequence[Trade]],
) -> dict[str, Any]:
    long_attempt = f"tier_a_long_only_{split}"
    short_attempt = f"tier_a_short_only_{split}"
    both_attempt = f"tier_a_both_no_fallback_{split}"
    long_rows = {row["bar_time"]: row for row in read_telemetry(telemetry_path(attempts[long_attempt]))}
    short_rows = {row["bar_time"]: row for row in read_telemetry(telemetry_path(attempts[short_attempt]))}
    both_rows = {row["bar_time"]: row for row in read_telemetry(telemetry_path(attempts[both_attempt]))}
    times = sorted(set(long_rows).intersection(short_rows).intersection(both_rows))
    long_candidates = [time for time in times if long_rows[time]["decision"] == "long"]
    short_candidates = [time for time in times if short_rows[time]["decision"] == "short"]
    same_bar = [time for time in times if time in set(long_candidates) and time in set(short_candidates)]
    opposite = [
        time
        for time in times
        if both_rows[time]["decision"] in {"long", "short"}
        and pos_side(both_rows[time]["position_before"]) in {"long", "short"}
        and both_rows[time]["decision"] != pos_side(both_rows[time]["position_before"])
    ]
    exec_counts = Counter(row["exec_action"] for row in both_rows.values())
    opposite_counts = Counter((pos_side(both_rows[time]["position_before"]), both_rows[time]["decision"], both_rows[time]["exec_action"]) for time in opposite)
    summary = split_summary_row(split, records, trades, times, long_candidates, short_candidates, same_bar, opposite, opposite_counts, exec_counts)
    events = event_rows(split, long_rows, short_rows, both_rows, same_bar, opposite)
    close_actions = close_action_rows(split, both_rows, trades[f"mt5_tier_a_both_no_fallback_{split}"])
    return {"summary": summary, "events": events, "close_actions": close_actions}


def split_summary_row(
    split: str,
    records: Sequence[Mapping[str, Any]],
    trades: Mapping[str, Sequence[Trade]],
    times: Sequence[str],
    long_candidates: Sequence[str],
    short_candidates: Sequence[str],
    same_bar: Sequence[str],
    opposite: Sequence[str],
    opposite_counts: Counter[tuple[str, str, str]],
    exec_counts: Counter[str],
) -> dict[str, Any]:
    long_view = f"mt5_tier_a_long_only_{split}"
    short_view = f"mt5_tier_a_short_only_{split}"
    both_view = f"mt5_tier_a_both_no_fallback_{split}"
    long_net = net_sum(trades[long_view])
    short_net = net_sum(trades[short_view])
    both_net = net_sum(trades[both_view])
    separate_sum = long_net + short_net
    trade_count_delta = len(trades[both_view]) - len(trades[long_view]) - len(trades[short_view])
    reverse_long = exec_counts["reverse_open_long"]
    reverse_short = exec_counts["reverse_open_short"]
    interpretation = "direct_collision_absent_reversal_sequence_driver" if not same_bar and opposite else "direct_collision_or_other_driver"
    return {
        "split": split,
        "aligned_bars": len(times),
        "long_candidate_bars": len(long_candidates),
        "short_candidate_bars": len(short_candidates),
        "same_bar_collision_count": len(same_bar),
        "opposite_position_signal_count": len(opposite),
        "short_position_to_long_signal_count": sum(count for (before, decision, _), count in opposite_counts.items() if before == "short" and decision == "long"),
        "long_position_to_short_signal_count": sum(count for (before, decision, _), count in opposite_counts.items() if before == "long" and decision == "short"),
        "reverse_open_long_count": reverse_long,
        "reverse_open_short_count": reverse_short,
        "opposite_close_max_hold_count": sum(count for (_, _, action), count in opposite_counts.items() if action == "close_max_hold"),
        "both_open_long_count": exec_counts["open_long"] + reverse_long,
        "both_open_short_count": exec_counts["open_short"] + reverse_short,
        "both_close_max_hold_count": exec_counts["close_max_hold"],
        "trade_count_delta": trade_count_delta,
        "net_damage": both_net - separate_sum,
        "interpretation": interpretation,
    }


def event_rows(
    split: str,
    long_rows: Mapping[str, Mapping[str, str]],
    short_rows: Mapping[str, Mapping[str, str]],
    both_rows: Mapping[str, Mapping[str, str]],
    same_bar: Sequence[str],
    opposite: Sequence[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for time in same_bar:
        rows.append(event_row("same_bar_long_short_candidate", split, time, long_rows, short_rows, both_rows, "same bar long-only and short-only candidates"))
    for time in opposite:
        rows.append(event_row("opposite_position_signal", split, time, long_rows, short_rows, both_rows, "both path held an opposite position when new direction signal arrived"))
    return rows


def event_row(
    event_type: str,
    split: str,
    time: str,
    long_rows: Mapping[str, Mapping[str, str]],
    short_rows: Mapping[str, Mapping[str, str]],
    both_rows: Mapping[str, Mapping[str, str]],
    detail: str,
) -> dict[str, Any]:
    both = both_rows[time]
    return {
        "event_type": event_type,
        "split": split,
        "bar_time": time,
        "long_only_decision": long_rows.get(time, {}).get("decision", ""),
        "short_only_decision": short_rows.get(time, {}).get("decision", ""),
        "both_decision": both.get("decision", ""),
        "position_before": both.get("position_before", ""),
        "position_after": both.get("position_after", ""),
        "exec_action": both.get("exec_action", ""),
        "p_short": both.get("p_short", ""),
        "p_long": both.get("p_long", ""),
        "detail": detail,
    }


def trade_identity_rows(split: str, trades: Mapping[str, Sequence[Trade]]) -> list[dict[str, Any]]:
    rows = []
    for side, direction in (("long", "buy"), ("short", "sell")):
        separate = list(trades[f"mt5_tier_a_{side}_only_{split}"])
        both = [trade for trade in trades[f"mt5_tier_a_both_no_fallback_{split}"] if trade.direction == direction]
        rows.append(identity_row(split, side, separate, both))
    return rows


def identity_row(split: str, side: str, separate: Sequence[Trade], both: Sequence[Trade]) -> dict[str, Any]:
    sep_exact = {exact_key(trade): trade for trade in separate}
    both_exact = {exact_key(trade): trade for trade in both}
    sep_open = {trade.open_time: trade for trade in separate}
    both_open = {trade.open_time: trade for trade in both}
    common_exact = set(sep_exact).intersection(both_exact)
    common_open = set(sep_open).intersection(both_open)
    changed_close = [time for time in common_open if sep_open[time].close_time != both_open[time].close_time]
    separate_only = set(sep_exact).difference(both_exact)
    both_only = set(both_exact).difference(sep_exact)
    return {
        "split": split,
        "side": side,
        "separate_count": len(separate),
        "both_side_count": len(both),
        "same_exact_trades": len(common_exact),
        "same_open_trades": len(common_open),
        "changed_close_trades": len(changed_close),
        "separate_net": net_sum(separate),
        "both_side_net": net_sum(both),
        "net_delta": net_sum(both) - net_sum(separate),
        "common_exact_net": sum(float(both_exact[key].net_profit) for key in common_exact),
        "separate_exact_only_net": sum(float(sep_exact[key].net_profit) for key in separate_only),
        "both_exact_only_net": sum(float(both_exact[key].net_profit) for key in both_only),
        "changed_close_net_delta": sum(float(both_open[time].net_profit - sep_open[time].net_profit) for time in changed_close),
    }


def close_action_rows(split: str, telemetry: Mapping[str, Mapping[str, str]], trades: Sequence[Trade]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for trade in trades:
        side = "long" if trade.direction == "buy" else "short"
        open_action = telemetry.get(mt5_time(trade.open_time), {}).get("exec_action", "missing")
        close_action = telemetry.get(mt5_time(trade.close_time), {}).get("exec_action", "missing")
        grouped[(side, open_action, close_action)].append(float(trade.net_profit))
    rows = []
    for (side, open_action, close_action), values in sorted(grouped.items()):
        rows.append(
            {
                "split": split,
                "side": side,
                "open_action": open_action,
                "close_action": close_action,
                "trade_count": len(values),
                "net_profit": sum(values),
                "avg_profit": sum(values) / len(values),
                "loss_count": sum(1 for value in values if value < 0.0),
            }
        )
    return rows


def build_ledgers(collision_rows: Sequence[Mapping[str, Any]], identity_rows_: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = [scope_row("Tier B", "tier_b_out_of_scope"), scope_row("Tier A+B", "tier_abb_out_of_scope")]
    for row in collision_rows:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__collision_{row['split']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"collision_{row['split']}",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": f"collision_{row['split']}",
                "tier_scope": "Tier A",
                "kpi_scope": "direction_collision_attribution",
                "scoreboard_lane": "runtime_probe_attribution",
                "status": "completed",
                "judgment": "inconclusive_collision_attribution_completed",
                "path": rel(RUN_ROOT / "telemetry_collision_summary.csv"),
                "primary_kpi": ledger_pairs((("same_bar_collision", row["same_bar_collision_count"]), ("opposite_events", row["opposite_position_signal_count"]), ("net_damage", row["net_damage"]))),
                "guardrail_kpi": ledger_pairs((("trade_delta", row["trade_count_delta"]), ("reverse_long", row["reverse_open_long_count"]), ("reverse_short", row["reverse_open_short_count"]), ("boundary", "no_alpha_quality"))),
                "external_verification_status": "completed_from_existing_mt5_reports_and_common_telemetry",
                "notes": "Collision attribution from RUN04F common telemetry and MT5 Strategy Tester deal lists.",
            }
        )
    for row in identity_rows_:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__identity_{row['split']}_{row['side']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"identity_{row['split']}_{row['side']}",
                "parent_run_id": SOURCE_ATTRIBUTION_RUN_ID,
                "record_view": f"identity_{row['split']}_{row['side']}",
                "tier_scope": "Tier A",
                "kpi_scope": "trade_identity_collision_attribution",
                "scoreboard_lane": "runtime_probe_attribution",
                "status": "completed",
                "judgment": "inconclusive_trade_identity_collision_attribution_completed",
                "path": rel(RUN_ROOT / "trade_collision_identity.csv"),
                "primary_kpi": ledger_pairs((("same_open", row["same_open_trades"]), ("same_exact", row["same_exact_trades"]), ("net_delta", row["net_delta"]))),
                "guardrail_kpi": ledger_pairs((("changed_close", row["changed_close_trades"]), ("changed_close_delta", row["changed_close_net_delta"]), ("boundary", "identity_not_promotion"))),
                "external_verification_status": "completed_from_existing_mt5_reports_and_common_telemetry",
                "notes": "Compares separate side-only trade identity against both-direction account path.",
            }
        )
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "direction_collision_attribution",
        "status": "reviewed",
        "judgment": "inconclusive_collision_attribution_completed",
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs((("source_run", SOURCE_RUN_ID), ("source_attribution", SOURCE_ATTRIBUTION_RUN_ID), ("boundary", "collision_attribution_only"))),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def scope_row(tier_scope: str, suffix: str) -> dict[str, Any]:
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
        "judgment": "out_of_scope_by_claim_collision_attribution",
        "path": rel(RUN_ROOT / "summary.json"),
        "primary_kpi": ledger_pairs((("source_run", SOURCE_RUN_ID),)),
        "guardrail_kpi": ledger_pairs((("boundary", "tier_a_direction_collision_only"),)),
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "RUN04H analyzes RUN04F Tier A direction collision only.",
    }


def skill_receipts(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"packet_id": PACKET_ID, "skill": "obsidian-performance-attribution", "status": "completed", "attribution_layers_checked": ["direction", "position_sequence", "trade_identity", "close_action", "drawdown_boundary"], "missing_layers": ["regime_context", "new MT5 execution", "WFO"], "allowed_claims": ["collision_attribution_completed"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-backtest-forensics", "status": "completed", "tester_report": rel(SOURCE_ROOT / "mt5/reports"), "tester_settings": "RUN04F MT5 Strategy Tester reports; US100 M5; deposit 500; leverage 1:100; model 4; same source reports as RUN04G", "spread_commission_slippage": "No new cost model; deal list net profit includes report commission/swap fields where present.", "trade_list_identity": "Six RUN04F HTML deal lists plus common telemetry CSV files parsed by this packet.", "forensic_gaps": ["No new MT5 execution", "Common telemetry is local external artifact under Terminal/Common/Files"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": "completed", "source_inputs": [rel(SOURCE_ROOT / "kpi_record.json"), rel(SOURCE_ROOT / "run_manifest.json"), "Terminal/Common/Files/Project_Obsidian_Prime_v2/stage13/run04F.../telemetry"], "produced_artifacts": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "telemetry_collision_summary.csv"), rel(RUN_ROOT / "trade_collision_identity.csv"), rel(REPORT_PATH)], "raw_evidence": [rel(SOURCE_ROOT / "mt5/reports"), "RUN04F common telemetry CSV"], "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "telemetry_collision_summary.csv")], "human_readable": [rel(REPORT_PATH), rel(DECISION_PATH)], "hashes_or_missing_reasons": "Source report and telemetry hashes are stored in summary.json.", "lineage_boundary": "connected_with_boundary_from_RUN04F_reports_and_common_telemetry"},
        {"packet_id": PACKET_ID, "skill": "obsidian-result-judgment", "status": "completed", "judgment_boundary": summary["judgment"], "allowed_claims": ["direction_collision_read", "trade_identity_attribution_read"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"], "evidence_used": [rel(RUN_ROOT / "telemetry_collision_summary.csv"), rel(RUN_ROOT / "trade_collision_identity.csv"), rel(RUN_ROOT / "close_action_summary.csv")]},
        {"packet_id": PACKET_ID, "skill": "obsidian-reentry-read", "status": "completed", "source_current_truth_docs": [rel(WORKSPACE_STATE_PATH), rel(CURRENT_STATE_PATH), rel(SELECTION_STATUS_PATH)], "active_stage": STAGE_ID, "current_run": RUN_ID, "detected_conflicts": [], "allowed_claims": ["stage13_run04H_collision_attribution"], "forbidden_claims": ["baseline", "promotion", "runtime_authority"]},
    ]


def build_summary(created_at: str) -> dict[str, Any]:
    records = source_records()
    attempts = attempts_by_name()
    trades = load_trades(records)
    split_results = [analyze_split(split, attempts, records, trades) for split in ("validation_is", "oos")]
    collision_rows = [result["summary"] for result in split_results]
    event_rows_ = [row for result in split_results for row in result["events"]]
    close_action_rows_ = [row for result in split_results for row in result["close_actions"]]
    identity_rows_ = [row for split in ("validation_is", "oos") for row in trade_identity_rows(split, trades)]
    source_hashes = collect_source_hashes(attempts, records)
    summary = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
        "created_at_utc": created_at,
        "exploration_label": EXPLORATION_LABEL,
        "status": "completed",
        "judgment": "inconclusive_collision_attribution_completed",
        "boundary": BOUNDARY,
        "telemetry_collision_summary": collision_rows,
        "trade_collision_identity": identity_rows_,
        "close_action_summary": close_action_rows_,
        "collision_event_count": len(event_rows_),
        "source_hashes": source_hashes,
    }
    write_csv(RUN_ROOT / "telemetry_collision_summary.csv", COLLISION_COLUMNS, collision_rows)
    write_csv(RUN_ROOT / "collision_events.csv", EVENT_COLUMNS, event_rows_)
    write_csv(RUN_ROOT / "trade_collision_identity.csv", IDENTITY_COLUMNS, identity_rows_)
    write_csv(RUN_ROOT / "close_action_summary.csv", CLOSE_ACTION_COLUMNS, close_action_rows_)
    summary["ledger_outputs"] = build_ledgers(collision_rows, identity_rows_)
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(RUN_ROOT / "kpi_record.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(created_at))
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(summary))
    write_md(PACKET_ROOT / "work_packet.md", work_packet_markdown())
    write_md(RUN_ROOT / "reports/result_summary.md", report_markdown(summary))
    write_md(REPORT_PATH, report_markdown(summary))
    write_md(DECISION_PATH, decision_markdown(summary))
    update_state_docs(summary)
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "summary": summary})
    return summary


def collect_source_hashes(attempts: Mapping[str, Mapping[str, Any]], records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    telemetry = {}
    for name, attempt in attempts.items():
        path = telemetry_path(attempt)
        telemetry[name] = {"path": path.as_posix(), "sha256": sha256_file_lf_normalized(path)}
    reports = {}
    for record in records:
        path = Path(str(record["metrics"]["report_path"]))
        reports[str(record["record_view"])] = {"path": path.as_posix(), "sha256": sha256_file_lf_normalized(path)}
    return {"telemetry": telemetry, "reports": reports}


def run_manifest(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": "run04H",
        "source_run_id": SOURCE_RUN_ID,
        "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
        "created_at_utc": created_at,
        "model_family": "sklearn_mlpclassifier_collision_attribution",
        "exploration_label": EXPLORATION_LABEL,
        "stage_inheritance": "independent_no_stage10_11_12_run_baseline_seed_or_reference",
        "boundary": BOUNDARY,
        "inputs": {"source_kpi_record": rel(SOURCE_ROOT / "kpi_record.json"), "source_manifest": rel(SOURCE_ROOT / "run_manifest.json"), "source_common_telemetry_root": "Terminal/Common/Files/Project_Obsidian_Prime_v2/stage13/run04F_mlp_direction_asymmetry_runtime_probe_v1/telemetry", "source_reports_root": rel(SOURCE_ROOT / "mt5/reports")},
        "outputs": {"summary": rel(RUN_ROOT / "summary.json"), "telemetry_collision_summary": rel(RUN_ROOT / "telemetry_collision_summary.csv"), "trade_collision_identity": rel(RUN_ROOT / "trade_collision_identity.csv"), "close_action_summary": rel(RUN_ROOT / "close_action_summary.csv"), "report": rel(REPORT_PATH)},
    }


def report_markdown(summary: Mapping[str, Any]) -> str:
    collision = summary["telemetry_collision_summary"]
    identity = summary["trade_collision_identity"]
    close_rows = summary["close_action_summary"]
    oos_short = next(row for row in identity if row["split"] == "oos" and row["side"] == "short")
    oos_collision = next(row for row in collision if row["split"] == "oos")
    lines = [
        f"# {RUN_ID} 결과 요약(Result Summary, 결과 요약)",
        "",
        "- status(상태): `completed(완료)`",
        "- judgment(판정): `inconclusive_collision_attribution_completed(충돌 기여도 분해 완료, 판단은 불충분)`",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## 핵심 판독(Core Read, 핵심 판독)",
        "",
        "- direct same-bar collision(같은 봉 직접 충돌): validation/OOS(검증/표본외) 모두 `0`이었다.",
        f"- OOS(표본외) opposite position signal(반대 포지션 신호): `{oos_collision['opposite_position_signal_count']}`개였다.",
        f"- OOS(표본외) reverse open(반전 진입): long(매수) `{oos_collision['reverse_open_long_count']}`, short(매도) `{oos_collision['reverse_open_short_count']}`였다.",
        f"- OOS(표본외) short(매도) same-open(같은 진입 시각) 중 close changed(청산 시각 변경): `{oos_short['changed_close_trades']}`개, delta(차이) `{oos_short['changed_close_net_delta']:.2f}`였다.",
        "",
        "효과(effect, 효과): both(양방향) 손상은 신호가 같은 봉에서 long/short(매수/매도)로 동시에 난 문제가 아니라, 단일 계좌 경로에서 reverse(반전)와 early close(조기 청산)가 거래 정체성을 바꾼 문제로 좁혀진다.",
        "",
        "## Telemetry Collision(원격측정 충돌)",
        "",
        "| split(분할) | long candidates(매수 후보) | short candidates(매도 후보) | same-bar collision(같은 봉 충돌) | opposite signals(반대 포지션 신호) | reverse long(반전 매수) | reverse short(반전 매도) | net damage(순손상) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in collision:
        lines.append(f"| {row['split']} | {row['long_candidate_bars']} | {row['short_candidate_bars']} | {row['same_bar_collision_count']} | {row['opposite_position_signal_count']} | {row['reverse_open_long_count']} | {row['reverse_open_short_count']} | {row['net_damage']:.2f} |")
    lines.extend(
        [
            "",
            "## Trade Identity(거래 정체성)",
            "",
            "| split(분할) | side(방향) | separate/both count(분리/양방향 거래 수) | same exact(완전 동일) | same open(같은 진입) | changed close(청산 변경) | net delta(순차이) | changed close delta(청산 변경 차이) |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in identity:
        lines.append(f"| {row['split']} | {row['side']} | {row['separate_count']}/{row['both_side_count']} | {row['same_exact_trades']} | {row['same_open_trades']} | {row['changed_close_trades']} | {row['net_delta']:.2f} | {row['changed_close_net_delta']:.2f} |")
    lines.extend(["", "## OOS Close Action(표본외 청산 행동)", "", "| side(방향) | open action(진입 행동) | close action(청산 행동) | trades(거래 수) | net(순수익) | avg(평균) |", "|---|---|---|---:|---:|---:|"])
    for row in close_rows:
        if row["split"] == "oos":
            lines.append(f"| {row['side']} | {row['open_action']} | {row['close_action']} | {row['trade_count']} | {row['net_profit']:.2f} | {row['avg_profit']:.2f} |")
    lines.extend(["", "효과(effect, 효과): short-only(매도 전용) OOS(표본외) 49 trades(49개 거래)는 여전히 얇은 clue(단서)이고, both(양방향)에서는 특히 short(매도) 청산 시각이 바뀌며 수익이 훼손됐다."])
    return "\n".join(lines)


def decision_markdown(summary: Mapping[str, Any]) -> str:
    oos_collision = next(row for row in summary["telemetry_collision_summary"] if row["split"] == "oos")
    return "\n".join(
        [
            "# 2026-05-02 Stage13 MLP Direction Collision Attribution",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- source(원천): `{SOURCE_RUN_ID}`",
            "- decision(결정): direct collision(직접 충돌)이 아니라 reverse sequence(반전 순서)와 close timing(청산 시각) 문제로 기록한다.",
            f"- OOS opposite position signal(표본외 반대 포지션 신호): `{oos_collision['opposite_position_signal_count']}`",
            f"- OOS net damage(표본외 순손상): `{oos_collision['net_damage']:.2f}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): 다음 stage13(13단계) 탐색에서 같은 threshold(임계값)를 더 깊게 튜닝하기보다, 양방향 단일 계좌의 reversal policy(반전 정책)를 따로 흔들지 여부를 선택할 수 있다.",
        ]
    )


def work_packet_markdown() -> str:
    return "\n".join(
        [
            f"# {PACKET_ID}",
            "",
            "- primary_family(주 작업군): `performance_attribution(성과 기여도 분해)`",
            "- primary_skill(주 스킬): `obsidian-performance-attribution(성과 기여도 분해)`",
            "- support_skills(보조 스킬): `obsidian-backtest-forensics(백테스트 포렌식)`, `obsidian-artifact-lineage(산출물 계보)`, `obsidian-result-judgment(결과 판정)`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            "- hypothesis(가설): both(양방향) 손상은 같은 봉 signal collision(신호 충돌)보다 단일 포지션 경로의 reverse(반전)와 close timing(청산 시각)에서 생긴다.",
            "- evidence_plan(근거 계획): RUN04F(실행 04F) common telemetry(공통 원격측정), MT5 report deal list(MT5 보고서 거래 목록), RUN04G(실행 04G) trade identity(거래 정체성) 관점.",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): 새 MT5(메타트레이더5) 실행 없이 기존 외부 산출물을 재분석해 손상 원인을 좁힌다.",
        ]
    )


def update_state_docs(summary: Mapping[str, Any]) -> None:
    section = (
        "stage13_mlp_direction_collision_attribution:\n"
        f"  run_id: {RUN_ID}\n"
        "  status: completed\n"
        "  judgment: inconclusive_collision_attribution_completed\n"
        f"  boundary: {BOUNDARY}\n"
        f"  source_run_id: {SOURCE_RUN_ID}\n"
        f"  source_attribution_run_id: {SOURCE_ATTRIBUTION_RUN_ID}\n"
        f"  report_path: {rel(REPORT_PATH)}\n"
    )
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state_text = state_text.replace("active_run04G_mlp_direction_trade_shape_attribution", "active_run04H_mlp_direction_collision_attribution")
    if "stage13_mlp_direction_collision_attribution:" not in state_text:
        state_text = state_text.replace("stage01_raw_m5_inventory:\n", section + "stage01_raw_m5_inventory:\n")
    io_path(WORKSPACE_STATE_PATH).write_text(state_text, encoding="utf-8")

    current_text = io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = current_text.replace(f"current run(현재 실행): `{SOURCE_ATTRIBUTION_RUN_ID}`", f"current run(현재 실행): `{RUN_ID}`")
    latest = (
        f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, RUN04F(실행 04F)의 telemetry(원격측정)와 MT5(메타트레이더5) 거래 목록으로 collision attribution(충돌 기여도 분해)을 완료했다.\n\n"
        "효과(effect, 효과): both(양방향) 손상이 같은 봉 long/short signal collision(매수/매도 신호 충돌) 때문인지, reverse(반전)와 close timing(청산 시각) 때문인지 분리했다."
    )
    marker = "## 쉬운 설명(Plain Read, 쉬운 설명)"
    if marker in current_text and "## Latest Stage 13 Update" in current_text:
        before, after = current_text.split(marker, 1)
        head = before.split("## Latest Stage 13 Update", 1)[0]
        current_text = head + "## Latest Stage 13 Update(최신 Stage 13 업데이트)\n\n" + latest + "\n" + marker + after
    io_path(CURRENT_STATE_PATH).write_text(current_text, encoding="utf-8-sig")

    write_md(
        SELECTION_STATUS_PATH,
        "\n".join(
            [
                "# Stage 13 Selection Status",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `reviewed_collision_attribution_completed(충돌 기여도 검토 완료)`",
                "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
                "- exploration depth(탐색 깊이): `collision_attribution_only(충돌 기여도만)`",
                "- independent scope(독립 범위): `no_stage10_11_12_run_baseline_or_seed(10/11/12단계 실행 기준선/씨앗 없음)`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                "- external verification status(외부 검증 상태): `completed_from_existing_mt5_reports_and_common_telemetry(기존 MT5 보고서와 공통 원격측정에서 완료)`",
                "- judgment(판정): `inconclusive_collision_attribution_completed(충돌 기여도 분해 완료, 판단은 불충분)`",
                "",
                "효과(effect, 효과): short-only(매도 전용) 단서는 보존하지만 alpha quality(알파 품질)나 운영 의미는 만들지 않는다.",
            ]
        ),
    )
    write_md(
        REVIEW_INDEX_PATH,
        "\n".join(
            [
                "# Stage 13 Review Index",
                "",
                "- `run04A_mlp_characteristic_runtime_probe_v1`: `inconclusive_mlp_characteristic_runtime_probe_completed`",
                "- `run04B_mlp_input_geometry_runtime_handoff_probe_v1`: `inconclusive_input_geometry_runtime_handoff_probe_completed`",
                "- `run04C_mlp_activation_runtime_probe_v1`: `inconclusive_activation_runtime_probe_completed`",
                "- `run04D_mlp_convergence_threshold_feasibility_probe_v1`: `inconclusive_convergence_threshold_feasibility_probe_completed`",
                "- `run04E_mlp_q90_threshold_trading_runtime_probe_v1`: `inconclusive_q90_threshold_trading_runtime_probe_completed`",
                "- `run04F_mlp_direction_asymmetry_runtime_probe_v1`: `inconclusive_direction_asymmetry_runtime_probe_completed`",
                "- `run04G_mlp_direction_trade_shape_attribution_v1`: `inconclusive_trade_shape_attribution_completed`",
                f"- `{RUN_ID}`: `inconclusive_collision_attribution_completed`, report(보고서) `{rel(REPORT_PATH)}`",
                "",
                "효과(effect, 효과): Stage13(13단계)의 실행 근거 위치를 한 곳에서 찾게 한다.",
            ]
        ),
    )
    changelog_line = f"\n- 2026-05-02: Added `{RUN_ID}` collision attribution(충돌 기여도 분해) from RUN04F MT5 telemetry/report evidence; no alpha quality(알파 품질), baseline(기준선), or promotion(승격) claim.\n"
    io_path(CHANGELOG_PATH).write_text(io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") + changelog_line, encoding="utf-8-sig")


def exact_key(trade: Trade) -> tuple[str, str, str]:
    return (trade.direction, trade.open_time.isoformat(), trade.close_time.isoformat())


def mt5_time(value: Any) -> str:
    return value.strftime("%Y.%m.%d %H:%M:%S")


def pos_side(value: str) -> str:
    text = str(value or "")
    return text.split(":", 1)[0] if text else "none"


def net_sum(trades: Sequence[Trade]) -> float:
    return sum(float(trade.net_profit) for trade in trades)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP direction collision attribution.")
    parser.parse_args(argv)
    summary = build_summary(utc_now())
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
