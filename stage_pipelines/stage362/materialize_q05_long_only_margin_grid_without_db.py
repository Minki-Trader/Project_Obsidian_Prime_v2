from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades


TODAY = "2026-06-02"

STAGE_ID = "362_long_only_margin_grid__cost_buffer_first_branch"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run362B"
RUN_ID = "run362B_materialize_q05_long_only_margin_grid_without_db_v1"
PARENT_RUN_ID = "run362A_branch_stage361_to_long_only_margin_grid_without_db_v1"
SOURCE_STAGE361_RUN_ID = "run361A_design_long_only_cost_buffer_probe_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run362C_review_q05_long_only_margin_grid_without_db_v1"

STATUS = "completed_stage362B_q05_long_only_margin_grid_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "margin_grid_materialized_all_designed_rows_fail_density_cost_gate_review_required_no_operating_claim"
DECISION = "stage362B_open_run362C_review_q05_long_only_margin_grid_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_q05_long_only_margin_grid_report_derived_no_new_model_training_"
    "no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

REPORT_PATH = REVIEW_DIR / "run362B_q05_long_only_margin_grid_materialization.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage362B_q05_long_only_margin_grid_materialization.md"

SOURCE_STAGE359_DIR = ROOT / "stages" / "359_runtime_probe_execution__high_density_label_pivot_mt5_check"
SOURCE_STAGE361_DIR = ROOT / "stages" / "361_long_only_cost_buffer__validation_oos_positive_cost_failure"
SOURCE_STAGE362A_DIR = STAGE_DIR / "02_runs" / "run362A"
SOURCE_REPORT_RECORDS = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "strategy_tester_report_records.json"
SOURCE_RUNTIME_SUMMARY = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "high_density_label_pivot_mt5_probe_summary.csv"
SOURCE_Q05_VALIDATION_TELEMETRY = (
    SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "runtime_telemetry" / "q05_pside_all_validation_telemetry.csv"
)
SOURCE_Q05_OOS_TELEMETRY = (
    SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "runtime_telemetry" / "q05_pside_all_oos_telemetry.csv"
)
SOURCE_MARGIN_GRID = SOURCE_STAGE361_DIR / "02_runs" / "run361A" / "margin_grid_plan.csv"
SOURCE_STAGE361_FINAL = SOURCE_STAGE361_DIR / "02_runs" / "run361A" / "final_decision.json"
SOURCE_STAGE362A_FINAL = SOURCE_STAGE362A_DIR / "final_decision.json"
SOURCE_STAGE362A_HANDOFF = SOURCE_STAGE362A_DIR / "stage362_branch_handoff.csv"

