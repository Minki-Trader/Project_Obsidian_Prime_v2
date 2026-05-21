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
from stage_pipelines.stage267 import run267AG_noncalendar_state_guard_followup_queue_materialization as source_materialization
from stage_pipelines.stage267 import run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review as source_review
from stage_pipelines.stage267 import run267AJ_noncalendar_state_guard_followup_design as source_design
from stage_pipelines.stage267 import run267W_true_internal_ablation_score_table_materialization as source_tables


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267AK"
RUN_ID = "run267AK_stage267_noncalendar_state_guard_repair_queue_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267AK_noncalendar_state_guard_repair_queue_materialized_execution_pending"
JUDGMENT = "repair_queue_materialized_execution_pending_no_candidate_selection"
NEXT_ACTION = "run267AL_execute_noncalendar_state_guard_repair_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_repair_queue_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_AJ_QUEUE_PATH = source_design.NEXT_EXPERIMENT_QUEUE_PATH
SOURCE_AJ_DECISION_PATH = source_design.CANDIDATE_DECISION_PATH
SOURCE_AJ_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_AJ_REPORT_PATH = source_design.REPORT_PATH
SOURCE_AG_VARIANT_MANIFEST_PATH = source_materialization.FOLLOWUP_VARIANT_MANIFEST_PATH
SOURCE_AG_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_AG_REPORT_PATH = source_materialization.REPORT_PATH
SOURCE_AI_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_AI_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_AI_TIER_DUPLICATE_REVIEW_PATH = source_review.TIER_DUPLICATE_REVIEW_PATH

REPAIR_QUEUE_PATH = RUN_ROOT / "repair_materialization_queue.csv"
REPAIR_VARIANT_MANIFEST_PATH = RUN_ROOT / "repair_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
MODEL_REPAIR_AUDIT_PATH = RUN_ROOT / "model_repair_audit.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
CANDIDATE_GATE_DECISION_PATH = RUN_ROOT / "candidate_gate_decision.csv"
DEFERRED_QUEUE_PATH = RUN_ROOT / "deferred_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AK_noncalendar_state_guard_repair_queue_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AK_noncalendar_state_guard_repair_queue_materialization.py")

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

COMMON_ROOT = "OPV2/s267ak/run267AK_noncalendar_state_guard_repair"
PERIOD_LABEL = input_probe.PERIOD_LABEL
CSV_MODEL_COLUMNS = source_materialization.CSV_MODEL_COLUMNS
MODEL_MATERIALIZATION_TYPE = "research_score_table_noncalendar_state_guard_repair_from_run267AJ_v1"

REPAIR_PROFILES: dict[str, tuple[tuple[float, float, float], ...]] = {
    "aia_dual_replacement_state_guard_repair_v3": (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-0.055, 0.110, -0.055),
        (-0.095, 0.190, -0.095),
        (-0.135, 0.270, -0.135),
    )
}

REPAIR_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_test_id",
    "source_queue_id",
    "source_run267AJ_queue_id",
    "repair_profile",
    "source_guard_state_features",
    "source_evidence",
    "materialization_status",
    "reason",
    "success_criteria",
    "failure_criteria",
    "stop_condition",
    "claim_boundary",
)

DEFERRED_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "candidate_scope",
    "workstream",
    "materialization_readiness",
    "defer_reason",
    "next_condition",
    "claim_boundary",
)

GATE_DECISION_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "run267AJ_decision_label",
    "run267AK_gate_decision",
    "materialized_variant_count",
    "deferred_reason",
    "next_condition",
    "claim_boundary",
)

VARIANT_COLUMNS = (
    "queue_id",
    "priority",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "source_test_id",
    "source_queue_id",
    "source_run267AJ_queue_id",
    "repair_profile",
    "model_materialization_type",
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
    "guard_score_feature_index",
    "source_guard_state_features",
    "runtime_rows",
    "signal_rows",
    "missing_feature_cells",
    "repair_terms",
    "neutral_bins_preserved",
    "claim_boundary",
)

CONTRACT_COLUMNS = (
    "queue_id",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "source_test_id",
    "shared_contract",
    "feature_count",
    "feature_order_hash",
    "model_backend",
    "model_materialization_type",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "max_hold_bars",
    "repair_profile",
    "known_difference",
    "runtime_claim_boundary",
)

AUDIT_COLUMNS = (
    "queue_id",
    "candidate_alias",
    "source_test_id",
    "source_model_file",
    "runtime_model_file",
    "repair_profile",
    "guard_score_feature_index",
    "repair_terms",
    "guard_score_rows",
    "changed_guard_score_rows",
    "non_guard_rows_changed",
    "neutral_bins_preserved",
    "audit_read",
)

ATTEMPT_COLUMNS = (
    "attempt_name",
    "queue_id",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "source_test_id",
    "source_queue_id",
    "repair_profile",
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
)

RECEIPT_COLUMNS = ("field", "value")
RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
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
    item = Path(path_text)
    return item if item.is_absolute() else REPO_ROOT / item


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


