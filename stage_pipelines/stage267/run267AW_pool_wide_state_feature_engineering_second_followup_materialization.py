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
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267AS_pool_wide_state_feature_engineering_followup_materialization as source_materialization
from stage_pipelines.stage267 import run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch as source_design
from stage_pipelines.stage267 import run267W_true_internal_ablation_score_table_materialization as source_tables


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267AW"
RUN_ID = "run267AW_stage267_pool_wide_state_feature_engineering_second_followup_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267AW_pool_wide_state_feature_engineering_second_followup_materialized_execution_pending"
JUDGMENT = "second_followup_materialized_execution_pending_no_candidate_selection"
NEXT_ACTION = "run267AX_execute_pool_wide_state_feature_engineering_second_followup_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_second_followup_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_QUEUE_PATH = source_design.NEXT_EXPERIMENT_QUEUE_PATH
SOURCE_PROFILE_DECISION_PATH = source_design.PROFILE_DECISION_PATH
SOURCE_CANDIDATE_DECISION_PATH = source_design.CANDIDATE_DECISION_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_ROUTE_DUPLICATE_REVIEW_PATH = source_design.SOURCE_TIER_DUPLICATE_REVIEW_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_materialization.FOLLOWUP_VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_DESIGN_REPORT_PATH = source_design.REPORT_PATH
SOURCE_MATERIALIZATION_REPORT_PATH = source_materialization.REPORT_PATH

PRESSURE_DESIGN_PATH = RUN_ROOT / "second_followup_pressure_design.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "second_followup_materialization_queue.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "second_followup_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
MODEL_PRESSURE_AUDIT_PATH = RUN_ROOT / "model_pressure_audit.csv"
CANDIDATE_ROLE_PRESSURE_PATH = RUN_ROOT / "candidate_role_pressure_matrix.csv"
ROUTE_GAP_AUDIT_PATH = RUN_ROOT / "route_gap_audit.csv"
TIER_RECORD_REQUIREMENT_AUDIT_PATH = RUN_ROOT / "tier_record_requirement_audit.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AW_pool_wide_state_feature_engineering_second_followup_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AW_pool_wide_state_feature_engineering_second_followup_materialization.py")

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
COMMON_ROOT = "OPV2/s267aw/run267AW_state_feature_second_followup"
PERIOD_LABEL = input_probe.PERIOD_LABEL
MODEL_MATERIALIZATION_TYPE = "research_score_table_pool_wide_state_feature_second_followup_pressure_v3"

PRESSURE_TERMS: dict[str, tuple[tuple[float, float, float], ...]] = {
    "core_range_volatility_interaction_v3": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.035, 0.075, -0.035),
        (-0.075, 0.160, -0.075),
        (-0.120, 0.245, -0.120),
    ),
    "core_volatility_range_interaction_v3": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.040, 0.085, -0.040),
        (-0.080, 0.175, -0.080),
        (-0.130, 0.260, -0.130),
    ),
    "oos_anchor_range_dd_conservative_v3": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.025, 0.055, -0.025),
        (-0.060, 0.125, -0.060),
        (-0.095, 0.190, -0.095),
    ),
    "oos_anchor_shock_range_conservative_v3": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.030, 0.065, -0.030),
        (-0.070, 0.145, -0.070),
        (-0.110, 0.220, -0.110),
    ),
    "defensive_control_repeat_audit_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.035, 0.075, -0.035),
        (-0.070, 0.150, -0.070),
        (-0.115, 0.230, -0.115),
    ),
    "validation_control_repeat_audit_v2": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.035, 0.075, -0.035),
        (-0.070, 0.150, -0.070),
        (-0.115, 0.230, -0.115),
    ),
    "stress_challenger_volatility_strict_prune_v3": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.055, 0.115, -0.055),
        (-0.115, 0.240, -0.115),
        (-0.180, 0.360, -0.180),
    ),
    "stress_challenger_trend_strict_prune_v3": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.050, 0.105, -0.050),
        (-0.105, 0.220, -0.105),
        (-0.165, 0.330, -0.165),
    ),
}

