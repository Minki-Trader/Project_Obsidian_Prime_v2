from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
    attempt_payload,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267AO_pool_wide_state_feature_engineering_materialization as source_materialization
from stage_pipelines.stage267 import run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch as source_design
from stage_pipelines.stage267 import run267W_true_internal_ablation_score_table_materialization as source_tables


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267AS"
RUN_ID = "run267AS_stage267_pool_wide_state_feature_engineering_followup_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267AS_pool_wide_state_feature_engineering_followup_materialized_execution_pending"
JUDGMENT = "pool_wide_state_feature_engineering_followup_materialized_execution_pending_no_candidate_selection"
NEXT_ACTION = "run267AT_execute_pool_wide_state_feature_engineering_followup_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_followup_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_AR_QUEUE_PATH = source_design.NEXT_EXPERIMENT_QUEUE_PATH
SOURCE_PROFILE_DECISION_PATH = source_design.PROFILE_DECISION_PATH
SOURCE_CANDIDATE_DECISION_PATH = source_design.CANDIDATE_DECISION_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_AR_REPORT_PATH = source_design.REPORT_PATH
SOURCE_AO_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_AO_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_AO_REPORT_PATH = source_materialization.REPORT_PATH

PRESSURE_DESIGN_PATH = RUN_ROOT / "state_feature_followup_pressure_design.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "followup_materialization_queue.csv"
FOLLOWUP_VARIANT_MANIFEST_PATH = RUN_ROOT / "followup_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
MODEL_PRESSURE_AUDIT_PATH = RUN_ROOT / "model_pressure_audit.csv"
CANDIDATE_ROLE_PRESSURE_PATH = RUN_ROOT / "candidate_role_pressure_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AS_pool_wide_state_feature_engineering_followup_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AS_pool_wide_state_feature_engineering_followup_materialization.py")

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
CSV_MODEL_COLUMNS = source_materialization.CSV_MODEL_COLUMNS
SOURCE_SIGNAL_COLUMN = input_probe.SOURCE_SIGNAL_COLUMN
COMMON_ROOT = "OPV2/s267as/run267AS_state_feature_followup"
PERIOD_LABEL = input_probe.PERIOD_LABEL
MODEL_MATERIALIZATION_TYPE = "research_score_table_pool_wide_state_feature_followup_pressure_v2"

PRESSURE_TERMS: dict[str, tuple[tuple[float, float, float], ...]] = {
    "core_range_resilience_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.025, 0.055, -0.025),
        (-0.055, 0.120, -0.055),
        (-0.090, 0.180, -0.090),
    ),
    "core_volatility_resilience_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.030, 0.065, -0.030),
        (-0.060, 0.135, -0.060),
        (-0.100, 0.200, -0.100),
    ),
    "oos_anchor_dd_resilience_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.020, 0.050, -0.020),
        (-0.050, 0.105, -0.050),
        (-0.080, 0.160, -0.080),
    ),
    "oos_anchor_shock_resilience_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.025, 0.060, -0.025),
        (-0.060, 0.130, -0.060),
        (-0.095, 0.190, -0.095),
    ),
    "stress_challenger_volatility_prune_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.045, 0.095, -0.045),
        (-0.090, 0.190, -0.090),
        (-0.145, 0.290, -0.145),
    ),
    "stress_challenger_trend_prune_pressure_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.040, 0.090, -0.040),
        (-0.085, 0.180, -0.085),
        (-0.135, 0.270, -0.135),
    ),
    "defensive_control_volatility_audit_v1": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.030, 0.065, -0.030),
        (-0.060, 0.135, -0.060),
        (-0.100, 0.200, -0.100),
    ),
    "validation_control_volatility_audit_v1": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.030, 0.065, -0.030),
        (-0.060, 0.135, -0.060),
        (-0.100, 0.200, -0.100),
    ),
}

PRESSURE_PLAN = (
    {
        "queue_id": "run267AS_p01_s264_aih_range_pressure",
        "source_queue_id": "run267AS_q01_noncalendar_slice_pressure_matrix",
        "priority": "P0",
        "candidate_alias": "s264_aih",
        "state_profile": "range_expansion_pressure",
        "followup_profile": "core_range_resilience_pressure_v2",
        "pressure_group": "core_challenger_slice_pressure",
        "reason": "best core challenger profile needs December and Monday pressure without calendar filter",
    },
    {
        "queue_id": "run267AS_p02_s264_aih_volatility_pressure",
        "source_queue_id": "run267AS_q01_noncalendar_slice_pressure_matrix",
        "priority": "P0",
        "candidate_alias": "s264_aih",
        "state_profile": "volatility_regime_expansion",
        "followup_profile": "core_volatility_resilience_pressure_v2",
        "pressure_group": "core_challenger_slice_pressure",
        "reason": "second core challenger profile checks volatility-state robustness rather than one lucky range profile",
    },
    {
        "queue_id": "run267AS_p03_s264_aia_range_pressure",
        "source_queue_id": "run267AS_q01_noncalendar_slice_pressure_matrix",
        "priority": "P0",
        "candidate_alias": "s264_aia",
        "state_profile": "range_expansion_pressure",
        "followup_profile": "oos_anchor_dd_resilience_pressure_v2",
        "pressure_group": "oos_anchor_watch_gate",
        "reason": "OOS anchor keeps watch status only if range pressure reduces weak slices without DD damage",
    },
    {
        "queue_id": "run267AS_p04_s264_aia_shock_pressure",
        "source_queue_id": "run267AS_q01_noncalendar_slice_pressure_matrix",
        "priority": "P0",
        "candidate_alias": "s264_aia",
        "state_profile": "return_shock_absorption",
        "followup_profile": "oos_anchor_shock_resilience_pressure_v2",
        "pressure_group": "oos_anchor_watch_gate",
        "reason": "return-shock axis tests whether the OOS anchor survives a similar noncalendar meaning shift",
    },
    {
        "queue_id": "run267AS_p05_s258_stc_volatility_pressure",
        "source_queue_id": "run267AS_q01_noncalendar_slice_pressure_matrix",
        "priority": "P0",
        "candidate_alias": "s258_stc",
        "state_profile": "volatility_regime_expansion",
        "followup_profile": "stress_challenger_volatility_prune_pressure_v2",
        "pressure_group": "stress_challenger_prune_or_rescue",
        "reason": "stress challenger headline strength must survive deeper volatility-state pressure",
    },
    {
        "queue_id": "run267AS_p06_s258_stc_trend_pressure",
        "source_queue_id": "run267AS_q01_noncalendar_slice_pressure_matrix",
        "priority": "P0",
        "candidate_alias": "s258_stc",
        "state_profile": "trend_strength_disagreement",
        "followup_profile": "stress_challenger_trend_prune_pressure_v2",
        "pressure_group": "stress_challenger_prune_or_rescue",
        "reason": "trend-strength replacement axis checks whether stress performance is indicator-specific",
    },
    {
        "queue_id": "run267AS_p07_s264_lc_control_volatility_audit",
        "source_queue_id": "run267AS_q03_defensive_validation_control_audit",
        "priority": "P1",
        "candidate_alias": "s264_lc",
        "state_profile": "volatility_regime_expansion",
        "followup_profile": "defensive_control_volatility_audit_v1",
        "pressure_group": "defensive_control_audit",
        "reason": "defensive control separates candidate-specific improvement from general score-table pressure",
    },
    {
        "queue_id": "run267AS_p08_s262_lih_control_volatility_audit",
        "source_queue_id": "run267AS_q03_defensive_validation_control_audit",
        "priority": "P1",
        "candidate_alias": "s262_lih",
        "state_profile": "volatility_regime_expansion",
        "followup_profile": "validation_control_volatility_audit_v1",
        "pressure_group": "validation_control_audit",
        "reason": "validation-heavy control checks whether validation stability survives the same pressure family",
    },
)


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


