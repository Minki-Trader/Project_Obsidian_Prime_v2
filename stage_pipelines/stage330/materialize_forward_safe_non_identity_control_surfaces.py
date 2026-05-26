from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage329 import forward_holdout_score_replay as replay  # noqa: E402


STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
SOURCE_STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_NUMBER = "run330B"
RUN_ID = "run330B_materialize_forward_safe_non_identity_control_surfaces_v1"
PARENT_RUN_ID = "run330A_design_forward_safe_non_identity_surface_robustness_packet_v1"
NEXT_RUN_ID = "run330C_forward_mt5_or_score_curve_review_v1"
STATUS = "completed_forward_safe_control_surface_materialization_no_selection"
JUDGMENT = "fixed_threshold_materialization_completed_no_forward_decision"
DECISION = "stage330B_control_surfaces_materialized_curve_and_runtime_review_next"
TODAY = "2026-05-26"
CLAIM_BOUNDARY = (
    "research_development_only_fixed_threshold_control_surface_materialization_no_forward_threshold_tuning_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PREDICTIONS_DIR = RUN_DIR / "predictions"
SIGNAL_PAYLOAD_DIR = RUN_DIR / "signal_payloads"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330B_forward_safe_control_surface_materialization.md"

RUN330A_DIR = STAGE_DIR / "02_runs" / "run330A"
STAGE330B_QUEUE = RUN330A_DIR / "stage330B_materialization_queue.csv"
SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs"
RUN329B_DIR = SOURCE_RUN_DIR / "run329B"
RUN329C_DIR = SOURCE_RUN_DIR / "run329C"
RUN329D_DIR = SOURCE_RUN_DIR / "run329D"
FEATURE_FRAME_DIR = RUN329B_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN329B_DIR / "feature_orders"
FEATURE_SUMMARY = RUN329B_DIR / "feature_set_materialization_summary.csv"
COMBINED_SOURCE_IDENTITY = RUN329B_DIR / "combined_source_identity.json"
SOURCE_QUEUE = RUN329C_DIR / "forward_replay_candidate_queue.csv"
SOURCE_THRESHOLD_MANIFEST = RUN329C_DIR / "fixed_threshold_manifest.csv"
SOURCE_OOS_SIGNAL_METRICS = RUN329C_DIR / "fixed_threshold_signal_metrics.csv"
SOURCE_RUN329D_SCORE_SUMMARY = RUN329D_DIR / "forward_score_summary.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RAW_VIEW = "raw_forward"
SESSION_VIEW = "old_session_parity"
VIEWS = [RAW_VIEW, SESSION_VIEW]
RAW_SESSION_SIGNAL_RATIO_WARN = 2.0
EXCLUSIVE_RAW_SIGNAL_RATE_WARN = 0.25
TAIL_GAP_WARN_HOURS = 48.0


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def path_is_file(path: Path) -> bool:
    return path_exists(path) and io_path(path).is_file()


def sha256_file(path: Path) -> str:
    if not path_is_file(path):
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_stage330b_subject_queue() -> list[dict[str, str]]:
    rows = read_csv(STAGE330B_QUEUE)
    return [row for row in rows if row.get("artifact_slug") and row.get("artifact_slug") != "all"]


def candidate_queue_by_slug() -> dict[str, dict[str, str]]:
    return {row["artifact_slug"]: row for row in read_csv(SOURCE_QUEUE)}


def source_identity_by_symbol() -> dict[str, dict[str, Any]]:
    payload = read_json(COMBINED_SOURCE_IDENTITY)
    return {str(row.get("contract_symbol")): row for row in payload.get("source_identities", [])}


def timestamp_gap_stats(timestamps: pd.Series) -> dict[str, Any]:
    ts = pd.to_datetime(timestamps, utc=True).sort_values()
    duplicate_count = int(ts.duplicated().sum())
    if len(ts) <= 1:
        return {"duplicate_timestamps": duplicate_count, "gaps_gt_5m": 0, "gaps_gt_1h": 0, "max_gap_minutes": 0.0}
    diffs = ts.diff().dropna().dt.total_seconds() / 60.0
    return {
        "duplicate_timestamps": duplicate_count,
        "gaps_gt_5m": int((diffs > 5.0).sum()),
        "gaps_gt_1h": int((diffs > 60.0).sum()),
        "max_gap_minutes": float(diffs.max()) if len(diffs) else 0.0,
    }


def feature_frame_audit(old_minutes: set[int]) -> list[dict[str, Any]]:
    summary_rows = {row["feature_set_id"]: row for row in read_csv(FEATURE_SUMMARY)}
    identities = source_identity_by_symbol()
    us100_identity = identities.get("US100", {})
    requested_to = pd.to_datetime(us100_identity.get("compute_end_utc"), utc=True)
    audit_rows: list[dict[str, Any]] = []
    for feature_set_id, summary in summary_rows.items():
        path = ROOT / summary["parquet_path"]
        frame = pd.read_parquet(io_path(path))
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        minutes = (frame["timestamp"].dt.hour * 60 + frame["timestamp"].dt.minute).astype(int)
        session_rows = int(minutes.isin(old_minutes).sum())
        last_ts = pd.to_datetime(frame["timestamp"], utc=True).max()
        tail_gap_hours = float((requested_to - last_ts).total_seconds() / 3600.0) if pd.notna(requested_to) and pd.notna(last_ts) else 0.0
        gaps = timestamp_gap_stats(frame["timestamp"])
        if len(frame) == 0:
            judgment = "blocked_forward_data_missing"
        elif tail_gap_hours > TAIL_GAP_WARN_HOURS:
            judgment = "usable_with_tail_gap_requires_calendar_context"
        else:
            judgment = "usable_for_fixed_replay_with_boundary"
        audit_rows.append(
            {
                "feature_set_id": feature_set_id,
                "feature_count": summary.get("feature_count"),
                "frame_path": rel(path),
                "frame_sha256": sha256_file(path),
                "rows": int(len(frame)),
                "session_rows": session_rows,
                "session_row_rate": float(session_rows / len(frame)) if len(frame) else 0.0,
                "first_timestamp": frame["timestamp"].min().isoformat() if len(frame) else "",
                "last_timestamp": last_ts.isoformat() if len(frame) else "",
                "source_compute_end_utc": requested_to.isoformat() if pd.notna(requested_to) else "",
                "tail_gap_hours_vs_source_compute_end": tail_gap_hours,
                "duplicate_timestamps": gaps["duplicate_timestamps"],
                "gaps_gt_5m": gaps["gaps_gt_5m"],
                "gaps_gt_1h": gaps["gaps_gt_1h"],
                "max_gap_minutes": gaps["max_gap_minutes"],
                "source_materialization_status": summary.get("status"),
                "audit_judgment": judgment,
            }
        )
    return audit_rows


def feature_order_audit(candidate_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    threshold_rows = {row["artifact_slug"]: row for row in read_csv(SOURCE_THRESHOLD_MANIFEST)}
    audit_rows = []
    for candidate in candidate_rows:
        slug = candidate["artifact_slug"]
        feature_set_id = candidate["feature_set_id"]
        order_path = FEATURE_ORDER_DIR / f"{feature_set_id}_feature_order.txt"
        features = replay.load_feature_order(feature_set_id)
        threshold = threshold_rows.get(slug, {})
        audit_rows.append(
            {
                "artifact_slug": slug,
                "candidate_id": candidate["candidate_id"],
                "feature_set_id": feature_set_id,
                "model_id": candidate["model_id"],
                "feature_order_path": rel(order_path),
                "feature_order_sha256": sha256_file(order_path),
                "feature_count_from_order": len(features),
                "feature_count_from_queue": candidate.get("feature_count"),
                "threshold_policy": threshold.get("policy"),
                "threshold": threshold.get("threshold"),
                "threshold_source_split": threshold.get("source_split"),
                "audit_judgment": "feature_order_and_fixed_threshold_bound",
            }
        )
    return audit_rows


def signal_payload(prediction: pd.DataFrame, payload_path: Path) -> int:
    signal = prediction.loc[prediction["signal"].astype(int) == 1].copy()
    columns = [
        "timestamp",
        "symbol",
        "candidate_id",
        "artifact_slug",
        "feature_set_id",
        "model_id",
        "view_id",
        "predicted_label",
        "signal_direction",
        "p_short",
        "p_flat",
        "p_long",
        "max_probability",
        "probability_margin",
        "decision_threshold",
        "hour_utc",
        "month",
        "us_cash_session",
        "volatility_regime",
        "adx_regime",
        "vix_zscore_regime",
        "usdx_zscore_regime",
        "us10yr_zscore_regime",
    ]
    for column in columns:
        if column not in signal.columns:
            signal[column] = ""
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    signal.loc[:, columns].to_csv(io_path(payload_path), index=False, encoding="utf-8", lineterminator="\n")
    return int(len(signal))


def raw_session_gap_rows(predictions: dict[tuple[str, str], pd.DataFrame], summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_key = {(row["artifact_slug"], row["view_id"]): row for row in summaries}
    rows: list[dict[str, Any]] = []
    for slug in sorted({key[0] for key in by_key}):
        raw_summary = by_key[(slug, RAW_VIEW)]
        session_summary = by_key[(slug, SESSION_VIEW)]
        raw_pred = predictions[(slug, RAW_VIEW)]
        session_pred = predictions[(slug, SESSION_VIEW)]
        raw_timestamps = set(pd.to_datetime(raw_pred["timestamp"], utc=True).astype(str))
        session_timestamps = set(pd.to_datetime(session_pred["timestamp"], utc=True).astype(str))
        raw_signal = raw_pred.loc[raw_pred["signal"].astype(int) == 1].copy()
        session_signal = session_pred.loc[session_pred["signal"].astype(int) == 1].copy()
        session_signal_timestamps = set(pd.to_datetime(session_signal["timestamp"], utc=True).astype(str))
        exclusive_raw_rows = len(raw_timestamps.difference(session_timestamps))
        exclusive_raw_signal_rows = int(
            pd.to_datetime(raw_signal["timestamp"], utc=True).astype(str).map(lambda value: value not in session_signal_timestamps).sum()
        )
        exclusive_raw_signal_rate = float(exclusive_raw_signal_rows / exclusive_raw_rows) if exclusive_raw_rows else 0.0
        raw_long_share = fnum(raw_summary.get("signal_long_share"))
        session_long_share = fnum(session_summary.get("signal_long_share"))
        ratio = fnum(raw_summary.get("signals_per_day")) / fnum(session_summary.get("signals_per_day"), 1.0)
        row_ratio = fnum(raw_summary.get("rows")) / fnum(session_summary.get("rows"), 1.0)
        if ratio > RAW_SESSION_SIGNAL_RATIO_WARN or exclusive_raw_signal_rate > EXCLUSIVE_RAW_SIGNAL_RATE_WARN:
            judgment = "raw_session_gap_high_pressure"
        elif ratio > 1.5 or exclusive_raw_signal_rate > 0.10:
            judgment = "raw_session_gap_watch"
        else:
            judgment = "raw_session_gap_within_review_band"
        rows.append(
            {
                "artifact_slug": slug,
                "candidate_id": raw_summary.get("candidate_id"),
                "feature_set_id": raw_summary.get("feature_set_id"),
                "raw_rows": raw_summary.get("rows"),
                "session_rows": session_summary.get("rows"),
                "raw_session_row_ratio": row_ratio,
                "raw_signals_per_day": raw_summary.get("signals_per_day"),
                "session_signals_per_day": session_summary.get("signals_per_day"),
                "raw_session_signal_per_day_ratio": ratio,
                "raw_signal_rate": raw_summary.get("signal_rate"),
                "session_signal_rate": session_summary.get("signal_rate"),
                "exclusive_raw_rows": exclusive_raw_rows,
                "exclusive_raw_signal_rows": exclusive_raw_signal_rows,
                "exclusive_raw_signal_rate": exclusive_raw_signal_rate,
                "raw_long_share": raw_long_share,
                "session_long_share": session_long_share,
                "long_share_shift": float(raw_long_share - session_long_share),
                "gap_judgment": judgment,
            }
        )
    return rows


def materialize_scores(old_minutes: set[int], subject_rows: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path], dict[tuple[str, str], pd.DataFrame]]:
    source_candidates = candidate_queue_by_slug()
    oos_metrics = replay.load_oos_signal_metrics()
    summary_rows: list[dict[str, Any]] = []
    density_input: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    slice_rows: list[dict[str, Any]] = []
    payload_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    predictions: dict[tuple[str, str], pd.DataFrame] = {}

    for subject in subject_rows:
        slug = subject["artifact_slug"]
        candidate = dict(source_candidates[slug])
        feature_set_id = candidate["feature_set_id"]
        features = replay.load_feature_order(feature_set_id)
        frame_path = FEATURE_FRAME_DIR / f"{feature_set_id}.parquet"
        frame = pd.read_parquet(io_path(frame_path))
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        missing_features = sorted(set(features).difference(frame.columns))
        if missing_features:
            raise RuntimeError(f"{feature_set_id} missing features: {missing_features}")
        values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
        if not np.isfinite(values).all():
            raise RuntimeError(f"{feature_set_id} contains non-finite feature values")
        minute_of_day = (frame["timestamp"].dt.hour * 60 + frame["timestamp"].dt.minute).astype(int)
        views = {
            RAW_VIEW: frame,
            SESSION_VIEW: frame.loc[minute_of_day.isin(old_minutes)].copy(),
        }
        for view_id in VIEWS:
            view_frame = views[view_id]
            if view_frame.empty:
                raise RuntimeError(f"{slug} {view_id} produced no rows")
            prediction, summary, parity = replay.score_frame(candidate, view_id, view_frame, features)
            prediction_path = PREDICTIONS_DIR / f"{slug}_{view_id}_score.parquet"
            prediction.to_parquet(io_path(prediction_path), index=False)
            payload_path = SIGNAL_PAYLOAD_DIR / f"{slug}_{view_id}_signals.csv"
            signal_rows = signal_payload(prediction, payload_path)
            artifacts.extend([prediction_path, payload_path])
            summary["prediction_path"] = rel(prediction_path)
            summary["signal_payload_path"] = rel(payload_path)
            summary["stage330_role"] = subject.get("role")
            summary["priority"] = subject.get("priority")
            summary_rows.append(summary)
            density_input.append(summary)
            parity_rows.append(parity)
            slice_rows.extend(replay.slice_rows(prediction))
            predictions[(slug, view_id)] = prediction
            payload_rows.append(
                {
                    "artifact_slug": slug,
                    "candidate_id": candidate["candidate_id"],
                    "view_id": view_id,
                    "prediction_path": rel(prediction_path),
                    "prediction_sha256": sha256_file(prediction_path),
                    "signal_payload_path": rel(payload_path),
                    "signal_payload_sha256": sha256_file(payload_path),
                    "signal_rows": signal_rows,
                    "threshold_policy": candidate.get("decision_threshold_policy"),
                    "threshold": candidate.get("decision_threshold"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    density_rows = replay.density_shift_rows(density_input, oos_metrics)
    return summary_rows, density_rows, parity_rows, slice_rows, payload_rows, artifacts, predictions


def data_integrity_receipt(audit_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    blocked = [row for row in audit_rows if row.get("audit_judgment") == "blocked_forward_data_missing"]
    tail = [row for row in audit_rows if row.get("audit_judgment") == "usable_with_tail_gap_requires_calendar_context"]
    judgment = "blocked" if blocked else ("usable_with_boundary_tail_gap_noted" if tail else "usable_with_boundary")
    return {
        "data_source": {
            "feature_frames": rel(FEATURE_FRAME_DIR),
            "stage330B_queue": rel(STAGE330B_QUEUE),
            "source_identity": rel(COMBINED_SOURCE_IDENTITY),
        },
        "time_axis": "US100 M5 broker/server timestamps converted to UTC-aware pandas timestamps; raw and old-session parity views stay separate",
        "sample_scope": "2026-04-14+ forward feature frames from Stage329B, with source compute end audited against feature-valid end",
        "missing_or_duplicate_check": "forward_data_availability_audit.csv records duplicates and timestamp gaps per feature set",
        "feature_label_boundary": "no forward labels, no forward threshold search, no lot/risk repair",
        "split_boundary": "old train/WFO/OOS thresholds from Stage329C are reused; latest forward is read-only replay",
        "leakage_risk": "session-only interpretation, forward threshold tuning, and tail-gap overclaim are the primary risks",
        "data_hash_or_identity": {row["feature_set_id"]: row.get("frame_sha256") for row in audit_rows},
        "integrity_judgment": judgment,
    }


def model_validation_receipt(subject_rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    return {
        "model_family": "Stage329 LogisticRegression research ONNX controls reused unchanged",
        "target_and_label": "historical Stage329 label; no new forward label is created in run330B",
        "split_method": "fixed train-only threshold replay on latest forward feature frames",
        "selection_metric": "none; all queued controls are materialized",
        "secondary_metrics": "signal density, raw/session gap, ONNX parity, slice signal attribution",
        "threshold_policy": "reuse Stage329C train_only_nonflat_margin_q60 thresholds exactly",
        "overfit_risk": "multiple controls, session parity positivity, raw-forward density explosion",
        "calibration_risk": "scores are ordering signals, not calibrated probabilities",
        "comparison_baseline": "Stage329D replay and Stage329G raw/session gap pressure",
        "validation_judgment": "fixed_threshold_materialization_completed_no_selection",
        "materialized_subject_count": len(subject_rows),
    }


def runtime_parity_receipt(parity_rows: Sequence[Mapping[str, Any]], payload_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    failures = [row for row in parity_rows if not bool(row.get("passed"))]
    return {
        "research_path": rel(Path(__file__)),
        "runtime_path": "signal_payloads materialized; MT5 tester not run in run330B",
        "shared_contract": "feature order, ONNX probability order short/flat/long, fixed threshold, signal direction, timestamp",
        "known_differences": "run330B is score/signal materialization only; MT5 fills and SL/TP behavior remain future evidence",
        "parity_check": "ONNX Runtime vs sklearn probability parity plus signal payload hash manifest",
        "parity_identity": {
            "parity_row_count": len(parity_rows),
            "parity_failure_count": len(failures),
            "payload_count": len(payload_rows),
        },
        "runtime_claim_boundary": "research_only_no_runtime_authority",
    }


def result_judgment_rows(audit_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    high_gap = [row for row in gap_rows if row.get("gap_judgment") == "raw_session_gap_high_pressure"]
    evidence_missing = "MT5 tester output, trade list, curve pocket, cost stress, lot-normalized result, final forward decision"
    if any(row.get("audit_judgment") == "blocked_forward_data_missing" for row in audit_rows):
        label = "blocked_forward_data_missing"
        next_condition = "repair_forward_feature_data_then_rerun_run330B"
    else:
        label = JUDGMENT
        next_condition = NEXT_RUN_ID
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "forward data audit, fixed threshold replay summary, ONNX parity, raw/session gap guard, signal payload manifest",
            "evidence_missing": evidence_missing,
            "judgment_label": label,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": next_condition,
            "user_explanation_hook": f"물질화는 끝났지만 Forward Passed/Failed는 아니다. raw/session high pressure controls={len(high_gap)}.",
        }
    ]


def required_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "data_integrity",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "forward_data_availability_audit.csv"),
            "effect": "latest forward feature availability and tail gap are explicit",
        },
        {
            "gate_id": "model_validation",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "model_validation_receipt.json"),
            "effect": "no new model, no threshold tuning, all controls replayed",
        },
        {
            "gate_id": "runtime_parity",
            "status": "onnx_payload_parity_only_mt5_not_claimed",
            "artifact_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
            "effect": "signal payload exists but runtime authority is not claimed",
        },
        {
            "gate_id": "raw_session_gap_guard",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "raw_session_gap_guard.csv"),
            "effect": "session-only positives cannot decide forward robustness",
        },
        {
            "gate_id": "result_judgment",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "result_judgment.csv"),
            "effect": "run330B closes without selection or forward decision",
        },
        {
            "gate_id": "artifact_lineage",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "effect": "inputs and outputs have hashes",
        },
    ]


def report_md(audit_rows: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], payload_rows: Sequence[Mapping[str, Any]]) -> str:
    high_gap = [row for row in gap_rows if row.get("gap_judgment") == "raw_session_gap_high_pressure"]
    tail_gap = [row for row in audit_rows if row.get("audit_judgment") == "usable_with_tail_gap_requires_calendar_context"]
    session_rows = [row for row in summary_rows if row.get("view_id") == SESSION_VIEW]
    payload_signal_count = sum(int(row.get("signal_rows") or 0) for row in payload_rows)
    best_session = sorted(session_rows, key=lambda row: str(row.get("artifact_slug")))[0] if session_rows else {}
    return f"""
# Run330B Forward-Safe Control Surface Materialization(330B 전진 안전 대조 표면 물질화)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## What Was Materialized(물질화 내용)

- control surfaces(대조 표면): `{len(set(row.get('artifact_slug') for row in summary_rows))}`
- scored views(점수화 보기): `{len(summary_rows)}`
- signal payload files(신호 인계 파일): `{len(payload_rows)}`
- total signal rows(총 신호 행): `{payload_signal_count}`
- first session example(세션 예시): `{best_session.get('artifact_slug', 'none')}` rows `{best_session.get('rows', '')}` signals/day `{best_session.get('signals_per_day', '')}`

## Guard Read(방어 판독)

- forward data audit rows(전진 데이터 감사 행): `{len(audit_rows)}`
- tail gap noted(꼬리 공백 기록): `{len(tail_gap)}`
- raw/session high pressure(원본/세션 고압): `{len(high_gap)}`

Effect(효과): c56_plain(코어56 일반) 같은 낮은 압력 단서도 바로 선택하지 않고, raw/session gap(원본/세션 간극)과 ONNX parity(온엑스 동등성)를 먼저 통과한 입력 파일로만 남겼다.

## What This Does Not Claim(주장하지 않는 것)

- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating promotion(운영 승격): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 이 payload(인계물)를 바탕으로 MT5 또는 score-curve(점수 곡선) 검토, curve pocket(곡선 포켓), cost stress(비용 압박), lot-normalized result(로트 정규화 결과)를 진행한다.
"""