PRESSURE_PLAN = (
    {
        "queue_id": "run267AW_p01_s264_aih_range_volatility_interaction",
        "source_queue_id": "run267AV_q01_core_challenger_second_pressure",
        "priority": "P0",
        "candidate_alias": "s264_aih",
        "state_profile": "range_expansion_pressure",
        "source_followup_profile": "core_range_resilience_pressure_v2",
        "second_followup_profile": "core_range_volatility_interaction_v3",
        "pressure_group": "core_challenger_second_pressure",
        "reason": "s264_aih range profile needs a stronger noncalendar interaction pressure before it can stay the core challenger",
    },
    {
        "queue_id": "run267AW_p02_s264_aih_volatility_range_interaction",
        "source_queue_id": "run267AV_q01_core_challenger_second_pressure",
        "priority": "P0",
        "candidate_alias": "s264_aih",
        "state_profile": "volatility_regime_expansion",
        "source_followup_profile": "core_volatility_resilience_pressure_v2",
        "second_followup_profile": "core_volatility_range_interaction_v3",
        "pressure_group": "core_challenger_second_pressure",
        "reason": "s264_aih volatility profile must reduce 2024-12 and Monday holes without trade-count collapse",
    },
    {
        "queue_id": "run267AW_p03_s264_aia_range_dd_watch",
        "source_queue_id": "run267AV_q02_oos_anchor_adapter_watch_gate",
        "priority": "P0",
        "candidate_alias": "s264_aia",
        "state_profile": "range_expansion_pressure",
        "source_followup_profile": "oos_anchor_dd_resilience_pressure_v2",
        "second_followup_profile": "oos_anchor_range_dd_conservative_v3",
        "pressure_group": "oos_anchor_adapter_watch_gate",
        "reason": "s264_aia can only remain an Adapter watch if the drawdown edge survives weak-slice pressure",
    },
    {
        "queue_id": "run267AW_p04_s264_aia_shock_range_watch",
        "source_queue_id": "run267AV_q02_oos_anchor_adapter_watch_gate",
        "priority": "P0",
        "candidate_alias": "s264_aia",
        "state_profile": "return_shock_absorption",
        "source_followup_profile": "oos_anchor_shock_resilience_pressure_v2",
        "second_followup_profile": "oos_anchor_shock_range_conservative_v3",
        "pressure_group": "oos_anchor_adapter_watch_gate",
        "reason": "s264_aia shock axis checks whether the OOS anchor is structural rather than one profile accident",
    },
    {
        "queue_id": "run267AW_p05_s264_lc_control_repeat_audit",
        "source_queue_id": "run267AV_q03_control_stability_audit",
        "priority": "P1",
        "candidate_alias": "s264_lc",
        "state_profile": "volatility_regime_expansion",
        "source_followup_profile": "defensive_control_volatility_audit_v1",
        "second_followup_profile": "defensive_control_repeat_audit_v2",
        "pressure_group": "defensive_control_repeat_audit",
        "reason": "s264_lc is kept only to separate challenger-specific improvement from broad pressure drift",
    },
    {
        "queue_id": "run267AW_p06_s262_lih_control_repeat_audit",
        "source_queue_id": "run267AV_q03_control_stability_audit",
        "priority": "P1",
        "candidate_alias": "s262_lih",
        "state_profile": "volatility_regime_expansion",
        "source_followup_profile": "validation_control_volatility_audit_v1",
        "second_followup_profile": "validation_control_repeat_audit_v2",
        "pressure_group": "validation_control_repeat_audit",
        "reason": "s262_lih is a validation-heavy comparator and not an Adapter lane unless it differentiates fragility",
    },
    {
        "queue_id": "run267AW_p07_s258_stc_volatility_strict_prune",
        "source_queue_id": "run267AV_q04_stress_challenger_prune_or_rescue",
        "priority": "P0",
        "candidate_alias": "s258_stc",
        "state_profile": "volatility_regime_expansion",
        "source_followup_profile": "stress_challenger_volatility_prune_pressure_v2",
        "second_followup_profile": "stress_challenger_volatility_strict_prune_v3",
        "pressure_group": "stress_challenger_prune_or_rescue",
        "reason": "s258_stc must pass risk, trade count, and weak-slice gates together or leave the active lane",
    },
    {
        "queue_id": "run267AW_p08_s258_stc_trend_strict_prune",
        "source_queue_id": "run267AV_q04_stress_challenger_prune_or_rescue",
        "priority": "P0",
        "candidate_alias": "s258_stc",
        "state_profile": "trend_strength_disagreement",
        "source_followup_profile": "stress_challenger_trend_prune_pressure_v2",
        "second_followup_profile": "stress_challenger_trend_strict_prune_v3",
        "pressure_group": "stress_challenger_prune_or_rescue",
        "reason": "s258_stc trend axis checks whether the stress result is too tied to one indicator family",
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
            break
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, current in enumerate(lines):
        if needle in current:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(line)
    return "\n".join(lines) + "\n"


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
        SOURCE_QUEUE_PATH,
        SOURCE_PROFILE_DECISION_PATH,
        SOURCE_CANDIDATE_DECISION_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def source_variants_by_key() -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("state_profile", ""), row.get("followup_profile", "")): row
        for row in read_csv(SOURCE_VARIANT_MANIFEST_PATH)
        if row.get("candidate_alias") and row.get("state_profile") and row.get("followup_profile")
    }


def source_contracts_by_key() -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("state_profile", ""), row.get("followup_profile", "")): row
        for row in read_csv(SOURCE_RUNTIME_CONTRACT_PATH)
        if row.get("candidate_alias") and row.get("state_profile") and row.get("followup_profile")
    }


def profile_decisions_by_key() -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("state_profile", ""), row.get("followup_profile", "")): row
        for row in read_csv(SOURCE_PROFILE_DECISION_PATH)
        if row.get("candidate_alias") and row.get("state_profile") and row.get("followup_profile")
    }


def candidate_decisions_by_alias() -> dict[str, dict[str, str]]:
    return {
        row.get("candidate_alias", ""): row
        for row in read_csv(SOURCE_CANDIDATE_DECISION_PATH)
        if row.get("candidate_alias")
    }


def source_queue_by_id() -> dict[str, dict[str, str]]:
    return {row.get("queue_id", ""): row for row in read_csv(SOURCE_QUEUE_PATH) if row.get("queue_id")}


