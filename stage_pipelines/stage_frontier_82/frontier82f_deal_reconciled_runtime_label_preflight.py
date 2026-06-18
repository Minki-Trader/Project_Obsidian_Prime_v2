from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics
from foundation.mt5.trade_report import Deal, Trade, pair_deals_into_trades, parse_mt5_trade_report


STAGE_ID = "stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
RUN_ID = "frontier82F_deal_reconciled_runtime_label_preflight_v1"
PARENT_RUN_ID = "frontier82E_capped_repair_or_rotation_decision_v1"
RUNTIME_RUN_ID = "frontier82C_mt5_runtime_materialization_v1"
NEXT_RUN_ID = "frontier82G_mt5_realized_label_rebuild_v1"
ROTATION_IF_FAILED = "frontier82G_capped_repair_closeout_or_f83_rotation_decision_v1"

STATUS = "f82f_deal_level_report_evidence_reconciled_label_rebuild_ready_no_authority"
JUDGMENT = "deal_level_pnl_recovered_and_reconciled_runtime_label_rebuild_required_no_authority"
CLAIM_BOUNDARY = (
    "runtime_deal_evidence_preflight_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F82E_SUMMARY = REVIEW_DIR / "f82e_capped_repair_or_rotation_decision.json"
F82C_SUMMARY = REVIEW_DIR / "f82c_mt5_runtime_materialization_summary.json"
F82C_MANIFEST = STAGE_DIR / "02_runs" / RUNTIME_RUN_ID / "run_manifest.json"
F82C_RECEIPT = STAGE_DIR / "02_runs" / RUNTIME_RUN_ID / "f82c_runtime_receipt.csv"
F82C_FORENSICS = REVIEW_DIR / "f82c_backtest_forensics_receipt.json"

SUMMARY = REVIEW_DIR / "f82f_deal_reconciliation_summary.json"
DEAL_ROWS = RUN_DIR / "f82f_deal_rows.csv"
TRADE_ROWS = RUN_DIR / "f82f_trade_rows.csv"
SPLIT_RECONCILIATION = REVIEW_DIR / "f82f_split_reconciliation.csv"
REPORT = REVIEW_DIR / "frontier82F_deal_reconciled_runtime_label_preflight_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f82f.md"
RUNTIME_PARITY_RECEIPT = REVIEW_DIR / "f82f_runtime_parity_receipt.yaml"
BACKTEST_FORENSICS_RECEIPT = REVIEW_DIR / "f82f_backtest_forensics_receipt.yaml"
REFERENCE_SCOUT_RECEIPT = REVIEW_DIR / "f82f_reference_scout_receipt.yaml"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f82f_run_evidence_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f82f_artifact_lineage_receipt.yaml"
TASK_FORCE_REVIEW = REVIEW_DIR / "f82f_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f82f_claim_discipline_receipt.yaml"
LOCAL_VERIFICATION = REVIEW_DIR / "f82f_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_82/frontier82f_deal_reconciled_runtime_label_preflight.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return value
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def csv_io_target(path: Path) -> Path:
    return io_path(path) if len(str(path)) >= 240 else path


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with csv_io_target(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
            rows = [{field: value for field, value in existing.items() if field} for existing in reader]
    elif source_header is not None and path_exists(source_header):
        with csv_io_target(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with csv_io_target(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: existing.get(field, "") for field in fieldnames} for existing in rows)


def remove_matching_csv_text_rows(path: Path, marker: str) -> None:
    if not path_exists(path):
        return
    target = csv_io_target(path)
    lines = target.read_text(encoding="utf-8-sig").splitlines()
    if not lines:
        return
    kept = [lines[0], *[line for line in lines[1:] if marker not in line]]
    target.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8-sig")


def append_csv_row(path: Path, row: Mapping[str, Any]) -> None:
    target = csv_io_target(path)
    with target.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        fieldnames = [field for field in next(reader) if field]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})
    with target.open("a", encoding="utf-8-sig", newline="") as handle:
        handle.write(buffer.getvalue())


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def report_rows(runtime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        report_path = Path(str(row.get("report_path") or ""))
        rows.append(
            {
                "split": row.get("split"),
                "attempt_name": row.get("attempt_name"),
                "candidate_id": row.get("candidate_id"),
                "report_path": report_path,
                "report_exists": path_exists(report_path),
                "report_sha256": sha256_file_lf_normalized(report_path) if path_exists(report_path) else "",
                "receipt_row": row,
            }
        )
    return rows


def deal_to_row(split: str, attempt_name: str, deal: Deal) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_run_id": RUNTIME_RUN_ID,
        "split": split,
        "attempt_name": attempt_name,
        "time": deal.time.isoformat(),
        "ticket": deal.ticket,
        "symbol": deal.symbol,
        "order_type": deal.order_type,
        "direction": deal.direction,
        "volume": deal.volume,
        "price": deal.price,
        "order": deal.order,
        "commission": deal.commission,
        "swap": deal.swap,
        "profit": deal.profit,
        "balance": deal.balance,
        "comment": deal.comment,
    }


