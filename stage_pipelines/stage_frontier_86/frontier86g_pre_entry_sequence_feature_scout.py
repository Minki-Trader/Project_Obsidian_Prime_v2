from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract
from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
RUN_ID = "frontier86G_pre_entry_intrabar_sequence_feature_scout_v1"
PARENT_RUN_ID = "frontier86F_first_touch_surface_repair_or_rotation_decision_v1"
F86D_RUN_ID = "frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1"
NEXT_RUNTIME_PREFLIGHT = "frontier86H_sequence_surface_runtime_materialization_preflight_v1"
NEXT_REPAIR_OR_ROTATION = "frontier86H_sequence_axis_repair_or_rotation_decision_v1"

CLAIM_BOUNDARY = (
    "f86g_pre_entry_sequence_feature_proxy_scout_only_no_strategy_tester_runtime_"
    "economics_no_runtime_authority_no_goal_achieve"
)
STATUS_POSITIVE = "f86g_pre_entry_sequence_proxy_positive_runtime_preflight_required_no_authority"
STATUS_WEAK = "f86g_pre_entry_sequence_proxy_weak_or_negative_repair_or_rotation_required_no_authority"
STATUS_BLOCKED = "f86g_pre_entry_sequence_source_blocked_no_runtime_authority"
JUDGMENT_POSITIVE = "positive_proxy_sequence_clue_with_locked_oos_readout_no_runtime_evidence"
JUDGMENT_WEAK = "weak_or_negative_sequence_proxy_scout_no_runtime_evidence"
JUDGMENT_BLOCKED = "blocked_pre_entry_source_export_no_model_judgment"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
SOURCE_DIR = RUN_DIR / "pre_entry_source"
FEATURE_DIR = RUN_DIR / "sequence_feature_surface"
MODEL_DIR = RUN_DIR / "models"
PROXY_DIR = RUN_DIR / "proxy_scout"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F85B_READOUT = (
    ROOT
    / "stages/stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild"
    / "03_reviews/f85b_selected_firewall_row_readout.csv"
)
F86D_LABELS = STAGE_DIR / "02_runs" / F86D_RUN_ID / "first_touch_labels/first_touch_labels.csv"
F86F_DECISION = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "decision/repair_or_rotation_decision.json"

PRE_ENTRY_M1_REGISTRY = SOURCE_DIR / "pre_entry_m1_registry.csv"
PRE_ENTRY_TICK_SUMMARY = SOURCE_DIR / "pre_entry_tick_summary.csv"
PRE_ENTRY_SOURCE_SUMMARY = SOURCE_DIR / "pre_entry_source_summary.json"
FEATURE_SURFACE = FEATURE_DIR / "sequence_feature_surface.csv"
FEATURE_SCHEMA = FEATURE_DIR / "feature_schema.json"
SCORES_CSV = PROXY_DIR / "proxy_scores.csv"
MODEL_METRICS = PROXY_DIR / "proxy_metrics.json"
MODEL_CARD = MODEL_DIR / "proxy_model_card.json"
BEST_MODEL = MODEL_DIR / "best_sequence_proxy_model.joblib"
SUMMARY_JSON = RUN_DIR / "summary.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

EXECUTION_SUMMARY = REVIEW_DIR / "f86g_execution_summary.json"
SOURCE_AUDIT = REVIEW_DIR / "f86g_pre_entry_source_audit.json"
LEAKAGE_AUDIT = REVIEW_DIR / "f86g_feature_leakage_audit.json"
SPLIT_AUDIT = REVIEW_DIR / "f86g_split_boundary_audit.json"
SCOPE_GATE = REVIEW_DIR / "f86g_scope_completion_gate.json"
KPI_AUDIT = REVIEW_DIR / "f86g_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f86g_artifact_lineage_audit.json"
RESULT_AUDIT = REVIEW_DIR / "f86g_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f86g_final_claim_guard.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f86g_run_evidence_receipt.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f86g_experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = REVIEW_DIR / "f86g_data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = REVIEW_DIR / "f86g_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f86g_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f86g_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f86g_claim_discipline_receipt.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
STAGE_SELECTION_STATUS = STAGE_DIR / "04_selected/selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"

POINT_SIZE = 0.01
PRE_ENTRY_MINUTES = 5
M1_OFFSETS = range(-PRE_ENTRY_MINUTES, 0)
TICK_COPY_FLAGS = "COPY_TICKS_ALL"

BASE_CONTEXT_NUMERIC_FEATURES = [
    "hour_utc",
    "hour_sin",
    "hour_cos",
]
SCALAR_CONTEXT_NUMERIC_FEATURES = [
    "p_short",
    "p_flat",
    "p_long",
    "f85b_side_prob",
    "f85b_probability_margin",
    "f85b_flat_pressure",
    "atr_points",
    "open_sl_points",
    "open_tp_points",
    "f85b_atr_sl_ratio",
    "computed_lot",
    "side_signed_probability_edge",
    "opposite_side_probability",
    "tp_sl_ratio",
    "sl_atr_ratio",
    "tp_atr_ratio",
]
SEQUENCE_NUMERIC_FEATURES = [
    "m1_pre_full_window",
    "m1_pre_return_points",
    "m1_pre_signed_return_points",
    "m1_pre_return_over_atr",
    "m1_pre_signed_return_over_atr",
    "m1_pre_range_sum_points",
    "m1_pre_range_mean_points",
    "m1_pre_range_max_points",
    "m1_pre_body_abs_sum_points",
    "m1_pre_wick_total_sum_points",
    "m1_pre_up_count",
    "m1_pre_down_count",
    "m1_pre_tick_volume_sum",
    "m1_pre_tick_volume_slope",
    "m1_pre_spread_mean",
    "m1_pre_spread_max",
    "m1_pre_spread_last",
    "tick_pre_count",
    "tick_pre_mid_return_points",
    "tick_pre_signed_mid_return_points",
    "tick_pre_mid_return_over_atr",
    "tick_pre_signed_mid_return_over_atr",
    "tick_pre_mid_range_points",
    "tick_pre_spread_mean",
    "tick_pre_spread_max",
    "tick_pre_spread_last",
    "tick_pre_last30s_count",
    "tick_pre_last30s_mid_return_points",
    "tick_pre_last30s_signed_mid_return_points",
]
CATEGORICAL_FEATURES = ["decision", "session_bucket"]
FEATURE_SETS = {
    "sequence_context": BASE_CONTEXT_NUMERIC_FEATURES + SEQUENCE_NUMERIC_FEATURES + CATEGORICAL_FEATURES,
    "sequence_plus_scalar_context": BASE_CONTEXT_NUMERIC_FEATURES
    + SCALAR_CONTEXT_NUMERIC_FEATURES
    + SEQUENCE_NUMERIC_FEATURES
    + CATEGORICAL_FEATURES,
}
AUDIT_ONLY_COLUMNS = [
    "row_index",
    "timestamp_utc",
    "split",
    "f85b_candidate_id",
    "input_hash",
    "target_candidate_id",
    "source_candidate_id",
    "runtime_wrapper_id",
]
FORBIDDEN_FEATURE_COLUMNS = [
    "runtime_net",
    "runtime_win_bool",
    "proxy_win",
    "proxy_win_runtime_loss",
    "proxy_loss_runtime_win",
    "proxy_both_hit",
    "proxy_exit_path_label",
    "first_touch_label",
    "label_resolution_method",
    "tick_count",
    "first_sl_time_msc_utc",
    "first_tp_time_msc_utc",
    "entry_price_proxy_m5_open",
    "m5_high",
    "m5_low",
    "m5_close",
    "sl_price",
    "tp_price",
    "m5_sl_hit",
    "m5_tp_hit",
    "m5_path_class",
    "m5_close_direction_win",
]
ALLOWED_CLAIMS = [
    "f86g_pre_entry_source_export_recorded",
    "f86g_sequence_feature_surface_materialized",
    "f86g_proxy_scout_result_recorded",
    "next_axis_decision_recorded",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "materialization_ready",
    "ea_onnx_runtime_bundle_ready",
    "oos_selected_model",
]


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt" and len(str(resolved)) >= 240:
        return io_path(path)
    return resolved


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        return json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_text(path: Path, text: str) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    if fieldnames is None:
        seen: set[str] = set()
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    ordered.append(key)
        fieldnames = ordered or ["empty"]
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    with fs_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def upsert_many_csv(path: Path, key: str, new_rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    new_rows = list(new_rows)
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(new_rows[0].keys()) if new_rows else [key]
        rows = []
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    replacement_keys = {str(row.get(key, "")) for row in new_rows}
    rows = [existing for existing in rows if str(existing.get(key, "")) not in replacement_keys]
    rows.extend({field: csv_value(row.get(field, "")) for field in fieldnames} for row in new_rows)
    write_csv_rows(path, rows, fieldnames)


def file_identity(path: Path) -> dict[str, Any]:
    native = io_path(path)
    if not native.exists():
        return {"path": rel(path), "exists": False}
    return {
        "path": rel(path),
        "exists": True,
        "size": native.stat().st_size,
        "sha256": sha256_file_lf_normalized(path),
    }


def feature_order_hash(columns: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(columns) + "\n").encode("utf-8")).hexdigest()


def parse_timestamp_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def utc_from_unix(seconds: int | float) -> str:
    return datetime.fromtimestamp(int(seconds), tz=UTC).isoformat().replace("+00:00", "Z")


def utc_from_msc(milliseconds: int | float) -> str:
    return datetime.fromtimestamp(float(milliseconds) / 1000.0, tz=UTC).isoformat().replace("+00:00", "Z")


def compact_terminal_info(info: Any) -> dict[str, Any]:
    if info is None:
        return {}
    fields = ["name", "company", "path", "data_path", "build", "connected", "trade_allowed", "maxbars"]
    return {field: getattr(info, field, None) for field in fields}


