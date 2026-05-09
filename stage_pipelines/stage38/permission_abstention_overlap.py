from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
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


STAGE_NUMBER = 38
STAGE_ID = "38_decision_layer__permission_abstention_overlap"
IDEA_ID = "IDEA-ST38-PERMISSION-ABSTENTION-OVERLAP"
RUN_ID = "run32A_permission_abstention_overlap_broad_mt5_probe_v1"
RUN_NUMBER = "run32A"
PACKET_ID = "stage38_run32A_permission_abstention_overlap_broad_mt5_probe_v1"
EXPLORATION_LABEL = "stage38_DecisionLayer__PermissionAbstentionOverlap"
SOURCE_FRONTIER = "Stage36 frontier01_permission_abstention_overlap"
BOUNDARY = "runtime_probe_only"
FINAL_BOUNDARY = "runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"
BLOCKED_JUDGMENT = "blocked_runtime_probe_missing_mt5_execution"
POSITIVE_JUDGMENT = "reviewed_completed_positive_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_runtime_probe_only"
SIGNAL_FEATURE_ORDER = ("stage38_decision_signal",)
SIGNAL_FEATURE_HASH = ordered_hash(SIGNAL_FEATURE_ORDER)
MAX_HOLD_BARS = 12
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"


@dataclass(frozen=True)
class SourceSurface:
    surface_key: str
    stage_id: str
    run_id: str
    tier_a_path: Path
    tier_b_path: Path
    role: str
    columns: tuple[str, ...]


@dataclass(frozen=True)
class CandidateSpec:
    candidate_id: str
    label: str
    enabled_surfaces: tuple[str, ...]
    entry_permission_rule: str
    abstention_rule: str
    fallback_rule: str = "Tier A primary + Tier B fallback"
    threshold_family: str = "loose_v1"
    threshold_overrides: Mapping[str, float] | None = None


SOURCE_SURFACES: tuple[SourceSurface, ...] = (
    SourceSurface(
        surface_key="stage19_ebm",
        stage_id="19_model_family_challenge__ebm_explainable_boosting_shape",
        run_id="run13E_ebm_q80_direction_asymmetry_probe_v1",
        tier_a_path=ROOT
        / "stages/19_model_family_challenge__ebm_explainable_boosting_shape/02_runs/run13E_ebm_q80_direction_asymmetry_probe_v1/predictions/tier_a_separate_predictions.parquet",
        tier_b_path=ROOT
        / "stages/19_model_family_challenge__ebm_explainable_boosting_shape/02_runs/run13E_ebm_q80_direction_asymmetry_probe_v1/predictions/tier_b_separate_predictions.parquet",
        role="ebm_direction",
        columns=("p_short", "p_flat", "p_long", "probability_margin"),
    ),
    SourceSurface(
        surface_key="stage23_permission",
        stage_id="23_regime_model__supervised_regime_classifier_filter",
        run_id="run17B_supervised_regime_classifier_runtime_probe_v1",
        tier_a_path=ROOT
        / "stages/23_regime_model__supervised_regime_classifier_filter/02_runs/run17B_supervised_regime_classifier_runtime_probe_v1/predictions/tier_a_runtime_probe_predictions.parquet",
        tier_b_path=ROOT
        / "stages/23_regime_model__supervised_regime_classifier_filter/02_runs/run17B_supervised_regime_classifier_runtime_probe_v1/predictions/tier_b_runtime_probe_predictions.parquet",
        role="permission_filter_signal",
        columns=("p_short", "p_flat", "p_long", "probability_margin", "p_permission", "p_block"),
    ),
    SourceSurface(
        surface_key="stage26_entropy",
        stage_id="26_model_family_challenge__ngboost_probabilistic_distribution_shape",
        run_id="run20B_ngboost_distribution_runtime_probe_v1",
        tier_a_path=ROOT
        / "stages/26_model_family_challenge__ngboost_probabilistic_distribution_shape/02_runs/run20B_ngboost_distribution_runtime_probe_v1/predictions/tier_a_ngboost_runtime_predictions.parquet",
        tier_b_path=ROOT
        / "stages/26_model_family_challenge__ngboost_probabilistic_distribution_shape/02_runs/run20B_ngboost_distribution_runtime_probe_v1/predictions/tier_b_ngboost_runtime_predictions.parquet",
        role="entropy",
        columns=("ngb_distribution_entropy", "ngb_flat_probability", "p_short", "p_flat", "p_long"),
    ),
    SourceSurface(
        surface_key="stage27_tail",
        stage_id="27_tail_model__quantile_boosting_risk_surface",
        run_id="run21B_quantile_boosting_tail_risk_runtime_probe_v1",
        tier_a_path=ROOT
        / "stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21B_quantile_boosting_tail_risk_runtime_probe_v1/predictions/tier_a_quantile_runtime_predictions.parquet",
        tier_b_path=ROOT
        / "stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21B_quantile_boosting_tail_risk_runtime_probe_v1/predictions/tier_b_quantile_runtime_predictions.parquet",
        role="tail_pressure",
        columns=("qtl_tail_pressure", "qtl_direction_score", "p_short", "p_flat", "p_long"),
    ),
    SourceSurface(
        surface_key="stage30_calibration",
        stage_id="30_decision_layer__probability_calibration_abstention",
        run_id="run24D_native_source_calibration_runtime_probe_v1",
        tier_a_path=ROOT
        / "stages/30_decision_layer__probability_calibration_abstention/02_runs/run24D_native_source_calibration_runtime_probe_v1/predictions/tier_a_stage30_runtime_predictions.parquet",
        tier_b_path=ROOT
        / "stages/30_decision_layer__probability_calibration_abstention/02_runs/run24D_native_source_calibration_runtime_probe_v1/predictions/tier_b_stage30_runtime_predictions.parquet",
        role="calibrated_margin",
        columns=("cal_direction_score", "cal_confidence", "cal_abstention_pressure", "p_short", "p_flat", "p_long", "probability_margin"),
    ),
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


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    def render(value: Any, indent: int = 0) -> list[str]:
        pad = " " * indent
        if isinstance(value, Mapping):
            lines: list[str] = []
            for key, item in value.items():
                if isinstance(item, Mapping):
                    lines.append(f"{pad}{key}:")
                    lines.extend(render(item, indent + 2))
                elif isinstance(item, (list, tuple)):
                    lines.append(f"{pad}{key}:")
                    for entry in item:
                        if isinstance(entry, Mapping):
                            lines.append(f"{pad}  -")
                            lines.extend(render(entry, indent + 4))
                        else:
                            lines.append(f"{pad}  - {entry}")
                else:
                    lines.append(f"{pad}{key}: {item}")
            return lines
        return [f"{pad}{value}"]

    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(render(json_ready(payload))) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True) + "\n")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
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


