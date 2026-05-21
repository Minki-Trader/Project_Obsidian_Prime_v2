from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    copy_to_common,
)
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import (
    run267BR_anti_overconstraint_cross_period_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267BS"
RUN_ID = "run267BS_stage267_pool_wide_directional_impulse_followup_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
STATUS = "run267BS_pool_wide_directional_impulse_followup_materialized_execution_pending"
JUDGMENT = "pool_wide_directional_impulse_followup_materialized_no_candidate_selection"
NEXT_ACTION = "run267BT_execute_pool_wide_directional_impulse_followup_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_directional_impulse_followup_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_FOLLOWUP_QUEUE_PATH = source_design.FOLLOWUP_QUEUE_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_2024_FEATURE_MANIFEST_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "features.csv"
SOURCE_2024_ATTEMPT_MANIFEST_PATH = STAGE_ROOT / "02_runs" / "run267B" / "historical_2024" / "attempts.csv"

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "directional_impulse_variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
FEATURE_ENGINEERING_DIAGNOSTICS_PATH = RUN_ROOT / "feature_engineering_diagnostics.csv"
ROUTE_GAP_AUDIT_PATH = RUN_ROOT / "route_gap_audit.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ARTIFACT_LINEAGE_RECEIPT_PATH = RUN_ROOT / "artifact_lineage_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BS_pool_wide_directional_impulse_followup_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BS_pool_wide_directional_impulse_followup_materialization.py")

STAGE_LEDGER_PATH = source_design.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_design.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_design.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_design.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_design.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_design.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_design.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_design.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_design.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_design.ARTIFACT_COLUMNS

COMMON_ROOT = "OPV2/s267bs/run267BS_directional_impulse_followup"
PERIOD_LABEL = input_probe.PERIOD_LABEL
EXPLORATION_LABEL = "stage267_BaselineRacing__DirectionalImpulseFollowup"
MATERIALIZATION_BOUNDARY = (
    "Tier_A_2024_cached_stress_materialized; "
    "Tier_B_and_actual_routed_total_blocked_until_true_fallback_manifest_exists"
)
SOURCE_LIMITATION = (
    "2024_cached_compact_rank_gate_context_frame; raw_ATR_return_features_not_available_in_this_materialization"
)

PROFILE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "run267bs_q01_pool_wide_directional_asymmetry": {
        "profile_token": "dir_asym",
        "profile_label": "directional_asymmetry",
        "engineered_features": [
            "stage267bs_short_side_rank_pressure_score",
            "stage267bs_long_side_rank_pressure_score",
        ],
        "model_terms": "side_specific_rank_pressure_main_effects",
        "next_decision_use": "sell_side_fragility_structural_check",
    },
    "run267bs_q02_aggressive_impulse_replacement": {
        "profile_token": "impulse_repl",
        "profile_label": "aggressive_impulse_replacement",
        "engineered_features": ["stage267bs_impulse_replacement_score"],
        "model_terms": "nonflat_impulse_pressure_main_effect",
        "next_decision_use": "aggressive_non_filter_branch_check",
    },
}

CANDIDATE_ORDER = [
    "s264_aih",
    "s264_lc",
    "s262_lih",
    "s264_aia",
    "s258_stc",
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}" if math.isfinite(value) else ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def parse_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line or line.startswith("["):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run267BS_pool_wide_directional_impulse_followup_materialization"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "mt5_tester_ini",
        "tester": dict(values),
    }


