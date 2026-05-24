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
    write_csv_rows,
)
from stage_pipelines.stage280.validate_directional_mapping_stability import (  # noqa: E402
    attribution_rows,
    drawdown_stats,
    quality_summary,
    safe_float,
    trade_frame,
)


STAGE287_ID = "287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild"
STAGE288_ID = "288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild"
RUN_ID = "run287C_review_density_scale_curve_pocket_mt5_probe_v1"
SOURCE_RUN_ID = "run287B_density_scale_curve_pocket_mt5_probe_v1"
STATUS = "completed_density_scale_curve_pocket_review_no_candidate_stage288_opened"
JUDGMENT = "density_profit_seed_found_but_efficiency_curve_fail_no_adapter_no_onnx"
NEXT_ACTION = "run288A_design_risk_reward_exit_asymmetry_rebuild_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE287 = ROOT / "stages" / STAGE287_ID
RUN287A = STAGE287 / "02_runs" / "run287A"
RUN287B = STAGE287 / "02_runs" / "run287B"
RUN_DIR = STAGE287 / "02_runs" / "run287C"
REVIEWS287 = STAGE287 / "03_reviews"
SELECTED287 = STAGE287 / "04_selected" / "selection_status.md"
REVIEW_INDEX287 = REVIEWS287 / "review_index.md"
STAGE_LEDGER287 = REVIEWS287 / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN287A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN287B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN287B / "execution_result.json"
SOURCE_RUN_MANIFEST = RUN287B / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage287/review_density_scale_curve_pocket_mt5_probe.py")

SCOREBOARD = RUN_DIR / "density_scale_curve_pocket_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
TRADE_QUALITY = RUN_DIR / "trade_quality_summary.csv"
CURVE = RUN_DIR / "curve_stability_summary.csv"
LOCAL_POCKETS = RUN_DIR / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
STAGE288_QUEUE = RUN_DIR / "stage288_risk_reward_exit_seed_queue.csv"
RECEIPT = RUN_DIR / "density_scale_curve_pocket_review_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS287 / "run287C_density_scale_curve_pocket_review_stage288_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage287_density_scale_curve_pocket_review_stage288_open.md"

STAGE288 = ROOT / "stages" / STAGE288_ID
SPEC288 = STAGE288 / "00_spec" / "stage_brief.md"
INPUTS288 = STAGE288 / "01_inputs"
REVIEWS288 = STAGE288 / "03_reviews"
SELECTED288 = STAGE288 / "04_selected" / "selection_status.md"
STAGE_LEDGER288 = REVIEWS288 / "stage_run_ledger.csv"
REVIEW_INDEX288 = REVIEWS288 / "review_index.md"
INPUT_REFS288 = INPUTS288 / "input_refs.md"
QUEUE288 = INPUTS288 / "stage288_risk_reward_exit_seed_queue.csv"

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
    "fresh_stage288_question",
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing = read_csv_dicts(path)
    new_keys = {str(row.get(key, "")).strip() for row in rows}
    merged = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, columns, merged)


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


