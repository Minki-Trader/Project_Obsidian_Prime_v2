from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss

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
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
)
from foundation.models.ebm_explainable import (
    EbmVariantSpec,
    fit_ebm_variant,
    probability_frame,
    term_importance_frame,
)
from foundation.models.ebm_score_table import (
    check_ebm_score_table_probability_parity,
    export_ebm_main_effect_score_table,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267K_retrained_soft_context_adapter_materialization as source_retrain
from stage_pipelines.stage267 import run267V_reconstruct_upstream_feature_surface as source_surface


STAGE_ID = input_probe.STAGE_ID
RUN_NUMBER = "run267W"
RUN_ID = "run267W_stage267_true_internal_ablation_score_table_materialization_v1"
PARENT_RUN_ID = source_surface.RUN_ID
STATUS = "run267W_true_internal_ablation_score_tables_materialized_execution_pending"
NEXT_ACTION = "run267X_execute_true_internal_ablation_score_table_mt5_batch"
JUDGMENT = "score_tables_materialized_execution_pending_no_candidate_selection"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "true_internal_ablation_score_table_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

INPUT_QUEUE_PATH = source_surface.RUN267W_QUEUE_PATH
INPUT_SCHEMA_PATH = source_surface.TRUE_INTERNAL_SCHEMA_MATRIX_PATH
INPUT_SURFACE_MANIFEST_PATH = source_surface.CANDIDATE_SURFACE_MANIFEST_PATH
INPUT_FAMILY_MAP_PATH = source_surface.FEATURE_FAMILY_COLUMN_MAP_PATH
INPUT_RUN267V_RESULT_PATH = source_surface.RESULT_PATH
RUN267V_REPORT_PATH = source_surface.REPORT_PATH

VARIANT_MANIFEST_PATH = RUN_ROOT / "true_internal_ablation_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
TRAINING_DIAGNOSTICS_PATH = RUN_ROOT / "training_frame_diagnostics.csv"
MODEL_VALIDATION_PATH = RUN_ROOT / "model_validation_snapshot.csv"
TERM_IMPORTANCE_PATH = RUN_ROOT / "term_importance.csv"
PARITY_CHECK_PATH = RUN_ROOT / "score_table_parity_check.csv"
SURFACE_ALIGNMENT_PATH = RUN_ROOT / "surface_alignment_check.csv"
SCHEMA_CORRECTION_PATH = RUN_ROOT / "schema_correction_audit.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempts.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267W_true_internal_ablation_score_table_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267W_true_internal_ablation_score_table_materialization.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267w/run267W_true_internal_ablation"
PERIOD_LABEL = input_probe.PERIOD_LABEL
SOURCE_SIGNAL_COLUMN = input_probe.SOURCE_SIGNAL_COLUMN
MODEL_MATERIALIZATION_TYPE = "supervised_ebm_true_internal_ablation_main_effect_v1"
MODEL_FAMILY = "ebm_main_effect_classifier_supervised_label_retrain"
TRAINING_CONTRACT_PATH = source_retrain.TRAINING_CONTRACT_PATH
MODEL_INPUT_CONTRACT_PATH = source_retrain.MODEL_INPUT_CONTRACT_PATH
MODEL_INPUT_DATASET_PATH = source_retrain.MODEL_INPUT_DATASET_PATH

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def q(values: Sequence[float], quantile: float) -> float:
    series = pd.Series([float(item) for item in values if math.isfinite(float(item))], dtype="float64")
    if series.empty:
        return 0.0
    return float(series.quantile(float(quantile)))


def split_semicolon(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def prepend_current_focus(text: str, block: str) -> str:
    if block.strip() in text:
        return text
    marker = "current_focus:\n"
    if marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def require_inputs() -> None:
    required = [
        INPUT_QUEUE_PATH,
        INPUT_SCHEMA_PATH,
        INPUT_SURFACE_MANIFEST_PATH,
        INPUT_FAMILY_MAP_PATH,
        INPUT_RUN267V_RESULT_PATH,
        MODEL_INPUT_DATASET_PATH,
        TRAINING_CONTRACT_PATH,
        MODEL_INPUT_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def rows_by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row[key]): row for row in rows if str(row.get(key, "")).strip()}


def rows_by_candidate_test(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], Mapping[str, str]]:
    return {
        (str(row.get("candidate_alias", "")), str(row.get("test_id", ""))): row
        for row in rows
        if str(row.get("candidate_alias", "")).strip() and str(row.get("test_id", "")).strip()
    }


def candidate_full_feature_order(spec: Any) -> tuple[list[str], str, str]:
    extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
    rank_column = str(spec.module.RANK_COLUMN)
    gate_column = f"{spec.module.GATE_COLUMN_PREFIX}_{extra['axis']}"
    return [SOURCE_SIGNAL_COLUMN, rank_column, gate_column, *source_surface.RAW_SURFACE_COLUMNS], rank_column, gate_column


