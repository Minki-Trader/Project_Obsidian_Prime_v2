from __future__ import annotations

import ast
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


STAGE_ID = "292_onnx_candidate_campaign__anti_direction_meta_label_trade_simulator_rebuild"
NEXT_REBUILD_STAGE_ID = "293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild"
NEXT_ADAPTER_STAGE_ID = "293_onnx_candidate_campaign__adapter_package_for_stage292_candidate"
RUN_ID = "run292C_review_anti_direction_meta_label_trade_simulator_mt5_probe_v1"
RUN_NUMBER = "run292C"
SOURCE_RUN_ID = "run292B_anti_direction_meta_label_trade_simulator_mt5_probe_v1"
PARENT_RUN_ID = "run292A_design_anti_direction_meta_label_trade_simulator_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_adapter_and_parity_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN292A = STAGE_ROOT / "02_runs" / "run292A"
RUN292B = STAGE_ROOT / "02_runs" / "run292B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_MANIFEST = RUN292A / "candidate_payload_manifest.csv"
SOURCE_KPI = RUN292B / "mt5_kpi_summary.csv"
SOURCE_EXECUTION = RUN292B / "execution_result.json"
PRODUCER = Path("stage_pipelines/stage292/review_anti_direction_meta_label_trade_simulator_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "anti_direction_meta_trade_sim_review_scoreboard.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage293_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run292C_anti_direction_meta_trade_sim_review_stage293_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage292_anti_direction_meta_trade_sim_review_stage293_open.md"

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
    "validation_min_trade_count",
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
    "validation_top_10pct_contribution_share",
    "oos_net_profit",
    "oos_pf",
    "oos_trade_count",
    "oos_min_trade_count",
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
    "oos_top_10pct_contribution_share",
    "combined_net_profit",
    "minimum_trade_gate",
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
    "aggressive_sweep",
    "defensive_sweep",
    "success_gate",
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


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def min_trade_count(split: str) -> int:
    return split_days(split) * 4


def resolve_report_path(path_text: str) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text)
    if path_exists(path):
        return path
    if path.name:
        fallback = RUN292B / "mt5" / "reports" / path.name
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
    for window, threshold in ((20, -100.0), (50, -140.0)):
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


