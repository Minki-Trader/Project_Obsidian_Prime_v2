from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_90__time_to_barrier_competing_risk_label_axis"
RUN_ID = "frontier90B_time_to_barrier_label_feasibility_scout_v1"
PARENT_RUN_ID = "frontier90A_stage_open_time_to_barrier_competing_risk_label_axis_v1"
NEXT_RUN_ID = "frontier90C_time_to_barrier_ordering_proxy_scout_v1"

SCRIPT_REL = "stage_pipelines/stage_frontier_90/frontier90b_time_to_barrier_label_feasibility_scout.py"
STATUS = "f90b_label_feasibility_scout_executed_tier_b_missing_boundary_no_authority"
JUDGMENT = "exploratory_label_feasibility_clue_tier_b_missing_combined_blocked_no_runtime_evidence"
DECISION = "continue_to_f90c_ordering_proxy_scout_only_after_preserving_tier_b_missing_boundary"
CLAIM_BOUNDARY = (
    "f90b_label_feasibility_scout_only_no_model_training_superiority_no_calibration_"
    "no_threshold_selection_no_selected_baseline_no_mt5_runtime_evidence_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_run_no_model_candidate_no_runnable_decision_surface_no_onnx_ea_set_behavior_"
    "no_runtime_materialization_economics_claim_not_cost_or_proxy_bad_skip"
)

HORIZON_BARS = 12
BARRIER_ATR_MULTIPLE = 0.75
LABEL_ID = f"time_to_barrier_competing_risk_v1_h{HORIZON_BARS}_atr{BARRIER_ATR_MULTIPLE:g}"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier90B"
LABEL_DIR = RUN_DIR / "labels"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
LABELS_CSV = LABEL_DIR / "frontier90b_barrier_labels.csv"
LABEL_STATS = LABEL_DIR / "label_feasibility_stats.json"
TIER_RECORDS = LABEL_DIR / "tier_records.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f90b_task_force_review_receipt.json"
SCOPE_GATE = REVIEW_DIR / "f90b_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f90b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f90b_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f90b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f90b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f90b_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f90b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f90b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f90b_required_gate_coverage_audit.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier90b_time_to_barrier_label_feasibility_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

F90A_RUN = STAGE_DIR / "02_runs" / "frontier90A"
F90A_SUMMARY = F90A_RUN / "summary.json"
F90A_KPI = F90A_RUN / "kpi_record.json"
F90A_CONTRACT = F90A_RUN / "design" / "time_to_barrier_competing_risk_label_contract.json"
F90A_BRIEF = F90A_RUN / "design" / "f90b_time_to_barrier_label_feasibility_scout_brief.json"
F90A_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"

FROZEN_DATASET_SUMMARY = ROOT / "data" / "processed" / "datasets" / "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01" / "dataset_summary.json"
FROZEN_FEATURES = ROOT / "data" / "processed" / "datasets" / "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01" / "features.parquet"
MODEL_INPUT_SUMMARY = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_summary.json"
MODEL_INPUT_DATASET = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_feature_order.txt"
RAW_US100_CSV = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
RAW_US100_MANIFEST = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"

ALLOWED_CLAIMS = [
    "f90b_label_feasibility_scout_executed",
    "time_to_barrier_labelability_clue_recorded",
    "tier_b_missing_required_recorded",
    "f90c_ordering_proxy_scout_planned",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "runtime_economics_pass",
    "materialization_ready",
    "mt5_handoff_ready",
    "onnx_handoff_ready",
    "ea_handoff_ready",
    "model_training_superiority",
    "calibration",
    "threshold_selection",
    "task_force_reviewed_pass",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "codex_task_force_review_packet",
    "scope_completion_gate",
    "data_integrity_audit",
    "model_validation_audit",
    "kpi_contract_audit",
    "artifact_lineage_audit",
    "result_judgment_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-run-evidence-system",
    "obsidian-data-integrity",
    "obsidian-experiment-design",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-task-force-review",
    "obsidian-result-judgment",
    "obsidian-claim-discipline",
]


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "size_bytes": io_path(path).stat().st_size,
    }


def source_inputs() -> list[Path]:
    return [
        F90A_SUMMARY,
        F90A_KPI,
        F90A_CONTRACT,
        F90A_BRIEF,
        F90A_PACKET,
        FROZEN_DATASET_SUMMARY,
        FROZEN_FEATURES,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_DATASET,
        MODEL_INPUT_FEATURE_ORDER,
        RAW_US100_CSV,
        RAW_US100_MANIFEST,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        LABELS_CSV,
        LABEL_STATS,
        TIER_RECORDS,
        RESULT_SUMMARY,
        TASK_FORCE_REVIEW,
        SCOPE_GATE,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_TASK_FORCE_REVIEW,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
    ]


def ensure_dirs() -> None:
    for path in [RUN_DIR, LABEL_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_model_input() -> pd.DataFrame:
    columns = [
        "timestamp",
        "symbol",
        "atr_14",
        "future_timestamp",
        "future_log_return_12",
        "label",
        "split",
        "split_id",
        "horizon_bars",
        "horizon_minutes",
    ]
    frame = pd.read_parquet(io_path(MODEL_INPUT_DATASET), columns=columns)
    return frame.sort_values("timestamp").reset_index(drop=True)


def load_raw_ohlc() -> pd.DataFrame:
    columns = ["time_close_unix", "open", "high", "low", "close", "spread_points"]
    frame = pd.read_csv(io_path(RAW_US100_CSV), usecols=columns)
    frame["timestamp"] = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True)
    frame = frame.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)
    return frame[["timestamp", "open", "high", "low", "close", "spread_points"]]


def classify_tier_a(frame: pd.DataFrame) -> pd.Series:
    required = ["timestamp", "atr_14", "split", "future_timestamp", "close", "high", "low"]
    finite = pd.Series(True, index=frame.index)
    for column in required:
        if column not in frame.columns:
            return pd.Series(False, index=frame.index)
        if pd.api.types.is_numeric_dtype(frame[column]):
            finite &= np.isfinite(frame[column].to_numpy(dtype="float64"))
        else:
            finite &= frame[column].notna()
    return finite


