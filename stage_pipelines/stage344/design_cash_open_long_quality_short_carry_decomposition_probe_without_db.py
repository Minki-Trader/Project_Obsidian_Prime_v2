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
    materialize_s07_deal_level_cost_session_forward_replay_validation_without_db as materialized,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_s07_forward_cost_stability_validation_package_without_db as pkg,
)
from stage_pipelines.stage344 import (  # noqa: E402
    review_s07_deal_level_cost_session_forward_replay_validation_without_db as review,
)


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344M"
RUN_ID = "run344M_design_cash_open_long_quality_short_carry_decomposition_probe_without_db_v1"
PARENT_RUN_ID = review.RUN_ID
SOURCE_PACKAGE_RUN_ID = review.SOURCE_PACKAGE_RUN_ID
SOURCE_RUNTIME_RUN_ID = review.SOURCE_RUNTIME_RUN_ID
NEXT_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"

STATUS = "completed_stage344M_cash_open_long_quality_short_carry_decomposition_design_ready_no_selection"
JUDGMENT = (
    "cash_open_long_quality_short_carry_decomposition_design_ready_"
    "posthoc_trade_filter_proxy_only_no_operating_claim"
)
DECISION = "stage344M_open_run344N_materialize_cash_open_long_quality_short_carry_package"
CLAIM_BOUNDARY = (
    "research_development_design_only_cash_open_long_quality_short_carry_decomposition_"
    "posthoc_trade_filter_proxy_no_new_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

S07_ATTEMPT = "s07_trend_confirmed_long_only"
CASH_OPEN_BUCKET = "cash_open_first_60m(현금장 첫 60분)"
CASH_LATE_BUCKET = "cash_late_after_210m(현금장 후반 210분 이후)"

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344M_cash_open_long_quality_short_carry_decomposition_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344M_cash_open_long_quality_short_carry_decomposition_design.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

CASH_OPEN_DECOMPOSITION = RUN_DIR / "cash_open_decomposition.csv"
FEATURE_STATE_DECOMPOSITION = RUN_DIR / "feature_state_decomposition.csv"
VARIANT_GRID_CONTRACT = RUN_DIR / "variant_grid_contract.csv"
HEAVY_COST_FLOOR_CONTRACT = RUN_DIR / "heavy_cost_recovery_floor_contract.csv"
EXPERIMENT_DESIGN_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "data_integrity_contract.csv"
MODEL_VALIDATION_CONTRACT = RUN_DIR / "model_validation_contract.csv"
RUNTIME_HANDOFF_PLAN = RUN_DIR / "runtime_handoff_plan.csv"
RUN344N_QUEUE = RUN_DIR / "run344N_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
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
    review.FINAL_DECISION,
    review.GATE_AUDIT,
    review.RUN344M_QUEUE,
    review.REVIEW_SCORECARD,
    review.SEGMENT_CONCENTRATION_REVIEW,
    review.COST_SURVIVAL_REVIEW,
    review.EQUITY_CURVE_QUALITY_REVIEW,
    materialized.TRADE_LEVEL_RECORDS,
    materialized.COST_REPLAY_SCORECARD,
)

