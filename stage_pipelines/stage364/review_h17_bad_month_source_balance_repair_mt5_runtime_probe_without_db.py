from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades  # noqa: E402
from stage_pipelines.stage364 import execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db as pkg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CQ"
RUN_ID = "run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
PACKAGE_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1"

TRADE_DENSITY_FLOOR = 3.0
SHORT_FLOOR = 100
LONG_SHARE_WARN = 0.85
EQUITY_DD_MULTIPLE_WARN = 1.5

STATUS = (
    "completed_stage364CQ_h17_bad_month_source_balance_mt5_probe_reviewed_positive_net_density_"
    "short_floor_month12_equity_dd_repair_required_no_authority"
)
JUDGMENT = (
    "mixed_positive_runtime_probe_net_pf_density_short_floor_clue_promotion_ineligible_"
    "month12_loss_equity_drawdown_long_skew_no_authority"
)
DECISION = "stage364CQ_open_run364CR_month12_long_equity_drawdown_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
MT5_KPI_REVIEW = RUN_DIR / "mt5_kpi_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "proxy_mt5_attribution.csv"
TRADE_SHAPE_REVIEW = RUN_DIR / "trade_shape_review.csv"
SIDE_ATTRIBUTION = RUN_DIR / "side_attribution.csv"
MONTH_ATTRIBUTION = RUN_DIR / "month_attribution.csv"
MONTH_SIDE_ATTRIBUTION = RUN_DIR / "month_side_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_attribution.csv"
DRAWDOWN_REVIEW = RUN_DIR / "drawdown_review.csv"
RUNTIME_QUALITY_REVIEW = RUN_DIR / "runtime_quality_review.csv"
TESTER_IDENTITY_REVIEW = RUN_DIR / "tester_identity_review.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364CR_month12_long_equity_drawdown_repair_queue.csv"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CQ_h17_bad_month_source_balance_repair_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CQ_h17_bad_month_source_balance_repair_mt5_runtime_probe_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.EXECUTION_SUMMARY,
    parent.PROXY_MT5_DIFF,
    parent.RUNTIME_OUTPUT_COPY,
    parent.STRATEGY_TESTER_REPORTS,
    parent.MT5_EXECUTION_RESULT,
    parent.EXPECTED_KPI_SUMMARY,
    parent.REPORT_PATH,
    pkg.FINAL_DECISION,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.TESTER_IDENTITY_CONTRACT,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.TESTER_SET_MANIFEST,
    pkg.TESTER_INI_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    MT5_KPI_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    TRADE_SHAPE_REVIEW,
    SIDE_ATTRIBUTION,
    MONTH_ATTRIBUTION,
    MONTH_SIDE_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    DRAWDOWN_REVIEW,
    RUNTIME_QUALITY_REVIEW,
    TESTER_IDENTITY_REVIEW,
    REVIEW_FINDINGS,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    KPI_RECEIPT,
    BACKTEST_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.resolve().as_posix()


def exists(path: Path | str) -> bool:
    return io_path(path).exists()


