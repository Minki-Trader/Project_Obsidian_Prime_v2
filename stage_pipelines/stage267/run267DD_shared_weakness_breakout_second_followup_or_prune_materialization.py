from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import (
    run267BW_aggressive_impulse_dd_shape_cross_period_materialization as source_bw,
)
from stage_pipelines.stage267 import (
    run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization as source_cz,
)
from stage_pipelines.stage267 import (
    run267DC_shared_weakness_breakout_second_followup_or_prune_design as source_design,
)
from stage_pipelines.stage267 import (
    run267BS_pool_wide_directional_impulse_followup_materialization as score_validator,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267DD"
RUN_ID = "run267DD_stage267_shared_weakness_breakout_second_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_CZ_RUN_ID = source_cz.RUN_ID
SOURCE_BW_RUN_ID = source_bw.RUN_ID
STATUS = "run267DD_shared_weakness_breakout_second_followup_or_prune_materialized_execution_pending"
JUDGMENT = "shared_weakness_second_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267DE_execute_shared_weakness_breakout_second_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_second_followup_or_prune_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_FEATURE_BLUEPRINT_PATH = source_design.FEATURE_BLUEPRINT_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_CZ_VARIANT_MANIFEST_PATH = source_cz.VARIANT_MANIFEST_PATH
SOURCE_CZ_ATTEMPT_MANIFEST_PATH = source_cz.ATTEMPT_MANIFEST_PATH
SOURCE_CZ_REPORT_PATH = source_cz.REPORT_PATH
SOURCE_BW_VARIANT_MANIFEST_PATH = source_bw.VARIANT_MANIFEST_PATH
SOURCE_BW_ATTEMPT_MANIFEST_PATH = source_bw.ATTEMPT_MANIFEST_PATH
SOURCE_BW_REPORT_PATH = source_bw.REPORT_PATH

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
HANDOFF_RECEIPT_PATH = RUN_ROOT / "handoff_receipt.csv"
FEATURE_MUTATION_RECEIPT_PATH = RUN_ROOT / "feature_mutation_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DD_shared_weakness_breakout_second_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DD_shared_weakness_breakout_second_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267dd/run267DD_shared_weakness_second_followup_or_prune"
MATERIALIZATION_BOUNDARY = "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B are kept only where source attempts exist; "
    "true Tier B fallback and actual routed total remain unclaimed"
)

PERIOD_SUFFIX = {
    "2023H2": "2023h2",
    "2025H1": "2025h1",
    "2025H2": "2025h2",
}


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


