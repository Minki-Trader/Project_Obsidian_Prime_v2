from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.pipelines.materialize_fpmarkets_v2_dataset import (  # noqa: E402
    BROKER_CLOCK_TIMEZONE,
    EXPECTED_FEATURE_ORDER_HASH,
    FEATURE_CONTRACT_VERSION,
    FEATURE_ORDER,
    PARSER_CONTRACT_VERSION,
    PARSER_VERSION,
    PRACTICAL_MODELING_START_UTC,
    RAW_TIME_AXIS_POLICY,
    SESSION_TIME_POLICY_STATUS,
    SESSION_TIMEZONE,
    TIME_AXIS_POLICY_VERSION,
    WARMUP_BARS,
    WINDOW_END_UTC,
    build_feature_frame,
    feature_order_hash,
    sha256_file,
)


FREEZE_MATERIALIZER_VERSION = "fpmarkets_v2_stage02_feature_frame_freeze_v1"
US100_SYMBOL = "US100"


@dataclass(frozen=True)
class FreezeSelectionSpec:
    target_id: str
    start_utc: pd.Timestamp
    row_scope: str
    session_scope: str
    day_scope: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize a selected feature-frame freeze.")
    parser.add_argument(
        "--raw-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative root containing raw M5 MT5 bar exports.",
    )
    parser.add_argument(
        "--dataset-id",
        required=True,
        help="Durable dataset identity for the selected freeze.",
    )
    parser.add_argument(
        "--output-root",
        default=None,
        help="Repo-relative output root for the selected freeze. Defaults to data/processed/datasets/<dataset-id>.",
    )
    parser.add_argument("--target-id", required=True, help="Selection target identity.")
    parser.add_argument("--start-utc", required=True, help="Inclusive UTC selection start.")
    parser.add_argument(
        "--row-scope",
        default="valid_row_only",
        help="Row-scope selector. Current supported value: valid_row_only.",
    )
    parser.add_argument(
        "--session-scope",
        default="cash_open_rows_only",
        help="Session-scope selector. Current supported value: cash_open_rows_only.",
    )
    parser.add_argument(
        "--day-scope",
        default="full_cash_session_days_only",
        help="Day-scope selector. Current supported value: full_cash_session_days_only.",
    )
    parser.add_argument(
        "--weights-path",
        default=None,
        help="Optional repo-relative top3 monthly weights CSV.",
    )
    parser.add_argument(
        "--weights-version-label",
        default=None,
        help="Optional durable label for the supplied weights source.",
    )
    return parser.parse_args()


def parse_utc_timestamp(value: str) -> pd.Timestamp:
    parsed = pd.Timestamp(value)
    if parsed.tzinfo is None:
        parsed = parsed.tz_localize("UTC")
    return parsed.tz_convert("UTC")


def build_cash_day_table(frame: pd.DataFrame) -> pd.DataFrame:
    cash = frame.loc[frame["is_us_cash_open"].fillna(0).eq(1), ["timestamp", "timestamp_ny"]].copy()
    cash["date_ny"] = cash["timestamp_ny"].dt.strftime("%Y-%m-%d")
    day_table = cash.groupby("date_ny").agg(
        cash_row_count=("timestamp", "size"),
        first_cash_timestamp=("timestamp", "min"),
        last_cash_timestamp=("timestamp", "max"),
    )
    day_table["is_full_cash_day"] = day_table["cash_row_count"] == 78
    return day_table


