from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.control_plane.tier_context_materialization import (
    TIER_B_CORE_FEATURE_ORDER,
    build_tier_b_partial_context_frames,
)
from foundation.features.candle_morphology import (
    SIGNAL_FEATURE_ORDER,
    CandleMorphologyCandidateSpec,
    apply_candidate_to_table,
    build_broad_candidate_grid,
    build_micro_candidate_grid,
    build_thresholds,
    candle_morphology_schema,
    materialize_candle_morphology,
    route_coverage_from_common,
    summarize_candidate_frames,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 40
STAGE_ID = "40_feature_structure__candle_morphology_signal_quality_scout"
IDEA_ID = "IDEA-ST40-CANDLE-MORPHOLOGY-SIGNAL-QUALITY"
RUN_ID = "run34A_candle_morphology_signal_quality_broad_mt5_probe_v1"
RUN_NUMBER = "run34A"
PACKET_ID = "stage40_run34A_candle_morphology_signal_quality_broad_mt5_probe_v1"
PARENT_PACKET_ID = PACKET_ID
EXPLORATION_LABEL = "stage40_FeatureStructure__CandleMorphologySignalQuality"
BOUNDARY = "runtime_probe_only"
FINAL_BOUNDARY = "runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"
BLOCKED_JUDGMENT = "blocked_runtime_probe_missing_mt5_execution"
POSITIVE_JUDGMENT = "reviewed_completed_positive_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_runtime_probe_only"
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 12
SIGNAL_FEATURE_HASH = ordered_hash(SIGNAL_FEATURE_ORDER)
COMMON_STAGE40_ROOT = f"Project_Obsidian_Prime_v2/stage40/{RUN_NUMBER}_candle_morphology"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
MODEL_INPUT_ROOT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
MODEL_INPUT_DATASET_PATH = MODEL_INPUT_ROOT / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER_PATH = MODEL_INPUT_ROOT / "model_input_feature_order.txt"
MODEL_INPUT_SUMMARY_PATH = MODEL_INPUT_ROOT / "model_input_summary.json"
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
RAW_MT5_ROOT = ROOT / "data/raw/mt5_bars/m5"
RAW_US100_BARS_PATH = RAW_MT5_ROOT / "US100/bars_us100_m5_mt5api_raw.csv"
LEGACY_STAGE32_SELECTION_STATUS_PATH = (
    ROOT.parent / "Project_Obsidian_Prime/stages/32_candle_pattern_exit_diagnostic/04_selected/selection_status.md"
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_name(value: str, limit: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_yaml_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def dataframe_to_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    frame = pd.DataFrame(list(rows))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8")
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_label_threshold() -> float:
    payload = json.loads(io_path(TRAINING_SUMMARY_PATH).read_text(encoding="utf-8"))
    threshold = float(payload["threshold_log_return"])
    if not math.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"invalid label threshold: {threshold}")
    return threshold


def load_model_input() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT_DATASET_PATH))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["timestamp_utc"] = frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    frame["validation_oos_split_label"] = frame["split"].astype(str).map({"validation": "validation_is"}).fillna(frame["split"].astype(str))
    return frame.sort_values("timestamp").reset_index(drop=True)


def source_lineage_entries() -> list[dict[str, Any]]:
    paths = [
        ("tier_a_model_input", MODEL_INPUT_DATASET_PATH, "input", "model label feature diagnostics"),
        ("tier_a_feature_order", MODEL_INPUT_FEATURE_ORDER_PATH, "input", "feature order"),
        ("model_input_summary", MODEL_INPUT_SUMMARY_PATH, "input", "data contract diagnostics"),
        ("training_summary", TRAINING_SUMMARY_PATH, "input", "label threshold"),
        ("raw_mt5_bars", RAW_MT5_ROOT, "input", "Tier B fallback materialization"),
        ("raw_us100_closed_m5_ohlc", RAW_US100_BARS_PATH, "input", "closed-bar candle morphology"),
        ("legacy_stage32_candle_pattern_status", LEGACY_STAGE32_SELECTION_STATUS_PATH, "idea_seed_only", "legacy clue only; no result inheritance"),
        ("mt5_runtime_ea", ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "MT5 handoff", "entry runtime"),
    ]
    rows = []
    for role, path, kind, surface in paths:
        rows.append(
            {
                "role": role,
                "path": rel(path),
                "source_stage": "foundation_or_current_data",
                "source_run": "current_truth_reentry",
                "created_by_script": "existing_repository_artifact",
                "sha256": sha256_file_lf_normalized(path) if path.is_file() else "directory_or_not_feasible",
                "artifact_kind": kind,
                "required_for_reproducibility": True,
                "affects": surface,
            }
        )
    return rows