def candidate_training_frame(source: pd.DataFrame, spec: Any) -> tuple[pd.DataFrame, dict[str, Any]]:
    full_order, rank_column, gate_column = candidate_full_feature_order(spec)
    extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
    rows: list[dict[str, Any]] = []
    for record in source.to_dict("records"):
        mapped = input_probe.row_mapping(record)
        signal = int(round(spec.module.s250.stage238.parse_float(mapped.get(SOURCE_SIGNAL_COLUMN), 0.0)))
        bucket_value, _ = spec.module.s250.stage238.rank_bucket_for(mapped)
        gate = spec.module.source_branch_gate_value(mapped, str(extra["source_branch_mode"]))
        payload: dict[str, Any] = {
            "timestamp": pd.Timestamp(record["timestamp"]),
            "symbol": record.get("symbol") or "US100",
            "split": str(record.get("split")),
            "label": str(record.get("label")),
            "label_class": int(record.get("label_class")),
            "bar_time_server": mapped["bar_time_server"],
            SOURCE_SIGNAL_COLUMN: float(signal),
            rank_column: float(bucket_value),
            gate_column: float(gate),
        }
        for column in source_surface.RAW_SURFACE_COLUMNS:
            payload[column] = as_float(record.get(column), default=float("nan"))
        rows.append(payload)
    frame = pd.DataFrame.from_records(rows)
    diagnostics = {
        "candidate_id": spec.candidate_id,
        "candidate_alias": spec.alias,
        "candidate_role": spec.role,
        "rank_column": rank_column,
        "gate_column": gate_column,
        "full_feature_count": len(full_order),
        "full_feature_order_hash": ordered_hash(full_order),
        "rows": int(len(frame)),
        "train_rows": int(frame["split"].eq("train").sum()),
        "validation_rows": int(frame["split"].eq("validation").sum()),
        "oos_rows": int(frame["split"].eq("oos").sum()),
        "signal_rows": int((frame[SOURCE_SIGNAL_COLUMN].astype(float) != 0.0).sum()),
        "blocked_signal_rows": int(((frame[SOURCE_SIGNAL_COLUMN].astype(float) != 0.0) & (frame[gate_column].astype(float) >= 0.5)).sum()),
        "missing_feature_cells": int(frame.loc[:, full_order].isna().sum().sum()),
    }
    return frame, diagnostics


def actual_feature_order(schema_row: Mapping[str, str], spec: Any) -> tuple[list[str], dict[str, Any]]:
    full_order, rank_column, gate_column = candidate_full_feature_order(spec)
    removed = split_semicolon(schema_row.get("removed_columns"))
    test_id = str(schema_row.get("test_id", ""))
    correction_reason = "none"
    if test_id == "abl_gate_rank_bucket" and rank_column not in removed:
        removed.append(rank_column)
        correction_reason = "direct_rank_column_removed_in_run267W"
    if test_id == "abl_gate_variant_rule" and gate_column not in removed:
        removed.append(gate_column)
        correction_reason = "direct_gate_column_removed_in_run267W"
    removed_set = set(removed)
    order = [column for column in full_order if column not in removed_set]
    target_hash = str(schema_row.get("variant_feature_order_hash", ""))
    actual_hash = ordered_hash(order)
    return order, {
        "removed_columns_actual": ";".join(removed),
        "removed_column_count_actual": len(removed),
        "target_feature_order_hash": target_hash,
        "actual_feature_order_hash": actual_hash,
        "target_hash_status": "matches_run267V_schema" if actual_hash == target_hash else "corrected_from_run267V_schema",
        "correction_reason": correction_reason,
        "gate_column": gate_column,
        "rank_column": rank_column,
        "gate_feature_index": order.index(gate_column) if gate_column in order else "",
        "rank_feature_index": order.index(rank_column) if rank_column in order else "",
    }


def write_runtime_feature_from_surface(
    surface_file: Path,
    destination: Path,
    feature_order: Sequence[str],
) -> tuple[dict[str, Any], pd.DataFrame]:
    surface = pd.read_csv(io_path(surface_file), encoding="utf-8-sig")
    missing = [column for column in ("bar_time_server", *feature_order) if column not in surface.columns]
    if missing:
        raise KeyError(f"missing runtime feature columns for {surface_file}: {missing}")
    selected = surface.loc[:, ["bar_time_server", *feature_order]].copy()
    rows = selected.to_dict("records")
    write_runtime_csv(destination, rows, ("bar_time_server", *feature_order))
    duplicate_times = int(selected["bar_time_server"].duplicated().sum())
    feature_missing = int(selected.loc[:, list(feature_order)].isna().sum().sum())
    return {
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "rows": int(len(selected)),
        "first_bar_time_server": str(selected["bar_time_server"].iloc[0]) if len(selected) else "",
        "last_bar_time_server": str(selected["bar_time_server"].iloc[-1]) if len(selected) else "",
        "duplicate_bar_time_rows": duplicate_times,
        "runtime_missing_feature_cells": feature_missing,
    }, selected


def training_stress_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.loc[
        frame["split"].eq("train")
        & frame["timestamp"].ge(pd.Timestamp("2024-01-01", tz="UTC"))
        & frame["timestamp"].lt(pd.Timestamp("2025-01-01", tz="UTC"))
    ].copy()


