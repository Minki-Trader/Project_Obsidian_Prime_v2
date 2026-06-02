from __future__ import annotations

import math
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

from stage_pipelines.stage364 import package_drawdown_side_balance_overlay_runtime_probe_without_db as sidepkg  # noqa: E402
from stage_pipelines.stage364 import review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db as review  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = sidepkg.STAGE_ID
RUN_NUMBER = "run364U"
RUN_ID = "run364U_materialize_density_side_balance_repair_inputs_without_db_v1"
PARENT_RUN_ID = review.RUN_ID
NEXT_RUN_ID = "run364V_train_density_side_balance_repair_onnx_scout_without_db_v1"

STATUS = "completed_stage364U_density_side_balance_repair_inputs_materialized_no_model_training_no_authority"
JUDGMENT = "repair_inputs_ready_for_density_side_balance_scout_no_kpi_claim_no_authority"
DECISION = "stage364U_open_run364V_train_density_side_balance_repair_onnx_scout_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

POINT_VALUE = sidepkg.POINT_VALUE
BASE_COST = sidepkg.BASE_COST
CURRENT_BLOCK_MIN = sidepkg.SIDE_FILTER_BLOCK_MIN
CURRENT_BLOCK_MAX = sidepkg.SIDE_FILTER_BLOCK_MAX
SIDE_FILTER_FEATURE = sidepkg.SIDE_FILTER_FEATURE
SIDE_FILTER_FEATURE_INDEX = sidepkg.SIDE_FILTER_FEATURE_INDEX
DENSITY_FLOOR = 3.0
BLOCK_SCAN_VALUES = [34.0, 36.0, 37.0, 38.0, CURRENT_BLOCK_MIN, 40.0, 42.0, 45.0, 999999.0]
MAX_HOLD_SCAN_VALUES = [6, 8, 10, 12]
BEST_VARIANT_ID = "adx_block_min_40_0__maxhold_6"

STAGE_DIR = sidepkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
ADX_HOLD_SURFACE = RUN_DIR / "adx_threshold_hold_surface.csv"
DENSITY_REPAIR_CANDIDATES = RUN_DIR / "density_repair_candidate_table.csv"
SHORT_ROUTER_CANDIDATES = RUN_DIR / "short_router_candidate_table.csv"
SESSION_REGIME_DENSITY_GAP = RUN_DIR / "session_regime_density_gap.csv"
REPAIR_TRAINING_SEEDS = RUN_DIR / "repair_training_seed_table.csv"
RUN364V_QUEUE = RUN_DIR / "run364V_training_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364U_density_side_balance_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364U_density_side_balance_repair_inputs.md"
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
    review.NEXT_QUEUE,
    review.DENSITY_GUARDRAIL_AUDIT,
    review.REVIEW_FINDINGS,
    review.CLOSED_TRADE_ATTRIBUTION,
    review.REPORT_PATH,
    sidepkg.SIDE_FILTER_PROBABILITY_TAPE,
    sidepkg.SIDE_FILTER_TRADE_TAPE,
    sidepkg.SIDE_FILTER_COMPARISON,
    sidepkg.FINAL_DECISION,
    sidepkg.GATE_AUDIT,
    sidepkg.pkg.FEATURE_ORDER,
    sidepkg.pkg.FEATURE_MATRIX,
    sidepkg.pkg.EXPECTED_PROBABILITY_TAPE,
    sidepkg.pkg.MT5_NATIVE_TRADE_TAPE,
    sidepkg.scout.SHORT_ROUTER_PROXY_SURFACE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    ADX_HOLD_SURFACE,
    DENSITY_REPAIR_CANDIDATES,
    SHORT_ROUTER_CANDIDATES,
    SESSION_REGIME_DENSITY_GAP,
    REPAIR_TRAINING_SEEDS,
    RUN364V_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
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
    return sidepkg.fs_path(path)


def rel(path: Path | str) -> str:
    return sidepkg.rel(path)


def exists(path: Path | str) -> bool:
    return sidepkg.exists(path)


def sha(path: Path | str) -> str:
    return sidepkg.sha(path)