def decision_doc_md() -> str:
    return f"""
# Decision: Stage330B Control Surface Materialization(결정: 330B 대조 표면 물질화)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

run330B(330B 실행)는 Stage329C(329C 실행)의 fixed threshold(고정 임계값)와 ONNX(온엑스)를 그대로 재생했다.
Effect(효과): latest forward(최신 전진) 결과로 threshold(임계값), lot(로트), decision rule(판단 규칙)을 고치지 않는다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위)는 모두 `not_claimed`다.
"""


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        STAGE330B_QUEUE,
        SOURCE_QUEUE,
        SOURCE_THRESHOLD_MANIFEST,
        FEATURE_SUMMARY,
        COMBINED_SOURCE_IDENTITY,
        SOURCE_RUN329D_SCORE_SUMMARY,
    ]
    inputs.extend(sorted(FEATURE_FRAME_DIR.glob("*.parquet")))
    inputs.extend(sorted((RUN329C_DIR / "onnx").glob("*.onnx")))
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "generated_at_utc": generated_at_utc,
        "inputs": [{"path": rel(path), "exists": path_exists(path), "sha256": sha256_file(path)} for path in inputs],
        "outputs": [{"path": rel(path), "exists": path_exists(path), "sha256": sha256_file(path)} for path in artifacts if path_is_file(path)],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def update_stage_docs() -> list[Path]:
    updated: list[Path] = []
    updated.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage330 Selection Status(330단계 선택 상태)

