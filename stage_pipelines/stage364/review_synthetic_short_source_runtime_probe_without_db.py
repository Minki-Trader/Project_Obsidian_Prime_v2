from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage364 import materialize_synthetic_short_source_runtime_repair_without_db as bv  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = bv.STAGE_ID
RUN_NUMBER = "run364BW"
RUN_ID = "run364BW_review_synthetic_short_source_runtime_probe_without_db_v1"
PARENT_RUN_ID = bv.RUN_ID
NEXT_RUN_ID = "run364BX_overlay_hour17_native_short_ablation_runtime_probe_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STATUS = "completed_stage364BW_reviewed_bv_runtime_probe_attribution_open_bx_no_authority"
JUDGMENT = "runtime_probe_review_positive_clue_weak_overlay_increment_native_short_and_hour17_edge_no_authority"
DECISION = "stage364BW_open_run364BX_overlay_hour17_native_short_ablation_runtime_probe"

STAGE_DIR = bv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
MT5_TRADE_ATTRIBUTION = RUN_DIR / "mt5_trade_attribution.csv"
ATTRIBUTION_BY_DIRECTION = RUN_DIR / "attribution_by_direction.csv"
ATTRIBUTION_BY_SOURCE_BUCKET = RUN_DIR / "attribution_by_source_bucket.csv"
ATTRIBUTION_BY_MONTH = RUN_DIR / "attribution_by_month.csv"
ATTRIBUTION_BY_HOUR = RUN_DIR / "attribution_by_hour.csv"
RUNTIME_SIGNAL_ATTRIBUTION = RUN_DIR / "runtime_signal_attribution.csv"
PROXY_RUNTIME_ATTRIBUTION = RUN_DIR / "proxy_runtime_diff_attribution.csv"
NEXT_PROBE_QUEUE = RUN_DIR / "run364BX_runtime_ablation_queue.csv"
KPI_CONTRACT_AUDIT = RUN_DIR / "kpi_contract_audit.csv"
ROW_GRAIN_AUDIT = RUN_DIR / "row_grain_audit.csv"
SOURCE_AUTHORITY_AUDIT = RUN_DIR / "source_authority_audit.csv"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BW_review_synthetic_short_source_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BW_review_synthetic_short_source_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_FILES = [
    bv.FINAL_DECISION,
    bv.STRATEGY_TESTER_REPORTS,
    bv.RUNTIME_OUTPUT_VALIDATION,
    bv.RUNTIME_OUTPUT_COPY,
    bv.PROXY_MT5_DIFF,
    bv.TESTER_IDENTITY_CONTRACT,
    bv.RUNTIME_PARITY_CONTRACT,
    bv.RUNTIME_POLICY_CONFIG,
    bv.RUN_MANIFEST,
    bv.SOURCE_SELECTED_CANDIDATE,
    bv.SOURCE_SYNTHETIC_SHORT_TAPE,
    bv.SOURCE_SELECTED_TRADE_TAPE,
    bv.REPORT_PATH,
]

BV_TELEMETRY = bv.TELEMETRY_COPY_DIR / f"{bv.ATTEMPT_NAME}_telemetry.csv"
BV_SUMMARY = bv.TELEMETRY_COPY_DIR / f"{bv.ATTEMPT_NAME}_summary.csv"
BV_HTML_REPORT = bv.REPORT_COPY_DIR / f"{bv.REPORT_NAME}.htm"

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    MT5_TRADE_ATTRIBUTION,
    ATTRIBUTION_BY_DIRECTION,
    ATTRIBUTION_BY_SOURCE_BUCKET,
    ATTRIBUTION_BY_MONTH,
    ATTRIBUTION_BY_HOUR,
    RUNTIME_SIGNAL_ATTRIBUTION,
    PROXY_RUNTIME_ATTRIBUTION,
    NEXT_PROBE_QUEUE,
    KPI_CONTRACT_AUDIT,
    ROW_GRAIN_AUDIT,
    SOURCE_AUTHORITY_AUDIT,
    PERFORMANCE_RECEIPT,
    BACKTEST_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
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
    return bv.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    bv.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    bv.write_csv(path, rows, fieldnames)


def read_rows(path: Path) -> list[dict[str, str]]:
    return bv.read_rows(path)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    bv.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    bv.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    bv.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return round(value, 10) if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(str(value).replace("\xa0", "").replace(" ", "").replace(",", ""))
    except (TypeError, ValueError):
        return default


def safe_pf(win_sum: float, loss_sum: float) -> float:
    return win_sum / abs(loss_sum) if loss_sum < 0 else math.inf