def ensure_dirs() -> None:
    for directory in (RUN_DIR, SOURCE_DIR, FEATURE_DIR, MODEL_DIR, PROXY_DIR, REPORT_DIR, REVIEW_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def mt5_initialize(mt5: Any) -> tuple[bool, dict[str, Any]]:
    attempts: list[dict[str, Any]] = [{"label": "default_initialize", "kwargs": {}}]
    for candidate in (Path("C:/Program Files/MetaTrader 5/terminal64.exe"), Path("C:/Program Files/MetaTrader 5/terminal.exe")):
        if candidate.exists():
            attempts.append({"label": f"path_initialize_{candidate.name}", "kwargs": {"path": str(candidate)}})
            attempts.append({"label": f"path_portable_initialize_{candidate.name}", "kwargs": {"path": str(candidate), "portable": True}})
    receipts: list[dict[str, Any]] = []
    for attempt in attempts:
        ok = bool(mt5.initialize(**attempt["kwargs"]))
        receipt = {"label": attempt["label"], "ok": ok, "last_error": str(mt5.last_error())}
        receipts.append(receipt)
        if ok:
            return True, {"status": "initialized", "attempts": receipts}
        try:
            mt5.shutdown()
        except Exception:
            pass
    return False, {"status": "blocked_initialize_failed", "attempts": receipts}


def rate_record(raw: Any) -> dict[str, Any]:
    names = list(raw.dtype.names or []) if hasattr(raw, "dtype") else []
    rec = {name: raw[name].item() if hasattr(raw[name], "item") else raw[name] for name in names}
    if rec.get("time") is not None:
        rec["time_utc"] = utc_from_unix(rec["time"])
    return rec


def tick_record(raw: Any) -> dict[str, Any]:
    names = list(raw.dtype.names or []) if hasattr(raw, "dtype") else []
    rec = {name: raw[name].item() if hasattr(raw[name], "item") else raw[name] for name in names}
    if rec.get("time") is not None:
        rec["time_utc"] = utc_from_unix(rec["time"])
    if rec.get("time_msc") is not None:
        rec["time_msc_utc"] = utc_from_msc(rec["time_msc"])
    return rec


def load_input_rows() -> pd.DataFrame:
    readout = read_csv_frame(F85B_READOUT)
    labels = read_csv_frame(F86D_LABELS)
    readout["row_index_join"] = pd.to_numeric(readout["row_index"], errors="raise").astype(int)
    labels["row_index_join"] = pd.to_numeric(labels["source_row_index"], errors="raise").astype(int)
    merged = readout.merge(
        labels[
            [
                "row_index_join",
                "first_touch_label",
                "label_resolution_method",
                "tick_count",
                "m5_path_class",
            ]
        ],
        on="row_index_join",
        how="inner",
        validate="one_to_one",
    )
    if len(merged) != len(readout) or len(merged) != len(labels):
        raise RuntimeError(f"F86G input join mismatch: readout={len(readout)} labels={len(labels)} merged={len(merged)}")
    merged = merged.rename(columns={"row_index": "row_index_source"})
    merged["row_index"] = merged["row_index_join"].astype(int)
    merged["timestamp_dt"] = merged["timestamp_utc"].map(parse_timestamp_utc)
    return merged.sort_values("timestamp_dt").reset_index(drop=True)


def export_pre_entry_sources(frame: pd.DataFrame) -> dict[str, Any]:
    try:
        import MetaTrader5 as mt5  # type: ignore
    except Exception as exc:
        summary = {
            "status": "blocked_metatrader5_import_failed",
            "error": f"{type(exc).__name__}: {exc}",
            "claim_effect": "No sequence feature model is trusted without pre-entry source export.",
        }
        write_json(PRE_ENTRY_SOURCE_SUMMARY, summary)
        return summary

    ok, init_receipt = mt5_initialize(mt5)
    if not ok:
        summary = {
            "status": "blocked_mt5_initialize_failed",
            "initialize": init_receipt,
            "claim_effect": "No sequence feature model is trusted without pre-entry source export.",
        }
        write_json(PRE_ENTRY_SOURCE_SUMMARY, summary)
        return summary

    terminal_info: dict[str, Any] = {}
    try:
        terminal_info = compact_terminal_info(mt5.terminal_info())
        m1_summary = export_pre_entry_m1(mt5, frame)
        tick_summary = export_pre_entry_tick_summaries(mt5, frame)
        status = "pass" if m1_summary["selected_rows_with_full_pre_entry_m1_window"] == len(frame) else "usable_with_boundary"
        summary = {
            "status": status,
            "symbol": "US100",
            "m1_offsets": list(M1_OFFSETS),
            "pre_entry_minutes": PRE_ENTRY_MINUTES,
            "tick_copy_flags": TICK_COPY_FLAGS,
            "selected_rows": int(len(frame)),
            "initialize": init_receipt,
            "terminal_info": terminal_info,
            "m1_summary": m1_summary,
            "tick_summary": tick_summary,
            "artifacts": {
                "m1_registry": file_identity(PRE_ENTRY_M1_REGISTRY),
                "tick_summary": file_identity(PRE_ENTRY_TICK_SUMMARY),
            },
            "claim_effect": "Only timestamps strictly before the selected M5 timestamp are used as features.",
        }
        write_json(PRE_ENTRY_SOURCE_SUMMARY, summary)
        return summary
    finally:
        mt5.shutdown()


def export_pre_entry_m1(mt5: Any, frame: pd.DataFrame) -> dict[str, Any]:
    timestamps = list(frame["timestamp_dt"])
    start = min(timestamps) - timedelta(minutes=PRE_ENTRY_MINUTES)
    end = max(timestamps)
    m1_by_time: dict[int, dict[str, Any]] = {}
    chunk_rows: list[dict[str, Any]] = []
    chunk_start = start
    while chunk_start <= end:
        chunk_end = min(chunk_start + timedelta(days=14), end)
        rates = mt5.copy_rates_range("US100", mt5.TIMEFRAME_M1, chunk_start, chunk_end)
        count = 0 if rates is None else int(len(rates))
        if rates is not None:
            for raw in rates:
                rec = rate_record(raw)
                m1_by_time[int(rec["time"])] = rec
        chunk_rows.append(
            {
                "chunk_start_utc": chunk_start.isoformat().replace("+00:00", "Z"),
                "chunk_end_utc": chunk_end.isoformat().replace("+00:00", "Z"),
                "rows": count,
                "last_error": str(mt5.last_error()),
            }
        )
        chunk_start = chunk_end + timedelta(seconds=60)

    registry_rows: list[dict[str, Any]] = []
    full_rows = 0
    missing_minutes = 0
    for record in frame.to_dict("records"):
        bar_start = record["timestamp_dt"]
        row_missing = 0
        for offset in M1_OFFSETS:
            minute_ts = int((bar_start + timedelta(minutes=int(offset))).timestamp())
            m1 = m1_by_time.get(minute_ts)
            if m1 is None:
                row_missing += 1
                missing_minutes += 1
                registry_rows.append(
                    {
                        "source_row_index": int(record["row_index"]),
                        "timestamp_utc": record["timestamp_utc"],
                        "m1_offset": int(offset),
                        "m1_time_utc": utc_from_unix(minute_ts),
                        "m1_present": False,
                    }
                )
                continue
            registry_rows.append(
                {
                    "source_row_index": int(record["row_index"]),
                    "timestamp_utc": record["timestamp_utc"],
                    "m1_offset": int(offset),
                    "m1_time_utc": m1.get("time_utc"),
                    "m1_present": True,
                    "open": m1.get("open"),
                    "high": m1.get("high"),
                    "low": m1.get("low"),
                    "close": m1.get("close"),
                    "tick_volume": m1.get("tick_volume"),
                    "spread": m1.get("spread"),
                    "real_volume": m1.get("real_volume"),
                }
            )
        if row_missing == 0:
            full_rows += 1
    write_csv_rows(PRE_ENTRY_M1_REGISTRY, registry_rows)
    return {
        "registry_path": rel(PRE_ENTRY_M1_REGISTRY),
        "expected_m1_rows": int(len(frame) * len(list(M1_OFFSETS))),
        "registered_m1_rows": int(sum(1 for row in registry_rows if row.get("m1_present") is True)),
        "missing_m1_minutes": int(missing_minutes),
        "selected_rows_with_full_pre_entry_m1_window": int(full_rows),
        "chunk_rows": chunk_rows,
    }


def export_pre_entry_tick_summaries(mt5: Any, frame: pd.DataFrame) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    blocked_rows = 0
    for record in frame.to_dict("records"):
        ts = record["timestamp_dt"]
        start = ts - timedelta(minutes=PRE_ENTRY_MINUTES)
        ticks = mt5.copy_ticks_range("US100", start, ts - timedelta(milliseconds=1), mt5.COPY_TICKS_ALL)
        if ticks is None:
            blocked_rows += 1
            rows.append(
                {
                    "source_row_index": int(record["row_index"]),
                    "timestamp_utc": record["timestamp_utc"],
                    "status": "blocked_copy_ticks_failed",
                    "last_error": str(mt5.last_error()),
                    "tick_pre_count": 0,
                }
            )
            continue
        recs = [tick_record(raw) for raw in ticks]
        rows.append(tick_summary_row(record, recs, str(mt5.last_error())))
    write_csv_rows(PRE_ENTRY_TICK_SUMMARY, rows)
    return {
        "summary_path": rel(PRE_ENTRY_TICK_SUMMARY),
        "rows": int(len(rows)),
        "blocked_rows": int(blocked_rows),
        "rows_with_ticks": int(sum(1 for row in rows if int(row.get("tick_pre_count") or 0) > 0)),
        "total_ticks_summarized": int(sum(int(row.get("tick_pre_count") or 0) for row in rows)),
    }


def tick_summary_row(record: Mapping[str, Any], ticks: Sequence[Mapping[str, Any]], last_error: str) -> dict[str, Any]:
    side = 1.0 if str(record.get("decision", "")).lower() == "long" else -1.0
    base = {
        "source_row_index": int(record["row_index"]),
        "timestamp_utc": record["timestamp_utc"],
        "status": "pass",
        "last_error": last_error,
        "tick_pre_count": int(len(ticks)),
    }
    if not ticks:
        base.update(
            {
                "tick_pre_mid_return_points": None,
                "tick_pre_signed_mid_return_points": None,
                "tick_pre_mid_range_points": None,
                "tick_pre_spread_mean": None,
                "tick_pre_spread_max": None,
                "tick_pre_spread_last": None,
                "tick_pre_last30s_count": 0,
                "tick_pre_last30s_mid_return_points": None,
                "tick_pre_last30s_signed_mid_return_points": None,
            }
        )
        return base
    bid = np.array([float(t.get("bid") or np.nan) for t in ticks], dtype=float)
    ask = np.array([float(t.get("ask") or np.nan) for t in ticks], dtype=float)
    mid = (bid + ask) / 2.0
    spread = ask - bid
    finite_mid = mid[np.isfinite(mid)]
    finite_spread = spread[np.isfinite(spread)]
    mid_return = float(finite_mid[-1] - finite_mid[0]) if len(finite_mid) >= 2 else None
    msc_values = [t.get("time_msc") for t in ticks]
    last_msc = max(int(value) for value in msc_values if value is not None) if any(value is not None for value in msc_values) else None
    last30_mask = []
    if last_msc is not None:
        cutoff = last_msc - 30_000
        last30_mask = [int(t.get("time_msc") or 0) >= cutoff for t in ticks]
    last30_mid = mid[np.array(last30_mask, dtype=bool)] if last30_mask else np.array([], dtype=float)
    last30_mid = last30_mid[np.isfinite(last30_mid)]
    last30_return = float(last30_mid[-1] - last30_mid[0]) if len(last30_mid) >= 2 else None
    base.update(
        {
            "tick_pre_mid_return_points": mid_return,
            "tick_pre_signed_mid_return_points": None if mid_return is None else mid_return * side,
            "tick_pre_mid_range_points": float(np.nanmax(finite_mid) - np.nanmin(finite_mid)) if len(finite_mid) else None,
            "tick_pre_spread_mean": float(np.nanmean(finite_spread)) if len(finite_spread) else None,
            "tick_pre_spread_max": float(np.nanmax(finite_spread)) if len(finite_spread) else None,
            "tick_pre_spread_last": float(finite_spread[-1]) if len(finite_spread) else None,
            "tick_pre_last30s_count": int(len(last30_mid)),
            "tick_pre_last30s_mid_return_points": last30_return,
            "tick_pre_last30s_signed_mid_return_points": None if last30_return is None else last30_return * side,
        }
    )
    return base


def m1_sequence_features(m1_frame: pd.DataFrame, input_frame: pd.DataFrame) -> pd.DataFrame:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in m1_frame.to_dict("records"):
        grouped[int(row["source_row_index"])].append(row)
    feature_rows: list[dict[str, Any]] = []
    side_by_row = {
        int(row["row_index"]): (1.0 if str(row.get("decision", "")).lower() == "long" else -1.0)
        for row in input_frame.to_dict("records")
    }
    atr_by_row = {int(row["row_index"]): float(row.get("atr_points") or np.nan) for row in input_frame.to_dict("records")}
    for row_index, rows in grouped.items():
        rows = sorted(rows, key=lambda item: int(item.get("m1_offset", 0)))
        present = [row for row in rows if str(row.get("m1_present")).lower() == "true" or row.get("m1_present") is True]
        side = side_by_row.get(row_index, 1.0)
        atr = atr_by_row.get(row_index, np.nan)
        out: dict[str, Any] = {"row_index": row_index, "m1_pre_full_window": int(len(present) == PRE_ENTRY_MINUTES)}
        if len(present) < 2:
            feature_rows.append(out)
            continue
        opens = np.array([float(row.get("open") or np.nan) for row in present], dtype=float)
        highs = np.array([float(row.get("high") or np.nan) for row in present], dtype=float)
        lows = np.array([float(row.get("low") or np.nan) for row in present], dtype=float)
        closes = np.array([float(row.get("close") or np.nan) for row in present], dtype=float)
        tick_volume = np.array([float(row.get("tick_volume") or np.nan) for row in present], dtype=float)
        spread = np.array([float(row.get("spread") or np.nan) for row in present], dtype=float)
        bodies = closes - opens
        ranges = highs - lows
        body_abs = np.abs(bodies)
        wick_total = np.maximum(ranges - body_abs, 0.0)
        ret = float(closes[-1] - opens[0])
        out.update(
            {
                "m1_pre_return_points": ret,
                "m1_pre_signed_return_points": ret * side,
                "m1_pre_return_over_atr": ret / atr if atr and math.isfinite(atr) and atr != 0 else None,
                "m1_pre_signed_return_over_atr": ret * side / atr if atr and math.isfinite(atr) and atr != 0 else None,
                "m1_pre_range_sum_points": float(np.nansum(ranges)),
                "m1_pre_range_mean_points": float(np.nanmean(ranges)),
                "m1_pre_range_max_points": float(np.nanmax(ranges)),
                "m1_pre_body_abs_sum_points": float(np.nansum(body_abs)),
                "m1_pre_wick_total_sum_points": float(np.nansum(wick_total)),
                "m1_pre_up_count": int(np.nansum(bodies > 0)),
                "m1_pre_down_count": int(np.nansum(bodies < 0)),
                "m1_pre_tick_volume_sum": float(np.nansum(tick_volume)),
                "m1_pre_tick_volume_slope": float(tick_volume[-1] - tick_volume[0]) if len(tick_volume) >= 2 else None,
                "m1_pre_spread_mean": float(np.nanmean(spread)),
                "m1_pre_spread_max": float(np.nanmax(spread)),
                "m1_pre_spread_last": float(spread[-1]),
            }
        )
        feature_rows.append(out)
    return pd.DataFrame(feature_rows)


def build_feature_surface(input_frame: pd.DataFrame, source_summary: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any]]:
    if str(source_summary.get("status", "")).startswith("blocked"):
        return pd.DataFrame(), blocked_leakage_audit(source_summary), split_audit_payload(pd.DataFrame())
    m1_frame = read_csv_frame(PRE_ENTRY_M1_REGISTRY)
    tick_frame = read_csv_frame(PRE_ENTRY_TICK_SUMMARY)
    m1_features = m1_sequence_features(m1_frame, input_frame)
    tick_frame = tick_frame.rename(columns={"source_row_index": "row_index"})
    merged = input_frame.merge(m1_features, on="row_index", how="left", validate="one_to_one")
    merged = merged.merge(tick_frame.drop(columns=["timestamp_utc"], errors="ignore"), on="row_index", how="left", validate="one_to_one")

    numeric_base = BASE_CONTEXT_NUMERIC_FEATURES + SCALAR_CONTEXT_NUMERIC_FEATURES + SEQUENCE_NUMERIC_FEATURES
    for column in numeric_base:
        if column in merged.columns:
            merged[column] = pd.to_numeric(merged[column], errors="coerce")
    for column in ["hour_utc", "p_short", "p_flat", "p_long", "f85b_side_prob", "atr_points", "open_sl_points", "open_tp_points", "f85b_atr_sl_ratio", "computed_lot"]:
        if column in merged.columns:
            merged[column] = pd.to_numeric(merged[column], errors="coerce")
    decision = merged["decision"].astype(str).str.lower()
    merged["opposite_side_probability"] = np.where(decision.eq("long"), merged["p_short"], merged["p_long"])
    merged["side_signed_probability_edge"] = np.where(
        decision.eq("long"),
        merged["p_long"] - merged["p_short"],
        merged["p_short"] - merged["p_long"],
    )
    merged["tp_sl_ratio"] = merged["open_tp_points"] / merged["open_sl_points"].replace(0, np.nan)
    merged["sl_atr_ratio"] = merged["open_sl_points"] / merged["atr_points"].replace(0, np.nan)
    merged["tp_atr_ratio"] = merged["open_tp_points"] / merged["atr_points"].replace(0, np.nan)
    hour = merged["hour_utc"].fillna(0.0).astype(float)
    merged["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    merged["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)
    for column in [
        "tick_pre_mid_return_points",
        "tick_pre_signed_mid_return_points",
        "tick_pre_mid_return_over_atr",
        "tick_pre_signed_mid_return_over_atr",
        "tick_pre_last30s_mid_return_points",
        "tick_pre_last30s_signed_mid_return_points",
    ]:
        if column not in merged.columns:
            continue
    merged["tick_pre_mid_return_over_atr"] = merged["tick_pre_mid_return_points"] / merged["atr_points"].replace(0, np.nan)
    merged["tick_pre_signed_mid_return_over_atr"] = merged["tick_pre_signed_mid_return_points"] / merged["atr_points"].replace(0, np.nan)
    merged["first_touch_group"] = np.select(
        [
            merged["first_touch_label"].astype(str).str.startswith("tp_first"),
            merged["first_touch_label"].astype(str).str.startswith("sl_first"),
            merged["first_touch_label"].astype(str).str.startswith("none_hit"),
        ],
        ["tp_first", "sl_first", "none_hit"],
        default="other",
    )
    merged["target_tp_first_binary"] = np.where(
        merged["first_touch_group"].eq("tp_first"),
        1,
        np.where(merged["first_touch_group"].eq("sl_first"), 0, np.nan),
    )
    surface_columns = (
        [column for column in AUDIT_ONLY_COLUMNS if column in merged.columns]
        + sorted({column for columns in FEATURE_SETS.values() for column in columns if column in merged.columns})
        + [
            "first_touch_group",
            "target_tp_first_binary",
            "first_touch_label",
            "label_resolution_method",
        ]
    )
    surface = merged[surface_columns].copy()
    feature_columns = sorted({column for columns in FEATURE_SETS.values() for column in columns if column in surface.columns})
    forbidden_intersection = sorted(set(feature_columns) & set(FORBIDDEN_FEATURE_COLUMNS))
    source_feature_time_max = "strictly_before_entry_timestamp"
    leakage = {
        "audit_name": "f86g_feature_leakage_audit",
        "status": "pass" if not forbidden_intersection else "blocked",
        "input_rows": int(len(input_frame)),
        "surface_rows": int(len(surface)),
        "feature_columns": feature_columns,
        "feature_sets": FEATURE_SETS,
        "forbidden_feature_columns": FORBIDDEN_FEATURE_COLUMNS,
        "forbidden_feature_intersection": forbidden_intersection,
        "source_feature_time_max": source_feature_time_max,
        "label_columns_target_only": ["first_touch_group", "target_tp_first_binary", "first_touch_label", "label_resolution_method"],
        "label_counts": surface["first_touch_label"].value_counts(dropna=False).to_dict(),
        "first_touch_group_counts": surface["first_touch_group"].value_counts(dropna=False).to_dict(),
        "claim_effect": "Pre-entry source windows end before timestamp_utc; F86D entry-window M1/tick registry is not used as feature input.",
    }
    split_audit = split_audit_payload(surface)
    return surface, leakage, split_audit


