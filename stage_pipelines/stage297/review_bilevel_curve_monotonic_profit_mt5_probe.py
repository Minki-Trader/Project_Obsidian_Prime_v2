from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402


STAGE_ID = "297_onnx_candidate_campaign__bilevel_curve_monotonic_profit_rebuild"
NEXT_STAGE_ID = "298_onnx_candidate_campaign__profit_scale_edge_amplification_rebuild"
RUN_ID = "run297C_review_bilevel_curve_monotonic_profit_mt5_probe_v1"
RUN_NUMBER = "run297C"
SOURCE_RUN_ID = "run297B_bilevel_curve_monotonic_profit_mt5_probe_v1"
PARENT_RUN_ID = "run297A_design_bilevel_curve_monotonic_profit_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN297A = STAGE_ROOT / "02_runs" / "run297A"
RUN297B = STAGE_ROOT / "02_runs" / "run297B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC = NEXT_STAGE_ROOT / "00_spec"
NEXT_REVIEWS = NEXT_STAGE_ROOT / "03_reviews"
NEXT_SELECTED = NEXT_STAGE_ROOT / "04_selected"

SOURCE_EXECUTION = RUN297B / "execution_result.json"
SOURCE_KPI = RUN297B / "mt5_kpi_summary.csv"
SOURCE_SCOUT = RUN297A / "model_scout_scoreboard.csv"
PRODUCER = Path("stage_pipelines/stage297/review_bilevel_curve_monotonic_profit_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "bilevel_curve_monotonic_profit_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage298_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run297C_bilevel_curve_monotonic_profit_review_stage298_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage297_bilevel_curve_monotonic_profit_review_stage298_open.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes")
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


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def read_text(path: Path) -> str:
    return ledger.io_path(path).read_text(encoding="utf-8-sig") if ledger.path_exists(path) else ""


def write_text(path: Path, text: str) -> None:
    ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ledger.io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    ledger.write_csv_rows(path, columns, rows)


def upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    ledger.upsert_csv_rows(path, columns, rows, key=key)


def parse_date(text: str) -> date:
    return date.fromisoformat(str(text).replace(".", "-"))


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        text = str(value).replace(",", "").strip()
        if not text:
            return default
        return float(text)
    except Exception:
        return default


def feature_trading_days(attempt: Mapping[str, Any]) -> int:
    feature_path = ""
    set_path = attempt.get("set", {}).get("path")
    if set_path and ledger.path_exists(Path(str(set_path))):
        text = ledger.io_path(Path(str(set_path))).read_text(encoding="utf-8-sig")
        for line in text.splitlines():
            if line.startswith("InpFeatureCsvPath="):
                feature_path = line.split("=", 1)[1].strip()
                break
    if not feature_path:
        feature_path = str(attempt.get("feature_path", "") or attempt.get("feature_file", ""))
    local = RUN297B / "features" / Path(feature_path).name
    if not ledger.path_exists(local) and feature_path.startswith("Project_Obsidian_Prime_v2/"):
        local = ROOT / feature_path.replace("Project_Obsidian_Prime_v2/", "")
    if not ledger.path_exists(local):
        local = Path(feature_path)
    dates: set[str] = set()
    with ledger.io_path(local).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            bar_time = row.get("bar_time_server") or row.get("timestamp_utc") or ""
            if bar_time:
                dates.add(str(bar_time)[:10].replace(".", "-"))
    return len(dates)


def session_label(ts: pd.Timestamp) -> str:
    hour = int(ts.hour)
    if 16 <= hour <= 17:
        return "cash_open_proxy(현금장 개장 대리)"
    if 18 <= hour <= 20:
        return "cash_mid_proxy(현금장 중반 대리)"
    if 21 <= hour <= 23:
        return "cash_late_proxy(현금장 후반 대리)"
    return "outside_cash_proxy(현금장 외부 대리)"


def parse_out_deals(report_path: Path) -> list[dict[str, Any]]:
    tables = pd.read_html(str(ledger.io_path(report_path)), encoding="utf-16")
    if len(tables) < 2:
        return []
    table = tables[1]
    start_index = None
    for index, row in table.iterrows():
        values = [str(value) for value in row.values]
        if values[:6] == ["시간", "거래", "통화", "종류", "방향", "거래량"]:
            start_index = index + 1
            break
    if start_index is None:
        return []
    deals: list[dict[str, Any]] = []
    for _, row in table.iloc[start_index:].iterrows():
        raw_time = row.iloc[0]
        if pd.isna(raw_time):
            continue
        kind = str(row.iloc[3]).strip()
        direction = str(row.iloc[4]).strip()
        if kind == "balance":
            continue
        if direction != "out":
            continue
        ts = pd.to_datetime(str(raw_time), errors="coerce")
        if pd.isna(ts):
            continue
        profit = number(row.iloc[10])
        balance = number(row.iloc[11])
        deals.append(
            {
                "time": ts,
                "month": ts.strftime("%Y-%m"),
                "session": session_label(ts),
                "profit": profit,
                "balance": balance,
            }
        )
    return deals


def curve_stats(deals: Sequence[Mapping[str, Any]], net_profit: float) -> dict[str, Any]:
    profits = [float(item["profit"]) for item in deals]
    balances = [float(item["balance"]) for item in deals]
    if not profits:
        return {
            "deal_count": 0,
            "worst_month_net": 0.0,
            "positive_month_share": 0.0,
            "worst_session_net": 0.0,
            "worst_rolling_20_net": 0.0,
            "worst_rolling_50_net": 0.0,
            "max_local_drawdown": 0.0,
            "max_underwater_trades": 0,
            "curve_pocket_gate": "failed",
        }
    monthly = defaultdict(float)
    session = defaultdict(float)
    for item in deals:
        monthly[str(item["month"])] += float(item["profit"])
        session[str(item["session"])] += float(item["profit"])
    worst_month = min(monthly.values()) if monthly else 0.0
    positive_month_share = sum(1 for value in monthly.values() if value > 0) / len(monthly) if monthly else 0.0
    worst_session = min(session.values()) if session else 0.0

    def worst_rolling(window: int) -> float:
        if len(profits) < window:
            return sum(profits)
        return min(sum(profits[index : index + window]) for index in range(len(profits) - window + 1))

    peak = balances[0]
    max_dd = 0.0
    underwater = 0
    max_underwater = 0
    for balance in balances:
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            max_underwater = max(max_underwater, underwater)
            max_dd = max(max_dd, peak - balance)
    worst20 = worst_rolling(20)
    worst50 = worst_rolling(50)
    curve_gate = "passed"
    if net_profit <= 0:
        curve_gate = "failed"
    if max_dd > max(25.0, net_profit * 0.35):
        curve_gate = "failed"
    if worst20 < -20.0 or worst50 < -35.0:
        curve_gate = "failed"
    if positive_month_share < 0.60:
        curve_gate = "failed"
    return {
        "deal_count": len(deals),
        "worst_month_net": worst_month,
        "positive_month_share": positive_month_share,
        "worst_session_net": worst_session,
        "worst_rolling_20_net": worst20,
        "worst_rolling_50_net": worst50,
        "max_local_drawdown": max_dd,
        "max_underwater_trades": max_underwater,
        "curve_pocket_gate": curve_gate,
    }


def load_actual_routed_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    execution = json.loads(ledger.io_path(SOURCE_EXECUTION).read_text(encoding="utf-8-sig"))
    attempts = {item.get("attempt_name"): item for item in execution.get("attempts", [])}
    scout_rows = {row["materialized_branch_id"]: row for row in ledger.read_csv_rows(SOURCE_SCOUT)}
    rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source_row in csv.DictReader(handle):
            if source_row.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source_row["metrics"])
            report = ast.literal_eval(source_row["report"])
            attempt_name = report.get("attempt_name")
            attempt = attempts.get(attempt_name, {})
            materialized_id = str(attempt.get("stage297_branch_id") or attempt.get("materialized_branch_id") or "")
            package_id = str(attempt.get("package_id") or scout_rows.get(materialized_id, {}).get("package_id") or "")
            tester = attempt.get("ini", {}).get("tester", {})
            from_date = tester.get("FromDate")
            to_date = tester.get("ToDate")
            calendar_days = (parse_date(to_date) - parse_date(from_date)).days + 1 if from_date and to_date else 0
            trading_days = feature_trading_days(attempt)
            trades = int(number(metrics.get("trade_count")))
            net_profit = number(metrics.get("net_profit"))
            report_path = Path(str(metrics.get("report_path")))
            deals = parse_out_deals(report_path)
            curve = curve_stats(deals, net_profit)
            row = {
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "split": source_row.get("split", ""),
                "net_profit": net_profit,
                "profit_factor": number(metrics.get("profit_factor")),
                "trade_count": trades,
                "trades_per_trading_day": trades / trading_days if trading_days else 0.0,
                "trades_per_calendar_day": trades / calendar_days if calendar_days else 0.0,
                "calendar_days": calendar_days,
                "trading_days": trading_days,
                "max_drawdown_amount": number(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount")),
                "max_drawdown_percent": number(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent")),
                "recovery_factor": number(metrics.get("recovery_factor")),
                "expectancy": number(metrics.get("expectancy")),
                "win_rate_percent": number(metrics.get("win_rate_percent")),
                "report_path": report_path.as_posix(),
                **curve,
            }
            rows.append(row)
            quality_rows.append(row)
    return rows, quality_rows, scout_rows


def build_scoreboard(rows: Sequence[Mapping[str, Any]], scout_rows: Mapping[str, Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_candidate[str(row["materialized_branch_id"])][str(row["split"])] = row
    scoreboard: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for candidate_id, split_rows in sorted(by_candidate.items()):
        val = split_rows.get("validation_is", {})
        oos = split_rows.get("oos", {})
        scout = scout_rows.get(candidate_id, {})
        val_net = number(val.get("net_profit"))
        oos_net = number(oos.get("net_profit"))
        combined = val_net + oos_net
        val_tpd = number(val.get("trades_per_trading_day"))
        oos_tpd = number(oos.get("trades_per_trading_day"))
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 700 and number(oos.get("trade_count")) >= 500 else "failed"
        density_gate = "passed" if 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0 else "failed"
        profit_scale_gate = "passed" if val_net >= 300.0 and oos_net >= 300.0 and combined >= 800.0 else "failed"
        efficiency_gate = "passed"
        if number(val.get("profit_factor")) < 1.12 or number(oos.get("profit_factor")) < 1.12:
            efficiency_gate = "failed"
        if number(val.get("recovery_factor")) < 1.0 or number(oos.get("recovery_factor")) < 1.0:
            efficiency_gate = "failed"
        if number(val.get("expectancy")) < 0.10 or number(oos.get("expectancy")) < 0.10:
            efficiency_gate = "failed"
        curve_gate = "passed" if val.get("curve_pocket_gate") == "passed" and oos.get("curve_pocket_gate") == "passed" else "failed"
        selected = (
            min_trade_gate == "passed"
            and density_gate == "passed"
            and profit_scale_gate == "passed"
            and efficiency_gate == "passed"
            and curve_gate == "passed"
        )
        row = {
            "materialized_branch_id": candidate_id,
            "package_id": val.get("package_id") or oos.get("package_id") or scout.get("package_id", ""),
            "validation_net_profit": val_net,
            "validation_pf": number(val.get("profit_factor")),
            "validation_trades": int(number(val.get("trade_count"))),
            "validation_trades_per_trading_day": val_tpd,
            "validation_recovery": number(val.get("recovery_factor")),
            "validation_expectancy": number(val.get("expectancy")),
            "validation_max_dd": number(val.get("max_drawdown_amount")),
            "validation_worst_month_net": number(val.get("worst_month_net")),
            "validation_worst_rolling_20_net": number(val.get("worst_rolling_20_net")),
            "validation_max_local_drawdown": number(val.get("max_local_drawdown")),
            "oos_net_profit": oos_net,
            "oos_pf": number(oos.get("profit_factor")),
            "oos_trades": int(number(oos.get("trade_count"))),
            "oos_trades_per_trading_day": oos_tpd,
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd": number(oos.get("max_drawdown_amount")),
            "oos_worst_month_net": number(oos.get("worst_month_net")),
            "oos_worst_rolling_20_net": number(oos.get("worst_rolling_20_net")),
            "oos_max_local_drawdown": number(oos.get("max_local_drawdown")),
            "combined_net_profit": combined,
            "minimum_trade_gate": min_trade_gate,
            "density_4_10_trading_day_gate": density_gate,
            "profit_scale_gate": profit_scale_gate,
            "efficiency_gate": efficiency_gate,
            "curve_pocket_gate": curve_gate,
            "selected_candidate": "yes" if selected else "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        scoreboard.append(row)
        if not selected:
            reasons = [
                name
                for name, value in (
                    ("minimum_trade_gate", min_trade_gate),
                    ("density_4_10_trading_day_gate", density_gate),
                    ("profit_scale_gate", profit_scale_gate),
                    ("efficiency_gate", efficiency_gate),
                    ("curve_pocket_gate", curve_gate),
                )
                if value != "passed"
            ]
            failure_rows.append(
                {
                    "failure_id": f"{candidate_id}_stage297_negative",
                    "materialized_branch_id": candidate_id,
                    "package_id": row["package_id"],
                    "failed_boundary": ",".join(reasons),
                    "why_failed": "actual MT5 routed total(실제 MT5 라우팅 전체)에서 순수익 규모, 효율, 확대 곡선 포켓 조건이 동시에 충족되지 않았다.",
                    "salvage_value": "4-10 trades/day(일 4-10거래) 밀도는 유지됐으므로 Stage298(298단계)에서 수익 단위 확대와 손실 포켓 억제를 새 논제로 사용한다.",
                    "reopen_condition": "validation/OOS(검증/표본외) 각각 net profit(순수익) 300 이상, combined(합산) 800 이상, OOS PF(표본외 수익 팩터) 1.12 이상, 깊은 rolling pocket(구간 포켓) 없음.",
                    "do_not_repeat": "Stage297의 robust bucket(강건 구간) agree/soft flip/veto 조합을 같은 임계값만 바꿔 반복하지 않는다.",
                    "claim_boundary": BOUNDARY,
                }
            )
    return scoreboard, failure_rows


def attribution_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    for row in rows:
        report_path = Path(str(row["report_path"]))
        deals = parse_out_deals(report_path)
        monthly = defaultdict(lambda: {"profit": 0.0, "trades": 0})
        sessions = defaultdict(lambda: {"profit": 0.0, "trades": 0})
        for deal in deals:
            monthly[str(deal["month"])]["profit"] += float(deal["profit"])
            monthly[str(deal["month"])]["trades"] += 1
            sessions[str(deal["session"])]["profit"] += float(deal["profit"])
            sessions[str(deal["session"])]["trades"] += 1
        for month, data in sorted(monthly.items()):
            monthly_rows.append(
                {
                    "materialized_branch_id": row["materialized_branch_id"],
                    "package_id": row["package_id"],
                    "split": row["split"],
                    "month": month,
                    "net_profit": data["profit"],
                    "trade_count": data["trades"],
                }
            )
        for session, data in sorted(sessions.items()):
            session_rows.append(
                {
                    "materialized_branch_id": row["materialized_branch_id"],
                    "package_id": row["package_id"],
                    "split": row["split"],
                    "session": session,
                    "net_profit": data["profit"],
                    "trade_count": data["trades"],
                }
            )
        curve_rows.append(
            {
                key: row[key]
                for key in (
                    "materialized_branch_id",
                    "package_id",
                    "split",
                    "net_profit",
                    "max_drawdown_amount",
                    "max_drawdown_percent",
                    "worst_month_net",
                    "positive_month_share",
                    "worst_session_net",
                    "worst_rolling_20_net",
                    "worst_rolling_50_net",
                    "max_local_drawdown",
                    "max_underwater_trades",
                    "curve_pocket_gate",
                )
            }
        )
        pocket_rows.append(
            {
                "materialized_branch_id": row["materialized_branch_id"],
                "package_id": row["package_id"],
                "split": row["split"],
                "pocket_gate": row["curve_pocket_gate"],
                "max_local_drawdown": row["max_local_drawdown"],
                "net_profit": row["net_profit"],
                "drawdown_to_net_ratio": number(row["max_local_drawdown"]) / max(number(row["net_profit"]), 1.0),
                "worst_rolling_20_net": row["worst_rolling_20_net"],
                "worst_rolling_50_net": row["worst_rolling_50_net"],
                "positive_month_share": row["positive_month_share"],
            }
        )
    return monthly_rows, session_rows, curve_rows, pocket_rows


def stage298_queue_rows() -> list[dict[str, Any]]:
    refs = ";".join(
        [
            "stage267_reference_evidence",
            "stage293_profit_scale_density_calibration_failure",
            "stage296_density_floor_profit_expansion_failure",
            "stage297_actual_mt5_low_profit_scale_failure",
        ]
    )
    return [
        {
            "seed_id": "stage298_profit_scale_edge_amplification_primary",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주축)",
            "hypothesis": "Stage297(297단계)은 4-10 trades/day(일 4-10거래)는 만들었지만 trade payoff(거래 보상 단위)가 작았다. Stage298(298단계)은 실제 MT5 out-deal(청산 거래) 수익을 직접 학습해 진입을 줄이지 않고 수익 단위를 키울 수 있는지 본다.",
            "broad_sweep": "MT5 out-deal label(청산 거래 라벨), payoff magnitude model(보상 크기 모델), session/volatility/state interaction(세션/변동성/상태 상호작용), density-preserving rank gate(밀도 보존 순위 관문)",
            "aggressive_sweep": "4/6/8/10 trades/day(일 4/6/8/10거래) 대역에서 payoff tail(보상 꼬리)을 넓히고, 큰 이익 구간의 hold/exit(보유/청산)를 공격적으로 바꾼다.",
            "defensive_sweep": "rolling pocket(구간 포켓), weak month(약한 월), weak session(약한 세션), drawdown-to-net ratio(순수익 대비 손실폭)를 강하게 거부한다.",
            "success_gate": "validation/OOS(검증/표본외) 각각 net profit(순수익) 300 이상, combined(합산) 800 이상, 4-10 trades/day(일 4-10거래), OOS PF(표본외 수익 팩터) 1.12 이상, 깊은 local hollow(국소 움푹 패임) 없음.",
            "discard_condition": "수익 규모가 한 달/한 세션/한 tail trade(꼬리 거래)에 집중되거나 OOS(표본외) 회복 계수가 1 미만이면 폐기한다.",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
        {
            "seed_id": "stage298_asymmetric_exit_payoff_router",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_aggressive(새 논제 공격형)",
            "hypothesis": "Stage297(297단계)의 기대값은 작았으므로 진입 표면보다 exit/hold asymmetry(청산/보유 비대칭)가 수익 규모 병목일 수 있다.",
            "broad_sweep": "winner extension(승자 연장), loser truncation(패자 단축), volatility-scaled hold(변동성 보정 보유), opposite-signal exit(반대 신호 청산)",
            "aggressive_sweep": "강한 보상 상태에서는 보유를 늘리고 약한 상태에서는 즉시 청산해 payoff skew(보상 기울기)를 키운다.",
            "defensive_sweep": "DD pocket(손실폭 포켓)과 session damage(세션 손상)가 생기면 즉시 탈락시킨다.",
            "success_gate": "거래수는 4-10 trades/day(일 4-10거래)를 유지하고, 순수익 규모와 회복 계수가 함께 개선된다.",
            "discard_condition": "거래 밀도만 줄어드는 thin repair(얇은 수리)나 한쪽 방향 몰림이면 폐기한다.",
            "prior_stage_refs": refs,
            "claim_boundary": BOUNDARY,
        },
    ]


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> str:
    best = max(scoreboard, key=lambda row: number(row.get("combined_net_profit"))) if scoreboard else {}
    total = len(scoreboard)
    minimum_pass = sum(1 for row in scoreboard if row.get("minimum_trade_gate") == "passed")
    density_pass = sum(1 for row in scoreboard if row.get("density_4_10_trading_day_gate") == "passed")
    profit_pass = sum(1 for row in scoreboard if row.get("profit_scale_gate") == "passed")
    efficiency_pass = sum(1 for row in scoreboard if row.get("efficiency_gate") == "passed")
    curve_pass = sum(1 for row in scoreboard if row.get("curve_pocket_gate") == "passed")
    lines = [
        "# run297C Bi-Level Curve-Monotonic Profit Review(297C 이중 단계 곡선 단조 수익 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- scoreboard_rows(점수판 행): `{len(scoreboard)}`",
        f"- failure_rows(실패 기억 행): `{len(failure_rows)}`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}` from `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): Stage297(297단계)은 실제 MT5 runtime probe(MT5 런타임 탐침)까지 완료했지만, 수익 규모와 확대 곡선 조건을 동시에 만족하지 못해 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.",
        "",
        "## Gate Result(관문 결과)",
        "",
        f"- minimum_trade_gate(최소 거래수 관문): `{minimum_pass}/{total}` 통과",
        f"- density_4_10_trading_day_gate(거래일 기준 일 4-10거래 관문): `{density_pass}/{total}` 통과",
        f"- profit_scale_gate(수익 규모 관문): `{profit_pass}/{total}` 통과",
        f"- efficiency_gate(효율 관문): `{efficiency_pass}/{total}` 통과",
        f"- curve_pocket_gate(곡선 포켓 관문): `{curve_pass}/{total}` 통과",
        "",
        "## Next Stage(다음 단계)",
        "",
        f"- opened_stage(열린 단계): `{NEXT_STAGE_ID}`",
        "- next_action(다음 행동): `run298A_design_profit_scale_edge_amplification_rebuild_packet`",
        "",
        f"`{BOUNDARY}`",
    ]
    return "\n".join(lines) + "\n"


def stage298_scaffold() -> None:
    for path in (NEXT_SPEC, NEXT_REVIEWS, NEXT_SELECTED):
        ledger.io_path(path).mkdir(parents=True, exist_ok=True)
    write_text(
        NEXT_SPEC / "stage_brief.md",
        "\n".join(
            [
                "# Stage298 Brief(298단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                "- question(질문): Can profit-scale edge amplification(수익 규모 거래우위 증폭) raise actual MT5 net profit(실제 MT5 순수익) while preserving 4-10 trades/day(일 4-10거래) and smooth zoomed curves(매끈한 확대 곡선)?",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): Stage297(297단계)의 낮은 순수익 failure memory(실패 기억)를 보존하되, 같은 bucket threshold(구간 임계값) 수리가 아니라 payoff magnitude(보상 크기), exit asymmetry(청산 비대칭), density-preserving rank(밀도 보존 순위)를 새 질문으로 연다.",
                "",
            ]
        ),
    )
    write_text(
        NEXT_SELECTED / "selection_status.md",
        "\n".join(
            [
                "# Stage298 Selection Status(298단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_profit_scale_edge_amplification_rebuild`",
                "- current_packet(현재 작업 묶음): `298_onnx_candidate_campaign__profit_scale_edge_amplification_rebuild_v1`",
                "- current_run(현재 실행): `none`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                "- target_candidate(목표 후보): `none`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(ONNX 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                "- next_action(다음 행동): `run298A_design_profit_scale_edge_amplification_rebuild_packet`",
                f"- stage297_review(297단계 검토): `{rel(REPORT)}`",
                "",
            ]
        ),
    )
    write_text(
        NEXT_REVIEWS / "review_index.md",
        "\n".join(
            [
                "# Stage298 Review Index(298단계 검토 색인)",
                "",
                f"- source_review(원천 검토): `{rel(REPORT)}`",
                f"- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`",
                "",
            ]
        ),
    )
    write_csv(
        NEXT_REVIEWS / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage298_opened_from_run297C",
                "stage_id": NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage297_review",
                "status": "opened_profit_scale_edge_amplification_rebuild",
                "judgment": "opened_from_stage297_low_profit_scale_failure_memory",
                "evidence_boundary": "planning_from_stage297_actual_mt5_evidence",
                "report_path": rel(REPORT),
                "notes": "next_action=run298A_design_profit_scale_edge_amplification_rebuild_packet",
            }
        ],
    )


def update_docs(status: str, judgment: str, next_action: str) -> None:
    selected = read_text(SELECTED)
    selected = selected.replace("`completed_bilevel_curve_monotonic_profit_mt5_probe_no_selection`", f"`{status}`")
    selected = selected.replace("`run297B_bilevel_curve_monotonic_profit_mt5_probe_v1`", f"`{RUN_ID}`")
    selected = selected.replace("`run297C_review_bilevel_curve_monotonic_profit_mt5_probe`", f"`{next_action}`")
    selected += f"- run297C_report(297C 보고): `{rel(REPORT)}`\n"
    selected += f"- stage298_opened(298단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index += f"- run297C_report(297C 보고): `{rel(REPORT)}`\n"
    review_index += f"- run297C_scoreboard(297C 점수판): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage298_seed_queue(298단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    lines = current.splitlines()
    replacements = {
        "- current_packet(": "- current_packet(현재 작업 묶음): `298_onnx_candidate_campaign__profit_scale_edge_amplification_rebuild_v1`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- status(": f"- status(상태): `{status}`",
        "- next_action(": f"- next_action(다음 행동): `{next_action}`",
    }
    new_lines = []
    replaced = set()
    for line in lines:
        changed = False
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                new_lines.append(replacement)
                replaced.add(prefix)
                changed = True
                break
        if not changed:
            new_lines.append(line)
    for prefix, replacement in replacements.items():
        if prefix not in replaced:
            new_lines.append(replacement)
    new_lines.append(
        f"- run297C_summary(297C 요약): Stage297(297단계) actual MT5 review(실제 MT5 검토)는 후보를 선택하지 않고 Stage298(298단계)을 열었다. Effect(효과): 낮은 순수익과 깊은 곡선 포켓을 failure memory(실패 기억)로 남기고, 다음 질문을 profit-scale edge amplification(수익 규모 거래우위 증폭)으로 바꾼다."
    )
    write_text(CURRENT_STATE, "\n".join(new_lines) + "\n")

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage297(297단계) run297C(297C 실행) bilevel curve-monotonic profit MT5 review(이중 단계 곡선 단조 수익 MT5 검토) `{RUN_ID}` closed Stage297 and opened Stage298(298단계). "
        f"Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 없고 next_action(다음 행동)은 `run298A_design_profit_scale_edge_amplification_rebuild_packet`이다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog += (
        f"\n## {UPDATED_ON} run297C bilevel curve-monotonic profit review(297C 이중 단계 곡선 단조 수익 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        "- effect(효과): Stage297(297단계)을 후보 없음으로 닫고 Stage298(298단계) profit-scale edge amplification(수익 규모 거래우위 증폭)을 열었다.\n"
        "- boundary(경계): Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 시작하지 않았다.\n"
    )
    write_text(CHANGELOG, changelog)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    if marker in workspace:
        return workspace
    needle = "current_focus:\n"
    if needle in workspace:
        return workspace.replace(needle, needle + focus, 1)
    return workspace.rstrip() + "\ncurrent_focus:\n" + focus


def update_registers(status: str, judgment: str, next_action: str) -> None:
    upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "bilevel_curve_monotonic_profit_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "notes": f"selected_candidate=none;adapter_package=none;onnx_readiness=not_started;next_action={next_action}.",
            }
        ],
        "run_id",
    )
    upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "bilevel_curve_monotonic_profit_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "trade_quality_curve_profit_scale",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": "selected_candidate=none;profit_scale_gate=failed",
                "guardrail_kpi": "Adapter=none;ONNX=not_started",
                "external_verification_status": "completed",
                "notes": f"next_action={next_action}.",
            }
        ],
        "ledger_row_id",
    )
    upsert(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "bilevel_curve_monotonic_profit_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "scoreboard": "bilevel_curve_monotonic_profit_review_scoreboard",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "runtime_probe_review_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": "Stage298 opened; no Adapter; no ONNX.",
            }
        ],
        "row_id",
    )


