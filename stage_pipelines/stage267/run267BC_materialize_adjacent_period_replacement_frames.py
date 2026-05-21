from __future__ import annotations

import csv
import json
import math
import sys
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
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import (
    run267BB_cross_period_replacement_ready_subset_review as source_review,
)
from stage_pipelines.stage267 import (
    run267K_retrained_soft_context_adapter_materialization as source_retrain,
)
from stage_pipelines.stage267 import (
    run267V_reconstruct_upstream_feature_surface as source_surface,
)
from stage_pipelines.stage267 import (
    run267W_true_internal_ablation_score_table_materialization as source_materialization,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267BC"
RUN_ID = "run267BC_stage267_adjacent_period_replacement_frame_materialization_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267BC_adjacent_period_replacement_frames_materialized_route_manifest_repair_inputs_ready_execution_pending"
JUDGMENT = "adjacent_period_attempt_inputs_materialized_no_mt5_execution_no_candidate_selection"
NEXT_ACTION = "run267BD_execute_s264_aia_adjacent_period_replacement_mt5_batch_or_repair_materialization_gaps"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "adjacent_period_replacement_frame_materialization"
FEATURE_ROOT = RUN_ROOT / "features"

SOURCE_SUBSET_REVIEW_PATH = source_review.SUBSET_REVIEW_PATH
SOURCE_NEXT_QUEUE_PATH = source_review.NEXT_EXPERIMENT_QUEUE_PATH
SOURCE_RUN267W_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_RUN267W_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH
SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH = source_review.SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH
SOURCE_BA_TRUE_FALLBACK_STATUS_PATH = source_review.SOURCE_BA_TRUE_FALLBACK_STATUS_PATH
SOURCE_Z_TIER_DUPLICATE_PATH = source_review.SOURCE_Z_TIER_DUPLICATE_PATH

PERIOD_AVAILABILITY_PATH = RUN_ROOT / "adjacent_period_source_availability.csv"
WATCH_PAIR_QUEUE_PATH = RUN_ROOT / "s264_aia_watch_pair_adjacent_period_queue.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "adjacent_period_feature_frame_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempts.csv"
ROUTE_REPAIR_INPUT_PATH = RUN_ROOT / "route_manifest_repair_inputs.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BC_adjacent_period_replacement_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BC_materialize_adjacent_period_replacement_frames.py")

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_review.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_review.ARTIFACT_COLUMNS

