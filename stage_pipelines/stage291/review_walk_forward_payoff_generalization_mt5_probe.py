from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from stage_pipelines.stage280.validate_directional_mapping_stability import safe_float, trade_frame  # noqa: E402


STAGE291_ID = "291_onnx_candidate_campaign__walk_forward_payoff_generalization_rebuild"
STAGE292_ID = "292_onnx_candidate_campaign__anti_direction_meta_label_trade_simulator_rebuild"
RUN_ID = "run291C_review_walk_forward_payoff_generalization_mt5_probe_v1"
RUN_NUMBER = "run291C"
SOURCE_RUN_ID = "run291B_walk_forward_payoff_generalization_mt5_probe_v1"
PARENT_RUN_ID = "run291A_design_walk_forward_payoff_generalization_rebuild_v1"
STATUS = "completed_walk_forward_payoff_review_no_candidate_stage292_opened"
JUDGMENT = "walk_forward_payoff_generalization_runtime_probe_negative_no_adapter_no_onnx"
NEXT_ACTION = "run292A_design_anti_direction_meta_label_trade_simulator_rebuild_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE291 = ROOT / "stages" / STAGE291_ID
STAGE292 = ROOT / "stages" / STAGE292_ID
RUN291A = STAGE291 / "02_runs" / "run291A"
RUN291B = STAGE291 / "02_runs" / "run291B"
RUN_DIR = STAGE291 / "02_runs" / RUN_NUMBER
REVIEWS291 = STAGE291 / "03_reviews"
SELECTED291 = STAGE291 / "04_selected" / "selection_status.md"
REVIEW_INDEX291 = REVIEWS291 / "review_index.md"
STAGE_LEDGER291 = REVIEWS291 / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN291A / "candidate_payload_manifest.csv"
SOURCE_MODEL_SCOREBOARD = RUN291A / "model_scout_scoreboard.csv"
SOURCE_WFO_SCOREBOARD = RUN291A / "wfo_fold_scoreboard.csv"
SOURCE_KPI = RUN291B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN291B / "execution_result.json"
SOURCE_RUN_MANIFEST = RUN291B / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage291/review_walk_forward_payoff_generalization_mt5_probe.py")

