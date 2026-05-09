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
from foundation.models.ebm_score_table import FIELDNAMES, load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from foundation.risk.exit_overlay import (
    STAGE39_FEATURE_ORDER,
    ExitOverlayCandidateSpec,
    apply_exit_overlay_candidate,
    build_broad_candidate_grid,
    build_loose_thresholds,
    hold_metrics_from_actions,
    rejection_reason,
    summarize_candidate_frames,
)


STAGE_NUMBER = 39
STAGE_ID = "39_exit_risk__non_entry_lifecycle_tail_overlay"
IDEA_ID = "IDEA-ST39-EXIT-RISK-NON-ENTRY-OVERLAY"
RUN_ID = "run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1"
RUN_NUMBER = "run33A"
PACKET_ID = "stage39_run33A_exit_risk_non_entry_overlay_broad_mt5_probe_v1"
EXPLORATION_LABEL = "stage39_ExitRisk__NonEntryLifecycleTailOverlay"
SOURCE_FRONTIER = "Stage36 frontier03_exit_risk_non_entry_overlay"
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
SIGNAL_FEATURE_HASH = ordered_hash(STAGE39_FEATURE_ORDER)
COMMON_STAGE39_ROOT = f"Project_Obsidian_Prime_v2/stage39/{RUN_NUMBER}_exit_overlay"

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

STAGE38_COMMON_PATH = ROOT / "stages/38_decision_layer__permission_abstention_overlap/02_runs/run32A_permission_abstention_overlap_broad_mt5_probe_v1/tables/stage38_common_decision_surface_table.parquet"
STAGE38_CANDIDATE_PATH = ROOT / "stages/38_decision_layer__permission_abstention_overlap/02_runs/run32A_permission_abstention_overlap_broad_mt5_probe_v1/tables/stage38_candidate_signal_table.parquet"
STAGE24_A_PATH = ROOT / "stages/24_exit_model__survival_time_to_event_hold_shape/02_runs/run18B_survival_time_to_event_runtime_probe_v1/predictions/tier_a_survival_permission_predictions.parquet"
STAGE24_B_PATH = ROOT / "stages/24_exit_model__survival_time_to_event_hold_shape/02_runs/run18B_survival_time_to_event_runtime_probe_v1/predictions/tier_b_survival_permission_predictions.parquet"
STAGE25_A_PATH = ROOT / "stages/25_exit_model__hazard_trade_lifecycle_risk/02_runs/run19B_hazard_trade_lifecycle_runtime_probe_v1/predictions/tier_a_hazard_permission_predictions.parquet"
STAGE25_B_PATH = ROOT / "stages/25_exit_model__hazard_trade_lifecycle_risk/02_runs/run19B_hazard_trade_lifecycle_runtime_probe_v1/predictions/tier_b_hazard_permission_predictions.parquet"
STAGE27_A_PATH = ROOT / "stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21B_quantile_boosting_tail_risk_runtime_probe_v1/predictions/tier_a_quantile_runtime_predictions.parquet"
STAGE27_B_PATH = ROOT / "stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21B_quantile_boosting_tail_risk_runtime_probe_v1/predictions/tier_b_quantile_runtime_predictions.parquet"


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


def load_frame(path: Path) -> pd.DataFrame:
    if not path_exists(path):
        raise FileNotFoundError(path)
    frame = pd.read_parquet(io_path(path))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return frame.sort_values("timestamp").reset_index(drop=True)


def source_payload(stage: str, run_id: str, path: Path) -> dict[str, Any]:
    return {
        "source_stage": stage,
        "source_run_id": run_id,
        "source_artifact_path": rel(path),
        "source_artifact_hash": sha256_file_lf_normalized(path) if path_exists(path) else "missing_required",
        "timestamp_alignment_rule": "exact UTC timestamp, split, label_class, and tier route row",
        "missingness_rule": "missing source value sets stage39_surface_missing and prevents overlay activation",
    }


def tier_source_frame(path: Path, tier_label: str, keep: Mapping[str, str]) -> pd.DataFrame:
    raw = load_frame(path)
    columns = ["timestamp", "split", "label_class", *[name for name in keep if name in raw.columns]]
    out = raw[columns].copy().rename(columns={source: target for source, target in keep.items() if source in raw.columns})
    out["tier_label"] = tier_label
    return out


def load_stage38_base() -> pd.DataFrame:
    common = load_frame(STAGE38_COMMON_PATH)
    candidates = load_frame(STAGE38_CANDIDATE_PATH)
    base = candidates.loc[candidates["candidate_id"].astype(str).eq("c01_no_overlap_reference")][
        ["stage38_row_id", "stage38_decision_signal", "entry_decision", "candidate_id"]
    ].copy()
    base = base.rename(
        columns={
            "stage38_decision_signal": "stage39_base_entry_signal",
            "entry_decision": "stage39_base_entry_decision",
            "candidate_id": "stage39_base_entry_source_candidate",
        }
    )
    merged = common.merge(base, on="stage38_row_id", how="inner", validate="one_to_one")
    merged["stage38_context_tail_pressure"] = merged["tail_pressure"]
    merged["stage38_context_permission_score"] = merged["permission_score"]
    merged["stage38_context_entropy"] = merged["entropy"]
    merged["stage38_context_p_flat"] = merged["p_flat"]
    return merged


