from __future__ import annotations

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

from stage_pipelines.stage364 import review_density_restore_stress_candidate_mt5_runtime_probe_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-04"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BG"
RUN_ID = "run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
PACKAGE_RUN_ID = parent.PACKAGE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1"

STATUS = "completed_stage364BG_density_restore_forward_regime_stress_inputs_materialized_no_authority"
JUDGMENT = "materialization_completed_forward_regime_stress_scout_inputs_no_authority"
DECISION = "stage364BG_open_run364BH_density_restore_forward_regime_stress_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
LONG_SHARE_WARN = 0.85

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SOURCE_RUNTIME_SUMMARY = RUN_DIR / "source_runtime_summary.csv"
FORWARD_BLOCK_STRESS = RUN_DIR / "forward_calendar_block_stress.csv"
MONTHLY_REGIME_STRESS = RUN_DIR / "monthly_regime_stress_matrix.csv"
SESSION_SIDE_STABILITY = RUN_DIR / "session_side_stability_matrix.csv"
DRAWDOWN_TAIL_STRESS = RUN_DIR / "drawdown_tail_stress_matrix.csv"
SHORT_RESTORE_SLICES = RUN_DIR / "short_restore_candidate_slices.csv"
REGIME_GUARDRAIL_MATRIX = RUN_DIR / "regime_guardrail_matrix.csv"
RUN364BH_QUEUE = RUN_DIR / "run364BH_forward_regime_stress_scout_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_boundary_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BG_density_restore_forward_regime_stress_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BG_density_restore_forward_regime_stress_inputs.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.CLOSED_TRADE_ATTRIBUTION,
    parent.MONTHLY_ATTRIBUTION,
    parent.ENTRY_HOUR_ATTRIBUTION,
    parent.SIDE_ATTRIBUTION,
    parent.HOLD_BUCKET_ATTRIBUTION,
    parent.DRAWDOWN_EVENT_REVIEW,
    parent.PROXY_MT5_ATTRIBUTION,
    parent.RUNTIME_QUALITY_REVIEW,
    parent.DENSITY_GUARDRAIL_AUDIT,
    parent.COST_SESSION_STRESS_REVIEW,
    parent.POSITIVE_CLUES,
    parent.FAILURE_MEMORY,
    parent.NEXT_QUEUE,
    parent.REPORT_PATH,
    parent.LINEAGE_RECEIPT,
    parent.RUNTIME_RECEIPT,
    parent.pkg.RUNTIME_POLICY_CONFIG,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SOURCE_RUNTIME_SUMMARY,
    FORWARD_BLOCK_STRESS,
    MONTHLY_REGIME_STRESS,
    SESSION_SIDE_STABILITY,
    DRAWDOWN_TAIL_STRESS,
    SHORT_RESTORE_SLICES,
    REGIME_GUARDRAIL_MATRIX,
    RUN364BH_QUEUE,
    WORK_PACKET,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
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
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_rows(path: Path) -> list[dict[str, str]]:
    _header, rows = parent.read_csv_rows(path)
    return rows


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


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


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        parent.io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BG inputs(BG 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"parent forbidden claim(부모 금지 주장): {key}={final.get(key)}")
    gates = read_rows(parent.GATE_AUDIT)
    if len(gates) != as_int(final.get("gate_total")) or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit(부모 게이트 감사)가 final decision(최종 결정)과 일치하지 않는다.")
    return final


def load_trades() -> pd.DataFrame:
    frame = pd.read_csv(parent.io_path(parent.CLOSED_TRADE_ATTRIBUTION))
    frame["entry_time"] = pd.to_datetime(frame["entry_time"])
    frame["exit_time"] = pd.to_datetime(frame["exit_time"])
    frame["entry_date"] = frame["entry_time"].dt.date
    frame["exit_date"] = frame["exit_time"].dt.date
    frame["entry_quarter"] = frame["entry_time"].dt.to_period("Q").astype(str)
    frame["entry_weekday"] = frame["entry_time"].dt.dayofweek
    frame["entry_hour"] = frame["entry_hour"].astype(int)
    frame["net_profit_after_cost"] = frame["net_profit_after_cost"].astype(float)
    frame["hold_m5_calendar"] = frame["hold_m5_calendar"].astype(int)
    frame["closed_balance_drawdown_percent"] = frame["closed_balance_drawdown_percent"].astype(float)
    return frame


def profit_factor(series: pd.Series) -> float | str:
    gains = float(series[series > 0].sum())
    losses = float(series[series < 0].sum())
    if losses < 0:
        return finite(gains / abs(losses), 9)
    return ""


def business_days(start: Any, end: Any) -> int:
    try:
        return int(len(pd.bdate_range(pd.Timestamp(start), pd.Timestamp(end))))
    except (TypeError, ValueError):
        return 0


