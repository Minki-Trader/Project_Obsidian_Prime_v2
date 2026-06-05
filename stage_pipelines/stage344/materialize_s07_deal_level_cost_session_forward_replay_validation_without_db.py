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

from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402
from stage_pipelines.stage344 import (  # noqa: E402
    design_s07_deal_level_cost_session_forward_replay_validation_without_db as design,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_s07_forward_cost_stability_validation_package_without_db as pkg,
)


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344K"
RUN_ID = "run344K_materialize_s07_deal_level_cost_session_forward_replay_validation_without_db_v1"
PARENT_RUN_ID = design.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
SOURCE_RUNTIME_RUN_ID = design.SOURCE_RUNTIME_RUN_ID
NEXT_RUN_ID = "run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1"

STATUS = "completed_stage344K_deal_level_cost_session_forward_replay_materialized_review_required_no_selection"
JUDGMENT = "deal_level_cost_session_regime_outputs_available_review_required_no_operating_claim"
DECISION = "stage344K_open_run344L_review_deal_level_cost_session_forward_replay_validation"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_deal_level_cost_session_forward_replay_validation_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344K_s07_deal_level_cost_session_forward_replay_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344K_s07_deal_level_cost_session_forward_replay_materialization.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

TRADE_LEVEL_RECORDS = RUN_DIR / "trade_level_records.csv"
SESSION_PNL_SCORECARD = RUN_DIR / "session_pnl_scorecard.csv"
REGIME_PNL_SCORECARD = RUN_DIR / "regime_pnl_scorecard.csv"
DIRECTION_PNL_SCORECARD = RUN_DIR / "direction_pnl_scorecard.csv"
COST_REPLAY_SCORECARD = RUN_DIR / "cost_replay_scorecard.csv"
EQUITY_CURVE_REPLAY = RUN_DIR / "equity_curve_replay.csv"
MATERIALIZATION_SUMMARY = RUN_DIR / "materialization_summary.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
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

SOURCE_PARENT_FINAL = design.FINAL_DECISION
SOURCE_PARENT_GATES = design.GATE_AUDIT
SOURCE_PARENT_QUEUE = design.RUN344K_QUEUE
SOURCE_PARENT_FEASIBILITY = design.DEAL_EXTRACTION_FEASIBILITY
SOURCE_PARENT_EXTRACTION_CONTRACT = design.DEAL_LEVEL_EXTRACTION_CONTRACT
SOURCE_PARENT_SESSION_PLAN = design.SESSION_PNL_JOIN_PLAN
SOURCE_PARENT_COST_CONTRACT = design.COST_REPLAY_CONTRACT
SOURCE_RUNTIME_REPORTS = design.SOURCE_RUNTIME_REPORTS
SOURCE_RUNTIME_SUMMARY = design.SOURCE_RUNTIME_SUMMARY
SOURCE_RUNTIME_DIFF = design.SOURCE_RUNTIME_DIFF
SOURCE_RUNTIME_IDENTITY = design.SOURCE_RUNTIME_IDENTITY
SOURCE_FEATURES = design.SOURCE_FEATURES

INPUT_FILES = (
    SOURCE_PARENT_FINAL,
    SOURCE_PARENT_GATES,
    SOURCE_PARENT_QUEUE,
    SOURCE_PARENT_FEASIBILITY,
    SOURCE_PARENT_EXTRACTION_CONTRACT,
    SOURCE_PARENT_SESSION_PLAN,
    SOURCE_PARENT_COST_CONTRACT,
    SOURCE_RUNTIME_REPORTS,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_RUNTIME_DIFF,
    SOURCE_RUNTIME_IDENTITY,
    SOURCE_FEATURES,
)

OUTPUT_FILES = (
    TRADE_LEVEL_RECORDS,
    SESSION_PNL_SCORECARD,
    REGIME_PNL_SCORECARD,
    DIRECTION_PNL_SCORECARD,
    COST_REPLAY_SCORECARD,
    EQUITY_CURVE_REPLAY,
    MATERIALIZATION_SUMMARY,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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
REGIME_BUCKETS = ("low(낮음)", "mid(중간)", "high(높음)")


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path) -> bool:
    return pkg.path_is_file(path)


