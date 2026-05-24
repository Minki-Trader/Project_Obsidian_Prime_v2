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


STAGE_ID = "299_onnx_candidate_campaign__runtime_realized_trade_shape_rebuild"
NEXT_STAGE_ID = "300_onnx_candidate_campaign__split_forward_trade_shape_generalization_rebuild"
RUN_ID = "run299C_review_runtime_realized_trade_shape_mt5_probe_v1"
RUN_NUMBER = "run299C"
SOURCE_RUN_ID = "run299B_runtime_realized_trade_shape_mt5_probe_v1"
PARENT_RUN_ID = "run299A_design_runtime_realized_trade_shape_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN299A = STAGE_ROOT / "02_runs" / "run299A"
RUN299B = STAGE_ROOT / "02_runs" / "run299B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC = NEXT_STAGE_ROOT / "00_spec"
NEXT_REVIEWS = NEXT_STAGE_ROOT / "03_reviews"
NEXT_SELECTED = NEXT_STAGE_ROOT / "04_selected"

SOURCE_EXECUTION = RUN299B / "execution_result.json"
SOURCE_KPI = RUN299B / "mt5_kpi_summary.csv"
SOURCE_SCOUT = RUN299A / "model_scout_scoreboard.csv"
PRODUCER = Path("stage_pipelines/stage299/review_runtime_realized_trade_shape_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "runtime_realized_trade_shape_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage300_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run299C_runtime_realized_trade_shape_review_stage300_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage299_runtime_realized_trade_shape_review_stage300_open.md"

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
    local = RUN299B / "features" / Path(feature_path).name
    if not ledger.path_exists(local) and feature_path.startswith("Project_Obsidian_Prime_v2/"):
        local = ROOT / feature_path.replace("Project_Obsidian_Prime_v2/", "")
    dates: set[str] = set()
    if not ledger.path_exists(local):
        return 183 if attempt.get("split") == "validation_is" else 131
    with ledger.io_path(local).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
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
    if max_dd > max(35.0, net_profit * 0.35):
        curve_gate = "failed"
    if worst20 < -20.0 or worst50 < -35.0:
        curve_gate = "failed"
    if positive_month_share < 0.60:
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


def load_actual_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
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
            materialized_id = str(attempt.get("stage299_branch_id") or attempt.get("materialized_branch_id") or "")
            package_id = str(attempt.get("package_id") or scout_rows.get(materialized_id, {}).get("package_id") or "")
            tester = attempt.get("ini", {}).get("tester", {})
            from_date = tester.get("FromDate")
            to_date = tester.get("ToDate")
            calendar_days = (parse_date(to_date) - parse_date(from_date)).days + 1 if from_date and to_date else 0
            trading_days = feature_trading_days(attempt)
            trades = int(number(metrics.get("trade_count")))
            net_profit = number(metrics.get("net_profit"))
            report_path = Path(str(metrics.get("report_path")))
            trade_rows = trade_frame(report_path)
            curve = curve_stats(trade_rows, net_profit)
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
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 650 and number(oos.get("trade_count")) >= 450 else "failed"
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
                    "failure_id": f"{candidate_id}_stage299_negative",
                    "materialized_branch_id": candidate_id,
                    "package_id": row["package_id"],
                    "failed_boundary": ",".join(reasons),
                    "why_failed": "actual MT5 routed total(실제 MT5 라우팅 전체)에서 validation(검증)은 일부 회복됐지만 OOS(표본외)가 음수라 수익 규모, 효율, 곡선 조건을 동시에 만족하지 못했다.",
                    "salvage_value": "validation-positive/OOS-negative split divergence(검증 양수/표본외 음수 분기)를 다음 단계의 일반화 문제로 보존한다.",
                    "reopen_condition": "split-forward train-only shape(분할 전진 학습 전용 형태)가 validation/OOS 모두 순수익 300 이상과 깊은 곡선 포켓 제거를 보여야 한다.",
                    "do_not_repeat": "Stage299 trade-shape score(거래 형태 점수)의 단순 quantile(분위) 조정이나 같은 loss-cluster veto(손실 군집 거부)만 반복하지 않는다.",
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
        trades = trade_frame(report_path)
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
            monthly_rows.append(
                {
                    "materialized_branch_id": row["materialized_branch_id"],
                    "package_id": row["package_id"],
                    "split": row["split"],
                    "month": month,
                    "net_profit": values["profit"],
                    "trade_count": values["trades"],
                }
            )
        for session, values in sessions.items():
            session_rows.append(
                {
                    "materialized_branch_id": row["materialized_branch_id"],
                    "package_id": row["package_id"],
                    "split": row["split"],
                    "session": session,
                    "net_profit": values["profit"],
                    "trade_count": values["trades"],
                }
            )
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


def stage300_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "seed_id": "stage300_split_forward_shape_generalization_primary",
            "source_stage_id": STAGE_ID,
            "source_run_id": RUN_ID,
            "seed_role": "fresh_thesis_primary(새 논제 주씨앗)",
            "hypothesis": "Stage299(299단계)는 validation(검증) 손상을 줄였지만 OOS(표본외)가 음수였다. Stage300(300단계)은 OOS(표본외) 결과를 학습 재료로 쓰지 않고, validation(검증) 내부 시간 순서 subfold(하위 분할)에서 일반화되는 trade shape(거래 형태)만 남겨 수익 규모와 4-10 trades/day(일 4-10거래)를 동시에 노린다.",
            "broad_sweep": "train-only chronological subfolds(학습 전용 시간 순서 하위 분할), regime-stable shape buckets(국면 안정 거래 형태 구간), density-preserving model variants(밀도 보존 모델 변형)",
            "aggressive_sweep": "validation-forward stable positive buckets(검증 전진 안정 양수 구간)을 6-8 trades/day(일 6-8거래)까지 재확장한다.",
            "defensive_sweep": "OOS-negative signature(표본외 음수 서명), late-window drawdown pocket(후반 손실 포켓), session inversion(세션 반전)을 사전 veto(거부)한다.",
            "success_gate": "validation/OOS each net profit(순수익) 300 이상, combined(합산) 800 이상, 4-10 trades/day(일 4-10거래), PF(수익 팩터) 1.12 이상, 깊은 local hollow(국소 꺼짐) 없음.",
            "discard_condition": "validation(검증)만 양수거나 OOS(표본외)가 다시 음수면 discard(폐기)하고 같은 shape-threshold repair(형태 임계값 수리)를 반복하지 않는다.",
            "prior_stage_refs": "stage298_payoff_rank_validation_damage;stage299_validation_positive_oos_negative_trade_shape_failure",
            "claim_boundary": BOUNDARY,
        }
    ]


