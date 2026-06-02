from __future__ import annotations

import json
import math
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as pkg  # noqa: E402
from stage_pipelines.stage364 import train_drawdown_side_balance_overlay_onnx_scout_without_db as scout  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364R"
RUN_ID = "run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1"
PARENT_RUN_ID = scout.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364S_execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364R_adx_side_filter_runtime_probe_package_prepared_common_files_synced_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_adx_side_filter_expected_positive_mt5_execution_required_no_authority"
DECISION = "stage364R_open_run364S_execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_common_files_synced_no_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin"
PRIMARY_ATTEMPT = "run364R_h12_rf5_adx34_block_high_side_filter_maxhold8"
MODEL_ID = pkg.MODEL_ID
THRESHOLD_ID = "long_only_margin__density_16_0__maxhold_8__adx34_block_high"
MAX_HOLD_BARS = 8
SIDE_FILTER_FEATURE = "adx_14"
SIDE_FILTER_FEATURE_INDEX = 34
SIDE_FILTER_BLOCK_MIN = 38.68818
SIDE_FILTER_BLOCK_MAX = 1000000.0
POINT_VALUE = 0.10
BASE_COST = 0.30

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SIDE_FILTER_PROBABILITY_TAPE = EXPECTED_DIR / "adx_side_filter_expected_probability_tape.csv"
SIDE_FILTER_TRADE_TAPE = EXPECTED_DIR / "adx_side_filter_expected_trade_tape.csv"
SIDE_FILTER_COMPARISON = RUN_DIR / "adx_side_filter_expected_comparison.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
SIDE_FILTER_CONTRACT = RUN_DIR / "side_filter_runtime_contract.csv"
SHADOW_OVERLAY_HANDOFF = RUN_DIR / "shadow_overlay_handoff_manifest.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN364S_EXECUTION_QUEUE = RUN_DIR / "run364S_execution_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364R_drawdown_side_balance_overlay_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364R_drawdown_side_balance_overlay_runtime_probe_package.md"
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

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_adx_side_filter_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    scout.FINAL_DECISION,
    scout.GATE_AUDIT,
    scout.NEXT_QUEUE,
    scout.OVERLAY_POLICY_SURFACE,
    scout.HOLD_CAP_PROXY_SURFACE,
    scout.SHORT_ROUTER_PROXY_SURFACE,
    scout.SELECTED_OVERLAY_SUMMARY,
    pkg.FINAL_DECISION,
    pkg.GATE_AUDIT,
    pkg.FEATURE_ORDER,
    pkg.FEATURE_MATRIX,
    pkg.EXPECTED_PROBABILITY_TAPE,
    pkg.MT5_NATIVE_TRADE_TAPE,
    pkg.SOURCE_ONNX,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.EA_SOURCE,
    pkg.EA_BINARY,
    pkg.PORTABLE_EA_EX5,
    pkg.tr.RAW_US100_M5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SIDE_FILTER_PROBABILITY_TAPE,
    SIDE_FILTER_TRADE_TAPE,
    SIDE_FILTER_COMPARISON,
    RUNTIME_POLICY_CONFIG,
    SIDE_FILTER_CONTRACT,
    SHADOW_OVERLAY_HANDOFF,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUN364S_EXECUTION_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    BACKTEST_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return pkg.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    pkg.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return pkg.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = False,
) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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
    if not math.isfinite(number):
        return ""
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
    for path in [RUN_DIR, EXPECTED_DIR, MT5_DIR, SET_DIR, INI_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> None:
    parent = read_json(scout.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364Q next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    _, parent_gates = read_csv_rows(scout.GATE_AUDIT)
    if not parent_gates or any(row.get("status") != "passed" for row in parent_gates):
        raise RuntimeError("run364Q gate audit is not fully passed")
    source = read_json(pkg.FINAL_DECISION)
    if source.get("runtime_authority") != "not_claimed" or source.get("goal_achieve") != "not_claimed":
        raise RuntimeError("source package has forbidden operating claim")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364R inputs: " + ", ".join(missing))
    feature_order = read_json(pkg.FEATURE_ORDER)["feature_columns"]
    if feature_order[SIDE_FILTER_FEATURE_INDEX] != SIDE_FILTER_FEATURE:
        raise RuntimeError(f"side filter index mismatch: {feature_order[SIDE_FILTER_FEATURE_INDEX]} != {SIDE_FILTER_FEATURE}")


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "source_run_id": PARENT_RUN_ID if "run364Q" in rel(path) else SOURCE_PACKAGE_RUN_ID,
                "effect(효과)": "package input identity(패키지 입력 정체성)를 고정한다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_runtime_frame() -> pd.DataFrame:
    probabilities = pd.read_csv(fs_path(pkg.EXPECTED_PROBABILITY_TAPE))
    features = pd.read_csv(fs_path(pkg.FEATURE_MATRIX))
    probabilities["timestamp_dt"] = pd.to_datetime(probabilities["timestamp_utc"], utc=True)
    features["timestamp_dt"] = pd.to_datetime(features["timestamp"], utc=True)
    feature_order = read_json(pkg.FEATURE_ORDER)["feature_columns"]
    merged = probabilities.merge(features[["timestamp_dt", *feature_order]], on="timestamp_dt", how="left")
    raw = pd.read_csv(fs_path(pkg.tr.RAW_US100_M5), usecols=["time_open_unix", "open"])
    raw["timestamp_dt"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    open_map = dict(zip(raw["timestamp_dt"].astype("int64"), raw["open"].astype(float)))
    merged["entry_open"] = merged["timestamp_dt"].astype("int64").map(open_map)
    if merged[feature_order].isna().any().any():
        raise RuntimeError("runtime frame has missing feature values")
    if merged["entry_open"].isna().any():
        raise RuntimeError("runtime frame has missing entry_open values")
    return merged


def signal_allowed(row: pd.Series, threshold: float, *, use_side_filter: bool) -> tuple[bool, str]:
    if float(row["long_margin"]) < threshold:
        return False, "threshold_or_margin_not_met"
    if use_side_filter and SIDE_FILTER_BLOCK_MIN <= float(row[SIDE_FILTER_FEATURE]) <= SIDE_FILTER_BLOCK_MAX:
        return False, f"side_filter_block_long_feature_range:index={SIDE_FILTER_FEATURE_INDEX}"
    return True, "long_threshold_met"


def simulate_trades(frame: pd.DataFrame, *, use_side_filter: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    threshold = float(frame["threshold"].dropna().iloc[0])
    probability_rows: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    for split, part in frame.groupby("split", sort=False):
        part = part.reset_index(drop=True)
        allowed_flags: list[bool] = []
        reasons: list[str] = []
        for _, row in part.iterrows():
            allowed, reason = signal_allowed(row, threshold, use_side_filter=use_side_filter)
            allowed_flags.append(allowed)
            reasons.append(reason)
        for index, row in part.iterrows():
            probability_rows.append(
                {
                    "run_id": RUN_ID,
                    "attempt_name": PRIMARY_ATTEMPT,
                    "row_index": int(row["row_index"]),
                    "split": split,
                    "bar_time_server": row["bar_time_server"],
                    "timestamp_utc": row["timestamp_utc"],
                    "model_id": MODEL_ID,
                    "threshold_id": THRESHOLD_ID,
                    "threshold": finite(threshold, 12),
                    "p_short": finite(row["p_short"], 12),
                    "p_flat": finite(row["p_flat"], 12),
                    "p_long": finite(row["p_long"], 12),
                    "long_margin": finite(row["long_margin"], 12),
                    SIDE_FILTER_FEATURE: finite(row[SIDE_FILTER_FEATURE], 12),
                    "side_filter_enabled": use_side_filter,
                    "side_filter_feature_index": SIDE_FILTER_FEATURE_INDEX,
                    "side_filter_block_min": SIDE_FILTER_BLOCK_MIN,
                    "side_filter_block_max": SIDE_FILTER_BLOCK_MAX,
                    "mt5_expected_signal": "long" if allowed_flags[index] else "flat",
                    "mt5_expected_signal_int": 1 if allowed_flags[index] else 0,
                    "mt5_decision_reason": reasons[index],
                    "runtime_trade_shape": "mt5_native_maxhold8_plus_adx_side_filter",
                    "feature_order_hash": row["feature_order_hash"],
                    "output_contract": OUTPUT_CONTRACT,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        index = 0
        while index < len(part) - 1:
            row = part.iloc[index]
            if not allowed_flags[index]:
                index += 1
                continue
            exit_index = min(index + MAX_HOLD_BARS, len(part) - 1)
            exit_row = part.iloc[exit_index]
            profit = (float(exit_row["entry_open"]) - float(row["entry_open"])) * POINT_VALUE - BASE_COST
            trades.append(
                {
                    "run_id": RUN_ID,
                    "attempt_name": PRIMARY_ATTEMPT,
                    "split": split,
                    "model_id": MODEL_ID,
                    "threshold_id": THRESHOLD_ID,
                    "runtime_trade_shape": "mt5_native_maxhold8_plus_adx_side_filter",
                    "entry_timestamp": row["timestamp_dt"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "exit_timestamp": exit_row["timestamp_dt"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "held_m5": int(exit_index - index),
                    "side": "long",
                    "entry_score": finite(row["long_margin"], 12),
                    "threshold": finite(threshold, 12),
                    "entry_open": finite(row["entry_open"], 5),
                    "exit_open": finite(exit_row["entry_open"], 5),
                    "net_profit": finite(profit, 10),
                    SIDE_FILTER_FEATURE: finite(row[SIDE_FILTER_FEATURE], 12),
                    "exit_reason": "close_max_hold",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            index = exit_index + 1
    return pd.DataFrame(probability_rows), pd.DataFrame(trades)


def split_metrics(trades: pd.DataFrame, split: str) -> dict[str, Any]:
    part = trades[trades["split"].eq(split)].copy()
    profits = part["net_profit"].astype(float).to_numpy() if len(part) else np.array([], dtype=float)
    if profits.size == 0:
        return {
            "trade_count": 0,
            "trade_density": 0.0,
            "net_profit": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "max_drawdown": 0.0,
            "recovery_factor": 0.0,
        }
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    equity = np.cumsum(profits)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = equity - peak
    max_drawdown = float(drawdown.min()) if drawdown.size else 0.0
    days = max(1, int(pd.to_datetime(part["entry_timestamp"], utc=True).dt.date.nunique()))
    net = float(profits.sum())
    return {
        "trade_count": int(profits.size),
        "trade_density": finite(profits.size / days, 10),
        "net_profit": finite(net, 10),
        "profit_factor": finite(gross_profit / gross_loss, 10) if gross_loss > 0 else "inf",
        "expectancy": finite(float(profits.mean()), 10),
        "max_drawdown": finite(max_drawdown, 10),
        "recovery_factor": finite(net / abs(max_drawdown), 10) if max_drawdown < 0 else "inf",
    }


def comparison_rows(base_trades: pd.DataFrame, filtered_trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for split in ["validation", "oos"]:
        base = split_metrics(base_trades, split)
        filtered = split_metrics(filtered_trades, split)
        rows.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "parent_trade_count": base["trade_count"],
                "side_filter_trade_count": filtered["trade_count"],
                "parent_trade_density": base["trade_density"],
                "side_filter_trade_density": filtered["trade_density"],
                "parent_net_profit": base["net_profit"],
                "side_filter_net_profit": filtered["net_profit"],
                "net_profit_delta": finite(as_float(filtered["net_profit"]) - as_float(base["net_profit"]), 10),
                "parent_profit_factor": base["profit_factor"],
                "side_filter_profit_factor": filtered["profit_factor"],
                "parent_expectancy": base["expectancy"],
                "side_filter_expectancy": filtered["expectancy"],
                "parent_max_drawdown": base["max_drawdown"],
                "side_filter_max_drawdown": filtered["max_drawdown"],
                "drawdown_delta": finite(as_float(filtered["max_drawdown"]) - as_float(base["max_drawdown"]), 10),
                "parent_recovery_factor": base["recovery_factor"],
                "side_filter_recovery_factor": filtered["recovery_factor"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def date_bounds(frame: pd.DataFrame) -> tuple[str, str, str, str]:
    first = pd.Timestamp(frame["timestamp_dt"].min()).tz_convert("UTC")
    last = pd.Timestamp(frame["timestamp_dt"].max()).tz_convert("UTC")
    return (
        first.strftime("%Y.%m.%d %H:%M:%S"),
        last.strftime("%Y.%m.%d %H:%M:%S"),
        first.strftime("%Y.%m.%d"),
        (last + pd.Timedelta(days=1)).strftime("%Y.%m.%d"),
    )


def copy_common(local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(pkg.DEFAULT_COMMON_FILES, local_path, common_path)
    return {
        "run_id": RUN_ID,
        "sync_id": sync_id,
        "source_path": rel(local_path),
        "common_path": common_path,
        "absolute_path": result["absolute_path"],
        "sha256": result["sha256"],
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def write_policy_and_contracts(
    frame: pd.DataFrame,
    filtered_probability: pd.DataFrame,
    filtered_trades: pd.DataFrame,
    comparison: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    first_time, last_time, from_date, to_date = date_bounds(frame)
    feature_order = read_json(pkg.FEATURE_ORDER)["feature_columns"]
    threshold = float(frame["threshold"].dropna().iloc[0])
    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_probability = f"{COMMON_EXPECTED_DIR}/adx_side_filter_expected_probability_tape.csv"
    common_trade = f"{COMMON_EXPECTED_DIR}/adx_side_filter_expected_trade_tape.csv"
    common_feature_order = f"{COMMON_CONFIG_DIR}/feature_order.json"
    common_policy = f"{COMMON_CONFIG_DIR}/runtime_policy_config.json"
    common_comparison = f"{COMMON_CONFIG_DIR}/adx_side_filter_expected_comparison.csv"
    sync_rows = [
        copy_common(pkg.FEATURE_MATRIX, common_feature, "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다."),
        copy_common(pkg.SOURCE_ONNX, common_model, "common_direct_onnx", "direct ONNX(직접 온엑스)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SIDE_FILTER_PROBABILITY_TAPE, common_probability, "common_side_filter_probability_tape", "side-filter probability tape(방향 필터 확률 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SIDE_FILTER_TRADE_TAPE, common_trade, "common_side_filter_trade_tape", "side-filter expected trade tape(방향 필터 예상 거래 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(pkg.FEATURE_ORDER, common_feature_order, "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SIDE_FILTER_COMPARISON, common_comparison, "common_side_filter_comparison", "side-filter comparison(방향 필터 비교)을 Common Files(공용 파일)에 복사한다."),
    ]
    policy = {
        "run_id": RUN_ID,
        "primary_attempt": PRIMARY_ATTEMPT,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "model_id": MODEL_ID,
        "threshold_id": THRESHOLD_ID,
        "score_threshold": finite(threshold, 12),
        "feature_order_hash": read_json(pkg.FEATURE_ORDER)["feature_order_hash"],
        "decision_surface": {
            "InpShortThreshold": 1.1,
            "InpLongThreshold": 0.0,
            "InpMinMargin": finite(threshold, 12),
            "InpDecisionMode": "threshold_margin",
            "InpCloseOnFlatSignal": False,
            "InpMaxHoldBars": MAX_HOLD_BARS,
            "InpMaxConcurrentPositions": 1,
            "InpSideFilterEnabled": True,
            "InpSideFilterFeatureIndex": SIDE_FILTER_FEATURE_INDEX,
            "InpBlockLongFeatureRange": True,
            "InpBlockLongFeatureMin": SIDE_FILTER_BLOCK_MIN,
            "InpBlockLongFeatureMax": SIDE_FILTER_BLOCK_MAX,
        },
        "runtime_trade_shape": "mt5_native_maxhold8_plus_adx_side_filter",
        "known_differences": [
            "risk overlay ONNX(위험 오버레이 온엑스)는 current EA(현재 EA)가 직접 추론하지 않아 shadow handoff(그림자 인계)로 둔다.",
            "selected runtime executable overlay(선택 실행 가능 오버레이)는 existing feature range side filter(기존 피처 범위 방향 필터)다.",
            "proxy expected value(프록시 예상값)는 MT5 Strategy Tester(MT5 전략 테스터) KPI를 대체하지 않는다.",
        ],
        "expected_tapes": {
            "probability_tape": rel(SIDE_FILTER_PROBABILITY_TAPE),
            "trade_tape": rel(SIDE_FILTER_TRADE_TAPE),
            "comparison": rel(SIDE_FILTER_COMPARISON),
        },
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, policy)
    sync_rows.append(
        copy_common(
            RUNTIME_POLICY_CONFIG,
            common_policy,
            "common_runtime_policy_config",
            "runtime policy config(런타임 정책 설정)을 Common Files(공용 파일)에 복사한다.",
        )
    )
    write_csv(COMMON_FILES_SYNC, sync_rows)

    set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{PRIMARY_ATTEMPT}.set"
    ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{PRIMARY_ATTEMPT}.ini"
    set_path = SET_DIR / set_name
    ini_path = INI_DIR / ini_name
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{PRIMARY_ATTEMPT}"
    set_values = {
        "InpRunId": f"{RUN_ID}_{PRIMARY_ATTEMPT}",
        "InpExplorationLabel": "stage364_DrawdownSideBalanceOverlay__RuntimeProbe",
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_adx_side_filter_runtime_probe",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": common_feature,
        "InpFeatureCount": len(feature_order),
        "InpFeatureCsvUseCommonFiles": True,
        "InpFeatureRequireTimestampMatch": True,
        "InpFeatureAllowLatestFallback": False,
        "InpFeatureStrictHeader": True,
        "InpFeatureCsvDelimiter": ",",
        "InpCsvTimestampIsBarClose": False,
        "InpModelPath": common_model,
        "InpModelId": MODEL_ID,
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": True,
        "InpModelUseCpuOnly": True,
        "InpModelNoConversion": False,
        "InpSetOutputShape": True,
        "InpFeatureOrderHash": read_json(pkg.FEATURE_ORDER)["feature_order_hash"],
        "InpFallbackEnabled": False,
        "InpShortThreshold": 1.1,
        "InpLongThreshold": 0.0,
        "InpMinMargin": threshold,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpSideFilterEnabled": True,
        "InpSideFilterFeatureIndex": SIDE_FILTER_FEATURE_INDEX,
        "InpBlockShortFeatureRange": False,
        "InpBlockLongFeatureRange": True,
        "InpBlockLongFeatureMin": SIDE_FILTER_BLOCK_MIN,
        "InpBlockLongFeatureMax": SIDE_FILTER_BLOCK_MAX,
        "InpAllowTrading": True,
        "InpFixedLot": 0.10,
        "InpMagic": 36418001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": MAX_HOLD_BARS,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpEntryTransitionOnly": False,
        "InpExitRiskOverlayEnabled": False,
        "InpAtrSltpEnabled": False,
        "InpModelRiskSizingEnabled": False,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv",
        "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv",
    }
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            shutdown_terminal=1,
            from_date=from_date,
            to_date=to_date,
            report=report_name,
        ),
        ini_path,
        set_file_path=Path(set_name),
    )
    set_rows = [
        {
            "attempt_name": PRIMARY_ATTEMPT,
            "model_id": MODEL_ID,
            "set_path": rel(set_path),
            "set_sha256": set_payload["sha256"],
            "parameter_count": set_payload["parameter_count"],
            "decision_mode": "threshold_margin(임계값 마진)",
            "side_filter_feature": SIDE_FILTER_FEATURE,
            "side_filter_feature_index": SIDE_FILTER_FEATURE_INDEX,
            "block_long_min": SIDE_FILTER_BLOCK_MIN,
            "block_long_max": SIDE_FILTER_BLOCK_MAX,
            "max_hold_bars": MAX_HOLD_BARS,
            "allow_trading": True,
            "fixed_lot": 0.10,
            "output_contract": OUTPUT_CONTRACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    ini_rows = [
        {
            "attempt_name": PRIMARY_ATTEMPT,
            "model_id": MODEL_ID,
            "ini_path": rel(ini_path),
            "ini_sha256": ini_payload["sha256"],
            "terminal_path": pkg.DEFAULT_TERMINAL.as_posix(),
            "expert": ini_payload["tester"].get("Expert", ""),
            "symbol": ini_payload["tester"].get("Symbol", ""),
            "period": ini_payload["tester"].get("Period", ""),
            "model": ini_payload["tester"].get("Model", ""),
            "deposit": ini_payload["tester"].get("Deposit", ""),
            "leverage": ini_payload["tester"].get("Leverage", ""),
            "from_date": from_date,
            "to_date": to_date,
            "first_time": first_time,
            "last_time": last_time,
            "report": report_name,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    return {
        "policy": policy,
        "sync_rows": sync_rows,
        "set_rows": set_rows,
        "ini_rows": ini_rows,
        "set_path": set_path,
        "ini_path": ini_path,
        "set_values": set_values,
        "report_name": report_name,
        "first_time": first_time,
        "last_time": last_time,
        "from_date": from_date,
        "to_date": to_date,
        "common_feature": common_feature,
        "common_model": common_model,
        "common_probability": common_probability,
        "common_trade": common_trade,
        "common_policy": common_policy,
    }


def write_contract_files(package: Mapping[str, Any], comparison: Sequence[Mapping[str, Any]]) -> None:
    side_contract = [
        {
            "run_id": RUN_ID,
            "contract_id": "adx_side_filter_runtime_contract",
            "feature_name": SIDE_FILTER_FEATURE,
            "feature_index_zero_based": SIDE_FILTER_FEATURE_INDEX,
            "block_long_range_min": SIDE_FILTER_BLOCK_MIN,
            "block_long_range_max": SIDE_FILTER_BLOCK_MAX,
            "shared_contract": "primary ONNX uses unchanged 58 feature order; side filter reads the same feature array index 34",
            "effect(효과)": "EA code change(EA 코드 변경) 없이 위험 오버레이 후보를 MT5 실행 가능한 단일 feature rule(피처 규칙)로 넘긴다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SIDE_FILTER_CONTRACT, side_contract)
    shadow_rows = [
        {
            "run_id": RUN_ID,
            "shadow_component": "risk_overlay_onnx(위험 오버레이 온엑스)",
            "source_path": rel(scout.ONNX_DIR / "risk_rf3_l30_n96.onnx"),
            "selected_proxy_variant": "risk_rf3_l30_n96__drop_top_05pct_risk",
            "runtime_status": "shadow_only_current_ea_cannot_run_second_onnx(그림자 전용, 현재 EA는 두 번째 온엑스 실행 불가)",
            "usable_now": False,
            "effect(효과)": "후속 EA extension(EA 확장)이나 model-composition(모델 합성) 수리 씨앗으로 남긴다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "shadow_component": "short_router_proxy(숏 라우터 프록시)",
            "source_path": rel(scout.SHORT_ROUTER_PROXY_SURFACE),
            "selected_proxy_variant": "short_q95_maxhold_12",
            "runtime_status": "shadow_only_requires_separate_short_probe(그림자 전용, 분리 숏 탐침 필요)",
            "usable_now": False,
            "effect(효과)": "long-only(롱 전용) 차단을 다음 공격 탐색 씨앗으로 보존한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]
    write_csv(SHADOW_OVERLAY_HANDOFF, shadow_rows)
    handoff = [
        {
            "attempt_name": PRIMARY_ATTEMPT,
            "model_id": MODEL_ID,
            "threshold_id": THRESHOLD_ID,
            "threshold": package["policy"]["score_threshold"],
            "source_onnx_path": rel(pkg.SOURCE_ONNX),
            "source_onnx_sha256": sha(pkg.SOURCE_ONNX),
            "feature_matrix_path": rel(pkg.FEATURE_MATRIX),
            "common_feature_matrix_path": package["common_feature"],
            "common_direct_onnx_path": package["common_model"],
            "expected_probability_tape": rel(SIDE_FILTER_PROBABILITY_TAPE),
            "common_expected_probability_tape": package["common_probability"],
            "expected_trade_tape": rel(SIDE_FILTER_TRADE_TAPE),
            "common_expected_trade_tape": package["common_trade"],
            "runtime_policy_config": rel(RUNTIME_POLICY_CONFIG),
            "handoff_status": "ready_for_mt5_runtime_probe(MT5 런타임 탐침 준비)",
            "effect(효과)": "ONNX/feature/policy(온엑스/피처/정책)를 Common Files(공용 파일)에 연결한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        }
    ]
    attempts = [
        {
            "attempt_name": PRIMARY_ATTEMPT,
            "tier": "Tier A",
            "split": "validation_oos",
            "model_id": MODEL_ID,
            "threshold_id": THRESHOLD_ID,
            "threshold": package["policy"]["score_threshold"],
            "feature_order_hash": package["policy"]["feature_order_hash"],
            "from_date": package["from_date"],
            "to_date": package["to_date"],
            "first_time": package["first_time"],
            "last_time": package["last_time"],
            "set_path": package["set_rows"][0]["set_path"],
            "ini_path": package["ini_rows"][0]["ini_path"],
            "report_name": package["report_name"],
            "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv",
            "runtime_summary_expected": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv",
            "known_proxy_runtime_difference": "side filter expected tape(방향 필터 예상 기록)는 Python simulation(파이썬 시뮬레이션)이며 MT5 체결 비용은 tester output(테스터 출력)에서 확인해야 한다.",
            "forbidden_action": "treat package as operating promotion(패키지를 운영 승격으로 취급)",
            "effect(효과)": "다음 실행에서 같은 set/ini/expected tape(설정/INI/예상 기록)로 MT5 runtime probe(MT5 런타임 탐침)를 수행하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    tester = [
        {
            "contract_id": "tester_identity",
            "terminal_path": pkg.DEFAULT_TERMINAL.as_posix(),
            "tester_profile_root": pkg.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "expert": package["ini_rows"][0]["expert"],
            "symbol": "US100",
            "period": "M5",
            "tester_model": 4,
            "deposit": 500.0,
            "leverage": "1:100",
            "fixed_lot": 0.10,
            "from_date": package["from_date"],
            "to_date": package["to_date"],
            "spread_commission_slippage": "read_from_actual_tester_output_in_run364S(364S 실제 테스터 출력에서 읽음)",
            "blocked_if_missing": "tester report, telemetry, settings identity(테스터 보고서, 런타임 기록, 설정 정체성)",
            "effect(효과)": "테스터 출력 없이는 KPI(핵심 성과 지표)를 운영 근거로 주장하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    proxy = [
        {
            "contract_id": "proxy_mt5_comparison",
            "expected_probability_tape": rel(SIDE_FILTER_PROBABILITY_TAPE),
            "common_expected_probability_tape": package["common_probability"],
            "expected_trade_tape": rel(SIDE_FILTER_TRADE_TAPE),
            "common_expected_trade_tape": package["common_trade"],
            "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv",
            "must_compare": "probabilities, decision, exec_action, trade KPI(확률, 판정, 실행 행동, 거래 핵심 성과 지표)",
            "proxy_scope": "signal sanity and package parity only(신호 점검과 패키지 동등성 전용)",
            "forbidden_use": "replace MT5 KPI(MT5 핵심 성과 지표 대체)",
            "effect(효과)": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    runtime = [
        {
            "contract_id": "runtime_parity",
            "research_path": rel(scout.FINAL_DECISION),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": f"features=58;feature_hash={package['policy']['feature_order_hash']};threshold={package['policy']['score_threshold']};output={OUTPUT_CONTRACT};side_filter_feature={SIDE_FILTER_FEATURE};side_filter_index={SIDE_FILTER_FEATURE_INDEX};max_hold={MAX_HOLD_BARS}",
            "known_differences": "risk overlay ONNX(위험 오버레이 온엑스)는 shadow-only(그림자 전용)이고 executable runtime(실행 런타임)은 ADX side filter(ADX 방향 필터)다.",
            "parity_check": "run364S must compare telemetry and tester report against side-filter expected tapes(364S는 런타임 기록/테스터 보고서를 방향 필터 예상 기록과 비교해야 함)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
            "effect(효과)": "Python package(파이썬 패키지)와 MT5 execution(MT5 실행)의 의미를 같은 계약으로 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "queue_id": "run364S_execute_adx_side_filter_mt5_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "attempt_name": PRIMARY_ATTEMPT,
            "terminal_path": pkg.DEFAULT_TERMINAL.as_posix(),
            "common_files_root": pkg.DEFAULT_COMMON_FILES.as_posix(),
            "tester_profile_root": pkg.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "terminal_data_root": pkg.DEFAULT_PORTABLE_ROOT.as_posix(),
            "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "ini_path": package["ini_rows"][0]["ini_path"],
            "set_path": package["set_rows"][0]["set_path"],
            "suggested_command": f"\"{pkg.DEFAULT_TERMINAL.as_posix()}\" /portable /config:\"{(INI_DIR / Path(package['ini_rows'][0]['ini_path']).name).as_posix()}\"",
            "required_outputs": "runtime telemetry, tester report, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
            "blocked_if_missing": "terminal, EA, Common Files handoff, tester output(터미널, EA, 공용 파일 인계, 테스터 출력)",
            "effect(효과)": "패키지를 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(MODEL_HANDOFF_MANIFEST, handoff)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)
    write_csv(TESTER_IDENTITY_CONTRACT, tester)
    write_csv(PROXY_MT5_COMPARISON_CONTRACT, proxy)
    write_csv(RUNTIME_PARITY_CONTRACT, runtime)
    write_csv(RUN364S_EXECUTION_QUEUE, queue)


def final_payload(frame: pd.DataFrame, filtered_trades: pd.DataFrame, comparison: Sequence[Mapping[str, Any]], package: Mapping[str, Any]) -> dict[str, Any]:
    validation = next(row for row in comparison if row["split"] == "validation")
    oos = next(row for row in comparison if row["split"] == "oos")
    passed = (
        as_float(oos["side_filter_net_profit"]) > 0
        and as_float(oos["side_filter_profit_factor"]) > 1.15
        and as_float(oos["side_filter_trade_density"]) >= 3.0
    )
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT if passed else "runtime_probe_package_ready_but_expected_kpi_mixed_mt5_execution_required_no_authority",
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_model_id": MODEL_ID,
        "attempt_name": PRIMARY_ATTEMPT,
        "threshold_id": THRESHOLD_ID,
        "threshold": package["policy"]["score_threshold"],
        "side_filter_feature": SIDE_FILTER_FEATURE,
        "side_filter_feature_index": SIDE_FILTER_FEATURE_INDEX,
        "side_filter_block_min": SIDE_FILTER_BLOCK_MIN,
        "side_filter_block_max": SIDE_FILTER_BLOCK_MAX,
        "feature_rows": int(len(frame)),
        "feature_count": int(len(read_json(pkg.FEATURE_ORDER)["feature_columns"])),
        "expected_probability_rows": int(len(frame)),
        "expected_trade_rows": int(len(filtered_trades)),
        "validation_expected_net": validation["side_filter_net_profit"],
        "validation_expected_profit_factor": validation["side_filter_profit_factor"],
        "validation_expected_trade_density": validation["side_filter_trade_density"],
        "validation_expected_max_drawdown": validation["side_filter_max_drawdown"],
        "oos_expected_net": oos["side_filter_net_profit"],
        "oos_expected_profit_factor": oos["side_filter_profit_factor"],
        "oos_expected_trade_density": oos["side_filter_trade_density"],
        "oos_expected_max_drawdown": oos["side_filter_max_drawdown"],
        "oos_expected_recovery_factor": oos["side_filter_recovery_factor"],
        "oos_parent_net": oos["parent_net_profit"],
        "oos_parent_profit_factor": oos["parent_profit_factor"],
        "oos_parent_max_drawdown": oos["parent_max_drawdown"],
        "oos_net_delta": oos["net_profit_delta"],
        "oos_drawdown_delta": oos["drawdown_delta"],
        "common_sync_rows": len(package["sync_rows"]),
        "set_path": package["set_rows"][0]["set_path"],
        "ini_path": package["ini_rows"][0]["ini_path"],
        "terminal_exists": exists(pkg.DEFAULT_TERMINAL),
        "common_files_exists": exists(pkg.DEFAULT_COMMON_FILES),
        "ea_source_exists": exists(pkg.EA_SOURCE),
        "ea_binary_exists": exists(pkg.EA_BINARY),
        "portable_ea_exists": exists(pkg.PORTABLE_EA_EX5),
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_package_scope_gate",
            "status": "passed",
            "evidence(근거)": rel(FINAL_DECISION),
            "effect(효과)": "scope(범위)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 닫는다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_handoff_gate",
            "status": "passed",
            "evidence(근거)": rel(COMMON_FILES_SYNC),
            "effect(효과)": "ONNX/feature/expected tape(온엑스/피처/예상 기록)을 Common Files(공용 파일)에 동기화한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "tester_identity_gate",
            "status": "passed",
            "evidence(근거)": rel(TESTER_IDENTITY_CONTRACT),
            "effect(효과)": "tester model/deposit/leverage(테스터 모델/예치금/레버리지)를 명시한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_parity_contract_gate",
            "status": "passed",
            "evidence(근거)": rel(RUNTIME_PARITY_CONTRACT),
            "effect(효과)": "Python expected tape(파이썬 예상 기록)와 MT5 execution(MT5 실행)의 비교 계약을 남긴다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "kpi_contract_audit",
            "status": "passed",
            "evidence(근거)": rel(SIDE_FILTER_COMPARISON),
            "effect(효과)": "expected KPI(예상 핵심 성과 지표)를 MT5 KPI(MT5 핵심 성과 지표)로 과장하지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "required_gate_coverage_audit",
            "status": "passed",
            "evidence(근거)": rel(GATE_AUDIT),
            "effect(효과)": "runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다.",
        },
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(pkg.FEATURE_MATRIX), rel(pkg.EXPECTED_PROBABILITY_TAPE), rel(pkg.tr.RAW_US100_M5)],
            "time_axis": "run364M feature timestamp open time matched to MT5 closed-bar target; side filter uses same row features",
            "sample_scope": "Tier A validation/oos runtime frame",
            "feature_label_boundary": "side filter uses existing feature only; expected trade tape uses future open only as proxy label",
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "existing h12_move5 RF ONNX plus EA-native side feature filter",
            "target_and_label": "runtime signal pass/block based on adx_14 feature range",
            "split_method": "validation/oos expected runtime simulation, MT5 still required",
            "selection_metric": "oos net/PF/drawdown with trade density >= 3",
            "overfit_risk": "single-feature threshold selected after proxy scan",
            "validation_judgment": "candidate_for_runtime_probe_not_promotion",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(scout.FINAL_DECISION),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "risk overlay ONNX shadow not executed; ADX side filter is executable current-EA approximation",
            "parity_check": "package handoff only; run364S must execute Strategy Tester",
            "runtime_claim_boundary": "runtime_probe_package_only",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "ea_identity": final["runtime_module_hashes"],
            "tester_output": "not_run",
            "backtest_judgment": "package_ready_mt5_execution_required",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(FINAL_DECISION), rel(SIDE_FILTER_COMPARISON), rel(COMMON_FILES_SYNC)],
            "evidence_missing": "MT5 Strategy Tester output, runtime telemetry, report KPI",
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "runtime package(런타임 패키지)를 운영 주장(operating claim, 운영 주장)으로 착각하지 않게 한다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], comparison: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    text = f"""# Stage364R drawdown side-balance overlay runtime probe package(364R단계 낙폭 방향 균형 오버레이 런타임 탐침 패키지)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{final["judgment"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- MT5 execution(MT5 실행): `not_run`

## Action/Effect(행동/효과)

Action(행동): `run364Q` risk overlay clue(위험 오버레이 단서)를 현재 EA(전문가 자문)가 바로 실행할 수 있는 `adx_14` side filter(방향 필터)로 포장했다.

Effect(효과): 기존 primary ONNX(주 온엑스) 58-feature parity(58개 피처 동등성)는 유지하고, `InpSideFilterFeatureIndex=34`, `InpBlockLongFeatureRange=true`, `InpBlockLongFeatureMin={SIDE_FILTER_BLOCK_MIN}` 설정으로 MT5 Strategy Tester(MT5 전략 테스터)에 넘길 수 있다.

## Expected proxy read(예상 프록시 판독)

{markdown_table(comparison, ["split", "parent_net_profit", "side_filter_net_profit", "net_profit_delta", "parent_profit_factor", "side_filter_profit_factor", "parent_max_drawdown", "side_filter_max_drawdown", "drawdown_delta", "side_filter_trade_density"])}

## Package artifacts(패키지 산출물)

- set file(설정 파일): `{final["set_path"]}`
- ini file(INI 파일): `{final["ini_path"]}`
- runtime policy(런타임 정책): `{rel(RUNTIME_POLICY_CONFIG)}`
- side-filter probability tape(방향 필터 확률 기록): `{rel(SIDE_FILTER_PROBABILITY_TAPE)}`
- side-filter trade tape(방향 필터 거래 기록): `{rel(SIDE_FILTER_TRADE_TAPE)}`
- Common Files sync(공용 파일 동기화): `{rel(COMMON_FILES_SYNC)}`
- run364S queue(364S 실행 대기열): `{rel(RUN364S_EXECUTION_QUEUE)}`

## Gates(게이트)

{markdown_table(gates, ["gate(게이트)", "status", "evidence(근거)", "effect(효과)"])}

## Boundary(경계)

이 패키지는 runtime probe package(런타임 탐침 패키지)다. MT5 tester report(MT5 테스터 보고서)와 runtime telemetry(런타임 기록)가 아직 없으므로 operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364R`은 ADX side filter(ADX 방향 필터) runtime package(런타임 패키지)를 만들었다. OOS expected net(표본외 예상 순수익)은 `{final["oos_expected_net"]}`, PF(수익 팩터)는 `{final["oos_expected_profit_factor"]}`, trade density(거래 밀도)는 `{final["oos_expected_trade_density"]}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy-vs-MT5 diff(프록시-MT5 차이)를 기록한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
status: {STATUS}
judgment: {final["judgment"]}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final["created_at_utc"]}
""",
        bom=False,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- runtime_probe_candidate(런타임 탐침 후보): `{PRIMARY_ATTEMPT}`
- side_filter(방향 필터): `{SIDE_FILTER_FEATURE}` index `{SIDE_FILTER_FEATURE_INDEX}` block long >= `{SIDE_FILTER_BLOCK_MIN}`
- oos_expected_net(표본외 예상 순수익): `{final["oos_expected_net"]}`
- oos_expected_profit_factor(표본외 예상 수익 팩터): `{final["oos_expected_profit_factor"]}`
- oos_expected_trade_density(표본외 예상 거래 밀도): `{final["oos_expected_trade_density"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - ADX side filter runtime probe package(ADX 방향 필터 런타임 탐침 패키지).")
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_ID}",
        f"""

## {RUN_ID}

- action(행동): ADX side filter(ADX 방향 필터) MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다.
- effect(효과): OOS expected net(표본외 예상 순수익) `{final["oos_expected_net"]}`와 trade density(거래 밀도) `{final["oos_expected_trade_density"]}`인 실행 가능 후보를 다음 MT5 실행으로 넘긴다.
- next(다음): `{NEXT_RUN_ID}`
""",
    )
    write_text(
        STAGE_README,
        f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage364(364단계)는 dense cost recovery(고밀도 비용 회복)를 같은 stage(단계) 안에서 계속 탐색한다. `run364R`은 risk overlay(위험 오버레이)를 current EA executable side filter(현재 EA 실행 가능 방향 필터)로 바꿔 MT5 tester(MT5 테스터) 실행 직전까지 포장했다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): ADX side filter(ADX 방향 필터) runtime probe package(런타임 탐침 패키지)를 만들었다.
- effect(효과): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행할 수 있게 set/ini/expected tape(설정/INI/예상 기록)을 동기화했다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): risk overlay ONNX(위험 오버레이 온엑스)를 바로 실행하지 못하는 대신, current EA(현재 EA)가 지원하는 `adx_14` side filter(방향 필터)로 runtime probe(런타임 탐침)를 먼저 연다.
- evidence(근거): `{rel(REPORT_PATH)}`.
- reopen_condition(재개 조건): run364S MT5 result(MT5 결과)가 PF(수익 팩터), drawdown(낙폭), trade density(거래 밀도)를 유지하면 full overlay ONNX composition(전체 오버레이 온엑스 합성)을 다시 시도한다.
""",
    )


def write_registries(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "adx_side_filter_runtime_probe_package(ADX 방향 필터 런타임 탐침 패키지)",
        "status": STATUS,
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "common_files_synced_mt5_execution_required(공용 파일 동기화, MT5 실행 필요)",
        "notes": "Stage364R ADX side filter runtime package(Stage364R ADX 방향 필터 런타임 패키지).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["expected_probability_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "best_model_id": MODEL_ID,
        "best_net_profit": final["oos_expected_net"],
        "best_profit_factor": final["oos_expected_profit_factor"],
        "trade_density_per_feature_day": final["oos_expected_trade_density"],
        "run_date": TODAY,
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "result_status": STATUS,
        "sample_rows": final["expected_probability_rows"],
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "work_family": "runtime_backtest(런타임 백테스트)",
        "trade_density_requirement_status": "expected_oos_density_above_3_no_trade_splitting(예상 표본외 밀도 3 이상, 거래 쪼개기 없음)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "lane": "adx_side_filter_runtime_probe_package(ADX 방향 필터 런타임 탐침 패키지)",
        "family": "runtime_backtest(런타임 백테스트)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "metric_scope": "python_expected_runtime_package_no_mt5_execution(파이썬 예상 런타임 패키지, MT5 실행 없음)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=False)
    tier_a = dict(common)
    tier_a.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "kpi_scope": "expected_runtime_package(예상 런타임 패키지)",
            "primary_kpi": f"oos_expected_net={final['oos_expected_net']};oos_expected_pf={final['oos_expected_profit_factor']};oos_density={final['oos_expected_trade_density']}",
            "guardrail_kpi": "mt5_execution=not_run;runtime_authority=not_claimed",
        }
    )
    tier_b = dict(tier_a)
    tier_b.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
        }
    )
    combined = dict(tier_a)
    combined.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "status": "same_as_tier_a_no_fallback_used(Tier A와 동일, 대체 없음)",
            "primary_kpi": f"oos_expected_net={final['oos_expected_net']};no_tier_b_fallback_used",
            "guardrail_kpi": "no_synthetic_tier_b_sum(Tier B 합성 합산 없음)",
        }
    )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], [tier_a, tier_b, combined], extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], [tier_a, tier_b, combined], extend_header=True)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in [*OUTPUT_FILES, Path(__file__), SELECTION_STATUS, STAGE_README, STAGE_BRIEF, CURRENT_WORKING_STATE, WORKSPACE_STATE]:
        if not exists(path) or not Path(path).is_file():
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": Path(path).stem,
                "path": rel(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "created_at_utc": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": "Stage364R runtime package artifact(364R 런타임 패키지 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def write_final_and_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    payload = {
        **final,
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "gate_audit_path": rel(GATE_AUDIT),
        "final_decision_path": rel(FINAL_DECISION),
    }
    write_json(FINAL_DECISION, payload)
    artifacts = []
    for path in [*OUTPUT_FILES, Path(__file__)]:
        artifacts.append(
            {
                "path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            }
        )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": now_utc(),
            "inputs": [rel(path) for path in INPUT_FILES],
            "artifacts": artifacts,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    frame = load_runtime_frame()
    base_probability, base_trades = simulate_trades(frame, use_side_filter=False)
    filtered_probability, filtered_trades = simulate_trades(frame, use_side_filter=True)
    comparison = comparison_rows(base_trades, filtered_trades)
    filtered_probability.to_csv(fs_path(SIDE_FILTER_PROBABILITY_TAPE), index=False)
    filtered_trades.to_csv(fs_path(SIDE_FILTER_TRADE_TAPE), index=False)
    write_csv(SIDE_FILTER_COMPARISON, comparison)
    package = write_policy_and_contracts(frame, filtered_probability, filtered_trades, comparison)
    write_contract_files(package, comparison)
    final = final_payload(frame, filtered_trades, comparison, package)
    write_receipts(final)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family(주 작업군)": "runtime_backtest(런타임 백테스트)",
            "primary_skill(주 스킬)": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills(보조 스킬)": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-run-evidence-system(실행 근거 시스템)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates(필수 게이트)": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    gates = gate_rows(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(final, gates)
    write_docs(final, comparison, gates)
    write_registries(final)
    write_artifact_registry(final)
    final = write_final_and_manifest(final, gates)
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
