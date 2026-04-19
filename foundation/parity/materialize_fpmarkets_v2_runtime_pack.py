from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from foundation.parity.render_fpmarkets_v2_mt5_snapshot_audit_set import render_set
from foundation.pipelines.materialize_fpmarkets_v2_dataset import (
    DATASET_ID,
    EXPECTED_FEATURE_ORDER_HASH,
    FEATURE_CONTRACT_VERSION,
    FEATURE_ORDER,
    PARSER_CONTRACT_VERSION,
    PARSER_VERSION,
    PRACTICAL_MODELING_START_UTC,
    SYMBOL_BINDINGS,
    WINDOW_END_UTC,
    WINDOW_START_UTC,
    build_feature_frame,
    load_raw_symbol,
)


RUNTIME_CONTRACT_VERSION = "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16"
BUSINESS_WEEKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
REQUIRED_UTC_OFFSETS = {-240, -300}
REPAIR_BUCKET_ORDER = (
    "negative_off_hours_pre_open",
    "negative_off_hours_post_close",
    "full_external_alignment",
    "regular_cash_session",
    "cash_close_boundary_1555",
    "cash_close_boundary_1600",
    "dst_sensitive_utc4",
    "dst_sensitive_utc5",
)
MINIMUM_BINDINGS_SEED_PATH = Path(
    "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/"
    "fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json"
)


@dataclass(frozen=True)
class ProfileConfig:
    name: str
    description: str
    fixture_set_id: str
    bundle_id: str
    report_id: str
    python_snapshot_id: str
    mt5_runtime_id: str
    fixture_bindings_filename: str
    python_snapshot_filename: str
    mt5_request_filename: str
    mt5_windows_filename: str
    hashes_filename: str
    mt5_audit_target_filename: str
    mt5_input_set_filename: str
    mt5_tester_ini_filename: str | None
    mt5_common_files_relative_path: str
    default_output_root: str
    default_inventory_path: str | None
    default_selection_manifest_path: str | None
    repo_import_path: str
    input_set_path: str
    source_stage: str
    emit_mt5_helpers: bool


@dataclass
class SelectedFixture:
    fixture_id: str
    stratum: str
    bucket: str
    expected_behavior: str
    row: pd.Series
    selection_rank: int
    bucket_rank: int