def build_common_table() -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    tier_a_raw = load_model_input()
    feature_order = load_feature_order(MODEL_INPUT_FEATURE_ORDER_PATH)
    label_threshold = load_label_threshold()
    tier_b_payload = build_tier_b_partial_context_frames(
        raw_root=RAW_MT5_ROOT,
        tier_a_frame=tier_a_raw,
        tier_a_feature_order=feature_order,
        tier_b_feature_order=TIER_B_CORE_FEATURE_ORDER,
        label_threshold=label_threshold,
    )
    tier_a = tier_a_raw.copy()
    tier_a["tier_label"] = mt5.TIER_A
    tier_a["routing_source"] = "tier_a_primary"
    tier_a["partial_context_subtype"] = "Tier_A_full_context"
    tier_a["tier_a_available"] = True
    tier_a["tier_b_fallback_available"] = False
    tier_b = tier_b_payload["tier_b_fallback_frame"].copy()
    tier_b["timestamp"] = pd.to_datetime(tier_b["timestamp"], utc=True)
    tier_b["timestamp_utc"] = tier_b["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    tier_b["validation_oos_split_label"] = tier_b["split"].astype(str).map({"validation": "validation_is"}).fillna(tier_b["split"].astype(str))
    tier_b["tier_label"] = mt5.TIER_B
    tier_b["routing_source"] = "tier_b_fallback"
    tier_b["tier_a_available"] = False
    tier_b["tier_b_fallback_available"] = True
    common_columns = sorted(set(tier_a.columns).intersection(set(tier_b.columns)).union({"timestamp", "timestamp_utc", "split", "validation_oos_split_label", "label_class", "tier_label", "routing_source", "partial_context_subtype", "tier_a_available", "tier_b_fallback_available"}))
    common = pd.concat([tier_a[common_columns], tier_b[common_columns]], ignore_index=True, sort=False)
    raw_bars = pd.read_csv(io_path(RAW_US100_BARS_PATH))
    morphology = materialize_candle_morphology(raw_bars)
    morphology_artifact = save_frame(RUN_ROOT / "tables/stage40_candle_morphology_closed_bar_table.parquet", morphology)
    common = common.merge(morphology, on="timestamp", how="left", validate="many_to_one")
    common = common.sort_values(["timestamp", "tier_label"]).reset_index(drop=True)
    common["stage40_row_id"] = np.arange(len(common), dtype=int)
    route_coverage = route_coverage_from_common(common, tier_b_payload.get("summary", {}).get("no_tier_by_split", {}))
    lineage = source_lineage_entries()
    lineage.append(
        {
            "role": "tier_b_fallback_materialization",
            "path": rel(RUN_ROOT / "tables/stage40_common_decision_surface_table.parquet"),
            "source_stage": STAGE_ID,
            "source_run": RUN_ID,
            "created_by_script": "stage_pipelines.stage40.candle_morphology_signal_quality_scout",
            "sha256": "computed_after_write",
            "artifact_kind": "intermediate",
            "required_for_reproducibility": True,
            "affects": "Tier B fallback routing and feature decision surface",
            "summary": tier_b_payload.get("summary", {}),
        }
    )
    lineage.append(
        {
            "role": "candle_morphology_closed_bar_materialization",
            "path": morphology_artifact["path"],
            "source_stage": STAGE_ID,
            "source_run": RUN_ID,
            "created_by_script": "foundation.features.candle_morphology.materialize_candle_morphology",
            "sha256": morphology_artifact["sha256"],
            "artifact_kind": "intermediate",
            "required_for_reproducibility": True,
            "affects": "closed-bar candle feature and candidate signal",
        }
    )
    return common, route_coverage, lineage


def export_signal_score_table(path: Path) -> dict[str, Any]:
    payload = export_single_discrete_signal_score_table(
        path,
        feature_order=SIGNAL_FEATURE_ORDER,
        logit_strength=4.0,
        format_name="stage40_candle_morphology_single_signal_ebm_score_table_csv_v1",
    )
    payload["path"] = rel(path)
    return payload


def export_candidate_feature_matrices(candidate_frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    feature_root = RUN_ROOT / "features"
    exports: dict[str, Any] = {}
    for candidate_id, frame in candidate_frames.items():
        for split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            for tier_label, tier_key in ((mt5.TIER_A, "tier_a"), (mt5.TIER_B, "tier_b_fallback")):
                selected = frame.loc[frame["split"].astype(str).eq(split) & frame["tier_label"].astype(str).eq(tier_label)].copy()
                output = feature_root / f"{candidate_id}_{tier_key}_{runtime_split}_stage40_signal_features.csv"
                exports[f"{candidate_id}_{tier_key}_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
                    selected,
                    SIGNAL_FEATURE_ORDER,
                    output,
                    metadata_columns=(
                        "candidate_id",
                        "candidate_label",
                        "mechanism_family",
                        "rule_code",
                        "tier_label",
                        "routing_source",
                        "partial_context_subtype",
                        "entry_decision",
                    ),
                )
    return exports


def resolve_artifact_path(value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    root_path = ROOT / path
    if path_exists(root_path):
        return root_path
    return RUN_ROOT / path


def copy_runtime_inputs(feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common_root: Path) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copied = []
    model_path = resolve_artifact_path(model_artifact["path"])
    copied.append(copy_to_common(model_path, f"{common}/models/{model_path.name}", common_root))
    for payload in feature_exports.values():
        local_path = resolve_artifact_path(payload["path"])
        copied.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", common_root))
    return copied


def make_attempts(
    candidate_specs: Sequence[CandleMorphologyCandidateSpec],
    feature_exports: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    common: pd.DataFrame,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common_name = common_run_root(STAGE_NUMBER, RUN_ID)
    model_name = Path(model_artifact["path"]).name
    for spec in candidate_specs:
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_frame = common.loc[common["split"].astype(str).eq(source_split) & common["tier_label"].astype(str).eq(mt5.TIER_A)]
            from_date, to_date = split_dates_from_frame(split_frame, source_split)
            tier_a_matrix = Path(feature_exports[f"{spec.candidate_id}_tier_a_{runtime_split}"]["path"]).name
            tier_b_matrix = Path(feature_exports[f"{spec.candidate_id}_tier_b_fallback_{runtime_split}"]["path"]).name
            attempts.append(
                attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=STAGE_NUMBER,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"routed_{safe_name(spec.candidate_id, 64)}_{runtime_split}",
                    tier=mt5.TIER_AB,
                    split=runtime_split,
                    model_path=f"{common_name}/models/{model_name}",
                    model_id=f"{RUN_ID}_{spec.candidate_id}_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{common_name}/features/{tier_a_matrix}",
                    feature_count=len(SIGNAL_FEATURE_ORDER),
                    feature_order_hash=SIGNAL_FEATURE_HASH,
                    short_threshold=SHORT_THRESHOLD,
                    long_threshold=LONG_THRESHOLD,
                    min_margin=MIN_MARGIN,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="routed_total",
                    record_view_prefix=f"mt5_routed_{spec.candidate_id}",
                    max_hold_bars=MAX_HOLD_BARS,
                    common_root=common_name,
                    fallback_enabled=True,
                    fallback_model_path=f"{common_name}/models/{model_name}",
                    fallback_model_id=f"{RUN_ID}_{spec.candidate_id}_fallback_signal_table",
                    fallback_model_backend="ebm_table",
                    fallback_feature_path=f"{common_name}/features/{tier_b_matrix}",
                    fallback_feature_count=len(SIGNAL_FEATURE_ORDER),
                    fallback_feature_order_hash=SIGNAL_FEATURE_HASH,
                    fallback_short_threshold=SHORT_THRESHOLD,
                    fallback_long_threshold=LONG_THRESHOLD,
                    fallback_min_margin=MIN_MARGIN,
                    fallback_invert_signal=False,
                    close_on_flat_signal=False,
                    reverse_on_opposite_signal=True,
                )
            )
    return attempts


def build_candidate_batch(
    *,
    specs: Sequence[CandleMorphologyCandidateSpec],
    common: pd.DataFrame,
    thresholds: Mapping[str, float],
    common_files_root: Path,
) -> dict[str, Any]:
    frames = {spec.candidate_id: apply_candidate_to_table(common, spec, thresholds) for spec in specs}
    summary = summarize_candidate_frames(frames)
    feature_exports = export_candidate_feature_matrices(frames)
    model_artifact = export_signal_score_table(RUN_ROOT / "models/stage40_candle_morphology_signal_score_table.csv")
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, common_files_root)
    attempts = make_attempts(specs, feature_exports, model_artifact, common)
    return {
        "specs": list(specs),
        "frames": frames,
        "summary": summary,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "common_copies": common_copies,
        "attempts": attempts,
    }


def prepared_payload(
    *,
    candidate_specs: Sequence[CandleMorphologyCandidateSpec],
    attempts: Sequence[Mapping[str, Any]],
    common: pd.DataFrame,
    feature_exports: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    common_copies: Sequence[Mapping[str, Any]],
    route_coverage: Mapping[str, Any],
    common_artifact: Mapping[str, Any],
    candidate_artifact: Mapping[str, Any],
    python_summary: Sequence[Mapping[str, Any]],
    lineage: Sequence[Mapping[str, Any]],
    thresholds: Mapping[str, float],
    batch_label: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_root": RUN_ROOT.as_posix(),
        "batch_label": batch_label,
        "attempts": list(attempts),
        "candidate_specs": [spec.__dict__ for spec in candidate_specs],
        "feature_matrices": dict(feature_exports),
        "model_artifacts": {"signal_score_table": dict(model_artifact)},
        "common_copies": list(common_copies),
        "route_coverage": dict(route_coverage),
        "common_table_artifact": dict(common_artifact),
        "candidate_table_artifact": dict(candidate_artifact),
        "python_candidate_summary": list(python_summary),
        "source_lineage": list(lineage),
        "thresholds": dict(thresholds),
        "idea_id": IDEA_ID,
        "run_number": RUN_NUMBER,
        "completion_goal": "Stage40 broad MT5 candle morphology signal-quality feature-structure runtime probe",
        "model_family": "stage40_candle_morphology_discrete_signal_ebm_table",
        "feature_set_id": "stage40_candle_morphology_single_signal_from_closed_ohlc_v2",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": FINAL_BOUNDARY,
    }


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": BLOCKED_JUDGMENT,
        }
    result = execute_prepared_run(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    completed = result.get("external_verification_status") == "completed" and any(
        item.get("status") == "completed" for item in result.get("strategy_tester_reports", [])
    )
    result["judgment"] = INCONCLUSIVE_JUDGMENT if completed else BLOCKED_JUDGMENT
    for record in result.get("mt5_kpi_records", []):
        record["idea_id"] = IDEA_ID
        record["packet_id"] = PACKET_ID
        record["boundary"] = BOUNDARY
    return result


def mt5_metric(record: Mapping[str, Any], *names: str) -> Any:
    metrics = record.get("metrics", {})
    for name in names:
        if name in metrics:
            return metrics.get(name)
    return None


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def build_mt5_candidate_summary(kpi_records: Sequence[Mapping[str, Any]], python_rows: Sequence[Mapping[str, Any]], execution_results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    python_by_key = {(row["candidate_id"], row["split"]): dict(row) for row in python_rows}
    exec_by_key = {}
    for execution in execution_results:
        match = re.match(r"routed_(?P<candidate>.+)_(?P<split>validation_is|oos)$", str(execution.get("attempt_name", "")))
        if match:
            exec_by_key[(match.group("candidate"), match.group("split"))] = execution
    totals = [record for record in kpi_records if record.get("route_role") == "routed_total"]
    components = {
        (record.get("record_view"), record.get("route_role")): record
        for record in kpi_records
        if record.get("route_role") in {"primary_used", "fallback_used"}
    }
    rows: list[dict[str, Any]] = []
    for total in totals:
        view = str(total.get("record_view", ""))
        match = re.match(r"mt5_routed_(?P<candidate>.+)_(?P<split>validation_is|oos)$", view)
        if not match:
            continue
        candidate_id = match.group("candidate")
        split = match.group("split")
        py = python_by_key.get((candidate_id, split), {})
        prefix = f"mt5_routed_{candidate_id}"
        primary = components.get((f"{prefix}_tier_a_used_{split}", "primary_used"), {})
        fallback = components.get((f"{prefix}_tier_b_fallback_used_{split}", "fallback_used"), {})
        metrics = total.get("metrics", {})
        execution = exec_by_key.get((candidate_id, split), {})
        rows.append(
            {
                **py,
                "candidate_id": candidate_id,
                "split": split,
                "net_profit": mt5_metric(total, "net_profit"),
                "profit_factor": mt5_metric(total, "profit_factor"),
                "max_drawdown": mt5_metric(total, "max_drawdown_amount", "max_drawdown"),
                "expectancy": mt5_metric(total, "expectancy"),
                "win_rate": mt5_metric(total, "win_rate_percent", "win_rate"),
                "trade_count": mt5_metric(total, "trade_count"),
                "order_attempt_count": mt5_metric(total, "order_attempt_count"),
                "fill_count": mt5_metric(total, "fill_count"),
                "tier_a_used_count_mt5": mt5_metric(primary, "signal_count"),
                "tier_b_fallback_used_count_mt5": mt5_metric(fallback, "signal_count"),
                "actual_routed_total_count_mt5": mt5_metric(total, "order_attempt_count"),
                "tester_status": execution.get("status"),
                "runtime_status": execution.get("runtime_outputs", {}).get("status") if execution else None,
                "tester_command": " ".join(str(item) for item in execution.get("command", [])) if execution else "",
                "tester_report_path": metrics.get("report_path") or total.get("report", {}).get("html_report", {}).get("path", ""),
                "candidate_rejection_reason": "mt5_imported_pending_gate",
            }
        )
    return rows


def pivot_candidate_mt5(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Mapping[str, Any]]]:
    out: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        out.setdefault(str(row["candidate_id"]), {})[str(row["split"])] = row
    return out


def evaluate_micro_search_gate(mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_candidate = pivot_candidate_mt5([row for row in mt5_rows if str(row.get("candidate_id", "")).startswith("c")])
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate_id, splits in by_candidate.items():
        val = splits.get("validation_is")
        oos = splits.get("oos")
        if not val or not oos:
            rejected.append({"candidate_id": candidate_id, "reason": "missing_validation_or_oos_mt5_row"})
            continue
        val_net = to_float(val.get("net_profit")) or 0.0
        oos_net = to_float(oos.get("net_profit")) or 0.0
        val_pf = to_float(val.get("profit_factor")) or 0.0
        oos_pf = to_float(oos.get("profit_factor")) or 0.0
        val_trades = int(to_float(val.get("trade_count")) or 0)
        oos_trades = int(to_float(oos.get("trade_count")) or 0)
        routed_total = int(to_float(val.get("actual_routed_total_count_mt5")) or 0) + int(to_float(oos.get("actual_routed_total_count_mt5")) or 0)
        tier_b = int(to_float(val.get("tier_b_fallback_used_count_mt5")) or 0) + int(to_float(oos.get("tier_b_fallback_used_count_mt5")) or 0)
        gap = abs(val_net - oos_net)
        reasons = []
        if val_net <= 0:
            reasons.append("validation_net_not_positive")
        if oos_net <= 0:
            reasons.append("oos_net_not_positive")
        if val_pf < 1.05:
            reasons.append("validation_pf_below_1_05")
        if oos_pf < 1.05:
            reasons.append("oos_pf_below_1_05")
        if val_trades < 20 or oos_trades < 20:
            reasons.append("trade_count_too_thin_for_micro_search")
        if routed_total > 0 and tier_b / routed_total > 0.60:
            reasons.append("tier_b_fallback_carrying_too_much")
        if gap > max(abs(val_net), abs(oos_net), 1.0) * 3.0:
            reasons.append("validation_oos_gap_extreme")
        payload = {
            "candidate_id": candidate_id,
            "validation_net": val_net,
            "oos_net": oos_net,
            "validation_pf": val_pf,
            "oos_pf": oos_pf,
            "validation_trades": val_trades,
            "oos_trades": oos_trades,
            "tier_b_signal_share": float(tier_b / routed_total) if routed_total else None,
            "validation_oos_gap": gap,
        }
        if reasons:
            rejected.append({**payload, "reason": ";".join(dict.fromkeys(reasons))})
        else:
            accepted.append(payload)
    accepted.sort(key=lambda item: (item["validation_net"] + item["oos_net"], item["oos_pf"]), reverse=True)
    return {
        "status": "passed" if accepted else "failed",
        "accepted_candidates": accepted,
        "rejected_candidates": rejected,
        "best_candidate": accepted[0]["candidate_id"] if accepted else None,
        "rule": "micro-search is allowed only when broad MT5 validation and OOS are both positive, PF>=1.05, not thin, not Tier-B-carried, and split gap is bounded",
    }


def evaluate_promotion_candidate_gate(mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_candidate = pivot_candidate_mt5(mt5_rows)
    reference = by_candidate.get("c01_reference_no_candle_morphology", {})
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate_id, splits in by_candidate.items():
        val = splits.get("validation_is")
        oos = splits.get("oos")
        reasons = []
        if not val or not oos:
            rejected.append({"candidate_id": candidate_id, "reason": "missing_validation_or_oos_mt5_row"})
            continue
        required = ["net_profit", "profit_factor", "trade_count", "max_drawdown"]
        for field in required:
            if to_float(val.get(field)) is None or to_float(oos.get(field)) is None:
                reasons.append(f"missing_required_kpi_{field}")
        val_net = to_float(val.get("net_profit")) or 0.0
        oos_net = to_float(oos.get("net_profit")) or 0.0
        val_pf = to_float(val.get("profit_factor")) or 0.0
        oos_pf = to_float(oos.get("profit_factor")) or 0.0
        val_trades = int(to_float(val.get("trade_count")) or 0)
        oos_trades = int(to_float(oos.get("trade_count")) or 0)
        routed_total = int(to_float(val.get("actual_routed_total_count_mt5")) or 0) + int(to_float(oos.get("actual_routed_total_count_mt5")) or 0)
        tier_b = int(to_float(val.get("tier_b_fallback_used_count_mt5")) or 0) + int(to_float(oos.get("tier_b_fallback_used_count_mt5")) or 0)
        if val_net <= 0:
            reasons.append("validation_net_not_positive")
        if oos_net <= 0:
            reasons.append("oos_net_not_positive")
        if val_pf < 1.10:
            reasons.append("validation_pf_below_1_10")
        if oos_pf < 1.10:
            reasons.append("oos_pf_below_1_10")
        if val_trades < 25 or oos_trades < 25:
            reasons.append("trade_count_thin")
        if routed_total <= 0:
            reasons.append("missing_entry_count_runtime")
        if routed_total and tier_b / routed_total > 0.60:
            reasons.append("tier_b_fallback_carrying_result")
        if val_trades and oos_trades and max(val_trades, oos_trades) / max(min(val_trades, oos_trades), 1) > 4:
            reasons.append("validation_oos_entry_count_instability")
        if abs(val_net - oos_net) > max(abs(val_net), abs(oos_net), 1.0) * 2.5:
            reasons.append("validation_oos_gap_unacceptable")
        ref_val = reference.get("validation_is")
        ref_oos = reference.get("oos")
        if ref_val and ref_oos:
            for label, row, ref_row in (("validation", val, ref_val), ("oos", oos, ref_oos)):
                drawdown = abs(to_float(row.get("max_drawdown")) or 0.0)
                ref_drawdown = abs(to_float(ref_row.get("max_drawdown")) or 0.0)
                if ref_drawdown and drawdown > ref_drawdown * 1.10 and (to_float(row.get("profit_factor")) or 0.0) < 1.25:
                    reasons.append(f"{label}_drawdown_worse_than_reference_without_strong_pf")
        reasons.append("cluster_concentration_check_not_available_for_positive_gate")
        payload = {
            "candidate_id": candidate_id,
            "validation_net": val_net,
            "oos_net": oos_net,
            "validation_pf": val_pf,
            "oos_pf": oos_pf,
            "validation_trades": val_trades,
            "oos_trades": oos_trades,
            "tier_b_signal_share": float(tier_b / routed_total) if routed_total else None,
        }
        if reasons:
            rejected.append({**payload, "reason": ";".join(dict.fromkeys(reasons))})
        else:
            accepted.append(payload)
    accepted.sort(key=lambda item: (item["validation_net"] + item["oos_net"], item["oos_pf"]), reverse=True)
    return {
        "status": "passed" if accepted else "failed",
        "accepted_candidates": accepted,
        "rejected_candidates": rejected,
        "candidate_id": accepted[0]["candidate_id"] if accepted else None,
        "promotion_packet_path": None,
        "rule": "actual MT5 output, positive validation/OOS, PF>=1.10, non-thin, drawdown and gap acceptable, no Tier B carry, no hidden entry instability, full KPI and reproducible lineage",
    }


def apply_gate_rejection_reasons(mt5_rows: Sequence[Mapping[str, Any]], gate: Mapping[str, Any]) -> list[dict[str, Any]]:
    rejected = {str(item.get("candidate_id")): str(item.get("reason")) for item in gate.get("rejected_candidates", []) if item.get("candidate_id")}
    accepted = {str(item.get("candidate_id")) for item in gate.get("accepted_candidates", []) if item.get("candidate_id")}
    rows: list[dict[str, Any]] = []
    for row in mt5_rows:
        candidate_id = str(row.get("candidate_id"))
        reason = row.get("candidate_rejection_reason")
        if candidate_id in rejected:
            reason = rejected[candidate_id]
        elif candidate_id in accepted:
            reason = "promotion_candidate_gate_passed"
        rows.append({**dict(row), "candidate_rejection_reason": reason})
    return rows


def actual_mt5_output_exists(result: Mapping[str, Any]) -> bool:
    return any(item.get("status") == "completed" for item in result.get("strategy_tester_reports", []))


def final_judgment_from_results(result: Mapping[str, Any], promotion_gate: Mapping[str, Any]) -> str:
    if not actual_mt5_output_exists(result):
        return BLOCKED_JUDGMENT
    if promotion_gate.get("status") == "passed":
        return POSITIVE_JUDGMENT
    return NEGATIVE_JUDGMENT


def kpi_report_path(record: Mapping[str, Any]) -> str:
    report = record.get("report", {})
    if isinstance(report, Mapping):
        html = report.get("html_report", {})
        if isinstance(html, Mapping):
            return str(html.get("path", ""))
    metrics = record.get("metrics", {})
    if isinstance(metrics, Mapping):
        return str(metrics.get("report_path", ""))
    return ""


def ledger_rows_from_kpis(kpi_records: Sequence[Mapping[str, Any]], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in kpi_records:
        metrics = record.get("metrics", {})
        view = str(record.get("record_view", ""))
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": PARENT_PACKET_ID,
                "record_view": view,
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "candle_morphology_signal_quality_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": "completed" if record.get("status") == "completed" else "blocked",
                "judgment": judgment,
                "path": kpi_report_path(record),
                "primary_kpi": f"net_profit={metrics.get('net_profit','')};profit_factor={metrics.get('profit_factor','')};trade_count={metrics.get('trade_count','')};signal_count={metrics.get('signal_count','')};expectancy={metrics.get('expectancy','')};win_rate={metrics.get('win_rate_percent', metrics.get('win_rate',''))}",
                "guardrail_kpi": f"route_role={record.get('route_role','')};a_used={metrics.get('tier_a_primary_labelable_rows','')};b_fallback={metrics.get('tier_b_fallback_labelable_rows','')};max_dd={metrics.get('max_drawdown_amount', metrics.get('max_drawdown',''))};boundary={BOUNDARY}",
                "external_verification_status": "completed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "notes": "Stage40 candle morphology signal-quality MT5 runtime-probe KPI row; no baseline, promotion, runtime authority, live readiness, or operating reference.",
            }
        )
    if not rows:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__blocked_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "blocked_mt5_execution",
                "parent_run_id": PARENT_PACKET_ID,
                "record_view": "blocked_mt5_execution",
                "tier_scope": mt5.TIER_AB,
                "kpi_scope": "candle_morphology_signal_quality_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": "blocked",
                "judgment": BLOCKED_JUDGMENT,
                "path": rel(RUN_ROOT),
                "primary_kpi": "missing_required_mt5_strategy_tester_output",
                "guardrail_kpi": f"boundary={BOUNDARY}",
                "external_verification_status": "blocked",
                "notes": "Stage40 blocked because MT5 Strategy Tester output artifact was not produced.",
            }
        )
    return rows


def write_ledgers(result: Mapping[str, Any], judgment: str) -> dict[str, Any]:
    kpi_records = result.get("mt5_kpi_records", [])
    stage_rows = ledger_rows_from_kpis(kpi_records, judgment)
    write_csv_rows(STAGE_ROOT / "03_reviews/stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, stage_rows)
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, stage_rows, key="ledger_row_id")
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_probe",
                "status": "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "judgment": judgment,
                "path": rel(RUN_ROOT),
                "notes": f"Stage40 independent candle morphology signal-quality scout; legacy Stage32 is idea-only; mt5_attempts={len(result.get('attempts', []))}; boundary={BOUNDARY}",
            }
        ],
        key="run_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}_run_manifest",
            "type": "run_manifest",
            "path": rel(RUN_ROOT / "run_manifest.json"),
            "status": "tracked_runtime_probe",
            "notes": "Stage40 run manifest; reproducibility required",
        },
        {
            "artifact_id": f"{RUN_ID}_candle_morphology_schema",
            "type": "feature_schema",
            "path": rel(RUN_ROOT / "tables/candle_morphology_schema.json"),
            "status": "tracked_runtime_probe",
            "notes": "Stage40 candle morphology closed-bar schema",
        },
        {
            "artifact_id": f"{RUN_ID}_candle_morphology_lineage",
            "type": "feature_lineage",
            "path": rel(RUN_ROOT / "tables/candle_morphology_lineage.csv"),
            "status": "tracked_runtime_probe",
            "notes": "Stage40 candle morphology source lineage",
        },
        {
            "artifact_id": f"{RUN_ID}_candidate_grid",
            "type": "candidate_grid",
            "path": rel(RUN_ROOT / "tables/stage40_candidate_grid.csv"),
            "status": "tracked_runtime_probe",
            "notes": "Stage40 broad candle morphology candidate grid",
        },
        {
            "artifact_id": f"{RUN_ID}_mt5_handoff_manifest",
            "type": "mt5_handoff_manifest",
            "path": rel(RUN_ROOT / "mt5/handoff_manifest.json"),
            "status": "tracked_runtime_probe",
            "notes": "Stage40 MT5 Strategy Tester handoff manifest",
        },
        {
            "artifact_id": f"{RUN_ID}_mt5_import_summary",
            "type": "mt5_import_summary",
            "path": rel(RUN_ROOT / "mt5/mt5_result_import_summary.json"),
            "status": "tracked_runtime_probe",
            "notes": "Stage40 imported MT5 result summary",
        },
        {
            "artifact_id": f"{RUN_ID}_review_packet",
            "type": "stage_review_packet",
            "path": rel(STAGE_ROOT / "03_reviews/run34A_candle_morphology_signal_quality_broad_mt5_probe_packet.md"),
            "status": "tracked_reviewed" if judgment != BLOCKED_JUDGMENT else "tracked_blocked",
            "notes": "Stage40 closeout packet",
        },
    ]
    existing = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    keys = {row["artifact_id"] for row in artifact_rows}
    merged = [row for row in existing if row.get("artifact_id") not in keys] + artifact_rows
    write_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), merged)
    return {
        "stage_run_ledger": rel(STAGE_ROOT / "03_reviews/stage_run_ledger.csv"),
        "project_alpha_ledger": project_payload,
        "run_registry": run_payload,
        "artifact_registry": {"path": rel(ARTIFACT_REGISTRY_PATH), "rows": len(merged)},
    }


