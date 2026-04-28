from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.mt5 import runtime_support as mt5


PACKET_ID_DEFAULT = "kpi_tier_balance_completion_v1"
ROOT = Path(__file__).resolve().parents[2]
RUNS_ROOT = ROOT / "stages"
COMMON_FILES_ROOT_DEFAULT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
TERMINAL_DATA_ROOT_DEFAULT = ROOT.parents[2]
TESTER_PROFILE_ROOT_DEFAULT = ROOT.parents[1] / "Profiles" / "Tester"
TERMINAL_PATH_DEFAULT = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe")
METAEDITOR_PATH_DEFAULT = Path(r"C:\Program Files\MetaTrader 5\metaeditor64.exe")
EA_TESTER_SET_NAME = "ObsidianPrimeV2_RuntimeProbeEA.set"

STAGE11_ID = "11_alpha_robustness__wfo_label_horizon_sensitivity"
STAGE12_ID = "12_model_family_challenge__extratrees_training_effect"
STAGE11_RUNS = RUNS_ROOT / STAGE11_ID / "02_runs"
STAGE12_RUNS = RUNS_ROOT / STAGE12_ID / "02_runs"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"

MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
RAW_ROOT = ROOT / "data/raw/mt5_bars/m5"
RUN03D_VARIANT_RESULTS = STAGE12_RUNS / "run03D_et_standalone_batch20_v1/results/variant_results.csv"

SUMMARY_COLUMNS = (
    "run_id",
    "stage_id",
    "source_run_id",
    "attempt_name",
    "split",
    "tier_scope",
    "route_role",
    "tester_status",
    "runtime_status",
    "report_status",
    "net_profit",
    "profit_factor",
    "trade_count",
    "report_path",
)

TARGET_COLUMNS = (
    "new_run_id",
    "source_run_id",
    "stage_id",
    "stage_number",
    "completion_goal",
    "required_views",
    "status",
    "reason",
)


@dataclass(frozen=True)
class Run02Target:
    new_run_id: str
    run_number: str
    source_run_id: str
    exploration_label: str
    completion_goal: str


RUN02_TARGETS: tuple[Run02Target, ...] = (
    Run02Target(
        new_run_id="run02AL_lgbm_fwd18_direct_tier_balance_v1",
        run_number="run02AL",
        source_run_id="run02X_lgbm_fwd18_rank_threshold_v1",
        exploration_label="stage11_TierBalance__Run02XDirect",
        completion_goal="add_tier_a_tier_b_and_keep_actual_routed_total",
    ),
    Run02Target(
        new_run_id="run02AM_lgbm_fwd18_inverse_tier_balance_v1",
        run_number="run02AM",
        source_run_id="run02Y_lgbm_fwd18_inverse_rank_threshold_v1",
        exploration_label="stage11_TierBalance__Run02YInverse",
        completion_goal="add_tier_a_tier_b_and_keep_actual_routed_total",
    ),
    Run02Target(
        new_run_id="run02AN_lgbm_fwd18_ctx_adx20_tier_balance_v1",
        run_number="run02AN",
        source_run_id="run02AC_lgbm_fwd18_inverse_rank_context_adx20_tier_a_only_v1",
        exploration_label="stage11_TierBalance__Run02ACAdx20",
        completion_goal="add_tier_b_and_actual_routed_total_for_prior_tier_a_only_context_stress",
    ),
    Run02Target(
        new_run_id="run02AO_lgbm_fwd18_ctx_adx25_tier_balance_v1",
        run_number="run02AO",
        source_run_id="run02AD_lgbm_fwd18_inverse_rank_context_adx25_tier_a_only_v1",
        exploration_label="stage11_TierBalance__Run02ADAdx25",
        completion_goal="add_tier_b_and_actual_routed_total_for_prior_tier_a_only_context_stress",
    ),
    Run02Target(
        new_run_id="run02AP_lgbm_fwd18_ctx_adx30_tier_balance_v1",
        run_number="run02AP",
        source_run_id="run02AE_lgbm_fwd18_inverse_rank_context_adx30_tier_a_only_v1",
        exploration_label="stage11_TierBalance__Run02AEAdx30",
        completion_goal="add_tier_b_and_actual_routed_total_for_prior_tier_a_only_context_stress",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True) + "\n")


def safe_name(value: str, limit: int = 96) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def common_run_root(stage_number: int, run_id: str) -> str:
    return f"Project_Obsidian_Prime_v2/stage{stage_number}/{run_id}"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def copy_file(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def copy_to_common(local_path: Path, common_path: str, common_root: Path) -> dict[str, Any]:
    destination = common_root / Path(common_path)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(local_path), io_path(destination))
    return {
        "source": rel(local_path),
        "common_path": common_path,
        "absolute_path": destination.as_posix(),
        "sha256": sha256_file_lf_normalized(destination),
    }


def parse_set(path: Path) -> dict[str, str]:
    text = io_path(path).read_text(encoding="utf-8-sig")
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def parse_ini(path: Path) -> dict[str, str]:
    text = io_path(path).read_text(encoding="utf-8-sig")
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.startswith("[") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=foundation.control_plane.mt5_tier_balance_completion"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": path.as_posix(), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": path.as_posix(), "sha256": sha256_file_lf_normalized(path), "format": "mt5_tester_ini", "tester": dict(values)}


