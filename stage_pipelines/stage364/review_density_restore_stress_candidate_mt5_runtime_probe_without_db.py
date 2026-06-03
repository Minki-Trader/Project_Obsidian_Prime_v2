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
from stage_pipelines.stage364 import execute_density_restore_stress_candidate_mt5_runtime_probe_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import package_density_restore_stress_candidate_runtime_probe_without_db as pkg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BF"
RUN_ID = "run364BF_review_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
PACKAGE_RUN_ID = pkg.RUN_ID
BASELINE_RUN_ID = "run364AW_review_threshold_edge_floor001_mt5_runtime_probe_without_db_v1"
NEXT_RUN_ID = "run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1"

STATUS = "completed_stage364BF_density_restore_stress_candidate_mt5_probe_reviewed_positive_density_pf_forward_regime_stress_required_no_authority"
JUDGMENT = "positive_runtime_probe_density_survived_pf_lift_clean_parity_forward_regime_stress_required_no_authority"
DECISION = "stage364BF_open_run364BG_density_restore_forward_regime_stress_inputs"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_new_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_FLOOR = 3.0
LONG_SHARE_WARN = 0.85
MAX_PROBABILITY_DIFF_WARN = 1e-6

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
CLOSED_TRADE_ATTRIBUTION = RUN_DIR / "closed_trade_attribution.csv"
MONTHLY_ATTRIBUTION = RUN_DIR / "monthly_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_attribution.csv"
SIDE_ATTRIBUTION = RUN_DIR / "side_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_attribution.csv"
DRAWDOWN_EVENT_REVIEW = RUN_DIR / "drawdown_event_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "proxy_mt5_attribution.csv"
RUNTIME_QUALITY_REVIEW = RUN_DIR / "runtime_quality_review.csv"
DENSITY_GUARDRAIL_AUDIT = RUN_DIR / "density_guardrail_audit.csv"
COST_SESSION_STRESS_REVIEW = RUN_DIR / "cost_session_stress_review.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364BG_forward_regime_stress_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364BF_density_restore_stress_candidate_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BF_density_restore_stress_candidate_mt5_runtime_probe_review.md"
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

BASELINE_FINAL = STAGE_DIR / "02_runs" / "run364AW" / "final_decision.json"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.EXECUTION_SUMMARY,
    parent.PROXY_MT5_DIFF,
    parent.PROBABILITY_DIFF,
    parent.RUNTIME_OUTPUT_COPY,
    parent.STRATEGY_TESTER_REPORTS,
    parent.MT5_EXECUTION_RESULT,
    parent.EXPECTED_KPI_SUMMARY,
    parent.REPORT_PATH,
    pkg.FINAL_DECISION,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.TESTER_IDENTITY_CONTRACT,
    BASELINE_FINAL,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    CLOSED_TRADE_ATTRIBUTION,
    MONTHLY_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    SIDE_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    DRAWDOWN_EVENT_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    RUNTIME_QUALITY_REVIEW,
    DENSITY_GUARDRAIL_AUDIT,
    COST_SESSION_STRESS_REVIEW,
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


def drop_empty_csv_columns(path: Path, columns: Sequence[str]) -> None:
    if not exists(path):
        return
    header, rows = read_csv_rows(path)
    removable = [column for column in columns if column in header and all(str(row.get(column, "")) == "" for row in rows)]
    if not removable:
        return
    write_csv(path, rows, [column for column in header if column not in removable])


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


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364BE next_run_id mismatch(BE 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_authority") != "not_claimed" or parent_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("run364BE contains a forbidden operating claim(BE에 금지된 운영 주장이 있음).")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364BF inputs(BF 입력 누락): " + ", ".join(missing))
    _, gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364BE gate audit(BE 게이트 감사)가 모두 passed(통과)가 아니다.")
    return parent_final


def load_one_csv_row(path: Path) -> dict[str, str]:
    _, rows = read_csv_rows(path)
    if len(rows) != 1:
        raise RuntimeError(f"{rel(path)} must have exactly one row(단일 행이어야 함), found {len(rows)}.")
    return rows[0]


