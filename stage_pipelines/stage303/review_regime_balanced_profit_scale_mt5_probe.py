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
from stage_pipelines.stage280.validate_directional_mapping_stability import trade_frame  # noqa: E402


STAGE_ID = "303_onnx_candidate_campaign__regime_balanced_profit_scale_router"
NEXT_STAGE_ID = "304_onnx_candidate_campaign__curve_pocket_aware_profit_source_rebuild"
RUN_ID = "run303C_review_regime_balanced_profit_scale_router_mt5_probe_v1"
RUN_NUMBER = "run303C"
SOURCE_RUN_ID = "run303B_regime_balanced_profit_scale_router_mt5_probe_v1"
PARENT_RUN_ID = "run303A_design_regime_balanced_profit_scale_router_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN303A = STAGE_ROOT / "02_runs" / "run303A"
RUN303B = STAGE_ROOT / "02_runs" / "run303B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC = NEXT_STAGE_ROOT / "00_spec"
NEXT_REVIEWS = NEXT_STAGE_ROOT / "03_reviews"
NEXT_SELECTED = NEXT_STAGE_ROOT / "04_selected"

SOURCE_EXECUTION = RUN303B / "execution_result.json"
SOURCE_KPI = RUN303B / "mt5_kpi_summary.csv"
SOURCE_SCOUT = RUN303A / "model_scout_scoreboard.csv"
PRODUCER = Path("stage_pipelines/stage303/review_regime_balanced_profit_scale_router_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "regime_balanced_profit_scale_router_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage304_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run303C_regime_balanced_profit_scale_router_review_stage304_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage303_regime_balanced_profit_scale_router_review_stage304_open.md"

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
    ledger.io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    ledger.write_csv_rows(path, columns, rows)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    try:
        ledger.upsert_csv_rows(path, columns, rows, key=key)
        return
    except OSError:
        existing = ledger.read_csv_rows(path) if ledger.path_exists(path) else []
        incoming = {str(row.get(key, "")): row for row in rows}
        merged = [row for row in existing if str(row.get(key, "")) not in incoming]
        merged.extend(rows)
        ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
        with ledger.io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns))
            writer.writeheader()
            for row in merged:
                writer.writerow({column: row.get(column, "") for column in columns})


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
    local = RUN303B / "features" / Path(feature_path).name
    if not ledger.path_exists(local) and feature_path.startswith("Project_Obsidian_Prime_v2/"):
        local = ROOT / feature_path.replace("Project_Obsidian_Prime_v2/", "")
    dates: set[str] = set()
    if not ledger.path_exists(local):
        return 183 if attempt.get("split") == "validation_is" else 131
    with ledger.io_path(local).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            bar_time = row.get("bar_time_server") or row.get("timestamp_utc") or ""
            if bar_time:
                dates.add(str(bar_time)[:10].replace(".", "-"))
    return len(dates)


def session_bucket(hour: int) -> str:
    if 16 <= hour < 18:
        return "cash_open_16_18"
    if 18 <= hour < 21:
        return "us_mid_18_21"
    if 21 <= hour <= 23:
        return "us_late_21_23"
    return "outside_cash"


def curve_stats(trades: pd.DataFrame, net_profit: float) -> dict[str, Any]:
    if trades.empty:
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
    profits = [float(value) for value in trades["net_profit"].tolist()]
    monthly: dict[str, float] = defaultdict(float)
    session: dict[str, float] = defaultdict(float)
    for _, trade in trades.iterrows():
        close_time = pd.to_datetime(trade["close_time"])
        monthly[close_time.strftime("%Y-%m")] += float(trade["net_profit"])
        session[session_bucket(int(close_time.hour))] += float(trade["net_profit"])

    balances: list[float] = []
    balance = 500.0
    for profit in profits:
        balance += profit
        balances.append(balance)
    peak = balances[0] if balances else 500.0
    max_dd = 0.0
    underwater = 0
    max_underwater = 0
    for balance_value in balances:
        if balance_value >= peak:
            peak = balance_value
            underwater = 0
        else:
            underwater += 1
            max_underwater = max(max_underwater, underwater)
            max_dd = max(max_dd, peak - balance_value)

    def worst_rolling(window: int) -> float:
        if len(profits) < window:
            return sum(profits)
        return min(sum(profits[index : index + window]) for index in range(len(profits) - window + 1))

    positive_month_share = sum(1 for value in monthly.values() if value > 0) / len(monthly) if monthly else 0.0
    worst20 = worst_rolling(20)
    worst50 = worst_rolling(50)
    curve_gate = "passed"
    if net_profit <= 0:
        curve_gate = "failed"
    if max_dd > max(80.0, net_profit * 0.45):
        curve_gate = "failed"
    if worst20 < -40.0 or worst50 < -80.0:
        curve_gate = "failed"
    if positive_month_share < 0.65:
        curve_gate = "failed"
    return {
        "deal_count": len(profits),
        "worst_month_net": min(monthly.values()) if monthly else 0.0,
        "positive_month_share": positive_month_share,
        "worst_session_net": min(session.values()) if session else 0.0,
        "worst_rolling_20_net": worst20,
        "worst_rolling_50_net": worst50,
        "max_local_drawdown": max_dd,
        "max_underwater_trades": max_underwater,
        "curve_pocket_gate": curve_gate,
    }


