from __future__ import annotations

import csv
import json
import math
import re
import shutil
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_NUMBER = "run267N"
RUN_ID = "run267N_stage267_pool_wide_ablation_replacement_materialization_v1"
STATUS = "run267N_pool_wide_ablation_replacement_materialized_execution_pending"
NEXT_ACTION = "run267N_execute_pool_wide_ablation_replacement_p0_mt5_batch"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
MATERIALIZATION_ROOT = RUN_ROOT / "p0_ablation_replacement_materialization"

RUN267M_ROOT = STAGE_ROOT / "02_runs" / "run267M" / "pool_wide_ablation_replacement_design"
INPUT_QUEUE_PATH = RUN267M_ROOT / "p0_materialization_queue.csv"
INPUT_MATRIX_PATH = RUN267M_ROOT / "ablation_replacement_matrix.csv"
BASE_FEATURE_MANIFEST_PATH = input_probe.FEATURE_MANIFEST_PATH

VARIANT_MANIFEST_PATH = MATERIALIZATION_ROOT / "p0_materialized_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = MATERIALIZATION_ROOT / "runtime_contract.csv"
FEATURE_DIAGNOSTICS_PATH = MATERIALIZATION_ROOT / "feature_diagnostics.csv"
ATTEMPT_MANIFEST_PATH = MATERIALIZATION_ROOT / "attempts.csv"
RUN_MANIFEST_PATH = MATERIALIZATION_ROOT / "run_manifest.json"
LINEAGE_PATH = MATERIALIZATION_ROOT / "lineage.json"
RESULT_PATH = MATERIALIZATION_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267N_pool_wide_ablation_replacement_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267N_pool_wide_ablation_replacement_materialization.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267n/run267N_p0_ablation_replacement"
PERIOD_LABEL = input_probe.PERIOD_LABEL
SOURCE_SIGNAL_COLUMN = input_probe.SOURCE_SIGNAL_COLUMN
MODEL_COLUMNS = ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long")
PROXY_SCORE_CUTS = (0.25, 0.50, 0.75)
PROXY_SCORE_TERMS = (
    (0.0, 0.0, 0.0),
    (-0.035, 0.070, -0.035),
    (-0.060, 0.120, -0.060),
    (-0.085, 0.170, -0.085),
    (-0.110, 0.220, -0.110),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def safe_token(value: str, limit: int = 80) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return token[:limit] or "item"


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_runtime_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    upsert_csv_rows(path, columns, [row], key=key)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
        lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_tail_from_marker(text: str, marker: str, replacement: str) -> str:
    start = text.find(marker)
    if start == -1:
        return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"
    return text[:start].rstrip() + "\n\n" + replacement.rstrip() + "\n"


def base_features_by_alias() -> dict[str, dict[str, str]]:
    rows = read_csv(BASE_FEATURE_MANIFEST_PATH)
    if not rows:
        raise RuntimeError(f"missing base feature manifest: {BASE_FEATURE_MANIFEST_PATH}")
    return {row["candidate_alias"]: row for row in rows}


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def p0_queue_rows() -> list[dict[str, str]]:
    rows = read_csv(INPUT_QUEUE_PATH)
    if not rows:
        raise RuntimeError(f"missing run267M P0 queue: {INPUT_QUEUE_PATH}")
    return sorted(rows, key=lambda row: row["queue_id"])


def source_context() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    frame, source_info = input_probe.build_2024_source_frame()
    frame = frame.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    numeric_columns = [
        "adx_14",
        "di_spread_14",
        "vortex_indicator",
        "supertrend_10_3",
        "atr_14",
        "atr_50",
        "atr_14_over_atr_50",
        "historical_vol_20",
        "historical_vol_5_over_20",
        "bollinger_width_20",
        "minutes_from_cash_open",
        "log_return_1",
        "log_return_3",
        "hl_range",
        "return_zscore_20",
        "return_1_over_atr_14",
        "close_ema20_ratio",
        "ema20_ema50_diff",
    ]
    stats: dict[str, dict[str, float]] = {}
    for column in numeric_columns:
        if column not in frame.columns:
            continue
        values = pd.to_numeric(frame[column], errors="coerce").dropna()
        abs_values = values.abs()
        stats[column] = {
            "q05": float(values.quantile(0.05)) if len(values) else 0.0,
            "q50": float(values.quantile(0.50)) if len(values) else 0.0,
            "q95": float(values.quantile(0.95)) if len(values) else 1.0,
            "abs_q95": float(abs_values.quantile(0.95)) if len(abs_values) else 1.0,
        }
    context: dict[str, dict[str, Any]] = {}
    for record in frame.to_dict("records"):
        timestamp = pd.Timestamp(record["timestamp"])
        key = timestamp.strftime("%Y.%m.%d %H:%M:%S")
        context[key] = dict(record)
    return context, {
        **source_info,
        "stats": stats,
        "context_columns": len(frame.columns),
    }


def norm_between(value: Any, low: float, high: float, default: float = 0.0) -> float:
    number = finite_float(value)
    if number is None:
        return default
    width = max(float(high) - float(low), 1.0e-9)
    return max(0.0, min(1.0, (number - float(low)) / width))


def abs_norm(value: Any, scale: float, default: float = 0.0) -> float:
    number = finite_float(value)
    if number is None:
        return default
    return max(0.0, min(1.0, abs(number) / max(float(scale), 1.0e-9)))


def low_score(value: Any, stats: Mapping[str, float]) -> float:
    return 1.0 - norm_between(value, float(stats.get("q05", 0.0)), float(stats.get("q95", 1.0)))


def high_score(value: Any, stats: Mapping[str, float]) -> float:
    return norm_between(value, float(stats.get("q05", 0.0)), float(stats.get("q95", 1.0)))


def soft_band(value: Any, center: float, half_width: float) -> float:
    number = finite_float(value)
    if number is None:
        return 0.0
    return max(0.0, min(1.0, 1.0 - abs(number - center) / max(half_width, 1.0e-9)))


def session_late_score(minutes: Any) -> float:
    number = finite_float(minutes)
    if number is None:
        return 0.0
    return 1.0 if 220.0 < number <= 330.0 else 0.0


def proxy_score_for(test_id: str, context_row: Mapping[str, Any], stats: Mapping[str, Mapping[str, float]]) -> float:
    if test_id in {"abl_volatility_bandwidth", "rep_volatility_atr"}:
        values = [
            low_score(context_row.get("atr_14_over_atr_50"), stats.get("atr_14_over_atr_50", {})),
            low_score(context_row.get("historical_vol_20"), stats.get("historical_vol_20", {})),
            low_score(context_row.get("bollinger_width_20"), stats.get("bollinger_width_20", {})),
        ]
        return sum(values) / len(values)
    if test_id in {"abl_trend_strength_direction", "rep_trend_strength_adx"}:
        adx_band = soft_band(context_row.get("adx_14"), 22.5, 7.5)
        di_component = 1.0 - abs_norm(context_row.get("di_spread_14"), stats.get("di_spread_14", {}).get("abs_q95", 1.0))
        vortex_component = 1.0 - abs_norm(context_row.get("vortex_indicator"), stats.get("vortex_indicator", {}).get("abs_q95", 1.0))
        return max(0.0, min(1.0, 0.50 * adx_band + 0.25 * di_component + 0.25 * vortex_component))
    if test_id == "abl_session_timing":
        return session_late_score(context_row.get("minutes_from_cash_open"))
    if test_id == "abl_ma_trend":
        return abs_norm(context_row.get("ema20_ema50_diff"), stats.get("ema20_ema50_diff", {}).get("abs_q95", 1.0))
    if test_id == "abl_price_return_range":
        values = [
            abs_norm(context_row.get("log_return_1"), stats.get("log_return_1", {}).get("abs_q95", 1.0)),
            abs_norm(context_row.get("hl_range"), stats.get("hl_range", {}).get("abs_q95", 1.0)),
            abs_norm(context_row.get("return_zscore_20"), stats.get("return_zscore_20", {}).get("abs_q95", 1.0)),
        ]
        return sum(values) / len(values)
    return 0.0


def direct_transform_type(test_id: str) -> str:
    if test_id == "abl_gate_rank_bucket":
        return "direct_rank_bucket_neutralization(직접 순위 구간 중립화)"
    if test_id == "abl_gate_variant_rule":
        return "direct_gate_filter_disable(직접 게이트 필터 비활성화)"
    return "context_proxy_score_extension(문맥 대체 점수 확장)"


def materialization_boundary(test_id: str) -> str:
    if test_id in {"abl_gate_rank_bucket", "abl_gate_variant_rule"}:
        return "direct_runtime_surface_ablation(직접 런타임 표면 제거)"
    return "proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)"


def feature_name_for(test_id: str) -> str:
    return f"stage267n_{safe_token(test_id, 48)}_score"


def model_type_for(test_id: str) -> str:
    if test_id == "abl_gate_rank_bucket":
        return "direct_feature_value_neutralization_model_unchanged_v1"
    if test_id == "abl_gate_variant_rule":
        return "direct_set_parameter_gate_ablation_model_unchanged_v1"
    return "context_proxy_score_table_extension_v1"


def copy_model(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {
        "source_model_file": rel(source),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
    }


def extend_model(source: Path, destination: Path, feature_index: int, test_id: str) -> dict[str, Any]:
    if test_id in {"abl_gate_rank_bucket", "abl_gate_variant_rule"}:
        return copy_model(source, destination)
    rows = read_csv(source)
    if not rows:
        raise RuntimeError(f"empty model file: {source}")
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    with io_path(destination).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MODEL_COLUMNS), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in MODEL_COLUMNS})
        for index, cut in enumerate(PROXY_SCORE_CUTS):
            writer.writerow(
                {
                    "record_type": "cut",
                    "feature_index": feature_index,
                    "item_index": index,
                    "value": f"{cut:.17g}",
                    "score_short": "",
                    "score_flat": "",
                    "score_long": "",
                }
            )
        for index, (score_short, score_flat, score_long) in enumerate(PROXY_SCORE_TERMS):
            writer.writerow(
                {
                    "record_type": "score",
                    "feature_index": feature_index,
                    "item_index": index,
                    "value": "",
                    "score_short": f"{score_short:.17g}",
                    "score_flat": f"{score_flat:.17g}",
                    "score_long": f"{score_long:.17g}",
                }
            )
    return {
        "source_model_file": rel(source),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
    }