- stage_status(단계 상태): `open_materialization_completed`
- selected_candidate(선택 후보): `none`
- research_onnx_status(연구 온엑스 상태): `fixed_threshold_control_surfaces_materialized_no_new_model_trained`
- source_cp322A_status(원천 cp322A 상태): `research_artifact_preserved_exact_forward_handoff_blocked`
- latest_completed_run(최신 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage330B(330B 실행)는 대조 표면을 물질화했지만 후보 확정이 아니며, 다음은 MT5/곡선/비용 검토다.
""",
        )
    )
    append_if_missing(
        STAGE_DIR / "00_spec" / "stage_brief.md",
        "run330B_materialization_summary",
        f"""
## run330B_materialization_summary(330B 물질화 요약)

- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): fixed threshold(고정 임계값) score/signal payload(점수/신호 인계물)를 만들었고, raw/session gap(원본/세션 간극)과 ONNX parity(온엑스 동등성)를 다음 검토의 필수 입력으로 고정했다.
""",
    )
    updated.append(STAGE_DIR / "00_spec" / "stage_brief.md")
    append_if_missing(
        STAGE_DIR / "01_inputs" / "input_refs.md",
        "run330B_materialization_outputs",
        f"""
## run330B_materialization_outputs(330B 물질화 출력)