def attempt_payload(
    *,
    run_root: Path,
    run_id: str,
    stage_number: int,
    exploration_label: str,
    attempt_name: str,
    tier: str,
    split: str,
    model_path: str,
    model_id: str,
    feature_path: str,
    feature_count: int,
    feature_order_hash: str,
    short_threshold: float,
    long_threshold: float,
    min_margin: float,
    invert_signal: bool,
    from_date: str,
    to_date: str,
    primary_active_tier: str,
    attempt_role: str,
    record_view_prefix: str,
    max_hold_bars: int,
    common_root: str,
    fallback_enabled: bool = False,
    fallback_model_path: str | None = None,
    fallback_model_id: str | None = None,
    fallback_feature_path: str | None = None,
    fallback_feature_count: int | None = None,
    fallback_feature_order_hash: str | None = None,
    fallback_short_threshold: float | None = None,
    fallback_long_threshold: float | None = None,
    fallback_min_margin: float | None = None,
    fallback_invert_signal: bool | None = None,
) -> dict[str, Any]:
    set_path = run_root / "mt5" / f"{attempt_name}.set"
    ini_path = run_root / "mt5" / f"{attempt_name}.ini"
    telemetry = f"{common_root}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{common_root}/telemetry/{attempt_name}_summary.csv"
    values: dict[str, Any] = {
        "InpRunId": run_id,
        "InpExplorationLabel": exploration_label,
        "InpTierLabel": tier,
        "InpPrimaryActiveTier": primary_active_tier,
        "InpSplitLabel": split,
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpModelPath": model_path,
        "InpModelId": model_id,
        "InpModelUseCommonFiles": "true",
        "InpFeatureCsvPath": feature_path,
        "InpFeatureCount": int(feature_count),
        "InpFeatureCsvUseCommonFiles": "true",
        "InpFeatureRequireTimestampMatch": "true",
        "InpFeatureAllowLatestFallback": "false",
        "InpFeatureStrictHeader": "true",
        "InpCsvTimestampIsBarClose": "true",
        "InpFeatureOrderHash": feature_order_hash,
        "InpFallbackEnabled": bool(fallback_enabled),
        "InpFallbackTierLabel": "Tier B partial-context fallback",
        "InpFallbackFeatureCsvPath": fallback_feature_path or feature_path,
        "InpFallbackFeatureCount": int(fallback_feature_count or feature_count),
        "InpFallbackModelPath": fallback_model_path or model_path,
        "InpFallbackModelId": fallback_model_id or model_id,
        "InpFallbackFeatureOrderHash": fallback_feature_order_hash or feature_order_hash,
        "InpTelemetryCsvPath": telemetry,
        "InpSummaryCsvPath": summary,
        "InpTelemetryUseCommonFiles": "true",
        "InpShortThreshold": float(short_threshold),
        "InpLongThreshold": float(long_threshold),
        "InpMinMargin": float(min_margin),
        "InpInvertSignal": bool(invert_signal),
        "InpFallbackShortThreshold": float(fallback_short_threshold if fallback_short_threshold is not None else short_threshold),
        "InpFallbackLongThreshold": float(fallback_long_threshold if fallback_long_threshold is not None else long_threshold),
        "InpFallbackMinMargin": float(fallback_min_margin if fallback_min_margin is not None else min_margin),
        "InpFallbackInvertSignal": bool(fallback_invert_signal if fallback_invert_signal is not None else invert_signal),
        "InpAllowTrading": "true",
        "InpFixedLot": 0.1,
        "InpMaxHoldBars": int(max_hold_bars),
        "InpMaxConcurrentPositions": 1,
        "InpMagic": 1001001 if tier == mt5.TIER_A else 1001002 if tier == mt5.TIER_B else 1001010,
    }
    set_payload = write_set(set_path, values)
    report_name = f"Project_Obsidian_Prime_v2_{run_id}_{attempt_name}"
    ini_payload = write_ini(
        ini_path,
        {
            "Expert": r"Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5",
            "Symbol": "US100",
            "Period": "M5",
            "Model": 4,
            "Deposit": 500,
            "Leverage": "1:100",
            "Optimization": 0,
            "ExecutionMode": 0,
            "ForwardMode": 0,
            "UseLocal": 1,
            "UseRemote": 0,
            "UseCloud": 0,
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
            "FromDate": from_date,
            "ToDate": to_date,
            "Report": report_name,
            "ExpertParameters": EA_TESTER_SET_NAME,
        },
    )
    payload = {
        "attempt_name": attempt_name,
        "tier": tier,
        "split": split,
        "attempt_role": attempt_role,
        "record_view_prefix": record_view_prefix,
        "set": set_payload,
        "ini": ini_payload,
        "common_telemetry_path": telemetry,
        "common_summary_path": summary,
        "max_hold_bars": int(max_hold_bars),
    }
    if fallback_enabled:
        payload["routing_mode"] = mt5.ROUTING_MODE_A_B_FALLBACK
        payload["routing_detail"] = "tier_a_primary_tier_b_partial_context_fallback"
        payload["fallback_enabled"] = True
    return payload


def source_split_dates(source_root: Path, split: str) -> tuple[str, str]:
    values = parse_ini(source_root / "mt5" / f"routed_{split}.ini")
    return values["FromDate"], values["ToDate"]