def build_pressure_design() -> list[dict[str, Any]]:
    source_queues = source_queue_by_id()
    profile_decisions = profile_decisions_by_key()
    candidate_decisions = candidate_decisions_by_alias()
    source_variants = source_variants_by_key()
    rows: list[dict[str, Any]] = []
    for plan in PRESSURE_PLAN:
        key = (
            str(plan["candidate_alias"]),
            str(plan["state_profile"]),
            str(plan["source_followup_profile"]),
        )
        source_queue = source_queues.get(str(plan["source_queue_id"]), {})
        profile = profile_decisions.get(key, {})
        candidate = candidate_decisions.get(str(plan["candidate_alias"]), {})
        source_variant = source_variants.get(key, {})
        second_profile = str(plan["second_followup_profile"])
        rows.append(
            {
                "queue_id": plan["queue_id"],
                "source_queue_id": plan["source_queue_id"],
                "priority": plan["priority"],
                "workstream": source_queue.get("workstream"),
                "candidate_alias": plan["candidate_alias"],
                "candidate_id": candidate.get("candidate_id") or source_variant.get("candidate_id"),
                "candidate_role": candidate.get("candidate_role") or source_variant.get("candidate_role"),
                "state_profile": plan["state_profile"],
                "source_followup_profile": plan["source_followup_profile"],
                "second_followup_profile": second_profile,
                "source_test_id": source_variant.get("source_test_id") or profile.get("source_test_id"),
                "source_run267AS_queue_id": source_variant.get("queue_id"),
                "pressure_group": plan["pressure_group"],
                "pressure_terms": terms_text(PRESSURE_TERMS[second_profile]),
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
                else "blocked_missing_run267AS_source_variant",
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
            signal_rows += 1 if as_float(row.get(input_probe.SOURCE_SIGNAL_COLUMN), 0.0) != 0.0 else 0
            missing_cells += sum(1 for column in feature_order if str(row.get(column, "")).strip() == "")
    return {
        "rows": rows,
        "signal_rows": signal_rows,
        "feature_order": feature_order,
        "feature_count": len(feature_order),
        "feature_order_hash": source_materialization.ordered_hash(feature_order),
        "missing_feature_cells": missing_cells,
    }


def copy_runtime_feature(source: Path, destination: Path) -> dict[str, Any]:
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    io_path(destination).write_bytes(io_path(source).read_bytes())
    meta = count_feature_rows(destination)
    meta.update({"runtime_feature_file": rel(destination), "runtime_feature_sha256": sha256_file_lf_normalized(destination)})
    return meta


def write_pressure_model(
    source: Path,
    destination: Path,
    state_feature_index: int,
    second_followup_profile: str,
) -> dict[str, Any]:
    terms = PRESSURE_TERMS[second_followup_profile]
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    output: list[dict[str, Any]] = []
    source_terms: list[tuple[float, float, float]] = []
    changed_rows = 0
    score_rows = 0
    cut_rows = 0
    neutral_bins_preserved = True
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

    if cut_rows != 3 or score_rows != len(terms):
        raise RuntimeError(f"state term row count mismatch for {source}: cuts={cut_rows}, scores={score_rows}")

    write_runtime_csv(destination, output, CSV_MODEL_COLUMNS)
    return {
        "source_runtime_model_file": rel(source),
        "runtime_model_file": rel(destination),
        "runtime_model_sha256": sha256_file_lf_normalized(destination),
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
    second_profile = str(queue_row["second_followup_profile"])
    queue_id = str(queue_row["queue_id"])
    queue_token = safe_token(queue_id, 72)
    profile_token = safe_token(f"{state_profile}_{second_profile}", 64)
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
        second_profile,
    )

    common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    _full_order, _rank_column, gate_column = source_tables.candidate_full_feature_order(spec)
    magic = 26736000 + index
    payload = attempt_payload(
        run_root=RUN_ROOT,
        run_id=RUN_ID,
        stage_number=267,
        exploration_label=f"stage267_StateFeatureSecondFollowup__{safe_token(second_profile, 32)}",
        attempt_name=f"{queue_token}_ta_2024",
        tier=input_probe.mt5.TIER_A,
        split=PERIOD_LABEL,
        model_path=common_model_path,
        model_id=f"{RUN_ID}_{alias}_{safe_token(state_profile, 32)}_{safe_token(second_profile, 32)}_v1",
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
        attempt_role="tier_only_total",
        record_view_prefix=f"mt5_ta_{alias}_{safe_token(state_profile, 24)}_aw",
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
            "source_test_id": queue_row.get("source_test_id"),
            "state_profile": state_profile,
            "source_followup_profile": queue_row.get("source_followup_profile"),
            "second_followup_profile": second_profile,
            "pressure_group": queue_row.get("pressure_group"),
            "source_run267AS_queue_id": queue_row.get("source_run267AS_queue_id"),
            "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
            "execution_status": "not_executed",
            "tier_pair_boundary": "Tier_B_and_actual_routed_total_blocked_until_true_fallback_manifest_exists",
        }
    )

    variant = {
        "queue_id": queue_id,
        "source_queue_id": queue_row.get("source_queue_id"),
        "priority": queue_row.get("priority"),
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": queue_row.get("source_test_id"),
        "source_run267AS_queue_id": queue_row.get("source_run267AS_queue_id"),
        "state_profile": state_profile,
        "state_feature": source_variant.get("state_feature"),
        "source_followup_profile": queue_row.get("source_followup_profile"),
        "second_followup_profile": second_profile,
        "pressure_group": queue_row.get("pressure_group"),
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
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
        "source_test_id": queue_row.get("source_test_id"),
        "state_profile": state_profile,
        "source_followup_profile": queue_row.get("source_followup_profile"),
        "second_followup_profile": second_profile,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;run267AS feature order;second follow-up pressure score-table terms;Tier A execution only until true fallback route exists",
        "feature_count": feature_meta["feature_count"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "short_threshold": as_float(source_contract.get("short_threshold"), spec.variant.short_threshold),
        "long_threshold": as_float(source_contract.get("long_threshold"), spec.variant.long_threshold),
        "min_margin": as_float(source_contract.get("min_margin"), 0.0),
        "max_hold_bars": as_int(source_contract.get("max_hold_bars"), spec.variant.max_hold_bars),
        "known_difference": "uses run267AS runtime features and changes only existing state feature score-table terms; no retraining, no literal weekday/month filter, no Tier A+B duplicate claim",
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }
    audit = {
        "queue_id": queue_id,
        "candidate_alias": alias,
        "state_profile": state_profile,
        "source_followup_profile": queue_row.get("source_followup_profile"),
        "second_followup_profile": second_profile,
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
        raise RuntimeError(f"second pressure model audit failed for {queue_id}: {audit}")
    return {
        "variant": variant,
        "contract": contract,
        "audit": audit,
        "attempt": payload,
        "feature_path": feature_path,
        "model_path": model_path,
    }


def build_candidate_role_pressure_matrix(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_alias: dict[str, list[str]] = {}
    for row in queue_rows:
        if row.get("materialization_status") == "ready_for_score_table_materialization":
            by_alias.setdefault(str(row.get("candidate_alias")), []).append(str(row.get("second_followup_profile")))
    rows: list[dict[str, Any]] = []
    for alias, candidate in candidate_decisions_by_alias().items():
        profiles = by_alias.get(alias, [])
        if alias == "s264_aih":
            action = "keep_core_challenger_under_second_pressure_not_selection"
        elif alias == "s264_aia":
            action = "adapter_watch_gate_only_after_slice_improvement"
        elif alias == "s258_stc":
            action = "strict_stress_prune_or_rescue_gate"
        elif alias in {"s264_lc", "s262_lih"}:
            action = "control_audit_only"
        else:
            action = "not_materialized"
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
                "run267AW_materialized_profiles": ";".join(profiles),
                "run267AW_materialized_variant_count": len(profiles),
                "run267AW_decision_effect": action,
                "prune_boundary": candidate.get("prune_boundary"),
                "reopen_condition": candidate.get("reopen_condition"),
                "do_not_claim": "no_selected_candidate_no_ONNX_no_goal_achieve",
            }
        )
    return rows


def build_route_gap_audit() -> list[dict[str, Any]]:
    q05 = source_queue_by_id().get("run267AV_q05_true_fallback_route_gap", {})
    return [
        {
            "route_gap_id": "run267AW_route_gap_true_tier_b_fallback",
            "source_queue_id": q05.get("queue_id", "run267AV_q05_true_fallback_route_gap"),
            "scope": q05.get("candidate_scope", "all_baseline_candidates"),
            "source_evidence": q05.get("source_evidence") or rel(SOURCE_ROUTE_DUPLICATE_REVIEW_PATH),
            "current_status": "gap_confirmed_before_runtime_claim",
            "fallback_manifest_status": "missing_required_before_Tier_A_B_or_actual_routed_total_claim",
            "tier_a_record_status": "materialized_for_8_second_followup_attempts",
            "tier_b_record_status": "blocked_missing_true_fallback_manifest",
            "actual_routed_total_status": "blocked_missing_true_fallback_manifest",
            "effect": "prevents duplicate Tier A+B rows from being treated as combined or routed survival evidence",
            "next_action": "create_true_fallback_manifest_or_keep_Tier_A_only_boundary_after_run267AX",
            "claim_boundary": "route_audit_only_no_runtime_reproduction_no_ONNX",
        }
    ]


def build_tier_record_requirement_audit(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "required_record": "Tier A separate",
            "status": "materialized",
            "evidence": rel(ATTEMPT_MANIFEST_PATH),
            "count": result["attempt_count"],
            "effect": "run267AX can execute the second follow-up pressure on the known full-context sample",
        },
        {
            "required_record": "Tier B separate",
            "status": "blocked_missing_true_fallback_manifest",
            "evidence": rel(ROUTE_GAP_AUDIT_PATH),
            "count": 0,
            "effect": "prevents a partial-context claim from being inferred from duplicate rows",
        },
        {
            "required_record": "Tier A+B actual routed total",
            "status": "blocked_missing_true_fallback_manifest",
            "evidence": rel(ROUTE_GAP_AUDIT_PATH),
            "count": 0,
            "effect": "keeps runtime reproduction and ONNX parity claims closed until fallback use is separable",
        },
    ]


def build_failure_memory() -> list[dict[str, Any]]:
    rows = list(read_csv(SOURCE_FAILURE_MEMORY_PATH))
    rows.extend(
        [
            {
                "memory_id": "run267AW_mem06_second_pressure_not_selection",
                "pattern": "second follow-up pressure materialization is not performance evidence(2차 후속 압박 물질화는 성과 근거가 아님)",
                "evidence": rel(PRESSURE_DESIGN_PATH),
                "affected_scope": "all run267AW materialized variants(모든 run267AW 물질화 변형)",
                "do_not_repeat": "do not select from materialization counts or pressure audit pass alone(물질화 수나 압박 감사 통과만으로 선택 금지)",
                "salvage_angle": "execute MT5 then inspect curve, weak slices, and trade quality(MT5 실행 후 곡선, 약한 구간, 거래 품질 확인)",
                "reopen_condition": "run267AX shows slice improvement without trade-count or DD damage(run267AX가 거래 수 또는 손실폭 손상 없이 구간 개선을 보임)",
                "boundary": "execution_pending_no_selection(실행 대기, 선택 없음)",
            },
            {
                "memory_id": "run267AW_mem07_true_fallback_route_gap",
                "pattern": "true Tier B fallback remains missing(진짜 Tier B 대체가 아직 없음)",
                "evidence": rel(ROUTE_GAP_AUDIT_PATH),
                "affected_scope": "Tier B and actual routed total records(Tier B와 실제 라우팅 전체 기록)",
                "do_not_repeat": "do not create duplicate Tier A+B attempts as routed fallback evidence(중복 Tier A+B 시도를 라우팅 대체 근거로 만들지 않음)",
                "salvage_angle": "build fallback manifest after Tier A pressure result if still worth route audit(Tier A 압박 결과 후 가치가 있으면 대체 목록 생성)",
                "reopen_condition": "fallback used count and component records are separable(대체 사용 수와 구성 기록이 분리됨)",
                "boundary": "runtime_reproduction_blocker(런타임 재현 차단 조건)",
            },
        ]
    )
    return rows


def build_experiment_design_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "hypothesis", "value": "run267AU headline-positive profiles still have deep 2024-12 and Monday holes, so one bounded second noncalendar pressure can decide keep, watch, or prune roles"},
        {"field": "decision_use", "value": "create run267AX Tier A MT5 attempt inputs and route-gap audit; no candidate selection and no ONNX readiness claim"},
        {"field": "comparison_baseline", "value": "run267AS materialized profiles plus run267AV candidate role decisions and failure memory"},
        {"field": "control_variables", "value": "same 2024 period; same candidate score source; same thresholds; same RuntimeProbeEA; no retraining"},
        {"field": "changed_variables", "value": "second follow-up state-feature score-table terms only"},
        {"field": "sample_scope", "value": "Tier A 2024 historical attempts materialized; Tier B and actual routed total blocked until true fallback manifest exists"},
        {"field": "success_criteria", "value": "future run267AX review must improve worst month and worst weekday while preserving trade count, PF, DD, and curve shape"},
        {"field": "failure_criteria", "value": "weak slices stay deep, DD worsens, trade count thins, or controls mirror challengers without added information"},
        {"field": "invalid_conditions", "value": "literal calendar filter; feature order mismatch; missing MT5 report; duplicate Tier A+B called true fallback"},
        {"field": "stop_conditions", "value": "if second pressure fails, prune or redirect rather than extending the same repair loop"},
        {"field": "evidence_plan", "value": "pressure_design;variant_manifest;runtime_contract;attempt_manifest;route_gap_audit;future_MT5_KPI;future_curve_time_slice_trade_quality_review"},
        {"field": "required_gate_coverage", "value": "experiment_design_schema;artifact_lineage_connected;runtime_parity_boundary;tier_record_boundary;result_claim_guard"},
    ]