def require_inputs() -> None:
    required = [
        SOURCE_AJ_QUEUE_PATH,
        SOURCE_AJ_DECISION_PATH,
        SOURCE_AJ_FAILURE_MEMORY_PATH,
        SOURCE_AG_VARIANT_MANIFEST_PATH,
        SOURCE_AG_RUNTIME_CONTRACT_PATH,
        SOURCE_AI_CANDIDATE_TEST_REVIEW_PATH,
        SOURCE_AI_TIER_DUPLICATE_REVIEW_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def source_variants_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("source_test_id", "")): row
        for row in read_csv(SOURCE_AG_VARIANT_MANIFEST_PATH)
        if row.get("candidate_alias") and row.get("source_test_id")
    }


def source_contracts_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("source_test_id", "")): row
        for row in read_csv(SOURCE_AG_RUNTIME_CONTRACT_PATH)
        if row.get("candidate_alias") and row.get("source_test_id")
    }


def source_review_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row.get("candidate_alias", ""), row.get("source_test_id", "")): row
        for row in read_csv(SOURCE_AI_CANDIDATE_TEST_REVIEW_PATH)
        if row.get("candidate_alias") and row.get("source_test_id")
    }


def source_aj_queue_by_id() -> dict[str, dict[str, str]]:
    return {row["queue_id"]: row for row in read_csv(SOURCE_AJ_QUEUE_PATH)}


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
        "feature_order_hash": ordered_hash(feature_order),
        "missing_feature_cells": missing_cells,
    }


def copy_runtime_feature(source: Path, destination: Path) -> dict[str, Any]:
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    io_path(destination).write_bytes(io_path(source).read_bytes())
    meta = count_feature_rows(destination)
    meta.update({"runtime_feature_file": rel(destination), "runtime_feature_sha256": sha256_file_lf_normalized(destination)})
    return meta


def repair_terms_text(terms: Sequence[Sequence[float]]) -> str:
    return ";".join("/".join(f"{value:.3f}" for value in row) for row in terms)


def write_repair_model(source: Path, destination: Path, guard_feature_index: int, profile: str) -> dict[str, Any]:
    terms = REPAIR_PROFILES[profile]
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    changed_rows = 0
    guard_score_rows = 0
    non_guard_changed = False
    neutral_bins_preserved = True
    out_rows: list[dict[str, Any]] = []
    for row in rows:
        current = {column: row.get(column, "") for column in CSV_MODEL_COLUMNS}
        is_guard_score = (
            current.get("record_type") == "score"
            and as_int(current.get("feature_index"), -1) == int(guard_feature_index)
        )
        if is_guard_score:
            item_index = as_int(current.get("item_index"), -1)
            if item_index < 0 or item_index >= len(terms):
                raise RuntimeError(f"unexpected guard score item index {item_index} in {source}")
            guard_score_rows += 1
            old = (current.get("score_short"), current.get("score_flat"), current.get("score_long"))
            new = terms[item_index]
            current["score_short"] = f"{new[0]:.17g}"
            current["score_flat"] = f"{new[1]:.17g}"
            current["score_long"] = f"{new[2]:.17g}"
            if old != (current["score_short"], current["score_flat"], current["score_long"]):
                changed_rows += 1
            if item_index in {0, 1} and any(abs(value) > 1.0e-12 for value in new):
                neutral_bins_preserved = False
        out_rows.append(current)
    if guard_score_rows != len(terms):
        raise RuntimeError(f"guard score row count mismatch for {source}: {guard_score_rows} != {len(terms)}")
    write_runtime_csv(destination, out_rows, CSV_MODEL_COLUMNS)
    return {
        "source_runtime_model_file": rel(source),
        "runtime_model_file": rel(destination),
        "runtime_model_sha256": sha256_file_lf_normalized(destination),
        "repair_profile": profile,
        "repair_terms": repair_terms_text(terms),
        "guard_score_rows": guard_score_rows,
        "changed_guard_score_rows": changed_rows,
        "non_guard_rows_changed": non_guard_changed,
        "neutral_bins_preserved": neutral_bins_preserved,
    }