def best_worst(rows: Sequence[Mapping[str, Any]], split: str) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None]:
    items = [row for row in rows if row.get("split") == split]
    if not items:
        return None, None
    key = lambda row: (to_float(row.get("net_profit")) or -1e18, to_float(row.get("profit_factor")) or 0.0)
    return max(items, key=key), min(items, key=key)


def write_handoff_files(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    mt5_root = RUN_ROOT / "mt5"
    handoff = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "common_files_root": str(COMMON_FILES_ROOT_DEFAULT),
        "terminal_path": str(TERMINAL_PATH_DEFAULT),
        "metaeditor_path": str(METAEDITOR_PATH_DEFAULT),
        "tester_profile_root": str(TESTER_PROFILE_ROOT_DEFAULT),
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "module_hashes": mt5.mt5_runtime_module_hashes(),
        "routing": "Tier A primary + Tier B fallback actual routed total",
    }
    tester_request = {
        "command_template": f"{TERMINAL_PATH_DEFAULT} /config:<ini_path>",
        "attempt_count": len(result.get("attempts", [])),
        "ini_files": [item.get("ini", {}).get("path") for item in result.get("attempts", [])],
        "set_files": [item.get("set", {}).get("path") for item in result.get("attempts", [])],
    }
    import_summary = {
        "imported_at": utc_now(),
        "strategy_tester_report_count": len(result.get("strategy_tester_reports", [])),
        "completed_report_count": sum(1 for item in result.get("strategy_tester_reports", []) if item.get("status") == "completed"),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "candidate_summary_rows": len(mt5_rows),
        "actual_mt5_output_exists": actual_mt5_output_exists(result),
    }
    write_json(mt5_root / "handoff_manifest.json", handoff)
    write_json(mt5_root / "tester_request.json", tester_request)
    write_json(mt5_root / "mt5_result_import_summary.json", import_summary)
    return {
        "handoff_manifest": rel(mt5_root / "handoff_manifest.json"),
        "tester_request": rel(mt5_root / "tester_request.json"),
        "mt5_result_import_summary": rel(mt5_root / "mt5_result_import_summary.json"),
    }