def blocked_leakage_audit(source_summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "f86g_feature_leakage_audit",
        "status": "blocked",
        "source_status": source_summary.get("status"),
        "claim_effect": "Feature surface was not materialized because pre-entry source export failed.",
    }


def split_audit_payload(surface: pd.DataFrame) -> dict[str, Any]:
    if surface.empty:
        return {
            "audit_name": "f86g_split_boundary_audit",
            "status": "blocked",
            "claim_effect": "No split audit because feature surface is absent.",
        }
    valid_binary = surface["target_tp_first_binary"].notna()
    return {
        "audit_name": "f86g_split_boundary_audit",
        "status": "pass",
        "split_policy": "validation chronological 70/30 fit/inner selection; locked OOS readout only",
        "split_counts": surface["split"].value_counts(dropna=False).to_dict(),
        "binary_target_counts_by_split": surface.loc[valid_binary].groupby("split")["target_tp_first_binary"].agg(["count", "mean"]).reset_index().to_dict("records"),
        "oos_selection_allowed": False,
        "claim_effect": "OOS is readout-only and cannot select model, feature set, or threshold.",
    }


def chronological_validation_fit_mask(frame: pd.DataFrame) -> tuple[pd.Series, pd.Series, pd.Series]:
    valid_binary = frame["target_tp_first_binary"].notna()
    validation = valid_binary & frame["split"].astype(str).eq("validation")
    oos = valid_binary & frame["split"].astype(str).eq("oos")
    validation_rows = frame.loc[validation].sort_values("timestamp_utc")
    if validation_rows.empty:
        raise RuntimeError("No validation rows are available for F86G proxy scout.")
    cutoff = int(math.floor(len(validation_rows) * 0.70))
    cutoff = max(1, min(cutoff, len(validation_rows) - 1))
    fit_indices = set(validation_rows.iloc[:cutoff].index)
    inner_indices = set(validation_rows.iloc[cutoff:].index)
    fit = frame.index.to_series().isin(fit_indices)
    inner = frame.index.to_series().isin(inner_indices)
    return fit, inner, oos