def build_repair_queue() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    aj_queue = source_aj_queue_by_id()
    q01 = aj_queue["run267AK_q01_s264_aia_dual_replacement_state_guard_repair"]
    review = source_review_by_alias_test()
    source_variants = source_variants_by_alias_test()
    selected = [
        ("run267AK_q01a_s264_aia_rep_trend_strength_adx_repair", "s264_aia", "rep_trend_strength_adx"),
        ("run267AK_q01b_s264_aia_rep_volatility_atr_repair", "s264_aia", "rep_volatility_atr"),
    ]
    queue_rows: list[dict[str, Any]] = []
    for queue_id, alias, test_id in selected:
        source = source_variants.get((alias, test_id))
        review_row = review.get((alias, test_id), {})
        queue_rows.append(
            {
                "queue_id": queue_id,
                "priority": "P0",
                "candidate_alias": alias,
                "candidate_id": source.get("candidate_id", "s264_allow_inner_all_oos_anchor") if source else "s264_allow_inner_all_oos_anchor",
                "candidate_role": source.get("candidate_role", "oos_anchor") if source else "oos_anchor",
                "source_test_id": test_id,
                "source_queue_id": source.get("queue_id", "") if source else "",
                "source_run267AJ_queue_id": q01["queue_id"],
                "repair_profile": "aia_dual_replacement_state_guard_repair_v3",
                "source_guard_state_features": source.get("source_guard_state_features", "") if source else "",
                "source_evidence": (
                    f"run267AI net={review_row.get('net_profit','')};pf={review_row.get('profit_factor','')};"
                    f"trades={review_row.get('trade_count','')};DD={review_row.get('report_equity_drawdown_percent','')};"
                    f"worst_month={review_row.get('worst_month','')}:{review_row.get('worst_month_net','')};"
                    f"worst_slice={review_row.get('worst_slice_axis','')}:{review_row.get('worst_slice_bucket','')}:{review_row.get('worst_slice_net','')}"
                ),
                "materialization_status": "ready_for_score_table_materialization" if source else "blocked_missing_source_variant",
                "reason": "materialize_run267AJ_P0_bounded_noncalendar_state_guard_repair_watch",
                "success_criteria": q01.get("success_criteria"),
                "failure_criteria": q01.get("failure_criteria"),
                "stop_condition": q01.get("stop_conditions"),
                "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
            }
        )
    deferred_rows: list[dict[str, Any]] = []
    for queue_id in (
        "run267AK_q02_s264_aih_core_role_prune_confirmation",
        "run267AK_q03_real_fallback_routing_probe_design",
        "run267AK_q04_broader_period_pressure_after_repair",
    ):
        row = aj_queue[queue_id]
        if queue_id.endswith("prune_confirmation"):
            defer_reason = "design_gate_only_s264_aih_needs_state_reason_before_any_new_materialization"
            next_condition = "only_materialize_if_s264_aia_repair_fails_or_specific_noncalendar_state_reason_is_named"
        elif "fallback" in queue_id:
            defer_reason = "real_Tier_B_fallback_probe_deferred_until_q01_survives"
            next_condition = "q01_MT5_review_survives_without_duplicate_Tier_A_plus_B_claim"
        else:
            defer_reason = "broader_period_pressure_deferred_until_repair_survives_2024"
            next_condition = "q01_or_q02_survivor_has_cleaner_2024_curve"
        deferred_rows.append(
            {
                "queue_id": row["queue_id"],
                "priority": row["priority"],
                "candidate_scope": row["candidate_scope"],
                "workstream": row["workstream"],
                "materialization_readiness": row["materialization_readiness"],
                "defer_reason": defer_reason,
                "next_condition": next_condition,
                "claim_boundary": "deferred_design_boundary_no_candidate_selection_no_onnx",
            }
        )
    return queue_rows, deferred_rows


