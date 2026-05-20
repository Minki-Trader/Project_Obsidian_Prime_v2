from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_NUMBER = "run267C"
RUN_ID = "run267C_stage267_execute_prioritized_ablation_replacement_variants_v1"
PACKET_ID = input_probe.PACKET_ID
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY
STAGE_ROOT = input_probe.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN267B_HIST_ROOT = input_probe.HIST_ROOT
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH

TRADE_RECORDS_PATH = RUN267B_HIST_ROOT / "trade_records.csv"
DESIGN_PATH = RUN267B_HIST_ROOT / "ablation_replacement_design.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
COUNTERFACTUAL_KPI_PATH = RUN_ROOT / "weak_slice_counterfactual_kpi.csv"
INTERSECTION_KPI_PATH = RUN_ROOT / "weak_slice_intersection_kpi.csv"
TRIAGE_SUMMARY_PATH = RUN_ROOT / "candidate_counterfactual_triage_summary.csv"
RESULT_PATH = RUN_ROOT / "weak_slice_counterfactual_triage.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_weak_slice_counterfactual_triage_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_weak_slice_counterfactual_triage.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

STATUS = "stage267_run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending"
NEXT_ACTION = "run267C_materialize_p0_mt5_variants_from_counterfactual_triage"
DEPOSIT = 500.0


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return value


def fnum(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"Missing text for replacement: {old}")
    return text.replace(old, new, 1)


def append_line_after_anchor(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"Missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    wins = sum(fnum(row.get("net_profit")) for row in rows if fnum(row.get("net_profit")) > 0.0)
    losses = -sum(fnum(row.get("net_profit")) for row in rows if fnum(row.get("net_profit")) < 0.0)
    if losses == 0.0:
        return math.inf if wins > 0.0 else None
    return wins / losses


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    underwater = 0
    longest_underwater = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += fnum(row.get("net_profit"))
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            longest_underwater = max(longest_underwater, underwater)
        dd = peak - balance
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd / peak * 100.0 if peak else 0.0)
    return max_dd, max_dd_pct, longest_underwater


def metrics(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    trade_count = len(ordered)
    net = sum(fnum(row.get("net_profit")) for row in ordered)
    wins = sum(1 for row in ordered if fnum(row.get("net_profit")) > 0.0)
    max_dd, max_dd_pct, longest_underwater = max_closed_balance_drawdown(ordered)
    return {
        "trade_count": trade_count,
        "net_profit": net,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / trade_count if trade_count else None,
        "win_rate": wins / trade_count if trade_count else None,
        "closed_balance_max_drawdown": max_dd,
        "closed_balance_max_drawdown_percent": max_dd_pct,
        "longest_underwater_trades": longest_underwater,
    }


def candidate_groups() -> dict[str, list[dict[str, str]]]:
    rows = [
        row
        for row in read_csv_rows(TRADE_RECORDS_PATH)
        if row.get("route_role") == "routed_total" and row.get("tier_scope") == "Tier A+B"
    ]
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("candidate_id"))].append(row)
    return dict(groups)


FilterFn = Callable[[Mapping[str, str]], bool]


