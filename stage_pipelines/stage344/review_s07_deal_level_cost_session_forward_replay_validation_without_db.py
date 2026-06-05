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
    materialize_s07_deal_level_cost_session_forward_replay_validation_without_db as parent,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_s07_forward_cost_stability_validation_package_without_db as pkg,
)


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344L"
RUN_ID = "run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_PACKAGE_RUN_ID = parent.SOURCE_PACKAGE_RUN_ID
SOURCE_RUNTIME_RUN_ID = parent.SOURCE_RUNTIME_RUN_ID
NEXT_RUN_ID = "run344M_design_cash_open_long_quality_short_carry_decomposition_probe_without_db_v1"

STATUS = "completed_stage344L_deal_level_cost_session_review_positive_clue_with_concentration_risk_no_selection"
JUDGMENT = (
    "s07_trade_level_review_positive_moderate_cost_but_cash_open_and_short_carry_"
    "concentration_require_next_probe_no_operating_claim"
)
DECISION = "stage344L_open_run344M_cash_open_long_quality_short_carry_decomposition_design"
CLAIM_BOUNDARY = (
    "research_development_review_only_deal_level_cost_session_forward_replay_positive_clue_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

S07_ATTEMPT = "s07_trend_confirmed_long_only"

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344L_s07_deal_level_cost_session_forward_replay_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344L_s07_deal_level_cost_session_forward_replay_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

REVIEW_SCORECARD = RUN_DIR / "review_scorecard.csv"
SEGMENT_CONCENTRATION_REVIEW = RUN_DIR / "segment_concentration_review.csv"
COST_SURVIVAL_REVIEW = RUN_DIR / "cost_survival_review.csv"
EQUITY_CURVE_QUALITY_REVIEW = RUN_DIR / "equity_curve_quality_review.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
RUN344M_QUEUE = RUN_DIR / "run344M_queue.csv"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
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
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = (
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.TRADE_LEVEL_RECORDS,
    parent.SESSION_PNL_SCORECARD,
    parent.REGIME_PNL_SCORECARD,
    parent.DIRECTION_PNL_SCORECARD,
    parent.COST_REPLAY_SCORECARD,
    parent.EQUITY_CURVE_REPLAY,
    parent.MATERIALIZATION_SUMMARY,
)

OUTPUT_FILES = (
    REVIEW_SCORECARD,
    SEGMENT_CONCENTRATION_REVIEW,
    COST_SURVIVAL_REVIEW,
    EQUITY_CURVE_QUALITY_REVIEW,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    RUN344M_QUEUE,
    PERFORMANCE_RECEIPT,
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
    IDEA_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


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


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_or_replace_csv(path, keys, rows)


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


def pct(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round(float(numerator) / float(denominator), 6)


def parent_gates_passed() -> bool:
    gates = read_csv(parent.GATE_AUDIT)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def bool_from_value(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def attempt_order(cost: pd.DataFrame) -> list[str]:
    base = cost.loc[cost["scenario_id"].astype(str).eq("base")].copy()
    base = base.sort_values("scenario_adjusted_net_rank")
    return base["attempt_name"].astype(str).tolist()


def first_row(frame: pd.DataFrame, **conditions: str) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for column, value in conditions.items():
        mask &= frame[column].astype(str).eq(str(value))
    matches = frame.loc[mask]
    if matches.empty:
        return pd.Series(dtype="object")
    return matches.iloc[0]


def build_review_scorecard(session: pd.DataFrame, direction: pd.DataFrame, cost: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for attempt in attempt_order(cost):
        base = first_row(cost, attempt_name=attempt, scenario_id="base")
        moderate = first_row(cost, attempt_name=attempt, scenario_id="moderate")
        heavy = first_row(cost, attempt_name=attempt, scenario_id="heavy")
        attempt_sessions = session.loc[session["attempt_name"].astype(str).eq(attempt)].copy()
        attempt_directions = direction.loc[direction["attempt_name"].astype(str).eq(attempt)].copy()
        total_net = as_float(base.get("base_net_profit"))
        total_trades = as_int(base.get("base_trade_count"))
        open_row = first_row(session, attempt_name=attempt, session_bucket="cash_open_first_60m(현금장 첫 60분)")
        late_row = first_row(session, attempt_name=attempt, session_bucket="cash_late_after_210m(현금장 후반 210분 이후)")
        buy = first_row(direction, attempt_name=attempt, direction="buy")
        sell = first_row(direction, attempt_name=attempt, direction="sell")
        dominant_session = (
            attempt_sessions.assign(abs_net=attempt_sessions["net_profit"].map(lambda value: abs(as_float(value))))
            .sort_values("abs_net", ascending=False)
            .iloc[0]
        )
        dominant_direction = (
            attempt_directions.assign(abs_net=attempt_directions["net_profit"].map(lambda value: abs(as_float(value))))
            .sort_values("abs_net", ascending=False)
            .iloc[0]
        )
        rows.append(
            {
                "attempt_name": attempt,
                "review_role": "focus(초점)" if attempt == S07_ATTEMPT else "comparator(대조)",
                "base_net_profit": round(total_net, 6),
                "base_profit_factor_estimate": as_float(base.get("adjusted_profit_factor_estimate")),
                "base_expectancy": as_float(base.get("adjusted_expectancy")),
                "trade_count": total_trades,
                "moderate_adjusted_net_profit": as_float(moderate.get("adjusted_net_profit")),
                "moderate_adjusted_profit_factor_estimate": as_float(moderate.get("adjusted_profit_factor_estimate")),
                "moderate_adjusted_recovery_factor": as_float(moderate.get("adjusted_recovery_factor")),
                "moderate_survival_passed": bool_from_value(moderate.get("survival_passed")),
                "moderate_adjusted_net_rank": as_int(moderate.get("scenario_adjusted_net_rank")),
                "heavy_adjusted_net_profit": as_float(heavy.get("adjusted_net_profit")),
                "heavy_adjusted_profit_factor_estimate": as_float(heavy.get("adjusted_profit_factor_estimate")),
                "heavy_adjusted_recovery_factor": as_float(heavy.get("adjusted_recovery_factor")),
                "heavy_survival_passed": bool_from_value(heavy.get("survival_passed")),
                "cash_open_net_profit": as_float(open_row.get("net_profit")),
                "cash_open_net_share": pct(as_float(open_row.get("net_profit")), total_net),
                "cash_open_trade_share": pct(as_int(open_row.get("trade_count")), total_trades),
                "cash_late_long_net_profit": as_float(late_row.get("long_net_profit")),
                "buy_net_profit": as_float(buy.get("net_profit")),
                "buy_profit_factor_estimate": as_float(buy.get("profit_factor_estimate")),
                "buy_trade_count": as_int(buy.get("trade_count")),
                "buy_net_share": pct(as_float(buy.get("net_profit")), total_net),
                "sell_net_profit": as_float(sell.get("net_profit")),
                "sell_profit_factor_estimate": as_float(sell.get("profit_factor_estimate")),
                "sell_trade_count": as_int(sell.get("trade_count")),
                "sell_net_share": pct(as_float(sell.get("net_profit")), total_net),
                "dominant_session_bucket": dominant_session.get("session_bucket", ""),
                "dominant_session_net_share": pct(as_float(dominant_session.get("net_profit")), total_net),
                "dominant_direction": dominant_direction.get("direction", ""),
                "dominant_direction_net_share": pct(as_float(dominant_direction.get("net_profit")), total_net),
                "review_judgment": (
                    "positive_research_clue_with_concentration_risk(집중 위험이 있는 긍정 연구 단서)"
                    if attempt == S07_ATTEMPT
                    else "comparator_context(대조 문맥)"
                ),
                "selection_status": "not_selected(선정 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_segment_concentration(session: pd.DataFrame, regime: pd.DataFrame, direction: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    totals: dict[str, dict[str, float]] = {}
    for attempt, group in direction.groupby("attempt_name", dropna=False):
        totals[str(attempt)] = {
            "net": float(group["net_profit"].map(as_float).sum()),
            "trades": float(group["trade_count"].map(as_int).sum()),
        }

    def add_row(source: Mapping[str, Any], dimension: str, bucket: str) -> None:
        attempt = str(source.get("attempt_name", ""))
        total = totals.get(attempt, {"net": 0.0, "trades": 0.0})
        net = as_float(source.get("net_profit"))
        trade_count = as_int(source.get("trade_count"))
        net_share = pct(net, total["net"])
        trade_share = pct(trade_count, total["trades"])
        concentration = abs(net_share) >= 0.60 or trade_share >= 0.50
        rows.append(
            {
                "attempt_name": attempt,
                "dimension": dimension,
                "segment_bucket": bucket,
                "trade_count": trade_count,
                "trade_share_of_attempt": trade_share,
                "net_profit": net,
                "net_share_of_attempt": net_share,
                "profit_factor_estimate": as_float(source.get("profit_factor_estimate")),
                "expectancy": as_float(source.get("expectancy")),
                "win_rate": as_float(source.get("win_rate")),
                "long_net_profit": as_float(source.get("long_net_profit")),
                "short_net_profit": as_float(source.get("short_net_profit")),
                "concentration_flag": "yes(예)" if concentration else "no(아니오)",
                "review_use": (
                    "next_probe_constraint(다음 탐침 제약)"
                    if concentration and attempt == S07_ATTEMPT
                    else "context(문맥)"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for _, row in session.iterrows():
        add_row(row, "session(세션)", str(row.get("session_bucket", "")))
    for _, row in direction.iterrows():
        add_row(row, "direction(방향)", str(row.get("direction", "")))
    for _, row in regime.iterrows():
        add_row(row, f"regime:{row.get('regime_dimension', '')}", str(row.get("segment_bucket", "")))
    return pd.DataFrame(rows)


def build_cost_survival_review(cost: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in cost.iterrows():
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "scenario_id": row.get("scenario_id", ""),
                "cost_per_closed_trade_account_currency": as_float(row.get("cost_per_closed_trade_account_currency")),
                "base_trade_count": as_int(row.get("base_trade_count")),
                "base_net_profit": as_float(row.get("base_net_profit")),
                "adjusted_net_profit": as_float(row.get("adjusted_net_profit")),
                "adjusted_profit_factor_estimate": as_float(row.get("adjusted_profit_factor_estimate")),
                "adjusted_expectancy": as_float(row.get("adjusted_expectancy")),
                "adjusted_recovery_factor": as_float(row.get("adjusted_recovery_factor")),
                "survival_passed": bool_from_value(row.get("survival_passed")),
                "survival_status": row.get("survival_status", ""),
                "scenario_adjusted_net_rank": as_int(row.get("scenario_adjusted_net_rank")),
                "review_use": (
                    "cost_survival_positive_clue(비용 생존 긍정 단서)"
                    if row.get("attempt_name") == S07_ATTEMPT and row.get("scenario_id") == "moderate"
                    else (
                        "cost_failure_constraint(비용 실패 제약)"
                        if row.get("attempt_name") == S07_ATTEMPT and row.get("scenario_id") == "heavy"
                        else "comparator_context(대조 문맥)"
                    )
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def max_consecutive(mask_values: Sequence[bool]) -> int:
    best = 0
    current = 0
    for flag in mask_values:
        if flag:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def build_equity_curve_quality(curve: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for attempt, group in curve.sort_values(["attempt_name", "trade_index"]).groupby("attempt_name", dropna=False):
        values = [as_float(value) for value in group["net_profit"].tolist()]
        cumulative_values = [as_float(value) for value in group["cumulative_net_profit"].tolist()]
        drawdowns = [as_float(value) for value in group["close_to_close_drawdown"].tolist()]
        final_net = cumulative_values[-1] if cumulative_values else 0.0
        min_dd = min(drawdowns) if drawdowns else 0.0
        max_dd_abs = abs(min_dd)
        recovery = round(final_net / max_dd_abs, 6) if max_dd_abs else 0.0
        worst = group.loc[group["close_to_close_drawdown"].map(as_float).idxmin()] if len(group) else pd.Series(dtype="object")
        rows.append(
            {
                "attempt_name": attempt,
                "trade_count": len(values),
                "final_closed_trade_net_profit": round(final_net, 6),
                "max_closed_trade_drawdown_abs": round(max_dd_abs, 6),
                "closed_trade_recovery_factor": recovery,
                "worst_drawdown_trade_index": as_int(worst.get("trade_index")),
                "worst_drawdown_close_time": worst.get("close_time", ""),
                "ending_drawdown": drawdowns[-1] if drawdowns else 0.0,
                "max_consecutive_losses": max_consecutive([value < 0 for value in values]),
                "max_consecutive_wins": max_consecutive([value > 0 for value in values]),
                "curve_authority": "closed_trade_replay_only(청산 거래 재생 전용)",
                "quality_label": (
                    "usable_research_curve(연구용 사용 가능 곡선)"
                    if final_net > 0 and recovery >= 1.0
                    else "weak_research_curve(약한 연구 곡선)"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_memory_tables(review: pd.DataFrame, segment: pd.DataFrame, cost_review: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    s07 = review.loc[review["attempt_name"].eq(S07_ATTEMPT)].iloc[0]
    s07_moderate = first_row(cost_review, attempt_name=S07_ATTEMPT, scenario_id="moderate")
    s07_heavy = first_row(cost_review, attempt_name=S07_ATTEMPT, scenario_id="heavy")
    s07_cash_open = first_row(
        segment,
        attempt_name=S07_ATTEMPT,
        dimension="session(세션)",
        segment_bucket="cash_open_first_60m(현금장 첫 60분)",
    )
    s07_sell = first_row(segment, attempt_name=S07_ATTEMPT, dimension="direction(방향)", segment_bucket="sell")
    positive_rows = [
        {
            "clue_id": "s07_moderate_cost_survival",
            "evidence": f"moderate_net={s07_moderate.get('adjusted_net_profit')};pf={s07_moderate.get('adjusted_profit_factor_estimate')};recovery={s07_moderate.get('adjusted_recovery_factor')}",
            "effect": "s07 can remain in offensive exploration under moderate cost(s07은 중간 비용에서 공격 탐색을 유지 가능)",
            "next_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "clue_id": "cash_open_first_hour_profit_engine",
            "evidence": f"net={s07_cash_open.get('net_profit')};share={s07_cash_open.get('net_share_of_attempt')}",
            "effect": "cash-open session becomes a concrete alpha seed(현금장 초반이 구체 알파 씨앗이 됨)",
            "next_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "clue_id": "long_side_quality_increment",
            "evidence": f"buy_net={s07.get('buy_net_profit')};buy_pf={s07.get('buy_profit_factor_estimate')};buy_trades={s07.get('buy_trade_count')}",
            "effect": "long quality is useful enough to decompose instead of discard(롱 품질은 폐기보다 분해 가치가 있음)",
            "next_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "clue_id": "s07_cost_rank_leads_comparators",
            "evidence": f"moderate_rank={s07.get('moderate_adjusted_net_rank')};base_net={s07.get('base_net_profit')}",
            "effect": "s07 remains the focus comparator for the next probe(s07은 다음 탐침의 초점 대조군으로 유지)",
            "next_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    failure_rows = [
        {
            "failure_id": "heavy_cost_recovery_break",
            "evidence": f"heavy_net={s07_heavy.get('adjusted_net_profit')};heavy_recovery={s07_heavy.get('adjusted_recovery_factor')}",
            "effect": "next design must reduce cost sensitivity or drawdown pressure(다음 설계는 비용 민감도나 낙폭 압박을 낮춰야 함)",
            "constraint_for_next": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "cash_open_concentration_risk",
            "evidence": f"cash_open_share={s07_cash_open.get('net_share_of_attempt')};trade_share={s07_cash_open.get('trade_share_of_attempt')}",
            "effect": "do not read one session as broad stability(한 세션을 넓은 안정성으로 읽지 않음)",
            "constraint_for_next": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "short_carry_majority",
            "evidence": f"sell_net={s07_sell.get('net_profit')};sell_share={s07_sell.get('net_share_of_attempt')}",
            "effect": "long improvement must be separated from inherited short carry(롱 개선과 기존 숏 기여를 분리해야 함)",
            "constraint_for_next": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "late_session_long_negative",
            "evidence": f"cash_late_long_net={s07.get('cash_late_long_net_profit')}",
            "effect": "late-session long fire must be controlled before promotion talk(후반 롱 진입은 승격 논의 전 통제 필요)",
            "constraint_for_next": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "tier_b_missing_required",
            "evidence": "Tier B separate and Tier A+B true combined are not available(Tier B 분리와 실제 합산 없음)",
            "effect": "combined stability cannot be claimed(합산 안정성 주장 불가)",
            "constraint_for_next": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    queue_rows = [
        {
            "queue_id": "q01_cash_open_direction_decomposition",
            "next_run_id": NEXT_RUN_ID,
            "design_question": "cash-open profit comes from long quality, short carry, or both(현금장 초반 수익 원천 분해)",
            "action": "split cash-open trades by direction and feature state(현금장 초반 거래를 방향/피처 상태로 분해)",
            "effect": "turn concentration into a controlled alpha source(집중을 통제 가능한 알파 원천으로 전환)",
            "must_not_claim": "operating_promotion(운영 승격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_long_quality_threshold_variants",
            "next_run_id": NEXT_RUN_ID,
            "design_question": "which long-quality filter keeps buy net while reducing late loss(어떤 롱 품질 필터가 후반 손실을 줄이는가)",
            "action": "test stricter trend/volatility/DI variants(더 엄격한 추세/변동성/DI 변형 시험)",
            "effect": "preserve buy edge while lowering cost stress(롱 우위를 보존하며 비용 압박 완화)",
            "must_not_claim": "candidate_selection(후보 선정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_short_carry_control",
            "next_run_id": NEXT_RUN_ID,
            "design_question": "whether inherited short carry is necessary or masking long edge(기존 숏 기여가 필수인지 롱 우위를 가리는지)",
            "action": "compare short-retain, short-throttle, and long-focused stacks(숏 유지/축소/롱 초점 묶음 비교)",
            "effect": "avoid over-crediting the new long idea(새 롱 아이디어를 과대평가하지 않음)",
            "must_not_claim": "runtime_authority(런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_heavy_cost_recovery_repair",
            "next_run_id": NEXT_RUN_ID,
            "design_question": "how to lift heavy-cost recovery above one(강한 비용 회복 계수를 1 위로 올리는 방법)",
            "action": "pressure-test fewer trades and cleaner exits(거래 수 축소와 더 깨끗한 청산 압박 시험)",
            "effect": "convert failure memory into a hard design floor(실패 기억을 설계 하한으로 전환)",
            "must_not_claim": "Goal Achieve(목표 달성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return pd.DataFrame(positive_rows), pd.DataFrame(failure_rows), pd.DataFrame(queue_rows)


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    rows = [
        ("parent_run344K_gates_passed", final["parent_gate_passed"], rel(parent.GATE_AUDIT), "run344K gate(게이트)를 이어받음"),
        ("review_inputs_loaded", final["review_input_rows"] > 0, rel(parent.TRADE_LEVEL_RECORDS), "거래별 검토 입력을 읽음"),
        ("s07_cost_survival_review_written", final["s07_moderate_survival_passed"], rel(COST_SURVIVAL_REVIEW), "s07 비용 생존 검토 작성"),
        ("segment_concentration_review_written", final["segment_review_rows"] >= 9, rel(SEGMENT_CONCENTRATION_REVIEW), "세션/방향/국면 집중 검토 작성"),
        ("equity_curve_quality_review_written", final["equity_quality_rows"] >= 3, rel(EQUITY_CURVE_QUALITY_REVIEW), "청산 거래 수익곡선 품질 검토 작성"),
        ("positive_and_failure_memory_written", final["positive_clue_rows"] >= 4 and final["failure_memory_rows"] >= 4, rel(POSITIVE_CLUES), "긍정 단서와 실패 기억 기록"),
        ("next_probe_queue_written", final["queue_rows"] >= 4, rel(RUN344M_QUEUE), "다음 탐색 큐 작성"),
        ("no_forbidden_operating_claim", no_forbidden, rel(FINAL_DECISION), "검토를 운영 주장으로 올리지 않음"),
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
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "primary_subject": S07_ATTEMPT,
            "attribution_summary": {
                "s07_net_profit": final["s07_net_profit"],
                "cash_open_net_share": final["s07_cash_open_net_share"],
                "sell_net_share": final["s07_sell_net_share"],
                "buy_net_profit": final["s07_buy_net_profit"],
                "moderate_adjusted_net_profit": final["s07_moderate_adjusted_net_profit"],
                "heavy_adjusted_recovery_factor": final["s07_heavy_adjusted_recovery_factor"],
            },
            "positive_clues": [rel(POSITIVE_CLUES), rel(REVIEW_SCORECARD)],
            "failure_memory": [rel(FAILURE_MEMORY), rel(SEGMENT_CONCENTRATION_REVIEW), rel(COST_SURVIVAL_REVIEW)],
            "alternative_explanations": [
                "cash-open concentration(현금장 초반 집중)",
                "short carry inheritance(기존 숏 기여)",
                "closed-trade replay only(청산 거래 재생 전용)",
            ],
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "judgment_label": "positive_research_clue_with_constraints(제약이 있는 긍정 연구 단서)",
            "why_not_promotion": [
                "heavy cost recovery fails(강한 비용 회복 실패)",
                "cash-open and short concentration remain(현금장 초반과 숏 집중 남음)",
                "Tier B missing_required(Tier B 필수 누락)",
                "no new forward pass(새 전진 통과 없음)",
            ],
            "allowed_claims": ["research clue(연구 단서)", "next probe design seed(다음 탐침 설계 씨앗)"],
            "forbidden_claims": ["candidate selection(후보 선정)", "operating promotion(운영 승격)", "runtime authority(런타임 권위)", "Goal Achieve(목표 달성)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": [
                "s07 positive research clue(s07 긍정 연구 단서)",
                "moderate cost survival(중간 비용 생존)",
                "concentration risk identified(집중 위험 식별)",
                "next probe queued(다음 탐침 큐 등록)",
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
    report = f"""# run344L s07 Deal-Level Cost/Session Review(344L s07 거래별 비용/세션 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- s07_net_profit(s07 순수익): `{final['s07_net_profit']}`
- s07_profit_factor(s07 수익 팩터): `{final['s07_profit_factor_estimate']}`
- s07_trade_count(s07 거래 수): `{final['s07_trade_count']}`
- moderate_cost_net(중간 비용 순수익): `{final['s07_moderate_adjusted_net_profit']}`
- heavy_cost_recovery(강한 비용 회복 계수): `{final['s07_heavy_adjusted_recovery_factor']}`
- cash_open_net_share(현금장 초반 순수익 비중): `{final['s07_cash_open_net_share']}`
- sell_net_share(숏 순수익 비중): `{final['s07_sell_net_share']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run344K deal-level records(run344K 거래별 기록)를 비용 생존(cost survival, 비용 생존), session concentration(세션 집중), direction concentration(방향 집중), closed-trade equity quality(청산 거래 수익곡선 품질)로 재검토했다.

## Effect(효과)

s07은 moderate cost(중간 비용)에서 살아남고 buy side(롱 방향)도 실제 순수익을 만들었다. 하지만 cash-open first hour(현금장 첫 60분)와 sell carry(숏 기여)에 수익이 많이 몰려, 다음 run344M은 이 집중을 분해해야 한다.

## Boundary(경계)

이 run(실행)은 review only(검토 전용)다. candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344L Review Decision(344L 검토 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(REVIEW_SCORECARD)}`, `{rel(SEGMENT_CONCENTRATION_REVIEW)}`, `{rel(COST_SURVIVAL_REVIEW)}`, `{rel(EQUITY_CURVE_QUALITY_REVIEW)}`

Action(행동): s07 거래별 손익을 비용/세션/방향/곡선 품질로 판정했다.
Effect(효과): s07은 긍정 연구 단서로 유지하되, 운영 주장이 아니라 현금장 초반 롱 품질과 숏 기여 분해 탐색으로 넘긴다.

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

run344L review(검토)가 완료되어 s07은 positive research clue(긍정 연구 단서)로 남았다. 다음 행동(action, 행동)은 cash-open long quality(현금장 초반 롱 품질)와 short carry(숏 기여)를 분해하는 설계를 여는 것이다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_review(최근 검토): `{RUN_ID}`
- research_clue(연구 단서): `s07_trend_confirmed_long_only`
- s07_moderate_cost_passed(s07 중간 비용 통과): `{final['s07_moderate_survival_passed']}`
- s07_heavy_cost_passed(s07 강한 비용 통과): `{final['s07_heavy_survival_passed']}`
- s07_cash_open_net_share(s07 현금장 초반 순수익 비중): `{final['s07_cash_open_net_share']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 좋은 단서는 보존하되 선정은 열지 않는다.
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
    marker = f"run344L {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344L s07 Deal-Level Review(344L s07 거래별 검토)

- run_id(실행 ID): `{RUN_ID}`
- s07_net(s07 순수익): `{final['s07_net_profit']}`
- moderate_cost_passed(중간 비용 통과): `{final['s07_moderate_survival_passed']}`
- cash_open_net_share(현금장 초반 순수익 비중): `{final['s07_cash_open_net_share']}`
- effect(효과): run344M cash-open/short-carry decomposition(현금장 초반/숏 기여 분해)을 열었다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344L s07 Deal-Level Review(344L s07 거래별 검토)

- report(보고서): `{rel(REPORT_PATH)}`
- review_scorecard(검토 점수판): `{rel(REVIEW_SCORECARD)}`
- concentration_review(집중 검토): `{rel(SEGMENT_CONCENTRATION_REVIEW)}`
- cost_review(비용 검토): `{rel(COST_SURVIVAL_REVIEW)}`
- effect(효과): s07 긍정 단서와 집중 위험을 분리했다.
""",
    )
    changelog = f"""## {TODAY} run344L s07 Deal-Level Review(s07 거래별 검토)

- action(행동): run344K 거래별 산출물을 비용/세션/방향/수익곡선으로 재판독했다.
- effect(효과): s07은 중간 비용 긍정 단서로 유지하고, 현금장 초반 집중과 숏 기여를 다음 탐색 제약으로 바꿨다.
- boundary(경계): 선정/운영 승격/런타임 권위/목표 달성은 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} run344L Idea Seed(아이디어 씨앗)

- idea(아이디어): cash-open long quality and short-carry decomposition(현금장 초반 롱 품질과 숏 기여 분해)
- source_run(원천 실행): `{RUN_ID}`
- effect(효과): s07 수익 집중을 다음 공격 탐색의 설계 질문으로 바꾼다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} run344L Failure Memory(실패 기억)

- source_run(원천 실행): `{RUN_ID}`
- failure(실패): heavy cost recovery breaks(강한 비용 회복 실패), cash-open concentration(현금장 초반 집중), short carry majority(숏 기여 과반)
- effect(효과): 다음 run344M은 이 조건을 완화하지 않고 설계 제약으로 가져간다.
""",
    )


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
        "notes": "s07 deal-level review positive clue with concentration risk(s07 거래별 검토 긍정 단서와 집중 위험); no selection(선정 없음).",
        "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
        "net_profit": final["s07_net_profit"],
        "profit_factor": final["s07_profit_factor_estimate"],
        "recovery_factor": final["s07_closed_trade_recovery_factor"],
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
            "metric_scope": "deal_level_review_cost_session_direction",
            "kpi_scope": "deal_level_review_cost_session_direction",
            "scoreboard_lane": "review_attribution(검토 귀속)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "net_profit": final["s07_net_profit"],
            "profit_factor": final["s07_profit_factor_estimate"],
            "expectancy": final["s07_expectancy"],
            "recovery_factor": final["s07_closed_trade_recovery_factor"],
            "trade_count": final["s07_trade_count"],
            "result_status": JUDGMENT,
            "primary_kpi": f"net={final['s07_net_profit']};pf={final['s07_profit_factor_estimate']};moderate_net={final['s07_moderate_adjusted_net_profit']}",
            "guardrail_kpi": f"heavy_recovery={final['s07_heavy_adjusted_recovery_factor']};cash_open_share={final['s07_cash_open_net_share']};sell_share={final['s07_sell_net_share']}",
            "external_verification_status": "review_from_existing_mt5_report(기존 MT5 보고서 기반 검토)",
            "notes": "Tier A deal-level review(Tier A 거래별 검토); no selection(선정 없음).",
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
            "net_profit": final["s07_net_profit"],
            "profit_factor": final["s07_profit_factor_estimate"],
            "expectancy": final["s07_expectancy"],
            "recovery_factor": final["s07_closed_trade_recovery_factor"],
            "trade_count": final["s07_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": f"net={final['s07_net_profit']};moderate_net={final['s07_moderate_adjusted_net_profit']}",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "review_from_existing_mt5_report(기존 MT5 보고서 기반 검토)",
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
                "notes": "run344L review artifact(run344L 검토 산출물)",
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
    parent_final = read_json(parent.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError("run344K next_run_id does not point to run344L")
    if not parent_gates_passed():
        raise RuntimeError("run344K gate audit has failed rows")

    trades = read_csv(parent.TRADE_LEVEL_RECORDS)
    session = read_csv(parent.SESSION_PNL_SCORECARD)
    regime = read_csv(parent.REGIME_PNL_SCORECARD)
    direction = read_csv(parent.DIRECTION_PNL_SCORECARD)
    cost = read_csv(parent.COST_REPLAY_SCORECARD)
    curve = read_csv(parent.EQUITY_CURVE_REPLAY)

    review = build_review_scorecard(session, direction, cost)
    segment = build_segment_concentration(session, regime, direction)
    cost_review = build_cost_survival_review(cost)
    equity = build_equity_curve_quality(curve)
    positive, failure, queue = build_memory_tables(review, segment, cost_review)

    write_frame(REVIEW_SCORECARD, review)
    write_frame(SEGMENT_CONCENTRATION_REVIEW, segment)
    write_frame(COST_SURVIVAL_REVIEW, cost_review)
    write_frame(EQUITY_CURVE_QUALITY_REVIEW, equity)
    write_frame(POSITIVE_CLUES, positive)
    write_frame(FAILURE_MEMORY, failure)
    write_frame(RUN344M_QUEUE, queue)

    s07 = review.loc[review["attempt_name"].eq(S07_ATTEMPT)].iloc[0]
    s07_equity = equity.loc[equity["attempt_name"].eq(S07_ATTEMPT)].iloc[0]
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
        "review_input_rows": int(len(trades) + len(session) + len(direction) + len(cost) + len(curve)),
        "review_scorecard_rows": int(len(review)),
        "segment_review_rows": int(len(segment)),
        "cost_review_rows": int(len(cost_review)),
        "equity_quality_rows": int(len(equity)),
        "positive_clue_rows": int(len(positive)),
        "failure_memory_rows": int(len(failure)),
        "queue_rows": int(len(queue)),
        "s07_net_profit": float(s07["base_net_profit"]),
        "s07_profit_factor_estimate": float(s07["base_profit_factor_estimate"]),
        "s07_expectancy": float(s07["base_expectancy"]),
        "s07_trade_count": int(s07["trade_count"]),
        "s07_moderate_adjusted_net_profit": float(s07["moderate_adjusted_net_profit"]),
        "s07_moderate_adjusted_profit_factor_estimate": float(s07["moderate_adjusted_profit_factor_estimate"]),
        "s07_moderate_adjusted_recovery_factor": float(s07["moderate_adjusted_recovery_factor"]),
        "s07_moderate_survival_passed": bool(s07["moderate_survival_passed"]),
        "s07_heavy_adjusted_net_profit": float(s07["heavy_adjusted_net_profit"]),
        "s07_heavy_adjusted_profit_factor_estimate": float(s07["heavy_adjusted_profit_factor_estimate"]),
        "s07_heavy_adjusted_recovery_factor": float(s07["heavy_adjusted_recovery_factor"]),
        "s07_heavy_survival_passed": bool(s07["heavy_survival_passed"]),
        "s07_cash_open_net_profit": float(s07["cash_open_net_profit"]),
        "s07_cash_open_net_share": float(s07["cash_open_net_share"]),
        "s07_cash_open_trade_share": float(s07["cash_open_trade_share"]),
        "s07_buy_net_profit": float(s07["buy_net_profit"]),
        "s07_buy_net_share": float(s07["buy_net_share"]),
        "s07_buy_trade_count": int(s07["buy_trade_count"]),
        "s07_sell_net_profit": float(s07["sell_net_profit"]),
        "s07_sell_net_share": float(s07["sell_net_share"]),
        "s07_sell_trade_count": int(s07["sell_trade_count"]),
        "s07_cash_late_long_net_profit": float(s07["cash_late_long_net_profit"]),
        "s07_closed_trade_recovery_factor": float(s07_equity["closed_trade_recovery_factor"]),
        "s07_closed_trade_max_drawdown_abs": float(s07_equity["max_closed_trade_drawdown_abs"]),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "review_from_existing_mt5_report(기존 MT5 보고서 기반 검토)",
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
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    return final


def main() -> None:
    final = build_review()
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