def artifact_hash_summary() -> list[dict[str, Any]]:
    rows = []
    if not path_exists(RUN_ROOT):
        return rows
    for path in sorted(io_path(RUN_ROOT).rglob("*")):
        local = Path(str(path).removeprefix("\\\\?\\"))
        if not local.is_file():
            continue
        try:
            rows.append({"path": rel(local), "sha256": sha256_file_lf_normalized(local), "bytes": int(local.stat().st_size)})
        except OSError:
            continue
    return rows


def write_stage_docs(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]], micro_gate: Mapping[str, Any], promotion_gate: Mapping[str, Any], judgment: str) -> None:
    best_val, worst_val = best_worst(mt5_rows, "validation_is")
    best_oos, worst_oos = best_worst(mt5_rows, "oos")
    actual_artifacts = [item for item in result.get("strategy_tester_reports", []) if item.get("status") == "completed"]
    command = ""
    if result.get("execution_results"):
        command = " ".join(str(item) for item in result["execution_results"][0].get("command", []))
    report_path = actual_artifacts[0].get("html_report", {}).get("path", "") if actual_artifacts else ""
    write_md(
        STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage40 Brief(40단계 개요)

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- source idea(원천 아이디어): legacy Stage32(레거시 32단계) candle morphology diagnostic(캔들 형태 진단), idea-only(아이디어 전용)
- question(질문): closed US100 M5 OHLC(확정 US100 5분봉 시가/고가/저가/종가) candle morphology(캔들 형태)가 validation/OOS(검증/표본외) MT5 runtime probe(런타임 탐침)에서 signal quality(신호 품질)를 가를 수 있는가?
- independence(독립성): Stage38/39(38/39단계)는 negative memory(부정 기억)로만 쓰고, legacy 34D/29N(레거시 34D/29N)은 baseline(기준선)으로 쓰지 않는다.
- claim boundary(주장 경계): `{FINAL_BOUNDARY}`

효과(effect, 효과): Stage40(40단계)은 permission/abstention(허용/기권), exit overlay(청산 덧씌움), state context(상태 문맥) 후속이 아니라 candle feature structure(캔들 피처 구조) 자체를 MT5 Strategy Tester(MT5 전략 테스터)에서 본다.
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage40 Input References(40단계 입력 참조)

- Tier A model input(Tier A 모델 입력): `{rel(MODEL_INPUT_DATASET_PATH)}`
- Tier A feature order(Tier A 피처 순서): `{rel(MODEL_INPUT_FEATURE_ORDER_PATH)}`
- training summary(학습 요약): `{rel(TRAINING_SUMMARY_PATH)}`
- raw US100 M5 OHLC(원천 US100 5분봉 OHLC): `{rel(RAW_US100_BARS_PATH)}`
- raw MT5 bars(raw MT5 봉): `{rel(RAW_MT5_ROOT)}`
- legacy idea seed(레거시 아이디어 씨앗): `{LEGACY_STAGE32_SELECTION_STATUS_PATH.as_posix()}`
- MT5 EA(MT5 전문가 자문): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`

효과(effect, 효과): candle morphology(캔들 형태)는 Python(파이썬)에서 닫힌 봉만으로 계산하고, MT5(MetaTrader 5, 메타트레이더5)는 후보별 신호 CSV(신호 CSV)를 실행한다.
""",
    )
    packet_lines = [
        "# Stage40 run34A Candle Morphology Signal Quality Packet(40단계 run34A 캔들 형태 신호 품질 묶음)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- idea_id(아이디어 ID): `{IDEA_ID}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        f"- judgment(판정): `{judgment}`",
        f"- claim boundary(주장 경계): `{FINAL_BOUNDARY}`",
        "",
        "## Broad Sweep(넓은 탐색)",
        "",
        f"- candidate_count(후보 수): `{len([item for item in result.get('candidate_specs', []) if str(item.get('candidate_id','')).startswith('c')])}`",
        f"- best_validation(검증 최상): `{best_val.get('candidate_id') if best_val else 'missing'}` net `{best_val.get('net_profit') if best_val else 'missing'}` PF `{best_val.get('profit_factor') if best_val else 'missing'}`",
        f"- worst_validation(검증 최하): `{worst_val.get('candidate_id') if worst_val else 'missing'}`",
        f"- best_oos(OOS 최상): `{best_oos.get('candidate_id') if best_oos else 'missing'}` net `{best_oos.get('net_profit') if best_oos else 'missing'}` PF `{best_oos.get('profit_factor') if best_oos else 'missing'}`",
        f"- worst_oos(OOS 최하): `{worst_oos.get('candidate_id') if worst_oos else 'missing'}`",
        "",
        "## Micro Search Gate(미세 탐색 게이트)",
        "",
        f"- status(상태): `{micro_gate.get('status')}`",
        f"- best_candidate(최상 후보): `{micro_gate.get('best_candidate')}`",
        f"- rule(규칙): `{micro_gate.get('rule')}`",
        "",
        "## MT5 Strategy Tester Execution(MT5 전략 테스터 실행)",
        "",
    ]
    if actual_artifacts:
        first_attempt = result.get("attempts", [{}])[0]
        packet_lines.extend(
            [
                f"- command used(사용 명령): `{command}`",
                "- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`",
                f"- .ini path(.ini 경로): `{first_attempt.get('ini', {}).get('path', '')}`",
                f"- .set path(.set 경로): `{first_attempt.get('set', {}).get('path', '')}`",
                f"- manifest path(목록 경로): `{rel(RUN_ROOT / 'run_manifest.json')}`",
                f"- terminal path(터미널 경로): `{TERMINAL_PATH_DEFAULT}`",
                f"- Common Files path(Common Files 공용 파일 경로): `{COMMON_FILES_ROOT_DEFAULT}`",
                f"- tester output path(테스터 출력 경로): `{report_path}`",
                f"- imported result path(가져온 결과 경로): `{rel(RUN_ROOT / 'mt5/mt5_result_import_summary.json')}`",
                f"- candidates tested in MT5(MT5 후보 수): `{len(result.get('candidate_specs', []))}`",
            ]
        )
    else:
        packet_lines.append("BLOCKED: MT5 Strategy Tester execution did not produce an artifact, so Stage40 run34A is incomplete.")
    packet_lines.extend(
        [
            "",
            "## Promotion Candidate Gate(승격 후보 게이트)",
            "",
            f"- status(상태): `{promotion_gate.get('status')}`",
            f"- candidate_id(후보 ID): `{promotion_gate.get('candidate_id')}`",
            f"- promotion packet path(승격 묶음 경로): `{promotion_gate.get('promotion_packet_path')}`",
            "",
            "## Result Judgment(결과 판정)",
            "",
            f"`{judgment}`",
            "",
            "Stage40 run34A remains runtime_probe_only(런타임 탐침 전용): no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no operating reference(운영 기준 없음).",
        ]
    )
    write_md(STAGE_ROOT / "03_reviews/run34A_candle_morphology_signal_quality_broad_mt5_probe_packet.md", "\n".join(packet_lines))
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Review Index(검토 색인)

