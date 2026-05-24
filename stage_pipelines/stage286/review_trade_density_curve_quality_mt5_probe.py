from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from stage_pipelines.stage280.validate_directional_mapping_stability import (  # noqa: E402
    attribution_rows,
    drawdown_stats,
    quality_summary,
    safe_float,
    trade_frame,
)


STAGE286_ID = "286_onnx_candidate_campaign__trade_density_curve_quality_rebuild"
STAGE287_ID = "287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild"
RUN_ID = "run286C_review_trade_density_curve_quality_mt5_probe_v1"
SOURCE_RUN_ID = "run286B_trade_density_curve_quality_mt5_probe_v1"
STATUS = "completed_trade_density_curve_quality_review_no_candidate_stage287_opened"
JUDGMENT = "density_scale_found_but_curve_pockets_fail_no_candidate"
NEXT_ACTION = "run287A_design_density_scale_curve_pocket_rebuild_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE286 = ROOT / "stages" / STAGE286_ID
RUN286A = STAGE286 / "02_runs" / "run286A"
RUN286B = STAGE286 / "02_runs" / "run286B"
RUN_DIR = STAGE286 / "02_runs" / "run286C"
REVIEWS286 = STAGE286 / "03_reviews"
SELECTED286 = STAGE286 / "04_selected" / "selection_status.md"
REVIEW_INDEX286 = REVIEWS286 / "review_index.md"
STAGE_LEDGER286 = REVIEWS286 / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN286A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN286B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN286B / "execution_result.json"
SOURCE_RUN_MANIFEST = RUN286B / "run_manifest.json"
SOURCE_SUPPLY = RUN286A / "candidate_supply_diagnostics.csv"
PRODUCER = Path("stage_pipelines/stage286/review_trade_density_curve_quality_mt5_probe.py")

SCOREBOARD = RUN_DIR / "trade_density_curve_quality_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
TRADE_QUALITY = RUN_DIR / "trade_quality_summary.csv"
CURVE = RUN_DIR / "curve_stability_summary.csv"
LOCAL_POCKETS = RUN_DIR / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
SURVIVOR_CLUE_QUEUE = RUN_DIR / "stage287_density_scale_curve_pocket_seed_queue.csv"
RECEIPT = RUN_DIR / "trade_density_curve_quality_review_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS286 / "run286C_trade_density_curve_quality_review_stage287_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage286_density_scale_curve_quality_review_stage287_open.md"

STAGE287 = ROOT / "stages" / STAGE287_ID
SPEC287 = STAGE287 / "00_spec" / "stage_brief.md"
INPUTS287 = STAGE287 / "01_inputs"
REVIEWS287 = STAGE287 / "03_reviews"
SELECTED287 = STAGE287 / "04_selected" / "selection_status.md"
STAGE_LEDGER287 = REVIEWS287 / "stage_run_ledger.csv"
REVIEW_INDEX287 = REVIEWS287 / "review_index.md"
INPUT_REFS287 = INPUTS287 / "input_refs.md"

STAGE267_REFS = [
    ROOT / "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_equity_curve_shape_grading_report.md",
    ROOT / "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_monthly_weakness_matrix.csv",
    ROOT / "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_segment_weakness_matrix.csv",
    ROOT / "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267ET_runtime_gap_aware_tenth_followup_or_prune_mt5_execution.md",
]
STAGE282_REFS = [
    ROOT / "stages/282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild/02_runs/run282C/stability_scoreboard.csv",
    ROOT / "stages/282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild/02_runs/run282C/curve_stability_summary.csv",
]

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