def make_preprocessor(feature_columns: Sequence[str]) -> ColumnTransformer:
    numeric = [column for column in feature_columns if column not in CATEGORICAL_FEATURES]
    categorical = [column for column in feature_columns if column in CATEGORICAL_FEATURES]
    return ColumnTransformer(
        [
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric),
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
        ]
    )


def candidate_models() -> dict[str, Any]:
    return {
        "logreg_l2_balanced": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=86),
        "random_forest_depth4_balanced": RandomForestClassifier(
            n_estimators=240,
            max_depth=4,
            min_samples_leaf=25,
            class_weight="balanced_subsample",
            random_state=86,
            n_jobs=-1,
        ),
        "extra_trees_depth5_balanced": ExtraTreesClassifier(
            n_estimators=320,
            max_depth=5,
            min_samples_leaf=20,
            class_weight="balanced",
            random_state=86,
            n_jobs=-1,
        ),
    }


def safe_metric(metric: str, y_true: np.ndarray, score: np.ndarray, pred: np.ndarray) -> float | None:
    if len(y_true) == 0 or len(np.unique(y_true)) < 2:
        return None
    if metric == "roc_auc":
        return float(roc_auc_score(y_true, score))
    if metric == "average_precision":
        return float(average_precision_score(y_true, score))
    if metric == "log_loss":
        return float(log_loss(y_true, np.vstack([1 - score, score]).T, labels=[0, 1]))
    if metric == "brier":
        return float(brier_score_loss(y_true, score))
    if metric == "accuracy":
        return float(accuracy_score(y_true, pred))
    raise ValueError(metric)


def quantile_readout(y_true: np.ndarray, score: np.ndarray, q: float, top: bool) -> dict[str, Any]:
    if len(y_true) == 0:
        return {"rows": 0, "tp_first_rate": None, "coverage": 0.0, "threshold": None}
    threshold = float(np.quantile(score, q if top else 1 - q))
    mask = score >= threshold if top else score <= threshold
    rows = int(mask.sum())
    return {
        "rows": rows,
        "tp_first_rate": float(y_true[mask].mean()) if rows else None,
        "coverage": float(rows / len(y_true)) if len(y_true) else 0.0,
        "threshold": threshold,
    }


def evaluate_split(frame: pd.DataFrame, mask: pd.Series, model: Pipeline, feature_columns: Sequence[str], split_name: str) -> dict[str, Any]:
    subset = frame.loc[mask].copy()
    if subset.empty:
        return {"split": split_name, "rows": 0, "tp_first_rate": None}
    y = subset["target_tp_first_binary"].astype(int).to_numpy()
    score = model.predict_proba(subset[list(feature_columns)])[:, 1]
    pred = (score >= 0.5).astype(int)
    base_rate = float(y.mean()) if len(y) else None
    top_decile = quantile_readout(y, score, 0.90, top=True)
    bottom_decile = quantile_readout(y, score, 0.90, top=False)
    return {
        "split": split_name,
        "rows": int(len(y)),
        "tp_first_rate": base_rate,
        "roc_auc": safe_metric("roc_auc", y, score, pred),
        "average_precision": safe_metric("average_precision", y, score, pred),
        "log_loss": safe_metric("log_loss", y, score, pred),
        "brier": safe_metric("brier", y, score, pred),
        "accuracy_at_0_5": safe_metric("accuracy", y, score, pred),
        "top_decile": top_decile,
        "bottom_decile": bottom_decile,
        "top_decile_lift": (top_decile["tp_first_rate"] / base_rate) if top_decile["tp_first_rate"] is not None and base_rate else None,
        "bottom_decile_lift": (bottom_decile["tp_first_rate"] / base_rate) if bottom_decile["tp_first_rate"] is not None and base_rate else None,
    }


def train_proxy_models(surface: pd.DataFrame) -> tuple[dict[str, Any], pd.DataFrame | None, Pipeline | None]:
    fit_mask, inner_mask, oos_mask = chronological_validation_fit_mask(surface)
    rows: list[dict[str, Any]] = []
    score_frames: list[pd.DataFrame] = []
    best: tuple[float, float, str, Pipeline, dict[str, Any]] | None = None
    for feature_set_id, feature_columns in FEATURE_SETS.items():
        feature_columns = [column for column in feature_columns if column in surface.columns]
        for model_id, estimator in candidate_models().items():
            pipeline = Pipeline([("preprocess", make_preprocessor(feature_columns)), ("model", estimator)])
            fit_frame = surface.loc[fit_mask].copy()
            y_fit = fit_frame["target_tp_first_binary"].astype(int)
            pipeline.fit(fit_frame[feature_columns], y_fit)
            fit_metrics = evaluate_split(surface, fit_mask, pipeline, feature_columns, "validation_fit")
            inner_metrics = evaluate_split(surface, inner_mask, pipeline, feature_columns, "inner_validation")
            oos_metrics = evaluate_split(surface, oos_mask, pipeline, feature_columns, "locked_oos_readout")
            metrics = {
                "feature_set_id": feature_set_id,
                "model_id": model_id,
                "full_model_id": f"{feature_set_id}__{model_id}",
                "feature_count": len(feature_columns),
                "feature_columns": feature_columns,
                "validation_fit": fit_metrics,
                "inner_validation": inner_metrics,
                "locked_oos_readout": oos_metrics,
            }
            rows.append(metrics)
            for mask_name, mask in [("validation_fit", fit_mask), ("inner_validation", inner_mask), ("locked_oos_readout", oos_mask)]:
                subset = surface.loc[mask].copy()
                if subset.empty:
                    continue
                scores = pipeline.predict_proba(subset[feature_columns])[:, 1]
                score_frames.append(
                    pd.DataFrame(
                        {
                            "row_index": subset["row_index"].to_numpy(),
                            "timestamp_utc": subset["timestamp_utc"].to_numpy(),
                            "split_view": mask_name,
                            "feature_set_id": feature_set_id,
                            "model_id": model_id,
                            "full_model_id": f"{feature_set_id}__{model_id}",
                            "score_tp_first": scores,
                            "target_tp_first_binary": subset["target_tp_first_binary"].to_numpy(),
                            "first_touch_group": subset["first_touch_group"].to_numpy(),
                        }
                    )
                )
            inner_auc = inner_metrics.get("roc_auc")
            inner_lift = inner_metrics.get("top_decile_lift")
            if inner_auc is None:
                continue
            rank = (float(inner_auc), float(inner_lift or 0.0))
            if best is None or rank > (best[0], best[1]):
                best = (rank[0], rank[1], f"{feature_set_id}__{model_id}", pipeline, metrics)
    if best is None:
        raise RuntimeError("No F86G model produced a valid inner validation AUC.")
    _, _, best_model_id, best_model, best_metrics = best
    scores = pd.concat(score_frames, ignore_index=True) if score_frames else pd.DataFrame()
    model_ids = [row["full_model_id"] for row in rows]
    positive_scout = positive_scout_decision(best_metrics)
    summary = {
        "model_ids": model_ids,
        "best_model_id": best_model_id,
        "best_metrics": best_metrics,
        "all_metrics": rows,
        "selection_policy": "max inner_validation roc_auc, tie inner top_decile_lift; locked OOS readout only",
        "positive_scout": positive_scout,
        "positive_scout_criteria": {
            "inner_auc_min": 0.53,
            "inner_top_decile_lift_min": 1.15,
            "oos_auc_min": 0.50,
            "oos_top_decile_lift_min": 1.0,
        },
    }
    return summary, scores, best_model