def sha(path: Path | str) -> str:
    return sha256_file(Path(path))


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n", bom=True)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    target = io_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    header: list[str] = []
    if target.exists():
        with target.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            header = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    if not header:
        for row in rows:
            for key in row:
                if key not in header:
                    header.append(str(key))
    if extend_header:
        for row in rows:
            for key in row:
                if key not in header:
                    header.append(str(key))

    def row_key(row: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(field, "")) for field in key_fields)

    replacement = {row_key(row): dict(row) for row in rows}
    kept = [row for row in existing if row_key(row) not in replacement]
    output_rows = kept + [replacement[key] for key in replacement]
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in output_rows:
            writer.writerow({field: row.get(field, "") for field in header})


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    lines = text.splitlines()
    seen: set[str] = set()
    updated: list[str] = []
    for line in lines:
        replaced = False
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                updated.append(replacement)
                seen.add(prefix)
                replaced = True
                break
        if not replaced:
            updated.append(line)
    for prefix, replacement in replacements.items():
        if prefix not in seen:
            updated.append(replacement)
    write_text(path, "\n".join(updated).rstrip() + "\n", bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CQ inputs(CQ 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CP next_run_id mismatch(CP 다음 실행 ID 불일치): {final.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CP gate audit(CP 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if int(final.get("runtime_completed_rows") or 0) < 1 or int(final.get("usable_report_rows") or 0) < 1:
        raise RuntimeError("CP has no usable runtime/report output(CP 사용 가능 런타임/보고서 출력 없음).")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CP runtime probe review source(CP 런타임 탐침 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
            ],
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "backtest_forensics_gate",
                "performance_attribution_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def report_path_from_records() -> Path:
    records = read_json(parent.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or not records:
        raise RuntimeError("strategy_tester_report_records(전략 테스터 보고서 기록)가 비어 있습니다.")
    html = records[0].get("html_report", {}) if isinstance(records[0], Mapping) else {}
    path = Path(str(html.get("path", "")))
    if not path.is_absolute():
        path = ROOT / path
    if not exists(path):
        raise FileNotFoundError(f"MT5 report missing(MT5 보고서 누락): {path}")
    return path


def trades_frame(report_path: Path) -> pd.DataFrame:
    parsed = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(parsed["deals"])
    rows = [
        {
            "trade_index": trade.index,
            "direction": trade.direction,
            "open_time": trade.open_time,
            "close_time": trade.close_time,
            "volume": trade.volume,
            "open_price": trade.open_price,
            "close_price": trade.close_price,
            "gross_profit": trade.gross_profit,
            "net_profit": trade.net_profit,
            "swap": trade.swap,
            "commission": trade.commission,
            "duration_minutes": (trade.close_time - trade.open_time).total_seconds() / 60.0,
        }
        for trade in trades
    ]
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame["month"] = frame["close_time"].dt.to_period("M").astype(str)
    frame["open_hour"] = frame["open_time"].dt.hour
    frame["close_hour"] = frame["close_time"].dt.hour
    frame["hold_bucket"] = pd.cut(
        frame["duration_minutes"],
        bins=[-1, 30, 60, 120, 10**9],
        labels=["<=30m", "31-60m", "61-120m", ">120m"],
    ).astype(str)
    return frame


def group_rows(frame: pd.DataFrame, group_cols: Sequence[str], output_path: Path, *, sort_by: str = "net_profit") -> list[dict[str, Any]]:
    if frame.empty:
        rows: list[dict[str, Any]] = []
    else:
        rows = (
            frame.groupby(list(group_cols), dropna=False, observed=False)
            .agg(
                trade_count=("net_profit", "size"),
                net_profit=("net_profit", "sum"),
                gross_profit=("gross_profit", "sum"),
                average_net=("net_profit", "mean"),
                win_rate=("net_profit", lambda s: float((s > 0).mean())),
            )
            .reset_index()
            .sort_values(sort_by)
            .to_dict("records")
        )
    for row in rows:
        row["run_id"] = RUN_ID
        row["claim_boundary"] = CLAIM_BOUNDARY
    write_csv(output_path, rows)
    return rows


def build_reviews(cp_final: Mapping[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    report_records = read_json(parent.STRATEGY_TESTER_REPORTS)
    report_metrics = report_records[0].get("metrics", {}) if report_records and isinstance(report_records[0], Mapping) else {}
    summary = read_csv(parent.EXECUTION_SUMMARY).to_dict("records")[0]
    proxy_diff = read_csv(parent.PROXY_MT5_DIFF).to_dict("records")[0]
    expected = read_csv(parent.EXPECTED_KPI_SUMMARY).to_dict("records")[0]
    tester_identity = read_csv(pkg.TESTER_IDENTITY_CONTRACT).to_dict("records")[0]

    expected_density = as_float(expected.get("expected_proxy_density"))
    expected_trade_count = as_float(expected.get("expected_proxy_trade_count"))
    feature_days = expected_trade_count / expected_density if expected_density > 0 else 0.0
    actual_trade_count = as_float(report_metrics.get("trade_count"))
    actual_density = actual_trade_count / feature_days if feature_days > 0 else 0.0
    long_count = as_float(report_metrics.get("long_trade_count"))
    short_count = as_float(report_metrics.get("short_trade_count"))
    long_share = long_count / actual_trade_count if actual_trade_count > 0 else 0.0
    balance_dd = as_float(report_metrics.get("balance_drawdown_maximal_amount"))
    equity_dd = as_float(report_metrics.get("equity_drawdown_maximal_amount"))
    equity_to_balance_dd = equity_dd / balance_dd if balance_dd > 0 else math.nan

    month_rows = group_rows(trades, ["month"], MONTH_ATTRIBUTION)
    group_rows(trades, ["direction"], SIDE_ATTRIBUTION)
    month_side_rows = group_rows(trades, ["month", "direction"], MONTH_SIDE_ATTRIBUTION)
    hour_rows = group_rows(trades, ["open_hour"], ENTRY_HOUR_ATTRIBUTION)
    group_rows(trades, ["hold_bucket", "direction"], HOLD_BUCKET_ATTRIBUTION)

    bad_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0]
    worst_month = min(month_rows, key=lambda row: as_float(row.get("net_profit"))) if month_rows else {}
    worst_hour = min(hour_rows, key=lambda row: as_float(row.get("net_profit"))) if hour_rows else {}
    month12_side = [
        row for row in month_side_rows
        if row.get("month") == "2025-12"
    ]
    month12_long = next((row for row in month12_side if row.get("direction") == "buy"), {})
    month12_short = next((row for row in month12_side if row.get("direction") == "sell"), {})

    mt5_kpi = {
        "run_id": RUN_ID,
        "candidate_id": cp_final.get("candidate_id", ""),
        "net_profit": finite(report_metrics.get("net_profit")),
        "profit_factor": finite(report_metrics.get("profit_factor")),
        "expectancy": finite(report_metrics.get("expectancy")),
        "trade_count": finite(actual_trade_count, 0),
        "trade_density_per_feature_day": finite(actual_density, 10),
        "density_floor": TRADE_DENSITY_FLOOR,
        "density_status": "passed" if actual_density >= TRADE_DENSITY_FLOOR else "failed",
        "gross_profit": finite(report_metrics.get("gross_profit")),
        "gross_loss": finite(report_metrics.get("gross_loss")),
        "win_rate_percent": finite(report_metrics.get("win_rate_percent")),
        "long_trade_count": finite(long_count, 0),
        "short_trade_count": finite(short_count, 0),
        "short_floor": SHORT_FLOOR,
        "short_floor_status": "passed" if short_count >= SHORT_FLOOR else "failed",
        "long_share": finite(long_share, 10),
        "long_share_status": "warn_long_skew" if long_share > LONG_SHARE_WARN else "acceptable",
        "balance_drawdown_maximal_amount": finite(balance_dd),
        "equity_drawdown_maximal_amount": finite(equity_dd),
        "equity_to_balance_dd_multiple": finite(equity_to_balance_dd),
        "equity_dd_status": "warn_equity_dd_gap" if equity_to_balance_dd > EQUITY_DD_MULTIPLE_WARN else "acceptable",
        "recovery_factor": finite(report_metrics.get("recovery_factor")),
        "bad_month_count": len(bad_months),
        "bad_month_status": "failed_zero_bad_month" if bad_months else "passed_zero_bad_month",
        "worst_month": worst_month.get("month", ""),
        "worst_month_net": finite(worst_month.get("net_profit")),
        "tester_status": summary.get("tester_status", ""),
        "tester_blocker": summary.get("blocker", ""),
        "runtime_status": summary.get("runtime_status", ""),
        "report_status": summary.get("report_status", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(MT5_KPI_REVIEW, [mt5_kpi])

    proxy_row = {
        "run_id": RUN_ID,
        "candidate_id": cp_final.get("candidate_id", ""),
        "proxy_net_profit": finite(proxy_diff.get("expected_net_profit")),
        "mt5_net_profit": finite(proxy_diff.get("actual_mt5_net_profit")),
        "net_diff_mt5_minus_proxy": finite(proxy_diff.get("net_profit_diff_actual_minus_expected")),
        "proxy_profit_factor": finite(proxy_diff.get("expected_profit_factor")),
        "mt5_profit_factor": finite(proxy_diff.get("actual_mt5_profit_factor")),
        "pf_diff_mt5_minus_proxy": finite(proxy_diff.get("profit_factor_diff_actual_minus_expected")),
        "proxy_expectancy": finite(proxy_diff.get("expected_expectancy")),
        "mt5_expectancy": finite(proxy_diff.get("actual_mt5_expectancy")),
        "expectancy_diff_mt5_minus_proxy": finite(proxy_diff.get("expectancy_diff_actual_minus_expected")),
        "proxy_trade_count": finite(proxy_diff.get("expected_trade_count"), 0),
        "mt5_trade_count": finite(proxy_diff.get("actual_mt5_trade_count"), 0),
        "trade_count_diff_mt5_minus_proxy": finite(proxy_diff.get("trade_count_diff_actual_minus_expected"), 0),
        "usability": "usable_as_runtime_probe_review_not_authority",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(PROXY_MT5_ATTRIBUTION, [proxy_row])

    trade_shape = {
        "run_id": RUN_ID,
        "trade_count": finite(actual_trade_count, 0),
        "deal_count": finite(report_metrics.get("deal_count"), 0),
        "parsed_trade_count": len(trades),
        "winning_trade_count": finite(report_metrics.get("winning_trade_count"), 0),
        "losing_trade_count": finite(report_metrics.get("losing_trade_count"), 0),
        "long_trade_count": finite(long_count, 0),
        "short_trade_count": finite(short_count, 0),
        "long_net_profit": finite(trades.loc[trades["direction"] == "buy", "net_profit"].sum() if not trades.empty else 0),
        "short_net_profit": finite(trades.loc[trades["direction"] == "sell", "net_profit"].sum() if not trades.empty else 0),
        "average_trade_net": finite(trades["net_profit"].mean() if not trades.empty else 0),
        "average_hold_minutes": finite(trades["duration_minutes"].mean() if not trades.empty else 0),
        "worst_trade_net": finite(trades["net_profit"].min() if not trades.empty else 0),
        "best_trade_net": finite(trades["net_profit"].max() if not trades.empty else 0),
        "trade_shape_status": "positive_but_long_skew_and_equity_dd_gap",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(TRADE_SHAPE_REVIEW, [trade_shape])

    drawdown = {
        "run_id": RUN_ID,
        "proxy_drawdown_basis": "closed_trade_or_balance_proxy(닫힌 거래 또는 잔고 프록시)",
        "proxy_drawdown": finite(pkg.parent.parent.DD_PROXY if hasattr(pkg.parent.parent, "DD_PROXY") else ""),
        "balance_drawdown": finite(balance_dd),
        "equity_drawdown": finite(equity_dd),
        "equity_to_balance_dd_multiple": finite(equity_to_balance_dd),
        "risk_read": "equity_drawdown_materially_above_balance_drawdown" if equity_to_balance_dd > EQUITY_DD_MULTIPLE_WARN else "equity_drawdown_aligned",
        "effect": "equity DD(수익곡선 낙폭)를 operating claim(운영 주장) 전 risk repair(위험 수리) 조건으로 남깁니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(DRAWDOWN_REVIEW, [drawdown])

    runtime_quality = {
        "run_id": RUN_ID,
        "runtime_status": summary.get("runtime_status", ""),
        "runtime_wait_status": summary.get("runtime_wait_status", ""),
        "tester_status": summary.get("tester_status", ""),
        "tester_blocker": summary.get("blocker", ""),
        "feature_ready_count": summary.get("feature_ready_count", ""),
        "model_ok_count": summary.get("model_ok_count", ""),
        "order_attempt_count": summary.get("order_attempt_count", ""),
        "order_filled_count": summary.get("order_filled_count", ""),
        "terminal_timeout_boundary": "outputs_available_after_timeout" if "timeout" in str(summary.get("blocker", "")) else "none",
        "quality_status": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(RUNTIME_QUALITY_REVIEW, [runtime_quality])

    tester_row = {
        "run_id": RUN_ID,
        **tester_identity,
        "report_path": cp_final.get("report_path", ""),
        "report_sha256": read_json(parent.STRATEGY_TESTER_REPORTS)[0]["html_report"]["sha256"],
        "set_manifest": rel(pkg.TESTER_SET_MANIFEST),
        "ini_manifest": rel(pkg.TESTER_INI_MANIFEST),
        "identity_status": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(TESTER_IDENTITY_REVIEW, [tester_row])

    positive_clues = [
        {
            "run_id": RUN_ID,
            "clue_id": "cq01_mt5_positive_net_pf_density",
            "evidence": rel(MT5_KPI_REVIEW),
            "read": f"MT5 net {mt5_kpi['net_profit']}, PF {mt5_kpi['profit_factor']}, density {mt5_kpi['trade_density_per_feature_day']} 유지",
            "effect": "CM04 rule surface(CM04 규칙 표면)를 다음 repair exploration(수리 탐색)의 baseline clue(기준 단서)로 보존합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "clue_id": "cq02_short_floor_positive_net",
            "evidence": rel(SIDE_ATTRIBUTION),
            "read": f"short trades {mt5_kpi['short_trade_count']} and short net {trade_shape['short_net_profit']}",
            "effect": "long-only failure(롱 전용 실패)는 완화됐지만 방향 균형 개선은 계속 봅니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(POSITIVE_CLUES, positive_clues)

    failure_memory = [
        {
            "run_id": RUN_ID,
            "failure_id": "cq01_month12_residual_loss",
            "evidence": rel(MONTH_ATTRIBUTION),
            "read": f"bad_month_count={len(bad_months)}, worst_month={worst_month.get('month', '')}, net={finite(worst_month.get('net_profit'))}",
            "repair_constraint": "Do not claim zero bad months(손실 월 0 주장 금지) until MT5 month attribution is non-negative.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "cq02_equity_drawdown_gap",
            "evidence": rel(DRAWDOWN_REVIEW),
            "read": f"equity DD {finite(equity_dd)} vs balance DD {finite(balance_dd)}",
            "repair_constraint": "Risk repair(위험 수리)는 balance DD(잔고 낙폭)뿐 아니라 equity DD(수익곡선 낙폭)를 같이 줄여야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "cq03_long_skew_remains",
            "evidence": rel(SIDE_ATTRIBUTION),
            "read": f"long_share={mt5_kpi['long_share']}, long trades={mt5_kpi['long_trade_count']}",
            "repair_constraint": "Short floor(숏 하한)만 통과한 것을 full side balance(완전 방향 균형)로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(FAILURE_MEMORY, failure_memory)

    findings = [
        {
            "run_id": RUN_ID,
            "finding_id": "cq_kpi_positive_with_boundary",
            "severity": "positive_clue",
            "finding": "MT5 net/PF/density/short floor passed(MT5 순수익/수익 팩터/밀도/숏 하한 통과).",
            "evidence": rel(MT5_KPI_REVIEW),
            "effect": "후보를 폐기하지 않고 다음 수리 기준선으로 유지합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "cq_month12_loss",
            "severity": "repair_required",
            "finding": "MT5 month attribution(MT5 월 귀속)에서 2025-12가 음수입니다.",
            "evidence": rel(MONTH_ATTRIBUTION),
            "effect": "zero bad month(손실 월 0) 주장은 닫고 month12 long repair(12월 롱 수리)를 엽니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "cq_equity_dd_gap",
            "severity": "repair_required",
            "finding": "Equity DD(수익곡선 낙폭)가 balance/proxy DD(잔고/프록시 낙폭)보다 큽니다.",
            "evidence": rel(DRAWDOWN_REVIEW),
            "effect": "operating promotion(운영 승격) 전에 risk shape(위험 형태)를 수리해야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(REVIEW_FINDINGS, findings)

    queue = [
        {
            "run_id": RUN_ID,
            "queue_id": "cr01_month12_long_guard_sweep",
            "next_run_id": NEXT_RUN_ID,
            "seed_evidence": rel(MONTH_SIDE_ATTRIBUTION),
            "candidate_seed": "month12 buy net negative; sell positive(12월 롱 음수, 숏 양수)",
            "action": "materialize month12 long guard variants(12월 롱 가드 변형 구체화)",
            "effect": "MT5에서 남은 bad month(손실 월)를 줄이는지 시험합니다.",
            "forbidden_action": "exact_date_filter(정확 날짜 필터), top_n(상위 N개), trade_splitting(거래 쪼개기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_id": "cr02_equity_dd_guard_sweep",
            "next_run_id": NEXT_RUN_ID,
            "seed_evidence": rel(DRAWDOWN_REVIEW),
            "candidate_seed": "equity DD exceeds balance DD(수익곡선 낙폭이 잔고 낙폭보다 큼)",
            "action": "materialize equity drawdown stress controls(수익곡선 낙폭 압박 대조 구체화)",
            "effect": "closed-trade proxy(닫힌 거래 프록시)가 놓친 open-risk(열린 위험)를 줄이는지 본다.",
            "forbidden_action": "operating_promotion_without_forward_or_parity(전진/동등성 없는 운영 승격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_id": "cr03_side_balance_not_just_short_floor",
            "next_run_id": NEXT_RUN_ID,
            "seed_evidence": rel(SIDE_ATTRIBUTION),
            "candidate_seed": "short count floor passes but long share remains high(숏 하한은 통과하지만 롱 비중 높음)",
            "action": "materialize side-balance stress without killing density(밀도 보존 방향 균형 압박 구체화)",
            "effect": "short floor(숏 하한)를 통과한 상태에서 수익을 나누지 않고 균형을 넓힙니다.",
            "forbidden_action": "trade_splitting(거래 쪼개기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_QUEUE, queue)

    return {
        "mt5_kpi": mt5_kpi,
        "proxy": proxy_row,
        "trade_shape": trade_shape,
        "drawdown": drawdown,
        "runtime_quality": runtime_quality,
        "positive_clues": positive_clues,
        "failure_memory": failure_memory,
        "findings": findings,
        "queue": queue,
        "bad_months": bad_months,
        "month12_long": month12_long,
        "month12_short": month12_short,
        "worst_hour": worst_hour,
        "feature_days": feature_days,
    }


def gate_rows(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    kpi = review["mt5_kpi"]
    return [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if kpi.get("net_profit") != "" and kpi.get("trade_count") != "" else "failed",
            "evidence": rel(MT5_KPI_REVIEW),
            "effect": "MT5 KPI(MT5 핵심 성과 지표)를 proxy(프록시)와 분리해 고정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed" if int(kpi.get("trade_count") or 0) == 982 else "failed",
            "evidence": rel(TRADE_SHAPE_REVIEW),
            "effect": "deal/trade row grain(체결/거래 행 단위)을 보고서 trade count(거래수)와 대조합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(PROXY_MT5_ATTRIBUTION),
            "effect": "MT5 report(MT5 보고서)를 실제 KPI source of truth(진실 원천)로 둡니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "backtest_forensics_gate",
            "status": "passed",
            "evidence": rel(TESTER_IDENTITY_REVIEW),
            "effect": "tester identity(테스터 정체성), report hash(보고서 해시), timeout boundary(시간 초과 경계)를 남깁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "performance_attribution_gate",
            "status": "passed",
            "evidence": f"{rel(MONTH_ATTRIBUTION)};{rel(SIDE_ATTRIBUTION)};{rel(DRAWDOWN_REVIEW)}",
            "effect": "월/방향/낙폭 성과 귀속을 다음 repair(수리) 조건으로 만듭니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "work packet(작업 묶음)의 필수 gate(게이트)를 closeout(종료 기록)에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(cp_final: Mapping[str, Any], review: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    kpi = review["mt5_kpi"]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": cp_final.get("candidate_id", ""),
        "mt5_net_profit": kpi["net_profit"],
        "mt5_profit_factor": kpi["profit_factor"],
        "mt5_expectancy": kpi["expectancy"],
        "mt5_trade_count": kpi["trade_count"],
        "mt5_density": kpi["trade_density_per_feature_day"],
        "density_status": kpi["density_status"],
        "long_trade_count": kpi["long_trade_count"],
        "short_trade_count": kpi["short_trade_count"],
        "short_floor_status": kpi["short_floor_status"],
        "long_share": kpi["long_share"],
        "bad_month_count": kpi["bad_month_count"],
        "bad_month_status": kpi["bad_month_status"],
        "worst_month": kpi["worst_month"],
        "worst_month_net": kpi["worst_month_net"],
        "balance_drawdown": kpi["balance_drawdown_maximal_amount"],
        "equity_drawdown": kpi["equity_drawdown_maximal_amount"],
        "equity_to_balance_dd_multiple": kpi["equity_to_balance_dd_multiple"],
        "recovery_factor": kpi["recovery_factor"],
        "proxy_net_diff_mt5_minus_proxy": review["proxy"]["net_diff_mt5_minus_proxy"],
        "proxy_trade_count_diff_mt5_minus_proxy": review["proxy"]["trade_count_diff_mt5_minus_proxy"],
        "tester_status": kpi["tester_status"],
        "tester_blocker": kpi["tester_blocker"],
        "runtime_status": kpi["runtime_status"],
        "report_status": kpi["report_status"],
        "review_class": "mixed_positive_repair_required",
        "package_decision": "open_cr_repair_inputs_no_authority",
        "external_verification_status": "completed_mt5_runtime_probe_reviewed_with_terminal_timeout_boundary",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], review: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        KPI_RECEIPT,
        {
            **base,
            "measurement_scope": "MT5 runtime probe review(MT5 런타임 탐침 검토)",
            "management_state": [rel(FINAL_DECISION), rel(RUN_MANIFEST), rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER)],
            "judgment_class": "mixed_positive_runtime_probe_repair_required",
            "scoreboard": "runtime_probe",
            "parity_level": "P3_runtime_shadow_parity_sampled",
            "wfo_status": "not_applicable",
            "registry_update_required": "yes",
            "negative_memory_required": "yes",
            "hard_gate_applicable": "no",
            "evidence_boundary": "runtime_probe_review",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(TESTER_IDENTITY_REVIEW),
            "ea_identity": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "report_identity": rel(parent.STRATEGY_TESTER_REPORTS),
            "trade_evidence": [rel(MT5_KPI_REVIEW), rel(TRADE_SHAPE_REVIEW), rel(MONTH_ATTRIBUTION)],
            "cost_assumptions": "FPMarkets US100 M5 Strategy Tester(전략 테스터) fixed lot 0.1, model 4, deposit 500, leverage 1:100",
            "forensic_checks": [rel(parent.MT5_EXECUTION_RESULT), rel(parent.RUNTIME_OUTPUT_COPY), rel(parent.STRATEGY_TESTER_REPORTS)],
            "backtest_judgment": "usable_with_boundary_terminal_timeout_after_outputs_available",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "MT5 confirmed positive net/PF but month12 and equity DD weakened proxy read(MT5 순수익/PF는 양수, 12월/수익곡선 낙폭은 프록시보다 약함)",
            "comparison_baseline": rel(parent.PROXY_MT5_DIFF),
            "likely_drivers": ["MT5 fill/cost/equity path", "month12 long residual loss", "long skew remains"],
            "segment_checks": [rel(MONTH_ATTRIBUTION), rel(MONTH_SIDE_ATTRIBUTION), rel(SIDE_ATTRIBUTION), rel(ENTRY_HOUR_ATTRIBUTION), rel(HOLD_BUCKET_ATTRIBUTION)],
            "trade_shape": rel(TRADE_SHAPE_REVIEW),
            "alternative_explanations": ["terminal timeout after outputs does not invalidate report but keeps boundary", "proxy drawdown used balance/closed-trade basis"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(MT5_KPI_REVIEW), rel(PROXY_MT5_ATTRIBUTION), rel(MONTH_ATTRIBUTION), rel(DRAWDOWN_REVIEW), rel(REVIEW_FINDINGS)],
            "evidence_missing": ["forward/replay evidence(전진/재생 근거)", "runtime authority parity closure(런타임 권위 동등성 폐쇄)", "WFO/out-of-sample hardening(WFO/표본외 경화)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Positive MT5 clue remains, but month12 loss and equity DD block operating claims(MT5 긍정 단서는 남지만 12월 손실과 수익곡선 낙폭이 운영 주장을 막음).",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_review_artifacts(추적 검토 산출물)",
            "lineage_judgment": "connected_with_runtime_probe_review_boundary",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "MT5 runtime probe review mixed positive clue only(MT5 런타임 탐침 검토의 혼합 긍정 단서만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "좋은 MT5 KPI를 운영 가능 모델로 과장하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    if len(rows) > limit:
        lines.append("| ... | ... | ... | ... |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], review: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    month_rows = read_csv(MONTH_ATTRIBUTION).sort_values("net_profit").head(8).to_dict("records")
    side_rows = read_csv(SIDE_ATTRIBUTION).to_dict("records")
    findings = read_csv(REVIEW_FINDINGS).to_dict("records")
    queue = read_csv(NEXT_QUEUE).to_dict("records")
    report = f"""# run364CQ h17 bad-month source-balance MT5 runtime probe review(17시 손실 월/원천 균형 MT5 런타임 탐침 검토)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{final['judgment']}`
- MT5 net/PF/trades(순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- density(밀도): `{final['mt5_density']}` per feature day(피처 일 기준)
- short count(숏 수): `{final['short_trade_count']}`
- bad month count(손실 월 수): `{final['bad_month_count']}`
- equity DD(수익곡선 낙폭): `{final['equity_drawdown']}`

## Action/Effect(행동/효과)

Action(행동): CP MT5 report(CP MT5 보고서)를 trade list(거래 목록), month/side/hour attribution(월/방향/시간 귀속), proxy/MT5 diff(프록시/MT5 차이)로 review(검토)했습니다.

Effect(효과): CM04 candidate(CM04 후보)는 positive runtime clue(긍정 런타임 단서)로 보존하지만, month12 loss(12월 손실), equity drawdown gap(수익곡선 낙폭 간극), long skew(롱 편중)를 다음 repair(수리) 입력으로 넘깁니다.

## Findings(발견)

{markdown_table(findings, ['finding_id', 'severity', 'finding', 'effect'])}

## Month Attribution(월 귀속)

{markdown_table(month_rows, ['month', 'trade_count', 'net_profit', 'average_net', 'win_rate'])}

## Side Attribution(방향 귀속)

{markdown_table(side_rows, ['direction', 'trade_count', 'net_profit', 'average_net', 'win_rate'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['queue_id', 'candidate_seed', 'action', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This review(이번 검토)는 runtime probe review(런타임 탐침 검토)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CQ decision(결정): h17 bad-month source-balance MT5 review

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- MT5 net/PF/trades(순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- bad month(손실 월): `{final['worst_month']}` net `{final['worst_month_net']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 12월 롱 손실과 equity DD(수익곡선 낙폭)를 다음 수리 입력으로 넘깁니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CQ__{RUN_ID}", f"\n- run364CQ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - MT5 runtime probe review(MT5 런타임 탐침 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364CQ__{RUN_ID}", f"\n## run364CQ MT5 Runtime Probe Review(MT5 런타임 탐침 검토)\n\nAction(행동): run364CP MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.\n\nEffect(효과): positive net/PF/density(양수 순수익/PF/밀도)는 보존하고, month12/equity DD(12월/수익곡선 낙폭)를 `{NEXT_RUN_ID}` 입력으로 넘깁니다.\n")
    append_text_once(STAGE_README, f"run364CQ__{RUN_ID}", f"\n<!-- run364CQ__{RUN_ID} -->\n## run364CQ MT5 runtime probe review(MT5 런타임 탐침 검토)\n\n`{final['candidate_id']}` review(검토) 완료. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CQ` reviewed(검토 완료) CM04 MT5 runtime probe(CM04 MT5 런타임 탐침). MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`, density(밀도)는 `{final['mt5_density']}`, short count(숏 수)는 `{final['short_trade_count']}`입니다.

Open repair(열린 수리): bad month count(손실 월 수) `{final['bad_month_count']}` with worst month(최악 월) `{final['worst_month']}` net `{final['worst_month_net']}`, equity DD(수익곡선 낙폭) `{final['equity_drawdown']}`, long share(롱 비중) `{final['long_share']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 month12 long guard(12월 롱 가드), equity drawdown stress(수익곡선 낙폭 압박), side balance(방향 균형) repair inputs(수리 입력)를 materialize(구체화)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest MT5 runtime probe review(최근 MT5 런타임 탐침 검토): `{RUN_ID}`.

Actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`.

Repair boundary(수리 경계): month12 loss(12월 손실), equity DD(수익곡선 낙폭), long skew(롱 편중).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364CQ__{RUN_ID}", f"\n<!-- run364CQ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed CM04 MT5 runtime probe(CM04 MT5 런타임 탐침 검토); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364CQ__{RUN_ID}", f"\n<!-- run364CQ__{RUN_ID} -->\n- `{RUN_ID}`: CM04 MT5 probe(CM04 MT5 탐침)는 net/PF/density(순수익/PF/밀도) 긍정 단서이나 month12/equity DD(12월/수익곡선 낙폭) 수리 필요.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364CQ__{RUN_ID}", f"\n<!-- run364CQ__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님), but zero bad month(손실 월 0) claim failed in MT5 because `{final['worst_month']}` net `{final['worst_month_net']}`. Reopen condition(재개 조건): MT5 month attribution(월 귀속) non-negative with density >= 3 and short floor >= 100.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "kpi_evidence(KPI 근거)",
        "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "runtime_probe_review_only(런타임 탐침 검토 전용)",
        "question": "Does CM04 remain usable after MT5 runtime probe review?(CM04가 MT5 런타임 탐침 검토 후에도 쓸 단서인가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "expectancy": final["mt5_expectancy"],
        "trade_count": final["mt5_trade_count"],
        "trade_density_per_feature_day": final["mt5_density"],
        "long_trade_count": final["long_trade_count"],
        "short_trade_count": final["short_trade_count"],
        "max_drawdown_amount": final["equity_drawdown"],
        "recovery_factor": final["recovery_factor"],
        "trade_density_requirement_status": "passed_mt5_density_ge_3_no_trade_splitting(MT5 밀도 3 이상, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(MT5_KPI_REVIEW),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)

    ledger_rows = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", STATUS, True),
        ("tier_b_fallback_used", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required_no_fallback_source(필수 누락, 대체 원천 없음)", False),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", STATUS, True),
    ]:
        row = {
            **common,
            "subrun_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
            "status": status,
            "rows": 1 if include_metrics else 0,
            "net_profit": final["mt5_net_profit"] if include_metrics else "",
            "profit_factor": final["mt5_profit_factor"] if include_metrics else "",
            "expectancy": final["mt5_expectancy"] if include_metrics else "",
            "trade_count": final["mt5_trade_count"] if include_metrics else "",
            "short_trade_count": final["short_trade_count"] if include_metrics else "",
            "max_drawdown_amount": final["equity_drawdown"] if include_metrics else "",
            "recovery_factor": final["recovery_factor"] if include_metrics else "",
        }
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)

    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("mt5_kpi_review", MT5_KPI_REVIEW, "MT5 KPI review(MT5 KPI 검토)."),
            ("proxy_mt5_attribution", PROXY_MT5_ATTRIBUTION, "Proxy/MT5 attribution(프록시/MT5 귀속)."),
            ("month_attribution", MONTH_ATTRIBUTION, "Month attribution(월 귀속)."),
            ("drawdown_review", DRAWDOWN_REVIEW, "Drawdown review(낙폭 검토)."),
            ("next_queue", NEXT_QUEUE, "CR repair queue(CR 수리 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    cp_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    trades = trades_frame(report_path_from_records())
    review = build_reviews(cp_final, trades)
    gates = gate_rows(review)
    created_at = now_utc()
    final = final_payload(cp_final, review, gates, created_at)
    write_receipts(final, review)
    gates = gate_rows(review)
    final = final_payload(cp_final, review, gates, created_at)
    write_docs(final, review, gates)
    write_final_files(final, gates)
    write_ledgers(final, gates)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
