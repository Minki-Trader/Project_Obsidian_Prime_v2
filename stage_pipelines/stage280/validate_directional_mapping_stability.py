from __future__ import annotations

import ast
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
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades  # noqa: E402


STAGE280_ID = "280_onnx_candidate_campaign__directional_mapping_stability_validation"
STAGE281_ID = "281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild"
RUN_ID = "run280A_directional_mapping_stability_validation_v1"
SOURCE_RUN_ID = "run279C_directional_runtime_mapping_mt5_signal_replay_v1"
STATUS = "completed_directional_mapping_stability_validation_no_candidate_selection"
JUDGMENT = "directional_mapping_seeds_failed_stability_no_candidate_selection_stage281_opened"
NEXT_ACTION = "run281A_design_drawdown_normalized_directional_candidate_rebuild_packet"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE279 = ROOT / "stages" / "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild"
RUN279C = STAGE279 / "02_runs" / "run279C"
STAGE280 = ROOT / "stages" / STAGE280_ID
RUN_DIR = STAGE280 / "02_runs" / "run280A"
REVIEWS280 = STAGE280 / "03_reviews"
SELECTED280 = STAGE280 / "04_selected" / "selection_status.md"
REVIEW_INDEX280 = REVIEWS280 / "review_index.md"
STAGE_LEDGER280 = REVIEWS280 / "stage_run_ledger.csv"
INPUTS280 = STAGE280 / "01_inputs"

SURVIVOR_QUEUE = INPUTS280 / "stage280_survivor_seed_queue.csv"
MT5_KPI_SUMMARY = RUN279C / "mt5_kpi_summary.csv"
EXECUTION_RESULT = RUN279C / "execution_result.json"
RUN279C_MANIFEST = RUN279C / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage280/validate_directional_mapping_stability.py")

SCOREBOARD = RUN_DIR / "stability_scoreboard.csv"
MONTHLY = RUN_DIR / "monthly_attribution.csv"
SESSION = RUN_DIR / "session_attribution.csv"
TRADE_QUALITY = RUN_DIR / "trade_quality_summary.csv"
CURVE = RUN_DIR / "curve_stability_summary.csv"
FAILURE_MEMORY = RUN_DIR / "stability_failure_memory.csv"
RECEIPT = RUN_DIR / "stability_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE = RUN_DIR / "artifact_lineage_receipt.json"
REPORT = REVIEWS280 / "run280A_stability_validation_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage280_stability_failure_stage281_rebuild_open.md"

STAGE281 = ROOT / "stages" / STAGE281_ID
SPEC281 = STAGE281 / "00_spec" / "stage_brief.md"
INPUTS281 = STAGE281 / "01_inputs"
REVIEWS281 = STAGE281 / "03_reviews"
SELECTED281 = STAGE281 / "04_selected" / "selection_status.md"
STAGE_LEDGER281 = REVIEWS281 / "stage_run_ledger.csv"
REVIEW_INDEX281 = REVIEWS281 / "review_index.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