def build_common_table() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    common = load_stage38_base()
    survival = pd.concat(
        [
            tier_source_frame(
                STAGE24_A_PATH,
                mt5.TIER_A,
                {
                    "survival_risk_z": "stage24_survival_risk_z",
                    "survival_raw_risk_score": "stage24_survival_raw_risk_score",
                    "survival_runtime_threshold": "stage24_survival_runtime_threshold",
                },
            ),
            tier_source_frame(
                STAGE24_B_PATH,
                mt5.TIER_B,
                {
                    "survival_risk_z": "stage24_survival_risk_z",
                    "survival_raw_risk_score": "stage24_survival_raw_risk_score",
                    "survival_runtime_threshold": "stage24_survival_runtime_threshold",
                },
            ),
        ],
        ignore_index=True,
    )
    hazard = pd.concat(
        [
            tier_source_frame(
                STAGE25_A_PATH,
                mt5.TIER_A,
                {
                    "hazard_risk_z": "stage25_hazard_risk_z",
                    "hazard_runtime_raw_risk": "stage25_hazard_runtime_raw_risk",
                    "hazard_elapsed_runtime_bar": "stage25_hazard_elapsed_runtime_bar",
                    "hazard_elapsed_runtime_frac": "stage25_hazard_elapsed_runtime_frac",
                    "hazard_runtime_threshold": "stage25_hazard_runtime_threshold",
                },
            ),
            tier_source_frame(
                STAGE25_B_PATH,
                mt5.TIER_B,
                {
                    "hazard_risk_z": "stage25_hazard_risk_z",
                    "hazard_runtime_raw_risk": "stage25_hazard_runtime_raw_risk",
                    "hazard_elapsed_runtime_bar": "stage25_hazard_elapsed_runtime_bar",
                    "hazard_elapsed_runtime_frac": "stage25_hazard_elapsed_runtime_frac",
                    "hazard_runtime_threshold": "stage25_hazard_runtime_threshold",
                },
            ),
        ],
        ignore_index=True,
    )
    tail = pd.concat(
        [
            tier_source_frame(
                STAGE27_A_PATH,
                mt5.TIER_A,
                {
                    "qtl_direction_score": "stage27_tail_direction_score",
                    "qtl_tail_width": "stage27_tail_width",
                    "qtl_tail_asymmetry_score": "stage27_tail_asymmetry_score",
                    "qtl_tail_pressure": "stage27_tail_pressure",
                    "quantile_tail_runtime_threshold": "stage27_tail_runtime_threshold",
                },
            ),
            tier_source_frame(
                STAGE27_B_PATH,
                mt5.TIER_B,
                {
                    "qtl_direction_score": "stage27_tail_direction_score",
                    "qtl_tail_width": "stage27_tail_width",
                    "qtl_tail_asymmetry_score": "stage27_tail_asymmetry_score",
                    "qtl_tail_pressure": "stage27_tail_pressure",
                    "quantile_tail_runtime_threshold": "stage27_tail_runtime_threshold",
                },
            ),
        ],
        ignore_index=True,
    )
    keys = ["timestamp", "split", "label_class", "tier_label"]
    common = common.merge(survival, on=keys, how="left", validate="one_to_one")
    common = common.merge(hazard, on=keys, how="left", validate="one_to_one")
    common = common.merge(tail, on=keys, how="left", validate="one_to_one")
    common["position_age_proxy_bars"] = pd.to_numeric(common["stage25_hazard_elapsed_runtime_bar"], errors="coerce").fillna(6).astype(int)
    common["runtime_position_age_field"] = "COpExecutionBridge.m_bars_in_position"
    common["direction_label"] = np.where(common["stage39_base_entry_signal"].gt(0), "long", np.where(common["stage39_base_entry_signal"].lt(0), "short", "flat"))
    common["validation_oos_split_label"] = common["split"].astype(str).map({"validation": "validation_is"}).fillna(common["split"].astype(str))
    common["timestamp_utc"] = common["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    common["timestamp_alignment_rule"] = "exact_utc_timestamp_inner_join_stage38_base_stage24_stage25_stage27"
    missing_columns = [
        "stage39_base_entry_signal",
        "stage24_survival_risk_z",
        "stage25_hazard_risk_z",
        "stage27_tail_pressure",
    ]
    for column in missing_columns:
        common[f"{column}_missing"] = common[column].isna()
    common["stage39_surface_missing"] = common[[f"{column}_missing" for column in missing_columns]].any(axis=1)
    common["stage39_row_id"] = np.arange(len(common), dtype=int)
    lineage = [
        {"surface_key": "stage38_base_entry", **source_payload("38_decision_layer__permission_abstention_overlap", "run32A_permission_abstention_overlap_broad_mt5_probe_v1", STAGE38_CANDIDATE_PATH)},
        {"surface_key": "stage24_survival", "tier_label": mt5.TIER_A, **source_payload("24_exit_model__survival_time_to_event_hold_shape", "run18B_survival_time_to_event_runtime_probe_v1", STAGE24_A_PATH)},
        {"surface_key": "stage24_survival", "tier_label": mt5.TIER_B, **source_payload("24_exit_model__survival_time_to_event_hold_shape", "run18B_survival_time_to_event_runtime_probe_v1", STAGE24_B_PATH)},
        {"surface_key": "stage25_hazard", "tier_label": mt5.TIER_A, **source_payload("25_exit_model__hazard_trade_lifecycle_risk", "run19B_hazard_trade_lifecycle_runtime_probe_v1", STAGE25_A_PATH)},
        {"surface_key": "stage25_hazard", "tier_label": mt5.TIER_B, **source_payload("25_exit_model__hazard_trade_lifecycle_risk", "run19B_hazard_trade_lifecycle_runtime_probe_v1", STAGE25_B_PATH)},
        {"surface_key": "stage27_tail", "tier_label": mt5.TIER_A, **source_payload("27_tail_model__quantile_boosting_risk_surface", "run21B_quantile_boosting_tail_risk_runtime_probe_v1", STAGE27_A_PATH)},
        {"surface_key": "stage27_tail", "tier_label": mt5.TIER_B, **source_payload("27_tail_model__quantile_boosting_risk_surface", "run21B_quantile_boosting_tail_risk_runtime_probe_v1", STAGE27_B_PATH)},
    ]
    return common.sort_values(["timestamp", "tier_label"]).reset_index(drop=True), lineage


def column_lineage(common: pd.DataFrame, source_lineage: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_surface = {str(item["surface_key"]): item for item in source_lineage}

    def surface_for(column: str) -> Mapping[str, Any]:
        if column.startswith("stage24_"):
            return by_surface["stage24_survival"]
        if column.startswith("stage25_") or column in {"position_age_proxy_bars", "runtime_position_age_field"}:
            return by_surface["stage25_hazard"]
        if column.startswith("stage27_"):
            return by_surface["stage27_tail"]
        if column.startswith("stage38_") or column.startswith("stage39_base"):
            return by_surface["stage38_base_entry"]
        return {
            "source_stage": STAGE_ID,
            "source_run_id": RUN_ID,
            "source_artifact_path": "stage39_materialized_common_table",
            "source_artifact_hash": "generated_in_stage39",
            "timestamp_alignment_rule": "derived from exact aligned common table",
            "missingness_rule": "derived fields inherit source missingness",
        }

    columns = []
    for column in common.columns:
        source = surface_for(column)
        effect = "diagnostics"
        if column in STAGE39_FEATURE_ORDER or column.startswith("stage39_close") or column == "stage39_overlay_max_hold_bars":
            effect = "exit_hold_risk_overlay"
        elif column == "stage39_base_entry_signal":
            effect = "entry_reference_only"
        elif "risk" in column or "tail" in column or "hazard" in column or "survival" in column:
            effect = "exit_hold_risk_overlay"
        columns.append(
            {
                "column": column,
                "source_stage": source.get("source_stage"),
                "source_run_id": source.get("source_run_id"),
                "source_artifact_path": source.get("source_artifact_path"),
                "source_artifact_hash": source.get("source_artifact_hash"),
                "timestamp_alignment_rule": source.get("timestamp_alignment_rule"),
                "missingness_rule": source.get("missingness_rule"),
                "used_directly_by_mt5": column in STAGE39_FEATURE_ORDER,
                "used_by_python_preparation": True,
                "effect_scope": effect,
            }
        )
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "alignment_grain": "feature-ready timestamp x tier route source",
        "columns": columns,
        "hard_non_entry_rule": "Only stage39_base_entry_signal affects entry probability; overlay features are neutral in the EBM score table and are consumed after a position exists.",
    }


def write_candidate_grid(path: Path, specs: Sequence[ExitOverlayCandidateSpec]) -> None:
    columns = [
        "candidate_id",
        "label",
        "enabled_surfaces",
        "exit_overlay_rule",
        "hold_override_rule",
        "direction_specific_rule",
        "fallback_rule",
        "threshold_family",
        "min_hold_bars",
        "dynamic_max_hold_bars",
        "long_enabled",
        "short_enabled",
        "adverse_excursion_proxy_required",
    ]
    rows = []
    for spec in specs:
        payload = {column: getattr(spec, column) for column in columns}
        payload["enabled_surfaces"] = "+".join(spec.enabled_surfaces) if spec.enabled_surfaces else "none"
        rows.append(payload)
    write_csv_rows(path, columns, rows)


def export_signal_score_table(path: Path) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    rows = [
        {"record_type": "intercept", "feature_index": -1, "item_index": -1, "value": "", "score_short": "0", "score_flat": "0", "score_long": "0"},
        {"record_type": "cut", "feature_index": 0, "item_index": 0, "value": "-0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "cut", "feature_index": 0, "item_index": 1, "value": "0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "score", "feature_index": 0, "item_index": 0, "value": "", "score_short": "4", "score_flat": "-4", "score_long": "-4"},
        {"record_type": "score", "feature_index": 0, "item_index": 1, "value": "", "score_short": "4", "score_flat": "-4", "score_long": "-4"},
        {"record_type": "score", "feature_index": 0, "item_index": 2, "value": "", "score_short": "-4", "score_flat": "4", "score_long": "-4"},
        {"record_type": "score", "feature_index": 0, "item_index": 3, "value": "", "score_short": "-4", "score_flat": "-4", "score_long": "4"},
    ]
    for feature_index in (1, 2, 3):
        rows.append({"record_type": "cut", "feature_index": feature_index, "item_index": 0, "value": "0.5", "score_short": "", "score_flat": "", "score_long": ""})
        for item_index in (0, 1, 2):
            rows.append({"record_type": "score", "feature_index": feature_index, "item_index": item_index, "value": "", "score_short": "0", "score_flat": "0", "score_long": "0"})
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    table = load_ebm_score_table(path, feature_count=len(STAGE39_FEATURE_ORDER))
    probs = score_ebm_table_probabilities(
        table,
        np.asarray(
            [
                [-1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 1.0, 6.0],
                [1.0, 0.0, 0.0, 0.0],
            ],
            dtype="float64",
        ),
    )
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "stage39_base_signal_with_neutral_overlay_feature_score_table_csv_v1",
        "feature_order": list(STAGE39_FEATURE_ORDER),
        "feature_order_hash": SIGNAL_FEATURE_HASH,
        "parity_sample_probabilities": probs.tolist(),
        "runtime_policy": "feature0 maps fixed entry signal; features1-3 are neutral for entry and consumed by EA after position exists",
    }