def parse_obj(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = str(value or "").strip()
    if not text:
        return {}
    return dict(ast.literal_eval(text))


def manifest_rows() -> list[dict[str, str]]:
    return read_csv_dicts(SOURCE_MANIFEST)


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {row["materialized_branch_id"]: row for row in manifest_rows()}


def attempt_role_key(tier_scope: str, route_role: str) -> str:
    if route_role == "actual_routed_total" or "Tier A primary" in tier_scope:
        return "actual_routed"
    if tier_scope == "Tier A full-context":
        return "tier_a"
    if tier_scope == "Tier B partial-context":
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


def metric(records: Mapping[tuple[str, str, str], Mapping[str, Any]], materialized_id: str, split: str, key: str) -> float:
    entry = records.get((materialized_id, "actual_routed", split), {})
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
    stats = drawdown_stats(profits)
    curve = {
        "materialized_branch_id": materialized_id,
        "seed_role": seed_role,
        "tier_scope": tier_scope,
        "split": split,
        **stats,
        "underwater_ratio": (stats["underwater_trade_count"] / len(profits)) if profits else 0.0,
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


def filtered_values(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, tier_scope: str, key: str) -> list[float]:
    return [
        safe_float(row.get(key))
        for row in rows
        if row.get("materialized_branch_id") == materialized_id
        and row.get("split") == split
        and row.get("tier_scope") == tier_scope
    ]


def min_bucket(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, tier_scope: str) -> float:
    values = filtered_values(rows, materialized_id, split, tier_scope, "net_profit")
    return min(values) if values else 0.0


def positive_share(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, tier_scope: str) -> float:
    values = filtered_values(rows, materialized_id, split, tier_scope, "net_profit")
    return sum(1 for value in values if value > 0) / len(values) if values else 0.0


def first_value(rows: Sequence[Mapping[str, Any]], materialized_id: str, split: str, tier_scope: str, key: str) -> float:
    values = filtered_values(rows, materialized_id, split, tier_scope, key)
    return values[0] if values else 0.0


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
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
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
            monthly, session, quality, curve, pockets = summarize_report(
                materialized_id=materialized_id,
                seed_role=seed_role,
                tier_scope=tier_scope,
                split=split,
                report_path=Path(str(entry.get("report_path", ""))),
            )
            monthly_rows.extend(monthly)
            session_rows.extend(session)
            quality_rows.append(quality)
            curve_rows.append(curve)
            pocket_rows.extend(pockets)

    val_trades = metric(records, materialized_id, "validation_is", "trade_count")
    oos_trades = metric(records, materialized_id, "oos", "trade_count")
    val_tpd = val_trades / split_days("validation_is")
    oos_tpd = oos_trades / split_days("oos")
    val_net = metric(records, materialized_id, "validation_is", "net_profit")
    oos_net = metric(records, materialized_id, "oos", "net_profit")
    val_pf = metric(records, materialized_id, "validation_is", "profit_factor")
    oos_pf = metric(records, materialized_id, "oos", "profit_factor")
    val_rec = metric(records, materialized_id, "validation_is", "recovery_factor")
    oos_rec = metric(records, materialized_id, "oos", "recovery_factor")
    val_exp = metric(records, materialized_id, "validation_is", "expectancy")
    oos_exp = metric(records, materialized_id, "oos", "expectancy")

    density_ok = 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0
    profit_ok = val_net > BASELINE_CP282D["validation_net"] and oos_net > BASELINE_CP282D["oos_net"]
    efficiency_ok = val_pf >= 1.10 and oos_pf >= 1.10 and val_rec >= 1.0 and oos_rec >= 1.0 and val_exp > 0 and oos_exp > 0
    curve_ok = (
        positive_share(monthly_rows, materialized_id, "validation_is", "Tier A+B") >= 0.60
        and positive_share(monthly_rows, materialized_id, "oos", "Tier A+B") >= 0.60
        and min_bucket(monthly_rows, materialized_id, "validation_is", "Tier A+B") >= -90.0
        and min_bucket(monthly_rows, materialized_id, "oos", "Tier A+B") >= -90.0
        and min_bucket(session_rows, materialized_id, "validation_is", "Tier A+B") >= -120.0
        and min_bucket(session_rows, materialized_id, "oos", "Tier A+B") >= -120.0
        and pocket_value(pocket_rows, materialized_id, "validation_is", 20) >= -120.0
        and pocket_value(pocket_rows, materialized_id, "oos", 20) >= -120.0
        and pocket_value(pocket_rows, materialized_id, "validation_is", 50) >= -150.0
        and pocket_value(pocket_rows, materialized_id, "oos", 50) >= -150.0
        and pocket_value(pocket_rows, materialized_id, "validation_is", 100) >= -180.0
        and pocket_value(pocket_rows, materialized_id, "oos", 100) >= -180.0
        and first_value(curve_rows, materialized_id, "validation_is", "Tier A+B", "underwater_ratio") <= 0.90
        and first_value(curve_rows, materialized_id, "oos", "Tier A+B", "underwater_ratio") <= 0.90
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
        label = "adapter_package_candidate_ready"
    elif density_ok and profit_ok:
        label = "density_profit_seed_efficiency_curve_fail"
    elif density_ok:
        label = "density_only_failure_memory"
    else:
        label = "valid_negative_or_smoothness_control"
    scoreboard = {
        "materialized_branch_id": materialized_id,
        "package_id": package_id,
        "experiment_lane": seed_role,
        "validation_net_profit": val_net,
        "validation_pf": val_pf,
        "validation_trade_count": val_trades,
        "validation_trades_per_day": val_tpd,
        "validation_dd": metric(records, materialized_id, "validation_is", "max_drawdown_amount"),
        "validation_recovery": val_rec,
        "validation_expectancy": val_exp,
        "validation_positive_month_share": positive_share(monthly_rows, materialized_id, "validation_is", "Tier A+B"),
        "validation_worst_month_net": min_bucket(monthly_rows, materialized_id, "validation_is", "Tier A+B"),
        "validation_worst_session_net": min_bucket(session_rows, materialized_id, "validation_is", "Tier A+B"),
        "validation_worst_rolling_20_net": pocket_value(pocket_rows, materialized_id, "validation_is", 20),
        "validation_worst_rolling_50_net": pocket_value(pocket_rows, materialized_id, "validation_is", 50),
        "validation_worst_rolling_100_net": pocket_value(pocket_rows, materialized_id, "validation_is", 100),
        "validation_underwater_ratio": first_value(curve_rows, materialized_id, "validation_is", "Tier A+B", "underwater_ratio"),
        "validation_max_losing_streak": first_value(quality_rows, materialized_id, "validation_is", "Tier A+B", "max_losing_streak_count"),
        "oos_net_profit": oos_net,
        "oos_pf": oos_pf,
        "oos_trade_count": oos_trades,
        "oos_trades_per_day": oos_tpd,
        "oos_dd": metric(records, materialized_id, "oos", "max_drawdown_amount"),
        "oos_recovery": oos_rec,
        "oos_expectancy": oos_exp,
        "oos_positive_month_share": positive_share(monthly_rows, materialized_id, "oos", "Tier A+B"),
        "oos_worst_month_net": min_bucket(monthly_rows, materialized_id, "oos", "Tier A+B"),
        "oos_worst_session_net": min_bucket(session_rows, materialized_id, "oos", "Tier A+B"),
        "oos_worst_rolling_20_net": pocket_value(pocket_rows, materialized_id, "oos", 20),
        "oos_worst_rolling_50_net": pocket_value(pocket_rows, materialized_id, "oos", 50),
        "oos_worst_rolling_100_net": pocket_value(pocket_rows, materialized_id, "oos", 100),
        "oos_underwater_ratio": first_value(curve_rows, materialized_id, "oos", "Tier A+B", "underwater_ratio"),
        "oos_max_losing_streak": first_value(quality_rows, materialized_id, "oos", "Tier A+B", "max_losing_streak_count"),
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
                "salvage_value": "risk_reward_exit_seed" if density_ok and (profit_ok or package_id.endswith("volnorm_pressure_release_surface")) else "failure_memory",
                "reopen_condition": "Only reopen with new exit/risk/reward construction, not threshold-only repair.",
                "claim_boundary": BOUNDARY,
            }
        )
    return scoreboard, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    records = parse_records()
    scoreboard_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    prior_refs = [
        rel(SCOREBOARD),
        rel(LOCAL_POCKETS),
        rel(FAILURE_MEMORY),
        rel(ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
        rel(ROOT / "stages/286_onnx_candidate_campaign__trade_density_curve_quality_rebuild/02_runs/run286C/trade_density_curve_quality_scoreboard.csv"),
        rel(ROOT / "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_segment_weakness_matrix.csv"),
    ]
    for row in manifest_rows():
        scoreboard, monthly, session, quality, curve, pockets, failures = summarize_candidate(row, records)
        scoreboard_rows.append(scoreboard)
        monthly_rows.extend(monthly)
        session_rows.extend(session)
        quality_rows.extend(quality)
        curve_rows.extend(curve)
        pocket_rows.extend(pockets)
        failure_rows.extend(failures)
        if scoreboard["package_id"] == "cp287E_consensus_pullback_mix_surface":
            queue_rows.append(
                {
                    "seed_id": "stage288_scale_density_seed_cp287E",
                    "source_materialized_branch_id": scoreboard["materialized_branch_id"],
                    "source_package_id": scoreboard["package_id"],
                    "seed_role": "scale_density_seed_not_candidate",
                    "fresh_stage288_question": "Can ATR SL/TP and exit-risk surface turn scale into credible PF/recovery and remove local pockets?",
                    "required_change": "risk_reward_exit_surface_with_atr_sltp_and_exit_overlay",
                    "forbidden_repair_loop": "Do not only nudge signal threshold or max_hold on cp287E.",
                    "prior_stage_refs": "|".join(prior_refs),
                    "claim_boundary": BOUNDARY,
                }
            )
        if scoreboard["package_id"] == "cp287B_volnorm_pressure_release_surface":
            queue_rows.append(
                {
                    "seed_id": "stage288_smoothness_control_seed_cp287B",
                    "source_materialized_branch_id": scoreboard["materialized_branch_id"],
                    "source_package_id": scoreboard["package_id"],
                    "seed_role": "smoothness_control_seed_not_candidate",
                    "fresh_stage288_question": "Can a smoother low-pocket control regain scale through reward asymmetry without overtrading?",
                    "required_change": "risk_reward_exit_surface_and_density_lift",
                    "forbidden_repair_loop": "Do not only lower the score threshold on cp287B.",
                    "prior_stage_refs": "|".join(prior_refs),
                    "claim_boundary": BOUNDARY,
                }
            )
    return scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows, queue_rows


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        f"- `{row['package_id']}`: validation(검증) net `{float(row['validation_net_profit']):.2f}`, `{float(row['validation_trades_per_day']):.2f}` trades/day(일 거래), OOS(표본외) net `{float(row['oos_net_profit']):.2f}`, `{float(row['oos_trades_per_day']):.2f}` trades/day(일 거래), gates(게이트) `{row['density_gate']}/{row['profit_scale_gate']}/{row['efficiency_gate']}/{row['curve_quality_gate']}`."
        for row in scoreboard_rows
    ]
    return f"""# run287C Density Scale Curve Pocket Review(287C 밀도/규모/곡선 포켓 검토)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage288_seed_count(288단계 씨앗 수): `{len(queue_rows)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Scoreboard(점수판)

{chr(10).join(lines)}

## Decision(결정)

cp287E(287E)는 density/profit scale(밀도/수익 규모)을 통과했지만 PF/recovery/curve(수익 팩터/회복/곡선)를 통과하지 못했다. cp287B(287B)는 더 매끄럽지만 density/profit scale(밀도/수익 규모)이 부족하다. Effect(효과): Stage287(287단계)는 후보 없이 닫고 Stage288(288단계)에서 risk/reward/exit surface(위험/보상/청산 표면)를 새 질문으로 연다.
"""


def stage288_stage_brief(queue_rows: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage288 Risk Reward Exit Asymmetry Rebuild(288단계 위험/보상/청산 비대칭 재구성)

- canonical_stage_id(정식 단계 ID): `{STAGE288_ID}`
- big_question(큰 질문): 4-10 trades/day(일 거래) 밀도와 수익 규모를 유지하면서 ATR SL/TP(ATR 손절/익절), exit overlay(청산 오버레이), model risk sizing(모델 위험 크기)로 PF/recovery/curve pocket(수익 팩터/회복/곡선 포켓)을 동시에 개선할 수 있는가?
- source_stage(원천 단계): `{STAGE287_ID}`
- seed_count(씨앗 수): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): Stage287(287단계)의 신호 밀도 실험을 좁게 수리하지 않고, trade exit/risk-reward surface(거래 청산/위험보상 표면) 자체를 새로 실험한다.
"""


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
    for path in (RUN_DIR, REVIEWS287, INPUTS288, REVIEWS288, SELECTED288.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(TRADE_QUALITY, TRADE_QUALITY_COLUMNS, quality_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(LOCAL_POCKETS, LOCAL_POCKET_COLUMNS, pocket_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(STAGE288_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(QUEUE288, QUEUE_COLUMNS, queue_rows)
    write_json(
        RECEIPT,
        {
            "run_id": RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "scoreboard_rows": len(scoreboard_rows),
            "stage288_seed_count": len(queue_rows),
            "candidate_selected": False,
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "created_at_utc": created_at,
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"{rel(SCOREBOARD)};{rel(LOCAL_POCKETS)};{rel(FAILURE_MEMORY)}",
                "evidence_missing": "Adapter package;ONNX export;ONNX parity;MT5 runtime reproduction for selected package",
                "judgment_label": JUDGMENT,
                "judgment_class": "negative_for_candidate_selection_but_seeded_next_stage(후보 선택은 부정, 다음 단계 씨앗 있음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "거래수와 규모 단서는 있지만 효율과 곡선이 부족해 후보가 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {"gate_name": "density_profit_efficiency_curve_joint_review(밀도/수익/효율/곡선 공동 검토)", "status": "passed", "evidence_path": rel(SCOREBOARD), "effect": "선택 후보 조건을 한 번에 판정했다."},
            {"gate_name": "no_adapter_without_candidate(후보 전 어댑터 금지)", "status": "passed", "evidence_path": rel(RESULT_JUDGMENT), "effect": "Adapter/ONNX(어댑터/온엑스) 진행을 막았다."},
            {"gate_name": "fresh_stage_transition(새 단계 전환)", "status": "passed", "evidence_path": rel(STAGE288_QUEUE), "effect": "단순 repair(수리)가 아니라 exit/risk surface(청산/위험 표면) 질문으로 넘겼다."},
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, queue_rows))
    write_md(SPEC288, stage288_stage_brief(queue_rows))
    input_refs = "\n".join(
        [
            "# Stage288 Input Refs(288단계 입력 참조)",
            "",
            f"- `{rel(SCOREBOARD)}`",
            f"- `{rel(LOCAL_POCKETS)}`",
            f"- `{rel(FAILURE_MEMORY)}`",
            f"- `{rel(STAGE288_QUEUE)}`",
            "- `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`",
            "- `foundation/mt5/include/ObsidianPrime/ExecutionBridge.mqh`",
            "",
            "Effect(효과): Stage288(288단계)은 signal threshold(신호 임계값) 반복이 아니라 risk/reward/exit(위험/보상/청산) 구조 실험으로 시작한다.",
        ]
    )
    write_md(INPUT_REFS288, input_refs)
    write_csv(
        STAGE_LEDGER288,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage288_opened_from_run287C",
                "stage_id": STAGE288_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage288_seed_queue",
                "status": "opened_risk_reward_exit_asymmetry_rebuild",
                "judgment": "stage_opened_no_candidate",
                "evidence_boundary": "planning_from_stage287_failure_memory",
                "report_path": rel(REPORT),
                "notes": f"seed_count={len(queue_rows)};next_action={NEXT_ACTION}",
            }
        ],
    )
    write_md(REVIEW_INDEX288, f"# Stage288 Review Index(288단계 검토 색인)\n\n- input_refs(입력 참조): `{rel(INPUT_REFS288)}`\n- seed_queue(씨앗 대기열): `{rel(QUEUE288)}`\n")
    write_md(
        SELECTED288,
        f"""# Stage288 Selection Status(288단계 선택 상태)

- stage_status(단계 상태): `opened_risk_reward_exit_asymmetry_rebuild`
- current_packet(현재 작업 묶음): `stage288_risk_reward_exit_asymmetry_rebuild_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE287_ID}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUT_REFS288)}`
""",
    )
    write_md(
        DECISION,
        f"""# Stage287 Closeout and Stage288 Open(287단계 종료와 288단계 개방)

- decision_date(결정일): `{UPDATED_ON}`
- source_run(원천 실행): `{RUN_ID}`
- selected_candidate(선택 후보): `none`
- reason(이유): density/profit seed(밀도/수익 씨앗)는 있으나 efficiency/curve gate(효율/곡선 게이트)가 실패했다.
- next_stage(다음 단계): `{STAGE288_ID}`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): Adapter/ONNX(어댑터/온엑스)로 넘어가지 않고, risk/reward/exit surface(위험/보상/청산 표면)로 새 연구 질문을 연다.
""",
    )
    final_paths = [
        SCOREBOARD,
        MONTHLY,
        SESSION,
        TRADE_QUALITY,
        CURVE,
        LOCAL_POCKETS,
        FAILURE_MEMORY,
        STAGE288_QUEUE,
        QUEUE288,
        RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        SPEC288,
        INPUT_REFS288,
        STAGE_LEDGER288,
        REVIEW_INDEX288,
        SELECTED288,
        DECISION,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE287_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "scoreboard_rows": len(scoreboard_rows),
            "failure_rows": len(failure_rows),
            "stage288_seed_count": len(queue_rows),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path_exists(path)},
            "claim_boundary": BOUNDARY,
        },
    )
    final_paths.append(RUN_MANIFEST)
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": PRODUCER.as_posix(),
            "source_artifacts": [rel(SOURCE_MANIFEST), rel(SOURCE_KPI), rel(SOURCE_EXECUTION), rel(SOURCE_RUN_MANIFEST)],
            "produced_artifacts": [rel(path) for path in final_paths if path_exists(path)],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER287), rel(ARTIFACT_REGISTRY)],
            "claim_boundary": BOUNDARY,
        },
    )
    final_paths.append(LINEAGE)
    return [path for path in final_paths if path_exists(path)]


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE287_ID,
                "lane": "density_scale_curve_pocket_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};stage288_seed_count={len(queue_rows)};selected_candidate=none;next_action={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    upsert_csv(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE287_ID,
                "run_id": RUN_ID,
                "subrun_id": "run287C",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "density_scale_curve_pocket_review(밀도/규모/곡선 포켓 검토)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "density_scale_curve_pocket",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};stage288_seed_count={len(queue_rows)}",
                "guardrail_kpi": "selected_candidate=none;adapter=none;onnx=not_claimed",
                "external_verification_status": "completed_run287B_mt5_probe",
                "notes": "Stage287 closed with no candidate; Stage288 opened.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv(
        STAGE_LEDGER287,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE287_ID,
                "run_id": RUN_ID,
                "view": "density_scale_curve_pocket_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": rel(SCOREBOARD),
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "no_candidate_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"failure_rows={len(failure_rows)};stage288_seed_count={len(queue_rows)}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage287_density_scale_curve_pocket_review_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE287_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run287C density scale curve pocket review(287C 밀도/규모/곡선 포켓 검토)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED287).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- selected_candidate(선택 후보):", "- selected_candidate(선택 후보): `none`")
    selected = replace_line_prefix(selected, "- Adapter package(어댑터 패키지):", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run287C_report", f"- run287C_report(287C 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage288_open", f"- stage288_open(288단계 개방): `{STAGE288_ID}`")
    write_md(SELECTED287, selected)

    review_index = io_path(REVIEW_INDEX287).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run287C_report",
        f"- run287C_report(287C 보고서): `{rel(REPORT)}`\n- run287C_scoreboard(287C 점수판): `{rel(SCOREBOARD)}`\n- run287C_failure_memory(287C 실패 기억): `{rel(FAILURE_MEMORY)}`",
    )
    write_md(REVIEW_INDEX287, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage288_risk_reward_exit_asymmetry_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE288_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run287C_summary",
        f"- run287C_summary(287C 요약): Stage287(287단계)은 density/profit seed(밀도/수익 씨앗)를 찾았지만 efficiency/curve gate(효율/곡선 게이트) 실패로 후보 없이 닫고 Stage288(288단계)을 열었다. Effect(효과): Adapter/ONNX(어댑터/온엑스)는 진행하지 않고 risk/reward/exit surface(위험/보상/청산 표면)를 새 질문으로 넘긴다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE288_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage287(287단계) run287C(287C 실행) density scale curve pocket review(밀도/규모/곡선 포켓 검토) `{RUN_ID}` closed Stage287 and opened Stage288(288단계). "
        f"Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 없고 next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run287C Density scale curve pocket review(287C 밀도/규모/곡선 포켓 검토)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): Stage287(287단계)을 selected candidate(선택 후보) 없이 닫고 Stage288(288단계)을 열었다.\n"
        f"- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST288-RISK-REWARD-EXIT-ASYMMETRY",
        f"| `IDEA-ST288-RISK-REWARD-EXIT-ASYMMETRY` | `{STAGE288_ID}` | ATR SL/TP + exit overlay + model risk sizing(ATR 손절/익절 + 청산 오버레이 + 모델 위험 크기) | `Tier A used + Tier B fallback stress + actual routed total` | `opened` | Stage287(287단계) density/profit seed(밀도/수익 씨앗)의 효율/곡선 실패를 risk/reward/exit surface(위험/보상/청산 표면)로 다시 실험한다. |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST287-DENSITY-SCALE-CURVE-POCKET",
        f"| `NEG-ST287-DENSITY-SCALE-CURVE-POCKET` | `{STAGE287_ID}` | `{RUN_ID}` | density/profit seed found but no candidate(밀도/수익 씨앗은 있으나 후보 없음) | efficiency/curve gate failed(효율/곡선 게이트 실패) | reopen only with risk/reward/exit surface(위험/보상/청산 표면으로만 재개) |",
    )
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    created_at = utc_now()
    outputs = build_outputs()
    artifacts = write_outputs(*outputs, created_at=created_at)
    scoreboard_rows, _, _, _, _, _, failure_rows, queue_rows = outputs
    update_registers_and_docs(created_at, artifacts, scoreboard_rows, failure_rows, queue_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "scoreboard_rows": len(scoreboard_rows),
                "failure_rows": len(failure_rows),
                "stage288_seed_count": len(queue_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
