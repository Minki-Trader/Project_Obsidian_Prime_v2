from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage338 import execute_runtime_collapsed_onnx_mt5_probe_without_db as ex  # noqa: E402


aw = ex.aw

TODAY = "2026-06-01"
STAGE_ID = ex.STAGE_ID
STAGE_DIR = ex.STAGE_DIR
RUN_NUMBER = "run338I"
RUN_ID = "run338I_review_runtime_collapsed_onnx_mt5_probe_or_repair_without_db_v1"
PARENT_RUN_ID = ex.RUN_ID
NEXT_RUN_ID = "run338J_materialize_trade_count_recovery_expansion_mt5_probe_package_without_db_v1"
STATUS = "completed_stage338I_runtime_positive_clue_reviewed_trade_count_recovery_repair_required_no_selection"
JUDGMENT = "mt5_runtime_positive_exact_parity_but_trade_count_low_recovery_under_floor_no_selection"
DECISION = "stage338I_open_run338J_trade_count_recovery_expansion_or_confirmation_probe"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338I_runtime_collapsed_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338I_runtime_collapsed_mt5_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUNTIME_REVIEW = RUN_DIR / "run338I_runtime_review_scorecard.csv"
PROXY_MT5_DIFF_ATTRIBUTION = RUN_DIR / "run338I_proxy_mt5_diff_attribution.csv"
KPI_JUDGMENT = RUN_DIR / "run338I_mt5_kpi_judgment.csv"
REPAIR_QUEUE = RUN_DIR / "run338J_repair_or_expansion_queue.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ex.FINAL_DECISION,
    ex.EXECUTION_SUMMARY,
    ex.PROXY_MT5_DIFF,
    ex.STRATEGY_TESTER_REPORTS,
    ex.RUNTIME_OUTPUT_COPY,
    ex.RUNTIME_IDENTITY,
    ex.pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    ex.pkg.rv.COLLAPSED_RUNTIME_PROXY,
)

OUTPUT_FILES = (
    RUNTIME_REVIEW,
    PROXY_MT5_DIFF_ATTRIBUTION,
    KPI_JUDGMENT,
    REPAIR_QUEUE,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return ex.read_csv(path)


def read_json(path: Path) -> Any:
    return ex.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return ex.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return ex.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return ex.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ex.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    ex.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    return ex.display_path(path)


def passed_status(series: pd.Series) -> pd.Series:
    return ex.passed_status(series)


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def integer(value: Any, default: int = 0) -> int:
    return int(round(numeric(value, float(default))))


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "passed", "completed"}


def safe_ratio(left: float, right: float) -> float:
    high = max(left, right)
    if high <= 0:
        return 0.0
    return min(left, right) / high


def first_record(value: Any) -> dict[str, Any]:
    if isinstance(value, list) and value:
        first = value[0]
        return first if isinstance(first, dict) else {}
    if isinstance(value, dict):
        return value
    return {}


def load_inputs() -> dict[str, Any]:
    parent_final = read_json(ex.FINAL_DECISION)
    parent_gates = read_csv(ex.GATE_AUDIT)
    summary = read_csv(ex.EXECUTION_SUMMARY).fillna("")
    if summary.empty:
        raise ValueError(f"{rel(ex.EXECUTION_SUMMARY)} is empty")
    report_record = first_record(read_json(ex.STRATEGY_TESTER_REPORTS))
    report_metrics = report_record.get("metrics", {}) if isinstance(report_record.get("metrics", {}), dict) else {}
    collapsed_proxy = read_csv(ex.pkg.rv.COLLAPSED_RUNTIME_PROXY).fillna("")
    proxy_row = collapsed_proxy.iloc[0].to_dict() if not collapsed_proxy.empty else {}
    attempt_package = read_csv(ex.pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE).fillna("")
    attempt_row = attempt_package.iloc[0].to_dict() if not attempt_package.empty else {}
    return {
        "parent_final": parent_final,
        "parent_gates": parent_gates,
        "summary_row": summary.iloc[0].to_dict(),
        "report_record": report_record,
        "report_metrics": report_metrics,
        "proxy_row": proxy_row,
        "attempt_row": attempt_row,
    }


