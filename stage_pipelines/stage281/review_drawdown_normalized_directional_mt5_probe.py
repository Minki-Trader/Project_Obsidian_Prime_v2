from __future__ import annotations

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


STAGE281_ID = "281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild"
STAGE282_ID = "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild"
RUN_ID = "run281C_review_drawdown_normalized_directional_mt5_probe_v1"
SOURCE_RUN_ID = "run281B_drawdown_normalized_directional_mt5_probe_v1"
STATUS = "completed_drawdown_normalized_directional_probe_review_no_candidate_selection_stage282_opened"
JUDGMENT = "drawdown_normalized_directional_rebuild_failed_validation_stability_no_candidate_selection"
NEXT_ACTION = "run282A_design_validation_first_asymmetric_confirmation_candidate_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE281 = ROOT / "stages" / STAGE281_ID
RUN281A = STAGE281 / "02_runs" / "run281A"
RUN281B = STAGE281 / "02_runs" / "run281B"
RUN_DIR = STAGE281 / "02_runs" / "run281C"
REVIEWS281 = STAGE281 / "03_reviews"
SELECTED281 = STAGE281 / "04_selected" / "selection_status.md"
REVIEW_INDEX281 = REVIEWS281 / "review_index.md"
STAGE_LEDGER281 = REVIEWS281 / "stage_run_ledger.csv"

SOURCE_BRANCH_QUEUE = RUN281A / "branch_design_queue.csv"
SOURCE_MANIFEST = RUN281A / "candidate_payload_manifest.csv"
SOURCE_EXECUTION = RUN281B / "execution_result.json"
SOURCE_KPI = RUN281B / "mt5_kpi_summary.csv"
SOURCE_RUN_MANIFEST = RUN281B / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage281/review_drawdown_normalized_directional_mt5_probe.py")
TERMINAL_ROOT = ROOT.parents[2]

SCOREBOARD = RUN_DIR / "probe_review_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
TRADE_QUALITY = RUN_DIR / "trade_quality_summary.csv"
CURVE = RUN_DIR / "curve_stability_summary.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
REBUILD_QUEUE = RUN_DIR / "stage282_seed_thesis_queue.csv"
RECEIPT = RUN_DIR / "probe_review_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS281 / "run281C_probe_review_stage282_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage281_closeout_stage282_validation_first_rebuild_open.md"