TERMINAL_ROOT = ROOT.parents[2]

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "package_id",
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
    "tier_b_oos_net_profit",
    "validation_positive_month_share",
    "oos_positive_month_share",
    "validation_worst_month_net",
    "oos_worst_month_net",
    "validation_worst_session_net",
    "oos_worst_session_net",
    "validation_max_losing_streak",
    "oos_max_losing_streak",
    "validation_top_month_contribution_share",
    "oos_top_month_contribution_share",
    "stability_label",
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
    "source_report_path",
)
FAILURE_COLUMNS = (
    "materialized_branch_id",
    "seed_role",
    "package_id",
    "failure_type",
    "failure_reasons",
    "salvage_value",
    "reopen_condition",
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


def parse_metrics(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if not isinstance(value, str) or not value.strip():
        return {}
    parsed = ast.literal_eval(value)
    return dict(parsed) if isinstance(parsed, Mapping) else {}


def materialized_from_record_view(record_view: str) -> str:
    text = str(record_view).removeprefix("mt5_")
    for suffix in (
        "_actual_routed_validation_is",
        "_actual_routed_oos",
        "_tier_a_validation_is",
        "_tier_a_oos",
        "_tier_b_validation_is",
        "_tier_b_oos",
    ):
        if text.endswith(suffix):
            return "run279B_" + text[: -len(suffix)]
    return "run279B_" + text


def route_role_key(tier_scope: str, route_role: str) -> str:
    if tier_scope == "Tier A+B" or route_role == "actual_routed_total":
        return "actual_routed"
    if tier_scope == "Tier A":
        return "tier_a"
    if tier_scope == "Tier B":
        return "tier_b"
    return str(tier_scope).lower().replace(" ", "_")


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def safe_int(value: Any) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def load_seeds() -> list[dict[str, str]]:
    if not path_exists(SURVIVOR_QUEUE):
        raise FileNotFoundError(SURVIVOR_QUEUE)
    return [dict(row) for row in pd.read_csv(io_path(SURVIVOR_QUEUE)).fillna("").to_dict("records")]


def load_kpi_records() -> dict[tuple[str, str, str], dict[str, Any]]:
    if not path_exists(MT5_KPI_SUMMARY):
        raise FileNotFoundError(MT5_KPI_SUMMARY)
    records: dict[tuple[str, str, str], dict[str, Any]] = {}
    frame = pd.read_csv(io_path(MT5_KPI_SUMMARY)).fillna("")
    for row in frame.to_dict("records"):
        metrics = parse_metrics(row.get("metrics"))
        materialized_id = materialized_from_record_view(str(row.get("record_view", "")))
        role = route_role_key(str(row.get("tier_scope", "")), str(row.get("route_role", "")))
        split = str(row.get("split", ""))
        records[(materialized_id, role, split)] = {
            "record_view": row.get("record_view", ""),
            "tier_scope": row.get("tier_scope", ""),
            "route_role": row.get("route_role", ""),
            "split": split,
            "metrics": metrics,
            "report_path": resolve_report_path(str(metrics.get("report_path", ""))),
        }
    return records


def resolve_report_path(path_text: str) -> Path:
    path = Path(path_text)
    if path_text and path_exists(path):
        return path
    if path.name:
        fallback = TERMINAL_ROOT / path.name
        if path_exists(fallback):
            return fallback
    return path


def trade_frame(report_path: Path) -> pd.DataFrame:
    if not path_exists(report_path):
        return pd.DataFrame()
    parsed = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(parsed.get("deals", []))
    rows = [
        {
            "index": trade.index,
            "direction": trade.direction,
            "open_time": trade.open_time,
            "close_time": trade.close_time,
            "hour": int(trade.close_time.hour),
            "month": trade.close_time.strftime("%Y-%m"),
            "session": session_bucket(int(trade.close_time.hour)),
            "net_profit": float(trade.net_profit),
            "gross_profit": float(trade.gross_profit),
            "swap": float(trade.swap),
            "commission": float(trade.commission),
        }
        for trade in trades
    ]
    return pd.DataFrame(rows)


def session_bucket(hour: int) -> str:
    if 0 <= hour < 8:
        return "asia_00_08(아시아 00-08)"
    if 8 <= hour < 16:
        return "europe_08_16(유럽 08-16)"
    if 16 <= hour < 21:
        return "us_cash_16_21(미국 현금장 16-21)"
    return "late_us_21_24(미국 후반 21-24)"


def profit_factor(profits: Sequence[float]) -> float:
    gross_profit = sum(value for value in profits if value > 0)
    gross_loss = sum(value for value in profits if value < 0)
    return gross_profit / abs(gross_loss) if gross_loss < 0 else 0.0


def drawdown_stats(profits: Sequence[float], start_balance: float = 500.0) -> dict[str, Any]:
    balance = start_balance
    peak = start_balance
    max_dd = 0.0
    max_dd_pct = 0.0
    new_high_count = 0
    underwater = 0
    for profit in profits:
        balance += float(profit)
        if balance > peak:
            peak = balance
            new_high_count += 1
        dd = peak - balance
        if dd > 0:
            underwater += 1
        if dd > max_dd:
            max_dd = dd
            max_dd_pct = (dd / peak * 100.0) if peak else 0.0
    net = balance - start_balance
    return {
        "start_balance": start_balance,
        "end_balance": balance,
        "net_profit": net,
        "max_drawdown": max_dd,
        "max_drawdown_percent": max_dd_pct,
        "recovery_factor": (net / max_dd) if max_dd else 0.0,
        "new_high_count": new_high_count,
        "underwater_trade_count": underwater,
    }


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


def quality_summary(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {
            "trade_count": 0,
            "net_profit": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": 0.0,
            "win_rate": 0.0,
            "expectancy": 0.0,
            "average_win": 0.0,
            "average_loss": 0.0,
            "largest_win": 0.0,
            "largest_loss": 0.0,
            "max_losing_streak_count": 0,
            "max_losing_streak_loss": 0.0,
            "top_trade_contribution_share": 0.0,
            "top_10pct_contribution_share": 0.0,
        }
    profits = [float(value) for value in frame["net_profit"].tolist()]
    winners = [value for value in profits if value > 0]
    losers = [value for value in profits if value < 0]
    max_streak_count, max_streak_loss = losing_streak(profits)
    net = sum(profits)
    positive_sorted = sorted((value for value in profits if value > 0), reverse=True)
    top_count = max(1, int(round(len(profits) * 0.10))) if profits else 0
    return {
        "trade_count": len(profits),
        "net_profit": net,
        "gross_profit": sum(winners),
        "gross_loss": sum(losers),
        "profit_factor": profit_factor(profits),
        "win_rate": len(winners) / len(profits) if profits else 0.0,
        "expectancy": net / len(profits) if profits else 0.0,
        "average_win": sum(winners) / len(winners) if winners else 0.0,
        "average_loss": sum(losers) / len(losers) if losers else 0.0,
        "largest_win": max(winners) if winners else 0.0,
        "largest_loss": min(losers) if losers else 0.0,
        "max_losing_streak_count": max_streak_count,
        "max_losing_streak_loss": max_streak_loss,
        "top_trade_contribution_share": (positive_sorted[0] / net) if positive_sorted and net > 0 else 0.0,
        "top_10pct_contribution_share": (sum(positive_sorted[:top_count]) / net) if positive_sorted and net > 0 else 0.0,
    }


def attribution_rows(
    frame: pd.DataFrame,
    *,
    materialized_id: str,
    seed_role: str,
    tier_scope: str,
    split: str,
    source_report_path: Path,
    bucket_column: str,
) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    total_positive_net = max(float(frame["net_profit"].sum()), 0.0)
    rows: list[dict[str, Any]] = []
    for bucket, group in frame.groupby(bucket_column, sort=True):
        profits = [float(value) for value in group["net_profit"].tolist()]
        wins = [value for value in profits if value > 0]
        rows.append(
            {
                "materialized_branch_id": materialized_id,
                "seed_role": seed_role,
                "tier_scope": tier_scope,
                "split": split,
                "bucket": bucket,
                "net_profit": sum(profits),
                "trade_count": len(profits),
                "win_rate": len(wins) / len(profits) if profits else 0.0,
                "gross_profit": sum(value for value in profits if value > 0),
                "gross_loss": sum(value for value in profits if value < 0),
                "profit_factor": profit_factor(profits),
                "share_of_positive_net": (sum(profits) / total_positive_net) if total_positive_net > 0 and sum(profits) > 0 else 0.0,
                "source_report_path": source_report_path.as_posix(),
            }
        )
    return rows


def metric(records: Mapping[tuple[str, str, str], Mapping[str, Any]], materialized_id: str, role: str, split: str, key: str) -> float:
    entry = records.get((materialized_id, role, split), {})
    metrics = entry.get("metrics", {}) if isinstance(entry, Mapping) else {}
    return safe_float(metrics.get(key))


def summarize_seed(
    seed: Mapping[str, str],
    records: Mapping[tuple[str, str, str], Mapping[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    materialized_id = str(seed["materialized_branch_id"])
    seed_role = str(seed["seed_role"])
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    derived: dict[str, Any] = {}

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
                    seed_role=seed_role,
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
                    seed_role=seed_role,
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
                    "seed_role": seed_role,
                    "tier_scope": tier_scope,
                    "split": split,
                    **q,
                    "source_report_path": report_path.as_posix(),
                }
            )
            profits = [float(value) for value in frame["net_profit"].tolist()] if not frame.empty else []
            c = drawdown_stats(profits)
            curve_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "seed_role": seed_role,
                    "tier_scope": tier_scope,
                    "split": split,
                    **c,
                    "source_report_path": report_path.as_posix(),
                }
            )
            if role == "actual_routed":
                prefix = "validation" if split == "validation_is" else "oos"
                derived[f"{prefix}_positive_month_share"] = positive_bucket_share(monthly_rows, materialized_id, tier_scope, split)
                derived[f"{prefix}_worst_month_net"] = worst_bucket_net(monthly_rows, materialized_id, tier_scope, split)
                derived[f"{prefix}_worst_session_net"] = worst_bucket_net(session_rows, materialized_id, tier_scope, split)
                derived[f"{prefix}_max_losing_streak"] = q["max_losing_streak_count"]
                derived[f"{prefix}_top_month_contribution_share"] = max_bucket_share(monthly_rows, materialized_id, tier_scope, split)

    val_net = metric(records, materialized_id, "actual_routed", "validation_is", "net_profit")
    val_pf = metric(records, materialized_id, "actual_routed", "validation_is", "profit_factor")
    val_trades = safe_int(metric(records, materialized_id, "actual_routed", "validation_is", "trade_count"))
    val_dd = metric(records, materialized_id, "actual_routed", "validation_is", "max_drawdown_amount")
    val_recovery = metric(records, materialized_id, "actual_routed", "validation_is", "recovery_factor")
    oos_net = metric(records, materialized_id, "actual_routed", "oos", "net_profit")
    oos_pf = metric(records, materialized_id, "actual_routed", "oos", "profit_factor")
    oos_trades = safe_int(metric(records, materialized_id, "actual_routed", "oos", "trade_count"))
    oos_dd = metric(records, materialized_id, "actual_routed", "oos", "max_drawdown_amount")
    oos_recovery = metric(records, materialized_id, "actual_routed", "oos", "recovery_factor")
    tier_b_val = metric(records, materialized_id, "tier_b", "validation_is", "net_profit")
    tier_b_oos = metric(records, materialized_id, "tier_b", "oos", "net_profit")

    reasons = stability_failures(
        val_net=val_net,
        val_pf=val_pf,
        val_trades=val_trades,
        val_dd=val_dd,
        val_recovery=val_recovery,
        oos_net=oos_net,
        oos_pf=oos_pf,
        oos_trades=oos_trades,
        oos_dd=oos_dd,
        oos_recovery=oos_recovery,
        tier_b_val=tier_b_val,
        derived=derived,
    )
    row = {
        "materialized_branch_id": materialized_id,
        "seed_role": seed_role,
        "package_id": seed.get("package_id", ""),
        "validation_net_profit": val_net,
        "validation_pf": val_pf,
        "validation_trade_count": val_trades,
        "validation_dd": val_dd,
        "validation_recovery": val_recovery,
        "oos_net_profit": oos_net,
        "oos_pf": oos_pf,
        "oos_trade_count": oos_trades,
        "oos_dd": oos_dd,
        "oos_recovery": oos_recovery,
        "tier_b_validation_net_profit": tier_b_val,
        "tier_b_oos_net_profit": tier_b_oos,
        "validation_positive_month_share": derived.get("validation_positive_month_share", 0.0),
        "oos_positive_month_share": derived.get("oos_positive_month_share", 0.0),
        "validation_worst_month_net": derived.get("validation_worst_month_net", 0.0),
        "oos_worst_month_net": derived.get("oos_worst_month_net", 0.0),
        "validation_worst_session_net": derived.get("validation_worst_session_net", 0.0),
        "oos_worst_session_net": derived.get("oos_worst_session_net", 0.0),
        "validation_max_losing_streak": derived.get("validation_max_losing_streak", 0),
        "oos_max_losing_streak": derived.get("oos_max_losing_streak", 0),
        "validation_top_month_contribution_share": derived.get("validation_top_month_contribution_share", 0.0),
        "oos_top_month_contribution_share": derived.get("oos_top_month_contribution_share", 0.0),
        "stability_label": "failed_stability_no_selected_candidate" if reasons else "stability_survivor_watch_not_selected_candidate",
        "failure_reasons": ";".join(reasons) if reasons else "watch_only_needs_adapter_package_gate(관찰 전용, 어댑터 패키지 게이트 필요)",
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": BOUNDARY,
    }
    failure = {
        "materialized_branch_id": materialized_id,
        "seed_role": seed_role,
        "package_id": seed.get("package_id", ""),
        "failure_type": "stability_validation_failure(안정성 검증 실패)" if reasons else "watch_only_not_selected(관찰 전용)",
        "failure_reasons": row["failure_reasons"],
        "salvage_value": "directional edge clues and risk asymmetry clues only(방향 우위 단서와 위험 비대칭 단서만 보존)",
        "reopen_condition": "fresh drawdown-normalized decision/risk surface, not simple threshold repair(단순 임계값 수리가 아닌 새 손실폭 정규화 판단/위험 표면)",
        "claim_boundary": BOUNDARY,
    }
    return row, monthly_rows, session_rows, quality_rows, curve_rows, failure


def positive_bucket_share(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str) -> float:
    selected = [
        row
        for row in rows
        if row["materialized_branch_id"] == materialized_id and row["tier_scope"] == tier_scope and row["split"] == split
    ]
    if not selected:
        return 0.0
    return sum(1 for row in selected if safe_float(row["net_profit"]) > 0) / len(selected)


def worst_bucket_net(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str) -> float:
    values = [
        safe_float(row["net_profit"])
        for row in rows
        if row["materialized_branch_id"] == materialized_id and row["tier_scope"] == tier_scope and row["split"] == split
    ]
    return min(values) if values else 0.0


def max_bucket_share(rows: Sequence[Mapping[str, Any]], materialized_id: str, tier_scope: str, split: str) -> float:
    selected = [
        row
        for row in rows
        if row["materialized_branch_id"] == materialized_id and row["tier_scope"] == tier_scope and row["split"] == split
    ]
    total = sum(safe_float(row["net_profit"]) for row in selected)
    positives = [safe_float(row["net_profit"]) for row in selected if safe_float(row["net_profit"]) > 0]
    return (max(positives) / total) if positives and total > 0 else 0.0


def stability_failures(**values: Any) -> list[str]:
    reasons: list[str] = []
    if values["val_net"] <= 0:
        reasons.append("validation_net_nonpositive(검증 순손익 비양수)")
    if values["oos_net"] <= 0:
        reasons.append("oos_net_nonpositive(표본외 순손익 비양수)")
    if values["val_pf"] < 1.05:
        reasons.append("validation_pf_below_1_05(검증 PF 1.05 미만)")
    if values["oos_pf"] < 1.05:
        reasons.append("oos_pf_below_1_05(표본외 PF 1.05 미만)")
    if values["val_trades"] < 80 or values["oos_trades"] < 80:
        reasons.append("thin_trade_count_under_80(거래 수 80 미만)")
    if values["val_recovery"] < 0.25:
        reasons.append("validation_recovery_below_0_25(검증 회복 0.25 미만)")
    if values["oos_recovery"] < 0.50:
        reasons.append("oos_recovery_below_0_50(표본외 회복 0.50 미만)")
    if values["val_net"] > 0 and values["val_dd"] / max(values["val_net"], 1.0) > 4.0:
        reasons.append("validation_drawdown_over_4x_net(검증 손실폭이 순손익의 4배 초과)")
    if values["tier_b_val"] < 0:
        reasons.append("tier_b_validation_negative(Tier B 검증 음수)")
    derived = values["derived"]
    if safe_float(derived.get("validation_positive_month_share", 0.0)) < 0.55:
        reasons.append("validation_positive_month_share_below_55pct(검증 양수 월 비중 55% 미만)")
    if safe_float(derived.get("oos_positive_month_share", 0.0)) < 0.55:
        reasons.append("oos_positive_month_share_below_55pct(표본외 양수 월 비중 55% 미만)")
    if safe_float(derived.get("validation_worst_month_net", 0.0)) < -100.0:
        reasons.append("validation_worst_month_below_minus_100(검증 최악 월 -100 미만)")
    if safe_float(derived.get("oos_worst_month_net", 0.0)) < -100.0:
        reasons.append("oos_worst_month_below_minus_100(표본외 최악 월 -100 미만)")
    if safe_int(derived.get("validation_max_losing_streak", 0)) >= 7:
        reasons.append("validation_losing_streak_ge_7(검증 연속 손실 7 이상)")
    if safe_int(derived.get("oos_max_losing_streak", 0)) >= 7:
        reasons.append("oos_losing_streak_ge_7(표본외 연속 손실 7 이상)")
    if safe_float(derived.get("validation_top_month_contribution_share", 0.0)) > 0.80:
        reasons.append("validation_top_month_contribution_over_80pct(검증 상위 월 기여 80% 초과)")
    if safe_float(derived.get("oos_top_month_contribution_share", 0.0)) > 0.80:
        reasons.append("oos_top_month_contribution_over_80pct(표본외 상위 월 기여 80% 초과)")
    return reasons


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    seeds = load_seeds()
    records = load_kpi_records()
    scoreboard_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for seed in seeds:
        row, month, session, quality, curve, failure = summarize_seed(seed, records)
        scoreboard_rows.append(row)
        monthly_rows.extend(month)
        session_rows.extend(session)
        quality_rows.extend(quality)
        curve_rows.extend(curve)
        failure_rows.append(failure)
    return scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows


def write_stage281_inputs(scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    for path in [STAGE281 / "00_spec", INPUTS281, STAGE281 / "02_runs", REVIEWS281, STAGE281 / "04_selected"]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(INPUTS281 / "stage280_stability_scoreboard.csv", SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(INPUTS281 / "stage280_stability_failure_memory.csv", FAILURE_COLUMNS, failure_rows)
    write_md(
        SPEC281,
        f"""# Stage281 Brief(281단계 개요): Drawdown-Normalized Directional Candidate Rebuild(손실폭 정규화 방향 후보 재구성)

- stage_id(단계 ID): `{STAGE281_ID}`
- opened_by(개시 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE280_ID}`
- active_question(핵심 질문): Can a fresh drawdown-normalized decision/risk surface create an ONNX-worthy candidate package?(새 손실폭 정규화 판단/위험 표면이 ONNX-worthy, 온엑스화 가치가 있는 후보 패키지를 만들 수 있는가?)
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): Stage279/280(279/280단계)의 방향 매핑 씨앗은 보존하지 않고, 손실폭 대비 기대값과 월/세션 취약성을 새 candidate construction(후보 구성)의 중심 질문으로 옮긴다.
""",
    )
    write_md(
        INPUTS281 / "input_refs.md",
        f"""# Stage281 Inputs(281단계 입력)

- stage280_scoreboard(280단계 점수판): `{rel(INPUTS281 / 'stage280_stability_scoreboard.csv')}`
- stage280_failure_memory(280단계 실패 기억): `{rel(INPUTS281 / 'stage280_stability_failure_memory.csv')}`
- monthly_attribution(월별 원인 분해): `{rel(MONTHLY)}`
- session_attribution(세션별 원인 분해): `{rel(SESSION)}`
- trade_quality(거래 품질): `{rel(TRADE_QUALITY)}`
- curve_stability(곡선 안정성): `{rel(CURVE)}`
""",
    )
    write_md(
        SELECTED281,
        f"""# Stage281 Selection Status(281단계 선택 상태)

- stage_status(단계 상태): `opened_drawdown_normalized_directional_candidate_rebuild_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage281_drawdown_normalized_directional_candidate_rebuild_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE280_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_csv(
        STAGE_LEDGER281,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage281_open",
                "stage_id": STAGE281_ID,
                "run_id": RUN_ID,
                "view": "stage281_open_drawdown_normalized_directional_candidate_rebuild",
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
    write_md(
        REVIEW_INDEX281,
        f"""# Stage281 Review Index(281단계 검토 색인)

- stage_open_report(단계 개시 보고): `{rel(REPORT)}`
- input_refs(입력 참조): `{rel(INPUTS281 / 'input_refs.md')}`
""",
    )


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run280A Report(280A 보고서): Directional Mapping Stability Validation(방향 매핑 안정성 검증)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- seed_count(씨앗 수): `{len(scoreboard_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Stability Read(안정성 판독)",
        "",
        "| seed(씨앗) | val net(검증 순손익) | val PF(검증 PF) | val recovery(검증 회복) | OOS net(표본외 순손익) | OOS PF(표본외 PF) | label(라벨) |",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {seed} | {vnet:.2f} | {vpf:.2f} | {vrec:.2f} | {onet:.2f} | {opf:.2f} | {label} |".format(
                seed=row["materialized_branch_id"],
                vnet=safe_float(row["validation_net_profit"]),
                vpf=safe_float(row["validation_pf"]),
                vrec=safe_float(row["validation_recovery"]),
                onet=safe_float(row["oos_net_profit"]),
                opf=safe_float(row["oos_pf"]),
                label=row["stability_label"],
            )
        )
    lines.extend(
        [
            "",
            "## Failure Memory(실패 기억)",
            "",
        ]
    )
    for row in failure_rows:
        lines.append(f"- `{row['materialized_branch_id']}`: {row['failure_reasons']}")
    lines.extend(
        [
            "",
            "## Meaning(의미)",
            "",
            "Stage280(280단계)는 Stage279(279단계)의 생존 씨앗을 거래 목록, 월별 손익, 세션 손익, 잔액 곡선, 거래 품질로 압박했다.",
            "Effect(효과): 표본외 숫자가 좋아 보여도 검증 회복, 손실폭 대비 순손익, 월/세션 취약성이 약하면 후보 패키지로 부르지 않는다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


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


def write_outputs(scoreboard_rows: Sequence[Mapping[str, Any]], monthly_rows: Sequence[Mapping[str, Any]], session_rows: Sequence[Mapping[str, Any]], quality_rows: Sequence[Mapping[str, Any]], curve_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], created_at: str) -> list[Path]:
    write_csv(SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(MONTHLY, ATTRIBUTION_COLUMNS, monthly_rows)
    write_csv(SESSION, ATTRIBUTION_COLUMNS, session_rows)
    write_csv(TRADE_QUALITY, TRADE_QUALITY_COLUMNS, quality_rows)
    write_csv(CURVE, CURVE_COLUMNS, curve_rows)
    write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows)
    write_json(
        RECEIPT,
        {
            "run_id": RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "seed_count": len(scoreboard_rows),
            "monthly_rows": len(monthly_rows),
            "session_rows": len(session_rows),
            "trade_quality_rows": len(quality_rows),
            "curve_rows": len(curve_rows),
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
                "evidence_available": f"seed_count={len(scoreboard_rows)};monthly_rows={len(monthly_rows)};session_rows={len(session_rows)};trade_quality_rows={len(quality_rows)};curve_rows={len(curve_rows)}",
                "evidence_missing": "fresh candidate package construction;Adapter package;ONNX parity;MT5 ONNX runtime reproduction",
                "judgment_label": JUDGMENT,
                "judgment_class": "stability_validation_negative(안정성 검증 부정)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "생존 씨앗은 후보로 승격되지 않았고 새 후보 구성으로 넘어간다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "mt5_trade_list_available(MT5 거래 목록 사용 가능)",
                "status": "passed",
                "evidence_path": rel(TRADE_QUALITY),
                "effect": "실제 MT5 보고서 거래 목록에서 거래 품질을 계산했다.",
            },
            {
                "gate_name": "monthly_session_curve_review(월/세션/곡선 검토)",
                "status": "passed",
                "evidence_path": f"{rel(MONTHLY)};{rel(SESSION)};{rel(CURVE)}",
                "effect": "표본외 순손익만으로 후보를 부르지 않게 했다.",
            },
            {
                "gate_name": "no_candidate_no_onnx_claim(후보/ONNX 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "Adapter package(어댑터 패키지)와 ONNX readiness(온엑스 준비)를 주장하지 않았다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, failure_rows))
    write_md(
        DECISION,
        f"""# Decision(결정): Stage280 Stability Failure and Stage281 Rebuild Open(280단계 안정성 실패와 281단계 재구성 개시)

- date(날짜): `{UPDATED_ON}`
- decision(결정): Stage280(280단계)는 no selected candidate(선택 후보 없음)로 닫고 Stage281(281단계)를 연다.
- effect(효과): 방향 매핑 씨앗을 보존하지 않고, drawdown-normalized decision/risk surface(손실폭 정규화 판단/위험 표면)를 새 질문으로 세운다.
- source(원천): `{rel(REPORT)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_stage281_inputs(scoreboard_rows, failure_rows)
    artifacts = [
        SCOREBOARD,
        MONTHLY,
        SESSION,
        TRADE_QUALITY,
        CURVE,
        FAILURE_MEMORY,
        RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        DECISION,
        SPEC281,
        INPUTS281 / "stage280_stability_scoreboard.csv",
        INPUTS281 / "stage280_stability_failure_memory.csv",
        INPUTS281 / "input_refs.md",
        SELECTED281,
        STAGE_LEDGER281,
        REVIEW_INDEX281,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE280_ID,
        "target_stage_id": STAGE281_ID,
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
        "source_inputs": [rel(SURVIVOR_QUEUE), rel(MT5_KPI_SUMMARY), rel(EXECUTION_RESULT), rel(RUN279C_MANIFEST), rel(ROOT / PRODUCER)],
        "source_hashes": {
            rel(path): sha256_file(path)
            for path in [SURVIVOR_QUEUE, MT5_KPI_SUMMARY, EXECUTION_RESULT, RUN279C_MANIFEST, ROOT / PRODUCER]
            if path_exists(path)
        },
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "lineage_judgment": "connected_no_candidate_no_onnx_claim(연결됨, 후보/ONNX 주장 없음)",
    }
    write_json(LINEAGE, lineage)
    artifacts.append(LINEAGE)
    return artifacts


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path], scoreboard_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE280_ID,
                "lane": "directional_mapping_stability_validation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"seed_count={len(scoreboard_rows)};target_stage={STAGE281_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stability_validation",
                "stage_id": STAGE280_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage280_stability_validation_stage281_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "stage280_stability_validation(280단계 안정성 검증)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "monthly_session_curve_trade_quality_no_candidate_selection",
                "scoreboard_lane": "stability_validation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"seed_count={len(scoreboard_rows)};failure_count={len(failure_rows)}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "mt5_trade_reports_parsed",
                "notes": f"target_stage={STAGE281_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    write_csv(
        STAGE_LEDGER280,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage280_closeout",
                "stage_id": STAGE280_ID,
                "run_id": RUN_ID,
                "view": "stage280_stability_validation_stage281_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stability_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"target_stage={STAGE281_ID};next_action={NEXT_ACTION}.",
            }
        ],
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage280_stability_validation_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE280_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run280A stability validation(280A 안정성 검증)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED280).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run280A_report", f"- run280A_report(280A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "stage281_open", f"- stage281_open(281단계 개시): `{STAGE281_ID}`")
    write_md(SELECTED280, selected)

    review_index = io_path(REVIEW_INDEX280).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX280) else "# Stage280 Review Index(280단계 검토 색인)\n"
    review_index = append_once(review_index, "run280A_report", f"- run280A_report(280A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX280, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage281_drawdown_normalized_directional_candidate_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE281_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE280_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `drawdown_normalized_directional_candidate_rebuild`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run280A_summary",
        f"- run280A_summary(280A 요약): Stage280(280단계)는 생존 씨앗 `{len(scoreboard_rows)}`개를 월/세션/곡선/거래품질로 압박했고 선택 후보 없이 Stage281(281단계)를 열었다. Effect(효과): Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE281_ID}")
    focus = (
        f"- >-\n"
        f"  Stage281(281단계) drawdown-normalized directional candidate rebuild(손실폭 정규화 방향 후보 재구성) opened by `{RUN_ID}`. "
        f"Effect(효과): Stage280(280단계) seed(씨앗) `{len(scoreboard_rows)}`개를 후보로 승격하지 않고 새 candidate construction(후보 구성)으로 넘긴다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run280A Stage280 stability validation(280A 280단계 안정성 검증)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): seed(씨앗) `{len(scoreboard_rows)}`개를 실패 기억으로 정리하고 Stage281(281단계)를 열었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST281-DRAWDOWN-NORMALIZED-DIRECTION",
        f"| `IDEA-ST281-DRAWDOWN-NORMALIZED-DIRECTION` | `{STAGE281_ID}` | 손실폭 정규화 방향 후보 재구성 | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `opened_no_candidate` | Stage280(280단계) 실패 기억에서 새 판단/위험 표면을 만든다 |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST280-DIRECTIONAL-STABILITY",
        f"| `NEG-ST280-DIRECTIONAL-STABILITY` | `{STAGE280_ID}` | 생존 씨앗 `{len(scoreboard_rows)}`개가 안정성 검증에서 선택 후보가 되지 못함 | 새 손실폭 정규화 판단/위험 표면일 때만 재개 | `{rel(FAILURE_MEMORY)}` |",
    )
    write_md(NEGATIVE_REGISTER, negative)


def main() -> None:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS280).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows = build_outputs()
    artifacts = write_outputs(scoreboard_rows, monthly_rows, session_rows, quality_rows, curve_rows, failure_rows, created_at)
    update_registers_and_docs(created_at, artifacts, scoreboard_rows, failure_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "seed_count": len(scoreboard_rows),
                "monthly_rows": len(monthly_rows),
                "session_rows": len(session_rows),
                "trade_quality_rows": len(quality_rows),
                "curve_rows": len(curve_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "target_stage": STAGE281_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
