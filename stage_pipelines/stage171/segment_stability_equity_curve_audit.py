from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, datetime
from html import unescape
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)

STAGE_ID = "171_adapter_research__segment_stability_equity_curve_audit"
RUN_NUMBER = "run171A"
RUN_ID = "run171A_stage171_segment_stability_equity_curve_audit_v1"
PACKET_ID = "stage171_segment_stability_equity_curve_audit_v1"
SOURCE_STAGE_ID = "170_adapter_research__stage169_net_density_followup_review"
SOURCE_RUN_ID = "run170A_stage170_stage169_net_density_followup_review_v1"
SOURCE_STAGE170_CLOSEOUT_COMMIT = "9e82e985bdd235efe4e04c9a36cde4368495e19e"
SOURCE_STAGE170_HASH_RECORD_COMMIT = "802fd1d18fe2d776866723556d63c409725f7c62"
NEXT_STAGE_ID = "172_adapter_research__validation_drawdown_concentration_repair"
NEXT_RUN_ID = "run172A_stage172_validation_drawdown_concentration_repair_v1"
NEXT_PACKET_ID = "stage172_validation_drawdown_concentration_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "open_stage172_validation_drawdown_concentration_repair_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage169_mt5_reports_completed"
LOCAL_UPDATED_ON = "2026-05-19"

PRIMARY_ADAPTER = "s169_short_pre_risk0350_h3_cd5_sht54_lng52"
BACKUP_ADAPTER = "s169_short_pre_risk0300_h3_cd5_sht54_lng52"
FAILURE_MEMORY_ADAPTER = "s169_short_pre_restore_long_risk0300_h3_cd5_sht54_lng52"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE170_REPORT = Path(
    "stages/170_adapter_research__stage169_net_density_followup_review/03_reviews/"
    "stage170_stage169_net_density_followup_review.md"
)
SOURCE_STAGE170_QUALITY = Path(
    "stages/170_adapter_research__stage169_net_density_followup_review/03_reviews/"
    "stage170_stage169_quality_matrix.csv"
)
SOURCE_STAGE170_SEGMENT = Path(
    "stages/170_adapter_research__stage169_net_density_followup_review/03_reviews/"
    "stage170_stage169_segment_review.csv"
)
SOURCE_STAGE170_DECISION = Path(
    "stages/170_adapter_research__stage169_net_density_followup_review/03_reviews/stage170_decision.md"
)
SOURCE_STAGE169_TRADE_AUDIT = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/03_reviews/stage169_trade_audit.csv"
)
SOURCE_STAGE169_SEGMENT = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/03_reviews/stage169_segment_kpi_summary.csv"
)
SOURCE_STAGE169_REPORT_ROOT = Path(
    "stages/169_adapter_research__net_density_lift_pf_preservation/02_runs/run169A/mt5/reports"
)

REPORT_PATH = REVIEWS_ROOT / "stage171_segment_stability_equity_curve_audit.md"
BALANCE_SUMMARY_PATH = REVIEWS_ROOT / "stage171_balance_curve_summary.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage171_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage171_concentration_audit.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage171_drawdown_recovery_summary.csv"
ROUTE_CSV_PATH = REVIEWS_ROOT / "stage171_route_summary.csv"
ROUTE_JSON_PATH = REVIEWS_ROOT / "stage171_route_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage171_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage171/segment_stability_equity_curve_audit.py")

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
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def abs_long_path(path: Path) -> str:
    resolved = str(io_path(path).resolve())
    if sys.platform == "win32" and not resolved.startswith("\\\\?\\") and len(resolved) >= 240:
        return "\\\\?\\" + resolved
    return resolved


def read_text_any(path: Path) -> str:
    data = Path(abs_long_path(path)).read_bytes()
    for encoding in ("utf-16", "utf-8-sig", "cp949", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")


def float_or_none(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "").replace("%", "").strip())
    except (TypeError, ValueError):
        return None


def rounded(value: Any, digits: int = 4) -> float | str:
    number = float_or_none(value)
    if number is None:
        return ""
    return round(number, digits)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def load_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


TAG_RE = re.compile(r"<[^>]+>")
ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
CELL_RE = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.IGNORECASE | re.DOTALL)


def clean_cell(raw: str) -> str:
    return unescape(TAG_RE.sub("", raw)).replace("\xa0", " ").strip()