def fail_reasons(data: Mapping[str, Mapping[str, float]]) -> tuple[str, str, str, str, str, list[str]]:
    minimum_ok = (
        data["validation_is"]["trades"] >= min_trade_count("validation_is")
        and data["oos"]["trades"] >= min_trade_count("oos")
    )
    density_ok = 4.0 <= data["validation_is"]["tpd"] <= 10.0 and 4.0 <= data["oos"]["tpd"] <= 10.0
    combined_net = data["validation_is"]["net"] + data["oos"]["net"]
    profit_ok = data["validation_is"]["net"] >= 300.0 and data["oos"]["net"] >= 300.0 and combined_net >= 800.0
    efficiency_ok = (
        data["validation_is"]["pf"] >= 1.12
        and data["oos"]["pf"] >= 1.12
        and data["validation_is"]["recovery"] >= 1.0
        and data["oos"]["recovery"] >= 1.0
        and data["validation_is"]["expectancy"] > 0.0
        and data["oos"]["expectancy"] > 0.0
    )
    curve_ok = (
        data["validation_is"]["net"] > 0.0
        and data["oos"]["net"] > 0.0
        and data["validation_is"]["positive_month_share"] >= 0.70
        and data["oos"]["positive_month_share"] >= 0.70
        and data["validation_is"]["worst_month_net"] >= -70.0
        and data["oos"]["worst_month_net"] >= -70.0
        and data["validation_is"]["worst_session_net"] >= -100.0
        and data["oos"]["worst_session_net"] >= -100.0
        and data["validation_is"]["r20"] >= -100.0
        and data["oos"]["r20"] >= -100.0
        and data["validation_is"]["r50"] >= -140.0
        and data["oos"]["r50"] >= -140.0
        and data["validation_is"]["underwater_ratio"] <= 0.80
        and data["oos"]["underwater_ratio"] <= 0.80
        and data["validation_is"]["top_10_share"] <= 0.75
        and data["oos"]["top_10_share"] <= 0.75
    )
    reasons: list[str] = []
    if not minimum_ok:
        reasons.append("minimum_trade_count_fail(최소 거래수 실패)")
    if not density_ok:
        reasons.append("trade_density_outside_4_10_per_day(일 4-10거래 밀도 실패)")
    if not profit_ok:
        reasons.append("profit_scale_not_enough(순수익 규모 부족)")
    if not efficiency_ok:
        reasons.append("pf_recovery_expectancy_joint_fail(PF/회복/기대값 동시 실패)")
    if not curve_ok:
        reasons.append("curve_quality_or_local_pocket_fail(곡선 품질 또는 국소 포켓 실패)")
    return (
        "passed" if minimum_ok else "failed",
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
    dict[str, Any] | None,
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
            quality = quality_summary(frame, materialized_id, package_id, split, report_path)
            quality_rows.append(quality)
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
                "top_10_share": safe_float(quality["top_10pct_contribution_share"]),
            }
        minimum_gate, density_gate, profit_gate, efficiency_gate, curve_gate, reasons = fail_reasons(data)
        label = "candidate_package_gate_ready" if not reasons else "valid_negative_no_candidate"
        row = {
            "materialized_branch_id": materialized_id,
            "package_id": package_id,
            "validation_net_profit": data["validation_is"]["net"],
            "validation_pf": data["validation_is"]["pf"],
            "validation_trade_count": data["validation_is"]["trades"],
            "validation_min_trade_count": min_trade_count("validation_is"),
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
            "validation_top_10pct_contribution_share": data["validation_is"]["top_10_share"],
            "oos_net_profit": data["oos"]["net"],
            "oos_pf": data["oos"]["pf"],
            "oos_trade_count": data["oos"]["trades"],
            "oos_min_trade_count": min_trade_count("oos"),
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
            "oos_top_10pct_contribution_share": data["oos"]["top_10_share"],
            "combined_net_profit": data["validation_is"]["net"] + data["oos"]["net"],
            "minimum_trade_gate": minimum_gate,
            "density_gate": density_gate,
            "profit_scale_gate": profit_gate,
            "efficiency_gate": efficiency_gate,
            "curve_quality_gate": curve_gate,
            "review_label": label,
            "failure_reasons": ";".join(reasons) if reasons else "none",
            "selected_candidate": "pending_selection" if not reasons else "none",
            "adapter_package": "none",
            "onnx_readiness": "not_started",
            "claim_boundary": BOUNDARY,
        }
        scoreboard_rows.append(row)
        if reasons:
            failure_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "failure_type": "valid_negative_runtime_probe(유효 부정 런타임 탐침)",
                    "failure_reasons": row["failure_reasons"],
                    "salvage_value": "runtime density and simulator gap evidence only(런타임 밀도와 시뮬레이터 공백 근거만 보존)",
                    "reopen_condition": "new simulator-to-runtime calibration or curve objective, not narrow threshold repair(새 시뮬레이터-런타임 보정 또는 곡선 목적함수일 때만 재개)",
                    "claim_boundary": BOUNDARY,
                }
            )

    passing = [row for row in scoreboard_rows if row["review_label"] == "candidate_package_gate_ready"]
    selected = None
    if passing:
        selected = max(
            passing,
            key=lambda row: (
                safe_float(row["combined_net_profit"]),
                safe_float(row["oos_pf"]),
                -safe_float(row["oos_underwater_ratio"]),
            ),
        )
        for row in scoreboard_rows:
            row["selected_candidate"] = row["package_id"] if row["package_id"] == selected["package_id"] else "none"

    queue_rows = stage293_queue_rows(selected)
    return scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows, queue_rows, selected