def intervention_specs() -> list[dict[str, Any]]:
    return [
        {
            "intervention_id": "cf_remove_vol_low",
            "design_links": "d01_vol_low_volatility_bandwidth_ablation;d02_vol_low_atr_to_historical_vol_replacement",
            "weakness_axis": "volatility_regime",
            "weakness_bucket": "vol_low",
            "counterfactual_action": "remove trades whose close attribution is vol_low",
            "predicate": lambda row: row.get("volatility_regime") != "vol_low",
        },
        {
            "intervention_id": "cf_remove_2024_07",
            "design_links": "d05_july_2024_holdout_stress",
            "weakness_axis": "month",
            "weakness_bucket": "2024-07",
            "counterfactual_action": "remove trades closed in 2024-07",
            "predicate": lambda row: row.get("month") != "2024-07",
        },
        {
            "intervention_id": "cf_remove_monday",
            "design_links": "d06_monday_session_timing_ablation",
            "weakness_axis": "weekday",
            "weakness_bucket": "Monday",
            "counterfactual_action": "remove trades closed on Monday",
            "predicate": lambda row: row.get("weekday") != "Monday",
        },
        {
            "intervention_id": "cf_remove_late_session",
            "design_links": "d07_late_session_interaction_engineering",
            "weakness_axis": "session_slice",
            "weakness_bucket": "late",
            "counterfactual_action": "remove trades attributed to late session",
            "predicate": lambda row: row.get("session_slice") != "late",
        },
        {
            "intervention_id": "cf_remove_vol_low_or_late",
            "design_links": "d01_vol_low_volatility_bandwidth_ablation;d07_late_session_interaction_engineering",
            "weakness_axis": "compound",
            "weakness_bucket": "vol_low_or_late",
            "counterfactual_action": "remove trades that are vol_low or late session",
            "predicate": lambda row: row.get("volatility_regime") != "vol_low" and row.get("session_slice") != "late",
        },
        {
            "intervention_id": "cf_remove_vol_low_or_july",
            "design_links": "d01_vol_low_volatility_bandwidth_ablation;d05_july_2024_holdout_stress",
            "weakness_axis": "compound",
            "weakness_bucket": "vol_low_or_2024_07",
            "counterfactual_action": "remove trades that are vol_low or closed in 2024-07",
            "predicate": lambda row: row.get("volatility_regime") != "vol_low" and row.get("month") != "2024-07",
        },
        {
            "intervention_id": "cf_remove_all_common_weak_axes",
            "design_links": "d01_vol_low_volatility_bandwidth_ablation;d05_july_2024_holdout_stress;d06_monday_session_timing_ablation;d07_late_session_interaction_engineering",
            "weakness_axis": "compound",
            "weakness_bucket": "vol_low_or_2024_07_or_Monday_or_late",
            "counterfactual_action": "remove trades touching any common weak axis",
            "predicate": lambda row: (
                row.get("volatility_regime") != "vol_low"
                and row.get("month") != "2024-07"
                and row.get("weekday") != "Monday"
                and row.get("session_slice") != "late"
            ),
        },
    ]


def intersection_specs() -> list[dict[str, Any]]:
    return [
        {
            "intersection_id": "ix_vol_low_late",
            "design_links": "d01;d07",
            "predicate": lambda row: row.get("volatility_regime") == "vol_low" and row.get("session_slice") == "late",
        },
        {
            "intersection_id": "ix_vol_low_july",
            "design_links": "d01;d05",
            "predicate": lambda row: row.get("volatility_regime") == "vol_low" and row.get("month") == "2024-07",
        },
        {
            "intersection_id": "ix_july_late",
            "design_links": "d05;d07",
            "predicate": lambda row: row.get("month") == "2024-07" and row.get("session_slice") == "late",
        },
        {
            "intersection_id": "ix_monday_late",
            "design_links": "d06;d07",
            "predicate": lambda row: row.get("weekday") == "Monday" and row.get("session_slice") == "late",
        },
        {
            "intersection_id": "ix_chron_mid_vol_low",
            "design_links": "d01;d09",
            "predicate": lambda row: row.get("chron_segment") == "chron_mid" and row.get("volatility_regime") == "vol_low",
        },
        {
            "intersection_id": "ix_chron_mid_july",
            "design_links": "d05;d09",
            "predicate": lambda row: row.get("chron_segment") == "chron_mid" and row.get("month") == "2024-07",
        },
    ]


def read_for_delta(baseline: Mapping[str, Any], variant: Mapping[str, Any]) -> str:
    trade_retention = fnum(variant.get("trade_retention"))
    net_delta = fnum(variant.get("net_delta"))
    dd_delta = fnum(variant.get("dd_percent_delta"))
    if trade_retention < 0.65:
        return "overpruned_not_candidate_solution"
    if net_delta > 100.0 and dd_delta < -5.0 and trade_retention >= 0.75:
        return "promising_counterfactual_requires_mt5_variant"
    if net_delta > 100.0 and trade_retention >= 0.65:
        return "damage_concentrated_but_filter_costly"
    if net_delta > 0.0:
        return "minor_counterfactual_improvement"
    return "not_a_repair_direction"