def rank_column(columns: Sequence[str]) -> str | None:
    for column in columns:
        if column.endswith("_source_feature_rank_bucket"):
            return column
    return None


def gate_column(columns: Sequence[str]) -> str | None:
    for column in columns:
        if "_source_feature_gate_" in column:
            return column
    return None


def transform_feature_file(
    source: Path,
    destination: Path,
    queue_row: Mapping[str, str],
    context: Mapping[str, Mapping[str, Any]],
    stats: Mapping[str, Mapping[str, float]],
) -> tuple[dict[str, Any], list[str]]:
    rows = read_csv(source)
    if not rows:
        raise RuntimeError(f"empty source feature file: {source}")
    base_columns = list(rows[0].keys())
    test_id = queue_row["test_id"]
    transform_type = direct_transform_type(test_id)
    added_feature = "" if test_id in {"abl_gate_rank_bucket", "abl_gate_variant_rule"} else feature_name_for(test_id)
    columns = list(base_columns) if not added_feature else [*base_columns, added_feature]
    rank_col = rank_column(base_columns)
    gate_col = gate_column(base_columns)

    transformed: list[dict[str, Any]] = []
    scores: list[float] = []
    signal_scores: list[float] = []
    total_signal_rows = 0
    context_missing_rows = 0
    changed_rows = 0
    rank_neutralized_rows = 0
    gate_feature_present_rows = 0
    for row in rows:
        current: dict[str, Any] = dict(row)
        key = str(row.get("bar_time_server", ""))
        context_row = context.get(key)
        if context_row is None:
            context_missing_rows += 1
        signal = int(round(float(row.get(SOURCE_SIGNAL_COLUMN) or 0.0)))
        if signal != 0:
            total_signal_rows += 1
        if test_id == "abl_gate_rank_bucket":
            if rank_col:
                before = current.get(rank_col)
                current[rank_col] = "1"
                if str(before) != "1":
                    rank_neutralized_rows += 1
                    changed_rows += 1
            score = 0.0
        elif test_id == "abl_gate_variant_rule":
            if gate_col and str(current.get(gate_col, "")).strip() != "":
                gate_feature_present_rows += 1
            score = 0.0
        else:
            score = proxy_score_for(test_id, context_row or {}, stats)
            current[added_feature] = score
            if score > 0.0:
                changed_rows += 1
            if signal != 0:
                signal_scores.append(score)
        scores.append(score)
        transformed.append(current)

    write_runtime_csv(destination, transformed, columns)
    feature_order = list(columns[1:])
    score_min = min(scores) if scores else 0.0
    score_max = max(scores) if scores else 0.0
    score_series = pd.Series(scores, dtype="float64") if scores else pd.Series([0.0], dtype="float64")
    signal_series = pd.Series(signal_scores, dtype="float64") if signal_scores else pd.Series([0.0], dtype="float64")
    diagnostics = {
        "queue_id": queue_row["queue_id"],
        "candidate_alias": queue_row["candidate_alias"],
        "test_id": test_id,
        "test_type": queue_row["test_type"],
        "feature_family": queue_row["feature_family"],
        "transform_type": transform_type,
        "materialization_boundary": materialization_boundary(test_id),
        "source_feature_file": rel(source),
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "added_feature": added_feature,
        "rows": len(transformed),
        "changed_rows": changed_rows,
        "context_missing_rows": context_missing_rows,
        "total_signal_rows": total_signal_rows,
        "score_min": score_min,
        "score_q50": float(score_series.quantile(0.50)),
        "score_q80": float(score_series.quantile(0.80)),
        "score_q95": float(score_series.quantile(0.95)),
        "score_max": score_max,
        "signal_score_q50": float(signal_series.quantile(0.50)),
        "signal_score_q80": float(signal_series.quantile(0.80)),
        "rank_column": rank_col or "",
        "rank_neutralized_rows": rank_neutralized_rows,
        "gate_column": gate_col or "",
        "gate_feature_present_rows": gate_feature_present_rows,
    }
    return diagnostics, feature_order


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "test_id": attempt.get("test_id"),
                "test_type": attempt.get("test_type"),
                "materialization_boundary": attempt.get("materialization_boundary"),
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def materialize_payload() -> dict[str, Any]:
    queue_rows = p0_queue_rows()
    base_features = base_features_by_alias()
    specs = specs_by_alias()
    context, context_info = source_context()
    stats = context_info["stats"]

    variant_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    diagnostics_rows: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []

    for variant_index, queue_row in enumerate(queue_rows, start=1):
        alias = str(queue_row["candidate_alias"])
        if alias not in base_features:
            raise KeyError(f"missing base feature for {alias}")
        if alias not in specs:
            raise KeyError(f"missing candidate spec for {alias}")
        spec = specs[alias]
        candidate_role = str(getattr(spec, "role", "") or "candidate_pool_member")
        base = base_features[alias]
        test_id = queue_row["test_id"]
        queue_token = safe_token(queue_row["queue_id"], 72)
        local_root = MATERIALIZATION_ROOT / "variants" / alias / queue_token
        feature_path = local_root / "features" / f"{alias}_{safe_token(test_id, 48)}.csv"
        model_path = local_root / "models" / f"{alias}_{safe_token(test_id, 48)}_model.csv"

        feature_meta, feature_order = transform_feature_file(
            Path(base["feature_file"]),
            feature_path,
            queue_row,
            context,
            stats,
        )
        variant_feature_index = "" if not feature_meta["added_feature"] else len(feature_order) - 1
        model_meta = extend_model(Path(base["model_file"]), model_path, int(variant_feature_index or 0), test_id)

        common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
        common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
        common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
        common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

        model_materialization_type = model_type_for(test_id)
        variant_row = {
            "queue_id": queue_row["queue_id"],
            "source_matrix_id": queue_row["source_matrix_id"],
            "candidate_id": queue_row["candidate_id"],
            "candidate_alias": alias,
            "candidate_role": candidate_role,
            "test_type": queue_row["test_type"],
            "test_id": test_id,
            "feature_family": queue_row["feature_family"],
            "features_or_replacements": queue_row["features_or_replacements"],
            "transform_type": feature_meta["transform_type"],
            "materialization_boundary": feature_meta["materialization_boundary"],
            "model_materialization_type": model_materialization_type,
            "source_feature_file": feature_meta["source_feature_file"],
            "feature_file": feature_meta["feature_file"],
            "feature_sha256": feature_meta["feature_sha256"],
            "source_model_file": model_meta["source_model_file"],
            "model_file": model_meta["model_file"],
            "model_sha256": model_meta["model_sha256"],
            "common_feature_path": common_feature_path,
            "common_feature_sha256": common_feature["sha256"],
            "common_model_path": common_model_path,
            "common_model_sha256": common_model["sha256"],
            "feature_count": feature_meta["feature_count"],
            "feature_order": feature_meta["feature_order"],
            "feature_order_hash": feature_meta["feature_order_hash"],
            "added_feature": feature_meta["added_feature"],
            "variant_feature_index": variant_feature_index,
            "rows": feature_meta["rows"],
            "changed_rows": feature_meta["changed_rows"],
            "context_missing_rows": feature_meta["context_missing_rows"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        variant_rows.append(variant_row)
        diagnostics_rows.append(feature_meta)
        contract_rows.append(
            {
                "queue_id": queue_row["queue_id"],
                "candidate_id": queue_row["candidate_id"],
                "candidate_alias": alias,
                "test_id": test_id,
                "shared_contract": "US100 M5;2024 historical stress window;MT5 RuntimeProbeEA;score_table_csv;attempt set/ini identity",
                "feature_count": feature_meta["feature_count"],
                "feature_order_hash": feature_meta["feature_order_hash"],
                "model_backend": "ebm_table",
                "model_materialization_type": model_materialization_type,
                "materialization_boundary": feature_meta["materialization_boundary"],
                "short_threshold": spec.variant.short_threshold,
                "long_threshold": spec.variant.long_threshold,
                "min_margin": 0.0,
                "max_hold_bars": spec.variant.max_hold_bars,
                "close_on_flat_signal": spec.variant.close_on_flat_signal,
                "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
                "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
                "known_difference": "direct gate/rank variants change runtime surface; all other P0 rows are context proxy adapters, not true internal feature ablations",
                "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
            }
        )
        lineage_rows.extend(
            [
                {
                    "queue_id": queue_row["queue_id"],
                    "artifact_role": "feature_csv",
                    "source_path": feature_meta["source_feature_file"],
                    "run267n_path": feature_meta["feature_file"],
                    "common_path": common_feature_path,
                    "run267n_sha256": feature_meta["feature_sha256"],
                    "common_sha256": common_feature["sha256"],
                },
                {
                    "queue_id": queue_row["queue_id"],
                    "artifact_role": "model_csv",
                    "source_path": model_meta["source_model_file"],
                    "run267n_path": model_meta["model_file"],
                    "common_path": common_model_path,
                    "run267n_sha256": model_meta["model_sha256"],
                    "common_sha256": common_model["sha256"],
                },
            ]
        )

        for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{safe_token(test_id, 26)}", "ta"),
                (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_{safe_token(test_id, 26)}", "rt"),
            ),
            start=1,
        ):
            magic = 26790000 + variant_index * 100 + role_index
            extra_set = dict(input_probe.base_extra_set_values(spec, magic))
            if test_id == "abl_gate_variant_rule":
                extra_set.update(
                    {
                        "InpSideFilterEnabled": False,
                        "InpBlockShortFeatureRange": False,
                        "InpBlockLongFeatureRange": False,
                    }
                )
            payload = attempt_payload(
                run_root=MATERIALIZATION_ROOT,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label=f"stage267_PoolWideP0__{safe_token(test_id, 32)}",
                attempt_name=f"{safe_token(queue_row['queue_id'], 58)}_{attempt_token}_2024",
                tier=tier,
                split=PERIOD_LABEL,
                model_path=common_model_path,
                model_id=f"{RUN_ID}_{alias}_{safe_token(test_id, 36)}",
                model_backend="ebm_table",
                feature_path=common_feature_path,
                feature_count=int(feature_meta["feature_count"]),
                feature_order_hash=str(feature_meta["feature_order_hash"]),
                short_threshold=spec.variant.short_threshold,
                long_threshold=spec.variant.long_threshold,
                min_margin=0.0,
                invert_signal=False,
                from_date="2024.01.02",
                to_date="2025.01.01",
                primary_active_tier="tier_a",
                attempt_role=attempt_role,
                record_view_prefix=prefix,
                max_hold_bars=spec.variant.max_hold_bars,
                common_root=f"{COMMON_ROOT}/{alias}/{queue_token}",
                fallback_enabled=False,
                close_on_flat_signal=spec.variant.close_on_flat_signal,
                reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                extra_set_values=extra_set,
            )
            payload.update(
                {
                    "queue_id": queue_row["queue_id"],
                    "candidate_id": queue_row["candidate_id"],
                    "candidate_alias": alias,
                    "candidate_role": candidate_role,
                    "test_id": test_id,
                    "test_type": queue_row["test_type"],
                    "materialization_boundary": feature_meta["materialization_boundary"],
                    "model_materialization_type": model_materialization_type,
                    "execution_status": "not_executed",
                }
            )
            attempts.append(payload)

    return {
        "created_at_utc": utc_now(),
        "input_queue": rel(INPUT_QUEUE_PATH),
        "input_matrix": rel(INPUT_MATRIX_PATH),
        "source_info": context_info,
        "variant_manifest": variant_rows,
        "runtime_contract": contract_rows,
        "feature_diagnostics": diagnostics_rows,
        "lineage": lineage_rows,
        "attempts": attempts,
    }


def write_outputs(result: Mapping[str, Any]) -> dict[str, Any]:
    variant_rows = list(result["variant_manifest"])
    contract_rows = list(result["runtime_contract"])
    diagnostics_rows = list(result["feature_diagnostics"])
    attempts = list(result["attempts"])
    lineage_rows = list(result["lineage"])

    write_csv(
        VARIANT_MANIFEST_PATH,
        variant_rows,
        (
            "queue_id",
            "source_matrix_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_type",
            "test_id",
            "feature_family",
            "features_or_replacements",
            "transform_type",
            "materialization_boundary",
            "model_materialization_type",
            "source_feature_file",
            "feature_file",
            "feature_sha256",
            "source_model_file",
            "model_file",
            "model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "added_feature",
            "variant_feature_index",
            "rows",
            "changed_rows",
            "context_missing_rows",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        contract_rows,
        (
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "test_id",
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "materialization_boundary",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        FEATURE_DIAGNOSTICS_PATH,
        diagnostics_rows,
        (
            "queue_id",
            "candidate_alias",
            "test_id",
            "test_type",
            "feature_family",
            "transform_type",
            "materialization_boundary",
            "source_feature_file",
            "feature_file",
            "feature_sha256",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "added_feature",
            "rows",
            "changed_rows",
            "context_missing_rows",
            "total_signal_rows",
            "score_min",
            "score_q50",
            "score_q80",
            "score_q95",
            "score_max",
            "signal_score_q50",
            "signal_score_q80",
            "rank_column",
            "rank_neutralized_rows",
            "gate_column",
            "gate_feature_present_rows",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(attempts),
        (
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "attempt_name",
            "tier",
            "split",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "fallback_enabled",
            "execution_status",
        ),
    )
    run_manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "created_at_utc": result["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "input_queue": rel(INPUT_QUEUE_PATH),
        "input_matrix": rel(INPUT_MATRIX_PATH),
        "outputs": {
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "feature_diagnostics": rel(FEATURE_DIAGNOSTICS_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": {
            "variant_manifest": sha256_file_lf_normalized(VARIANT_MANIFEST_PATH),
            "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
            "feature_diagnostics": sha256_file_lf_normalized(FEATURE_DIAGNOSTICS_PATH),
            "attempt_manifest": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
        },
        "attempt_count": len(attempts),
        "variant_count": len(variant_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    write_json(
        LINEAGE_PATH,
        {
            "source_inputs": [rel(INPUT_QUEUE_PATH), rel(INPUT_MATRIX_PATH), rel(BASE_FEATURE_MANIFEST_PATH)],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": {
                "variant_manifest": rel(VARIANT_MANIFEST_PATH),
                "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
                "feature_diagnostics": rel(FEATURE_DIAGNOSTICS_PATH),
                "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
                "run_manifest": rel(RUN_MANIFEST_PATH),
            },
            "lineage_rows": lineage_rows,
            "registry_links": ["artifact_registry.csv", "run_registry.csv", "alpha_run_ledger.csv", "stage_run_ledger.csv"],
            "availability": "tracked_plus_common_files_copy(추적 산출물 + Common Files 복사)",
            "lineage_judgment": "connected_with_boundary(경계付き 연결)",
        },
    )
    final_result = {
        **dict(result),
        "run_manifest": run_manifest,
        "variant_count": len(variant_rows),
        "attempt_count": len(attempts),
        "candidate_count": len({row["candidate_alias"] for row in variant_rows}),
        "direct_variant_count": sum(
            1 for row in variant_rows if str(row["materialization_boundary"]).startswith("direct_runtime_surface_ablation")
        ),
        "proxy_variant_count": sum(
            1
            for row in variant_rows
            if str(row["materialization_boundary"]).startswith("proxy_adapter_variant")
        ),
    }
    write_json(RESULT_PATH, final_result)
    write_md(REPORT_PATH, report_markdown(final_result))
    return final_result


def report_markdown(result: Mapping[str, Any]) -> str:
    variants = list(result["variant_manifest"])
    attempts = list(result["attempts"])
    candidate_counts = Counter(row["candidate_alias"] for row in variants)
    boundary_counts = Counter(row["materialization_boundary"] for row in variants)
    test_counts = Counter(row["test_id"] for row in variants)
    candidate_lines = [
        f"| `{candidate}` | {count} |"
        for candidate, count in sorted(candidate_counts.items())
    ]
    boundary_lines = [
        f"| `{boundary}` | {count} |"
        for boundary, count in sorted(boundary_counts.items())
    ]
    test_lines = [
        f"| `{test}` | {count} |"
        for test, count in sorted(test_counts.items())
    ]
    return "\n".join(
        [
            "# Stage267 Run267N Pool-wide P0 Materialization(267N 후보군 전체 P0 물질화)",
            "",
            "## Summary(요약)",
            "",
            f"- status(상태): `{STATUS}`",
            f"- run_id(실행 ID): `{RUN_ID}`",
            "- primary_family(주 작업군): `experiment_materialization(실험 물질화)`.",
            "- primary_skill(주 스킬): `obsidian-artifact-lineage(산출물 계보)`.",
            "- support_skills(보조 스킬): `obsidian-data-integrity(데이터 무결성)`, `obsidian-model-validation(모델 검증)`, `obsidian-result-judgment(결과 판정)`.",
            f"- action(행동): run267M(267M 실행)의 P0 materialization queue(P0 물질화 큐) `{len(variants)}`개를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 고정했다.",
            f"- effect(효과): 다음 MT5(MetaTrader 5, 메타트레이더5) 실행이 말로 된 계획이 아니라 `{len(attempts)}`개 attempt(시도) 정체성으로 이어진다.",
            "",
            "## Materialized Scope(물질화 범위)",
            "",
            f"- candidate_count(후보 수): `{result['candidate_count']}`.",
            f"- variant_count(변형 수): `{result['variant_count']}`.",
            f"- attempt_count(시도 수): `{result['attempt_count']}`.",
            f"- direct_variant_count(직접 변형 수): `{result['direct_variant_count']}`.",
            f"- proxy_variant_count(대체 변형 수): `{result['proxy_variant_count']}`.",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`.",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`.",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`.",
            "",
            "## Candidate Queue(후보 큐)",
            "",
            "| candidate(후보) | variants(변형) |",
            "| --- | ---: |",
            *candidate_lines,
            "",
            "## Boundary Counts(경계 수)",
            "",
            "| boundary(경계) | variants(변형) |",
            "| --- | ---: |",
            *boundary_lines,
            "",
            "## Test Counts(시험 수)",
            "",
            "| test_id(시험 ID) | variants(변형) |",
            "| --- | ---: |",
            *test_lines,
            "",
            "## Data Integrity(데이터 무결성)",
            "",
            f"- data_source(데이터 원천): run267M queue(267M 큐) `{rel(INPUT_QUEUE_PATH)}`, base 2024 feature manifest(기초 2024 피처 목록) `{rel(BASE_FEATURE_MANIFEST_PATH)}`.",
            "- time_axis(시간축): FPMarkets US100 M5 broker-time bar close(FPMarkets US100 M5 브로커 시간 봉 마감)로 MT5 CSV와 맞춘다.",
            "- sample_scope(표본 범위): 2024 Tier A historical stress(2024 티어 A 과거 압박) 실행 준비.",
            "- feature_label_boundary(피처/라벨 경계): 이번 run(실행)은 새 label(라벨)을 만들지 않고, 기존 2024 source context(원천 문맥)에서 실행 피처만 만든다.",
            "- split_boundary(분리 경계): 2024는 robustness stress(견고성 압박)이며 학습 선택 근거로 과장하지 않는다.",
            "- leakage_risk(누수 위험): 약한 월/ADX/ATR 단서를 target(목표)으로 학습하면 누수 또는 선택 편향이 된다. 이번 산출물은 execution pending(실행 대기) 정체성만 제공한다.",
            "- integrity_judgment(무결성 판정): `usable_with_boundary(경계付き 사용 가능)`.",
            "",
            "## Model Validation(모델 검증)",
            "",
            "- model_family(모델군): baseline score-table CSV(기준 점수표 CSV)와 proxy score extension(대체 점수 확장).",
            "- threshold_policy(문턱값 정책): 기존 후보 threshold(문턱값)를 유지하고 새 threshold search(문턱값 탐색)는 하지 않았다.",
            "- overfit_risk(과적합 위험): proxy variant(대체 변형)가 약한 구간을 직접 겨냥하므로, MT5 결과가 나와도 단일 최고 숫자로 선택하면 안 된다.",
            "- calibration_risk(보정 위험): score-table(점수표)은 probability(확률)가 아니라 decision surface(의사결정 표면)이다.",
            "- validation_judgment(검증 판정): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 선택 후보 없음)`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(INPUT_QUEUE_PATH)}`, `{rel(INPUT_MATRIX_PATH)}`, `{rel(BASE_FEATURE_MANIFEST_PATH)}`.",
            f"- producer(생성자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{NEXT_ACTION}`.",
            "- availability(가용성): tracked repo artifacts(저장소 추적 산출물)와 MT5 Common Files(Common Files 인계 복사)를 함께 둔다.",
            "- lineage_judgment(계보 판정): `connected_with_boundary(경계付き 연결)`.",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(판정 대상): run267N pool-wide P0 materialization(267N 후보군 전체 P0 물질화).",
            "- evidence_available(있는 근거): variant manifest(변형 목록), runtime contract(런타임 계약), feature diagnostics(피처 진단), attempts(시도 목록), lineage(계보), run manifest(실행 목록).",
            "- evidence_missing(없는 근거): MT5 execution(MT5 실행), trade records(거래 기록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 선택 후보 없음)`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifacts = [
        ("stage267_run267N_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267N pool-wide P0 materialization."),
        ("stage267_run267N_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267N materialized variant manifest."),
        ("stage267_run267N_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267N runtime contract."),
        ("stage267_run267N_feature_diagnostics", "feature_diagnostics", FEATURE_DIAGNOSTICS_PATH, "Run267N feature diagnostics."),
        ("stage267_run267N_attempts", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267N MT5 attempt manifest."),
        ("stage267_run267N_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267N run manifest."),
        ("stage267_run267N_lineage", "lineage", LINEAGE_PATH, "Run267N lineage."),
        ("stage267_run267N_result", "result", RESULT_PATH, "Run267N JSON result."),
        ("stage267_run267N_report", "review_report", REPORT_PATH, "User-facing run267N materialization report."),
    ]
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in artifacts
    ]


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267N_pool_wide_ablation_replacement_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_ablation_replacement_p0_materialization",
            "tier_scope": "Tier A and actual routed total attempts planned",
            "scoreboard": "experiment_materialization",
            "status": STATUS,
            "judgment": "materialized_execution_pending_no_candidate_selection",
            "evidence_boundary": "set_ini_feature_model_manifest_only_no_mt5_kpi_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};direct={result['direct_variant_count']};proxy={result['proxy_variant_count']};next_action={NEXT_ACTION}.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__pool_wide_ablation_replacement_p0_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "pool_wide_ablation_replacement_p0_materialization",
                "parent_run_id": RUN_ID,
                "record_view": "pool_wide_ablation_replacement_p0_materialization",
                "tier_scope": "Tier A and actual routed total attempts planned",
                "kpi_scope": "materialization_identity_no_mt5_kpi",
                "scoreboard_lane": "experiment_materialization",
                "status": STATUS,
                "judgment": "materialized_execution_pending_no_candidate_selection",
                "path": rel(REPORT_PATH),
                "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_started_materialization_only",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_pool_wide_p0_materialization",
                "status": STATUS,
                "judgment": "materialized_execution_pending_no_candidate_selection",
                "path": rel(REPORT_PATH),
                "notes": f"Run267N P0 materialization; variants={result['variant_count']}; attempts={result['attempt_count']}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    for row in artifact_rows(created_at):
        upsert_csv(
            ARTIFACT_REGISTRY_PATH,
            "artifact_id",
            row,
            ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        )


def update_current_working_state() -> None:
    text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_ablation_replacement_p0_materialization`")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    evidence_line = f"- Stage267(267단계) run267N pool-wide P0 materialization(후보군 전체 P0 물질화): `{rel(REPORT_PATH)}`"
    text = append_after_contains(text, "stage267_run267M_pool_wide_ablation_replacement_design.md", evidence_line)
    latest_line = f"- latest_materialization(최신 물질화): run267N(267N 실행) pool-wide P0 materialization(후보군 전체 P0 물질화) `{rel(REPORT_PATH)}`."
    text = append_after_contains(text, "latest_design(최신 설계): run267M", latest_line)
    text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    text = replace_line_prefix(
        text,
        "- action(행동):",
        "- action(행동): run267N(267N 실행)는 run267M(267M 실행)의 P0 queue(P0 큐)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.",
    )
    text = replace_line_prefix(
        text,
        "- effect(효과):",
        "- effect(효과): 다음 작업은 같은 후보군의 P0 변형을 MT5(MetaTrader 5, 메타트레이더5)에서 실행해 누가 덜 깨지는지 확인할 수 있다.",
    )
    text = replace_line_prefix(
        text,
        "- next_action(다음 행동):",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 물질화된 P0 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) 묶음 실행으로 넘긴다.",
    )
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter MT5 review(P0 부드러운 비달력 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭)가 여전히 불편해 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267K(267K 실행)는 retrained soft-context Adapter MT5 review(재학습 부드러운 문맥 어댑터 MT5 검토)를 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 좋아졌지만 Monday(월요일), 2024-12 약점과 거래 수 축소가 남았다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 salvage clue(회수 단서)로 가지치기했다.\n"
            "Effect(효과): 한 후보 수리 루프를 끊고 후보군 전체 검증으로 되돌렸다.\n\n"
            "Run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 설계했다.\n"
            "Effect(효과): 다음 행동을 한 후보 미세 수리가 아니라 후보군 전체 P0 물질화로 전환했다.\n\n"
            "Run267N(267N 실행)는 run267M(267M 실행)의 P0 queue(P0 큐)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.\n"
            f"Effect(효과): 다음 행동(next action, 다음 행동)은 `{NEXT_ACTION}`이고, 아직 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 없다.\n"
        ),
    )
    write_md(CURRENT_WORKING_STATE_PATH, text)


def update_selection_status() -> None:
    text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    text = append_after_contains(
        text,
        "run267M_pool_wide_ablation_replacement_design",
        f"- run267N_pool_wide_ablation_replacement_materialization(267N 후보군 전체 제거/대체 물질화): `{rel(REPORT_PATH)}`",
    )
    text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 standalone candidate(독립 후보)가 아니라 salvage clue(회수 단서)로 가지치기했다.\n"
            "Effect(효과): selected candidate(선택 후보)는 없고, 후보군 전체 설계로 되돌아갔다.\n\n"
            "Run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 설계했다.\n"
            "Effect(효과): selected candidate(선택 후보)는 없고, 후보군 전체 P0 물질화로 넘어갔다.\n\n"
            "Run267N(267N 실행)는 다섯 Baseline candidates(기준 후보)의 P0 ablation/replacement(우선 제거/대체)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.\n"
            f"Effect(효과): selected candidate(선택 후보)는 여전히 없고, next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
        ),
    )
    write_md(SELECTION_STATUS_PATH, text)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    text = append_after_contains(
        text,
        "run267M_pool_wide_ablation_replacement_design",
        f"- run267N_pool_wide_ablation_replacement_materialization(267N 후보군 전체 제거/대체 물질화): `{rel(REPORT_PATH)}`",
    )
    text = replace_tail_from_marker(
        text,
        "Run267I(267I 실행)는",
        (
            "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화), MT5 execution(MT5 실행), MT5 review(MT5 검토)까지 완료했다.\n"
            "Effect(효과): 순수익/PF(profit factor, 수익 팩터)는 2024년 원형보다 좋아졌지만 DD(drawdown, 손실폭), Monday(월요일), July(7월), chron_mid(중간 순서 구간) 약점이 남아 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n\n"
            "Run267L(267L 실행)는 retrained soft-context branch(재학습 부드러운 문맥 분기)를 standalone candidate(독립 후보)가 아니라 salvage clue(회수 단서)로 가지치기했다.\n"
            "Effect(효과): selected candidate(선택 후보)는 없고, 후보군 전체 설계로 되돌아갔다.\n\n"
            "Run267M(267M 실행)는 다섯 Baseline candidates(기준 후보) 전체의 ablation/replacement(제거/대체), weak-slice matrix(약한 구간 행렬), P0 materialization queue(P0 물질화 큐)를 설계했다.\n"
            "Effect(효과): selected candidate(선택 후보)는 없고, 후보군 전체 P0 물질화로 넘어갔다.\n\n"
            "Run267N(267N 실행)는 다섯 Baseline candidates(기준 후보)의 P0 ablation/replacement(우선 제거/대체)를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.\n"
            f"Effect(효과): selected candidate(선택 후보)는 여전히 없고, next_action(다음 행동)은 `{NEXT_ACTION}`이다.\n"
        ),
    )
    write_md(REVIEW_INDEX_PATH, text)


def update_workspace_state() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267N(267N 실행) pool-wide P0 materialization(후보군 전체 P0 물질화) `{STATUS}`. Effect(효과): run267M(267M 실행)의 P0 queue(P0 큐)를 `{len(p0_queue_rows())}`개 feature/model/set/ini(피처/모델/설정/초기화) 변형과 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)로 고정했으며 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다."
    )
    if f"`{STATUS}`" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    text = text.replace(
        "  Next action(다음 행동)는 `run267N_materialize_pool_wide_ablation_replacement_p0`이다. Effect(효과): P0 ablation/replacement(우선 제거/대체) 변형을 물질화해 MT5(MetaTrader 5, 메타트레이더5) 실행 준비로 넘긴다.",
        f"  Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): 물질화된 P0 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) 묶음 실행으로 넘긴다.",
        1,
    )
    text = text.replace(
        "is active_run267M_pool_wide_ablation_replacement_design_completed(267M 후보군 전체 제거/대체 설계 완료 활성).",
        "is active_run267N_pool_wide_ablation_replacement_materialized_execution_pending(267N 후보군 전체 제거/대체 물질화 완료, 실행 대기 활성).",
        1,
    )
    text = text.replace("  status: run267M_pool_wide_ablation_replacement_design_completed", f"  status: {STATUS}", 1)
    text = text.replace("  current_run_id: run267M_stage267_pool_wide_ablation_replacement_design_v1", f"  current_run_id: {RUN_ID}", 1)
    text = text.replace("  last_completed_run_id: run267M_stage267_pool_wide_ablation_replacement_design_v1", f"  last_completed_run_id: {RUN_ID}", 1)
    text = append_after_contains(
        text,
        "run267M_pool_wide_ablation_replacement_design_path",
        f"  run267N_pool_wide_ablation_replacement_materialization_path: {rel(REPORT_PATH)}",
    )
    text = text.replace("  next_action: run267N_materialize_pool_wide_ablation_replacement_p0", f"  next_action: {NEXT_ACTION}", 1)
    write_md(WORKSPACE_STATE_PATH, text)


def update_docs() -> None:
    update_current_working_state()
    update_selection_status()
    update_review_index()
    update_workspace_state()


def materialize() -> dict[str, Any]:
    payload = materialize_payload()
    result = write_outputs(payload)
    update_ledgers(result)
    update_docs()
    return result


def main() -> int:
    result = materialize()
    print(
        json.dumps(
            {
                "status": STATUS,
                "candidate_count": result["candidate_count"],
                "variant_count": result["variant_count"],
                "attempt_count": result["attempt_count"],
                "direct_variant_count": result["direct_variant_count"],
                "proxy_variant_count": result["proxy_variant_count"],
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