def parse_report_deals(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    text = read_text_any(path)
    rows: list[dict[str, Any]] = []
    in_deals = False
    for row_html in ROW_RE.findall(text):
        cells = [clean_cell(cell) for cell in CELL_RE.findall(row_html)]
        if not cells:
            continue
        if {"시간", "거래", "종류", "방향", "수익", "잔액"}.issubset(set(cells)):
            in_deals = True
            continue
        if not in_deals or len(cells) < 13:
            continue
        deal_type = cells[3]
        direction = cells[4]
        if deal_type not in {"balance", "buy", "sell"}:
            continue
        rows.append(
            {
                "time": cells[0],
                "deal": cells[1],
                "symbol": cells[2],
                "type": deal_type,
                "direction": direction,
                "volume": rounded(cells[5], 4),
                "price": rounded(cells[6], 4),
                "order": cells[7],
                "commission": rounded(cells[8], 4),
                "swap": rounded(cells[9], 4),
                "profit": rounded(cells[10], 4),
                "balance": rounded(cells[11], 4),
                "comment": cells[12],
            }
        )
    return rows, extract_report_metrics(text)


def extract_report_metrics(text: str) -> dict[str, Any]:
    labels = [
        "Balance Drawdown Absolute",
        "Equity Drawdown Absolute",
        "Balance Drawdown Maximal",
        "Equity Drawdown Maximal",
        "Balance Drawdown Relative",
        "Equity Drawdown Relative",
        "Profit Factor",
    ]
    metrics: dict[str, Any] = {}
    for label in labels:
        pattern = re.compile(re.escape(label) + r":</td>\s*<td[^>]*><b>(.*?)</b>", re.IGNORECASE | re.DOTALL)
        match = pattern.search(text)
        if match:
            value = clean_cell(match.group(1))
            key = label.lower().replace(" ", "_")
            metrics[key] = value
            amount, percent = parse_amount_percent(value)
            if amount is not None:
                metrics[f"{key}_amount"] = amount
            if percent is not None:
                metrics[f"{key}_percent"] = percent
    return metrics


def parse_amount_percent(value: str) -> tuple[float | None, float | None]:
    numbers = re.findall(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
    if not numbers:
        return None, None
    if "%" in value and value.strip().startswith(tuple("0123456789")):
        percent = float(numbers[0])
        amount = float(numbers[1]) if len(numbers) > 1 else None
        return amount, percent
    amount = float(numbers[0])
    percent = float(numbers[1]) if "%" in value and len(numbers) > 1 else None
    return amount, percent


def report_path_for(split: str) -> Path:
    suffix = "rt_val.htm" if split == "validation_is" else "rt_oos.htm"
    matches = sorted(SOURCE_STAGE169_REPORT_ROOT.glob(f"*{PRIMARY_ADAPTER}*{suffix}"))
    if not matches:
        raise FileNotFoundError(f"missing report(보고서): {PRIMARY_ADAPTER} {split}")
    return matches[0]


def out_deals(deals: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in deals:
        if row.get("direction") != "out" or float_or_none(row.get("profit")) is None:
            continue
        item = dict(row)
        item["net_pnl"] = deal_pnl(item)
        rows.append(item)
    return rows


def deal_pnl(row: Mapping[str, Any]) -> float:
    return sum(
        float_or_none(row.get(key)) or 0.0
        for key in ("profit", "commission", "swap")
    )


def initial_balance(deals: Sequence[Mapping[str, Any]]) -> float:
    for row in deals:
        if row.get("type") == "balance":
            balance = float_or_none(row.get("balance"))
            if balance is not None:
                return balance
    first = float_or_none(deals[0].get("balance")) if deals else None
    return first if first is not None else 0.0


def drawdown_stats(points: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not points:
        return {}
    peak_balance = float(points[0]["balance"])
    peak_index = 0
    worst = {
        "max_drawdown_amount": 0.0,
        "max_drawdown_percent": 0.0,
        "drawdown_peak_index": 0,
        "drawdown_trough_index": 0,
        "drawdown_peak_time": points[0]["time"],
        "drawdown_trough_time": points[0]["time"],
    }
    underwater_start: int | None = None
    max_underwater_trades = 0
    for idx, point in enumerate(points):
        balance = float(point["balance"])
        if balance >= peak_balance:
            peak_balance = balance
            peak_index = idx
            underwater_start = None
        else:
            if underwater_start is None:
                underwater_start = peak_index
            max_underwater_trades = max(max_underwater_trades, idx - underwater_start)
        drawdown = peak_balance - balance
        drawdown_percent = drawdown / peak_balance * 100 if peak_balance else 0.0
        if drawdown > worst["max_drawdown_amount"]:
            worst.update(
                {
                    "max_drawdown_amount": round(drawdown, 4),
                    "max_drawdown_percent": round(drawdown_percent, 4),
                    "drawdown_peak_index": peak_index,
                    "drawdown_trough_index": idx,
                    "drawdown_peak_time": points[peak_index]["time"],
                    "drawdown_trough_time": point["time"],
                }
            )
    peak_balance_for_worst = float(points[int(worst["drawdown_peak_index"])]["balance"])
    recovery_index = None
    for idx in range(int(worst["drawdown_trough_index"]) + 1, len(points)):
        if float(points[idx]["balance"]) >= peak_balance_for_worst:
            recovery_index = idx
            break
    worst["recovered"] = recovery_index is not None
    worst["recovery_index"] = recovery_index if recovery_index is not None else ""
    worst["recovery_time"] = points[recovery_index]["time"] if recovery_index is not None else ""
    worst["recovery_trades"] = (
        recovery_index - int(worst["drawdown_trough_index"]) if recovery_index is not None else ""
    )
    worst["max_underwater_trades"] = max_underwater_trades
    worst["final_balance_is_new_high"] = float(points[-1]["balance"]) >= max(float(point["balance"]) for point in points)
    return worst


def concentration_stats(closed: Sequence[Mapping[str, Any]], net: float) -> dict[str, Any]:
    profits = [float(row.get("net_pnl", deal_pnl(row))) for row in closed]
    winners = sorted([value for value in profits if value > 0], reverse=True)
    losers = sorted([value for value in profits if value < 0])
    denominator = net if abs(net) > 1e-9 else 1.0
    last_quarter = profits[int(len(profits) * 0.75) :] if profits else []
    return {
        "top1_winner": round(winners[0], 4) if winners else 0.0,
        "top1_winner_share_of_net": round((winners[0] / denominator), 4) if winners else 0.0,
        "top3_winner_share_of_net": round(sum(winners[:3]) / denominator, 4) if winners else 0.0,
        "top5_winner_share_of_net": round(sum(winners[:5]) / denominator, 4) if winners else 0.0,
        "worst_loss": round(losers[0], 4) if losers else 0.0,
        "worst_loss_share_of_net_abs": round(abs(losers[0]) / denominator, 4) if losers else 0.0,
        "last_quarter_net": round(sum(last_quarter), 4),
        "last_quarter_net_share": round(sum(last_quarter) / denominator, 4) if profits else 0.0,
    }


def profit_factor(profits: Sequence[float]) -> float | str:
    wins = sum(value for value in profits if value > 0)
    losses = abs(sum(value for value in profits if value < 0))
    if losses == 0:
        return ""
    return round(wins / losses, 6)


def monthly_rows(split: str, closed: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[float]] = {}
    for row in closed:
        month = str(row["time"])[:7]
        buckets.setdefault(month, []).append(float(row.get("net_pnl", deal_pnl(row))))
    rows = []
    for month, values in sorted(buckets.items()):
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": PRIMARY_ADAPTER,
                "split": split,
                "month": month,
                "trade_count": len(values),
                "net_profit": round(sum(values), 4),
                "profit_factor": profit_factor(values),
                "winner_count": sum(1 for value in values if value > 0),
                "loser_count": sum(1 for value in values if value < 0),
                "quality_flag": month_quality_flag(values),
            }
        )
    return rows


def month_quality_flag(values: Sequence[float]) -> str:
    net = sum(values)
    pf = profit_factor(values)
    if net < 0:
        return "negative_month(손실 월)"
    if isinstance(pf, float) and pf < LEGACY_34D["profit_factor"]:
        return "pf_below_34d(34D 미만 수익요인)"
    return "acceptable_measurement_only(측정상 허용)"


def stage170_late_share(segment_rows: Sequence[Mapping[str, str]], split: str) -> float | None:
    for row in segment_rows:
        if (
            row.get("adapter_id") == PRIMARY_ADAPTER
            and row.get("split") == split
            and row.get("segment") == "late"
        ):
            return float_or_none(row.get("net_contribution_of_split"))
    return None


def stage170_weak_segments(quality_rows: Sequence[Mapping[str, str]]) -> str:
    for row in quality_rows:
        if row.get("adapter_id") == PRIMARY_ADAPTER:
            return row.get("validation_weak_segments", "")
    return ""


def trade_audit_lookup(rows: Sequence[Mapping[str, str]], split: str) -> Mapping[str, str]:
    for row in rows:
        if row.get("variant_id") == PRIMARY_ADAPTER and row.get("split") == split:
            return row
    return {}


def build_audit() -> dict[str, Any]:
    trade_audit_rows = load_csv(SOURCE_STAGE169_TRADE_AUDIT)
    segment_rows = load_csv(SOURCE_STAGE170_SEGMENT)
    quality_rows = load_csv(SOURCE_STAGE170_QUALITY)
    balance_rows: list[dict[str, Any]] = []
    concentration_rows: list[dict[str, Any]] = []
    monthly: list[dict[str, Any]] = []
    drawdown_rows: list[dict[str, Any]] = []

    for split in ("validation_is", "oos"):
        report_path = report_path_for(split)
        deals, report_metrics = parse_report_deals(report_path)
        closed = out_deals(deals)
        start_balance = initial_balance(deals)
        points = [{"time": deals[0]["time"] if deals else "", "balance": start_balance, "profit": 0.0}]
        running_balance = start_balance
        for row in closed:
            pnl = float(row.get("net_pnl", deal_pnl(row)))
            running_balance += pnl
            points.append({"time": row["time"], "balance": round(running_balance, 4), "profit": pnl})
        final_balance = float(points[-1]["balance"]) if points else start_balance
        net = final_balance - start_balance
        dd = drawdown_stats(points)
        conc = concentration_stats(closed, net)
        trade_audit = trade_audit_lookup(trade_audit_rows, split)
        late_share = stage170_late_share(segment_rows, split)
        weak_segments = stage170_weak_segments(quality_rows) if split == "validation_is" else ""
        validation_dd_fail = split == "validation_is" and dd.get("max_drawdown_percent", 0) > LEGACY_34D["max_drawdown_percent"]
        late_concentration_fail = late_share is not None and late_share > 0.50
        weak_segment_fail = split == "validation_is" and bool(weak_segments)
        split_flag = split_quality_flag(split, validation_dd_fail, late_concentration_fail, weak_segment_fail)

        base = {
            "run_id": RUN_ID,
            "adapter_id": PRIMARY_ADAPTER,
            "split": split,
            "report_path": rel(report_path),
            "initial_balance": round(start_balance, 4),
            "final_balance": round(final_balance, 4),
            "net_profit": round(net, 4),
            "closed_trade_count": len(closed),
            "profit_factor": profit_factor([float(row.get("net_pnl", deal_pnl(row))) for row in closed]),
            "legacy_34d_pf": LEGACY_34D["profit_factor"],
            "legacy_34d_dd_percent": LEGACY_34D["max_drawdown_percent"],
            "max_drawdown_amount": dd.get("max_drawdown_amount", ""),
            "max_drawdown_percent": dd.get("max_drawdown_percent", ""),
            "report_balance_drawdown_maximal": report_metrics.get("balance_drawdown_maximal", ""),
            "report_equity_drawdown_maximal": report_metrics.get("equity_drawdown_maximal", ""),
            "report_balance_drawdown_relative": report_metrics.get("balance_drawdown_relative", ""),
            "report_equity_drawdown_relative": report_metrics.get("equity_drawdown_relative", ""),
            "late_net_share": rounded(late_share, 4),
            "validation_weak_segments": weak_segments,
            "cost_stressed_expectancy": rounded(trade_audit.get("cost_stressed_expectancy"), 6),
            "mfe_capture_ratio": rounded(trade_audit.get("mfe_capture_ratio"), 6),
            "same_move_reentry_ratio": rounded(trade_audit.get("same_move_reentry_ratio"), 6),
            "split_quality_flag": split_flag,
        }
        balance_rows.append(base)
        concentration_rows.append({"run_id": RUN_ID, "adapter_id": PRIMARY_ADAPTER, "split": split, **conc})
        drawdown_rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": PRIMARY_ADAPTER,
                "split": split,
                **dd,
                "drawdown_flag": "dd_above_34d(34D 초과 낙폭)" if validation_dd_fail else "dd_measurement_only(낙폭 측정 전용)",
            }
        )
        monthly.extend(monthly_rows(split, closed))
    return {
        "balance_rows": balance_rows,
        "concentration_rows": concentration_rows,
        "monthly_rows": monthly,
        "drawdown_rows": drawdown_rows,
        "decision": decide(balance_rows),
    }


