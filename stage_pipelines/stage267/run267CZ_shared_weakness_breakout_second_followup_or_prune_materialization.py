from __future__ import annotations

import csv
import json
import math
import shutil
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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import (
    run267CR_shared_weakness_breakout_followup_materialization as materializer,
)
from stage_pipelines.stage267 import (
    run267CV_shared_weakness_breakout_followup_or_prune_materialization as source_cv,
)
from stage_pipelines.stage267 import (
    run267CY_shared_weakness_breakout_second_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CZ"
RUN_ID = "run267CZ_stage267_shared_weakness_breakout_second_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_CV_RUN_ID = source_cv.RUN_ID
SOURCE_CR_RUN_ID = materializer.RUN_ID
STATUS = "run267CZ_shared_weakness_breakout_second_followup_or_prune_materialized_execution_pending"
JUDGMENT = "shared_weakness_second_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267DA_execute_shared_weakness_breakout_second_followup_or_prune_mt5_batch"
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
SOURCE_CV_VARIANT_MANIFEST_PATH = source_cv.VARIANT_MANIFEST_PATH
SOURCE_CV_ATTEMPT_MANIFEST_PATH = source_cv.ATTEMPT_MANIFEST_PATH
SOURCE_CV_RUNTIME_CONTRACT_PATH = source_cv.RUNTIME_CONTRACT_PATH
SOURCE_CR_VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
SOURCE_CR_ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
SOURCE_DESIGN_REPORT_PATH = source_design.REPORT_PATH
SOURCE_CV_REPORT_PATH = source_cv.REPORT_PATH

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
SOURCE_REPRODUCTION_RECEIPT_PATH = RUN_ROOT / "source_profile_reproduction_receipt.csv"
FEATURE_ENGINEERING_DIAGNOSTICS_PATH = RUN_ROOT / "feature_engineering_diagnostics.csv"
CONTROL_REJOIN_RECEIPT_PATH = RUN_ROOT / "control_rejoin_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267cz/run267CZ_shared_weakness_second_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessSecondFollowupOrPrune"
PERIOD_LABEL = "historical_2024_tier_a_train_era_stress"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B inputs are materialized; true Tier B fallback "
    "and actual routed total remain outside this run"
)
MATERIALIZATION_BOUNDARY = "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"

ACTIVE_APPEND_CONFIGS = (
    {
        "queue_id": "cy_q02_explosive_combo_cross_period_prune_gate",
        "source_run_id": SOURCE_CV_RUN_ID,
        "source_profile_label": "explosive_shock_state_combo",
        "profile_label": "explosive_second_survival",
        "profile_token": "explosive_second",
        "variant_token": "explosive_second",
        "engineered_feature": "stage267cz_explosive_second_survival_score",
        "aliases": ("s258_stc", "s264_aia", "s264_aih"),
        "model_materialization_type": "augmented_run267CV_explosive_combo_with_second_survival_feature",
        "model_strength": "aggressive_shock_state_without_defensive_filter_stack",
        "known_difference": "adds one second-follow-up explosive survival feature; no calendar hard ban and no repair loop extension",
    },
    {
        "queue_id": "cy_q03_s264_aia_validation_damage_probe",
        "source_run_id": SOURCE_CV_RUN_ID,
        "source_profile_label": "explosive_shock_state_combo",
        "profile_label": "aia_validation_damage_probe",
        "profile_token": "aia_val_damage",
        "variant_token": "aia_val_damage",
        "engineered_feature": "stage267cz_aia_validation_damage_probe_score",
        "aliases": ("s264_aia",),
        "model_materialization_type": "augmented_run267CV_s264_aia_with_validation_damage_probe_feature",
        "model_strength": "oos_anchor_validation_damage_probe_without_oos_only_selection",
        "known_difference": "adds one validation-damage probe feature to s264_aia explosive source; OOS-only headline is not used",
    },
    {
        "queue_id": "cy_q04_aih_final_supply_or_prune",
        "source_run_id": SOURCE_CV_RUN_ID,
        "source_profile_label": "aih_aggressive_supply_repair",
        "profile_label": "aih_final_supply_or_prune",
        "profile_token": "aih_final_supply",
        "variant_token": "aih_final_supply",
        "engineered_feature": "stage267cz_aih_final_supply_or_prune_score",
        "aliases": ("s264_aih",),
        "model_materialization_type": "augmented_run267CV_aih_supply_repair_with_final_supply_feature",
        "model_strength": "single_final_supply_probe_before_prune",
        "known_difference": "adds one final supply-or-prune feature; this is not an open-ended repair branch",
    },
)

CONTROL_COPY_CONFIGS = (
    {
        "queue_id": "cy_q06_control_rejoin_guardrail",
        "source_run_id": SOURCE_CR_RUN_ID,
        "source_profile_label": "state_phase_monday_replacement",
        "profile_label": "control_rejoin_guardrail_identity",
        "profile_token": "control_rejoin",
        "variant_token": "control_rejoin",
        "aliases": ("s264_lc", "s262_lih"),
        "model_materialization_type": "identity_copy_run267CR_control_rejoin_no_new_alpha_feature",
        "model_strength": "control_rejoin_same_period_cost_risk_no_new_alpha_feature",
        "known_difference": "copies the run267CR control feature/model identity into the current run so controls rejoin the next MT5 batch",
    },
)