BASELINE_CP282D = {
    "validation_net": 89.64,
    "oos_net": 190.55,
    "validation_trade_density": 80 / 183,
    "oos_trade_density": 81 / 131,
}

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "experiment_lane",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_trades_per_day",
    "validation_dd",
    "validation_recovery",
    "validation_expectancy",
    "validation_positive_month_share",
    "validation_worst_month_net",
    "validation_worst_session_net",
    "validation_worst_rolling_20_net",
    "validation_worst_rolling_50_net",
    "validation_worst_rolling_100_net",
    "validation_underwater_ratio",
    "validation_max_losing_streak",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_trades_per_day",
    "oos_dd",
    "oos_recovery",
    "oos_expectancy",
    "oos_positive_month_share",
    "oos_worst_month_net",
    "oos_worst_session_net",
    "oos_worst_rolling_20_net",
    "oos_worst_rolling_50_net",
    "oos_worst_rolling_100_net",
    "oos_underwater_ratio",
    "oos_max_losing_streak",
    "density_gate",
    "profit_scale_gate",
    "efficiency_gate",
    "curve_quality_gate",
    "review_label",
    "failure_reasons",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
ATTRIBUTION_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "tier_scope",
    "split",
    "bucket",
    "net_profit",
    "trade_count",
    "win_rate",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "share_of_positive_net",
    "source_report_path",
)
TRADE_QUALITY_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "tier_scope",
    "split",
    "trade_count",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "win_rate",
    "expectancy",
    "average_win",
    "average_loss",
    "largest_win",
    "largest_loss",
    "max_losing_streak_count",
    "max_losing_streak_loss",
    "top_trade_contribution_share",
    "top_10pct_contribution_share",
    "source_report_path",
)
CURVE_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "tier_scope",
    "split",
    "start_balance",
    "end_balance",
    "net_profit",
    "max_drawdown",
    "max_drawdown_percent",
    "recovery_factor",
    "new_high_count",
    "underwater_trade_count",
    "underwater_ratio",
    "source_report_path",
)
LOCAL_POCKET_COLUMNS = (
    "materialized_branch_id",
    "tier_scope",
    "split",
    "rolling_window",
    "worst_rolling_net",
    "pocket_threshold",
    "pocket_label",
    "source_report_path",
)
FAILURE_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "failure_type",
    "failure_reasons",
    "salvage_value",
    "reopen_condition",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "seed_id",
    "source_materialized_branch_id",
    "source_package_id",
    "seed_role",
    "fresh_stage287_question",
    "required_change",
    "forbidden_repair_loop",
    "prior_stage_refs",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    text = str(value or "").strip()
    if not text:
        return {}
    return dict(ast.literal_eval(text))


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_MANIFEST)}


def attempt_role_key(tier_scope: str, route_role: str) -> str:
    if tier_scope == "Tier A+B" or route_role == "actual_routed_total":
        return "actual_routed"
    if tier_scope == "Tier A":
        return "tier_a"
    if tier_scope == "Tier B":
        return "tier_b"
    return str(tier_scope).lower().replace(" ", "_")


def parse_records() -> dict[tuple[str, str, str], dict[str, Any]]:
    records: dict[tuple[str, str, str], dict[str, Any]] = {}
    known_ids = sorted(manifest_by_id(), key=len, reverse=True)
    for row in read_csv_dicts(SOURCE_KPI):
        metrics = parse_obj(row.get("metrics"))
        report = parse_obj(row.get("report"))
        attempt_name = str(report.get("attempt_name") or row.get("record_view") or "")
        materialized_id = next((item for item in known_ids if item in attempt_name), "")
        role = attempt_role_key(str(row.get("tier_scope", "")), str(row.get("route_role", "")))
        split = str(row.get("split", ""))
        if materialized_id:
            records[(materialized_id, role, split)] = {
                "tier_scope": row.get("tier_scope", ""),
                "route_role": row.get("route_role", ""),
                "split": split,
                "metrics": metrics,
                "report_path": Path(str(metrics.get("report_path", ""))),
                "attempt_name": attempt_name,
            }
    return records


def metric(records: Mapping[tuple[str, str, str], Mapping[str, Any]], materialized_id: str, role: str, split: str, key: str) -> float:
    entry = records.get((materialized_id, role, split), {})
    metrics = entry.get("metrics", {}) if isinstance(entry, Mapping) else {}
    return safe_float(metrics.get(key))


def rolling_min(profits: Sequence[float], window: int) -> float:
    if len(profits) < window:
        return 0.0
    return float(pd.Series([float(value) for value in profits]).rolling(window).sum().min())


def split_days(split: str) -> int:
    return 183 if split == "validation_is" else 131