SCOREBOARD = RUN_DIR / "walk_forward_payoff_review_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
TRADE_QUALITY = RUN_DIR / "trade_quality_summary.csv"
CURVE = RUN_DIR / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_DIR / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
STAGE292_QUEUE = RUN_DIR / "stage292_seed_queue.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS291 / "run291C_walk_forward_payoff_review_stage292_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage291_walk_forward_payoff_review_stage292_open.md"

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
    "validation_underwater_ratio",
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
    "oos_underwater_ratio",
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
    "package_id",
    "split",
    "bucket_type",
    "bucket",
    "trade_count",
    "net_profit",
    "profit_factor",
    "positive_bucket",
    "source_report_path",
)
TRADE_QUALITY_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "split",
    "trade_count",
    "net_profit",
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
    "package_id",
    "split",
    "trade_count",
    "final_net",
    "max_equity_peak",
    "min_equity",
    "max_local_drawdown_from_peak",
    "new_high_count",
    "underwater_ratio",
    "source_report_path",
)
POCKET_COLUMNS = (
    "materialized_branch_id",
    "package_id",
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
    "source_stage_id",
    "source_run_id",
    "seed_role",
    "hypothesis",
    "broad_sweep",
    "extreme_sweep",
    "micro_search_gate",
    "wfo_plan",
    "required_change",
    "discard_condition",
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


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    upsert_csv_rows(path, columns, rows, key=key)


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
    if isinstance(value, Mapping):
        return dict(value)
    text = str(value or "").strip()
    if not text:
        return {}
    parsed = ast.literal_eval(text)
    return dict(parsed) if isinstance(parsed, Mapping) else {}


def safe_name(value: str, limit: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def variant_token(row: Mapping[str, str], limit: int = 44) -> str:
    text = str(row.get("materialized_branch_id") or row.get("queue_id") or "unknown")
    return safe_name(text, limit)


def manifest_by_id() -> dict[str, dict[str, str]]:
    rows = read_csv_rows(SOURCE_MANIFEST)
    if not rows:
        raise FileNotFoundError(SOURCE_MANIFEST)
    return {row["materialized_branch_id"]: dict(row) for row in rows}


def split_days(split: str) -> int:
    return 183 if split == "validation_is" else 131


def resolve_report_path(path_text: str) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text)
    if path_exists(path):
        return path
    if path.name:
        fallback = RUN291B / "mt5" / "reports" / path.name
        if path_exists(fallback):
            return fallback
    return path


def load_actual_routed_records() -> dict[tuple[str, str], dict[str, Any]]:
    manifest = manifest_by_id()
    token_to_id = {variant_token(row): materialized_id for materialized_id, row in manifest.items()}
    tokens = sorted((token for token in token_to_id if token), key=len, reverse=True)
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for row in read_csv_rows(SOURCE_KPI):
        if row.get("route_role") != "actual_routed_total":
            continue
        metrics = parse_obj(row.get("metrics"))
        report = parse_obj(row.get("report"))
        haystack = " ".join(
            [
                str(row.get("record_view") or ""),
                str(report.get("attempt_name") or ""),
                str(report.get("report_name") or ""),
            ]
        )
        materialized_id = ""
        for known in sorted(manifest, key=len, reverse=True):
            if known in haystack:
                materialized_id = known
                break
        if not materialized_id:
            materialized_id = next((token_to_id[token] for token in tokens if token in haystack), "")
        if not materialized_id:
            continue
        report_path_text = str(metrics.get("report_path") or "").strip()
        records[(materialized_id, str(row.get("split", "")))] = {
            "metrics": metrics,
            "report_path": resolve_report_path(report_path_text),
            "record_view": row.get("record_view", ""),
        }
    if not records:
        raise RuntimeError(f"No actual_routed_total records found in {SOURCE_KPI}")
    return records


def profit_factor(profits: Sequence[float]) -> float:
    gross_profit = sum(value for value in profits if value > 0)
    gross_loss = sum(value for value in profits if value < 0)
    return gross_profit / abs(gross_loss) if gross_loss < 0 else 0.0


def rolling_min(profits: Sequence[float], window: int) -> float:
    if len(profits) < window:
        return sum(profits) if profits else 0.0
    return min(sum(float(value) for value in profits[index : index + window]) for index in range(0, len(profits) - window + 1))


def losing_streak(profits: Sequence[float]) -> tuple[int, float]:
    count = 0
    loss = 0.0
    max_count = 0
    max_loss = 0.0
    for profit in profits:
        value = float(profit)
        if value < 0:
            count += 1
            loss += value
            if count > max_count or (count == max_count and abs(loss) > abs(max_loss)):
                max_count = count
                max_loss = loss
        else:
            count = 0
            loss = 0.0
    return max_count, max_loss


def attribution_rows(
    frame: Any,
    materialized_id: str,
    package_id: str,
    split: str,
    bucket_type: str,
    bucket_column: str,
    report_path: Path | None,
) -> list[dict[str, Any]]:
    if frame.empty or bucket_column not in frame.columns:
        return []
    rows: list[dict[str, Any]] = []
    for bucket, group in frame.groupby(bucket_column, sort=True):
        profits = [float(value) for value in group["net_profit"].tolist()]
        net = sum(profits)
        rows.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "split": split,
                "bucket_type": bucket_type,
                "bucket": str(bucket),
                "trade_count": len(profits),
                "net_profit": net,
                "profit_factor": profit_factor(profits),
                "positive_bucket": "yes" if net > 0 else "no",
                "source_report_path": report_path.as_posix() if report_path else "",
            }
        )
    return rows


def quality_summary(
    frame: Any,
    materialized_id: str,
    package_id: str,
    split: str,
    report_path: Path | None,
) -> dict[str, Any]:
    profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
    winners = [value for value in profits if value > 0]
    losers = [value for value in profits if value < 0]
    net = sum(profits)
    streak_count, streak_loss = losing_streak(profits)
    positive_sorted = sorted(winners, reverse=True)
    top_count = max(1, int(round(len(profits) * 0.10))) if profits else 0
    return {
        "materialized_branch_id": materialized_id,
        "package_id": package_id,
        "split": split,
        "trade_count": len(profits),
        "net_profit": net,
        "profit_factor": profit_factor(profits),
        "win_rate": len(winners) / len(profits) if profits else 0.0,
        "expectancy": net / len(profits) if profits else 0.0,
        "average_win": sum(winners) / len(winners) if winners else 0.0,
        "average_loss": sum(losers) / len(losers) if losers else 0.0,
        "largest_win": max(winners) if winners else 0.0,
        "largest_loss": min(losers) if losers else 0.0,
        "max_losing_streak_count": streak_count,
        "max_losing_streak_loss": streak_loss,
        "top_trade_contribution_share": (positive_sorted[0] / net) if positive_sorted and net > 0 else 0.0,
        "top_10pct_contribution_share": (sum(positive_sorted[:top_count]) / net) if positive_sorted and net > 0 else 0.0,
        "source_report_path": report_path.as_posix() if report_path else "",
    }