def build_data_integrity_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "data_source", "value": f"{rel(SOURCE_QUEUE_PATH)} and {rel(SOURCE_VARIANT_MANIFEST_PATH)}"},
        {"field": "time_axis", "value": "bar_time_server copied from run267AS runtime feature files; MT5 window remains 2024.01.02 through 2025.01.01"},
        {"field": "sample_scope", "value": "US100 M5 2024 historical stress window; run267AW creates 8 Tier A attempts"},
        {"field": "missing_or_duplicate_check", "value": f"variant_feature_missing_cells={sum(as_int(row.get('missing_feature_cells')) for row in result['variant_manifest'])};ready_queue_rows={result['ready_queue_rows']}/{result['queue_rows']}"},
        {"field": "feature_label_boundary", "value": "no MT5 PnL becomes a label; model is not retrained; only existing state feature score terms are changed"},
        {"field": "split_boundary", "value": "materialization-only; execution and KPI review remain pending run267AX"},
        {"field": "leakage_risk", "value": "weak-slice evidence drives exploratory pressure, so later results are diagnostic until broader validation passes"},
        {"field": "data_hash_or_identity", "value": f"run_manifest={rel(RUN_MANIFEST_PATH)}"},
        {"field": "integrity_judgment", "value": "usable_with_Tier_A_only_boundary" if result["ready_queue_rows"] == result["queue_rows"] else "inconclusive"},
    ]


