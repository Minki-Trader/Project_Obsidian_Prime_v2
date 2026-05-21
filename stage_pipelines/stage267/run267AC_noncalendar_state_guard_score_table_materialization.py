from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
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
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
)
from foundation.models.ebm_score_table import (
    load_ebm_score_table,
    score_ebm_table_probabilities,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267AB_noncalendar_weak_slice_resilience_queue as source_queue
from stage_pipelines.stage267 import run267W_true_internal_ablation_score_table_materialization as source_tables


STAGE_ID = input_probe.STAGE_ID
RUN_NUMBER = "run267AC"
RUN_ID = "run267AC_stage267_noncalendar_state_guard_score_table_materialization_v1"
PARENT_RUN_ID = source_queue.RUN_ID
SOURCE_SCORE_TABLE_RUN_ID = source_tables.RUN_ID
STATUS = "run267AC_noncalendar_state_guard_score_tables_materialized_execution_pending"
JUDGMENT = "state_guard_score_tables_materialized_execution_pending_no_candidate_selection"
NEXT_ACTION = "run267AD_execute_noncalendar_state_guard_score_table_mt5_batch"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_score_table_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_QUEUE_PATH = source_queue.GUARD_MATERIALIZATION_QUEUE_PATH
SOURCE_REPEATED_STATE_PATH = source_queue.REPEATED_STATE_SUMMARY_PATH
SOURCE_STATE_CONTRAST_PATH = source_queue.WEAK_SLICE_STATE_CONTRAST_PATH
SOURCE_QUEUE_REPORT_PATH = source_queue.REPORT_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_tables.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_tables.RUNTIME_CONTRACT_PATH
SOURCE_SCORE_TABLE_REPORT_PATH = source_tables.REPORT_PATH

VARIANT_MANIFEST_PATH = RUN_ROOT / "noncalendar_state_guard_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
GUARD_DIAGNOSTICS_PATH = RUN_ROOT / "guard_state_diagnostics.csv"
PARITY_CHECK_PATH = RUN_ROOT / "neutral_guard_score_parity_check.csv"
SURFACE_ALIGNMENT_PATH = RUN_ROOT / "surface_alignment_check.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempts.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AC_noncalendar_state_guard_score_table_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AC_noncalendar_state_guard_score_table_materialization.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267ac/run267AC_noncalendar_state_guard"
PERIOD_LABEL = input_probe.PERIOD_LABEL
MODEL_MATERIALIZATION_TYPE = "research_score_table_noncalendar_state_guard_extension_not_retrained_v1"
GUARD_SCORE_FEATURE = "stage267_noncalendar_guard_score"
GUARD_SCORE_CUTS = (0.25, 0.50, 0.75)
GUARD_SCORE_TERMS = (
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0),
    (-0.025, 0.05, -0.025),
    (-0.05, 0.10, -0.05),
    (-0.075, 0.15, -0.075),
)
CSV_MODEL_COLUMNS = ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long")

STAGE_LEDGER_COLUMNS = source_tables.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_tables.ARTIFACT_COLUMNS


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    item = Path(path_text)
    return item if item.is_absolute() else REPO_ROOT / item