def split_diagnostics(
    queue_id: str,
    candidate_alias: str,
    test_id: str,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        part = frame.loc[frame["split"].eq(split)]
        labels = {str(k): int(v) for k, v in part["label_class"].value_counts().sort_index().items()}
        rows.append(
            {
                "queue_id": queue_id,
                "candidate_alias": candidate_alias,
                "test_id": test_id,
                "split": split,
                "rows": int(len(part)),
                "class_counts": json.dumps(labels, ensure_ascii=False, sort_keys=True),
                "missing_feature_cells": int(part.loc[:, list(feature_order)].isna().sum().sum()) if len(part) else 0,
            }
        )
    stress = training_stress_frame(frame)
    labels = {str(k): int(v) for k, v in stress["label_class"].value_counts().sort_index().items()}
    rows.append(
        {
            "queue_id": queue_id,
            "candidate_alias": candidate_alias,
            "test_id": test_id,
            "split": PERIOD_LABEL,
            "rows": int(len(stress)),
            "class_counts": json.dumps(labels, ensure_ascii=False, sort_keys=True),
            "missing_feature_cells": int(stress.loc[:, list(feature_order)].isna().sum().sum()) if len(stress) else 0,
        }
    )
    return rows


def validation_snapshot(
    queue_id: str,
    candidate_alias: str,
    test_id: str,
    probabilities: pd.DataFrame,
    spec: Any,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        part = probabilities.loc[probabilities["split"].astype(str).eq(split)]
        if part.empty:
            continue
        y = part["label_class"].astype("int64").to_numpy()
        proba = part.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64")
        pred = proba.argmax(axis=1)
        short_decision = (part["p_short"].to_numpy(dtype="float64") >= float(spec.variant.short_threshold)) & (
            part["p_short"].to_numpy(dtype="float64") > part["p_long"].to_numpy(dtype="float64")
        )
        long_decision = (part["p_long"].to_numpy(dtype="float64") >= float(spec.variant.long_threshold)) & (
            part["p_long"].to_numpy(dtype="float64") > part["p_short"].to_numpy(dtype="float64")
        )
        rows.append(
            {
                "queue_id": queue_id,
                "candidate_alias": candidate_alias,
                "test_id": test_id,
                "split": split,
                "rows": int(len(part)),
                "accuracy": float(accuracy_score(y, pred)),
                "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
                "log_loss": float(log_loss(y, proba, labels=[0, 1, 2])),
                "short_threshold": float(spec.variant.short_threshold),
                "long_threshold": float(spec.variant.long_threshold),
                "short_threshold_decisions": int(short_decision.sum()),
                "long_threshold_decisions": int(long_decision.sum()),
                "flat_or_no_trade_decisions": int(len(part) - short_decision.sum() - long_decision.sum()),
                "selection_metric": "offline_label_sanity_only_not_trading_selection",
                "validation_judgment": "materialized_for_mt5_test_not_candidate_selection",
            }
        )
    return rows


def surface_alignment_row(
    queue_id: str,
    candidate_alias: str,
    test_id: str,
    feature_order: Sequence[str],
    runtime_surface: pd.DataFrame,
    candidate_frame: pd.DataFrame,
    runtime_meta: Mapping[str, Any],
) -> dict[str, Any]:
    stress = training_stress_frame(candidate_frame)
    expected_times = list(stress["bar_time_server"].astype(str))
    runtime_times = list(runtime_surface["bar_time_server"].astype(str))
    time_match = expected_times == runtime_times
    missing_in_runtime = [column for column in feature_order if column not in runtime_surface.columns]
    return {
        "queue_id": queue_id,
        "candidate_alias": candidate_alias,
        "test_id": test_id,
        "runtime_rows": int(len(runtime_surface)),
        "training_2024_rows": int(len(stress)),
        "bar_time_order_match": bool(time_match),
        "duplicate_bar_time_rows": int(runtime_meta["duplicate_bar_time_rows"]),
        "runtime_missing_feature_cells": int(runtime_meta["runtime_missing_feature_cells"]),
        "missing_runtime_columns": ";".join(missing_in_runtime),
        "alignment_status": "pass" if time_match and not missing_in_runtime else "invalid",
    }


def extra_set_for_feature_order(spec: Any, feature_order: Sequence[str], gate_column: str, magic: int) -> dict[str, Any]:
    values = dict(input_probe.base_extra_set_values(spec, magic))
    if gate_column in feature_order:
        gate_index = int(list(feature_order).index(gate_column))
        values["InpSideFilterEnabled"] = True
        values["InpSideFilterFeatureIndex"] = gate_index
        values["InpFallbackSideFilterFeatureIndex"] = gate_index
    else:
        values["InpSideFilterEnabled"] = False
        values["InpBlockShortFeatureRange"] = False
        values["InpBlockLongFeatureRange"] = False
        values["InpSideFilterFeatureIndex"] = 0
        values["InpFallbackSideFilterFeatureIndex"] = 0
    values["InpMagic"] = magic
    return values


def fit_variant(
    schema_row: Mapping[str, str],
    queue_row: Mapping[str, str],
    spec: Any,
    candidate_frame: pd.DataFrame,
    source_info: Mapping[str, Any],
    variant_index: int,
) -> dict[str, Any]:
    queue_id = str(queue_row["queue_id"])
    test_id = str(queue_row["test_id"])
    feature_order, correction = actual_feature_order(schema_row, spec)
    queue_token = safe_token(queue_id, 72)
    local_root = VARIANT_ROOT / spec.alias / queue_token
    feature_path = local_root / "features" / f"{spec.alias}_{safe_token(test_id, 48)}_true_internal.csv"
    model_path = local_root / "models" / f"{spec.alias}_{safe_token(test_id, 48)}_true_internal_model.csv"

    runtime_meta, runtime_surface = write_runtime_feature_from_surface(
        repo_path(str(queue_row["input_surface_file"])),
        feature_path,
        feature_order,
    )
    alignment = surface_alignment_row(
        queue_id,
        spec.alias,
        test_id,
        feature_order,
        runtime_surface,
        candidate_frame,
        runtime_meta,
    )
    if alignment["alignment_status"] != "pass":
        raise RuntimeError(f"surface alignment failed for {queue_id}: {alignment}")

    train_frame = candidate_frame.loc[:, ["timestamp", "symbol", "split", "label", "label_class", *feature_order]].copy()
    ebm_spec = EbmVariantSpec(
        variant_id=f"{spec.alias}_{safe_token(test_id, 36)}_true_internal_ablation_v1",
        idea_id="stage267_true_internal_feature_ablation",
        description=f"Stage267 true internal feature ablation score table for {spec.alias} {test_id}.",
        max_bins=32,
        interactions=0,
        outer_bags=1,
        learning_rate=0.04,
        max_rounds=80,
        early_stopping_rounds=15,
        min_samples_leaf=24,
        reg_lambda=0.01,
        random_state=26720 + variant_index,
    )
    model, fit_info = fit_ebm_variant(train_frame, feature_order, ebm_spec)
    model_meta = export_ebm_main_effect_score_table(model, model_path, feature_count=len(feature_order))
    validation_sample = train_frame.loc[train_frame["split"].eq("validation")].head(2048)
    parity = check_ebm_score_table_probability_parity(
        model,
        model_path,
        validation_sample.loc[:, feature_order].to_numpy(dtype="float64"),
        feature_count=len(feature_order),
    )
    probabilities = probability_frame(model, train_frame, feature_order)
    importance = term_importance_frame(model, feature_order)
    importance_rows = [
        {
            "queue_id": queue_id,
            "candidate_id": spec.candidate_id,
            "candidate_alias": spec.alias,
            "test_id": test_id,
            "feature_family": queue_row.get("feature_family"),
            **row,
        }
        for row in importance.to_dict("records")
    ]

    common_feature_path = f"{COMMON_ROOT}/{spec.alias}/{queue_token}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{spec.alias}/{queue_token}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    attempts: list[dict[str, Any]] = []
    for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
        (
            (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{spec.alias}_{safe_token(test_id, 26)}_true", "ta"),
            (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{spec.alias}_{safe_token(test_id, 26)}_true", "rt"),
        ),
        start=1,
    ):
        magic = 26720000 + variant_index * 100 + role_index
        payload = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=267,
            exploration_label=f"stage267_TrueInternalAblation__{safe_token(test_id, 32)}",
            attempt_name=f"{queue_token}_{attempt_token}_2024",
            tier=tier,
            split=PERIOD_LABEL,
            model_path=common_model_path,
            model_id=f"{RUN_ID}_{spec.alias}_{safe_token(test_id, 36)}",
            model_backend="ebm_table",
            feature_path=common_feature_path,
            feature_count=len(feature_order),
            feature_order_hash=ordered_hash(feature_order),
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
            common_root=f"{COMMON_ROOT}/{spec.alias}/{queue_token}",
            fallback_enabled=False,
            close_on_flat_signal=spec.variant.close_on_flat_signal,
            reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
            close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
            extra_set_values=extra_set_for_feature_order(spec, feature_order, str(correction["gate_column"]), magic),
        )
        payload.update(
            {
                "queue_id": queue_id,
                "candidate_id": spec.candidate_id,
                "candidate_alias": spec.alias,
                "candidate_role": spec.role,
                "test_id": test_id,
                "feature_family": queue_row.get("feature_family"),
                "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                "execution_status": "not_executed",
            }
        )
        attempts.append(payload)

    validation_rows = validation_snapshot(queue_id, spec.alias, test_id, probabilities, spec)
    training_rows = split_diagnostics(queue_id, spec.alias, test_id, candidate_frame, feature_order)
    top_importance = importance.head(8)
    top_terms = ";".join(str(item) for item in top_importance["feature"].tolist())
    top_gain_share = float(top_importance["gain_share"].sum()) if not top_importance.empty else 0.0
    manifest = {
        "queue_id": queue_id,
        "source_schema_id": schema_row.get("schema_id"),
        "candidate_id": spec.candidate_id,
        "candidate_alias": spec.alias,
        "candidate_role": spec.role,
        "test_id": test_id,
        "feature_family": queue_row.get("feature_family"),
        "queue_lane": queue_row.get("queue_lane"),
        "model_family": MODEL_FAMILY,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "source_model_file": rel(spec.model_path),
        "input_surface_file": queue_row.get("input_surface_file"),
        "runtime_feature_file": runtime_meta["feature_file"],
        "runtime_feature_sha256": runtime_meta["feature_sha256"],
        "runtime_model_file": rel(model_path),
        "runtime_model_sha256": model_meta["sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "removed_columns_actual": correction["removed_columns_actual"],
        "removed_column_count_actual": correction["removed_column_count_actual"],
        "target_feature_order_hash": correction["target_feature_order_hash"],
        "target_hash_status": correction["target_hash_status"],
        "gate_feature_index": correction["gate_feature_index"],
        "rank_feature_index": correction["rank_feature_index"],
        "train_rows": int(fit_info["train_rows"]),
        "source_rows": int(source_info["rows"]),
        "runtime_rows": int(runtime_meta["rows"]),
        "parity_passed": parity["passed"],
        "parity_max_abs_diff": parity["max_abs_diff"],
        "top8_gain_share": top_gain_share,
        "top8_terms": top_terms,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    contract = {
        "queue_id": queue_id,
        "candidate_id": spec.candidate_id,
        "candidate_alias": spec.alias,
        "test_id": test_id,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;true_internal_feature_order;supervised_EBM_score_table_csv;attempt set/ini identity",
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "model_backend": "ebm_table",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "short_threshold": spec.variant.short_threshold,
        "long_threshold": spec.variant.long_threshold,
        "min_margin": 0.0,
        "max_hold_bars": spec.variant.max_hold_bars,
        "close_on_flat_signal": spec.variant.close_on_flat_signal,
        "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
        "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
        "side_filter_status": "enabled" if correction["gate_column"] in feature_order else "disabled_gate_removed",
        "side_filter_feature_index": correction["gate_feature_index"] if correction["gate_column"] in feature_order else "",
        "known_difference": "score table is supervised retrain over true internal feature order; MT5 execution not yet run; no candidate selection",
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }
    correction_row = {
        "queue_id": queue_id,
        "candidate_alias": spec.alias,
        "test_id": test_id,
        "run267V_schema_hash": correction["target_feature_order_hash"],
        "run267W_actual_hash": correction["actual_feature_order_hash"],
        "target_hash_status": correction["target_hash_status"],
        "correction_reason": correction["correction_reason"],
        "removed_columns_actual": correction["removed_columns_actual"],
        "feature_count_actual": len(feature_order),
    }
    parity_row = {
        "queue_id": queue_id,
        "candidate_alias": spec.alias,
        "test_id": test_id,
        "passed": parity["passed"],
        "max_abs_diff": parity["max_abs_diff"],
        "tolerance": parity["tolerance"],
        "rows": parity["rows"],
        "table_path": rel(model_path),
    }
    return {
        "variant": manifest,
        "runtime_contract": contract,
        "training_diagnostics": training_rows,
        "validation": validation_rows,
        "term_importance": importance_rows,
        "parity": parity_row,
        "surface_alignment": alignment,
        "schema_correction": correction_row,
        "attempts": attempts,
        "ebm_spec": ebm_spec.payload(),
        "feature_path": feature_path,
        "model_path": model_path,
    }


def build_receipts(source_info: Mapping[str, Any], result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    experiment = [
        {
            "field": "hypothesis",
            "value": "true_internal_feature_order_ablation_can_restore_candidate_distinguishability_after_proxy_signature_collapse",
        },
        {"field": "decision_use", "value": "materialize_MT5_attempt_inputs_only_no_candidate_selection"},
        {"field": "comparison_baseline", "value": "run267N_proxy_adapter_variants_and_run267T_signature_collapse"},
        {"field": "control_variables", "value": "US100;M5;label_v1;split_v1;Tier_A_training;2024_historical_stress_runtime_window"},
        {"field": "changed_variables", "value": "feature_order;removed_feature_family;supervised_EBM_score_table_hash"},
        {"field": "sample_scope", "value": f"train/validation/OOS rows from label surface; runtime 2024 rows={result['runtime_2024_rows_per_variant']}"},
        {"field": "success_criteria", "value": "24 score tables built with parity pass and runtime feature hashes"},
        {"field": "failure_criteria", "value": "missing raw feature, parity failure, time-axis mismatch, or no feature-order hash change for direct probes"},
        {"field": "invalid_conditions", "value": "2024 MT5 profit used as training target or label/split boundary changed"},
        {"field": "stop_conditions", "value": "do_not_execute_MT5_if_any_model_or_feature_contract_missing"},
        {"field": "evidence_plan", "value": "variant_manifest;runtime_contract;score_table_parity;surface_alignment;attempt_manifest;ledger_rows"},
    ]
    integrity = [
        {"field": "data_source", "value": f"Stage56 Tier A label surface rows={source_info['rows']}; run267V upstream 2024 surfaces"},
        {"field": "time_axis", "value": "UTC timestamp for training; bar_time_server string for MT5 runtime 2024 feature CSV"},
        {"field": "sample_scope", "value": "US100 M5 Tier A; train 2022-09-01 to 2024-12-31; validation/OOS retained for offline sanity"},
        {"field": "missing_or_duplicate_check", "value": f"duplicates={source_info['duplicates']};missing_labels={source_info['missing_label_rows']};alignment_rows={result['surface_alignment_rows']}"},
        {"field": "feature_label_boundary", "value": "uses label_v1_fwd12 split_v1 only; no MT5 PnL or weak-month outcome is a training label"},
        {"field": "split_boundary", "value": "train/validation/OOS split_v1 preserved; 2024 runtime is train-era historical stress output"},
        {"field": "leakage_risk", "value": "selection bias remains because variants were chosen after earlier Stage267 reviews; MT5 execution still required"},
        {"field": "data_hash_or_identity", "value": f"variant_manifest_path={rel(VARIANT_MANIFEST_PATH)}"},
        {"field": "integrity_judgment", "value": "usable_with_boundary"},
    ]
    return experiment, integrity


def build_materialization() -> dict[str, Any]:
    require_inputs()
    queue_rows = sorted(read_csv(INPUT_QUEUE_PATH), key=lambda row: as_int(row.get("queue_order")))
    schema_rows = sorted(read_csv(INPUT_SCHEMA_PATH), key=lambda row: as_int(row.get("schema_order")))
    if len(queue_rows) != len(schema_rows):
        raise RuntimeError(f"queue/schema row mismatch: {len(queue_rows)} != {len(schema_rows)}")
    schema_by_source = rows_by_key(schema_rows, "source_queue_id")
    schema_by_pair = rows_by_candidate_test(schema_rows)
    specs = specs_by_alias()
    source, source_info = source_retrain.source_frame()
    candidate_frames: dict[str, pd.DataFrame] = {}
    candidate_diagnostics: list[dict[str, Any]] = []
    for alias, spec in specs.items():
        frame, diagnostics = candidate_training_frame(source, spec)
        candidate_frames[alias] = frame
        candidate_diagnostics.append(diagnostics)

    variant_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    training_rows: list[dict[str, Any]] = []
    validation_rows: list[dict[str, Any]] = []
    importance_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    alignment_rows: list[dict[str, Any]] = []
    correction_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    ebm_specs: list[dict[str, Any]] = []
    dynamic_artifacts: list[dict[str, Any]] = []

    for index, queue_row in enumerate(queue_rows, start=1):
        queue_id = str(queue_row["queue_id"])
        schema_row = schema_by_source.get(queue_id) or schema_by_pair.get(
            (str(queue_row.get("candidate_alias", "")), str(queue_row.get("test_id", "")))
        )
        if not schema_row:
            raise KeyError(f"missing schema row for {queue_id}")
        alias = str(queue_row["candidate_alias"])
        spec = specs[alias]
        item = fit_variant(schema_row, queue_row, spec, candidate_frames[alias], source_info, index)
        variant_rows.append(item["variant"])
        contract_rows.append(item["runtime_contract"])
        training_rows.extend(item["training_diagnostics"])
        validation_rows.extend(item["validation"])
        importance_rows.extend(item["term_importance"])
        parity_rows.append(item["parity"])
        alignment_rows.append(item["surface_alignment"])
        correction_rows.append(item["schema_correction"])
        attempts.extend(item["attempts"])
        ebm_specs.append({"queue_id": queue_id, "ebm_spec": item["ebm_spec"]})
        dynamic_artifacts.extend(
            [
                {
                    "artifact_id": f"stage267_run267W_{safe_token(queue_id, 64)}_runtime_feature",
                    "artifact_type": "runtime_feature_csv",
                    "path": rel(item["feature_path"]),
                    "notes": f"Run267W runtime feature CSV for {queue_id}.",
                },
                {
                    "artifact_id": f"stage267_run267W_{safe_token(queue_id, 64)}_runtime_model",
                    "artifact_type": "runtime_model_csv",
                    "path": rel(item["model_path"]),
                    "notes": f"Run267W EBM score table CSV for {queue_id}.",
                },
            ]
        )

    created_at = utc_now()
    artifact_hashes = {
        "variant_manifest": "",
        "runtime_contract": "",
        "training_diagnostics": "",
        "model_validation": "",
        "score_table_parity": "",
        "term_importance": "",
        "surface_alignment": "",
        "schema_correction": "",
        "attempt_manifest": "",
        "run_manifest": "",
        "lineage": "",
        "result": "",
    }
    result = {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "candidate_count": len({row["candidate_alias"] for row in variant_rows}),
        "variant_count": len(variant_rows),
        "attempt_count": len(attempts),
        "training_rows": int(source_info["rows"]),
        "runtime_2024_rows_per_variant": int(alignment_rows[0]["runtime_rows"]) if alignment_rows else 0,
        "parity_passed_count": sum(1 for row in parity_rows if str(row["passed"]).lower() == "true" or row["passed"] is True),
        "surface_alignment_pass_count": sum(1 for row in alignment_rows if row["alignment_status"] == "pass"),
        "surface_alignment_rows": len(alignment_rows),
        "schema_correction_rows": sum(1 for row in correction_rows if row["target_hash_status"] != "matches_run267V_schema"),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_info": source_info,
        "candidate_diagnostics": candidate_diagnostics,
        "variant_manifest": variant_rows,
        "runtime_contract": contract_rows,
        "training_diagnostics": training_rows,
        "model_validation": validation_rows,
        "term_importance": importance_rows,
        "score_table_parity": parity_rows,
        "surface_alignment": alignment_rows,
        "schema_correction": correction_rows,
        "attempts": attempts,
        "ebm_specs": ebm_specs,
        "dynamic_artifacts": dynamic_artifacts,
        "inputs": {
            "run267W_queue": rel(INPUT_QUEUE_PATH),
            "run267V_schema": rel(INPUT_SCHEMA_PATH),
            "run267V_surface_manifest": rel(INPUT_SURFACE_MANIFEST_PATH),
            "run267V_report": rel(RUN267V_REPORT_PATH),
            "model_input_dataset": rel(MODEL_INPUT_DATASET_PATH),
            "training_contract": rel(TRAINING_CONTRACT_PATH),
            "model_input_contract": rel(MODEL_INPUT_CONTRACT_PATH),
        },
        "outputs": {
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "training_diagnostics": rel(TRAINING_DIAGNOSTICS_PATH),
            "model_validation": rel(MODEL_VALIDATION_PATH),
            "score_table_parity": rel(PARITY_CHECK_PATH),
            "term_importance": rel(TERM_IMPORTANCE_PATH),
            "surface_alignment": rel(SURFACE_ALIGNMENT_PATH),
            "schema_correction": rel(SCHEMA_CORRECTION_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": artifact_hashes,
    }
    experiment, integrity = build_receipts(source_info, result)
    result["experiment_design_receipt"] = experiment
    result["data_integrity_receipt"] = integrity
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        VARIANT_MANIFEST_PATH,
        result["variant_manifest"],
        (
            "queue_id",
            "source_schema_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "feature_family",
            "queue_lane",
            "model_family",
            "model_materialization_type",
            "source_model_file",
            "input_surface_file",
            "runtime_feature_file",
            "runtime_feature_sha256",
            "runtime_model_file",
            "runtime_model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "removed_columns_actual",
            "removed_column_count_actual",
            "target_feature_order_hash",
            "target_hash_status",
            "gate_feature_index",
            "rank_feature_index",
            "train_rows",
            "source_rows",
            "runtime_rows",
            "parity_passed",
            "parity_max_abs_diff",
            "top8_gain_share",
            "top8_terms",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        result["runtime_contract"],
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
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "side_filter_status",
            "side_filter_feature_index",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        TRAINING_DIAGNOSTICS_PATH,
        result["training_diagnostics"],
        ("queue_id", "candidate_alias", "test_id", "split", "rows", "class_counts", "missing_feature_cells"),
    )
    write_csv(
        MODEL_VALIDATION_PATH,
        result["model_validation"],
        (
            "queue_id",
            "candidate_alias",
            "test_id",
            "split",
            "rows",
            "accuracy",
            "balanced_accuracy",
            "log_loss",
            "short_threshold",
            "long_threshold",
            "short_threshold_decisions",
            "long_threshold_decisions",
            "flat_or_no_trade_decisions",
            "selection_metric",
            "validation_judgment",
        ),
    )
    write_csv(
        TERM_IMPORTANCE_PATH,
        result["term_importance"],
        (
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "test_id",
            "feature_family",
            "term_index",
            "term_name",
            "feature",
            "term_degree",
            "importance",
            "gain",
            "gain_share",
            "score_abs_max",
            "score_std",
            "short_range",
            "flat_range",
            "long_range",
        ),
    )
    write_csv(PARITY_CHECK_PATH, result["score_table_parity"], ("queue_id", "candidate_alias", "test_id", "passed", "max_abs_diff", "tolerance", "rows", "table_path"))
    write_csv(
        SURFACE_ALIGNMENT_PATH,
        result["surface_alignment"],
        (
            "queue_id",
            "candidate_alias",
            "test_id",
            "runtime_rows",
            "training_2024_rows",
            "bar_time_order_match",
            "duplicate_bar_time_rows",
            "runtime_missing_feature_cells",
            "missing_runtime_columns",
            "alignment_status",
        ),
    )
    write_csv(
        SCHEMA_CORRECTION_PATH,
        result["schema_correction"],
        (
            "queue_id",
            "candidate_alias",
            "test_id",
            "run267V_schema_hash",
            "run267W_actual_hash",
            "target_hash_status",
            "correction_reason",
            "removed_columns_actual",
            "feature_count_actual",
        ),
    )
    attempt_rows = []
    for attempt in result["attempts"]:
        attempt_rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "queue_id": attempt["queue_id"],
                "candidate_id": attempt["candidate_id"],
                "candidate_alias": attempt["candidate_alias"],
                "candidate_role": attempt["candidate_role"],
                "test_id": attempt["test_id"],
                "tier": attempt["tier"],
                "attempt_role": attempt["attempt_role"],
                "set_path": attempt["set"]["path"],
                "set_sha256": attempt["set"]["sha256"],
                "ini_path": attempt["ini"]["path"],
                "ini_sha256": attempt["ini"]["sha256"],
                "execution_status": attempt["execution_status"],
            }
        )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows,
        (
            "attempt_name",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "tier",
            "attempt_role",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "execution_status",
        ),
    )
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("field", "value"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("field", "value"))
    run_manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "variant_manifest": rel(VARIANT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "attempts": result["attempts"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    lineage = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": result["inputs"],
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": result["outputs"],
        "registry_links": {
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            "run_registry": rel(RUN_REGISTRY_PATH),
            "alpha_run_ledger": rel(PROJECT_LEDGER_PATH),
            "stage_run_ledger": rel(STAGE_LEDGER_PATH),
        },
        "availability": "tracked_generated_with_manifest_and_common_file_copies",
        "lineage_judgment": "connected_with_boundary",
        "boundary": CLAIM_BOUNDARY,
    }
    write_json(LINEAGE_PATH, lineage)
    artifact_hashes = {
        "variant_manifest": sha256_file_lf_normalized(VARIANT_MANIFEST_PATH),
        "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
        "training_diagnostics": sha256_file_lf_normalized(TRAINING_DIAGNOSTICS_PATH),
        "model_validation": sha256_file_lf_normalized(MODEL_VALIDATION_PATH),
        "score_table_parity": sha256_file_lf_normalized(PARITY_CHECK_PATH),
        "term_importance": sha256_file_lf_normalized(TERM_IMPORTANCE_PATH),
        "surface_alignment": sha256_file_lf_normalized(SURFACE_ALIGNMENT_PATH),
        "schema_correction": sha256_file_lf_normalized(SCHEMA_CORRECTION_PATH),
        "experiment_design_receipt": sha256_file_lf_normalized(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "data_integrity_receipt": sha256_file_lf_normalized(DATA_INTEGRITY_RECEIPT_PATH),
        "attempt_manifest": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
        "run_manifest": sha256_file_lf_normalized(RUN_MANIFEST_PATH),
        "lineage": sha256_file_lf_normalized(LINEAGE_PATH),
    }
    result_with_hashes = dict(result)
    result_with_hashes["artifact_hashes"] = artifact_hashes
    write_json(RESULT_PATH, result_with_hashes)
    write_md(REPORT_PATH, report_markdown(result_with_hashes))


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267W True Internal Ablation Score Table Materialization(267단계 267W 진짜 내부 제거 점수표 물질화)",
        "",
        "- action(행동): run267V(267V 실행)의 raw feature surface(원시 피처 표면)에서 24개 feature order(피처 순서)를 만들고 supervised EBM(지도학습 EBM) score table(점수표)을 재학습했다.",
        "- effect(효과): 다음 MT5(MetaTrader 5, 메타트레이더5) 실행은 proxy score extension(대체 점수 확장)이 아니라 실제 내부 feature removal/replacement(피처 제거/대체) 표면을 쓴다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267W(267W 실행)는 24개 후보-시험 조합을 모두 새 score table(점수표)로 만들었다. 2024년 결과를 정답으로 쓰지 않았고, label_v1/split_v1(라벨 v1/분할 v1) 학습 표면만 썼다.",
        "효과(effect, 효과)는 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음 실행)에서 후보가 진짜로 특정 feature family(피처 계열)를 잃어도 버티는지 볼 수 있게 된 것이다.",
        "",
        "## Materialization Summary(물질화 요약)",
        "",
        f"- candidates(후보): `{result['candidate_count']}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- attempts queued(대기 시도): `{result['attempt_count']}`",
        f"- training rows(학습 표면 행): `{result['training_rows']}`",
        f"- runtime rows per variant(변형별 런타임 행): `{result['runtime_2024_rows_per_variant']}`",
        f"- parity passed(동등성 통과): `{result['parity_passed_count']}/{result['variant_count']}`",
        f"- surface alignment passed(표면 정렬 통과): `{result['surface_alignment_pass_count']}/{result['surface_alignment_rows']}`",
        f"- corrected direct compressed rows(직접 압축 행 보정): `{result['schema_correction_rows']}`",
        "",
        "## Boundary(경계)",
        "",
        "- MT5 execution(MT5 실행): `not_executed`",
        "- trading KPI(거래 핵심 성과 지표): `not_claimed`",
        "- balance/equity curve(잔액/평가금 곡선): `pending_MT5`",
        "- time-slice KPI(시간 구간 핵심 성과 지표): `pending_MT5`",
        "- candidate selection(후보 선정): `none`",
        "",
        "## Outputs(산출물)",
        "",
        f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
        f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        f"- score_table_parity(점수표 동등성): `{rel(PARITY_CHECK_PATH)}`",
        f"- surface_alignment(표면 정렬): `{rel(SURFACE_ALIGNMENT_PATH)}`",
        f"- schema_correction(스키마 보정): `{rel(SCHEMA_CORRECTION_PATH)}`",
        f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        "- effect(효과): 물질화된 48개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실행해 거래 목록, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)를 확인한다.",
        "",
    ]
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    static = [
        ("stage267_run267W_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267W true internal ablation score tables."),
        ("stage267_run267W_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267W true internal ablation variant manifest."),
        ("stage267_run267W_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267W runtime contract."),
        ("stage267_run267W_training_diagnostics", "training_frame_diagnostics", TRAINING_DIAGNOSTICS_PATH, "Run267W training diagnostics."),
        ("stage267_run267W_model_validation", "model_validation_snapshot", MODEL_VALIDATION_PATH, "Run267W offline model validation snapshot."),
        ("stage267_run267W_score_table_parity", "score_table_parity_check", PARITY_CHECK_PATH, "Run267W score table parity check."),
        ("stage267_run267W_term_importance", "term_importance", TERM_IMPORTANCE_PATH, "Run267W term importance."),
        ("stage267_run267W_surface_alignment", "surface_alignment_check", SURFACE_ALIGNMENT_PATH, "Run267W runtime surface alignment check."),
        ("stage267_run267W_schema_correction", "schema_correction_audit", SCHEMA_CORRECTION_PATH, "Run267W correction audit for direct compressed rows."),
        ("stage267_run267W_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267W experiment design receipt."),
        ("stage267_run267W_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267W data integrity receipt."),
        ("stage267_run267W_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267W MT5 attempt manifest."),
        ("stage267_run267W_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267W run manifest."),
        ("stage267_run267W_lineage", "lineage", LINEAGE_PATH, "Run267W lineage."),
        ("stage267_run267W_result", "result_json", RESULT_PATH, "Run267W result JSON."),
        ("stage267_run267W_report", "review_report", REPORT_PATH, "Run267W review report."),
    ]
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in static
    ]
    for item in result["dynamic_artifacts"]:
        path = repo_path(str(item["path"]))
        rows.append(
            {
                "artifact_id": item["artifact_id"],
                "artifact_type": item["artifact_type"],
                "path": item["path"],
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": item["notes"],
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "true_internal_ablation_score_table_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT),
        "notes": (
            f"variants={result['variant_count']};attempts={result['attempt_count']};"
            f"parity_passed={result['parity_passed_count']};selected_candidate=none;"
            f"onnx_readiness=not_claimed;goal_achieve=not_claimed;next_action={NEXT_ACTION}."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__true_internal_ablation_score_table_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "true_internal_ablation_score_table_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "true_internal_ablation_score_table_materialization",
        "tier_scope": "Tier A training plus 2024 historical runtime feature surface",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "experiment_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};parity_passed={result['parity_passed_count']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;mt5_execution=not_executed",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    stage_row = {
        "row_id": "stage267_run267W_true_internal_ablation_score_table_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "true_internal_ablation_score_table_materialization",
        "tier_scope": "Tier A label surface and 2024 historical runtime surface",
        "scoreboard": "feature_model_set_ini_manifest",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "score_table_materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};next_action={NEXT_ACTION}.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def update_docs() -> None:
    report_line = f"- Stage267(267단계) run267W true internal ablation score table materialization(진짜 내부 제거 점수표 물질화): `{rel(REPORT_PATH)}`"
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `true_internal_ablation_score_table_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(current, "run267V_reconstruct_upstream_feature_surface", report_line)
    current = append_block_once(
        current,
        "Run267W(267W 실행)는 run267V",
        "\n".join(
            [
                "Run267W(267W 실행)는 run267V(267V 실행)의 raw feature surface(원시 피처 표면)를 받아 24개 supervised EBM(지도학습 EBM) score table(점수표)을 물질화했다.",
                "Effect(효과): 다음 run267X(267X 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 진짜 내부 feature ablation/replacement(피처 제거/대체)를 검증할 수 있다.",
            ]
        ),
    )
    current = current.replace("`run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces`", f"`{NEXT_ACTION}`")
    current = current.replace(
        "- next_run(다음 실행): `run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    current = current.replace(
        "- next_action(다음 행동): `run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(selection, "run267V_reconstruct_upstream_feature_surface", report_line)
    selection = selection.replace(
        "- next_action(다음 행동): `run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = append_after_contains(review, "run267V_reconstruct_upstream_feature_surface", report_line)
    write_text(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus_block = (
        "- >-\n"
        "  Stage267(267단계) run267W(267W 실행) true internal ablation score table materialization(진짜 내부 제거 점수표 물질화) "
        f"`{STATUS}`. Effect(효과): run267V(267V 실행)의 raw feature surface(원시 피처 표면)에 맞춰 24개 score table/model(점수표/모델)과 48개 MT5(MetaTrader 5, 메타트레이더5) 시도 입력을 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = workspace.replace("current_run_id: run267V_stage267_reconstruct_upstream_feature_surface_v1", f"current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace("status: run267V_upstream_feature_surface_reconstructed", f"status: {STATUS}", 1)
    workspace = workspace.replace("current_run_id: run267V_stage267_reconstruct_upstream_feature_surface_v1", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace("last_completed_run_id: run267V_stage267_reconstruct_upstream_feature_surface_v1", f"last_completed_run_id: {RUN_ID}")
    workspace = workspace.replace("status: run267V_upstream_feature_surface_reconstructed", f"status: {STATUS}")
    workspace = workspace.replace(
        "next_action: run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces",
        f"next_action: {NEXT_ACTION}",
    )
    insert = f"  run267W_true_internal_ablation_score_table_materialization_report_path: {rel(REPORT_PATH)}"
    workspace = append_after_contains(workspace, "run267V_reconstruct_upstream_feature_surface_report_path", insert)
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces`이다. Effect(효과): 재구축된 raw feature surface(원시 피처 표면)에 맞는 score table/model(점수표/모델)을 만든다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): 물질화된 score table/model(점수표/모델)을 MT5(MetaTrader 5, 메타트레이더5)로 실행해 거래/곡선/시간구간을 확인한다.",
    )
    write_text(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_materialization()
    write_outputs(result)
    final_result = read_json(RESULT_PATH)
    update_ledgers(final_result)
    update_docs()
    print(
        json.dumps(
            {
                "status": STATUS,
                "variant_count": final_result["variant_count"],
                "attempt_count": final_result["attempt_count"],
                "parity_passed_count": final_result["parity_passed_count"],
                "surface_alignment_pass_count": final_result["surface_alignment_pass_count"],
                "schema_correction_rows": final_result["schema_correction_rows"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