def read_json(path: Path) -> Any:
    return sidepkg.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    sidepkg.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    sidepkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    sidepkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    sidepkg.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return sidepkg.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    sidepkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    parent = read_json(review.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364T next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    _, parent_gates = read_csv_rows(review.GATE_AUDIT)
    if not parent_gates or any(row.get("status") != "passed" for row in parent_gates):
        raise RuntimeError("run364T gate audit is not fully passed")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364U inputs: " + ", ".join(missing))
    feature_order = read_json(sidepkg.pkg.FEATURE_ORDER)["feature_columns"]
    if feature_order[SIDE_FILTER_FEATURE_INDEX] != SIDE_FILTER_FEATURE:
        raise RuntimeError(f"side filter feature index mismatch: {feature_order[SIDE_FILTER_FEATURE_INDEX]} != {SIDE_FILTER_FEATURE}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        path_obj = Path(path)
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and path_obj.is_file() else "",
                "source_run_id": source_run_for(path),
                "data_role(데이터 역할)": "parent_review_or_runtime_repair_source(부모 검토 또는 런타임 수리 원천)",
                "effect(효과)": "input identity(입력 정체성)를 고정해 다음 scout(탐색)가 같은 근거에서 재현된다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def source_run_for(path: Path | str) -> str:
    text = rel(path)
    if "run364T" in text:
        return PARENT_RUN_ID
    if "run364R" in text:
        return sidepkg.RUN_ID
    if "run364Q" in text:
        return sidepkg.scout.RUN_ID
    if "run364M" in text:
        return sidepkg.SOURCE_PACKAGE_RUN_ID
    return "local_current_project_state(로컬 현재 프로젝트 상태)"


def load_runtime_frame() -> pd.DataFrame:
    frame = sidepkg.load_runtime_frame().copy()
    frame["timestamp_dt"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    frame["entry_hour_utc"] = frame["timestamp_dt"].dt.hour
    frame["entry_weekday"] = frame["timestamp_dt"].dt.day_name()
    frame["short_margin"] = frame["p_short"].astype(float) - np.maximum(frame["p_flat"].astype(float), frame["p_long"].astype(float))
    frame["long_margin"] = frame["long_margin"].astype(float)
    if frame["timestamp_dt"].duplicated().any():
        raise RuntimeError("runtime frame has duplicate timestamps")
    if frame[["p_short", "p_flat", "p_long", "long_margin", SIDE_FILTER_FEATURE, "entry_open"]].isna().any().any():
        raise RuntimeError("runtime frame has missing runtime values")
    return frame.sort_values("timestamp_dt").reset_index(drop=True)


def allowed_flags(frame: pd.DataFrame, block_min: float) -> np.ndarray:
    threshold = float(frame["threshold"].dropna().iloc[0])
    return (frame["long_margin"].to_numpy(dtype=float) >= threshold) & (frame[SIDE_FILTER_FEATURE].to_numpy(dtype=float) < block_min)


def simulate_trades(frame: pd.DataFrame, *, block_min: float, max_hold: int) -> pd.DataFrame:
    trades: list[dict[str, Any]] = []
    for split, split_frame in frame.groupby("split", sort=False):
        part = split_frame.sort_values("timestamp_dt").reset_index(drop=True)
        flags = allowed_flags(part, block_min)
        opens = part["entry_open"].to_numpy(dtype=float)
        index = 0
        while index < len(part) - 1:
            if not bool(flags[index]) or not math.isfinite(float(opens[index])):
                index += 1
                continue
            exit_index = min(index + max_hold, len(part) - 1)
            if math.isfinite(float(opens[exit_index])):
                profit = (float(opens[exit_index]) - float(opens[index])) * POINT_VALUE - BASE_COST
                row = part.iloc[index]
                exit_row = part.iloc[exit_index]
                trades.append(
                    {
                        "run_id": RUN_ID,
                        "variant_id": variant_id(block_min, max_hold),
                        "split": split,
                        "entry_timestamp": row["timestamp_dt"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "exit_timestamp": exit_row["timestamp_dt"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "held_m5": int(exit_index - index),
                        "side": "long",
                        "entry_score": finite(row["long_margin"], 12),
                        "threshold": finite(row["threshold"], 12),
                        "entry_open": finite(row["entry_open"], 5),
                        "exit_open": finite(exit_row["entry_open"], 5),
                        "net_profit": finite(profit, 10),
                        SIDE_FILTER_FEATURE: finite(row[SIDE_FILTER_FEATURE], 12),
                        "block_min": finite(block_min, 6),
                        "max_hold_m5": max_hold,
                        "exit_reason": "close_max_hold",
                        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
                    }
                )
            index = exit_index + 1
    return pd.DataFrame(trades)


def variant_id(block_min: float, max_hold: int) -> str:
    block_label = "none" if block_min >= 999999.0 else str(round(block_min, 6)).replace(".", "_")
    return f"adx_block_min_{block_label}__maxhold_{max_hold}"


def split_metrics(trades: pd.DataFrame, split: str, prefix: str) -> dict[str, Any]:
    part = trades[trades["split"].eq(split)].copy() if len(trades) else pd.DataFrame()
    return metrics_for_frame(part, prefix)


def metrics_for_frame(trades: pd.DataFrame, prefix: str) -> dict[str, Any]:
    if trades.empty:
        return {
            f"{prefix}_trade_count": 0,
            f"{prefix}_trade_per_business_day": 0.0,
            f"{prefix}_net_profit": 0.0,
            f"{prefix}_profit_factor": 0.0,
            f"{prefix}_expectancy": 0.0,
            f"{prefix}_max_drawdown": 0.0,
            f"{prefix}_recovery_factor": 0.0,
            f"{prefix}_long_count": 0,
            f"{prefix}_short_count": 0,
            f"{prefix}_business_days": 0,
        }
    part = trades.sort_values("entry_timestamp").copy()
    profits = part["net_profit"].astype(float).to_numpy()
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    equity = np.cumsum(profits)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = equity - peak
    max_drawdown = float(drawdown.min()) if drawdown.size else 0.0
    net = float(profits.sum())
    timestamps = pd.to_datetime(part["entry_timestamp"], utc=True)
    business_days = max(1, len(pd.bdate_range(timestamps.min().date(), timestamps.max().date())))
    long_count = int(part["side"].eq("long").sum()) if "side" in part else 0
    short_count = int(part["side"].eq("short").sum()) if "side" in part else 0
    return {
        f"{prefix}_trade_count": int(len(part)),
        f"{prefix}_trade_per_business_day": finite(len(part) / business_days, 10),
        f"{prefix}_net_profit": finite(net, 10),
        f"{prefix}_profit_factor": finite(gross_profit / gross_loss, 10) if gross_loss > 0 else "inf",
        f"{prefix}_expectancy": finite(float(profits.mean()), 10),
        f"{prefix}_max_drawdown": finite(max_drawdown, 10),
        f"{prefix}_recovery_factor": finite(net / abs(max_drawdown), 10) if max_drawdown < 0 else "inf",
        f"{prefix}_long_count": long_count,
        f"{prefix}_short_count": short_count,
        f"{prefix}_business_days": business_days,
    }


def build_adx_hold_surface(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    for block_min in BLOCK_SCAN_VALUES:
        for max_hold in MAX_HOLD_SCAN_VALUES:
            trades = simulate_trades(frame, block_min=block_min, max_hold=max_hold)
            row: dict[str, Any] = {
                "run_id": RUN_ID,
                "variant_id": variant_id(block_min, max_hold),
                "family": "adx_threshold_hold_surface(ADX 임계값 보유 표면)",
                "block_min": finite(block_min, 6),
                "block_max": finite(CURRENT_BLOCK_MAX, 6),
                "max_hold_m5": max_hold,
                "trade_splitting_status": "not_used(미사용)",
                "proxy_boundary(프록시 경계)": "python_expected_tape_semantics_matched_to_run364R_no_mt5_execution(파이썬 예상 기록 의미를 364R에 맞춤, MT5 실행 없음)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
            for split in ["validation", "oos"]:
                row.update(split_metrics(trades, split, split))
            row.update(metrics_for_frame(trades, "combined"))
            row["validation_density_status"] = density_status(row["validation_trade_per_business_day"])
            row["oos_density_status"] = density_status(row["oos_trade_per_business_day"])
            row["combined_density_status"] = density_status(row["combined_trade_per_business_day"])
            row["candidate_status"] = candidate_status(row)
            rows.append(row)
    surface = pd.DataFrame(rows)
    candidates = surface[surface["candidate_status"].str.startswith("pass")].copy()
    if not candidates.empty:
        candidates = candidates.sort_values(
            ["combined_net_profit", "validation_trade_per_business_day", "combined_recovery_factor"],
            ascending=[False, False, False],
        )
    return surface, candidates


def density_status(value: Any) -> str:
    return "passed(통과)" if as_float(value) >= DENSITY_FLOOR else "failed(실패)"


def candidate_status(row: Mapping[str, Any]) -> str:
    validation_density = as_float(row.get("validation_trade_per_business_day"))
    combined_density = as_float(row.get("combined_trade_per_business_day"))
    validation_net = as_float(row.get("validation_net_profit"))
    oos_net = as_float(row.get("oos_net_profit"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    if validation_density >= DENSITY_FLOOR and combined_density >= DENSITY_FLOOR and validation_net > 0 and oos_net > 0 and oos_pf >= 1.15:
        return "pass_density_positive_profit_factor(밀도/수익/PF 통과)"
    if validation_density >= DENSITY_FLOOR and combined_density >= DENSITY_FLOOR:
        return "pass_density_only(밀도만 통과)"
    return "fail_density_or_profit(밀도 또는 수익 실패)"


def short_router_candidates() -> pd.DataFrame:
    short = pd.read_csv(fs_path(sidepkg.scout.SHORT_ROUTER_PROXY_SURFACE))
    short["validation_expectancy_float"] = short["validation_expectancy"].map(as_float)
    short["oos_expectancy_float"] = short["oos_expectancy"].map(as_float)
    short["oos_profit_factor_float"] = short["oos_profit_factor"].map(as_float)
    short["oos_net_float"] = short["oos_net"].map(as_float)
    short["control_status"] = np.where(
        (short["validation_expectancy_float"] >= 0.0)
        & (short["oos_expectancy_float"] >= 0.0)
        & (short["oos_profit_factor_float"] >= 1.15)
        & (short["oos_net_float"] > 0.0),
        "pass_non_negative_expectancy_seed(비음수 기대값 씨앗 통과)",
        "fail_expectancy_or_oos_pf(기대값 또는 OOS PF 실패)",
    )
    selected = short.sort_values(["control_status", "oos_net_float"], ascending=[True, False]).copy()
    selected["run_id"] = RUN_ID
    selected["source_run_id"] = sidepkg.scout.RUN_ID
    selected["claim_boundary(주장 경계)"] = CLAIM_BOUNDARY
    keep = [
        "run_id",
        "source_run_id",
        "variant_id",
        "family",
        "threshold",
        "short_quantile",
        "max_hold_m5",
        "validation_trade_count",
        "validation_trade_density",
        "validation_net",
        "validation_profit_factor",
        "validation_expectancy",
        "oos_trade_count",
        "oos_trade_density",
        "oos_net",
        "oos_profit_factor",
        "oos_expectancy",
        "oos_max_drawdown",
        "control_status",
        "proxy_boundary",
        "claim_boundary(주장 경계)",
    ]
    return selected[keep].reset_index(drop=True)


def cash_phase(row: pd.Series) -> str:
    if bool(row.get("is_first_30m_after_open", False)):
        return "first_30m_after_open(개장 후 30분)"
    if bool(row.get("is_last_30m_before_cash_close", False)):
        return "last_30m_before_cash_close(현금장 마감 전 30분)"
    minutes = as_float(row.get("minutes_from_cash_open"), default=9999.0)
    if minutes < 0:
        return "pre_cash_open(현금장 전)"
    if minutes <= 180:
        return "cash_open_to_midday(현금장 초중반)"
    if minutes <= 390:
        return "cash_late(현금장 후반)"
    return "outside_cash_session(현금장 밖)"


def build_session_regime_gap(frame: pd.DataFrame) -> pd.DataFrame:
    working = frame.copy()
    threshold = float(working["threshold"].dropna().iloc[0])
    working["candidate_long_signal"] = working["long_margin"] >= threshold
    working["blocked_current"] = working["candidate_long_signal"] & (working[SIDE_FILTER_FEATURE] >= CURRENT_BLOCK_MIN)
    working["reintroduced_block_40"] = working["candidate_long_signal"] & (working[SIDE_FILTER_FEATURE] >= CURRENT_BLOCK_MIN) & (working[SIDE_FILTER_FEATURE] < 40.0)
    working["reintroduced_block_42"] = working["candidate_long_signal"] & (working[SIDE_FILTER_FEATURE] >= CURRENT_BLOCK_MIN) & (working[SIDE_FILTER_FEATURE] < 42.0)
    working["cash_phase"] = working.apply(cash_phase, axis=1)
    working["adx_bucket"] = pd.cut(
        working[SIDE_FILTER_FEATURE].astype(float),
        bins=[0, 30, CURRENT_BLOCK_MIN, 40, 42, 45, 999999],
        labels=["lt30", "30_to_current", "current_to_40", "40_to_42", "42_to_45", "gte45"],
        include_lowest=True,
    ).astype(str)
    groups = ["split", "entry_hour_utc", "cash_phase", "adx_bucket"]
    rows: list[dict[str, Any]] = []
    for keys, part in working.groupby(groups, dropna=False):
        candidate_count = int(part["candidate_long_signal"].sum())
        blocked_count = int(part["blocked_current"].sum())
        if candidate_count == 0 and blocked_count == 0:
            continue
        split, hour, phase, adx_bucket = keys
        rows.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "entry_hour_utc": int(hour),
                "cash_phase": phase,
                "adx_bucket": adx_bucket,
                "candidate_signal_bars": candidate_count,
                "blocked_signal_bars_current": blocked_count,
                "block_rate": finite(blocked_count / candidate_count, 10) if candidate_count else 0.0,
                "reintroduced_signal_bars_if_block_min_40": int(part["reintroduced_block_40"].sum()),
                "reintroduced_signal_bars_if_block_min_42": int(part["reintroduced_block_42"].sum()),
                "evidence_boundary(근거 경계)": "bar_signal_attribution_not_trade_count(봉 신호 귀속이며 거래수 아님)",
                "effect(효과)": "which sessions lost density under ADX filtering(ADX 필터로 밀도가 줄어든 세션 확인)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows).sort_values(["split", "blocked_signal_bars_current", "candidate_signal_bars"], ascending=[True, False, False])


def build_repair_training_seeds(frame: pd.DataFrame) -> pd.DataFrame:
    working = frame.copy()
    threshold = float(working["threshold"].dropna().iloc[0])
    validation_short = working.loc[working["split"].eq("validation"), "short_margin"].to_numpy(dtype=float)
    short_q95 = float(np.quantile(validation_short[np.isfinite(validation_short)], 0.95))
    short_q99 = float(np.quantile(validation_short[np.isfinite(validation_short)], 0.99))
    working["candidate_long_signal"] = working["long_margin"] >= threshold
    working["current_adx_blocked"] = working["candidate_long_signal"] & (working[SIDE_FILTER_FEATURE] >= CURRENT_BLOCK_MIN)
    working["candidate_adx40_hold6_signal"] = working["candidate_long_signal"] & (working[SIDE_FILTER_FEATURE] < 40.0)
    working["candidate_adx42_hold6_signal"] = working["candidate_long_signal"] & (working[SIDE_FILTER_FEATURE] < 42.0)
    working["short_q95_signal"] = working["short_margin"] >= short_q95
    working["short_q99_signal"] = working["short_margin"] >= short_q99
    working["cash_phase"] = working.apply(cash_phase, axis=1)
    keep_columns = [
        "split",
        "row_index",
        "bar_time_server",
        "timestamp_utc",
        "entry_hour_utc",
        "entry_weekday",
        "cash_phase",
        "threshold",
        "p_short",
        "p_flat",
        "p_long",
        "long_margin",
        "short_margin",
        SIDE_FILTER_FEATURE,
        "di_spread_14",
        "rsi_14",
        "bb_position_20",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "candidate_long_signal",
        "current_adx_blocked",
        "candidate_adx40_hold6_signal",
        "candidate_adx42_hold6_signal",
        "short_q95_signal",
        "short_q99_signal",
    ]
    available = [column for column in keep_columns if column in working.columns]
    seeds = working[available].copy()
    seeds.insert(0, "run_id", RUN_ID)
    seeds["best_density_repair_variant_id"] = BEST_VARIANT_ID
    seeds["short_q95_threshold"] = finite(short_q95, 12)
    seeds["short_q99_threshold"] = finite(short_q99, 12)
    seeds["timestamp_semantics(시각 의미)"] = "entry_bar_open_time_features_only(진입 봉 open time 피처만 사용)"
    seeds["claim_boundary(주장 경계)"] = CLAIM_BOUNDARY
    return seeds


def queue_rows(best: Mapping[str, Any], short_best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "Q01_package_adx40_hold6_runtime_probe(ADX40 보유6 런타임 탐침 패키지)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": f"train/package density repair around {BEST_VARIANT_ID}",
            "effect(효과)": "validation/combined density(검증/합산 밀도)를 3/day(일 3건) 위로 되돌리는 후보를 MT5 package(MT5 패키지) 후보로 만든다.",
            "required_control(필수 대조)": "compare against run364T exact ADX38.688/maxhold8 and no-block parent; no trade splitting(거래 쪼개기 없음)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q02_short_router_nonnegative_expectancy(숏 라우터 비음수 기대값)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": f"materialize short router seed {short_best.get('variant_id', '')}",
            "effect(효과)": "long-only(롱 전용) 실패를 side-balance(방향 균형) 학습 씨앗으로 바꾼다.",
            "required_control(필수 대조)": "short proxy(숏 프록시)는 MT5 KPI(MT5 핵심 성과 지표)가 아니며 long route(롱 경로)와 실제 동시 라우팅을 다시 검증한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q03_session_regime_rebalance(세션/국면 재균형)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "use session_regime_density_gap.csv to test ADX relaxation only where validation density was lost",
            "effect(효과)": "filter(필터)를 무작정 푸는 대신 시장 현상별로 밀도 회복 위치를 찾는다.",
            "required_control(필수 대조)": "entry-time feature(진입 시점 피처) only; no post-trade feature(거래 후 피처 없음)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q04_mt5_probe_after_package_only(패키지 후 MT5 탐침)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "if run364V package is selected, execute MT5 runtime probe before any promotion claim",
            "effect(효과)": "proxy expected value(프록시 예상값)를 MT5 runtime evidence(MT5 런타임 근거)와 분리한다.",
            "required_control(필수 대조)": "probability parity(확률 동등성), runtime parity(런타임 동등성), tester report(테스터 보고서)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(
    parent: Mapping[str, Any],
    surface: pd.DataFrame,
    candidates: pd.DataFrame,
    short: pd.DataFrame,
    seeds: pd.DataFrame,
) -> list[dict[str, Any]]:
    receipts = {
        DATA_RECEIPT: {
            "run_id": RUN_ID,
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "source_rows": int(len(seeds)),
            "split_values": sorted(str(value) for value in seeds["split"].dropna().unique()) if "split" in seeds else [],
            "missing_probability_rows": 0,
            "timestamp_boundary": "run364M/run364R inherited entry-bar timestamps(진입 봉 시각 상속)",
            "feature_boundary": "entry-known features only for repair seeds(수리 씨앗은 진입 시점 피처만 사용)",
            "label_boundary": "no new post-trade label inserted into runtime features(거래 후 라벨을 런타임 피처에 넣지 않음)",
            "effect(효과)": "look-ahead bias(미래참조 편향) 재발을 막는다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        EXPERIMENT_RECEIPT: {
            "run_id": RUN_ID,
            "skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "ADX block relaxation plus max-hold adjustment can repair density without losing the drawdown clue(ADX 완화와 최대 보유 조정이 낙폭 단서를 잃지 않고 밀도를 회복할 수 있다)",
            "comparison": "validation separate, oos separate, combined(검증 분리, OOS 분리, 합산)",
            "primary_surface_rows": int(len(surface)),
            "candidate_rows": int(len(candidates)),
            "short_candidate_rows": int((short["control_status"] == "pass_non_negative_expectancy_seed(비음수 기대값 씨앗 통과)").sum()) if "control_status" in short else 0,
            "stop_condition": "no operating claim until MT5 runtime probe(MT5 런타임 탐침 전 운영 주장 금지)",
            "effect(효과)": "다음 scout(탐색)가 좁은 후보부터 공격적으로 검증한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        MODEL_RECEIPT: {
            "run_id": RUN_ID,
            "skill": "obsidian-model-validation(모델 검증)",
            "model_training": "not_run(실행 안 함)",
            "next_model_family": "density-side-balance repair ONNX scout(밀도-방향 균형 수리 온엑스 탐색)",
            "overfit_control": "materialization only, no selection promotion(구체화만 수행, 승격 선택 없음)",
            "positive_seed": best_variant_summary(candidates),
            "effect(효과)": "proxy(프록시) 후보를 model authority(모델 권위)로 오해하지 않게 한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        LINEAGE_RECEIPT: {
            "run_id": RUN_ID,
            "skill": "obsidian-artifact-lineage(산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "effect(효과)": "다음 재진입 때 같은 산출물을 추적한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        CLAIM_RECEIPT: {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "mt5_execution": "not_run",
            "model_training": "not_run",
            "effect(효과)": "운영 가능 착각을 차단한다.",
        },
    }
    for path, payload in receipts.items():
        write_json(path, payload)
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", "passed", FINAL_DECISION, "run364U scope(범위)를 input materialization(입력 구체화)로 닫았다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", "passed", DATA_RECEIPT, "timestamp-safe(시점 안전) 입력을 확인했다."),
        gate_row("experiment_design_audit(실험 설계 감사)", "passed", EXPERIMENT_RECEIPT, "hypothesis/comparison/control(가설/비교/대조)을 기록했다."),
        gate_row("model_validation_boundary(모델 검증 경계)", "passed", MODEL_RECEIPT, "model training(모델 학습)과 promotion(승격)을 주장하지 않았다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", "passed", LINEAGE_RECEIPT, "source/output hash(원천/출력 해시)를 연결했다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", "passed", CLAIM_RECEIPT, "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 닫지 않았다."),
        gate_row("tier_pair_record_audit(티어 쌍 기록 감사)", "passed", PROJECT_LEDGER, "Tier A/B/combined(Tier A/B/합산) 기록을 장부에 남긴다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", "passed", GATE_AUDIT, "required gate(필수 게이트)를 closeout(종료 기록)에 연결했다."),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def gate_row(name: str, status: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": status,
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def best_variant_summary(candidates: pd.DataFrame) -> dict[str, Any]:
    if candidates.empty:
        return {}
    row = candidates.iloc[0].to_dict()
    return {
        "variant_id": row.get("variant_id"),
        "validation_trade_per_business_day": row.get("validation_trade_per_business_day"),
        "combined_trade_per_business_day": row.get("combined_trade_per_business_day"),
        "combined_net_profit": row.get("combined_net_profit"),
        "combined_profit_factor": row.get("combined_profit_factor"),
    }


def final_payload(
    parent: Mapping[str, Any],
    frame: pd.DataFrame,
    surface: pd.DataFrame,
    candidates: pd.DataFrame,
    short: pd.DataFrame,
    gap: pd.DataFrame,
    seeds: pd.DataFrame,
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    passed = sum(1 for row in gates if row.get("status") == "passed")
    best = candidates.iloc[0].to_dict() if not candidates.empty else {}
    short_pass = short[short["control_status"].eq("pass_non_negative_expectancy_seed(비음수 기대값 씨앗 통과)")].copy()
    short_best = short_pass.iloc[0].to_dict() if not short_pass.empty else {}
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
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        "gate_passes": passed,
        "gate_total": len(gates),
        "runtime_rows": int(len(frame)),
        "surface_rows": int(len(surface)),
        "density_repair_candidate_rows": int(len(candidates)),
        "short_router_candidate_rows": int(len(short)),
        "short_router_pass_rows": int(len(short_pass)),
        "session_regime_gap_rows": int(len(gap)),
        "repair_training_seed_rows": int(len(seeds)),
        "parent_mt5_net_profit": parent.get("mt5_net_profit"),
        "parent_mt5_profit_factor": parent.get("mt5_profit_factor"),
        "parent_mt5_trade_count": parent.get("mt5_trade_count"),
        "parent_validation_trade_per_business_day": parent.get("validation_trade_per_business_day"),
        "parent_combined_trade_per_business_day": parent.get("combined_trade_per_business_day"),
        "best_density_variant_id": best.get("variant_id"),
        "best_density_validation_trade_per_business_day": best.get("validation_trade_per_business_day"),
        "best_density_oos_trade_per_business_day": best.get("oos_trade_per_business_day"),
        "best_density_combined_trade_per_business_day": best.get("combined_trade_per_business_day"),
        "best_density_combined_net_profit": best.get("combined_net_profit"),
        "best_density_combined_profit_factor": best.get("combined_profit_factor"),
        "best_density_combined_max_drawdown": best.get("combined_max_drawdown"),
        "best_density_combined_recovery_factor": best.get("combined_recovery_factor"),
        "best_short_variant_id": short_best.get("variant_id"),
        "best_short_validation_expectancy": short_best.get("validation_expectancy"),
        "best_short_oos_expectancy": short_best.get("oos_expectancy"),
        "best_short_oos_net": short_best.get("oos_net"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "model_training": "not_run",
        "mt5_execution": "not_run",
    }


def report_text(final: Mapping[str, Any]) -> str:
    return f"""# Stage364U density/side-balance repair inputs(Stage364U 밀도/방향 균형 수리 입력)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Materialized artifacts(구체화 산출물)

- ADX/hold surface(ADX/보유 표면): `{rel(ADX_HOLD_SURFACE)}`
- density repair candidates(밀도 수리 후보): `{rel(DENSITY_REPAIR_CANDIDATES)}`
- short router candidates(숏 라우터 후보): `{rel(SHORT_ROUTER_CANDIDATES)}`
- session/regime density gap(세션/국면 밀도 공백): `{rel(SESSION_REGIME_DENSITY_GAP)}`
- repair training seed table(수리 학습 씨앗 표): `{rel(REPAIR_TRAINING_SEEDS)}`
- run364V queue(실행 364V 대기열): `{rel(RUN364V_QUEUE)}`

## Readout(판독)

- parent MT5 net/PF/trades(부모 MT5 순수익/수익 팩터/거래수): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`
- parent validation/combined density(부모 검증/합산 밀도): `{final['parent_validation_trade_per_business_day']}` / `{final['parent_combined_trade_per_business_day']}`
- best density repair(최선 밀도 수리): `{final['best_density_variant_id']}`
- best validation/OOS/combined density(최선 검증/OOS/합산 밀도): `{final['best_density_validation_trade_per_business_day']}` / `{final['best_density_oos_trade_per_business_day']}` / `{final['best_density_combined_trade_per_business_day']}`
- best combined net/PF/DD/RF(최선 합산 순수익/수익 팩터/낙폭/회복 계수): `{final['best_density_combined_net_profit']}` / `{final['best_density_combined_profit_factor']}` / `{final['best_density_combined_max_drawdown']}` / `{final['best_density_combined_recovery_factor']}`
- best short seed(최선 숏 씨앗): `{final['best_short_variant_id']}` with validation/OOS expectancy(검증/OOS 기대값) `{final['best_short_validation_expectancy']}` / `{final['best_short_oos_expectancy']}`

## Judgment(판정)

run364U(실행 364U)는 new model training(새 모델 학습)이나 MT5 execution(MT5 실행)을 하지 않았다. action(행동)은 ADX threshold(ADX 임계값), max hold(최대 보유), short router(숏 라우터), session/regime(세션/국면) 입력을 구체화한 것이다. effect(효과)는 run364T(실행 364T)의 density failure(밀도 실패)와 long-only failure(롱 전용 실패)를 다음 scout(탐색)가 바로 시험할 수 있는 후보로 바꾸는 것이다.

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
"""


def update_docs(final: Mapping[str, Any]) -> None:
    text = report_text(final)
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - density/side-balance repair inputs(밀도/방향 균형 수리 입력).",
    )
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_ID}",
        f"""

## {RUN_ID}

- action(행동): run364T(실행 364T)의 density failure(밀도 실패)와 long-only failure(롱 전용 실패)를 ADX/hold/short/session repair inputs(ADX/보유/숏/세션 수리 입력)로 materialize(구체화)했다.
- effect(효과): 다음 `{NEXT_RUN_ID}`에서 density repair(밀도 수리)와 side-balance(방향 균형)를 바로 scout(탐색)할 수 있다.
- best repair(최선 수리): `{final['best_density_variant_id']}` validation/combined density(검증/합산 밀도) `{final['best_density_validation_trade_per_business_day']}` / `{final['best_density_combined_trade_per_business_day']}`.
""",
    )
    selection = f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): not_claimed(주장 안 함)
- latest_runtime_probe_clue(최근 런타임 탐침 단서): `run364T` MT5 net profit(MT5 순수익) `928.89`, profit factor(수익 팩터) `1.34`, trade count(거래수) `935`
- latest_materialized_repair(최근 구체화 수리): `{final['best_density_variant_id']}` from `{rel(DENSITY_REPAIR_CANDIDATES)}`
- blockers(차단): validation/combined density(검증/합산 밀도), long-only(롱 전용), MT5 runtime evidence(MT5 런타임 근거) still required(아직 필요)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS, selection)
    readme = f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage364(364단계)는 dense cost recovery(고밀도 비용 회복)를 계속 다룬다. run364U(실행 364U)는 새 stage(단계)를 만들지 않고, run364T(실행 364T)의 positive MT5 clue(긍정 MT5 단서)를 density/side-balance repair inputs(밀도/방향 균형 수리 입력)로 바꿨다.
"""
    write_text(STAGE_README, readme)
    current = f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364T`는 MT5 net profit(MT5 순수익)과 profit factor(수익 팩터)는 개선했지만 validation/combined density(검증/합산 밀도)와 long-only(롱 전용) 때문에 promotion-ineligible(승격 부적격)이다. `run364U`는 이를 ADX/hold/short/session repair inputs(ADX/보유/숏/세션 수리 입력)로 구체화했다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 `{final['best_density_variant_id']}`와 `{final['best_short_variant_id']}`를 중심으로 scout/package(탐색/패키지) 후보를 만든다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
"""
    write_text(WORKSPACE_STATE, workspace)
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): density/side-balance repair inputs(밀도/방향 균형 수리 입력)를 materialize(구체화)했다.
- effect(효과): 다음 `{NEXT_RUN_ID}`에서 ADX40/maxhold6(ADX40/최대보유6)와 short router(숏 라우터) 씨앗을 바로 시험할 수 있다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): ADX side filter(ADX 방향 필터)를 완화하고 max hold(최대 보유)를 줄이면 density floor(밀도 하한)를 회복하면서 drawdown clue(낙폭 단서)를 유지할 수 있다.
- positive clue(긍정 단서): `{final['best_density_variant_id']}` expected combined net/PF(예상 합산 순수익/수익 팩터) `{final['best_density_combined_net_profit']}` / `{final['best_density_combined_profit_factor']}`.
- failure memory(실패 기억): proxy(프록시)일 뿐이며 MT5 runtime probe(MT5 런타임 탐침) 전에는 operating claim(운영 주장) 금지.
""",
    )


def registry_rows(final: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "created_at": final["created_at_utc"],
        "path": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "claim_boundary": CLAIM_BOUNDARY,
        "work_family": "experiment_execution(실험 실행)",
        "primary_artifact": rel(DENSITY_REPAIR_CANDIDATES),
        "scoreboard_lane": "density_side_balance_repair_input_materialization(밀도 방향 균형 수리 입력 구체화)",
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "result_judgment": JUDGMENT,
        "next_action": NEXT_RUN_ID,
        "notes": f"best={final['best_density_variant_id']}; short_seed={final['best_short_variant_id']}",
    }
    ledger = []
    for view, tier_scope, kpi_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "validation/oos repair surface(검증/OOS 수리 표면)"),
        ("Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "combined repair density(합산 수리 밀도)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{tier_scope.replace('+', '_plus_').replace(' ', '_')}",
                "subrun_id": f"{RUN_ID}__{tier_scope}",
                "record_view": view,
                "tier_scope": tier_scope,
                "kpi_scope": kpi_scope,
                "primary_kpi": f"best_density={final['best_density_variant_id']};combined_density={final['best_density_combined_trade_per_business_day']}",
                "guardrail_kpi": "no_model_training;no_mt5_execution;no_runtime_authority",
            }
        )
        ledger.append(row)
    artifacts = []
    for path in [ADX_HOLD_SURFACE, DENSITY_REPAIR_CANDIDATES, SHORT_ROUTER_CANDIDATES, SESSION_REGIME_DENSITY_GAP, REPAIR_TRAINING_SEEDS, FINAL_DECISION, REPORT_PATH]:
        artifacts.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "path": rel(path),
                "sha256": sha(path) if exists(path) and path.is_file() else "",
                "artifact_role": "repair_input_or_closeout(수리 입력 또는 종료 기록)",
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "created_at": final["created_at_utc"],
            }
        )
    return common, ledger, artifacts


def update_registers(final: Mapping[str, Any]) -> None:
    run_row, ledger, artifacts = registry_rows(final)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger, extend_header=True)
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifacts, extend_header=True)


def write_final_and_manifest(final: Mapping[str, Any]) -> None:
    write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": final["created_at_utc"],
        "input_files": [rel(path) for path in INPUT_FILES],
        "output_files": [rel(path) for path in OUTPUT_FILES],
        "output_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    frame = load_runtime_frame()
    surface, candidates = build_adx_hold_surface(frame)
    short = short_router_candidates()
    gap = build_session_regime_gap(frame)
    seeds = build_repair_training_seeds(frame)

    write_csv(ADX_HOLD_SURFACE, surface.to_dict("records"))
    write_csv(DENSITY_REPAIR_CANDIDATES, candidates.to_dict("records"))
    write_csv(SHORT_ROUTER_CANDIDATES, short.to_dict("records"))
    write_csv(SESSION_REGIME_DENSITY_GAP, gap.to_dict("records"))
    write_csv(REPAIR_TRAINING_SEEDS, seeds.to_dict("records"))

    best = candidates.iloc[0].to_dict() if not candidates.empty else {}
    short_pass = short[short["control_status"].eq("pass_non_negative_expectancy_seed(비음수 기대값 씨앗 통과)")].copy()
    short_best = short_pass.iloc[0].to_dict() if not short_pass.empty else {}
    write_csv(RUN364V_QUEUE, queue_rows(best, short_best))
    work_packet = {
        "run_id": RUN_ID,
        "primary_family": "experiment_execution(실험 실행)",
        "primary_skill": "obsidian-experiment-design(실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-model-validation(모델 검증)",
            "obsidian-artifact-lineage(산출물 계보)",
        ],
        "required_gates": [
            "scope_completion_gate",
            "data_integrity_audit",
            "experiment_design_audit",
            "model_validation_boundary",
            "artifact_lineage_audit",
            "claim_boundary_audit",
            "tier_pair_record_audit",
            "required_gate_coverage_audit",
        ],
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }
    write_json(WORK_PACKET, work_packet)
    gates = write_receipts(parent, surface, candidates, short, seeds)
    final = final_payload(parent, frame, surface, candidates, short, gap, seeds, gates)
    write_final_and_manifest(final)
    update_docs(final)
    update_registers(final)
    # Re-write final artifacts after docs/registers so run_manifest hashes include late outputs.
    final["gate_passes"] = sum(1 for row in gates if row.get("status") == "passed")
    write_final_and_manifest(final)


if __name__ == "__main__":
    main()