QUEUE_HOLD_REASONS = {
    "cy_q01_s258_redzone_cross_period_survival": {
        "decision": "held_for_dedicated_adjacent_period_redzone_pack",
        "decision_readable": "held_for_dedicated_adjacent_period_redzone_pack(전용 인접 기간 위험 구역 묶음까지 보류)",
        "why": "이 queue(대기열)는 2023H2/2025H1/2025H2 redzone feature frames(위험 구역 피처 프레임)가 필요하다. run267CZ(267CZ 실행)는 2024-only files(2024년 전용 파일)로 cross-period evidence(확장 기간 근거)를 꾸미지 않는다.",
        "next": "open a narrow redzone cross-period pack if the run267CZ explosive batch leaves s258_stc alive.",
    },
    "cy_q05_feature_reliance_ablation_replacement": {
        "decision": "held_until_p0_survivors_exist",
        "decision_readable": "held_until_p0_survivors_exist(P0 생존 후보가 나온 뒤까지 보류)",
        "why": "Feature ablation/replacement(피처 제거/대체)는 q02/q03/q04에서 survivors(생존 후보)가 나온 뒤에만 의미가 있음; 그렇지 않으면 이미 죽은 branch(분기)만 제거하게 됨.",
        "next": "materialize ablation/replacement for survivors after run267DA/run267DB curve and trade-quality review.",
    },
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


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
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


def configure_materializer() -> None:
    materializer.RUN_NUMBER = RUN_NUMBER
    materializer.RUN_ID = RUN_ID
    materializer.PARENT_RUN_ID = PARENT_RUN_ID
    materializer.SOURCE_MATERIALIZATION_RUN_ID = f"{SOURCE_CV_RUN_ID};{SOURCE_CR_RUN_ID}"
    materializer.STATUS = STATUS
    materializer.JUDGMENT = JUDGMENT
    materializer.NEXT_ACTION = NEXT_ACTION
    materializer.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    materializer.STAGE_ROOT = STAGE_ROOT
    materializer.REVIEWS_ROOT = REVIEWS_ROOT
    materializer.RUN_ROOT = RUN_ROOT
    materializer.FEATURE_ROOT = FEATURE_ROOT
    materializer.VARIANT_ROOT = VARIANT_ROOT
    materializer.MT5_ROOT = MT5_ROOT
    materializer.COMMON_ROOT = COMMON_ROOT
    materializer.EXPLORATION_LABEL = EXPLORATION_LABEL
    materializer.PERIOD_LABEL = PERIOD_LABEL
    materializer.TIER_PAIR_BOUNDARY = TIER_PAIR_BOUNDARY
    materializer.MATERIALIZATION_BOUNDARY = MATERIALIZATION_BOUNDARY
    materializer.compute_engineered_feature = compute_engineered_feature


def component(
    frame: pd.DataFrame,
    column: str,
    transform: str,
    *,
    weight: float,
    feature_name: str,
) -> tuple[pd.Series, dict[str, Any]]:
    return materializer.component(frame, column, transform, weight=weight, feature_name=feature_name)


def rolling_state_pressure(frame: pd.DataFrame, feature_name: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    return materializer.rolling_state_pressure(frame, feature_name)


def compute_engineered_feature(frame: pd.DataFrame, *, mode: str, feature_name: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    if mode == "explosive_second_survival":
        parts = (
            ("stage267cv_explosive_shock_state_combo_score", "raw", 0.24),
            ("stage267cr_state_phase_monday_replacement_score", "raw", 0.14),
            ("stage267cn_shared_weakness_state_interaction_score", "raw", 0.12),
            ("stage267cf_volatility_energy_transition_score", "raw", 0.11),
            ("return_zscore_20", "abs", 0.10),
            ("atr_14_over_atr_50", "raw", 0.09),
            ("gap_percent", "abs", 0.08),
            ("bb_position_20", "abs_center_0_5", 0.05),
        )
        extra_weight = 0.07
    elif mode == "aia_validation_damage_probe":
        parts = (
            ("stage267cv_explosive_shock_state_combo_score", "raw", 0.22),
            ("stage267cr_state_phase_monday_replacement_score", "raw", 0.17),
            ("stage267cf_trend_strength_replacement_score", "raw", 0.13),
            ("atr_14_over_atr_50", "abs_center_1", 0.12),
            ("historical_vol_5_over_20", "abs_center_1", 0.11),
            ("di_spread_14", "abs", 0.09),
            ("return_1_over_atr_14", "negative_pressure", 0.08),
        )
        extra_weight = 0.08
    elif mode == "aih_final_supply_or_prune":
        parts = (
            ("stage267cv_aih_aggressive_supply_repair_score", "raw", 0.26),
            ("stage267cr_aggressive_shock_supply_expansion_score", "raw", 0.18),
            ("stage267cn_aggressive_shock_release_reentry_score", "raw", 0.14),
            ("return_1_over_atr_14", "positive_pressure", 0.12),
            ("close_prev_close_ratio", "abs_center_1", 0.10),
            ("gap_percent", "abs", 0.08),
            ("bb_position_20", "abs_center_0_5", 0.05),
        )
        extra_weight = 0.07
    else:
        raise ValueError(f"unknown feature mode: {mode}")

    score = pd.Series(0.0, index=frame.index, dtype="float64")
    weight_sum = 0.0
    diagnostics: list[dict[str, Any]] = []
    for column, transform, weight in parts:
        scaled, row = component(frame, column, transform, weight=weight, feature_name=feature_name)
        score = score + float(weight) * scaled
        weight_sum += float(weight)
        diagnostics.append(row)
    cluster, cluster_rows = rolling_state_pressure(frame, feature_name)
    score = score + extra_weight * cluster
    weight_sum += extra_weight
    diagnostics.extend(cluster_rows)
    return (score / weight_sum).clip(0.0, 1.0).astype("float64"), diagnostics


def source_variants() -> dict[tuple[str, str], dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_run_id, path in (
        (SOURCE_CV_RUN_ID, SOURCE_CV_VARIANT_MANIFEST_PATH),
        (SOURCE_CR_RUN_ID, SOURCE_CR_VARIANT_MANIFEST_PATH),
    ):
        for row in read_csv(path):
            row = dict(row)
            row["source_run_id"] = source_run_id
            rows.append(row)
    return {
        (row.get("source_run_id", ""), row.get("candidate_alias", ""), row.get("profile_label", "")): row
        for row in rows
        if row.get("source_run_id") and row.get("candidate_alias") and row.get("profile_label")
    }


def source_attempts() -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for path in (SOURCE_CV_ATTEMPT_MANIFEST_PATH, SOURCE_CR_ATTEMPT_MANIFEST_PATH):
        for row in read_csv(path):
            if row.get("variant_id") and row.get("tier"):
                result[(row["variant_id"], row["tier"])] = row
    return result


def build_materialization_plan(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    variants = source_variants()
    rows: list[dict[str, Any]] = []
    order = 0
    for materialization_type, configs in (
        ("append_feature", ACTIVE_APPEND_CONFIGS),
        ("identity_copy", CONTROL_COPY_CONFIGS),
    ):
        for config in configs:
            queue = queue_by_id[str(config["queue_id"])]
            for alias in config["aliases"]:
                key = (str(config["source_run_id"]), alias, str(config["source_profile_label"]))
                if key not in variants:
                    raise KeyError(f"missing source variant for {key}")
                source = variants[key]
                order += 1
                variant_id = f"run267cz_{order:02d}_{alias}_{config['variant_token']}"
                rows.append(
                    {
                        "plan_id": variant_id,
                        "materialization_type": materialization_type,
                        "queue_id": queue["queue_id"],
                        "priority": queue.get("priority"),
                        "workstream": queue.get("workstream"),
                        "candidate_id": source.get("candidate_id"),
                        "candidate_alias": alias,
                        "candidate_role": source.get("candidate_role"),
                        "source_run_id": config["source_run_id"],
                        "source_variant_id": source.get("variant_id"),
                        "source_profile_label": source.get("profile_label"),
                        "source_feature_file": source.get("runtime_feature_file"),
                        "source_model_file": source.get("runtime_model_file"),
                        "source_feature_count": source.get("feature_count"),
                        "profile_label": config["profile_label"],
                        "profile_token": config["profile_token"],
                        "engineered_feature": config.get("engineered_feature", ""),
                        "model_materialization_type": config["model_materialization_type"],
                        "model_strength": config["model_strength"],
                        "known_difference": config["known_difference"],
                        "materialization_decision": "materialize_feature_model_set_ini_inputs",
                        "materialization_boundary": MATERIALIZATION_BOUNDARY,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def sanitize_appended_rows(
    variant: dict[str, Any],
    attempts: list[dict[str, Any]],
    feature: dict[str, Any],
    model: dict[str, Any],
    diagnostics: list[dict[str, Any]],
    reproduction: list[dict[str, Any]],
    contract: dict[str, Any],
    plan: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    contract["shared_contract"] = (
        "US100 M5;2024 historical stress window;RuntimeProbeEA;"
        "run267CV feature order plus one run267CZ engineered feature;EBM score table extension;attempt set/ini identity"
    )
    contract["tier_pair_boundary"] = TIER_PAIR_BOUNDARY
    contract["runtime_claim_boundary"] = CLAIM_BOUNDARY
    contract["source_run_id"] = plan["source_run_id"]
    for row in reproduction:
        row["reproduction_status"] = "source_profile_reused_with_one_added_run267CZ_feature"
        row["effect"] = "source profile remains comparison anchor while run267CZ adds one explicit second follow-up feature"
        row["claim_boundary"] = CLAIM_BOUNDARY
    for row in attempts:
        row["claim_boundary"] = CLAIM_BOUNDARY
        row["source_run_id"] = plan["source_run_id"]
    for row in diagnostics:
        row["source_run_id"] = plan["source_run_id"]
    variant["source_run_id"] = plan["source_run_id"]
    feature["source_run_id"] = plan["source_run_id"]
    model["source_run_id"] = plan["source_run_id"]
    return variant, attempts, feature, model, diagnostics, reproduction, contract


def materialize_identity_copy(
    plan: Mapping[str, Any],
    attempts_by_variant_tier: Mapping[tuple[str, str], Mapping[str, str]],
    *,
    order: int,
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
]:
    alias = str(plan["candidate_alias"])
    variant_id = str(plan["plan_id"])
    profile_label = str(plan["profile_label"])
    profile_token = str(plan["profile_token"])
    source_variant_id = str(plan["source_variant_id"])
    source_feature_path = repo_path(str(plan["source_feature_file"]))
    source_model_path = repo_path(str(plan["source_model_file"]))
    feature_order = materializer.source_feature_order(source_feature_path)
    feature_order_hash = ordered_hash(feature_order)

    frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    feature_path = FEATURE_ROOT / alias / variant_id / f"{variant_id}_features.csv"
    model_path = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"
    io_path(feature_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
    frame.loc[:, ["bar_time_server", *feature_order]].to_csv(
        io_path(feature_path),
        index=False,
        encoding="utf-8",
        lineterminator="\n",
    )
    shutil.copyfile(io_path(source_model_path), io_path(model_path))
    validation = materializer.score_table_extender.validate_score_table(feature_path, model_path, feature_order)

    common_feature_path = f"{COMMON_ROOT}/{alias}/{variant_id}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{variant_id}/models/{model_path.name}"
    common_feature = materializer.copy_to_common(feature_path, common_feature_path, materializer.COMMON_FILES_ROOT_DEFAULT)
    common_model = materializer.copy_to_common(model_path, common_model_path, materializer.COMMON_FILES_ROOT_DEFAULT)

    missing_feature_cells = int(frame.loc[:, feature_order].isna().sum().sum()) if len(frame) else 0
    duplicate_bar_time_rows = int(frame["bar_time_server"].duplicated().sum()) if len(frame) else 0
    feature_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_run_id": plan["source_run_id"],
        "source_variant_id": source_variant_id,
        "source_feature_file": rel(source_feature_path),
        "source_feature_sha256": sha256_file_lf_normalized(source_feature_path),
        "runtime_feature_file": rel(feature_path),
        "runtime_feature_sha256": sha256_file_lf_normalized(feature_path),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "source_feature_count": len(feature_order),
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": feature_order_hash,
        "appended_feature": "",
        "feature_mode": profile_label,
        "feature_min": "",
        "feature_max": "",
        "feature_mean": "",
        "feature_nonzero_rows": "",
        "rows": int(len(frame)),
        "first_bar_time_server": str(frame["bar_time_server"].iloc[0]) if len(frame) else "",
        "last_bar_time_server": str(frame["bar_time_server"].iloc[-1]) if len(frame) else "",
        "duplicate_bar_time_rows": duplicate_bar_time_rows,
        "runtime_missing_feature_cells": missing_feature_cells,
        **validation,
        "materialization_status": "identity_copied_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_run_id": plan["source_run_id"],
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": rel(model_path),
        "runtime_model_sha256": sha256_file_lf_normalized(model_path),
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "appended_feature": "",
        "model_strength": plan["model_strength"],
        "model_materialization_type": plan["model_materialization_type"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    variant_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "source_run_id": plan["source_run_id"],
        "source_variant_id": source_variant_id,
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "source_profile_label": plan["source_profile_label"],
        "model_materialization_type": model_row["model_materialization_type"],
        "runtime_model_file": model_row["runtime_model_file"],
        "runtime_model_sha256": model_row["runtime_model_sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": feature_row["runtime_feature_file"],
        "runtime_feature_sha256": feature_row["runtime_feature_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": feature_order_hash,
        "engineered_features": "",
        "known_difference": plan["known_difference"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_contract = {
        "variant_id": variant_id,
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "source_profile_label": plan["source_profile_label"],
        "source_run_id": plan["source_run_id"],
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;control identity copy;no new alpha feature;attempt set/ini identity",
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "model_backend": "ebm_table",
        "model_materialization_type": model_row["model_materialization_type"],
        "engineered_features": "",
        "known_difference": plan["known_difference"],
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "runtime_claim_boundary": CLAIM_BOUNDARY,
    }

    attempt_rows: list[dict[str, Any]] = []
    reproduction_rows: list[dict[str, Any]] = []
    for tier_index, (tier, role, token) in enumerate(
        (
            ("Tier A", "tier_only_total", "ta"),
            ("Tier A+B", "routed_total_duplicate_boundary", "rt"),
        ),
        start=1,
    ):
        source_attempt = dict(attempts_by_variant_tier[(source_variant_id, tier)])
        source_set_values = materializer.parse_key_values(repo_path(source_attempt["set_path"]))
        source_ini_values = materializer.parse_key_values(repo_path(source_attempt["ini_path"]))
        attempt_name = f"{variant_id}_{token}_2024"
        telemetry = f"{COMMON_ROOT}/{alias}/{variant_id}/telemetry/{attempt_name}_telemetry.csv"
        summary = f"{COMMON_ROOT}/{alias}/{variant_id}/telemetry/{attempt_name}_summary.csv"
        model_id = f"{RUN_ID}_{variant_id}_score_table"
        set_values = dict(source_set_values)
        set_values.update(
            {
                "InpRunId": RUN_ID,
                "InpExplorationLabel": EXPLORATION_LABEL,
                "InpTierLabel": tier,
                "InpPrimaryActiveTier": "tier_a",
                "InpSplitLabel": PERIOD_LABEL,
                "InpModelPath": common_model_path,
                "InpModelId": model_id,
                "InpModelBackend": "ebm_table",
                "InpModelUseCommonFiles": "true",
                "InpFeatureCsvPath": common_feature_path,
                "InpFeatureCount": len(feature_order),
                "InpFeatureCsvUseCommonFiles": "true",
                "InpFeatureRequireTimestampMatch": "true",
                "InpFeatureAllowLatestFallback": "false",
                "InpFeatureStrictHeader": "true",
                "InpFeatureOrderHash": feature_order_hash,
                "InpFallbackEnabled": "false",
                "InpFallbackFeatureCsvPath": common_feature_path,
                "InpFallbackFeatureCount": len(feature_order),
                "InpFallbackModelPath": common_model_path,
                "InpFallbackModelId": f"{model_id}_fallback_disabled",
                "InpFallbackModelBackend": "ebm_table",
                "InpFallbackFeatureOrderHash": feature_order_hash,
                "InpTelemetryCsvPath": telemetry,
                "InpSummaryCsvPath": summary,
                "InpTelemetryUseCommonFiles": "true",
                "InpMagic": 26739000 + order * 10 + tier_index,
            }
        )
        set_payload = materializer.write_set(MT5_ROOT / f"{attempt_name}.set", set_values)
        ini_values = dict(source_ini_values)
        ini_values.update(
            {
                "ExpertParameters": Path(set_payload["path"]).name,
                "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
                "ReplaceReport": 1,
                "ShutdownTerminal": 1,
            }
        )
        ini_payload = materializer.write_ini(MT5_ROOT / f"{attempt_name}.ini", ini_values)
        attempt_rows.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant_id,
                "queue_id": plan["queue_id"],
                "source_run_id": plan["source_run_id"],
                "source_variant_id": source_variant_id,
                "source_attempt_name": source_attempt["attempt_name"],
                "candidate_id": plan["candidate_id"],
                "candidate_alias": alias,
                "candidate_role": plan["candidate_role"],
                "profile_label": profile_label,
                "tier": tier,
                "attempt_role": role,
                "record_view_prefix": f"mt5_{token}_{alias}_{profile_token}",
                "set_path": set_payload["path"],
                "set_sha256": set_payload["sha256"],
                "ini_path": ini_payload["path"],
                "ini_sha256": ini_payload["sha256"],
                "common_telemetry_path": telemetry,
                "common_summary_path": summary,
                "common_feature_path": common_feature_path,
                "common_model_path": common_model_path,
                "tier_pair_boundary": TIER_PAIR_BOUNDARY,
                "execution_status": "execution_pending",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        reproduction_rows.append(
            {
                "queue_id": plan["queue_id"],
                "candidate_alias": alias,
                "source_run_id": plan["source_run_id"],
                "source_profile_label": plan["source_profile_label"],
                "source_variant_id": source_variant_id,
                "source_attempt_name": source_attempt["attempt_name"],
                "tier": tier,
                "source_set_path": source_attempt["set_path"],
                "source_ini_path": source_attempt["ini_path"],
                "source_feature_file": rel(source_feature_path),
                "source_model_file": rel(source_model_path),
                "reproduction_status": "source_control_identity_copied_no_new_alpha_feature",
                "effect": "control candidates rejoin the next MT5 batch without adding a new alpha feature",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    control_receipt = {
        "receipt_id": f"run267cz_control_rejoin_{alias}",
        "candidate_alias": alias,
        "source_run_id": plan["source_run_id"],
        "source_variant_id": source_variant_id,
        "variant_id": variant_id,
        "feature_order_hash": feature_order_hash,
        "new_alpha_feature": "false",
        "decision_use": "keep aggressive rows honest by comparing against defensive/validation-heavy controls",
        "materialization_status": "identity_copied_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return variant_row, attempt_rows, feature_row, model_row, [], reproduction_rows, runtime_contract, control_receipt


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]], plan_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialized_by_queue: dict[str, int] = {}
    for row in plan_rows:
        key = str(row["queue_id"])
        materialized_by_queue[key] = materialized_by_queue.get(key, 0) + 1
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = queue["queue_id"]
        if queue_id in materialized_by_queue:
            decision = "materialized_execution_pending"
            decision_readable = "materialized_execution_pending(물질화 완료, 실행 대기)"
            effect = f"{materialized_by_queue[queue_id]}개 variant rows(변형 행)를 MT5 input attempts(MT5 입력 시도)로 바꿨다."
        else:
            held = QUEUE_HOLD_REASONS.get(queue_id, {})
            decision = str(held.get("decision", "held_for_followup"))
            decision_readable = str(held.get("decision_readable", "held_for_followup(후속까지 보류)"))
            effect = str(held.get("why", "held to avoid widening this materialization beyond executable evidence."))
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "workstream": queue.get("workstream"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "run267CZ_decision": decision,
                "run267CZ_decision_readable": decision_readable,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = queue.get("queue_id", "")
        if queue_id not in QUEUE_HOLD_REASONS:
            continue
        held = QUEUE_HOLD_REASONS[queue_id]
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "hold_status": held["decision"],
                "why_held": held["why"],
                "next_action": held["next"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def experiment_design_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267cz_q02_explosive_second_survival",
            "hypothesis": "Explosive shock-state rows that looked constructive in run267CX should survive one stronger non-calendar shock/loss-shape feature before any Adapter structure is considered.",
            "decision_use": "Decide whether s258_stc, s264_aia, or s264_aih explosive branches deserve MT5 curve review or immediate prune/demotion.",
            "comparison_baseline": "run267CX explosive rows and run267CV source profiles.",
            "control_variables": "US100 M5, 2024 stress window, same cost/risk, feature order anchor, RuntimeProbeEA handoff.",
            "changed_variables": "one run267CZ explosive second-survival feature is appended.",
            "sample_scope": "Tier A and duplicate-boundary Tier A+B 2024 MT5 inputs.",
            "success_criteria": "MT5 review later shows net>2200, PF>=1.35, trades>=450, DD<=22%, and no chron_mid collapse.",
            "failure_criteria": "DD>=28%, chron_mid_net<0, or worst_month_net<-220.",
            "invalid_conditions": "feature order mismatch, missing MT5 report, changed cost/risk, or treating duplicate boundary as true fallback.",
            "stop_conditions": "If two or more explosive rows fail DD/month gates, shrink the explosive branch.",
            "evidence_plan": "run267DA MT5 KPI, reports, trade list, balance/equity curve, month/weekday/session slices.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "receipt_id": "run267cz_q03_aia_validation_damage_probe",
            "hypothesis": "s264_aia OOS anchor strength must survive validation-damage-like pressure and cannot rely on OOS headline numbers only.",
            "decision_use": "Keep or demote s264_aia as OOS anchor observation.",
            "comparison_baseline": "run267CX s264_aia explosive net=1452.57, PF=1.4374, DD=14.63.",
            "control_variables": "same source variant, same cost/risk, same tester contract.",
            "changed_variables": "one validation damage probe feature appended.",
            "sample_scope": "Tier A and duplicate-boundary Tier A+B 2024 MT5 inputs.",
            "success_criteria": "DD<=18%, PF>=1.32, worst_month_net>-160 after MT5 review.",
            "failure_criteria": "DD grows materially or three negative months remain.",
            "invalid_conditions": "OOS-only score read or missing validation-like slice review.",
            "stop_conditions": "Two validation-damage failures lower s264_aia to observation only.",
            "evidence_plan": "run267DA execution followed by curve/time-slice/trade-quality review.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "receipt_id": "run267cz_q04_aih_final_supply_or_prune",
            "hypothesis": "s264_aih supply repair has one final chance to raise trade count without worsening Monday/session holes.",
            "decision_use": "Close or keep the AIH supply branch as a bounded observation.",
            "comparison_baseline": "run267CX aih_aggressive_supply_repair net=1047.25, PF=1.7443, trades=283, Monday=-198.19.",
            "control_variables": "same source profile, same period/cost/risk, no calendar ban.",
            "changed_variables": "one final supply-or-prune feature appended.",
            "sample_scope": "Tier A and duplicate-boundary Tier A+B 2024 MT5 inputs.",
            "success_criteria": "trades>=340, net>=1300, PF>=1.50, DD<=18, Monday net>-140.",
            "failure_criteria": "trades<320, Monday net<-180, or DD>=22.",
            "invalid_conditions": "more than one additional repair attempt or hidden threshold tuning.",
            "stop_conditions": "One failed attempt closes this repair branch.",
            "evidence_plan": "run267DA MT5 output and run267DB curve/trade-quality review.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "receipt_id": "run267cz_q06_control_rejoin_guardrail",
            "hypothesis": "Recent aggressive rows need s264_lc and s262_lih control rejoin so the pool-wide read is not biased toward high-ceiling candidates.",
            "decision_use": "Compare aggressive breakage against defensive/validation-heavy controls.",
            "comparison_baseline": "run267CR state_phase control rows.",
            "control_variables": "no new alpha feature, same 2024 period/cost/risk, same source feature/model identity.",
            "changed_variables": "only run identity and MT5 handoff paths change.",
            "sample_scope": "Tier A and duplicate-boundary Tier A+B 2024 MT5 inputs.",
            "success_criteria": "Controls are less broken in weak slices or explain shared weakness.",
            "failure_criteria": "Controls break in the same month/session with no explanatory value.",
            "invalid_conditions": "claiming pool-wide read while omitting control rows.",
            "stop_conditions": "If controls add no explanatory value twice, keep only failure memory.",
            "evidence_plan": "run267DA MT5 output and run267DB time-slice comparison.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def environment_receipt_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267cz_environment_reproducibility",
            "execution_environment": "Windows local MT5 workspace; Python pipeline materialization; MT5 Strategy Tester execution pending",
            "dependency_surface": "Python pandas; project foundation helpers; run267CR materialization helper; run267CV and run267CR source artifacts; MT5 Common Files handoff",
            "entry_command": f"python {rel(PRODUCER_PATH)}",
            "mt5_execution_status": "execution_pending",
            "common_root": COMMON_ROOT,
            "source_materializations": f"{SOURCE_CV_RUN_ID};{SOURCE_CR_RUN_ID}",
            "reproducibility_judgment": "reproducible_with_project_data_and_common_files_setup",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267cz_feature_frame_integrity",
            "feature_frames": len(feature_rows),
            "rows_min": min((int(row.get("rows", 0)) for row in feature_rows), default=0),
            "rows_max": max((int(row.get("rows", 0)) for row in feature_rows), default=0),
            "duplicate_bar_time_rows_total": sum(int(row.get("duplicate_bar_time_rows", 0)) for row in feature_rows),
            "runtime_missing_feature_cells_total": sum(int(row.get("runtime_missing_feature_cells", 0)) for row in feature_rows),
            "feature_label_boundary": "current/prior closed-bar features only; no future trade result input",
            "integrity_status": "passed" if feature_rows and all(row.get("score_table_validation") == "passed" for row in feature_rows) else "failed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_parity_rows(feature_rows: Sequence[Mapping[str, Any]], model_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    models = {row["variant_id"]: row for row in model_rows}
    rows: list[dict[str, Any]] = []
    for feature in feature_rows:
        model = models[str(feature["variant_id"])]
        rows.append(
            {
                "receipt_id": f"run267cz_runtime_parity_{feature['variant_id']}",
                "variant_id": feature["variant_id"],
                "candidate_alias": feature["candidate_alias"],
                "feature_order_hash": feature["feature_order_hash"],
                "feature_count": feature["feature_count"],
                "model_sha256": model["runtime_model_sha256"],
                "common_feature_path": feature["common_feature_path"],
                "common_model_path": model["common_model_path"],
                "score_table_validation": feature["score_table_validation"],
                "runtime_handoff_status": "set_ini_materialized_execution_pending",
                "parity_boundary": "Python materialization and MT5 handoff are aligned by feature count/order/hash; MT5 runtime reproduction is next run",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "judgment_id": "run267cz_materialization_judgment",
            "result_subject": "run267CZ shared weakness second follow-up/prune materialization(267CZ 공유 약점 2차 후속/가지치기 물질화)",
            "evidence_available": "feature/model/set/ini inputs, manifests, runtime contracts, held queue receipts",
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
        ("materialized_queue_rows_expected", counts["materialized_queue_rows"] == 4, f"materialized_queue_rows={counts['materialized_queue_rows']}"),
        ("variants_materialized", counts["variants"] == 7, f"variants={counts['variants']}"),
        ("attempt_inputs_created", counts["attempts"] == 14, f"attempts={counts['attempts']}"),
        ("p0_explosive_materialized", counts["q02_variants"] == 3, f"q02_variants={counts['q02_variants']}"),
        ("control_rejoin_materialized", counts["control_copy_variants"] == 2, f"control_copy_variants={counts['control_copy_variants']}"),
        ("held_queue_documented", counts["held_rows"] == 2, f"held_rows={counts['held_rows']}"),
        ("score_table_validation_passed", counts["score_table_validation_passed"] == counts["variants"], f"passed={counts['score_table_validation_passed']};variants={counts['variants']}"),
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
    write_csv(SOURCE_REPRODUCTION_RECEIPT_PATH, result["source_profile_reproduction_receipt"])
    write_csv(FEATURE_ENGINEERING_DIAGNOSTICS_PATH, result["feature_engineering_diagnostics"])
    write_csv(CONTROL_REJOIN_RECEIPT_PATH, result["control_rejoin_receipt"])
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
        "source_run_ids": [SOURCE_CV_RUN_ID, SOURCE_CR_RUN_ID, source_design.RUN_ID],
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
    payload = dict(result)
    payload.pop("feature_engineering_diagnostics", None)
    payload["feature_engineering_diagnostics_count"] = len(result["feature_engineering_diagnostics"])
    return payload


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    variant_lines = "\n".join(
        f"| `{row['variant_id']}` | `{row['candidate_alias']}` | `{row['profile_label']}` | `{row['queue_id']}` |"
        for row in result["variant_manifest"]
    )
    queue_lines = "\n".join(
        f"| `{row['queue_id']}` | `{row['run267CZ_decision_readable']}` | {row['effect']} |"
        for row in result["queue_decisions"]
    )
    return f"""# Stage267 Run267CZ Second Follow-up/Prune Materialization(267단계 267CZ 2차 후속/가지치기 물질화)

- status(상태): `{STATUS}`
- variants(변형): `{counts['variants']}`
- attempts(시도): `{counts['attempts']}`
- materialized_queue_rows(물질화 대기열 행): `{counts['materialized_queue_rows']}`
- held_rows(보류 행): `{counts['held_rows']}`
- next_action(다음 행동): `{NEXT_ACTION}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 판독)

run267CZ(267CZ 실행)는 run267CY(267CY 실행)의 queue(대기열)를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꿨다.
Effect(효과): explosive second-survival(폭발형 2차 생존), s264_aia validation damage(검증 손상), s264_aih final supply(최종 공급), control rejoin(대조 재합류)을 다음 실행에서 바로 볼 수 있다.

q01 redzone cross-period(위험 구역 확장 기간)와 q05 ablation/replacement(제거/대체)는 held(보류)다.
Effect(효과): 2024-only(2024년 전용) 파일로 확장 기간 근거를 꾸미지 않고, 생존 후보가 나온 뒤 제거/대체를 붙이게 했다.

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
- held_queue(보류 대기열): `{rel(HELD_QUEUE_PATH)}`
- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`

## Boundary(경계)

run267CZ(267CZ 실행)는 materialization(물질화)이다. MT5(MetaTrader 5, 메타트레이더5) 실행 결과, balance/equity curve(잔액/평가금 곡선), selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비)는 주장하지 않는다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifact_specs = (
        ("stage267_run267CZ_producer", "producer_script", PRODUCER_PATH, "Builds run267CZ materialization."),
        ("stage267_run267CZ_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267CZ_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decisions."),
        ("stage267_run267CZ_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267CZ_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267CZ_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267CZ_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267CZ_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267CZ_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267CZ_source_reproduction", "source_reproduction_receipt", SOURCE_REPRODUCTION_RECEIPT_PATH, "Source reproduction receipt."),
        ("stage267_run267CZ_feature_diagnostics", "feature_engineering_diagnostics", FEATURE_ENGINEERING_DIAGNOSTICS_PATH, "Feature diagnostics."),
        ("stage267_run267CZ_control_rejoin", "control_rejoin_receipt", CONTROL_REJOIN_RECEIPT_PATH, "Control rejoin receipt."),
        ("stage267_run267CZ_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267CZ_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267CZ_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267CZ_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267CZ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267CZ_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267CZ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267CZ_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267CZ_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267CZ_report", "review_report", REPORT_PATH, "User-facing report."),
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
        "row_id": "stage267_run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_second_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B attempt inputs; true fallback not claimed",
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
        "tier_scope": "Tier A and duplicate-boundary Tier A+B attempt inputs; true fallback not claimed",
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
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def update_current_documents(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization"
        f"(267CZ 공유 약점 2차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267CZ_summary(267CZ 요약): run267CY(267CY 실행)의 materialization queue(물질화 대기열)를 "
        f"variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개로 바꿨다. "
        "Effect(효과): 폭발형 2차 생존, s264_aia 검증 손상, s264_aih 최종 공급, s264_lc/s262_lih 대조 재합류를 다음 MT5 실행 입력으로 만들었다."
    )
    block = "\n".join(
        [
            "Run267CZ(267CZ 실행)는 run267CY(267CY 실행)의 2차 follow-up/prune queue(후속/가지치기 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개를 만들고, q01 cross-period(확장 기간)와 q05 ablation/replacement(제거/대체)는 held(보류)로 남겼다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_materialization`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267CY_shared_weakness_breakout_second_followup_or_prune_design.md", report_line)
            text = append_after_contains(text, "run267CY_summary", summary_line)
            text = append_block_once(text, "Run267CZ(267CZ 실행)는 run267CY", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CY_shared_weakness_breakout_second_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267CZ(267CZ 실행)는 run267CY", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267CY_shared_weakness_breakout_second_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267CZ(267CZ 실행)는 run267CY", block)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CZ(267CZ 실행) shared weakness breakout second follow-up/prune materialization"
        f"(공유 약점 2차 후속/가지치기 물질화) `{STATUS}`. Effect(효과): run267CY(267CY 실행)의 queue(대기열)를 "
        f"variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개로 나눴고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_line)
    workspace = workspace.replace(f"next_action: {source_design.NEXT_ACTION}", f"next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CY_shared_weakness_breakout_second_followup_or_prune_design_report_path",
        f"  run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}",
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
        SOURCE_CV_VARIANT_MANIFEST_PATH,
        SOURCE_CV_ATTEMPT_MANIFEST_PATH,
        SOURCE_CV_RUNTIME_CONTRACT_PATH,
        SOURCE_CR_VARIANT_MANIFEST_PATH,
        SOURCE_CR_ATTEMPT_MANIFEST_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    configure_materializer()
    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    plan_rows = build_materialization_plan(queue_rows)
    attempts_by_variant_tier = source_attempts()

    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []
    reproduction_rows: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    control_receipts: list[dict[str, Any]] = []

    for order, plan in enumerate(plan_rows, start=1):
        if plan["materialization_type"] == "append_feature":
            variant, attempts, feature, model, diagnostics, reproduction, contract = materializer.materialize_variant(
                plan,
                attempts_by_variant_tier,
                order=order,
            )
            variant, attempts, feature, model, diagnostics, reproduction, contract = sanitize_appended_rows(
                variant,
                attempts,
                feature,
                model,
                diagnostics,
                reproduction,
                contract,
                plan,
            )
        else:
            variant, attempts, feature, model, diagnostics, reproduction, contract, control_receipt = materialize_identity_copy(
                plan,
                attempts_by_variant_tier,
                order=order,
            )
            control_receipts.append(control_receipt)
        variant_rows.append(variant)
        attempt_rows.extend(attempts)
        feature_rows.append(feature)
        model_rows.append(model)
        diagnostic_rows.extend(diagnostics)
        reproduction_rows.extend(reproduction)
        contracts.append(contract)

    held_rows = held_queue_rows(queue_rows)
    queue_decisions = queue_decision_rows(queue_rows, plan_rows)
    materialized_queue_ids = {row["queue_id"] for row in plan_rows}
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len(materialized_queue_ids),
        "held_rows": len(held_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "diagnostics": len(diagnostic_rows),
        "source_reproduction_receipts": len(reproduction_rows),
        "control_rejoin_receipts": len(control_receipts),
        "score_table_validation_passed": sum(1 for row in feature_rows if row.get("score_table_validation") == "passed"),
        "q02_variants": sum(1 for row in variant_rows if row.get("queue_id") == "cy_q02_explosive_combo_cross_period_prune_gate"),
        "control_copy_variants": sum(1 for row in variant_rows if row.get("queue_id") == "cy_q06_control_rejoin_guardrail"),
    }
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_cv_run_id": SOURCE_CV_RUN_ID,
        "source_cr_run_id": SOURCE_CR_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "counts": counts,
        "materialization_plan": plan_rows,
        "queue_decisions": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": contracts,
        "held_queue": held_rows,
        "source_profile_reproduction_receipt": reproduction_rows,
        "feature_engineering_diagnostics": diagnostic_rows,
        "control_rejoin_receipt": control_receipts,
        "experiment_design_receipt": experiment_design_rows(),
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
            "source_cv_variant_manifest": rel(SOURCE_CV_VARIANT_MANIFEST_PATH),
            "source_cv_attempt_manifest": rel(SOURCE_CV_ATTEMPT_MANIFEST_PATH),
            "source_cv_runtime_contract": rel(SOURCE_CV_RUNTIME_CONTRACT_PATH),
            "source_cr_variant_manifest": rel(SOURCE_CR_VARIANT_MANIFEST_PATH),
            "source_cr_attempt_manifest": rel(SOURCE_CR_ATTEMPT_MANIFEST_PATH),
            "source_design_report": rel(SOURCE_DESIGN_REPORT_PATH),
            "source_cv_report": rel(SOURCE_CV_REPORT_PATH),
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
            "source_profile_reproduction_receipt": rel(SOURCE_REPRODUCTION_RECEIPT_PATH),
            "feature_engineering_diagnostics": rel(FEATURE_ENGINEERING_DIAGNOSTICS_PATH),
            "control_rejoin_receipt": rel(CONTROL_REJOIN_RECEIPT_PATH),
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
                "q02_variants": counts["q02_variants"],
                "control_copy_variants": counts["control_copy_variants"],
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