def attach_day_flags(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    working = frame.copy()
    working["date_ny"] = working["timestamp_ny"].dt.strftime("%Y-%m-%d")
    day_table = build_cash_day_table(working)
    working = working.merge(
        day_table[["cash_row_count", "is_full_cash_day"]],
        left_on="date_ny",
        right_index=True,
        how="left",
    )
    working["cash_row_count"] = working["cash_row_count"].fillna(0).astype(int)
    working["is_full_cash_day"] = working["is_full_cash_day"].eq(True)
    return working, day_table


def _window_invalid_breakdown(window_frame: pd.DataFrame) -> dict[str, int]:
    reason_columns = sorted(column for column in window_frame.columns if column.startswith("invalid__"))
    return {
        column.removeprefix("invalid__"): int(window_frame[column].astype(bool).sum())
        for column in reason_columns
    }


def select_freeze_rows(
    frame: pd.DataFrame,
    counts: dict[str, object],
    selection: FreezeSelectionSpec,
) -> dict[str, object]:
    if selection.row_scope != "valid_row_only":
        raise ValueError(f"Unsupported row_scope: {selection.row_scope}")
    if selection.session_scope != "cash_open_rows_only":
        raise ValueError(f"Unsupported session_scope: {selection.session_scope}")
    if selection.day_scope != "full_cash_session_days_only":
        raise ValueError(f"Unsupported day_scope: {selection.day_scope}")

    flagged_frame, day_table = attach_day_flags(frame)
    window_mask = flagged_frame["timestamp"] >= selection.start_utc
    window_frame = flagged_frame.loc[window_mask].copy()
    window_raw_rows = int(len(window_frame))
    window_valid_rows = int(window_frame["valid_row"].astype(bool).sum())
    window_invalid_rows = int((~window_frame["valid_row"].astype(bool)).sum())

    cash_window_frame = window_frame.loc[window_frame["is_us_cash_open"].fillna(0).eq(1)].copy()
    candidate_mask = window_mask & flagged_frame["valid_row"].astype(bool)
    candidate_mask &= flagged_frame["is_us_cash_open"].fillna(0).eq(1)
    candidate_frame = flagged_frame.loc[candidate_mask].copy()

    selected_mask = candidate_mask & flagged_frame["is_full_cash_day"].astype(bool)
    selected_frame = flagged_frame.loc[selected_mask].copy().sort_values("timestamp").reset_index(drop=True)

    eligible_full_cash_day_count = int(
        cash_window_frame.loc[cash_window_frame["is_full_cash_day"].astype(bool), "date_ny"].nunique()
    )
    selected_valid_row_ny_days = int(selected_frame["date_ny"].nunique())
    excluded_partial_cash_days = int(
        cash_window_frame.loc[~cash_window_frame["is_full_cash_day"].astype(bool), "date_ny"].nunique()
    )
    excluded_partial_day_valid_rows = int(len(candidate_frame) - len(selected_frame))

    if selected_frame["timestamp"].duplicated().any():
        raise RuntimeError("Duplicate timestamps detected in selected freeze rows.")
    if not selected_frame["timestamp"].is_monotonic_increasing:
        raise RuntimeError("Selected freeze timestamps are not monotonic increasing.")

    return {
        "frame": flagged_frame,
        "day_table": day_table,
        "window_frame": window_frame,
        "selected_frame": selected_frame,
        "selection_summary": {
            "target_id": selection.target_id,
            "start_utc": selection.start_utc.isoformat(),
            "row_scope": selection.row_scope,
            "session_scope": selection.session_scope,
            "day_scope": selection.day_scope,
            "window_raw_rows": window_raw_rows,
            "window_valid_rows": window_valid_rows,
            "window_invalid_rows": window_invalid_rows,
            "window_invalid_reason_breakdown": _window_invalid_breakdown(window_frame),
            "candidate_cash_open_valid_rows": int(len(candidate_frame)),
            "selected_rows": int(len(selected_frame)),
            "eligible_full_cash_day_count": eligible_full_cash_day_count,
            "selected_valid_row_ny_days": selected_valid_row_ny_days,
            "excluded_partial_cash_days": excluded_partial_cash_days,
            "excluded_partial_day_valid_rows": excluded_partial_day_valid_rows,
            "first_selected_timestamp": selected_frame["timestamp"].iloc[0].isoformat() if len(selected_frame) else None,
            "last_selected_timestamp": selected_frame["timestamp"].iloc[-1].isoformat() if len(selected_frame) else None,
            "weights_version": counts["weights_version"],
            "raw_time_axis_policy": counts["raw_time_axis_policy"],
            "session_time_policy_status": counts["session_time_policy_status"],
            "broker_clock_timezone": counts["broker_clock_timezone"],
            "session_timezone": counts["session_timezone"],
        },
    }


def write_selected_freeze_outputs(
    *,
    output_root: Path,
    dataset_id: str,
    selected_frame: pd.DataFrame,
    selection_summary: dict[str, object],
    source_identities: list[dict[str, object]],
) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    current_feature_hash = feature_order_hash()
    if current_feature_hash != EXPECTED_FEATURE_ORDER_HASH:
        raise RuntimeError(
            f"Feature order hash mismatch: {current_feature_hash} != {EXPECTED_FEATURE_ORDER_HASH}"
        )

    features_path = output_root / "features.parquet"
    summary_path = output_root / "dataset_summary.json"
    validity_path = output_root / "row_validity_report.json"
    feature_order_path = output_root / "feature_order.txt"
    parser_manifest_path = output_root / "parser_manifest.json"
    selection_path = output_root / "freeze_selection.json"
    merge_report_path = output_root / "external_merge_report.json"
    debug_rows_path = output_root / "sample_debug_rows.csv"

    export_frame = selected_frame.loc[:, ["timestamp"] + FEATURE_ORDER].copy()
    export_frame["symbol"] = US100_SYMBOL
    export_frame = export_frame[["timestamp", "symbol"] + FEATURE_ORDER]
    export_frame[FEATURE_ORDER] = export_frame[FEATURE_ORDER].astype("float32")
    export_frame.to_parquet(features_path, index=False)

    row_validity_payload = {
        "dataset_id": dataset_id,
        "window_start": selection_summary["start_utc"],
        "window_end_inclusive": WINDOW_END_UTC.isoformat(),
        "raw_rows": selection_summary["window_raw_rows"],
        "valid_rows": selection_summary["window_valid_rows"],
        "invalid_rows": selection_summary["window_invalid_rows"],
        "invalid_reason_breakdown": selection_summary["window_invalid_reason_breakdown"],
        "selected_rows": selection_summary["selected_rows"],
        "target_id": selection_summary["target_id"],
        "row_scope": selection_summary["row_scope"],
        "session_scope": selection_summary["session_scope"],
        "day_scope": selection_summary["day_scope"],
        "eligible_full_cash_day_count": selection_summary["eligible_full_cash_day_count"],
        "selected_valid_row_ny_days": selection_summary["selected_valid_row_ny_days"],
        "excluded_partial_cash_days": selection_summary["excluded_partial_cash_days"],
        "excluded_partial_day_valid_rows": selection_summary["excluded_partial_day_valid_rows"],
        "raw_time_axis_policy": selection_summary["raw_time_axis_policy"],
        "session_time_policy_status": selection_summary["session_time_policy_status"],
        "broker_clock_timezone": selection_summary["broker_clock_timezone"],
        "session_timezone": selection_summary["session_timezone"],
    }
    validity_path.write_text(json.dumps(row_validity_payload, indent=2), encoding="utf-8")

    summary_payload = {
        "dataset_id": dataset_id,
        "parser_version": PARSER_VERSION,
        "freeze_materializer_version": FREEZE_MATERIALIZER_VERSION,
        "feature_count": len(FEATURE_ORDER),
        "feature_order_hash": current_feature_hash,
        "feature_order_sha256": current_feature_hash,
        "window_start": selection_summary["start_utc"],
        "window_end_inclusive": WINDOW_END_UTC.isoformat(),
        "practical_modeling_start": PRACTICAL_MODELING_START_UTC.isoformat(),
        "warmup_bars": WARMUP_BARS,
        "preload_policy": (
            "300 bars minimum; practical modeling start remains 2022-09-01; "
            "selected freeze keeps valid cash-open rows on full cash-session days only"
        ),
        "weights_version": selection_summary["weights_version"],
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
        "raw_rows": selection_summary["window_raw_rows"],
        "valid_rows": selection_summary["window_valid_rows"],
        "invalid_rows": selection_summary["window_invalid_rows"],
        "invalid_reason_breakdown": selection_summary["window_invalid_reason_breakdown"],
        "source_identities": source_identities,
        "raw_time_axis_policy": selection_summary["raw_time_axis_policy"],
        "session_time_policy_status": selection_summary["session_time_policy_status"],
        "broker_clock_timezone": selection_summary["broker_clock_timezone"],
        "session_timezone": selection_summary["session_timezone"],
        "selection_target_id": selection_summary["target_id"],
        "selection_row_scope": selection_summary["row_scope"],
        "selection_session_scope": selection_summary["session_scope"],
        "selection_day_scope": selection_summary["day_scope"],
        "selected_rows": selection_summary["selected_rows"],
        "eligible_full_cash_day_count": selection_summary["eligible_full_cash_day_count"],
        "selected_valid_row_ny_days": selection_summary["selected_valid_row_ny_days"],
        "excluded_partial_cash_days": selection_summary["excluded_partial_cash_days"],
        "excluded_partial_day_valid_rows": selection_summary["excluded_partial_day_valid_rows"],
        "first_selected_timestamp": selection_summary["first_selected_timestamp"],
        "last_selected_timestamp": selection_summary["last_selected_timestamp"],
    }
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    feature_order_path.write_text("\n".join(FEATURE_ORDER), encoding="utf-8")
    parser_manifest_path.write_text(
        json.dumps(
            {
                "dataset_id": dataset_id,
                "parser_version": PARSER_VERSION,
                "freeze_materializer_version": FREEZE_MATERIALIZER_VERSION,
                "feature_contract_version": FEATURE_CONTRACT_VERSION,
                "parser_contract_version": PARSER_CONTRACT_VERSION,
                "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
                "feature_order_hash": current_feature_hash,
                "raw_root": "data/raw/mt5_bars/m5",
                "output_root": str(output_root.as_posix()),
                "selection": {
                    "target_id": selection_summary["target_id"],
                    "start_utc": selection_summary["start_utc"],
                    "row_scope": selection_summary["row_scope"],
                    "session_scope": selection_summary["session_scope"],
                    "day_scope": selection_summary["day_scope"],
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    selection_path.write_text(json.dumps(selection_summary, indent=2), encoding="utf-8")
    merge_report_path.write_text(
        json.dumps({"dataset_id": dataset_id, "source_identities": source_identities}, indent=2),
        encoding="utf-8",
    )

    debug_columns = [
        "timestamp",
        "timestamp_event_utc",
        "timestamp_ny",
        "date_ny",
        "valid_row",
        "is_us_cash_open",
        "cash_row_count",
        "is_full_cash_day",
    ] + FEATURE_ORDER[:6]
    debug_frame = selected_frame.loc[:, debug_columns].copy()
    for column in ("timestamp", "timestamp_event_utc", "timestamp_ny"):
        debug_frame[column] = pd.to_datetime(debug_frame[column]).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    debug_frame.head(200).to_csv(debug_rows_path, index=False)

    hashes = {
        "features_parquet_sha256": sha256_file(features_path),
        "dataset_summary_sha256": sha256_file(summary_path),
        "row_validity_report_sha256": sha256_file(validity_path),
        "freeze_selection_sha256": sha256_file(selection_path),
        "parser_manifest_sha256": sha256_file(parser_manifest_path),
    }
    return {
        "output_root": str(output_root.as_posix()),
        "hashes": hashes,
        "summary_path": str(summary_path.as_posix()),
        "features_path": str(features_path.as_posix()),
        "row_validity_path": str(validity_path.as_posix()),
        "freeze_selection_path": str(selection_path.as_posix()),
    }


def materialize_selected_freeze(
    *,
    raw_root: Path,
    output_root: Path,
    dataset_id: str,
    selection: FreezeSelectionSpec,
    weights_path: Path | None = None,
    weights_version_label: str | None = None,
) -> dict[str, object]:
    frame, counts = build_feature_frame(
        raw_root,
        weights_path=weights_path,
        weights_version_label=weights_version_label,
    )
    selection_payload = select_freeze_rows(frame, counts, selection)
    write_payload = write_selected_freeze_outputs(
        output_root=output_root,
        dataset_id=dataset_id,
        selected_frame=selection_payload["selected_frame"],
        selection_summary=selection_payload["selection_summary"],
        source_identities=counts["source_identities"],
    )
    return {
        "status": "ok",
        "dataset_id": dataset_id,
        "selection": selection_payload["selection_summary"],
        "artifacts": write_payload,
        "raw_time_axis_policy": counts["raw_time_axis_policy"],
        "session_time_policy_status": counts["session_time_policy_status"],
    }


def main() -> int:
    args = parse_args()
    selection = FreezeSelectionSpec(
        target_id=args.target_id,
        start_utc=parse_utc_timestamp(args.start_utc),
        row_scope=args.row_scope,
        session_scope=args.session_scope,
        day_scope=args.day_scope,
    )
    output_root = (
        Path(args.output_root)
        if args.output_root is not None
        else Path("data/processed/datasets") / args.dataset_id
    )
    payload = materialize_selected_freeze(
        raw_root=Path(args.raw_root),
        output_root=output_root,
        dataset_id=args.dataset_id,
        selection=selection,
        weights_path=Path(args.weights_path) if args.weights_path else None,
        weights_version_label=args.weights_version_label,
    )
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
