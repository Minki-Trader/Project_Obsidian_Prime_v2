from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

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


FIXTURE_SET_ID = "fixture_fpmarkets_v2_runtime_minimum_0001"
BUNDLE_ID = "bundle_fpmarkets_v2_runtime_minimum_0001"
REPORT_ID = "report_fpmarkets_v2_runtime_parity_0001"
PYTHON_SNAPSHOT_ID = "snapshot_fpmarkets_v2_runtime_python_0001"
MT5_RUNTIME_ID = "runtime_fpmarkets_v2_mt5_snapshot_0001"
FIXTURE_BINDINGS_FILENAME = "fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json"
PYTHON_SNAPSHOT_FILENAME = "python_snapshot_fpmarkets_v2_runtime_minimum_0001.json"
MT5_REQUEST_FILENAME = "mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json"
MT5_WINDOWS_FILENAME = "mt5_target_windows_utc.txt"
HASHES_FILENAME = "artifact_hashes.json"
MT5_AUDIT_TARGET_FILENAME = "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl"
MT5_INPUT_SET_FILENAME = "mt5_snapshot_audit_inputs.set"
MT5_COMMON_FILES_RELATIVE_PATH = (
    "Project_Obsidian_Prime_v2/runtime_parity/runtime_parity_pack_0001/"
    "mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl"
)
RUNTIME_CONTRACT_VERSION = "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize the Stage 03 minimum runtime parity pack.")
    parser.add_argument(
        "--raw-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative root containing raw M5 MT5 bar exports.",
    )
    parser.add_argument(
        "--output-root",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001",
        help="Repo-relative output root for the minimum runtime parity pack artifacts.",
    )
    return parser.parse_args()


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


def find_dst_sensitive_row(valid: pd.DataFrame) -> pd.Series:
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