STAGE282 = ROOT / "stages" / STAGE282_ID
SPEC282 = STAGE282 / "00_spec" / "stage_brief.md"
INPUTS282 = STAGE282 / "01_inputs"
REVIEWS282 = STAGE282 / "03_reviews"
SELECTED282 = STAGE282 / "04_selected" / "selection_status.md"
STAGE_LEDGER282 = REVIEWS282 / "stage_run_ledger.csv"
REVIEW_INDEX282 = REVIEWS282 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "source_payload",
    "validation_net_profit",
    "validation_pf",
    "validation_trade_count",
    "validation_dd",
    "validation_recovery",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_dd",
    "oos_recovery",
    "tier_b_validation_net_profit",
    "tier_b_validation_pf",
    "tier_b_oos_net_profit",
    "validation_worst_month_net",
    "oos_worst_month_net",
    "validation_worst_session_net",
    "oos_worst_session_net",
    "validation_max_losing_streak",
    "oos_max_losing_streak",
    "validation_top_10pct_contribution_share",
    "oos_top_10pct_contribution_share",
    "review_label",
    "failure_reasons",
    "salvage_value",
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
REBUILD_COLUMNS = (
    "stage282_seed_id",
    "fresh_thesis",
    "source_failure_memory",
    "candidate_construction",
    "feature_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "success_criteria",
    "failure_criteria",
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


def load_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def attempt_role_key(tier_scope: str, attempt_role: str) -> str:
    if tier_scope == "Tier A+B" or attempt_role == "actual_routed_total":
        return "actual_routed"
    if tier_scope == "Tier A":
        return "tier_a"
    if tier_scope == "Tier B":
        return "tier_b"
    return str(tier_scope).lower().replace(" ", "_")


def parse_kpi_records() -> dict[tuple[str, str, str], dict[str, Any]]:
    execution = load_json(SOURCE_EXECUTION)
    attempt_meta = {
        str(item.get("attempt_name", "")): dict(item)
        for item in execution.get("execution_results", [])
        if item.get("attempt_name")
    }
    records: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in read_csv_dicts(SOURCE_KPI):
        report = json.loads(row.get("report") or "{}")
        metrics = json.loads(row.get("metrics") or "{}")
        attempt_name = str(report.get("attempt_name", ""))
        meta = attempt_meta.get(attempt_name, {})
        materialized_id = str(meta.get("materialized_branch_id", attempt_name))
        tier_scope = str(row.get("tier_scope", meta.get("tier", "")))
        split = str(row.get("split", meta.get("split", "")))
        role = attempt_role_key(tier_scope, str(row.get("route_role", meta.get("attempt_role", ""))))
        report_path = resolve_report_path(str(metrics.get("report_path", "")), report)
        records[(materialized_id, role, split)] = {
            "record_view": row.get("record_view", ""),
            "tier_scope": tier_scope,
            "route_role": row.get("route_role", meta.get("attempt_role", "")),
            "split": split,
            "metrics": metrics,
            "report_path": report_path,
        }
    return records


def resolve_report_path(path_text: str, report: Mapping[str, Any]) -> Path:
    path = Path(path_text)
    if path_text and path_exists(path):
        return path
    html_report = report.get("html_report", {}) if isinstance(report, Mapping) else {}
    if isinstance(html_report, Mapping):
        for key in ("path", "source_path"):
            candidate_text = str(html_report.get(key, ""))
            candidate = Path(candidate_text)
            if candidate_text and path_exists(candidate):
                return candidate
    if path.name:
        fallback = TERMINAL_ROOT / path.name
        if path_exists(fallback):
            return fallback
    return path


def metric(records: Mapping[tuple[str, str, str], Mapping[str, Any]], materialized_id: str, role: str, split: str, key: str) -> float:
    entry = records.get((materialized_id, role, split), {})
    metrics = entry.get("metrics", {}) if isinstance(entry, Mapping) else {}
    return safe_float(metrics.get(key))


def worst_bucket_net(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str) -> float:
    values = [
        safe_float(row.get("net_profit"))
        for row in rows
        if row.get("materialized_branch_id") == materialized_id
        and row.get("tier_scope") == tier_scope
        and row.get("split") == split
    ]
    return min(values) if values else 0.0


def quality_value(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str, key: str) -> float:
    for row in rows:
        if row.get("materialized_branch_id") == materialized_id and row.get("tier_scope") == tier_scope and row.get("split") == split:
            return safe_float(row.get(key))
    return 0.0


def build_rebuild_queue(failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    source_failures = ";".join(str(row.get("materialized_branch_id", "")) for row in failure_rows)
    return [
        {
            "stage282_seed_id": "cp282A_validation_recovery_floor_direction_surface",
            "fresh_thesis": "Validation-first recovery floor before OOS scale.",
            "source_failure_memory": source_failures,
            "candidate_construction": "Reject any direction signal until validation-like recovery and PF gates agree with the route source.",
            "feature_surface": "route_signal_value plus validation-recovery proxy, ATR compression, DI spread, and return pressure state.",
            "decision_surface": "long/short only when direction agrees with trend and recovery proxy; otherwise flat.",
            "risk_logic": "Drawdown-normalized entry budget with hard flat state during high pressure clusters.",
            "adapter_path": "Candidate package must expose feature order, route diagnostics, recovery gate, and risk state.",
            "runtime_handoff": "MT5 signal replay first, Adapter package later only if stability survives.",
            "success_criteria": "Validation net positive, PF >= 1.12, recovery >= 0.35, OOS PF >= 1.20, trade count >= 80.",
            "failure_criteria": "Validation recovery below 0.25, negative Tier B fallback, or month/session concentration persists.",
            "claim_boundary": BOUNDARY,
        },
        {
            "stage282_seed_id": "cp282B_session_loss_asymmetry_surface",
            "fresh_thesis": "Session-specific loss asymmetry is a decision surface, not a post-hoc filter.",
            "source_failure_memory": source_failures,
            "candidate_construction": "Build separate session risk states and allow direction only where session expectancy is not structurally negative.",
            "feature_surface": "session bucket, DI spread, ATR ratio, route signal, and recent adverse excursion proxy.",
            "decision_surface": "route_signal_value is gated by session loss state and direction concordance.",
            "risk_logic": "Position stays flat in weak session states; no threshold repair loop is allowed.",
            "adapter_path": "Adapter schema must preserve session state and risk reason.",
            "runtime_handoff": "One-table signal replay is acceptable only as a pressure probe.",
            "success_criteria": "Worst session improves above -80 while validation/OOS stay positive.",
            "failure_criteria": "One session still carries most loss or OOS edge collapses below PF 1.10.",
            "claim_boundary": BOUNDARY,
        },
        {
            "stage282_seed_id": "cp282C_concentration_penalty_confirmation_surface",
            "fresh_thesis": "Top-month and top-trade concentration must be penalized inside construction.",
            "source_failure_memory": source_failures,
            "candidate_construction": "Use a concentration penalty state so signals that only work through clustered wins are demoted before MT5.",
            "feature_surface": "rolling signal density, rolling win/loss pressure proxy, route signal, and volatility band state.",
            "decision_surface": "direction requires low concentration pressure plus trend confirmation.",
            "risk_logic": "Reduce clustered re-entry after large wins or loss bursts to avoid fragile equity curves.",
            "adapter_path": "Adapter must expose concentration penalty input and output reason.",
            "runtime_handoff": "MT5 replay must record Tier A used, Tier B fallback stress, and actual routed total.",
            "success_criteria": "Top 10 percent contribution share below 1.80 with validation recovery >= 0.35.",
            "failure_criteria": "Net relies on one month or top trade cluster after review.",
            "claim_boundary": BOUNDARY,
        },
        {
            "stage282_seed_id": "cp282D_macro_trend_countercheck_surface",
            "fresh_thesis": "Macro trend agreement needs a countercheck that protects validation, not only OOS upside.",
            "source_failure_memory": source_failures,
            "candidate_construction": "Rebuild macro/trend concordance with a validation-side countercheck for weak-month states.",
            "feature_surface": "macro spread, DI spread, RSI slope, ATR ratio, route signal, and return pressure.",
            "decision_surface": "direction only when macro and local trend agree or weak-month state is flat.",
            "risk_logic": "Preserve OOS upside only after validation loss concentration is reduced.",
            "adapter_path": "Adapter path must make macro/local trend provenance traceable.",
            "runtime_handoff": "No ONNX step until package and runtime handoff are traceable.",
            "success_criteria": "Validation PF >= 1.12, Tier B validation positive, OOS net >= 150.",
            "failure_criteria": "Validation PF remains near 1.0 or Tier B fallback is weaker than Tier A.",
            "claim_boundary": BOUNDARY,
        },
    ]


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    branch_rows = read_csv_dicts(SOURCE_BRANCH_QUEUE)
    records = parse_kpi_records()
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []

    for branch in branch_rows:
        materialized_id = branch["materialized_branch_id"]
        package_id = branch["package_id"]
        for role, tier_scope in (("actual_routed", "Tier A+B"), ("tier_a", "Tier A"), ("tier_b", "Tier B")):
            for split in ("validation_is", "oos"):
                entry = records.get((materialized_id, role, split))
                if not entry:
                    continue
                report_path = Path(str(entry.get("report_path", "")))
                frame = trade_frame(report_path)
                monthly_rows.extend(
                    attribution_rows(
                        frame,
                        materialized_id=materialized_id,
                        seed_role=package_id,
                        tier_scope=tier_scope,
                        split=split,
                        source_report_path=report_path,
                        bucket_column="month",
                    )
                )
                session_rows.extend(
                    attribution_rows(
                        frame,
                        materialized_id=materialized_id,
                        seed_role=package_id,
                        tier_scope=tier_scope,
                        split=split,
                        source_report_path=report_path,
                        bucket_column="session",
                    )
                )
                q = quality_summary(frame)
                quality_rows.append(
                    {
                        "materialized_branch_id": materialized_id,
                        "seed_role": package_id,
                        "tier_scope": tier_scope,
                        "split": split,
                        **q,
                        "source_report_path": report_path.as_posix(),
                    }
                )
                profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
                curve_rows.append(
                    {
                        "materialized_branch_id": materialized_id,
                        "seed_role": package_id,
                        "tier_scope": tier_scope,
                        "split": split,
                        **drawdown_stats(profits),
                        "source_report_path": report_path.as_posix(),
                    }
                )

    scoreboard_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for branch in branch_rows:
        materialized_id = branch["materialized_branch_id"]
        package_id = branch["package_id"]
        validation_net = metric(records, materialized_id, "actual_routed", "validation_is", "net_profit")
        validation_pf = metric(records, materialized_id, "actual_routed", "validation_is", "profit_factor")
        validation_trades = int(metric(records, materialized_id, "actual_routed", "validation_is", "trade_count"))
        validation_dd = metric(records, materialized_id, "actual_routed", "validation_is", "max_drawdown_amount")
        validation_recovery = metric(records, materialized_id, "actual_routed", "validation_is", "recovery_factor")
        oos_net = metric(records, materialized_id, "actual_routed", "oos", "net_profit")
        oos_pf = metric(records, materialized_id, "actual_routed", "oos", "profit_factor")
        oos_trades = int(metric(records, materialized_id, "actual_routed", "oos", "trade_count"))
        oos_dd = metric(records, materialized_id, "actual_routed", "oos", "max_drawdown_amount")
        oos_recovery = metric(records, materialized_id, "actual_routed", "oos", "recovery_factor")
        tier_b_validation_net = metric(records, materialized_id, "tier_b", "validation_is", "net_profit")
        tier_b_validation_pf = metric(records, materialized_id, "tier_b", "validation_is", "profit_factor")
        tier_b_oos_net = metric(records, materialized_id, "tier_b", "oos", "net_profit")
        validation_worst_month = worst_bucket_net(monthly_rows, materialized_id, "Tier A+B", "validation_is")
        oos_worst_month = worst_bucket_net(monthly_rows, materialized_id, "Tier A+B", "oos")
        validation_worst_session = worst_bucket_net(session_rows, materialized_id, "Tier A+B", "validation_is")
        oos_worst_session = worst_bucket_net(session_rows, materialized_id, "Tier A+B", "oos")
        validation_streak = int(quality_value(quality_rows, materialized_id, "Tier A+B", "validation_is", "max_losing_streak_count"))
        oos_streak = int(quality_value(quality_rows, materialized_id, "Tier A+B", "oos", "max_losing_streak_count"))
        validation_top10 = quality_value(quality_rows, materialized_id, "Tier A+B", "validation_is", "top_10pct_contribution_share")
        oos_top10 = quality_value(quality_rows, materialized_id, "Tier A+B", "oos", "top_10pct_contribution_share")
        reasons: list[str] = []
        if validation_net <= 0:
            reasons.append("validation_net_not_positive")
        if validation_pf < 1.08:
            reasons.append("validation_pf_below_1_08")
        if validation_recovery < 0.30:
            reasons.append("validation_recovery_below_0_30")
        if validation_dd > max(validation_net, 1.0) * 4.0:
            reasons.append("validation_drawdown_too_large_vs_net")
        if tier_b_validation_net <= 0 or tier_b_validation_pf < 1.0:
            reasons.append("tier_b_validation_weak")
        if oos_pf < 1.10 or oos_trades < 70 or oos_recovery < 0.50:
            reasons.append("oos_guardrail_weak")
        if validation_worst_month < -100:
            reasons.append("validation_worst_month_below_minus_100")
        if validation_streak >= 7:
            reasons.append("validation_losing_streak_high")
        label = "failed_validation_stability_no_candidate" if reasons else "survivor_watch_requires_stage282_redesign"
        salvage = (
            "OOS upside survives but validation recovery is too weak; use only as failure memory for validation-first construction."
            if oos_net > 150 and oos_pf >= 1.20
            else "No package-level survival; retain as discard memory."
        )
        row = {
            "materialized_branch_id": materialized_id,
            "package_id": package_id,
            "source_payload": branch.get("source_payload", ""),
            "validation_net_profit": validation_net,
            "validation_pf": validation_pf,
            "validation_trade_count": validation_trades,
            "validation_dd": validation_dd,
            "validation_recovery": validation_recovery,
            "oos_net_profit": oos_net,
            "oos_pf": oos_pf,
            "oos_trade_count": oos_trades,
            "oos_dd": oos_dd,
            "oos_recovery": oos_recovery,
            "tier_b_validation_net_profit": tier_b_validation_net,
            "tier_b_validation_pf": tier_b_validation_pf,
            "tier_b_oos_net_profit": tier_b_oos_net,
            "validation_worst_month_net": validation_worst_month,
            "oos_worst_month_net": oos_worst_month,
            "validation_worst_session_net": validation_worst_session,
            "oos_worst_session_net": oos_worst_session,
            "validation_max_losing_streak": validation_streak,
            "oos_max_losing_streak": oos_streak,
            "validation_top_10pct_contribution_share": validation_top10,
            "oos_top_10pct_contribution_share": oos_top10,
            "review_label": label,
            "failure_reasons": ";".join(reasons),
            "salvage_value": salvage,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard_rows.append(row)
        failure_rows.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "failure_type": label,
                "failure_reasons": ";".join(reasons),
                "salvage_value": salvage,
                "reopen_condition": "Only a new validation-first construction may reuse this evidence; no direct repair branch.",
                "claim_boundary": BOUNDARY,
            }
        )
    rebuild_rows = build_rebuild_queue(failure_rows)
    return scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows, rebuild_rows


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


def stage282_spec_markdown(rebuild_rows: Sequence[Mapping[str, str]]) -> str:
    rows = "\n".join(f"- `{row['stage282_seed_id']}`: {row['fresh_thesis']}" for row in rebuild_rows)
    return f"""# Stage282 Brief(282단계 개요): Validation-First Asymmetric Confirmation Rebuild(검증 우선 비대칭 확인 재구성)

- canonical_stage_id(정식 단계 ID): `{STAGE282_ID}`
- single_question(단일 질문): Stage281(281단계)의 OOS(표본외) 상방은 살리되 validation(검증) 회복력과 약한 구간을 먼저 통과하는 새 후보 패키지를 만들 수 있는가?
- source_stage(원천 단계): `{STAGE281_ID}`
- source_run(원천 실행): `{RUN_ID}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Fresh Thesis(새 논제)

Stage281(281단계)은 OOS(표본외) 숫자는 강했지만 validation(검증) PF(수익 팩터), recovery(회복), drawdown(손실폭)이 약했다.
Effect(효과): Stage282(282단계)는 OOS(표본외)를 먼저 키우는 수리가 아니라 validation-first(검증 우선) 구조로 새 decision surface(판단 표면)를 만든다.

## Seed Queue(씨앗 대기열)

{rows}

## Boundary(경계)

`{BOUNDARY}`
"""


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], rebuild_rows: Sequence[Mapping[str, str]]) -> str:
    lines = [
        "# run281C Report(281C 보고서): Drawdown-Normalized Directional Probe Review(손실폭 정규화 방향 탐침 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- branch_count(분기 수): `{len(scoreboard_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Scoreboard(점수판)",
        "",
        "| branch(분기) | val net(검증 순수익) | val PF(검증 수익 팩터) | val recovery(검증 회복) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | label(라벨) |",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {branch} | {vnet:.2f} | {vpf:.2f} | {vrec:.2f} | {onet:.2f} | {opf:.2f} | {label} |".format(
                branch=row["materialized_branch_id"],
                vnet=safe_float(row["validation_net_profit"]),
                vpf=safe_float(row["validation_pf"]),
                vrec=safe_float(row["validation_recovery"]),
                onet=safe_float(row["oos_net_profit"]),
                opf=safe_float(row["oos_pf"]),
                label=row["review_label"],
            )
        )
    lines.extend(
        [
            "",
            "## Stage282 Queue(282단계 대기열)",
            "",
        ]
    )
    for row in rebuild_rows:
        lines.append(f"- `{row['stage282_seed_id']}`: {row['fresh_thesis']}")
    lines.extend(
        [
            "",
            "## Meaning(의미)",
            "",
            "Stage281(281단계)은 OOS(표본외) 상방을 다시 보였지만 validation(검증) 회복력이 후보 패키지 기준에 닿지 않았다.",
            "Effect(효과): 이 분기는 선택 후보로 부르지 않고, Stage282(282단계)에서 validation-first(검증 우선) 후보 구성을 새 질문으로 연다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def write_stage282_inputs(rebuild_rows: Sequence[Mapping[str, str]]) -> None:
    for path in (SPEC282.parent, INPUTS282, REVIEWS282, SELECTED282.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(SPEC282, stage282_spec_markdown(rebuild_rows))
    write_csv(INPUTS282 / "stage281_failure_memory.csv", FAILURE_COLUMNS, read_csv_dicts(FAILURE_MEMORY))
    write_csv(INPUTS282 / "stage282_seed_thesis_queue.csv", REBUILD_COLUMNS, rebuild_rows)
    write_md(
        INPUTS282 / "input_refs.md",
        f"""# Stage282 Input References(282단계 입력 참조)

- source_review(원천 검토): `{rel(REPORT)}`
- source_scoreboard(원천 점수판): `{rel(SCOREBOARD)}`
- source_failure_memory(원천 실패 기억): `{rel(FAILURE_MEMORY)}`
- seed_thesis_queue(씨앗 논제 대기열): `{rel(INPUTS282 / 'stage282_seed_thesis_queue.csv')}`

Effect(효과): Stage281(281단계)의 후보명은 보존하지 않고, 실패 기억과 새 논제만 Stage282(282단계)로 넘긴다.
""",
    )
    write_md(
        SELECTED282,
        f"""# Stage282 Selection Status(282단계 선택 상태)

- stage_status(단계 상태): `opened_validation_first_asymmetric_confirmation_rebuild_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage282_validation_first_asymmetric_confirmation_rebuild_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE281_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUTS282 / 'input_refs.md')}`
""",
    )
    write_md(
        REVIEW_INDEX282,
        f"""# Stage282 Review Index(282단계 검토 색인)

- stage_brief(단계 개요): `{rel(SPEC282)}`
- input_refs(입력 참조): `{rel(INPUTS282 / 'input_refs.md')}`
""",
    )
    write_csv(
        STAGE_LEDGER282,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage282_open",
                "stage_id": STAGE282_ID,
                "run_id": RUN_ID,
                "view": "stage282_open_validation_first_rebuild",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_no_candidate_selection",
                "judgment": JUDGMENT,
                "evidence_boundary": "stage_open_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_outputs(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    quality_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    rebuild_rows: Sequence[Mapping[str, str]],
    created_at: str,
) -> list[Path]:
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(TRADE_QUALITY, TRADE_QUALITY_COLUMNS, quality_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(REBUILD_QUEUE, REBUILD_COLUMNS, rebuild_rows)
    write_json(
        RECEIPT,
        {
            "run_id": RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "branch_count": len(scoreboard_rows),
            "monthly_rows": len(monthly_rows),
            "session_rows": len(session_rows),
            "trade_quality_rows": len(quality_rows),
            "curve_rows": len(curve_rows),
            "failure_rows": len(failure_rows),
            "stage282_seed_rows": len(rebuild_rows),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "judgment": JUDGMENT,
            "next_action": NEXT_ACTION,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"branches={len(scoreboard_rows)};monthly_rows={len(monthly_rows)};session_rows={len(session_rows)};trade_quality_rows={len(quality_rows)};curve_rows={len(curve_rows)}",
                "evidence_missing": "selected candidate package;Adapter package;ONNX parity;MT5 ONNX runtime reproduction",
                "judgment_label": JUDGMENT,
                "judgment_class": "negative_valid_runtime_probe_review",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "OOS 상방은 있지만 검증 회복력이 약해 후보 선택 없이 새 논제로 넘어간다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "mt5_kpi_and_trade_reports_available(MT5 KPI와 거래 보고 사용 가능)",
                "status": "passed",
                "evidence_path": f"{rel(SOURCE_KPI)};{rel(TRADE_QUALITY)}",
                "effect": "숫자와 거래 목록을 함께 읽어 후보 생존 여부를 판단한다.",
            },
            {
                "gate_name": "no_candidate_no_onnx_claim(후보와 온엑스 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "선택 후보, 어댑터 패키지, 온엑스 준비를 주장하지 않는다.",
            },
            {
                "gate_name": "fresh_thesis_stage282_opened(새 논제 282단계 개방)",
                "status": "passed",
                "evidence_path": rel(REBUILD_QUEUE),
                "effect": "동일 수리 반복이 아니라 검증 우선 비대칭 확인 구조로 질문을 바꾼다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, rebuild_rows))
    write_md(
        DECISION,
        f"""# Decision(결정): Stage281 Closeout and Stage282 Open(281단계 종료와 282단계 개방)

- date(날짜): `{UPDATED_ON}`
- decision(결정): Stage281(281단계)은 선택 후보 없이 닫고 Stage282(282단계)를 validation-first asymmetric confirmation rebuild(검증 우선 비대칭 확인 재구성)로 연다.
- effect(효과): OOS(표본외) 상방만으로 후보를 고르지 않고, validation(검증) 회복력을 먼저 통과하는 새 후보 패키지를 만든다.
- source(원천): `{rel(REPORT)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage282_inputs(rebuild_rows)
    artifacts = [
        SCOREBOARD,
        MONTHLY,
        SESSION,
        TRADE_QUALITY,
        CURVE,
        FAILURE_MEMORY,
        REBUILD_QUEUE,
        RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC282,
        INPUTS282 / "stage281_failure_memory.csv",
        INPUTS282 / "stage282_seed_thesis_queue.csv",
        INPUTS282 / "input_refs.md",
        SELECTED282,
        STAGE_LEDGER282,
        REVIEW_INDEX282,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE281_ID,
        "target_stage_id": STAGE282_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    lineage = {
        "run_id": RUN_ID,
        "source_inputs": [rel(SOURCE_BRANCH_QUEUE), rel(SOURCE_MANIFEST), rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_RUN_MANIFEST), rel(ROOT / PRODUCER)],
        "source_hashes": {
            rel(path): sha256_file(path)
            for path in [SOURCE_BRANCH_QUEUE, SOURCE_MANIFEST, SOURCE_EXECUTION, SOURCE_KPI, SOURCE_RUN_MANIFEST, ROOT / PRODUCER]
            if path_exists(path)
        },
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "lineage_judgment": "connected_with_boundary_no_candidate_no_onnx_claim",
    }
    write_json(LINEAGE, lineage)
    artifacts.append(LINEAGE)
    return artifacts


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], rebuild_rows: Sequence[Mapping[str, str]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE281_ID,
                "lane": "drawdown_normalized_directional_probe_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branches={len(scoreboard_rows)};target_stage={STAGE282_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__probe_review",
                "stage_id": STAGE281_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage281_probe_review_stage282_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "stage281_probe_review(281단계 탐침 검토)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "monthly_session_curve_trade_quality_no_candidate_selection",
                "scoreboard_lane": "probe_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"branches={len(scoreboard_rows)};failure_rows={len(failure_rows)}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "mt5_trade_reports_parsed",
                "notes": f"target_stage={STAGE282_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER281,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage281_closeout",
                "stage_id": STAGE281_ID,
                "run_id": RUN_ID,
                "view": "stage281_probe_review_stage282_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "probe_review_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"target_stage={STAGE282_ID};next_action={NEXT_ACTION}.",
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage281_probe_review_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE281_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run281C probe review(281C 탐침 검토)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED281).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run281C_report", f"- run281C_report(281C 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage282_open", f"- stage282_open(282단계 개방): `{STAGE282_ID}`")
    write_md(SELECTED281, selected)

    review_index = io_path(REVIEW_INDEX281).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX281) else "# Stage281 Review Index(281단계 검토 색인)\n"
    review_index = append_once(review_index, "run281C_report", f"- run281C_report(281C 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX281, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage282_validation_first_asymmetric_confirmation_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE282_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE281_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `validation_first_asymmetric_confirmation_rebuild`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_validation_first_asymmetric_confirmation_rebuild_no_candidate_selection`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run281C_summary",
        f"- run281C_summary(281C 요약): Stage281(281단계)의 MT5 탐침 `{len(scoreboard_rows)}`개 분기를 검토하고 선택 후보 없이 Stage282(282단계)를 열었다. Effect(효과): OOS(표본외) 상방은 실패 기억으로만 쓰고 validation-first(검증 우선) 후보 구성을 새 질문으로 넘긴다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE282_ID}")
    focus = (
        f"- >-\n"
        f"  Stage282(282단계) validation-first asymmetric confirmation rebuild(검증 우선 비대칭 확인 재구성) opened by `{RUN_ID}`. "
        f"Effect(효과): Stage281(281단계) OOS(표본외) 상방을 선택 후보로 고르지 않고 새 candidate package(후보 패키지) 구성 질문으로 바꾼다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run281C Stage281 probe review(281C 281단계 탐침 검토)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): branch(분기) `{len(scoreboard_rows)}`개를 실패 기억으로 닫고 Stage282(282단계) seed(씨앗) `{len(rebuild_rows)}`개를 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST282-VALIDATION-FIRST-ASYMMETRIC-CONFIRMATION",
        f"| `IDEA-ST282-VALIDATION-FIRST-ASYMMETRIC-CONFIRMATION` | `{STAGE282_ID}` | validation-first asymmetric confirmation(검증 우선 비대칭 확인) | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `opened_no_candidate` | Stage281(281단계)의 OOS(표본외) 상방 착시를 막고 검증 회복력을 먼저 요구한다. |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST281-DRAWDOWN-NORMALIZED-DIRECTION",
        f"| `NEG-ST281-DRAWDOWN-NORMALIZED-DIRECTION` | `{STAGE281_ID}` | drawdown-normalized directional rebuild(손실폭 정규화 방향 재구성)이 validation(검증) 회복력 기준을 통과하지 못함 | OOS(표본외) 상방은 후보 선택 근거가 아니라 Stage282(282단계) 새 논제 입력으로만 사용 | `{rel(FAILURE_MEMORY)}` |",
    )
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS281).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows, rebuild_rows = build_outputs()
    artifacts = write_outputs(scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows, rebuild_rows, created_at)
    update_registers_and_docs(created_at, artifacts, scoreboard_rows, failure_rows, rebuild_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "branch_count": len(scoreboard_rows),
                "failure_memory_count": len(failure_rows),
                "stage282_seed_count": len(rebuild_rows),
                "monthly_rows": len(monthly_rows),
                "session_rows": len(session_rows),
                "trade_quality_rows": len(quality_rows),
                "curve_rows": len(curve_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "target_stage": STAGE282_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