def split_quality_flag(split: str, validation_dd_fail: bool, late_concentration_fail: bool, weak_segment_fail: bool) -> str:
    flags: list[str] = []
    if validation_dd_fail:
        flags.append("validation_dd_above_34d(검증 낙폭 34D 초과)")
    if late_concentration_fail:
        flags.append("late_concentration_above_50pct(후반 집중 50% 초과)")
    if weak_segment_fail:
        flags.append("validation_early_mid_pf_below_34d(검증 초중반 수익요인 34D 미만)")
    if not flags:
        flags.append("acceptable_measurement_only(측정상 허용)")
    return ";".join(flags)


def decide(balance_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validation = next(row for row in balance_rows if row["split"] == "validation_is")
    oos = next(row for row in balance_rows if row["split"] == "oos")
    validation_flags = str(validation.get("split_quality_flag", ""))
    oos_flags = str(oos.get("split_quality_flag", ""))
    failed = "validation_dd_above_34d" in validation_flags or "validation_early_mid_pf_below_34d" in validation_flags
    return {
        "decision": DECISION,
        "audit_judgment": (
            "segment_equity_audit_failed_repair_required_not_final"
            if failed
            else "segment_equity_audit_passed_measurement_only_not_final"
        ),
        "why": (
            "Validation(검증) drawdown(낙폭) and early/mid PF(초반/중반 수익요인) fail the research-grade stability bar(연구급 안정성 기준). "
            "OOS(표본외)는 강하지만 final(최종) 주장은 금지한다."
            if failed
            else "Primary(주 후보) passes this audit(감사), but package(패키지) completion(완료)은 아직 아니다."
        ),
        "validation_flags": validation_flags,
        "oos_flags": oos_flags,
        "next_stage": NEXT_STAGE_ID,
    }


def table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    labels = {
        "split": "split(분할)",
        "net_profit": "net_profit(순손익)",
        "profit_factor": "profit_factor(수익요인)",
        "max_drawdown_amount": "max_drawdown_amount(최대 낙폭 금액)",
        "max_drawdown_percent": "max_drawdown_percent(최대 낙폭률)",
        "report_balance_drawdown_relative": "report_balance_drawdown_relative(보고서 잔고 상대 낙폭)",
        "report_equity_drawdown_relative": "report_equity_drawdown_relative(보고서 자산 상대 낙폭)",
        "late_net_share": "late_net_share(후반 순손익 비중)",
        "validation_weak_segments": "validation_weak_segments(검증 약한 구간)",
        "split_quality_flag": "split_quality_flag(분할 품질 표식)",
        "drawdown_peak_time": "drawdown_peak_time(낙폭 고점 시간)",
        "drawdown_trough_time": "drawdown_trough_time(낙폭 저점 시간)",
        "recovered": "recovered(회복 여부)",
        "recovery_time": "recovery_time(회복 시간)",
        "recovery_trades": "recovery_trades(회복 거래 수)",
        "max_underwater_trades": "max_underwater_trades(최장 수중 거래 수)",
        "drawdown_flag": "drawdown_flag(낙폭 표식)",
        "top1_winner_share_of_net": "top1_winner_share_of_net(최대 승리 순손익 비중)",
        "top3_winner_share_of_net": "top3_winner_share_of_net(상위 3승 순손익 비중)",
        "top5_winner_share_of_net": "top5_winner_share_of_net(상위 5승 순손익 비중)",
        "worst_loss_share_of_net_abs": "worst_loss_share_of_net_abs(최대 손실 순손익 비중)",
        "last_quarter_net_share": "last_quarter_net_share(마지막 25% 순손익 비중)",
    }
    header = "| " + " | ".join(labels.get(column, column) for column in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def report_markdown(audit: Mapping[str, Any], routes: Sequence[Mapping[str, Any]]) -> str:
    balance_rows = audit["balance_rows"]
    concentration_rows = audit["concentration_rows"]
    drawdown_rows = audit["drawdown_rows"]
    decision = audit["decision"]
    return f"""# Stage171 Segment/Equity Curve Audit(171단계 구간/자산 곡선 감사)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE170_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_STAGE170_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Does `{PRIMARY_ADAPTER}` survive segment stability(구간 안정성), equity curve(자산 곡선), balance curve(잔고 곡선), concentration(집중도), drawdown recovery(낙폭 회복), and MFE/MAE behavior(MFE/MAE 동작) audit as a research candidate(연구 후보)?

## Answer(답)

No(아니오). KPI(핵심 성과 지표)는 34D(34D)에 매우 가까워졌지만, research-grade candidate(연구급 후보)로 바로 넘기기에는 validation drawdown(검증 낙폭), validation early/mid PF(검증 초반/중반 수익요인), late concentration(후반 집중)이 약하다.

Effect(효과): Stage172(172단계)는 open-ended tuning(개방형 튜닝)이 아니라 validation DD/concentration repair(검증 낙폭/집중도 수리)만 좁게 다룬다.

## Balance Curve Summary(잔고 곡선 요약)

{table(balance_rows, ["split", "net_profit", "profit_factor", "max_drawdown_amount", "max_drawdown_percent", "report_balance_drawdown_relative", "report_equity_drawdown_relative", "late_net_share", "validation_weak_segments", "split_quality_flag"])}

## Drawdown Recovery(낙폭 회복)

{table(drawdown_rows, ["split", "max_drawdown_amount", "max_drawdown_percent", "drawdown_peak_time", "drawdown_trough_time", "recovered", "recovery_time", "recovery_trades", "max_underwater_trades", "drawdown_flag"])}

## Concentration(집중도)

{table(concentration_rows, ["split", "top1_winner_share_of_net", "top3_winner_share_of_net", "top5_winner_share_of_net", "worst_loss_share_of_net_abs", "last_quarter_net_share"])}

## Decision Basis(판정 근거)

- action(행동): MT5 report(메타트레이더5 보고서)의 closed deals(청산 거래)에서 balance curve(잔고 곡선)를 재구성했다. effect(효과): final net(최종 순손익)만 보지 않고 peak-to-trough drawdown(고점-저점 낙폭)과 recovery(회복)를 확인했다.
- action(행동): Stage170 segment review(170단계 구간 검토)를 결합했다. effect(효과): validation early/mid PF(검증 초반/중반 수익요인) 약점과 late contribution(후반 기여)을 그대로 보존했다.
- action(행동): Stage169 trade audit(169단계 거래 감사)의 cost stress/MFE/re-entry(비용 압박/MFE/재진입)를 같이 읽었다. effect(효과): OOS(표본외)가 강한 부분은 보존하되, 약한 validation(검증)을 다음 repair(수리) 질문으로 넘긴다.

## Route Decision(경로 판정)

1. primary(주): `{routes[0]["route"]}`.
2. guardrail(보호 기준): `{routes[1]["route"]}`.
3. failure_memory(실패 기억): `{routes[2]["route"]}`.

Audit judgment(감사 판정): `{decision["audit_judgment"]}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def route_rows(audit: Mapping[str, Any]) -> list[dict[str, Any]]:
    decision = audit["decision"]
    return [
        {
            "run_id": RUN_ID,
            "route_rank": 1,
            "route": "stage172_validation_drawdown_concentration_repair",
            "adapter_id": PRIMARY_ADAPTER,
            "bounded_question": "Can validation DD/concentration(검증 낙폭/집중도)를 낮추면서 near-34D net/OOS PF/DD(34D 근접 순손익/표본외 수익요인/낙폭)를 보존할 수 있는가?",
            "why": decision["why"],
            "do_not_do": "Do not run open-ended hunting(개방형 사냥 금지), do not claim final(최종 주장 금지), do not start ONNX hardening(ONNX 경화 시작 금지).",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 2,
            "route": "preserve_oos_strength_and_risk_atr_telemetry",
            "adapter_id": PRIMARY_ADAPTER,
            "bounded_question": "Preserve OOS(표본외) PF/DD(수익요인/낙폭), cost-stressed expectancy(비용 압박 기대값), MFE capture(MFE 포착), and low same-move re-entry(낮은 동일 움직임 재진입).",
            "why": "OOS(표본외)는 강하므로 repair(수리)는 validation weakness(검증 약점)를 겨냥해야 한다.",
            "do_not_do": "Do not damage OOS(표본외 훼손 금지) to make validation(검증) look smoother.",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 3,
            "route": "keep_long_restore_as_failure_memory",
            "adapter_id": FAILURE_MEMORY_ADAPTER,
            "bounded_question": "Keep long restore(롱 복원)를 failure memory(실패 기억)로 둔다.",
            "why": "Stage170(170단계)에서 OOS PF/DD(표본외 수익요인/낙폭) 손상이 확인됐다.",
            "do_not_do": "Do not cherry-pick validation net(검증 순손익만 골라보기 금지).",
        },
    ]


def decision_markdown(audit: Mapping[str, Any]) -> str:
    decision = audit["decision"]
    return f"""# Stage171 Decision(171단계 판정)

- decision(판정): `{DECISION}`
- audit_judgment(감사 판정): `{decision["audit_judgment"]}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage170_closeout_commit(원천 170단계 종료 커밋): `{SOURCE_STAGE170_CLOSEOUT_COMMIT}`
- source_stage170_hash_record_commit(원천 170단계 해시 기록 커밋): `{SOURCE_STAGE170_HASH_RECORD_COMMIT}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- balance_summary(잔고 요약): `{rel(BALANCE_SUMMARY_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_audit(집중도 감사): `{rel(CONCENTRATION_PATH)}`
- drawdown_recovery(낙폭 회복): `{rel(DRAWDOWN_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage171(171단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        BALANCE_SUMMARY_PATH,
        MONTHLY_KPI_PATH,
        CONCENTRATION_PATH,
        DRAWDOWN_PATH,
        ROUTE_CSV_PATH,
        ROUTE_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        SOURCE_STAGE170_REPORT,
        SOURCE_STAGE170_QUALITY,
        SOURCE_STAGE170_SEGMENT,
        SOURCE_STAGE170_DECISION,
        SOURCE_STAGE169_TRADE_AUDIT,
        SOURCE_STAGE169_SEGMENT,
        report_path_for("validation_is"),
        report_path_for("oos"),
    ]
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage171_audit_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage171 audit evidence(171단계 감사 근거); no deployment(배포) or live-readiness(실거래 준비) claim(주장).",
                }
            )
    return rows


def write_ledgers() -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage171_segment_equity_curve_audit",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage170_closeout_commit", SOURCE_STAGE170_CLOSEOUT_COMMIT),
                        ("source_stage170_hash_record_commit", SOURCE_STAGE170_HASH_RECORD_COMMIT),
                        ("primary_adapter", PRIMARY_ADAPTER),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only_no_inheritance"),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__audit",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "audit",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "stage171_segment_equity_curve_audit",
            "tier_scope": "Stage169 MT5 reports and Stage170 review",
            "kpi_scope": "segment_equity_concentration_drawdown_recovery",
            "scoreboard_lane": "research_audit",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": "validation_dd_concentration_repair_required",
            "guardrail_kpi": "no_final_adapter_no_deployment_no_live_readiness",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage171 audited Stage169 near-34D adapter and opened Stage172 bounded repair.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifacts = artifact_rows()
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {
        "run_registry": run_payload,
        "alpha_ledger": alpha_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(audit: Mapping[str, Any], routes: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "audit": audit,
        "route_rows": list(routes),
        "report_path": rel(REPORT_PATH),
        "balance_summary": rel(BALANCE_SUMMARY_PATH),
        "monthly_kpi": rel(MONTHLY_KPI_PATH),
        "concentration_audit": rel(CONCENTRATION_PATH),
        "drawdown_recovery": rel(DRAWDOWN_PATH),
        "route_summary": rel(ROUTE_CSV_PATH),
        "ledger_payload": ledger_payload,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage171 Closeout Packet(171단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage171(171단계) audit(감사) 결과를 packet(작업 묶음)에 연결하고 Stage172(172단계)의 validation drawdown/concentration repair(검증 낙폭/집중도 수리) 질문을 좁혔다.
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage172(172단계)는 Stage171(171단계) audit(감사)에서 확인한 validation drawdown/concentration weakness(검증 낙폭/집중도 약점)만 repair(수리)한다.

## Bounded Question(경계 질문)

Can `{PRIMARY_ADAPTER}` or a bounded sibling(경계 형제 후보) reduce validation DD(검증 낙폭), validation early/mid PF weakness(검증 초반/중반 수익요인 약점), and late concentration(후반 집중)을 개선하면서 near-34D net(34D 근접 순손익), OOS PF/DD(표본외 수익요인/낙폭), risk/ATR telemetry(위험/ATR 텔레메트리)를 보존할 수 있는가?

Effect(효과): Stage172(172단계)는 open-ended search(개방형 탐색)가 아니라 Stage171(171단계)에서 드러난 약점만 고친다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage172 Inputs(172단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage171_report(171단계 보고서): `{rel(REPORT_PATH)}`
- balance_summary(잔고 요약): `{rel(BALANCE_SUMMARY_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_audit(집중도 감사): `{rel(CONCENTRATION_PATH)}`
- drawdown_recovery(낙폭 회복): `{rel(DRAWDOWN_PATH)}`
- stage170_report(170단계 보고서): `{rel(SOURCE_STAGE170_REPORT)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage172 Review Index(172단계 검토 색인)

- status(상태): `open_planned_from_stage171`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage172 Selection Status(172단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage171`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on: .*$", f"updated_on: '{LOCAL_UPDATED_ON}'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage171(171단계) closed(종료) as `{DECISION}` and Stage172(172단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): near-34D(34D 근접) 숫자를 final(최종)로 보지 않고 validation drawdown/concentration repair(검증 낙폭/집중도 수리)로 넘긴다.
- >-
  Stage171 evidence(171단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(BALANCE_SUMMARY_PATH)}`, `{rel(MONTHLY_KPI_PATH)}`, `{rel(CONCENTRATION_PATH)}`, `{rel(DRAWDOWN_PATH)}`에 있다. Effect(효과): equity/balance curve(자산/잔고 곡선), segment(구간), recovery(회복), concentration(집중도)를 같이 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\n\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage171_segment_stability_equity_curve_audit:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage171_segment_stability_equity_curve_audit:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage170_closeout_commit: {SOURCE_STAGE170_CLOSEOUT_COMMIT}
  source_stage170_hash_record_commit: {SOURCE_STAGE170_HASH_RECORD_COMMIT}
  decision: {DECISION}
  primary_adapter: {PRIMARY_ADAPTER}
  report_path: {rel(REPORT_PATH)}
  balance_summary_path: {rel(BALANCE_SUMMARY_PATH)}
  monthly_kpi_path: {rel(MONTHLY_KPI_PATH)}
  concentration_audit_path: {rel(CONCENTRATION_PATH)}
  drawdown_recovery_path: {rel(DRAWDOWN_PATH)}
  route_summary_path: {rel(ROUTE_CSV_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{PRIMARY_ADAPTER}`
- status(상태): `stage171_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage171(171단계)는 Stage169/170(169/170단계)의 near-34D(34D 근접) 후보를 segment/equity/concentration audit(구간/자산 곡선/집중도 감사)로 판독했다. Effect(효과): Stage172(172단계)는 validation drawdown/concentration repair(검증 낙폭/집중도 수리)로만 좁힌다.

## Latest Stage171 Evidence(최신 171단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- balance_summary(잔고 요약): `{rel(BALANCE_SUMMARY_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_audit(집중도 감사): `{rel(CONCENTRATION_PATH)}`
- drawdown_recovery(낙폭 회복): `{rel(DRAWDOWN_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage171 Selection Status(171단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- primary_adapter(주 어댑터): `{PRIMARY_ADAPTER}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage171(171단계)은 audit-only(감사 전용) 질문만 닫고, 전체 목표 완료를 주장하지 않는다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage171 Review Index(171단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- balance_summary(잔고 요약): `{rel(BALANCE_SUMMARY_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_audit(집중도 감사): `{rel(CONCENTRATION_PATH)}`
- drawdown_recovery(낙폭 회복): `{rel(DRAWDOWN_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage171 segment/equity curve audit closeout(171단계 구간/자산 곡선 감사 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage172(172단계)를 validation drawdown/concentration repair(검증 낙폭/집중도 수리)로 열었다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    audit = build_audit()
    routes = route_rows(audit)
    write_csv(BALANCE_SUMMARY_PATH, audit["balance_rows"])
    write_csv(MONTHLY_KPI_PATH, audit["monthly_rows"])
    write_csv(CONCENTRATION_PATH, audit["concentration_rows"])
    write_csv(DRAWDOWN_PATH, audit["drawdown_rows"])
    write_csv(ROUTE_CSV_PATH, routes)
    write_json(
        ROUTE_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "audit": audit,
            "route_rows": routes,
            "legacy_34d": LEGACY_34D,
            "primary_adapter": PRIMARY_ADAPTER,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_md(REPORT_PATH, report_markdown(audit, routes))
    write_md(DECISION_PATH, decision_markdown(audit))
    ledger_payload = write_ledgers()
    write_packet_files(audit, routes, ledger_payload)
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "audit_judgment": audit["decision"]["audit_judgment"],
                    "report_path": rel(REPORT_PATH),
                    "next_stage": NEXT_STAGE_ID,
                    "overall_goal_complete": False,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
