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

from foundation.control_plane.mt5_trade_attribution import MarketData, compute_trade_attribution
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage341 import design_f01_stability_cost_regime_validation_without_db as ds


TODAY = ds.TODAY
STAGE_ID = ds.STAGE_ID
STAGE_DIR = ds.STAGE_DIR
RUN_NUMBER = "run341C"
RUN_ID = "run341C_materialize_f01_stability_cost_regime_validation_inputs_without_db_v1"
PARENT_RUN_ID = ds.RUN_ID
NEXT_RUN_ID = "run341D_review_f01_stability_cost_regime_validation_without_db_v1"

STATUS = "completed_stage341C_f01_stability_cost_regime_validation_inputs_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "trade_level_attribution_and_proxy_cost_session_regime_outputs_available_review_required_no_selection"
DECISION = "stage341C_open_run341D_review_f01_stability_cost_regime_validation"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_existing_mt5_report_trade_attribution_proxy_cost_stress_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run341C_f01_stability_cost_regime_validation_inputs.md"
DECISION_DOC = ds.ROOT / "docs" / "decisions" / f"{TODAY}_stage341C_f01_stability_cost_regime_validation_inputs.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

TRADE_LEVEL = RUN_DIR / "trade_level_records.csv"
ATTRIBUTION_SUMMARY = RUN_DIR / "attribution_summary.csv"
COST_STRESS_MATRIX = RUN_DIR / "cost_stress_matrix.csv"
SESSION_REGIME_SCORECARD = RUN_DIR / "session_regime_scorecard.csv"
EQUITY_CURVE_QUALITY = RUN_DIR / "equity_curve_quality.csv"
VALIDATION_SCORECARD = RUN_DIR / "validation_scorecard.csv"
REPORT_PARSE_INVENTORY = RUN_DIR / "report_parse_inventory.csv"
PARSER_ERRORS = RUN_DIR / "parser_errors.json"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

SOURCE_DESIGN_GATES = STAGE_DIR / "02_runs" / "run341B" / "required_gate_coverage_audit.csv"
SOURCE_MATERIALIZATION_QUEUE = ds.MATERIALIZATION_QUEUE
SOURCE_REPORT_RECORDS = ds.SOURCE_REPORT_RECORDS
SOURCE_RUNTIME_SUMMARY = ds.SOURCE_RUNTIME_SUMMARY
SOURCE_SCORECARD = ds.SOURCE_SCORECARD
SOURCE_COST_CONTRACT = ds.COST_STRESS_CONTRACT
RAW_BARS = ds.RAW_BARS
FEATURE_FRAME = ds.FEATURE_FRAME