def split_dates_from_frame(frame: pd.DataFrame, split_name: str) -> tuple[str, str]:
    split = frame.loc[frame["split"].astype(str).eq(split_name)]
    if split.empty:
        raise RuntimeError(f"empty split: {split_name}")
    timestamps = pd.to_datetime(split["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def source_rule_values(source_root: Path) -> dict[str, Any]:
    values = parse_set(source_root / "mt5/routed_validation_is.set")
    return {
        "short_threshold": float(values["InpShortThreshold"]),
        "long_threshold": float(values["InpLongThreshold"]),
        "min_margin": float(values["InpMinMargin"]),
        "invert_signal": bool_value(values.get("InpInvertSignal", "false")),
        "fallback_short_threshold": float(values["InpFallbackShortThreshold"]),
        "fallback_long_threshold": float(values["InpFallbackLongThreshold"]),
        "fallback_min_margin": float(values["InpFallbackMinMargin"]),
        "fallback_invert_signal": bool_value(values.get("InpFallbackInvertSignal", "false")),
        "max_hold_bars": int(float(values["InpMaxHoldBars"])),
        "tier_a_hash": values["InpFeatureOrderHash"],
        "tier_b_hash": values["InpFallbackFeatureOrderHash"],
    }


def prepare_run02_target(target: Run02Target, common_root: Path) -> dict[str, Any]:
    source_root = STAGE11_RUNS / target.source_run_id
    run_root = STAGE11_RUNS / target.new_run_id
    if not path_exists(source_root):
        raise FileNotFoundError(source_root)
    io_path(run_root / "models").mkdir(parents=True, exist_ok=True)
    io_path(run_root / "mt5").mkdir(parents=True, exist_ok=True)

    common = common_run_root(11, target.new_run_id)
    copied = []
    model_map = {
        "tier_a": ("tier_a_lgbm_58_model.onnx", 58, "tier_a_58_feature_order.txt"),
        "tier_b": ("tier_b_lgbm_core42_model.onnx", 42, "tier_b_core42_feature_order.txt"),
    }
    for _tier, (model_name, _count, order_name) in model_map.items():
        copied.append(copy_file(source_root / "models" / model_name, run_root / "models" / model_name))
        copied.append(copy_file(source_root / "models" / order_name, run_root / "models" / order_name))
        copied.append(copy_to_common(run_root / "models" / model_name, f"{common}/models/{model_name}", common_root))
    for split in ("validation_is", "oos"):
        for prefix in ("tier_a", "tier_b"):
            matrix_name = f"{prefix}_{split}_feature_matrix.csv"
            copied.append(copy_file(source_root / "mt5" / matrix_name, run_root / "mt5" / matrix_name))
            copied.append(copy_to_common(run_root / "mt5" / matrix_name, f"{common}/features/{matrix_name}", common_root))

    rule = source_rule_values(source_root)
    attempts: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        from_date, to_date = source_split_dates(source_root, split)
        attempts.append(
            attempt_payload(
                run_root=run_root,
                run_id=target.new_run_id,
                stage_number=11,
                exploration_label=target.exploration_label,
                attempt_name=f"tier_a_only_{split}",
                tier=mt5.TIER_A,
                split=split,
                model_path=f"{common}/models/tier_a_lgbm_58_model.onnx",
                model_id=f"{target.new_run_id}_tier_a_primary",
                feature_path=f"{common}/features/tier_a_{split}_feature_matrix.csv",
                feature_count=58,
                feature_order_hash=rule["tier_a_hash"],
                short_threshold=rule["short_threshold"],
                long_threshold=rule["long_threshold"],
                min_margin=rule["min_margin"],
                invert_signal=rule["invert_signal"],
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
                max_hold_bars=rule["max_hold_bars"],
                common_root=common,
            )
        )
        attempts.append(
            attempt_payload(
                run_root=run_root,
                run_id=target.new_run_id,
                stage_number=11,
                exploration_label=target.exploration_label,
                attempt_name=f"tier_b_fallback_only_{split}",
                tier=mt5.TIER_B,
                split=split,
                model_path=f"{common}/models/tier_b_lgbm_core42_model.onnx",
                model_id=f"{target.new_run_id}_tier_b_fallback",
                feature_path=f"{common}/features/tier_b_{split}_feature_matrix.csv",
                feature_count=42,
                feature_order_hash=rule["tier_b_hash"],
                short_threshold=rule["fallback_short_threshold"],
                long_threshold=rule["fallback_long_threshold"],
                min_margin=rule["fallback_min_margin"],
                invert_signal=rule["fallback_invert_signal"],
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
                max_hold_bars=rule["max_hold_bars"],
                common_root=common,
            )
        )
        attempts.append(
            attempt_payload(
                run_root=run_root,
                run_id=target.new_run_id,
                stage_number=11,
                exploration_label=target.exploration_label,
                attempt_name=f"routed_{split}",
                tier=mt5.TIER_AB,
                split=split,
                model_path=f"{common}/models/tier_a_lgbm_58_model.onnx",
                model_id=f"{target.new_run_id}_tier_a_primary",
                feature_path=f"{common}/features/tier_a_{split}_feature_matrix.csv",
                feature_count=58,
                feature_order_hash=rule["tier_a_hash"],
                short_threshold=rule["short_threshold"],
                long_threshold=rule["long_threshold"],
                min_margin=rule["min_margin"],
                invert_signal=rule["invert_signal"],
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                max_hold_bars=rule["max_hold_bars"],
                common_root=common,
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/tier_b_lgbm_core42_model.onnx",
                fallback_model_id=f"{target.new_run_id}_tier_b_fallback",
                fallback_feature_path=f"{common}/features/tier_b_{split}_feature_matrix.csv",
                fallback_feature_count=42,
                fallback_feature_order_hash=rule["tier_b_hash"],
                fallback_short_threshold=rule["fallback_short_threshold"],
                fallback_long_threshold=rule["fallback_long_threshold"],
                fallback_min_margin=rule["fallback_min_margin"],
                fallback_invert_signal=rule["fallback_invert_signal"],
            )
        )

    route_coverage = {
        "by_split": {
            "validation": matrix_route_counts(run_root, "validation_is"),
            "oos": matrix_route_counts(run_root, "oos"),
        },
        "tier_b_fallback_by_split_subtype": {},
        "no_tier_by_split": {"validation": None, "oos": None},
    }
    return {
        "stage_id": STAGE11_ID,
        "stage_number": 11,
        "run_id": target.new_run_id,
        "run_number": target.run_number,
        "source_run_id": target.source_run_id,
        "run_root": run_root,
        "attempts": attempts,
        "common_copies": copied,
        "route_coverage": route_coverage,
        "completion_goal": target.completion_goal,
        "model_family": "lightgbm_lgbmclassifier_multiclass",
        "feature_set_id": "feature_set_v2_mt5_price_proxy_top3_weights_58_features_and_core42_partial_context",
        "label_id": "label_v1_fwd18_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "stage_inheritance": "stage11_lgbm_source_surface_supplement",
    }


def matrix_route_counts(run_root: Path, split: str) -> dict[str, Any]:
    a_path = run_root / "mt5" / f"tier_a_{split}_feature_matrix.csv"
    b_path = run_root / "mt5" / f"tier_b_{split}_feature_matrix.csv"
    a_rows = csv_row_count(a_path)
    b_rows = csv_row_count(b_path)
    return {
        "tier_a_primary_rows": a_rows,
        "tier_b_fallback_rows": b_rows,
        "no_tier_labelable_rows": None,
        "routed_labelable_rows": None if a_rows is None or b_rows is None else a_rows + b_rows,
    }


def csv_row_count(path: Path) -> int | None:
    if not path_exists(path):
        return None
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _row in reader)


def train_et_model(frame: pd.DataFrame, feature_order: Sequence[str], params: Mapping[str, Any]) -> ExtraTreesClassifier:
    validate_model_input_frame(frame, list(feature_order))
    train = frame.loc[frame["split"].astype(str).eq("train")]
    x_train = train.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    y_train = train["label_class"].astype("int64").to_numpy()
    model = ExtraTreesClassifier(**{key: value for key, value in params.items() if key != "n_jobs"}, n_jobs=-1)
    return model.fit(x_train, y_train)


def probability_frame(model: Any, frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.DataFrame:
    probabilities = mt5.ordered_sklearn_probabilities(model, frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False))
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": frame["split"].astype(str).to_numpy(),
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
        }
    )