def split_semicolon(value: Any) -> list[str]:
    text = str(value or "").strip()
    return [part.strip() for part in text.split(";") if part.strip()]


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
    lines = ["; generated_by=run267DD_shared_weakness_breakout_second_followup_or_prune_materialization"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_tester_ini"}


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, current in enumerate(lines):
        if needle in current:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + marker + focus_block
    return text.replace(marker, marker + focus_block, 1)


def normalize(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").fillna(0.0).astype("float64")
    lo = float(values.min()) if len(values) else 0.0
    hi = float(values.max()) if len(values) else 0.0
    if hi <= lo:
        return pd.Series(0.5, index=values.index, dtype="float64")
    return ((values - lo) / (hi - lo)).clip(0.0, 1.0)


def mutate_aia_similar_replacement(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    target = "stage267cz_aia_validation_damage_probe_score"
    parts: list[pd.Series] = []
    weights: list[float] = []
    for column, weight in (
        ("stage267cf_volatility_energy_transition_score", 0.35),
        ("stage267cf_range_pressure_asymmetry_score", 0.25),
        ("historical_vol_5_over_20", 0.20),
        ("atr_14_over_atr_50", 0.20),
    ):
        if column in frame.columns:
            parts.append(normalize(frame[column]))
            weights.append(weight)
    if not parts:
        raise RuntimeError("missing columns for s264_aia similar replacement")
    total = sum(weights)
    replacement = sum(weight * part for part, weight in zip(parts, weights, strict=True)) / total
    output = frame.copy()
    output[target] = replacement.clip(0.0, 1.0)
    return output, {
        "mutation_type": "similar_feature_replacement",
        "target_feature": target,
        "replacement_columns": ";".join(
            column
            for column in (
                "stage267cf_volatility_energy_transition_score",
                "stage267cf_range_pressure_asymmetry_score",
                "historical_vol_5_over_20",
                "atr_14_over_atr_50",
            )
            if column in frame.columns
        ),
        "replacement_min": float(output[target].min()) if len(output) else 0.0,
        "replacement_max": float(output[target].max()) if len(output) else 0.0,
        "replacement_mean": float(output[target].mean()) if len(output) else 0.0,
    }


def mutate_aia_ablation_neutralized(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    target = "stage267cz_aia_validation_damage_probe_score"
    if target not in frame.columns:
        raise RuntimeError(f"missing target feature for ablation: {target}")
    output = frame.copy()
    median = float(pd.to_numeric(output[target], errors="coerce").median())
    if not math.isfinite(median):
        median = 0.5
    output[target] = median
    return output, {
        "mutation_type": "feature_neutralization_ablation",
        "target_feature": target,
        "replacement_columns": "constant_median",
        "replacement_min": median,
        "replacement_max": median,
        "replacement_mean": median,
    }


def identity_mutation(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    return frame.copy(), {
        "mutation_type": "identity_copy",
        "target_feature": "",
        "replacement_columns": "",
        "replacement_min": "",
        "replacement_max": "",
        "replacement_mean": "",
    }


def validate_runtime_feature(feature_path: Path, model_path: Path, feature_order: Sequence[str]) -> dict[str, Any]:
    return score_validator.validate_score_table(feature_path, model_path, feature_order)


def source_attempts_by_variant(rows: Sequence[Mapping[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(str(row["variant_id"]), []).append(dict(row))
    for attempts in result.values():
        attempts.sort(key=lambda item: (item.get("tier", ""), item.get("attempt_name", "")))
    return result


def source_variant_by_id(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row["variant_id"]): dict(row) for row in rows}


def copy_model(source_model: Path, target_model: Path) -> None:
    io_path(target_model.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source_model), io_path(target_model))


def materialize_variant(
    *,
    plan: Mapping[str, Any],
    source_variant: Mapping[str, str],
    source_attempts: Sequence[Mapping[str, str]],
    mutation: Callable[[pd.DataFrame], tuple[pd.DataFrame, dict[str, Any]]],
    period_override: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    variant_id = str(plan["variant_id"])
    alias = str(source_variant["candidate_alias"])
    source_feature_path = repo_path(str(source_variant["runtime_feature_file"]))
    source_model_path = repo_path(str(source_variant["runtime_model_file"]))
    if not path_exists(source_feature_path):
        raise FileNotFoundError(source_feature_path)
    if not path_exists(source_model_path):
        raise FileNotFoundError(source_model_path)

    feature_order = split_semicolon(source_variant["feature_order"])
    frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    frame, mutation_receipt = mutation(frame)
    if ordered_hash(feature_order) != str(source_variant["feature_order_hash"]):
        raise RuntimeError(f"source feature order hash mismatch: {source_variant['variant_id']}")

    target_feature_path = FEATURE_ROOT / alias / variant_id / f"{variant_id}_features.csv"
    target_model_path = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"
    io_path(target_feature_path.parent).mkdir(parents=True, exist_ok=True)
    frame.loc[:, ["bar_time_server", *feature_order]].to_csv(
        io_path(target_feature_path),
        index=False,
        encoding="utf-8",
        lineterminator="\n",
    )
    copy_model(source_model_path, target_model_path)
    validation = validate_runtime_feature(target_feature_path, target_model_path, feature_order)

    common_root = f"{COMMON_ROOT}/{alias}/{variant_id}"
    common_feature_path = f"{common_root}/features/{target_feature_path.name}"
    common_model_path = f"{common_root}/models/{target_model_path.name}"
    common_feature = copy_to_common(target_feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(target_model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)
    feature_order_hash = ordered_hash(feature_order)

    variant_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "source_run_id": plan["source_run_id"],
        "source_variant_id": source_variant["variant_id"],
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": source_variant.get("candidate_role"),
        "profile_label": plan["profile_label"],
        "source_profile_label": source_variant.get("profile_label"),
        "model_materialization_type": plan["model_materialization_type"],
        "runtime_model_file": rel(target_model_path),
        "runtime_model_sha256": sha256_file_lf_normalized(target_model_path),
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": rel(target_feature_path),
        "runtime_feature_sha256": sha256_file_lf_normalized(target_feature_path),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": feature_order_hash,
        "engineered_features": source_variant.get("engineered_features"),
        "known_difference": plan["known_difference"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    feature_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_run_id": plan["source_run_id"],
        "source_variant_id": source_variant["variant_id"],
        "source_feature_file": rel(source_feature_path),
        "source_feature_sha256": sha256_file_lf_normalized(source_feature_path),
        "runtime_feature_file": rel(target_feature_path),
        "runtime_feature_sha256": sha256_file_lf_normalized(target_feature_path),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "rows": int(len(frame)),
        "first_bar_time_server": str(frame["bar_time_server"].iloc[0]) if len(frame) else "",
        "last_bar_time_server": str(frame["bar_time_server"].iloc[-1]) if len(frame) else "",
        "duplicate_bar_time_rows": int(frame["bar_time_server"].duplicated().sum()) if len(frame) else 0,
        "runtime_missing_feature_cells": int(frame.loc[:, feature_order].isna().sum().sum()) if len(frame) else 0,
        **validation,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_run_id": plan["source_run_id"],
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": rel(target_model_path),
        "runtime_model_sha256": sha256_file_lf_normalized(target_model_path),
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "model_materialization_type": plan["model_materialization_type"],
        "claim_boundary": CLAIM_BOUNDARY,
    }

    attempt_rows: list[dict[str, Any]] = []
    for index, source_attempt in enumerate(source_attempts, start=1):
        tier = str(source_attempt.get("tier") or plan.get("tier") or "Tier A")
        tier_token = "rt" if "A+B" in tier else "ta"
        period_token = str(plan.get("period_token") or "2024")
        attempt_name = f"{variant_id}_{tier_token}_{period_token}"
        telemetry = f"{common_root}/telemetry/{attempt_name}_telemetry.csv"
        summary = f"{common_root}/telemetry/{attempt_name}_summary.csv"

        set_values = parse_key_values(repo_path(str(source_attempt["set_path"])))
        set_values.update(
            {
                "InpRunId": RUN_ID,
                "InpExplorationLabel": str(plan["exploration_label"]),
                "InpTierLabel": tier,
                "InpSplitLabel": str(plan.get("split_label") or source_attempt.get("split") or "historical_2024"),
                "InpModelPath": common_model_path,
                "InpModelId": f"{RUN_ID}_{variant_id}",
                "InpModelBackend": "ebm_table",
                "InpModelUseCommonFiles": "true",
                "InpFeatureCsvPath": common_feature_path,
                "InpFeatureCount": len(feature_order),
                "InpFeatureCsvUseCommonFiles": "true",
                "InpFeatureRequireTimestampMatch": "true",
                "InpFeatureAllowLatestFallback": "false",
                "InpFeatureStrictHeader": "true",
                "InpFeatureOrderHash": feature_order_hash,
                "InpFallbackEnabled": set_values.get("InpFallbackEnabled", "false"),
                "InpFallbackFeatureCsvPath": common_feature_path,
                "InpFallbackFeatureCount": len(feature_order),
                "InpFallbackModelPath": common_model_path,
                "InpFallbackModelId": f"{RUN_ID}_{variant_id}_fallback_boundary",
                "InpFallbackModelBackend": "ebm_table",
                "InpFallbackFeatureOrderHash": feature_order_hash,
                "InpTelemetryCsvPath": telemetry,
                "InpSummaryCsvPath": summary,
                "InpTelemetryUseCommonFiles": "true",
                "InpMagic": 26740000 + int(plan["order"]) * 10 + index,
            }
        )
        set_payload = write_set(MT5_ROOT / f"{attempt_name}.set", set_values)

        ini_values = parse_key_values(repo_path(str(source_attempt["ini_path"])))
        if period_override:
            ini_values.update(period_override)
        ini_values.update(
            {
                "ExpertParameters": EA_TESTER_SET_NAME,
                "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
                "ReplaceReport": 1,
                "ShutdownTerminal": 1,
            }
        )
        ini_payload = write_ini(MT5_ROOT / f"{attempt_name}.ini", ini_values)

        attempt_rows.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant_id,
                "queue_id": plan["queue_id"],
                "source_run_id": plan["source_run_id"],
                "source_variant_id": source_variant["variant_id"],
                "source_attempt_name": source_attempt["attempt_name"],
                "candidate_id": source_variant.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": source_variant.get("candidate_role"),
                "profile_label": plan["profile_label"],
                "tier": tier,
                "attempt_role": source_attempt.get("attempt_role") or ("routed_total_duplicate_boundary" if "A+B" in tier else "tier_only_total"),
                "target_period": plan.get("target_period", "historical_2024"),
                "split": plan.get("split_label") or source_attempt.get("split") or "historical_2024",
                "record_view_prefix": f"mt5_{tier_token}_{alias}_{plan['profile_token']}",
                "set_path": set_payload["path"],
                "set_sha256": set_payload["sha256"],
                "ini_path": ini_payload["path"],
                "ini_sha256": ini_payload["sha256"],
                "common_telemetry_path": telemetry,
                "common_summary_path": summary,
                "common_feature_path": common_feature_path,
                "common_model_path": common_model_path,
                "tier_pair_boundary": plan.get("tier_pair_boundary") or TIER_PAIR_BOUNDARY,
                "execution_status": "execution_pending",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    mutation_row = {
        "receipt_id": f"run267dd_mutation_{variant_id}",
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_variant_id": source_variant["variant_id"],
        "source_run_id": plan["source_run_id"],
        "mutation_status": "materialized",
        "effect": plan["known_difference"],
        **mutation_receipt,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    handoff_row = {
        "receipt_id": f"run267dd_handoff_{variant_id}",
        "variant_id": variant_id,
        "candidate_alias": alias,
        "feature_order_hash": feature_order_hash,
        "feature_count": len(feature_order),
        "model_sha256": model_row["runtime_model_sha256"],
        "attempts": len(attempt_rows),
        "handoff_status": "model_feature_set_ini_manifest_ready",
        "runtime_claim": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_contract = {
        "variant_id": variant_id,
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": source_variant.get("candidate_role"),
        "profile_label": plan["profile_label"],
        "source_profile_label": source_variant.get("profile_label"),
        "source_run_id": plan["source_run_id"],
        "shared_contract": "US100 M5; MT5 RuntimeProbeEA handoff; score table model; feature order hash tracked",
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "model_backend": "ebm_table",
        "model_materialization_type": plan["model_materialization_type"],
        "known_difference": plan["known_difference"],
        "tier_pair_boundary": plan.get("tier_pair_boundary") or TIER_PAIR_BOUNDARY,
        "runtime_claim_boundary": CLAIM_BOUNDARY,
    }
    return variant_row, feature_row, model_row, attempt_rows, runtime_contract, mutation_row, [handoff_row]


def build_plans(cz_variants: Mapping[str, Mapping[str, str]], bw_variants: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    bw_s258 = [
        row
        for row in bw_variants.values()
        if row.get("candidate_alias") == "s258_stc" and row.get("target_period") in PERIOD_SUFFIX
    ]
    bw_s258.sort(key=lambda row: str(row.get("target_period")))
    plans: list[dict[str, Any]] = []
    order = 0
    for source in bw_s258:
        order += 1
        period = str(source["target_period"])
        token = PERIOD_SUFFIX[period]
        plans.append(
            {
                "order": order,
                "queue_id": "dc_q01_s258_session_cross_period_stress",
                "source_run_id": SOURCE_BW_RUN_ID,
                "source_variant_id": source["variant_id"],
                "variant_id": f"run267dd_{order:02d}_s258_stc_{token}_session_cross_stress",
                "profile_label": "s258_session_cross_period_stress",
                "profile_token": f"session_cross_{token}",
                "target_period": period,
                "period_token": token,
                "split_label": source.get("period_label") or source.get("target_period"),
                "exploration_label": f"stage267_BaselineRacing__S258SessionCrossPeriod_{token}",
                "model_materialization_type": "cloned_run267BW_s258_adjacent_period_impulse_replacement_as_session_cross_period_stress",
                "known_difference": "reuses prior adjacent-period s258 feature/model handoff as compact session/cross-period stress bridge; no new calendar filter",
                "tier_pair_boundary": "Tier A adjacent-period attempt only; true Tier B fallback and duplicate routed total not claimed for q01",
                "mutation": identity_mutation,
            }
        )

    explicit = [
        (
            "dc_q02_s264_aia_adapter_replacement_watch",
            "run267cz_04_s264_aia_aia_val_damage",
            "s264_aia_similar_replacement_watch",
            "aia_similar_replacement",
            "stage267_BaselineRacing__AIAAdapterSimilarReplacement",
            "same score table and feature order; validation-damage feature column is replaced by volatility/range-energy similar meaning",
            "similar_replacement_on_run267CZ_s264_aia_validation_damage_probe",
            mutate_aia_similar_replacement,
            None,
        ),
        (
            "dc_q02_s264_aia_adapter_replacement_watch",
            "run267cz_04_s264_aia_aia_val_damage",
            "s264_aia_ablation_neutralized_watch",
            "aia_ablation_neutral",
            "stage267_BaselineRacing__AIAAdapterAblationNeutralization",
            "same score table and feature order; validation-damage feature column is neutralized to median as a narrow ablation stress",
            "feature_neutralization_ablation_on_run267CZ_s264_aia_validation_damage_probe",
            mutate_aia_ablation_neutralized,
            None,
        ),
        (
            "dc_q03_s264_aih_destructive_prune_probe",
            "run267cz_05_s264_aih_aih_final_supply",
            "s264_aih_december_destructive_prune",
            "aih_december_prune",
            "stage267_BaselineRacing__AIHDecemberDestructivePruneProbe",
            "same feature/model identity; tester period is narrowed to 2024-12 to pressure the known worst-month hole",
            "identity_copy_with_2024_12_destructive_prune_period",
            identity_mutation,
            {"FromDate": "2024.12.01", "ToDate": "2025.01.01"},
        ),
        (
            "dc_q04_control_pair_weekday_dd_audit",
            "run267cz_06_s264_lc_control_rejoin",
            "s264_lc_weekday_dd_control",
            "lc_weekday_dd",
            "stage267_BaselineRacing__ControlPairWeekdayDDAudit",
            "control identity is copied beside aggressive rows so weekday/DD weakness has a same-batch comparison",
            "identity_copy_run267CZ_control_for_weekday_dd_audit",
            identity_mutation,
            None,
        ),
        (
            "dc_q04_control_pair_weekday_dd_audit",
            "run267cz_07_s262_lih_control_rejoin",
            "s262_lih_weekday_dd_control",
            "lih_weekday_dd",
            "stage267_BaselineRacing__ControlPairWeekdayDDAudit",
            "validation-heavy control identity is copied beside aggressive rows so weekday/DD weakness has a same-batch comparison",
            "identity_copy_run267CZ_control_for_weekday_dd_audit",
            identity_mutation,
            None,
        ),
    ]
    for queue_id, source_variant_id, suffix, profile_token, label, difference, model_type, mutation, period_override in explicit:
        if source_variant_id not in cz_variants:
            raise KeyError(source_variant_id)
        order += 1
        alias = str(cz_variants[source_variant_id]["candidate_alias"])
        plans.append(
            {
                "order": order,
                "queue_id": queue_id,
                "source_run_id": SOURCE_CZ_RUN_ID,
                "source_variant_id": source_variant_id,
                "variant_id": f"run267dd_{order:02d}_{suffix}",
                "profile_label": suffix,
                "profile_token": profile_token,
                "target_period": "historical_2024_december" if period_override else "historical_2024",
                "period_token": "2024",
                "split_label": "historical_2024_december_destructive_prune" if period_override else "historical_2024",
                "exploration_label": label,
                "model_materialization_type": model_type,
                "known_difference": difference,
                "tier_pair_boundary": TIER_PAIR_BOUNDARY,
                "mutation": mutation,
                "period_override": period_override,
                "candidate_alias": alias,
            }
        )
    return plans


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]], plan_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for row in plan_rows:
        key = str(row["queue_id"])
        counts[key] = counts.get(key, 0) + 1
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = str(queue["queue_id"])
        if queue_id in counts:
            decision = "materialized_execution_pending"
            effect = f"variants={counts[queue_id]}개를 MT5 입력으로 만들었다."
        elif queue_id == "dc_q05_survivor_ablation_replacement_gate":
            decision = "held_until_run267DE_run267DF_survivors_exist"
            effect = "P0 생존 후보가 아직 없어서 feature ablation(피처 제거)과 similar replacement(유사 대체)를 보류했다."
        elif queue_id == "dc_q06_runtime_handoff_receipt_gap":
            decision = "receipt_attached_no_mt5_attempt"
            effect = "모든 물질화 variant(변형)에 handoff receipt(인계 영수증)를 붙였고, runtime authority(런타임 권위)는 주장하지 않는다."
        else:
            decision = "held_unrecognized_scope"
            effect = "이번 물질화 범위 밖으로 보류했다."
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "workstream": queue.get("workstream"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "run267DD_decision": decision,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = str(queue.get("queue_id", ""))
        if queue_id == "dc_q05_survivor_ablation_replacement_gate":
            rows.append(
                {
                    "queue_id": queue_id,
                    "priority": queue.get("priority"),
                    "candidate_aliases": queue.get("candidate_aliases"),
                    "hold_status": "held_until_run267DE_run267DF_survivors_exist",
                    "why_held": "생존 후보가 확정되기 전 제거/대체를 돌리면 죽은 분기까지 다시 넓혀 병목이 된다.",
                    "next_action": "after MT5 execution and balance/time-slice review, materialize only surviving candidates.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        elif queue_id == "dc_q06_runtime_handoff_receipt_gap":
            rows.append(
                {
                    "queue_id": queue_id,
                    "priority": queue.get("priority"),
                    "candidate_aliases": queue.get("candidate_aliases"),
                    "hold_status": "converted_to_handoff_receipts_no_mt5_attempt",
                    "why_held": "이 큐는 성능 실험이 아니라 인계 공백 감사라 별도 MT5 attempt(시도)를 만들지 않는다.",
                    "next_action": "block next MT5 execution if any handoff receipt is incomplete.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        rows.append(
            {
                "receipt_id": f"run267dd_{queue.get('queue_id')}",
                "hypothesis": queue.get("hypothesis"),
                "decision_use": queue.get("decision_use"),
                "comparison_baseline": queue.get("comparison_baseline"),
                "control_variables": queue.get("control_variables"),
                "changed_variables": queue.get("changed_variables"),
                "sample_scope": queue.get("sample_scope"),
                "success_criteria": queue.get("success_criteria"),
                "failure_criteria": queue.get("failure_criteria"),
                "invalid_conditions": queue.get("invalid_conditions"),
                "stop_conditions": queue.get("stop_conditions"),
                "evidence_plan": queue.get("evidence_plan"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def environment_receipt_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267dd_environment_reproducibility",
            "execution_environment": "Windows local MT5 workspace; Python materialization; MT5 Strategy Tester execution pending",
            "dependency_surface": "pandas; project ledger helpers; run267CZ/run267BW source artifacts; MT5 Common Files handoff",
            "entry_command": f"python {rel(PRODUCER_PATH)}",
            "mt5_execution_status": "execution_pending",
            "common_root": COMMON_ROOT,
            "reproducibility_judgment": "reproducible_with_project_artifacts_and_common_files_setup",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicates = sum(int(row.get("duplicate_bar_time_rows", 0)) for row in feature_rows)
    missing = sum(int(row.get("runtime_missing_feature_cells", 0)) for row in feature_rows)
    return [
        {
            "receipt_id": "run267dd_feature_frame_integrity",
            "feature_frames": len(feature_rows),
            "duplicate_bar_time_rows_total": duplicates,
            "runtime_missing_feature_cells_total": missing,
            "score_table_validation_passed": sum(1 for row in feature_rows if row.get("score_table_validation") == "passed"),
            "integrity_status": "passed" if feature_rows and duplicates == 0 and missing == 0 else "warning",
            "effect": "MT5 입력 전에 feature order(피처 순서), timestamp(타임스탬프), score table(점수표) 연결을 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_parity_rows(feature_rows: Sequence[Mapping[str, Any]], model_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    models = {row["variant_id"]: row for row in model_rows}
    return [
        {
            "receipt_id": f"run267dd_runtime_handoff_{row['variant_id']}",
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
            "feature_order_hash": row["feature_order_hash"],
            "model_sha256": models[str(row["variant_id"])]["runtime_model_sha256"],
            "score_table_validation": row.get("score_table_validation"),
            "runtime_handoff_status": "set_ini_materialized_execution_pending",
            "parity_boundary": "Python materialization and MT5 handoff are aligned by file/hash/order only; runtime reproduction is next run.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in feature_rows
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "judgment_id": "run267dd_materialization_judgment",
            "result_subject": "run267DD shared weakness second follow-up/prune materialization(공유 약점 2차 후속/가지치기 물질화)",
            "evidence_available": "feature/model/set/ini inputs, manifests, queue decisions, handoff receipts",
            "evidence_missing": "MT5 execution, balance/equity curve, time-slice KPI, trade quality, true Tier B fallback",
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "counts": json.dumps(json_ready(dict(counts)), ensure_ascii=False, sort_keys=True),
            "next_action": NEXT_ACTION,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = (
        ("source_design_queue_available", counts["queue_rows"] == 6, f"queue_rows={counts['queue_rows']}"),
        ("variant_count_expected", counts["variants"] == 8, f"variants={counts['variants']}"),
        ("attempt_count_expected", counts["attempts"] == 13, f"attempts={counts['attempts']}"),
        ("q01_cross_period_materialized", counts["q01_variants"] == 3, f"q01_variants={counts['q01_variants']}"),
        ("q02_replacement_ablation_materialized", counts["q02_variants"] == 2, f"q02_variants={counts['q02_variants']}"),
        ("q03_prune_probe_materialized", counts["q03_variants"] == 1, f"q03_variants={counts['q03_variants']}"),
        ("q04_control_pair_materialized", counts["q04_variants"] == 2, f"q04_variants={counts['q04_variants']}"),
        ("held_or_receipt_rows_documented", counts["held_rows"] == 2, f"held_rows={counts['held_rows']}"),
        ("score_table_validation_passed", counts["score_table_validation_passed"] == counts["variants"], f"passed={counts['score_table_validation_passed']};variants={counts['variants']}"),
        ("handoff_receipts_complete", counts["handoff_receipts"] == counts["variants"], f"handoff_receipts={counts['handoff_receipts']}"),
        ("no_selection_claim", True, "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed"),
    )
    return [
        {
            "gate": name,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, passed, evidence in checks
    ]


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(MATERIALIZATION_PLAN_PATH, result["materialization_plan"])
    write_csv(QUEUE_DECISION_PATH, result["queue_decisions"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(MODEL_MANIFEST_PATH, result["model_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"])
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"])
    write_csv(HELD_QUEUE_PATH, result["held_queue"])
    write_csv(HANDOFF_RECEIPT_PATH, result["handoff_receipt"])
    write_csv(FEATURE_MUTATION_RECEIPT_PATH, result["feature_mutation_receipt"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, result["environment_reproducibility_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, run_manifest_payload(result))
    write_json(LINEAGE_PATH, lineage_payload(result))
    write_json(REVIEW_RESULT_PATH, review_result_payload(result))
    write_md(REPORT_PATH, report_markdown(result))


def run_manifest_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_ids": [source_design.RUN_ID, SOURCE_CZ_RUN_ID, SOURCE_BW_RUN_ID],
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": result["counts"],
        "outputs": result["outputs"],
        "sources": result["sources"],
    }


def lineage_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_inputs": result["sources"],
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": result["outputs"],
        "registry_links": {
            "stage_ledger": rel(STAGE_LEDGER_PATH),
            "project_ledger": rel(PROJECT_LEDGER_PATH),
            "run_registry": rel(RUN_REGISTRY_PATH),
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
        },
        "availability": "tracked_after_git_add_force_for_02_runs",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_result_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "next_action": NEXT_ACTION,
        "counts": result["counts"],
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "outputs": result["outputs"],
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    variant_lines = "\n".join(
        f"| `{row['variant_id']}` | `{row['candidate_alias']}` | `{row['profile_label']}` | `{row['queue_id']}` |"
        for row in result["variant_manifest"]
    )
    queue_lines = "\n".join(
        f"| `{row['queue_id']}` | `{row['run267DD_decision']}` | {row['effect']} |"
        for row in result["queue_decisions"]
    )
    return f"""# Stage267 Run267DD Shared Weakness Second Follow-up/Prune Materialization(267단계 267DD 공유 약점 2차 후속/가지치기 물질화)

- status(상태): `{STATUS}`
- variants(변형): `{counts['variants']}`
- attempts(시도): `{counts['attempts']}`
- held_rows(보류 행): `{counts['held_rows']}`
- next_action(다음 행동): `{NEXT_ACTION}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DD(267DD 실행)는 run267DC(267DC 실행)의 설계를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꿨다.
Effect(효과): s258_stc는 인접 기간 압박, s264_aia는 유사 대체와 피처 중립화, s264_aih는 2024년 12월 파괴 압박, s264_lc/s262_lih는 대조 쌍으로 다음 실행에서 바로 비교할 수 있다.

아직 후보 선택(selection, 선택)이 아니다. 숫자를 보려면 run267DE(267DE 실행) MT5 실행과 run267DF(267DF 실행) balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토가 필요하다.

## Queue Decisions(대기열 판단)

| queue(대기열) | decision(판단) | effect(효과) |
|---|---|---|
{queue_lines}

## Variants(변형)

| variant(변형) | candidate(후보) | profile(프로필) | queue(대기열) |
|---|---|---|---|
{variant_lines}

## Artifacts(산출물)

- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`
- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`
- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`
- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`
- handoff_receipt(인계 영수증): `{rel(HANDOFF_RECEIPT_PATH)}`
- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`

## Boundary(경계)

이 실행은 materialization(물질화)만 닫는다. deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    artifact_specs = (
        ("stage267_run267DD_producer", "producer_script", PRODUCER_PATH, "Builds run267DD materialization."),
        ("stage267_run267DD_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267DD_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decisions."),
        ("stage267_run267DD_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267DD_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267DD_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267DD_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267DD_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267DD_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267DD_handoff_receipt", "handoff_receipt", HANDOFF_RECEIPT_PATH, "Handoff receipt."),
        ("stage267_run267DD_feature_mutation", "feature_mutation_receipt", FEATURE_MUTATION_RECEIPT_PATH, "Feature mutation receipt."),
        ("stage267_run267DD_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DD_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267DD_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267DD_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267DD_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DD_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DD_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DD_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DD_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267DD_report", "review_report", REPORT_PATH, "User-facing report."),
    )
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in artifact_specs:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256_lf": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    stage_row = {
        "row_id": "stage267_run267DD_shared_weakness_breakout_second_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_second_followup_or_prune_materialization",
        "tier_scope": "Tier A plus duplicate-boundary rows where source exists; true fallback not claimed",
        "scoreboard": "feature_model_set_ini_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
        "path": rel(REPORT_PATH),
        "notes": f"variants={counts['variants']};attempts={counts['attempts']};held_rows={counts['held_rows']};next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_shared_weakness_second_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"variants={counts['variants']};attempts={counts['attempts']};held_rows={counts['held_rows']};next_action={NEXT_ACTION}.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_second_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_second_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_second_followup_or_prune_materialization",
        "tier_scope": "Tier A plus duplicate-boundary rows where source exists; true fallback not claimed",
        "kpi_scope": "feature_model_set_ini_materialization",
        "scoreboard_lane": "shared_weakness_second_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_documents(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267DD_shared_weakness_breakout_second_followup_or_prune_materialization"
        f"(267DD 공유 약점 2차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267DD_summary(267DD 요약): run267DC(267DC 실행)의 materialization queue(물질화 대기열)를 "
        f"variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개로 바꿨다. "
        "Effect(효과): s258 인접 기간, s264_aia 대체/중립화, s264_aih 파괴 압박, control pair(대조 쌍)를 다음 MT5 실행 입력으로 만들었다."
    )
    block = "\n".join(
        [
            "Run267DD(267DD 실행)는 run267DC(267DC 실행)의 2차 follow-up/prune queue(후속/가지치기 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개를 만들고, survivor ablation/replacement(생존 후보 제거/대체)는 run267DE/run267DF 이후로 보류했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_materialization`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267DC_shared_weakness_breakout_second_followup_or_prune_design.md", report_line)
            text = append_after_contains(text, "run267DC_summary", summary_line)
            text = append_block_once(text, "Run267DD(267DD 실행)는 run267DC", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267DC_shared_weakness_breakout_second_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267DD(267DD 실행)는 run267DC", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267DC_shared_weakness_breakout_second_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267DD(267DD 실행)는 run267DC", block)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DD(267DD 실행) shared weakness breakout second follow-up/prune materialization"
        f"(공유 약점 2차 후속/가지치기 물질화) `{STATUS}`. Effect(효과): run267DC(267DC 실행)의 queue(대기열)를 "
        f"variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개로 나눴고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_line)
    workspace = workspace.replace(f"next_action: {source_design.NEXT_ACTION}", f"next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267DC_shared_weakness_breakout_second_followup_or_prune_design_report_path",
        f"  run267DD_shared_weakness_breakout_second_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build_result() -> dict[str, Any]:
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_FEATURE_BLUEPRINT_PATH,
        SOURCE_BRANCH_DECISION_PATH,
        SOURCE_PRUNE_MATRIX_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_CZ_VARIANT_MANIFEST_PATH,
        SOURCE_CZ_ATTEMPT_MANIFEST_PATH,
        SOURCE_BW_VARIANT_MANIFEST_PATH,
        SOURCE_BW_ATTEMPT_MANIFEST_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    cz_variants = source_variant_by_id(read_csv(SOURCE_CZ_VARIANT_MANIFEST_PATH))
    bw_variants = source_variant_by_id(read_csv(SOURCE_BW_VARIANT_MANIFEST_PATH))
    cz_attempts = source_attempts_by_variant(read_csv(SOURCE_CZ_ATTEMPT_MANIFEST_PATH))
    bw_attempts = source_attempts_by_variant(read_csv(SOURCE_BW_ATTEMPT_MANIFEST_PATH))
    plan_rows = build_plans(cz_variants, bw_variants)

    variant_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    mutation_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []

    for plan in plan_rows:
        source_run_id = str(plan["source_run_id"])
        variants = bw_variants if source_run_id == SOURCE_BW_RUN_ID else cz_variants
        attempts = bw_attempts if source_run_id == SOURCE_BW_RUN_ID else cz_attempts
        source_variant = variants[str(plan["source_variant_id"])]
        source_variant_attempts = attempts[str(plan["source_variant_id"])]
        if source_run_id == SOURCE_BW_RUN_ID:
            source_variant_attempts = [row for row in source_variant_attempts if row.get("tier") == "Tier A"]
        variant, feature, model, attempt, contract, mutation, handoff = materialize_variant(
            plan=plan,
            source_variant=source_variant,
            source_attempts=source_variant_attempts,
            mutation=plan["mutation"],
            period_override=plan.get("period_override"),
        )
        variant_rows.append(variant)
        feature_rows.append(feature)
        model_rows.append(model)
        attempt_rows.extend(attempt)
        contracts.append(contract)
        mutation_rows.append(mutation)
        handoff_rows.extend(handoff)

    queue_decisions = queue_decision_rows(queue_rows, plan_rows)
    held_rows = held_queue_rows(queue_rows)
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "held_rows": len(held_rows),
        "handoff_receipts": len(handoff_rows),
        "feature_mutation_receipts": len(mutation_rows),
        "score_table_validation_passed": sum(1 for row in feature_rows if row.get("score_table_validation") == "passed"),
        "q01_variants": sum(1 for row in variant_rows if row.get("queue_id") == "dc_q01_s258_session_cross_period_stress"),
        "q02_variants": sum(1 for row in variant_rows if row.get("queue_id") == "dc_q02_s264_aia_adapter_replacement_watch"),
        "q03_variants": sum(1 for row in variant_rows if row.get("queue_id") == "dc_q03_s264_aih_destructive_prune_probe"),
        "q04_variants": sum(1 for row in variant_rows if row.get("queue_id") == "dc_q04_control_pair_weekday_dd_audit"),
    }
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_cz_run_id": SOURCE_CZ_RUN_ID,
        "source_bw_run_id": SOURCE_BW_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": counts,
        "materialization_plan": [
            {key: value for key, value in row.items() if key not in {"mutation", "period_override"}}
            for row in plan_rows
        ],
        "queue_decisions": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": contracts,
        "held_queue": held_rows,
        "handoff_receipt": handoff_rows,
        "feature_mutation_receipt": mutation_rows,
        "experiment_design_receipt": experiment_design_rows(queue_rows),
        "environment_reproducibility_receipt": environment_receipt_rows(),
        "data_integrity_receipt": data_integrity_rows(feature_rows),
        "runtime_parity_receipt": runtime_parity_rows(feature_rows, model_rows),
        "result_judgment": result_judgment_rows(counts),
        "gate_audit": gate_audit_rows(counts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "sources": {
            "source_queue": rel(SOURCE_QUEUE_PATH),
            "source_feature_blueprint": rel(SOURCE_FEATURE_BLUEPRINT_PATH),
            "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
            "source_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_cz_variant_manifest": rel(SOURCE_CZ_VARIANT_MANIFEST_PATH),
            "source_cz_attempt_manifest": rel(SOURCE_CZ_ATTEMPT_MANIFEST_PATH),
            "source_bw_variant_manifest": rel(SOURCE_BW_VARIANT_MANIFEST_PATH),
            "source_bw_attempt_manifest": rel(SOURCE_BW_ATTEMPT_MANIFEST_PATH),
            "source_design_report": rel(source_design.REPORT_PATH),
            "source_cz_report": rel(SOURCE_CZ_REPORT_PATH),
            "source_bw_report": rel(SOURCE_BW_REPORT_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "materialization_plan": rel(MATERIALIZATION_PLAN_PATH),
            "queue_decision": rel(QUEUE_DECISION_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
            "model_manifest": rel(MODEL_MANIFEST_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "held_queue": rel(HELD_QUEUE_PATH),
            "handoff_receipt": rel(HANDOFF_RECEIPT_PATH),
            "feature_mutation_receipt": rel(FEATURE_MUTATION_RECEIPT_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "environment_reproducibility_receipt": rel(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    return result


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers_and_artifacts(str(result["created_at_utc"]), result)
    update_current_documents(result)
    return result


def main() -> int:
    result = execute()
    counts = result["counts"]
    print(
        json.dumps(
            {
                "status": result["status"],
                "variants": counts["variants"],
                "attempts": counts["attempts"],
                "held_rows": counts["held_rows"],
                "score_table_validation_passed": counts["score_table_validation_passed"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
