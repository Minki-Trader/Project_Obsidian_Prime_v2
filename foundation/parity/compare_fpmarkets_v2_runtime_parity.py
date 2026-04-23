from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from foundation.parity.runtime_pack_paths import DEFAULT_MT5_REQUEST, resolve_runtime_pack_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare a materialized Python runtime snapshot against an MT5 feature snapshot audit export."
    )
    parser.add_argument(
        "--python-snapshot",
        default=None,
        help="Repo-relative path to the materialized Python runtime snapshot JSON.",
    )
    parser.add_argument(
        "--mt5-request",
        default=str(DEFAULT_MT5_REQUEST),
        help="Repo-relative path to the MT5 request pack JSON.",
    )
    parser.add_argument(
        "--mt5-snapshot",
        default=None,
        help="Repo-relative path to the MT5 feature snapshot audit JSONL export.",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Repo-relative path for the comparison summary JSON.",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-5,
        help="Absolute tolerance for ready-row feature comparisons.",
    )
    parser.add_argument(
        "--summary-json",
        default=None,
        help="Optional path to write the structured step summary JSON.",
    )
    return parser.parse_args()


def read_text_robust(path: Path) -> str:
    payload = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode text from {path}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text_robust(path))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(read_text_robust(path).splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive parsing guard
            raise RuntimeError(f"Invalid JSONL at line {line_number} in {path}: {exc}") from exc
        payload["_jsonl_line_number"] = line_number
        records.append(payload)
    return records


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def feature_order_hash(feature_names: list[str]) -> str:
    payload = "\n".join(feature_names).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def parse_time_as_utc(value: str) -> datetime | None:
    text = value.strip()
    if not text:
        return None

    if text.endswith("Z"):
        try:
            return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        except ValueError:
            pass

    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y.%m.%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            parsed = datetime.strptime(text, fmt)
        except ValueError:
            continue
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
    return None


def normalize_utc_text(value: str | None) -> str | None:
    if value is None:
        return None
    parsed = parse_time_as_utc(value)
    if parsed is None:
        return None
    return parsed.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def iso_to_window_text(value: str) -> str:
    parsed = parse_time_as_utc(value)
    if parsed is None:
        raise RuntimeError(f"Could not parse timestamp as UTC: {value}")
    return parsed.astimezone(UTC).strftime("%Y.%m.%d %H:%M:%S")


def unique_non_empty(values: list[str | None]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value is None:
            continue
        text = value.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return ordered


def canonical_symbol_key(symbol: str) -> str:
    text = symbol.strip().upper()
    if text.endswith(".XNAS"):
        return text[:-5]
    return text


def canonicalize_match_map(match_map: dict[str, bool]) -> dict[str, bool]:
    canonical: dict[str, bool] = {}
    for symbol, matched in match_map.items():
        canonical[canonical_symbol_key(symbol)] = bool(matched)
    return canonical


def extract_mt5_features(record: dict[str, Any]) -> tuple[list[str], list[float], list[dict[str, Any]]]:
    raw_features = record.get("features")
    if not isinstance(raw_features, list):
        return [], [], []

    feature_names: list[str] = []
    feature_values: list[float] = []
    normalized_entries: list[dict[str, Any]] = []

    for index, entry in enumerate(raw_features):
        if isinstance(entry, dict):
            name = str(entry.get("name", f"feature_{index}"))
            value = float(entry.get("value", 0.0))
            normalized_entries.append(
                {
                    "index": int(entry.get("index", index)),
                    "name": name,
                    "value": value,
                }
            )
            feature_names.append(name)
            feature_values.append(value)
            continue

        value = float(entry)
        name = f"feature_{index}"
        normalized_entries.append({"index": index, "name": name, "value": value})
        feature_names.append(name)
        feature_values.append(value)

    return feature_names, feature_values, normalized_entries


def extract_requested_close_iso(record: dict[str, Any]) -> tuple[str | None, list[str]]:
    raw_inputs = record.get("external_inputs")
    if not isinstance(raw_inputs, list):
        return None, []

    requested_values = unique_non_empty(
        [
            normalize_utc_text(item.get("requested_close_utc"))
            for item in raw_inputs
            if isinstance(item, dict)
        ]
    )
    if len(requested_values) == 1:
        return requested_values[0], requested_values
    return None, requested_values


def external_match_map(record: dict[str, Any]) -> dict[str, bool]:
    raw_inputs = record.get("external_inputs")
    if not isinstance(raw_inputs, list):
        return {}

    matches: dict[str, bool] = {}
    for item in raw_inputs:
        if not isinstance(item, dict):
            continue
        symbol = str(item.get("symbol", "")).strip()
        if not symbol:
            continue

        requested_iso = normalize_utc_text(item.get("requested_close_utc"))
        selected_iso = normalize_utc_text(item.get("selected_close_utc"))
        fallback_used = bool(item.get("fallback_used", False))
        status = str(item.get("status", "")).strip().upper()
        matches[symbol] = (
            requested_iso is not None
            and selected_iso is not None
            and requested_iso == selected_iso
            and not fallback_used
            and "MISS" not in status
            and "FAIL" not in status
            and "STALE" not in status
        )
    return matches


def argmax_label(probabilities: tuple[float, float, float] | None) -> str | None:
    if probabilities is None:
        return None
    p_short, p_flat, p_long = probabilities
    if p_short >= p_flat and p_short >= p_long:
        return "SHORT"
    if p_flat >= p_short and p_flat >= p_long:
        return "FLAT"
    return "LONG"


def extract_probabilities(record: dict[str, Any]) -> tuple[float, float, float] | None:
    keys = ("p_short", "p_flat", "p_long")
    if not all(key in record for key in keys):
        return None
    try:
        return tuple(float(record[key]) for key in keys)  # type: ignore[return-value]
    except (TypeError, ValueError):
        return None


def build_expected_maps(fixtures: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
    by_timestamp: dict[str, str] = {}
    by_window_text: dict[str, str] = {}
    for fixture_id, payload in fixtures.items():
        timestamp_utc = str(payload["timestamp_utc"])
        by_timestamp[timestamp_utc] = fixture_id
        by_window_text[iso_to_window_text(timestamp_utc)] = fixture_id
    return by_timestamp, by_window_text


def normalize_mt5_record(record: dict[str, Any]) -> dict[str, Any]:
    feature_names, feature_values, feature_entries = extract_mt5_features(record)
    requested_close_iso, raw_requested_closes = extract_requested_close_iso(record)
    timestamp_candidates = unique_non_empty(
        [
            normalize_utc_text(record.get("timestamp_utc")),
            normalize_utc_text(record.get("bar_time_utc")),
            normalize_utc_text(record.get("event_timestamp_utc")),
            requested_close_iso,
        ]
    )

    bar_time_server = str(record.get("bar_time_server", "")).strip() or None
    return {
        "raw": record,
        "line_number": record.get("_jsonl_line_number"),
        "fixture_id": str(record.get("fixture_id", "")).strip() or None,
        "timestamp_candidates": timestamp_candidates,
        "requested_close_candidates": raw_requested_closes,
        "bar_time_server": bar_time_server,
        "feature_names": feature_names,
        "feature_values": feature_values,
        "feature_entries": feature_entries,
        "derived_feature_order_hash": feature_order_hash(feature_names) if feature_names else None,
        "feature_count": int(record.get("feature_count", len(feature_values) or 0)),
        "feature_vector_complete": bool(record.get("feature_vector_complete", False)),
        "feature_fingerprint": record.get("feature_fingerprint"),
        "row_ready": bool(record.get("row_ready", False)),
        "skip_reason": str(record.get("skip_reason", "")).strip(),
        "decision": str(record.get("decision", "")).strip() or None,
        "decision_reason": str(record.get("decision_reason", "")).strip() or None,
        "probabilities": extract_probabilities(record),
        "external_match_map": external_match_map(record),
    }


def match_mt5_records(
    fixtures: dict[str, Any],
    mt5_records: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[str]]:
    expected_by_timestamp, expected_by_window_text = build_expected_maps(fixtures)
    matched: dict[str, dict[str, Any]] = {}
    unexpected: list[dict[str, Any]] = []
    warnings: list[str] = []

    for record in mt5_records:
        fixture_id: str | None = None
        matched_by: str | None = None

        explicit_fixture_id = record["fixture_id"]
        if explicit_fixture_id in fixtures and explicit_fixture_id not in matched:
            fixture_id = explicit_fixture_id
            matched_by = "fixture_id"

        if fixture_id is None:
            for candidate in record["timestamp_candidates"]:
                if candidate in expected_by_timestamp and expected_by_timestamp[candidate] not in matched:
                    fixture_id = expected_by_timestamp[candidate]
                    matched_by = "timestamp_candidate"
                    break

        if fixture_id is None and record["bar_time_server"] in expected_by_window_text:
            candidate_fixture = expected_by_window_text[record["bar_time_server"]]
            if candidate_fixture not in matched:
                fixture_id = candidate_fixture
                matched_by = "bar_time_server_text"
                warnings.append(
                    f"{candidate_fixture} was matched by raw bar_time_server text because no explicit UTC identity field was available."
                )

        if fixture_id is None:
            unexpected.append(record)
            continue

        if fixture_id in matched:
            unexpected.append(record)
            warnings.append(f"Duplicate MT5 snapshot record detected for {fixture_id}.")
            continue

        record["matched_fixture_id"] = fixture_id
        record["matched_by"] = matched_by
        matched[fixture_id] = record

    return matched, unexpected, warnings


def compare_feature_vectors(
    expected_fixture: dict[str, Any],
    expected_feature_order: list[str],
    mt5_record: dict[str, Any],
    tolerance: float,
) -> dict[str, Any]:
    expected_vector = expected_fixture.get("feature_vector")
    if expected_vector is None:
        return {
            "feature_vector_compared": False,
            "feature_name_order_match": mt5_record["feature_names"] == expected_feature_order if mt5_record["feature_names"] else None,
            "derived_feature_order_hash": mt5_record["derived_feature_order_hash"],
            "feature_count_expected": 0,
            "feature_count_actual": mt5_record["feature_count"],
            "exact_match": None,
            "tolerance_match": None,
            "max_abs_diff": None,
            "features_over_tolerance_count": None,
            "zero_shift_share": None,
            "top_abs_diffs": [],
        }

    actual_values = mt5_record["feature_values"]
    compare_count = min(len(expected_vector), len(actual_values))
    abs_diffs: list[tuple[int, str, float, float, float]] = []
    zero_shift_count = 0
    exact_match = len(expected_vector) == len(actual_values)
    tolerance_match = len(expected_vector) == len(actual_values)

    for index in range(compare_count):
        expected_value = float(expected_vector[index])
        actual_value = float(actual_values[index])
        abs_diff = abs(actual_value - expected_value)
        name = expected_feature_order[index] if index < len(expected_feature_order) else f"feature_{index}"
        abs_diffs.append((index, name, expected_value, actual_value, abs_diff))
        exact_match = exact_match and actual_value == expected_value
        tolerance_match = tolerance_match and abs_diff <= tolerance
        if abs_diff == 0.0:
            zero_shift_count += 1

    if len(expected_vector) != len(actual_values):
        exact_match = False
        tolerance_match = False

    top_abs_diffs = [
        {
            "index": index,
            "name": name,
            "expected": expected_value,
            "actual": actual_value,
            "abs_diff": abs_diff,
        }
        for index, name, expected_value, actual_value, abs_diff in sorted(abs_diffs, key=lambda item: item[4], reverse=True)[:5]
    ]

    max_abs_diff = max((item[4] for item in abs_diffs), default=0.0)
    features_over_tolerance_count = sum(1 for item in abs_diffs if item[4] > tolerance)
    return {
        "feature_vector_compared": True,
        "feature_name_order_match": mt5_record["feature_names"] == expected_feature_order,
        "derived_feature_order_hash": mt5_record["derived_feature_order_hash"],
        "feature_count_expected": len(expected_vector),
        "feature_count_actual": mt5_record["feature_count"],
        "exact_match": exact_match,
        "tolerance_match": tolerance_match,
        "max_abs_diff": max_abs_diff,
        "features_over_tolerance_count": features_over_tolerance_count,
        "zero_shift_share": zero_shift_count / compare_count if compare_count else None,
        "top_abs_diffs": top_abs_diffs,
    }


def compare_external_alignment(expected_fixture: dict[str, Any], mt5_record: dict[str, Any]) -> dict[str, Any]:
    expected_match_map = canonicalize_match_map(expected_fixture.get("external_timestamp_match") or {})
    actual_match_map = canonicalize_match_map(mt5_record["external_match_map"])
    if not expected_match_map or not actual_match_map:
        return {
            "compared": False,
            "exact_match": None,
            "expected_missing_symbols": expected_fixture.get("missing_external_symbols", []),
            "actual_missing_symbols": [],
            "mismatched_symbols": [],
        }

    expected_missing_symbols = sorted(symbol for symbol, matched in expected_match_map.items() if not matched)
    actual_missing_symbols = sorted(symbol for symbol, matched in actual_match_map.items() if not matched)
    symbols = sorted(set(expected_match_map) | set(actual_match_map))
    mismatched_symbols = [
        symbol
        for symbol in symbols
        if expected_match_map.get(symbol) != actual_match_map.get(symbol)
    ]
    return {
        "compared": True,
        "exact_match": len(mismatched_symbols) == 0,
        "expected_missing_symbols": expected_missing_symbols,
        "actual_missing_symbols": actual_missing_symbols,
        "mismatched_symbols": mismatched_symbols,
    }


def negative_fixture_skip_match(expected_fixture: dict[str, Any], mt5_record: dict[str, Any]) -> bool | None:
    if expected_fixture.get("valid_row", True):
        return None

    skip_reason = mt5_record["skip_reason"].upper()
    if expected_fixture.get("invalid_reason_flags", {}).get("external_alignment_missing"):
        return skip_reason.startswith("EXTERNAL_") or "EXTERNAL" in skip_reason
    return len(skip_reason) > 0


def build_identity_summary(
    python_snapshot: dict[str, Any],
    mt5_request: dict[str, Any],
    mt5_records: list[dict[str, Any]],
    python_snapshot_path: Path,
    mt5_request_path: Path,
    mt5_snapshot_path: Path,
) -> dict[str, Any]:
    expected = {
        "dataset_id": python_snapshot.get("dataset_id"),
        "fixture_set_id": python_snapshot.get("fixture_set_id"),
        "bundle_id": python_snapshot.get("bundle_id"),
        "report_id": python_snapshot.get("report_id"),
        "runtime_id": mt5_request.get("target_runtime_id"),
        "parser_version": python_snapshot.get("parser_version"),
        "feature_contract_version": python_snapshot.get("feature_contract_version"),
        "runtime_contract_version": mt5_request.get("runtime_contract_version"),
        "feature_order_hash": python_snapshot.get("feature_order_hash"),
    }

    tracked_fields = (
        "dataset_id",
        "fixture_set_id",
        "bundle_id",
        "report_id",
        "runtime_id",
        "parser_version",
        "feature_contract_version",
        "runtime_contract_version",
        "feature_order_hash",
    )

    mt5_identity_values = {
        field: unique_non_empty(
            [
                None if record["raw"].get(field) is None else str(record["raw"].get(field))
                for record in mt5_records
            ]
        )
        for field in tracked_fields
    }
    mt5_identity_fields_present = {
        field: any(field in record["raw"] for record in mt5_records)
        for field in tracked_fields
    }
    mt5_identity_matches = {
        field: (len(values) == 1 and values[0] == str(expected[field])) if expected[field] is not None else None
        for field, values in mt5_identity_values.items()
    }
    request_consistency = {
        "dataset_id_match": mt5_request.get("dataset_id") == expected["dataset_id"],
        "fixture_set_id_match": mt5_request.get("fixture_set_id") == expected["fixture_set_id"],
        "bundle_id_match": mt5_request.get("bundle_id") == expected["bundle_id"],
        "report_id_match": mt5_request.get("report_id") == expected["report_id"],
        "parser_version_match": mt5_request.get("parser_version") == expected["parser_version"],
        "feature_contract_version_match": mt5_request.get("feature_contract_version") == expected["feature_contract_version"],
        "runtime_contract_version_match": mt5_request.get("runtime_contract_version") == expected["runtime_contract_version"],
        "feature_order_hash_match": mt5_request.get("feature_order_hash") == expected["feature_order_hash"],
    }
    machine_readable_identity_trace = {
        "request_consistent": all(bool(value) for value in request_consistency.values()),
        "mt5_fields_present": all(bool(value) for value in mt5_identity_fields_present.values()),
        "mt5_values_match": all(bool(value) for value in mt5_identity_matches.values()),
    }
    machine_readable_identity_trace["traceable"] = all(machine_readable_identity_trace.values())

    return {
        "expected": expected,
        "request_consistency": request_consistency,
        "mt5_identity_fields_present": mt5_identity_fields_present,
        "mt5_identity_values": mt5_identity_values,
        "mt5_identity_matches": mt5_identity_matches,
        "machine_readable_identity_trace": machine_readable_identity_trace,
        "artifact_hashes": {
            "python_snapshot_sha256": sha256_file(python_snapshot_path),
            "mt5_request_sha256": sha256_file(mt5_request_path),
            "mt5_snapshot_sha256": sha256_file(mt5_snapshot_path),
        },
    }


def main() -> int:
    args = parse_args()
    resolved_paths = resolve_runtime_pack_paths(
        Path(args.mt5_request),
        python_snapshot_path=Path(args.python_snapshot) if args.python_snapshot else None,
        mt5_snapshot_path=Path(args.mt5_snapshot) if args.mt5_snapshot else None,
        comparison_json_path=Path(args.output_json) if args.output_json else None,
    )
    python_snapshot_path = resolved_paths.python_snapshot_path
    mt5_request_path = resolved_paths.mt5_request_path
    mt5_snapshot_path = resolved_paths.mt5_snapshot_path
    output_json_path = resolved_paths.comparison_json_path

    python_snapshot = load_json(python_snapshot_path)
    mt5_request = resolved_paths.mt5_request
    mt5_raw_records = load_jsonl(mt5_snapshot_path)
    mt5_records = [normalize_mt5_record(record) for record in mt5_raw_records]

    fixtures = dict(python_snapshot["fixtures"])
    expected_feature_order = list(python_snapshot["feature_order"])
    expected_feature_order_hash = str(python_snapshot["feature_order_hash"])

    matched_records, unexpected_records, matching_warnings = match_mt5_records(fixtures, mt5_records)
    missing_fixture_ids = [fixture_id for fixture_id in fixtures if fixture_id not in matched_records]

    fixture_results: dict[str, Any] = {}
    ready_fixture_exact_match_count = 0
    ready_fixture_tolerance_match_count = 0
    ready_fixture_count = 0
    non_ready_fixture_match_count = 0
    compared_feature_rows = 0
    features_over_tolerance_count = 0
    zero_shift_shares: list[float] = []
    max_abs_diff = 0.0
    warnings = list(matching_warnings)

    for fixture_id, expected_fixture in fixtures.items():
        mt5_record = matched_records.get(fixture_id)
        if mt5_record is None:
            fixture_results[fixture_id] = {
                "status": "missing_mt5_record",
                "expected_timestamp_utc": expected_fixture["timestamp_utc"],
                "expected_row_ready": expected_fixture["valid_row"],
            }
            continue

        row_ready_match = mt5_record["row_ready"] == bool(expected_fixture["valid_row"])
        negative_skip_reason_match = negative_fixture_skip_match(expected_fixture, mt5_record)
        feature_comparison = compare_feature_vectors(
            expected_fixture=expected_fixture,
            expected_feature_order=expected_feature_order,
            mt5_record=mt5_record,
            tolerance=args.tolerance,
        )
        external_alignment = compare_external_alignment(expected_fixture, mt5_record)

        if expected_fixture["valid_row"]:
            ready_fixture_count += 1
            compared_feature_rows += 1
            if feature_comparison["exact_match"]:
                ready_fixture_exact_match_count += 1
            if (
                feature_comparison["tolerance_match"]
                and row_ready_match
                and bool(feature_comparison["feature_name_order_match"])
                and external_alignment["exact_match"] is not False
            ):
                ready_fixture_tolerance_match_count += 1
            if feature_comparison["zero_shift_share"] is not None:
                zero_shift_shares.append(float(feature_comparison["zero_shift_share"]))
            if feature_comparison["max_abs_diff"] is not None:
                max_abs_diff = max(max_abs_diff, float(feature_comparison["max_abs_diff"]))
            if feature_comparison["features_over_tolerance_count"] is not None:
                features_over_tolerance_count += int(feature_comparison["features_over_tolerance_count"])
        else:
            if row_ready_match and negative_skip_reason_match is not False:
                non_ready_fixture_match_count += 1

        derived_order_hash_match = (
            feature_comparison["derived_feature_order_hash"] == expected_feature_order_hash
            if feature_comparison["derived_feature_order_hash"] is not None
            else None
        )
        if feature_comparison["feature_name_order_match"] is False:
            warnings.append(f"{fixture_id} feature name order differs from the Python snapshot order.")
        if external_alignment["exact_match"] is False:
            warnings.append(f"{fixture_id} external timestamp alignment differs between Python and MT5 evidence.")
        if not row_ready_match:
            warnings.append(f"{fixture_id} row_ready differs between Python and MT5 evidence.")

        fixture_results[fixture_id] = {
            "status": "matched",
            "matched_by": mt5_record.get("matched_by"),
            "mt5_jsonl_line_number": mt5_record["line_number"],
            "expected_timestamp_utc": expected_fixture["timestamp_utc"],
            "mt5_timestamp_candidates": mt5_record["timestamp_candidates"],
            "mt5_requested_close_candidates": mt5_record["requested_close_candidates"],
            "mt5_bar_time_server": mt5_record["bar_time_server"],
            "expected_row_ready": expected_fixture["valid_row"],
            "actual_row_ready": mt5_record["row_ready"],
            "row_ready_match": row_ready_match,
            "skip_reason": mt5_record["skip_reason"],
            "negative_skip_reason_match": negative_skip_reason_match,
            "feature_vector_complete": mt5_record["feature_vector_complete"],
            "feature_name_order_match": feature_comparison["feature_name_order_match"],
            "derived_feature_order_hash": feature_comparison["derived_feature_order_hash"],
            "derived_feature_order_hash_match": derived_order_hash_match,
            "external_alignment": external_alignment,
            "feature_comparison": feature_comparison,
            "decision": {
                "decision": mt5_record["decision"],
                "decision_reason": mt5_record["decision_reason"],
                "probabilities": mt5_record["probabilities"],
                "argmax_class": argmax_label(mt5_record["probabilities"]),
            },
        }

    exact_parity = (
        len(missing_fixture_ids) == 0
        and len(unexpected_records) == 0
        and ready_fixture_exact_match_count == ready_fixture_count
        and non_ready_fixture_match_count == sum(1 for fixture in fixtures.values() if not fixture["valid_row"])
    )
    tolerance_parity = (
        len(missing_fixture_ids) == 0
        and len(unexpected_records) == 0
        and ready_fixture_tolerance_match_count == ready_fixture_count
        and non_ready_fixture_match_count == sum(1 for fixture in fixtures.values() if not fixture["valid_row"])
    )

    summary = {
        "status": "ok",
        "identity": build_identity_summary(
            python_snapshot=python_snapshot,
            mt5_request=mt5_request,
            mt5_records=mt5_records,
            python_snapshot_path=python_snapshot_path,
            mt5_request_path=mt5_request_path,
            mt5_snapshot_path=mt5_snapshot_path,
        ),
        "comparison_contract": {
            "tolerance_abs": args.tolerance,
            "feature_count_expected": len(expected_feature_order),
            "feature_order_hash_expected": expected_feature_order_hash,
        },
        "matching": {
            "fixture_count_expected": len(fixtures),
            "fixture_count_matched": len(matched_records),
            "missing_fixture_ids": missing_fixture_ids,
            "unexpected_record_count": len(unexpected_records),
            "unexpected_record_lines": [record["line_number"] for record in unexpected_records],
        },
        "aggregate_results": {
            "ready_fixture_count_expected": ready_fixture_count,
            "ready_fixture_exact_match_count": ready_fixture_exact_match_count,
            "ready_fixture_tolerance_match_count": ready_fixture_tolerance_match_count,
            "non_ready_fixture_match_count": non_ready_fixture_match_count,
            "features_over_tolerance_count": features_over_tolerance_count,
            "max_abs_diff": max_abs_diff if compared_feature_rows > 0 else None,
            "zero_shift_share_mean": (sum(zero_shift_shares) / len(zero_shift_shares)) if zero_shift_shares else None,
            "exact_parity": exact_parity,
            "tolerance_parity": tolerance_parity,
        },
        "fixtures": fixture_results,
        "warnings": warnings,
    }

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    step_summary = {
        "status": "ok",
        "output_json": str(output_json_path.resolve()),
        "matched_fixtures": len(matched_records),
        "missing_fixtures": missing_fixture_ids,
        "unexpected_record_count": len(unexpected_records),
        "exact_parity": exact_parity,
        "tolerance_parity": tolerance_parity,
        "max_abs_diff": summary["aggregate_results"]["max_abs_diff"],
    }
    if args.summary_json:
        summary_path = Path(args.summary_json)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(step_summary, indent=2), encoding="utf-8")
    print(json.dumps(step_summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