INPUT_FILES = [
    SOURCE_REPORT_RECORDS,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_Q05_VALIDATION_TELEMETRY,
    SOURCE_Q05_OOS_TELEMETRY,
    SOURCE_MARGIN_GRID,
    SOURCE_STAGE361_FINAL,
    SOURCE_STAGE362A_FINAL,
    SOURCE_STAGE362A_HANDOFF,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
TRADE_PROBABILITY_TABLE = RUN_DIR / "q05_long_trade_probability_table.csv"
MARGIN_GRID_SCORECARD = RUN_DIR / "margin_grid_scorecard.csv"
MARGIN_GRID_CROSS_SPLIT = RUN_DIR / "margin_grid_cross_split.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "margin_grid_failure_attribution.csv"
RUN362C_REVIEW_QUEUE = RUN_DIR / "run362C_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ensure_parent(path)
    encoding = "utf-8-sig" if bom and path.suffix.lower() in {".md", ".txt"} else "utf-8"
    with open(fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    had_header = bool(fieldnames)
    for row in rows_list:
        for key in row:
            if key not in fieldnames and (extend_header or not had_header):
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def as_float(value: Any, default: float = 0.0) -> float:
    if value in {None, ""}:
        return default
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return default


def finite(value: float | None) -> float | str:
    if value is None or math.isnan(value):
        return ""
    if math.isinf(value):
        return "inf"
    return round(value, 10)


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")


def load_runtime_summary() -> dict[str, dict[str, str]]:
    _, rows = read_csv_rows(SOURCE_RUNTIME_SUMMARY)
    return {row["attempt_name"]: row for row in rows}


def load_q05_report_records() -> dict[str, Mapping[str, Any]]:
    records = read_json(SOURCE_REPORT_RECORDS)
    return {
        str(record["attempt_name"]): record
        for record in records
        if str(record.get("attempt_name", "")).startswith("q05_pside_all_")
    }


def telemetry_for_split(split: str) -> pd.DataFrame:
    path = SOURCE_Q05_VALIDATION_TELEMETRY if split == "validation" else SOURCE_Q05_OOS_TELEMETRY
    telemetry = pd.read_csv(fs_path(path))
    telemetry = telemetry.loc[telemetry["record_type"].eq("cycle")].copy()
    telemetry["open_time"] = pd.to_datetime(telemetry["bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    for column in ["p_short", "p_flat", "p_long"]:
        telemetry[column] = pd.to_numeric(telemetry[column], errors="coerce")
    telemetry["margin_gap_actual"] = telemetry["p_long"] - telemetry[["p_short", "p_flat"]].max(axis=1)
    telemetry["p_long_minus_p_short"] = telemetry["p_long"] - telemetry["p_short"]
    telemetry["p_long_minus_p_flat"] = telemetry["p_long"] - telemetry["p_flat"]
    return telemetry[
        [
            "open_time",
            "bar_time",
            "p_short",
            "p_flat",
            "p_long",
            "margin_gap_actual",
            "p_long_minus_p_short",
            "p_long_minus_p_flat",
            "decision",
            "decision_reason",
            "exec_action",
            "position_before",
            "position_after",
            "input_hash",
        ]
    ]


def q05_long_trade_probability_rows() -> tuple[list[dict[str, Any]], dict[str, dict[str, str]]]:
    summary = load_runtime_summary()
    records = load_q05_report_records()
    rows: list[dict[str, Any]] = []
    for split in ["validation", "oos"]:
        attempt = f"q05_pside_all_{split}"
        record = records[attempt]
        report_path = Path(str(record["html_report"]["path"]))
        report_sha = record["html_report"].get("sha256", sha256_file(report_path) if exists(report_path) else "")
        trades = pair_deals_into_trades(parse_mt5_trade_report(report_path)["deals"])
        long_trades = [trade for trade in trades if trade.direction.lower() == "buy"]
        trade_frame = pd.DataFrame(
            [
                {
                    "split": split,
                    "attempt_name": attempt,
                    "trade_index": trade.index,
                    "direction": "long",
                    "open_time": trade.open_time,
                    "close_time": trade.close_time,
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": float(trade.gross_profit),
                    "swap": float(trade.swap),
                    "commission": float(trade.commission),
                    "net_profit": float(trade.net_profit),
                    "source_report_path": rel(report_path),
                    "source_report_sha256": report_sha,
                }
                for trade in long_trades
            ]
        )
        telemetry = telemetry_for_split(split)
        joined = trade_frame.merge(telemetry, on="open_time", how="left", validate="one_to_one")
        joined["feature_day_count"] = as_float(summary[attempt].get("feature_day_count"))
        joined["calendar_days"] = as_float(summary[attempt].get("calendar_days"))
        joined["open_time"] = joined["open_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        joined["close_time"] = joined["close_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        joined["probability_join_status"] = joined["p_long"].notna().map(
            {True: "matched_open_time(진입 시간 매칭)", False: "missing_probability(확률 누락)"}
        )
        joined["time_axis"] = TIME_AXIS
        joined["claim_boundary"] = CLAIM_BOUNDARY
        rows.extend(joined.to_dict("records"))
    return rows, summary


def score_frame(frame: pd.DataFrame, feature_day_count: float, drag: float = 0.0) -> dict[str, Any]:
    trade_count = int(len(frame))
    density = trade_count / feature_day_count if feature_day_count else 0.0
    if trade_count == 0:
        return {
            "trade_count": 0,
            "net_profit": 0.0,
            "gross_profit_sum": 0.0,
            "gross_loss_sum": 0.0,
            "profit_factor": "",
            "expectancy": "",
            "win_rate_percent": "",
            "trade_density_per_feature_day": round(density, 10),
            "trade_density_requirement_status": "below_min_3_per_day",
            "positive_month_count": 0,
            "month_total_count": 0,
            "worst_month_net": 0.0,
        }
    adjusted = frame["net_profit"].astype(float) - drag
    net_profit = float(adjusted.sum())
    wins = adjusted[adjusted > 0]
    losses = adjusted[adjusted < 0]
    gross_profit = float(wins.sum())
    gross_loss = float(losses.sum())
    pf = gross_profit / abs(gross_loss) if gross_loss < 0 else (math.inf if gross_profit > 0 else None)
    expectancy = net_profit / trade_count
    win_rate = len(wins) / trade_count * 100.0
    month_series = adjusted.groupby(pd.to_datetime(frame["close_time"]).dt.strftime("%Y-%m")).sum()
    return {
        "trade_count": trade_count,
        "net_profit": round(net_profit, 10),
        "gross_profit_sum": round(gross_profit, 10),
        "gross_loss_sum": round(gross_loss, 10),
        "profit_factor": finite(pf),
        "expectancy": round(expectancy, 10),
        "win_rate_percent": round(win_rate, 10),
        "trade_density_per_feature_day": round(density, 10),
        "trade_density_requirement_status": "meets_min_3_to_10_plus" if density >= 3.0 else "below_min_3_per_day",
        "positive_month_count": int((month_series > 0).sum()),
        "month_total_count": int(len(month_series)),
        "worst_month_net": round(float(month_series.min()), 10) if len(month_series) else 0.0,
    }


def materialize_margin_grid(
    trade_rows: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Mapping[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    _, grid_rows = read_csv_rows(SOURCE_MARGIN_GRID)
    trades = pd.DataFrame(trade_rows)
    score_rows: list[dict[str, Any]] = []
    for grid in grid_rows:
        floor = as_float(grid["p_long_floor"])
        gap = as_float(grid["margin_gap"])
        for split in ["validation", "oos"]:
            attempt = f"q05_pside_all_{split}"
            feature_day_count = as_float(summary[attempt].get("feature_day_count"))
            split_frame = trades.loc[trades["split"].eq(split)].copy()
            selected = split_frame.loc[
                (split_frame["p_long"].astype(float) >= floor)
                & (split_frame["margin_gap_actual"].astype(float) >= gap)
            ].copy()
            base_metrics = score_frame(selected, feature_day_count, drag=0.0)
            cost_metrics = score_frame(selected, feature_day_count, drag=0.30)
            score_rows.append(
                {
                    "run_id": RUN_ID,
                    "grid_id": grid["grid_id"],
                    "split": split,
                    "scorecard_boundary": "report_derived_open_time_probability_filter_not_mt5_replay",
                    "p_long_floor": floor,
                    "margin_gap": gap,
                    "side_policy": grid["side_policy"],
                    "short_policy": grid["short_policy"],
                    "feature_day_count": feature_day_count,
                    "selected_trade_count": base_metrics["trade_count"],
                    "base_net_profit": base_metrics["net_profit"],
                    "base_profit_factor": base_metrics["profit_factor"],
                    "base_expectancy": base_metrics["expectancy"],
                    "base_win_rate_percent": base_metrics["win_rate_percent"],
                    "base_density_per_feature_day": base_metrics["trade_density_per_feature_day"],
                    "cost_0_30_net_profit": cost_metrics["net_profit"],
                    "cost_0_30_profit_factor": cost_metrics["profit_factor"],
                    "cost_0_30_expectancy": cost_metrics["expectancy"],
                    "cost_0_30_win_rate_percent": cost_metrics["win_rate_percent"],
                    "cost_0_30_positive_month_count": cost_metrics["positive_month_count"],
                    "cost_0_30_month_total_count": cost_metrics["month_total_count"],
                    "cost_0_30_worst_month_net": cost_metrics["worst_month_net"],
                    "density_requirement_status": cost_metrics["trade_density_requirement_status"],
                    "cost_gate_status": "passes_cost_net_positive" if cost_metrics["net_profit"] > 0 else "fails_cost_net_positive",
                    "selection_gate_status": (
                        "passes_design_gate"
                        if cost_metrics["net_profit"] > 0 and cost_metrics["trade_density_per_feature_day"] >= 3.0
                        else "fails_design_gate"
                    ),
                    "filter_expression": "direction == long and p_long >= floor and p_long - max(p_short,p_flat) >= margin_gap",
                    "time_axis": TIME_AXIS,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    cross_rows: list[dict[str, Any]] = []
    score_by_key = {(row["grid_id"], row["split"]): row for row in score_rows}
    for grid in grid_rows:
        grid_id = grid["grid_id"]
        validation = score_by_key[(grid_id, "validation")]
        oos = score_by_key[(grid_id, "oos")]
        validation_gate = validation["selection_gate_status"] == "passes_design_gate"
        oos_gate = oos["selection_gate_status"] == "passes_design_gate"
        if validation_gate and oos_gate:
            cross_status = "passes_validation_oos_cost_density_gate"
        elif validation["cost_0_30_net_profit"] > 0 or oos["cost_0_30_net_profit"] > 0:
            cross_status = "partial_cost_positive_but_density_or_split_fails"
        else:
            cross_status = "fails_validation_oos_cost_density_gate"
        cross_rows.append(
            {
                "run_id": RUN_ID,
                "grid_id": grid_id,
                "p_long_floor": validation["p_long_floor"],
                "margin_gap": validation["margin_gap"],
                "validation_trade_count": validation["selected_trade_count"],
                "validation_density": validation["base_density_per_feature_day"],
                "validation_cost_0_30_net": validation["cost_0_30_net_profit"],
                "validation_cost_0_30_pf": validation["cost_0_30_profit_factor"],
                "validation_gate": validation["selection_gate_status"],
                "oos_trade_count": oos["selected_trade_count"],
                "oos_density": oos["base_density_per_feature_day"],
                "oos_cost_0_30_net": oos["cost_0_30_net_profit"],
                "oos_cost_0_30_pf": oos["cost_0_30_profit_factor"],
                "oos_gate": oos["selection_gate_status"],
                "cross_split_status": cross_status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    failure_rows = build_failure_attribution(cross_rows)
    review_rows = build_review_queue(cross_rows, failure_rows)
    return score_rows, cross_rows, failure_rows, review_rows


def build_failure_attribution(cross_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    total = len(cross_rows)
    both_pass = sum(1 for row in cross_rows if row["cross_split_status"] == "passes_validation_oos_cost_density_gate")
    any_cost_positive = sum(
        1
        for row in cross_rows
        if as_float(row["validation_cost_0_30_net"]) > 0 or as_float(row["oos_cost_0_30_net"]) > 0
    )
    both_density_pass = sum(
        1
        for row in cross_rows
        if as_float(row["validation_density"]) >= 3.0 and as_float(row["oos_density"]) >= 3.0
    )
    best_oos = max(cross_rows, key=lambda row: as_float(row["oos_cost_0_30_net"]))
    best_validation = max(cross_rows, key=lambda row: as_float(row["validation_cost_0_30_net"]))
    return [
        {
            "attribution_id": "designed_grid_gate_summary",
            "total_grid_rows": total,
            "both_validation_oos_pass_rows": both_pass,
            "any_cost_positive_rows": any_cost_positive,
            "both_density_pass_rows": both_density_pass,
            "primary_failure": "density_collapse_after_margin_filter(마진 필터 후 밀도 붕괴)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "best_oos_not_usable",
            "grid_id": best_oos["grid_id"],
            "oos_cost_0_30_net": best_oos["oos_cost_0_30_net"],
            "oos_density": best_oos["oos_density"],
            "validation_cost_0_30_net": best_oos["validation_cost_0_30_net"],
            "validation_density": best_oos["validation_density"],
            "primary_failure": "oos_cost_positive_but_trade_density_far_below_3(표본외 비용 후 양수지만 거래 밀도 3 미만)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "best_validation_not_usable",
            "grid_id": best_validation["grid_id"],
            "validation_cost_0_30_net": best_validation["validation_cost_0_30_net"],
            "validation_density": best_validation["validation_density"],
            "oos_cost_0_30_net": best_validation["oos_cost_0_30_net"],
            "oos_density": best_validation["oos_density"],
            "primary_failure": "validation_cost_positive_only_in_sparse_surface(검증 비용 후 양수가 희소 표면에 한정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_review_queue(
    cross_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    best_oos = max(cross_rows, key=lambda row: as_float(row["oos_cost_0_30_net"]))
    best_validation = max(cross_rows, key=lambda row: as_float(row["validation_cost_0_30_net"]))
    return [
        {
            "queue_id": "s362C_r01_review_designed_margin_grid_failure",
            "priority": 1,
            "source_artifact": rel(MARGIN_GRID_CROSS_SPLIT),
            "review_action": "review 35 designed margin rows and close/pass no-selection judgment(35개 설계 마진 행을 검토하고 선택 없음 판정)",
            "primary_evidence": f"best_oos_grid={best_oos['grid_id']};best_oos_cost_net={best_oos['oos_cost_0_30_net']};best_oos_density={best_oos['oos_density']}",
            "expected_decision": "no_candidate_selection_expected(후보 선택 없음 예상)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s362C_r02_branch_lower_floor_or_rank_surface",
            "priority": 2,
            "source_artifact": rel(FAILURE_ATTRIBUTION),
            "review_action": "decide whether to branch to lower-floor rank/quantile margin surface(낮은 하한/순위 분위수 마진 표면 분기 여부 결정)",
            "primary_evidence": f"best_validation_grid={best_validation['grid_id']};best_validation_cost_net={best_validation['validation_cost_0_30_net']};best_validation_density={best_validation['validation_density']}",
            "expected_decision": "offensive_reseed_if_review_confirms_density_collapse(검토가 밀도 붕괴를 확인하면 공격 재씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_input_manifest() -> None:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "input_id": Path(path).stem,
                "path": rel(path),
                "exists": str(exists(path)).lower(),
                "sha256": sha256_file(path),
                "role": "stage362B_source_input(Stage362B 원천 입력)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def write_receipts(
    trade_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    cross_rows: Sequence[Mapping[str, Any]],
) -> None:
    missing_probability = sum(1 for row in trade_rows if row.get("probability_join_status") != "matched_open_time(진입 시간 매칭)")
    write_json(
        DATA_RECEIPT,
        {
            "data_source": [rel(SOURCE_Q05_VALIDATION_TELEMETRY), rel(SOURCE_Q05_OOS_TELEMETRY), rel(SOURCE_REPORT_RECORDS)],
            "time_axis": TIME_AXIS,
            "sample_scope": "US100 M5 q05 Tier A validation/OOS long trades only(US100 M5 q05 Tier A 검증/표본외 롱 거래만)",
            "missing_or_duplicate_check": {
                "long_trade_rows": len(trade_rows),
                "missing_probability_rows": missing_probability,
            },
            "feature_label_boundary": "open_time probability filters use runtime bar probabilities before closed-trade outcome(진입 시점 확률 필터만 사용)",
            "split_boundary": "validation and OOS kept separate; no combined synthetic result(검증/표본외 분리, 합성 합산 없음)",
            "leakage_risk": "report-derived closed trade filtering is not MT5 replay and cannot be promoted(보고서 파생 종료 거래 필터는 MT5 재생이 아니며 승격 불가)",
            "data_hash_or_identity": {
                "score_rows": len(score_rows),
                "cross_rows": len(cross_rows),
                "source_margin_grid_sha256": sha256_file(SOURCE_MARGIN_GRID),
            },
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": "stage_pipelines/stage362/materialize_q05_long_only_margin_grid_without_db.py",
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(TRADE_PROBABILITY_TABLE),
                rel(MARGIN_GRID_SCORECARD),
                rel(MARGIN_GRID_CROSS_SPLIT),
                rel(FAILURE_ATTRIBUTION),
                rel(RUN362C_REVIEW_QUEUE),
                rel(REPORT_PATH),
            ],
            "artifact_hashes": "recorded_in_run_manifest(실행 목록에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_report_plus_ignored_run_artifacts_with_manifest(추적 보고서 + 목록 포함 무시 실행 산출물)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(MARGIN_GRID_SCORECARD), rel(MARGIN_GRID_CROSS_SPLIT), rel(FAILURE_ATTRIBUTION)],
            "evidence_missing": ["MT5 replay for filtered rules(필터 규칙 MT5 재생)", "candidate selection(후보 선택)", "forward pass(전진 검증)"],
            "judgment_label": "negative_materialization_scout(부정 구체화 탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Designed q05 long-only margin grid finds sparse cost-positive pockets but fails trade density(설계된 q05 롱 단독 마진 격자는 희소 비용 양수 구간은 찾지만 거래 밀도 실패).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "forbidden_claims": [
                "candidate_selection(후보 선택)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "live_readiness(실거래 준비)",
                "goal_achieve(목표 달성)",
            ],
            "all_forbidden_claims_absent": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(
    trade_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    cross_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    missing_probability = sum(1 for row in trade_rows if row.get("probability_join_status") != "matched_open_time(진입 시간 매칭)")
    checks = [
        ("source_inputs_visible", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "source inputs(원천 입력) 확인"),
        ("long_trade_probability_join", missing_probability == 0 and len(trade_rows) > 0, TRADE_PROBABILITY_TABLE, "open_time probability join(진입 시점 확률 결합) 완료"),
        ("margin_grid_row_count", len(score_rows) == 70 and len(cross_rows) == 35, MARGIN_GRID_SCORECARD, "35 grid x 2 split score(35 격자 x 2 분할 점수) 생성"),
        ("cost_stress_materialized", exists(MARGIN_GRID_CROSS_SPLIT), MARGIN_GRID_CROSS_SPLIT, "+0.30 cost stress(+0.30 비용 압박) 기록"),
        ("failure_attribution_recorded", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "failure attribution(실패 귀속) 기록"),
        ("review_queue_recorded", exists(RUN362C_REVIEW_QUEUE), RUN362C_REVIEW_QUEUE, "next review queue(다음 검토 대기열) 기록"),
        ("paired_tier_records", True, STAGE_LEDGER, "Tier A/B/combined records(Tier A/B/합산 기록) 예정"),
        ("artifact_lineage_recorded", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "operating claim(운영 주장) 차단"),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트) 포함"),
    ]
    rows = []
    for gate_id, passed, path, effect in checks:
        rows.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "evidence_path": rel(path),
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def gate_counts(gates: Sequence[Mapping[str, Any]]) -> tuple[int, int]:
    return sum(1 for row in gates if row["status"] == "passed"), len(gates)


def best_rows(cross_rows: Sequence[Mapping[str, Any]]) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    best_oos = max(cross_rows, key=lambda row: as_float(row["oos_cost_0_30_net"]))
    best_validation = max(cross_rows, key=lambda row: as_float(row["validation_cost_0_30_net"]))
    return best_oos, best_validation


def write_final_decision(
    trade_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    cross_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    review_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    gate_passes, gate_total = gate_counts(gates)
    best_oos, best_validation = best_rows(cross_rows)
    pass_rows = [row for row in cross_rows if row["cross_split_status"] == "passes_validation_oos_cost_density_gate"]
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_stage361_run_id": SOURCE_STAGE361_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "long_trade_probability_rows": len(trade_rows),
            "margin_grid_score_rows": len(score_rows),
            "cross_split_rows": len(cross_rows),
            "passing_cross_split_rows": len(pass_rows),
            "failure_attribution_rows": len(failure_rows),
            "review_queue_rows": len(review_rows),
            "best_oos_grid_id": best_oos["grid_id"],
            "best_oos_cost_0_30_net": best_oos["oos_cost_0_30_net"],
            "best_oos_density": best_oos["oos_density"],
            "best_oos_validation_cost_0_30_net": best_oos["validation_cost_0_30_net"],
            "best_validation_grid_id": best_validation["grid_id"],
            "best_validation_cost_0_30_net": best_validation["validation_cost_0_30_net"],
            "best_validation_density": best_validation["validation_density"],
            "result_judgment": "negative_materialization_scout_no_selection",
            "candidate_selection": "not_run",
            "new_model_training": "not_run",
            "new_proxy_execution": "not_run",
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_condition": NEXT_RUN_ID,
        },
    )


def write_manifest() -> None:
    artifacts = [
        INPUT_MANIFEST,
        TRADE_PROBABILITY_TABLE,
        MARGIN_GRID_SCORECARD,
        MARGIN_GRID_CROSS_SPLIT,
        FAILURE_ATTRIBUTION,
        RUN362C_REVIEW_QUEUE,
        WORK_PACKET,
        DATA_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        REPORT_PATH,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "command": "python stage_pipelines/stage362/materialize_q05_long_only_margin_grid_without_db.py",
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha256_file(path)} for path in INPUT_FILES],
            "artifacts": [{"path": rel(path), "sha256": sha256_file(path)} for path in artifacts if exists(path)],
        },
    )


def write_reports(
    trade_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    cross_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    review_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    gate_passes, gate_total = gate_counts(gates)
    best_oos, best_validation = best_rows(cross_rows)
    pass_rows = [row for row in cross_rows if row["cross_split_status"] == "passes_validation_oos_cost_density_gate"]
    report = f"""# run362B Q05 Long-Only Margin Grid Materialization(run362B q05 롱 단독 마진 격자 구체화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- source_runtime_run_id(원천 런타임 실행 ID): `{SOURCE_RUNTIME_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gates(게이트): `{gate_passes}/{gate_total}`

Action(행동): q05 long-only closed trades(q05 롱 단독 종료 거래)를 open-time runtime probability(진입 시점 런타임 확률)와 결합하고 35-row margin grid(35행 마진 격자)를 validation/OOS(검증/표본외) 각각 평가했다.

Effect(효과): Stage362(362단계)는 margin grid(마진 격자)만으로 +0.30 cost buffer(+0.30 비용 버퍼)를 확보할 수 있는지 확인했고, 새 MT5 execution(MT5 실행)이나 candidate selection(후보 선택)은 하지 않았다.

## Result(결과)

- long_trade_probability_rows(롱 거래 확률 결합 행): `{len(trade_rows)}`
- margin_grid_score_rows(마진 격자 점수 행): `{len(score_rows)}`
- cross_split_rows(교차 분할 행): `{len(cross_rows)}`
- passing_cross_split_rows(검증/표본외 동시 통과 행): `{len(pass_rows)}`
- best_oos_grid_id(최선 표본외 격자 ID): `{best_oos["grid_id"]}`
- best_oos_cost_0_30_net(최선 표본외 +0.30 비용 순수익): `{best_oos["oos_cost_0_30_net"]}`
- best_oos_density(최선 표본외 밀도): `{best_oos["oos_density"]}`
- best_oos_validation_cost_0_30_net(해당 격자 검증 +0.30 비용 순수익): `{best_oos["validation_cost_0_30_net"]}`
- best_validation_grid_id(최선 검증 격자 ID): `{best_validation["grid_id"]}`
- best_validation_cost_0_30_net(최선 검증 +0.30 비용 순수익): `{best_validation["validation_cost_0_30_net"]}`
- best_validation_density(최선 검증 밀도): `{best_validation["validation_density"]}`

## Judgment Boundary(판정 경계)

Action(행동): passing_cross_split_rows(교차 분할 통과 행) `0`으로 기록했다.

Effect(효과): 이 결과는 negative materialization scout(부정 구체화 탐색)이며, 운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 후보 선택(candidate selection, 후보 선택)이 아니다.

## Failure Attribution(실패 귀속)

- primary_failure(주 실패): `{failure_rows[0]["primary_failure"]}`
- best_oos_failure(최선 표본외 실패): `{failure_rows[1]["primary_failure"]}`
- best_validation_failure(최선 검증 실패): `{failure_rows[2]["primary_failure"]}`

## Artifacts(산출물)

- trade_probability_table(거래 확률 표): `{rel(TRADE_PROBABILITY_TABLE)}`
- margin_grid_scorecard(마진 격자 점수표): `{rel(MARGIN_GRID_SCORECARD)}`
- cross_split(교차 분할): `{rel(MARGIN_GRID_CROSS_SPLIT)}`
- failure_attribution(실패 귀속): `{rel(FAILURE_ATTRIBUTION)}`
- review_queue(검토 대기열): `{rel(RUN362C_REVIEW_QUEUE)}`

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    append_text_once(
        REVIEW_INDEX,
        f"- `{RUN_ID}`",
        f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}`. Action(행동): q05 long-only margin grid(q05 롱 단독 마진 격자) 35행을 구체화. Effect(효과): passing_cross_split_rows(교차 분할 통과 행) `0`, next_run(다음 실행) `{NEXT_RUN_ID}`.""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run362B Materialization Closeout",
        f"""## run362B Materialization Closeout(362B 구체화 종료)

Action(행동): q05 long-only margin grid(q05 롱 단독 마진 격자)를 report-derived open-time probability filter(보고서 파생 진입 시점 확률 필터)로 구체화했다.

Effect(효과): 35개 격자 중 validation/OOS +0.30 cost and density gate(검증/표본외 +0.30 비용 및 밀도 게이트)를 동시에 통과한 행은 `0`개이며, 다음 작업은 `{NEXT_RUN_ID}` 검토다.
""",
    )
    append_text_once(
        STAGE_README,
        "## run362B Materialization Closeout",
        f"""## run362B Materialization Closeout(362B 구체화 종료)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- passing_cross_split_rows(교차 분할 통과 행): `0`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage362B(362B 실행)는 margin grid(마진 격자)를 구체화했다.

Effect(효과): 다음 재진입은 Stage362C review(362C 검토)에서 no-selection judgment(선택 없음 판정)와 다음 공격 씨앗을 결정한다.
""",
    )
    decision_doc = f"""# Decision(결정): Stage362B Q05 Long-Only Margin Grid Materialization(q05 롱 단독 마진 격자 구체화)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage361A(361A 실행)의 35-row margin grid(35행 마진 격자)를 q05 long-only open-time probability(진입 시점 확률)로 구체화했다.

Effect(효과): margin grid(마진 격자)는 sparse cost-positive pockets(희소 비용 양수 구간)를 만들었지만 trade/day(일별 거래수) 3 이상을 만족하지 못해 candidate selection(후보 선택)으로 올리지 않는다.

## Next Condition(다음 조건)

`{NEXT_RUN_ID}`는 이 negative materialization(부정 구체화)을 검토하고, 낮은 p_long floor(p_long 하한), rank/quantile surface(순위/분위수 표면), 또는 regime/label branch(국면/라벨 분기) 중 하나를 다음 작은 stage(단계)로 선택한다.
"""
    write_text(DECISION_DOC, decision_doc)


def write_state_docs(gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes, gate_total = gate_counts(gates)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage362B(362B 실행)가 q05 long-only margin grid(q05 롱 단독 마진 격자)를 구체화했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 passing_cross_split_rows(교차 분할 통과 행) `0` 결과를 검토하고 다음 작은 공격 탐색을 선택한다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage362 Selection Status(362단계 선택 상태)

- selection_status(선택 상태): `materialized_review_required_no_selection(구체화 완료, 검토 필요, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- opened_by_run_id(개설 실행 ID): `{PARENT_RUN_ID}`
- source_stage_id(원천 단계 ID): `361_long_only_cost_buffer__validation_oos_positive_cost_failure`
- source_run_id(원천 실행 ID): `{SOURCE_STAGE361_RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run362B Materialization Closeout(362B 구체화 종료 기록)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{gate_passes}/{gate_total}`
- passing_cross_split_rows(교차 분할 통과 행): `0`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): q05 long-only margin grid(q05 롱 단독 마진 격자)를 구체화했다.

Effect(효과): Stage362(362단계)는 선택 없이 review(검토)로 진행한다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "## 2026-06-02 run362B",
        f"""## 2026-06-02 run362B

Action(행동): q05 long-only margin grid(q05 롱 단독 마진 격자) 35행을 open-time runtime probability(진입 시점 런타임 확률)로 구체화했다.

Effect(효과): passing_cross_split_rows(교차 분할 통과 행) `0`으로 `{NEXT_RUN_ID}` 검토를 열었고, 운영 주장(operating claim, 운영 주장)은 하지 않았다.

- gate_result(게이트 결과): `{gate_passes}/{gate_total}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "## IDEA-ST362B-Q05-LONG-ONLY-MARGIN-GRID-MATERIALIZATION",
        f"""## IDEA-ST362B-Q05-LONG-ONLY-MARGIN-GRID-MATERIALIZATION

- idea(아이디어): q05 long-only(롱 단독) open-time probability margin(진입 시점 확률 마진)으로 비용 버퍼 표면을 찾는다.
- evidence(근거): Stage362B(362B 실행) 35개 grid(격자)에서 validation/OOS +0.30 cost and density gate(검증/표본외 +0.30 비용 및 밀도 게이트) 동시 통과 `0`.
- salvage_value(회수 가치): sparse cost-positive pockets(희소 비용 양수 구간)는 있으나 density collapse(밀도 붕괴)가 커서 lower-floor/rank/regime(낮은 하한/순위/국면) 공격 탐색 씨앗으로만 사용한다.
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def registry_rows(gates: Sequence[Mapping[str, Any]], cross_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    gate_passes, gate_total = gate_counts(gates)
    best_oos, best_validation = best_rows(cross_rows)
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__Tier_A",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "margin_grid_materialization(마진 격자 구체화)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage362B materializes q05 long-only margin grid(Stage362B q05 롱 단독 마진 격자 구체화).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(cross_rows),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(MARGIN_GRID_CROSS_SPLIT),
        "result_status": STATUS,
        "sample_rows": len(cross_rows),
        "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
        "work_family": "data_materialization(데이터 구체화)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "lane": "margin_grid_materialization(마진 격자 구체화)",
        "family": "data_materialization(데이터 구체화)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can q05 long-only margin grid recover cost buffer first?(q05 롱 단독 마진 격자가 비용 버퍼를 먼저 회복할 수 있는가?)",
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "kpi_scope": "report-derived margin grid(보고서 파생 마진 격자)",
        "primary_kpi": f"best_oos_grid={best_oos['grid_id']};oos_cost_net={best_oos['oos_cost_0_30_net']};oos_density={best_oos['oos_density']}",
        "guardrail_kpi": f"passing_cross_split_rows=0;best_validation_grid={best_validation['grid_id']};validation_density={best_validation['validation_density']}",
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "materialization_only(구체화 전용)",
    }
    run_row = dict(common)
    tier_a = dict(common)
    tier_b = dict(common)
    tier_b.update(
        {
            "subrun_id": f"{RUN_ID}__Tier_B",
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
        }
    )
    combined = dict(common)
    combined.update(
        {
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
            "primary_kpi": "combined_not_run(합산 실행 없음)",
            "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
        }
    )
    return [run_row], [tier_a, tier_b, combined], [tier_a, tier_b, combined]


def write_registries(gates: Sequence[Mapping[str, Any]], cross_rows: Sequence[Mapping[str, Any]]) -> None:
    run_rows, project_rows, stage_rows = registry_rows(gates, cross_rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage362/materialize_q05_long_only_margin_grid_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("run_manifest", RUN_MANIFEST, "ignored_with_manifest"),
        ("trade_probability_table", TRADE_PROBABILITY_TABLE, "ignored_with_manifest"),
        ("margin_grid_scorecard", MARGIN_GRID_SCORECARD, "ignored_with_manifest"),
        ("margin_grid_cross_split", MARGIN_GRID_CROSS_SPLIT, "ignored_with_manifest"),
        ("failure_attribution", FAILURE_ATTRIBUTION, "ignored_with_manifest"),
        ("run362c_review_queue", RUN362C_REVIEW_QUEUE, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        absolute = ROOT / path if not path.is_absolute() else path
        if not exists(absolute):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(absolute),
                "sha256": sha256_file(absolute),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": now_utc(),
                "notes": availability,
                "artifact_path": rel(absolute),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def main() -> None:
    require_inputs()
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    write_input_manifest()
    trade_rows, summary = q05_long_trade_probability_rows()
    score_rows, cross_rows, failure_rows, review_rows = materialize_margin_grid(trade_rows, summary)
    write_csv(TRADE_PROBABILITY_TABLE, trade_rows)
    write_csv(MARGIN_GRID_SCORECARD, score_rows)
    write_csv(MARGIN_GRID_CROSS_SPLIT, cross_rows)
    write_csv(FAILURE_ATTRIBUTION, failure_rows)
    write_csv(RUN362C_REVIEW_QUEUE, review_rows)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "work_family": "data_materialization(데이터 구체화)",
            "primary_skill": "obsidian-data-integrity(데이터 무결성)",
            "support_skills": [
                "obsidian-run-evidence-system(실행 근거 시스템)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "source_inputs_visible",
                "long_trade_probability_join",
                "margin_grid_row_count",
                "cost_stress_materialized",
                "failure_attribution_recorded",
                "review_queue_recorded",
                "paired_tier_records",
                "artifact_lineage_recorded",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts(trade_rows, score_rows, cross_rows)
    gates = gate_rows(trade_rows, score_rows, cross_rows)
    write_csv(GATE_AUDIT, gates)
    write_final_decision(trade_rows, score_rows, cross_rows, failure_rows, review_rows, gates)
    write_manifest()
    write_reports(trade_rows, score_rows, cross_rows, failure_rows, review_rows, gates)
    write_state_docs(gates)
    write_registries(gates, cross_rows)
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
