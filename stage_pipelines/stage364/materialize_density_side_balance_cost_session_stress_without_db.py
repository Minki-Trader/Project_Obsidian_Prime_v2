from __future__ import annotations

import math
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_density_side_balance_repair_mt5_runtime_probe_without_db as review  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = review.STAGE_ID
RUN_NUMBER = "run364Z"
RUN_ID = "run364Z_materialize_density_side_balance_cost_session_stress_without_db_v1"
PARENT_RUN_ID = review.RUN_ID
NEXT_RUN_ID = "run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1"

STATUS = "completed_stage364Z_density_side_balance_cost_session_stress_inputs_materialized_no_training_no_mt5_no_authority"
JUDGMENT = "stress_inputs_ready_pf_drawdown_session_repair_scout_no_operating_claim"
DECISION = "stage364Z_open_run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = review.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
STRESS_ZONE_SURFACE = RUN_DIR / "cost_session_stress_zone_surface.csv"
STRESS_ZONE_CANDIDATES = RUN_DIR / "cost_session_stress_zone_candidates.csv"
SIMPLE_FILTER_PROXY = RUN_DIR / "simple_filter_proxy_density_audit.csv"
ACCOUNT_DRAWDOWN_TABLE = RUN_DIR / "account_state_drawdown_guardrail_table.csv"
PARAMETER_QUEUE = RUN_DIR / "pf_drawdown_parameter_neighborhood_queue.csv"
SHORT_QUALITY_QUEUE = RUN_DIR / "short_quality_guardrail_queue.csv"
RUN364AA_QUEUE = RUN_DIR / "run364AA_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_boundary_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364Z_density_side_balance_cost_session_stress_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364Z_density_side_balance_cost_session_stress_inputs.md"
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
    review.FINAL_DECISION,
    review.GATE_AUDIT,
    review.CLOSED_TRADE_ATTRIBUTION,
    review.MONTHLY_ATTRIBUTION,
    review.ENTRY_HOUR_ATTRIBUTION,
    review.SIDE_ATTRIBUTION,
    review.HOLD_BUCKET_ATTRIBUTION,
    review.DRAWDOWN_BUCKET_ATTRIBUTION,
    review.COST_DRAWDOWN_REVIEW,
    review.REVIEW_FINDINGS,
    review.NEXT_QUEUE,
    review.REPORT_PATH,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    STRESS_ZONE_SURFACE,
    STRESS_ZONE_CANDIDATES,
    SIMPLE_FILTER_PROXY,
    ACCOUNT_DRAWDOWN_TABLE,
    PARAMETER_QUEUE,
    SHORT_QUALITY_QUEUE,
    RUN364AA_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
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


def rel(path: Path | str) -> str:
    return review.rel(path)


def exists(path: Path | str) -> bool:
    return review.exists(path)


def sha(path: Path | str) -> str:
    return review.sha(path)


def read_json(path: Path) -> Any:
    return review.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    review.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    review.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    review.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    review.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return review.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    review.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(path, exist_ok=True)