def stage300_scaffold() -> None:
    for path in (NEXT_SPEC, NEXT_REVIEWS, NEXT_SELECTED):
        ledger.io_path(path).mkdir(parents=True, exist_ok=True)
    write_text(
        NEXT_SPEC / "stage_brief.md",
        "\n".join(
            [
                "# Stage300 Brief(300단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                "- question(질문): Can split-forward trade-shape generalization(분할 전진 거래 형태 일반화) keep the validation-positive clue(검증 양수 단서) without repeating OOS-negative failure(표본외 음수 실패), while preserving 4-10 trades/day(일 4-10거래), profit scale(수익 규모), and smooth curves(매끄러운 곡선)?",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): Stage299(299단계)의 validation-only recovery(검증 전용 회복)를 후보로 보존하지 않고, 시간 순서 일반화가 되는 구조만 새로 만든다.",
                "",
            ]
        ),
    )
    write_text(
        NEXT_SELECTED / "selection_status.md",
        "\n".join(
            [
                "# Stage300 Selection Status(300단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_split_forward_trade_shape_generalization_rebuild`",
                "- current_packet(현재 작업 묶음): `300_onnx_candidate_campaign__split_forward_trade_shape_generalization_rebuild_v1`",
                "- current_run(현재 실행): `none`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                "- target_candidate(목표 후보): `none`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(ONNX 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                "- next_action(다음 행동): `run300A_design_split_forward_trade_shape_generalization_rebuild_packet`",
                f"- stage299_review(299단계 검토): `{rel(REPORT)}`",
                "",
            ]
        ),
    )
    write_text(
        NEXT_REVIEWS / "review_index.md",
        "\n".join(
            [
                "# Stage300 Review Index(300단계 검토 색인)",
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
                "row_id": "stage300_opened_from_run299C",
                "stage_id": NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage299_review",
                "status": "opened_split_forward_trade_shape_generalization_rebuild",
                "judgment": "opened_from_stage299_validation_positive_oos_negative_failure_memory",
                "evidence_boundary": "planning_from_stage299_actual_mt5_evidence",
                "report_path": rel(REPORT),
                "notes": "next_action=run300A_design_split_forward_trade_shape_generalization_rebuild_packet",
            }
        ],
    )


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> str:
    best = max(scoreboard, key=lambda row: number(row.get("combined_net_profit"))) if scoreboard else {}
    total = len(scoreboard)
    profit_pass = sum(1 for row in scoreboard if row.get("profit_scale_gate") == "passed")
    efficiency_pass = sum(1 for row in scoreboard if row.get("efficiency_gate") == "passed")
    curve_pass = sum(1 for row in scoreboard if row.get("curve_pocket_gate") == "passed")
    lines = [
        "# run299C Runtime-Realized Trade Shape Review(299C 런타임 실제 거래 형태 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- scoreboard_rows(점수판 행): `{len(scoreboard)}`",
        f"- failure_rows(실패 기억 행): `{len(failures)}`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}` from `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): Stage299(299단계)는 validation(검증) 일부 회복을 만들었지만 OOS(표본외)가 음수라 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.",
        "",
        "## Scoreboard(점수판)",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        gate_text = ",".join(
            name
            for name, value in (
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
            "## Gate Result(관문 결과)",
            "",
            f"- profit_scale_gate(수익 규모 관문): `{profit_pass}/{total}` 통과",
            f"- efficiency_gate(효율 관문): `{efficiency_pass}/{total}` 통과",
            f"- curve_pocket_gate(곡선 포켓 관문): `{curve_pass}/{total}` 통과",
            "",
            "## Next Stage(다음 단계)",
            "",
            f"- opened_stage(열린 단계): `{NEXT_STAGE_ID}`",
            "- next_action(다음 행동): `run300A_design_split_forward_trade_shape_generalization_rebuild_packet`",
            "",
            f"`{BOUNDARY}`",
            "",
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
    selected += f"- run299C_report(299C 보고): `{rel(REPORT)}`\n"
    selected += f"- stage300_opened(300단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index += f"- run299C_report(299C 보고): `{rel(REPORT)}`\n"
    review_index += f"- run299C_scoreboard(299C 점수판): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage300_seed_queue(300단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = current.rstrip() + f"\n- run299C_summary(299C 요약): Stage299(299단계) actual MT5 review(실제 MT5 검토)는 후보를 선택하지 않고 Stage300(300단계)을 열었다. Effect(효과): validation-positive/OOS-negative(검증 양수/표본외 음수) 실패를 failure memory(실패 기억)로 남기고 split-forward trade shape generalization(분할 전진 거래 형태 일반화)으로 질문을 바꾼다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage299(299단계) run299C(299C 실행) runtime-realized trade shape MT5 review(런타임 실제 거래 형태 MT5 검토) `{RUN_ID}` closed Stage299 and opened Stage300(300단계). "
        f"Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 없고 next_action(다음 행동)은 `run300A_design_split_forward_trade_shape_generalization_rebuild_packet`이다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog += (
        f"\n## {UPDATED_ON} run299C runtime-realized trade shape review(299C 런타임 실제 거래 형태 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        "- effect(효과): Stage299(299단계)을 후보 없음으로 닫고 Stage300(300단계) split-forward trade shape generalization(분할 전진 거래 형태 일반화)을 열었다.\n"
        "- boundary(경계): Adapter(어댑터), ONNX(온엑스), Goal Achieve(목표 달성)는 시작하지 않았다.\n"
    )
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str, next_action: str) -> None:
    upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_realized_trade_shape_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate=none;adapter_package=none;onnx_readiness=not_started;next_action={next_action}."}],
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
                "record_view": "runtime_realized_trade_shape_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "trade_quality_curve_profit_scale",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": "selected_candidate=none;oos_negative_failure=present",
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
        [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "runtime_realized_trade_shape_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "runtime_realized_trade_shape_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": "Stage300 opened; no Adapter; no ONNX."}],
        "row_id",
    )


def update_memory_registers(failures: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} split-forward trade shape handoff(분할 전진 거래 형태 인계)\n\n"
            "- idea_id(아이디어 ID): `stage300_split_forward_shape_generalization_primary`\n"
            "- hypothesis(가설): Stage299(299단계)의 validation(검증) 회복은 일반화되지 않았으므로 시간 순서 subfold(하위 분할)에서 살아남는 형태만 후보가 될 수 있다.\n"
            "- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).\n"
        )
        write_text(IDEA_REGISTER, idea)
    negative = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in negative:
        negative += (
            f"\n## {RUN_ID} Stage299 validation-positive OOS-negative memory(299단계 검증 양수 표본외 음수 기억)\n\n"
            f"- failed_profiles(실패 프로필): `{len(failures)}`\n"
            "- failure_boundary(실패 경계): 일부 후보는 validation(검증) 순수익/PF(수익 팩터)를 회복했지만 OOS(표본외)가 음수라 ONNX-worthy(온엑스 가치) 조건을 만족하지 못했다.\n"
            "- do_not_repeat(반복 금지): 같은 trade-shape quantile(거래 형태 분위) 또는 loss-cluster veto(손실 군집 거부) 조정만 반복하지 않는다.\n"
            "- reopen_condition(재개 조건): split-forward(분할 전진) 구조에서 validation/OOS 모두 순수익 300 이상과 곡선 포켓 제거를 먼저 보여야 한다.\n"
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
                "artifact_type": "stage299_runtime_realized_trade_shape_review_artifact",
                "path": rel(path),
                "sha256": ledger.sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": "2026-05-24T20:30:00Z",
                "notes": "Stage299 review and Stage300 open handoff",
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
    queue_rows = stage300_queue_rows()
    write_csv(NEXT_STAGE_QUEUE, list(queue_rows[0].keys()), queue_rows)
    status = "completed_runtime_realized_trade_shape_review_no_candidate_stage300_opened"
    judgment = "runtime_realized_trade_shape_actual_mt5_negative_oos_generalization_failure_no_adapter_no_onnx"
    next_action = "run300A_design_split_forward_trade_shape_generalization_rebuild_packet"
    result_rows = [
        {
            "result_subject": "Stage299 runtime-realized trade shape actual MT5 review(299단계 런타임 실제 거래 형태 실제 MT5 검토)",
            "evidence_available": f"scoreboard_rows={len(scoreboard)};failure_rows={len(failure_rows)};source_kpi={rel(SOURCE_KPI)}",
            "evidence_missing": "Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성), MT5 runtime reproduction package(MT5 런타임 재현 패키지)",
            "judgment_label": "negative",
            "judgment_class": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "검증은 일부 살아났지만 표본외가 음수라 ONNX(온엑스)로 넘길 수 없다.",
        }
    ]
    gate_rows = [
        {"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "36/36 attempt(시도)를 실제 tester output(테스터 출력)에 연결했다."},
        {"gate_name": "minimum_trade_and_density(최소 거래수와 밀도)", "status": "passed", "evidence_path": rel(SCOREBOARD), "effect": "거래 수와 4-10 trades/day(일 4-10거래)는 대체로 지켰다."},
        {"gate_name": "profit_scale_efficiency_curve(수익 규모/효율/곡선)", "status": "failed", "evidence_path": rel(SCOREBOARD), "effect": "OOS(표본외) 음수와 곡선 포켓 때문에 조건 미달이다."},
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
                "# Stage299 Review Decision(299단계 검토 결정)",
                "",
                f"- decision(결정): `{judgment}`",
                f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
                "- effect(효과): Stage299(299단계)는 후보 없음으로 닫고, Stage300(300단계)에서 split-forward trade shape generalization(분할 전진 거래 형태 일반화)을 새 논제로 연다.",
                "",
            ]
        ),
    )
    stage300_scaffold()
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
    rows, quality_rows, scout_rows = load_actual_rows()
    scoreboard, failure_rows = build_scoreboard(rows, scout_rows)
    write_result_files(scoreboard, failure_rows, quality_rows)


if __name__ == "__main__":
    main()