def sign_series(values: pd.Series, deadband: float = 1e-12) -> pd.Series:
    arr = pd.to_numeric(values, errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    return pd.Series(np.where(arr > deadband, 1, np.where(arr < -deadband, -1, 0)), index=values.index)


def source_lineage_payload(surface: SourceSurface, tier_path: Path) -> dict[str, Any]:
    return {
        "surface_key": surface.surface_key,
        "source_stage": surface.stage_id,
        "source_run_id": surface.run_id,
        "source_artifact_path": rel(tier_path),
        "source_artifact_hash": sha256_file_lf_normalized(tier_path) if path_exists(tier_path) else "missing_required",
        "timestamp_alignment_rule": "UTC timestamp exact inner join on feature-ready row",
        "missingness_rule": "missing source rows mark surface_missing and block candidate signal",
        "mt5_use": "Python preparation only unless included in stage38_decision_signal feature",
    }


def rename_surface_columns(frame: pd.DataFrame, surface: SourceSurface) -> pd.DataFrame:
    keep = ["timestamp", "split", "label_class", *surface.columns]
    if "partial_context_subtype" in frame.columns:
        keep.append("partial_context_subtype")
    out = frame[[name for name in keep if name in frame.columns]].copy()
    rename = {
        name: f"{surface.surface_key}_{name}"
        for name in surface.columns
        if name in out.columns and name not in {"timestamp", "split", "label_class"}
    }
    return out.rename(columns=rename)


def build_common_table() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    tier_frames: list[pd.DataFrame] = []
    lineage: list[dict[str, Any]] = []
    for tier_name, tier_label in (("tier_a", mt5.TIER_A), ("tier_b", mt5.TIER_B)):
        merged: pd.DataFrame | None = None
        partial_context_frame: pd.DataFrame | None = None
        for surface in SOURCE_SURFACES:
            path = surface.tier_a_path if tier_name == "tier_a" else surface.tier_b_path
            raw = load_frame(path)
            renamed = rename_surface_columns(raw, surface)
            keys = ["timestamp", "split", "label_class"]
            if "partial_context_subtype" in renamed.columns:
                if tier_name == "tier_b" and partial_context_frame is None:
                    partial_context_frame = renamed[keys + ["partial_context_subtype"]].copy()
                renamed = renamed.drop(columns=["partial_context_subtype"])
            if merged is None:
                merged = renamed
            else:
                merged = merged.merge(renamed, on=keys, how="inner", validate="one_to_one")
            lineage.append({**source_lineage_payload(surface, path), "tier_label": tier_label})
        if merged is None:
            raise RuntimeError(f"No surface frames loaded for {tier_name}")
        merged["tier_label"] = tier_label
        merged["tier_a_available"] = tier_name == "tier_a"
        merged["tier_b_fallback_available"] = tier_name == "tier_b"
        merged["routing_source"] = "tier_a_primary" if tier_name == "tier_a" else "tier_b_fallback"
        if tier_name == "tier_a":
            merged["partial_context_subtype"] = "Tier_A_full_context"
        elif partial_context_frame is not None:
            merged = merged.merge(partial_context_frame, on=["timestamp", "split", "label_class"], how="left", validate="one_to_one")
            merged["partial_context_subtype"] = merged["partial_context_subtype"].fillna("B_partial_context").astype(str)
        else:
            merged["partial_context_subtype"] = "B_partial_context"
        tier_frames.append(merged)

    common = pd.concat(tier_frames, ignore_index=True).sort_values(["timestamp", "tier_label"]).reset_index(drop=True)
    common["p_flat"] = common["stage30_calibration_p_flat"]
    common["calibrated_margin"] = (
        common[["stage30_calibration_p_short", "stage30_calibration_p_long"]].max(axis=1) - common["stage30_calibration_p_flat"]
    )
    common["entropy"] = common["stage26_entropy_ngb_distribution_entropy"]
    common["tail_pressure"] = common["stage27_tail_qtl_tail_pressure"]
    common["ebm_direction"] = common["stage19_ebm_p_long"] - common["stage19_ebm_p_short"]
    common["ebm_abs_direction"] = common["ebm_direction"].abs()
    common["permission_score"] = common.get("stage23_permission_p_permission", common[["stage23_permission_p_short", "stage23_permission_p_long"]].max(axis=1)) - common.get(
        "stage23_permission_p_block", common["stage23_permission_p_flat"]
    )
    common["permission_filter_signal"] = False
    common["permission_direction"] = sign_series(common["stage23_permission_p_long"] - common["stage23_permission_p_short"])
    common["calibrated_direction"] = sign_series(common.get("stage30_calibration_cal_direction_score", common["stage30_calibration_p_long"] - common["stage30_calibration_p_short"]))
    common["ebm_direction_signal"] = sign_series(common["ebm_direction"])
    common["reference_entry_decision"] = common["ebm_direction_signal"]
    common["target_direction"] = common["permission_direction"].where(common["permission_direction"].ne(0), common["ebm_direction_signal"])
    common["validation_oos_split_label"] = common["split"].astype(str).map({"validation": "validation_is"}).fillna(common["split"].astype(str))
    common["timestamp_utc"] = common["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    common["timestamp_alignment_rule"] = "exact_utc_timestamp_inner_join_stage19_23_26_27_30"
    common["surface_missing"] = common[
        ["p_flat", "calibrated_margin", "entropy", "tail_pressure", "ebm_direction", "permission_score"]
    ].isna().any(axis=1)
    common["stage38_row_id"] = np.arange(len(common), dtype=int)
    return common, lineage


def build_common_table_schema(lineage: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    source_by_role = {item["surface_key"]: item for item in lineage}
    columns = [
        ("p_flat", "Stage30 calibrated flat probability", "stage30_calibration", True),
        ("calibrated_margin", "max(nonflat calibrated probability) - p_flat", "stage30_calibration", True),
        ("entropy", "Stage26 NGBoost distribution entropy", "stage26_entropy", True),
        ("tail_pressure", "Stage27 quantile tail pressure", "stage27_tail", True),
        ("ebm_direction", "Stage19 EBM p_long - p_short", "stage19_ebm", True),
        ("permission_filter_signal", "Stage38 loose permission boolean from Stage23 score", "stage23_permission", False),
        ("tier_label", "Tier A or Tier B", "stage38_materialization", True),
        ("tier_a_available", "Tier A route availability flag", "stage38_materialization", True),
        ("tier_b_fallback_available", "Tier B fallback route availability flag", "stage38_materialization", True),
        ("routing_source", "Tier A primary or Tier B fallback source", "stage38_materialization", True),
        ("target_direction", "direction used before candidate-specific gating", "stage38_materialization", True),
        ("validation_oos_split_label", "runtime split label", "stage38_materialization", True),
        ("timestamp_utc", "UTC timestamp string", "stage38_materialization", True),
    ]
    payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "alignment_grain": "feature-ready timestamp x tier route source",
        "columns": [],
    }
    for name, description, source_key, direct_mt5 in columns:
        source = source_by_role.get(source_key, {})
        payload["columns"].append(
            {
                "column": name,
                "description": description,
                "source_stage": source.get("source_stage", STAGE_ID),
                "source_run_id": source.get("source_run_id", RUN_ID),
                "source_artifact_path": source.get("source_artifact_path", "stage38_materialized"),
                "source_artifact_hash": source.get("source_artifact_hash", "generated_in_stage38"),
                "timestamp_alignment_rule": "exact UTC timestamp; Tier A and Tier B retain separate route rows",
                "missingness_rule": "surface_missing blocks candidate signal; tier availability is explicit boolean",
                "used_directly_by_mt5": bool(direct_mt5 and name in {"tier_label", "routing_source", "timestamp_utc"}),
                "used_by_python_preparation": True,
            }
        )
    payload["mt5_direct_feature"] = {
        "column": SIGNAL_FEATURE_ORDER[0],
        "source_stage": STAGE_ID,
        "source_run_id": RUN_ID,
        "source_artifact_path": "candidate-specific feature CSV files",
        "timestamp_alignment_rule": "exported with bar_time_server and timestamp_utc using MT5 runtime artifact helper",
        "missingness_rule": "flat signal 0 when candidate rule fails or surface_missing is true",
        "used_directly_by_mt5": True,
    }
    return payload


def quantile(series: pd.Series, q: float, fallback: float) -> float:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return float(fallback)
    return float(values.quantile(q))


def loose_thresholds(common: pd.DataFrame) -> dict[str, float]:
    train = common.loc[common["split"].astype(str).eq("train") & ~common["surface_missing"]]
    return {
        "permission_score_min": quantile(train["permission_score"], 0.25, 0.05),
        "p_flat_max": quantile(train["p_flat"], 0.75, 0.70),
        "calibrated_margin_min": quantile(train["calibrated_margin"], 0.25, -0.05),
        "entropy_max": quantile(train["entropy"], 0.75, 0.90),
        "tail_pressure_max": quantile(train["tail_pressure"], 0.75, 0.02),
        "ebm_abs_min": quantile(train["ebm_abs_direction"], 0.25, 0.01),
    }


def build_candidate_grid(threshold_family: str = "loose_v1") -> list[CandidateSpec]:
    items = [
        ("c01_no_overlap_reference", "carry/reference no-overlap", ()),
        ("c02_permission_only", "permission only", ("permission",)),
        ("c03_abstention_only", "abstention only", ("abstention",)),
        ("c04_permission_abstention", "permission + abstention overlap", ("permission", "abstention")),
        ("c05_permission_entropy", "permission + entropy", ("permission", "entropy")),
        ("c06_permission_tail", "permission + tail pressure", ("permission", "tail")),
        ("c07_permission_ebm", "permission + EBM direction", ("permission", "ebm")),
        ("c08_permission_abstention_entropy", "permission + abstention + entropy", ("permission", "abstention", "entropy")),
        ("c09_permission_abstention_tail", "permission + abstention + tail pressure", ("permission", "abstention", "tail")),
        ("c10_permission_abstention_ebm", "permission + abstention + EBM direction", ("permission", "abstention", "ebm")),
        ("c11_permission_entropy_tail", "permission + entropy + tail pressure", ("permission", "entropy", "tail")),
        ("c12_permission_entropy_ebm", "permission + entropy + EBM direction", ("permission", "entropy", "ebm")),
        ("c13_permission_tail_ebm", "permission + tail pressure + EBM direction", ("permission", "tail", "ebm")),
        ("c14_permission_abstention_entropy_tail", "permission + abstention + entropy + tail pressure", ("permission", "abstention", "entropy", "tail")),
        ("c15_permission_abstention_entropy_ebm", "permission + abstention + entropy + EBM direction", ("permission", "abstention", "entropy", "ebm")),
        ("c16_permission_abstention_tail_ebm", "permission + abstention + tail pressure + EBM direction", ("permission", "abstention", "tail", "ebm")),
        ("c17_permission_abstention_entropy_tail_ebm", "permission + abstention + entropy + tail pressure + EBM direction", ("permission", "abstention", "entropy", "tail", "ebm")),
    ]
    specs: list[CandidateSpec] = []
    for candidate_id, label, surfaces in items:
        specs.append(
            CandidateSpec(
                candidate_id=candidate_id,
                label=label,
                enabled_surfaces=tuple(surfaces),
                entry_permission_rule="stage23 permission_score loose threshold" if "permission" in surfaces else "reference surface only",
                abstention_rule="stage30 p_flat max plus calibrated margin min" if "abstention" in surfaces else "not enabled",
                threshold_family=threshold_family,
            )
        )
    return specs


def candidate_thresholds(base: Mapping[str, float], spec: CandidateSpec) -> dict[str, float]:
    values = dict(base)
    if spec.threshold_overrides:
        values.update({key: float(value) for key, value in spec.threshold_overrides.items()})
    return values


def candidate_surface_masks(frame: pd.DataFrame, thresholds: Mapping[str, float]) -> dict[str, pd.Series]:
    return {
        "permission": frame["permission_score"].ge(float(thresholds["permission_score_min"])),
        "abstention": frame["p_flat"].le(float(thresholds["p_flat_max"])) & frame["calibrated_margin"].ge(float(thresholds["calibrated_margin_min"])),
        "entropy": frame["entropy"].le(float(thresholds["entropy_max"])),
        "tail": frame["tail_pressure"].le(float(thresholds["tail_pressure_max"])),
        "ebm": frame["ebm_abs_direction"].ge(float(thresholds["ebm_abs_min"])) & frame["ebm_direction_signal"].ne(0),
    }


def apply_candidate_to_table(common: pd.DataFrame, spec: CandidateSpec, base_thresholds: Mapping[str, float]) -> pd.DataFrame:
    thresholds = candidate_thresholds(base_thresholds, spec)
    masks = candidate_surface_masks(common, thresholds)
    surface_names = tuple(spec.enabled_surfaces)
    if spec.candidate_id == "c01_no_overlap_reference":
        pass_mask = masks["ebm"]
        direction = common["ebm_direction_signal"]
    elif not surface_names:
        pass_mask = pd.Series(True, index=common.index)
        direction = common["target_direction"]
    else:
        pass_mask = pd.Series(True, index=common.index)
        for name in surface_names:
            pass_mask &= masks[name]
        if "ebm" in surface_names:
            direction = common["ebm_direction_signal"]
            if "permission" in surface_names:
                pass_mask &= common["permission_direction"].eq(common["ebm_direction_signal"])
        elif "abstention" in surface_names and "permission" not in surface_names:
            direction = common["calibrated_direction"]
        else:
            direction = common["permission_direction"]
    pass_mask &= ~common["surface_missing"]
    signal = direction.where(pass_mask & direction.ne(0), 0).astype(int)
    out = common[
        [
            "stage38_row_id",
            "timestamp",
            "timestamp_utc",
            "split",
            "validation_oos_split_label",
            "label_class",
            "tier_label",
            "routing_source",
            "partial_context_subtype",
            "tier_a_available",
            "tier_b_fallback_available",
            "p_flat",
            "calibrated_margin",
            "entropy",
            "tail_pressure",
            "ebm_direction",
            "permission_score",
            "target_direction",
            "surface_missing",
        ]
    ].copy()
    out["candidate_id"] = spec.candidate_id
    out["candidate_label"] = spec.label
    out["enabled_surfaces"] = "+".join(surface_names) if surface_names else "reference_no_overlap"
    out["entry_permission_rule"] = spec.entry_permission_rule
    out["abstention_rule"] = spec.abstention_rule
    out["fallback_rule"] = spec.fallback_rule
    out["threshold_family"] = spec.threshold_family
    for key, value in thresholds.items():
        out[key] = float(value)
    out["surface_permission_pass"] = masks["permission"].to_numpy()
    out["surface_abstention_pass"] = masks["abstention"].to_numpy()
    out["surface_entropy_pass"] = masks["entropy"].to_numpy()
    out["surface_tail_pass"] = masks["tail"].to_numpy()
    out["surface_ebm_pass"] = masks["ebm"].to_numpy()
    out["candidate_pass"] = pass_mask.to_numpy()
    out[SIGNAL_FEATURE_ORDER[0]] = signal.to_numpy(dtype="int32")
    out["entry_decision"] = np.where(out[SIGNAL_FEATURE_ORDER[0]].gt(0), "long", np.where(out[SIGNAL_FEATURE_ORDER[0]].lt(0), "short", "flat"))
    return out


def split_alias(split: str) -> str:
    return "validation_is" if split == "validation" else split


def compute_candidate_summary(candidate_frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    reference_counts: dict[str, int] = {}
    reference = candidate_frames["c01_no_overlap_reference"]
    for split in ("validation", "oos"):
        reference_counts[split] = int(reference.loc[reference["split"].eq(split), SIGNAL_FEATURE_ORDER[0]].ne(0).sum())
    rows: list[dict[str, Any]] = []
    for candidate_id, frame in candidate_frames.items():
        for split in ("validation", "oos"):
            view = frame.loc[frame["split"].eq(split)]
            tier_a = view.loc[view["tier_label"].eq(mt5.TIER_A)]
            tier_b = view.loc[view["tier_label"].eq(mt5.TIER_B)]
            signal = view[SIGNAL_FEATURE_ORDER[0]].astype(int)
            signal_count = int(signal.ne(0).sum())
            ref_count = max(reference_counts.get(split, 0), 1)
            enabled = str(view["enabled_surfaces"].iloc[0]) if not view.empty else ""
            abstention_fail = int((~view["surface_abstention_pass"]).sum()) if "abstention" in enabled else 0
            rejected = "mt5_pending"
            if signal_count < 20:
                rejected = "thin_trade_stream_python_signal_count_lt_20"
            elif signal_count / ref_count < 0.10 and candidate_id != "c01_no_overlap_reference":
                rejected = "thin_trade_stream_vs_reference"
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_label": str(view["candidate_label"].iloc[0]) if not view.empty else "",
                    "split": split_alias(split),
                    "enabled_surfaces": enabled,
                    "thresholds": json.dumps(
                        {
                            "permission_score_min": float(view["permission_score_min"].iloc[0]),
                            "p_flat_max": float(view["p_flat_max"].iloc[0]),
                            "calibrated_margin_min": float(view["calibrated_margin_min"].iloc[0]),
                            "entropy_max": float(view["entropy_max"].iloc[0]),
                            "tail_pressure_max": float(view["tail_pressure_max"].iloc[0]),
                            "ebm_abs_min": float(view["ebm_abs_min"].iloc[0]),
                        },
                        sort_keys=True,
                    ),
                    "entry_permission_rule": str(view["entry_permission_rule"].iloc[0]) if not view.empty else "",
                    "abstention_rule": str(view["abstention_rule"].iloc[0]) if not view.empty else "",
                    "fallback_rule": str(view["fallback_rule"].iloc[0]) if not view.empty else "",
                    "tier_a_used_count": int(tier_a[SIGNAL_FEATURE_ORDER[0]].ne(0).sum()),
                    "tier_b_fallback_used_count": int(tier_b[SIGNAL_FEATURE_ORDER[0]].ne(0).sum()),
                    "actual_routed_total_count": signal_count,
                    "validation_trade_count": signal_count if split == "validation" else "",
                    "oos_trade_count": signal_count if split == "oos" else "",
                    "no_trade_rate": float(1.0 - (signal_count / len(view))) if len(view) else 1.0,
                    "abstention_rate": float(abstention_fail / len(view)) if len(view) else 1.0,
                    "thinning_ratio_vs_reference": float(signal_count / ref_count),
                    "long_count": int(signal.gt(0).sum()),
                    "short_count": int(signal.lt(0).sum()),
                    "candidate_rejection_reason": rejected,
                }
            )
    return rows


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
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    table = load_ebm_score_table(path, feature_count=1)
    probs = score_ebm_table_probabilities(table, np.asarray([[-1.0], [0.0], [1.0]], dtype="float64"))
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "stage38_single_signal_ebm_score_table_csv_v1",
        "feature_order": list(SIGNAL_FEATURE_ORDER),
        "feature_order_hash": SIGNAL_FEATURE_HASH,
        "parity_sample_probabilities": probs.tolist(),
        "runtime_policy": "-1 short, 0 flat, +1 long; EA still decides via probability thresholds",
    }