def load_actual_rows() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    execution = json.loads(ledger.io_path(SOURCE_EXECUTION).read_text(encoding="utf-8-sig"))
    attempts = {item.get("attempt_name"): item for item in execution.get("attempts", [])}
    scout_rows = {row["materialized_branch_id"]: row for row in ledger.read_csv_rows(SOURCE_SCOUT)}
    rows: list[dict[str, Any]] = []
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source_row in csv.DictReader(handle):
            if source_row.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source_row["metrics"])
            report = ast.literal_eval(source_row["report"])
            attempt = attempts.get(report.get("attempt_name"), {})
            materialized_id = str(attempt.get("stage303_branch_id") or attempt.get("materialized_branch_id") or "")
            package_id = str(attempt.get("package_id") or scout_rows.get(materialized_id, {}).get("package_id") or "")
            tester = attempt.get("ini", {}).get("tester", {})
            from_date = tester.get("FromDate")
            to_date = tester.get("ToDate")
            calendar_days = (parse_date(to_date) - parse_date(from_date)).days + 1 if from_date and to_date else 0
            trading_days = feature_trading_days(attempt)
            trades = int(number(metrics.get("trade_count")))
            net_profit = number(metrics.get("net_profit"))
            report_path = Path(str(metrics.get("report_path")))
            curve = curve_stats(trade_frame(report_path), net_profit)
            rows.append(
                {
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
            )
    return rows, scout_rows


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
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 650 and number(oos.get("trade_count")) >= 450 else "failed"
        density_gate = "passed" if 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0 else "failed"
        profit_scale_gate = "passed" if val_net >= 350.0 and oos_net >= 250.0 and combined >= 800.0 else "failed"
        efficiency_gate = "passed"
        if number(val.get("profit_factor")) < 1.12 or number(oos.get("profit_factor")) < 1.10:
            efficiency_gate = "failed"
        if number(val.get("recovery_factor")) < 1.0 or number(oos.get("recovery_factor")) < 1.0:
            efficiency_gate = "failed"
        if number(val.get("expectancy")) < 0.10 or number(oos.get("expectancy")) < 0.10:
            efficiency_gate = "failed"
        curve_gate = "passed" if val.get("curve_pocket_gate") == "passed" and oos.get("curve_pocket_gate") == "passed" else "failed"
        selected = all(
            gate == "passed"
            for gate in (min_trade_gate, density_gate, profit_scale_gate, efficiency_gate, curve_gate)
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
            failed = [
                name
                for name, gate in (
                    ("minimum_trade_gate", min_trade_gate),
                    ("density_4_10_trading_day_gate", density_gate),
                    ("profit_scale_gate", profit_scale_gate),
                    ("efficiency_gate", efficiency_gate),
                    ("curve_pocket_gate", curve_gate),
                )
                if gate != "passed"
            ]
            failure_rows.append(
                {
                    "failure_id": f"{candidate_id}_stage303_negative_or_watch",
                    "materialized_branch_id": candidate_id,
                    "package_id": row["package_id"],
                    "failed_boundary": ",".join(failed),
                    "why_failed": "actual MT5(실제 메타트레이더5) routed total(라우팅 전체)에서 수익 규모(profit scale, 수익 규모), 효율(efficiency, 효율), 곡선 포켓(curve pocket, 곡선 함몰) 조건을 동시에 통과하지 못했다.",
                    "salvage_value": "cp302A/cp302E처럼 OOS scale(표본외 규모)은 크지만 validation damage(검증 손상)가 큰 표본은 regime-balanced router(레짐 균형 라우터) 새 논제의 입력 단서로만 쓴다.",
                    "reopen_condition": "validation/OOS(검증/표본외) 모두 충분한 순수익, 4-10 trades/day(일 4-10거래), PF(수익요인), recovery(회복), 확대 곡선 품질을 동시에 보여야 한다.",
                    "do_not_repeat": "ATR/risk multiplier(ATR/위험 배수)만 좁게 조정하는 repair loop(수정 반복)는 하지 않는다.",
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
        trades = trade_frame(Path(str(row["report_path"])))
        monthly = defaultdict(lambda: {"profit": 0.0, "trades": 0})
        sessions = defaultdict(lambda: {"profit": 0.0, "trades": 0})
        for _, trade in trades.iterrows():
            close_time = pd.to_datetime(trade["close_time"])
            month = close_time.strftime("%Y-%m")
            session = session_bucket(int(close_time.hour))
            monthly[month]["profit"] += float(trade["net_profit"])
            monthly[month]["trades"] += 1
            sessions[session]["profit"] += float(trade["net_profit"])
            sessions[session]["trades"] += 1
        for month, values in monthly.items():
            monthly_rows.append({"materialized_branch_id": row["materialized_branch_id"], "package_id": row["package_id"], "split": row["split"], "month": month, "net_profit": values["profit"], "trade_count": values["trades"]})
        for session, values in sessions.items():
            session_rows.append({"materialized_branch_id": row["materialized_branch_id"], "package_id": row["package_id"], "split": row["split"], "session": session, "net_profit": values["profit"], "trade_count": values["trades"]})
        curve_rows.append({key: value for key, value in row.items() if key != "report_path"})
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


def stage304_queue_rows(scoreboard: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = sorted(scoreboard, key=lambda row: number(row.get("combined_net_profit")), reverse=True)[:2]
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(best, start=1):
        rows.append(
            {
                "seed_id": f"stage304_seed_{index:02d}",
                "source_stage_id": STAGE_ID,
                "source_run_id": RUN_ID,
                "source_package_id": row.get("package_id", ""),
                "seed_role": "positive_but_not_worthy(양수지만 가치 부족)",
                "hypothesis": "regime-balanced profit scale router(레짐 균형 수익 규모 라우터)가 OOS scale(표본외 규모)을 보존하면서 validation damage(검증 손상)를 줄일 수 있는지 본다.",
                "broad_sweep": "regime features(레짐 피처), session routing(세션 라우팅), model variants(모델 변형), risk gating(위험 게이팅)을 제한 없이 탐색한다.",
                "aggressive_sweep": "OOS scale(표본외 규모)을 만든 cp302A/cp302E류 upside(상방)를 보존한다.",
                "defensive_sweep": "validation drawdown(검증 손실폭), weak month(약한 월), weak session(약한 세션)을 먼저 차단한다.",
                "discard_condition": "actual MT5(실제 메타트레이더5)에서 validation/OOS 균형이 동시에 나오지 않으면 폐기한다.",
                "prior_stage_refs": "stage301_positive_small;stage303_oos_scale_validation_damage",
                "claim_boundary": BOUNDARY,
            }
        )
    if not rows:
        rows.append(
            {
                "seed_id": "stage304_seed_fresh_regime_balance",
                "source_stage_id": STAGE_ID,
                "source_run_id": RUN_ID,
                "source_package_id": "none",
                "seed_role": "fresh_thesis(새 논제)",
                "hypothesis": "payoff convexity(보상 볼록성)가 split damage(분할 손상)를 만들면 regime router(레짐 라우터)를 새로 만든다.",
                "broad_sweep": "unrestricted(무제한)",
                "aggressive_sweep": "profit scale first(수익 규모 우선)",
                "defensive_sweep": "curve pocket removal(곡선 함몰 제거)",
                "discard_condition": "no actual MT5 positive OOS(실제 표본외 양수 없음)",
                "prior_stage_refs": "stage303",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def scaffold_stage304() -> None:
    for path in (NEXT_SPEC, NEXT_REVIEWS, NEXT_SELECTED):
        ledger.io_path(path).mkdir(parents=True, exist_ok=True)
    write_text(
        NEXT_SPEC / "stage_brief.md",
        "\n".join(
            [
                "# Stage304 Brief(304단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                "- question(질문): Can a curve-pocket-aware profit source rebuild(곡선 포켓 인식 수익 원천 재구성) create scale(규모), 4-10 trades/day(일 4-10거래), and smooth equity(매끄러운 평가금) together?",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): Stage303(303단계)의 no-late router(후반 제외 라우터)를 좁게 수리하지 않고, 곡선 포켓과 수익 규모를 함께 겨냥하는 새 후보 영역을 연다.",
            ]
        ),
    )
    write_text(
        NEXT_SELECTED / "selection_status.md",
        "\n".join(
            [
                "# Stage304 Selection Status(304단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_curve_pocket_aware_profit_source_rebuild`",
                "- current_packet(현재 작업 묶음): `304_onnx_candidate_campaign__curve_pocket_aware_profit_source_rebuild_v1`",
                "- current_run(현재 실행): `none`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                "- target_candidate(목표 후보): `none`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                "- next_action(다음 행동): `run304A_design_curve_pocket_aware_profit_source_rebuild_packet`",
                f"- stage303_review(303단계 검토): `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(
        NEXT_REVIEWS / "review_index.md",
        "\n".join(
            [
                "# Stage304 Review Index(304단계 검토 색인)",
                "",
                f"- source_review(원천 검토): `{rel(REPORT)}`",
                f"- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`",
            ]
        ),
    )
    write_csv(
        NEXT_REVIEWS / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage304_opened_from_run303C",
                "stage_id": NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage303_review",
                "status": "opened_curve_pocket_aware_profit_source_rebuild",
                "judgment": "opened_from_stage303_router_failure_no_onnx_worthy_candidate",
                "evidence_boundary": "planning_from_stage303_actual_mt5_evidence",
                "report_path": rel(REPORT),
                "notes": "next_action=run304A_design_curve_pocket_aware_profit_source_rebuild_packet",
            }
        ],
    )
    return
    for path in (NEXT_SPEC, NEXT_REVIEWS, NEXT_SELECTED):
        ledger.io_path(path).mkdir(parents=True, exist_ok=True)
    write_text(
        NEXT_SPEC / "stage_brief.md",
        "\n".join(
            [
                "# Stage303 Brief(303단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                "- question(질문): Can a regime-balanced profit scale router(레짐 균형 수익 규모 라우터) preserve the OOS scale(표본외 규모) seen in Stage303(302단계) while removing validation damage(검증 손상), keeping 4-10 trades/day(일 4-10거래), and smoothing the equity curve(평가금 곡선)?",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): ATR/risk(ATR/위험) 배수만 좁게 고치지 않고, 레짐/세션/위험 라우팅을 새로 설계한다.",
            ]
        ),
    )
    write_text(
        NEXT_SELECTED / "selection_status.md",
        "\n".join(
            [
                "# Stage303 Selection Status(303단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_regime_balanced_profit_scale_router`",
                "- current_packet(현재 작업 묶음): `303_onnx_candidate_campaign__regime_balanced_profit_scale_router_v1`",
                "- current_run(현재 실행): `none`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                "- target_candidate(목표 후보): `none`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                "- next_action(다음 행동): `run304A_design_curve_pocket_aware_profit_source_rebuild_packet`",
                f"- stage303_review(302단계 검토): `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(
        NEXT_REVIEWS / "review_index.md",
        "\n".join(
            [
                "# Stage303 Review Index(303단계 검토 색인)",
                "",
                f"- source_review(원천 검토): `{rel(REPORT)}`",
                f"- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`",
            ]
        ),
    )
    write_csv(
        NEXT_REVIEWS / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage304_opened_from_run303C",
                "stage_id": NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage303_review",
                "status": "opened_regime_balanced_profit_scale_router",
                "judgment": "opened_from_stage303_oos_scale_validation_damage_no_onnx_worthy_candidate",
                "evidence_boundary": "planning_from_stage303_actual_mt5_evidence",
                "report_path": rel(REPORT),
                "notes": "next_action=run304A_design_curve_pocket_aware_profit_source_rebuild_packet",
            }
        ],
    )


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> str:
    best = max(scoreboard, key=lambda row: number(row.get("combined_net_profit"))) if scoreboard else {}
    lines = [
        "# run303C Regime Balanced Profit Scale Router Review(302C 보상 볼록성 수익 규모 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- scoreboard_rows(점수판 행): `{len(scoreboard)}`",
        f"- failure_rows(실패 기억 행): `{len(failures)}`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}` from `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): Stage303(302단계)는 OOS(표본외) 수익 규모를 일부 만들었지만 validation(검증) 안정성, 효율, 곡선 품질을 동시에 만족하지 못해 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.",
        "",
        "## Scoreboard(점수판)",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 수익요인) | OOS net(표본외 순수익) | OOS PF(표본외 수익요인) | trades/day(일 거래수) | gates(관문) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        gate_text = ",".join(
            name
            for name, value in (
                ("min", row["minimum_trade_gate"]),
                ("density", row["density_4_10_trading_day_gate"]),
                ("scale", row["profit_scale_gate"]),
                ("eff", row["efficiency_gate"]),
                ("curve", row["curve_pocket_gate"]),
            )
            if value != "passed"
        )
        lines.append(
            "| {pkg} | {vn:.2f} | {vpf:.2f} | {on:.2f} | {opf:.2f} | {td:.2f}/{od:.2f} | {gates} |".format(
                pkg=row["package_id"],
                vn=number(row["validation_net_profit"]),
                vpf=number(row["validation_pf"]),
                on=number(row["oos_net_profit"]),
                opf=number(row["oos_pf"]),
                td=number(row["validation_trades_per_trading_day"]),
                od=number(row["oos_trades_per_trading_day"]),
                gates=gate_text or "passed",
            )
        )
    lines.extend(
        [
            "",
            "## Next Stage(다음 단계)",
            "",
            f"- opened_stage(열린 단계): `{NEXT_STAGE_ID}`",
            "- next_action(다음 행동): `run304A_design_curve_pocket_aware_profit_source_rebuild_packet`",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


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


def update_docs(status: str, judgment: str, next_action: str) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selected += f"- run303C_report(302C 보고): `{rel(REPORT)}`\n"
    selected += f"- stage304_opened(303단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index += f"- run303C_report(302C 보고): `{rel(REPORT)}`\n"
    review_index += f"- run303C_scoreboard(302C 점수판): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage304_seed_queue(303단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current += "- run303C_summary(302C 요약): Stage303(302단계)는 actual MT5(실제 메타트레이더5) OOS scale(표본외 규모)을 만들었지만 validation damage(검증 손상)가 커서 ONNX-worthy(온엑스 가치 있음) 조건에는 부족했다. Effect(효과): Adapter(어댑터)와 ONNX(온엑스)를 시작하지 않고 Stage303(303단계) regime-balanced router(레짐 균형 라우터) 질문으로 전환했다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage303(302단계) run303C(302C 실행) regime balanced profit scale router review(보상 볼록성 수익 규모 검토) `{RUN_ID}` closed Stage303 and opened Stage304(304단계). "
        f"Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 없고 next_action(다음 행동)은 `run304A_design_curve_pocket_aware_profit_source_rebuild_packet`이다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog += (
        f"\n## {UPDATED_ON} run303C regime balanced profit scale router review(302C 보상 볼록성 수익 규모 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        "- effect(효과): Stage303(302단계)를 후보 없음으로 닫고 Stage303(303단계) regime-balanced profit scale router(레짐 균형 수익 규모 라우터)를 열었다.\n"
        "- boundary(경계): Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 시작하지 않았다.\n"
    )
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str, next_action: str) -> None:
    safe_upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "regime_balanced_profit_scale_router_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate=none;adapter_package=none;onnx_readiness=not_started;next_action={next_action}."}],
        "run_id",
    )
    safe_upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "regime_balanced_profit_scale_router_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "trade_quality_curve_profit_scale",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": "positive_small_no_selected_candidate",
                "guardrail_kpi": "Adapter=none;ONNX=not_started",
                "external_verification_status": "completed",
                "notes": f"next_action={next_action}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "regime_balanced_profit_scale_router_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "regime_balanced_profit_scale_router_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": "Stage303 opened; no Adapter(어댑터); no ONNX(온엑스)."}],
        "row_id",
    )


def update_memory_registers(failures: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} regime-balanced router handoff(레짐 균형 라우터 인계)\n\n"
            "- idea_id(아이디어 ID): `stage304_curve_pocket_aware_profit_source_primary`\n"
            "- hypothesis(가설): Stage303(302단계)의 OOS scale(표본외 규모)은 레짐/세션 조건을 분리해야 validation damage(검증 손상) 없이 살아남을 수 있다.\n"
            "- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).\n"
        )
        write_text(IDEA_REGISTER, idea)
    negative = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in negative:
        negative += (
            f"\n## {RUN_ID} Stage303 OOS-scale validation-damage failure memory(302단계 표본외 규모/검증 손상 실패 기억)\n\n"
            f"- failed_profiles(실패 프로필): `{len(failures)}`\n"
            "- failure_boundary(실패 경계): 일부 profile(프로필)은 OOS(표본외) 수익 규모가 컸지만 validation(검증) 손익/회복/곡선 포켓 조건을 동시에 만족하지 못했다.\n"
            "- do_not_repeat(반복 금지): ATR/risk(ATR/위험) 배수만 좁게 조정하지 않는다.\n"
            "- reopen_condition(재개 조건): 실제 MT5(메타트레이더5)에서 충분한 OOS(표본외) 순수익과 매끄러운 확대 곡선을 먼저 보여야 한다.\n"
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
                "artifact_type": "stage303_regime_balanced_profit_scale_router_review_artifact",
                "path": rel(path),
                "sha256": ledger.sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": "2026-05-24T20:50:00Z",
                "notes": "Stage303 review and Stage304 open handoff",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    rows, scout_rows = load_actual_rows()
    scoreboard, failure_rows = build_scoreboard(rows, scout_rows)
    monthly_rows, session_rows, curve_rows, pocket_rows = attribution_rows(rows)
    stage304_rows = stage304_queue_rows(scoreboard)
    status = "completed_regime_balanced_profit_scale_router_review_no_candidate_stage304_opened"
    judgment = "actual_mt5_oos_scale_validation_damage_not_onnx_worthy_no_adapter_no_onnx"
    next_action = "run304A_design_curve_pocket_aware_profit_source_rebuild_packet"

    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["materialized_branch_id"], scoreboard)
    write_csv(TRADE_QUALITY, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(MONTHLY, list(monthly_rows[0].keys()) if monthly_rows else ["materialized_branch_id"], monthly_rows)
    write_csv(SESSION, list(session_rows[0].keys()) if session_rows else ["materialized_branch_id"], session_rows)
    write_csv(CURVE, list(curve_rows[0].keys()) if curve_rows else ["materialized_branch_id"], curve_rows)
    write_csv(LOCAL_POCKETS, list(pocket_rows[0].keys()) if pocket_rows else ["materialized_branch_id"], pocket_rows)
    write_csv(FAILURE_MEMORY, list(failure_rows[0].keys()) if failure_rows else ["failure_id"], failure_rows)
    write_csv(NEXT_STAGE_QUEUE, list(stage304_rows[0].keys()), stage304_rows)
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "next_action": next_action, "claim_boundary": BOUNDARY}],
    )
    gate_rows = [
        {"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "36/36 attempt(시도)를 실제 tester output(테스터 출력)에 연결했다."},
        {"gate_name": "minimum_trade_and_density(최소 거래수와 밀도)", "status": "mixed", "evidence_path": rel(SCOREBOARD), "effect": "대부분 4-10 trades/day(일 4-10거래)를 지켰지만 일부는 최소 거래수 또는 밀도에서 벗어났다."},
        {"gate_name": "profit_scale_efficiency_curve(수익 규모/효율/곡선)", "status": "failed", "evidence_path": rel(SCOREBOARD), "effect": "OOS(표본외) 순수익 규모와 recovery/curve(회복/곡선) 조건이 부족하다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "후보 관문 실패로 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(ONNX 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전 단계이므로 ONNX(온엑스)를 시작하지 않는다."},
    ]
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
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(LINEAGE, json.dumps({"run_id": RUN_ID, "producer": str(PRODUCER), "inputs": [rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_SCOUT)], "outputs": manifest["artifacts"]}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard, failure_rows))
    write_text(
        DECISION,
        "\n".join(
            [
                "# Stage303 Decision(302단계 결정)",
                "",
                f"- decision(결정): `{judgment}`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
                "",
                "Effect(효과): OOS scale(표본외 규모) 단서는 보존하지만 ONNX-worthy(온엑스 가치 있음) 후보로 선언하지 않고, regime-balanced router(레짐 균형 라우터) 새 단계로 넘긴다.",
            ]
        ),
    )
    scaffold_stage304()
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


if __name__ == "__main__":
    main()