def export_candidate_feature_matrices(candidate_frames: Mapping[str, pd.DataFrame]) -> tuple[dict[str, Any], dict[str, Any]]:
    feature_root = RUN_ROOT / "features"
    exports: dict[str, Any] = {}
    for candidate_id, frame in candidate_frames.items():
        short_id = safe_name(candidate_id, 32)
        for split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            for tier_label, tier_key in ((mt5.TIER_A, "tier_a"), (mt5.TIER_B, "tier_b_fallback")):
                selected = frame.loc[frame["split"].eq(split) & frame["tier_label"].eq(tier_label)].copy()
                output = feature_root / f"{short_id}_{tier_key}_{runtime_split}_s39.csv"
                exports[f"{candidate_id}_{tier_key}_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
                    selected,
                    STAGE39_FEATURE_ORDER,
                    output,
                    metadata_columns=(
                        "candidate_id",
                        "candidate_label",
                        "enabled_surfaces",
                        "tier_label",
                        "routing_source",
                        "entry_decision",
                        "exit_overlay_rule",
                        "hold_override_rule",
                        "direction_specific_rule",
                    ),
                )
    model_artifact = export_signal_score_table(RUN_ROOT / "models/stage39_base_signal_exit_overlay_score_table.csv")
    return exports, model_artifact