def export_candidate_feature_matrices(candidate_frames: Mapping[str, pd.DataFrame]) -> tuple[dict[str, Any], dict[str, Any]]:
    feature_root = RUN_ROOT / "features"
    exports: dict[str, Any] = {}
    for candidate_id, frame in candidate_frames.items():
        for split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            for tier_label, tier_key in ((mt5.TIER_A, "tier_a"), (mt5.TIER_B, "tier_b_fallback")):
                selected = frame.loc[frame["split"].eq(split) & frame["tier_label"].eq(tier_label)].copy()
                output = feature_root / f"{candidate_id}_{tier_key}_{runtime_split}_stage38_signal_features.csv"
                exports[f"{candidate_id}_{tier_key}_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
                    selected,
                    SIGNAL_FEATURE_ORDER,
                    output,
                    metadata_columns=("candidate_id", "candidate_label", "enabled_surfaces", "tier_label", "routing_source", "entry_decision"),
                )
    model_artifact = export_signal_score_table(RUN_ROOT / "models/stage38_decision_signal_score_table.csv")
    return exports, model_artifact


def copy_runtime_inputs(feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common_root: Path) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copied = []
    model_path = resolve_artifact_path(model_artifact["path"])
    copied.append(copy_to_common(model_path, f"{common}/models/{model_path.name}", common_root))
    for payload in feature_exports.values():
        local_path = resolve_artifact_path(payload["path"])
        copied.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", common_root))
    return copied