def build_runtime_parity_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"field": "runtime_feature_order", "value": "run267AS feature_order copied unchanged and feature_order_hash recorded per variant"},
        {"field": "score_table_change", "value": "only existing state feature score rows are changed; cut rows and feature count are unchanged"},
        {"field": "model_pressure_audit", "value": f"{result['model_pressure_audit_pass_count']}/{result['variant_count']}"},
        {"field": "Tier_B_fallback", "value": "blocked_missing_true_fallback_manifest"},
        {"field": "MT5_execution_status", "value": "not_executed_materialization_only"},
        {"field": "runtime_claim_boundary", "value": "no runtime authority; no ONNX; no candidate selection"},
    ]


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"variants={result['variant_count']};attempts={result['attempt_count']};pressure_audit_pass={result['model_pressure_audit_pass_count']}/{result['variant_count']};route_gap_rows={result['route_gap_rows']}",
            "evidence_missing": "MT5_execution;trade_list_review;balance_equity_curve;time_slice_KPI;trade_quality_after_second_pressure;true_Tier_B_fallback_manifest",
            "judgment_label": JUDGMENT,
            "claim_boundary": "materialization_only_no_candidate_selection_no_onnx_no_goal_achieve_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 다음 MT5 실행용 2차 압박 입력을 만들었고, Tier B 대체 공백은 공백으로 못박은 상태다.",
        }
    ]