def materialize_variant(
    queue_row: Mapping[str, Any],
    source_variant: Mapping[str, str],
    source_contract: Mapping[str, str],
    spec: Any,
    index: int,
) -> dict[str, Any]:
    alias = str(queue_row["candidate_alias"])
    test_id = str(queue_row["source_test_id"])
    queue_id = str(queue_row["queue_id"])
    profile = str(queue_row["repair_profile"])
    queue_token = safe_token(queue_id, 72)
    test_token = safe_token(test_id, 48)
    local_root = VARIANT_ROOT / alias / queue_token
    feature_path = local_root / "features" / f"{alias}_{test_token}_repair_guard.csv"
    model_path = local_root / "models" / f"{alias}_{test_token}_repair_guard_model.csv"

    feature_meta = copy_runtime_feature(repo_path(str(source_variant["runtime_feature_file"])), feature_path)
    guard_feature_index = as_int(source_variant.get("guard_score_feature_index"), feature_meta["feature_count"] - 1)
    model_meta = write_repair_model(repo_path(str(source_variant["runtime_model_file"])), model_path, guard_feature_index, profile)

    common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    feature_order = list(feature_meta["feature_order"])
    _full_order, _rank_column, gate_column = source_tables.candidate_full_feature_order(spec)
    attempts: list[dict[str, Any]] = []
    for role_index, (tier, attempt_role, prefix, token) in enumerate(
        (
            (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{safe_token(test_id, 28)}_repair", "ta"),
            (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_{safe_token(test_id, 28)}_repair", "rt"),
        ),
        start=1,
    ):
        magic = 26732000 + index * 100 + role_index
        payload = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=267,
            exploration_label=f"stage267_NoncalendarStateGuardRepair__{safe_token(test_id, 32)}",
            attempt_name=f"{queue_token}_{token}_2024",
            tier=tier,
            split=PERIOD_LABEL,
            model_path=common_model_path,
            model_id=f"{RUN_ID}_{alias}_{safe_token(test_id, 36)}_repair_guard_v1",
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
                "source_test_id": test_id,
                "source_queue_id": queue_row.get("source_queue_id"),
                "repair_profile": profile,
                "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                "execution_status": "not_executed",
            }
        )
        attempts.append(payload)

    variant = {
        "queue_id": queue_id,
        "priority": queue_row.get("priority"),
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": test_id,
        "source_queue_id": queue_row.get("source_queue_id"),
        "source_run267AJ_queue_id": queue_row.get("source_run267AJ_queue_id"),
        "repair_profile": profile,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
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
        "guard_score_feature_index": guard_feature_index,
        "source_guard_state_features": queue_row.get("source_guard_state_features"),
        "runtime_rows": feature_meta["rows"],
        "signal_rows": feature_meta["signal_rows"],
        "missing_feature_cells": feature_meta["missing_feature_cells"],
        "repair_terms": model_meta["repair_terms"],
        "neutral_bins_preserved": model_meta["neutral_bins_preserved"],
        "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
    }
    contract = {
        "queue_id": queue_id,
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": test_id,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;run267AG feature order;repair score-table terms;attempt set/ini identity",
        "feature_count": feature_meta["feature_count"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "short_threshold": as_float(source_contract.get("short_threshold"), spec.variant.short_threshold),
        "long_threshold": as_float(source_contract.get("long_threshold"), spec.variant.long_threshold),
        "min_margin": as_float(source_contract.get("min_margin"), 0.0),
        "max_hold_bars": as_int(source_contract.get("max_hold_bars"), spec.variant.max_hold_bars),
        "repair_profile": profile,
        "known_difference": "uses run267AG runtime feature surface and changes only guard score-table terms; no retraining and no calendar literal filter",
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }
    audit = {
        "queue_id": queue_id,
        "candidate_alias": alias,
        "source_test_id": test_id,
        "source_model_file": model_meta["source_runtime_model_file"],
        "runtime_model_file": model_meta["runtime_model_file"],
        "repair_profile": profile,
        "guard_score_feature_index": guard_feature_index,
        "repair_terms": model_meta["repair_terms"],
        "guard_score_rows": model_meta["guard_score_rows"],
        "changed_guard_score_rows": model_meta["changed_guard_score_rows"],
        "non_guard_rows_changed": model_meta["non_guard_rows_changed"],
        "neutral_bins_preserved": model_meta["neutral_bins_preserved"],
        "audit_read": "pass_guard_terms_only" if model_meta["neutral_bins_preserved"] and not model_meta["non_guard_rows_changed"] else "invalid",
    }
    if audit["audit_read"] != "pass_guard_terms_only":
        raise RuntimeError(f"repair model audit failed for {queue_id}: {audit}")
    return {"variant": variant, "contract": contract, "audit": audit, "attempts": attempts, "feature_path": feature_path, "model_path": model_path}


def build_candidate_gate_decisions(repair_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialized_count = {}
    for row in repair_queue:
        if row.get("materialization_status") == "ready_for_score_table_materialization":
            materialized_count[str(row.get("candidate_alias"))] = materialized_count.get(str(row.get("candidate_alias")), 0) + 1
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_AJ_DECISION_PATH):
        alias = row["candidate_alias"]
        if alias == "s264_aia":
            gate = "materialized_P0_bounded_repair_watch_not_selection"
            deferred_reason = ""
            next_condition = "run267AL_MT5_review_reduces_Monday_and_2024_12_without_trade_count_collapse"
        elif alias == "s264_aih":
            gate = "design_gate_only_core_role_prune_boundary"
            deferred_reason = "run267AJ_downgraded_core_role_and_no_specific_new_state_reason_named"
            next_condition = "only_reopen_if_s264_aia_fails_or_new_state_reason_is_named"
        else:
            gate = "preserved_role_no_new_run267AK_materialization"
            deferred_reason = "no_new_run267AI_evidence_for_this_candidate"
            next_condition = "pool_wide_queue_targets_candidate_again"
        rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": row.get("candidate_id"),
                "candidate_role": row.get("candidate_role"),
                "run267AJ_decision_label": row.get("run267AJ_decision_label"),
                "run267AK_gate_decision": gate,
                "materialized_variant_count": materialized_count.get(alias, 0),
                "deferred_reason": deferred_reason,
                "next_condition": next_condition,
                "claim_boundary": "no_selected_candidate_no_onnx_no_goal_achieve",
            }
        )
    return rows


def build_failure_memory() -> list[dict[str, Any]]:
    rows = [dict(row) for row in read_csv(SOURCE_AJ_FAILURE_MEMORY_PATH)]
    rows.append(
        {
            "memory_id": "run267AK_m06_materialized_only_guard_terms_changed",
            "pattern": "repair_materialization_changes_guard_score_table_terms_only",
            "evidence": "run267AK source feature files copied from run267AG; non_guard_model_rows unchanged by audit",
            "affected_scope": "s264_aia",
            "do_not_repeat": "do_not_claim_performance_improvement_before_run267AL_MT5_execution",
            "salvage_angle": "execute_and_review_balance_time_slice_trade_quality",
            "reopen_condition": "run267AL_shows_cleaner_2024_curve_without_trade_count_collapse",
            "boundary": "materialization_memory_no_kpi_claim",
        }
    )
    return rows