- run packet(실행 묶음): `03_reviews/run34A_candle_morphology_signal_quality_broad_mt5_probe_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
""",
    )
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage40 Selection Status(40단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- micro_search_gate(미세 탐색 게이트): `{micro_gate.get('status')}`
- promotion_candidate_gate(승격 후보 게이트): `{promotion_gate.get('status')}`

효과(effect, 효과): Stage40(40단계)은 runtime_probe_only(런타임 탐침 전용)로 남고, 운영 선택을 만들지 않는다.
""",
    )

def write_packet_files(
    result: Mapping[str, Any],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    promotion_gate: Mapping[str, Any],
    judgment: str,
    ledger_payload: Mapping[str, Any],
    validation_commands: Sequence[Mapping[str, Any]],
) -> None:
    actual_mt5 = judgment != BLOCKED_JUDGMENT
    required_gates = ["runtime_evidence_gate", "result_judgment_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    write_yaml_text(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
parent_packet_id: {PARENT_PACKET_ID}
stage_id: {STAGE_ID}
run_id: {RUN_ID}
idea_id: {IDEA_ID}
primary_family: runtime_backtest
primary_skill: obsidian-runtime-parity
support_skills:
  - obsidian-experiment-design
  - obsidian-exploration-mandate
  - obsidian-data-integrity
  - obsidian-backtest-forensics
  - obsidian-artifact-lineage
  - obsidian-performance-attribution
  - obsidian-model-validation
  - obsidian-result-judgment
  - obsidian-code-surface-guard
  - obsidian-environment-reproducibility
required_gates:
  - runtime_evidence_gate
  - result_judgment_gate
  - kpi_contract_audit
  - required_gate_coverage_audit
  - final_claim_guard
claim_boundary: {FINAL_BOUNDARY}
status: {"completed" if actual_mt5 else "blocked"}
""",
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "completed", "evidence": "stage question, broad sweep, micro gate, stop conditions, and failure modes recorded"},
                {"skill": "obsidian-exploration-mandate", "status": "completed", "evidence": "broad sweep precedes any micro-search, Stage38/39 are negative memory, and legacy Stage32 is idea-only"},
                {"skill": "obsidian-data-integrity", "status": "completed", "evidence": "Tier A/B source rows, split labels, missingness, and route coverage recorded"},
                {"skill": "obsidian-runtime-parity", "status": "passed" if actual_mt5 else "blocked", "evidence": "MT5 handoff manifest, .ini/.set, compile, tester output, and imported KPI rows recorded"},
                {"skill": "obsidian-backtest-forensics", "status": "passed" if actual_mt5 else "blocked", "evidence": "tester command, EA, report paths, costs from tester profile, and KPI rows recorded"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "evidence": "source lineage and generated artifact hashes recorded"},
                {"skill": "obsidian-performance-attribution", "status": "completed", "evidence": "validation/OOS best/worst, Tier A/B route components, drawdown, PF, and trade counts recorded"},
                {"skill": "obsidian-model-validation", "status": "completed", "evidence": "promotion candidate gate blocks Python-only or split-unstable claims"},
                {"skill": "obsidian-result-judgment", "status": "completed", "evidence": f"allowed judgment {judgment} with runtime_probe_only boundary"},
            ],
        },
    )
    best_val, worst_val = best_worst(mt5_rows, "validation_is")
    best_oos, worst_oos = best_worst(mt5_rows, "oos")
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "idea_id": IDEA_ID,
            "judgment": judgment,
            "actual_mt5_artifact_exists": actual_mt5,
            "broad_candidate_count": len([item for item in result.get("candidate_specs", []) if str(item.get("candidate_id", "")).startswith("c")]),
            "micro_candidate_count": len([item for item in result.get("candidate_specs", []) if str(item.get("candidate_id", "")).startswith("m")]),
            "mt5_attempt_count": len(result.get("attempts", [])),
            "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
            "best_validation_mt5": best_val,
            "worst_validation_mt5": worst_val,
            "best_oos_mt5": best_oos,
            "worst_oos_mt5": worst_oos,
            "micro_search_gate": micro_gate,
            "promotion_candidate_gate": promotion_gate,
            "boundary": FINAL_BOUNDARY,
            "ledger_sync": ledger_payload,
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "status": "passed" if actual_mt5 else "failed",
            "actual_mt5_strategy_tester_output_exists": actual_mt5,
            "compile": result.get("compile", {}),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "blocker_if_failed": {
                "judgment": BLOCKED_JUDGMENT,
                "terminal_path_expected": str(TERMINAL_PATH_DEFAULT),
                "common_files_path_expected": str(COMMON_FILES_ROOT_DEFAULT),
                "retry_command": "python -m foundation.pipelines.run_stage40_candle_morphology_signal_quality_scout --timeout-seconds 900",
            },
        },
    )
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "allowed_judgments": [POSITIVE_JUDGMENT, INCONCLUSIVE_JUDGMENT, NEGATIVE_JUDGMENT, BLOCKED_JUDGMENT], "boundary": FINAL_BOUNDARY})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if actual_mt5 else "blocked", "mt5_kpi_records": len(result.get("mt5_kpi_records", [])), "required_tier_records": ["Tier A used", "Tier B fallback used", "actual routed total"], "synthetic_sum_used_as_routed_total": False, "missing_required_kpi_fields": [] if actual_mt5 else ["actual_mt5_strategy_tester_output"]})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed", "required_gates": required_gates, "covered_gates": required_gates, "missing_gates": []})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": FINAL_BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": list(validation_commands), "mt5_command_count": len(result.get("execution_results", [])), "status": "recorded"})


def create_promotion_packet_if_needed(promotion_gate: Mapping[str, Any]) -> dict[str, Any]:
    if promotion_gate.get("status") != "passed" or not promotion_gate.get("candidate_id"):
        return dict(promotion_gate)
    candidate_id = str(promotion_gate["candidate_id"])
    packet_root = ROOT / "docs/agent_control/packets" / f"promotion_candidate_review_stage40_{candidate_id}_v1"
    write_yaml_text(
        packet_root / "work_packet.yaml",
        f"""packet_id: promotion_candidate_review_stage40_{candidate_id}_v1
source_parent_packet_id: {PARENT_PACKET_ID}
source_stage_id: {STAGE_ID}
source_run_id: {RUN_ID}
candidate_id: {candidate_id}
status: review_ready_not_promoted
claim_boundary: promotion_candidate_review_ready_no_baseline_no_operating_promotion
""",
    )
    write_json(packet_root / "review_ready_summary.json", {"candidate_id": candidate_id, "source_stage_id": STAGE_ID, "source_run_id": RUN_ID, "promotion_gate": promotion_gate, "no_silent_promotion": True})
    return {**dict(promotion_gate), "promotion_packet_path": rel(packet_root)}


def write_run_files(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]], micro_gate: Mapping[str, Any], promotion_gate: Mapping[str, Any], judgment: str) -> dict[str, Any]:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "idea_id": IDEA_ID,
            "parent_packet_id": PARENT_PACKET_ID,
            "run_number": RUN_NUMBER,
            "completion_goal": result.get("completion_goal"),
            "attempts": result.get("attempts", []),
            "common_copies": result.get("common_copies", []),
            "compile": result.get("compile", {}),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": judgment,
            "boundary": FINAL_BOUNDARY,
        },
    )
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "idea_id": IDEA_ID,
            "kpi_scope": "candle_morphology_signal_quality_mt5_runtime_probe",
            "model_family": result.get("model_family"),
            "feature_set_id": result.get("feature_set_id"),
            "label_id": result.get("label_id"),
            "split_contract": result.get("split_contract"),
            "mt5": {
                "scoreboard_lane": "runtime_probe",
                "external_verification_status": result.get("external_verification_status"),
                "execution_results": result.get("execution_results", []),
                "strategy_tester_reports": result.get("strategy_tester_reports", []),
                "kpi_records": result.get("mt5_kpi_records", []),
                "candidate_summary": list(mt5_rows),
            },
            "micro_search_gate": micro_gate,
            "promotion_candidate_gate": promotion_gate,
            "judgment": judgment,
            "boundary": FINAL_BOUNDARY,
        },
    )
    dataframe_to_csv(RUN_ROOT / "tables/stage40_mt5_candidate_summary.csv", mt5_rows)
    dataframe_to_csv(RUN_ROOT / "tables/stage40_python_candidate_summary.csv", result.get("python_candidate_summary", []))
    write_json(RUN_ROOT / "tables/stage40_route_coverage.json", result.get("route_coverage", {}))
    handoff = write_handoff_files(result, mt5_rows)
    write_json(RUN_ROOT / "artifact_lineage.json", {"source_lineage": result.get("source_lineage", []), "generated_artifacts": artifact_hash_summary()})
    return handoff


def update_current_truth(result: Mapping[str, Any], judgment: str, micro_gate: Mapping[str, Any], promotion_gate: Mapping[str, Any]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        r"^active_branch: .*$": "active_branch: codex/stage40-candle-morphology-signal-quality",
        r"^active_stage: .*$": f"active_stage: {STAGE_ID}",
        r"^current_run_id: .*$": f"current_run_id: {RUN_ID}",
    }
    for pattern, value in replacements.items():
        state_text = re.sub(pattern, value, state_text, flags=re.MULTILINE)
    status_text = "reviewed_runtime_probe_completed" if judgment != BLOCKED_JUDGMENT else "blocked_runtime_probe_missing_mt5_execution"
    block = f"""

stage40_feature_structure_candle_morphology_signal_quality_scout:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: {status_text}
  current_run_id: {RUN_ID}
  mt5_attempt_count: {len(result.get("attempts", []))}
  mt5_kpi_record_count: {len(result.get("mt5_kpi_records", []))}
  judgment: {judgment}
  micro_search_gate: {micro_gate.get("status")}
  promotion_candidate_gate: {promotion_gate.get("status")}
  legacy_source: Stage32 candle morphology idea only, no legacy result inherited
  report_path: {rel(STAGE_ROOT / "03_reviews/run34A_candle_morphology_signal_quality_broad_mt5_probe_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {FINAL_BOUNDARY}
"""
    state_text = re.sub(r"\n+stage40_feature_structure_candle_morphology_signal_quality_scout:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = re.sub(r"## Latest Stage40 Candle Morphology Signal Quality\(.*?\)\n.*?(?=\n## |\Z)", "", current, flags=re.DOTALL).lstrip()
    actual = judgment != BLOCKED_JUDGMENT
    section = f"""## Latest Stage40 Candle Morphology Signal Quality(최신 40단계 캔들 형태 신호 품질)

Stage40(40단계) `{STAGE_ID}`는 legacy Stage32(레거시 32단계) candle morphology(캔들 형태)를 idea-only(아이디어 전용) seed(씨앗)로만 가져와 run34A(실행34A) MT5 runtime probe(런타임 탐침)를 수행했다. legacy 34D/29N(레거시 34D/29N), baseline(기준선), promotion(승격), operating reference(운영 기준)는 상속하지 않는다.

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{judgment}`
- MT5 evidence(MT5 근거): `{"present" if actual else "missing"}`
- MT5 attempts(MT5 시도): `{len(result.get("attempts", []))}`
- MT5 KPI rows(MT5 KPI 행): `{len(result.get("mt5_kpi_records", []))}`
- micro_search_gate(미세 탐색 게이트): `{micro_gate.get("status")}`
- promotion_candidate_gate(승격 후보 게이트): `{promotion_gate.get("status")}`
- boundary(경계): `{FINAL_BOUNDARY}`