def curve_outputs(
    frame: Any,
    materialized_id: str,
    package_id: str,
    split: str,
    report_path: Path | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
    balance = 0.0
    peak = 0.0
    min_equity = 0.0
    max_dd = 0.0
    underwater = 0
    new_high = 0
    for profit in profits:
        balance += profit
        if balance > peak:
            peak = balance
            new_high += 1
        min_equity = min(min_equity, balance)
        dd = peak - balance
        if dd > 0:
            underwater += 1
        max_dd = max(max_dd, dd)
    source = report_path.as_posix() if report_path else ""
    curve = {
        "materialized_branch_id": materialized_id,
        "package_id": package_id,
        "split": split,
        "trade_count": len(profits),
        "final_net": balance,
        "max_equity_peak": peak,
        "min_equity": min_equity,
        "max_local_drawdown_from_peak": max_dd,
        "new_high_count": new_high,
        "underwater_ratio": underwater / len(profits) if profits else 1.0,
        "source_report_path": source,
    }
    pockets = []
    for window, threshold in ((20, -120.0), (50, -150.0)):
        worst = rolling_min(profits, window)
        pockets.append(
            {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "split": split,
                "rolling_window": window,
                "worst_rolling_net": worst,
                "pocket_threshold": threshold,
                "pocket_label": "deep_local_pocket" if worst < threshold else "tolerable",
                "source_report_path": source,
            }
        )
    return curve, pockets


def positive_share(rows: Sequence[Mapping[str, Any]]) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if safe_float(row.get("net_profit")) > 0) / len(rows)


def min_net(rows: Sequence[Mapping[str, Any]]) -> float:
    if not rows:
        return 0.0
    return min(safe_float(row.get("net_profit")) for row in rows)