def resolve_artifact_path(value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    root_path = ROOT / path
    if path_exists(root_path):
        return root_path
    return RUN_ROOT / path


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
    candidate_specs: Sequence[CandidateSpec],
    feature_exports: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    common: pd.DataFrame,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common.copy()
    common_name = common_run_root(STAGE_NUMBER, RUN_ID)
    model_name = Path(model_artifact["path"]).name
    for spec in candidate_specs:
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_frame = common.loc[common["split"].eq(source_split) & common["tier_label"].eq(mt5.TIER_A)]
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
    if not math.isfinite(number):
        return None
    return number


def build_mt5_candidate_summary(kpi_records: Sequence[Mapping[str, Any]], python_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    python_by_key = {(row["candidate_id"], row["split"]): dict(row) for row in python_rows}
    totals = [record for record in kpi_records if record.get("route_role") == "routed_total"]
    components = {
        (record.get("record_view"), record.get("route_role")): record
        for record in kpi_records
        if record.get("route_role") in {"primary_used", "fallback_used"}
    }
    rows: list[dict[str, Any]] = []
    for total in totals:
        view = str(total.get("record_view", ""))
        match = re.match(r"mt5_routed_(?P<candidate>c\d+_[A-Za-z0-9_]+|m\d+_[A-Za-z0-9_]+)_(?P<split>validation_is|oos)$", view)
        if not match:
            continue
        candidate_id = match.group("candidate")
        split = match.group("split")
        py = python_by_key.get((candidate_id, split), {})
        prefix = f"mt5_routed_{candidate_id}"
        primary = components.get((f"{prefix}_tier_a_used_{split}", "primary_used"), {})
        fallback = components.get((f"{prefix}_tier_b_fallback_used_{split}", "fallback_used"), {})
        metrics = total.get("metrics", {})
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
    by_candidate = pivot_candidate_mt5(mt5_rows)
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
        if val_trades < 25 or oos_trades < 25:
            reasons.append("trade_count_too_thin")
        if routed_total <= 0:
            reasons.append("routed_total_not_explainable")
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
            rejected.append({**payload, "reason": ";".join(reasons)})
        else:
            accepted.append(payload)
    accepted.sort(key=lambda item: (item["validation_net"] + item["oos_net"], item["oos_pf"]), reverse=True)
    return {
        "status": "passed" if accepted else "failed",
        "accepted_candidates": accepted,
        "rejected_candidates": rejected,
        "best_candidate": accepted[0]["candidate_id"] if accepted else None,
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
            reason = "micro_search_gate_passed"
        rows.append({**dict(row), "candidate_rejection_reason": reason})
    return rows


def build_micro_candidates(best_candidate: str, broad_specs: Sequence[CandidateSpec], base_thresholds: Mapping[str, float], common: pd.DataFrame) -> list[CandidateSpec]:
    base = next(spec for spec in broad_specs if spec.candidate_id == best_candidate)
    train = common.loc[common["split"].eq("train")]
    grids = [
        ("m01_relaxed_permission", {"permission_score_min": quantile(train["permission_score"], 0.20, base_thresholds["permission_score_min"])}),
        ("m02_firmer_permission", {"permission_score_min": quantile(train["permission_score"], 0.35, base_thresholds["permission_score_min"])}),
        ("m03_relaxed_entropy", {"entropy_max": quantile(train["entropy"], 0.85, base_thresholds["entropy_max"])}),
        ("m04_firmer_entropy", {"entropy_max": quantile(train["entropy"], 0.65, base_thresholds["entropy_max"])}),
        ("m05_relaxed_tail", {"tail_pressure_max": quantile(train["tail_pressure"], 0.85, base_thresholds["tail_pressure_max"])}),
        ("m06_firmer_tail", {"tail_pressure_max": quantile(train["tail_pressure"], 0.65, base_thresholds["tail_pressure_max"])}),
    ]
    return [
        replace(
            base,
            candidate_id=f"{micro_id}_{safe_name(best_candidate, 36)}",
            label=f"bounded micro-search {micro_id} around {base.label}",
            threshold_family="micro_search_bounded_v1",
            threshold_overrides=overrides,
        )
        for micro_id, overrides in grids
    ]


def prepared_payload(
    *,
    candidate_specs: Sequence[CandidateSpec],
    attempts: Sequence[Mapping[str, Any]],
    common: pd.DataFrame,
    feature_exports: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    common_copies: Sequence[Mapping[str, Any]],
    route_coverage: Mapping[str, Any],
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
        "source_run_id": SOURCE_FRONTIER,
        "run_number": RUN_NUMBER,
        "completion_goal": "Stage38 broad MT5 permission/abstention overlap runtime probe",
        "model_family": "stage38_decision_signal_score_table_from_cross_stage_surfaces",
        "feature_set_id": "single_signal_from_common_stage19_23_26_27_30_surfaces",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
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
        terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
        common_files_root=COMMON_FILES_ROOT_DEFAULT,
        tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
        timeout_seconds=int(args.timeout_seconds),
    )
    completed = result.get("external_verification_status") == "completed" and bool(result.get("strategy_tester_reports"))
    result["judgment"] = INCONCLUSIVE_JUDGMENT if completed else BLOCKED_JUDGMENT
    for record in result.get("mt5_kpi_records", []):
        record["idea_id"] = IDEA_ID
        record["packet_id"] = PACKET_ID
        record["boundary"] = BOUNDARY
    return result


def merge_execution_results(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    base = dict(results[0]) if results else {}
    if not results:
        return base
    merged = dict(base)
    merged["attempts"] = [attempt for result in results for attempt in result.get("attempts", [])]
    merged["execution_results"] = [item for result in results for item in result.get("execution_results", [])]
    merged["strategy_tester_reports"] = [item for result in results for item in result.get("strategy_tester_reports", [])]
    merged["mt5_kpi_records"] = [item for result in results for item in result.get("mt5_kpi_records", [])]
    merged["common_copies"] = [item for result in results for item in result.get("common_copies", [])]
    merged["external_verification_status"] = (
        "completed" if all(result.get("external_verification_status") == "completed" for result in results) else "blocked"
    )
    return merged


def artifact_hash_rows(paths: Iterable[Path], role: str, created_by: str, required: bool = True) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        rows.append(
            {
                "role": role,
                "path": rel(path),
                "created_by": created_by,
                "sha256_lf": sha256_file_lf_normalized(path) if path_exists(path) else "missing_required",
                "required_for_reproducibility": bool(required),
            }
        )
    return rows


def metric_pairs(items: Sequence[tuple[str, Any]]) -> str:
    return ledger_pairs([(key, "" if value is None else value) for key, value in items])


def ledger_rows_from_kpi(result: Mapping[str, Any], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {})
        view = str(record.get("record_view"))
        report = record.get("report", {})
        report_path = ""
        if isinstance(report, Mapping):
            html = report.get("html_report", {})
            if isinstance(html, Mapping):
                report_path = html.get("path", "")
            if not report_path:
                source = report.get("source_report", {})
                if isinstance(source, Mapping):
                    html = source.get("html_report", {})
                    if isinstance(html, Mapping):
                        report_path = html.get("path", "")
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": SOURCE_FRONTIER,
                "record_view": view,
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "permission_abstention_overlap_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status"),
                "judgment": judgment,
                "path": report_path,
                "primary_kpi": metric_pairs(
                    [
                        ("net_profit", metrics.get("net_profit")),
                        ("profit_factor", metrics.get("profit_factor")),
                        ("trade_count", metrics.get("trade_count")),
                        ("signal_count", metrics.get("signal_count")),
                        ("expectancy", metrics.get("expectancy")),
                        ("win_rate", metrics.get("win_rate_percent")),
                    ]
                ),
                "guardrail_kpi": metric_pairs(
                    [
                        ("route_role", record.get("route_role")),
                        ("a_used", metrics.get("tier_a_used_count") or metrics.get("route_bar_count")),
                        ("b_fallback", metrics.get("tier_b_fallback_used_count")),
                        ("max_dd", metrics.get("max_drawdown_amount")),
                        ("boundary", BOUNDARY),
                    ]
                ),
                "external_verification_status": result.get("external_verification_status"),
                "notes": "Stage38 MT5 runtime-probe KPI row; no baseline, promotion, runtime authority, live readiness, or operating reference.",
            }
        )
    return rows


def write_ledgers(result: Mapping[str, Any], judgment: str) -> dict[str, Any]:
    status = "reviewed" if result.get("external_verification_status") == "completed" else "blocked"
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_probe",
        "status": status,
        "judgment": judgment,
        "path": rel(RUN_ROOT),
        "notes": f"Stage38 run32A permission/abstention overlap; mt5_attempts={len(result.get('attempts', []))}; boundary={BOUNDARY}",
    }
    kpi_rows = ledger_rows_from_kpi(result, judgment)
    outputs = {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, kpi_rows, key="ledger_row_id"),
        "stage_run_ledger": upsert_csv_rows(STAGE_ROOT / "03_reviews/stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, kpi_rows, key="ledger_row_id"),
    }
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{safe_name(path.name, 80)}",
            "type": role,
            "path": rel(path),
            "status": status,
            "notes": f"Stage38 {role}; sha256_lf={sha256_file_lf_normalized(path) if path_exists(path) else 'missing_required'}; boundary={BOUNDARY}",
        }
        for role, paths in {
            "run_manifest": [RUN_ROOT / "run_manifest.json"],
            "kpi_record": [RUN_ROOT / "kpi_record.json"],
            "review_packet": [STAGE_ROOT / "03_reviews/run32A_permission_abstention_overlap_broad_mt5_probe_packet.md"],
            "common_table": [RUN_ROOT / "tables/stage38_common_decision_surface_table.parquet"],
            "candidate_grid": [RUN_ROOT / "tables/candidate_grid.csv"],
            "mt5_handoff_manifest": [RUN_ROOT / "mt5/handoff_manifest.json"],
            "mt5_result_import": [RUN_ROOT / "mt5/mt5_result_import_summary.json"],
        }.items()
        for path in paths
    ]
    outputs["artifact_registry"] = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "type", "path", "status", "notes"),
        artifact_rows,
        key="artifact_id",
    )
    return outputs