def ensure_parent(path: Path) -> None:
    pkg.ensure_parent(path)


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
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
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


def parent_gates_passed() -> bool:
    gates = read_csv(SOURCE_PARENT_GATES)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def session_bucket(minutes: Any) -> str:
    value = as_float(minutes, -10_000.0)
    if value < 0:
        return SESSION_BUCKETS[0]
    if value < 60:
        return SESSION_BUCKETS[1]
    if value < 210:
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


def pf_from_values(values: Sequence[float]) -> float:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = abs(sum(value for value in values if value < 0))
    if gross_loss == 0:
        return 0.0
    return round(gross_profit / gross_loss, 6)


def score_values(values: Sequence[float]) -> dict[str, Any]:
    vals = [float(value) for value in values]
    wins = [value for value in vals if value > 0]
    losses = [value for value in vals if value < 0]
    return {
        "trade_count": len(vals),
        "net_profit": round(sum(vals), 6),
        "gross_profit": round(sum(wins), 6),
        "gross_loss": round(sum(losses), 6),
        "profit_factor_estimate": pf_from_values(vals),
        "expectancy": round(sum(vals) / len(vals), 6) if vals else 0.0,
        "win_rate": round(len(wins) / len(vals), 6) if vals else 0.0,
    }


def prepare_features(features: pd.DataFrame) -> pd.DataFrame:
    out = features.copy()
    out["timestamp_key"] = out["timestamp"].astype(str)
    for column in ("minutes_from_cash_open", "adx_14", "historical_vol_20", "di_spread_14"):
        if column not in out.columns:
            out[column] = pd.NA
        out[column] = pd.to_numeric(out[column], errors="coerce")
    return out.drop_duplicates("timestamp_key", keep="last").set_index("timestamp_key")


def regime_edges(features: pd.DataFrame) -> dict[str, tuple[float, float]]:
    edges: dict[str, tuple[float, float]] = {}
    for column in ("adx_14", "historical_vol_20"):
        valid = pd.to_numeric(features[column], errors="coerce").dropna()
        low, high = valid.quantile([0.333333, 0.666667]).tolist()
        edges[column] = (float(low), float(high))
    return edges