def stage293_queue_rows(selected: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    refs = ";".join(
        [
            "stage267_reference_evidence",
            "stage290_payoff_weighted_edge",
            "stage291_walk_forward_negative",
            "stage292_anti_direction_meta_trade_sim_runtime_probe",
        ]
    )
    if selected:
        return [
            {
                "seed_id": "stage293_adapter_package_for_stage292_candidate",
                "source_stage_id": STAGE_ID,
                "source_run_id": RUN_ID,
                "seed_role": "adapter_package_build(어댑터 패키지 구성)",
                "hypothesis": f"{selected['package_id']} can be formalized as an Adapter package(어댑터 패키지) with traceable feature order(피처 순서) and runtime handoff(런타임 인계).",
                "broad_sweep": "feature order receipt, decision surface receipt, risk logic receipt(피처 순서/판단 표면/위험 로직 영수증)",
                "aggressive_sweep": "none; adapter packaging only(없음; 어댑터 패키징만)",
                "defensive_sweep": "parity pressure before ONNX export(ONNX 내보내기 전 동등성 압박)",
                "success_gate": "Adapter package complete, feature order fixed, runtime handoff reproducible(어댑터 패키지 완료/피처 순서 고정/런타임 인계 재현)",
                "discard_condition": "feature order or runtime handoff cannot be traced(피처 순서 또는 런타임 인계를 추적할 수 없음)",
                "prior_stage_refs": refs,
                "claim_boundary": BOUNDARY,
            }
        ]
    return [
        {
            "seed_id": "stage293_runtime_aware_trade_simulator_calibration",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주축)",
            "hypothesis": "runtime-aware trade simulator calibration(런타임 인식 거래 시뮬레이터 보정)이 proxy-positive/runtime-weak gap(대리 양수/런타임 약점 공백)을 줄일 수 있다.",
            "broad_sweep": "cost, spread, hold, reverse, flat, cooldown calibration(비용/스프레드/보유/반전/관망/쿨다운 보정)",
            "aggressive_sweep": "profit-scale objective and asymmetric reward routing(순수익 규모 목적함수와 비대칭 보상 라우팅)",
            "defensive_sweep": "monthly/session/pocket penalties(월별/세션/포켓 벌점)",
            "success_gate": "MT5 actual routed total positive with 4-10 trades/day and no deep local pocket(MT5 실제 라우팅 전체 양수, 일 4-10거래, 깊은 포켓 없음)",
            "discard_condition": "simulator-ranked positives remain runtime negative(시뮬레이터 양수 순위가 런타임에서 계속 음수)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage293_density_profit_scale_router",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_density_scale(새 논제 밀도/규모)",
            "hypothesis": "density/profit scale router(밀도/순수익 규모 라우터)가 trade count(거래수)와 net profit(순수익)을 동시에 제한할 수 있다.",
            "broad_sweep": "4-10 trades/day band, per-session quota, weak-month veto(일 4-10거래 대역/세션별 할당/약한 월 거부)",
            "aggressive_sweep": "high-conviction dense windows and tail capture(고확신 고밀도 구간과 꼬리 수익 포착)",
            "defensive_sweep": "drawdown pocket cap and concentration cap(손실폭 포켓 상한과 수익 집중 상한)",
            "success_gate": "minimum trade count, PF, recovery, expectancy, smooth curve all pass(최소 거래수/PF/회복/기대값/매끈한 곡선 모두 통과)",
            "discard_condition": "density increase lowers PF below usable level(밀도 증가가 PF를 사용 불가 수준으로 낮춤)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage293_smooth_curve_objective_walk_forward",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_curve(새 논제 곡선)",
            "hypothesis": "smooth curve objective(매끈한 곡선 목적함수)가 local pocket(국소 포켓)과 weak session(약한 세션)을 직접 줄일 수 있다.",
            "broad_sweep": "rolling drawdown penalty, month/session balance, equity monotonicity proxy(롤링 손실폭 벌점/월세션 균형/평가금 단조성 대리값)",
            "aggressive_sweep": "allow higher trade count only where curve stays controlled(곡선이 통제될 때만 높은 거래수 허용)",
            "defensive_sweep": "hard veto on deep rolling loss pockets(깊은 롤링 손실 포켓 강한 거부)",
            "success_gate": "zoomed balance/equity segments remain upward without a deep hollow(확대 구간 잔액/평가금이 깊은 움푹 파임 없이 우상향)",
            "discard_condition": "smoothness removes profit scale or density(매끈함이 순수익 규모나 밀도를 제거)",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
    ]


def status_pack(selected: Mapping[str, Any] | None) -> tuple[str, str, str, str]:
    if selected:
        return (
            "completed_anti_direction_meta_trade_sim_review_candidate_gate_ready_stage293_adapter_opened",
            "anti_direction_meta_trade_sim_candidate_package_gate_ready_adapter_required_no_onnx",
            "run293A_design_adapter_package_for_stage292_candidate",
            NEXT_ADAPTER_STAGE_ID,
        )
    return (
        "completed_anti_direction_meta_trade_sim_review_no_candidate_stage293_opened",
        "anti_direction_meta_trade_sim_runtime_probe_negative_no_adapter_no_onnx",
        "run293A_design_profit_scale_density_calibration_rebuild_packet",
        NEXT_REBUILD_STAGE_ID,
    )


def result_rows(
    selected: Mapping[str, Any] | None,
    scoreboard_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    next_action: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_gate = "passed" if selected else "failed"
    rows = [
        {
            "result_subject": "Stage292 anti-direction meta-label trade simulator MT5 review(292단계 반대방향 메타라벨 거래 시뮬레이터 MT5 검토)",
            "evidence_available": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};source_kpi={rel(SOURCE_KPI)}",
            "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(ONNX 동등성), MT5 runtime reproduction(MT5 런타임 재현)",
            "judgment_label": "exploratory" if selected else "negative",
            "judgment_class": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "조건을 만족하면 Adapter(어댑터)로 넘기고, 아니면 새 논제로 순수익 규모와 곡선을 다시 만든다.",
        }
    ]
    gates = [
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "passed",
            "evidence_path": rel(SOURCE_KPI),
            "effect": "actual routed total(실제 라우팅 전체)을 기준으로 후보를 판정한다.",
        },
        {
            "gate_name": "minimum_trade_and_density(최소 거래수와 밀도)",
            "status": candidate_gate,
            "evidence_path": rel(SCOREBOARD),
            "effect": "최소 거래수와 일 4-10거래 조건을 동시에 본다.",
        },
        {
            "gate_name": "profit_efficiency_curve(순수익/효율/곡선)",
            "status": candidate_gate,
            "evidence_path": rel(SCOREBOARD),
            "effect": "순수익 규모, PF(수익 팩터), 회복, 기대값, 확대 곡선 포켓을 함께 본다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 게이트 전에는 Adapter(어댑터)를 만들지 않는다.",
        },
        {
            "gate_name": "onnx_readiness(ONNX 준비)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "Adapter(어댑터)와 parity(동등성) 전에는 ONNX(온엑스)를 시작하지 않는다.",
        },
    ]
    return rows, gates