def source_feature_order(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    if not header or header[0] != "bar_time_server":
        raise RuntimeError(f"unexpected feature header: {rel(path)}")
    return list(header[1:])


def score_terms_for_feature(profile_label: str, feature_name: str) -> tuple[list[float], list[tuple[float, float, float]]]:
    cuts = [0.2, 0.4, 0.6, 0.8]
    if profile_label == "directional_asymmetry" and "short_side" in feature_name:
        scores = [
            (0.0, 0.0, 0.0),
            (0.01, 0.0, -0.01),
            (0.04, -0.01, -0.03),
            (0.07, -0.03, -0.05),
            (0.1, -0.04, -0.08),
            (0.13, -0.05, -0.1),
        ]
    elif profile_label == "directional_asymmetry" and "long_side" in feature_name:
        scores = [
            (0.0, 0.0, 0.0),
            (-0.01, 0.0, 0.01),
            (-0.03, -0.01, 0.04),
            (-0.05, -0.03, 0.07),
            (-0.08, -0.04, 0.1),
            (-0.1, -0.05, 0.13),
        ]
    else:
        scores = [
            (0.0, 0.0, 0.0),
            (-0.04, 0.08, -0.04),
            (-0.01, 0.02, -0.01),
            (0.03, -0.04, 0.03),
            (0.07, -0.1, 0.07),
            (0.12, -0.16, 0.12),
        ]
    return cuts, scores


def append_model_features(
    source_model_path: Path,
    destination_model_path: Path,
    *,
    source_feature_count: int,
    profile_label: str,
    engineered_features: Sequence[str],
) -> None:
    io_path(destination_model_path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(source_model_path).open("r", encoding="utf-8-sig", newline="") as source_handle:
        rows = list(csv.DictReader(source_handle))
    fieldnames = ["record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long"]
    for offset, feature_name in enumerate(engineered_features):
        feature_index = int(source_feature_count) + offset
        cuts, scores = score_terms_for_feature(profile_label, feature_name)
        for cut_index, cut_value in enumerate(cuts):
            rows.append(
                {
                    "record_type": "cut",
                    "feature_index": str(feature_index),
                    "item_index": str(cut_index),
                    "value": f"{cut_value:.17g}",
                    "score_short": "",
                    "score_flat": "",
                    "score_long": "",
                }
            )
        for item_index, (score_short, score_flat, score_long) in enumerate(scores):
            rows.append(
                {
                    "record_type": "score",
                    "feature_index": str(feature_index),
                    "item_index": str(item_index),
                    "value": "",
                    "score_short": f"{score_short:.17g}",
                    "score_flat": f"{score_flat:.17g}",
                    "score_long": f"{score_long:.17g}",
                }
            )
    with io_path(destination_model_path).open("w", encoding="utf-8", newline="") as destination_handle:
        writer = csv.DictWriter(destination_handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_engineered_frame(
    source_feature_path: Path,
    destination_feature_path: Path,
    *,
    feature_order: Sequence[str],
    rank_column: str,
    gate_column: str,
    profile_label: str,
    engineered_features: Sequence[str],
) -> dict[str, Any]:
    frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    signal = pd.to_numeric(frame["stage56_context_et_event_signal"], errors="coerce").fillna(0.0)
    rank = pd.to_numeric(frame[rank_column], errors="coerce").fillna(0.0)
    gate = pd.to_numeric(frame[gate_column], errors="coerce").fillna(0.0)
    rank_max = max(float(rank.max()), 1.0)
    gate_max = max(float(gate.max()), 1.0)
    rank_norm = (rank / rank_max).clip(0.0, 1.0)
    gate_norm = (gate / gate_max).clip(0.0, 1.0)

    if profile_label == "directional_asymmetry":
        short_signal = (signal < 0).astype(float)
        long_signal = (signal > 0).astype(float)
        frame[engineered_features[0]] = (0.45 * short_signal + 0.3 * rank_norm + 0.25 * gate_norm).clip(0.0, 1.0)
        frame[engineered_features[1]] = (0.45 * long_signal + 0.3 * rank_norm + 0.25 * gate_norm).clip(0.0, 1.0)
    else:
        impulse = signal.abs().clip(0.0, 1.0)
        frame[engineered_features[0]] = (0.4 * impulse + 0.35 * rank_norm + 0.25 * gate_norm).clip(0.0, 1.0)

    runtime_columns = ["bar_time_server", *feature_order, *engineered_features]
    missing = [column for column in runtime_columns if column not in frame.columns]
    if missing:
        raise RuntimeError(f"missing runtime columns after feature engineering: {missing}")
    io_path(destination_feature_path.parent).mkdir(parents=True, exist_ok=True)
    frame.loc[:, runtime_columns].to_csv(io_path(destination_feature_path), index=False, encoding="utf-8", lineterminator="\n")

    diagnostics: dict[str, Any] = {
        "rows": int(len(frame)),
        "source_feature_count": int(len(feature_order)),
        "engineered_feature_count": int(len(engineered_features)),
        "output_feature_count": int(len(runtime_columns) - 1),
        "missing_feature_cells": int(frame.loc[:, runtime_columns[1:]].isna().sum().sum()),
    }
    for feature_name in engineered_features:
        diagnostics[f"{feature_name}_min"] = float(frame[feature_name].min())
        diagnostics[f"{feature_name}_max"] = float(frame[feature_name].max())
        diagnostics[f"{feature_name}_mean"] = float(frame[feature_name].mean())
    return diagnostics


def validate_score_table(feature_path: Path, model_path: Path, feature_order: Sequence[str]) -> dict[str, Any]:
    frame = pd.read_csv(io_path(feature_path), encoding="utf-8-sig")
    values = frame.loc[:, list(feature_order)].head(32).to_numpy(dtype="float64")
    table = load_ebm_score_table(model_path, feature_count=len(feature_order))
    probabilities = score_ebm_table_probabilities(table, values)
    return {
        "score_table_validation": "passed",
        "probability_rows_checked": int(len(probabilities)),
        "probability_columns": int(probabilities.shape[1]) if len(probabilities) else 0,
        "probability_sum_max_abs_error": float(abs(probabilities.sum(axis=1) - 1.0).max()) if len(probabilities) else 0.0,
    }


def source_manifests() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    queue_rows = read_csv(SOURCE_FOLLOWUP_QUEUE_PATH)
    feature_rows = read_csv(SOURCE_2024_FEATURE_MANIFEST_PATH)
    attempt_rows = read_csv(SOURCE_2024_ATTEMPT_MANIFEST_PATH)
    features_by_alias = {row["candidate_alias"]: row for row in feature_rows}
    attempts_by_alias = {
        row["candidate_alias"]: row
        for row in attempt_rows
        if row.get("tier") == "Tier A" and row.get("attempt_name", "").endswith("_ta_2024")
    }
    return queue_rows, features_by_alias, attempts_by_alias


def materialization_plan_rows(
    queue_rows: Sequence[Mapping[str, str]],
    features_by_alias: Mapping[str, Mapping[str, str]],
) -> list[dict[str, Any]]:
    p0_rows = [row for row in queue_rows if row.get("queue_id") in PROFILE_DEFINITIONS]
    rows: list[dict[str, Any]] = []
    order = 0
    for queue in p0_rows:
        profile = PROFILE_DEFINITIONS[str(queue["queue_id"])]
        for alias in CANDIDATE_ORDER:
            source = features_by_alias[alias]
            order += 1
            variant_id = f"run267bs_{order:02d}_{alias}_{profile['profile_token']}"
            attempt_name = f"{variant_id}_ta24"
            rows.append(
                {
                    "plan_id": variant_id,
                    "queue_id": queue["queue_id"],
                    "priority": queue["priority"],
                    "workstream": queue["workstream"],
                    "candidate_id": source["candidate_id"],
                    "candidate_alias": alias,
                    "candidate_role": source["role"],
                    "profile_label": profile["profile_label"],
                    "profile_token": profile["profile_token"],
                    "attempt_name": attempt_name,
                    "source_feature_file": source["feature_file"],
                    "source_model_file": source["model_file"],
                    "source_feature_order": source["feature_order"],
                    "source_feature_order_hash": source["feature_order_hash"],
                    "rank_column": source["rank_column"],
                    "gate_column": source["gate_column"],
                    "source_rows": source["rows"],
                    "engineered_features": profile["engineered_features"],
                    "source_limitation": SOURCE_LIMITATION,
                    "materialization_decision": "materialize_tier_a_2024_execution_inputs",
                    "tier_pair_boundary": MATERIALIZATION_BOUNDARY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def materialize_variant(
    plan: Mapping[str, Any],
    attempts_by_alias: Mapping[str, Mapping[str, str]],
    *,
    order: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    alias = str(plan["candidate_alias"])
    variant_id = str(plan["plan_id"])
    attempt_name = str(plan["attempt_name"])
    profile_label = str(plan["profile_label"])
    engineered_features = [str(item) for item in plan["engineered_features"]]
    source_feature_path = repo_path(str(plan["source_feature_file"]))
    source_model_path = repo_path(str(plan["source_model_file"]))
    source_attempt = attempts_by_alias[alias]
    source_set_path = repo_path(str(source_attempt["set_path"]))
    source_ini_path = repo_path(str(source_attempt["ini_path"]))

    feature_order = source_feature_order(source_feature_path)
    output_feature_order = [*feature_order, *engineered_features]
    feature_order_hash = ordered_hash(output_feature_order)
    variant_dir = VARIANT_ROOT / alias / variant_id
    feature_path = variant_dir / "features" / f"{variant_id}_features.csv"
    model_path = variant_dir / "models" / f"{variant_id}_model.csv"

    diagnostics = build_engineered_frame(
        source_feature_path,
        feature_path,
        feature_order=feature_order,
        rank_column=str(plan["rank_column"]),
        gate_column=str(plan["gate_column"]),
        profile_label=profile_label,
        engineered_features=engineered_features,
    )
    append_model_features(
        source_model_path,
        model_path,
        source_feature_count=len(feature_order),
        profile_label=profile_label,
        engineered_features=engineered_features,
    )
    validation = validate_score_table(feature_path, model_path, output_feature_order)

    common_feature_path = f"{COMMON_ROOT}/{alias}/{variant_id}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{variant_id}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    source_set_values = parse_key_values(source_set_path)
    telemetry = f"{COMMON_ROOT}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{COMMON_ROOT}/telemetry/{attempt_name}_summary.csv"
    model_id = f"{RUN_ID}_{variant_id}_score_table"
    set_values = dict(source_set_values)
    set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": PERIOD_LABEL,
            "InpModelPath": common_model_path,
            "InpModelId": model_id,
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": len(output_feature_order),
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureOrderHash": feature_order_hash,
            "InpFallbackEnabled": "false",
            "InpFallbackFeatureCsvPath": common_feature_path,
            "InpFallbackFeatureCount": len(output_feature_order),
            "InpFallbackModelPath": common_model_path,
            "InpFallbackModelId": model_id,
            "InpFallbackModelBackend": "ebm_table",
            "InpFallbackFeatureOrderHash": feature_order_hash,
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpMagic": 26719000 + int(order),
        }
    )
    set_payload = write_set(MT5_ROOT / f"{attempt_name}.set", set_values)

    source_ini_values = parse_key_values(source_ini_path)
    ini_values = dict(source_ini_values)
    ini_values.update(
        {
            "ExpertParameters": EA_TESTER_SET_NAME,
            "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
        }
    )
    ini_payload = write_ini(MT5_ROOT / f"{attempt_name}.ini", ini_values)

    variant_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "priority": plan["priority"],
        "workstream": plan["workstream"],
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "profile_token": plan["profile_token"],
        "model_materialization_type": "score_table_appended_directional_impulse_main_effects_v1",
        "source_feature_file": rel(source_feature_path),
        "source_feature_sha256": sha256_file_lf_normalized(source_feature_path),
        "runtime_feature_file": rel(feature_path),
        "runtime_feature_sha256": sha256_file_lf_normalized(feature_path),
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": rel(model_path),
        "runtime_model_sha256": sha256_file_lf_normalized(model_path),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "source_feature_count": len(feature_order),
        "engineered_feature_count": len(engineered_features),
        "feature_count": len(output_feature_order),
        "feature_order": output_feature_order,
        "feature_order_hash": feature_order_hash,
        "engineered_features": engineered_features,
        "rank_column": plan["rank_column"],
        "gate_column": plan["gate_column"],
        "runtime_rows": diagnostics["rows"],
        "missing_feature_cells": diagnostics["missing_feature_cells"],
        "source_limitation": SOURCE_LIMITATION,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    attempt_row = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "tier": "Tier A",
        "split": PERIOD_LABEL,
        "attempt_role": "tier_only_total",
        "record_view_prefix": f"mt5_ta_{variant_id}",
        "set_path": set_payload["path"],
        "set_sha256": set_payload["sha256"],
        "ini_path": ini_payload["path"],
        "ini_sha256": ini_payload["sha256"],
        "common_telemetry_path": telemetry,
        "common_summary_path": summary,
        "tier_pair_boundary": MATERIALIZATION_BOUNDARY,
        "execution_status": "execution_pending",
    }
    diagnostics_row = {
        "variant_id": variant_id,
        "candidate_alias": alias,
        "profile_label": profile_label,
        **diagnostics,
        **validation,
        "feature_order_hash": feature_order_hash,
    }
    return variant_row, attempt_row, diagnostics_row


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = str(queue.get("queue_id", ""))
        if queue_id not in PROFILE_DEFINITIONS:
            continue
        rows.append(
            {
                "receipt_id": f"run267bs_{PROFILE_DEFINITIONS[queue_id]['profile_token']}_experiment_design",
                "hypothesis": queue.get("hypothesis"),
                "decision_use": queue.get("decision_use"),
                "comparison_baseline": queue.get("comparison_baseline"),
                "control_variables": queue.get("control_variables"),
                "changed_variables": queue.get("changed_variables"),
                "sample_scope": "Tier A cached 2024 historical stress inputs for all five baseline candidates; Tier B blocked until true fallback manifest exists",
                "success_criteria": queue.get("success_criteria"),
                "failure_criteria": queue.get("failure_criteria"),
                "invalid_conditions": queue.get("invalid_conditions"),
                "stop_conditions": queue.get("stop_conditions"),
                "evidence_plan": queue.get("evidence_plan"),
            }
        )
    return rows


def route_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_view": "Tier A separate",
            "status": "materialized_execution_pending",
            "evidence": rel(ATTEMPT_MANIFEST_PATH),
            "effect": "MT5(MetaTrader 5, 메타트레이더5) 실행에서 2024 cached stress(캐시 2024 압박)를 바로 비교할 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "route_view": "Tier B separate",
            "status": "blocked_true_fallback_manifest_absent",
            "evidence": MATERIALIZATION_BOUNDARY,
            "effect": "Tier B(티어 B)를 합성하지 않아 routed total(라우팅 전체)을 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "route_view": "actual routed total",
            "status": "blocked_true_fallback_manifest_absent",
            "evidence": MATERIALIZATION_BOUNDARY,
            "effect": "actual routed total(실제 라우팅 전체)은 실제 fallback(대체) manifest(목록)가 생기기 전까지 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def result_judgment_rows(variant_count: int, attempt_count: int) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": (
                f"materialization_plan={rel(MATERIALIZATION_PLAN_PATH)}; "
                f"variants={variant_count}; attempts={attempt_count}; "
                f"runtime_contract={rel(RUNTIME_CONTRACT_PATH)}"
            ),
            "evidence_missing": "MT5 execution, KPI, trade records, balance/equity curve, time-slice KPI",
            "judgment_label": "exploratory_materialization_only_no_candidate_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "실행 입력은 준비됐지만 아직 성과 판정은 아니다.",
        }
    ]


def gate_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "experiment_design",
            "status": "covered",
            "evidence": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "effect": "q01/q02 가설, 비교 기준, 성공/실패/무효 조건을 실행 입력 전에 고정했다.",
        },
        {
            "gate_id": "artifact_lineage",
            "status": "covered",
            "evidence": rel(ARTIFACT_LINEAGE_RECEIPT_PATH),
            "effect": "source feature/model(원천 피처/모델)에서 runtime handoff(런타임 인계)까지 hash(해시)를 연결했다.",
        },
        {
            "gate_id": "result_judgment",
            "status": "covered",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "물질화 완료와 후보 선택을 분리했다.",
        },
        {
            "gate_id": "tier_pair_boundary",
            "status": "covered_with_blocked_tier_b_boundary",
            "evidence": rel(ROUTE_GAP_AUDIT_PATH),
            "effect": "Tier A+B(티어 A+B) 합성 결과를 actual routed total(실제 라우팅 전체)로 말하지 않는다.",
        },
    ]