def build_materialization() -> dict[str, Any]:
    require_inputs()
    pressure_design = build_pressure_design()
    ready_rows = [row for row in pressure_design if row.get("materialization_status") == "ready_for_score_table_materialization"]
    source_variants = source_variants_by_key()
    source_contracts = source_contracts_by_key()
    specs = specs_by_alias()

    variants: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    dynamic_artifacts: list[dict[str, Any]] = []
    for index, queue_row in enumerate(ready_rows, start=1):
        key = (
            str(queue_row["candidate_alias"]),
            str(queue_row["state_profile"]),
            str(queue_row["source_followup_profile"]),
        )
        source_variant = source_variants.get(key)
        source_contract = source_contracts.get(key)
        if source_variant is None or source_contract is None:
            raise KeyError(f"missing run267AS source variant/contract for {key}")
        item = materialize_variant(queue_row, source_variant, source_contract, specs[str(queue_row["candidate_alias"])], index)
        variants.append(item["variant"])
        contracts.append(item["contract"])
        audits.append(item["audit"])
        attempts.append(item["attempt"])
        dynamic_artifacts.extend(
            [
                {
                    "artifact_id": f"stage267_run267AW_{safe_token(str(queue_row['queue_id']), 64)}_runtime_feature",
                    "artifact_type": "runtime_feature_csv",
                    "path": rel(item["feature_path"]),
                    "notes": f"Run267AW runtime feature CSV for {queue_row['queue_id']}.",
                },
                {
                    "artifact_id": f"stage267_run267AW_{safe_token(str(queue_row['queue_id']), 64)}_runtime_model",
                    "artifact_type": "runtime_model_csv",
                    "path": rel(item["model_path"]),
                    "notes": f"Run267AW second follow-up pressure score table CSV for {queue_row['queue_id']}.",
                },
            ]
        )

    candidate_role_pressure = build_candidate_role_pressure_matrix(pressure_design)
    route_gap_audit = build_route_gap_audit()
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
        "route_gap_rows": len(route_gap_audit),
        "failure_memory_rows": len(failure_memory),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "pressure_design": pressure_design,
        "variant_manifest": variants,
        "runtime_contract": contracts,
        "model_pressure_audit": audits,
        "attempts": attempts,
        "candidate_role_pressure": candidate_role_pressure,
        "route_gap_audit": route_gap_audit,
        "failure_memory": failure_memory,
        "dynamic_artifacts": dynamic_artifacts,
        "inputs": {
            "run267AV_queue": rel(SOURCE_QUEUE_PATH),
            "run267AV_profile_decision": rel(SOURCE_PROFILE_DECISION_PATH),
            "run267AV_candidate_decision": rel(SOURCE_CANDIDATE_DECISION_PATH),
            "run267AV_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "run267AV_route_duplicate_review": rel(SOURCE_ROUTE_DUPLICATE_REVIEW_PATH),
            "run267AS_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "run267AS_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "run267AV_report": rel(SOURCE_DESIGN_REPORT_PATH),
            "run267AS_report": rel(SOURCE_MATERIALIZATION_REPORT_PATH),
        },
        "outputs": {
            "pressure_design": rel(PRESSURE_DESIGN_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "model_pressure_audit": rel(MODEL_PRESSURE_AUDIT_PATH),
            "candidate_role_pressure": rel(CANDIDATE_ROLE_PRESSURE_PATH),
            "route_gap_audit": rel(ROUTE_GAP_AUDIT_PATH),
            "tier_record_requirement_audit": rel(TIER_RECORD_REQUIREMENT_AUDIT_PATH),
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
    result["tier_record_requirement_audit"] = build_tier_record_requirement_audit(result)
    result["experiment_design_receipt"] = build_experiment_design_receipt(result)
    result["data_integrity_receipt"] = build_data_integrity_receipt(result)
    result["runtime_parity_receipt"] = build_runtime_parity_receipt(result)
    result["result_judgment"] = build_result_judgment(result)
    return result


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "attempt_name": attempt.get("attempt_name"),
            "queue_id": attempt.get("queue_id"),
            "candidate_id": attempt.get("candidate_id"),
            "candidate_alias": attempt.get("candidate_alias"),
            "candidate_role": attempt.get("candidate_role"),
            "source_test_id": attempt.get("source_test_id"),
            "state_profile": attempt.get("state_profile"),
            "source_followup_profile": attempt.get("source_followup_profile"),
            "second_followup_profile": attempt.get("second_followup_profile"),
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
            "tier_pair_boundary": attempt.get("tier_pair_boundary"),
            "execution_status": attempt.get("execution_status", "not_executed"),
        }
        for attempt in attempts
    ]


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
        "source_followup_profile",
        "second_followup_profile",
        "source_test_id",
        "source_run267AS_queue_id",
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
    write_csv(MATERIALIZATION_QUEUE_PATH, result["pressure_design"], pressure_columns)
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"], tuple(result["variant_manifest"][0].keys()) if result["variant_manifest"] else ())
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"], tuple(result["runtime_contract"][0].keys()) if result["runtime_contract"] else ())
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_rows(result["attempts"]), tuple(attempt_rows(result["attempts"])[0].keys()) if result["attempts"] else ())
    write_csv(MODEL_PRESSURE_AUDIT_PATH, result["model_pressure_audit"], tuple(result["model_pressure_audit"][0].keys()) if result["model_pressure_audit"] else ())
    write_csv(CANDIDATE_ROLE_PRESSURE_PATH, result["candidate_role_pressure"], tuple(result["candidate_role_pressure"][0].keys()) if result["candidate_role_pressure"] else ())
    write_csv(ROUTE_GAP_AUDIT_PATH, result["route_gap_audit"], tuple(result["route_gap_audit"][0].keys()))
    write_csv(TIER_RECORD_REQUIREMENT_AUDIT_PATH, result["tier_record_requirement_audit"], tuple(result["tier_record_requirement_audit"][0].keys()))
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], tuple(result["failure_memory"][0].keys()) if result["failure_memory"] else ())
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("field", "value"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("field", "value"))
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"], ("field", "value"))
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], tuple(result["result_judgment"][0].keys()))

    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": result["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "attempts": result["attempts"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)

    lineage = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "inputs": result["inputs"],
        "outputs": result["outputs"],
        "availability": "tracked_generated_with_manifest_and_common_file_copies",
        "lineage_judgment": "connected_with_Tier_A_only_boundary",
        "boundary": CLAIM_BOUNDARY,
    }
    write_json(LINEAGE_PATH, lineage)

    artifact_hashes = {
        "pressure_design": sha256_file_lf_normalized(PRESSURE_DESIGN_PATH),
        "materialization_queue": sha256_file_lf_normalized(MATERIALIZATION_QUEUE_PATH),
        "variant_manifest": sha256_file_lf_normalized(VARIANT_MANIFEST_PATH),
        "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
        "attempt_manifest": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
        "model_pressure_audit": sha256_file_lf_normalized(MODEL_PRESSURE_AUDIT_PATH),
        "candidate_role_pressure": sha256_file_lf_normalized(CANDIDATE_ROLE_PRESSURE_PATH),
        "route_gap_audit": sha256_file_lf_normalized(ROUTE_GAP_AUDIT_PATH),
        "tier_record_requirement_audit": sha256_file_lf_normalized(TIER_RECORD_REQUIREMENT_AUDIT_PATH),
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
        "# Stage267 Run267AW Pool-wide State Feature Engineering Second Follow-up Materialization(267단계 267AW 후보군 전체 상태 피처 엔지니어링 2차 후속 물질화)",
        "",
        f"- action(행동): run267AV(267AV 실행)의 next experiment queue(다음 실험 큐)를 run267AX(267AX 실행)에서 돌릴 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.",
        "- effect(효과): Stage58(58단계) 이후 연구 단서를 다시 쓰되, 약한 월/요일 구멍을 달력 직접 필터로 덮지 않고 비달력 상태 압박(noncalendar state pressure, 비달력 상태 압박)으로 한 번 더 검증한다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AU(267AU 실행)에서 숫자가 좋아 보인 후보도 2024-12(2024년 12월)와 Monday(월요일) 구멍이 남았다.",
        "run267AV(267AV 실행)는 그래서 바로 후보를 고르지 않고, 한 번 더 넓은 상태 압박을 설계했다.",
        "run267AW(267AW 실행)는 그 설계를 실제 파일로 만들었다. 아직 성과 판정은 아니고, 다음 MT5 실행 대기 상태다.",
        "",
        "## Materialization Summary(물질화 요약)",
        "",
        f"- queue_rows(큐 행): `{result['queue_rows']}`",
        f"- ready_queue_rows(준비 큐 행): `{result['ready_queue_rows']}`",
        f"- candidates(후보): `{result['candidate_count']}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- Tier A attempts(티어 A 시도): `{result['attempt_count']}`",
        f"- model_pressure_audit passed(모델 압박 감사 통과): `{result['model_pressure_audit_pass_count']}/{result['variant_count']}`",
        f"- route_gap_rows(라우팅 공백 행): `{result['route_gap_rows']}`",
        f"- failure_memory_rows(실패 기억 행): `{result['failure_memory_rows']}`",
        "",
        "## Candidate Meaning(후보 의미)",
        "",
        "- `s264_aih`: core challenger(핵심 도전자) 유지 여부를 2차 range/volatility(범위/변동성) 압박으로 본다.",
        "- `s264_aia`: OOS anchor(표본외 앵커)는 Adapter watch(어댑터 관찰)일 뿐이며, 약한 구간이 줄어야 다음으로 간다.",
        "- `s264_lc`, `s262_lih`: control audit(기준 감사) 전용이다. 좋은 후보 선택 근거가 아니다.",
        "- `s258_stc`: stress challenger(압박 도전자)는 엄격한 가지치기/회수 gate(게이트)로만 본다.",
        "",
        "## Tier Boundary(티어 경계)",
        "",
        "- Tier A separate(Tier A 분리): `materialized`",
        "- Tier B separate(Tier B 분리): `blocked_missing_true_fallback_manifest`",
        "- actual routed total(실제 라우팅 전체): `blocked_missing_true_fallback_manifest`",
        "- effect(효과): 중복 Tier A+B(Tier A+B 합산) 행을 진짜 fallback(대체) 생존성으로 오해하지 않는다.",
        "",
        "## Outputs(산출물)",
        "",
        f"- pressure_design(압박 설계): `{rel(PRESSURE_DESIGN_PATH)}`",
        f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
        f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
        f"- model_pressure_audit(모델 압박 감사): `{rel(MODEL_PRESSURE_AUDIT_PATH)}`",
        f"- route_gap_audit(라우팅 공백 감사): `{rel(ROUTE_GAP_AUDIT_PATH)}`",
        f"- tier_record_requirement_audit(티어 기록 필요 감사): `{rel(TIER_RECORD_REQUIREMENT_AUDIT_PATH)}`",
        f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- effect(효과): 8개 MT5(MetaTrader 5, 메타트레이더5) Tier A(티어 A) 시도를 실행한 뒤 balance/equity curve(잔액/평가금 곡선), weak slice(약한 구간), trade quality(거래 품질)를 다시 본다.",
    ]
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    static = [
        ("stage267_run267AW_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267AW second follow-up inputs."),
        ("stage267_run267AW_pressure_design", "pressure_design", PRESSURE_DESIGN_PATH, "Run267AW second follow-up pressure design."),
        ("stage267_run267AW_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267AW materialization queue."),
        ("stage267_run267AW_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267AW variant manifest."),
        ("stage267_run267AW_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267AW runtime contract."),
        ("stage267_run267AW_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267AW MT5 attempt manifest."),
        ("stage267_run267AW_model_pressure_audit", "model_pressure_audit", MODEL_PRESSURE_AUDIT_PATH, "Run267AW model pressure audit."),
        ("stage267_run267AW_candidate_role_pressure", "candidate_role_pressure", CANDIDATE_ROLE_PRESSURE_PATH, "Run267AW candidate role pressure matrix."),
        ("stage267_run267AW_route_gap_audit", "route_gap_audit", ROUTE_GAP_AUDIT_PATH, "Run267AW true fallback route gap audit."),
        ("stage267_run267AW_tier_record_requirement_audit", "tier_record_requirement_audit", TIER_RECORD_REQUIREMENT_AUDIT_PATH, "Run267AW tier record requirement audit."),
        ("stage267_run267AW_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267AW failure memory."),
        ("stage267_run267AW_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267AW experiment design receipt."),
        ("stage267_run267AW_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267AW data integrity receipt."),
        ("stage267_run267AW_runtime_parity_receipt", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267AW runtime parity receipt."),
        ("stage267_run267AW_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AW result judgment."),
        ("stage267_run267AW_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267AW run manifest."),
        ("stage267_run267AW_lineage", "lineage", LINEAGE_PATH, "Run267AW lineage."),
        ("stage267_run267AW_review_result", "review_result_json", REVIEW_RESULT_PATH, "Run267AW review result JSON."),
        ("stage267_run267AW_report", "review_report", REPORT_PATH, "Run267AW review report."),
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
        "lane": "pool_wide_state_feature_engineering_second_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT),
        "notes": (
            f"variants={result['variant_count']};attempts={result['attempt_count']};"
            f"pressure_audit={result['model_pressure_audit_pass_count']}/{result['variant_count']};"
            f"route_gap_rows={result['route_gap_rows']};selected_candidate=none;onnx_readiness=not_claimed;"
            f"goal_achieve=not_claimed;next_action={NEXT_ACTION}."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_state_feature_engineering_second_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_state_feature_engineering_second_followup_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pool_wide_state_feature_engineering_second_followup_materialization",
        "tier_scope": "Tier A 2024 historical attempts planned; Tier B and actual routed total blocked until true fallback manifest exists",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "experiment_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};pressure_audit={result['model_pressure_audit_pass_count']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;mt5_execution=not_executed;true_fallback_manifest=missing",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    stage_row = {
        "row_id": "stage267_run267AW_pool_wide_state_feature_engineering_second_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_state_feature_engineering_second_followup_materialization",
        "tier_scope": "Tier A historical 2024 second follow-up attempts planned; Tier B blocked by route gap audit",
        "scoreboard": "feature_model_set_ini_manifest_pressure_audit_route_gap_audit",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};route_gap=confirmed;next_action={NEXT_ACTION}.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def update_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267AW_pool_wide_state_feature_engineering_second_followup_materialization(267AW 후보군 전체 상태 피처 엔지니어링 2차 후속 물질화): `{rel(REPORT_PATH)}`"

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_second_followup_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(current, "run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch", report_line)
    current = current.replace("run267AW_materialize_pool_wide_state_feature_engineering_second_followup_queue_from_run267AV_design", NEXT_ACTION)
    current = append_block_once(
        current,
        "Run267AW(267AW 실행)는 run267AV(267AV 실행)의 2차 후속 큐를 물질화했다.",
        "\n".join(
            [
                "Run267AW(267AW 실행)는 run267AV(267AV 실행)의 2차 후속 큐를 물질화했다.",
                f"Effect(효과): {result['variant_count']}개 variant(변형)와 {result['attempt_count']}개 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었고, Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 없어 route gap audit(라우팅 공백 감사)로 막아 두었다.",
                "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
            ]
        ),
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(selection, "run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch", report_line)
    selection = selection.replace("run267AW_materialize_pool_wide_state_feature_engineering_second_followup_queue_from_run267AV_design", NEXT_ACTION)
    selection = append_block_once(
        selection,
        "Run267AW(267AW 실행)는 pool-wide state feature engineering second follow-up materialization",
        "\n".join(
            [
                "Run267AW(267AW 실행)는 pool-wide state feature engineering second follow-up materialization(후보군 전체 상태 피처 엔지니어링 2차 후속 물질화)을 완료했다.",
                "Effect(효과): 다음 run267AX(267AX 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 실제 거래/곡선/시간구간 영향을 확인한다. 선택 후보(selected candidate, 선택 후보)는 없다.",
            ]
        ),
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{STATUS}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after_contains(review, "run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch", report_line)
    review = review.replace("run267AW_materialize_pool_wide_state_feature_engineering_second_followup_queue_from_run267AV_design", NEXT_ACTION)
    review = append_block_once(
        review,
        "Run267AW(267AW 실행)는 pool-wide state feature engineering second follow-up materialization",
        "\n".join(
            [
                "Run267AW(267AW 실행)는 pool-wide state feature engineering second follow-up materialization(후보군 전체 상태 피처 엔지니어링 2차 후속 물질화)을 완료했다.",
                f"Effect(효과): {result['variant_count']}개 2차 후속 variant(변형)와 {result['attempt_count']}개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었지만 아직 실행 결과가 아니므로 선택 후보(selected candidate, 선택 후보)는 없다.",
            ]
        ),
    )
    write_text(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus_block = (
        "- >-\n"
        f"  Stage267(267단계) run267AW(267AW 실행) pool-wide state feature engineering second follow-up materialization(후보군 전체 상태 피처 엔지니어링 2차 후속 물질화) `{STATUS}`. "
        f"Effect(효과): run267AV(267AV 실행)의 큐를 {result['variant_count']}개 variant(변형)와 {result['attempt_count']}개 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) 시도 입력으로 만들고, Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 없어 route gap audit(라우팅 공백 감사)로 막아 두었다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_design.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {source_design.RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {source_design.RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = append_after_contains(
        workspace,
        "run267AV_pool_wide_state_feature_engineering_followup_or_adapter_branch_report_path",
        f"  run267AW_pool_wide_state_feature_engineering_second_followup_materialization_report_path: {rel(REPORT_PATH)}",
    )
    workspace = workspace.replace("next_action: run267AW_materialize_pool_wide_state_feature_engineering_second_followup_queue_from_run267AV_design", f"next_action: {NEXT_ACTION}")
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
                "route_gap_rows": final_result["route_gap_rows"],
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