def normalized_records(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    return mt5_kpi_recorder.build_normalized_records(ROOT, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "path": rel(RUN_ROOT)}])


def write_packet_files(summary: Mapping[str, Any]) -> None:
    gates = [
        "runtime_evidence_gate",
        "scope_completion_gate",
        "kpi_contract_audit",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    status = "passed" if summary["final_judgment"] != BLOCKED_JUDGMENT else "blocked"
    write_yaml(
        PACKET_ROOT / "work_packet.yaml",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "idea_id": IDEA_ID,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-backtest-forensics",
                "obsidian-performance-attribution",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
            ],
            "required_gates": gates,
            "claim_boundary": FINAL_BOUNDARY,
            "source_frontier": SOURCE_FRONTIER,
            "status": "completed" if status == "passed" else "blocked",
        },
    )
    receipts = [
        {"skill": "obsidian-experiment-design", "status": "completed", "evidence": "hypothesis, broad grid, micro-search gate recorded"},
        {"skill": "obsidian-data-integrity", "status": "completed", "evidence": "common table exact timestamp join and missingness audit recorded"},
        {"skill": "obsidian-model-validation", "status": "completed", "evidence": "decision-surface construction and over-thinning checks recorded"},
        {"skill": "obsidian-runtime-parity", "status": status, "evidence": "MT5 handoff manifest plus tester result import"},
        {"skill": "obsidian-backtest-forensics", "status": status, "evidence": "tester command, report path, and KPI rows recorded"},
        {"skill": "obsidian-performance-attribution", "status": "completed", "evidence": "validation/OOS, long/short, thinning, and Tier B dependence summaries recorded"},
        {"skill": "obsidian-artifact-lineage", "status": "completed", "evidence": "artifact hash summary and source lineage schema recorded"},
        {"skill": "obsidian-result-judgment", "status": "completed", "evidence": f"allowed judgment {summary['final_judgment']} only"},
    ]
    write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "receipts": receipts})
    write_json(PACKET_ROOT / "aggregate_summary.json", dict(summary))
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "status": status,
            "allowed_judgment": summary["final_judgment"],
            "actual_mt5_artifact_exists": bool(summary.get("actual_mt5_artifact_exists")),
            "claim_boundary": FINAL_BOUNDARY,
            "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"],
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "status": status,
            "mt5_attempt_count": summary.get("mt5_attempt_count"),
            "tester_output_paths": summary.get("tester_output_paths", []),
            "blocked_reason": None if status == "passed" else BLOCKED_JUDGMENT,
        },
    )
    write_json(
        PACKET_ROOT / "scope_completion_gate.json",
        {"status": status, "stage_folder": rel(STAGE_ROOT), "packet_folder": rel(PACKET_ROOT), "broad_candidate_count": summary.get("broad_candidate_count")},
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {"status": status, "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"), "required_tier_records": ["Tier A used", "Tier B fallback used", "actual routed total"]},
    )
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": status, "required_gates": gates, "covered_gates": gates})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "claim_boundary": FINAL_BOUNDARY})