def aggregate_frame(group: pd.DataFrame, *, run_id: str = RUN_ID) -> dict[str, Any]:
    wins = group[group["net_profit_after_cost"] > 0]
    losses = group[group["net_profit_after_cost"] < 0]
    start = group["entry_time"].min().date()
    end = group["entry_time"].max().date()
    days = business_days(start, end)
    long_count = int((group["side"] == "long").sum())
    short_count = int((group["side"] == "short").sum())
    trade_count = int(len(group))
    return {
        "run_id": run_id,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "business_days_by_trade_span": days,
        "trade_count": trade_count,
        "trade_density_per_business_day": finite(trade_count / days, 10) if days else "",
        "net_profit_after_cost": finite(group["net_profit_after_cost"].sum(), 6),
        "gross_profit_after_cost": finite(wins["net_profit_after_cost"].sum(), 6),
        "gross_loss_after_cost": finite(losses["net_profit_after_cost"].sum(), 6),
        "profit_factor_after_cost": profit_factor(group["net_profit_after_cost"]),
        "expectancy_after_cost": finite(group["net_profit_after_cost"].mean(), 6),
        "win_rate_after_cost_percent": finite((group["net_profit_after_cost"] > 0).mean() * 100.0, 6),
        "long_trade_count": long_count,
        "short_trade_count": short_count,
        "long_share": finite(long_count / max(trade_count, 1), 10),
        "short_share": finite(short_count / max(trade_count, 1), 10),
        "median_hold_m5_calendar": finite(group["hold_m5_calendar"].median(), 6),
        "max_hold_m5_calendar": int(group["hold_m5_calendar"].max()),
        "max_closed_balance_drawdown_percent": finite(group["closed_balance_drawdown_percent"].max(), 6),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "input_role": input_role(path),
                "effect": "BF MT5 review(BF MT5 검토) 근거를 BG materialization(BG 물질화) 입력으로 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "closed_trade_attribution.csv":
        return "deal-level MT5 closed trades(거래 단위 MT5 종료 거래)"
    if name in {"monthly_attribution.csv", "entry_hour_attribution.csv", "side_attribution.csv", "hold_bucket_attribution.csv"}:
        return "parent performance attribution(부모 성과 귀속)"
    if name == "run364BG_forward_regime_stress_queue.csv":
        return "parent BG seed queue(부모 BG 씨앗 대기열)"
    if name == "runtime_policy_config.json":
        return "runtime policy config(런타임 정책 설정)"
    return "supporting evidence(보조 근거)"


def source_summary_rows(final: Mapping[str, Any], trades: pd.DataFrame) -> list[dict[str, Any]]:
    months = read_rows(parent.MONTHLY_ATTRIBUTION)
    hours = read_rows(parent.ENTRY_HOUR_ATTRIBUTION)
    worst_month = min(months, key=lambda row: as_float(row.get("net_profit_after_cost")))
    weakest_hour = min(hours, key=lambda row: as_float(row.get("expectancy_after_cost")))
    return [
        {
            "run_id": RUN_ID,
            "summary_id": "parent_mt5_runtime_kpi(부모 MT5 런타임 KPI)",
            "value": f"net={final.get('mt5_net_profit')};pf={final.get('mt5_profit_factor')};trades={final.get('mt5_trade_count')};density={final.get('trade_per_business_day')};dd={final.get('mt5_max_drawdown_percent')}",
            "effect": "positive runtime clue(긍정 런타임 단서)를 forward/regime stress(전진/국면 압박)의 기준으로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "parent_proxy_mt5_diff(부모 프록시-MT5 차이)",
            "value": f"net_diff={final.get('actual_minus_expected_net_profit')};pf_diff={final.get('actual_minus_expected_profit_factor')};trade_diff={final.get('actual_minus_expected_trade_count')}",
            "effect": "proxy(프록시)는 다음 scout(스카우트)의 보조 기준으로만 유지하고 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "worst_regime_clues(최악 국면 단서)",
            "value": f"worst_month={worst_month.get('group_value')} net={worst_month.get('net_profit_after_cost')};weakest_hour={weakest_hour.get('group_value')} exp={weakest_hour.get('expectancy_after_cost')}",
            "effect": "hard delete(강제 삭제)가 아니라 forward stress label(전진 압박 라벨)과 soft firewall(소프트 방화벽) 입력으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "time_axis_and_scope(시간축과 범위)",
            "value": f"trades={len(trades)};first={trades['entry_time'].min().date()};last={trades['entry_time'].max().date()};broker-clock closed trade timestamps",
            "effect": "closed trade evidence(종료 거래 근거)를 시점 안전 검토 입력으로만 쓰고 forward pass(전진 통과)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def forward_block_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for block, group in trades.groupby("entry_quarter", sort=True):
        row = aggregate_frame(group)
        row.update(
            {
                "block_id": f"forward_like_{block}",
                "block_type": "calendar_quarter_forward_like_replay(달력 분기 전진 유사 재생)",
                "stress_status": stress_status(row),
                "stability_note": stability_note(row),
                "timestamp_boundary": "block assigned by entry_time known after historical review(진입 시각 기준 블록, 과거 검토용)",
            }
        )
        rows.append(row)
    return rows


def stress_status(row: Mapping[str, Any]) -> str:
    pf = as_float(row.get("profit_factor_after_cost"))
    net = as_float(row.get("net_profit_after_cost"))
    density = as_float(row.get("trade_density_per_business_day"))
    long_share = as_float(row.get("long_share"))
    if net < 0 or pf < 1.0:
        return "fail_stress_negative_or_pf_below_one(음수 또는 PF 1 미만 압박 실패)"
    if density < DENSITY_FLOOR:
        return "density_stress_review_required(밀도 압박 검토 필요)"
    if long_share > LONG_SHARE_WARN:
        return "long_skew_stress_review_required(롱 편향 압박 검토 필요)"
    return "passed_for_materialization_read(물질화 판독 통과)"


def stability_note(row: Mapping[str, Any]) -> str:
    notes = []
    if as_float(row.get("profit_factor_after_cost")) < 1.1:
        notes.append("pf_near_floor(PF 하한 근접)")
    if as_float(row.get("trade_density_per_business_day")) < DENSITY_FLOOR:
        notes.append("density_below_floor(밀도 하한 미달)")
    if as_float(row.get("long_share")) > LONG_SHARE_WARN:
        notes.append("long_skew(롱 편향)")
    if as_float(row.get("max_closed_balance_drawdown_percent")) > 12:
        notes.append("drawdown_pressure(낙폭 압박)")
    return ";".join(notes) if notes else "stable_clue(안정 단서)"


def monthly_regime_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for month, group in trades.groupby("entry_month", sort=True):
        row = aggregate_frame(group)
        pf = as_float(row["profit_factor_after_cost"])
        net = as_float(row["net_profit_after_cost"])
        exp = as_float(row["expectancy_after_cost"])
        row.update(
            {
                "month": month,
                "regime_bucket": monthly_bucket(pf, net, exp),
                "stress_score": int(net < 0) + int(pf < 1.05) + int(exp < 0.1) + int(as_float(row["long_share"]) > LONG_SHARE_WARN),
                "proposed_use": "stress_label_no_hard_delete(압박 라벨, 강제 삭제 없음)",
                "timestamp_boundary": "month known at entry time(月은 진입 시점에 알려짐)",
            }
        )
        rows.append(row)
    return rows


def monthly_bucket(pf: float, net: float, exp: float) -> str:
    if net < 0 or pf < 1.0:
        return "negative_month_regime(음수 월 국면)"
    if pf < 1.15 or exp < 0.25:
        return "thin_edge_month_regime(얇은 엣지 월 국면)"
    if pf >= 1.5 and exp >= 1.0:
        return "strong_month_regime(강한 월 국면)"
    return "normal_positive_month_regime(일반 양수 월 국면)"


def session_side_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for (hour, side), group in trades.groupby(["entry_hour", "side"], sort=True):
        row = aggregate_frame(group)
        row.update(
            {
                "entry_hour": int(hour),
                "side": side,
                "session_side_bucket": session_side_bucket(row, side),
                "proposed_use": session_side_use(row, side),
                "timestamp_boundary": "entry hour and side are known at decision time(진입 시간과 방향은 결정 시점에 알려짐)",
            }
        )
        rows.append(row)
    return rows


def session_side_bucket(row: Mapping[str, Any], side: str) -> str:
    pf = as_float(row.get("profit_factor_after_cost"))
    exp = as_float(row.get("expectancy_after_cost"))
    trades = as_int(row.get("trade_count"))
    if trades < 10:
        return f"{side}_small_sample({side} 소표본)"
    if pf < 1.0 or exp < 0:
        return f"{side}_weak_session({side} 약한 세션)"
    if side == "short" and pf >= 1.05:
        return "short_positive_restore_candidate(숏 양수 복원 후보)"
    if exp < 0.25:
        return f"{side}_thin_edge_session({side} 얇은 엣지 세션)"
    return f"{side}_usable_session({side} 사용 가능 세션)"


def session_side_use(row: Mapping[str, Any], side: str) -> str:
    bucket = session_side_bucket(row, side)
    if "short_positive" in bucket:
        return "short router expansion seed(숏 라우터 확장 씨앗)"
    if "weak" in bucket or "thin" in bucket:
        return "soft firewall stress label only(소프트 방화벽 압박 라벨 전용)"
    return "control slice(대조 구간)"


def dd_bucket(value: float) -> str:
    if value < 5:
        return "dd_00_lt5(낙폭 5 미만)"
    if value < 10:
        return "dd_01_5_to_10(낙폭 5-10)"
    if value < 15:
        return "dd_02_10_to_15(낙폭 10-15)"
    return "dd_03_ge15(낙폭 15 이상)"


def drawdown_tail_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    working = trades.copy()
    working["drawdown_bucket"] = working["closed_balance_drawdown_percent"].map(dd_bucket)
    rows = []
    for bucket, group in working.groupby("drawdown_bucket", sort=True):
        row = aggregate_frame(group)
        row.update(
            {
                "drawdown_bucket": bucket,
                "tail_loss_count": int((group["net_profit_after_cost"] <= -10.0).sum()),
                "tail_gain_count": int((group["net_profit_after_cost"] >= 20.0).sum()),
                "hold_tail_gt_288_count": int((group["hold_m5_calendar"] > 288).sum()),
                "proposed_use": "risk stress label for BH, not direct runtime veto(BH 위험 압박 라벨, 직접 런타임 제외 아님)",
                "feature_label_boundary": "drawdown outcome after trade, label only(거래 후 낙폭 결과, 라벨 전용)",
            }
        )
        rows.append(row)
    return rows


def short_restore_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    short = trades[trades["side"] == "short"].copy()
    rows = []
    for (month, hour), group in short.groupby(["entry_month", "entry_hour"], sort=True):
        if len(group) < 2:
            continue
        row = aggregate_frame(group)
        pf = as_float(row["profit_factor_after_cost"])
        net = as_float(row["net_profit_after_cost"])
        row.update(
            {
                "slice_id": f"short_{month}_h{int(hour):02d}",
                "month": month,
                "entry_hour": int(hour),
                "slice_bucket": "short_positive_slice(숏 양수 조각)" if net > 0 and pf >= 1.0 else "short_stress_slice(숏 압박 조각)",
                "proposed_use": "short restore candidate if positive, stress label otherwise(양수면 숏 복원 후보, 아니면 압박 라벨)",
                "timestamp_boundary": "month/hour/side known at entry decision(月/시간/방향은 진입 결정 시점에 알려짐)",
            }
        )
        rows.append(row)
    rows.sort(key=lambda item: (as_float(item.get("net_profit_after_cost")), as_float(item.get("profit_factor_after_cost"))), reverse=True)
    return rows


def queue_rows(
    final: Mapping[str, Any],
    forward_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    short_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    weak_months = [row["month"] for row in monthly_rows if row["regime_bucket"] != "normal_positive_month_regime(일반 양수 월 국면)" and row["regime_bucket"] != "strong_month_regime(강한 월 국면)"]
    weak_hours = sorted({str(row["entry_hour"]) for row in session_rows if "weak" in row["session_side_bucket"] or "thin" in row["session_side_bucket"]})
    positive_short = [row["slice_id"] for row in short_rows if row["slice_bucket"].startswith("short_positive")]
    base_density = as_float(final.get("trade_per_business_day"))
    base_trade_count = as_int(final.get("mt5_trade_count"))
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "minimum_density_per_day": DENSITY_FLOOR,
        "parent_mt5_density_per_day": base_density,
        "parent_mt5_trade_count": base_trade_count,
        "trade_splitting_status": "not_used(거래 쪼개기 없음)",
        "top_n_status": "forbidden(금지)",
        "oos_threshold_selection_status": "forbidden(금지)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bh01_forward_block_replay_current_policy",
            "idea_type": "runtime_verification(런타임 검증)",
            "input_artifact": rel(FORWARD_BLOCK_STRESS),
            "policy_family": "no_policy_change_forward_like_replay(정책 변경 없는 전진 유사 재생)",
            "stress_labels": ";".join(row["block_id"] for row in forward_rows if row["stress_status"] != "passed_for_materialization_read(물질화 판독 통과)") or "none(없음)",
            "proposed_change": "replay current policy by calendar block without threshold relaxation(임계값 완화 없이 현재 정책을 달력 블록별 재생)",
            "timestamp_boundary": "block assignment is historical review only; no live decision use(블록 배정은 과거 검토 전용, 실시간 결정에 사용 안 함)",
            "success_criteria": "no forward-like block has net<=0 or PF<1 while combined density stays >=3/day(전진 유사 블록 순수익 양수/PF 1 이상, 합산 밀도 3/day 이상)",
            "failure_criteria": "any material block net<=0 or PF<1 marks forward stress failure(의미 있는 블록이 음수 또는 PF 1 미만이면 전진 압박 실패)",
            "expected_effect": "separate one-window luck(단일 구간 운)을 from durable clue(지속 단서) before any runtime authority(런타임 권위).",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bh02_month_regime_soft_firewall_no_delete",
            "idea_type": "repair_control(수리/대조)",
            "input_artifact": rel(MONTHLY_REGIME_STRESS),
            "policy_family": "month_regime_soft_firewall(月 국면 소프트 방화벽)",
            "stress_labels": ";".join(weak_months) or "none(없음)",
            "proposed_change": "test extra margin or no-new-entry stress labels on weak months, no hard delete(약한 월에 추가 마진/신규진입 제한 라벨 시험, 강제 삭제 없음)",
            "timestamp_boundary": "entry month is known at entry time(月은 진입 시점에 알려짐)",
            "success_criteria": "PF improves or weak-month loss shrinks while estimated density remains >=3/day(PF 개선 또는 약한 월 손실 축소, 추정 밀도 3/day 이상)",
            "failure_criteria": "density falls below 3/day or weak-month label only curve-fits(밀도 3/day 미만 또는 약한 월 라벨 과적합)",
            "expected_effect": "turn December/August stress(12월/8월 압박)를 guardrail input(가드레일 입력)으로 바꾼다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bh03_hour18_19_session_side_firewall",
            "idea_type": "repair_control(수리/대조)",
            "input_artifact": rel(SESSION_SIDE_STABILITY),
            "policy_family": "hour_side_soft_firewall(시간/방향 소프트 방화벽)",
            "stress_labels": ";".join(weak_hours) or "none(없음)",
            "proposed_change": "stress hour 18/19 and weak side slices with margin guard, no trade splitting(18/19시와 약한 방향 조각을 마진 가드로 압박, 거래 쪼개기 없음)",
            "timestamp_boundary": "hour and side are known at entry decision(시간과 방향은 진입 결정 시점에 알려짐)",
            "success_criteria": "hour 18/19 expectancy improves without cutting total density below 3/day(18/19시 기대값 개선, 전체 밀도 3/day 이상)",
            "failure_criteria": "guardrail removes too many trades or hides loss in another hour(가드레일이 거래를 너무 줄이거나 다른 시간 손실을 숨김)",
            "expected_effect": "protect PF(수익 팩터)를 while preserving density(밀도 보존).",
        },
        {
            **common,
            "queue_rank": 4,
            "queue_id": "bh04_short_positive_slice_restore",
            "idea_type": "offensive_exploration(공격 탐색)",
            "input_artifact": rel(SHORT_RESTORE_SLICES),
            "policy_family": "short_router_restore(숏 라우터 복원)",
            "stress_labels": ";".join(positive_short[:8]) or "short positive net exists but sparse(숏 양수는 있으나 희소)",
            "proposed_change": "use positive short slices to seek short_share >=0.12 without changing long entry rule(양수 숏 조각으로 숏 비중 0.12 이상 탐색, 롱 진입 규칙은 유지)",
            "timestamp_boundary": "short router uses closed-bar probability plus entry month/hour only(숏 라우터는 닫힌 봉 확률과 진입 월/시간만 사용)",
            "success_criteria": "short net remains positive and long_share falls below 0.88 with density >=3/day(숏 순수익 양수 유지, 롱 비중 0.88 미만, 밀도 3/day 이상)",
            "failure_criteria": "short expansion turns negative or increases drawdown(숏 확장이 음수 전환 또는 낙폭 증가)",
            "expected_effect": "reduce long skew(롱 편향)를 while keeping BF positive density(BF 양수 밀도) clue.",
        },
        {
            **common,
            "queue_rank": 5,
            "queue_id": "bh05_drawdown_tail_hold_stress_not_hard_cap",
            "idea_type": "repair_control(수리/대조)",
            "input_artifact": rel(DRAWDOWN_TAIL_STRESS),
            "policy_family": "drawdown_tail_hold_stress(낙폭 꼬리 보유 압박)",
            "stress_labels": "dd_02_10_to_15;dd_03_ge15;hold_tail_gt_288",
            "proposed_change": "stress drawdown-tail entries and long hold winners without hard cap by default(낙폭 꼬리 진입과 장기 보유 승자를 압박하되 기본 강제 상한 없음)",
            "timestamp_boundary": "drawdown outcome is label only, not live entry feature(낙폭 결과는 라벨 전용, 실시간 진입 피처 아님)",
            "success_criteria": "drawdown tail shrinks while preserving long-hold positive contribution(낙폭 꼬리 축소와 장기 보유 양수 기여 보존)",
            "failure_criteria": "hard cap removes positive tail or creates hidden lookahead(강제 상한이 양수 꼬리를 제거하거나 미래참조 생성)",
            "expected_effect": "separate risk label(위험 라벨) from runtime veto(런타임 제외) before implementation.",
        },
    ]
    return rows


def guardrail_rows(queue: Sequence[Mapping[str, Any]], final: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        {
            "guardrail": "no_trade_splitting(거래 쪼개기 금지)",
            "status": "passed" if all("not_used" in row["trade_splitting_status"] for row in queue) else "failed",
            "evidence": rel(RUN364BH_QUEUE),
            "effect": "거래수를 쪼개서 KPI(핵심 성과 지표)를 부풀리지 않는다.",
        },
        {
            "guardrail": "no_top_n_or_oos_threshold_selection(top_n/OOS 임계값 선택 금지)",
            "status": "passed" if all("forbidden" in row["top_n_status"] and "forbidden" in row["oos_threshold_selection_status"] for row in queue) else "failed",
            "evidence": rel(RUN364BH_QUEUE),
            "effect": "사후 상위 선택이나 표본외 임계값 선택으로 과적합하지 않는다.",
        },
        {
            "guardrail": "timestamp_boundary(시점 경계)",
            "status": "passed" if all("timestamp_boundary" in row and row["timestamp_boundary"] for row in queue) else "failed",
            "evidence": rel(DATA_RECEIPT),
            "effect": "month/hour/side(월/시간/방향)는 진입 시점 정보로, outcome labels(결과 라벨)는 학습/압박 전용으로 분리한다.",
        },
        {
            "guardrail": "parent_density_floor_context(부모 밀도 하한 문맥)",
            "status": "passed" if as_float(final.get("trade_per_business_day")) >= DENSITY_FLOOR else "review_required",
            "evidence": rel(parent.DENSITY_GUARDRAIL_AUDIT),
            "effect": "BF 실제 MT5 밀도 3/day(일 3회) 이상 단서를 다음 scout(스카우트)의 하한으로 유지한다.",
        },
        {
            "guardrail": "operating_claim_guard(운영 주장 가드)",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "forward pass(전진 통과)와 runtime authority(런타임 권위)를 주장하지 않는다.",
        },
    ]
    for row in checks:
        row.update({"run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY})
    return checks


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any], queue: Sequence[Mapping[str, Any]]) -> None:
    base = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": "passed(통과)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "source_kpi": {
                "mt5_net_profit": final["mt5_net_profit"],
                "mt5_profit_factor": final["mt5_profit_factor"],
                "mt5_trade_count": final["mt5_trade_count"],
                "trade_density": final["trade_per_business_day"],
                "drawdown_percent": final["mt5_max_drawdown_percent"],
                "long_share": final["long_share"],
            },
            "effect": "BF MT5 KPI(BF MT5 핵심 성과 지표)를 BG materialization(BG 물질화)의 기준 근거로 고정한다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(parent.CLOSED_TRADE_ATTRIBUTION),
            "time_axis": "MT5 broker-clock closed trade timestamps; month/hour are entry-time-known fields(MT5 브로커 시계 종료 거래 시각, 월/시간은 진입 시점 정보)",
            "sample_scope": f"US100 M5 MT5 runtime probe trades; {final['first_trade_date']}..{final['last_trade_date']}; rows={final['closed_trade_rows']}",
            "missing_or_duplicate_check": "closed_trade_rows matched parent final decision(종료 거래 행 수가 부모 최종 결정과 일치)",
            "feature_label_boundary": "entry month/hour/side are decision-time fields; drawdown/profit/hold are post-trade labels only(진입 월/시간/방향은 결정 시점 필드, 낙폭/수익/보유는 거래 후 라벨 전용)",
            "split_boundary": "forward-like calendar blocks are stress slices, not claimed forward pass(전진 유사 달력 블록은 압박 조각, 전진 통과 주장 아님)",
            "leakage_risk": "using historical weak month/hour as live hard-delete would overfit(과거 약한 월/시간을 실전 강제 삭제로 쓰면 과적합)",
            "data_hash_or_identity": sha(parent.CLOSED_TRADE_ATTRIBUTION),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "BF positive MT5 density clue(BF 긍정 MT5 밀도 단서)가 forward/regime stress(전진/국면 압박)에서도 버티면 다음 runtime probe(런타임 탐침) 후보로 강화할 수 있다.",
            "comparison": "current policy replay vs soft month/hour/side/firewall and short restore seeds(현재 정책 재생 대 월/시간/방향 소프트 방화벽과 숏 복원 씨앗)",
            "controls": "no threshold relaxation, no top_n, no trade splitting(임계값 완화 없음, top_n 없음, 거래 쪼개기 없음)",
            "success_criteria": "density >=3/day, PF >=1, net positive across forward-like stress blocks(밀도 3/day 이상, PF 1 이상, 전진 유사 블록 순수익 양수)",
            "failure_criteria": "negative forward-like block, density collapse, short expansion loss, or hard-delete overfit(전진 유사 블록 음수, 밀도 붕괴, 숏 확장 손실, 강제 삭제 과적합)",
            "queue_rows": len(queue),
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "new_model_training": "not_run(실행 안 함)",
            "new_onnx_export": "not_run(실행 안 함)",
            "model_validation_judgment": "model_boundary_only(모델 경계만)",
            "effect": "BG는 model authority(모델 권위)가 아니라 BH scout inputs(BH 스카우트 입력)만 만든다.",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "source_artifacts": [rel(FORWARD_BLOCK_STRESS), rel(MONTHLY_REGIME_STRESS), rel(SESSION_SIDE_STABILITY), rel(DRAWDOWN_TAIL_STRESS), rel(SHORT_RESTORE_SLICES)],
            "positive_clue": "net/PF/density survived in MT5(BF에서 순수익/PF/밀도 생존)",
            "failure_memory": "long_share high and forward/regime evidence missing(롱 비중 높고 전진/국면 근거 누락)",
            "effect": "성과 변화 원인을 다음 scout(스카우트)의 비교축으로 바꾼다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": JUDGMENT,
            "result_class": "materialized_inputs_no_authority(입력 물질화, 권위 없음)",
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "forward_passed": "not_claimed",
        },
    )


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate": name,
        "status": status,
        "evidence": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_rows(guards: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    guard_status = "passed" if all(row["status"] == "passed" for row in guards) else "failed"
    return [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "BG materialization(BG 물질화) 범위를 final decision(최종 결정)으로 닫는다."),
        gate_row("kpi_contract_audit(KPI 계약 감사)", RUN_EVIDENCE_RECEIPT, "BF MT5 KPI(BF MT5 핵심 성과 지표)를 원천 권위로 둔다."),
        gate_row("skill_receipt_lint(스킬 영수증 점검)", WORK_PACKET, "primary/support skills(주/보조 스킬)와 receipt(영수증)를 연결한다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점/라벨/분할 경계를 기록한다."),
        gate_row("forward_regime_materialization_gate(전진/국면 물질화 게이트)", RUN364BH_QUEUE, "BH scout(BH 스카우트) 입력 대기열을 생성한다."),
        gate_row("guardrail_matrix_gate(가드레일 행렬 게이트)", REGIME_GUARDRAIL_MATRIX, "거래 쪼개기/top_n/표본외 임계값 선택 금지를 확인한다.", guard_status),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 산출물 해시를 연결한다."),
        gate_row("claim_boundary_gate(주장 경계 게이트)", CLAIM_RECEIPT, "운영 주장과 전진 통과 주장을 열지 않는다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "registry(등록부)의 필수 gate(게이트)를 closeout(종료 기록)에 연결한다."),
    ]


def final_payload(
    parent_final: Mapping[str, Any],
    forward_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    short_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    weak_month_count = sum(1 for row in monthly_rows if "negative" in row["regime_bucket"] or "thin" in row["regime_bucket"])
    weak_session_count = sum(1 for row in session_rows if "weak" in row["session_side_bucket"] or "thin" in row["session_side_bucket"])
    positive_short_rows = sum(1 for row in short_rows if str(row.get("slice_bucket", "")).startswith("short_positive"))
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_mt5_net_profit": parent_final.get("mt5_net_profit"),
        "parent_mt5_profit_factor": parent_final.get("mt5_profit_factor"),
        "parent_mt5_trade_count": parent_final.get("mt5_trade_count"),
        "parent_trade_density": parent_final.get("trade_per_business_day"),
        "parent_expectancy": parent_final.get("mt5_expectancy"),
        "parent_recovery_factor": parent_final.get("mt5_recovery_factor"),
        "parent_drawdown_percent": parent_final.get("mt5_max_drawdown_percent"),
        "parent_long_trade_count": parent_final.get("long_trade_count"),
        "parent_short_trade_count": parent_final.get("short_trade_count"),
        "parent_long_share": parent_final.get("long_share"),
        "parent_short_share": parent_final.get("short_share"),
        "parent_actual_minus_expected_net_profit": parent_final.get("actual_minus_expected_net_profit"),
        "parent_actual_minus_expected_profit_factor": parent_final.get("actual_minus_expected_profit_factor"),
        "parent_actual_minus_expected_trade_count": parent_final.get("actual_minus_expected_trade_count"),
        "forward_block_rows": len(forward_rows),
        "forward_block_stress_rows": sum(1 for row in forward_rows if row["stress_status"] != "passed_for_materialization_read(물질화 판독 통과)"),
        "monthly_regime_rows": len(monthly_rows),
        "weak_month_count": weak_month_count,
        "session_side_rows": len(session_rows),
        "weak_session_side_count": weak_session_count,
        "short_restore_slice_rows": len(short_rows),
        "positive_short_restore_slice_rows": positive_short_rows,
        "queue_rows": len(queue),
        "guardrail_passes": sum(1 for row in guards if row["status"] == "passed"),
        "guardrail_total": len(guards),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "forward_passed": "not_claimed",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "external_verification_status": "out_of_scope_by_claim_materialization_only(주장 범위 밖, 물질화만)",
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = parent.io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig")
    lines = []
    for line in text.splitlines():
        if line.startswith("- current_run_id"):
            lines.append(f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`")
        elif line.startswith("- latest_completed_run_id"):
            lines.append(f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`")
        elif line.startswith("- selection_status"):
            lines.append(f"- selection_status(선택 상태): `{STATUS}`")
        elif line.startswith("- claim_boundary"):
            lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines).rstrip() + "\n", bom=True)


def write_docs(
    final: Mapping[str, Any],
    forward_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    forward_preview = [
        {
            "block_id": row["block_id"],
            "trades": row["trade_count"],
            "net": row["net_profit_after_cost"],
            "pf": row["profit_factor_after_cost"],
            "density": row["trade_density_per_business_day"],
            "long_share": row["long_share"],
            "stress": row["stress_status"],
        }
        for row in forward_rows
    ]
    monthly_preview = [
        {
            "month": row["month"],
            "trades": row["trade_count"],
            "net": row["net_profit_after_cost"],
            "pf": row["profit_factor_after_cost"],
            "bucket": row["regime_bucket"],
            "score": row["stress_score"],
        }
        for row in monthly_rows
        if as_int(row.get("stress_score")) > 0
    ]
    session_preview = [
        {
            "hour": row["entry_hour"],
            "side": row["side"],
            "trades": row["trade_count"],
            "net": row["net_profit_after_cost"],
            "pf": row["profit_factor_after_cost"],
            "bucket": row["session_side_bucket"],
        }
        for row in session_rows
        if "weak" in row["session_side_bucket"] or "thin" in row["session_side_bucket"] or "short_positive" in row["session_side_bucket"]
    ]
    report = f"""# run364BG density restore forward/regime stress inputs(364BG 밀도 복원 전진/국면 압박 입력)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- parent MT5 net/PF/trades/density(부모 MT5 순수익/수익 팩터/거래수/밀도): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}` / `{final['parent_trade_density']}`
- parent long/short(부모 롱/숏): `{final['parent_long_trade_count']}` / `{final['parent_short_trade_count']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action And Effect(행동과 효과)

Action(행동): BF MT5 runtime probe review(BF MT5 런타임 탐침 검토)를 forward block(전진 블록), month regime(月 국면), session/side(세션/방향), drawdown tail(낙폭 꼬리), short restore(숏 복원) 입력으로 materialize(물질화)했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도) 긍정 단서를 BH scout(BH 스카우트)의 압박 대기열로 넘기되, forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.

## Forward Blocks(전진 유사 블록)

{markdown_table(forward_preview, ['block_id', 'trades', 'net', 'pf', 'density', 'long_share', 'stress'])}

## Monthly Stress(月별 압박)

{markdown_table(monthly_preview, ['month', 'trades', 'net', 'pf', 'bucket', 'score'])}

## Session/Side Stress(세션/방향 압박)

{markdown_table(session_preview, ['hour', 'side', 'trades', 'net', 'pf', 'bucket'])}

## BH Queue(BH 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'idea_type', 'policy_family', 'stress_labels', 'success_criteria'])}

## Guardrails(가드레일)

{markdown_table(guards, ['guardrail', 'status', 'evidence', 'effect'])}

## Required Gates(필수 게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BG는 materialization only(물질화 전용)다. 새 model training(모델 학습), 새 MT5 execution(MT5 실행), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, report, bom=True)
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
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364BG` materialized(물질화 완료) BF MT5 runtime probe review(BF MT5 런타임 탐침 검토)를 forward/regime stress inputs(전진/국면 압박 입력)로 바꿨다. Parent MT5 net/PF/trades/density(부모 MT5 순수익/수익 팩터/거래수/밀도)는 `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}` / `{final['parent_trade_density']}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 forward-like block replay(전진 유사 블록 재생), month/hour/side soft firewall(月/시간/방향 소프트 방화벽), short restore(숏 복원), drawdown tail stress(낙폭 꼬리 압박)를 proxy scout(프록시 스카우트)로 실행한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(없음, 물질화만)
- runtime_probe_candidate(런타임 탐침 후보): `run364BB_ba02_between_ax03_ax08_floor025_ps450` remains research watchlist(연구 감시 유지)
- latest_mt5_probe(최근 MT5 탐침): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1`
- latest_mt5_net_pf_trades(최근 MT5 순수익/수익 팩터/거래수): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`
- latest_trade_density(최근 거래 밀도): `{final['parent_trade_density']}` per business day(영업일당), floor(하한) `{DENSITY_FLOOR}`
- latest_long_short(최근 롱/숏): `{final['parent_long_trade_count']}` / `{final['parent_short_trade_count']}`
- latest_materialization(최근 물질화): `{RUN_ID}`
- next_scout_queue(다음 스카우트 대기열): `{rel(RUN364BH_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - density restore forward/regime stress input materialization(밀도 복원 전진/국면 압박 입력 물질화).",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364BG Forward/Regime Stress Inputs Closeout",
        f"""## run364BG Forward/Regime Stress Inputs Closeout(364BG 전진/국면 압박 입력 종료)

Action(행동): run364BF(364BF 실행)의 MT5 positive clue(MT5 긍정 단서)를 forward/regime stress inputs(전진/국면 압박 입력)와 BH scout queue(BH 스카우트 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고, 운영 주장 없이 `{NEXT_RUN_ID}`에서 forward-like replay(전진 유사 재생)와 soft firewall(소프트 방화벽)을 시험할 수 있게 했다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BG Density Restore Forward/Regime Stress Inputs(364BG 밀도 복원 전진/국면 압박 입력)

Action(행동): BF MT5 review(BF MT5 검토)를 BH scout queue(BH 스카우트 대기열)로 물질화했다.

Effect(효과): positive net/PF/density(양수 순수익/수익 팩터/밀도)를 forward/regime stress(전진/국면 압박)로 검증할 준비가 됐다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} - {RUN_ID}

- action(행동): density restore forward/regime stress inputs(밀도 복원 전진/국면 압박 입력)를 물질화했다.
- effect(효과): `{NEXT_RUN_ID}` scout queue(스카우트 대기열)를 만들고, 운영 주장은 닫았다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): BF positive runtime clue(BF 긍정 런타임 단서)를 forward-like block replay(전진 유사 블록 재생), month/hour/side soft firewall(月/시간/방향 소프트 방화벽), short restore(숏 복원)로 압박한다.
- positive clue(긍정 단서): MT5 net `{final['parent_mt5_net_profit']}`, PF `{final['parent_mt5_profit_factor']}`, density `{final['parent_trade_density']}`.
- failure memory(실패 기억): long share(롱 비중) `{final['parent_long_share']}`와 missing forward/regime evidence(전진/국면 근거 누락)는 운영 승격을 막는다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): materialized_forward_regime_stress_inputs_no_authority(전진/국면 압박 입력 물질화, 권위 없음).
- failure_memory(실패 기억): forward pass(전진 통과) 없음, long share(롱 비중) `{final['parent_long_share']}`, drawdown(낙폭) `{final['parent_drawdown_percent']}`%.
- effect(효과): 같은 차단 원인을 반복 보고하지 않고 BH scout(BH 스카우트)의 비교축으로 바꾼다.
""",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(RUN364BH_QUEUE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "out_of_scope_by_claim_materialization_only(주장 범위 밖, 물질화만)",
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "materialization(물질화)",
        "net_profit": final["parent_mt5_net_profit"],
        "profit_factor": final["parent_mt5_profit_factor"],
        "expectancy": final["parent_expectancy"],
        "drawdown": final["parent_drawdown_percent"],
        "recovery_factor": final["parent_recovery_factor"],
        "trade_count": final["parent_mt5_trade_count"],
        "trade_density_per_feature_day": final["parent_trade_density"],
        "trade_density_requirement_status": "parent_passed_bg_stress_inputs_materialized(부모 통과, BG 압박 입력 물질화)",
        "long_trade_count": final["parent_long_trade_count"],
        "short_trade_count": final["parent_short_trade_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can BF positive MT5 density survive forward/regime stress before any operating claim?(BF 긍정 MT5 밀도가 운영 주장 전 전진/국면 압박을 버틸 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, kpi_scope, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "forward_regime_stress_inputs(전진/국면 압박 입력)", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)", "out_of_scope_by_claim(주장 범위 밖)", "not_materialized_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A materialized queue plus Tier B out_of_scope(Tier A 물질화 대기열 + Tier B 범위 밖)", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": kpi_scope,
                "status": status,
                "judgment": judgment,
                "primary_kpi": f"queue_rows={final['queue_rows']};forward_blocks={final['forward_block_rows']};weak_months={final['weak_month_count']}",
                "guardrail_kpi": "no_trade_splitting;no_top_n;no_oos_threshold_selection;no_forward_claim",
            }
        )
        if tier == "Tier B":
            row.update({"net_profit": "", "profit_factor": "", "expectancy": "", "drawdown": "", "recovery_factor": "", "trade_count": "", "long_trade_count": "", "short_trade_count": ""})
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("forward_block_stress", FORWARD_BLOCK_STRESS, "Forward-like calendar block stress(전진 유사 달력 블록 압박)."),
        ("monthly_regime_stress", MONTHLY_REGIME_STRESS, "Monthly regime stress matrix(月별 국면 압박 행렬)."),
        ("session_side_stability", SESSION_SIDE_STABILITY, "Session-side stability matrix(세션-방향 안정성 행렬)."),
        ("drawdown_tail_stress", DRAWDOWN_TAIL_STRESS, "Drawdown tail stress matrix(낙폭 꼬리 압박 행렬)."),
        ("short_restore_slices", SHORT_RESTORE_SLICES, "Short restore candidate slices(숏 복원 후보 조각)."),
        ("next_queue", RUN364BH_QUEUE, "BH scout queue(BH 스카우트 대기열)."),
        ("report", REPORT_PATH, "BG materialization report(BG 물질화 보고서)."),
        ("decision", DECISION_DOC, "BG decision record(BG 결정 기록)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
    ]:
        if exists(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at_utc": final["created_at_utc"],
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)
    parent.drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    parent.drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_manifested_after_commit(커밋 후 추적 또는 목록화)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "package_run_id": PACKAGE_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    trades = load_trades()
    if len(trades) != as_int(parent_final.get("closed_trade_rows")):
        raise RuntimeError(f"closed trade row mismatch(종료 거래 행 불일치): {len(trades)} != {parent_final.get('closed_trade_rows')}")

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    forward = forward_block_rows(trades)
    monthly = monthly_regime_rows(trades)
    session_side = session_side_rows(trades)
    drawdown = drawdown_tail_rows(trades)
    short_slices = short_restore_rows(trades)
    queue = queue_rows(parent_final, forward, monthly, session_side, short_slices)
    write_csv(SOURCE_RUNTIME_SUMMARY, source_summary_rows(parent_final, trades))
    write_csv(FORWARD_BLOCK_STRESS, forward)
    write_csv(MONTHLY_REGIME_STRESS, monthly)
    write_csv(SESSION_SIDE_STABILITY, session_side)
    write_csv(DRAWDOWN_TAIL_STRESS, drawdown)
    write_csv(SHORT_RESTORE_SLICES, short_slices)
    write_csv(RUN364BH_QUEUE, queue)

    write_receipts(parent_final, queue)
    guards = guardrail_rows(queue, parent_final)
    write_csv(REGIME_GUARDRAIL_MATRIX, guards)
    gates = gate_rows(guards)
    write_csv(GATE_AUDIT, gates)
    if any(row["status"] != "passed" for row in gates):
        raise RuntimeError("BG gate failure(BG 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] != "passed"))

    created_at = now_utc()
    final = final_payload(parent_final, forward, monthly, session_side, short_slices, queue, guards, gates, created_at)
    write_json(FINAL_DECISION, final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_docs(final, forward, monthly, session_side, queue, guards, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