def summarize_report(
    *,
    materialized_id: str,
    package_id: str,
    seed_role: str,
    tier_scope: str,
    split: str,
    report_path: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    frame = trade_frame(report_path)
    monthly = attribution_rows(
        frame,
        materialized_id=materialized_id,
        seed_role=seed_role,
        tier_scope=tier_scope,
        split=split,
        source_report_path=report_path,
        bucket_column="month",
    )
    session = attribution_rows(
        frame,
        materialized_id=materialized_id,
        seed_role=seed_role,
        tier_scope=tier_scope,
        split=split,
        source_report_path=report_path,
        bucket_column="session",
    )
    quality = {
        "materialized_branch_id": materialized_id,
        "seed_role": seed_role,
        "tier_scope": tier_scope,
        "split": split,
        **quality_summary(frame),
        "source_report_path": report_path.as_posix(),
    }
    profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
    curve = {
        "materialized_branch_id": materialized_id,
        "seed_role": seed_role,
        "tier_scope": tier_scope,
        "split": split,
        **drawdown_stats(profits),
        "underwater_ratio": (drawdown_stats(profits)["underwater_trade_count"] / len(profits)) if profits else 0.0,
        "source_report_path": report_path.as_posix(),
    }
    pocket_rows = []
    for window in (20, 50, 100):
        worst = rolling_min(profits, window)
        threshold = -120.0 if window == 20 else -150.0 if window == 50 else -180.0
        pocket_rows.append(
            {
                "materialized_branch_id": materialized_id,
                "tier_scope": tier_scope,
                "split": split,
                "rolling_window": window,
                "worst_rolling_net": worst,
                "pocket_threshold": threshold,
                "pocket_label": "deep_local_pocket" if worst < threshold else "tolerable",
                "source_report_path": report_path.as_posix(),
            }
        )
    return monthly, session, quality, curve, pocket_rows


def min_bucket(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, tier_scope: str) -> float:
    values = [
        safe_float(row.get("net_profit"))
        for row in rows
        if row.get("materialized_branch_id") == materialized_id and row.get("split") == split and row.get("tier_scope") == tier_scope
    ]
    return min(values) if values else 0.0


def positive_share(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, tier_scope: str) -> float:
    values = [
        safe_float(row.get("net_profit"))
        for row in rows
        if row.get("materialized_branch_id") == materialized_id and row.get("split") == split and row.get("tier_scope") == tier_scope
    ]
    return sum(1 for value in values if value > 0) / len(values) if values else 0.0


def curve_value(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, key: str) -> float:
    for row in rows:
        if row.get("materialized_branch_id") == materialized_id and row.get("split") == split and row.get("tier_scope") == "Tier A+B":
            return safe_float(row.get(key))
    return 0.0


def quality_value(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, key: str) -> float:
    for row in rows:
        if row.get("materialized_branch_id") == materialized_id and row.get("split") == split and row.get("tier_scope") == "Tier A+B":
            return safe_float(row.get(key))
    return 0.0


def pocket_value(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, window: int) -> float:
    for row in rows:
        if (
            row.get("materialized_branch_id") == materialized_id
            and row.get("split") == split
            and row.get("tier_scope") == "Tier A+B"
            and int(row.get("rolling_window", 0)) == window
        ):
            return safe_float(row.get("worst_rolling_net"))
    return 0.0


def summarize_candidate(
    manifest_row: Mapping[str, str],
    records: Mapping[tuple[str, str, str], Mapping[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    materialized_id = str(manifest_row["materialized_branch_id"])
    package_id = str(manifest_row["package_id"])
    seed_role = str(manifest_row.get("queue_role", ""))
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    for role, tier_scope in (("actual_routed", "Tier A+B"), ("tier_a", "Tier A"), ("tier_b", "Tier B")):
        for split in ("validation_is", "oos"):
            entry = records.get((materialized_id, role, split))
            if not entry:
                continue
            report_path = Path(str(entry.get("report_path", "")))
            monthly, session, quality, curve, pockets = summarize_report(
                materialized_id=materialized_id,
                package_id=package_id,
                seed_role=seed_role,
                tier_scope=tier_scope,
                split=split,
                report_path=report_path,
            )
            monthly_rows.extend(monthly)
            session_rows.extend(session)
            quality_rows.append(quality)
            curve_rows.append(curve)
            pocket_rows.extend(pockets)

    val_trades = metric(records, materialized_id, "actual_routed", "validation_is", "trade_count")
    oos_trades = metric(records, materialized_id, "actual_routed", "oos", "trade_count")
    val_tpd = val_trades / split_days("validation_is")
    oos_tpd = oos_trades / split_days("oos")
    val_net = metric(records, materialized_id, "actual_routed", "validation_is", "net_profit")
    oos_net = metric(records, materialized_id, "actual_routed", "oos", "net_profit")
    val_pf = metric(records, materialized_id, "actual_routed", "validation_is", "profit_factor")
    oos_pf = metric(records, materialized_id, "actual_routed", "oos", "profit_factor")
    val_rec = metric(records, materialized_id, "actual_routed", "validation_is", "recovery_factor")
    oos_rec = metric(records, materialized_id, "actual_routed", "oos", "recovery_factor")
    val_exp = metric(records, materialized_id, "actual_routed", "validation_is", "expectancy")
    oos_exp = metric(records, materialized_id, "actual_routed", "oos", "expectancy")

    density_ok = 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0
    profit_ok = val_net > BASELINE_CP282D["validation_net"] and oos_net > BASELINE_CP282D["oos_net"]
    efficiency_ok = val_pf >= 1.10 and oos_pf >= 1.10 and val_rec >= 1.0 and oos_rec >= 1.0 and val_exp > 0 and oos_exp > 0
    curve_ok = (
        positive_share(monthly_rows, materialized_id, "validation_is", "Tier A+B") >= 0.60
        and positive_share(monthly_rows, materialized_id, "oos", "Tier A+B") >= 0.60
        and min_bucket(monthly_rows, materialized_id, "validation_is", "Tier A+B") >= -90.0
        and min_bucket(monthly_rows, materialized_id, "oos", "Tier A+B") >= -90.0
        and pocket_value(pocket_rows, materialized_id, "validation_is", 20) >= -120.0
        and pocket_value(pocket_rows, materialized_id, "validation_is", 50) >= -150.0
        and pocket_value(pocket_rows, materialized_id, "oos", 50) >= -150.0
        and curve_value(curve_rows, materialized_id, "validation_is", "underwater_ratio") <= 0.90
        and curve_value(curve_rows, materialized_id, "oos", "underwater_ratio") <= 0.90
    )
    reasons: list[str] = []
    if not density_ok:
        reasons.append("trade_density_outside_4_10")
    if not profit_ok:
        reasons.append("profit_scale_not_both_splits")
    if not efficiency_ok:
        reasons.append("efficiency_pf_recovery_expectancy_not_jointly_credible")
    if not curve_ok:
        reasons.append("curve_quality_local_pockets_or_underwater_ratio_fail")
    if not reasons:
        label = "pressure_survivor_needs_adapter_stage"
    elif density_ok and profit_ok:
        label = "scale_density_clue_curve_rebuild_seed"
    else:
        label = "valid_negative_or_control"
    scoreboard = {
        "materialized_branch_id": materialized_id,
        "package_id": package_id,
        "experiment_lane": seed_role,
        "validation_net_profit": val_net,
        "validation_pf": val_pf,
        "validation_trade_count": val_trades,
        "validation_trades_per_day": val_tpd,
        "validation_dd": metric(records, materialized_id, "actual_routed", "validation_is", "max_drawdown_amount"),
        "validation_recovery": val_rec,
        "validation_expectancy": val_exp,
        "validation_positive_month_share": positive_share(monthly_rows, materialized_id, "validation_is", "Tier A+B"),
        "validation_worst_month_net": min_bucket(monthly_rows, materialized_id, "validation_is", "Tier A+B"),
        "validation_worst_session_net": min_bucket(session_rows, materialized_id, "validation_is", "Tier A+B"),
        "validation_worst_rolling_20_net": pocket_value(pocket_rows, materialized_id, "validation_is", 20),
        "validation_worst_rolling_50_net": pocket_value(pocket_rows, materialized_id, "validation_is", 50),
        "validation_worst_rolling_100_net": pocket_value(pocket_rows, materialized_id, "validation_is", 100),
        "validation_underwater_ratio": curve_value(curve_rows, materialized_id, "validation_is", "underwater_ratio"),
        "validation_max_losing_streak": quality_value(quality_rows, materialized_id, "validation_is", "max_losing_streak_count"),
        "oos_net_profit": oos_net,
        "oos_pf": oos_pf,
        "oos_trade_count": oos_trades,
        "oos_trades_per_day": oos_tpd,
        "oos_dd": metric(records, materialized_id, "actual_routed", "oos", "max_drawdown_amount"),
        "oos_recovery": oos_rec,
        "oos_expectancy": oos_exp,
        "oos_positive_month_share": positive_share(monthly_rows, materialized_id, "oos", "Tier A+B"),
        "oos_worst_month_net": min_bucket(monthly_rows, materialized_id, "oos", "Tier A+B"),
        "oos_worst_session_net": min_bucket(session_rows, materialized_id, "oos", "Tier A+B"),
        "oos_worst_rolling_20_net": pocket_value(pocket_rows, materialized_id, "oos", 20),
        "oos_worst_rolling_50_net": pocket_value(pocket_rows, materialized_id, "oos", 50),
        "oos_worst_rolling_100_net": pocket_value(pocket_rows, materialized_id, "oos", 100),
        "oos_underwater_ratio": curve_value(curve_rows, materialized_id, "oos", "underwater_ratio"),
        "oos_max_losing_streak": quality_value(quality_rows, materialized_id, "oos", "max_losing_streak_count"),
        "density_gate": "passed" if density_ok else "failed",
        "profit_scale_gate": "passed" if profit_ok else "failed",
        "efficiency_gate": "passed" if efficiency_ok else "failed",
        "curve_quality_gate": "passed" if curve_ok else "failed",
        "review_label": label,
        "failure_reasons": "|".join(reasons) if reasons else "none",
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": BOUNDARY,
    }
    failure_rows = []
    if reasons:
        failure_rows.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "failure_type": label,
                "failure_reasons": "|".join(reasons),
                "salvage_value": "density_scale_seed" if density_ok and profit_ok else "failure_memory",
                "reopen_condition": "Only reopen with new curve-pocket construction, not threshold-only repair.",
                "claim_boundary": BOUNDARY,
            }
        )
    return scoreboard, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows


def build_outputs() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    records = parse_records()
    scoreboard_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    prior_refs = [rel(path) for path in [*STAGE267_REFS, *STAGE282_REFS] if path_exists(path)]
    for row in read_csv_dicts(SOURCE_MANIFEST):
        scoreboard, monthly, session, quality, curve, pockets, failures = summarize_candidate(row, records)
        scoreboard_rows.append(scoreboard)
        monthly_rows.extend(monthly)
        session_rows.extend(session)
        quality_rows.extend(quality)
        curve_rows.extend(curve)
        pocket_rows.extend(pockets)
        failure_rows.extend(failures)
        if scoreboard["density_gate"] == "passed" and scoreboard["profit_scale_gate"] == "passed":
            queue_rows.append(
                {
                    "seed_id": f"stage287_seed_{scoreboard['materialized_branch_id']}",
                    "source_materialized_branch_id": scoreboard["materialized_branch_id"],
                    "source_package_id": scoreboard["package_id"],
                    "seed_role": "density_scale_clue_not_candidate",
                    "fresh_stage287_question": "Can density/scale survive if local curve pockets are removed by session-aware risk and hold logic?",
                    "required_change": "new curve-pocket construction using prior stage weakness matrices plus Stage286 D/E seed behavior",
                    "forbidden_repair_loop": "Do not only nudge threshold on the same branch.",
                    "prior_stage_refs": "|".join(prior_refs),
                    "claim_boundary": BOUNDARY,
                }
            )
    return scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows, queue_rows


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    seed_lines = [
        f"- `{row['package_id']}`: validation(검증) `{float(row['validation_net_profit']):.2f}` / `{float(row['validation_trades_per_day']):.2f}` trades/day(일 거래), OOS(표본외) `{float(row['oos_net_profit']):.2f}` / `{float(row['oos_trades_per_day']):.2f}` trades/day(일 거래), curve gate(곡선 게이트) `{row['curve_quality_gate']}`."
        for row in scoreboard_rows
    ]
    return f"""# run286C Trade Density Curve Quality Review(286C 거래 밀도/곡선 품질 검토)

- stage_id(단계 ID): `{STAGE286_ID}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Stage287 seeds(287단계 씨앗): `{len(queue_rows)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Review Read(검토 판독)

{chr(10).join(seed_lines)}

Stage286(286단계)는 density/scale clue(밀도/규모 단서)를 찾았지만 smooth curve(매끄러운 곡선) 조건은 통과하지 못했다.
Effect(효과): cp286D/cp286E(286D/286E 후보)는 selected candidate(선택 후보)가 아니라 Stage287(287단계) curve-pocket rebuild(곡선 포켓 재구성) seed(씨앗)로만 넘긴다.

## Boundary(경계)

`{BOUNDARY}`

Effect(효과): 운영 의미나 ONNX(온엑스) 진행을 주장하지 않고, 다음 단계에서 새 구조로 검증한다.
"""


def write_stage287_open(queue_rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(SPEC287.parent).mkdir(parents=True, exist_ok=True)
    io_path(INPUTS287).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS287).mkdir(parents=True, exist_ok=True)
    io_path(SELECTED287.parent).mkdir(parents=True, exist_ok=True)
    write_md(
        SPEC287,
        f"""# Stage287 Density Scale Curve Pocket Rebuild(287단계 밀도/규모/곡선 포켓 재구성)

- canonical_stage_id(정식 단계 ID): `{STAGE287_ID}`
- big_question(큰 질문): 4-10 trades/day(일 4-10거래)와 순수익 규모를 유지하면서 확대 구간 curve pocket(곡선 포켓)을 구조적으로 줄일 수 있는가?
- source_stage(원천 단계): `{STAGE286_ID}`
- seed_count(씨앗 수): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): Stage286(286단계)의 cp286D/cp286E(286D/286E)는 후보가 아니라 density/scale clue(밀도/규모 단서)로만 쓰며, threshold-only repair(임계값만 고치는 수리)는 금지한다.
""",
    )
    prior_lines = [f"- `{rel(path)}`" for path in [*STAGE267_REFS, *STAGE282_REFS, SCOREBOARD, LOCAL_POCKETS] if path_exists(path)]
    write_md(
        INPUT_REFS287,
        f"""# Stage287 Input Refs(287단계 입력 참조)

{chr(10).join(prior_lines)}

Effect(효과): 과거 stage(단계) 자료를 curve pocket(곡선 포켓), 월별 약점, segment weakness(구간 약점), trade density(거래 밀도) 설계 입력으로 다시 연결한다.
""",
    )
    write_csv(INPUTS287 / "stage287_density_scale_curve_pocket_seed_queue.csv", QUEUE_COLUMNS, queue_rows)
    write_md(
        SELECTED287,
        f"""# Stage287 Selection Status(287단계 선택 상태)

- stage_status(단계 상태): `opened_density_scale_curve_pocket_rebuild`
- current_packet(현재 작업 묶음): `stage287_density_scale_curve_pocket_rebuild_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE286_ID}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUT_REFS287)}`
""",
    )
    write_csv(
        STAGE_LEDGER287,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage287_open",
                "stage_id": STAGE287_ID,
                "run_id": RUN_ID,
                "view": "stage287_open_from_stage286_density_scale_clues",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage287_seed_queue",
                "status": "opened_density_scale_curve_pocket_rebuild",
                "judgment": "opened_from_density_scale_clue_no_candidate",
                "evidence_boundary": "no_candidate_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"seed_count={len(queue_rows)};next_action={NEXT_ACTION}",
            }
        ],
    )
    write_md(REVIEW_INDEX287, f"# Stage287 Review Index(287단계 검토 색인)\n\n- input_refs(입력 참조): `{rel(INPUT_REFS287)}`\n")