def safe_token(value: str, limit: int = 80) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return token[:limit] or "item"


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_runtime_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, text: str) -> None:
    write_text(path, text)


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
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def terms_text(terms: Sequence[Sequence[float]]) -> str:
    return ";".join("/".join(f"{value:.3f}" for value in row) for row in terms)


def require_inputs() -> None:
    required = [
        SOURCE_AR_QUEUE_PATH,
        SOURCE_PROFILE_DECISION_PATH,
        SOURCE_CANDIDATE_DECISION_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_AO_VARIANT_MANIFEST_PATH,
        SOURCE_AO_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def source_variants_by_alias_profile() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("state_profile", "")): row
        for row in read_csv(SOURCE_AO_VARIANT_MANIFEST_PATH)
        if row.get("candidate_alias") and row.get("state_profile")
    }


def source_contracts_by_alias_profile() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("state_profile", "")): row
        for row in read_csv(SOURCE_AO_RUNTIME_CONTRACT_PATH)
        if row.get("candidate_alias") and row.get("state_profile")
    }


def profile_decisions_by_alias_profile() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("state_profile", "")): row
        for row in read_csv(SOURCE_PROFILE_DECISION_PATH)
        if row.get("candidate_alias") and row.get("state_profile")
    }


def candidate_decisions_by_alias() -> dict[str, dict[str, str]]:
    return {
        row.get("candidate_alias", ""): row
        for row in read_csv(SOURCE_CANDIDATE_DECISION_PATH)
        if row.get("candidate_alias")
    }


def source_queue_by_id() -> dict[str, dict[str, str]]:
    return {
        row.get("queue_id", ""): row
        for row in read_csv(SOURCE_AR_QUEUE_PATH)
        if row.get("queue_id")
    }


def build_pressure_design() -> list[dict[str, Any]]:
    profile_decisions = profile_decisions_by_alias_profile()
    candidate_decisions = candidate_decisions_by_alias()
    source_queues = source_queue_by_id()
    source_variants = source_variants_by_alias_profile()
    rows: list[dict[str, Any]] = []
    for plan in PRESSURE_PLAN:
        alias = str(plan["candidate_alias"])
        state_profile = str(plan["state_profile"])
        source_queue = source_queues.get(str(plan["source_queue_id"]), {})
        profile = profile_decisions.get((alias, state_profile), {})
        candidate = candidate_decisions.get(alias, {})
        source_variant = source_variants.get((alias, state_profile), {})
        rows.append(
            {
                "queue_id": plan["queue_id"],
                "source_queue_id": plan["source_queue_id"],
                "priority": plan["priority"],
                "workstream": source_queue.get("workstream"),
                "candidate_alias": alias,
                "candidate_id": candidate.get("candidate_id") or source_variant.get("candidate_id"),
                "candidate_role": candidate.get("candidate_role") or source_variant.get("candidate_role"),
                "state_profile": state_profile,
                "source_test_id": source_variant.get("source_test_id") or profile.get("source_test_id"),
                "source_run267AO_queue_id": source_variant.get("queue_id"),
                "followup_profile": plan["followup_profile"],
                "pressure_group": plan["pressure_group"],
                "pressure_terms": terms_text(PRESSURE_TERMS[str(plan["followup_profile"])]),
                "source_net_profit": profile.get("net_profit"),
                "source_profit_factor": profile.get("profit_factor"),
                "source_trade_count": profile.get("trade_count"),
                "source_equity_drawdown_percent": profile.get("equity_drawdown_percent"),
                "source_worst_month": profile.get("worst_month"),
                "source_worst_month_net": profile.get("worst_month_net"),
                "source_worst_slice_axis": profile.get("worst_slice_axis"),
                "source_worst_slice_bucket": profile.get("worst_slice_bucket"),
                "source_worst_slice_net": profile.get("worst_slice_net"),
                "source_profile_decision": profile.get("profile_decision"),
                "candidate_decision": candidate.get("decision_label"),
                "reason": plan["reason"],
                "materialization_status": "ready_for_score_table_materialization"
                if source_variant
                else "blocked_missing_run267AO_source_variant",
                "success_criteria": source_queue.get("success_criteria"),
                "failure_criteria": source_queue.get("failure_criteria"),
                "invalid_conditions": source_queue.get("invalid_conditions"),
                "stop_conditions": source_queue.get("stop_conditions"),
                "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
            }
        )
    return rows


def count_feature_rows(path: Path) -> dict[str, Any]:
    rows = 0
    signal_rows = 0
    missing_cells = 0
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        feature_order = [column for column in (reader.fieldnames or []) if column != "bar_time_server"]
        for row in reader:
            rows += 1
            signal_rows += 1 if as_float(row.get(SOURCE_SIGNAL_COLUMN), 0.0) != 0.0 else 0
            missing_cells += sum(1 for column in feature_order if str(row.get(column, "")).strip() == "")
    return {
        "rows": rows,
        "signal_rows": signal_rows,
        "feature_order": feature_order,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "missing_feature_cells": missing_cells,
    }


def copy_runtime_feature(source: Path, destination: Path) -> dict[str, Any]:
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    io_path(destination).write_bytes(io_path(source).read_bytes())
    meta = count_feature_rows(destination)
    meta.update({"runtime_feature_file": rel(destination), "runtime_feature_sha256": sha256_file_lf_normalized(destination)})
    return meta


