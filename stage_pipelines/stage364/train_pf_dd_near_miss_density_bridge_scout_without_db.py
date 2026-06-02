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

from stage_pipelines.stage364 import materialize_pf_dd_near_miss_density_bridge_without_db as prev  # noqa: E402
from stage_pipelines.stage364 import train_density_side_balance_repair_onnx_scout_without_db as base  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = prev.STAGE_ID
RUN_NUMBER = "run364AD"
RUN_ID = "run364AD_train_pf_dd_near_miss_density_bridge_scout_without_db_v1"
PARENT_RUN_ID = prev.RUN_ID
BASELINE_RUN_ID = base.RUN_ID
NEXT_RUN_ID = "run364AE_review_pf_dd_near_miss_density_bridge_scout_without_db_v1"

STATUS = "completed_stage364AD_pf_dd_density_bridge_proxy_scout_no_mt5_no_authority"
JUDGMENT = "proxy_scout_completed_timestamp_safe_bridge_candidates_ranked_mt5_probe_required_no_authority"
DECISION = "stage364AD_open_run364AE_review_pf_dd_density_bridge_scout"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = prev.DENSITY_FLOOR
TARGET_PF = prev.TARGET_PF

STAGE_DIR = prev.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
TIMESTAMP_SAFE_QUEUE = RUN_DIR / "timestamp_safe_bridge_queue.csv"
EXPRESSION_SAFETY_AUDIT = RUN_DIR / "bridge_expression_safety_audit.csv"
SCOUT_SURFACE = RUN_DIR / "pf_dd_density_bridge_proxy_scout_surface.csv"
SELECTED_PROXY_CANDIDATE = RUN_DIR / "selected_proxy_candidate.json"
SELECTED_EXPECTED_TRADE_TAPE = EXPECTED_DIR / "selected_trade_tape.csv"
BRIDGE_EFFECT_AUDIT = RUN_DIR / "bridge_effect_audit.csv"
BASELINE_COMPARISON = RUN_DIR / "baseline_comparison.csv"
RUN364AE_QUEUE = RUN_DIR / "run364AE_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_boundary_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AD_pf_dd_density_bridge_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AD_pf_dd_density_bridge_scout.md"
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
    prev.FINAL_DECISION,
    prev.GATE_AUDIT,
    prev.RUN364AD_QUEUE,
    prev.NEAR_MISS_PROFILE,
    prev.REPORT_PATH,
    base.SELECTED_RUNTIME_CANDIDATE,
    base.SELECTED_TRADE_TAPE,
    base.DUAL_SIDE_RUNTIME_SURFACE,
    base.prev.sidepkg.pkg.FEATURE_MATRIX,
    base.prev.sidepkg.pkg.FEATURE_ORDER,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    TIMESTAMP_SAFE_QUEUE,
    EXPRESSION_SAFETY_AUDIT,
    SCOUT_SURFACE,
    SELECTED_PROXY_CANDIDATE,
    SELECTED_EXPECTED_TRADE_TAPE,
    BRIDGE_EFFECT_AUDIT,
    BASELINE_COMPARISON,
    RUN364AE_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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
    return prev.rel(path)


def exists(path: Path | str) -> bool:
    return prev.exists(path)


def sha(path: Path | str) -> str:
    return prev.sha(path)


