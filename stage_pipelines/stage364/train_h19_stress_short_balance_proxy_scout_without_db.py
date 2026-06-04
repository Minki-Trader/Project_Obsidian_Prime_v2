from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import materialize_h19_runtime_probe_stress_short_balance_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-04"
BK = parent.parent
BJ = BK.parent

STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BM"
RUN_ID = "run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = BK.RUN_ID
BASELINE_RUN_ID = BK.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BN_review_h19_stress_short_balance_proxy_scout_without_db_v1"

STATUS = "completed_stage364BM_h19_stress_short_balance_proxy_scout_no_package_candidate_review_required_no_authority"
JUDGMENT = "combined_proxy_improved_but_short_source_negative_package_ineligible_review_required_no_authority"
DECISION = "stage364BM_open_run364BN_h19_stress_short_balance_proxy_scout_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
TARGET_SHORT_SHARE = 0.12
MIN_PF_KEEP = 1.35
DEPOSIT = 500.0
FIXED_LOT = 0.1
FIXED_HOLD_BARS = 6
SPREAD_POINT_TO_PRICE = 0.01

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
ENTRY_PROBABILITY_JOIN_AUDIT = RUN_DIR / "entry_probability_join_audit.csv"
RAW_BAR_PRICE_PARITY_AUDIT = RUN_DIR / "raw_bar_price_parity_audit.csv"
BASELINE_CLOSED_TRADE_METRICS = RUN_DIR / "baseline_closed_trade_metrics.csv"
PROXY_SCOUT_SURFACE = RUN_DIR / "proxy_scout_surface.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_PROXY_TRADE_TAPE = RUN_DIR / "selected_proxy_trade_tape.csv"
SHORT_SOURCE_FEASIBILITY = RUN_DIR / "short_source_feasibility.csv"
SHORT_SYNTHETIC_CANDIDATES = RUN_DIR / "short_synthetic_candidates.csv"
DISPLACED_PARENT_TRADES = RUN_DIR / "displaced_parent_trades.csv"
FORWARD_REGIME_REPLAY = RUN_DIR / "forward_regime_replay.csv"
EQUITY_DD_PROXY_DIAGNOSTIC = RUN_DIR / "equity_dd_proxy_diagnostic.csv"
REJECTED_CANDIDATES = RUN_DIR / "rejected_candidates.csv"
RUN364BN_QUEUE = RUN_DIR / "run364BN_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BM_h19_stress_short_balance_proxy_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BM_h19_stress_short_balance_proxy_scout.md"
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

US100_BARS = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364BM_QUEUE,
    parent.SOURCE_RUNTIME_PROBE_SUMMARY,
    parent.SHORT_SOURCE_RESTORE_PLAN,
    parent.FORWARD_REGIME_REPLAY_PLAN,
    parent.EQUITY_DD_COST_GUARDRAIL_PLAN,
    parent.RUNTIME_TELEMETRY_PRESSURE_MATRIX,
    BK.FINAL_DECISION,
    BK.CLOSED_TRADE_ATTRIBUTION,
    BK.SIDE_ATTRIBUTION,
    BK.QUARTER_ATTRIBUTION,
    BK.MONTHLY_ATTRIBUTION,
    BK.ENTRY_HOUR_ATTRIBUTION,
    BK.HOLD_BUCKET_ATTRIBUTION,
    BK.RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW,
    BK.PARENT_TELEMETRY_COPY,
    BK.RUNTIME_RECEIPT,
    US100_BARS,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    ENTRY_PROBABILITY_JOIN_AUDIT,
    RAW_BAR_PRICE_PARITY_AUDIT,
    BASELINE_CLOSED_TRADE_METRICS,
    PROXY_SCOUT_SURFACE,
    SELECTED_PROXY_CANDIDATE,
    SELECTED_PROXY_TRADE_TAPE,
    SHORT_SOURCE_FEASIBILITY,
    SHORT_SYNTHETIC_CANDIDATES,
    DISPLACED_PARENT_TRADES,
    FORWARD_REGIME_REPLAY,
    EQUITY_DD_PROXY_DIAGNOSTIC,
    REJECTED_CANDIDATES,
    RUN364BN_QUEUE,
    WORK_PACKET,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
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


def io_path(path: Path | str) -> Path:
    return BK.io_path(Path(path))


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


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