def report_path(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def build_trade_records(
    summary: pd.DataFrame,
    report_records: Sequence[Mapping[str, Any]],
    features: pd.DataFrame,
) -> pd.DataFrame:
    feature_index = prepare_features(features)
    edges = regime_edges(features)
    model_by_attempt = dict(zip(summary["attempt_name"].astype(str), summary["model_id"].astype(str)))
    rows: list[dict[str, Any]] = []
    for record in report_records:
        attempt = str(record.get("attempt_name", ""))
        parsed = parse_mt5_trade_report(report_path(record))
        trades = pair_deals_into_trades(parsed["deals"])
        for trade in trades:
            key = trade.open_time.strftime("%Y.%m.%d %H:%M:%S")
            feature = feature_index.loc[key] if key in feature_index.index else pd.Series(dtype="float64")
            minutes = feature.get("minutes_from_cash_open", pd.NA)
            adx = feature.get("adx_14", pd.NA)
            vol = feature.get("historical_vol_20", pd.NA)
            adx_low, adx_high = edges["adx_14"]
            vol_low, vol_high = edges["historical_vol_20"]
            rows.append(
                {
                    "attempt_name": attempt,
                    "model_id": model_by_attempt.get(attempt, ""),
                    "trade_index": trade.index,
                    "direction": trade.direction,
                    "open_time": key,
                    "close_time": trade.close_time.strftime("%Y.%m.%d %H:%M:%S"),
                    "hold_bars": round((trade.close_time - trade.open_time).total_seconds() / 60.0 / 5.0, 6),
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": round(trade.gross_profit, 6),
                    "net_profit": round(trade.net_profit, 6),
                    "swap": round(trade.swap, 6),
                    "commission": round(trade.commission, 6),
                    "entry_feature_match": key in feature_index.index,
                    "minutes_from_cash_open": as_float(minutes, 0.0),
                    "session_bucket": session_bucket(minutes),
                    "adx_14": as_float(adx, 0.0),
                    "historical_vol_20": as_float(vol, 0.0),
                    "adx_bucket": quantile_bucket(adx, adx_low, adx_high),
                    "historical_vol_bucket": quantile_bucket(vol, vol_low, vol_high),
                    "attribution_time_policy": "entry_time(진입 시각)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def grouped_score(frame: pd.DataFrame, group_columns: Sequence[str], value_column: str = "net_profit") -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for keys, group in frame.groupby(list(group_columns), dropna=False):
        key_tuple = keys if isinstance(keys, tuple) else (keys,)
        payload = {column: key_tuple[index] for index, column in enumerate(group_columns)}
        scores = score_values(group[value_column].astype(float).tolist())
        long_net = round(group.loc[group["direction"].eq("buy"), value_column].astype(float).sum(), 6)
        short_net = round(group.loc[group["direction"].eq("sell"), value_column].astype(float).sum(), 6)
        rows.append(
            {
                **payload,
                **scores,
                "long_net_profit": long_net,
                "short_net_profit": short_net,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_regime_scores(trades: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for column, label in (("adx_bucket", "adx_14(ADX 14)"), ("historical_vol_bucket", "historical_vol_20(20봉 역사 변동성)")):
        frame = grouped_score(trades, ["attempt_name", column]).rename(columns={column: "segment_bucket"})
        frame.insert(1, "regime_dimension", label)
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def build_cost_replay(trades: pd.DataFrame, summary: pd.DataFrame, cost_contract: pd.DataFrame) -> pd.DataFrame:
    max_dd_by_attempt = dict(zip(summary["attempt_name"].astype(str), summary["max_drawdown_amount"].map(as_float)))
    rows: list[dict[str, Any]] = []
    for attempt, group in trades.groupby("attempt_name", dropna=False):
        base_values = group["net_profit"].astype(float).tolist()
        max_dd = max_dd_by_attempt.get(str(attempt), 0.0)
        for _, scenario in cost_contract.iterrows():
            cost = as_float(scenario.get("cost_per_closed_trade_account_currency"))
            adjusted = [value - cost for value in base_values]
            scores = score_values(adjusted)
            recovery = round(scores["net_profit"] / max_dd, 6) if max_dd else 0.0
            survival = scores["net_profit"] > 0 and scores["profit_factor_estimate"] >= 1.5 and recovery >= 1.0
            rows.append(
                {
                    "attempt_name": attempt,
                    "scenario_id": scenario.get("scenario_id", ""),
                    "cost_per_closed_trade_account_currency": cost,
                    "base_trade_count": len(base_values),
                    "base_net_profit": round(sum(base_values), 6),
                    "adjusted_net_profit": scores["net_profit"],
                    "adjusted_profit_factor_estimate": scores["profit_factor_estimate"],
                    "adjusted_expectancy": scores["expectancy"],
                    "max_drawdown_amount": max_dd,
                    "adjusted_recovery_factor": recovery,
                    "survival_passed": survival,
                    "survival_status": "passed(통과)" if survival else "failed(실패)",
                    "success_floor": scenario.get("success_floor", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    out = pd.DataFrame(rows)
    out["scenario_adjusted_net_rank"] = out.groupby("scenario_id")["adjusted_net_profit"].rank(method="dense", ascending=False).astype(int)
    return out


def build_equity_curve(trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for attempt, group in trades.sort_values(["attempt_name", "close_time", "trade_index"]).groupby("attempt_name", dropna=False):
        cumulative = 0.0
        peak = 0.0
        for _, row in group.iterrows():
            cumulative += as_float(row["net_profit"])
            peak = max(peak, cumulative)
            drawdown = cumulative - peak
            rows.append(
                {
                    "attempt_name": attempt,
                    "trade_index": int(row["trade_index"]),
                    "close_time": row["close_time"],
                    "net_profit": row["net_profit"],
                    "cumulative_net_profit": round(cumulative, 6),
                    "close_to_close_drawdown": round(drawdown, 6),
                    "curve_authority": "closed_trade_replay_only(청산 거래 재생 전용)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    rows = [
        ("parent_run344J_gates_passed", final["parent_gate_passed"], rel(SOURCE_PARENT_GATES), "run344J gate(게이트)를 이어받음"),
        ("trade_records_materialized", final["trade_record_rows"] == final["expected_trade_rows"], rel(TRADE_LEVEL_RECORDS), "거래별 기록 작성"),
        ("s07_net_matches_report", abs(final["s07_net_profit_diff"]) < 1e-9, rel(MATERIALIZATION_SUMMARY), "s07 거래별 순손익이 MT5 보고서와 일치"),
        ("entry_feature_join_complete", final["entry_feature_missing_rows"] == 0, rel(TRADE_LEVEL_RECORDS), "진입 시각 피처 조인 완료"),
        ("session_pnl_scorecard_written", final["session_pnl_rows"] >= 3, rel(SESSION_PNL_SCORECARD), "세션별 손익 점수판 작성"),
        ("regime_pnl_scorecard_written", final["regime_pnl_rows"] >= 6, rel(REGIME_PNL_SCORECARD), "국면별 손익 점수판 작성"),
        ("cost_replay_scorecard_written", final["cost_replay_rows"] == 12, rel(COST_REPLAY_SCORECARD), "거래별 비용 재생 점수판 작성"),
        ("equity_curve_replay_written", final["equity_curve_rows"] == final["trade_record_rows"], rel(EQUITY_CURVE_REPLAY), "청산 거래 수익곡선 재생 작성"),
        ("no_forbidden_operating_claim", no_forbidden, rel(FINAL_DECISION), "물질화를 운영 주장으로 올리지 않음"),
        ("required_gate_coverage_audit_written", True, rel(GATE_AUDIT), "필수 gate coverage audit(게이트 커버리지 감사) 기록"),
    ]
    return pd.DataFrame(
        [
            {"gate_id": gate, "status": "passed" if passed else "failed", "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
            for gate, passed, evidence, effect in rows
        ]
    )


def build_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        DATA_RECEIPT,
        {
            "data_source": [rel(SOURCE_RUNTIME_REPORTS), rel(SOURCE_FEATURES)],
            "time_axis": "entry_time joins to runtime feature timestamp(진입 시각을 런타임 피처 시각에 조인)",
            "sample_scope": f"trade_rows={final['trade_record_rows']}; Tier A US100 M5",
            "missing_or_duplicate_check": f"entry_feature_missing_rows={final['entry_feature_missing_rows']}",
            "feature_label_boundary": "no new feature or label; existing runtime features only(새 피처/라벨 없음, 기존 런타임 피처만)",
            "split_boundary": "inner holdout runtime probe materialization only(내부 홀드아웃 런타임 탐침 물질화 전용)",
            "leakage_risk": "post-hoc s07 review remains; no selection claim(사후 s07 검토 위험 유지, 선정 주장 없음)",
            "data_hash_or_identity": f"features_sha256={sha256_file(SOURCE_FEATURES)}",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(SOURCE_RUNTIME_REPORTS), rel(SOURCE_RUNTIME_IDENTITY)],
            "shared_contract": "run344H MT5 report trades and run344G feature timestamps(run344H MT5 거래와 run344G 피처 시각)",
            "known_differences": "no new MT5 execution; Python recomputation from reports(새 MT5 실행 없음, 보고서 기반 파이썬 재계산)",
            "parity_check": rel(SOURCE_RUNTIME_DIFF),
            "parity_identity": rel(SOURCE_RUNTIME_IDENTITY),
            "runtime_claim_boundary": "materialization_only_no_runtime_authority(물질화 전용, 런타임 권위 없음)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "observed_change": "signal-only buckets converted to trade-level PnL buckets(신호 전용 버킷을 거래별 손익 버킷으로 전환)",
            "comparison_baseline": "run344I review scorecards(run344I 검토 점수판)",
            "likely_drivers": "trade direction, session, adx and volatility bucket(거래 방향, 세션, ADX와 변동성 버킷)",
            "segment_checks": [rel(SESSION_PNL_SCORECARD), rel(REGIME_PNL_SCORECARD), rel(DIRECTION_PNL_SCORECARD)],
            "trade_shape": f"s07_trades={final['s07_trade_count']};s07_net={final['s07_net_profit']}",
            "alternative_explanations": "single-window and short carry concentration(단일 구간과 숏 기여 집중)",
            "attribution_confidence": "medium_pending_review(검토 전 중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(TRADE_LEVEL_RECORDS), rel(SESSION_PNL_SCORECARD), rel(REGIME_PNL_SCORECARD), rel(COST_REPLAY_SCORECARD)],
            "evidence_missing": ["review judgment(run344L 검토 판정)", "forward pass(전진 통과)", "live-like readiness(실거래 유사 준비)"],
            "judgment_label": "review_required(검토 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "거래별 손익 표는 만들어졌고, 다음 단계에서 s07의 비용/세션 구조를 판정해야 한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": ["trade-level artifacts materialized(거래별 산출물 물질화)", "review required(검토 필요)"],
            "forbidden_claims": ["candidate selection(후보 선정)", "forward pass(전진 통과)", "operating promotion(운영 승격)", "runtime authority(런타임 권위)", "Goal Achieve(목표 달성)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344K s07 Deal-Level Cost/Session Materialization(344K s07 거래별 비용/세션 물질화)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- trade_rows(거래 행): `{final['trade_record_rows']}`
- s07_trades(s07 거래 수): `{final['s07_trade_count']}`
- s07_net(s07 순손익): `{final['s07_net_profit']}`
- s07_moderate_adjusted_net(s07 중간 비용 조정 순손익): `{final['s07_moderate_adjusted_net_profit']}`
- s07_moderate_pf(s07 중간 비용 PF): `{final['s07_moderate_adjusted_profit_factor_estimate']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

MT5 report(MT5 보고서)의 deals(딜)를 paired trades(짝지은 거래)로 바꾸고, entry feature(진입 피처)를 붙여 session/regime PnL(세션/국면 손익)과 cost replay(비용 재생)를 만들었다.

## Effect(효과)

run344L review(검토)가 이제 신호 수가 아니라 실제 거래 손익으로 s07 구조를 판단할 수 있다.

## Boundary(경계)

이 run(실행)은 materialization only(물질화 전용)다. candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344K Materialization Decision(344K 물질화 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(TRADE_LEVEL_RECORDS)}`, `{rel(SESSION_PNL_SCORECARD)}`, `{rel(REGIME_PNL_SCORECARD)}`, `{rel(COST_REPLAY_SCORECARD)}`

Action(행동): 거래별 비용/세션/국면 손익 산출물을 만들었다.
Effect(효과): run344L이 s07을 실제 거래 손익 구조로 판정할 수 있다.

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

run344K materialization(물질화)이 완료되어 run344L review(검토)를 열었다. 다음 행동(action, 행동)은 s07의 비용/세션/국면 손익 구조를 판정하는 것이다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_materialization(최근 물질화): `{RUN_ID}`
- research_clue(연구 단서): `s07_trend_confirmed_long_only`
- s07_trade_count(s07 거래 수): `{final['s07_trade_count']}`
- s07_net_profit(s07 순손익): `{final['s07_net_profit']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 거래별 산출물은 만들었지만 선정은 열지 않는다.
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
    marker = f"run344K {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344K Deal-Level Materialization(344K 거래별 물질화)

- run_id(실행 ID): `{RUN_ID}`
- trade_rows(거래 행): `{final['trade_record_rows']}`
- s07_net(s07 순손익): `{final['s07_net_profit']}`
- effect(효과): run344L review(검토)를 열었다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344K Deal-Level Materialization(344K 거래별 물질화)

- report(보고서): `{rel(REPORT_PATH)}`
- trades(거래): `{rel(TRADE_LEVEL_RECORDS)}`
- session_pnl(세션 손익): `{rel(SESSION_PNL_SCORECARD)}`
- cost_replay(비용 재생): `{rel(COST_REPLAY_SCORECARD)}`
- effect(효과): 거래별 손익 판정을 위한 산출물을 만들었다.
""",
    )
    changelog = f"""## {TODAY} run344K Deal-Level Materialization(거래별 물질화)

- action(행동): MT5 report(MT5 보고서) 거래를 파싱해 비용/세션/국면 손익 표를 만들었다.
- effect(효과): run344L에서 실제 거래 손익 구조를 검토할 수 있다.
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
        "lane": "kpi_evidence(KPI 근거)",
        "family": "kpi_evidence(KPI 근거)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "deal-level cost/session materialization(거래별 비용/세션 물질화); review required(검토 필요).",
        "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
        "net_profit": final["s07_net_profit"],
        "profit_factor": final["s07_profit_factor_estimate"],
        "trade_count": final["s07_trade_count"],
        "expectancy": final["s07_expectancy"],
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
            "metric_scope": "deal_level_cost_session_regime",
            "kpi_scope": "deal_level_cost_session_regime",
            "scoreboard_lane": "kpi_evidence(KPI 근거)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "net_profit": final["s07_net_profit"],
            "profit_factor": final["s07_profit_factor_estimate"],
            "expectancy": final["s07_expectancy"],
            "trade_count": final["s07_trade_count"],
            "result_status": JUDGMENT,
            "primary_kpi": f"s07_net={final['s07_net_profit']};pf={final['s07_profit_factor_estimate']};trades={final['s07_trade_count']}",
            "guardrail_kpi": f"moderate_net={final['s07_moderate_adjusted_net_profit']};review_required",
            "external_verification_status": "completed_from_existing_mt5_report(기존 MT5 보고서에서 완료)",
            "notes": "Tier A deal-level materialization(Tier A 거래별 물질화).",
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
            "scoreboard_lane": "kpi_evidence(KPI 근거)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B was outside this materialization(Tier B는 이번 물질화 밖).",
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
            "scoreboard_lane": "kpi_evidence(KPI 근거)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "net_profit": final["s07_net_profit"],
            "profit_factor": final["s07_profit_factor_estimate"],
            "expectancy": final["s07_expectancy"],
            "trade_count": final["s07_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": f"s07_net={final['s07_net_profit']};trades={final['s07_trade_count']}",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "completed_from_existing_mt5_report(기존 MT5 보고서에서 완료)",
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
    required_fields = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary", "artifact_id", "created_at_utc", "notes", "artifact_path"]
    for field in required_fields:
        if field not in fieldnames:
            fieldnames.append(field)
    new_rows: list[dict[str, Any]] = []
    for path in paths:
        if not exists(path):
            continue
        artifact_id = f"{RUN_NUMBER}::{rel(path)}"
        new_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lower().lstrip(".") or "artifact",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": artifact_id,
                "notes": "run344K materialization artifact(run344K 물질화 산출물)",
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


def build_materialization() -> Mapping[str, Any]:
    for path in INPUT_FILES:
        required(path)
    parent_final = read_json(SOURCE_PARENT_FINAL)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError("run344J next_run_id does not point to run344K")
    if not parent_gates_passed():
        raise RuntimeError("run344J gate audit has failed rows")

    summary = read_csv(SOURCE_RUNTIME_SUMMARY)
    report_records = read_json(SOURCE_RUNTIME_REPORTS)
    features = read_csv(SOURCE_FEATURES)
    cost_contract = read_csv(SOURCE_PARENT_COST_CONTRACT)
    trades = build_trade_records(summary, report_records, features)
    session = grouped_score(trades, ["attempt_name", "session_bucket"])
    regime = build_regime_scores(trades)
    direction = grouped_score(trades, ["attempt_name", "direction"])
    cost = build_cost_replay(trades, summary, cost_contract)
    curve = build_equity_curve(trades)
    s07_trades = trades.loc[trades["attempt_name"].eq("s07_trend_confirmed_long_only")]
    s07_scores = score_values(s07_trades["net_profit"].astype(float).tolist())
    s07_cost_moderate = cost.loc[cost["attempt_name"].eq("s07_trend_confirmed_long_only") & cost["scenario_id"].eq("moderate")].iloc[0]
    expected_trade_rows = int(summary["trade_count"].map(as_int).sum())
    summary_rows = [
        {
            "summary_id": "materialization_total",
            "trade_record_rows": len(trades),
            "expected_trade_rows": expected_trade_rows,
            "session_pnl_rows": len(session),
            "regime_pnl_rows": len(regime),
            "direction_pnl_rows": len(direction),
            "cost_replay_rows": len(cost),
            "entry_feature_missing_rows": int((~trades["entry_feature_match"].astype(bool)).sum()),
            "s07_net_profit": s07_scores["net_profit"],
            "s07_profit_factor_estimate": s07_scores["profit_factor_estimate"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_frame(TRADE_LEVEL_RECORDS, trades)
    write_frame(SESSION_PNL_SCORECARD, session)
    write_frame(REGIME_PNL_SCORECARD, regime)
    write_frame(DIRECTION_PNL_SCORECARD, direction)
    write_frame(COST_REPLAY_SCORECARD, cost)
    write_frame(EQUITY_CURVE_REPLAY, curve)
    write_csv(MATERIALIZATION_SUMMARY, summary_rows)

    final: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "parent_gate_passed": True,
        "trade_record_rows": int(len(trades)),
        "expected_trade_rows": expected_trade_rows,
        "session_pnl_rows": int(len(session)),
        "regime_pnl_rows": int(len(regime)),
        "direction_pnl_rows": int(len(direction)),
        "cost_replay_rows": int(len(cost)),
        "equity_curve_rows": int(len(curve)),
        "entry_feature_missing_rows": int((~trades["entry_feature_match"].astype(bool)).sum()),
        "s07_trade_count": int(s07_scores["trade_count"]),
        "s07_net_profit": float(s07_scores["net_profit"]),
        "s07_profit_factor_estimate": float(s07_scores["profit_factor_estimate"]),
        "s07_expectancy": float(s07_scores["expectancy"]),
        "s07_reported_net_profit": float(summary.loc[summary["attempt_name"].eq("s07_trend_confirmed_long_only"), "net_profit"].iloc[0]),
        "s07_net_profit_diff": round(float(s07_scores["net_profit"]) - float(summary.loc[summary["attempt_name"].eq("s07_trend_confirmed_long_only"), "net_profit"].iloc[0]), 6),
        "s07_moderate_adjusted_net_profit": float(s07_cost_moderate["adjusted_net_profit"]),
        "s07_moderate_adjusted_profit_factor_estimate": float(s07_cost_moderate["adjusted_profit_factor_estimate"]),
        "s07_moderate_adjusted_recovery_factor": float(s07_cost_moderate["adjusted_recovery_factor"]),
        "s07_moderate_survival_passed": bool(s07_cost_moderate["survival_passed"]),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "completed_from_existing_mt5_report(기존 MT5 보고서에서 완료)",
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
            "created_at_utc": now_utc(),
            "execution_command": f"python -B {rel(Path(__file__))}",
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    build_receipts(final)
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
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    return final


def main() -> None:
    final = build_materialization()
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