def write_pressure_model(source: Path, destination: Path, state_feature_index: int, followup_profile: str) -> dict[str, Any]:
    terms = PRESSURE_TERMS[followup_profile]
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    output: list[dict[str, Any]] = []
    source_terms: list[tuple[float, float, float]] = []
    changed_rows = 0
    score_rows = 0
    neutral_bins_preserved = True
    cut_rows = 0
    for row in rows:
        current = {column: row.get(column, "") for column in CSV_MODEL_COLUMNS}
        feature_index = as_int(current.get("feature_index"), -1)
        record_type = current.get("record_type")
        if record_type == "cut" and feature_index == state_feature_index:
            cut_rows += 1
        if record_type == "score" and feature_index == state_feature_index:
            item_index = as_int(current.get("item_index"), -1)
            if item_index < 0 or item_index >= len(terms):
                raise RuntimeError(f"unexpected state score item index {item_index} in {source}")
            old = (
                as_float(current.get("score_short")),
                as_float(current.get("score_flat")),
                as_float(current.get("score_long")),
            )
            source_terms.append(old)
            new = terms[item_index]
            current["score_short"] = f"{new[0]:.17g}"
            current["score_flat"] = f"{new[1]:.17g}"
            current["score_long"] = f"{new[2]:.17g}"
            if old != new:
                changed_rows += 1
            if item_index in {0, 1} and any(abs(value) > 1.0e-12 for value in new):
                neutral_bins_preserved = False
            score_rows += 1
        output.append(current)

    if score_rows != len(terms):
        raise RuntimeError(f"state score row count mismatch for {source}: {score_rows} != {len(terms)}")
    if cut_rows != len(source_materialization.STATE_FEATURE_CUTS):
        raise RuntimeError(f"state cut row count mismatch for {source}: {cut_rows}")

    write_runtime_csv(destination, output, CSV_MODEL_COLUMNS)
    return {
        "source_runtime_model_file": rel(source),
        "runtime_model_file": rel(destination),
        "runtime_model_sha256": sha256_file_lf_normalized(destination),
        "followup_profile": followup_profile,
        "source_terms": terms_text(source_terms),
        "pressure_terms": terms_text(terms),
        "state_score_rows": score_rows,
        "state_cut_rows": cut_rows,
        "changed_state_score_rows": changed_rows,
        "neutral_bins_preserved": neutral_bins_preserved,
        "only_state_score_terms_changed": True,
    }