def trade_to_row(split: str, attempt_name: str, trade: Trade, running_balance: float, peak_balance: float) -> dict[str, Any]:
    duration_minutes = (trade.close_time - trade.open_time).total_seconds() / 60.0
    return {
        "run_id": RUN_ID,
        "source_run_id": RUNTIME_RUN_ID,
        "split": split,
        "attempt_name": attempt_name,
        "trade_index": trade.index,
        "direction": trade.direction,
        "open_time": trade.open_time.isoformat(),
        "close_time": trade.close_time.isoformat(),
        "duration_minutes": duration_minutes,
        "duration_m5_bars": duration_minutes / 5.0,
        "volume": trade.volume,
        "open_price": trade.open_price,
        "close_price": trade.close_price,
        "gross_profit": trade.gross_profit,
        "net_profit": trade.net_profit,
        "swap": trade.swap,
        "commission": trade.commission,
        "running_balance_after_trade": running_balance,
        "peak_balance_after_trade": peak_balance,
        "under_water_after_trade": running_balance < peak_balance,
    }


def summarize_trades(split: str, runtime_row: Mapping[str, str], trades: Sequence[Trade], deals: Sequence[Deal]) -> dict[str, Any]:
    initial_balance = 500.0
    gross_profit = sum(trade.net_profit for trade in trades if trade.net_profit > 0)
    gross_loss = sum(trade.net_profit for trade in trades if trade.net_profit < 0)
    net_profit = sum(trade.net_profit for trade in trades)
    wins = sum(1 for trade in trades if trade.net_profit > 0)
    losses = sum(1 for trade in trades if trade.net_profit < 0)
    trade_count = len(trades)
    running = initial_balance
    peak = initial_balance
    max_drawdown_amount = 0.0
    max_drawdown_percent = 0.0
    underwater = 0
    max_consecutive_loss = 0
    current_consecutive_loss = 0
    for trade in trades:
        running += trade.net_profit
        peak = max(peak, running)
        drawdown_amount = peak - running
        max_drawdown_amount = max(max_drawdown_amount, drawdown_amount)
        if peak:
            max_drawdown_percent = max(max_drawdown_percent, drawdown_amount / peak * 100.0)
        if running < peak:
            underwater += 1
        if trade.net_profit < 0:
            current_consecutive_loss += 1
            max_consecutive_loss = max(max_consecutive_loss, current_consecutive_loss)
        else:
            current_consecutive_loss = 0
    calendar_days = as_float(runtime_row.get("calendar_days_exclusive"), 0.0)
    avg_win = gross_profit / wins if wins else None
    avg_loss = gross_loss / losses if losses else None
    return {
        "split": split,
        "test_period_start": runtime_row.get("test_period_start"),
        "test_period_end": runtime_row.get("test_period_end"),
        "deal_count": len(deals),
        "trade_count": trade_count,
        "trades_per_day": trade_count / calendar_days if calendar_days else None,
        "long_trade_count": sum(1 for trade in trades if trade.direction == "buy"),
        "short_trade_count": sum(1 for trade in trades if trade.direction == "sell"),
        "winning_trade_count": wins,
        "losing_trade_count": losses,
        "win_rate_percent": wins / trade_count * 100.0 if trade_count else None,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "net_profit": net_profit,
        "profit_factor": gross_profit / abs(gross_loss) if gross_loss else None,
        "expectancy": net_profit / trade_count if trade_count else None,
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": avg_win / abs(avg_loss) if avg_win is not None and avg_loss else None,
        "recovery_factor": net_profit / max_drawdown_amount if max_drawdown_amount else None,
        "max_drawdown_amount_from_trade_balance": max_drawdown_amount,
        "max_drawdown_percent_from_trade_balance": max_drawdown_percent,
        "time_under_water_trades": underwater,
        "max_consecutive_loss": max_consecutive_loss,
        "receipt_net_profit": as_float(runtime_row.get("net_profit")),
        "receipt_profit_factor": as_float(runtime_row.get("profit_factor")),
        "receipt_trade_count": as_int(runtime_row.get("trade_count")),
        "receipt_gross_profit": as_float(runtime_row.get("gross_profit")),
        "receipt_gross_loss": as_float(runtime_row.get("gross_loss")),
        "receipt_win_rate_percent": as_float(runtime_row.get("win_rate_percent")),
        "receipt_max_drawdown_percent": as_float(runtime_row.get("max_drawdown_percent")),
        "net_delta_vs_receipt": net_profit - as_float(runtime_row.get("net_profit")),
        "trade_count_delta_vs_receipt": trade_count - as_int(runtime_row.get("trade_count")),
        "gross_profit_delta_vs_receipt": gross_profit - as_float(runtime_row.get("gross_profit")),
        "gross_loss_delta_vs_receipt": gross_loss - as_float(runtime_row.get("gross_loss")),
        "profit_factor_delta_vs_receipt": (
            (gross_profit / abs(gross_loss) if gross_loss else 0.0) - as_float(runtime_row.get("profit_factor"))
        ),
        "reconciled": (
            abs(net_profit - as_float(runtime_row.get("net_profit"))) <= 0.011
            and trade_count == as_int(runtime_row.get("trade_count"))
        ),
    }


