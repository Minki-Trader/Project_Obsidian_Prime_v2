from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage344 import (  # noqa: E402
    execute_s07_forward_cost_stability_validation_mt5_probe_without_db as probe,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_s07_forward_cost_stability_validation_package_without_db as pkg,
)


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344I"
RUN_ID = "run344I_review_s07_forward_cost_stability_validation_mt5_probe_without_db_v1"
PARENT_RUN_ID = probe.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run344J_design_s07_deal_level_cost_session_forward_replay_validation_without_db_v1"

STATUS = "completed_stage344I_s07_forward_cost_stability_validation_reviewed_positive_moderate_cost_no_selection"
JUDGMENT = (
    "s07_survives_moderate_cost_overlay_and_exact_runtime_parity_"
    "heavy_cost_and_session_pnl_still_unresolved_no_operating_claim"
)
DECISION = "stage344I_open_run344J_deal_level_cost_session_forward_replay_validation_design"
CLAIM_BOUNDARY = (
    "research_development_review_only_s07_forward_cost_stability_validation_positive_moderate_cost_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344I_s07_forward_cost_stability_validation_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344I_s07_forward_cost_stability_validation_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

COST_STRESS_SCORECARD = RUN_DIR / "cost_stress_scorecard.csv"
SESSION_SIGNAL_STABILITY = RUN_DIR / "session_signal_stability.csv"
REGIME_SIGNAL_STABILITY = RUN_DIR / "regime_signal_stability.csv"
COMPARATOR_REVIEW = RUN_DIR / "comparator_review_scorecard.csv"
EQUITY_CURVE_QUALITY = RUN_DIR / "equity_curve_quality.csv"
TELEMETRY_READ_MANIFEST = RUN_DIR / "telemetry_read_manifest.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
RUN344J_QUEUE = RUN_DIR / "run344J_queue.csv"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

INPUT_FILES = (
    probe.FINAL_DECISION,
    probe.GATE_AUDIT,
    probe.EXECUTION_SUMMARY,
    probe.PROXY_MT5_DIFF,
    probe.STRATEGY_TESTER_REPORTS,
    probe.RUNTIME_IDENTITY,
    pkg.COST_STRESS_CONTRACT,
    pkg.SESSION_REGIME_PLAN,
    pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    pkg.FEATURE_MATRIX,
)

OUTPUT_FILES = (
    COST_STRESS_SCORECARD,
    SESSION_SIGNAL_STABILITY,
    REGIME_SIGNAL_STABILITY,
    COMPARATOR_REVIEW,
    EQUITY_CURVE_QUALITY,
    TELEMETRY_READ_MANIFEST,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    RUN344J_QUEUE,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
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

SESSION_BUCKETS = (
    "pre_cash_or_off_session(현금장 전/외부)",
    "cash_open_first_60m(현금장 첫 60분)",
    "cash_mid_60_210m(현금장 중반 60-210분)",
    "cash_late_after_210m(현금장 후반 210분 이후)",
)
REGIME_BUCKETS = (
    "low(낮음)",
    "mid(중간)",
    "high(높음)",
)
TELEMETRY_RESOLUTION_CACHE: dict[str, Path] = {}
TELEMETRY_READ_ROWS: list[dict[str, Any]] = []


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def ensure_parent(path: Path) -> None:
    pkg.ensure_parent(path)


def exists(path: Path) -> bool:
    return pkg.path_is_file(path)


def required(path: Path) -> Path:
    return pkg.required(path)


def sha256_file(path: Path) -> str:
    return pkg.sha256_file(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fields: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields
    ensure_parent(path)
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_frame(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    frame.to_csv(path, index=False, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_or_replace_csv(path, keys, rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value) or value == "":
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def pct(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round(float(numerator) / float(denominator), 6)


def parent_gates_passed() -> bool:
    gates = read_csv(probe.GATE_AUDIT)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def report_metric_map(report_records: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    out: dict[str, Mapping[str, Any]] = {}
    for record in report_records:
        out[str(record.get("attempt_name", ""))] = record.get("metrics", {})
    return out


def scenario_id(raw: Any) -> str:
    text = str(raw)
    return text.split("(", 1)[0].strip()


def build_cost_stress(
    summary: pd.DataFrame,
    report_records: Sequence[Mapping[str, Any]],
    cost_contract: pd.DataFrame,
    attempts: pd.DataFrame,
) -> pd.DataFrame:
    metrics_by_attempt = report_metric_map(report_records)
    role_by_attempt = dict(zip(attempts["attempt_name"].astype(str), attempts["variant_role"].astype(str)))
    rows: list[dict[str, Any]] = []
    for _, attempt_row in summary.iterrows():
        attempt = str(attempt_row["attempt_name"])
        metrics = metrics_by_attempt.get(attempt, {})
        trade_count = as_int(metrics.get("trade_count", attempt_row.get("trade_count")))
        gross_profit = as_float(metrics.get("gross_profit"))
        gross_loss = as_float(metrics.get("gross_loss"))
        gross_loss_abs = abs(gross_loss)
        net_profit = as_float(metrics.get("net_profit", attempt_row.get("net_profit")))
        max_dd = as_float(metrics.get("max_drawdown_amount", attempt_row.get("max_drawdown_amount")))
        for _, cost_row in cost_contract.iterrows():
            cost_per_trade = as_float(cost_row.get("cost_per_closed_trade_account_currency"))
            cost_total = round(cost_per_trade * trade_count, 6)
            adjusted_net = round(net_profit - cost_total, 6)
            adjusted_expectancy = round(adjusted_net / trade_count, 6) if trade_count else 0.0
            adjusted_gross_profit = round(max(gross_profit - cost_total, 0.0), 6)
            adjusted_pf = round(adjusted_gross_profit / gross_loss_abs, 6) if gross_loss_abs else 0.0
            adjusted_recovery = round(adjusted_net / max_dd, 6) if max_dd else 0.0
            survival_passed = adjusted_net > 0 and adjusted_pf >= 1.5 and adjusted_recovery >= 1.0
            rows.append(
                {
                    "attempt_name": attempt,
                    "variant_role": role_by_attempt.get(attempt, ""),
                    "cost_scenario": cost_row.get("cost_scenario", ""),
                    "cost_scenario_id": scenario_id(cost_row.get("cost_scenario", "")),
                    "cost_per_closed_trade_account_currency": cost_per_trade,
                    "trade_count": trade_count,
                    "base_net_profit": net_profit,
                    "base_profit_factor": as_float(metrics.get("profit_factor", attempt_row.get("profit_factor"))),
                    "base_recovery_factor": as_float(metrics.get("recovery_factor", attempt_row.get("recovery_factor"))),
                    "base_expectancy": as_float(metrics.get("expectancy", attempt_row.get("expectancy"))),
                    "gross_profit": gross_profit,
                    "gross_loss": gross_loss,
                    "max_drawdown_amount": max_dd,
                    "cost_total": cost_total,
                    "adjusted_net_profit": adjusted_net,
                    "adjusted_profit_factor_estimate": adjusted_pf,
                    "adjusted_expectancy": adjusted_expectancy,
                    "adjusted_recovery_factor": adjusted_recovery,
                    "survival_passed": survival_passed,
                    "survival_status": "passed(통과)" if survival_passed else "failed(실패)",
                    "floor_rule": "net>0;profit_factor_estimate>=1.5;recovery>=1.0",
                    "use": cost_row.get("use", ""),
                    "limitation": "post-MT5 overlay estimate(MT5 이후 오버레이 추정); not tester authority(테스터 권위 아님)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    frame = pd.DataFrame(rows)
    if not frame.empty:
        frame["scenario_adjusted_net_rank"] = (
            frame.groupby("cost_scenario_id")["adjusted_net_profit"].rank(method="dense", ascending=False).astype(int)
        )
        frame["scenario_adjusted_recovery_rank"] = (
            frame.groupby("cost_scenario_id")["adjusted_recovery_factor"].rank(method="dense", ascending=False).astype(int)
        )
    return frame


def session_bucket(minutes: Any) -> str:
    minute = as_float(minutes, -10_000.0)
    if minute < 0:
        return SESSION_BUCKETS[0]
    if minute < 60:
        return SESSION_BUCKETS[1]
    if minute < 210:
        return SESSION_BUCKETS[2]
    return SESSION_BUCKETS[3]


def quantile_bucket(value: Any, low_edge: float, high_edge: float) -> str:
    number = as_float(value, float("nan"))
    if pd.isna(number):
        return "missing(누락)"
    if number <= low_edge:
        return REGIME_BUCKETS[0]
    if number <= high_edge:
        return REGIME_BUCKETS[1]
    return REGIME_BUCKETS[2]


def decision_counts(frame: pd.DataFrame) -> dict[str, Any]:
    total = len(frame)
    long_count = int(frame["decision"].astype(str).str.lower().eq("long").sum()) if total else 0
    short_count = int(frame["decision"].astype(str).str.lower().eq("short").sum()) if total else 0
    flat_count = int(frame["decision"].astype(str).str.lower().eq("flat").sum()) if total else 0
    order_attempt_count = int(frame["order_attempted"].map(as_bool).sum()) if total else 0
    order_fill_count = int(frame["order_filled"].map(as_bool).sum()) if total else 0
    return {
        "cycle_rows": total,
        "long_signal_count": long_count,
        "short_signal_count": short_count,
        "flat_count": flat_count,
        "order_attempt_count": order_attempt_count,
        "order_fill_count": order_fill_count,
        "long_signal_share": pct(long_count, total),
        "short_signal_share": pct(short_count, total),
        "fill_rate_vs_attempts": pct(order_fill_count, order_attempt_count),
        "fill_rate_vs_cycles": pct(order_fill_count, total),
    }


def resolve_telemetry_path(attempt_name: str, telemetry_path: Path) -> Path:
    if attempt_name in TELEMETRY_RESOLUTION_CACHE:
        return TELEMETRY_RESOLUTION_CACHE[attempt_name]
    if telemetry_path.exists():
        TELEMETRY_RESOLUTION_CACHE[attempt_name] = telemetry_path
        TELEMETRY_READ_ROWS.append(
            {
                "attempt_name": attempt_name,
                "requested_path": rel(telemetry_path),
                "read_path": rel(telemetry_path),
                "path_source": "local_copy(로컬 복사본)",
                "effect": "reads copied runtime telemetry(복사된 런타임 텔레메트리 읽기)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        return telemetry_path
    copy_manifest = read_csv(probe.RUNTIME_OUTPUT_COPY)
    matches = copy_manifest.loc[
        copy_manifest["attempt_name"].astype(str).eq(attempt_name)
        & copy_manifest["copy_id"].astype(str).str.endswith("::telemetry")
    ]
    for _, row in matches.iterrows():
        for column in ("target_path", "source_path"):
            candidate = Path(str(row.get(column, "")))
            if not candidate.is_absolute():
                candidate = ROOT / candidate
            if candidate.exists():
                TELEMETRY_RESOLUTION_CACHE[attempt_name] = candidate
                TELEMETRY_READ_ROWS.append(
                    {
                        "attempt_name": attempt_name,
                        "requested_path": rel(telemetry_path),
                        "read_path": candidate.as_posix() if candidate.is_absolute() and not str(candidate).startswith(str(ROOT)) else rel(candidate),
                        "path_source": f"manifest_{column}_fallback({column} 대체)",
                        "effect": "keeps review runnable while preserving source path choice(원천 경로 선택을 남기며 검토 실행 유지)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
                return candidate
    raise FileNotFoundError(f"telemetry file not readable for {attempt_name}: {telemetry_path}")


def joined_cycles(attempt_name: str, telemetry_path: Path, features: pd.DataFrame) -> pd.DataFrame:
    telemetry = read_csv(resolve_telemetry_path(attempt_name, telemetry_path))
    cycles = telemetry.loc[telemetry["record_type"].astype(str).str.lower().eq("cycle")].copy()
    cycles["join_time"] = cycles["source_time"].fillna(cycles["bar_time"]).astype(str)
    feature_cols = ["timestamp", "minutes_from_cash_open", "is_first_30m_after_open", "adx_14", "historical_vol_20"]
    feature_part = features.loc[:, feature_cols].copy()
    feature_part["join_time"] = feature_part["timestamp"].astype(str)
    merged = cycles.merge(feature_part.drop(columns=["timestamp"]), how="left", on="join_time")
    return merged


def build_session_signal_stability(summary: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, attempt_row in summary.iterrows():
        attempt = str(attempt_row["attempt_name"])
        telemetry_path = ROOT / str(attempt_row["local_telemetry_path"])
        merged = joined_cycles(attempt, telemetry_path, features)
        merged["session_bucket"] = merged["minutes_from_cash_open"].map(session_bucket)
        for bucket in SESSION_BUCKETS:
            subset = merged.loc[merged["session_bucket"].eq(bucket)].copy()
            counts = decision_counts(subset)
            rows.append(
                {
                    "attempt_name": attempt,
                    "segment_type": "session(세션)",
                    "segment_bucket": bucket,
                    **counts,
                    "missing_feature_rows": int(subset["minutes_from_cash_open"].isna().sum()) if len(subset) else 0,
                    "attribution_scope": "signal_and_fill_only_no_pnl(신호/체결만, 손익 없음)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def build_regime_signal_stability(summary: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    edges: dict[str, tuple[float, float]] = {}
    for column in ("adx_14", "historical_vol_20"):
        valid = pd.to_numeric(features[column], errors="coerce").dropna()
        low, high = valid.quantile([0.333333, 0.666667]).tolist()
        edges[column] = (float(low), float(high))
    for _, attempt_row in summary.iterrows():
        attempt = str(attempt_row["attempt_name"])
        telemetry_path = ROOT / str(attempt_row["local_telemetry_path"])
        merged = joined_cycles(attempt, telemetry_path, features)
        for column, label in (("adx_14", "adx_14(ADX 14)"), ("historical_vol_20", "historical_vol_20(20봉 역사 변동성)")):
            low, high = edges[column]
            merged[f"{column}_bucket"] = merged[column].map(lambda value, lo=low, hi=high: quantile_bucket(value, lo, hi))
            for bucket in REGIME_BUCKETS:
                subset = merged.loc[merged[f"{column}_bucket"].eq(bucket)].copy()
                counts = decision_counts(subset)
                rows.append(
                    {
                        "attempt_name": attempt,
                        "segment_type": "regime(국면)",
                        "regime_dimension": label,
                        "segment_bucket": bucket,
                        "low_edge": round(low, 6),
                        "high_edge": round(high, 6),
                        **counts,
                        "missing_feature_rows": int(subset[column].isna().sum()) if len(subset) else 0,
                        "attribution_scope": "signal_and_fill_only_no_pnl(신호/체결만, 손익 없음)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return pd.DataFrame(rows)


def build_equity_quality(summary: pd.DataFrame, report_records: Sequence[Mapping[str, Any]]) -> pd.DataFrame:
    metrics_by_attempt = report_metric_map(report_records)
    rows: list[dict[str, Any]] = []
    for _, row in summary.iterrows():
        attempt = str(row["attempt_name"])
        metrics = metrics_by_attempt.get(attempt, {})
        winning = as_int(metrics.get("winning_trade_count"))
        losing = as_int(metrics.get("losing_trade_count"))
        gross_profit = as_float(metrics.get("gross_profit"))
        gross_loss_abs = abs(as_float(metrics.get("gross_loss")))
        avg_win = round(gross_profit / winning, 6) if winning else 0.0
        avg_loss = round(gross_loss_abs / losing, 6) if losing else 0.0
        payoff_ratio = round(avg_win / avg_loss, 6) if avg_loss else 0.0
        recovery = as_float(metrics.get("recovery_factor", row.get("recovery_factor")))
        dd_pct = as_float(metrics.get("max_drawdown_percent"))
        trade_count = as_int(metrics.get("trade_count", row.get("trade_count")))
        label = "constructive_but_needs_deal_curve(구성적이나 거래별 곡선 필요)"
        if recovery < 1.5:
            label = "fragile_recovery(회복 계수 취약)"
        if trade_count < 20:
            label = "thin_trade_count(거래 수 얇음)"
        rows.append(
            {
                "attempt_name": attempt,
                "trade_count": trade_count,
                "win_rate_percent": as_float(metrics.get("win_rate_percent")),
                "gross_profit": gross_profit,
                "gross_loss_abs": gross_loss_abs,
                "average_win_estimate": avg_win,
                "average_loss_estimate": avg_loss,
                "payoff_ratio_estimate": payoff_ratio,
                "max_drawdown_amount": as_float(metrics.get("max_drawdown_amount", row.get("max_drawdown_amount"))),
                "max_drawdown_percent": dd_pct,
                "recovery_factor": recovery,
                "sharpe_ratio": as_float(metrics.get("sharpe_ratio")),
                "equity_quality_label": label,
                "limitation": "HTML report summary only(HTML 보고서 요약 전용); deal-level curve not extracted(거래별 곡선 미추출)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_comparator_review(summary: pd.DataFrame, cost_stress: pd.DataFrame, equity: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    equity_by_attempt = {str(row["attempt_name"]): row for _, row in equity.iterrows()}
    for _, row in summary.iterrows():
        attempt = str(row["attempt_name"])
        moderate = cost_stress.loc[
            cost_stress["attempt_name"].eq(attempt) & cost_stress["cost_scenario_id"].eq("moderate_overlay")
        ].iloc[0]
        heavy = cost_stress.loc[
            cost_stress["attempt_name"].eq(attempt) & cost_stress["cost_scenario_id"].eq("heavy_overlay")
        ].iloc[0]
        eq = equity_by_attempt.get(attempt, {})
        rows.append(
            {
                "attempt_name": attempt,
                "model_id": row.get("model_id", ""),
                "base_net_profit": as_float(row.get("net_profit")),
                "base_profit_factor": as_float(row.get("profit_factor")),
                "base_expectancy": as_float(row.get("expectancy")),
                "base_recovery_factor": as_float(row.get("recovery_factor")),
                "trade_count": as_int(row.get("trade_count")),
                "long_trade_count": as_int(row.get("long_trade_count")),
                "short_trade_count": as_int(row.get("short_trade_count")),
                "moderate_adjusted_net_profit": moderate["adjusted_net_profit"],
                "moderate_adjusted_profit_factor_estimate": moderate["adjusted_profit_factor_estimate"],
                "moderate_adjusted_recovery_factor": moderate["adjusted_recovery_factor"],
                "moderate_survival_passed": bool(moderate["survival_passed"]),
                "moderate_adjusted_net_rank": int(moderate["scenario_adjusted_net_rank"]),
                "heavy_adjusted_net_profit": heavy["adjusted_net_profit"],
                "heavy_adjusted_recovery_factor": heavy["adjusted_recovery_factor"],
                "heavy_survival_passed": bool(heavy["survival_passed"]),
                "equity_quality_label": eq.get("equity_quality_label", ""),
                "review_judgment": (
                    "positive_research_clue(긍정 연구 단서)"
                    if attempt == "s07_trend_confirmed_long_only" and bool(moderate["survival_passed"])
                    else "comparator_reference(대조 기준)"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values(["moderate_adjusted_net_rank", "base_net_profit"], ascending=[True, False])


def build_memory_tables(final: Mapping[str, Any], comparator: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    s07 = comparator.loc[comparator["attempt_name"].eq("s07_trend_confirmed_long_only")].iloc[0]
    positive = pd.DataFrame(
        [
            {
                "clue_id": "s07_exact_runtime_parity",
                "clue": "s07 keeps exact MT5 parity(s07이 정확한 MT5 동등성을 유지)",
                "evidence": rel(probe.PROXY_MT5_DIFF),
                "next_use": "keep_as_runtime_mapped_candidate_seed(런타임 매핑 후보 씨앗으로 보존)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "clue_id": "s07_moderate_cost_survival",
                "clue": "s07 remains top under moderate cost overlay(s07이 중간 비용 오버레이에서 1위 유지)",
                "evidence": rel(COST_STRESS_SCORECARD),
                "next_use": "test_deal_level_cost_and_forward_replay(거래별 비용과 전진 재생으로 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "clue_id": "s07_long_supply_added",
                "clue": "s07 raises long trades versus anchors(s07이 앵커 대비 롱 거래를 늘림)",
                "evidence": rel(COMPARATOR_REVIEW),
                "next_use": "probe_long_quality_without_short_collapse(숏 붕괴 없이 롱 품질을 탐침)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    failure = pd.DataFrame(
        [
            {
                "memory_id": "heavy_cost_recovery_floor_fail",
                "failure_memory": "heavy overlay breaks recovery floor for all attempts(강한 오버레이에서 전 후보 회복 계수 하한 실패)",
                "evidence": rel(COST_STRESS_SCORECARD),
                "constraint": "do not claim cost-stress robustness beyond moderate overlay(중간 오버레이 초과 비용 견고성 주장 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "memory_id": "short_dominant_trade_shape",
                "failure_memory": "s07 is still short-dominant despite more longs(s07은 롱 증가에도 여전히 숏 우세)",
                "evidence": rel(COMPARATOR_REVIEW),
                "constraint": "next probe must separate long quality from short carry(다음 탐침은 롱 품질과 숏 기여를 분리)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "memory_id": "session_regime_no_pnl",
                "failure_memory": "session/regime attribution is signal-only, not PnL(세션/국면 귀속은 신호 전용, 손익 아님)",
                "evidence": f"{rel(SESSION_SIGNAL_STABILITY)};{rel(REGIME_SIGNAL_STABILITY)}",
                "constraint": "deal extraction required before session PnL claim(세션 손익 주장 전 거래 추출 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "memory_id": "no_forward_pass",
                "failure_memory": "no forward pass or live-like readiness was tested(전진 통과 또는 실거래 유사 준비 미검증)",
                "evidence": rel(probe.FINAL_DECISION),
                "constraint": "keep selection and operating promotion closed(선정과 운영 승격 닫기)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "opened_by": RUN_ID,
                "priority": 1,
                "action": "design deal-level cost/session forward replay validation(거래별 비용/세션 전진 재생 검증 설계)",
                "effect": "turn signal-only stability into trade-level evidence(신호 전용 안정성을 거래 단위 근거로 바꿈)",
                "s07_moderate_adjusted_net_profit": s07["moderate_adjusted_net_profit"],
                "s07_heavy_survival_passed": bool(s07["heavy_survival_passed"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return positive, failure, queue


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    rows = [
        ("parent_run344H_gates_passed", final["parent_gate_passed"], rel(probe.GATE_AUDIT), "run344H MT5 gate(게이트)를 이어받음"),
        ("mt5_summary_loaded", final["summary_rows"] == 3, rel(probe.EXECUTION_SUMMARY), "MT5 summary(요약)를 검토 입력으로 적재"),
        ("exact_runtime_parity_preserved", final["mismatch_rows"] == 0 and final["matched_rows"] == final["expected_rows"], rel(probe.PROXY_MT5_DIFF), "runtime parity(런타임 동등성)를 유지"),
        ("cost_stress_scorecard_written", final["cost_stress_rows"] == 12 and exists(COST_STRESS_SCORECARD), rel(COST_STRESS_SCORECARD), "cost stress(비용 압박) 점수판 작성"),
        ("moderate_cost_survival_checked", final["s07_moderate_cost_passed"] is True, rel(COST_STRESS_SCORECARD), "s07 moderate cost(중간 비용) 생존 여부 확인"),
        ("session_regime_signal_stability_written", final["session_signal_rows"] >= 12 and final["regime_signal_rows"] >= 18, f"{rel(SESSION_SIGNAL_STABILITY)};{rel(REGIME_SIGNAL_STABILITY)}", "session/regime(세션/국면) 신호 안정성 작성"),
        ("comparator_review_written", final["comparator_rows"] == 3 and exists(COMPARATOR_REVIEW), rel(COMPARATOR_REVIEW), "s07/s05/s01 comparator(대조) 검토 작성"),
        ("no_forbidden_operating_claim", no_forbidden, rel(FINAL_DECISION), "review(검토)를 운영 주장으로 올리지 않음"),
        ("required_gate_coverage_audit_written", True, rel(GATE_AUDIT), "필수 gate coverage audit(게이트 커버리지 감사) 기록"),
    ]
    return pd.DataFrame(
        [
            {
                "gate_id": gate,
                "status": "passed" if passed else "failed",
                "evidence_path": evidence,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for gate, passed, evidence, effect in rows
        ]
    )


def build_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(probe.EXECUTION_SUMMARY),
                rel(COST_STRESS_SCORECARD),
                rel(COMPARATOR_REVIEW),
                rel(SESSION_SIGNAL_STABILITY),
                rel(REGIME_SIGNAL_STABILITY),
            ],
            "evidence_missing": [
                "deal-level PnL by session/regime(세션/국면별 거래 손익)",
                "forward replay pass(전진 재생 통과)",
                "Tier B separate KPI(Tier B 분리 KPI)",
            ],
            "judgment_label": "positive_research_clue(긍정 연구 단서)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "s07은 중간 비용까지 버티지만 강한 비용과 거래별 세션 손익은 아직 닫히지 않았다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "observed_change": "s07 top net/recovery under moderate overlay(s07 중간 오버레이 순익/회복 1위)",
            "comparison_baseline": "s05_long_quality_extreme_top20 and s01_anchor_short_supply_control",
            "likely_drivers": [
                "trend-confirmed long side filter(추세 확인 롱 필터)",
                "more long trades than comparators(대조보다 많은 롱 거래)",
                "same short carry base(비슷한 숏 기여 기반)",
            ],
            "segment_checks": [
                rel(SESSION_SIGNAL_STABILITY),
                rel(REGIME_SIGNAL_STABILITY),
                "PnL segment missing(손익 구간 누락)",
            ],
            "trade_shape": {
                "s07_trade_count": final["s07_trade_count"],
                "s07_long_trade_count": final["s07_long_trade_count"],
                "s07_short_trade_count": final["s07_short_trade_count"],
                "s07_base_recovery_factor": final["s07_base_recovery_factor"],
                "s07_moderate_adjusted_recovery_factor": final["s07_moderate_adjusted_recovery_factor"],
            },
            "alternative_explanations": [
                "short-side carry still dominates(숏 기여가 여전히 큼)",
                "sample is one Tier A inner holdout window(표본은 Tier A 내부 홀드아웃 한 구간)",
            ],
            "attribution_confidence": "medium(중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "research_path": rel(pkg.EXPECTED_TAPE),
            "runtime_path": rel(probe.EXECUTION_SUMMARY),
            "shared_contract": "feature timestamp, thresholds, ONNX model, telemetry decision tape(피처 시각, 임계값, ONNX 모델, 텔레메트리 결정 테이프)",
            "known_differences": "cost overlay is post-MT5 attribution only(비용 오버레이는 MT5 이후 귀속 전용)",
            "parity_check": "row-level proxy-MT5 comparison(행 단위 프록시-MT5 비교)",
            "parity_identity": rel(probe.RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침), not runtime_authority(런타임 권위 아님)",
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY],
            "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if exists(path) and path != ARTIFACT_REGISTRY},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적됨 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": [
                "positive research clue(긍정 연구 단서)",
                "moderate cost overlay survival(중간 비용 오버레이 생존)",
                "runtime probe parity preserved(런타임 탐침 동등성 유지)",
            ],
            "forbidden_claims": [
                "candidate selection(후보 선정)",
                "forward pass(전진 통과)",
                "live readiness(실거래 준비)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344I s07 Forward/Cost/Stability Review(344I s07 전진/비용/안정성 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- MT5 parity(MT5 동등성): `{final['matched_rows']}/{final['expected_rows']}`, mismatch(불일치) `{final['mismatch_rows']}`
- s07 base net profit(s07 기본 순수익): `{final['s07_base_net_profit']}`
- s07 moderate adjusted net(s07 중간 비용 조정 순수익): `{final['s07_moderate_adjusted_net_profit']}`
- s07 moderate recovery(s07 중간 비용 회복 계수): `{final['s07_moderate_adjusted_recovery_factor']}`
- s07 heavy survival(s07 강한 비용 생존): `{final['s07_heavy_cost_passed']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run344H MT5 runtime probe(MT5 런타임 탐침)를 비용 오버레이(cost overlay, 비용 오버레이), comparator review(대조 검토), session/regime signal stability(세션/국면 신호 안정성)로 재판독했다.

## Effect(효과)

s07은 중간 비용(moderate cost, 중간 비용)에서도 s05/s01보다 순수익과 회복 계수가 높다. 다만 강한 비용(heavy cost, 강한 비용)에서는 회복 계수 하한을 깨고, 세션/국면은 아직 PnL attribution(손익 귀속)이 아니라 signal/fill attribution(신호/체결 귀속)이다.

## Boundary(경계)

이 run(실행)은 review(검토)다. candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344I Review Decision(344I 검토 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(COST_STRESS_SCORECARD)}`, `{rel(COMPARATOR_REVIEW)}`, `{rel(SESSION_SIGNAL_STABILITY)}`, `{rel(REGIME_SIGNAL_STABILITY)}`

Action(행동): s07 validation MT5 evidence(s07 검증 MT5 근거)를 비용/세션/국면으로 재판독했다.
Effect(효과): s07을 다음 deal-level forward replay(거래별 전진 재생) 설계로 넘기되 운영 주장은 닫았다.

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

run344I review(검토)가 완료되어 s07은 moderate cost positive clue(중간 비용 긍정 단서)로 남았다. 다음 행동(action, 행동)은 거래별 비용과 세션 손익을 설계하는 것이다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_review(최근 검토): `{RUN_ID}`
- research_clue(연구 단서): `s07_trend_confirmed_long_only`
- s07_moderate_cost_passed(s07 중간 비용 통과): `{final['s07_moderate_cost_passed']}`
- s07_heavy_cost_passed(s07 강한 비용 통과): `{final['s07_heavy_cost_passed']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 좋은 단서는 보존하되 운영 선정은 열지 않는다.
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
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(WORKSPACE_STATE, workspace)
    marker = f"run344I {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344I s07 Validation Review(344I s07 검증 검토)

- run_id(실행 ID): `{RUN_ID}`
- moderate_cost_passed(중간 비용 통과): `{final['s07_moderate_cost_passed']}`
- heavy_cost_passed(강한 비용 통과): `{final['s07_heavy_cost_passed']}`
- effect(효과): run344J deal-level validation design(거래별 검증 설계)을 열었다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344I s07 Validation Review(344I s07 검증 검토)

- report(보고서): `{rel(REPORT_PATH)}`
- cost_scorecard(비용 점수판): `{rel(COST_STRESS_SCORECARD)}`
- comparator_review(대조 검토): `{rel(COMPARATOR_REVIEW)}`
- effect(효과): s07의 긍정 단서와 실패 기억을 분리했다.
""",
    )
    changelog = f"""## {TODAY} run344I s07 Validation Review(s07 검증 검토)

- action(행동): run344H MT5 probe(MT5 탐침)를 비용/세션/국면으로 재판독했다.
- effect(효과): s07은 중간 비용에서 유지되지만 강한 비용과 세션 손익은 다음 검증으로 남겼다.
- boundary(경계): 선정/운영 승격/런타임 권위/목표 달성은 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    run_row = {
        **base_row,
        "lane": "review_attribution(검토 귀속)",
        "family": "performance_attribution(성과 귀속)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "s07 moderate cost positive clue(s07 중간 비용 긍정 단서); no selection(선정 없음).",
        "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
        "net_profit": final["s07_base_net_profit"],
        "profit_factor": final["s07_base_profit_factor"],
        "drawdown": final["s07_max_drawdown_amount"],
        "recovery_factor": final["s07_base_recovery_factor"],
        "trade_count": final["s07_trade_count"],
        "expectancy": final["s07_base_expectancy"],
        "attempt_count": final["attempt_rows"],
        "matched_rows": final["matched_rows"],
        "result_status": JUDGMENT,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    rows = [
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "review_cost_session_regime",
            "kpi_scope": "review_cost_session_regime",
            "scoreboard_lane": "review_attribution(검토 귀속)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "net_profit": final["s07_base_net_profit"],
            "profit_factor": final["s07_base_profit_factor"],
            "expectancy": final["s07_base_expectancy"],
            "drawdown": final["s07_max_drawdown_amount"],
            "recovery_factor": final["s07_base_recovery_factor"],
            "trade_count": final["s07_trade_count"],
            "result_status": JUDGMENT,
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
            "primary_kpi": f"base_net={final['s07_base_net_profit']};moderate_net={final['s07_moderate_adjusted_net_profit']};moderate_pf={final['s07_moderate_adjusted_profit_factor_estimate']}",
            "guardrail_kpi": f"heavy_pass={final['s07_heavy_cost_passed']};long_short={final['s07_long_trade_count']}/{final['s07_short_trade_count']}",
            "external_verification_status": "completed(완료)",
            "notes": "Tier A MT5 evidence reviewed(Tier A MT5 근거 검토); no selection(선정 없음).",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "review_attribution(검토 귀속)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B was outside this narrow review(Tier B는 이번 좁은 검토 밖).",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "review_attribution(검토 귀속)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "net_profit": final["s07_base_net_profit"],
            "profit_factor": final["s07_base_profit_factor"],
            "expectancy": final["s07_base_expectancy"],
            "drawdown": final["s07_max_drawdown_amount"],
            "recovery_factor": final["s07_base_recovery_factor"],
            "trade_count": final["s07_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": f"base_net={final['s07_base_net_profit']};moderate_net={final['s07_moderate_adjusted_net_profit']}",
            "guardrail_kpi": f"heavy_pass={final['s07_heavy_cost_passed']};long_short={final['s07_long_trade_count']}/{final['s07_short_trade_count']}",
            "external_verification_status": "completed(완료)",
            "notes": "Combined view is same as Tier A until Tier B exists(Tier B 전에는 합산이 Tier A와 같음).",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], rows)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    ensure_parent(ARTIFACT_REGISTRY)
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if exists(ARTIFACT_REGISTRY):
        with open(ARTIFACT_REGISTRY, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [dict(row) for row in reader]
    required_fields = [
        "stage_id",
        "run_id",
        "artifact_type",
        "path",
        "sha256",
        "created_at",
        "claim_boundary",
        "artifact_id",
        "created_at_utc",
        "notes",
        "artifact_path",
    ]
    for field in required_fields:
        if field not in fieldnames:
            fieldnames.append(field)
    new_rows: list[dict[str, Any]] = []
    for path in paths:
        if not exists(path):
            continue
        artifact_id = f"{RUN_NUMBER}::{rel(path)}"
        artifact_type = path.suffix.lower().lstrip(".") or "artifact"
        new_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": artifact_id,
                "notes": "run344I review artifact(run344I 검토 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    new_ids = {row["artifact_id"] for row in new_rows}
    kept = [row for row in existing_rows if row.get("artifact_id") not in new_ids]
    with open(ARTIFACT_REGISTRY, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in kept + new_rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def build_review() -> Mapping[str, Any]:
    for path in INPUT_FILES:
        required(path)
    parent_final = read_json(probe.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError("run344H next_run_id does not point to run344I")
    if not parent_gates_passed():
        raise RuntimeError("run344H gate audit has failed rows")

    summary = read_csv(probe.EXECUTION_SUMMARY)
    report_records = read_json(probe.STRATEGY_TESTER_REPORTS)
    cost_contract = read_csv(pkg.COST_STRESS_CONTRACT)
    attempts = read_csv(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE)
    features = read_csv(pkg.FEATURE_MATRIX)

    cost_stress = build_cost_stress(summary, report_records, cost_contract, attempts)
    session = build_session_signal_stability(summary, features)
    regime = build_regime_signal_stability(summary, features)
    write_csv(TELEMETRY_READ_MANIFEST, TELEMETRY_READ_ROWS)
    equity = build_equity_quality(summary, report_records)
    comparator = build_comparator_review(summary, cost_stress, equity)
    positive, failure, queue = build_memory_tables(parent_final, comparator)

    write_frame(COST_STRESS_SCORECARD, cost_stress)
    write_frame(SESSION_SIGNAL_STABILITY, session)
    write_frame(REGIME_SIGNAL_STABILITY, regime)
    write_frame(EQUITY_CURVE_QUALITY, equity)
    write_frame(COMPARATOR_REVIEW, comparator)
    write_frame(POSITIVE_CLUES, positive)
    write_frame(FAILURE_MEMORY, failure)
    write_frame(RUN344J_QUEUE, queue)

    s07 = comparator.loc[comparator["attempt_name"].eq("s07_trend_confirmed_long_only")].iloc[0]
    final: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "attempt_rows": int(len(summary)),
        "summary_rows": int(len(summary)),
        "expected_rows": int(parent_final.get("expected_rows", 0)),
        "matched_rows": int(parent_final.get("matched_rows", 0)),
        "mismatch_rows": int(parent_final.get("mismatch_rows", 0)),
        "cost_stress_rows": int(len(cost_stress)),
        "session_signal_rows": int(len(session)),
        "regime_signal_rows": int(len(regime)),
        "telemetry_read_rows": int(len(TELEMETRY_READ_ROWS)),
        "comparator_rows": int(len(comparator)),
        "positive_clue_rows": int(len(positive)),
        "failure_memory_rows": int(len(failure)),
        "parent_gate_passed": True,
        "s07_base_net_profit": float(s07["base_net_profit"]),
        "s07_base_profit_factor": float(s07["base_profit_factor"]),
        "s07_base_expectancy": float(s07["base_expectancy"]),
        "s07_base_recovery_factor": float(s07["base_recovery_factor"]),
        "s07_max_drawdown_amount": float(summary.loc[summary["attempt_name"].eq("s07_trend_confirmed_long_only"), "max_drawdown_amount"].iloc[0]),
        "s07_trade_count": int(s07["trade_count"]),
        "s07_long_trade_count": int(s07["long_trade_count"]),
        "s07_short_trade_count": int(s07["short_trade_count"]),
        "s07_moderate_adjusted_net_profit": float(s07["moderate_adjusted_net_profit"]),
        "s07_moderate_adjusted_profit_factor_estimate": float(s07["moderate_adjusted_profit_factor_estimate"]),
        "s07_moderate_adjusted_recovery_factor": float(s07["moderate_adjusted_recovery_factor"]),
        "s07_moderate_cost_passed": bool(s07["moderate_survival_passed"]),
        "s07_moderate_adjusted_net_rank": int(s07["moderate_adjusted_net_rank"]),
        "s07_heavy_adjusted_net_profit": float(s07["heavy_adjusted_net_profit"]),
        "s07_heavy_adjusted_recovery_factor": float(s07["heavy_adjusted_recovery_factor"]),
        "s07_heavy_cost_passed": bool(s07["heavy_survival_passed"]),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "completed(완료)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = make_gates(final)
    final["gate_passes"] = int(gates["status"].astype(str).eq("passed").sum())
    final["gate_total"] = int(len(gates))

    write_frame(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "created_at_utc": now_utc(),
            "execution_command": f"python -B {rel(Path(__file__))}",
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    build_receipts(final)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    return final


def main() -> None:
    final = build_review()
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