def materialize_variant(
    queue_row: Mapping[str, Any],
    source_variant: Mapping[str, str],
    source_contract: Mapping[str, str],
    spec: Any,
    index: int,
) -> dict[str, Any]:
    alias = str(queue_row["candidate_alias"])
    state_profile = str(queue_row["state_profile"])
    source_test_id = str(queue_row["source_test_id"])
    queue_id = str(queue_row["queue_id"])
    followup_profile = str(queue_row["followup_profile"])
    queue_token = safe_token(queue_id, 72)
    profile_token = safe_token(f"{state_profile}_{followup_profile}", 64)
    local_root = VARIANT_ROOT / alias / queue_token
    feature_path = local_root / "features" / f"{alias}_{profile_token}_features.csv"
    model_path = local_root / "models" / f"{alias}_{profile_token}_model.csv"

    feature_meta = copy_runtime_feature(repo_path(str(source_variant["runtime_feature_file"])), feature_path)
    feature_order = list(feature_meta["feature_order"])
    state_feature_index = as_int(source_variant.get("state_feature_index"), feature_meta["feature_count"] - 1)
    model_meta = write_pressure_model(
        repo_path(str(source_variant["runtime_model_file"])),
        model_path,
        state_feature_index,
        followup_profile,
    )

    common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    _full_order, _rank_column, gate_column = source_tables.candidate_full_feature_order(spec)
    attempts: list[dict[str, Any]] = []
    for role_index, (tier, attempt_role, prefix, token) in enumerate(
        (
            (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{safe_token(state_profile, 24)}_as", "ta"),
            (input_probe.mt5.TIER_AB, "routed_total_duplicate_boundary", f"mt5_rt_{alias}_{safe_token(state_profile, 24)}_as", "rt"),
        ),
        start=1,
    ):
        magic = 26735000 + index * 100 + role_index
        payload = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=267,
            exploration_label=f"stage267_StateFeatureFollowup__{safe_token(followup_profile, 32)}",
            attempt_name=f"{queue_token}_{token}_2024",
            tier=tier,
            split=PERIOD_LABEL,
            model_path=common_model_path,
            model_id=f"{RUN_ID}_{alias}_{safe_token(state_profile, 32)}_{safe_token(followup_profile, 32)}_v1",
            model_backend="ebm_table",
            feature_path=common_feature_path,
            feature_count=feature_meta["feature_count"],
            feature_order_hash=feature_meta["feature_order_hash"],
            short_threshold=as_float(source_contract.get("short_threshold"), spec.variant.short_threshold),
            long_threshold=as_float(source_contract.get("long_threshold"), spec.variant.long_threshold),
            min_margin=as_float(source_contract.get("min_margin"), 0.0),
            invert_signal=False,
            from_date="2024.01.02",
            to_date="2025.01.01",
            primary_active_tier="tier_a",
            attempt_role=attempt_role,
            record_view_prefix=prefix,
            max_hold_bars=as_int(source_contract.get("max_hold_bars"), spec.variant.max_hold_bars),
            common_root=f"{COMMON_ROOT}/{alias}/{queue_token}",
            fallback_enabled=False,
            close_on_flat_signal=str(source_contract.get("close_on_flat_signal", spec.variant.close_on_flat_signal)).lower() == "true",
            reverse_on_opposite_signal=str(source_contract.get("reverse_on_opposite_signal", spec.variant.reverse_on_opposite_signal)).lower() == "true",
            close_only_on_opposite_signal=str(source_contract.get("close_only_on_opposite_signal", spec.variant.close_only_on_opposite_signal)).lower() == "true",
            extra_set_values=source_tables.extra_set_for_feature_order(spec, feature_order, gate_column, magic),
        )
        payload.update(
            {
                "queue_id": queue_id,
                "candidate_id": queue_row.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": queue_row.get("candidate_role"),
                "source_test_id": source_test_id,
                "state_profile": state_profile,
                "followup_profile": followup_profile,
                "pressure_group": queue_row.get("pressure_group"),
                "source_run267AO_queue_id": queue_row.get("source_run267AO_queue_id"),
                "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                "execution_status": "not_executed",
            }
        )
        attempts.append(payload)

    variant = {
        "queue_id": queue_id,
        "source_queue_id": queue_row.get("source_queue_id"),
        "priority": queue_row.get("priority"),
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": source_test_id,
        "source_run267AO_queue_id": queue_row.get("source_run267AO_queue_id"),
        "state_profile": state_profile,
        "state_feature": source_variant.get("state_feature"),
        "followup_profile": followup_profile,
        "pressure_group": queue_row.get("pressure_group"),
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "source_variant_manifest": rel(SOURCE_AO_VARIANT_MANIFEST_PATH),
        "source_runtime_feature_file": source_variant.get("runtime_feature_file"),
        "runtime_feature_file": feature_meta["runtime_feature_file"],
        "runtime_feature_sha256": feature_meta["runtime_feature_sha256"],
        "source_runtime_model_file": model_meta["source_runtime_model_file"],
        "runtime_model_file": model_meta["runtime_model_file"],
        "runtime_model_sha256": model_meta["runtime_model_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "feature_count": feature_meta["feature_count"],
        "feature_order": ";".join(feature_order),
        "feature_order_hash": feature_meta["feature_order_hash"],
        "state_feature_index": state_feature_index,
        "runtime_rows": feature_meta["rows"],
        "signal_rows": feature_meta["signal_rows"],
        "missing_feature_cells": feature_meta["missing_feature_cells"],
        "source_state_terms": model_meta["source_terms"],
        "pressure_terms": model_meta["pressure_terms"],
        "neutral_bins_preserved": model_meta["neutral_bins_preserved"],
        "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
    }
    contract = {
        "queue_id": queue_id,
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": source_test_id,
        "state_profile": state_profile,
        "followup_profile": followup_profile,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;run267AO feature order;state-feature follow-up pressure score-table terms;attempt set/ini identity",
        "feature_count": feature_meta["feature_count"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "short_threshold": as_float(source_contract.get("short_threshold"), spec.variant.short_threshold),
        "long_threshold": as_float(source_contract.get("long_threshold"), spec.variant.long_threshold),
        "min_margin": as_float(source_contract.get("min_margin"), 0.0),
        "max_hold_bars": as_int(source_contract.get("max_hold_bars"), spec.variant.max_hold_bars),
        "known_difference": "uses run267AO runtime features and changes only the existing state feature score-table terms; no retraining and no literal weekday/month filter",
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }
    audit = {
        "queue_id": queue_id,
        "candidate_alias": alias,
        "source_test_id": source_test_id,
        "state_profile": state_profile,
        "followup_profile": followup_profile,
        "source_model_file": model_meta["source_runtime_model_file"],
        "runtime_model_file": model_meta["runtime_model_file"],
        "state_feature_index": state_feature_index,
        "source_state_terms": model_meta["source_terms"],
        "pressure_terms": model_meta["pressure_terms"],
        "state_cut_rows": model_meta["state_cut_rows"],
        "state_score_rows": model_meta["state_score_rows"],
        "changed_state_score_rows": model_meta["changed_state_score_rows"],
        "only_state_score_terms_changed": model_meta["only_state_score_terms_changed"],
        "neutral_bins_preserved": model_meta["neutral_bins_preserved"],
        "audit_read": "pass_state_terms_only"
        if model_meta["neutral_bins_preserved"] and model_meta["only_state_score_terms_changed"]
        else "invalid",
    }
    if audit["audit_read"] != "pass_state_terms_only":
        raise RuntimeError(f"pressure model audit failed for {queue_id}: {audit}")
    return {"variant": variant, "contract": contract, "audit": audit, "attempts": attempts, "feature_path": feature_path, "model_path": model_path}


def build_candidate_role_pressure_matrix(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialized_by_alias: dict[str, list[str]] = {}
    for row in queue_rows:
        if row.get("materialization_status") == "ready_for_score_table_materialization":
            materialized_by_alias.setdefault(str(row.get("candidate_alias")), []).append(str(row.get("state_profile")))
    rows: list[dict[str, Any]] = []
    for alias, candidate in candidate_decisions_by_alias().items():
        materialized = materialized_by_alias.get(alias, [])
        if alias == "s264_aih":
            effect = "materialize_core_challenger_pressure_not_selection"
        elif alias == "s264_aia":
            effect = "materialize_oos_anchor_watch_gate_not_selection"
        elif alias == "s258_stc":
            effect = "materialize_stress_challenger_prune_or_rescue_pressure"
        elif alias in {"s264_lc", "s262_lih"}:
            effect = "materialize_control_audit_only"
        else:
            effect = "not_materialized"
        rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate.get("candidate_id"),
                "candidate_role": candidate.get("candidate_role"),
                "source_decision_label": candidate.get("decision_label"),
                "priority": candidate.get("priority"),
                "best_profile": candidate.get("best_profile"),
                "deep_hole_count": candidate.get("deep_hole_count"),
                "worst_month_net_min": candidate.get("worst_month_net_min"),
                "worst_slice_net_min": candidate.get("worst_slice_net_min"),
                "run267AS_materialized_profiles": ";".join(materialized),
                "run267AS_materialized_variant_count": len(materialized),
                "run267AS_decision_effect": effect,
                "prune_boundary": candidate.get("prune_boundary"),
                "reopen_condition": candidate.get("reopen_condition"),
                "do_not_claim": "no_selected_candidate_no_ONNX_no_goal_achieve",
            }
        )
    return rows


def build_failure_memory() -> list[dict[str, Any]]:
    rows = [dict(row) for row in read_csv(SOURCE_FAILURE_MEMORY_PATH)]
    rows.extend(
        [
            {
                "memory_id": "run267AS_m01_pressure_materialization_not_selection",
                "pattern": "followup_pressure_is_execution_input_not_candidate_selection(후속 압박은 실행 입력이지 후보 선택이 아님)",
                "evidence": "run267AS materializes pressure terms only; MT5 execution and curve review remain missing",
                "affected_scope": "all_run267AS_variants",
                "do_not_repeat": "do_not_promote_or_ONNX_from_materialization_manifest",
                "salvage_angle": "execute run267AT and review curve/time-slice/trade-quality before any branch watch upgrade",
                "reopen_condition": "run267AT reduces Monday and 2024-12 holes without trade count collapse",
                "boundary": "materialization_only_no_candidate_selection",
            },
            {
                "memory_id": "run267AS_m02_no_single_calendar_repair_guard",
                "pattern": "calendar_slice_is_evaluation_gate_not_entry_filter(달력 구간은 평가 게이트이지 진입 필터가 아님)",
                "evidence": "run267AR q05 blocks single Monday or December threshold tuning",
                "affected_scope": "Monday;2024-12;all_candidates",
                "do_not_repeat": "do_not_add_literal_weekday_or_month_filter_to_repair_the_named_hole",
                "salvage_angle": "use noncalendar volatility/trend/range/shock state pressure and then test slices",
                "reopen_condition": "structural state pressure improves weak slices in MT5 without direct calendar leakage",
                "boundary": "anti_bottleneck_guardrail",
            },
            {
                "memory_id": "run267AS_m03_p0_pressure_loop_limit",
                "pattern": "same_pressure_branch_must_not_extend_past_next_review_if_holes_persist(같은 압박 분기는 다음 검토 뒤 구멍이 남으면 늘리지 않음)",
                "evidence": "user goal limits deep repair loops; run267AR q01/q02 require prune or redirect after pressure",
                "affected_scope": "s264_aih;s264_aia;s258_stc",
                "do_not_repeat": "do_not_spend_more_stages_on_the_same_state_terms_if_run267AT_review_still_has_deep_holes",
                "salvage_angle": "pivot to new feature structure, adapter structure, or model family if pressure fails",
                "reopen_condition": "new independent evidence changes the failure shape rather than tuning one month or one weekday",
                "boundary": "bounded_repair_loop_guard",
            },
        ]
    )
    return rows


def build_experiment_design_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "hypothesis", "value": "run267AQ headline-positive candidates may fail because state-feature score terms are too mild, so role-specific noncalendar pressure can test whether weak slices reduce without calendar filters"},
        {"field": "decision_use", "value": "create run267AT MT5 attempt inputs only; no candidate selection and no ONNX readiness claim"},
        {"field": "comparison_baseline", "value": "run267AO state feature score tables plus run267AQ balance/time-slice/trade-quality review and run267AR follow-up queue"},
        {"field": "control_variables", "value": "same 2024 period; same five-candidate pool roles; same run267AO feature order; same thresholds; same RuntimeProbeEA"},
        {"field": "changed_variables", "value": "state-feature score-table terms by candidate role and profile; no retraining; no literal weekday/month filters"},
        {"field": "sample_scope", "value": "Tier A and Tier A+B duplicate-boundary 2024 historical runtime attempts planned"},
        {"field": "success_criteria", "value": "future run267AT review must preserve trade count and reduce Monday/2024-12 holes without DD worsening"},
        {"field": "failure_criteria", "value": "headline improves while deep slices remain, trade count thins, DD worsens, or controls move identically to challengers"},
        {"field": "invalid_conditions", "value": "literal calendar filter; feature order mismatch; missing MT5 report; Tier A+B duplicate boundary called real fallback"},
        {"field": "stop_conditions", "value": "if run267AT keeps same deep holes, stop this pressure loop and redirect rather than extending the same repair"},
        {"field": "evidence_plan", "value": "pressure_design;materialization_queue;variant_manifest;runtime_contract;attempt_manifest;model_pressure_audit;future_MT5_KPI;future_curve_time_slice_trade_quality_review"},
        {"field": "required_gate_coverage", "value": "experiment_design_schema;artifact_lineage_connected;runtime_parity_boundary;result_claim_guard"},
    ]