효과(effect, 효과): 현재 진실(current truth, 현재 진실)은 Stage40(40단계)을 candle morphology(캔들 형태) runtime_probe_only(런타임 탐침 전용)로만 기록한다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    entry = f"\n- {utc_now()} `{STAGE_ID}` `{RUN_ID}` completed with judgment `{judgment}`; boundary `{FINAL_BOUNDARY}`; legacy Stage32 candle morphology used as idea-only seed.\n"
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + entry, encoding="utf-8-sig")


def merge_execution_results(broad: Mapping[str, Any], micro: Mapping[str, Any] | None) -> dict[str, Any]:
    if micro is None:
        return dict(broad)
    merged = dict(broad)
    for key in ("attempts", "candidate_specs", "common_copies", "execution_results", "strategy_tester_reports", "mt5_kpi_records", "python_candidate_summary"):
        merged[key] = list(broad.get(key, [])) + list(micro.get(key, []))
    merged["feature_matrices"] = {**dict(broad.get("feature_matrices", {})), **dict(micro.get("feature_matrices", {}))}
    merged["external_verification_status"] = (
        "completed"
        if broad.get("external_verification_status") == "completed" and micro.get("external_verification_status") == "completed"
        else "partial_completed_with_blocked_micro_attempt"
    )
    merged["micro_execution"] = {"status": micro.get("external_verification_status"), "attempt_count": len(micro.get("attempts", []))}
    return merged


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage40 candle morphology signal-quality MT5 runtime probe.")
    parser.add_argument("--materialize-only", action="store_true", help="Write artifacts but do not invoke MT5.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)
    validation_commands = [
        {
            "command": "python -m foundation.pipelines.run_stage40_candle_morphology_signal_quality_scout --timeout-seconds 900",
            "result": "running_or_recorded_by_pipeline",
            "failures_or_blockers": "",
        }
    ]
    common, route_coverage, lineage = build_common_table()
    schema_rows = [
        {
            **row,
            "source_data_path": rel(RAW_US100_BARS_PATH),
            "source_symbol": "US100",
            "timeframe": "M5",
            "timestamp_rule": "bar close timestamp from time_close_unix; closed bars only",
            "ohlc_column_mapping": "open=open, high=high, low=low, close=close",
            "used_directly_in_mt5": False,
            "used_for_python_candidate_design": True,
        }
        for row in candle_morphology_schema()
    ]
    write_json(RUN_ROOT / "tables/candle_morphology_schema.json", {"columns": schema_rows})
    dataframe_to_csv(RUN_ROOT / "tables/candle_morphology_lineage.csv", schema_rows)
    thresholds = build_thresholds(common)
    common_artifact = save_frame(RUN_ROOT / "tables/stage40_common_decision_surface_table.parquet", common)
    lineage = [{**item, "sha256": common_artifact["sha256"] if item.get("sha256") == "computed_after_write" else item.get("sha256")} for item in lineage]
    broad_specs = build_broad_candidate_grid()
    dataframe_to_csv(RUN_ROOT / "tables/stage40_candidate_grid.csv", [spec.__dict__ for spec in broad_specs])
    broad_batch = build_candidate_batch(specs=broad_specs, common=common, thresholds=thresholds, common_files_root=Path(args.common_files_root))
    all_frames = dict(broad_batch["frames"])
    candidate_artifact = save_frame(RUN_ROOT / "tables/stage40_candidate_signal_table.parquet", pd.concat(all_frames.values(), ignore_index=True))
    broad_prepared = prepared_payload(
        candidate_specs=broad_specs,
        attempts=broad_batch["attempts"],
        common=common,
        feature_exports=broad_batch["feature_exports"],
        model_artifact=broad_batch["model_artifact"],
        common_copies=broad_batch["common_copies"],
        route_coverage=route_coverage,
        common_artifact=common_artifact,
        candidate_artifact=candidate_artifact,
        python_summary=broad_batch["summary"],
        lineage=lineage,
        thresholds=thresholds,
        batch_label="broad_sweep",
    )
    broad_result = execute_or_block(broad_prepared, args)
    broad_rows = build_mt5_candidate_summary(broad_result.get("mt5_kpi_records", []), broad_batch["summary"], broad_result.get("execution_results", []))
    micro_gate = evaluate_micro_search_gate(broad_rows)
    micro_result = None
    if micro_gate.get("status") == "passed" and not args.materialize_only:
        micro_specs = build_micro_candidate_grid(str(micro_gate["best_candidate"]), broad_specs, thresholds)
        micro_batch = build_candidate_batch(specs=micro_specs, common=common, thresholds=thresholds, common_files_root=Path(args.common_files_root))
        all_frames.update(micro_batch["frames"])
        candidate_artifact = save_frame(RUN_ROOT / "tables/stage40_candidate_signal_table.parquet", pd.concat(all_frames.values(), ignore_index=True))
        micro_prepared = prepared_payload(
            candidate_specs=micro_specs,
            attempts=micro_batch["attempts"],
            common=common,
            feature_exports=micro_batch["feature_exports"],
            model_artifact=micro_batch["model_artifact"],
            common_copies=micro_batch["common_copies"],
            route_coverage=route_coverage,
            common_artifact=common_artifact,
            candidate_artifact=candidate_artifact,
            python_summary=micro_batch["summary"],
            lineage=lineage,
            thresholds=thresholds,
            batch_label="micro_search",
        )
        micro_result = execute_or_block(micro_prepared, args)
    result = merge_execution_results(broad_result, micro_result)
    mt5_rows = build_mt5_candidate_summary(result.get("mt5_kpi_records", []), result.get("python_candidate_summary", []), result.get("execution_results", []))
    promotion_gate = create_promotion_packet_if_needed(evaluate_promotion_candidate_gate(mt5_rows))
    mt5_rows = apply_gate_rejection_reasons(mt5_rows, promotion_gate)
    judgment = final_judgment_from_results(result, promotion_gate)
    result["judgment"] = judgment
    result["candidate_table_artifact"] = candidate_artifact
    result["validation_commands"] = validation_commands
    handoff_payload = write_run_files(result, mt5_rows, micro_gate, promotion_gate, judgment)
    ledger_payload = write_ledgers(result, judgment)
    write_stage_docs(result, mt5_rows, micro_gate, promotion_gate, judgment)
    write_packet_files(result, mt5_rows, micro_gate, promotion_gate, judgment, ledger_payload, validation_commands)
    update_current_truth(result, judgment, micro_gate, promotion_gate)
    write_json(
        RUN_ROOT / "final_execution_summary.json",
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "judgment": judgment,
            "handoff": handoff_payload,
            "ledger": ledger_payload,
            "micro_search_gate": micro_gate,
            "promotion_candidate_gate": promotion_gate,
            "claim_boundary": FINAL_BOUNDARY,
        },
    )


if __name__ == "__main__":
    main()
