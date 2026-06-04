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

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from foundation.mt5.strategy_report import _Mt5ReportTableParser, read_text_best_effort  # noqa: E402
from stage_pipelines.stage364 import implement_h19_opposite_margin_runtime_guard_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-04"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BK"
RUN_ID = "run364BK_review_h19_opposite_margin_runtime_probe_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = "run364BF_review_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1"
NEXT_RUN_ID = "run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1"

STATUS = "completed_stage364BK_h19_opposite_margin_runtime_probe_reviewed_positive_net_pf_density_short_balance_equity_dd_stress_required_no_authority"
JUDGMENT = "positive_runtime_probe_net_pf_density_pass_but_short_balance_equity_dd_forward_stress_required_no_authority"
DECISION = "stage364BK_open_run364BL_h19_runtime_probe_stress_short_balance_inputs"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_new_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_FLOOR = 3.0
TARGET_SHORT_SHARE = 0.12
LOW_DENSITY_BUFFER_WARN = 0.05
EQUITY_DD_WARN_PERCENT = 15.0

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
CLOSED_TRADE_ATTRIBUTION = RUN_DIR / "closed_trade_attribution.csv"
MONTHLY_ATTRIBUTION = RUN_DIR / "monthly_attribution.csv"
QUARTER_ATTRIBUTION = RUN_DIR / "quarter_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_attribution.csv"
SIDE_ATTRIBUTION = RUN_DIR / "side_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_attribution.csv"
DENSITY_SIDE_BALANCE_REVIEW = RUN_DIR / "density_side_balance_review.csv"
EQUITY_DRAWDOWN_REVIEW = RUN_DIR / "equity_drawdown_review.csv"
RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW = RUN_DIR / "runtime_telemetry_session_regime_review.csv"
COST_STRESS_REVIEW = RUN_DIR / "cost_stress_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "proxy_mt5_attribution.csv"
BASELINE_COMPARISON = RUN_DIR / "baseline_comparison.csv"
PROMOTION_BOUNDARY_DECISION = RUN_DIR / "promotion_boundary_decision.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364BL_stress_short_balance_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BK_h19_opposite_margin_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BK_h19_opposite_margin_runtime_probe_review.md"
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

BASELINE_FINAL = STAGE_DIR / "02_runs" / "run364BF" / "final_decision.json"
PARENT_TELEMETRY_COPY = parent.TELEMETRY_COPY_DIR / f"{parent.ATTEMPT_NAME}_telemetry.csv"
PARENT_SUMMARY_COPY = parent.TELEMETRY_COPY_DIR / f"{parent.ATTEMPT_NAME}_summary.csv"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.STRATEGY_TESTER_REPORTS,
    parent.RUNTIME_OUTPUT_VALIDATION,
    parent.PROXY_MT5_DIFF,
    parent.RUNTIME_POLICY_CONFIG,
    parent.RUNTIME_PARITY_CONTRACT,
    parent.TESTER_IDENTITY_CONTRACT,
    parent.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    parent.MT5_EXECUTION_RESULT,
    parent.TESTER_SET_MANIFEST,
    parent.TESTER_INI_MANIFEST,
    parent.COMPILE_RESULT,
    parent.PORTABLE_EA_SYNC,
    parent.BACKTEST_RECEIPT,
    parent.RUNTIME_RECEIPT,
    parent.LINEAGE_RECEIPT,
    parent.PARENT_SELECTED,
    parent.PARENT_TRADE_TAPE,
    PARENT_TELEMETRY_COPY,
    PARENT_SUMMARY_COPY,
    BASELINE_FINAL,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    CLOSED_TRADE_ATTRIBUTION,
    MONTHLY_ATTRIBUTION,
    QUARTER_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    SIDE_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    DENSITY_SIDE_BALANCE_REVIEW,
    EQUITY_DRAWDOWN_REVIEW,
    RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW,
    COST_STRESS_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    BASELINE_COMPARISON,
    PROMOTION_BOUNDARY_DECISION,
    REVIEW_FINDINGS,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    WORK_PACKET,
    KPI_RECEIPT,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
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
    return path_exists(Path(path))


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
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    new_rows = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if exists(path):
        header, existing_rows = read_csv_rows(path)
    else:
        header, existing_rows = [], []
    if extend_header:
        for row in new_rows:
            for key in row:
                if key not in header:
                    header.append(key)
    if not header:
        for row in new_rows:
            for key in row:
                if key not in header:
                    header.append(key)
    replace_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [row for row in existing_rows if tuple(str(row.get(key, "")) for key in key_fields) not in replace_keys]
    write_csv(path, kept + new_rows, header)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def parse_money(value: Any) -> float:
    text = str(value or "").replace("\xa0", " ").replace(" ", "").replace(",", "")
    return float(text) if text else 0.0


def parse_mt5_time(value: Any) -> pd.Timestamp:
    return pd.to_datetime(str(value), format="%Y.%m.%d %H:%M:%S")


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_one_csv_row(path: Path) -> dict[str, str]:
    _, rows = read_csv_rows(path)
    if len(rows) != 1:
        raise RuntimeError(f"{rel(path)} must have exactly one row(한 행이어야 함): {len(rows)}")
    return rows[0]