def nonflat_threshold(prob_frame: pd.DataFrame, quantile: float) -> float:
    validation = prob_frame.loc[prob_frame["split"].astype(str).eq("validation")]
    confidence = validation[["p_short", "p_long"]].max(axis=1)
    return float(np.quantile(confidence.to_numpy(dtype="float64"), quantile))


def decision_metrics(prob_frame: pd.DataFrame, threshold: float) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        frame = prob_frame.loc[prob_frame["split"].astype(str).eq(split)]
        p_short = frame["p_short"].to_numpy(dtype="float64")
        p_long = frame["p_long"].to_numpy(dtype="float64")
        labels = frame["label_class"].to_numpy(dtype="int64")
        decision = np.full(len(frame), 1, dtype="int64")
        short_ok = (p_short >= p_long) & (p_short >= threshold)
        long_ok = (p_long > p_short) & (p_long >= threshold)
        decision[short_ok] = 0
        decision[long_ok] = 2
        signals = decision != 1
        metrics[split] = {
            "rows": int(len(frame)),
            "signal_count": int(signals.sum()),
            "short_count": int((decision == 0).sum()),
            "long_count": int((decision == 2).sum()),
            "signal_coverage": float(signals.mean()) if len(frame) else None,
            "directional_correct_count": int((decision[signals] == labels[signals]).sum()) if signals.any() else 0,
            "directional_hit_rate": float((decision[signals] == labels[signals]).mean()) if signals.any() else None,
        }
    return metrics