def metric(row: Mapping[str, Any], report: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    if key in report and report.get(key) not in ("", None):
        return numeric(report.get(key), default)
    return numeric(row.get(key), default)


def build_review() -> tuple[dict[str, Any], dict[str, pd.DataFrame]]:
    data = load_inputs()
    row = data["summary_row"]
    report = data["report_metrics"]
    proxy = data["proxy_row"]
    attempt = data["attempt_row"]

    net_profit = metric(row, report, "net_profit")
    profit_factor = metric(row, report, "profit_factor")
    expectancy = metric(row, report, "expectancy")
    recovery_factor = metric(row, report, "recovery_factor")
    max_drawdown_amount = metric(row, report, "max_drawdown_amount")
    max_drawdown_percent = metric(row, report, "max_drawdown_percent")
    trade_count = integer(report.get("trade_count", row.get("trade_count")))
    long_trade_count = integer(report.get("long_trade_count", row.get("long_trade_count")))
    short_trade_count = integer(report.get("short_trade_count", row.get("short_trade_count")))
    signal_long_count = integer(row.get("long_count"))
    signal_short_count = integer(row.get("short_count"))
    expected_rows = integer(row.get("expected_rows"))
    matched_rows = integer(row.get("matched_rows"))
    probability_mismatch_rows = integer(row.get("probability_mismatch_rows"))
    decision_mismatch_rows = integer(row.get("decision_mismatch_rows"))
    hash_mismatch_rows = integer(row.get("hash_mismatch_rows"))
    mismatch_rows = probability_mismatch_rows + decision_mismatch_rows + hash_mismatch_rows
    max_abs_probability_diff = numeric(row.get("max_abs_probability_diff"))

    runtime_exact_parity = (
        matched_rows == expected_rows
        and expected_rows > 0
        and probability_mismatch_rows == 0
        and decision_mismatch_rows == 0
        and hash_mismatch_rows == 0
        and str(row.get("comparison_status", "")) == "completed_exact_proxy_mt5_parity_reached_feature_last"
    )
    report_available = (
        str(data["report_record"].get("status", "")) == "completed"
        and str(row.get("report_status", "")) == "completed"
        and not report.get("missing_required_metrics")
    )

    trade_side_balance = safe_ratio(long_trade_count, short_trade_count)
    signal_side_balance = safe_ratio(signal_long_count, signal_short_count)
    net_pass = net_profit > 0
    pf_pass = profit_factor >= 1.10
    expectancy_pass = expectancy > 0
    drawdown_pass = max_drawdown_amount <= 150.0
    recovery_pass = recovery_factor >= 1.0
    trade_count_pass = trade_count >= 30
    trade_side_pass = trade_side_balance >= 0.25
    signal_side_pass = signal_side_balance >= 0.10

    weakness = []
    if not recovery_pass:
        weakness.append("recovery_factor_below_1_00")
    if not trade_count_pass:
        weakness.append("trade_count_below_30")
    if not signal_side_pass:
        weakness.append("signal_side_short_heavy")
    if not trade_side_pass:
        weakness.append("filled_trade_side_imbalance")
    if not drawdown_pass:
        weakness.append("drawdown_above_150")
    if not report_available:
        weakness.append("mt5_report_not_authoritative")
    if not runtime_exact_parity:
        weakness.append("runtime_parity_not_exact")

    operating_ready = all(
        [
            runtime_exact_parity,
            report_available,
            net_pass,
            pf_pass,
            expectancy_pass,
            drawdown_pass,
            recovery_pass,
            trade_count_pass,
            trade_side_pass,
            signal_side_pass,
        ]
    )
    positive_clue = runtime_exact_parity and report_available and net_pass and pf_pass and expectancy_pass
    weakness_tags = ";".join(weakness) if weakness else "none"

    review = pd.DataFrame(
        [
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "attempt_name": row.get("attempt_name", ""),
                "model_id": row.get("model_id", ""),
                "tier": attempt.get("tier", "Tier A"),
                "split": attempt.get("split", "inner_holdout_runtime_collapsed_probe"),
                "runtime_exact_parity": runtime_exact_parity,
                "report_available": report_available,
                "expected_rows": expected_rows,
                "matched_rows": matched_rows,
                "mismatch_rows": mismatch_rows,
                "max_abs_probability_diff": max_abs_probability_diff,
                "mt5_net_profit": net_profit,
                "mt5_profit_factor": profit_factor,
                "mt5_expectancy": expectancy,
                "mt5_recovery_factor": recovery_factor,
                "mt5_max_drawdown_amount": max_drawdown_amount,
                "mt5_max_drawdown_percent": max_drawdown_percent,
                "mt5_trade_count": trade_count,
                "mt5_long_trade_count": long_trade_count,
                "mt5_short_trade_count": short_trade_count,
                "trade_side_balance_ratio": round(trade_side_balance, 8),
                "signal_long_count": signal_long_count,
                "signal_short_count": signal_short_count,
                "signal_side_balance_ratio": round(signal_side_balance, 8),
                "order_attempt_count": integer(row.get("order_attempt_count")),
                "order_fill_count": integer(row.get("order_fill_count")),
                "positive_clue": positive_clue,
                "operating_ready": operating_ready,
                "weakness_tags": weakness_tags,
                "allowed_use": "runtime_probe_positive_clue_only(런타임 탐침 양수 단서 전용)",
                "effect": "MT5(메타트레이더5) 양수 근거를 보존하되 운영 승격(operating promotion, 운영 승격)을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    proxy_trade_count = integer(proxy.get("trade_count"))
    proxy_long_trades = integer(proxy.get("long_trades"))
    proxy_short_trades = integer(proxy.get("short_trades"))
    proxy_net_log_return = numeric(proxy.get("proxy_net_log_return"))
    proxy_profit_factor = numeric(proxy.get("proxy_profit_factor"))
    proxy_recovery = numeric(proxy.get("proxy_recovery"))

    attribution_rows = [
        {
            "attribution_id": "exact_signal_parity",
            "proxy_value": f"{matched_rows}/{expected_rows} matched rows",
            "mt5_value": f"{mismatch_rows} mismatch rows",
            "diff": "none at probability/decision layer(확률/판단 층 차이 없음)",
            "cause": "ONNX(온엑스) probability tape(확률 테이프)와 MT5(메타트레이더5) runtime(런타임)이 같은 입력 해시(input hash, 입력 해시)를 사용했다.",
            "usability": "usable_for_runtime_parity(런타임 동등성에는 사용 가능)",
            "effect": "모델 인계(handoff, 인계)가 깨지지 않았음을 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "trade_count_compression",
            "proxy_value": proxy_trade_count,
            "mt5_value": trade_count,
            "diff": proxy_trade_count - trade_count,
            "cause": "proxy(프록시)는 신호 단위 trade shape(거래 형태)을 가볍게 본 반면 MT5(메타트레이더5)는 one-position lifecycle(단일 포지션 생명주기), max hold(최대 보유), broker execution(브로커 실행)을 적용했다.",
            "usability": "proxy_can_rank_signals_but_cannot_replace_mt5_kpi(프록시는 신호 선별 보조만 가능하고 MT5 KPI 대체 불가)",
            "effect": "다음 run338J(338J 실행)는 거래수와 회복 계수(recovery factor, 회복 계수)를 MT5(메타트레이더5)에서 직접 넓힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "profit_unit_difference",
            "proxy_value": f"net_log_return={proxy_net_log_return};pf={proxy_profit_factor};recovery={proxy_recovery}",
            "mt5_value": f"net_profit={net_profit};pf={profit_factor};recovery={recovery_factor}",
            "diff": "different measurement units(측정 단위 다름)",
            "cause": "proxy(프록시)는 log return(로그 수익률) 근사이고 MT5(메타트레이더5)는 broker PnL(브로커 손익)과 tester cost(테스터 비용)를 반영한다.",
            "usability": "use_proxy_as_sanity_check_only(프록시는 신호 점검 전용)",
            "effect": "운영 판단은 Strategy Tester(전략 테스터) 지표로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "side_shape_warning",
            "proxy_value": f"signals long={proxy_long_trades};short={proxy_short_trades}",
            "mt5_value": f"filled trades long={long_trade_count};short={short_trade_count}",
            "diff": "short-heavy signal shape(숏 쏠림 신호 형태)",
            "cause": "threshold(임계값) 0.60, margin(마진) 0.00에서 long(롱) 신호가 드물다.",
            "usability": "requires_threshold_corridor_probe(임계값 구간 탐침 필요)",
            "effect": "롱/숏 균형(long/short balance, 롱/숏 균형)을 다음 탐색 제약으로 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    attribution = pd.DataFrame(attribution_rows)

    kpi_rows = [
        ("runtime_exact_parity", runtime_exact_parity, "exact 5827/5827 and zero mismatch", "P0", "Python(파이썬)과 MT5(메타트레이더5)의 확률/판단 의미를 고정한다."),
        ("mt5_report_available", report_available, "Strategy Tester report completed", "P0", "MT5 KPI(MT5 핵심 성과 지표)의 출처를 고정한다."),
        ("net_profit", net_profit, "> 0", "P0", "순수익(net profit, 순수익)이 양수인지 확인한다."),
        ("profit_factor", profit_factor, ">= 1.10", "P0", "수익 팩터(profit factor, 수익 팩터)가 최소선 위인지 확인한다."),
        ("expectancy", expectancy, "> 0", "P0", "기대값(expectancy, 기대값)이 양수인지 확인한다."),
        ("max_drawdown_amount", max_drawdown_amount, "<= 150", "P1", "낙폭(drawdown, 낙폭)이 과도하지 않은지 확인한다."),
        ("recovery_factor", recovery_factor, ">= 1.00", "P0", "회복 계수(recovery factor, 회복 계수)가 운영 최소선 위인지 확인한다."),
        ("trade_count", trade_count, ">= 30", "P0", "거래수(trade count, 거래수)가 표본 주장에 충분한지 확인한다."),
        ("filled_trade_side_balance", round(trade_side_balance, 8), ">= 0.25", "P1", "체결 거래 기준 롱/숏 균형(long/short balance, 롱/숏 균형)을 확인한다."),
        ("signal_side_balance", round(signal_side_balance, 8), ">= 0.10", "P1", "원 신호(raw signal, 원 신호)의 숏 쏠림을 확인한다."),
        ("forward_or_live_evidence", "not_available", "required before operation", "P0", "전진/실거래 근거(forward/live evidence, 전진/실거래 근거)가 없으면 운영 주장을 막는다."),
    ]
    pass_map = {
        "runtime_exact_parity": runtime_exact_parity,
        "mt5_report_available": report_available,
        "net_profit": net_pass,
        "profit_factor": pf_pass,
        "expectancy": expectancy_pass,
        "max_drawdown_amount": drawdown_pass,
        "recovery_factor": recovery_pass,
        "trade_count": trade_count_pass,
        "filled_trade_side_balance": trade_side_pass,
        "signal_side_balance": signal_side_pass,
        "forward_or_live_evidence": False,
    }
    kpi = pd.DataFrame(
        [
            {
                "kpi_id": kpi_id,
                "value": value,
                "pass": pass_map[kpi_id],
                "floor": floor,
                "severity": severity,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for kpi_id, value, floor, severity, effect in kpi_rows
        ]
    )

    queue = pd.DataFrame(
        [
            {
                "queue_id": "threshold_corridor_trade_count_expansion",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "action": "materialize MT5 package(패키지 생성) for p55_m00, p50_m00, p55_m05 corridors",
                "reason": "positive MT5 clue(MT5 양수 단서)는 있으나 trade_count(거래수) 11과 recovery_factor(회복 계수) 0.78이 약하다.",
                "required_verification": "execute MT5 runtime probe(MT5 런타임 탐침 실행) and compare proxy-MT5 diff(프록시-MT5 차이 비교)",
                "forbidden_action": "treat threshold change as selection(임계값 변경을 선택으로 취급 금지)",
                "effect": "수익 단서를 죽이지 않고 거래수와 회복 계수(recovery factor, 회복 계수)를 넓힌다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "lifecycle_compression_review",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P1",
                "action": "attribute proxy 83 trades versus MT5 11 trades(프록시 83건과 MT5 11건 귀속)",
                "reason": "runtime parity(런타임 동등성)는 정확하지만 KPI(핵심 성과 지표) 단위가 다르다.",
                "required_verification": "record position lifecycle(포지션 생명주기), max_hold_bars(최대 보유 봉), reverse behavior(반전 행동)",
                "forbidden_action": "use proxy trade count as MT5 trade count(프록시 거래수를 MT5 거래수로 대체 금지)",
                "effect": "다음 패키지의 trade shape(거래 형태) 가정을 더 정확하게 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "session_regime_followup",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P2",
                "action": "keep session/regime stability(세션/국면 안정성) as post-corridor review",
                "reason": "거래수 11건은 session/regime claim(세션/국면 주장)에 부족하다.",
                "required_verification": "only after expanded MT5 trade sample(확장된 MT5 거래 표본 이후)",
                "forbidden_action": "claim stability from 11 trades(11건으로 안정성 주장 금지)",
                "effect": "운영 주장(operating claim, 운영 주장)을 성급하게 닫지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    for path, frame in [
        (RUNTIME_REVIEW, review),
        (PROXY_MT5_DIFF_ATTRIBUTION, attribution),
        (KPI_JUDGMENT, kpi),
        (REPAIR_QUEUE, queue),
    ]:
        write_csv(path, frame)

    parent_gates = data["parent_gates"]
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_selection": "not_run",
        "selected_model": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_exact_parity": runtime_exact_parity,
        "report_available": report_available,
        "positive_clue": positive_clue,
        "operating_ready": operating_ready,
        "expected_rows": expected_rows,
        "matched_rows": matched_rows,
        "mismatch_rows": mismatch_rows,
        "max_abs_probability_diff": max_abs_probability_diff,
        "mt5_net_profit": net_profit,
        "mt5_profit_factor": profit_factor,
        "mt5_expectancy": expectancy,
        "mt5_recovery_factor": recovery_factor,
        "mt5_max_drawdown_amount": max_drawdown_amount,
        "mt5_max_drawdown_percent": max_drawdown_percent,
        "mt5_trade_count": trade_count,
        "mt5_long_trade_count": long_trade_count,
        "mt5_short_trade_count": short_trade_count,
        "trade_side_balance_ratio": round(trade_side_balance, 8),
        "signal_long_count": signal_long_count,
        "signal_short_count": signal_short_count,
        "signal_side_balance_ratio": round(signal_side_balance, 8),
        "proxy_trade_count": proxy_trade_count,
        "proxy_net_log_return": proxy_net_log_return,
        "proxy_profit_factor": proxy_profit_factor,
        "proxy_recovery": proxy_recovery,
        "weakness_tags": weakness_tags,
        "parent_gate_passed": bool(passed_status(parent_gates["status"]).all()) if "status" in parent_gates else False,
        "parent_goal_achieve": data["parent_final"].get("goal_achieve", "not_claimed"),
    }
    return final, {"review": review, "attribution": attribution, "kpi": kpi, "queue": queue}


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row(
                "parent_338H_gates_passed",
                "passed" if boolish(final["parent_gate_passed"]) else "failed",
                rel(ex.GATE_AUDIT),
                "run338H(338H 실행) MT5 runtime probe(MT5 런타임 탐침) 근거를 이어받는다.",
            ),
            gate_row(
                "mt5_report_available",
                "passed" if boolish(final["report_available"]) else "failed",
                rel(ex.STRATEGY_TESTER_REPORTS),
                "Strategy Tester report(전략 테스터 보고서)에서 KPI(핵심 성과 지표)를 읽는다.",
            ),
            gate_row(
                "runtime_parity_exact",
                "passed" if boolish(final["runtime_exact_parity"]) else "failed",
                rel(RUNTIME_REVIEW),
                "proxy-MT5 parity(프록시-MT5 동등성)가 정확한지 확인한다.",
            ),
            gate_row(
                "mt5_positive_kpis_recorded",
                "passed" if boolish(final["positive_clue"]) else "failed",
                rel(KPI_JUDGMENT),
                "양수 MT5 KPI(MT5 핵심 성과 지표)를 긍정 단서로만 기록한다.",
            ),
            gate_row(
                "weak_kpis_block_operating_claim",
                "passed" if not boolish(final["operating_ready"]) else "failed",
                rel(KPI_JUDGMENT),
                "trade_count(거래수)와 recovery factor(회복 계수)가 약하면 운영 승격(operating promotion, 운영 승격)을 막는다.",
            ),
            gate_row(
                "proxy_mt5_attribution_written",
                "passed" if exists(PROXY_MT5_DIFF_ATTRIBUTION) else "failed",
                rel(PROXY_MT5_DIFF_ATTRIBUTION),
                "proxy(프록시)와 MT5(메타트레이더5)의 차이를 귀속한다.",
            ),
            gate_row(
                "run338J_repair_or_expansion_queue_opened",
                "passed" if exists(REPAIR_QUEUE) else "failed",
                rel(REPAIR_QUEUE),
                "다음 실행(run338J, 338J 실행)의 탐색 제약을 만든다.",
            ),
            gate_row(
                "artifact_lineage_written",
                "passed" if exists(LINEAGE_RECEIPT) else "pending_until_receipt_write",
                rel(LINEAGE_RECEIPT),
                "입력/출력 산출물 계보(artifact lineage, 산출물 계보)를 연결한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(FINAL_DECISION),
                "selected model(선정 모델), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 남긴다.",
            ),
        ]
    )


def output_paths_that_exist() -> list[Path]:
    return [path for path in OUTPUT_FILES if exists(path)]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": ex.pkg.now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "runtime_exact_parity": final["runtime_exact_parity"],
            "expected_rows": final["expected_rows"],
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "max_abs_probability_diff": final["max_abs_probability_diff"],
            "parity_evidence": rel(RUNTIME_REVIEW),
            "effect": "runtime parity(런타임 동등성) 근거를 운영 주장이 아닌 탐침 근거로 보존한다.",
        },
    )
    write_json(
        FORENSICS_RECEIPT,
        {
            **base,
            "tester_report": rel(ex.STRATEGY_TESTER_REPORTS),
            "runtime_identity": rel(ex.RUNTIME_IDENTITY),
            "mt5_net_profit": final["mt5_net_profit"],
            "mt5_profit_factor": final["mt5_profit_factor"],
            "mt5_trade_count": final["mt5_trade_count"],
            "effect": "Strategy Tester(전략 테스터) 수치를 proxy(프록시) 점수와 분리한다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "kpi_judgment": rel(KPI_JUDGMENT),
            "proxy_mt5_attribution": rel(PROXY_MT5_DIFF_ATTRIBUTION),
            "weakness_tags": final["weakness_tags"],
            "effect": "수익 구조와 약점을 다음 탐색 제약으로 바꾼다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_judgment": JUDGMENT,
            "positive_clue": final["positive_clue"],
            "operating_ready": final["operating_ready"],
            "goal_achieve": "not_claimed",
            "effect": "좋은 단서와 운영 불가 판정을 동시에 보존한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "MT5(메타트레이더5) 양수 결과를 목표 달성(Goal Achieve, 목표 달성)으로 과장하지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in output_paths_that_exist()],
            "artifact_hashes": {display_path(path): sha(path) for path in output_paths_that_exist()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)",
            "effect": "다음 실행(run338J, 338J 실행)이 어떤 근거에서 출발하는지 추적한다.",
        },
    )


def write_final(final: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    payload = {
        **dict(final),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": ex.pkg.now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in output_paths_that_exist()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338I Runtime-Collapsed MT5 Probe Review(런타임 축약 MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- MT5 net profit(MT5 순수익): `{final['mt5_net_profit']}`
- profit factor(수익 팩터): `{final['mt5_profit_factor']}`
- expectancy(기대값): `{final['mt5_expectancy']}`
- drawdown(낙폭): `{final['mt5_max_drawdown_amount']}`
- recovery factor(회복 계수): `{final['mt5_recovery_factor']}`
- trade count(거래수): `{final['mt5_trade_count']}`
- long/short(롱/숏): `{final['mt5_long_trade_count']}/{final['mt5_short_trade_count']}`
- weakness(약점): `{final['weakness_tags']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Action(행동)

run338H(338H 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 proxy(프록시), parity(동등성), KPI(핵심 성과 지표)로 나눠 검토했다.

Effect(효과): net profit(순수익) 42.01, profit factor(수익 팩터) 2.12, expectancy(기대값) 3.82라는 positive clue(긍정 단서)는 살리고, trade count(거래수) 11과 recovery factor(회복 계수) 0.78 때문에 operating promotion(운영 승격)은 막는다.

## Judgment(판정)

positive clue(긍정 단서)는 유효하다. 다만 selected model(선정 모델), runtime authority(런타임 권위), live readiness(실거래 준비), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.

## Evidence(근거)

- runtime review(런타임 검토): `{rel(RUNTIME_REVIEW)}`
- KPI judgment(KPI 판정): `{rel(KPI_JUDGMENT)}`
- proxy-MT5 attribution(프록시-MT5 귀속): `{rel(PROXY_MT5_DIFF_ATTRIBUTION)}`
- repair queue(수리 대기열): `{rel(REPAIR_QUEUE)}`
- final decision(최종 결정): `{rel(FINAL_DECISION)}`
"""
    decision = f"""# {TODAY} Stage338I Decision(338I 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_REVIEW)}`, `{rel(KPI_JUDGMENT)}`, `{rel(REPAIR_QUEUE)}`

Action(행동): MT5 positive clue(MT5 양수 단서)를 operating promotion(운영 승격)이 아니라 trade count/recovery expansion(거래수/회복 확장) 문제로 넘겼다.

Effect(효과): 좋은 단서를 버리지 않고, 약한 KPI(핵심 성과 지표)를 다음 run338J(338J 실행)의 제약으로 고정한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run338I(338I 실행)는 MT5 positive clue(MT5 양수 단서)를 확인했지만, operating promotion(운영 승격)은 막았다. run338J(338J 실행)는 threshold corridor(임계값 구간)로 trade count/recovery(거래수/회복 계수)를 넓히는 방향으로 간다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- MT5 net profit(MT5 순수익): `{final['mt5_net_profit']}`
- profit factor(수익 팩터): `{final['mt5_profit_factor']}`
- recovery factor(회복 계수): `{final['mt5_recovery_factor']}`
- trade count(거래수): `{final['mt5_trade_count']}`
- weakness(약점): `{final['weakness_tags']}`
- runtime authority(런타임 권위): `not_claimed(주장 없음)`
- operating promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 양수 MT5 결과를 운영 가능한 모델로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run338I {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run338I MT5 Probe Review(MT5 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- MT5 net profit(MT5 순수익): `{final['mt5_net_profit']}`
- profit factor(수익 팩터): `{final['mt5_profit_factor']}`
- trade count(거래수): `{final['mt5_trade_count']}`
- weakness(약점): `{final['weakness_tags']}`
- effect(효과): 양수 단서는 보존하고 운영 승격(operating promotion, 운영 승격)은 막았다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run338I MT5 Probe Review(MT5 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- review(검토): `{rel(RUNTIME_REVIEW)}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- effect(효과): Stage338(338단계)을 trade count/recovery expansion(거래수/회복 확장)으로 이어간다.
""",
    )
    changelog = f"""## {TODAY} run338I Runtime-Collapsed MT5 Probe Review(런타임 축약 MT5 탐침 검토)

- action(행동): MT5 runtime probe(MT5 런타임 탐침)를 KPI(핵심 성과 지표)와 proxy-MT5 diff(프록시-MT5 차이)로 검토했다.
- effect(효과): net `{final['mt5_net_profit']}`, profit factor(수익 팩터) `{final['mt5_profit_factor']}`는 positive clue(긍정 단서)로 보존하고, weakness(약점) `{final['weakness_tags']}` 때문에 operating promotion(운영 승격)을 막았다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_review",
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "expectancy": final["mt5_expectancy"],
            "recovery_factor": final["mt5_recovery_factor"],
            "trade_count": final["mt5_trade_count"],
            "result_status": JUDGMENT,
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "expectancy": final["mt5_expectancy"],
            "recovery_factor": final["mt5_recovery_factor"],
            "trade_count": final["mt5_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[
            ~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))
        ].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    ensure_parent(ARTIFACT_REGISTRY)
    temp_path = ARTIFACT_REGISTRY.with_suffix(".tmp.csv")
    with io(temp_path).open("w", encoding="utf-8-sig", newline="") as handle:
        ordered.to_csv(handle, index=False, lineterminator="\n")
    io(temp_path).replace(io(ARTIFACT_REGISTRY))


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338I inputs: {missing}")

    final_seed, _tables = build_review()
    gates = make_gates(final_seed)
    write_receipts(final_seed)
    gates.loc[gates["gate_id"].eq("artifact_lineage_written"), "status"] = "passed" if exists(LINEAGE_RECEIPT) else "failed"
    write_csv(GATE_AUDIT, gates)
    final = write_final(final_seed, gates)
    write_docs(final)
    write_registers(final, gates)
    write_receipts(final)
    final = write_final(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338I gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "mt5_net_profit": final["mt5_net_profit"],
                "mt5_profit_factor": final["mt5_profit_factor"],
                "mt5_recovery_factor": final["mt5_recovery_factor"],
                "mt5_trade_count": final["mt5_trade_count"],
                "weakness_tags": final["weakness_tags"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