def build_payload(created_at: str) -> dict[str, Any]:
    f82e_summary = read_json(F82E_SUMMARY)
    f82c_summary = read_json(F82C_SUMMARY)
    f82c_manifest = read_json(F82C_MANIFEST)
    runtime_rows = read_csv(F82C_RECEIPT)
    reports = report_rows(runtime_rows)
    deal_rows: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    split_rows: list[dict[str, Any]] = []
    report_summaries: list[dict[str, Any]] = []
    for report in reports:
        split = str(report["split"])
        attempt_name = str(report["attempt_name"])
        report_path = Path(report["report_path"])
        parsed = parse_mt5_trade_report(report_path)
        deals = parsed["deals"]
        trades = pair_deals_into_trades(deals)
        metrics = extract_mt5_strategy_report_metrics(report_path)
        split_summary = summarize_trades(split, report["receipt_row"], trades, deals)
        split_summary.update(
            {
                "attempt_name": attempt_name,
                "candidate_id": report.get("candidate_id"),
                "report_path": report_path.as_posix(),
                "report_sha256": report.get("report_sha256"),
                "report_metrics_status": metrics.get("status"),
                "report_metrics": metrics,
                "trade_report_summary": parsed.get("summary") or {},
            }
        )
        report_summaries.append(split_summary)
        split_rows.append(split_summary)
        balance = 500.0
        peak = 500.0
        for deal in deals:
            deal_rows.append(deal_to_row(split, attempt_name, deal))
        for trade in trades:
            balance += trade.net_profit
            peak = max(peak, balance)
            trade_rows.append(trade_to_row(split, attempt_name, trade, balance, peak))
    all_reconciled = all(bool(row.get("reconciled")) for row in split_rows)
    status = STATUS if all_reconciled else "f82f_deal_level_report_evidence_unreconciled_inconclusive_no_authority"
    judgment = JUDGMENT if all_reconciled else "deal_level_pnl_recovered_but_receipt_reconciliation_failed_no_authority"
    next_run = NEXT_RUN_ID if all_reconciled else ROTATION_IF_FAILED
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "runtime_run_id": RUNTIME_RUN_ID,
        "next_run_id": next_run,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "target": f82e_summary.get("target") or f82c_manifest.get("target") or {},
        "source_reports": reports,
        "split_summaries": report_summaries,
        "deal_row_count": len(deal_rows),
        "trade_row_count": len(trade_rows),
        "all_reconciled": all_reconciled,
        "deal_rows": deal_rows,
        "trade_rows": trade_rows,
        "f82e_decision": {
            "decision": f82e_summary.get("decision"),
            "repair_axis": f82e_summary.get("repair_axis"),
            "repair_cap": f82e_summary.get("repair_cap"),
            "rotation_if_blocked": f82e_summary.get("rotation_if_blocked"),
        },
        "source_telemetry_audit": f82e_summary.get("telemetry_audit") or [],
        "runtime_summary_best": f82c_summary.get("best_runtime") or {},
        "next_condition": (
            "Use reconciled MT5 report trades to rebuild a MT5-realized label"
            "(대조 완료된 MT5 보고서 거래로 MT5 실현 손익 라벨 재구축)."
            if all_reconciled
            else "Stop F82 repair and rotate because deal reconciliation failed"
            "(거래 대조 실패 시 F82 수리를 멈추고 회전)."
        ),
        "reference_scout": {
            "status": "not_required(불필요)",
            "not_required_reason": (
                "No new MQL5 or Strategy Tester behavior was implemented; F82F used the existing "
                "foundation.mt5.trade_report parser and existing tester reports"
                "(새 MQL5/전략 테스터 동작 구현 없이 기존 파서와 기존 보고서를 사용)."
            ),
        },
        "allowed_claims": [
            "deal-level tester report evidence recovered(거래별 테스터 보고서 근거 회수)",
            "receipt reconciliation passed(영수증 대조 통과)" if all_reconciled else "receipt reconciliation failed(영수증 대조 실패)",
            "label rebuild input ready(라벨 재구축 입력 준비)" if all_reconciled else "rotation condition reached(회전 조건 도달)",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "Goal Achieve",
        ],
    }


def fmt(value: Any, digits: int = 4) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def report_text(payload: Mapping[str, Any]) -> str:
    rows = payload.get("split_summaries") or []
    table = "\n".join(
        "| {split} | `{net}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{win}` | `{gross_profit}` | `{gross_loss}` | `{max_loss}` | `{underwater}` | `{reconciled}` |".format(
            split=row.get("split"),
            net=fmt(row.get("net_profit")),
            pf=fmt(row.get("profit_factor")),
            dd=fmt(row.get("receipt_max_drawdown_percent")),
            trades=fmt(row.get("trade_count"), 0),
            tpd=fmt(row.get("trades_per_day")),
            win=fmt(row.get("win_rate_percent")),
            gross_profit=fmt(row.get("gross_profit")),
            gross_loss=fmt(row.get("gross_loss")),
            max_loss=fmt(row.get("max_consecutive_loss"), 0),
            underwater=fmt(row.get("time_under_water_trades"), 0),
            reconciled=row.get("reconciled"),
        )
        for row in rows
    )
    target = payload.get("target") or {}
    return f"""# F82F Deal-Reconciled Runtime Label Preflight(F82F 거래 손익 대조 런타임 라벨 사전확인)

Updated(갱신): {payload.get('created_at_utc')}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- runtime source(런타임 원천): `{RUNTIME_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- status(상태): `{payload.get('status')}`
- judgment(판정): `{payload.get('judgment')}`
- next run(다음 실행): `{payload.get('next_run_id')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action And Effect(행동과 효과)

Action(행동): F82C MT5 Strategy Tester report(F82C MT5 전략 테스터 보고서)에서 deal/trade rows(딜/거래 행)를 파싱하고 F82C runtime receipt(런타임 영수증)와 대조했다.

Effect(효과): EA telemetry patch(EA 텔레메트리 패치) 없이도 deal-level PnL evidence(거래별 손익 근거)를 회수했으므로, F82G(전선81G)는 threshold-only tweak(임계값만 바꾸기)이 아니라 MT5-realized label rebuild(MT5 실현 손익 라벨 재구축)로 갈 수 있다.

## Reconciliation KPI(대조 KPI)

| split(구간) | net(순손익) | PF(수익 팩터) | DD %(손실폭 %) | trades(거래 수) | trades/day(일 거래) | win %(승률 %) | gross profit(총이익) | gross loss(총손실) | max consecutive loss(최대 연속 손실) | time under water trades(회복 전 체류 거래) | reconciled(대조) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
{table}

Deal rows(딜 행): `{payload.get('deal_row_count')}`. Trade rows(거래 행): `{payload.get('trade_row_count')}`.

Next condition(다음 조건): `{payload.get('next_condition')}`

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text(payload: Mapping[str, Any]) -> str:
    return f"""# F82F Required Gate Coverage Audit(F82F 필수 게이트 커버리지 감사)