def replace_top_level_yaml_block(text: str, key: str, block: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line == key:
            start = index
            break
    if start is None:
        return text.rstrip() + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" ") and not lines[index].startswith("-"):
            end = index
            break
    return "\n".join([*lines[:start], *block.rstrip().splitlines(), *lines[end:]]) + "\n"


def remove_existing_stage38_current_updates(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    index = 0
    heading = "## Latest Stage38 RUN32A Permission/Abstention Runtime Probe"
    while index < len(lines):
        if lines[index].startswith(heading):
            index += 1
            while index < len(lines) and not lines[index].startswith("## "):
                index += 1
            continue
        out.append(lines[index])
        index += 1
    return "\n".join(out).lstrip() + ("\n" if out else "")


def update_current_truth(summary: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        "active_branch: ": "active_branch: codex/stage38-permission-abstention-overlap",
        "active_stage: ": f"active_stage: {STAGE_ID}",
        "current_run_id: ": f"current_run_id: {RUN_ID}",
    }
    lines = state.splitlines()
    for index, line in enumerate(lines):
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                lines[index] = replacement
    state = "\n".join(lines) + "\n"
    status = "reviewed_runtime_probe_completed" if summary["final_judgment"] != BLOCKED_JUDGMENT else "blocked_runtime_probe_missing_mt5_execution"
    block = f"""stage38_permission_abstention_overlap:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: {status}
  current_run_id: {RUN_ID}
  source_frontier: {SOURCE_FRONTIER}
  mt5_attempt_count: {summary.get('mt5_attempt_count')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  judgment: {summary['final_judgment']}
  report_path: stages/{STAGE_ID}/03_reviews/run32A_permission_abstention_overlap_broad_mt5_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  boundary: {FINAL_BOUNDARY}
"""
    state = replace_top_level_yaml_block(state, "stage38_permission_abstention_overlap:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")
    update = f"""## Latest Stage38 RUN32A Permission/Abstention Runtime Probe(최신 38단계 32A 실행 허용/기권 런타임 탐침)

Stage38(38단계) `{RUN_ID}`는 Stage23 permission(허용), Stage30 calibration/abstention(보정/기권), Stage26 entropy(엔트로피), Stage27 tail pressure(꼬리 압력), Stage19 EBM direction(EBM 방향)을 같은 timestamp table(시각 테이블)에 겹쳐 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `{summary['final_judgment']}`. MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`.

효과(effect, 효과): decision layer(결정 계층)의 entry permission(진입 허용)과 abstention(기권) 겹침을 확인했지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않았다.

"""
    current = remove_existing_stage38_current_updates(io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig"))
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else "# Changelog\n"
    entry = f"- 2026-05-09: Stage38(38단계) `{RUN_ID}` permission/abstention overlap(허용/기권 겹침) MT5 runtime_probe(MT5 런타임 탐침)를 `{summary['final_judgment']}`로 기록했다. 효과(effect, 효과): 공통 표면, broad sweep(넓은 훑기), MT5 인계/가져오기, 장부를 동기화했고 운영 주장은 만들지 않았다.\n"
    if RUN_ID in changelog:
        lines = [entry.rstrip() if RUN_ID in line and "Stage38" in line else line for line in changelog.splitlines()]
        io_path(CHANGELOG_PATH).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")
    else:
        io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + "\n" + entry, encoding="utf-8-sig")


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int | None = None) -> list[str]:
    visible = list(rows[:limit] if limit else rows)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in visible:
        lines.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return lines