PROFILES = {
    "minimum_0001": ProfileConfig(
        name="minimum_0001",
        description="Materialize the Stage 03 minimum runtime parity pack.",
        fixture_set_id="fixture_fpmarkets_v2_runtime_minimum_0001",
        bundle_id="bundle_fpmarkets_v2_runtime_minimum_0001",
        report_id="report_fpmarkets_v2_runtime_parity_0001",
        python_snapshot_id="snapshot_fpmarkets_v2_runtime_python_0001",
        mt5_runtime_id="runtime_fpmarkets_v2_mt5_snapshot_0001",
        fixture_bindings_filename="fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json",
        python_snapshot_filename="python_snapshot_fpmarkets_v2_runtime_minimum_0001.json",
        mt5_request_filename="mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json",
        mt5_windows_filename="mt5_target_windows_utc.txt",
        hashes_filename="artifact_hashes.json",
        mt5_audit_target_filename="mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl",
        mt5_input_set_filename="mt5_snapshot_audit_inputs.set",
        mt5_tester_ini_filename=None,
        mt5_common_files_relative_path=(
            "Project_Obsidian_Prime_v2/runtime_parity/runtime_parity_pack_0001/"
            "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl"
        ),
        default_output_root="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001",
        default_inventory_path=None,
        default_selection_manifest_path=None,
        repo_import_path=(
            "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/"
            "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl"
        ),
        input_set_path=(
            "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/"
            "mt5_snapshot_audit_inputs.set"
        ),
        source_stage="03_runtime_parity_closure",
        emit_mt5_helpers=False,
    ),
    "broader_0001": ProfileConfig(
        name="broader_0001",
        description="Materialize the first Stage 05 broader-sample runtime parity pack.",
        fixture_set_id="fixture_fpmarkets_v2_runtime_broader_0001",
        bundle_id="bundle_fpmarkets_v2_runtime_broader_0001",
        report_id="report_fpmarkets_v2_runtime_broader_parity_0001",
        python_snapshot_id="snapshot_fpmarkets_v2_runtime_python_broader_0001",
        mt5_runtime_id="runtime_fpmarkets_v2_mt5_snapshot_broader_0001",
        fixture_bindings_filename="fixture_bindings_fpmarkets_v2_runtime_broader_0001.json",
        python_snapshot_filename="python_snapshot_fpmarkets_v2_runtime_broader_0001.json",
        mt5_request_filename="mt5_snapshot_request_fpmarkets_v2_runtime_broader_0001.json",
        mt5_windows_filename="mt5_target_windows_utc.txt",
        hashes_filename="artifact_hashes.json",
        mt5_audit_target_filename="mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0001.jsonl",
        mt5_input_set_filename="mt5_snapshot_audit_inputs.set",
        mt5_tester_ini_filename="mt5_tester_runtime_broader_pack_0001.ini",
        mt5_common_files_relative_path=(
            "Project_Obsidian_Prime_v2/runtime_parity/runtime_broader_pack_0001/"
            "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0001.jsonl"
        ),
        default_output_root="stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0001",
        default_inventory_path="stages/05_exploration_kernel_freeze/01_inputs/first_bound_runtime_broader_fixture_inventory.md",
        default_selection_manifest_path=(
            "stages/05_exploration_kernel_freeze/01_inputs/"
            "first_bound_runtime_broader_fixture_manifest_0001.json"
        ),
        repo_import_path=(
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0001/"
            "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0001.jsonl"
        ),
        input_set_path=(
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0001/"
            "mt5_snapshot_audit_inputs.set"
        ),
        source_stage="05_exploration_kernel_freeze",
        emit_mt5_helpers=True,
    ),
    "broader_0002": ProfileConfig(
        name="broader_0002",
        description="Materialize the contract-aligned Stage 05 broader-sample runtime parity pack after the first mismatch-open evidence pass.",
        fixture_set_id="fixture_fpmarkets_v2_runtime_broader_0002",
        bundle_id="bundle_fpmarkets_v2_runtime_broader_0002",
        report_id="report_fpmarkets_v2_runtime_broader_parity_0002",
        python_snapshot_id="snapshot_fpmarkets_v2_runtime_python_broader_0002",
        mt5_runtime_id="runtime_fpmarkets_v2_mt5_snapshot_broader_0002",
        fixture_bindings_filename="fixture_bindings_fpmarkets_v2_runtime_broader_0002.json",
        python_snapshot_filename="python_snapshot_fpmarkets_v2_runtime_broader_0002.json",
        mt5_request_filename="mt5_snapshot_request_fpmarkets_v2_runtime_broader_0002.json",
        mt5_windows_filename="mt5_target_windows_utc.txt",
        hashes_filename="artifact_hashes.json",
        mt5_audit_target_filename="mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0002.jsonl",
        mt5_input_set_filename="mt5_snapshot_audit_inputs.set",
        mt5_tester_ini_filename="mt5_tester_runtime_broader_pack_0002.ini",
        mt5_common_files_relative_path=(
            "Project_Obsidian_Prime_v2/runtime_parity/runtime_broader_pack_0002/"
            "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0002.jsonl"
        ),
        default_output_root="stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002",
        default_inventory_path="stages/05_exploration_kernel_freeze/01_inputs/second_bound_runtime_broader_fixture_inventory.md",
        default_selection_manifest_path=(
            "stages/05_exploration_kernel_freeze/01_inputs/"
            "second_bound_runtime_broader_fixture_manifest_0002.json"
        ),
        repo_import_path=(
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/"
            "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_broader_0002.jsonl"
        ),
        input_set_path=(
            "stages/05_exploration_kernel_freeze/02_runs/runtime_broader_pack_0002/"
            "mt5_snapshot_audit_inputs.set"
        ),
        source_stage="05_exploration_kernel_freeze",
        emit_mt5_helpers=True,
    ),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize a runtime parity pack for the selected profile.")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="minimum_0001")
    parser.add_argument("--raw-root", default="data/raw/mt5_bars/m5")
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--selection-manifest", default=None)
    parser.add_argument("--inventory-path", default=None)
    parser.add_argument("--force-reselect", action="store_true")
    return parser.parse_args(argv)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def feature_vector_sha256(values: list[float]) -> str:
    vector = np.asarray(values, dtype=np.float32)
    return hashlib.sha256(vector.tobytes()).hexdigest()


def iso_z(timestamp: pd.Timestamp) -> str:
    return timestamp.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")


def mt5_window_text(timestamp: pd.Timestamp) -> str:
    return timestamp.tz_convert("UTC").strftime("%Y.%m.%d %H:%M:%S")


def build_raw_presence(raw_root: Path) -> dict[str, set[pd.Timestamp]]:
    presence: dict[str, set[pd.Timestamp]] = {}
    for binding in SYMBOL_BINDINGS:
        frame = load_raw_symbol(raw_root, binding)
        presence[binding.contract_symbol] = set(frame["timestamp"].tolist())
    return presence


def prepare_base_frame(raw_root: Path) -> pd.DataFrame:
    frame, _ = build_feature_frame(raw_root)
    frame = frame.copy()
    frame["timestamp_ny"] = frame["timestamp"].dt.tz_convert("America/New_York")
    frame["ny_time"] = frame["timestamp_ny"].dt.strftime("%H:%M")
    frame["ny_date"] = frame["timestamp_ny"].dt.date.astype(str)
    frame["month_ny"] = frame["timestamp_ny"].dt.strftime("%Y-%m")
    frame["weekday_ny"] = frame["timestamp_ny"].dt.day_name()
    frame["utc_offset_minutes"] = frame["timestamp_ny"].apply(
        lambda ts: int(ts.utcoffset().total_seconds() // 60)
    )
    return frame


def choose_row(frame: pd.DataFrame, *masks: pd.Series, label: str) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for extra_mask in masks:
        mask &= extra_mask
    matches = frame.loc[mask]
    if matches.empty:
        raise RuntimeError(f"Could not find a candidate row for {label}")
    return matches.iloc[0]


def find_minimum_dst_sensitive_row(valid: pd.DataFrame) -> pd.Series:
    sixteen = valid.loc[valid["ny_time"] == "16:00"].copy()
    sixteen = sixteen.sort_values("timestamp")
    previous_offset = sixteen["utc_offset_minutes"].shift(1)
    changed = sixteen.loc[previous_offset.notna() & (sixteen["utc_offset_minutes"] != previous_offset)]
    changed = changed.loc[changed["timestamp"] >= PRACTICAL_MODELING_START_UTC]
    if changed.empty:
        raise RuntimeError("Could not find a DST-sensitive valid row at 16:00 America/New_York")
    return changed.iloc[0]


def external_match_detail(row: pd.Series, raw_presence: dict[str, set[pd.Timestamp]]) -> dict[str, bool]:
    timestamp = row["timestamp"]
    return {
        binding.contract_symbol: timestamp in raw_presence[binding.contract_symbol]
        for binding in SYMBOL_BINDINGS
        if binding.contract_symbol != "US100"
    }


def build_feature_vector(row: pd.Series) -> list[float]:
    return [float(np.float32(row[name])) for name in FEATURE_ORDER]


def serialize_fixture(
    fixture: SelectedFixture,
    raw_presence: dict[str, set[pd.Timestamp]],
) -> dict[str, Any]:
    row = fixture.row
    payload: dict[str, Any] = {
        "fixture_id": fixture.fixture_id,
        "timestamp_utc": iso_z(row["timestamp"]),
        "timestamp_america_new_york": row["timestamp_ny"].isoformat(),
        "valid_row": bool(row["valid_row"]),
        "source_role": "python_snapshot",
        "expected_behavior": fixture.expected_behavior,
        "selection_stratum": fixture.stratum,
        "selection_bucket": fixture.bucket,
        "selection_rank": fixture.selection_rank,
        "bucket_rank": fixture.bucket_rank,
        "selection_month_ny": str(row["month_ny"]),
        "selection_weekday_ny": str(row["weekday_ny"]),
        "selection_utc_offset_minutes": int(row["utc_offset_minutes"]),
        "session_fields": {
            "is_us_cash_open": float(row["is_us_cash_open"]),
            "minutes_from_cash_open": float(row["minutes_from_cash_open"]),
            "is_first_30m_after_open": float(row["is_first_30m_after_open"]),
            "is_last_30m_before_cash_close": float(row["is_last_30m_before_cash_close"]),
            "overnight_return": None if pd.isna(row["overnight_return"]) else float(row["overnight_return"]),
        },
        "external_timestamp_match": external_match_detail(row, raw_presence),
    }

    invalid_reason_flags = {
        column.removeprefix("invalid__"): bool(row[column])
        for column in row.index
        if column.startswith("invalid__")
    }
    payload["invalid_reason_flags"] = invalid_reason_flags
    payload["missing_external_symbols"] = [
        symbol for symbol, matched in payload["external_timestamp_match"].items() if not matched
    ]

    if payload["valid_row"]:
        feature_vector = build_feature_vector(row)
        payload["feature_vector"] = feature_vector
        payload["feature_vector_sha256"] = feature_vector_sha256(feature_vector)
        payload["feature_count"] = len(feature_vector)
        payload["feature_order_hash"] = EXPECTED_FEATURE_ORDER_HASH
    else:
        payload["feature_vector"] = None
        payload["feature_vector_sha256"] = None
        payload["feature_count"] = 0
        payload["feature_order_hash"] = EXPECTED_FEATURE_ORDER_HASH

    return payload


def select_minimum_fixtures(base: pd.DataFrame) -> list[SelectedFixture]:
    practical = base.loc[base["timestamp"] >= PRACTICAL_MODELING_START_UTC].copy()
    valid = practical.loc[practical["valid_row"]].copy()
    invalid = practical.loc[~practical["valid_row"]].copy()

    regular_row = choose_row(
        valid.sort_values("timestamp"),
        valid["is_us_cash_open"].eq(1.0),
        valid["is_first_30m_after_open"].eq(0.0),
        valid["is_last_30m_before_cash_close"].eq(0.0),
        valid["minutes_from_cash_open"].between(180.0, 240.0),
        label="regular closed-bar sample",
    )
    session_boundary_row = choose_row(
        valid.sort_values("timestamp"),
        valid["ny_time"].eq("16:00"),
        label="session-boundary sample",
    )
    dst_sensitive_row = find_minimum_dst_sensitive_row(valid)
    external_alignment_row = choose_row(
        valid.sort_values("timestamp"),
        valid["ny_time"].eq("15:55"),
        label="external-alignment sample",
    )

    ordered_invalid = invalid.sort_values("timestamp")
    negative_common_masks = (
        invalid["invalid__external_alignment_missing"],
        ~invalid["invalid__warmup_incomplete"],
        ~invalid["invalid__main_symbol_missing"],
        ~invalid["invalid__session_semantics_missing"],
        ~invalid["invalid__weights_unavailable"],
    )
    preferred_negative = ordered_invalid.loc[
        negative_common_masks[0]
        & negative_common_masks[1]
        & negative_common_masks[2]
        & negative_common_masks[3]
        & negative_common_masks[4]
        & ordered_invalid["ny_time"].eq("09:35")
    ]


def fixtures_from_existing_bindings(base: pd.DataFrame, bindings_payload: dict[str, Any]) -> list[SelectedFixture]:
    by_timestamp = {iso_z(row["timestamp"]): row for _, row in base.iterrows()}
    fixtures: list[SelectedFixture] = []
    for selection_rank, (fixture_id, payload) in enumerate(bindings_payload["fixtures"].items(), start=1):
        timestamp_utc = str(payload["timestamp_utc"])
        row = by_timestamp.get(timestamp_utc)
        if row is None:
            raise RuntimeError(f"Frozen fixture timestamp is not present in the materialized frame: {timestamp_utc}")
        fixtures.append(
            SelectedFixture(
                fixture_id=str(fixture_id),
                stratum=str(payload.get("selection_stratum") or fixture_id),
                bucket=str(payload.get("selection_bucket") or fixture_id),
                expected_behavior=str(payload["expected_behavior"]),
                row=row,
                selection_rank=selection_rank,
                bucket_rank=1,
            )
        )
    return fixtures
    if not preferred_negative.empty:
        negative_row = preferred_negative.iloc[0]
    else:
        negative_row = choose_row(
            ordered_invalid,
            *negative_common_masks,
            label="negative required-missing sample",
        )

    return [
        SelectedFixture(
            fixture_id="fix_regular_closed_bar_0001",
            stratum="regular_closed_bar",
            bucket="regular_closed_bar",
            expected_behavior="all required inputs present and the row remains runtime-ready on a normal closed-bar sample",
            row=regular_row,
            selection_rank=1,
            bucket_rank=1,
        ),
        SelectedFixture(
            fixture_id="fix_session_boundary_0001",
            stratum="session_boundary",
            bucket="cash_close_boundary_1600",
            expected_behavior="cash-close session flags and minute fields stay exact on the contract surface",
            row=session_boundary_row,
            selection_rank=2,
            bucket_rank=1,
        ),
        SelectedFixture(
            fixture_id="fix_dst_sensitive_0001",
            stratum="dst_sensitive",
            bucket="dst_sensitive_1600",
            expected_behavior="the same contract surface survives a DST transition-week sample without timezone drift",
            row=dst_sensitive_row,
            selection_rank=3,
            bucket_rank=1,
        ),
        SelectedFixture(
            fixture_id="fix_external_alignment_0001",
            stratum="external_alignment",
            bucket="external_alignment_1555",
            expected_behavior="all required external symbols share the exact US100 closed-bar timestamp",
            row=external_alignment_row,
            selection_rank=4,
            bucket_rank=1,
        ),
        SelectedFixture(
            fixture_id="fix_negative_required_missing_0001",
            stratum="negative_required_missing",
            bucket="negative_cash_open_missing_equities",
            expected_behavior="required-missing inputs stay non-ready and no silent substitution is allowed",
            row=negative_row,
            selection_rank=5,
            bucket_rank=1,
        ),
    ]


def selected_timestamps(fixtures: list[SelectedFixture]) -> set[pd.Timestamp]:
    return {fixture.row["timestamp"] for fixture in fixtures}


def min_day_distance(candidate_row: pd.Series, chosen_rows: list[SelectedFixture]) -> int:
    if not chosen_rows:
        return -1
    current_day = candidate_row["timestamp_ny"].date()
    return min(abs((current_day - fixture.row["timestamp_ny"].date()).days) for fixture in chosen_rows)


def balance_key(
    candidate_row: pd.Series,
    chosen_global: list[SelectedFixture],
    chosen_bucket: list[SelectedFixture],
) -> tuple[int, int, int, int, float]:
    chosen_months = {fixture.row["month_ny"] for fixture in chosen_global}
    chosen_weekdays = {fixture.row["weekday_ny"] for fixture in chosen_global}
    unseen_month = 1 if candidate_row["month_ny"] not in chosen_months else 0
    unseen_weekday = 1 if candidate_row["weekday_ny"] not in chosen_weekdays else 0
    spacing_score = min_day_distance(candidate_row, chosen_bucket)
    business_day = 1 if candidate_row["weekday_ny"] in BUSINESS_WEEKDAYS else 0
    return (
        unseen_month,
        unseen_weekday,
        spacing_score,
        business_day,
        -candidate_row["timestamp"].timestamp(),
    )


def select_bucket_rows(
    bucket_name: str,
    stratum_name: str,
    frame: pd.DataFrame,
    count: int,
    chosen_global: list[SelectedFixture],
    expected_behavior: str,
    fixture_id_prefix: str,
) -> list[SelectedFixture]:
    rows: list[SelectedFixture] = []
    if len(frame) < count:
        raise RuntimeError(f"Bucket {bucket_name} has only {len(frame)} candidates, expected at least {count}.")

    sorted_frame = frame.sort_values("timestamp")
    while len(rows) < count:
        used_timestamps = selected_timestamps(chosen_global) | selected_timestamps(rows)
        available = sorted_frame.loc[~sorted_frame["timestamp"].isin(used_timestamps)]
        if available.empty:
            raise RuntimeError(f"Bucket {bucket_name} ran out of distinct timestamps while selecting.")
        best_row = max(
            (row for _, row in available.iterrows()),
            key=lambda row: balance_key(row, chosen_global, rows),
        )
        rows.append(
            SelectedFixture(
                fixture_id=f"{fixture_id_prefix}{len(rows) + 1:04d}",
                stratum=stratum_name,
                bucket=bucket_name,
                expected_behavior=expected_behavior,
                row=best_row,
                selection_rank=0,
                bucket_rank=len(rows) + 1,
            )
        )
        chosen_global.append(rows[-1])
    return rows


def broader_bucket_candidates(base: pd.DataFrame) -> dict[str, pd.DataFrame]:
    practical = base.loc[base["timestamp"] >= PRACTICAL_MODELING_START_UTC].copy()
    valid = practical.loc[practical["valid_row"]].copy()
    invalid = practical.loc[~practical["valid_row"]].copy()

    boundary_1600 = valid.loc[valid["ny_time"].eq("16:00")].copy().sort_values("timestamp")
    previous_offset = boundary_1600["utc_offset_minutes"].shift(1)
    dst_candidates = boundary_1600.loc[
        previous_offset.notna() & (boundary_1600["utc_offset_minutes"] != previous_offset)
    ].copy()

    shared_negative_mask = (
        invalid["invalid__external_alignment_missing"]
        & ~invalid["invalid__warmup_incomplete"]
        & ~invalid["invalid__main_symbol_missing"]
        & ~invalid["invalid__session_semantics_missing"]
        & ~invalid["invalid__weights_unavailable"]
    )

    return {
        "regular_cash_session": valid.loc[
            valid["is_us_cash_open"].eq(1.0)
            & valid["is_first_30m_after_open"].eq(0.0)
            & valid["is_last_30m_before_cash_close"].eq(0.0)
            & valid["minutes_from_cash_open"].between(180.0, 240.0)
        ].copy(),
        "cash_close_boundary_1555": valid.loc[valid["ny_time"].eq("15:55")].copy(),
        "cash_close_boundary_1600": valid.loc[
            valid["ny_time"].eq("16:00") & ~valid["timestamp"].isin(dst_candidates["timestamp"])
        ].copy(),
        "dst_sensitive_utc4": dst_candidates.loc[dst_candidates["utc_offset_minutes"].eq(-240)].copy(),
        "dst_sensitive_utc5": dst_candidates.loc[dst_candidates["utc_offset_minutes"].eq(-300)].copy(),
        "full_external_alignment": valid.loc[valid["ny_time"].between("14:00", "15:00")].copy(),
        "negative_cash_open_missing_equities": invalid.loc[
            shared_negative_mask & invalid["ny_time"].eq("09:35")
        ].copy(),
        "negative_off_hours_pre_open": invalid.loc[
            shared_negative_mask & (invalid["ny_time"] < "09:35")
        ].copy(),
        "negative_off_hours_post_close": invalid.loc[
            shared_negative_mask & (invalid["ny_time"] > "16:00")
        ].copy(),
    }


def broader_constraint_summary(fixtures: list[SelectedFixture]) -> dict[str, Any]:
    ready_rows = [fixture for fixture in fixtures if bool(fixture.row["valid_row"])]
    negative_rows = [fixture for fixture in fixtures if not bool(fixture.row["valid_row"])]
    months = {fixture.row["month_ny"] for fixture in fixtures}
    weekdays = {fixture.row["weekday_ny"] for fixture in fixtures}
    offsets = {int(fixture.row["utc_offset_minutes"]) for fixture in fixtures}
    bucket_counts: dict[str, int] = {}
    for fixture in fixtures:
        bucket_counts[fixture.bucket] = bucket_counts.get(fixture.bucket, 0) + 1
    return {
        "fixture_count": len(fixtures),
        "ready_count": len(ready_rows),
        "negative_count": len(negative_rows),
        "distinct_month_count": len(months),
        "distinct_weekday_count": len(weekdays),
        "utc_offsets": sorted(offsets),
        "bucket_counts": bucket_counts,
    }


def broader_constraints_met(fixtures: list[SelectedFixture]) -> bool:
    summary = broader_constraint_summary(fixtures)
    return (
        summary["fixture_count"] == 24
        and summary["ready_count"] == 16
        and summary["negative_count"] == 8
        and summary["distinct_month_count"] >= 6
        and summary["distinct_weekday_count"] >= 3
        and REQUIRED_UTC_OFFSETS.issubset(set(summary["utc_offsets"]))
        and summary["bucket_counts"].get("cash_close_boundary_1555") == 2
        and summary["bucket_counts"].get("cash_close_boundary_1600") == 2
        and summary["bucket_counts"].get("dst_sensitive_utc4") == 2
        and summary["bucket_counts"].get("dst_sensitive_utc5") == 2
        and summary["bucket_counts"].get("negative_off_hours_pre_open") == 2
        and summary["bucket_counts"].get("negative_off_hours_post_close") == 2
    )


def broader_score(fixtures: list[SelectedFixture]) -> tuple[int, int, int]:
    summary = broader_constraint_summary(fixtures)
    present_offsets = len(REQUIRED_UTC_OFFSETS.intersection(summary["utc_offsets"]))
    return (
        present_offsets,
        summary["distinct_month_count"],
        summary["distinct_weekday_count"],
    )


def repair_broader_selection(
    selections: dict[str, list[SelectedFixture]],
    candidates: dict[str, pd.DataFrame],
) -> None:
    current = [fixture for rows in selections.values() for fixture in rows]
    if broader_constraints_met(current):
        return

    for _ in range(64):
        if broader_constraints_met(current):
            return

        improved = False
        current_score = broader_score(current)
        for bucket_name in REPAIR_BUCKET_ORDER:
            chosen_bucket = selections[bucket_name]
            candidate_frame = candidates[bucket_name].sort_values("timestamp")
            for replace_index, existing in enumerate(chosen_bucket):
                used_elsewhere = {
                    fixture.row["timestamp"]
                    for name, rows in selections.items()
                    for idx, fixture in enumerate(rows)
                    if not (name == bucket_name and idx == replace_index)
                }
                available = candidate_frame.loc[~candidate_frame["timestamp"].isin(used_elsewhere)]
                for _, candidate_row in available.iterrows():
                    if candidate_row["timestamp"] == existing.row["timestamp"]:
                        continue
                    replacement = SelectedFixture(
                        fixture_id=existing.fixture_id,
                        stratum=existing.stratum,
                        bucket=existing.bucket,
                        expected_behavior=existing.expected_behavior,
                        row=candidate_row,
                        selection_rank=existing.selection_rank,
                        bucket_rank=existing.bucket_rank,
                    )
                    trial: list[SelectedFixture] = []
                    for name, rows in selections.items():
                        if name == bucket_name:
                            trial.extend(
                                replacement if idx == replace_index else row
                                for idx, row in enumerate(rows)
                            )
                        else:
                            trial.extend(rows)
                    trial_score = broader_score(trial)
                    if trial_score > current_score:
                        selections[bucket_name][replace_index] = replacement
                        current = [fixture for rows in selections.values() for fixture in rows]
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
        if not improved:
            break

    current = [fixture for rows in selections.values() for fixture in rows]
    if not broader_constraints_met(current):
        raise RuntimeError(
            "Could not satisfy the broader-sample global coverage constraints after the repair pass."
        )


def select_broader_fixtures(base: pd.DataFrame) -> list[SelectedFixture]:
    candidates = broader_bucket_candidates(base)
    chosen_global: list[SelectedFixture] = []
    selected_by_bucket: dict[str, list[SelectedFixture]] = {}

    selected_by_bucket["regular_cash_session"] = select_bucket_rows(
        bucket_name="regular_cash_session",
        stratum_name="regular_cash_session",
        frame=candidates["regular_cash_session"],
        count=4,
        chosen_global=chosen_global,
        expected_behavior=(
            "all required inputs remain runtime-ready on a normal US cash-session middle-segment sample"
        ),
        fixture_id_prefix="fix_regular_cash_session_",
    )
    selected_by_bucket["cash_close_boundary_1555"] = select_bucket_rows(
        bucket_name="cash_close_boundary_1555",
        stratum_name="cash_close_boundary",
        frame=candidates["cash_close_boundary_1555"],
        count=2,
        chosen_global=chosen_global,
        expected_behavior=(
            "cash-close pre-boundary semantics remain exact on a 15:55 America/New_York contract-surface sample"
        ),
        fixture_id_prefix="fix_cash_close_boundary_1555_",
    )
    selected_by_bucket["cash_close_boundary_1600"] = select_bucket_rows(
        bucket_name="cash_close_boundary_1600",
        stratum_name="cash_close_boundary",
        frame=candidates["cash_close_boundary_1600"],
        count=2,
        chosen_global=chosen_global,
        expected_behavior=(
            "cash-close boundary semantics remain exact on a 16:00 America/New_York contract-surface sample"
        ),
        fixture_id_prefix="fix_cash_close_boundary_1600_",
    )
    selected_by_bucket["dst_sensitive_utc4"] = select_bucket_rows(
        bucket_name="dst_sensitive_utc4",
        stratum_name="dst_sensitive",
        frame=candidates["dst_sensitive_utc4"],
        count=2,
        chosen_global=chosen_global,
        expected_behavior=(
            "the same contract surface survives a DST transition-week 16:00 sample on the UTC-4 side without timezone drift"
        ),
        fixture_id_prefix="fix_dst_sensitive_utc4_",
    )
    selected_by_bucket["dst_sensitive_utc5"] = select_bucket_rows(
        bucket_name="dst_sensitive_utc5",
        stratum_name="dst_sensitive",
        frame=candidates["dst_sensitive_utc5"],
        count=2,
        chosen_global=chosen_global,
        expected_behavior=(
            "the same contract surface survives a DST transition-week 16:00 sample on the UTC-5 side without timezone drift"
        ),
        fixture_id_prefix="fix_dst_sensitive_utc5_",
    )
    selected_by_bucket["full_external_alignment"] = select_bucket_rows(
        bucket_name="full_external_alignment",
        stratum_name="full_external_alignment",
        frame=candidates["full_external_alignment"],
        count=4,
        chosen_global=chosen_global,
        expected_behavior=(
            "all required external symbols exact-timestamp match on a non-boundary afternoon sample"
        ),
        fixture_id_prefix="fix_full_external_alignment_",
    )
    selected_by_bucket["negative_cash_open_missing_equities"] = select_bucket_rows(
        bucket_name="negative_cash_open_missing_equities",
        stratum_name="cash_open_missing_equities",
        frame=candidates["negative_cash_open_missing_equities"],
        count=4,
        chosen_global=chosen_global,
        expected_behavior=(
            "equity external alignment missing keeps the 09:35 cash-open row non-ready under all-or-skip semantics"
        ),
        fixture_id_prefix="fix_negative_cash_open_missing_equities_",
    )
    selected_by_bucket["negative_off_hours_pre_open"] = select_bucket_rows(
        bucket_name="negative_off_hours_pre_open",
        stratum_name="off_hours_external_alignment_missing",
        frame=candidates["negative_off_hours_pre_open"],
        count=2,
        chosen_global=chosen_global,
        expected_behavior=(
            "off-hours external alignment missing keeps the pre-open row non-ready with no reduced substitute"
        ),
        fixture_id_prefix="fix_negative_off_hours_pre_open_",
    )
    selected_by_bucket["negative_off_hours_post_close"] = select_bucket_rows(
        bucket_name="negative_off_hours_post_close",
        stratum_name="off_hours_external_alignment_missing",
        frame=candidates["negative_off_hours_post_close"],
        count=2,
        chosen_global=chosen_global,
        expected_behavior=(
            "off-hours external alignment missing keeps the post-close row non-ready with no reduced substitute"
        ),
        fixture_id_prefix="fix_negative_off_hours_post_close_",
    )

    repair_broader_selection(selected_by_bucket, candidates)

    ordered: list[SelectedFixture] = []
    for bucket_name in (
        "regular_cash_session",
        "cash_close_boundary_1555",
        "cash_close_boundary_1600",
        "dst_sensitive_utc4",
        "dst_sensitive_utc5",
        "full_external_alignment",
        "negative_cash_open_missing_equities",
        "negative_off_hours_pre_open",
        "negative_off_hours_post_close",
    ):
        ordered.extend(selected_by_bucket[bucket_name])

    for index, fixture in enumerate(ordered, start=1):
        fixture.selection_rank = index

    if not broader_constraints_met(ordered):
        raise RuntimeError("The broader-sample selection does not satisfy the frozen charter constraints.")
    return ordered


def broader_selection_manifest(profile: ProfileConfig, fixtures: list[SelectedFixture]) -> dict[str, Any]:
    summary = broader_constraint_summary(fixtures)
    return {
        "profile": profile.name,
        "selection_method": "balance_first_global_and_bucket_greedy_v1",
        "dataset_id": DATASET_ID,
        "fixture_set_id": profile.fixture_set_id,
        "bundle_id": profile.bundle_id,
        "report_id": profile.report_id,
        "python_snapshot_id": profile.python_snapshot_id,
        "target_runtime_id": profile.mt5_runtime_id,
        "parser_version": PARSER_VERSION,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "runtime_contract_version": RUNTIME_CONTRACT_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "selection_constraints": {
            "fixture_count": 24,
            "ready_rows": 16,
            "negative_non_ready_rows": 8,
            "minimum_distinct_months_ny": 6,
            "minimum_distinct_weekdays_ny": 3,
            "required_utc_offsets": sorted(REQUIRED_UTC_OFFSETS),
            "cash_close_boundary_1555_count": 2,
            "cash_close_boundary_1600_count": 2,
            "dst_sensitive_utc4_count": 2,
            "dst_sensitive_utc5_count": 2,
            "negative_off_hours_pre_open_count": 2,
            "negative_off_hours_post_close_count": 2,
        },
        "selection_coverage": {
            "distinct_month_count_ny": summary["distinct_month_count"],
            "distinct_weekday_count_ny": summary["distinct_weekday_count"],
            "utc_offsets_present": summary["utc_offsets"],
            "bucket_counts": summary["bucket_counts"],
        },
        "fixtures": [
            {
                "fixture_id": fixture.fixture_id,
                "selection_rank": fixture.selection_rank,
                "bucket_rank": fixture.bucket_rank,
                "stratum": fixture.stratum,
                "bucket": fixture.bucket,
                "timestamp_utc": iso_z(fixture.row["timestamp"]),
                "timestamp_america_new_york": fixture.row["timestamp_ny"].isoformat(),
                "month_ny": str(fixture.row["month_ny"]),
                "weekday_ny": str(fixture.row["weekday_ny"]),
                "utc_offset_minutes": int(fixture.row["utc_offset_minutes"]),
                "valid_row": bool(fixture.row["valid_row"]),
                "expected_behavior": fixture.expected_behavior,
            }
            for fixture in fixtures
        ],
    }


def validate_broader_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    fixtures = list(manifest.get("fixtures") or [])
    if len(fixtures) != 24:
        raise RuntimeError(f"Expected 24 broader fixtures, found {len(fixtures)}.")

    timestamps = [fixture["timestamp_utc"] for fixture in fixtures]
    if len(set(timestamps)) != 24:
        raise RuntimeError("The broader manifest does not contain 24 distinct timestamps.")

    ready_count = sum(1 for fixture in fixtures if bool(fixture["valid_row"]))
    negative_count = len(fixtures) - ready_count
    if ready_count != 16 or negative_count != 8:
        raise RuntimeError(
            f"Expected 16 ready rows and 8 negative rows, found {ready_count} ready and {negative_count} negative."
        )

    months = {fixture["month_ny"] for fixture in fixtures}
    weekdays = {fixture["weekday_ny"] for fixture in fixtures}
    offsets = {int(fixture["utc_offset_minutes"]) for fixture in fixtures}
    if len(months) < 6:
        raise RuntimeError("The broader manifest does not meet the six-month minimum.")
    if len(weekdays) < 3:
        raise RuntimeError("The broader manifest does not meet the three-weekday minimum.")
    if not REQUIRED_UTC_OFFSETS.issubset(offsets):
        raise RuntimeError("The broader manifest does not cover both UTC-4 and UTC-5.")

    bucket_counts: dict[str, int] = {}
    for fixture in fixtures:
        bucket = str(fixture["bucket"])
        bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1

    expected_bucket_counts = {
        "regular_cash_session": 4,
        "cash_close_boundary_1555": 2,
        "cash_close_boundary_1600": 2,
        "dst_sensitive_utc4": 2,
        "dst_sensitive_utc5": 2,
        "full_external_alignment": 4,
        "negative_cash_open_missing_equities": 4,
        "negative_off_hours_pre_open": 2,
        "negative_off_hours_post_close": 2,
    }
    for bucket, expected_count in expected_bucket_counts.items():
        actual_count = bucket_counts.get(bucket, 0)
        if actual_count != expected_count:
            raise RuntimeError(f"Bucket {bucket} expected {expected_count} fixtures, found {actual_count}.")

    return {
        "fixture_count": len(fixtures),
        "ready_count": ready_count,
        "negative_count": negative_count,
        "distinct_month_count_ny": len(months),
        "distinct_weekday_count_ny": len(weekdays),
        "utc_offsets_present": sorted(offsets),
        "bucket_counts": bucket_counts,
    }


def fixtures_from_manifest(base: pd.DataFrame, manifest: dict[str, Any]) -> list[SelectedFixture]:
    by_timestamp = {iso_z(row["timestamp"]): row for _, row in base.iterrows()}
    fixtures: list[SelectedFixture] = []
    for payload in manifest["fixtures"]:
        timestamp_utc = str(payload["timestamp_utc"])
        row = by_timestamp.get(timestamp_utc)
        if row is None:
            raise RuntimeError(f"Manifest timestamp is not present in the materialized frame: {timestamp_utc}")
        if bool(row["valid_row"]) != bool(payload["valid_row"]):
            raise RuntimeError(f"Manifest ready-state mismatch for {payload['fixture_id']}: {timestamp_utc}")
        fixtures.append(
            SelectedFixture(
                fixture_id=str(payload["fixture_id"]),
                stratum=str(payload["stratum"]),
                bucket=str(payload["bucket"]),
                expected_behavior=str(payload["expected_behavior"]),
                row=row,
                selection_rank=int(payload["selection_rank"]),
                bucket_rank=int(payload["bucket_rank"]),
            )
        )
    return fixtures


def render_broader_inventory(
    profile: ProfileConfig,
    fixtures: list[SelectedFixture],
    manifest_repo_path: str,
    python_snapshot_relative_ref: str,
    run_root_name: str,
) -> str:
    summary = broader_constraint_summary(fixtures)
    lines = [
        "# Bound Runtime Broader Fixture Inventory",
        "",
        "## Identity",
        "",
        f"- profile: `{profile.name}`",
        f"- fixture_set_id: `{profile.fixture_set_id}`",
        "- created_on: `2026-04-19`",
        "- owner: `Project_Obsidian_Prime_v2 workspace`",
        f"- dataset_id: `{DATASET_ID}`",
        f"- bundle_id: `{profile.bundle_id}`",
        f"- python_snapshot_id: `{profile.python_snapshot_id}`",
        f"- target_mt5_runtime_id: `{profile.mt5_runtime_id}`",
        f"- report_id: `{profile.report_id}`",
        "",
        "## Contract Versions",
        "",
        f"- feature_contract_version: `{FEATURE_CONTRACT_VERSION}`",
        f"- parser_version: `{PARSER_VERSION}`",
        f"- parser_contract_version: `{PARSER_CONTRACT_VERSION}`",
        f"- runtime_contract_version: `{RUNTIME_CONTRACT_VERSION}`",
        f"- feature_order_hash: `{EXPECTED_FEATURE_ORDER_HASH}`",
        "",
        "## Coverage Summary",
        "",
        "- pack_type: `fixed stratified audit pack`",
        f"- fixture_count: `{summary['fixture_count']}`",
        f"- ready_rows: `{summary['ready_count']}`",
        f"- negative_non_ready_rows: `{summary['negative_count']}`",
        f"- distinct_month_count_ny: `{summary['distinct_month_count']}`",
        f"- distinct_weekday_count_ny: `{summary['distinct_weekday_count']}`",
        f"- utc_offsets_present: `{', '.join(str(value) for value in summary['utc_offsets'])}`",
        f"- selection_manifest_ref: `{manifest_repo_path}`",
        "",
    ]

    grouped: dict[str, list[SelectedFixture]] = {}
    for fixture in fixtures:
        grouped.setdefault(fixture.stratum, []).append(fixture)

    headings = (
        "regular_cash_session",
        "cash_close_boundary",
        "dst_sensitive",
        "full_external_alignment",
        "cash_open_missing_equities",
        "off_hours_external_alignment_missing",
    )
    for heading in headings:
        if heading not in grouped:
            continue
        lines.extend([f"## {heading}", ""])
        for fixture in grouped[heading]:
            lines.append(f"### {fixture.fixture_id}")
            lines.append(f"- stratum: `{fixture.stratum}`")
            lines.append(f"- bucket: `{fixture.bucket}`")
            lines.append(f"- evaluated_timestamp_utc: `{iso_z(fixture.row['timestamp'])}`")
            lines.append(f"- evaluated_timestamp_america_new_york: `{fixture.row['timestamp_ny'].isoformat()}`")
            lines.append(f"- month_ny: `{fixture.row['month_ny']}`")
            lines.append(f"- weekday_ny: `{fixture.row['weekday_ny']}`")
            lines.append(f"- utc_offset_minutes: `{int(fixture.row['utc_offset_minutes'])}`")
            lines.append(f"- expected_row_ready: `{bool(fixture.row['valid_row'])}`")
            lines.append(f"- expected_contract_behavior: `{fixture.expected_behavior}`")
            lines.append(f"- source_artifact_ref: `{python_snapshot_relative_ref}`")
            lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- known_caveats: `this broader-sample fixture inventory, selection manifest, Python snapshot, MT5 request, and MT5 helper pack are materialized, but the MT5 snapshot export, comparison summary, and rendered broader parity report remain pending the paired evaluation pass`",
            f"- mt5_request_ref: `../02_runs/{run_root_name}/{profile.mt5_request_filename}`",
            f"- mt5_window_spec_ref: `../02_runs/{run_root_name}/{profile.mt5_windows_filename}`",
            f"- selection_manifest_ref: `{manifest_repo_path}`",
            "- reuse_guidance: `this inventory now freezes the selected Stage 05 broader-sample twenty-four-window pack; the paired MT5 snapshot export and parity comparison must reuse these same timestamps and ids rather than sampling a new window set`",
            "",
        ]
    )
    return "\n".join(lines)