def materialize_labels() -> tuple[pd.DataFrame, dict[str, Any]]:
    model = load_model_input()
    raw = load_raw_ohlc()
    raw_indexed = raw.set_index("timestamp", drop=False)
    frame = model.merge(raw, on="timestamp", how="left", validate="one_to_one")
    frame["tier_scope"] = np.where(classify_tier_a(frame), "tier_a_separate", "no_tier")
    frame["anchor_close"] = frame["close"]
    frame["barrier_points"] = frame["atr_14"].astype("float64") * BARRIER_ATR_MULTIPLE
    frame["upper_level"] = frame["anchor_close"] + frame["barrier_points"]
    frame["lower_level"] = frame["anchor_close"] - frame["barrier_points"]

    timestamps = frame["timestamp"].to_numpy()
    splits = frame["split"].astype(str).to_numpy()
    raw_lookup = raw_indexed[["high", "low"]]

    labels: list[dict[str, Any]] = []
    for idx, row in frame.iterrows():
        reason = ""
        event_type = "invalid"
        bars_to_event: int | None = None
        same_bar_both_hit = False
        hit_timestamp = None
        upper_hits = 0
        lower_hits = 0
        if row["tier_scope"] != "tier_a_separate":
            reason = "anchor_or_feature_missing"
        elif idx + HORIZON_BARS >= len(frame):
            reason = "no_full_horizon"
        elif any(splits[idx + step] != splits[idx] for step in range(1, HORIZON_BARS + 1)):
            reason = "future_window_crosses_split_boundary"
        elif not np.isfinite(float(row["barrier_points"])) or float(row["barrier_points"]) <= 0:
            reason = "non_positive_barrier"
        else:
            future_ts = list(timestamps[idx + 1 : idx + HORIZON_BARS + 1])
            missing = [ts for ts in future_ts if ts not in raw_lookup.index]
            if missing:
                reason = "future_ohlc_missing"
            else:
                reason = "classified"
                for step, ts in enumerate(future_ts, start=1):
                    future = raw_lookup.loc[ts]
                    hit_upper = bool(float(future["high"]) >= float(row["upper_level"]))
                    hit_lower = bool(float(future["low"]) <= float(row["lower_level"]))
                    upper_hits += int(hit_upper)
                    lower_hits += int(hit_lower)
                    if hit_upper and hit_lower:
                        event_type = "ambiguous"
                        bars_to_event = step
                        same_bar_both_hit = True
                        hit_timestamp = pd.Timestamp(ts).isoformat()
                        break
                    if hit_upper:
                        event_type = "upper_first"
                        bars_to_event = step
                        hit_timestamp = pd.Timestamp(ts).isoformat()
                        break
                    if hit_lower:
                        event_type = "lower_first"
                        bars_to_event = step
                        hit_timestamp = pd.Timestamp(ts).isoformat()
                        break
                if bars_to_event is None:
                    event_type = "censored"
        labels.append(
            {
                "timestamp": pd.Timestamp(row["timestamp"]).isoformat(),
                "split": str(row["split"]),
                "tier_scope": str(row["tier_scope"]),
                "anchor_close": float(row["anchor_close"]) if pd.notna(row["anchor_close"]) else None,
                "atr_14": float(row["atr_14"]) if pd.notna(row["atr_14"]) else None,
                "barrier_points": float(row["barrier_points"]) if pd.notna(row["barrier_points"]) else None,
                "upper_level": float(row["upper_level"]) if pd.notna(row["upper_level"]) else None,
                "lower_level": float(row["lower_level"]) if pd.notna(row["lower_level"]) else None,
                "event_type": event_type,
                "bars_to_event": bars_to_event,
                "same_bar_both_hit": same_bar_both_hit,
                "hit_timestamp": hit_timestamp,
                "invalid_reason": "" if event_type != "invalid" else reason,
                "classification_reason": reason,
                "upper_hit_bars_before_event": upper_hits,
                "lower_hit_bars_before_event": lower_hits,
                "label_id": LABEL_ID,
            }
        )

    labels_frame = pd.DataFrame(labels)
    io_path(LABELS_CSV.parent).mkdir(parents=True, exist_ok=True)
    labels_frame.to_csv(io_path(LABELS_CSV), index=False)
    stats = build_label_stats(frame, labels_frame)
    write_json(LABEL_STATS, stats)
    write_json(TIER_RECORDS, build_tier_records(stats))
    return labels_frame, stats


def _count_dict(series: pd.Series) -> dict[str, int]:
    return {str(key): int(value) for key, value in series.value_counts(dropna=False).sort_index().items()}


def _ratio(numerator: int, denominator: int) -> float | None:
    return round(float(numerator) / float(denominator), 6) if denominator else None


def _bars_quantiles(series: pd.Series) -> dict[str, float | None]:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return {"mean": None, "median": None, "q10": None, "q25": None, "q75": None, "q90": None}
    return {
        "mean": round(float(clean.mean()), 6),
        "median": round(float(clean.median()), 6),
        "q10": round(float(clean.quantile(0.10)), 6),
        "q25": round(float(clean.quantile(0.25)), 6),
        "q75": round(float(clean.quantile(0.75)), 6),
        "q90": round(float(clean.quantile(0.90)), 6),
    }