def report_markdown(
    scoreboard_rows: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any] | None,
    status: str,
    judgment: str,
    next_action: str,
    next_stage_id: str,
) -> str:
    lines = [
        "# run292C Anti-Direction Meta Trade Sim Review(292C 반대방향 메타 거래 시뮬레이터 검토)",
        "",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- selected_candidate(선택 후보): `{selected['package_id'] if selected else 'none'}`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_started`",
        f"- next_action(다음 행동): `{next_action}`",
        f"- next_stage(다음 단계): `{next_stage_id}`",
        "",
        "Effect(효과): MT5 actual routed total(MT5 실제 라우팅 전체)을 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 확대 곡선 포켓 조건으로 판정한다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | val/day(검증 일거래) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS/day(표본외 일거래) | gate(게이트) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.2f} | {vpf:.2f} | {vtd:.2f} | {on:.2f} | {opf:.2f} | {otd:.2f} | {gate} |".format(
                pkg=row["package_id"],
                vn=safe_float(row["validation_net_profit"]),
                vpf=safe_float(row["validation_pf"]),
                vtd=safe_float(row["validation_trades_per_day"]),
                on=safe_float(row["oos_net_profit"]),
                opf=safe_float(row["oos_pf"]),
                otd=safe_float(row["oos_trades_per_day"]),
                gate=row["review_label"],
            )
        )
    lines.extend(
        [
            "",
            "Claim boundary(주장 경계): 이 결과는 연구/개발 판정이다. 운영 승격, 런타임 권위, 배포, production baseline(운영 기준선)은 주장하지 않는다.",
        ]
    )
    return "\n".join(lines)


def decision_markdown(selected: Mapping[str, Any] | None, status: str, judgment: str, next_stage_id: str) -> str:
    if selected:
        decision = f"{selected['package_id']} passes the candidate package gate(후보 패키지 게이트 통과) and moves to Adapter package(어댑터 패키지) work."
    else:
        decision = "No Stage292 package passes the ONNX-worthy candidate gate(ONNX화 가치 후보 게이트), so Stage293 opens a fresh profit-scale/density/curve thesis(순수익 규모/밀도/곡선 새 논제)."
    return f"""# Stage292 Decision(292단계 결정)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): {decision}
- next_stage(다음 단계): `{next_stage_id}`

Effect(효과): 좁은 repair(수리) 반복을 멈추고, 조건을 통과한 경우에는 Adapter(어댑터)로, 실패한 경우에는 새 구조 실험으로 넘어간다.
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
    selected: Mapping[str, Any] | None,
    created_at: str,
    status: str,
    judgment: str,
    next_action: str,
    next_stage_id: str,
) -> list[Path]:
    for path in (RUN_ROOT, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    result_rows_out, gate_rows = result_rows(selected, scoreboard_rows, failure_rows, status, judgment, next_action)
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(TRADE_QUALITY, TRADE_QUALITY_COLUMNS, quality_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(LOCAL_POCKETS, POCKET_COLUMNS, pocket_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_csv(NEXT_STAGE_QUEUE, QUEUE_COLUMNS, queue_rows)
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows_out)
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": status,
            "judgment": judgment,
            "selected_candidate": selected["package_id"] if selected else "none",
            "adapter_package": "none",
            "onnx_readiness": "not_started",
            "next_action": next_action,
            "next_stage_id": next_stage_id,
            "created_at_utc": created_at,
            "artifacts": [rel(path) for path in (SCOREBOARD, MONTHLY, SESSION, TRADE_QUALITY, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)],
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source": {
                "manifest": rel(SOURCE_MANIFEST),
                "mt5_kpi_summary": rel(SOURCE_KPI),
                "execution_result": rel(SOURCE_EXECUTION),
            },
            "outputs": {
                "scoreboard": rel(SCOREBOARD),
                "failure_memory": rel(FAILURE_MEMORY),
                "next_stage_queue": rel(NEXT_STAGE_QUEUE),
                "report": rel(REPORT),
            },
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, selected, status, judgment, next_action, next_stage_id))
    write_md(DECISION, decision_markdown(selected, status, judgment, next_stage_id))
    return [
        SCOREBOARD,
        MONTHLY,
        SESSION,
        TRADE_QUALITY,
        CURVE,
        LOCAL_POCKETS,
        FAILURE_MEMORY,
        NEXT_STAGE_QUEUE,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
        DECISION,
    ]


def write_next_stage_scaffold(queue_rows: Sequence[Mapping[str, Any]], selected: Mapping[str, Any] | None, next_stage_id: str, next_action: str) -> None:
    stage_root = ROOT / "stages" / next_stage_id
    for subdir in ("01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(stage_root / subdir).mkdir(parents=True, exist_ok=True)
    if selected:
        write_csv(stage_root / "01_inputs" / "adapter_seed_queue.csv", QUEUE_COLUMNS, queue_rows)
        input_name = "adapter_seed_queue.csv"
        status = "opened_adapter_package_for_stage292_candidate"
        target = selected["package_id"]
    else:
        write_csv(stage_root / "01_inputs" / "stage293_seed_queue.csv", QUEUE_COLUMNS, queue_rows)
        input_name = "stage293_seed_queue.csv"
        status = "opened_profit_scale_density_calibration_rebuild"
        target = "none"
    write_md(
        stage_root / "01_inputs" / "input_refs.md",
        f"""# Stage293 Input Refs(293단계 입력 참조)

- source_report(원천 보고): `{rel(REPORT)}`
- source_scoreboard(원천 점수표): `{rel(SCOREBOARD)}`
- source_failure_memory(원천 실패 기억): `{rel(FAILURE_MEMORY)}`
- source_queue(원천 대기열): `{rel(stage_root / "01_inputs" / input_name)}`

Effect(효과): Stage292(292단계)의 결과를 후보명 보존이 아니라 다음 질문의 입력 근거로만 사용한다.
""",
    )
    write_md(stage_root / "03_reviews" / "review_index.md", "# Stage293 Review Index(293단계 검토 색인)\n")
    write_csv(
        stage_root / "03_reviews" / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage293_opened_from_run292C",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage292_review",
                "status": status,
                "judgment": "opened_from_stage292_runtime_review",
                "evidence_boundary": "planning_from_stage292_evidence",
                "report_path": rel(REPORT),
                "notes": f"queue_rows={len(queue_rows)};next_action={next_action}",
            }
        ],
    )
    write_md(
        stage_root / "04_selected" / "selection_status.md",
        f"""# Stage293 Selection Status(293단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{next_stage_id}_v1`
- current_run(현재 실행): `not_started`
- source_stage(원천 단계): `{STAGE_ID}`
- target_candidate(목표 후보): `{target}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- input_refs(입력 참조): `{rel(stage_root / "01_inputs" / "input_refs.md")}`
""",
    )


def update_docs(
    created_at: str,
    artifacts: Sequence[Path],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any] | None,
    status: str,
    judgment: str,
    next_action: str,
    next_stage_id: str,
) -> None:
    selected_text = selected["package_id"] if selected else "none"
    upsert_csv(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "anti_direction_meta_trade_sim_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "notes": f"scoreboard_rows={len(scoreboard_rows)};failure_rows={len(failure_rows)};selected_candidate={selected_text};target_stage={next_stage_id};next_action={next_action}",
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
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "anti_direction_meta_trade_sim_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_selection_review",
                "scoreboard_lane": "anti_direction_meta_trade_sim",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": f"scoreboard_rows={len(scoreboard_rows)};selected_candidate={selected_text}",
                "guardrail_kpi": "adapter_package=none;onnx_readiness=not_started",
                "external_verification_status": "completed_run292B_mt5_probe",
                "notes": f"target_stage={next_stage_id};next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "anti_direction_meta_trade_sim_review",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "anti_direction_meta_trade_sim_review_scoreboard",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "candidate_gate_review_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"target_stage={next_stage_id};selected_candidate={selected_text}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage292_anti_direction_meta_trade_sim_review_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run292C anti-direction meta trade simulator review and Stage293 handoff",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_next_stage_scaffold(queue_rows, selected, next_stage_id, next_action)

    write_md(
        SELECTED,
        f"""# Stage292 Selection Status(292단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `Stage291`
- selected_candidate(선택 후보): `{selected_text}`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- report(보고): `{rel(REPORT)}`
- scoreboard(점수표): `{rel(SCOREBOARD)}`
""",
    )
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage292 Review Index(292단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run292C_report",
        f"- run292C_report(292C 보고): `{rel(REPORT)}`\n- run292C_scoreboard(292C 점수표): `{rel(SCOREBOARD)}`\n- run292C_failure_memory(292C 실패 기억): `{rel(FAILURE_MEMORY)}`",
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{next_stage_id}`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_once(
        current,
        "run292C_summary",
        f"- run292C_summary(292C 요약): Stage292(292단계) MT5 actual routed total(MT5 실제 라우팅 전체)을 검토했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_text}`이고 Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage292(292단계) run292C(292C 실행) anti-direction meta trade simulator review(반대방향 메타 거래 시뮬레이터 검토) `{RUN_ID}`. "
        f"Effect(효과): scoreboard(점수표) `{len(scoreboard_rows)}`행, failure memory(실패 기억) `{len(failure_rows)}`행, selected candidate(선택 후보) `{selected_text}`로 `{next_stage_id}`를 열었다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run292C Anti-direction meta trade sim review(292C 반대방향 메타 거래 시뮬레이터 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): Stage292(292단계)를 `{selected_text}` 선택 상태로 판정하고 `{next_stage_id}`를 열었다.\n"
        f"- boundary(경계): Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 `not_started/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)
    update_registers(selected, next_stage_id)


def update_registers(selected: Mapping[str, Any] | None, next_stage_id: str) -> None:
    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "Register ideas when they become durable work.\n"
    if selected and "IDEA-ST293-ADAPTER-FOR-STAGE292-CANDIDATE" not in idea:
        idea = (
            idea.rstrip()
            + f"\n\n| `IDEA-ST293-ADAPTER-FOR-STAGE292-CANDIDATE` | `{next_stage_id}` | Adapter package(어댑터 패키지) for Stage292 candidate(292단계 후보) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_after_candidate_gate` | 후보 게이트는 통과했지만 ONNX(온엑스)는 Adapter(어댑터)와 parity(동등성) 이후에만 진행 |\n"
        )
        write_md(IDEA_REGISTER, idea)
    if not selected and "IDEA-ST293-PROFIT-SCALE-DENSITY-CALIBRATION" not in idea:
        idea = (
            idea.rstrip()
            + f"\n\n| `IDEA-ST293-PROFIT-SCALE-DENSITY-CALIBRATION` | `{next_stage_id}` | runtime-aware profit-scale/density/curve calibration(런타임 인식 순수익 규모/밀도/곡선 보정) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage292(292단계)의 proxy-runtime gap(대리-런타임 공백)을 새 구조 논제로 전환 |\n"
        )
        write_md(IDEA_REGISTER, idea)

    if not selected:
        negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        if "NEG-ST292-ANTI-DIRECTION-META-TRADE-SIM" not in negative:
            negative = (
                negative.rstrip()
                + "\n\n| `NEG-ST292-ANTI-DIRECTION-META-TRADE-SIM` | `IDEA-ST292-ANTI-DIRECTION-META-LABEL-TRADE-SIM` | anti-direction/meta trade simulator(반대방향/메타 거래 시뮬레이터)가 ONNX-worthy candidate(ONNX화 가치 후보)로 닫히지 않음 | run292C(292C 실행)에서 최소 거래수, 일 4-10거래, 순수익 규모, PF(수익 팩터), 회복, 기대값, 곡선 포켓을 함께 통과한 패키지가 없음 | proxy(대리값)와 MT5 runtime(MT5 런타임)의 공백을 실패 기억으로 보존 | 새 runtime-aware simulator calibration(런타임 인식 시뮬레이터 보정)이나 curve objective(곡선 목적함수)일 때만 재개 |\n"
            )
            write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    created_at = utc_now()
    scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, pocket_rows, failure_rows, queue_rows, selected = build_outputs()
    status, judgment, next_action, next_stage_id = status_pack(selected)
    artifacts = write_outputs(
        scoreboard_rows,
        monthly_rows,
        session_rows,
        quality_rows,
        curve_rows,
        pocket_rows,
        failure_rows,
        queue_rows,
        selected,
        created_at,
        status,
        judgment,
        next_action,
        next_stage_id,
    )
    update_docs(
        created_at,
        artifacts,
        scoreboard_rows,
        failure_rows,
        queue_rows,
        selected,
        status,
        judgment,
        next_action,
        next_stage_id,
    )
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "scoreboard_rows": len(scoreboard_rows),
                "failure_rows": len(failure_rows),
                "selected_candidate": selected["package_id"] if selected else "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "next_action": next_action,
                "next_stage_id": next_stage_id,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