def build_counterfactual_rows(groups: Mapping[str, Sequence[Mapping[str, str]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate_id, trades in groups.items():
        baseline = metrics(trades)
        for spec in intervention_specs():
            kept = [row for row in trades if spec["predicate"](row)]
            removed = [row for row in trades if not spec["predicate"](row)]
            variant = metrics(kept)
            removed_metrics = metrics(removed)
            row = {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "candidate_alias": trades[0].get("candidate_alias") if trades else "",
                "candidate_role": trades[0].get("candidate_role") if trades else "",
                "intervention_id": spec["intervention_id"],
                "design_links": spec["design_links"],
                "weakness_axis": spec["weakness_axis"],
                "weakness_bucket": spec["weakness_bucket"],
                "counterfactual_action": spec["counterfactual_action"],
                "baseline_trade_count": baseline["trade_count"],
                "baseline_net_profit": baseline["net_profit"],
                "baseline_profit_factor": baseline["profit_factor"],
                "baseline_expectancy": baseline["expectancy"],
                "baseline_dd_percent": baseline["closed_balance_max_drawdown_percent"],
                "kept_trade_count": variant["trade_count"],
                "kept_net_profit": variant["net_profit"],
                "kept_profit_factor": variant["profit_factor"],
                "kept_expectancy": variant["expectancy"],
                "kept_dd_percent": variant["closed_balance_max_drawdown_percent"],
                "removed_trade_count": removed_metrics["trade_count"],
                "removed_net_profit": removed_metrics["net_profit"],
                "removed_profit_factor": removed_metrics["profit_factor"],
                "trade_retention": variant["trade_count"] / baseline["trade_count"] if baseline["trade_count"] else None,
                "net_delta": fnum(variant["net_profit"]) - fnum(baseline["net_profit"]),
                "pf_delta": (
                    fnum(variant["profit_factor"]) - fnum(baseline["profit_factor"])
                    if variant["profit_factor"] not in {None, math.inf} and baseline["profit_factor"] not in {None, math.inf}
                    else None
                ),
                "dd_percent_delta": fnum(variant["closed_balance_max_drawdown_percent"])
                - fnum(baseline["closed_balance_max_drawdown_percent"]),
            }
            row["counterfactual_read"] = read_for_delta(baseline, row)
            rows.append(row)
    return sorted(rows, key=lambda item: (str(item["candidate_alias"]), str(item["intervention_id"])))


def build_intersection_rows(groups: Mapping[str, Sequence[Mapping[str, str]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate_id, trades in groups.items():
        baseline = metrics(trades)
        for spec in intersection_specs():
            selected = [row for row in trades if spec["predicate"](row)]
            item = metrics(selected)
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "candidate_alias": trades[0].get("candidate_alias") if trades else "",
                    "candidate_role": trades[0].get("candidate_role") if trades else "",
                    "intersection_id": spec["intersection_id"],
                    "design_links": spec["design_links"],
                    "baseline_trade_count": baseline["trade_count"],
                    "baseline_net_profit": baseline["net_profit"],
                    "intersection_trade_count": item["trade_count"],
                    "intersection_net_profit": item["net_profit"],
                    "intersection_profit_factor": item["profit_factor"],
                    "intersection_expectancy": item["expectancy"],
                    "intersection_dd_percent": item["closed_balance_max_drawdown_percent"],
                    "trade_share": item["trade_count"] / baseline["trade_count"] if baseline["trade_count"] else None,
                    "net_share": item["net_profit"] / baseline["net_profit"] if baseline["net_profit"] else None,
                    "slice_read": "negative_intersection" if item["net_profit"] < 0.0 else "nonnegative_intersection",
                }
            )
    return sorted(rows, key=lambda item: (str(item["candidate_alias"]), fnum(item["intersection_net_profit"])))


def triage_label(best: Mapping[str, Any]) -> str:
    read = str(best.get("counterfactual_read"))
    if read == "promising_counterfactual_requires_mt5_variant":
        return "mt5_variant_worth_testing"
    if read == "damage_concentrated_but_filter_costly":
        return "needs_feature_engineering_not_naive_filter"
    if read == "overpruned_not_candidate_solution":
        return "broad_fragility_or_overprune"
    return "weak_counterfactual_evidence"


def build_candidate_summary(counterfactual_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in counterfactual_rows:
        grouped[str(row["candidate_id"])].append(row)
    summaries: list[dict[str, Any]] = []
    for candidate_id, rows in grouped.items():
        best = max(rows, key=lambda row: (fnum(row.get("net_delta")), -abs(fnum(row.get("trade_retention")) - 0.8)))
        p0_reads = ";".join(
            f"{row['intervention_id']}={row['counterfactual_read']}"
            for row in rows
            if str(row.get("design_links", "")).startswith("d01")
            or "d05" in str(row.get("design_links", ""))
            or "d07" in str(row.get("design_links", ""))
            or "d08" in str(row.get("design_links", ""))
        )
        summaries.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "candidate_alias": best.get("candidate_alias"),
                "candidate_role": best.get("candidate_role"),
                "baseline_net_profit": best.get("baseline_net_profit"),
                "baseline_profit_factor": best.get("baseline_profit_factor"),
                "baseline_trade_count": best.get("baseline_trade_count"),
                "baseline_dd_percent": best.get("baseline_dd_percent"),
                "best_counterfactual": best.get("intervention_id"),
                "best_net_delta": best.get("net_delta"),
                "best_trade_retention": best.get("trade_retention"),
                "best_dd_percent_delta": best.get("dd_percent_delta"),
                "triage_label": triage_label(best),
                "p0_design_read": p0_reads,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return sorted(summaries, key=lambda item: fnum(item.get("best_net_delta")), reverse=True)


def upsert_simple_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv_rows(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(row)
    write_csv(path, merged, columns)


def upsert_stage_ledger() -> None:
    row = {
        "row_id": "stage267_run267C_weak_slice_counterfactual_triage",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "weak_slice_counterfactual_triage",
        "tier_scope": "Tier A+B routed historical 2024 trade records",
        "scoreboard": "trade_shape",
        "status": "completed_counterfactual_triage_mt5_variants_pending",
        "judgment": "exploratory_counterfactual_only_no_candidate_selection",
        "evidence_boundary": "closed_trade_counterfactual_not_mt5_rerun_not_feature_ablation_proof",
        "report_path": rel(REPORT_PATH),
        "notes": "Weak-slice counterfactual triage completed from run267B trade records; selected candidate none.",
    }
    rows = input_probe.read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    input_probe.write_csv(
        STAGE_LEDGER_PATH,
        merged,
        (
            "row_id",
            "stage_id",
            "run_id",
            "view",
            "tier_scope",
            "scoreboard",
            "status",
            "judgment",
            "evidence_boundary",
            "report_path",
            "notes",
        ),
    )


def upsert_run_registers() -> None:
    upsert_simple_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_counterfactual_triage",
            "status": "completed_counterfactual_triage_mt5_variants_pending",
            "judgment": "exploratory_counterfactual_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": "Uses run267B 2024 MT5 trade records to prioritize P0 ablation/replacement variants; no operating meaning.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_simple_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__weak_slice_counterfactual_triage",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "weak_slice_counterfactual_triage",
            "parent_run_id": input_probe.RUN_ID,
            "record_view": "weak_slice_counterfactual_triage",
            "tier_scope": "Tier A+B routed historical 2024 trade records",
            "kpi_scope": "trade_shape_counterfactual",
            "scoreboard_lane": "trade_shape",
            "status": "completed_counterfactual_triage_mt5_variants_pending",
            "judgment": "exploratory_counterfactual_only_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"counterfactual_rows={len(read_csv_rows(COUNTERFACTUAL_KPI_PATH))}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;mt5_rerun=pending",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Closed-trade counterfactual triage, not a new MT5 rerun and not feature ablation proof.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267C_counterfactual_script", "producer_script", PRODUCER_PATH, "Builds run267C weak-slice counterfactual triage."),
        ("stage267_run267C_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267C manifest."),
        ("stage267_run267C_counterfactual_kpi", "counterfactual_kpi", COUNTERFACTUAL_KPI_PATH, "Weak-slice counterfactual KPI by candidate."),
        ("stage267_run267C_intersection_kpi", "intersection_kpi", INTERSECTION_KPI_PATH, "Weak-slice intersection KPI by candidate."),
        ("stage267_run267C_candidate_triage_summary", "triage_summary", TRIAGE_SUMMARY_PATH, "Candidate-level counterfactual triage summary."),
        ("stage267_run267C_counterfactual_result", "review_result", RESULT_PATH, "JSON payload for run267C weak-slice counterfactual triage."),
        ("stage267_run267C_counterfactual_report", "review_report", REPORT_PATH, "User-facing run267C weak-slice counterfactual triage report."),
    )
    rows = input_probe.read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = []
    for artifact_id, artifact_type, path, notes in entries:
        new_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    replacement = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    input_probe.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def write_run_manifest(result: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "status": STATUS,
        "created_on": "2026-05-20",
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": "Common weak slices from run267B reveal whether P0 ablation/replacement variants should be MT5-tested or rejected as naive overprune.",
        "decision_use": "Prioritize the next MT5 variant materialization; cannot select a candidate, cannot start ONNX review.",
        "comparison_baseline": rel(TRADE_RECORDS_PATH),
        "control_variables": [
            "source trade records are run267B 2024 historical stress routed totals",
            "candidate pool remains the five baseline research candidates",
            "no MT5 rerun is claimed in this pass",
        ],
        "changed_variables": [
            "counterfactual removal of vol_low",
            "counterfactual removal of 2024-07",
            "counterfactual removal of Monday",
            "counterfactual removal of late session",
            "compound weak-axis removals",
        ],
        "sample_scope": "historical_2024_train_era_stress closed trades from run267B routed_total records",
        "success_criteria": "Identify which P0 axes deserve MT5 materialization without treating naive filters as final repairs.",
        "failure_criteria": "All useful-looking improvements require severe trade-count collapse or only hide a broad curve defect.",
        "invalid_conditions": "Missing run267B trade records, duplicate tier records included, or period mislabeled as OOS.",
        "stop_conditions": "If counterfactual requires over-pruning, move to feature engineering or candidate downgrade rather than calendar/threshold micro-repair.",
        "evidence_plan": [
            rel(COUNTERFACTUAL_KPI_PATH),
            rel(INTERSECTION_KPI_PATH),
            rel(TRIAGE_SUMMARY_PATH),
            rel(RESULT_PATH),
            rel(REPORT_PATH),
        ],
        "outputs": dict(result["outputs"]),
        "latest_judgment": {
            "result_subject": "run267C weak-slice counterfactual triage",
            "evidence_available": list(result["outputs"].values()),
            "evidence_missing": [
                "actual MT5 ablation/replacement reruns",
                "full feature-category ablation",
                "similar feature replacement model materialization",
                "Adapter validation",
                "ONNX parity",
            ],
            "judgment_label": "exploratory_counterfactual_only",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
        },
        "next_action": NEXT_ACTION,
    }
    write_json(RUN_MANIFEST_PATH, manifest)


def update_current_truth_docs() -> None:
    current_text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = replace_once(
        current_text,
        "- current_run(현재 실행): `run267B_stage267_extended_period_ablation_probe_v1`",
        f"- current_run(현재 실행): `{RUN_ID}`",
    )
    current_text = replace_once(
        current_text,
        "- status(상태): `stage267_run267B_historical_2024_visual_ablation_replacement_design_completed`",
        f"- status(상태): `{STATUS}`",
    )
    current_text = append_line_after_anchor(
        current_text,
        "- Stage267(267단계) historical 2024 visual ablation design(2024 시각/제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_visual_ablation_design_report.md`",
        "- Stage267(267단계) run267C weak-slice counterfactual triage(약점 구간 반사실 선별): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_weak_slice_counterfactual_triage_report.md`",
    )
    current_text = replace_once(
        current_text,
        "- next_run(다음 실행): `run267C_stage267_execute_prioritized_ablation_replacement_variants`",
        f"- next_run(다음 실행): `{RUN_ID}`",
    )
    current_text = replace_once(
        current_text,
        "- action(행동): 2024 historical stress(2024 과거 압박) MT5 chart PNG(MT5 차트 이미지) 10개를 sanity check(기초 점검)하고, 약점 기반 ablation/replacement design(제거/대체 설계) 10개를 만들었다.",
        "- action(행동): run267B(267B 실행) 2024 routed trade records(라우팅 거래 기록)로 weak-slice counterfactual triage(약점 구간 반사실 선별)를 실행했다.",
    )
    current_text = replace_once(
        current_text,
        "- effect(효과): 공통 약점인 vol_low(낮은 변동성), 2024-07(2024년 7월), Monday(월요일), late session(후반 세션)을 다음 실행 가능한 feature ablation(피처 제거), similar replacement(유사 대체), feature engineering(피처 엔지니어링) 질문으로 바꾸었다.",
        "- effect(효과): naive filter(단순 필터)로 좋아 보이는 축과 trade count collapse(거래 수 붕괴)를 일으키는 축을 분리해, 다음 MT5 variant(MT5 변형) 물질화 우선순위를 좁혔다.",
    )
    current_text = replace_once(
        current_text,
        "- next_action(다음 행동): `run267C_stage267_execute_prioritized_ablation_replacement_variants`. Effect(효과): 설계만 끝낸 상태에서 멈추지 않고, 실제 rerun(재실행)으로 어떤 후보가 덜 깨지는지 확인한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): counterfactual(반사실)로 좁힌 P0(우선순위 0) 축을 실제 MT5 rerun(MT5 재실행) 후보로 만든다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current_text)

    selection_text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection_text = replace_once(
        selection_text,
        "- stage_status(단계 상태): `run267B_historical_2024_visual_ablation_replacement_design_completed`",
        "- stage_status(단계 상태): `run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending`",
    )
    selection_text = replace_once(
        selection_text,
        "- current_run(현재 실행): `run267B_stage267_extended_period_ablation_probe_v1`",
        f"- current_run(현재 실행): `{RUN_ID}`",
    )
    selection_text = append_line_after_anchor(
        selection_text,
        "- historical_2024_visual_ablation_design(2024 시각/제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_visual_ablation_design_report.md`",
        "- run267C_counterfactual_triage(267C 반사실 선별): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_weak_slice_counterfactual_triage_report.md`",
    )
    selection_text = replace_once(
        selection_text,
        "- next_action(다음 행동): `run267C_stage267_execute_prioritized_ablation_replacement_variants`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection_text = replace_once(
        selection_text,
        "Run267B(267B 실행)는 input readiness(입력 준비), first-pass equity curve shape grading(1차 평가금 곡선 형태 판정), 2024 historical stress input materialization(2024 과거 압박 입력 산출물화), 2024 MT5 Strategy Tester execution(MT5 전략 테스터 실행), 2024 balance/time-slice review(잔액/시간 구간 검토), visual artifact sanity(시각 산출물 기초 점검), ablation/replacement design(제거/대체 설계)을 완료했다.",
        "Run267C(267C 실행)는 run267B(267B 실행)의 routed trade records(라우팅 거래 기록)로 weak-slice counterfactual triage(약점 구간 반사실 선별)를 완료했다.",
    )
    selection_text = replace_once(
        selection_text,
        "Effect(효과): 공통 약점은 vol_low(낮은 변동성), 2024-07(2024년 7월), Monday(월요일), late session(후반 세션)이고, 선택 후보(selected candidate, 선택 후보)는 계속 없다.",
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 실제 MT5 variant(MT5 변형) 물질화다.",
    )
    write_md(SELECTION_STATUS_PATH, selection_text)

    review_text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_text = replace_once(
        review_text,
        "- status(상태): `run267B_historical_2024_visual_ablation_replacement_design_completed`",
        "- status(상태): `run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending`",
    )
    review_text = replace_once(
        review_text,
        "- current_run(현재 실행): `run267B_stage267_extended_period_ablation_probe_v1`",
        f"- current_run(현재 실행): `{RUN_ID}`",
    )
    review_text = append_line_after_anchor(
        review_text,
        "- run267B_historical_2024_visual_ablation_design(267B 2024 시각/제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_visual_ablation_design_report.md`",
        "- run267C_weak_slice_counterfactual_triage(267C 약점 구간 반사실 선별): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_weak_slice_counterfactual_triage_report.md`",
    )
    review_text = replace_once(
        review_text,
        "Run267B(267B 실행)는 input readiness(입력 준비), existing MT5 report(기존 MT5 보고서)의 equity curve shape grading(평가금 곡선 형태 판정), 2024 historical stress(2024 과거 압박) 입력 물질화(materialization, 산출물화), 2024 MT5 Strategy Tester execution(MT5 전략 테스터 실행), 2024 balance/time-slice review(잔액/시간 구간 검토), visual artifact sanity(시각 산출물 기초 점검), ablation/replacement design(제거/대체 설계)을 완료했다.",
        "Run267C(267C 실행)는 run267B(267B 실행)의 2024 routed trade records(라우팅 거래 기록)로 weak-slice counterfactual triage(약점 구간 반사실 선별)를 완료했다.",
    )
    review_text = replace_once(
        review_text,
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_stage267_execute_prioritized_ablation_replacement_variants`로 넘어간다.",
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`로 넘어간다.",
    )
    write_md(REVIEW_INDEX_PATH, review_text)

    workspace_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace_text = replace_once(workspace_text, f"current_run_id: {input_probe.RUN_ID}", f"current_run_id: {RUN_ID}")
    workspace_text = replace_once(
        workspace_text,
        "Stage267(267단계) run267B(267B 실행) historical 2024 visual ablation/replacement design(2024 시각 제거/대체 설계) completed(완료).",
        "Stage267(267단계) run267C(267C 실행) weak-slice counterfactual triage(약점 구간 반사실 선별) completed(완료).",
    )
    workspace_text = replace_once(
        workspace_text,
        "Effect(효과): 2024 deal list(거래 목록), time-slice KPI(시간 구간 핵심 성과 지표), chart PNG(차트 이미지)를 다음 feature ablation(피처 제거), similar replacement(유사 대체), feature engineering(피처 엔지니어링) 실행 질문 10개로 연결했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "Effect(효과): run267B(267B 실행) trade records(거래 기록)를 이용해 naive weak-slice filter(단순 약점 구간 필터)가 후보 개선처럼 보이는지 먼저 분리했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "Next action(다음 행동)는 `run267C_stage267_execute_prioritized_ablation_replacement_variants`이다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "active_historical_2024_visual_ablation_replacement_design_completed(2024 시각 제거/대체 설계 완료 활성).",
        "active_run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending(267C 약점 구간 반사실 선별 완료 후 MT5 변형 대기 활성).",
    )
    write_md(WORKSPACE_STATE_PATH, workspace_text)


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    counterfactual_rows: Sequence[Mapping[str, Any]],
    result: Mapping[str, Any],
) -> str:
    top_rows = sorted(counterfactual_rows, key=lambda row: fnum(row.get("net_delta")), reverse=True)[:10]
    lines = [
        "# Stage267 Run267C Weak-Slice Counterfactual Triage(267단계 267C 약점 구간 반사실 선별)",
        "",
        "- action(행동): run267B(267B 실행) 2024 routed trade records(라우팅 거래 기록)에서 약한 구간을 제거하는 counterfactual(반사실) KPI(핵심 성과 지표)를 계산했다.",
        "- effect(효과): 단순히 약한 월/세션을 지우면 좋아 보이는지, 아니면 trade count collapse(거래 수 붕괴)로 착시가 생기는지 분리했다.",
        f"- counterfactual_rows(반사실 행): `{len(counterfactual_rows)}`",
        f"- intersection_rows(교차 구간 행): `{result['intersection_rows']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Candidate Triage(후보 선별)",
        "",
        "| candidate(후보) | role(역할) | baseline net(기준 순수익) | baseline PF(기준 수익 팩터) | baseline DD%(기준 손실폭%) | best counterfactual(최선 반사실) | net delta(순수익 변화) | retention(유지율) | read(판독) |",
        "| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |",
    ]
    for row in summaries:
        lines.append(
            f"| `{row.get('candidate_id')}` | `{row.get('candidate_role')}` | {cell(row.get('baseline_net_profit'))} | {cell(row.get('baseline_profit_factor'))} | {cell(row.get('baseline_dd_percent'))} | `{row.get('best_counterfactual')}` | {cell(row.get('best_net_delta'))} | {cell(row.get('best_trade_retention'))} | `{row.get('triage_label')}` |"
        )
    lines.extend(
        [
            "",
            "## Top Counterfactual Deltas(상위 반사실 변화)",
            "",
            "| candidate(후보) | intervention(개입) | kept trades(유지 거래) | net delta(순수익 변화) | DD delta(손실폭 변화) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in top_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('intervention_id')}` | {cell(row.get('kept_trade_count'))} | {cell(row.get('net_delta'))} | {cell(row.get('dd_percent_delta'))} | `{row.get('counterfactual_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 결과는 closed trade counterfactual(청산 거래 반사실)이다. Effect(효과): 실제 feature ablation(피처 제거), similar replacement(유사 대체), MT5 rerun(MT5 재실행)을 대체하지 않는다.",
            "- naive filter(단순 필터)가 좋아 보여도 바로 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)로 이어지지 않는다.",
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage267 run267C weak-slice counterfactual triage(약점 구간 반사실 선별).",
            "- evidence_available(사용 가능 근거): run267B trade records(거래 기록), counterfactual KPI(반사실 핵심 성과 지표), intersection KPI(교차 구간 핵심 성과 지표), candidate summary(후보 요약).",
            "- evidence_missing(부족 근거): actual MT5 ablation/replacement reruns(실제 MT5 제거/대체 재실행), full feature ablation(전체 피처 제거), similar feature replacement(유사 피처 대체), Adapter validation(어댑터 검증), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `exploratory_counterfactual_only`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def execute() -> dict[str, Any]:
    created_at = utc_now()
    groups = candidate_groups()
    if not groups:
        raise RuntimeError("No routed_total Tier A+B trade records found for run267B")
    counterfactual_rows = build_counterfactual_rows(groups)
    intersection_rows = build_intersection_rows(groups)
    summaries = build_candidate_summary(counterfactual_rows)
    result = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_trade_records": rel(TRADE_RECORDS_PATH),
        "source_design": rel(DESIGN_PATH),
        "candidate_count": len(groups),
        "counterfactual_rows": len(counterfactual_rows),
        "intersection_rows": len(intersection_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "outputs": {
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "counterfactual_kpi": rel(COUNTERFACTUAL_KPI_PATH),
            "intersection_kpi": rel(INTERSECTION_KPI_PATH),
            "triage_summary": rel(TRIAGE_SUMMARY_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "next_action": NEXT_ACTION,
    }
    write_csv(
        COUNTERFACTUAL_KPI_PATH,
        counterfactual_rows,
        (
            "run_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "intervention_id",
            "design_links",
            "weakness_axis",
            "weakness_bucket",
            "counterfactual_action",
            "baseline_trade_count",
            "baseline_net_profit",
            "baseline_profit_factor",
            "baseline_expectancy",
            "baseline_dd_percent",
            "kept_trade_count",
            "kept_net_profit",
            "kept_profit_factor",
            "kept_expectancy",
            "kept_dd_percent",
            "removed_trade_count",
            "removed_net_profit",
            "removed_profit_factor",
            "trade_retention",
            "net_delta",
            "pf_delta",
            "dd_percent_delta",
            "counterfactual_read",
        ),
    )
    write_csv(
        INTERSECTION_KPI_PATH,
        intersection_rows,
        (
            "run_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "intersection_id",
            "design_links",
            "baseline_trade_count",
            "baseline_net_profit",
            "intersection_trade_count",
            "intersection_net_profit",
            "intersection_profit_factor",
            "intersection_expectancy",
            "intersection_dd_percent",
            "trade_share",
            "net_share",
            "slice_read",
        ),
    )
    write_csv(
        TRIAGE_SUMMARY_PATH,
        summaries,
        (
            "run_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "baseline_net_profit",
            "baseline_profit_factor",
            "baseline_trade_count",
            "baseline_dd_percent",
            "best_counterfactual",
            "best_net_delta",
            "best_trade_retention",
            "best_dd_percent_delta",
            "triage_label",
            "p0_design_read",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_json(RESULT_PATH, result)
    write_run_manifest(result)
    write_md(REPORT_PATH, build_report(summaries, counterfactual_rows, result))
    upsert_stage_ledger()
    upsert_run_registers()
    update_current_truth_docs()
    upsert_artifacts(created_at)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "candidate_count": result["candidate_count"],
                "counterfactual_rows": result["counterfactual_rows"],
                "intersection_rows": result["intersection_rows"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