def write_outputs(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    quality_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    pocket_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    created_at: str,
) -> list[Path]:
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(TRADE_QUALITY, TRADE_QUALITY_COLUMNS, quality_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(LOCAL_POCKETS, LOCAL_POCKET_COLUMNS, pocket_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(SURVIVOR_CLUE_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_json(
        RECEIPT,
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "candidate_selected": False,
            "density_scale_seed_count": len(queue_rows),
            "stage287_opened": True,
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run286C_density_scale_curve_quality_review",
                "evidence_available": rel(SCOREBOARD),
                "evidence_missing": "Adapter package and ONNX parity because curve quality failed",
                "judgment_label": JUDGMENT,
                "judgment_class": "negative_with_salvage_seed",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "밀도/수익 규모 단서는 있으나 곡선 포켓 때문에 후보 선택은 없다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "trade_density_review(거래 밀도 검토)",
                "status": "passed",
                "evidence_path": rel(SCOREBOARD),
                "effect": "4-10 trades/day(일 4-10거래) 통과 후보를 분리했다.",
            },
            {
                "gate_name": "curve_quality_review(곡선 품질 검토)",
                "status": "failed_for_candidate_selection",
                "evidence_path": rel(LOCAL_POCKETS),
                "effect": "곡선 포켓 때문에 Adapter/ONNX(어댑터/온엑스) 진행을 막았다.",
            },
            {
                "gate_name": "stage_commit_required(단계 커밋 필요)",
                "status": "pending_external_git_commit",
                "evidence_path": rel(REPORT),
                "effect": "Stage286(286단계) 종료 뒤 Git commit(깃 커밋)을 별도 수행한다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, queue_rows))
    write_md(
        DECISION,
        f"""# Stage286 Density Scale Found, Curve Quality Failed(286단계 밀도/규모 발견, 곡선 품질 실패)

- date(날짜): `{UPDATED_ON}`
- stage_id(단계 ID): `{STAGE286_ID}`
- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Stage287(287단계): `{STAGE287_ID}`

Effect(효과): cp286D/cp286E(286D/286E)는 ONNX-worthy candidate(온엑스 가치 후보)가 아니라 density/scale clue(밀도/규모 단서)로만 남긴다.
""",
    )
    write_stage287_open(queue_rows)
    artifacts = [
        SCOREBOARD,
        MONTHLY,
        SESSION,
        TRADE_QUALITY,
        CURVE,
        LOCAL_POCKETS,
        FAILURE_MEMORY,
        SURVIVOR_CLUE_QUEUE,
        RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC287,
        INPUT_REFS287,
        INPUTS287 / "stage287_density_scale_curve_pocket_seed_queue.csv",
        SELECTED287,
        STAGE_LEDGER287,
        REVIEW_INDEX287,
    ]
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": PRODUCER.as_posix(),
            "source_artifacts": [rel(SOURCE_MANIFEST), rel(SOURCE_KPI), rel(SOURCE_EXECUTION), rel(SOURCE_RUN_MANIFEST), rel(SOURCE_SUPPLY)],
            "prior_stage_refs": [rel(path) for path in [*STAGE267_REFS, *STAGE282_REFS] if path_exists(path)],
            "produced_artifacts": [rel(path) for path in artifacts if path_exists(path)],
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts.append(LINEAGE)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE286_ID,
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "stage287_opened": STAGE287_ID,
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts.append(RUN_MANIFEST)
    return [path for path in artifacts if path_exists(path)]


def update_registers_and_docs(
    created_at: str,
    artifacts: Sequence[Path],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE286_ID,
                "lane": "onnx_candidate_campaign_trade_density_curve_quality_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};stage287_seed_count={len(queue_rows)}",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage286_closeout",
                "stage_id": STAGE286_ID,
                "run_id": RUN_ID,
                "subrun_id": "run286C",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "trade_density_curve_quality_review",
                "tier_scope": "Tier A/Tier B/Tier A+B",
                "kpi_scope": "regular_risk_execution",
                "scoreboard_lane": "trade_density_curve_quality",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"stage287_seed_count={len(queue_rows)}",
                "guardrail_kpi": "curve_quality_failed_no_adapter_no_onnx",
                "external_verification_status": "completed",
                "notes": "Stage286 closed with density/scale clues but no selected candidate.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER286,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage286_closeout",
                "stage_id": STAGE286_ID,
                "run_id": RUN_ID,
                "view": "trade_density_curve_quality_review_stage287_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "trade_density_curve_quality_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "no_candidate_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"failure_rows={len(failure_rows)};stage287_seed_count={len(queue_rows)}",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage286_curve_quality_review_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE286_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run286C trade density curve quality review(286C 거래 밀도 곡선 품질 검토)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED286).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- selected_candidate(선택 후보):", "- selected_candidate(선택 후보): `none`")
    selected = replace_line_prefix(selected, "- Adapter package(어댑터 패키지):", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run286C_report", f"- run286C_report(286C 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage287_open", f"- stage287_open(287단계 개방): `{STAGE287_ID}`")
    write_md(SELECTED286, selected)

    review_index = io_path(REVIEW_INDEX286).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX286) else "# Stage286 Review Index(286단계 검토 색인)\n"
    review_index = append_once(review_index, "run286C_report", f"- run286C_report(286C 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX286, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage287_density_scale_curve_pocket_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE287_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE286_ID}`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_density_scale_curve_pocket_rebuild`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = replace_line_prefix(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{BOUNDARY}`")
    current = append_once(
        current,
        "run286C_summary",
        f"- run286C_summary(286C 요약): Stage286(286단계)은 density/scale clue(밀도/규모 단서) `{len(queue_rows)}`개를 찾았지만 curve pocket(곡선 포켓) 때문에 selected candidate(선택 후보) 없이 닫고 Stage287(287단계)을 열었다. Effect(효과): Adapter/ONNX(어댑터/온엑스)는 진행하지 않고 곡선 포켓을 새 구조로 줄이는 질문으로 넘긴다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE287_ID}")
    focus = (
        f"- >-\n"
        f"  Stage286(286단계) run286C(286C 실행) trade density/curve quality review(거래 밀도/곡선 품질 검토) `{RUN_ID}`. "
        f"Effect(효과): density/scale clue(밀도/규모 단서) `{len(queue_rows)}`개를 Stage287(287단계) seed(씨앗)로 넘기고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run286C Density scale clue, curve quality failure(286C 밀도/규모 단서, 곡선 품질 실패)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Stage286(286단계)을 selected candidate(선택 후보) 없이 닫고 Stage287(287단계)을 열었다.\n- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST287-DENSITY-SCALE-CURVE-POCKET-REBUILD",
        f"| `IDEA-ST287-DENSITY-SCALE-CURVE-POCKET-REBUILD` | `{STAGE287_ID}` | density/scale clue(밀도/규모 단서) `{len(queue_rows)}`개에서 curve pocket(곡선 포켓)을 구조적으로 줄이는 새 후보 구성 | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | threshold-only repair(임계값만 고치는 수리)를 금지하고 과거 stage(단계) 약점 자료를 다시 연결한다. |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST286-CURVE-QUALITY-FAIL",
        f"| `NEG-ST286-CURVE-QUALITY-FAIL` | `{STAGE286_ID}` | `{RUN_ID}` | density/scale clue(밀도/규모 단서)는 있으나 curve pocket(곡선 포켓)과 underwater ratio(수중 비율)가 ONNX-worthy candidate(온엑스 가치 후보) 기준 미달 | Stage287(287단계)에서 새 구조로만 재개 | threshold-only repair(임계값만 고치는 수리) 금지 |",
    )
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS286).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows, queue_rows = build_outputs()
    artifacts = write_outputs(
        scoreboard_rows,
        monthly_rows,
        session_rows,
        quality_rows,
        curve_rows,
        pocket_rows,
        failure_rows,
        queue_rows,
        created_at,
    )
    update_registers_and_docs(created_at, artifacts, scoreboard_rows, failure_rows, queue_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "scoreboard_rows": len(scoreboard_rows),
                "failure_memory_count": len(failure_rows),
                "stage287_seed_count": len(queue_rows),
                "target_stage": STAGE287_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