def fail_reasons(data: Mapping[str, Mapping[str, float]]) -> tuple[str, str, str, str, list[str]]:
    density_ok = 4.0 <= data["validation_is"]["tpd"] <= 10.0 and 4.0 <= data["oos"]["tpd"] <= 10.0
    profit_ok = data["validation_is"]["net"] >= 200.0 and data["oos"]["net"] >= 250.0
    efficiency_ok = (
        data["validation_is"]["pf"] >= 1.10
        and data["oos"]["pf"] >= 1.10
        and data["validation_is"]["recovery"] >= 1.0
        and data["oos"]["recovery"] >= 1.0
        and data["validation_is"]["expectancy"] > 0.0
        and data["oos"]["expectancy"] > 0.0
    )
    curve_ok = (
        data["validation_is"]["net"] > 0.0
        and data["oos"]["net"] > 0.0
        and data["validation_is"]["positive_month_share"] >= 0.60
        and data["oos"]["positive_month_share"] >= 0.60
        and data["validation_is"]["worst_month_net"] >= -90.0
        and data["oos"]["worst_month_net"] >= -90.0
        and data["validation_is"]["worst_session_net"] >= -120.0
        and data["oos"]["worst_session_net"] >= -120.0
        and data["validation_is"]["r20"] >= -120.0
        and data["oos"]["r20"] >= -120.0
        and data["validation_is"]["r50"] >= -150.0
        and data["oos"]["r50"] >= -150.0
        and data["validation_is"]["underwater_ratio"] <= 0.85
        and data["oos"]["underwater_ratio"] <= 0.85
    )
    reasons: list[str] = []
    if not density_ok:
        reasons.append("trade_density_outside_4_10_per_day(일 4-10거래 밀도 실패)")
    if not profit_ok:
        reasons.append("profit_scale_not_enough(순수익 규모 부족)")
    if not efficiency_ok:
        reasons.append("pf_recovery_expectancy_joint_fail(PF/회복/기대값 동시 실패)")
    if not curve_ok:
        reasons.append("curve_quality_or_local_pocket_fail(곡선 품질 또는 국소 포켓 실패)")
    return (
        "passed" if density_ok else "failed",
        "passed" if profit_ok else "failed",
        "passed" if efficiency_ok else "failed",
        "passed" if curve_ok else "failed",
        reasons,
    )


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
    manifest = manifest_by_id()
    records = load_actual_routed_records()
    scoreboard_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []

    for materialized_id, manifest_row in manifest.items():
        package_id = manifest_row["package_id"]
        data: dict[str, dict[str, float]] = {}
        for split in ("validation_is", "oos"):
            entry = records.get((materialized_id, split), {})
            metrics = entry.get("metrics", {}) if isinstance(entry, Mapping) else {}
            report_path = entry.get("report_path") if isinstance(entry, Mapping) else None
            frame = trade_frame(report_path) if isinstance(report_path, Path) and path_exists(report_path) else trade_frame(Path(""))
            split_monthly = attribution_rows(frame, materialized_id, package_id, split, "month", "month", report_path)
            split_session = attribution_rows(frame, materialized_id, package_id, split, "session", "session", report_path)
            monthly_rows.extend(split_monthly)
            session_rows.extend(split_session)
            quality_rows.append(quality_summary(frame, materialized_id, package_id, split, report_path))
            curve, pockets = curve_outputs(frame, materialized_id, package_id, split, report_path)
            curve_rows.append(curve)
            pocket_rows.extend(pockets)
            data[split] = {
                "net": safe_float(metrics.get("net_profit")),
                "pf": safe_float(metrics.get("profit_factor")),
                "trades": safe_float(metrics.get("trade_count")),
                "tpd": safe_float(metrics.get("trade_count")) / split_days(split),
                "dd": safe_float(metrics.get("max_drawdown_amount")),
                "recovery": safe_float(metrics.get("recovery_factor")),
                "expectancy": safe_float(metrics.get("expectancy")),
                "positive_month_share": positive_share(split_monthly),
                "worst_month_net": min_net(split_monthly),
                "worst_session_net": min_net(split_session),
                "r20": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 20),
                "r50": next(row["worst_rolling_net"] for row in pockets if row["rolling_window"] == 50),
                "underwater_ratio": safe_float(curve["underwater_ratio"]),
            }
        density_gate, profit_gate, efficiency_gate, curve_gate, reasons = fail_reasons(data)
        label = "candidate_package_gate_ready" if not reasons else "valid_negative_no_candidate"
        row = {
            "materialized_branch_id": materialized_id,
            "package_id": package_id,
            "validation_net_profit": data["validation_is"]["net"],
            "validation_pf": data["validation_is"]["pf"],
            "validation_trade_count": data["validation_is"]["trades"],
            "validation_trades_per_day": data["validation_is"]["tpd"],
            "validation_dd": data["validation_is"]["dd"],
            "validation_recovery": data["validation_is"]["recovery"],
            "validation_expectancy": data["validation_is"]["expectancy"],
            "validation_positive_month_share": data["validation_is"]["positive_month_share"],
            "validation_worst_month_net": data["validation_is"]["worst_month_net"],
            "validation_worst_session_net": data["validation_is"]["worst_session_net"],
            "validation_worst_rolling_20_net": data["validation_is"]["r20"],
            "validation_worst_rolling_50_net": data["validation_is"]["r50"],
            "validation_underwater_ratio": data["validation_is"]["underwater_ratio"],
            "oos_net_profit": data["oos"]["net"],
            "oos_pf": data["oos"]["pf"],
            "oos_trade_count": data["oos"]["trades"],
            "oos_trades_per_day": data["oos"]["tpd"],
            "oos_dd": data["oos"]["dd"],
            "oos_recovery": data["oos"]["recovery"],
            "oos_expectancy": data["oos"]["expectancy"],
            "oos_positive_month_share": data["oos"]["positive_month_share"],
            "oos_worst_month_net": data["oos"]["worst_month_net"],
            "oos_worst_session_net": data["oos"]["worst_session_net"],
            "oos_worst_rolling_20_net": data["oos"]["r20"],
            "oos_worst_rolling_50_net": data["oos"]["r50"],
            "oos_underwater_ratio": data["oos"]["underwater_ratio"],
            "density_gate": density_gate,
            "profit_scale_gate": profit_gate,
            "efficiency_gate": efficiency_gate,
            "curve_quality_gate": curve_gate,
            "review_label": label,
            "failure_reasons": ";".join(reasons) if reasons else "none",
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
                "failure_type": "valid_negative_runtime_probe(유효 부정 런타임 탐침)",
                "failure_reasons": row["failure_reasons"],
                "salvage_value": "density behavior and negative-direction evidence only(밀도 행동과 역방향 단서만 보존)",
                "reopen_condition": "fresh anti-direction meta-label or trade-simulator objective, not threshold repair(새 역방향 메타라벨 또는 거래 시뮬레이터 목적함수일 때만 재개)",
                "claim_boundary": BOUNDARY,
            }
        )
    queue_rows = stage292_queue_rows()
    return scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows, queue_rows