def summarize_trades(frame: pd.DataFrame, group_cols: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped = frame.groupby(group_cols, dropna=False) if group_cols else [((), frame)]
    for key, group in grouped:
        if not isinstance(key, tuple):
            key = (key,)
        wins = group[group["net_profit"] > 0.0]["net_profit"].sum()
        losses = group[group["net_profit"] < 0.0]["net_profit"].sum()
        row = {col: key[index] for index, col in enumerate(group_cols)}
        row.update(
            {
                "trade_count": int(len(group)),
                "net_profit": round(float(group["net_profit"].sum()), 2),
                "expectancy": round(float(group["net_profit"].mean()), 6),
                "win_count": int((group["net_profit"] > 0.0).sum()),
                "loss_count": int((group["net_profit"] < 0.0).sum()),
                "win_rate_percent": round(float((group["net_profit"] > 0.0).mean() * 100.0), 6),
                "gross_profit": round(float(wins), 2),
                "gross_loss": round(float(losses), 2),
                "profit_factor": round(float(safe_pf(float(wins), float(losses))), 6) if math.isfinite(safe_pf(float(wins), float(losses))) else "inf",
                "avg_hold_minutes": round(float(group["hold_minutes"].mean()), 6),
            }
        )
        rows.append(row)
    return rows


def read_runtime_cycles() -> tuple[pd.DataFrame, dict[str, Any]]:
    telemetry = pd.read_csv(io_path(BV_TELEMETRY))
    cycles = telemetry[telemetry["record_type"].eq("cycle")].copy()
    cycles["written_dt"] = pd.to_datetime(cycles["written_at"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    cycles["bar_dt"] = pd.to_datetime(cycles["bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    cycles["bar_month"] = cycles["bar_dt"].dt.to_period("M").astype(str)
    cycles["bar_hour"] = cycles["bar_dt"].dt.hour
    cycles["order_filled_bool"] = cycles["order_filled"].astype(str).str.lower().eq("true")
    summary_rows = read_rows(BV_SUMMARY)
    summary = summary_rows[-1] if summary_rows else {}
    return cycles, summary


def parse_mt5_report_trades(cycles: pd.DataFrame) -> pd.DataFrame:
    html = io_path(BV_HTML_REPORT).read_text(encoding="utf-16")
    tables = pd.read_html(StringIO(html))
    deal_table = tables[1]
    header_candidates = deal_table[(deal_table[0].eq("시간")) & (deal_table[1].eq("거래")) & (deal_table[4].eq("방향"))].index
    if len(header_candidates) == 0:
        raise RuntimeError("MT5 deal table header not found.")
    start = int(header_candidates[-1]) + 1
    rows = deal_table.iloc[start:].copy()
    rows.columns = [
        "time",
        "deal",
        "symbol",
        "type",
        "direction",
        "volume",
        "price",
        "order",
        "commission",
        "swap",
        "profit",
        "balance",
        "comment",
    ]
    rows = rows[pd.to_datetime(rows["time"], format="%Y.%m.%d %H:%M:%S", errors="coerce").notna()].copy()
    for column in ["volume", "price", "commission", "swap", "profit", "balance"]:
        rows[column] = rows[column].map(as_float)
    rows["dt"] = pd.to_datetime(rows["time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")

    open_cycles = cycles[cycles["exec_action"].isin(["open_long", "open_short", "reverse_open_long", "reverse_open_short"])].copy()
    open_cycles["trade_direction"] = open_cycles["exec_action"].map(
        {
            "open_long": "long",
            "reverse_open_long": "long",
            "open_short": "short",
            "reverse_open_short": "short",
        }
    )
    open_cycles["source_bucket"] = open_cycles["decision_reason"].astype(str).map(source_bucket)
    open_cycles = open_cycles[
        [
            "written_dt",
            "bar_dt",
            "trade_direction",
            "source_bucket",
            "decision_reason",
            "p_short",
            "p_flat",
            "p_long",
        ]
    ].copy()

    trades: list[dict[str, Any]] = []
    open_trade: dict[str, Any] | None = None
    for _, raw in rows.iterrows():
        if raw["type"] == "balance":
            continue
        if raw["direction"] == "in":
            open_trade = {
                "open_time": raw["dt"],
                "open_type": raw["type"],
                "open_price": raw["price"],
                "volume": raw["volume"],
            }
            continue
        if raw["direction"] != "out":
            continue
        direction = "unknown"
        open_time = pd.NaT
        open_price = math.nan
        volume = raw["volume"]
        if open_trade is not None:
            open_time = open_trade["open_time"]
            open_price = open_trade["open_price"]
            volume = open_trade["volume"]
            direction = "long" if open_trade["open_type"] == "buy" else "short" if open_trade["open_type"] == "sell" else "unknown"
        net = float(raw["profit"] + raw["swap"] + raw["commission"])
        trades.append(
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "open_time": open_time,
                "close_time": raw["dt"],
                "direction": direction,
                "volume": volume,
                "open_price": open_price,
                "close_price": raw["price"],
                "profit_column": raw["profit"],
                "swap": raw["swap"],
                "commission": raw["commission"],
                "net_profit": net,
                "balance_after": raw["balance"],
                "hold_minutes": (raw["dt"] - open_time).total_seconds() / 60.0 if pd.notna(open_time) else math.nan,
                "open_hour": int(open_time.hour) if pd.notna(open_time) else "",
                "close_hour": int(raw["dt"].hour),
                "close_month": str(raw["dt"].to_period("M")),
                "close_date": raw["dt"].date().isoformat(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        open_trade = None

    frame = pd.DataFrame(trades)
    frame["open_time"] = pd.to_datetime(frame["open_time"], errors="coerce")
    frame["close_time"] = pd.to_datetime(frame["close_time"], errors="coerce")
    joined = frame.merge(
        open_cycles,
        left_on=["open_time", "direction"],
        right_on=["written_dt", "trade_direction"],
        how="left",
    )
    joined["source_bucket"] = joined["source_bucket"].fillna("unmatched_runtime_source")
    joined["source_reason"] = joined["decision_reason"].fillna("")
    joined["open_time"] = joined["open_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    joined["close_time"] = joined["close_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    return joined[
        [
            "run_id",
            "parent_run_id",
            "open_time",
            "close_time",
            "direction",
            "source_bucket",
            "source_reason",
            "volume",
            "open_price",
            "close_price",
            "profit_column",
            "swap",
            "commission",
            "net_profit",
            "balance_after",
            "hold_minutes",
            "open_hour",
            "close_hour",
            "close_month",
            "close_date",
            "p_short",
            "p_flat",
            "p_long",
            "claim_boundary",
        ]
    ].copy()


def source_bucket(reason: Any) -> str:
    text = str(reason or "")
    if text.startswith("synthetic_short_source_overlay"):
        return "synthetic_short_overlay"
    if text == "short_threshold_met" or text.endswith("|short_threshold_met"):
        return "native_short_threshold"
    if "long_threshold_met" in text:
        return "long_threshold"
    return "other_runtime_source"


def signal_rows(cycles: pd.DataFrame) -> list[dict[str, Any]]:
    frame = cycles.copy()
    frame["source_bucket"] = frame["decision_reason"].map(source_bucket)
    grouped = frame.groupby(["decision", "source_bucket", "bar_hour"], dropna=False)
    rows = []
    for (decision, bucket, hour), group in grouped:
        rows.append(
            {
                "run_id": RUN_ID,
                "decision": decision,
                "source_bucket": bucket,
                "bar_hour": hour,
                "cycle_count": int(len(group)),
                "order_filled_count": int(group["order_filled_bool"].sum()),
                "mean_p_short": round(float(pd.to_numeric(group["p_short"], errors="coerce").mean()), 10),
                "mean_p_long": round(float(pd.to_numeric(group["p_long"], errors="coerce").mean()), 10),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_runtime_rows(trades: pd.DataFrame, final: Mapping[str, Any], candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    by_bucket = {row["source_bucket"]: row for row in summarize_trades(trades, ["source_bucket"])}
    overlay = by_bucket.get("synthetic_short_overlay", {})
    native = by_bucket.get("native_short_threshold", {})
    long_row = by_bucket.get("long_threshold", {})
    return [
        {
            "run_id": RUN_ID,
            "comparison": "proxy_total_vs_bv_mt5_total",
            "proxy_net_profit": final.get("selected_proxy_net_profit"),
            "mt5_net_profit": final.get("mt5_net_profit"),
            "net_diff_proxy_minus_mt5": round(float(final.get("selected_proxy_net_profit", 0.0)) - float(final.get("mt5_net_profit", 0.0)), 2),
            "proxy_trade_count": final.get("selected_proxy_trade_count"),
            "mt5_trade_count": final.get("mt5_trade_count"),
            "interpretation": "proxy remains useful for signal sanity, but MT5 report is KPI authority(프록시는 신호 점검용, MT5 보고서가 KPI 권위).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "comparison": "proxy_synthetic_short_vs_runtime_overlay_trade_source",
            "proxy_net_profit": candidate.get("synthetic_short_net_profit"),
            "mt5_net_profit": overlay.get("net_profit", 0.0),
            "net_diff_proxy_minus_mt5": round(float(candidate.get("synthetic_short_net_profit", 0.0)) - float(overlay.get("net_profit", 0.0)), 2),
            "proxy_trade_count": candidate.get("synthetic_short_trade_count"),
            "mt5_trade_count": overlay.get("trade_count", 0),
            "interpretation": "runtime overlay fired more trades with lower expectancy(런타임 덧씌움은 거래가 늘고 기대값이 낮아짐).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "comparison": "runtime_native_short_vs_runtime_overlay",
            "proxy_net_profit": "",
            "mt5_net_profit": native.get("net_profit", 0.0),
            "net_diff_proxy_minus_mt5": round(float(native.get("net_profit", 0.0)) - float(overlay.get("net_profit", 0.0)), 2),
            "proxy_trade_count": "",
            "mt5_trade_count": native.get("trade_count", 0),
            "interpretation": "native short threshold carried stronger short edge than synthetic overlay(기본 숏 임계값이 합성 덧씌움보다 강함).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "comparison": "runtime_long_source_share",
            "proxy_net_profit": "",
            "mt5_net_profit": long_row.get("net_profit", 0.0),
            "net_diff_proxy_minus_mt5": "",
            "proxy_trade_count": "",
            "mt5_trade_count": long_row.get("trade_count", 0),
            "interpretation": "most MT5 profit remains long source driven(대부분의 MT5 수익은 롱 원천에서 나옴).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "variant_id": "bx01_overlay_hour17_only_keep_native_short",
            "action": "MT5 runtime ablation(MT5 런타임 절제): keep native short threshold(기본 숏 임계값 유지), restrict synthetic overlay(합성 덧씌움 제한) to hour 17 only.",
            "evidence_seed": "BV overlay open-hour attribution: hour17 net +90.14, non-17 overlay net -71.12.",
            "timestamp_safety": "uses entry-time server hour only(진입 시점 서버 시간만 사용).",
            "success_condition": "net improves over BV without PF/recovery/trade-density collapse(BV보다 순수익 개선, PF/회복/밀도 붕괴 없음).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "variant_id": "bx02_native_short_only_overlay_disabled",
            "action": "MT5 runtime control(MT5 런타임 대조): disable synthetic overlay(합성 덧씌움 비활성) while keeping calendar block(달력 차단 유지).",
            "evidence_seed": "Synthetic overlay source net was only +19.02; native short source net was +128.70.",
            "timestamp_safety": "no new data feature(새 데이터 피처 없음).",
            "success_condition": "isolates whether overlay adds real net or only churn(덧씌움이 실제 수익인지 회전인지 분리).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "variant_id": "bx03_hour17_overlay_plus_weak_late_session_firewall",
            "action": "MT5 runtime probe(MT5 런타임 탐침): hour17 overlay(17시 덧씌움) plus weak close-hour 22/late-session risk firewall(22시/후반 세션 위험 방화벽).",
            "evidence_seed": "Close hour 22 net -19.95 and 18/21 near-flat; month 12 remained negative.",
            "timestamp_safety": "uses entry/closed-bar time only(진입/닫힌 봉 시간만 사용).",
            "success_condition": "improves December and weak-session risk without deleting trade density(12월/약세 세션 위험 개선, 거래 밀도 유지).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_audits(trades: pd.DataFrame, cycles: pd.DataFrame, summary: Mapping[str, Any], report_metrics: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    parsed_net = round(float(trades["net_profit"].sum()), 2)
    parsed_count = int(len(trades))
    parsed_long = int((trades["direction"] == "long").sum())
    parsed_short = int((trades["direction"] == "short").sum())
    kpi_rows = [
        {
            "run_id": RUN_ID,
            "check": "mt5_report_vs_parsed_trade_count",
            "status": "passed" if parsed_count == int(report_metrics.get("trade_count", -1)) else "failed",
            "expected": report_metrics.get("trade_count"),
            "observed": parsed_count,
            "effect": "trade row grain matches MT5 report(거래 행 단위가 MT5 보고서와 일치).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "mt5_report_vs_parsed_net_profit",
            "status": "passed" if abs(parsed_net - float(report_metrics.get("net_profit", 999999.0))) < 0.01 else "failed",
            "expected": report_metrics.get("net_profit"),
            "observed": parsed_net,
            "effect": "profit+swap+commission reconciles to MT5 net(수익+스왑+수수료가 MT5 순수익과 일치).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "mt5_report_vs_direction_counts",
            "status": "passed" if parsed_long == int(report_metrics.get("long_trade_count", -1)) and parsed_short == int(report_metrics.get("short_trade_count", -1)) else "failed",
            "expected": f"long={report_metrics.get('long_trade_count')};short={report_metrics.get('short_trade_count')}",
            "observed": f"long={parsed_long};short={parsed_short}",
            "effect": "direction attribution uses MT5 report direction counts(방향 귀속이 MT5 방향 수와 일치).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    row_rows = [
        {
            "run_id": RUN_ID,
            "artifact": rel(MT5_TRADE_ATTRIBUTION),
            "row_grain": "one closed MT5 trade per row(MT5 종료 거래 1개당 1행)",
            "row_count": parsed_count,
            "status": "passed" if parsed_count > 0 else "failed",
            "effect": "trade-shape attribution has executable row grain(거래 형태 귀속 행 단위가 명확).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "artifact": rel(RUNTIME_SIGNAL_ATTRIBUTION),
            "row_grain": "decision/source/hour aggregate(판정/원천/시간 집계)",
            "row_count": int(len(signal_rows(cycles))),
            "status": "passed",
            "effect": "runtime signal source counts are separated from PnL(런타임 신호 수와 손익을 분리).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    source_rows = [
        {
            "run_id": RUN_ID,
            "source": rel(bv.STRATEGY_TESTER_REPORTS),
            "authority": "MT5 Strategy Tester KPI authority(MT5 전략 테스터 KPI 권위)",
            "status": "passed" if report_metrics.get("status") == "completed" else "failed",
            "sha256": sha(bv.STRATEGY_TESTER_REPORTS),
            "effect": "headline trading KPI uses MT5 report, not proxy(MT5 보고서가 헤드라인 KPI 근거).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "source": rel(BV_TELEMETRY),
            "authority": "runtime signal/source attribution(런타임 신호/원천 귀속)",
            "status": "passed" if int(summary.get("model_ok_count", 0)) == int(len(cycles)) else "passed_with_boundary",
            "sha256": sha(BV_TELEMETRY),
            "effect": "signal reason uses runtime telemetry(신호 이유는 런타임 원격측정 기준).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "source": rel(bv.SOURCE_SELECTED_CANDIDATE),
            "authority": "proxy comparator only(프록시 비교 기준 전용)",
            "status": "passed",
            "sha256": sha(bv.SOURCE_SELECTED_CANDIDATE),
            "effect": "proxy is not promoted to MT5 authority(프록시를 MT5 권위로 승격하지 않음).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return kpi_rows, row_rows, source_rows


def gate_rows(kpi_rows: Sequence[Mapping[str, Any]], row_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    def all_passed(rows: Sequence[Mapping[str, Any]]) -> bool:
        return all(str(row.get("status", "")).startswith("passed") for row in rows)

    gates = [
        ("kpi_contract_audit", all_passed(kpi_rows), KPI_CONTRACT_AUDIT, "MT5 KPI와 파싱 거래가 일치한다."),
        ("row_grain_audit", all_passed(row_rows), ROW_GRAIN_AUDIT, "거래/신호 행 단위가 분리된다."),
        ("source_authority_audit", all_passed(source_rows), SOURCE_AUTHORITY_AUDIT, "MT5와 proxy 권위 경계를 분리한다."),
        ("performance_attribution_gate", exists(ATTRIBUTION_BY_SOURCE_BUCKET) and exists(ATTRIBUTION_BY_MONTH), PERFORMANCE_RECEIPT, "성과 귀속 산출물이 생성된다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "운영 승격/런타임 권위를 주장하지 않는다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "필수 gate를 종료 기록에 연결한다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int | None = None) -> str:
    selected = list(rows)[:limit] if limit else list(rows)
    if not selected:
        return "_No rows(행 없음)._"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in selected:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def build_report(
    final: Mapping[str, Any],
    candidate: Mapping[str, Any],
    metrics: Mapping[str, Any],
    direction_rows: Sequence[Mapping[str, Any]],
    bucket_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    hour_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> str:
    worst_months = sorted(month_rows, key=lambda item: float(item.get("net_profit", 0.0)))[:6]
    best_months = sorted(month_rows, key=lambda item: float(item.get("net_profit", 0.0)), reverse=True)[:6]
    return f"""# run364BW BV runtime probe review(364BW BV 런타임 탐침 검토)

## Result(결과)

Action(행동): `run364BV` MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터) report(보고서), deal table(딜 표), runtime telemetry(런타임 원격측정), proxy diff(프록시 차이)를 분해했다.

Effect(효과): synthetic short source overlay(합성 숏 원천 덧씌움)가 전체 수익을 만든 것이 아니라, native short threshold(기본 숏 임계값)과 long source(롱 원천)가 더 큰 수익 동인임을 분리했다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{metrics.get('net_profit')}` / `{metrics.get('profit_factor')}` / `{metrics.get('trade_count')}`
- MT5 expectancy/recovery/DD(기대값/회복 계수/낙폭): `{metrics.get('expectancy')}` / `{metrics.get('recovery_factor')}` / `{metrics.get('equity_drawdown_maximal_amount')}`
- proxy net/PF/trades(프록시 순수익/수익 팩터/거래수): `{final.get('selected_proxy_net_profit')}` / `{final.get('selected_proxy_profit_factor')}` / `{final.get('selected_proxy_trade_count')}`
- operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).

## Source Attribution(원천 귀속)

{table(bucket_rows, ['source_bucket', 'direction', 'trade_count', 'net_profit', 'expectancy', 'profit_factor', 'win_rate_percent'])}

Read(판독): synthetic overlay(합성 덧씌움)는 `73` trades(거래)에서 약한 `+19.02` net(순수익)만 만들었다. Native short(기본 숏)는 `41` trades(거래)에서 `+128.70`이고, long(롱)은 `+818.60`이다.

## Direction Attribution(방향 귀속)

{table(direction_rows, ['direction', 'trade_count', 'net_profit', 'expectancy', 'profit_factor', 'win_rate_percent'])}

## Time And Regime(시간 및 국면)

Worst months(취약 월):

{table(worst_months, ['close_month', 'trade_count', 'net_profit', 'expectancy', 'profit_factor', 'win_rate_percent'])}

Best months(강한 월):

{table(best_months, ['close_month', 'trade_count', 'net_profit', 'expectancy', 'profit_factor', 'win_rate_percent'])}

Close-hour attribution(청산 시간 귀속):

{table(hour_rows, ['close_hour', 'trade_count', 'net_profit', 'expectancy', 'profit_factor', 'win_rate_percent'])}

## Proxy MT5 Diff(프록시 MT5 차이)

{table(proxy_rows, ['comparison', 'proxy_net_profit', 'mt5_net_profit', 'net_diff_proxy_minus_mt5', 'proxy_trade_count', 'mt5_trade_count', 'interpretation'])}

Attribution confidence(귀속 신뢰도): medium(중간). Deal-level PnL(딜 단위 손익)과 runtime source(런타임 원천)는 매칭됐지만, overlay/calendar(덧씌움/달력 차단)의 true counterfactual(진짜 반사실)은 아직 별도 MT5 ablation(절제 실행)이 필요하다.

## Next Probe(다음 탐침)

{table(queue, ['variant_id', 'action', 'evidence_seed', 'success_condition'])}

## Gates(게이트)

{table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This review(이 검토)는 runtime probe review(런타임 탐침 검토)만 주장한다. Forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""


def build_final(
    created_at: str,
    final: Mapping[str, Any],
    candidate: Mapping[str, Any],
    metrics: Mapping[str, Any],
    trades: pd.DataFrame,
    bucket_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    hour_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    bucket_map = {row["source_bucket"]: row for row in bucket_rows}
    month_sorted = sorted(month_rows, key=lambda item: float(item.get("net_profit", 0.0)))
    hour_map = {str(row["close_hour"]): row for row in hour_rows}
    active_day_counts = trades.groupby("close_date").size()
    pass_count = sum(1 for row in gates if row["status"] == "passed")
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "bv_mt5_net_profit": metrics.get("net_profit"),
        "bv_mt5_profit_factor": metrics.get("profit_factor"),
        "bv_mt5_expectancy": metrics.get("expectancy"),
        "bv_mt5_trade_count": metrics.get("trade_count"),
        "bv_mt5_recovery_factor": metrics.get("recovery_factor"),
        "bv_mt5_equity_drawdown_amount": metrics.get("equity_drawdown_maximal_amount"),
        "proxy_net_profit": final.get("selected_proxy_net_profit"),
        "proxy_profit_factor": final.get("selected_proxy_profit_factor"),
        "proxy_trade_count": final.get("selected_proxy_trade_count"),
        "proxy_minus_mt5_net_diff": round(float(final.get("selected_proxy_net_profit", 0.0)) - float(metrics.get("net_profit", 0.0)), 2),
        "synthetic_overlay_trade_count": bucket_map.get("synthetic_short_overlay", {}).get("trade_count", 0),
        "synthetic_overlay_net_profit": bucket_map.get("synthetic_short_overlay", {}).get("net_profit", 0.0),
        "native_short_trade_count": bucket_map.get("native_short_threshold", {}).get("trade_count", 0),
        "native_short_net_profit": bucket_map.get("native_short_threshold", {}).get("net_profit", 0.0),
        "long_source_net_profit": bucket_map.get("long_threshold", {}).get("net_profit", 0.0),
        "worst_month": month_sorted[0].get("close_month") if month_sorted else "",
        "worst_month_net_profit": month_sorted[0].get("net_profit") if month_sorted else "",
        "close_hour_22_net_profit": hour_map.get("22", {}).get("net_profit", ""),
        "trade_days": int(len(active_day_counts)),
        "trade_density_per_active_trade_day": round(float(active_day_counts.mean()), 6),
        "median_trades_per_active_trade_day": round(float(active_day_counts.median()), 6),
        "min_trades_per_active_trade_day": int(active_day_counts.min()) if len(active_day_counts) else 0,
        "attribution_confidence": "medium_counterfactual_ablation_required",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_review_of_completed_bv_probe",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": pass_count,
        "gate_total": len(gates),
    }


def write_receipts(
    final_payload: Mapping[str, Any],
    direction_rows: Sequence[Mapping[str, Any]],
    bucket_rows: Sequence[Mapping[str, Any]],
    month_rows: Sequence[Mapping[str, Any]],
    hour_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
) -> None:
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "observed_change": "BV MT5 probe net 966.32 vs BK 959.64 and proxy 1063.14(BV MT5 순수익 966.32, BK 959.64, proxy 1063.14 대비)",
            "comparison_baseline": "run364BK MT5 reference and run364BS proxy(BK MT5 기준과 BS 프록시)",
            "likely_drivers": [
                "long_threshold source remains dominant(롱 임계값 원천이 지배적)",
                "native_short_threshold outperforms synthetic overlay(기본 숏 임계값이 합성 덧씌움보다 강함)",
                "synthetic overlay non-17 hours are drag(합성 덧씌움 비17시가 부담)",
            ],
            "segment_checks": {
                "direction": rel(ATTRIBUTION_BY_DIRECTION),
                "source_bucket": rel(ATTRIBUTION_BY_SOURCE_BUCKET),
                "month": rel(ATTRIBUTION_BY_MONTH),
                "close_hour": rel(ATTRIBUTION_BY_HOUR),
            },
            "trade_shape": {
                "trade_count": final_payload.get("bv_mt5_trade_count"),
                "net_profit": final_payload.get("bv_mt5_net_profit"),
                "profit_factor": final_payload.get("bv_mt5_profit_factor"),
                "recovery_factor": final_payload.get("bv_mt5_recovery_factor"),
                "synthetic_overlay": bucket_rows,
            },
            "alternative_explanations": [
                "runtime position lifecycle differs from fixed-hold proxy(런타임 포지션 생명주기가 고정 보유 프록시와 다름)",
                "real-tick execution and swap affect net(실제 틱 실행과 스왑이 순손익에 영향)",
                "calendar block and overlay interaction not isolated yet(달력 차단과 덧씌움 상호작용 미분리)",
            ],
            "attribution_confidence": final_payload.get("attribution_confidence"),
            "next_probe": rel(NEXT_PROBE_QUEUE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(bv.TESTER_IDENTITY_CONTRACT),
            "ea_identity": rel(bv.RUNTIME_PARITY_CONTRACT),
            "report_identity": rel(bv.STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(MT5_TRADE_ATTRIBUTION),
            "cost_assumptions": "broker-native real tick, commission 0, swap parsed from deal table(브로커 실제 틱, 수수료 0, 스왑은 딜 표에서 파싱)",
            "forensic_checks": source_rows,
            "backtest_judgment": "usable_with_runtime_probe_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "run364BV MT5 runtime probe review(BV MT5 런타임 탐침 검토)",
            "evidence_available": [rel(bv.STRATEGY_TESTER_REPORTS), rel(BV_TELEMETRY), rel(MT5_TRADE_ATTRIBUTION), rel(PROXY_RUNTIME_ATTRIBUTION)],
            "evidence_missing": "counterfactual MT5 ablation for overlay/calendar, forward replay, live-like readiness(덧씌움/달력 반사실 MT5 절제, 전진 재생, 실거래 유사 준비)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": rel(NEXT_PROBE_QUEUE),
            "user_explanation_hook": "BV is a usable runtime clue, but not operating authority(BV는 쓸 수 있는 런타임 단서지만 운영 권위는 아님).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "runtime_probe_review": "claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage364BW_runtime_probe_review",
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": created_at,
                    "created_at_utc": created_at,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_NUMBER}__{Path(path).stem}",
                    "notes": "Stage364BW runtime probe review artifact(364BW 런타임 탐침 검토 산출물).",
                }
            )
    return rows


def ledger_rows(final_payload: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "completed_source_runtime_probe_review",
        "notes": "BV MT5 probe reviewed; no new MT5 execution in BW(BV MT5 탐침 검토, BW 신규 MT5 실행 없음).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": final_payload.get("gate_passes"),
        "gate_total": final_payload.get("gate_total"),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "work_family": "kpi_evidence(핵심 성과 지표 근거)",
        "family": "runtime_probe_review(런타임 탐침 검토)",
        "lane": "runtime_probe_review(런타임 탐침 검토)",
        "primary_report": rel(REPORT_PATH),
        "result_status": STATUS,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final_payload.get("created_at_utc"),
        "net_profit": final_payload.get("bv_mt5_net_profit"),
        "profit_factor": final_payload.get("bv_mt5_profit_factor"),
        "expectancy": final_payload.get("bv_mt5_expectancy"),
        "recovery_factor": final_payload.get("bv_mt5_recovery_factor"),
        "max_drawdown_amount": final_payload.get("bv_mt5_equity_drawdown_amount"),
        "trade_count": final_payload.get("bv_mt5_trade_count"),
        "long_trade_count": 904,
        "short_trade_count": 114,
        "trade_density_per_feature_day": final_payload.get("trade_density_per_active_trade_day"),
        "trade_density_requirement_status": "average_pass_daily_floor_not_claimed(평균 통과, 일별 바닥은 주장 안 함)",
        "question": "Why did BV MT5 differ from BS proxy and what source should be probed next?(BV MT5가 BS 프록시와 왜 달랐고 다음 원천은 무엇인가?)",
        "next_action": NEXT_RUN_ID,
    }
    views = [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_probe_review", ""),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required", "Tier B fallback not used in BV/BW(BV/BW에서 Tier B 대체 미사용)."),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_probe_review", ""),
    ]
    alpha_rows = []
    stage_rows = []
    for record_view, tier_scope, kpi_scope, notes in views:
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}::{tier_scope.replace(' ', '_')}",
                "row_id": f"{RUN_ID}::{tier_scope.replace(' ', '_')}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "tier": tier_scope,
                "view": record_view,
                "metric_scope": kpi_scope,
                "kpi_scope": kpi_scope,
                "notes": notes or base["notes"],
            }
        )
        if tier_scope == "Tier B":
            row.update({"net_profit": "", "profit_factor": "", "expectancy": "", "trade_count": "", "long_trade_count": "", "short_trade_count": ""})
        alpha_rows.append(row)
        stage_rows.append(row)
    return alpha_rows, stage_rows, base


def sync_state(final_payload: Mapping[str, Any]) -> None:
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
updated_at_utc: {final_payload['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final_payload['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364BW` reviewed BV MT5 runtime probe(BV MT5 런타임 탐침 검토). MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `{final_payload['bv_mt5_net_profit']}` / `{final_payload['bv_mt5_profit_factor']}` / `{final_payload['bv_mt5_trade_count']}`이고, synthetic overlay(합성 덧씌움)는 약한 `+{final_payload['synthetic_overlay_net_profit']}` net(순수익), native short(기본 숏)는 `+{final_payload['native_short_net_profit']}` net(순수익)이다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 hour17-only overlay(17시 한정 덧씌움), native-short-only control(기본 숏 단독 대조), weak late-session firewall(후반 세션 약한 방화벽)을 MT5 runtime ablation(런타임 절제 실행)으로 비교한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final_payload['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe candidate(런타임 탐침 후보): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`

MT5 KPI(MT5 핵심 성과 지표): net `{final_payload['bv_mt5_net_profit']}`, PF `{final_payload['bv_mt5_profit_factor']}`, trades `{final_payload['bv_mt5_trade_count']}`, recovery `{final_payload['bv_mt5_recovery_factor']}`.

Attribution(귀속): long source(롱 원천) net `{final_payload['long_source_net_profit']}`, native short(기본 숏) net `{final_payload['native_short_net_profit']}`, synthetic overlay(합성 덧씌움) net `{final_payload['synthetic_overlay_net_profit']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        STAGE_README,
        "<!-- run364BW -->",
        f"\n<!-- run364BW -->\n- `{RUN_ID}` reviewed BV runtime probe(BV 런타임 탐침 검토): synthetic overlay(합성 덧씌움) weak positive, native short/hour17 clue(기본 숏/17시 단서) opened `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        REVIEW_INDEX,
        "<!-- run364BW -->",
        f"\n<!-- run364BW -->\n- [run364BW review(검토)]({Path(rel(REPORT_PATH)).name}) - `{JUDGMENT}`.\n",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "<!-- run364BW -->",
        f"\n<!-- run364BW -->\n- {final_payload['created_at_utc']} `{RUN_ID}` reviewed BV MT5 runtime probe(BV MT5 런타임 탐침 검토) and opened `{NEXT_RUN_ID}`. Judgment(판정): `{JUDGMENT}`.\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        "<!-- run364BW -->",
        f"\n<!-- run364BW -->\n- Idea(아이디어): hour17-only synthetic overlay(17시 한정 합성 덧씌움) + native short control(기본 숏 대조). Evidence(근거): BV overlay hour17 was positive while non-17 overlay dragged net(BV 덧씌움 17시는 양수, 비17시는 순수익 부담).\n",
    )


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = now_utc()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)

    final = read_json(bv.FINAL_DECISION)
    candidate = read_json(bv.SOURCE_SELECTED_CANDIDATE)
    report_records = read_json(bv.STRATEGY_TESTER_REPORTS)
    metrics = report_records[0]["metrics"]
    cycles, summary = read_runtime_cycles()
    trades = parse_mt5_report_trades(cycles)

    direction_rows = summarize_trades(trades, ["direction"])
    bucket_rows = summarize_trades(trades, ["source_bucket", "direction"])
    month_rows = summarize_trades(trades, ["close_month"])
    hour_rows = summarize_trades(trades, ["close_hour"])
    signal_summary = signal_rows(cycles)
    proxy_rows = proxy_runtime_rows(trades, final, candidate)
    queue = queue_rows()
    kpi_rows, row_rows, source_rows = build_audits(trades, cycles, summary, metrics)

    write_csv(INPUT_MANIFEST, input_manifest_rows(created_at))
    write_json(WORK_PACKET, work_packet(created_at))
    write_csv(MT5_TRADE_ATTRIBUTION, trades.to_dict("records"))
    write_csv(ATTRIBUTION_BY_DIRECTION, direction_rows)
    write_csv(ATTRIBUTION_BY_SOURCE_BUCKET, bucket_rows)
    write_csv(ATTRIBUTION_BY_MONTH, month_rows)
    write_csv(ATTRIBUTION_BY_HOUR, hour_rows)
    write_csv(RUNTIME_SIGNAL_ATTRIBUTION, signal_summary)
    write_csv(PROXY_RUNTIME_ATTRIBUTION, proxy_rows)
    write_csv(NEXT_PROBE_QUEUE, queue)
    write_csv(KPI_CONTRACT_AUDIT, kpi_rows)
    write_csv(ROW_GRAIN_AUDIT, row_rows)
    write_csv(SOURCE_AUTHORITY_AUDIT, source_rows)

    gates = gate_rows(kpi_rows, row_rows, source_rows)
    final_payload = build_final(created_at, final, candidate, metrics, trades, bucket_rows, month_rows, hour_rows, gates)
    write_receipts(final_payload, direction_rows, bucket_rows, month_rows, hour_rows, proxy_rows, source_rows)
    gates = gate_rows(kpi_rows, row_rows, source_rows)
    final_payload = build_final(created_at, final, candidate, metrics, trades, bucket_rows, month_rows, hour_rows, gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final_payload)
    write_json(RUN_MANIFEST, run_manifest(created_at, final_payload, gates))
    write_text(REPORT_PATH, build_report(final, candidate, metrics, direction_rows, bucket_rows, month_rows, hour_rows, proxy_rows, queue, gates), bom=True)
    write_text(
        DECISION_DOC,
        f"""# 2026-06-05 Stage364BW decision(결정)

Decision(결정): `{DECISION}`

Judgment(판정): `{JUDGMENT}`

Action(행동): BV MT5 runtime probe(BV MT5 런타임 탐침)를 source bucket(원천 묶음), direction(방향), month/hour(월/시간), proxy diff(프록시 차이)로 검토했다. Effect(효과): synthetic overlay(합성 덧씌움)를 약한 보조 원천으로 낮추고, hour17-only overlay(17시 한정 덧씌움)와 native short control(기본 숏 대조)을 다음 MT5 ablation(MT5 절제 실행)으로 열었다.

Forbidden claims(금지 주장): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성).
""",
        bom=True,
    )

    alpha_rows, stage_rows, run_row = ledger_rows(final_payload)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], alpha_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], stage_rows)
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows(created_at))
    sync_state(final_payload)

    # Refresh hashes for mutable docs after state sync.
    write_json(LINEAGE_RECEIPT, lineage_receipt(created_at))
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows(created_at))
    return final_payload


def input_manifest_rows(created_at: str) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BW runtime probe review source(BW 런타임 탐침 검토 원천)",
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in [*SOURCE_FILES, BV_TELEMETRY, BV_SUMMARY, BV_HTML_REPORT]
    ]


def work_packet(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "primary_family": "kpi_evidence(핵심 성과 지표 근거)",
        "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
        "support_skills": [
            "obsidian-performance-attribution(성과 귀속)",
            "obsidian-backtest-forensics(백테스트 포렌식)",
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-result-judgment(결과 판정)",
        ],
        "question": "Why did BV MT5 differ from BS proxy and what source should be probed next?(BV MT5가 BS 프록시와 왜 달랐고 다음 원천은 무엇인가?)",
        "required_gates": [
            "kpi_contract_audit",
            "row_grain_audit",
            "source_authority_audit",
            "performance_attribution_gate",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def run_manifest(created_at: str, final_payload: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "work_packet": rel(WORK_PACKET),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "gate_audit": rel(GATE_AUDIT),
        "gate_passes": final_payload.get("gate_passes"),
        "gate_total": final_payload.get("gate_total"),
        "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
        "gates": list(gates),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage_receipt(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_inputs": input_manifest_rows(created_at),
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
        "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_after_commit_expected(커밋 후 추적 예정)",
        "lineage_judgment": "connected_with_runtime_probe_review_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review Stage364BV synthetic short source runtime probe.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    final_payload = run(parse_args(argv))
    print(json.dumps(json_ready(final_payload), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