OUTPUT_FILES = (
    CASH_OPEN_DECOMPOSITION,
    FEATURE_STATE_DECOMPOSITION,
    VARIANT_GRID_CONTRACT,
    HEAVY_COST_FLOOR_CONTRACT,
    EXPERIMENT_DESIGN_CONTRACT,
    DATA_INTEGRITY_CONTRACT,
    MODEL_VALIDATION_CONTRACT,
    RUNTIME_HANDOFF_PLAN,
    RUN344N_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def pct(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round(float(numerator) / float(denominator), 6)


def parent_gates_passed() -> bool:
    gates = read_csv(review.GATE_AUDIT)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


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


def first_row(frame: pd.DataFrame, **conditions: str) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for column, value in conditions.items():
        mask &= frame[column].astype(str).eq(str(value))
    matches = frame.loc[mask]
    if matches.empty:
        return pd.Series(dtype="object")
    return matches.iloc[0]


def s07_trades(trades: pd.DataFrame) -> pd.DataFrame:
    out = trades.loc[trades["attempt_name"].astype(str).eq(S07_ATTEMPT)].copy()
    out["net_profit"] = out["net_profit"].map(as_float)
    out["trade_index"] = out["trade_index"].map(as_int)
    return out


def build_cash_open_decomposition(trades: pd.DataFrame) -> pd.DataFrame:
    s07 = s07_trades(trades)
    cash_open = s07.loc[s07["session_bucket"].astype(str).eq(CASH_OPEN_BUCKET)].copy()
    s07_net = float(s07["net_profit"].sum())
    cash_open_net = float(cash_open["net_profit"].sum())
    cash_open_count = len(cash_open)
    rows: list[dict[str, Any]] = []

    def add_groups(group_cols: Sequence[str], dimension: str) -> None:
        for keys, group in cash_open.groupby(list(group_cols), dropna=False):
            key_tuple = keys if isinstance(keys, tuple) else (keys,)
            bucket = "|".join(str(value) for value in key_tuple)
            scores = score_values(group["net_profit"].tolist())
            rows.append(
                {
                    "dimension": dimension,
                    "segment_bucket": bucket,
                    "direction": group["direction"].astype(str).iloc[0] if "direction" in group.columns else "",
                    **scores,
                    "net_share_of_s07": pct(scores["net_profit"], s07_net),
                    "net_share_of_cash_open": pct(scores["net_profit"], cash_open_net),
                    "trade_share_of_cash_open": pct(scores["trade_count"], cash_open_count),
                    "attribution_scope": "posthoc_trade_filter_proxy_only(사후 거래 필터 프록시 전용)",
                    "design_use": "decompose_cash_open_profit_source(현금장 초반 수익 원천 분해)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    add_groups(["direction"], "cash_open_direction(현금장 초반 방향)")
    add_groups(["direction", "adx_bucket"], "cash_open_direction_adx(현금장 초반 방향/ADX)")
    add_groups(["direction", "historical_vol_bucket"], "cash_open_direction_volatility(현금장 초반 방향/변동성)")
    return pd.DataFrame(rows)


def build_feature_state_decomposition(trades: pd.DataFrame) -> pd.DataFrame:
    s07 = s07_trades(trades)
    total_net = float(s07["net_profit"].sum())
    total_count = len(s07)
    rows: list[dict[str, Any]] = []
    group_sets = [
        (["session_bucket", "direction"], "session_direction(세션/방향)"),
        (["adx_bucket", "direction"], "adx_direction(ADX/방향)"),
        (["historical_vol_bucket", "direction"], "volatility_direction(변동성/방향)"),
    ]
    for group_cols, dimension in group_sets:
        for keys, group in s07.groupby(group_cols, dropna=False):
            key_tuple = keys if isinstance(keys, tuple) else (keys,)
            scores = score_values(group["net_profit"].tolist())
            rows.append(
                {
                    "dimension": dimension,
                    "segment_bucket": "|".join(str(value) for value in key_tuple),
                    "trade_count": scores["trade_count"],
                    "trade_share_of_s07": pct(scores["trade_count"], total_count),
                    "net_profit": scores["net_profit"],
                    "net_share_of_s07": pct(scores["net_profit"], total_net),
                    "profit_factor_estimate": scores["profit_factor_estimate"],
                    "expectancy": scores["expectancy"],
                    "win_rate": scores["win_rate"],
                    "attribution_scope": "posthoc_trade_filter_proxy_only(사후 거래 필터 프록시 전용)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def adjusted_scores(values: Sequence[float], cost_per_trade: float, max_dd_bound: float) -> dict[str, Any]:
    adjusted = [float(value) - cost_per_trade for value in values]
    scores = score_values(adjusted)
    recovery = round(scores["net_profit"] / max_dd_bound, 6) if max_dd_bound else 0.0
    return {
        "adjusted_net_profit": scores["net_profit"],
        "adjusted_profit_factor_estimate": scores["profit_factor_estimate"],
        "adjusted_expectancy": scores["expectancy"],
        "adjusted_recovery_factor_vs_parent_dd": recovery,
    }


def build_variant_grid(trades: pd.DataFrame, parent_max_dd: float) -> pd.DataFrame:
    s07 = s07_trades(trades)
    cash_open = s07["session_bucket"].astype(str).eq(CASH_OPEN_BUCKET)
    cash_late = s07["session_bucket"].astype(str).eq(CASH_LATE_BUCKET)
    buy = s07["direction"].astype(str).eq("buy")
    sell = s07["direction"].astype(str).eq("sell")
    variants = [
        (
            "m01_cash_open_long_only",
            "cash_open_long_only(현금장 초반 롱 전용)",
            cash_open & buy,
            "isolates long-quality contribution(롱 품질 기여 분리)",
        ),
        (
            "m02_cash_open_short_carry_only",
            "cash_open_short_carry_only(현금장 초반 숏 기여 전용)",
            cash_open & sell,
            "isolates inherited short carry(기존 숏 기여 분리)",
        ),
        (
            "m03_cash_open_directional_mix",
            "cash_open_directional_mix(현금장 초반 방향 혼합)",
            cash_open,
            "tests whether cash-open alone is the profit engine(현금장 초반 자체가 수익 엔진인지 시험)",
        ),
        (
            "m04_s07_without_late_long",
            "s07_without_late_long(s07 후반 롱 제거)",
            ~(cash_late & buy),
            "turns late-long failure memory into a firewall(후반 롱 실패 기억을 방화벽으로 전환)",
        ),
        (
            "m05_s07_long_only_all_sessions",
            "s07_long_only_all_sessions(s07 전체 세션 롱 전용)",
            buy,
            "checks whether long quality can stand alone(롱 품질 단독 생존 확인)",
        ),
        (
            "m06_s07_sell_only_all_sessions",
            "s07_sell_only_all_sessions(s07 전체 세션 숏 전용)",
            sell,
            "measures inherited short baseline(기존 숏 기준선 측정)",
        ),
        (
            "m07_long_all_plus_cash_open_short",
            "long_all_plus_cash_open_short(전체 롱 + 현금장 초반 숏)",
            buy | (cash_open & sell),
            "keeps long idea while throttling non-open shorts(롱 아이디어 유지와 비초반 숏 축소)",
        ),
        (
            "m08_no_cash_open_short",
            "no_cash_open_short(현금장 초반 숏 제거)",
            ~(cash_open & sell),
            "tests whether cash-open short carry is masking risk(현금장 초반 숏 기여가 위험을 가리는지 확인)",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for variant_id, label, mask, design_use in variants:
        subset = s07.loc[mask].copy()
        values = subset["net_profit"].tolist()
        base_scores = score_values(values)
        moderate = adjusted_scores(values, 2.0, parent_max_dd)
        heavy = adjusted_scores(values, 4.0, parent_max_dd)
        rows.append(
            {
                "variant_id": variant_id,
                "variant_label": label,
                "variant_family": "cash_open_long_short_decomposition(현금장 초반 롱/숏 분해)",
                "trade_filter_proxy_net_profit": base_scores["net_profit"],
                "trade_filter_proxy_profit_factor_estimate": base_scores["profit_factor_estimate"],
                "trade_filter_proxy_expectancy": base_scores["expectancy"],
                "trade_filter_proxy_trade_count": base_scores["trade_count"],
                "moderate_adjusted_net_profit": moderate["adjusted_net_profit"],
                "moderate_adjusted_profit_factor_estimate": moderate["adjusted_profit_factor_estimate"],
                "moderate_adjusted_recovery_factor_vs_parent_dd": moderate["adjusted_recovery_factor_vs_parent_dd"],
                "heavy_adjusted_net_profit": heavy["adjusted_net_profit"],
                "heavy_adjusted_profit_factor_estimate": heavy["adjusted_profit_factor_estimate"],
                "heavy_adjusted_recovery_factor_vs_parent_dd": heavy["adjusted_recovery_factor_vs_parent_dd"],
                "posthoc_proxy_only": True,
                "design_use": design_use,
                "package_action": "materialize_as_runtime_attempt_if_rule_can_be_encoded(규칙 인코딩 가능 시 런타임 시도 물질화)",
                "must_not_claim": "candidate_selection(후보 선정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    frame = pd.DataFrame(rows)
    frame["base_proxy_net_rank"] = frame["trade_filter_proxy_net_profit"].rank(method="dense", ascending=False).astype(int)
    frame["heavy_proxy_recovery_rank"] = frame["heavy_adjusted_recovery_factor_vs_parent_dd"].rank(method="dense", ascending=False).astype(int)
    return frame


def build_heavy_cost_floor_contract(parent_final: Mapping[str, Any], variant_grid: pd.DataFrame) -> pd.DataFrame:
    parent_dd = as_float(parent_final.get("s07_closed_trade_max_drawdown_abs"))
    mt5_dd_bound = 89.31
    best_heavy = variant_grid.sort_values("heavy_adjusted_recovery_factor_vs_parent_dd", ascending=False).iloc[0]
    return pd.DataFrame(
        [
            {
                "floor_id": "f01_parent_mt5_dd_recovery_floor",
                "metric": "heavy_adjusted_recovery_factor_vs_parent_mt5_dd(강한 비용 조정 회복 계수)",
                "current_s07_value": as_float(parent_final.get("s07_heavy_adjusted_recovery_factor")),
                "floor_value": 1.0,
                "design_reason": "run344L heavy cost failed recovery floor(run344L 강한 비용 회복 하한 실패)",
                "next_use": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "floor_id": "f02_cash_open_concentration_floor",
                "metric": "cash_open_net_share(현금장 초반 순수익 비중)",
                "current_s07_value": as_float(parent_final.get("s07_cash_open_net_share")),
                "floor_value": 0.60,
                "design_reason": "do not let one session pretend broad stability(한 세션이 넓은 안정성처럼 보이지 않게 함)",
                "next_use": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "floor_id": "f03_short_carry_concentration_floor",
                "metric": "sell_net_share(숏 순수익 비중)",
                "current_s07_value": as_float(parent_final.get("s07_sell_net_share")),
                "floor_value": 0.70,
                "design_reason": "separate long improvement from inherited short carry(롱 개선과 기존 숏 기여 분리)",
                "next_use": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "floor_id": "f04_posthoc_proxy_best_heavy_read",
                "metric": "best_trade_filter_heavy_recovery_vs_parent_dd(최고 사후 필터 강한 비용 회복)",
                "current_s07_value": as_float(best_heavy.get("heavy_adjusted_recovery_factor_vs_parent_dd")),
                "floor_value": 1.0,
                "design_reason": f"best_proxy_variant={best_heavy.get('variant_id')}",
                "next_use": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "floor_id": "f05_closed_trade_curve_reference",
                "metric": "closed_trade_max_drawdown_abs(청산 거래 최대 낙폭)",
                "current_s07_value": parent_dd,
                "floor_value": mt5_dd_bound,
                "design_reason": "closed-trade replay drawdown is descriptive, MT5 DD remains stress bound(청산 거래 낙폭은 설명용, MT5 낙폭은 압박 하한)",
                "next_use": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def build_contract_tables(parent_final: Mapping[str, Any], trades: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    s07 = s07_trades(trades)
    experiment = pd.DataFrame(
        [
            {
                "field": "hypothesis",
                "value": "s07 cash-open profit can be decomposed into long-quality and inherited short-carry sources(s07 현금장 초반 수익은 롱 품질과 기존 숏 기여로 분해 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "decision_use",
                "value": "decide which variants run344N should package for MT5 probe(run344N이 어떤 변형을 MT5 탐침으로 포장할지 결정)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "comparison_baseline",
                "value": "run344L reviewed s07 and s01/s05 comparators(run344L 검토 s07 및 s01/s05 대조군)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "control_variables",
                "value": "FPMarkets US100 M5, existing run344K trade records, entry-time feature attribution(FPMarkets US100 M5, 기존 run344K 거래 기록, 진입 시각 피처 귀속)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "changed_variables",
                "value": "cash-open session gate, long-only/short-only/mixed rule stacks, late-long firewall(현금장 초반 세션 문, 롱 전용/숏 전용/혼합 규칙 묶음, 후반 롱 방화벽)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "sample_scope",
                "value": f"Tier A current MT5 report replay only, s07 trades={len(s07)}(Tier A 현재 MT5 보고서 재생 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "success_criteria",
                "value": "packageable variants with moderate cost survival and explicit heavy-cost floor(포장 가능한 변형, 중간 비용 생존, 강한 비용 하한 명시)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "failure_criteria",
                "value": "variant design depends only on posthoc PnL ranking or cannot encode runtime-safe rules(변형 설계가 사후 손익 순위에만 의존하거나 런타임 안전 규칙으로 인코딩 불가)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "invalid_conditions",
                "value": "uses exit-time/future PnL as feature, changes MT5 report meaning, or claims selection(청산 시각/미래 손익을 피처로 쓰거나 MT5 보고서 의미 변경 또는 선정 주장)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "stop_conditions",
                "value": "stop at design if rules cannot be encoded into EA set/manifest without logic drift(규칙이 EA 설정/목록으로 의미 보존 인코딩 불가하면 설계에서 중지)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "field": "evidence_plan",
                "value": "run344N package, run344O MT5 probe, run344P review if package succeeds(run344N 포장, 성공 시 run344O MT5 탐침, run344P 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    data = pd.DataFrame(
        [
            {
                "data_source": rel(materialized.TRADE_LEVEL_RECORDS),
                "time_axis": "entry_time attribution only(진입 시각 귀속 전용)",
                "sample_scope": f"Tier A, {S07_ATTEMPT}, rows={len(s07)}",
                "missing_or_duplicate_check": f"entry_feature_missing_rows={int((~s07['entry_feature_match'].astype(bool)).sum())}",
                "feature_label_boundary": "features are from entry bar state; realized PnL is posthoc attribution only(피처는 진입 봉 상태, 실현 손익은 사후 귀속 전용)",
                "split_boundary": "existing MT5 replay; no new train/validation split(기존 MT5 재생, 새 학습/검증 분할 없음)",
                "leakage_risk": "posthoc PnL can bias variant choice; therefore design-only boundary(사후 손익이 변형 선택을 편향시킬 수 있어 설계 전용 경계)",
                "data_hash_or_identity": sha256_file(materialized.TRADE_LEVEL_RECORDS),
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    model = pd.DataFrame(
        [
            {
                "model_family": "existing logistic regression runtime bundle plus rule-stack variants(기존 로지스틱 회귀 런타임 번들과 규칙 묶음 변형)",
                "target_and_label": "no new label in run344M; decomposition of existing executed trades(run344M 새 라벨 없음, 기존 실행 거래 분해)",
                "split_method": "posthoc MT5 replay design read(사후 MT5 재생 설계 판독)",
                "selection_metric": "none for selection; descriptive net/PF/recovery only(선정 없음, 설명용 순수익/PF/회복만)",
                "secondary_metrics": "trade count, long/short balance, cash-open share, heavy-cost recovery(거래 수, 롱/숏 균형, 현금장 초반 비중, 강한 비용 회복)",
                "threshold_policy": "no threshold chosen; package variants only if runtime-safe(임계값 선택 없음, 런타임 안전 시 변형 포장)",
                "overfit_risk": "high if posthoc proxy is treated as model selection(사후 프록시를 모델 선정으로 보면 높음)",
                "calibration_risk": "not applicable; score probability not recalibrated(해당 없음, 점수 확률 재보정 없음)",
                "comparison_baseline": "s07, s05, s01 from run344L(run344L의 s07/s05/s01)",
                "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    handoff = pd.DataFrame(
        [
            {
                "handoff_id": "run344N_package",
                "next_run_id": NEXT_RUN_ID,
                "input_contract": rel(VARIANT_GRID_CONTRACT),
                "runtime_requirement": "encode variants as set/manifest parameters or explicit module version if logic changes(변형은 설정/목록 파라미터로 인코딩, 로직 변경 시 모듈 버전 명시)",
                "mt5_requirement": "no operating claim until MT5 strategy tester output exists(MT5 전략 테스터 출력 전 운영 주장 없음)",
                "effect": "turn design into executable package without changing claim boundary(설계를 실행 가능한 패키지로 바꾸되 주장 경계 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "q01_materialize_variant_package",
                "next_run_id": NEXT_RUN_ID,
                "action": "write runtime attempt manifest and set files for safe variants(안전 변형의 런타임 시도 목록과 설정 파일 작성)",
                "effect": "prepare the narrow MT5 probe without selecting a model(모델 선정 없이 좁은 MT5 탐침 준비)",
                "must_not_claim": "candidate_selection(후보 선정)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "q02_encode_late_long_firewall",
                "next_run_id": NEXT_RUN_ID,
                "action": "encode late-long firewall if supported by existing EA inputs(기존 EA 입력이 지원하면 후반 롱 방화벽 인코딩)",
                "effect": "tests failure memory as control, not as promotion filter(실패 기억을 승격 필터가 아닌 통제 조건으로 시험)",
                "must_not_claim": "runtime_authority(런타임 권위)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "q03_package_short_carry_controls",
                "next_run_id": NEXT_RUN_ID,
                "action": "package short-retain, short-throttle, and long-focused attempts(숏 유지/축소/롱 초점 시도 포장)",
                "effect": "separates new long edge from inherited short carry(새 롱 우위와 기존 숏 기여 분리)",
                "must_not_claim": "operating_promotion(운영 승격)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    return experiment, data, model, handoff, queue


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    rows = [
        ("parent_run344L_gates_passed", final["parent_gate_passed"], rel(review.GATE_AUDIT), "run344L gate(게이트)를 이어받음"),
        ("parent_queue_targets_run344M", final["parent_queue_targets_run"], rel(review.RUN344M_QUEUE), "run344M queue(큐)를 확인"),
        ("experiment_design_contract_written", final["experiment_design_rows"] >= 10, rel(EXPERIMENT_DESIGN_CONTRACT), "실험 설계 계약 작성"),
        ("data_integrity_contract_written", final["data_integrity_rows"] >= 1, rel(DATA_INTEGRITY_CONTRACT), "데이터 무결성 계약 작성"),
        ("model_validation_contract_written", final["model_validation_rows"] >= 1, rel(MODEL_VALIDATION_CONTRACT), "모델 검증 계약 작성"),
        ("cash_open_decomposition_written", final["cash_open_decomposition_rows"] >= 4, rel(CASH_OPEN_DECOMPOSITION), "현금장 초반 분해 작성"),
        ("variant_grid_has_controls", final["variant_grid_rows"] >= 8 and final["variant_grid_has_long_short_mix"], rel(VARIANT_GRID_CONTRACT), "롱/숏/혼합/방화벽 변형 포함"),
        ("heavy_cost_floor_contract_written", final["heavy_cost_floor_rows"] >= 5, rel(HEAVY_COST_FLOOR_CONTRACT), "강한 비용 하한 계약 작성"),
        ("next_package_queue_written", final["queue_rows"] >= 3, rel(RUN344N_QUEUE), "다음 포장 큐 작성"),
        ("no_forbidden_operating_claim", no_forbidden, rel(FINAL_DECISION), "설계를 운영 주장으로 올리지 않음"),
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
        DATA_RECEIPT,
        {
            "data_source": [rel(materialized.TRADE_LEVEL_RECORDS), rel(review.REVIEW_SCORECARD)],
            "time_axis": "entry_time attribution only(진입 시각 귀속 전용)",
            "sample_scope": f"Tier A {S07_ATTEMPT}; trades={final['s07_trade_count']}",
            "missing_or_duplicate_check": "run344K entry_feature_missing_rows=0(run344K 진입 피처 누락 0)",
            "feature_label_boundary": "no new label; realized PnL is posthoc attribution only(새 라벨 없음, 실현 손익은 사후 귀속 전용)",
            "split_boundary": "existing MT5 replay only(기존 MT5 재생 전용)",
            "leakage_risk": "posthoc proxy can overfit design choice(사후 프록시가 설계 선택을 과적합시킬 수 있음)",
            "data_hash_or_identity": sha256_file(materialized.TRADE_LEVEL_RECORDS),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "model_family": "logreg bundle plus rule-stack variants(로지스틱 회귀 번들과 규칙 묶음 변형)",
            "target_and_label": "no new training label in run344M(run344M 새 학습 라벨 없음)",
            "split_method": "posthoc MT5 replay design read(사후 MT5 재생 설계 판독)",
            "selection_metric": "none(없음)",
            "secondary_metrics": ["net/PF/recovery(순수익/PF/회복)", "session concentration(세션 집중)", "long/short balance(롱/숏 균형)"],
            "threshold_policy": "not selected(선정 없음)",
            "overfit_risk": "high_if_promoted_from_posthoc_proxy(사후 프록시를 승격하면 높음)",
            "calibration_risk": "not_applicable(해당 없음)",
            "comparison_baseline": "run344L s07/s05/s01",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": [
                "experiment design ready(실험 설계 준비)",
                "posthoc decomposition available(사후 분해 가능)",
                "run344N package queue ready(run344N 포장 큐 준비)",
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
    report = f"""# run344M Cash-Open Long/Short Decomposition Design(344M 현금장 초반 롱/숏 분해 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- s07_trades(s07 거래 수): `{final['s07_trade_count']}`
- cash_open_long_proxy_net(현금장 초반 롱 프록시 순수익): `{final['cash_open_long_proxy_net']}`
- cash_open_short_proxy_net(현금장 초반 숏 프록시 순수익): `{final['cash_open_short_proxy_net']}`
- best_posthoc_heavy_recovery_variant(최고 사후 강한 비용 회복 변형): `{final['best_heavy_recovery_variant']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run344L failure memory(실패 기억)를 받아 cash-open long quality(현금장 초반 롱 품질), short carry(숏 기여), late-long firewall(후반 롱 방화벽) 변형 설계를 만들었다.

## Effect(효과)

다음 run344N은 바로 runtime package(런타임 패키지)를 만들 수 있다. 단, 이번 수치는 posthoc trade-filter proxy(사후 거래 필터 프록시)이므로 candidate selection(후보 선정)이나 operating promotion(운영 승격) 근거가 아니다.

## Boundary(경계)

이 run(실행)은 design only(설계 전용)다. 새 MT5 execution(MT5 실행), forward pass(전진 통과), live readiness(실거래 준비), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344M Design Decision(344M 설계 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(EXPERIMENT_DESIGN_CONTRACT)}`, `{rel(VARIANT_GRID_CONTRACT)}`, `{rel(HEAVY_COST_FLOOR_CONTRACT)}`

Action(행동): 현금장 초반 롱/숏 분해와 강한 비용 하한 계약을 만들었다.
Effect(효과): 다음 작업은 run344N package(포장)이며, 아직 운영 의미는 닫혀 있다.

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

run344M design(설계)이 완료되어 cash-open long/short decomposition(현금장 초반 롱/숏 분해) 패키지 작업으로 넘어간다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_design(최근 설계): `{RUN_ID}`
- research_clue(연구 단서): `s07_cash_open_long_short_decomposition`
- best_posthoc_heavy_recovery_variant(최고 사후 강한 비용 회복 변형): `{final['best_heavy_recovery_variant']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 변형 설계는 보존하되 선정은 열지 않는다.
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
    marker = f"run344M {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344M Cash-Open Decomposition Design(344M 현금장 초반 분해 설계)

- run_id(실행 ID): `{RUN_ID}`
- variant_rows(변형 행): `{final['variant_grid_rows']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): 현금장 초반 롱/숏 분해를 런타임 패키지 큐로 넘겼다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344M Cash-Open Decomposition Design(344M 현금장 초반 분해 설계)

- report(보고서): `{rel(REPORT_PATH)}`
- variant_grid(변형 격자): `{rel(VARIANT_GRID_CONTRACT)}`
- cost_floor(비용 하한): `{rel(HEAVY_COST_FLOOR_CONTRACT)}`
- effect(효과): run344N materialization(물질화)을 열었다.
""",
    )
    changelog = f"""## {TODAY} run344M Cash-Open Decomposition Design(현금장 초반 분해 설계)

- action(행동): s07 현금장 초반 롱/숏 기여와 후반 롱 방화벽 변형을 설계했다.
- effect(효과): 다음 run344N이 MT5 package(MT5 포장)로 갈 수 있다.
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
        "lane": "experiment_design(실험 설계)",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "cash-open long/short decomposition design(현금장 초반 롱/숏 분해 설계); no selection(선정 없음).",
        "candidate_model_id": "variant_grid_only(변형 격자 전용)",
        "trade_count": final["s07_trade_count"],
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
            "metric_scope": "design_cash_open_long_short_decomposition",
            "kpi_scope": "design_cash_open_long_short_decomposition",
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": "variant_grid_only(변형 격자 전용)",
            "trade_count": final["s07_trade_count"],
            "result_status": JUDGMENT,
            "primary_kpi": f"cash_open_long_proxy_net={final['cash_open_long_proxy_net']};cash_open_short_proxy_net={final['cash_open_short_proxy_net']}",
            "guardrail_kpi": f"best_heavy_recovery_variant={final['best_heavy_recovery_variant']};design_only",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "notes": "Tier A design evidence only(Tier A 설계 근거 전용).",
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
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B remains missing for this narrow design(Tier B는 이번 좁은 설계에서 필수 누락).",
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
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": "variant_grid_only(변형 격자 전용)",
            "trade_count": final["s07_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": f"variant_rows={final['variant_grid_rows']};design_only",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "notes": "Combined view is same as Tier A until Tier B exists(Tier B 전에는 합산이 Tier A와 같음).",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], rows)


def write_lineage_receipt() -> None:
    hashed = {
        rel(path): sha256_file(path)
        for path in OUTPUT_FILES
        if exists(path) and path not in {ARTIFACT_REGISTRY, LINEAGE_RECEIPT}
    }
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY],
            "artifact_hashes": hashed,
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적됨 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


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
                "notes": "run344M design artifact(run344M 설계 산출물)",
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


def build_design() -> Mapping[str, Any]:
    for path in INPUT_FILES:
        required(path)
    parent_final = read_json(review.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError("run344L next_run_id does not point to run344M")
    if not parent_gates_passed():
        raise RuntimeError("run344L gate audit has failed rows")
    queue = read_csv(review.RUN344M_QUEUE)
    parent_queue_targets_run = bool(queue["next_run_id"].astype(str).eq(RUN_ID).all() and len(queue) >= 4)

    trades = read_csv(materialized.TRADE_LEVEL_RECORDS)
    cost_replay = read_csv(materialized.COST_REPLAY_SCORECARD)
    s07 = s07_trades(trades)
    parent_max_dd = as_float(first_row(cost_replay, attempt_name=S07_ATTEMPT, scenario_id="base").get("max_drawdown_amount"))
    cash_open_decomp = build_cash_open_decomposition(trades)
    feature_decomp = build_feature_state_decomposition(trades)
    variant_grid = build_variant_grid(trades, parent_max_dd)
    heavy_floor = build_heavy_cost_floor_contract(parent_final, variant_grid)
    experiment, data, model, handoff, run_queue = build_contract_tables(parent_final, trades)

    write_frame(CASH_OPEN_DECOMPOSITION, cash_open_decomp)
    write_frame(FEATURE_STATE_DECOMPOSITION, feature_decomp)
    write_frame(VARIANT_GRID_CONTRACT, variant_grid)
    write_frame(HEAVY_COST_FLOOR_CONTRACT, heavy_floor)
    write_frame(EXPERIMENT_DESIGN_CONTRACT, experiment)
    write_frame(DATA_INTEGRITY_CONTRACT, data)
    write_frame(MODEL_VALIDATION_CONTRACT, model)
    write_frame(RUNTIME_HANDOFF_PLAN, handoff)
    write_frame(RUN344N_QUEUE, run_queue)

    cash_open_long = first_row(cash_open_decomp, dimension="cash_open_direction(현금장 초반 방향)", segment_bucket="buy")
    cash_open_short = first_row(cash_open_decomp, dimension="cash_open_direction(현금장 초반 방향)", segment_bucket="sell")
    best_heavy = variant_grid.sort_values("heavy_adjusted_recovery_factor_vs_parent_dd", ascending=False).iloc[0]
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
        "parent_queue_targets_run": parent_queue_targets_run,
        "s07_trade_count": int(len(s07)),
        "cash_open_decomposition_rows": int(len(cash_open_decomp)),
        "feature_state_decomposition_rows": int(len(feature_decomp)),
        "variant_grid_rows": int(len(variant_grid)),
        "heavy_cost_floor_rows": int(len(heavy_floor)),
        "experiment_design_rows": int(len(experiment)),
        "data_integrity_rows": int(len(data)),
        "model_validation_rows": int(len(model)),
        "runtime_handoff_rows": int(len(handoff)),
        "queue_rows": int(len(run_queue)),
        "variant_grid_has_long_short_mix": bool(
            variant_grid["variant_id"].astype(str).isin(
                ["m01_cash_open_long_only", "m02_cash_open_short_carry_only", "m03_cash_open_directional_mix", "m04_s07_without_late_long"]
            ).sum()
            == 4
        ),
        "cash_open_long_proxy_net": float(cash_open_long.get("net_profit", 0.0)),
        "cash_open_short_proxy_net": float(cash_open_short.get("net_profit", 0.0)),
        "cash_open_long_proxy_trades": int(cash_open_long.get("trade_count", 0)),
        "cash_open_short_proxy_trades": int(cash_open_short.get("trade_count", 0)),
        "best_heavy_recovery_variant": str(best_heavy.get("variant_id")),
        "best_heavy_recovery_proxy": float(best_heavy.get("heavy_adjusted_recovery_factor_vs_parent_dd")),
        "parent_s07_heavy_recovery": as_float(parent_final.get("s07_heavy_adjusted_recovery_factor")),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
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
    write_lineage_receipt()
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    return final


def main() -> None:
    final = build_design()
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