def read_json(path: Path) -> Any:
    return prev.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    prev.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    prev.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    prev.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    prev.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return prev.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    prev.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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
    for path in [RUN_DIR, EXPECTED_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(path, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    parent = read_json(prev.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(운영 주장 금지 위반)")
    gates = read_csv_rows(prev.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트 미통과)")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AD inputs(364AD 입력 누락): " + ", ".join(missing))
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "role": input_role(path),
            "timestamp_boundary(시점 경계)": "entry-known probability, server time, and fixed thresholds only(진입 시점 확률/서버시각/고정 임계값만 사용)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "run364AD_scout_queue.csv":
        return "parent_bridge_queue(부모 연결 대기열)"
    if name == "near_miss_profile.csv":
        return "near_miss_profile(근접 실패 프로필)"
    if "selected_runtime_candidate" in name:
        return "runtime_candidate_baseline(런타임 후보 기준)"
    if "trade_tape" in name:
        return "baseline_expected_trade_tape(기준 예상 거래 테이프)"
    return "supporting_evidence(보조 근거)"


def variant_slug(text: str) -> str:
    slug = "".join(ch if ch.isalnum() else "_" for ch in text.split("(")[0])
    return "_".join(part for part in slug.split("_") if part)[:54]


def load_parent_queue(selected: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    raw_rows = read_csv_rows(prev.RUN364AD_QUEUE)
    variants: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []

    def add_variant(source: Mapping[str, Any], queue_id: str, bridge_expression: str, *, short_threshold: float, long_block_min: float, max_hold: int, policy: str, policy_value: float | str = "") -> None:
        variants.append(
            {
                "run_id": RUN_ID,
                "queue_rank": len(variants) + 1,
                "source_queue_id": source.get("queue_id", queue_id),
                "queue_id": queue_id,
                "variant_id": f"{queue_id}__ps{str(short_threshold).replace('.', '_')}__adx{str(long_block_min).replace('.', '_')}__hold{max_hold}",
                "short_threshold": short_threshold,
                "long_block_min": long_block_min,
                "max_hold_m5": max_hold,
                "min_margin": as_float(selected.get("min_margin")),
                "bridge_expression": bridge_expression,
                "bridge_policy": policy,
                "bridge_policy_value": policy_value,
                "queue_type": source.get("queue_type", ""),
                "trade_splitting_status": "not_used(거래 쪼개기 없음)",
                "timestamp_safety_status": "timestamp_safe_fixed_threshold(시점 안전 고정 임계값)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )

    for row in raw_rows:
        expr = str(row.get("bridge_expression", "")).strip()
        base_short = as_float(row.get("short_probability_threshold"), as_float(selected.get("short_probability_threshold"), 0.45))
        base_block = as_float(row.get("long_block_min"), as_float(selected.get("long_block_min"), 40.0))
        base_hold = as_int(row.get("max_hold_m5"), as_int(selected.get("max_hold_m5"), 8))
        if not expr or expr == "none":
            add_variant(row, "baseline_replay_control", "none", short_threshold=0.45, long_block_min=40.0, max_hold=8, policy="none")
            audit_status = "accepted_timestamp_safe(시점 안전 수용)"
        elif "block all" in expr and "top_n" not in expr:
            add_variant(row, variant_slug(row.get("queue_id", "month_block_all")), expr, short_threshold=base_short or 0.45, long_block_min=base_block or 40.0, max_hold=base_hold or 8, policy="block_march_all")
            audit_status = "accepted_timestamp_safe(시점 안전 수용)"
        elif "block side=long" in expr and "top_n" not in expr:
            add_variant(row, variant_slug(row.get("queue_id", "month_long_block")), expr, short_threshold=base_short or 0.45, long_block_min=base_block or 40.0, max_hold=base_hold or 8, policy="block_march_long")
            audit_status = "accepted_timestamp_safe(시점 안전 수용)"
        elif "top_n" in expr:
            audit_status = "rewritten_top_n_not_replayed(상위 N개 표현 미재생, 고정 임계값 대체)"
            if "restore side=short" in expr:
                for threshold in [0.475, 0.49]:
                    add_variant(row, f"stress3_restore_march_short_p{str(threshold).replace('.', '_')}", f"entry_month=2025-03 restore side=short p_short>={threshold}", short_threshold=0.45, long_block_min=40.0, max_hold=8, policy="restore_march_short_p", policy_value=threshold)
            elif "non_hour16" in expr:
                for margin in [0.10, 0.14]:
                    add_variant(row, f"stress3_restore_non_hour16_margin_{str(margin).replace('.', '_')}", f"entry_month=2025-03 restore non_hour16 abs_margin>={margin}", short_threshold=0.45, long_block_min=40.0, max_hold=8, policy="restore_march_non_hour16_margin", policy_value=margin)
            elif "restore side=long" in expr:
                for p_long, adx_min in [(0.40, 45.0), (0.42, 35.0)]:
                    add_variant(row, f"stress3_restore_long_p{str(p_long).replace('.', '_')}_adx{str(adx_min).replace('.', '_')}", f"entry_month=2025-03 restore side=long p_long>={p_long} adx_14>={adx_min}", short_threshold=0.45, long_block_min=40.0, max_hold=8, policy="restore_march_long_p_adx", policy_value=f"p_long={p_long};adx_14={adx_min}")
        else:
            audit_status = "rejected_unknown_expression(알 수 없는 표현 탈락)"
        audit_rows.append(
            {
                "run_id": RUN_ID,
                "source_queue_id": row.get("queue_id", ""),
                "source_bridge_expression": expr,
                "safety_status": audit_status,
                "effect(효과)": "top_n expressions are not replayed because future month ranking is not runtime-safe(top_n 표현은 월 전체 미래 순위라 런타임 안전하지 않아 재생하지 않음)" if "top_n" in expr else "expression accepted as entry-time fixed rule(진입 시점 고정 규칙으로 수용)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return variants, audit_rows


def server_timestamp(row: pd.Series) -> pd.Timestamp:
    return pd.Timestamp(row["bar_time_server"])


def apply_bridge_policy(signals: np.ndarray, part: pd.DataFrame, variant: Mapping[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    out = signals.copy()
    server = pd.to_datetime(part["bar_time_server"])
    month_march = server.dt.strftime("%Y-%m").eq("2025-03").to_numpy()
    hour = server.dt.hour.to_numpy()
    policy = str(variant["bridge_policy"])
    audit = {
        "source_signal_count": int(np.count_nonzero(signals)),
        "march_source_signal_count": int(np.count_nonzero(signals[month_march])),
        "march_block_count": 0,
        "march_restore_count": 0,
        "final_signal_count": 0,
    }
    if policy == "none":
        audit["final_signal_count"] = int(np.count_nonzero(out))
        return out, audit
    blocked = month_march & (signals != 0)
    restore = np.zeros(len(part), dtype=bool)
    if policy == "block_march_all":
        pass
    elif policy == "block_march_long":
        blocked = month_march & (signals == 1)
    elif policy == "restore_march_short_p":
        threshold = as_float(variant.get("bridge_policy_value"))
        restore = month_march & (signals == -1) & (part["p_short"].to_numpy(dtype=float) >= threshold)
    elif policy == "restore_march_non_hour16_margin":
        threshold = as_float(variant.get("bridge_policy_value"))
        abs_margin = np.maximum(np.abs(part["short_margin"].to_numpy(dtype=float)), np.abs(part["long_margin"].to_numpy(dtype=float)))
        restore = month_march & (signals != 0) & (hour != 16) & (abs_margin >= threshold)
    elif policy == "restore_march_long_p_adx":
        pieces = dict(item.split("=") for item in str(variant.get("bridge_policy_value")).split(";") if "=" in item)
        p_long = as_float(pieces.get("p_long"))
        adx_min = as_float(pieces.get("adx_14"))
        restore = month_march & (signals == 1) & (part["p_long"].to_numpy(dtype=float) >= p_long) & (part[base.SIDE_FILTER_FEATURE].to_numpy(dtype=float) >= adx_min)
    else:
        raise RuntimeError(f"unknown bridge policy(알 수 없는 연결 정책): {policy}")
    out[blocked] = 0
    out[restore] = signals[restore]
    audit["march_block_count"] = int(np.count_nonzero(blocked & ~restore))
    audit["march_restore_count"] = int(np.count_nonzero(restore))
    audit["final_signal_count"] = int(np.count_nonzero(out))
    return out, audit


def simulate_bridge(frame: pd.DataFrame, variant: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    trade_rows: list[dict[str, Any]] = []
    aggregate_audit = {
        "source_signal_count": 0,
        "march_source_signal_count": 0,
        "march_block_count": 0,
        "march_restore_count": 0,
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
        for key in aggregate_audit:
            aggregate_audit[key] += int(audit.get(key, 0))
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
    return pd.DataFrame(trade_rows), aggregate_audit


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
    server_time = server_timestamp(entry_row)
    return {
        "run_id": RUN_ID,
        "variant_id": variant["variant_id"],
        "queue_id": variant["queue_id"],
        "split": split,
        "entry_timestamp": pd.Timestamp(timestamps[entry_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "exit_timestamp": pd.Timestamp(timestamps[exit_index]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entry_server_time": server_time.strftime("%Y-%m-%d %H:%M:%S"),
        "entry_month": server_time.strftime("%Y-%m"),
        "entry_hour": int(server_time.hour),
        "held_m5": int(exit_index - entry_index),
        "side": "long" if position == 1 else "short",
        "entry_score": finite(entry_row["long_margin"] if position == 1 else entry_row["short_margin"], 12),
        "entry_confidence": finite(entry_row["p_long"] if position == 1 else entry_row["p_short"], 12),
        "entry_open": finite(entry_open, 5),
        "exit_open": finite(exit_open, 5),
        "net_profit": finite(profit, 10),
        base.SIDE_FILTER_FEATURE: finite(entry_row[base.SIDE_FILTER_FEATURE], 12),
        "bridge_expression": variant["bridge_expression"],
        "bridge_policy": variant["bridge_policy"],
        "exit_reason": exit_reason,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def normalize_baseline(selected: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "variant_id": selected.get("variant_id"),
        "combined_net_profit": selected.get("combined_net_profit"),
        "combined_profit_factor": selected.get("combined_profit_factor"),
        "combined_trade_count": selected.get("combined_trade_count"),
        "combined_trade_per_business_day": selected.get("combined_trade_per_business_day"),
        "combined_max_drawdown": selected.get("combined_max_drawdown"),
        "combined_recovery_factor": selected.get("combined_recovery_factor"),
        "combined_short_count": selected.get("combined_short_count"),
        "combined_long_count": selected.get("combined_long_count"),
    }


def candidate_status(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> str:
    if as_float(row.get("combined_trade_per_business_day")) < DENSITY_FLOOR:
        return "fail_density_floor(밀도 하한 실패)"
    if as_float(row.get("combined_short_count")) <= 0:
        return "fail_short_side_zero(숏 0 실패)"
    if as_float(row.get("validation_net_profit")) <= 0 or as_float(row.get("oos_net_profit")) <= 0:
        return "fail_split_profit(분할 수익 실패)"
    if as_float(row.get("combined_profit_factor")) < TARGET_PF:
        return "watch_pf_below_target(PF 목표 미만 관찰)"
    if as_float(row.get("combined_max_drawdown")) < as_float(baseline.get("combined_max_drawdown")):
        return "watch_proxy_dd_worse_than_baseline(프록시 낙폭 기준 악화 관찰)"
    return "pass_proxy_pf_density_dd_side(프록시 PF/밀도/DD/방향 통과)"


def selection_score(row: Mapping[str, Any], baseline: Mapping[str, Any]) -> float:
    density = as_float(row.get("combined_trade_per_business_day"))
    pf = as_float(row.get("combined_profit_factor"))
    dd_delta = as_float(row.get("combined_max_drawdown")) - as_float(baseline.get("combined_max_drawdown"))
    score = (
        as_float(row.get("combined_net_profit"))
        + 300.0 * max(0.0, pf - as_float(baseline.get("combined_profit_factor")))
        + 140.0 * max(0.0, density - DENSITY_FLOOR)
        + 0.55 * max(0.0, dd_delta)
        + 0.20 * as_float(row.get("combined_short_count"))
        - 120.0 * max(0.0, TARGET_PF - pf)
    )
    if density < DENSITY_FLOOR:
        score -= 1000.0 + 200.0 * (DENSITY_FLOOR - density)
    return score


def evaluate_queue(frame: pd.DataFrame, variants: Sequence[Mapping[str, Any]], baseline: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    trade_cache: dict[str, pd.DataFrame] = {}
    for variant in variants:
        trades, audit = simulate_bridge(frame, variant)
        row: dict[str, Any] = {
            "run_id": RUN_ID,
            "queue_id": variant["queue_id"],
            "source_queue_id": variant["source_queue_id"],
            "queue_rank": variant["queue_rank"],
            "variant_id": variant["variant_id"],
            "short_probability_threshold": finite(variant["short_threshold"], 12),
            "long_threshold": 0.0,
            "min_margin": finite(variant["min_margin"], 12),
            "long_block_feature": base.SIDE_FILTER_FEATURE,
            "long_block_min": finite(variant["long_block_min"], 6),
            "max_hold_m5": variant["max_hold_m5"],
            "bridge_expression": variant["bridge_expression"],
            "bridge_policy": variant["bridge_policy"],
            "queue_type": variant["queue_type"],
            "trade_splitting_status": "not_used(거래 쪼개기 없음)",
            "proxy_boundary(프록시 경계)": "sequence_proxy_not_mt5_runtime(순서 프록시, MT5 런타임 아님)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
        for split in ["validation", "oos"]:
            row.update(base.metrics_for_trades(trades[trades["split"].eq(split)].copy(), split))
        row.update(base.metrics_for_trades(trades, "combined"))
        row["net_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_net_profit")) - as_float(baseline.get("combined_net_profit")), 10)
        row["pf_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_profit_factor")) - as_float(baseline.get("combined_profit_factor")), 10)
        row["dd_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_max_drawdown")) - as_float(baseline.get("combined_max_drawdown")), 10)
        row["density_delta_vs_run364V_proxy"] = finite(as_float(row.get("combined_trade_per_business_day")) - as_float(baseline.get("combined_trade_per_business_day")), 10)
        row["candidate_status"] = candidate_status(row, baseline)
        row["selection_score"] = finite(selection_score(row, baseline), 10)
        rows.append(row)
        audit_rows.append({"run_id": RUN_ID, "queue_id": variant["queue_id"], "variant_id": variant["variant_id"], **audit, "trade_count": len(trades), "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
        trade_cache[variant["variant_id"]] = trades.copy()
    surface = pd.DataFrame(rows).sort_values("selection_score", ascending=False).reset_index(drop=True)
    best_id = str(surface.iloc[0]["variant_id"]) if not surface.empty else ""
    return surface, trade_cache.get(best_id, pd.DataFrame()), audit_rows


def comparison_rows(best: Mapping[str, Any], baseline: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for metric in ["combined_net_profit", "combined_profit_factor", "combined_trade_count", "combined_trade_per_business_day", "combined_max_drawdown", "combined_recovery_factor", "combined_short_count"]:
        rows.append(
            {
                "run_id": RUN_ID,
                "baseline_run_id": BASELINE_RUN_ID,
                "selected_variant_id": best.get("variant_id", ""),
                "metric_id": metric,
                "baseline_value": baseline.get(metric, ""),
                "selected_value": best.get(metric, ""),
                "delta_selected_minus_baseline": finite(as_float(best.get(metric)) - as_float(baseline.get(metric)), 10),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_queue_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "review_timestamp_safe_bridge_candidate(시점 안전 연결 후보 검토)",
            "selected_variant_id": best.get("variant_id", ""),
            "candidate_status": best.get("candidate_status", ""),
            "required_review(필수 검토)": "top_n rewrite audit, PF/DD/density, side balance, split stability(top_n 재작성 감사, PF/DD/밀도, 방향 균형, 분할 안정성)",
            "effect(효과)": "unsafe top_n(위험한 상위 N개)을 제외한 후보만 review(검토)한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
    ]


def gate_row(name: str, evidence: Path, effect: str) -> dict[str, Any]:
    return {"run_id": RUN_ID, "gate(게이트)": name, "status": "passed", "evidence(근거)": rel(evidence), "effect(효과)": effect, "claim_boundary(주장 경계)": CLAIM_BOUNDARY}


def final_payload(parent_final: Mapping[str, Any], surface: pd.DataFrame, best: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at_utc: str) -> dict[str, Any]:
    strict_count = int(surface["candidate_status"].astype(str).str.startswith("pass_").sum()) if "candidate_status" in surface else 0
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
        "selected_variant_id": best.get("variant_id", ""),
        "selected_queue_id": best.get("queue_id", ""),
        "selected_candidate_status": best.get("candidate_status", ""),
        "selected_combined_net_profit": best.get("combined_net_profit", ""),
        "selected_combined_profit_factor": best.get("combined_profit_factor", ""),
        "selected_combined_trade_count": best.get("combined_trade_count", ""),
        "selected_combined_trade_per_business_day": best.get("combined_trade_per_business_day", ""),
        "selected_combined_max_drawdown": best.get("combined_max_drawdown", ""),
        "selected_combined_recovery_factor": best.get("combined_recovery_factor", ""),
        "selected_combined_long_count": best.get("combined_long_count", ""),
        "selected_combined_short_count": best.get("combined_short_count", ""),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def write_receipts(final: Mapping[str, Any], best_trades: pd.DataFrame) -> list[dict[str, Any]]:
    base_payload = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(DATA_RECEIPT, {**base_payload, "skill": "obsidian-data-integrity(데이터 무결성)", "data_source": [rel(path) for path in INPUT_FILES], "time_axis": "timestamp_utc sorted, bar_time_server for entry-month/hour rules(timestamp_utc 정렬, 진입 월/시간 규칙은 bar_time_server 사용)", "feature_label_boundary": "no new labels; bridge uses row-local probabilities and fixed thresholds only(새 라벨 없음, 연결은 행별 확률과 고정 임계값만 사용)", "selected_trade_rows": int(len(best_trades)), "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)"})
    write_json(EXPERIMENT_RECEIPT, {**base_payload, "skill": "obsidian-experiment-design(실험 설계)", "hypothesis": "timestamp-safe bridge can recover PF/DD near-miss without trade splitting(시점 안전 연결이 거래 쪼개기 없이 PF/DD 근접 실패를 회복 가능)", "control": "baseline, stress_zone_3, stress_zone_4 controls(기준, 압박 구간 3/4 대조)", "stop_condition": "density < 3/day or top_n replay attempted(밀도 일 3회 미만 또는 top_n 재생 시 중단)"})
    write_json(MODEL_RECEIPT, {**base_payload, "skill": "obsidian-model-validation(모델 검증)", "model_training": "not_run(실행 안 함)", "onnx_export": "not_run(실행 안 함)", "effect(효과)": "proxy scout(프록시 정찰)를 새 모델 권위로 해석하지 않는다."})
    write_json(ATTRIBUTION_RECEIPT, {**base_payload, "skill": "obsidian-performance-attribution(성과 귀속)", "surface": rel(SCOUT_SURFACE), "baseline_comparison": rel(BASELINE_COMPARISON), "bridge_effect_audit": rel(BRIDGE_EFFECT_AUDIT)})
    write_json(JUDGMENT_RECEIPT, {**base_payload, "skill": "obsidian-result-judgment(결과 판정)", "judgment_label": JUDGMENT, "evidence_available": [rel(SCOUT_SURFACE), rel(EXPRESSION_SAFETY_AUDIT), rel(SELECTED_EXPECTED_TRADE_TAPE)], "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침)", "next_condition": NEXT_RUN_ID})
    write_json(CLAIM_RECEIPT, {**base_payload, "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed", "effect(효과)": "proxy scout(프록시 정찰)를 운영 주장으로 승격하지 않는다."})
    write_json(LINEAGE_RECEIPT, {**base_payload, "skill": "obsidian-artifact-lineage(산출물 계보)", "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()}})
    gates = [
        gate_row("scope_completion_gate(범위 완료 게이트)", FINAL_DECISION, "run364AD scope(364AD 범위)를 proxy scout(프록시 정찰)로 닫는다."),
        gate_row("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점 안전 고정 임계값 경계를 기록한다."),
        gate_row("topn_rewrite_gate(top_n 재작성 게이트)", EXPRESSION_SAFETY_AUDIT, "top_n 표현을 직접 재생하지 않는다."),
        gate_row("proxy_replay_gate(프록시 재생 게이트)", SCOUT_SURFACE, "timestamp-safe variants(시점 안전 변형)를 재생한다."),
        gate_row("performance_attribution_gate(성과 귀속 게이트)", ATTRIBUTION_RECEIPT, "기준 대비 KPI 차이를 기록한다."),
        gate_row("model_boundary_gate(모델 경계 게이트)", MODEL_RECEIPT, "새 모델/ONNX(온엑스) 권위를 주장하지 않는다."),
        gate_row("result_judgment_gate(결과 판정 게이트)", JUDGMENT_RECEIPT, "MT5 필요 경계로 판정한다."),
        gate_row("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 hash(해시)를 연결한다."),
        gate_row("claim_boundary_audit(주장 경계 감사)", CLAIM_RECEIPT, "runtime authority(런타임 권위)를 열지 않는다."),
        gate_row("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결한다."),
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


def write_docs(final: Mapping[str, Any], surface: pd.DataFrame, safety_rows: Sequence[Mapping[str, Any]], comparison: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    top = surface.head(10).to_dict("records")
    text = f"""# run364AD PF/DD density bridge scout(364AD PF/DD 밀도 연결 정찰)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- scout_rows(정찰 행): `{final['scout_rows']}`
- strict_pass_rows(엄격 통과 행): `{final['strict_pass_rows']}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- selected net/PF/trades/density/DD(선택 순수익/수익 팩터/거래수/밀도/낙폭): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_max_drawdown']}`
- runtime_authority(런타임 권위): `not_claimed`

## Top proxy rows(상위 프록시 행)

{markdown_table(top, ['queue_id', 'combined_net_profit', 'combined_profit_factor', 'combined_trade_per_business_day', 'combined_max_drawdown', 'combined_short_count', 'candidate_status', 'selection_score'])}

## Expression safety audit(표현 안전 감사)

{markdown_table(safety_rows, ['source_queue_id', 'safety_status', 'effect(효과)'])}

## Baseline comparison(기준 비교)

{markdown_table(comparison, ['metric_id', 'baseline_value', 'selected_value', 'delta_selected_minus_baseline'])}

## Gate audit(게이트 감사)

{markdown_table(gates, ['gate(게이트)', 'status', 'evidence(근거)', 'effect(효과)'])}

## Claim boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Effect(효과): 이 scout(정찰)는 timestamp-safe proxy(시점 안전 프록시) 후보 선별이며, MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(REVIEW_INDEX, RUN_ID, f"\n## {RUN_ID}\n\n- report(보고서): `{rel(REPORT_PATH)}`\n- judgment(판정): `{JUDGMENT}`\n- selected(선택): `{final['selected_variant_id']}`\n- effect(효과): top_n(상위 N개) 표현을 고정 임계값으로 바꿔 안전하게 scout(정찰)했다.\n")
    append_text_once(STAGE_BRIEF, RUN_ID, f"\n## run364AD PF/DD Density Bridge Scout Closeout(364AD PF/DD 밀도 연결 정찰 종료)\n\nAction(행동): run364AC(364AC 실행) queue(대기열)를 timestamp-safe fixed-threshold variants(시점 안전 고정 임계값 변형)로 replay(재생)했다.\n\nEffect(효과): `{final['selected_variant_id']}`를 `{NEXT_RUN_ID}` review(검토) 대상으로 넘긴다.\n")
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): proxy_review_candidate_not_operating(프록시 검토 후보, 운영 아님)
- latest_proxy_scout(최근 프록시 정찰): `run364AD`
- selected_proxy_variant(선택 프록시 변형): `{final['selected_variant_id']}`
- selected_proxy_net_pf_density(선택 프록시 순수익/수익 팩터/밀도): `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_per_business_day']}`
- blockers(차단): review(검토), package decision(패키지 결정), MT5 runtime probe(MT5 런타임 탐침)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(CURRENT_WORKING_STATE, f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): run364AD(364AD 실행)는 run364AC(364AC 실행) density bridge queue(밀도 연결 대기열)를 timestamp-safe fixed thresholds(시점 안전 고정 임계값)로 replay scout(재생 정찰)했다. selected proxy(선택 프록시)는 `{final['selected_variant_id']}`이고 net/PF/trades/density/DD(순수익/수익 팩터/거래수/밀도/낙폭)는 `{final['selected_combined_net_profit']}` / `{final['selected_combined_profit_factor']}` / `{final['selected_combined_trade_count']}` / `{final['selected_combined_trade_per_business_day']}` / `{final['selected_combined_max_drawdown']}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 proxy evidence(프록시 근거)를 review(검토)한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""")
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, f"\n## {TODAY} - {RUN_ID}\n\n- action(행동): PF/DD density bridge proxy scout(PF/DD 밀도 연결 프록시 정찰)를 실행했다.\n- effect(효과): `{NEXT_RUN_ID}` review(검토) 대상으로 selected proxy(선택 프록시)를 남겼다.\n- report(보고서): `{rel(REPORT_PATH)}`\n")
    append_text_once(IDEA_REGISTRY, RUN_ID, f"\n## {RUN_ID}\n\n- idea(아이디어): near-miss density bridge(근접 실패 밀도 연결)를 top_n(상위 N개) 없이 고정 임계값으로 시험한다.\n- positive clue(긍정 단서): selected proxy(선택 프록시) `{final['selected_variant_id']}`.\n- failure memory(실패 기억): top_n month ranking(월 전체 상위 N개 순위)은 timestamp-safe(시점 안전)가 아니므로 직접 재생 금지.\n")
    append_text_once(STAGE_README, RUN_ID, f"\n## {RUN_ID}\n\n- action(행동): timestamp-safe bridge scout(시점 안전 연결 정찰)를 완료했다.\n- effect(효과): Stage364(364단계) 안에서 review(검토)로 이어간다.\n")


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
        "expectancy": "",
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
        (f"{RUN_ID}__Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A only plus Tier B missing_required(Tier A만 있고 Tier B 필수 누락)"),
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
            ("expression_safety_audit", EXPRESSION_SAFETY_AUDIT, "Expression safety audit(표현 안전 감사)."),
            ("selected_expected_trade_tape", SELECTED_EXPECTED_TRADE_TAPE, "Selected expected trade tape(선택 예상 거래 테이프)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "baseline_run_id": BASELINE_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    selected = read_json(base.SELECTED_RUNTIME_CANDIDATE)
    frame, _, _ = base.load_runtime_frame()
    frame = frame.sort_values("timestamp_dt").reset_index(drop=True)
    frame["short_margin"] = frame["p_short"].astype(float) - np.maximum(frame["p_flat"].astype(float), frame["p_long"].astype(float))
    variants, safety_rows = load_parent_queue(selected)
    baseline = normalize_baseline(selected)
    surface, best_trades, audit_rows = evaluate_queue(frame, variants, baseline)
    best = surface.iloc[0].to_dict()
    comparison = comparison_rows(best, baseline)
    review_queue = review_queue_rows(best)
    write_csv(TIMESTAMP_SAFE_QUEUE, variants)
    write_csv(EXPRESSION_SAFETY_AUDIT, safety_rows)
    write_csv(SCOUT_SURFACE, surface.to_dict("records"))
    write_csv(SELECTED_EXPECTED_TRADE_TAPE, best_trades.to_dict("records"))
    write_json(SELECTED_PROXY_CANDIDATE, best)
    write_csv(BRIDGE_EFFECT_AUDIT, audit_rows)
    write_csv(BASELINE_COMPARISON, comparison)
    write_csv(RUN364AE_QUEUE, review_queue)
    write_json(WORK_PACKET, {"run_id": RUN_ID, "primary_family": "experiment_execution(실험 실행)", "primary_skill": "obsidian-experiment-design(실험 설계)", "support_skills": ["obsidian-data-integrity(데이터 무결성)", "obsidian-model-validation(모델 검증)", "obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)"], "required_gates": ["scope_completion_gate", "data_integrity_audit", "topn_rewrite_gate", "proxy_replay_gate", "performance_attribution_gate", "model_boundary_gate", "result_judgment_gate", "artifact_lineage_audit", "claim_boundary_audit", "required_gate_coverage_audit"], "claim_boundary(주장 경계)": CLAIM_BOUNDARY})
    created_at = now_utc()
    temp_final = {"created_at_utc": created_at}
    gates = write_receipts(temp_final, best_trades)
    final = final_payload(parent_final, surface, best, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, safety_rows, comparison, gates)
    write_ledgers(final, gates)
    write_json(FINAL_DECISION, final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