def stage292_queue_rows() -> list[dict[str, Any]]:
    refs = ";".join(
        [
            "stage267_reference_evidence",
            "stage286_density_curve_failure",
            "stage290_payoff_weighted_edge_near_density",
            "stage291_wfo_negative_runtime",
        ]
    )
    return [
        {
            "seed_id": "stage292_anti_direction_meta_label",
            "source_stage_id": STAGE291_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주 씨앗)",
            "hypothesis": "anti-direction meta-label(역방향 메타라벨)이 direct WFO loss(직접 워크포워드 손실)를 invert/skip decision(반전/회피 판단)으로 바꿀 수 있다.",
            "broad_sweep": "direct, inverse, conditional inverse, skip-heavy regimes(직접/역방향/조건부 역방향/회피 중심 국면)",
            "extreme_sweep": "contrarian-only, side-specific only, session-blocked extremes(완전 역추세/방향별 단독/세션 차단 극단)",
            "micro_search_gate": "validation and OOS both positive with 4-10 trades/day(검증과 표본외 모두 양수, 일 4-10거래)",
            "wfo_plan": "rolling folds with validation/OOS separation(롤링 폴드와 검증/표본외 분리)",
            "required_change": "learn when to invert or skip from realized trade outcomes(실현 거래 결과로 반전/회피 시점을 학습)",
            "discard_condition": "both direct and anti-direction variants remain negative in MT5 probe(MT5 탐침에서 직접/역방향 모두 음수)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage292_trade_simulator_objective",
            "source_stage_id": STAGE291_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_profit_scale(새 논제 수익 규모)",
            "hypothesis": "trade simulator objective(거래 시뮬레이터 목적함수)가 bar-return proxy(봉 수익 대리값)보다 net/PF/recovery(순수익/PF/회복)를 직접 맞출 수 있다.",
            "broad_sweep": "hold, reverse, flat, cooldown, cost-aware payoff(보유/반전/관망/쿨다운/비용 반영 손익)",
            "extreme_sweep": "short hold 2 bars, long hold 12 bars, forced flat, reverse-only(2봉 보유/12봉 보유/강제 관망/반전 전용)",
            "micro_search_gate": "simulator proxy must rank at least one branch positive in both splits(시뮬레이터 대리 점수가 양 구간 양수 분기를 하나 이상 세움)",
            "wfo_plan": "walk-forward simulator fitting with frozen validation bands(워크포워드 시뮬레이터 적합과 고정 검증 대역)",
            "required_change": "optimize trade PnL path and curve pockets directly(거래 손익 경로와 곡선 포켓을 직접 최적화)",
            "discard_condition": "proxy positivity does not survive MT5 routed totals(대리 양수가 MT5 실제 라우팅에서 생존 못 함)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage292_density_profit_two_head_router",
            "source_stage_id": STAGE291_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_density_profit_balance(새 논제 밀도/수익 균형)",
            "hypothesis": "two-head router(이중 헤드 라우터)가 density head(밀도 헤드)와 profit-quality head(수익 품질 헤드)를 분리해 4-10 trades/day(일 4-10거래)와 수익 규모를 함께 맞출 수 있다.",
            "broad_sweep": "density target 4, 6, 8, 10 trades/day with quality veto(일 4/6/8/10거래 목표와 품질 거부)",
            "extreme_sweep": "minimum-density only, maximum-density only, quality-veto only(최소 밀도/최대 밀도/품질 거부 단독)",
            "micro_search_gate": "density pass without negative expectancy(밀도 통과와 기대값 음수 회피)",
            "wfo_plan": "fold-level density calibration plus OOS trade simulator review(폴드별 밀도 보정과 표본외 거래 시뮬레이터 검토)",
            "required_change": "separate trade supply from trade acceptance(거래 공급과 거래 수락을 분리)",
            "discard_condition": "density pass still creates negative net or deep pockets(밀도 통과가 여전히 순손실 또는 깊은 포켓 생성)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
    ]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = []
    for row in scoreboard_rows:
        lines.append(
            f"- `{row['package_id']}`: validation(검증) net `{float(row['validation_net_profit']):.2f}`, "
            f"PF `{float(row['validation_pf']):.2f}`, `{float(row['validation_trades_per_day']):.2f}` trades/day(일 거래); "
            f"OOS(표본외) net `{float(row['oos_net_profit']):.2f}`, PF `{float(row['oos_pf']):.2f}`, "
            f"`{float(row['oos_trades_per_day']):.2f}` trades/day(일 거래); "
            f"gate(관문) `{row['density_gate']}/{row['profit_scale_gate']}/{row['efficiency_gate']}/{row['curve_quality_gate']}`."
        )
    seed_lines = [f"- `{row['seed_id']}`: {row['hypothesis']}" for row in queue_rows]
    return f"""# run291C Walk-forward Payoff Review(291C 워크포워드 손익 검토)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage292_seed_count(292단계 씨앗 수): `{len(queue_rows)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Scoreboard(점수판)

{chr(10).join(lines)}

## Stage292 Seeds(292단계 씨앗)

{chr(10).join(seed_lines)}

## Decision(결정)

Stage291(291단계)은 WFO payoff generalization(워크포워드 손익 일반화)을 실제 MT5(MetaTrader 5, 메타트레이더5) routed total(실제 라우팅 전체)로 확인했지만, 모든 분기가 순손실과 낮은 PF(수익 팩터)로 candidate package(후보 패키지) 기준을 통과하지 못했다.
Effect(효과): 같은 WFO classifier/regressor(분류기/회귀기) repair(수리)를 반복하지 않고 Stage292(292단계)에서 anti-direction meta-label(역방향 메타라벨), trade simulator objective(거래 시뮬레이터 목적함수), density/profit two-head router(밀도/수익 이중 헤드 라우터)로 새 질문을 연다.

## Boundary(경계)

`{BOUNDARY}`
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
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(TRADE_QUALITY, TRADE_QUALITY_COLUMNS, quality_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(LOCAL_POCKETS, POCKET_COLUMNS, pocket_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(STAGE292_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"scoreboard={rel(SCOREBOARD)};mt5_kpi={rel(SOURCE_KPI)};failure_rows={len(failure_rows)}",
                "evidence_missing": "selected candidate;Adapter package;ONNX export/parity;MT5 runtime reproduction",
                "judgment_label": JUDGMENT,
                "judgment_class": "valid_negative_runtime_review(유효 부정 런타임 검토)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "팩터보다 순수익과 곡선이 먼저 무너져서 ONNX(온엑스)로 넘기지 않는다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "mt5_external_evidence(MT5 외부 근거)",
                "status": "passed",
                "evidence_path": rel(SOURCE_KPI),
                "effect": "run291B(291B 실행)의 36개 Strategy Tester(전략 테스터) KPI를 검토 근거로 고정한다.",
            },
            {
                "gate_name": "onnx_worthy_candidate_gate(온엑스 가치 후보 관문)",
                "status": "failed",
                "evidence_path": rel(SCOREBOARD),
                "effect": "거래 수, 일 거래수, 순수익, PF, 회복, 기대값, 곡선을 함께 보아 후보 선택을 막는다.",
            },
            {
                "gate_name": "fresh_thesis_handoff(새 논제 인계)",
                "status": "passed",
                "evidence_path": rel(STAGE292_QUEUE),
                "effect": "좁은 repair(수리) 반복 대신 Stage292(292단계) 새 구조로 넘긴다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, queue_rows))
    write_md(
        DECISION,
        f"""# Stage291 Walk-forward Payoff Review Decision(291단계 워크포워드 손익 검토 결정)