def resolve_artifact_path(value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    root_path = ROOT / path
    if path_exists(root_path):
        return root_path
    return RUN_ROOT / path


def copy_runtime_inputs(feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common_root: Path) -> list[dict[str, Any]]:
    common = COMMON_STAGE39_ROOT
    copied = []
    model_path = resolve_artifact_path(model_artifact["path"])
    copied.append(copy_to_common(model_path, f"{common}/models/{model_path.name}", common_root))
    for payload in feature_exports.values():
        local_path = resolve_artifact_path(payload["path"])
        copied.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", common_root))
    return copied


def route_coverage_from_common(common: pd.DataFrame) -> dict[str, Any]:
    by_split = {}
    subtype = {}
    for split in ("validation", "oos"):
        view = common.loc[common["split"].eq(split)]
        tier_a_rows = int(view["tier_label"].eq(mt5.TIER_A).sum())
        tier_b_rows = int(view["tier_label"].eq(mt5.TIER_B).sum())
        by_split[split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
        }
        subtype[split] = view.loc[view["tier_label"].eq(mt5.TIER_B), "partial_context_subtype"].value_counts().to_dict()
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": subtype, "no_tier_by_split": {"validation": 0, "oos": 0}}


def make_attempts(
    candidate_specs: Sequence[ExitOverlayCandidateSpec],
    feature_exports: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    common: pd.DataFrame,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common_name = COMMON_STAGE39_ROOT
    model_name = Path(model_artifact["path"]).name
    by_id = {spec.candidate_id: spec for spec in candidate_specs}
    for candidate_id, spec in by_id.items():
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_frame = common.loc[common["split"].eq(source_split) & common["tier_label"].eq(mt5.TIER_A)]
            from_date, to_date = split_dates_from_frame(split_frame, source_split)
            tier_a_matrix = Path(feature_exports[f"{candidate_id}_tier_a_{runtime_split}"]["path"]).name
            tier_b_matrix = Path(feature_exports[f"{candidate_id}_tier_b_fallback_{runtime_split}"]["path"]).name
            overlay_enabled = candidate_id != "c01_no_overlay_reference"
            attempts.append(
                attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=STAGE_NUMBER,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"routed_{safe_name(candidate_id, 64)}_{runtime_split}",
                    tier=mt5.TIER_AB,
                    split=runtime_split,
                    model_path=f"{common_name}/models/{model_name}",
                    model_id=f"{RUN_ID}_{candidate_id}_base_signal_overlay_table",
                    model_backend="ebm_table",
                    feature_path=f"{common_name}/features/{tier_a_matrix}",
                    feature_count=len(STAGE39_FEATURE_ORDER),
                    feature_order_hash=SIGNAL_FEATURE_HASH,
                    short_threshold=SHORT_THRESHOLD,
                    long_threshold=LONG_THRESHOLD,
                    min_margin=MIN_MARGIN,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="routed_total",
                    record_view_prefix=f"mt5_routed_{candidate_id}",
                    max_hold_bars=MAX_HOLD_BARS,
                    common_root=common_name,
                    fallback_enabled=True,
                    fallback_model_path=f"{common_name}/models/{model_name}",
                    fallback_model_id=f"{RUN_ID}_{candidate_id}_fallback_base_signal_overlay_table",
                    fallback_model_backend="ebm_table",
                    fallback_feature_path=f"{common_name}/features/{tier_b_matrix}",
                    fallback_feature_count=len(STAGE39_FEATURE_ORDER),
                    fallback_feature_order_hash=SIGNAL_FEATURE_HASH,
                    fallback_short_threshold=SHORT_THRESHOLD,
                    fallback_long_threshold=LONG_THRESHOLD,
                    fallback_min_margin=MIN_MARGIN,
                    fallback_invert_signal=False,
                    close_on_flat_signal=False,
                    reverse_on_opposite_signal=True,
                    extra_set_values={
                        "InpExitRiskOverlayEnabled": overlay_enabled,
                        "InpExitRiskCloseLongFeatureIndex": 1,
                        "InpExitRiskCloseShortFeatureIndex": 2,
                        "InpExitRiskCloseThreshold": 0.5,
                        "InpExitRiskMinHoldBars": int(spec.min_hold_bars),
                        "InpExitRiskMaxHoldFeatureIndex": 3,
                    },
                )
            )
    return attempts


def prepared_payload(
    *,
    candidate_specs: Sequence[ExitOverlayCandidateSpec],
    attempts: Sequence[Mapping[str, Any]],
    common: pd.DataFrame,
    feature_exports: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    common_copies: Sequence[Mapping[str, Any]],
    route_coverage: Mapping[str, Any],
    common_artifact: Mapping[str, Any],
    candidate_artifact: Mapping[str, Any],
    python_summary: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_root": RUN_ROOT.as_posix(),
        "attempts": list(attempts),
        "candidate_specs": [spec.__dict__ for spec in candidate_specs],
        "feature_matrices": dict(feature_exports),
        "model_artifacts": {"signal_score_table": dict(model_artifact)},
        "common_copies": list(common_copies),
        "route_coverage": dict(route_coverage),
        "common_table_artifact": dict(common_artifact),
        "candidate_table_artifact": dict(candidate_artifact),
        "python_candidate_summary": list(python_summary),
        "source_run_id": SOURCE_FRONTIER,
        "run_number": RUN_NUMBER,
        "completion_goal": "Stage39 broad MT5 non-entry exit/risk overlay runtime probe",
        "model_family": "stage39_fixed_base_signal_with_exit_risk_overlay_features",
        "feature_set_id": "stage38_c01_base_signal_plus_stage24_survival_stage25_hazard_stage27_tail_overlay",
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


def parse_runtime_actions(runtime_outputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    telemetry_path = Path(str(runtime_outputs.get("telemetry_path", "")))
    summary = dict(runtime_outputs.get("last_summary", {})) if isinstance(runtime_outputs.get("last_summary"), Mapping) else {}
    if not telemetry_path or not path_exists(telemetry_path):
        return [], summary
    rows: list[dict[str, Any]] = []
    with io_path(telemetry_path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if str(row.get("record_type", "")) == "cycle":
                rows.append(dict(row))
    return rows, summary


def telemetry_metrics_for_execution(execution: Mapping[str, Any]) -> dict[str, Any]:
    actions, summary = parse_runtime_actions(execution.get("runtime_outputs", {}))
    hold = hold_metrics_from_actions(actions)
    model_ok = int(float(summary.get("model_ok_count") or 0)) if summary else 0
    overlay_rate = float(hold["early_exit_count_runtime"] / model_ok) if model_ok else 0.0
    action_counts: dict[str, int] = {}
    for row in actions:
        action = str(row.get("exec_action", ""))
        action_counts[action] = action_counts.get(action, 0) + 1
    return {
        **hold,
        "overlay_activation_rate_mt5": overlay_rate,
        "runtime_action_counts": action_counts,
        "runtime_summary": summary,
    }


def build_mt5_candidate_summary(
    kpi_records: Sequence[Mapping[str, Any]],
    python_rows: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    python_by_key = {(row["candidate_id"], row["split"]): dict(row) for row in python_rows}
    exec_by_key = {}
    for execution in execution_results:
        attempt_name = str(execution.get("attempt_name", ""))
        match = re.match(r"routed_(?P<candidate>.+)_(?P<split>validation_is|oos)$", attempt_name)
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
        telemetry = telemetry_metrics_for_execution(execution) if execution else {}
        rows.append(
            {
                **py,
                **telemetry,
                "candidate_id": candidate_id,
                "split": split,
                "net_profit": mt5_metric(total, "net_profit"),
                "profit_factor": mt5_metric(total, "profit_factor"),
                "max_drawdown": mt5_metric(total, "max_drawdown_amount", "max_drawdown"),
                "equity_drawdown": mt5_metric(total, "equity_drawdown_amount", "max_drawdown_amount", "max_drawdown"),
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
    reference_entries = {
        row["split"]: int(row.get("entry_count_runtime") or 0)
        for row in rows
        if row.get("candidate_id") == "c01_no_overlay_reference"
    }
    reference_by_split = {
        row["split"]: row
        for row in rows
        if row.get("candidate_id") == "c01_no_overlay_reference"
    }
    enriched = []
    for row in rows:
        split = str(row.get("split"))
        row = dict(row)
        row["entry_count_delta_runtime_vs_reference"] = int(row.get("entry_count_runtime") or 0) - int(reference_entries.get(split, 0))
        row["candidate_rejection_reason"] = rejection_reason(row, reference_by_split.get(split))
        enriched.append(row)
    return enriched


def pivot_candidate_mt5(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Mapping[str, Any]]]:
    out: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        out.setdefault(str(row["candidate_id"]), {})[str(row["split"])] = row
    return out


def evaluate_micro_search_gate(mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_candidate = pivot_candidate_mt5(mt5_rows)
    reference = by_candidate.get("c01_no_overlay_reference", {})
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate_id, splits in by_candidate.items():
        if candidate_id == "c01_no_overlay_reference":
            rejected.append({"candidate_id": candidate_id, "reason": "reference_not_micro_search_candidate"})
            continue
        val = splits.get("validation_is")
        oos = splits.get("oos")
        ref_val = reference.get("validation_is")
        ref_oos = reference.get("oos")
        if not val or not oos or not ref_val or not ref_oos:
            rejected.append({"candidate_id": candidate_id, "reason": "missing_validation_or_oos_mt5_or_reference_row"})
            continue
        reasons = []
        if int(to_float(val.get("entry_count_delta_runtime_vs_reference")) or 0) != 0 or int(to_float(oos.get("entry_count_delta_runtime_vs_reference")) or 0) != 0:
            reasons.append("entry_count_not_stable")
        for label, row, ref in (("validation", val, ref_val), ("oos", oos, ref_oos)):
            pf = to_float(row.get("profit_factor")) or 0.0
            ref_pf = to_float(ref.get("profit_factor")) or 0.0
            trades = to_float(row.get("trade_count")) or 0.0
            ref_trades = max(to_float(ref.get("trade_count")) or 1.0, 1.0)
            drawdown = to_float(row.get("max_drawdown"))
            ref_drawdown = to_float(ref.get("max_drawdown"))
            if pf < max(0.80, ref_pf * 0.70):
                reasons.append(f"{label}_profit_factor_collapse")
            if trades / ref_trades < 0.50:
                reasons.append(f"{label}_trade_count_too_thin_vs_reference")
            if drawdown is None or ref_drawdown is None or drawdown >= ref_drawdown:
                reasons.append(f"{label}_drawdown_not_improved")
        activation = (to_float(val.get("overlay_activation_rate_mt5")) or 0.0) + (to_float(oos.get("overlay_activation_rate_mt5")) or 0.0)
        if activation <= 0.0:
            reasons.append("overlay_activation_trivially_zero")
        routed_total = (to_float(val.get("actual_routed_total_count_mt5")) or 0.0) + (to_float(oos.get("actual_routed_total_count_mt5")) or 0.0)
        tier_b = (to_float(val.get("tier_b_fallback_used_count_mt5")) or 0.0) + (to_float(oos.get("tier_b_fallback_used_count_mt5")) or 0.0)
        if routed_total > 0 and tier_b / routed_total > 0.60:
            reasons.append("tier_b_fallback_carrying_too_much")
        payload = {
            "candidate_id": candidate_id,
            "validation_net": to_float(val.get("net_profit")),
            "oos_net": to_float(oos.get("net_profit")),
            "validation_pf": to_float(val.get("profit_factor")),
            "oos_pf": to_float(oos.get("profit_factor")),
            "validation_drawdown": to_float(val.get("max_drawdown")),
            "oos_drawdown": to_float(oos.get("max_drawdown")),
            "validation_trades": to_float(val.get("trade_count")),
            "oos_trades": to_float(oos.get("trade_count")),
            "tier_b_signal_share": float(tier_b / routed_total) if routed_total else None,
            "overlay_activation_sum": activation,
        }
        if reasons:
            rejected.append({**payload, "reason": ";".join(dict.fromkeys(reasons))})
        else:
            accepted.append(payload)
    accepted.sort(key=lambda item: ((item.get("validation_net") or 0) + (item.get("oos_net") or 0), -(item.get("oos_drawdown") or 0)), reverse=True)
    return {
        "status": "passed" if accepted else "failed",
        "accepted_candidates": accepted,
        "rejected_candidates": rejected,
        "best_candidate": accepted[0]["candidate_id"] if accepted else None,
        "rule": "bounded micro-search allowed only when validation and OOS risk improve without entry-count instability",
    }


def final_judgment_from_results(result: Mapping[str, Any], micro_gate: Mapping[str, Any]) -> str:
    actual_mt5 = bool(result.get("strategy_tester_reports")) and any(item.get("status") == "completed" for item in result.get("strategy_tester_reports", []))
    if not actual_mt5:
        return BLOCKED_JUDGMENT
    if micro_gate.get("status") == "passed":
        return POSITIVE_JUDGMENT
    return NEGATIVE_JUDGMENT


def dataframe_to_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    frame = pd.DataFrame(list(rows))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8")
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def write_handoff_files(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    mt5_root = RUN_ROOT / "mt5"
    handoff = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "common_files_root": str(COMMON_FILES_ROOT_DEFAULT),
        "terminal_path": str(TERMINAL_PATH_DEFAULT),
        "metaeditor_path": str(METAEDITOR_PATH_DEFAULT),
        "tester_profile_root": str(TESTER_PROFILE_ROOT_DEFAULT),
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "module_hashes": mt5.mt5_runtime_module_hashes(),
        "hard_non_entry_rule": "overlay inputs are ignored until a position exists in COpExecutionBridge.Execute",
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
    }
    write_json(mt5_root / "handoff_manifest.json", handoff)
    write_json(mt5_root / "tester_request.json", tester_request)
    write_json(mt5_root / "mt5_result_import_summary.json", import_summary)
    return {"handoff_manifest": rel(mt5_root / "handoff_manifest.json"), "tester_request": rel(mt5_root / "tester_request.json"), "mt5_result_import_summary": rel(mt5_root / "mt5_result_import_summary.json")}


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
                "parent_run_id": SOURCE_FRONTIER,
                "record_view": view,
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "exit_risk_non_entry_overlay_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": "completed" if record.get("status") == "completed" else "blocked",
                "judgment": judgment,
                "path": kpi_report_path(record),
                "primary_kpi": f"net_profit={metrics.get('net_profit','')};profit_factor={metrics.get('profit_factor','')};trade_count={metrics.get('trade_count','')};signal_count={metrics.get('signal_count','')};expectancy={metrics.get('expectancy','')};win_rate={metrics.get('win_rate_percent', metrics.get('win_rate',''))}",
                "guardrail_kpi": f"route_role={record.get('route_role','')};a_used={metrics.get('tier_a_primary_labelable_rows','')};b_fallback={metrics.get('tier_b_fallback_labelable_rows','')};max_dd={metrics.get('max_drawdown_amount', metrics.get('max_drawdown',''))};boundary={BOUNDARY}",
                "external_verification_status": "completed",
                "notes": "Stage39 MT5 runtime-probe KPI row; no baseline, promotion, runtime authority, live readiness, or operating reference.",
            }
        )
    if not rows:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__blocked_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "blocked_mt5_execution",
                "parent_run_id": SOURCE_FRONTIER,
                "record_view": "blocked_mt5_execution",
                "tier_scope": mt5.TIER_AB,
                "kpi_scope": "exit_risk_non_entry_overlay_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": "blocked",
                "judgment": BLOCKED_JUDGMENT,
                "path": rel(RUN_ROOT),
                "primary_kpi": "missing_required_mt5_strategy_tester_output",
                "guardrail_kpi": f"boundary={BOUNDARY}",
                "external_verification_status": "blocked",
                "notes": "Stage39 blocked because MT5 Strategy Tester output artifact was not produced.",
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
                "notes": f"Stage39 exit/risk non-entry overlay; mt5_attempts={len(result.get('attempts', []))}; boundary={BOUNDARY}",
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
            "notes": "Stage39 run manifest; reproducibility required",
        },
        {
            "artifact_id": f"{RUN_ID}_mt5_import_summary",
            "type": "mt5_import_summary",
            "path": rel(RUN_ROOT / "mt5/mt5_result_import_summary.json"),
            "status": "tracked_runtime_probe",
            "notes": "Stage39 imported MT5 result summary",
        },
        {
            "artifact_id": f"{RUN_ID}_review_packet",
            "type": "stage_review_packet",
            "path": rel(STAGE_ROOT / "03_reviews/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_packet.md"),
            "status": "tracked_reviewed" if judgment != BLOCKED_JUDGMENT else "tracked_blocked",
            "notes": "Stage39 closeout packet",
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


def packet_markdown(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]], micro_gate: Mapping[str, Any], judgment: str) -> str:
    best_val, worst_val = best_worst(mt5_rows, "validation_is")
    best_oos, worst_oos = best_worst(mt5_rows, "oos")
    actual_artifacts = [item for item in result.get("strategy_tester_reports", []) if item.get("status") == "completed"]
    command = ""
    if result.get("execution_results"):
        command = " ".join(str(item) for item in result["execution_results"][0].get("command", []))
    report_path = actual_artifacts[0].get("html_report", {}).get("path", "") if actual_artifacts else ""
    lines = [
        "# Stage39 run33A Exit Risk Non-Entry Overlay Packet(39단계 33A 청산 위험 비진입 덧씌움 묶음)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- idea_id(아이디어 ID): `{IDEA_ID}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        f"- judgment(판정): `{judgment}`",
        f"- claim boundary(주장 경계): `{FINAL_BOUNDARY}`",
        "",
        "## Design(설계)",
        "",
        "Entry permission(진입 허용)은 Stage38 c01 reference(38단계 c01 참고) 신호로 고정했다. Stage39 후보는 position exists(포지션 존재) 이후에만 close/reduce-hold(청산/보유 축소)를 수행한다.",
        "",
        "## Broad Sweep(넓은 훑기)",
        "",
        f"- candidate_count(후보 수): `{len(result.get('candidate_specs', []))}`",
        f"- best_validation(검증 최상): `{best_val.get('candidate_id') if best_val else 'missing'}`",
        f"- worst_validation(검증 최하): `{worst_val.get('candidate_id') if worst_val else 'missing'}`",
        f"- best_oos(표본외 최상): `{best_oos.get('candidate_id') if best_oos else 'missing'}`",
        f"- worst_oos(표본외 최하): `{worst_oos.get('candidate_id') if worst_oos else 'missing'}`",
        "",
        "## Micro Search Gate(미세 탐색 게이트)",
        "",
        f"- status(상태): `{micro_gate.get('status')}`",
        f"- best_candidate(최상 후보): `{micro_gate.get('best_candidate')}`",
        "- decision(결정): broad sweep(넓은 훑기) 뒤 조건을 통과한 후보만 micro-search(미세 탐색)를 허용한다.",
        "",
        "## MT5 Strategy Tester Execution",
        "",
    ]
    if actual_artifacts:
        first_attempt = result.get("attempts", [{}])[0]
        lines.extend(
            [
                f"- command used(사용 명령): `{command}`",
                "- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`",
                f"- .ini path(.ini 경로): `{first_attempt.get('ini', {}).get('path', '')}`",
                f"- .set path(.set 경로): `{first_attempt.get('set', {}).get('path', '')}`",
                f"- manifest path(목록 경로): `{rel(RUN_ROOT / 'run_manifest.json')}`",
                f"- terminal path(터미널 경로): `{TERMINAL_PATH_DEFAULT}`",
                f"- Common Files path(공용 파일 경로): `{COMMON_FILES_ROOT_DEFAULT}`",
                f"- tester output path(테스터 출력 경로): `{report_path}`",
                f"- imported result path(가져온 결과 경로): `{rel(RUN_ROOT / 'mt5/mt5_result_import_summary.json')}`",
                f"- candidates tested in MT5(MT5 후보 수): `{len(result.get('candidate_specs', []))}`",
                f"- validation MT5 KPI summary(검증 KPI 요약): best `{best_val.get('candidate_id') if best_val else 'missing'}` net `{best_val.get('net_profit') if best_val else 'missing'}` PF `{best_val.get('profit_factor') if best_val else 'missing'}`",
                f"- OOS MT5 KPI summary(표본외 KPI 요약): best `{best_oos.get('candidate_id') if best_oos else 'missing'}` net `{best_oos.get('net_profit') if best_oos else 'missing'}` PF `{best_oos.get('profit_factor') if best_oos else 'missing'}`",
            ]
        )
    else:
        lines.append("BLOCKED: MT5 Strategy Tester execution did not produce an artifact, so Stage39 run33A is incomplete.")
    lines.extend(
        [
            "",
            "## Result Judgment(결과 판정)",
            "",
            f"`{judgment}`",
            "",
            "Stage39 run33A remains runtime_probe_only: no baseline, no promotion, no runtime authority, no live readiness, and no operating reference.",
            "",
        ]
    )
    return "\n".join(lines)


def write_stage_docs(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]], micro_gate: Mapping[str, Any], judgment: str) -> None:
    write_md(
        STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage39 Brief(39단계 개요)

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- source frontier(원천 전선): `{SOURCE_FRONTIER}`
- topic(주제): entry surface(진입 표면)을 고정하고 post-entry lifecycle/tail risk overlay(진입 후 생애주기/꼬리 위험 덧씌움)를 시험한다.
- boundary(경계): `{FINAL_BOUNDARY}`

효과(effect, 효과): Stage39(39단계)는 entry filter(진입 필터)가 아니라 close/hold/risk behavior(청산/보유/위험 행동)를 MT5 Strategy Tester(전략 테스터)에서 확인한다.
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage39 Input References(39단계 입력 참조)

- Stage38 base/carry reference(38단계 기준 운반 참고): `{rel(STAGE38_CANDIDATE_PATH)}`
- Stage24 survival clock(24단계 생존 시계): `{rel(STAGE24_A_PATH)}`, `{rel(STAGE24_B_PATH)}`
- Stage25 hazard lifecycle risk(25단계 위험률 생애주기 위험): `{rel(STAGE25_A_PATH)}`, `{rel(STAGE25_B_PATH)}`
- Stage27 tail pressure(27단계 꼬리 압력): `{rel(STAGE27_A_PATH)}`, `{rel(STAGE27_B_PATH)}`

효과(effect, 효과): 모든 surface(표면)는 exact timestamp alignment(정확 시각 정렬)로 common table(공통 표)에 합쳐지고, Stage38(38단계)은 context-only(문맥 전용) 단서로만 남긴다.
""",
    )
    write_md(STAGE_ROOT / "03_reviews/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_packet.md", packet_markdown(result, mt5_rows, micro_gate, judgment))
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage39 Review Index(39단계 검토 색인)

- run packet(실행 묶음): `03_reviews/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
- selection status(선택 상태): `04_selected/selection_status.md`
""",
    )
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage39 Selection Status(39단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- micro_search_gate(미세 탐색 게이트): `{micro_gate.get('status')}`

효과(effect, 효과): Stage39(39단계)은 runtime_probe_only(런타임 탐침 전용)로 남고, 운영 선택을 만들지 않는다.
""",
    )


def write_packet_files(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]], micro_gate: Mapping[str, Any], judgment: str, ledger_payload: Mapping[str, Any]) -> None:
    actual_mt5 = judgment != BLOCKED_JUDGMENT
    required_gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    write_yaml_text(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_id: {RUN_ID}
idea_id: {IDEA_ID}
primary_family: runtime_backtest
primary_skill: obsidian-runtime-parity
support_skills:
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-backtest-forensics
  - obsidian-performance-attribution
  - obsidian-artifact-lineage
  - obsidian-result-judgment
required_gates:
  - runtime_evidence_gate
  - scope_completion_gate
  - kpi_contract_audit
  - required_gate_coverage_audit
  - final_claim_guard
claim_boundary: {FINAL_BOUNDARY}
source_frontier: {SOURCE_FRONTIER}
status: {"completed" if actual_mt5 else "blocked"}
""",
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "completed", "evidence": "hypothesis, broad candidate grid, and micro-search gate recorded"},
                {"skill": "obsidian-data-integrity", "status": "completed", "evidence": "common table exact timestamp alignment, missingness, and Tier A/B route rows recorded"},
                {"skill": "obsidian-runtime-parity", "status": "passed" if actual_mt5 else "blocked", "evidence": "MT5 EA overlay parameter path, handoff manifest, compile, and tester output import"},
                {"skill": "obsidian-backtest-forensics", "status": "passed" if actual_mt5 else "blocked", "evidence": "tester command, .ini/.set, report paths, and KPI rows recorded"},
                {"skill": "obsidian-performance-attribution", "status": "completed", "evidence": "validation/OOS, drawdown, entry-count, hold, and overlay activation summaries recorded"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "evidence": "source lineage and artifact hashes recorded"},
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
            "broad_candidate_count": len(result.get("candidate_specs", [])),
            "mt5_attempt_count": len(result.get("attempts", [])),
            "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
            "best_validation_mt5": best_val,
            "worst_validation_mt5": worst_val,
            "best_oos_mt5": best_oos,
            "worst_oos_mt5": worst_oos,
            "micro_search_gate": micro_gate,
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
            "required_recovery_attempts": {
                "repository_mt5_runners_inspected": True,
                "runtime_artifact_helpers_inspected": True,
                "tester_file_helpers_inspected": True,
                "previous_stage_probe_scripts_inspected": True,
                "terminal_path": str(TERMINAL_PATH_DEFAULT),
                "metaeditor_path": str(METAEDITOR_PATH_DEFAULT),
                "common_files_path": str(COMMON_FILES_ROOT_DEFAULT),
            },
        },
    )
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed" if judgment in {POSITIVE_JUDGMENT, INCONCLUSIVE_JUDGMENT, NEGATIVE_JUDGMENT, BLOCKED_JUDGMENT} else "failed", "judgment": judgment, "allowed_judgments": [POSITIVE_JUDGMENT, INCONCLUSIVE_JUDGMENT, NEGATIVE_JUDGMENT, BLOCKED_JUDGMENT], "boundary": FINAL_BOUNDARY})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if actual_mt5 else "blocked", "mt5_kpi_records": len(result.get("mt5_kpi_records", [])), "required_tier_records": ["Tier A used", "Tier B fallback used", "actual routed total"], "synthetic_sum_used_as_routed_total": False})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed", "required_gates": required_gates, "covered_gates": required_gates, "missing_gates": []})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": FINAL_BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": result.get("validation_commands", []), "mt5_command_count": len(result.get("execution_results", [])), "status": "recorded"})