ATTEMPTS = [
    "q01_ctl_s55_l51_m01_h12",
    "q09_s545_l51_m01_h12",
    "q07_h10_s55_l51_m01_h10",
    "q08_h14_s55_l51_m01_h14",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return ds.rel(path)


def exists(path: Path) -> bool:
    return ds.exists(path)


def sha(path: Path) -> str:
    return ds.sha(path)


def read_csv(path: Path) -> pd.DataFrame:
    return ds.read_csv(path)


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ds.br.ensure_parent(path)
    with open(ds.br.fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    ds.br.ensure_parent(path)
    with open(ds.br.fs_path(path), "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n")


def write_text(path: Path, text: str) -> None:
    ds.br.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ds.br.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, keys: list[str], rows: list[Mapping[str, Any]]) -> None:
    ds.br.append_or_replace_csv(path, keys, rows)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def profit_factor(values: Sequence[float]) -> float | None:
    gross_profit = sum(value for value in values if value > 0.0)
    gross_loss = sum(value for value in values if value < 0.0)
    if gross_loss == 0.0:
        return None
    return gross_profit / abs(gross_loss)


def max_drawdown(values: Sequence[float]) -> float:
    equity = []
    total = 0.0
    for value in values:
        total += float(value)
        equity.append(total)
    peak = 0.0
    max_dd = 0.0
    for value in equity:
        peak = max(peak, value)
        max_dd = max(max_dd, peak - value)
    return max_dd


def consecutive_losses(values: Sequence[float]) -> int:
    best = 0
    current = 0
    for value in values:
        if value < 0.0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def group_summary(frame: pd.DataFrame, group_column: str, attempt: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if group_column not in frame.columns:
        return rows
    total_abs_loss = abs(frame.loc[frame["net_profit"] < 0, "net_profit"].sum())
    total_abs_profit = abs(frame["net_profit"].sum()) or 1.0
    for bucket, group in frame.groupby(group_column, dropna=False):
        values = group["net_profit"].astype(float).tolist()
        gross_loss = sum(value for value in values if value < 0.0)
        rows.append(
            {
                "attempt_name": attempt,
                "axis": group_column,
                "bucket": str(bucket),
                "trade_count": len(group),
                "net_profit": sum(values),
                "profit_factor": profit_factor(values),
                "expectancy": sum(values) / len(values) if len(values) else None,
                "long_trade_count": int(group["direction"].astype(str).eq("buy").sum()),
                "short_trade_count": int(group["direction"].astype(str).eq("sell").sum()),
                "net_share_of_total_abs": abs(sum(values)) / total_abs_profit,
                "loss_share_of_total_loss": abs(gross_loss) / total_abs_loss if total_abs_loss else 0.0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def records_by_attempt() -> dict[str, Mapping[str, Any]]:
    records = json.loads(Path(ds.br.fs_path(SOURCE_REPORT_RECORDS)).read_text(encoding="utf-8-sig"))
    return {str(record.get("attempt_name")): record for record in records}


def report_path_for(record: Mapping[str, Any]) -> Path | None:
    html = record.get("html_report", {})
    if isinstance(html, Mapping) and html.get("path"):
        return Path(str(html["path"]))
    return None


def load_reported_summary() -> dict[str, Mapping[str, Any]]:
    frame = read_csv(SOURCE_RUNTIME_SUMMARY)
    return {str(row["attempt_name"]): row for row in frame.to_dict("records")}


def parse_attempts() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, Any]], pd.DataFrame]:
    market = MarketData.load(ds.ROOT)
    records = records_by_attempt()
    reported = load_reported_summary()
    trade_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    inventory_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for attempt in ATTEMPTS:
        record = records.get(attempt)
        report_path = report_path_for(record or {})
        inventory = {
            "attempt_name": attempt,
            "report_path": report_path.as_posix() if report_path else "",
            "report_exists": bool(report_path and report_path.exists()),
            "parse_status": "pending(대기)",
            "deal_count": "",
            "trade_count": "",
            "reported_trade_count": reported.get(attempt, {}).get("trade_count", ""),
            "reported_net_profit": reported.get(attempt, {}).get("net_profit", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        if report_path is None or not report_path.exists():
            inventory["parse_status"] = "missing_report(보고서 누락)"
            errors.append({"attempt_name": attempt, "error": "missing_report", "report_path": inventory["report_path"]})
            inventory_rows.append(inventory)
            continue
        try:
            parsed = parse_mt5_trade_report(report_path)
            trades = pair_deals_into_trades(parsed["deals"])
            stats = compute_trade_attribution(trades, market)
        except Exception as exc:
            inventory["parse_status"] = "parse_error(파싱 오류)"
            errors.append({"attempt_name": attempt, "error": str(exc), "report_path": inventory["report_path"]})
            inventory_rows.append(inventory)
            continue

        payloads = stats["trades"]
        for payload in payloads:
            row = {
                "attempt_name": attempt,
                "source_role": source_role(attempt),
                "trade_index": payload["trade_index"],
                "direction": payload["direction"],
                "open_time": payload["open_time"],
                "close_time": payload["close_time"],
                "hold_bars": payload["hold_bars"],
                "volume": payload["volume"],
                "open_price": payload["open_price"],
                "close_price": payload["close_price"],
                "gross_profit": payload["gross_profit"],
                "net_profit": payload["net_profit"],
                "swap": payload["swap"],
                "commission": payload["commission"],
                "mfe": payload["mfe"],
                "mae": payload["mae"],
                "realized_over_mfe": payload["realized_over_mfe"],
                "session_slice": payload["session_slice"],
                "volatility_regime": payload["volatility_regime"],
                "trend_regime": payload["trend_regime"],
                "adx_bucket": payload["adx_bucket"],
                "spread_regime": payload["spread_regime"],
                "month": payload["month"],
                "quarter": payload["quarter"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
            trade_rows.append(row)

        values = [float(row["net_profit"]) for row in trade_rows if row["attempt_name"] == attempt]
        reported_row = reported.get(attempt, {})
        long_rows = [row for row in trade_rows if row["attempt_name"] == attempt and row["direction"] == "buy"]
        short_rows = [row for row in trade_rows if row["attempt_name"] == attempt and row["direction"] == "sell"]
        by_month = pd.DataFrame([row for row in trade_rows if row["attempt_name"] == attempt]).groupby("month")["net_profit"].sum()
        dd = max_drawdown(values)
        net = sum(values)
        summary_rows.append(
            {
                "attempt_name": attempt,
                "source_role": source_role(attempt),
                "trade_count": len(values),
                "reported_trade_count": reported_row.get("trade_count", ""),
                "net_profit": net,
                "reported_net_profit": reported_row.get("net_profit", ""),
                "net_profit_diff_vs_report": net - safe_float(reported_row.get("net_profit")),
                "profit_factor": profit_factor(values),
                "reported_profit_factor": reported_row.get("profit_factor", ""),
                "expectancy": net / len(values) if values else None,
                "reported_expectancy": reported_row.get("expectancy", ""),
                "max_drawdown_trade_equity": dd,
                "reported_max_drawdown_amount": reported_row.get("max_drawdown_amount", ""),
                "recovery_factor_trade_equity": net / dd if dd > 0 else None,
                "reported_recovery_factor": reported_row.get("recovery_factor", ""),
                "long_trade_count": len(long_rows),
                "short_trade_count": len(short_rows),
                "long_net_profit": sum(float(row["net_profit"]) for row in long_rows),
                "short_net_profit": sum(float(row["net_profit"]) for row in short_rows),
                "avg_hold_bars": sum(float(row["hold_bars"]) for row in trade_rows if row["attempt_name"] == attempt) / len(values) if values else None,
                "consecutive_losses": consecutive_losses(values),
                "active_month_count": len(by_month),
                "positive_month_ratio": float((by_month > 0).sum() / len(by_month)) if len(by_month) else None,
                "parser_trade_count_status": "matched(일치)" if len(values) == int(safe_float(reported_row.get("trade_count"))) else "differs(차이 있음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        inventory["parse_status"] = "parsed(파싱 완료)"
        inventory["deal_count"] = len(parsed["deals"])
        inventory["trade_count"] = len(values)
        inventory_rows.append(inventory)

    return pd.DataFrame(trade_rows), pd.DataFrame(summary_rows), errors, pd.DataFrame(inventory_rows)


def source_role(attempt: str) -> str:
    return {
        "q01_ctl_s55_l51_m01_h12": "quality_anchor(품질 기준점)",
        "q09_s545_l51_m01_h12": "net_clue(순수익 단서)",
        "q07_h10_s55_l51_m01_h10": "negative_control_short_hold(짧은 보유 부정 대조)",
        "q08_h14_s55_l51_m01_h14": "negative_control_long_hold(긴 보유 부정 대조)",
    }.get(attempt, "unknown(알 수 없음)")


def build_cost_stress(trades: pd.DataFrame) -> pd.DataFrame:
    stress = read_csv(SOURCE_COST_CONTRACT)
    rows: list[dict[str, Any]] = []
    for attempt, group in trades.groupby("attempt_name"):
        base_values = group["net_profit"].astype(float).tolist()
        for stress_row in stress.to_dict("records"):
            extra = safe_float(stress_row.get("extra_cost_per_trade"))
            values = [value - extra for value in base_values]
            net = sum(values)
            dd = max_drawdown(values)
            rows.append(
                {
                    "attempt_name": attempt,
                    "source_role": source_role(attempt),
                    "stress_id": stress_row.get("stress_id", ""),
                    "extra_cost_per_trade": extra,
                    "trade_count": len(values),
                    "stressed_net_profit": net,
                    "stressed_profit_factor": profit_factor(values),
                    "stressed_expectancy": net / len(values) if values else None,
                    "stressed_max_drawdown": dd,
                    "stressed_recovery_factor": net / dd if dd > 0 else None,
                    "cost_floor_pass": net > 0 and (profit_factor(values) or 0.0) >= 1.10 and (net / dd if dd > 0 else 0.0) >= 1.00,
                    "proxy_boundary": "proxy_cost_stress_not_mt5_replacement(프록시 비용 압박, MT5 대체 아님)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def build_session_regime(trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for attempt, group in trades.groupby("attempt_name"):
        for column in ["session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime", "month", "quarter"]:
            rows.extend(group_summary(group, column, attempt))
    return pd.DataFrame(rows)


def build_equity_quality(trades: pd.DataFrame, session_regime: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for attempt, group in trades.groupby("attempt_name"):
        values = group.sort_values("close_time")["net_profit"].astype(float).tolist()
        by_month = group.groupby("month")["net_profit"].sum()
        session_rows = session_regime.loc[(session_regime["attempt_name"].eq(attempt)) & (session_regime["axis"].eq("session_slice"))]
        worst_session_loss_share = float(session_rows["loss_share_of_total_loss"].max()) if not session_rows.empty else 0.0
        net = sum(values)
        dd = max_drawdown(values)
        rows.append(
            {
                "attempt_name": attempt,
                "source_role": source_role(attempt),
                "trade_count": len(values),
                "net_profit": net,
                "max_drawdown_trade_equity": dd,
                "recovery_factor_trade_equity": net / dd if dd > 0 else None,
                "consecutive_losses": consecutive_losses(values),
                "active_month_count": len(by_month),
                "positive_month_ratio": float((by_month > 0).sum() / len(by_month)) if len(by_month) else None,
                "worst_month_net_profit": float(by_month.min()) if len(by_month) else None,
                "best_month_net_profit": float(by_month.max()) if len(by_month) else None,
                "worst_session_loss_share": worst_session_loss_share,
                "quality_warning": quality_warning(net, dd, consecutive_losses(values), worst_session_loss_share),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def quality_warning(net: float, dd: float, losses: int, session_loss_share: float) -> str:
    warnings = []
    if dd > 100:
        warnings.append("trade_equity_drawdown_gt_100(거래 수익곡선 낙폭 100 초과)")
    if losses >= 4:
        warnings.append("loss_cluster_ge_4(연속 손실 4 이상)")
    if session_loss_share >= 0.70:
        warnings.append("single_session_loss_concentration(단일 세션 손실 집중)")
    if net <= 0:
        warnings.append("non_positive_net(비양수 순수익)")
    return ";".join(warnings) if warnings else "none(없음)"


def build_validation_scorecard(summary: pd.DataFrame, cost: pd.DataFrame, equity: pd.DataFrame) -> pd.DataFrame:
    rows = []
    stress_1 = cost.loc[cost["stress_id"].eq("c03_plus_1_00")]
    for record in summary.to_dict("records"):
        attempt = record["attempt_name"]
        stress_row = stress_1.loc[stress_1["attempt_name"].eq(attempt)]
        equity_row = equity.loc[equity["attempt_name"].eq(attempt)]
        stressed_net = stress_row.iloc[0]["stressed_net_profit"] if not stress_row.empty else math.nan
        stressed_recovery = stress_row.iloc[0]["stressed_recovery_factor"] if not stress_row.empty else math.nan
        warning = equity_row.iloc[0]["quality_warning"] if not equity_row.empty else "missing(누락)"
        rows.append(
            {
                "attempt_name": attempt,
                "source_role": source_role(attempt),
                "base_net_profit": record.get("net_profit"),
                "base_profit_factor": record.get("profit_factor"),
                "base_recovery_factor_trade_equity": record.get("recovery_factor_trade_equity"),
                "reported_recovery_factor": record.get("reported_recovery_factor"),
                "plus_1_cost_net_profit": stressed_net,
                "plus_1_cost_recovery_factor": stressed_recovery,
                "quality_warning": warning,
                "review_need": "review_required(검토 필요)",
                "selection_claim": "not_claimed(주장 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def output_files() -> list[Path]:
    return [
        TRADE_LEVEL,
        ATTRIBUTION_SUMMARY,
        COST_STRESS_MATRIX,
        SESSION_REGIME_SCORECARD,
        EQUITY_CURVE_QUALITY,
        VALIDATION_SCORECARD,
        REPORT_PARSE_INVENTORY,
        PARSER_ERRORS,
        RESULT_JUDGMENT_RECEIPT,
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        DATA_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
        STAGE_BRIEF,
        STAGE_README,
        ds.br.WORKSPACE_STATE,
        ds.br.CURRENT_WORKING_STATE,
        STAGE_LEDGER,
        ds.br.RUN_REGISTRY,
        ds.br.PROJECT_LEDGER,
        ds.br.ARTIFACT_REGISTRY,
        Path(__file__),
    ]


def write_receipts(summary: pd.DataFrame, errors: list[dict[str, Any]]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "judgment_class": "materialized_review_required(물질화 완료, 검토 필요)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "effect": "새 MT5 실행 없이 기존 MT5 report(보고서)를 재분해했다.",
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "attribution_axes": ["cost_stress(비용 압박)", "session_regime(세션/국면)", "equity_curve_quality(수익곡선 품질)"],
            "attempt_count": int(summary["attempt_name"].nunique()) if not summary.empty else 0,
            "effect": "run341D(341D 실행)가 q01/q09(큐01/큐09)의 수익 구조를 비교할 수 있다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(SOURCE_REPORT_RECORDS), rel(RAW_BARS), rel(FEATURE_FRAME)],
            "parse_error_count": len(errors),
            "time_axis": "MT5 report broker clock(브로커 시계) with attribution join(귀속 결합)",
            "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)" if not errors else "inconclusive(불충분)",
            "effect": "파싱 실패가 있으면 검토에서 긍정 판정으로 닫지 못하게 한다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in [SOURCE_MATERIALIZATION_QUEUE, SOURCE_REPORT_RECORDS, SOURCE_RUNTIME_SUMMARY, RAW_BARS, FEATURE_FRAME]],
            "artifact_paths": [rel(path) for path in output_files()],
            "source_artifact_hashes": {rel(path): sha(path) for path in [SOURCE_MATERIALIZATION_QUEUE, SOURCE_REPORT_RECORDS, SOURCE_RUNTIME_SUMMARY, RAW_BARS, FEATURE_FRAME] if exists(path) and ds.br.path_is_file(path)},
            "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
            "effect": "기존 MT5 report(보고서)에서 파생된 파일임을 추적한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "promotion_candidate": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "proxy_cost_stress_replaces_mt5": False,
            "effect": "proxy cost stress(프록시 비용 압박)를 MT5 KPI(MT5 핵심 성과 지표) 대체물로 쓰지 않는다.",
        },
    )


def gate_row(gate_id: str, status: str, evidence_path: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": evidence_path,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(summary: pd.DataFrame, inventory: pd.DataFrame, errors: list[dict[str, Any]]) -> pd.DataFrame:
    design_gates = read_csv(SOURCE_DESIGN_GATES) if exists(SOURCE_DESIGN_GATES) else pd.DataFrame({"status": ["missing"]})
    parsed_attempts = set(inventory.loc[inventory["parse_status"].astype(str).str.startswith("parsed"), "attempt_name"])
    return pd.DataFrame(
        [
            gate_row(
                "parent_341B_gates_passed",
                "passed" if not design_gates.empty and design_gates["status"].astype(str).str.lower().eq("passed").all() else "failed",
                rel(SOURCE_DESIGN_GATES),
                "run341B(341B 실행) 설계를 이어받는다.",
            ),
            gate_row(
                "required_reports_parsed",
                "passed" if {"q01_ctl_s55_l51_m01_h12", "q09_s545_l51_m01_h12"}.issubset(parsed_attempts) else "failed",
                rel(REPORT_PARSE_INVENTORY),
                "q01/q09(큐01/큐09) 필수 보고서를 파싱한다.",
            ),
            gate_row(
                "negative_controls_parsed_or_recorded",
                "passed" if {"q07_h10_s55_l51_m01_h10", "q08_h14_s55_l51_m01_h14"}.issubset(parsed_attempts) else "failed",
                rel(REPORT_PARSE_INVENTORY),
                "q07/q08(큐07/큐08) 부정 대조를 같은 방식으로 기록한다.",
            ),
            gate_row(
                "market_feature_sources_available",
                "passed" if exists(RAW_BARS) and exists(FEATURE_FRAME) else "failed",
                f"{rel(RAW_BARS)};{rel(FEATURE_FRAME)}",
                "MFE/MAE(유리/불리 이동)와 session/regime(세션/국면) 귀속 원천을 확인한다.",
            ),
            gate_row(
                "attribution_outputs_written",
                "passed" if all(exists(path) for path in [TRADE_LEVEL, ATTRIBUTION_SUMMARY, SESSION_REGIME_SCORECARD, EQUITY_CURVE_QUALITY]) else "failed",
                f"{rel(TRADE_LEVEL)};{rel(ATTRIBUTION_SUMMARY)};{rel(SESSION_REGIME_SCORECARD)};{rel(EQUITY_CURVE_QUALITY)}",
                "거래 단위와 국면 귀속 산출물을 만든다.",
            ),
            gate_row(
                "proxy_cost_stress_written",
                "passed" if exists(COST_STRESS_MATRIX) and not read_csv(COST_STRESS_MATRIX).empty else "failed",
                rel(COST_STRESS_MATRIX),
                "proxy cost stress(프록시 비용 압박)를 별도 파일로 분리한다.",
            ),
            gate_row(
                "review_required_no_selection",
                "passed" if not summary.empty and len(errors) == 0 else "failed",
                rel(VALIDATION_SCORECARD),
                "materialization(물질화) 결과를 review required(검토 필요)로만 둔다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
            ),
        ]
    )


def write_docs(summary: pd.DataFrame, scorecard: pd.DataFrame) -> None:
    q01 = summary.loc[summary["attempt_name"].eq("q01_ctl_s55_l51_m01_h12")]
    q09 = summary.loc[summary["attempt_name"].eq("q09_s545_l51_m01_h12")]
    q01_net = q01.iloc[0]["net_profit"] if not q01.empty else ""
    q09_net = q09.iloc[0]["net_profit"] if not q09.empty else ""
    report = f"""# run341C F01 Stability Cost Regime Validation Inputs(341C F01 안정성 비용 국면 검증 입력)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- parsed_attempts(파싱 시도): `{summary['attempt_name'].nunique() if not summary.empty else 0}`
- q01 trade-level net(큐01 거래 단위 순수익): `{q01_net}`
- q09 trade-level net(큐09 거래 단위 순수익): `{q09_net}`

## Action(행동)

기존 MT5 strategy tester report(메타트레이더5 전략 테스터 보고서)를 trade-level(거래 단위)로 파싱하고, cost stress(비용 압박), session/regime(세션/국면), equity curve quality(수익곡선 품질) 파일을 만들었다.
Effect(효과): run341D(341D 실행)가 q01 quality anchor(품질 기준점)와 q09 net clue(순수익 단서)를 숫자 한 줄이 아니라 수익 구조로 판정할 수 있다.

## Boundary(경계)

No new MT5 execution(새 MT5 실행 없음). Proxy cost stress(프록시 비용 압박)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. Selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage 341C Validation Input Materialization(341C 검증 입력 물질화)

- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- output(출력): `{rel(VALIDATION_SCORECARD)}`

Action(행동): q01/q09/q07/q08(큐01/큐09/큐07/큐08) MT5 report(보고서)를 거래 단위로 분해했다.
Effect(효과): Stage 341(341단계)이 cost/session/regime/equity(비용/세션/국면/수익곡선) 검토로 바로 넘어갈 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 341 Selection Status(341단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- quality_anchor(품질 기준점): `q01_ctl_s55_l51_m01_h12`
- net_high_clue(순수익 높은 단서): `q09_s545_l51_m01_h12`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): run341D(341D 실행)가 review(검토)를 하더라도 selection claim(선정 주장)을 새로 열기 전까지 막는다.
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

run341D(341D 실행)는 `{rel(VALIDATION_SCORECARD)}`를 중심으로 q01/q09(큐01/큐09)의 cost/session/regime/equity(비용/세션/국면/수익곡선) 안정성을 검토한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
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
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(SELECTION_STATUS, selection)
    write_text(ds.br.CURRENT_WORKING_STATE, current)
    write_text(ds.br.WORKSPACE_STATE, workspace)
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""## run341C Validation Inputs(341C 검증 입력)

- run_id(실행 ID): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): 기존 MT5 report(보고서)를 trade-level attribution(거래 단위 귀속) 산출물로 물질화했다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run341C Validation Inputs(341C 검증 입력)

- run_id(실행 ID): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): run341D(341D 실행)가 수익 구조를 검토할 수 있게 했다.
""",
    )
    changelog = f"""## {TODAY} run341C Validation Inputs(341C 검증 입력)

- action(행동): 기존 MT5 report(메타트레이더5 보고서)를 거래 단위로 파싱했다.
- effect(효과): q01/q09(큐01/큐09)의 cost/session/regime/equity(비용/세션/국면/수익곡선) 검토 자료를 만들었다.
- boundary(경계): 새 MT5 실행 없음, 선정 없음, 런타임 권위 없음, 목표 달성 없음.
"""
    append_text_once(ds.br.ROOT_CHANGELOG, RUN_ID, changelog)
    append_text_once(ds.br.WORKSPACE_CHANGELOG, RUN_ID, changelog)


def ledger_rows(gates: pd.DataFrame, summary: pd.DataFrame) -> list[dict[str, Any]]:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    q09 = summary.loc[summary["attempt_name"].eq("q09_s545_l51_m01_h12")]
    q09_row = q09.iloc[0].to_dict() if not q09.empty else {}
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
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": "logreg_balanced_c025_q09_s545_l51_m01_h12",
        "net_profit": q09_row.get("net_profit", ""),
        "profit_factor": q09_row.get("profit_factor", ""),
        "drawdown": q09_row.get("max_drawdown_trade_equity", ""),
        "recovery_factor": q09_row.get("recovery_factor_trade_equity", ""),
        "trade_count": q09_row.get("trade_count", ""),
        "result_status": "materialized_review_required_no_selection(물질화 완료, 검토 필요, 선정 없음)",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": "",
        "expectancy": q09_row.get("expectancy", ""),
        "attempt_count": int(summary["attempt_name"].nunique()) if not summary.empty else "",
    }
    rows = []
    for view, tier, metric_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "trade_attribution_materialized_review_required"),
        ("Tier B separate(Tier B 분리)", "Tier B", "missing_required"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "same_as_tier_a_until_tier_b_available"),
    ]:
        row = dict(base)
        row.update({"view": view, "tier": tier, "metric_scope": metric_scope})
        if metric_scope == "missing_required":
            for metric in ["candidate_model_id", "net_profit", "profit_factor", "drawdown", "recovery_factor", "trade_count", "matched_rows", "expectancy", "attempt_count"]:
                row[metric] = ""
            row["result_status"] = "missing_required(필수 누락)"
        rows.append(row)
    return rows


def write_registries(gates: pd.DataFrame, summary: pd.DataFrame) -> None:
    rows = ledger_rows(gates, summary)
    existing = read_csv(STAGE_LEDGER) if exists(STAGE_LEDGER) else pd.DataFrame()
    if not existing.empty and "run_id" in existing.columns:
        existing = existing.loc[~existing["run_id"].astype(str).eq(RUN_ID)].copy()
    write_csv(STAGE_LEDGER, pd.concat([existing, pd.DataFrame(rows)], ignore_index=True))
    append_or_replace_csv(ds.br.RUN_REGISTRY, ["run_id"], [rows[0]])
    project_rows = []
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["kpi_scope"] = "trade_attribution_materialization(거래 귀속 물질화)"
        project_row["scoreboard_lane"] = "runtime_probe_attribution(런타임 탐침 귀속)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        project_rows.append(project_row)
    append_or_replace_csv(ds.br.PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    artifact_rows = []
    for path in output_files():
        if exists(path) and ds.br.path_is_file(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": path.suffix.lstrip(".") or "file",
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(ds.br.ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def main() -> None:
    ds.br.Path(ds.br.fs_path(RUN_DIR)).mkdir(parents=True, exist_ok=True)
    ds.br.Path(ds.br.fs_path(REVIEW_DIR)).mkdir(parents=True, exist_ok=True)
    for path in [SOURCE_MATERIALIZATION_QUEUE, SOURCE_REPORT_RECORDS, SOURCE_RUNTIME_SUMMARY, RAW_BARS, FEATURE_FRAME]:
        if not exists(path):
            raise FileNotFoundError(f"missing required materialization input: {rel(path)}")

    trades, summary, errors, inventory = parse_attempts()
    cost = build_cost_stress(trades)
    session = build_session_regime(trades)
    equity = build_equity_quality(trades, session)
    scorecard = build_validation_scorecard(summary, cost, equity)

    write_csv(TRADE_LEVEL, trades)
    write_csv(ATTRIBUTION_SUMMARY, summary)
    write_csv(COST_STRESS_MATRIX, cost)
    write_csv(SESSION_REGIME_SCORECARD, session)
    write_csv(EQUITY_CURVE_QUALITY, equity)
    write_csv(VALIDATION_SCORECARD, scorecard)
    write_csv(REPORT_PARSE_INVENTORY, inventory)
    write_json(PARSER_ERRORS, errors)
    write_receipts(summary, errors)
    gates = build_gates(summary, inventory, errors)
    write_csv(GATE_AUDIT, gates)
    write_docs(summary, scorecard)
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
            "gate_total": int(len(gates)),
            "attempt_count": int(summary["attempt_name"].nunique()) if not summary.empty else 0,
            "parse_error_count": len(errors),
            "candidate_selection": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "command": "python -B stage_pipelines/stage341/materialize_f01_stability_cost_regime_validation_inputs_without_db.py",
            "outputs": [rel(path) for path in output_files() if exists(path)],
            "status": STATUS,
            "judgment": JUDGMENT,
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_registries(gates, summary)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "attempt_count": int(summary["attempt_name"].nunique()) if not summary.empty else 0,
                "parse_error_count": len(errors),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