def build_data_integrity_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "data_source", "value": f"{rel(SOURCE_AR_QUEUE_PATH)} and {rel(SOURCE_AO_VARIANT_MANIFEST_PATH)}"},
        {"field": "time_axis", "value": "bar_time_server from run267AO runtime feature files; MT5 test window stays 2024.01.02 through 2025.01.01"},
        {"field": "sample_scope", "value": "US100 M5 2024 historical stress window; run267AS creates 8 follow-up pressure variants"},
        {"field": "missing_or_duplicate_check", "value": f"variant_feature_missing_cells={sum(as_int(row.get('missing_feature_cells')) for row in result['followup_variant_manifest'])};ready_queue_rows={result['ready_queue_rows']}/{result['queue_rows']}"},
        {"field": "feature_label_boundary", "value": "no MT5 PnL becomes a label; model is not retrained; only pre-existing state feature score terms are changed"},
        {"field": "split_boundary", "value": "materialization-only; execution and KPI review remain pending run267AT"},
        {"field": "leakage_risk", "value": "weak-slice evidence influenced follow-up pressure, so next run must be read as exploratory pressure, not selection proof"},
        {"field": "data_hash_or_identity", "value": f"run_manifest={rel(RUN_MANIFEST_PATH)}"},
        {"field": "integrity_judgment", "value": "usable_with_boundary" if result["ready_queue_rows"] == result["queue_rows"] else "inconclusive"},
    ]


def build_runtime_parity_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "runtime_feature_order", "value": "run267AO feature_order copied unchanged and feature_order_hash recorded per variant"},
        {"field": "score_table_change", "value": "only existing state feature score rows are changed; cut rows and feature count are unchanged"},
        {"field": "model_pressure_audit", "value": f"{result['model_pressure_audit_pass_count']}/{result['variant_count']}"},
        {"field": "MT5_execution_status", "value": "not_executed_materialization_only"},
        {"field": "runtime_claim_boundary", "value": "no runtime authority; no ONNX; no candidate selection"},
    ]


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"variants={result['variant_count']};attempts={result['attempt_count']};pressure_audit_pass={result['model_pressure_audit_pass_count']}/{result['variant_count']};candidate_role_rows={result['candidate_role_pressure_rows']}",
            "evidence_missing": "MT5_execution;trade_list_review;balance_equity_curve;time_slice_KPI;trade_quality_after_pressure",
            "judgment_label": JUDGMENT,
            "claim_boundary": "materialization_only_no_candidate_selection_no_onnx_no_goal_achieve_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 기존 후보 5개의 후속 압박 실험을 실제 MT5 실행 대기 입력으로 만든 상태다. 아직 성과 판정은 아니다.",
        }
    ]