def prepare_run03_target(common_root: Path) -> dict[str, Any]:
    run_id = "run03F_et_v11_tier_balance_mt5_v1"
    run_root = STAGE12_RUNS / run_id
    io_path(run_root / "models").mkdir(parents=True, exist_ok=True)
    io_path(run_root / "mt5").mkdir(parents=True, exist_ok=True)
    io_path(run_root / "predictions").mkdir(parents=True, exist_ok=True)

    variants = pd.read_csv(io_path(RUN03D_VARIANT_RESULTS))
    source = variants.loc[variants["variant_id"].astype(str).eq("v11_base_leaf20_q85")]
    if source.empty:
        raise RuntimeError("missing run03D source variant v11_base_leaf20_q85")
    source_row = source.iloc[0].to_dict()
    params = json.loads(str(source_row["model_params_json"]))
    threshold_quantile = float(source_row["threshold_quantile"])

    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    tier_a_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    tier_a_hash = mt5.ordered_hash(tier_a_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    label_threshold = float(training_summary["threshold_log_return"])
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
    )
    tier_b_training = tier_b_context["tier_b_training_frame"]
    tier_b_fallback = tier_b_context["tier_b_fallback_frame"]
    no_tier = tier_b_context["no_tier_frame"]
    tier_b_hash = mt5.ordered_hash(tier_b_feature_order)

    tier_a_model = train_et_model(tier_a_frame, tier_a_feature_order, params)
    tier_b_model = train_et_model(tier_b_training, tier_b_feature_order, params)
    tier_a_prob = probability_frame(tier_a_model, tier_a_frame, tier_a_feature_order)
    tier_b_prob = probability_frame(tier_b_model, tier_b_fallback, tier_b_feature_order)
    threshold_a = float(source_row["threshold"])
    threshold_b = nonflat_threshold(tier_b_prob, threshold_quantile)
    tier_a_metrics = decision_metrics(tier_a_prob, threshold_a)
    tier_b_metrics = decision_metrics(tier_b_prob, threshold_b)

    copied = []
    tier_a_joblib = run_root / "models/tier_a_extratrees_58_model.joblib"
    tier_b_joblib = run_root / "models/tier_b_extratrees_core42_model.joblib"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_onnx = run_root / "models/tier_a_extratrees_58_model.onnx"
    tier_b_onnx = run_root / "models/tier_b_extratrees_core42_model.onnx"
    mt5.export_sklearn_to_onnx_zipmap_disabled(tier_a_model, tier_a_onnx, feature_count=len(tier_a_feature_order))
    mt5.export_sklearn_to_onnx_zipmap_disabled(tier_b_model, tier_b_onnx, feature_count=len(tier_b_feature_order))
    io_path(run_root / "models/tier_a_58_feature_order.txt").write_text("\n".join(tier_a_feature_order) + "\n", encoding="utf-8")
    io_path(run_root / "models/tier_b_core42_feature_order.txt").write_text("\n".join(tier_b_feature_order) + "\n", encoding="utf-8")

    sample_a = tier_a_frame.loc[:, tier_a_feature_order].to_numpy(dtype="float64", copy=False)[:128]
    sample_b = tier_b_fallback.loc[:, tier_b_feature_order].to_numpy(dtype="float64", copy=False)[:128]
    onnx_parity = {
        "tier_a": mt5.check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, sample_a),
        "tier_b": mt5.check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, sample_b),
    }
    onnx_parity["passed"] = bool(onnx_parity["tier_a"]["passed"] and onnx_parity["tier_b"]["passed"])
    if not onnx_parity["passed"]:
        raise RuntimeError("run03F ONNX parity failed")

    common = common_run_root(12, run_id)
    for model_path in (tier_a_onnx, tier_b_onnx):
        copied.append(copy_to_common(model_path, f"{common}/models/{model_path.name}", common_root))

    attempts: list[dict[str, Any]] = []
    feature_matrices: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        source_split = "validation" if split == "validation_is" else "oos"
        a_split = tier_a_frame.loc[tier_a_frame["split"].astype(str).eq(source_split)].copy().reset_index(drop=True)
        b_split = tier_b_fallback.loc[tier_b_fallback["split"].astype(str).eq(source_split)].copy().reset_index(drop=True)
        from_date, to_date = split_dates_from_frame(a_split, source_split)
        a_matrix = run_root / "mt5" / f"tier_a_{split}_feature_matrix.csv"
        b_matrix = run_root / "mt5" / f"tier_b_{split}_feature_matrix.csv"
        feature_matrices.append(mt5.export_mt5_feature_matrix_csv(a_split, tier_a_feature_order, a_matrix))
        feature_matrices.append(
            mt5.export_mt5_feature_matrix_csv(
                b_split,
                tier_b_feature_order,
                b_matrix,
                metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
            )
        )
        copied.append(copy_to_common(a_matrix, f"{common}/features/{a_matrix.name}", common_root))
        copied.append(copy_to_common(b_matrix, f"{common}/features/{b_matrix.name}", common_root))
        attempts.append(
            attempt_payload(
                run_root=run_root,
                run_id=run_id,
                stage_number=12,
                exploration_label="stage12_Model__ExtraTreesV11TierBalance",
                attempt_name=f"tier_a_only_{split}",
                tier=mt5.TIER_A,
                split=split,
                model_path=f"{common}/models/{tier_a_onnx.name}",
                model_id=f"{run_id}_tier_a_v11",
                feature_path=f"{common}/features/{a_matrix.name}",
                feature_count=len(tier_a_feature_order),
                feature_order_hash=tier_a_hash,
                short_threshold=threshold_a,
                long_threshold=threshold_a,
                min_margin=0.0,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
                max_hold_bars=9,
                common_root=common,
            )
        )
        attempts.append(
            attempt_payload(
                run_root=run_root,
                run_id=run_id,
                stage_number=12,
                exploration_label="stage12_Model__ExtraTreesV11TierBalance",
                attempt_name=f"tier_b_fallback_only_{split}",
                tier=mt5.TIER_B,
                split=split,
                model_path=f"{common}/models/{tier_b_onnx.name}",
                model_id=f"{run_id}_tier_b_v11",
                feature_path=f"{common}/features/{b_matrix.name}",
                feature_count=len(tier_b_feature_order),
                feature_order_hash=tier_b_hash,
                short_threshold=threshold_b,
                long_threshold=threshold_b,
                min_margin=0.0,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
                max_hold_bars=9,
                common_root=common,
            )
        )
        attempts.append(
            attempt_payload(
                run_root=run_root,
                run_id=run_id,
                stage_number=12,
                exploration_label="stage12_Model__ExtraTreesV11TierBalance",
                attempt_name=f"routed_{split}",
                tier=mt5.TIER_AB,
                split=split,
                model_path=f"{common}/models/{tier_a_onnx.name}",
                model_id=f"{run_id}_tier_a_v11",
                feature_path=f"{common}/features/{a_matrix.name}",
                feature_count=len(tier_a_feature_order),
                feature_order_hash=tier_a_hash,
                short_threshold=threshold_a,
                long_threshold=threshold_a,
                min_margin=0.0,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                max_hold_bars=9,
                common_root=common,
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_onnx.name}",
                fallback_model_id=f"{run_id}_tier_b_v11",
                fallback_feature_path=f"{common}/features/{b_matrix.name}",
                fallback_feature_count=len(tier_b_feature_order),
                fallback_feature_order_hash=tier_b_hash,
                fallback_short_threshold=threshold_b,
                fallback_long_threshold=threshold_b,
                fallback_min_margin=0.0,
                fallback_invert_signal=False,
            )
        )

    route_coverage = dict(tier_b_context["summary"])
    write_json(run_root / "summary.json", {
        "run_id": run_id,
        "stage_id": STAGE12_ID,
        "source_run_id": "run03D_et_standalone_batch20_v1",
        "source_variant_id": "v11_base_leaf20_q85",
        "model_family": "sklearn_extratreesclassifier_multiclass",
        "tier_a_signal_metrics": tier_a_metrics,
        "tier_b_signal_metrics": tier_b_metrics,
        "thresholds": {"tier_a": threshold_a, "tier_b": threshold_b, "quantile": threshold_quantile},
        "onnx_parity": onnx_parity,
        "route_coverage": route_coverage,
    })
    tier_a_prob.to_parquet(io_path(run_root / "predictions/tier_a_probabilities.parquet"), index=False)
    tier_b_prob.to_parquet(io_path(run_root / "predictions/tier_b_probabilities.parquet"), index=False)
    return {
        "stage_id": STAGE12_ID,
        "stage_number": 12,
        "run_id": run_id,
        "run_number": "run03F",
        "source_run_id": "run03D_et_standalone_batch20_v1",
        "run_root": run_root,
        "attempts": attempts,
        "common_copies": copied,
        "feature_matrices": feature_matrices,
        "route_coverage": route_coverage,
        "completion_goal": "add_tier_a_tier_b_and_actual_routed_total_for_stage12_v11",
        "model_family": "sklearn_extratreesclassifier_multiclass",
        "feature_set_id": "feature_set_v2_mt5_price_proxy_top3_weights_58_features_and_core42_partial_context",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "stage_inheritance": "stage12_standalone_no_stage10_11_threshold_or_model_inheritance",
        "python_metrics": {"tier_a": tier_a_metrics, "tier_b": tier_b_metrics},
        "onnx_parity": onnx_parity,
    }