def build_receipts(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    design = [
        {"field": "hypothesis", "value": "run267AJ_s264_aia_constructive_rows_may_survive_a_bounded_noncalendar_state_guard_repair"},
        {"field": "decision_use", "value": "materialize_MT5_attempt_inputs_only_no_candidate_selection"},
        {"field": "comparison_baseline", "value": "run267AI s264_aia rep_trend_strength_adx and rep_volatility_atr Tier A rows"},
        {"field": "control_variables", "value": "same_2024_period_same_run267AG_feature_order_same_thresholds_same_RuntimeProbeEA"},
        {"field": "changed_variables", "value": "guard_score_table_terms_only_for_s264_aia_repair_profile"},
        {"field": "sample_scope", "value": "Tier A and Tier A+B 2024 historical runtime attempts planned; Tier A+B remains fallback-disabled duplicate boundary until real fallback probe"},
        {"field": "success_criteria", "value": "run267AL_trades_at_least_290_net_at_least_900_PF_at_least_1_35_DD_at_most_18_worst_month_above_minus_120_Monday_above_minus_180"},
        {"field": "failure_criteria", "value": "trade_count_collapse_or_Monday_or_December_hole_remains_deep"},
        {"field": "invalid_conditions", "value": "literal_weekday_month_filter_or_feature_order_untracked_or_non_guard_model_rows_changed"},
        {"field": "stop_conditions", "value": "stop_after_one_materialization_and_one_MT5_review_if_deep_holes_remain"},
        {"field": "evidence_plan", "value": "repair_queue;variant_manifest;runtime_contract;model_repair_audit;attempt_manifest;future_MT5_curve_review"},
    ]
    integrity = [
        {"field": "data_source", "value": f"{rel(SOURCE_AG_VARIANT_MANIFEST_PATH)} and {rel(SOURCE_AJ_QUEUE_PATH)}"},
        {"field": "time_axis", "value": "inherits run267AG runtime feature files and 2024 historical stress window"},
        {"field": "sample_scope", "value": "US100 M5 2024 historical stress; s264_aia two constructive replacement rows"},
        {"field": "missing_or_duplicate_check", "value": f"missing_feature_cells={result['missing_feature_cells']};source_variants_found={result['source_variants_found']}"},
        {"field": "feature_label_boundary", "value": "no new training label; score-table guard terms only"},
        {"field": "split_boundary", "value": "materialization only; MT5 execution and trade review remain pending"},
        {"field": "leakage_risk", "value": "repair selected after weak-slice review, so future MT5 result must be treated as exploratory"},
        {"field": "data_hash_or_identity", "value": f"variant_manifest={rel(REPAIR_VARIANT_MANIFEST_PATH)}"},
        {"field": "integrity_judgment", "value": "usable_with_boundary" if result["audit_pass_count"] == result["variant_count"] else "inconclusive"},
    ]
    judgment = [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"variants={result['variant_count']};attempts={result['attempt_count']};audit_pass={result['audit_pass_count']}/{result['variant_count']};deferred={result['deferred_queue_count']}",
            "evidence_missing": "MT5_execution;trade_list_review;balance_equity_curve;time_slice_KPI;trade_quality_after_repair;real_Tier_B_fallback",
            "judgment_label": JUDGMENT,
            "claim_boundary": "score_table_materialization_only_no_candidate_selection_no_onnx_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "좋아 보였던 s264_aia 두 줄만 실제 실행 입력으로 만들었고, 성능 판단은 다음 MT5 실행 뒤에만 할 수 있다.",
        }
    ]
    return design, integrity, judgment


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name", ""),
                "queue_id": attempt.get("queue_id", ""),
                "candidate_id": attempt.get("candidate_id", ""),
                "candidate_alias": attempt.get("candidate_alias", ""),
                "candidate_role": attempt.get("candidate_role", ""),
                "source_test_id": attempt.get("source_test_id", ""),
                "source_queue_id": attempt.get("source_queue_id", ""),
                "repair_profile": attempt.get("repair_profile", ""),
                "tier": attempt.get("tier", ""),
                "attempt_role": attempt.get("attempt_role", ""),
                "record_view_prefix": attempt.get("record_view_prefix", ""),
                "set_path": attempt.get("set", {}).get("path", ""),
                "set_sha256": attempt.get("set", {}).get("sha256", ""),
                "ini_path": attempt.get("ini", {}).get("path", ""),
                "ini_sha256": attempt.get("ini", {}).get("sha256", ""),
                "common_telemetry_path": attempt.get("common_telemetry_path", ""),
                "common_summary_path": attempt.get("common_summary_path", ""),
                "execution_status": attempt.get("execution_status", ""),
            }
        )
    return rows


def artifact_entry(artifact_id: str, artifact_type: str, path: Path, created_at: str, notes: str) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "notes": notes,
    }