def build_materialization() -> dict[str, Any]:
    require_inputs()
    pressure_design = build_pressure_design()
    ready_rows = [row for row in pressure_design if row.get("materialization_status") == "ready_for_score_table_materialization"]
    source_variants = source_variants_by_alias_profile()
    source_contracts = source_contracts_by_alias_profile()
    specs = specs_by_alias()

    variants: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    dynamic_artifacts: list[dict[str, Any]] = []
    for index, queue_row in enumerate(ready_rows, start=1):
        key = (str(queue_row["candidate_alias"]), str(queue_row["state_profile"]))
        source_variant = source_variants.get(key)
        source_contract = source_contracts.get(key)
        if source_variant is None or source_contract is None:
            raise KeyError(f"missing run267AO source variant/contract for {key}")
        item = materialize_variant(queue_row, source_variant, source_contract, specs[str(queue_row["candidate_alias"])], index)
        variants.append(item["variant"])
        contracts.append(item["contract"])
        audits.append(item["audit"])
        attempts.extend(item["attempts"])
        dynamic_artifacts.extend(
            [
                {
                    "artifact_id": f"stage267_run267AS_{safe_token(str(queue_row['queue_id']), 64)}_runtime_feature",
                    "artifact_type": "runtime_feature_csv",
                    "path": rel(item["feature_path"]),
                    "notes": f"Run267AS runtime feature CSV for {queue_row['queue_id']}.",
                },
                {
                    "artifact_id": f"stage267_run267AS_{safe_token(str(queue_row['queue_id']), 64)}_runtime_model",
                    "artifact_type": "runtime_model_csv",
                    "path": rel(item["model_path"]),
                    "notes": f"Run267AS follow-up pressure score table CSV for {queue_row['queue_id']}.",
                },
            ]
        )

    candidate_role_pressure = build_candidate_role_pressure_matrix(pressure_design)
    failure_memory = build_failure_memory()
    created_at = utc_now()
    result: dict[str, Any] = {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "queue_rows": len(pressure_design),
        "ready_queue_rows": len(ready_rows),
        "candidate_count": len({row.get("candidate_alias") for row in pressure_design}),
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "model_pressure_audit_pass_count": sum(1 for row in audits if row.get("audit_read") == "pass_state_terms_only"),
        "candidate_role_pressure_rows": len(candidate_role_pressure),
        "failure_memory_rows": len(failure_memory),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "pressure_design": pressure_design,
        "followup_variant_manifest": variants,
        "runtime_contract": contracts,
        "model_pressure_audit": audits,
        "attempts": attempts,
        "candidate_role_pressure": candidate_role_pressure,
        "failure_memory": failure_memory,
        "dynamic_artifacts": dynamic_artifacts,
        "inputs": {
            "run267AR_queue": rel(SOURCE_AR_QUEUE_PATH),
            "run267AR_profile_decision": rel(SOURCE_PROFILE_DECISION_PATH),
            "run267AR_candidate_decision": rel(SOURCE_CANDIDATE_DECISION_PATH),
            "run267AR_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "run267AO_variant_manifest": rel(SOURCE_AO_VARIANT_MANIFEST_PATH),
            "run267AO_runtime_contract": rel(SOURCE_AO_RUNTIME_CONTRACT_PATH),
            "run267AR_report": rel(SOURCE_AR_REPORT_PATH),
            "run267AO_report": rel(SOURCE_AO_REPORT_PATH),
        },
        "outputs": {
            "pressure_design": rel(PRESSURE_DESIGN_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "followup_variant_manifest": rel(FOLLOWUP_VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "model_pressure_audit": rel(MODEL_PRESSURE_AUDIT_PATH),
            "candidate_role_pressure": rel(CANDIDATE_ROLE_PRESSURE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": {},
    }
    result["experiment_design_receipt"] = build_experiment_design_receipt(result)
    result["data_integrity_receipt"] = build_data_integrity_receipt(result)
    result["runtime_parity_receipt"] = build_runtime_parity_receipt(result)
    result["result_judgment"] = build_result_judgment(result)
    return result


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "source_test_id": attempt.get("source_test_id"),
                "state_profile": attempt.get("state_profile"),
                "followup_profile": attempt.get("followup_profile"),
                "pressure_group": attempt.get("pressure_group"),
                "tier": attempt.get("tier"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def write_outputs(result: Mapping[str, Any]) -> None:
    pressure_columns = (
        "queue_id",
        "source_queue_id",
        "priority",
        "workstream",
        "candidate_alias",
        "candidate_id",
        "candidate_role",
        "state_profile",
        "source_test_id",
        "source_run267AO_queue_id",
        "followup_profile",
        "pressure_group",
        "pressure_terms",
        "source_net_profit",
        "source_profit_factor",
        "source_trade_count",
        "source_equity_drawdown_percent",
        "source_worst_month",
        "source_worst_month_net",
        "source_worst_slice_axis",
        "source_worst_slice_bucket",
        "source_worst_slice_net",
        "source_profile_decision",
        "candidate_decision",
        "reason",
        "materialization_status",
        "success_criteria",
        "failure_criteria",
        "invalid_conditions",
        "stop_conditions",
        "claim_boundary",
    )
    write_csv(PRESSURE_DESIGN_PATH, result["pressure_design"], pressure_columns)
    write_csv(
        MATERIALIZATION_QUEUE_PATH,
        result["pressure_design"],
        (
            "queue_id",
            "source_queue_id",
            "priority",
            "candidate_alias",
            "state_profile",
            "source_test_id",
            "followup_profile",
            "pressure_group",
            "materialization_status",
            "claim_boundary",
        ),
    )
    write_csv(
        FOLLOWUP_VARIANT_MANIFEST_PATH,
        result["followup_variant_manifest"],
        (
            "queue_id",
            "source_queue_id",
            "priority",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "source_run267AO_queue_id",
            "state_profile",
            "state_feature",
            "followup_profile",
            "pressure_group",
            "model_materialization_type",
            "source_variant_manifest",
            "source_runtime_feature_file",
            "runtime_feature_file",
            "runtime_feature_sha256",
            "source_runtime_model_file",
            "runtime_model_file",
            "runtime_model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "state_feature_index",
            "runtime_rows",
            "signal_rows",
            "missing_feature_cells",
            "source_state_terms",
            "pressure_terms",
            "neutral_bins_preserved",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        result["runtime_contract"],
        (
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "state_profile",
            "followup_profile",
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(result["attempts"]),
        (
            "attempt_name",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "state_profile",
            "followup_profile",
            "pressure_group",
            "tier",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "execution_status",
        ),
    )
    write_csv(
        MODEL_PRESSURE_AUDIT_PATH,
        result["model_pressure_audit"],
        (
            "queue_id",
            "candidate_alias",
            "source_test_id",
            "state_profile",
            "followup_profile",
            "source_model_file",
            "runtime_model_file",
            "state_feature_index",
            "source_state_terms",
            "pressure_terms",
            "state_cut_rows",
            "state_score_rows",
            "changed_state_score_rows",
            "only_state_score_terms_changed",
            "neutral_bins_preserved",
            "audit_read",
        ),
    )
    write_csv(
        CANDIDATE_ROLE_PRESSURE_PATH,
        result["candidate_role_pressure"],
        (
            "candidate_alias",
            "candidate_id",
            "candidate_role",
            "source_decision_label",
            "priority",
            "best_profile",
            "deep_hole_count",
            "worst_month_net_min",
            "worst_slice_net_min",
            "run267AS_materialized_profiles",
            "run267AS_materialized_variant_count",
            "run267AS_decision_effect",
            "prune_boundary",
            "reopen_condition",
            "do_not_claim",
        ),
    )
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], source_design.FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("field", "value"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("field", "value"))
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"], ("field", "value"))
    write_csv(
        RESULT_JUDGMENT_PATH,
        result["result_judgment"],
        (
            "result_subject",
            "evidence_available",
            "evidence_missing",
            "judgment_label",
            "claim_boundary",
            "next_condition",
            "user_explanation_hook",
        ),
    )
    run_manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "pressure_design": rel(PRESSURE_DESIGN_PATH),
        "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
        "followup_variant_manifest": rel(FOLLOWUP_VARIANT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "attempts": result["attempts"],
        "model_pressure_audit": rel(MODEL_PRESSURE_AUDIT_PATH),
        "candidate_role_pressure": rel(CANDIDATE_ROLE_PRESSURE_PATH),
        "failure_memory": rel(FAILURE_MEMORY_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    lineage = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "source_inputs": result["inputs"],
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": result["outputs"],
        "registry_links": {
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            "run_registry": rel(RUN_REGISTRY_PATH),
            "alpha_run_ledger": rel(PROJECT_LEDGER_PATH),
            "stage_run_ledger": rel(STAGE_LEDGER_PATH),
        },
        "availability": "tracked_generated_with_manifest_and_common_file_copies",
        "lineage_judgment": "connected_with_boundary",
        "boundary": CLAIM_BOUNDARY,
    }
    write_json(LINEAGE_PATH, lineage)

    artifact_hashes = {
        "pressure_design": sha256_file_lf_normalized(PRESSURE_DESIGN_PATH),
        "materialization_queue": sha256_file_lf_normalized(MATERIALIZATION_QUEUE_PATH),
        "followup_variant_manifest": sha256_file_lf_normalized(FOLLOWUP_VARIANT_MANIFEST_PATH),
        "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
        "attempt_manifest": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
        "model_pressure_audit": sha256_file_lf_normalized(MODEL_PRESSURE_AUDIT_PATH),
        "candidate_role_pressure": sha256_file_lf_normalized(CANDIDATE_ROLE_PRESSURE_PATH),
        "failure_memory": sha256_file_lf_normalized(FAILURE_MEMORY_PATH),
        "experiment_design_receipt": sha256_file_lf_normalized(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "data_integrity_receipt": sha256_file_lf_normalized(DATA_INTEGRITY_RECEIPT_PATH),
        "runtime_parity_receipt": sha256_file_lf_normalized(RUNTIME_PARITY_RECEIPT_PATH),
        "result_judgment": sha256_file_lf_normalized(RESULT_JUDGMENT_PATH),
        "run_manifest": sha256_file_lf_normalized(RUN_MANIFEST_PATH),
        "lineage": sha256_file_lf_normalized(LINEAGE_PATH),
    }
    final_result = dict(result)
    final_result["artifact_hashes"] = artifact_hashes
    write_json(REVIEW_RESULT_PATH, final_result)
    write_md(REPORT_PATH, report_markdown(final_result))


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267AS Pool-wide State Feature Engineering Follow-up Materialization(267단계 267AS 후보군 전체 상태 피처 엔지니어링 후속 물질화)",
        "",
        "- action(행동): run267AR(267AR 실행)의 next experiment queue(다음 실험 큐)를 run267AT(267AT 실행)에서 돌릴 수 있는 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
        "- effect(효과): headline KPI(대표 핵심 성과 지표)가 좋은 후보를 바로 고르지 않고, Monday(월요일)와 2024-12(2024년 12월) 구멍을 비달력 상태 압박(noncalendar state pressure, 비달력 상태 압박)으로 다시 시험할 수 있다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AQ(267AQ 실행)에서는 숫자가 좋아 보여도 월요일과 2024년 12월에서 깊게 깨지는 후보가 많았다.",
        "run267AR(267AR 실행)은 그래서 다음 큐를 만들었고, run267AS(267AS 실행)는 그 큐를 실제 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력으로 만들었다.",
        "효과(effect, 효과): 이제 다음 run267AT(267AT 실행)에서 후보가 정말 덜 깨지는지 볼 수 있다. 아직 좋은 후보를 골랐다는 뜻은 아니다.",
        "",
        "## Materialization Summary(물질화 요약)",
        "",
        f"- queue_rows(큐 행): `{result['queue_rows']}`",
        f"- ready_queue_rows(준비된 큐 행): `{result['ready_queue_rows']}`",
        f"- candidates(후보): `{result['candidate_count']}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- attempts queued(대기 시도): `{result['attempt_count']}`",
        f"- model_pressure_audit passed(모델 압박 감사 통과): `{result['model_pressure_audit_pass_count']}/{result['variant_count']}`",
        f"- candidate_role_pressure_rows(후보 역할 압박 행): `{result['candidate_role_pressure_rows']}`",
        f"- failure_memory_rows(실패 기억 행): `{result['failure_memory_rows']}`",
        "",
        "## Candidate Meaning(후보 의미)",
        "",
        "- `s264_aih`: core challenger(핵심 도전자)로 유지하되, range/volatility(범위/변동성) 압박에서 구멍이 줄어야 한다.",
        "- `s264_aia`: OOS anchor(표본외 앵커) 관찰 후보지만, DD(drawdown, 손실폭)와 약한 구간이 편해야 한다.",
        "- `s258_stc`: stress challenger(압박 도전자)라서 강하게 압박하고, 실패하면 가지치기해야 한다.",
        "- `s264_lc`, `s262_lih`: control audit(통제 감사) 전용이다. 좋은 후보 선택 근거가 아니다.",
        "",
        "## Boundary(경계)",
        "",
        "- MT5 execution(MT5 실행): `not_executed`",
        "- balance/equity curve(잔액/평가금 곡선): `pending_run267AT`",
        "- trade quality(거래 품질): `pending_run267AT`",
        "- candidate selection(후보 선택): `none`",
        "- ONNX(ONNX): `not_reviewed`",
        "",
        "## Outputs(산출물)",
        "",
        f"- pressure_design(압박 설계): `{rel(PRESSURE_DESIGN_PATH)}`",
        f"- materialization_queue(물질화 큐): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
        f"- followup_variant_manifest(후속 변형 목록): `{rel(FOLLOWUP_VARIANT_MANIFEST_PATH)}`",
        f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
        f"- model_pressure_audit(모델 압박 감사): `{rel(MODEL_PRESSURE_AUDIT_PATH)}`",
        f"- candidate_role_pressure(후보 역할 압박): `{rel(CANDIDATE_ROLE_PRESSURE_PATH)}`",
        f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- effect(효과): 16개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행한 뒤 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 검토한다.",
    ]
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    static = [
        ("stage267_run267AS_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267AS pool-wide state feature follow-up inputs."),
        ("stage267_run267AS_pressure_design", "pressure_design", PRESSURE_DESIGN_PATH, "Run267AS state feature follow-up pressure design."),
        ("stage267_run267AS_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267AS follow-up materialization queue."),
        ("stage267_run267AS_followup_variant_manifest", "variant_manifest", FOLLOWUP_VARIANT_MANIFEST_PATH, "Run267AS follow-up variant manifest."),
        ("stage267_run267AS_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267AS runtime contract."),
        ("stage267_run267AS_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267AS MT5 attempt manifest."),
        ("stage267_run267AS_model_pressure_audit", "model_pressure_audit", MODEL_PRESSURE_AUDIT_PATH, "Run267AS model pressure audit."),
        ("stage267_run267AS_candidate_role_pressure", "candidate_role_pressure", CANDIDATE_ROLE_PRESSURE_PATH, "Run267AS candidate role pressure matrix."),
        ("stage267_run267AS_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267AS failure memory."),
        ("stage267_run267AS_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267AS experiment design receipt."),
        ("stage267_run267AS_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267AS data integrity receipt."),
        ("stage267_run267AS_runtime_parity_receipt", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267AS runtime parity receipt."),
        ("stage267_run267AS_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AS result judgment."),
        ("stage267_run267AS_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267AS run manifest."),
        ("stage267_run267AS_lineage", "lineage", LINEAGE_PATH, "Run267AS lineage."),
        ("stage267_run267AS_review_result", "review_result_json", REVIEW_RESULT_PATH, "Run267AS review result JSON."),
        ("stage267_run267AS_report", "review_report", REPORT_PATH, "Run267AS review report."),
    ]
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in static
    ]
    for item in result["dynamic_artifacts"]:
        path = repo_path(str(item["path"]))
        rows.append(
            {
                "artifact_id": item["artifact_id"],
                "artifact_type": item["artifact_type"],
                "path": item["path"],
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": item["notes"],
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "pool_wide_state_feature_engineering_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT),
        "notes": (
            f"variants={result['variant_count']};attempts={result['attempt_count']};"
            f"pressure_audit={result['model_pressure_audit_pass_count']}/{result['variant_count']};"
            f"selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;next_action={NEXT_ACTION}."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_state_feature_engineering_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_state_feature_engineering_followup_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pool_wide_state_feature_engineering_followup_materialization",
        "tier_scope": "Tier A and Tier A+B 2024 historical runtime attempts planned; Tier A+B duplicate boundary until fallback enabled",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "experiment_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};pressure_audit={result['model_pressure_audit_pass_count']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;mt5_execution=not_executed",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    stage_row = {
        "row_id": "stage267_run267AS_pool_wide_state_feature_engineering_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_state_feature_engineering_followup_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 follow-up attempts planned",
        "scoreboard": "feature_model_set_ini_manifest_and_pressure_audit",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};next_action={NEXT_ACTION}.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def update_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267AS_pool_wide_state_feature_engineering_followup_materialization(267AS 후보군 전체 상태 피처 엔지니어링 후속 물질화): `{rel(REPORT_PATH)}`"

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_followup_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(current, "run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch", report_line)
    current = current.replace(
        "- next_run(다음 실행): `run267AS_materialize_pool_wide_state_feature_engineering_followup_queue`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    current = current.replace(
        "- next_action(다음 행동): `run267AS_materialize_pool_wide_state_feature_engineering_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    current = append_block_once(
        current,
        "Run267AS(267AS 실행)는 run267AR",
        "\n".join(
            [
                "Run267AS(267AS 실행)는 run267AR(267AR 실행)의 next experiment queue(다음 실험 큐)를 pool-wide state feature engineering follow-up materialization(후보군 전체 상태 피처 엔지니어링 후속 물질화)으로 바꿨다.",
                f"Effect(효과): {result['variant_count']}개 variant(변형)와 {result['attempt_count']}개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
            ]
        ),
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(selection, "run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch", report_line)
    selection = selection.replace(
        "- next_action(다음 행동): `run267AS_materialize_pool_wide_state_feature_engineering_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection = append_block_once(
        selection,
        "Run267AS(267AS 실행)는 pool-wide state feature engineering follow-up",
        "\n".join(
            [
                "Run267AS(267AS 실행)는 pool-wide state feature engineering follow-up materialization(후보군 전체 상태 피처 엔지니어링 후속 물질화)을 완료했다.",
                "Effect(효과): 다음 run267AT(267AT 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 실제 거래/곡선/시간구간 영향을 확인한다. 선택 후보(selected candidate, 선택 후보)는 없다.",
            ]
        ),
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{STATUS}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after_contains(review, "run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch", report_line)
    review = review.replace(
        "- next_action(다음 행동): `run267AS_materialize_pool_wide_state_feature_engineering_followup_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    review = append_block_once(
        review,
        "Run267AS(267AS 실행)는 pool-wide state feature engineering follow-up",
        "\n".join(
            [
                "Run267AS(267AS 실행)는 pool-wide state feature engineering follow-up materialization(후보군 전체 상태 피처 엔지니어링 후속 물질화)을 완료했다.",
                f"Effect(효과): {result['variant_count']}개 follow-up variant(후속 변형)와 {result['attempt_count']}개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었지만 아직 실행 결과가 아니므로 선택 후보(selected candidate, 선택 후보)는 없다.",
            ]
        ),
    )
    write_text(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus_block = (
        "- >-\n"
        f"  Stage267(267단계) run267AS(267AS 실행) pool-wide state feature engineering follow-up materialization(후보군 전체 상태 피처 엔지니어링 후속 물질화) `{STATUS}`. "
        f"Effect(효과): run267AR(267AR 실행)의 큐를 {result['variant_count']}개 variant(변형)와 {result['attempt_count']}개 MT5(MetaTrader 5, 메타트레이더5) 시도 입력으로 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_design.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {source_design.RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {source_design.RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = append_after_contains(
        workspace,
        "run267AR_pool_wide_state_feature_engineering_followup_or_adapter_branch_report_path",
        f"  run267AS_pool_wide_state_feature_engineering_followup_materialization_report_path: {rel(REPORT_PATH)}",
    )
    workspace = workspace.replace(
        "next_action: run267AS_materialize_pool_wide_state_feature_engineering_followup_queue",
        f"next_action: {NEXT_ACTION}",
    )
    write_text(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_materialization()
    write_outputs(result)
    final_result = json.loads(io_path(REVIEW_RESULT_PATH).read_text(encoding="utf-8"))
    update_ledgers(final_result)
    update_docs(final_result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "queue_rows": final_result["queue_rows"],
                "ready_queue_rows": final_result["ready_queue_rows"],
                "variant_count": final_result["variant_count"],
                "attempt_count": final_result["attempt_count"],
                "model_pressure_audit_pass_count": final_result["model_pressure_audit_pass_count"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