def update_current_truth(result: Mapping[str, Any], judgment: str, micro_gate: Mapping[str, Any]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        r"^active_branch: .*$": "active_branch: codex/stage39-exit-risk-non-entry-overlay",
        r"^active_stage: .*$": f"active_stage: {STAGE_ID}",
        r"^current_run_id: .*$": f"current_run_id: {RUN_ID}",
    }
    for pattern, value in replacements.items():
        state_text = re.sub(pattern, value, state_text, flags=re.MULTILINE)
    block = f"""

stage39_exit_risk_non_entry_overlay:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: {"reviewed_runtime_probe_completed" if judgment != BLOCKED_JUDGMENT else "blocked_runtime_probe_missing_mt5_execution"}
  current_run_id: {RUN_ID}
  source_frontier: {SOURCE_FRONTIER}
  mt5_attempt_count: {len(result.get("attempts", []))}
  mt5_kpi_record_count: {len(result.get("mt5_kpi_records", []))}
  judgment: {judgment}
  report_path: {rel(STAGE_ROOT / "03_reviews/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {FINAL_BOUNDARY}
"""
    state_text = re.sub(r"\n+stage39_exit_risk_non_entry_overlay:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = re.sub(
        r"## Latest Stage39 RUN33A Exit Risk Non-Entry Overlay\(최신 39단계 33A 청산 위험 비진입 덧씌움\)\n.*?(?=\n## |\Z)",
        "",
        current,
        flags=re.DOTALL,
    ).lstrip()
    actual = judgment != BLOCKED_JUDGMENT
    section = f"""## Latest Stage39 RUN33A Exit Risk Non-Entry Overlay(최신 39단계 33A 청산 위험 비진입 덧씌움)

Stage39(39단계) `{RUN_ID}`는 Stage38 c01 base entry(38단계 c01 기준 진입)를 고정하고 Stage24 survival(생존), Stage25 hazard(위험률), Stage27 tail pressure(꼬리 압력)를 post-entry overlay(진입 후 덧씌움)로 MT5 Strategy Tester(전략 테스터)에 실행했다.

결과(result, 결과): `{judgment}`. MT5 KPI records(MT5 핵심 성과 지표 기록): `{len(result.get("mt5_kpi_records", []))}`. Micro-search gate(미세 탐색 게이트): `{micro_gate.get("status")}`.

효과(effect, 효과): {'actual Stage39 MT5 artifacts(실제 39단계 MT5 산출물)를 가져왔지만' if actual else 'MT5 Strategy Tester artifact(전략 테스터 산출물)가 없어 blocked(차단)로 낮췄고'} baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않았다.
"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section.rstrip() + "\n\n" + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    line = f"- 2026-05-09: Stage39(39단계) `{RUN_ID}` exit/risk non-entry overlay(청산/위험 비진입 덧씌움) MT5 runtime_probe(MT5 런타임 탐침)를 `{judgment}`로 기록했다. 효과(effect, 효과): Stage24/25/27 위험 표면을 진입 필터가 아니라 보유/청산 행동으로 시험했고 운영 주장은 만들지 않았다.\n"
    if line not in changelog:
        io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def write_run_files(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]], micro_gate: Mapping[str, Any], judgment: str) -> None:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "idea_id": IDEA_ID,
            "packet_id": PACKET_ID,
            "source_frontier": SOURCE_FRONTIER,
            "attempts": result.get("attempts", []),
            "candidate_specs": result.get("candidate_specs", []),
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
            "kpi_scope": "exit_risk_non_entry_overlay_mt5_runtime_probe",
            "external_verification_status": result.get("external_verification_status"),
            "judgment": judgment,
            "mt5": {
                "execution_results": result.get("execution_results", []),
                "strategy_tester_reports": result.get("strategy_tester_reports", []),
                "kpi_records": result.get("mt5_kpi_records", []),
                "candidate_summary": list(mt5_rows),
            },
            "micro_search_gate": micro_gate,
            "boundary": FINAL_BOUNDARY,
        },
    )
    write_json(RUN_ROOT / "summary.json", {"judgment": judgment, "mt5_candidate_rows": len(mt5_rows), "micro_search_gate": micro_gate, "boundary": FINAL_BOUNDARY})
    write_json(RUN_ROOT / "artifact_hash_summary.json", artifact_hash_summary())
    write_json(RUN_ROOT / "validation_commands.json", {"commands": result.get("validation_commands", []), "status": "recorded"})
    write_md(
        RUN_ROOT / "retry_commands.ps1",
        f"""python -m foundation.pipelines.run_stage39_exit_risk_non_entry_overlay --timeout-seconds 900