def safe_token(value: str, limit: int = 80) -> str:
    import re

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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def require_inputs() -> None:
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_REPEATED_STATE_PATH,
        SOURCE_STATE_CONTRAST_PATH,
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def source_variants_by_pair() -> dict[tuple[str, str], dict[str, str]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    return {
        (str(row.get("candidate_alias", "")), str(row.get("test_id", ""))): dict(row)
        for row in rows
        if row.get("candidate_alias") and row.get("test_id")
    }


def parse_guard_states(value: str) -> list[tuple[str, str]]:
    states: list[tuple[str, str]] = []
    for part in str(value or "").split(";"):
        if not part.strip() or "=" not in part:
            continue
        feature, bucket = part.split("=", 1)
        states.append((feature.strip(), bucket.strip()))
    return states


def threshold_map(surface: pd.DataFrame, guard_states: Sequence[tuple[str, str]]) -> dict[str, tuple[float, float]]:
    thresholds: dict[str, tuple[float, float]] = {}
    for feature, _bucket in guard_states:
        if feature in thresholds:
            continue
        if feature.startswith("abs_"):
            source = feature[4:]
            if source not in surface.columns:
                raise KeyError(f"missing raw guard source column: {source}")
            series = pd.to_numeric(surface[source], errors="coerce").abs()
        else:
            if feature not in surface.columns:
                raise KeyError(f"missing raw guard source column: {feature}")
            series = pd.to_numeric(surface[feature], errors="coerce")
        thresholds[feature] = (float(series.quantile(0.25)), float(series.quantile(0.75)))
    return thresholds


def state_bucket(row: Mapping[str, Any], feature: str, thresholds: Mapping[str, tuple[float, float]]) -> str:
    if feature.startswith("abs_"):
        value = abs(as_float(row.get(feature[4:]), float("nan")))
    else:
        value = as_float(row.get(feature), float("nan"))
    if not math.isfinite(value):
        return "missing"
    q1, q3 = thresholds[feature]
    if value <= q1:
        return "low"
    if value >= q3:
        return "high"
    return "mid"


def guard_score_for_raw_row(
    raw_row: Mapping[str, Any] | None,
    guard_states: Sequence[tuple[str, str]],
    thresholds: Mapping[str, tuple[float, float]],
) -> tuple[float, list[str]]:
    if raw_row is None or not guard_states:
        return 0.0, []
    matched: list[str] = []
    for feature, bucket in guard_states:
        actual = state_bucket(raw_row, feature, thresholds)
        if actual == bucket:
            matched.append(f"{feature}={bucket}")
    return len(matched) / len(guard_states), matched


def copy_and_extend_score_table(source: Path, destination: Path, guard_feature_index: int) -> dict[str, Any]:
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    with io_path(destination).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_MODEL_COLUMNS), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in source_rows:
            writer.writerow({column: row.get(column, "") for column in CSV_MODEL_COLUMNS})
        for index, cut in enumerate(GUARD_SCORE_CUTS):
            writer.writerow(
                {
                    "record_type": "cut",
                    "feature_index": guard_feature_index,
                    "item_index": index,
                    "value": f"{cut:.17g}",
                    "score_short": "",
                    "score_flat": "",
                    "score_long": "",
                }
            )
        for index, scores in enumerate(GUARD_SCORE_TERMS):
            writer.writerow(
                {
                    "record_type": "score",
                    "feature_index": guard_feature_index,
                    "item_index": index,
                    "value": "",
                    "score_short": f"{scores[0]:.17g}",
                    "score_flat": f"{scores[1]:.17g}",
                    "score_long": f"{scores[2]:.17g}",
                }
            )
    return {
        "source_model_rows": len(source_rows),
        "added_cut_rows": len(GUARD_SCORE_CUTS),
        "added_score_rows": len(GUARD_SCORE_TERMS),
        "runtime_model_file": rel(destination),
        "runtime_model_sha256": sha256_file_lf_normalized(destination),
        "guard_score_cuts": ";".join(f"{value:.2f}" for value in GUARD_SCORE_CUTS),
        "guard_score_terms": ";".join("/".join(f"{score:.3f}" for score in row) for row in GUARD_SCORE_TERMS),
    }


def neutral_parity_row(
    queue_id: str,
    candidate_alias: str,
    test_id: str,
    source_model: Path,
    extended_model: Path,
    source_features: pd.DataFrame,
    source_feature_order: Sequence[str],
    extended_feature_order: Sequence[str],
) -> dict[str, Any]:
    rows = min(2048, len(source_features))
    source_matrix = source_features.loc[: rows - 1, list(source_feature_order)].to_numpy(dtype="float64")
    extended_matrix = np.column_stack([source_matrix, np.zeros(rows, dtype="float64")])
    source_table = load_ebm_score_table(source_model, feature_count=len(source_feature_order))
    extended_table = load_ebm_score_table(extended_model, feature_count=len(extended_feature_order))
    source_prob = score_ebm_table_probabilities(source_table, source_matrix)
    extended_prob = score_ebm_table_probabilities(extended_table, extended_matrix)
    max_abs_diff = float(np.max(np.abs(source_prob - extended_prob))) if rows else 0.0
    tolerance = 1.0e-10
    return {
        "queue_id": queue_id,
        "candidate_alias": candidate_alias,
        "test_id": test_id,
        "passed": max_abs_diff <= tolerance,
        "max_abs_diff": max_abs_diff,
        "tolerance": tolerance,
        "rows": rows,
        "source_feature_count": len(source_feature_order),
        "extended_feature_count": len(extended_feature_order),
        "guard_zero_policy": "guard_score_zero_must_equal_source_score_table",
        "table_path": rel(extended_model),
    }