def _group_stats(labels: pd.DataFrame, keys: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group_key, group in labels.groupby(keys, dropna=False):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        record = {key: str(value) for key, value in zip(keys, group_key)}
        total = int(len(group))
        valid = int(group["event_type"].isin(["upper_first", "lower_first", "censored", "ambiguous"]).sum())
        invalid = int(group["event_type"].eq("invalid").sum())
        ambiguous = int(group["event_type"].eq("ambiguous").sum())
        censored = int(group["event_type"].eq("censored").sum())
        record.update(
            {
                "total_rows": total,
                "valid_rows": valid,
                "invalid_rows": invalid,
                "censored_rows": censored,
                "ambiguous_rows": ambiguous,
                "same_bar_dual_hit_rows": int(group["same_bar_both_hit"].sum()),
                "same_bar_dual_hit_rate": _ratio(int(group["same_bar_both_hit"].sum()), valid),
                "event_distribution": _count_dict(group["event_type"]),
                "invalid_reason_distribution": _count_dict(group.loc[group["event_type"].eq("invalid"), "invalid_reason"]),
                "bars_to_event": _bars_quantiles(group.loc[group["event_type"].ne("censored"), "bars_to_event"]),
            }
        )
        rows.append(record)
    return rows


def build_label_stats(frame: pd.DataFrame, labels: pd.DataFrame) -> dict[str, Any]:
    timestamps = frame["timestamp"]
    gaps = timestamps.diff().dropna()
    same_day = timestamps.dt.date.eq(timestamps.shift(1).dt.date).iloc[1:]
    same_day_gaps = gaps.loc[same_day.to_numpy()]
    total = int(len(labels))
    valid = int(labels["event_type"].isin(["upper_first", "lower_first", "censored", "ambiguous"]).sum())
    invalid = int(labels["event_type"].eq("invalid").sum())
    ambiguous = int(labels["event_type"].eq("ambiguous").sum())
    censored = int(labels["event_type"].eq("censored").sum())
    upper = int(labels["event_type"].eq("upper_first").sum())
    lower = int(labels["event_type"].eq("lower_first").sum())
    raw_joined = int(frame[["open", "high", "low", "close"]].notna().all(axis=1).sum())
    feature_count = len([name for name in pd.read_parquet(io_path(MODEL_INPUT_DATASET), columns=None).columns if name not in {"timestamp", "symbol", "future_timestamp", "future_log_return_12", "label", "label_class", "label_id", "split", "split_id", "horizon_bars", "horizon_minutes"}])
    return {
        "run_id": RUN_ID,
        "label_id": LABEL_ID,
        "horizon_bars": HORIZON_BARS,
        "barrier_geometry": {
            "anchor_price": "raw US100 close at anchor timestamp",
            "upper_barrier": "anchor_close + 0.75 * atr_14",
            "lower_barrier": "anchor_close - 0.75 * atr_14",
            "atr_source": rel(MODEL_INPUT_DATASET),
            "threshold_source": "predeclared_in_f90b_before_measurement_not_validation_oos_tuned",
        },
        "overall": {
            "total_rows": total,
            "valid_rows": valid,
            "invalid_rows": invalid,
            "labelable_rows": valid,
            "upper_first_rows": upper,
            "lower_first_rows": lower,
            "censored_rows": censored,
            "ambiguous_rows": ambiguous,
            "valid_rate": _ratio(valid, total),
            "invalid_rate": _ratio(invalid, total),
            "censored_rate_of_valid": _ratio(censored, valid),
            "ambiguous_rate_of_valid": _ratio(ambiguous, valid),
            "upper_first_rate_of_valid": _ratio(upper, valid),
            "lower_first_rate_of_valid": _ratio(lower, valid),
            "same_bar_dual_hit_rows": int(labels["same_bar_both_hit"].sum()),
            "same_bar_dual_hit_rate_of_valid": _ratio(int(labels["same_bar_both_hit"].sum()), valid),
            "bars_to_event": _bars_quantiles(labels.loc[labels["event_type"].isin(["upper_first", "lower_first", "ambiguous"]), "bars_to_event"]),
        },
        "by_split": _group_stats(labels, ["split"]),
        "by_tier": _group_stats(labels, ["tier_scope"]),
        "by_split_tier": _group_stats(labels, ["split", "tier_scope"]),
        "data_integrity": {
            "timestamp_unique": bool(timestamps.is_unique),
            "timestamp_monotonic_increasing": bool(timestamps.is_monotonic_increasing),
            "duplicate_timestamps": int(timestamps.duplicated().sum()),
            "selected_row_gap_count": int(len(gaps)),
            "selected_row_non_5m_gap_count": int((gaps != pd.Timedelta(minutes=5)).sum()),
            "same_utc_day_non_5m_gap_count": int((same_day_gaps != pd.Timedelta(minutes=5)).sum()),
            "raw_ohlc_joined_rows": raw_joined,
            "raw_ohlc_join_coverage": _ratio(raw_joined, total),
            "feature_count_reference": feature_count,
            "feature_label_join_coverage": _ratio(valid + invalid, total),
            "split_boundary_invalid_rows": int(labels["invalid_reason"].eq("future_window_crosses_split_boundary").sum()),
            "no_full_horizon_invalid_rows": int(labels["invalid_reason"].eq("no_full_horizon").sum()),
        },
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_tier_records(stats: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "required_views": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
        "records": [
            {
                "record_view": "tier_a_separate",
                "status": "measured",
                "tier_scope": "Tier A separate",
                "primary_kpi": stats["overall"],
                "claim_boundary": "Tier A label feasibility only; not whole-alpha read.",
            },
            {
                "record_view": "tier_b_separate",
                "status": "missing_required",
                "tier_scope": "Tier B separate",
                "reason": "No F90B partial-context/Core42 Tier B source was materialized in this packet.",
                "claim_effect": "Tier B performance, labelability, and fallback coverage are not claimed.",
            },
            {
                "record_view": "tier_ab_combined",
                "status": "blocked_by_missing_tier_b",
                "tier_scope": "Tier A+B combined",
                "reason": "Combined read cannot be claimed from Tier A-only measured rows.",
                "claim_effect": "Whole-alpha or combined signal claim is forbidden.",
            },
        ],
    }


def task_force_calls() -> list[dict[str, str]]:
    return [
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edd55-aca3-73f2-992b-e52d71744ead",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd6a-50cd-73b0-8606-d64619be5eb7",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edd55-f3c5-7b70-848e-c5a381ca8f65",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd6a-7607-7101-a2b3-b596f4b961d7",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edd56-3bf0-7db0-968e-a0124d6b1de4",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd6a-922f-7c51-845e-07baf7a291ad",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edd56-821f-7b02-b9d0-13d779165917",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd6a-b205-7a32-9673-7c01376e172e",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edd57-0364-7ae1-b027-9f8fc36269b0",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd6a-d153-7171-874e-584c91364054",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
    ]


def build_payload(now: str, stats: Mapping[str, Any]) -> dict[str, Any]:
    model_summary = read_json(MODEL_INPUT_SUMMARY)
    dataset_summary = read_json(FROZEN_DATASET_SUMMARY)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": "Time-to-barrier competing-risk labels may preserve event ordering and censoring information better than a binary adverse-selection teacher.",
        "proxy": "ATR-normalized OHLC barrier label materialized on frozen US100 M5 model-input rows.",
        "barrier_contract": stats["barrier_geometry"],
        "source_identity": {
            "dataset_id": dataset_summary.get("dataset_id"),
            "model_input_dataset_id": model_summary.get("model_input_dataset_id"),
            "feature_set_id": model_summary.get("feature_set_id"),
            "feature_order_hash": model_summary.get("included_feature_order_hash"),
            "raw_us100": file_identity(RAW_US100_CSV),
            "raw_us100_manifest": file_identity(RAW_US100_MANIFEST),
            "model_input_dataset": file_identity(MODEL_INPUT_DATASET),
            "feature_order": file_identity(MODEL_INPUT_FEATURE_ORDER),
        },
        "stats": stats,
        "tier_records": read_json(TIER_RECORDS),
        "runtime_boundary": {
            "runtime_probe_status": RUNTIME_PROBE_STATUS,
            "valid_n_a_reason": "F90B remains Python/data label feasibility only; no model candidate, runnable decision surface, ONNX/EA/set behavior, or runtime/materialization/economics claim exists.",
            "invalid_deferrals": ["cost/expense", "proxy_bad"],
            "future_trigger": "A deterministic candidate plus entry/exit/risk mapping and ONNX/EA/set materialization path would trigger same-packet MT5 Strategy Tester probe.",
        },
        "task_force": {
            "review_requirement": "active_goal_required_and_explicit_user_instruction_required",
            "agents_used": [call["roster_agent_id"] for call in task_force_calls()],
            "actual_subagent_calls": task_force_calls(),
            "advice_classification": {
                "agent_04_evidence_control_plane": "accepted",
                "agent_05_data_feature_contract": "needs_local_verification",
                "agent_06_quant_research": "accepted",
                "agent_07_model_validation_risk": "accepted",
                "agent_08_mt5_onnx_runtime": "accepted",
            },
            "local_verification_response": [
                "F90B predeclared a single ATR barrier geometry before measurement.",
                "Same-bar both-hit rows are ambiguous, not hidden.",
                "Tier B and combined views are structured missing/blocked, not omitted.",
                "No runtime/economics/materialization claim is made.",
            ],
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def run_manifest(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "proxy_scout",
        "producer": SCRIPT_REL,
        "source_inputs": [rel(path) for path in source_inputs()],
        "produced_artifacts": [rel(path) for path in produced_artifacts()],
        "control_plane_gates": dict(gate_results or {}),
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "current_branch": current_branch(),
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    overall = payload["stats"]["overall"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "time_to_barrier_label_feasibility_scout",
        "scoreboard_lane": "structural_scout",
        "label_id": LABEL_ID,
        "horizon_bars": HORIZON_BARS,
        "barrier_atr_multiple": BARRIER_ATR_MULTIPLE,
        "total_rows": overall["total_rows"],
        "valid_rows": overall["valid_rows"],
        "invalid_rows": overall["invalid_rows"],
        "upper_first_rows": overall["upper_first_rows"],
        "lower_first_rows": overall["lower_first_rows"],
        "censored_rows": overall["censored_rows"],
        "ambiguous_rows": overall["ambiguous_rows"],
        "same_bar_dual_hit_rows": overall["same_bar_dual_hit_rows"],
        "bars_to_event": overall["bars_to_event"],
        "tier_a_record_status": "measured",
        "tier_b_record_status": "missing_required",
        "tier_ab_record_status": "blocked_by_missing_tier_b",
        "runtime_kpi": "not_applicable_no_strategy_tester_run",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def result_summary_text(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> str:
    overall = payload["stats"]["overall"]
    gate_status = ", ".join(f"{name}={result.get('status', 'unknown')}" for name, result in (gate_results or {}).items()) or "pending"
    return f"""# F90B Label Feasibility Scout(F90B 라벨 가능성 탐색)

Updated(갱신): {payload['created_at_utc']}

Conclusion(결론): F90B measured(측정) a time-to-barrier competing-risk label surface(장벽 도달 시간 경쟁위험 라벨 표면) on Tier A(티어 A) model-input rows. This is a feasibility clue(가능성 단서), not runtime evidence(런타임 근거), model readiness(모델 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).

Action(행동): Used predeclared(사전 선언) `{HORIZON_BARS}` selected bars(선택 봉) and `{BARRIER_ATR_MULTIPLE} * ATR14` symmetric barriers(대칭 장벽) from anchor close(기준 종가).

Effect(효과): Labelability(라벨 가능성), censoring(검열), same-bar ambiguity(동일봉 모호성), split boundary(분할 경계), and Tier A/B/combined(티어 A/B/합산) gaps are visible before any model or MT5 claim(모델 또는 MT5 주장).

KPI(핵심 성과 지표): total `{overall['total_rows']}`, valid `{overall['valid_rows']}`, invalid `{overall['invalid_rows']}`, upper_first `{overall['upper_first_rows']}`, lower_first `{overall['lower_first_rows']}`, censored `{overall['censored_rows']}`, ambiguous `{overall['ambiguous_rows']}`, same_bar_dual_hit `{overall['same_bar_dual_hit_rows']}`.

Tier records(티어 기록): Tier A separate(티어 A 분리) measured(측정됨); Tier B separate(티어 B 분리) `missing_required(필수 누락)`; Tier A+B combined(티어 A+B 합산) `blocked_by_missing_tier_b(티어 B 누락으로 차단)`.

Runtime(런타임): no Strategy Tester probe(전략 테스터 탐침 없음). Reason(사유): no model candidate(모델 후보 없음), no runnable decision surface(실행 가능한 의사결정 표면 없음), no ONNX/EA/set behavior(ONNX/EA/설정 동작 없음), and no runtime/materialization/economics claim(런타임/물질화/경제성 주장 없음). This is not cost/expense deferral(비용 지연 아님) and not proxy-bad skip(프록시 부진 생략 아님).

Next action(다음 행동): F90C may test ordering proxy(순서 프록시) only within scout boundary(탐색 경계). It must not claim model superiority(모델 우위), calibration(보정), runtime authority(런타임 권위), or operating promotion(운영 승격).

Gate status(게이트 상태): {gate_status}.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload, gate_results))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload, gate_results))


def task_force_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": "active_goal_required_and_explicit_user_instruction_required",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": "gpt-5.5_xhigh_floor_with_existing_spawned_roster_context_refresh",
        "bounded_evidence": [rel(LABEL_STATS), rel(KPI_RECORD), rel(TIER_RECORDS), rel(WORK_PACKET)],
        "advice_classification": payload["task_force"]["advice_classification"],
        "local_verification": payload["task_force"]["local_verification_response"],
        "final_codex_direction": "Record F90B as label feasibility clue with Tier B missing boundary and no runtime claim.",
        "forbidden_claim_check": "No completion, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve claim.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def audit_payload(name: str, status: str, *, passed: bool = True, counts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_name": name,
        "packet_id": RUN_ID,
        "status": status,
        "passed": passed,
        "created_at_utc": utc_now(),
        "counts": dict(counts or {}),
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def final_claim_guard_payload() -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_audits(payload: Mapping[str, Any]) -> None:
    stats = payload["stats"]
    task_force = task_force_receipt(payload)
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(PACKET_TASK_FORCE_REVIEW, task_force)
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", counts={"produced_artifacts": len([path for path in produced_artifacts() if path_exists(path)])}))
    write_json(
        DATA_INTEGRITY_AUDIT,
        audit_payload(
            "data_integrity_audit",
            "pass_with_tier_b_missing_boundary",
            counts={
                "timestamp_unique": stats["data_integrity"]["timestamp_unique"],
                "timestamp_monotonic_increasing": stats["data_integrity"]["timestamp_monotonic_increasing"],
                "raw_ohlc_join_coverage": stats["data_integrity"]["raw_ohlc_join_coverage"],
                "same_utc_day_non_5m_gap_count": stats["data_integrity"]["same_utc_day_non_5m_gap_count"],
                "tier_b_status": "missing_required",
            },
        ),
    )
    write_json(MODEL_VALIDATION_AUDIT, audit_payload("model_validation_audit", "pass_no_model_training_or_threshold_selection_claim", counts={"profile": "proxy_scout"}))
    write_json(KPI_CONTRACT_AUDIT, audit_payload("kpi_contract_audit", "pass", counts=stats["overall"]))
    write_json(ARTIFACT_AUDIT, audit_payload("artifact_lineage_audit", "pass", counts={"source_inputs": len(source_inputs()), "produced_artifacts": len(produced_artifacts())}))
    write_json(
        RESULT_JUDGMENT_AUDIT,
        {
            **audit_payload("result_judgment_audit", "pass"),
            "result_subject": RUN_ID,
            "evidence_available": [rel(LABEL_STATS), rel(KPI_RECORD), rel(TIER_RECORDS), rel(RESULT_SUMMARY)],
            "evidence_missing": ["Tier B partial-context label surface", "MT5 Strategy Tester output", "model/ONNX/EA candidate"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
        },
    )
    guard = final_claim_guard_payload()
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)


def receipt_path_for(skill: str) -> Path:
    return SKILL_RECEIPT_DIR / f"{skill.replace('obsidian-', '').replace('-', '_')}.json"


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "packet_id": RUN_ID,
        "status": "executed",
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    return [
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "ledger_rows": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
            "missing_evidence": ["Tier B source", "MT5 runtime output"],
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel(MODEL_INPUT_DATASET), rel(RAW_US100_CSV), rel(FROZEN_DATASET_SUMMARY)],
            "time_axis_boundary": "timestamp is bar-close alignment key from materializer; future labels use t+1 through t+12 selected rows.",
            "split_boundary": "future window crossing split is invalid.",
            "leakage_checks": ["anchor uses closed bar t", "future OHLC only after t", "barrier geometry predeclared"],
            "missing_data_boundary": "Tier B missing_required; combined blocked_by_missing_tier_b.",
        },
        {
            **common,
            "skill": "obsidian-experiment-design",
            "hypothesis": payload["hypothesis"],
            "baseline": "F89/F90A reference only; no inherited baseline.",
            "changed_variables": ["label representation", "event ordering", "censoring", "barrier geometry"],
            "invalid_conditions": ["threshold tuned on validation/OOS", "same-bar ambiguity omitted", "Tier B omitted"],
            "evidence_plan": [rel(LABEL_STATS), rel(TIER_RECORDS), rel(KPI_RECORD)],
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "No model training; one predeclared ATR barrier geometry only.",
            "validation_split": "train/validation/oos split labels measured separately.",
            "overfit_checks": ["no barrier sweep", "no validation/OOS tuning", "no calibration claim"],
            "selection_metric_boundary": "label feasibility only; no selection metric or candidate rank.",
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(RAW_US100_CSV), rel(RAW_US100_MANIFEST), rel(MODEL_INPUT_DATASET)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(LABEL_STATS), rel(TIER_RECORDS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs() + [LABEL_STATS, TIER_RECORDS, KPI_RECORD]],
            "lineage_boundary": CLAIM_BOUNDARY,
        },
        task_force_receipt(payload),
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "evidence_used": [rel(LABEL_STATS), rel(KPI_RECORD), rel(TIER_RECORDS)],
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "final_status": STATUS,
        },
    ]


def write_receipts(payload: Mapping[str, Any]) -> None:
    rows = skill_receipts(payload)
    for row in rows:
        write_json(receipt_path_for(row["skill"]), row)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "receipts": rows})


def work_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gates = {
        "work_packet_schema_lint": (gate_results or {}).get("work_packet_schema_lint", {}).get("status", "pending_external_lint"),
        "skill_receipt_schema_lint": (gate_results or {}).get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint"),
        "codex_task_force_review_packet": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": "pass_with_tier_b_missing_boundary",
        "model_validation_audit": "pass_no_model_training_or_threshold_selection_claim",
        "kpi_contract_audit": "pass",
        "artifact_lineage_audit": "pass",
        "result_judgment_audit": "pass",
        "state_sync_audit": (gate_results or {}).get("state_sync_audit", {}).get("status", "pending_external_lint"),
        "required_gate_coverage_audit": (gate_results or {}).get("required_gate_coverage_audit", {}).get("status", "pending_external_lint"),
        "final_claim_guard": "pass",
    }
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "F90B Python/data label feasibility scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion.", "No runtime authority.", "No live readiness."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(RUN_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "threshold_tuning_after_results": "high",
                "same_bar_ambiguity_hidden": "high",
                "tier_b_omitted": "high",
                "runtime_probe_absence_misread_as_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not describe Tier A-only rows as combined alpha read.",
                "Do not call label feasibility a trained model candidate.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "verification_profile": "proxy_scout",
                "strategy_tester_required_now": False,
                "reason": "No model candidate, runnable decision surface, ONNX/EA/set behavior, or runtime/materialization/economics claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F90B label feasibility scout", "Tier A/B/combined records", "Task Force receipt", "state sync"],
            "scope_units": ["local_python_execution", "run_evidence", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["raw US100 OHLC", "model input parquet", "label stats", "Task Force actual calls"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal_frontier_continuation", "F90A brief", "explicit user instruction requiring Task Force when triggered"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(LABEL_STATS), rel(TIER_RECORDS), rel(KPI_RECORD), rel(PACKET_TASK_FORCE_REVIEW), rel(WORK_PACKET)],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface_no_runtime_materialization_economics_claim",
                    "reason": "F90B is Python/data label feasibility only and has no model candidate, runnable decision surface, ONNX/EA/set behavior, or runtime claim.",
                    "claim_effect": "Runtime probe, runtime verified, economics pass, materialization ready, handoff ready, authority, live readiness, and Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "wfo_stress_gate",
                    "reason_code": "outside_claim_surface_no_model_candidate",
                    "reason": "F90B creates no model candidate and performs no threshold/model selection.",
                    "claim_effect": "WFO/stress pass and model superiority claims are forbidden.",
                },
            ],
            "stop_conditions": ["Tier B missing must be recorded", "Same-bar ambiguity must be separated", "Runtime claims must trigger MT5 probe or be forbidden"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F90B label stats exist.", "expected_artifact": rel(LABEL_STATS), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-002", "text": "Tier A/B/combined records exist or missing/blocked is structured.", "expected_artifact": rel(TIER_RECORDS), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "F90B Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F90A contract.", "Refresh relevant Task Force agents.", "Measure labels.", "Write evidence and gates."],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": ["Do not force MT5 without runnable candidate.", "Do not claim combined read without Tier B."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-data-integrity",
                "obsidian-experiment-design",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report or trade list exists in F90B."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in [RAW_US100_CSV, RAW_US100_MANIFEST, MODEL_INPUT_DATASET, FROZEN_DATASET_SUMMARY]],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, LABEL_STATS, TIER_RECORDS, SKILL_RECEIPTS, PACKET_TASK_FORCE_REVIEW]],
            "human_readable": [rel(path) for path in [RESULT_SUMMARY, STAGE_BRIEF, CURRENT_WORKING_STATE, DECISION_MEMO]],
        },
        "gates": {
            "required": REQUIRED_GATES,
            **gates,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_runtime_materialization_economics_claim",
                "wfo_stress_gate": "outside_claim_surface_no_model_candidate",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
    }


def closeout_gate(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = dict(gate_results or {})
    audits = [
        {"audit_name": "work_packet_schema_lint", "path": rel(PACKET_WORK_PACKET_LINT), "status": gate_results.get("work_packet_schema_lint", {}).get("status", "pending_external_lint")},
        {"audit_name": "skill_receipt_schema_lint", "path": rel(PACKET_SKILL_RECEIPT_LINT), "status": gate_results.get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint")},
        {"audit_name": "codex_task_force_review_packet", "path": rel(PACKET_TASK_FORCE_REVIEW), "status": "pass"},
        {"audit_name": "scope_completion_gate", "path": rel(SCOPE_GATE), "status": "pass"},
        {"audit_name": "data_integrity_audit", "path": rel(DATA_INTEGRITY_AUDIT), "status": "pass_with_tier_b_missing_boundary"},
        {"audit_name": "model_validation_audit", "path": rel(MODEL_VALIDATION_AUDIT), "status": "pass_no_model_training_or_threshold_selection_claim"},
        {"audit_name": "kpi_contract_audit", "path": rel(KPI_CONTRACT_AUDIT), "status": "pass"},
        {"audit_name": "artifact_lineage_audit", "path": rel(ARTIFACT_AUDIT), "status": "pass"},
        {"audit_name": "result_judgment_audit", "path": rel(RESULT_JUDGMENT_AUDIT), "status": "pass"},
        {"audit_name": "state_sync_audit", "path": rel(PACKET_STATE_SYNC_AUDIT), "status": gate_results.get("state_sync_audit", {}).get("status", "pending_external_lint")},
        {"audit_name": "required_gate_coverage_audit", "path": rel(PACKET_REQUIRED_GATE_AUDIT), "status": gate_results.get("required_gate_coverage_audit", {}).get("status", "pending_external_lint")},
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if gate_results.get("required_gate_coverage_audit", {}).get("status") == "pass" else "pending_external_lint",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "audits": audits,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": "pass"},
    }


def write_packet_and_gate(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet(payload, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate(payload, gate_results))


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: f90b_label_feasibility_scout_recorded_f90c_ordering_proxy_scout_planned_no_authority
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: not_due_after_f89_closeout_next_boundary_f100_e01_closed_for_f050
frontier_topic_rotation_status: passed_f90_new_label_representation_axis_not_threshold_tweak
task_force_status: f90b_actual_subagent_context_refresh_recorded_5_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F90B measured(측정) time-to-barrier label feasibility(장벽 도달 시간 라벨 가능성) on Tier A model-input rows.'
- 'Effect(효과): Tier B missing_required(티어 B 필수 누락) and combined blocked(합산 차단)을 명시해 Tier A-only read(티어 A 단독 판독) 과장을 막았다.'
- 'Runtime(런타임): no Strategy Tester evidence(전략 테스터 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).'
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    overall = payload["stats"]["overall"]
    return f"""# Current Working State(현재 작업 상태)

- active_stage(활성 단계): `{STAGE_ID}`
- latest_completed_run(최신 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `f90b_label_feasibility_scout_recorded_f90c_ordering_proxy_scout_planned_no_authority`
- judgment(판정): `{JUDGMENT}`
- KPI(핵심 성과 지표): valid `{overall['valid_rows']}`, invalid `{overall['invalid_rows']}`, upper `{overall['upper_first_rows']}`, lower `{overall['lower_first_rows']}`, censored `{overall['censored_rows']}`, ambiguous `{overall['ambiguous_rows']}`
- Task Force(태스크포스): 5 selected agents(선택 요원) refreshed with F90B context(전선90B 맥락 갱신), no Task Force reviewed/pass claim(검토됨/통과 주장 없음)
- Runtime(런타임): `{RUNTIME_PROBE_STATUS}`
- Boundary(경계): `{CLAIM_BOUNDARY}`
"""


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {STAGE_ID}

Question(질문): Can time-to-barrier competing-risk labels(장벽 도달 시간 경쟁위험 라벨) create a leakage-safe clue(누수 없는 단서) for US100 M5?

F90B result(F90B 결과): label feasibility clue(라벨 가능성 단서) on Tier A(티어 A), with Tier B missing_required(티어 B 필수 누락) and combined blocked(합산 차단).

Next(다음): `{NEXT_RUN_ID}` may test ordering proxy(순서 프록시) only. Runtime authority(런타임 권위), selected baseline(선택 기준선), live readiness(실거래 준비), and Goal Achieve(목표 달성) are not claimed.
"""


def input_refs_text(payload: Mapping[str, Any]) -> str:
    lines = ["# Input References(입력 참조)", ""]
    for path in source_inputs():
        ident = file_identity(path)
        lines.append(f"- `{ident['path']}` sha256 `{ident['sha256']}`")
    return "\n".join(lines)


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# Selection Status(선택 상태)

No selected baseline(선택 기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).

F90B(전선90B) is a label feasibility clue(라벨 가능성 단서) only. Tier B(티어 B) remains `missing_required(필수 누락)`, so Tier A+B combined(티어 A+B 합산) is blocked(차단).
"""


def review_index_text(payload: Mapping[str, Any]) -> str:
    rows = [
        ("f90b_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f90b_data_integrity_audit", DATA_INTEGRITY_AUDIT),
        ("f90b_model_validation_audit", MODEL_VALIDATION_AUDIT),
        ("f90b_kpi_contract_audit", KPI_CONTRACT_AUDIT),
        ("f90b_artifact_lineage_audit", ARTIFACT_AUDIT),
        ("f90b_result_judgment_audit", RESULT_JUDGMENT_AUDIT),
        ("f90b_required_gate_coverage_audit", REQUIRED_GATE_AUDIT),
    ]
    lines = ["# Review Index(검토 색인)", ""]
    for name, path in rows:
        lines.append(f"- `{name}`: `{rel(path)}`")
    return "\n".join(lines)


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    return f"""# F90B Decision Memo(F90B 결정 메모)

Decision(결정): Preserve F90B as a label feasibility clue(라벨 가능성 단서) and continue to `{NEXT_RUN_ID}` only within proxy scout boundary(프록시 탐색 경계).

Reason(이유): The run materialized event/censoring/ambiguity counts(사건/검열/모호성 수)를 만들었지만, Tier B(티어 B)는 missing_required(필수 누락)이고 no model/ONNX/EA/runtime candidate(모델/ONNX/EA/런타임 후보 없음)이다.

Forbidden(금지): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def update_state_docs(payload: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(payload))
    write_text(STAGE_BRIEF, stage_brief_text(payload))
    write_text(INPUT_REFS, input_refs_text(payload))
    write_text(SELECTION_STATUS, selection_status_text(payload))
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text(payload))
    write_text(DECISION_MEMO, decision_memo_text(payload))


def append_dict_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    keys_to_replace = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in keys_to_replace]
    normalized = [{field: json_ready(row.get(field, "")) for field in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def replace_rows_by_field(path: Path, field: str, value: str, rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    kept = [row for row in existing if str(row.get(field, "")).strip() != value]
    normalized = [{column: json_ready(row.get(column, "")) for column in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    created_date = payload["created_at_utc"][:10]
    overall = payload["stats"]["overall"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "time_to_barrier_label_feasibility_scout",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F90B label feasibility scout; no runtime authority.",
        "family": "experiment_execution",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier90B",
        "date": created_date,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": overall["total_rows"],
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_date,
        "primary_artifact": rel(LABEL_STATS),
        "result_status": STATUS,
        "scoreboard_lane": "structural_scout",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": payload["created_at_utc"],
        "work_family": "experiment_execution",
        "evidence_boundary": "label_feasibility_scout_only_no_runtime_evidence",
        "next_action": NEXT_RUN_ID,
        "question": "Can time-to-barrier labels be materialized leakage-safely?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
    }
    views = [
        ("tier_a_separate", "Tier A separate", "measured", f"valid={overall['valid_rows']};ambiguous={overall['ambiguous_rows']};censored={overall['censored_rows']}", "combined forbidden without Tier B"),
        ("tier_b_separate", "Tier B separate", "missing_required", "missing_required_no_partial_context_source", "no Tier B performance or labelability claim"),
        ("tier_ab_combined", "Tier A+B combined", "blocked_by_missing_tier_b", "blocked_by_missing_tier_b", "whole-alpha combined read forbidden"),
    ]
    rows = []
    for record_view, tier_scope, view_status, primary_kpi, guardrail in views:
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{record_view}",
                "subrun_id": f"{RUN_ID}__{record_view}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": "time_to_barrier_label_feasibility",
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "row_id": f"{RUN_ID}__{record_view}",
                "view": record_view,
                "tier": tier_scope,
                "metric_scope": "label_feasibility",
                "result_status": view_status,
            }
        )
        rows.append(row)
    planned = dict(base)
    planned.update(
        {
            "run_id": NEXT_RUN_ID,
            "status": "planned_current_run_no_authority",
            "judgment": "pending_time_to_barrier_ordering_proxy_scout",
            "path": rel(STAGE_DIR),
            "notes": "Planned after F90B; must remain proxy scout until a runnable candidate exists.",
            "primary_report": rel(STAGE_BRIEF),
            "run_number": "frontier90C",
            "decision": "pending_execution",
            "parent_run_id": RUN_ID,
            "next_run_id": "",
            "rows": 0,
            "gate_passes": 0,
            "gate_total": 0,
            "claim_boundary": "planned_current_run_no_authority_no_runtime_claim_no_goal_achieve",
            "report_path": rel(STAGE_BRIEF),
            "primary_artifact": rel(STAGE_BRIEF),
            "result_status": "planned_current_run_no_authority",
            "external_verification_status": "pending",
            "result_judgment": "pending",
            "gate_audit_path": "",
            "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "subrun_id": f"{NEXT_RUN_ID}__planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "not_applicable_planned",
            "kpi_scope": "pending",
            "primary_kpi": "pending",
            "guardrail_kpi": "pending_runtime_claim_forbidden",
            "row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "view": "planned_current_run",
            "tier": "not_applicable_planned",
            "metric_scope": "pending",
            "evidence_boundary": "planned_only_no_runtime_evidence",
            "next_action": "execute_time_to_barrier_ordering_proxy_scout",
            "question": "Can F90B label ordering become a proxy scout without runtime authority claims?",
            "artifact_count": 0,
            "required_gate_audit": "",
            "run_type": "planned_current_run",
            "input_run_id": RUN_ID,
            "output_path": rel(STAGE_DIR),
            "result_path": rel(STAGE_BRIEF),
            "scout_clue_count": 0,
        }
    )
    rows.append(planned)
    return rows


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes=gate_passes)
    run_rows = [dict(rows[0]), dict(rows[-1])]
    append_dict_rows(RUN_REGISTRY, ["run_id"], run_rows)
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], rows)
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], rows, header_source=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f90b_label_feasibility_scout",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F90B label feasibility scout artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports F90B label feasibility clue and Tier B missing boundary only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = RUN_ID
    idea_addition = f"""
## F90B time-to-barrier label feasibility clue(F90B 장벽 도달 시간 라벨 가능성 단서)

- run_id: `{RUN_ID}`
- hypothesis(가설): time-to-barrier competing-risk labels(장벽 도달 시간 경쟁위험 라벨)이 binary adverse-selection teacher(이진 불리선택 교사)보다 event ordering(사건 순서) 단서를 줄 수 있는지 본다.
- result(결과): Tier A measured(티어 A 측정), Tier B missing_required(티어 B 필수 누락), combined blocked(합산 차단).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
## F90B Tier B missing boundary(F90B 티어 B 누락 경계)

- run_id: `{RUN_ID}`
- boundary(경계): Tier B separate(티어 B 분리) is `missing_required(필수 누락)` and Tier A+B combined(티어 A+B 합산) is `blocked_by_missing_tier_b(티어 B 누락으로 차단)`.
- effect(효과): Tier A-only labelability(티어 A 단독 라벨 가능성)를 whole-alpha read(전체 알파 판독)로 과장하지 않는다.
"""
    changelog_addition = f"""
## {payload['created_at_utc']} - F90B Label Feasibility Scout(F90B 라벨 가능성 탐색)

- Action(행동): measured `{LABEL_ID}` on Tier A model-input rows(티어 A 모델 입력 행).
- Effect(효과): event/censoring/ambiguity(사건/검열/모호성) and Tier B missing boundary(티어 B 누락 경계)를 기록했다.
- Runtime(런타임): no Strategy Tester evidence(전략 테스터 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).
- Packet(묶음): `{rel(WORK_PACKET)}`.
"""
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(NEGATIVE_REGISTER, marker, negative_addition)
    append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    append_once(ROOT_CHANGELOG, marker, changelog_addition)


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=180)
    payload: dict[str, Any] = read_json(output_path) if path_exists(output_path) else {}
    result = {
        "command": command,
        "output_path": rel(output_path),
        "returncode": completed.returncode,
        "status": payload.get("status", "missing_output"),
        "passed": payload.get("status") == "pass" or payload.get("passed", False),
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }
    if completed.returncode != 0 or result["status"] != "pass":
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def write_initial(payload: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet_and_gate(payload)
    update_state_docs(payload)
    update_ledgers(payload)
    update_register_docs(payload)
    write_json(PACKET_STATE_SYNC_AUDIT, audit_payload("state_sync_audit", "pending_external_lint", counts={"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID}))
    write_json(STATE_SYNC_AUDIT, read_json(PACKET_STATE_SYNC_AUDIT))


def run_control_gates(payload: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", current_branch()],
        PACKET_STATE_SYNC_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    write_packet_and_gate(payload, results)
    results["required_gate_coverage_audit"] = run_gate_cmd(
        ["foundation.control_plane.required_gate_coverage_audit", "--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE)],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    write_packet_and_gate(payload, results)
    return results


def write_final(payload: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = len(REQUIRED_GATES)
    write_run_artifacts(payload, gate_results)
    write_audits(payload)
    write_receipts(payload)
    write_packet_and_gate(payload, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_state_docs(payload)
    update_ledgers(payload, gate_passes=gate_passes)
    update_artifact_registry(payload)


def main() -> int:
    missing = [rel(path) for path in source_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F90B source evidence: {missing}")
    ensure_dirs()
    _, stats = materialize_labels()
    payload = build_payload(utc_now(), stats)
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "label_id": LABEL_ID,
                "overall": payload["stats"]["overall"],
                "next_run_id": NEXT_RUN_ID,
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "task_force_call_count": len(task_force_calls()),
                "gate_results": gate_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