def artifact_lineage_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in variant_rows:
        rows.append(
            {
                "lineage_id": f"lineage_{row['variant_id']}",
                "source_inputs": f"{row['source_feature_file']};{row['source_model_file']}",
                "producer": rel(PRODUCER_PATH),
                "consumer": NEXT_ACTION,
                "artifact_paths": f"{row['runtime_feature_file']};{row['runtime_model_file']}",
                "artifact_hashes": f"feature={row['runtime_feature_sha256']};model={row['runtime_model_sha256']}",
                "registry_links": f"{rel(ARTIFACT_REGISTRY_PATH)};{rel(RUN_REGISTRY_PATH)}",
                "availability": "tracked_and_common_files_handoff",
                "lineage_judgment": "connected_with_boundary",
            }
        )
    return rows


def runtime_contract_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in variant_rows:
        rows.append(
            {
                "variant_id": row["variant_id"],
                "queue_id": row["queue_id"],
                "candidate_id": row["candidate_id"],
                "candidate_alias": row["candidate_alias"],
                "candidate_role": row["candidate_role"],
                "profile_label": row["profile_label"],
                "shared_contract": "score_table_runtime_csv_common_files_handoff",
                "feature_count": row["feature_count"],
                "feature_order_hash": row["feature_order_hash"],
                "model_backend": "ebm_table",
                "model_materialization_type": row["model_materialization_type"],
                "known_difference": SOURCE_LIMITATION,
                "runtime_claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def report_text(result: Mapping[str, Any]) -> str:
    return f"""# Stage267 Run267BS Pool-Wide Directional/Impulse Follow-Up Materialization(267단계 267BS 후보군 전체 방향/임펄스 후속 물질화)

## Summary(요약)

Run267BS(267BS 실행)는 run267BR(267BR 실행)의 P0 queue(P0 대기열) 두 개를 다섯 baseline candidates(기준 후보) 전체의 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.

- variants(변형): `{result['variant_count']}`
- attempts(시도): `{result['attempt_count']}`
- candidates(후보): `5`
- profiles(프로필): `directional_asymmetry(방향 비대칭)`, `aggressive_impulse_replacement(공격형 임펄스 대체)`
- next_action(다음 행동): `{NEXT_ACTION}`

Effect(효과): baseline(기준 후보)을 지금 고르는 대신, 이전 연구에서 나온 sell-side fragility(매도측 취약성)와 2023H2 impulse clue(2023년 하반기 임펄스 단서)를 후보군 전체에서 같은 조건으로 깨뜨려 볼 수 있게 했다.

## Boundary(경계)

이 run(실행)은 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표), trade records(거래 기록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표)는 없다.

selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 `none/not_claimed`이다.

## Inputs(입력)

- source queue(원천 대기열): `{rel(SOURCE_FOLLOWUP_QUEUE_PATH)}`
- source 2024 feature manifest(2024 피처 목록): `{rel(SOURCE_2024_FEATURE_MANIFEST_PATH)}`
- source 2024 attempts(2024 시도 목록): `{rel(SOURCE_2024_ATTEMPT_MANIFEST_PATH)}`

## Outputs(출력)

- variant manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`
- attempt manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`
- runtime contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`
- diagnostics(진단): `{rel(FEATURE_ENGINEERING_DIAGNOSTICS_PATH)}`
- route gap audit(라우팅 공백 감사): `{rel(ROUTE_GAP_AUDIT_PATH)}`

## Tier Boundary(티어 경계)

Tier A(티어 A)는 실행 대기 입력까지 물질화했다. Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 없어서 blocked(차단)로 남긴다.

Effect(효과): duplicate Tier A+B(중복 티어 A+B)를 routed total(라우팅 전체)처럼 말하지 않는다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            break
    return "\n".join(lines) + "\n"


def insert_before_once(text: str, marker: str, block: str, unique_token: str) -> str:
    if unique_token in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n\n" + block.rstrip() + "\n"
    return text.replace(marker, block.rstrip() + "\n\n" + marker, 1)


def update_current_working_state(result: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_WORKING_STATE_PATH)
    text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line(
        text,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `pool_wide_directional_impulse_followup_materialization`",
    )
    text = replace_line(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    text = replace_line(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    text = text.replace(
        "- next_action(다음 행동): `run267BS_materialize_pool_wide_directional_impulse_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    text = text.replace(
        "- next_run(다음 실행): `run267BS_materialize_pool_wide_directional_impulse_followup_queue`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    block = (
        f"- Stage267(267단계) run267BS(267BS 실행) pool-wide directional/impulse follow-up materialization"
        f"(후보군 전체 방향/임펄스 후속 물질화): `{rel(REPORT_PATH)}`\n"
        f"  Effect(효과): run267BR(267BR 실행)의 q01/q02 P0 queue(P0 대기열)를 variants(변형) `{result['variant_count']}`개와 "
        f"MT5(MetaTrader 5, 메타트레이더5) attempts(시도) `{result['attempt_count']}`개로 만들었고, selected candidate(선택 후보), "
        f"selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    text = insert_before_once(text, "## Current Next Action(현재 다음 행동)", block, "run267BS(267BS 실행) pool-wide")
    write_text(CURRENT_WORKING_STATE_PATH, text)


def update_selection_status(result: Mapping[str, Any]) -> None:
    text = read_text(SELECTION_STATUS_PATH)
    text = replace_line(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    text = replace_line(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    text = text.replace(
        "- next_action(다음 행동): `run267BS_materialize_pool_wide_directional_impulse_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    text = text.replace(
        "- next_run(다음 실행): `run267BS_materialize_pool_wide_directional_impulse_followup_queue`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    block = (
        f"- run267BS_pool_wide_directional_impulse_followup_materialization(267BS 후보군 전체 방향/임펄스 후속 물질화): "
        f"`{rel(REPORT_PATH)}`\n"
        f"- run267BS_variant_count(267BS 변형 수): `{result['variant_count']}`\n"
        f"- run267BS_attempt_count(267BS 시도 수): `{result['attempt_count']}`"
    )
    text = insert_before_once(text, "Forbidden claims(금지 주장):", block, "run267BS_pool_wide_directional_impulse_followup_materialization")
    write_text(SELECTION_STATUS_PATH, text)


def update_workspace_state(result: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = replace_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = replace_line(text, "updated_on:", "updated_on: '2026-05-22'")
    focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267BS(267BS 실행) pool-wide directional/impulse follow-up materialization"
        f"(후보군 전체 방향/임펄스 후속 물질화) `{STATUS}`. Effect(효과): run267BR(267BR 실행)의 q01/q02 P0 queue(P0 대기열)를 "
        f"variants(변형) `{result['variant_count']}`개와 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) attempts(시도) "
        f"`{result['attempt_count']}`개로 물질화했고 selected candidate(선택 후보), selected research baseline(선택 연구 기준선), "
        f"ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run267BS(267BS 실행) pool-wide directional/impulse" not in text:
        text = text.replace("current_focus:\n", focus + "\n", 1)
    write_text(WORKSPACE_STATE_PATH, text)


def update_review_index(result: Mapping[str, Any]) -> None:
    text = read_text(REVIEW_INDEX_PATH)
    if "Run267BS(267BS 실행)" in text:
        return
    block = f"""

Run267BS(267BS 실행)는 run267BR(267BR 실행)의 P0 follow-up queue(P0 후속 대기열)를 후보군 전체 direction/impulse materialization(방향/임펄스 물질화)으로 바꿨다.
Effect(효과): variants(변형) `{result['variant_count']}`개와 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) attempts(시도) `{result['attempt_count']}`개를 만들었고, 다음 run267BT(267BT 실행)에서 KPI(핵심 성과 지표)와 curve/time-slice/trade-quality(곡선/시간구간/거래품질)를 볼 수 있다.
Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.
"""
    write_text(REVIEW_INDEX_PATH, text.rstrip() + block)


def upsert_ledgers_and_artifacts(result: Mapping[str, Any]) -> dict[str, Any]:
    now = utc_now()
    stage_row = {
        "row_id": "stage267_run267BS_pool_wide_directional_impulse_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_directional_impulse_followup_materialization",
        "tier_scope": "Tier A materialized; Tier B and actual routed total blocked",
        "scoreboard": "feature_model_set_ini_materialization_no_trading_kpi",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};next_action={NEXT_ACTION}.",
    }
    alpha_row = {
        "ledger_row_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization",
        "tier_scope": "Tier A materialized; Tier B blocked",
        "kpi_scope": "feature_model_set_ini_materialization_no_trading_kpi",
        "scoreboard_lane": "regular_risk_execution_preparation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']}",
        "guardrail_kpi": "no_mt5_kpi_yet;no_candidate_selection;no_onnx",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "Materialized q01/q02 pool-wide Tier A execution inputs only.",
    }
    existing_stage_rows = [
        row
        for row in read_csv(STAGE_LEDGER_PATH)
        if row.get("run_id") != RUN_ID and row.get("row_id") != stage_row["row_id"]
    ]
    write_csv(STAGE_LEDGER_PATH, [*existing_stage_rows, stage_row], STAGE_LEDGER_COLUMNS)
    stage_ledger = {
        "path": rel(STAGE_LEDGER_PATH),
        "sha256": sha256_file_lf_normalized(STAGE_LEDGER_PATH),
        "hash_policy": "lf_normalized_text_register",
        "rows": len(existing_stage_rows) + 1,
        "upserted_rows": 1,
    }
    project_ledger = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    run_registry = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage267_baseline_candidate_racing_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};next={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    artifacts = [
        ("stage267_run267BS_report", "report", REPORT_PATH, "Run267BS user-facing report."),
        ("stage267_run267BS_manifest", "run_manifest_json", RUN_MANIFEST_PATH, "Run267BS run manifest."),
        ("stage267_run267BS_variant_manifest", "variant_manifest_csv", VARIANT_MANIFEST_PATH, "Run267BS variant manifest."),
        ("stage267_run267BS_attempt_manifest", "attempt_manifest_csv", ATTEMPT_MANIFEST_PATH, "Run267BS MT5 attempt manifest."),
        ("stage267_run267BS_runtime_contract", "runtime_contract_csv", RUNTIME_CONTRACT_PATH, "Run267BS runtime contract."),
        ("stage267_run267BS_review_result", "review_result_json", REVIEW_RESULT_PATH, "Run267BS review result."),
        ("stage267_run267BS_producer", "stage_pipeline", PRODUCER_PATH, "Run267BS producer script."),
    ]
    artifact_rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in artifacts:
        path_obj = REPO_ROOT / path if not Path(path).is_absolute() else Path(path)
        artifact_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path_obj),
                "sha256": sha256_file_lf_normalized(path_obj) if path_exists(path_obj) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": notes,
            }
        )
    artifact_registry = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    return {
        "stage_ledger": stage_ledger,
        "project_ledger": project_ledger,
        "run_registry": run_registry,
        "artifact_registry": artifact_registry,
    }


def run() -> dict[str, Any]:
    queue_rows, features_by_alias, attempts_by_alias = source_manifests()
    missing_features = [alias for alias in CANDIDATE_ORDER if alias not in features_by_alias]
    missing_attempts = [alias for alias in CANDIDATE_ORDER if alias not in attempts_by_alias]
    if missing_features or missing_attempts:
        raise RuntimeError(f"missing source manifests: features={missing_features}; attempts={missing_attempts}")

    plan_rows = materialization_plan_rows(queue_rows, features_by_alias)
    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    diagnostics_rows: list[dict[str, Any]] = []
    for order, plan in enumerate(plan_rows, start=1):
        variant_row, attempt_row, diagnostics_row = materialize_variant(plan, attempts_by_alias, order=order)
        variant_rows.append(variant_row)
        attempt_rows.append(attempt_row)
        diagnostics_rows.append(diagnostics_row)

    runtime_contract = runtime_contract_rows(variant_rows)
    experiment_design = experiment_design_rows(queue_rows)
    artifact_lineage = artifact_lineage_rows(variant_rows)
    route_gap = route_gap_rows()
    result_judgment = result_judgment_rows(len(variant_rows), len(attempt_rows))
    gate_audit = gate_audit_rows()

    write_csv(MATERIALIZATION_PLAN_PATH, plan_rows)
    write_csv(VARIANT_MANIFEST_PATH, variant_rows)
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_rows)
    write_csv(RUNTIME_CONTRACT_PATH, runtime_contract)
    write_csv(FEATURE_ENGINEERING_DIAGNOSTICS_PATH, diagnostics_rows)
    write_csv(ROUTE_GAP_AUDIT_PATH, route_gap)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, experiment_design)
    write_csv(ARTIFACT_LINEAGE_RECEIPT_PATH, artifact_lineage)
    write_csv(RESULT_JUDGMENT_PATH, result_judgment)
    write_csv(GATE_AUDIT_PATH, gate_audit)

    result: dict[str, Any] = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "candidate_count": len(CANDIDATE_ORDER),
        "variant_count": len(variant_rows),
        "attempt_count": len(attempt_rows),
        "profile_count": len(PROFILE_DEFINITIONS),
        "source_followup_queue": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
        "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
        "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
        "variant_manifest": rel(VARIANT_MANIFEST_PATH),
        "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "route_gap_audit": rel(ROUTE_GAP_AUDIT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
        "tier_pair_boundary": MATERIALIZATION_BOUNDARY,
        "source_limitation": SOURCE_LIMITATION,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    write_json(RUN_MANIFEST_PATH, result)
    write_json(
        LINEAGE_PATH,
        {
            "source_inputs": {
                "followup_queue": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
                "branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
                "failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
                "historical_2024_features": rel(SOURCE_2024_FEATURE_MANIFEST_PATH),
                "historical_2024_attempts": rel(SOURCE_2024_ATTEMPT_MANIFEST_PATH),
            },
            "producer": rel(PRODUCER_PATH),
            "outputs": {
                "variant_manifest": rel(VARIANT_MANIFEST_PATH),
                "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
                "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
                "report": rel(REPORT_PATH),
            },
            "lineage_judgment": "connected_with_boundary",
            "boundary": MATERIALIZATION_BOUNDARY,
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_text(result))

    registry_payload = upsert_ledgers_and_artifacts(result)
    result["registry_updates"] = registry_payload
    write_json(REVIEW_RESULT_PATH, result)
    write_json(RUN_MANIFEST_PATH, result)

    update_current_working_state(result)
    update_selection_status(result)
    update_workspace_state(result)
    update_review_index(result)
    return result


if __name__ == "__main__":
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
