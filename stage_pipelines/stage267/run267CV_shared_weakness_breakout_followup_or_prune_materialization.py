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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267CR_shared_weakness_breakout_followup_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267CU_shared_weakness_breakout_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CV"
RUN_ID = "run267CV_stage267_shared_weakness_breakout_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267CV_shared_weakness_breakout_followup_or_prune_materialized_execution_pending"
JUDGMENT = "shared_weakness_breakout_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267CW_execute_shared_weakness_breakout_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_followup_or_prune_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_FEATURE_BLUEPRINT_PATH = source_design.FEATURE_BLUEPRINT_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_REPORT_PATH = source_design.REPORT_PATH
SOURCE_MATERIALIZATION_REPORT_PATH = source_materialization.REPORT_PATH

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
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CV_shared_weakness_breakout_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CV_shared_weakness_breakout_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267cv/run267CV_shared_weakness_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessFollowupOrPrune"
PERIOD_LABEL = "historical_2024_tier_a_train_era_stress"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B inputs are materialized; true Tier B fallback "
    "and actual routed total remain outside this run"
)
MATERIALIZATION_BOUNDARY = "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"

ACTIVE_VARIANT_CONFIGS = (
    {
        "queue_id": "cu_q02_s258_redzone_monday_dd_pressure",
        "source_profile_label": "redzone_stress_blast",
        "profile_label": "redzone_monday_dd_pressure",
        "profile_token": "redzone_monday_dd",
        "variant_token": "redzone_monday_dd",
        "engineered_feature": "stage267cv_redzone_monday_dd_pressure_score",
        "aliases": ("s258_stc",),
        "model_materialization_type": "augmented_run267CR_score_table_with_redzone_monday_dd_pressure_feature",
        "model_strength": "aggressive_redzone_monday_dd_pressure_without_calendar_ban",
        "known_difference": "adds one noncalendar loss-shape/Monday-DD pressure feature on top of run267CR redzone stress; no literal weekday ban",
    },
    {
        "queue_id": "cu_q04_aih_aggressive_supply_repair_or_prune",
        "source_profile_label": "aggressive_shock_supply_expansion",
        "profile_label": "aih_aggressive_supply_repair",
        "profile_token": "aih_supply_repair",
        "variant_token": "aih_supply_repair",
        "engineered_feature": "stage267cv_aih_aggressive_supply_repair_score",
        "aliases": ("s264_aih",),
        "model_materialization_type": "augmented_run267CR_score_table_with_supply_repair_feature",
        "model_strength": "bounded_supply_expansion_for_high_pf_thin_trade_surface",
        "known_difference": "adds bounded supply repair feature on top of run267CR aggressive supply expansion; maximum two repair attempts in design boundary",
    },
    {
        "queue_id": "cu_q05_explosive_shock_state_combo",
        "source_profile_label_by_alias": {
            "s264_aih": "state_phase_monday_replacement",
            "s264_aia": "state_phase_monday_replacement",
            "s258_stc": "redzone_stress_blast",
        },
        "profile_label": "explosive_shock_state_combo",
        "profile_token": "explosive_combo",
        "variant_token": "explosive_combo",
        "engineered_feature": "stage267cv_explosive_shock_state_combo_score",
        "aliases": ("s264_aih", "s264_aia", "s258_stc"),
        "model_materialization_type": "augmented_run267CR_score_table_with_explosive_shock_state_combo_feature",
        "model_strength": "high_ceiling_shock_state_combo_without_defensive_filter_stack",
        "known_difference": "adds one explosive shock-state combo feature; one attempt per candidate before prune/fail memory",
    },
)