def transform_runtime_feature(
    queue_row: Mapping[str, str],
    source_variant: Mapping[str, str],
    destination: Path,
) -> tuple[dict[str, Any], pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    source_feature_path = repo_path(str(source_variant["runtime_feature_file"]))
    raw_surface_path = repo_path(str(source_variant["input_surface_file"]))
    feature_frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    raw_surface = pd.read_csv(io_path(raw_surface_path), encoding="utf-8-sig")
    guard_states = parse_guard_states(str(queue_row.get("guard_state_features", "")))
    thresholds = threshold_map(raw_surface, guard_states)
    raw_by_time = {str(row["bar_time_server"]): row for row in raw_surface.to_dict("records")}
    source_columns = list(feature_frame.columns)
    source_feature_order = source_columns[1:]
    extended_feature_order = [*source_feature_order, GUARD_SCORE_FEATURE]

    rows: list[dict[str, Any]] = []
    scores: list[float] = []
    signal_scores: list[float] = []
    context_missing_rows = 0
    signal_rows = 0
    high_guard_signal_rows = 0
    state_match_counts = {f"{feature}={bucket}": 0 for feature, bucket in guard_states}
    state_signal_match_counts = {key: 0 for key in state_match_counts}

    for row in feature_frame.to_dict("records"):
        current = dict(row)
        raw_row = raw_by_time.get(str(row.get("bar_time_server", "")))
        if raw_row is None:
            context_missing_rows += 1
        score, matched = guard_score_for_raw_row(raw_row, guard_states, thresholds)
        for key in matched:
            state_match_counts[key] = state_match_counts.get(key, 0) + 1
        current[GUARD_SCORE_FEATURE] = score
        scores.append(score)
        signal = int(round(as_float(row.get(source_tables.SOURCE_SIGNAL_COLUMN), 0.0)))
        if signal != 0:
            signal_rows += 1
            signal_scores.append(score)
            if score >= 2.0 / 3.0:
                high_guard_signal_rows += 1
            for key in matched:
                state_signal_match_counts[key] = state_signal_match_counts.get(key, 0) + 1
        rows.append(current)

    write_runtime_csv(destination, rows, ("bar_time_server", *extended_feature_order))
    raw_times = list(raw_surface["bar_time_server"].astype(str))
    feature_times = list(feature_frame["bar_time_server"].astype(str))
    state_rows = []
    for feature, bucket in guard_states:
        key = f"{feature}={bucket}"
        q1, q3 = thresholds[feature]
        state_rows.append(
            {
                "queue_id": queue_row.get("queue_id"),
                "candidate_alias": queue_row.get("candidate_alias"),
                "test_id": queue_row.get("source_test_id"),
                "guard_state": key,
                "q25": q1,
                "q75": q3,
                "matched_rows": state_match_counts.get(key, 0),
                "matched_signal_rows": state_signal_match_counts.get(key, 0),
                "state_source": "run267V_2024_raw_surface_quantile_q25_q75",
            }
        )
    diagnostics = {
        "source_feature_file": rel(source_feature_path),
        "raw_surface_file": rel(raw_surface_path),
        "runtime_feature_file": rel(destination),
        "runtime_feature_sha256": sha256_file_lf_normalized(destination),
        "rows": int(len(rows)),
        "source_feature_count": len(source_feature_order),
        "extended_feature_count": len(extended_feature_order),
        "source_feature_order_hash": ordered_hash(source_feature_order),
        "feature_order": ";".join(extended_feature_order),
        "feature_order_hash": ordered_hash(extended_feature_order),
        "guard_score_feature": GUARD_SCORE_FEATURE,
        "guard_score_feature_index": len(extended_feature_order) - 1,
        "guard_state_count": len(guard_states),
        "guard_state_features": ";".join(f"{feature}={bucket}" for feature, bucket in guard_states),
        "guard_score_q50": float(pd.Series(scores, dtype="float64").quantile(0.50)) if scores else 0.0,
        "guard_score_q80": float(pd.Series(scores, dtype="float64").quantile(0.80)) if scores else 0.0,
        "guard_score_q95": float(pd.Series(scores, dtype="float64").quantile(0.95)) if scores else 0.0,
        "signal_rows": signal_rows,
        "signal_guard_score_q80": float(pd.Series(signal_scores, dtype="float64").quantile(0.80)) if signal_scores else 0.0,
        "high_guard_signal_rows": high_guard_signal_rows,
        "high_guard_signal_ratio": high_guard_signal_rows / signal_rows if signal_rows else 0.0,
        "context_missing_rows": context_missing_rows,
        "bar_time_order_match": raw_times == feature_times,
        "duplicate_bar_time_rows": int(feature_frame["bar_time_server"].duplicated().sum()),
        "runtime_missing_feature_cells": int(pd.DataFrame(rows).loc[:, extended_feature_order].isna().sum().sum()) if rows else 0,
    }
    return diagnostics, feature_frame, state_rows, {"source_feature_order": source_feature_order, "extended_feature_order": extended_feature_order}


def materialize_variant(
    queue_row: Mapping[str, str],
    source_variant: Mapping[str, str],
    spec: Any,
    index: int,
) -> dict[str, Any]:
    queue_id = str(queue_row["queue_id"])
    alias = str(queue_row["candidate_alias"])
    test_id = str(queue_row["source_test_id"])
    queue_token = safe_token(queue_id, 72)
    test_token = safe_token(test_id, 48)
    local_root = VARIANT_ROOT / alias / queue_token
    feature_path = local_root / "features" / f"{alias}_{test_token}_state_guard.csv"
    model_path = local_root / "models" / f"{alias}_{test_token}_state_guard_model.csv"

    feature_meta, source_feature_frame, state_rows, order_meta = transform_runtime_feature(queue_row, source_variant, feature_path)
    source_feature_order = list(order_meta["source_feature_order"])
    extended_feature_order = list(order_meta["extended_feature_order"])
    source_model_path = repo_path(str(source_variant["runtime_model_file"]))
    model_meta = copy_and_extend_score_table(source_model_path, model_path, int(feature_meta["guard_score_feature_index"]))
    parity = neutral_parity_row(
        queue_id,
        alias,
        test_id,
        source_model_path,
        model_path,
        source_feature_frame,
        source_feature_order,
        extended_feature_order,
    )

    common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    _full_order, _rank_column, gate_column = source_tables.candidate_full_feature_order(spec)
    attempts: list[dict[str, Any]] = []
    for role_index, (tier, attempt_role, prefix, token) in enumerate(
        (
            (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{safe_token(test_id, 28)}_state_guard", "ta"),
            (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_{safe_token(test_id, 28)}_state_guard", "rt"),
        ),
        start=1,
    ):
        magic = 26730000 + index * 100 + role_index
        payload = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=267,
            exploration_label=f"stage267_NoncalendarStateGuard__{safe_token(test_id, 32)}",
            attempt_name=f"{queue_token}_{token}_2024",
            tier=tier,
            split=PERIOD_LABEL,
            model_path=common_model_path,
            model_id=f"{RUN_ID}_{alias}_{safe_token(test_id, 36)}_state_guard_v1",
            model_backend="ebm_table",
            feature_path=common_feature_path,
            feature_count=len(extended_feature_order),
            feature_order_hash=ordered_hash(extended_feature_order),
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
            extra_set_values=source_tables.extra_set_for_feature_order(spec, extended_feature_order, gate_column, magic),
        )
        payload.update(
            {
                "queue_id": queue_id,
                "candidate_id": queue_row.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": queue_row.get("candidate_role"),
                "source_test_id": test_id,
                "guard_rule_family": queue_row.get("guard_rule_family"),
                "guard_state_features": queue_row.get("guard_state_features"),
                "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                "execution_status": "not_executed",
            }
        )
        attempts.append(payload)

    manifest = {
        "queue_id": queue_id,
        "priority": queue_row.get("priority"),
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": test_id,
        "guard_rule_family": queue_row.get("guard_rule_family"),
        "guard_intent": queue_row.get("guard_intent"),
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "source_queue_path": rel(SOURCE_QUEUE_PATH),
        "source_runtime_feature_file": feature_meta["source_feature_file"],
        "runtime_feature_file": feature_meta["runtime_feature_file"],
        "runtime_feature_sha256": feature_meta["runtime_feature_sha256"],
        "source_runtime_model_file": rel(source_model_path),
        "runtime_model_file": model_meta["runtime_model_file"],
        "runtime_model_sha256": model_meta["runtime_model_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "source_feature_count": feature_meta["source_feature_count"],
        "feature_count": feature_meta["extended_feature_count"],
        "source_feature_order_hash": feature_meta["source_feature_order_hash"],
        "feature_order": feature_meta["feature_order"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "guard_score_feature": feature_meta["guard_score_feature"],
        "guard_score_feature_index": feature_meta["guard_score_feature_index"],
        "guard_state_features": feature_meta["guard_state_features"],
        "guard_score_cuts": model_meta["guard_score_cuts"],
        "guard_score_terms": model_meta["guard_score_terms"],
        "runtime_rows": feature_meta["rows"],
        "signal_rows": feature_meta["signal_rows"],
        "high_guard_signal_rows": feature_meta["high_guard_signal_rows"],
        "high_guard_signal_ratio": feature_meta["high_guard_signal_ratio"],
        "neutral_parity_passed": parity["passed"],
        "neutral_parity_max_abs_diff": parity["max_abs_diff"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    contract = {
        "queue_id": queue_id,
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": test_id,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;true_internal_feature_order_plus_noncalendar_guard_score;EBM score table extension;attempt set/ini identity",
        "feature_count": feature_meta["extended_feature_count"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "short_threshold": spec.variant.short_threshold,
        "long_threshold": spec.variant.long_threshold,
        "min_margin": 0.0,
        "max_hold_bars": spec.variant.max_hold_bars,
        "close_on_flat_signal": spec.variant.close_on_flat_signal,
        "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
        "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
        "guard_rule_family": queue_row.get("guard_rule_family"),
        "guard_score_feature_index": feature_meta["guard_score_feature_index"],
        "known_difference": "extends run267W score table with one noncalendar guard score feature; no retraining and no calendar literal filter",
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }
    alignment = {
        "queue_id": queue_id,
        "candidate_alias": alias,
        "source_test_id": test_id,
        "runtime_rows": feature_meta["rows"],
        "raw_surface_rows": int(len(pd.read_csv(io_path(repo_path(str(source_variant["input_surface_file"]))), encoding="utf-8-sig"))),
        "bar_time_order_match": feature_meta["bar_time_order_match"],
        "duplicate_bar_time_rows": feature_meta["duplicate_bar_time_rows"],
        "runtime_missing_feature_cells": feature_meta["runtime_missing_feature_cells"],
        "context_missing_rows": feature_meta["context_missing_rows"],
        "alignment_status": "pass"
        if feature_meta["bar_time_order_match"] and not feature_meta["context_missing_rows"] and not feature_meta["runtime_missing_feature_cells"]
        else "invalid",
    }
    if alignment["alignment_status"] != "pass":
        raise RuntimeError(f"surface alignment failed for {queue_id}: {alignment}")
    return {
        "variant": manifest,
        "contract": contract,
        "diagnostics": state_rows,
        "parity": parity,
        "alignment": alignment,
        "attempts": attempts,
        "feature_path": feature_path,
        "model_path": model_path,
    }


def build_receipts(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    design = [
        {"field": "hypothesis", "value": "run267AB_weak_noncalendar_states_can_be_materialized_as_soft_score_table_guard_without_calendar_literal_filter"},
        {"field": "decision_use", "value": "materialize_MT5_attempt_inputs_only_no_candidate_selection"},
        {"field": "comparison_baseline", "value": "run267W true internal ablation score tables plus run267AB guard queue"},
        {"field": "control_variables", "value": "same_2024_period_same_candidate_pool_same_true_internal_score_table_sources_same_thresholds"},
        {"field": "changed_variables", "value": "adds_one_guard_score_feature_and_small_flat_bias_score_table_terms"},
        {"field": "sample_scope", "value": "Tier A and Tier A+B 2024 historical runtime attempts planned; no new MT5 KPI in materialization"},
        {"field": "success_criteria", "value": f"variants={result['variant_count']};attempts={result['attempt_count']};neutral_parity={result['neutral_parity_passed_count']}/{result['variant_count']};surface_alignment={result['surface_alignment_pass_count']}/{result['variant_count']}"},
        {"field": "failure_criteria", "value": "surface_mismatch_or_neutral_parity_failure_or_trade_supply_collapses_in_next_MT5_execution"},
        {"field": "invalid_conditions", "value": "calendar_literal_filter_or_MT5_PnL_as_training_label_or_selected_candidate_claim"},
        {"field": "stop_conditions", "value": "do_not_extend_this_guard_branch_beyond_two_failed_materialization_execution_review_passes"},
        {"field": "evidence_plan", "value": "variant_manifest;runtime_contract;guard_diagnostics;neutral_parity;surface_alignment;attempt_manifest;future_MT5_trade_review"},
    ]
    integrity = [
        {"field": "data_source", "value": f"{rel(SOURCE_QUEUE_PATH)} and {rel(SOURCE_VARIANT_MANIFEST_PATH)}"},
        {"field": "time_axis", "value": "bar_time_server from run267W runtime feature files aligned to run267V raw surface"},
        {"field": "sample_scope", "value": "US100 M5 2024 historical stress window; run267AB ready guard queue rows only"},
        {"field": "missing_or_duplicate_check", "value": f"context_missing_rows={result['context_missing_rows']};surface_alignment_pass={result['surface_alignment_pass_count']}"},
        {"field": "feature_label_boundary", "value": "guard states use raw feature quantile buckets; no MT5 PnL is used as a training label"},
        {"field": "split_boundary", "value": "materialization uses 2024 train-era historical stress runtime surface only; execution and review remain pending"},
        {"field": "leakage_risk", "value": "guard queue was selected after weak-slice attribution, so next MT5 and broader review must treat this as exploratory"},
        {"field": "data_hash_or_identity", "value": f"variant_manifest={rel(VARIANT_MANIFEST_PATH)}"},
        {"field": "integrity_judgment", "value": "usable_with_boundary" if result["surface_alignment_pass_count"] == result["variant_count"] else "inconclusive"},
    ]
    judgment = [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"guard_variants={result['variant_count']};attempts={result['attempt_count']};neutral_parity={result['neutral_parity_passed_count']}/{result['variant_count']}",
            "evidence_missing": "MT5_execution;trade_list_review;balance_equity_curve;time_slice_KPI;trade_quality_after_guard",
            "judgment_label": JUDGMENT,
            "claim_boundary": "score_table_materialization_only_no_candidate_selection_no_onnx_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 약한 구간의 비달력 상태를 모델 옆에 작은 브레이크로 붙였고, 아직 실제 주행 점수는 보지 않았다.",
        }
    ]
    return design, integrity, judgment


def build_materialization() -> dict[str, Any]:
    require_inputs()
    queue_rows = [
        row
        for row in read_csv(SOURCE_QUEUE_PATH)
        if row.get("materialization_status") == "ready_for_noncalendar_state_guard_score_table_design"
    ]
    if not queue_rows:
        raise RuntimeError("no ready guard queue rows")
    source_by_pair = source_variants_by_pair()
    specs = specs_by_alias()
    variants: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    alignment_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    dynamic_artifacts: list[dict[str, Any]] = []

    for index, queue_row in enumerate(queue_rows, start=1):
        alias = str(queue_row["candidate_alias"])
        test_id = str(queue_row["source_test_id"])
        source_variant = source_by_pair.get((alias, test_id))
        if not source_variant:
            raise KeyError(f"missing run267W source variant for {alias}:{test_id}")
        spec = specs[alias]
        item = materialize_variant(queue_row, source_variant, spec, index)
        variants.append(item["variant"])
        contracts.append(item["contract"])
        diagnostics.extend(item["diagnostics"])
        parity_rows.append(item["parity"])
        alignment_rows.append(item["alignment"])
        attempts.extend(item["attempts"])
        dynamic_artifacts.extend(
            [
                {
                    "artifact_id": f"stage267_run267AC_{safe_token(str(queue_row['queue_id']), 64)}_runtime_feature",
                    "artifact_type": "runtime_feature_csv",
                    "path": rel(item["feature_path"]),
                    "notes": f"Run267AC runtime feature CSV for {queue_row['queue_id']}.",
                },
                {
                    "artifact_id": f"stage267_run267AC_{safe_token(str(queue_row['queue_id']), 64)}_runtime_model",
                    "artifact_type": "runtime_model_csv",
                    "path": rel(item["model_path"]),
                    "notes": f"Run267AC EBM score table CSV for {queue_row['queue_id']}.",
                },
            ]
        )

    created_at = utc_now()
    result: dict[str, Any] = {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_score_table_run_id": SOURCE_SCORE_TABLE_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "candidate_count": len({row["candidate_alias"] for row in variants}),
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "neutral_parity_passed_count": sum(1 for row in parity_rows if str(row.get("passed")).lower() == "true" or row.get("passed") is True),
        "surface_alignment_pass_count": sum(1 for row in alignment_rows if row.get("alignment_status") == "pass"),
        "context_missing_rows": sum(int(row.get("context_missing_rows", 0)) for row in alignment_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "variant_manifest": variants,
        "runtime_contract": contracts,
        "guard_state_diagnostics": diagnostics,
        "neutral_guard_score_parity": parity_rows,
        "surface_alignment": alignment_rows,
        "attempts": attempts,
        "dynamic_artifacts": dynamic_artifacts,
        "inputs": {
            "run267AB_guard_queue": rel(SOURCE_QUEUE_PATH),
            "run267AB_repeated_state_summary": rel(SOURCE_REPEATED_STATE_PATH),
            "run267AB_state_contrast": rel(SOURCE_STATE_CONTRAST_PATH),
            "run267W_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "run267W_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "run267AB_report": rel(SOURCE_QUEUE_REPORT_PATH),
            "run267W_report": rel(SOURCE_SCORE_TABLE_REPORT_PATH),
        },
        "outputs": {
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "guard_state_diagnostics": rel(GUARD_DIAGNOSTICS_PATH),
            "neutral_guard_score_parity": rel(PARITY_CHECK_PATH),
            "surface_alignment": rel(SURFACE_ALIGNMENT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "review_result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": {},
    }
    design, integrity, judgment = build_receipts(result)
    result["experiment_design_receipt"] = design
    result["data_integrity_receipt"] = integrity
    result["result_judgment"] = judgment
    return result


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "source_test_id": attempt.get("source_test_id"),
                "guard_rule_family": attempt.get("guard_rule_family"),
                "tier": attempt.get("tier"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        VARIANT_MANIFEST_PATH,
        result["variant_manifest"],
        (
            "queue_id",
            "priority",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "guard_rule_family",
            "guard_intent",
            "model_materialization_type",
            "source_queue_path",
            "source_runtime_feature_file",
            "runtime_feature_file",
            "runtime_feature_sha256",
            "source_runtime_model_file",
            "runtime_model_file",
            "runtime_model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "source_feature_count",
            "feature_count",
            "source_feature_order_hash",
            "feature_order",
            "feature_order_hash",
            "guard_score_feature",
            "guard_score_feature_index",
            "guard_state_features",
            "guard_score_cuts",
            "guard_score_terms",
            "runtime_rows",
            "signal_rows",
            "high_guard_signal_rows",
            "high_guard_signal_ratio",
            "neutral_parity_passed",
            "neutral_parity_max_abs_diff",
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
            "candidate_role",
            "source_test_id",
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
            "guard_rule_family",
            "guard_score_feature_index",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        GUARD_DIAGNOSTICS_PATH,
        result["guard_state_diagnostics"],
        (
            "queue_id",
            "candidate_alias",
            "test_id",
            "guard_state",
            "q25",
            "q75",
            "matched_rows",
            "matched_signal_rows",
            "state_source",
        ),
    )
    write_csv(
        PARITY_CHECK_PATH,
        result["neutral_guard_score_parity"],
        (
            "queue_id",
            "candidate_alias",
            "test_id",
            "passed",
            "max_abs_diff",
            "tolerance",
            "rows",
            "source_feature_count",
            "extended_feature_count",
            "guard_zero_policy",
            "table_path",
        ),
    )
    write_csv(
        SURFACE_ALIGNMENT_PATH,
        result["surface_alignment"],
        (
            "queue_id",
            "candidate_alias",
            "source_test_id",
            "runtime_rows",
            "raw_surface_rows",
            "bar_time_order_match",
            "duplicate_bar_time_rows",
            "runtime_missing_feature_cells",
            "context_missing_rows",
            "alignment_status",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(result["attempts"]),
        (
            "attempt_name",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "guard_rule_family",
            "tier",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "execution_status",
        ),
    )
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("field", "value"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("field", "value"))
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], ("result_subject", "evidence_available", "evidence_missing", "judgment_label", "claim_boundary", "next_condition", "user_explanation_hook"))

    run_manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_score_table_run_id": SOURCE_SCORE_TABLE_RUN_ID,
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
        "source_score_table_run_id": SOURCE_SCORE_TABLE_RUN_ID,
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
        "guard_state_diagnostics": sha256_file_lf_normalized(GUARD_DIAGNOSTICS_PATH),
        "neutral_guard_score_parity": sha256_file_lf_normalized(PARITY_CHECK_PATH),
        "surface_alignment": sha256_file_lf_normalized(SURFACE_ALIGNMENT_PATH),
        "experiment_design_receipt": sha256_file_lf_normalized(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "data_integrity_receipt": sha256_file_lf_normalized(DATA_INTEGRITY_RECEIPT_PATH),
        "result_judgment": sha256_file_lf_normalized(RESULT_JUDGMENT_PATH),
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
        "# Stage267 Run267AC Noncalendar State Guard Score Table Materialization(267단계 267AC 비달력 상태 방어 점수표 물질화)",
        "",
        "- action(행동): run267AB(267AB 실행)의 guard queue(방어 큐)를 run267W(267W 실행)의 true internal score table(진짜 내부 점수표)에 soft guard score(부드러운 방어 점수)로 붙였다.",
        "- effect(효과): calendar literal filter(달력 직접 필터)를 쓰지 않고, 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 약한 상태가 덜 깨지는지 확인할 수 있다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AB(267AB 실행)는 약한 거래가 자주 모이는 market state(시장 상태)를 찾았다. run267AC(267AC 실행)는 그 상태를 바로 잘라내지 않고, 모델 점수표(score table, 점수표)에 작은 flat-bias(무거래 쪽 가중)로 붙였다.",
        "Effect(효과): 거래 수가 무너지는지, 손실이 다른 구간으로 옮겨가는지, 실제로 약한 구간이 나아지는지는 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 봐야 한다.",
        "",
        "## Materialization Summary(물질화 요약)",
        "",
        f"- candidates(후보): `{result['candidate_count']}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- attempts queued(대기 시도): `{result['attempt_count']}`",
        f"- neutral parity passed(중립 동등성 통과): `{result['neutral_parity_passed_count']}/{result['variant_count']}`",
        f"- surface alignment passed(표면 정렬 통과): `{result['surface_alignment_pass_count']}/{result['variant_count']}`",
        f"- context missing rows(문맥 누락 행): `{result['context_missing_rows']}`",
        "",
        "## Boundary(경계)",
        "",
        "- MT5 execution(MT5 실행): `not_executed`",
        "- trading KPI(거래 핵심 성과 지표): `not_claimed`",
        "- balance/equity curve(잔액/평가금 곡선): `pending_MT5`",
        "- candidate selection(후보 선택): `none`",
        "- ONNX(ONNX): `not_reviewed`",
        "",
        "## Outputs(산출물)",
        "",
        f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
        f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        f"- guard_diagnostics(방어 진단): `{rel(GUARD_DIAGNOSTICS_PATH)}`",
        f"- neutral_parity(중립 동등성): `{rel(PARITY_CHECK_PATH)}`",
        f"- surface_alignment(표면 정렬): `{rel(SURFACE_ALIGNMENT_PATH)}`",
        f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        "- effect(효과): 14개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해서 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)를 확인한다.",
        "",
    ]
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    static = [
        ("stage267_run267AC_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267AC noncalendar state guard score table inputs."),
        ("stage267_run267AC_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267AC noncalendar state guard variant manifest."),
        ("stage267_run267AC_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267AC runtime contract."),
        ("stage267_run267AC_guard_diagnostics", "guard_state_diagnostics", GUARD_DIAGNOSTICS_PATH, "Run267AC guard state diagnostics."),
        ("stage267_run267AC_neutral_parity", "neutral_guard_score_parity_check", PARITY_CHECK_PATH, "Run267AC neutral guard score parity check."),
        ("stage267_run267AC_surface_alignment", "surface_alignment_check", SURFACE_ALIGNMENT_PATH, "Run267AC surface alignment check."),
        ("stage267_run267AC_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267AC experiment design receipt."),
        ("stage267_run267AC_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267AC data integrity receipt."),
        ("stage267_run267AC_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AC result judgment."),
        ("stage267_run267AC_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267AC MT5 attempt manifest."),
        ("stage267_run267AC_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267AC run manifest."),
        ("stage267_run267AC_lineage", "lineage", LINEAGE_PATH, "Run267AC lineage."),
        ("stage267_run267AC_review_result", "review_result_json", RESULT_PATH, "Run267AC review result JSON."),
        ("stage267_run267AC_report", "review_report", REPORT_PATH, "Run267AC review report."),
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
        "lane": "noncalendar_state_guard_score_table_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT),
        "notes": (
            f"variants={result['variant_count']};attempts={result['attempt_count']};"
            f"neutral_parity={result['neutral_parity_passed_count']}/{result['variant_count']};"
            f"selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;next_action={NEXT_ACTION}."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_score_table_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "noncalendar_state_guard_score_table_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "noncalendar_state_guard_score_table_materialization",
        "tier_scope": "Tier A and Tier A+B 2024 historical runtime attempts planned",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "experiment_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};neutral_parity={result['neutral_parity_passed_count']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;mt5_execution=not_executed",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    stage_row = {
        "row_id": "stage267_run267AC_noncalendar_state_guard_score_table_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "noncalendar_state_guard_score_table_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 noncalendar guard attempts planned",
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
    report_line = f"- run267AC_noncalendar_state_guard_score_table_materialization(267AC 비달력 상태 방어 점수표 물질화): `{rel(REPORT_PATH)}`"
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_score_table_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(current, "run267AB_noncalendar_weak_slice_resilience_queue", report_line)
    current = current.replace("`run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`", f"`{NEXT_ACTION}`")
    current = current.replace(
        "- next_run(다음 실행): `run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    current = current.replace(
        "- next_action(다음 행동): `run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    current = current.replace(
        "- action(행동): run267AB(267AB 실행)는 run267Z(267Z 실행) 거래와 run267V(267V 실행) raw feature surface(원시 피처 표면)를 결합해 비달력 약점 상태를 큐로 만들었다.",
        "- action(행동): run267AC(267AC 실행)는 run267AB(267AB 실행)의 guard queue(방어 큐)를 score table/model/set/ini(점수표/모델/설정/초기화) 묶음으로 만들었다.",
    )
    current = current.replace(
        "- effect(효과): Monday(월요일)/2024-12(2024년 12월)를 직접 자르지 않고, 반복된 시장 상태 guard(방어 장치)만 다음 score table(점수표) 설계로 보낸다.",
        "- effect(효과): calendar literal filter(달력 직접 필터)를 쓰지 않고, 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 거래/곡선/시간구간 영향을 확인한다.",
    )
    current = append_block_once(
        current,
        "Run267AC(267AC 실행)는 run267AB",
        "\n".join(
            [
                "Run267AC(267AC 실행)는 run267AB(267AB 실행)의 guard queue(방어 큐)를 score table/model(점수표/모델) 입력으로 물질화했다.",
                "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음 run267AD(267AD 실행)에서 14개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실행해 실제 거래/곡선/시간구간 영향을 확인한다.",
            ]
        ),
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(selection, "run267AB_noncalendar_weak_slice_resilience_queue", report_line)
    selection = selection.replace(
        "- next_action(다음 행동): `run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection = selection.replace(
        "- status(상태): `run267AB_noncalendar_weak_slice_resilience_queue_materialized`",
        f"- status(상태): `{STATUS}`",
    )
    selection = append_block_once(
        selection,
        "Run267AC(267AC 실행)는 noncalendar state guard score table",
        "\n".join(
            [
                "Run267AC(267AC 실행)는 noncalendar state guard score table materialization(비달력 상태 방어 점수표 물질화)을 완료했다.",
                "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, run267AD(267AD 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 실제 거래/곡선/시간구간 영향을 확인한다.",
            ]
        ),
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{STATUS}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after_contains(review, "run267AB_noncalendar_weak_slice_resilience_queue", report_line)
    review = review.replace(
        "- next_action(다음 행동): `run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    review = append_block_once(
        review,
        "Run267AC(267AC 실행)는 noncalendar state guard score table",
        "\n".join(
            [
                "Run267AC(267AC 실행)는 noncalendar state guard score table materialization(비달력 상태 방어 점수표 물질화)을 완료했다.",
                "Effect(효과): run267AB(267AB 실행)의 비달력 상태 단서를 14개 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 시도로 바꿨고, 선택 후보(selected candidate, 선택 후보)는 없다.",
            ]
        ),
    )
    write_text(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus_block = (
        "- >-\n"
        f"  Stage267(267단계) run267AC(267AC 실행) noncalendar state guard score table materialization(비달력 상태 방어 점수표 물질화) `{STATUS}`. "
        "Effect(효과): run267AB(267AB 실행)의 상태 guard(방어 장치) 큐를 7개 score table/model(점수표/모델)과 14개 MT5(MetaTrader 5, 메타트레이더5) 시도 입력으로 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace("  status: run267AB_noncalendar_weak_slice_resilience_queue_materialized", f"  status: {STATUS}", 1)
    workspace = workspace.replace("  current_run_id: run267AB_stage267_noncalendar_weak_slice_resilience_queue_v1", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace("  last_completed_run_id: run267AB_stage267_noncalendar_weak_slice_resilience_queue_v1", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = append_after_contains(
        workspace,
        "run267AB_noncalendar_weak_slice_resilience_queue_report_path",
        f"  run267AC_noncalendar_state_guard_score_table_materialization_report_path: {rel(REPORT_PATH)}",
    )
    workspace = workspace.replace(
        "next_action: run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue",
        f"next_action: {NEXT_ACTION}",
    )
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`이다. Effect(효과): run267AB(267AB 실행)의 비달력 상태 guard(방어 장치) 큐를 score table/model(점수표/모델) 설계로 물질화한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): run267AC(267AC 실행)의 14개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실행해 거래/곡선/시간구간 영향을 확인한다.",
    )
    workspace = workspace.replace(
        "active_run267Z_true_internal_ablation_balance_timeslice_trade_quality_review_completed(267Z 진짜 내부 제거 잔액/시간구간/거래품질 검토 완료 활성)",
        "active_run267AC_noncalendar_state_guard_score_table_materialization(267AC 비달력 상태 방어 점수표 물질화 활성)",
    )
    write_text(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_materialization()
    write_outputs(result)
    final_result = json.loads(io_path(RESULT_PATH).read_text(encoding="utf-8"))
    update_ledgers(final_result)
    update_docs()
    print(
        json.dumps(
            {
                "status": STATUS,
                "variant_count": final_result["variant_count"],
                "attempt_count": final_result["attempt_count"],
                "neutral_parity_passed_count": final_result["neutral_parity_passed_count"],
                "surface_alignment_pass_count": final_result["surface_alignment_pass_count"],
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