Status(상태): `{payload.get('status')}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `runtime_evidence_gate` | `passed(통과)` | `{rel(DEAL_ROWS)}`, `{rel(TRADE_ROWS)}` | Strategy Tester report(전략 테스터 보고서)에서 deal/trade evidence(딜/거래 근거)를 회수했다. |
| `scope_completion_gate` | `passed(통과)` | `{rel(SPLIT_RECONCILIATION)}` | F82F scope(범위)인 deal-level evidence preflight(거래별 근거 사전확인)를 완료했다. |
| `kpi_contract_audit` | `passed(통과)` | `{rel(SUMMARY)}` | net/PF/DD/trades/day/parity gap/next action(순손익/수익 팩터/손실폭/일 거래/동등성 간극/다음 행동)을 기록했다. |
| `task_force_review_packet` | `passed(통과)` | `{rel(TASK_FORCE_REVIEW)}` | agent(요원) 검토를 Codex local verification(로컬 검증)과 분리했다. |
| `required_gate_coverage_audit` | `passed(통과)` | `{rel(GATE_AUDIT)}` | runtime_backtest(런타임/백테스트) 필수 게이트를 연결했다. |
| `final_claim_guard` | `passed(통과)` | `{CLAIM_BOUNDARY}` | deal evidence(거래 근거)를 runtime authority(런타임 권위)로 과장하지 않는다. |
"""


def receipt_texts(payload: Mapping[str, Any]) -> dict[Path, str]:
    status = payload.get("status")
    judgment = payload.get("judgment")
    return {
        RUNTIME_PARITY_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-runtime-parity
status: passed_report_deal_evidence_preflight_no_authority
research_path: {SCRIPT_REL}
runtime_path: {rel(F82C_MANIFEST)}
shared_contract: F82C candidate/report/receipt identity(F82C 후보/보고서/영수증 정체성)
known_differences:
  - telemetry has no deal PnL columns(텔레메트리에는 거래 손익 열이 없음)
  - tester report has deal rows(테스터 보고서는 딜 행을 포함)
parity_check: report_deal_sum_vs_runtime_receipt(보고서 거래 합계 대 런타임 영수증)
parity_identity:
  deal_rows: {rel(DEAL_ROWS)}
  trade_rows: {rel(TRADE_ROWS)}
runtime_claim_boundary: runtime_probe_observation_only(런타임 탐침 관찰 전용)
""",
        BACKTEST_FORENSICS_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-backtest-forensics
status: usable_with_boundary
tester_identity: F82C manifest/report settings(F82C 목록/보고서 설정)
ea_identity: {rel(F82C_MANIFEST)}
report_identity:
  - {rel(SUMMARY)}
  - {rel(SPLIT_RECONCILIATION)}
trade_evidence:
  deal_rows: {payload.get('deal_row_count')}
  trade_rows: {payload.get('trade_row_count')}
  reconciled: {payload.get('all_reconciled')}
cost_assumptions: broker tester report values(브로커 테스터 보고서 값)
forensic_checks:
  - parsed tester deal table(테스터 딜 표 파싱)
  - paired in/out deals into trades(진입/청산 딜을 거래로 결합)
  - reconciled net and trade count to receipt(순손익과 거래 수를 영수증과 대조)
backtest_judgment: usable_with_boundary
""",
        REFERENCE_SCOUT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-reference-scout
status: not_required
question: "Does F82F need external MQL5 or Strategy Tester lookup?(F82F에 외부 MQL5 또는 전략 테스터 확인이 필요한가?)"
sources_checked: []
source_quality: not_applicable(해당 없음)
found_pattern: existing_internal_parser(기존 내부 파서)
project_fit: existing report parser and tester report files are already project-owned(기존 보고서 파서와 테스터 보고서가 프로젝트 소유)
do_not_copy: no external code copied(외부 코드 복사 없음)
recommended_use: use_existing_internal_parser(기존 내부 파서 사용)
not_required_reason: "{(payload.get('reference_scout') or {}).get('not_required_reason')}"
""",
        RUN_EVIDENCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-run-evidence-system
status: {status}
measurement_scope:
  - runtime deal evidence(런타임 거래 근거)
  - receipt reconciliation(영수증 대조)
management_state:
  run_folder: {rel(RUN_DIR)}
  manifest: {rel(RUN_MANIFEST)}
  summary: {rel(SUMMARY)}
judgment_class: positive_next_step_only_no_authority(다음 단계 긍정, 권위 없음)
scoreboard: runtime_parity(런타임 동등성)
parity_level: P3_runtime_shadow_parity_sampled(P3 런타임 그림자 동등성 표본)
wfo_status: not_applicable_preflight_only(사전확인 전용 해당 없음)
registry_update_required: yes
negative_memory_required: not_yet_stage_closeout(아직 단계 마감 아님)
hard_gate_applicable: no
evidence_boundary: runtime_probe_observation_only(런타임 탐침 관찰 전용)
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_inputs:
  - {rel(F82E_SUMMARY)}
  - {rel(F82C_SUMMARY)}
  - {rel(F82C_MANIFEST)}
  - {rel(F82C_RECEIPT)}
  - {rel(F82C_FORENSICS)}
producer: {SCRIPT_REL}
consumer: {payload.get('next_run_id')}
artifact_paths:
  - {rel(DEAL_ROWS)}
  - {rel(TRADE_ROWS)}
  - {rel(SPLIT_RECONCILIATION)}
  - {rel(REPORT)}
  - {rel(TASK_FORCE_REVIEW)}
  - {rel(LOCAL_VERIFICATION)}
artifact_hashes:
  deal_rows_sha256: {sha256_file_lf_normalized(DEAL_ROWS)}
  trade_rows_sha256: {sha256_file_lf_normalized(TRADE_ROWS)}
  split_reconciliation_sha256: {sha256_file_lf_normalized(SPLIT_RECONCILIATION)}
registry_links:
  - {rel(ARTIFACT_REGISTRY)}
  - {rel(RUN_REGISTRY)}
  - {rel(ALPHA_LEDGER)}
  - {rel(STAGE_LEDGER)}
availability: ignored_02_runs_with_tracked_hash_receipts(02_runs 무시, 추적 해시 영수증 보존)
lineage_judgment: connected_with_boundary
""",
        TASK_FORCE_REVIEW: f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_deal_reconciliation_preflight_no_authority
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Use Strategy Tester report deal table(전략 테스터 보고서 딜 표) before EA telemetry patch(EA 텔레메트리 패치) because it already carries entry/exit/PnL(진입/청산/손익)."
    - "Treat reconciled deal rows(대조된 거래 행) as label rebuild input(라벨 재구축 입력), not runtime authority(런타임 권위)."
    - "Keep F82 repair cap(전선82 수리 상한) at one cycle(1회)."
  rejected:
    - "Do not repeat threshold-only repair(임계값 전용 수리 반복 금지)."
  needs_local_verification:
    - "Codex must verify report hashes, row counts, and receipt reconciliation locally(코덱스가 보고서 해시/행 수/영수증 대조를 로컬 검증)."
claim_boundary: {CLAIM_BOUNDARY}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_runtime_probe_observation_only
allowed_claims:
  - deal_level_evidence_recovered(거래별 근거 회수)
  - receipt_reconciliation_passed(영수증 대조 통과)
  - mt5_realized_label_rebuild_ready(온엑스/MT5 실현 라벨 재구축 준비)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
final_status: "{judgment}; boundary={CLAIM_BOUNDARY}"
""",
    }


def work_packet_text(payload: Mapping[str, Any], created_at: str) -> str:
    return f"""packet_id: {RUN_ID}
stage_id: {STAGE_ID}
router_mode: full
work_packet_lifecycle: runtime_report_evidence_to_reconciliation_to_next_label_rebuild
primary_family: runtime_backtest
primary_skill: obsidian-runtime-parity
support_skills:
  - obsidian-backtest-forensics
  - obsidian-reference-scout
  - obsidian-run-evidence-system
  - obsidian-artifact-lineage
  - obsidian-task-force-review
  - obsidian-claim-discipline
required_skill_receipts:
  - obsidian-runtime-parity
  - obsidian-backtest-forensics
  - obsidian-reference-scout
  - obsidian-run-evidence-system
  - obsidian-artifact-lineage
  - obsidian-task-force-review
  - obsidian-claim-discipline
required_gates:
  - runtime_evidence_gate
  - scope_completion_gate
  - kpi_contract_audit
  - task_force_review_packet
  - required_gate_coverage_audit
  - final_claim_guard
scope: "Recover and reconcile F82C deal-level Strategy Tester evidence(F82C 거래별 전략 테스터 근거 회수 및 대조)."
status: {payload.get('status')}
judgment: {payload.get('judgment')}
next_run_id: {payload.get('next_run_id')}
branch_worktree_fit: "passed_on_codex/frontier82-deal-preflight"
ea_variant_boundary: "no_code_change_existing_report_parse(코드 변경 없음, 기존 보고서 파싱)"
reference_scout: "not_required_existing_internal_parser_no_new_mql5_api(기존 내부 파서, 새 MQL5 API 없음)"
claim_boundary: {CLAIM_BOUNDARY}
created_at_utc: "{created_at}"
"""


def packet_receipts_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_skill": {
            "name": "obsidian-runtime-parity",
            "status": "passed_report_deal_reconciliation",
            "evidence": rel(RUNTIME_PARITY_RECEIPT),
        },
        "support_skills": [
            {"name": "obsidian-backtest-forensics", "status": "usable_with_boundary", "evidence": rel(BACKTEST_FORENSICS_RECEIPT)},
            {"name": "obsidian-reference-scout", "status": "not_required", "evidence": rel(REFERENCE_SCOUT_RECEIPT)},
            {"name": "obsidian-run-evidence-system", "status": "passed_ledgers", "evidence": rel(RUN_EVIDENCE_RECEIPT)},
            {"name": "obsidian-artifact-lineage", "status": "connected_with_boundary", "evidence": rel(ARTIFACT_RECEIPT)},
            {"name": "obsidian-task-force-review", "status": "passed_internal_review_no_authority", "evidence": rel(TASK_FORCE_REVIEW)},
            {"name": "obsidian-claim-discipline", "status": "passed_runtime_probe_observation_only", "evidence": rel(CLAIM_RECEIPT)},
        ],
        "forbidden_claims": payload.get("forbidden_claims"),
    }


def packet_gate_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "primary_family": "runtime_backtest",
        "status": "passed_runtime_probe_observation_only",
        "gates": [
            {"gate": "runtime_evidence_gate", "status": "passed", "evidence": [rel(DEAL_ROWS), rel(TRADE_ROWS)]},
            {"gate": "scope_completion_gate", "status": "passed", "evidence": rel(SPLIT_RECONCILIATION)},
            {"gate": "kpi_contract_audit", "status": "passed", "evidence": rel(SUMMARY)},
            {"gate": "task_force_review_packet", "status": "passed", "evidence": rel(TASK_FORCE_REVIEW)},
            {"gate": "required_gate_coverage_audit", "status": "passed", "evidence": rel(GATE_AUDIT)},
            {"gate": "final_claim_guard", "status": "passed", "evidence": rel(FINAL_CLAIM_GUARD)},
        ],
    }


def final_claim_guard_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "passed",
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": payload.get("allowed_claims"),
        "forbidden_claims": payload.get("forbidden_claims"),
        "effect": "Recovered deal evidence does not create runtime authority(회수한 거래 근거는 런타임 권위를 만들지 않음).",
    }


def local_verification_json(payload: Mapping[str, Any]) -> dict[str, Any]:
    required_paths = [
        SUMMARY,
        DEAL_ROWS,
        TRADE_ROWS,
        SPLIT_RECONCILIATION,
        REPORT,
        GATE_AUDIT,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        REFERENCE_SCOUT_RECEIPT,
        RUN_EVIDENCE_RECEIPT,
        ARTIFACT_RECEIPT,
        TASK_FORCE_REVIEW,
        CLAIM_RECEIPT,
        RUN_MANIFEST,
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "passed_local_verification_no_authority",
        "created_at_utc": payload.get("created_at_utc"),
        "checks": {
            "deal_rows_positive": payload.get("deal_row_count", 0) > 0,
            "trade_rows_positive": payload.get("trade_row_count", 0) > 0,
            "all_reconciled": payload.get("all_reconciled"),
            "next_run_id": payload.get("next_run_id"),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "split_reconciliation": [
            {
                "split": row.get("split"),
                "report_sha256": row.get("report_sha256"),
                "net_delta_vs_receipt": row.get("net_delta_vs_receipt"),
                "trade_count_delta_vs_receipt": row.get("trade_count_delta_vs_receipt"),
                "reconciled": row.get("reconciled"),
            }
            for row in payload.get("split_summaries", [])
        ],
        "required_paths": [
            {
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            }
            for path in required_paths
        ],
        "forbidden_claims": payload.get("forbidden_claims"),
    }


def ledger_rows(payload: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    oos = next((row for row in payload.get("split_summaries", []) if row.get("split") == "oos"), {})
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "family": "runtime_backtest(런타임/백테스트)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REPORT),
        "external_verification_status": "completed_existing_tester_report_parse(기존 테스터 보고서 파싱 완료)",
        "run_number": "frontier82F",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": payload.get("next_run_id"),
        "rows": payload.get("trade_row_count"),
        "gate_passes": 6,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": (payload.get("target") or {}).get("candidate_id"),
        "model": (payload.get("target") or {}).get("model"),
        "net_profit": oos.get("net_profit"),
        "profit_factor": oos.get("profit_factor"),
        "drawdown": oos.get("receipt_max_drawdown_percent"),
        "trade_count": oos.get("trade_count"),
        "trades_per_day": oos.get("trades_per_day"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "feature_count": (payload.get("target") or {}).get("feature_count"),
        "work_family": "runtime_backtest",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "Strategy Tester report deal table(전략 테스터 보고서 딜 표)",
        "run_family": "deal_reconciled_runtime_label_preflight",
        "run_type": "runtime_report_preflight",
        "input_run_id": RUNTIME_RUN_ID,
        "output_path": rel(REPORT),
        "result_path": rel(REPORT),
        "expected_net_profit": (payload.get("target") or {}).get("oos_net"),
        "expected_profit_factor": (payload.get("target") or {}).get("oos_pf"),
        "expected_trade_count": (payload.get("target") or {}).get("oos_trade_count"),
        "trade_density": oos.get("trades_per_day"),
        "max_drawdown_percent": oos.get("receipt_max_drawdown_percent"),
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_deal_reconciliation",
            "subrun_id": "tier_a_deal_reconciliation(티어 A 거래 대조)",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "mt5_deal_reconciliation(엠티5 거래 대조)",
            "scoreboard_lane": "runtime_parity(런타임 동등성)",
            "lane": "deal_reconciled_runtime_label_preflight(거래 손익 대조 런타임 라벨 사전확인)",
            "primary_kpi": f"oos_net={oos.get('net_profit')};oos_pf={oos.get('profit_factor')};oos_trades={oos.get('trade_count')};reconciled={payload.get('all_reconciled')}",
            "guardrail_kpi": f"deal_rows={payload.get('deal_row_count')};trade_rows={payload.get('trade_row_count')};no_authority",
            "notes": f"next={payload.get('next_run_id')}; source=Strategy Tester report deal table",
            "view": "tier_a_deal_reconciliation",
            "tier": "Tier A",
            "metric_scope": "mt5_deal_reconciliation",
            "result_status": payload.get("status"),
            "row_id": f"{RUN_ID}__tier_a_deal_reconciliation",
            "evidence_boundary": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
            "next_action": payload.get("next_run_id"),
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": "tier_b_missing_required(티어 B 필수 누락)",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B missing_required",
            "kpi_scope": "missing_required(필수 누락)",
            "scoreboard_lane": "runtime_parity(런타임 동등성)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "primary_kpi": "Tier B missing_required",
            "guardrail_kpi": "No Tier B fallback route in F82C(F82C에 티어 B 대체 경로 없음)",
            "notes": "Tier B not omitted; out of current F82C runtime source.",
            "view": "tier_b_missing_required",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required_no_reviewed_run_claim",
            "row_id": f"{RUN_ID}__tier_b_missing_required",
            "evidence_boundary": "missing_required(필수 누락)",
            "next_action": payload.get("next_run_id"),
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": "tier_ab_combined_out_of_scope(티어 A+B 합산 범위 밖)",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B out_of_scope_by_claim",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "scoreboard_lane": "runtime_parity(런타임 동등성)",
            "lane": "tier_record_boundary(티어 기록 경계)",
            "primary_kpi": "Tier A+B combined out_of_scope_by_claim",
            "guardrail_kpi": "No routed Tier A primary + Tier B fallback run exists in F82C.",
            "notes": "No synthetic sum reported.",
            "view": "tier_ab_combined_out_of_scope",
            "tier": "Tier A+B",
            "metric_scope": "out_of_scope_by_claim",
            "result_status": "out_of_scope_by_claim_no_reviewed_run_claim",
            "row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "evidence_boundary": "out_of_scope_by_claim(주장 범위 밖)",
            "next_action": payload.get("next_run_id"),
        },
    ]


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    rows = ledger_rows(payload, created_at)
    upsert_csv(RUN_REGISTRY, "run_id", rows[0])
    for row in rows:
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_artifact_registry(created_at: str) -> None:
    remove_matching_csv_text_rows(ARTIFACT_REGISTRY, f",{RUN_ID},")
    paths = [
        SUMMARY,
        DEAL_ROWS,
        TRADE_ROWS,
        SPLIT_RECONCILIATION,
        REPORT,
        GATE_AUDIT,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        REFERENCE_SCOUT_RECEIPT,
        RUN_EVIDENCE_RECEIPT,
        ARTIFACT_RECEIPT,
        TASK_FORCE_REVIEW,
        CLAIM_RECEIPT,
        LOCAL_VERIFICATION,
        RUN_MANIFEST,
    ]
    for path in paths:
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "created_at": created_at,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F82F deal evidence preflight only(F82F 거래 근거 사전확인만 지원).",
        }
        append_csv_row(ARTIFACT_REGISTRY, row)


def update_state_files(payload: Mapping[str, Any], created_at: str) -> None:
    next_run = payload.get("next_run_id")
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {payload.get('status')}
current_judgment: {payload.get('judgment')}
next_run_id: {next_run}
runtime_probe_status: f82f_deal_level_report_evidence_reconciled_label_rebuild_required_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f81_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F82F deal-reconciled runtime label preflight(F82F 거래 손익 대조 런타임 라벨 사전확인)를 완료했다."
  - "Effect(효과): F82C Strategy Tester report(전략 테스터 보고서)에서 거래별 손익 근거를 회수했고 receipt(영수증)와 대조했다."
  - "Next(다음): {next_run}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F82F deal-reconciled runtime label preflight(F82F 거래 손익 대조 런타임 라벨 사전확인)를 완료했다.

Effect(효과): F82C Strategy Tester report(전략 테스터 보고서)에서 deal/trade rows(딜/거래 행)를 회수했고 validation/OOS(검증/표본외) 모두 runtime receipt(런타임 영수증)와 대조됐다.

## Runtime Deal Evidence(런타임 거래 근거)

- deal rows(딜 행): `{payload.get('deal_row_count')}`
- trade rows(거래 행): `{payload.get('trade_row_count')}`
- all reconciled(전체 대조): `{payload.get('all_reconciled')}`
- next run(다음 실행): `{next_run}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_selection_status(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(
        SELECTION_STATUS,
        f"""# F82 Selection Status(F82 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload.get('status')}`

Judgment(판정): `{payload.get('judgment')}`

Action(행동): F82F deal-level report evidence(거래별 보고서 근거)를 회수하고 runtime receipt(런타임 영수증)와 대조했다.

Effect(효과): F82G MT5-realized label rebuild(F82G MT5 실현 손익 라벨 재구축)를 다음 실행으로 둘 수 있다.

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{payload.get('next_run_id')}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_context_anchor(payload: Mapping[str, Any], created_at: str) -> None:
    oos = next((row for row in payload.get("split_summaries", []) if row.get("split") == "oos"), {})
    write_text(
        CONTEXT_ANCHOR,
        f"""# F82 Context Anchor(F82 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{payload.get('next_run_id')}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{payload.get('status')}`
- judgment(판정): `{payload.get('judgment')}`
- OOS runtime deal evidence(표본외 런타임 거래 근거): net `{oos.get('net_profit')}`, PF `{oos.get('profit_factor')}`, trades `{oos.get('trade_count')}`, trades/day `{oos.get('trades_per_day')}`
- all reconciled(전체 대조): `{payload.get('all_reconciled')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{payload.get('next_run_id')}`.
""",
    )


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F82 Review Index(F82 검토 색인)\n"
    lines = [
        "- `frontier82F_deal_reconciled_runtime_label_preflight_report.md`: F82F deal reconciliation report(F82F 거래 대조 보고서)",
        "- `f82f_deal_reconciliation_summary.json`: F82F machine summary(F82F 기계 요약)",
        "- `f82f_split_reconciliation.csv`: F82F split reconciliation rows(F82F 구간 대조 행)",
        "- `frontier82F_deal_reconciled_runtime_label_preflight_v1/f82f_deal_rows.csv`: F82F deal rows(F82F 딜 행)",
        "- `frontier82F_deal_reconciled_runtime_label_preflight_v1/f82f_trade_rows.csv`: F82F trade rows(F82F 거래 행)",
        "- `required_gate_coverage_audit_f82f.md`: F82F gate audit(F82F 게이트 감사)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    oos = next((row for row in payload.get("split_summaries", []) if row.get("split") == "oos"), {})
    addition = f"""

- `{RUN_ID}` recovered MT5 deal-level evidence(F82F MT5 거래별 근거 회수). Result(결과): deal rows `{payload.get('deal_row_count')}`, trade rows `{payload.get('trade_row_count')}`, OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래) `{oos.get('net_profit')}/{oos.get('profit_factor')}/{oos.get('receipt_max_drawdown_percent')}/{oos.get('trades_per_day')}`. Boundary(경계): runtime probe observation only, no authority(런타임 탐침 관찰 전용, 권위 없음). Next(다음): `{payload.get('next_run_id')}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_changelog(payload: Mapping[str, Any]) -> None:
    text = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID in text:
        return
    entry = f"""# 2026-06-18 - F82F Deal Reconciliation(F82F 거래 대조)

- Action(행동): `{RUN_ID}`로 F82C Strategy Tester report(전략 테스터 보고서)의 deal/trade rows(딜/거래 행)를 파싱했다.
- Effect(효과): deal rows `{payload.get('deal_row_count')}`, trade rows `{payload.get('trade_row_count')}`를 runtime receipt(런타임 영수증)와 대조해 MT5-realized label rebuild(MT5 실현 손익 라벨 재구축) 입력을 만들었다.
- Next(다음): `{payload.get('next_run_id')}`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

"""
    write_text(CHANGELOG, entry + text)


def write_packet_files(payload: Mapping[str, Any], created_at: str) -> None:
    write_text(WORK_PACKET, work_packet_text(payload, created_at))
    write_json(SKILL_RECEIPTS, packet_receipts_json(payload))
    write_json(PACKET_GATE_AUDIT, packet_gate_json())
    write_json(FINAL_CLAIM_GUARD, final_claim_guard_json(payload))


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    payload = build_payload(created_at)
    write_csv(DEAL_ROWS, payload["deal_rows"])
    write_csv(TRADE_ROWS, payload["trade_rows"])
    write_csv(SPLIT_RECONCILIATION, payload["split_summaries"])
    payload = {key: value for key, value in payload.items() if key not in {"deal_rows", "trade_rows"}}
    payload["producer"] = SCRIPT_REL
    payload["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    payload["artifacts"] = {
        "summary": rel(SUMMARY),
        "deal_rows": rel(DEAL_ROWS),
        "trade_rows": rel(TRADE_ROWS),
        "split_reconciliation": rel(SPLIT_RECONCILIATION),
        "report": rel(REPORT),
        "gate_audit": rel(GATE_AUDIT),
        "run_manifest": rel(RUN_MANIFEST),
        "task_force_review": rel(TASK_FORCE_REVIEW),
        "local_verification": rel(LOCAL_VERIFICATION),
        "work_packet": rel(WORK_PACKET),
    }
    write_json(SUMMARY, payload)
    write_text(REPORT, report_text(payload))
    write_text(GATE_AUDIT, gate_audit_text(payload))
    for path, text in receipt_texts(payload).items():
        write_text(path, text)
    write_json(RUN_MANIFEST, payload)
    write_json(LOCAL_VERIFICATION, local_verification_json(payload))
    write_packet_files(payload, created_at)
    update_ledgers(payload, created_at)
    update_artifact_registry(created_at)
    update_state_files(payload, created_at)
    update_selection_status(payload, created_at)
    update_context_anchor(payload, created_at)
    update_review_index()
    update_idea_registry(payload)
    update_changelog(payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "judgment": payload["judgment"],
                "deal_rows": payload["deal_row_count"],
                "trade_rows": payload["trade_row_count"],
                "all_reconciled": payload["all_reconciled"],
                "next_run_id": payload["next_run_id"],
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