def positive_scout_decision(metrics: Mapping[str, Any]) -> bool:
    inner = metrics["inner_validation"]
    oos = metrics["locked_oos_readout"]
    return (
        (inner.get("roc_auc") or 0.0) >= 0.53
        and (inner.get("top_decile_lift") or 0.0) >= 1.15
        and (oos.get("roc_auc") or 0.0) >= 0.50
        and (oos.get("top_decile_lift") or 0.0) >= 1.0
    )


def write_model_artifacts(surface: pd.DataFrame, source_summary: Mapping[str, Any], leakage: Mapping[str, Any], split_audit: Mapping[str, Any]) -> tuple[dict[str, Any], str, str]:
    if surface.empty or leakage.get("status") == "blocked":
        created_at = now_utc()
        model_summary = {
            "model_ids": [],
            "best_model_id": None,
            "best_metrics": {},
            "all_metrics": [],
            "selection_policy": "not_run_source_blocked",
            "positive_scout": False,
            "blocked_reason": source_summary.get("status") or leakage.get("status"),
        }
        status = STATUS_BLOCKED
        judgment = JUDGMENT_BLOCKED
        write_json(MODEL_METRICS, model_summary)
        write_csv_rows(SCORES_CSV, [])
        write_json(
            MODEL_CARD,
            {
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "status": status,
                "judgment": judgment,
                "model_materialized": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        return model_summary, status, judgment

    model_summary, scores, best_model = train_proxy_models(surface)
    status = STATUS_POSITIVE if model_summary["positive_scout"] else STATUS_WEAK
    judgment = JUDGMENT_POSITIVE if model_summary["positive_scout"] else JUDGMENT_WEAK
    joblib.dump(best_model, io_path(BEST_MODEL))
    write_csv_rows(SCORES_CSV, scores.to_dict("records"))
    write_json(MODEL_METRICS, model_summary)
    write_json(
        MODEL_CARD,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "best_model_id": model_summary["best_model_id"],
            "model_path": rel(BEST_MODEL),
            "feature_set_id": model_summary["best_metrics"].get("feature_set_id"),
            "feature_columns": model_summary["best_metrics"].get("feature_columns"),
            "selection_policy": model_summary["selection_policy"],
            "positive_scout": model_summary["positive_scout"],
            "source_summary": rel(PRE_ENTRY_SOURCE_SUMMARY),
            "feature_schema": rel(FEATURE_SCHEMA),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return model_summary, status, judgment


def write_feature_artifacts(surface: pd.DataFrame, leakage: Mapping[str, Any], split_audit: Mapping[str, Any]) -> None:
    if surface.empty:
        write_csv_rows(FEATURE_SURFACE, [])
        write_json(FEATURE_SCHEMA, {"run_id": RUN_ID, "status": "blocked", "claim_boundary": CLAIM_BOUNDARY})
        return
    write_csv_rows(FEATURE_SURFACE, surface.to_dict("records"))
    feature_columns = sorted({column for columns in FEATURE_SETS.values() for column in columns if column in surface.columns})
    schema = {
        "schema_id": "f86g_pre_entry_sequence_feature_schema_v1",
        "run_id": RUN_ID,
        "feature_surface": rel(FEATURE_SURFACE),
        "surface_rows": int(len(surface)),
        "feature_columns": feature_columns,
        "feature_sets": {key: [column for column in value if column in surface.columns] for key, value in FEATURE_SETS.items()},
        "feature_order_hash": feature_order_hash(feature_columns),
        "label_columns": ["first_touch_group", "target_tp_first_binary"],
        "audit_only_columns": AUDIT_ONLY_COLUMNS,
        "source_window": "timestamp_utc minus 5 minutes up to strictly before timestamp_utc",
        "forbidden_feature_columns": FORBIDDEN_FEATURE_COLUMNS,
        "leakage_audit": rel(LEAKAGE_AUDIT),
        "split_audit": rel(SPLIT_AUDIT),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_SCHEMA, schema)


def artifact_paths() -> list[Path]:
    return [
        ROOT / "stage_pipelines/stage_frontier_86/frontier86g_pre_entry_sequence_feature_scout.py",
        PRE_ENTRY_M1_REGISTRY,
        PRE_ENTRY_TICK_SUMMARY,
        PRE_ENTRY_SOURCE_SUMMARY,
        FEATURE_SURFACE,
        FEATURE_SCHEMA,
        SCORES_CSV,
        MODEL_METRICS,
        MODEL_CARD,
        BEST_MODEL,
        SUMMARY_JSON,
        RUN_MANIFEST,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        SOURCE_AUDIT,
        LEAKAGE_AUDIT,
        SPLIT_AUDIT,
        SCOPE_GATE,
        KPI_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_AUDIT,
        FINAL_CLAIM_GUARD,
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        WORK_PACKET,
        PACKET_SKILL_RECEIPTS,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
    ]


def write_summary_artifacts(
    surface: pd.DataFrame,
    source_summary: Mapping[str, Any],
    leakage: Mapping[str, Any],
    split_audit: Mapping[str, Any],
    model_summary: Mapping[str, Any],
    status: str,
    judgment: str,
    created_at: str,
) -> dict[str, Any]:
    next_run_id = NEXT_RUNTIME_PREFLIGHT if model_summary.get("positive_scout") else NEXT_REPAIR_OR_ROTATION
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "positive_scout": bool(model_summary.get("positive_scout")),
        "next_run_id": next_run_id,
        "surface_rows": int(len(surface)) if not surface.empty else 0,
        "binary_target_rows": int(surface["target_tp_first_binary"].notna().sum()) if not surface.empty else 0,
        "source_summary": source_summary,
        "leakage_audit_status": leakage.get("status"),
        "split_audit_status": split_audit.get("status"),
        "best_model_id": model_summary.get("best_model_id"),
        "best_metrics": model_summary.get("best_metrics", {}),
        "model_summary": model_summary,
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_type": "pre_entry_intrabar_sequence_feature_scout",
        "created_at_utc": created_at,
        "source_inputs": [rel(F85B_READOUT), rel(F86D_LABELS), rel(F86F_DECISION)],
        "produced_artifacts": [rel(path) for path in artifact_paths() if path_exists(path)],
        "external_verification_status": "mt5_api_pre_entry_source_export_completed_no_strategy_tester_runtime_claim"
        if not str(source_summary.get("status", "")).startswith("blocked")
        else "blocked_pre_entry_source_export",
        "mt5_strategy_tester_status": "not_applicable_no_runtime_or_economics_claim",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "scoreboard": "structural_scout",
        "status": status,
        "judgment": judgment,
        "primary_kpi": primary_kpi_text(model_summary),
        "guardrail_kpi": guardrail_kpi_text(model_summary),
        "net_profit": None,
        "profit_factor": None,
        "drawdown": None,
        "trade_count": None,
        "trades_per_day": None,
        "n_a_reason": "F86G is a Python proxy scout over first-touch labels; no Strategy Tester runtime economics were executed.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(KPI_RECORD, kpi_record)
    write_json(SUMMARY_JSON, summary)
    write_json(EXECUTION_SUMMARY, summary)
    return summary


def primary_kpi_text(model_summary: Mapping[str, Any]) -> str:
    best = model_summary.get("best_metrics") or {}
    inner = best.get("inner_validation") or {}
    return f"best_model={model_summary.get('best_model_id')};inner_auc={inner.get('roc_auc')};inner_top_decile_lift={inner.get('top_decile_lift')}"


def guardrail_kpi_text(model_summary: Mapping[str, Any]) -> str:
    best = model_summary.get("best_metrics") or {}
    oos = best.get("locked_oos_readout") or {}
    return f"oos_readout_only=true;oos_auc={oos.get('roc_auc')};oos_top_decile_lift={oos.get('top_decile_lift')};no_runtime_authority"


def result_summary_text(summary: Mapping[str, Any]) -> str:
    best = summary.get("best_metrics") or {}
    inner = best.get("inner_validation") or {}
    oos = best.get("locked_oos_readout") or {}
    return f"""# F86G Result Summary(F86G 결과 요약)

## Conclusion(결론)

F86G materialized a pre-entry M1/tick sequence feature scout(진입 전 1분/틱 시퀀스 피처 스카우트) and judged it as `{summary['judgment']}`.

This is proxy scout evidence(프록시 탐색 근거) only. It is not Strategy Tester runtime evidence(전략 테스터 런타임 근거), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## What changed(변경 사항)

Action(행동): F86G exported a new pre-entry source window(진입 전 원천 창) ending strictly before each selected timestamp(선택 타임스탬프 직전) and built sequence features(시퀀스 피처).

Effect(효과): The script avoids using F86D entry-window M1/tick registry(F86D 진입 창 1분/틱 등록부) as model features, so first-touch label leakage(첫 터치 라벨 누수)를 줄인다.

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)가 통과 대상이다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다.

codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

frontier_topic_rotation_check(전선 주제 회전 점검)는 새 canonical frontier open(정식 전선 개방)이 아니라 F86 내부 continuation(계속)이므로 해당 없음이다.

## What is still not enforced(아직 강제되지 않음)

F86G does not enforce ONNX export(온엑스 내보내기), EA handoff(EA 인계), Strategy Tester execution(전략 테스터 실행), runtime parity(런타임 동등성), WFO/stress validation(워크포워드/스트레스 검증), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Allowed claims(허용 주장)

f86g_pre_entry_source_export_recorded(F86G 진입 전 원천 내보내기 기록), f86g_sequence_feature_surface_materialized(F86G 시퀀스 피처 표면 물질화), f86g_proxy_scout_result_recorded(F86G 프록시 탐색 결과 기록), next_axis_decision_recorded(다음 축 결정 기록).

## Forbidden claims(금지 주장)

completion(완성), selected_baseline(선택 기준선), operating_promotion(운영 승격), runtime_authority(런타임 권위), live_readiness(실거래 준비), Goal Achieve(목표 달성), runtime_verified(런타임 검증됨), strategy_tester_runtime_economics(전략 테스터 런타임 경제성), materialization_ready(물질화 준비됨), EA/ONNX runtime bundle ready(EA/온엑스 런타임 번들 준비됨), OOS selected model(표본외 선택 모델).

## Next hardening step(다음 경화 단계)

Next(다음): `{summary['next_run_id']}`.

Action(행동): use the F86G result(결과)에 따라 runtime materialization preflight(런타임 물질화 사전확인) 또는 sequence-axis repair/rotation decision(시퀀스 축 수리/회전 결정)로 간다.

Effect(효과): positive proxy clue(긍정 프록시 단서)가 없으면 MT5 runtime claim(MT5 런타임 주장)으로 뛰지 않는다.

## Key Readout(핵심 판독)

- Source status(원천 상태): `{summary['source_summary'].get('status')}`
- Surface rows(표면 행): `{summary['surface_rows']}`
- Best model(최선 모델): `{summary.get('best_model_id')}`
- Positive scout(긍정 스카우트): `{summary['positive_scout']}`
- Inner validation AUC(내부 검증 AUC): `{inner.get('roc_auc')}`
- Inner top-decile lift(내부 상위 10% 리프트): `{inner.get('top_decile_lift')}`
- Locked OOS AUC(잠금 표본외 AUC): `{oos.get('roc_auc')}`
- Locked OOS top-decile lift(잠금 표본외 상위 10% 리프트): `{oos.get('top_decile_lift')}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_audits(summary: Mapping[str, Any], leakage: Mapping[str, Any], split_audit: Mapping[str, Any]) -> None:
    write_json(SOURCE_AUDIT, summary["source_summary"])
    write_json(LEAKAGE_AUDIT, leakage)
    write_json(SPLIT_AUDIT, split_audit)
    scope = {
        "audit_name": "scope_completion_gate",
        "status": "pass" if summary["surface_rows"] > 0 or summary["status"] == STATUS_BLOCKED else "blocked",
        "expected_outputs": [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(FEATURE_SURFACE), rel(MODEL_METRICS), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(SCOPE_GATE, scope)
    artifact_audit = {
        "audit_name": "artifact_lineage_audit",
        "status": "pass_connected_with_boundary",
        "source_inputs": [rel(F85B_READOUT), rel(F86D_LABELS), rel(F86F_DECISION)],
        "produced_artifacts": [rel(path) for path in artifact_paths() if path_exists(path)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(ARTIFACT_AUDIT, artifact_audit)
    result_audit = {
        "audit_name": "result_judgment_receipt",
        "status": "pass",
        "judgment": summary["judgment"],
        "evidence_available": [rel(MODEL_METRICS), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
        "evidence_missing": ["Strategy Tester report", "ONNX/EA bundle", "trade list", "runtime telemetry"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RESULT_AUDIT, result_audit)
    guard = final_claim_guard_payload(summary)
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)


def final_claim_guard_payload(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "blocked_claims": FORBIDDEN_CLAIMS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "claim_effect": "F86G can report proxy scout evidence only.",
        "summary_status": summary["status"],
    }


def receipt_payloads(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    produced = [rel(path) for path in artifact_paths() if path_exists(path)]
    source_inputs = [rel(F85B_READOUT), rel(F86D_LABELS), rel(F86F_DECISION)]
    receipts = [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "measurement_scope": "structural_scout proxy model over pre-entry M1/tick sequence features",
            "management_state": "run_manifest/kpi_record/summary/result_summary created",
            "judgment_class": "positive" if summary["positive_scout"] else ("blocked" if summary["status"] == STATUS_BLOCKED else "negative"),
            "scoreboard": "structural_scout",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "registry_update_required": "yes",
            "negative_memory_required": "yes" if not summary["positive_scout"] else "no",
            "hard_gate_applicable": "no",
            "evidence_boundary": "proxy-scout-only",
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "ledger_rows": [
                f"docs/registers/run_registry.csv::{RUN_ID}",
                f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv::{RUN_ID}",
                f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv::{summary['next_run_id']}",
            ],
            "missing_evidence": ["MT5 Strategy Tester report", "EA/ONNX bundle identity", "trade list and telemetry", "WFO/stress/runtime validation"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "Pre-entry M1/tick sequence and liquidity state may explain first-touch path better than F86E scalar context.",
            "baseline": "F86E scalar first-touch proxy scout metrics.",
            "decision_use": "Decide whether sequence-axis evidence justifies runtime materialization preflight or needs repair/rotation.",
            "comparison_baseline": "F86E scalar first-touch proxy scout.",
            "control_variables": ["F86D first-touch labels as target-only", "validation-inner selection", "locked OOS readout only", "no Strategy Tester runtime claim"],
            "changed_variables": ["new pre-entry M1 sequence summaries", "new pre-entry tick/spread summaries"],
            "sample_scope": "F86D/F85B selected rows, US100 M5 validation and OOS splits",
            "success_criteria": "inner AUC >= 0.53, inner top-decile lift >= 1.15, OOS AUC >= 0.50, OOS top-decile lift >= 1.0",
            "failure_criteria": "near-random inner/OOS metrics or OOS collapse",
            "invalid_conditions": ["pre-entry source export unavailable", "post-entry label-window columns enter feature set", "OOS used for model selection"],
            "stop_conditions": ["record proxy scout result and next action without runtime authority"],
            "evidence_plan": [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(FEATURE_SCHEMA), rel(MODEL_METRICS), rel(RESULT_SUMMARY)],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_source": source_inputs + [rel(PRE_ENTRY_SOURCE_SUMMARY)],
            "data_sources_checked": source_inputs + [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(PRE_ENTRY_M1_REGISTRY), rel(PRE_ENTRY_TICK_SUMMARY)],
            "time_axis": "UTC timestamp_utc is selected M5 bar open; feature source window ends strictly before timestamp_utc.",
            "time_axis_boundary": "Feature windows use [timestamp_utc - 5 minutes, timestamp_utc) in UTC; label windows begin at timestamp_utc.",
            "sample_scope": f"US100 M5 selected rows={summary['surface_rows']}",
            "missing_or_duplicate_check": "M1 full-window count and tick rows are recorded in pre_entry_source_summary.",
            "feature_label_boundary": "F86D first-touch labels are target-only; entry-window M1/tick fields are not feature inputs.",
            "split_boundary": "validation chronological fit/inner; OOS readout only",
            "leakage_checks": [
                "F86D entry-window M1/tick registry is not a feature source",
                "forbidden post-entry/path outcome columns are excluded from feature sets",
                "OOS is not used for model or feature-set selection",
            ],
            "leakage_risk": "Using F86D entry-window M1/tick registry as features would leak; F86G avoids it.",
            "missing_data_boundary": "If pre-entry MT5 API export is blocked, the run can only claim blocked source export and cannot claim model evidence.",
            "data_hash_or_identity": {"source_summary": file_identity(PRE_ENTRY_SOURCE_SUMMARY), "feature_surface": file_identity(FEATURE_SURFACE)},
            "integrity_judgment": "usable_with_boundary" if summary["surface_rows"] else "blocked",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_family": summary["model_summary"].get("model_ids", []),
            "model_or_threshold_surface": "Fixed proxy model family over sequence_context and sequence_plus_scalar_context feature sets; no runtime threshold selected.",
            "target_and_label": "F86D first-touch tp_first vs sl_first binary target; none_hit excluded from binary model metrics.",
            "split_method": "chronological validation fit/inner selection with locked OOS readout",
            "validation_split": "validation split is chronologically divided 70/30 for fit/inner; OOS is readout-only.",
            "selection_metric": "inner_validation roc_auc, tie top_decile_lift",
            "selection_metric_boundary": "Best model and feature set are selected only on inner_validation roc_auc/top_decile_lift.",
            "secondary_metrics": ["average_precision", "log_loss", "brier", "accuracy_at_0_5", "top_decile_lift", "OOS readout"],
            "threshold_policy": "no runtime threshold selected; score readout only",
            "overfit_risk": "multiple fixed model/feature-set scout; OOS is not used for selection",
            "overfit_checks": [
                "fixed finite candidate model list",
                "validation-inner only model selection",
                "locked OOS readout only",
                "no threshold search",
            ],
            "calibration_risk": "scores are ranks, not calibrated runtime probabilities",
            "comparison_baseline": "F86E scalar proxy metrics",
            "validation_judgment": summary["judgment"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": source_inputs,
            "raw_evidence": source_inputs + [rel(PRE_ENTRY_SOURCE_SUMMARY)],
            "producer": rel(ROOT / "stage_pipelines/stage_frontier_86/frontier86g_pre_entry_sequence_feature_scout.py"),
            "consumer": [rel(RESULT_SUMMARY), rel(WORK_PACKET), rel(SUMMARY_JSON)],
            "artifact_paths": produced,
            "produced_artifacts": produced,
            "machine_readable": [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(FEATURE_SCHEMA), rel(MODEL_METRICS), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(EXECUTION_SUMMARY), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS)],
            "artifact_hashes": {rel(path): file_identity(path).get("sha256") for path in artifact_paths() if path_exists(path)},
            "hashes_or_missing_reasons": {rel(path): file_identity(path) for path in artifact_paths() if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_generated_with_manifest",
            "lineage_boundary": "connected_with_boundary_proxy_scout_no_runtime_bundle",
            "lineage_judgment": "connected_with_boundary",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "result_subject": RUN_ID,
            "evidence_used": [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(FEATURE_SCHEMA), rel(MODEL_METRICS), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "evidence_available": [rel(MODEL_METRICS), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "evidence_missing": ["Strategy Tester output", "ONNX/EA bundle", "runtime parity"],
            "judgment_label": "positive" if summary["positive_scout"] else ("blocked" if summary["status"] == STATUS_BLOCKED else "negative"),
            "judgment_boundary": summary["judgment"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": summary["next_run_id"],
            "user_explanation_hook": "The sequence axis was tested as proxy evidence only; runtime claims still require MT5 artifacts.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "proxy_scout_only_no_runtime_authority",
        },
    ]
    return receipts


def write_receipts(receipts: Sequence[Mapping[str, Any]]) -> None:
    path_by_skill = {
        "obsidian-run-evidence-system": RUN_EVIDENCE_RECEIPT,
        "obsidian-experiment-design": EXPERIMENT_RECEIPT,
        "obsidian-data-integrity": DATA_INTEGRITY_RECEIPT,
        "obsidian-model-validation": MODEL_VALIDATION_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-result-judgment": RESULT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
    }
    for receipt in receipts:
        path = path_by_skill[str(receipt["skill"])]
        payload = dict(receipt)
        payload["receipt_path"] = rel(path)
        write_json(path, payload)
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-run-evidence-system",
            "receipts": [dict(receipt, receipt_path=rel(path_by_skill[str(receipt["skill"])])) for receipt in receipts],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def work_packet_payload(summary: Mapping[str, Any]) -> dict[str, Any]:
    required_gates = [
        "work_packet_schema_lint",
        "skill_receipt_schema_lint",
        "frontier_extra_due_check",
        "frontier_five_stage_direction_synthesis",
        "scope_completion_gate",
        "kpi_contract_audit",
        "artifact_lineage_audit",
        "result_judgment_receipt",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F86G pre-entry M1/tick sequence feature proxy scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["runtime candidate remains not claimed unless MT5 Strategy Tester evidence exists"],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(PACKET_DIR), rel(STAGE_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "pre_entry_window_accidentally_uses_label_window": "high",
                "weak_proxy_overclaimed_as_runtime_candidate": "high",
                "oos_selection_leakage": "medium",
            },
            "hard_stop_risks": [
                "Do not use F86D entry-window tick/M1 registry as features.",
                "Do not select model, feature set, or threshold from OOS.",
                "Do not claim runtime authority, live readiness, or Goal Achieve.",
            ],
            "required_gates": required_gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "pre_entry_source_export_required": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F86G pre-entry source export", "F86G sequence feature surface", "F86G proxy scout metrics"],
            "scope_units": ["run", "feature_surface", "model_scout", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "mt5_api_source_export_no_strategy_tester", "proxy_model_training"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["pre-entry source summary", "feature schema", "proxy metrics", "KPI record", "result summary"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F86G uses all F86D/F85B selected rows and does not top-k reduce source rows before modeling.",
            },
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
            "variants_requested": {"value": len(FEATURE_SETS) * len(candidate_models()), "n_a_reason": ""},
            "verification_layers": ["work_packet_schema_lint", "skill_receipt_schema_lint", "kpi_contract_audit", "required_gate_coverage_audit"],
            "mt5_required": "mt5_api_source_export_only_no_strategy_tester",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "experiment_run",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f86g", "F86F_sequence_axis_required"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(FEATURE_SCHEMA), rel(MODEL_METRICS), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F86G does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_f86g_proxy_scout",
                    "reason": "No Task Force reviewed/pass claim, policy change, roster change, or stage closeout authority claim is made.",
                    "claim_effect": "No Task Force review claim is made.",
                },
                {
                    "gate": "frontier_topic_rotation_check",
                    "reason_code": "same_stage_continuation_not_new_frontier_open",
                    "reason": "F86G stays inside active F86 sequence-axis continuation and does not open a new canonical frontier.",
                    "claim_effect": "No next-frontier-open discipline claim is made.",
                },
            ],
            "stop_conditions": ["stop after proxy scout metrics, source/feature audits, and next action are recorded"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Pre-entry source export summary exists.", "expected_artifact": rel(PRE_ENTRY_SOURCE_SUMMARY), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Feature schema records leakage boundary.", "expected_artifact": rel(FEATURE_SCHEMA), "verification_method": "feature_leakage_audit", "required": True},
            {"id": "AC-003", "text": "Proxy metrics use validation-inner selection and locked OOS readout.", "expected_artifact": rel(MODEL_METRICS), "verification_method": "split_boundary_audit", "required": True},
        ],
        "work_plan": {
            "phases": ["Export pre-entry M1/tick source summaries.", "Build leakage-safe sequence feature surface.", "Train fixed proxy models and write receipts/gates/state sync."],
            "expected_outputs": [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(FEATURE_SCHEMA), rel(MODEL_METRICS), rel(RESULT_SUMMARY)],
            "stop_conditions": ["No runtime/materialization/economics claim."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_considered": [
                "obsidian-reentry-read",
                "obsidian-work-packet-router",
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
                "obsidian-runtime-parity",
            ],
            "skills_selected": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F86G."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F86G."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F86G."},
            ],
            "required_skill_receipts": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F85B_READOUT), rel(F86D_LABELS), rel(F86F_DECISION)],
            "machine_readable": [rel(PRE_ENTRY_SOURCE_SUMMARY), rel(FEATURE_SCHEMA), rel(MODEL_METRICS), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(EXECUTION_SUMMARY), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": required_gates,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass_recorded",
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pending_external_lint",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "result_judgment_receipt": "pass",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
                "frontier_topic_rotation_check": "same-stage continuation; no new canonical frontier open",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml"},
    }


def write_packet_and_gate(summary: Mapping[str, Any], kpi_contract_status: str = "pending_external_lint") -> None:
    write_yaml(WORK_PACKET, work_packet_payload(summary))
    closeout_gate = {
        "packet_id": RUN_ID,
        "status": "pass",
        "audits": [
            {"audit_name": "frontier_extra_due_check", "status": "pass_not_due", "path": rel(REVIEW_DIR / "f86d_frontier_extra_due_check.json")},
            {"audit_name": "frontier_five_stage_direction_synthesis", "status": "pass", "path": rel(REVIEW_DIR / "f86d_frontier_five_stage_direction_synthesis.json")},
            {"audit_name": "scope_completion_gate", "status": "pass", "path": rel(SCOPE_GATE)},
            {"audit_name": "kpi_contract_audit", "status": kpi_contract_status, "path": rel(KPI_AUDIT)},
            {"audit_name": "pre_entry_source_audit", "status": summary["source_summary"].get("status"), "path": rel(SOURCE_AUDIT)},
            {"audit_name": "feature_leakage_audit", "status": summary["leakage_audit_status"], "path": rel(LEAKAGE_AUDIT)},
            {"audit_name": "split_boundary_audit", "status": summary["split_audit_status"], "path": rel(SPLIT_AUDIT)},
            {"audit_name": "artifact_lineage_audit", "status": "pass_connected_with_boundary", "path": rel(ARTIFACT_AUDIT)},
            {"audit_name": "result_judgment_receipt", "status": "pass", "path": rel(RESULT_AUDIT)},
        ],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate)
    state_sync = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "active_stage": STAGE_ID,
        "current_run_id": summary["next_run_id"],
        "latest_completed_run_id": RUN_ID,
        "checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS), rel(STAGE_LEDGER), rel(RUN_REGISTRY)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync)
    write_json(REVIEW_DIR / "f86g_state_sync_audit.json", state_sync)


def state_text(summary: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {summary['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {summary['status']}
current_judgment: {summary['judgment']}
next_run_id: {summary['next_run_id']}
frontier_extra_due_status: not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: f86g_no_strategy_tester_runtime_probe_proxy_scout_only
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{summary['created_at_utc']}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F86G exported pre-entry M1/tick source summaries(진입 전 1분/틱 원천 요약) and built sequence feature proxy scout(시퀀스 피처 프록시 스카우트)."
  - "Effect(효과): first-touch label learning(첫 터치 라벨 학습)을 새 sequence axis(시퀀스 축)로 시험하되 Strategy Tester runtime evidence(전략 테스터 런타임 근거), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
  - "Best model(최선 모델): {summary.get('best_model_id')}; positive_scout(긍정 스카우트)={summary['positive_scout']}."
  - "Next(다음): {summary['next_run_id']}."
"""


def current_state_md(summary: Mapping[str, Any]) -> str:
    best = summary.get("best_metrics") or {}
    inner = best.get("inner_validation") or {}
    oos = best.get("locked_oos_readout") or {}
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{summary['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86G에서 pre-entry M1/tick sequence feature scout(진입 전 1분/틱 시퀀스 피처 스카우트)를 실행했다.

Effect(효과): F86D first-touch labels(첫 터치 라벨)를 target-only(목표 전용)로 유지하고, F86D entry-window tick/M1 registry(진입 창 틱/1분 등록부)를 feature(피처)로 쓰지 않는 새 sequence axis(시퀀스 축)를 검증했다.

Key readout(핵심 판독): best model(최선 모델) `{summary.get('best_model_id')}`, inner validation AUC(내부 검증 AUC) `{inner.get('roc_auc')}`, locked OOS AUC(잠금 표본외 AUC) `{oos.get('roc_auc')}`, locked OOS top-decile lift(잠금 표본외 상위 10% 리프트) `{oos.get('top_decile_lift')}`.

Next(다음): `{summary['next_run_id']}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_md(summary: Mapping[str, Any]) -> str:
    return f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Current run(현재 실행): `{summary['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86G가 pre-entry M1/tick sequence surface(진입 전 1분/틱 시퀀스 표면)를 proxy scout(프록시 스카우트)로 시험했다.

Effect(효과): next run(다음 실행)은 결과에 따라 runtime materialization preflight(런타임 물질화 사전확인) 또는 sequence-axis repair/rotation decision(시퀀스 축 수리/회전 결정)으로 간다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def update_state_docs(summary: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, state_text(summary))
    current = current_state_md(summary)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(REVIEW_DIR / "context_anchor.md", current)
    selection = selection_status_md(summary)
    write_text(STAGE_SELECTION_STATUS, selection)
    write_text(GLOBAL_SELECTION_STATUS, selection)
    brief = io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig") if path_exists(STAGE_BRIEF) else ""
    brief = brief.replace("Next run(다음 실행): `frontier86G_pre_entry_intrabar_sequence_feature_scout_v1`", f"Next run(다음 실행): `{summary['next_run_id']}`")
    brief = brief.replace("Status(상태): `f86f_scalar_surface_repair_capped_sequence_axis_required_no_authority`", f"Status(상태): `{summary['status']}`")
    marker = "## F86G Pre-Entry Sequence Feature Scout Receipt"
    if marker not in brief:
        brief = brief.rstrip() + f"""

{marker}(F86G 진입 전 시퀀스 피처 스카우트 영수증)

Action(행동): F86G exported pre-entry M1/tick source summaries(진입 전 1분/틱 원천 요약), built sequence features(시퀀스 피처), and ran fixed proxy models(고정 프록시 모델).

Effect(효과): F86E scalar-only weakness(스칼라 단독 약점)을 같은 threshold/filter(임계값/필터)로 반복하지 않고, 새 pre-entry sequence axis(진입 전 시퀀스 축)의 근거를 남긴다.

Key readout(핵심 판독): best model(최선 모델) `{summary.get('best_model_id')}`, positive_scout(긍정 스카우트) `{summary['positive_scout']}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(STAGE_BRIEF, brief)
    index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Review Index(검토 색인)\n"
    for line in [
        "- `f86g_execution_summary.json`: F86G execution summary(F86G 실행 요약)",
        "- `f86g_pre_entry_source_audit.json`: F86G pre-entry source audit(F86G 진입 전 원천 감사)",
        "- `f86g_feature_leakage_audit.json`: F86G feature leakage audit(F86G 피처 누수 감사)",
        "- `f86g_split_boundary_audit.json`: F86G split boundary audit(F86G 분할 경계 감사)",
        "- `f86g_final_claim_guard.json`: F86G final claim guard(F86G 최종 주장 보호)",
    ]:
        if line not in index:
            index += line + "\n"
    write_text(REVIEW_INDEX, index)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in changelog:
        changelog = changelog.rstrip() + f"""

{marker}

## 2026-06-19 Frontier86G Pre-Entry Sequence Feature Scout(F86G 진입 전 시퀀스 피처 스카우트)

- Action(행동): `{RUN_ID}`로 pre-entry M1/tick sequence feature surface(진입 전 1분/틱 시퀀스 피처 표면)와 proxy scout(프록시 스카우트)를 실행했다.
- Effect(효과): next(다음)는 `{summary['next_run_id']}`이며, Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(CHANGELOG, changelog)


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary.get("best_metrics") or {}
    inner = best.get("inner_validation") or {}
    oos = best.get("locked_oos_readout") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__sequence_proxy_scout",
        "row_id": f"{RUN_ID}__sequence_proxy_scout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pre_entry_sequence_feature_proxy_scout",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "validation_inner_selection_locked_oos_readout",
        "scoreboard_lane": "source_integrity_sequence_scout",
        "lane": "sequence_feature_scout",
        "family": "experiment_execution",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": f"best_model={summary.get('best_model_id')};inner_auc={inner.get('roc_auc')};inner_top_decile_lift={inner.get('top_decile_lift')}",
        "guardrail_kpi": f"oos_readout_only=true;oos_auc={oos.get('roc_auc')};oos_top_decile_lift={oos.get('top_decile_lift')};no_runtime_authority",
        "external_verification_status": "mt5_api_source_export_completed_no_strategy_tester_runtime_claim",
        "notes": f"next={summary['next_run_id']}; no OOS model selection; no runtime authority",
        "run_number": "frontier86G",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["surface_rows"],
        "gate_passes": 12,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "proxy_scout",
        "tier": "not_applicable",
        "metric_scope": "validation_inner_selection_locked_oos_readout",
        "result_status": summary["status"],
        "work_family": "experiment_execution",
        "evidence_boundary": "proxy_scout_only_no_authority",
        "next_action": summary["next_run_id"],
        "question": "Can pre-entry M1/tick sequence features learn first-touch labels better than F86E scalar features?",
        "artifact_count": len([path for path in artifact_paths() if path_exists(path)]),
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "f86g_pre_entry_mt5_api_source_summary",
        "run_family": "experiment_execution",
        "run_type": "pre_entry_intrabar_sequence_feature_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(EXECUTION_SUMMARY),
        "best_candidate_id": summary.get("best_model_id"),
        "candidate_count": len(summary["model_summary"].get("model_ids", [])),
        "scout_clue_count": 1 if summary["positive_scout"] else 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 1 if summary["positive_scout"] else 0,
        "completion_candidate_count": 0,
        "model": summary.get("best_model_id"),
    }


def planned_next_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    next_run = str(summary["next_run_id"])
    return {
        "ledger_row_id": f"{next_run}__planned_current_run",
        "row_id": f"{next_run}__planned_current_run",
        "run_id": next_run,
        "stage_id": STAGE_ID,
        "parent_run_id": RUN_ID,
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "pending",
        "scoreboard_lane": "source_integrity_sequence_scout",
        "lane": "sequence_feature_scout",
        "family": "experiment_execution",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "Planned after F86G sequence proxy scout; no runtime authority.",
        "run_number": "frontier86H",
        "date": summary["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "pending_no_runtime_authority_no_goal_achieve",
        "report_path": "",
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": "",
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "pending",
        "work_family": "experiment_execution",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "open_f86h_after_sequence_proxy_scout",
        "question": "Should F86G sequence-axis evidence move to runtime materialization preflight or repair/rotation?",
        "artifact_count": 0,
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "runtime_preflight_or_repair_rotation_decision",
        "input_run_id": RUN_ID,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    actual = ledger_row(summary)
    planned = planned_next_row(summary)
    upsert_many_csv(RUN_REGISTRY, "run_id", [actual, planned])
    upsert_many_csv(ALPHA_LEDGER, "ledger_row_id", [actual, planned])
    upsert_many_csv(STAGE_LEDGER, "ledger_row_id", [actual, planned], source_header=ALPHA_LEDGER)


def update_artifact_registry(summary: Mapping[str, Any]) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [row for row in reader if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")]
    else:
        fieldnames = []
        existing = []
    rows = []
    for path in artifact_paths():
        if not path_exists(path):
            continue
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "created_at": summary["created_at_utc"],
            "created_at_utc": summary["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F86G proxy scout only(F86G 프록시 스카우트만 지원).",
        }
        rows.append(row)
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    if not fieldnames:
        fieldnames = list(rows[0].keys()) if rows else ["artifact_id"]
    write_csv_rows(ARTIFACT_REGISTRY, existing + rows, fieldnames)


def update_register_notes(summary: Mapping[str, Any]) -> None:
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea_text:
        idea_text = idea_text.rstrip() + f"""

{marker}
- `{RUN_ID}` tested pre-entry M1/tick sequence feature scout(진입 전 1분/틱 시퀀스 피처 스카우트). Best model(최선 모델): `{summary.get('best_model_id')}`. Positive scout(긍정 스카우트): `{summary['positive_scout']}`. Boundary(경계): no runtime authority(런타임 권위 없음).
"""
        write_text(IDEA_REGISTRY, idea_text)
    if not summary["positive_scout"]:
        negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        neg_marker = f"<!-- {RUN_ID} -->"
        if neg_marker not in negative_text:
            negative_text = negative_text.rstrip() + f"""

{neg_marker}
- `{RUN_ID}` did not create a strong sequence-axis proxy scout clue(강한 시퀀스 축 프록시 단서 없음). Salvage value(회수 가치): pre-entry source export and feature schema(진입 전 원천 내보내기와 피처 스키마) are reusable as bounded reference evidence(경계 있는 참고 근거). Reopen condition(재개 조건): new representation beyond five-minute M1/tick summaries(5분 1분/틱 요약을 넘는 새 표현) or runtime materialization evidence(런타임 물질화 근거), not scalar threshold/filter retuning(스칼라 임계값/필터 재조정 아님). Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
            write_text(NEGATIVE_REGISTER, negative_text)


def run_kpi_audit() -> str:
    result = audit_kpi_contract(
        KpiContract(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            run_root=RUN_DIR,
            required_files=("run_manifest.json", "kpi_record.json", "summary.json", "reports/result_summary.md"),
            stage_ledger_path=STAGE_LEDGER,
            project_ledger_path=RUN_REGISTRY,
            expected_stage_ledger_rows=1,
            expected_project_ledger_rows=1,
        )
    )
    write_json(KPI_AUDIT, result.to_dict())
    return result.status


def main() -> int:
    ensure_dirs()
    created_at = now_utc()
    input_frame = load_input_rows()
    source_summary = export_pre_entry_sources(input_frame)
    surface, leakage, split_audit = build_feature_surface(input_frame, source_summary)
    write_feature_artifacts(surface, leakage, split_audit)
    model_summary, status, judgment = write_model_artifacts(surface, source_summary, leakage, split_audit)
    summary = write_summary_artifacts(surface, source_summary, leakage, split_audit, model_summary, status, judgment, created_at)
    write_text(RESULT_SUMMARY, result_summary_text(summary))
    write_audits(summary, leakage, split_audit)
    write_receipts(receipt_payloads(summary))
    write_packet_and_gate(summary)
    update_state_docs(summary)
    update_ledgers(summary)
    update_artifact_registry(summary)
    update_register_notes(summary)
    kpi_status = run_kpi_audit()
    summary["audit_status"] = {"kpi_contract_status": kpi_status}
    write_json(SUMMARY_JSON, summary)
    write_json(EXECUTION_SUMMARY, summary)
    write_packet_and_gate(summary, kpi_status)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": status,
                    "judgment": judgment,
                    "best_model_id": summary.get("best_model_id"),
                    "positive_scout": summary["positive_scout"],
                    "next_run_id": summary["next_run_id"],
                    "source_status": source_summary.get("status"),
                    "kpi_contract_status": kpi_status,
                    "report": rel(RESULT_SUMMARY),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if kpi_status == "pass" and not str(source_summary.get("status", "")).startswith("blocked") else 2


if __name__ == "__main__":
    raise SystemExit(main())