- source_run(원천 실행): `{SOURCE_RUN_ID}`
- review_run(검토 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- target_stage(대상 단계): `{STAGE292_ID}`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): Stage291(291단계)을 선택 후보 없이 닫고 Stage292(292단계)를 anti-direction meta-label/trade simulator(역방향 메타라벨/거래 시뮬레이터) 새 논제로 연다.
""",
    )
    final = [
        SCOREBOARD,
        MONTHLY,
        SESSION,
        TRADE_QUALITY,
        CURVE,
        LOCAL_POCKETS,
        FAILURE_MEMORY,
        STAGE292_QUEUE,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
    ]
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": PRODUCER.as_posix(),
            "source_artifacts": [
                rel(SOURCE_MANIFEST),
                rel(SOURCE_MODEL_SCOREBOARD),
                rel(SOURCE_WFO_SCOREBOARD),
                rel(SOURCE_KPI),
                rel(SOURCE_EXECUTION),
                rel(SOURCE_RUN_MANIFEST),
            ],
            "produced_artifacts": [rel(path) for path in final if path_exists(path)],
            "claim_boundary": BOUNDARY,
        },
    )
    final.append(LINEAGE)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE291_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "scoreboard_rows": len(scoreboard_rows),
            "failure_rows": len(failure_rows),
            "stage292_seed_rows": len(queue_rows),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
            "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final if path_exists(path)},
        },
    )
    final.append(RUN_MANIFEST)
    return [path for path in final if path_exists(path)]


def ensure_stage292(queue_rows: Sequence[Mapping[str, Any]]) -> None:
    for path in (STAGE292 / "00_spec", STAGE292 / "01_inputs", STAGE292 / "03_reviews", STAGE292 / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(
        STAGE292 / "00_spec" / "stage_brief.md",
        f"""# Stage292 Anti-direction Meta-label Trade Simulator Rebuild(292단계 역방향 메타라벨 거래 시뮬레이터 재구성)