def clear_runtime_outputs(common_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def execute_prepared_run(
    prepared: Mapping[str, Any],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    run_root = Path(prepared["run_root"])
    attempts = list(prepared["attempts"])
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, run_root / "mt5/mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
            result = mt5.run_mt5_tester(
                terminal_path,
                Path(attempt["ini"]["path"]),
                set_path=Path(attempt["set"]["path"]),
                tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=tester_profile_root / f"opv2_{safe_name(str(prepared['run_id']), 48)}_{attempt['attempt_name']}.ini",
                timeout_seconds=timeout_seconds,
            )
            result["tier"] = attempt["tier"]
            result["split"] = attempt["split"]
            result["attempt_name"] = attempt["attempt_name"]
            result["attempt_role"] = attempt.get("attempt_role")
            result["record_view_prefix"] = attempt.get("record_view_prefix")
            if "routing_mode" in attempt:
                result["routing_mode"] = attempt["routing_mode"]
            result["ini_path"] = attempt["ini"]["path"]
            result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
            if result["runtime_outputs"].get("status") != "completed":
                result["status"] = "blocked"
            execution_results.append(result)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=run_root,
        attempts=attempts,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, prepared["route_coverage"])
    completed = bool(execution_results) and all(item.get("status") == "completed" for item in execution_results)
    report_completed = bool(kpi_records) and all(item.get("status") == "completed" for item in kpi_records)
    return {
        **dict(prepared),
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "external_verification_status": "completed" if completed and report_completed else "blocked",
        "judgment": "inconclusive_tier_balance_runtime_probe_completed" if completed and report_completed else "blocked_tier_balance_runtime_probe",
    }


def write_run_files(result: Mapping[str, Any]) -> None:
    run_root = Path(result["run_root"])
    kpi_payload = {
        "run_id": result["run_id"],
        "stage_id": result["stage_id"],
        "source_run_id": result["source_run_id"],
        "kpi_scope": "tier_balance_mt5_runtime_probe",
        "model_family": result["model_family"],
        "feature_set_id": result["feature_set_id"],
        "label_id": result["label_id"],
        "split_contract": result["split_contract"],
        "stage_inheritance": result["stage_inheritance"],
        "python_metrics": result.get("python_metrics", {}),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result["external_verification_status"],
            "execution_results": result["execution_results"],
            "strategy_tester_reports": result["strategy_tester_reports"],
            "kpi_records": result["mt5_kpi_records"],
        },
        "external_verification_status": result["external_verification_status"],
        "judgment": result["judgment"],
        "boundary": "runtime_probe_only_not_alpha_quality_not_live_readiness_not_operating_promotion",
    }
    manifest = {
        "run_id": result["run_id"],
        "stage_id": result["stage_id"],
        "source_run_id": result["source_run_id"],
        "run_number": result["run_number"],
        "completion_goal": result["completion_goal"],
        "attempts": result["attempts"],
        "common_copies": result.get("common_copies", []),
        "compile": result["compile"],
        "external_verification_status": result["external_verification_status"],
        "judgment": result["judgment"],
    }
    write_json(run_root / "run_manifest.json", manifest)
    write_json(run_root / "kpi_record.json", kpi_payload)
    write_result_summary(run_root / "reports/result_summary.md", result)


def write_result_summary(path: Path, result: Mapping[str, Any]) -> None:
    lines = [
        f"# {result['run_id']} Tier Balance Completion",
        "",
        f"- source_run_id: `{result['source_run_id']}`",
        f"- external_verification_status: `{result['external_verification_status']}`",
        f"- judgment: `{result['judgment']}`",
        "",
        "| view | split | net_profit | profit_factor | trades |",
        "|---|---:|---:|---:|---:|",
    ]
    for record in result["mt5_kpi_records"]:
        metrics = record.get("metrics", {})
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        lines.append(
            "| {view} | {split} | {net} | {pf} | {trades} |".format(
                view=record.get("record_view"),
                split=record.get("split"),
                net=metrics.get("net_profit"),
                pf=metrics.get("profit_factor"),
                trades=metrics.get("trade_count"),
            )
        )
    lines.extend(
        [
            "",
            "Boundary: runtime_probe only. No alpha quality, live readiness, operating promotion, or runtime authority expansion is claimed.",
            "",
        ]
    )
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines), encoding="utf-8-sig")


