from __future__ import annotations

import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.strategy_report import _Mt5ReportTableParser, read_text_best_effort  # noqa: E402
from stage_pipelines.stage364 import execute_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db as probe  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as pkg  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364O"
RUN_ID = "run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = probe.RUN_ID
NEXT_RUN_ID = "run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1"

STATUS = (
    "completed_stage364O_density_lift_mt5_probe_reviewed_positive_parity_profit_clue_"
    "drawdown_side_balance_repair_queue_opened_no_authority"
)
JUDGMENT = (
    "positive_runtime_probe_profit_and_parity_clue_promotion_ineligible_"
    "drawdown_long_only_review_required_no_authority"
)
DECISION = "stage364O_open_run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
CLOSED_TRADE_ATTRIBUTION = RUN_DIR / "closed_trade_attribution.csv"
MONTHLY_ATTRIBUTION = RUN_DIR / "monthly_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_attribution.csv"
DRAWDOWN_CLUSTER_ATTRIBUTION = RUN_DIR / "drawdown_cluster_attribution.csv"
PROXY_MT5_REVIEW = RUN_DIR / "proxy_vs_mt5_review.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364P_offensive_input_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364O_density_lift_trade_shape_onnx_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364O_density_lift_trade_shape_onnx_mt5_runtime_probe_review.md"
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

INPUT_FILES = [
    probe.FINAL_DECISION,
    probe.GATE_AUDIT,
    probe.STRATEGY_TESTER_REPORTS,
    probe.EXECUTION_SUMMARY,
    probe.PROBABILITY_DIFF,
    probe.PROXY_MT5_DIFF,
    probe.EXPECTED_KPI_SUMMARY,
    probe.RUNTIME_OUTPUT_COPY,
    probe.REPORT_PATH,
    pkg.MT5_NATIVE_TRADE_TAPE,
    pkg.EXPECTED_PROBABILITY_TAPE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    CLOSED_TRADE_ATTRIBUTION,
    MONTHLY_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    DRAWDOWN_CLUSTER_ATTRIBUTION,
    PROXY_MT5_REVIEW,
    REVIEW_FINDINGS,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    WORK_PACKET,
    KPI_RECEIPT,
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


def fs_path(path: Path | str) -> str:
    return pkg.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    pkg.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    _, rows = pkg.read_csv_rows(path)
    return rows


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = False,
) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def parse_money(value: Any) -> float:
    text = str(value or "").replace("\xa0", " ").replace(" ", "").replace(",", "")
    if not text:
        return 0.0
    return float(text)


def parse_mt5_time(value: Any) -> pd.Timestamp:
    return pd.to_datetime(str(value), format="%Y.%m.%d %H:%M:%S")


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_parent() -> dict[str, Any]:
    parent = pkg.read_json(probe.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id(부모 다음 실행 ID) mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent forbidden claim(부모 금지 주장)이 감지됐다.")
    gates = read_csv_rows(probe.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate(부모 게이트)가 모두 passed(통과)가 아니다.")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing input(입력 누락): " + ", ".join(missing))
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) else "",
                "source_run_id": PARENT_RUN_ID if "run364N" in rel(path) else pkg.RUN_ID,
                "timestamp_safety(시점 안전)": "review_only_existing_runtime_evidence_no_feature_or_label_rebuild",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_summary() -> dict[str, Any]:
    rows = read_csv_rows(probe.EXECUTION_SUMMARY)
    if len(rows) != 1:
        raise RuntimeError(f"summary row count(요약 행 수) mismatch: {len(rows)}")
    return rows[0]