COMMON_ROOT = "OPV2/s267bc/run267BC_adjacent_period_replacement"
WATCH_ALIAS = "s264_aia"
WATCH_TESTS = ("rep_trend_strength_adx", "rep_volatility_atr")
ADJACENT_PERIODS = (
    {
        "period_id": "adjacent_2023_h2_train_pre_2024",
        "period_label": "adjacent_2023_h2_train_pre_2024",
        "start": "2023-07-01",
        "end": "2024-01-01",
        "period_role": "pre_2024_train_context",
    },
    {
        "period_id": "adjacent_2025_h1_validation_post_2024",
        "period_label": "adjacent_2025_h1_validation_post_2024",
        "start": "2025-01-01",
        "end": "2025-07-01",
        "period_role": "post_2024_validation_context",
    },
    {
        "period_id": "adjacent_2025_h2_oos_followthrough",
        "period_label": "adjacent_2025_h2_oos_followthrough",
        "start": "2025-07-01",
        "end": "2026-01-01",
        "period_role": "oos_followthrough_context",
    },
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
    if isinstance(value, (list, tuple, set)):
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
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def split_semicolon(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


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


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            replaced = True
            break
    if not replaced:
        lines.append(replacement)
    return "\n".join(lines) + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    output: list[str] = []
    inserted = False
    for item in text.splitlines():
        output.append(item)
        if needle in item and not inserted:
            output.append(line)
            inserted = True
    if not inserted:
        output.append(line)
    return "\n".join(output) + "\n"


def append_block_once(text: str, unique: str, block: str) -> str:
    if unique in text:
        return text
    suffix = "\n" if text.endswith("\n") else "\n\n"
    return text + suffix + block.rstrip() + "\n"


def prepend_current_focus(text: str, block: str) -> str:
    if "run267BC(267BC 실행)" in text:
        return text
    marker = "current_focus:\n"
    if marker in text:
        return text.replace(marker, marker + block, 1)
    return text + "\ncurrent_focus:\n" + block


def source_hashes(paths: Mapping[str, Path]) -> dict[str, str]:
    output: dict[str, str] = {}
    for key, path in paths.items():
        output[key] = sha256_file_lf_normalized(path) if path_exists(path) else "missing"
    return output


def require_inputs() -> None:
    required = (
        SOURCE_SUBSET_REVIEW_PATH,
        SOURCE_NEXT_QUEUE_PATH,
        SOURCE_RUN267W_VARIANT_MANIFEST_PATH,
        SOURCE_RUN267W_ATTEMPT_MANIFEST_PATH,
        SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH,
        SOURCE_BA_TRUE_FALLBACK_STATUS_PATH,
        SOURCE_Z_TIER_DUPLICATE_PATH,
    )
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run267BC inputs: " + "; ".join(missing))


def watch_rows() -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(SOURCE_SUBSET_REVIEW_PATH)
        if row.get("candidate_alias") == WATCH_ALIAS
        and row.get("test_id") in WATCH_TESTS
        and row.get("run267BB_decision") == "watch_pair_for_adjacent_period_materialization"
    ]
    if len(rows) != len(WATCH_TESTS):
        raise RuntimeError(f"expected {len(WATCH_TESTS)} watch rows, found {len(rows)}")
    return sorted(rows, key=lambda row: WATCH_TESTS.index(str(row["test_id"])))


def variant_manifest_by_test() -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in read_csv(SOURCE_RUN267W_VARIANT_MANIFEST_PATH):
        if row.get("candidate_alias") == WATCH_ALIAS and row.get("test_id") in WATCH_TESTS:
            output[str(row["test_id"])] = row
    missing = [test_id for test_id in WATCH_TESTS if test_id not in output]
    if missing:
        raise RuntimeError("missing run267W variant manifest rows: " + ";".join(missing))
    return output


def period_frame(source: pd.DataFrame, period: Mapping[str, str]) -> pd.DataFrame:
    start = pd.Timestamp(str(period["start"]), tz="UTC")
    end = pd.Timestamp(str(period["end"]), tz="UTC")
    frame = source.loc[source["timestamp"].ge(start) & source["timestamp"].lt(end)].copy()
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    if frame.empty:
        raise RuntimeError(f"empty adjacent period source frame: {period['period_id']}")
    return frame


def date_for_tester(timestamp: pd.Timestamp) -> str:
    return timestamp.strftime("%Y.%m.%d")


def build_period_availability(source: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    frames: dict[str, pd.DataFrame] = {}
    raw_columns = list(source_surface.RAW_SURFACE_COLUMNS)
    for period in ADJACENT_PERIODS:
        frame = period_frame(source, period)
        frames[str(period["period_id"])] = frame
        first = pd.Timestamp(frame["timestamp"].iloc[0])
        last = pd.Timestamp(frame["timestamp"].iloc[-1])
        missing_raw = int(frame.loc[:, raw_columns].isna().sum().sum())
        split_counts = {str(k): int(v) for k, v in frame["split"].value_counts().sort_index().items()}
        rows.append(
            {
                "period_id": period["period_id"],
                "period_label": period["period_label"],
                "period_role": period["period_role"],
                "requested_start_utc": period["start"],
                "requested_end_exclusive_utc": period["end"],
                "rows": int(len(frame)),
                "first_time_utc": first.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "last_time_utc": last.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "tester_from_date": date_for_tester(first),
                "tester_to_date": pd.Timestamp(str(period["end"]), tz="UTC").strftime("%Y.%m.%d"),
                "split_counts": json.dumps(split_counts, ensure_ascii=False, sort_keys=True),
                "duplicate_timestamp_rows": int(frame["timestamp"].duplicated().sum()),
                "missing_signal_rows": int(pd.to_numeric(frame[input_probe.SOURCE_SIGNAL_COLUMN], errors="coerce").isna().sum()),
                "missing_raw_feature_cells": missing_raw,
                "availability_status": "usable" if missing_raw == 0 else "usable_with_boundary",
            }
        )
    return rows, frames


def spec_for_watch_alias() -> Any:
    specs = {spec.alias: spec for spec in input_probe.candidate_specs()}
    return specs[WATCH_ALIAS]


def gate_column_for_spec(spec: Any) -> str:
    extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
    return f"{spec.module.GATE_COLUMN_PREFIX}_{extra['axis']}"


def feature_value(record: Mapping[str, Any], spec: Any, rank_column: str, gate_column: str, feature: str) -> Any:
    mapped = input_probe.row_mapping(record)
    if feature == input_probe.SOURCE_SIGNAL_COLUMN:
        return int(round(spec.module.s250.stage238.parse_float(mapped.get(input_probe.SOURCE_SIGNAL_COLUMN), 0.0)))
    if feature == rank_column:
        bucket_value, _ = spec.module.s250.stage238.rank_bucket_for(mapped)
        return bucket_value
    if feature == gate_column:
        extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
        return spec.module.source_branch_gate_value(mapped, str(extra["source_branch_mode"]))
    return record.get(feature)


def build_runtime_feature_file(
    frame: pd.DataFrame,
    spec: Any,
    feature_order: Sequence[str],
    destination: Path,
) -> tuple[dict[str, Any], pd.DataFrame]:
    rank_column = str(spec.module.RANK_COLUMN)
    gate_column = gate_column_for_spec(spec)
    rows: list[dict[str, Any]] = []
    for record in frame.to_dict("records"):
        timestamp = pd.Timestamp(record["timestamp"])
        row: dict[str, Any] = {"bar_time_server": timestamp.strftime("%Y.%m.%d %H:%M:%S")}
        for feature in feature_order:
            row[feature] = feature_value(record, spec, rank_column, gate_column, feature)
        rows.append(row)
    write_runtime_csv(destination, rows, ("bar_time_server", *feature_order))
    runtime = pd.DataFrame.from_records(rows)
    missing_cells = int(runtime.loc[:, list(feature_order)].isna().sum().sum()) if len(runtime) else 0
    meta = {
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "rows": int(len(runtime)),
        "first_bar_time_server": str(runtime["bar_time_server"].iloc[0]) if len(runtime) else "",
        "last_bar_time_server": str(runtime["bar_time_server"].iloc[-1]) if len(runtime) else "",
        "duplicate_bar_time_rows": int(runtime["bar_time_server"].duplicated().sum()) if len(runtime) else 0,
        "runtime_missing_feature_cells": missing_cells,
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
    }
    return meta, runtime


def build_watch_pair_queue(watch: Sequence[Mapping[str, str]], periods: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    order = 1
    for item in watch:
        for period in periods:
            rows.append(
                {
                    "queue_order": order,
                    "queue_id": f"run267BC_q{order:02d}_{WATCH_ALIAS}_{item['test_id']}_{period['period_id']}",
                    "parent_materialization_id": item.get("materialization_id"),
                    "candidate_id": item.get("candidate_id"),
                    "candidate_alias": item.get("candidate_alias"),
                    "candidate_role": item.get("candidate_role"),
                    "test_id": item.get("test_id"),
                    "feature_family": item.get("feature_family"),
                    "period_id": period["period_id"],
                    "period_role": period["period_role"],
                    "comparison_baseline": "run267BB 2024 Tier A replacement subset review",
                    "decision_use": "decide whether s264_aia watch pair survives outside 2024 before Adapter spending",
                    "required_evidence": "MT5 KPI;trade list;balance/equity curve;time-slice KPI;route boundary",
                    "queue_status": "materialized_execution_pending",
                }
            )
            order += 1
    return rows


def build_route_repair_inputs() -> list[dict[str, Any]]:
    requirement_rows = read_csv(SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH)
    status_rows = read_csv(SOURCE_BA_TRUE_FALLBACK_STATUS_PATH)
    duplicate_rows = read_csv(SOURCE_Z_TIER_DUPLICATE_PATH)
    duplicate_audit = {
        str(row.get("candidate_alias")): str(row.get("tier_duplicate_audit") or row.get("audit_status") or "")
        for row in duplicate_rows
    }
    rows: list[dict[str, Any]] = []
    for status in status_rows:
        alias = str(status.get("candidate_alias"))
        for req in requirement_rows:
            rows.append(
                {
                    "candidate_alias": alias,
                    "required_field": req.get("required_field"),
                    "current_status": req.get("current_status"),
                    "run267BA_status": status.get("materialization_status"),
                    "tier_a_record_status": status.get("tier_a_record_status"),
                    "tier_b_record_status": status.get("tier_b_record_status"),
                    "actual_routed_total_status": status.get("actual_routed_total_status"),
                    "duplicate_audit": duplicate_audit.get(alias, "duplicate_due_to_fallback_disabled_or_missing"),
                    "run267BC_repair_input_status": "input_recorded_still_blocked",
                    "next_required_action": "build_component_route_manifest_before_any_routed_MT5_claim",
                    "effect": "keeps actual routed total separate from synthetic Tier A+B rows",
                }
            )
    return rows


def materialize_attempts(
    frames: Mapping[str, pd.DataFrame],
    watch: Sequence[Mapping[str, str]],
    variant_by_test: Mapping[str, Mapping[str, str]],
    period_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    spec = spec_for_watch_alias()
    gate_column = gate_column_for_spec(spec)
    period_by_id = {str(row["period_id"]): row for row in period_rows}
    attempts: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    order = 1
    for item in watch:
        test_id = str(item["test_id"])
        variant = variant_by_test[test_id]
        feature_order = split_semicolon(variant["feature_order"])
        if not feature_order:
            raise RuntimeError(f"empty feature order for {test_id}")
        if ordered_hash(feature_order) != str(variant["feature_order_hash"]):
            raise RuntimeError(f"feature order hash mismatch for {test_id}")
        model_local_path = repo_path(str(variant["runtime_model_file"]))
        if not path_exists(model_local_path):
            raise FileNotFoundError(model_local_path)
        for period in ADJACENT_PERIODS:
            period_id = str(period["period_id"])
            period_meta = period_by_id[period_id]
            period_token = safe_token(period_id, 48)
            test_token = safe_token(test_id, 40)
            feature_path = FEATURE_ROOT / WATCH_ALIAS / period_token / f"{WATCH_ALIAS}_{test_token}_{period_token}.csv"
            feature_meta, runtime_frame = build_runtime_feature_file(frames[period_id], spec, feature_order, feature_path)
            common_feature_path = f"{COMMON_ROOT}/{WATCH_ALIAS}/{period_token}/{test_token}/features/{feature_path.name}"
            common_model_path = f"{COMMON_ROOT}/{WATCH_ALIAS}/{test_token}/models/{model_local_path.name}"
            common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
            common_model = copy_to_common(model_local_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)
            magic = 26730000 + order
            attempt_name = f"adj_{WATCH_ALIAS}_{test_token}_{period_token}"
            payload = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label=f"stage267_AdjacentReplacement__{test_token}",
                attempt_name=attempt_name,
                tier=input_probe.mt5.TIER_A,
                split=str(period["period_label"]),
                model_path=common_model_path,
                model_id=f"{RUN_ID}_{WATCH_ALIAS}_{test_token}",
                model_backend="ebm_table",
                feature_path=common_feature_path,
                feature_count=len(feature_order),
                feature_order_hash=ordered_hash(feature_order),
                short_threshold=spec.variant.short_threshold,
                long_threshold=spec.variant.long_threshold,
                min_margin=0.0,
                invert_signal=False,
                from_date=str(period_meta["tester_from_date"]),
                to_date=str(period_meta["tester_to_date"]),
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix=f"mt5_ta_{WATCH_ALIAS}_{test_token}_{period_token}",
                max_hold_bars=spec.variant.max_hold_bars,
                common_root=f"{COMMON_ROOT}/{WATCH_ALIAS}/{period_token}/{test_token}",
                fallback_enabled=False,
                close_on_flat_signal=spec.variant.close_on_flat_signal,
                reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                extra_set_values=source_materialization.extra_set_for_feature_order(spec, feature_order, gate_column, magic),
            )
            payload.update(
                {
                    "queue_order": order,
                    "queue_id": f"run267BC_q{order:02d}_{WATCH_ALIAS}_{test_id}_{period_id}",
                    "candidate_id": item.get("candidate_id"),
                    "candidate_alias": WATCH_ALIAS,
                    "candidate_role": item.get("candidate_role"),
                    "test_id": test_id,
                    "feature_family": item.get("feature_family"),
                    "period_id": period_id,
                    "period_role": period["period_role"],
                    "source_run267W_queue_id": variant.get("queue_id"),
                    "source_2024_attempt": item.get("tier_a_2024_attempt"),
                    "common_feature_path": common_feature_path,
                    "common_feature_sha256": common_feature["sha256"],
                    "common_model_path": common_model_path,
                    "common_model_sha256": common_model["sha256"],
                    "execution_status": "not_executed",
                    "fallback_enabled": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(payload)
            feature_rows.append(
                {
                    "queue_order": order,
                    "queue_id": payload["queue_id"],
                    "candidate_id": item.get("candidate_id"),
                    "candidate_alias": WATCH_ALIAS,
                    "candidate_role": item.get("candidate_role"),
                    "test_id": test_id,
                    "feature_family": item.get("feature_family"),
                    "period_id": period_id,
                    "period_role": period["period_role"],
                    "runtime_feature_file": feature_meta["feature_file"],
                    "runtime_feature_sha256": feature_meta["feature_sha256"],
                    "common_feature_path": common_feature_path,
                    "common_feature_sha256": common_feature["sha256"],
                    "runtime_model_file": variant.get("runtime_model_file"),
                    "runtime_model_sha256": variant.get("runtime_model_sha256"),
                    "common_model_path": common_model_path,
                    "common_model_sha256": common_model["sha256"],
                    "rows": feature_meta["rows"],
                    "first_bar_time_server": feature_meta["first_bar_time_server"],
                    "last_bar_time_server": feature_meta["last_bar_time_server"],
                    "duplicate_bar_time_rows": feature_meta["duplicate_bar_time_rows"],
                    "runtime_missing_feature_cells": feature_meta["runtime_missing_feature_cells"],
                    "feature_count": feature_meta["feature_count"],
                    "feature_order_hash": feature_meta["feature_order_hash"],
                    "removed_columns_actual": variant.get("removed_columns_actual"),
                    "bar_time_order_status": "pass" if feature_meta["duplicate_bar_time_rows"] == 0 else "blocked_duplicate_time",
                    "materialization_status": "materialized_execution_pending",
                }
            )
            order += 1
    return feature_rows, attempts


def build_receipts(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    experiment = [
        {
            "field": "hypothesis",
            "value": "s264_aia replacement watch pair is useful only if adjacent periods do not break it",
        },
        {
            "field": "decision_use",
            "value": "materialize MT5 attempt inputs; decide later from adjacent-period KPI and curve evidence",
        },
        {
            "field": "comparison_baseline",
            "value": "run267BB 2024 Tier A replacement subset review",
        },
        {
            "field": "control_variables",
            "value": "same s264_aia score tables; same feature order hash; no calendar rule change; Tier A only",
        },
        {
            "field": "changed_variables",
            "value": "runtime feature period window only",
        },
        {
            "field": "sample_scope",
            "value": "2023H2 train-era, 2025H1 validation-era, 2025H2 OOS-followthrough Tier A source frames",
        },
        {
            "field": "success_criteria",
            "value": "MT5 execution later shows viable net/PF/trades/DD and no deep Monday/month hole",
        },
        {
            "field": "failure_criteria",
            "value": "watch pair collapses outside 2024 or remains dependent on one period",
        },
        {
            "field": "invalid_conditions",
            "value": "feature order hash mismatch, duplicate timestamps, missing model, or routed total claim from fallback-disabled rows",
        },
        {
            "field": "stop_conditions",
            "value": "execute only these six Tier A attempts before any Adapter build; keep true fallback blocked until manifest repair",
        },
        {
            "field": "evidence_plan",
            "value": "attempt manifest, MT5 KPI, trade records, balance/equity curve, time-slice KPI, route boundary audit",
        },
    ]
    data = [
        {
            "field": "data_source",
            "value": "Stage56 Tier A source frame rebuilt through run267K source_frame and run267W feature order",
        },
        {
            "field": "time_axis",
            "value": "UTC timestamp converted to MT5 bar_time_server; feature timestamp match remains required",
        },
        {
            "field": "sample_scope",
            "value": f"periods={result['counts']['period_rows']};feature_frames={result['counts']['feature_frames']}",
        },
        {
            "field": "missing_or_duplicate_check",
            "value": f"duplicates_total={result['counts']['duplicate_timestamp_rows']};missing_feature_cells={result['counts']['missing_feature_cells']}",
        },
        {
            "field": "feature_label_boundary",
            "value": "MT5 PnL is not used for feature generation; runtime frames reuse prebuilt supervised EBM score tables",
        },
        {
            "field": "split_boundary",
            "value": "period roles are labeled train/validation/OOS context, but no new selection claim is made",
        },
        {
            "field": "leakage_risk",
            "value": "selection bias remains because watch pair was chosen after 2024 review; later results are diagnostic only",
        },
        {
            "field": "data_hash_or_identity",
            "value": rel(FEATURE_FRAME_MANIFEST_PATH),
        },
        {
            "field": "integrity_judgment",
            "value": "usable_with_boundary",
        },
    ]
    runtime = [
        {
            "receipt_id": "run267BC_runtime_01",
            "subject": "MT5 attempt inputs",
            "status": "materialized_execution_pending",
            "evidence": rel(ATTEMPT_MANIFEST_PATH),
            "effect": "next run can execute adjacent-period Tier A attempts without changing score tables",
        },
        {
            "receipt_id": "run267BC_runtime_02",
            "subject": "true fallback route",
            "status": "still_blocked_manifest_repair_inputs_only",
            "evidence": rel(ROUTE_REPAIR_INPUT_PATH),
            "effect": "prevents synthetic Tier A+B rows from becoming an actual routed total claim",
        },
        {
            "receipt_id": "run267BC_runtime_03",
            "subject": "ONNX parity",
            "status": "not_allowed_until_goal_gate",
            "evidence": "",
            "effect": "no ONNX review from materialization-only evidence",
        },
    ]
    gates = [
        {
            "gate_id": "watch_pair_only",
            "status": "pass",
            "evidence": rel(WATCH_PAIR_QUEUE_PATH),
            "effect": "only the run267BB s264_aia watch pair is materialized",
        },
        {
            "gate_id": "feature_order_hash_preserved",
            "status": "pass",
            "evidence": rel(FEATURE_FRAME_MANIFEST_PATH),
            "effect": "period pressure changes data window, not model meaning",
        },
        {
            "gate_id": "mt5_not_claimed",
            "status": "pass",
            "evidence": rel(ATTEMPT_MANIFEST_PATH),
            "effect": "execution is pending, so no KPI claim is made",
        },
        {
            "gate_id": "true_fallback_not_claimed",
            "status": "pass_with_blocker",
            "evidence": rel(ROUTE_REPAIR_INPUT_PATH),
            "effect": "fallback remains blocked until component manifest fields exist",
        },
        {
            "gate_id": "selection_and_onnx_closed",
            "status": "pass",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected candidate, ONNX readiness, and Goal Achieve stay unclaimed",
        },
    ]
    return experiment, data, runtime, gates


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = result["counts"]
    return [
        {
            "result_subject": "overall_run267BC_materialization",
            "evidence_available": f"periods={counts['period_rows']};feature_frames={counts['feature_frames']};attempts={counts['attempts']}",
            "evidence_missing": "MT5 KPI, trade list, balance/equity curve, time-slice review, true fallback component manifest",
            "judgment_label": JUDGMENT,
            "claim_boundary": "materialization only; no selected candidate; no ONNX readiness; no Goal Achieve",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "We prepared the period tests; we did not prove the candidate yet.",
        },
        {
            "result_subject": "s264_aia_watch_pair_adjacent_period",
            "evidence_available": "six Tier A attempt inputs across two replacement tests and three adjacent periods",
            "evidence_missing": "period KPI and curve evidence after MT5 execution",
            "judgment_label": "execution_pending_watch_only",
            "claim_boundary": "watch is not selection",
            "next_condition": "run267BD MT5 execution and curve/time-slice review",
            "user_explanation_hook": "The watch pair gets a wider test, not a promotion.",
        },
        {
            "result_subject": "true_fallback_route",
            "evidence_available": rel(ROUTE_REPAIR_INPUT_PATH),
            "evidence_missing": "tier_a_primary_record_id, tier_b_fallback_record_id, route_rule_id, fallback_used_count, component record reconciliation",
            "judgment_label": "blocked",
            "claim_boundary": "no actual routed total claim",
            "next_condition": "component route manifest exists and reconciles nonzero fallback use",
            "user_explanation_hook": "Fallback remains blocked because the route components are still not separable.",
        },
    ]


def build_result() -> dict[str, Any]:
    require_inputs()
    created_at = utc_now()
    watch = watch_rows()
    variant_by_test = variant_manifest_by_test()
    source, source_info = source_retrain.source_frame()
    period_rows, frames = build_period_availability(source)
    queue_rows = build_watch_pair_queue(watch, period_rows)
    feature_rows, attempts = materialize_attempts(frames, watch, variant_by_test, period_rows)
    route_inputs = build_route_repair_inputs()
    counts = {
        "watch_rows": len(watch),
        "period_rows": len(period_rows),
        "queue_rows": len(queue_rows),
        "feature_frames": len(feature_rows),
        "attempts": len(attempts),
        "route_repair_rows": len(route_inputs),
        "duplicate_timestamp_rows": sum(as_int(row.get("duplicate_timestamp_rows")) for row in period_rows),
        "missing_feature_cells": sum(as_int(row.get("runtime_missing_feature_cells")) for row in feature_rows),
    }
    sources = {
        "subset_review": SOURCE_SUBSET_REVIEW_PATH,
        "next_queue": SOURCE_NEXT_QUEUE_PATH,
        "run267W_variant_manifest": SOURCE_RUN267W_VARIANT_MANIFEST_PATH,
        "run267W_attempt_manifest": SOURCE_RUN267W_ATTEMPT_MANIFEST_PATH,
        "true_fallback_requirements": SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH,
        "true_fallback_status": SOURCE_BA_TRUE_FALLBACK_STATUS_PATH,
        "tier_duplicate_audit": SOURCE_Z_TIER_DUPLICATE_PATH,
        "producer": PRODUCER_PATH,
    }
    result: dict[str, Any] = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "source_info": source_info,
        "watch_rows": watch,
        "period_availability": period_rows,
        "watch_pair_queue": queue_rows,
        "feature_frame_manifest": feature_rows,
        "attempts": attempts,
        "route_manifest_repair_inputs": route_inputs,
        "counts": counts,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "sources": {name: rel(path) for name, path in sources.items()},
        "outputs": {
            "period_availability": rel(PERIOD_AVAILABILITY_PATH),
            "watch_pair_queue": rel(WATCH_PAIR_QUEUE_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "route_manifest_repair_inputs": rel(ROUTE_REPAIR_INPUT_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": source_hashes(sources),
    }
    experiment, data, runtime, gates = build_receipts(result)
    result["experiment_design_receipt"] = experiment
    result["data_integrity_receipt"] = data
    result["runtime_parity_receipt"] = runtime
    result["gate_audit"] = gates
    result["result_judgment"] = build_result_judgment(result)
    return result


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267BC Adjacent-period Replacement Materialization(267단계 267BC 인접 기간 대체 물질화)",
        "",
        "- action(행동): run267BB(267BB 실행)의 `s264_aia` watch pair(관찰 쌍) 2개를 2023H2/2025H1/2025H2 adjacent period(인접 기간) feature frame(피처 프레임)과 MT5 attempt manifest(MT5 시도 목록)로 만들었다.",
        "- effect(효과): 다음 run267BD(267BD 실행)에서 후보 의미를 바꾸지 않고 기간만 넓혀 덜 깨지는지 확인할 수 있다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- periods(기간): `{counts['period_rows']}`",
        f"- feature_frames(피처 프레임): `{counts['feature_frames']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "이번 실행은 성과를 낸 실행이 아니라, 성과를 검증할 재료를 만든 실행이다.",
        "Effect(효과): `s264_aia`가 2024년에서만 좋아 보인 것인지, 2023년 후반과 2025년 구간에서도 덜 깨지는지 다음 MT5(MetaTrader 5, 메타트레이더5)에서 볼 수 있다.",
        "",
        "좋은 후보라고 부르려면 아직 멀었다. 지금은 watch(관찰) 상태다.",
        "Effect(효과): 숫자 몇 개가 좋았다는 이유로 Adapter(어댑터) 개발이나 ONNX(ONNX) 검토로 뛰지 않는다.",
        "",
        "true fallback(실제 대체)은 여전히 막혀 있다.",
        "Effect(효과): duplicate Tier A+B(중복 Tier A+B)를 actual routed total(실제 라우팅 전체)처럼 오해하지 않는다.",
        "",
        "## Period Availability(기간 가용성)",
        "",
        "| period(기간) | role(역할) | rows(행) | first(첫 시각) | last(마지막 시각) | split counts(스플릿 수) | status(상태) |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in result["period_availability"]:
        lines.append(
            f"| `{row['period_id']}` | `{row['period_role']}` | {row['rows']} | `{row['first_time_utc']}` | `{row['last_time_utc']}` | `{row['split_counts']}` | `{row['availability_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| queue(큐) | test(시험) | period(기간) | rows(행) | feature hash(피처 해시) | status(상태) |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in result["feature_frame_manifest"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['test_id']}` | `{row['period_id']}` | {row['rows']} | `{row['feature_order_hash']}` | `{row['materialization_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- MT5 execution(MT5 실행): `not_executed`, 다음 실행에서 확인한다.",
            "- true fallback(실제 대체): `blocked`, route manifest(라우팅 목록) 구성요소가 아직 없다.",
            "- Adapter(어댑터): 보류. adjacent-period(인접 기간) KPI(핵심 성과 지표), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선)를 본 뒤 판단한다.",
            "- ONNX parity(ONNX 동등성): 금지. Goal gate(목표 게이트) 전에는 검토하지 않는다.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source subset review(원천 부분집합 검토): `{rel(SOURCE_SUBSET_REVIEW_PATH)}`.",
            f"- source run267W variant manifest(원천 267W 변형 목록): `{rel(SOURCE_RUN267W_VARIANT_MANIFEST_PATH)}`.",
            f"- feature manifest(피처 목록): `{rel(FEATURE_FRAME_MANIFEST_PATH)}`.",
            f"- attempt manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`.",
            f"- route repair inputs(라우팅 수정 입력): `{rel(ROUTE_REPAIR_INPUT_PATH)}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": result["created_at_utc"],
        "sources": result["sources"],
        "outputs": result["outputs"],
        "artifact_hashes": result["artifact_hashes"],
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BC_producer", "producer_script", PRODUCER_PATH, "Builds run267BC adjacent-period materialization."),
        ("stage267_run267BC_period_availability", "period_availability", PERIOD_AVAILABILITY_PATH, "Adjacent-period source availability."),
        ("stage267_run267BC_watch_pair_queue", "experiment_queue", WATCH_PAIR_QUEUE_PATH, "s264_aia adjacent-period watch pair queue."),
        ("stage267_run267BC_feature_frame_manifest", "runtime_feature_manifest", FEATURE_FRAME_MANIFEST_PATH, "Adjacent-period feature frame manifest."),
        ("stage267_run267BC_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 attempt manifest for run267BD execution."),
        ("stage267_run267BC_route_repair_inputs", "route_repair_inputs", ROUTE_REPAIR_INPUT_PATH, "True fallback route manifest repair inputs."),
        ("stage267_run267BC_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BC design receipt."),
        ("stage267_run267BC_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267BC data receipt."),
        ("stage267_run267BC_runtime_parity_receipt", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267BC runtime boundary receipt."),
        ("stage267_run267BC_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BC result judgment."),
        ("stage267_run267BC_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BC gate audit."),
        ("stage267_run267BC_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BC run manifest."),
        ("stage267_run267BC_lineage", "lineage", LINEAGE_PATH, "Run267BC lineage."),
        ("stage267_run267BC_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BC review payload."),
        ("stage267_run267BC_report", "review_report", REPORT_PATH, "Run267BC report."),
    ]
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]
    for row in result["feature_frame_manifest"]:
        path = Path(str(row["runtime_feature_file"]))
        rows.append(
            {
                "artifact_id": f"stage267_run267BC_feature_{safe_token(str(row['queue_id']), 72)}",
                "artifact_type": "runtime_feature_csv",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Adjacent-period runtime feature CSV for {row['queue_id']}.",
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    stage_row = {
        "row_id": "stage267_run267BC_adjacent_period_replacement_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "adjacent_period_replacement_frame_materialization",
        "tier_scope": "Tier A adjacent-period attempt inputs; true fallback blocked",
        "scoreboard": "feature_frames_attempt_manifest_route_repair_inputs",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_new_mt5_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"feature_frames={counts['feature_frames']};attempts={counts['attempts']};next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "adjacent_period_replacement_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={counts['attempts']};selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__adjacent_period_replacement_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "adjacent_period_replacement_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "attempt_input_materialization",
        "tier_scope": "Tier A adjacent periods; true fallback blocked",
        "kpi_scope": "materialization_only_no_new_MT5_KPI",
        "scoreboard_lane": "diagnostic_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"periods={counts['period_rows']};feature_frames={counts['feature_frames']};attempts={counts['attempts']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;true_fallback_blocked",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(str(result["created_at_utc"]), result), key="artifact_id")


def update_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267BC_adjacent_period_replacement_materialization"
        f"(267BC 인접 기간 대체 물질화): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267BC(267BC 실행)는 run267BB(267BB 실행)의 `s264_aia` watch pair(관찰 쌍)를 adjacent-period(인접 기간) MT5 attempt inputs(MT5 시도 입력)로 물질화했다.",
            f"Effect(효과): feature frames(피처 프레임) `{counts['feature_frames']}`개와 attempts(시도) `{counts['attempts']}`개를 만들었지만, MT5 execution(MT5 실행)은 아직 하지 않았으므로 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `adjacent_period_replacement_materialization`")
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267BB_cross_period_replacement_ready_subset_review.md", report_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267BB_cross_period_replacement_ready_subset_review.md", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267BB_cross_period_replacement_ready_subset_review.md", report_line)
        text = append_block_once(text, "Run267BC(267BC 실행)는 run267BB", block)
        write_text(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BC(267BC 실행) adjacent-period replacement materialization(인접 기간 대체 물질화) `{STATUS}`. "
        f"Effect(효과): run267BB(267BB 실행)의 `s264_aia` watch pair(관찰 쌍) 2개를 2023H2/2025H1/2025H2 adjacent period(인접 기간) feature frames(피처 프레임) `{counts['feature_frames']}`개와 MT5 attempts(MT5 시도) `{counts['attempts']}`개로 만들었고, true fallback(실제 대체)은 route manifest(라우팅 목록) 공백 때문에 계속 차단했다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_review.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {source_review.RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {source_review.RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"next_action: {source_review.NEXT_ACTION}", f"next_action: {NEXT_ACTION}")
    workspace = append_after_contains(
        workspace,
        "run267BB_cross_period_replacement_ready_subset_review_report_path",
        f"  run267BC_adjacent_period_replacement_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_text(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(PERIOD_AVAILABILITY_PATH, result["period_availability"])
    write_csv(WATCH_PAIR_QUEUE_PATH, result["watch_pair_queue"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempts"])
    write_csv(ROUTE_REPAIR_INPUT_PATH, result["route_manifest_repair_inputs"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "counts": result["counts"],
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    lineage = build_lineage(result)
    write_json(LINEAGE_PATH, lineage)
    payload = dict(result)
    payload["run_manifest"] = run_manifest
    payload["lineage"] = lineage
    write_json(REVIEW_RESULT_PATH, payload)
    write_text(REPORT_PATH, report_markdown(payload))
    update_ledgers(payload)
    update_docs(payload)


def main() -> int:
    result = build_result()
    write_outputs(result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "run_id": RUN_ID,
                "feature_frames": result["counts"]["feature_frames"],
                "attempts": result["counts"]["attempts"],
                "route_repair_rows": result["counts"]["route_repair_rows"],
                "report": rel(REPORT_PATH),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