def attempt_summary_rows(results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        reports_by_name = {record.get("report_name"): record for record in result["strategy_tester_reports"]}
        for execution in result["execution_results"]:
            report_name = mt5.report_name_from_attempt(next(a for a in result["attempts"] if a["attempt_name"] == execution["attempt_name"]))
            report = reports_by_name.get(report_name, {})
            metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
            rows.append(
                {
                    "run_id": result["run_id"],
                    "stage_id": result["stage_id"],
                    "source_run_id": result["source_run_id"],
                    "attempt_name": execution.get("attempt_name"),
                    "split": "validation" if execution.get("split") == "validation_is" else execution.get("split"),
                    "tier_scope": execution.get("tier"),
                    "route_role": execution.get("attempt_role") or ("routed_total" if execution.get("routing_mode") else "tier_only_total"),
                    "tester_status": execution.get("status"),
                    "runtime_status": execution.get("runtime_outputs", {}).get("status"),
                    "report_status": report.get("status") if isinstance(report, Mapping) else None,
                    "net_profit": metrics.get("net_profit") if isinstance(metrics, Mapping) else None,
                    "profit_factor": metrics.get("profit_factor") if isinstance(metrics, Mapping) else None,
                    "trade_count": metrics.get("trade_count") if isinstance(metrics, Mapping) else None,
                    "report_path": report.get("html_report", {}).get("path") if isinstance(report.get("html_report"), Mapping) else "",
                }
            )
    return rows


def write_ledgers(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_rows = []
    ledger_rows_by_stage: dict[str, list[dict[str, Any]]] = {}
    project_rows = []
    for result in results:
        run_rows.append(
            {
                "run_id": result["run_id"],
                "stage_id": result["stage_id"],
                "lane": "tier_balance_mt5_runtime_probe",
                "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
                "judgment": result["judgment"],
                "path": rel(Path(result["run_root"])),
                "notes": f"source_run_id={result['source_run_id']};views=tier_a_only,tier_b_fallback_only,routed_total;boundary=runtime_probe_only",
            }
        )
        for record in result["mt5_kpi_records"]:
            metrics = record.get("metrics", {})
            view = str(record.get("record_view"))
            row = {
                "ledger_row_id": f"{result['run_id']}__{view}",
                "stage_id": result["stage_id"],
                "run_id": result["run_id"],
                "subrun_id": view,
                "parent_run_id": result["source_run_id"],
                "record_view": view,
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "tier_balance_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status"),
                "judgment": result["judgment"],
                "path": record.get("report", {}).get("html_report", {}).get("path", ""),
                "primary_kpi": ledger_pairs(
                    [
                        ("net_profit", metrics.get("net_profit")),
                        ("profit_factor", metrics.get("profit_factor")),
                        ("trade_count", metrics.get("trade_count")),
                        ("signal_count", metrics.get("signal_count")),
                    ]
                ),
                "guardrail_kpi": ledger_pairs(
                    [
                        ("source_run_id", result["source_run_id"]),
                        ("route_role", record.get("route_role")),
                        ("boundary", "runtime_probe_only"),
                    ]
                ),
                "external_verification_status": result["external_verification_status"],
                "notes": "Supplemental tier-balance record; does not alter prior source-run judgment.",
            }
            project_rows.append(row)
            ledger_rows_by_stage.setdefault(str(result["stage_id"]), []).append(row)
    outputs = {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, project_rows, key="ledger_row_id"),
    }
    for stage_id, rows in ledger_rows_by_stage.items():
        path = RUNS_ROOT / stage_id / "03_reviews/stage_run_ledger.csv"
        outputs[f"{stage_id}_stage_ledger"] = upsert_csv_rows(path, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    return outputs


def normalized_packet_rows(results: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows = [
        {
            "run_id": result["run_id"],
            "stage_id": result["stage_id"],
            "path": rel(Path(result["run_root"])),
        }
        for result in results
    ]
    return mt5_kpi_recorder.build_normalized_records(ROOT, rows)


def write_packet(
    packet_dir: Path,
    *,
    packet_id: str,
    created_at_utc: str,
    results: Sequence[Mapping[str, Any]],
    normalized_records: Sequence[Mapping[str, Any]],
    normalized_summary_rows: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
    trade_enriched: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    trade_summary_rows: Sequence[Mapping[str, Any]],
    trade_parser_errors: Sequence[Mapping[str, Any]],
    ledger_outputs: Mapping[str, Any],
) -> dict[str, Any]:
    io_path(packet_dir / "skill_receipts").mkdir(parents=True, exist_ok=True)
    summary = {
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "target_runs_total": len(results),
        "mt5_attempts_total": sum(len(result["attempts"]) for result in results),
        "mt5_execution_results": sum(len(result["execution_results"]) for result in results),
        "mt5_kpi_records": sum(len(result["mt5_kpi_records"]) for result in results),
        "normalized_records": len(normalized_records),
        "trade_attribution_records": len(trade_summary_rows),
        "trade_level_rows": len(trade_rows),
        "parser_errors": len(parser_errors),
        "trade_parser_errors": len(trade_parser_errors),
        "completed_runs": sum(1 for result in results if result["external_verification_status"] == "completed"),
        "blocked_runs": [result["run_id"] for result in results if result["external_verification_status"] != "completed"],
        "status": "completed" if all(result["external_verification_status"] == "completed" for result in results) else "partial",
        "completed_forbidden": not all(result["external_verification_status"] == "completed" for result in results),
    }
    target_rows = [
        {
            "new_run_id": result["run_id"],
            "source_run_id": result["source_run_id"],
            "stage_id": result["stage_id"],
            "stage_number": result["stage_number"],
            "completion_goal": result["completion_goal"],
            "required_views": "tier_a_only;tier_b_fallback_only;routed_total",
            "status": result["external_verification_status"],
            "reason": result["judgment"],
        }
        for result in results
    ]
    write_csv_rows(packet_dir / "target_matrix.csv", TARGET_COLUMNS, target_rows)
    write_csv_rows(packet_dir / "attempt_summary.csv", SUMMARY_COLUMNS, attempt_summary_rows(results))
    write_json(packet_dir / "execution_results.json", [
        {
            "run_id": result["run_id"],
            "stage_id": result["stage_id"],
            "source_run_id": result["source_run_id"],
            "compile": result["compile"],
            "execution_results": result["execution_results"],
            "strategy_tester_reports": result["strategy_tester_reports"],
        }
        for result in results
    ])
    write_jsonl(packet_dir / "normalized_kpi_records.jsonl", normalized_records)
    write_csv_rows(packet_dir / "normalized_kpi_summary.csv", mt5_kpi_recorder.SUMMARY_COLUMNS, normalized_summary_rows)
    write_jsonl(packet_dir / "enriched_kpi_records.jsonl", trade_enriched)
    write_csv_rows(packet_dir / "trade_level_records.csv", mt5_trade_attribution.TRADE_COLUMNS, trade_rows)
    write_csv_rows(packet_dir / "trade_attribution_summary.csv", mt5_trade_attribution.SUMMARY_COLUMNS, trade_summary_rows)
    write_json(packet_dir / "parser_errors.json", list(parser_errors))
    write_json(packet_dir / "trade_parser_errors.json", list(trade_parser_errors))
    write_json(packet_dir / "ledger_outputs.json", ledger_outputs)
    write_json(packet_dir / "packet_summary.json", summary)
    write_json(
        packet_dir / "work_packet.json",
        {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "user_quote": "run 02 03 missing KPI must be filled through MT5 tier-balance reinforcement",
            "interpreted_scope": {
                "run02_sources": [target.source_run_id for target in RUN02_TARGETS],
                "run03_supplement": "run03F_et_v11_tier_balance_mt5_v1",
                "required_views": ["tier_a_only", "tier_b_fallback_only", "routed_total"],
                "no_prior_raw_report_overwrite": True,
            },
            "acceptance_criteria": [
                "Create supplemental run folders instead of overwriting prior source runs.",
                "Run MT5 for Tier A only, Tier B fallback only, and actual routed total on validation and OOS.",
                "Write normalized 7-layer KPI records and trade attribution records.",
                "Update run registry and alpha ledgers with runtime_probe-only boundary.",
            ],
        },
    )
    receipts = {
        "experiment_design": {
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "Missing tier views can reveal whether Tier B fallback changes run02/run03 model-development reads.",
            "decision_use": "diagnostic tier-balance comparison only",
            "success_criteria": "all target views have MT5 reports and KPI rows",
            "invalid_conditions": "missing model, feature matrix, ONNX parity failure, tester output missing",
        },
        "runtime_parity": {
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "research_path": "existing run02 source artifacts plus run03F trained Tier A/B ExtraTrees",
            "runtime_path": "ObsidianPrimeV2_RuntimeProbeEA with supplemental .set/.ini attempts",
            "runtime_claim_boundary": "runtime_probe",
        },
        "backtest_forensics": {
            "skill": "obsidian-backtest-forensics",
            "status": "executed",
            "trade_evidence": f"{summary['mt5_kpi_records']} MT5 KPI records",
            "backtest_judgment": "usable_with_boundary" if summary["status"] == "completed" else "blocked",
        },
        "run_evidence_system": {
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "measurement_scope": "run_identity, signal_model, mt5_headline, risk, trade_diagnostics, regime_slice, execution",
            "evidence_boundary": "runtime_probe",
            "registry_update_required": "yes",
        },
        "artifact_lineage": {
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "producer": "foundation.control_plane.mt5_tier_balance_completion",
            "availability": "tracked_or_generated_with_manifest",
        },
        "performance_attribution": {
            "skill": "obsidian-performance-attribution",
            "status": "executed",
            "segment_checks": "trade_attribution_summary.csv and trade_level_records.csv",
            "attribution_confidence": "diagnostic_not_promotion",
        },
    }
    for name, receipt in receipts.items():
        receipt_path = packet_dir / "skill_receipts" / f"{name}.json"
        write_json(
            receipt_path,
            {
                "packet_id": packet_id,
                "created_at_utc": created_at_utc,
                "triggered": True,
                "receipt_path": receipt_path.as_posix(),
                "blocking": False,
                **receipt,
            },
        )
    write_json(
        packet_dir / "skill_receipts.json",
        {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "receipts": [
                {
                    "skill": receipt["skill"],
                    "triggered": True,
                    "status": receipt["status"],
                    "receipt_path": (packet_dir / "skill_receipts" / f"{name}.json").as_posix(),
                    "blocking": False,
                }
                for name, receipt in receipts.items()
            ],
        },
    )
    return summary


def run_completion(
    *,
    packet_id: str,
    output_dir: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    timeout_seconds: int,
    materialize_only: bool,
    created_at_utc: str | None,
) -> dict[str, Any]:
    created_at = created_at_utc or utc_now()
    common_root = COMMON_FILES_ROOT_DEFAULT
    prepared = [prepare_run02_target(target, common_root) for target in RUN02_TARGETS]
    prepared.append(prepare_run03_target(common_root))
    if materialize_only:
        results = [
            {
                **item,
                "compile": {"status": "not_attempted"},
                "execution_results": [],
                "strategy_tester_reports": [],
                "mt5_kpi_records": [],
                "external_verification_status": "blocked",
                "judgment": "blocked_materialize_only_no_mt5_execution",
            }
            for item in prepared
        ]
    else:
        results = [
            execute_prepared_run(
                item,
                terminal_path=terminal_path,
                metaeditor_path=metaeditor_path,
                terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
                common_files_root=common_root,
                tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
                timeout_seconds=timeout_seconds,
            )
            for item in prepared
        ]
    for result in results:
        write_run_files(result)
    ledger_outputs = write_ledgers(results)
    records, summary_rows, missing_runs, parser_errors = normalized_packet_rows(results)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary_rows, trade_parser_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    packet_dir = output_dir if output_dir.is_absolute() else ROOT / output_dir
    packet_summary = write_packet(
        packet_dir,
        packet_id=packet_id,
        created_at_utc=created_at,
        results=results,
        normalized_records=records,
        normalized_summary_rows=summary_rows,
        parser_errors=[*parser_errors, *missing_runs],
        trade_enriched=enriched,
        trade_rows=trade_rows,
        trade_summary_rows=trade_summary_rows,
        trade_parser_errors=trade_parser_errors,
        ledger_outputs=ledger_outputs,
    )
    return packet_summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Complete run02/run03 tier-balance MT5 KPI supplement.")
    parser.add_argument("--packet-id", default=PACKET_ID_DEFAULT)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--created-at-utc", default=None)
    args = parser.parse_args(argv)
    output_dir = Path(args.output_dir) if args.output_dir else Path("docs/agent_control/packets") / args.packet_id
    summary = run_completion(
        packet_id=args.packet_id,
        output_dir=output_dir,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        timeout_seconds=args.timeout_seconds,
        materialize_only=bool(args.materialize_only),
        created_at_utc=args.created_at_utc,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