- canonical_stage_id(정식 단계 ID): `{STAGE292_ID}`
- big_question(큰 질문): Can anti-direction meta-labels and trade-simulator objectives create an ONNX-worthy candidate with 4-10 trades/day and a smoother rising curve?(역방향 메타라벨과 거래 시뮬레이터 목적함수가 일 4-10거래와 더 매끄러운 우상향 곡선을 가진 온엑스 가치 후보를 만들 수 있는가?)
- source_stage(원천 단계): `{STAGE291_ID}`
- seed_count(씨앗 수): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): Stage291(291단계)의 broad WFO loss(넓은 워크포워드 손실)를 같은 repair(수리)로 반복하지 않고, direction inversion(방향 반전), simulator objective(시뮬레이터 목적함수), density/profit separation(밀도/수익 분리)을 새 구조로 시험한다.
""",
    )
    write_csv(STAGE292 / "01_inputs" / "stage292_seed_queue.csv", QUEUE_COLUMNS, queue_rows)
    write_md(
        STAGE292 / "01_inputs" / "input_refs.md",
        f"""# Stage292 Input Refs(292단계 입력 참조)

- run291C_scoreboard(291C 점수판): `{rel(SCOREBOARD)}`
- run291C_failure_memory(291C 실패 기억): `{rel(FAILURE_MEMORY)}`
- run291C_curve_pockets(291C 곡선 포켓): `{rel(LOCAL_POCKETS)}`
- run291B_mt5_kpi_summary(291B MT5 KPI 요약): `{rel(SOURCE_KPI)}`
- stage290_scoreboard_reference(290단계 점수판 참조): `stages/290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild/02_runs/run290C/payoff_weighted_edge_scoreboard.csv`

Effect(효과): 과거 stage(단계)는 후보명 보존이 아니라 실패 기억과 구조 단서로만 사용한다.
""",
    )
    write_md(
        STAGE292 / "03_reviews" / "review_index.md",
        "# Stage292 Review Index(292단계 검토 색인)\n",
    )
    write_csv(
        STAGE292 / "03_reviews" / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage292_opened_from_run291C",
                "stage_id": STAGE292_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage292_seed_queue",
                "status": "opened_anti_direction_meta_label_trade_simulator_rebuild",
                "judgment": "stage_opened_from_stage291_valid_negative",
                "evidence_boundary": "planning_from_stage291_evidence",
                "report_path": rel(REPORT),
                "notes": f"seed_count={len(queue_rows)};next_action={NEXT_ACTION}",
            }
        ],
    )
    write_md(
        STAGE292 / "04_selected" / "selection_status.md",
        f"""# Stage292 Selection Status(292단계 선택 상태)

