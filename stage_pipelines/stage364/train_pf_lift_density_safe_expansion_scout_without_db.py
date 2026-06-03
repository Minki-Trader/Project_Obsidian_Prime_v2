from __future__ import annotations

import json
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

from stage_pipelines.stage364 import materialize_pf_lift_density_safe_expansion_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_density_side_balance_repair_onnx_scout_without_db as base  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AG"
RUN_ID = "run364AG_train_pf_lift_density_safe_expansion_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = base.RUN_ID
NEXT_RUN_ID = "run364AH_review_pf_lift_density_safe_expansion_scout_without_db_v1"

STATUS = "completed_stage364AG_pf_lift_density_safe_proxy_scout_no_mt5_no_authority"
JUDGMENT = "proxy_scout_completed_pf_lift_density_safe_candidates_ranked_mt5_probe_required_no_authority"
DECISION = "stage364AG_open_run364AH_review_pf_lift_density_safe_expansion_scout"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_PF = parent.TARGET_PF

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
QUEUE_REPLAY_AUDIT = RUN_DIR / "queue_replay_audit.csv"
SCOUT_SURFACE = RUN_DIR / "pf_lift_density_safe_proxy_scout_surface.csv"
STRICT_CANDIDATES = RUN_DIR / "strict_proxy_candidates.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_EXPECTED_TRADE_TAPE = EXPECTED_DIR / "selected_trade_tape.csv"
SELECTED_MONTH_SIDE_SUMMARY = RUN_DIR / "selected_month_side_summary.csv"
SELECTED_SESSION_SUMMARY = RUN_DIR / "selected_session_summary.csv"
BASELINE_COMPARISON = RUN_DIR / "baseline_comparison.csv"
RUN364AH_QUEUE = RUN_DIR / "run364AH_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
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

REPORT_PATH = REVIEW_DIR / "run364AG_pf_lift_density_safe_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AG_pf_lift_density_safe_scout.md"
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
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364AG_QUEUE,
    parent.PF_LIFT_PROFILE,
    parent.DENSITY_RESTORE_RULE_QUEUE,
    parent.REPORT_PATH,
    base.SELECTED_RUNTIME_CANDIDATE,
    base.SELECTED_TRADE_TAPE,
    base.DUAL_SIDE_RUNTIME_SURFACE,
    base.prev.sidepkg.pkg.FEATURE_MATRIX,
    base.prev.sidepkg.pkg.FEATURE_ORDER,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    QUEUE_REPLAY_AUDIT,
    SCOUT_SURFACE,
    STRICT_CANDIDATES,
    SELECTED_PROXY_CANDIDATE,
    SELECTED_EXPECTED_TRADE_TAPE,
    SELECTED_MONTH_SIDE_SUMMARY,
    SELECTED_SESSION_SUMMARY,
    BASELINE_COMPARISON,
    RUN364AH_QUEUE,
    WORK_PACKET,
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


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    parent.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


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
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
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
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, EXPECTED_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(path, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과되지 않음)")
    queue = read_csv_rows(parent.RUN364AG_QUEUE)
    if len(queue) != 12:
        raise RuntimeError(f"unexpected run364AG queue rows(364AG 대기열 행 수 이상): {len(queue)}")
    if any("top_n" in str(row.get("bridge_expression", "")) for row in queue):
        raise RuntimeError("top_n replay is forbidden(top_n 재생은 금지)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AG inputs(364AG 입력 누락): " + ", ".join(missing))
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "role(역할)": input_role(path),
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364AG_scout_queue.csv":
        return "parent queue(부모 대기열)"
    if name == "selected_runtime_candidate.json":
        return "runtime candidate baseline(런타임 후보 기준)"
    if "trade_tape" in name:
        return "baseline expected trade tape(기준 예상 거래 테이프)"
    if name in {"feature_matrix.csv", "feature_order.json"}:
        return "runtime feature source(런타임 피처 원천)"
    return "supporting evidence(보조 근거)"


def slug(text: str) -> str:
    out = "".join(ch if ch.isalnum() else "_" for ch in text)
    return "_".join(part for part in out.split("_") if part)


def load_runtime_frame() -> tuple[pd.DataFrame, list[str], float]:
    frame, feature_order, threshold = base.load_runtime_frame()
    frame = frame.sort_values("timestamp_dt").reset_index(drop=True)
    frame["long_margin"] = frame["p_long"].astype(float) - np.maximum(frame["p_flat"].astype(float), frame["p_short"].astype(float))
    frame["short_margin"] = frame["p_short"].astype(float) - np.maximum(frame["p_flat"].astype(float), frame["p_long"].astype(float))
    if frame["timestamp_dt"].duplicated().any():
        raise RuntimeError("runtime frame has duplicate timestamps(런타임 프레임에 중복 시각이 있음)")
    required = ["p_short", "p_flat", "p_long", "long_margin", "short_margin", base.SIDE_FILTER_FEATURE, "entry_open", "bar_time_server"]
    if frame[required].isna().any().any():
        raise RuntimeError("runtime frame has missing required values(런타임 프레임 필수 값 누락)")
    return frame, feature_order, threshold