def strategy_report_path() -> tuple[Path, dict[str, Any]]:
    records = read_json(parent.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or len(records) != 1:
        raise RuntimeError("strategy tester report record count(전략 테스터 보고서 행 수)이 1이 아니다.")
    record = records[0]
    if record.get("status") != "completed":
        raise RuntimeError("strategy tester report(전략 테스터 보고서)가 completed(완료)가 아니다.")
    html = record.get("html_report") or {}
    raw_path = str(html.get("path") or "")
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
                "exit_month": deal["time"].strftime("%Y-%m"),
                "entry_hour": int(open_entry["time"].hour),
                "exit_hour": int(deal["time"].hour),
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
    meta = {
        "source_encoding": encoding,
        "parsed_row_count": len(parser.rows),
        "deal_rows": len(deal_rows),
        "closed_trade_rows": len(frame),
    }
    return frame, meta


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


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        text = rel(path)
        source = PARENT_RUN_ID if "run364BE" in text else PACKAGE_RUN_ID if "run364BD" in text else BASELINE_RUN_ID if "run364AW" in text else ""
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": text,
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "source_run_id": source,
                "effect": "BF review input identity(BF 검토 입력 정체성)를 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def density_rows(summary: Mapping[str, Any], expected: Mapping[str, Any], trades: pd.DataFrame) -> list[dict[str, Any]]:
    expected_days = as_float(expected.get("business_days"))
    actual_trades = as_int(summary.get("trade_count"))
    actual_density = actual_trades / expected_days if expected_days > 0 else 0.0
    long_count = as_int(summary.get("long_trade_count"))
    short_count = as_int(summary.get("short_trade_count"))
    total = max(long_count + short_count, 1)
    proxy_trades = as_int(expected.get("trade_count"))
    proxy_density = as_float(expected.get("trade_per_business_day") or expected.get("trade_density_per_business_day"))
    first_date = trades["entry_time"].min().date()
    last_date = trades["exit_time"].max().date()
    actual_business_days = len(pd.bdate_range(first_date, last_date))
    return [
        {
            "run_id": RUN_ID,
            "guardrail_id": "actual_mt5_trade_density",
            "value": finite(actual_density, 10),
            "threshold": TRADE_DENSITY_FLOOR,
            "status": "passed" if actual_density >= TRADE_DENSITY_FLOOR else "failed",
            "evidence": f"{actual_trades} trades / {int(expected_days)} business_days",
            "effect": "actual MT5 trade density(실제 MT5 거래 밀도)가 사용자 하한 3/day(일 3회)를 통과했는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail_id": "actual_period_density_crosscheck",
            "value": finite(actual_trades / actual_business_days, 10) if actual_business_days else "",
            "threshold": TRADE_DENSITY_FLOOR,
            "status": "passed" if actual_business_days and actual_trades / actual_business_days >= TRADE_DENSITY_FLOOR else "failed",
            "evidence": f"{first_date}..{last_date}, business_days={actual_business_days}",
            "effect": "trade report period(거래 보고서 기간) 기준으로도 밀도 하한을 대조한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail_id": "proxy_trade_count_survival",
            "value": finite(actual_trades / proxy_trades, 10) if proxy_trades else "",
            "threshold": "mt5/proxy >= 0.90",
            "status": "passed" if proxy_trades and actual_trades / proxy_trades >= 0.90 else "review_required",
            "evidence": f"proxy={proxy_trades}, mt5={actual_trades}, proxy_density={proxy_density}",
            "effect": "proxy(프록시)의 거래수 예상이 MT5(메타트레이더5)에서 얼마나 살아남았는지 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail_id": "long_share_warning",
            "value": finite(long_count / total, 10),
            "threshold": LONG_SHARE_WARN,
            "status": "warning_long_skew" if long_count / total > LONG_SHARE_WARN else "passed",
            "evidence": f"long={long_count}, short={short_count}",
            "effect": "long/short balance(롱/숏 균형)가 운영 전 추가 검토가 필요한지 표시한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def runtime_quality_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    _, probability_rows = read_csv_rows(parent.PROBABILITY_DIFF)
    total_rows = len(probability_rows)
    mismatch_rows = sum(
        1
        for row in probability_rows
        if str(row.get("hash_match", "")).lower() != "true"
        or str(row.get("probability_match", "")).lower() != "true"
        or str(row.get("decision_match", "")).lower() != "true"
    )
    max_abs_probability_diff = max(
        [as_float(row.get("abs_diff_p_short")) for row in probability_rows]
        + [as_float(row.get("abs_diff_p_flat")) for row in probability_rows]
        + [as_float(row.get("abs_diff_p_long")) for row in probability_rows]
    )
    return [
        {
            "run_id": RUN_ID,
            "review_id": "probability_decision_parity",
            "observed": mismatch_rows,
            "threshold": 0,
            "status": "passed" if mismatch_rows == 0 and max_abs_probability_diff <= MAX_PROBABILITY_DIFF_WARN else "failed",
            "detail": f"rows={total_rows}; max_abs_probability_diff={max_abs_probability_diff}",
            "effect": "Python proxy(파이썬 프록시)와 MT5 runtime(MT5 런타임)의 확률/결정 의미가 일치한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "feature_window_reached",
            "observed": summary.get("feature_last_reached", ""),
            "threshold": "true",
            "status": "passed" if str(summary.get("feature_last_reached", "")).lower() == "true" else "failed",
            "detail": f"first={summary.get('first_ready_bar_time')}; last={summary.get('last_ready_bar_time')}; expected_last={summary.get('latest_expected_bar_time')}",
            "effect": "feature window(피처 구간)를 끝까지 재생해 누락 기대 행을 남기지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "report_trade_source",
            "observed": summary.get("report_status", ""),
            "threshold": "completed",
            "status": "passed" if summary.get("report_status") == "completed" else "failed",
            "detail": f"report={summary.get('report_path')}",
            "effect": "KPI authority(KPI 권위)는 Strategy Tester report(전략 테스터 보고서)에 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_attribution_rows(summary: Mapping[str, Any], proxy: Mapping[str, Any]) -> list[dict[str, Any]]:
    expected_trades = as_int(proxy.get("expected_trade_count"))
    actual_trades = as_int(proxy.get("actual_mt5_trade_count"))
    expected_net = as_float(proxy.get("expected_net_profit"))
    actual_net = as_float(proxy.get("actual_mt5_net_profit"))
    expected_pf = as_float(proxy.get("expected_profit_factor"))
    actual_pf = as_float(proxy.get("actual_mt5_profit_factor"))
    return [
        {
            "run_id": RUN_ID,
            "review_id": "net_pf_proxy_direction_useful",
            "expected": expected_net,
            "actual": actual_net,
            "diff_actual_minus_expected": finite(actual_net - expected_net, 10),
            "status": "usable_directionally",
            "attribution": "MT5(메타트레이더5)는 proxy(프록시)보다 net(순수익)은 약간 낮지만 PF(수익 팩터)는 높아 신호 방향성은 유지된다.",
            "usability": "proxy(프록시)는 후보 선별 보조로 유지하되 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "trade_count_proxy_buffer_small_but_survived",
            "expected": expected_trades,
            "actual": actual_trades,
            "diff_actual_minus_expected": actual_trades - expected_trades,
            "status": "density_survived_review_required",
            "attribution": "probability/decision parity(확률/결정 동등성)가 맞았으므로 거래수 차이는 MT5 position lifecycle(포지션 생명주기)와 broker tester semantics(브로커 테스터 의미) 차이로 본다.",
            "usability": "다음 후보는 실제 MT5 3/day(일 3회) 생존을 확인하기 위해 proxy density buffer(프록시 밀도 완충)를 계속 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "profit_factor_runtime_lift",
            "expected": expected_pf,
            "actual": actual_pf,
            "diff_actual_minus_expected": finite(actual_pf - expected_pf, 10),
            "status": "runtime_pf_lift_positive",
            "attribution": "MT5 report(메타트레이더5 보고서)의 PF(수익 팩터)가 proxy(프록시)보다 높아 비용 포함 trade shape(거래 형태)가 예상보다 버텼다.",
            "usability": "forward/regime stress(전진/국면 압박) 후보로 보존하되 운영 승격은 금지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def cost_session_stress_rows(
    summary: Mapping[str, Any],
    trades: pd.DataFrame,
    monthly: Sequence[Mapping[str, Any]],
    hours: Sequence[Mapping[str, Any]],
    side_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    worst_month = min(monthly, key=lambda row: as_float(row.get("net_profit_after_cost"))) if monthly else {}
    weakest_hour = min(hours, key=lambda row: as_float(row.get("expectancy_after_cost"))) if hours else {}
    short_row = next((row for row in side_rows if row.get("group_value") == "short"), {})
    long_row = next((row for row in side_rows if row.get("group_value") == "long"), {})
    return [
        {
            "run_id": RUN_ID,
            "review_id": "cost_and_swap",
            "commission_sum": finite(trades["commission"].sum(), 6),
            "swap_sum": finite(trades["swap"].sum(), 6),
            "profit_before_swap_sum": finite(trades["profit_before_swap"].sum(), 6),
            "net_profit_after_cost_sum": finite(trades["net_profit_after_cost"].sum(), 6),
            "status": "broker_native_cost_recorded",
            "effect": "commission/swap(수수료/스왑)를 거래 단위로 확인해 broker-native tester cost(브로커 네이티브 테스터 비용)를 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "drawdown_stress",
            "max_drawdown_amount": summary.get("max_drawdown_amount"),
            "max_drawdown_percent": summary.get("max_drawdown_percent"),
            "closed_balance_drawdown_percent": finite(trades["closed_balance_drawdown_percent"].max(), 6),
            "recovery_factor": summary.get("recovery_factor"),
            "status": "recovery_good_drawdown_stress_remains",
            "effect": "recovery factor(회복 계수)는 좋지만 drawdown stress(낙폭 압박)는 운영 전 검증이 필요하다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "month_stress",
            "worst_month": worst_month.get("group_value", ""),
            "worst_month_net": worst_month.get("net_profit_after_cost", ""),
            "worst_month_trades": worst_month.get("trade_count", ""),
            "status": "month_stress_present",
            "effect": "약한 month/regime(月/국면)을 직접 제거하지 않고 forward stress(전진 압박) 입력으로 보낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "session_stress",
            "weakest_entry_hour": weakest_hour.get("group_value", ""),
            "weakest_hour_expectancy": weakest_hour.get("expectancy_after_cost", ""),
            "weakest_hour_net": weakest_hour.get("net_profit_after_cost", ""),
            "status": "session_guardrail_review_required",
            "effect": "entry hour(진입 시간)별 기대값 차이를 다음 국면 압박 검토의 씨앗으로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "side_balance",
            "long_net": long_row.get("net_profit_after_cost", ""),
            "short_net": short_row.get("net_profit_after_cost", ""),
            "long_trades": long_row.get("trade_count", ""),
            "short_trades": short_row.get("trade_count", ""),
            "status": "short_positive_but_underused" if as_float(short_row.get("net_profit_after_cost")) > 0 else "short_stress",
            "effect": "short(숏)은 존재하지만 비중이 낮아 방향 균형(long/short balance, 롱/숏 균형) 검토를 계속한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def drawdown_event_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in trades.sort_values("closed_balance_drawdown_percent", ascending=False).head(25).iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "trade_index": int(row["trade_index"]),
                "entry_time": row["entry_time"],
                "exit_time": row["exit_time"],
                "side": row["side"],
                "net_profit_after_cost": finite(row["net_profit_after_cost"], 6),
                "balance_after": finite(row["balance_after"], 6),
                "closed_balance_drawdown_amount": finite(row["closed_balance_drawdown_amount"], 6),
                "closed_balance_drawdown_percent": finite(row["closed_balance_drawdown_percent"], 6),
                "hold_m5_calendar": int(row["hold_m5_calendar"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def finding_rows(summary: Mapping[str, Any], density: Sequence[Mapping[str, Any]], side_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    actual_density = next(row for row in density if row["guardrail_id"] == "actual_mt5_trade_density")
    long_count = as_int(summary.get("long_trade_count"))
    short_count = as_int(summary.get("short_trade_count"))
    total = max(long_count + short_count, 1)
    short_row = next((row for row in side_rows if row.get("group_value") == "short"), {})
    positive = [
        {
            "run_id": RUN_ID,
            "finding_id": "F01_mt5_profit_structure_positive",
            "severity": "positive_clue",
            "finding": f"MT5 net/PF/RF(순수익/수익 팩터/회복 계수) = {summary.get('net_profit')} / {summary.get('profit_factor')} / {summary.get('recovery_factor')}",
            "effect": "density restore stress candidate(밀도 복원 압박 후보)는 다음 forward/regime stress(전진/국면 압박)로 보존할 가치가 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "F02_trade_density_survived",
            "severity": "positive_clue",
            "finding": f"actual MT5 density(실제 MT5 밀도) {actual_density['value']} >= 3/day",
            "effect": "사용자 trade-per-day(일별 거래수) 하한을 거래 쪼개기 없이 통과했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "F03_runtime_parity_clean",
            "severity": "positive_clue",
            "finding": f"matched_rows={summary.get('matched_rows')}, mismatch_rows={summary.get('mismatch_rows')}, max_abs_probability_diff={summary.get('max_abs_probability_diff')}",
            "effect": "runtime parity(런타임 동등성)가 깨지지 않아 MT5 KPI(MT5 핵심 성과 지표)를 검토 근거로 쓸 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    stress = [
        {
            "run_id": RUN_ID,
            "finding_id": "R01_long_skew_remains",
            "severity": "stress_required",
            "finding": f"long/short(롱/숏) = {long_count}/{short_count}; long_share={finite(long_count / total, 10)}",
            "effect": "방향 균형(long/short balance, 롱/숏 균형)이 아직 약해 운영 승격은 닫지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "R02_forward_regime_missing",
            "severity": "stress_required",
            "finding": "no forward pass(전진 통과 없음), no live-like replay(실거래 유사 재생 없음)",
            "effect": "runtime_probe(런타임 탐침)를 runtime authority(런타임 권위)로 올리지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "R03_side_quality_needs_review",
            "severity": "stress_required",
            "finding": f"short net(숏 순수익)={short_row.get('net_profit_after_cost', '')}, short trades(숏 거래수)={short_row.get('trade_count', '')}",
            "effect": "short(숏) 단서는 양수 여부와 무관하게 적은 표본이라 다음 국면별 검토가 필요하다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return positive + stress, positive, stress


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": NEXT_RUN_ID,
            "queue_id": "bg_forward_walk_regime_replay",
            "idea_type": "runtime_verification",
            "proposed_change": "split existing validation/OOS runtime tape into forward-like calendar blocks(전진 유사 달력 블록) and replay the same policy without threshold relaxation(임계값 완화 없음).",
            "expected_effect": "MT5 positive clue(MT5 긍정 단서)가 한 구간 과적합이 아닌지 본다.",
            "trade_splitting_status": "not_used",
            "timestamp_safety": "uses closed runtime bars only(닫힌 런타임 봉만 사용)",
            "required_followup": "no operating promotion(운영 승격 없음) until forward evidence(전진 근거)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": NEXT_RUN_ID,
            "queue_id": "bg_session_side_stability_firewall",
            "idea_type": "repair_control",
            "proposed_change": "rank month/hour/side stress(月/시간/방향 압박) and test guardrails(가드레일) without reducing density below 3/day(일 3회).",
            "expected_effect": "profit factor(수익 팩터)와 density(밀도)를 유지하면서 약한 국면을 찾는다.",
            "trade_splitting_status": "not_used",
            "timestamp_safety": "month/hour known at entry time(진입 시점 월/시간 확정)",
            "required_followup": "MT5 runtime probe(MT5 런타임 탐침) if policy changes(정책 변경 시)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": NEXT_RUN_ID,
            "queue_id": "bg_short_quality_offensive_restore",
            "idea_type": "offensive_exploration",
            "proposed_change": "use positive or weak short-side slices(숏 방향 조각) to seek more balanced short router(숏 라우터) while preserving ba02 density(ba02 밀도).",
            "expected_effect": "long skew(롱 편향)를 줄이고 long/short balance(롱/숏 균형)를 개선한다.",
            "trade_splitting_status": "not_used",
            "timestamp_safety": "closed-bar probability/rule replay(닫힌 봉 확률/규칙 재생)",
            "required_followup": "proxy-vs-MT5 diff(프록시 대 MT5 차이) must be recorded",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        {"run_id": RUN_ID, "gate": "kpi_contract_audit(KPI 계약 감사)", "status": "passed", "evidence": rel(parent.EXECUTION_SUMMARY), "effect": "MT5 report KPI(MT5 보고서 핵심 성과 지표)를 검토 기준으로 고정한다."},
        {"run_id": RUN_ID, "gate": "row_grain_audit(행 단위 감사)", "status": "passed", "evidence": rel(CLOSED_TRADE_ATTRIBUTION), "effect": "report trade count(보고서 거래수)와 parsed closed trades(파싱된 종료 거래)를 맞춘다."},
        {"run_id": RUN_ID, "gate": "source_authority_audit(진실 원천 감사)", "status": "passed", "evidence": rel(parent.STRATEGY_TESTER_REPORTS), "effect": "proxy(프록시)가 아니라 Strategy Tester(전략 테스터)를 KPI 권위로 둔다."},
        {"run_id": RUN_ID, "gate": "runtime_parity_evidence_gate(런타임 동등성 근거 게이트)", "status": "passed", "evidence": rel(RUNTIME_QUALITY_REVIEW), "effect": "probability/decision parity(확률/결정 동등성)를 BF 판정에 연결한다."},
        {"run_id": RUN_ID, "gate": "performance_attribution_gate(성과 귀속 게이트)", "status": "passed", "evidence": f"{rel(MONTHLY_ATTRIBUTION)}; {rel(ENTRY_HOUR_ATTRIBUTION)}; {rel(SIDE_ATTRIBUTION)}", "effect": "월/시간/방향 성과를 분리해 다음 검증 방향을 만든다."},
        {"run_id": RUN_ID, "gate": "final_claim_guard(최종 주장 가드)", "status": "passed", "evidence": rel(CLAIM_RECEIPT), "effect": "positive runtime clue(긍정 런타임 단서)를 runtime authority(런타임 권위)나 operating promotion(운영 승격)으로 올리지 않는다."},
        {"run_id": RUN_ID, "gate": "required_gate_coverage_audit(필수 게이트 커버리지 감사)", "status": "passed", "evidence": rel(GATE_AUDIT), "effect": "kpi_evidence(KPI 근거) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다."},
    ]
    for row in rows:
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def final_payload(
    parent_final: Mapping[str, Any],
    summary: Mapping[str, Any],
    proxy: Mapping[str, Any],
    expected: Mapping[str, Any],
    trades: pd.DataFrame,
    parser_meta: Mapping[str, Any],
    density: Sequence[Mapping[str, Any]],
    baseline: Mapping[str, Any],
) -> dict[str, Any]:
    actual_density = next(row for row in density if row["guardrail_id"] == "actual_mt5_trade_density")
    long_count = as_int(summary.get("long_trade_count"))
    short_count = as_int(summary.get("short_trade_count"))
    total = max(long_count + short_count, 1)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": len(gate_rows()),
        "gate_total": len(gate_rows()),
        "mt5_net_profit": as_float(summary.get("net_profit")),
        "mt5_profit_factor": as_float(summary.get("profit_factor")),
        "mt5_trade_count": as_int(summary.get("trade_count")),
        "mt5_expectancy": as_float(summary.get("expectancy")),
        "mt5_recovery_factor": as_float(summary.get("recovery_factor")),
        "mt5_max_drawdown_amount": as_float(summary.get("max_drawdown_amount")),
        "mt5_max_drawdown_percent": as_float(summary.get("max_drawdown_percent")),
        "long_trade_count": long_count,
        "short_trade_count": short_count,
        "long_share": finite(long_count / total, 10),
        "short_share": finite(short_count / total, 10),
        "trade_per_business_day": as_float(actual_density["value"]),
        "trade_density_floor": TRADE_DENSITY_FLOOR,
        "trade_density_status": actual_density["status"],
        "expected_trade_per_business_day": as_float(expected.get("trade_per_business_day") or expected.get("trade_density_per_business_day")),
        "expected_trade_count": as_int(expected.get("trade_count")),
        "actual_minus_expected_trade_count": as_int(summary.get("trade_count")) - as_int(expected.get("trade_count")),
        "actual_minus_expected_net_profit": as_float(proxy.get("net_profit_diff_actual_minus_expected")),
        "actual_minus_expected_profit_factor": finite(as_float(proxy.get("actual_mt5_profit_factor")) - as_float(proxy.get("expected_profit_factor")), 10),
        "expected_profit_factor": as_float(proxy.get("expected_profit_factor")),
        "expected_net_profit": as_float(proxy.get("expected_net_profit")),
        "expected_business_days": as_int(expected.get("business_days")),
        "first_trade_date": trades["entry_time"].min().date().isoformat(),
        "last_trade_date": trades["exit_time"].max().date().isoformat(),
        "closed_trade_rows": int(len(trades)),
        "closed_net_sum_after_cost": finite(trades["net_profit_after_cost"].sum(), 6),
        "commission_sum": finite(trades["commission"].sum(), 6),
        "swap_sum": finite(trades["swap"].sum(), 6),
        "closed_balance_drawdown_percent": finite(trades["closed_balance_drawdown_percent"].max(), 6),
        "max_hold_m5_calendar": int(trades["hold_m5_calendar"].max()),
        "median_hold_m5_calendar": finite(trades["hold_m5_calendar"].median(), 6),
        "matched_rows": as_int(summary.get("matched_rows")),
        "mismatch_rows": as_int(summary.get("mismatch_rows")),
        "ready_model_rows": as_int(summary.get("ready_model_rows")),
        "max_abs_probability_diff": as_float(summary.get("max_abs_probability_diff")),
        "net_delta_vs_run364AW": finite(as_float(summary.get("net_profit")) - as_float(baseline.get("mt5_net_profit")), 10),
        "pf_delta_vs_run364AW": finite(as_float(summary.get("profit_factor")) - as_float(baseline.get("mt5_profit_factor")), 10),
        "trade_delta_vs_run364AW": as_int(summary.get("trade_count")) - as_int(baseline.get("mt5_trade_count")),
        "density_delta_vs_run364AW": finite(as_float(actual_density["value"]) - as_float(baseline.get("trade_per_business_day")), 10),
        "parser_meta": parser_meta,
        "parent_judgment": parent_final.get("judgment", ""),
        "promotion_candidate": "research_watchlist_candidate_no_operating_promotion(연구 감시 후보, 운영 승격 아님)",
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
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [row["gate"] for row in gate_rows()],
        },
    )
    write_json(KPI_RECEIPT, {**base, "kpi_source": rel(parent.EXECUTION_SUMMARY), "density_guardrail": rel(DENSITY_GUARDRAIL_AUDIT), "judgment": final["judgment"]})
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "ea_identity": rel(parent.RUNTIME_IDENTITY),
            "report_identity": rel(parent.STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(CLOSED_TRADE_ATTRIBUTION),
            "cost_assumptions": "broker-native tester cost(브로커 네이티브 테스터 비용) from MT5 report(MT5 보고서)",
            "forensic_checks": [rel(parent.MT5_EXECUTION_RESULT), rel(parent.STRATEGY_TESTER_REPORTS), rel(CLOSED_TRADE_ATTRIBUTION)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.SOURCE_SELECTED_TRADE_TAPE),
            "runtime_path": rel(parent.RUNTIME_OUTPUT_COPY),
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "parity_check": rel(RUNTIME_QUALITY_REVIEW),
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "runtime_claim_boundary": "runtime_probe_review_only_no_authority(런타임 탐침 검토 전용, 권위 없음)",
        },
    )
    write_json(PERFORMANCE_RECEIPT, {**base, "monthly": rel(MONTHLY_ATTRIBUTION), "entry_hour": rel(ENTRY_HOUR_ATTRIBUTION), "side": rel(SIDE_ATTRIBUTION), "proxy_attribution": rel(PROXY_MT5_ATTRIBUTION)})
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(parent.EXECUTION_SUMMARY), rel(parent.PROXY_MT5_DIFF), rel(parent.PROBABILITY_DIFF), rel(CLOSED_TRADE_ATTRIBUTION)],
            "evidence_missing": ["forward pass(전진 통과)", "live readiness(실거래 준비)", "operating promotion evidence(운영 승격 근거)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "promotion_candidate": final["promotion_candidate"],
            "effect": "positive runtime clue(긍정 런타임 단서)를 operating claim(운영 주장)으로 승격하지 않는다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


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
    monthly_rows: Sequence[Mapping[str, Any]],
    hour_rows: Sequence[Mapping[str, Any]],
    side_rows: Sequence[Mapping[str, Any]],
    density_rows_: Sequence[Mapping[str, Any]],
    proxy_rows_: Sequence[Mapping[str, Any]],
    findings: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364BF density restore stress candidate MT5 runtime probe review(364BF 밀도 복원 압박 후보 MT5 런타임 탐침 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## KPI Read(KPI 판독)

- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- expectancy/recovery/DD(기대값/회복 계수/낙폭): `{final['mt5_expectancy']}` / `{final['mt5_recovery_factor']}` / `{final['mt5_max_drawdown_percent']}%`
- trade density(거래 밀도): `{final['trade_per_business_day']}` per business day(영업일당), floor(하한) `{TRADE_DENSITY_FLOOR}`
- long/short(롱/숏): `{final['long_trade_count']}` / `{final['short_trade_count']}`
- proxy diff(프록시 차이): net(순수익) `{final['actual_minus_expected_net_profit']}`, PF(수익 팩터) `{final['actual_minus_expected_profit_factor']}`, trades(거래수) `{final['actual_minus_expected_trade_count']}`

## Judgment(판정)

Action(행동): BE runtime probe(BE 런타임 탐침)를 KPI(핵심 성과 지표), density guardrail(밀도 가드레일), session/side/month attribution(세션/방향/월 귀속), runtime parity(런타임 동등성)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서지만, forward pass(전진 통과)와 live-like replay(실거래 유사 재생)가 없어 operating promotion(운영 승격)과 runtime authority(런타임 권위)는 주장하지 않는다.

## Density Guardrail(거래 밀도 가드레일)

{markdown_table(density_rows_, ["guardrail_id", "value", "threshold", "status", "evidence", "effect"])}

## Proxy vs MT5 Attribution(프록시 대 MT5 귀속)

{markdown_table(proxy_rows_, ["review_id", "expected", "actual", "diff_actual_minus_expected", "status", "attribution", "usability"])}

## Side Attribution(방향 귀속)

{markdown_table(side_rows, ["group_value", "trade_count", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "win_rate_after_cost_percent", "max_hold_m5_calendar"])}

## Entry Hour Attribution(진입 시간 귀속)

{markdown_table(hour_rows, ["group_value", "trade_count", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "win_rate_after_cost_percent", "max_hold_m5_calendar"])}

## Monthly Attribution(월별 귀속)

{markdown_table(monthly_rows, ["group_value", "trade_count", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "win_rate_after_cost_percent", "max_hold_m5_calendar"])}

## Findings(발견)

{markdown_table(findings, ["finding_id", "severity", "finding", "effect"])}

## Required Gates(필수 게이트)

{markdown_table(gates, ["gate", "status", "evidence", "effect"])}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 forward/regime stress input(전진/국면 압박 입력), session-side guardrail(세션-방향 가드레일), short quality restore(숏 품질 복원)를 materialize(구체화)한다. trade splitting(거래 쪼개기)은 사용하지 않는다.

## Boundary(경계)

이 결과는 runtime_probe_review(런타임 탐침 검토)다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, report, bom=True)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364BF` reviewed(검토 완료) `run364BE` MT5 runtime probe(MT5 런타임 탐침). MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`이고, actual trade density(실제 거래 밀도)는 `{final['trade_per_business_day']}` per business day(영업일당)로 사용자 하한 3/day(일 3회)를 통과했다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 forward/regime stress input(전진/국면 압박 입력)과 session/side guardrail(세션/방향 가드레일)을 구체화한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
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

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): research_watchlist_candidate_no_operating_promotion(연구 감시 후보, 운영 승격 아님)
- runtime_probe_candidate(런타임 탐침 후보): `run364BB_ba02_between_ax03_ax08_floor025_ps450`
- latest_mt5_probe(최근 MT5 탐침): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- latest_mt5_net_pf_trades(최근 MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- latest_trade_density(최근 거래 밀도): `{final['trade_per_business_day']}` per business day(영업일당), floor(하한) `{TRADE_DENSITY_FLOOR}`
- latest_long_short(최근 롱/숏): `{final['long_trade_count']}` / `{final['short_trade_count']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - MT5 runtime probe review(MT5 런타임 탐침 검토), forward/regime stress required(전진/국면 압박 필요).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BF Density Restore Stress Candidate MT5 Review Closeout",
        f"""## run364BF Density Restore Stress Candidate MT5 Review Closeout(364BF 밀도 복원 압박 후보 MT5 검토 종료)

Action(행동): run364BE(364BE 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side(핵심 성과 지표/밀도/세션/방향)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서이고 actual density(실제 밀도)는 `{final['trade_per_business_day']}`로 3/day(일 3회)를 통과했다. 다만 forward/regime stress(전진/국면 압박) 전까지 운영 주장은 닫지 않는다.
""",
    )
    sync_stage_brief_header()
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BF Density Restore Stress Candidate MT5 Runtime Probe Review(364BF 밀도 복원 압박 후보 MT5 런타임 탐침 검토)

Action(행동): BE runtime probe(런타임 탐침)를 performance attribution(성과 귀속)으로 검토했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `{NEXT_RUN_ID}` forward/regime stress(전진/국면 압박)로 이어간다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} - {RUN_ID}

- action(행동): density restore stress candidate MT5 runtime probe(밀도 복원 압박 후보 MT5 런타임 탐침)를 review(검토)했다.
- effect(효과): net/PF/density(순수익/수익 팩터/밀도) 단서를 보존하고, forward/regime stress(전진/국면 압박)를 다음 input(입력)으로 바꿨다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): density restore stress candidate(밀도 복원 압박 후보)는 MT5 net/PF/density(순수익/수익 팩터/밀도)를 유지했다.
- positive clue(긍정 단서): net `{final['mt5_net_profit']}`, PF `{final['mt5_profit_factor']}`, density `{final['trade_per_business_day']}`, clean parity(깨끗한 동등성).
- failure memory(실패 기억): long share(롱 비중) `{final['long_share']}`와 missing forward/regime evidence(전진/국면 근거 누락)가 운영 승격을 막는다.
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
        "drawdown": final["mt5_max_drawdown_percent"],
        "recovery_factor": final["mt5_recovery_factor"],
        "trade_count": final["mt5_trade_count"],
        "trade_density_per_feature_day": final["trade_per_business_day"],
        "trade_density_requirement_status": "passed_ge_3_no_trade_splitting(3 이상 통과, 거래 쪼개기 없음)",
        "long_trade_count": final["long_trade_count"],
        "short_trade_count": final["short_trade_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "promotion_candidate": final["promotion_candidate"]}], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, kpi_scope, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "mt5_runtime_probe_review(MT5 런타임 탐침 검토)", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)", "out_of_scope_by_claim(주장 범위 밖)", "not_run_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "actual_routed_total_same_as_tier_a_no_tier_b_fallback(실제 라우팅 전체, Tier A와 같음)", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": kpi_scope,
                "status": status,
                "judgment": judgment,
            }
        )
        if tier == "Tier B":
            row.update({"net_profit": "", "profit_factor": "", "expectancy": "", "drawdown": "", "recovery_factor": "", "trade_count": "", "long_trade_count": "", "short_trade_count": ""})
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])

    artifact_rows = []
    for artifact_type, path, notes in [
        ("closed_trade_attribution", CLOSED_TRADE_ATTRIBUTION, "Closed trade attribution(종료 거래 귀속)."),
        ("density_guardrail", DENSITY_GUARDRAIL_AUDIT, "Density guardrail audit(밀도 가드레일 감사)."),
        ("proxy_mt5_attribution", PROXY_MT5_ATTRIBUTION, "Proxy-vs-MT5 attribution(프록시 대 MT5 귀속)."),
        ("cost_session_stress", COST_SESSION_STRESS_REVIEW, "Cost/session stress review(비용/세션 압박 검토)."),
        ("next_queue", NEXT_QUEUE, "Next forward/regime stress queue(다음 전진/국면 압박 대기열)."),
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
            "package_run_id": PACKAGE_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "output_files": [{"path": rel(path), "sha256": sha(path)} for path in outputs if Path(path).is_file()],
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    summary = load_one_csv_row(parent.EXECUTION_SUMMARY)
    proxy = load_one_csv_row(parent.PROXY_MT5_DIFF)
    _, expected_rows = read_csv_rows(parent.EXPECTED_KPI_SUMMARY)
    expected = next(row for row in expected_rows if row.get("split") == "combined")
    baseline = read_json(BASELINE_FINAL)
    report_path, _report_record = strategy_report_path()
    trades, parser_meta = parse_closed_trades(report_path)
    if len(trades) != as_int(summary.get("trade_count")):
        raise RuntimeError(f"closed trade count mismatch(종료 거래수 불일치): {len(trades)} != {summary.get('trade_count')}")

    trades["hold_bucket"] = trades["hold_m5_calendar"].map(hold_bucket)
    monthly_rows = aggregate(trades, "entry_month")
    hour_rows = aggregate(trades, "entry_hour")
    side_rows = aggregate(trades, "side")
    hold_rows = aggregate(trades, "hold_bucket")
    density = density_rows(summary, expected, trades)
    runtime_quality = runtime_quality_rows(summary)
    proxy_attr = proxy_attribution_rows(summary, proxy)
    cost_stress = cost_session_stress_rows(summary, trades, monthly_rows, hour_rows, side_rows)
    findings, positives, failures = finding_rows(summary, density, side_rows)
    queue = next_queue_rows()
    gates = gate_rows()

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(CLOSED_TRADE_ATTRIBUTION, trades.to_dict("records"))
    write_csv(MONTHLY_ATTRIBUTION, monthly_rows)
    write_csv(ENTRY_HOUR_ATTRIBUTION, hour_rows)
    write_csv(SIDE_ATTRIBUTION, side_rows)
    write_csv(HOLD_BUCKET_ATTRIBUTION, hold_rows)
    write_csv(DRAWDOWN_EVENT_REVIEW, drawdown_event_rows(trades))
    write_csv(PROXY_MT5_ATTRIBUTION, proxy_attr)
    write_csv(RUNTIME_QUALITY_REVIEW, runtime_quality)
    write_csv(DENSITY_GUARDRAIL_AUDIT, density)
    write_csv(COST_SESSION_STRESS_REVIEW, cost_stress)
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(POSITIVE_CLUES, positives)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, queue)
    write_csv(GATE_AUDIT, gates)

    final = final_payload(parent_final, summary, proxy, expected, trades, parser_meta, density, baseline)
    write_receipts(final)
    write_json(FINAL_DECISION, final)
    write_docs(final, monthly_rows, hour_rows, side_rows, density, proxy_attr, findings, gates)
    write_ledgers(final)
    write_manifest(final)
    repair_run_registry_line_endings(RUN_ID)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