def serialize_row(
    fixture_id: str,
    row: pd.Series,
    raw_presence: dict[str, set[pd.Timestamp]],
    expected_behavior: str,
    source_role: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "fixture_id": fixture_id,
        "timestamp_utc": iso_z(row["timestamp"]),
        "timestamp_america_new_york": row["timestamp_ny"].isoformat(),
        "valid_row": bool(row["valid_row"]),
        "source_role": source_role,
        "expected_behavior": expected_behavior,
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


def find_negative_row(invalid: pd.DataFrame) -> pd.Series:
    ordered = invalid.sort_values("timestamp")
    common_masks = (
        invalid["invalid__external_alignment_missing"],
        ~invalid["invalid__warmup_incomplete"],
        ~invalid["invalid__main_symbol_missing"],
        ~invalid["invalid__session_semantics_missing"],
        ~invalid["invalid__weights_unavailable"],
    )
    preferred = ordered.loc[
        common_masks[0] & common_masks[1] & common_masks[2] & common_masks[3] & common_masks[4] & ordered["ny_time"].eq("09:35")
    ]
    if not preferred.empty:
        return preferred.iloc[0]
    return choose_row(
        ordered,
        *common_masks,
        label="negative required-missing sample",
    )


def main() -> int:
    args = parse_args()
    raw_root = Path(args.raw_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    base = prepare_base_frame(raw_root)
    raw_presence = build_raw_presence(raw_root)
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
    dst_sensitive_row = find_dst_sensitive_row(valid)
    external_alignment_row = choose_row(
        valid.sort_values("timestamp"),
        valid["ny_time"].eq("15:55"),
        label="external-alignment sample",
    )
    negative_row = find_negative_row(invalid)

    fixture_payload = build_feature_vector_fixture(
        regular_row=regular_row,
        session_boundary_row=session_boundary_row,
        dst_sensitive_row=dst_sensitive_row,
        external_alignment_row=external_alignment_row,
        negative_row=negative_row,
        raw_presence=raw_presence,
    )

    bindings_path = output_root / FIXTURE_BINDINGS_FILENAME
    python_snapshot_path = output_root / PYTHON_SNAPSHOT_FILENAME
    mt5_request_path = output_root / MT5_REQUEST_FILENAME
    mt5_windows_path = output_root / MT5_WINDOWS_FILENAME

    bindings_path.write_text(
        json.dumps(fixture_payload["fixture_bindings"], indent=2),
        encoding="utf-8",
    )
    python_snapshot_path.write_text(
        json.dumps(fixture_payload["python_snapshot"], indent=2),
        encoding="utf-8",
    )
    mt5_request_path.write_text(
        json.dumps(fixture_payload["mt5_request"], indent=2),
        encoding="utf-8",
    )
    mt5_windows_path.write_text(fixture_payload["mt5_window_spec"] + "\n", encoding="utf-8")

    hashes_payload = {
        "fixture_bindings_sha256": sha256_file(bindings_path),
        "python_snapshot_sha256": sha256_file(python_snapshot_path),
        "mt5_request_sha256": sha256_file(mt5_request_path),
        "mt5_windows_sha256": sha256_file(mt5_windows_path),
    }
    (output_root / HASHES_FILENAME).write_text(json.dumps(hashes_payload, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "ok",
                "dataset_id": DATASET_ID,
                "fixture_set_id": FIXTURE_SET_ID,
                "bundle_id": BUNDLE_ID,
                "report_id": REPORT_ID,
                "python_snapshot_id": PYTHON_SNAPSHOT_ID,
                "mt5_runtime_id": MT5_RUNTIME_ID,
                "output_root": str(output_root.resolve()),
                "selected_timestamps": {
                    key: value["timestamp_utc"]
                    for key, value in fixture_payload["fixture_bindings"]["fixtures"].items()
                },
                "hashes": hashes_payload,
            },
            indent=2,
        )
    )
    return 0


def build_feature_vector_fixture(
    regular_row: pd.Series,
    session_boundary_row: pd.Series,
    dst_sensitive_row: pd.Series,
    external_alignment_row: pd.Series,
    negative_row: pd.Series,
    raw_presence: dict[str, set[pd.Timestamp]],
) -> dict[str, Any]:
    regular = serialize_row(
        fixture_id="fix_regular_closed_bar_0001",
        row=regular_row,
        raw_presence=raw_presence,
        expected_behavior="all required inputs present and the row remains runtime-ready on a normal closed-bar sample",
        source_role="python_snapshot",
    )
    session_boundary = serialize_row(
        fixture_id="fix_session_boundary_0001",
        row=session_boundary_row,
        raw_presence=raw_presence,
        expected_behavior="cash-close session flags and minute fields stay exact on the contract surface",
        source_role="python_snapshot",
    )
    dst_sensitive = serialize_row(
        fixture_id="fix_dst_sensitive_0001",
        row=dst_sensitive_row,
        raw_presence=raw_presence,
        expected_behavior="the same contract surface survives a DST transition-week sample without timezone drift",
        source_role="python_snapshot",
    )
    external_alignment = serialize_row(
        fixture_id="fix_external_alignment_0001",
        row=external_alignment_row,
        raw_presence=raw_presence,
        expected_behavior="all required external symbols share the exact US100 closed-bar timestamp",
        source_role="python_snapshot",
    )
    negative = serialize_row(
        fixture_id="fix_negative_required_missing_0001",
        row=negative_row,
        raw_presence=raw_presence,
        expected_behavior="required-missing inputs stay non-ready and no silent substitution is allowed",
        source_role="python_snapshot",
    )

    fixtures = {
        "fix_regular_closed_bar_0001": regular,
        "fix_session_boundary_0001": session_boundary,
        "fix_dst_sensitive_0001": dst_sensitive,
        "fix_external_alignment_0001": external_alignment,
        "fix_negative_required_missing_0001": negative,
    }

    ordered_windows = [
        regular["timestamp_utc"],
        session_boundary["timestamp_utc"],
        dst_sensitive["timestamp_utc"],
        external_alignment["timestamp_utc"],
        negative["timestamp_utc"],
    ]
    mt5_window_spec = ";".join(
        mt5_window_text(pd.Timestamp(ts, tz="UTC")) if isinstance(ts, str) else mt5_window_text(ts)
        for ts in [pd.Timestamp(item) for item in ordered_windows]
    )

    fixture_bindings = {
        "dataset_id": DATASET_ID,
        "fixture_set_id": FIXTURE_SET_ID,
        "bundle_id": BUNDLE_ID,
        "report_id": REPORT_ID,
        "python_snapshot_id": PYTHON_SNAPSHOT_ID,
        "mt5_runtime_id": MT5_RUNTIME_ID,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "runtime_contract_version": RUNTIME_CONTRACT_VERSION,
        "window_start_utc": iso_z(WINDOW_START_UTC),
        "window_end_utc": iso_z(WINDOW_END_UTC),
        "fixtures": fixtures,
    }

    python_snapshot = {
        "dataset_id": DATASET_ID,
        "fixture_set_id": FIXTURE_SET_ID,
        "bundle_id": BUNDLE_ID,
        "report_id": REPORT_ID,
        "source_snapshot_id": PYTHON_SNAPSHOT_ID,
        "parser_version": PARSER_VERSION,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "feature_order": FEATURE_ORDER,
        "fixtures": fixtures,
        "notes": {
            "weights_placeholder": True,
            "mt5_snapshot_status": "pending_mt5_materialization",
            "negative_fixture_includes_feature_vector": False,
        },
    }

    mt5_request = {
        "dataset_id": DATASET_ID,
        "fixture_set_id": FIXTURE_SET_ID,
        "bundle_id": BUNDLE_ID,
        "report_id": REPORT_ID,
        "target_runtime_id": MT5_RUNTIME_ID,
        "parser_version": PARSER_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "runtime_contract_version": RUNTIME_CONTRACT_VERSION,
        "window_start_utc": iso_z(WINDOW_START_UTC),
        "feature_snapshot_audit_use_common_files": True,
        "target_output_path": MT5_COMMON_FILES_RELATIVE_PATH,
        "common_files_output_path": MT5_COMMON_FILES_RELATIVE_PATH,
        "common_files_root_hint": "MetaQuotes/Terminal/Common/Files",
        "repo_import_path": str(
            Path("stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001") / MT5_AUDIT_TARGET_FILENAME
        ).replace("\\", "/"),
        "input_set_path": str(
            Path("stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001") / MT5_INPUT_SET_FILENAME
        ).replace("\\", "/"),
        "target_windows_utc": mt5_window_spec,
        "target_windows_utc_note": "Compatible with the MT5 feature snapshot audit window grammar (semicolon-separated exact UTC timestamps).",
        "fixtures": {
            fixture_id: {
                "timestamp_utc": payload["timestamp_utc"],
                "timestamp_america_new_york": payload["timestamp_america_new_york"],
                "expected_behavior": payload["expected_behavior"],
                "row_ready_expected": payload["valid_row"],
            }
            for fixture_id, payload in fixtures.items()
        },
    }

    return {
        "fixture_bindings": fixture_bindings,
        "python_snapshot": python_snapshot,
        "mt5_request": mt5_request,
        "mt5_window_spec": mt5_window_spec,
    }


if __name__ == "__main__":
    raise SystemExit(main())