def render_tester_ini(
    mt5_request: dict[str, Any],
    tester_ini_path: Path,
    fixtures: list[SelectedFixture],
) -> str:
    tester_inputs = [
        line
        for line in render_set(mt5_request).splitlines()
        if line and not line.startswith(";")
    ]
    max_timestamp_ny = max(fixture.row["timestamp_ny"] for fixture in fixtures)
    to_date = (max_timestamp_ny.normalize() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")
    report_stem = tester_ini_path.with_suffix("")
    lines = [
        "[Tester]",
        r"Expert=Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeParityAuditEA.ex5",
        "Symbol=US100",
        "Period=M5",
        "Optimization=0",
        "Model=4",
        "Dates=1",
        f"FromDate={WINDOW_START_UTC.strftime('%Y.%m.%d')}",
        f"ToDate={to_date}",
        "ForwardMode=0",
        "Deposit=500",
        "Currency=USD",
        "ProfitInPips=0",
        "Leverage=100",
        "ExecutionMode=0",
        "OptimizationCriterion=0",
        "Visual=0",
        f"Report={report_stem.resolve()}",
        "ReplaceReport=1",
        "ShutdownTerminal=1",
        "",
        "[TesterInputs]",
        *tester_inputs,
        "",
    ]
    return "\n".join(lines)


def build_runtime_payload(
    profile: ProfileConfig,
    fixtures: list[SelectedFixture],
    raw_presence: dict[str, set[pd.Timestamp]],
) -> dict[str, Any]:
    serialized = {
        fixture.fixture_id: serialize_fixture(fixture=fixture, raw_presence=raw_presence)
        for fixture in fixtures
    }

    ordered_windows = [payload["timestamp_utc"] for payload in serialized.values()]
    mt5_window_spec = ";".join(mt5_window_text(pd.Timestamp(item)) for item in ordered_windows)

    fixture_bindings = {
        "dataset_id": DATASET_ID,
        "fixture_set_id": profile.fixture_set_id,
        "bundle_id": profile.bundle_id,
        "report_id": profile.report_id,
        "python_snapshot_id": profile.python_snapshot_id,
        "mt5_runtime_id": profile.mt5_runtime_id,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "runtime_contract_version": RUNTIME_CONTRACT_VERSION,
        "window_start_utc": iso_z(WINDOW_START_UTC),
        "window_end_utc": iso_z(WINDOW_END_UTC),
        "fixtures": serialized,
    }

    python_snapshot = {
        "dataset_id": DATASET_ID,
        "fixture_set_id": profile.fixture_set_id,
        "bundle_id": profile.bundle_id,
        "report_id": profile.report_id,
        "source_snapshot_id": profile.python_snapshot_id,
        "parser_version": PARSER_VERSION,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "feature_order": FEATURE_ORDER,
        "fixtures": serialized,
        "notes": {
            "weights_placeholder": True,
            "mt5_snapshot_status": "pending_mt5_materialization",
            "negative_fixture_includes_feature_vector": False,
            "profile": profile.name,
        },
    }

    mt5_request = {
        "dataset_id": DATASET_ID,
        "fixture_set_id": profile.fixture_set_id,
        "bundle_id": profile.bundle_id,
        "report_id": profile.report_id,
        "target_runtime_id": profile.mt5_runtime_id,
        "parser_version": PARSER_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "runtime_contract_version": RUNTIME_CONTRACT_VERSION,
        "window_start_utc": iso_z(WINDOW_START_UTC),
        "feature_snapshot_audit_use_common_files": True,
        "target_output_path": profile.mt5_common_files_relative_path,
        "common_files_output_path": profile.mt5_common_files_relative_path,
        "common_files_root_hint": "MetaQuotes/Terminal/Common/Files",
        "repo_import_path": profile.repo_import_path,
        "input_set_path": profile.input_set_path,
        "target_windows_utc": mt5_window_spec,
        "target_windows_utc_note": "Compatible with the MT5 feature snapshot audit window grammar (semicolon-separated exact UTC timestamps).",
        "fixtures": {
            fixture_id: {
                "timestamp_utc": payload["timestamp_utc"],
                "timestamp_america_new_york": payload["timestamp_america_new_york"],
                "expected_behavior": payload["expected_behavior"],
                "row_ready_expected": payload["valid_row"],
                "selection_stratum": payload.get("selection_stratum"),
                "selection_bucket": payload.get("selection_bucket"),
            }
            for fixture_id, payload in serialized.items()
        },
    }

    return {
        "fixture_bindings": fixture_bindings,
        "python_snapshot": python_snapshot,
        "mt5_request": mt5_request,
        "mt5_window_spec": mt5_window_spec,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_runtime_pack(
    profile: ProfileConfig,
    output_root: Path,
    payload: dict[str, Any],
    fixtures: list[SelectedFixture],
) -> dict[str, str]:
    output_root.mkdir(parents=True, exist_ok=True)

    bindings_path = output_root / profile.fixture_bindings_filename
    python_snapshot_path = output_root / profile.python_snapshot_filename
    mt5_request_path = output_root / profile.mt5_request_filename
    mt5_windows_path = output_root / profile.mt5_windows_filename

    write_json(bindings_path, payload["fixture_bindings"])
    write_json(python_snapshot_path, payload["python_snapshot"])
    write_json(mt5_request_path, payload["mt5_request"])
    mt5_windows_path.write_text(payload["mt5_window_spec"] + "\n", encoding="utf-8")

    hashes_payload = {
        "fixture_bindings_sha256": sha256_file(bindings_path),
        "python_snapshot_sha256": sha256_file(python_snapshot_path),
        "mt5_request_sha256": sha256_file(mt5_request_path),
        "mt5_windows_sha256": sha256_file(mt5_windows_path),
    }
    write_json(output_root / profile.hashes_filename, hashes_payload)

    generated_paths = {
        "fixture_bindings_path": str(bindings_path.resolve()),
        "python_snapshot_path": str(python_snapshot_path.resolve()),
        "mt5_request_path": str(mt5_request_path.resolve()),
        "mt5_windows_path": str(mt5_windows_path.resolve()),
        "artifact_hashes_path": str((output_root / profile.hashes_filename).resolve()),
    }

    if profile.emit_mt5_helpers and profile.mt5_tester_ini_filename is not None:
        mt5_request = payload["mt5_request"]
        input_set_path = output_root / profile.mt5_input_set_filename
        tester_ini_path = output_root / profile.mt5_tester_ini_filename
        input_set_path.write_text(render_set(mt5_request), encoding="utf-8")
        tester_ini_path.write_text(
            render_tester_ini(
                mt5_request=mt5_request,
                tester_ini_path=tester_ini_path,
                fixtures=fixtures,
            ),
            encoding="utf-8",
        )
        hashes_payload["mt5_input_set_sha256"] = sha256_file(input_set_path)
        hashes_payload["mt5_tester_ini_sha256"] = sha256_file(tester_ini_path)
        write_json(output_root / profile.hashes_filename, hashes_payload)
        generated_paths["mt5_input_set_path"] = str(input_set_path.resolve())
        generated_paths["mt5_tester_ini_path"] = str(tester_ini_path.resolve())

    return generated_paths


def broader_selection_materialize(
    profile: ProfileConfig,
    raw_root: Path,
    base: pd.DataFrame,
    manifest_path: Path,
    inventory_path: Path,
    output_root: Path,
    force_reselect: bool,
) -> tuple[list[SelectedFixture], dict[str, Any]]:
    if manifest_path.exists() and not force_reselect:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_broader_manifest(manifest)
        fixtures = fixtures_from_manifest(base=base, manifest=manifest)
    else:
        fixtures = select_broader_fixtures(base)
        manifest = broader_selection_manifest(profile, fixtures)
        validate_broader_manifest(manifest)
        write_json(manifest_path, manifest)

    raw_presence = build_raw_presence(raw_root)
    payload = build_runtime_payload(profile=profile, fixtures=fixtures, raw_presence=raw_presence)
    generated_paths = write_runtime_pack(profile=profile, output_root=output_root, payload=payload, fixtures=fixtures)

    run_root_name = output_root.name
    inventory_markdown = render_broader_inventory(
        profile=profile,
        fixtures=fixtures,
        manifest_repo_path=manifest_path.as_posix(),
        python_snapshot_relative_ref=f"../02_runs/{run_root_name}/{profile.python_snapshot_filename}",
        run_root_name=run_root_name,
    )
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(inventory_markdown, encoding="utf-8")

    summary = {
        "selection_manifest_path": str(manifest_path.resolve()),
        "inventory_path": str(inventory_path.resolve()),
        **generated_paths,
        "selection_coverage": validate_broader_manifest(
            json.loads(manifest_path.read_text(encoding="utf-8"))
        ),
    }
    return fixtures, summary


def materialize_runtime_pack(
    profile_name: str,
    raw_root: Path,
    output_root: Path | None = None,
    selection_manifest_path: Path | None = None,
    inventory_path: Path | None = None,
    force_reselect: bool = False,
) -> dict[str, Any]:
    if profile_name not in PROFILES:
        raise RuntimeError(f"Unknown runtime pack profile: {profile_name}")
    profile = PROFILES[profile_name]
    output_root = output_root or Path(profile.default_output_root)
    base = prepare_base_frame(raw_root)

    if profile_name == "minimum_0001":
        raw_presence = build_raw_presence(raw_root)
        if MINIMUM_BINDINGS_SEED_PATH.exists():
            seed_payload = json.loads(MINIMUM_BINDINGS_SEED_PATH.read_text(encoding="utf-8"))
            fixtures = fixtures_from_existing_bindings(base, seed_payload)
        else:
            fixtures = select_minimum_fixtures(base)
        payload = build_runtime_payload(profile=profile, fixtures=fixtures, raw_presence=raw_presence)
        generated_paths = write_runtime_pack(profile=profile, output_root=output_root, payload=payload, fixtures=fixtures)
        return {
            "status": "ok",
            "profile": profile.name,
            "dataset_id": DATASET_ID,
            "fixture_set_id": profile.fixture_set_id,
            "bundle_id": profile.bundle_id,
            "report_id": profile.report_id,
            "python_snapshot_id": profile.python_snapshot_id,
            "mt5_runtime_id": profile.mt5_runtime_id,
            "output_root": str(output_root.resolve()),
            "selected_timestamps": {
                fixture.fixture_id: iso_z(fixture.row["timestamp"])
                for fixture in fixtures
            },
            "generated_paths": generated_paths,
        }

    manifest_path = selection_manifest_path or Path(profile.default_selection_manifest_path or "")
    inventory_path = inventory_path or Path(profile.default_inventory_path or "")
    if not manifest_path:
        raise RuntimeError("The broader runtime profile requires a selection manifest path.")
    if not inventory_path:
        raise RuntimeError("The broader runtime profile requires an inventory path.")

    fixtures, summary = broader_selection_materialize(
        profile=profile,
        raw_root=raw_root,
        base=base,
        manifest_path=manifest_path,
        inventory_path=inventory_path,
        output_root=output_root,
        force_reselect=force_reselect,
    )
    return {
        "status": "ok",
        "profile": profile.name,
        "dataset_id": DATASET_ID,
        "fixture_set_id": profile.fixture_set_id,
        "bundle_id": profile.bundle_id,
        "report_id": profile.report_id,
        "python_snapshot_id": profile.python_snapshot_id,
        "mt5_runtime_id": profile.mt5_runtime_id,
        "output_root": str(output_root.resolve()),
        "selected_timestamps": {
            fixture.fixture_id: iso_z(fixture.row["timestamp"])
            for fixture in fixtures
        },
        "generated_paths": summary,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = materialize_runtime_pack(
        profile_name=args.profile,
        raw_root=Path(args.raw_root),
        output_root=Path(args.output_root) if args.output_root else None,
        selection_manifest_path=Path(args.selection_manifest) if args.selection_manifest else None,
        inventory_path=Path(args.inventory_path) if args.inventory_path else None,
        force_reselect=bool(args.force_reselect),
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