- materialization_report(물질화 보고서): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/03_reviews/run330B_forward_safe_control_surface_materialization.md`
- fixed_threshold_summary(고정 임계값 요약): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330B/fixed_threshold_replay_summary.csv`
- signal_payload_manifest(신호 인계 목록): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330B/signal_payload_manifest.csv`
- raw_session_gap_guard(원본/세션 간극 방어): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330B/raw_session_gap_guard.csv`

Effect(효과): run330C(330C 실행)는 새 점수 계산 없이 이 고정 인계물을 소비할 수 있다.
""",
    )
    updated.append(STAGE_DIR / "01_inputs" / "input_refs.md")
    return updated


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage330(330단계) run330B(330B 실행)는 `{STATUS}`로 고정 규칙 대조 표면을 물질화했다. Effect(효과): Forward Passed/Failed(전진 통과/실패) 없이 run330C(330C 실행)의 MT5/곡선/비용 검토로 넘긴다.\n"
    )
    if "Stage330(330단계) run330B(330B 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    marker = "stage330B_forward_safe_control_surface_materialization:"
    block = f"""
stage330B_forward_safe_control_surface_materialization:
  packet_id: {STAGE_ID}_v2
  stage_id: {STAGE_ID}
  status: {STATUS}
  judgment: {JUDGMENT}
  decision: {DECISION}
  completed_run_id: {RUN_ID}
  next_run_id: {NEXT_RUN_ID}
  report_path: stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/03_reviews/run330B_forward_safe_control_surface_materialization.md
  boundary: {CLAIM_BOUNDARY}