def update_memory_registers(failure_rows: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} profit-scale edge amplification handoff(수익 규모 거래우위 증폭 인계)\n\n"
            "- idea_id(아이디어 ID): `stage298_profit_scale_edge_amplification_primary`\n"
            "- hypothesis(가설): Stage297(297단계)의 낮은 순수익은 진입 수가 아니라 payoff magnitude(보상 크기)와 exit asymmetry(청산 비대칭)의 병목일 수 있다.\n"
            "- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).\n"
        )
        write_text(IDEA_REGISTER, idea)
    negative = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in negative:
        negative += (
            f"\n## {RUN_ID} Stage297 low profit-scale negative memory(297단계 낮은 수익 규모 부정 기억)\n\n"
            f"- failed_profiles(실패 프로필): `{len(failure_rows)}`\n"
            "- failure_boundary(실패 경계): 4-10 trades/day(일 4-10거래)는 대체로 유지됐지만 순수익 규모, OOS PF(표본외 수익 팩터), recovery(회복), curve pocket(곡선 포켓)이 동시에 부족했다.\n"
            "- do_not_repeat(반복 금지): Stage297 robust bucket(강건 구간) agree/soft flip/veto 임계값만 좁게 바꾸는 repair(수리)는 하지 않는다.\n"
            "- reopen_condition(재개 조건): 실제 MT5 routed total(라우팅 전체)에서 validation/OOS 각각 net profit(순수익) 300 이상과 combined(합산) 800 이상을 먼저 보여야 한다.\n"
        )
        write_text(NEGATIVE_REGISTER, negative)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    for path in paths:
        if not ledger.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage297_bilevel_curve_monotonic_profit_review_artifact",
                "path": rel(path),
                "sha256": ledger.sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": "2026-05-24T15:30:00Z",
                "notes": "Stage297 review and Stage298 open handoff",
            }
        )
    upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def write_result_files(scoreboard: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]], quality_rows: Sequence[Mapping[str, Any]]) -> None:
    monthly_rows, session_rows, curve_rows, pocket_rows = attribution_rows(quality_rows)
    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["materialized_branch_id"], scoreboard)
    write_csv(TRADE_QUALITY, list(quality_rows[0].keys()) if quality_rows else ["materialized_branch_id"], quality_rows)
    write_csv(MONTHLY, ["materialized_branch_id", "package_id", "split", "month", "net_profit", "trade_count"], monthly_rows)
    write_csv(SESSION, ["materialized_branch_id", "package_id", "split", "session", "net_profit", "trade_count"], session_rows)
    write_csv(CURVE, list(curve_rows[0].keys()) if curve_rows else ["materialized_branch_id"], curve_rows)
    write_csv(LOCAL_POCKETS, list(pocket_rows[0].keys()) if pocket_rows else ["materialized_branch_id"], pocket_rows)
    write_csv(FAILURE_MEMORY, list(failure_rows[0].keys()) if failure_rows else ["failure_id"], failure_rows)
    queue_rows = stage298_queue_rows()
    write_csv(NEXT_STAGE_QUEUE, list(queue_rows[0].keys()), queue_rows)
    status = "completed_bilevel_curve_monotonic_profit_review_no_candidate_stage298_opened"
    judgment = "bilevel_curve_monotonic_profit_actual_mt5_negative_low_profit_scale_no_adapter_no_onnx"
    next_action = "run298A_design_profit_scale_edge_amplification_rebuild_packet"
    result_rows = [
        {
            "result_subject": "Stage297 bi-level curve-monotonic profit actual MT5 review(297단계 이중 단계 곡선 단조 수익 실제 MT5 검토)",
            "evidence_available": f"scoreboard_rows={len(scoreboard)};failure_rows={len(failure_rows)};source_kpi={rel(SOURCE_KPI)}",
            "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성), MT5 runtime reproduction package(MT5 런타임 재현 패키지)",
            "judgment_label": "negative",
            "judgment_class": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "일 거래수는 만들었지만 순수익 규모와 확대 곡선이 부족해 ONNX(온엑스)로 넘길 수 없다.",
        }
    ]
    gate_rows = [
        {"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "36/36 attempt(시도)를 실제 tester output(테스터 출력)에 연결했다."},
        {"gate_name": "minimum_trade_and_density(최소 거래수와 밀도)", "status": "passed", "evidence_path": rel(SCOREBOARD), "effect": "거래일 기준 4-10 trades/day(일 4-10거래)는 대체로 유지됐다."},
        {"gate_name": "profit_scale_efficiency_curve(수익 규모/효율/곡선)", "status": "failed", "evidence_path": rel(SCOREBOARD), "effect": "순수익 규모, OOS 효율, curve pocket(곡선 포켓)이 조건 미달이다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "후보 관문 실패로 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(ONNX 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전 단계이므로 ONNX(온엑스)를 시작하지 않는다."},
    ]
    write_csv(RESULT_JUDGMENT, list(result_rows[0].keys()), result_rows)
    write_csv(GATE_AUDIT, list(gate_rows[0].keys()), gate_rows)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_started",
        "goal_achieve": "not_claimed",
        "next_stage_id": NEXT_STAGE_ID,
        "next_action": next_action,
        "artifacts": [rel(path) for path in (SCOREBOARD, TRADE_QUALITY, MONTHLY, SESSION, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)],
        "claim_boundary": BOUNDARY,
    }
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    write_text(LINEAGE, json.dumps({"producer": rel(PRODUCER), "inputs": [rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_SCOUT)], "outputs": manifest["artifacts"]}, ensure_ascii=False, indent=2) + "\n")
    write_text(REPORT, report_markdown(scoreboard, failure_rows))
    write_text(
        DECISION,
        "\n".join(
            [
                "# Stage297 Review Decision(297단계 검토 결정)",
                "",
                f"- decision(결정): `{judgment}`",
                f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
                "- effect(효과): Stage297(297단계)은 후보 없음으로 닫고, Stage298(298단계)에서 수익 규모 거래우위 증폭을 새 논제로 연다.",
                "",
            ]
        ),
    )
    stage298_scaffold()
    update_docs(status, judgment, next_action)
    update_registers(status, judgment, next_action)
    update_memory_registers(failure_rows)
    update_artifact_registry([SCOREBOARD, TRADE_QUALITY, MONTHLY, SESSION, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, DECISION, NEXT_SPEC / "stage_brief.md", NEXT_SELECTED / "selection_status.md", NEXT_REVIEWS / "review_index.md", NEXT_REVIEWS / "stage_run_ledger.csv"])
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "scoreboard_rows": len(scoreboard),
                "failure_rows": len(failure_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def main() -> None:
    rows, quality_rows, scout_rows = load_actual_routed_rows()
    scoreboard, failure_rows = build_scoreboard(rows, scout_rows)
    write_result_files(scoreboard, failure_rows, quality_rows)


if __name__ == "__main__":
    main()