QUEUE_HOLD_REASONS = {
    "cu_q01_balanced_pair_cross_period_pressure": {
        "decision": "held_for_true_adjacent_period_state_phase_feature_frames",
        "why": "2023H2/2025H1/2025H2 state_phase feature frames are required; run267CV does not fake cross-period pressure from 2024 files.",
        "next": "materialize a narrow adjacent-period state_phase pack if run267CV/run267CW leaves this branch alive.",
    },
    "cu_q03_control_guardrail_retest": {
        "decision": "held_until_p0_outputs_to_avoid_duplicate_retest",
        "why": "Control and guardrail retest should consume finalized P0 outputs, not duplicate the already-executed run267CS controls.",
        "next": "reopen after P0 aggressive/state inputs are executed and reviewed.",
    },
    "cu_q06_feature_reliance_ablation_replacement_audit": {
        "decision": "held_until_p0_p1_survivors_define_ablation_scope",
        "why": "Feature ablation/replacement audit is meaningful only after run267CV P0/P1 candidates survive execution and curve review.",
        "next": "materialize ablation/replacement only for candidates still alive after run267CW/run267CX.",
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


def component(frame: pd.DataFrame, column: str, transform: str, *, weight: float, feature_name: str) -> tuple[pd.Series, dict[str, Any]]:
    return source_materialization.component(frame, column, transform, weight=weight, feature_name=feature_name)


def rolling_state_pressure(frame: pd.DataFrame, feature_name: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    return source_materialization.rolling_state_pressure(frame, feature_name)


def compute_engineered_feature(frame: pd.DataFrame, *, mode: str, feature_name: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    if mode == "redzone_monday_dd_pressure":
        parts = (
            ("stage267cr_redzone_stress_blast_score", "raw", 0.30),
            ("stage267cn_shared_weakness_state_interaction_score", "raw", 0.16),
            ("stage267cf_range_pressure_asymmetry_score", "raw", 0.14),
            ("return_1_over_atr_14", "negative_pressure", 0.12),
            ("atr_14_over_atr_50", "raw", 0.10),
            ("historical_vol_5_over_20", "raw", 0.08),
            ("bb_position_20", "abs_center_0_5", 0.05),
        )
        extra_weight = 0.05
    elif mode == "aih_aggressive_supply_repair":
        parts = (
            ("stage267cr_aggressive_shock_supply_expansion_score", "raw", 0.28),
            ("stage267cn_aggressive_shock_release_reentry_score", "raw", 0.16),
            ("stage267cf_trend_strength_replacement_score", "raw", 0.14),
            ("return_1_over_atr_14", "positive_pressure", 0.12),
            ("close_prev_close_ratio", "abs_center_1", 0.10),
            ("gap_percent", "abs", 0.08),
            ("bb_position_20", "abs_center_0_5", 0.06),
        )
        extra_weight = 0.06
    elif mode == "explosive_shock_state_combo":
        parts = (
            ("stage267cr_state_phase_monday_replacement_score", "raw", 0.20),
            ("stage267cr_redzone_stress_blast_score", "raw", 0.18),
            ("stage267cr_aggressive_shock_supply_expansion_score", "raw", 0.16),
            ("stage267cn_shared_weakness_state_interaction_score", "raw", 0.12),
            ("stage267cn_aggressive_shock_release_reentry_score", "raw", 0.10),
            ("stage267cf_volatility_energy_transition_score", "raw", 0.09),
            ("return_zscore_20", "abs", 0.07),
            ("gap_percent", "abs", 0.04),
        )
        extra_weight = 0.04
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


def configure_source_materializer() -> None:
    source_materialization.RUN_NUMBER = RUN_NUMBER
    source_materialization.RUN_ID = RUN_ID
    source_materialization.PARENT_RUN_ID = PARENT_RUN_ID
    source_materialization.SOURCE_MATERIALIZATION_RUN_ID = SOURCE_MATERIALIZATION_RUN_ID
    source_materialization.STATUS = STATUS
    source_materialization.JUDGMENT = JUDGMENT
    source_materialization.NEXT_ACTION = NEXT_ACTION
    source_materialization.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    source_materialization.STAGE_ROOT = STAGE_ROOT
    source_materialization.REVIEWS_ROOT = REVIEWS_ROOT
    source_materialization.RUN_ROOT = RUN_ROOT
    source_materialization.FEATURE_ROOT = FEATURE_ROOT
    source_materialization.VARIANT_ROOT = VARIANT_ROOT
    source_materialization.MT5_ROOT = MT5_ROOT
    source_materialization.SOURCE_VARIANT_MANIFEST_PATH = SOURCE_VARIANT_MANIFEST_PATH
    source_materialization.SOURCE_ATTEMPT_MANIFEST_PATH = SOURCE_ATTEMPT_MANIFEST_PATH
    source_materialization.SOURCE_RUNTIME_CONTRACT_PATH = SOURCE_RUNTIME_CONTRACT_PATH
    source_materialization.COMMON_ROOT = COMMON_ROOT
    source_materialization.EXPLORATION_LABEL = EXPLORATION_LABEL
    source_materialization.PERIOD_LABEL = PERIOD_LABEL
    source_materialization.TIER_PAIR_BOUNDARY = TIER_PAIR_BOUNDARY
    source_materialization.MATERIALIZATION_BOUNDARY = MATERIALIZATION_BOUNDARY
    source_materialization.compute_engineered_feature = compute_engineered_feature


def source_variants_by_alias_profile() -> dict[tuple[str, str], dict[str, str]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    return {
        (row.get("candidate_alias", ""), row.get("profile_label", "")): row
        for row in rows
        if row.get("candidate_alias") and row.get("profile_label")
    }


def source_attempts_by_variant_tier() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["variant_id"], row["tier"]): row
        for row in read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
        if row.get("variant_id") and row.get("tier")
    }


def materialization_plan_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    source_variants = source_variants_by_alias_profile()
    rows: list[dict[str, Any]] = []
    order = 0
    for config in ACTIVE_VARIANT_CONFIGS:
        queue = queue_by_id[str(config["queue_id"])]
        for alias in config["aliases"]:
            source_profile = str(config.get("source_profile_label_by_alias", {}).get(alias, config.get("source_profile_label")))
            source_key = (alias, source_profile)
            if source_key not in source_variants:
                raise KeyError(f"missing source variant for {source_key}")
            source = source_variants[source_key]
            order += 1
            variant_id = f"run267cv_{order:02d}_{alias}_{config['variant_token']}"
            rows.append(
                {
                    "plan_id": variant_id,
                    "queue_id": queue["queue_id"],
                    "priority": queue.get("priority"),
                    "candidate_id": source.get("candidate_id"),
                    "candidate_alias": alias,
                    "candidate_role": source.get("candidate_role"),
                    "source_variant_id": source.get("variant_id"),
                    "source_profile_label": source_profile,
                    "source_feature_file": source.get("runtime_feature_file"),
                    "source_model_file": source.get("runtime_model_file"),
                    "source_feature_count": source.get("feature_count"),
                    "profile_label": config["profile_label"],
                    "profile_token": config["profile_token"],
                    "engineered_feature": config["engineered_feature"],
                    "model_materialization_type": config["model_materialization_type"],
                    "model_strength": config["model_strength"],
                    "known_difference": config["known_difference"],
                    "materialization_decision": "materialize_feature_model_set_ini_inputs",
                    "materialization_boundary": MATERIALIZATION_BOUNDARY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def sanitize_returned_rows(
    variant: dict[str, Any],
    attempts: list[dict[str, Any]],
    feature: dict[str, Any],
    model: dict[str, Any],
    diagnostics: list[dict[str, Any]],
    reproduction: list[dict[str, Any]],
    contract: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    contract["shared_contract"] = (
        "US100 M5;2024 historical stress window;RuntimeProbeEA;"
        "run267CR feature order plus one run267CV engineered feature;EBM score table extension;attempt set/ini identity"
    )
    contract["tier_pair_boundary"] = TIER_PAIR_BOUNDARY
    contract["runtime_claim_boundary"] = CLAIM_BOUNDARY
    for row in reproduction:
        row["reproduction_status"] = "source_run267CR_profile_reused_with_one_added_run267CV_feature"
        row["effect"] = "source run267CR profile remains comparison anchor while run267CV adds one explicit follow-up/prune feature"
        row["claim_boundary"] = CLAIM_BOUNDARY
    for row in attempts:
        row["claim_boundary"] = CLAIM_BOUNDARY
    variant["source_run_id"] = SOURCE_MATERIALIZATION_RUN_ID
    return variant, attempts, feature, model, diagnostics, reproduction, contract


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]], plan_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialized_by_queue: dict[str, int] = {}
    for row in plan_rows:
        materialized_by_queue[str(row["queue_id"])] = materialized_by_queue.get(str(row["queue_id"]), 0) + 1
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = queue["queue_id"]
        if queue_id in materialized_by_queue:
            decision = "materialized_execution_pending"
            effect = f"{materialized_by_queue[queue_id]} variant rows were converted into feature/model/set/ini inputs."
        else:
            held = QUEUE_HOLD_REASONS.get(queue_id, {})
            decision = str(held.get("decision", "held_for_followup"))
            effect = str(held.get("why", "held to avoid widening this materialization beyond executable source surfaces."))
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "workstream": queue.get("workstream"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "run267CV_decision": decision,
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


def environment_receipt_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267cv_environment_reproducibility",
            "execution_environment": source_materialization.EXECUTION_ENVIRONMENT,
            "dependency_surface": "Python pandas; project foundation helpers; run267CR materialization helpers; MT5 Common Files handoff",
            "entry_command": f"python {rel(PRODUCER_PATH)}",
            "mt5_execution_status": "execution_pending",
            "common_root": COMMON_ROOT,
            "source_materialization": SOURCE_MATERIALIZATION_RUN_ID,
            "reproducibility_judgment": "reproducible_with_project_data_and_common_files_setup",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267cv_feature_frame_integrity",
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
                "receipt_id": f"run267cv_runtime_parity_{feature['variant_id']}",
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


def result_judgment_rows(counts: Mapping[str, int]) -> list[dict[str, Any]]:
    return [
        {
            "judgment_id": "run267cv_materialization_judgment",
            "result_subject": "run267CV shared weakness follow-up/prune materialization(267CV 공유 약점 후속/가지치기 물질화)",
            "evidence_available": "feature/model/set/ini inputs, manifests, runtime contracts, held queue receipts",
            "evidence_missing": "MT5 execution, balance/equity curve, time-slice KPI, trade quality, adjacent-period state_phase frames",
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


def gate_audit_rows(counts: Mapping[str, int]) -> list[dict[str, Any]]:
    checks = (
        ("source_design_queue_available", counts["queue_rows"] == 6, f"queue_rows={counts['queue_rows']}"),
        ("materialized_queue_rows_expected", counts["materialized_queue_rows"] == 3, f"materialized_queue_rows={counts['materialized_queue_rows']}"),
        ("executable_variants_materialized", counts["variants"] == 5, f"variants={counts['variants']}"),
        ("attempt_inputs_created", counts["attempts"] == 10, f"attempts={counts['attempts']}"),
        ("score_table_validation_passed", counts["score_table_validation_passed"] == counts["variants"], f"passed={counts['score_table_validation_passed']};variants={counts['variants']}"),
        ("held_queue_documented", counts["held_rows"] == 3, f"held_rows={counts['held_rows']}"),
        ("aggressive_materialized", counts["aggressive_variants"] >= 4, f"aggressive_variants={counts['aggressive_variants']}"),
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


def run_manifest_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
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
        "lineage_judgment": "connected_materialization_with_boundary(경계 포함 물질화 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_result_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "counts": result["counts"],
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": result["sources"],
        "outputs": result["outputs"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267CV Shared Weakness Follow-up/Prune Materialization(267단계 267CV 공유 약점 후속/가지치기 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- held_queue_rows(보류 대기열 행): `{counts['held_rows']}`",
        f"- score_table_validation_passed(점수표 검증 통과): `{counts['score_table_validation_passed']}`",
        f"- aggressive_variants(공격형 변형): `{counts['aggressive_variants']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267CV(267CV 실행)는 run267CU(267CU 실행)의 materialization queue(물질화 대기열) 중 지금 바로 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들 수 있는 축만 물질화했다.",
        "효과: redzone Monday/DD pressure(위험 구역 월요일/손실폭 압박), explosive shock-state combo(폭발형 충격-상태 조합), s264_aih supply repair(s264_aih 공급 수리)를 `.set/.ini`, feature CSV(피처 CSV), model CSV(모델 CSV)로 만들었다.",
        "",
        "cross-period state_phase(확장 기간 상태 구간)와 feature ablation/replacement(피처 제거/대체)는 아직 가짜로 만들지 않았다.",
        "효과: 기간별 feature frame(피처 프레임)이나 P0/P1 실행 결과가 필요한 작업은 held(보류)로 기록되어, 다음 연구가 허술한 근거로 이어지지 않는다.",
        "",
        "## Materialized Variants(물질화된 변형)",
        "",
        "| variant(변형) | candidate(후보) | profile(프로필) | source_profile(원천 프로필) | feature_count(피처 수) |",
        "|---|---|---|---|---:|",
    ]
    for row in result["variant_manifest"]:
        lines.append(
            f"| `{row['variant_id']}` | `{row['candidate_alias']}` | `{row['profile_label']}` | "
            f"`{row['source_profile_label']}` | {row['feature_count']} |"
        )
    lines.extend(
        [
            "",
            "## Queue Decisions(대기열 판단)",
            "",
            "| queue(대기열) | decision(판단) | effect(효과) |",
            "|---|---|---|",
        ]
    )
    for row in result["queue_decisions"]:
        lines.append(f"| `{row['queue_id']}` | {row['run267CV_decision']} | {row['effect']} |")
    lines.extend(
        [
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
            f"- held_queue(보류 대기열): `{rel(HELD_QUEUE_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Boundary(경계)",
            "",
            "run267CV(267CV 실행)는 execution pending(실행 대기) 물질화다. 아직 MT5 실행, balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질) 판정은 없다.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


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
    write_csv(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, result["environment_reproducibility_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, run_manifest_payload(result))
    write_json(LINEAGE_PATH, lineage_payload(result))
    write_json(REVIEW_RESULT_PATH, review_result_payload(result))
    write_md(REPORT_PATH, report_markdown(result))


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifacts = [
        ("stage267_run267CV_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH),
        ("stage267_run267CV_queue_decision", "queue_decision", QUEUE_DECISION_PATH),
        ("stage267_run267CV_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH),
        ("stage267_run267CV_model_manifest", "model_manifest", MODEL_MANIFEST_PATH),
        ("stage267_run267CV_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH),
        ("stage267_run267CV_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH),
        ("stage267_run267CV_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH),
        ("stage267_run267CV_held_queue", "held_queue", HELD_QUEUE_PATH),
        ("stage267_run267CV_source_reproduction", "source_reproduction_receipt", SOURCE_REPRODUCTION_RECEIPT_PATH),
        ("stage267_run267CV_feature_engineering_diagnostics", "feature_engineering_diagnostics", FEATURE_ENGINEERING_DIAGNOSTICS_PATH),
        ("stage267_run267CV_environment_receipt", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH),
        ("stage267_run267CV_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH),
        ("stage267_run267CV_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH),
        ("stage267_run267CV_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH),
        ("stage267_run267CV_gate_audit", "gate_audit", GATE_AUDIT_PATH),
        ("stage267_run267CV_run_manifest", "run_manifest", RUN_MANIFEST_PATH),
        ("stage267_run267CV_lineage", "lineage", LINEAGE_PATH),
        ("stage267_run267CV_review_result", "review_result", REVIEW_RESULT_PATH),
        ("stage267_run267CV_report", "review_report", REPORT_PATH),
    ]
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": f"Run267CV {artifact_type}; materialization only; no candidate selection.",
        }
        for artifact_id, artifact_type, path in artifacts
    ]
    for row in result["feature_frame_manifest"]:
        rows.append(
            {
                "artifact_id": f"stage267_run267CV_feature_{row['variant_id']}",
                "artifact_type": "runtime_feature_frame",
                "path": row["runtime_feature_file"],
                "sha256": row["runtime_feature_sha256"],
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Run267CV feature frame for {row['candidate_alias']}.",
            }
        )
    for row in result["model_manifest"]:
        rows.append(
            {
                "artifact_id": f"stage267_run267CV_model_{row['variant_id']}",
                "artifact_type": "runtime_model_table",
                "path": row["runtime_model_file"],
                "sha256": row["runtime_model_sha256"],
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Run267CV model table for {row['candidate_alias']}.",
            }
        )
    for row in result["attempt_manifest"]:
        rows.extend(
            [
                {
                    "artifact_id": f"stage267_run267CV_set_{row['attempt_name']}",
                    "artifact_type": "mt5_set",
                    "path": row["set_path"],
                    "sha256": row["set_sha256"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": f"Run267CV set file for {row['attempt_name']}.",
                },
                {
                    "artifact_id": f"stage267_run267CV_ini_{row['attempt_name']}",
                    "artifact_type": "mt5_ini",
                    "path": row["ini_path"],
                    "sha256": row["ini_sha256"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": f"Run267CV tester ini for {row['attempt_name']}.",
                },
            ]
        )
    return rows


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    notes = (
        f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']};"
        f"aggressive_variants={counts['aggressive_variants']};next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CV_shared_weakness_breakout_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B MT5 inputs; true Tier B fallback not claimed",
        "scoreboard": "feature_model_set_ini_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_execution_pending_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_shared_weakness_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "feature_model_set_ini_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B MT5 inputs; true Tier B fallback outside claim",
        "kpi_scope": "materialization_counts_only_execution_pending",
        "scoreboard_lane": "shared_weakness_followup_or_prune_materialization",
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


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267CV_shared_weakness_breakout_followup_or_prune_materialization"
        f"(267CV 공유 약점 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267CV_summary(267CV 요약): run267CU(267CU 실행)의 대기열 중 실행 가능한 축을 "
        f"variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개로 물질화했다. "
        f"held queue(보류 대기열)는 `{counts['held_rows']}`개다. Effect(효과): redzone Monday/DD pressure(위험 구역 월요일/손실폭 압박), "
        "explosive shock-state combo(폭발형 충격-상태 조합), s264_aih supply repair(s264_aih 공급 수리)를 다음 MT5 실행 입력으로 만들었다."
    )
    block = "\n".join(
        [
            "Run267CV(267CV 실행)는 run267CU(267CU 실행)의 follow-up/prune queue(후속/가지치기 대기열)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개를 만들고, cross-period state_phase(확장 기간 상태 구간)와 feature ablation/replacement(피처 제거/대체)는 held(보류)로 기록했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_followup_or_prune_materialization`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267CU_shared_weakness_breakout_followup_or_prune_design.md", report_line)
            text = append_after_contains(text, "run267CU_shared_weakness_breakout_followup_or_prune_design", summary_line)
            text = append_block_once(text, "Run267CV(267CV 실행)는 run267CU", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CU_shared_weakness_breakout_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267CV(267CV 실행)는 run267CU", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267CU_shared_weakness_breakout_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267CV(267CV 실행)는 run267CU", block)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CV(267CV 실행) shared weakness breakout follow-up/prune materialization"
        f"(공유 약점 돌파 후속/가지치기 물질화) `{STATUS}`. Effect(효과): run267CU(267CU 실행)의 "
        f"materialization queue(물질화 대기열)를 variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, "
        f"held rows(보류 행) `{counts['held_rows']}`개로 나눴고, selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_line)
    workspace = workspace.replace(f"next_action: {source_design.NEXT_ACTION}", f"next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CU_shared_weakness_breakout_followup_or_prune_design_report_path",
        f"  run267CV_shared_weakness_breakout_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}",
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
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_ATTEMPT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    configure_source_materializer()
    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    plan_rows = materialization_plan_rows(queue_rows)
    source_attempts = source_attempts_by_variant_tier()

    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []
    reproduction_rows: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    for order, plan in enumerate(plan_rows, start=1):
        variant, attempts, feature, model, diagnostics, reproduction, contract = source_materialization.materialize_variant(
            plan,
            source_attempts,
            order=order,
        )
        variant, attempts, feature, model, diagnostics, reproduction, contract = sanitize_returned_rows(
            variant,
            attempts,
            feature,
            model,
            diagnostics,
            reproduction,
            contract,
        )
        variant_rows.append(variant)
        attempt_rows.extend(attempts)
        feature_rows.append(feature)
        model_rows.append(model)
        diagnostic_rows.extend(diagnostics)
        reproduction_rows.extend(reproduction)
        contracts.append(contract)

    held_rows = held_queue_rows(queue_rows)
    queue_decisions = queue_decision_rows(queue_rows, plan_rows)
    aggressive_queue_ids = {
        "cu_q02_s258_redzone_monday_dd_pressure",
        "cu_q04_aih_aggressive_supply_repair_or_prune",
        "cu_q05_explosive_shock_state_combo",
    }
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len({row["queue_id"] for row in plan_rows}),
        "held_rows": len(held_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "diagnostics": len(diagnostic_rows),
        "source_reproduction_receipts": len(reproduction_rows),
        "score_table_validation_passed": sum(1 for row in feature_rows if row.get("score_table_validation") == "passed"),
        "aggressive_variants": sum(1 for row in variant_rows if row.get("queue_id") in aggressive_queue_ids),
    }
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
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
            "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "source_design_report": rel(SOURCE_REPORT_PATH),
            "source_materialization_report": rel(SOURCE_MATERIALIZATION_REPORT_PATH),
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
    update_current_docs(result)
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
                "aggressive_variants": counts["aggressive_variants"],
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