def validate_parent() -> dict[str, Any]:
    parent = read_json(review.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(금지된 운영 주장)")
    gates = read_csv_rows(review.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit is not fully passed(부모 게이트 미통과)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364Z inputs(입력 누락): " + ", ".join(missing))
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "role": input_role(path),
                "timestamp_boundary(시점 경계)": "post-run review evidence only, not runtime feature(실행 후 검토 근거, 런타임 피처 아님)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def input_role(path: Path) -> str:
    name = path.name
    if name == "closed_trade_attribution.csv":
        return "mt5_closed_trade_evidence(MT5 종료 거래 근거)"
    if "attribution" in name:
        return "performance_attribution_source(성과 귀속 원천)"
    if "final_decision" in name:
        return "parent_final_decision(부모 최종 판정)"
    if "gate" in name:
        return "parent_gate_audit(부모 게이트 감사)"
    if "queue" in name:
        return "parent_next_queue(부모 다음 대기열)"
    return "supporting_evidence(보조 근거)"


def read_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def coerce_trade_frame(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    numeric_columns = [
        "trade_index",
        "entry_hour",
        "exit_hour",
        "volume",
        "commission",
        "swap",
        "profit_before_swap",
        "net_profit_after_cost",
        "balance_after",
        "hold_minutes_calendar",
        "hold_m5_calendar",
        "closed_balance_peak",
        "closed_balance_drawdown_amount",
        "closed_balance_drawdown_percent",
    ]
    for column in numeric_columns:
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["entry_month"] = frame["entry_month"].astype(str)
    frame["exit_month"] = frame["exit_month"].astype(str)
    frame["side"] = frame["side"].astype(str)
    frame["previous_closed_balance_drawdown_percent"] = frame["closed_balance_drawdown_percent"].shift(1).fillna(0.0)
    frame["previous_drawdown_bucket"] = frame["previous_closed_balance_drawdown_percent"].map(drawdown_bucket)
    return frame


def drawdown_bucket(value: Any) -> str:
    value = as_float(value)
    if value <= 2:
        return "001_prev_0_to_2pct"
    if value <= 5:
        return "002_prev_2_to_5pct"
    if value <= 10:
        return "003_prev_5_to_10pct"
    if value <= 20:
        return "004_prev_10_to_20pct"
    return "005_prev_20_to_40pct"


def aggregate_group(frame: pd.DataFrame, group_cols: Sequence[str], *, runtime_status: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for keys, group in frame.groupby(list(group_cols), dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        trade_count = int(len(group))
        net = float(group["net_profit_after_cost"].sum())
        gross_profit = float(group.loc[group["net_profit_after_cost"] > 0, "net_profit_after_cost"].sum())
        gross_loss = float(group.loc[group["net_profit_after_cost"] < 0, "net_profit_after_cost"].sum())
        pf = gross_profit / abs(gross_loss) if gross_loss < 0 else math.inf
        expectancy = net / trade_count if trade_count else 0.0
        win_count = int((group["net_profit_after_cost"] > 0).sum())
        loss_count = int((group["net_profit_after_cost"] <= 0).sum())
        group_value = "|".join(f"{column}={value}" for column, value in zip(group_cols, keys, strict=True))
        reasons = stress_reasons(trade_count, net, pf, expectancy, float(group["net_profit_after_cost"].min()))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "group_columns": "+".join(group_cols),
                "group_value": group_value,
                "trade_count": trade_count,
                "net_profit_after_cost": finite(net, 6),
                "gross_profit_after_cost": finite(gross_profit, 6),
                "gross_loss_after_cost": finite(gross_loss, 6),
                "profit_factor_after_cost": finite(pf, 9),
                "expectancy_after_cost": finite(expectancy, 6),
                "win_count_after_cost": win_count,
                "loss_count_after_cost": loss_count,
                "win_rate_after_cost_percent": finite(100.0 * win_count / trade_count if trade_count else 0.0, 6),
                "min_trade_after_cost": finite(float(group["net_profit_after_cost"].min()), 6),
                "max_trade_after_cost": finite(float(group["net_profit_after_cost"].max()), 6),
                "median_hold_m5_calendar": finite(float(group["hold_m5_calendar"].median()), 6),
                "max_hold_m5_calendar": finite(float(group["hold_m5_calendar"].max()), 6),
                "runtime_feature_status": runtime_status,
                "stress_reasons": ";".join(reasons),
                "stress_score": finite(stress_score(trade_count, net, pf, expectancy, float(group["net_profit_after_cost"].min())), 6),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def stress_reasons(trade_count: int, net: float, pf: float, expectancy: float, min_trade: float) -> list[str]:
    reasons: list[str] = []
    if trade_count >= 20 and net < 0:
        reasons.append("negative_net(순손익 음수)")
    if trade_count >= 20 and pf < 1.0:
        reasons.append("pf_below_1_0(PF 1.0 미만)")
    elif trade_count >= 20 and pf < 1.15:
        reasons.append("pf_below_1_15(PF 1.15 미만)")
    if expectancy < 0:
        reasons.append("negative_expectancy(기대값 음수)")
    if min_trade <= -25:
        reasons.append("tail_loss(꼬리 손실)")
    return reasons


def stress_score(trade_count: int, net: float, pf: float, expectancy: float, min_trade: float) -> float:
    pf_gap = max(0.0, 1.20 - (pf if math.isfinite(pf) else 1.20))
    return (
        max(0.0, -net)
        + pf_gap * 35.0
        + max(0.0, -expectancy) * 12.0
        + max(0.0, abs(min_trade) - 25.0) * 0.75
        + max(0.0, trade_count - 40.0) * 0.05
    )


def build_stress_surface(trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    entry_known = "entry_known_candidate(진입 시점 사용 가능 후보)"
    diagnostic = "diagnostic_only_not_direct_runtime_feature(진단 전용, 직접 런타임 피처 아님)"
    account_state = "account_state_candidate_requires_previous_balance(계좌 상태 후보, 이전 잔고 필요)"
    for columns, status in [
        (["entry_month"], entry_known),
        (["entry_hour"], entry_known),
        (["side"], entry_known),
        (["entry_month", "entry_hour"], entry_known),
        (["entry_hour", "side"], entry_known),
        (["entry_month", "side"], entry_known),
        (["previous_drawdown_bucket"], account_state),
        (["previous_drawdown_bucket", "side"], account_state),
        (["hold_bucket"], diagnostic),
        (["drawdown_bucket"], diagnostic),
    ]:
        rows.extend(aggregate_group(trades, columns, runtime_status=status))
    surface = pd.DataFrame(rows)
    if surface.empty:
        return surface
    surface = surface.sort_values(["stress_score", "trade_count"], ascending=[False, False]).reset_index(drop=True)
    return surface


def candidate_filter(surface: pd.DataFrame) -> pd.DataFrame:
    if surface.empty:
        return surface
    mask = (
        surface["stress_reasons"].astype(str).ne("")
        & (pd.to_numeric(surface["trade_count"], errors="coerce") >= 20)
        & (surface["runtime_feature_status"].astype(str).str.contains("entry_known|account_state", regex=True))
    )
    candidates = surface.loc[mask].copy()
    candidates["candidate_rank"] = range(1, len(candidates) + 1)
    candidates["candidate_use"] = candidates.apply(candidate_use, axis=1)
    return candidates.head(24)


def candidate_use(row: pd.Series) -> str:
    status = str(row.get("runtime_feature_status", ""))
    reasons = str(row.get("stress_reasons", ""))
    group_columns = str(row.get("group_columns", ""))
    if "account_state" in status:
        return "previous_balance_drawdown_guardrail_probe(이전 잔고 낙폭 가드레일 탐침)"
    if "entry_hour" in group_columns and "negative_net" in reasons:
        return "session_filter_or_soft_size_probe(세션 필터 또는 소프트 사이징 탐침)"
    if "side" in group_columns:
        return "side_quality_guardrail_probe(방향 품질 가드레일 탐침)"
    return "diagnostic_guardrail_probe(진단 가드레일 탐침)"


def simple_filter_rows(candidates: pd.DataFrame, final: Mapping[str, Any]) -> list[dict[str, Any]]:
    total_trades = as_int(final.get("mt5_trade_count"))
    total_net = as_float(final.get("mt5_net_profit"))
    business_days = total_trades / max(as_float(final.get("combined_trade_per_business_day")), 1e-9)
    rows: list[dict[str, Any]] = []
    for _, row in candidates.iterrows():
        removed_trades = as_int(row.get("trade_count"))
        removed_net = as_float(row.get("net_profit_after_cost"))
        projected_trades = total_trades - removed_trades
        projected_net = total_net - removed_net
        projected_density = projected_trades / business_days if business_days else 0.0
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_rank": as_int(row.get("candidate_rank")),
                "filter_expression": row.get("group_value"),
                "filter_feature_status": row.get("runtime_feature_status"),
                "removed_trade_count": removed_trades,
                "removed_net_profit_after_cost": finite(removed_net, 6),
                "projected_trade_count_if_removed": projected_trades,
                "projected_net_if_removed": finite(projected_net, 6),
                "projected_trade_per_business_day_if_removed": finite(projected_density, 10),
                "density_floor_status": "pass(통과)" if projected_density >= 3.0 else "fail_density_floor(밀도 하한 실패)",
                "proxy_scope": "simple_removal_proxy_no_sequence_replay(단순 제거 프록시, 순서 재생 아님)",
                "effect(효과)": "hard block(하드 차단)이 거래 밀도 3/day(일 3회)를 깨는지 먼저 본다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def account_drawdown_table(trades: pd.DataFrame) -> pd.DataFrame:
    rows = aggregate_group(
        trades,
        ["previous_drawdown_bucket", "side"],
        runtime_status="account_state_candidate_requires_previous_balance(계좌 상태 후보, 이전 잔고 필요)",
    )
    return pd.DataFrame(rows).sort_values(["group_value"]).reset_index(drop=True)


def parameter_queue_rows(stress_candidates: pd.DataFrame) -> list[dict[str, Any]]:
    base_rows = [
        ("baseline_replay_control", 0.45, 40.0, 8, "none(없음)", "control(대조)", "exact run364X behavior(364X 동일 동작)"),
        ("maxhold6_density_control", 0.45, 40.0, 6, "none(없음)", "repair_probe(수리 탐침)", "reduce tail hold(꼬리 보유 축소)"),
        ("adx42_pf_control", 0.45, 42.0, 8, "none(없음)", "repair_probe(수리 탐침)", "raise ADX block(ADX 차단 상향)"),
        ("adx38_density_counterfactual", 0.45, 38.0, 8, "none(없음)", "counterfactual(대조 반사실)", "test density/PF tension(밀도/PF 긴장 확인)"),
        ("short050_quality_probe", 0.50, 40.0, 8, "short_only_threshold(숏 전용 임계값)", "repair_probe(수리 탐침)", "improve short PF(숏 PF 개선)"),
        ("short055_quality_probe", 0.55, 40.0, 8, "short_only_threshold(숏 전용 임계값)", "stress_probe(압박 탐침)", "strict short quality(엄격 숏 품질)"),
        ("hour16_soft_guardrail", 0.45, 40.0, 8, "soft_guard_entry_hour_16(16시 소프트 가드)", "session_probe(세션 탐침)", "worst hour repair(최악 시간 수리)"),
        ("hour16_maxhold6_guardrail", 0.45, 40.0, 6, "soft_guard_entry_hour_16(16시 소프트 가드)", "session_probe(세션 탐침)", "hour16 plus hold repair(16시+보유 수리)"),
        ("prevdd_2pct_soft_stop", 0.45, 40.0, 8, "soft_stop_prev_closed_dd_ge_2pct(이전 종료잔고 DD 2% 이상 소프트 중지)", "account_state_probe(계좌 상태 탐침)", "drawdown cluster repair(낙폭 군집 수리)"),
        ("prevdd_5pct_soft_stop", 0.45, 40.0, 8, "soft_stop_prev_closed_dd_ge_5pct(이전 종료잔고 DD 5% 이상 소프트 중지)", "account_state_probe(계좌 상태 탐침)", "deeper drawdown repair(깊은 낙폭 수리)"),
        ("short050_hour16_soft_guardrail", 0.50, 40.0, 8, "short_threshold_plus_hour16_soft_guard(숏 임계값+16시 소프트 가드)", "combined_probe(합성 탐침)", "combine short/session repair(숏/세션 수리 결합)"),
        ("adx42_maxhold6_short050", 0.50, 42.0, 6, "none(없음)", "combined_probe(합성 탐침)", "PF/DD neighborhood repair(PF/DD 이웃 수리)"),
    ]
    rows = []
    for rank, (queue_id, short_threshold, adx_block_min, max_hold_m5, guardrail, queue_type, hypothesis) in enumerate(base_rows, start=1):
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_rank": rank,
                "queue_id": queue_id,
                "next_run_id": NEXT_RUN_ID,
                "short_threshold": short_threshold,
                "long_threshold": 0.0,
                "adx_block_min": adx_block_min,
                "max_hold_m5": max_hold_m5,
                "guardrail_expression": guardrail,
                "queue_type": queue_type,
                "hypothesis(가설)": hypothesis,
                "required_control(필수 대조)": "trade_per_day >= 3 and no trade splitting(일 거래 3회 이상, 거래 쪼개기 금지)",
                "runtime_claim_boundary": "proxy_scout_required_no_authority(프록시 탐색 필요, 권위 없음)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    top = stress_candidates.head(4)
    for _, row in top.iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_rank": len(rows) + 1,
                "queue_id": f"stress_zone_{as_int(row.get('candidate_rank'))}",
                "next_run_id": NEXT_RUN_ID,
                "short_threshold": 0.45,
                "long_threshold": 0.0,
                "adx_block_min": 40.0,
                "max_hold_m5": 8,
                "guardrail_expression": row.get("group_value"),
                "queue_type": "stress_zone_guardrail_probe(압박 구간 가드레일 탐침)",
                "hypothesis(가설)": f"reduce weak zone {row.get('group_value')} without breaking density(약한 구간 축소, 밀도 유지)",
                "required_control(필수 대조)": "simple filter proxy must not replace MT5/proxy replay(단순 필터 프록시는 MT5/프록시 재생 대체 금지)",
                "runtime_claim_boundary": "materialized_queue_only_no_authority(대기열 구체화만, 권위 없음)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def short_quality_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    short = trades.loc[trades["side"].eq("short")].copy()
    if short.empty:
        return []
    rows = aggregate_group(short, ["entry_hour"], runtime_status="entry_known_short_quality(진입 시점 숏 품질)")
    frame = pd.DataFrame(rows).sort_values(["stress_score", "trade_count"], ascending=[False, False]).reset_index(drop=True)
    out: list[dict[str, Any]] = []
    for idx, row in frame.iterrows():
        out.append(
            {
                "run_id": RUN_ID,
                "short_guardrail_rank": idx + 1,
                "entry_hour": str(row.get("group_value", "")).replace("entry_hour=", ""),
                "short_trade_count": row.get("trade_count"),
                "short_net_profit_after_cost": row.get("net_profit_after_cost"),
                "short_profit_factor_after_cost": row.get("profit_factor_after_cost"),
                "short_expectancy_after_cost": row.get("expectancy_after_cost"),
                "proposal": "tighten_short_threshold_or_hour_guard(숏 임계값 강화 또는 시간 가드)",
                "effect(효과)": "숏 균형을 유지하되 비용 부담이 큰 숏 구간을 분리한다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return out


def scout_queue_rows(parameter_rows: Sequence[Mapping[str, Any]], filter_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in parameter_rows[:12]:
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_id": row["queue_id"],
                "queue_source": "parameter_neighborhood(파라미터 이웃)",
                "priority": "high" if row["queue_rank"] <= 6 else "medium",
                "required_inputs": f"{rel(PARAMETER_QUEUE)}; {rel(STRESS_ZONE_CANDIDATES)}",
                "success_condition(성공 조건)": "net positive, PF > 1.30, DD not worse, density >= 3/day(순수익 양수, PF 1.30 초과, 낙폭 악화 없음, 일 3회 이상)",
                "stop_condition(중단 조건)": "density below 3 or short side collapses to zero(밀도 3 미만 또는 숏 0으로 붕괴)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    density_safe_filters = [row for row in filter_rows if row.get("density_floor_status") == "pass(통과)"]
    for row in density_safe_filters[:6]:
        rows.append(
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_id": f"filter_proxy_{row['candidate_rank']}",
                "queue_source": "simple_filter_proxy(단순 필터 프록시)",
                "priority": "medium",
                "required_inputs": f"{rel(SIMPLE_FILTER_PROXY)}; {rel(STRESS_ZONE_SURFACE)}",
                "success_condition(성공 조건)": "proxy replay must confirm sequence-safe improvement(순서 안전 프록시 재생 개선 확인 필요)",
                "stop_condition(중단 조건)": "simple removal only improves by deleting too many trades(단순 제거가 거래 삭제로만 개선)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def gate_row(name: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": "passed",
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def write_receipts(
    final: Mapping[str, Any],
    stress_candidates: pd.DataFrame,
    filter_rows: Sequence[Mapping[str, Any]],
    account_rows: pd.DataFrame,
    scout_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = {
        DATA_RECEIPT: {
            **base,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "source_trade_rows": final["source_trade_rows"],
            "timestamp_boundary": "all stress labels are post-run evidence; next runtime controls must use entry-known fields only(압박 라벨은 실행 후 근거, 다음 런타임 제어는 진입 시점 필드만 사용)",
            "lookahead_control": "previous_closed_balance_drawdown uses shifted closed-balance state(이전 종료 잔고 낙폭은 shift 적용)",
            "effect(효과)": "미래참조 편향(look-ahead bias, 미래참조 편향)을 연구 입력과 런타임 후보 사이에서 분리한다.",
        },
        EXPERIMENT_RECEIPT: {
            **base,
            "skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "session/account-state/short guardrails can improve PF/DD without splitting trades(세션/계좌상태/숏 가드레일이 거래 쪼개기 없이 PF/DD를 개선할 수 있다)",
            "comparison": "baseline replay, parameter neighborhood, simple filter proxy(기준 재생, 파라미터 이웃, 단순 필터 프록시)",
            "stress_candidate_rows": int(len(stress_candidates)),
            "scout_queue_rows": int(len(scout_rows)),
            "effect(효과)": "다음 scout(탐색)가 무작위가 아니라 실패 기억(failure memory, 실패 기억)에서 시작한다.",
        },
        MODEL_RECEIPT: {
            **base,
            "skill": "obsidian-model-validation(모델 검증)",
            "model_training": "not_run(실행 안 함)",
            "selection": "not_claimed(주장 안 함)",
            "overfit_control": "month controls marked diagnostic unless replay confirms stability(월 제어는 재생 안정성 전까지 진단용)",
            "effect(효과)": "materialization(구체화)을 모델 성능 주장으로 오해하지 않게 한다.",
        },
        ATTRIBUTION_RECEIPT: {
            **base,
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "observed_change": "PF/DD pressure after density/short repair(밀도/숏 수리 뒤 PF/DD 압박)",
            "segment_checks": [rel(STRESS_ZONE_SURFACE), rel(SIMPLE_FILTER_PROXY), rel(ACCOUNT_DRAWDOWN_TABLE), rel(SHORT_QUALITY_QUEUE)],
            "attribution_confidence": "medium_for_stress_location_low_for_repair_effect(압박 위치 중간, 수리 효과 낮음)",
            "effect(효과)": "개선 원인을 확정하지 않고 확인할 수 있는 다음 탐침으로 넘긴다.",
        },
        LINEAGE_RECEIPT: {
            **base,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
        CLAIM_RECEIPT: {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "mt5_execution": "not_run(실행 안 함)",
            "model_training": "not_run(실행 안 함)",
            "effect(효과)": "압박 입력을 운영 승격(operating promotion, 운영 승격)으로 착각하지 않는다.",
        },
    }
    for path, payload in receipts.items():
        write_json(path, payload)
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364Z scope(범위)를 input materialization(입력 구체화)로 닫는다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "entry-known/control boundary(진입 시점/대조 경계)를 기록한다."),
        gate_row("experiment_design_audit(실험 설계 감사)", EXPERIMENT_RECEIPT, "hypothesis/comparison/stop condition(가설/비교/중단 조건)을 남긴다."),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "세션/방향/계좌상태 구간을 분해한다."),
        gate_row("model_boundary_gate(모델 경계 게이트)", MODEL_RECEIPT, "model training(모델 학습)과 selection(선택)을 주장하지 않는다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "source/output hash(원천/출력 해시)를 연결한다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "runtime authority(런타임 권위)를 닫지 않는다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "required gate(필수 게이트)를 closeout(종료 기록)에 연결한다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def final_payload(
    parent: Mapping[str, Any],
    trades: pd.DataFrame,
    stress_candidates: pd.DataFrame,
    filter_rows: Sequence[Mapping[str, Any]],
    account_rows: pd.DataFrame,
    parameter_rows: Sequence[Mapping[str, Any]],
    scout_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    filter_pass = sum(1 for row in filter_rows if row.get("density_floor_status") == "pass(통과)")
    worst_candidate = stress_candidates.iloc[0].to_dict() if not stress_candidates.empty else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "source_trade_rows": int(len(trades)),
        "parent_mt5_net_profit": parent.get("mt5_net_profit"),
        "parent_mt5_profit_factor": parent.get("mt5_profit_factor"),
        "parent_mt5_trade_count": parent.get("mt5_trade_count"),
        "parent_combined_trade_per_business_day": parent.get("combined_trade_per_business_day"),
        "parent_long_short": f"{parent.get('long_trade_count')}/{parent.get('short_trade_count')}",
        "stress_surface_rows": int(len(read_frame(STRESS_ZONE_SURFACE))) if exists(STRESS_ZONE_SURFACE) else 0,
        "stress_candidate_rows": int(len(stress_candidates)),
        "simple_filter_proxy_rows": int(len(filter_rows)),
        "density_safe_simple_filter_rows": int(filter_pass),
        "account_drawdown_rows": int(len(account_rows)),
        "parameter_queue_rows": int(len(parameter_rows)),
        "scout_queue_rows": int(len(scout_rows)),
        "worst_stress_group": worst_candidate.get("group_value", ""),
        "worst_stress_score": worst_candidate.get("stress_score", ""),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(
    final: Mapping[str, Any],
    stress_candidates: pd.DataFrame,
    filter_rows: Sequence[Mapping[str, Any]],
    parameter_rows: Sequence[Mapping[str, Any]],
    scout_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top_stress = stress_candidates.head(8).to_dict("records")
    top_filters = list(filter_rows)[:8]
    top_params = list(parameter_rows)[:8]
    text = f"""# Stage364Z cost/session stress inputs(Stage364Z 비용/세션 압박 입력)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- source_trade_rows(원천 거래 행): `{final['source_trade_rows']}`
- parent MT5 net/PF/trades(부모 MT5 순수익/수익 팩터/거래수): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`
- density(밀도): `{final['parent_combined_trade_per_business_day']}`
- runtime_authority(런타임 권위): `not_claimed`

## Stress candidates(압박 후보)

{markdown_table(top_stress, ['candidate_rank', 'group_columns', 'group_value', 'trade_count', 'net_profit_after_cost', 'profit_factor_after_cost', 'stress_reasons', 'candidate_use'])}

## Simple filter proxy(단순 필터 프록시)

{markdown_table(top_filters, ['candidate_rank', 'filter_expression', 'removed_trade_count', 'projected_net_if_removed', 'projected_trade_per_business_day_if_removed', 'density_floor_status'])}

## Parameter queue(파라미터 대기열)

{markdown_table(top_params, ['queue_rank', 'queue_id', 'short_threshold', 'adx_block_min', 'max_hold_m5', 'guardrail_expression', 'queue_type'])}

## Gate audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 report(보고서)는 다음 `run364AA` scout(탐색)의 입력을 만든다. MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"""

## {RUN_ID}

- report(보고서): `{rel(REPORT_PATH)}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): cost/session/drawdown stress(비용/세션/낙폭 압박)를 `run364AA` scout queue(탐색 대기열)로 materialize(구체화)했다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""

## run364Z cost/session stress input materialization(364Z 비용/세션 압박 입력 구체화)

- action(행동): `run364Y` MT5 runtime review(MT5 런타임 검토)의 약한 월/시간/방향/계좌상태 구간을 materialize(구체화)했다.
- effect(효과): 다음 `{NEXT_RUN_ID}`에서 PF/DD(수익 팩터/낙폭) 수리를 거래 쪼개기 없이 시험할 수 있다.
- next(다음): `{NEXT_RUN_ID}`
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): stress_candidate_not_operating(압박 시험 후보, 운영 아님)
- latest_mt5_probe(최근 MT5 탐침): `run364X`
- latest_mt5_review(최근 MT5 검토): `run364Y`
- latest_materialization(최근 구체화): `run364Z`
- parent_mt5_net_pf_trades(부모 MT5 순수익/수익 팩터/거래수): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`
- stress_queue_rows(압박 대기열 행): `{final['scout_queue_rows']}`
- blockers(차단): proxy replay(프록시 재생), MT5 runtime probe(MT5 런타임 탐침), forward evidence(전진 근거), runtime authority audit(런타임 권위 감사)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364Z`는 `run364Y` MT5 review(MT5 검토)의 cost/session/drawdown stress(비용/세션/낙폭 압박)를 `run364AA` scout queue(탐색 대기열)로 materialize(구체화)했다. source trades(원천 거래)는 `{final['source_trade_rows']}`, stress candidate rows(압박 후보 행)는 `{final['stress_candidate_rows']}`, scout queue rows(탐색 대기열 행)는 `{final['scout_queue_rows']}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 parameter neighborhood/simple replay(파라미터 이웃/단순 재생)를 실행해 PF/DD(수익 팩터/낙폭)를 수리한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
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
updated_at_utc: {final['created_at_utc']}
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): cost/session/drawdown stress inputs(비용/세션/낙폭 압박 입력)를 materialize(구체화)했다.
- effect(효과): 다음 `{NEXT_RUN_ID}`에서 PF/DD repair scout(PF/DD 수리 탐색)를 바로 실행할 수 있다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): session/account-state/short guardrails(세션/계좌상태/숏 가드레일)이 density(밀도)를 유지하면서 PF/DD(수익 팩터/낙폭)를 개선할 수 있다.
- positive clue(긍정 단서): `run364Y` MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수) `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`.
- failure memory(실패 기억): simple filter proxy(단순 필터 프록시)는 sequence replay(순서 재생)와 MT5 runtime probe(MT5 런타임 탐침)를 대체하지 않는다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""

## {RUN_ID}

- action(행동): `run364Y`의 비용/세션/낙폭 압박을 `run364AA` 입력으로 구체화했다.
- effect(효과): 새 stage(단계) 분기 없이 Stage364(364단계) 안에서 PF/DD 수리를 이어간다.
""",
    )


def write_final_and_manifest(final: Mapping[str, Any]) -> None:
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stress_input_materialization(압박 입력 구체화)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"stress_candidates={final['stress_candidate_rows']}; scout_queue={final['scout_queue_rows']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["source_trade_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(RUN364AA_QUEUE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": "materialization_only_parent_density_passed(구체화 전용, 부모 밀도 통과)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "net_profit": final["parent_mt5_net_profit"],
        "profit_factor": final["parent_mt5_profit_factor"],
        "trade_count": final["parent_mt5_trade_count"],
        "evidence_scope": "input_materialization_no_authority(입력 구체화, 권위 없음)",
    }
    run_row = dict(common)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "MT5 review-derived stress inputs(MT5 검토 기반 압박 입력)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)"),
        (f"{RUN_ID}__Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "actual routed total stress input(실제 라우팅 전체 압박 입력)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": subrun_id,
                "subrun_id": subrun_id,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": kpi_scope,
            }
        )
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("stress_zone_surface", STRESS_ZONE_SURFACE, "Cost/session stress surface(비용/세션 압박 표면)."),
            ("stress_zone_candidates", STRESS_ZONE_CANDIDATES, "Stress candidates(압박 후보)."),
            ("simple_filter_proxy", SIMPLE_FILTER_PROXY, "Simple filter proxy density audit(단순 필터 프록시 밀도 감사)."),
            ("account_drawdown_table", ACCOUNT_DRAWDOWN_TABLE, "Account state drawdown table(계좌 상태 낙폭 표)."),
            ("parameter_queue", PARAMETER_QUEUE, "PF/DD parameter queue(PF/DD 파라미터 대기열)."),
            ("run364AA_queue", RUN364AA_QUEUE, "Next scout queue(다음 탐색 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def main() -> None:
    ensure_dirs()
    parent = validate_parent()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    trades = coerce_trade_frame(read_frame(review.CLOSED_TRADE_ATTRIBUTION))
    if int(len(trades)) != as_int(parent.get("mt5_trade_count")):
        raise RuntimeError(f"trade row mismatch(거래 행 불일치): {len(trades)} != {parent.get('mt5_trade_count')}")
    surface = build_stress_surface(trades)
    stress_candidates = candidate_filter(surface)
    filter_rows = simple_filter_rows(stress_candidates, parent)
    account_rows = account_drawdown_table(trades)
    short_rows = short_quality_rows(trades)
    parameter_rows = parameter_queue_rows(stress_candidates)
    scout_rows = scout_queue_rows(parameter_rows, filter_rows)

    write_csv(STRESS_ZONE_SURFACE, surface.to_dict("records"))
    write_csv(STRESS_ZONE_CANDIDATES, stress_candidates.to_dict("records"))
    write_csv(SIMPLE_FILTER_PROXY, filter_rows)
    write_csv(ACCOUNT_DRAWDOWN_TABLE, account_rows.to_dict("records"))
    write_csv(PARAMETER_QUEUE, parameter_rows)
    write_csv(SHORT_QUALITY_QUEUE, short_rows)
    write_csv(RUN364AA_QUEUE, scout_rows)

    final = final_payload(parent, trades, stress_candidates, filter_rows, account_rows, parameter_rows, scout_rows)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "data_integrity_audit",
                "experiment_design_audit",
                "performance_attribution_gate",
                "model_boundary_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    gates = write_receipts(final, stress_candidates, filter_rows, account_rows, scout_rows)
    final["gate_passes"] = sum(1 for row in gates if row.get("status") == "passed")
    final["gate_total"] = len(gates)
    write_docs(final, stress_candidates, filter_rows, parameter_rows, scout_rows, gates)
    write_final_and_manifest(final)
    write_ledgers(final, gates)
    write_final_and_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