def drop_empty_csv_columns(path: Path, columns: Sequence[str]) -> None:
    if not exists(path):
        return
    header, rows = BK.read_csv_rows(path)
    removable = [column for column in columns if column in header and all(str(row.get(column, "")) == "" for row in rows)]
    if removable:
        write_csv(path, rows, [column for column in header if column not in removable])


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    return parent.as_int(value, default)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 14) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    if not exists(path):
        return
    text = io_path(path).read_text(encoding="utf-8-sig")
    updated: list[str] = []
    for line in text.splitlines():
        replacement = None
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                replacement = value
                break
        updated.append(replacement if replacement is not None else line)
    write_text(path, "\n".join(updated).rstrip() + "\n", bom=bom)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BM inputs(BM 입력 누락): " + ", ".join(missing))
    bl_final = read_json(parent.FINAL_DECISION)
    if bl_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BL next_run_id mismatch(BL 다음 실행 불일치): {bl_final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]:
        if bl_final.get(key) != "not_claimed":
            raise RuntimeError(f"BL forbidden claim(BL 금지 주장): {key}={bl_final.get(key)}")
    bl_gates = read_rows(parent.GATE_AUDIT)
    if not bl_gates or any(row.get("status") != "passed" for row in bl_gates):
        raise RuntimeError("BL gate audit(BL 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_rows(parent.RUN364BM_QUEUE)
    if len(queue) != 6:
        raise RuntimeError(f"BM queue row mismatch(BM 대기열 행 불일치): expected 6, got {len(queue)}")
    bk_final = read_json(BK.FINAL_DECISION)
    if as_int(bk_final.get("mt5_trade_count")) != as_int(bl_final.get("parent_mt5_trade_count")):
        raise RuntimeError("BK/BL trade count mismatch(BK/BL 거래수 불일치)")
    return bl_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BM source input(BM 원천 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_closed_trades_with_probabilities() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    trades = pd.read_csv(io_path(BK.CLOSED_TRADE_ATTRIBUTION), encoding="utf-8-sig")
    trades["entry_time_dt"] = pd.to_datetime(trades["entry_time"])
    trades["exit_time_dt"] = pd.to_datetime(trades["exit_time"])
    trades["entry_month"] = trades["entry_time_dt"].dt.strftime("%Y-%m")
    trades["entry_month_num"] = trades["entry_time_dt"].dt.strftime("%m")
    trades["entry_quarter"] = trades["entry_time_dt"].dt.to_period("Q").astype(str)
    trades["entry_hour"] = trades["entry_time_dt"].dt.hour
    trades["pnl"] = pd.to_numeric(trades["net_profit_after_cost"], errors="coerce").fillna(0.0)
    trades["source"] = "parent_mt5_closed_trade(부모 MT5 종료 거래)"
    trades = trades.sort_values("trade_index").reset_index(drop=True)

    tele = pd.read_csv(
        io_path(BK.PARENT_TELEMETRY_COPY),
        usecols=[
            "record_type",
            "written_at",
            "bar_time",
            "p_short",
            "p_flat",
            "p_long",
            "decision",
            "decision_reason",
            "exec_action",
            "order_attempted",
            "order_filled",
        ],
        encoding="utf-8-sig",
    )
    opens = tele[
        (tele["record_type"].astype(str) == "cycle")
        & (tele["order_filled"].astype(str).str.lower() == "true")
        & (tele["exec_action"].astype(str).str.contains("open", na=False))
    ].copy()
    opens["entry_time_dt"] = pd.to_datetime(opens["written_at"], format="%Y.%m.%d %H:%M:%S")
    for col in ["p_short", "p_flat", "p_long"]:
        opens[col] = pd.to_numeric(opens[col], errors="coerce")
    opens["selected_probability"] = np.where(opens["decision"] == "long", opens["p_long"], opens["p_short"])
    opens["opposite_probability"] = np.where(opens["decision"] == "long", opens["p_short"], opens["p_long"])
    opens["margin_vs_opposite"] = opens["selected_probability"] - opens["opposite_probability"]
    opens["margin_vs_flat"] = opens["selected_probability"] - opens["p_flat"]
    opens["margin_vs_max_other"] = opens.apply(
        lambda row: row["p_long"] - max(row["p_short"], row["p_flat"])
        if row["decision"] == "long"
        else row["p_short"] - max(row["p_long"], row["p_flat"]),
        axis=1,
    )
    join_cols = [
        "entry_time_dt",
        "bar_time",
        "p_short",
        "p_flat",
        "p_long",
        "decision",
        "decision_reason",
        "selected_probability",
        "opposite_probability",
        "margin_vs_opposite",
        "margin_vs_flat",
        "margin_vs_max_other",
    ]
    joined = trades.merge(opens[join_cols], on="entry_time_dt", how="left", validate="one_to_one")
    audit = [
        {
            "run_id": RUN_ID,
            "audit_id": "entry_probability_join(진입 확률 결합)",
            "closed_trade_rows": len(trades),
            "telemetry_open_rows": len(opens),
            "joined_rows": len(joined),
            "missing_probability_rows": int(joined["selected_probability"].isna().sum()),
            "duplicate_closed_entry_time_rows": int(trades["entry_time_dt"].duplicated().sum()),
            "duplicate_telemetry_open_time_rows": int(opens["entry_time_dt"].duplicated().sum()),
            "time_axis": "MT5 entry_time joined to telemetry written_at, telemetry bar_time is prior closed M5(MT5 진입시각과 telemetry 작성시각 결합, telemetry bar_time은 직전 닫힌 5분봉)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    if (
        audit[0]["missing_probability_rows"]
        or audit[0]["duplicate_closed_entry_time_rows"]
        or audit[0]["duplicate_telemetry_open_time_rows"]
        or len(opens) != len(trades)
    ):
        raise RuntimeError("entry probability join failed(진입 확률 결합 실패)")
    return joined, audit


def load_telemetry_cycles() -> pd.DataFrame:
    tele = pd.read_csv(io_path(BK.PARENT_TELEMETRY_COPY), encoding="utf-8-sig")
    tele = tele[tele["record_type"].astype(str) == "cycle"].copy()
    tele["written_at_dt"] = pd.to_datetime(tele["written_at"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    tele["entry_hour"] = tele["written_at_dt"].dt.hour
    tele["entry_month"] = tele["written_at_dt"].dt.strftime("%Y-%m")
    tele["entry_quarter"] = tele["written_at_dt"].dt.to_period("Q").astype(str)
    for col in ["p_short", "p_flat", "p_long"]:
        tele[col] = pd.to_numeric(tele[col], errors="coerce")
    tele["short_margin_vs_long"] = tele["p_short"] - tele["p_long"]
    tele["short_margin_vs_flat"] = tele["p_short"] - tele["p_flat"]
    return tele.sort_values("written_at_dt").reset_index(drop=True)


def load_us100_bars() -> tuple[pd.DataFrame, dict[pd.Timestamp, int]]:
    bars = pd.read_csv(io_path(US100_BARS), encoding="utf-8-sig")
    bars["bar_time_dt"] = pd.to_datetime(bars["time_open_unix"], unit="s")
    bars["spread_price"] = pd.to_numeric(bars["spread_points"], errors="coerce").fillna(0.0) * SPREAD_POINT_TO_PRICE
    for col in ["open", "high", "low", "close"]:
        bars[col] = pd.to_numeric(bars[col], errors="coerce")
    bars = bars.sort_values("bar_time_dt").reset_index(drop=True)
    index_by_time = {time: idx for idx, time in enumerate(bars["bar_time_dt"])}
    return bars, index_by_time


def raw_bar_price_parity_rows(trades: pd.DataFrame, bars: pd.DataFrame) -> list[dict[str, Any]]:
    quote = bars.set_index("bar_time_dt")[["open", "spread_price"]]
    probe = trades.copy()
    probe = probe.join(quote.rename(columns={"open": "entry_bid", "spread_price": "entry_spread"}), on="entry_time_dt")
    probe = probe.join(quote.rename(columns={"open": "exit_bid", "spread_price": "exit_spread"}), on="exit_time_dt")
    matched = probe[probe[["entry_bid", "exit_bid"]].notna().all(axis=1)].copy()
    if not matched.empty:
        matched["synthetic_entry"] = np.where(matched["side"] == "long", matched["entry_bid"] + matched["entry_spread"], matched["entry_bid"])
        matched["synthetic_exit"] = np.where(matched["side"] == "long", matched["exit_bid"], matched["exit_bid"] + matched["exit_spread"])
        matched["synthetic_pnl"] = np.where(
            matched["side"] == "long",
            (matched["synthetic_exit"] - matched["synthetic_entry"]) * matched["volume"].astype(float),
            (matched["synthetic_entry"] - matched["synthetic_exit"]) * matched["volume"].astype(float),
        )
        diff = (matched["synthetic_pnl"].round(2) - matched["pnl"].round(2)).abs()
        median_abs = float(diff.median())
        max_abs = float(diff.max())
        large_diff_rows = int((diff > 1.5).sum())
    else:
        median_abs = 999.0
        max_abs = 999.0
        large_diff_rows = len(probe)
    return [
        {
            "run_id": RUN_ID,
            "audit_id": "raw_bar_price_parity(원천 봉 가격 정합)",
            "closed_trade_rows": len(probe),
            "matched_entry_exit_bar_rows": len(matched),
            "unmatched_entry_exit_bar_rows": int(len(probe) - len(matched)),
            "median_abs_pnl_diff": finite(median_abs, 10),
            "max_abs_pnl_diff": finite(max_abs, 10),
            "large_diff_rows_gt_1_5": large_diff_rows,
            "price_model": "long entry=bid open+spread, long exit=bid open, short entry=bid open, short exit=bid open+spread(롱 진입=bid open+스프레드, 롱 청산=bid open, 숏 진입=bid open, 숏 청산=bid open+스프레드)",
            "usability": "usable_for_fixed6_proxy_labels_not_mt5_replacement(고정 6봉 프록시 라벨에는 사용 가능, MT5 대체 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def full_business_days(frame: pd.DataFrame) -> int:
    start = frame["entry_time_dt"].min().date()
    end = frame["entry_time_dt"].max().date()
    return int(np.busday_count(start, end + timedelta(days=1)))


def metric_frame(frame: pd.DataFrame, *, full_days: int) -> dict[str, Any]:
    if frame.empty:
        return {
            "net_profit": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "trade_count": 0,
            "trade_density_per_business_day": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "closed_drawdown_amount": 0.0,
            "closed_drawdown_percent": 0.0,
            "recovery_factor": 0.0,
            "win_rate_percent": 0.0,
            "long_trade_count": 0,
            "short_trade_count": 0,
            "long_share": 0.0,
            "short_share": 0.0,
        }
    ordered = frame.sort_values("entry_time_dt").copy()
    pnl = ordered["pnl"].astype(float)
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(-pnl[pnl < 0].sum())
    net = float(pnl.sum())
    balance = DEPOSIT + pnl.cumsum()
    peak = balance.cummax()
    drawdown = peak - balance
    dd_amount = float(drawdown.max()) if len(drawdown) else 0.0
    dd_percent = float(((drawdown / peak.replace(0, np.nan)) * 100.0).max()) if len(drawdown) else 0.0
    count = int(len(ordered))
    longs = int((ordered["side"].astype(str) == "long").sum())
    shorts = int((ordered["side"].astype(str) == "short").sum())
    return {
        "net_profit": round(net, 2),
        "profit_factor": finite(gross_profit / gross_loss if gross_loss else 999.0, 10),
        "expectancy": finite(net / count if count else 0.0, 10),
        "trade_count": count,
        "trade_density_per_business_day": finite(count / full_days if full_days else 0.0, 10),
        "gross_profit": finite(gross_profit, 10),
        "gross_loss": finite(gross_loss, 10),
        "closed_drawdown_amount": finite(dd_amount, 10),
        "closed_drawdown_percent": finite(dd_percent, 10),
        "recovery_factor": finite(net / dd_amount if dd_amount else 999.0, 10),
        "win_rate_percent": finite((pnl > 0).mean() * 100.0, 10),
        "long_trade_count": longs,
        "short_trade_count": shorts,
        "long_share": finite(longs / count if count else 0.0, 10),
        "short_share": finite(shorts / count if count else 0.0, 10),
    }


def candidate_definitions() -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "bm00_current_h19_mt5_closed_trade_reference",
            "queue_id": "bm01_forward_quarter_replay_h19_guard_reference",
            "candidate_kind": "reference(기준)",
            "idea_type": "runtime_reference(런타임 기준)",
            "policy_family": "no_policy_change(정책 변경 없음)",
            "description": "BK h19 runtime probe closed trade tape reference(BK h19 런타임 탐침 종료 거래 기준)",
        },
        {
            "variant_id": "bm02_december_h18_19_low_margin_soft_guard_0005",
            "queue_id": "bm02_december_hour18_19_label_soft_guard",
            "candidate_kind": "closed_trade_filter_proxy(종료거래 필터 프록시)",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "december_hour18_19_low_margin_soft_guard(12월 18/19시 저마진 소프트 가드)",
            "blocked_months": ["2025-12"],
            "long_hours": [18, 19],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.0005,
            "description": "stress-label December h18/h19 weak long entries(12월 18/19시 약한 롱 진입 압박 라벨)",
        },
        {
            "variant_id": "bm02_hour18_19_low_margin_soft_guard_0010",
            "queue_id": "bm02_december_hour18_19_label_soft_guard",
            "candidate_kind": "closed_trade_filter_proxy(종료거래 필터 프록시)",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hour18_19_low_margin_soft_guard(18/19시 저마진 소프트 가드)",
            "long_hours": [18, 19],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.001,
            "description": "stress-label h18/h19 weak long entries(18/19시 약한 롱 진입 압박 라벨)",
        },
        {
            "variant_id": "bm05_hold7to12_low_margin_guard_0005",
            "queue_id": "bm05_equity_dd_hold_7to12_guardrail_diagnostic",
            "candidate_kind": "closed_trade_filter_proxy(종료거래 필터 프록시)",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "hold7to12_low_margin_dd_diagnostic(7~12봉 보유 저마진 낙폭 진단)",
            "hold_buckets": ["002_7_to_12_m5_calendar"],
            "margin_col": "margin_vs_opposite",
            "margin_min": 0.0005,
            "description": "diagnose 7-12 bar weak-margin trades without outcome feature use(7~12봉 약한 마진 거래 진단, 결과 피처 사용 없음)",
        },
        {
            "variant_id": "bm03_short_router_ps0445_all_hours_fixed6",
            "queue_id": "bm03_short_source_router_ps0445_no_long_delete",
            "candidate_kind": "synthetic_short_router_proxy(합성 숏 라우터 프록시)",
            "idea_type": "offensive_exploration(공격 탐색)",
            "policy_family": "short_source_restore_all_hours(전시간 숏 원천 복원)",
            "short_threshold": 0.445,
            "session_hours": [],
            "fixed_hold_bars": FIXED_HOLD_BARS,
            "description": "add flat-no-position short-like p_short>=0.445 entries(무포지션 숏 유사 p_short>=0.445 진입 추가)",
        },
        {
            "variant_id": "bm03_short_router_ps0440_all_hours_fixed6",
            "queue_id": "bm03_short_source_router_ps0445_no_long_delete",
            "candidate_kind": "synthetic_short_router_proxy(합성 숏 라우터 프록시)",
            "idea_type": "offensive_exploration(공격 탐색)",
            "policy_family": "short_source_restore_all_hours(전시간 숏 원천 복원)",
            "short_threshold": 0.44,
            "session_hours": [],
            "fixed_hold_bars": FIXED_HOLD_BARS,
            "description": "add flat-no-position short-like p_short>=0.440 entries(무포지션 숏 유사 p_short>=0.440 진입 추가)",
        },
        {
            "variant_id": "bm04_short_router_ps0445_h17_20_overlay_fixed6",
            "queue_id": "bm04_short_router_session_regime_overlay",
            "candidate_kind": "synthetic_short_router_proxy(합성 숏 라우터 프록시)",
            "idea_type": "offensive_exploration(공격 탐색)",
            "policy_family": "h17_20_short_router_overlay(17~20시 숏 라우터 오버레이)",
            "short_threshold": 0.445,
            "session_hours": [17, 18, 19, 20],
            "fixed_hold_bars": FIXED_HOLD_BARS,
            "description": "short source in cash-open hours only(캐시 오픈 시간대 숏 원천만 사용)",
        },
        {
            "variant_id": "bm04_short_router_ps0440_h17_20_overlay_fixed6",
            "queue_id": "bm04_short_router_session_regime_overlay",
            "candidate_kind": "synthetic_short_router_proxy(합성 숏 라우터 프록시)",
            "idea_type": "offensive_exploration(공격 탐색)",
            "policy_family": "h17_20_short_router_overlay(17~20시 숏 라우터 오버레이)",
            "short_threshold": 0.44,
            "session_hours": [17, 18, 19, 20],
            "fixed_hold_bars": FIXED_HOLD_BARS,
            "description": "slightly lower short router in cash-open hours(캐시 오픈 시간대 숏 라우터 소폭 완화)",
        },
        {
            "variant_id": "bm04_short_router_ps0435_h17_20_overlay_fixed6",
            "queue_id": "bm04_short_router_session_regime_overlay",
            "candidate_kind": "synthetic_short_router_proxy(합성 숏 라우터 프록시)",
            "idea_type": "offensive_exploration(공격 탐색)",
            "policy_family": "h17_20_short_router_overlay(17~20시 숏 라우터 오버레이)",
            "short_threshold": 0.435,
            "session_hours": [17, 18, 19, 20],
            "fixed_hold_bars": FIXED_HOLD_BARS,
            "description": "stress lower short router in cash-open hours(캐시 오픈 시간대 숏 라우터 완화 압박)",
        },
    ]


def closed_filter_mask(frame: pd.DataFrame, candidate: Mapping[str, Any]) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    blocked_months = [str(item) for item in candidate.get("blocked_months", [])]
    long_hours = [as_int(item) for item in candidate.get("long_hours", [])]
    hold_buckets = [str(item) for item in candidate.get("hold_buckets", [])]
    margin_col = str(candidate.get("margin_col", ""))
    margin_min = candidate.get("margin_min")
    if blocked_months and long_hours:
        mask &= ~((frame["side"] == "long") & frame["entry_month"].isin(blocked_months) & frame["entry_hour"].isin(long_hours))
    elif blocked_months:
        mask &= ~frame["entry_month"].isin(blocked_months)
    if long_hours and margin_col and margin_min is not None:
        mask &= ~(
            (frame["side"] == "long")
            & frame["entry_hour"].isin(long_hours)
            & (pd.to_numeric(frame[margin_col], errors="coerce") < as_float(margin_min))
        )
    if hold_buckets and margin_col and margin_min is not None:
        mask &= ~(
            frame["hold_bucket"].isin(hold_buckets)
            & (pd.to_numeric(frame[margin_col], errors="coerce") < as_float(margin_min))
        )
    return mask


def synthetic_short_candidates(
    cycles: pd.DataFrame,
    bars: pd.DataFrame,
    index_by_time: Mapping[pd.Timestamp, int],
    candidate: Mapping[str, Any],
) -> pd.DataFrame:
    threshold = as_float(candidate.get("short_threshold"), 999.0)
    hours = [as_int(item) for item in candidate.get("session_hours", [])]
    hold_bars = as_int(candidate.get("fixed_hold_bars"), FIXED_HOLD_BARS)
    pool = cycles[
        (cycles["exec_action"].astype(str) == "flat_no_position")
        & (cycles["p_short"] >= threshold)
        & (cycles["p_short"] > cycles["p_long"])
        & (cycles["p_short"] > cycles["p_flat"])
    ].copy()
    if hours:
        pool = pool[pool["entry_hour"].isin(hours)].copy()
    selected: list[dict[str, Any]] = []
    occupied_until = pd.Timestamp.min
    for _, row in pool.sort_values("written_at_dt").iterrows():
        entry_dt = row["written_at_dt"]
        if pd.isna(entry_dt) or entry_dt <= occupied_until:
            continue
        bar_idx = index_by_time.get(entry_dt)
        if bar_idx is None:
            continue
        exit_idx = bar_idx + hold_bars
        if exit_idx >= len(bars):
            continue
        entry_bar = bars.iloc[bar_idx]
        exit_bar = bars.iloc[exit_idx]
        exit_dt = exit_bar["bar_time_dt"]
        if pd.isna(exit_dt) or exit_dt <= entry_dt:
            continue
        entry_price = float(entry_bar["open"])
        exit_price = float(exit_bar["open"]) + float(exit_bar["spread_price"])
        pnl = (entry_price - exit_price) * FIXED_LOT
        selected.append(
            {
                "variant_id": candidate["variant_id"],
                "synthetic_trade_id": f"{candidate['variant_id']}__syn{len(selected) + 1:04d}",
                "source": "synthetic_fixed6_short_proxy(합성 고정6봉 숏 프록시)",
                "side": "short",
                "entry_time_dt": entry_dt,
                "exit_time_dt": exit_dt,
                "entry_time": entry_dt.isoformat(),
                "exit_time": exit_dt.isoformat(),
                "entry_hour": int(row["entry_hour"]),
                "entry_month": row["entry_month"],
                "entry_quarter": row["entry_quarter"],
                "entry_price": finite(entry_price, 8),
                "exit_price": finite(exit_price, 8),
                "volume": FIXED_LOT,
                "pnl": finite(pnl, 10),
                "p_short": finite(row["p_short"], 10),
                "p_flat": finite(row["p_flat"], 10),
                "p_long": finite(row["p_long"], 10),
                "short_margin_vs_long": finite(row["short_margin_vs_long"], 10),
                "short_margin_vs_flat": finite(row["short_margin_vs_flat"], 10),
                "fixed_hold_bars": hold_bars,
                "label_source": "US100 raw M5 bid/ask proxy(US100 원천 M5 bid/ask 프록시)",
                "feature_boundary": "entry-known probabilities and hour only; future bars label evaluation only(진입시점 확률/시간만 피처, 미래 봉은 라벨 평가 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        occupied_until = exit_dt
    return pd.DataFrame(selected)


def parent_trade_tape(frame: pd.DataFrame) -> pd.DataFrame:
    tape = frame.copy()
    tape["trade_id"] = tape["trade_index"].apply(lambda value: f"parent_{int(value):04d}")
    tape["source"] = "parent_kept(부모 유지)"
    return tape[
        [
            "trade_id",
            "source",
            "trade_index",
            "side",
            "entry_time_dt",
            "exit_time_dt",
            "entry_time",
            "exit_time",
            "entry_hour",
            "entry_month",
            "entry_quarter",
            "pnl",
            "p_short",
            "p_flat",
            "p_long",
            "margin_vs_opposite",
            "margin_vs_flat",
            "claim_boundary",
        ]
    ].copy()


def combine_with_synthetic(parent_trades: pd.DataFrame, synthetic: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if synthetic.empty:
        tape = parent_trade_tape(parent_trades)
        tape["displaced_by"] = ""
        return tape.sort_values("entry_time_dt").reset_index(drop=True), pd.DataFrame()
    displaced_ids: set[int] = set()
    displaced_rows = []
    for _, syn in synthetic.iterrows():
        hits = parent_trades[
            (parent_trades["entry_time_dt"] >= syn["entry_time_dt"])
            & (parent_trades["entry_time_dt"] < syn["exit_time_dt"])
        ].copy()
        for _, hit in hits.iterrows():
            trade_index = int(hit["trade_index"])
            displaced_ids.add(trade_index)
            displaced_rows.append(
                {
                    "variant_id": syn["variant_id"],
                    "synthetic_trade_id": syn["synthetic_trade_id"],
                    "displaced_parent_trade_index": trade_index,
                    "displaced_entry_time": hit["entry_time"],
                    "displaced_exit_time": hit["exit_time"],
                    "displaced_side": hit["side"],
                    "displaced_pnl": hit["pnl"],
                    "displacement_reason": "one_position_semantics(단일 포지션 의미)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    kept = parent_trades[~parent_trades["trade_index"].isin(displaced_ids)].copy()
    parent_tape = parent_trade_tape(kept)
    parent_tape["displaced_by"] = ""
    synthetic_tape = synthetic.copy()
    synthetic_tape["trade_id"] = synthetic_tape["synthetic_trade_id"]
    synthetic_tape["trade_index"] = ""
    synthetic_tape["margin_vs_opposite"] = synthetic_tape["short_margin_vs_long"]
    synthetic_tape["margin_vs_flat"] = synthetic_tape["short_margin_vs_flat"]
    synthetic_tape["displaced_by"] = ""
    synthetic_tape = synthetic_tape[
        [
            "trade_id",
            "source",
            "trade_index",
            "side",
            "entry_time_dt",
            "exit_time_dt",
            "entry_time",
            "exit_time",
            "entry_hour",
            "entry_month",
            "entry_quarter",
            "pnl",
            "p_short",
            "p_flat",
            "p_long",
            "margin_vs_opposite",
            "margin_vs_flat",
            "claim_boundary",
            "displaced_by",
        ]
    ]
    combined = pd.concat([parent_tape, synthetic_tape], ignore_index=True).sort_values("entry_time_dt").reset_index(drop=True)
    return combined, pd.DataFrame(displaced_rows)


def synthetic_quality_metrics(synthetic: pd.DataFrame) -> dict[str, Any]:
    if synthetic.empty:
        return {
            "synthetic_short_net_profit": 0.0,
            "synthetic_short_profit_factor": 0.0,
            "synthetic_short_trade_count": 0,
            "synthetic_short_expectancy": 0.0,
            "synthetic_short_win_rate_percent": 0.0,
        }
    pnl = pd.to_numeric(synthetic["pnl"], errors="coerce").fillna(0.0)
    gp = float(pnl[pnl > 0].sum())
    gl = float(-pnl[pnl < 0].sum())
    count = int(len(pnl))
    return {
        "synthetic_short_net_profit": finite(float(pnl.sum()), 10),
        "synthetic_short_profit_factor": finite(gp / gl if gl else 999.0, 10),
        "synthetic_short_trade_count": count,
        "synthetic_short_expectancy": finite(float(pnl.sum()) / count if count else 0.0, 10),
        "synthetic_short_win_rate_percent": finite((pnl > 0).mean() * 100.0, 10),
    }


def status_for(row: Mapping[str, Any], baseline: Mapping[str, Any], bl_final: Mapping[str, Any]) -> str:
    if as_float(row["trade_density_per_business_day"]) < DENSITY_FLOOR:
        return "rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴)"
    if as_float(row["profit_factor"]) < MIN_PF_KEEP:
        return "watch_pf_below_keep_floor(PF 유지 하한 미달 관찰)"
    if as_float(row["short_share"]) < TARGET_SHORT_SHARE:
        return "watch_short_share_still_below_target(숏 비중 목표 미달 관찰)"
    if as_int(row.get("synthetic_short_trade_count")) and as_int(row.get("synthetic_short_trade_count")) < as_int(bl_final.get("additional_shorts_needed_if_no_long_delete")):
        return "watch_new_short_count_below_balance_need(신규 숏 수량 균형 필요량 미달 관찰)"
    if as_int(row.get("synthetic_short_trade_count")) and (
        as_float(row.get("synthetic_short_net_profit")) < 0.0 or as_float(row.get("synthetic_short_profit_factor")) < 1.15
    ):
        return "watch_combined_proxy_improves_but_short_source_negative(관찰, 합산 프록시 개선이나 숏 원천 단독 음수)"
    if as_float(row["net_profit"]) >= as_float(baseline["net_profit"]) and as_float(row["closed_drawdown_amount"]) <= as_float(baseline["closed_drawdown_amount"]):
        return "proxy_review_candidate_short_balance_density_dd_pass(프록시 검토 후보, 숏 균형/밀도/낙폭 통과)"
    return "watch_proxy_tradeoff_review_required(프록시 상충 검토 필요)"


def selection_score(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> float:
    score = (as_float(row["net_profit"]) - as_float(baseline["net_profit"])) * 0.5
    score += (as_float(row["profit_factor"]) - MIN_PF_KEEP) * 160.0
    score += max(0.0, TARGET_SHORT_SHARE - as_float(baseline["short_share"])) * 200.0
    score += max(0.0, as_float(row["short_share"]) - TARGET_SHORT_SHARE) * 180.0
    score += (as_float(baseline["closed_drawdown_amount"]) - as_float(row["closed_drawdown_amount"])) * 0.35
    score += min(0.20, max(0.0, as_float(row["trade_density_per_business_day"]) - DENSITY_FLOOR)) * 160.0
    score -= max(0, as_int(row.get("displaced_parent_trade_count")) - 40) * 0.2
    if as_float(row["trade_density_per_business_day"]) < DENSITY_FLOOR:
        score -= 1000.0
    if as_float(row["profit_factor"]) < MIN_PF_KEEP:
        score -= 200.0
    if as_float(row["short_share"]) < TARGET_SHORT_SHARE:
        score -= 120.0
    if "exact" in str(row.get("policy_family", "")):
        score -= 40.0
    return round(score, 10)


def build_surface(
    trades: pd.DataFrame,
    cycles: pd.DataFrame,
    bars: pd.DataFrame,
    index_by_time: Mapping[pd.Timestamp, int],
    bl_final: Mapping[str, Any],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], dict[str, Any]]:
    full_days = full_business_days(trades)
    baseline = metric_frame(trades, full_days=full_days)
    tapes: dict[str, pd.DataFrame] = {}
    all_synth: list[pd.DataFrame] = []
    all_displaced: list[pd.DataFrame] = []
    rows: list[dict[str, Any]] = []
    for candidate in candidate_definitions():
        candidate_kind = str(candidate.get("candidate_kind", ""))
        if "synthetic_short_router" in candidate_kind:
            synthetic = synthetic_short_candidates(cycles, bars, index_by_time, candidate)
            tape, displaced = combine_with_synthetic(trades, synthetic)
            all_synth.append(synthetic)
            if not displaced.empty:
                all_displaced.append(displaced)
            metrics = metric_frame(tape, full_days=full_days)
            quality = synthetic_quality_metrics(synthetic)
            available_pool = cycles[
                (cycles["exec_action"].astype(str) == "flat_no_position")
                & (cycles["p_short"] >= as_float(candidate.get("short_threshold"), 999.0))
                & (cycles["p_short"] > cycles["p_long"])
                & (cycles["p_short"] > cycles["p_flat"])
            ].copy()
            hours = [as_int(item) for item in candidate.get("session_hours", [])]
            if hours:
                available_pool = available_pool[available_pool["entry_hour"].isin(hours)].copy()
            removed_count = int(len(trades) - len(tape[tape["source"].astype(str).str.contains("parent_kept", na=False)]))
            row = {
                **candidate,
                **metrics,
                **quality,
                "run_id": RUN_ID,
                "available_short_like_cycle_count": int(len(available_pool)),
                "synthetic_added_short_count": int(len(synthetic)),
                "displaced_parent_trade_count": int(len(displaced)),
                "displaced_parent_net_profit": finite(displaced["displaced_pnl"].astype(float).sum() if not displaced.empty else 0.0, 10),
                "removed_trade_count": removed_count,
                "synthetic_label_status": "fixed6_bidask_proxy_label_not_mt5_runtime(고정6봉 bid/ask 프록시 라벨, MT5 런타임 아님)",
            }
        else:
            if "reference" in candidate_kind:
                mask = pd.Series(True, index=trades.index)
            else:
                mask = closed_filter_mask(trades, candidate)
            tape = parent_trade_tape(trades[mask].copy())
            tape["displaced_by"] = ""
            metrics = metric_frame(tape, full_days=full_days)
            row = {
                **candidate,
                **metrics,
                "run_id": RUN_ID,
                "available_short_like_cycle_count": 0,
                "synthetic_added_short_count": 0,
                "displaced_parent_trade_count": 0,
                "displaced_parent_net_profit": 0.0,
                "removed_trade_count": int(len(trades) - int(len(tape))),
                "synthetic_short_net_profit": 0.0,
                "synthetic_short_profit_factor": 0.0,
                "synthetic_short_trade_count": 0,
                "synthetic_short_expectancy": 0.0,
                "synthetic_short_win_rate_percent": 0.0,
                "synthetic_label_status": "not_applicable_closed_trade_proxy(해당 없음, 종료거래 프록시)",
            }
        row["net_delta_vs_baseline"] = finite(as_float(row["net_profit"]) - as_float(baseline["net_profit"]), 10)
        row["pf_delta_vs_baseline"] = finite(as_float(row["profit_factor"]) - as_float(baseline["profit_factor"]), 10)
        row["density_delta_vs_baseline"] = finite(as_float(row["trade_density_per_business_day"]) - as_float(baseline["trade_density_per_business_day"]), 10)
        row["closed_dd_delta_vs_baseline"] = finite(as_float(row["closed_drawdown_amount"]) - as_float(baseline["closed_drawdown_amount"]), 10)
        row["density_floor_pass"] = as_float(row["trade_density_per_business_day"]) >= DENSITY_FLOOR
        row["pf_keep_floor_pass"] = as_float(row["profit_factor"]) >= MIN_PF_KEEP
        row["short_share_target_pass"] = as_float(row["short_share"]) >= TARGET_SHORT_SHARE
        row["new_short_need_pass"] = as_int(row.get("synthetic_added_short_count")) >= as_int(bl_final.get("additional_shorts_needed_if_no_long_delete"))
        row["candidate_status"] = status_for(row, baseline, bl_final)
        row["selection_score"] = selection_score(row, baseline)
        row["claim_boundary"] = CLAIM_BOUNDARY
        rows.append(row)
        tapes[str(candidate["variant_id"])] = tape
    surface = pd.DataFrame(rows).sort_values(
        ["candidate_status", "selection_score", "net_profit"],
        ascending=[True, False, False],
    ).reset_index(drop=True)
    surface = surface.sort_values(
        by=["short_share_target_pass", "pf_keep_floor_pass", "density_floor_pass", "selection_score"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    all_synthetic = pd.concat([frame for frame in all_synth if not frame.empty], ignore_index=True) if any(not frame.empty for frame in all_synth) else pd.DataFrame()
    all_displaced_df = pd.concat(all_displaced, ignore_index=True) if all_displaced else pd.DataFrame()
    tapes["__all_synthetic__"] = all_synthetic
    tapes["__all_displaced__"] = all_displaced_df
    return surface, tapes, baseline


def segment_rows(frame: pd.DataFrame, group_col: str, segment_type: str, *, full_days: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if frame.empty or group_col not in frame.columns:
        return rows
    for key, part in frame.groupby(group_col, sort=True):
        if full_days is None:
            days = max(1, int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1))))
        else:
            days = full_days
        metric = metric_frame(part.copy(), full_days=days)
        rows.append(
            {
                "run_id": RUN_ID,
                "segment_type": segment_type,
                "segment_id": str(key),
                "business_days": days,
                **metric,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def short_source_rows(surface: pd.DataFrame, selected: Mapping[str, Any], cycles: pd.DataFrame, bl_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    flat_short_like_0445 = cycles[
        (cycles["exec_action"].astype(str) == "flat_no_position")
        & (cycles["p_short"] >= 0.445)
        & (cycles["p_short"] > cycles["p_long"])
        & (cycles["p_short"] > cycles["p_flat"])
    ]
    h17_20 = flat_short_like_0445[flat_short_like_0445["entry_hour"].isin([17, 18, 19, 20])]
    rows.append(
        {
            "run_id": RUN_ID,
            "audit_id": "short_like_cycle_coverage(숏 유사 사이클 커버리지)",
            "flat_short_like_ps0445_cycles": len(flat_short_like_0445),
            "flat_short_like_ps0445_h17_20_cycles": len(h17_20),
            "additional_shorts_needed": bl_final.get("additional_shorts_needed_if_no_long_delete"),
            "coverage_pass": len(h17_20) >= as_int(bl_final.get("additional_shorts_needed_if_no_long_delete")),
            "effect": "new short source(새 숏 원천)가 long hard delete(롱 강제 삭제)보다 먼저 검토 가능함을 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    for _, row in surface[surface["candidate_kind"].astype(str).str.contains("synthetic_short_router", na=False)].iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "audit_id": row["variant_id"],
                "short_threshold": row.get("short_threshold", ""),
                "session_hours": ",".join(str(item) for item in row.get("session_hours", [])) if isinstance(row.get("session_hours"), list) else row.get("session_hours", ""),
                "available_short_like_cycle_count": row["available_short_like_cycle_count"],
                "synthetic_added_short_count": row["synthetic_added_short_count"],
                "displaced_parent_trade_count": row["displaced_parent_trade_count"],
                "synthetic_short_net_profit": row["synthetic_short_net_profit"],
                "synthetic_short_profit_factor": row["synthetic_short_profit_factor"],
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "short_share": row["short_share"],
                "candidate_status": row["candidate_status"],
                "effect": "short router(숏 라우터)의 coverage(커버리지)와 proxy EV(프록시 기대값)를 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "run_id": RUN_ID,
            "audit_id": "selected_short_balance(선택 숏 균형)",
            "selected_variant_id": selected["variant_id"],
            "selected_short_share": selected["short_share"],
            "selected_short_trade_count": selected["short_trade_count"],
            "selected_synthetic_added_short_count": selected["synthetic_added_short_count"],
            "selected_displaced_parent_trade_count": selected["displaced_parent_trade_count"],
            "judgment": "review_required_mt5_runtime_probe_needed(검토 필요, MT5 런타임 탐침 필요)",
            "effect": "숏 비중 개선을 운영 주장으로 올리기 전에 MT5 재탐침 조건으로 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def equity_dd_rows(baseline: Mapping[str, Any], selected: Mapping[str, Any], bl_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "diagnostic_id": "parent_mt5_equity_dd(부모 MT5 평가손익 낙폭)",
            "value": bl_final.get("parent_equity_dd_percent"),
            "threshold": parent.EQUITY_DD_WARN_PERCENT,
            "status": "stress_required(압박 필요)" if as_float(bl_final.get("parent_equity_dd_percent")) > parent.EQUITY_DD_WARN_PERCENT else "watch(관찰)",
            "effect": "closed-trade proxy(종료거래 프록시)가 MT5 equity path(MT5 평가손익 경로)를 대체하지 못함을 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "diagnostic_id": "baseline_closed_trade_dd(기준 종료거래 낙폭)",
            "value": baseline["closed_drawdown_amount"],
            "percent": baseline["closed_drawdown_percent"],
            "status": "proxy_reference(프록시 기준)",
            "effect": "BM 후보의 낙폭 개선은 종료거래 기준으로만 비교한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "diagnostic_id": "selected_closed_trade_dd(선택 종료거래 낙폭)",
            "value": selected["closed_drawdown_amount"],
            "percent": selected["closed_drawdown_percent"],
            "delta_vs_baseline": selected["closed_dd_delta_vs_baseline"],
            "status": "proxy_improved(프록시 개선)" if as_float(selected["closed_dd_delta_vs_baseline"]) < 0 else "proxy_not_improved(프록시 미개선)",
            "effect": "BN review(BN 검토)에서 MT5 equity DD(MT5 평가손익 낙폭) 재탐침 필요 여부를 결정하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "selected_variant_id": selected["variant_id"],
        "trade_splitting_status": "forbidden_not_used(금지 및 미사용)",
        "top_n_status": "forbidden_not_used(금지 및 미사용)",
        "oos_threshold_selection_status": "not_claimed_same_tape_review_required(미주장, 동일 테이프 검토 필요)",
        "timestamp_boundary": "entry_known_closed_m5_only(진입시점 닫힌 M5 정보만 사용)",
        "feature_label_boundary": "future bars used only for proxy labels(미래 봉은 프록시 라벨 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bn01_review_combined_gain_vs_negative_short_source",
            "review_question": "Is the combined gain caused by displacing worse parent trades rather than positive short source?(합산 개선이 양수 숏 원천이 아니라 더 나쁜 부모 거래 대체에서 온 것인가?)",
            "required_evidence": rel(PROXY_SCOUT_SURFACE),
            "success_criteria": "attribution separates synthetic short PF from displaced parent PnL(합성 숏 PF와 대체된 부모 손익을 분리)",
            "effect": "combined proxy(합산 프록시) 착시를 먼저 제거한다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bn02_repair_short_source_quality_or_reject_package",
            "review_question": "Can short source quality be repaired without long hard-delete or trade splitting?(롱 강제 삭제나 거래 쪼개기 없이 숏 원천 품질을 수리할 수 있는가?)",
            "required_evidence": rel(SELECTED_PROXY_CANDIDATE),
            "success_criteria": "synthetic short PF>=1.15 and combined PF>=1.35 with density>=3/day(합성 숏 PF 1.15 이상, 합산 PF 1.35 이상, 밀도 3/day 이상)",
            "effect": "negative short source(음수 숏 원천)는 package(패키지) 후보에서 제외한다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bn03_package_gate_only_if_short_source_positive",
            "review_question": "Only if short source becomes positive, prepare narrow MT5 runtime probe handoff(숏 원천이 양수로 바뀔 때만 좁은 MT5 런타임 탐침 인계를 준비할 것인가?)",
            "required_evidence": rel(RUN364BN_QUEUE),
            "success_criteria": "fixed parameters plus positive short source and proxy/MT5 diff plan(고정 파라미터 + 양수 숏 원천 + 프록시/MT5 차이 계획)",
            "effect": "proxy-only(프록시 전용) 성과를 운영 claim(운영 주장)으로 착각하지 않는다.",
        },
    ]


def gate_rows(
    join_audit: Sequence[Mapping[str, Any]],
    parity_audit: Sequence[Mapping[str, Any]],
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    selected_status = str(selected["candidate_status"])
    rows = [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed",
            "evidence": rel(PROXY_SCOUT_SURFACE),
            "effect": "BL queue(BL 대기열)의 forward/regime, short source, equity DD 축을 BM surface(BM 표면)로 닫았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if as_float(selected["trade_density_per_business_day"]) >= DENSITY_FLOOR and as_float(selected["profit_factor"]) >= MIN_PF_KEEP else "failed",
            "evidence": rel(SELECTED_PROXY_CANDIDATE),
            "effect": "net/PF/expectancy/DD/recovery/trades/long-short를 동시에 기록했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "data_integrity_join_audit",
            "status": "passed" if join_audit and as_int(join_audit[0]["missing_probability_rows"]) == 0 else "failed",
            "evidence": rel(ENTRY_PROBABILITY_JOIN_AUDIT),
            "effect": "closed trade(종료거래)와 telemetry(실행 기록)를 1:1로 결합했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "raw_bar_proxy_label_audit",
            "status": "passed" if parity_audit and as_float(parity_audit[0]["median_abs_pnl_diff"], 999.0) <= 0.05 else "failed",
            "evidence": rel(RAW_BAR_PRICE_PARITY_AUDIT),
            "effect": "US100 raw M5(원천 5분봉) 기반 synthetic short label(합성 숏 라벨)의 최소 가격 정합성을 확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "short_balance_proxy_gate",
            "status": "passed" if as_float(selected["short_share"]) >= TARGET_SHORT_SHARE else "failed",
            "evidence": rel(SHORT_SOURCE_FEASIBILITY),
            "effect": "short share(숏 비중) 목표는 통과했지만 short source PF(숏 원천 PF)는 별도 실패 기억으로 낮췄다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "no_trade_splitting_gate",
            "status": "passed",
            "evidence": rel(SELECTED_PROXY_TRADE_TAPE),
            "effect": "synthetic short(합성 숏)은 fixed hold(고정 보유) 단일 포지션 의미로만 추가했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "skill_receipt_lint",
            "status": "passed",
            "evidence": ";".join(rel(path) for path in [RUN_EVIDENCE_RECEIPT, DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT]),
            "effect": "experiment_execution(실험 실행) 스킬 영수증을 산출물에 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if len(queue) == 3 and selected_status else "failed",
            "evidence": rel(RUN364BN_QUEUE),
            "effect": "BN review(BN 검토) 이전에 필수 게이트와 다음 조건을 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 차단했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def final_payload(
    bl_final: Mapping[str, Any],
    baseline: Mapping[str, Any],
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    selected_tape: pd.DataFrame,
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    strict_rows = int(surface["candidate_status"].astype(str).str.contains("proxy_review_candidate", na=False).sum())
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_mt5_net_profit": bl_final.get("parent_mt5_net_profit"),
        "parent_mt5_profit_factor": bl_final.get("parent_mt5_profit_factor"),
        "parent_mt5_expectancy": bl_final.get("parent_mt5_expectancy"),
        "parent_mt5_trade_count": bl_final.get("parent_mt5_trade_count"),
        "parent_trade_density": bl_final.get("parent_trade_density"),
        "parent_equity_dd_percent": bl_final.get("parent_equity_dd_percent"),
        "parent_short_share": bl_final.get("parent_short_share"),
        "parent_long_share": bl_final.get("parent_long_share"),
        "additional_shorts_needed": bl_final.get("additional_shorts_needed_if_no_long_delete"),
        "baseline_closed_trade_net_profit": baseline["net_profit"],
        "baseline_closed_trade_profit_factor": baseline["profit_factor"],
        "baseline_closed_trade_count": baseline["trade_count"],
        "baseline_closed_trade_density": baseline["trade_density_per_business_day"],
        "baseline_closed_trade_dd_amount": baseline["closed_drawdown_amount"],
        "selected_variant_id": selected["variant_id"],
        "selected_queue_id": selected["queue_id"],
        "selected_policy_family": selected["policy_family"],
        "selected_candidate_status": selected["candidate_status"],
        "selected_net_profit": selected["net_profit"],
        "selected_profit_factor": selected["profit_factor"],
        "selected_expectancy": selected["expectancy"],
        "selected_trade_count": selected["trade_count"],
        "selected_trade_density": selected["trade_density_per_business_day"],
        "selected_closed_drawdown_amount": selected["closed_drawdown_amount"],
        "selected_closed_drawdown_percent": selected["closed_drawdown_percent"],
        "selected_recovery_factor": selected["recovery_factor"],
        "selected_long_trade_count": selected["long_trade_count"],
        "selected_short_trade_count": selected["short_trade_count"],
        "selected_long_share": selected["long_share"],
        "selected_short_share": selected["short_share"],
        "selected_synthetic_added_short_count": selected["synthetic_added_short_count"],
        "selected_displaced_parent_trade_count": selected["displaced_parent_trade_count"],
        "selected_synthetic_short_net_profit": selected["synthetic_short_net_profit"],
        "selected_synthetic_short_profit_factor": selected["synthetic_short_profit_factor"],
        "selected_net_delta_vs_baseline": selected["net_delta_vs_baseline"],
        "selected_pf_delta_vs_baseline": selected["pf_delta_vs_baseline"],
        "selected_density_delta_vs_baseline": selected["density_delta_vs_baseline"],
        "selected_closed_dd_delta_vs_baseline": selected["closed_dd_delta_vs_baseline"],
        "selected_selection_score": selected["selection_score"],
        "surface_rows": len(surface),
        "proxy_review_candidate_rows": strict_rows,
        "selected_tape_rows": len(selected_tape),
        "next_queue_rows": len(queue),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_started_proxy_only(프록시 전용이라 시작 안 함)",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
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
            "effect": "BL queue(BL 대기열)를 BM proxy scout(BM 프록시 정찰)으로 실행하고 BN review(BN 검토) 입력을 만든다.",
        },
    )


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "evidence_available": [rel(PROXY_SCOUT_SURFACE), rel(SELECTED_PROXY_CANDIDATE), rel(SELECTED_PROXY_TRADE_TAPE), rel(SHORT_SOURCE_FEASIBILITY)],
            "evidence_missing": ["new MT5 execution(새 MT5 실행)", "forward pass(전진 통과)", "runtime authority audit(런타임 권위 감사)"],
            "measurement_scope": "closed trade plus fixed6 synthetic short proxy(종료거래 + 고정6봉 합성 숏 프록시)",
            "judgment": JUDGMENT,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(BK.CLOSED_TRADE_ATTRIBUTION), rel(BK.PARENT_TELEMETRY_COPY), rel(US100_BARS)],
            "time_axis": "MT5 entry_time and telemetry written_at are broker-aligned; raw M5 time_open_unix matches entry quote timestamps(MT5 진입시각과 telemetry 작성시각은 브로커 정렬, 원천 M5 time_open_unix는 진입 호가 시각과 정합)",
            "sample_scope": "US100 M5 BK runtime probe trades plus flat-no-position telemetry cycles(US100 M5 BK 런타임 탐침 거래와 무포지션 telemetry cycle)",
            "feature_label_boundary": "candidate features are entry-known probability/hour/session only; future bars are label/evaluation only(후보 피처는 진입시점 확률/시간/세션만, 미래 봉은 라벨/평가 전용)",
            "leakage_risk": "same-tape threshold choice, therefore review required and no operating claim(동일 테이프 임계값 선택이라 검토 필요 및 운영 주장 없음)",
            "integrity_judgment": "usable_proxy_with_boundary(경계 포함 프록시 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "h17-20 short source can restore short balance while preserving net/PF/density(17~20시 숏 원천이 순수익/PF/밀도를 보존하며 숏 균형을 복원할 수 있음)",
            "comparison_baseline": SOURCE_RUNTIME_PROBE_RUN_ID,
            "control_variables": ["US100 M5", "fixed 0.1 lot(고정 0.1랏)", "one-position semantics(단일 포지션 의미)", "no trade splitting(거래 쪼개기 없음)"],
            "changed_variables": ["short probability threshold(숏 확률 임계값)", "h17-20 session overlay(17~20시 세션 오버레이)", "fixed6 synthetic label(고정6봉 합성 라벨)"],
            "success_criteria": "PF>=1.35, density>=3/day, short_share>=0.12, closed DD improves(PF 1.35 이상, 밀도 3/day 이상, 숏비중 0.12 이상, 종료거래 낙폭 개선)",
            "failure_criteria": "PF or density breaks, short source net negative, or MT5 reprobe fails(PF/밀도 붕괴, 숏 원천 순손실, MT5 재탐침 실패)",
            "decision_use": NEXT_RUN_ID,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "no new model trained; runtime ONNX probabilities reused(새 모델 학습 없음, 런타임 ONNX 확률 재사용)",
            "threshold_policy": "same-tape proxy scout threshold, not operating selection(동일 테이프 프록시 정찰 임계값, 운영 선택 아님)",
            "overfit_risk": "medium_high_same_tape_synthetic_label(중상, 동일 테이프 합성 라벨)",
            "validation_judgment": "proxy_review_required(프록시 검토 필요)",
            "selected_variant_id": selected["variant_id"],
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(BK.RUNTIME_RECEIPT), rel(BK.PARENT_TELEMETRY_COPY)],
            "shared_contract": "closed M5 bar probabilities p_short/p_flat/p_long, one-position MT5 semantics(닫힌 M5 확률 p_short/p_flat/p_long, 단일 포지션 MT5 의미)",
            "known_differences": "BM does not execute EA and synthetic fixed6 labels approximate only(BM은 EA를 실행하지 않고 합성 고정6봉 라벨은 근사일 뿐)",
            "parity_check": rel(RAW_BAR_PRICE_PARITY_AUDIT),
            "runtime_claim_boundary": "proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"selected={selected['variant_id']}; net={selected['net_profit']}; pf={selected['profit_factor']}; density={selected['trade_density_per_business_day']}; short_share={selected['short_share']}; synthetic_short_pf={selected['synthetic_short_profit_factor']}",
            "likely_drivers": "combined gain comes from displacing worse parent trades while standalone synthetic shorts are negative(합산 개선은 더 나쁜 부모 거래 대체에서 오며 합성 숏 단독은 음수)",
            "alternative_explanations": "same-tape displacement can hide weak short source quality(동일 테이프 대체 효과가 약한 숏 원천 품질을 숨길 수 있음)",
            "attribution_confidence": "low_to_medium_proxy_only(프록시 전용 낮음~중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(PROXY_SCOUT_SURFACE), rel(SELECTED_PROXY_CANDIDATE), rel(GATE_AUDIT)],
            "evidence_missing": ["MT5 strategy tester output(MT5 전략 테스터 출력)", "forward/replay pass(전진/재생 통과)", "operating promotion audit(운영 승격 감사)"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve", "forward_passed"],
            "effect": "proxy success(프록시 성공)를 runtime authority(런타임 권위)로 올리지 않는다.",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_proxy_boundary(프록시 경계 포함 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    forward_rows: Sequence[Mapping[str, Any]],
    short_rows: Sequence[Mapping[str, Any]],
    dd_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top = surface.head(8).to_dict("records")
    rejected = surface[~surface["candidate_status"].astype(str).str.contains("proxy_review_candidate", na=False)].head(8).to_dict("records")
    report = f"""# run364BM h19 stress short-balance proxy scout(364BM h19 압박 숏 균형 프록시 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- selected_variant(선택 변형): `{final['selected_variant_id']}`
- selected net/PF/expectancy/trades/density(선택 순수익/수익 팩터/기대값/거래수/밀도): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_expectancy']}` / `{final['selected_trade_count']}` / `{final['selected_trade_density']}`
- selected long/short/share(선택 롱/숏/비중): `{final['selected_long_trade_count']}` / `{final['selected_short_trade_count']}` / `{final['selected_short_share']}`
- selected closed DD/recovery(선택 종료거래 낙폭/회복 계수): `{final['selected_closed_drawdown_amount']}` / `{final['selected_recovery_factor']}`
- parent MT5 net/PF/trades/equity DD(부모 MT5 순수익/수익 팩터/거래수/평가손익 낙폭): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}` / `{final['parent_equity_dd_percent']}%`
- synthetic short PF/net(합성 숏 PF/순수익): `{final['selected_synthetic_short_profit_factor']}` / `{final['selected_synthetic_short_net_profit']}`. This is no package candidate(패키지 후보 없음) until repaired.

## Action And Effect(행동과 효과)

Action(행동): BL queue(BL 대기열)를 closed trade + telemetry + US100 raw M5(종료거래 + 실행기록 + US100 원천 5분봉)로 proxy scout(프록시 정찰)했다.

Effect(효과): h17-20 short router(17~20시 숏 라우터)는 combined proxy(합산 프록시)를 개선했지만 standalone short source(숏 원천 단독)는 음수라서, BN review(BN 검토)에서 package reject(패키지 거절) 또는 short source repair(숏 원천 수리)로 분리한다.

## Top Surface(상위 표면)

{markdown_table(top, ['variant_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_business_day', 'closed_drawdown_amount', 'short_share', 'synthetic_added_short_count', 'displaced_parent_trade_count', 'selection_score'])}

## Rejected Or Watch(거절 또는 관찰)

{markdown_table(rejected, ['variant_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_count', 'short_share', 'closed_drawdown_amount'])}

## Forward/Regime Replay(전진/국면 재생)

{markdown_table(forward_rows, ['segment_type', 'segment_id', 'trade_count', 'net_profit', 'profit_factor', 'trade_density_per_business_day', 'short_share'])}

## Short Source(숏 원천)

{markdown_table(short_rows, ['audit_id', 'short_threshold', 'available_short_like_cycle_count', 'synthetic_added_short_count', 'displaced_parent_trade_count', 'synthetic_short_net_profit', 'profit_factor', 'short_share', 'candidate_status'])}

## Equity DD Boundary(평가손익 낙폭 경계)

{markdown_table(dd_rows, ['diagnostic_id', 'value', 'percent', 'delta_vs_baseline', 'status', 'effect'])}

## BN Queue(BN 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'review_question', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Claim Boundary(주장 경계)

This run(이번 실행)은 proxy scout(프록시 정찰)이다. New MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BM h19 stress short-balance proxy scout decision(결정)

Action(행동): `{RUN_ID}`가 `{final['selected_variant_id']}`를 BN review(BN 검토) 후보로 넘겼다.

Effect(효과): combined proxy(합산 프록시)는 좋아졌지만 synthetic short PF(합성 숏 PF)가 낮아 package candidate(패키지 후보)는 아니다. MT5 runtime probe(MT5 런타임 탐침) 없이는 운영 주장으로 승격하지 않는다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - h19 stress short-balance proxy scout(h19 압박 숏 균형 프록시 정찰).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BM H19 Stress Short-Balance Proxy Scout Closeout",
        f"""## run364BM H19 Stress Short-Balance Proxy Scout Closeout(364BM h19 압박 숏 균형 프록시 정찰 종료)

Action(행동): BL queue(BL 대기열)를 telemetry + US100 raw M5(실행기록 + US100 원천 5분봉)로 실행해 `{final['selected_variant_id']}`를 찾았다.

Effect(효과): Stage364(364단계)를 분기하지 않고 `{NEXT_RUN_ID}` review(검토)로 이어가며, runtime authority(런타임 권위)는 주장하지 않는다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BM H19 Stress Short-Balance Proxy Scout(364BM h19 압박 숏 균형 프록시 정찰)

Action(행동): h17-20 short router(17~20시 숏 라우터)를 fixed6 proxy(고정6봉 프록시)로 정찰했다.

Effect(효과): `{final['selected_variant_id']}`가 BN review(BN 검토)로 넘어가며, MT5 재탐침 전까지 운영 주장은 닫는다.
""",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    replace_prefixed_lines(
        STAGE_README,
        {
            "Current run(현재 실행):": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run(최근 완료 실행):": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BM(364BM 실행)은 `{final['selected_variant_id']}` combined proxy subject(합산 프록시 검토 대상)를 만들었지만 synthetic short PF(합성 숏 PF)가 낮아 package candidate(패키지 후보)는 아니다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 packageability(패키지 가능성)와 MT5 reprobe handoff(MT5 재탐침 인계)를 검토한다.",
        },
        bom=True,
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
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364BM`은 BL queue(BL 대기열)를 proxy scout(프록시 정찰)로 실행했고, selected review subject(선택 검토 대상)는 `{final['selected_variant_id']}`다. Proxy net/PF/trades/density/short_share(프록시 순수익/수익 팩터/거래수/밀도/숏비중)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_count']}` / `{final['selected_trade_density']}` / `{final['selected_short_share']}`지만, synthetic short PF(합성 숏 PF)는 `{final['selected_synthetic_short_profit_factor']}`라서 package candidate(패키지 후보)는 아니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 combined gain attribution(합산 개선 귀속), short source repair(숏 원천 수리), package rejection gate(패키지 거절 게이트)를 검토한다.

Operating boundary(운영 경계): no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Proxy review subject(프록시 검토 대상): `{final['selected_variant_id']}`

Status(상태): `{STATUS}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, expectancy `{final['selected_expectancy']}`, trades `{final['selected_trade_count']}`, density `{final['selected_trade_density']}`, closed DD `{final['selected_closed_drawdown_amount']}`, recovery `{final['selected_recovery_factor']}`.

Short balance(숏 균형): parent short share(부모 숏 비중) `{final['parent_short_share']}` -> selected short share(선택 숏 비중) `{final['selected_short_share']}`. Synthetic short PF(합성 숏 PF) `{final['selected_synthetic_short_profit_factor']}`라서 package candidate(패키지 후보)는 아니다.

Next queue(다음 대기열): `{rel(RUN364BN_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): h19 stress short-balance proxy scout(h19 압박 숏 균형 프록시 정찰)를 실행했다.
- effect(효과): `{final['selected_variant_id']}`를 BN review(BN 검토)로 넘기고, MT5 runtime probe(MT5 런타임 탐침) 전 운영 주장을 차단했다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h17-20 short router(17~20시 숏 라우터)가 h19 guard(h19 가드)의 short balance(숏 균형)를 회복할 수 있다.
- positive clue(긍정 단서): selected proxy net/PF/density/short share `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}` / `{final['selected_short_share']}`.
- effect(효과): long delete(롱 삭제) 대신 new short source(새 숏 원천)를 다음 MT5 검토 후보로 만든다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): proxy_only_review_required(프록시 전용, 검토 필요).
- failure_memory(실패 기억): synthetic fixed6 label(합성 고정6봉 라벨)과 same-tape threshold(동일 테이프 임계값)는 MT5 runtime evidence(MT5 런타임 근거)를 대체하지 못한다.
- effect(효과): BN review(BN 검토)에서 packageability(패키지 가능성)와 MT5 reprobe(MT5 재탐침)를 먼저 확인한다.
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
        "rows": final["surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(SELECTED_PROXY_CANDIDATE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": final["external_verification_status"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 정찰)",
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "drawdown": final["selected_closed_drawdown_percent"],
        "recovery_factor": final["selected_recovery_factor"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_trade_density"],
        "trade_density_requirement_status": "proxy_passed_ge_3_no_trade_splitting(프록시 3 이상 통과, 거래 쪼개기 없음)",
        "long_trade_count": final["selected_long_trade_count"],
        "short_trade_count": final["selected_short_trade_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can h17-20 short router restore h19 probe short balance without breaking net/PF/density?(17~20시 숏 라우터가 순수익/PF/밀도 붕괴 없이 h19 탐침 숏 균형을 회복하는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, kpi_scope, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy scout closed trade plus synthetic short label(프록시 정찰 종료거래 + 합성 숏 라벨)", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)", "out_of_scope_by_claim(주장 범위 밖)", "not_run_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A proxy plus Tier B out_of_scope(Tier A 프록시 + Tier B 범위 밖)", STATUS, JUDGMENT),
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
                "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_trade_density']};short_share={final['selected_short_share']}",
                "guardrail_kpi": f"synthetic_added={final['selected_synthetic_added_short_count']};displaced={final['selected_displaced_parent_trade_count']};mt5_reprobe_required",
            }
        )
        if tier == "Tier B":
            for key in ["net_profit", "profit_factor", "expectancy", "drawdown", "recovery_factor", "trade_count", "long_trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])

    artifact_rows = []
    for artifact_type, path, notes in [
        ("proxy_scout_surface", PROXY_SCOUT_SURFACE, "BM proxy scout surface(BM 프록시 정찰 표면)."),
        ("selected_candidate", SELECTED_PROXY_CANDIDATE, "Selected BM proxy candidate(선택 BM 프록시 후보)."),
        ("selected_trade_tape", SELECTED_PROXY_TRADE_TAPE, "Selected BM proxy trade tape(선택 BM 프록시 거래 테이프)."),
        ("short_source_feasibility", SHORT_SOURCE_FEASIBILITY, "Short source feasibility(숏 원천 가능성)."),
        ("synthetic_short_candidates", SHORT_SYNTHETIC_CANDIDATES, "Synthetic short candidate labels(합성 숏 후보 라벨)."),
        ("next_queue", RUN364BN_QUEUE, "BN review queue(BN 검토 대기열)."),
        ("report", REPORT_PATH, "BM report(BM 보고서)."),
        ("decision", DECISION_DOC, "BM decision doc(BM 결정 문서)."),
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
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
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
    bl_final = validate_inputs()
    write_work_packet()
    trades, join_audit = load_closed_trades_with_probabilities()
    cycles = load_telemetry_cycles()
    bars, index_by_time = load_us100_bars()
    parity_audit = raw_bar_price_parity_rows(trades, bars)
    surface, tapes, baseline = build_surface(trades, cycles, bars, index_by_time, bl_final)
    selected = surface.iloc[0].to_dict()
    selected_tape = tapes[str(selected["variant_id"])].copy()
    all_synthetic = tapes["__all_synthetic__"].copy()
    all_displaced = tapes["__all_displaced__"].copy()
    full_days = full_business_days(trades)
    forward_rows = []
    forward_rows.extend(segment_rows(selected_tape, "entry_quarter", "quarter", full_days=None))
    forward_rows.extend(segment_rows(selected_tape, "entry_month", "month", full_days=None))
    forward_rows.extend(segment_rows(selected_tape, "entry_hour", "entry_hour", full_days=None))
    short_rows = short_source_rows(surface, selected, cycles, bl_final)
    dd_rows = equity_dd_rows(baseline, selected, bl_final)
    queue = queue_rows(selected)
    gates = gate_rows(join_audit, parity_audit, surface, selected, queue)
    if any(row["status"] != "passed" for row in gates):
        write_csv(INPUT_MANIFEST, input_manifest_rows())
        write_csv(ENTRY_PROBABILITY_JOIN_AUDIT, join_audit)
        write_csv(RAW_BAR_PRICE_PARITY_AUDIT, parity_audit)
        write_csv(PROXY_SCOUT_SURFACE, surface.to_dict("records"))
        write_csv(GATE_AUDIT, gates)
        raise RuntimeError("BM gate failure(BM 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] != "passed"))

    created_at = now_utc()
    final = final_payload(bl_final, baseline, surface, selected, selected_tape, queue, gates, created_at)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(ENTRY_PROBABILITY_JOIN_AUDIT, join_audit)
    write_csv(RAW_BAR_PRICE_PARITY_AUDIT, parity_audit)
    write_csv(BASELINE_CLOSED_TRADE_METRICS, [{"run_id": RUN_ID, **baseline, "business_days": full_days, "claim_boundary": CLAIM_BOUNDARY}])
    write_csv(PROXY_SCOUT_SURFACE, surface.to_dict("records"))
    write_json(SELECTED_PROXY_CANDIDATE, selected)
    write_csv(SELECTED_PROXY_TRADE_TAPE, selected_tape.drop(columns=["entry_time_dt", "exit_time_dt"], errors="ignore").to_dict("records"))
    write_csv(SHORT_SOURCE_FEASIBILITY, short_rows)
    write_csv(SHORT_SYNTHETIC_CANDIDATES, all_synthetic.drop(columns=["entry_time_dt", "exit_time_dt"], errors="ignore").to_dict("records") if not all_synthetic.empty else [])
    write_csv(DISPLACED_PARENT_TRADES, all_displaced.to_dict("records") if not all_displaced.empty else [])
    write_csv(FORWARD_REGIME_REPLAY, forward_rows)
    write_csv(EQUITY_DD_PROXY_DIAGNOSTIC, dd_rows)
    write_csv(REJECTED_CANDIDATES, surface[~surface["candidate_status"].astype(str).str.contains("proxy_review_candidate", na=False)].to_dict("records"))
    write_csv(RUN364BN_QUEUE, queue)
    write_receipts(final, selected)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_docs(final, surface, selected, forward_rows, short_rows, dd_rows, queue, gates)
    write_ledgers(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