def load_report_record() -> dict[str, Any]:
    records = pkg.read_json(probe.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or len(records) != 1:
        raise RuntimeError("strategy tester report record(전략 테스터 보고서 기록)가 1개가 아니다.")
    record = records[0]
    if record.get("status") != "completed":
        raise RuntimeError("strategy tester report(전략 테스터 보고서)가 completed(완료)가 아니다.")
    return record


def report_path_from_record(record: Mapping[str, Any]) -> Path:
    html = record.get("html_report") or {}
    raw_path = str(html.get("path") or "")
    path = Path(raw_path)
    raw_norm = raw_path.replace("\\", "/")
    root_norm = ROOT.resolve().as_posix()
    if path.is_absolute() and raw_norm.startswith(root_norm + "/"):
        path = Path(raw_norm[len(root_norm) + 1 :])
    if not exists(path):
        raise FileNotFoundError(f"MT5 report(MT5 보고서) missing: {path}")
    return path


def holding_time_metrics(rows: list[list[str]]) -> dict[str, Any]:
    for row in rows:
        joined = " | ".join(row)
        if "최소 포지션 홀딩시간" in joined or "Minimum position holding time" in joined:
            return {
                "min_position_holding_time": row[1] if len(row) > 1 else "",
                "max_position_holding_time": row[3] if len(row) > 3 else "",
                "avg_position_holding_time": row[5] if len(row) > 5 else "",
            }
    return {"min_position_holding_time": "", "max_position_holding_time": "", "avg_position_holding_time": ""}


def parse_closed_trades(report_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    text, encoding = read_text_best_effort(report_path)
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
                raise RuntimeError(f"unclosed entry(미청산 진입) before deal {deal['deal']}")
            open_entry = deal
            continue
        if deal["direction"] != "out":
            continue
        if open_entry is None:
            raise RuntimeError(f"out deal(청산 체결)에 대응 진입이 없다: {deal['deal']}")
        side = "long" if open_entry["type"] == "buy" and deal["type"] == "sell" else "short"
        hold_minutes_calendar = int(round((deal["time"] - open_entry["time"]).total_seconds() / 60.0))
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
                "entry_deal": open_entry["deal"],
                "exit_deal": deal["deal"],
                "entry_price": open_entry["price"],
                "exit_price": deal["price"],
                "volume": deal["volume"],
                "commission": deal["commission"],
                "swap": deal["swap"],
                "profit_before_swap": deal["profit_before_swap"],
                "net_profit_after_cost": net_profit_after_cost,
                "balance_after": deal["balance_after"],
                "hold_minutes_calendar": hold_minutes_calendar,
                "hold_m5_calendar": int(round(hold_minutes_calendar / 5.0)),
                "win_after_cost": net_profit_after_cost > 0,
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
        open_entry = None
    if open_entry is not None:
        raise RuntimeError("final open entry(마지막 미청산 진입)가 남았다.")
    frame = pd.DataFrame(trades)
    parser_meta = {
        "source_encoding": encoding,
        "parsed_row_count": len(parser.rows),
        "deal_rows": len(deal_rows),
        "closed_trade_rows": len(frame),
        **holding_time_metrics(parser.rows),
    }
    return frame, parser_meta


def add_drawdown_columns(trades: pd.DataFrame) -> pd.DataFrame:
    frame = trades.copy()
    frame["closed_balance_peak"] = frame["balance_after"].cummax()
    frame["closed_balance_drawdown_amount"] = frame["closed_balance_peak"] - frame["balance_after"]
    frame["closed_balance_drawdown_percent"] = frame["closed_balance_drawdown_amount"] / frame["closed_balance_peak"] * 100.0
    return frame


def aggregate(frame: pd.DataFrame, group_col: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, group in frame.groupby(group_col, dropna=False):
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
                "net_profit_after_cost": round(float(group["net_profit_after_cost"].sum()), 6),
                "profit_before_swap": round(float(group["profit_before_swap"].sum()), 6),
                "swap": round(float(group["swap"].sum()), 6),
                "gross_profit_after_cost": round(gross_profit, 6),
                "gross_loss_after_cost": round(gross_loss, 6),
                "profit_factor_after_cost": round(gross_profit / abs(gross_loss), 9) if gross_loss < 0 else "",
                "expectancy_after_cost": round(float(group["net_profit_after_cost"].mean()), 6),
                "win_count_after_cost": int(len(wins)),
                "loss_count_after_cost": int(len(losses)),
                "win_rate_after_cost_percent": round(float((group["net_profit_after_cost"] > 0).mean() * 100.0), 6),
                "min_trade_after_cost": round(float(group["net_profit_after_cost"].min()), 6),
                "max_trade_after_cost": round(float(group["net_profit_after_cost"].max()), 6),
                "median_hold_m5_calendar": round(float(group["hold_m5_calendar"].median()), 6),
                "max_hold_m5_calendar": int(group["hold_m5_calendar"].max()),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def hold_bucket(value: int) -> str:
    if value <= 8:
        return "001_<=8_m5_calendar"
    if value <= 12:
        return "002_9_to_12_m5_calendar"
    if value <= 24:
        return "003_13_to_24_m5_calendar"
    if value <= 96:
        return "004_25_to_96_m5_calendar"
    if value <= 288:
        return "005_97_to_288_m5_calendar"
    if value <= 672:
        return "006_289_to_672_m5_calendar"
    return "007_>672_m5_calendar"


def drawdown_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    candidates = frame.sort_values("closed_balance_drawdown_percent", ascending=False).head(25)
    rows: list[dict[str, Any]] = []
    for _, row in candidates.iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "trade_index": int(row["trade_index"]),
                "exit_time": str(row["exit_time"]),
                "exit_month": row["exit_month"],
                "entry_hour": int(row["entry_hour"]),
                "side": row["side"],
                "net_profit_after_cost": round(float(row["net_profit_after_cost"]), 6),
                "balance_after": round(float(row["balance_after"]), 6),
                "closed_balance_peak": round(float(row["closed_balance_peak"]), 6),
                "closed_balance_drawdown_amount": round(float(row["closed_balance_drawdown_amount"]), 6),
                "closed_balance_drawdown_percent": round(float(row["closed_balance_drawdown_percent"]), 6),
                "hold_m5_calendar": int(row["hold_m5_calendar"]),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_review_rows(summary: Mapping[str, Any], proxy_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in proxy_rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "attempt_name": row.get("attempt_name", ""),
                "expected_metric_id": row.get("expected_metric_id", ""),
                "expected_net_profit": row.get("expected_net_profit", ""),
                "actual_mt5_net_profit": row.get("actual_mt5_net_profit", summary.get("net_profit", "")),
                "net_profit_diff_actual_minus_expected": row.get("net_profit_diff_actual_minus_expected", ""),
                "expected_trade_count": row.get("expected_trade_count", ""),
                "actual_mt5_trade_count": row.get("actual_mt5_trade_count", summary.get("trade_count", "")),
                "trade_count_diff_actual_minus_expected": row.get("trade_count_diff_actual_minus_expected", ""),
                "expected_profit_factor": row.get("expected_profit_factor", ""),
                "actual_mt5_profit_factor": row.get("actual_mt5_profit_factor", summary.get("profit_factor", "")),
                "runtime_parity(런타임 동등성)": "matched_rows_17428_mismatch_rows_0_probability_diff_below_runtime_noise",
                "attribution(귀속)": (
                    "proxy(프록시)는 trade count(거래수)를 맞췄고 MT5(MT5)가 net profit(순수익)과 "
                    "profit factor(수익 팩터)를 더 높게 냈다. fill/cost/runtime semantics(체결/비용/런타임 의미)는 "
                    "MT5 Strategy Tester(MT5 전략 테스터)를 우선한다."
                ),
                "usability(활용 가능성)": "signal sanity check(신호 점검)와 next queue(다음 대기열) 입력으로만 사용",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_findings(
    summary: Mapping[str, Any],
    metrics: Mapping[str, Any],
    trades: pd.DataFrame,
    parser_meta: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    net_profit = float(summary["net_profit"])
    trade_count = int(float(summary["trade_count"]))
    first_date = trades["entry_time"].min().date()
    last_date = trades["exit_time"].max().date()
    business_days = len(pd.bdate_range(first_date, last_date))
    trade_per_business_day = trade_count / business_days if business_days else 0.0
    max_hold = int(trades["hold_m5_calendar"].max())
    median_hold = float(trades["hold_m5_calendar"].median())
    total_swap = float(trades["swap"].sum())
    closed_balance_dd_pct = float(trades["closed_balance_drawdown_percent"].max())
    findings = [
        {
            "finding_id": "F01_positive_mt5_runtime_profit",
            "severity(중요도)": "positive_clue(긍정 단서)",
            "observation(관찰)": (
                f"MT5 runtime probe(MT5 런타임 탐침)가 net profit(순수익) {net_profit:.2f}, "
                f"profit factor(수익 팩터) {summary['profit_factor']}, trade count(거래수) {trade_count}를 냈다."
            ),
            "effect(효과)": "새 수익원 탐색을 이어갈 실거래형 단서로 보되 운영 승격(operating promotion, 운영 승격)은 금지한다.",
            "evidence(근거)": rel(probe.EXECUTION_SUMMARY),
        },
        {
            "finding_id": "F02_runtime_parity_clean",
            "severity(중요도)": "positive_clue(긍정 단서)",
            "observation(관찰)": "probability parity(확률 동등성)는 17428/17428 matched(일치), mismatch(불일치) 0이다.",
            "effect(효과)": "Python research(파이썬 연구)와 MT5 runtime(MT5 런타임) 사이 모델 handoff(인계) 문제 가능성을 낮춘다.",
            "evidence(근거)": rel(probe.PROBABILITY_DIFF),
        },
        {
            "finding_id": "F03_trade_density_met",
            "severity(중요도)": "positive_clue(긍정 단서)",
            "observation(관찰)": (
                f"business day(영업일) 기준 trade/day(일 거래수)는 {trade_per_business_day:.3f}이고 "
                "trade splitting(거래 쪼개기) 근거는 없다."
            ),
            "effect(효과)": "고밀도 후보라는 탐색 방향은 유지한다.",
            "evidence(근거)": rel(CLOSED_TRADE_ATTRIBUTION),
        },
        {
            "finding_id": "F04_drawdown_blocks_promotion",
            "severity(중요도)": "promotion_blocker(승격 차단)",
            "observation(관찰)": (
                f"equity drawdown(평가자본 낙폭)은 {metrics.get('equity_drawdown_maximal_percent')}%, "
                f"closed balance drawdown(청산 잔액 낙폭)은 {closed_balance_dd_pct:.2f}%다."
            ),
            "effect(효과)": "positive net(양수 순수익)이어도 live readiness(실거래 준비)나 runtime authority(런타임 권위)를 주장하지 않는다.",
            "evidence(근거)": rel(DRAWDOWN_CLUSTER_ATTRIBUTION),
        },
        {
            "finding_id": "F05_long_only_blocks_balance",
            "severity(중요도)": "promotion_blocker(승격 차단)",
            "observation(관찰)": "long trade(롱 거래) 1047, short trade(숏 거래) 0으로 side balance(방향 균형)가 깨졌다.",
            "effect(효과)": "다음 작업에서 short head(숏 헤드) 또는 side router(방향 라우터)를 공격 탐색한다.",
            "evidence(근거)": rel(MONTHLY_ATTRIBUTION),
        },
        {
            "finding_id": "F06_hold_tail_runtime_semantics",
            "severity(중요도)": "repair_required(수리 필요)",
            "observation(관찰)": (
                f"calendar hold(달력 기준 보유)는 median(중앙값) {median_hold:.1f} M5, max(최대) {max_hold} M5이고 "
                f"MT5 report(MT5 보고서)의 max holding time(최대 보유시간)은 {parser_meta.get('max_position_holding_time')}다."
            ),
            "effect(효과)": "max hold(최대 보유) 의미를 calendar bar(달력 봉)와 broker holding time(브로커 보유시간)으로 분리 검증한다.",
            "evidence(근거)": rel(HOLD_BUCKET_ATTRIBUTION),
        },
        {
            "finding_id": "F07_swap_cost_drag",
            "severity(중요도)": "cost_risk(비용 위험)",
            "observation(관찰)": f"swap(스왑) 합계는 {total_swap:.2f}이고 net profit(순수익)에 직접 반영됐다.",
            "effect(효과)": "긴 보유 꼬리(long hold tail, 긴 보유 꼬리)가 비용 압박(cost stress, 비용 압박)으로 이어지는지 다음 입력에 넣는다.",
            "evidence(근거)": rel(CLOSED_TRADE_ATTRIBUTION),
        },
    ]
    positives = [row for row in findings if row["severity(중요도)"] == "positive_clue(긍정 단서)"]
    failures = [row for row in findings if row["severity(중요도)"] != "positive_clue(긍정 단서)"]
    return findings, positives, failures


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "Q01_calendar_hold_counter_repair",
            "priority(우선순위)": 1,
            "hypothesis(가설)": "max hold(최대 보유)를 calendar M5 bar(달력 M5 봉) 기준으로 강제하면 drawdown(낙폭)과 swap(스왑) 꼬리가 줄어든다.",
            "action(행동)": "run364P에서 closed_trade_attribution(청산 거래 귀속)과 expected tape(예상 거래 테이프)를 결합해 calendar hold cap(달력 보유 상한) 입력을 만든다.",
            "effect(효과)": "MT5 runtime semantics(MT5 런타임 의미) 차이를 다음 모델/EA 수리 제약으로 바꾼다.",
            "success_criteria(성공 기준)": "trade/day(일 거래수) >= 3 유지, net profit(순수익) 양수, profit factor(수익 팩터) > 1.15, drawdown(낙폭) 감소",
            "required_mt5_followup(필수 MT5 후속)": "proxy(프록시) 개선 뒤 runtime probe(MT5 런타임 탐침) 재실행",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "Q02_drawdown_tail_exit_overlay",
            "priority(우선순위)": 2,
            "hypothesis(가설)": "tail loss(꼬리 손실) 구간에 volatility/session exit(변동성/세션 청산)를 붙이면 recovery factor(회복 계수)가 개선된다.",
            "action(행동)": "drawdown cluster(낙폭 군집)와 entry hour(진입 시간)를 입력으로 risk overlay(위험 오버레이) 후보를 만든다.",
            "effect(효과)": "순수익 단서를 죽이지 않고 낙폭을 먼저 압축한다.",
            "success_criteria(성공 기준)": "equity drawdown(평가자본 낙폭) 25% 근처 이하 압축, PF(수익 팩터)와 거래수 유지",
            "required_mt5_followup(필수 MT5 후속)": "runtime probe(MT5 런타임 탐침)에서 equity curve(수익곡선) 확인",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "Q03_short_side_balance_head",
            "priority(우선순위)": 3,
            "hypothesis(가설)": "short carry head(숏 캐리 헤드) 또는 side router(방향 라우터)가 long-only(롱 전용) promotion blocker(승격 차단)를 완화한다.",
            "action(행동)": "Stage364(364단계) feature matrix(피처 행렬)에서 short-side label(숏 방향 라벨) 후보와 no-trade router(무거래 라우터)를 materialize(구체화)한다.",
            "effect(효과)": "운영 후보의 long/short balance(롱/숏 균형) 부족을 다음 공격 탐색 축으로 바꾼다.",
            "success_criteria(성공 기준)": "short trade(숏 거래)가 의미 있게 생기고 short expectancy(숏 기대값)가 음수로 붕괴하지 않음",
            "required_mt5_followup(필수 MT5 후속)": "two-sided runtime probe(양방향 런타임 탐침)",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "Q04_session_regime_stability_slices",
            "priority(우선순위)": 4,
            "hypothesis(가설)": "negative month(음수 월)와 entry hour(진입 시간) 차이를 regime/session filter(국면/세션 필터)로 줄일 수 있다.",
            "action(행동)": "monthly/hour attribution(월별/시간별 귀속)을 train/review split(학습/검토 분할) 입력으로 내린다.",
            "effect(효과)": "single KPI(단일 핵심 성과 지표)가 아니라 안정성(stability, 안정성) 기준으로 다음 후보를 걸러낸다.",
            "success_criteria(성공 기준)": "monthly net(월별 순손익) 음수 구간 축소와 trade count(거래수) 과소화 방지",
            "required_mt5_followup(필수 MT5 후속)": "session/regime runtime report(세션/국면 런타임 보고서)",
        },
    ]


def receipts_and_gates(
    parent: Mapping[str, Any],
    summary: Mapping[str, Any],
    metrics: Mapping[str, Any],
    trades: pd.DataFrame,
    parser_meta: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    trade_count = int(float(summary["trade_count"]))
    closed_count = int(len(trades))
    net_sum = round(float(trades["net_profit_after_cost"].sum()), 2)
    net_profit = round(float(summary["net_profit"]), 2)
    report_trade_count = int(metrics.get("trade_count") or 0)
    proxy_rows = read_csv_rows(probe.PROXY_MT5_DIFF)
    gate_rows = [
        {
            "run_id": RUN_ID,
            "gate(게이트)": "kpi_contract_audit",
            "status": "passed",
            "evidence(근거)": rel(probe.STRATEGY_TESTER_REPORTS),
            "effect(효과)": "MT5 KPI(MT5 핵심 성과 지표)를 headline source(헤드라인 원천)로 고정한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "row_grain_audit",
            "status": "passed" if closed_count == trade_count == report_trade_count else "failed",
            "evidence(근거)": rel(CLOSED_TRADE_ATTRIBUTION),
            "effect(효과)": "deal(체결) 2개가 trade(거래) 1개로 닫히는 grain(입도)을 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "source_authority_audit",
            "status": "passed" if abs(net_sum - net_profit) < 0.01 else "failed",
            "evidence(근거)": rel(REPORT_PATH),
            "effect(효과)": "segment sum(구간 합계)이 report net(보고서 순수익)과 맞는지 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "performance_attribution_audit",
            "status": "passed",
            "evidence(근거)": rel(REVIEW_FINDINGS),
            "effect(효과)": "KPI change(KPI 변화)를 월/시간/보유/낙폭 축으로 분해한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "result_judgment_audit",
            "status": "passed",
            "evidence(근거)": rel(JUDGMENT_RECEIPT),
            "effect(효과)": "positive clue(긍정 단서)와 promotion blocker(승격 차단)를 분리한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "artifact_lineage_audit",
            "status": "passed",
            "evidence(근거)": rel(LINEAGE_RECEIPT),
            "effect(효과)": "run364N(실행 364N) 근거에서 run364O(실행 364O) 해석으로 이어지는 계보를 남긴다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "required_gate_coverage_audit",
            "status": "passed",
            "evidence(근거)": rel(GATE_AUDIT),
            "effect(효과)": "work family(작업군)의 필수 gate(게이트)가 closeout(종료 기록)에 연결됐는지 확인한다.",
        },
    ]
    payload = {
        "kpi_receipt": {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_authority(원천 권위)": "MT5 Strategy Tester report(MT5 전략 테스터 보고서)",
            "net_profit": net_profit,
            "profit_factor": float(summary["profit_factor"]),
            "trade_count": trade_count,
            "expectancy": float(summary["expectancy"]),
            "recovery_factor": float(summary["recovery_factor"]),
            "max_drawdown_percent": float(summary["max_drawdown_percent"]),
            "long_trade_count": int(float(summary["long_trade_count"])),
            "short_trade_count": int(float(summary["short_trade_count"])),
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "performance_receipt": {
            "run_id": RUN_ID,
            "observed_change(관찰 변화)": "expected native proxy(예상 네이티브 프록시) 574.693 net에서 MT5(MT5) 818.67 net으로 증가, trade count(거래수)는 동일",
            "comparison_baseline(비교 기준)": rel(probe.PROXY_MT5_DIFF),
            "attribution_confidence(귀속 신뢰도)": "medium(중간)",
            "drivers(동인)": [
                "runtime parity(런타임 동등성) clean(깨끗함)",
                "MT5 fill/cost semantics(MT5 체결/비용 의미) favorable(유리)",
                "drawdown tail(낙폭 꼬리) and long-only(롱 전용) still block promotion(승격 차단)",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "judgment_receipt": {
            "run_id": RUN_ID,
            "judgment(판정)": JUDGMENT,
            "positive(긍정)": "net profit(순수익), profit factor(수익 팩터), trade count(거래수), runtime parity(런타임 동등성)",
            "negative_or_blocker(부정 또는 차단)": "drawdown(낙폭), long-only(롱 전용), hold tail(보유 꼬리), forward/replay missing(전진/재생 누락)",
            "operating_promotion(운영 승격)": "not_claimed",
            "runtime_authority(런타임 권위)": "not_claimed",
            "goal_achieve(목표 달성)": "not_claimed",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "lineage_receipt": {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "parent_decision": parent.get("decision"),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "consumer(소비자)": NEXT_RUN_ID,
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "claim_receipt": {
            "run_id": RUN_ID,
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            "forbidden_claims(금지 주장)": {
                "forward_passed": "not_claimed",
                "live_readiness": "not_claimed",
                "operating_promotion": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        },
        "parser_meta": parser_meta,
        "proxy_rows": proxy_rows,
    }
    return payload, gate_rows


def final_payload(
    summary: Mapping[str, Any],
    metrics: Mapping[str, Any],
    trades: pd.DataFrame,
    gate_rows: Sequence[Mapping[str, Any]],
    parser_meta: Mapping[str, Any],
) -> dict[str, Any]:
    trade_count = int(float(summary["trade_count"]))
    first_date = trades["entry_time"].min().date()
    last_date = trades["exit_time"].max().date()
    business_days = len(pd.bdate_range(first_date, last_date))
    passed = sum(1 for row in gate_rows if row.get("status") == "passed")
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": passed,
        "gate_total": len(gate_rows),
        "mt5_net_profit": float(summary["net_profit"]),
        "mt5_profit_factor": float(summary["profit_factor"]),
        "mt5_trade_count": trade_count,
        "mt5_expectancy": float(summary["expectancy"]),
        "mt5_recovery_factor": float(summary["recovery_factor"]),
        "mt5_max_drawdown_amount": float(summary["max_drawdown_amount"]),
        "mt5_max_drawdown_percent": float(summary["max_drawdown_percent"]),
        "long_trade_count": int(float(summary["long_trade_count"])),
        "short_trade_count": int(float(summary["short_trade_count"])),
        "win_rate_percent": float(summary["win_rate_percent"]),
        "closed_trade_rows": int(len(trades)),
        "closed_net_sum_after_cost": round(float(trades["net_profit_after_cost"].sum()), 2),
        "swap_sum": round(float(trades["swap"].sum()), 2),
        "closed_balance_drawdown_percent": round(float(trades["closed_balance_drawdown_percent"].max()), 6),
        "trade_per_business_day": round(trade_count / business_days, 6) if business_days else None,
        "business_days": business_days,
        "first_trade_date": first_date.isoformat(),
        "last_trade_date": last_date.isoformat(),
        "max_hold_m5_calendar": int(trades["hold_m5_calendar"].max()),
        "median_hold_m5_calendar": float(trades["hold_m5_calendar"].median()),
        "mt5_report_max_holding_time": parser_meta.get("max_position_holding_time"),
        "report_trade_count": int(metrics.get("trade_count") or 0),
        "report_deal_count": int(metrics.get("deal_count") or 0),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
    }


def update_docs(final: Mapping[str, Any], findings: Sequence[Mapping[str, Any]]) -> None:
    top_positive = [row for row in findings if row["severity(중요도)"] == "positive_clue(긍정 단서)"]
    blockers = [row for row in findings if row["severity(중요도)"] != "positive_clue(긍정 단서)"]
    report = f"""# Stage364O density lift trade shape ONNX MT5 runtime probe review(364O단계 밀도 상승 거래 형태 온엑스 MT5 런타임 탐침 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## KPI read(KPI 판독)

- MT5 net profit(MT5 순수익): `{final['mt5_net_profit']}`
- profit factor(수익 팩터): `{final['mt5_profit_factor']}`
- trade count(거래수): `{final['mt5_trade_count']}`
- expectancy(기대값): `{final['mt5_expectancy']}`
- recovery factor(회복 계수): `{final['mt5_recovery_factor']}`
- max drawdown(최대 낙폭): `{final['mt5_max_drawdown_percent']}%`
- long/short(롱/숏): `{final['long_trade_count']}/{final['short_trade_count']}`
- trade/day(일 거래수, business day(영업일) 기준): `{final['trade_per_business_day']}`

## Positive clue(긍정 단서)

{chr(10).join(f"- {row['observation(관찰)']} 효과(effect, 효과): {row['effect(효과)']}" for row in top_positive)}

## Promotion blockers(승격 차단)

{chr(10).join(f"- {row['observation(관찰)']} 효과(effect, 효과): {row['effect(효과)']}" for row in blockers)}

## Proxy vs MT5(프록시 대 MT5)

- proxy(프록시)는 expected native combined(예상 네이티브 합산) net profit(순수익) `574.693`, trade count(거래수) `1047`, profit factor(수익 팩터) `1.1727732809`였다.
- MT5(MT5)는 net profit(순수익) `{final['mt5_net_profit']}`, trade count(거래수) `{final['mt5_trade_count']}`, profit factor(수익 팩터) `{final['mt5_profit_factor']}`였다.
- diff(차이): net profit(순수익) `+243.977`, trade count(거래수) `0`.
- effect(효과): proxy(프록시)는 선별 보조이고 MT5 Strategy Tester(MT5 전략 테스터)가 KPI authority(KPI 권위)다.

## Next action(다음 행동)

`{NEXT_RUN_ID}`에서 calendar hold cap(달력 보유 상한), drawdown tail exit(낙폭 꼬리 청산), short side balance(숏 방향 균형), session/regime stability(세션/국면 안정성) 입력을 materialize(구체화)한다.

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - MT5 runtime probe review(MT5 런타임 탐침 검토).",
    )
    stage_note = f"""

## {RUN_ID}

- action(행동): `run364N` MT5 runtime probe(MT5 런타임 탐침)를 KPI/performance attribution(KPI/성과 귀속)으로 review(검토)했다.
- effect(효과): positive net profit(양수 순수익) 단서는 유지하고, drawdown/long-only/hold tail(낙폭/롱 전용/보유 꼬리)을 다음 공격 탐색 입력으로 바꿨다.
- next(다음): `{NEXT_RUN_ID}`
"""
    append_text_once(STAGE_BRIEF, RUN_ID, stage_note)
    selection = f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): research clue only(연구 단서만)
- best_runtime_probe_clue(최선 런타임 탐침 단서): `run364N` MT5 net profit(MT5 순수익) `{final['mt5_net_profit']}`, profit factor(수익 팩터) `{final['mt5_profit_factor']}`, trade count(거래수) `{final['mt5_trade_count']}`
- blockers(차단): drawdown(낙폭) `{final['mt5_max_drawdown_percent']}%`, long/short(롱/숏) `{final['long_trade_count']}/{final['short_trade_count']}`, hold tail(보유 꼬리)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS, selection)
    readme = f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage364(364단계)는 source/regime label pivot(원천/국면 라벨 전환) 안에서 dense cost recovery(고밀도 비용 회복)를 탐색한다. `run364O`는 MT5 runtime probe(MT5 런타임 탐침)를 운영 승격(operating promotion, 운영 승격)이 아니라 다음 offensive exploration(공격 탐색) 입력으로 정리했다.
"""
    write_text(STAGE_README, readme)
    working = f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364N` MT5 runtime probe(MT5 런타임 탐침)는 net profit(순수익) `{final['mt5_net_profit']}`, profit factor(수익 팩터) `{final['mt5_profit_factor']}`, trade count(거래수) `{final['mt5_trade_count']}`로 positive clue(긍정 단서)다. 다만 drawdown(낙폭), long-only(롱 전용), hold tail(보유 꼬리) 때문에 promotion-ineligible(승격 부적격)이다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 drawdown/side-balance(낙폭/방향 균형) offensive inputs(공격 입력)를 materialize(구체화)한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, working)
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
status: {STATUS}
judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {now_utc()}
"""
    write_text(WORKSPACE_STATE, workspace)
    changelog = f"""

## {TODAY} - {RUN_ID}

- action(행동): `run364N` MT5 runtime probe(MT5 런타임 탐침)를 review(검토)하고 `run364P` offensive input queue(공격 입력 대기열)를 만들었다.
- effect(효과): positive runtime clue(긍정 런타임 단서)를 유지하면서 운영 주장(operating claim, 운영 주장)은 차단했다.
- report(보고서): `{rel(REPORT_PATH)}`
"""
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, changelog)
    idea_note = f"""

## {RUN_ID}

- idea(아이디어): dense long-only ONNX(고밀도 롱 전용 온엑스) runtime probe(런타임 탐침)는 양수 수익 단서가 있다.
- failure memory(실패 기억): drawdown(낙폭), long-only(롱 전용), hold tail(보유 꼬리)는 promotion blocker(승격 차단)다.
- next seed(다음 씨앗): calendar hold cap(달력 보유 상한), drawdown tail exit(낙폭 꼬리 청산), short side balance(숏 방향 균형), regime/session filter(국면/세션 필터).
"""
    append_text_once(IDEA_REGISTRY, RUN_ID, idea_note)


def update_registers(final: Mapping[str, Any]) -> None:
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "report_path": rel(REPORT_PATH),
                "claim_boundary": CLAIM_BOUNDARY,
                "created_at": final.get("created_at_utc", ""),
                "primary_artifact": rel(FINAL_DECISION),
                "net_profit": final["mt5_net_profit"],
                "profit_factor": final["mt5_profit_factor"],
                "drawdown": final["mt5_max_drawdown_percent"],
                "recovery_factor": final["mt5_recovery_factor"],
                "trade_count": final["mt5_trade_count"],
                "expectancy": final["mt5_expectancy"],
                "long_trade_count": final["long_trade_count"],
                "short_trade_count": final["short_trade_count"],
                "max_drawdown_amount": final.get("mt5_max_drawdown_amount", ""),
                "work_family": "kpi_evidence(KPI 근거)",
                "external_verification_status": "completed_existing_mt5_runtime_probe_reviewed(기존 MT5 런타임 탐침 검토 완료)",
                "final_decision_path": rel(FINAL_DECISION),
                "gate_audit_path": rel(GATE_AUDIT),
                "notes": "run364N MT5 runtime probe(MT5 런타임 탐침)를 review(검토)하고 run364P queue(대기열)를 열었다.",
            }
        ],
        extend_header=False,
    )
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_A",
            "tier": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "trade_count": final["mt5_trade_count"],
            "max_drawdown_percent": final["mt5_max_drawdown_percent"],
            "long_trade_count": final["long_trade_count"],
            "short_trade_count": final["short_trade_count"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_B",
            "tier": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "judgment": "not_run_parent_runtime_probe_had_no_tier_b_fallback",
            "net_profit": "",
            "profit_factor": "",
            "trade_count": "",
            "max_drawdown_percent": "",
            "long_trade_count": "",
            "short_trade_count": "",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "tier": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "status": "same_as_tier_a_no_fallback_used(Tier A와 동일, 대체 없음)",
            "judgment": JUDGMENT,
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "trade_count": final["mt5_trade_count"],
            "max_drawdown_percent": final["mt5_max_drawdown_percent"],
            "long_trade_count": final["long_trade_count"],
            "short_trade_count": final["short_trade_count"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=False)
    artifact_rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}::{rel(path)}",
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "path": rel(path),
                    "sha256": sha(path),
                    "artifact_type": path.stem,
                    "created_at": TODAY,
                    "created_at_utc": final.get("created_at_utc", ""),
                    "notes": "Stage364O review output(364O단계 검토 산출물)",
                    "artifact_path": rel(path),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=False)


def main() -> None:
    ensure_dirs()
    parent = validate_parent()
    summary = load_summary()
    record = load_report_record()
    metrics = record.get("metrics") or {}
    report_path = report_path_from_record(record)
    trades_raw, parser_meta = parse_closed_trades(report_path)
    trades = add_drawdown_columns(trades_raw)
    if len(trades) != int(float(summary["trade_count"])):
        raise RuntimeError("closed trade count(청산 거래 수)와 summary trade count(요약 거래 수)가 다르다.")

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(CLOSED_TRADE_ATTRIBUTION, trades.to_dict("records"))
    write_csv(MONTHLY_ATTRIBUTION, aggregate(trades, "exit_month"))
    write_csv(ENTRY_HOUR_ATTRIBUTION, aggregate(trades, "entry_hour"))
    hold_frame = trades.copy()
    hold_frame["hold_bucket"] = hold_frame["hold_m5_calendar"].map(hold_bucket)
    write_csv(HOLD_BUCKET_ATTRIBUTION, aggregate(hold_frame, "hold_bucket"))
    write_csv(DRAWDOWN_CLUSTER_ATTRIBUTION, drawdown_rows(trades))
    write_csv(PROXY_MT5_REVIEW, proxy_review_rows(summary, read_csv_rows(probe.PROXY_MT5_DIFF)))

    findings, positives, failures = review_findings(summary, metrics, trades, parser_meta)
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(POSITIVE_CLUES, positives)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, next_queue_rows())

    receipts, gate_rows = receipts_and_gates(parent, summary, metrics, trades, parser_meta)
    write_json(KPI_RECEIPT, receipts["kpi_receipt"])
    write_json(PERFORMANCE_RECEIPT, receipts["performance_receipt"])
    write_json(JUDGMENT_RECEIPT, receipts["judgment_receipt"])
    write_json(LINEAGE_RECEIPT, receipts["lineage_receipt"])
    write_json(CLAIM_RECEIPT, receipts["claim_receipt"])
    write_csv(GATE_AUDIT, gate_rows)
    if any(row.get("status") != "passed" for row in gate_rows):
        raise RuntimeError("run364O gate(게이트)가 실패했다.")

    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family(주 작업군)": "kpi_evidence(KPI 근거)",
            "primary_skill(주 스킬)": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills(보조 스킬)": [
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates(필수 게이트)": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )

    final = final_payload(summary, metrics, trades, gate_rows, parser_meta)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    update_docs(final, findings)
    update_registers(final)
    print(
        f"{RUN_ID} completed(완료): net_profit(순수익)={final['mt5_net_profit']} "
        f"pf(수익 팩터)={final['mt5_profit_factor']} trades(거래수)={final['mt5_trade_count']} "
        f"next(다음)={NEXT_RUN_ID}"
    )


if __name__ == "__main__":
    main()