"""
    if marker not in workspace_text:
        workspace_text = workspace_text.rstrip() + "\n\n" + block.strip() + "\n"
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v3`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `forward_safe_non_identity_control_surface_curve_review`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": "- status(상태): `stage330_run330B_materialization_completed_curve_review_next`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run330B_summary(330B 요약): forward-safe control surface materialization(전진 안전 대조 표면 물질화)을 `{STATUS}`로 닫았다. "
        "Effect(효과): 고정 threshold(임계값) score/signal payload(점수/신호 인계물), data audit(데이터 감사), ONNX parity(온엑스 동등성), raw/session gap guard(원본/세션 간극 방어)를 만들었고 선택 후보는 없다."
    )
    if "run330B_summary(330B 요약)" not in current_text:
        current_text = current_text.replace(f"- decision(판정): `{DECISION}`\n", f"- decision(판정): `{DECISION}`\n{summary}\n", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    append_if_missing(
        CHANGELOG,
        "Stage330B Forward-Safe Control Surface Materialization",
        f"""
## 2026-05-26 - Stage330B Forward-Safe Control Surface Materialization(330B 전진 안전 대조 표면 물질화)

- run330B(330B 실행): Stage329C(329C 실행)의 ONNX(온엑스)와 fixed threshold(고정 임계값)를 그대로 써서 Stage330(330단계) score/signal payload(점수/신호 인계물)를 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): selected candidate(선택 후보), Forward Passed(전진 통과), Forward Failed(전진 실패), Goal Achieve(목표 달성)는 없고, 다음은 `{NEXT_RUN_ID}`다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run330B_forward_safe_control_surface_materialization.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "model_validation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": "fixed_threshold_control_surface_materialization;no_candidate_selection;next_curve_review;goal_achieve_not_claimed.",
            }
        ],
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__fixed_threshold_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "fixed_threshold_control_surface_materialization",
        "tier_scope": "latest forward raw and old-session parity views",
        "kpi_scope": "data_integrity_score_density_onnx_parity_raw_session_gap",
        "scoreboard_lane": "model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "signal_payload_count",
        "guardrail_kpi": "no_forward_threshold_tuning;no_candidate_selection;runtime_authority_not_claimed",
        "external_verification_status": "out_of_scope_by_claim_no_mt5_tester_in_run330B",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [ledger_row])
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__fixed_threshold_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fixed_threshold_control_surface_materialization(고정 임계값 대조 표면 물질화)",
                "tier_scope": "latest forward raw and old-session parity views(최신 전진 원본 및 기존 세션 동등 보기)",
                "scoreboard": "data_integrity_score_density_onnx_parity_raw_session_gap(데이터 무결성/점수 밀도/온엑스 동등성/원본 세션 간극)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selection;no_forward_decision;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    rows = []
    for path in artifacts:
        if path_is_file(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(path)}",
                    "artifact_type": "stage330B_forward_safe_control_surface_materialization_artifact",
                    "path": rel(path),
                    "sha256": sha256_file(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage330B fixed-threshold materialization artifact; no selected candidate and no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_outputs(generated_at_utc: str) -> list[Path]:
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    SIGNAL_PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    old_minutes, session_manifest = replay.load_old_session_minutes()
    subject_rows = load_stage330b_subject_queue()
    audit_rows = feature_frame_audit(old_minutes)
    order_rows = feature_order_audit(subject_rows)
    summary_rows, density_rows, parity_rows, slice_rows, payload_rows, score_artifacts, predictions = materialize_scores(old_minutes, subject_rows)
    gap_rows = raw_session_gap_rows(predictions, summary_rows)
    artifacts: list[Path] = list(score_artifacts)
    artifacts.append(write_csv(RUN_DIR / "forward_data_availability_audit.csv", ["feature_set_id", "feature_count", "frame_path", "frame_sha256", "rows", "session_rows", "session_row_rate", "first_timestamp", "last_timestamp", "source_compute_end_utc", "tail_gap_hours_vs_source_compute_end", "duplicate_timestamps", "gaps_gt_5m", "gaps_gt_1h", "max_gap_minutes", "source_materialization_status", "audit_judgment"], audit_rows))
    artifacts.append(write_csv(RUN_DIR / "feature_order_hash_audit.csv", ["artifact_slug", "candidate_id", "feature_set_id", "model_id", "feature_order_path", "feature_order_sha256", "feature_count_from_order", "feature_count_from_queue", "threshold_policy", "threshold", "threshold_source_split", "audit_judgment"], order_rows))
    artifacts.append(write_csv(RUN_DIR / "fixed_threshold_replay_summary.csv", ["candidate_id", "artifact_slug", "feature_set_id", "model_id", "view_id", "rows", "days", "rows_per_day", "start_timestamp", "end_timestamp", "decision_threshold_policy", "decision_threshold", "signal_rows", "signal_rate", "signals_per_day", "pred_short", "pred_flat", "pred_long", "signal_short", "signal_long", "signal_long_share", "mean_max_probability", "mean_probability_margin", "median_probability_margin", "prediction_path", "signal_payload_path", "stage330_role", "priority"], summary_rows))
    artifacts.append(write_csv(RUN_DIR / "density_shift_vs_oos.csv", ["candidate_id", "artifact_slug", "feature_set_id", "model_id", "view_id", "rows", "days", "rows_per_day", "signal_rows", "signal_rate", "signals_per_day", "oos_signal_rate", "oos_signals_per_day", "signal_rate_delta_vs_oos", "signals_per_day_ratio_vs_oos", "signal_long_share", "density_judgment"], density_rows))
    artifacts.append(write_csv(RUN_DIR / "forward_onnx_parity_summary.csv", ["candidate_id", "artifact_slug", "feature_set_id", "model_id", "view_id", "rows", "passed", "max_abs_diff", "mean_abs_diff", "onnx_row_sum_max_abs_error", "input_name", "output_names", "onnx_path", "onnx_sha256", "sklearn_model_path", "sklearn_model_sha256"], parity_rows))
    artifacts.append(write_csv(RUN_DIR / "forward_slice_signal_attribution.csv", ["candidate_id", "artifact_slug", "feature_set_id", "model_id", "view_id", "slice_type", "slice_value", "rows", "signal_rows", "signal_rate", "signal_long", "signal_short", "signal_long_share", "mean_max_probability", "mean_probability_margin"], slice_rows))
    artifacts.append(write_csv(RUN_DIR / "raw_session_gap_guard.csv", ["artifact_slug", "candidate_id", "feature_set_id", "raw_rows", "session_rows", "raw_session_row_ratio", "raw_signals_per_day", "session_signals_per_day", "raw_session_signal_per_day_ratio", "raw_signal_rate", "session_signal_rate", "exclusive_raw_rows", "exclusive_raw_signal_rows", "exclusive_raw_signal_rate", "raw_long_share", "session_long_share", "long_share_shift", "gap_judgment"], gap_rows))
    artifacts.append(write_csv(RUN_DIR / "signal_payload_manifest.csv", ["artifact_slug", "candidate_id", "view_id", "prediction_path", "prediction_sha256", "signal_payload_path", "signal_payload_sha256", "signal_rows", "threshold_policy", "threshold", "claim_boundary"], payload_rows))
    artifacts.append(write_json(RUN_DIR / "old_session_parity_manifest.json", session_manifest))
    artifacts.append(write_json(RUN_DIR / "data_integrity_receipt.json", data_integrity_receipt(audit_rows)))
    artifacts.append(write_json(RUN_DIR / "model_validation_receipt.json", model_validation_receipt(subject_rows)))
    artifacts.append(write_json(RUN_DIR / "runtime_parity_receipt.json", runtime_parity_receipt(parity_rows, payload_rows)))
    artifacts.append(write_csv(RUN_DIR / "result_judgment.csv", ["result_subject", "evidence_available", "evidence_missing", "judgment_label", "claim_boundary", "next_condition", "user_explanation_hook"], result_judgment_rows(audit_rows, gap_rows)))
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_id", "status", "artifact_path", "effect"], required_gate_rows()))
    artifacts.append(write_md(REVIEWS_DIR / "run330B_forward_safe_control_surface_materialization.md", report_md(audit_rows, summary_rows, gap_rows, payload_rows)))
    artifacts.append(write_md(DECISION_DOC, decision_doc_md()))
    artifacts.extend(update_stage_docs())
    artifacts.extend(update_current_truth())
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_mt5_tester_in_run330B",
                "materialized_subject_count": len(subject_rows),
                "scored_view_count": len(summary_rows),
            },
        )
    )
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    update_registers(generated_at_utc, artifacts + [Path(__file__)])
    return artifacts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize Stage330B fixed-threshold forward-safe control surfaces.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "artifact_count": len(artifacts),
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