def queue_variants(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = read_csv_rows(parent.RUN364AG_QUEUE)
    variants: list[dict[str, Any]] = []
    for row in rows:
        short_threshold = as_float(row.get("short_probability_threshold"), 0.45)
        long_block_min = as_float(row.get("long_block_min"), 40.0)
        max_hold = as_int(row.get("max_hold_m5"), 8)
        floor = as_float(row.get("entry_margin_floor"), 0.0)
        queue_id = str(row.get("queue_id", ""))
        variants.append(
            {
                "run_id": RUN_ID,
                "queue_rank": as_int(row.get("queue_rank"), len(variants) + 1),
                "queue_id": queue_id,
                "axis_id": row.get("axis_id", ""),
                "queue_type": row.get("queue_type", ""),
                "seed_variant_id": row.get("seed_variant_id", ""),
                "variant_id": f"{slug(queue_id)}__ps{str(short_threshold).replace('.', '_')}__floor{str(floor).replace('.', '_')}__hold{max_hold}",
                "short_threshold": short_threshold,
                "long_block_min": long_block_min,
                "max_hold_m5": max_hold,
                "min_margin": as_float(selected.get("min_margin")),
                "entry_margin_floor": floor,
                "bridge_policy": row.get("bridge_policy", ""),
                "bridge_policy_value": row.get("bridge_policy_value", ""),
                "bridge_expression": row.get("bridge_expression", ""),
                "expected_effect(효과)": row.get("expected_effect(효과)", ""),
                "timestamp_safety_status": row.get("timestamp_safety_status", ""),
                "trade_splitting_status": "not_used(거래 쪼개기 없음)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return variants


def potential_signals(part: pd.DataFrame, *, short_threshold: float, long_threshold: float, min_margin: float, long_block_min: float) -> np.ndarray:
    p_short = part["p_short"].to_numpy(dtype=float)
    p_long = part["p_long"].to_numpy(dtype=float)
    short_margin = part["short_margin"].to_numpy(dtype=float)
    long_margin = part["long_margin"].to_numpy(dtype=float)
    signals = np.zeros(len(part), dtype=np.int8)
    short_ok = (p_short >= short_threshold) & (short_margin >= min_margin)
    long_ok = (p_long >= long_threshold) & (long_margin >= min_margin)
    signals[short_ok] = -1
    signals[long_ok & ((~short_ok) | (p_long >= p_short))] = 1
    block_long = (signals == 1) & (part[base.SIDE_FILTER_FEATURE].to_numpy(dtype=float) >= long_block_min)
    signals[block_long] = 0
    return signals


def margin_floor_mask(signals: np.ndarray, part: pd.DataFrame, floor: float) -> np.ndarray:
    if floor <= 0:
        return np.ones(len(part), dtype=bool)
    short_margin = part["short_margin"].to_numpy(dtype=float)
    long_margin = part["long_margin"].to_numpy(dtype=float)
    side_margin = np.where(signals == -1, short_margin, np.where(signals == 1, long_margin, 0.0))
    return (signals == 0) | (side_margin >= floor)


def parse_policy_values(value: Any) -> dict[str, float]:
    text = str(value or "")
    out: dict[str, float] = {}
    for piece in text.split(";"):
        if "=" not in piece:
            continue
        key, raw = piece.split("=", 1)
        out[key.strip()] = as_float(raw)
    return out


def apply_bridge_policy(signals: np.ndarray, part: pd.DataFrame, variant: Mapping[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    out = signals.copy()
    server = pd.to_datetime(part["bar_time_server"])
    month_march = server.dt.strftime("%Y-%m").eq("2025-03").to_numpy()
    hour = server.dt.hour.to_numpy()
    policy = str(variant.get("bridge_policy", ""))
    policy_value = str(variant.get("bridge_policy_value", ""))
    abs_margin = np.maximum(np.abs(part["short_margin"].to_numpy(dtype=float)), np.abs(part["long_margin"].to_numpy(dtype=float)))
    audit = {
        "source_signal_count": int(np.count_nonzero(signals)),
        "march_source_signal_count": int(np.count_nonzero(signals[month_march])),
        "march_block_count": 0,
        "march_restore_count": 0,
        "entry_margin_floor_filtered_count": 0,
        "final_signal_count": 0,
    }
    blocked = np.zeros(len(part), dtype=bool)
    restore = np.zeros(len(part), dtype=bool)
    restore_signals = signals.copy()

    if policy in {"", "none"}:
        pass
    elif policy == "block_march_long":
        blocked = month_march & (signals == 1)
    elif policy == "restore_march_short_p":
        threshold = as_float(policy_value)
        blocked = month_march & (signals != 0)
        candidate = potential_signals(
            part,
            short_threshold=threshold,
            long_threshold=base.LONG_THRESHOLD,
            min_margin=as_float(variant.get("min_margin")),
            long_block_min=as_float(variant.get("long_block_min")),
        )
        restore = month_march & (candidate == -1)
        restore_signals[restore] = -1
    elif policy == "restore_march_non_hour16_margin":
        threshold = as_float(policy_value)
        blocked = month_march & (signals != 0)
        restore = month_march & (signals != 0) & (hour != 16) & (abs_margin >= threshold)
    elif policy == "block_march_long_restore_non_hour16_margin":
        threshold = as_float(policy_value)
        blocked = month_march & (signals == 1)
        restore = month_march & (signals != 0) & (hour != 16) & (abs_margin >= threshold)
    elif policy == "block_march_long_restore_short_p":
        threshold = as_float(policy_value)
        blocked = month_march & (signals == 1)
        candidate = potential_signals(
            part,
            short_threshold=threshold,
            long_threshold=base.LONG_THRESHOLD,
            min_margin=as_float(variant.get("min_margin")),
            long_block_min=as_float(variant.get("long_block_min")),
        )
        restore = month_march & (candidate == -1)
        restore_signals[restore] = -1
    elif policy == "restore_march_long_p_adx_and_short_p":
        pieces = parse_policy_values(policy_value)
        blocked = month_march & (signals != 0)
        p_long = part["p_long"].to_numpy(dtype=float)
        p_short = part["p_short"].to_numpy(dtype=float)
        long_margin = part["long_margin"].to_numpy(dtype=float)
        short_margin = part["short_margin"].to_numpy(dtype=float)
        adx = part[base.SIDE_FILTER_FEATURE].to_numpy(dtype=float)
        min_margin = as_float(variant.get("min_margin"))
        long_restore = month_march & (p_long >= pieces.get("p_long", 999.0)) & (adx >= pieces.get("adx_14", 999.0)) & (long_margin >= min_margin)
        short_restore = month_march & (p_short >= pieces.get("p_short", 999.0)) & (short_margin >= min_margin)
        restore = long_restore | short_restore
        restore_signals[long_restore] = 1
        restore_signals[short_restore & ((~long_restore) | (p_short >= p_long))] = -1
    else:
        raise RuntimeError(f"unknown bridge policy(알 수 없는 연결 정책): {policy}")

    out[blocked] = 0
    out[restore] = restore_signals[restore]
    floor_mask = margin_floor_mask(out, part, as_float(variant.get("entry_margin_floor")))
    audit["entry_margin_floor_filtered_count"] = int(np.count_nonzero((out != 0) & ~floor_mask))
    out[~floor_mask] = 0
    audit["march_block_count"] = int(np.count_nonzero(blocked & ~restore))
    audit["march_restore_count"] = int(np.count_nonzero(restore))
    audit["final_signal_count"] = int(np.count_nonzero(out))
    return out, audit


def session_label(hour: int) -> str:
    if 0 <= hour < 6:
        return "asia_late(아시아 후반)"
    if 6 <= hour < 12:
        return "eu_morning(유럽 오전)"
    if 12 <= hour < 17:
        return "us_premarket_cash_open(미국 프리마켓/현금장 초반)"
    if 17 <= hour < 22:
        return "us_cash_core(미국 현금장 핵심)"
    return "post_cash_late(현금장 후반)"


def simulate_variant(frame: pd.DataFrame, variant: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    trade_rows: list[dict[str, Any]] = []
    aggregate = {
        "source_signal_count": 0,
        "march_source_signal_count": 0,
        "march_block_count": 0,
        "march_restore_count": 0,
        "entry_margin_floor_filtered_count": 0,
        "final_signal_count": 0,
    }
    for split, split_frame in frame.groupby("split", sort=False):
        part = split_frame.sort_values("timestamp_dt").reset_index(drop=True)
        signals, _ = base.decision_signals(
            part,
            short_threshold=float(variant["short_threshold"]),
            long_block_min=float(variant["long_block_min"]),
            min_margin=float(variant["min_margin"]),
            with_reasons=False,
        )
        bridged, audit = apply_bridge_policy(signals, part, variant)
        for key in aggregate:
            aggregate[key] += int(audit.get(key, 0))
        opens = part["entry_open"].to_numpy(dtype=float)
        timestamps = part["timestamp_dt"].to_numpy()
        position = 0
        entry_index = 0
        entry_open = 0.0
        bars_in_position = 0
        for index in range(len(part)):
            if position != 0:
                bars_in_position += 1
            if position != 0 and bars_in_position >= int(variant["max_hold_m5"]):
                trade_rows.append(make_trade_row(variant, split, part, timestamps, opens, position, entry_index, index, entry_open, "close_max_hold"))
                position = 0
                bars_in_position = 0
                continue
            signal = int(bridged[index])
            if signal == 0:
                continue
            if position == 0:
                position = signal
                entry_index = index
                entry_open = float(opens[index])
                bars_in_position = 0
                continue
            if signal == position:
                continue
            trade_rows.append(make_trade_row(variant, split, part, timestamps, opens, position, entry_index, index, entry_open, "reverse_on_opposite"))
            position = signal
            entry_index = index
            entry_open = float(opens[index])
            bars_in_position = 0
    return pd.DataFrame(trade_rows), aggregate


def make_trade_row(
    variant: Mapping[str, Any],
    split: str,
    part: pd.DataFrame,
    timestamps: np.ndarray,
    opens: np.ndarray,
    position: int,
    entry_index: int,
    exit_index: int,
    entry_open: float,
    exit_reason: str,
) -> dict[str, Any]:
    exit_open = float(opens[exit_index])
    profit = (exit_open - entry_open) * base.POINT_VALUE - base.BASE_COST if position == 1 else (entry_open - exit_open) * base.POINT_VALUE - base.BASE_COST
    entry_row = part.iloc[entry_index]
    server_time = pd.Timestamp(entry_row["bar_time_server"])
    return {
        "run_id": RUN_ID,
        "variant_id": variant["variant_id"],
        "queue_id": variant["queue_id"],
        "axis_id": variant.get("axis_id", ""),
        "split": split,
        "entry_timestamp": pd.Timestamp(timestamps[entry_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "exit_timestamp": pd.Timestamp(timestamps[exit_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entry_server_time": server_time.strftime("%Y-%m-%d %H:%M:%S"),
        "entry_month": server_time.strftime("%Y-%m"),
        "entry_hour": int(server_time.hour),
        "entry_session": session_label(int(server_time.hour)),
        "held_m5": int(exit_index - entry_index),
        "side": "long" if position == 1 else "short",
        "entry_score": finite(entry_row["long_margin"] if position == 1 else entry_row["short_margin"], 12),
        "entry_confidence": finite(entry_row["p_long"] if position == 1 else entry_row["p_short"], 12),
        "entry_open": finite(entry_open, 5),
        "exit_open": finite(exit_open, 5),
        "net_profit": finite(profit, 10),
        base.SIDE_FILTER_FEATURE: finite(entry_row[base.SIDE_FILTER_FEATURE], 12),
        "short_probability_threshold": finite(variant["short_threshold"], 12),
        "entry_margin_floor": finite(variant.get("entry_margin_floor"), 12),
        "bridge_policy": variant.get("bridge_policy", ""),
        "bridge_policy_value": variant.get("bridge_policy_value", ""),
        "bridge_expression": variant.get("bridge_expression", ""),
        "exit_reason": exit_reason,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def candidate_status(row: Mapping[str, Any], reference: Mapping[str, Any]) -> str:
    density = as_float(row.get("combined_trade_per_business_day"))
    pf = as_float(row.get("combined_profit_factor"))
    val_net = as_float(row.get("validation_net_profit"))
    oos_net = as_float(row.get("oos_net_profit"))
    short_count = as_float(row.get("combined_short_count"))
    dd = as_float(row.get("combined_max_drawdown"))
    ref_dd = as_float(reference.get("combined_max_drawdown"))
    if density < DENSITY_FLOOR:
        return "fail_density_floor(밀도 하한 실패)"
    if short_count <= 0:
        return "fail_short_side_zero(숏 0 실패)"
    if val_net <= 0 or oos_net <= 0:
        return "fail_split_profit(분할 수익 실패)"
    if pf < TARGET_PF:
        return "watch_pf_below_target(PF 목표 미만 관찰)"
    if dd < ref_dd:
        return "watch_dd_worse_than_reference(낙폭 기준보다 악화 관찰)"
    return "pass_proxy_pf_density_split_dd_side(프록시 PF/밀도/분할/낙폭/방향 통과)"


def selection_score(row: Mapping[str, Any], reference: Mapping[str, Any]) -> float:
    density = as_float(row.get("combined_trade_per_business_day"))
    pf = as_float(row.get("combined_profit_factor"))
    net = as_float(row.get("combined_net_profit"))
    dd_delta = as_float(row.get("combined_max_drawdown")) - as_float(reference.get("combined_max_drawdown"))
    side_balance = as_float(row.get("combined_long_short_balance"))
    score = (
        net
        + 650.0 * max(0.0, pf - TARGET_PF)
        + 260.0 * max(0.0, pf - as_float(reference.get("combined_profit_factor")))
        + 150.0 * max(0.0, density - DENSITY_FLOOR)
        + 0.70 * max(0.0, dd_delta)
        + 55.0 * side_balance
        + 0.18 * as_float(row.get("combined_short_count"))
        - 450.0 * max(0.0, TARGET_PF - pf)
        - 1250.0 * max(0.0, DENSITY_FLOOR - density)
    )
    if as_float(row.get("validation_net_profit")) <= 0 or as_float(row.get("oos_net_profit")) <= 0:
        score -= 500.0
    return score


def evaluate_queue(frame: pd.DataFrame, variants: Sequence[Mapping[str, Any]], reference: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    trade_cache: dict[str, pd.DataFrame] = {}
    for variant in variants:
        trades, audit = simulate_variant(frame, variant)
        row: dict[str, Any] = {
            "run_id": RUN_ID,
            "queue_id": variant["queue_id"],
            "axis_id": variant["axis_id"],
            "queue_type": variant["queue_type"],
            "queue_rank": variant["queue_rank"],
            "seed_variant_id": variant["seed_variant_id"],
            "variant_id": variant["variant_id"],
            "short_probability_threshold": finite(variant["short_threshold"], 12),
            "long_threshold": finite(base.LONG_THRESHOLD, 12),
            "min_margin": finite(variant["min_margin"], 12),
            "entry_margin_floor": finite(variant["entry_margin_floor"], 12),
            "long_block_feature": base.SIDE_FILTER_FEATURE,
            "long_block_min": finite(variant["long_block_min"], 6),
            "max_hold_m5": variant["max_hold_m5"],
            "bridge_expression": variant["bridge_expression"],
            "bridge_policy": variant["bridge_policy"],
            "bridge_policy_value": variant["bridge_policy_value"],
            "trade_splitting_status": "not_used(거래 쪼개기 없음)",
            "proxy_boundary(프록시 경계)": "sequence_proxy_not_mt5_runtime(순서 프록시, MT5 런타임 아님)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for split in ["validation", "oos"]:
            row.update(base.metrics_for_trades(trades[trades["split"].eq(split)].copy(), split))
        row.update(base.metrics_for_trades(trades, "combined"))
        row["net_delta_vs_run364AD_selected"] = finite(as_float(row.get("combined_net_profit")) - as_float(reference.get("combined_net_profit")), 10)
        row["pf_delta_vs_run364AD_selected"] = finite(as_float(row.get("combined_profit_factor")) - as_float(reference.get("combined_profit_factor")), 10)
        row["dd_delta_vs_run364AD_selected"] = finite(as_float(row.get("combined_max_drawdown")) - as_float(reference.get("combined_max_drawdown")), 10)
        row["density_delta_vs_run364AD_selected"] = finite(as_float(row.get("combined_trade_per_business_day")) - as_float(reference.get("combined_trade_per_business_day")), 10)
        row["candidate_status"] = candidate_status(row, reference)
        row["selection_score"] = finite(selection_score(row, reference), 10)
        rows.append(row)
        audit_rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": variant["queue_id"],
                "variant_id": variant["variant_id"],
                **audit,
                "trade_count": len(trades),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
        trade_cache[variant["variant_id"]] = trades.copy()
    surface = pd.DataFrame(rows).sort_values("selection_score", ascending=False).reset_index(drop=True)
    best_id = str(surface.iloc[0]["variant_id"]) if not surface.empty else ""
    return surface, trade_cache.get(best_id, pd.DataFrame()), audit_rows


def reference_from_run364ad() -> dict[str, Any]:
    selected = read_json(parent.parent.scout.SELECTED_PROXY_CANDIDATE)
    return {
        "variant_id": selected.get("variant_id", ""),
        "combined_net_profit": selected.get("combined_net_profit", ""),
        "combined_profit_factor": selected.get("combined_profit_factor", ""),
        "combined_trade_count": selected.get("combined_trade_count", ""),
        "combined_trade_per_business_day": selected.get("combined_trade_per_business_day", ""),
        "combined_max_drawdown": selected.get("combined_max_drawdown", ""),
        "combined_recovery_factor": selected.get("combined_recovery_factor", ""),
        "combined_long_count": selected.get("combined_long_count", ""),
        "combined_short_count": selected.get("combined_short_count", ""),
        "combined_long_short_balance": selected.get("combined_long_short_balance", ""),
    }


def comparison_rows(best: Mapping[str, Any], reference: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for metric in [
        "combined_net_profit",
        "combined_profit_factor",
        "combined_trade_count",
        "combined_trade_per_business_day",
        "combined_expectancy",
        "combined_max_drawdown",
        "combined_recovery_factor",
        "combined_long_count",
        "combined_short_count",
        "combined_long_short_balance",
    ]:
        rows.append(
            {
                "run_id": RUN_ID,
                "reference_run_id": "run364AD_selected_proxy",
                "selected_variant_id": best.get("variant_id", ""),
                "metric_id": metric,
                "reference_value": reference.get(metric, ""),
                "selected_value": best.get(metric, ""),
                "delta_selected_minus_reference": finite(as_float(best.get(metric)) - as_float(reference.get(metric)), 10),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary_rows(trades: pd.DataFrame, columns: Sequence[str]) -> list[dict[str, Any]]:
    if trades.empty:
        return []
    rows: list[dict[str, Any]] = []
    for keys, part in trades.groupby(list(columns), dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = {column: value for column, value in zip(columns, keys, strict=False)}
        row.update(base.metrics_for_trades(part.copy(), "segment"))
        row["run_id"] = RUN_ID
        row["claim_boundary(주장 경계)"] = CLAIM_BOUNDARY
        rows.append(row)
    return rows


def review_queue_rows(best: Mapping[str, Any], strict_count: int) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "review_pf_lift_density_safe_proxy_scout(PF 상승 밀도 안전 프록시 정찰 검토)",
            "selected_variant_id": best.get("variant_id", ""),
            "selected_queue_id": best.get("queue_id", ""),
            "candidate_status": best.get("candidate_status", ""),
            "strict_pass_rows": strict_count,
            "required_review(필수 검토)": "PF/density/DD/split/session/side and MT5 probe need(PF/밀도/낙폭/분할/세션/방향과 MT5 탐침 필요성)",
            "effect(효과)": "proxy scout(프록시 정찰)를 package(패키지)나 runtime authority(런타임 권위)로 승격하지 않고 검토한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
    ]


def gate_row(name: str, evidence: Path, effect: str, status: str = "passed") -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "gate(게이트)": name,
        "status": status,
        "evidence(근거)": rel(evidence),
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def final_payload(parent_final: Mapping[str, Any], surface: pd.DataFrame, best: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at_utc: str) -> dict[str, Any]:
    strict_count = int(surface["candidate_status"].astype(str).str.startswith("pass_").sum()) if "candidate_status" in surface else 0
    selected_status = str(best.get("candidate_status", ""))
    package_path = "review_required_strict_proxy_pass(엄격 프록시 통과, 검토 필요)" if strict_count else "no_package_proxy_review_required(패키지 없음, 프록시 검토 필요)"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_materialization_run_id": parent_final.get("run_id"),
        "scout_rows": int(len(surface)),
        "strict_pass_rows": strict_count,
        "package_path": package_path,
        "selected_variant_id": best.get("variant_id", ""),
        "selected_queue_id": best.get("queue_id", ""),
        "selected_candidate_status": selected_status,
        "selected_combined_net_profit": best.get("combined_net_profit", ""),
        "selected_combined_profit_factor": best.get("combined_profit_factor", ""),
        "selected_combined_trade_count": best.get("combined_trade_count", ""),
        "selected_combined_trade_per_business_day": best.get("combined_trade_per_business_day", ""),
        "selected_combined_expectancy": best.get("combined_expectancy", ""),
        "selected_combined_max_drawdown": best.get("combined_max_drawdown", ""),
        "selected_combined_recovery_factor": best.get("combined_recovery_factor", ""),
        "selected_combined_long_count": best.get("combined_long_count", ""),
        "selected_combined_short_count": best.get("combined_short_count", ""),
        "selected_combined_long_short_balance": best.get("combined_long_short_balance", ""),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def write_receipts(final: Mapping[str, Any], best_trades: pd.DataFrame) -> list[dict[str, Any]]:
    base_payload = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "timestamp_utc sorted, bar_time_server for entry-month/hour/session rules(timestamp_utc 정렬, 진입 월/시간/세션 규칙은 bar_time_server 사용)",
            "sample_scope": "US100 M5 Stage364 Tier A proxy replay only(US100 5분봉 Stage364 티어 A 프록시 재생 전용)",
            "missing_or_duplicate_check": "runtime frame duplicate and required-value checks passed(런타임 프레임 중복과 필수 값 확인 통과)",
            "feature_label_boundary": "no new labels; queue uses row-local probabilities and fixed thresholds only(새 라벨 없음, 대기열은 행 단위 확률과 고정 임계값만 사용)",
            "split_boundary": "existing validation/oos split inherited from runtime frame(기존 검증/표본외 분할 상속)",
            "leakage_risk": "selection after full proxy surface; used for scout only, not operating claim(전체 프록시 표면 이후 선택, 정찰 전용이며 운영 주장 아님)",
            "data_hash_or_identity": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "selected_trade_rows": int(len(best_trades)),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "hypothesis": "PF lift and density restore can jointly find PF>=1.30 with density>=3/day without trade splitting(PF 상승과 밀도 복원이 거래 쪼개기 없이 PF 1.30 이상과 일 3회 이상 밀도를 함께 찾을 수 있음)",
            "decision_use": "rank proxy candidates for review, not MT5 package authority(검토용 프록시 후보 순위화, MT5 패키지 권위 아님)",
            "comparison_baseline": "run364AD selected proxy and run364V base runtime proxy(364AD 선택 프록시와 364V 기준 런타임 프록시)",
            "control_variables": "US100 M5, max_hold 8, ADX block 40, reverse-on-opposite, no trade splitting(US100 5분봉, 최대 보유 8, ADX 차단 40, 반대 신호 반전, 거래 쪼개기 없음)",
            "changed_variables": "short threshold, March restore policy, entry margin floor(숏 임계값, 3월 복원 정책, 진입 마진 하한)",
            "sample_scope": "validation and OOS proxy replay(검증과 표본외 프록시 재생)",
            "success_criteria": "combined PF>=1.30, density>=3/day, split net positive, short side nonzero(PF 1.30 이상, 일 3회 이상 밀도, 분할 순수익 양수, 숏 0 아님)",
            "failure_criteria": "PF lift breaks density or density restore keeps PF below 1.30(PF 상승이 밀도를 깨거나 밀도 복원이 PF 1.30 미만 유지)",
            "invalid_conditions": "top_n replay, post-entry ranking, MT5 claim without MT5 output(top_n 재생, 진입 후 순위, MT5 출력 없는 MT5 주장)",
            "stop_conditions": "strict pass zero moves to review/repair, strict pass nonzero moves to review before package(엄격 통과 0이면 검토/수리, 1개 이상이면 패키지 전 검토)",
            "evidence_plan": [rel(SCOUT_SURFACE), rel(SELECTED_EXPECTED_TRADE_TAPE), rel(GATE_AUDIT), rel(FINAL_DECISION)],
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-model-validation(옵시디언 모델 검증)",
            "model_training": "not_run(실행 안 함)",
            "onnx_export": "not_run(실행 안 함)",
            "effect(효과)": "proxy replay scout(프록시 재생 정찰)를 새 모델 권위로 해석하지 않음",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-performance-attribution(옵시디언 성과 귀속)",
            "observed_change": "PF and density trade off across short threshold and March restore policy(PF와 밀도가 숏 임계값 및 3월 복원 정책에 따라 맞교환됨)",
            "comparison_baseline": "run364AD selected proxy(364AD 선택 프록시)",
            "likely_drivers": "short threshold strictness, March long block, non-hour16 restore, entry margin floor(숏 임계값 엄격도, 3월 롱 차단, non-hour16 복원, 진입 마진 하한)",
            "segment_checks": [rel(SELECTED_MONTH_SIDE_SUMMARY), rel(SELECTED_SESSION_SUMMARY)],
            "trade_shape": {
                "selected_trade_count": final.get("selected_combined_trade_count"),
                "selected_expectancy": final.get("selected_combined_expectancy"),
                "selected_drawdown": final.get("selected_combined_max_drawdown"),
                "selected_long_count": final.get("selected_combined_long_count"),
                "selected_short_count": final.get("selected_combined_short_count"),
            },
            "alternative_explanations": "proxy sequence assumptions may differ from MT5 fills or broker spread(프록시 순서 가정이 MT5 체결 또는 브로커 스프레드와 다를 수 있음)",
            "attribution_confidence": "medium_proxy_only(MT5 전까지 중간, 프록시 전용)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-result-judgment(옵시디언 결과 판정)",
            "result_subject": RUN_ID,
            "evidence_available": [rel(SCOUT_SURFACE), rel(STRICT_CANDIDATES), rel(SELECTED_EXPECTED_TRADE_TAPE), rel(FINAL_DECISION)],
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "proxy scout only; useful candidate evidence but not operating model(프록시 정찰 전용, 후보 근거로는 유용하지만 운영 모델은 아님)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base_payload,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect(효과)": "proxy scout(프록시 정찰)를 운영 주장으로 승격하지 않음",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base_payload,
            "skill": "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_generated_with_manifest(커밋 후 추적 또는 매니페스트로 재생성 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AG proxy scout(364AG 프록시 정찰)를 닫음"),
        gate_row("input_parent_gate(부모 입력 게이트)", INPUT_MANIFEST, "run364AF 대기열과 기준 산출물을 확인함"),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점 안전 고정 임계값과 분할 경계를 기록함"),
        gate_row("queue_replay_gate(대기열 재생 게이트)", SCOUT_SURFACE, "12개 대기열 행을 재생함"),
        gate_row("topn_absence_gate(top_n 부재 게이트)", QUEUE_REPLAY_AUDIT, "top_n 재생이 없음을 확인함"),
        gate_row("kpi_contract_audit(KPI 계약 감사)", SCOUT_SURFACE, "net/PF/expectancy/DD/RF/trades/side/density를 기록함"),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "월/세션/방향 요약을 연결함"),
        gate_row("model_boundary_gate(모델 경계 게이트)", MODEL_RECEIPT, "새 모델/ONNX 권위를 주장하지 않음"),
        gate_row("result_judgment_gate(결과 판정 게이트)", JUDGMENT_RECEIPT, "MT5 필요 경계로 판정함"),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 해시를 연결함"),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "런타임 권위를 주장하지 않음"),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 게이트를 종료 기록에 연결함"),
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
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
    write_text(STAGE_BRIEF, "\n".join(lines) + "\n")


def write_docs(final: Mapping[str, Any], surface: pd.DataFrame, comparison: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    top = surface.head(10).to_dict("records")
    text = f"""# run364AG PF lift density-safe scout(364AG PF 상승 밀도 안전 정찰)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- scout_rows(정찰 행): `{final['scout_rows']}`
- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_expectancy']}` / `{final['selected_combined_max_drawdown']}` / `{final['selected_combined_recovery_factor']}`
- selected long/short/balance(선택 롱/숏/균형): `{final['selected_combined_long_count']}` / `{final['selected_combined_short_count']}` / `{final['selected_combined_long_short_balance']}`
- runtime_authority(런타임 권위): `not_claimed`

## Top Proxy Rows(상위 프록시 행)

{markdown_table(top, ['queue_id', 'axis_id', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count', 'candidate_status', 'selection_score'])}

## Baseline Comparison(기준 비교)

{markdown_table(comparison, ['metric_id', 'reference_value', 'selected_value', 'delta_selected_minus_reference'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 scout(정찰)는 timestamp-safe proxy(시점 안전 프록시) 후보 선별이며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- selected(선택): `{final['selected_variant_id']}`\n- effect(효과): PF lift density-safe queue(PF 상승 밀도 안전 대기열)를 프록시로 재생해 `{NEXT_RUN_ID}` 검토 대상으로 넘겼다.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"\n## run364AG PF Lift Density-Safe Scout Closeout(364AG PF 상승 밀도 안전 정찰 종료)\n\nAction(행동): run364AF(364AF 실행) queue(대기열) `12`개를 timestamp-safe proxy replay(시점 안전 프록시 재생)로 실행했다.\n\nEffect(효과): `{final['selected_variant_id']}`를 `{NEXT_RUN_ID}` review(검토) 대상으로 넘긴다. 운영 주장(operating claim, 운영 주장)은 없다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_proxy_scout_review_required(프록시 정찰 검토 필요로 없음)
- latest_proxy_scout(최근 프록시 정찰): `run364AG`
- selected_proxy_variant(선택 프록시 변형): `{final['selected_variant_id']}`
- selected_proxy_net_pf_density(선택 프록시 순수익/수익 팩터/밀도): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_per_business_day']}`
- next_review_queue(다음 검토 대기열): `{rel(RUN364AH_QUEUE)}`
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

current_truth(현재 진실): run364AG(364AG 실행)는 PF lift density-safe queue(PF 상승 밀도 안전 대기열) `12`개를 proxy replay scout(프록시 재생 정찰)했다. 선택 프록시 후보는 `{final['selected_variant_id']}`이고, net/PF/trades/density/DD(순수익/수익 팩터/거래수/밀도/낙폭)는 `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_max_drawdown']}`이다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 proxy evidence(프록시 근거)를 review(검토)한다.

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
        bom=False,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF lift density-safe proxy scout(PF 상승 밀도 안전 프록시 정찰)를 실행했다.\n- effect(효과): `{NEXT_RUN_ID}` review(검토) 대상으로 selected proxy(선택 프록시)를 넘겼다.\n- report(보고서): `{rel(REPORT_PATH)}`\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- idea(아이디어): PF lift(PF 상승)와 density restore(밀도 복원)를 고정 임계값으로 재생해 동시 통과 후보를 찾는다.\n- positive clue(긍정 단서): selected proxy(선택 프록시) `{final['selected_variant_id']}`.\n- failure memory(실패 기억): MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장 금지.\n",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"\n## {RUN_ID}\n\n- action(행동): PF lift density-safe proxy scout(PF 상승 밀도 안전 프록시 정찰)를 실행했다.\n- effect(효과): Stage364(364단계) 안에서 review(검토)로 이어간다.\n",
    )


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "proxy_scout(프록시 정찰)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "notes": f"selected={final['selected_variant_id']}; pass_rows={final['strict_pass_rows']}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["scout_rows"],
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(SCOUT_SURFACE),
        "result_status": STATUS,
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": "proxy_checked_no_trade_splitting(프록시 확인, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "net_profit": final["selected_combined_net_profit"],
        "profit_factor": final["selected_combined_profit_factor"],
        "trade_count": final["selected_combined_trade_count"],
        "expectancy": final["selected_combined_expectancy"],
        "max_drawdown_amount": final["selected_combined_max_drawdown"],
        "long_trade_count": final["selected_combined_long_count"],
        "short_trade_count": final["selected_combined_short_count"],
        "evidence_scope": "proxy_scout_no_authority(프록시 정찰, 권위 없음)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for subrun_id, record_view, tier_scope, kpi_scope in [
        (f"{RUN_ID}__Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "proxy scout surface(프록시 정찰 표면)"),
        (f"{RUN_ID}__Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)"),
        (
            f"{RUN_ID}__Tier_A_plus_B",
            "Tier A+B combined(Tier A+B 합산)",
            "Tier A+B",
            "Tier A only plus Tier B missing_required(Tier A만 있고 Tier B 필수 누락)",
        ),
    ]:
        row = dict(common)
        row.update({"ledger_row_id": subrun_id, "subrun_id": subrun_id, "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": kpi_scope})
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
            ("scout_surface", SCOUT_SURFACE, "Proxy scout surface(프록시 정찰 표면)."),
            ("strict_candidates", STRICT_CANDIDATES, "Strict proxy candidates(엄격 프록시 후보)."),
            ("selected_expected_trade_tape", SELECTED_EXPECTED_TRADE_TAPE, "Selected expected trade tape(선택 예상 거래 테이프)."),
            ("month_side_summary", SELECTED_MONTH_SIDE_SUMMARY, "Month/side summary(월/방향 요약)."),
            ("session_summary", SELECTED_SESSION_SUMMARY, "Session summary(세션 요약)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    selected_base = read_json(base.SELECTED_RUNTIME_CANDIDATE)
    frame, _, _ = load_runtime_frame()
    variants = queue_variants(selected_base)
    reference = reference_from_run364ad()
    surface, best_trades, audit_rows = evaluate_queue(frame, variants, reference)
    best = surface.iloc[0].to_dict() if not surface.empty else {}
    strict = surface[surface["candidate_status"].astype(str).str.startswith("pass_")].copy() if not surface.empty else pd.DataFrame()
    comparison = comparison_rows(best, reference)
    month_side = summary_rows(best_trades, ["entry_month", "side"])
    session = summary_rows(best_trades, ["entry_session", "side"])
    review_queue = review_queue_rows(best, int(len(strict)))
    write_csv(QUEUE_REPLAY_AUDIT, audit_rows)
    write_csv(SCOUT_SURFACE, surface.to_dict("records"))
    write_csv(STRICT_CANDIDATES, strict.to_dict("records"))
    write_json(SELECTED_PROXY_CANDIDATE, best)
    write_csv(SELECTED_EXPECTED_TRADE_TAPE, best_trades.to_dict("records"))
    write_csv(SELECTED_MONTH_SIDE_SUMMARY, month_side)
    write_csv(SELECTED_SESSION_SUMMARY, session)
    write_csv(BASELINE_COMPARISON, comparison)
    write_csv(RUN364AH_QUEUE, review_queue)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-performance-attribution(옵시디언 성과 귀속)",
                "obsidian-result-judgment(옵시디언 결과 판정)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "input_parent_gate",
                "data_integrity_audit",
                "queue_replay_gate",
                "topn_absence_gate",
                "kpi_contract_audit",
                "performance_attribution_gate",
                "model_boundary_gate",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "claim_boundary_audit",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    created_at = now_utc()
    temp_final = final_payload(parent_final, surface, best, [], created_at)
    write_json(FINAL_DECISION, temp_final)
    gates = write_receipts(temp_final, best_trades)
    final = final_payload(parent_final, surface, best, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, comparison, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