def build_materialization() -> dict[str, Any]:
    require_inputs()
    repair_queue, deferred_queue = build_repair_queue()
    ready_rows = [row for row in repair_queue if row.get("materialization_status") == "ready_for_score_table_materialization"]
    source_variants = source_variants_by_alias_test()
    source_contracts = source_contracts_by_alias_test()
    specs = specs_by_alias()
    variants: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    dynamic_artifacts: list[dict[str, Any]] = []
    source_variants_found = 0
    for index, queue_row in enumerate(ready_rows, start=1):
        key = (str(queue_row["candidate_alias"]), str(queue_row["source_test_id"]))
        source_variant = source_variants.get(key)
        source_contract = source_contracts.get(key)
        if not source_variant or not source_contract:
            raise KeyError(f"missing run267AG source variant or contract for {key}")
        source_variants_found += 1
        spec = specs[str(queue_row["candidate_alias"])]
        item = materialize_variant(queue_row, source_variant, source_contract, spec, index)
        variants.append(item["variant"])
        contracts.append(item["contract"])
        audits.append(item["audit"])
        attempts.extend(item["attempts"])
        dynamic_artifacts.extend(
            [
                {
                    "artifact_id": f"stage267_run267AK_{safe_token(str(queue_row['queue_id']), 64)}_runtime_feature",
                    "artifact_type": "runtime_feature_csv",
                    "path": rel(item["feature_path"]),
                    "notes": f"Run267AK runtime feature CSV for {queue_row['queue_id']}.",
                },
                {
                    "artifact_id": f"stage267_run267AK_{safe_token(str(queue_row['queue_id']), 64)}_runtime_model",
                    "artifact_type": "runtime_model_csv",
                    "path": rel(item["model_path"]),
                    "notes": f"Run267AK repair EBM score table CSV for {queue_row['queue_id']}.",
                },
            ]
        )

    created_at = utc_now()
    gate_decisions = build_candidate_gate_decisions(repair_queue)
    failure_memory = build_failure_memory()
    result: dict[str, Any] = {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "candidate_count": len({row["candidate_alias"] for row in variants}),
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "deferred_queue_count": len(deferred_queue),
        "audit_pass_count": sum(1 for row in audits if row.get("audit_read") == "pass_guard_terms_only"),
        "source_variants_found": source_variants_found,
        "missing_feature_cells": sum(as_int(row.get("missing_feature_cells")) for row in variants),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "repair_queue": repair_queue,
        "deferred_queue": deferred_queue,
        "repair_variant_manifest": variants,
        "runtime_contract": contracts,
        "model_repair_audit": audits,
        "attempts": attempts,
        "candidate_gate_decision": gate_decisions,
        "failure_memory": failure_memory,
        "dynamic_artifacts": dynamic_artifacts,
        "inputs": {
            "run267AJ_queue": rel(SOURCE_AJ_QUEUE_PATH),
            "run267AJ_candidate_decision": rel(SOURCE_AJ_DECISION_PATH),
            "run267AJ_failure_memory": rel(SOURCE_AJ_FAILURE_MEMORY_PATH),
            "run267AG_variant_manifest": rel(SOURCE_AG_VARIANT_MANIFEST_PATH),
            "run267AG_runtime_contract": rel(SOURCE_AG_RUNTIME_CONTRACT_PATH),
            "run267AI_candidate_test_review": rel(SOURCE_AI_CANDIDATE_TEST_REVIEW_PATH),
            "run267AI_tier_duplicate_review": rel(SOURCE_AI_TIER_DUPLICATE_REVIEW_PATH),
        },
        "outputs": {
            "repair_queue": rel(REPAIR_QUEUE_PATH),
            "repair_variant_manifest": rel(REPAIR_VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "model_repair_audit": rel(MODEL_REPAIR_AUDIT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "candidate_gate_decision": rel(CANDIDATE_GATE_DECISION_PATH),
            "deferred_queue": rel(DEFERRED_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    design, integrity, judgment = build_receipts(result)
    result["experiment_design_receipt"] = design
    result["data_integrity_receipt"] = integrity
    result["result_judgment"] = judgment
    return result


def table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return lines


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267AK Noncalendar State Guard Repair Queue Materialization(267단계 267AK 비달력 상태 방어 수리 큐 물질화)",
        "",
        "- action(행동): run267AJ(267AJ 실행)의 P0 수리 큐를 score table/model/set/ini(점수표/모델/설정/초기화) 실행 입력으로 만들었다.",
        "- effect(효과): `s264_aia` 두 constructive row(건설적 행)를 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 같은 조건으로 시험할 수 있다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- attempts(시도): `{result['attempt_count']}`",
        f"- deferred_queue(보류 큐): `{result['deferred_queue_count']}`",
        f"- model_audit(모델 감사): `{result['audit_pass_count']}/{result['variant_count']}` pass(통과)",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "`s264_aia`의 두 줄만 실제 실행 대기 입력으로 만들었다.",
        "Effect(효과): 좋아 보였던 후보를 바로 고르지 않고, Monday(월요일)와 2024-12 구멍이 줄어드는지 다음 실행에서 본다.",
        "",
        "`s264_aih`는 이번 물질화에서 제외하고 gate(게이트)만 남겼다.",
        "Effect(효과): 약해진 core role(핵심 역할)을 계속 끌고 가는 repair loop(수리 반복)를 막는다.",
        "",
        "Tier A+B(Tier A+B 합산)는 아직 fallback disabled(대체 비활성) 경계다.",
        "Effect(효과): 다음 실행 결과가 나오더라도 real fallback routing(실제 대체 라우팅) 근거로 과장하지 않는다.",
        "",
        "## Repair Queue(수리 큐)",
        "",
        *table(
            result["repair_queue"],
            ("queue_id", "candidate_alias", "source_test_id", "repair_profile", "materialization_status", "success_criteria"),
        ),
        "",
        "## Deferred Queue(보류 큐)",
        "",
        *table(result["deferred_queue"], ("queue_id", "candidate_scope", "materialization_readiness", "defer_reason", "next_condition")),
        "",
        "## Candidate Gate(후보 게이트)",
        "",
        *table(result["candidate_gate_decision"], ("candidate_alias", "run267AJ_decision_label", "run267AK_gate_decision", "materialized_variant_count")),
        "",
        "## Evidence(근거)",
        "",
        f"- repair_variant_manifest(수리 변형 목록): `{rel(REPAIR_VARIANT_MANIFEST_PATH)}`",
        f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        f"- model_repair_audit(모델 수리 감사): `{rel(MODEL_REPAIR_AUDIT_PATH)}`",
        f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
        f"- run_manifest(실행 목록): `{rel(RUN_MANIFEST_PATH)}`",
        "",
        "## Result Judgment(결과 판정)",
        "",
        f"- result_subject(결과 대상): `{RUN_ID}`.",
        f"- evidence_available(사용 근거): variants(변형) `{result['variant_count']}`, attempts(시도) `{result['attempt_count']}`, audit_pass(감사 통과) `{result['audit_pass_count']}/{result['variant_count']}`.",
        "- evidence_missing(부족 근거): MT5 execution(MT5 실행), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질), real Tier B fallback(실제 Tier B 대체).",
        f"- judgment_label(판정 라벨): `{JUDGMENT}`.",
        "- claim_boundary(주장 경계): 물질화 완료만 주장한다. 선택 후보, ONNX 준비, 목표 달성은 주장하지 않는다.",
        f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
        "",
        "## Artifact Lineage(산출물 계보)",
        "",
        f"- source_inputs(원천 입력): `{rel(SOURCE_AJ_QUEUE_PATH)}`, `{rel(SOURCE_AG_VARIANT_MANIFEST_PATH)}`, `{rel(SOURCE_AI_CANDIDATE_TEST_REVIEW_PATH)}`.",
        f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
        f"- outputs(출력): `{rel(REPAIR_QUEUE_PATH)}`, `{rel(REPAIR_VARIANT_MANIFEST_PATH)}`, `{rel(ATTEMPT_MANIFEST_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        f"- consumer(소비자): `{NEXT_ACTION}`.",
        "- lineage_judgment(계보 판정): `connected_with_boundary`.",
    ]
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__noncalendar_state_guard_repair_queue_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_state_guard_repair_queue_materialization",
                "tier_scope": "Tier A and Tier A+B 2024 repair attempts planned; Tier A+B duplicate boundary retained",
                "scoreboard": "feature_model_set_ini_manifest",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "noncalendar_state_guard_repair_queue_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"Run267AK materialized run267AJ P0 repair queue; variants={result['variant_count']}; attempts={result['attempt_count']}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_repair_queue_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_state_guard_repair_queue_materialization",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "noncalendar_state_guard_repair_queue_materialization",
                "tier_scope": "Tier A and Tier A+B 2024 repair attempts planned; Tier A+B duplicate boundary retained",
                "kpi_scope": "materialization_no_mt5_kpi",
                "scoreboard_lane": "feature_model_set_ini_manifest",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};audit_pass={result['audit_pass_count']}/{result['variant_count']}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;mt5_execution=not_executed",
                "external_verification_status": "not_applicable_materialization_only",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        artifact_entry("stage267_run267AK_materialization_script", "producer_script", PRODUCER_PATH, created_at, "Builds run267AK repair materialization from run267AJ evidence."),
        artifact_entry("stage267_run267AK_repair_queue", "design_queue", REPAIR_QUEUE_PATH, created_at, "Run267AK repair materialization queue."),
        artifact_entry("stage267_run267AK_repair_variant_manifest", "variant_manifest", REPAIR_VARIANT_MANIFEST_PATH, created_at, "Run267AK repair variant manifest."),
        artifact_entry("stage267_run267AK_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, created_at, "Run267AK runtime contract."),
        artifact_entry("stage267_run267AK_model_repair_audit", "model_audit", MODEL_REPAIR_AUDIT_PATH, created_at, "Run267AK model repair audit."),
        artifact_entry("stage267_run267AK_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, created_at, "Run267AK MT5 attempt manifest."),
        artifact_entry("stage267_run267AK_candidate_gate_decision", "decision_matrix", CANDIDATE_GATE_DECISION_PATH, created_at, "Run267AK candidate gate decisions."),
        artifact_entry("stage267_run267AK_deferred_queue", "deferred_queue", DEFERRED_QUEUE_PATH, created_at, "Run267AK deferred queue."),
        artifact_entry("stage267_run267AK_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, created_at, "Run267AK failure memory."),
        artifact_entry("stage267_run267AK_experiment_design_receipt", "gate_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, created_at, "Run267AK experiment design receipt."),
        artifact_entry("stage267_run267AK_data_integrity_receipt", "gate_receipt", DATA_INTEGRITY_RECEIPT_PATH, created_at, "Run267AK data integrity receipt."),
        artifact_entry("stage267_run267AK_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, created_at, "Run267AK result judgment."),
        artifact_entry("stage267_run267AK_run_manifest", "run_manifest", RUN_MANIFEST_PATH, created_at, "Run267AK run manifest."),
        artifact_entry("stage267_run267AK_lineage", "lineage", LINEAGE_PATH, created_at, "Run267AK lineage."),
        artifact_entry("stage267_run267AK_review_result", "review_result", REVIEW_RESULT_PATH, created_at, "Run267AK review result JSON."),
        artifact_entry("stage267_run267AK_review_report", "review_report", REPORT_PATH, created_at, "User-facing run267AK report."),
    ]
    for row in result.get("dynamic_artifacts", []):
        artifact_rows.append(
            artifact_entry(str(row["artifact_id"]), str(row["artifact_type"]), repo_path(str(row["path"])), created_at, str(row.get("notes", "")))
        )
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_workspace_state_text(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_focus = "run267AK(" in text
    inserted_path = "run267AK_noncalendar_state_guard_repair_queue_materialization_report_path" in text
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AK(267AK 실행) noncalendar state guard repair queue materialization(비달력 상태 방어 수리 큐 물질화) `{STATUS}`. Effect(효과): run267AJ(267AJ 실행)의 P0 repair queue(P0 수리 큐)를 2개 variant(변형)와 4개 MT5(MetaTrader 5, 메타트레이더5) 시도 입력으로 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not inserted_focus:
            output.append(line)
            output.extend(focus_block)
            inserted_focus = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
            if "run267AJ_noncalendar_state_guard_followup_design_report_path" in stripped and not inserted_path:
                output.append(line)
                output.append(f"  run267AK_noncalendar_state_guard_repair_queue_materialization_report_path: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        output.append(line)
    if in_stage267 and not inserted_path:
        output.append(f"  run267AK_noncalendar_state_guard_repair_queue_materialization_report_path: {rel(REPORT_PATH)}")
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267AK_noncalendar_state_guard_repair_queue_materialization(267AK 비달력 상태 방어 수리 큐 물질화): `{rel(REPORT_PATH)}`"
    latest_line = (
        "- latest_materialization(최신 물질화): run267AK(267AK 실행) "
        f"variants(변형) `{result['variant_count']}`, attempts(시도) `{result['attempt_count']}`, "
        f"deferred queue(보류 큐) `{result['deferred_queue_count']}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AK(267AK 실행)는 run267AJ(267AJ 실행)의 P0 noncalendar state guard repair queue(비달력 상태 방어 수리 큐)를 물질화했다.",
            "Effect(효과): s264_aia 두 constructive row(건설적 행)는 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력이 되었고, s264_aih는 가지치기 gate(게이트)로 남았다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_repair_queue_materialization`")
            text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(
                text,
                "- action(",
                "- action(행동): run267AK(267AK 실행)는 run267AJ(267AJ 실행)의 P0 수리 큐를 score table/model/set/ini(점수표/모델/설정/초기화) 입력으로 만들었다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(",
                "- effect(효과): 다음 run267AL(267AL 실행)에서 s264_aia(264 AIA) 두 변형이 Monday(월요일)와 2024-12 구멍을 줄이는지 MT5(MetaTrader 5, 메타트레이더5)로 확인할 수 있다.",
            )
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267AJ_noncalendar_state_guard_followup_design", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
        else:
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            if path == SELECTION_STATUS_PATH:
                text = replace_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            if path == REVIEW_INDEX_PATH:
                text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
            text = append_after_contains(text, "run267AJ_noncalendar_state_guard_followup_design", report_line)
        text = append_block_once(text, "Run267AK(267AK 실행)는 run267AJ", closing_block)
        write_md(path, text)
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(read_text(WORKSPACE_STATE_PATH)))


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(REPAIR_QUEUE_PATH, result["repair_queue"], REPAIR_QUEUE_COLUMNS)
    write_csv(REPAIR_VARIANT_MANIFEST_PATH, result["repair_variant_manifest"], VARIANT_COLUMNS)
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"], CONTRACT_COLUMNS)
    write_csv(MODEL_REPAIR_AUDIT_PATH, result["model_repair_audit"], AUDIT_COLUMNS)
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_rows(result["attempts"]), ATTEMPT_COLUMNS)
    write_csv(CANDIDATE_GATE_DECISION_PATH, result["candidate_gate_decision"], GATE_DECISION_COLUMNS)
    write_csv(DEFERRED_QUEUE_PATH, result["deferred_queue"], DEFERRED_QUEUE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], source_design.FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], RECEIPT_COLUMNS)
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], RECEIPT_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "source_run_id": PARENT_RUN_ID,
            "variant_count": result["variant_count"],
            "attempt_count": result["attempt_count"],
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "repair_variant_manifest": rel(REPAIR_VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_PATH,
        {
            "created_at_utc": result["created_at_utc"],
            "run_id": RUN_ID,
            "source_inputs": result["inputs"],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": result["outputs"],
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def run() -> dict[str, Any]:
    result = build_materialization()
    write_outputs(result)
    update_ledgers(str(result["created_at_utc"]), result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = run()
    print(
        json.dumps(
            {
                "status": result["status"],
                "variants": result["variant_count"],
                "attempts": result["attempt_count"],
                "audit_pass": f"{result['audit_pass_count']}/{result['variant_count']}",
                "deferred_queue": result["deferred_queue_count"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