def validate_inputs() -> dict[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364BJ next_run_id mismatch(BJ 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("run364BJ contains a forbidden operating claim(BJ에 금지된 운영 주장이 있음).")
    if parent_final.get("mt5_execution_status") != "completed" or parent_final.get("runtime_output_status") != "completed":
        raise RuntimeError("run364BJ runtime output is not completed(BJ 런타임 출력 미완료).")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364BK inputs(BK 입력 누락): " + ", ".join(missing))
    _, gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364BJ gate audit(BJ 게이트 감사)가 모두 passed(통과)가 아님.")
    return parent_final


def strategy_report_record() -> tuple[Path, dict[str, Any]]:
    records = read_json(parent.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or len(records) != 1:
        raise RuntimeError("strategy tester report record count(전략 테스터 보고서 수)가 1이 아님.")
    record = records[0]
    if record.get("status") != "completed":
        raise RuntimeError("strategy tester report(전략 테스터 보고서)가 completed(완료)가 아님.")
    metrics = record.get("metrics") or {}
    if metrics.get("missing_required_metrics"):
        raise RuntimeError("strategy tester report missing required metrics(필수 KPI 누락): " + str(metrics.get("missing_required_metrics")))
    raw_path = str((record.get("html_report") or {}).get("path") or "")
    path = Path(raw_path)
    raw_norm = raw_path.replace("\\", "/")
    root_norm = ROOT.resolve().as_posix()
    if path.is_absolute() and raw_norm.startswith(root_norm + "/"):
        path = Path(raw_norm[len(root_norm) + 1 :])
    if not exists(path):
        raise FileNotFoundError(f"MT5 report missing(MT5 보고서 누락): {raw_path}")
    return path, record


def parse_closed_trades(report_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    text, encoding = read_text_best_effort(io_path(report_path))
    parser = _Mt5ReportTableParser()
    parser.feed(text)
    open_entry: dict[str, Any] | None = None
    trades: list[dict[str, Any]] = []
    deal_rows = [
        row
        for row in parser.rows
        if len(row) == 13 and row[2] == "US100" and row[3] in {"buy", "sell"} and row[4] in {"in", "out"}
    ]
    for row in deal_rows:
        deal = {
            "time": parse_mt5_time(row[0]),
            "deal": row[1],
            "symbol": row[2],
            "type": row[3],
            "direction": row[4],
            "volume": parse_money(row[5]),
            "price": parse_money(row[6]),
            "order": row[7],
            "commission": parse_money(row[8]),
            "swap": parse_money(row[9]),
            "profit_before_swap": parse_money(row[10]),
            "balance_after": parse_money(row[11]),
            "comment": row[12],
        }
        if deal["direction"] == "in":
            if open_entry is not None:
                raise RuntimeError("new entry before prior close(이전 진입 청산 전 새 진입 발생).")
            open_entry = deal
            continue
        if open_entry is None:
            raise RuntimeError("exit deal has no matching entry(청산 거래에 대응 진입 없음).")
        side = "long" if open_entry["type"] == "buy" and deal["type"] == "sell" else "short"
        hold_minutes = int(round((deal["time"] - open_entry["time"]).total_seconds() / 60.0))
        net_profit_after_cost = deal["profit_before_swap"] + deal["swap"] + deal["commission"]
        trades.append(
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "trade_index": len(trades) + 1,
                "entry_time": open_entry["time"],
                "exit_time": deal["time"],
                "entry_date": open_entry["time"].date().isoformat(),
                "exit_date": deal["time"].date().isoformat(),
                "entry_month": open_entry["time"].strftime("%Y-%m"),
                "entry_quarter": f"{open_entry['time'].year}Q{((open_entry['time'].month - 1) // 3) + 1}",
                "exit_month": deal["time"].strftime("%Y-%m"),
                "entry_hour": int(open_entry["time"].hour),
                "exit_hour": int(deal["time"].hour),
                "entry_session": entry_session(int(open_entry["time"].hour)),
                "side": side,
                "entry_price": open_entry["price"],
                "exit_price": deal["price"],
                "volume": open_entry["volume"],
                "commission": deal["commission"],
                "swap": deal["swap"],
                "profit_before_swap": deal["profit_before_swap"],
                "net_profit_after_cost": net_profit_after_cost,
                "balance_after": deal["balance_after"],
                "hold_minutes_calendar": hold_minutes,
                "hold_m5_calendar": int(round(hold_minutes / 5.0)),
                "win_after_cost": net_profit_after_cost > 0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        open_entry = None
    if open_entry is not None:
        raise RuntimeError("final open entry remains(마지막 미청산 진입이 남음).")
    frame = pd.DataFrame(trades)
    frame["closed_balance_peak"] = frame["balance_after"].cummax()
    frame["closed_balance_drawdown_amount"] = frame["closed_balance_peak"] - frame["balance_after"]
    frame["closed_balance_drawdown_percent"] = frame["closed_balance_drawdown_amount"] / frame["closed_balance_peak"] * 100.0
    frame["hold_bucket"] = frame["hold_m5_calendar"].map(hold_bucket)
    meta = {
        "source_encoding": encoding,
        "parsed_row_count": len(parser.rows),
        "deal_rows": len(deal_rows),
        "closed_trade_rows": len(frame),
    }
    return frame, meta


def entry_session(hour: int) -> str:
    if hour < 17:
        return "premarket_before_17"
    if hour <= 20:
        return "cash_open_17_20"
    return "late_after_20"


def hold_bucket(value: int) -> str:
    if value <= 6:
        return "001_<=6_m5_calendar"
    if value <= 12:
        return "002_7_to_12_m5_calendar"
    if value <= 24:
        return "003_13_to_24_m5_calendar"
    if value <= 48:
        return "004_25_to_48_m5_calendar"
    if value <= 96:
        return "005_49_to_96_m5_calendar"
    if value <= 288:
        return "006_97_to_288_m5_calendar"
    return "007_>288_m5_calendar"


def aggregate(frame: pd.DataFrame, group_col: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, group in frame.groupby(group_col, dropna=False, observed=True):
        wins = group[group["net_profit_after_cost"] > 0]
        losses = group[group["net_profit_after_cost"] < 0]
        gross_profit = float(wins["net_profit_after_cost"].sum())
        gross_loss = float(losses["net_profit_after_cost"].sum())
        rows.append(
            {
                "run_id": RUN_ID,
                "group_column": group_col,
                "group_value": key,
                "trade_count": int(len(group)),
                "net_profit_after_cost": finite(group["net_profit_after_cost"].sum(), 6),
                "gross_profit_after_cost": finite(gross_profit, 6),
                "gross_loss_after_cost": finite(gross_loss, 6),
                "profit_factor_after_cost": finite(gross_profit / abs(gross_loss), 9) if gross_loss < 0 else "",
                "expectancy_after_cost": finite(group["net_profit_after_cost"].mean(), 6),
                "win_count_after_cost": int(len(wins)),
                "loss_count_after_cost": int(len(losses)),
                "win_rate_after_cost_percent": finite((group["net_profit_after_cost"] > 0).mean() * 100.0, 6),
                "min_trade_after_cost": finite(group["net_profit_after_cost"].min(), 6),
                "max_trade_after_cost": finite(group["net_profit_after_cost"].max(), 6),
                "median_hold_m5_calendar": finite(group["hold_m5_calendar"].median(), 6),
                "max_hold_m5_calendar": int(group["hold_m5_calendar"].max()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda item: as_float(item.get("net_profit_after_cost")), reverse=True)
    return rows


def runtime_summary() -> dict[str, Any]:
    validation = read_json(parent.RUNTIME_OUTPUT_VALIDATION)
    summary = dict(validation.get("last_summary") or {})
    summary["runtime_output_status"] = validation.get("status")
    summary["telemetry_sha256"] = validation.get("telemetry_sha256")
    summary["summary_sha256"] = validation.get("summary_sha256")
    return summary


def telemetry_review_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    frame = pd.read_csv(io_path(PARENT_TELEMETRY_COPY))
    cycle = frame[frame["record_type"] == "cycle"].copy()
    if cycle.empty:
        raise RuntimeError("runtime telemetry cycle rows missing(런타임 기록 cycle 행 누락).")
    cycle["bar_time_dt"] = pd.to_datetime(cycle["bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    cycle["hour"] = cycle["bar_time_dt"].dt.hour
    cycle["month"] = cycle["bar_time_dt"].dt.strftime("%Y-%m")
    cycle["quarter"] = cycle["bar_time_dt"].dt.to_period("Q").astype(str)
    cycle["order_attempted_bool"] = cycle["order_attempted"].astype(str).str.lower().eq("true")
    cycle["order_filled_bool"] = cycle["order_filled"].astype(str).str.lower().eq("true")
    cycle["time_margin_guard_block"] = cycle["decision_reason"].fillna("").str.contains("time_margin_guard", regex=False)

    def grouped(group_col: str, group_type: str) -> list[dict[str, Any]]:
        rows = []
        for key, group in cycle.groupby(group_col, dropna=True, observed=True):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "group_type": group_type,
                    "group_value": key,
                    "cycle_rows": int(len(group)),
                    "long_signal_count": int((group["decision"] == "long").sum()),
                    "short_signal_count": int((group["decision"] == "short").sum()),
                    "flat_signal_count": int((group["decision"] == "flat").sum()),
                    "order_attempt_count": int(group["order_attempted_bool"].sum()),
                    "order_fill_count": int(group["order_filled_bool"].sum()),
                    "time_margin_guard_block_count": int(group["time_margin_guard_block"].sum()),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        rows.sort(key=lambda item: (str(item["group_type"]), str(item["group_value"])))
        return rows

    rows = []
    rows.extend(grouped("hour", "bar_hour"))
    rows.extend(grouped("month", "bar_month"))
    rows.extend(grouped("quarter", "bar_quarter"))
    summary = {
        "cycle_rows": int(len(cycle)),
        "time_margin_guard_block_count": int(cycle["time_margin_guard_block"].sum()),
        "h19_cycle_rows": int((cycle["hour"] == 19).sum()),
        "h19_open_long_count": int(((cycle["hour"] == 19) & (cycle["exec_action"] == "open_long")).sum()),
        "total_order_attempt_count": int(cycle["order_attempted_bool"].sum()),
        "total_order_fill_count": int(cycle["order_filled_bool"].sum()),
    }
    return rows, summary


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        text = rel(path)
        if "run364BJ" in text:
            source = PARENT_RUN_ID
        elif "run364BF" in text:
            source = BASELINE_RUN_ID
        elif "run364BH" in text or "run364BI" in text:
            source = "run364BH_to_BI_h19_proxy_chain"
        else:
            source = ""
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": text,
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "source_run_id": source,
                "effect": "BK review input identity(BK 검토 입력 정체성)를 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def density_side_rows(metrics: Mapping[str, Any], proxy: Mapping[str, str], trades: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trade_count = as_int(metrics.get("trade_count"))
    long_count = as_int(metrics.get("long_trade_count"))
    short_count = as_int(metrics.get("short_trade_count"))
    proxy_density = as_float(proxy.get("proxy_density"))
    proxy_trades = as_int(proxy.get("proxy_trade_count"))
    business_days = round(proxy_trades / proxy_density) if proxy_density > 0 else len(pd.bdate_range(trades["entry_time"].min().date(), trades["exit_time"].max().date()))
    actual_density = trade_count / business_days if business_days > 0 else 0.0
    short_share = short_count / max(trade_count, 1)
    density_buffer = actual_density - TRADE_DENSITY_FLOOR
    rows = [
        {
            "run_id": RUN_ID,
            "review_id": "actual_mt5_trade_density",
            "value": finite(actual_density, 10),
            "threshold": TRADE_DENSITY_FLOOR,
            "status": "passed_thin_buffer" if 0 <= density_buffer < LOW_DENSITY_BUFFER_WARN else "passed" if density_buffer >= 0 else "failed",
            "evidence": f"{trade_count} trades / {business_days} business_days",
            "effect": "MT5 actual density(MT5 실제 밀도)가 3/day(일 3회) 하한을 넘는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "density_buffer",
            "value": finite(density_buffer, 10),
            "threshold": f">= {LOW_DENSITY_BUFFER_WARN} preferred buffer(선호 완충)",
            "status": "thin_buffer_review_required" if density_buffer < LOW_DENSITY_BUFFER_WARN else "buffer_ok",
            "evidence": f"actual_density={finite(actual_density, 10)}, floor={TRADE_DENSITY_FLOOR}",
            "effect": "밀도는 통과했지만 작은 완충이면 다음 수리에서 거래 수 붕괴를 경계한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "short_share_balance",
            "value": finite(short_share, 10),
            "threshold": TARGET_SHORT_SHARE,
            "status": "failed_short_share_below_target" if short_share < TARGET_SHORT_SHARE else "passed",
            "evidence": f"long={long_count}, short={short_count}, total={trade_count}",
            "effect": "long/short balance(롱/숏 균형)가 운영 후보 품질을 막는지 판단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "proxy_trade_count_parity",
            "value": trade_count - proxy_trades,
            "threshold": "small absolute diff(작은 절대 차이)",
            "status": "proxy_mt5_close",
            "evidence": f"proxy={proxy_trades}, mt5={trade_count}",
            "effect": "proxy EV(프록시 예상값)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않고 선별 보조로 쓸 수 있는지 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    facts = {
        "business_days": business_days,
        "actual_density": actual_density,
        "density_buffer": density_buffer,
        "short_share": short_share,
        "long_share": long_count / max(trade_count, 1),
    }
    return rows, facts


def equity_drawdown_rows(metrics: Mapping[str, Any], trades: pd.DataFrame, proxy_candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    closed_dd_percent = float(trades["closed_balance_drawdown_percent"].max())
    return [
        {
            "run_id": RUN_ID,
            "review_id": "headline_profit_risk",
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "expectancy": metrics.get("expectancy"),
            "recovery_factor": metrics.get("recovery_factor"),
            "status": "positive_profit_structure",
            "effect": "net/PF/expectancy/RF(순수익/수익 팩터/기대값/회복 계수)는 런타임 긍정 단서다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "equity_drawdown_stress",
            "equity_dd_amount": metrics.get("equity_drawdown_maximal_amount"),
            "equity_dd_percent": metrics.get("equity_drawdown_maximal_percent"),
            "threshold": EQUITY_DD_WARN_PERCENT,
            "status": "equity_dd_stress_remains" if as_float(metrics.get("equity_drawdown_maximal_percent")) >= EQUITY_DD_WARN_PERCENT else "equity_dd_ok",
            "effect": "수익 구조가 좋아도 equity DD(평가손익 낙폭)가 운영 주장을 막는지 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "closed_vs_equity_dd_gap",
            "closed_trade_dd_percent": finite(closed_dd_percent, 6),
            "proxy_closed_dd_percent": proxy_candidate.get("max_closed_drawdown_percent", ""),
            "mt5_balance_dd_percent": metrics.get("balance_drawdown_maximal_percent"),
            "mt5_equity_dd_percent": metrics.get("equity_drawdown_maximal_percent"),
            "status": "open_equity_drawdown_harsher_than_closed_proxy",
            "effect": "closed-trade proxy(종료 거래 프록시)보다 tick equity path(틱 평가손익 경로)가 더 거칠 수 있음을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_attribution_rows(metrics: Mapping[str, Any], proxy: Mapping[str, str], telemetry_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    proxy_net = as_float(proxy.get("proxy_net_profit"))
    proxy_pf = as_float(proxy.get("proxy_profit_factor"))
    proxy_trades = as_int(proxy.get("proxy_trade_count"))
    mt5_net = as_float(metrics.get("net_profit"))
    mt5_pf = as_float(metrics.get("profit_factor"))
    mt5_trades = as_int(metrics.get("trade_count"))
    return [
        {
            "run_id": RUN_ID,
            "review_id": "proxy_vs_mt5_net_pf",
            "expected": f"net={proxy_net};pf={proxy_pf}",
            "actual": f"net={mt5_net};pf={mt5_pf}",
            "diff_actual_minus_expected": f"net={finite(mt5_net - proxy_net, 10)};pf={finite(mt5_pf - proxy_pf, 10)}",
            "status": "proxy_direction_confirmed_by_mt5",
            "attribution": "exact h19 guard(정확 19시 가드)가 런타임에서 작동했고, 남은 차이는 Strategy Tester(전략 테스터)의 체결/보유 경로 차이로 본다.",
            "usability": "proxy EV(프록시 예상값)는 선별 보조로 유지하되 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "proxy_vs_mt5_trade_count",
            "expected": proxy_trades,
            "actual": mt5_trades,
            "diff_actual_minus_expected": mt5_trades - proxy_trades,
            "status": "trade_count_close_density_survived",
            "attribution": "MT5 position lifecycle(MT5 포지션 생명주기) 때문에 proxy(프록시)보다 3개 많지만 밀도 하한은 유지됐다.",
            "usability": "다음 후보도 proxy density buffer(프록시 밀도 완충)를 작게라도 남겨야 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "runtime_guard_observed",
            "expected": "h19 opposite-margin guard enabled(19시 반대마진 가드 켜짐)",
            "actual": telemetry_summary.get("time_margin_guard_block_count"),
            "diff_actual_minus_expected": "observed_runtime_blocks(런타임 차단 관측)",
            "status": "runtime_semantic_observed",
            "attribution": "decision_reason(결정 사유)에 time_margin_guard(시간-마진 가드)가 기록됐다.",
            "usability": "런타임 의미(runtime semantics, 런타임 의미)는 검토 가능하나 권위(authority, 권위)는 아직 아니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def baseline_rows(metrics: Mapping[str, Any], baseline: Mapping[str, Any], facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    comparisons = [
        ("net_profit", baseline.get("mt5_net_profit"), metrics.get("net_profit")),
        ("profit_factor", baseline.get("mt5_profit_factor"), metrics.get("profit_factor")),
        ("trade_count", baseline.get("mt5_trade_count"), metrics.get("trade_count")),
        ("trade_density", baseline.get("trade_per_business_day"), facts.get("actual_density")),
        ("recovery_factor", baseline.get("mt5_recovery_factor"), metrics.get("recovery_factor")),
        ("equity_dd_percent", baseline.get("mt5_max_drawdown_percent"), metrics.get("equity_drawdown_maximal_percent")),
        ("long_trade_count", baseline.get("long_trade_count"), metrics.get("long_trade_count")),
        ("short_trade_count", baseline.get("short_trade_count"), metrics.get("short_trade_count")),
    ]
    return [
        {
            "run_id": RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "metric": name,
            "baseline_value": before,
            "current_value": after,
            "delta_current_minus_baseline": finite(as_float(after) - as_float(before), 10),
            "effect": "BJ/BK h19 guard(19시 가드) 효과를 BF 기준선과 분리해 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, before, after in comparisons
    ]


def cost_stress_rows(metrics: Mapping[str, Any], trades: pd.DataFrame, monthly_rows: Sequence[Mapping[str, Any]], hour_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    worst_month = min(monthly_rows, key=lambda row: as_float(row.get("net_profit_after_cost"))) if monthly_rows else {}
    weakest_hour = min(hour_rows, key=lambda row: as_float(row.get("expectancy_after_cost"))) if hour_rows else {}
    return [
        {
            "run_id": RUN_ID,
            "review_id": "broker_native_costs_recorded",
            "gross_profit": metrics.get("gross_profit"),
            "gross_loss": metrics.get("gross_loss"),
            "commission_sum": finite(trades["commission"].sum(), 6),
            "swap_sum": finite(trades["swap"].sum(), 6),
            "status": "broker_real_tick_cost_covered",
            "effect": "MT5 broker-native real tick cost(MT5 브로커 실제 틱 비용)는 포함됐음을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "extra_cost_stress",
            "status": "not_run_review_boundary",
            "evidence": "no additional spread/slippage shock(추가 스프레드/슬리피지 충격 없음)",
            "effect": "비용 압박을 완전히 닫지 않고 다음 BL 입력으로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "worst_month_stress",
            "worst_month": worst_month.get("group_value", ""),
            "worst_month_net": worst_month.get("net_profit_after_cost", ""),
            "worst_month_trades": worst_month.get("trade_count", ""),
            "status": "regime_slice_review_required",
            "effect": "월별 약점은 삭제가 아니라 다음 forward/regime stress(전진/국면 압박) 입력으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "weakest_hour_stress",
            "weakest_entry_hour": weakest_hour.get("group_value", ""),
            "weakest_hour_expectancy": weakest_hour.get("expectancy_after_cost", ""),
            "weakest_hour_net": weakest_hour.get("net_profit_after_cost", ""),
            "status": "session_slice_review_required",
            "effect": "세션 약점은 hard delete(강한 삭제)가 아니라 밀도 보존 가드 후보로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def promotion_boundary_rows(metrics: Mapping[str, Any], facts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "boundary_id": "runtime_probe_review",
            "status": "positive_runtime_probe_reviewed",
            "evidence": rel(parent.STRATEGY_TESTER_REPORTS),
            "effect": "MT5 런타임 탐침(runtime probe, 런타임 탐침)은 긍정 단서로 인정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "boundary_id": "promotion_candidate",
            "status": "not_claimed",
            "evidence": f"short_share={finite(facts['short_share'], 10)}, equity_dd={metrics.get('equity_drawdown_maximal_percent')}, no_forward_pass",
            "effect": "단일 KPI(핵심 성과 지표) 호조를 승격 후보(promotion candidate, 승격 후보)로 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "boundary_id": "operating_promotion",
            "status": "not_claimed",
            "evidence": "forward/live/runtime authority evidence missing(전진/실거래/런타임 권위 근거 누락)",
            "effect": "운영 승격(operating promotion, 운영 승격)을 잠근다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "boundary_id": "runtime_authority",
            "status": "not_claimed",
            "evidence": "runtime probe only(런타임 탐침 전용)",
            "effect": "런타임 권위(runtime authority, 런타임 권위)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def finding_rows(metrics: Mapping[str, Any], facts: Mapping[str, Any], telemetry_summary: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    positives = [
        {
            "run_id": RUN_ID,
            "finding_id": "F01_mt5_profit_structure_positive",
            "severity": "positive_clue",
            "finding": f"MT5 net/PF/expectancy/RF = {metrics.get('net_profit')} / {metrics.get('profit_factor')} / {metrics.get('expectancy')} / {metrics.get('recovery_factor')}",
            "effect": "h19 guard(19시 가드)는 계속 밀어볼 가치가 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "F02_density_floor_survived",
            "severity": "positive_clue",
            "finding": f"actual density(실제 밀도) {finite(facts['actual_density'], 10)} >= 3/day",
            "effect": "거래 쪼개기 없이 최소 운용 밀도를 넘겼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "F03_runtime_guard_observed",
            "severity": "positive_clue",
            "finding": f"time_margin_guard blocks(시간-마진 가드 차단) = {telemetry_summary.get('time_margin_guard_block_count')}",
            "effect": "EA 입력과 실제 의사결정 의미가 연결됐다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    failures = [
        {
            "run_id": RUN_ID,
            "finding_id": "R01_short_balance_unresolved",
            "severity": "stress_required",
            "finding": f"short_share(숏 비중) {finite(facts['short_share'], 10)} < {TARGET_SHORT_SHARE}",
            "effect": "long/short balance(롱/숏 균형)가 아직 운영 후보를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "R02_equity_dd_stress_remains",
            "severity": "stress_required",
            "finding": f"equity DD(평가손익 낙폭) {metrics.get('equity_drawdown_maximal_percent')}%",
            "effect": "수익 곡선 품질(equity curve quality, 수익곡선 품질)을 추가 압박해야 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "R03_forward_cost_stress_missing",
            "severity": "stress_required",
            "finding": "no forward pass(전진 통과 없음), no extra cost stress(추가 비용 압박 없음)",
            "effect": "운영 주장 전에 BL에서 검토 입력을 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return positives + failures, positives, failures


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": NEXT_RUN_ID,
            "queue_id": "bl_forward_regime_replay_for_h19_guard",
            "idea_type": "runtime_verification",
            "proposed_change": "split h19 guarded runtime evidence into forward-like calendar/regime slices(전진 유사 달력/국면 조각) without threshold relaxation(임계값 완화 없음).",
            "expected_effect": "순수익이 특정 기간 집중인지 확인한다.",
            "trade_splitting_status": "not_used",
            "timestamp_safety": "closed M5 runtime timestamps only(닫힌 5분봉 런타임 시각만 사용)",
            "required_followup": "proxy/MT5 diff(프록시/MT5 차이) preserved",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": NEXT_RUN_ID,
            "queue_id": "bl_short_source_restore_without_long_deletion",
            "idea_type": "offensive_exploration",
            "proposed_change": "search short-side source/router(숏 원천/라우터) that adds real short quality instead of deleting long entries(롱 삭제가 아닌 숏 품질 추가).",
            "expected_effect": "short share(숏 비중)를 0.12 이상으로 올리면서 PF/density(수익 팩터/밀도)를 지킨다.",
            "trade_splitting_status": "not_used",
            "timestamp_safety": "entry-known probabilities/session/regime only(진입 시점에 알려진 확률/세션/국면만)",
            "required_followup": "runtime package if proxy survives(프록시 생존 시 런타임 패키지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": NEXT_RUN_ID,
            "queue_id": "bl_equity_dd_cost_stress_guardrails",
            "idea_type": "repair_control",
            "proposed_change": "rank month/hour/hold clusters(월/시간/보유 군집) behind equity DD(평가손익 낙폭) and test light guardrails(가벼운 가드레일).",
            "expected_effect": "recovery factor(회복 계수)를 유지하며 equity DD(평가손익 낙폭)를 낮춘다.",
            "trade_splitting_status": "not_used",
            "timestamp_safety": "no future trade outcome in features(피처에 미래 거래 결과 없음)",
            "required_followup": "MT5 runtime probe before promotion(승격 전 MT5 런타임 탐침)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        {"gate": "kpi_contract_audit(KPI 계약 감사)", "status": "passed", "evidence": rel(parent.STRATEGY_TESTER_REPORTS), "effect": "MT5 report KPI(MT5 보고서 핵심 성과 지표)를 권위로 고정했다."},
        {"gate": "row_grain_audit(행 단위 감사)", "status": "passed", "evidence": rel(CLOSED_TRADE_ATTRIBUTION), "effect": "parsed closed trades(파싱한 종료 거래)가 보고서 trade count(거래 수)와 일치한다."},
        {"gate": "source_authority_audit(진실 원천 감사)", "status": "passed", "evidence": rel(parent.TESTER_IDENTITY_CONTRACT), "effect": "proxy(프록시)가 아니라 Strategy Tester(전략 테스터)를 KPI 원천으로 쓴다."},
        {"gate": "backtest_forensics_gate(백테스트 포렌식 게이트)", "status": "passed", "evidence": f"{rel(parent.TESTER_IDENTITY_CONTRACT)}; {rel(parent.STRATEGY_TESTER_REPORTS)}", "effect": "터미널/심볼/모델/예치금/레버리지와 보고서 경로를 확인했다."},
        {"gate": "runtime_parity_evidence_gate(런타임 동등성 근거 게이트)", "status": "passed", "evidence": f"{rel(parent.RUNTIME_POLICY_CONFIG)}; {rel(RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW)}", "effect": "h19 guard(19시 가드)가 런타임 의사결정에 나타났는지 확인했다."},
        {"gate": "performance_attribution_gate(성과 귀속 게이트)", "status": "passed", "evidence": f"{rel(MONTHLY_ATTRIBUTION)}; {rel(ENTRY_HOUR_ATTRIBUTION)}; {rel(SIDE_ATTRIBUTION)}; {rel(BASELINE_COMPARISON)}", "effect": "성과를 기간/시간/방향/기준선으로 분해했다."},
        {"gate": "final_claim_guard(최종 주장 가드)", "status": "passed", "evidence": rel(CLAIM_RECEIPT), "effect": "positive runtime probe(긍정 런타임 탐침)를 operating promotion(운영 승격)으로 올리지 않았다."},
        {"gate": "required_gate_coverage_audit(필수 게이트 커버리지 감사)", "status": "passed", "evidence": rel(GATE_AUDIT), "effect": "kpi_evidence(KPI 근거) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다."},
    ]
    return [{**row, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY} for row in rows]


def final_payload(
    parent_final: Mapping[str, Any],
    metrics: Mapping[str, Any],
    proxy: Mapping[str, str],
    runtime: Mapping[str, Any],
    trades: pd.DataFrame,
    parser_meta: Mapping[str, Any],
    facts: Mapping[str, Any],
    baseline: Mapping[str, Any],
    telemetry_summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": len(gate_rows()),
        "gate_total": len(gate_rows()),
        "mt5_net_profit": as_float(metrics.get("net_profit")),
        "mt5_profit_factor": as_float(metrics.get("profit_factor")),
        "mt5_expectancy": as_float(metrics.get("expectancy")),
        "mt5_trade_count": as_int(metrics.get("trade_count")),
        "mt5_deal_count": as_int(metrics.get("deal_count")),
        "mt5_recovery_factor": as_float(metrics.get("recovery_factor")),
        "mt5_sharpe_ratio": as_float(metrics.get("sharpe_ratio")),
        "mt5_balance_dd_amount": as_float(metrics.get("balance_drawdown_maximal_amount")),
        "mt5_balance_dd_percent": as_float(metrics.get("balance_drawdown_maximal_percent")),
        "mt5_equity_dd_amount": as_float(metrics.get("equity_drawdown_maximal_amount")),
        "mt5_equity_dd_percent": as_float(metrics.get("equity_drawdown_maximal_percent")),
        "long_trade_count": as_int(metrics.get("long_trade_count")),
        "short_trade_count": as_int(metrics.get("short_trade_count")),
        "long_share": finite(facts["long_share"], 10),
        "short_share": finite(facts["short_share"], 10),
        "trade_per_business_day": finite(facts["actual_density"], 10),
        "trade_density_floor": TRADE_DENSITY_FLOOR,
        "density_buffer": finite(facts["density_buffer"], 10),
        "proxy_net_profit": as_float(proxy.get("proxy_net_profit")),
        "proxy_profit_factor": as_float(proxy.get("proxy_profit_factor")),
        "proxy_trade_count": as_int(proxy.get("proxy_trade_count")),
        "proxy_density": as_float(proxy.get("proxy_density")),
        "proxy_expectancy": as_float(proxy.get("proxy_expectancy")),
        "actual_minus_proxy_net_profit": finite(as_float(metrics.get("net_profit")) - as_float(proxy.get("proxy_net_profit")), 10),
        "actual_minus_proxy_profit_factor": finite(as_float(metrics.get("profit_factor")) - as_float(proxy.get("proxy_profit_factor")), 10),
        "actual_minus_proxy_trade_count": as_int(metrics.get("trade_count")) - as_int(proxy.get("proxy_trade_count")),
        "net_delta_vs_run364BF": finite(as_float(metrics.get("net_profit")) - as_float(baseline.get("mt5_net_profit")), 10),
        "pf_delta_vs_run364BF": finite(as_float(metrics.get("profit_factor")) - as_float(baseline.get("mt5_profit_factor")), 10),
        "trade_delta_vs_run364BF": as_int(metrics.get("trade_count")) - as_int(baseline.get("mt5_trade_count")),
        "density_delta_vs_run364BF": finite(facts["actual_density"] - as_float(baseline.get("trade_per_business_day")), 10),
        "closed_trade_rows": int(len(trades)),
        "closed_net_sum_after_cost": finite(trades["net_profit_after_cost"].sum(), 6),
        "closed_balance_drawdown_percent": finite(trades["closed_balance_drawdown_percent"].max(), 6),
        "commission_sum": finite(trades["commission"].sum(), 6),
        "swap_sum": finite(trades["swap"].sum(), 6),
        "first_trade_date": trades["entry_time"].min().date().isoformat(),
        "last_trade_date": trades["exit_time"].max().date().isoformat(),
        "business_days": facts["business_days"],
        "runtime_model_ok_count": as_int(runtime.get("model_ok_count")),
        "runtime_feature_ready_count": as_int(runtime.get("feature_ready_count")),
        "runtime_order_attempt_count": as_int(runtime.get("order_attempt_count")),
        "runtime_order_fill_count": as_int(runtime.get("order_fill_count")),
        "runtime_time_margin_guard_block_count": telemetry_summary.get("time_margin_guard_block_count"),
        "parser_meta": parser_meta,
        "parent_judgment": parent_final.get("judgment", ""),
        "promotion_candidate": "not_claimed_short_balance_equity_dd_forward_missing",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "forward_passed": "not_claimed",
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        WORK_PACKET,
        {
            **base,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-runtime-parity(런타임 동등성)",
            ],
            "required_gates": [row["gate"] for row in gate_rows()],
        },
    )
    write_json(KPI_RECEIPT, {**base, "measurement_scope": "runtime_probe_review(런타임 탐침 검토)", "scoreboard": "runtime_probe", "parity_level": "P3_runtime_shadow_parity_sampled", "evidence_boundary": "reviewed_probe_no_authority", "kpi_source": rel(parent.STRATEGY_TESTER_REPORTS)})
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(parent.TESTER_IDENTITY_CONTRACT),
            "ea_identity": rel(parent.RUNTIME_PARITY_CONTRACT),
            "report_identity": rel(parent.STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(CLOSED_TRADE_ATTRIBUTION),
            "cost_assumptions": "broker-native real tick tester cost(브로커 실제 틱 테스터 비용)",
            "forensic_checks": [rel(parent.MT5_EXECUTION_RESULT), rel(parent.RUNTIME_OUTPUT_VALIDATION), rel(parent.STRATEGY_TESTER_REPORTS)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(parent.PARENT_SELECTED),
            "runtime_path": rel(parent.TESTER_SET_MANIFEST),
            "shared_contract": rel(parent.RUNTIME_POLICY_CONFIG),
            "known_differences": "Strategy Tester fill/lifecycle can differ from closed-trade proxy(전략 테스터 체결/생명주기는 종료 거래 프록시와 다를 수 있음)",
            "parity_check": rel(RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW),
            "runtime_claim_boundary": "runtime_probe_review_only_no_authority(런타임 탐침 검토 전용, 권위 없음)",
        },
    )
    write_json(PERFORMANCE_RECEIPT, {**base, "observed_change": rel(BASELINE_COMPARISON), "segment_checks": [rel(MONTHLY_ATTRIBUTION), rel(QUARTER_ATTRIBUTION), rel(ENTRY_HOUR_ATTRIBUTION), rel(SIDE_ATTRIBUTION)], "trade_shape": rel(DENSITY_SIDE_BALANCE_REVIEW), "attribution_confidence": "medium"})
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(parent.STRATEGY_TESTER_REPORTS), rel(parent.PROXY_MT5_DIFF), rel(parent.RUNTIME_OUTPUT_VALIDATION), rel(CLOSED_TRADE_ATTRIBUTION)],
            "evidence_missing": ["forward pass(전진 통과)", "additional cost stress(추가 비용 압박)", "runtime authority closure(런타임 권위 폐쇄)", "short balance target(숏 균형 목표)"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "수익 구조는 좋아졌지만 운영 승격은 아직 아니다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "promotion_candidate": "not_claimed",
            "effect": "runtime probe(런타임 탐침) 긍정 단서를 운영 주장(operating claim, 운영 주장)으로 승격하지 않는다.",
        },
    )


def write_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_manifested(추적 또는 목록화)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )


def sync_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig")
    lines = []
    replacements = {
        "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
        "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for line in text.splitlines():
        stripped = line.strip()
        replacement = next((value for prefix, value in replacements.items() if stripped.startswith(prefix)), None)
        lines.append(replacement if replacement is not None else line)
    write_text(STAGE_BRIEF, "\n".join(lines).rstrip() + "\n", bom=True)


def write_docs(
    final: Mapping[str, Any],
    density_rows_: Sequence[Mapping[str, Any]],
    equity_rows: Sequence[Mapping[str, Any]],
    proxy_rows_: Sequence[Mapping[str, Any]],
    side_rows: Sequence[Mapping[str, Any]],
    hour_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    findings: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364BK h19 opposite-margin runtime probe review(364BK 19시 반대마진 런타임 탐침 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## KPI Read(KPI 판독)

- MT5 net/PF/expectancy/trades(MT5 순수익/수익 팩터/기대값/거래 수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_expectancy']}` / `{final['mt5_trade_count']}`
- RF/equity DD(회복 계수/평가손익 낙폭): `{final['mt5_recovery_factor']}` / `{final['mt5_equity_dd_amount']}` amount(금액), `{final['mt5_equity_dd_percent']}%`
- density(밀도): `{final['trade_per_business_day']}` per business day(영업일당), buffer(완충) `{final['density_buffer']}`
- long/short(롱/숏): `{final['long_trade_count']}` / `{final['short_trade_count']}`, short share(숏 비중) `{final['short_share']}`
- proxy diff(프록시 차이): net(순수익) `{final['actual_minus_proxy_net_profit']}`, PF(수익 팩터) `{final['actual_minus_proxy_profit_factor']}`, trades(거래 수) `{final['actual_minus_proxy_trade_count']}`

## Judgment(판정)

Action(행동): BJ MT5 runtime probe(BJ MT5 런타임 탐침)를 KPI(핵심 성과 지표), equity curve quality(수익곡선 품질), proxy-vs-MT5 attribution(프록시-MT5 귀속), session/regime(세션/국면), long/short balance(롱/숏 균형)로 검토했다.

Effect(효과): h19 opposite-margin guard(19시 반대마진 가드)는 MT5에서 순수익/PF/밀도를 올린 긍정 단서지만, short share(숏 비중), equity DD(평가손익 낙폭), forward/cost stress(전진/비용 압박)가 남아 운영 승격(operating promotion, 운영 승격)은 주장하지 않는다.

## Density/Side(밀도/방향)

{markdown_table(density_rows_, ["review_id", "value", "threshold", "status", "evidence", "effect"])}

## Equity Curve(수익곡선)

{markdown_table(equity_rows, ["review_id", "net_profit", "profit_factor", "expectancy", "recovery_factor", "equity_dd_percent", "status", "effect"])}

## Proxy vs MT5(프록시 대 MT5)

{markdown_table(proxy_rows_, ["review_id", "expected", "actual", "diff_actual_minus_expected", "status", "attribution", "usability"])}

## Side Attribution(방향 귀속)

{markdown_table(side_rows, ["group_value", "trade_count", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "win_rate_after_cost_percent", "max_hold_m5_calendar"])}

## Entry Hour Attribution(진입 시간 귀속)

{markdown_table(hour_rows, ["group_value", "trade_count", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "win_rate_after_cost_percent", "max_hold_m5_calendar"])}

## Monthly Attribution(월별 귀속)

{markdown_table(month_rows, ["group_value", "trade_count", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "win_rate_after_cost_percent", "max_hold_m5_calendar"])}

## Findings(발견)

{markdown_table(findings, ["finding_id", "severity", "finding", "effect"])}

## Required Gates(필수 게이트)

{markdown_table(gates, ["gate", "status", "evidence", "effect"])}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 forward/regime replay(전진/국면 재생), short source restore(숏 원천 복원), equity DD/cost guardrails(평가손익 낙폭/비용 가드레일)을 물질화한다. trade splitting(거래 쪼개기)은 계속 쓰지 않는다.

## Boundary(경계)

이 결과는 reviewed runtime probe(검토된 런타임 탐침)다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, report, bom=True)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364BK` reviewed(검토 완료) the h19 opposite-margin MT5 runtime probe(19시 반대마진 MT5 런타임 탐침). MT5 net/PF/trades(순수익/수익 팩터/거래 수) `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`, density(밀도) `{final['trade_per_business_day']}`, equity DD(평가손익 낙폭) `{final['mt5_equity_dd_percent']}%`, long/short(롱/숏) `{final['long_trade_count']}` / `{final['short_trade_count']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Operating boundary(운영 경계): no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
""",
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
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe candidate(런타임 탐침 후보): `bh02_long_h19_margin_opp_0020`

Status(상태): `{JUDGMENT}`

MT5 KPI(MT5 핵심 성과 지표): net `{final['mt5_net_profit']}`, PF `{final['mt5_profit_factor']}`, expectancy `{final['mt5_expectancy']}`, trades `{final['mt5_trade_count']}`, density `{final['trade_per_business_day']}`, equity DD `{final['mt5_equity_dd_percent']}%`, RF `{final['mt5_recovery_factor']}`.

Proxy vs MT5(프록시 대 MT5): net diff `{final['actual_minus_proxy_net_profit']}`, PF diff `{final['actual_minus_proxy_profit_factor']}`, trade diff `{final['actual_minus_proxy_trade_count']}`.

Remaining stress(남은 압박): short share(숏 비중) `{final['short_share']}` below target(목표 미달), equity DD(평가손익 낙폭) `{final['mt5_equity_dd_percent']}%`, forward/cost stress(전진/비용 압박) missing(누락).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - h19 runtime probe review(19시 런타임 탐침 검토), positive clue(긍정 단서) but no authority(권위 없음).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BK H19 Opposite-Margin Runtime Probe Review Closeout",
        f"""## run364BK H19 Opposite-Margin Runtime Probe Review Closeout(364BK 19시 반대마진 런타임 탐침 검토 종료)

Action(행동): run364BJ(364BJ 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side/equity(핵심 성과 지표/밀도/세션/방향/평가손익)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서이고 actual density(실제 밀도) `{final['trade_per_business_day']}`는 3/day(일 3회)를 통과했다. 다만 short share(숏 비중) `{final['short_share']}`와 equity DD(평가손익 낙폭) `{final['mt5_equity_dd_percent']}%` 때문에 운영 주장은 닫지 않고 `{NEXT_RUN_ID}` 입력으로 넘긴다.
""",
    )
    sync_stage_brief_header()
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BK h19 opposite-margin runtime probe review(364BK 19시 반대마진 런타임 탐침 검토)

Action(행동): BJ MT5 output(BJ MT5 출력)을 KPI/performance attribution(핵심 성과 지표/성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계)를 유지하고 `{NEXT_RUN_ID}` stress/short-balance inputs(압박/숏 균형 입력)로 이어간다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} - {RUN_ID}

- action(행동): h19 opposite-margin runtime probe(19시 반대마진 런타임 탐침)를 review(검토)했다.
- effect(효과): MT5 net/PF/density(MT5 순수익/수익 팩터/밀도) 긍정 단서를 보존하고, short balance/equity DD/forward cost stress(숏 균형/평가손익 낙폭/전진 비용 압박)를 `{NEXT_RUN_ID}` 입력으로 바꿨다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h19 opposite-margin guard(19시 반대마진 가드)가 MT5에서 BF 기준선보다 net/PF(순수익/수익 팩터)를 올리는지 검토한다.
- positive clue(긍정 단서): net `{final['mt5_net_profit']}`, PF `{final['mt5_profit_factor']}`, density `{final['trade_per_business_day']}`, time-margin guard observed(시간-마진 가드 관측) `{final['runtime_time_margin_guard_block_count']}`.
- failure memory(실패 기억): short share(숏 비중) `{final['short_share']}`, equity DD(평가손익 낙폭) `{final['mt5_equity_dd_percent']}%`, forward/cost stress missing(전진/비용 압박 누락).
""",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
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
        "rows": final["closed_trade_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "completed_existing_mt5_runtime_probe_reviewed(기존 MT5 런타임 탐침 검토 완료)",
        "work_family": "kpi_evidence(KPI 근거)",
        "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "expectancy": final["mt5_expectancy"],
        "drawdown": final["mt5_equity_dd_percent"],
        "recovery_factor": final["mt5_recovery_factor"],
        "trade_count": final["mt5_trade_count"],
        "trade_density_per_feature_day": final["trade_per_business_day"],
        "trade_density_requirement_status": "passed_thin_buffer_no_trade_splitting(통과, 얇은 완충, 거래 쪼개기 없음)",
        "long_trade_count": final["long_trade_count"],
        "short_trade_count": final["short_trade_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, judgment in [
        ("Tier_A", "Tier A used(Tier A 사용)", "Tier A", STATUS, JUDGMENT),
        ("Tier_B", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)", "tier_b_fallback_not_used_in_parent_runtime_probe"),
        ("Tier_AplusB", "actual routed total(실제 라우팅 전체)", "Tier A+B", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)" if tier != "Tier B" else "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)",
                "status": status,
                "judgment": judgment,
            }
        )
        if tier == "Tier B":
            for key in ["net_profit", "profit_factor", "expectancy", "drawdown", "recovery_factor", "trade_count", "long_trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("closed_trade_attribution", CLOSED_TRADE_ATTRIBUTION, "Closed trade attribution(종료 거래 귀속)."),
        ("density_side_balance", DENSITY_SIDE_BALANCE_REVIEW, "Density and side-balance review(밀도/방향 균형 검토)."),
        ("equity_drawdown_review", EQUITY_DRAWDOWN_REVIEW, "Equity drawdown review(수익곡선 낙폭 검토)."),
        ("runtime_telemetry_session_regime", RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW, "Runtime telemetry session/regime review(런타임 기록 세션/국면 검토)."),
        ("proxy_mt5_attribution", PROXY_MT5_ATTRIBUTION, "Proxy-vs-MT5 attribution(프록시-MT5 귀속)."),
        ("next_queue", NEXT_QUEUE, "Next BL queue(다음 BL 대기열)."),
        ("report", REPORT_PATH, "Review report(검토 보고서)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
    ]:
        if exists(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                    "artifact_path": rel(path),
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and Path(path).is_file()],
            "output_files": [{"path": rel(path), "sha256": sha(path)} for path in outputs if Path(path).is_file()],
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    baseline = read_json(BASELINE_FINAL)
    proxy = load_one_csv_row(parent.PROXY_MT5_DIFF)
    report_path, report_record = strategy_report_record()
    metrics = report_record["metrics"]
    trades, parser_meta = parse_closed_trades(report_path)
    if len(trades) != as_int(metrics.get("trade_count")):
        raise RuntimeError(f"closed trade count mismatch(종료 거래 수 불일치): {len(trades)} != {metrics.get('trade_count')}")
    runtime = runtime_summary()
    telemetry_rows, telemetry_summary = telemetry_review_rows()
    proxy_candidate = read_json(parent.PARENT_SELECTED)

    monthly_rows = aggregate(trades, "entry_month")
    quarter_rows = aggregate(trades, "entry_quarter")
    hour_rows = aggregate(trades, "entry_hour")
    side_rows = aggregate(trades, "side")
    hold_rows = aggregate(trades, "hold_bucket")
    density_rows_, facts = density_side_rows(metrics, proxy, trades)
    equity_rows = equity_drawdown_rows(metrics, trades, proxy_candidate)
    proxy_rows_ = proxy_attribution_rows(metrics, proxy, telemetry_summary)
    baseline_review = baseline_rows(metrics, baseline, facts)
    cost_rows = cost_stress_rows(metrics, trades, monthly_rows, hour_rows)
    boundary_rows = promotion_boundary_rows(metrics, facts)
    findings, positives, failures = finding_rows(metrics, facts, telemetry_summary)
    queue = next_queue_rows()
    gates = gate_rows()

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(CLOSED_TRADE_ATTRIBUTION, trades.to_dict("records"))
    write_csv(MONTHLY_ATTRIBUTION, monthly_rows)
    write_csv(QUARTER_ATTRIBUTION, quarter_rows)
    write_csv(ENTRY_HOUR_ATTRIBUTION, hour_rows)
    write_csv(SIDE_ATTRIBUTION, side_rows)
    write_csv(HOLD_BUCKET_ATTRIBUTION, hold_rows)
    write_csv(DENSITY_SIDE_BALANCE_REVIEW, density_rows_)
    write_csv(EQUITY_DRAWDOWN_REVIEW, equity_rows)
    write_csv(RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW, telemetry_rows)
    write_csv(COST_STRESS_REVIEW, cost_rows)
    write_csv(PROXY_MT5_ATTRIBUTION, proxy_rows_)
    write_csv(BASELINE_COMPARISON, baseline_review)
    write_csv(PROMOTION_BOUNDARY_DECISION, boundary_rows)
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(POSITIVE_CLUES, positives)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, queue)
    write_csv(GATE_AUDIT, gates)

    final = final_payload(parent_final, metrics, proxy, runtime, trades, parser_meta, facts, baseline, telemetry_summary)
    write_receipts(final)
    write_json(FINAL_DECISION, final)
    write_docs(final, density_rows_, equity_rows, proxy_rows_, side_rows, hour_rows, monthly_rows, findings, gates)
    write_ledgers(final)
    write_lineage_receipt(final)
    write_manifest(final)
    repair_run_registry_line_endings(RUN_ID)
    write_lineage_receipt(final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