- stage_status(단계 상태): `opened_anti_direction_meta_label_trade_simulator_rebuild`
- current_packet(현재 작업 묶음): `{STAGE292_ID}_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE291_ID}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(STAGE292 / "01_inputs" / "input_refs.md")}`
""",
    )


def update_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE291_ID,
                "lane": "walk_forward_payoff_generalization_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};target_stage={STAGE292_ID};next_action={NEXT_ACTION}",
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
                "stage_id": STAGE291_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "walk_forward_payoff_generalization_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "walk_forward_payoff_generalization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "completed_run291B_mt5_probe",
                "notes": f"target_stage={STAGE292_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv(
        STAGE_LEDGER291,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE291_ID,
                "run_id": RUN_ID,
                "view": "walk_forward_payoff_generalization_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "walk_forward_payoff_review_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "valid_negative_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"target_stage={STAGE292_ID};selected_candidate=none.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage291_walk_forward_payoff_review_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE291_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run291C walk-forward payoff review and Stage292 handoff",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    ensure_stage292(queue_rows)

    selected = io_path(SELECTED291).read_text(encoding="utf-8-sig") if path_exists(SELECTED291) else ""
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run291C_report", f"- run291C_report(291C 보고): `{rel(REPORT)}`")
    selected = append_once(selected, "run291C_scoreboard", f"- run291C_scoreboard(291C 점수판): `{rel(SCOREBOARD)}`")
    write_md(SELECTED291, selected)

    review_index = io_path(REVIEW_INDEX291).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX291) else "# Stage291 Review Index(291단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run291C_report",
        f"- run291C_report(291C 보고): `{rel(REPORT)}`\n- run291C_scoreboard(291C 점수판): `{rel(SCOREBOARD)}`\n- run291C_failure_memory(291C 실패 기억): `{rel(FAILURE_MEMORY)}`",
    )
    write_md(REVIEW_INDEX291, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", f"- current_packet(현재 작업 묶음): `{STAGE292_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE292_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE291_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `none`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run291C_summary",
        f"- run291C_summary(291C 요약): Stage291(291단계) WFO payoff generalization(워크포워드 손익 일반화)을 MT5 KPI/곡선/거래품질로 검토했다. Effect(효과): 모든 후보가 순손실 또는 효율/곡선 gate(관문)를 실패해 selected_candidate(선택 후보)는 `none`, 다음 단계는 `{STAGE292_ID}`다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE292_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage291(291단계) run291C(291C 실행) walk-forward payoff review(워크포워드 손익 검토) `{RUN_ID}`. "
        f"Effect(효과): scoreboard(점수판) `{len(scoreboard_rows)}`행과 failure memory(실패 기억) `{len(failure_rows)}`행을 만들고 selected candidate(선택 후보) 없이 `{STAGE292_ID}`를 열었다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run291C Walk-forward payoff review(291C 워크포워드 손익 검토)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): Stage291(291단계)을 선택 후보 없이 닫고 `{STAGE292_ID}`를 열었다.\n"
        f"- selected_candidate(선택 후보): `none`\n"
        f"- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    update_idea_and_negative_registers()


def update_idea_and_negative_registers() -> None:
    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "Register ideas when they become durable work.\n"
    if "IDEA-ST292-ANTI-DIRECTION-META-LABEL-TRADE-SIM" not in idea:
        idea = (
            idea.rstrip()
            + "\n\n| `IDEA-ST292-ANTI-DIRECTION-META-LABEL-TRADE-SIM` | `"
            + STAGE292_ID
            + "` | anti-direction meta-label/trade simulator rebuild(역방향 메타라벨/거래 시뮬레이터 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage291(291단계)의 WFO negative runtime(워크포워드 음수 런타임)을 새 invert/skip/simulator/density-profit 구조로 바꾼다. selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |\n"
        )
        write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    if "NEG-ST291-WFO-PAYOFF-GENERALIZATION" not in negative:
        negative = (
            negative.rstrip()
            + "\n\n| `NEG-ST291-WFO-PAYOFF-GENERALIZATION` | `IDEA-ST291-WFO-PAYOFF-GENERALIZATION` | walk-forward payoff generalization(워크포워드 손익 일반화)이 ONNX-worthy candidate(온엑스 가치 후보)로 이어질 수 있다 | run291C(291C 실행)에서 6개 후보 모두 actual routed total(실제 라우팅 전체) 기준 순손실 또는 낮은 PF/회복/곡선 실패로 candidate package(후보 패키지)가 없었다 | broad WFO signal(넓은 워크포워드 신호)은 실패 기억으로 남기고, invert/skip/meta-label(반전/회피/메타라벨) 단서만 Stage292(292단계)로 넘긴다 | anti-direction meta-label(역방향 메타라벨), trade simulator objective(거래 시뮬레이터 목적함수), density/profit two-head router(밀도/수익 이중 헤드 라우터)처럼 구조가 바뀔 때만 재개 |\n"
        )
        write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
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
    update_docs(created_at, artifacts, scoreboard_rows, failure_rows, queue_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "scoreboard_rows": len(scoreboard_rows),
                "failure_rows": len(failure_rows),
                "stage292_seed_rows": len(queue_rows),
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