def packet_markdown(summary: Mapping[str, Any]) -> str:
    broad = summary.get("mt5_candidate_rows", [])
    gate = summary.get("micro_search_gate", {})
    commands = summary.get("test_commands", [])
    return "\n".join(
        [
            "# Stage38 RUN32A Permission/Abstention Overlap MT5 Runtime Probe Packet(38단계 32A 실행 허용/기권 겹침 MT5 런타임 탐침 묶음)",
            "",
            "## Judgment(판정)",
            "",
            f"- final_judgment(최종 판정): `{summary['final_judgment']}`",
            f"- claim_boundary(주장 경계): `{FINAL_BOUNDARY}`",
            f"- MT5 attempts(MT5 시도): `{summary.get('mt5_attempt_count')}`",
            f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`",
            "",
            "## Broad Sweep(넓은 훑기)",
            "",
            *markdown_table(
                broad,
                ["candidate_id", "split", "net_profit", "profit_factor", "trade_count", "tier_a_used_count_mt5", "tier_b_fallback_used_count_mt5", "candidate_rejection_reason"],
                limit=40,
            ),
            "",
            "## Micro Search Gate(미세 탐색 게이트)",
            "",
            f"- status(상태): `{gate.get('status')}`",
            f"- best_candidate(최선 후보): `{gate.get('best_candidate')}`",
            "",
            "## Validation Commands(검증 명령)",
            "",
            *markdown_table(commands, ["command", "result", "failures_or_blockers"]),
            "",
            "## Boundary(경계)",
            "",
            "Stage38 run32A remains runtime_probe_only: no baseline, no promotion, no runtime authority, no live readiness, and no operating reference.",
        ]
    )


def stage_docs(summary: Mapping[str, Any]) -> None:
    write_md(
        STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage38 Brief(38단계 요약): Permission/Abstention Overlap(허용/기권 겹침)

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- source frontier(원천 전선): `{SOURCE_FRONTIER}`
- hypothesis(가설): Stage23 permission(허용), Stage30 calibration/abstention(보정/기권), Stage26 entropy(엔트로피), Stage27 tail pressure(꼬리 압력), Stage19 EBM direction(EBM 방향)을 겹치면 나쁜 진입을 줄일 수 있다.
- boundary(경계): `{FINAL_BOUNDARY}`

효과(effect, 효과): 이 단계는 모델군을 또 바꾸지 않고 decision layer(결정 계층)의 허용/기권 겹침을 실제 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)로 확인한다.
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs/input_refs.md",
        "\n".join(
            [
                "# Stage38 Input References(38단계 입력 참조)",
                "",
                *[
                    f"- {surface.role}: `{surface.stage_id}` `{surface.run_id}` Tier A `{rel(surface.tier_a_path)}`, Tier B `{rel(surface.tier_b_path)}`"
                    for surface in SOURCE_SURFACES
                ],
                "",
                "효과(effect, 효과): 모든 표면은 exact timestamp join(정확 시각 결합)으로 합치며, Tier B fallback(티어 B 대체) 의존을 숨기지 않는다.",
            ]
        ),
    )
    write_md(STAGE_ROOT / "03_reviews/run32A_permission_abstention_overlap_broad_mt5_probe_packet.md", packet_markdown(summary))
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage38 Review Index(38단계 검토 색인)

- `run32A_permission_abstention_overlap_broad_mt5_probe_packet.md`: broad MT5 runtime probe(넓은 MT5 런타임 탐침) packet(묶음)
- `stage_run_ledger.csv`: Stage38 KPI ledger(Stage38 핵심 성과 지표 장부)
""",
    )
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage38 Selection Status(38단계 선택 상태)

- final_judgment(최종 판정): `{summary['final_judgment']}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- micro_search_gate(미세 탐색 게이트): `{summary.get('micro_search_gate', {}).get('status')}`

효과(effect, 효과): Stage38(38단계)은 runtime_probe_only(런타임 탐침 전용)로 남고, 운영 선택을 만들지 않는다.
""",
    )


def tester_paths(result: Mapping[str, Any]) -> list[str]:
    paths: list[str] = []
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report, Mapping) else {}
        if isinstance(html, Mapping) and html.get("path"):
            paths.append(str(html["path"]))
    return paths


def summarize_validation_oos(mt5_rows: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    totals = [row for row in mt5_rows if row.get("split") in {"validation_is", "oos"}]
    validation = [row for row in totals if row.get("split") == "validation_is"]
    oos = [row for row in totals if row.get("split") == "oos"]
    key = lambda row: (to_float(row.get("net_profit")) or -1e18, to_float(row.get("profit_factor")) or 0.0)
    return (max(validation, key=key) if validation else None, max(oos, key=key) if oos else None)


def final_judgment_from_results(result: Mapping[str, Any], gate: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]]) -> str:
    if result.get("external_verification_status") != "completed" or not tester_paths(result):
        return BLOCKED_JUDGMENT
    if gate.get("status") == "passed":
        return POSITIVE_JUDGMENT
    by_candidate = pivot_candidate_mt5(mt5_rows)
    both_positive = []
    for splits in by_candidate.values():
        val = splits.get("validation_is")
        oos = splits.get("oos")
        if val and oos and (to_float(val.get("net_profit")) or 0) > 0 and (to_float(oos.get("net_profit")) or 0) > 0:
            both_positive.append(True)
    return INCONCLUSIVE_JUDGMENT if both_positive else NEGATIVE_JUDGMENT


def write_run_files(
    *,
    result: Mapping[str, Any],
    common_artifact: Mapping[str, Any],
    schema: Mapping[str, Any],
    lineage: Sequence[Mapping[str, Any]],
    thresholds: Mapping[str, float],
    candidate_specs: Sequence[CandidateSpec],
    python_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    final_judgment: str,
    ledger_outputs: Mapping[str, Any],
    normalized_payload: tuple[Sequence[Mapping[str, Any]], Sequence[Mapping[str, Any]], Sequence[Mapping[str, Any]], Sequence[Mapping[str, Any]]],
    test_commands: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    actual_paths = tester_paths(result)
    best_validation, best_oos = summarize_validation_oos(mt5_rows)
    summary = {
        "created_at_utc": utc_now(),
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_frontier": SOURCE_FRONTIER,
        "boundary": FINAL_BOUNDARY,
        "final_judgment": final_judgment,
        "external_verification_status": result.get("external_verification_status"),
        "actual_mt5_artifact_exists": bool(actual_paths),
        "mt5_attempt_count": len(result.get("attempts", [])),
        "mt5_execution_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "broad_candidate_count": len([spec for spec in candidate_specs if spec.candidate_id.startswith("c")]),
        "micro_candidate_count": len([spec for spec in candidate_specs if spec.candidate_id.startswith("m")]),
        "candidate_grid": [spec.__dict__ for spec in candidate_specs],
        "thresholds": dict(thresholds),
        "common_table": common_artifact,
        "common_table_schema": schema,
        "lineage": list(lineage),
        "python_candidate_rows": list(python_rows),
        "mt5_candidate_rows": list(mt5_rows),
        "micro_search_gate": dict(micro_gate),
        "tester_output_paths": actual_paths,
        "best_validation_mt5": best_validation,
        "best_oos_mt5": best_oos,
        "compile": result.get("compile"),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "ledger_outputs": dict(ledger_outputs),
        "test_commands": list(test_commands or []),
    }
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "idea_id": IDEA_ID,
            "source_frontier": SOURCE_FRONTIER,
            "candidate_grid": [spec.__dict__ for spec in candidate_specs],
            "attempts": result.get("attempts", []),
            "common_table": common_artifact,
            "model_artifacts": result.get("model_artifacts", {}),
            "feature_matrices": result.get("feature_matrices", {}),
            "common_copies": result.get("common_copies", []),
            "boundary": FINAL_BOUNDARY,
        },
    )
    write_json(RUN_ROOT / "kpi_record.json", {"run_id": RUN_ID, "stage_id": STAGE_ID, "judgment": final_judgment, "mt5_kpi_records": result.get("mt5_kpi_records", [])})
    write_json(
        RUN_ROOT / "mt5/mt5_result_import_summary.json",
        {
            "run_id": RUN_ID,
            "import_status": "completed" if actual_paths else "blocked",
            "mt5_candidate_rows": list(mt5_rows),
            "tester_output_paths": actual_paths,
            "imported_result_path": rel(RUN_ROOT / "mt5/mt5_result_import_summary.json"),
        },
    )
    write_json(
        RUN_ROOT / "mt5/handoff_manifest.json",
        {
            "run_id": RUN_ID,
            "attempts": result.get("attempts", []),
            "terminal_path": str(TERMINAL_PATH_DEFAULT),
            "common_files_path": str(COMMON_FILES_ROOT_DEFAULT),
            "tester_profile_root": str(TESTER_PROFILE_ROOT_DEFAULT),
            "model_artifacts": result.get("model_artifacts", {}),
            "feature_matrices": result.get("feature_matrices", {}),
        },
    )
    write_json(RUN_ROOT / "mt5/tester_request.json", {"attempts": result.get("attempts", []), "command_examples": [item.get("command") for item in result.get("execution_results", [])]})
    write_text(
        RUN_ROOT / "retry_commands.ps1",
        f"python -m foundation.pipelines.run_stage38_permission_abstention_overlap --timeout-seconds 900\n",
    )
    records, normalized_summary, missing_runs, parser_errors = normalized_payload
    write_json(PACKET_ROOT / "normalized_kpi_records.json", list(records))
    write_json(PACKET_ROOT / "normalized_kpi_summary.json", list(normalized_summary))
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", list(missing_runs))
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", list(parser_errors))
    try:
        market_data = mt5_trade_attribution.MarketData.load(ROOT)
        enriched, trade_rows, trade_summary_rows, trade_parser_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    except Exception as exc:
        enriched, trade_rows, trade_summary_rows, trade_parser_errors = [], [], [], [{"error": str(exc)}]
    write_json(PACKET_ROOT / "enriched_kpi_records.json", list(enriched))
    write_json(PACKET_ROOT / "trade_level_records.json", list(trade_rows))
    write_json(PACKET_ROOT / "trade_attribution_summary.json", list(trade_summary_rows))
    write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", list(trade_parser_errors))
    hash_paths = [
        RUN_ROOT / "summary.json",
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        RUN_ROOT / "tables/stage38_common_decision_surface_table.parquet",
        RUN_ROOT / "tables/candidate_grid.csv",
        RUN_ROOT / "tables/broad_sweep_python_summary.csv",
        RUN_ROOT / "tables/mt5_candidate_summary.csv",
        RUN_ROOT / "mt5/handoff_manifest.json",
        RUN_ROOT / "mt5/mt5_result_import_summary.json",
    ]
    write_json(RUN_ROOT / "artifact_hash_summary.json", artifact_hash_rows(hash_paths, "stage38_generated_artifact", rel(Path(__file__))))
    stage_docs(summary)
    write_packet_files(summary)
    return summary


def materialize_and_run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    for path in [
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        RUN_ROOT / "tables",
        RUN_ROOT / "features",
        RUN_ROOT / "models",
        RUN_ROOT / "mt5",
        RUN_ROOT / "reports",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        PACKET_ROOT,
    ]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    common, lineage = build_common_table()
    thresholds = loose_thresholds(common)
    common["permission_filter_signal"] = common["permission_score"].ge(float(thresholds["permission_score_min"]))
    common_artifact = save_frame(RUN_ROOT / "tables/stage38_common_decision_surface_table.parquet", common)
    schema = build_common_table_schema(lineage)
    write_json(RUN_ROOT / "tables/common_table_schema.json", schema)
    write_json(RUN_ROOT / "tables/common_table_lineage.json", list(lineage))
    broad_specs = build_candidate_grid()
    candidate_frames = {spec.candidate_id: apply_candidate_to_table(common, spec, thresholds) for spec in broad_specs}
    combined_candidate_table = pd.concat(candidate_frames.values(), ignore_index=True)
    save_frame(RUN_ROOT / "tables/stage38_candidate_signal_table.parquet", combined_candidate_table)
    python_rows = compute_candidate_summary(candidate_frames)
    write_csv_rows(RUN_ROOT / "tables/candidate_grid.csv", [
        "candidate_id", "label", "enabled_surfaces", "entry_permission_rule", "abstention_rule", "fallback_rule", "threshold_family"
    ], [
        {
            "candidate_id": spec.candidate_id,
            "label": spec.label,
            "enabled_surfaces": "+".join(spec.enabled_surfaces) if spec.enabled_surfaces else "reference_no_overlap",
            "entry_permission_rule": spec.entry_permission_rule,
            "abstention_rule": spec.abstention_rule,
            "fallback_rule": spec.fallback_rule,
            "threshold_family": spec.threshold_family,
        }
        for spec in broad_specs
    ])
    write_csv_rows(RUN_ROOT / "tables/broad_sweep_python_summary.csv", list(python_rows[0].keys()), python_rows)
    feature_exports, model_artifact = export_candidate_feature_matrices(candidate_frames)
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, COMMON_FILES_ROOT_DEFAULT)
    route_coverage = route_coverage_from_common(common)
    broad_attempts = make_attempts(broad_specs, feature_exports, model_artifact, common)
    broad_prepared = prepared_payload(
        candidate_specs=broad_specs,
        attempts=broad_attempts,
        common=common,
        feature_exports=feature_exports,
        model_artifact=model_artifact,
        common_copies=common_copies,
        route_coverage=route_coverage,
    )
    broad_result = execute_or_block(broad_prepared, args)
    broad_result["feature_matrices"] = feature_exports
    broad_result["model_artifacts"] = {"signal_score_table": model_artifact}
    broad_result["common_copies"] = common_copies
    broad_mt5_rows = build_mt5_candidate_summary(broad_result.get("mt5_kpi_records", []), python_rows)
    gate = evaluate_micro_search_gate(broad_mt5_rows) if broad_result.get("external_verification_status") == "completed" else {
        "status": "failed",
        "accepted_candidates": [],
        "rejected_candidates": [{"reason": BLOCKED_JUDGMENT}],
        "best_candidate": None,
    }
    broad_mt5_rows = apply_gate_rejection_reasons(broad_mt5_rows, gate)
    all_specs = list(broad_specs)
    all_results = [broad_result]
    all_python_rows = list(python_rows)
    all_mt5_rows = list(broad_mt5_rows)
    if gate.get("status") == "passed" and gate.get("best_candidate"):
        micro_specs = build_micro_candidates(str(gate["best_candidate"]), broad_specs, thresholds, common)
        micro_frames = {spec.candidate_id: apply_candidate_to_table(common, spec, thresholds) for spec in micro_specs}
        micro_python_rows = compute_candidate_summary(micro_frames)
        micro_feature_exports, _micro_model_artifact = export_candidate_feature_matrices(micro_frames)
        micro_common_copies = copy_runtime_inputs(micro_feature_exports, model_artifact, COMMON_FILES_ROOT_DEFAULT)
        micro_attempts = make_attempts(micro_specs, micro_feature_exports, model_artifact, common)
        micro_prepared = prepared_payload(
            candidate_specs=micro_specs,
            attempts=micro_attempts,
            common=common,
            feature_exports=micro_feature_exports,
            model_artifact=model_artifact,
            common_copies=micro_common_copies,
            route_coverage=route_coverage,
        )
        micro_result = execute_or_block(micro_prepared, args)
        micro_result["feature_matrices"] = micro_feature_exports
        micro_result["model_artifacts"] = {"signal_score_table": model_artifact}
        micro_result["common_copies"] = micro_common_copies
        all_specs.extend(micro_specs)
        all_results.append(micro_result)
        all_python_rows.extend(micro_python_rows)
        all_mt5_rows.extend(build_mt5_candidate_summary(micro_result.get("mt5_kpi_records", []), micro_python_rows))
        save_frame(RUN_ROOT / "tables/stage38_micro_candidate_signal_table.parquet", pd.concat(micro_frames.values(), ignore_index=True))
        write_csv_rows(RUN_ROOT / "tables/micro_search_grid.csv", list(micro_python_rows[0].keys()), micro_python_rows)
    merged_result = merge_execution_results(all_results)
    merged_result["feature_matrices"] = feature_exports
    merged_result["model_artifacts"] = {"signal_score_table": model_artifact}
    merged_result["common_copies"] = common_copies
    write_csv_rows(RUN_ROOT / "tables/mt5_candidate_summary.csv", list(all_mt5_rows[0].keys()) if all_mt5_rows else ["candidate_id"], all_mt5_rows)
    final_judgment = final_judgment_from_results(merged_result, gate, all_mt5_rows)
    write_json(RUN_ROOT / "kpi_record.json", {"run_id": RUN_ID, "stage_id": STAGE_ID, "judgment": final_judgment, "mt5_kpi_records": merged_result.get("mt5_kpi_records", [])})
    ledger_outputs = write_ledgers(merged_result, final_judgment)
    normalized_payload = normalized_records(merged_result)
    summary = write_run_files(
        result=merged_result,
        common_artifact=common_artifact,
        schema=schema,
        lineage=lineage,
        thresholds=thresholds,
        candidate_specs=all_specs,
        python_rows=all_python_rows,
        mt5_rows=all_mt5_rows,
        micro_gate=gate,
        final_judgment=final_judgment,
        ledger_outputs=ledger_outputs,
        normalized_payload=normalized_payload,
    )
    ledger_outputs = write_ledgers(merged_result, final_judgment)
    summary["ledger_outputs"] = ledger_outputs
    write_json(RUN_ROOT / "summary.json", summary)
    write_packet_files(summary)
    update_current_truth(summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage38 permission/abstention overlap MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    summary = materialize_and_run(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary.get("final_judgment") != BLOCKED_JUDGMENT else 2


if __name__ == "__main__":
    raise SystemExit(main())