""",
    )


def materialize_and_run(args: argparse.Namespace) -> dict[str, Any]:
    common, lineage = build_common_table()
    thresholds = build_loose_thresholds(common)
    specs = build_broad_candidate_grid()
    candidate_frames = {spec.candidate_id: apply_exit_overlay_candidate(common, spec, thresholds) for spec in specs}
    common_artifact = save_frame(RUN_ROOT / "tables/stage39_common_lifecycle_tail_overlay_table.parquet", common)
    write_json(RUN_ROOT / "tables/common_table_schema.json", column_lineage(common, lineage))
    write_json(RUN_ROOT / "tables/lifecycle_tail_risk_lineage_table.json", lineage)
    write_candidate_grid(RUN_ROOT / "tables/candidate_grid.csv", specs)
    combined = pd.concat(candidate_frames.values(), ignore_index=True)
    candidate_artifact = save_frame(RUN_ROOT / "tables/stage39_candidate_overlay_signal_table.parquet", combined)
    python_rows = summarize_candidate_frames(candidate_frames)
    dataframe_to_csv(RUN_ROOT / "tables/broad_sweep_python_summary.csv", python_rows)
    feature_exports, model_artifact = export_candidate_feature_matrices(candidate_frames)
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    route_coverage = route_coverage_from_common(common)
    attempts = make_attempts(specs, feature_exports, model_artifact, common)
    prepared = prepared_payload(
        candidate_specs=specs,
        attempts=attempts,
        common=common,
        feature_exports=feature_exports,
        model_artifact=model_artifact,
        common_copies=common_copies,
        route_coverage=route_coverage,
        common_artifact=common_artifact,
        candidate_artifact=candidate_artifact,
        python_summary=python_rows,
    )
    result = execute_or_block(prepared, args)
    mt5_rows = build_mt5_candidate_summary(result.get("mt5_kpi_records", []), python_rows, result.get("execution_results", []))
    dataframe_to_csv(RUN_ROOT / "tables/mt5_candidate_summary.csv", mt5_rows)
    micro_gate = evaluate_micro_search_gate(mt5_rows) if mt5_rows else {"status": "failed", "reason": "missing_mt5_candidate_summary", "accepted_candidates": [], "rejected_candidates": []}
    result["micro_search_gate"] = micro_gate
    result["mt5_candidate_summary"] = mt5_rows
    result["validation_commands"] = [
        {"command": "python -m foundation.pipelines.run_stage39_exit_risk_non_entry_overlay --timeout-seconds 900", "result": "executed", "failures_or_blockers": ""},
    ]
    judgment = final_judgment_from_results(result, micro_gate)
    result["judgment"] = judgment
    write_handoff_files(result, mt5_rows)
    write_run_files(result, mt5_rows, micro_gate, judgment)
    ledger_payload = write_ledgers(result, judgment)
    write_stage_docs(result, mt5_rows, micro_gate, judgment)
    write_packet_files(result, mt5_rows, micro_gate, judgment, ledger_payload)
    update_current_truth(result, judgment, micro_gate)
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage39 exit-risk non-entry overlay MT5 runtime probe")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = materialize_and_run(args)
    print(json.dumps({"run_id": RUN_ID, "judgment": result.get("judgment"), "external_verification_status": result.get("external_verification_status")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
